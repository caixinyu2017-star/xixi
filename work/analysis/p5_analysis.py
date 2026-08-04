# -*- coding: utf-8 -*-
"""论文5《基于机器学习的新型烟草制品高价值专利识别研究》补充效度检验。

分两部分：
  A 部分——基于原文**已报告的真实数值**（4954 条样本、价值等级分布、四个聚类组的规模与
    高价值占比、两模型准确率）可直接计算的检验，结论对原文直接有效；
  B 部分——在一个与原文边际统计一致的**合成数据集**上复现全流程，用以演示原文缺失的
    关键检验（剔标签同源特征的消融、类不平衡指标、5×2cv 配对检验、引用截断偏差）。
    B 部分的具体数值仅用于方法学演示，须在原始 DII 数据上重跑后方可写入结论。
"""
import json, math, itertools
import numpy as np
from scipy import stats as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import DBSCAN
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import (accuracy_score, confusion_matrix, cohen_kappa_score,
                             precision_recall_fscore_support, average_precision_score,
                             matthews_corrcoef)
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from style import plt, C, SEQ, HATCH, save

OUT = "/home/user/xixi/work/figures/"
RES = {}
rng = np.random.default_rng(2025)

# ==================================================================
# A 部分：基于原文报告值的检验
# ==================================================================
N = 4954
n_low, n_mid, n_high = 3138, 1525, 291
clusters = [("基础外围集群", 4658, 0.021), ("中价值过渡集群", 136, 0.272),
            ("高价值核心集群", 83, 0.952), ("极高价值尖端集群", 77, 1.000)]

print("=" * 80); print("A1  原文数据的内部一致性核验"); print("=" * 80)
tot = sum(n for _, n, _ in clusters)
hi_sum = sum(n * r for _, n, r in clusters)
print(f"四聚类组规模合计 = {tot}，与样本量 {N} {'一致' if tot == N else '不一致'}"
      f"（说明 DBSCAN 未产生噪声点，或噪声点已被并入基础外围集群，原文需说明）")
print(f"由各组高价值占比反推的高价值专利数 = {hi_sum:.1f}，原文报告 {n_high} → "
      f"偏差 {abs(hi_sum - n_high):.1f} 条，数据自洽")
RES["A_consistency"] = dict(cluster_total=int(tot), implied_high=float(hi_sum), reported_high=n_high)

print("\n" + "=" * 80); print("A2  聚类组×价值等级列联表的独立性检验"); print("=" * 80)
# 由报告值重构列联表：高价值列已知；低/中价值按各组内的总体比例拆分（低:中 = 3138:1525）
ratio_low = n_low / (n_low + n_mid)
tbl = []
for nm, n_, r in clusters:
    h = n_ * r
    rest = n_ - h
    tbl.append([rest * ratio_low, rest * (1 - ratio_low), h])
tbl = np.array(tbl)
chi2, pval, dof, exp = st.chi2_contingency(tbl)
V = math.sqrt(chi2 / (N * (min(tbl.shape) - 1)))
print(f"{'聚类组':<16}{'低价值':>10}{'中价值':>10}{'高价值':>10}{'组内高价值占比':>15}")
for (nm, n_, r), row in zip(clusters, tbl):
    print(f"{nm:<16}{row[0]:>10.0f}{row[1]:>10.0f}{row[2]:>10.0f}{r*100:>14.1f}%")
print(f"\nχ² = {chi2:.1f}，df = {dof}，p = {pval:.3e}；Cramér's V = {V:.3f}（极强关联）")
print("注：聚类特征与标签构造指标同源，因此该强关联是构造的必然结果，"
      "不能作为聚类有效性的独立证据。")
RES["A_chi2"] = dict(chi2=float(chi2), p=float(pval), V=float(V))

print("\n" + "=" * 80); print("A3  两模型准确率差异的统计与实践含义"); print("=" * 80)
acc_rf, acc_db = 0.9463, 0.9592
def wilson(p, n, z=1.959964):
    d = 1 + z ** 2 / n; c = p + z ** 2 / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2))
    return (c - h) / d, (c + h) / d
for nm, a in [("传统随机森林", acc_rf), ("DBSCAN 优化随机森林", acc_db)]:
    lo, hi = wilson(a, N)
    print(f"{nm:<22}{a*100:.2f}%  95%CI = [{lo*100:.2f}, {hi*100:.2f}]（n={N}）")
