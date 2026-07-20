# -*- coding: utf-8 -*-
"""生成全部分析图（nature 风格，matplotlib）。章节编号命名。"""
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from figstyle import save, PAL, SERIES, REGION_C, CJK
from matplotlib.ticker import MaxNLocator

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)
df = pd.read_csv(os.path.join(HERE, 'data', 'panel.csv'))
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))
YEARS = sorted(df.year.unique())


def yrs(d):
    return [int(k) for k in d], [d[k] for k in d]


# ============================ 第3章 典型事实 ============================
def fig3_gdp_urban():
    yr = list(range(2012, 2025))
    gdp = [51.93, 57.76, 64.36, 68.89, 74.64, 83.20, 91.93, 98.65, 101.36, 114.92, 120.47, 129.43, 134.91]
    urb = [52.57, 53.73, 54.77, 56.10, 57.35, 58.52, 59.58, 60.60, 63.89, 64.72, 65.22, 66.16, 67.00]
    fig, ax1 = plt.subplots(figsize=(6.4, 3.6))
    b = ax1.bar(yr, gdp, color=PAL['ltblue'], width=0.6, label='国内生产总值')
    ax1.set_ylabel('国内生产总值（万亿元）', color=PAL['blue'])
    ax1.set_xlabel('年份')
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)
    ax2.plot(yr, urb, color=PAL['orange'], marker='o', ms=4, lw=1.8, label='常住人口城镇化率')
    ax2.set_ylabel('城镇化率（%）', color=PAL['orange'])
    ax2.grid(False)
    ax1.set_xticks(yr[::2])
    fig.legend(loc='upper left', bbox_to_anchor=(0.13, 0.96), fontsize=8)
    save(fig, f'{FIG}/fig3_1.png')


def fig3_digital():
    yr = [2012, 2016, 2020, 2021, 2022, 2023]
    scale = [11.0, 22.6, 39.2, 45.5, 50.2, 53.9]
    share = [21.6, 30.3, 38.6, 39.8, 41.5, 42.8]
    fig, ax1 = plt.subplots(figsize=(6.0, 3.6))
    ax1.bar(range(len(yr)), scale, color=PAL['teal'], width=0.55)
    ax1.set_xticks(range(len(yr)))
    ax1.set_xticklabels(yr)
    ax1.set_ylabel('数字经济规模（万亿元）', color=PAL['teal'])
    ax1.set_xlabel('年份')
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)
    ax2.plot(range(len(yr)), share, color=PAL['red'], marker='s', ms=5, lw=1.8)
    ax2.set_ylabel('占GDP比重（%）', color=PAL['red'])
    ax2.grid(False)
    for i, s in enumerate(share):
        ax2.annotate(f'{s}%', (i, s), textcoords='offset points', xytext=(0, 7),
                     ha='center', fontsize=7, color=PAL['red'])
    save(fig, f'{FIG}/fig3_2.png')


def fig3_regional_gap():
    prov = ['北京', '上海', '江苏', '福建', '浙江', '广东', '湖北', '内蒙古', '全国',
            '四川', '河南', '广西', '黑龙江', '云南', '贵州', '甘肃']
    pgdp = [22.8, 21.6, 15.8, 13.4, 13.5, 10.6, 9.5, 10.1, 9.5, 7.2, 6.6, 5.5, 5.0, 6.4, 5.6, 5.3]
    colors = [PAL['blue'] if p != '全国' else PAL['gray'] for p in prov]
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    ax.bar(range(len(prov)), pgdp, color=colors, width=0.68)
    ax.set_xticks(range(len(prov)))
    ax.set_xticklabels(prov, rotation=55, ha='right', fontsize=7.5)
    ax.set_ylabel('人均GDP（万元）')
    ax.axhline(9.5, color=PAL['red'], ls='--', lw=1, alpha=0.7)
    ax.annotate('全国平均', (len(prov) - 1, 9.5), fontsize=7, color=PAL['red'], va='bottom', ha='right')
    save(fig, f'{FIG}/fig3_3.png')


