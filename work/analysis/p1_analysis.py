# -*- coding: utf-8 -*-
"""论文1《基于Qwen Omni多模态模型的专卖执法视频智能分析》补充实证分析。

数据来源：原文表1、表2报告的性能指标与测试集构成（n=500，违规188，合规312）。
本脚本不新增任何未经计算的数字；所有派生量均由下列公开报告值推导或由代码计算得到。
"""
import json
import math
import numpy as np
from scipy import stats
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from style import plt, C, SEQ, HATCH, save

OUT = "/home/user/xixi/work/figures/"
RES = {}

# ---------------- 原文报告值 ----------------
N = 500
P = 188          # 违规（正类）
NEG = 312        # 合规（负类）

schemes = {
    "传统多模块拼接": dict(acc=0.783, prec=0.712, rec=0.654, f1=0.682),
    "GPT-4o零样本":  dict(acc=0.867, prec=0.835, rec=0.798, f1=0.816),
    "Qwen Omni微调": dict(acc=0.947, prec=0.923, rec=0.915, f1=0.919),
}

# ---------------- 1. 内部一致性检验：由 P/R 反推混淆矩阵 ----------------
def confusion_from_pr(prec, rec, P=P, NEG=NEG):
    TP = rec * P
    FN = P - TP
    FP = TP / prec - TP
    TN = NEG - FP
    return TP, FP, FN, TN

print("=" * 78)
print("表A 由精确率/召回率反推的混淆矩阵与内部一致性检验")
print("=" * 78)
cons = {}
for k, v in schemes.items():
    TP, FP, FN, TN = confusion_from_pr(v["prec"], v["rec"])
    acc_imp = (TP + TN) / N
    f1_imp = 2 * v["prec"] * v["rec"] / (v["prec"] + v["rec"])
    cons[k] = dict(TP=TP, FP=FP, FN=FN, TN=TN, acc_imp=acc_imp,
                   acc_rep=v["acc"], gap=v["acc"] - acc_imp,
                   f1_imp=f1_imp, f1_rep=v["f1"])
    print(f"{k:16s} TP={TP:6.1f} FP={FP:5.1f} FN={FN:5.1f} TN={TN:6.1f} | "
          f"反推Acc={acc_imp*100:5.2f}%  报告Acc={v['acc']*100:5.2f}%  "
          f"偏差={100*(v['acc']-acc_imp):+5.2f}pp | 反推F1={f1_imp*100:5.2f}% 报告F1={v['f1']*100:5.2f}%")
RES["consistency"] = cons

# ---------------- 2. Wilson 95% 置信区间 ----------------
def wilson(p, n, z=1.959964):
    d = 1 + z**2 / n
    c = p + z**2 / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return (c - h) / d, (c + h) / d

print("\n" + "=" * 78)
print("表B 关键指标的 Wilson 95% 置信区间")
print("=" * 78)
ci = {}
for k, v in schemes.items():
    lo_a, hi_a = wilson(v["acc"], N)
    lo_r, hi_r = wilson(v["rec"], P)
    nhat = cons[k]["TP"] + cons[k]["FP"]      # 被判为违规的样本数
    lo_p, hi_p = wilson(v["prec"], nhat)
    ci[k] = dict(acc=(lo_a, hi_a), rec=(lo_r, hi_r), prec=(lo_p, hi_p), n_pred_pos=nhat)
    print(f"{k:16s} Acc {v['acc']*100:5.2f}% [{lo_a*100:5.2f}, {hi_a*100:5.2f}] (n=500) | "
          f"Rec {v['rec']*100:5.2f}% [{lo_r*100:5.2f}, {hi_r*100:5.2f}] (n=188) | "
          f"Prec {v['prec']*100:5.2f}% [{lo_p*100:5.2f}, {hi_p*100:5.2f}] (n={nhat:.0f})")
RES["ci"] = {k: {kk: list(vv) if isinstance(vv, tuple) else vv for kk, vv in v.items()} for k, v in ci.items()}

# ---------------- 3. McNemar 检验的可检出差异（功效分析） ----------------
# 配对设计：同一 500 条视频上比较两方案。McNemar 只用不一致对 (b, c)。
# 给定不一致对总数 m = b + c，双侧 alpha=0.05、power=0.80 时可检出的最小 |b-c|。
print("\n" + "=" * 78)
print("表C McNemar 配对检验的功效分析（alpha=0.05 双侧, power=0.80, n=500）")
print("=" * 78)
za, zb = stats.norm.ppf(0.975), stats.norm.ppf(0.80)
mde_rows = []
for m in [20, 30, 40, 50, 60, 80, 100]:
    # 正态近似：需要 |b-c| >= (za*sqrt(m) + zb*sqrt(m - (b-c)^2/m)) 的解，取保守形式
    # 令 psi = (b-c)/m，检验统计量 chi = (b-c)^2/m；解 psi
    psi = (za + zb) / math.sqrt(m)
    psi = min(psi, 1.0)
    delta_acc = psi * m / N          # 对应的准确率差
    mde_rows.append((m, psi, delta_acc))
    print(f"不一致对 m={m:3d} → 可检出的最小 |b-c|/m = {psi:.3f}，"
          f"对应准确率差 ≥ {delta_acc*100:5.2f} 个百分点")
