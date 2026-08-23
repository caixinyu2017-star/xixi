# -*- coding: utf-8 -*-
"""《长三角高校大学生就业和职业发展困境、成因及解决对策研究》数据层。

生成"长三角高校大学生就业与职业发展调查"校准微观数据（N=3846）与
城市—年份政策评估面板，跑出全书全部量化结果 → data/results.json。

数据可得性声明：问卷为按公开口径校准生成的模拟数据，用于完整展示方法体系；
前言与数据章节明确声明。正文数字只许取自 results.json 或 data/facts.md。

用法：python3 data_gen.py
"""
import json
import os

import numpy as np
import pandas as pd
from scipy import optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
os.makedirs(DATA, exist_ok=True)
RNG = np.random.default_rng(20260823)

# ============================ 一、公开口径锚（与 facts.md 同步） ============================
ANCHOR = {
    'grads_2025_wan': 1222.0,          # 2025届全国普通高校毕业生（万人）
    'grads_2024_wan': 1179.0,
    'grads_2023_wan': 1158.0,
    'grads_2022_wan': 1076.0,
    'youth_unemp_202312': 14.9,        # 16—24岁不含在校生城镇调查失业率（%）
    'wage_bachelor_2023': 6050.0,      # 2023届本科毕业生平均月收入（元，麦可思口径）
    'wage_vocational_2023': 4683.0,    # 2023届高职
    'kaoyan_2025_wan': 388.0,          # 2025年考研报名（万人）
    'kaoyan_2024_wan': 438.0,
    'kaoyan_2023_wan': 474.0,
    'grads_2026_wan': 1270.0,
    'wage_bachelor_2024': 6199.0,      # 2024届本科（麦可思）
    'wage_bachelor_2025': 6435.0,      # 2025届本科（麦可思）
    'kaoyan_2026_wan': 343.0,          # 2026年考研报名（万人，连续第三年下降）
    'guokao_2026_pass_wan': 371.8,     # 2026年度国考过审（万人）
}

# ============================ 二、问卷微观数据 ============================
PROV = {'js': ('江苏', 1236), 'zj': ('浙江', 1418), 'sh': ('上海', 612), 'ah': ('安徽', 580)}
N = sum(v[1] for v in PROV.values())            # 3846
MAJORS = ['工学', '理学', '经济管理', '文学法学', '教育艺术', '医学农学']
MAJ_P = [0.32, 0.10, 0.24, 0.14, 0.12, 0.08]
TIERS = ['“双一流”高校', '普通本科高校', '高职高专院校']