def fig3_entities():
    yr = list(range(2013, 2025))
    ent = [0.61, 0.69, 0.78, 0.87, 0.98, 1.10, 1.23, 1.39, 1.54, 1.69, 1.84, 1.89]
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.fill_between(yr, ent, color=PAL['ltblue'], alpha=0.5)
    ax.plot(yr, ent, color=PAL['blue'], marker='o', ms=4, lw=1.8)
    ax.set_ylabel('登记在册经营主体（亿户）')
    ax.set_xlabel('年份')
    ax.set_xticks(yr[::2])
    save(fig, f'{FIG}/fig3_4.png')


# ============================ 第5章 NUMI 测度 ============================
def fig5_numi_national():
    x, y = yrs(R['numi_national'])
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(x, y, color=PAL['blue'], marker='o', ms=4, lw=2)
    ax.fill_between(x, y, min(y) - 0.02, color=PAL['ltblue'], alpha=0.25)
    for yy, lab in [(2013, '十八大'), (2020, '要素市场化\n配置意见'), (2022, '统一大市场\n《意见》')]:
        ax.axvline(yy, color=PAL['gray'], ls=':', lw=1)
        ax.annotate(lab, (yy, min(y)), fontsize=6.8, color=PAL['gray'], ha='center', va='bottom')
    ax.set_ylabel('全国统一大市场建设指数（NUMI）')
    ax.set_xlabel('年份')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=8))
    save(fig, f'{FIG}/fig5_2.png')


def fig5_numi_region():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for reg in ['东部', '中部', '西部', '东北']:
        x, y = yrs(R['numi_by_region'][reg])
        ax.plot(x, y, marker='o', ms=3, lw=1.7, color=REGION_C[reg], label=reg)
    ax.set_ylabel('NUMI')
    ax.set_xlabel('年份')
    ax.legend(ncol=4, loc='upper left', fontsize=8)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=8))
    save(fig, f'{FIG}/fig5_3.png')


def fig5_radar():
    dims = ['d_goods', 'd_labor', 'd_capital', 'd_land', 'd_tech', 'd_inst']
    labs = ['商品市场', '劳动力市场', '资本市场', '土地市场', '技术数据', '制度环境']
    v06 = [R['numi_dims'][d]['2006'] for d in dims]
    v23 = [R['numi_dims'][d]['2023'] for d in dims]
    ang = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
    ang += ang[:1]
    v06 += v06[:1]
    v23 += v23[:1]
    fig, ax = plt.subplots(figsize=(4.8, 4.6), subplot_kw=dict(polar=True))
    ax.plot(ang, v06, color=PAL['gray'], lw=1.8, label='2006年')
    ax.fill(ang, v06, color=PAL['gray'], alpha=0.12)
    ax.plot(ang, v23, color=PAL['blue'], lw=2, label='2023年')
    ax.fill(ang, v23, color=PAL['blue'], alpha=0.18)
    ax.set_xticks(ang[:-1])
    ax.set_xticklabels(labs, fontsize=8.5)
    ax.set_ylim(0, 0.85)
    ax.grid(alpha=0.4)
    ax.legend(loc='upper right', bbox_to_anchor=(1.22, 1.12), fontsize=8)
    save(fig, f'{FIG}/fig5_4.png')


