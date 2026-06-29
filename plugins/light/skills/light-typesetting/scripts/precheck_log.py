#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""precheck_log.py — 扫描 LaTeX .log，汇总编译问题报告（纯标准库，无外部依赖）。

抓取：
  - Undefined references / citations（未定义引用、未定义文献）
  - Multiply defined labels（重复标签）
  - Overfull / Underfull \\hbox & \\vbox（盒子溢出）
  - Missing figure / file not found（图片/文件找不到）
  - Undefined control sequence（未定义命令，常因缺宏包）
  - Missing $ inserted / runaway argument 等致命错误（LaTeX Error / ! 行）
  - Font / package warnings 汇总计数

用法：
  python precheck_log.py path/to/file.log [--json] [--max N]
  无参数运行 → 跑内置样例 log 自测。

退出码：0=无致命错误；1=存在 LaTeX Error / undefined control sequence 等致命项。
"""
from __future__ import annotations
import sys
import re
import json
import argparse
from collections import Counter

# --- 正则规则表：(键, 严重度, 编译后的正则, 说明) ---------------------------
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}

RULES = [
    ("latex_error", "error",
     re.compile(r"^! LaTeX Error: (.+)$", re.M),
     "LaTeX 致命错误"),
    ("tex_error", "error",
     re.compile(r"^! (Undefined control sequence|Missing \$ inserted|"
                r"Missing \} inserted|Runaway argument|Emergency stop|"
                r"Paragraph ended before|Too many \}|Extra \}|"
                r"Double superscript|Misplaced alignment)\.?", re.M),
     "TeX 引擎致命错误"),
    ("undef_ref", "warning",
     re.compile(r"(?:Reference|LaTeX Warning: Reference) [`'\"]([^'\"]+)['\"] "
                r"on page \d+ undefined", re.M),
     "未定义的交叉引用 \\ref/\\label"),
    ("undef_cite", "warning",
     re.compile(r"(?:Citation|LaTeX Warning: Citation) [`'\"]([^'\"]+)['\"] "
                r"on page \d+ undefined", re.M),
     "未定义的文献引用 \\cite（多半要跑 bibtex/biber）"),
    ("multiply_label", "warning",
     re.compile(r"LaTeX Warning: Label [`'\"]([^'\"]+)['\"] multiply defined", re.M),
     "标签重复定义"),
    ("overfull_hbox", "warning",
     re.compile(r"^Overfull \\hbox \(([\d.]+)pt too wide\)(.*)$", re.M),
     "Overfull \\hbox（行内容过宽，可能溢出页边）"),
    ("underfull_hbox", "info",
     re.compile(r"^Underfull \\hbox \(badness (\d+)\)(.*)$", re.M),
     "Underfull \\hbox（行内容过稀）"),
    ("overfull_vbox", "warning",
     re.compile(r"^Overfull \\vbox \(([\d.]+)pt too high\)(.*)$", re.M),
     "Overfull \\vbox（竖向溢出）"),
    ("missing_file", "error",
     re.compile(r"(?:! LaTeX Error: File [`'\"]([^'\"]+)['\"] not found|"
                r"^! Unable to load picture or PDF file [`'\"]?([^'\".]+\.\w+)['\"]?)", re.M),
     "找不到文件/图片"),
    ("missing_graphic", "error",
     re.compile(r"LaTeX Warning: File [`'\"]([^'\"]+)['\"] not found", re.M),
     "graphicx 找不到图片文件"),
    ("rerun", "info",
     re.compile(r"(Rerun to get cross-references right|"
                r"Label\(s\) may have changed)", re.M),
     "需要再次编译以收敛交叉引用/目录"),
    ("font_warning", "info",
     re.compile(r"^LaTeX Font Warning: (.+)$", re.M),
     "字体警告"),
    ("pkg_warning", "info",
     re.compile(r"^Package (\w+) Warning: (.+)$", re.M),
     "宏包警告"),
]


def _dewrap(text: str) -> str:
    """LaTeX log 把行硬折在 ~79 字符（max_print_line），长引用名/文件名被折断 → 正则漏报。
    启发式拼回：一行恰好 79/80 字符且下一行非空、不以已知行首标记开头，视为被折断，拼接。
    保守：只拼"看起来被机械折断"的行，不动正常段落。"""
    lines = text.split("\n")
    out, i = [], 0
    # 这些行首是 log 里独立条目的开头，遇到它们不该把上一行往后拼
    starts = ("!", "Overfull", "Underfull", "Package", "LaTeX", "Missing",
              "Document", "This is", "(", ")", "[", "<", "Output", "Rerun")
    while i < len(lines):
        cur = lines[i]
        # 79/80 列硬折：当前行长度达阈值且下一行存在、非空、不是新条目开头 → 拼接
        while (len(cur) in (79, 80) and i + 1 < len(lines)
               and lines[i + 1].strip()
               and not lines[i + 1].lstrip().startswith(starts)):
            i += 1
            cur = cur + lines[i]
        out.append(cur)
        i += 1
    return "\n".join(out)


def scan(text: str, strict: bool = False) -> dict:
    """扫描 log 文本，返回结构化结果。先 de-wrap 拼回硬折行再匹配（消除长名漏报）。
    strict=True 时把 undefined ref/cite/multiply_label 提升为 error（交付门要拦）。"""
    text = _dewrap(text)
    findings = {}
    strict_promote = {"undef_ref", "undef_cite", "multiply_label"}
    for key, sev, rx, desc in RULES:
        hits = []
        for m in rx.finditer(text):
            groups = [g for g in m.groups() if g]
            detail = " | ".join(groups) if groups else m.group(0).strip()
            hits.append(detail.strip())
        if hits:
            eff_sev = "error" if (strict and key in strict_promote) else sev
            findings[key] = {"severity": eff_sev, "desc": desc,
                             "count": len(hits), "items": hits,
                             "promoted_by_strict": strict and key in strict_promote}
    return findings


def summarize(findings: dict, max_items: int = 8) -> str:
    """生成人类可读报告。"""
    if not findings:
        return "OK: 未发现 undefined refs / overfull hbox / missing figure 等问题。"
    lines = []
    sev_counts = Counter()
    for f in findings.values():
        sev_counts[f["severity"]] += f["count"]
    head = (f"发现问题：errors={sev_counts['error']} "
            f"warnings={sev_counts['warning']} infos={sev_counts['info']}")
    lines.append(head)
    lines.append("=" * len(head))
    # 按严重度排序输出
    for key in sorted(findings,
                      key=lambda k: SEVERITY_ORDER[findings[k]["severity"]]):
        f = findings[key]
        tag = {"error": "[ERR ]", "warning": "[WARN]", "info": "[INFO]"}[f["severity"]]
        lines.append(f"\n{tag} {key} ×{f['count']} — {f['desc']}")
        for item in f["items"][:max_items]:
            lines.append(f"    - {item}")
        if f["count"] > max_items:
            lines.append(f"    ... 其余 {f['count'] - max_items} 条省略")
    return "\n".join(lines)


def has_fatal(findings: dict) -> bool:
    return any(f["severity"] == "error" for f in findings.values())


SAMPLE_LOG = r"""
This is pdfTeX, Version 3.141592653-2.6-1.40.25 (TeX Live 2023)
(./paper.tex
LaTeX2e <2023-11-01>
(./IEEEtran.cls
Document Class: IEEEtran 2015/08/26 V1.8b)
! Undefined control sequence.
l.42 \includegrpahics
                     [width=\linewidth]{fig1.png}
! LaTeX Error: File `fig1.png' not found.
See the LaTeX manual or LaTeX Companion for explanation.
LaTeX Warning: File `results/plot.pdf' not found on input line 88.
Overfull \hbox (15.2pt too wide) in paragraph at lines 120--122
[]\OT1/cmr/m/n/10 This is a very long line that does not fit nicely
Underfull \hbox (badness 1300) in paragraph at lines 130--131
LaTeX Warning: Reference `fig:arch' on page 3 undefined on input line 145.
LaTeX Warning: Citation `smith2020' on page 4 undefined on input line 200.
LaTeX Warning: Citation `doe2019' on page 4 undefined on input line 201.
LaTeX Warning: Label `sec:intro' multiply defined.
LaTeX Font Warning: Font shape `OT1/cmr/bx/sc' undefined.
Package hyperref Warning: Token not allowed in a PDF string.
LaTeX Warning: There were undefined references.
LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.
)
"""



def _selftest() -> int:
    findings = scan(SAMPLE_LOG)
    assert has_fatal(findings), findings
    for key in ("latex_error", "tex_error", "missing_graphic", "undef_ref", "undef_cite", "multiply_label", "overfull_hbox"):
        assert key in findings, (key, findings)
    report = summarize(findings, max_items=3)
    assert "errors=" in report and "warnings=" in report, report
    clean = scan("This is a clean LaTeX log.\nOutput written on paper.pdf")
    assert not has_fatal(clean) and summarize(clean).startswith("OK:"), clean

    # TS-2 strict 模式：undefined ref/cite 在普通模式是 warning，strict 下提升为 error → fatal
    warn_log = "LaTeX Warning: Reference `fig:x' on page 1 undefined on input line 5."
    f_normal = scan(warn_log, strict=False)
    f_strict = scan(warn_log, strict=True)
    assert not has_fatal(f_normal), "普通模式 undef_ref 不该 fatal"
    assert has_fatal(f_strict), "strict 模式 undef_ref 应 fatal"
    assert f_strict["undef_ref"]["promoted_by_strict"], f_strict

    # TS-2 de-wrap：被 79 列硬折断的长引用名拼回后仍能匹配（消除漏报）
    long_ref = "x" * 40
    wrapped = ("LaTeX Warning: Citation `" + long_ref[:30] + "\n"
               + long_ref[30:] + "' on page 2 undefined on input line 9.")
    # 折断处构造成 79 列触发 de-wrap
    line1 = "LaTeX Warning: Citation `verylongcitationkey2024deeplearningmethodfoo"
    line1 = line1 + "x" * (79 - len(line1))   # 垫到 79 列
    wrapped2 = line1 + "\n" + "bar' on page 2 undefined on input line 9."
    f_wrap = scan(wrapped2, strict=True)
    assert "undef_cite" in f_wrap, f"de-wrap 后应匹配到被折断的 undefined citation: {f_wrap}"
    print("[selftest] PASS precheck_log (+strict +de-wrap)")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="扫描 LaTeX .log 汇总编译问题")
    p.add_argument("logfile", nargs="?", help="LaTeX .log 路径；省略则跑内置自测")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    p.add_argument("--max", type=int, default=8, help="每类最多展示条数")
    p.add_argument("--selftest", action="store_true", help="run built-in log parser self-test")
    p.add_argument("--strict", action="store_true",
                   help="把 undefined ref/cite/multiply label 提升为 error（交付门拦截，退出码非0）")
    args = p.parse_args(argv)

    if args.selftest:
        return _selftest()

    if args.logfile:
        with open(args.logfile, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        src = args.logfile
    else:
        text = SAMPLE_LOG
        src = "<内置样例 log（自测）>"

    findings = scan(text, strict=args.strict)
    if args.json:
        print(json.dumps({"source": src, "strict": args.strict, "fatal": has_fatal(findings),
                          "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print(f"# precheck_log 报告 — 来源: {src}" + ("  [strict]" if args.strict else "") + "\n")
        print(summarize(findings, args.max))
    return 1 if has_fatal(findings) else 0


if __name__ == "__main__":
    sys.exit(main())