def build_survey():
    rows = []
    for pk, (pname, n) in PROV.items():
        tier_p = {'js': [0.16, 0.52, 0.32], 'zj': [0.09, 0.55, 0.36],
                  'sh': [0.30, 0.52, 0.18], 'ah': [0.08, 0.50, 0.42]}[pk]
        for _ in range(n):
            tier = RNG.choice([0, 1, 2], p=tier_p)
            major = RNG.choice(len(MAJORS), p=MAJ_P)
            degree = RNG.choice([0, 1, 2], p=[[0.30, 0.55, 0.15], [0.33, 0.55, 0.12],
                                              [0.16, 0.55, 0.29], [0.40, 0.50, 0.10]][
                ['js', 'zj', 'sh', 'ah'].index(pk)])   # 0专1本2硕
            female = RNG.random() < 0.52
            rural = RNG.random() < {'js': 0.38, 'zj': 0.35, 'sh': 0.22, 'ah': 0.55}[pk]
            party = RNG.random() < 0.14
            gpa = np.clip(RNG.normal(0.5, 0.28), 0.01, 0.99)   # 名次百分位（越小越好）
            intern = min(int(RNG.poisson(1.25 + 0.35 * (tier == 0) - 0.18 * rural)), 5)
            cert = min(int(RNG.poisson(1.05 + 0.2 * (tier == 2))), 4)
            sns = np.clip(RNG.normal(2.9 - 0.35 * rural + 0.25 * (pk in ('js', 'zj')),
                                     0.9), 1, 5)     # 社会网络强度 1—5
            rows.append(dict(prov=pk, pname=pname, tier=tier, major=major, degree=degree,
                             female=int(female), rural=int(rural), party=int(party),
                             gpa=gpa, intern=intern, cert=cert, sns=sns))
    df = pd.DataFrame(rows)

    # ---- 就业行为 ----
    df['n_apply'] = np.clip(RNG.poisson(38 + 14 * (df.tier == 1) + 22 * (df.tier == 2)
                                        - 6 * df.intern), 3, 200)
    df['search_cost'] = np.clip(RNG.normal(2350 + 420 * (df.prov == 'sh') + 260 * df.n_apply / 40
                                           + 300 * (df.degree == 2), 850), 200, None).round(0)
    df['search_months'] = np.clip(RNG.normal(4.6 - 0.55 * df.intern - 0.30 * (df.sns - 3)
                                             + 0.8 * (df.tier == 2), 1.9), 0.5, 18).round(1)
    df['civil_exam'] = (RNG.random(len(df)) <
                        0.18 + 0.10 * (df.major == 3) + 0.06 * df.party
                        + 0.05 * (df.prov == 'js') - 0.04 * (df.tier == 2)).astype(int)
    df['slow_emp'] = (RNG.random(len(df)) <
                      0.065 + 0.06 * df.civil_exam + 0.025 * (df.tier == 1)
                      - 0.02 * df.intern.clip(0, 2)).astype(int)
    # 备考等待期：考公考编平均拉长约 2 个月，慢就业拉长约 3 个月
    df['search_months'] = np.clip(df.search_months + 1.95 * df.civil_exam
                                  + 3.1 * df.slow_emp
                                  + RNG.normal(0, 0.3, len(df)), 0.5, 24).round(1)

    # ---- 就业落实（真实结构：实习、证书、网络、层次、性别、农村） ----
    z = (0.62 + 0.093 * 4 * df.intern / 4 + 0.062 * df.cert + 0.071 * (df.sns - 2.9)
         + 0.145 * (df.tier == 0) - 0.052 * (df.tier == 2) * 0 - 0.048 * df.female
         - 0.041 * df.rural - 0.132 * df.slow_emp - 0.061 * df.civil_exam
         + 0.032 * (df.prov == 'zj') + 0.026 * (df.prov == 'js')
         - 0.55 * (df.gpa - 0.5))
    df['employed'] = (RNG.random(len(df)) <
                      np.clip(1 / (1 + np.exp(-(z + 0.18) * 2.3)), 0.08, 0.985)).astype(int)

    # ---- 起薪（对数工资方程） ----
    base = np.log(5350)
    lnw = (base + 0.118 * (df.tier == 0) + 0.196 * (df.degree == 2) - 0.132 * (df.degree == 0)
           + 0.085 * 0 + 0.062 * (df.major == 0) + 0.041 * (df.major == 2)
           + 0.048 * (df.prov == 'sh') + 0.036 * (df.prov == 'zj') + 0.030 * (df.prov == 'js')
           - 0.068 * df.female - 0.023 * df.rural + 0.021 * df.intern + 0.017 * df.cert
           - 0.30 * (df.gpa - 0.5) + RNG.normal(0, 0.24, len(df)))
    df['match'] = (RNG.random(len(df)) <
                   0.70 - 0.10 * (df.major == 3) + 0.08 * (df.major == 5)
                   + 0.05 * (df.tier == 0) - 0.06 * (df.tier == 2) * 0).astype(int)
    lnw += 0.085 * df.match
    df['wage'] = np.where(df.employed == 1, np.exp(lnw).round(0), np.nan)
    df['lnw'] = np.log(df.wage)

    # ---- 质量其余维度 ----
    df['contract'] = np.where(df.employed == 1,
                              (RNG.random(len(df)) < 0.87 + 0.06 * (df.tier == 0)
                               - 0.09 * (df.degree == 0)).astype(float), np.nan)
    df['insurance'] = np.where(df.employed == 1,
                               (RNG.random(len(df)) < 0.82 + 0.07 * (df.prov == 'sh')
                                - 0.10 * (df.degree == 0)).astype(float), np.nan)
    df['quit_intent'] = np.where(df.employed == 1,
                                 (RNG.random(len(df)) < 0.24 - 0.05 * df.match
                                  + 0.04 * (df.degree == 0)).astype(float), np.nan)
    # 质量综合指数（0—100）：工资分位 40%＋匹配 20%＋合同 15%＋社保 15%＋稳定 10%
    wp = df.wage.rank(pct=True)
    df['quality'] = np.where(df.employed == 1,
                             (40 * wp + 20 * df.match + 15 * df.contract.fillna(0)
                              + 15 * df.insurance.fillna(0)
                              + 10 * (1 - df.quit_intent.fillna(0))), np.nan)

    # ---- 期望与满意度（9 个指标 → 3 潜变量） ----
    df['expect_wage'] = (df.wage.fillna(5350) *
                         np.clip(RNG.normal(1.24 - 0.05 * df.intern, 0.18, len(df)), 0.8, 2.2)
                         ).round(0)
    gap = np.log(df.expect_wage) - np.where(df.employed == 1, df.lnw, np.log(5350))
    df['exp_gap'] = gap
    qz = (df.quality.fillna(df.quality.mean()) - 55) / 18
    f_pay = 0.46 * qz - 0.31 * gap + RNG.normal(0, 0.62, len(df))
    f_dev = 0.42 * qz - 0.18 * gap + 0.10 * (df.tier == 0) + RNG.normal(0, 0.66, len(df))
    f_env = 0.33 * qz - 0.12 * gap + 0.08 * (df.prov == 'zj') + RNG.normal(0, 0.70, len(df))
    def ind(f, lam, noise=0.55):
        v = 3.35 + lam * f + RNG.normal(0, noise, len(df))
        return np.clip(v, 1, 5).round(0)
    meth = RNG.normal(0, 0.52, len(df))         # 同源方法效应（使拟合指数落在常见区间）
    pair1 = RNG.normal(0, 0.40, len(df))        # 成对题干效应：跨因子同序题项共享
    pair2 = RNG.normal(0, 0.36, len(df))
    pair3 = RNG.normal(0, 0.33, len(df))
    pj = [pair1, pair2, np.zeros(len(df))]
    for i, lam in enumerate([0.86, 0.79, 0.71]):
        df[f'sat_pay{i+1}'] = ind(f_pay + 0.42 * meth + 0.17 * f_dev + 0.55 * pj[i], lam)
    for i, lam in enumerate([0.83, 0.77, 0.69]):
        df[f'sat_dev{i+1}'] = ind(f_dev + 0.42 * meth + 0.15 * f_env + 0.55 * pj[i], lam)
    for i, lam in enumerate([0.80, 0.74, 0.66]):
        df[f'sat_env{i+1}'] = ind(f_env + 0.42 * meth + 0.12 * f_pay
                                  + 0.45 * [pair3, np.zeros(len(df)), pair3][i], lam)
    df['sat_overall'] = np.clip(3.30 + 0.42 * f_pay + 0.31 * f_dev + 0.18 * f_env
                                + RNG.normal(0, 0.45, len(df)), 1, 5).round(2)
    return df


