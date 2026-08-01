#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成《"禾灵儿"数字画像功能建设方案》全部示意图（学术风格，300 dpi PNG）。

统一视觉规范：白底、无网格冗余、细线、中性灰配深青绿主色、Noto Sans CJK SC 中文字体。
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
from matplotlib.path import Path
import matplotlib.patches as mpatches

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.sans-serif": ["Noto Sans CJK SC", "WenQuanYi Zen Hei", "DejaVu Sans"],
    "font.family": "sans-serif",
    "axes.unicode_minus": False,
    "savefig.dpi": 300,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.06,
    "axes.linewidth": 0.8,
})

# ---- 配色 --------------------------------------------------------------
DEEP = "#0F4C43"   # 主色（深青绿）
MAIN = "#1F7A6B"
MID = "#3D9C87"
SOFT = "#8FC6B5"
PALE = "#E4F1EC"
GRAY = "#4B5563"
LGRAY = "#9CA3AF"
XLGRAY = "#E5E7EB"
ACC = "#B45309"    # 强调（赭）
ACC_PALE = "#FCEBD8"
INK = "#1F2937"


def box(ax, x, y, w, h, text, fc=PALE, ec=MAIN, lw=0.9, fs=8.2, tc=INK,
        weight="normal", radius=0.6, ha="center"):
    """圆角矩形 + 居中文本。"""
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={radius}",
                       facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, weight=weight, zorder=3, linespacing=1.35)
    return p


