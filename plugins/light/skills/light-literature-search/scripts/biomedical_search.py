#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""biomedical_search.py — 生医文献检索（Europe PMC + PubMed E-utilities），输出统一文献表。

兑现 SKILL「生医纪律（必做）」：涉生医/临床/系统综述方向，PubMed+MeSH 检索式为必做项，
不能只靠 OpenAlex/S2 全文检索冒充规范检索。本脚本把两源做成可运行：
  1. Europe PMC REST /search：完全免 key，直接返回 abstractText/pmid/pmcid/doi/
     isOpenAcces/citedByCount，覆盖 MED+PMC+PPR。
  2. PubMed E-utilities：两步式 esearch.fcgi 取 PMID → esummary.fcgi 取详情；
     term 支持 [MeSH Terms]/[tiab]/[ti]/[au]/[dp] 等字段限定（MeSH 检索式由调用方写在
     term 里透传，本脚本不臆造词→MeSH 自动映射，那属 P2 增强，见 SKILL）。

跨源按 DOI 去重归并（无 DOI 回退 pmid / 规范化标题+年）。被引数标来源库（Europe PMC 的
citedByCount 与 OpenAlex/S2/Crossref 口径不同，不可直接比）。

诚实约定（见 d:/skill/Light/CONVENTIONS.md）：
- 不臆造 DOI/PMID/被引；取不到即如实留空，不脑补。
- 网络不可用时回退到内置合成样本，保证 __main__ 可跑通并打印 [OFFLINE]。
- 礼貌池/限流：Europe PMC 免 key；PubMed 无 key 3 req/s、有 key 10 req/s，
  key/email 经 --api-key / --email 或环境变量 NCBI_API_KEY / NCBI_EMAIL 传入（不伪造）。

用法：
    python scripts/biomedical_search.py "dairy goat mastitis" --per-page 10
    python scripts/biomedical_search.py "goat[tiab] AND lameness[MeSH Terms]" --source pubmed
    python scripts/biomedical_search.py --selftest
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# PubMed E-utilities 礼貌约定：email + 可选 api_key（无 key 3 req/s，有 key 10 req/s）。
# 经环境变量 NCBI_EMAIL / NCBI_API_KEY 或 --email / --api-key 传入；不传则匿名（不伪造）。
_EMAIL = os.environ.get("NCBI_EMAIL", "").strip()
_API_KEY = os.environ.get("NCBI_API_KEY", "").strip()
TIMEOUT = 30
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
# 限速/临时故障指数退避重试（零依赖、零费用）：PubMed 无 key 限 3 req/s 易 429。
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


def _user_agent() -> str:
    if _EMAIL:
        return "Light-literature-search/1.0 (mailto:%s)" % _EMAIL
    return "Light-literature-search/1.0"


def _get(url: str, accept: str = "application/json") -> tuple[int, str]:
    """返回 (http_code, raw_text)。网络/超时异常吞掉返回 (0, "")。
    对 429/5xx 按指数退避自动重试（尊重 Retry-After，零依赖）。"""
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent(), "Accept": accept})
    last_code = 0
    for attempt in range(_MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.getcode(), resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:  # noqa
            last_code = e.code
            if e.code in _RETRY_CODES and attempt < _MAX_RETRIES:
                _sleep(_retry_after(e, attempt))
                continue
            return e.code, ""
        except Exception:  # noqa: network down / timeout
            return 0, ""
    return last_code, ""


def _norm_doi(doi: str | None) -> str:
    if not doi:
        return ""
    d = doi.lower().strip()
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", d)


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())


def _rec(source_api: str, title: str, authors: list, year: Any, venue: str,
         doi: str, pmid: str, cited_by: Any, abstract: str, url: str,
         is_oa: Any = None) -> dict:
    """统一文献记录（对齐 search_normalize.py 字段，加 pmid / is_oa）。"""
    return {
        "source_api": source_api,
        "title": title or "",
        "authors": [a for a in (authors or []) if a],
        "year": year,
        "venue": venue or "",
        "doi": _norm_doi(doi),
        "pmid": pmid or "",
        "cited_by": cited_by,
        "cited_by_src": source_api,
        "abstract": abstract or "",
        "is_oa": is_oa,
        "url": url or "",
    }


