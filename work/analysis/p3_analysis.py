# -*- coding: utf-8 -*-
"""论文3《精细化管理视角下相关方安全监管策略优化研究》补充量化分析。

说明：原文无一手数据。本脚本构造 60 家相关方的**情景样本**（分布参数依据烟草商业企业
相关方的通常构成设定，已在正文说明），并在其上真实运行 LEC 风险定级、AHP–熵权组合赋权、
监管资源优化配置与隐患帕累托分析。所有数字均由本脚本运行产生、可复现。
"""
import json, math
import numpy as np
from scipy import optimize
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from style import plt, C, SEQ, HATCH, save
import matplotlib.patches as mpatch

OUT = "/home/user/xixi/work/figures/"
RES = {}
rng = np.random.default_rng(31)

# ============ 1. 相关方情景样本与 LEC 风险定级 ============
# D = L × E × C ；L 事故可能性, E 暴露频率, C 后果严重度
types = [("工程施工类", 12, (4.5, 1.6), (6.0, 1.5), (10.0, 3.0), (62, 11)),
         ("设备维护类", 16, (3.0, 1.2), (4.5, 1.5), (7.0, 2.5), (70, 10)),
         ("物流辅助类", 14, (2.0, 0.9), (6.5, 1.5), (5.0, 2.0), (66, 12)),
         ("服务保障类", 18, (1.2, 0.6), (7.5, 1.2), (3.5, 1.5), (74, 9))]
rows = []
for name, n, (lm, ls), (em, es), (cm, cs), (am, asd) in types:
    L = np.clip(rng.normal(lm, ls, n), 0.2, 10)
    E = np.clip(rng.normal(em, es, n), 0.5, 10)
    Cc = np.clip(rng.normal(cm, cs, n), 1, 40)
    A = np.clip(rng.normal(am, asd, n), 30, 98)          # 安全管理能力评分 0—100
    for i in range(n):
        rows.append((name, L[i], E[i], Cc[i], L[i] * E[i] * Cc[i], A[i]))
tp = np.array([r[0] for r in rows])
Lv = np.array([r[1] for r in rows]); Ev = np.array([r[2] for r in rows])
Cv = np.array([r[3] for r in rows]); Dv = np.array([r[4] for r in rows])
Av = np.array([r[5] for r in rows])
Nf = len(rows)

def rlevel(d):
    return "高风险" if d > 160 else ("中风险" if d > 70 else "低风险")
def alevel(a):
    return "能力强" if a >= 80 else ("能力中" if a >= 60 else "能力弱")
GRID = {("高风险", "能力弱"): "A1", ("高风险", "能力中"): "A2", ("高风险", "能力强"): "B1",
        ("中风险", "能力弱"): "A2", ("中风险", "能力中"): "B1", ("中风险", "能力强"): "B2",
        ("低风险", "能力弱"): "B2", ("低风险", "能力中"): "C1", ("低风险", "能力强"): "C2"}
grade = np.array([GRID[(rlevel(d), alevel(a))] for d, a in zip(Dv, Av)])

print("=" * 78); print(f"表A 相关方情景样本概况（N={Nf}）"); print("=" * 78)
print(f"{'类别':<10}{'N':>4}{'D 均值':>10}{'D 中位':>10}{'D 最大':>10}{'能力均值':>10}{'高风险占比':>11}")
desc = {}
for name, *_ in types:
    m = tp == name
    hi = (Dv[m] > 160).mean()
    desc[name] = dict(n=int(m.sum()), d_mean=float(Dv[m].mean()), d_med=float(np.median(Dv[m])),
                      d_max=float(Dv[m].max()), a_mean=float(Av[m].mean()), hi=float(hi))
    print(f"{name:<10}{m.sum():>4}{Dv[m].mean():>10.1f}{np.median(Dv[m]):>10.1f}"
          f"{Dv[m].max():>10.1f}{Av[m].mean():>10.1f}{hi*100:>10.1f}%")
print(f"{'合计':<10}{Nf:>4}{Dv.mean():>10.1f}{np.median(Dv):>10.1f}{Dv.max():>10.1f}"
      f"{Av.mean():>10.1f}{(Dv>160).mean()*100:>10.1f}%")
print("\n分级结果分布：")
for g_ in ["A1", "A2", "B1", "B2", "C1", "C2"]:
    print(f"  {g_}: {int((grade==g_).sum()):>3} 家（{(grade==g_).mean()*100:5.1f}%）")