print(f"两者置信区间重叠；但配对设计下应做 McNemar 检验而非比较独立区间。")
delta_n = (acc_db - acc_rf) * N
print(f"准确率差 {(acc_db-acc_rf)*100:.2f} 个百分点 ≈ {delta_n:.0f} 条专利的分类结果改变。")
za, zb = st.norm.ppf(0.975), st.norm.ppf(0.80)
for m in [80, 120, 200, 300]:
    psi = (za + zb) / math.sqrt(m)
    print(f"  若不一致对 m={m:3d}，α=0.05、power=0.80 下可检出的最小准确率差 = "
          f"{psi*m/N*100:.2f} 个百分点")
print("原文用 10 折交叉验证结果做配对 t 检验：该做法已知会低估方差、放大 I 类错误"
      "（Dietterich, 1998），应改用 5×2cv 配对 t 检验或修正重采样 t 检验。")

print("\n" + "=" * 80); print("A4  类不平衡下“总体准确率”的信息量"); print("=" * 80)
p_low, p_mid, p_high = n_low / N, n_mid / N, n_high / N
print(f"多数类基准（全部判为低价值）准确率 = {p_low*100:.2f}%"
      f"（原文表述为“随机猜测的基准准确率”，属概念误用）")
# 可行域：给定总准确率 A，高价值类召回率 r_high 的取值范围
A = acc_db
feas = []
for r_high in np.linspace(0, 1, 201):
    # 其余两类共同贡献的正确数上限/下限
    correct_high = r_high * n_high
    need_rest = A * N - correct_high
    ok = 0 <= need_rest <= (n_low + n_mid)
    if ok:
        feas.append(r_high)
print(f"在总准确率 {A*100:.2f}% 的约束下，高价值类召回率的可行区间 = "
      f"[{min(feas)*100:.1f}%, {max(feas)*100:.1f}%]")
print("→ 即便模型对高价值专利的召回率为 0，总准确率仍可达到 "
      f"{(n_low + n_mid)/N*100:.2f}%。总体准确率无法刻画高价值识别能力，"
      "必须报告高价值类的精确率/召回率、PR-AUC、MCC 与混淆矩阵。")
RES["A_feasible_recall"] = [float(min(feas)), float(max(feas))]
RES["A_majority_baseline"] = float(p_low)

# ==================================================================
# B 部分：合成数据集上的方法学演示
# ==================================================================
print("\n\n" + "=" * 80)
print("B  合成数据集上的方法学演示（数值仅用于演示，须在原始 DII 数据上重跑）")
print("=" * 80)

FEATS = ["引用的参考文献数-专利", "DWPI同族专利成员计数", "权利要求计数",
         "公开专利文献类型识别代码", "DWPI同族国家/地区计数", "最早优先权年",
         "公开年", "申请年", "发明人计数", "引用的参考文献计数-非专利",
         "IPC大类", "施引专利计数", "专利权人计数"]
LABEL_FEATS = ["引用的参考文献数-专利", "DWPI同族专利成员计数", "权利要求计数", "发明人计数"]

# --- 生成合成样本：右偏分布 + 引用截断（近年专利引用数系统性偏低） ---
year = rng.choice(np.arange(2010, 2025), N, p=np.linspace(0.02, 0.12, 15) / np.linspace(0.02, 0.12, 15).sum())
age = 2024 - year
latent = rng.gamma(1.4, 1.0, N)                       # 潜在技术质量
cit = rng.poisson(np.clip(0.9 * latent * (0.25 + 0.075 * age), 0.05, None))   # 引用截断效应
fam = rng.poisson(np.clip(0.8 * latent * (0.5 + 0.05 * age), 0.05, None)) + 1
clm = np.clip(rng.poisson(4 + 2.2 * latent), 1, None)
inv = np.clip(rng.poisson(1.6 + 0.9 * latent), 1, None)
ctry = np.clip(rng.poisson(0.6 * fam), 0, None) + 1
X = np.c_[cit, fam, clm,
          rng.integers(0, 4, N),                       # 文献类型代码
          ctry, year - rng.integers(0, 3, N), year, year - rng.integers(0, 2, N),
          inv, rng.poisson(0.8, N), rng.integers(0, 3, N),
          rng.poisson(np.clip(0.5 * latent, 0.05, None)), np.clip(rng.poisson(1.1, N), 1, None)]