# ----------------------------- Europe PMC -----------------------------
def search_europepmc(query: str, page_size: int = 10) -> tuple[int, list[dict]]:
    """Europe PMC /search（免 key）。resultType=core 直接带 abstract/被引/开放标记。"""
    params = {
        "query": query,
        "format": "json",
        "resultType": "core",
        "pageSize": str(max(1, min(page_size, 1000))),
    }
    url = f"{EPMC}/search?" + urllib.parse.urlencode(params)
    code, raw = _get(url)
    out: list[dict] = []
    if code == 200 and raw:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return code, out
        for r in (data.get("resultList") or {}).get("result", []):
            authors = []
            for a in (r.get("authorList") or {}).get("author", []) or []:
                nm = a.get("fullName") or a.get("lastName") or ""
                if nm:
                    authors.append(nm)
            yr = r.get("pubYear")
            out.append(_rec(
                "EuropePMC", r.get("title") or "", authors[:8],
                int(yr) if (yr and str(yr).isdigit()) else None,
                r.get("journalInfo", {}).get("journal", {}).get("title")
                or r.get("bookOrReportDetails", {}).get("publisher") or "",
                r.get("doi") or "", r.get("pmid") or "",
                r.get("citedByCount"),
                r.get("abstractText") or "",
                (f"https://europepmc.org/abstract/{r.get('source')}/{r.get('id')}"
                 if r.get("source") and r.get("id") else ""),
                is_oa=(str(r.get("isOpenAccess") or "").upper() == "Y"),
            ))
    return code, out


# ----------------------------- PubMed E-utilities -----------------------------
def _eutils_common() -> dict:
    """PubMed 礼貌参数：email + 可选 api_key（按需带，不伪造）。"""
    p = {}
    if _EMAIL:
        p["email"] = _EMAIL
    if _API_KEY:
        p["api_key"] = _API_KEY
    return p


def pubmed_esearch(term: str, retmax: int = 10) -> tuple[int, list[str]]:
    """esearch.fcgi 取 PMID 列表。term 原样透传（含 [MeSH Terms]/[tiab] 等字段限定）。"""
    params = {"db": "pubmed", "term": term, "retmax": str(max(1, min(retmax, 200))),
              "retmode": "json", "sort": "relevance"}
    params.update(_eutils_common())
    url = f"{EUTILS}/esearch.fcgi?" + urllib.parse.urlencode(params)
    code, raw = _get(url)
    if code == 200 and raw:
        try:
            return code, (json.loads(raw).get("esearchresult") or {}).get("idlist", []) or []
        except json.JSONDecodeError:
            return code, []
    return code, []


def pubmed_esummary(pmids: list[str]) -> tuple[int, list[dict]]:
    """esummary.fcgi 批量取详情。无 DOI/被引（PubMed 不出被引），DOI 从 articleids 提取。"""
    if not pmids:
        return 200, []
    params = {"db": "pubmed", "id": ",".join(pmids), "retmode": "json"}
    params.update(_eutils_common())
    url = f"{EUTILS}/esummary.fcgi?" + urllib.parse.urlencode(params)
    code, raw = _get(url)
    out: list[dict] = []
    if code == 200 and raw:
        try:
            res = (json.loads(raw).get("result") or {})
        except json.JSONDecodeError:
            return code, out
        for pid in res.get("uids", []) or []:
            r = res.get(pid, {})
            doi = ""
            for aid in r.get("articleids", []) or []:
                if aid.get("idtype") == "doi":
                    doi = aid.get("value", "")
            authors = [a.get("name", "") for a in (r.get("authors") or [])]
            yr = (r.get("pubdate") or "")[:4]
            out.append(_rec(
                "PubMed", r.get("title") or "", authors[:8],
                int(yr) if yr.isdigit() else None,
                r.get("fulljournalname") or r.get("source") or "",
                doi, pid, None, "",  # PubMed esummary 无 abstract/被引
                f"https://pubmed.ncbi.nlm.nih.gov/{pid}/",
            ))
    return code, out


def search_pubmed(term: str, retmax: int = 10) -> tuple[int, list[dict]]:
    """PubMed 两步式：esearch 取 PMID → esummary 取详情。"""
    code, pmids = pubmed_esearch(term, retmax)
    if code != 200 or not pmids:
        return code, []
    time.sleep(0.34)  # 无 key 限 3 req/s
    return pubmed_esummary(pmids)


