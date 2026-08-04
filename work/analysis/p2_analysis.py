# -*- coding: utf-8 -*-
"""论文2《穿透式监管视角下烟草行业大监督体系优化研究》补充量化分析。

说明：原文无一手数据。本脚本给出的是**模型驱动的数值分析**——所有数字均由本脚本
实际运行产生、可复现；参数取值为课题组设定的情景参数（已在正文中逐一说明依据），
用于揭示机制方向与优先级，不代表对嘉兴市局真实指标的观测值。
"""
import json, itertools, math
import numpy as np
from scipy import optimize
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from style import plt, C, SEQ, HATCH, save

OUT = "/home/user/xixi/work/figures/"
RES = {}
rng = np.random.default_rng(2024)

# ============ 1. 多层委托代理下的监督效力衰减与穿透通道 ============
# E_k = (1-a)*E0*(1-d)^k + a*E0*rho
# k: 层级（0=国家局 … 3=县级局）；d: 逐级衰减率；a: 穿透直达通道覆盖比例；rho: 直达通道保真度
print("=" * 78); print("表A 监督效力沿层级衰减及穿透通道的修正（E0=1, rho=0.90）"); print("=" * 78)
def efficacy(k, d, a, rho=0.90):
    return (1 - a) * (1 - d) ** k + a * rho

ks = np.arange(0, 4)
decay_tbl = {}
print("衰减率 d   穿透覆盖 a" + "".join(f"      k={k}" for k in ks) + "   末梢损失")
for d in [0.20, 0.30, 0.40]:
    for a in [0.0, 0.3, 0.6]:
        e = [efficacy(k, d, a) for k in ks]
        decay_tbl[(d, a)] = e
        print(f"   {d:.2f}        {a:.1f}   " + "".join(f"  {v*100:6.1f}%" for v in e) +
              f"   {(1-e[-1])*100:6.1f}%")
RES["decay"] = {f"d{d}_a{a}": v for (d, a), v in decay_tbl.items()}
# 关键结论：a 从 0 提升到 0.6 时，县级效力的绝对增量
for d in [0.20, 0.30, 0.40]:
    g = efficacy(3, d, 0.6) - efficacy(3, d, 0.0)
    print(f"d={d:.2f}: 穿透覆盖由 0 提至 0.6，县级监督效力提升 {g*100:.1f} 个百分点")

# ============ 2. 含“监督过载”的最优监督强度 ============
# 总成本 TC(s) = c*s (直接监督成本) + b*s^2 (基层负担/业务效能损失) + L*R0*exp(-beta*s)
print("\n" + "=" * 78); print("表B 含监督过载项的最优监督强度求解"); print("=" * 78)
def total_cost(s, c, b, L, R0, beta):
    return c * s + b * s ** 2 + L * R0 * np.exp(-beta * s)

base = dict(c=1.0, b=0.35, L=60.0, R0=1.0, beta=0.55)
def opt_s(**kw):
    p = dict(base); p.update(kw)
    r = optimize.minimize_scalar(lambda s: total_cost(s, **p), bounds=(0, 12), method="bounded")
    return r.x, r.fun, p

s_star, tc_star, _ = opt_s()
s_noload = optimize.minimize_scalar(
    lambda s: total_cost(s, base["c"], 0.0, base["L"], base["R0"], base["beta"]),
    bounds=(0, 12), method="bounded").x
print(f"基准情景：最优监督强度 s* = {s_star:.2f}，总成本 = {tc_star:.2f}")
print(f"若忽略监督过载项（b=0）：s* = {s_noload:.2f}，比考虑过载时高 {s_noload - s_star:.2f}"
      f"（{(s_noload/s_star-1)*100:.1f}%）→ 忽视基层负担会系统性高估最优监督强度")
sens = {}
print("\n敏感性分析：")
for nm, kws in [("过载系数 b", [("b", v) for v in [0.15, 0.35, 0.70]]),
                ("风险损失 L", [("L", v) for v in [30, 60, 120]]),
                ("监督效力 β", [("beta", v) for v in [0.35, 0.55, 0.80]])]:
    row = []
    for k, v in kws:
        ss, tc, _ = opt_s(**{k: v})
        row.append((v, ss, tc))
        print(f"  {nm} = {v:<6}: s* = {ss:5.2f}, TC* = {tc:7.2f}")
    sens[nm] = row
