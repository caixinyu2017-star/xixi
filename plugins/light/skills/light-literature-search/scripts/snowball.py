#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""snowball.py — 引用滚雪球（前向被引 + 后向参考）。

给一个种子（DOI / OpenAlex workid / 标题），抓取其引用邻居做一/两跳扩展：
- 后向（参考 references）：
    OpenAlex GET /works/{id} 取 referenced_works → 批量回填
      GET /works?filter=openalex_id:W..|W..（OR 竖线分批，每批 ≤50）。
    或 S2 GET /paper/{DOI:..}/references?fields=title,year,citationCount,isInfluential
      （offset/limit 分页）。
- 前向（被引 citations）：
    OpenAlex GET /works?filter=cites:{workid}&sort=cited_by_count:desc
      （注意是 cites: 过滤器，OpenAlex 无单独 cited_by 端点）。
    或 S2 GET /paper/{id}/citations（offset/limit 分页，带 isInfluential）。

诚实约定（见 d:/skill/Light/CONVENTIONS.md）：
- 不臆造 DOI/被引；被引数标来源库（OpenAlex vs S2 口径不同，不可直接比）。
- 网络不可用时回退到内置合成样本，保证 __main__ 可跑通并打印 [OFFLINE]。
- S2 的 citations/references 用 offset/limit 翻页；token 续翻只属于 /paper/search/bulk。
- 礼貌池邮箱经环境变量 OPENALEX_MAILTO / CROSSREF_MAILTO 或 --mailto 传入；不传则匿名（不伪造）。
- OpenAlex key 经 OPENALEX_API_KEY / --api-key 传入（2026 起需 key，口径见 references）；
  S2 可选 key 经 S2_API_KEY / --s2-api-key 传入。

用法：
    python scripts/snowball.py 10.1016/j.compag.2021.100001 --mailto you@inst.edu
    python scripts/snowball.py W2000000001 --hops 2 --provider openalex
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 复用 search_normalize 的规范化逻辑（同目录导入；失败则内联同名实现）。
try:
    from search_normalize import _norm_doi, _norm_title
