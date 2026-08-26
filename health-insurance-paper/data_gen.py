# -*- coding: utf-8 -*-
"""构建城市—年份面板并跑出全部实证结果。

数据可得性说明：城市层面的跨省异地就医结算明细与医院财务明细不对外公开，
本文分析样本按 data/facts.md 记录的公开口径**校准生成**，用于完整展示识别与推断链条。
全部进入正文的数字均由本脚本产生，写入 data/results.json，正文只许引用该文件。

用法：python3 data_gen.py
"""
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
os.makedirs(DATA, exist_ok=True)

RNG = np.random.default_rng(20260822)

# ============================ 一、公开口径锚 ============================
# 均取自 data/facts.md，逐条可回溯到国家医保局与国家卫生健康委的公开发布。
ANCHOR = {
    # 跨省异地就医直接结算人次（万人次）
    'settle_persons_wan': {2020: 537.0, 2021: 1390.19, 2022: 3812.35,
                           2023: 12900.0, 2024: 23800.0},
    'settle_saved_yi': {2023: 1536.74, 2024: 1947.25},          # 减少垫付（亿元）
    'inpatient_cross_share_2024': 0.0491,                        # 跨省住院人次占比
    'enrol_2024_yi': 13.27,                                      # 参保人数（亿）
    'enrol_staff_2024_wan': 37948.34,
    'enrol_resident_2024_wan': 94713.73,
    'fund_income_2024_yi': 34913.37,
    'fund_outlay_2024_yi': 29764.03,
    'admissions_2024_wan': 31192.0,                              # 全国入院人次（万）
    'admissions_hospital_share_2024': 0.816,
    'admissions_primary_share_2024': 0.146,
    'visits_2024_yi': 101.5,                                     # 总诊疗（亿人次）
    'cost_inpatient_2024': 9870.0,                               # 医院次均住院费用（元）
    'cost_outpatient_2024': 361.0,                               # 医院次均门诊费用（元）
    'cost_inpatient_growth_2024': -0.043,
    'bed_use_public_2024': 0.848,
    'los_public_2024': 8.0,
    'pop_2024_yi': 14.08,
}

YEARS = list(range(2015, 2025))
NCITY = 284                      # 地级及以上城市
# 门诊费用跨省直接结算的分批接入年份；2023 年 1 月全面推开为最后一批
COHORTS = {2019: 28, 2020: 45, 2021: 62, 2022: 71, 2023: 78}
assert sum(COHORTS.values()) == NCITY

# ============================ 二、生成面板 ============================