RES["desc"] = desc
RES["grade_dist"] = {g_: int((grade == g_).sum()) for g_ in ["A1", "A2", "B1", "B2", "C1", "C2"]}

# ============ 2. 安全绩效评价指标体系的 AHP–熵权组合赋权 ============
print("\n" + "=" * 78); print("表B 相关方安全绩效评价指标体系的组合赋权"); print("=" * 78)
crit = ["安全责任落实", "人员资质与培训", "作业票与交底执行",
        "现场违章频次", "隐患整改及时率", "应急能力"]
A_ahp = np.array([
    [1,   1,   1/2, 1/2, 1,   2],
    [1,   1,   1/2, 1/2, 1,   2],
    [2,   2,   1,   1,   2,   3],
    [2,   2,   1,   1,   2,   3],
    [1,   1,   1/2, 1/2, 1,   2],
    [1/2, 1/2, 1/3, 1/3, 1/2, 1],
], dtype=float)
ev, evec = np.linalg.eig(A_ahp)
i0 = int(np.argmax(ev.real)); lmax = ev.real[i0]
w_ahp = np.abs(evec[:, i0].real); w_ahp /= w_ahp.sum()
n_ = len(crit); CI = (lmax - n_) / (n_ - 1); RI = 1.24; CR = CI / RI
print(f"AHP：λmax={lmax:.4f}, CI={CI:.4f}, RI={RI}, CR={CR:.4f} "
      f"{'（一致性通过）' if CR < 0.10 else '（一致性未通过）'}")
S = np.clip(rng.normal([72, 78, 66, 70, 75, 63], [11, 9, 14, 13, 10, 15], size=(Nf, 6)), 20, 100)
P = S / S.sum(axis=0)
E_ = -(P * np.log(P + 1e-12)).sum(axis=0) / np.log(Nf)
w_ent = (1 - E_) / (1 - E_).sum()
w_comb = np.sqrt(w_ahp * w_ent); w_comb /= w_comb.sum()
print(f"\n{'指标':<16}{'AHP':>9}{'熵权':>9}{'组合':>9}")
for c_, a_, e_, m_ in zip(crit, w_ahp, w_ent, w_comb):
    print(f"{c_:<16}{a_:>9.4f}{e_:>9.4f}{m_:>9.4f}")
RES["weights3"] = dict(crit=crit, ahp=w_ahp.tolist(), ent=w_ent.tolist(),
                       comb=w_comb.tolist(), CR=float(CR))

# ============ 3. 监管资源优化配置 ============
# 年度可用检查人日 T；对第 i 家投入 x_i 次检查，风险削减 = D_i * (1 - exp(-gamma_i * x_i))
# gamma_i 随能力评分递减（能力弱者单次检查的边际削减更大）
print("\n" + "=" * 78); print("表C 监管资源配置策略比较（年度检查总量 T=240 次）"); print("=" * 78)
T_total = 240
gamma = 0.18 + 0.22 * (1 - (Av - Av.min()) / (Av.max() - Av.min()))   # 0.18~0.40
def reduction(x):
    return (Dv * (1 - np.exp(-gamma * x))).sum()

# (a) 平均分配
x_avg = np.full(Nf, T_total / Nf)
# (b) 按风险线性分配
x_risk = T_total * Dv / Dv.sum()
# (c) 按二维分级分配（A1:8, A2:6, B1:4, B2:3, C1:2, C2:1，再按比例缩放到 T）
base_alloc = {"A1": 8, "A2": 6, "B1": 4, "B2": 3, "C1": 2, "C2": 1}
x_grade = np.array([base_alloc[g_] for g_ in grade], dtype=float)
x_grade *= T_total / x_grade.sum()
# (d) 边际收益最优分配（贪心；边际收益递减 ⇒ 贪心即全局最优）
x_opt = np.zeros(Nf)
for _ in range(T_total):
    mg = Dv * gamma * np.exp(-gamma * x_opt)
    x_opt[int(np.argmax(mg))] += 1

strategies = [("平均分配", x_avg), ("按风险线性分配", x_risk),
              ("二维分级分配", x_grade), ("边际收益最优分配", x_opt)]
r_avg = reduction(x_avg)
print(f"{'策略':<18}{'风险削减总量':>14}{'较平均分配':>12}{'达到最优的比例':>15}")
r_opt = reduction(x_opt)
alloc_res = {}
for nm, x in strategies:
    r = reduction(x)
    alloc_res[nm] = dict(reduction=float(r), vs_avg=float(r / r_avg - 1), vs_opt=float(r / r_opt))
    print(f"{nm:<18}{r:>14.1f}{(r/r_avg-1)*100:>11.1f}%{r/r_opt*100:>14.1f}%")
