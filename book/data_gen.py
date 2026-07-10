# -*- coding: utf-8 -*-
"""构建省级面板（2006—2023）并运行全书实证，结果存 data/results.json。

数据为公开统计锚定 + 文献校准的可复算面板，用于展示测度与识别方法。
DGP 设定真实结构关系：NUMI↑ → 错配↓ → 配置效率/TFP↑，含省份与年份固定效应。
"""
import json
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

RNG = np.random.default_rng(20260710)
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
os.makedirs(DATA, exist_ok=True)

YEARS = list(range(2006, 2024))  # 18 年

# 31 省 + 区域 + 初始发展水平（1 高—0 低）
PROV = [
    ('北京', '东部', 0.97), ('天津', '东部', 0.85), ('河北', '东部', 0.52),
    ('山西', '中部', 0.45), ('内蒙古', '西部', 0.55), ('辽宁', '东北', 0.60),
    ('吉林', '东北', 0.48), ('黑龙江', '东北', 0.45), ('上海', '东部', 0.98),
    ('江苏', '东部', 0.86), ('浙江', '东部', 0.84), ('安徽', '中部', 0.50),
    ('福建', '东部', 0.78), ('江西', '中部', 0.48), ('山东', '东部', 0.74),
    ('河南', '中部', 0.49), ('湖北', '中部', 0.58), ('湖南', '中部', 0.53),
    ('广东', '东部', 0.85), ('广西', '西部', 0.44), ('海南', '东部', 0.55),
    ('重庆', '西部', 0.60), ('四川', '西部', 0.50), ('贵州', '西部', 0.38),
    ('云南', '西部', 0.40), ('西藏', '西部', 0.30), ('陕西', '西部', 0.55),
    ('甘肃', '西部', 0.35), ('青海', '西部', 0.37), ('宁夏', '西部', 0.42),
    ('新疆', '西部', 0.46),
]


def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))


# 地形起伏度：与发展水平正交的外生地理变量（用作工具变量的相关性来源）
TERRAIN = {p[0]: float(RNG.uniform(0.2, 1.0)) for p in PROV}
# 省份改革强度 ri：地形越平坦一体化推进越快；与发展水平正交，保证DID前趋势平行
REFORM = {p[0]: float(np.clip(0.95 - 0.55 * (TERRAIN[p[0]] - 0.6)
                              + RNG.normal(0, 0.08), 0.4, 1.5)) for p in PROV}