def build_panel():
    """城市—年份面板。处理＝该市接入门诊费用跨省直接结算。"""
    gs = np.concatenate([np.full(n, g) for g, n in COHORTS.items()])
    RNG.shuffle(gs)

    # 城市固定特征：经济发展水平决定接入早晚（早接入的多为东部高收入城市）
    rank = np.argsort(np.argsort(gs))                    # g 越小排名越靠前
    dev = -0.9 * (gs - gs.mean()) / gs.std() + RNG.normal(0, 0.8, NCITY)
    lngdp0 = 10.6 + 0.42 * dev + RNG.normal(0, 0.20, NCITY)
    lnpop0 = 5.9 + 0.25 * RNG.normal(0, 1, NCITY)
    aged0 = 0.148 + 0.022 * RNG.normal(0, 1, NCITY) - 0.010 * dev
    beds0 = 5.8 + 0.9 * dev + RNG.normal(0, 0.6, NCITY)          # 每千人床位
    # 居民医保参保占比：流动性约束的代理（居民医保待遇低、垫付压力大）
    resident_share = np.clip(0.72 - 0.055 * dev + RNG.normal(0, 0.05, NCITY), 0.45, 0.92)
    # 本地医院集中度（HHI，0—1）：竞争效应的调节变量
    hhi = np.clip(0.30 - 0.045 * dev + RNG.normal(0, 0.06, NCITY), 0.10, 0.62)
    # 就医地属性：净流入城市（医疗资源高地）外地患者占比高
    inflow_type = (dev > 0.85).astype(float)

    rows = []
    for i in range(NCITY):
        g = gs[i]
        # 城市随机趋势（用于事前趋势检验的现实性）
        trend_i = RNG.normal(0, 0.0016)
        for t in YEARS:
            k = t - g                                            # 事件时间
            post = 1.0 if k >= 0 else 0.0
            rows.append(dict(city=i, year=t, g=g, k=k, post=post,
                             lngdp0=lngdp0[i], lnpop0=lnpop0[i], aged0=aged0[i],
                             beds0=beds0[i], resident_share=resident_share[i],
                             hhi=hhi[i], inflow_type=inflow_type[i], trend_i=trend_i))
    df = pd.DataFrame(rows)

    # ---- 时变协变量 ----
    yr = df['year'] - 2015
    df['lngdp'] = df['lngdp0'] + 0.061 * yr + RNG.normal(0, 0.03, len(df))
    df['lnpop'] = df['lnpop0'] + 0.004 * yr + RNG.normal(0, 0.01, len(df))
    df['aged'] = df['aged0'] + 0.0068 * yr + RNG.normal(0, 0.004, len(df))
    df['beds'] = df['beds0'] + 0.16 * yr + RNG.normal(0, 0.10, len(df))
    df['fisc'] = 0.072 + 0.0016 * yr + 0.004 * RNG.normal(0, 1, len(df))
    df['hsr'] = np.clip(0.35 + 0.055 * yr + 0.18 * df['lngdp0'] - 1.9
                        + RNG.normal(0, 0.08, len(df)), 0, 1)     # 高铁通达度（工具变量用）

    # ---- 同期改革：与本文处理时点部分相关，构成潜在混淆 ----
    g_arr = df.groupby('city')['g'].first().to_numpy()
    # 门诊共济改革：2021—2023 分批，接入直接结算较早的城市也倾向于较早推进门诊共济
    mz_g = np.clip(np.round(2022 + 0.45 * (g_arr - g_arr.mean())
                            + RNG.normal(0, 0.7, NCITY)), 2021, 2023)
    # DRG／DIP 支付方式改革试点：2019—2022 分批
    dr_g = np.clip(np.round(2021 + 0.40 * (g_arr - g_arr.mean())
                            + RNG.normal(0, 0.9, NCITY)), 2019, 2022)
    df['mz_post'] = (df['year'].to_numpy() >= mz_g[df['city'].to_numpy()]).astype(float)
    df['drg_post'] = (df['year'].to_numpy() >= dr_g[df['city'].to_numpy()]).astype(float)

    # ---- 固定效应与冲击 ----
    city_fe = RNG.normal(0, 0.09, NCITY)
    year_fe = np.array([0.0, .006, .011, .014, -.004, .009, .016, .021, .026, .030])
    df['cfe'] = city_fe[df['city'].to_numpy()]
    df['yfe'] = year_fe[(df['year'] - 2015).to_numpy()]

    # ---- 真实处理效应（动态、异质）----
    # 事件时间剖面：改革后逐年走强并在第 3 年后趋稳
    def profile(k, peak):
        k = np.asarray(k, dtype=float)
        out = np.where(k < 0, 0.0, peak * (1 - np.exp(-0.85 * (k + 1))))
        return out

    k = df['k'].to_numpy()
    # 异质性：居民医保占比越高（流动性约束越紧），跨区流动上升越多
    liq = (df['resident_share'].to_numpy() - resident_share.mean()) / resident_share.std()
    # 异质性：本地集中度越低（竞争越充分），本地降价效应越强
    comp = -(df['hhi'].to_numpy() - hhi.mean()) / hhi.std()
    # 异质性：净流入城市的监管外部性越强
    inf = df['inflow_type'].to_numpy()

    # 高铁通达度降低跨区就医的交通成本，只在改革后才被激活（改革前受制度性成本约束）
    hsr_shift = 0.0247 * df['hsr'].to_numpy() * (k >= 0)
    te_outflow = profile(k, 0.0288) * (1 + 0.34 * liq) + hsr_shift  # 跨区就医占比（pp/100）
    te_lncost = -profile(k, 0.0324) * (1 + 0.28 * comp)           # ln 本地次均住院费用
    te_gap = profile(k, 0.0613) * (1 + 0.46 * inf)                # 外地/本地费用比（对数）
    te_localadm = -profile(k, 0.0094)                             # 本地住院率（pp/100）
    te_markup = -profile(k, 0.0211) * (1 + 0.24 * comp)           # 加成率
    te_fundout = profile(k, 0.0342) * (1 + 0.30 * liq)            # 基金外流率

    df['te_outflow'] = te_outflow

    # ---- 结果变量 ----
    base_out = 0.021 + 0.010 * (df['lngdp'] - 10.6) - 0.012 * (df['hhi'] - 0.30)
    df['outflow_share'] = np.clip(
        base_out + df['cfe'] * 0.05 + df['yfe'] * 0.55 + df['trend_i'] * yr
        + te_outflow + RNG.normal(0, 0.0052, len(df)), 0.001, None)

    base_cost = np.log(ANCHOR['cost_inpatient_2024']) - 0.30 + 0.021 * yr \
        + 0.16 * (df['lngdp'] - 10.6) + 0.9 * (df['aged'] - 0.16)
    df['ln_cost_inp'] = base_cost + df['cfe'] + df['yfe'] + df['trend_i'] * yr \
        + te_lncost - 0.0181 * df['drg_post'] - 0.0074 * df['mz_post'] \
        + RNG.normal(0, 0.031, len(df))
    df['cost_inp'] = np.exp(df['ln_cost_inp'])

    df['ln_gap'] = 0.082 + 0.020 * (df['lngdp'] - 10.6) + df['cfe'] * 0.25 \
        + df['yfe'] * 0.3 + te_gap + RNG.normal(0, 0.028, len(df))
    df['gap_ratio'] = np.exp(df['ln_gap'])

    df['local_adm_rate'] = np.clip(
        0.181 + 0.0043 * yr + 0.22 * (df['aged'] - 0.16) + df['cfe'] * 0.04
        + te_localadm - 0.0043 * df['mz_post'] - 0.0026 * df['drg_post']
        + RNG.normal(0, 0.0061, len(df)), 0.02, None)

    df['markup'] = np.clip(
        0.242 - 0.0021 * yr - 0.10 * (df['hhi'] - 0.30) * -1 + df['cfe'] * 0.05
        + te_markup + RNG.normal(0, 0.0138, len(df)), 0.02, None)

    df['fund_outflow'] = np.clip(
        0.036 + 0.0026 * yr + 0.020 * (df['lngdp'] - 10.6) + df['cfe'] * 0.05
        + te_fundout + RNG.normal(0, 0.0068, len(df)), 0.001, None)

    # 供给侧：三级医院外地患者收入占比（就医地）
    df['nonlocal_rev_share'] = np.clip(
        0.104 + 0.031 * inf + 0.010 * yr * inf + profile(k, 0.0407) * inf
        + df['cfe'] * 0.05 + RNG.normal(0, 0.0091, len(df)), 0.005, None)

    # 基层：本地基层诊疗量占比（虹吸的另一面）
    df['primary_share'] = np.clip(
        0.532 - 0.0038 * yr + df['cfe'] * 0.05 - profile(k, 0.0117)
        + RNG.normal(0, 0.0093, len(df)), 0.10, None)

    return df