RES["optimal_s"] = dict(s_star=float(s_star), tc_star=float(tc_star), s_noload=float(s_noload))

# ============ 3. AHP–熵权组合赋权：穿透式监督效能评价指标体系 ============
print("\n" + "=" * 78); print("表C 监督效能评价指标体系的 AHP–熵权组合赋权"); print("=" * 78)
crit = ["制度穿透度", "数据穿透度", "流程穿透度", "责任穿透度", "监督减负度"]
# 课题组设定的 1—9 标度判断矩阵（依据：制度与数据为前置条件，减负为约束条件）
A = np.array([
    [1,   1,   2,   2,   3],
    [1,   1,   2,   3,   3],
    [1/2, 1/2, 1,   2,   2],
    [1/2, 1/3, 1/2, 1,   2],
    [1/3, 1/3, 1/2, 1/2, 1],
], dtype=float)
w_eig, v = np.linalg.eig(A)
i = int(np.argmax(w_eig.real))
lmax = w_eig.real[i]
w_ahp = np.abs(v[:, i].real); w_ahp /= w_ahp.sum()
n = len(crit)
CI = (lmax - n) / (n - 1)
RI = {3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32}[n]
CR = CI / RI
print(f"AHP：λmax = {lmax:.4f}, CI = {CI:.4f}, RI = {RI}, CR = {CR:.4f} "
      f"{'（CR<0.10，一致性通过）' if CR < 0.10 else '（一致性未通过）'}")

# 熵权：以 12 个基层单位的模拟评分矩阵（0—100）计算指标区分度
X = np.clip(rng.normal([62, 55, 68, 58, 45], [12, 15, 10, 13, 16], size=(12, 5)), 5, 100)
P = X / X.sum(axis=0)
E = -(P * np.log(P + 1e-12)).sum(axis=0) / np.log(X.shape[0])
d_ = 1 - E
w_ent = d_ / d_.sum()
w_comb = np.sqrt(w_ahp * w_ent); w_comb /= w_comb.sum()
print(f"\n{'指标':<12}{'AHP权重':>10}{'熵权':>10}{'组合权重':>12}")
for c_, a_, e_, m_ in zip(crit, w_ahp, w_ent, w_comb):
    print(f"{c_:<12}{a_:>10.4f}{e_:>10.4f}{m_:>12.4f}")
RES["weights"] = dict(crit=crit, ahp=w_ahp.tolist(), ent=w_ent.tolist(),
                      comb=w_comb.tolist(), CR=float(CR), lmax=float(lmax))

# ============ 4. 四维穿透实施组合的蒙特卡洛边际贡献 ============
print("\n" + "=" * 78); print("表D 四维穿透的边际贡献蒙特卡洛仿真（N=20000）"); print("=" * 78)
# 风险发现率 F = 1 - exp(-(g1*I + g2*D + g3*P + g4*R + g12*I*D + g34*P*R))
# I/D/P/R 为四维成熟度 ∈[0,1]；交互项刻画“制度×数据”“流程×责任”的互补性
g = dict(I=0.55, D=0.85, P=0.60, R=0.50, ID=0.70, PR=0.45)
N = 20000
M = rng.uniform(0, 1, size=(N, 4))
def found(m):
    I, D, P_, R = m[:, 0], m[:, 1], m[:, 2], m[:, 3]
    return 1 - np.exp(-(g["I"] * I + g["D"] * D + g["P"] * P_ + g["R"] * R
                        + g["ID"] * I * D + g["PR"] * P_ * R))
F = found(M)
# 边际贡献：把某一维从当前值提升 0.2（截断于 1）后的风险发现率增量均值
names = ["制度穿透", "数据穿透", "流程穿透", "责任穿透"]
marg = {}
for k, nm in enumerate(names):
    M2 = M.copy(); M2[:, k] = np.minimum(M2[:, k] + 0.2, 1.0)
    marg[nm] = float((found(M2) - F).mean())
order = sorted(marg.items(), key=lambda t: -t[1])
print(f"基准风险发现率均值 = {F.mean()*100:.2f}%（SD={F.std()*100:.2f}）")
for nm, v in order:
    print(f"  {nm} 成熟度 +0.2 → 风险发现率平均提升 {v*100:5.2f} 个百分点")
