# -*- coding: utf-8 -*-
"""论文二《计量摩擦、价格离散与智能服务市场发育》的数据层与全部实证结果。

数据可得性说明：城市层面的智能服务成交价格明细与企业采纳明细不公开，
本文分析样本按 data/facts.md 记录的公开锚点（平台上线时点、补贴券城市与年份、
全国日均词元调用量、同一模型同一问题跨平台真实价差最高约 10 倍）**校准生成**，
用于完整展示识别与推断链条。一切进入正文的数字均由本脚本产生并写入
data/results.json，正文只许引用该文件。

用法：python3 data_gen.py
仅依赖 numpy / pandas / scipy。
"""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
os.makedirs(DATA, exist_ok=True)

SEED = 20260825
RNG = np.random.default_rng(SEED)

# ============================ 一、时间轴与处理时点 ============================
Y0, M0, NT = 2023, 1, 44          # 2023-01 至 2026-08，共 44 期
NCITY = 200                       # 地级及以上城市


def mi(y, m):
    """年月转月份序号，2023-01 记为 0。"""
    return (y - Y0) * 12 + (m - M0)


def ymstr(t):
    y = Y0 + (M0 - 1 + t) // 12
    m = (M0 - 1 + t) % 12 + 1
    return '%04d-%02d' % (y, m)


MONTHS = [ymstr(t) for t in range(NT)]

# ---- 处理 A：城市级统一计量结算平台（facts.md 第二节，逐条对应）----
# 第一代：算力调度型（统一纳管与调度，尚未以词元为计量基准）
NAMED_A1 = {'重庆': mi(2024, 11), '杭州': mi(2025, 3)}
# 第二代：词元计量型（以词元为统一计量与结算基准）
# 北京经开区词元工厂 2026-06-30 投产、国资词元工厂 2026-07-03 亮相，
# 月度面板按“当月末投产、次月起实际运行”口径归入 2026-07。
NAMED_A2 = {'广州': mi(2026, 4), '无锡': mi(2026, 5), '北京': mi(2026, 7),
            '温州': mi(2026, 7), '常州': mi(2026, 7), '嘉兴': mi(2026, 7),
            '苏州': mi(2026, 8)}
# ---- 处理 B：算力券／训力券／词元券（facts.md 第三节）----
NAMED_B = {'成都': mi(2023, 1), '扬州': mi(2024, 5), '深圳': mi(2024, 12),
           '武汉': mi(2025, 2), '北京': mi(2026, 8)}

# 各批次城市数（含上列有名可查的城市，其余按合理比例随机分配）
A1_COH = {mi(2024, 11): 5, mi(2025, 3): 6, mi(2025, 6): 6,
          mi(2025, 9): 5, mi(2025, 12): 4}                     # 26 个
A2_COH = {mi(2026, 4): 4, mi(2026, 5): 5, mi(2026, 6): 6,
          mi(2026, 7): 9, mi(2026, 8): 6}                      # 30 个
B_COH = {mi(2023, 1): 6, mi(2023, 7): 8, mi(2024, 1): 10, mi(2024, 5): 10,
         mi(2024, 12): 12, mi(2025, 2): 12, mi(2025, 8): 12,
         mi(2026, 2): 12, mi(2026, 8): 6}                      # 88 个
N_BOTH_RANDOM = 27          # 两套处理重叠的匿名城市数（另加北京，共 28 个）

NAMED = ['北京', '深圳', '广州', '杭州', '苏州', '重庆', '成都', '武汉',
         '无锡', '常州', '嘉兴', '温州', '扬州']
assert len(NAMED) == 13

# ---- 全国日均词元调用量锚点（facts.md 第五节，国家数据局）----
TOKEN_ANCHOR = {mi(2024, 1): 0.10, mi(2025, 6): 30.0,
                mi(2025, 12): 100.0, mi(2026, 3): 140.0}       # 万亿枚／日

# ---- 计量摩擦与价格离散的现实锚 ----
SPREAD_ANCHOR = 10.0        # 同一模型同一问题跨平台真实价差最高约 10 倍
N_PLAT, N_TASK = 12, 10     # 每城每月对 10 类代表性任务各采集 12 家可比供给方报价

ANCHOR = {
    'spread_max_reported': SPREAD_ANCHOR,
    'token_char_ratio': [1.0, 1.8],          # 词元—汉字换算口径区间
    'cache_hit_high': [0.80, 0.90],          # 高缓存命中率区间
    'cache_hit_low': 0.50,
    'national_daily_tokens_wanyi': {ymstr(k): v for k, v in TOKEN_ANCHOR.items()},
    'smart_compute_eflops_202606': 2185.0,
    'rack_rate_202606': 0.714,
    'gen1_max_window_months': NT - min(A1_COH),
    'gen2_max_window_months': NT - min(A2_COH),
}

# ============================ 二、城市分配 ============================


def assign_cities():
    """把 200 个城市分配到两套处理的各批次；有名可查的城市按 facts.md 硬编码。"""
    name = NAMED + ['C%03d' % (i + 1) for i in range(len(NAMED), NCITY)]
    idx = {c: i for i, c in enumerate(name)}

    # 数字经济基础（城市固定特征）：有名可查的城市取较高值
    zdig = RNG.normal(0.0, 1.0, NCITY)
    zdig[:len(NAMED)] = 1.05 + 0.42 * RNG.normal(0, 1, len(NAMED))

    pool = np.arange(len(NAMED), NCITY)              # 187 个匿名城市
    w = np.exp(1.10 * zdig[pool])
    n_a_rand = sum(A1_COH.values()) + sum(A2_COH.values()) \
        - len(NAMED_A1) - len(NAMED_A2)
    a_rand = RNG.choice(pool, size=n_a_rand, replace=False, p=w / w.sum())

    # 处理 B 的随机城市：一部分落在处理 A 的城市上（构成重叠组）
    wb = np.exp(0.60 * zdig[a_rand])
    b_in_a = RNG.choice(a_rand, size=N_BOTH_RANDOM, replace=False, p=wb / wb.sum())
    rest = np.setdiff1d(pool, a_rand)
    n_b_rand = sum(B_COH.values()) - len(NAMED_B) - N_BOTH_RANDOM
    wr = np.exp(0.80 * zdig[rest])
    b_out_a = RNG.choice(rest, size=n_b_rand, replace=False, p=wr / wr.sum())
    b_rand = np.concatenate([b_in_a, b_out_a])
    RNG.shuffle(b_rand)

    def fill(coh, named, rand_pool):
        """先放有名可查的城市，再用随机城市补足每个批次。"""
        g = np.full(NCITY, np.nan)
        for c, t in named.items():
            g[idx[c]] = t
        left = list(rand_pool)
        ptr = 0
        for t in sorted(coh):
            need = coh[t] - sum(1 for c, tt in named.items() if tt == t)
            assert need >= 0, (t, coh[t])
            for _ in range(need):
                g[left[ptr]] = t
                ptr += 1
        assert ptr == len(left), (ptr, len(left))
        return g

    a1_named = {c: t for c, t in NAMED_A1.items()}
    a2_named = {c: t for c, t in NAMED_A2.items()}
    n1 = sum(A1_COH.values()) - len(a1_named)
    gA1 = fill(A1_COH, a1_named, list(a_rand[:n1]))
    gA2 = fill(A2_COH, a2_named, list(a_rand[n1:]))
    gB = fill(B_COH, NAMED_B, list(b_rand))

    assert np.isnan(gA1 * gA2).all() or not np.any(~np.isnan(gA1) & ~np.isnan(gA2))
    return name, zdig, gA1, gA2, gB


# ============================ 三、面板生成 ============================


def ar1(sd, rho, rng):
    e = rng.normal(0.0, sd, (NCITY, NT))
    x = np.empty_like(e)
    x[:, 0] = e[:, 0] / np.sqrt(1 - rho ** 2)
    for t in range(1, NT):
        x[:, t] = rho * x[:, t - 1] + e[:, t]
    return x


def prof(k, rate):
    """事件时间剖面：处理后按 1-exp(-rate*(k+1)) 逐月走强，处理前为 0。"""
    k = np.asarray(k, dtype=float)
    out = np.where(np.isfinite(k) & (k >= 0), 1.0 - np.exp(-rate * (k + 1.0)), 0.0)
    return out


def national_daily_path():
    """全国日均词元调用量（万亿枚／日）：锚点间对数线性插值，两端外推并标记。"""
    ks = sorted(TOKEN_ANCHOR)
    ln = np.full(NT, np.nan)
    for k in ks:
        ln[k] = np.log(TOKEN_ANCHOR[k])
    for a, b in zip(ks[:-1], ks[1:]):
        sl = (ln[b] - ln[a]) / (b - a)
        for t in range(a + 1, b):
            ln[t] = ln[a] + sl * (t - a)
    sl0 = (ln[ks[1]] - ln[ks[0]]) / (ks[1] - ks[0])
    for t in range(ks[0] - 1, -1, -1):
        ln[t] = ln[t + 1] - sl0
    sl1 = (ln[ks[-1]] - ln[ks[-2]]) / (ks[-1] - ks[-2])
    step = sl1
    for t in range(ks[-1] + 1, NT):
        step *= 0.90                     # 增速逐月递减，避免线性外推失真
        ln[t] = ln[t - 1] + step
    interp = np.ones(NT, dtype=bool)
    for k in ks:
        interp[k] = False
    return np.exp(ln), interp


# 关键结构参数（全部在此集中，便于复核）
PAR = dict(
    tau0=0.65,          # 计量摩擦指数基准水平（ln η 的先验标准差）
    tau_decay=0.0228,   # 计量摩擦的自然收敛速度（每年绝对降幅，对所有城市相同，
                        # 以免在处理组与对照组之间制造事前差异化趋势）
    r_gen1=0.105,       # 第一代平台对计量摩擦的峰值压降比例
    r_gen2=0.270,       # 第二代平台对计量摩擦的峰值压降比例
    rate_gen1=0.15,     # 第一代效应的月度爬升速度
    rate_gen2=0.45,     # 第二代效应的月度爬升速度
    rate_B=0.25,        # 补贴效应的月度爬升速度
    s_free=0.16,        # 搜寻成本为零时的残余真实价格离散（对数标准差）
    s_lam=0.55,         # 真实价格离散对计量摩擦的弹性（命题 1）
    b_eta=-0.55,        # 平均成交效值对计量摩擦的斜率（命题 2）
    b_sme=-0.42,        # 中小企业采纳率对计量摩擦的斜率（命题 3）
    b_lrg=-0.145,       # 大企业采纳率对计量摩擦的斜率
    b_tok=-1.02,        # 词元调用量（对数）对计量摩擦的斜率
    b_mu=0.28,          # 名义单价（对数）对计量摩擦的斜率
    B_disp=0.000,       # 补贴对价格方差的直接效应：理论上为零
    B_sme=0.026, B_lrg=0.014, B_eta=-0.019, B_tok=0.082, B_mu=-0.086,
    AB_sme=0.008, AB_lrg=0.002, AB_eta=0.024, AB_tok=0.020, AB_mu=-0.006,
    mu0=np.log(28.0),   # 2023-01 市场均价（元／百万词元）
    mu_decay=0.62,      # 名义单价年度对数降幅
    tpc0=np.log(0.0018),  # 2023-01 每次调用词元数（百万枚）
    tpc_grow=0.20,
)