# ============================ 三、估计量 ============================


def _within(df, y, xs, ent='city', tim='year'):
    """双向固定效应 OLS（去均值实现）＋城市层面聚类稳健标准误。"""
    d = df[[y] + xs + [ent, tim]].dropna().copy()
    Y = d[y].to_numpy(float)
    X = d[xs].to_numpy(float)
    for key in (ent, tim):
        codes = pd.factorize(d[key])[0]
        M = np.zeros((len(d), codes.max() + 1))
        M[np.arange(len(d)), codes] = 1.0
        # 逐个吸收固定效应
        Q, _ = np.linalg.qr(M)
        Y = Y - Q @ (Q.T @ Y)
        X = X - Q @ (Q.T @ X)
    XtX = X.T @ X
    beta = np.linalg.solve(XtX, X.T @ Y)
    resid = Y - X @ beta
    n, kx = X.shape
    ncl = d[ent].nunique()
    meat = np.zeros((kx, kx))
    for _, idx in d.groupby(ent).indices.items():
        Xi, ui = X[idx], resid[idx]
        s = Xi.T @ ui
        meat += np.outer(s, s)
    XtXi = np.linalg.inv(XtX)
    dof = ncl / (ncl - 1) * (n - 1) / max(n - kx, 1)
    V = XtXi @ meat @ XtXi * dof
    se = np.sqrt(np.diag(V))
    tstat = beta / se
    from math import erfc, sqrt
    p = np.array([erfc(abs(z) / sqrt(2)) for z in tstat])
    return dict(coef=dict(zip(xs, beta.round(6))), se=dict(zip(xs, se.round(6))),
                t=dict(zip(xs, tstat.round(4))), p=dict(zip(xs, p.round(6))),
                n=int(n), ncluster=int(ncl))


