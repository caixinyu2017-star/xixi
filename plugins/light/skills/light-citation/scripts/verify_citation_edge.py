#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_citation_edge.py — 实证"A 引用了 B"的引用边，三态输出，不靠印象。

输入 (citing_doi, cited_doi)，多源开放索引兜底核验：
  ① OpenCitations 双向交叉：
     /index/v2/references/doi:{A}  看 cited 列是否含 B；
     /index/v2/citations/doi:{B}   看 citing 列是否含 A。
  ② Semantic Scholar /paper/DOI:{A}/references?fields=externalIds 匹配 B 的 DOI。

三态 status（绝不输出裸 edge_exists:false）：
  - confirmed       任一源在开放索引中查到 A→B 这条边。
  - not_in_open_index  所有可用源都 200 但均未含 B —— 注意：
                    开放索引未覆盖 ≠ 未引用；需人工查全文或 WoS/Scopus 确认。
  - unknown         端点非 200 / 限速 / 无网络 —— 无法判定，需重试或换源。

实测端点（references.md，2026-06-06，均 HTTP 200）：
  https://api.opencitations.net/index/v2/references/doi:{A}
  https://api.opencitations.net/index/v2/citations/doi:{B}
  https://api.semanticscholar.org/graph/v1/paper/DOI:{A}/references?fields=externalIds

诚实原则：只报开放索引真实返回；查不到时明确"未覆盖≠未引用"，不替任一方圆场。
礼貌池邮箱经环境变量 CROSSREF_MAILTO / OPENALEX_MAILTO 或 --mailto 传入；不传则匿名（不伪造）。
Semantic Scholar 可选 key 经环境变量 S2_API_KEY 或 --s2-api-key 传入（提高限速）。

用法：
  python scripts/verify_citation_edge.py 10.1186/1756-8722-6-59 10.1056/nejabc.xxx
  python scripts/verify_citation_edge.py --citing <A> --cited <B> --mailto you@inst.edu --out edge.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 礼貌池邮箱：优先环境变量 CROSSREF_MAILTO / OPENALEX_MAILTO，其次 --mailto，不传则匿名（不伪造）。
# 本脚本查 OpenCitations 与 Semantic Scholar，二者均可匿名查；带真实邮箱进 UA 更礼貌。
# Semantic Scholar 可选 API key（x-api-key header）：经 --s2-api-key 或环境变量 S2_API_KEY 传入，
# 提高限速上限；不传则用公共匿名通道。
_MAILTO = (os.environ.get("CROSSREF_MAILTO") or os.environ.get("OPENALEX_MAILTO") or "").strip()
_S2_API_KEY = os.environ.get("S2_API_KEY", "").strip()


def _user_agent() -> str:
    if _MAILTO:
        return "light-citation/1.0 (mailto:%s)" % _MAILTO
    return "light-citation/1.0"


def _get_json(url: str, timeout: int = 30, headers: dict | None = None):
    """返回 (http_code, obj_or_None)。沿用 verify_refs.py 模式。"""
    h = {"User-Agent": _user_agent(), "Accept": "application/json"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None
    except (urllib.error.URLError, TimeoutError):
        return 0, None


def _norm_doi(doi: str) -> str:
    """归一化 DOI：去前缀、去空白、转小写（DOI 大小写不敏感）。"""
    return (doi or "").strip().replace("https://doi.org/", "").replace(
        "http://doi.org/", "").replace("doi:", "").lower()


def _split_dois(field: str):
    """OpenCitations 的 citing/cited 字段可含多个标识符（空格分隔，带 doi: 前缀）。"""
    out = []
    for tok in (field or "").split():
        if tok.lower().startswith("doi:"):
            out.append(_norm_doi(tok))
    return out


def _oc_check(citing: str, cited: str):
    """OpenCitations 双向兜底。返回 (hit: bool, ok_any: bool, http: dict)。
    hit  = 在任一方向查到 A→B 这条边；
    ok_any = 至少一个端点 HTTP 200（用于区分 not_in_open_index vs unknown）。"""
    http = {}
    hit = False
    ok_any = False

    # 方向①：A 的 references 里是否含 B
    ref_url = f"https://api.opencitations.net/index/v2/references/doi:{urllib.parse.quote(citing)}"
    code, refs = _get_json(ref_url)
    http["opencitations_references"] = code
    if code == 200:
        ok_any = True
        if isinstance(refs, list):
            for row in refs:
                if cited in _split_dois(row.get("cited", "")):
                    hit = True
                    break

    # 方向②：B 的 citations 里是否含 A（交叉兜底）
    cit_url = f"https://api.opencitations.net/index/v2/citations/doi:{urllib.parse.quote(cited)}"
    code2, cits = _get_json(cit_url)
    http["opencitations_citations"] = code2
    if code2 == 200:
        ok_any = True
        if isinstance(cits, list):
            for row in cits:
                if citing in _split_dois(row.get("citing", "")):
                    hit = True
                    break
    return hit, ok_any, http


def _s2_check(citing: str, cited: str):
    """Semantic Scholar 兜底：A 的 references 的 externalIds.DOI 是否含 B。
    返回 (hit: bool, ok: bool, http_code: int)。"""
    url = (f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(citing)}"
           f"/references?fields=externalIds&limit=1000")
    s2_headers = {"x-api-key": _S2_API_KEY} if _S2_API_KEY else None
    code, data = _get_json(url, headers=s2_headers)
    if code != 200 or not isinstance(data, dict):
        return False, False, code
    for item in data.get("data", []) or []:
        cp = (item or {}).get("citedPaper") or {}
        ext = cp.get("externalIds") or {}
        if _norm_doi(ext.get("DOI", "")) == cited:
            return True, True, code
    return False, True, code