def build_panel():
    name, zdig, gA1, gA2, gB = assign_cities()

    zdig = (zdig - zdig.mean()) / zdig.std()
    # 企业规模结构：中小企业占比（数字经济基础越强，大企业相对更多）
    sme_share = np.clip(0.862 + 0.030 * RNG.normal(0, 1, NCITY)
                        - 0.013 * zdig, 0.72, 0.95)
    zsme = (sme_share - sme_share.mean()) / sme_share.std()
    zsize = 0.55 * zdig + 0.835 * RNG.normal(0, 1, NCITY)

    lnpop0 = 6.00 + 0.35 * zsize
    lngdp0 = 7.90 + 0.45 * zdig + 0.55 * (lnpop0 - 6.0) + 0.15 * RNG.normal(0, 1, NCITY)
    dig0 = 45.0 + 9.0 * zdig + 3.0 * RNG.normal(0, 1, NCITY)
    ai0 = np.clip(8.0 + 4.5 * zdig + 1.5 * RNG.normal(0, 1, NCITY), 0.6, None)

    t = np.arange(NT)[None, :].repeat(NCITY, axis=0).astype(float)
    yr = t / 12.0

    kA1 = np.where(np.isnan(gA1)[:, None], np.nan, t - gA1[:, None])
    kA2 = np.where(np.isnan(gA2)[:, None], np.nan, t - gA2[:, None])
    kB = np.where(np.isnan(gB)[:, None], np.nan, t - gB[:, None])

    fA1 = prof(kA1, PAR['rate_gen1'])
    fA2 = prof(kA2, PAR['rate_gen2'])
    fA = fA1 + fA2                       # 两代互斥，可直接相加
    fB = prof(kB, PAR['rate_B'])
    fAB = fA * fB

    # 处理强度的城市异质性（命题 3）：中小企业占比越高、折算能力 κ 越低，
    # 统一计量对计量摩擦的压降比例越大。
    mod = np.clip(1.0 + 0.52 * zsme, 0.30, 2.00)[:, None]
    red = np.clip((PAR['r_gen1'] * fA1 + PAR['r_gen2'] * fA2) * mod, 0.0, 0.60)

    # ---- 计量摩擦指数（潜变量）----
    ar_tau = ar1(0.009, 0.85, RNG)
    tau0_i = PAR['tau0'] * np.exp(-0.120 * zdig + 0.09 * RNG.normal(0, 1, NCITY))
    tau_free = np.clip(tau0_i[:, None] * np.exp(ar_tau) - PAR['tau_decay'] * yr,
                       0.15, None)                # 无平台情形下的计量摩擦路径
    tau = tau_free * (1.0 - red)
    TAU0 = float(tau[:, 0].mean())

    # ---- 跨平台报价模拟：真实（折算后）单价与名义单价 ----
    s = (PAR['s_free'] + PAR['s_lam'] * tau) * np.exp(0.05 * RNG.normal(0, 1, (NCITY, NT)))
    eps = RNG.standard_normal((NCITY, NT, N_TASK, N_PLAT))
    task_off = RNG.normal(0, 0.35, N_TASK)
    logp_real = task_off[None, None, :, None] + s[:, :, None, None] * eps
    p_real = np.exp(logp_real)
    cv = p_real.std(axis=3, ddof=1) / p_real.mean(axis=3)
    disp = cv.mean(axis=2)
    q1, q2, q3 = np.quantile(p_real, [0.25, 0.50, 0.75], axis=3)
    disp_iqr = ((q3 - q1) / q2).mean(axis=2)
    spread_task = p_real.max(axis=3) / p_real.min(axis=3)
    spread = spread_task.mean(axis=2)

    eta_e = RNG.standard_normal((NCITY, NT, N_TASK, N_PLAT))
    logp_nom = logp_real + tau[:, :, None, None] * eta_e
    sd_nom = logp_nom.std(axis=3, ddof=1).mean(axis=2)
    sd_real = logp_real.std(axis=3, ddof=1).mean(axis=2)
    mfi = sd_nom - sd_real                      # 计量摩擦指数（可观测构造）

    ar_disp = ar1(0.006, 0.80, RNG)
    disp = disp + ar_disp + PAR['B_disp'] * fB
    disp_iqr = disp_iqr + 1.15 * ar_disp
    mfi = mfi + 0.45 * ar_disp

    # ---- 采纳率 ----
    L_sme = 0.14 + 0.34 / (1.0 + np.exp(-(t - 24.0) / 7.5))
    L_lrg = 0.28 + 0.44 / (1.0 + np.exp(-(t - 22.0) / 8.0))
    ar_ad = ar1(0.004, 0.85, RNG)
    cfe = RNG.normal(0, 1, NCITY)[:, None]
    adopt_sme = np.clip(
        L_sme + 0.055 * zdig[:, None] + PAR['b_sme'] * (tau - TAU0)
        + PAR['B_sme'] * fB + PAR['AB_sme'] * fAB
        + 0.012 * cfe + ar_ad + RNG.normal(0, 0.012, (NCITY, NT)), 0.01, 0.98)
    adopt_large = np.clip(
        L_lrg + 0.075 * zdig[:, None] + PAR['b_lrg'] * (tau - TAU0)
        + PAR['B_lrg'] * fB + PAR['AB_lrg'] * fAB
        + 0.016 * cfe + 0.9 * ar_ad + RNG.normal(0, 0.014, (NCITY, NT)), 0.01, 0.98)

    # ---- 平均成交效值（逆向选择渠道）----
    ar_eta = ar1(0.007, 0.85, RNG)
    eta_bar = (1.25 + PAR['b_eta'] * tau + PAR['B_eta'] * fB + PAR['AB_eta'] * fAB
               + 0.020 * cfe + ar_eta + RNG.normal(0, 0.020, (NCITY, NT)))

    # ---- 词元调用量 ----
    nat_daily, interp_flag = national_daily_path()
    nat_month_yi = nat_daily * 1e4 * 30.4                    # 亿枚／月
    w = np.exp(0.75 * zsize)
    share0 = w / w.sum()
    ar_tok = ar1(0.025, 0.85, RNG)
    ln_tok_raw = (np.log(share0)[:, None] + np.log(nat_month_yi)[None, :]
                  + PAR['b_tok'] * (tau - TAU0) + PAR['B_tok'] * fB
                  + PAR['AB_tok'] * fAB + 0.060 * cfe + ar_tok
                  + RNG.normal(0, 0.060, (NCITY, NT)))
    tok = np.exp(ln_tok_raw)
    tok *= (nat_month_yi / tok.sum(axis=0))[None, :]         # 月度共同因子，被时间固定效应吸收
    ln_token = np.log(tok)

    # ---- 价格水平与单位调用支出 ----
    ar_mu = ar1(0.012, 0.85, RNG)
    mu = (PAR['mu0'] - PAR['mu_decay'] * yr + PAR['b_mu'] * (tau - TAU0)
          + PAR['B_mu'] * fB + PAR['AB_mu'] * fAB + 0.050 * cfe + ar_mu
          + RNG.normal(0, 0.030, (NCITY, NT)))
    ln_tpc = PAR['tpc0'] + PAR['tpc_grow'] * yr + RNG.normal(0, 0.020, (NCITY, NT))
    ln_spend = mu + ln_tpc
    spend_per_call = np.exp(ln_spend)

    # ---- 控制变量（外生，不受处理影响）----
    lngdp = lngdp0[:, None] + 0.052 * yr + RNG.normal(0, 0.020, (NCITY, NT))
    lnpop = lnpop0[:, None] + 0.004 * yr + RNG.normal(0, 0.004, (NCITY, NT))
    dig = dig0[:, None] + 4.2 * yr + RNG.normal(0, 0.80, (NCITY, NT))
    ai_firm = ai0[:, None] * np.exp(0.28 * yr) + RNG.normal(0, 0.20, (NCITY, NT))

    ci = np.repeat(np.arange(NCITY), NT)
    df = pd.DataFrame(dict(
        city=ci, cityname=np.array(name)[ci], month=np.tile(np.arange(NT), NCITY),
        ym=np.array(MONTHS)[np.tile(np.arange(NT), NCITY)],
        gA1=np.repeat(gA1, NT), gA2=np.repeat(gA2, NT), gB=np.repeat(gB, NT),
        kA1=kA1.ravel(), kA2=kA2.ravel(), kB=kB.ravel(),
        zdig=np.repeat(zdig, NT), zsme=np.repeat(zsme, NT),
        sme_share=np.repeat(sme_share, NT),
        lngdp=lngdp.ravel(), lnpop=lnpop.ravel(), dig=dig.ravel(),
        ai_firm=ai_firm.ravel(),
        tau=tau.ravel(), mfi=mfi.ravel(),
        disp=disp.ravel(), disp_iqr=disp_iqr.ravel(), spread=spread.ravel(),
        adopt_sme=adopt_sme.ravel(), adopt_large=adopt_large.ravel(),
        eta_bar=eta_bar.ravel(), ln_token=ln_token.ravel(),
        token_yi=tok.ravel(), spend_per_call=spend_per_call.ravel(),
        ln_spend=ln_spend.ravel(),
    ))
    df['post_A1'] = (df['kA1'] >= 0).fillna(False).astype(float)
    df['post_A2'] = (df['kA2'] >= 0).fillna(False).astype(float)
    df['post_A'] = np.maximum(df['post_A1'], df['post_A2'])
    df['post_B'] = (df['kB'] >= 0).fillna(False).astype(float)
    df['post_AB'] = df['post_A'] * df['post_B']
    df['kA'] = np.where(np.isfinite(df['kA1']), df['kA1'], df['kA2'])
    df['gA'] = np.where(np.isfinite(df['gA1']), df['gA1'], df['gA2'])
    df['gen'] = np.where(np.isfinite(df['gA1']), 1,
                         np.where(np.isfinite(df['gA2']), 2, 0))

    everA = np.isfinite(df.groupby('city')['gA'].first().to_numpy())
    everB = np.isfinite(df.groupby('city')['gB'].first().to_numpy())
    grp = np.where(everA & everB, 'both',
                   np.where(everA, 'onlyA', np.where(everB, 'onlyB', 'none')))
    df['grp'] = grp[df['city'].to_numpy()]

    meta = dict(spread_task=spread_task, interp_flag=interp_flag,
                nat_daily=nat_daily, nat_month_yi=nat_month_yi,
                TAU0=TAU0, name=name)
    return df, meta


# ============================ 四、估计量 ============================

CTRL = ['lngdp', 'lnpop', 'dig', 'ai_firm']


def _absorb(A, idxs, ns, tol=1e-11, maxit=400):
    """交替投影去均值，吸收多重高维固定效应（平衡面板一轮即精确收敛）。"""
    A = np.array(A, dtype=float, copy=True)
    if A.ndim == 1:
        A = A[:, None]
    for _ in range(maxit):
        delta = 0.0
        for idx, n in zip(idxs, ns):
            cnt = np.bincount(idx, minlength=n).astype(float)
            cnt[cnt == 0] = 1.0
            for j in range(A.shape[1]):
                gm = np.bincount(idx, weights=A[:, j], minlength=n) / cnt
                A[:, j] -= gm[idx]
                delta = max(delta, float(np.abs(gm).max()))
        if delta < tol:
            break
    return A


def _p(x):
    """p 值保精度：≥1e-6 保留 6 位小数，更小则保留两位有效数字，
    避免在 results.json 里写出恰好为 0 的 p 值。"""
    x = float(x)
    return round(x, 6) if x >= 1e-6 else float('%.2e' % x)


def _meat(X, u, idx):
    g = int(idx.max()) + 1
    S = np.empty((g, X.shape[1]))
    for j in range(X.shape[1]):
        S[:, j] = np.bincount(idx, weights=X[:, j] * u, minlength=g)
    return S.T @ S


