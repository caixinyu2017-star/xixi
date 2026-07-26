# -*- coding: utf-8 -*-
"""生成两篇青年就业论文的插图。全部数据来自 p1_sim.py / p2_sim.py 的估计输出。"""
import json
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
OUT = "/tmp/claude-0/-home-user-xixi/6b37a25a-9ac4-51b0-95a3-103191b10bff/scratchpad"

# ================= 论文1 图1：数字经济与青年高质量就业的演进 =================
tr = pd.read_csv(f"{OUT}/p1_trend.csv")
trg = pd.read_csv(f"{OUT}/p1_trend_region.csv")
names = {0: "东部地区", 1: "中部地区", 2: "西部地区"}
marks = {0: "o", 1: "s", 2: "^"}

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), dpi=300)
ax = axes[0]
ax.plot(tr["year"], tr["dig"], "-o", ms=3.6, lw=1.5, color=BLUE, label="数字经济发展水平")
ax2 = ax.twinx()
ax2.plot(tr["year"], tr["yqe"], "--s", ms=3.6, lw=1.5, color=RED, label="青年高质量就业水平")
ax.set_xlabel("年份", fontsize=9)
ax.set_ylabel("数字经济发展水平", fontsize=9, color=BLUE)
ax2.set_ylabel("青年高质量就业水平", fontsize=9, color=RED)
ax.tick_params(labelsize=8); ax2.tick_params(labelsize=8)
ax.set_xticks(range(2012, 2024, 2))
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=7.5, loc="upper left", frameon=False)
ax.set_title("(a) 总体演进趋势", fontsize=9.5, y=-0.32)

ax = axes[1]
for k, nm in names.items():
    s = trg[trg["region"] == k]
    ax.plot(s["year"], s["yqe"], f"-{marks[k]}", ms=3.4, lw=1.4, label=nm)
ax.set_xlabel("年份", fontsize=9)
ax.set_ylabel("青年高质量就业水平", fontsize=9)
ax.set_xticks(range(2012, 2024, 2))
ax.tick_params(labelsize=8)
ax.legend(fontsize=7.5, frameon=False)
ax.set_title("(b) 分区域演进趋势", fontsize=9.5, y=-0.32)
for a in list(axes) + [ax2]:
    for s in ("top",):
        a.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/p1_fig1.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# ================= 论文1 图2：门槛效应的似然比与分区间效应 =================
res1 = json.load(open(f"{OUT}/p1_results.json", encoding="utf-8"))
ssr = pd.read_csv(f"{OUT}/p1_threshold_ssr.csv")
th = res1["threshold"]

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), dpi=300)
ax = axes[0]
lr = (ssr["ssr"] - ssr["ssr"].min()) / (ssr["ssr"].min() / 3336)
ax.plot(ssr["gamma"], lr, lw=1.5, color=BLUE)
ax.axhline(7.35, ls="--", lw=1.0, color=RED)
ax.text(ssr["gamma"].min() + 0.02, 22, "95%置信水平临界值", fontsize=7.5, color=RED)
ax.axvline(th["gamma1"], ls=":", lw=1.2, color=GREY)
ax.annotate(f"$\\hat{{\\gamma}}_1$={th['gamma1']:.3f}", xy=(th["gamma1"], lr.max() * 0.55),
            xytext=(th["gamma1"] + 0.22, lr.max() * 0.72), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8, color=GREY))
ax.set_xlabel("门槛变量取值（人力资本水平）", fontsize=9)
ax.set_ylabel("似然比统计量 $LR$", fontsize=9)
ax.tick_params(labelsize=8)
ax.set_title("(a) 门槛值的似然比检验", fontsize=9.5, y=-0.32)

ax = axes[1]
segs = ["_r1", "_r2", "_r3"]
labels = [f"区间Ⅰ\n(hc≤{th['gamma1']:.2f})",
          f"区间Ⅱ\n({th['gamma1']:.2f}<hc≤{th['gamma2']:.2f})",
          f"区间Ⅲ\n(hc>{th['gamma2']:.2f})"]
vals = [float(th["double"][s]["coef"].rstrip("*")) for s in segs]
tvals = [abs(float(th["double"][s]["t"].strip("()"))) for s in segs]
ses = [abs(v) / t if t > 0 else 0 for v, t in zip(vals, tvals)]
colors = [GREY if abs(v / (se or 1)) < 1.96 else BLUE for v, se in zip(vals, ses)]
bars = ax.bar(range(3), vals, yerr=[1.96 * s for s in ses], capsize=4,
              color=colors, width=0.56, error_kw=dict(lw=0.9))
for i, (v, se, sh) in enumerate(zip(vals, ses, [th["share_r1"], th["share_r2"], th["share_r3"]])):
    top = v + 1.96 * se
    ax.text(i, top + 0.018, f"{v:.4f}", ha="center", fontsize=8)
    ax.text(i, -0.135, f"样本占比{sh*100:.1f}%", ha="center", fontsize=7, color=GREY)
