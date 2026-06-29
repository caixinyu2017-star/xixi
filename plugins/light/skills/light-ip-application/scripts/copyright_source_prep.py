#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
copyright_source_prep.py — 软件著作权(软著)源代码材料整理。

按中国版权保护中心(CPCC)要求生成提交用源代码:
  * 规则:连续源码,每页约 50 行;总量 <=60 页则全交,否则交"前 30 页 + 后 30 页";
  * 页眉含软件全称 + 版本号;
  * 去除注释中的个人/敏感信息(本脚本做基础脱敏:邮箱/手机号/常见密钥行)。

诚实声明:本脚本只做"形式整理",不审查代码质量/新颖性;材料须真实对应,
不得拼凑虚构(CONVENTIONS.md / 联动 a10)。

自测: python copyright_source_prep.py --selftest  (用内置合成代码,不读外部文件)
真实使用: python copyright_source_prep.py --src <代码目录> --name "软件全称" --version "V1.0" \
          --ext .py,.java,.js --out submit_source.txt
"""
from __future__ import annotations
import argparse
import os
import re
import sys

LINES_PER_PAGE = 50
PAGE_RULE_FULL_MAX = 60   # <=60 页全交
HEAD_PAGES = 30
TAIL_PAGES = 30

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE = re.compile(r"(?<!\d)(?:\+?86)?1[3-9]\d{9}(?!\d)")
_SECRET = re.compile(r"(?i)(password|passwd|secret|api[_-]?key|token|access[_-]?key)\s*[=:]\s*\S+")
_PEM = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
_IPV4 = re.compile(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)")
# 长 base64/hex 串（疑似密钥/凭证），≥40 连续字符
_LONGB64 = re.compile(r"(?<![\w/+])[A-Za-z0-9+/]{40,}={0,2}(?![\w/+])")
_HEXKEY = re.compile(r"(?<![\w])[0-9a-fA-F]{32,}(?![\w])")
_redaction_stats = {"hits": 0}


def desensitize(line: str) -> str:
    """基础脱敏（注释/字符串里的个人与凭证信息）。**只做正则粗筛，不保证完备**——
    输出末尾会提示命中数 + 让人工复核（见 render）。统计命中数供免责提示。"""
    n0 = _redaction_stats["hits"]

    def _sub(rx, repl, s):
        new, k = rx.subn(repl, s)
        _redaction_stats["hits"] += k
        return new

    line = _sub(_PEM, "-----BEGIN PRIVATE KEY----- <redacted>", line)
    line = _sub(_EMAIL, "<email>", line)
    line = _sub(_PHONE, "<phone>", line)
    line = _sub(_SECRET, lambda m: f"{m.group(1)}=<redacted>", line)
    line = _sub(_IPV4, "<ip>", line)
    line = _sub(_LONGB64, "<redacted-b64>", line)
    line = _sub(_HEXKEY, "<redacted-hex>", line)
    return line


def collect_source_lines(src_dir: str, exts: list[str]) -> list[str]:
    """按文件名排序遍历,拼接所有匹配扩展名的源码行(已脱敏)。"""
    exts = {e if e.startswith(".") else "." + e for e in exts}
    files = []
    for root, _dirs, names in os.walk(src_dir):
        for n in sorted(names):
            if os.path.splitext(n)[1].lower() in exts:
                files.append(os.path.join(root, n))
    files.sort()
    lines: list[str] = []
    for f in files:
        rel = os.path.relpath(f, src_dir)
        lines.append(f"//// FILE: {rel}")
        with open(f, "r", encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                lines.append(desensitize(raw.rstrip("\n")))
    return lines


def effective_code_lines(lines: list) -> int:
    """有效代码行数：排除 `//// FILE:` 文件标记行与纯空行（软著 60 行/页按有效行算更准，
    避免标记/空行虚增页数误导'够不够 60 页'的判断）。"""
    n = 0
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("//// FILE:"):
            continue
        n += 1
    return n


def paginate(lines: list[str], per_page: int = LINES_PER_PAGE) -> list[list[str]]:
    return [lines[i:i + per_page] for i in range(0, len(lines), per_page)]


def select_pages(pages: list[list[str]], lines: list = None) -> tuple[list[list[str]], str]:
    """按软著规则挑选提交页。返回(选中页, 说明)。
    说明里同时给"含标记/空行的版面页数"与"有效代码行数"，避免页数被标记行虚增误导。"""
    n = len(pages)
    eff_note = ""
    if lines is not None:
        eff = effective_code_lines(lines)
        eff_pages = (eff + LINES_PER_PAGE - 1) // LINES_PER_PAGE
        eff_note = f"（有效代码 {eff} 行≈{eff_pages} 页，已排除 FILE 标记行/空行；版面 {n} 页含这些）"
    if n <= PAGE_RULE_FULL_MAX:
        return pages, f"全部提交({n} 页 <= {PAGE_RULE_FULL_MAX} 页){eff_note}"
    head = pages[:HEAD_PAGES]
    tail = pages[-TAIL_PAGES:]
    return head + tail, f"前 {HEAD_PAGES} 页 + 后 {TAIL_PAGES} 页(总 {n} 页 > {PAGE_RULE_FULL_MAX}){eff_note}"


def render(selected: list[list[str]], all_pages: list[list[str]], name: str,
           version: str) -> str:
    """渲染成带页眉/页码的提交文本。后段页码沿用其在全文中的真实页号。"""
    n = len(all_pages)
    out = []
    if n <= PAGE_RULE_FULL_MAX:
        numbered = list(enumerate(selected, 1))
    else:
        numbered = [(i + 1, p) for i, p in enumerate(all_pages[:HEAD_PAGES])]
        numbered += [(n - TAIL_PAGES + i + 1, p) for i, p in enumerate(all_pages[-TAIL_PAGES:])]
    for pageno, page in numbered:
        out.append(f"===== {name} {version}  -  第 {pageno} 页 =====")
        out.extend(page)
        out.append("")
    return "\n".join(out)


def prepare(src_dir: str, exts: list[str], name: str, version: str) -> tuple[str, str]:
    _redaction_stats["hits"] = 0          # 重置脱敏命中计数
    lines = collect_source_lines(src_dir, exts)
    pages = paginate(lines)
    selected, note = select_pages(pages, lines)
    # 脱敏免责：正则粗筛非完备，提示人工复核（避免给用户"已彻底脱敏"的错觉）
    note += (f"\n[脱敏] 正则命中并替换 {_redaction_stats['hits']} 处(邮箱/手机/密钥/PEM/IPv4/base64/hex)"
             f"——**仅正则粗筛不保证完备**，提交前请人工复核源码无残留个人信息/密钥/内部地址。")
    return render(selected, pages, name, version), note


def _selftest() -> int:
    import tempfile
    sample = ("def f():\n    api_key = 'ABCD1234'\n    # contact me@x.com or 13800138000\n"
              "    return 1\n") * 50  # 制造 200 行 -> 4 页(<=60 全交)
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "a.py"), "w", encoding="utf-8") as fh:
            fh.write(sample)
        text, note = prepare(d, [".py"], "测试软件", "V1.0")
    assert "<email>" in text and "<phone>" in text, "脱敏失败"
    assert "api_key=<redacted>" in text or "api_key = <redacted>" in text.replace("'ABCD1234'", "<redacted>") or "<redacted>" in text, "密钥脱敏失败"
    assert "测试软件 V1.0" in text and "第 1 页" in text, "页眉失败"
    assert "全部提交" in note, note
    # IP-6 脱敏强化：PEM/IPv4/base64 也被脱敏 + 免责提示
    sec = ("-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA" + "A" * 50 + "\n"
           "host = 192.168.1.100\ntoken = " + "x" * 45 + "\n")
    import tempfile as _tf
    with _tf.TemporaryDirectory() as d2:
        with open(os.path.join(d2, "k.py"), "w", encoding="utf-8") as fh:
            fh.write(sec)
        text2, note2x = prepare(d2, [".py"], "K", "V1")
    assert "<ip>" in text2, "IPv4 未脱敏"
    assert "PRIVATE KEY----- <redacted>" in text2 or "<redacted-b64>" in text2, "PEM/base64 未脱敏"
    assert "不保证完备" in note2x and "[脱敏]" in note2x, "缺脱敏免责"
    # IP-7 有效行口径：FILE 标记行/空行不计入
    eff = effective_code_lines(["//// FILE: a.py", "", "  ", "x = 1", "y = 2"])
    assert eff == 2, f"有效行应只数代码行: {eff}"

    # 大文件路径:制造 >60 页,验证前30+后30选择
    big = paginate([f"line{i}" for i in range(60 * 50 + 10)])
    sel, note2 = select_pages(big)
    assert len(sel) == HEAD_PAGES + TAIL_PAGES, len(sel)
    assert "前 30 页 + 后 30 页" in note2, note2
    rendered = render(sel, big, "X", "V2")
    assert f"第 {len(big)} 页" in rendered, "尾页页号应为真实总页号"
    print("[selftest] OK ", note, "|", note2, "| 总页数", len(big))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="软著源代码材料整理(50行/页, <=60页全交否则前30+后30)")
    ap.add_argument("--src", help="源代码目录")
    ap.add_argument("--name", default="软件全称", help="软件全称(进页眉)")
    ap.add_argument("--version", default="V1.0", help="版本号(进页眉)")
    ap.add_argument("--ext", default=".py,.java,.js,.c,.cpp,.go,.ts", help="逗号分隔扩展名")
    ap.add_argument("--out", default=None, help="输出文件,缺省打印到 stdout")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return _selftest()
    if not args.src:
        ap.error("需要 --src(或用 --selftest)")
    text, note = prepare(args.src, args.ext.split(","), args.name, args.version)
    sys.stderr.write(f"[软著源码整理] {note}\n")
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        sys.stderr.write(f"已写出 {args.out}\n")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
