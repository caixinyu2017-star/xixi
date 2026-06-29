#!/usr/bin/env python3
"""生成 README 技能链路图 assets/pipeline.svg(+png)。

可复现:`python assets/make_pipeline_svg.py`。纯 matplotlib,无网络。
主线 28 技能里的 17 手动技能沿科研主线串联,外圈标注 11 常驻技能兜底。
中文字体优先 Microsoft YaHei/SimHei(Windows 自带);缺失则退 DejaVu(英文标签仍可读)。
"""
from __future__ import annotations
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

CJK = next((n for n in ["Microsoft YaHei", "SimHei", "SimSun",
                        "Noto Sans CJK SC", "Source Han Sans SC"]
            if n in {f.name for f in fm.fontManager.ttflist}), "DejaVu Sans")
plt.rcParams["font.sans-serif"] = [CJK, "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INDIGO = "#5B6FE0"
GREEN = "#3DDC84"
AMBER = "#FFA63D"
INK = "#1F2430"
GREY = "#8A93A6"

# 主线节点:(label, sub)
MAIN = [
    ("文献检索", "literature-search"),
    ("数据工程", "data-engineering"),
    ("创新点·严审", "idea-gen / critique"),
    ("方案设计", "research-plan"),
    ("实验落地", "backend-coding"),
    ("结果分析", "result-analysis"),
    ("写作·润色", "drafting / polishing"),
    ("图表", "figure plan / draw"),
    ("引用·排版", "citation · typesetting"),
    ("投稿·返修", "venue / rebuttal"),
    ("成果转化", "软著·专利·PPT·竞赛"),
]
RESIDENT = ("file-reading · memory-pm · orchestrator · backend-coding · "
            "system-design · frontend-design · project-structure · "
            "consistency · self-review · tool-selection · research-ethics")


def main(out_svg="assets/pipeline.svg", out_png="assets/pipeline.png"):
    cols = 4
    rows = (len(MAIN) + cols - 1) // cols
    fig_w, fig_h = 13.0, 7.4
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
    ax.set_xlim(0, cols)
    ax.set_ylim(-1.15, rows + 0.7)
    ax.axis("off")

    bw, bh = 0.86, 0.62
    centers = []
    for i, (label, sub) in enumerate(MAIN):
        r = i // cols
        c = i % cols
        # 蛇形:奇数行从右往左,视觉连续
        if r % 2 == 1:
            c = cols - 1 - c
        y = (rows - 1 - r) + 0.25
        x = c + 0.5
        centers.append((x, y, i))
        box = FancyBboxPatch((x - bw / 2, y - bh / 2), bw, bh,
                             boxstyle="round,pad=0.02,rounding_size=0.10",
                             linewidth=1.6, edgecolor=INDIGO,
                             facecolor="#EEF1FE")
        ax.add_patch(box)
        ax.text(x, y + 0.10, label, ha="center", va="center",
                fontsize=11.5, color=INK, fontweight="bold")
        ax.text(x, y - 0.16, sub, ha="center", va="center",
                fontsize=7.0, color=GREY)

    # 主线箭头(按 i 顺序连)
    for (x0, y0, i0), (x1, y1, i1) in zip(centers, centers[1:]):
        same_row = abs(y0 - y1) < 1e-6
        if same_row:
            xa = x0 + (bw / 2 if x1 > x0 else -bw / 2)
            xb = x1 + (-bw / 2 if x1 > x0 else bw / 2)
            arr = FancyArrowPatch((xa, y0), (xb, y1),
                                  arrowstyle="-|>", mutation_scale=14,
                                  linewidth=1.5, color=INDIGO)
        else:
            arr = FancyArrowPatch((x0, y0 - bh / 2), (x1, y1 + bh / 2),
                                  connectionstyle="arc3,rad=0.0",
                                  arrowstyle="-|>", mutation_scale=14,
                                  linewidth=1.5, color=INDIGO)
        ax.add_patch(arr)

    # 标题
    ax.text(cols / 2, rows + 0.42, "Light 科研主线 · 17 手动技能闭环",
            ha="center", va="center", fontsize=15, fontweight="bold", color=INK)

    # 常驻环底注
    band = FancyBboxPatch((0.15, -1.02), cols - 0.30, 0.62,
                          boxstyle="round,pad=0.02,rounding_size=0.08",
                          linewidth=1.4, edgecolor=GREEN, facecolor="#ECFBF2")
    ax.add_patch(band)
    ax.text(cols / 2, -0.58, "11 常驻技能后台兜底", ha="center", va="center",
            fontsize=10.5, fontweight="bold", color="#1B7F4B")
    ax.text(cols / 2, -0.86, RESIDENT, ha="center", va="center",
            fontsize=6.6, color="#2E7D52")

    fig.tight_layout()
    fig.savefig(out_svg, format="svg", bbox_inches="tight", transparent=True)
    fig.savefig(out_png, format="png", bbox_inches="tight",
                facecolor="white", dpi=150)
    plt.close(fig)
    print(f"wrote {out_svg} and {out_png} (font={CJK})")


if __name__ == "__main__":
    main(*(sys.argv[1:3] if len(sys.argv) >= 3 else []))