def _fit(Y, X, names, cl1, cl2=None, kabs=0):
    """已去均值数据上的 OLS ＋（双重）聚类稳健标准误。

    先做秩检验再求解：np.linalg.pinv 对秩亏设计会静默返回最小范数解，
    该解依参数化而变、并非一个良定义的估计量（例如某批次无事前期时，
    其群组×相对期哑变量与该批城市的固定效应完全共线）。此处显式拦截。
    """
    XtX = X.T @ X
    rk = int(np.linalg.matrix_rank(XtX))
    if rk < X.shape[1]:
        raise ValueError('设计矩阵秩亏：列数 %d、秩 %d；存在完全共线的回归元。'
                         '前若干列：%s' % (X.shape[1], rk, '、'.join(list(names)[:10])))
    XtXi = np.linalg.pinv(XtX)
    beta = XtXi @ (X.T @ Y)
    u = Y - X @ beta
    n, kx = X.shape
    kk = kx + kabs

    def adj(idx):
        g = int(idx.max()) + 1
        return g / max(g - 1, 1) * (n - 1) / max(n - kk, 1)

    V = XtXi @ (_meat(X, u, cl1) * adj(cl1)) @ XtXi
    ncl = int(cl1.max()) + 1
    if cl2 is not None:
        V2 = XtXi @ (_meat(X, u, cl2) * adj(cl2)) @ XtXi
        both = pd.factorize(pd.Series(cl1).astype(str) + '_' + pd.Series(cl2).astype(str))[0]
        V12 = XtXi @ (_meat(X, u, both) * adj(both)) @ XtXi
        V = V + V2 - V12
        w, Q = np.linalg.eigh((V + V.T) / 2.0)
        V = Q @ np.diag(np.clip(w, 0.0, None)) @ Q.T
    se = np.sqrt(np.clip(np.diag(V), 0.0, None))
    tv = np.divide(beta, se, out=np.zeros_like(beta), where=se > 0)
    pv = 2.0 * stats.norm.sf(np.abs(tv))
    r = dict(coef={}, se={}, t={}, p={}, n=int(n), ncluster=ncl,
             r2_within=float(1 - u.var() / Y.var()) if Y.var() > 0 else 0.0)
    for j, nm in enumerate(names):
        r['coef'][nm] = round(float(beta[j]), 6)
        r['se'][nm] = round(float(se[j]), 6)
        r['t'][nm] = round(float(tv[j]), 4)
        r['p'][nm] = _p(pv[j])
    r['_V'] = V
    r['_names'] = list(names)
    return r


def _within(d, y, xs, cluster2=None, extra_fe=None):
    """城市＋月份双向固定效应回归，城市层面聚类（可选城市—月份双重聚类）。"""
    cols = [y] + list(xs)
    dd = d[cols + ['city', 'month']].dropna()
    ci = pd.factorize(dd['city'])[0]
    ti = pd.factorize(dd['month'])[0]
    idxs, ns = [ci, ti], [ci.max() + 1, ti.max() + 1]
    if extra_fe is not None:
        for c in extra_fe:
            e = pd.factorize(d.loc[dd.index, c])[0]
            idxs.append(e)
            ns.append(e.max() + 1)
    M = _absorb(dd[cols].to_numpy(float), idxs, ns)
    kabs = sum(ns) - len(ns) + 1
    cl2 = ti if cluster2 == 'month' else None
    return _fit(M[:, 0], M[:, 1:], list(xs), ci, cl2=cl2, kabs=kabs)


def _wald(r, keys):
    """若干系数联合为零的 Wald 检验。"""
    pos = [r['_names'].index(k) for k in keys]
    b = np.array([r['coef'][k] for k in keys])
    V = r['_V'][np.ix_(pos, pos)]
    w = float(b @ np.linalg.pinv(V) @ b)
    return dict(wald=round(w, 4), df=len(keys),
                p=_p(stats.chi2.sf(w, len(keys))))


def _pick(r, key):
    return dict(coef=r['coef'][key], se=r['se'][key], t=r['t'][key],
                p=r['p'][key], n=r['n'], ncluster=r['ncluster'])


# ---------------------------- 事件研究 ----------------------------
# 相对期上限受制于样本末期：第一代最长 22 个月，第二代最长 5 个月，
# 故第二代的事件研究上限只能取 +4，不得伪造更长的动态路径。
EVWIN = {'A1': (-6, 6), 'A2': (-6, 4), 'B': (-6, 6)}
BASEK = -1


def _drop_nobase(d, gcol):
    """剔除在样本期内没有基期（k=BASEK）的批次城市。

    2023-01 批次的补贴城市自样本首期即已受处理，其群组×相对期哑变量之和恒为 1，
    与该批城市的城市固定效应完全共线；CS 估计量本就跳过这类批次，
    事件研究与 SA 也必须同样剔除，否则只能靠伪逆给出无定义的最小范数解。
    """
    g = d[gcol].to_numpy(float)
    bad = np.isfinite(g) & (g + BASEK < 0)
    n = int(d.loc[bad, 'city'].nunique())
    return (d[~bad].copy() if n else d), n


def _evcols(d, kcol, lo, hi, tag):
    ever = np.isfinite(d[kcol].to_numpy())
    kk = np.where(ever, np.clip(d[kcol].to_numpy(), lo, hi), np.nan)
    cols = []
    for kv in range(lo, hi + 1):
        if kv == BASEK:
            continue
        c = '%s_k%s' % (tag, ('m%d' % -kv) if kv < 0 else ('p%d' % kv))
        d[c] = ((kk == kv) & ever).astype(float)
        cols.append((kv, c))
    return cols


def event_study(df, y, which):
    lo, hi = EVWIN[which]
    kcol = {'A1': 'kA1', 'A2': 'kA2', 'B': 'kB'}[which]
    other = {'A1': ['post_A2', 'post_B'], 'A2': ['post_A1', 'post_B'],
             'B': ['post_A1', 'post_A2']}[which]
    gcol = {'A1': 'gA1', 'A2': 'gA2', 'B': 'gB'}[which]
    d, ndrop = _drop_nobase(df, gcol)
    cols = _evcols(d, kcol, lo, hi, which)
    r = _within(d, y, [c for _, c in cols] + other + CTRL)
    out = {'window': [lo, hi], 'base': BASEK,
           'binned_ends': True,
           'coefs': {str(kv): dict(coef=r['coef'][c], se=r['se'][c],
                                   t=r['t'][c], p=r['p'][c]) for kv, c in cols},
           'ncity_dropped_nobase': ndrop,
           'n': r['n'], 'ncluster': r['ncluster']}
    pre = [c for kv, c in cols if kv < BASEK]
    post = [c for kv, c in cols if kv >= 0]
    out['pretrend_joint'] = _wald(r, pre)
    out['post_joint'] = _wald(r, post)
    return out


def event_study_long(df, y, hi=12):
    """第一代平台窗口较长，另给出 +12 期的动态路径（第二代无此数据基础）。"""
    d, ndrop = _drop_nobase(df, 'gA1')
    cols = _evcols(d, 'kA1', -6, hi, 'A1L')
    r = _within(d, y, [c for _, c in cols] + ['post_A2', 'post_B'] + CTRL)
    return {'window': [-6, hi], 'base': BASEK, 'binned_ends': True,
            'ncity_dropped_nobase': ndrop,
            'coefs': {str(kv): dict(coef=r['coef'][c], se=r['se'][c], p=r['p'][c])
                      for kv, c in cols}}


# ------------------ Callaway & Sant'Anna（2021）------------------


def callaway_santanna(df, y, gcol, lo, hi, ctl_never_only=False):
    """群组—时期 ATT(g,t)，比较组为尚未接受同类处理的城市，按事件时间聚合。

    聚合方差用城市层面影响函数计算：同一城市反复出现在多个 (g,t) 单元中，
    若按独立单元加总会低估标准误。
    """
    g_all = df.groupby('city')[gcol].first()
    gs = sorted(g_all.dropna().unique())
    ever = g_all.notna()
    piv = df.pivot(index='city', columns='month', values=y)
    cities = piv.index.to_numpy()
    cpos = {c: j for j, c in enumerate(cities)}
    cells = {}
    for g in gs:
        pre = int(g) - 1
        if pre < 0:
            continue                                   # 首批城市无事前期，不参与
        trt_c = g_all[g_all == g].index.to_numpy()
        for t in range(NT):
            e = t - int(g)
            if e < lo or e > hi or t == pre:
                continue
            if ctl_never_only:
                ctl_c = g_all[~ever].index.to_numpy()
            else:                                      # 尚未处理（含从未处理）
                ctl_c = g_all[(~ever) | (g_all > max(t, g))].index.to_numpy()
            if len(trt_c) < 3 or len(ctl_c) < 10:
                continue
            dvec = (piv[t] - piv[pre])
            dt = dvec.loc[trt_c].to_numpy(float)
            dc = dvec.loc[ctl_c].to_numpy(float)
            att = float(dt.mean() - dc.mean())
            psi = np.zeros(len(cities))
            psi[[cpos[c] for c in trt_c]] = (dt - dt.mean()) / len(dt)
            psi[[cpos[c] for c in ctl_c]] -= (dc - dc.mean()) / len(dc)
            cells.setdefault(e, []).append((att, psi, len(dt), int(g)))

    def agg(lst):
        w = np.array([x[2] for x in lst], float)
        w /= w.sum()
        a = float(w @ np.array([x[0] for x in lst]))
        psi = np.zeros(len(cities))
        for wi, x in zip(w, lst):
            psi += wi * x[1]
        se = float(np.sqrt((psi ** 2).sum()))
        z = a / se if se > 0 else 0.0
        return dict(coef=round(a, 6), se=round(se, 6), t=round(z, 4),
                    p=_p(2 * stats.norm.sf(abs(z))))

    out = {'by_event': {}}
    for e, lst in sorted(cells.items()):
        out['by_event'][str(e)] = agg(lst)
    for tag, sel in (('att', lambda e: e >= 0), ('pre', lambda e: e < 0)):
        flat = [c for e, lst in cells.items() if sel(e) for c in lst]
        if flat:
            out[tag] = agg(flat)
    out['ncell'] = int(sum(len(v) for v in cells.values()))
    out['ncity_treated'] = int(ever.sum())
    _gv = g_all.to_numpy(float)
    out['ncity_dropped_nobase'] = int((np.isfinite(_gv) & (_gv + BASEK < 0)).sum())
    return out


# ------------------ Sun & Abraham（2021）------------------


def sun_abraham(df, y, kcol, gcol, lo, hi, other):
    """群组×相对期交互加权估计；从未处理城市为干净参照组。

    无事前期的批次（样本首期即已受处理）必须整批剔除：其群组×相对期哑变量
    之和恒为 1，与该批城市的城市固定效应完全共线，估计量无定义。
    """
    d, ndrop = _drop_nobase(df, gcol)
    ever = np.isfinite(d[kcol].to_numpy())
    kk = np.where(ever, np.clip(d[kcol].to_numpy(), lo, hi), np.nan)
    gv = d[gcol].to_numpy()
    gs = sorted(pd.unique(gv[np.isfinite(gv)]))
    cols, meta = [], []
    for g in gs:
        for kv in range(lo, hi + 1):
            if kv == BASEK:
                continue
            c = 'S%d_%s' % (int(g), ('m%d' % -kv) if kv < 0 else ('p%d' % kv))
            v = ((gv == g) & (kk == kv)).astype(float)
            if v.sum() > 0:
                d[c] = v
                cols.append(c)
                meta.append((int(g), kv))
    r = _within(d, y, cols + other + CTRL)
    share = d.groupby(gcol)['city'].nunique()
    share = share / share.sum()
    pos = {c: r['_names'].index(c) for c in cols}

    def lincomb(pairs):
        """pairs: [(列名, 权重)]，用完整协方差阵算线性组合的方差。"""
        idx = [pos[c] for c, _ in pairs]
        w = np.array([x[1] for x in pairs], float)
        b = float(w @ np.array([r['coef'][c] for c, _ in pairs]))
        V = r['_V'][np.ix_(idx, idx)]
        se = float(np.sqrt(max(w @ V @ w, 0.0)))
        z = b / se if se > 0 else 0.0
        return dict(coef=round(b, 6), se=round(se, 6), t=round(z, 4),
                    p=_p(2 * stats.norm.sf(abs(z))))

    agg = {}
    for (g, kv), c in zip(meta, cols):
        agg.setdefault(kv, []).append((c, float(share[g])))
    out = {'by_event': {}}
    for kv, lst in sorted(agg.items()):
        tot = sum(x[1] for x in lst)
        out['by_event'][str(kv)] = lincomb([(c, w / tot) for c, w in lst])
    # 总体 ATT：先在群组内部对其实际可观测的事后期取平均，再按群组规模加权，
    # 避免把只观测到 k=0 的晚批次与观测到 k=0—6 的早批次直接混平均。
    for tag, sel in (('att', lambda k: k >= 0), ('pre', lambda k: k < 0)):
        by_g = {}
        for (g, kv), c in zip(meta, cols):
            if sel(kv):
                by_g.setdefault(g, []).append(c)
        if not by_g:
            continue
        wsum = sum(float(share[g]) for g in by_g)
        pairs = []
        for g, lst in by_g.items():
            for c in lst:
                pairs.append((c, float(share[g]) / wsum / len(lst)))
        out[tag] = lincomb(pairs)
    out['n'] = r['n']
    out['ncluster'] = r['ncluster']
    out['ncity_dropped_nobase'] = ndrop
    out['ncohort'] = len(gs)
    return out


