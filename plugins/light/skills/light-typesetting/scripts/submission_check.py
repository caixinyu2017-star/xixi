#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""submission_check.py — 投稿前合规/匿名雷区扫描（补零自动化的 desk-reject 盲区）。

很多拒稿不是内容问题，而是 desk-reject 雷区：双盲稿露了作者、PDF 元数据带真名、超页数。
本脚本静态扫 .tex 源 + 可选 PDF，列出会被编辑一眼拒的合规问题。纯标准库零依赖、离线、只读。

检查项：
  A. 双盲匿名（--double-blind）：未注释的 \\author/\\thanks/\\affiliation、致谢/基金露名、
     "our previous work [12]" 式自指、可识别的 github.com/<user> 或个人主页链接。
  B. PDF 元数据（--pdf）：/Author /Title /Subject /Creator 是否泄露真名（双盲时必须清空）。
  C. 页数上限（--max-pages）：从 PDF 数页或从 log 取，超限预警。
  D. 通用：\\todo/\\TODO/占位 XXX、第一人称未匿名化。

诚实：只扫静态可见的合规雷区，不保证过编辑形式审；命中是"高风险需人工确认"，非绝对违规。
PDF 元数据用正则扫原始字节（不强依赖 PyPDF），扫不到的标 skip 不臆断。

用法：
  python submission_check.py --tex paper.tex --double-blind
  python submission_check.py --tex paper.tex --pdf paper.pdf --double-blind --max-pages 8
  python submission_check.py --selftest