def fig5_rank():
    rk = R['numi_2023_rank']
    prov = [r[0] for r in rk]
    val = [r[2] for r in rk]
    col = [REGION_C.get(r[1], PAL['gray']) for r in rk]
    fig, ax = plt.subplots(figsize=(5.6, 6.8))
    y = range(len(prov))
    ax.barh(y, val, color=col, height=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels(prov, fontsize=7.5)
    ax.invert_yaxis()
    ax.set_xlabel('2023年 NUMI')
    ax.legend(handles=[Patch(color=REGION_C[r], label=r) for r in ['东部', '中部', '西部', '东北']],
              loc='lower right', fontsize=7.5)
    save(fig, f'{FIG}/fig5_5.png')


def fig5_seg():
    x, y = yrs(R['seg_national'])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(x, y, color=PAL['red'], marker='v', ms=4, lw=1.9)
    ax.fill_between(x, y, color=PAL['red'], alpha=0.12)
    ax.set_ylabel('国内市场分割指数（相对价格法）')
    ax.set_xlabel('年份')
    ax.annotate('市场一体化程度提高', (x[len(x)//2], y[len(y)//2]),
                textcoords='offset points', xytext=(20, 25), fontsize=8,
                arrowprops=dict(arrowstyle='->', color=PAL['gray']))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=8))
    save(fig, f'{FIG}/fig5_6.png')


def fig5_kde():
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    from scipy.stats import gaussian_kde
    for yy, c, lab in [(2006, PAL['gray'], '2006年'), (2013, PAL['teal'], '2013年'),
                       (2023, PAL['blue'], '2023年')]:
        d = df[df.year == yy].numi.values
        kde = gaussian_kde(d)
        xs = np.linspace(0.1, 1.0, 200)
        ax.plot(xs, kde(xs), color=c, lw=1.9, label=lab)
        ax.fill_between(xs, kde(xs), color=c, alpha=0.08)
    ax.set_xlabel('NUMI')
    ax.set_ylabel('核密度')
    ax.legend(fontsize=8)
    save(fig, f'{FIG}/fig5_7.png')


# ============================ 第6章 错配 ============================
def fig6_mis():
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    capital = [df[df.year == y].miscap.mean() for y in YEARS]
    labor = [df[df.year == y].mislab.mean() for y in YEARS]
    ax.plot(YEARS, capital, color=PAL['blue'], marker='o', ms=3, lw=1.8, label='资本错配')
    ax.plot(YEARS, labor, color=PAL['orange'], marker='s', ms=3, lw=1.8, label='劳动力错配')
    ax.set_ylabel('要素错配程度（对数楔子离散度）')
    ax.set_xlabel('年份')
    ax.legend(fontsize=8)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=8))
    save(fig, f'{FIG}/fig6_1.png')


def fig6_tfploss():
    x, y = yrs(R['tfp_loss'])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(x, y, color=PAL['gold'], width=0.6, alpha=0.85)
    ax.set_ylabel('消除要素错配的反事实TFP提升（%）')
    ax.set_xlabel('年份')
    ax.axhline(np.mean(y), color=PAL['red'], ls='--', lw=1)
    ax.set_xticks(x[::2])
    save(fig, f'{FIG}/fig6_2.png')


def fig6_scatter():
    d23 = df[df.year == 2023]
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    sc = ax.scatter(d23.numi, d23.mismean, c=[REGION_C.get(r, PAL['gray']) for r in d23.region],
                    s=28, alpha=0.85, edgecolor='white', lw=0.5)
    z = np.polyfit(d23.numi, d23.mismean, 1)
    xs = np.linspace(d23.numi.min(), d23.numi.max(), 50)
    ax.plot(xs, np.polyval(z, xs), color=PAL['red'], lw=1.6, ls='--')
    ax.set_xlabel('NUMI（2023年）')
    ax.set_ylabel('要素错配程度')
    ax.legend(handles=[Patch(color=REGION_C[r], label=r) for r in ['东部', '中部', '西部', '东北']],
              fontsize=7.5, loc='upper right')
    save(fig, f'{FIG}/fig6_3.png')


def fig6_ace():
    x, y = yrs(R['ace_national'])
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(x, y, color=PAL['green'], marker='o', ms=4, lw=1.9)
    ax.fill_between(x, y, min(y) - 0.02, color=PAL['green'], alpha=0.12)
    ax.set_ylabel('要素配置效率（ACE）')
    ax.set_xlabel('年份')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=8))
    save(fig, f'{FIG}/fig6_4.png')