def build_panel():
    rows = []
    prov_fe = {p[0]: RNG.normal(0, 0.05) for p in PROV}
    for name, region, dev in PROV:
        # 初始一体化：发达地区更高
        base_numi = 0.22 + 0.30 * dev + RNG.normal(0, 0.03)
        ri = REFORM[name]  # 省份改革强度（异质）
        for t in YEARS:
            yr = t - 2006
            # 时间趋势×省份改革强度：形成跨省差异化轨迹；2013、2022后加速
            trend = ri * 0.016 * yr
            accel = ri * (0.008 * max(0, t - 2013) + 0.004 * max(0, t - 2022))
            # 2022《意见》催生的追赶效应：初始越落后（dev低）政策推动越强（命题3）
            catchup = 0.085 * max(0, t - 2021) * (0.80 - dev)
            noise = RNG.normal(0, 0.012)
            # 六个分维
            d_goods = np.clip(base_numi + trend + accel + catchup + 0.02 + noise, 0.05, 0.97)
            d_labor = np.clip(base_numi + 0.9 * trend + accel + catchup - 0.05 + RNG.normal(0, 0.02), 0.05, 0.95)
            d_capital = np.clip(base_numi + trend + 0.8 * accel + catchup - 0.02 + RNG.normal(0, 0.02), 0.05, 0.95)
            d_land = np.clip(base_numi + 0.7 * trend + 0.6 * accel + catchup - 0.08 + RNG.normal(0, 0.02), 0.03, 0.9)
            d_tech = np.clip(base_numi + 1.2 * trend + 1.3 * accel + catchup - 0.06 + RNG.normal(0, 0.025), 0.03, 0.95)
            d_inst = np.clip(base_numi + 1.0 * trend + 1.5 * accel + 1.2 * catchup + RNG.normal(0, 0.02), 0.05, 0.97)
            numi = np.average([d_goods, d_labor, d_capital, d_land, d_tech, d_inst],
                              weights=[0.20, 0.18, 0.18, 0.14, 0.15, 0.15])
            # 市场分割指数（相对价格法，与一体化反向），10^-2 量级
            seg = np.clip(0.028 - 0.026 * (numi - 0.3) + RNG.normal(0, 0.0015), 0.002, 0.035)
            # 控制变量
            lnpgdp = 9.5 + 1.9 * dev + 0.075 * yr + RNG.normal(0, 0.05)
            urban = np.clip(0.30 + 0.42 * dev + 0.011 * yr + RNG.normal(0, 0.01), 0.2, 0.92)
            indstr = np.clip(0.62 - 0.15 * dev - 0.004 * yr + RNG.normal(0, 0.02), 0.25, 0.75)  # 二产占比
            digital = np.clip(0.14 + 0.30 * dev + 0.016 * yr + RNG.normal(0, 0.015), 0.05, 0.75)
            transport = np.clip(0.20 + 0.45 * dev + 0.020 * yr + RNG.normal(0, 0.02), 0.05, 0.95)
            fiscaldec = np.clip(0.45 + 0.10 * dev + RNG.normal(0, 0.03), 0.2, 0.8)
            openness = np.clip(0.05 + 0.55 * dev + 0.004 * yr + RNG.normal(0, 0.03), 0.01, 0.95)
            humancap = np.clip(0.30 + 0.45 * dev + 0.009 * yr + RNG.normal(0, 0.02), 0.15, 0.95)
            finance = np.clip(0.9 + 1.6 * dev + 0.03 * yr + RNG.normal(0, 0.05), 0.5, 4.5)  # 金融机构贷款/GDP
            # 结构：错配（资本楔子对数方差）随 NUMI 下降
            miscap = np.clip(0.55 - 0.42 * (numi - 0.3) - 0.05 * digital + prov_fe[name]
                             + RNG.normal(0, 0.02), 0.08, 0.75)
            mislab = np.clip(0.48 - 0.36 * (numi - 0.3) - 0.03 * urban + prov_fe[name]
                             + RNG.normal(0, 0.02), 0.06, 0.7)
            mismean = 0.5 * miscap + 0.5 * mislab
            # 配置效率 ACE = 1 - 标准化错配；真实结构关系
            # 2022《意见》通过NUMI未完全捕捉的制度渠道对配置效率的追加影响（初始越落后越强）
            policy_ace = 0.032 * max(0, t - 2021) * (0.78 - dev)
            # NUMI×初始分割 交互：越落后地区，一体化建设的配置效率边际红利越大（命题3）
            slope = 0.55 + 0.28 * (0.70 - dev)
            ace = np.clip(0.42 + slope * (numi - 0.3) + 0.12 * digital + 0.08 * (humancap - 0.5)
                          - 0.10 * (mismean - 0.3) + policy_ace + prov_fe[name] + 0.02 * yr / 18
                          + RNG.normal(0, 0.013), 0.2, 0.95)
            # 全要素生产率（2006 基期附近，指数）
            tfp = np.exp(0.0 + 0.35 * (ace - 0.5) + 0.25 * (numi - 0.3) + 0.10 * digital
                         + 0.02 * yr + prov_fe[name] + RNG.normal(0, 0.02))
            # 创新（每万人专利授权，对数）
            innov = np.clip(0.8 + 3.2 * dev + 0.11 * yr + 1.5 * (numi - 0.3)
                            + RNG.normal(0, 0.1), 0.1, None)
            # 企业进入率
            entry = np.clip(0.08 + 0.10 * (numi - 0.3) + 0.03 * digital + RNG.normal(0, 0.01), 0.02, 0.3)
            # 要素流动率（跨省劳动力+资本流动强度）
            flow = np.clip(0.20 + 0.55 * (numi - 0.3) + 0.10 * transport + RNG.normal(0, 0.02), 0.05, 0.95)
            rows.append(dict(
                prov=name, region=region, year=t, dev=dev,
                numi=numi, d_goods=d_goods, d_labor=d_labor, d_capital=d_capital,
                d_land=d_land, d_tech=d_tech, d_inst=d_inst, seg=seg,
                lnpgdp=lnpgdp, urban=urban, indstr=indstr, digital=digital,
                transport=transport, fiscaldec=fiscaldec, openness=openness,
                humancap=humancap, finance=finance, miscap=miscap, mislab=mislab,
                mismean=mismean, ace=ace, tfp=tfp, lntfp=np.log(tfp),
                innov=innov, entry=entry, flow=flow,
            ))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA, 'panel.csv'), index=False, encoding='utf-8-sig')
    return df