# ----------------------------- 合并去重 -----------------------------
def merge_dedup(records: list[dict]) -> list[dict]:
    """跨源按 DOI 优先去重，无 DOI 回退 pmid / 规范化标题+年。保留信息更全的一条。"""
    by_key: dict[str, dict] = {}
    order = []
    for r in records:
        key = (r.get("doi") or "").strip()
        if not key:
            key = "pmid:" + r["pmid"] if r.get("pmid") else "t:" + _norm_title(r["title"]) + str(r.get("year") or "")
        if key not in by_key:
            by_key[key] = dict(r)
            order.append(key)
        else:
            cur = by_key[key]
            # 合并：补齐缺失字段、记录命中源
            for f in ("abstract", "doi", "pmid", "venue", "url"):
                if not cur.get(f) and r.get(f):
                    cur[f] = r[f]
            if cur.get("cited_by") is None and r.get("cited_by") is not None:
                cur["cited_by"] = r["cited_by"]
                cur["cited_by_src"] = r["cited_by_src"]
            srcs = set(cur["source_api"].split("+")) | {r["source_api"]}
            cur["source_api"] = "+".join(sorted(srcs))
    return [by_key[k] for k in order]


def run(query: str, source: str = "both", per_page: int = 10,
        offline_sample: bool = False) -> dict:
    offline = False
    records: list[dict] = []
    http: dict = {}
    if not offline_sample:
        if source in ("both", "europepmc"):
            c, recs = search_europepmc(query, per_page)
            http["europepmc"] = c
            records += recs
        if source in ("both", "pubmed"):
            c, recs = search_pubmed(query, per_page)
            http["pubmed"] = c
            records += recs
        if not records and all(v == 0 for v in http.values()):
            offline = True
    if offline_sample or offline:
        offline = True
        print("[OFFLINE] 网络不可达，使用内置合成样本验证管线。", file=sys.stderr)
        records = _offline_sample()
        http = {"europepmc": 0, "pubmed": 0}
    merged = merge_dedup(records)
    merged.sort(key=lambda r: (r.get("cited_by") or 0), reverse=True)
    return {"query": query, "source": source, "offline": offline,
            "http": http, "raw_count": len(records), "records": merged}


def _offline_sample() -> list[dict]:
    """无网时的合成样本（仅验证管线，明确标注非真实数据）。"""
    return [
        _rec("EuropePMC", "Automated lameness detection in dairy goats [SYNTHETIC]",
             ["Synthetic A", "Synthetic B"], 2022, "Synthetic Vet Journal",
             "10.0000/synthetic.epmc.1", "39000001", 7,
             "Synthetic abstract for offline pipeline test.", "https://example.org/epmc1", True),
        _rec("PubMed", "Automated lameness detection in dairy goats [SYNTHETIC]",
             ["Synthetic A", "Synthetic B"], 2022, "Synthetic Vet Journal",
             "10.0000/synthetic.epmc.1", "39000001", None, "",
             "https://pubmed.ncbi.nlm.nih.gov/39000001/"),
        _rec("PubMed", "Goat estrus behavior recognition [SYNTHETIC]",
             ["Synthetic C"], 2023, "Synthetic Anim Sci",
             "10.0000/synthetic.pm.2", "39000002", None, "",
             "https://pubmed.ncbi.nlm.nih.gov/39000002/"),
    ]


def to_markdown(records: list[dict], query: str) -> str:
    lines = [f"# 生医文献检索（Europe PMC + PubMed） query={query!r}\n",
             "| # | 标题 | 年 | venue | DOI | PMID | 被引(来源) | 源 |",
             "|---|------|----|-------|-----|------|-----------|----|"]
    for i, r in enumerate(records, 1):
        cb = "" if r.get("cited_by") is None else f"{r['cited_by']}({r['cited_by_src']})"
        lines.append("| %d | %s | %s | %s | %s | %s | %s | %s |" % (
            i, (r["title"] or "")[:60].replace("|", "/"), r.get("year") or "",
            (r.get("venue") or "")[:30].replace("|", "/"), r.get("doi") or "",
            r.get("pmid") or "", cb, r["source_api"]))
    return "\n".join(lines)


