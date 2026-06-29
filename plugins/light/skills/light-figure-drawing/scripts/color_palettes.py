#!/usr/bin/env python3
"""color_palettes.py — 投稿级配色工具 (Light / light-figure-drawing)

提供:
  - OKABE_ITO            8 色色盲安全离散调色板 (hex 常量)
  - 连续色板 (sequential) 与发散色板 (diverging) 构造器
  - apply_palette()      把离散调色板设为 matplotlib 当前色环
  - to_grayscale()       把任意颜色按感知亮度转灰度 (检查黑白打印可辨)
  - simulate_cvd()       色盲(CVD)模拟; 有 colorspacious 用精确算法, 否则降级近似
  - preview_palette()    出一张对照图 (原色/灰度/三种色盲) 存 png

无外部数据; matplotlib Agg; __main__ 自检并产预览图。
"""
from __future__ import annotations
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import (LinearSegmentedColormap, to_rgb, to_hex,
                               ListedColormap)

# --- Okabe-Ito (2008) 色盲安全 8 色 ---
OKABE_ITO = {
    "black":        "#000000",
    "orange":       "#E69F00",
    "sky_blue":     "#56B4E9",
    "bluish_green": "#009E73",
    "yellow":       "#F0E442",
    "blue":         "#0072B2",
    "vermillion":   "#D55E00",
    "reddish_purple": "#CC79A7",
}
OKABE_ITO_LIST = list(OKABE_ITO.values())

# 感知亮度权重 (Rec.709 线性近似, 用于灰度)
_LUMA = np.array([0.2126, 0.7152, 0.0722])

def sequential_cmap(name="light_seq", colors=("#FFF7EC", "#FC8D59", "#7F0000"),
                    n=256):
    """构造连续(顺序)色板: 浅->深, 适合单向数值。返回 Colormap。"""
    return LinearSegmentedColormap.from_list(name, list(colors), N=n)


def diverging_cmap(name="light_div",
                   colors=("#0072B2", "#F7F7F7", "#D55E00"), n=256):
    """构造发散色板: 蓝-白-橙(色盲安全两端), 适合有中性零点的数据。"""
    return LinearSegmentedColormap.from_list(name, list(colors), N=n)


def discrete_cmap(colors=None, name="okabe_ito"):
    """把离散色列表包成 ListedColormap。默认 Okabe-Ito。"""
    if colors is None:
        colors = OKABE_ITO_LIST
    return ListedColormap(colors, name=name)


def apply_palette(colors=None, ax=None):
    """把离散调色板设为当前(或指定 ax 的)色环。默认 Okabe-Ito。"""
    if colors is None:
        colors = OKABE_ITO_LIST
    from cycler import cycler
    cyc = cycler(color=colors)
    if ax is not None:
        ax.set_prop_cycle(cyc)
    else:
        plt.rcParams["axes.prop_cycle"] = cyc
    return colors


def to_grayscale(color):
    """单色 -> 灰度 hex (感知亮度)。color 可为 hex/名称/rgb。"""
    rgb = np.array(to_rgb(color))
    y = float(np.dot(rgb, _LUMA))
    return to_hex((y, y, y))


def palette_grayscale(colors=None):
    """整组颜色转灰度 hex 列表。"""
    if colors is None:
        colors = OKABE_ITO_LIST
    return [to_grayscale(c) for c in colors]


# --- 色盲(CVD)模拟 ---
# 降级用的线性近似矩阵 (Machado 2009 严重程度近似), 仅在缺 colorspacious 时用。
_CVD_APPROX = {
    "deuteranomaly": np.array([[0.367, 0.861, -0.228],
                               [0.280, 0.673, 0.047],
                               [-0.012, 0.043, 0.969]]),
    "protanomaly":   np.array([[0.152, 1.053, -0.205],
                               [0.115, 0.786, 0.099],
                               [-0.004, -0.048, 1.052]]),
    "tritanomaly":   np.array([[1.256, -0.077, -0.179],
                               [-0.078, 0.931, 0.148],
                               [0.005, 0.691, 0.304]]),
}
# colorspacious 命名映射
_CS_NAME = {"deuteranomaly": "deuteranomaly",
            "protanomaly": "protanomaly",
            "tritanomaly": "tritanomaly"}


