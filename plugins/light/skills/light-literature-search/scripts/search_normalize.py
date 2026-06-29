#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""search_normalize.py — 多源文献检索与规范化（OpenAlex + Crossref）。

功能：
1. urllib 直连 OpenAlex /works 与 Crossref /works（无第三方依赖，按需带 mailto 进礼貌池）。
2. 还原 OpenAlex 的 abstract_inverted_index 为正文摘要。
3. 跨源按 DOI 去重归并（无 DOI 回退到 规范化标题+年）。
4. 按 cited_by 排序。
5. 输出统一文献表：JSON + Markdown。

诚实约定（见 d:/skill/Light/CONVENTIONS.md）：
- 不臆造 DOI/被引；被引数标来源库（OpenAlex vs Crossref 口径不同，不可直接比）。
- 网络不可用时回退到内置合成样本，保证 __main__ 可跑通并打印 [OFFLINE] 标记。
- 礼貌池邮箱经环境变量 OPENALEX_MAILTO / CROSSREF_MAILTO 或 --mailto 传入；不传则匿名（不伪造）。
- OpenAlex key 经环境变量 OPENALEX_API_KEY 或 --api-key 传入（2026 起需 key，口径见 references）。

用法：
    python scripts/search_normalize.py "dairy goat behavior" --per-page 10 --mailto you@inst.edu
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

# 礼貌池邮箱：优先环境变量 OPENALEX_MAILTO / CROSSREF_MAILTO，其次 --mailto，不传则匿名（不伪造）。
# 不再硬编码伪造邮箱（旧版硬编码了一个 example.com 占位邮箱，违反 OpenAlex/Crossref 礼貌池约定且无意义）。
# OpenAlex API key：2026 起 OpenAlex 需免费 key，经 --api-key 或环境变量 OPENALEX_API_KEY 传入；
# key/限流/计费的唯一口径见本技能 references「OpenAlex 接入真相源」节，本脚本不复写数字。
_MAILTO = (os.environ.get("OPENALEX_MAILTO") or os.environ.get("CROSSREF_MAILTO") or "").strip()
_API_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
TIMEOUT = 30
# 限速/临时故障重试：免 key 匿名走共享池，高峰常 429；503/502/504 是上游临时故障。
# 用指数退避自动重试（零依赖、零费用，纯 time.sleep），尊重服务端 Retry-After 头。
# references「OpenAlex 接入真相源」要求"遇 429 指数退避"——此处兑现。
_RETRY_CODES = {429, 502, 503, 504}
_MAX_RETRIES = 2          # 首次失败后最多再试 2 次（共 3 次尝试）
_BACKOFF_BASE = 0.5       # 退避基数秒：0.5 → 1.0 → 2.0（指数）
_sleep = time.sleep       # 可注入点：selftest 替换为无操作，避免真睡


def _retry_after(e: "urllib.error.HTTPError", attempt: int) -> float:
    """计算退避秒数：优先服务端 Retry-After 头，否则指数退避（带上限 8s）。"""
    ra = e.headers.get("Retry-After") if getattr(e, "headers", None) else None
    if ra:
        try:
            return min(float(ra), 8.0)  # 只认数值秒；HTTP-date 形式忽略走指数
        except ValueError:
            pass
    return min(_BACKOFF_BASE * (2 ** attempt), 8.0)



def _user_agent() -> str:
    if _MAILTO:
        return "Light-literature-search/1.0 (mailto:%s)" % _MAILTO
    return "Light-literature-search/1.0"


def _oa_params(params: dict) -> dict:
    """给 OpenAlex 查询参数按需注入 mailto（礼貌池）与 api_key（2026 起需 key）。"""
    p = dict(params)
    if _MAILTO:
        p["mailto"] = _MAILTO
    if _API_KEY:
        p["api_key"] = _API_KEY
    return p


def _cr_params(params: dict) -> dict:
    """给 Crossref 查询参数按需注入 mailto（礼貌池）。Crossref 不需 api_key。"""
    p = dict(params)
    if _MAILTO:
        p["mailto"] = _MAILTO
    return p


def _get_json(url: str) -> tuple[int, Any]:
    """返回 (http_code, parsed_json_or_None)。任何异常吞掉返回 (0, None)。
    对 429/5xx 限速与临时故障按指数退避自动重试（尊重 Retry-After，零依赖）。"""
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent(), "Accept": "application/json"})
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


def restore_abstract(inv: dict | None) -> str:
    """OpenAlex abstract_inverted_index -> 正文。inv: {word: [pos,...]}。"""
    if not inv:
        return ""
    positions: list[tuple[int, str]] = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort(key=lambda x: x[0])
    return " ".join(w for _, w in positions)


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())


def _norm_doi(doi: str | None) -> str:
    if not doi:
        return ""
    d = doi.lower().strip()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d


