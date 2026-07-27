# -*- coding: utf-8 -*-
"""生成两篇青年就业论文的插图。全部数据来自 p1_sim.py / p2_sim.py 的估计输出。

制图规范（见仓库根目录 STYLE.md 第三节）：
  1. **图例一律不进入数据区**——或置于绘图区上方横排，或直接在曲线末端标注，
     以避免遮挡数据；图元含义在正文的图注中写明。
  2. 分панель标题由 fig.text 统一置于图底同一水平线上，避免与横轴标签相撞。
  3. 误差棒统一表示 95% 置信区间；数值标签一律置于误差棒之外，
     并按端点方向留出足够的坐标余量，确保不与刻度标签重叠。
  4. 全图共用一套配色，同一颜色在不同分图中含义一致。
"""
import json
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_manager.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False
BLUE, RED, GREY = "#3B6EA5", "#C0504D", "#7F7F7F"
GREEN, ORANGE, DARK = "#4E8A45", "#D98A21", "#333333"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figs")
os.makedirs(FIG, exist_ok=True)

CAP = 9.5          # 分图标题字号
LEG = 7.6          # 图例字号


def top_legend(ax, ncol, handles=None, labels=None):
    """把图例横排放在绘图区正上方，彻底避开数据区。"""
    kw = dict(loc="lower left", bbox_to_anchor=(0.0, 1.01), ncol=ncol,
              fontsize=LEG, frameon=False, handlelength=1.9,
              columnspacing=1.3, handletextpad=0.5, borderaxespad=0.0)
    return ax.legend(handles, labels, **kw) if handles else ax.legend(**kw)


def panel_titles(fig, texts, y=0.015):
    """分图标题统一置于图底同一水平线，避免与各自横轴标签相撞。"""
    for x, t in texts:
        fig.text(x, y, t, ha="center", va="bottom", fontsize=CAP)


def clean(ax, keep_right=False):
    ax.spines["top"].set_visible(False)
    if not keep_right:
        ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)


# ================= 论文1 图1：数字经济与青年高质量就业的演进 =================
tr = pd.read_csv(f"{OUT}/p1_trend.csv")
trg = pd.read_csv(f"{OUT}/p1_trend_region.csv")
names = {0: "东部地区", 1: "中部地区", 2: "西部地区"}
marks = {0: "o", 1: "s", 2: "^"}
cols = {0: BLUE, 1: ORANGE, 2: GREEN}
Y0, Y1 = int(tr["year"].min()), int(tr["year"].max())

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1), dpi=300)
ax = axes[0]
l1, = ax.plot(tr["year"], tr["dig"], "-o", ms=3.6, lw=1.5, color=BLUE,
              label="数字经济发展水平（左轴）")
ax2 = ax.twinx()
l2, = ax2.plot(tr["year"], tr["yqe"], "--s", ms=3.6, lw=1.5, color=RED,
               label="青年高质量就业水平（右轴）")
ax.set_xlabel("年份", fontsize=9)
ax.set_ylabel("数字经济发展水平", fontsize=9, color=BLUE)
ax2.set_ylabel("青年高质量就业水平", fontsize=9, color=RED)
ax.set_xticks(range(Y0, Y1 + 1, 2))
clean(ax, keep_right=True)
clean(ax2, keep_right=True)
ax.grid(axis="y", ls=":", lw=0.6, color="0.85")
ax.set_axisbelow(True)
top_legend(ax, 1, [l1, l2], [l1.get_label(), l2.get_label()])

ax = axes[1]
for k, nm in names.items():
    s = trg[trg["region"] == k]
    ax.plot(s["year"], s["yqe"], f"-{marks[k]}", ms=3.4, lw=1.4,
            color=cols[k], label=nm)
ax.set_xlabel("年份", fontsize=9)
ax.set_ylabel("青年高质量就业水平", fontsize=9)
ax.set_xticks(range(Y0, Y1 + 1, 2))
clean(ax)
ax.grid(axis="y", ls=":", lw=0.6, color="0.85")
ax.set_axisbelow(True)
top_legend(ax, 3)

fig.tight_layout(rect=[0, 0.08, 1, 1])
panel_titles(fig, [(0.28, "(a) 总体演进趋势"), (0.78, "(b) 分区域演进趋势")])
fig.savefig(os.path.join(FIG, "p1_fig1.png"), dpi=300, bbox_inches="tight")
plt.close(fig)

