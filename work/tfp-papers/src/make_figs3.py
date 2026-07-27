# -*- coding: utf-8 -*-
"""生成两篇论文的插图。全部数据来自 p3_sim.py / p4_sim.py 的估计输出。"""
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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "results")
FIG = os.path.join(ROOT, "figs")
os.makedirs(FIG, exist_ok=True)

p3 = json.load(open(os.path.join(RES, "p3_results.json"), encoding="utf-8"))
p4 = json.load(open(os.path.join(RES, "p4_results.json"), encoding="utf-8"))

# ============ 论文3 图1：事件研究（平行趋势检验与动态效应） ============
# 体例：以处理前一期（e = −1）为基期，其系数按识别所需的归一化约束设为 0，
# 图中以空心标记单独标示；端点为分箱估计（e ≤ −5 与 e ≥ 6）；
# 误差棒为基于城市层面聚类稳健标准误的 95% 置信区间。
EMIN, EMAX, BASE = -5, 6, -1
ev = pd.DataFrame(p3["event_study_sa"]).sort_values("e")
cs = pd.DataFrame(p3["cs_dynamic"]).sort_values("e")
if BASE not in set(cs["e"]):                       # 补回被归一化的基期点
    cs = pd.concat([cs, pd.DataFrame([{"e": BASE, "coef": 0.0, "se": 0.0,
                                       "supt_lo": 0.0, "supt_hi": 0.0}])],
                   ignore_index=True).sort_values("e")

pt = p3["pretrend_joint"]["wald_aggregated"]
BMEAN = p3["base_period_mean"]
lo = min(ev["supt_lo"].min(), cs["supt_lo"].min())
hi = max(ev["supt_hi"].max(), cs["supt_hi"].max())
pad = 0.20 * (hi - lo)
YLIM = (lo - 0.45 * pad, hi + pad)
MINUS = "-"          # 绘图字体缺少 U+2212，标签统一用半角连字符


def _lab(e):
    return f"{MINUS}{-e}" if e < 0 else str(e)


XTICKS = list(range(EMIN, EMAX + 1))
XLAB = ([f"≤{_lab(EMIN)}"] + [_lab(e) for e in range(EMIN + 1, EMAX)]
        + [f"≥{EMAX}"])

PANELS = [
    dict(ax=0, df=ev, color=BLUE, marker="o",
         title="(a) Sun-Abraham 交互加权估计量"),
    dict(ax=1, df=cs, color=RED, marker="s",
         title="(b) Callaway-Sant'Anna 双重稳健估计量"),
]

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.3), dpi=300, sharey=True)
for cfg in PANELS:
    ax, d, c = axes[cfg["ax"]], cfg["df"], cfg["color"]
    ax.axvspan(EMIN - 0.6, -0.5, color="0.92", zorder=0)     # 政策实施前区间
    ax.axhline(0, color="k", lw=0.8, zorder=1)
    ax.axvline(-0.5, color="0.35", ls="--", lw=1.0, zorder=1)
    est = d[d["e"] != BASE]
    for seg in (d[d["e"] <= BASE - 1], d[d["e"] >= BASE + 1]):  # 基期处断开
        ax.fill_between(seg["e"], seg["supt_lo"], seg["supt_hi"],
                        color=c, alpha=0.13, lw=0, zorder=1)
    ax.errorbar(est["e"], est["coef"], yerr=1.96 * est["se"], fmt="none",
                ecolor=GREY, elinewidth=1.0, capsize=2.5, zorder=2)
    ax.plot(d["e"], d["coef"], "-", lw=1.3, color=c, zorder=3)
    ax.plot(est["e"], est["coef"], cfg["marker"], ms=4.2, color=c,
            mec=c, mfc=c, zorder=4)
    ax.plot([BASE], [0.0], cfg["marker"], ms=5.6, mec=c, mfc="white",
            mew=1.4, zorder=5)                                # 基期：空心标记
    ax.annotate("基期", xy=(BASE, 0.0), xytext=(BASE, YLIM[0] + 0.30 * pad),
                fontsize=7.4, color="0.25", ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color="0.55", lw=0.7,
                                shrinkA=1, shrinkB=4))
    ax.text(-0.32, YLIM[1] - 1.05 * pad, "政策实施", fontsize=7.4,
            color="0.25", ha="left", va="top")
    ax.set_xlim(EMIN - 0.6, EMAX + 0.6)
    ax.set_ylim(*YLIM)
    ax.set_xticks(XTICKS)
    ax.set_xticklabels(XLAB, fontsize=7.6)
    ax.set_xlabel("相对政策实施年份（年）", fontsize=9)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_title(cfg["title"], fontsize=9.5, y=-0.36)

axes[0].set_ylabel("估计系数", fontsize=9)
axes[0].text(EMIN - 0.4, YLIM[1] - 0.06 * pad,
             "前期系数联合为零的Wald检验\n"
             f"$\\chi^2$({pt['df']})={pt['stat']:.4f}，P={pt['p']:.4f}",
             fontsize=7.4, color="0.15", ha="left", va="top", linespacing=1.5)
axes[1].text(EMAX + 0.45, YLIM[0] + 0.16 * pad,
             f"基期被解释变量均值＝{BMEAN:.4f}", fontsize=7.4, color="0.15",
             ha="right", va="bottom")