# ----------------------------- OpenAlex -----------------------------
def _oa_rec(w: dict) -> dict:
    """OpenAlex work -> 统一记录。"""
    auths = [a.get("author", {}).get("display_name", "")
             for a in w.get("authorships", [])][:8]
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    return {
        "source_api": "OpenAlex",
        "title": w.get("title") or "",
        "authors": [a for a in auths if a],
        "year": w.get("publication_year"),
        "venue": src.get("display_name") or "",
        "doi": _norm_doi(w.get("doi")),
        "cited_by": w.get("cited_by_count"),
        "cited_by_src": "OpenAlex",
        "type": w.get("type") or "",
        "abstract": restore_abstract(w.get("abstract_inverted_index")),
        "url": w.get("id") or "",
        "oa_relevance": w.get("relevance_score"),  # OpenAlex 服务端相关度,供时效综合重排
        "referenced_works": w.get("referenced_works") or [],
    }


def search_openalex(query: str, per_page: int = 10, from_date: str = "",
                    max_results: int = 0, sort_by: str = "relevance") -> tuple[int, list[dict]]:
    """OpenAlex /works 检索。max_results>per_page 时用 cursor=* 深翻页直到取够或翻完
    （让"穷尽"深度档真可用）；max_results<=0 表示只取一页 per_page 条（默认行为）。
    sort_by: 'relevance'（相关度排序，治宽 query 顶跑题高被引文，默认）/ 'cited'（被引降序）。
    实测 relevance_score:desc 可与 cursor 深翻页并用（HTTP 200）。"""
    select = ("id,doi,title,publication_year,cited_by_count,"
              "authorships,primary_location,abstract_inverted_index,type,referenced_works,relevance_score")
    oa_sort = "cited_by_count:desc" if sort_by == "cited" else "relevance_score:desc"
    target = max_results if max_results and max_results > per_page else per_page
    page_size = min(200, target)  # OpenAlex 单页上限 200
    out: list[dict] = []
    cursor = "*"
    last_code = 0
    while len(out) < target:
        params = {"search": query, "per-page": str(page_size),
                  "sort": oa_sort, "select": select, "cursor": cursor}
        if from_date:
            params["filter"] = "from_publication_date:" + from_date
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(_oa_params(params))
        last_code, data = _get_json(url)
        if not data or "results" not in data:
            break
        out += [_oa_rec(w) for w in data["results"]]
        cursor = ((data.get("meta") or {}).get("next_cursor"))
        if not cursor or not data["results"]:
            break  # 翻完了
    return last_code, out[:target]


# ----------------------------- Crossref -----------------------------
def _cr_rec(it: dict) -> dict:
    """Crossref item -> 统一记录。"""
    auths = []
    for a in it.get("author", []) or []:
        nm = (a.get("given", "") + " " + a.get("family", "")).strip()
        if nm:
            auths.append(nm)
    year = None
    dp = it.get("issued", {}).get("date-parts", [[None]])
    if dp and dp[0]:
        year = dp[0][0]
    ct = it.get("container-title") or [""]
    ttl = it.get("title") or [""]
    abs = re.sub(r"<[^>]+>", "", it.get("abstract", "") or "").strip()
    return {
        "source_api": "Crossref",
        "title": ttl[0] if ttl else "",
        "authors": auths[:8],
        "year": year,
        "venue": ct[0] if ct else "",
        "doi": _norm_doi(it.get("DOI")),
        "cited_by": it.get("is-referenced-by-count"),
        "cited_by_src": "Crossref",
        "type": it.get("type") or "",
        "abstract": abs,
        "url": "https://doi.org/" + it.get("DOI") if it.get("DOI") else "",
    }


def search_crossref(query: str, rows: int = 10, from_date: str = "",
                    max_results: int = 0, sort_by: str = "relevance") -> tuple[int, list[dict]]:
    """Crossref /works 检索。max_results>rows 时用 cursor=* 深翻页（Crossref deep paging）。
    sort_by: 'relevance'（相关度排序，治跑题，默认）/ 'cited'（被引降序）。"""
    select = "DOI,title,author,issued,container-title,is-referenced-by-count,type,abstract"
    target = max_results if max_results and max_results > rows else rows
    page_size = min(100, target)  # 礼貌取 ≤100
    out: list[dict] = []
    cursor = "*"
    last_code = 0
    while len(out) < target:
        params = {"query.bibliographic": query, "rows": str(page_size),
                  "sort": ("is-referenced-by-count" if sort_by == "cited" else "relevance"),
                  "order": "desc", "select": select, "cursor": cursor}
        if from_date:
            params["filter"] = "from-pub-date:" + from_date
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode(_cr_params(params))
        last_code, data = _get_json(url)
        items = (data or {}).get("message", {}).get("items") if data else None
        if not items:
            break
        out += [_cr_rec(it) for it in items]
        cursor = ((data.get("message") or {}).get("next-cursor"))
        if not cursor:
            break
    return last_code, out[:target]


