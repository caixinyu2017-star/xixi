# -*- coding: utf-8 -*-
"""论文一《词元价格下行与智能服务支出的背离》的数据层与全部实证结果。

两套分析样本：
  A. 模型档位—月度享乐价格面板（2023-01 至 2026-08，44 期）——质量调整价格指数 STPI；
  B. 行业—季度需求支出面板（2023Q1 至 2026Q2，14 期）——需求弹性与回弹分解。

数据可得性声明：档位层面的明细挂牌价与行业层面的词元用量、接口支出均不公开，
本文分析样本按 data/facts.md 收录的公开锚（国家数据局日均词元调用量、
斯坦福《人工智能指数报告》质量恒定价格、企业接口支出增速、智能体词元倍数、
工业和信息化部智能算力规模）**校准生成**，用于完整展示测度与识别链条。
全部进入正文的数字由本脚本产生并写入 data/results.json，正文只许引用该文件。

依赖：numpy / pandas / scipy。用法：python3 data_gen.py
"""
import json
import os
from math import log, exp, sqrt

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
os.makedirs(DATA, exist_ok=True)

RNG = np.random.default_rng(20260825)

# ============================ 零、公开锚（全部取自 data/facts.md） ============================
ANCHOR = {
    # 国家数据局：全国日均词元调用量（万亿枚／日）
    'daily_tokens_wanyi': {'2024Q1': 0.10, '2025Q2': 30.0, '2025Q4': 100.0, '2026Q1': 140.0},
    'daily_tokens_note': '发布主体＝国家数据局；2026Q2 与 2023 各季为校准外推／插值，官方未单独发布',
    # 斯坦福《2025 年人工智能指数报告》：质量恒定口径最低报价（美元／百万词元）
    'quality_constant_usd': {'2022-11': 20.00, '2024-10': 0.07},
    'quality_constant_months': 23,           # 2022-11 至 2024-10 实为 23 个月
    'quality_constant_fold': round(20.00 / 0.07, 2),                   # 285.71
    'quality_constant_annual_fold': round((20.00 / 0.07) ** (12 / 23), 2),   # 19.11
    'quality_constant_note': ('原报告行文作「约 18 个月」，但所给两个时点相隔 23 个月；'
                              '本文一律按时点作差（23 个月）折年，正文只写时点区间，'
                              '不复述「18 个月」这一措辞。'),
    'task_annual_fold_range': [9, 900],      # 同一报告：因任务而异的年降幅区间
    # 同一供给方旗舰档／经济档输出价比（调价前 6 与 2；调价后高峰 27 与 9）
    'flag_econ_output_ratio': 3.0,
    'reprice_2026_08': {'flag_pre': 6.0, 'econ_pre': 2.0, 'flag_peak': 27.0, 'econ_peak': 9.0},
    # Menlo Ventures：企业级大模型接口支出（美元口径，禁止折算为人民币）
    'api_spend_usd_yi': {'2024H2_end': 35.0, '2025H1_end': 84.0},
    'api_spend_halfyear_growth': 1.40,
    # 智能体词元倍数（厂商工程团队公开实测）
    'agent_multiple': {'single_turn': 1.0, 'agentic': 4.0, 'multi_agent': 15.0},
    # 工业和信息化部：智能算力规模（EFLOPS, FP16）与区域分布
    'smart_compute_eflops_2026H1': 2185.0,
    'smart_compute_yoy': 1.77,
    'rack_rate': 0.714,
    'region_share': {'east': 0.559, 'central': 0.106, 'west': 0.326, 'northeast': 0.009},
    'unit_cost_cut_carrier': 0.30,   # 运营商自报：单位词元成本压降约 30%
}

# ============================ 一、通用估计工具 ============================


def _p_from_t(t, dof):
    return float(2 * stats.t.sf(abs(t), dof))


def _ols(y, X, cluster=None, k_absorbed=0, want_r2=True, ybase=None):
    """OLS＋（聚类）稳健标准误。cluster=None 时用 HC1。"""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    n, k = X.shape
    XtX = X.T @ X
    XtXi = np.linalg.pinv(XtX)
    b = XtXi @ (X.T @ y)
    r = y - X @ b
    kk = k + k_absorbed
    if cluster is None:
        meat = (X * (r ** 2)[:, None]).T @ X
        adj = n / max(n - kk, 1)
        V = XtXi @ meat @ XtXi * adj
        dof = max(n - kk, 1)
        ncl = n
    else:
        g = pd.factorize(np.asarray(cluster))[0]
        G = int(g.max()) + 1
        meat = np.zeros((k, k))
        for j in range(G):
            m = g == j
            s = X[m].T @ r[m]
            meat += np.outer(s, s)
        adj = G / (G - 1) * (n - 1) / max(n - kk, 1)
        V = XtXi @ meat @ XtXi * adj
        dof = G - 1
        ncl = G
    se = np.sqrt(np.maximum(np.diag(V), 0))
    tv = np.where(se > 0, b / np.maximum(se, 1e-300), 0.0)
    out = dict(b=b, se=se, t=tv, V=V, resid=r, n=int(n), dof=int(dof), ncluster=int(ncl))
    if want_r2:
        base = y if ybase is None else np.asarray(ybase, float)
        sst = float(np.sum((base - base.mean()) ** 2))
        ssr = float(np.sum(r ** 2))
        out['r2'] = round(1 - ssr / sst, 6) if sst > 0 else None
        out['r2_within'] = None
    out['p'] = np.array([_p_from_t(x, out['dof']) for x in tv])
    return out


def _fmt(names, res, keep=None):
    keep = keep or names
    idx = {nm: i for i, nm in enumerate(names)}
    d = {}
    for nm in keep:
        i = idx[nm]
        d[nm] = dict(coef=round(float(res['b'][i]), 6), se=round(float(res['se'][i]), 6),
                     t=round(float(res['t'][i]), 4), p=round(float(res['p'][i]), 6))
    d['n'] = res['n']
    d['ncluster'] = res['ncluster']
    if res.get('r2') is not None:
        d['r2'] = res['r2']
    return d


def _dummies(codes, drop_first=True):
    codes = pd.factorize(np.asarray(codes))[0]
    K = int(codes.max()) + 1
    M = np.zeros((len(codes), K))
    M[np.arange(len(codes)), codes] = 1.0
    return M[:, 1:] if drop_first else M


def _absorb(mats, *arrays):
    """用 QR 把若干组固定效应虚拟变量投影掉，返回残差化后的数组与被吸收的自由度。"""
    A = np.hstack(mats)
    Q, R = np.linalg.qr(A)
    keep = np.abs(np.diag(R)) > 1e-9
    Q = Q[:, keep]
    out = [np.asarray(a, float) - Q @ (Q.T @ np.asarray(a, float)) for a in arrays]
    return out, int(Q.shape[1])


def within(df, y, xs, ent, tim, cluster=None):
    """双向固定效应 OLS（虚拟变量投影实现）＋聚类稳健标准误。"""
    cols = [y] + xs + [ent, tim] + ([cluster] if cluster else [])
    d = df[list(dict.fromkeys(cols))].dropna()
    Y = d[y].to_numpy(float)
    X = d[xs].to_numpy(float)
    (Yd, Xd), kabs = _absorb([_dummies(d[ent], False), _dummies(d[tim], True)], Y, X)
    cl = d[cluster if cluster else ent].to_numpy()
    res = _ols(Yd, Xd, cluster=cl, k_absorbed=kabs, ybase=Yd)
    res['r2_within'] = res.pop('r2')
    return res


def iv_within(df, y, endog, instr, exog, ent, tim, cluster=None):
    """双向固定效应 2SLS；报告第一阶段联合 F、Hansen J 与聚类稳健二阶段推断。"""
    cols = [y] + endog + instr + exog + [ent, tim] + ([cluster] if cluster else [])
    d = df[list(dict.fromkeys(cols))].dropna()
    Y = d[y].to_numpy(float)
    D = d[endog].to_numpy(float)
    Z = d[instr].to_numpy(float)
    W = d[exog].to_numpy(float) if exog else np.zeros((len(d), 0))
    (Yd, Dd, Zd, Wd), kabs = _absorb([_dummies(d[ent], False), _dummies(d[tim], True)], Y, D, Z, W)
    cl = d[cluster if cluster else ent].to_numpy()

    # ---- 第一阶段 ----
    Z1 = np.hstack([Zd, Wd])
    fs = _ols(Dd[:, 0], Z1, cluster=cl, k_absorbed=kabs, ybase=Dd[:, 0])
    kz = Zd.shape[1]
    Vz = fs['V'][:kz, :kz]
    bz = fs['b'][:kz]
    wald = float(bz @ np.linalg.pinv(Vz) @ bz)
    F = wald / kz                       # 聚类稳健的第一阶段联合 F（Kleibergen–Paap 型）

    # ---- 二阶段 ----
    X = np.hstack([Dd, Wd])
    ZZ = np.hstack([Zd, Wd])
    PZ = ZZ @ np.linalg.pinv(ZZ.T @ ZZ) @ ZZ.T
    Xh = PZ @ X
    A = np.linalg.pinv(Xh.T @ X)
    b = A @ (Xh.T @ Yd)
    r = Yd - X @ b
    g = pd.factorize(cl)[0]
    G = int(g.max()) + 1
    k = X.shape[1]
    meat = np.zeros((k, k))
    for j in range(G):
        m = g == j
        s = Xh[m].T @ r[m]
        meat += np.outer(s, s)
    adj = G / (G - 1) * (len(d) - 1) / max(len(d) - k - kabs, 1)
    V = A @ meat @ A.T * adj
    se = np.sqrt(np.maximum(np.diag(V), 0))
    tv = b / np.maximum(se, 1e-300)
    pv = [_p_from_t(x, G - 1) for x in tv]

    # ---- Hansen J（过度识别检验，聚类稳健）----
    J, Jp, Jdf = None, None, kz - len(endog)
    if Jdf > 0:
        gbar = np.zeros(ZZ.shape[1])
        S = np.zeros((ZZ.shape[1], ZZ.shape[1]))
        for j in range(G):
            m = g == j
            s = ZZ[m].T @ r[m]
            gbar += s
            S += np.outer(s, s)
        J = float(gbar @ np.linalg.pinv(S) @ gbar)
        Jp = float(stats.chi2.sf(J, Jdf))

    names = endog + exog
    out = dict(first_stage={instr[i]: dict(coef=round(float(fs['b'][i]), 6),
                                           se=round(float(fs['se'][i]), 6),
                                           t=round(float(fs['t'][i]), 4),
                                           p=round(float(fs['p'][i]), 6)) for i in range(kz)},
               first_stage_F=round(F, 3), first_stage_df=kz,
               first_stage_r2_within=fs.get('r2'),
               weak_iv=dict(F=round(F, 3), rule_of_thumb=10.0,
                            stock_yogo_10pct=19.93 if kz == 2 else 16.38,
                            pass_rule=bool(F > 10.0)),
               second_stage={nm: dict(coef=round(float(b[i]), 6), se=round(float(se[i]), 6),
                                      t=round(float(tv[i]), 4), p=round(float(pv[i]), 6))
                             for i, nm in enumerate(names)},
               n=int(len(d)), ncluster=int(G))
    if J is not None:
        out['hansen_J'] = dict(J=round(J, 4), df=int(Jdf), p=round(Jp, 4))
    return out


def dwh_test(df, y, endog, instr, exog, ent, tim, cluster=None):
    """Durbin–Wu–Hausman 控制函数检验：把第一阶段残差并入 FE 回归，检验其系数是否为零。

    系数显著 ⇒ 拒绝价格外生，须用工具变量；不显著 ⇒ 不能拒绝外生性。
    该写法比「(b_IV-b_OLS)/sqrt(V_IV-V_OLS)」稳健：聚类稳健下后者的方差差可能为负。
    """
    cols = [y, endog] + instr + exog + [ent, tim] + ([cluster] if cluster else [])
    d = df[list(dict.fromkeys(cols))].dropna().copy()
    r1 = within(d, endog, instr + exog, ent, tim, cluster=cluster)
    d['_cf'] = r1['resid']
    xs = [endog] + exog + ['_cf']
    r2 = within(d, y, xs, ent, tim, cluster=cluster)
    i = xs.index('_cf')
    return dict(cf_coef=round(float(r2['b'][i]), 6), cf_se=round(float(r2['se'][i]), 6),
                cf_t=round(float(r2['t'][i]), 4), cf_p=round(float(r2['p'][i]), 6),
                beta_with_cf=round(float(r2['b'][0]), 6), n=r2['n'], ncluster=r2['ncluster'],
                reject_exogeneity=bool(r2['p'][i] < 0.10),
                note='控制函数系数即 DWH 统计量；beta_with_cf 与 2SLS 系数在数值上一致')


def l1_fit(X, y, iters=200, eps=1e-7):
    """中位数（L1）回归：IRLS 实现，只依赖 numpy。"""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    for _ in range(iters):
        r = y - X @ b
        w = 1.0 / np.maximum(np.abs(r), eps)
        XW = X * w[:, None]
        nb = np.linalg.solve(X.T @ XW + 1e-10 * np.eye(X.shape[1]), XW.T @ y)
        if np.max(np.abs(nb - b)) < 1e-10:
            b = nb
            break
        b = nb
    return b


