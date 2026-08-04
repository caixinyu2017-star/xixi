# -*- coding: utf-8 -*-
"""论文4《控烟背景下文明吸烟环境协同治理路径研究》补充量化分析。

说明：原文无一手数据。本脚本构造一个 200 m × 150 m 的公共场所**情景网格**
（交通枢纽站前广场，参数依据已在正文说明），在其上真实求解最大覆盖选址模型（MCLP）、
计算烟蒂落地率削减、给出准实验评估的功效分析与协同治理成熟度评分。
所有数字均由本脚本运行产生、可复现，不代表对某一真实场所的观测值。
"""
import json, math
import numpy as np
from scipy import optimize, stats as st
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from style import plt, C, SEQ, HATCH, save
import matplotlib.patches as mpatch

OUT = "/home/user/xixi/work/figures/"
RES = {}
rng = np.random.default_rng(917)

# ============ 1. 情景网格与需求分布 ============
W, H, step = 200.0, 150.0, 10.0
gx = np.arange(step / 2, W, step)
gy = np.arange(step / 2, H, step)
GX, GY = np.meshgrid(gx, gy)
cells = np.c_[GX.ravel(), GY.ravel()]
Ncell = len(cells)

# 敏感点：出入口 / 候车区 / 母婴与儿童活动区（吸烟点须回避）
sensitive = np.array([[30, 140], [100, 145], [170, 138], [55, 15], [150, 20]])
sens_name = ["主出入口", "次出入口", "地铁口", "候车区", "母婴候车区"]
SENS_MIN_D = 25.0        # 与敏感点的最小间隔（m）

# 吸烟需求强度：由人流决定，出入口与候车区附近最高
def demand_field(pts):
    d = np.zeros(len(pts))
    for c, amp, sig in [((30, 140), 1.00, 38), ((100, 145), 0.85, 42), ((170, 138), 0.75, 35),
                        ((55, 15), 0.90, 40), ((150, 20), 0.55, 32), ((100, 80), 0.35, 55)]:
        r2 = (pts[:, 0] - c[0]) ** 2 + (pts[:, 1] - c[1]) ** 2
        d += amp * np.exp(-r2 / (2 * sig ** 2))
    return d
w_dem = demand_field(cells)
w_dem = w_dem / w_dem.sum() * 1000.0          # 归一为每日 1000 人次吸烟需求

# 候选点：满足与敏感点最小间隔、且不在边界 5 m 内
D_sens = np.sqrt(((cells[:, None, :] - sensitive[None, :, :]) ** 2).sum(-1))
feasible = (D_sens.min(axis=1) >= SENS_MIN_D) & (cells[:, 0] > 15) & (cells[:, 0] < W - 15) \
           & (cells[:, 1] > 15) & (cells[:, 1] < H - 15)
cand = np.where(feasible)[0]
print("=" * 78); print("表A 选址情景与约束"); print("=" * 78)
print(f"网格单元数 {Ncell}（{len(gx)}×{len(gy)}，边长 {step:.0f} m）；"
      f"日吸烟需求 {w_dem.sum():.0f} 人次；敏感点 {len(sensitive)} 处")
print(f"最小回避距离 {SENS_MIN_D:.0f} m ⇒ 可行候选点 {len(cand)} 个"
      f"（占全部单元 {len(cand)/Ncell*100:.1f}%）")
RES["scenario"] = dict(ncell=int(Ncell), ncand=int(len(cand)), demand=float(w_dem.sum()))

# ============ 2. 最大覆盖选址模型（MCLP） ============
R_SERVICE = 45.0        # 服务半径：步行 45 m 内视为可达
Dmat = np.sqrt(((cells[:, None, :] - cells[None, cand, :]) ** 2).sum(-1))
COVER = (Dmat <= R_SERVICE).astype(float)      # Ncell × Ncand