# ----------------------------- DOAJ（开放获取期刊，完全免 key）-----------------------------
def _doaj_rec(it: dict) -> dict:
    """DOAJ article -> 统一记录。DOAJ 按相关度排序，补 OpenAlex/Crossref 纯被引排序的盲区。"""
    b = it.get("bibjson", {}) or {}
    ids = b.get("identifier", []) or []
    doi = next((x.get("id") for x in ids if x.get("type") == "doi"), "") or ""
    auths = [a.get("name", "") for a in (b.get("author") or [])][:8]
    jr = b.get("journal", {}) or {}
    yr = b.get("year")
    return {
        "source_api": "DOAJ",
        "title": b.get("title") or "",
        "authors": [a for a in auths if a],
        "year": int(yr) if (yr and str(yr).isdigit()) else None,
        "venue": jr.get("title") or "",
        "doi": _norm_doi(doi),
        "cited_by": None,            # DOAJ 不出被引（不臆造）
        "cited_by_src": None,
        "type": "article",
        "abstract": b.get("abstract") or "",
        "url": ("https://doi.org/" + doi) if doi else (b.get("link", [{}])[0].get("url", "") if b.get("link") else ""),
        "is_oa": True,               # DOAJ 收录的都是开放获取
    }


def search_doaj(query: str, per_page: int = 10) -> tuple[int, list[dict]]:
    """DOAJ /search/articles（完全免 key）。按相关度排序，补开放获取/小众刊盲区。"""
    q = urllib.parse.quote(query, safe="")
    url = ("https://doaj.org/api/v2/search/articles/%s?pageSize=%d"
           % (q, max(1, min(per_page, 100))))
    code, data = _get_json(url)
    if not data or "results" not in data:
        return code, []
    return code, [_doaj_rec(it) for it in data["results"]]


# ----------------------------- 去重归并 -----------------------------
def dedup_merge(records: list[dict], sort_by: str = "cited") -> list[dict]:
    """跨源按 DOI 优先归并；无 DOI 回退 规范化标题+年。
    sort_by: 'cited' 合并后按被引降序（默认，兼容旧行为）；
             'relevance' 保留各源 API 返回的相关度序（dict 插入序=首次出现序，不重排，
             否则会把各源的相关度排序抹成被引序，白费 relevance 检索）。"""
    buckets: dict[str, dict] = {}
    for r in records:
        key = _norm_doi(r.get("doi")) or (_norm_title(r.get("title")) + str(r.get("year") or ""))
        if not key:
            key = str(id(r))
        if key not in buckets:
            r = dict(r)
            r["cited_by_by_src"] = {}
            if r.get("cited_by") is not None:
                r["cited_by_by_src"][r["cited_by_src"]] = r["cited_by"]
            r["sources"] = [r["source_api"]]
            buckets[key] = r
        else:
            b = buckets[key]
            if r["source_api"] not in b["sources"]:
                b["sources"].append(r["source_api"])
            if r.get("cited_by") is not None:
                b["cited_by_by_src"][r["cited_by_src"]] = r["cited_by"]
            if len(r.get("abstract", "")) > len(b.get("abstract", "")):
                b["abstract"] = r["abstract"]
            if not b.get("doi") and r.get("doi"):
                b["doi"] = r["doi"]
            if not b.get("venue") and r.get("venue"):
                b["venue"] = r["venue"]
    merged = list(buckets.values())
    if sort_by == "relevance":
        return merged  # 保留首次出现序（各源相关度序），不按被引重排

    def _sortkey(x: dict) -> int:
        vals = [v for v in x.get("cited_by_by_src", {}).values() if isinstance(v, int)]
        return max(vals) if vals else -1
    merged.sort(key=_sortkey, reverse=True)
    return merged