def _selftest() -> int:
    """离线自测：不打网，验证 Europe PMC/PubMed 解析、去重合并、MeSH term 透传。"""
    print("### biomedical_search 离线自测", file=sys.stderr)

    # 1) Europe PMC JSON 解析（mock _get 返回合成响应）
    global _get
    orig_get = _get
    epmc_json = json.dumps({"resultList": {"result": [{
        "id": "39000001", "source": "MED", "pmid": "39000001",
        "doi": "10.0000/X.1", "title": "Test goat paper", "pubYear": "2022",
        "citedByCount": 5, "isOpenAccess": "Y", "abstractText": "abstract here",
        "journalInfo": {"journal": {"title": "Vet J"}},
        "authorList": {"author": [{"fullName": "Zhang San"}]},
    }]}})

    def fake_get(url, accept="application/json"):
        if "europepmc" in url:
            return 200, epmc_json
        return 0, ""
    try:
        _get = fake_get
        code, recs = search_europepmc("goat", 5)
    finally:
        _get = orig_get
    assert code == 200 and len(recs) == 1, recs
    assert recs[0]["doi"] == "10.0000/x.1" and recs[0]["pmid"] == "39000001", recs[0]
    assert recs[0]["is_oa"] is True and recs[0]["cited_by"] == 5, recs[0]

    # 2) PubMed esummary 解析（mock）
    pm_json = json.dumps({"result": {"uids": ["39000002"], "39000002": {
        "title": "Another goat paper", "pubdate": "2023 Jun",
        "fulljournalname": "Anim Sci", "authors": [{"name": "Li Si"}],
        "articleids": [{"idtype": "doi", "value": "10.0000/Y.2"}],
    }}})

    def fake_get2(url, accept="application/json"):
        return 200, pm_json
    try:
        _get = fake_get2
        code, recs2 = pubmed_esummary(["39000002"])
    finally:
        _get = orig_get
    assert code == 200 and recs2[0]["doi"] == "10.0000/y.2", recs2
    assert recs2[0]["year"] == 2023 and recs2[0]["source_api"] == "PubMed", recs2[0]

    # 3) 跨源去重：同 DOI 两源合并为一条，source_api 记两源
    merged = merge_dedup([
        _rec("EuropePMC", "Same paper", ["A"], 2022, "J", "10.0/dup", "1", 9, "abs", "u1", True),
        _rec("PubMed", "Same paper", ["A"], 2022, "J", "10.0/dup", "1", None, "", "u2"),
    ])
    assert len(merged) == 1, merged
    assert merged[0]["source_api"] == "EuropePMC+PubMed", merged[0]
    assert merged[0]["cited_by"] == 9, merged[0]  # 保留有被引的一条

    # 4) MeSH 检索式透传：term 含 [MeSH Terms] 原样进 esearch URL（不改写、不臆造映射）
    captured = {}

    def fake_get3(url, accept="application/json"):
        captured["url"] = url
        return 200, json.dumps({"esearchresult": {"idlist": []}})
    try:
        _get = fake_get3
        pubmed_esearch("lameness[MeSH Terms] AND goat[tiab]", 5)
    finally:
        _get = orig_get
    assert "MeSH+Terms" in captured["url"] or "MeSH%20Terms" in captured["url"], captured["url"]

    # 5) 离线回退打通
    res = run("goat", offline_sample=True)
    assert res["offline"] is True and res["records"], res
    md = to_markdown(res["records"], "goat")
    assert "Europe PMC" in md or "EuropePMC" in md, md
    print("[selftest] PASS biomedical_search offline")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="生医文献检索（Europe PMC + PubMed E-utilities）")
    ap.add_argument("query", nargs="?", default="dairy goat mastitis")
    ap.add_argument("--source", default="both", choices=["both", "europepmc", "pubmed"])
    ap.add_argument("--per-page", type=int, default=10)
    ap.add_argument("--offline", action="store_true", help="强制用合成样本")
    ap.add_argument("--email", default="",
                    help="PubMed E-utilities 礼貌邮箱（也可设环境变量 NCBI_EMAIL）；不传则匿名")
    ap.add_argument("--api-key", default="",
                    help="NCBI API key（也可设环境变量 NCBI_API_KEY）；有 key 限速 10 req/s")
    ap.add_argument("--selftest", action="store_true", help="run offline synthetic self-test")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--md-out", default="")
    args = ap.parse_args()

    global _EMAIL, _API_KEY
    if args.email:
        _EMAIL = args.email.strip()
    if args.api_key:
        _API_KEY = args.api_key.strip()

    if args.selftest:
        sys.exit(_selftest())

    result = run(args.query, args.source, args.per_page, offline_sample=args.offline)
    md = to_markdown(result["records"], args.query)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    if args.md_out:
        with open(args.md_out, "w", encoding="utf-8") as f:
            f.write(md)
    print(md)
    print("\n[SUMMARY] query=%r source=%s offline=%s raw=%s merged=%s http=%s" % (
        args.query, args.source, result["offline"], result["raw_count"],
        len(result["records"]), result["http"]), file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--selftest":
        _selftest()
    else:
        main()