def simulate_cvd(color, kind="deuteranomaly", severity=100):
    """模拟色盲下的颜色。优先 colorspacious(精确), 否则线性近似(降级)。

    kind: deuteranomaly / protanomaly / tritanomaly
    severity: 0-100
    返回 hex。
    """
    rgb = np.array(to_rgb(color), dtype=float)
    try:
        import colorspacious as cs
        cvd_space = {"name": "sRGB1+CVD", "cvd_type": _CS_NAME[kind],
                     "severity": severity}
        out = cs.cspace_convert(rgb, cvd_space, "sRGB1")
        out = np.clip(out, 0, 1)
        return to_hex(tuple(out))
    except Exception:
        # 降级: 线性矩阵 + severity 线性插值
        m = _CVD_APPROX[kind]
        sev = severity / 100.0
        full = np.clip(m @ rgb, 0, 1)
        out = (1 - sev) * rgb + sev * full
        return to_hex(tuple(np.clip(out, 0, 1)))


def cvd_backend():
    """返回当前 CVD 模拟用的后端名: 'colorspacious' 或 'approx'。"""
    try:
        import colorspacious  # noqa
        return "colorspacious"
    except Exception:
        return "approx"


def preview_palette(colors=None, outpath=None, title="palette"):
    """出对照预览: 原色 / 灰度 / 三种色盲, 存 png。返回路径。"""
    if colors is None:
        colors = OKABE_ITO_LIST
    rows = [("original", list(colors)),
            ("grayscale", palette_grayscale(colors)),
            ("deuteranomaly", [simulate_cvd(c, "deuteranomaly") for c in colors]),
            ("protanomaly", [simulate_cvd(c, "protanomaly") for c in colors]),
            ("tritanomaly", [simulate_cvd(c, "tritanomaly") for c in colors])]
    n = len(colors)
    fig, ax = plt.subplots(figsize=(max(4, n * 0.7), len(rows) * 0.7))
    for r, (label, cols) in enumerate(rows):
        y = len(rows) - 1 - r
        for i, c in enumerate(cols):
            ax.add_patch(plt.Rectangle((i, y), 0.96, 0.96, color=c))
        ax.text(-0.2, y + 0.48, label, ha="right", va="center", fontsize=8)
    ax.set_xlim(-2.2, n)
    ax.set_ylim(0, len(rows))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{title}  (CVD backend: {cvd_backend()})", fontsize=9, loc="left")
    if outpath is None:
        outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "examples", "_export_demo", "palette_preview.png")
    os.makedirs(os.path.dirname(os.path.abspath(outpath)), exist_ok=True)
    fig.savefig(outpath, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return outpath


def _selfcheck():
    # 常量
    assert len(OKABE_ITO_LIST) == 8
    assert all(c.startswith("#") and len(c) == 7 for c in OKABE_ITO_LIST)
    # 灰度: 黄色亮度应高于蓝色
    gy = float(np.dot(to_rgb(OKABE_ITO["yellow"]), _LUMA))
    gb = float(np.dot(to_rgb(OKABE_ITO["blue"]), _LUMA))
    assert gy > gb, (gy, gb)
    # 色板构造
    assert sequential_cmap().N == 256
    assert diverging_cmap().N == 256
    assert discrete_cmap().N == 8
    # apply_palette 改色环
    apply_palette()
    cyc = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    assert cyc[0].lower() == "#000000"
    # CVD 模拟返回合法 hex
    for k in ("deuteranomaly", "protanomaly", "tritanomaly"):
        h = simulate_cvd("#E69F00", k)
        assert h.startswith("#") and len(h) == 7, h
    # 预览图
    p = preview_palette(title="Okabe-Ito")
    assert os.path.exists(p) and os.path.getsize(p) > 0
    print(f"[selfcheck] PASS  CVD backend={cvd_backend()}  preview={os.path.abspath(p)}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--selftest":
        raise SystemExit("usage: python color_palettes.py [--selftest]")
    _selfcheck()