# ================= 论文1 图2：门槛效应的似然比与分区间效应 =================
res1 = json.load(open(f"{OUT}/p1_results.json", encoding="utf-8"))
ssr = pd.read_csv(f"{OUT}/p1_threshold_ssr.csv")
th = res1["threshold"]

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1), dpi=300)
ax = axes[0]
lr = (ssr["ssr"] - ssr["ssr"].min()) / (ssr["ssr"].min() / 3336)
lr_line, = ax.plot(ssr["gamma"], lr, lw=1.5, color=BLUE, label="似然比统计量 $LR(\\gamma)$")
crit = ax.axhline(7.35, ls="--", lw=1.0, color=RED, label="95%置信水平临界值 7.35")
gam = ax.axvline(th["gamma1"], ls=":", lw=1.2, color=GREY,
                 label=f"门槛估计值 $\\hat{{\\gamma}}_1$={th['gamma1']:.3f}")
ax.set_xlabel("门槛变量取值（人力资本水平）", fontsize=9)
ax.set_ylabel("似然比统计量 $LR$", fontsize=9)
ax.set_ylim(-12, lr.max() * 1.10)
clean(ax)
top_legend(ax, 1, [lr_line, crit, gam],
           [lr_line.get_label(), crit.get_label(), gam.get_label()])

ax = axes[1]
segs = ["_r1", "_r2", "_r3"]
labels = [f"区间Ⅰ\n(hc≤{th['gamma1']:.2f})",
          f"区间Ⅱ\n({th['gamma1']:.2f}<hc≤{th['gamma2']:.2f})",
          f"区间Ⅲ\n(hc>{th['gamma2']:.2f})"]
vals = [float(th["double"][s]["coef"].rstrip("*")) for s in segs]
tvals = [abs(float(th["double"][s]["t"].strip("()"))) for s in segs]
ses = [abs(v) / t if t > 0 else 0 for v, t in zip(vals, tvals)]
sig = [abs(v / (se or 1)) >= 1.96 for v, se in zip(vals, ses)]
bar_c = [BLUE if s else GREY for s in sig]
ax.bar(range(3), vals, yerr=[1.96 * s for s in ses], capsize=4,
       color=bar_c, width=0.56, error_kw=dict(lw=0.9, ecolor=DARK))
lo = min(v - 1.96 * s for v, s in zip(vals, ses))
hi = max(v + 1.96 * s for v, s in zip(vals, ses))
span = hi - lo
ax.set_ylim(lo - 0.34 * span, hi + 0.20 * span)
for i, (v, se, sh) in enumerate(zip(vals, ses,
                                    [th["share_r1"], th["share_r2"], th["share_r3"]])):
    ax.text(i, v + 1.96 * se + 0.035 * span, f"{v:.4f}", ha="center", fontsize=8)
    ax.text(i, lo - 0.28 * span, f"样本占比{sh * 100:.1f}%", ha="center",
            fontsize=7, color=GREY)
ax.axhline(0, color="0.35", lw=0.8)
ax.set_xticks(range(3))
ax.set_xticklabels(labels, fontsize=7.6)
ax.set_ylabel("数字经济的估计系数", fontsize=9)
clean(ax)

fig.tight_layout(rect=[0, 0.08, 1, 1])
panel_titles(fig, [(0.28, "(a) 门槛值的似然比检验"), (0.78, "(b) 分区间的边际效应")])
fig.savefig(os.path.join(FIG, "p1_fig2.png"), dpi=300, bbox_inches="tight")
plt.close(fig)

# ================= 论文2 图1：人工智能与青年就业的U型关系 =================
res2 = json.load(open(f"{OUT}/p2_results.json", encoding="utf-8"))
p2 = pd.read_csv(f"{OUT}/p2_panel.csv")
mb = res2["baseline"][-1]
b1, b2 = mb["ai_std"]["b"], mb["ai_sq"]["b"]
turn = res2["ushape"]["turn_std"]

# 去除固定效应后的部分残差图
d = p2.copy()
d["_y"] = d["lnyemp"] - d.groupby("pid")["lnyemp"].transform("mean") \
          - d.groupby("year")["lnyemp"].transform("mean") + d["lnyemp"].mean()

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1), dpi=300)
ax = axes[0]
pts = ax.scatter(d["ai_std"], d["_y"], s=5, alpha=0.28, color=BLUE, lw=0,
                 label="城市—年份观测值")
xs = np.linspace(d["ai_std"].min(), d["ai_std"].max(), 200)
fit = b1 * xs + b2 * xs ** 2
fit = fit - fit.mean() + d["_y"].mean()
curve, = ax.plot(xs, fit, lw=2.0, color=RED, label="二次项拟合曲线")
vline = ax.axvline(turn, ls="--", lw=1.1, color=GREY,
                   label=f"拐点 $\\tau^*$={turn:.3f}")