# ============================ 第7章 基准 ============================
def fig7_binscatter():
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    # 双向去均值后 binscatter
    d = df.copy()
    for c in ['numi', 'ace']:
        d[c + '_dm'] = (d[c] - d.groupby('prov')[c].transform('mean')
                        - d.groupby('year')[c].transform('mean') + d[c].mean())
    d['bin'] = pd.qcut(d['numi_dm'], 20, labels=False)
    g = d.groupby('bin').agg(x=('numi_dm', 'mean'), y=('ace_dm', 'mean'))
    ax.scatter(g.x, g.y, color=PAL['blue'], s=30, alpha=0.85)
    z = np.polyfit(d['numi_dm'], d['ace_dm'], 1)
    xs = np.linspace(g.x.min(), g.x.max(), 50)
    ax.plot(xs, np.polyval(z, xs), color=PAL['red'], lw=1.7)
    ax.set_xlabel('NUMI（双向固定效应去均值）')
    ax.set_ylabel('要素配置效率（去均值）')
    b = R['baseline']['m3']['numi']
    ax.annotate(f"斜率={b['coef']:.3f} (t={b['t']:.1f})", (0.05, 0.9),
                xycoords='axes fraction', fontsize=8.5)
    save(fig, f'{FIG}/fig7_1.png')


def fig7_coefplot():
    specs = ['m1', 'm2', 'm3']
    labs = ['(1) 仅核心变量', '(2) 加基础控制', '(3) 全部控制']
    co = [R['baseline'][s]['numi']['coef'] for s in specs]
    se = [R['baseline'][s]['numi']['se'] for s in specs]
    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    y = range(len(specs))
    ax.errorbar(co, y, xerr=[1.96 * s for s in se], fmt='o', color=PAL['blue'],
                ecolor=PAL['gray'], capsize=3, ms=6)
    ax.set_yticks(y)
    ax.set_yticklabels(labs)
    ax.axvline(0, color=PAL['red'], ls='--', lw=1)
    ax.set_xlabel('NUMI 对配置效率的估计系数（95%置信区间）')
    save(fig, f'{FIG}/fig7_2.png')


# ============================ 第8章 机制/异质性 ============================
def fig8_dims():
    dims = ['d_goods', 'd_labor', 'd_capital', 'd_land', 'd_tech', 'd_inst']
    labs = ['商品\n市场', '劳动力\n市场', '资本\n市场', '土地\n市场', '技术\n数据', '制度\n环境']
    co = [R['dim_reg'][d][d]['coef'] for d in dims]
    se = [R['dim_reg'][d][d]['se'] for d in dims]
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.bar(range(len(dims)), co, yerr=[1.96 * s for s in se], color=SERIES,
           capsize=3, width=0.62, alpha=0.9)
    ax.set_xticks(range(len(dims)))
    ax.set_xticklabels(labs, fontsize=8)
    ax.set_ylabel('对配置效率的估计系数')
    save(fig, f'{FIG}/fig8_2.png')


def fig8_mech():
    items = [('要素流动', R['mechanism']['numi_flow']['numi']),
             ('企业进入', R['mechanism']['numi_entry']['numi']),
             ('创新产出', R['mechanism']['numi_innov']['numi']),
             ('错配下降', R['mechanism']['numi_mis']['numi'])]
    labs = [i[0] for i in items]
    co = [i[1]['coef'] for i in items]
    se = [i[1]['se'] for i in items]
    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    colors = [PAL['blue'], PAL['teal'], PAL['green'], PAL['orange']]
    ax.barh(range(len(labs)), co, xerr=[1.96 * s for s in se], color=colors,
            capsize=3, height=0.6)
    ax.set_yticks(range(len(labs)))
    ax.set_yticklabels(labs)
    ax.axvline(0, color=PAL['red'], ls='--', lw=1)
    ax.set_xlabel('NUMI 对各中介变量的估计系数')
    save(fig, f'{FIG}/fig8_3.png')


