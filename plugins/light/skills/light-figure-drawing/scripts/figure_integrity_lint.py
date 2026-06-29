#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""figure_integrity_lint.py — 扫描 matplotlib 绘图代码，提示图表诚实性风险。

最伤公信力的图不是丑，而是误导：偷偷截断的 y 轴、不说类型的误差棒、
制造伪相关的双 y 轴、掩盖分布的 bar plot。审稿人最爱抓这些。本脚本静态
扫描绘图代码（不执行），按 references/figure_integrity.md 的硬规范报风险。

检查项：
  AXIS_TRUNCATE   set_ylim 起点非 0 又没断轴标注 —— 可能偷偷放大差异
  TWIN_AXIS       twinx/twiny 双轴 —— 易制造伪相关，提示考虑拆分 panel
  BAR_NO_ERR      bar/barh 调用但全图无 yerr/errorbar —— 可能掩盖不确定性
  BAR_PLOT_SMALL  bar + 小样本提示 —— 建议散点/箱线展示原始分布
  ERRBAR_NO_TYPE  有误差棒但代码/邻近注释未出现 SD/SEM/CI/置信 字样
  RAINBOW_CMAP    用了 jet/rainbow 等非感知均匀且非色盲安全的 cmap
  PIE_3D          3D 饼图/柱状 —— 透视扭曲比例

诚实原则：静态扫描只能提示"可能误导"，不能断定真误导（如 ylim 非 0 可能
完全合理）。每条都是 warning 级提示，最终判断交作者。不改代码。

用法：
  python figure_integrity_lint.py --file plot.py
  python figure_integrity_lint.py --file plot.py --json
  python figure_integrity_lint.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys

RAINBOW = re.compile(r"cmap\s*=\s*['\"](jet|rainbow|hsv|gist_rainbow|nipy_spectral)['\"]", re.I)
TWIN = re.compile(r"\.(twinx|twiny)\s*\(")
# bar：含 matplotlib .bar/.barh 与 seaborn .barplot/.boxplot/.violinplot（原漏 seaborn）
BAR = re.compile(r"\.(bar|barh|barplot)\s*\(")
DISTRIB_PLOT = re.compile(r"\.(boxplot|violinplot|stripplot|swarmplot)\s*\(")
ERRBAR = re.compile(r"(errorbar|yerr\s*=|xerr\s*=|fill_between|capsize\s*=|ci\s*=|errorbar\s*=)")
# 误差类型声明：SD/SEM/CI/置信 等词，但**排除 .std() 方法调用**（numpy 数据计算 ≠ 误差类型声明）。
# 只认作为"词"出现的类型名，不认 `.std(` / `np.std(` 这种方法调用。
ERRTYPE = re.compile(r"(?<![.\w])(SD|SEM|CI|stderr|confidence|置信|标准差|标准误)(?![\w(])|"
                     r"\bs\.?d\.?\b|95%", re.I)
STD_CALL = re.compile(r"\.std\s*\(|\bnp\.std\b|\bnumpy\.std\b")
# set_ylim：支持位置参数 set_ylim(5, ...) 与关键字 set_ylim(bottom=5)（原漏关键字形式）
SETYLIM = re.compile(r"set_ylim\s*\(\s*(?:bottom\s*=\s*)?([-\d.eE]+)")
YLIM_TUPLE = re.compile(r"ylim\s*=\s*\(\s*([-\d.eE]+)")
BREAK_HINT = re.compile(r"(brokenaxes|break|断轴|broken|d=\s*[\d.]|diagonal)", re.I)
PIE3D = re.compile(r"(Axes3D|projection\s*=\s*['\"]3d['\"]).*(pie|bar)", re.I)
# 小样本：literal n= 或注释/文本里 "n<10"、"每组 N 个" 这类提示
SMALL_N = re.compile(r"\bn\s*=\s*([1-9])\b|每组\s*([1-9])\b|n\s*<\s*10")