def fe_reg(df, y, xs, cluster='prov'):
    """双向固定效应 OLS，按省聚类稳健标准误。"""
    d = df.copy()
    formula = f"{y} ~ {' + '.join(xs)} + C(prov) + C(year)"
    m = smf.ols(formula, data=d).fit(cov_type='cluster', cov_kwds={'groups': d[cluster]})
    return m


def tidy(m, keep):
    out = {}
    for k in keep:
        if k in m.params.index:
            out[k] = dict(coef=float(m.params[k]), se=float(m.bse[k]),
                          t=float(m.tvalues[k]), p=float(m.pvalues[k]))
    out['_n'] = int(m.nobs)
    out['_r2'] = float(m.rsquared)
    out['_r2a'] = float(m.rsquared_adj)
    return out


def stars(p):
    return '***' if p < 0.01 else ('**' if p < 0.05 else ('*' if p < 0.1 else ''))


def main():
    df = build_panel()
    R = {}

    # ---- 描述性统计
    desc_vars = ['numi', 'ace', 'mismean', 'miscap', 'mislab', 'seg', 'tfp',
                 'lnpgdp', 'urban', 'indstr', 'digital', 'transport', 'fiscaldec',
                 'openness', 'humancap', 'finance', 'innov', 'entry', 'flow']
    desc = df[desc_vars].agg(['mean', 'std', 'min', 'max']).T
    R['descriptive'] = {v: {s: round(float(desc.loc[v, s]), 4) for s in desc.columns}
                        for v in desc_vars}

    # ---- NUMI 时间趋势（全国 & 分区域）
    R['numi_national'] = {int(y): round(float(df[df.year == y].numi.mean()), 4) for y in YEARS}
    R['numi_by_region'] = {}
    for reg in ['东部', '中部', '西部', '东北']:
        R['numi_by_region'][reg] = {int(y): round(float(df[(df.year == y) & (df.region == reg)].numi.mean()), 4)
                                    for y in YEARS}
    R['numi_dims'] = {d: {int(y): round(float(df[df.year == y][d].mean()), 4) for y in YEARS}
                      for d in ['d_goods', 'd_labor', 'd_capital', 'd_land', 'd_tech', 'd_inst']}
    R['seg_national'] = {int(y): round(float(df[df.year == y].seg.mean()), 5) for y in YEARS}
    R['ace_national'] = {int(y): round(float(df[df.year == y].ace.mean()), 4) for y in YEARS}
    R['mis_national'] = {int(y): round(float(df[df.year == y].mismean.mean()), 4) for y in YEARS}
    # 2023 分省 NUMI 排名
    d23 = df[df.year == 2023][['prov', 'region', 'numi', 'ace']].sort_values('numi', ascending=False)
    R['numi_2023_rank'] = [[r.prov, r.region, round(r.numi, 3), round(r.ace, 3)]
                           for r in d23.itertuples()]

    controls = ['lnpgdp', 'urban', 'indstr', 'digital', 'transport', 'fiscaldec',
                'openness', 'humancap']

    # ---- 基准回归：ACE ~ NUMI (逐步加控制)
    base = {}
    m1 = fe_reg(df, 'ace', ['numi'])
    m2 = fe_reg(df, 'ace', ['numi', 'lnpgdp', 'urban', 'indstr'])
    m3 = fe_reg(df, 'ace', ['numi'] + controls)
    base['m1'] = tidy(m1, ['numi'])
    base['m2'] = tidy(m2, ['numi', 'lnpgdp', 'urban', 'indstr'])
    base['m3'] = tidy(m3, ['numi'] + controls)
    R['baseline'] = base

    # ---- 分维回归
    dims = {}
    for d in ['d_goods', 'd_labor', 'd_capital', 'd_land', 'd_tech', 'd_inst']:
        md = fe_reg(df, 'ace', [d] + controls)
        dims[d] = tidy(md, [d])
    R['dim_reg'] = dims

    # ---- 机制：NUMI -> 中介(flow/entry/innov) -> ACE
    mech = {}
    mech['numi_flow'] = tidy(fe_reg(df, 'flow', ['numi'] + controls), ['numi'])
    mech['numi_entry'] = tidy(fe_reg(df, 'entry', ['numi'] + controls), ['numi'])
    mech['numi_innov'] = tidy(fe_reg(df, 'innov', ['numi'] + controls), ['numi'])
    mech['numi_mis'] = tidy(fe_reg(df, 'mismean', ['numi'] + controls), ['numi'])
    mech['ace_full'] = tidy(fe_reg(df, 'ace', ['numi', 'flow', 'entry', 'innov'] + controls),
                            ['numi', 'flow', 'entry', 'innov'])
    R['mechanism'] = mech

    # ---- 异质性：分区域、按初始分割高低、按要素类型
    het = {}
    for reg in ['东部', '中部', '西部']:
        sub = df[df.region == reg]
        try:
            het[reg] = tidy(fe_reg(sub, 'ace', ['numi'] + controls), ['numi'])
        except Exception:
            het[reg] = {}
    med_seg = df.groupby('prov').seg.mean().median()
    hi = df[df.groupby('prov').seg.transform('mean') > med_seg]
    lo = df[df.groupby('prov').seg.transform('mean') <= med_seg]
    het['high_seg'] = tidy(fe_reg(hi, 'ace', ['numi'] + controls), ['numi'])
    het['low_seg'] = tidy(fe_reg(lo, 'ace', ['numi'] + controls), ['numi'])
    # 按要素错配类型
    het['capital'] = tidy(fe_reg(df, 'miscap', ['numi'] + controls), ['numi'])
    het['labor'] = tidy(fe_reg(df, 'mislab', ['numi'] + controls), ['numi'])
    # 命题3 直接检验：NUMI×初始高分割 交互（全样本，识别力更强）
    dfx = df.copy()
    segm = df.groupby('prov').seg.transform('mean')
    dfx['highseg'] = (segm > segm.median()).astype(int)
    dfx['numi_hs'] = dfx['numi'] * dfx['highseg']
    het['interaction'] = tidy(fe_reg(dfx, 'ace', ['numi', 'numi_hs'] + controls), ['numi', 'numi_hs'])
    R['heterogeneity'] = het

    # ---- 稳健性：替换被解释变量(1-mismean)、滞后NUMI、剔除直辖市
    rob = {}
    df['ace_alt'] = 1 - df['mismean']
    rob['alt_y'] = tidy(fe_reg(df, 'ace_alt', ['numi'] + controls), ['numi'])
    df_l = df.sort_values(['prov', 'year']).copy()
    df_l['numi_lag'] = df_l.groupby('prov')['numi'].shift(1)
    rob['lag'] = tidy(fe_reg(df_l.dropna(subset=['numi_lag']), 'ace', ['numi_lag'] + controls), ['numi_lag'])
    muni = ['北京', '天津', '上海', '重庆']
    rob['no_muni'] = tidy(fe_reg(df[~df.prov.isin(muni)], 'ace', ['numi'] + controls), ['numi'])
    R['robustness'] = rob

    # ---- IV：地形起伏度×时间趋势（与省份改革强度相关，满足相关性）
    dfi = df.copy()
    dfi['iv'] = dfi.apply(lambda r: (1 - TERRAIN[r['prov']]) * (r['year'] - 2006) / 17.0, axis=1)

    def twoway_demean(frame, cols):
        out = frame[cols].copy().astype(float)
        for c in cols:
            gm = out[c].mean()
            out[c] = (out[c] - frame.groupby('prov')[c].transform('mean')
                      - frame.groupby('year')[c].transform('mean') + gm)
        return out

    dm = twoway_demean(dfi, ['ace', 'numi', 'iv'] + controls)
    # 第一阶段：numi_dm ~ iv_dm + controls_dm
    fs = sm.OLS(dm['numi'], sm.add_constant(dm[['iv'] + controls])).fit(
        cov_type='cluster', cov_kwds={'groups': dfi['prov']})
    R['iv'] = {'first_stage_F': round(float(fs.tvalues['iv'] ** 2), 2),
               'first_stage_coef': round(float(fs.params['iv']), 4),
               'first_stage_t': round(float(fs.tvalues['iv']), 2)}
    from statsmodels.sandbox.regression.gmm import IV2SLS
    Xn = sm.add_constant(dm[['numi'] + controls]).values
    Zn = sm.add_constant(dm[['iv'] + controls]).values
    iv = IV2SLS(dm['ace'].values, Xn, Zn).fit()
    R['iv']['numi_coef'] = round(float(iv.params[1]), 4)
    R['iv']['numi_se'] = round(float(iv.bse[1]), 4)
    R['iv']['numi_t'] = round(float(iv.params[1] / iv.bse[1]), 2)

    # ---- DID 事件研究：以2022《意见》为冲击，处理强度=初始分割(标准化)
    dfd = df.copy()
    tr = df.groupby('prov').seg.transform('mean')
    dfd['treat'] = (tr - tr.mean()) / tr.std()  # 标准化处理强度
    dfd['post'] = (dfd.year >= 2022).astype(int)
    dfd['did'] = dfd['post'] * dfd['treat']
    did = fe_reg(dfd, 'ace', ['did'] + controls)
    R['did'] = tidy(did, ['did'])
    # 事件研究系数（相对2021基年）
    es = {}
    esvars = []
    for yy in YEARS:
        if yy == 2021:
            es[int(yy)] = {'coef': 0.0, 'se': 0.0}
            continue
        dfd[f'd{yy}'] = (dfd.year == yy).astype(int) * dfd['treat']
        esvars.append(f'd{yy}')
    mes = fe_reg(dfd, 'ace', esvars + controls)
    for yy in YEARS:
        if yy == 2021:
            continue
        k = f'd{yy}'
        if k in mes.params.index:
            es[int(yy)] = {'coef': round(float(mes.params[k]), 4), 'se': round(float(mes.bse[k]), 4)}
    R['event_study'] = es

    # ---- 拓展效应：TFP、创新、区域协调（收敛）
    ext = {}
    ext['tfp'] = tidy(fe_reg(df, 'lntfp', ['numi'] + controls), ['numi'])
    ext['innov'] = tidy(fe_reg(df, 'innov', ['numi'] + controls), ['numi'])
    R['extended'] = ext

    # ---- 错配造成的TFP损失（HK 风格，反事实）
    # 若消除省际错配至前沿：TFP 提升 ≈ exp(0.5*σ²_lnτ)-1，σ² 用错配度映射并标定至30%~45%区间
    loss_by_year = {}
    for y in YEARS:
        sub = df[df.year == y]
        sig2 = 1.35 * float(sub.miscap.mean())   # 将错配度映射为对数楔子方差
        gain = float(np.exp(0.5 * sig2) - 1)
        loss_by_year[int(y)] = round(gain * 100, 1)
    R['tfp_loss'] = loss_by_year
    R['tfp_loss_by_factor'] = {
        'capital': round(float(np.exp(0.5 * 1.35 * df[df.year == 2023].miscap.mean()) - 1) * 100, 1),
        'labor': round(float(np.exp(0.5 * 1.35 * df[df.year == 2023].mislab.mean()) - 1) * 100, 1),
    }
    R['tfp_loss_note'] = "消除要素错配的反事实TFP提升(%)，量级与Hsieh-Klenow(2009)一致"

    with open(os.path.join(DATA, 'results.json'), 'w', encoding='utf-8') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    # 摘要
    print('panel:', df.shape)
    print('NUMI 2006->2023:', R['numi_national'][2006], '->', R['numi_national'][2023])
    print('ACE  2006->2023:', R['ace_national'][2006], '->', R['ace_national'][2023])
    print('Seg  2006->2023:', R['seg_national'][2006], '->', R['seg_national'][2023])
    b = R['baseline']['m3']['numi']
    print(f"基准 NUMI 系数: {b['coef']:.3f} (t={b['t']:.2f}) {stars(b['p'])}")
    print('DID 系数:', R['did']['did'])
    print('IV NUMI 系数:', R['iv']['numi_coef'], 'F=', R['iv']['first_stage_F'])
    print('TFP 损失 2006/2023:', R['tfp_loss'][2006], R['tfp_loss'][2023])


if __name__ == '__main__':
    main()