# ---------------------------- 安慰剂检验 ----------------------------


def placebo(df, y, which='A', reps=500, rng=None):
    """随机化处理时点：保持各批次城市数不变，把批次标签在城市间随机重排。"""
    rng = rng or RNG
    ci = pd.factorize(df['city'])[0]
    ti = pd.factorize(df['month'])[0]
    nc, nt = ci.max() + 1, ti.max() + 1
    tvec = df['month'].to_numpy()
    # 安慰剂分布与「真实系数」必须来自同一设定：置换 A 时另一处理固定为 post_B，
    # 置换 B 时另一处理固定为 post_A（合并档），与下面 true 的设定逐字对应。
    fixed = ['post_B'] if which == 'A' else ['post_A']
    base = _absorb(df[[y] + fixed + CTRL].to_numpy(float), [ci, ti], [nc, nt])
    Yd, Zd = base[:, 0], base[:, 1:]
    kabs = nc + nt - 1
    gcol = 'gA' if which == 'A' else 'gB'
    g_city = df.groupby('city')[gcol].first().to_numpy(float)
    true = _within(df, y, ['post_A', 'post_B'] + CTRL)['coef'][
        'post_A' if which == 'A' else 'post_B']
    coefs = np.empty(reps)
    for r in range(reps):
        gp = rng.permutation(g_city)
        post = (tvec >= gp[ci]).astype(float)
        post = np.where(np.isnan(gp[ci]), 0.0, post)
        Pd = _absorb(post[:, None], [ci, ti], [nc, nt])
        X = np.hstack([Pd, Zd])
        b = np.linalg.lstsq(X, Yd, rcond=None)[0]
        coefs[r] = b[0]
    a = np.abs(coefs)
    # 蒙特卡洛 p 值用 (1+#)/(1+R)：置换检验的经验 p 值不可能恰好为 0，
    # 500 次重排能达到的下界是 1/501≈0.002。
    nge = int((a >= abs(true)).sum())
    return dict(true=round(float(true), 6), reps=int(reps),
                mean=round(float(coefs.mean()), 6), sd=round(float(coefs.std(ddof=1)), 6),
                n_ge_abs=nge, p_min_attainable=round(1.0 / (reps + 1), 4),
                p_two_sided=round((1.0 + nge) / (reps + 1.0), 4),
                q95_abs=round(float(np.quantile(a, 0.95)), 6),
                q99_abs=round(float(np.quantile(a, 0.99)), 6),
                pct=[round(float(np.quantile(coefs, q)), 6)
                     for q in (0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99)],
                draws=[round(float(c), 6) for c in coefs])


# ---------------------------- 机制与制度成分分解 ----------------------------

MECH_Y = ['disp', 'disp_iqr', 'adopt_sme', 'adopt_large', 'eta_bar',
          'spend_per_call', 'ln_spend', 'ln_token']


def mech_decomp(df):
    """把样本分为「仅补贴」「仅计量」「两者兼有」三组，各自与从未处理城市对照。"""
    out = {'group_size': {g: int(df[df.grp == g]['city'].nunique())
                          for g in ['none', 'onlyA', 'onlyB', 'both']}, 'by_y': {}}
    for y in MECH_Y:
        res = {}
        sub = df[df.grp.isin(['onlyB', 'none'])]
        res['onlyB'] = _pick(_within(sub, y, ['post_B'] + CTRL), 'post_B')
        sub = df[df.grp.isin(['onlyA', 'none'])]
        res['onlyA'] = _pick(_within(sub, y, ['post_A'] + CTRL), 'post_A')
        sub = df[df.grp.isin(['both', 'none'])]
        rb = _within(sub, y, ['post_A', 'post_B', 'post_AB'] + CTRL)
        res['both'] = {k: _pick(rb, k) for k in ['post_A', 'post_B', 'post_AB']}
        idx = [rb['_names'].index(k) for k in ['post_A', 'post_B', 'post_AB']]
        w = np.ones(3)
        tot = float(w @ np.array([rb['coef'][k] for k in ['post_A', 'post_B', 'post_AB']]))
        V = rb['_V'][np.ix_(idx, idx)]
        se = float(np.sqrt(max(w @ V @ w, 0.0)))
        res['both']['total'] = dict(coef=round(tot, 6), se=round(se, 6),
                                    t=round(tot / se, 4),
                                    p=_p(2 * stats.norm.sf(abs(tot / se))))
        # 不可替代性检验一：两组效应之差
        da = res['onlyA']['coef'] - res['onlyB']['coef']
        sda = np.sqrt(res['onlyA']['se'] ** 2 + res['onlyB']['se'] ** 2)
        res['diff_A_minus_B'] = dict(coef=round(float(da), 6), se=round(float(sda), 6),
                                     z=round(float(da / sda), 4),
                                     p=_p(2 * stats.norm.sf(abs(da / sda))),
                                     se_note='两组来自不同子样本但共用「从未处理」对照组，'
                                             '此处按独立处理，忽略正协方差，标准误偏保守')
        # 不可替代性检验二：兼有组的合计效应 vs 两者单独效应之和（超可加／次可加）
        add = res['onlyA']['coef'] + res['onlyB']['coef']
        dsup = res['both']['total']['coef'] - add
        sse = np.sqrt(res['both']['total']['se'] ** 2 + res['onlyA']['se'] ** 2
                      + res['onlyB']['se'] ** 2)
        res['superadd'] = dict(sum_separate=round(float(add), 6),
                               both_total=res['both']['total']['coef'],
                               coef=round(float(dsup), 6), se=round(float(sse), 6),
                               z=round(float(dsup / sse), 4),
                               p=_p(2 * stats.norm.sf(abs(dsup / sse))))
        out['by_y'][y] = res
    return out


# ---------------------------- 异质性 ----------------------------


def hetero(df, y, modvar, label):
    """按城市固定特征的中位数分组分别估计处理 A 的效应。"""
    v = df.groupby('city')[modvar].first()
    hi_set = set(v[v > v.median()].index)
    xs = ['post_A1', 'post_A2', 'post_B', 'post_AB'] + CTRL
    out = {'modvar': modvar, 'label': label}
    for nm, sel in (('high', df['city'].isin(hi_set)), ('low', ~df['city'].isin(hi_set))):
        r = _within(df[sel], y, xs)
        out[nm] = {k: _pick(r, k) for k in ['post_A1', 'post_A2', 'post_B']}
    for k in ['post_A1', 'post_A2', 'post_B']:
        d0 = out['high'][k]['coef'] - out['low'][k]['coef']
        s0 = np.sqrt(out['high'][k]['se'] ** 2 + out['low'][k]['se'] ** 2)
        out.setdefault('diff', {})[k] = dict(
            coef=round(float(d0), 6), se=round(float(s0), 6), z=round(float(d0 / s0), 4),
            p=_p(2 * stats.norm.sf(abs(d0 / s0))))
    return out


# ---------------------------- 稳健性 ----------------------------

BASE_X = ['post_A1', 'post_A2', 'post_B', 'post_AB']
KEYS = ['post_A', 'post_A1', 'post_A2', 'post_B', 'post_AB']


def baseline(df, y, ctrl=True):
    c = CTRL if ctrl else []
    r1 = _within(df, y, ['post_A', 'post_B', 'post_AB'] + c)
    r2 = _within(df, y, BASE_X + c)
    out = {k: _pick(r2, k) for k in BASE_X}
    out['post_A'] = _pick(r1, 'post_A')
    out['r2_within'] = round(r2['r2_within'], 4)
    idx = [r2['_names'].index(k) for k in ['post_A2', 'post_A1']]
    w = np.array([1.0, -1.0])
    b = float(w @ np.array([r2['coef']['post_A2'], r2['coef']['post_A1']]))
    V = r2['_V'][np.ix_(idx, idx)]
    se = float(np.sqrt(max(w @ V @ w, 0.0)))
    out['gen2_minus_gen1'] = dict(coef=round(b, 6), se=round(se, 6),
                                  z=round(b / se, 4),
                                  p=_p(2 * stats.norm.sf(abs(b / se))))
    return out


def robustness(df, y):
    out = {}
    out['full'] = {k: _pick(_within(df, y, BASE_X + CTRL), k) for k in BASE_X}
    # 1. 剔除各处理的首批城市（重庆／广州／成都所在批次）
    first = [min(A1_COH), min(A2_COH), min(B_COH)]
    drop = df.groupby('city')[['gA1', 'gA2', 'gB']].first()
    bad = set(drop.index[(drop['gA1'] == first[0]) | (drop['gA2'] == first[1])
                         | (drop['gB'] == first[2])])
    sub = df[~df['city'].isin(bad)]
    out['drop_first'] = {k: _pick(_within(sub, y, BASE_X + CTRL), k) for k in BASE_X}
    out['drop_first']['ncity_dropped'] = len(bad)
    # 2. 城市—月份双重聚类
    r = _within(df, y, BASE_X + CTRL, cluster2='month')
    out['twoway_cluster'] = {k: _pick(r, k) for k in BASE_X}
    # 3. 城市线性趋势
    d = df.copy()
    d['tt'] = d['month'] / 12.0
    codes = pd.factorize(d['city'])[0]
    T = np.zeros((len(d), codes.max() + 1))
    T[np.arange(len(d)), codes] = d['tt'].to_numpy()
    # 全部 200 条城市趋势之和等于时间趋势 t，与月份固定效应完全共线，
    # 故归一化掉第 1 个城市的趋势列（去掉后报告系数不变，见复核脚本）。
    trend_cols = ['tr%03d' % j for j in range(T.shape[1])]
    d = pd.concat([d.reset_index(drop=True),
                   pd.DataFrame(T, columns=trend_cols)], axis=1)
    trend_cols = trend_cols[1:]
    r = _within(d, y, BASE_X + CTRL + trend_cols)
    out['city_trend'] = {k: _pick(r, k) for k in BASE_X}
    out['city_trend']['ntrend'] = len(trend_cols)
    # 4. 省级聚类（按城市编号取模构造 31 个省份分组）
    d2 = df.copy()
    d2['prov'] = d2['city'] % 31
    dd = d2[[y] + BASE_X + CTRL + ['city', 'month', 'prov']].dropna()
    ci = pd.factorize(dd['city'])[0]
    ti = pd.factorize(dd['month'])[0]
    M = _absorb(dd[[y] + BASE_X + CTRL].to_numpy(float), [ci, ti], [ci.max() + 1, ti.max() + 1])
    pv = pd.factorize(dd['prov'])[0]
    rp = _fit(M[:, 0], M[:, 1:], BASE_X + CTRL, pv, kabs=ci.max() + ti.max() + 1)
    out['cluster_prov'] = {k: _pick(rp, k) for k in BASE_X}
    # 5. 不加控制变量
    out['nocontrol'] = {k: _pick(_within(df, y, BASE_X), k) for k in BASE_X}
    return out


# ---------------------------- 渠道识别（2SLS）----------------------------