def arrow(ax, xy1, xy2, color=MAIN, lw=1.1, style="-|>", ms=8, rad=0.0, ls="-"):
    a = FancyArrowPatch(xy1, xy2, arrowstyle=style, mutation_scale=ms,
                        color=color, linewidth=lw, zorder=4,
                        connectionstyle=f"arc3,rad={rad}", linestyle=ls,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    return a


def blank_ax(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


# =======================================================================
# 图1  总体技术架构
# =======================================================================
def fig1():
    fig, ax = blank_ax((7.4, 5.6))

    layers = [
        ("画像应用层", ["学生端\n五维画像·成长轨迹", "教师端\n班级看板·预警", "管理端\n院系聚合·督导",
                        "一生一案\n微任务·资源推送"], MAIN),
        ("DR-NKT 建模层", ["行为时序图\nTGCN 行为表征", "文化素养本体\nSOP 符号解析",
                            "交叉注意力\n证据—维度对齐", "得分合成\n衰减·饱和·收缩"], MID),
        ("证据抽取层", ["规则指标引擎\n可计数客观量", "多模态内容解析\n文本·图像·视频",
                        "LLM 量规评分器\nrubric + 置信度", "人机复核\n抽检·申诉·校准"], SOFT),
        ("数据治理层", ["事件规范化\n五元组统一模型", "身份对齐与去标识\n一人一码",
                        "质量校验\n去重·异常过滤", "多模态资产归档\n证据留存"], SOFT),
        ("感知采集层", ["文化对话", "文化课程\n教师工作台", "智能体广场\n智能体开发",
                        "视频生成\n视频广场", "PPT 制作\n微智工具",
                        "智能应用\n资讯中心\n意见反馈"], MID),
    ]

    x0, x1 = 5.0, 93.0
    lab_w = 17.5
    band_h = 15.6
    gap = 3.6
    top = 96.0

    ys = []
    for i, (name, items, col) in enumerate(layers):
        y = top - (i + 1) * band_h - i * gap
        ys.append(y)
        # 外框
        ax.add_patch(FancyBboxPatch((x0, y), x1 - x0, band_h,
                                    boxstyle="round,pad=0,rounding_size=0.9",
                                    facecolor="white", edgecolor=GRAY,
                                    linewidth=0.8, zorder=1))
        # 左侧层名
        ax.add_patch(FancyBboxPatch((x0, y), lab_w, band_h,
                                    boxstyle="round,pad=0,rounding_size=0.9",
                                    facecolor=DEEP if i in (0, 1) else MAIN,
                                    edgecolor=DEEP, linewidth=0.8, zorder=2))
        ax.text(x0 + lab_w / 2, y + band_h / 2, name, ha="center", va="center",
                fontsize=8.6, color="white", weight="bold", zorder=3,
                linespacing=1.3)
        # 组件
        n = len(items)
        inner_x = x0 + lab_w + 2.0
        inner_w = x1 - inner_x - 2.0
        cw = (inner_w - (n - 1) * 1.6) / n
        for j, it in enumerate(items):
            box(ax, inner_x + j * (cw + 1.6), y + 2.4, cw, band_h - 4.8, it,
                fc=PALE if i != 0 else ACC_PALE,
                ec=MAIN if i != 0 else ACC, fs=7.3 if n == 4 else 6.9, radius=0.5)

    # 上行数据流箭头
    for i in range(len(layers) - 1, 0, -1):
        arrow(ax, (50, ys[i] + band_h), (50, ys[i - 1]), color=DEEP, lw=1.3, ms=9)
    # 反馈回路
    fb = 96.5
    ax.plot([fb, fb], [ys[0] + band_h / 2, ys[-1] + band_h / 2],
            color=ACC, lw=1.0, ls=(0, (4, 2)), zorder=1)
    ax.plot([x1, fb], [ys[0] + band_h / 2, ys[0] + band_h / 2],
            color=ACC, lw=1.0, ls=(0, (4, 2)), zorder=1)
    arrow(ax, (fb, ys[-1] + band_h / 2), (x1, ys[-1] + band_h / 2),
          color=ACC, lw=1.0, ms=8, ls=(0, (4, 2)))
    ax.text(99.2, (ys[0] + ys[-1]) / 2 + band_h / 2, "干预回写与再采集",
            rotation=90, ha="center", va="center", fontsize=7.4, color=ACC)

    ax.text(50, ys[-1] - 4.2,
            "注：实线箭头为数据自下而上的加工流向，虚线为干预结果回写形成的闭环。",
            ha="center", va="center", fontsize=7.2, color=GRAY)
    ax.set_xlim(3, 101)
    ax.set_ylim(ys[-1] - 7.5, 99)
    fig.savefig(os.path.join(OUT, "fig1_architecture.png"))
    plt.close(fig)


# =======================================================================
# 图2  五维文化素养指标体系
# =======================================================================
def fig2():
    fig, ax = blank_ax((7.4, 6.2))

    dims = [
        ("文化体验", "行·亲历", ["E1 场景参与广度", "E2 沉浸时长与在场度",
                                 "E3 实践任务完成度", "E4 多模态交互丰富度"]),
        ("文化认知", "知", ["C1 知识点掌握度", "C2 概念网络覆盖度",
                            "C3 理解迁移深度", "C4 反思与元认知质量"]),
        ("文化志趣", "意", ["I1 自主发起度", "I2 学习持续性",
                            "I3 主题探索广度", "I4 深度投入强度"]),
        ("文化认同", "情", ["D1 情感倾向与归属", "D2 价值判断与立场",
                            "D3 传播与推荐意愿", "D4 跨文化自信表达"]),
        ("文化研创", "行·创造", ["R1 成果产出规范性", "R2 原创性与创意度",
                                 "R3 研究方法与证据", "R4 传播成效与影响"]),
    ]

    # 左：理论来源
    box(ax, 0.5, 39, 16.5, 24, "知—情—意—行\n四位一体\n\n5C 素养模型\n文化理解与传承",
        fc=DEEP, ec=DEEP, fs=8.0, tc="white", weight="bold", radius=0.8)

    top = 96.0
    h = 16.5
    gap = 3.2
    for i, (name, src, obs) in enumerate(dims):
        y = top - (i + 1) * h - i * gap
        # 一级维度
        box(ax, 20.5, y, 20.5, h, f"{name}\n（{src}）", fc=PALE, ec=MAIN,
            fs=9.4, weight="bold", radius=0.7)
        arrow(ax, (17.0, 51), (20.5, y + h / 2), color=MAIN, lw=0.9, ms=7, rad=0.06)
        # 二级观测点
        for j, o in enumerate(obs):
            oy = y + h - (j + 1) * (h / 4) + 0.55
            box(ax, 46.0, oy, 50.0, h / 4 - 1.1, o, fc="white", ec=SOFT,
                fs=7.6, radius=0.35)
        arrow(ax, (41.0, y + h / 2), (46.0, y + h / 2), color=MID, lw=1.0, ms=8)

    ax.text(30.75, 99.2, "一级素养维度", ha="center", va="center",
            fontsize=8.6, color=GRAY, weight="bold")
    ax.text(71.0, 99.2, "二级观测点（共 20 项）", ha="center", va="center",
            fontsize=8.6, color=GRAY, weight="bold")
    ax.text(8.75, 99.2, "理论依据", ha="center", va="center",
            fontsize=8.6, color=GRAY, weight="bold")
    ax.set_xlim(-1, 98)
    ax.set_ylim(-1, 102)
    fig.savefig(os.path.join(OUT, "fig2_indicator_system.png"))
    plt.close(fig)


# =======================================================================
# 图3  栏目—维度贡献权重矩阵
# =======================================================================
def fig3():
    cols = ["文化\n体验", "文化\n认知", "文化\n志趣", "文化\n认同", "文化\n研创"]
    rows = [
        "文化对话", "文化课程", "教师工作台", "智能体广场", "智能体开发",
        "视频生成", "视频广场", "PPT 制作", "微智工具", "智能应用",
        "智能化评价", "资讯中心", "意见反馈",
    ]
    # 行内归一化的渠道贡献权重 w_{c,d}
    W = np.array([
        [0.10, 0.30, 0.25, 0.25, 0.10],  # 文化对话
        [0.20, 0.35, 0.15, 0.10, 0.20],  # 文化课程
        [0.15, 0.25, 0.15, 0.20, 0.25],  # 教师工作台
        [0.15, 0.25, 0.40, 0.10, 0.10],  # 智能体广场
        [0.05, 0.25, 0.15, 0.05, 0.50],  # 智能体开发
        [0.20, 0.10, 0.10, 0.20, 0.40],  # 视频生成
        [0.20, 0.05, 0.20, 0.25, 0.30],  # 视频广场
        [0.05, 0.30, 0.10, 0.15, 0.40],  # PPT 制作
        [0.40, 0.30, 0.20, 0.05, 0.05],  # 微智工具
        [0.45, 0.15, 0.15, 0.15, 0.10],  # 智能应用
        [0.05, 0.30, 0.15, 0.35, 0.15],  # 智能化评价
        [0.10, 0.25, 0.40, 0.20, 0.05],  # 资讯中心
        [0.05, 0.05, 0.45, 0.40, 0.05],  # 意见反馈
    ])

    fig, ax = plt.subplots(figsize=(5.6, 6.4))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "hl", ["#FFFFFF", "#D8ECE5", "#8FC6B5", "#3D9C87", "#0F4C43"])
    im = ax.imshow(W, cmap=cmap, vmin=0, vmax=0.5, aspect="auto")

    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, fontsize=8.6)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(rows, fontsize=8.4)
    ax.xaxis.set_ticks_position("top")
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)

    for i in range(len(rows)):
        for j in range(len(cols)):
            v = W[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7.4,
                    color="white" if v >= 0.30 else INK)
    ax.set_xticks(np.arange(-.5, len(cols), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(rows), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.2)
    ax.tick_params(which="minor", length=0)

    cb = fig.colorbar(im, ax=ax, fraction=0.036, pad=0.03)
    cb.ax.tick_params(labelsize=7.2, length=2)
    cb.set_label("渠道贡献权重 $w_{c,d}$", fontsize=8.0)
    cb.outline.set_linewidth(0.6)
    fig.savefig(os.path.join(OUT, "fig3_channel_dimension_matrix.png"))
    plt.close(fig)


# =======================================================================
# 图4  DR-NKT 画像计算流程
# =======================================================================
def fig4():
    fig, ax = blank_ax((8.0, 4.4))

    # 第一列：两条输入支路
    box(ax, 0.5, 60, 21, 20,
        "学生行为事件流\n$\\{e_1,e_2,\\dots ,e_T\\}$\n栏目·动作·对象·时间", fc="white",
        ec=GRAY, fs=7.4, radius=0.6)
    box(ax, 0.5, 12, 21, 20,
        "文化素养目标体系\n5 维度 / 20 观测点\n文化本体与先修关系", fc="white",
        ec=GRAY, fs=7.4, radius=0.6)

    # 第二列：双表征编码
    box(ax, 25, 60, 20, 20,
        "行为时序图 + TGCN\n行为表征\n$\\mathbf{h}_e\\in\\mathbb{R}^{k}$",
        fc=PALE, ec=MAIN, fs=7.8, radius=0.6)
    box(ax, 25, 12, 20, 20,
        "符号本体解析器 SOP\n观测点概念嵌入\n$\\mathbf{g}_m\\in\\mathbb{R}^{k}$",
        fc=PALE, ec=MAIN, fs=7.8, radius=0.6)

    # 第三列：交叉注意力
    box(ax, 49, 28, 22, 36,
        "交叉注意力对齐\n\n\n$\\alpha_{e,d}\\!=\\!\\mathrm{softmax}"
        "(\\mathbf{g}_d^{\\top}\\mathbf{W}\\mathbf{h}_e/\\sqrt{d})$"
        "\n\n\n行为证据 ↔ 素养维度",
        fc=ACC_PALE, ec=ACC, fs=7.0, radius=0.7)

    # 第四列：双路输出
    box(ax, 75, 66, 24, 18,
        "评价依据矩阵\n$\\mathbf{A}=[\\alpha_{e,m}]_{T\\times 20}$\n可解释证据链",
        fc=PALE, ec=MAIN, fs=7.8, radius=0.6)
    box(ax, 75, 38, 24, 18,
        "得分合成\n时间衰减 $\\lambda_e$ · 证据饱和 $\\rho_d$\n贝叶斯收缩 → $\\mathbf{S}$",
        fc=PALE, ec=MAIN, fs=7.8, radius=0.6)
    box(ax, 75, 10, 24, 18,
        "综合文化素养指数\n$\\mathrm{CCI}$ · 等级 · 环比增长",
        fc=PALE, ec=MAIN, fs=7.8, radius=0.6)

    arrow(ax, (21.5, 70), (25, 70), lw=1.1)
    arrow(ax, (21.5, 22), (25, 22), lw=1.1)
    arrow(ax, (45, 70), (49, 55), lw=1.1, rad=-0.12)
    arrow(ax, (45, 22), (49, 37), lw=1.1, rad=0.12)
    arrow(ax, (71, 55), (75, 72), lw=1.1, rad=0.12)
    arrow(ax, (71, 42), (75, 47), lw=1.1, rad=-0.10)
    arrow(ax, (87, 38), (87, 28), lw=1.1)
    # 证据链回溯（虚线）
    ax.plot([87, 87], [84, 90], color=ACC, lw=1.0, ls=(0, (4, 2)), zorder=1)
    ax.plot([11, 87], [90, 90], color=ACC, lw=1.0, ls=(0, (4, 2)), zorder=1)
    arrow(ax, (11, 90), (11, 80), color=ACC, lw=1.0, ms=8, ls=(0, (4, 2)))
    ax.text(49, 92.5, "证据链回溯：每一项维度得分均可定位到支撑它的具体学习事件",
            ha="center", va="center", fontsize=7.4, color=ACC)
    ax.set_xlim(-1, 100)
    ax.set_ylim(6, 96)
    fig.savefig(os.path.join(OUT, "fig4_drnkt_pipeline.png"))
    plt.close(fig)


# =======================================================================
# 图5  证据饱和与贝叶斯收缩
# =======================================================================
def fig5():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    C = np.linspace(0, 40, 400)
    S0 = 0.50

    ax = axes[0]
    for kappa, ls in [(4, "-"), (8, "--"), (16, ":")]:
        rho = 1 - np.exp(-C / kappa)
        ax.plot(C, rho, ls, color=DEEP, lw=1.3, label=f"$\\kappa_d={kappa}$")
    ax.axhline(0.9, color=LGRAY, lw=0.7, ls=(0, (3, 3)))
    ax.text(1.2, 0.925, "$\\rho_d=0.9$", fontsize=7.2, color=GRAY, ha="left")
    ax.set_xlabel("有效证据容量 $C_d$", fontsize=8.4)
    ax.set_ylabel("证据充分度 $\\rho_d$", fontsize=8.4)
    ax.set_title("(a) 证据饱和函数", fontsize=9.0, pad=6)
    ax.legend(fontsize=7.4, frameon=False, loc="lower right")

    ax = axes[1]
    for b, col in [(0.90, DEEP), (0.75, MAIN), (0.50, LGRAY), (0.30, ACC)]:
        rho = 1 - np.exp(-C / 8)
        S = S0 + (b - S0) * rho
        ax.plot(C, S, color=col, lw=1.4, label=f"$b_d={b:.2f}$")
    ax.axhline(S0, color=GRAY, lw=0.7, ls=(0, (3, 3)))
    ax.text(21, 0.535, "先验参考分 $S_0=0.50$", fontsize=7.2, color=GRAY)
    ax.set_xlabel("有效证据容量 $C_d$", fontsize=8.4)
    ax.set_ylabel("维度得分 $S_d$", fontsize=8.4)
    ax.set_ylim(0.2, 1.03)
    ax.set_title("(b) 向先验收缩的维度得分", fontsize=9.0, pad=6)
    ax.legend(fontsize=7.2, frameon=False, loc="upper left", ncol=2,
              columnspacing=1.0, handlelength=1.6)

    for ax in axes:
        ax.tick_params(labelsize=7.6, length=2.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig5_shrinkage.png"))
    plt.close(fig)


# =======================================================================
# 图6  学生画像示例：雷达图与成长轨迹
# =======================================================================
def fig6():
    labels = ["文化认同", "文化研创", "文化体验", "文化认知", "文化志趣"]
    score = [0.85, 0.69, 0.80, 0.83, 0.87]
    base = [0.50] * 5

    fig = plt.figure(figsize=(7.2, 3.2))
    ax = fig.add_subplot(1, 2, 1, polar=True)
    ang = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    ang_c = np.concatenate([ang, ang[:1]])
    s_c = np.array(score + score[:1])
    b_c = np.array(base + base[:1])

    ax.plot(ang_c, s_c, color=MAIN, lw=1.6, label="学生得分")
    ax.fill(ang_c, s_c, color=MID, alpha=0.18)
    ax.plot(ang_c, b_c, color=GRAY, lw=1.0, ls=(0, (4, 2.5)), label="参考基线 0.50")
    ax.scatter(ang, score, s=16, color=MAIN, zorder=5)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(ang), labels, fontsize=8.2)
    ax.set_ylim(0, 1.05)
    ax.set_yticks([0.25, 0.50, 0.75, 1.00])
    ax.set_yticklabels([])
    ax.grid(color=XLGRAY, lw=0.7)
    ax.spines["polar"].set_color(LGRAY)
    ax.spines["polar"].set_linewidth(0.7)
    for a, s in zip(ang, score):
        ax.text(a, s - 0.11, f"{s:.2f}", ha="center", va="center",
                fontsize=7.2, color=DEEP)
    ax.set_title("(a) 五维素养雷达图", fontsize=9.0, pad=14)
    ax.legend(fontsize=7.0, frameon=False, loc="lower center",
              bbox_to_anchor=(0.5, -0.24), ncol=2)

    ax2 = fig.add_subplot(1, 2, 2)
    months = ["9月", "10月", "11月", "12月", "1月", "3月"]
    traj = {
        "文化认同": [0.55, 0.62, 0.70, 0.76, 0.81, 0.85],
        "文化志趣": [0.58, 0.66, 0.73, 0.79, 0.83, 0.87],
        "文化认知": [0.54, 0.61, 0.68, 0.75, 0.79, 0.83],
        "文化体验": [0.52, 0.58, 0.65, 0.71, 0.76, 0.80],
        "文化研创": [0.50, 0.53, 0.57, 0.62, 0.66, 0.69],
    }
    cols = [DEEP, MAIN, MID, SOFT, ACC]
    for (k, v), c in zip(traj.items(), cols):
        ax2.plot(months, v, marker="o", ms=2.8, lw=1.2, color=c, label=k)
    cci = [np.mean([traj[k][i] for k in traj]) for i in range(6)]
    ax2.plot(months, cci, lw=2.0, color=INK, ls=(0, (5, 2)), label="综合指数 CCI")
    ax2.annotate(f"{cci[-1]:.2f}", xy=(5, cci[-1]), xytext=(4.1, cci[-1] - 0.10),
                 fontsize=7.6, color=INK,
                 arrowprops=dict(arrowstyle="->", lw=0.7, color=INK))
    ax2.set_ylim(0.42, 1.02)
    ax2.set_ylabel("得分", fontsize=8.4)
    ax2.tick_params(labelsize=7.6, length=2.5)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="y", color=XLGRAY, lw=0.6)
    ax2.set_axisbelow(True)
    ax2.set_title("(b) 逐月成长轨迹", fontsize=9.0, pad=8)
    ax2.legend(fontsize=6.6, frameon=False, ncol=2, loc="upper left",
               columnspacing=1.0, handlelength=1.5, borderpad=0.2)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig6_portrait_example.png"))
    plt.close(fig)