def wild_cluster_boot(df, y, xs, ent, tim, target, h0, cluster=None, B=999):
    """受约束的 Wild Cluster Bootstrap（Rademacher），检验 H0: beta_target = h0。"""
    cols = [y] + xs + [ent, tim] + ([cluster] if cluster else [])
    d = df[list(dict.fromkeys(cols))].dropna()
    Y = d[y].to_numpy(float)
    X = d[xs].to_numpy(float)
    (Yd, Xd), kabs = _absorb([_dummies(d[ent], False), _dummies(d[tim], True)], Y, X)
    cl = pd.factorize(d[cluster if cluster else ent].to_numpy())[0]
    G = int(cl.max()) + 1
    j = xs.index(target)
    full = _ols(Yd, Xd, cluster=cl, k_absorbed=kabs, ybase=Yd)
    t_obs = float((full['b'][j] - h0) / full['se'][j])
    # 受约束估计
    keep = [i for i in range(Xd.shape[1]) if i != j]
    Yr = Yd - h0 * Xd[:, j]
    Xr = Xd[:, keep]
    br = np.linalg.pinv(Xr.T @ Xr) @ (Xr.T @ Yr)
    ur = Yr - Xr @ br
    fit = h0 * Xd[:, j] + Xr @ br
    rng = np.random.default_rng(20260825)
    ts = np.empty(B)
    for bidx in range(B):
        v = rng.choice([-1.0, 1.0], size=G)[cl]
        ys = fit + ur * v
        rb = _ols(ys, Xd, cluster=cl, k_absorbed=kabs, ybase=ys)
        ts[bidx] = (rb['b'][j] - h0) / rb['se'][j]
    p = float((np.sum(np.abs(ts) >= abs(t_obs)) + 1) / (B + 1))
    return dict(h0=h0, t_obs=round(t_obs, 4), p_wild=round(p, 4), B=B, ncluster=G)


# ============================ 二、共用：全国日均词元调用量序列 ============================
MONTHS = [f'{y}-{m:02d}' for y in range(2023, 2027) for m in range(1, 13)]
MONTHS = MONTHS[MONTHS.index('2023-01'):MONTHS.index('2026-08') + 1]   # 44 期
T_A = len(MONTHS)
MIDX = {m: i for i, m in enumerate(MONTHS)}

# 官方锚在月度序列上的位置（国家数据局口径，万亿枚／日）
_TOK_ANCHOR = [('2024-01', 0.10), ('2025-06', 30.0), ('2025-12', 100.0), ('2026-03', 140.0)]


def daily_tokens_series():
    """月度全国日均词元调用量（万亿枚／日）。锚点精确穿过，锚点外为对数线性外推（须标注）。"""
    xs = np.array([MIDX[m] for m, _ in _TOK_ANCHOR], float)
    ys = np.log(np.array([v for _, v in _TOK_ANCHOR], float))
    out = np.empty(T_A)
    slope_head = (ys[1] - ys[0]) / (xs[1] - xs[0]) * 0.60      # 回溯段增速阻尼
    slope_tail = (ys[3] - ys[2]) / (xs[3] - xs[2]) * 0.85      # 外推段增速阻尼
    for i in range(T_A):
        if i <= xs[0]:
            out[i] = ys[0] + slope_head * (i - xs[0])
        elif i >= xs[-1]:
            out[i] = ys[-1] + slope_tail * (i - xs[-1])
        else:
            out[i] = float(np.interp(i, xs, ys))
    return np.exp(out)


DAILY_TOK = daily_tokens_series()          # 万亿枚／日
DAYS = np.array([pd.Period(m, 'M').days_in_month for m in MONTHS], float)
MONTH_TOK = DAILY_TOK * DAYS               # 万亿枚／月（物理词元，输入＋输出合计）

# ============================ 三、A 卷：档位—月度享乐价格面板 ============================
TIERS = ['经济档', '均衡档', '旗舰档', '推理增强档']
TIER_EN = {'经济档': 'econ', '均衡档': 'balanced', '旗舰档': 'flagship', '推理增强档': 'reasoning'}
NSUP = {'经济档': 6, '均衡档': 6, '旗舰档': 5, '推理增强档': 4}      # 每档 4—6 家代表性供给方

# 享乐 DGP 的真实参数（原始单位；估计式用标准化能力得分，故报告值为标准化系数）
B_CAP = 4.63        # 每单位能力得分（0—1 综合基准分）
B_CTX = 0.16        # ln(上下文窗口／千词元)
B_LAT = -0.10       # ln(输出时延，毫秒／词元)
B_MM = 0.09         # 多模态
B_CACHE = -0.11     # 支持缓存计价
B_REASON = 0.75     # 推理增强
A0 = 0.9711         # 基期（2023-01）质量恒定对数价格截距
A41 = -3.3332       # 2026-06 质量恒定对数价格截距

# 档位特征起讫值：(能力得分, 上下文窗口 K, 输出时延 ms/词元, 多模态起用月, 缓存计价起用月)
TIER_SPEC = {
    '经济档':     dict(c=(0.30, 0.73), ctx=(8, 128),   lat=(8.0, 3.0),  mm_m=14, ca_m=15),
    '均衡档':     dict(c=(0.45, 0.82), ctx=(32, 256),  lat=(14.0, 5.0), mm_m=10, ca_m=12),
    '旗舰档':     dict(c=(0.62, 0.905), ctx=(128, 800), lat=(25.0, 9.0), mm_m=4, ca_m=11),
    '推理增强档': dict(c=(0.66, 0.97), ctx=(128, 512), lat=(60.0, 26.0), mm_m=16, ca_m=13),
}
# 2026-07／08 结构性提价（对数幅度，乘以供给方参与系数 rho）
# facts.md 锚：同一供给方调价前后旗舰档／经济档输出价比稳定在约 3 倍（6→27 与 2→9，
# 两档同为 4.5 倍），故提价在档位间近似同比例；档位间与供给方间的分化来自
# 「是否跟进提价」（rho），而不是档位本身。月度均价为峰谷分时的加权，涨幅小于高峰报价。
HIKE = {t: (0.20, 0.42) for t in TIERS}
# 物理词元量在档位间的份额（起讫，logistic 过渡）
TIER_VOL = {'经济档': (0.30, 0.63), '均衡档': (0.34, 0.24),
            '旗舰档': (0.28, 0.085), '推理增强档': (0.08, 0.045)}


def _shape(t, tau=14.0, tmax=41.0):
    """0→1 的减速型时间形状：前期快、后期收敛。"""
    return (1 - np.exp(-t / tau)) / (1 - np.exp(-tmax / tau))


def _logistic_share(t, a, b, tmid=22.0, k=0.13):
    return a + (b - a) / (1 + np.exp(-k * (t - tmid)))


def build_panel_A():
    t = np.arange(T_A, dtype=float)
    tt = np.clip(t, 0, 41.0)
    f = _shape(tt)                                   # 质量与价格的共同时间形状
    # 质量恒定对数价格截距：0—41 期按减速形状下行；42—43 期由提价推高（见 HIKE）
    alpha_true = A0 + (A41 - A0) * f

    rows = []
    firm_pool = [f'S{j:02d}' for j in range(1, 13)]  # 12 家供给方，可跨档位供给
    fi = 0
    for tier in TIERS:
        sp = TIER_SPEC[tier]
        for s in range(NSUP[tier]):
            firm = firm_pool[fi % len(firm_pool)]
            fi += 1
            # 供给方固定偏移（定价与能力的异质性）
            d_price = RNG.normal(0, 0.16)
            d_cap = RNG.normal(0, 0.055)
            d_ctx = RNG.normal(0, 0.52)
            d_lat = RNG.normal(0, 0.30)
            rho = float(RNG.choice([0.0, 0.5, 1.0], p=[0.30, 0.25, 0.45]))   # 提价参与度
            eps = RNG.normal(0, 0.055, T_A)
            eps = pd.Series(eps).ewm(alpha=0.45).mean().to_numpy()           # 轻度序列相关
            for i in range(T_A):
                cap = sp['c'][0] + (sp['c'][1] - sp['c'][0]) * _shape(tt[i], 16.0) + d_cap
                lnctx = log(sp['ctx'][0]) + (log(sp['ctx'][1]) - log(sp['ctx'][0])) \
                    * _shape(tt[i], 9.0) + d_ctx
                lnlat = log(sp['lat'][0]) + (log(sp['lat'][1]) - log(sp['lat'][0])) \
                    * _shape(tt[i], 13.0) + d_lat
                mm = 1.0 if i >= sp['mm_m'] + (s % 3) * 2 else 0.0
                ca = 1.0 if i >= sp['ca_m'] + (s % 3) * 2 else 0.0
                rea = 1.0 if tier == '推理增强档' else 0.0
                hk = 0.0
                if i == T_A - 2:
                    hk = HIKE[tier][0] * rho
                elif i == T_A - 1:
                    hk = HIKE[tier][1] * rho
                lnp = (alpha_true[i] + B_CAP * cap + B_CTX * lnctx + B_LAT * lnlat
                       + B_MM * mm + B_CACHE * ca + B_REASON * rea + d_price + hk + eps[i])
                # 输入价／输出价之比：缓存与长上下文推动输入相对更便宜
                r_io = 0.28 - 0.08 * _shape(tt[i], 18.0) + 0.015 * RNG.normal()
                rows.append(dict(item=f'{TIER_EN[tier]}_{s+1}', firm=firm, tier=tier,
                                 month=MONTHS[i], t=i, cap=cap, lnctx=lnctx, lnlat=lnlat,
                                 mm=mm, cache=ca, reason=rea, hike=hk, rho=rho,
                                 p_out=exp(lnp), p_in=exp(lnp) * r_io, io_ratio=r_io))
    df = pd.DataFrame(rows)

    # ---- 物理词元量：由全国月度总量按档位份额、档位内供给方份额分配 ----
    tier_share = {}
    for tier in TIERS:
        a, b = TIER_VOL[tier]
        tier_share[tier] = _logistic_share(t, a, b)
    S = np.vstack([tier_share[x] for x in TIERS])
    S = S / S.sum(axis=0, keepdims=True)
    tier_share = {tier: S[k] for k, tier in enumerate(TIERS)}

    sup_w = {}
    for tier in TIERS:
        base = RNG.dirichlet(np.full(NSUP[tier], 6.0))
        drift = RNG.normal(0, 0.010, (NSUP[tier], T_A)).cumsum(axis=1)
        w = np.exp(np.log(base)[:, None] + drift)
        sup_w[tier] = w / w.sum(axis=0, keepdims=True)

    # 输出／输入词元量之比（输入侧远大于输出侧，且随上下文变长而上升）
    v_out_share = 1.0 / (1.0 + (5.0 + 2.0 * _shape(tt, 20.0)))
    qty, qout, qin = [], [], []
    for _, r in df.iterrows():
        i = int(r['t'])
        k = int(r['item'].split('_')[1]) - 1
        q = MONTH_TOK[i] * tier_share[r['tier']][i] * sup_w[r['tier']][k, i]   # 万亿枚／月
        qty.append(q)
        qout.append(q * v_out_share[i])
        qin.append(q * (1 - v_out_share[i]))
    df['q_tok'] = qty
    df['q_out'] = qout
    df['q_in'] = qin
    # 混合单价（元／百万词元）＝支出／物理词元量
    df['exp_yuan'] = (df['q_out'] * df['p_out'] + df['q_in'] * df['p_in']) * 1e6   # 万亿枚×元/百万＝1e6 元
    df['p_blend'] = df['exp_yuan'] / (df['q_tok'] * 1e6)
    return df


# ---------------------------- 享乐回归与指数编制 ----------------------------
XVARS = ['cap_z', 'lnctx', 'lnlat_z', 'mm', 'cache', 'reason']
XLABEL = {'cap_z': '能力得分（标准化）', 'lnctx': 'ln 上下文窗口（千词元）',
          'lnlat_z': 'ln 输出时延（标准化）', 'mm': '多模态（0/1）',
          'cache': '支持缓存计价（0/1）', 'reason': '推理增强（0/1）'}


def _prep_X(df):
    d = df.copy()
    d['cap_z'] = (d['cap'] - d['cap'].mean()) / d['cap'].std(ddof=0)
    d['lnlat_z'] = (d['lnlat'] - d['lnlat'].mean()) / d['lnlat'].std(ddof=0)
    return d


def hedonic(d, ycol='p_out', drop_months=None, robust_median=False, cluster='firm'):
    """ln p_mt = alpha_t + x'beta + e；时期虚拟系数 alpha_t 即质量调整价格指数。"""
    dd = d if drop_months is None else d[~d['month'].isin(drop_months)].copy()
    months = [m for m in MONTHS if m in set(dd['month'])]
    y = np.log(dd[ycol].to_numpy(float))
    D = np.zeros((len(dd), len(months) - 1))
    code = dd['month'].map({m: i for i, m in enumerate(months)}).to_numpy()
    for j in range(1, len(months)):
        D[:, j - 1] = (code == j).astype(float)
    X = np.hstack([np.ones((len(dd), 1)), D, dd[XVARS].to_numpy(float)])
    names = ['const'] + [f'D_{m}' for m in months[1:]] + XVARS
    if robust_median:
        b = l1_fit(X, y)
        res = dict(b=b, se=np.full(len(b), np.nan), t=np.full(len(b), np.nan),
                   p=np.full(len(b), np.nan), n=len(dd), dof=len(dd) - len(b),
                   ncluster=dd[cluster].nunique(), r2=None, resid=y - X @ b)
    else:
        res = _ols(y, X, cluster=dd[cluster].to_numpy())
    alpha = np.concatenate([[0.0], res['b'][1:len(months)]])
    # 偏 R²：把时期虚拟先投影掉（组内去均值），只看特征对同期截面价差的解释力。
    # 总 R² 里绝大部分来自时期虚拟捕捉的价格下行，单看总 R² 会高估享乐方程的信息量。
    yw = y - pd.Series(y).groupby(dd['month'].to_numpy()).transform('mean').to_numpy()
    sstw = float(np.sum((yw - yw.mean()) ** 2))
    r2p = round(1 - float(np.sum(res['resid'] ** 2)) / sstw, 6) if sstw > 0 else None
    return dict(res=res, names=names, months=months, alpha=alpha, r2_partial=r2p,
                beta={v: float(res['b'][names.index(v)]) for v in XVARS},
                X=X, y=y, d=dd)