def fig8_het():
    groups = [('东部', R['heterogeneity']['东部']), ('中部', R['heterogeneity']['中部']),
              ('西部', R['heterogeneity']['西部']), ('低分割组', R['heterogeneity']['low_seg']),
              ('高分割组', R['heterogeneity']['high_seg'])]
    labs = [g[0] for g in groups]
    co = [g[1]['numi']['coef'] for g in groups]
    se = [g[1]['numi']['se'] for g in groups]
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    cols = [PAL['blue'], PAL['orange'], PAL['red'], PAL['ltblue'], PAL['purple']]
    ax.errorbar(co, range(len(labs)), xerr=[1.96 * s for s in se], fmt='o',
                color=PAL['blue'], ecolor=PAL['gray'], capsize=3, ms=6)
    for i, c in enumerate(cols):
        ax.plot(co[i], i, 'o', color=c, ms=7)
    ax.set_yticks(range(len(labs)))
    ax.set_yticklabels(labs)
    ax.set_xlabel('分组估计系数（95%置信区间）')
    save(fig, f'{FIG}/fig8_4.png')


# ============================ 第9章 DID/拓展 ============================
def fig9_event():
    es = R['event_study']
    xs = sorted(int(y) for y in es)
    co = [es[str(y)]['coef'] for y in xs]
    se = [es[str(y)]['se'] for y in xs]
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.errorbar(xs, co, yerr=[1.96 * s for s in se], fmt='o-', color=PAL['blue'],
                ecolor=PAL['gray'], capsize=2.5, ms=4, lw=1.4)
    ax.axhline(0, color='black', lw=0.8)
    ax.axvline(2021.5, color=PAL['red'], ls='--', lw=1.2)
    ax.annotate('2022《意见》', (2021.6, max(co) * 0.8), fontsize=8, color=PAL['red'])
    ax.set_xlabel('年份')
    ax.set_ylabel('动态处理效应（相对2021年）')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=8))
    save(fig, f'{FIG}/fig9_1.png')


def fig9_convergence():
    sigma = [np.std(np.log(df[df.year == y].tfp)) for y in YEARS]
    numi_cv = [df[df.year == y].numi.std() / df[df.year == y].numi.mean() for y in YEARS]
    fig, ax1 = plt.subplots(figsize=(6.2, 3.5))
    ax1.plot(YEARS, sigma, color=PAL['blue'], marker='o', ms=3, lw=1.8, label='TFP对数标准差（σ收敛）')
    ax1.set_ylabel('地区TFP离散度', color=PAL['blue'])
    ax1.set_xlabel('年份')
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)
    ax2.plot(YEARS, numi_cv, color=PAL['orange'], marker='s', ms=3, lw=1.6, label='NUMI变异系数')
    ax2.set_ylabel('NUMI地区差异（变异系数）', color=PAL['orange'])
    ax2.grid(False)
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.96), fontsize=7.5)
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=8))
    save(fig, f'{FIG}/fig9_3.png')


def fig9_tfp_innov():
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    items = [('全要素生产率', R['extended']['tfp']['numi']),
             ('创新产出', R['extended']['innov']['numi'])]
    labs = [i[0] for i in items]
    co = [i[1]['coef'] for i in items]
    se = [i[1]['se'] for i in items]
    ax.bar(range(len(labs)), co, yerr=[1.96 * s for s in se], color=[PAL['blue'], PAL['green']],
           capsize=4, width=0.5, alpha=0.9)
    ax.set_xticks(range(len(labs)))
    ax.set_xticklabels(labs)
    ax.set_ylabel('NUMI 的估计系数')
    save(fig, f'{FIG}/fig9_2.png')


if __name__ == '__main__':
    fns = [fig3_gdp_urban, fig3_digital, fig3_regional_gap, fig3_entities,
           fig5_numi_national, fig5_numi_region, fig5_radar, fig5_rank, fig5_seg, fig5_kde,
           fig6_mis, fig6_tfploss, fig6_scatter, fig6_ace,
           fig7_binscatter, fig7_coefplot, fig8_dims, fig8_mech, fig8_het,
           fig9_event, fig9_convergence, fig9_tfp_innov]
    for f in fns:
        f()
        print('ok', f.__name__)
    print('done, figures in', FIG)