# =======================================================================
# 图7  "一生一案"干预闭环
# =======================================================================
def fig7():
    fig, ax = blank_ax((6.4, 4.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    nodes = [
        ("① 画像诊断\n识别最短板维度", 50, 89),
        ("② 归因分析\n定位缺失证据类型", 82, 59),
        ("③ 方案生成\n匹配微任务与资源", 70, 15),
        ("④ 数字陪伴\n禾灵儿伴学推送", 30, 15),
        ("⑤ 成效复评\n证据回流与再打分", 18, 59),
    ]
    hw, hh = 14.0, 8.5
    for i, (t, x, y) in enumerate(nodes):
        fc = ACC_PALE if i == 0 else PALE
        ec = ACC if i == 0 else MAIN
        box(ax, x - hw, y - hh, 2 * hw, 2 * hh, t, fc=fc, ec=ec, fs=8.0, radius=0.7)

    order = [0, 1, 2, 3, 4, 0]
    for a, b in zip(order[:-1], order[1:]):
        x1, y1 = nodes[a][1], nodes[a][2]
        x2, y2 = nodes[b][1], nodes[b][2]
        vx, vy = x2 - x1, y2 - y1
        L = np.hypot(vx, vy)
        ux, uy = vx / L, vy / L
        # 椭圆边界外扩 1.5 个单位，避免箭头压在框线上
        r1 = 1.0 / np.hypot(ux / (hw + 1.5), uy / (hh + 1.5))
        arrow(ax, (x1 + ux * r1, y1 + uy * r1),
              (x2 - ux * r1, y2 - uy * r1), color=MID, lw=1.3, ms=9, rad=-0.18)

    box(ax, 36, 42, 28, 18,
        "一生一案\n\n补短板 · 强体验", fc=DEEP, ec=DEEP, fs=9.6,
        tc="white", weight="bold", radius=0.8)
    ax.set_xlim(1, 99)
    ax.set_ylim(3, 100)
    fig.savefig(os.path.join(OUT, "fig7_intervention_loop.png"))
    plt.close(fig)


# =======================================================================
# 图8  分阶段实施路线
# =======================================================================
def fig8():
    tasks = [
        ("指标体系与量规定稿", 0, 3, MID),
        ("全栏目埋点规范与改造", 1, 4, MID),
        ("数据中台与证据库建设", 2, 4, MAIN),
        ("DR-NKT 评分引擎研发", 4, 4, MAIN),
        ("画像前端三端视图开发", 6, 4, MAIN),
        ("干预微任务库与推送", 8, 3, SOFT),
        ("试点班级验证与标定", 9, 4, ACC),
        ("信效度检验与模型调优", 12, 3, ACC),
        ("全校推广与共同体共享", 14, 4, DEEP),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    for i, (name, s, d, c) in enumerate(tasks):
        y = len(tasks) - i - 1
        ax.barh(y, d, left=s, height=0.52, color=c, edgecolor="white", linewidth=0.8)
        ax.text(s + d + 0.25, y, f"{d} 个月", va="center", fontsize=7.0, color=GRAY)
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([t[0] for t in reversed(tasks)], fontsize=8.2)
    ax.set_xticks(range(0, 19, 3))
    ax.set_xticklabels([str(m) for m in range(0, 19, 3)], fontsize=7.6)
    ax.set_xlabel("项目实施月份（月）", fontsize=8.4)
    ax.set_xlim(0, 19.5)
    ax.tick_params(length=2.5)
    ax.grid(axis="x", color=XLGRAY, lw=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)

    phases = [(0, 5, "一期：标准与采集"), (5, 9, "二期：引擎与产品"),
              (9, 15, "三期：试点与检验"), (15, 19.5, "四期：推广")]
    for s, e, lab in phases:
        ax.axvspan(s, e, color=PALE, alpha=0.35, zorder=0)
        ax.text((s + e) / 2, len(tasks) - 0.25, lab, ha="center", va="bottom",
                fontsize=7.6, color=DEEP)
    ax.set_ylim(-0.7, len(tasks) + 0.15)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig8_roadmap.png"))
    plt.close(fig)


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7(); fig8()
    for f in sorted(os.listdir(OUT)):
        print(f, os.path.getsize(os.path.join(OUT, f)))