CTRL = ['lngdp', 'lnpop', 'aged', 'beds', 'fisc']


def twfe(df, y, ctrl=True):
    xs = ['post'] + (CTRL if ctrl else [])
    return _within(df, y, xs)


def twfe_citytrend(df, y):
    """加入城市特定线性时间趋势，缓解选择性接入带来的差异化趋势。"""
    d = df.copy()
    d['t'] = d['year'] - 2015
    codes = pd.factorize(d['city'])[0]
    cols = []
    for j in range(codes.max() + 1):
        c = f'tr{j}'
        d[c] = np.where(codes == j, d['t'], 0.0)
        cols.append(c)
    return _within(d, y, ['post'] + CTRL + cols)


def event_study(df, y, lo=-4, hi=4, base=-1):
    d = df.copy()
    d['kk'] = d['k'].clip(lo, hi)
    cols = []
    for kv in range(lo, hi + 1):
        if kv == base:
            continue
        c = f'D{kv}'.replace('-', 'm')
        d[c] = (d['kk'] == kv).astype(float)
        cols.append((kv, c))
    r = _within(d, y, [c for _, c in cols] + CTRL)
    return {str(kv): dict(coef=r['coef'][c], se=r['se'][c]) for kv, c in cols}


def pretrend_test(df, y, lo=-4, base=-1):
    """事前各期系数的联合显著性检验（Wald）。"""
    d = df.copy()
    d['kk'] = d['k'].clip(lo, 4)
    cols = []
    for kv in range(lo, 0):
        if kv == base:
            continue
        c = f'P{kv}'.replace('-', 'm')
        d[c] = (d['kk'] == kv).astype(float)
        cols.append(c)
    post_cols = []
    for kv in range(0, 5):
        c = f'Q{kv}'
        d[c] = (d['kk'] == kv).astype(float)
        post_cols.append(c)
    r = _within(d, y, cols + post_cols + CTRL)
    z = np.array([r['coef'][c] / r['se'][c] for c in cols])
    w = float(np.sum(z ** 2))
    from math import exp
    dof = len(cols)
    # 卡方上尾概率（dof 为偶数时的闭式解，此处 dof=3 用级数近似）
    from math import erfc, sqrt, gamma
    def chi2_sf(x, k):
        # 正则化上不完全伽马函数的简单数值积分
        t = np.linspace(0, 60, 60001)
        f = t ** (k / 2 - 1) * np.exp(-t / 2)
        f = f / (2 ** (k / 2) * gamma(k / 2))
        m = t >= x
        return float(np.trapezoid(f[m], t[m])) if m.any() else 0.0
    return dict(wald=round(w, 4), df=dof, p=round(chi2_sf(w, dof), 4),
                coefs={c: dict(coef=r['coef'][c], se=r['se'][c]) for c in cols})


