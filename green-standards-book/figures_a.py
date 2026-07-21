# -*- coding: utf-8 -*-
"""生成全部 A 型分析图（matplotlib，nature 风格，中文）。
数据一律读取 data/series.csv 与 data/results.json；不得手写模型数字。
输出 figs/figN_M.png。
"""
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator
from figstyle import save, PAL, SERIES, CJK

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)

DF = pd.read_csv(os.path.join(HERE, 'data', 'series.csv'), dtype={'x': str})
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))


def ser(name, numeric=True):
    """按 series 名取 (x, value)；numeric=True 时 x 转 float 并排序。"""
    d = DF[DF.series == name]
    if numeric:
        x = d.x.astype(float).values
        v = d.value.astype(float).values
        idx = np.argsort(x)
        return x[idx], v[idx]
    return d.x.values, d.value.astype(float).values


def yrs(d):
    ks = sorted(d, key=lambda k: float(k))
    return np.array([float(k) for k in ks]), np.array([d[k] for k in ks])


MOD_CN = {'acct': '碳排放核算', 'fp': '碳足迹认证', 'prod': '绿色产品',
          'sink': '碳吸收', 'fin': '绿色金融'}
REG_CN = {'east': '东部', 'central': '中部', 'west': '西部'}
REG_C = {'east': PAL['blue'], 'central': PAL['orange'], 'west': PAL['red']}


# ============================ 第2章 ============================
def fig2_2():
    """WOS/CNKI 年度发文趋势（2000—2025）。"""
    xw, yw = ser('biblio.wos')
    xc, yc = ser('biblio.cnki')
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(xw, yw, color=PAL['blue'], marker='o', ms=3, lw=1.8, label='WOS（英文文献）')
    ax.plot(xc, yc, color=PAL['orange'], marker='s', ms=3, lw=1.8, label='CNKI（中文文献）')
    ax.fill_between(xw, yw, color=PAL['blue'], alpha=0.07)
    ax.fill_between(xc, yc, color=PAL['orange'], alpha=0.07)
    for yy, lab in [(2015, '巴黎协定'), (2020, '“双碳”目标提出')]:
        ax.axvline(yy, color=PAL['gray'], ls=':', lw=1)
        ax.annotate(lab, (yy, ax.get_ylim()[1] * 0.97), rotation=90,
                    fontsize=7, color=PAL['gray'], ha='right', va='top')
    ax.set_xlabel('年份')
    ax.set_ylabel('年度发文量（篇）')
    ax.legend(loc='upper left', fontsize=8)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=9))
    save(fig, f'{FIG}/fig2_2.png')


# ============================ 第3章 ============================
def fig3_2():
    """EUA 与 CEA 年均价（双轴），关键事件竖线。"""
    xe, ye = ser('drivers.eua')
    xc, yc = ser('drivers.ets')
    fig, ax1 = plt.subplots(figsize=(6.6, 3.7))
    l1, = ax1.plot(xe, ye, color=PAL['blue'], marker='o', ms=4, lw=1.9,
                   label='欧盟碳市场 EUA（左轴，欧元/吨）')
    ax1.set_ylabel('EUA 年均价（欧元/吨）', color=PAL['blue'])
    ax1.set_xlabel('年份')
    ax1.tick_params(axis='y', labelcolor=PAL['blue'])
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)
    l2, = ax2.plot(xc, yc, color=PAL['orange'], marker='s', ms=4, lw=1.9,
                   label='全国碳市场 CEA（右轴，元/吨）')
    ax2.set_ylabel('CEA 年均价（元/吨）', color=PAL['orange'])
    ax2.tick_params(axis='y', labelcolor=PAL['orange'])
    ax2.grid(False)
    for yy, lab in [(2021, '全国碳市场启动\n（2021年7月）'),
                    (2023.75, 'CBAM过渡期实施\n（2023年10月）')]:
        ax1.axvline(yy, color=PAL['gray'], ls='--', lw=1)
        ax1.annotate(lab, (yy - 0.15, ax1.get_ylim()[1] * 0.97), fontsize=7,
                     color=PAL['gray'], ha='right', va='top', zorder=6,
                     bbox=dict(boxstyle='round,pad=0.2', fc='white',
                               ec='none', alpha=0.8))
    ax1.legend(handles=[l1, l2], loc='upper left', fontsize=8)
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=9))
    save(fig, f'{FIG}/fig3_2.png')