def iv_channel(df, y, endog='mfi', inst=('post_A1', 'post_A2')):
    """以两代平台上线为工具变量，估计计量摩擦指数对结果变量的因果效应。

    排他性约束即本文的理论假设：统一计量平台只通过降低计量摩擦影响结果变量。
    两个工具构成过度识别，Hansen J 检验两代平台是否隐含同一结构参数。
    """
    exog = ['post_B', 'post_AB'] + CTRL
    cols = [y, endog] + list(inst) + exog
    dd = df[cols + ['city', 'month']].dropna()
    ci = pd.factorize(dd['city'])[0]
    ti = pd.factorize(dd['month'])[0]
    M = _absorb(dd[cols].to_numpy(float), [ci, ti], [ci.max() + 1, ti.max() + 1])
    Y = M[:, 0]
    D = M[:, 1:2]
    Z = M[:, 2:2 + len(inst)]
    W = M[:, 2 + len(inst):]
    kabs = ci.max() + ti.max() + 1
    # 第一阶段
    fs = _fit(D[:, 0], np.hstack([Z, W]), list(inst) + exog, ci, kabs=kabs)
    Fj = _wald(fs, list(inst))
    # 2SLS
    ZZ = np.hstack([Z, W])
    XX = np.hstack([D, W])
    P = ZZ @ np.linalg.pinv(ZZ.T @ ZZ) @ (ZZ.T @ XX)
    b = np.linalg.pinv(P.T @ XX) @ (P.T @ Y)
    u = Y - XX @ b
    A = np.linalg.pinv(P.T @ XX)
    g = int(ci.max()) + 1
    S = np.zeros((g, P.shape[1]))
    for j in range(P.shape[1]):
        S[:, j] = np.bincount(ci, weights=P[:, j] * u, minlength=g)
    n = len(Y)
    adj = g / max(g - 1, 1) * (n - 1) / max(n - XX.shape[1] - kabs, 1)
    V = A @ (S.T @ S * adj) @ A.T
    se = float(np.sqrt(max(V[0, 0], 0.0)))
    coef = float(b[0])
    z = coef / se if se > 0 else 0.0
    # Hansen J：以工具与残差的相关性构造
    gbar = np.zeros((g, Z.shape[1]))
    for j in range(Z.shape[1]):
        gbar[:, j] = np.bincount(ci, weights=Z[:, j] * u, minlength=g)
    gm = gbar.sum(axis=0)
    Om = gbar.T @ gbar
    J = float(gm @ np.linalg.pinv(Om) @ gm)
    dfJ = Z.shape[1] - 1
    return dict(coef=round(coef, 6), se=round(se, 6), t=round(z, 4),
                p=_p(2 * stats.norm.sf(abs(z))), n=int(n),
                ncluster=g, endog=endog, instruments=list(inst),
                first_stage={i: dict(coef=fs['coef'][i], se=fs['se'][i], t=fs['t'][i])
                             for i in inst},
                first_stage_F=round(Fj['wald'] / len(inst), 3),
                first_stage_p=Fj['p'],
                hansen_J=round(J, 4), hansen_df=dfJ,
                hansen_p=_p(stats.chi2.sf(J, dfJ)) if dfJ > 0 else None)


# ============================ 五、变量定义与描述统计 ============================

VARDEF = {
    'disp': ('本地智能服务真实价格离散度（变异系数）',
             '每城每月对 10 类代表性任务各采集 12 家可比供给方的质量折算后单价，'
             '先在任务内计算变异系数，再对任务取均值', '无量纲'),
    'disp_iqr': ('真实价格离散度（四分位距口径）',
                 '任务内 (P75−P25)/P50，再对任务取均值', '无量纲'),
    'spread': ('跨平台真实价差倍数', '任务内最高价与最低价之比，再对任务取均值', '倍'),
    'mfi': ('计量摩擦指数', '名义单价对数标准差与折算后单价对数标准差之差', '无量纲'),
    'adopt_sme': ('中小企业智能服务采纳率', '本地采购智能服务的中小企业占比', '比例'),
    'adopt_large': ('大企业智能服务采纳率', '本地采购智能服务的大企业占比', '比例'),
    'eta_bar': ('平均成交效值', '成交供给方的质量折算系数按成交额加权平均，中型通用档＝1',
                '无量纲'),
    'ln_token': ('本地词元调用量（对数）', '城市月度词元调用量取自然对数', 'ln(亿枚)'),
    'token_yi': ('本地词元调用量', '城市月度词元调用量', '亿枚'),
    'spend_per_call': ('单位调用支出', '城市月度智能服务支出除以调用次数', '元／次'),
    'ln_spend': ('单位调用支出（对数）', 'spend_per_call 取自然对数', 'ln(元／次)'),
    'lngdp': ('地区生产总值（对数）', '城市月度折算的地区生产总值取对数', 'ln(亿元)'),
    'lnpop': ('常住人口（对数）', '', 'ln(万人)'),
    'dig': ('数字经济发展指数', '', '0—100'),
    'ai_firm': ('人工智能企业密度', '每万户市场主体中的人工智能企业数', '家／万户'),
    'sme_share': ('中小企业占比', '城市企业规模结构', '比例'),
    'post_A': ('统一计量平台（处理 A）', '城市级统一计量结算平台上线当月及以后取 1', '0/1'),
    'post_A1': ('第一代平台（算力调度型）', '2024-11 起分批', '0/1'),
    'post_A2': ('第二代平台（词元计量型）', '2026-04 起分批', '0/1'),
    'post_B': ('价格补贴（处理 B）', '算力券／训力券／词元券实施当月及以后取 1', '0/1'),
    'post_AB': ('两套处理的交乘项', 'post_A × post_B', '0/1'),
}
DESC_VARS = list(VARDEF)


def describe(df):
    out = {}
    for v in DESC_VARS:
        if v not in df.columns:
            continue
        s = df[v].astype(float)
        lab, dfn, unit = VARDEF[v]
        out[v] = dict(label=lab, definition=dfn, unit=unit, n=int(s.notna().sum()),
                      mean=round(float(s.mean()), 4), sd=round(float(s.std()), 4),
                      p25=round(float(s.quantile(.25)), 4),
                      p50=round(float(s.median()), 4),
                      p75=round(float(s.quantile(.75)), 4),
                      min=round(float(s.min()), 4), max=round(float(s.max()), 4))
    return out


def fig_series(df, meta):
    """图 2：三组城市的价格离散度走势；另给出事件时间对齐的走势。"""
    g = df.groupby(['gen', 'month'])['disp'].mean().unstack(0)
    out = {'months': MONTHS,
           'never_A': [round(float(x), 5) for x in g[0]],
           'gen1': [round(float(x), 5) for x in g[1]],
           'gen2': [round(float(x), 5) for x in g[2]]}
    # 走势图必须用不随时间变化的分组，否则组内城市构成逐月变化（post_B=1 的城市
    # 由 6 个增至 88 个），组均值的变化里混入的是构成变动而不是处理效应。
    everB = df.groupby('city')['gB'].transform('first').notna()
    b = df.assign(everB=everB).groupby(['everB', 'month'])['spend_per_call'] \
          .mean().unstack(0)
    out['spend_neverB'] = [round(float(x), 6) for x in b[False]]
    out['spend_everB'] = [round(float(x), 6) for x in b[True]]
    out['spend_group_note'] = ('按“是否曾受补贴”分组（从未 %d 城、曾受 %d 城），'
                               '分组不随时间变化；竖线可标各批次上线月份。'
                               % (int((~everB).groupby(df['city']).first().sum()),
                                  int(everB.groupby(df['city']).first().sum())))
    st = meta['spread_task']
    pre = st[:, :min(A1_COH), :].ravel()
    out['spread_pre'] = dict(
        mean=round(float(pre.mean()), 3), p50=round(float(np.median(pre)), 3),
        p75=round(float(np.percentile(pre, 75)), 3),
        p90=round(float(np.percentile(pre, 90)), 3),
        p95=round(float(np.percentile(pre, 95)), 3),
        p99=round(float(np.percentile(pre, 99)), 3),
        share_ge_10x=round(float((pre >= SPREAD_ANCHOR).mean()), 4),
        note='2023-01—2024-10（任何统一计量平台上线之前）的城市—月—任务单元')
    out['national_daily_wanyi'] = [round(float(x), 4) for x in meta['nat_daily']]
    out['national_interp'] = [bool(x) for x in meta['interp_flag']]
    return out


# ============================ 六、主程序 ============================

YS = ['disp', 'disp_iqr', 'adopt_sme', 'adopt_large', 'eta_bar',
      'ln_token', 'spend_per_call', 'ln_spend', 'mfi']
EVENT_Y = ['disp', 'adopt_sme', 'adopt_large', 'eta_bar', 'ln_token', 'ln_spend']
ROBUST_Y = ['disp', 'disp_iqr', 'adopt_sme', 'eta_bar']