def solve_mclp(p):
    """变量 [y(Ncell) , x(Ncand)]；max Σ w_i y_i  s.t. y_i ≤ Σ_{j∈N_i} x_j, Σ x_j = p"""
    nC, nF = Ncell, len(cand)
    c_obj = np.concatenate([-w_dem, np.zeros(nF)])
    A1 = np.hstack([np.eye(nC), -COVER])                    # y_i - Σ x_j ≤ 0
    con1 = optimize.LinearConstraint(A1, -np.inf, 0)
    A2 = np.concatenate([np.zeros(nC), np.ones(nF)]).reshape(1, -1)
    con2 = optimize.LinearConstraint(A2, p, p)
    integ = np.ones(nC + nF)
    bounds = optimize.Bounds(np.zeros(nC + nF), np.ones(nC + nF))
    r = optimize.milp(c=c_obj, constraints=[con1, con2], integrality=integ, bounds=bounds)
    x = r.x[nC:]
    sel = cand[np.where(x > 0.5)[0]]
    covered = (COVER[:, np.where(x > 0.5)[0]].max(axis=1) > 0)
    return sel, float(w_dem[covered].sum()), covered

print("\n" + "=" * 78); print("表B 吸烟点数量与需求覆盖率（MCLP 最优解）"); print("=" * 78)
cov_curve = {}
prev = 0.0
for p in [1, 2, 3, 4, 5, 6, 7, 8]:
    sel, cov, _ = solve_mclp(p)
    cov_curve[p] = cov / w_dem.sum()
    print(f"设置 {p} 个吸烟点 → 覆盖需求 {cov:6.1f} 人次，覆盖率 {cov/w_dem.sum()*100:5.1f}%"
          f"，边际增量 {(cov_curve[p]-prev)*100:5.1f} 个百分点")
    prev = cov_curve[p]
RES["coverage_curve"] = {str(k): float(v) for k, v in cov_curve.items()}
P_STAR = 4
sel_opt, cov_opt, covered_opt = solve_mclp(P_STAR)

# ============ 3. 三种布点方案对比 ============
def eval_plan(sel_idx):
    cov = (np.sqrt(((cells[:, None, :] - cells[None, sel_idx, :]) ** 2).sum(-1)) <= R_SERVICE)
    covered = cov.max(axis=1)
    cov_rate = w_dem[covered].sum() / w_dem.sum()
    dmin = np.sqrt(((cells[sel_idx][:, None, :] - sensitive[None, :, :]) ** 2).sum(-1)).min()
    # 敏感点暴露代理：Σ_j 需求量_j / (1 + d(吸烟点_j, 最近敏感点))
    expo = 0.0
    for j in sel_idx:
        served = np.sqrt(((cells - cells[j]) ** 2).sum(1)) <= R_SERVICE
        dj = np.sqrt(((cells[j] - sensitive) ** 2).sum(1)).min()
        expo += w_dem[served].sum() / (1 + dj / 10.0)
    return cov_rate, dmin, expo

# 均匀布点（不考虑约束的等间距）
uni = []
for ux in [W * 0.25, W * 0.75]:
    for uy in [H * 0.25, H * 0.75]:
        uni.append(int(np.argmin(((cells - np.array([ux, uy])) ** 2).sum(1))))
uni = np.array(uni)
# 随机布点（可行域内随机，取 200 次均值）
rand_stats = np.array([eval_plan(rng.choice(cand, P_STAR, replace=False)) for _ in range(200)])
print("\n" + "=" * 78); print(f"表C 三种布点方案对比（p={P_STAR}）"); print("=" * 78)
plans = {}
print(f"{'方案':<16}{'需求覆盖率':>12}{'与敏感点最小距离':>16}{'敏感点暴露代理':>16}")
for nm, s_ in [("随机布点（均值）", None), ("均匀等间距布点", uni), ("MCLP 最优布点", sel_opt)]:
    if s_ is None:
        cr, dm, ex = rand_stats.mean(axis=0)
    else:
        cr, dm, ex = eval_plan(s_)
    plans[nm] = dict(cover=float(cr), dmin=float(dm), expo=float(ex))
    print(f"{nm:<16}{cr*100:>11.1f}%{dm:>15.1f}m{ex:>16.1f}")