# ----------------------------- 时效综合重排 -----------------------------
def recency_rerank(records: list[dict], current_year: int,
                   half_life: int = 4, classic_percentile: float = 0.9,
                   classic_min_cites: int = 500) -> list[dict]:
    """按"相关度 × 时效"综合重排，近期文上浮，但**经典高被引文豁免**不被时效压下去。

    解决科研真实需求：要出成果须盯近几年的相关工作（老文多半已被做过），
    但极经典的奠基文（高被引）不能漏。故综合分 = 相关度 × 时效衰减，再对
    被引进入本批 top (1-classic_percentile) 的"经典"豁免时效惩罚（保住奠基文）。

    - 相关度基：优先 OpenAlex 服务端 oa_relevance（数值大、区分度高），
      无则回退本地 relevance_score（标题/摘要覆盖率）。批内各自归一到 0~1。
    - 时效因子：age=current_year-year，0.5 ** (age/half_life)（半衰期 half_life 年，
      默认 4 年→4 年前的文时效权重减半）；年份缺失给中性 0.5。
    - 经典豁免：被引**同时满足** ≥本批 classic_percentile 分位（默认 top10%）**且**
      ≥classic_min_cites 绝对下限（默认 500，防小样本里百来引的平庸文被误判经典），
      时效因子取 max(原值, 0.85)，使其凭相关度+被引仍能留在前列（不硬砍老经典）。
    - 每条写 `rerank_score` + `rerank_parts`（relevance/recency/is_classic）留痕，可复核。
    current_year 由调用方传入（脚本不依赖 Date.now，保持可复现）。
    """
    if not records:
        return records
    # 相关度基：批内归一
    def _relbase(r):
        v = r.get("oa_relevance")
        if isinstance(v, (int, float)):
            return float(v)
        return float(r.get("relevance_score") or 0.0)
    rels = [_relbase(r) for r in records]
    rmax = max(rels) or 1.0
    # 经典阈值：本批被引分位数 与 绝对下限 取较大者（双闸，防小样本误判）
    cites = sorted([r.get("cited_by") or 0 for r in records])
    idx = min(len(cites) - 1, int(len(cites) * classic_percentile))
    classic_cut = max(cites[idx] if cites else 0, classic_min_cites)
    for r, rel in zip(records, rels):
        rel_n = rel / rmax
        yr = r.get("year")
        if isinstance(yr, int) and yr > 0:
            age = max(0, current_year - yr)
            recency = 0.5 ** (age / max(1, half_life))
        else:
            recency = 0.5
        is_classic = (r.get("cited_by") or 0) >= classic_cut and classic_cut > 0
        if is_classic:
            recency = max(recency, 0.85)  # 经典豁免：不被时效压沉
        r["rerank_score"] = round(rel_n * recency, 4)
        r["rerank_parts"] = {"relevance": round(rel_n, 3),
                             "recency": round(recency, 3), "is_classic": is_classic}
    records.sort(key=lambda x: x.get("rerank_score", 0.0), reverse=True)
    return records


# ----------------------------- 相关度过滤 -----------------------------
def _term_hit(text: str, term: str) -> bool:
    """词命中：归一化大小写后子串匹配（中英通用，不做词干）。"""
    return term.lower().strip() in (text or "").lower()


def relevance_score(rec: dict, query: str) -> float:
    """query 词在 标题(权重0.7)+摘要(0.3) 中的覆盖率，0~1。启发式非真值。

    改进点：旧版纯标题 Jaccard 会被长标题稀释（|q∪t| 变大→分母虚高，区分度差，
    实测宽 query 普遍 0.0~0.12）。改用"query 词覆盖率"（命中 query 词数 / query 词总数），
    标题为主、摘要补充——更能反映"query 的关键词到底被命中多少"，宽 query 下区分度更高。
    """
    q = set(re.findall(r"[a-z0-9]+|[一-鿿]", (query or "").lower()))
    if not q:
        return 0.0
    t = set(re.findall(r"[a-z0-9]+|[一-鿿]", (rec.get("title") or "").lower()))
    a = set(re.findall(r"[a-z0-9]+|[一-鿿]", (rec.get("abstract") or "").lower()))
    title_cov = len(q & t) / len(q)            # query 词被标题覆盖的比例
    abs_cov = len(q & a) / len(q) if a else 0.0  # 被摘要覆盖的比例
    return round(0.7 * title_cov + 0.3 * abs_cov, 3)


def filter_relevance(records: list[dict], query: str = "",
                     require_terms: list | None = None,
                     exclude_terms: list | None = None,
                     min_score: float = 0.0) -> tuple[list[dict], list[dict]]:
    """对去重后的文献做相关度过滤，返回 (kept, dropped)。

    解决"宽 query + 纯被引排序顶出跑题高被引文"的硬伤：
    - require_terms：标题或摘要须**全部**含这些词（AND）
    - exclude_terms：标题或摘要命中**任一**即剔（OR 排除）
    - min_score：标题×query 词重叠 Jaccard 低于此值剔（默认 0=不按分截断）
    每条附 relevance_score；dropped 记 drop_reason 便于人工复核（不静默丢弃）。
    """
    require_terms = [t for t in (require_terms or []) if t.strip()]
    exclude_terms = [t for t in (exclude_terms or []) if t.strip()]
    kept, dropped = [], []
    for r in records:
        hay = (r.get("title") or "") + " " + (r.get("abstract") or "")
        r["relevance_score"] = relevance_score(r, query)
        reason = None
        if require_terms and not all(_term_hit(hay, t) for t in require_terms):
            miss = [t for t in require_terms if not _term_hit(hay, t)]
            reason = f"缺必含词 {miss}"
        elif exclude_terms and any(_term_hit(hay, t) for t in exclude_terms):
            hit = [t for t in exclude_terms if _term_hit(hay, t)]
            reason = f"命中排除词 {hit}"
        elif min_score > 0 and r["relevance_score"] < min_score:
            reason = f"标题相关度 {r['relevance_score']}<{min_score}"
        if reason:
            r["drop_reason"] = reason
            dropped.append(r)
        else:
            kept.append(r)
    return kept, dropped