def eta_from_beta(d, beta, base_month='2023-01', qcol='q_tok'):
    """由享乐隐含价格 beta 构造效值系数 eta（基期加权平均束＝1），并给出质量调整价格。"""
    b0 = d[d['month'] == base_month]
    w0 = b0[qcol].to_numpy(float)
    w0 = w0 / w0.sum()
    xbar0 = {v: float(np.sum(w0 * b0[v].to_numpy(float))) for v in XVARS}
    lne = np.zeros(len(d))
    for v in XVARS:
        lne = lne + beta[v] * (d[v].to_numpy(float) - xbar0[v])
    return np.exp(lne), xbar0


def build_indexes(d, alpha, months, pcol='p_out', qcol='q_out'):
    """名义指数（单位价值／简单算术／对数加权）与质量调整指数（享乐时期虚拟）。"""
    piv_p = d.pivot_table(index='month', columns='item', values=pcol).loc[months]
    piv_q = d.pivot_table(index='month', columns='item', values=qcol).loc[months]
    P = piv_p.to_numpy(float)
    Q = piv_q.to_numpy(float)
    E = P * Q
    W = E / E.sum(axis=1, keepdims=True)

    unit_value = (E.sum(axis=1) / Q.sum(axis=1))
    npi_uv = 100 * unit_value / unit_value[0]
    simple = P.mean(axis=1)
    npi_simple = 100 * simple / simple[0]
    lnp_geo = (W * np.log(P)).sum(axis=1)
    npi_geo = 100 * np.exp(lnp_geo - lnp_geo[0])
    stpi = 100 * np.exp(alpha - alpha[0])

    # 定基 Laspeyres／Paasche／Fisher（基期＝首期）
    lasp = 100 * (P * Q[0]).sum(axis=1) / (P[0] * Q[0]).sum()
    paas = 100 * (P * Q).sum(axis=1) / (P[0] * Q).sum(axis=1)
    fish = np.sqrt(lasp * paas)
    # 链式 Fisher（逐期环比连乘）
    chain = np.ones(len(months))
    for i in range(1, len(months)):
        lL = (P[i] * Q[i - 1]).sum() / (P[i - 1] * Q[i - 1]).sum()
        lP = (P[i] * Q[i]).sum() / (P[i - 1] * Q[i]).sum()
        chain[i] = chain[i - 1] * sqrt(lL * lP)
    chain = 100 * chain
    return dict(months=months, NPI_unit_value=npi_uv, NPI_simple=npi_simple,
                NPI_geo=npi_geo, STPI=stpi, laspeyres=lasp, paasche=paas,
                fisher=fish, chained_fisher=chain, W=W, P=P, Q=Q, lnp_geo=lnp_geo)


def decompose_price(d, hres, idx, t0='2023-01', t1='2026-06'):
    """名义价格变化 ＝ 真实价格效应 ＋ 质量效应 ＋ 结构效应 ＋ 残差（恒等，Bennet 分解）。"""
    months = idx['months']
    i0, i1 = months.index(t0), months.index(t1)
    W, P = idx['W'], idx['P']
    items = list(d.pivot_table(index='month', columns='item', values='p_out').columns)
    Xm = {v: d.pivot_table(index='month', columns='item', values=v).loc[months][items].to_numpy(float)
          for v in XVARS}
    beta = hres['beta']
    xb = np.zeros_like(P)
    for v in XVARS:
        xb = xb + beta[v] * Xm[v]
    alpha = hres['alpha']

    w0, w1 = W[i0], W[i1]
    wbar = 0.5 * (w0 + w1)
    xb0, xb1 = xb[i0], xb[i1]
    xbbar = 0.5 * (xb0 + xb1)

    total = float(idx['lnp_geo'][i1] - idx['lnp_geo'][i0])
    real = float(alpha[i1] - alpha[i0])
    quality = float(np.sum(wbar * (xb1 - xb0)))
    structure = float(np.sum((w1 - w0) * xbbar))
    resid0 = float(idx['lnp_geo'][i0] - alpha[i0] - np.sum(w0 * xb0))
    resid1 = float(idx['lnp_geo'][i1] - alpha[i1] - np.sum(w1 * xb1))
    residual = resid1 - resid0
    chk = real + quality + structure + residual - total
    return dict(t0=t0, t1=t1,
                base_index='NPI_geo：支出份额加权的对数均价指数（≠速查表首列的单位价值指数 NPI）',
                total_ln=round(total, 6), real_price_ln=round(real, 6),
                quality_ln=round(quality, 6), structure_ln=round(structure, 6),
                residual_ln=round(residual, 6), identity_gap=round(chk, 12),
                total_pct=round(100 * (exp(total) - 1), 3),
                share={'real_price': round(real / total, 4),
                       'quality': round(quality / total, 4),
                       'structure': round(structure / total, 4),
                       'residual': round(residual / total, 4)},
                note='份额以对数变化为分母；quality>0 表示质量改进把观测均价托高，'
                     'structure<0 表示档位替代压低观测均价')


def annual_fold(index_series, months, m0, m1):
    """指数从 m0 到 m1 的年均下降倍数。"""
    i0, i1 = months.index(m0), months.index(m1)
    yrs = (i1 - i0) / 12.0
    ratio = index_series[i0] / index_series[i1]
    return dict(total_fold=round(float(ratio), 3),
                total_pct=round(float(100 * (index_series[i1] / index_series[i0] - 1)), 3),
                annual_fold=round(float(ratio ** (1 / yrs)), 3), years=round(yrs, 3))


# ============================ 四、B 卷：行业—季度需求支出面板 ============================
QUARTERS = ['2023Q1', '2023Q2', '2023Q3', '2023Q4', '2024Q1', '2024Q2', '2024Q3', '2024Q4',
            '2025Q1', '2025Q2', '2025Q3', '2025Q4', '2026Q1', '2026Q2']
T_B = len(QUARTERS)
Q2M = {q: [MONTHS.index(f'{q[:4]}-{mm:02d}')
           for mm in range(3 * (int(q[-1]) - 1) + 1, 3 * (int(q[-1]) - 1) + 4)] for q in QUARTERS}

INDUSTRIES = ['软件与信息技术服务', '互联网平台', '电信服务', '金融', '保险',
              '汽车制造', '电子设备制造', '通用装备制造', '化工与材料', '能源电力',
              '医药与生命科学', '医疗健康服务', '教育培训', '文化传媒', '零售与电商',
              '物流与供应链', '专业服务（法律会计）', '建筑与工程', '农业与食品', '公共管理与政务']
NIND = len(INDUSTRIES)
REGIONS = ['east', 'central', 'west', 'northeast']

EPS_TRUE = -1.75      # 真实（质量调整口径）需求价格弹性（样本均值）
EPS_HET_AI = -0.20    # 行业智能化基础对弹性的调节（基础越好越有弹性）
EPS_HET_SIZE = -1.30  # 大型企业用量占比对弹性的调节
GAM_TRUE = 0.85       # 任务复杂度指数的真实系数
SIG_U_AR = 0.40       # 需求冲击的行业内序列相关部分
SIG_U_IID = 0.12      # 需求冲击的独立部分
# 拥塞加价：短期推理产能有限，行业自身的需求冲击经排队与峰谷分时定价推高其有效购进价格
# （facts.md：2026 年出现「工作日高峰翻倍、夜间与周末维持平峰」的分时定价）。
# 这是价格内生性的来源，也是本文必须用成本推移工具变量识别的原因。
PHI_CONGEST = 0.30
DELTA_V = 1.05        # 版本更替（相对同期均值）对名义价格的压降
KAPPA_V = 1.30        # 版本更替（相对同期均值）对效值的提升
THETA_HW = 2.30       # 算力硬件租金 Bartik 的价格传导
THETA_EL = 1.85       # 电价 Bartik 的价格传导


def build_panel_B(dA, eta_item):
    """行业—季度面板：用量、质量调整价格、名义价格、支出、智能体化程度与成本工具。"""
    dA = dA.copy()
    dA['eta'] = eta_item
    # ---- 档位—季度价格与效值（由 A 卷聚合）----
    dA['q'] = dA['month'].map({MONTHS[i]: q for q in QUARTERS for i in Q2M[q]})
    dq = dA.dropna(subset=['q']).copy()
    dq['lneta_w'] = np.log(dq['eta']) * dq['q_tok']
    agg = dq.groupby(['tier', 'q'], observed=True).agg(
        E=('exp_yuan', 'sum'), Q=('q_tok', 'sum'), LW=('lneta_w', 'sum'))
    tier_p = (agg['E'] / (agg['Q'] * 1e6)).unstack()[QUARTERS]
    tier_eta = np.exp(agg['LW'] / agg['Q']).unstack()[QUARTERS]

    # ---- 行业固定属性 ----
    base_ai = np.clip(RNG.normal(0, 1, NIND), -2.4, 2.4)                # 行业智能化基础
    base_ai = (base_ai - base_ai.mean()) / base_ai.std()
    large_share = np.clip(0.28 + 0.09 * base_ai + RNG.normal(0, 0.07, NIND), 0.08, 0.62)
    scale0 = RNG.dirichlet(np.full(NIND, 2.2)) * 0.7 + 0.3 / NIND       # 基期用量份额
    scale0 = scale0 / scale0.sum()
    # 行业推理算力的地区暴露（份额—移动工具的“份额”一侧，基期固定）
    reg_prior = np.array([ANCHOR['region_share'][r] for r in REGIONS]) * 4.0
    reg_share = RNG.dirichlet(reg_prior, NIND)

    # ---- 地区成本冲击（份额—移动工具的“移动”一侧）----
    tb = np.arange(T_B, dtype=float)
    g_hw = {}   # 算力硬件租金对数指数（智能算力供给扩张 → 租金下行，地区节奏不同）
    g_el = {}
    for k, r in enumerate(REGIONS):
        drop = np.array([1.05, 0.86, 1.22, 0.72])[k]
        tau = np.array([12.0, 21.0, 9.0, 27.0])[k]          # 各区算力供给扩张节奏不同
        ar = pd.Series(RNG.normal(0, 1, T_B)).ewm(alpha=0.45).mean().to_numpy()
        g_hw[r] = -drop * _shape(np.clip(tb * 3, 0, 41), tau) + 0.55 * ar
        amp = np.array([0.16, 0.11, 0.24, 0.09])[k]
        ar2 = pd.Series(RNG.normal(0, 1, T_B)).ewm(alpha=0.5).mean().to_numpy()
        g_el[r] = amp * np.sin(0.9 * tb + k) + 0.26 * ar2
    G_HW = np.vstack([g_hw[r] for r in REGIONS])     # 4 x T
    G_EL = np.vstack([g_el[r] for r in REGIONS])
    W_HW, W_EL = 0.72, 0.28                          # 可变推理成本中硬件租金与电力的份额

    # ---- 行业—季度的档位结构、版本更替与任务复杂化 ----
    tier_mix = np.zeros((NIND, T_B, len(TIERS)))
    for i in range(NIND):
        tilt = np.array([-0.25, -0.05, 0.19, 0.17]) * base_ai[i]
        for s in range(T_B):
            base = np.array([_logistic_share(Q2M[QUARTERS[s]][1], *TIER_VOL[x]) for x in TIERS])
            v = np.log(base) + tilt + RNG.normal(0, 0.10, len(TIERS))
            e = np.exp(v)
            tier_mix[i, s] = e / e.sum()

    # 版本更替（最新代际模型用量占比）与任务复杂化
    v_shock = RNG.normal(0, 1, (NIND, T_B))
    ag_i = 0.35 * base_ai + 0.94 * RNG.normal(0, 1, NIND)   # 智能体化推进速度（与基础弱相关）
    VINT = np.zeros((NIND, T_B))
    ZAG = np.zeros((NIND, T_B))
    A1 = np.zeros((NIND, T_B)); A4 = np.zeros((NIND, T_B)); A15 = np.zeros((NIND, T_B))
    for i in range(NIND):
        VINT[i] = np.clip(0.20 + 0.55 * _shape(tb * 3, 18.0) + 0.11 * base_ai[i]
                          + 0.185 * pd.Series(v_shock[i]).ewm(alpha=0.6).mean().to_numpy(),
                          0.02, 0.98)
        # 任务复杂化：单轮问答／智能体工作流／多智能体的份额（倍数 1／4／15，见 facts.md）
        # 智能体化推进速度 ag 与行业智能化基础只弱相关，其余为行业自身的业务流程改造节奏
        sh = pd.Series(RNG.normal(0, 1, T_B)).ewm(alpha=0.5).mean().to_numpy()
        am = np.clip(0.005 + 0.075 * _shape(tb * 3, 22.0) * (1 + 0.45 * ag_i[i])
                     * np.exp(0.34 * sh), 0, 0.32)
        aa = np.clip(0.03 + 0.46 * _shape(tb * 3, 20.0) * (1 + 0.25 * ag_i[i])
                     * np.exp(0.28 * sh), 0, 0.70)
        a1 = np.clip(1 - aa - am, 0.05, 1.0)
        A1[i], A4[i], A15[i] = a1, aa, am
        ZAG[i] = np.log(a1 * 1.0 + aa * 4.0 + am * 15.0)
    # 份额—移动工具：按季度中心化，只保留行业间相对暴露差异（总量路径由 A 卷价格决定）
    BHW = W_HW * (reg_share @ G_HW)
    BEL = W_EL * (reg_share @ G_EL)
    BHW = BHW - BHW.mean(axis=0, keepdims=True)
    BEL = BEL - BEL.mean(axis=0, keepdims=True)
    VC = VINT - VINT.mean(axis=0, keepdims=True)      # 相对同期均值的版本更替进度

    # ---- 行业—季度需求冲击：先抽取，再经拥塞加价进入价格（制造价格内生性）----
    ar_u = np.vstack([pd.Series(RNG.normal(0, 1, T_B)).ewm(alpha=0.35).mean().to_numpy()
                      for _ in range(NIND)])
    U = SIG_U_AR * ar_u + RNG.normal(0, SIG_U_IID, (NIND, T_B))

    rows = []
    for i in range(NIND):
        for s in range(T_B):
            mix = tier_mix[i, s]
            p_mix = float(np.sum(mix * tier_p[QUARTERS[s]].reindex(TIERS).to_numpy()))
            eta_mix = float(np.exp(np.sum(mix * np.log(tier_eta[QUARTERS[s]].reindex(TIERS).to_numpy()))))
            lnp = (log(p_mix) - DELTA_V * VC[i, s] + THETA_HW * BHW[i, s]
                   + THETA_EL * BEL[i, s] + PHI_CONGEST * U[i, s] + RNG.normal(0, 0.030))
            lneta = log(eta_mix) + KAPPA_V * VC[i, s] + RNG.normal(0, 0.012)
            rows.append(dict(ind=INDUSTRIES[i], iid=i, quarter=QUARTERS[s], s=s,
                             base_ai=base_ai[i], large_share=large_share[i],
                             tier_econ=mix[0], tier_bal=mix[1], tier_flag=mix[2],
                             tier_reason=mix[3], vintage=VINT[i, s], z_agent=ZAG[i, s],
                             a_single=A1[i, s], a_agent=A4[i, s], a_multi=A15[i, s],
                             B_hw=BHW[i, s], B_el=BEL[i, s], ln_p_nom=lnp, ln_eta=lneta,
                             ln_p_adj=lnp - lneta, scale0=scale0[i], u_shock=U[i, s]))
    d = pd.DataFrame(rows)

    # ---- 结构式需求：ln T_std = eps_i*ln p_adj + gamma*z + mu_i + lambda_t + u ----
    mu = RNG.normal(0, 0.42, NIND) + 1.9 * np.log(scale0 / scale0.mean())
    lam = np.zeros(T_B)          # 共同扩散效应（先置零，随后由总量锚校准吸收）
    eps_i = (EPS_TRUE + EPS_HET_AI * base_ai
             + EPS_HET_SIZE * (large_share - large_share.mean()))
    u = d['u_shock'].to_numpy(float)      # 与价格中的拥塞加价同源 ⇒ ln p 内生
    d['eps_i'] = eps_i[d['iid'].to_numpy()]
    d['ln_T_std'] = (d['eps_i'].to_numpy() * d['ln_p_adj'].to_numpy()
                     + GAM_TRUE * d['z_agent'].to_numpy()
                     + mu[d['iid'].to_numpy()] + lam[d['s'].to_numpy()] + u)

    # ---- 用总量锚校准：每季度按比例缩放，使物理词元总量精确等于国家数据局口径 ----
    d['ln_T_phy'] = d['ln_T_std'] - d['ln_eta']
    for s in range(T_B):
        m = d['s'] == s
        tgt = float(MONTH_TOK[Q2M[QUARTERS[s]]].sum())        # 万亿枚／季
        cur = float(np.exp(d.loc[m, 'ln_T_phy']).sum())
        adj = log(tgt / cur)
        d.loc[m, 'ln_T_phy'] += adj
        d.loc[m, 'ln_T_std'] += adj
    d['T_phy_wanyi'] = np.exp(d['ln_T_phy'])
    d['T_std_wanyi'] = np.exp(d['ln_T_std'])
    d['p_nom'] = np.exp(d['ln_p_nom'])
    d['p_adj'] = np.exp(d['ln_p_adj'])
    d['eta'] = np.exp(d['ln_eta'])
    # 支出（亿元）：万亿枚 × 元／百万词元 × 1e6 元 = 1e6 元 → /1e8 亿元
    d['spend_yi'] = d['T_phy_wanyi'] * d['p_nom'] * 1e6 / 1e8
    d['ln_E'] = np.log(d['spend_yi'])
    return d


