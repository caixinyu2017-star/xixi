#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""citekey_audit.py — \\cite 键 ↔ .bib 键双向对账（补 workflow 第 8 步说了却无脚本的缺口）。

把正文里 \\cite{key} 引用的键 与 .bib 文件定义的键 求双向差集：
  - 缺失键（cited but undefined）：正文引了但 .bib 没有 → 编译会出 ??，必修
  - 冗余键（defined but uncited）：.bib 有但正文没引 → 投稿前清理（审稿人嫌库脏）
另可选按 authorYearWord 惯例校验 citekey 命名（与 m07/m08 占位公式同源）。

纯标准库零依赖、离线、只读不改。支持 LaTeX(\\cite/\\citep/\\citet/\\parencite 等) 与
Markdown/pandoc([@key]) 两种引用语法。

用法：
  python citekey_audit.py --tex paper.tex --bib refs.bib
  python citekey_audit.py --tex paper.md --bib refs.bib --check-naming
  python citekey_audit.py --selftest
"""
from __future__ import annotations
import argparse
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# LaTeX 各种 cite 命令：\cite \citep \citet \citeauthor \parencite \textcite \autocite \footcite ...
_LATEX_CITE = re.compile(r"\\(?:cite|citep|citet|citealt|citealp|citeauthor|citeyear|"
                         r"parencite|textcite|autocite|footcite|smartcite|supercite)\*?"
                         r"(?:\[[^\]]*\])*\{([^}]*)\}")
# Markdown/pandoc 引用：[@key], [@key1; @key2], @key
_MD_CITE = re.compile(r"@([A-Za-z][\w:.\-]+)")
# .bib 条目定义：@article{key, / @inproceedings{key,
_BIB_ENTRY = re.compile(r"@\s*\w+\s*\{\s*([^,\s}]+)\s*,")
# authorYearWord 惯例：小写姓+4位年+可选小写词（如 vaswani2017attention）
_NAMING_RE = re.compile(r"^[a-z]+\d{4}[a-z]*$")


def extract_cited_keys(text: str) -> set:
    """从正文抽所有被引 citekey（LaTeX + Markdown 两种语法），多键 {a,b} 拆开。"""
    keys = set()
    for m in _LATEX_CITE.finditer(text):
        for k in m.group(1).split(","):
            k = k.strip()
            if k:
                keys.add(k)
    # Markdown：仅当看起来是 pandoc 引用上下文（@key），排除 email 等用 [@ 锚定
    for m in re.finditer(r"\[\s*@[^\]]+\]", text):
        for mk in _MD_CITE.finditer(m.group(0)):
            keys.add(mk.group(1))
    return keys


def extract_bib_keys(text: str) -> list:
    """从 .bib 抽所有定义的 citekey（保序，便于查重复定义）。"""
    return [m.group(1).strip() for m in _BIB_ENTRY.finditer(text)]


def audit(tex_text: str, bib_text: str, check_naming: bool = False) -> dict:
    cited = extract_cited_keys(tex_text)
    bib_list = extract_bib_keys(bib_text)
    bib = set(bib_list)
    missing = sorted(cited - bib)        # 引了但未定义 → 编译 ??
    uncited = sorted(bib - cited)        # 定义了但没引 → 清理
    # .bib 内重复定义键
    seen, dup = set(), []
    for k in bib_list:
        if k in seen and k not in dup:
            dup.append(k)
        seen.add(k)
    naming_bad = []
    if check_naming:
        naming_bad = sorted(k for k in bib if not _NAMING_RE.match(k))
    return {
        "n_cited": len(cited), "n_bib": len(bib),
        "missing_keys": missing,           # 必修
        "uncited_keys": uncited,           # 建议清理
        "duplicate_bib_keys": dup,         # .bib 重复定义
        "naming_violations": naming_bad,   # 非 authorYearWord（仅 --check-naming）
        "ok": not missing and not dup,     # 缺失/重复才算硬错；冗余只警告
    }


def render(rep: dict) -> str:
    L = [f"# citekey 对账：正文引用 {rep['n_cited']} 个 / .bib 定义 {rep['n_bib']} 个", ""]
    if rep["missing_keys"]:
        L.append(f"## 🛑 缺失键 {len(rep['missing_keys'])}（正文引了但 .bib 没有，编译出 ??，必修）")
        L += [f"- `{k}`" for k in rep["missing_keys"]]
    if rep["duplicate_bib_keys"]:
        L.append(f"## 🛑 .bib 重复定义 {len(rep['duplicate_bib_keys'])}（必修）")
        L += [f"- `{k}`" for k in rep["duplicate_bib_keys"]]
    if rep["uncited_keys"]:
        L.append(f"## ⚠ 冗余键 {len(rep['uncited_keys'])}（.bib 有但正文没引，投稿前清理）")
        L += [f"- `{k}`" for k in rep["uncited_keys"][:50]]
    if rep["naming_violations"]:
        L.append(f"## ⚠ 命名不合 authorYearWord {len(rep['naming_violations'])}（可选规范）")
        L += [f"- `{k}`" for k in rep["naming_violations"][:50]]
    if rep["ok"] and not rep["uncited_keys"]:
        L.append("✅ 引用与 .bib 完全对齐，无缺失/重复/冗余。")
    elif rep["ok"]:
        L.append("✅ 无缺失/重复（硬错）；仅有冗余键待清理。")
    return "\n".join(L)


def _selftest() -> int:
    print("### citekey_audit 离线自测", file=sys.stderr)
    tex = (r"As shown by \citep{vaswani2017attention} and \citet{he2016deep}, "
           r"the method works \cite{vaswani2017attention,missing2099key}.")
    bib = ("@inproceedings{vaswani2017attention, title={Attention}}\n"
           "@article{he2016deep, title={ResNet}}\n"
           "@article{unused2020paper, title={Never cited}}\n")
    rep = audit(tex, bib)
    assert rep["n_cited"] == 3, rep            # vaswani, he, missing2099key
    assert rep["missing_keys"] == ["missing2099key"], rep
    assert rep["uncited_keys"] == ["unused2020paper"], rep
    assert not rep["ok"] is False or rep["missing_keys"]  # 有缺失 → ok=False
    assert rep["ok"] is False, rep

    # Markdown/pandoc 语法
    md = "See [@vaswani2017attention] and [@he2016deep; @unused2020paper]."
    rep_md = audit(md, bib)
    assert rep_md["missing_keys"] == [] and rep_md["uncited_keys"] == [], rep_md
    assert rep_md["ok"], rep_md

    # .bib 重复定义检测
    dupbib = bib + "@misc{he2016deep, title={dup}}\n"
    rep_d = audit(tex, dupbib)
    assert "he2016deep" in rep_d["duplicate_bib_keys"], rep_d

    # 命名校验
    badname = "@article{BadKey_2020, title={x}}\n@article{good2020word, title={y}}"
    rep_n = audit("\\cite{good2020word}", badname, check_naming=True)
    assert "BadKey_2020" in rep_n["naming_violations"], rep_n
    assert "good2020word" not in rep_n["naming_violations"], rep_n

    # 完全对齐
    rep_ok = audit("\\cite{he2016deep}", "@article{he2016deep,title={x}}")
    assert rep_ok["ok"] and not rep_ok["uncited_keys"], rep_ok
    md_render = render(rep)
    assert "缺失键" in md_render and "missing2099key" in md_render, md_render
    print("[selftest] PASS citekey_audit offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="\\cite 键 ↔ .bib 键双向对账")
    ap.add_argument("--tex", help="正文 .tex / .md 路径")
    ap.add_argument("--bib", help=".bib 路径")
    ap.add_argument("--check-naming", action="store_true", help="校验 citekey 是否合 authorYearWord 惯例")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest or not (args.tex and args.bib):
        return _selftest()
    with open(args.tex, encoding="utf-8") as f:
        tex_text = f.read()
    with open(args.bib, encoding="utf-8") as f:
        bib_text = f.read()
    rep = audit(tex_text, bib_text, check_naming=args.check_naming)
    if args.json:
        import json
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(render(rep))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