# ----------------------------- 输出 -----------------------------
def to_markdown(records: list[dict], query: str, sort_by: str = "cited") -> str:
    order_desc = "按相关度排序" if sort_by == "relevance" else "按被引降序"
    lines = [f"# 文献表：{query}", "",
             f"共 {len(records)} 条（跨源去重后，{order_desc}）。被引数标来源库，"
             "OpenAlex/Crossref 口径不同不可直接比。", "",
             "| # | 标题 | 年 | venue | 被引(来源) | 来源API | DOI |",
             "|---|------|----|-------|-----------|---------|-----|"]
    for i, r in enumerate(records, 1):
        cb = "; ".join(f"{v}({k})" for k, v in r.get("cited_by_by_src", {}).items()) or "NA"
        title = (r.get("title") or "").replace("|", "/")[:80]
        lines.append(f"| {i} | {title} | {r.get('year') or ''} | "
                     f"{(r.get('venue') or '')[:30]} | {cb} | "
                     f"{'+'.join(r.get('sources', []))} | {r.get('doi') or ''} |")
    return "\n".join(lines)


def run(query: str, per_page: int = 10, offline_sample: bool = False,
        from_date: str = "", known_dois: set | None = None,
        require_terms: list | None = None, exclude_terms: list | None = None,
        min_score: float = 0.0, max_results: int = 0, use_doaj: bool = True,
        sort_by: str = "relevance", recency_boost: bool = False,
        current_year: int = 0, half_life: int = 4,
        classic_min_cites: int = 500) -> dict:
    offline = False
    recs: list[dict] = []
    if not offline_sample:
        oa_code, oa = search_openalex(query, per_page, from_date, max_results, sort_by)
        cr_code, cr = search_crossref(query, per_page, from_date, max_results, sort_by)
        recs = oa + cr
        codes = [oa_code, cr_code]
        # DOAJ（免 key、按相关度排序，补纯被引排序盲区）；增量追踪(from_date)时跳过——
        # DOAJ API 无发表日期过滤，掺进来会污染"只取新发表"的增量语义。
        dj_code = None
        if use_doaj and not from_date:
            dj_code, dj = search_doaj(query, per_page)
            recs += dj
            codes.append(dj_code)
        print(f"[HTTP] OpenAlex={oa_code} Crossref={cr_code}"
              + (f" DOAJ={dj_code}" if dj_code is not None else ""), file=sys.stderr)
        if all(c == 0 for c in codes):
            offline = True
    if offline_sample or offline:
        offline = True
        recs = _SYNTHETIC
        print("[OFFLINE] 网络不可达，使用内置合成样本验证管线。", file=sys.stderr)
    merged = dedup_merge(recs, sort_by=sort_by)
    out = {"query": query, "offline": offline, "from_date": from_date,
           "sort_by": sort_by, "raw_count": len(recs), "merged_count": len(merged)}
    # 相关度过滤：剔跑题（解决宽 query 顶出高被引跑题文）。dropped 留痕不静默丢。
    if require_terms or exclude_terms or min_score > 0:
        kept, dropped = filter_relevance(merged, query, require_terms, exclude_terms, min_score)
        out["filtered"] = True
        out["dropped_count"] = len(dropped)
        out["dropped_records"] = dropped
        out["filter_note"] = ("已按 require/exclude/min-score 剔跑题；dropped 留痕供人工复核。"
                              "relevance_score 为标题×query 词重叠启发式、非真值。")
        merged = kept
        out["merged_count"] = len(merged)
    else:
        # 即便不过滤也附 relevance_score，便于人工看相关度
        for r in merged:
            r["relevance_score"] = relevance_score(r, query)
        # 宽 query 无过滤软告警：纯 cited_by 排序会把领域外高被引文顶上来
        # （examples/goat_littable.md 实证：搜"dairy goat behavior"顶出 theory of
        # planned behavior / G*Power 等跑题文——它们靠蹭中单个宽泛词(behavior)拿低分，
        # 故不能看分数均值，要看"前几条里有几条命中 query 多数词"）。不强改行为，只留痕。
        head = merged[:8]
        nq = len(set(re.findall(r"[a-z0-9]+|[一-鿿]", (query or "").lower())))
        if len(merged) >= 2 and nq >= 2:
            well_matched = sum(1 for r in head if r.get("relevance_score", 0.0) >= 0.6)
            hit_ratio = well_matched / len(head)
            if hit_ratio < 0.34:  # 前排不足 1/3 条命中 query 多数词 → 大概率跑题
                out["relevance_warning"] = (
                    f"未加相关度过滤：前 {len(head)} 条仅 {well_matched} 条命中 query 多数词"
                    f"（{round(hit_ratio*100)}%），纯被引排序可能顶出领域外高被引跑题文。"
                    "建议加 --require-terms/--exclude-terms/--min-score 收窄，详见 SKILL「检索策略」。")
    # 时效综合重排（默认关，开启后近期文上浮、经典高被引豁免不被压沉）。
    # 在相关度过滤之后对留下的条目重排：先剔跑题，再让"近且相关"的上浮。
    if recency_boost and current_year and merged:
        merged = recency_rerank(merged, current_year, half_life=half_life,
                                classic_min_cites=classic_min_cites)
        out["recency_boost"] = True
        out["recency_note"] = (f"已按相关度×时效综合重排（half_life={half_life}年，current_year={current_year}）；"
                               "经典高被引文豁免时效惩罚，每条 rerank_parts 留痕可复核。")
    out["records"] = merged
    # 定期追踪：给了已读库 DOI 集合，则切出"新增（去重后未见过）"条目做增量 diff。
    if known_dois is not None:
        known = {_norm_doi(d) for d in known_dois if d}
        new_recs = [r for r in merged if _norm_doi(r.get("doi")) and _norm_doi(r["doi"]) not in known]
        out["known_count"] = len(known)
        out["new_count"] = len(new_recs)
        out["new_records"] = new_recs
    return out


