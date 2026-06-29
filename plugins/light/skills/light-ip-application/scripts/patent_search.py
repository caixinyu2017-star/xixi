#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patent_search.py — 在先技术(prior-art)检索辅助。

诚实声明(d:/skill/Light/CONVENTIONS.md):
  * OpenAlex 是本脚本唯一"可程序化的真实公开数据源",用于"非专利文献(NPL)"型在先技术。
    2026 起 OpenAlex 接入需免费 API key(接入口径以 m01 light-literature-search
    references「OpenAlex 接入真相源」节为准)。key 经 --api-key 或环境变量 OPENALEX_API_KEY
    传入,由 _http_get_json 对 OpenAlex 端点统一注入(不污染专利库请求);未配置时退回匿名
    请求(过渡期或仍可用但不保证)。mailto 经 --mailto 进 polite pool。
  * 专利数据库(EPO OPS / The Lens / USPTO ODP)均需注册凭证,本脚本提供
    "构造请求"的适配器(build_*_request),便于用户带 key 时直接发起;不内置任何
    伪造 key,也不臆造返回。
  * 端点状态(2026-06 curl 实测,见 references.md):
      - OpenAlex            GET  api.openalex.org/works                 -> 200 (现行需免费 key)
      - EPO OPS  auth       POST ops.epo.org/3.2/auth/accesstoken       -> 401 (需 key)
      - The Lens patent     POST api.lens.org/patent/search             -> 401 (需 token)
      - USPTO 程序化 API    POST api.uspto.gov/api/v1/patent/.../search -> 401 (需 X-Api-Key)
      - 旧 api.patentsview.org -> 301 弃用; search.patentsview.org 本机无法解析(未实测)
  * 检索结果仅供查新参考,FTO/新颖性/无效结论须由专利代理师/律师判定。

无网络/无 key 时:运行 `python patent_search.py --selftest` 用内置离线样本自测
请求构造与排序逻辑,不发任何网络请求。
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

OPENALEX_BASE = "https://api.openalex.org"

# 礼貌池邮箱与 OpenAlex API key 的运行时口径（不硬编码）：
# mailto 经各 build_* 的 mailto= 参数传入（main 从 --mailto / 环境变量取）；
# OpenAlex 2026 起需免费 key——经 --api-key / 环境变量 OPENALEX_API_KEY 传入，
# 由 _http_get_json 对 OpenAlex 域名统一注入（不污染 Lens/EPO/USPTO 等其它端点请求）。
# key/限流/计费的唯一口径见 light-literature-search references「OpenAlex 接入真相源」节。
_API_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()