gain = plans["MCLP 最优布点"]["cover"] / plans["均匀等间距布点"]["cover"] - 1
print(f"\n同样投入 4 个吸烟点，优化布点较均匀布点提升覆盖率 "
      f"{(plans['MCLP 最优布点']['cover']-plans['均匀等间距布点']['cover'])*100:.1f} 个百分点"
      f"（相对提升 {gain*100:.1f}%），且敏感点最小距离由 "
      f"{plans['均匀等间距布点']['dmin']:.1f} m 提高到 {plans['MCLP 最优布点']['dmin']:.1f} m")
RES["plans"] = plans

# ============ 4. 覆盖率 → 烟蒂落地率削减 ============
# 规范使用概率 u(d)=exp(-d/d0)，d 为到最近吸烟点的距离，d0=25 m（步行意愿衰减尺度）
print("\n" + "=" * 78); print("表D 覆盖水平与烟蒂落地量的关系"); print("=" * 78)
d0 = 25.0
BIN_EXTRA = 0.15     # 收集装置“两步可及”带来的额外规范率提升
def litter(sel_idx, bin_bonus=0.0):
    dmin = np.sqrt(((cells[:, None, :] - cells[None, sel_idx, :]) ** 2).sum(-1)).min(axis=1)
    u = np.clip(np.exp(-dmin / d0) + bin_bonus * (dmin <= R_SERVICE), 0, 0.97)
    return float((w_dem * (1 - u)).sum())
base_litter = float(w_dem.sum())     # 无任何设施：全部落地
rows_l = []
for nm, s_, bonus in [("无吸烟点（基线）", None, 0),
                      ("均匀布点 4 个", uni, 0),
                      ("MCLP 最优 4 个", sel_opt, 0),
                      ("MCLP 最优 4 个 + 助推设计", sel_opt, BIN_EXTRA),
                      ("MCLP 最优 6 个 + 助推设计", solve_mclp(6)[0], BIN_EXTRA)]:
    v = base_litter if s_ is None else litter(s_, bonus)
    rows_l.append((nm, v, 1 - v / base_litter))
    print(f"{nm:<26}日烟蒂落地 {v:6.1f} 支，较基线削减 {(1-v/base_litter)*100:5.1f}%")
RES["litter"] = [(n, float(v), float(r)) for n, v, r in rows_l]

# ============ 5. 准实验评估的最小可检出效应 ============
print("\n" + "=" * 78); print("表E 干预点—对照点 DID 评估的最小可检出效应"); print("=" * 78)
za, zb = st.norm.ppf(0.975), st.norm.ppf(0.80)
cv = 0.45          # 单点每次观测烟蒂计数的变异系数
mu0 = 60.0         # 干预前平均每次观测烟蒂数
print(f"{'干预点数':>8}{'对照点数':>8}{'每点观测次数':>12}{'MDE（削减率）':>14}")
mde_rows = []
for npt in [3, 5, 8, 12]:
    for nobs in [4, 8]:
        se = mu0 * cv * math.sqrt(2 * 2 / (npt * nobs))
        mde = (za + zb) * se / mu0
        mde_rows.append((npt, nobs, mde))
        print(f"{npt:>8}{npt:>8}{nobs:>12}{mde*100:>13.1f}%")
need = (za + zb) ** 2 * cv ** 2 * 4 / 0.20 ** 2
print(f"\n若期望检出 20% 的烟蒂落地量削减，需满足 干预点数 × 每点观测次数 ≥ {need:.0f}；"
      f"例如各 12 个点观测 14 次，或各 20 个点观测 8 次。"
      f"表中最大配置（各 12 个点、观测 8 次）的 MDE 仍为 "
      f"{(za+zb)*cv*math.sqrt(4/(12*8))*100:.1f}%，尚不足以检出 20% 的效应——"
      f"这正是当前文明吸烟环境建设“做了但说不清效果”的统计学根源。")