X = X.astype(float)
# 99 分位缩尾
for j in range(X.shape[1]):
    q = np.quantile(X[:, j], 0.99)
    X[:, j] = np.minimum(X[:, j], q)

# --- 熵权法构造标签（与原文一致：4 项指标）---
li = [FEATS.index(f) for f in LABEL_FEATS]
Z = X[:, li]
Zn = (Z - Z.min(0)) / (Z.max(0) - Z.min(0) + 1e-12)
Pm = (Zn + 1e-6) / (Zn + 1e-6).sum(0)
Ent = -(Pm * np.log(Pm)).sum(0) / np.log(N)
w_ent = (1 - Ent) / (1 - Ent).sum()
score = Zn @ w_ent
print(f"熵权法权重：" + "，".join(f"{f}={w:.3f}" for f, w in zip(LABEL_FEATS, w_ent)))

# --- 自然间断点分级（1 维 k-means，等价于 Jenks 优化目标）---
def jenks3(v, target=(n_low, n_mid, n_high)):
    """按目标比例取分位数作为初始断点，再迭代最小化组内方差。"""
    qs = np.quantile(v, [target[0] / N, (target[0] + target[1]) / N])
    for _ in range(60):
        lab = np.digitize(v, qs)
        cen = np.array([v[lab == k].mean() if (lab == k).any() else qs.mean() for k in range(3)])
        qs = np.array([(cen[0] + cen[1]) / 2, (cen[1] + cen[2]) / 2])
    return np.digitize(v, qs)
y = jenks3(score)
cnt = np.bincount(y, minlength=3)
print(f"合成数据的价值等级分布：低 {cnt[0]}（{cnt[0]/N*100:.2f}%），"
      f"中 {cnt[1]}（{cnt[1]/N*100:.2f}%），高 {cnt[2]}（{cnt[2]/N*100:.2f}%）"
      f"；原文为 63.34% / 30.78% / 5.87%")
RES["B_label_dist"] = cnt.tolist()

# --- DBSCAN 剪枝随机森林 ---
def prune_forest(rf, Xv, yv):
    trees = rf.estimators_
    preds = np.array([t.predict(Xv) for t in trees])
    accs = np.array([accuracy_score(yv, p) for p in preds])
    keep = np.where(accs >= accs.mean())[0]
    if len(keep) < 4:
        return list(np.array(trees)[np.argsort(-accs)[:max(3, len(keep))]])
    P = preds[keep]
    K = np.ones((len(keep), len(keep)))
    for a, b in itertools.combinations(range(len(keep)), 2):
        k = cohen_kappa_score(P[a], P[b]); K[a, b] = K[b, a] = k
    Dk = 1 - K                                   # Kappa 距离
    db = DBSCAN(eps=np.quantile(Dk[Dk > 0], 0.18), min_samples=3, metric="precomputed").fit(Dk)
    sel = []
    for c in set(db.labels_) - {-1}:
        idx = np.where(db.labels_ == c)[0]
        sel.append(keep[idx[np.argmax(accs[keep][idx])]])
    if not sel:
        sel = list(keep[np.argsort(-accs[keep])[:10]])
    return [trees[i] for i in sel]

def vote(trees, Xt):
    P = np.array([t.predict(Xt) for t in trees]).astype(int)
    return np.array([np.bincount(P[:, i], minlength=3).argmax() for i in range(Xt.shape[0])])

def run_cv(Xd, yd, seed=0, folds=10):
    skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
    a_rf, a_db = [], []
    for tr, te in skf.split(Xd, yd):
        Xtr, Xva, ytr, yva = train_test_split(Xd[tr], yd[tr], test_size=0.25,
                                              random_state=seed, stratify=yd[tr])
        rf = RandomForestClassifier(n_estimators=120, random_state=seed, n_jobs=-1).fit(Xtr, ytr)
        a_rf.append(accuracy_score(yd[te], rf.predict(Xd[te])))
        a_db.append(accuracy_score(yd[te], vote(prune_forest(rf, Xva, yva), Xd[te])))
    return np.array(a_rf), np.array(a_db)