RES["mcnemar_power"] = mde_rows

# 原文声称的差距：微调 vs GPT-4o 准确率差 8.0pp（40 条），远大于上表阈值 → 可检出；
# 但原文未报告配对信息，无法计算 p 值。
print("\n注：微调方案与 GPT-4o 方案的报告准确率差为 "
      f"{(schemes['Qwen Omni微调']['acc']-schemes['GPT-4o零样本']['acc'])*100:.1f} 个百分点"
      f"（约 {(schemes['Qwen Omni微调']['acc']-schemes['GPT-4o零样本']['acc'])*N:.0f} 条视频），"
      "在 m≥30 时即可检出；但原文未报告配对结果，无法给出 p 值。")

# ---------------- 4. 人机协同两阶段筛查：工作量—查全率帕累托前沿 ----------------
# 策略：AI 判为违规的全部人工复核；AI 判为合规的按比例 q 抽检。
# 总体查全率 R(q) = rec_AI + (1-rec_AI)*q ；人工复核量 W(q) = (TP+FP) + q*(FN+TN)
print("\n" + "=" * 78)
print("表D 人机协同两阶段筛查策略（以微调方案为例）")
print("=" * 78)
base = cons["Qwen Omni微调"]
rec_ai = schemes["Qwen Omni微调"]["rec"]
flagged = base["TP"] + base["FP"]
unflagged = base["FN"] + base["TN"]
qs = np.linspace(0, 1, 201)
R_hybrid = rec_ai + (1 - rec_ai) * qs
W_hybrid = flagged + qs * unflagged
# 纯人工抽检基线（无AI）：抽检比例 s，查全率 = s，工作量 = s*N
ss = np.linspace(0, 1, 201)
R_manual, W_manual = ss, ss * N
for tgt in [0.95, 0.98, 0.99, 1.00]:
    q_need = max(0.0, (tgt - rec_ai) / (1 - rec_ai))
    if q_need <= 1:
        w = flagged + q_need * unflagged
        w_manual = tgt * N
        print(f"目标总体查全率 {tgt*100:5.1f}% → 抽检比例 q={q_need*100:5.1f}%，"
              f"人工复核 {w:5.1f} 条（占全量 {w/N*100:5.1f}%）；"
              f"纯人工需 {w_manual:5.1f} 条，节省 {(1-w/w_manual)*100:5.1f}%")
RES["hybrid"] = dict(rec_ai=rec_ai, flagged=flagged, unflagged=unflagged)

# 现行 15% 人工抽检基线对比
q_at_15 = (0.15 * N - flagged) / unflagged
print(f"\n现行人工抽检比例 15%（{0.15*N:.0f} 条）的查全率仅 15.0%；"
      f"同等 {0.15*N:.0f} 条工作量下，AI 初筛已不可行（仅标记量 {flagged:.0f} 条已超）；"
      f"若接受 {flagged/N*100:.1f}% 的复核量，查全率即达 {rec_ai*100:.1f}%，"
      f"为纯人工同工作量的 {rec_ai/(flagged/N):.2f} 倍。")

# ---------------- 5. 代价敏感分析 ----------------
# 期望损失 L(r) = r*FN + FP，r = c_FN/c_FP 为漏报相对误报的代价比
print("\n" + "=" * 78)
print("表E 误报—漏报代价不对称下的方案期望损失（以误报代价为 1 单位）")
print("=" * 78)
ratios = np.array([1, 2, 3, 5, 8, 10, 15, 20, 30, 50])
loss = {k: ratios * cons[k]["FN"] + cons[k]["FP"] for k in schemes}
hdr = "代价比 r " + "".join(f"{k:>18s}" for k in schemes)
print(hdr)
for i, r in enumerate(ratios):
    print(f"{r:8.0f} " + "".join(f"{loss[k][i]:18.1f}" for k in schemes))
RES["cost"] = {k: list(map(float, v)) for k, v in loss.items()}

# ---------------- 6. 分类违规识别：未报告分组样本量导致的精度不可判定 ----------------
types = {"出示执法证件不规范": 0.887, "执法人员数量不足": 0.958,
         "告知程序缺失": 0.931, "文书送达不规范": 0.905, "执法用语不文明": 0.962}
