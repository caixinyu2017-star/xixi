#!/usr/bin/env python3
"""example_framework_render.py — 渲染 example_framework.dot 为图

优先用 Graphviz `dot` 二进制 (最佳排版); 若环境无 dot, 自动降级:
用 matplotlib 画等价的分层框架图 (块 + 箭头), 保证本脚本永远能跑通产 png。

直接 python 运行; matplotlib Agg。
"""
import os
import shutil
import subprocess
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
DOT = os.path.join(HERE, "example_framework.dot")
OKABE = {"blue": "#56B4E9", "green": "#009E73", "orange": "#E69F00",
         "purple": "#CC79A7", "yellow": "#F0E442"}


def render_with_graphviz():
    dot_bin = shutil.which("dot")
    if not dot_bin:
        return None
    out = os.path.join(HERE, "out_framework.png")
    try:
        subprocess.run([dot_bin, "-Tpng", "-Gdpi=600", DOT, "-o", out],
                       check=True, capture_output=True, timeout=60)
        return out if os.path.exists(out) else None
    except Exception as e:
        print("[framework] dot 渲染失败, 降级 matplotlib:", e)
        return None


def render_fallback():
    """matplotlib 等价分层框架图。"""
    plt.style.use(os.path.join(HERE, "..", "assets", "publication.mplstyle"))
    fig, ax = plt.subplots(figsize=(7.2, 2.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")

    def box(x, y, w, h, text, fc):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                           linewidth=1.0, edgecolor="#333333", facecolor=fc)
        ax.add_patch(p)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8)
        return (x + w, y + h / 2), (x, y + h / 2)

    def arrow(p_from, p_to, style="-", color="#555555"):
        a = FancyArrowPatch(p_from, p_to, arrowstyle="-|>", mutation_scale=10,
                            lw=1.0, color=color, linestyle=style,
                            shrinkA=0, shrinkB=0)
        ax.add_patch(a)

    nodes = [
        (0.3, "Input\n(image/signal)", OKABE["blue"]),
        (2.6, "Backbone\nEncoder", OKABE["green"]),
        (4.9, "Feature\nPyramid", OKABE["green"]),
        (7.2, "Attention\nFusion", OKABE["orange"]),
        (9.5, "Task\nHead", OKABE["orange"]),
    ]
    w, h, y = 1.9, 1.0, 1.5
    rights, lefts = [], []
    for x, txt, fc in nodes:
        r, l = box(x, y, w, h, txt, fc)
        rights.append(r)
        lefts.append(l)
    for i in range(len(nodes) - 1):
        arrow(rights[i], lefts[i + 1])
    # skip 连接 enc1 -> attn (虚线, 走上方)
    arrow((rights[1][0], y + h), (lefts[3][0], y + h), style="--", color="#888888")
    ax.text((rights[1][0] + lefts[3][0]) / 2, y + h + 0.15, "skip",
            ha="center", fontsize=7, color="#888888")
    # 输出 + loss (椭圆用文字框替代)
    ax.text(11.3, y + h / 2, "Prediction\n+ Loss", ha="center", va="center",
            fontsize=8, bbox=dict(boxstyle="round", fc=OKABE["yellow"],
                                  ec="#333333", lw=1.0))
    arrow(rights[4], (10.7, y + h / 2))

    out = os.path.join(HERE, "out_framework.png")
    fig.savefig(out, dpi=600, bbox_inches="tight")
    plt.close(fig)
    return out


def main():
    out = render_with_graphviz()
    backend = "graphviz(dot)"
    if out is None:
        out = render_fallback()
        backend = "matplotlib(fallback)"
    ok = os.path.exists(out) and os.path.getsize(out) > 0
    print(f"[framework] backend={backend} -> {os.path.basename(out)} ok={ok}")


if __name__ == "__main__":
    main()