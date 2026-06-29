#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_refs.py — 一批 DOI 的真实性 + 元数据一致性核验，产机读 JSON 报告。

对每个 DOI 同时查 Crossref `/works/{doi}` 与 OpenAlex `/works/https://doi.org/{doi}`，
核对：是否存在、标题/年份是否一致、被引数、是否自引、出版年龄、**是否被撤稿**。
另从 OpenAlex 同一响应读开放性字段（is_oa/oa_status/venue/is_in_doaj/type/version，不新增 HTTP）。
汇总：中外文献占比、自引率、缺近 2 年标志、预印本数、撤稿数、errors[].severity / warnings[]。

撤稿检测复用 light-research-ethics/check_retractions.py 的判定口径（同源真相，见其 FLAG_TYPES）：
读同一份 Crossref message 的 update-to[] 字段，type 命中 retraction/withdrawal 报 high severity；
另把标题 `RETRACTED` 前缀作补充信号（经典撤稿论文本身常不暴露 update-to[]，仅标题带前缀）。
不新增 HTTP（update-to 就在已取的 Crossref 响应里）。诚实局限：无信号 != 保证未撤稿，
高风险引用须交叉查 Retraction Watch（见 check_retractions.py 注释）。

OA 字段定位"开放性/可访问性"，非权威性；权威性须人工查 DOAJ/分区/预警名单。
warning 只对预印本或非正式版本产生；闭源(oa_status=closed)绝不告警（顶刊多闭源）。

实测端点（2026-06-06，均 HTTP 200）：
  https://api.crossref.org/works/10.1038/s41597-023-02555-8[?mailto=...]
  https://api.openalex.org/works/https://doi.org/10.1038/...[?mailto=...&api_key=...]

诚实原则：只报 API 真实返回；查不到 -> error severity=high（疑似臆造/需核查），不替它圆场。
礼貌池邮箱经环境变量 OPENALEX_MAILTO / CROSSREF_MAILTO 或 --mailto 传入；不传则匿名查询（不伪造）。
OpenAlex key 经环境变量 OPENALEX_API_KEY 或 --api-key 传入（2026 起需 key，口径见 m01 references）。

用法：
  python scripts/verify_refs.py 10.1038/s41597-023-02555-8 10.1145/3292500.3330701
  python scripts/verify_refs.py --file dois.txt --self-author "Vayssade" --mailto you@inst.edu --out report.json
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 礼貌池邮箱：优先环境变量（OpenAlex 用 OPENALEX_MAILTO，Crossref 用 CROSSREF_MAILTO；
# 两者皆空时回退 --mailto），都不传则匿名查询（不伪造邮箱）。不再硬编码伪造邮箱。
# OpenAlex API key：2026 起 OpenAlex 需免费 key，经 --api-key 或环境变量 OPENALEX_API_KEY 传入；
# key/限流/计费的唯一口径见 light-literature-search references「OpenAlex 接入真相源」节，本脚本不复写。
_MAILTO = (os.environ.get("OPENALEX_MAILTO") or os.environ.get("CROSSREF_MAILTO") or "").strip()
_API_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
THIS_YEAR = datetime.date.today().year

# 标题一致性告警阈值（Crossref vs OpenAlex 标题字符级 Jaccard 低于此值 → 提示人工确认）。
# 经验默认值、可调：0.6 是"明显不是同一篇"的保守线（含副标题差异/大小写/标点归一后仍偏低才报），
# 调高更敏感(更多告警)、调低更宽松。非数据反推，按需改。
TITLE_SIM_WARN = 0.6


def _user_agent() -> str:
    if _MAILTO:
        return "light-citation/1.0 (mailto:%s)" % _MAILTO
    return "light-citation/1.0"


def _oa_params(params: dict) -> str:
    """OpenAlex 查询参数：按需带 mailto（礼貌池）与 api_key（2026 起需 key）。"""
    p = dict(params)
    if _MAILTO:
        p.setdefault("mailto", _MAILTO)
    if _API_KEY:
        p.setdefault("api_key", _API_KEY)
    return urllib.parse.urlencode(p)


def _cr_suffix() -> str:
    """Crossref polite-pool 后缀：带 mailto 进 polite pool，不带则匿名。"""
    return ("?mailto=" + urllib.parse.quote(_MAILTO, safe="")) if _MAILTO else ""

CN_RE = re.compile(r"[一-鿿]")