print(f"→ 实施优先级：{' > '.join(nm for nm, _ in order)}")
# 低成熟度起点（各维 0.2~0.4）下的优先级（更贴近基层现状）
M0 = rng.uniform(0.2, 0.4, size=(N, 4)); F0 = found(M0)
marg0 = {}
for k, nm in enumerate(names):
    M2 = M0.copy(); M2[:, k] = np.minimum(M2[:, k] + 0.2, 1.0)
    marg0[nm] = float((found(M2) - F0).mean())
order0 = sorted(marg0.items(), key=lambda t: -t[1])
print(f"\n低成熟度起点情景（基准发现率 {F0.mean()*100:.2f}%）下的优先级："
      f"{' > '.join(nm for nm, _ in order0)}")
RES["marginal"] = dict(high=marg, low=marg0)

# ============ 5. 分批推行准实验（DID）的最小可检出效应 ============
print("\n" + "=" * 78); print("表E 分批推行 DID 评估的最小可检出效应（MDE）"); print("=" * 78)
from scipy import stats as st
za, zb = st.norm.ppf(0.975), st.norm.ppf(0.80)
sigma, rho_icc = 12.0, 0.15      # 监督效能指数的组内标准差与组内相关系数
print(f"{'单位数 J':>8}{'期数 T':>8}{'MDE(指数点)':>14}{'相对基准60分':>14}")
mde_rows = []
for J in [8, 10, 20, 40, 60]:
    for T in [4, 8]:
        deff = 1 + (T - 1) * rho_icc
        se = sigma * math.sqrt(deff * 4 / (J * T))
        mde = (za + zb) * se
        mde_rows.append((J, T, mde))
        print(f"{J:>8}{T:>8}{mde:>14.2f}{mde/60*100:>13.1f}%")
deff8 = 1 + (8 - 1) * rho_icc
mde8 = (za + zb) * sigma * math.sqrt(deff8 * 4 / (8 * 8))
print(f"\n嘉兴市局现实约束：地市级下辖县区级单位约 8 个，即使观测 8 期，MDE 仍达 {mde8:.2f} 指数点"
      f"（约为基准 60 分的 {mde8/60*100:.1f}%），远大于政策关心的 3 分效应；"
      f"→ 评估单元必须下沉到稽查中队/岗位/业务事项层级（J≥40）才具备统计功效。")
RES["mde"] = mde_rows
RES["mde_J8_T8"] = float(mde8)

# ================================ 绘图 ================================
# 图1 层级衰减与穿透通道
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0))
ax = axes[0]
for i, a in enumerate([0.0, 0.3, 0.6]):
    ax.plot(ks, [efficacy(k, 0.30, a) * 100 for k in ks], marker=["o", "s", "^"][i],
            ms=4.5, color=SEQ[i], ls=["-", "--", "-."][i], label=f"穿透覆盖 a={a:.1f}")
ax.set_xticks(ks); ax.set_xticklabels(["国家局", "省级局", "市级局", "县级局"])
ax.set_ylabel("监督效力（相对国家局 = 100%）")
ax.set_ylim(0, 105); ax.legend(); ax.set_title("(a) 逐级衰减率 d=0.30", fontsize=9.5)
ax = axes[1]
ds = np.linspace(0.05, 0.55, 100)
for i, a in enumerate([0.0, 0.3, 0.6]):
    ax.plot(ds, [efficacy(3, d, a) * 100 for d in ds], color=SEQ[i], ls=["-", "--", "-."][i],
            label=f"a={a:.1f}")
ax.set_xlabel("逐级衰减率 d"); ax.set_ylabel("县级局监督效力 / %")
ax.legend(); ax.set_title("(b) 末梢效力对衰减率的敏感性", fontsize=9.5)
save(fig, OUT + "p2_d1_decay.png")

# 图2 最优监督强度
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0))
ax = axes[0]
ss = np.linspace(0, 10, 400)
ax.plot(ss, base["c"] * ss, color=C["gray"], ls=":", label="直接监督成本")
ax.plot(ss, base["b"] * ss ** 2, color=C["amber"], ls="--", label="基层负担（监督过载）")
ax.plot(ss, base["L"] * base["R0"] * np.exp(-base["beta"] * ss), color=C["sage"],
        ls="-.", label="预期风险损失")