def main():
    df, meta = build_panel()
    df.to_csv(os.path.join(DATA, 'panel.csv'), index=False, encoding='utf-8-sig')

    gsize = df.groupby('grp')['city'].nunique().to_dict()
    cohorts = {
        'A1': {ymstr(k): int(v) for k, v in sorted(A1_COH.items())},
        'A2': {ymstr(k): int(v) for k, v in sorted(A2_COH.items())},
        'B': {ymstr(k): int(v) for k, v in sorted(B_COH.items())}}
    OUT = {
        'meta': dict(
            paper=2, seed=SEED, script='data_gen.py',
            note='城市层面成交价格与企业采纳明细不公开，分析样本按 data/facts.md 的'
                 '公开锚点校准生成；一切进入正文的数字均由本脚本产生。',
            deps='numpy/pandas/scipy'),
        'anchor': ANCHOR,
        'sample': dict(
            ncity=NCITY, nmonth=NT, nobs=int(len(df)),
            period=[MONTHS[0], MONTHS[-1]],
            n_plat=N_PLAT, n_task=N_TASK,
            cohorts=cohorts,
            named_cities={
                'A1': {c: ymstr(t) for c, t in NAMED_A1.items()},
                'A2': {c: ymstr(t) for c, t in NAMED_A2.items()},
                'B': {c: ymstr(t) for c, t in NAMED_B.items()}},
            named_note='仅对 facts.md 有公开记录的 13 个城市使用真实城市名，'
                       '其余 187 个城市匿名编号，处理时点按批次随机分配。'
                       '北京经开区词元工厂 2026-06-30 投产、国资词元工厂 2026-07-03 亮相，'
                       '月度面板归入 2026-07。',
            group_size={k: int(v) for k, v in gsize.items()},
            n_treated_A=int(gsize.get('onlyA', 0) + gsize.get('both', 0)),
            n_treated_B=int(gsize.get('onlyB', 0) + gsize.get('both', 0)),
            gen1_max_post=NT - min(A1_COH), gen2_max_post=NT - min(A2_COH),
            window_note='第二代平台后处理期最长仅 %d 个月，事件研究相对期上限取 +%d；'
                        '第一代最长 %d 个月，上限取 +%d（另给出 +12 的补充路径）。'
                        % (NT - min(A2_COH), EVWIN['A2'][1],
                           NT - min(A1_COH), EVWIN['A1'][1])),
        'par': {k: (round(float(v), 6) if isinstance(v, float) else v)
                for k, v in PAR.items()},
    }

    OUT['desc'] = describe(df)
    OUT['fig'] = fig_series(df, meta)

    print('--- 基准交错 DID ---')
    OUT['baseline'] = {}
    for y in YS:
        OUT['baseline'][y] = baseline(df, y)
        OUT['baseline'][y]['nocontrol'] = {
            k: _pick(_within(df, y, BASE_X), k) for k in BASE_X}
        b = OUT['baseline'][y]
        print('%-14s A %9.5f(t%6.2f)  A1 %9.5f  A2 %9.5f  B %9.5f(t%6.2f)'
              % (y, b['post_A']['coef'], b['post_A']['t'], b['post_A1']['coef'],
                 b['post_A2']['coef'], b['post_B']['coef'], b['post_B']['t']))

    print('--- 事件研究 ---')
    OUT['event'] = {}
    for y in EVENT_Y:
        OUT['event'][y] = {w: event_study(df, y, w) for w in ('A1', 'A2', 'B')}
        OUT['event'][y]['A1_long'] = event_study_long(df, y, hi=12)
        print('%-12s 事前联合 p: A1 %.3f  A2 %.3f  B %.3f' % (
            y, OUT['event'][y]['A1']['pretrend_joint']['p'],
            OUT['event'][y]['A2']['pretrend_joint']['p'],
            OUT['event'][y]['B']['pretrend_joint']['p']))

    print('--- 异质性稳健估计量 ---')
    SPEC = {'A1': ('kA1', 'gA1', EVWIN['A1'], ['post_A2', 'post_B']),
            'A2': ('kA2', 'gA2', EVWIN['A2'], ['post_A1', 'post_B']),
            'B': ('kB', 'gB', EVWIN['B'], ['post_A1', 'post_A2'])}
    OUT['cs'], OUT['sa'] = {}, {}
    for y in ['disp', 'adopt_sme', 'adopt_large', 'eta_bar', 'ln_token', 'ln_spend']:
        OUT['cs'][y], OUT['sa'][y] = {}, {}
        for w, (kc, gc, (lo, hi), oth) in SPEC.items():
            OUT['cs'][y][w] = callaway_santanna(df, y, gc, lo, hi)
            OUT['sa'][y][w] = sun_abraham(df, y, kc, gc, lo, hi, oth)
        # 稳健性：把对照组限定为从未受补贴的城市，排除补贴成分的污染
        OUT['cs'][y]['A2_neverB'] = callaway_santanna(
            df[df.grp.isin(['onlyA', 'none'])], y, 'gA2', *EVWIN['A2'])
        print('%-12s CS: A1 %8.5f A2 %8.5f B %8.5f | SA: A1 %8.5f A2 %8.5f B %8.5f'
              % (y, OUT['cs'][y]['A1']['att']['coef'], OUT['cs'][y]['A2']['att']['coef'],
                 OUT['cs'][y]['B']['att']['coef'], OUT['sa'][y]['A1']['att']['coef'],
                 OUT['sa'][y]['A2']['att']['coef'], OUT['sa'][y]['B']['att']['coef']))

    print('--- 安慰剂检验（500 次随机化处理时点）---')
    OUT['placebo'] = {}
    for y in ['disp', 'adopt_sme', 'eta_bar']:
        for w in ('A', 'B'):
            r = placebo(df, y, w, reps=500)
            OUT['placebo']['%s_%s' % (y, w)] = r
            print('%-12s %s  真实 %9.5f  安慰剂均值 %9.5f  sd %.5f  经验 p %.4f'
                  % (y, w, r['true'], r['mean'], r['sd'], r['p_two_sided']))

    print('--- 机制与制度成分分解 ---')
    OUT['mech'] = mech_decomp(df)
    for y in ['disp', 'adopt_sme', 'eta_bar', 'ln_spend']:
        r = OUT['mech']['by_y'][y]
        print('%-12s 仅补贴 %9.5f(t%6.2f)  仅计量 %9.5f(t%6.2f)  兼有合计 %9.5f  '
              '差异 z %5.2f' % (y, r['onlyB']['coef'], r['onlyB']['t'],
                              r['onlyA']['coef'], r['onlyA']['t'],
                              r['both']['total']['coef'], r['diff_A_minus_B']['z']))

    print('--- 异质性 ---')
    OUT['hetero'] = {}
    for y in ['disp', 'adopt_sme', 'eta_bar']:
        OUT['hetero'][y] = {
            'digital_base': hetero(df, y, 'zdig', '城市数字经济基础'),
            'firm_size': hetero(df, y, 'zsme', '企业规模结构（中小企业占比）')}
        for k in ('digital_base', 'firm_size'):
            h = OUT['hetero'][y][k]
            print('%-12s %-13s A2 高组 %9.5f  低组 %9.5f  差异 z %5.2f'
                  % (y, k, h['high']['post_A2']['coef'], h['low']['post_A2']['coef'],
                     h['diff']['post_A2']['z']))

    print('--- 稳健性 ---')
    OUT['robust'] = {y: robustness(df, y) for y in ROBUST_Y}
    for k in ['drop_first', 'twoway_cluster', 'city_trend', 'cluster_prov', 'nocontrol']:
        v = OUT['robust']['disp'][k]
        print('%-16s A1 %9.5f(t%6.2f)  A2 %9.5f(t%6.2f)  B %9.5f(t%6.2f)'
              % (k, v['post_A1']['coef'], v['post_A1']['t'], v['post_A2']['coef'],
                 v['post_A2']['t'], v['post_B']['coef'], v['post_B']['t']))

    print('--- 渠道识别：以平台上线为工具变量估计计量摩擦的因果效应 ---')
    OUT['channel'] = {'reduced_form_mfi': OUT['baseline']['mfi'], 'iv': {}}
    for y in ['disp', 'disp_iqr', 'adopt_sme', 'adopt_large', 'eta_bar',
              'ln_token', 'ln_spend']:
        r = iv_channel(df, y)
        OUT['channel']['iv'][y] = r
        print('%-12s d%s/d(mfi) %9.5f（se %.5f, t=%6.2f）  一阶段 F=%.1f  Hansen J p=%.3f'
              % (y, '', r['coef'], r['se'], r['t'], r['first_stage_F'], r['hansen_p']))

    OUT['checks'] = run_checks(OUT)
    with open(os.path.join(DATA, 'results.json'), 'w', encoding='utf-8') as f:
        json.dump(OUT, f, ensure_ascii=False, indent=1)
    write_spec(OUT)
    print('\n--- 自检 ---')
    for k, v in OUT['checks'].items():
        if k != 'all_pass':
            print(('  [√] ' if v['pass'] else '  [×] ') + k + '：' + v['msg'])
    print('全部通过：', OUT['checks']['all_pass'])
    print('\n已写出 data/results.json、data/RESULTS_SPEC.md、data/panel.csv；N =', len(df))
    return OUT


# ============================ 七、自检与速查表 ============================


def run_checks(O):
    ck = {}

    def add(k, ok, msg):
        ck[k] = dict(**{'pass': bool(ok)}, msg=msg)

    b = O['baseline']
    add('A_lowers_disp', b['disp']['post_A']['coef'] < 0 and b['disp']['post_A']['p'] < .05,
        '统一计量显著压降价格离散度：%.5f（t=%.2f）'
        % (b['disp']['post_A']['coef'], b['disp']['post_A']['t']))
    add('gen2_stronger', b['disp']['post_A2']['coef'] < b['disp']['post_A1']['coef'],
        '第二代（词元计量型）效应强于第一代：%.5f vs %.5f（差异 z=%.2f）'
        % (b['disp']['post_A2']['coef'], b['disp']['post_A1']['coef'],
           b['disp']['gen2_minus_gen1']['z']))
    add('B_no_variance', abs(b['disp']['post_B']['t']) < 1.96,
        '补贴不改变价格方差：%.5f（t=%.2f，不显著）'
        % (b['disp']['post_B']['coef'], b['disp']['post_B']['t']))
    add('B_moves_level', b['ln_spend']['post_B']['coef'] < 0 and b['ln_spend']['post_B']['p'] < .05,
        '补贴显著压低价格水平：ln 单位调用支出 %.5f（t=%.2f）'
        % (b['ln_spend']['post_B']['coef'], b['ln_spend']['post_B']['t']))
    add('sme_gt_large',
        b['adopt_sme']['post_A2']['coef'] > b['adopt_large']['post_A2']['coef'] > 0,
        '中小企业采纳效应大于大企业：%.5f vs %.5f（倍数 %.2f）'
        % (b['adopt_sme']['post_A2']['coef'], b['adopt_large']['post_A2']['coef'],
           b['adopt_sme']['post_A2']['coef'] / max(b['adopt_large']['post_A2']['coef'], 1e-9)))
    add('eta_up', b['eta_bar']['post_A']['coef'] > 0 and b['eta_bar']['post_A']['p'] < .05,
        '统一计量提高平均成交效值：%.5f（t=%.2f）'
        % (b['eta_bar']['post_A']['coef'], b['eta_bar']['post_A']['t']))
    add('eta_B_down', b['eta_bar']['post_B']['coef'] < 0,
        '仅补贴加剧逆向选择（效值下降）：%.5f（t=%.2f）'
        % (b['eta_bar']['post_B']['coef'], b['eta_bar']['post_B']['t']))
    add('token_up', b['ln_token']['post_A']['coef'] > 0 and b['ln_token']['post_B']['coef'] > 0,
        '两套处理都提高调用量：A %.5f、B %.5f'
        % (b['ln_token']['post_A']['coef'], b['ln_token']['post_B']['coef']))

    ps = [O['event'][y][w]['pretrend_joint']['p']
          for y in O['event'] for w in ('A1', 'A2', 'B')]
    add('pretrend', min(ps) > 0.05,
        '%d 组事件研究的事前联合检验最小 p 值 %.3f，均不能拒绝平行趋势'
        % (len(ps), min(ps)))

    pp = {k: v['p_two_sided'] for k, v in O['placebo'].items() if k.endswith('_A')}
    pmin = list(O['placebo'].values())[0]['p_min_attainable']
    add('placebo', max(pp.values()) < 0.05,
        '随机化处理时点 500 次，处理 A 的经验 p 值最大为 %.4f'
        '（蒙特卡洛 p 值取 (1+#)/(1+R)，500 次重排能达到的下界为 %.4f，'
        '不存在“恰好为零”的安慰剂 p 值）' % (max(pp.values()), pmin))

    # 只对 TWFE 已显著的格子比较符号与量级；TWFE 不显著的格子改查 CS／SA 是否同样不显著
    ok, det = True, []
    for y in ['disp', 'adopt_sme', 'eta_bar', 'ln_token']:
        for w in ('A1', 'A2', 'B'):
            tw = O['baseline'][y]['post_' + w]
            cs_, sa_ = O['cs'][y][w]['att'], O['sa'][y][w]['att']
            if tw['p'] < 0.05:
                good = (np.sign(cs_['coef']) == np.sign(tw['coef'])
                        and np.sign(sa_['coef']) == np.sign(tw['coef'])
                        and 0.4 <= abs(cs_['coef'] / tw['coef']) <= 2.5
                        and 0.4 <= abs(sa_['coef'] / tw['coef']) <= 2.5)
                tag = '同号同量级' if good else '不一致'
            else:
                good = cs_['p'] > 0.05 and sa_['p'] > 0.05
                tag = '三者同为不显著' if good else '不一致'
            ok = ok and good
            det.append('%s/%s %.4f|%.4f|%.4f（%s）'
                       % (y, w, tw['coef'], cs_['coef'], sa_['coef'], tag))
    add('cs_sa_consistent', ok,
        'CS 与 SA 的 ATT 与 TWFE 一致（TWFE|CS|SA）：' + '；'.join(det))

    m = O['mech']['by_y']
    add('mech_nonsub',
        m['disp']['diff_A_minus_B']['p'] < 0.05 and m['ln_spend']['diff_A_minus_B']['p'] < 0.05,
        '不可替代性：离散度上仅计量与仅补贴之差 z=%.2f（p=%.4f）；'
        '价格水平上二者之差 z=%.2f（p=%.4f）'
        % (m['disp']['diff_A_minus_B']['z'], m['disp']['diff_A_minus_B']['p'],
           m['ln_spend']['diff_A_minus_B']['z'], m['ln_spend']['diff_A_minus_B']['p']))
    add('mech_onlyB_disp_null', abs(m['disp']['onlyB']['t']) < 1.96,
        '仅补贴组的离散度效应不显著：%.5f（t=%.2f）'
        % (m['disp']['onlyB']['coef'], m['disp']['onlyB']['t']))

    h = O['hetero']['disp']['firm_size']
    add('hetero_sme', h['high']['post_A2']['coef'] < h['low']['post_A2']['coef'],
        '中小企业占比高的城市离散度压降更大：%.5f vs %.5f（z=%.2f）'
        % (h['high']['post_A2']['coef'], h['low']['post_A2']['coef'],
           h['diff']['post_A2']['z']))

    rb = O['robust']['disp']
    add('robust_gen2', all(rb[k]['post_A2']['coef'] < 0 and rb[k]['post_A2']['p'] < .05
                           for k in ['drop_first', 'twoway_cluster', 'city_trend',
                                     'cluster_prov', 'nocontrol']),
        '第二代平台的离散度效应在全部 5 项稳健性检验中保持负向显著')

    sp = O['fig']['spread_pre']
    add('spread_anchor', sp['p90'] <= SPREAD_ANCHOR <= sp['p99'],
        '事前跨平台真实价差：中位数 %.2f 倍、P90 %.2f 倍、P99 %.2f 倍，%.1f%% 的'
        '城市—月—任务单元达到或超过 10 倍，即公开报道的 10 倍落在本文分布的第 %d—%d 百分位。'
        '口径提示：facts.md 的 10 倍是“同一模型同一问题跨平台”的窄口径极值，'
        '本文的 spread 是同一任务上 12 家可比供给方之间的宽口径极差，'
        '后者本应更大，二者不是同一个对象，正文只做量级参照，不作等同引用'
        % (sp['p50'], sp['p90'], sp['p99'], 100 * sp['share_ge_10x'], 90, 99))

    # 分解恒等式：兼有组合计＝A＋B＋交乘；超可加＝合计−两者单独之和
    worst = 0.0
    for yy, r in O['mech']['by_y'].items():
        t3 = r['both']['total']['coef']
        s3 = r['both']['post_A']['coef'] + r['both']['post_B']['coef'] \
            + r['both']['post_AB']['coef']
        s2 = r['onlyA']['coef'] + r['onlyB']['coef']
        worst = max(worst, abs(t3 - s3), abs(r['superadd']['sum_separate'] - s2),
                    abs(r['superadd']['coef'] - (t3 - s2)),
                    abs(r['diff_A_minus_B']['coef']
                        - (r['onlyA']['coef'] - r['onlyB']['coef'])))
    add('decomp_identity', worst < 2e-6,
        '%d 个结果变量的分解恒等式全部成立（兼有组合计＝post_A＋post_B＋交乘；'
        '超可加项＝合计−两者单独效应之和），最大偏差 %.1e（仅舍入误差）'
        % (len(O['mech']['by_y']), worst))

    # 无事前期批次的处置：CS／SA／事件研究必须一致地整批剔除
    dr = {'CS': O['cs']['disp']['B']['ncity_dropped_nobase'],
          'SA': O['sa']['disp']['B']['ncity_dropped_nobase'],
          'ES': O['event']['disp']['B']['ncity_dropped_nobase']}
    add('nobase_cohort_dropped', len(set(dr.values())) == 1 and dr['CS'] > 0,
        '2023-01 批次的 %d 个补贴城市自样本首期即已受处理、无基期，'
        'CS／SA／事件研究一致整批剔除（该批次的群组×相对期哑变量与其城市固定效应'
        '完全共线，保留则只能靠伪逆给出无定义的最小范数解）；'
        '二值 TWFE 保留这些城市，但其 post_B 组内无变异，不参与识别'
        % dr['CS'])

    j = {k: v['hansen_p'] for k, v in O['channel']['iv'].items()}
    badj = [k for k, v in j.items() if v is not None and v < 0.05]
    add('iv_overid', len(badj) <= 1,
        '过度识别检验：%d 个结果变量中 %d 个在 5%% 水平上拒绝 Hansen J（%s）；'
        '拒绝者正文须如实报告并说明两代平台的排他性约束在该结果上不完全一致'
        % (len(j), len(badj), '、'.join(badj) if badj else '无'))

    ck['all_pass'] = all(v['pass'] for k, v in ck.items() if k != 'all_pass')
    return ck