def _http_get_json(url: str, timeout: float = 30.0) -> dict:
    # 仅对 OpenAlex 端点注入 api_key（若已带或未配置则原样）。
    if _API_KEY and url.startswith(OPENALEX_BASE) and "api_key=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}api_key={urllib.parse.quote(_API_KEY, safe='')}"
    req = urllib.request.Request(url, headers={"User-Agent": "light-ip-application/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_openalex_url(query: str, *, from_year: int | None = None,
                       to_year: int | None = None, per_page: int = 25,
                       mailto: str | None = None) -> str:
    """构造 OpenAlex /works 检索 URL(NPL 在先技术)。

    per_page 上限 200(API 实测 201 -> HTTP 400)。建议带 mailto 进 polite pool。
    """
    per_page = max(1, min(int(per_page), 200))
    params: list[tuple[str, str]] = [
        ("search", query),
        ("per_page", str(per_page)),
        ("select", "id,title,publication_year,doi,cited_by_count,"
                   "referenced_works,authorships"),
    ]
    filters = []
    if from_year is not None:
        filters.append(f"from_publication_date:{int(from_year)}-01-01")
    if to_year is not None:
        filters.append(f"to_publication_date:{int(to_year)}-12-31")
    if filters:
        params.append(("filter", ",".join(filters)))
    if mailto:
        params.append(("mailto", mailto))
    return f"{OPENALEX_BASE}/works?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def _normalize_work(w: dict, origin: str = "seed") -> dict:
    """把 OpenAlex work 对象归一化为 prior-art 候选记录。

    origin 标注来源:seed(关键词命中)/backward(后向引文)/forward(前向引文),
    便于交底书留档引用链路。
    """
    insts = []
    for a in (w.get("authorships") or [])[:5]:
        for ins in (a.get("institutions") or []):
            if ins.get("display_name"):
                insts.append(ins["display_name"])
    return {
        "source": "OpenAlex(NPL)",
        "id": w.get("id"),
        "title": w.get("title"),
        "year": w.get("publication_year"),
        "doi": w.get("doi"),
        "cited_by_count": w.get("cited_by_count", 0),
        "referenced_works": list(w.get("referenced_works") or []),
        "cited_by_api_url": w.get("cited_by_api_url"),
        "institutions": sorted(set(insts))[:5],
        "origin": origin,
    }


def search_openalex_npl(query: str, **kw) -> list[dict]:
    """实发 OpenAlex 检索,归一化为 prior-art 候选记录。OpenAlex 2026 起需免费 key(见 m01 真相源)。"""
    url = build_openalex_url(query, **kw)
    data = _http_get_json(url)
    return [_normalize_work(w, origin="seed") for w in data.get("results", [])]


# ---- 引用图一跳扩展(snowballing,OpenAlex,2026 起需免费 key)----

def _openalex_short_id(work_id: str) -> str:
    """把 https://openalex.org/W123 或 W123 归一为短 id 'W123'。"""
    if not work_id:
        return ""
    return work_id.rstrip("/").rsplit("/", 1)[-1]


def build_openalex_ids_url(ids: list[str], *, per_page: int = 200,
                           mailto: str | None = None) -> str:
    """构造按 openalex_id OR 批量回填的 /works URL(单批 <=200)。"""
    per_page = max(1, min(int(per_page), 200))
    short = [s for s in (_openalex_short_id(i) for i in ids) if s]
    params: list[tuple[str, str]] = [
        ("filter", "openalex_id:" + "|".join(short[:per_page])),
        ("per_page", str(per_page)),
        ("select", "id,title,publication_year,doi,cited_by_count,"
                   "referenced_works,authorships"),
    ]
    if mailto:
        params.append(("mailto", mailto))
    return f"{OPENALEX_BASE}/works?" + urllib.parse.urlencode(
        params, quote_via=urllib.parse.quote)


def build_openalex_cites_url(work_id: str, *, per_page: int = 200,
                             mailto: str | None = None) -> str:
    """构造前向引文 URL:filter=cites:{id}(引用了该 work 的文献)。"""
    per_page = max(1, min(int(per_page), 200))
    params: list[tuple[str, str]] = [
        ("filter", f"cites:{_openalex_short_id(work_id)}"),
        ("per_page", str(per_page)),
        ("select", "id,title,publication_year,doi,cited_by_count,"
                   "referenced_works,authorships"),
    ]
    if mailto:
        params.append(("mailto", mailto))
    return f"{OPENALEX_BASE}/works?" + urllib.parse.urlencode(
        params, quote_via=urllib.parse.quote)


def merge_dedup(records: list[dict]) -> list[dict]:
    """按 id 合并去重;保留首个 origin,但 seed 优先级最高。"""
    order = {"seed": 0, "backward": 1, "forward": 2}
    by_id: dict[str, dict] = {}
    for r in records:
        rid = r.get("id")
        if not rid:
            continue
        if rid not in by_id:
            by_id[rid] = dict(r)
        else:
            cur = by_id[rid]
            if order.get(r.get("origin"), 9) < order.get(cur.get("origin"), 9):
                cur["origin"] = r.get("origin")
    return list(by_id.values())


def expand_openalex_citations(seeds: list[dict], *, direction: str = "both",
                              per_seed: int = 200,
                              mailto: str | None = None) -> list[dict]:
    """对种子候选做一跳引用图扩展(OpenAlex,2026 起需免费 key)。
    backward: 种子的 referenced_works(它引用的在先文献)。
    forward : filter=cites:{id}(后续引用它的文献)。
    单跳为限,避免指数爆炸;每种子配额由 per_seed 钳制。
    """
    out: list[dict] = []
    want_back = direction in ("both", "backward")
    want_fwd = direction in ("both", "forward")
    for s in seeds:
        sid = _openalex_short_id(s.get("id", ""))
        if not sid:
            continue
        if want_back:
            refs = (s.get("referenced_works") or [])[:per_seed]
            for batch in (refs[i:i + 200] for i in range(0, len(refs), 200)):
                if not batch:
                    continue
                data = _http_get_json(
                    build_openalex_ids_url(batch, mailto=mailto))
                out += [_normalize_work(w, origin="backward")
                        for w in data.get("results", [])]
        if want_fwd:
            data = _http_get_json(
                build_openalex_cites_url(sid, per_page=per_seed, mailto=mailto))
            out += [_normalize_work(w, origin="forward")
                    for w in data.get("results", [])]
    return out


def build_lens_citation_request(lens_id: str, edge: str = "references") -> dict:
    """The Lens 专利↔论文引用关系(PatCite)。edge: references|cited_by。
    key-gated 可选项,优先级低;发起需 Bearer token。"""
    field = "references" if edge == "references" else "cited_by"
    return {
        "method": "POST",
        "url": "https://api.lens.org/patent/search",
        "headers": {"Authorization": "Bearer <YOUR_LENS_TOKEN>",
                    "Content-Type": "application/json"},
        "body": {"query": {"term": {"lens_id": lens_id}},
                 "include": ["lens_id", field]},
        "note": f"取该专利的 {field} 引用边(PatCite);需付费 scholarly 权限",
    }


def build_lens_request(query: str, size: int = 25) -> dict:
    """The Lens 专利检索请求体(ES 风格 DSL)。发起需 Authorization: Bearer <token>。"""
    return {
        "method": "POST",
        "url": "https://api.lens.org/patent/search",
        "headers": {"Authorization": "Bearer <YOUR_LENS_TOKEN>",
                    "Content-Type": "application/json"},
        "body": {"query": {"match": {"title": query}}, "size": int(size),
                 "include": ["lens_id", "biblio", "abstract"]},
    }


def build_epo_ops_search(cql: str, range_hdr: str = "1-25") -> dict:
    """EPO OPS published-data 检索。先 OAuth2 换 Bearer token(/auth/accesstoken)。"""
    return {
        "method": "GET",
        "url": "https://ops.epo.org/3.2/rest-services/published-data/search",
        "params": {"q": cql},
        "headers": {"Authorization": "Bearer <OPS_ACCESS_TOKEN>", "Range": range_hdr},
        "note": "CQL 字段: ti= ab= ta= txt= pa= in= cpc= ipc= pn= pd=; 每页<=100,翻页用 Range 头",
    }


def build_uspto_odp_request(query_json: dict) -> dict:
    """USPTO 程序化 API(ODP 迁移后)。需 X-Api-Key(api.uspto.gov 实测 401=需鉴权)。"""
    return {
        "method": "POST",
        "url": "https://api.uspto.gov/api/v1/patent/applications/search",
        "headers": {"X-Api-Key": "<YOUR_USPTO_ODP_KEY>", "Content-Type": "application/json"},
        "body": query_json,
        "note": "旧 api.patentsview.org 已 301 弃用; search.patentsview.org 本机无法解析(未实测); 统一走 api.uspto.gov",
    }


def rank_candidates(records: list[dict]) -> list[dict]:
    """按被引次数降序排候选(被引高者更可能是关键在先技术)。"""
    return sorted(records, key=lambda r: r.get("cited_by_count", 0) or 0, reverse=True)


_OFFLINE_SAMPLE = [
    {"source": "OpenAlex(NPL)", "id": "W1", "title": "A graphene battery method",
     "year": 2017, "doi": "10.x/a", "cited_by_count": 300, "institutions": ["MIT"]},
    {"source": "OpenAlex(NPL)", "id": "W2", "title": "Neural net patent landscape",
     "year": 2019, "doi": "10.x/b", "cited_by_count": 50, "institutions": ["THU"]},
]


def build_freesearch_urls(keywords: str, cpc: str = "", before: str = "",
                          country: str = "CN") -> list:
    """生成"人工点开即用"的免凭证检索链接（无 API key 的主力查新路径）。
    返回 [{engine, url, note}]。这些是公开网页高级检索入口，拼好查询参数，用户点开就能查
    专利在先技术——弥补 patent_search 主体需 OpenAlex/凭证、无 API 用户拿不到专利库结果的空白。"""
    kw = keywords.strip()
    q = urllib.parse.quote(kw)
    urls = []
    # Google Patents 高级检索（免登录，支持 before:priority、country、cpc）
    gp = f"https://patents.google.com/?q={q}"
    if country:
        gp += f"&country={country}"
    if before:
        gp += f"&before=priority:{before}"   # 仅检索优先日之前的在先技术
    if cpc:
        gp += f"&cpc={urllib.parse.quote(cpc)}"
    urls.append({"engine": "Google Patents", "url": gp,
                 "note": "免登录网页高级检索；before:priority 卡优先日之前为在先技术；可加 CPC 分类号收敛"})
    # CNIPA 专利检索及分析系统（需注册免费账号，公开可用）
    urls.append({"engine": "CNIPA pss-system", "url": "https://pss-system.cponline.cnipa.gov.cn/",
                 "note": f"国家知识产权局官方检索系统(免费注册)；进高级检索填关键词『{kw}』+IPC/申请日范围；中国专利权威源"})
    # Lens.org（免费学术专利检索，无需 key 可网页查）
    urls.append({"engine": "Lens.org", "url": f"https://www.lens.org/lens/search/patent/list?q={q}",
                 "note": "免费网页专利检索(注册后功能更全)；跨库(USPTO/EPO/WIPO/CNIPA)，适合全球查新"})
    # WIPO PATENTSCOPE（PCT 国际申请）
    urls.append({"engine": "WIPO PATENTSCOPE",
                 "url": f"https://patentscope.wipo.int/search/en/result.jsf?query={q}",
                 "note": "WIPO 官方，PCT 国际申请检索；查是否有国际同族在先技术"})
    return urls


def _selftest() -> int:
    # 1) URL 构造与 per_page 上限钳制
    u = build_openalex_url("graphene battery", from_year=2015, to_year=2020,
                           per_page=999, mailto="a@b.com")
    assert "per_page=200" in u, u
    assert "from_publication_date%3A2015" in u or "from_publication_date:2015" in u, u
    assert "mailto=a%40b.com" in u, u
    # 2) 适配器请求体结构
    assert build_lens_request("x")["url"].endswith("/patent/search")
    assert build_epo_ops_search("ti=x")["params"]["q"] == "ti=x"
    assert build_uspto_odp_request({"q": "x"})["headers"]["X-Api-Key"].startswith("<")
    # 3) 排序
    ranked = rank_candidates(list(_OFFLINE_SAMPLE))
    assert ranked[0]["cited_by_count"] == 300, ranked
    # 4) 引用图扩展 URL 构造(unquote 后比对,避开 %3A/%7C 编码差异)
    bu = urllib.parse.unquote(
        build_openalex_ids_url(["https://openalex.org/W10", "W11"], mailto="a@b.com"))
    assert "openalex_id:W10|W11" in bu, bu
    cu = urllib.parse.unquote(build_openalex_cites_url("https://openalex.org/W1"))
    assert "cites:W1" in cu, cu
    # 5) merge_dedup:同 id 合并,seed origin 优先
    merged = merge_dedup([
        {"id": "W1", "origin": "backward"}, {"id": "W1", "origin": "seed"},
        {"id": "W2", "origin": "forward"}, {"id": "W2", "origin": "forward"},
    ])
    assert len(merged) == 2, merged
    w1 = next(r for r in merged if r["id"] == "W1")
    assert w1["origin"] == "seed", w1
    # 6) Lens 引用边请求体
    lc = build_lens_citation_request("123-456-789", edge="cited_by")
    assert lc["body"]["include"] == ["lens_id", "cited_by"], lc
    # 7) IP-2 免凭证检索链接清单：4 引擎、Google Patents 带 before:priority/country/cpc
    fu = build_freesearch_urls("graphene battery", cpc="H01M", before="2020-01-01", country="CN")
    engines = {e["engine"] for e in fu}
    assert {"Google Patents", "CNIPA pss-system", "Lens.org", "WIPO PATENTSCOPE"} <= engines, engines
    gp = next(e for e in fu if e["engine"] == "Google Patents")["url"]
    assert "before=priority:2020-01-01" in gp and "country=CN" in gp and "cpc=H01M" in gp, gp
    print("[selftest] OK  url=", u)
    print("[selftest] ranked top:", ranked[0]["title"])
    print("[selftest] snowball+merge_dedup+lens-cite: PASS")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="在先技术检索辅助(OpenAlex NPL + 专利库请求构造)")
    ap.add_argument("query", nargs="?", help="检索关键词")
    ap.add_argument("--from-year", type=int, default=None)
    ap.add_argument("--to-year", type=int, default=None)
    ap.add_argument("--per-page", type=int, default=10)
    ap.add_argument("--mailto", default=None, help="进入 OpenAlex polite pool")
    ap.add_argument("--api-key", default="",
                    help="OpenAlex API key（也可设环境变量 OPENALEX_API_KEY；2026 起需 key，口径见 m01 references）")
    ap.add_argument("--snowball", nargs="?", type=int, const=3, default=0,
                    metavar="N",
                    help="对前 N 条命中(默认3)做一跳引用图扩展(后向+前向),省配额默认关")
    ap.add_argument("--selftest", action="store_true", help="离线自测(不联网)")
    ap.add_argument("--print-adapters", action="store_true", help="打印专利库请求构造示例")
    ap.add_argument("--free-urls", action="store_true",
                    help="只生成免凭证检索链接清单(CNIPA/Google Patents/Lens/WIPO，人工点开即用)")
    ap.add_argument("--cpc", default="", help="CPC 分类号(配合 --free-urls 收敛)")
    ap.add_argument("--before", default="", help="优先日 YYYY-MM-DD(配合 --free-urls 只查之前在先技术)")
    args = ap.parse_args()

    global _API_KEY
    if args.api_key:
        _API_KEY = args.api_key.strip()

    if args.selftest:
        return _selftest()
    if args.free_urls:
        if not args.query:
            ap.error("--free-urls 需要 query(关键词)")
        urls = build_freesearch_urls(args.query, cpc=args.cpc, before=args.before)
        print("# 免凭证专利检索链接(人工点开即用；无 OpenAlex/API key 也能查在先技术)\n")
        for e in urls:
            print(f"## {e['engine']}\n{e['url']}\n  {e['note']}\n")
        print("> 这些是公开网页高级检索入口；命中文献号/日期/相关段落随交底书留档，"
              "FTO/无效结论须代理师/律师定。")
        return 0
    if args.print_adapters:
        print(json.dumps({
            "lens": build_lens_request("neural network"),
            "epo_ops": build_epo_ops_search('ti=neural and ab=network'),
            "uspto_odp": build_uspto_odp_request({"q": "neural network"}),
        }, ensure_ascii=False, indent=2))
        return 0
    if not args.query:
        ap.error("需要 query(或用 --selftest / --print-adapters)")
    seeds = search_openalex_npl(
        args.query, from_year=args.from_year, to_year=args.to_year,
        per_page=args.per_page, mailto=args.mailto)
    pool = list(seeds)
    if args.snowball:
        top_seeds = rank_candidates(list(seeds))[:args.snowball]
        print(f"# 引用图一跳扩展: 对前 {len(top_seeds)} 条种子做后向+前向追踪")
        pool += expand_openalex_citations(top_seeds, mailto=args.mailto)
    recs = rank_candidates(merge_dedup(pool))
    n_seed = sum(1 for r in recs if r.get("origin") == "seed")
    print(f"# NPL 在先技术候选(OpenAlex) query={args.query!r} "
          f"n={len(recs)} (seed={n_seed}, 扩展={len(recs) - n_seed})")
    for i, r in enumerate(recs, 1):
        og = r.get("origin", "seed")
        print(f"{i}. [{r['year']}] {r['title']}  "
              f"(cited={r['cited_by_count']}, {og}) {r['doi'] or ''}")
    print("\n注:仅 NPL 文献;专利库检索请用 --print-adapters 取请求模板,自带 key 发起。"
          "查新/FTO 结论须代理师判定。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
