#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""doi_to_any.py — DOI 一键转多格式引用。

通过 DOI.org 内容协商（Content Negotiation）取回 BibTeX / CSL JSON / RIS，
以及 APA / IEEE 的 CSL 排版文本；再由 CSL JSON 在本地排版成 GB/T 7714-2015
（顺序编码制）中文国标文本（内容协商无中文国标 style，故本地排版）。

实测端点（2026-06-06，HTTP 200）：
  curl -LH "Accept: application/x-bibtex" https://doi.org/10.1038/s41597-023-02555-8
  curl -LH "Accept: application/vnd.citationstyles.csl+json" https://doi.org/<doi>
  curl -LH "Accept: text/x-bibliography; style=apa" https://doi.org/<doi>

诚实原则（CONVENTIONS §4）：只对真实 DOI 协商，不臆造字段；取不到即如实报错。
APA/IEEE 为 DOI 内容协商直出的 CSL 排版文本（非脚本本地排版），输出已注明来源。
礼貌池邮箱经环境变量 CROSSREF_MAILTO 或 --mailto 传入；不传则匿名（不伪造）。

用法：
  python scripts/doi_to_any.py 10.1038/s41597-023-02555-8
  python scripts/doi_to_any.py 10.1038/... --format bibtex|csljson|gbt7714|apa|ieee|ris|all
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

DOI_BASE = "https://doi.org/"
# 礼貌池邮箱：优先环境变量 CROSSREF_MAILTO（doi.org 内容协商背后是 Crossref/DataCite），
# 其次 --mailto，都不传则匿名（不伪造）。doi.org 内容协商不强制 mailto，但带真实邮箱更礼貌。
_MAILTO = (os.environ.get("CROSSREF_MAILTO") or os.environ.get("OPENALEX_MAILTO") or "").strip()
# 直出格式：bibtex/csljson/ris 由 DOI 内容协商一次取回；
# apa/ieee 走 DOI 内容协商 text/x-bibliography; style=（CSL 排版文本，Crossref/DataCite 支持）；
# gbt7714 由 csljson 本地排版（中文国标，内容协商无此 style）。
ACCEPT = {
    "bibtex": "application/x-bibtex",
    "csljson": "application/vnd.citationstyles.csl+json",
    "ris": "application/x-research-info-systems",
    "apa": "text/x-bibliography; style=apa",
    "ieee": "text/x-bibliography; style=ieee",
}


def _user_agent() -> str:
    if _MAILTO:
        return "light-citation/1.0 (mailto:%s)" % _MAILTO
    return "light-citation/1.0"


def _has_cjk(text: str) -> bool:
    """判断字符串是否含 CJK 汉字（用于推断 langid）。"""
    for ch in text or "":
        if "一" <= ch <= "鿿" or "㐀" <= ch <= "䶿":
            return True
    return False


def inject_langid(bibtex: str) -> str:
    """给 BibTeX 条目注入 langid 字段（GB/T 7714 排版必需）。

    按 author/title 是否含 CJK 字符判定：含汉字→langid={chinese}，否则→{english}。
    已存在 langid 的条目不重复注入。诚实原则：只依据真实字段判定，不臆造。
    """
    if not bibtex or "@" not in bibtex:
        return bibtex
    if "langid" in bibtex.lower():
        return bibtex
    lang = "chinese" if _has_cjk(bibtex) else "english"
    # 定位 @type{citekey, 后的首个逗号，在其后插入 langid 字段（兼容单行/多行）
    brace = bibtex.find("{")
    if brace == -1:
        return bibtex
    comma = bibtex.find(",", brace)
    if comma == -1:
        return bibtex
    return f"{bibtex[:comma + 1]} langid={{{lang}}},{bibtex[comma + 1:]}"