ax.set_xlabel("人工智能应用水平（标准化）", fontsize=9)
ax.set_ylabel("青年就业规模（去除固定效应）", fontsize=9)
clean(ax)
top_legend(ax, 2, [pts, curve, vline],
           [pts.get_label(), curve.get_label(), vline.get_label()])

ax = axes[1]
st = res2["structure"]
items = ["青年高技能就业占比", "青年低技能就业占比", "常规任务岗位占比", "新兴数字职业占比"]
vals = [st[k]["b"] for k in items]
tv = [abs(float(st[k]["t"].strip("()"))) for k in items]
ses = [abs(v) / t for v, t in zip(vals, tv)]
cols_b = [BLUE if v > 0 else RED for v in vals]
ax.barh(range(4), vals, xerr=[1.96 * s for s in ses], capsize=3.5,
        color=cols_b, height=0.55, error_kw=dict(lw=0.9, ecolor=DARK))
ends = [v + (1.96 * s if v > 0 else -1.96 * s) for v, s in zip(vals, ses)]
lim = max(abs(e) for e in ends)
pad = lim * 0.52                      # 为数值标签预留的坐标余量
ax.set_xlim(-lim - pad, lim + pad)
for i, (v, e) in enumerate(zip(vals, ends)):
    off = lim * 0.05
    ax.text(e + (off if v > 0 else -off), i, f"{v:.3f}", va="center",
            ha="left" if v > 0 else "right", fontsize=7.6)
ax.set_yticks(range(4))
ax.set_yticklabels(["青年高技能\n就业占比", "青年低技能\n就业占比",
                    "常规任务\n岗位占比", "新兴数字\n职业占比"], fontsize=7.6)
ax.axvline(0, color="0.35", lw=0.8)
ax.set_xlabel("人工智能应用的估计系数", fontsize=9)
ax.invert_yaxis()
clean(ax)

fig.tight_layout(rect=[0, 0.08, 1, 1])
panel_titles(fig, [(0.28, "(a) U型关系与拐点"), (0.78, "(b) 就业结构效应")])
fig.savefig(os.path.join(FIG, "p2_fig1.png"), dpi=300, bbox_inches="tight")
plt.close(fig)

# ================= 论文2 图2：调节效应与分位数效应 =================
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1), dpi=300)
ax = axes[0]
mod = res2["moderation"]["教育发展水平"]
bx = float(mod["x"]["coef"].rstrip("*"))
bx2 = float(mod["x2"]["coef"].rstrip("*"))
binter = float(mod["inter"]["coef"].rstrip("*"))
xs = np.linspace(-2.0, 2.4, 120)
# 直接在曲线末端标注，取代图例，避免遮挡曲线
for zval, style, color, lab in [(-1.0, ":", RED, "低教育水平"),
                                (0.0, "-", DARK, "平均教育水平"),
                                (1.0, "--", BLUE, "高教育水平")]:
    ys = bx * xs + bx2 * xs ** 2 + binter * xs * zval
    ys = ys - ys[0]
    ax.plot(xs, ys, style, lw=1.6, color=color)
    ax.text(xs[-1] + 0.12, ys[-1], lab, fontsize=LEG, color=color,
            va="center", ha="left")
ax.set_xlim(-2.15, 4.35)
ax.set_xlabel("人工智能应用水平（标准化）", fontsize=9)
ax.set_ylabel("青年就业规模的相对变化", fontsize=9)
ax.set_xticks([-2, -1, 0, 1, 2])
clean(ax)

ax = axes[1]
q = res2["quantile"]
qs = list(q.keys())
b1q = [float(q[k]["x"].rstrip("*")) for k in qs]
b2q = [float(q[k]["x2"].rstrip("*")) for k in qs]
x = np.arange(len(qs))
ax.plot(x, b1q, "-o", ms=4.4, lw=1.5, color=RED, label="一次项系数 $\\beta_1$")
ax.plot(x, b2q, "-s", ms=4.4, lw=1.5, color=BLUE, label="二次项系数 $\\beta_2$")
ax.axhline(0, color="0.35", lw=0.8)
ax.set_xticks(x)
ax.set_xticklabels([k.replace("Q", "第") + "分位" for k in qs], fontsize=7.6)
ax.set_ylabel("估计系数", fontsize=9)
clean(ax)
top_legend(ax, 2)

fig.tight_layout(rect=[0, 0.08, 1, 1])
panel_titles(fig, [(0.28, "(a) 教育发展水平的调节作用"),
                   (0.78, "(b) 分位数回归的系数变化")])
fig.savefig(os.path.join(FIG, "p2_fig2.png"), dpi=300, bbox_inches="tight")
plt.close(fig)

print("figures done: p1_fig1, p1_fig2, p2_fig1, p2_fig2")