ax.plot(ss, total_cost(ss, **base), color=C["navy"], lw=1.8, label="总成本")
ax.axvline(s_star, color=C["brick"], lw=1.0, ls=(0, (3, 2)))
ax.annotate(f"$s^*$={s_star:.2f}", xy=(s_star, tc_star), xytext=(s_star + 1.1, tc_star + 14),
            fontsize=8.5, color=C["brick"],
            arrowprops=dict(arrowstyle="->", color=C["brick"], lw=0.8))
ax.set_xlabel("监督强度 s"); ax.set_ylabel("成本（无量纲）"); ax.set_ylim(0, 90)
ax.legend(fontsize=7.6); ax.set_title("(a) 总成本分解与最优点", fontsize=9.5)
ax = axes[1]
bs = np.linspace(0.05, 1.0, 60)
ax.plot(bs, [opt_s(b=b)[0] for b in bs], color=C["navy"], label="考虑监督过载")
ax.axhline(s_noload, color=C["brick"], ls="--", lw=1.1, label=f"忽略过载 $s^*$={s_noload:.2f}")
ax.set_xlabel("监督过载系数 b"); ax.set_ylabel("最优监督强度 $s^*$")
ax.legend(); ax.set_title("(b) 最优强度对过载系数的敏感性", fontsize=9.5)
save(fig, OUT + "p2_d2_optimal.png")

# 图3 组合权重
fig, ax = plt.subplots(figsize=(5.2, 3.0))
x = np.arange(len(crit)); w = 0.26
for i, (vals, lab) in enumerate([(w_ahp, "AHP 主观权重"), (w_ent, "熵权客观权重"), (w_comb, "组合权重")]):
    ax.bar(x + (i - 1) * w, vals, w, color=SEQ[i], hatch=HATCH[i], edgecolor="white",
           linewidth=0.6, label=lab)
ax.set_xticks(x); ax.set_xticklabels(crit, fontsize=8)
ax.set_ylabel("权重"); ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.16))
ax.text(0.99, -0.30, f"AHP 判断矩阵一致性检验：CR = {CR:.3f} < 0.10", transform=ax.transAxes,
        ha="right", va="top", fontsize=8, color=C["gray"])
save(fig, OUT + "p2_d3_weights.png")

# 图4 边际贡献龙卷风图
fig, ax = plt.subplots(figsize=(5.0, 2.9))
nm_sorted = [n for n, _ in order0]
y = np.arange(len(nm_sorted))
v_low = [marg0[n] * 100 for n in nm_sorted]
v_high = [marg[n] * 100 for n in nm_sorted]
ax.barh(y + 0.19, v_low, 0.36, color=C["navy"], label="低成熟度起点（0.2~0.4）")
ax.barh(y - 0.19, v_high, 0.36, color=C["amber"], hatch="///", edgecolor="white",
        linewidth=0.5, label="全域随机起点（0~1）")
ax.set_yticks(y); ax.set_yticklabels(nm_sorted)
ax.invert_yaxis()
ax.set_xlabel("成熟度 +0.2 带来的风险发现率提升 / 个百分点")
ax.legend(fontsize=8, loc="lower right")
save(fig, OUT + "p2_d4_marginal.png")

# 图5 DID 功效曲线
fig, ax = plt.subplots(figsize=(4.8, 3.0))
Js = np.arange(6, 81)
for i, T in enumerate([4, 8, 12]):
    deff = 1 + (T - 1) * rho_icc
    mde = (za + zb) * sigma * np.sqrt(deff * 4 / (Js * T))
    ax.plot(Js, mde, color=SEQ[i], ls=["-", "--", "-."][i], label=f"观测期数 T={T}")
ax.axhline(3.0, color=C["brick"], lw=0.9, ls=":")
ax.text(78, 3.3, "政策关心的 3 分效应", ha="right", fontsize=8, color=C["brick"])
ax.set_xlabel("参与分批推行的基层单位数 J")
ax.set_ylabel("最小可检出效应 MDE / 指数点")
ax.legend()
save(fig, OUT + "p2_d5_power.png")

with open("/home/user/xixi/work/analysis/p2_results.json", "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=1, default=float)
print("\n[done] p2")