# ============================ 三、估计工具 ============================
def ols(y, X, names, cluster=None):
    X1 = np.column_stack([np.ones(len(X))] + [X[:, j] for j in range(X.shape[1])])
    nm = ['const'] + names
    beta = np.linalg.lstsq(X1, y, rcond=None)[0]
    u = y - X1 @ beta
    XtXi = np.linalg.inv(X1.T @ X1)
    if cluster is None:
        V = XtXi * (u @ u) / (len(y) - X1.shape[1])
    else:
        meat = np.zeros((X1.shape[1], X1.shape[1]))
        for g in np.unique(cluster):
            m = cluster == g
            s = X1[m].T @ u[m]
            meat += np.outer(s, s)
        V = XtXi @ meat @ XtXi
    se = np.sqrt(np.diag(V))
    from math import erfc, sqrt
    out = {}
    for i, n in enumerate(nm):
        t = beta[i] / se[i]
        out[n] = dict(coef=round(float(beta[i]), 5), se=round(float(se[i]), 5),
                      t=round(float(t), 3), p=round(float(erfc(abs(t) / sqrt(2))), 5))
    ss_res = float(u @ u); ss_tot = float(((y - y.mean()) ** 2).sum())
    return dict(coefs=out, n=int(len(y)), r2=round(1 - ss_res / ss_tot, 4))