def callaway_santanna(df, y, lo=-4, hi=4):
    """CS(2021) 群组—时期 ATT，比较组为尚未接入城市，按事件时间聚合。"""
    gs = sorted(df['g'].unique())
    att, wts = {}, {}
    for g in gs:
        for t in YEARS:
            e = t - g
            if e < lo or e > hi or t < 2016:
                continue
            pre = g - 1
            if pre < YEARS[0]:
                continue
            trt = df[(df['g'] == g) & (df['year'].isin([pre, t]))]
            ctl = df[(df['g'] > max(t, g)) & (df['year'].isin([pre, t]))]
            if trt['city'].nunique() < 5 or ctl['city'].nunique() < 5:
                continue
            def diff(sub):
                a = sub[sub['year'] == t].groupby('city')[y].mean()
                b = sub[sub['year'] == pre].groupby('city')[y].mean()
                return (a - b).dropna()
            dt, dc = diff(trt), diff(ctl)
            if len(dt) < 5 or len(dc) < 5:
                continue
            a = dt.mean() - dc.mean()
            v = dt.var(ddof=1) / len(dt) + dc.var(ddof=1) / len(dc)
            att.setdefault(e, []).append((a, v, len(dt)))
    out = {}
    for e, lst in sorted(att.items()):
        w = np.array([x[2] for x in lst], float)
        w = w / w.sum()
        a = float(np.sum(w * np.array([x[0] for x in lst])))
        v = float(np.sum(w ** 2 * np.array([x[1] for x in lst])))
        out[str(e)] = dict(coef=round(a, 6), se=round(np.sqrt(v), 6))
    # 总体效应：对全部事后 (g,t) 单元按处理组规模加权平均（对应 aggte 的 simple 口径），
    # 与 Sun–Abraham 的群组加权口径可比。
    cells = [(a, v, n) for e, lst in att.items() if e >= 0 for (a, v, n) in lst]
    if cells:
        w = np.array([c[2] for c in cells], float); w = w / w.sum()
        a = float(np.sum(w * np.array([c[0] for c in cells])))
        v = float(np.sum(w ** 2 * np.array([c[1] for c in cells])))
        out['overall'] = dict(coef=round(a, 6), se=round(np.sqrt(v), 6))
    return out


def sun_abraham(df, y, lo=-4, hi=4, base=-1):
    """Sun & Abraham(2021) 交互加权估计：群组×事件时间交互后按群组规模加权。"""
    gs = sorted(df['g'].unique())
    d = df.copy()
    d['kk'] = d['k'].clip(lo, hi)
    cols, meta = [], []
    for g in gs[:-1]:                      # 末一群组作参照，避免共线
        for kv in range(lo, hi + 1):
            if kv == base:
                continue
            c = f'G{g}_K{kv}'.replace('-', 'm')
            d[c] = ((d['g'] == g) & (d['kk'] == kv)).astype(float)
            if d[c].sum() > 0:
                cols.append(c)
                meta.append((g, kv))
    r = _within(d, y, cols + CTRL)
    share = d.groupby('g')['city'].nunique()
    share = share / share.sum()
    agg = {}
    for (g, kv), c in zip(meta, cols):
        agg.setdefault(kv, []).append((r['coef'][c], r['se'][c], float(share[g])))
    out = {}
    for kv, lst in sorted(agg.items()):
        w = np.array([x[2] for x in lst]); w = w / w.sum()
        out[str(kv)] = dict(coef=round(float(np.sum(w * np.array([x[0] for x in lst]))), 6),
                            se=round(float(np.sqrt(np.sum(w ** 2 * np.array([x[1] for x in lst]) ** 2))), 6))
    # 总体效应：先在每个群组内部对其**实际可观测**的事后期取平均，再按群组规模加权，
    # 避免把只观测到 k=0、1 的晚接入群组与观测到 k=0—4 的早接入群组直接混平均。
    by_g = {}
    for (g, kv), c in zip(meta, cols):
        if kv >= 0:
            by_g.setdefault(g, []).append((r['coef'][c], r['se'][c]))
    num, var, wsum = 0.0, 0.0, 0.0
    for g, lst in by_g.items():
        a_g = float(np.mean([x[0] for x in lst]))
        v_g = float(np.mean([x[1] ** 2 for x in lst]) / len(lst))
        w_g = float(share[g])
        num += w_g * a_g; var += (w_g ** 2) * v_g; wsum += w_g
    out['overall'] = dict(coef=round(num / wsum, 6), se=round(float(np.sqrt(var)) / wsum, 6))
    return out


def placebo(df, y, reps=500):
    """随机打乱处理年份，检验基准估计是否为偶然。"""
    gs = df.groupby('city')['g'].first().to_numpy()
    coefs = []
    for _ in range(reps):
        perm = RNG.permutation(gs)
        m = dict(zip(sorted(df['city'].unique()), perm))
        d = df.copy()
        d['g_f'] = d['city'].map(m)
        d['post'] = (d['year'] >= d['g_f']).astype(float)
        coefs.append(_within(d, y, ['post'] + CTRL)['coef']['post'])
    coefs = np.array(coefs)
    true = twfe(df, y)['coef']['post']
    return dict(mean=round(float(coefs.mean()), 6), sd=round(float(coefs.std()), 6),
                p_two_sided=round(float(np.mean(np.abs(coefs) >= abs(true))), 4),
                true=round(float(true), 6), reps=reps)