def negotiate(doi: str, kind: str, timeout: int = 30):
    """对 DOI 做内容协商，返回 (http_code, text)。kind ∈ ACCEPT。"""
    doi = doi.strip().replace("https://doi.org/", "").replace("doi:", "")
    req = urllib.request.Request(
        DOI_BASE + doi,
        headers={"Accept": ACCEPT[kind], "User-Agent": _user_agent()},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


# ---------- CSL JSON -> GB/T 7714-2015 顺序编码制排版 ----------
_TYPE_TAG = {
    "article-journal": "J",
    "paper-conference": "C",
    "book": "M",
    "chapter": "M",
    "thesis": "D",
    "report": "R",
    "patent": "P",
    "standard": "S",
    "dataset": "DS",
    "webpage": "EB/OL",
    "article": "J",
}


def _has_cjk(s: str) -> bool:
    """是否含 CJK 汉字（中日韩统一表意文字区段）。中文名不能套西文缩写。"""
    return any("一" <= ch <= "鿿" or "㐀" <= ch <= "䶿" for ch in (s or ""))


def _fmt_authors_gbt(authors, limit: int = 3) -> str:
    """GB/T 7714：作者≤3 全列，>3 取前 limit 加 '等'。
    西文：姓前名后、名取首字母大写（FamilyName G. M.）。
    中文（CJK）：整名作单元，**姓名连写不缩写、不加点**（如"张伟"非"张 W."）——修中文名被西文
    缩写逻辑误处理的 bug。literal/混合也按是否含 CJK 分流。"""
    if not authors:
        return "[佚名]"
    names = []
    for a in authors:
        if "literal" in a:
            lit = a["literal"]
            # literal 整名：含 CJK 原样保留（中文常把整名塞 literal/family），否则原样
            names.append(lit)
            continue
        fam = (a.get("family") or "").strip()
        giv = (a.get("given") or "").strip()
        # CJK 作者：family/given 任一含汉字 → 整名连写，不缩写
        if _has_cjk(fam) or _has_cjk(giv):
            names.append((fam + giv).strip() or fam or giv)
        elif fam and giv:
            # 西文：FamilyName G. M.（缩写名）
            initials = " ".join(p[0].upper() + "." for p in giv.replace(".", " ").split() if p)
            names.append(f"{fam} {initials}".strip())
        else:
            # 只有 family（可能是整名 literal 塞进 family）：含 CJK 原样，否则原样
            names.append(fam or giv or a.get("name", ""))
    if len(names) > limit:
        return ", ".join(names[:limit]) + ", 等"
    return ", ".join(names)


def csljson_to_gbt7714(csl: dict) -> str:
    """把单条 CSL JSON 排版成 GB/T 7714-2015 顺序编码制书目文本。"""
    typ = csl.get("type", "article-journal")
    tag = _TYPE_TAG.get(typ, "J")
    authors = _fmt_authors_gbt(csl.get("author") or [])
    title = html.unescape((csl.get("title") or "")).rstrip(".")
    container = html.unescape(csl.get("container-title") or csl.get("publisher") or "")
    issued = csl.get("issued", {}).get("date-parts", [[None]])
    year = issued[0][0] if issued and issued[0] else ""
    vol = csl.get("volume", "")
    issue = csl.get("issue", "")
    page = csl.get("page", "")
    doi = csl.get("DOI") or csl.get("DOI".lower(), "")
    url = csl.get("URL") or csl.get("url") or ""
    # 访问日期（电子资源 [EB/OL] 国标要求）：CSL accessed
    acc = csl.get("accessed", {}).get("date-parts", [[None]])
    acc_date = ""
    if acc and acc[0] and acc[0][0]:
        acc_date = "-".join(str(x).zfill(2) if i else str(x) for i, x in enumerate(acc[0]))

    parts = [f"{authors}. {title}[{tag}]."]
    if container:
        seg = f" {container}"
        if year:
            seg += f", {year}"
        if vol:
            seg += f", {vol}"
            if issue:
                seg += f"({issue})"
        if page:
            seg += f": {page}"
        parts.append(seg + ".")
    elif year:
        parts.append(f" {year}.")
    # 电子资源 [EB/OL]/[DS]：国标要求带访问日期与 URL；缺则显式占位提示补全（不静默丢）
    if tag in ("EB/OL", "DS"):
        if acc_date:
            parts.append(f" [{acc_date}].")
        else:
            parts.append(" [访问日期待补].")
    if doi:
        parts.append(f" DOI: {doi}.")
    elif url and tag in ("EB/OL", "DS"):
        parts.append(f" {url}.")
    return "".join(parts)


def main(argv=None):
    ap = argparse.ArgumentParser(description="DOI -> BibTeX / CSL JSON / GB-T 7714 / APA / IEEE / RIS")
    ap.add_argument("doi", help="DOI，如 10.1038/s41597-023-02555-8")
    ap.add_argument("--format", default="all",
                    choices=["bibtex", "csljson", "gbt7714", "apa", "ieee", "ris", "all"])
    ap.add_argument("--mailto", default="",
                    help="礼貌池邮箱（也可设环境变量 CROSSREF_MAILTO）；不传则匿名查")
    args = ap.parse_args(argv)

    global _MAILTO
    if args.mailto:
        _MAILTO = args.mailto.strip()

    # all = 常用四种（bibtex/csljson/gbt7714/apa）；ris/ieee 需显式指定，避免噪声
    want = ["bibtex", "csljson", "gbt7714", "apa"] if args.format == "all" else [args.format]

    # gbt7714 与 csljson 都依赖 CSL JSON
    csl_obj = None
    if "csljson" in want or "gbt7714" in want:
        code, txt = negotiate(args.doi, "csljson")
        print(f"[content-negotiation csljson] HTTP {code}", file=sys.stderr)
        if code == 200:
            csl_obj = json.loads(txt)

    if "bibtex" in want:
        code, txt = negotiate(args.doi, "bibtex")
        print(f"[content-negotiation bibtex] HTTP {code}", file=sys.stderr)
        print("=== BibTeX ===")
        print(inject_langid(txt.strip()) if code == 200 else f"[ERROR HTTP {code}] {txt[:200]}")

    if "csljson" in want:
        print("=== CSL JSON ===")
        print(json.dumps(csl_obj, ensure_ascii=False, indent=2)
              if csl_obj else "[ERROR] 取 CSL JSON 失败")

    if "gbt7714" in want:
        print("=== GB/T 7714-2015（顺序编码制） ===")
        print(csljson_to_gbt7714(csl_obj) if csl_obj else "[ERROR] 缺 CSL JSON，无法排版")

    # APA / IEEE：DOI 内容协商直出 CSL 排版文本（非脚本本地排版，故标来源）
    for style in ("apa", "ieee"):
        if style in want:
            code, txt = negotiate(args.doi, style)
            print(f"[content-negotiation {style}] HTTP {code}", file=sys.stderr)
            print(f"=== {style.upper()}（DOI 内容协商 CSL 排版，非本地排版） ===")
            print(txt.strip() if code == 200 else f"[ERROR HTTP {code}] {txt[:200]}")

    if "ris" in want:
        code, txt = negotiate(args.doi, "ris")
        print(f"[content-negotiation ris] HTTP {code}", file=sys.stderr)
        print("=== RIS（EndNote/Zotero 可导入） ===")
        print(txt.strip() if code == 200 else f"[ERROR HTTP {code}] {txt[:200]}")
    return 0


def _selftest():
    """离线自测：验证 DOI 格式化核心逻辑，不访问 doi.org/Crossref。"""
    print("### doi_to_any 离线自测")
    en_entry = "@article{smith2024demo, title={A Reliable Dataset}, author={Smith, John}, year={2024}}"
    en_tagged = inject_langid(en_entry)
    assert "langid={english}" in en_tagged, en_tagged

    cn_entry = (
        "@article{zhang2024shenjing,\n"
        "  title = {深度神经网络研究},\n"
        "  author = {张三 and 李四},\n"
        "  year = {2024},\n}"
    )
    cn_tagged = inject_langid(cn_entry)
    assert "langid={chinese}" in cn_tagged, cn_tagged
    assert inject_langid(cn_tagged).count("langid") == 1, "langid 注入应幂等"

    csl = {
        "type": "article-journal",
        "author": [{"family": "Smith", "given": "John Michael"}, {"family": "Wang", "given": "Li"}, {"family": "Brown", "given": "A"}, {"family": "Zhang", "given": "Wei"}],
        "title": "A Reliable Dataset.",
        "container-title": "Data Journal",
        "issued": {"date-parts": [[2024]]},
        "volume": "12",
        "issue": "3",
        "page": "10-20",
        "DOI": "10.1234/demo",
    }
    gbt = csljson_to_gbt7714(csl)
    assert "Smith J. M." in gbt and ", 等" in gbt, gbt
    assert "A Reliable Dataset[J]." in gbt and "DOI: 10.1234/demo." in gbt, gbt

    # CT-1 CJK 作者特判：中文名整名连写、不缩写不加点（修被西文逻辑误处理的 bug）
    cn_csl = {"type": "article-journal",
              "author": [{"family": "张", "given": "伟"}, {"family": "李娜"},
                         {"literal": "王建国"}],
              "title": "深度学习综述", "container-title": "计算机学报",
              "issued": {"date-parts": [[2023]]}, "volume": "46", "page": "1-20"}
    cn_gbt = csljson_to_gbt7714(cn_csl)
    assert "张伟" in cn_gbt, f"中文名应整名连写: {cn_gbt}"
    assert "张 W." not in cn_gbt and "张 伟" not in cn_gbt, f"中文名不应西文缩写: {cn_gbt}"
    assert "李娜" in cn_gbt and "王建国" in cn_gbt, cn_gbt
    # 西文与中文混合：西文仍缩写、中文不缩写
    assert _has_cjk("张伟") and not _has_cjk("Smith"), "_has_cjk 判定"

    # CT-1 电子资源 [EB/OL]：带访问日期占位（缺则显式提示补全，不静默丢）
    eb_csl = {"type": "webpage", "author": [{"literal": "OpenAI"}],
              "title": "GPT-X Technical Report", "URL": "https://example.org/x",
              "issued": {"date-parts": [[2024]]}}
    eb_gbt = csljson_to_gbt7714(eb_csl)
    assert "[EB/OL]" in eb_gbt, eb_gbt
    assert "访问日期待补" in eb_gbt, f"缺访问日期应显式占位: {eb_gbt}"
    assert "https://example.org/x" in eb_gbt, eb_gbt
    # 带访问日期则用真实日期
    eb_csl2 = dict(eb_csl, accessed={"date-parts": [[2026, 6, 14]]})
    assert "2026-06-14" in csljson_to_gbt7714(eb_csl2), csljson_to_gbt7714(eb_csl2)

    # 新增格式已注册到内容协商表（apa/ieee/ris 直出，离线只验注册与 Accept 头，不打网）
    for k in ("apa", "ieee", "ris"):
        assert k in ACCEPT, f"{k} 应在 ACCEPT 表"
    assert "style=apa" in ACCEPT["apa"] and "style=ieee" in ACCEPT["ieee"], ACCEPT
    print("[selftest] PASS doi_to_any offline")




if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--selftest":
        _selftest()
    else:
        sys.exit(main())