fig.tight_layout(rect=[0, 0.07, 1, 1])
fig.savefig(os.path.join(FIG, "p3_fig1.png"), bbox_inches="tight")
plt.close(fig)

# ============ 论文3 图2：随机化推断安慰剂检验 ============
pl = pd.read_csv(os.path.join(RES, "p3_placebo.csv"))["b"].to_numpy()
actual = p3["placebo"]["actual"]

fig, ax = plt.subplots(figsize=(5.4, 3.1), dpi=300)
grid = np.linspace(pl.min() - 0.004, max(pl.max(), actual) + 0.004, 400)
h = 1.06 * pl.std(ddof=1) * len(pl) ** (-0.2)
dens = np.exp(-0.5 * ((grid[:, None] - pl[None, :]) / h) ** 2).sum(1) / (
    len(pl) * h * np.sqrt(2 * np.pi))
ax.plot(grid, dens, color=BLUE, lw=1.5)
ax.fill_between(grid, 0, dens, color=BLUE, alpha=0.14)
ax.scatter(pl, np.full(len(pl), -0.6), s=3, color=GREY, alpha=0.35,
           marker="|", linewidths=0.6)
ax.axvline(actual, color=RED, ls="--", lw=1.4)
ax.annotate(f"基准估计值 {actual:.4f}", xy=(actual, dens.max() * 0.72),
            xytext=(actual - 0.019, dens.max() * 0.86), fontsize=8, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=0.9))
ax.axvline(0, color="k", lw=0.8)
ax.set_xlabel("安慰剂估计系数", fontsize=9)
ax.set_ylabel("核密度", fontsize=9)
ax.tick_params(labelsize=8)
ax.set_ylim(bottom=-3)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "p3_fig2.png"), bbox_inches="tight")
plt.close(fig)

# ============ 论文4 图1：2023 年全要素生产率的 Moran 散点图 ============
ms = pd.read_csv(os.path.join(RES, "p4_moran_scatter.csv"))
I2023 = [m for m in p4["moran"] if m["year"] == 2023][0]["I_tfp"]

fig, ax = plt.subplots(figsize=(5.0, 4.4), dpi=300)
cols = {0: BLUE, 1: "#4E9A51", 2: RED}
labs = {0: "东部地区", 1: "中部地区", 2: "西部地区"}
for k in (0, 1, 2):
    s = ms[ms["region"] == k]
    ax.scatter(s["z"], s["Wz"], s=26, color=cols[k], label=labs[k],
               edgecolors="white", linewidths=0.5, zorder=3)
xg = np.linspace(ms["z"].min() - 0.3, ms["z"].max() + 0.3, 50)
ax.plot(xg, I2023 * xg, color="k", lw=1.2, zorder=2)
ax.axhline(0, color=GREY, lw=0.8, ls="--")
ax.axvline(0, color=GREY, lw=0.8, ls="--")
for _, r in ms.iterrows():
    ax.annotate(r["province"], (r["z"], r["Wz"]), fontsize=6.2,
                xytext=(2.5, 2.5), textcoords="offset points", color="#333333")
ax.set_xlabel("全要素生产率（标准化）", fontsize=9)
ax.set_ylabel("邻近省份全要素生产率的空间滞后", fontsize=9)
ax.tick_params(labelsize=8)
ax.legend(fontsize=7.5, frameon=False, loc="upper left")
ax.text(0.98, 0.02, f"Moran's I = {I2023:.4f}", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=8.5)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "p4_fig1.png"), bbox_inches="tight")
plt.close(fig)

# ============ 论文4 图2：门槛值估计的似然比统计量曲线 ============
lr = pd.read_csv(os.path.join(RES, "p4_threshold_lr.csv"))
crit = 7.35                                     # 95% 置信水平下的临界值
titles = {1: "(a) 第一阶段：单一门槛搜索", 2: "(b) 第二阶段：给定第一门槛的搜索"}
ci = {}

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1), dpi=300)
for k, stage in enumerate((1, 2)):
    s = lr[lr["stage"] == stage].sort_values("gamma")
    ghat = float(s.loc[s["LR"].idxmin(), "gamma"])
    below = s[s["LR"] <= crit]["gamma"]
    ci[stage] = (float(below.min()), float(below.max()))
    ax = axes[k]
    ax.plot(s["gamma"], s["LR"], color=BLUE, lw=1.5)
    ax.axhline(crit, color=RED, ls="--", lw=1.1)
    ax.text(s["gamma"].min(), crit, " 95%临界值7.35", fontsize=7.2, color=RED,
            va="bottom", ha="left")
    ax.axvline(ghat, color=GREY, ls=":", lw=1.0)
    ax.annotate(f"γ={ghat:.4f}", xy=(ghat, s["LR"].max() * 0.92), fontsize=7.8,
                ha="center", color="#333333")
    ax.set_xlabel("研发强度门槛值（%）", fontsize=9)
    ax.set_ylabel("似然比统计量", fontsize=9)
    ax.tick_params(labelsize=8)
    ax.set_title(titles[stage], fontsize=9.5, y=-0.34)

fig.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig(os.path.join(FIG, "p4_fig2.png"), bbox_inches="tight")
plt.close(fig)
print("门槛值的95%置信区间：", {k: (round(v[0], 4), round(v[1], 4))
                               for k, v in ci.items()})

print("figures written to", FIG)