RES["alloc"] = alloc_res
# 达到平均分配同等效果所需的检查总量
def need_for(target):
    lo, hi = 1, 600
    while hi - lo > 1:
        mid = (lo + hi) // 2
        x = np.zeros(Nf)
        for _ in range(mid):
            mg = Dv * gamma * np.exp(-gamma * x)
            x[int(np.argmax(mg))] += 1
        if reduction(x) >= target: hi = mid
        else: lo = mid
    return hi
t_need = need_for(r_avg)
print(f"\n最优配置只需 {t_need} 次检查即可达到平均分配 240 次的风险削减效果，"
      f"节省监管人力 {(1 - t_need/T_total)*100:.1f}%")
RES["t_need"] = int(t_need)

# ============ 4. 隐患帕累托分析 ============
print("\n" + "=" * 78); print("表D 相关方隐患类型帕累托分析"); print("=" * 78)
hz_types = ["个体防护用品缺失", "临时用电不规范", "动火作业未办票", "高处作业无防护",
            "现场围挡与警示缺失", "特种作业人员无证", "设备检修未挂牌上锁",
            "受限空间未检测", "消防通道占用", "交叉作业未协调"]
# 频次按 Zipf 型分布生成
freq = np.array([rng.poisson(lam) for lam in [86, 71, 48, 42, 33, 24, 19, 14, 11, 7]])
idx = np.argsort(-freq)
hz_sorted = [hz_types[i] for i in idx]; f_sorted = freq[idx]
cum = np.cumsum(f_sorted) / f_sorted.sum()
k80 = int(np.searchsorted(cum, 0.80) + 1)
print(f"{'隐患类型':<20}{'频次':>6}{'占比':>8}{'累计占比':>10}")
for h, f_, cp in zip(hz_sorted, f_sorted, cum):
    print(f"{h:<20}{f_:>6}{f_/f_sorted.sum()*100:>7.1f}%{cp*100:>9.1f}%")
print(f"\n前 {k80} 类（占类型数 {k80/len(hz_types)*100:.0f}%）贡献了 {cum[k80-1]*100:.1f}% 的隐患，"
      f"符合帕累托规律 → 专项治理应聚焦这 {k80} 类")
RES["pareto"] = dict(types=hz_sorted, freq=f_sorted.tolist(), k80=k80, cum80=float(cum[k80-1]))

# ================================ 绘图 ================================
# 图1 二维分级散点
fig, ax = plt.subplots(figsize=(5.4, 3.6))
cmap = {"工程施工类": C["brick"], "设备维护类": C["navy"],
        "物流辅助类": C["amber"], "服务保障类": C["sage"]}
mk = {"工程施工类": "o", "设备维护类": "s", "物流辅助类": "^", "服务保障类": "D"}
ax.axhspan(160, Dv.max() * 1.08, color="#F7E9E8", zorder=0)
ax.axhspan(70, 160, color="#FBF3E8", zorder=0)
ax.axhspan(0, 70, color="#F2F6F2", zorder=0)
for v in [60, 80]:
    ax.axvline(v, color=C["gray"], lw=0.8, ls=(0, (3, 2)), zorder=1)
for v in [70, 160]:
    ax.axhline(v, color=C["gray"], lw=0.8, ls=(0, (3, 2)), zorder=1)
for name in cmap:
    m = tp == name
    ax.scatter(Av[m], Dv[m], s=26, c=cmap[name], marker=mk[name], edgecolor="white",
               linewidth=0.5, label=name, zorder=3)
ax.set_xlabel("相关方安全管理能力评分"); ax.set_ylabel("LEC 作业风险值 D")
ax.set_yscale("log")
for txt, xx, yy in [("A1", 45, 320), ("A2", 70, 320), ("B1", 90, 320),
                    ("B2", 45, 110), ("B1", 70, 110), ("B2", 90, 110),
                    ("B2", 45, 30), ("C1", 70, 30), ("C2", 90, 30)]:
    ax.text(xx, yy, txt, fontsize=9, color=C["ink"], alpha=0.45, ha="center",
            fontweight="bold", zorder=2)
ax.legend(ncol=2, fontsize=7.8, loc="lower left")
save(fig, OUT + "p3_d1_grid.png")

# 图2 组合权重
fig, ax = plt.subplots(figsize=(5.6, 3.0))
y = np.arange(len(crit))
ax.barh(y + 0.2, w_ahp, 0.38, color=C["steel"], label="AHP 主观权重")
ax.barh(y - 0.2, w_comb, 0.38, color=C["navy"], hatch="///", edgecolor="white",
        linewidth=0.5, label="AHP–熵权组合权重")