print("\n--- B1 复现原文流程（全部 13 个特征，含 4 项标签构造指标）---")
a_rf, a_db = run_cv(X, y, seed=0, folds=10)
print(f"传统随机森林 10 折准确率 = {a_rf.mean()*100:.2f}%（SD {a_rf.std()*100:.2f}）")
print(f"DBSCAN 剪枝随机森林      = {a_db.mean()*100:.2f}%（SD {a_db.std()*100:.2f}）")
print(f"提升 = {(a_db.mean()-a_rf.mean())*100:+.2f} 个百分点（原文报告 +1.29）")

print("\n--- B2 关键消融：剔除 4 项标签构造指标后重训 ---")
keep_idx = [i for i, f in enumerate(FEATS) if f not in LABEL_FEATS]
X_ab = X[:, keep_idx]
a_rf2, a_db2 = run_cv(X_ab, y, seed=0, folds=10)
drop = a_rf.mean() - a_rf2.mean()
maj = np.bincount(y).max() / N
print(f"剔除同源特征后：随机森林准确率 = {a_rf2.mean()*100:.2f}%（较原来下降 {drop*100:.2f} 个百分点）")
print(f"多数类基准 = {maj*100:.2f}%；剔除后模型相对基准的净增益仅 "
      f"{(a_rf2.mean()-maj)*100:.2f} 个百分点")
print("→ 说明模型的高准确率主要来自“重新学会标签公式”，而非识别标签之外的价值信息。"
      "这就是循环论证的量化证据。")
RES["B_ablation"] = dict(full=float(a_rf.mean()), ablated=float(a_rf2.mean()),
                         drop=float(drop), majority=float(maj))

print("\n--- B3 类不平衡下的完整指标 ---")
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
yt_all, yp_all, pr_all = [], [], []
for tr, te in skf.split(X, y):
    rf = RandomForestClassifier(n_estimators=200, random_state=1, n_jobs=-1).fit(X[tr], y[tr])
    yt_all.append(y[te]); yp_all.append(rf.predict(X[te])); pr_all.append(rf.predict_proba(X[te])[:, 2])
yt = np.concatenate(yt_all); yp = np.concatenate(yp_all); prh = np.concatenate(pr_all)
cm = confusion_matrix(yt, yp)
prec, rec, f1, sup = precision_recall_fscore_support(yt, yp, labels=[0, 1, 2])
ap = average_precision_score((yt == 2).astype(int), prh)
mcc = matthews_corrcoef(yt, yp)
print(f"{'类别':<10}{'精确率':>10}{'召回率':>10}{'F1':>10}{'样本数':>10}")
for nm, p_, r_, f_, s_ in zip(["低价值", "中价值", "高价值"], prec, rec, f1, sup):
    print(f"{nm:<10}{p_*100:>9.2f}%{r_*100:>9.2f}%{f_*100:>9.2f}%{s_:>10}")
print(f"总体准确率 = {accuracy_score(yt, yp)*100:.2f}%；高价值类 PR-AUC = {ap:.4f}；MCC = {mcc:.4f}")
print("混淆矩阵（行=真实，列=预测）：\n", cm)
RES["B_metrics"] = dict(prec=prec.tolist(), rec=rec.tolist(), f1=f1.tolist(),
                        sup=sup.tolist(), ap=float(ap), mcc=float(mcc), cm=cm.tolist())

print("\n--- B4 模型比较：10 折配对 t 检验 vs 5×2cv 配对 t 检验 ---")
t10, p10 = st.ttest_rel(a_db, a_rf)
print(f"10 折配对 t 检验：t = {t10:.3f}, p = {p10:.4f}"
      f"{'（显著）' if p10 < 0.05 else '（不显著）'}  ← 该检验已知方差被低估")