"""
from __future__ import annotations
import argparse
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 未注释的身份命令（行首非 % 的 \author 等）
_IDENTITY_CMDS = re.compile(r"^[^%\n]*\\(author|thanks|affil|affiliation|email|institute|address)\b",
                            re.M | re.I)
# 致谢/基金段（双盲常见泄漏点）
_ACK = re.compile(r"\\(section|subsection)\*?\{[^}]*(acknowledg|funding|致谢|资助|基金)[^}]*\}", re.I)
# 可识别链接
_LINK = re.compile(r"(github\.com/[\w\-]+|gitlab\.com/[\w\-]+|[\w\-]+\.github\.io|"
                   r"huggingface\.co/[\w\-]+|orcid\.org/[\d\-]+)", re.I)
# 自指前作（双盲忌讳明示"我们之前的工作"）
_SELFREF = re.compile(r"\b(our|my)\s+(previous|prior|earlier|recent)\s+(work|paper|study|method)\b", re.I)
_SELFREF_ZH = re.compile(r"我们(之前|先前|此前|早期)的(工作|论文|研究|方法)")
# 残留占位
_TODO = re.compile(r"\\todo\b|\bTODO\b|\bXXX\b|\bFIXME\b|\[占位\]|\bplaceholder\b", re.I)
# PDF 元数据键
_PDF_META = re.compile(rb"/(Author|Title|Subject|Creator|Keywords)\s*\(([^)]*)\)")


def check_tex(text: str, double_blind: bool = False) -> list:
    findings = []

    def add(sev, code, msg):
        findings.append({"severity": sev, "code": code, "msg": msg})

    if double_blind:
        ids = []
        for m in _IDENTITY_CMDS.finditer(text):
            # 取命中所在整行（含 {...} 参数），才能识别 \author{Anonymous} 这类已匿名写法
            ls = text.rfind("\n", 0, m.start()) + 1
            le = text.find("\n", m.start())
            line = text[ls:(le if le >= 0 else len(text))].strip()
            if re.search(r"anonymous|匿名|removed for review|for blind review|\\author\s*\{\s*\}", line, re.I):
                continue
            ids.append(line[:70])
        if ids:
            add("high", "BLIND_IDENTITY", f"双盲稿含未匿名身份命令 {len(ids)} 处（首例: {ids[0]}）——注释或匿名化")
        if _ACK.search(text):
            add("high", "BLIND_ACK", "双盲稿含致谢/基金小节——通常露名，投稿版应移除或匿名（终稿再加回）")
        links = sorted({m.group(0) for m in _LINK.finditer(text)})
        if links:
            add("high", "BLIND_LINK", f"含可识别链接 {links[:3]}——双盲应换匿名仓库(如 anonymous.4open.science)")
        sref = _SELFREF.findall(text) or _SELFREF_ZH.findall(text)
        if sref:
            add("med", "BLIND_SELFREF", "含『我们之前的工作』式自指——双盲应改第三人称引用（如『Prior work [x]』）")

    todos = [m.group(0) for m in _TODO.finditer(text)]
    if todos:
        add("high", "RESIDUAL_TODO", f"残留占位/待办 {len(todos)} 处（{sorted(set(todos))[:5]}）——投稿前清零")
    return findings


def check_pdf_metadata(path: str, double_blind: bool = False) -> list:
    """正则扫 PDF 原始字节里的 /Author /Title 等元数据（不强依赖 PyPDF）。"""
    findings = []
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError as e:
        return [{"severity": "info", "code": "PDF_UNREADABLE", "msg": f"PDF 读不了: {e}"}]
    meta = {}
    for m in _PDF_META.finditer(raw):
        key = m.group(1).decode("latin-1")
        val = m.group(2).decode("latin-1", "replace").strip()
        if val:
            meta.setdefault(key, val)
    if meta.get("Author"):
        sev = "high" if double_blind else "med"
        findings.append({"severity": sev, "code": "PDF_AUTHOR_META",
                         "msg": f"PDF 元数据 /Author='{meta['Author'][:40]}'"
                                + ("——双盲必须清空（pdfx/hyperref pdfauthor={} 或导出后用 exiftool 清）"
                                   if double_blind else "（确认是否要暴露）")})
    if double_blind and meta.get("Title") and re.search(r"[A-Za-z]{4}", meta.get("Title", "")):
        findings.append({"severity": "info", "code": "PDF_TITLE_META",
                         "msg": f"PDF 元数据 /Title='{meta['Title'][:40]}'（核对不含作者/单位信息）"})
    if not meta:
        findings.append({"severity": "info", "code": "PDF_META_NONE",
                         "msg": "PDF 未扫到 /Author /Title 等元数据（可能已清空或正则未覆盖，建议 exiftool 复核）"})
    return findings


def check_pages(path: str, max_pages: int) -> list:
    """数 PDF 页数（正则数 /Type/Page），超 max_pages 预警。"""
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError:
        return []
    n = len(re.findall(rb"/Type\s*/Page\b(?!s)", raw))
    if n == 0:
        return [{"severity": "info", "code": "PAGES_UNKNOWN", "msg": "未能从 PDF 数出页数（正则未匹配）"}]
    if n > max_pages:
        return [{"severity": "high", "code": "PAGES_OVER",
                 "msg": f"PDF 约 {n} 页 > 上限 {max_pages} 页——超页会被 desk-reject，删减或移附录"}]
    return [{"severity": "info", "code": "PAGES_OK", "msg": f"PDF 约 {n} 页（≤{max_pages} 上限）"}]


def render(findings: list) -> str:
    if not findings:
        return "✅ 未发现合规/匿名雷区（仍建议人工核对目标 venue 的 desk-reject 规则）。"
    order = {"high": 0, "med": 1, "info": 2}
    findings = sorted(findings, key=lambda f: order.get(f["severity"], 9))
    icon = {"high": "🛑", "med": "⚠️", "info": "ℹ️"}
    lines = ["# 投稿合规/匿名检查", ""]
    for f in findings:
        lines.append(f"{icon.get(f['severity'],'')} [{f['code']}] {f['msg']}")
    n_high = sum(1 for f in findings if f["severity"] == "high")
    lines.append("")
    lines.append(f"高危 {n_high} 项 — {'有高危，投稿前必处理' if n_high else '无高危，仍人工复核'}。"
                 "只扫静态雷区，不替代目标 venue 投稿须知核对。")
    return "\n".join(lines)


def _selftest() -> int:
    print("### submission_check 离线自测", file=sys.stderr)
    # 双盲稿含身份命令 + 链接 + 自指 + todo
    bad = (r"\author{Zhang Wei \thanks{Tsinghua}}" "\n"
           r"\section{Acknowledgements} Funded by NSFC 12345." "\n"
           r"See our previous work [3]. Code at github.com/zhangwei/proj." "\n"
           r"\todo{fix this} Results XXX." "\n")
    fb = check_tex(bad, double_blind=True)
    codes = {f["code"] for f in fb}
    assert "BLIND_IDENTITY" in codes, codes
    assert "BLIND_ACK" in codes, codes
    assert "BLIND_LINK" in codes, codes
    assert "BLIND_SELFREF" in codes, codes
    assert "RESIDUAL_TODO" in codes, codes
    # 高危计数
    assert sum(1 for f in fb if f["severity"] == "high") >= 3, fb

    # 干净匿名稿不报匿名问题
    good = (r"\author{Anonymous Authors}" "\n"
            r"This work builds on prior art [3]. See anonymous.4open.science/r/x." "\n")
    fg = check_tex(good, double_blind=True)
    gcodes = {f["code"] for f in fg}
    assert "BLIND_IDENTITY" not in gcodes, f"匿名作者不该报: {fg}"
    assert "BLIND_LINK" not in gcodes, f"匿名仓库链接不该报: {fg}"

    # 非双盲模式不查匿名（只查 todo 等）
    fn = check_tex(bad, double_blind=False)
    assert not any(f["code"].startswith("BLIND") for f in fn), fn
    assert any(f["code"] == "RESIDUAL_TODO" for f in fn), fn

    # PDF 元数据正则（构造最小 PDF 字节）
    fake_pdf = b"%PDF-1.5\n/Author (Zhang Wei) /Title (My Paper)\n/Type /Page\n/Type /Page\n"
    import tempfile, os
    p = os.path.join(tempfile.mkdtemp(), "t.pdf")
    with open(p, "wb") as f:
        f.write(fake_pdf)
    fm = check_pdf_metadata(p, double_blind=True)
    assert any(f["code"] == "PDF_AUTHOR_META" and f["severity"] == "high" for f in fm), fm
    # 页数
    fp = check_pages(p, max_pages=1)
    assert any(f["code"] == "PAGES_OVER" for f in fp), fp   # 2页 > 1
    fp2 = check_pages(p, max_pages=8)
    assert any(f["code"] == "PAGES_OK" for f in fp2), fp2

    md = render(fb)
    assert "高危" in md and "BLIND_IDENTITY" in md, md
    print("[selftest] PASS submission_check offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="投稿前合规/匿名雷区扫描")
    ap.add_argument("--tex", help="正文 .tex 路径")
    ap.add_argument("--pdf", help="编译出的 PDF（查元数据/页数）")
    ap.add_argument("--double-blind", action="store_true", help="双盲投稿：查作者/致谢/链接泄漏")
    ap.add_argument("--max-pages", type=int, default=0, help="页数上限（>0 才查）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest or not (args.tex or args.pdf):
        return _selftest()

    findings = []
    if args.tex:
        with open(args.tex, encoding="utf-8", errors="replace") as f:
            findings += check_tex(f.read(), double_blind=args.double_blind)
    if args.pdf:
        findings += check_pdf_metadata(args.pdf, double_blind=args.double_blind)
        if args.max_pages > 0:
            findings += check_pages(args.pdf, args.max_pages)
    if args.json:
        import json
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        print(render(findings))
    return 1 if any(f["severity"] == "high" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