def verify_edge(citing_doi: str, cited_doi: str):
    """核验单条引用边 A→B，三态输出。"""
    citing = _norm_doi(citing_doi)
    cited = _norm_doi(cited_doi)
    rec = {"citing": citing, "cited": cited, "status": "unknown",
           "sources": [], "http": {}, "note": None}

    # ① OpenCitations 双向
    oc_hit, oc_ok, oc_http = _oc_check(citing, cited)
    rec["http"].update(oc_http)
    if oc_hit:
        rec["sources"].append("opencitations")

    # ② Semantic Scholar 兜底
    s2_hit, s2_ok, s2_code = _s2_check(citing, cited)
    rec["http"]["semanticscholar_references"] = s2_code
    if s2_hit:
        rec["sources"].append("semanticscholar")

    # 三态裁决
    if rec["sources"]:
        rec["status"] = "confirmed"
        rec["note"] = ("开放引用索引已实证 A→B 这条边（来源：%s）。"
                       % "、".join(rec["sources"]))
    elif oc_ok or s2_ok:
        # 至少一个源 200 且都未含 B
        rec["status"] = "not_in_open_index"
        rec["note"] = ("开放索引（OpenCitations/Semantic Scholar）已响应但未收录 A→B。"
                       "注意：开放索引未覆盖 ≠ 未引用——开放 DOI-DOI 索引不完整，"
                       "请人工查全文参考文献，或用 WoS/Scopus 等商业库确认后再下结论。")
    else:
        rec["status"] = "unknown"
        rec["note"] = ("所有开放索引端点均非 200（限速/网络/未收录该 DOI），无法判定。"
                       "请稍后重试或换源；切勿据此断言引用关系存在与否。")
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="实证引用边 A→B（三态：confirmed/not_in_open_index/unknown）")
    ap.add_argument("dois", nargs="*", help="位置参数：<citing_doi> <cited_doi>")
    ap.add_argument("--citing", help="施引文献 DOI（A）")
    ap.add_argument("--cited", help="被引文献 DOI（B）")
    ap.add_argument("--mailto", default="",
                    help="礼貌池邮箱（也可设环境变量 CROSSREF_MAILTO / OPENALEX_MAILTO）；不传则匿名")
    ap.add_argument("--s2-api-key", default="",
                    help="Semantic Scholar API key（也可设环境变量 S2_API_KEY）；不传走匿名公共通道")
    ap.add_argument("--out", help="报告输出路径（默认 stdout）")
    args = ap.parse_args(argv)

    global _MAILTO, _S2_API_KEY
    if args.mailto:
        _MAILTO = args.mailto.strip()
    if args.s2_api_key:
        _S2_API_KEY = args.s2_api_key.strip()

    citing = args.citing
    cited = args.cited
    if not (citing and cited):
        if len(args.dois) >= 2:
            citing, cited = args.dois[0], args.dois[1]
        else:
            ap.error("请提供 <citing_doi> <cited_doi> 或 --citing/--cited")

    rec = verify_edge(citing, cited)
    out = json.dumps(rec, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"报告已写入 {args.out}", file=sys.stderr)
    else:
        print(out)
    return 0


def _selftest():
    """离线自测：猴子补丁开放索引函数，验证三态裁决与 DOI 解析。"""
    print("### verify_citation_edge 离线自测")
    global _oc_check, _s2_check
    orig_oc, orig_s2 = _oc_check, _s2_check

    def fake_oc(citing: str, cited: str):
        if citing == "10.a/citing" and cited == "10.b/cited":
            return True, True, {"opencitations_references": 200, "opencitations_citations": 200}
        if citing == "10.a/citing" and cited == "10.z/missing":
            return False, True, {"opencitations_references": 200, "opencitations_citations": 200}
        return False, False, {"opencitations_references": 0, "opencitations_citations": 0}

    def fake_s2(citing: str, cited: str):
        if citing == "10.s2/citing" and cited == "10.s2/cited":
            return True, True, 200
        if citing == "10.a/citing" and cited == "10.z/missing":
            return False, True, 200
        return False, False, 0

    try:
        _oc_check, _s2_check = fake_oc, fake_s2
        confirmed = verify_edge("https://doi.org/10.A/CITING", "doi:10.B/CITED")
        assert confirmed["status"] == "confirmed" and "opencitations" in confirmed["sources"], confirmed
        assert "edge_exists" not in confirmed, confirmed

        s2_confirmed = verify_edge("10.s2/citing", "10.s2/cited")
        assert s2_confirmed["status"] == "confirmed" and "semanticscholar" in s2_confirmed["sources"], s2_confirmed

        absent = verify_edge("10.a/citing", "10.z/missing")
        assert absent["status"] == "not_in_open_index", absent
        assert "未覆盖 ≠ 未引用" in absent["note"], absent["note"]

        unknown = verify_edge("10.offline/a", "10.offline/b")
        assert unknown["status"] == "unknown", unknown
        assert _split_dois("doi:10.1/a doi:10.2/b") == ["10.1/a", "10.2/b"]
    finally:
        _oc_check, _s2_check = orig_oc, orig_s2
    print("[selftest] PASS verify_citation_edge offline")




if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--selftest":
        _selftest()
    else:
        sys.exit(main())