ax.axhline(0, color="0.3", lw=0.8)
ax.set_xticks(range(3)); ax.set_xticklabels(labels, fontsize=7.6)
ax.set_ylabel("数字经济的估计系数", fontsize=9)
ax.set_ylim(-0.17, 0.46)
ax.tick_params(labelsize=8)
ax.set_title("(b) 分区间的边际效应", fontsize=9.5, y=-0.38)
for a in axes:
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/p1_fig2.png", dpi=300, bbox_inches="tight")
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

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), dpi=300)
ax = axes[0]
ax.scatter(d["ai_std"], d["_y"], s=5, alpha=0.28, color=BLUE, lw=0)
xs = np.linspace(d["ai_std"].min(), d["ai_std"].max(), 200)
fit = b1 * xs + b2 * xs ** 2
fit = fit - fit.mean() + d["_y"].mean()
ax.plot(xs, fit, lw=2.0, color=RED)
ax.axvline(turn, ls="--", lw=1.1, color=GREY)
ax.annotate(f"拐点 $\\tau^*$={turn:.3f}", xy=(turn, fit.min()),
            xytext=(turn + 0.35, fit.min() + 0.10), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8, color=GREY))
ax.set_xlabel("人工智能应用水平（标准化）", fontsize=9)
ax.set_ylabel("青年就业规模（去除固定效应）", fontsize=9)
ax.tick_params(labelsize=8)
ax.set_title("(a) U型关系与拐点", fontsize=9.5, y=-0.32)

ax = axes[1]
st = res2["structure"]
items = ["青年高技能就业占比", "青年低技能就业占比", "常规任务岗位占比", "新兴数字职业占比"]
vals = [st[k]["b"] for k in items]
tv = [abs(float(st[k]["t"].strip("()"))) for k in items]
ses = [abs(v) / t for v, t in zip(vals, tv)]
cols = [BLUE if v > 0 else RED for v in vals]
ax.barh(range(4), vals, xerr=[1.96 * s for s in ses], capsize=3.5,
        color=cols, height=0.55, error_kw=dict(lw=0.9))
ax.set_yticks(range(4))
ax.set_yticklabels(["青年高技能\n就业占比", "青年低技能\n就业占比",
                    "常规任务\n岗位占比", "新兴数字\n职业占比"], fontsize=7.6)
ax.axvline(0, color="0.3", lw=0.8)
for i, (v, se) in enumerate(zip(vals, ses)):
    end = v + (1.96 * se if v > 0 else -1.96 * se)
    ax.text(end + (0.22 if v > 0 else -0.22), i, f"{v:.3f}", va="center",
            ha="left" if v > 0 else "right", fontsize=7.6)
ax.set_xlabel("人工智能应用的估计系数", fontsize=9)
ax.set_xlim(-6.4, 6.4)
ax.tick_params(labelsize=8)
ax.invert_yaxis()
ax.set_title("(b) 就业结构效应", fontsize=9.5, y=-0.32)
for a in axes:
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/p2_fig1.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# ================= 论文2 图2：调节效应与分位数效应 =================
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), dpi=300)
ax = axes[0]
mod = res2["moderation"]["教育发展水平"]
bx = float(mod["x"]["coef"].rstrip("*"))
bx2 = float(mod["x2"]["coef"].rstrip("*"))
binter = float(mod["inter"]["coef"].rstrip("*"))
xs = np.linspace(-2.0, 2.4, 120)
for zval, style, lab in [(-1.0, ":", "低教育水平（低1个标准差）"),
                         (0.0, "-", "平均教育水平"),
                         (1.0, "--", "高教育水平（高1个标准差）")]:
    ys = bx * xs + bx2 * xs ** 2 + binter * xs * zval
    ax.plot(xs, ys - ys[0], style, lw=1.6, label=lab)
ax.set_xlabel("人工智能应用水平（标准化）", fontsize=9)
ax.set_ylabel("青年就业规模的相对变化", fontsize=9)
ax.legend(fontsize=7.2, frameon=False, loc="upper left")
ax.tick_params(labelsize=8)
ax.set_title("(a) 教育发展水平的调节作用", fontsize=9.5, y=-0.32)

ax = axes[1]
q = res2["quantile"]
qs = list(q.keys())
b1q = [float(q[k]["x"].rstrip("*")) for k in qs]
b2q = [float(q[k]["x2"].rstrip("*")) for k in qs]
x = np.arange(len(qs))
ax.plot(x, b1q, "-o", ms=4.4, lw=1.5, color=RED, label="一次项系数 $\\beta_1$")
ax.plot(x, b2q, "-s", ms=4.4, lw=1.5, color=BLUE, label="二次项系数 $\\beta_2$")
ax.axhline(0, color="0.35", lw=0.8)
ax.set_xticks(x); ax.set_xticklabels([k.replace("Q", "第") + "分位" for k in qs], fontsize=7.6)
ax.set_ylabel("估计系数", fontsize=9)
ax.legend(fontsize=7.5, frameon=False)
ax.tick_params(labelsize=8)
ax.set_title("(b) 分位数回归的系数变化", fontsize=9.5, y=-0.32)
for a in axes:
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/p2_fig2.png", dpi=300, bbox_inches="tight")
plt.close(fig)

print("figures done: p1_fig1, p1_fig2, p2_fig1, p2_fig2")
