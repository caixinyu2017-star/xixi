#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_citations.py — DOI 引用核验与幻觉引用标记。

思路（诚实第一）：
- 拿一条待核验引用（DOI + 声称的标题/作者/年/期刊），回 Crossref 内容协商
  (Accept: application/vnd.citationstyles.csl+json) 取权威元数据。
- 比对标题相似度、年份、首作者姓氏、期刊，给出 verdict：
  VERIFIED / METADATA_MISMATCH / DOI_NOT_FOUND（疑似幻觉）/ NO_DOI（需人工）。
- 产出核查报告（JSON + 文本）。

不臆造：DOI 解析失败即标 DOI_NOT_FOUND，不替用户脑补正确 DOI。

用法：
    python scripts/verify_citations.py            # 跑内置真实 DOI 自测
    python scripts/verify_citations.py 10.xxxx/yy --title "..." --year 2023
"""
from __future__ import annotations
import argparse
import difflib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from typing import Any

_MAILTO = (os.environ.get("CROSSREF_MAILTO") or os.environ.get("OPENALEX_MAILTO") or "").strip()
TIMEOUT = 30
# 限速/临时故障指数退避重试（零依赖、零费用）：doi.org/Crossref/arXiv 高峰偶限速。
_RETRY_CODES = {429, 502, 503, 504}
_MAX_RETRIES = 2
_BACKOFF_BASE = 0.5
_sleep = time.sleep


def _retry_after(e, attempt: int) -> float:
    ra = e.headers.get("Retry-After") if getattr(e, "headers", None) else None
    if ra:
        try:
            return min(float(ra), 8.0)
        except ValueError:
            pass
    return min(_BACKOFF_BASE * (2 ** attempt), 8.0)


def _urlopen_retry(req) -> tuple[int, bytes | None]:
    """统一打开请求，对 429/5xx 指数退避重试。返回 (http_code, raw_bytes_or_None)。
    HTTPError(非重试码) 返回 (code, None)；网络异常返回 (0, None)。"""
    last_code = 0
    for attempt in range(_MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.getcode(), resp.read()
        except urllib.error.HTTPError as e:  # noqa
            last_code = e.code
            if e.code in _RETRY_CODES and attempt < _MAX_RETRIES:
                _sleep(_retry_after(e, attempt))
                continue
            return e.code, None
        except Exception:  # noqa: network down / timeout
            return 0, None
    return last_code, None

# 标题比对告警阈值：声称标题 vs DOI 实际标题的 difflib 相似度低于此 → 标"标题相似度低"(疑似张冠李戴)。
# 经验默认值、可调：0.6 是保守线（归一化后明显不同才报），调高更敏感、调低更宽松。非数据反推。
TITLE_SIM_WARN = 0.6


def _user_agent() -> str:
    if _MAILTO:
        return "Light-literature-search/1.0 (mailto:%s)" % _MAILTO
    return "Light-literature-search/1.0"


def _norm_doi(doi: str) -> str:
    d = (doi or "").lower().strip()
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", d)


def _title_sim(a: str, b: str) -> float:
    na = re.sub(r"[^a-z0-9]+", " ", (a or "").lower()).strip()
    nb = re.sub(r"[^a-z0-9]+", " ", (b or "").lower()).strip()
    if not na or not nb:
        return 0.0
    return round(difflib.SequenceMatcher(None, na, nb).ratio(), 3)


def fetch_doi_csl(doi: str) -> tuple[int, dict | None]:
    """DOI 内容协商取 CSL-JSON。先打 doi.org，失败回退 Crossref /works/{doi}。
    429/5xx 由 _urlopen_retry 指数退避重试；404（DOI 不存在）不重试直接返回。"""
    doi = _norm_doi(doi)
    headers = {"User-Agent": _user_agent(), "Accept": "application/vnd.citationstyles.csl+json"}
    url = "https://doi.org/" + urllib.parse.quote(doi, safe="/().;:")
    code, raw = _urlopen_retry(urllib.request.Request(url, headers=headers))
    if code == 404:
        return 404, None
    if code == 200 and raw is not None:
        try:
            return 200, json.loads(raw.decode("utf-8", "replace"))
        except Exception:  # noqa: JSON 解析失败则回退 Crossref
            pass
    # 回退 Crossref
    cr = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/().;:")
    if _MAILTO:
        cr += "?mailto=" + urllib.parse.quote(_MAILTO, safe="")
    req2 = urllib.request.Request(cr, headers={"User-Agent": _user_agent(), "Accept": "application/json"})
    code2, raw2 = _urlopen_retry(req2)
    if code2 == 200 and raw2 is not None:
        try:
            return code2, json.loads(raw2.decode("utf-8", "replace")).get("message")
        except Exception:  # noqa
            return code2, None
    return code2, None


_ARXIV_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?$|^([a-z\-]+(\.[A-Z]{2})?/\d{7})")


def _extract_arxiv_id(s: str) -> str:
    """从字符串里抽 arXiv id（新式 2401.01234 或旧式 cs.AI/0701001）；抽不到返回空。"""
    s = (s or "").strip().replace("arXiv:", "").replace("arxiv:", "")
    m = _ARXIV_RE.search(s)
    if not m:
        return ""
    return (m.group(1) or m.group(3) or "").strip()


def verify_arxiv(arxiv_id: str) -> tuple[int, dict | None]:
    """打 export.arxiv.org/api/query 核验 arXiv id 是否真实存在，返回 (http_code, meta_or_None)。
    解决 arXiv-only（无 DOI）条目过去只能落 NO_DOI 的盲区。"""
    aid = _extract_arxiv_id(arxiv_id)
    if not aid:
        return 0, None
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"id_list": aid, "max_results": "1"})
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent()})
    code, raw_bytes = _urlopen_retry(req)
    if code != 200 or raw_bytes is None:
        return code, None
    raw = raw_bytes.decode("utf-8", "replace")
    # Atom 里有 <entry> 且 title 不是 "Error" 即命中（不引 XML 库，正则取 title）
    if "<entry>" not in raw:
        return code, None
    mt = re.search(r"<entry>.*?<title>(.*?)</title>", raw, re.S)
    title = re.sub(r"\s+", " ", (mt.group(1) if mt else "")).strip()
    if not title or title.lower() == "error":
        return code, None
    return code, {"arxiv_id": aid, "title": title}


def crossref_reverse_lookup(title: str, max_n: int = 3) -> list[dict]:
    """无 DOI 时按标题反查 Crossref 候选 DOI 给人工确认（不自动采信，只给候选）。"""
    if not (title or "").strip():
        return []
    params = {"query.bibliographic": title, "rows": str(max_n),
              "select": "DOI,title,author,issued"}
    if _MAILTO:
        params["mailto"] = _MAILTO
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent(), "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
    except Exception:
        return []
    out = []
    for it in (data.get("message", {}) or {}).get("items", [])[:max_n]:
        ttl = (it.get("title") or [""])[0]
        out.append({"doi": _norm_doi(it.get("DOI", "")), "title": ttl,
                    "title_sim": _title_sim(title, ttl)})
    return out


def _meta_from_csl(m: dict) -> dict:
    """CSL-JSON 或 Crossref message -> 统一元数据。"""
    title = m.get("title")
    if isinstance(title, list):
        title = title[0] if title else ""
    ct = m.get("container-title")
    if isinstance(ct, list):
        ct = ct[0] if ct else ""
    year = None
    for k in ("issued", "published", "published-print", "published-online"):
        dp = (m.get(k) or {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            year = dp[0][0]
            break
    authors = []
    for a in m.get("author", []) or []:
        fam = a.get("family") or a.get("name") or ""
        if fam:
            authors.append(fam)
    return {"title": title or "", "container": ct or "", "year": year, "authors": authors}


def verify_one(claim: dict) -> dict:
    """claim: {doi, title?, year?, first_author?}。返回核查结果。"""
    doi = _norm_doi(claim.get("doi", ""))
    rep: dict[str, Any] = {"claim": claim, "doi": doi}
    if not doi:
        # 无 DOI：先试 arXiv id 核验，再按标题反查 Crossref 候选 DOI（给人工确认，不自动采信）
        aid_src = claim.get("arxiv") or claim.get("arxiv_id") or claim.get("title", "") or claim.get("url", "")
        ax_code, ax_meta = verify_arxiv(aid_src) if _extract_arxiv_id(aid_src) else (0, None)
        if ax_meta:
            rep["verdict"] = "ARXIV_VERIFIED"
            rep["arxiv"] = ax_meta
            rep["http_code"] = ax_code
            if claim.get("title"):
                rep["title_similarity"] = _title_sim(claim["title"], ax_meta["title"])
            rep["note"] = ("arXiv 预印本核验存在（export.arxiv.org）；预印本未经同行评审，"
                          "引用须注明 preprint 或换正式发表版 DOI。")
            return rep
        candidates = crossref_reverse_lookup(claim.get("title", "")) if claim.get("title") else []
        rep["verdict"] = "NO_DOI"
        rep["candidates"] = candidates
        if candidates:
            rep["note"] = ("无 DOI；已按标题反查 Crossref 候选 DOI（见 candidates，按 title_sim 排序），"
                          "请人工确认是否匹配后补全 DOI 再核验——不自动采信。")
        else:
            rep["note"] = "无 DOI 且标题反查无候选，需人工查证（疑似来源不明）。"
        return rep
    code, meta = fetch_doi_csl(doi)
    rep["http_code"] = code
    if code == 404 or meta is None:
        rep["verdict"] = "DOI_NOT_FOUND"
        rep["note"] = "DOI 无法解析，疑似幻觉引用或 DOI 拼写错误。"
        return rep
    authoritative = _meta_from_csl(meta)
    rep["authoritative"] = authoritative
    issues = []
    # 标题比对
    if claim.get("title"):
        sim = _title_sim(claim["title"], authoritative["title"])
        rep["title_similarity"] = sim
        if sim < TITLE_SIM_WARN:
            issues.append(f"标题相似度低({sim}<{TITLE_SIM_WARN})：声称={claim['title']!r} vs 实际={authoritative['title']!r}")
    # 年份比对
    if claim.get("year") and authoritative.get("year"):
        if int(claim["year"]) != int(authoritative["year"]):
            issues.append(f"年份不符：声称={claim['year']} vs 实际={authoritative['year']}")
    # 首作者
    if claim.get("first_author") and authoritative.get("authors"):
        fa = claim["first_author"].split()[-1].lower()
        if fa not in [a.lower() for a in authoritative["authors"]]:
            issues.append(f"首作者姓氏未匹配：声称={claim['first_author']!r} vs 实际作者={authoritative['authors'][:3]}")
    rep["issues"] = issues
    rep["verdict"] = "VERIFIED" if not issues else "METADATA_MISMATCH"
    return rep


def verify_batch(claims: list[dict]) -> dict:
    results = [verify_one(c) for c in claims]
    summary = {}
    for r in results:
        summary[r["verdict"]] = summary.get(r["verdict"], 0) + 1
    return {"total": len(results), "summary": summary, "results": results}


def report_text(batch: dict) -> str:
    lines = ["# 引用核查报告", "",
             f"共 {batch['total']} 条。判定分布：{batch['summary']}", ""]
    flag = {"VERIFIED": "[OK]", "METADATA_MISMATCH": "[!]",
            "DOI_NOT_FOUND": "[幻觉?]", "NO_DOI": "[需人工]", "ARXIV_VERIFIED": "[arXiv预印本]"}
    for i, r in enumerate(batch["results"], 1):
        lines.append(f"## {i}. {flag.get(r['verdict'], '')} {r['verdict']}  DOI={r.get('doi') or 'NA'}")
        if r.get("http_code") is not None:
            lines.append(f"- HTTP={r['http_code']}")
        if r.get("authoritative"):
            a = r["authoritative"]
            lines.append(f"- 权威元数据：{a['title']!r} ({a['year']}) {a['container']!r} 作者={a['authors'][:3]}")
        if r.get("title_similarity") is not None:
            lines.append(f"- 标题相似度={r['title_similarity']}")
        for iss in r.get("issues", []):
            lines.append(f"- 问题：{iss}")
        if r.get("note"):
            lines.append(f"- 说明：{r['note']}")
        lines.append("")
    return "\n".join(lines)



def _selftest() -> int:
    """离线自测：猴子补丁 DOI 元数据获取，覆盖四类 verdict。"""
    print("[SELFTEST] verify_citations offline", file=sys.stderr)
    global fetch_doi_csl
    orig_fetch = fetch_doi_csl

    def fake_fetch(doi: str):
        doi = _norm_doi(doi)
        if doi == "10.1234/real":
            return 200, {
                "title": "Reliable citation verification",
                "container-title": "Journal of Testing",
                "issued": {"date-parts": [[2024]]},
                "author": [{"family": "Smith"}, {"family": "Wang"}],
            }
        return 404, None

    try:
        fetch_doi_csl = fake_fetch
        batch = verify_batch([
            {"doi": "10.1234/real", "title": "Reliable citation verification", "year": 2024, "first_author": "Smith"},
            {"doi": "10.1234/real", "title": "Fabricated goat title", "year": 1999, "first_author": "Nobody"},
            {"doi": "10.0000/missing", "title": "Phantom paper", "year": 2024},
            {"doi": "", "title": "No DOI"},
        ])
    finally:
        fetch_doi_csl = orig_fetch

    summary = batch["summary"]
    assert summary.get("VERIFIED") == 1, summary
    assert summary.get("METADATA_MISMATCH") == 1, summary
    assert summary.get("DOI_NOT_FOUND") == 1, summary
    assert summary.get("NO_DOI") == 1, summary
    txt = report_text(batch)
    assert "[OK]" in txt and "[幻觉?]" in txt and "[需人工]" in txt, txt

    # arXiv id 抽取
    assert _extract_arxiv_id("arXiv:2401.01234v2") == "2401.01234", _extract_arxiv_id("arXiv:2401.01234v2")
    assert _extract_arxiv_id("no id here") == "", "应抽不到"

    # 无 DOI 但有 arXiv id → ARXIV_VERIFIED（mock verify_arxiv）
    global verify_arxiv, crossref_reverse_lookup
    ova, ocrl = verify_arxiv, crossref_reverse_lookup
    try:
        verify_arxiv = lambda s: (200, {"arxiv_id": "2401.01234", "title": "A preprint on goats"})
        r_ax = verify_one({"doi": "", "arxiv": "arXiv:2401.01234", "title": "A preprint on goats"})
        assert r_ax["verdict"] == "ARXIV_VERIFIED" and r_ax["arxiv"]["arxiv_id"] == "2401.01234", r_ax
        # 无 DOI 无 arXiv 但有标题 → NO_DOI + 反查候选
        verify_arxiv = lambda s: (0, None)
        crossref_reverse_lookup = lambda t, max_n=3: [{"doi": "10.1/cand", "title": t, "title_sim": 0.9}]
        r_nd = verify_one({"doi": "", "title": "Some real title"})
        assert r_nd["verdict"] == "NO_DOI" and r_nd["candidates"][0]["doi"] == "10.1/cand", r_nd
    finally:
        verify_arxiv, crossref_reverse_lookup = ova, ocrl

    print("[selftest] PASS verify_citations offline (含 arXiv 核验 + 无DOI反查)")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="DOI 引用核验与幻觉标记")
    ap.add_argument("doi", nargs="?", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--year", default="")
    ap.add_argument("--first-author", default="")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--mailto", default="",
                    help="礼貌池邮箱（也可设环境变量 CROSSREF_MAILTO / OPENALEX_MAILTO）；不传则匿名查")
    ap.add_argument("--selftest", action="store_true", help="run offline synthetic self-test")
    args = ap.parse_args()

    global _MAILTO
    if args.mailto:
        _MAILTO = args.mailto.strip()

    if args.selftest or not args.doi:
        raise SystemExit(_selftest())

    if args.doi:
        claims = [{"doi": args.doi, "title": args.title or None,
                   "year": args.year or None, "first_author": args.first_author or None}]
    else:
        # 内置真实 DOI 自测：1 真实可核验 + 1 故意标题错配 + 1 伪造 DOI
        claims = [
            {"doi": "10.1038/s41597-023-02555-8",
             "title": "A dataset", "year": 2023, "first_author": None},
            {"doi": "10.1038/s41597-023-02555-8",
             "title": "Completely unrelated fabricated title about quantum goats",
             "year": 1999, "first_author": "Nobody"},
            {"doi": "10.0000/this-doi-does-not-exist-9999",
             "title": "Phantom paper", "year": 2024, "first_author": "Ghost"},
        ]
        print("[SELFTEST] 用 3 条样本核验：真实DOI / 标题年份错配 / 伪造DOI", file=sys.stderr)

    batch = verify_batch(claims)
    txt = report_text(batch)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)
    print(txt)
    print(f"[SUMMARY] {batch['summary']}")


if __name__ == "__main__":
    main()

