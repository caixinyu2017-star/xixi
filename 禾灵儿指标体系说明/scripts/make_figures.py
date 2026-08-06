#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成《禾灵儿数字画像指标体系与评分内核技术说明》中的数据类图件。

概念类示意图（图 1—图 3）由 gpt-image-2 生成，见 scripts/ai_prompts.json；
本脚本只负责必须与真实数值对齐的图件（图 4—图 8），全部由算分内核实时算出，
不写死任何结果，改参数即可复现。
"""
from __future__ import annotations

import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, "/home/user/xixi/禾灵儿德育画像系统")
os.environ.setdefault("HLR_DB", "/tmp/q50.db")
import hlr_portrait as H            # noqa: E402
import kernel_facts as KF           # noqa: E402
FACTS = KF.facts()

DIMS = list(H.DIMS)

plt.rcParams.update({
    "font.sans-serif": ["Noto Sans CJK SC", "WenQuanYi Zen Hei", "DejaVu Sans"],
    "font.family": "sans-serif",
    "axes.unicode_minus": False,
    "savefig.dpi": 300, "figure.dpi": 300,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.06,
    "axes.linewidth": 0.8,
})

DEEP, MAIN, MID, SOFT, PALE = "#0F4C43", "#1F7A6B", "#3D9C87", "#8FC6B5", "#E4F1EC"
GRAY, LGRAY, XLGRAY = "#4B5563", "#9CA3AF", "#E5E7EB"
ACC, ACC_PALE, INK = "#B45309", "#FCEBD8", "#1F2937"

CH_CN = {"dialogue": "文化对话", "enrollment": "文化课程报名", "homework": "课程作业",
         "video": "课程视频", "artifact": "学生作业成果", "agent": "学生自建智能体"}
CH_ORDER = ["dialogue", "homework", "artifact", "agent", "enrollment", "video"]
# 标定前的旧参数（用于对照图）
W_OLD = {
    "dialogue": {"文化体验": .20, "文化认知": .55, "文化志趣": .50, "文化认同": .40, "文化研创": .25},
    "enrollment": {"文化体验": .40, "文化认知": .25, "文化志趣": .60, "文化认同": .25, "文化研创": .10},
    "homework": {"文化体验": .25, "文化认知": .65, "文化志趣": .40, "文化认同": .20, "文化研创": .35},
    "video": {"文化体验": .60, "文化认知": .45, "文化志趣": .35, "文化认同": .20, "文化研创": .05},
    "artifact": {"文化体验": .35, "文化认知": .45, "文化志趣": .30, "文化认同": .40, "文化研创": .85},
    "agent": {"文化体验": .20, "文化认知": .50, "文化志趣": .40, "文化认同": .35, "文化研创": 1.0},
}
CAP_OLD = {"dialogue": 6., "enrollment": 6., "homework": 8., "video": 6.,
           "artifact": 12., "agent": 12.}
K_OLD = {"文化体验": 4.5, "文化认知": 5.0, "文化志趣": 4.5, "文化认同": 4.0, "文化研创": 3.5}


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p)
    plt.close(fig)
    print("  ✓", name)


# =========================================================================
# 图 4  渠道—维度权重矩阵
# =========================================================================
def fig4():
    M = np.array([[H.CHANNEL_WEIGHTS[c][d] for d in DIMS] for c in CH_ORDER])
    fig, ax = plt.subplots(figsize=(7.6, 4.3))
    im = ax.imshow(M, cmap="BuGn", vmin=0, vmax=1.8, aspect="auto")
    ax.set_xticks(range(5)); ax.set_xticklabels(DIMS, fontsize=9.5)
    ax.set_yticks(range(len(CH_ORDER)))
    ax.set_yticklabels([CH_CN[c] for c in CH_ORDER], fontsize=9.5)
    for i in range(len(CH_ORDER)):
        for j in range(5):
            v = M[i, j]
            ax.text(j, i, f"{v:.3f}".rstrip("0").rstrip("."),
                    ha="center", va="center", fontsize=9,
                    color="white" if v > 1.0 else INK)
    # 左侧渠道类型标注
    ax.annotate("", xy=(-0.86, -0.45), xytext=(-0.86, 3.45),
                arrowprops=dict(arrowstyle="-", lw=2.2, color=MAIN))
    ax.text(-0.97, 1.5, "投入型", rotation=90, ha="center", va="center",
            fontsize=9.5, color=MAIN)
    ax.annotate("", xy=(-0.86, 3.55), xytext=(-0.86, 5.45),
                arrowprops=dict(arrowstyle="-", lw=2.2, color=LGRAY))
    ax.text(-0.97, 4.5, "参与型", rotation=90, ha="center", va="center",
            fontsize=9.5, color=GRAY)
    ax.set_xlim(-1.08, 4.55)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    cb = fig.colorbar(im, ax=ax, fraction=0.030, pad=0.02)
    cb.ax.tick_params(labelsize=8, length=2)
    cb.set_label("贡献权重", fontsize=9)
    cb.outline.set_linewidth(0.6)
    save(fig, "fig4_weight_matrix.png")


# =========================================================================
# 图 5  问卷两步换算
# =========================================================================
def fig5():
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.5))

    ax = axes[0]
    sd = np.linspace(0, 0.30, 400)
    for mean, c, ls, lab in ((1.00, DEEP, "-", "问卷均分 1.00"),
                             (0.80, MAIN, "--", "问卷均分 0.80"),
                             (0.72, MID, "-.", "问卷均分 0.72"),
                             (0.65, SOFT, ":", "问卷均分 ≤0.65")):
        pen = H.SL_PENALTY + (1 - H.SL_PENALTY) * np.minimum(1, sd / H.SL_SD_FULL)
        relief = np.clip((H.SL_MEAN_HI - mean) / H.SL_MEAN_SPAN, 0, 1)
        ax.plot(sd, pen + (1 - pen) * relief, color=c, ls=ls, lw=1.7, label=lab)
    ax.axvline(H.SL_SD_FULL, color=ACC, lw=1.0, ls=":")
    ax.text(H.SL_SD_FULL + .007, 0.706, "σ = 0.18\n判定阈值", fontsize=8, color=ACC)
    ax.scatter([0], [H.SL_PENALTY], s=26, color=DEEP, zorder=5)
    ax.annotate("每题都选同一档", xy=(0.002, H.SL_PENALTY), xytext=(0.038, 0.752),
                fontsize=8.5, color=DEEP,
                arrowprops=dict(arrowstyle="->", lw=0.8, color=DEEP))
    ax.set_xlabel("题目级作答标准差 σ", fontsize=9.5)
    ax.set_ylabel("折减系数", fontsize=9.5)
    ax.set_ylim(0.68, 1.03); ax.set_xlim(0, 0.30)
    ax.legend(fontsize=8, frameon=False, loc="upper left",
              bbox_to_anchor=(0.28, 0.62))
    ax.set_title("(a) 第一步：直线作答折减", fontsize=10, pad=7)

    ax = axes[1]
    q = np.linspace(0, 1, 400)
    ax.plot(q, q, color=LGRAY, ls="--", lw=1.3, label="标定前：直接取均分")
    ax.plot(q, H.BASE_MIN + (H.BASE_MAX - H.BASE_MIN) * q ** H.BASE_GAMMA,
            color=DEEP, lw=2.0, label="标定后：窄带压缩")
    ax.axhline(H.BASE_MAX, color=ACC, lw=0.9, ls=":")
    ax.text(0.03, H.BASE_MAX + .022, "问卷天花板 0.50", fontsize=8, color=ACC)
    for key, name, off in (("straight", "每题都选最高档", (-0.30, 0.29)),
                           ("high", "认真作答、自评偏高", (-0.36, -0.20))):
        pen, y, mean, sd, x = FACTS["qex"][key]
        ax.scatter([x], [y], s=28, color=ACC, zorder=6)
        ax.annotate(f"{name} {y:.2f}", xy=(x, y), xytext=(x + off[0], y + off[1]),
                    fontsize=8.5, color=ACC,
                    arrowprops=dict(arrowstyle="->", lw=0.8, color=ACC))
    ax.set_xlabel("折减后的作答强度", fontsize=9.5)
    ax.set_ylabel("初始得分 B", fontsize=9.5)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.set_title("(b) 第二步：窄带压缩", fontsize=10, pad=7)

    for ax in axes:
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=8.5, length=2.5)
    fig.tight_layout()
    save(fig, "fig5_questionnaire_mapping.png")


# =========================================================================
# 图 6  维度合成的饱和函数
# =========================================================================
def fig6():
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.5))
    A = np.linspace(0, 30, 500)

    ax = axes[0]
    for k, c, ls in ((3.5, LGRAY, "--"), (5.0, SOFT, "-."),
                     (6.5, MAIN, "-"), (7.0, DEEP, "-")):
        ax.plot(A, 0.30 + 0.70 * (1 - np.exp(-A / k)), color=c, ls=ls, lw=1.7,
                label=f"κ = {k}")
    ax.axhline(1.0, color=ACC, lw=0.9, ls=":")
    ax.text(21.5, 1.012, "封顶 1.0", fontsize=8, color=ACC)
    ax.axhline(0.30, color=GRAY, lw=0.8, ls=":")
    ax.text(0.4, 0.245, "初始得分 B = 0.30", fontsize=8, color=GRAY)
    ax.set_xlabel("有效证据量 $A_d$", fontsize=9.5)
    ax.set_ylabel("维度得分 $S_d$", fontsize=9.5)
    ax.set_ylim(0, 1.09); ax.set_xlim(0, 30)
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    ax.set_title("(a) 饱和常数 κ 的作用", fontsize=10, pad=7)

    ax = axes[1]
    for b, c, ls in ((0.20, SOFT, "-."), (0.30, MID, "--"),
                     (0.40, MAIN, "-"), (0.55, DEEP, "-")):
        ax.plot(A, b + (1 - b) * (1 - np.exp(-A / 6.5)), color=c, ls=ls, lw=1.7,
                label=f"B = {b:.2f}")
    ax.axhline(1.0, color=ACC, lw=0.9, ls=":")
    ax.set_xlabel("有效证据量 $A_d$", fontsize=9.5)
    ax.set_ylabel("维度得分 $S_d$", fontsize=9.5)
    ax.set_ylim(0, 1.09); ax.set_xlim(0, 30)
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    ax.set_title("(b) 初始得分 B 的作用（κ = 6.5）", fontsize=10, pad=7)

    for ax in axes:
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=8.5, length=2.5)
    fig.tight_layout()
    save(fig, "fig6_saturation.png")


# =========================================================================
# 图 7  标定前后对照（真实数据实算）
# =========================================================================
def _raw_all():
    cx = H.STORE.conn()
    raw = {}
    for r in cx.execute("SELECT sid,channel,dim,SUM(amount*quality*relevance) s "
                        "FROM evidences WHERE grade='大一' GROUP BY 1,2,3"):
        raw.setdefault(r['sid'], {}).setdefault(r['channel'], {})[r['dim']] = float(r['s'] or 0)
    return raw


def _cci(raw_s, W, CAP, K, B):
    tot = 0.0
    for d in DIMS:
        a = 0.0
        for ch, m in raw_s.items():
            if ch in W:
                a += min(m.get(d, 0.0) * W[ch][d], CAP.get(ch, 8.0))
        tot += min(1.0, B + (1 - B) * (1 - math.exp(-a / K[d])))
    return tot / 5


def fig7():
    raw = _raw_all()
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.5))

    # (a) 单位行为的证据当量：直接反映"计量是否与投入强度对齐"
    ORD = KF.UNIT_ORDER
    eo = [FACTS["eqv"][c][0] for c in ORD]
    en = [FACTS["eqv"][c][1] for c in ORD]
    ax = axes[0]
    y = np.arange(len(ORD))
    ax.barh(y + 0.19, eo, height=0.36, color=XLGRAY, edgecolor=LGRAY, lw=0.6,
            label="标定前")
    ax.barh(y - 0.19, en, height=0.36, color=MID, edgecolor=DEEP, lw=0.6,
            label="标定后")
    hi = max(max(eo), max(en))
    for i in range(len(ORD)):
        ax.text(eo[i] + hi * .015, i + 0.19, f"{eo[i]:.2f}", va="center",
                fontsize=7.8, color=GRAY)
        ax.text(en[i] + hi * .015, i - 0.19, f"{en[i]:.2f}", va="center",
                fontsize=7.8, color=DEEP)
    ax.set_yticks(y); ax.set_yticklabels([KF.UNIT_LABEL[c] for c in ORD], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("该行为折算出的证据当量（五维合计）", fontsize=9.5)
    ax.set_xlim(0, hi * 1.30)
    ax.legend(fontsize=8, frameon=False, loc="center right",
              bbox_to_anchor=(1.0, 0.62))
    ax.set_title("(a) 单位行为的证据当量", fontsize=10, pad=7)

    # (b) 综合指数分布
    ax = axes[1]
    old, new = FACTS["old_all"], FACTS["new_all"]
    bins = np.linspace(0.25, 0.85, 49)
    ax.hist(old, bins=bins, color=XLGRAY, edgecolor=LGRAY, lw=0.4, label="标定前")
    ax.hist(new, bins=bins, color=MID, alpha=.88, edgecolor=DEEP, lw=0.4, label="标定后")
    ax.set_ylim(0, max(np.histogram(new, bins=bins)[0]) * 1.20)
    top = ax.get_ylim()[1]
    for v, c in ((np.median(old), GRAY), (np.median(new), DEEP)):
        ax.axvline(v, color=c, ls="--", lw=1.1)
    ax.annotate(f"中位 {np.median(old):.2f}", xy=(np.median(old), top * .72),
                xytext=(np.median(old) + .045, top * .72), fontsize=8, color=GRAY,
                va="center", arrowprops=dict(arrowstyle="->", lw=0.7, color=GRAY))
    ax.annotate(f"中位 {np.median(new):.2f}", xy=(np.median(new), top * .86),
                xytext=(np.median(new) + .045, top * .86), fontsize=8, color=DEEP,
                va="center", arrowprops=dict(arrowstyle="->", lw=0.7, color=DEEP))
    ax.set_xlabel("综合文化素养指数 CCI", fontsize=9.5)
    ax.set_ylabel("学生人数", fontsize=9.5)
    ax.legend(fontsize=8, frameon=False, loc="upper right")
    ax.set_title("(b) 大一全体 5307 人的分数分布（尚未做问卷）", fontsize=10, pad=7)

    for ax in axes:
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=8.5, length=2.5)
    fig.tight_layout()
    save(fig, "fig7_calibration_contrast.png")
    return old, new


# =========================================================================
# 图 8  发展性等级阶梯与两类学生的四年轨迹
# =========================================================================
def fig8():
    act, pas = FACTS["act"], FACTS["pas"]

    fig, ax = plt.subplots(figsize=(7.8, 4.0))
    x = np.arange(4)
    cuts = [("A 引领级", H.LEVEL_CUTS[0], "#C4E3D8"),
            ("B 胜任级", H.LEVEL_CUTS[1], "#DBEDE6"),
            ("C 发展级", H.LEVEL_CUTS[2], "#EDF5F2"),
            ("D 起步级", 0.0, "#FFFFFF")]
    for g in range(4):
        for i, (lab, c0, col) in enumerate(cuts):
            lo = c0 + (H.LEVEL_STEP * g if i < 3 else 0)
            hi = (1.06 if i == 0 else cuts[i - 1][1] + H.LEVEL_STEP * g)
            ax.add_patch(Rectangle((g - .5, lo), 1.0, hi - lo, facecolor=col,
                                   edgecolor="white", lw=1.0, zorder=0))
    for i, (lab, c0, col) in enumerate(cuts):
        lo = c0 + (H.LEVEL_STEP * 3 if i < 3 else 0.20)
        hi = (1.06 if i == 0 else cuts[i - 1][1] + H.LEVEL_STEP * 3)
        ax.text(3.58, (lo + hi) / 2, lab, fontsize=8.5, va="center",
                color=DEEP if i < 3 else GRAY)

    ax.plot(x, act, "-o", color=DEEP, lw=2.0, ms=6, label="持续投入的学生")
    ax.plot(x, pas, "s--", color=ACC, lw=2.0, ms=5.5, label="只刷问卷、之后基本不用")
    for i in range(4):
        ax.annotate(f"{act[i]:.2f}", (i, act[i]), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=8.5, color=DEEP)
        ax.annotate(f"{pas[i]:.2f}", (i, pas[i]), textcoords="offset points",
                    xytext=(0, -15), ha="center", fontsize=8.5, color=ACC)
    ax.set_xticks(x); ax.set_xticklabels(list(H.GRADES), fontsize=10)
    ax.set_xlim(-0.5, 4.15); ax.set_ylim(0.20, 1.06)
    ax.set_ylabel("综合文化素养指数 CCI", fontsize=9.5)
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=9, length=2.5)
    fig.tight_layout()
    save(fig, "fig8_growth_ladder.png")
    return act, pas


if __name__ == "__main__":
    print("生成数据类图件：")
    fig4(); fig5(); fig6()
    old, new = fig7()
    act, pas = fig8()
    print(f"\n核对：标定前中位 {np.median(old):.3f} → 标定后 {np.median(new):.3f}；"
          f"最高 {max(old):.3f} → {max(new):.3f}")
    print(f"      持续投入 {[round(v,3) for v in act]}")
    print(f"      基本不用 {[round(v,3) for v in pas]}")