# 撤稿/更正判定类型，与 light-research-ethics/check_retractions.py FLAG_TYPES 同源（单一口径）。
# update-to[].type 命中 retraction/withdrawal -> 撤稿(high)；correction/EoC -> 仅 warning。
# 类型集单一真相源：skills/light-research-ethics/references/retraction_flag_types.json；
# 跨技能路径在某些 CI 工作目录可能解析失败 -> 静默回退内联默认，保证离线 selftest 不依赖该文件。
_RET_FALLBACK = {"retraction", "withdrawal"}
_CON_FALLBACK = {"correction", "expression_of_concern"}


def _load_flag_types():
    path = os.path.join(os.path.dirname(__file__), "..", "..",
                        "light-research-ethics", "references", "retraction_flag_types.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        ret, con = set(data["retraction_level"]), set(data["concern_level"])
        if ret and con:
            return ret, con
    except Exception:
        pass
    return set(_RET_FALLBACK), set(_CON_FALLBACK)


RETRACTION_TYPES, CONCERN_TYPES = _load_flag_types()
RETRACTED_TITLE_RE = re.compile(r"^\s*retracted\b", re.I)


def _get_json(url: str, timeout: int = 30):
    """返回 (http_code, obj_or_None)。"""
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent(), "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None
    except (urllib.error.URLError, TimeoutError):
        return 0, None


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9一-鿿]+", "", (s or "").lower())