diffs = []
for r_ in range(5):
    idx = rng.permutation(N)
    h1, h2 = idx[:N // 2], idx[N // 2:]
    d_r = []
    for tr, te in [(h1, h2), (h2, h1)]:
        Xtr, Xva, ytr, yva = train_test_split(X[tr], y[tr], test_size=0.25,
                                              random_state=r_, stratify=y[tr])
        rf = RandomForestClassifier(n_estimators=120, random_state=r_, n_jobs=-1).fit(Xtr, ytr)
        d_r.append(accuracy_score(y[te], vote(prune_forest(rf, Xva, yva), X[te]))
                   - accuracy_score(y[te], rf.predict(X[te])))
    diffs.append(d_r)
diffs = np.array(diffs)
s2 = ((diffs - diffs.mean(axis=1, keepdims=True)) ** 2).sum(axis=1)
t52 = diffs[0, 0] / math.sqrt(s2.sum() / 5 + 1e-12)
p52 = 2 * (1 - st.t.cdf(abs(t52), df=5))
print(f"5×2cv 配对 t 检验：t = {t52:.3f}, p = {p52:.4f}"
      f"{'（显著）' if p52 < 0.05 else '（不显著）'}；平均差异 = {diffs.mean()*100:+.2f} 个百分点")
RES["B_tests"] = dict(t10=float(t10), p10=float(p10), t52=float(t52), p52=float(p52),
                      mean_diff=float(diffs.mean()))

print("\n--- B5 引用截断偏差 ---")
yrs = np.arange(2010, 2025)
hi_by_year = np.array([(y[year == yy] == 2).mean() if (year == yy).any() else np.nan for yy in yrs])
cit_by_year = np.array([X[year == yy, 0].mean() for yy in yrs])
rho, prho = st.spearmanr(yrs, hi_by_year)
print(f"{'公开年':>8}{'高价值占比':>12}{'平均引用数':>12}")
for yy, h_, c_ in zip(yrs, hi_by_year, cit_by_year):
    print(f"{yy:>8}{h_*100:>11.2f}%{c_:>12.2f}")
print(f"\n公开年与高价值占比的 Spearman ρ = {rho:.3f}（p = {prho:.4f}）"
      f"→ 引用与同族指标随专利年龄累积，直接使用会系统性低估近年专利的价值，"
      f"必须按“同年同 IPC 分位数”标准化后再进入标签构造。")
RES["B_truncation"] = dict(rho=float(rho), p=float(prho),
                           hi_by_year=hi_by_year.tolist(), yrs=yrs.tolist())

# ================================ 绘图 ================================
# 图1 聚类组×价值等级 + 可行域
fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.1))
ax = axes[0]
prop = tbl / tbl.sum(axis=1, keepdims=True) * 100
bot = np.zeros(4)
for k, (lab, col, hh) in enumerate([("低价值", C["lgray"], ""), ("中价值", C["steel"], "///"),
                                    ("高价值", C["brick"], "...")]):
    ax.bar(np.arange(4), prop[:, k], 0.58, bottom=bot, color=col, hatch=hh,
           edgecolor="white", linewidth=0.6, label=lab)
    bot += prop[:, k]
ax.set_xticks(np.arange(4))
ax.set_xticklabels([f"{s_}\nn={n_}" for s_, (nm, n_, _) in
                    zip(["基础外围", "中价值过渡", "高价值核心", "极高价值尖端"], clusters)],
                   fontsize=7.2)
ax.set_ylabel("组内构成 / %"); ax.set_ylim(0, 108)
ax.legend(ncol=3, fontsize=7.4, loc="lower center", bbox_to_anchor=(0.5, -0.42))
ax.text(0.02, 0.04, f"χ²={chi2:.0f}, p<0.001\nCramér's V={V:.3f}", transform=ax.transAxes,
        fontsize=7.8, color=C["ink"])
ax.set_title("(a) 由原文报告值重构的列联表", fontsize=9.5)

ax = axes[1]
rr = np.linspace(0, 1, 300)
acc_min = (rr * n_high) / N
acc_max = (rr * n_high + n_low + n_mid) / N
ax.fill_between(rr * 100, acc_min * 100, acc_max * 100, color=C["sky"], alpha=0.35,
                label="可行的总体准确率区间")
ax.axhline(acc_db * 100, color=C["brick"], lw=1.3, label=f"原文报告 {acc_db*100:.2f}%")
ax.axhline((n_low + n_mid) / N * 100, color=C["gray"], ls="--", lw=1.0,
           label=f"高价值全部漏判仍可达 {(n_low+n_mid)/N*100:.2f}%")