def hetero(df, y, modvar, label):
    """按调节变量的中位数分组分别估计。"""
    med = df.groupby('city')[modvar].first().median()
    hi_c = df.groupby('city')[modvar].first()
    hi_set = set(hi_c[hi_c > med].index)
    out = {}
    for nm, sel in (('high', df['city'].isin(hi_set)), ('low', ~df['city'].isin(hi_set))):
        r = twfe(df[sel], y)
        out[nm] = dict(coef=r['coef']['post'], se=r['se']['post'], p=r['p']['post'], n=r['n'])
    d = out['high']['coef'] - out['low']['coef']
    sd = np.sqrt(out['high']['se'] ** 2 + out['low']['se'] ** 2)
    out['diff'] = dict(coef=round(float(d), 6), se=round(float(sd), 6),
                       z=round(float(d / sd), 4))
    out['modvar'] = modvar
    out['label'] = label
    return out


def iv_outflow(df):
    """以高铁通达度作为跨区就医强度的外生变动，估计其对费用缺口的影响。"""
    d = df.copy()
    d['hsr_post'] = d['hsr'] * d['post']
    first = _within(d, 'outflow_share', ['hsr_post', 'post'] + CTRL)
    d['fit'] = np.nan
    # 简化两阶段：用第一阶段拟合值替代内生变量
    sub = d[['outflow_share', 'hsr_post', 'post'] + CTRL + ['city', 'year']].dropna()
    Xn = sub[['hsr_post', 'post'] + CTRL].to_numpy(float)
    fit = Xn @ np.array([first['coef'][c] for c in ['hsr_post', 'post'] + CTRL])
    d.loc[sub.index, 'fit'] = fit
    second = _within(d, 'ln_gap', ['fit'] + CTRL)
    F = (first['coef']['hsr_post'] / first['se']['hsr_post']) ** 2
    return dict(first_stage=dict(coef=first['coef']['hsr_post'], se=first['se']['hsr_post'],
                                 F=round(float(F), 2)),
                second_stage=dict(coef=second['coef']['fit'], se=second['se']['fit'],
                                  p=second['p']['fit']))


# ============================ 四、主程序 ============================


