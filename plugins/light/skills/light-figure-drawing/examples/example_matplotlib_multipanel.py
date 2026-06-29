#!/usr/bin/env python3
"""example_matplotlib_multipanel.py — GridSpec 多面板 + 子图标号 + 误差棒 + 显著性星标

演示 light-figure-drawing 的组图标准做法:
  - GridSpec 不规则布局 (顶部跨列 + 下方两格)
  - (a)(b)(c) 子图标号 (统一样式)
  - 误差棒 + 显著性星标 (annotate 横杠 + 星号)
  - 套用 assets/publication.mplstyle + Okabe-Ito 配色
  - 用 figure_export.save_for_journal 按 Nature 双栏导出并校验

合成数据自带; matplotlib Agg; 直接 python 运行产 png/pdf。
默认输出到临时目录（不污染仓库 examples/）；如需留存到指定目录，传 `--outdir <dir>`。
"""
import os
import sys
import tempfile
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import figure_export as fx          # noqa: E402
import color_palettes as cp         # noqa: E402


def panel_tag(ax, tag, dx=-0.12, dy=1.02):
    """统一的 (a)(b)(c) 标号: 左上角, 粗体。"""
    ax.text(dx, dy, tag, transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="bottom", ha="right")


def sig_bar(ax, x1, x2, y, text, h=None):
    """显著性横杠 + 星标。"""
    if h is None:
        h = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.03
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=0.8, c="black")
    ax.text((x1 + x2) / 2, y + h, text, ha="center", va="bottom", fontsize=8)


def main(outdir=None):
    outdir = outdir or tempfile.mkdtemp(prefix="light_multipanel_demo_")
    os.makedirs(outdir, exist_ok=True)
    plt.style.use(os.path.join(HERE, "..", "assets", "publication.mplstyle"))
    rng = np.random.default_rng(7)
    colors = cp.OKABE_ITO_LIST

    fig = plt.figure(figsize=(7.2, 4.6))
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1.0, 1.1],
                  hspace=0.45, wspace=0.32)

    # (a) 顶部跨两列: 时间序列 + 误差带
    ax_a = fig.add_subplot(gs[0, :])
    t = np.linspace(0, 10, 200)
    for i, (lbl, freq) in enumerate([("ctrl", 1.0), ("drug", 1.4)]):
        y = np.sin(freq * t) * np.exp(-t / 12) + rng.normal(0, 0.02, t.size)
        err = 0.08 + 0.01 * np.abs(np.cos(freq * t))
        ax_a.plot(t, y, color=colors[i + 1], label=lbl, lw=1.3)
        ax_a.fill_between(t, y - err, y + err, color=colors[i + 1], alpha=0.18)
    ax_a.set_xlabel("time (s)")
    ax_a.set_ylabel("response (a.u.)")
    ax_a.legend(ncol=2, loc="upper right")
    panel_tag(ax_a, "a", dx=-0.06)

    # (b) 分组柱状 + 误差棒 + 显著性
    ax_b = fig.add_subplot(gs[1, 0])
    groups = ["WT", "KO", "Rescue"]
    means = np.array([4.2, 6.8, 4.6])
    sems = np.array([0.3, 0.4, 0.35])
    xpos = np.arange(len(groups))
    ax_b.bar(xpos, means, yerr=sems, capsize=3,
             color=[colors[3], colors[6], colors[2]], width=0.65,
             error_kw=dict(lw=0.8))
    ax_b.set_xticks(xpos)
    ax_b.set_xticklabels(groups)
    ax_b.set_ylabel("firing rate (Hz)")
    ax_b.set_ylim(0, 8.5)
    sig_bar(ax_b, 0, 1, 7.4, "**")
    sig_bar(ax_b, 1, 2, 8.0, "*")
    panel_tag(ax_b, "b")

    # (c) 散点 + 拟合线 + 95% 区间
    ax_c = fig.add_subplot(gs[1, 1])
    x = rng.uniform(0, 10, 60)
    y = 0.8 * x + 1.0 + rng.normal(0, 1.2, x.size)
    ax_c.scatter(x, y, s=12, color=colors[5], alpha=0.7, edgecolor="none")
    coef = np.polyfit(x, y, 1)
    xs = np.linspace(0, 10, 50)
    ys = np.polyval(coef, xs)
    resid = y - np.polyval(coef, x)
    se = resid.std() * 1.96
    ax_c.plot(xs, ys, color="black", lw=1.2)
    ax_c.fill_between(xs, ys - se, ys + se, color="black", alpha=0.12)
    ax_c.set_xlabel("dose (mg)")
    ax_c.set_ylabel("effect")
    ax_c.text(0.05, 0.92, f"slope={coef[0]:.2f}", transform=ax_c.transAxes,
              fontsize=7)
    panel_tag(ax_c, "c")

    out = os.path.join(outdir, "out_multipanel")
    written, info = fx.save_for_journal(fig, out, journal="nature",
                                        column="double", height_mm=120,
                                        formats=("pdf", "png"))
    rep = fx.check_figure_size(fig, journal="nature", column="double")
    print("[example] 导出:", [os.path.basename(p) for p in written], "->", outdir)
    print("[example] 规格:", info)
    print("[example] 校验:", "OK" if rep["ok"] else f"FAIL {rep['problems']}")
    plt.close(fig)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="GridSpec 多面板组图示例（默认输出临时目录）")
    ap.add_argument("--outdir", default=None,
                    help="输出目录；缺省落临时目录，不污染 examples/")
    a = ap.parse_args()
    main(a.outdir)