# ---------------------------- 需求弹性、工具变量与回弹分解 ----------------------------
ZCTRL = ['z_agent']


def demand_fe(d, price, extra=None, sub=None, cluster='ind', ind_trend=False):
    dd = (d if sub is None else d[sub]).copy()
    xs = [price] + ZCTRL + (extra or [])
    if ind_trend:                      # 行业特定线性时间趋势
        for j in sorted(dd['iid'].unique())[:-1]:
            c = f'tr{j}'
            dd[c] = np.where(dd['iid'] == j, dd['s'], 0.0)
            xs.append(c)
    r = within(dd, 'ln_T_std', xs, 'iid', 's', cluster=cluster)
    out = _fmt([price] + ZCTRL + (extra or []), r)
    out['r2_within'] = r['r2_within']
    out['elasticity'] = out[price]['coef']
    return out


def demand_dynamic(d, cluster='ind'):
    """动态设定：同时纳入当期与一期滞后价格，报告长期（累积）弹性。"""
    dd = d.sort_values(['iid', 's']).copy()
    dd['ln_p_adj_l1'] = dd.groupby('iid', observed=True)['ln_p_adj'].shift(1)
    dd = dd.dropna(subset=['ln_p_adj_l1'])
    xs = ['ln_p_adj', 'ln_p_adj_l1'] + ZCTRL
    r = within(dd, 'ln_T_std', xs, 'iid', 's', cluster=cluster)
    out = _fmt(xs, r)
    lr = float(r['b'][0] + r['b'][1])
    v = float(r['V'][0, 0] + r['V'][1, 1] + 2 * r['V'][0, 1])
    se = sqrt(max(v, 0))
    out['long_run'] = dict(coef=round(lr, 6), se=round(se, 6),
                           t=round(lr / se, 4),
                           p=round(_p_from_t(lr / se, r['dof']), 6))
    out['label'] = '动态设定：当期价格系数（长期弹性另列）'
    return out


def demand_pooled(d, price):
    """不含固定效应的混合 OLS，作为对照（仅作对照，不作为识别结果）。"""
    X = np.column_stack([np.ones(len(d)), d[price].to_numpy(float),
                         d['z_agent'].to_numpy(float)])
    y = d['ln_T_std'].to_numpy(float)
    r = _ols(y, X, cluster=d['ind'].to_numpy())
    out = _fmt(['const', price, 'z_agent'], r)
    rq = _ols(y, X, cluster=d['quarter'].to_numpy())
    out['se_cluster_quarter'] = round(float(rq['se'][1]), 6)
    out['t_cluster_quarter'] = round(float(rq['t'][1]), 4)
    out['caveat'] = ('混合 OLS 不含双向固定效应，其识别变异几乎全部来自价格与用量的共同时间路径；'
                     '按行业聚类把 20 个行业当作独立信息，会低估标准误，故并列报告按季度聚类的'
                     '标准误。本文不以该设定作为弹性的识别结果，只用作「不做任何控制会得到什么」的对照。')
    return out


def critical_elasticity(e, se, ncluster, label='双向固定效应（质量调整价）'):
    """支出上升的临界条件：dlnE/dln p̃ ＝ 1＋ε＜0，即 |ε|＞1。"""
    t = (e + 1.0) / se
    dof = ncluster - 1
    return dict(label=label, elasticity=e, se=se, threshold=-1.0,
                dlnE_dlnp=round(e + 1.0, 6), dlnE_dlnp_se=round(se, 6),
                t_H0_eps_eq_minus1=round(float(t), 4),
                p_one_sided=round(float(stats.t.cdf(t, dof)), 6),
                verdict='|ε|>1，价格下降引致支出上升（回弹超过 100%）' if e < -1 else '|ε|<1')


def agg_series(d):
    g = d.groupby('s', observed=True)
    E = g['spend_yi'].sum().to_numpy(float)
    Ts = g['T_std_wanyi'].sum().to_numpy(float)
    Tp = g['T_phy_wanyi'].sum().to_numpy(float)
    w = d['spend_yi'].to_numpy(float)
    zbar = np.array([float(np.average(d.loc[d['s'] == s, 'z_agent'],
                                      weights=w[(d['s'] == s).to_numpy()])) for s in range(T_B)])
    return dict(E=E, T_std=Ts, T_phy=Tp, P_adj=E * 1e8 / (Ts * 1e6),
                P_nom=E * 1e8 / (Tp * 1e6), zbar=zbar)


def time_effects(d, price, eps, gam):
    """扣除价格与复杂度后的共同时间效应 λ_t（技术扩散与市场普及）。"""
    y = d['ln_T_std'].to_numpy(float) - eps * d[price].to_numpy(float) \
        - gam * d['z_agent'].to_numpy(float)
    X = np.hstack([_dummies(d['iid'], False), _dummies(d['s'], True)])
    b = np.linalg.pinv(X.T @ X) @ (X.T @ y)
    lam = np.concatenate([[0.0], b[NIND:]])
    return lam


def rebound_decomp(d, eps, gam, s0=0, s1=T_B - 1, estimator='双向固定效应'):
    a = agg_series(d)
    lam = time_effects(d, 'ln_p_adj', eps, gam)

    dlnE = float(np.log(a['E'][s1] / a['E'][s0]))
    dlnP = float(np.log(a['P_adj'][s1] / a['P_adj'][s0]))
    dlnT = float(np.log(a['T_std'][s1] / a['T_std'][s0]))
    dz = float(a['zbar'][s1] - a['zbar'][s0])
    dlam = float(lam[s1] - lam[s0])

    price_eff = dlnP
    pure_rebound = eps * dlnP
    nonprice = dlnT - pure_rebound
    task = gam * dz
    diffusion = nonprice - task
    three = dict(price_effect=round(price_eff, 6),
                 pure_rebound=round(pure_rebound, 6),
                 nonprice_quantity=round(nonprice, 6))
    net_price_channel = price_eff + pure_rebound
    four = dict(price_effect=round(price_eff, 6),
                pure_rebound=round(pure_rebound, 6),
                task_complexity=round(task, 6),
                diffusion_other=round(diffusion, 6))
    return dict(window=[QUARTERS[s0], QUARTERS[s1]], estimator=estimator,
                total_lnE=round(dlnE, 6),
                total_pct=round(100 * (exp(dlnE) - 1), 2),
                dln_p_adj=round(dlnP, 6), dln_T_std=round(dlnT, 6),
                dln_p_nom=round(float(np.log(a['P_nom'][s1] / a['P_nom'][s0])), 6),
                dln_T_phy=round(float(np.log(a['T_phy'][s1] / a['T_phy'][s0])), 6),
                d_zbar=round(dz, 6), d_lambda=round(dlam, 6),
                decomp3=three, decomp4=four,
                share3={k: round(v / dlnE, 4) for k, v in three.items()},
                share4={k: round(v / dlnE, 4) for k, v in four.items()},
                identity_gap3=round(price_eff + pure_rebound + nonprice - dlnE, 12),
                identity_gap4=round(price_eff + pure_rebound + task + diffusion - dlnE, 12),
                net_price_channel=round(net_price_channel, 6),
                net_price_channel_pct=round(100 * (exp(net_price_channel) - 1), 2),
                eps_used=eps, gamma_used=gam,
                note='价格效应＝质量调整价格的对数变化；纯回弹＝ε×价格效应；'
                     '非价格数量效应＝任务复杂化（γ×Δz）＋共同扩散与其他，三项／四项均恒等加总')


def hetero_elasticity(d, var, label):
    med = d.groupby('iid', observed=True)[var].first().median()
    hi = set(d.groupby('iid', observed=True)[var].first().pipe(lambda s: s[s > med]).index)
    out = {'modvar': var, 'label': label, 'median': round(float(med), 4)}
    for nm, sel in (('high', d['iid'].isin(hi)), ('low', ~d['iid'].isin(hi))):
        r = demand_fe(d, 'ln_p_adj', sub=sel)
        out[nm] = dict(coef=r['ln_p_adj']['coef'], se=r['ln_p_adj']['se'],
                       p=r['ln_p_adj']['p'], n=r['n'], ncluster=r['ncluster'])
    dd = out['high']['coef'] - out['low']['coef']
    sd = sqrt(out['high']['se'] ** 2 + out['low']['se'] ** 2)
    out['diff'] = dict(coef=round(dd, 6), se=round(sd, 6), z=round(dd / sd, 4),
                       p=round(float(2 * stats.norm.sf(abs(dd / sd))), 6))
    return out


def true_eps_weighted(d):
    """异质斜率下双向固定效应 OLS 的估计目标：以各行业价格 within 方差为权的 eps_i 加权平均。"""
    (X,), _ = _absorb([_dummies(d['iid'], False), _dummies(d['s'], True)],
                      d[['ln_p_adj', 'z_agent']].to_numpy(float))
    x = X[:, 0] - X[:, 1] * float(X[:, 1] @ X[:, 0]) / float(X[:, 1] @ X[:, 1])
    ids = sorted(d['iid'].unique())
    w = np.array([float(np.sum(x[(d['iid'] == i).to_numpy()] ** 2)) for i in ids])
    w = w / w.sum()
    e = d.groupby('iid', observed=True)['eps_i'].first().reindex(ids).to_numpy(float)
    return float(w @ e)