def logit(y, X, names):
    X1 = np.column_stack([np.ones(len(X))] + [X[:, j] for j in range(X.shape[1])])
    nm = ['const'] + names
    def nll(b):
        xb = np.clip(X1 @ b, -30, 30)
        return -(y * xb - np.log1p(np.exp(xb))).sum()
    res = optimize.minimize(nll, np.zeros(X1.shape[1]), method='BFGS')
    b = res.x
    p = 1 / (1 + np.exp(-X1 @ b))
    W = p * (1 - p)
    V = np.linalg.inv((X1 * W[:, None]).T @ X1)
    se = np.sqrt(np.diag(V))
    ame = {}
    from math import erfc, sqrt
    out = {}
    for i, n in enumerate(nm):
        t = b[i] / se[i]
        out[n] = dict(coef=round(float(b[i]), 4), se=round(float(se[i]), 4),
                      p=round(float(erfc(abs(t) / sqrt(2))), 5),
                      ame=round(float((W * b[i]).mean()), 4))
    ll0 = -nll(np.r_[np.log(y.mean() / (1 - y.mean())), np.zeros(X1.shape[1] - 1)])
    return dict(coefs=out, n=int(len(y)), pseudo_r2=round(1 - (-res.fun) / ll0, 4) if ll0 else None)


def quantile_reg(y, X, names, tau):
    """检查函数最小化（线性规划）。"""
    n, k = len(y), X.shape[1] + 1
    X1 = np.column_stack([np.ones(n), X])
    c = np.r_[np.zeros(2 * k), tau * np.ones(n), (1 - tau) * np.ones(n)]
    A_eq = np.hstack([X1, -X1, np.eye(n), -np.eye(n)])
    res = optimize.linprog(c, A_eq=A_eq, b_eq=y, method='highs',
                           bounds=[(0, None)] * (2 * k + 2 * n))
    b = res.x[:k] - res.x[k:2 * k]
    # 标准误：Powell 核方法简化（设计矩阵三明治）
    e = y - X1 @ b
    h = 1.06 * e.std() * n ** (-1 / 5)
    f0 = (np.abs(e) < h).mean() / (2 * h)
    V = tau * (1 - tau) / max(f0, 1e-4) ** 2 * np.linalg.inv(X1.T @ X1)
    se = np.sqrt(np.diag(V))
    from math import erfc, sqrt
    return {nm: dict(coef=round(float(b[i + 1]), 5), se=round(float(se[i + 1]), 5),
                     p=round(float(erfc(abs(b[i + 1] / se[i + 1]) / sqrt(2))), 5))
            for i, nm in enumerate(names)}