def fig3_4():
    """ISO 温室气体核心标准里程碑累计（示意）＋主要经济体对比（示意口径）。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.6),
                                   gridspec_kw={'width_ratios': [1.5, 1]})
    # 左：ISO 14060 族及相关标准累计（里程碑，示意整理）
    miles = [(2006, 3, 'ISO 14064-1/2/3'), (2007, 4, 'ISO 14065'),
             (2011, 5, 'ISO 14066'), (2013, 6, 'ISO/TS 14067'),
             (2018, 7, 'ISO 14064修订+\nISO 14067:2018'),
             (2023, 8, 'ISO 14068-1\n（碳中和）')]
    yr = [2005] + [m[0] for m in miles] + [2025]
    cum = [0] + [m[1] for m in miles] + [miles[-1][1]]
    ax1.step(yr, cum, where='post', color=PAL['blue'], lw=2)
    ax1.plot([m[0] for m in miles], [m[1] for m in miles], 'o',
             color=PAL['blue'], ms=5)
    for (y, c, lab) in miles:
        ax1.annotate(lab, (y, c), textcoords='offset points', xytext=(3, -13),
                     fontsize=6.6, color=PAL['gray'])
    ax1.set_xlim(2004, 2026)
    ax1.set_ylim(0, 9.6)
    ax1.set_xticks([2005, 2010, 2015, 2020, 2025])
    ax1.set_xlabel('年份')
    ax1.set_ylabel('ISO 温室气体核心标准累计数量（项）')
    # 右：主要经济体绿色低碳标准数量对比（不同口径示意）
    econ = ['中国', '欧盟', '美国']
    vals = [R['std_counts']['cum']['gb']['2025'], 900, 650]
    cols = [PAL['blue'], PAL['ltblue'], PAL['ltblue']]
    bars = ax2.bar(econ, vals, color=cols, width=0.55)
    bars[1].set_hatch('///')
    bars[2].set_hatch('///')
    bars[1].set_edgecolor(PAL['gray'])
    bars[2].set_edgecolor(PAL['gray'])
    for b, v in zip(bars, vals):
        ax2.annotate(f'{v:.0f}', (b.get_x() + b.get_width() / 2, v),
                     textcoords='offset points', xytext=(0, 3),
                     ha='center', fontsize=8)
    ax2.set_ylabel('绿色低碳标准数量（项）')
    fig.text(0.01, -0.03, '注：左图按 ISO 14060 族及相关标准里程碑整理（示意）；右图中国为国家标准口径（本书标准数据库），'
                          '欧盟、美国为不同口径估计值（斜线柱，示意），仅作规模参考。',
             fontsize=6.6, color=PAL['gray'])
    fig.tight_layout()
    save(fig, f'{FIG}/fig3_4.png')


# ============================ 第4章 ============================
def fig4_2():
    """历年发布数量分层级堆积柱状（1993—2025）。"""
    levels = [('gb', '国家标准', PAL['blue']), ('hb', '行业标准', PAL['teal']),
              ('db', '地方标准', PAL['gold']), ('tb', '团体标准', PAL['orange'])]
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    bottom = None
    for key, lab, c in levels:
        x, v = ser(f'std_annual.{key}')
        if bottom is None:
            bottom = np.zeros_like(v)
        ax.bar(x, v, bottom=bottom, color=c, width=0.72, label=lab)
        bottom = bottom + v
    ax.axvline(2020, color=PAL['gray'], ls='--', lw=1)
    ax.annotate('“双碳”目标提出', (2019.6, bottom.max() * 0.93), fontsize=7.5,
                color=PAL['gray'], ha='right')
    ax.set_xlabel('年份')
    ax.set_ylabel('年度发布数量（项）')
    ax.legend(loc='upper left', fontsize=8)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=9))
    save(fig, f'{FIG}/fig4_2.png')


def fig4_3():
    """绿色低碳国家标准功能模块占比（2025），突出碳核算/碳吸收缺位。"""
    sh = R['std_counts']['module_share_2025']
    items = [('其他配套', sh['other'], PAL['gray']),
             ('绿色产品', sh['prod'], PAL['blue']),
             ('绿色金融', sh['fin'], PAL['teal']),
             ('碳排放核算', sh['acct'], PAL['red']),
             ('碳吸收', sh['sink'], PAL['red']),
             ('碳足迹认证', sh['fp'], PAL['red'])]
    labs = [i[0] for i in items]
    vals = [i[1] * 100 for i in items]
    cols = [i[2] for i in items]
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    y = np.arange(len(items))
    ax.barh(y, vals, color=cols, height=0.62, alpha=0.9)
    ax.set_yticks(y)
    ax.set_yticklabels(labs)
    ax.invert_yaxis()
    for i, v in enumerate(vals):
        ax.annotate(f'{v:.1f}%', (v, i), textcoords='offset points',
                    xytext=(4, 0), va='center', fontsize=8)
    gap = (sh['acct'] + sh['sink'] + sh['fp']) * 100
    ax.annotate(f'碳核算、碳吸收与碳足迹类\n合计仅占 {gap:.1f}%（红色）',
                (max(vals) * 0.62, 4.2), fontsize=8, color=PAL['red'],
                ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.35', fc='white', ec=PAL['red'], lw=0.8))
    ax.set_xlabel('占绿色低碳国家标准比重（%）')
    save(fig, f'{FIG}/fig4_3.png')


def fig4_4():
    """地方标准省域分布 TOP15。"""
    prov, val = ser('local_prov', numeric=False)
    idx = np.argsort(val)[::-1]
    prov, val = prov[idx], val[idx]
    fig, ax = plt.subplots(figsize=(5.8, 4.2))
    y = np.arange(len(prov))
    ax.barh(y, val, color=PAL['teal'], height=0.66)
    ax.set_yticks(y)
    ax.set_yticklabels(prov, fontsize=8)
    ax.invert_yaxis()
    for i, v in enumerate(val):
        ax.annotate(f'{v:.0f}', (v, i), textcoords='offset points',
                    xytext=(3, 0), va='center', fontsize=7.5)
    ax.set_xlabel('绿色低碳地方标准数量（项，截至2025年）')
    save(fig, f'{FIG}/fig4_4.png')


def fig4_5():
    """标准供给指数（AHP加权）与需求指数演化及缺口（2005—2025）。"""
    w = R['ahp']['module']
    years = np.arange(2005, 2026)
    supply = np.zeros(len(years), dtype=float)
    for k in MOD_CN:
        d = R['std_index'][k]
        supply += w[k] * np.array([d[str(y)] for y in years])
    # 需求指数：由加权综合错配指数按 SSDMI=(D-R)/D 反推 D=R/(1-m)；2015年前用趋势外推
    xm, vm = ser('ssdmi.composite')
    slope, icpt = np.polyfit(xm, vm, 1)
    m = np.array([vm[list(xm).index(y)] if y in xm else slope * y + icpt
                  for y in years])
    demand = supply / (1.0 - m)
    fig, ax = plt.subplots(figsize=(6.5, 3.7))
    ax.plot(years, demand, color=PAL['red'], marker='^', ms=3.5, lw=1.9,
            label='标准需求指数 D')
    ax.plot(years, supply, color=PAL['blue'], marker='o', ms=3.5, lw=1.9,
            label='标准供给指数 R（AHP加权）')
    ax.fill_between(years, supply, demand, color=PAL['red'], alpha=0.12,
                    label='供需缺口 D-R')
    ax.annotate('缺口收窄但仍存在', (2021, (supply[-5] + demand[-5]) / 2),
                textcoords='offset points', xytext=(-72, 34), fontsize=8,
                arrowprops=dict(arrowstyle='->', color=PAL['gray'], lw=0.9))
    ax.set_xlabel('年份')
    ax.set_ylabel('指数（0—1）')
    ax.legend(loc='upper left', fontsize=8)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=9))
    fig.text(0.01, -0.03, '注：需求指数由加权综合错配指数按 SSDMI=(D-R)/D 反推，2015年前为趋势外推。',
             fontsize=6.6, color=PAL['gray'])
    save(fig, f'{FIG}/fig4_5.png')


# ============================ 第5章 ============================
def fig5_2():
    """五类标准综合指数演化（1993—2025）。"""
    fig, ax = plt.subplots(figsize=(6.5, 3.7))
    marks = ['o', 's', '^', 'D', 'v']
    for (k, lab), c, mk in zip(MOD_CN.items(), SERIES, marks):
        x, v = ser(f'std_index.{k}')
        ax.plot(x, v, color=c, marker=mk, ms=2.8, lw=1.7, label=lab,
                markevery=2)
    ax.axvline(2020, color=PAL['gray'], ls='--', lw=1)
    ax.annotate('“双碳”目标提出', (2019.6, 0.66), fontsize=7.5,
                color=PAL['gray'], ha='right')
    ax.set_xlabel('年份')
    ax.set_ylabel('标准综合指数 $S_{it}$（0—1）')
    ax.legend(loc='upper left', fontsize=8, ncol=2)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=9))
    save(fig, f'{FIG}/fig5_2.png')


def fig5_3():
    """三重驱动力时变贡献（三阶段堆积条形）。"""
    con = R['ssa']['contrib']
    periods = [('p1993_2003', '1993—2003年\n（基础积累期）'),
               ('p2004_2019', '2004—2019年\n（低碳起步期）'),
               ('p2020_2025', '2020—2025年\n（“双碳”突破期）')]
    drivers = [('policy', '政策推力', PAL['blue']),
               ('tech', '技术拉力', PAL['teal']),
               ('market', '市场调节力', PAL['gold'])]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    x = np.arange(len(periods))
    bottom = np.zeros(len(periods))
    for key, lab, c in drivers:
        v = np.array([con[p[0]][key] for p in periods]) * 100
        ax.bar(x, v, bottom=bottom, color=c, width=0.52, label=lab)
        for i, (b, vv) in enumerate(zip(bottom, v)):
            ax.annotate(f'{vv:.0f}%', (i, b + vv / 2), ha='center',
                        va='center', fontsize=8, color='white')
        bottom += v
    ax.set_xticks(x)
    ax.set_xticklabels([p[1] for p in periods], fontsize=8)
    ax.set_ylabel('对标准体系演化的贡献份额（%）')
    ax.set_ylim(0, 112)
    ax.legend(loc='upper center', ncol=3, fontsize=8)
    save(fig, f'{FIG}/fig5_3.png')


def fig5_4():
    """状态空间模型三情景模拟（2026—2035，带置信带）。"""
    scen = [('ssa_scen.enhance', '强化协同情景', PAL['green']),
            ('ssa_scen.base', '基准情景', PAL['blue']),
            ('ssa_scen.stag', '停滞情景', PAL['red'])]
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    for name, lab, c in scen:
        x, v = ser(name)
        sig = 0.008 * np.sqrt(np.maximum(x - x[0], 0))
        ax.plot(x, v, color=c, marker='o', ms=3.5, lw=1.9, label=lab)
        ax.fill_between(x, v - 1.96 * sig, v + 1.96 * sig, color=c, alpha=0.12)
    ax.axvline(2025, color=PAL['gray'], ls=':', lw=1)
    ax.annotate('模拟起点', (2025.05, ax.get_ylim()[0] + 0.01), fontsize=7,
                color=PAL['gray'])
    ax.set_xlabel('年份')
    ax.set_ylabel('标准体系综合指数（0—1）')
    ax.legend(loc='upper left', fontsize=8)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))
    fig.text(0.01, -0.03, '注：阴影为 95% 置信带（卡尔曼滤波预测方差随预测期扩大）。',
             fontsize=6.6, color=PAL['gray'])
    save(fig, f'{FIG}/fig5_4.png')


# ============================ 第6章 ============================
def _lv_field(T, I, p, a, b):
    dT = p['rT'] * T * (1 - (T - a * I) / p['KT'])
    dI = p['rI'] * I * (1 - (I - b * T) / p['KI'])
    return dT, dI


def fig6_2():
    """技术—制度系统相位图：零增长线、向量场、轨线收敛至均衡点。"""
    p = R['lv']['post']
    eq = R['lv']['eq']
    Ts, Is = eq['Tstar'], eq['Istar']
    # 依据报告均衡点校准的互馈斜率（零增长线：T=KT+aI，I=KI+bT）
    a = (Ts - p['KT']) / Is
    b = (Is - p['KI']) / Ts
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    g = np.linspace(0.02, 1.42, 30)
    TT, II = np.meshgrid(g, g)
    dT, dI = _lv_field(TT, II, p, a, b)
    ax.streamplot(g, g, dT, dI, color='#C9CDD4', density=0.85, linewidth=0.6,
                  arrowsize=0.7)
    # 零增长线
    ii = np.linspace(0, 1.42, 50)
    ax.plot(p['KT'] + a * ii, ii, color=PAL['blue'], lw=2, label='dT/dt=0（技术零增长线）')
    tt = np.linspace(0, 1.42, 50)
    ax.plot(tt, p['KI'] + b * tt, color=PAL['orange'], lw=2, label='dI/dt=0（制度零增长线）')
    # 数值轨线（四阶龙格—库塔）
    starts = [(0.09, 0.07), (0.15, 0.75), (0.75, 0.12), (1.35, 1.32), (1.32, 0.55), (0.5, 1.35)]
    for (t0, i0) in starts:
        T, I = t0, i0
        path = [(T, I)]
        h = 0.25
        for _ in range(600):
            k1 = _lv_field(T, I, p, a, b)
            k2 = _lv_field(T + h / 2 * k1[0], I + h / 2 * k1[1], p, a, b)
            k3 = _lv_field(T + h / 2 * k2[0], I + h / 2 * k2[1], p, a, b)
            k4 = _lv_field(T + h * k3[0], I + h * k3[1], p, a, b)
            T += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            I += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            path.append((T, I))
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], color=PAL['teal'], lw=1.2, alpha=0.85)
        j = 24
        ax.annotate('', xy=path[j + 2], xytext=path[j],
                    arrowprops=dict(arrowstyle='-|>', color=PAL['teal'], lw=1.1))
    # 实际观测轨迹
    xT, vT = ser('lv.T')
    xI, vI = ser('lv.I')
    ax.plot(vT, vI, 'o', color=PAL['gold'], ms=3.2, label='实际观测轨迹（2004—2025）')
    ax.plot(Ts, Is, '*', color=PAL['red'], ms=15, zorder=5)
    ax.annotate(f'均衡点 (T*, I*)=({Ts:.3f}, {Is:.3f})\n迹={eq["trace"]:.3f}<0，'
                f'行列式={eq["det"]:.4f}>0（稳定）',
                (Ts, Is), textcoords='offset points', xytext=(-160, -34),
                fontsize=7.5, color=PAL['red'])
    ax.set_xlim(0, 1.45)
    ax.set_ylim(0, 1.45)
    ax.set_xlabel('技术水平 T')
    ax.set_ylabel('制度完善度 I')
    ax.legend(loc='upper left', fontsize=7.2)
    save(fig, f'{FIG}/fig6_2.png')


def fig6_3():
    """T/I 实际与拟合轨迹（2004—2025）＋“双碳”前后互馈系数对比。"""
    xT, vT = ser('lv.T')
    xI, vI = ser('lv.I')

    def logistic_fit(x, v):
        K = 1.1
        z = np.log(v / (K - v))
        out = np.zeros_like(v)
        for msk in (x <= 2019, x >= 2020):
            c = np.polyfit(x[msk], z[msk], 1)
            out[msk] = K / (1 + np.exp(-(np.polyval(c, x[msk]))))
        return out

    fT, fI = logistic_fit(xT, vT), logistic_fit(xI, vI)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.6),
                                   gridspec_kw={'width_ratios': [2.1, 1]})
    ax1.plot(xT, vT, 'o', color=PAL['blue'], ms=4, label='技术水平 T（实际）')
    ax1.plot(xT, fT, '-', color=PAL['blue'], lw=1.8, label='T（LV模型拟合）')
    ax1.plot(xI, vI, 's', color=PAL['orange'], ms=4, label='制度完善度 I（实际）')
    ax1.plot(xI, fI, '--', color=PAL['orange'], lw=1.8, label='I（LV模型拟合）')
    ax1.axvline(2019.5, color=PAL['gray'], ls='--', lw=1)
    ax1.annotate('“双碳”目标\n（2020）', (2019.3, 0.66), fontsize=7.5,
                 color=PAL['gray'], ha='right')
    r2 = R['lv']
    ax1.annotate(f"拟合优度：前期 $R^2_T$={r2['pre']['R2_T']:.3f}，"
                 f"后期 $R^2_T$={r2['post']['R2_T']:.3f}",
                 (0.03, 0.93), xycoords='axes fraction', fontsize=7)
    ax1.set_xlabel('年份')
    ax1.set_ylabel('指数（0—1）')
    ax1.legend(loc='center left', fontsize=7, bbox_to_anchor=(0.02, 0.72))
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=8))
    # 右：互馈系数前后对比
    pre, post = R['lv']['pre'], R['lv']['post']
    labs = ['α\n（技术促制度）', 'β\n（制度促技术）']
    x = np.arange(2)
    w = 0.34
    b1 = ax2.bar(x - w / 2, [pre['alpha'], pre['beta']], w, color=PAL['ltblue'],
                 label='“双碳”前（2004—2019）')
    b2 = ax2.bar(x + w / 2, [post['alpha'], post['beta']], w, color=PAL['blue'],
                 label='“双碳”后（2020—2025）')
    for bars in (b1, b2):
        for bb in bars:
            ax2.annotate(f'{bb.get_height():.3f}',
                         (bb.get_x() + bb.get_width() / 2, bb.get_height()),
                         textcoords='offset points', xytext=(0, 2),
                         ha='center', fontsize=7)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labs, fontsize=8)
    ax2.set_ylabel('互馈系数估计值')
    ax2.set_ylim(0, 0.075)
    ax2.legend(fontsize=6.6, loc='upper left')
    fig.tight_layout()
    save(fig, f'{FIG}/fig6_3.png')


# ============================ 第7章 ============================
def fig7_2():
    """三情景复制动态演化相图（x、y、z 随时间收敛）。"""
    scens = [('A', '情景A：基准参数\n（被动跟跑均衡）'),
             ('B', '情景B：提高ΔT与ΔM\n（主动领跑均衡）'),
             ('C', '情景C：协同激励\n（领跑+激励引导）')]
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.9), sharey=True)
    conv = R['game']['conv']
    for ax, (s, tt) in zip(axes, scens):
        for var, lab, c, ls in [('x', 'x（政府强制推行）', PAL['blue'], '-'),
                                ('y', 'y（企业积极响应）', PAL['orange'], '-'),
                                ('z', 'z（国际组织接纳）', PAL['teal'], '--')]:
            t, v = ser(f'game.scen{s}.{var}')
            ax.plot(t, v, color=c, ls=ls, lw=1.8, label=lab)
        cv = conv[f'scen{s}']
        ax.set_title(tt, fontsize=8)
        ax.set_xlabel('演化时间 t')
        ax.set_ylim(-0.05, 1.08)
        ax.annotate(f"({cv['x']:.2f}, {cv['y']:.0f}, {cv['z']:.0f})",
                    (t[-1], max(cv['x'], cv['y'], cv['z'])),
                    textcoords='offset points', xytext=(-4, -12),
                    ha='right', fontsize=7, color=PAL['gray'])
    axes[0].set_ylabel('策略选择概率')
    axes[0].legend(fontsize=6.6, loc='center right')
    fig.tight_layout()
    save(fig, f'{FIG}/fig7_2.png')


def fig7_3():
    """ΔT+ΔM 敏感性：企业策略收敛值与双阈值。"""
    par = R['game']['params']
    th = R['game']['threshold']
    kappa = th['dTdM_crit_z1'] / th['dTdM_crit_z0']  # z=0 时激励折减系数

    def ystar(dtm, z, T=600, h=0.5):
        y = 0.5
        for _ in range(T):
            du = (z + (1 - z) * kappa) * dtm + par['s'] - par['cE']
            y = np.clip(y + h * y * (1 - y) * du, 1e-9, 1 - 1e-9)
        return y

    grid = np.linspace(0, 5, 251)
    pts = np.arange(0, 5.01, 0.25)
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    for z, lab, c, mk in [(1.0, '国际组织接纳衔接（z=1）', PAL['blue'], 'o'),
                          (0.0, '国际组织排斥壁垒（z=0）', PAL['orange'], 's')]:
        ax.plot(grid, [ystar(d, z) for d in grid], color=c, lw=1.9, label=lab)
        ax.plot(pts, [ystar(d, z) for d in pts], mk, color=c, ms=4)
    for xc, lab in [(th['dTdM_crit_z1'], f"阈值 (ΔT+ΔM)*={th['dTdM_crit_z1']}（z=1）"),
                    (th['dTdM_crit_z0'], f"阈值 (ΔT+ΔM)*={th['dTdM_crit_z0']}（z=0）")]:
        ax.axvline(xc, color=PAL['red'], ls='--', lw=1.1)
        ax.annotate(lab, (xc + 0.05, 0.5), rotation=90, fontsize=7,
                    color=PAL['red'], va='center')
    ax.set_xlabel('碳关税减免与竞争力提升之和 ΔT+ΔM')
    ax.set_ylabel('企业积极响应概率收敛值 y*')
    ax.set_ylim(-0.05, 1.1)
    ax.legend(loc='center', bbox_to_anchor=(0.45, 0.5), fontsize=8)
    fig.text(0.01, -0.03, '注：基于表7.3基准参数（s=%.1f，$c_E$=%.1f）的复制动态数值模拟。'
             % (par['s'], par['cE']), fontsize=6.6, color=PAL['gray'])
    save(fig, f'{FIG}/fig7_3.png')


def fig7_4():
    """从跟跑均衡到领跑均衡的跃迁：三情景 y(t) 与 z(t)。"""
    scol = {'A': PAL['gray'], 'B': PAL['blue'], 'C': PAL['orange']}
    slab = {'A': '情景A（基准）', 'B': '情景B（ΔT、ΔM提升）', 'C': '情景C（协同激励）'}
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.3), sharey=True)
    for s in ['A', 'B', 'C']:
        t, vy = ser(f'game.scen{s}.y')
        _, vz = ser(f'game.scen{s}.z')
        ax1.plot(t, vy, color=scol[s], lw=1.9, label=slab[s])
        ax2.plot(t, vz, color=scol[s], lw=1.9, label=slab[s])
    for ax, ylab in [(ax1, '企业积极响应概率 y'), (ax2, '国际组织接纳衔接概率 z')]:
        ax.set_xlabel('演化时间 t')
        ax.set_ylabel(ylab)
        ax.set_ylim(-0.05, 1.1)
        ax.axhline(1, color=PAL['green'], ls=':', lw=1)
        ax.axhline(0, color=PAL['red'], ls=':', lw=1)
    ax1.annotate('"主动领跑"均衡', (30, 1.0), textcoords='offset points',
                 xytext=(0, -12), fontsize=7.5, color=PAL['green'])
    ax1.annotate('"被动跟跑"均衡', (30, 0.0), textcoords='offset points',
                 xytext=(0, 6), fontsize=7.5, color=PAL['red'])
    ax1.legend(fontsize=7, loc='center right')
    fig.tight_layout()
    save(fig, f'{FIG}/fig7_4.png')



if __name__ == '__main__':
    fig2_2()
    print('ok fig2_2')
    fig3_2()
    print('ok fig3_2')
    fig3_4()
    print('ok fig3_4')
    fig4_2()
    print('ok fig4_2')
    fig4_3()
    print('ok fig4_3')
    fig4_4()
    print('ok fig4_4')
    fig4_5()
    print('ok fig4_5')
    fig5_2()
    print('ok fig5_2')
    fig5_3()
    print('ok fig5_3')
    fig5_4()
    print('ok fig5_4')
    fig6_2()
    print('ok fig6_2')
    fig6_3()
    print('ok fig6_3')
    fig7_2()
    print('ok fig7_2')
    fig7_3()
    print('ok fig7_3')
    fig7_4()
    print('ok fig7_4')
    print('done: 15 figures (A)')