ax.set_yticks(y); ax.set_yticklabels(crit, fontsize=8.2); ax.invert_yaxis()
ax.set_xlabel("权重"); ax.legend(fontsize=8)
ax.text(0.99, 0.03, f"CR = {CR:.3f} < 0.10", transform=ax.transAxes, ha="right",
        fontsize=8, color=C["gray"])
save(fig, OUT + "p3_d2_weights.png")

# 图3 资源配置策略
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0))
ax = axes[0]
nms = [s[0] for s in strategies]
vals = [alloc_res[n]["reduction"] for n in nms]
b = ax.bar(np.arange(4), vals, 0.55, color=[C["gray"], C["steel"], C["amber"], C["navy"]],
           edgecolor="white", linewidth=0.6)
for i, v in enumerate(vals):
    ax.text(i, v * 1.01, f"{v:,.0f}\n(+{(v/r_avg-1)*100:.1f}%)", ha="center", va="bottom", fontsize=7.8)
ax.set_xticks(np.arange(4)); ax.set_xticklabels(["平均\n分配", "按风险\n线性", "二维\n分级", "边际收益\n最优"])
ax.set_ylabel("风险削减总量（无量纲）"); ax.set_ylim(0, max(vals) * 1.22)
ax.set_title("(a) 同等检查总量下的削减效果", fontsize=9.5)
ax = axes[1]
Ts = np.arange(40, 401, 20)
curves = {}
_cols = {"平均分配": C["gray"], "二维分级分配": C["amber"], "边际收益最优分配": C["navy"]}
_lss = {"平均分配": ":", "二维分级分配": "--", "边际收益最优分配": "-"}
for nm in ["平均分配", "二维分级分配", "边际收益最优分配"]:
    ys = []
    for Tt in Ts:
        if nm == "平均分配":
            x = np.full(Nf, Tt / Nf)
        elif nm == "二维分级分配":
            x = np.array([base_alloc[g_] for g_ in grade], dtype=float); x *= Tt / x.sum()
        else:
            x = np.zeros(Nf)
            for _ in range(int(Tt)):
                mg = Dv * gamma * np.exp(-gamma * x); x[int(np.argmax(mg))] += 1
        ys.append(reduction(x))
    curves[nm] = ys
    ax.plot(Ts, ys, label=nm, color=_cols[nm], ls=_lss[nm])
ax.axhline(r_avg, color=C["brick"], ls=":", lw=0.9)
ax.axvline(t_need, color=C["brick"], ls=":", lw=0.9)
ax.text(t_need + 6, r_avg * 0.55, f"最优配置仅需 {t_need} 次\n即达平均分配 240 次效果",
        fontsize=7.8, color=C["brick"])
ax.set_xlabel("年度检查总量 T / 次"); ax.set_ylabel("风险削减总量")
ax.legend(fontsize=8, loc="lower right"); ax.set_title("(b) 投入—产出曲线", fontsize=9.5)
save(fig, OUT + "p3_d3_alloc.png")

# 图4 帕累托图
fig, ax = plt.subplots(figsize=(6.0, 3.2))
xx = np.arange(len(hz_sorted))
ax.bar(xx, f_sorted, 0.6, color=C["steel"], edgecolor="white", linewidth=0.6)
ax.set_ylabel("隐患发生频次"); ax.set_xticks(xx)
ax.set_xticklabels([h.replace("作业", "作业\n").replace("人员", "人员\n") for h in hz_sorted],
                   rotation=38, ha="right", fontsize=7.4)
ax2 = ax.twinx()
ax2.plot(xx, cum * 100, color=C["brick"], marker="o", ms=4)
ax2.axhline(80, color=C["gray"], ls=":", lw=0.9)
ax2.set_ylabel("累计占比 / %"); ax2.set_ylim(0, 105); ax2.spines["top"].set_visible(False)
ax2.annotate(f"前 {k80} 类占 {cum[k80-1]*100:.1f}%", xy=(k80 - 1, cum[k80-1] * 100),
             xytext=(k80 + 0.6, 62), fontsize=8, color=C["brick"],
             arrowprops=dict(arrowstyle="->", color=C["brick"], lw=0.8))
save(fig, OUT + "p3_d4_pareto.png")

with open("/home/user/xixi/work/analysis/p3_results.json", "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=1, default=float)
print("\n[done] p3")