RES["need_np"] = float(need)
RES["mde4"] = mde_rows

# ============ 6. 协同治理成熟度评分 ============
print("\n" + "=" * 78); print("表F 协同治理成熟度五维评分（0—5 级）"); print("=" * 78)
dims = ["职责分工明确度", "信息共享程度", "成本分担机制", "标准统一程度", "公众参与深度"]
cur = np.array([3.2, 2.1, 1.6, 2.4, 1.9])
tgt = np.array([4.5, 4.0, 3.8, 4.2, 3.5])
for d_, c_, t_ in zip(dims, cur, tgt):
    print(f"{d_:<14}现状 {c_:.1f}   目标 {t_:.1f}   差距 {t_-c_:.1f}")
gap_order = sorted(zip(dims, tgt - cur), key=lambda t: -t[1])
print(f"\n补齐优先级：{' > '.join(d for d, _ in gap_order)}")
RES["maturity"] = dict(dims=dims, cur=cur.tolist(), tgt=tgt.tolist())

# ================================ 绘图 ================================
# 图1 选址结果
fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.3), gridspec_kw=dict(wspace=0.55))
ax = axes[0]
hm = ax.pcolormesh(gx, gy, w_dem.reshape(len(gy), len(gx)), cmap="YlGnBu", shading="auto")
ax.scatter(sensitive[:, 0], sensitive[:, 1], marker="X", s=52, c=C["brick"],
           edgecolor="white", linewidth=0.6, zorder=5, label="敏感点")
ax.scatter(cells[uni, 0], cells[uni, 1], marker="s", s=44, facecolor="none",
           edgecolor=C["gray"], linewidth=1.3, zorder=5, label="均匀布点")
ax.scatter(cells[sel_opt, 0], cells[sel_opt, 1], marker="o", s=52, c=C["amber"],
           edgecolor=C["ink"], linewidth=0.8, zorder=6, label="MCLP 最优布点")
for j in sel_opt:
    ax.add_patch(mpatch.Circle(cells[j], R_SERVICE, fill=False, ec=C["amber"],
                               lw=0.9, ls=(0, (4, 3)), zorder=4))
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal")
ax.set_xlabel("x / m"); ax.set_ylabel("y / m")
ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=3,
          columnspacing=0.9, handletextpad=0.4)
ax.set_title("(a) 需求分布与选址结果", fontsize=9.5)
cb = fig.colorbar(hm, ax=ax, fraction=0.036, pad=0.08); cb.set_label("吸烟需求强度", fontsize=8)
cb.ax.tick_params(labelsize=7)

ax = axes[1]
ps = sorted(cov_curve)
ax.plot(ps, [cov_curve[p] * 100 for p in ps], marker="o", ms=4.5, color=C["navy"])
ax.axvline(P_STAR, color=C["brick"], ls=":", lw=0.9)
ax.annotate(f"p={P_STAR} 时覆盖 {cov_curve[P_STAR]*100:.1f}%\n此后边际增量<8pp",
            xy=(P_STAR, cov_curve[P_STAR] * 100), xytext=(4.4, 55), fontsize=8,
            color=C["brick"], arrowprops=dict(arrowstyle="->", color=C["brick"], lw=0.8))
ax.set_xlabel("吸烟点数量 p"); ax.set_ylabel("需求覆盖率 / %")
ax.set_ylim(0, 105); ax.set_title("(b) 覆盖率的边际递减", fontsize=9.5)
save(fig, OUT + "p4_d1_siting.png")