def main():
    df = build_panel()
    df.to_csv(os.path.join(DATA, 'panel.csv'), index=False, encoding='utf-8-sig')

    OUT = {'anchor': ANCHOR, 'sample': dict(
        ncity=NCITY, years=[YEARS[0], YEARS[-1]], nobs=int(len(df)),
        cohorts={str(k): v for k, v in COHORTS.items()})}

    YS = {
        'outflow_share': '跨区就医人次占比',
        'ln_cost_inp': '本地次均住院费用（对数）',
        'ln_gap': '外地—本地次均费用比（对数）',
        'local_adm_rate': '本地住院率',
        'markup': '医院加成率',
        'fund_outflow': '医保基金外流率',
        'nonlocal_rev_share': '三级医院外地患者收入占比',
        'primary_share': '基层诊疗量占比',
    }

    OUT['desc'] = {}
    for y, lab in YS.items():
        s = df[y]
        OUT['desc'][y] = dict(label=lab, mean=round(float(s.mean()), 4),
                              sd=round(float(s.std()), 4), p25=round(float(s.quantile(.25)), 4),
                              p50=round(float(s.median()), 4), p75=round(float(s.quantile(.75)), 4),
                              min=round(float(s.min()), 4), max=round(float(s.max()), 4))
    for c in CTRL + ['resident_share', 'hhi', 'hsr']:
        s = df[c]
        OUT['desc'][c] = dict(label=c, mean=round(float(s.mean()), 4),
                              sd=round(float(s.std()), 4), p25=round(float(s.quantile(.25)), 4),
                              p50=round(float(s.median()), 4), p75=round(float(s.quantile(.75)), 4),
                              min=round(float(s.min()), 4), max=round(float(s.max()), 4))

    OUT['baseline'] = {}
    for y in YS:
        OUT['baseline'][y] = dict(nocontrol=twfe(df, y, ctrl=False), full=twfe(df, y))
        print('baseline', y, OUT['baseline'][y]['full']['coef']['post'])

    OUT['event'] = {y: event_study(df, y) for y in
                    ['outflow_share', 'ln_cost_inp', 'ln_gap', 'local_adm_rate']}
    OUT['concurrent'] = {}
    for y in ['outflow_share', 'ln_cost_inp', 'ln_gap', 'local_adm_rate']:
        r = _within(df, y, ['post', 'mz_post', 'drg_post'] + CTRL)
        OUT['concurrent'][y] = dict(
            coef=r['coef']['post'], se=r['se']['post'], p=r['p']['post'], n=r['n'],
            mz=dict(coef=r['coef']['mz_post'], se=r['se']['mz_post'], p=r['p']['mz_post']),
            drg=dict(coef=r['coef']['drg_post'], se=r['se']['drg_post'], p=r['p']['drg_post']))

    # 更换聚类层级：省级（按城市编号分组为 31 个省）
    df['prov'] = df['city'] % 31
    OUT['cluster_prov'] = {}
    for y in ['outflow_share', 'ln_cost_inp', 'ln_gap', 'local_adm_rate']:
        r = _within(df, y, ['post'] + CTRL, ent='prov')
        OUT['cluster_prov'][y] = dict(coef=r['coef']['post'], se=r['se']['post'],
                                      p=r['p']['post'], ncluster=r['ncluster'])

    OUT['citytrend'] = {}
    for y in ['outflow_share', 'ln_cost_inp', 'ln_gap', 'local_adm_rate']:
        r = twfe_citytrend(df, y)
        OUT['citytrend'][y] = dict(coef=r['coef']['post'], se=r['se']['post'],
                                   p=r['p']['post'], n=r['n'])
    OUT['pretrend'] = {y: pretrend_test(df, y) for y in
                       ['outflow_share', 'ln_cost_inp', 'ln_gap', 'local_adm_rate']}
    OUT['cs'] = {y: callaway_santanna(df, y) for y in
                 ['outflow_share', 'ln_cost_inp', 'ln_gap', 'local_adm_rate']}
    OUT['sa'] = {y: sun_abraham(df, y) for y in ['outflow_share', 'ln_gap']}
    OUT['placebo'] = {y: placebo(df, y, reps=500) for y in ['outflow_share', 'ln_gap']}
    OUT['iv'] = iv_outflow(df)

    OUT['hetero'] = {
        'liquidity': hetero(df, 'outflow_share', 'resident_share', '居民医保参保占比'),
        'competition': hetero(df, 'ln_cost_inp', 'hhi', '本地医院集中度'),
        'externality': hetero(df, 'ln_gap', 'inflow_type', '净流入城市'),
    }

    # 政策模拟：把异地就医纳入就医地 DRG／DIP 统一管理，等价于把监管强度差 s_L-s_F 压缩
    gap_att = OUT['baseline']['ln_gap']['full']['coef']['post']
    cost_att = OUT['baseline']['ln_cost_inp']['full']['coef']['post']
    outflow_att = OUT['baseline']['outflow_share']['full']['coef']['post']
    # 底数用 2024 年跨省异地就医直接结算"减少个人垫付"额，它近似等于当年跨省就医的基金报销规模，
    # 比"基金总支出×跨省住院人次占比"更贴近口径（跨省患者次均费用高于全国平均）。
    cross_fund = ANCHOR['settle_saved_yi'][2024]
    for rho in (0.5, 0.75, 1.0):
        saved = cross_fund * (np.exp(gap_att * rho) - 1) / np.exp(gap_att * rho)
        OUT.setdefault('policy_sim', {})[f'unify_{int(rho*100)}'] = dict(
            rho=rho, gap_closed=round(float(gap_att * rho), 6),
            fund_saved_yi=round(float(abs(saved)), 2))
    OUT['policy_sim']['note'] = ('底数为 2024 年跨省异地就医减少个人垫付额 1947.25 亿元，'
                                 'ρ 为监管统一后费用缺口被压缩的比例')
    OUT['policy_sim']['att'] = dict(gap=gap_att, cost=cost_att, outflow=outflow_att)

    with open(os.path.join(DATA, 'results.json'), 'w', encoding='utf-8') as f:
        json.dump(OUT, f, ensure_ascii=False, indent=1)
    print('saved data/results.json  &  data/panel.csv;  N =', len(df))


if __name__ == '__main__':
    main()
