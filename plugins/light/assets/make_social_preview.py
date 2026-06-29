#!/usr/bin/env python3
"""生成 GitHub 社交预览图 assets/social-preview.png(1280x640)。

可复现:`python assets/make_social_preview.py`。纯 matplotlib,无网络。
GitHub Settings > Social preview 推荐 1280x640。logo 标语 + 量化数字 + 主线示意。
"""
from __future__ import annotations
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
INK = "#1B2030"
WHITE = "#FFFFFF"
MUTE = "#5C6478"


def main(out="assets/social-preview.png"):
    W, H = 1280, 640
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # 背景:淡靛渐变带
    ax.add_patch(plt.Rectangle((0, 0), W, H, color="#FBFCFF"))
    ax.add_patch(plt.Rectangle((0, 0), W, 14, color=INDIGO))
    ax.add_patch(plt.Rectangle((0, H - 14), W, 14, color=GREEN))

    # 品牌名
    ax.text(80, 500, "Light", fontsize=84, fontweight="bold", color=INDIGO,
            ha="left", va="center")
    # 标语
    ax.text(82, 430, "全流程科研技能包", fontsize=36, fontweight="bold",
            color=INK, ha="left", va="center")
    ax.text(82, 384, "让 AI 陪你把一篇论文从想法做到投稿", fontsize=22,
            color=MUTE, ha="left", va="center")

    # 数字卡片
    stats = [("28", "技能"), ("9", "知识库"), ("49", "脚本"),
             ("39", "模板"), ("317", "知识卡")]
    cw, gap = 198, 22
    x0 = 80
    y0 = 250
    for i, (num, lab) in enumerate(stats):
        x = x0 + i * (cw + gap)
        card = FancyBboxPatch((x, y0 - 56), cw, 112,
                              boxstyle="round,pad=2,rounding_size=14",
                              linewidth=2, edgecolor=INDIGO, facecolor="#EEF1FE")
        ax.add_patch(card)
        ax.text(x + cw / 2, y0 + 16, num, fontsize=40, fontweight="bold",
                color=INDIGO, ha="center", va="center")
        ax.text(x + cw / 2, y0 - 30, lab, fontsize=18, color=MUTE,
                ha="center", va="center")

    # 主线示意箭头条
    chain = ["文献", "数据", "创新", "实验", "分析", "写作", "图表", "投稿", "成果"]
    bx = 80
    by = 120
    bw2 = 110
    bgap = 18
    for i, c in enumerate(chain):
        x = bx + i * (bw2 + bgap)
        col = GREEN if i == len(chain) - 1 else INDIGO
        fc = "#ECFBF2" if i == len(chain) - 1 else "#EEF1FE"
        box = FancyBboxPatch((x, by - 26), bw2, 52,
                             boxstyle="round,pad=1,rounding_size=10",
                             linewidth=1.6, edgecolor=col, facecolor=fc)
        ax.add_patch(box)
        ax.text(x + bw2 / 2, by, c, fontsize=19, fontweight="bold",
                color=INK, ha="center", va="center")
        if i < len(chain) - 1:
            xa = x + bw2
            ax.add_patch(FancyArrowPatch((xa, by), (xa + bgap, by),
                         arrowstyle="-|>", mutation_scale=12,
                         linewidth=1.6, color=INDIGO))

    # 底注卖点
    ax.text(W - 70, 500, "Claude Code · Codex",
            fontsize=20, color=INDIGO, ha="right", va="center", fontweight="bold")
    ax.text(W - 70, 466, "28 技能沿科研主线闭环 · 全程不编造",
            fontsize=16, color=MUTE, ha="right", va="center")

    fig.savefig(out, format="png", dpi=100, facecolor="#FBFCFF")
    plt.close(fig)
    print(f"wrote {out} ({W}x{H}, font={CJK})")


if __name__ == "__main__":
    main()