_SYNTHETIC = [
    {"source_api": "OpenAlex", "title": "Automated behaviour monitoring of dairy goats",
     "authors": ["A Smith", "B Lee"], "year": 2021,
     "venue": "Computers and Electronics in Agriculture",
     "doi": "10.1016/j.compag.2021.100001", "cited_by": 88, "cited_by_src": "OpenAlex",
     "type": "article", "abstract": "We present a system for goat behaviour.", "url": "openalex:W1"},
    {"source_api": "Crossref", "title": "Automated Behaviour Monitoring of Dairy Goats",
     "authors": ["Alice Smith"], "year": 2021,
     "venue": "Computers and Electronics in Agriculture",
     "doi": "10.1016/j.compag.2021.100001", "cited_by": 61, "cited_by_src": "Crossref",
     "type": "journal-article", "abstract": "",
     "url": "https://doi.org/10.1016/j.compag.2021.100001"},
    {"source_api": "OpenAlex", "title": "Accelerometer-based activity recognition in goats",
     "authors": ["C Wang"], "year": 2019, "venue": "Animals", "doi": "10.3390/ani9120999",
     "cited_by": 45, "cited_by_src": "OpenAlex", "type": "article",
     "abstract": "Activity recognition using sensors.", "url": "openalex:W2"},
]