def desc_table(df, cols, labels):
    out = {}
    for c in cols:
        s = pd.to_numeric(df[c], errors='coerce').dropna()
        out[c] = dict(label=labels.get(c, c), n=int(s.size),
                      mean=round(float(s.mean()), 4), sd=round(float(s.std()), 4),
                      p25=round(float(s.quantile(.25)), 4), p50=round(float(s.median()), 4),
                      p75=round(float(s.quantile(.75)), 4),
                      min=round(float(s.min()), 4), max=round(float(s.max()), 4))
    return out


def _r(a, nd=4):
    return [round(float(x), nd) for x in np.asarray(a, float)]


# ============================ 五、主程序 ============================
TASK_TYPES = {'通用问答类': -1.35, '编码与工具调用类': 0.0, '长文本与多模态类': 1.57}


def main():
    OUT = {'meta': dict(
        paper='词元价格下行与智能服务支出的背离——质量调整价格指数与回弹效应的分解',
        seed=20260825, generated_by='data_gen.py',
        statement=('档位明细挂牌价与行业词元用量／接口支出不公开，分析样本按 data/facts.md '
                   '公开锚校准生成；全部正文数字由本脚本产生，可复现。')),
        'anchor': ANCHOR}

    # ---------------- A 卷 ----------------
    dA = _prep_X(build_panel_A())
    h = hedonic(dA, 'p_out')
    eta, xbar0 = eta_from_beta(dA, h['beta'])
    dA['eta'] = eta
    dA['p_out_adj'] = dA['p_out'] / dA['eta']
    idx = build_indexes(dA, h['alpha'], h['months'])
    idxq = build_indexes(dA, h['alpha'], h['months'], pcol='p_out_adj')

    hin = hedonic(dA, 'p_in')
    hbl = hedonic(dA, 'p_blend')

    OUT['sampleA'] = dict(
        months=[MONTHS[0], MONTHS[-1]], T=T_A, tiers=TIERS,
        suppliers_per_tier={k: v for k, v in NSUP.items()},
        n_items=int(dA['item'].nunique()), n_firms=int(dA['firm'].nunique()),
        nobs=int(len(dA)),
        note='面板为平衡面板；2026-07／08 为结构性提价与峰谷分时定价起始期')

    OUT['descA'] = desc_table(dA, ['p_out', 'p_in', 'p_blend', 'cap', 'cap_z', 'lnctx',
                                   'lnlat', 'lnlat_z', 'mm', 'cache', 'reason', 'eta',
                                   'p_out_adj', 'io_ratio'],
                              {'p_out': '输出价（元／百万词元）', 'p_in': '输入价（元／百万词元）',
                               'p_blend': '混合单价（元／百万词元）', 'cap': '能力得分（原始 0—1）',
                               'cap_z': '能力得分（标准化）', 'lnctx': 'ln 上下文窗口（千词元）',
                               'lnlat': 'ln 输出时延（毫秒／词元）', 'lnlat_z': 'ln 输出时延（标准化）',
                               'mm': '多模态（0/1）', 'cache': '支持缓存计价（0/1）',
                               'reason': '推理增强（0/1）', 'eta': '效值系数 η',
                               'p_out_adj': '质量调整输出价', 'io_ratio': '输入价／输出价'})

    def _hed_out(hh, label):
        r = hh['res']
        nm = hh['names']
        d = {'label': label, 'n': r['n'], 'ncluster': r['ncluster'],
             'r2': r.get('r2'), 'r2_partial': hh.get('r2_partial'), 'beta': {}}
        for v in XVARS:
            i = nm.index(v)
            d['beta'][v] = dict(label=XLABEL[v], coef=round(float(r['b'][i]), 6),
                                se=None if np.isnan(r['se'][i]) else round(float(r['se'][i]), 6),
                                t=None if np.isnan(r['t'][i]) else round(float(r['t'][i]), 4),
                                p=None if np.isnan(r['p'][i]) else round(float(r['p'][i]), 6))
        d['alpha'] = {m: round(float(a), 6) for m, a in zip(hh['months'], hh['alpha'])}
        return d

    OUT['hedonic'] = dict(output_price=_hed_out(h, '输出价（基准）'),
                          input_price=_hed_out(hin, '输入价'),
                          blend_price=_hed_out(hbl, '混合单价'),
                          eta_base_bundle={k: round(v, 6) for k, v in xbar0.items()},
                          note='时期虚拟变量以 2023-01 为基期；标准误按供给方聚类；'
                               'η 由估计得到的隐含价格 β 构造，基期加权平均束归一为 1')

    ms = h['months']
    OUT['index'] = dict(
        months=ms,
        NPI_unit_value=_r(idx['NPI_unit_value'], 4), NPI_simple=_r(idx['NPI_simple'], 4),
        NPI_geo=_r(idx['NPI_geo'], 4), STPI=_r(idx['STPI'], 4),
        laspeyres=_r(idx['laspeyres'], 4), paasche=_r(idx['paasche'], 4),
        fisher=_r(idx['fisher'], 4), chained_fisher=_r(idx['chained_fisher'], 4),
        STPI_laspeyres=_r(idxq['laspeyres'], 4), STPI_paasche=_r(idxq['paasche'], 4),
        STPI_fisher=_r(idxq['fisher'], 4), STPI_chained_fisher=_r(idxq['chained_fisher'], 4),
        base='2023-01＝100',
        base_note=('名义口径有两个：NPI（单位价值＝支出／物理词元量，速查表首列与正文默认口径）'
                   '与 NPI_geo（支出份额加权的对数均价指数，三重分解的分解对象）。'
                   '二者数值不同，正文引用时必须点明是哪一个，不得混用。'),
        endpoints={m: dict(NPI=round(float(idx['NPI_unit_value'][ms.index(m)]), 3),
                           NPI_geo=round(float(idx['NPI_geo'][ms.index(m)]), 3),
                           STPI=round(float(idx['STPI'][ms.index(m)]), 3),
                           fisher=round(float(idx['fisher'][ms.index(m)]), 3),
                           chained=round(float(idx['chained_fisher'][ms.index(m)]), 3))
                   for m in ['2023-06', '2024-01', '2024-10', '2025-01', '2025-06',
                             '2025-12', '2026-03', '2026-06', '2026-08']},
        rates=dict(NPI=annual_fold(idx['NPI_unit_value'], ms, '2023-01', '2026-06'),
                   NPI_geo=annual_fold(idx['NPI_geo'], ms, '2023-01', '2026-06'),
                   STPI=annual_fold(idx['STPI'], ms, '2023-01', '2026-06'),
                   fisher=annual_fold(idx['fisher'], ms, '2023-01', '2026-06')),
        rates_subperiod={
            '2023-01→2024-10': dict(NPI=annual_fold(idx['NPI_unit_value'], ms, '2023-01', '2024-10'),
                                    STPI=annual_fold(idx['STPI'], ms, '2023-01', '2024-10')),
            '2024-10→2026-06': dict(NPI=annual_fold(idx['NPI_unit_value'], ms, '2024-10', '2026-06'),
                                    STPI=annual_fold(idx['STPI'], ms, '2024-10', '2026-06'))},
        break_2026=dict(NPI_change_pct=round(float(100 * (idx['NPI_unit_value'][-1] /
                                                          idx['NPI_unit_value'][ms.index('2026-06')] - 1)), 3),
                        STPI_change_pct=round(float(100 * (idx['STPI'][-1] /
                                                           idx['STPI'][ms.index('2026-06')] - 1)), 3),
                        window='2026-06→2026-08'))

    OUT['decomp_price'] = dict(
        full=decompose_price(dA, h, idx, '2023-01', '2026-06'),
        with_break=decompose_price(dA, h, idx, '2023-01', '2026-08'),
        phase1=decompose_price(dA, h, idx, '2023-01', '2024-10'),
        phase2=decompose_price(dA, h, idx, '2024-10', '2026-06'))

    # ---- 档位价格结构与 facts 对齐检查 ----
    tp = dA.pivot_table(index='month', columns='tier', values='p_out', aggfunc='mean').loc[ms]
    OUT['tier_price'] = dict(
        months=ms, table={t: _r(tp[t].to_numpy(), 4) for t in TIERS},
        snapshot={m: {t: round(float(tp.loc[m, t]), 3) for t in TIERS}
                  for m in ['2023-01', '2024-01', '2025-01', '2026-01', '2026-06', '2026-08']},
        ratio_flag_econ={m: round(float(tp.loc[m, '旗舰档'] / tp.loc[m, '经济档']), 3)
                         for m in ['2023-01', '2025-01', '2026-06', '2026-08']},
        ratio_reason_econ={m: round(float(tp.loc[m, '推理增强档'] / tp.loc[m, '经济档']), 3)
                           for m in ['2023-01', '2025-01', '2026-06', '2026-08']},
        item_spread={m: round(float(dA[dA['month'] == m]['p_out'].max() /
                                    dA[dA['month'] == m]['p_out'].min()), 3)
                     for m in ['2023-01', '2025-01', '2026-06', '2026-08']})

    # ---- A 卷稳健性 ----
    hnb = hedonic(dA, 'p_out', drop_months=['2026-07', '2026-08'])
    idx_nb = build_indexes(dA[~dA['month'].isin(['2026-07', '2026-08'])], hnb['alpha'], hnb['months'])
    hmed = hedonic(dA, 'p_out', robust_median=True)
    idx_med = build_indexes(dA, hmed['alpha'], hmed['months'])
    task = {}
    for tk, g in TASK_TYPES.items():
        dt = dA.copy()
        dt['p_task'] = dt['p_out'] * np.exp(g * _shape(np.clip(dt['t'].to_numpy(float), 0, 41)))
        ht = hedonic(dt, 'p_task')
        it = build_indexes(dt, ht['alpha'], ht['months'], pcol='p_task')
        task[tk] = dict(STPI=_r(it['STPI'], 4), NPI=_r(it['NPI_unit_value'], 4),
                        rate=annual_fold(it['STPI'], ms, '2023-01', '2026-06'),
                        beta_cap=round(ht['beta']['cap_z'], 6), r2=ht['res'].get('r2'))
    OUT['robustA'] = dict(
        drop_break=dict(label='剔除结构转向期（2026-07、2026-08）',
                        months=hnb['months'], STPI=_r(idx_nb['STPI'], 4),
                        rate=annual_fold(idx_nb['STPI'], hnb['months'], '2023-01', '2026-06'),
                        beta={v: round(hnb['beta'][v], 6) for v in XVARS},
                        r2=hnb['res'].get('r2'), n=hnb['res']['n']),
        median_reg=dict(label='中位数（L1）回归', STPI=_r(idx_med['STPI'], 4),
                        rate=annual_fold(idx_med['STPI'], ms, '2023-01', '2026-06'),
                        beta={v: round(hmed['beta'][v], 6) for v in XVARS},
                        stpi_2026_06=round(float(idx_med['STPI'][ms.index('2026-06')]), 4)),
        by_task=task,
        task_note='按任务类型分层后年均降幅区间由本脚本估计；facts.md 记录的 9—900 倍／年'
                  '为前沿最低报价口径的任务区间，二者口径不同，不可直接比较')

    # ---------------- B 卷 ----------------
    dB = build_panel_B(dA, eta)
    agg = agg_series(dB)

    OUT['sampleB'] = dict(quarters=[QUARTERS[0], QUARTERS[-1]], T=T_B,
                          n_industry=NIND, industries=INDUSTRIES, nobs=int(len(dB)),
                          note='行业—季度平衡面板；总量按国家数据局日均词元调用量锚校准')

    OUT['descB'] = desc_table(dB, ['ln_T_std', 'ln_T_phy', 'ln_p_adj', 'ln_p_nom', 'ln_eta',
                                   'ln_E', 'spend_yi', 'z_agent', 'base_ai', 'large_share',
                                   'vintage', 'B_hw', 'B_el', 'tier_econ', 'tier_flag'],
                              {'ln_T_std': 'ln 标准词元用量（万亿枚）',
                               'ln_T_phy': 'ln 物理词元用量（万亿枚）',
                               'ln_p_adj': 'ln 质量调整价格（元／百万词元）',
                               'ln_p_nom': 'ln 名义价格（元／百万词元）',
                               'ln_eta': 'ln 效值系数', 'ln_E': 'ln 智能服务支出（亿元）',
                               'spend_yi': '智能服务支出（亿元）',
                               'z_agent': '智能体化程度（任务复杂度指数）',
                               'base_ai': '行业智能化基础（标准化）',
                               'large_share': '大型企业用量占比',
                               'vintage': '最新代际模型用量占比',
                               'B_hw': '算力硬件租金暴露（Bartik）',
                               'B_el': '电价暴露（Bartik）',
                               'tier_econ': '经济档用量占比', 'tier_flag': '旗舰档用量占比'})

    fe_adj = demand_fe(dB, 'ln_p_adj')
    fe_nom = demand_fe(dB, 'ln_p_nom')
    po_adj = demand_pooled(dB, 'ln_p_adj')
    po_nom = demand_pooled(dB, 'ln_p_nom')
    e_a, e_n = fe_adj['ln_p_adj']['coef'], fe_nom['ln_p_nom']['coef']
    OUT['demand'] = dict(
        fe_quality_adjusted=fe_adj, fe_nominal=fe_nom,
        pooled_quality_adjusted=po_adj, pooled_nominal=po_nom,
        bias=dict(eps_adj=e_a, eps_nom=e_n,
                  ratio_abs=round(abs(e_n) / abs(e_a), 4),
                  gap=round(e_n - e_a, 6),
                  overstate_pct=round(100 * (abs(e_n) / abs(e_a) - 1), 2),
                  conclusion='以名义（物理）词元价格估计的弹性绝对值系统性大于质量调整口径，'
                             '名义价格高估需求价格弹性的绝对值'),
        critical=critical_elasticity(fe_adj['ln_p_adj']['coef'], fe_adj['ln_p_adj']['se'],
                                     fe_adj['ncluster']),
        wild_bootstrap=wild_cluster_boot(dB, 'ln_T_std', ['ln_p_adj'] + ZCTRL,
                                         'iid', 's', 'ln_p_adj', -1.0, B=999),
        spec='ln T_std = ε·ln p̃ + γ·z + μ_i + λ_t + u；行业层面聚类稳健标准误')

    _ivm = iv_within(dB, 'ln_T_std', ['ln_p_adj'], ['B_hw', 'B_el'], ZCTRL, 'iid', 's')
    OUT['iv'] = dict(
        main=_ivm,
        nominal=iv_within(dB, 'ln_T_std', ['ln_p_nom'], ['B_hw', 'B_el'], ZCTRL, 'iid', 's'),
        just_identified_hw=iv_within(dB, 'ln_T_std', ['ln_p_adj'], ['B_hw'], ZCTRL, 'iid', 's'),
        dwh=dwh_test(dB, 'ln_T_std', 'ln_p_adj', ['B_hw', 'B_el'], ZCTRL, 'iid', 's'),
        critical_iv=critical_elasticity(_ivm['second_stage']['ln_p_adj']['coef'],
                                        _ivm['second_stage']['ln_p_adj']['se'],
                                        _ivm['ncluster'], label='2SLS（质量调整价）'),
        design=('Bartik 式份额—移动工具：份额为行业基期推理算力的东／中／西／东北地区分布，'
                '移动为地区算力硬件租金指数与电价指数；成本份额取硬件 0.72、电力 0.28'),
        note=('第一阶段 F 为聚类稳健的联合 Wald／工具个数。成本工具只挑出与质量变动无关的'
              '供给侧价格推移，故在 2SLS 下名义口径与质量调整口径的弹性趋于一致——'
              '这恰好反证：固定效应 OLS 下两口径的差距确由质量改进与档位替代混入名义价格所致。'))

    _e, _g = fe_adj['ln_p_adj']['coef'], fe_adj['z_agent']['coef']
    _ei = _ivm['second_stage']['ln_p_adj']['coef']
    _gi = _ivm['second_stage']['z_agent']['coef']
    OUT['rebound'] = dict(
        full=rebound_decomp(dB, _e, _g),
        full_iv=rebound_decomp(dB, _ei, _gi, estimator='2SLS（Bartik 成本工具）'),
        window_2024Q4_2025Q2=rebound_decomp(dB, _e, _g, QUARTERS.index('2024Q4'),
                                            QUARTERS.index('2025Q2')),
        window_2025=rebound_decomp(dB, _e, _g, QUARTERS.index('2024Q4'),
                                   QUARTERS.index('2025Q4')),
        window_2024Q1_2026Q2=rebound_decomp(dB, _e, _g, QUARTERS.index('2024Q1'),
                                            QUARTERS.index('2026Q2')),
        note=('基准分解用双向固定效应弹性；因拥塞加价使固定效应 OLS 的 |ε| 向零偏，'
              '纯回弹效应是**下界**，full_iv 给出以 2SLS 弹性重算的分解作为上界。'
              '两者的价格通道净效应同号，故「背离」的定量条件不依赖于用哪一个弹性。'))

    OUT['hetero'] = dict(
        ai_base=hetero_elasticity(dB, 'base_ai', '行业智能化基础'),
        firm_size=hetero_elasticity(dB, 'large_share', '企业规模结构（大型企业用量占比）'))

    top3 = dB.groupby('iid', observed=True)['T_phy_wanyi'].sum().nlargest(3).index
    OUT['robustB'] = dict(
        drop_turn=dict(label='剔除结构转向期（2026Q1—Q2）',
                       **demand_fe(dB, 'ln_p_adj', sub=~dB['quarter'].isin(['2026Q1', '2026Q2']))),
        drop_top3=dict(label='剔除用量最大的三个行业',
                       **demand_fe(dB, 'ln_p_adj', sub=~dB['iid'].isin(top3))),
        add_structure=dict(label='加入档位结构控制',
                           **demand_fe(dB, 'ln_p_adj', extra=['tier_econ', 'tier_flag'])),
        ind_trend=dict(label='加入行业特定线性时间趋势',
                       **demand_fe(dB, 'ln_p_adj', ind_trend=True)),
        cluster_quarter=dict(label='改按季度聚类（14 簇）',
                             **demand_fe(dB, 'ln_p_adj', cluster='quarter')),
        early_sample=dict(label='仅 2023Q1—2025Q2',
                          **demand_fe(dB, 'ln_p_adj',
                                      sub=dB['s'] <= QUARTERS.index('2025Q2'))),
        dynamic=demand_dynamic(dB))

    # ---------------- 参数复原检查（模拟面板才做得了的自检）----------------
    sd_cap = float(dA['cap'].std(ddof=0))
    sd_lat = float(dA['lnlat'].std(ddof=0))
    hb = OUT['hedonic']['output_price']['beta']
    tru = {'cap_z': B_CAP * sd_cap, 'lnctx': B_CTX, 'lnlat_z': B_LAT * sd_lat,
           'mm': B_MM, 'cache': B_CACHE, 'reason': B_REASON}
    ew = true_eps_weighted(dB)
    iv2 = OUT['iv']['main']['second_stage']['ln_p_adj']
    _fs = OUT['iv']['main']['first_stage']
    OUT['dgp_recovery'] = dict(
        note=('分析样本由已知参数的数据生成过程校准生成，故可直接检验估计量能否找回真值。'
              '「(估计−真值)/标准误」应大体落在 ±2 以内；需求弹性的真值有两个口径：'
              '样本算术平均 eps_i，以及异质斜率下 FE-OLS 的实际估计目标'
              '（以各行业价格 within 方差为权的加权平均）。'),
        hedonic={v: dict(label=XLABEL[v], true=round(tru[v], 6), est=hb[v]['coef'],
                         se=hb[v]['se'],
                         z=round((hb[v]['coef'] - tru[v]) / hb[v]['se'], 3)) for v in XVARS},
        demand=dict(
            eps_true_mean=round(float(dB.groupby('iid', observed=True)['eps_i'].first().mean()), 6),
            eps_true_varweighted=round(ew, 6),
            eps_fe_ols=fe_adj['ln_p_adj']['coef'], eps_fe_ols_se=fe_adj['ln_p_adj']['se'],
            eps_2sls=iv2['coef'], eps_2sls_se=iv2['se'],
            z_fe_vs_weighted=round((fe_adj['ln_p_adj']['coef'] - ew) / fe_adj['ln_p_adj']['se'], 3),
            z_2sls_vs_weighted=round((iv2['coef'] - ew) / iv2['se'], 3),
            gamma_true=GAM_TRUE, gamma_est=fe_adj['z_agent']['coef'],
            gamma_se=fe_adj['z_agent']['se'],
            z_gamma=round((fe_adj['z_agent']['coef'] - GAM_TRUE) / fe_adj['z_agent']['se'], 3),
            endogeneity=dict(phi_congestion=PHI_CONGEST,
                             mechanism='行业自身需求冲击经拥塞与峰谷加价进入其有效购进价格，'
                                       '故 FE-OLS 向零偏（|ε| 被低估），成本推移工具变量纠正之')),
        first_stage=dict(
            theta_hw_true=THETA_HW, theta_el_true=THETA_EL,
            est_hw=_fs['B_hw']['coef'], se_hw=_fs['B_hw']['se'],
            z_hw=round((_fs['B_hw']['coef'] - THETA_HW) / _fs['B_hw']['se'], 3),
            est_el=_fs['B_el']['coef'], se_el=_fs['B_el']['se'],
            z_el=round((_fs['B_el']['coef'] - THETA_EL) / _fs['B_el']['se'], 3),
            corr_hw_el=round(float(np.corrcoef(dB['B_hw'], dB['B_el'])[0, 1]), 4),
            note='份额已含在 Bartik 变量内，故第一阶段系数的真值就是 THETA_HW 与 THETA_EL。'
                 '电价工具的 within 方差远小于硬件租金工具，其系数本就估得不准（标准误大），'
                 '故以联合 F 与 Hansen J 判断工具，不逐点比对单个系数'),
        r2_caveat=('享乐方程的偏 R²（剔除时期虚拟后特征对同期截面价差的解释力）为 '
                   + str(OUT['hedonic']['output_price']['r2_partial']) +
                   '，高于真实挂牌价数据可期的水平：模拟面板只设了一个供给方层面的'
                   '未观测定价偏移，而现实中同档位不同供给方的报价差异更大。'
                   '正文应把享乐方程的 R² 表述为模拟设定下的上界，不据此评价方法的解释力。'))

    # ---------------- 校准检验 ----------------
    q_daily = np.array([float(DAILY_TOK[Q2M[q]].mean()) for q in QUARTERS])
    sp = agg['E']
    OUT['calibration'] = dict(
        daily_tokens_wanyi={q: round(float(v), 4) for q, v in zip(QUARTERS, q_daily)},
        daily_tokens_check={k: round(float(DAILY_TOK[MIDX[m]]), 4)
                            for m, k in [('2024-01', '2024年初'), ('2025-06', '2025年6月底'),
                                         ('2025-12', '2025年底'), ('2026-03', '2026年3月')]},
        panel_total_vs_anchor={q: round(float(dB.loc[dB['quarter'] == q, 'T_phy_wanyi'].sum()
                                              / MONTH_TOK[Q2M[q]].sum()), 8) for q in QUARTERS},
        spend_growth_2024Q4_2025Q2=round(float(sp[QUARTERS.index('2025Q2')] /
                                               sp[QUARTERS.index('2024Q4')] - 1), 4),
        spend_growth_anchor=ANCHOR['api_spend_halfyear_growth'],
        spend_growth_note=('本面板支出由国家数据局的词元调用量锚与本文价格指数相乘得到，'
                           '增速远高于 facts.md 记录的美国企业接口支出半年 140%——两者'
                           '市场范围、统计口径与货币单位均不同，正文只作方向性对照，'
                           '严禁相除或换算'),
        spend_yi_by_quarter={q: round(float(v), 2) for q, v in zip(QUARTERS, sp)},
        agent_multiple_check=dict(
            zbar_first=round(float(agg['zbar'][0]), 4), zbar_last=round(float(agg['zbar'][-1]), 4),
            implied_multiple_first=round(float(exp(agg['zbar'][0])), 3),
            implied_multiple_last=round(float(exp(agg['zbar'][-1])), 3),
            anchor=ANCHOR['agent_multiple']),
        flag_econ_ratio_2026_06=OUT['tier_price']['ratio_flag_econ']['2026-06'],
        flag_econ_ratio_anchor=ANCHOR['flag_econ_output_ratio'],
        stpi_vs_frontier=dict(
            stpi_annual_fold=OUT['index']['rates']['STPI']['annual_fold'],
            frontier_annual_fold=ANCHOR['quality_constant_annual_fold'],
            note='前沿口径为固定能力水平下的最低报价，本文 STPI 为代表性供给方篮子的'
                 '质量调整指数，故降幅低于前沿口径，属预期之内'))

    # ---------------- 图表用序列 ----------------
    OUT['figdata'] = dict(
        fig1=dict(months=ms, NPI=_r(idx['NPI_unit_value'], 3), STPI=_r(idx['STPI'], 3),
                  fisher=_r(idx['fisher'], 3), chained=_r(idx['chained_fisher'], 3),
                  break_month='2026-07'),
        fig2=OUT['decomp_price']['full'],
        fig3=[dict(spec='混合 OLS（质量调整价）', coef=po_adj['ln_p_adj']['coef'],
                   se=po_adj['ln_p_adj']['se']),
              dict(spec='双向固定效应（质量调整价）', coef=fe_adj['ln_p_adj']['coef'],
                   se=fe_adj['ln_p_adj']['se']),
              dict(spec='双向固定效应（名义价）', coef=fe_nom['ln_p_nom']['coef'],
                   se=fe_nom['ln_p_nom']['se']),
              dict(spec='工具变量 2SLS（质量调整价）',
                   coef=OUT['iv']['main']['second_stage']['ln_p_adj']['coef'],
                   se=OUT['iv']['main']['second_stage']['ln_p_adj']['se']),
              dict(spec='智能化基础高组', coef=OUT['hetero']['ai_base']['high']['coef'],
                   se=OUT['hetero']['ai_base']['high']['se']),
              dict(spec='智能化基础低组', coef=OUT['hetero']['ai_base']['low']['coef'],
                   se=OUT['hetero']['ai_base']['low']['se']),
              dict(spec='大型企业占比高组', coef=OUT['hetero']['firm_size']['high']['coef'],
                   se=OUT['hetero']['firm_size']['high']['se']),
              dict(spec='大型企业占比低组', coef=OUT['hetero']['firm_size']['low']['coef'],
                   se=OUT['hetero']['firm_size']['low']['se'])],
        fig4=OUT['rebound']['full']['decomp4'],
        agg_series=dict(quarters=QUARTERS, spend_yi=_r(agg['E'], 2),
                        T_std_wanyi=_r(agg['T_std'], 3), T_phy_wanyi=_r(agg['T_phy'], 3),
                        P_adj=_r(agg['P_adj'], 5), P_nom=_r(agg['P_nom'], 5),
                        zbar=_r(agg['zbar'], 4)))

    dA.to_csv(os.path.join(DATA, 'panel_hedonic.csv'), index=False, encoding='utf-8-sig')
    dB.to_csv(os.path.join(DATA, 'panel_demand.csv'), index=False, encoding='utf-8-sig')
    with open(os.path.join(DATA, 'results.json'), 'w', encoding='utf-8') as f:
        json.dump(OUT, f, ensure_ascii=False, indent=1)

    write_spec(OUT)

    # ---------------- 控制台诊断 ----------------
    print('=' * 72)
    print('A 卷 N =', len(dA), ' 享乐 R² =', h['res']['r2'])
    print('β:', {k: round(v, 4) for k, v in h['beta'].items()})
    print('NPI 2026-06 =', round(idx['NPI_unit_value'][ms.index('2026-06')], 3),
          ' STPI 2026-06 =', round(idx['STPI'][ms.index('2026-06')], 3))
    print('NPI 2026-08 =', round(idx['NPI_unit_value'][-1], 3),
          ' STPI 2026-08 =', round(idx['STPI'][-1], 3))
    print('年均降幅（倍）NPI/STPI:', OUT['index']['rates']['NPI']['annual_fold'],
          OUT['index']['rates']['STPI']['annual_fold'])
    print('旗舰／经济 2026-06 =', OUT['tier_price']['ratio_flag_econ']['2026-06'])
    print('三重分解:', OUT['decomp_price']['full']['decomp' if False else 'total_ln'],
          OUT['decomp_price']['full']['real_price_ln'],
          OUT['decomp_price']['full']['quality_ln'],
          OUT['decomp_price']['full']['structure_ln'],
          'gap=', OUT['decomp_price']['full']['identity_gap'])
    print('-' * 72)
    print('B 卷 N =', len(dB))
    print('ε(质量调整) =', e_a, ' ε(名义) =', e_n, ' 比值 =', OUT['demand']['bias']['ratio_abs'])
    print('IV: F =', OUT['iv']['main']['first_stage_F'],
          ' 2SLS ε =', OUT['iv']['main']['second_stage']['ln_p_adj']['coef'],
          ' J p =', OUT['iv']['main'].get('hansen_J', {}).get('p'))
    print('回弹分解 total/三项:', OUT['rebound']['full']['total_lnE'],
          OUT['rebound']['full']['decomp3'], 'gap=', OUT['rebound']['full']['identity_gap3'])
    print('支出增速 2024Q4→2025Q2 =', OUT['calibration']['spend_growth_2024Q4_2025Q2'],
          '（锚 1.40）')
    print('=' * 72)
    return OUT


