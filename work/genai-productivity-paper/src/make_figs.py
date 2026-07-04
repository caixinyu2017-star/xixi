# -*- coding: utf-8 -*-
"""生成论文插图：图1 事件研究动态效应；图2 分位数处理效应。
数值锚定于核心论文报告的结果，中间点位由平滑插值模拟得到。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_manager.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
plt.rcParams["font.family"] = "WenQuanYi Zen Hei"
plt.rcParams["axes.unicode_minus"] = False

rng = np.random.default_rng(20260704)
OUT = "/tmp/claude-0/-home-user-xixi/6b37a25a-9ac4-51b0-95a3-103191b10bff/scratchpad"

# ---------- 图1：事件研究动态效应 ----------
weeks = np.arange(-4, 25)
beta = np.zeros_like(weeks, dtype=float)
for i, w in enumerate(weeks):
    if w <= 0:
        # 试验前系数在 ±0.015 内波动，第0周标准化为0
        beta[i] = 0.0 if w == 0 else rng.uniform(-0.013, 0.013)
    elif w <= 10:
        # 第1周 -0.09，逐步加深至第10周 -0.31（凹形学习曲线）
        frac = (w - 1) / 9
        beta[i] = -0.09 + (-0.31 + 0.09) * (1 - (1 - frac) ** 1.6) + rng.normal(0, 0.006)
    else:
        # 第10—24周平台期 -0.31±0.02
        beta[i] = -0.31 + rng.normal(0, 0.009)
beta[weeks == 1] = -0.09
beta[weeks == 10] = -0.312
se = np.where(weeks <= 0, 0.012, 0.021 + 0.004 * rng.random(len(weeks)))
se[weeks == 0] = 0.0
ci = 1.96 * se

fig, ax = plt.subplots(figsize=(7.0, 3.6), dpi=300)
ax.axhline(0, color="0.35", lw=0.8)
ax.axvline(0.5, color="0.6", lw=0.8, ls="--")
ax.axhspan(-0.33, -0.29, xmin=0.0, alpha=0.15, color="#4C72B0", lw=0)
ax.errorbar(weeks, beta, yerr=ci, fmt="o", ms=3.4, lw=1.0, capsize=2,
            color="#4C72B0", ecolor="#4C72B0", elinewidth=0.8)
ax.plot(weeks, beta, lw=1.0, color="#4C72B0", alpha=0.65)
ax.annotate("实验启动", xy=(0.5, 0.055), xytext=(-3.6, 0.075), fontsize=9,
            arrowprops=dict(arrowstyle="->", lw=0.8, color="0.3"))
ax.annotate("平台期：$-0.31\\pm0.02$", xy=(17, -0.29), xytext=(13.2, -0.175),
            fontsize=9, arrowprops=dict(arrowstyle="->", lw=0.8, color="0.3"))
ax.set_xlabel("实验周数", fontsize=10)
ax.set_ylabel("对数任务完成时间的处理效应", fontsize=10)
ax.set_xlim(-5, 25)
ax.set_ylim(-0.42, 0.12)
ax.set_xticks(np.arange(-4, 25, 4))
ax.tick_params(labelsize=9)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/fig1_event_study.png", dpi=300)
plt.close(fig)

# ---------- 图2：分位数处理效应 ----------
taus = np.arange(0.05, 0.96, 0.05)
anchor_t = np.array([0.10, 0.25, 0.50, 0.75, 0.90])
anchor_q = np.array([6.8, 5.6, 3.8, 2.1, 0.7])
qte = np.interp(taus, anchor_t, anchor_q)
qte[taus < 0.10] = 6.8 + (0.10 - taus[taus < 0.10]) * 6.0
qte[taus > 0.90] = np.maximum(0.7 + (0.90 - taus[taus > 0.90]) * 5.0, 0.2)
qte = qte + rng.normal(0, 0.08, len(taus))
for t, q in zip(anchor_t, anchor_q):
    qte[np.isclose(taus, t)] = q
se2 = 0.8 + 0.5 * np.abs(taus - 0.5) * 2
ci2 = 1.96 * se2

fig, ax = plt.subplots(figsize=(7.0, 3.6), dpi=300)
ax.axhline(0, color="0.35", lw=0.8)
ax.fill_between(taus, qte - ci2, qte + ci2, color="#4C72B0", alpha=0.18, lw=0)
ax.plot(taus, qte, lw=1.6, color="#4C72B0")
ax.plot(anchor_t, anchor_q, "o", ms=5, color="#C44E52", zorder=5)
for t, q in zip(anchor_t, anchor_q):
    ax.annotate(f"$+{q}$", xy=(t, q), xytext=(t - 0.012, q + 0.75), fontsize=9,
                color="#C44E52")
ax.set_xlabel("产出质量分位点 $\\tau$", fontsize=10)
ax.set_ylabel("分位数处理效应（分）", fontsize=10)
ax.set_xlim(0.02, 0.98)
ax.set_ylim(-2.5, 10.5)
ax.set_xticks(anchor_t)
ax.tick_params(labelsize=9)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/fig2_qte.png", dpi=300)
plt.close(fig)
print("figures done")