def _selftest() -> int:
    # 限速重试：mock urlopen 连抛两次 429 后成功，验证 _get_json 指数退避重试生效
    global _sleep
    import urllib.error as _ue
    import io as _io
    slept = []
    orig_sleep, orig_urlopen = _sleep, urllib.request.urlopen
    _sleep = lambda s: slept.append(s)  # 不真睡，记录退避秒数
    calls = {"n": 0}

    def fake_urlopen(req, timeout=None):
        calls["n"] += 1
        if calls["n"] <= 2:  # 前两次 429
            raise _ue.HTTPError(req.full_url, 429, "Too Many Requests", {}, None)
        class _R:  # 第三次成功
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def getcode(self): return 200
            def read(self): return b'{"results": []}'
        return _R()
    try:
        urllib.request.urlopen = fake_urlopen
        code, data = _get_json("https://api.openalex.org/works?x=1")
    finally:
        urllib.request.urlopen = orig_urlopen
        _sleep = orig_sleep
    assert code == 200 and data == {"results": []}, (code, data)
    assert calls["n"] == 3 and len(slept) == 2, (calls, slept)  # 重试 2 次后成功
    assert slept == [0.5, 1.0], slept                            # 指数退避 0.5→1.0

    result = run("dairy goat behavior", per_page=3, offline_sample=True)
    assert result["offline"] is True, result
    assert result["raw_count"] >= 2 and result["merged_count"] >= 2, result
    dois = {r.get("doi") for r in result["records"]}
    assert "10.1016/j.compag.2021.100001" in dois, dois
    md = to_markdown(result["records"], "dairy goat behavior")
    assert "10.1016/j.compag.2021.100001" in md and "dairy goats" in md.lower(), md
    # 排序模式：cited 按被引降序；relevance 保留输入(各源相关度)序、不按被引重排
    recs_in = [
        {"source_api": "OpenAlex", "title": "Low cite but relevant", "doi": "10.1/rel", "cited_by": 3, "cited_by_src": "OpenAlex"},
        {"source_api": "OpenAlex", "title": "High cite off topic", "doi": "10.1/hi", "cited_by": 999, "cited_by_src": "OpenAlex"},
    ]
    m_cited = dedup_merge([dict(x) for x in recs_in], sort_by="cited")
    assert m_cited[0]["doi"] == "10.1/hi", m_cited      # 被引高的顶上来
    m_rel = dedup_merge([dict(x) for x in recs_in], sort_by="relevance")
    assert m_rel[0]["doi"] == "10.1/rel", m_rel         # 保留输入序：相关的(虽低被引)在前
    # 时效综合重排：近期相关上浮、经典高被引豁免不沉底
    rr_in = [
        {"title": "recent relevant", "doi": "10.1/new", "year": 2025, "cited_by": 5, "oa_relevance": 90.0},
        {"title": "old classic foundational", "doi": "10.1/classic", "year": 2008, "cited_by": 5000, "oa_relevance": 88.0},
        {"title": "old mediocre", "doi": "10.1/old", "year": 2008, "cited_by": 8, "oa_relevance": 80.0},
    ]
    rr = recency_rerank([dict(x) for x in rr_in], current_year=2026, half_life=4)
    order = [r["doi"] for r in rr]
    assert order.index("10.1/new") < order.index("10.1/old"), order      # 近期相关 > 老平庸
    assert order.index("10.1/classic") < order.index("10.1/old"), order  # 经典豁免 > 老平庸(虽同龄)
    assert rr[[r["doi"] for r in rr].index("10.1/classic")]["rerank_parts"]["is_classic"] is True, rr
    # 定期追踪增量 diff：已读库含合成样本里的一条 DOI，则新增应排除它。
    incr = run("dairy goat behavior", per_page=3, offline_sample=True,
               from_date="2020-01-01",
               known_dois={"10.1016/j.compag.2021.100001"})
    assert incr["from_date"] == "2020-01-01", incr
    assert incr["known_count"] == 1, incr
    new_dois = {r.get("doi") for r in incr["new_records"]}
    assert "10.1016/j.compag.2021.100001" not in new_dois, incr  # 已读，被剔
    assert "10.3390/ani9120999" in new_dois, incr                # 未读，留作新增
    assert incr["new_count"] == len(incr["new_records"]) >= 1, incr

    # 相关度过滤：require/exclude/min-score 三路 + dropped 留痕
    r_req = run("dairy goat behavior", offline_sample=True, require_terms=["goat"])
    assert all(_term_hit((x.get("title") or "")+(x.get("abstract") or ""), "goat")
               for x in r_req["records"]), r_req
    r_exc = run("dairy goat behavior", offline_sample=True, exclude_terms=["accelerometer"])
    assert r_exc.get("filtered") and r_exc["dropped_count"] >= 1, r_exc
    assert all("accelerometer" not in ((x.get("title") or "")+(x.get("abstract") or "")).lower()
               for x in r_exc["records"]), r_exc
    # dropped 留痕带 reason，不静默丢
    assert all(d.get("drop_reason") for d in r_exc["dropped_records"]), r_exc
    # 不过滤时也附 relevance_score
    r_plain = run("dairy goat behavior", offline_sample=True)
    assert all("relevance_score" in x for x in r_plain["records"]), r_plain
    # DOAJ 记录解析：bibjson 结构 → 统一记录（is_oa=True、DOI 从 identifier 抽、不臆造被引）
    dj = _doaj_rec({"bibjson": {
        "title": "Goat behaviour OA paper",
        "year": "2023",
        "author": [{"name": "A One"}, {"name": "B Two"}],
        "journal": {"title": "Open Vet J"},
        "identifier": [{"type": "doi", "id": "10.1/oa.1"}, {"type": "pissn", "id": "1234-5678"}],
        "abstract": "open access goat study",
    }})
    assert dj["doi"] == "10.1/oa.1" and dj["is_oa"] is True, dj
    assert dj["year"] == 2023 and dj["cited_by"] is None and dj["source_api"] == "DOAJ", dj
    assert dj["venue"] == "Open Vet J" and len(dj["authors"]) == 2, dj
    # 宽 query 无过滤软告警：用与样本标题几乎无重叠的跑题 query 触发低相关度告警
    r_warn = run("quantum chromodynamics lattice", offline_sample=True)
    assert r_warn.get("relevance_warning"), r_warn  # 前 5 条相关度均值低 → 应告警
    # 加了 require-terms（走过滤分支）则不应有该软告警
    r_nowarn = run("dairy goat behavior", offline_sample=True, require_terms=["goat"])
    assert not r_nowarn.get("relevance_warning"), r_nowarn
    print("[selftest] PASS search_normalize (含 --from-date 增量 diff + 相关度过滤)")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="多源文献检索与规范化")
    ap.add_argument("query", nargs="?", default="dairy goat behavior")
    ap.add_argument("--per-page", type=int, default=10)
    ap.add_argument("--offline", action="store_true", help="强制用合成样本")
    ap.add_argument("--from-date", default="",
                    help="定期追踪：只取该日期(YYYY-MM-DD)之后发表的文献，做增量重跑")
    ap.add_argument("--known-dois", default="",
                    help="定期追踪：已读库 DOI 清单文件(每行一个)，输出标出新增条目")
    ap.add_argument("--selftest", action="store_true", help="run offline synthetic self-test")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--md-out", default="")
    ap.add_argument("--mailto", default="",
                    help="礼貌池邮箱（也可设环境变量 OPENALEX_MAILTO / CROSSREF_MAILTO）；不传则匿名查")
    ap.add_argument("--api-key", default="",
                    help="OpenAlex API key（也可设环境变量 OPENALEX_API_KEY）；口径见本技能 references")
    ap.add_argument("--require-terms", default="",
                    help="相关度过滤：标题/摘要须全部含这些词（逗号分隔，AND），剔跑题")
    ap.add_argument("--exclude-terms", default="",
                    help="相关度过滤：标题/摘要命中任一即剔（逗号分隔，OR 排除）")
    ap.add_argument("--min-score", type=float, default=0.0,
                    help="相关度过滤：标题×query 词重叠 Jaccard 低于此值剔（0=不按分截断）")
    ap.add_argument("--max-results", type=int, default=0,
                    help="穷尽检索：用 cursor 深翻页取到这么多条（>per-page 才生效，0=只取一页）")
    ap.add_argument("--no-doaj", action="store_true",
                    help="关闭 DOAJ 源（默认开；DOAJ 免 key 按相关度排序，补纯被引排序盲区）")
    ap.add_argument("--sort", default="relevance", choices=["relevance", "cited"],
                    help="OpenAlex/Crossref 排序：relevance 相关度(默认,治宽query顶跑题文)/cited 被引降序(找高被引经典)")
    ap.add_argument("--recency-boost", action="store_true",
                    help="时效综合重排：近期相关文上浮、经典高被引豁免不被压沉（需配 --current-year）")
    ap.add_argument("--current-year", type=int, default=0,
                    help="当前年份（时效重排基准；显式传入不依赖系统时钟，保可复现）")
    ap.add_argument("--half-life", type=int, default=4,
                    help="时效半衰期（年，默认4）：N 年前的文时效权重减半，越小越偏向最新")
    ap.add_argument("--classic-min-cites", type=int, default=500,
                    help="经典豁免的绝对被引下限（默认500，领域差异大：CS调高、小众畜牧调低）")
    args = ap.parse_args()

    global _MAILTO, _API_KEY
    if args.mailto:
        _MAILTO = args.mailto.strip()
    if args.api_key:
        _API_KEY = args.api_key.strip()

    if args.selftest:
        sys.exit(_selftest())

    req = [t.strip() for t in args.require_terms.split(",") if t.strip()]
    exc = [t.strip() for t in args.exclude_terms.split(",") if t.strip()]

    known: set | None = None
    if args.known_dois:
        with open(args.known_dois, encoding="utf-8") as f:
            known = {ln.strip() for ln in f if ln.strip() and not ln.startswith("#")}

    result = run(args.query, args.per_page, offline_sample=args.offline,
                 from_date=args.from_date, known_dois=known,
                 require_terms=req, exclude_terms=exc, min_score=args.min_score,
                 max_results=args.max_results, use_doaj=not args.no_doaj,
                 sort_by=args.sort, recency_boost=args.recency_boost,
                 current_year=args.current_year, half_life=args.half_life,
                 classic_min_cites=args.classic_min_cites)
    md = to_markdown(result["records"], args.query, sort_by=args.sort)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    if args.md_out:
        with open(args.md_out, "w", encoding="utf-8") as f:
            f.write(md)

    print(md)
    summary = (f"\n[SUMMARY] query={args.query!r} offline={result['offline']} "
               f"sort={result.get('sort_by','relevance')} "
               f"raw={result['raw_count']} merged={result['merged_count']}")
    if args.from_date:
        summary += f" from_date={args.from_date}"
    if "new_count" in result:
        summary += f" known={result['known_count']} new={result['new_count']}"
    if result.get("filtered"):
        summary += f" dropped={result['dropped_count']}(相关度过滤,留痕见 JSON dropped_records)"
    print(summary)
    if result.get("relevance_warning"):
        print("[WARN] " + result["relevance_warning"], file=sys.stderr)


if __name__ == "__main__":
    main()