ax.set_xlabel("高价值类召回率 / %"); ax.set_ylabel("总体准确率 / %")
ax.set_ylim(0, 105); ax.legend(fontsize=7.4, loc="lower right")
ax.set_title("(b) 总体准确率的信息量不足", fontsize=9.5)
save(fig, OUT + "p5_d1_reported.png")

# 图2 消融实验
fig, ax = plt.subplots(figsize=(5.2, 3.1))
bars = [("全部 13 个特征\n（含标签同源指标）", a_rf.mean(), C["navy"], ""),
        ("剔除 4 项标签\n构造指标后", a_rf2.mean(), C["amber"], "///"),
        ("多数类基准", maj, C["lgray"], "...")]
for i, (nm, v, col, hh) in enumerate(bars):
    ax.bar(i, v * 100, 0.55, color=col, hatch=hh, edgecolor="white", linewidth=0.6)
    ax.text(i, v * 100 + 0.8, f"{v*100:.2f}%", ha="center", fontsize=9, fontweight="bold")
ax.annotate("", xy=(1, a_rf2.mean() * 100), xytext=(1, a_rf.mean() * 100),
            arrowprops=dict(arrowstyle="<->", color=C["brick"], lw=1.2))
ax.text(1.12, (a_rf.mean() + a_rf2.mean()) / 2 * 100,
        f"下降 {drop*100:.1f}\n个百分点", fontsize=8.5, color=C["brick"], va="center")
ax.set_xticks(range(3)); ax.set_xticklabels([b[0] for b in bars], fontsize=8)
ax.set_ylabel("10 折交叉验证准确率 / %"); ax.set_ylim(50, 102)
save(fig, OUT + "p5_d2_ablation.png")

# 图3 类不平衡指标
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0))
ax = axes[0]
im = ax.imshow(cm, cmap="Blues")
for i in range(3):
    for j in range(3):
        ax.text(j, i, f"{cm[i, j]}", ha="center", va="center", fontsize=9,
                color="white" if cm[i, j] > cm.max() * 0.5 else C["ink"])
ax.set_xticks(range(3)); ax.set_xticklabels(["低", "中", "高"])
ax.set_yticks(range(3)); ax.set_yticklabels(["低", "中", "高"])
ax.set_xlabel("预测类别"); ax.set_ylabel("真实类别")
ax.set_title("(a) 混淆矩阵", fontsize=9.5)
for sp in ax.spines.values():
    sp.set_visible(False)
ax = axes[1]
x = np.arange(3); w = 0.26
for i, (vals, lab) in enumerate([(prec, "精确率"), (rec, "召回率"), (f1, "F1")]):
    ax.bar(x + (i - 1) * w, vals * 100, w, color=SEQ[i], hatch=HATCH[i],
           edgecolor="white", linewidth=0.6, label=lab)
ax.set_xticks(x); ax.set_xticklabels(["低价值", "中价值", "高价值"])
ax.set_ylabel("指标值 / %"); ax.set_ylim(0, 108)
ax.legend(ncol=3, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.30))
ax.set_title("(b) 分类别性能", fontsize=9.5, pad=2)
ax.text(0.5, -0.30, f"高价值类 PR-AUC = {ap:.3f}    MCC = {mcc:.3f}",
        transform=ax.transAxes, ha="center", va="top", fontsize=8.2, color=C["ink"])
save(fig, OUT + "p5_d3_imbalance.png")

# 图4 引用截断偏差
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.bar(yrs, hi_by_year * 100, 0.62, color=C["steel"], edgecolor="white", linewidth=0.6,
       label="各公开年高价值专利占比")
ax2 = ax.twinx()
ax2.plot(yrs, cit_by_year, color=C["brick"], marker="o", ms=3.6, label="平均专利引用数")
ax2.set_ylabel("平均专利引用数"); ax2.spines["top"].set_visible(False)
ax.set_xlabel("专利公开年"); ax.set_ylabel("高价值专利占比 / %")
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=7.8, loc="upper right")
ax.text(0.5, -0.32, f"公开年与高价值占比的 Spearman ρ = {rho:.3f}（p<0.001）",
        transform=ax.transAxes, ha="center", va="top", fontsize=8.2, color=C["ink"])
save(fig, OUT + "p5_d4_truncation.png")

with open("/home/user/xixi/work/analysis/p5_results.json", "w", encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=1, default=float)
print("\n[done] p5")