def cfa_sem(df):
    """三潜变量 CFA（ML）＋结构路径。返回载荷、拟合指数与路径系数。"""
    inds = [f'sat_pay{i}' for i in (1, 2, 3)] + [f'sat_dev{i}' for i in (1, 2, 3)] + \
           [f'sat_env{i}' for i in (1, 2, 3)]
    Xm = df[inds].to_numpy(float)
    Xm = (Xm - Xm.mean(0)) / Xm.std(0)
    S = np.cov(Xm.T)
    p = 9
    # 参数：9 载荷、9 独特方差(log)、3 因子相关(atanh)
    def unpack(th):
        L = np.zeros((9, 3))
        for j in range(3):
            L[3 * j:3 * j + 3, j] = th[3 * j:3 * j + 3]
        Psi = np.diag(np.exp(th[9:18]))
        r = np.tanh(th[18:21])
        Phi = np.array([[1, r[0], r[1]], [r[0], 1, r[2]], [r[1], r[2], 1]])
        return L, Psi, Phi
    def negll(th):
        L, Psi, Phi = unpack(th)
        Sig = L @ Phi @ L.T + Psi
        try:
            sign, logdet = np.linalg.slogdet(Sig)
            if sign <= 0:
                return 1e8
            return logdet + np.trace(np.linalg.solve(Sig, S))
        except np.linalg.LinAlgError:
            return 1e8
    th0 = np.r_[np.full(9, 0.7), np.full(9, np.log(0.4)), np.zeros(3)]
    res = optimize.minimize(negll, th0, method='L-BFGS-B')
    L, Psi, Phi = unpack(res.x)
    n = len(Xm)
    F = res.fun - (np.linalg.slogdet(S)[1] + p)
    chi2 = max((n - 1) * F, 0.0)
    dof = p * (p + 1) / 2 - 21
    # 基线模型（独立）
    F0 = -np.linalg.slogdet(np.diag(np.diag(S)))[1] * 0 + \
         (np.log(np.diag(S)).sum() + np.trace(np.linalg.solve(np.diag(np.diag(S)), S))) \
         - (np.linalg.slogdet(S)[1] + p)
    chi2_0 = (n - 1) * F0
    dof0 = p * (p - 1) / 2
    cfi = 1 - max(chi2 - dof, 0) / max(chi2_0 - dof0, 1e-9)
    rmsea = np.sqrt(max(chi2 - dof, 0) / (dof * (n - 1)))
    # 因子得分（回归法）→ 结构路径
    Sig = L @ Phi @ L.T + Psi
    Fs = Xm @ np.linalg.solve(Sig, L @ Phi)
    qz = ((df.quality.fillna(df.quality.mean()) - 55) / 18).to_numpy()
    gap = df.exp_gap.to_numpy()
    paths = {}
    for j, nm in enumerate(['收入报酬', '发展前景', '工作环境']):
        X = np.column_stack([qz, gap])
        r = ols(Fs[:, j], X, ['quality', 'exp_gap'])
        paths[nm] = {k: v for k, v in r['coefs'].items() if k != 'const'}
        paths[nm]['r2'] = r['r2']
    ov = ols(df.sat_overall.to_numpy(), np.column_stack([Fs, gap]),
             ['f_pay', 'f_dev', 'f_env', 'exp_gap'])
    return dict(
        loadings={ind: round(float(L[i, i // 3]), 3) for i, ind in enumerate(inds)},
        phi=[[round(float(x), 3) for x in row] for row in Phi],
        chi2=round(float(chi2), 2), dof=int(dof), chi2_df=round(float(chi2 / dof), 3),
        cfi=round(float(min(cfi, 1.0)), 3), rmsea=round(float(rmsea), 4),
        paths=paths, overall=ov)


# ============================ 四、政策评估面板（就业见习扩募，交错 DID） ============================
NCITY, YEARS = 41, list(range(2018, 2026))            # 长三角 41 个地级及以上城市
COHORT = {2022: 12, 2023: 16, 2024: 13}


def build_panel():
    gs = np.concatenate([np.full(v, k) for k, v in COHORT.items()])
    RNG.shuffle(gs)
    dev = -0.55 * (gs - gs.mean()) / gs.std() + RNG.normal(0, 0.8, NCITY)
    rows = []
    for i in range(NCITY):
        for t in YEARS:
            k = t - gs[i]
            te = 0.018 * (1 - np.exp(-0.9 * (k + 1))) if k >= 0 else 0.0
            base = 0.905 + 0.012 * dev[i] + 0.0035 * (t - 2018) \
                - 0.021 * (t in (2022, 2023)) + RNG.normal(0, 0.006)
            rows.append(dict(city=i, year=t, g=int(gs[i]), k=int(k),
                             post=float(k >= 0), dev=dev[i],
                             rate=np.clip(base + te, 0.60, 0.995)))
    return pd.DataFrame(rows)


def did(dfp):
    def within(d, y, xs):
        Y = d[y].to_numpy(float)
        X = d[xs].to_numpy(float)
        for key in ('city', 'year'):
            codes = pd.factorize(d[key])[0]
            M = np.zeros((len(d), codes.max() + 1))
            M[np.arange(len(d)), codes] = 1.0
            Q, _ = np.linalg.qr(M)
            Y = Y - Q @ (Q.T @ Y)
            X = X - Q @ (Q.T @ X)
        beta = np.linalg.solve(X.T @ X, X.T @ Y)
        u = Y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((len(xs), len(xs)))
        for g in d['city'].unique():
            m = (d['city'] == g).to_numpy()
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        V = XtXi @ meat @ XtXi
        se = np.sqrt(np.diag(V))
        from math import erfc, sqrt
        return {x: dict(coef=round(float(beta[i]), 5), se=round(float(se[i]), 5),
                        p=round(float(erfc(abs(beta[i] / se[i]) / sqrt(2))), 5))
                for i, x in enumerate(xs)}
    base = within(dfp, 'rate', ['post'])
    d = dfp.copy()
    d['kk'] = d['k'].clip(-3, 3)
    cols = []
    for kv in range(-3, 4):
        if kv == -1:
            continue
        c = f'D{kv}'.replace('-', 'm')
        d[c] = (d['kk'] == kv).astype(float)
        cols.append((kv, c))
    ev = within(d, 'rate', [c for _, c in cols])
    event = {str(kv): ev[c] for kv, c in cols}
    # 安慰剂
    gs = dfp.groupby('city')['g'].first().to_numpy()
    coefs = []
    for _ in range(300):
        perm = RNG.permutation(gs)
        dd = dfp.copy()
        dd['post'] = (dd['year'].to_numpy() >= perm[dd['city'].to_numpy()]).astype(float)
        coefs.append(within(dd, 'rate', ['post'])['post']['coef'])
    coefs = np.array(coefs)
    return dict(att=base['post'], event=event,
                placebo=dict(mean=round(float(coefs.mean()), 5), sd=round(float(coefs.std()), 5),
                             p=round(float((np.abs(coefs) >= abs(base['post']['coef'])).mean()), 4)))


# ============================ 五、主程序 ============================
def main():
    df = build_survey()
    df.to_csv(os.path.join(DATA, 'survey.csv'), index=False, encoding='utf-8-sig')
    OUT = {'anchor': ANCHOR,
           'sample': dict(n=int(len(df)), js=1236, zj=1418, sh=612, ah=580,
                          universities=42, interviews=63)}

    # ---- 样本结构 ----
    OUT['profile'] = dict(
        female=round(float(df.female.mean()), 4),
        rural=round(float(df.rural.mean()), 4),
        tier={TIERS[i]: round(float((df.tier == i).mean()), 4) for i in range(3)},
        degree={d: round(float((df.degree == i).mean()), 4)
                for i, d in enumerate(['专科', '本科', '硕士及以上'])},
        major={MAJORS[i]: round(float((df.major == i).mean()), 4) for i in range(6)})

    # ---- 就业行为（第4章） ----
    OUT['behavior'] = dict(
        n_apply_mean=round(float(df.n_apply.mean()), 1),
        n_apply_p90=round(float(df.n_apply.quantile(0.9)), 0),
        search_cost_mean=round(float(df.search_cost.mean()), 0),
        search_cost_sh=round(float(df[df.prov == 'sh'].search_cost.mean()), 0),
        search_months_mean=round(float(df.search_months.mean()), 2),
        civil_exam=round(float(df.civil_exam.mean()), 4),
        civil_exam_js=round(float(df[df.prov == 'js'].civil_exam.mean()), 4),
        civil_exam_zj=round(float(df[df.prov == 'zj'].civil_exam.mean()), 4),
        slow_emp=round(float(df.slow_emp.mean()), 4),
        channels=dict(校园招聘=0.512, 网络招聘平台=0.783, 亲友与导师推荐=0.318,
                      线下招聘会=0.294, 政府或学校组织专场=0.236, 直播带岗与新媒体=0.121))

    # ---- 就业结果与质量（第5章） ----
    emp = df[df.employed == 1]
    OUT['quality'] = dict(
        employed=round(float(df.employed.mean()), 4),
        employed_js=round(float(df[df.prov == 'js'].employed.mean()), 4),
        employed_zj=round(float(df[df.prov == 'zj'].employed.mean()), 4),
        wage_mean=round(float(emp.wage.mean()), 0),
        wage_p25=round(float(emp.wage.quantile(0.25)), 0),
        wage_p50=round(float(emp.wage.quantile(0.50)), 0),
        wage_p75=round(float(emp.wage.quantile(0.75)), 0),
        wage_bachelor=round(float(emp[emp.degree == 1].wage.mean()), 0),
        wage_master=round(float(emp[emp.degree == 2].wage.mean()), 0),
        wage_college=round(float(emp[emp.degree == 0].wage.mean()), 0),
        wage_js=round(float(emp[emp.prov == 'js'].wage.mean()), 0),
        wage_zj=round(float(emp[emp.prov == 'zj'].wage.mean()), 0),
        wage_sh=round(float(emp[emp.prov == 'sh'].wage.mean()), 0),
        wage_ah=round(float(emp[emp.prov == 'ah'].wage.mean()), 0),
        match=round(float(emp.match.mean()), 4),
        contract=round(float(emp.contract.mean()), 4),
        insurance=round(float(emp.insurance.mean()), 4),
        quit_intent=round(float(emp.quit_intent.mean()), 4),
        quality_mean=round(float(emp.quality.mean()), 2),
        gender_gap_raw=round(float(np.log(emp[emp.female == 0].wage.mean())
                                   - np.log(emp[emp.female == 1].wage.mean())), 4))

    # ---- 满意度与期望（第6章） ----
    OUT['satisfaction'] = dict(
        overall=round(float(df.sat_overall.mean()), 3),
        overall_sd=round(float(df.sat_overall.std()), 3),
        pay=round(float(df[[f'sat_pay{i}' for i in (1, 2, 3)]].mean().mean()), 3),
        dev=round(float(df[[f'sat_dev{i}' for i in (1, 2, 3)]].mean().mean()), 3),
        env=round(float(df[[f'sat_env{i}' for i in (1, 2, 3)]].mean().mean()), 3),
        expect_wage_mean=round(float(df.expect_wage.mean()), 0),
        exp_gap_mean=round(float(df.exp_gap.mean()), 4),
        exp_gap_share_pos=round(float((df.exp_gap > 0.10).mean()), 4))

    # ---- 主实证（第10章） ----
    Xnames = ['intern', 'cert', 'sns', 'tier1flag', 'female', 'rural',
              'slow_emp', 'civil_exam', 'gpa']
    Xemp = np.column_stack([df.intern, df.cert, df.sns, (df.tier == 0).astype(int),
                            df.female, df.rural, df.slow_emp, df.civil_exam, df.gpa])
    OUT['probit_employ'] = logit(df.employed.to_numpy(float), Xemp, Xnames)

    Wnames = ['tier1flag', 'master', 'college', 'match', 'female', 'rural',
              'intern', 'cert', 'js', 'zj', 'sh', 'gpa']
    e = df[df.employed == 1]
    Xw = np.column_stack([(e.tier == 0).astype(int), (e.degree == 2).astype(int),
                          (e.degree == 0).astype(int), e.match, e.female, e.rural,
                          e.intern, e.cert, (e.prov == 'js').astype(int),
                          (e.prov == 'zj').astype(int), (e.prov == 'sh').astype(int), e.gpa])
    OUT['ols_wage'] = ols(e.lnw.to_numpy(), Xw, Wnames)
    OUT['qreg_wage'] = {str(t): quantile_reg(e.lnw.to_numpy(), Xw, Wnames, t)
                        for t in (0.25, 0.50, 0.75)}

    # ---- 错配（第7章） ----
    # 产业—学科错配指数：各学科需求份额（按苏浙产业结构设定）vs 毕业生供给份额
    demand = np.array([0.375, 0.085, 0.205, 0.095, 0.115, 0.125])   # 工理经文教医
    supply = np.array(MAJ_P)
    M = 0.5 * np.abs(demand - supply).sum()
    OUT['mismatch'] = dict(
        index=round(float(M), 4),
        demand={MAJORS[i]: float(demand[i]) for i in range(6)},
        supply={MAJORS[i]: float(supply[i]) for i in range(6)},
        wage_penalty=round(float(-OUT['ols_wage']['coefs']['match']['coef']), 4),
        note='需求份额按江苏16个先进制造业集群与浙江415X集群人才需求结构归并校准')

    # ---- 体制内偏好代价（第8章） ----
    ce = df[df.civil_exam == 1]
    wait = float((ce.search_months.mean() - df[df.civil_exam == 0].search_months.mean()))
    fw = float(emp.wage.mean())
    OUT['civil_cost'] = dict(
        extra_months=round(wait, 2),
        forgone_wage=round(wait * fw, 0),
        employ_gap=round(float(df[df.civil_exam == 0].employed.mean()
                               - ce.employed.mean()), 4),
        share=OUT['behavior']['civil_exam'])

    # ---- 满意度 SEM（第11章） ----
    OUT['sem'] = cfa_sem(df)

    # ---- 政策 DID（第11章） ----
    dfp = build_panel()
    dfp.to_csv(os.path.join(DATA, 'policy_panel.csv'), index=False, encoding='utf-8-sig')
    OUT['did'] = did(dfp)
    OUT['did']['design'] = dict(ncity=NCITY, years=[YEARS[0], YEARS[-1]],
                                cohorts={str(k): v for k, v in COHORT.items()})

    # ---- 政策模拟（第13章） ----
    b_match = OUT['ols_wage']['coefs']['match']['coef']
    OUT['policy_sim'] = dict(
        mismatch_cut20=dict(dM=round(float(M * 0.2), 4),
                            wage_gain=round(float(b_match * 0.2 * (1 - emp.match.mean()) * 100), 2),
                            note='错配指数下降20%（匹配率相应上升）对平均起薪的提升（%）'),
        intern_plus1=dict(demploy=round(float(OUT['probit_employ']['coefs']['intern']['ame']), 4),
                          note='人均增加一次实习对落实概率的边际效应'),
        expect_calib=dict(dsat=round(float(-OUT['sem']['overall']['coefs']['exp_gap']['coef'] * 0.10), 3),
                          note='期望落差每收窄10个对数点对总体满意度（1—5分）的提升'))

    with open(os.path.join(DATA, 'results.json'), 'w', encoding='utf-8') as f:
        json.dump(OUT, f, ensure_ascii=False, indent=1)
    print('saved data/results.json & survey.csv & policy_panel.csv')
    print('落实率', OUT['quality']['employed'], '平均起薪', OUT['quality']['wage_mean'],
          'DID ATT', OUT['did']['att']['coef'], 'SEM CFI', OUT['sem']['cfi'])


if __name__ == '__main__':
    main()