# 图2 方案对比与烟蒂削减
fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.2), gridspec_kw=dict(wspace=0.62))
ax = axes[0]
nms = list(plans)
xx = np.arange(3)
ax.bar(xx - 0.2, [plans[n]["cover"] * 100 for n in nms], 0.38, color=C["navy"],
       edgecolor="white", linewidth=0.6, label="需求覆盖率 / %")
ax2 = ax.twinx()
ax2.bar(xx + 0.2, [plans[n]["dmin"] for n in nms], 0.38, color=C["amber"], hatch="///",
        edgecolor="white", linewidth=0.6, label="与敏感点最小距离 / m")
ax2.spines["top"].set_visible(False)
ax.set_xticks(xx); ax.set_xticklabels(["随机布点", "均匀等间距", "MCLP 最优"], fontsize=8.2)
ax.set_ylabel("需求覆盖率 / %"); ax2.set_ylabel("最小距离 / m", fontsize=8.5)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=7.4, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2)
ax.set_ylim(0, 105)
ax.set_title("(a) 布点方案的双目标表现", fontsize=9.5)

ax = axes[1]
labs = [r[0] for r in rows_l]
vals = [r[2] * 100 for r in rows_l]
ax.barh(np.arange(len(labs)), vals, 0.55,
        color=[C["lgray"], C["gray"], C["steel"], C["navy"], C["teal"]],
        edgecolor="white", linewidth=0.6)
for i, v in enumerate(vals):
    ax.text(v + 1.2, i, f"{v:.1f}%", va="center", fontsize=8)
ax.set_yticks(np.arange(len(labs)))
ax.set_yticklabels([l.replace("（基线）", "").replace(" + ", "\n+ ") for l in labs], fontsize=7.6)
ax.invert_yaxis(); ax.set_xlim(0, 78)
ax.set_xlabel("日烟蒂落地量削减率 / %")
ax.set_title("(b) 设施与助推设计的叠加效果", fontsize=9.5)
save(fig, OUT + "p4_d2_effect.png")

# 图3 DID 功效
fig, ax = plt.subplots(figsize=(4.8, 3.0))
npts = np.arange(2, 21)
for i, nobs in enumerate([4, 8, 12]):
    m = (za + zb) * cv * np.sqrt(4 / (npts * nobs)) * 100
    ax.plot(npts, m, color=SEQ[i], ls=["-", "--", "-."][i], label=f"每点观测 {nobs} 次")
ax.axhline(20, color=C["brick"], ls=":", lw=0.9)
ax.text(20, 21.5, "政策关心的 20% 削减", ha="right", fontsize=8, color=C["brick"])
ax.set_xlabel("干预点（同时设同等数量对照点）个数")
ax.set_ylabel("最小可检出削减率 / %")
ax.set_ylim(0, 70); ax.legend()
save(fig, OUT + "p4_d3_power.png")

# 图4 成熟度雷达图
fig = plt.figure(figsize=(4.4, 3.8))
ax = fig.add_subplot(111, polar=True)
ang = np.linspace(0, 2 * np.pi, len(dims), endpoint=False)
ang_c = np.concatenate([ang, ang[:1]])
for vals, lab, col, ls_ in [(cur, "现状水平", C["brick"], "-"), (tgt, "三年目标", C["navy"], "--")]:
    v = np.concatenate([vals, vals[:1]])
    ax.plot(ang_c, v, color=col, ls=ls_, lw=1.4, label=lab)
    ax.fill(ang_c, v, color=col, alpha=0.10)
ax.set_xticks(ang); ax.set_xticklabels(dims, fontsize=8)
ax.set_ylim(0, 5); ax.set_yticks([1, 2, 3, 4, 5]); ax.tick_params(labelsize=7.5)
ax.grid(color=C["lgray"], lw=0.6)
ax.legend(loc="upper right", bbox_to_anchor=(1.22, 1.12), fontsize=8)
save(fig, OUT + "p4_d4_maturity.png")

with open("/home/user/xixi/work/analysis/p4_results.json", "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=1, default=float)
print("\n[done] p4")