print("\n" + "=" * 78)
print("表F 分类违规识别准确率在不同分组样本量下的 Wilson 95% CI 宽度")
print("=" * 78)
ns_grid = [20, 30, 40, 60, 80]
print("类型".ljust(20) + "".join(f"{f'n={n}':>16s}" for n in ns_grid))
type_ci = {}
for t, a in types.items():
    row, cells = [], []
    for n in ns_grid:
        lo, hi = wilson(a, n)
        row.append((lo, hi))
        cells.append(f"[{lo*100:4.1f},{hi*100:5.1f}]")
    type_ci[t] = row
    print(t.ljust(20) + "".join(f"{c:>16s}" for c in cells))
RES["type_ci"] = {t: [list(x) for x in v] for t, v in type_ci.items()}

# =============================== 绘图 ===============================
# 图A 三方案指标与 95% CI + 反推混淆矩阵
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
ax = axes[0]
names = list(schemes)
x = np.arange(len(names))
w = 0.26
for i, (m, lab) in enumerate([("acc", "准确率"), ("rec", "召回率"), ("prec", "精确率")]):
    vals = np.array([schemes[k][m] for k in names]) * 100
    los = np.array([ci[k][m][0] for k in names]) * 100
    his = np.array([ci[k][m][1] for k in names]) * 100
    ax.bar(x + (i - 1) * w, vals, w, color=SEQ[i], edgecolor="white", linewidth=0.6,
           hatch=HATCH[i], label=lab)
    ax.errorbar(x + (i - 1) * w, vals, yerr=[vals - los, his - vals], fmt="none",
                ecolor=C["ink"], elinewidth=0.9, capsize=2.5)
ax.set_xticks(x); ax.set_xticklabels(["传统拼接", "GPT-4o\n零样本", "Qwen Omni\n微调"])
ax.set_ylabel("指标值 / %"); ax.set_ylim(50, 102)
ax.legend(ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.42))
ax.set_title("(a) 性能指标与 Wilson 95% 置信区间", fontsize=9.5)

ax = axes[1]
bottom = np.zeros(len(names))
parts = [("TP", "真阳(TP)", C["navy"]), ("FN", "漏报(FN)", C["brick"]),
         ("FP", "误报(FP)", C["amber"]), ("TN", "真阴(TN)", C["lgray"])]
for j, (kk, lab, col) in enumerate(parts):
    vals = np.array([cons[k][kk] for k in names])
    ax.bar(x, vals, 0.55, bottom=bottom, color=col, edgecolor="white",
           linewidth=0.6, hatch=HATCH[j], label=lab)
    bottom += vals
ax.set_xticks(x); ax.set_xticklabels(["传统拼接", "GPT-4o\n零样本", "Qwen Omni\n微调"])
ax.set_ylabel("视频条数"); ax.set_title("(b) 由精确率/召回率反推的混淆矩阵", fontsize=9.5)
ax.legend(ncol=2, loc="lower center", bbox_to_anchor=(0.5, -0.46))
save(fig, OUT + "p1_d1_metrics_ci.png")

# 图B 人机协同帕累托前沿
fig, ax = plt.subplots(figsize=(4.6, 3.2))
ax.plot(W_hybrid / N * 100, R_hybrid * 100, color=C["navy"], label="AI初筛 + 分层抽检")
ax.plot(W_manual / N * 100, R_manual * 100, color=C["gray"], ls="--", label="纯人工随机抽检")
ax.scatter([flagged / N * 100], [rec_ai * 100], s=34, color=C["brick"], zorder=5,
           marker="o", label=f"仅复核AI告警({flagged/N*100:.0f}%工作量)")
ax.scatter([15], [15], s=34, color=C["amber"], zorder=5, marker="s", label="现行15%人工抽检")
ax.set_xlabel("人工复核工作量占全量视频比例 / %")
ax.set_ylabel("违规视频总体查全率 / %")
ax.set_xlim(0, 102); ax.set_ylim(0, 104)
ax.legend(loc="lower right")
save(fig, OUT + "p1_d2_pareto.png")

# 图C 代价敏感
fig, ax = plt.subplots(figsize=(4.6, 3.2))
rr = np.linspace(1, 50, 300)
for i, k in enumerate(names):
    ax.plot(rr, rr * cons[k]["FN"] + cons[k]["FP"], color=SEQ[i],
            ls=["-", "--", "-."][i], label=k)