def _title_match(a: str, b: str) -> float:
    """粗略标题一致度：归一化后字符级 Jaccard（够用，不引外部依赖）。"""
    sa, sb = set(_norm(a)), set(_norm(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def verify_one(doi: str, self_authors=None, claimed=None):
    """核验单个 DOI，返回结构化记录。
    claimed: 可选 {"title": 声称标题, "first_author": 声称首作者姓}——用于**嵌合引用检测**
    （Chimeric Citation：DOI 真实存在、标题也对，但作者被换成别人，借 PHY041）。"""
    self_authors = [s.lower() for s in (self_authors or [])]
    claimed = claimed or {}
    doi = doi.strip().replace("https://doi.org/", "").replace("doi:", "")
    rec = {"doi": doi, "found_crossref": False, "found_openalex": False,
           "http": {}, "title": None, "year": None,
           "cited_by_count": None, "is_cn": False, "is_self_cite": False,
           "is_oa": None, "oa_status": None, "venue": None,
           "is_in_doaj": None, "oa_type": None, "version": None,
           "is_retracted": False, "retraction_flags": [], "is_chimeric": False,
           "unverified_offline": False, "errors": [], "warnings": []}

    # --- Crossref ---
    cr_url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}" + _cr_suffix()
    code, cr = _get_json(cr_url)
    rec["http"]["crossref"] = code
    cr_title = cr_year = None
    authors_str = ""
    if code == 200 and cr and cr.get("message"):
        m = cr["message"]
        rec["found_crossref"] = True
        cr_title = (m.get("title") or [None])[0]
        rec["title"] = cr_title
        dp = m.get("issued", {}).get("date-parts", [[None]])
        cr_year = dp[0][0] if dp and dp[0] else None
        rec["year"] = cr_year
        rec["cited_by_count"] = m.get("is-referenced-by-count")
        auth = m.get("author", []) or []
        authors_str = " ".join((a.get("family", "") + " " + a.get("given", "")) for a in auth)
        rec["is_cn"] = bool(CN_RE.search(cr_title or "")) or "China" in authors_str
        # 嵌合引用检测（Chimeric Citation，借 PHY041）：DOI 真实、标题也对得上，但声称的首作者
        # 不在真实作者列表里 —— 典型 AI 幻觉"真标题配错作者"。仅在提供 claimed.first_author 时查。
        claimed_fa = (claimed.get("first_author") or "").strip().lower()
        if claimed_fa:
            real_fams = [(a.get("family", "") or "").strip().lower() for a in auth]
            real_fams = [f for f in real_fams if f]
            # 声称首作者姓未出现在任何真实作者姓里 → 疑似嵌合（姓做子串双向匹配，容缩写/音译差异）
            hit = any(claimed_fa == f or claimed_fa in f or f in claimed_fa for f in real_fams)
            claimed_title = (claimed.get("title") or "").strip().lower()
            title_match = (not claimed_title) or (cr_title and
                          _title_match(claimed_title, cr_title.lower()) >= TITLE_SIM_WARN)
            if title_match and real_fams and not hit:
                rec["is_chimeric"] = True
                rec["errors"].append({"severity": "high",
                    "msg": f"疑似嵌合引用（Chimeric）：DOI/标题真实，但声称首作者『{claimed.get('first_author')}』"
                           f"不在真实作者 {[a.get('family') for a in auth][:4]} 中——典型'真标题配错作者'"
                           f"幻觉，核对原文作者后改正"})
        # --- 撤稿检测（复用 check_retractions.py 口径，同一份 message，不新增 HTTP）---
        for u in (m.get("update-to") or []):
            utype = (u.get("type") or "").lower().replace("-", "_")
            if utype in RETRACTION_TYPES:
                rec["retraction_flags"].append({"type": utype, "doi": u.get("DOI"),
                                                "label": u.get("label"), "source": "crossref:update-to"})
            elif utype in CONCERN_TYPES:
                rec["warnings"].append(
                    f"该文献有 {utype}（更正/关注声明，Crossref update-to）：引用前确认是否影响所引结论")
        # 经典撤稿论文本身常不暴露 update-to，仅标题带 RETRACTED 前缀，作补充信号
        if RETRACTED_TITLE_RE.match(cr_title or ""):
            rec["retraction_flags"].append({"type": "retraction", "doi": doi,
                                            "label": "title-prefixed RETRACTED", "source": "crossref:title"})
        if rec["retraction_flags"]:
            rec["is_retracted"] = True
            rec["errors"].append({"severity": "high",
                                  "msg": "该文献已被撤稿（Crossref 撤稿信号），严禁作为有效证据引用，须删除或换源"})
    else:
        # 区分"网络失败(code=0)"与"连上了但查无此 DOI(404 等)"：
        # 前者是无法核验（不可冒充已核验，也不可诬为臆造），后者才是疑似臆造。
        if code == 0:
            rec["net_fail_crossref"] = True
        else:
            rec["errors"].append({"severity": "high",
                                  "msg": f"Crossref 查不到该 DOI（HTTP {code}）——疑似臆造或 DOI 错误，需核查"})

    # --- OpenAlex ---
    oa_url = (f"https://api.openalex.org/works/https://doi.org/{urllib.parse.quote(doi)}"
              + ("?" + _oa_params({}) if (_MAILTO or _API_KEY) else ""))
    code2, oa = _get_json(oa_url)
    rec["http"]["openalex"] = code2
    if code2 == 200 and oa and oa.get("id"):
        rec["found_openalex"] = True
        oa_title = oa.get("title")
        oa_year = oa.get("publication_year")
        if rec["year"] is None:
            rec["year"] = oa_year
        if rec["cited_by_count"] is None:
            rec["cited_by_count"] = oa.get("cited_by_count")
        # 一致性
        if cr_title and oa_title:
            sim = _title_match(cr_title, oa_title)
            if sim < TITLE_SIM_WARN:
                rec["warnings"].append(
                    f"Crossref 与 OpenAlex 标题不一致(相似度{sim:.2f}<{TITLE_SIM_WARN})，请人工确认")
        if cr_year and oa_year and abs(cr_year - oa_year) > 1:
            rec["warnings"].append(f"年份不一致：Crossref {cr_year} vs OpenAlex {oa_year}")
        # 语言/国别
        if oa.get("language") == "zh":
            rec["is_cn"] = True
        # --- 开放性字段（复用本次 OpenAlex 响应，不新增 HTTP；规避 Unpaywall 邮箱坑）---
        oaobj = oa.get("open_access") or {}
        rec["is_oa"] = oaobj.get("is_oa")
        rec["oa_status"] = oaobj.get("oa_status")  # gold/green/hybrid/bronze/closed
        rec["oa_type"] = oa.get("type")            # journal-article/preprint/...
        ploc = oa.get("primary_location") or {}
        src = ploc.get("source") or {}
        rec["venue"] = src.get("display_name")
        rec["is_in_doaj"] = src.get("is_in_doaj")
        rec["version"] = ploc.get("version")       # publishedVersion/acceptedVersion/...
        # warning 判据：仅预印本 或 非正式版本才告警；闭源(closed)绝不告警（顶刊多闭源）
        if rec["oa_type"] == "preprint":
            rec["warnings"].append(
                "疑似预印本(type=preprint)：引用须注明未经同行评审，或换正式发表版 DOI")
        elif rec["version"] and rec["version"] != "publishedVersion":
            rec["warnings"].append(
                f"非正式发表版本(version={rec['version']})：确认是否应换 publishedVersion DOI")
    else:
        if rec["found_crossref"]:
            rec["warnings"].append(f"OpenAlex 未收录（HTTP {code2}），仅 Crossref 单源，建议补证")
        elif code == 0 and code2 == 0:
            # 两源都网络失败 → 无法核验（离线降级），不报 high error，明确需联网重试
            rec["unverified_offline"] = True
            rec["warnings"].append(
                "⚠ 网络不可达，Crossref+OpenAlex 均未连通——该引用【未核验】，"
                "不可当作已核验/已证伪；联网后须重跑 verify_refs.py 再下结论")
        else:
            rec["errors"].append({"severity": "high",
                                  "msg": f"Crossref+OpenAlex 双源均查不到（HTTP {code}/{code2}）——高度疑似臆造"})

    # --- 自引判断（按作者姓精确词匹配，而非整串子串：避免 "li" 误命中 "Smolin" 等高频姓子串）---
    if self_authors and auth:
        real_fams = {(a.get("family", "") or "").strip().lower() for a in auth if a.get("family")}
        # 精确姓匹配 + 全名兜底（中文整名塞 family 时）；不再用 `sa in 整串` 的脆弱子串
        if any(sa in real_fams or any(sa == f for f in real_fams) for sa in self_authors):
            rec["is_self_cite"] = True
        else:
            rec["self_cite_note"] = "按作者姓精确匹配未判为自引（旧子串匹配可能误报，已升级）"
    elif self_authors and authors_str:
        # auth 缺失（仅有拼接串）时退回子串但标注不可靠
        low = authors_str.lower()
        if any(sa in low for sa in self_authors):
            rec["is_self_cite"] = True
            rec["warnings"].append("自引按整串子串判定（无结构化作者列表），高频姓可能误报，人工复核")

    # --- 时效性 ---
    if rec["year"] and rec["year"] <= THIS_YEAR - 6 and (rec["cited_by_count"] or 0) < 5:
        rec["warnings"].append(
            f"较旧({rec['year']})且被引偏低({rec['cited_by_count']})，代表性存疑")
    return rec


def build_report(dois, self_authors=None):
    items = [verify_one(d, self_authors) for d in dois if d.strip()]
    n = len(items)
    cn = sum(1 for r in items if r["is_cn"])
    self_n = sum(1 for r in items if r["is_self_cite"])
    recent = sum(1 for r in items if (r["year"] or 0) >= THIS_YEAR - 2)
    n_err = sum(len(r["errors"]) for r in items)
    preprint_n = sum(1 for r in items if r.get("oa_type") == "preprint")
    retracted_n = sum(1 for r in items if r.get("is_retracted"))
    unverified_offline_n = sum(1 for r in items if r.get("unverified_offline"))
    summary = {
        "total": n,
        "verified_ok": sum(1 for r in items if r["found_crossref"] and not r["errors"]),
        "high_severity_errors": n_err,
        "unverified_offline_count": unverified_offline_n,
        "cn_count": cn, "foreign_count": n - cn,
        "cn_ratio": round(cn / n, 3) if n else 0,
        "self_citation_rate": round(self_n / n, 3) if n else 0,
        "recent_2y_count": recent,
        "missing_recent_2y": recent == 0 and n > 0,
        "preprint_count": preprint_n,
        "retracted_count": retracted_n,
        "retraction_signals_used": ["crossref:update-to[retraction/withdrawal]", "title:RETRACTED 前缀"],
        "retraction_coverage": (
            f"已用上述 2 类信号扫了 {n} 条；命中 {retracted_n} 条。"
            "⚠ retracted_count=0 ≠ 保证全部未撤稿——经典撤稿常不暴露 Crossref update-to[]，"
            "本脚本主路径会漏报。高风险/高龄引用须**交叉查 Retraction Watch**（"
            "可选第二跳：跑 a10 `light-research-ethics/scripts/check_retractions.py --file dois.txt` "
            "独立复核，其口径同源但单独成报，把'已查信号'与'未覆盖经典撤稿'分开看）。"),
        "retraction_note": "撤稿判定复用 check_retractions.py 口径（Crossref update-to + 标题 RETRACTED 前缀）；无信号≠保证未撤稿，高风险引用须交叉查 Retraction Watch",
        "authority_note": "权威性/掠夺性判定需人工+查 DOAJ/分区/预警名单；脚本仅给 OA 线索，oa_status 反映开放性≠权威性",
        "offline_note": ("⚠ 有 %d 条引用因网络不可达【未核验】（非疑似臆造）：离线降级不放行核验闸门，"
                         "联网后须重跑再判真实性，切勿当作已核验通过" % unverified_offline_n)
                        if unverified_offline_n else "全部引用均已联网核验（无离线未核验项）",
        "checked_at": datetime.date.today().isoformat(),
    }
    return {"summary": summary, "items": items}


def main(argv=None):
    ap = argparse.ArgumentParser(description="批量 DOI 真实性/一致性核验 -> 机读 JSON")
    ap.add_argument("dois", nargs="*", help="DOI 列表")
    ap.add_argument("--file", help="每行一个 DOI 的文件")
    ap.add_argument("--self-author", action="append", default=[],
                    help="本文作者姓氏（判自引），可多次")
    ap.add_argument("--mailto", default="",
                    help="礼貌池邮箱（也可设环境变量 OPENALEX_MAILTO / CROSSREF_MAILTO）；不传则匿名查")
    ap.add_argument("--api-key", default="",
                    help="OpenAlex API key（也可设环境变量 OPENALEX_API_KEY）；口径见 m01 references")
    ap.add_argument("--out", help="报告输出路径（默认 stdout）")
    args = ap.parse_args(argv)

    global _MAILTO, _API_KEY
    if args.mailto:
        _MAILTO = args.mailto.strip()
    if args.api_key:
        _API_KEY = args.api_key.strip()

    dois = list(args.dois)
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            dois += [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    if not dois:
        ap.error("请提供至少一个 DOI 或 --file")

    report = build_report(dois, args.self_author)
    out = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"报告已写入 {args.out}", file=sys.stderr)
    else:
        print(out)
    return 0


def _selftest():
    """离线自测：猴子补丁 verify_one，验证报告汇总/OA 字段/告警边界。"""
    print("### verify_refs 离线自测")
    global verify_one
    orig_verify_one = verify_one

    def fake_verify_one(doi: str, self_authors=None):
        if "missing" in doi:
            return {
                "doi": doi, "found_crossref": False, "found_openalex": False,
                "http": {"crossref": 404, "openalex": 404}, "title": None, "year": None,
                "cited_by_count": None, "is_cn": False, "is_self_cite": False,
                "is_oa": None, "oa_status": None, "venue": None, "is_in_doaj": None,
                "oa_type": None, "version": None,
                "is_retracted": False, "retraction_flags": [],
                "errors": [{"severity": "high", "msg": "synthetic missing DOI"}], "warnings": [],
            }
        return {
            "doi": doi, "found_crossref": True, "found_openalex": True,
            "http": {"crossref": 200, "openalex": 200},
            "title": "Synthetic Dataset", "year": THIS_YEAR,
            "cited_by_count": 12, "is_cn": False, "is_self_cite": True,
            "is_oa": False, "oa_status": "closed", "venue": "Synthetic Journal",
            "is_in_doaj": False, "oa_type": "journal-article", "version": "publishedVersion",
            "is_retracted": False, "retraction_flags": [],
            "errors": [], "warnings": [],
        }

    try:
        verify_one = fake_verify_one
        rep = build_report(["10.1234/ok", "10.0000/missing"], self_authors=["Smith"])
    finally:
        verify_one = orig_verify_one

    s = rep["summary"]
    assert s["total"] == 2 and s["verified_ok"] == 1, s
    assert s["high_severity_errors"] == 1, s
    assert s["self_citation_rate"] == 0.5, s
    assert "preprint_count" in s and "authority_note" in s, s
    assert "retracted_count" in s and "retraction_note" in s, s
    ok = rep["items"][0]
    assert ok["oa_status"] == "closed" and not ok["warnings"], ok
    assert _title_match("A reliable dataset", "Reliable dataset") > 0.6

    # --- 撤稿检测分支：mock _get_json 让 verify_one 真跑 update-to / 标题前缀解析 ---
    global _get_json
    orig_get_json = _get_json

    def fake_get_json(url, timeout=30):
        if "crossref" not in url:
            return 404, None  # 不查 OpenAlex，聚焦撤稿分支
        if "retr.updateto" in url:  # update-to 暴露 retraction
            return 200, {"message": {"title": ["A flawed study"], "issued": {"date-parts": [[2020]]},
                                     "update-to": [{"type": "retraction", "DOI": "10.x/notice"}]}}
        if "retr.title" in url:  # 仅标题带 RETRACTED 前缀（经典案例，update-to 空）
            return 200, {"message": {"title": ["RETRACTED: An old retracted paper"],
                                     "issued": {"date-parts": [[2020]]}}}
        if "concern" in url:  # correction/EoC -> 仅 warning，不算撤稿
            return 200, {"message": {"title": ["A corrected paper"], "issued": {"date-parts": [[2021]]},
                                     "update-to": [{"type": "correction", "DOI": "10.x/corr"}]}}
        return 200, {"message": {"title": ["A clean paper"], "issued": {"date-parts": [[2024]]}}}

    try:
        _get_json = fake_get_json
        r_ut = verify_one("10.0000/retr.updateto")
        r_ti = verify_one("10.0000/retr.title")
        r_co = verify_one("10.0000/concern")
        r_cl = verify_one("10.0000/clean")
    finally:
        _get_json = orig_get_json

    assert r_ut["is_retracted"] and any(e["severity"] == "high" for e in r_ut["errors"]), r_ut
    assert r_ti["is_retracted"] and r_ti["retraction_flags"][0]["source"] == "crossref:title", r_ti
    assert not r_co["is_retracted"] and any("更正" in w or "correction" in w for w in r_co["warnings"]), r_co
    assert not r_cl["is_retracted"] and not any(e.get("msg", "").startswith("该文献已被撤稿") for e in r_cl["errors"]), r_cl

    # --- CT-5 嵌合引用检测：DOI 真实+标题对，但声称首作者不在真实作者列表 ---
    def fake_get_chimeric(url, timeout=30):
        if "crossref" not in url:
            return 404, None
        return 200, {"message": {
            "title": ["Attention Is All You Need"], "issued": {"date-parts": [[2017]]},
            "author": [{"family": "Vaswani", "given": "Ashish"},
                       {"family": "Shazeer", "given": "Noam"}]}}
    try:
        _get_json = fake_get_chimeric
        # 声称首作者 "Smith"（真实是 Vaswani）→ 嵌合
        r_chi = verify_one("10.0000/real.doi", claimed={"first_author": "Smith",
                           "title": "Attention Is All You Need"})
        # 声称首作者 "Vaswani"（对得上）→ 不嵌合
        r_okc = verify_one("10.0000/real.doi", claimed={"first_author": "Vaswani"})
    finally:
        _get_json = orig_get_json
    assert r_chi["is_chimeric"] and any("嵌合" in e["msg"] for e in r_chi["errors"]), r_chi
    assert not r_okc["is_chimeric"], r_okc

    # --- CT-2 撤稿覆盖度：summary 显式区分"已用信号"与"未覆盖经典撤稿" ---
    assert "retraction_coverage" in s and "retraction_signals_used" in s, s
    assert "Retraction Watch" in s["retraction_coverage"], s["retraction_coverage"]

    # --- 离线降级分支：两源 code=0(网络失败) → unverified_offline，不诬为"疑似臆造"high error ---
    def fake_get_offline(url, timeout=30):
        return 0, None  # 模拟网络不可达

    def fake_get_404(url, timeout=30):
        return 404, None  # 模拟连上了但查无此 DOI

    try:
        _get_json = fake_get_offline
        r_off = verify_one("10.0000/offline.case")
        _get_json = fake_get_404
        r_404 = verify_one("10.0000/truly.missing")
    finally:
        _get_json = orig_get_json
    # 网络失败：标记未核验、给 warning、绝不报 high severity "疑似臆造"
    assert r_off["unverified_offline"] is True, r_off
    assert not r_off["errors"], r_off  # 无 high error
    assert any("未核验" in w for w in r_off["warnings"]), r_off["warnings"]
    # 真查不到(404)：仍报 high severity 疑似臆造，离线降级不能掩盖真问题
    assert r_404["unverified_offline"] is False, r_404
    assert any(e["severity"] == "high" for e in r_404["errors"]), r_404
    # build_report 汇总把离线未核验数单列，offline_note 提示不放行核验闸门
    try:
        _get_json = fake_get_offline
        rep_off = build_report(["10.0000/a", "10.0000/b"])
    finally:
        _get_json = orig_get_json
    assert rep_off["summary"]["unverified_offline_count"] == 2, rep_off["summary"]
    assert "未核验" in rep_off["summary"]["offline_note"], rep_off["summary"]["offline_note"]
    print("[selftest] PASS verify_refs offline")




if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--selftest":
        _selftest()
    else:
        sys.exit(main())