except Exception:  # noqa: 单文件运行时的兜底
    def _norm_title(t: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", (t or "").lower())

    def _norm_doi(doi: str | None) -> str:
        if not doi:
            return ""
        d = doi.lower().strip()
        d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
        return d

MAILTO_ENV = (os.environ.get("OPENALEX_MAILTO") or os.environ.get("CROSSREF_MAILTO") or "").strip()
_MAILTO = MAILTO_ENV
_API_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
_S2_API_KEY = os.environ.get("S2_API_KEY", "").strip()
TIMEOUT = 30
PLACEHOLDER_MORE = None
# 限速/临时故障指数退避重试（零依赖、零费用）：免 key 走共享池高峰常 429。
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
    if _MAILTO:
        return "Light-literature-search/1.0 (mailto:%s)" % _MAILTO
    return "Light-literature-search/1.0"


def _oa_suffix() -> str:
    """OpenAlex 字符串型 URL 的礼貌池/key 后缀（拼在已有查询串后，故用 & 前缀按需追加）。"""
    extra = ""
    if _MAILTO:
        extra += "&mailto=" + urllib.parse.quote(_MAILTO, safe="")
    if _API_KEY:
        extra += "&api_key=" + urllib.parse.quote(_API_KEY, safe="")
    return extra


def _oa_dict(params: dict) -> dict:
    """OpenAlex dict 型参数：按需注入 mailto 与 api_key。"""
    p = dict(params)
    if _MAILTO:
        p["mailto"] = _MAILTO
    if _API_KEY:
        p["api_key"] = _API_KEY
    return p


def _get_json(url: str, headers: dict | None = None) -> tuple[int, Any]:
    """返回 (http_code, parsed_json_or_None)。任何异常吞掉返回 (0, None)。
    对 429/5xx 按指数退避自动重试（尊重 Retry-After，零依赖）。"""
    h = {"User-Agent": _user_agent(), "Accept": "application/json"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    last_code = 0
    for attempt in range(_MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                code = resp.getcode()
                data = json.loads(resp.read().decode("utf-8", "replace"))
                return code, data
        except urllib.error.HTTPError as e:  # noqa
            last_code = e.code
            if e.code in _RETRY_CODES and attempt < _MAX_RETRIES:
                _sleep(_retry_after(e, attempt))
                continue
            return e.code, None
        except Exception:  # noqa: network down / timeout / json error
            return 0, None
    return last_code, None


def _oa_id(workid: str) -> str:
    """归一化 OpenAlex work id：取末段 W... 大写。"""
    s = (workid or "").strip().rstrip("/")
    s = s.split("/")[-1]
    return s.upper() if s.upper().startswith("W") else s


def _rec_from_oa(w: dict, edge: str, is_infl: bool | None = None) -> dict:
    """OpenAlex work dict -> 统一邻居记录。edge: 'reference'|'citation'。"""
    auths = [a.get("author", {}).get("display_name", "")
             for a in w.get("authorships", [])][:8]
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    return {
        "edge": edge,
        "source_api": "OpenAlex",
        "title": w.get("title") or "",
        "authors": [a for a in auths if a],
        "year": w.get("publication_year"),
        "venue": src.get("display_name") or "",
        "doi": _norm_doi(w.get("doi")),
        "cited_by": w.get("cited_by_count"),
        "cited_by_src": "OpenAlex",
        "is_influential": is_infl,
        "oa_id": _oa_id(w.get("id") or ""),
        "url": w.get("id") or "",
    }


# ----------------------------- OpenAlex seed -----------------------------
def oa_resolve_seed(seed: str) -> tuple[int, dict | None]:
    """把种子（DOI / W-id / 标题）解析成一个 OpenAlex work（含 referenced_works）。"""
    sel = ("id,doi,title,publication_year,cited_by_count,authorships,"
           "primary_location,type,referenced_works")
    s = seed.strip()
    if s.upper().startswith("W") and re.fullmatch(r"[Ww]\d+", s):
        url = ("https://api.openalex.org/works/%s?select=%s%s"
               % (_oa_id(s), sel, _oa_suffix()))
    elif _norm_doi(s):
        url = ("https://api.openalex.org/works/doi:%s?select=%s%s"
               % (urllib.parse.quote(_norm_doi(s)), sel, _oa_suffix()))
    else:
        params = {"search": s, "per-page": "1", "select": sel}
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(_oa_dict(params))
        code, data = _get_json(url)
        if data and data.get("results"):
            return code, data["results"][0]
        return code, None
    code, data = _get_json(url)
    return code, data if isinstance(data, dict) and data.get("id") else None


# ----------------------------- OpenAlex backward -----------------------------
def oa_backward(seed_work: dict, max_refs: int = 50) -> tuple[int, list[dict]]:
    """后向参考：referenced_works → 分批 filter=openalex_id:W..|W..（每批 ≤50）。"""
    refs = [_oa_id(x) for x in (seed_work.get("referenced_works") or [])][:max_refs]
    out: list[dict] = []
    last_code = 0
    sel = ("id,doi,title,publication_year,cited_by_count,authorships,"
           "primary_location,type")
    for i in range(0, len(refs), 50):
        batch = refs[i:i + 50]
        flt = "openalex_id:" + "|".join(batch)  # OR 用竖线
        params = {"filter": flt, "per-page": "50", "select": sel}
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(_oa_dict(params))
        last_code, data = _get_json(url)
        if data and data.get("results"):
            for w in data["results"]:
                out.append(_rec_from_oa(w, "reference"))
    return last_code, out


# ----------------------------- OpenAlex forward -----------------------------
def oa_forward(seed_work: dict, limit: int = 50) -> tuple[int, list[dict]]:
    """前向被引：filter=cites:{workid}&sort=cited_by_count:desc（无单独端点）。"""
    wid = _oa_id(seed_work.get("id") or "")
    if not wid:
        return 0, []
    sel = ("id,doi,title,publication_year,cited_by_count,authorships,"
           "primary_location,type")
    params = {"filter": "cites:" + wid, "sort": "cited_by_count:desc",
              "per-page": str(min(limit, 200)), "select": sel}
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(_oa_dict(params))
    code, data = _get_json(url)
    out: list[dict] = []
    if data and data.get("results"):
        for w in data["results"]:
            out.append(_rec_from_oa(w, "citation"))
    return code, out


# ----------------------------- Semantic Scholar -----------------------------
def _s2_pid(seed: str) -> str:
    """把种子映射成 S2 paper id：DOI -> DOI:..；W-id 不被 S2 直接识别，回退原串。"""
    s = seed.strip()
    if _norm_doi(s) and not re.fullmatch(r"[Ww]\d+", s):
        return "DOI:" + _norm_doi(s)
    return s


def _rec_from_s2(p: dict, edge: str, is_infl: bool | None) -> dict:
    ext = p.get("externalIds") or {}
    return {
        "edge": edge,
        "source_api": "SemanticScholar",
        "title": p.get("title") or "",
        "authors": [a.get("name", "") for a in (p.get("authors") or [])][:8],
        "year": p.get("year"),
        "venue": p.get("venue") or "",
        "doi": _norm_doi(ext.get("DOI")),
        "cited_by": p.get("citationCount"),
        "cited_by_src": "SemanticScholar",
        "is_influential": is_infl,
        "oa_id": "",
        "url": p.get("url") or "",
    }


def s2_neighbors(seed: str, edge: str, limit: int = 50) -> tuple[int, list[dict]]:
    """S2 /paper/{id}/references|citations，offset/limit 分页（非 token）。"""
    pid = _s2_pid(seed)
    endpoint = "references" if edge == "reference" else "citations"
    inner = "title,year,citationCount,externalIds,venue,authors,url"
    fields = "isInfluential,%s" % inner
    base = ("https://api.semanticscholar.org/graph/v1/paper/%s/%s"
            % (urllib.parse.quote(pid, safe=":"), endpoint))
    out: list[dict] = []
    last_code = 0
    offset = 0
    page = min(limit, 100)
    s2_headers = {"x-api-key": _S2_API_KEY} if _S2_API_KEY else None
    while offset < limit:
        params = {"fields": fields, "offset": str(offset),
                  "limit": str(min(page, limit - offset))}
        url = base + "?" + urllib.parse.urlencode(params)
        last_code, data = _get_json(url, headers=s2_headers)
        items = (data or {}).get("data") or []
        if not items:
            break
        for it in items:
            paper = it.get("citingPaper" if edge == "citation"
                           else "citedPaper") or {}
            out.append(_rec_from_s2(paper, edge, it.get("isInfluential")))
        if (data or {}).get("next") is None:
            break
        offset += len(items)
    return last_code, out


# ----------------------------- 去重归并 -----------------------------
def dedup_neighbors(records: list[dict]) -> list[dict]:
    """邻居去重：DOI 优先，无 DOI 回退 规范化标题+年。合并边类型与被引来源。"""
    buckets: dict[str, dict] = {}
    for r in records:
        key = (_norm_doi(r.get("doi"))
               or (_norm_title(r.get("title")) + str(r.get("year") or "")))
        if not key:
            key = str(id(r))
        if key not in buckets:
            r = dict(r)
            r["edges"] = [r["edge"]]
            r["cited_by_by_src"] = {}
            if r.get("cited_by") is not None:
                r["cited_by_by_src"][r["cited_by_src"]] = r["cited_by"]
            buckets[key] = r
        else:
            b = buckets[key]
            if r["edge"] not in b["edges"]:
                b["edges"].append(r["edge"])
            if r.get("cited_by") is not None:
                b["cited_by_by_src"][r["cited_by_src"]] = r["cited_by"]
            if r.get("is_influential") and not b.get("is_influential"):
                b["is_influential"] = True
            if not b.get("doi") and r.get("doi"):
                b["doi"] = r["doi"]
    merged = list(buckets.values())

    def _sortkey(x: dict) -> int:
        vals = [v for v in x.get("cited_by_by_src", {}).values()
                if isinstance(v, int)]
        return max(vals) if vals else -1
    merged.sort(key=_sortkey, reverse=True)
    return merged


# ----------------------------- 编排 -----------------------------
def snowball(seed: str, hops: int = 1, provider: str = "openalex",
             limit: int = 50, offline_sample: bool = False,
             expand_top: int = 3, two_hop_direction: str = "backward") -> dict:
    offline = False
    all_recs: list[dict] = []
    seed_title = seed
    if not offline_sample:
        if provider == "s2":
            rc, refs = s2_neighbors(seed, "reference", limit)
            cc, cites = s2_neighbors(seed, "citation", limit)
            print("[HTTP] S2 references=%s citations=%s" % (rc, cc),
                  file=sys.stderr)
            all_recs = refs + cites
            if rc == 0 and cc == 0:
                offline = True
        else:
            sc, seed_work = oa_resolve_seed(seed)
            print("[HTTP] OpenAlex seed=%s" % sc, file=sys.stderr)
            if seed_work:
                seed_title = seed_work.get("title") or seed
                bc, refs = oa_backward(seed_work, max_refs=limit)
                fc, cites = oa_forward(seed_work, limit=limit)
                print("[HTTP] OpenAlex backward=%s forward=%s" % (bc, fc),
                      file=sys.stderr)
                all_recs = refs + cites
                # 两跳：对一跳邻居中被引最高的若干篇再扩展。
                # 方向可控（默认 backward 保持原行为、不增请求量）：
                #   backward=追根溯源（被引最高邻居的参考文献，找共同奠基工作）
                #   forward=追踪最新（被引最高邻居的后续被引，找前沿，请求量更大）
                #   both=两个方向都扩（最全但请求量最大）
                if hops >= 2 and (refs or cites):
                    one = dedup_neighbors(refs + cites)[:max(1, expand_top)]
                    for nb in one:
                        if not nb.get("oa_id"):
                            continue
                        c2, w2 = oa_resolve_seed(nb["oa_id"])
                        if not w2:
                            continue
                        if two_hop_direction in ("backward", "both"):
                            _, r2 = oa_backward(w2, max_refs=limit)
                            for x in r2:
                                x["edge"] = "reference"
                            all_recs += r2
                        if two_hop_direction in ("forward", "both"):
                            _, f2 = oa_forward(w2, limit=limit)
                            for x in f2:
                                x["edge"] = "citation"
                            all_recs += f2
            else:
                offline = True
    if offline_sample or offline:
        offline = True
        all_recs = _SYNTHETIC
        seed_title = seed
        print("[OFFLINE] 网络不可达，使用内置合成样本验证管线。", file=sys.stderr)
    merged = dedup_neighbors(all_recs)
    return {"seed": seed, "seed_title": seed_title, "provider": provider,
            "hops": hops, "two_hop_direction": two_hop_direction if hops >= 2 else None,
            "offline": offline, "raw_count": len(all_recs),
            "merged_count": len(merged), "neighbors": merged}


_SYNTHETIC = [
    {"edge": "reference", "source_api": "OpenAlex",
     "title": "Accelerometer-based activity recognition in goats",
     "authors": ["C Wang"], "year": 2019, "venue": "Animals",
     "doi": "10.3390/ani9120999", "cited_by": 45, "cited_by_src": "OpenAlex",
     "is_influential": None, "oa_id": "W2000000002", "url": "openalex:W2"},
    {"edge": "reference", "source_api": "SemanticScholar",
     "title": "Accelerometer-Based Activity Recognition in Goats",
     "authors": ["Chen Wang"], "year": 2019, "venue": "Animals",
     "doi": "10.3390/ani9120999", "cited_by": 52, "cited_by_src": "SemanticScholar",
     "is_influential": True, "oa_id": "", "url": "https://s2/paper2"},
    {"edge": "citation", "source_api": "OpenAlex",
     "title": "Deep learning for precision livestock farming",
     "authors": ["D Kim", "E Park"], "year": 2023,
     "venue": "Computers and Electronics in Agriculture",
     "doi": "10.1016/j.compag.2023.200200", "cited_by": 120,
     "cited_by_src": "OpenAlex", "is_influential": None,
     "oa_id": "W2000000003", "url": "openalex:W3"},
    {"edge": "citation", "source_api": "SemanticScholar",
     "title": "A review of sensor-based animal behaviour monitoring",
     "authors": ["F Li"], "year": 2022, "venue": "Sensors",
     "doi": "10.3390/s22010100", "cited_by": 78, "cited_by_src": "SemanticScholar",
     "is_influential": True, "oa_id": "", "url": "https://s2/paper4"},
]


def to_markdown(result: dict) -> str:
    nb = result["neighbors"]
    lines = [
        "# 引用滚雪球：%s" % result.get("seed_title", result["seed"]),
        "",
        "种子=`%s`  provider=%s  hops=%s  offline=%s" % (
            result["seed"], result["provider"], result["hops"],
            result["offline"]),
        "共 %d 个邻居（去重后，按被引降序）。被引数标来源库，"
        "OpenAlex/S2 口径不同不可直接比；Europe PMC/PubMed 又是另一口径。" % len(nb),
        "",
        "| # | 边类型 | infl | 标题 | 年 | 被引(来源) | DOI |",
        "|---|--------|------|------|----|-----------|-----|",
    ]
    for i, r in enumerate(nb, 1):
        cb = "; ".join("%s(%s)" % (v, k)
                       for k, v in r.get("cited_by_by_src", {}).items()) or "NA"
        edges = "+".join(r.get("edges", []))
        infl = "Y" if r.get("is_influential") else ""
        title = (r.get("title") or "").replace("|", "/")[:70]
        lines.append("| %d | %s | %s | %s | %s | %s | %s |" % (
            i, edges, infl, title, r.get("year") or "", cb, r.get("doi") or ""))
    return "\n".join(lines)



def _selftest() -> int:
    result = snowball("10.1016/j.compag.2021.100001", hops=1, provider="openalex", limit=5, offline_sample=True)
    assert result["offline"] is True, result
    assert result["raw_count"] >= 1 and result["merged_count"] >= 1, result
    md = to_markdown(result)
    assert "10.1016/j.compag.2021.100001" in md and result.get("merged_count", 0) >= 1, md

    # 两跳方向可控：mock 一跳/解析/扩展，验证 backward 只扩后向、both 两向都扩
    global oa_resolve_seed, oa_backward, oa_forward
    o_res, o_bwd, o_fwd = oa_resolve_seed, oa_backward, oa_forward
    log = {"bwd": 0, "fwd": 0}
    seed_w = {"id": "https://openalex.org/W1", "title": "seed", "referenced_works": ["W9"]}
    nb_rec = {"edge": "reference", "source_api": "OpenAlex", "title": "hop1",
              "doi": "10.1/hop1", "cited_by": 50, "cited_by_src": "OpenAlex",
              "is_influential": None, "oa_id": "W2", "url": "openalex:W2"}

    def fake_res(seed):
        return 200, (seed_w if str(seed).upper().startswith("10") or "W1" in str(seed)
                     else {"id": "https://openalex.org/W2", "title": "hop1node"})

    def fake_bwd(w, max_refs=50):
        log["bwd"] += 1
        return 200, [dict(nb_rec)]

    def fake_fwd(w, limit=50):
        log["fwd"] += 1
        return 200, [dict(nb_rec, edge="citation", doi="10.1/fwd", oa_id="W3")]
    try:
        oa_resolve_seed, oa_backward, oa_forward = fake_res, fake_bwd, fake_fwd
        # backward（默认）：一跳各 1 次 + 两跳只 backward
        log["bwd"] = log["fwd"] = 0
        snowball("10.1/seed", hops=2, expand_top=1, two_hop_direction="backward")
        assert log["fwd"] == 1 and log["bwd"] >= 2, log  # forward 仅一跳那次；backward 一跳+两跳
        # both：两跳两个方向都扩 → forward 被多调用
        log["bwd"] = log["fwd"] = 0
        snowball("10.1/seed", hops=2, expand_top=1, two_hop_direction="both")
        assert log["fwd"] >= 2 and log["bwd"] >= 2, log  # 一跳+两跳各方向都有
    finally:
        oa_resolve_seed, oa_backward, oa_forward = o_res, o_bwd, o_fwd

    print("[selftest] PASS snowball (含两跳方向 backward/forward/both)")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="引用滚雪球（前向被引+后向参考）")
    ap.add_argument("seed", nargs="?", default="10.1016/j.compag.2021.100001",
                    help="DOI / OpenAlex workid(W..) / 标题")
    ap.add_argument("--hops", type=int, default=1, choices=[1, 2])
    ap.add_argument("--expand-top", type=int, default=3,
                    help="两跳时对一跳邻居中被引最高的前 N 篇再扩展（默认 3，可配）")
    ap.add_argument("--two-hop-direction", default="backward",
                    choices=["backward", "forward", "both"],
                    help="两跳方向：backward追根溯源(默认)/forward追前沿(请求更多)/both全扩")
    ap.add_argument("--provider", default="openalex",
                    choices=["openalex", "s2"])
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--offline", action="store_true", help="强制用合成样本")
    ap.add_argument("--selftest", action="store_true", help="run offline synthetic self-test")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--md-out", default="")
    ap.add_argument("--mailto", default="",
                    help="礼貌池邮箱（也可设环境变量 OPENALEX_MAILTO / CROSSREF_MAILTO）；不传则匿名查")
    ap.add_argument("--api-key", default="",
                    help="OpenAlex API key（也可设环境变量 OPENALEX_API_KEY）；口径见本技能 references")
    ap.add_argument("--s2-api-key", default="",
                    help="Semantic Scholar API key（也可设环境变量 S2_API_KEY）；provider=s2 时提高限速")
    args = ap.parse_args()

    global _MAILTO, _API_KEY, _S2_API_KEY
    if args.mailto:
        _MAILTO = args.mailto.strip()
    if args.api_key:
        _API_KEY = args.api_key.strip()
    if args.s2_api_key:
        _S2_API_KEY = args.s2_api_key.strip()

    if args.selftest:
        sys.exit(_selftest())

    result = snowball(args.seed, hops=args.hops, provider=args.provider,
                      limit=args.limit, offline_sample=args.offline,
                      expand_top=args.expand_top,
                      two_hop_direction=args.two_hop_direction)
    md = to_markdown(result)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    if args.md_out:
        with open(args.md_out, "w", encoding="utf-8") as f:
            f.write(md)

    print(md)
    print("\n[SUMMARY] seed=%r provider=%s hops=%s offline=%s raw=%s merged=%s"
          % (args.seed, args.provider, args.hops, result["offline"],
             result["raw_count"], result["merged_count"]))


if __name__ == "__main__":
    main()
