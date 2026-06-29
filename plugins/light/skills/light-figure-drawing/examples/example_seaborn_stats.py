#!/usr/bin/env python3
"""example_seaborn_stats.py — seaborn 统计对比组图 (分布 + 分类 + 显著性)

演示:
  - sns.set_theme(context="paper", style="ticks") + Okabe-Ito 调色板
  - 箱线 + 抖动散点 (overlay) 做组间分布对比
  - 小提琴图看分布形状
  - 误差棒条形 (pointplot/barplot) + 显著性星标
  - sns.despine() 去 chart junk; 物理尺寸按双栏

合成数据自带; matplotlib Agg; 直接 python 运行产 png/pdf。
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import figure_export as fx          # noqa: E402
import color_palettes as cp         # noqa: E402


def make_data(rng):
    groups, vals, cond = [], [], []
    base = {"A": 5.0, "B": 6.5, "C": 5.2}
    for g, mu in base.items():
        for c, shift in [("pre", 0.0), ("post", 1.3)]:
            n = 40
            v = rng.normal(mu + shift, 1.0, n)
            groups += [g] * n
            cond += [c] * n
            vals += list(v)
    return pd.DataFrame({"group": groups, "condition": cond, "value": vals})


def sig_bar(ax, x1, x2, y, text):
    h = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.025
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=0.8, c="black")
    ax.text((x1 + x2) / 2, y + h, text, ha="center", va="bottom", fontsize=8)


def main():
    sns.set_theme(context="paper", style="ticks",
                  rc={"font.family": "sans-serif"})
    pal = cp.OKABE_ITO_LIST[1:4]
    rng = np.random.default_rng(3)
    df = make_data(rng)

    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6))

    # (a) 箱线 + 抖动散点
    ax = axes[0]
    sns.boxplot(data=df, x="group", y="value", hue="group", palette=pal,
                width=0.6, fliersize=0, ax=ax, legend=False)
    sns.stripplot(data=df, x="group", y="value", color="0.25", size=2,
                  alpha=0.4, jitter=0.18, ax=ax)
    ax.set_title("a", loc="left", fontweight="bold")
    ax.set_xlabel("")

    # (b) 小提琴
    ax = axes[1]
    sns.violinplot(data=df, x="group", y="value", hue="group", palette=pal,
                   inner="quartile", ax=ax, legend=False)
    ax.set_title("b", loc="left", fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("")

    # (c) 条形 + 误差棒 + 显著性 (pre vs post)
    ax = axes[2]
    sns.barplot(data=df, x="group", y="value", hue="condition",
                palette=[cp.OKABE_ITO["sky_blue"], cp.OKABE_ITO["vermillion"]],
                errorbar="se", capsize=0.1, err_kws={"linewidth": 0.8}, ax=ax)
    ax.set_title("c", loc="left", fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_ylim(0, ax.get_ylim()[1] * 1.15)
    sig_bar(ax, -0.2, 0.2, df["value"].max() * 0.95, "*")
    ax.legend(title="", fontsize=6, loc="upper left")

    sns.despine(fig)
    fig.tight_layout()

    out = os.path.join(HERE, "out_seaborn_stats")
    written, info = fx.save_for_journal(fig, out, journal="nature",
                                        column="double", height_mm=70,
                                        formats=("pdf", "png"))
    rep = fx.check_figure_size(fig, journal="nature", column="double")
    print("[example] 导出:", [os.path.basename(p) for p in written])
    print("[example] 校验:", "OK" if rep["ok"] else f"FAIL {rep['problems']}")
    plt.close(fig)


if __name__ == "__main__":
    main()