def _fmt(d, nd=4):
    return '%.*f（%.*f）' % (nd, d['coef'], nd, d['se'])


def write_spec(O):
    b, m, L = O['baseline'], O['mech']['by_y'], []
    s = O['sample']
    ap = L.append
    ap('# results.json 速查表（论文二：计量摩擦、价格离散与智能服务市场发育）\n')
    ap('由 `data_gen.py` 自动生成，随脚本同步更新。**正文中一切数字只许引用本文件'
       '与 `data/facts.md`，不得手写。**括号内为城市层面聚类稳健标准误。\n')
    ap('- 样本：%d 个地级及以上城市 × %d 个月（%s—%s），共 %d 个观测。'
       % (s['ncity'], s['nmonth'], s['period'][0], s['period'][1], s['nobs']))
    ap('- 价格采集口径：每城每月对 %d 类代表性任务各采集 %d 家可比供给方的折算后单价。'
       % (s['n_task'], s['n_plat']))
    ap('- 处理 A（统一计量结算平台）覆盖 %d 城：第一代 %d 城（%s 起 %d 批）、'
       '第二代 %d 城（%s 起 %d 批）。'
       % (s['n_treated_A'], sum(s['cohorts']['A1'].values()),
          list(s['cohorts']['A1'])[0], len(s['cohorts']['A1']),
          sum(s['cohorts']['A2'].values()), list(s['cohorts']['A2'])[0],
          len(s['cohorts']['A2'])))
    ap('- 处理 B（算力券／训力券／词元券）覆盖 %d 城，%s 起 %d 批。'
       % (s['n_treated_B'], list(s['cohorts']['B'])[0], len(s['cohorts']['B'])))
    ap('- 四组城市：仅计量 %d、仅补贴 %d、两者兼有 %d、从未处理 %d。'
       % (s['group_size']['onlyA'], s['group_size']['onlyB'],
          s['group_size']['both'], s['group_size']['none']))
    ap('- **识别边界（正文须如实交代）**：%s\n' % s['window_note'])
    ap('- 城市名纪律：%s\n' % s['named_note'])

    ap('## 1. `sample` / `anchor` / `desc`（表 1：变量定义与描述统计）\n')
    ap('`desc[变量]` 含 label、definition、unit、n、mean、sd、p25、p50、p75、min、max。'
       '主要结果变量的均值（标准差）：\n')
    ap('| 变量 | 含义 | 单位 | 均值 | 标准差 | P25 | 中位数 | P75 |')
    ap('|---|---|---|---|---|---|---|---|')
    for v in ['disp', 'disp_iqr', 'spread', 'mfi', 'adopt_sme', 'adopt_large',
              'eta_bar', 'ln_token', 'spend_per_call', 'lngdp', 'lnpop', 'dig',
              'ai_firm', 'sme_share', 'post_A1', 'post_A2', 'post_B']:
        d = O['desc'][v]
        ap('| `%s` | %s | %s | %.4f | %.4f | %.4f | %.4f | %.4f |'
           % (v, d['label'], d['unit'], d['mean'], d['sd'], d['p25'], d['p50'], d['p75']))
    ap('\n**三条变量口径提示（写进表注，避免误读）**：')
    ap('1. `ln_token` 的城市值经过“各城之和恰等于当月全国调用量”的归一化，'
       '共同因子被月份固定效应吸收，因此其系数读作**相对份额效应**'
       '（处理城市相对于对照城市的调用量变化），不是全国总量的增量。')
    ap('2. `adopt_sme` 在下界 0.01 处有约 1.6%% 的删失观测（集中在 2023 年上半年'
       '采纳率极低的城市），线性模型的估计因而略偏保守。')
    ap('3. `spread`／`disp`／`mfi` 都是每城每月 10 类任务×12 家供给方报价的'
       '样本统计量，含抽样噪声；`mfi` 因此是带测量误差的代理变量，'
       '这正是机制识别改用工具变量而非直接回归的原因。\n')
    sp = O['fig']['spread_pre']
    ap('\n**价格离散度的现实锚**：事前（%s）同一任务上 12 家可比供给方之间的真实'
       '价差，中位数 **%.2f 倍**、P90 **%.2f 倍**、P99 **%.2f 倍**，'
       '**%.1f%%** 的城市—月—任务单元达到或超过 **10 倍**；'
       'facts.md 记录的 10 倍落在本文分布的 **P90—P99** 之间。'
       '**引用时须区分两个口径**：facts.md 的 10 倍是“同一模型、同一问题、'
       '跨平台”的窄口径极值（差异只来自计费规则与缓存让利），'
       '本文的 `spread` 是“同一任务、跨可比供给方”的宽口径极差，'
       '后者本应更大。正文只能写“量级参照”，不得把二者当作同一个统计量。'
       '（`fig.spread_pre`）\n'
       % ('2023-01—2024-10', sp['p50'], sp['p90'], sp['p99'], 100 * sp['share_ge_10x']))

    ap('## 2. `baseline`（表 2：基准交错双重差分）\n')
    ap('设定：$y_{it}=\\alpha_i+\\lambda_t+\\beta_1 A_{it}+\\beta_2 B_{it}'
       '+\\beta_3 A_{it}B_{it}+X_{it}\\gamma+\\varepsilon_{it}$，城市层面聚类。'
       '`post_A` 为合并档，`post_A1`／`post_A2` 为分代档（同一列内同时纳入）。\n')
    ap('| 结果变量 | post_A | post_A1（第一代） | post_A2（第二代） | post_B | post_A×post_B |')
    ap('|---|---|---|---|---|---|')
    for y in YS:
        d = b[y]
        ap('| `%s` | %s | %s | %s | %s | %s |'
           % (y, _fmt(d['post_A']), _fmt(d['post_A1']), _fmt(d['post_A2']),
              _fmt(d['post_B']), _fmt(d['post_AB'])))
    ap('\n第二代与第一代之差（离散度）：%s，z=%.2f，p=%.4f。'
       % (_fmt(b['disp']['gen2_minus_gen1']), b['disp']['gen2_minus_gen1']['z'],
          b['disp']['gen2_minus_gen1']['p']))
    ap('`baseline[y]["nocontrol"]` 为不加控制变量的对照列。\n')

    ap('## 3. `event`（图 3：事件研究）\n')
    ap('`event[y][{A1,A2,B}]`：`window`、`base`(=−1)、`coefs[相对期]`、'
       '`pretrend_joint`（事前系数联合 Wald）、`post_joint`。'
       '第一代另有 `A1_long`（相对期至 +12）。**第二代上限只能到 +%d**。\n'
       % EVWIN['A2'][1])
    ap('**两条口径必须写进图注，不得让读者按字面理解**：')
    _neg = lambda v: ('\u2212%d' % -v) if v < 0 else ('%d' % v)   # 负号用 U+2212
    ap('1. `binned_ends = true`：窗口两端为**归并档**——`window[0]` 的系数是'
       '“相对期 ≤ %s”而非恰好第 %s 期，`window[1]` 的系数是“相对期 ≥ %s”。'
       '第二代的 %s 档吸收了处理前的绝大多数月份，因此事前联合检验读作'
       '“处理前的水平差与 %s 期无系统差异”，而不是逐月的斜率检验。'
       % (_neg(EVWIN['A2'][0]), _neg(EVWIN['A2'][0]), _neg(EVWIN['A2'][1]),
          _neg(EVWIN['A2'][0]), _neg(BASEK)))
    ap('2. `ncity_dropped_nobase`：**无事前期的批次整批剔除**。'
       '2023-01 批次的 %d 个补贴城市自样本首期即已受处理，没有基期 k=−1；'
       '其群组×相对期哑变量之和恒为 1、与该批城市的固定效应完全共线。'
       'CS、SA 与事件研究一律剔除这些城市（二值 TWFE 保留，但它们的 post_B '
       '组内无变异、不参与识别）。\n'
       % O['event']['disp']['B']['ncity_dropped_nobase'])
    ap('| 结果变量 | A1 事前联合 p | A2 事前联合 p | B 事前联合 p |')
    ap('|---|---|---|---|')
    for y in EVENT_Y:
        e = O['event'][y]
        ap('| `%s` | %.3f | %.3f | %.3f |' % (
            y, e['A1']['pretrend_joint']['p'], e['A2']['pretrend_joint']['p'],
            e['B']['pretrend_joint']['p']))
    ap('')

    ap('## 4. `cs` / `sa`（表 3：异质性处理效应稳健估计）\n')
    ap('`cs` 为 Callaway & Sant\'Anna（2021）群组—时期 ATT（比较组为尚未处理城市，'
       '方差按城市层面影响函数聚合）；`sa` 为 Sun & Abraham（2021）交互加权估计。'
       '各含 `att`（事后总体）、`pre`（事前聚合）、`by_event`。'
       '`cs[y]["A2_neverB"]` 把对照组限定为从未受补贴的城市。\n')
    ap('| 结果变量 | 处理 | TWFE | CS ATT | SA ATT | CS 事前 | SA 事前 |')
    ap('|---|---|---|---|---|---|---|')
    for y in ['disp', 'adopt_sme', 'eta_bar', 'ln_token']:
        for w in ('A1', 'A2', 'B'):
            ap('| `%s` | %s | %s | %s | %s | %s | %s |'
               % (y, w, _fmt(b[y]['post_' + w]), _fmt(O['cs'][y][w]['att']),
                  _fmt(O['sa'][y][w]['att']), _fmt(O['cs'][y][w]['pre']),
                  _fmt(O['sa'][y][w]['pre'])))
    ap('')

    ap('## 5. `placebo`（图 4：安慰剂检验）\n')
    ap('保持各批次城市数不变、把批次标签在城市间随机重排，重复 500 次。'
       '含 `true`、`mean`、`sd`、`p_two_sided`、`q95_abs`、`q99_abs`、`pct`、`draws`（500 个系数）。\n')
    ap('| 结果变量 | 处理 | 真实系数 | 安慰剂均值 | 安慰剂 sd | \\|安慰剂\\| 的 95 分位 | 经验 p |')
    ap('|---|---|---|---|---|---|---|')
    for k, v in O['placebo'].items():
        ap('| `%s` | %s | %.5f | %.5f | %.5f | %.5f | %.4f |'
           % (k.rsplit('_', 1)[0], k.rsplit('_', 1)[1], v['true'], v['mean'],
              v['sd'], v['q95_abs'], v['p_two_sided']))
    ap('')

    ap('## 6. `mech` / `channel`（表 4：机制与制度成分分解）——本文的核心命题\n')
    ap('把样本分成三组，各自以从未处理城市为对照：`onlyB`（仅补贴）、'
       '`onlyA`（仅计量）、`both`（两者兼有，报告 post_A／post_B／交乘及 `total` 合计）。'
       '`diff_A_minus_B` 检验二者效应之差，`superadd` 检验兼有组合计效应与'
       '两者单独效应之和的差（互补性）。\n')
    ap('> 口径提示：`diff_A_minus_B` 与 `superadd` 的标准误按两个子样本相互独立计算，'
       '而这两个子回归共用“从未处理”对照组、协方差为正，'
       '故该标准误**偏保守**（真实标准误更小、显著性只会更强），'
       '正文按保守值报告。\n')
    ap('| 结果变量 | 仅补贴 | 仅计量 | 兼有（合计） | 仅计量−仅补贴（z） |')
    ap('|---|---|---|---|---|')
    for y in MECH_Y:
        r = m[y]
        ap('| `%s` | %s | %s | %s | %.2f |'
           % (y, _fmt(r['onlyB']), _fmt(r['onlyA']), _fmt(r['both']['total']),
              r['diff_A_minus_B']['z']))
    ap('\n**可检验含义的三条对照**：')
    ap('1. 离散度：仅补贴 %.5f（t=%.2f，不显著）、仅计量 %.5f（t=%.2f），'
       '差异 z=%.2f、p=%.4f —— **补贴不降低价格方差，统一计量降低**。'
       % (m['disp']['onlyB']['coef'], m['disp']['onlyB']['t'],
          m['disp']['onlyA']['coef'], m['disp']['onlyA']['t'],
          m['disp']['diff_A_minus_B']['z'], m['disp']['diff_A_minus_B']['p']))
    ap('2. 价格水平：仅补贴对 ln 单位调用支出 %.5f（t=%.2f）、仅计量 %.5f（t=%.2f），'
       '差异 z=%.2f、p=%.4f —— **补贴移动价格水平，统一计量不移动**。'
       % (m['ln_spend']['onlyB']['coef'], m['ln_spend']['onlyB']['t'],
          m['ln_spend']['onlyA']['coef'], m['ln_spend']['onlyA']['t'],
          m['ln_spend']['diff_A_minus_B']['z'], m['ln_spend']['diff_A_minus_B']['p']))
    ap('3. 平均成交效值：仅补贴 %.5f（t=%.2f）、仅计量 %.5f（t=%.2f）—— '
       '**仅补贴而不统一计量时逆向选择渠道不被关闭，效值反而下降**。\n'
       % (m['eta_bar']['onlyB']['coef'], m['eta_bar']['onlyB']['t'],
          m['eta_bar']['onlyA']['coef'], m['eta_bar']['onlyA']['t']))
    ap('`channel`：以两代平台上线为工具变量、计量摩擦指数 `mfi` 为内生变量的两阶段'
       '最小二乘。排他性约束即本文理论假设——统一计量只通过降低计量摩擦影响结果变量；'
       '两个工具构成过度识别，Hansen J 检验两代平台是否隐含同一结构参数。'
       '`channel.reduced_form_mfi` 为 mfi 的简约式（第一阶段）结果。\n')
    ap('| 结果变量 | 计量摩擦的因果效应 d·/d(mfi) | t | 一阶段 F | Hansen J 的 p |')
    ap('|---|---|---|---|---|')
    for y, v in O['channel']['iv'].items():
        ap('| `%s` | %s | %.2f | %.1f | %.3f |'
           % (y, _fmt(v), v['t'], v['first_stage_F'], v['hansen_p']))
    _bad = [k for k, v in O['channel']['iv'].items()
            if v['hansen_p'] is not None and v['hansen_p'] < 0.05]
    ap('\n> **过度识别检验须如实报告**：%s。'
       '拒绝意味着两代平台在该结果变量上并不隐含同一个结构参数，'
       '正文应把它读作“两代平台的作用渠道不完全相同”，'
       '而不是回避不报。\n'
       % ('%s 的 Hansen J 在 5%% 水平上被拒绝（p=%.3f）'
          % ('、'.join('`%s`' % k for k in _bad),
             O['channel']['iv'][_bad[0]]['hansen_p'])
          if _bad else '全部结果变量均不能拒绝过度识别约束'))
    ap('\n计量摩擦指数本身的简约式：post_A1 %s、post_A2 %s、post_B %s'
       '（补贴不改变计量摩擦，这正是两种政策成分不可替代的直接证据）。\n'
       % (_fmt(b['mfi']['post_A1']), _fmt(b['mfi']['post_A2']),
          _fmt(b['mfi']['post_B'])))

    ap('## 7. `hetero`（异质性）\n')
    ap('按城市固定特征的中位数分组：`digital_base`（数字经济基础）、'
       '`firm_size`（企业规模结构，中小企业占比）。各含 `high`／`low`／`diff`。\n')
    ap('| 结果变量 | 分组维度 | 高组 post_A2 | 低组 post_A2 | 差异 z | p |')
    ap('|---|---|---|---|---|---|')
    for y, dd in O['hetero'].items():
        for k, h in dd.items():
            ap('| `%s` | %s | %s | %s | %.2f | %.4f |'
               % (y, h['label'], _fmt(h['high']['post_A2']),
                  _fmt(h['low']['post_A2']), h['diff']['post_A2']['z'],
                  h['diff']['post_A2']['p']))
    ap('')

    ap('## 8. `robust`（表 5：稳健性）\n')
    ap('五列：`drop_first`（剔除重庆／广州／成都所在首批城市）、'
       '`twoway_cluster`（城市—月份双重聚类）、`city_trend`（加入城市线性时间趋势，'
       '归一化掉 1 条冗余趋势列以消除与月份固定效应的完全共线）、'
       '`cluster_prov`（省级聚类）、`nocontrol`（不加控制变量）；'
       '`disp_iqr` 一行即“更换离散度指标为四分位距”。\n')
    ap('> **`cluster_prov` 的口径必须在表注写明**：模拟面板的 187 个匿名城市没有'
       '真实省份归属，省份是按城市编号取模构造的 31 个**合成分组**，'
       '该列只用于说明“把聚类层级放粗到 31 组时推断如何变化”，'
       '不得表述为“按真实省份聚类”。\n')
    ap('| 结果变量 | 设定 | post_A1 | post_A2 | post_B |')
    ap('|---|---|---|---|---|')
    for y in ROBUST_Y:
        for k in ['full', 'drop_first', 'twoway_cluster', 'city_trend',
                  'cluster_prov', 'nocontrol']:
            v = O['robust'][y][k]
            ap('| `%s` | %s | %s | %s | %s |'
               % (y, k, _fmt(v['post_A1']), _fmt(v['post_A2']), _fmt(v['post_B'])))
    _nsig = sum(1 for k in ['full', 'drop_first', 'twoway_cluster', 'city_trend',
                            'cluster_prov', 'nocontrol']
                if O['robust']['disp'][k]['post_B']['p'] < 0.05)
    ap('\n> **须如实交代的一处不齐整**：补贴对离散度的系数在 6 个设定里有 %d 个'
       '在 5%% 水平上显著（%s），其余不显著；`disp_iqr` 在加入城市线性趋势时'
       '甚至转为正向显著。正文的写法应是“补贴对价格方差没有稳定的压降效应”，'
       '而不是“补贴对价格方差的效应精确为零”——后者既不是数据说的话，'
       '也会让读者怀疑结果被修饰过。\n'
       % (_nsig, '、'.join(k for k in ['full', 'drop_first', 'twoway_cluster',
                                       'city_trend', 'cluster_prov', 'nocontrol']
                           if O['robust']['disp'][k]['post_B']['p'] < 0.05) or '无'))

    ap('## 9. `fig`（图 2、图 4 的绘图数据）\n')
    ap('- `fig.months`：44 个月份标签；`fig.never_A`／`gen1`／`gen2`：三组城市的'
       '离散度月度均值（图 2）。分组按“是否曾上线平台、第几代”，不随时间变化。')
    ap('- `fig.spend_neverB`／`spend_everB`：**从未受补贴／曾受补贴**城市的单位调用'
       '支出月度均值（`fig.spend_group_note` 记录两组城市数）。这里必须用'
       '“是否曾受补贴”这一不随时间变化的分组：若按当期 post_B 分组，'
       '组内城市数将由 6 个逐月增至 88 个，组均值的变化里混进的是构成变动而非处理效应。')
    ap('- `fig.national_daily_wanyi`：全国日均词元调用量（万亿枚／日）；'
       '`fig.national_interp` 为 True 的点系插值或外推，图注须注明，'
       '官方锚点仅 %s。**2024-01 之前的取值是按 2024-01→2025-06 那段极陡增速'
       '向后外推的结果（2023-01 折合 %.4f 万亿枚／日），只用于给面板一个'
       '起点量级，不得当作事实引用；2026-04 之后为增速逐月递减的向前外推。**'
       % ('、'.join(O['anchor']['national_daily_tokens_wanyi']),
          O['fig']['national_daily_wanyi'][0]))
    ap('- `placebo[*].draws`：安慰剂系数 500 个（图 4 直方图），'
       '竖线位置取 `true`。\n')
    ap('其余顶层键：`meta`（论文号、随机种子 %d、依赖）、`anchor`（facts.md 公开锚点，'
       '不得改动）、`par`（数据生成的结构参数，供复核校准逻辑）。\n' % O['meta']['seed'])

    ap('## 10. `checks`（脚本自检，交付前须全部为真）\n')
    for k, v in O['checks'].items():
        if k == 'all_pass':
            continue
        ap('- **%s**：%s %s' % (k, '通过' if v['pass'] else '未通过', v['msg']))
    ap('\n`checks.all_pass = %s`\n' % O['checks']['all_pass'])

    with open(os.path.join(DATA, 'RESULTS_SPEC.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))


if __name__ == '__main__':
    main()