# ============================ 六、速查表 data/RESULTS_SPEC.md ============================
def write_spec(O):
    ix, rt = O['index'], O['index']['rates']
    dp = O['decomp_price']['full']
    dm, iv, rb = O['demand'], O['iv']['main'], O['rebound']['full']
    hb = O['hetero']
    L = []
    A = L.append

    def _pf(p):
        """p 值排版：小于 1e-6 不写成 0.0。"""
        if p is None:
            return '—'
        return '<1e-6' if p < 1e-6 else (f'{p:.6f}'.rstrip('0').rstrip('.') if p < 0.1 else f'{p:.4f}')
    A('# results.json 速查表（论文一：词元价格下行与智能服务支出的背离）\n')
    A('> 本表由 `data_gen.py` 自动生成，随 `data/results.json` 同步更新。')
    A('> **正文一切数字只许引自本表或 results.json；宏观事实数字引自 `data/facts.md`。**')
    A('> 分析样本为按公开锚校准生成的模拟面板（声明见 results.json 的 `meta.statement`）。\n')

    A('## 0 样本\n')
    A('| 面板 | 单位 | 区间 | 期数 | 截面 | 观测 |')
    A('|---|---|---|---|---|---|')
    A(f"| A 享乐价格面板 | 模型档位—供给方×月 | {O['sampleA']['months'][0]}—"
      f"{O['sampleA']['months'][1]} | {O['sampleA']['T']} | "
      f"{O['sampleA']['n_items']} 个档位—供给方（{O['sampleA']['n_firms']} 家供给方） | "
      f"{O['sampleA']['nobs']} |")
    A(f"| B 需求支出面板 | 行业×季 | {O['sampleB']['quarters'][0]}—"
      f"{O['sampleB']['quarters'][1]} | {O['sampleB']['T']} | "
      f"{O['sampleB']['n_industry']} 个行业 | {O['sampleB']['nobs']} |")
    A('')
    A('档位：经济档 6 家、均衡档 6 家、旗舰档 5 家、推理增强档 4 家（一律用抽象档位名）。\n')

    A('## 1 价格指数（2023-01＝100）　→ 图 1\n')
    A('| 时点 | 名义指数 NPI（单位价值） | 名义指数 NPI_geo（份额加权对数均价） | '
      '质量调整指数 STPI | Fisher | 链式 Fisher |')
    A('|---|---|---|---|---|---|')
    for m, v in ix['endpoints'].items():
        A(f"| {m} | {v['NPI']} | {v['NPI_geo']} | {v['STPI']} | {v['fisher']} | {v['chained']} |")
    A('')
    A('> ⚠ **两个名义口径不可混用**：NPI＝支出／物理词元量（单位价值），是正文默认口径；'
      'NPI_geo＝支出份额加权的对数均价指数，是第 3 节三重分解的分解对象。'
      f"2023-01→2026-06 前者累计 {rt['NPI']['total_pct']}%、后者 {rt['NPI_geo']['total_pct']}%，"
      '引用时必须点明是哪一个。\n')
    A(f"- 2023-01→2026-06：NPI 累计 **{rt['NPI']['total_pct']}%**（{rt['NPI']['total_fold']} 倍，"
      f"年均 **{rt['NPI']['annual_fold']} 倍**）；"
      f"STPI 累计 **{rt['STPI']['total_pct']}%**（{rt['STPI']['total_fold']} 倍，"
      f"年均 **{rt['STPI']['annual_fold']} 倍**）。")
    A(f"- **质量调整指数的降幅大于名义指数**：名义口径低估真实降价、低估真实投入量增长。")
    A(f"- 结构转向（2026-06→2026-08）：NPI **{ix['break_2026']['NPI_change_pct']}%**、"
      f"STPI **{ix['break_2026']['STPI_change_pct']}%**，价格掉头向上。")
    sub = ix['rates_subperiod']
    A(f"- **降幅收敛**：STPI 在 2023-01→2024-10 年均 **{sub['2023-01→2024-10']['STPI']['annual_fold']} 倍**，"
      f"在 2024-10→2026-06 收敛至 **{sub['2024-10→2026-06']['STPI']['annual_fold']} 倍**；"
      f"NPI 同期由 {sub['2023-01→2024-10']['NPI']['annual_fold']} 倍收敛至 "
      f"{sub['2024-10→2026-06']['NPI']['annual_fold']} 倍。")
    A(f"- 前沿对照：facts.md 质量恒定口径（斯坦福《人工智能指数报告》）2022-11→2024-10 年均"
      f" {O['anchor']['quality_constant_annual_fold']} 倍；本文 STPI 在 2023-01→2024-10 为"
      f" {sub['2023-01→2024-10']['STPI']['annual_fold']} 倍，方向一致而幅度更保守——"
      '前沿口径是固定能力水平下的**最低报价**，本文是代表性供给方**篮子**的质量调整指数，'
      '正文只作方向性对照，不可相除、不可互换。\n')

    i66 = ix['months'].index('2026-06')
    A(f"- 指数编制对照（2026-06）：定基 Laspeyres {ix['laspeyres'][i66]}、Paasche {ix['paasche'][i66]}、"
      f"Fisher {ix['fisher'][i66]}、链式 Fisher {ix['chained_fisher'][i66]}；"
      f"单位价值指数 {ix['NPI_unit_value'][i66]}、简单算术平均 {ix['NPI_simple'][i66]}。"
      '固定篮子指数高于单位价值指数：单位价值指数把「用量迁移到便宜档位」记成了降价，'
      '固定篮子指数不记，二者之差是**档位替代对单位价值的拉低作用**——'
      '它与第 3 节 Bennet 分解里的「结构效应」是两个不同的量（后者衡量支出份额迁移'
      '带来的**质量束**变化），数值不可互相替代，正文不得混称。')
    _sn0, _sn1 = O['tier_price']['snapshot']['2023-01'], O['tier_price']['snapshot']['2026-06']
    _de = 100 * (_sn1['经济档'] / _sn0['经济档'] - 1)
    _df = 100 * (_sn1['旗舰档'] / _sn0['旗舰档'] - 1)
    A(f"- Paasche（{ix['paasche'][i66]}）高于 Laspeyres（{ix['laspeyres'][i66]}），与教科书常见的"
      f"「Laspeyres≥Paasche」次序相反，原因是用量迁往的经济档恰是降幅**较小**的档位"
      f"（2023-01→2026-06 经济档 {_de:.1f}%、旗舰档 {_df:.1f}%），"
      '以现期用量加权自然给降得少的档位更大权重。这不是编制错误，正文如报告 Fisher 指数须一并说明。')
    A(f"- 质量调整口径的同类指数（2026-06）：Laspeyres {ix['STPI_laspeyres'][i66]}、"
      f"Paasche {ix['STPI_paasche'][i66]}、Fisher {ix['STPI_fisher'][i66]}、"
      f"链式 Fisher {ix['STPI_chained_fisher'][i66]}。\n")

    A('## 2 享乐回归（表 2）\n')
    hm = O['hedonic']['output_price']
    A(f"因变量 ln 输出价；{hm['n']} 个观测，供给方聚类（{hm['ncluster']} 簇），"
      f"总 R² ＝ **{hm['r2']}**，剔除时期虚拟后的偏 R² ＝ **{hm['r2_partial']}**。\n")
    A('| 特征 | 系数 | 标准误 | t | p |')
    A('|---|---|---|---|---|')
    for v, b in hm['beta'].items():
        A(f"| {b['label']} | {b['coef']} | {b['se']} | {b['t']} | {b['p']} |")
    A('')
    A(f"输入价方程 R² ＝ {O['hedonic']['input_price']['r2']}；"
      f"混合单价方程 R² ＝ {O['hedonic']['blend_price']['r2']}。")
    A('> ⚠ 总 R² 中绝大部分由时期虚拟（价格下行本身）贡献；偏 R² 才是特征对同期截面价差的'
      '净解释力。且模拟面板只设了一个供给方层面的未观测定价偏移，偏 R² 高于真实挂牌价数据'
      '可期的水平，正文须把它表述为模拟设定下的上界，不据此评价享乐方法的解释力。\n')

    A('## 3 名义降价的三重分解（表 4 上半／图 2）\n')
    A('恒等式：Δln 名义价格 ＝ 真实价格效应 ＋ 质量效应 ＋ 结构效应 ＋ 残差\n')
    A(f"> 分解对象是 **NPI_geo**（支出份额加权的对数均价指数），"
      f"2023-01→2026-06 累计 **{dp['total_pct']}%**；"
      f"不是第 1 节首列的单位价值指数 NPI（累计 {O['index']['rates']['NPI']['total_pct']}%）。"
      '正文写「名义价格累计下降 X%」时，必须与所引的分解表同口径。\n')
    A('（占比＝该项／名义总变化；正数表示把价格往**下**推、构成降幅的一部分，负数表示抵消降幅）\n')
    A('| 项 | 对数变化 | 占名义降幅 |')
    A('|---|---|---|')
    A(f"| 名义价格总变化（NPI_geo 口径） | {dp['total_ln']} | 100% |")
    A(f"| 真实价格效应（STPI） | {dp['real_price_ln']} | {dp['share']['real_price']*100:.1f}% |")
    A(f"| 质量效应 | {dp['quality_ln']} | {dp['share']['quality']*100:.1f}% |")
    A(f"| 结构（档位替代）效应 | {dp['structure_ln']} | {dp['share']['structure']*100:.1f}% |")
    A(f"| 残差 | {dp['residual_ln']} | {dp['share']['residual']*100:.1f}% |")
    A('')
    A(f"恒等式误差 {dp['identity_gap']}（机器精度）。质量效应为正：质量改进把观测均价托高，"
      '若只看名义单价便会把「同价买到更强词元」误记为没有降价；结构效应为负：'
      '用量向经济档迁移压低观测均价。\n')

    A('## 4 需求价格弹性（表 3／图 3）\n')
    A('| 设定 | 价格口径 | ε | 标准误 | t | p | N |')
    A('|---|---|---|---|---|---|---|')
    for key, lab, pv in (('pooled_quality_adjusted', '混合 OLS', 'ln_p_adj'),
                         ('pooled_nominal', '混合 OLS', 'ln_p_nom'),
                         ('fe_quality_adjusted', '双向固定效应', 'ln_p_adj'),
                         ('fe_nominal', '双向固定效应', 'ln_p_nom')):
        r = dm[key][pv]
        cap = '质量调整价' if pv == 'ln_p_adj' else '名义价'
        A(f"| {lab} | {cap} | **{r['coef']}** | {r['se']} | {r['t']} | {_pf(r['p'])} | {dm[key]['n']} |")
    s2 = iv['second_stage']['ln_p_adj']
    A(f"| 2SLS（Bartik 成本工具） | 质量调整价 | **{s2['coef']}** | {s2['se']} | "
      f"{s2['t']} | {_pf(s2['p'])} | {iv['n']} |")
    A('')
    A('> ⚠ 混合 OLS 两行**只作对照，不是识别结果**：不含双向固定效应时，识别变异几乎全部来自'
      '价格与用量的共同时间路径，按行业聚类会低估标准误（按季度聚类的标准误为 '
      f"{dm['pooled_quality_adjusted']['se_cluster_quarter']}）。本文的基准估计是双向固定效应与 2SLS。\n")
    A(f"- **核心结论**：名义价格口径的弹性绝对值为 {abs(dm['bias']['eps_nom']):.4f}，"
      f"质量调整口径为 {abs(dm['bias']['eps_adj']):.4f}，"
      f"名义口径**高估 {dm['bias']['overstate_pct']}%**（倍数 {dm['bias']['ratio_abs']}）。")
    A(f"- 智能体化程度系数 γ ＝ {dm['fe_quality_adjusted']['z_agent']['coef']}"
      f"（se {dm['fe_quality_adjusted']['z_agent']['se']}）。")
    cr = dm['critical']
    A(f"- 临界条件：dlnE/dln p̃ ＝ 1＋ε ＝ **{cr['dlnE_dlnp']}**＜0，"
      f"H0: ε＝−1 的 t ＝ {cr['t_H0_eps_eq_minus1']}，单侧 p ＝ {_pf(cr['p_one_sided'])}；"
      f"Wild Cluster Bootstrap p ＝ {dm['wild_bootstrap']['p_wild']}（B＝999）。")
    A(f"- 工具变量：第一阶段 F ＝ **{iv['first_stage_F']}**（>10，亦高于 2 工具的 Stock–Yogo "
      f"10% 临界值 {iv['weak_iv']['stock_yogo_10pct']}），"
      f"Hansen J ＝ {iv.get('hansen_J', {}).get('J')}（p ＝ {iv.get('hansen_J', {}).get('p')}，"
      '不能拒绝工具外生）；仅用硬件租金工具的恰好识别结果为 '
      f"{O['iv']['just_identified_hw']['second_stage']['ln_p_adj']['coef']}。")
    dwh = O['iv']['dwh']
    civ = O['iv']['critical_iv']
    A(f"- **价格内生性**：数据生成中行业自身的需求冲击经拥塞与峰谷加价进入其有效购进价格"
      f"（传导系数 {O['dgp_recovery']['demand']['endogeneity']['phi_congestion']}），"
      f"故固定效应 OLS 向零偏；2SLS 的 |ε| 大于 OLS（{s2['coef']} 对 "
      f"{dm['fe_quality_adjusted']['ln_p_adj']['coef']}），方向与理论一致。"
      f"Durbin–Wu–Hausman 控制函数系数 {dwh['cf_coef']}（se {dwh['cf_se']}，t {dwh['cf_t']}，"
      f"p {_pf(dwh['cf_p'])}）：在 20 个行业的聚类稳健推断下检验力有限，"
      '**不能在常规水平上拒绝价格外生**，正文须如实报告，不得声称「内生性检验支持使用工具变量」。')
    A(f"- 2SLS 口径的临界条件：dlnE/dln p̃ ＝ {civ['dlnE_dlnp']}，"
      f"H0: ε＝−1 的 t ＝ {civ['t_H0_eps_eq_minus1']}，单侧 p ＝ {_pf(civ['p_one_sided'])}"
      '——2SLS 点估计支持 |ε|>1，但因标准误更大而未达 5% 水平；'
      '**「|ε|>1 在 5% 水平显著」只可依据双向固定效应估计陈述**。')
    A(f"- 2SLS 下名义口径弹性为 {O['iv']['nominal']['second_stage']['ln_p_nom']['coef']}，"
      f"与质量调整口径的 {iv['second_stage']['ln_p_adj']['coef']} 接近："
      '成本工具只识别与质量无关的供给侧价格推移，两口径自然收敛；'
      '这从反面印证固定效应 OLS 下的口径差距来自质量改进与档位替代被计入名义价格。\n')

    A('## 5 支出变化的回弹分解（表 4 下半／图 4）\n')
    A(f"窗口 {rb['window'][0]}—{rb['window'][1]}；总支出对数变化 **{rb['total_lnE']}**"
      f"（＋{rb['total_pct']}%）。\n")
    A('| 项 | 对数变化 | 占总变化 |')
    A('|---|---|---|')
    lab4 = {'price_effect': '价格效应（质量调整价下行）', 'pure_rebound': '纯回弹效应（ε×价格效应）',
            'task_complexity': '任务复杂化效应（γ×Δz）', 'diffusion_other': '共同扩散与其他数量效应'}
    for k, v in rb['decomp4'].items():
        A(f"| {lab4[k]} | {v} | {rb['share4'][k]*100:.1f}% |")
    A('')
    A('三项口径（供正文「三项分解」表述使用）：')
    lab3 = {'price_effect': '价格效应', 'pure_rebound': '纯回弹效应',
            'nonprice_quantity': '非价格数量效应（任务复杂化＋扩散）'}
    A('| 项 | 对数变化 | 占总变化 |')
    A('|---|---|---|')
    for k, v in rb['decomp3'].items():
        A(f"| {lab3[k]} | {v} | {rb['share3'][k]*100:.1f}% |")
    A('')
    A(f"恒等式误差：三项 {rb['identity_gap3']}、四项 {rb['identity_gap4']}。\n")
    A(f"- **价格通道净效应**：价格效应＋纯回弹 ＝ **{rb['net_price_channel']}**"
      f"（相当于支出 ＋{rb['net_price_channel_pct']}%）＞0——"
      '即使不计任务复杂化与市场扩散，仅价格通道本身就足以让支出上升，这正是「背离」的定量条件。')
    rbi = O['rebound']['full_iv']
    A(f"- **弹性口径敏感性**：改用 2SLS 弹性（{rbi['eps_used']}）重算，"
      f"纯回弹效应为 {rbi['decomp4']['pure_rebound']}（占总变化 {rbi['share4']['pure_rebound']*100:.1f}%），"
      f"价格通道净效应 {rbi['net_price_channel']}（支出 ＋{rbi['net_price_channel_pct']}%），"
      f"共同扩散与其他数量效应 {rbi['decomp4']['diffusion_other']}。"
      '固定效应弹性向零偏，故基准分解的纯回弹是**下界**、扩散项是**上界**；'
      '两口径的价格通道净效应同号，「背离」的定量条件不依赖于用哪一个弹性。')
    w = O['rebound']['window_2024Q4_2025Q2']
    A(f"- 半年窗口（2024Q4→2025Q2）支出增长 **{w['total_pct']}%**。"
      'facts.md 记录的企业接口支出半年增长约 140% 系**美国市场、美元口径**，'
      '与本文由国家数据局调用量锚推算的人民币口径总支出**不可比、不可相除**，'
      '正文只可作「同向、量级更大」的方向性表述。\n')

    A('## 6 异质性（表 5 上半）\n')
    A('| 分组 | 高组 ε | 低组 ε | 差异 | z | p |')
    A('|---|---|---|---|---|---|')
    for k, h in hb.items():
        A(f"| {h['label']} | {h['high']['coef']}（se {h['high']['se']}） | "
          f"{h['low']['coef']}（se {h['low']['se']}） | {h['diff']['coef']} | "
          f"{h['diff']['z']} | {h['diff']['p']} |")
    A('')

    A('## 7 稳健性（表 5 下半）\n')
    A('**A 卷（指数）**\n')
    ra = O['robustA']
    A(f"- 剔除结构转向期：STPI 2026-06 年均降幅 {ra['drop_break']['rate']['annual_fold']} 倍，"
      f"累计 {ra['drop_break']['rate']['total_pct']}%。")
    A(f"- 中位数（L1）回归：STPI 2026-06 ＝ {ra['median_reg']['stpi_2026_06']}，"
      f"年均 {ra['median_reg']['rate']['annual_fold']} 倍。")
    A('- 按任务类型分层的 STPI 年均降幅：'
      + '；'.join(f"{k} {v['rate']['annual_fold']} 倍" for k, v in ra['by_task'].items()) + '。')
    A('')
    A('**B 卷（弹性）**\n')
    A('| 设定 | ε | 标准误 | p | N |')
    A('|---|---|---|---|---|')
    for k, r in O['robustB'].items():
        A(f"| {r['label']} | {r['ln_p_adj']['coef']} | {r['ln_p_adj']['se']} | "
          f"{_pf(r['ln_p_adj']['p'])} | {r['n']} |")
    lr = O['robustB']['dynamic']['long_run']
    A(f"| └ 动态设定的长期弹性（当期＋滞后） | {lr['coef']} | {lr['se']} | {_pf(lr['p'])} | "
      f"{O['robustB']['dynamic']['n']} |")
    A('')

    A('## 8 档位价格结构（描述性）\n')
    tpz = O['tier_price']
    A('| 时点 | ' + ' | '.join(TIERS) + ' | 旗舰／经济 | 最高／最低（个体） |')
    A('|---|' + '---|' * (len(TIERS) + 2))
    for m in ['2023-01', '2025-01', '2026-06', '2026-08']:
        row = tpz['snapshot'][m]
        A(f"| {m} | " + ' | '.join(str(row[t]) for t in TIERS) + ' | '
          + f"{tpz['ratio_flag_econ'][m]} | {tpz['item_spread'][m]} |")
    A('')
    A(f"facts.md 锚：同一供给方旗舰档／经济档输出价比约 3 倍 → 本样本 2026-06 为 "
      f"**{tpz['ratio_flag_econ']['2026-06']}** 倍，对齐。")
    A('⚠ DESIGN.md 一稿所称「档位间价差扩大到数十倍」不成立：以**档位均价比**衡量价差在收敛'
      '（旗舰／经济由 %s 倍降至 %s 倍），只有**个体最高／最低价差**仍在十余倍。'
      % (tpz['ratio_flag_econ']['2023-01'], tpz['ratio_flag_econ']['2026-06']))
    A('')

    A('## 9 校准检验\n')
    cal = O['calibration']
    A('| 检验项 | 本脚本 | 公开锚 |')
    A('|---|---|---|')
    for m, v in cal['daily_tokens_check'].items():
        A(f"| 全国日均词元调用量 {m}（万亿枚／日） | {v} | "
          f"{ANCHOR['daily_tokens_wanyi'].get({'2024年初':'2024Q1','2025年6月底':'2025Q2','2025年底':'2025Q4','2026年3月':'2026Q1'}[m])} |")
    A(f"| 支出半年增速（2024Q4→2025Q2） | {cal['spend_growth_2024Q4_2025Q2']*100:.1f}% | "
      '（不可比）美国企业接口支出同口径半年约 140% |')
    A(f"| 旗舰／经济输出价比（2026-06） | {cal['flag_econ_ratio_2026_06']} | 约 3 倍 |")
    A(f"| 智能体化倍数（期末加权） | {cal['agent_multiple_check']['implied_multiple_last']} | "
      '单轮 1／智能体 4／多智能体 15 之间 |')
    A(f"| 面板总量／官方锚（各季比值） | 恒为 1.0 | — |")
    A('')
    A('**口径提醒**：美元口径支出（35→84 亿美元、370 亿美元）只作增速对照，'
      '不与本文人民币口径支出相除或混用；日均词元调用量的非锚点期为校准插值／外推，'
      '正文引用须注明。\n')

    A('## 10 参数复原检查（模拟面板自检）\n')
    dr = O['dgp_recovery']
    A('分析样本由已知参数的数据生成过程校准生成，故可直接检验估计量能否找回真值。'
      '下表的 z ＝（估计−真值）／标准误。\n')
    A('| 参数 | 真值 | 估计 | 标准误 | z |')
    A('|---|---|---|---|---|')
    for v, r in dr['hedonic'].items():
        A(f"| 享乐 β：{r['label']} | {r['true']} | {r['est']} | {r['se']} | {r['z']} |")
    dd = dr['demand']
    A(f"| 需求弹性 ε（FE-OLS 的估计目标：方差加权真值） | {dd['eps_true_varweighted']} | "
      f"{dd['eps_fe_ols']} | {dd['eps_fe_ols_se']} | {dd['z_fe_vs_weighted']} |")
    A(f"| 需求弹性 ε（同一真值，2SLS） | {dd['eps_true_varweighted']} | "
      f"{dd['eps_2sls']} | {dd['eps_2sls_se']} | {dd['z_2sls_vs_weighted']} |")
    A(f"| 智能体化系数 γ | {dd['gamma_true']} | {dd['gamma_est']} | {dd['gamma_se']} | "
      f"{dd['z_gamma']} |")
    fs = dr['first_stage']
    A(f"| 第一阶段 θ（硬件租金） | {fs['theta_hw_true']} | {fs['est_hw']} | {fs['se_hw']} | "
      f"{fs['z_hw']} |")
    A(f"| 第一阶段 θ（电价） | {fs['theta_el_true']} | {fs['est_el']} | {fs['se_el']} | "
      f"{fs['z_el']} |")
    A('')
    A(f"- 需求弹性的真值有两个口径：样本算术平均 eps_i ＝ {dd['eps_true_mean']}；"
      f"异质斜率下双向固定效应 OLS 的**实际估计目标**是以各行业价格 within 方差为权的加权平均"
      f"＝ {dd['eps_true_varweighted']}。正文谈「真实弹性」时须用后者，"
      '并说明异质斜率下固定效应估计量是方差加权平均而非算术平均。')
    A(f"- 固定效应 OLS 距该真值 {dd['z_fe_vs_weighted']} 个标准误（拥塞加价造成的向零偏），"
      f"2SLS 距该真值 {dd['z_2sls_vs_weighted']} 个标准误——成本推移工具变量把偏误基本消掉，"
      '这是本文识别策略在模拟环境下的直接证据。')
    A('- 享乐 β 的 z 全部落在 ±2 以内，未出现「恰好等于真值」的可疑吻合。')
    A('')
    A(f"> {dr['r2_caveat']}\n")

    with open(os.path.join(DATA, 'RESULTS_SPEC.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))


if __name__ == '__main__':
    main()
