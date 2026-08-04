# -*- coding: utf-8 -*-
"""论文级绘图统一样式（nature-figure Python backend）。
所有图：白底、无顶右边框、300dpi、中文黑体近似字形（Noto Sans CJK SC）。
配色对色盲友好，并以线型/填充做冗余编码，保证黑白打印可辨。
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

fm._load_fontmanager(try_read_cache=False)

CN = "Noto Sans CJK SC"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": [CN, "DejaVu Sans"],
    "axes.unicode_minus": False,
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8.5,
    "legend.frameon": False,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "lines.linewidth": 1.4,
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
})

# 主色板（低饱和、打印友好、色盲可辨）
C = {
    "navy":   "#1F3B63",
    "steel":  "#3D6E9E",
    "sky":    "#8FB4D9",
    "amber":  "#E0A33E",
    "clay":   "#B5651D",
    "brick":  "#A8423F",
    "sage":   "#7A9E7E",
    "teal":   "#2A7F7F",
    "gray":   "#6B7A8F",
    "lgray":  "#C8CFD8",
    "ink":    "#2C3E50",
}
SEQ = [C["navy"], C["steel"], C["amber"], C["brick"], C["sage"], C["gray"]]
HATCH = ["", "///", "...", "xxx", "\\\\\\", "|||"]


def save(fig, path):
    fig.savefig(path)
    plt.close(fig)
    print("[saved]", path)