def lint_text(text: str) -> list:
    findings = []
    lines = text.splitlines()
    has_errbar = bool(ERRBAR.search(text))
    # 判误差类型声明前，先抹掉 .std()/np.std 方法调用，避免数据计算被误当类型声明（修假阴性）
    text_no_stdcall = STD_CALL.sub(" ", text)
    has_errtype = bool(ERRTYPE.search(text_no_stdcall))
    has_break = bool(BREAK_HINT.search(text))
    has_distrib = bool(DISTRIB_PLOT.search(text))   # 已有箱线/小提琴则不催"用散点展示分布"

    for i, line in enumerate(lines, 1):
        def add(cat, msg):
            findings.append({"line": i, "category": cat, "issue": msg,
                             "context": line.strip()[:90]})

        if RAINBOW.search(line):
            add("RAINBOW_CMAP", "用了 jet/rainbow 类 cmap：非感知均匀且非色盲安全，有序数据改用 viridis")
        if TWIN.search(line):
            add("TWIN_AXIS", "双 y 轴：易因坐标缩放制造伪相关，考虑拆成两个 panel；保留则在 caption 说明")
        if PIE3D.search(line):
            add("PIE_3D", "3D 图：透视会扭曲面积/高度比例，改用 2D")

        m = SETYLIM.search(line) or YLIM_TUPLE.search(line)
        if m:
            try:
                low = float(m.group(1))
                if low != 0 and not has_break:
                    add("AXIS_TRUNCATE", f"y 轴起点={low}（非 0）且未见断轴标注：可能放大组间差异，确需如此请在 caption 说明")
            except ValueError:
                pass

    if BAR.search(text):
        if not has_errbar:
            findings.append({"line": 0, "category": "BAR_NO_ERR",
                             "issue": "出现 bar/barh 但全图未见 yerr/errorbar：柱状图应带误差棒，否则掩盖不确定性",
                             "context": "(whole file)"})
        if SMALL_N.search(text) and not has_distrib:
            findings.append({"line": 0, "category": "BAR_PLOT_SMALL",
                             "issue": "bar + 小样本(n<10?)：建议散点/箱线展示原始分布，别用 bar 掩盖分布",
                             "context": "(whole file)"})

    if has_errbar and not has_errtype:
        findings.append({"line": 0, "category": "ERRBAR_NO_TYPE",
                         "issue": "有误差棒/误差带但代码与注释未出现 SD/SEM/CI：caption 必须注明误差类型与 n=",
                         "context": "(whole file)"})
    return findings


def selftest() -> int:
    bad = """
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.bar([1,2,3], [10,11,12])      # n=3 per group
ax.set_ylim(9, 13)               # 偷偷截断放大差异
ax2 = ax.twinx()
im = ax.imshow(data, cmap='jet')
"""
    good = """
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
# error bars = SEM, n=200 per group
ax.errorbar(x, y, yerr=sem, capsize=3, fmt='o')
ax.set_ylim(0, 13)
ax.imshow(data, cmap='viridis')
"""
    fb = lint_text(bad)
    fg = lint_text(good)
    cats_bad = {f["category"] for f in fb}
    print("[bad 样例] 命中:", sorted(cats_bad))
    for f in fb:
        print(f"   L{f['line']:>3} {f['category']}: {f['issue'][:50]}")
    print("[good 样例] 命中:", sorted({f['category'] for f in fg}) or "无（干净）")
    # 期望:bad 至少抓到截断/双轴/rainbow/bar无误差;good 应基本干净
    want = {"AXIS_TRUNCATE", "TWIN_AXIS", "RAINBOW_CMAP", "BAR_NO_ERR"}
    ok = want.issubset(cats_bad) and len(fg) == 0

    # FD-1 假阴性回归：以下原来漏报，现在应抓到
    # 1) sns.barplot 无误差棒（原 BAR 正则漏 seaborn）
    sns_bar = "import seaborn as sns\nsns.barplot(x='m', y='acc', data=df)\n"
    assert any(f["category"] == "BAR_NO_ERR" for f in lint_text(sns_bar)), "sns.barplot 应被检出 BAR_NO_ERR"
    # 2) .std() 数据计算不应压掉 ERRBAR_NO_TYPE（原 \bstd\b 误判）
    std_calc = ("ax.errorbar(x, y, yerr=resid.std(), fmt='o')\n"  # 用 .std() 算但没声明误差类型
                "ax.set_title('results')\n")                       # 注释/代码均无类型词
    assert any(f["category"] == "ERRBAR_NO_TYPE" for f in lint_text(std_calc)), \
        ".std() 不该被当成误差类型声明"
    # 3) 真声明 SEM 时不报 ERRBAR_NO_TYPE
    with_sem = "# error bars are SEM, n=200\nax.errorbar(x, y, yerr=sem)\n"
    assert not any(f["category"] == "ERRBAR_NO_TYPE" for f in lint_text(with_sem)), "声明 SEM 不应报"
    # 4) set_ylim(bottom=5) 关键字形式（原正则漏）
    kw_ylim = "ax.set_ylim(bottom=5)\nax.bar([1],[2])\n"
    assert any(f["category"] == "AXIS_TRUNCATE" for f in lint_text(kw_ylim)), "set_ylim(bottom=) 应被检出"
    print("[FD-1 假阴性回归] sns.barplot / .std()不压制 / SEM豁免 / set_ylim(bottom=) 全 OK")

    print("[selftest]", "OK" if ok else f"FAIL (bad缺{want-cats_bad}, good误报{len(fg)})")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="图表诚实性 lint")
    ap.add_argument("--file", help="绘图代码文件(.py)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.file:
        ap.error("需要 --file 或 --selftest")
        return 2

    with open(args.file, encoding="utf-8") as f:
        findings = lint_text(f.read())
    if args.json:
        print(json.dumps({"file": args.file, "n": len(findings), "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        if not findings:
            print(f"{args.file}: 未发现诚实性风险点")
        for f in findings:
            loc = f"L{f['line']}" if f["line"] else "全文"
            print(f"  [{f['category']}] {loc}: {f['issue']}")
    # 有风险点返回非零，便于当 pipeline 提示（但诚实性多为 warning，调用方可选择不阻断）
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