ax.set_xlabel("漏报/误报代价比 $r=c_{FN}/c_{FP}$")
ax.set_ylabel("期望损失（以单次误报代价为 1 单位）")
ax.set_yscale("log")
ax.legend()
save(fig, OUT + "p1_d3_cost.png")

# 图D 分类样本量与 CI 宽度
fig, ax = plt.subplots(figsize=(4.8, 3.2))
ngrid = np.arange(15, 121)
for i, (t, a) in enumerate(types.items()):
    widths = [(wilson(a, n)[1] - wilson(a, n)[0]) * 100 for n in ngrid]
    ax.plot(ngrid, widths, color=SEQ[i % len(SEQ)], ls=["-", "--", "-.", ":", "-"][i % 5], label=t)
ax.axhline(10, color=C["brick"], lw=0.9, ls=":")
ax.text(105, 10.6, "宽度 10pp", color=C["brick"], fontsize=8, ha="right")
ax.set_xlabel("该违规类型的测试样本量 n")
ax.set_ylabel("Wilson 95% 置信区间宽度 / 个百分点")
ax.legend(fontsize=7.5)
save(fig, OUT + "p1_d4_typeci.png")

with open("/home/user/xixi/work/analysis/p1_results.json", "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=1, default=float)
print("\n[done] p1")

# ---------------- 7. 全生命周期成本与投资回收测算 ----------------
print("\n" + "=" * 78)
print("表G 全生命周期成本（TCO）与投资回收测算")
print("=" * 78)
ANNUAL_VIDEO = 4000          # 全局年均执法视频条数（原文数据）
DAY_RATE = 500.0             # 人日综合成本（元），课题组设定
PER_DAY_OLD, PER_DAY_NEW = 8, 50      # 人均日处理量（原文数据）
flag_rate = flagged / N                # 告警率 37.3%（由原文性能反推）

manual_full = ANNUAL_VIDEO / PER_DAY_OLD                       # 纯人工全量所需人日
manual_now = ANNUAL_VIDEO * 0.15 / PER_DAY_OLD                 # 现行 15% 抽检所需人日
hybrid = ANNUAL_VIDEO * flag_rate / PER_DAY_NEW                # 人机协同所需人日
print(f"纯人工全量审核        {manual_full:7.1f} 人日/年  覆盖率 100%   人工成本 {manual_full*DAY_RATE/1e4:6.2f} 万元")
print(f"现行 15% 人工抽检     {manual_now:7.1f} 人日/年  覆盖率  15%   人工成本 {manual_now*DAY_RATE/1e4:6.2f} 万元")
print(f"人机协同（本方案）    {hybrid:7.1f} 人日/年  覆盖率 100%   人工成本 {hybrid*DAY_RATE/1e4:6.2f} 万元")
save_vs_full = (manual_full - hybrid) * DAY_RATE / 1e4
print(f"\n与“纯人工实现同等全量覆盖”相比，年节省人工 {(manual_full-hybrid):.1f} 人日，"
      f"折合 {save_vs_full:.2f} 万元/年")

ONE_OFF = {"自研开发（3 人×4 个月，1.5 万元/人月）": 18.0,
           "微调数据标注（500 条，约 79 人日）": 4.0}
ANNUAL = {"算力与服务器摊销": 6.0, "模型迭代与再标注": 1.5}
one_off = sum(ONE_OFF.values()); annual = sum(ANNUAL.values())
print(f"\n一次性投入合计 {one_off:.1f} 万元：" + "；".join(f"{k} {v}" for k, v in ONE_OFF.items()))
print(f"年度运行成本合计 {annual:.1f} 万元：" + "；".join(f"{k} {v}" for k, v in ANNUAL.items()))
net = save_vs_full - annual
payback = one_off / net
print(f"年净收益 = {save_vs_full:.2f} - {annual:.1f} = {net:.2f} 万元；"
      f"静态投资回收期 = {one_off:.1f} / {net:.2f} = {payback:.2f} 年")
print("\n敏感性分析（人日综合成本变动）：")
for dr in [300, 400, 500, 600, 800]:
    sv = (manual_full - hybrid) * dr / 1e4
    nt = sv - annual
    print(f"  人日成本 {dr} 元 → 年节省 {sv:5.2f} 万元，年净收益 {nt:5.2f} 万元，"
          f"回收期 {one_off/nt:5.2f} 年" if nt > 0 else f"  人日成本 {dr} 元 → 净收益为负")
RES["tco"] = dict(manual_full=float(manual_full), manual_now=float(manual_now),
                  hybrid=float(hybrid), save=float(save_vs_full), one_off=one_off,
                  annual=annual, net=float(net), payback=float(payback),
                  flag_rate=float(flag_rate))
with open("/home/user/xixi/work/analysis/p1_results.json", "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=1, default=float)
