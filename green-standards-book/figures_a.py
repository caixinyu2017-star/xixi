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
from matplotlib import font_manager as _fm
from figstyle import save, PAL, SERIES, CJK

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)

DF = pd.read_csv(os.path.join(HERE, 'data', 'series.csv'), dtype={'x': str})
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))

# ---- 局部样式辅助（仅限本文件使用，不改动 figstyle.py） ----
_BOLD_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
_fm.fontManager.addfont(_BOLD_PATH)
BOLD_FP = _fm.FontProperties(fname=_BOLD_PATH, size=10.5)

# 注记白底衬垫（避免文字被曲线/流线穿越）
WBOX = dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85)
NOTE_FS = 8  # 图内脚注字号（13.5cm 版面缩印后仍可读）


def panel_label(ax, s, x=-0.12, y=1.02):
    """多面板图黑体面板标签（a）（b）（c）…（左上角）。"""
    ax.text(x, y, s, transform=ax.transAxes, fontproperties=BOLD_FP,
            ha='left', va='bottom')


def line_end_label(ax, x, y, text, color, dx=0.0, dy=0.0, fs=8):
    """线末直接标注（替代图例框）。"""
    ax.annotate(text, (x + dx, y + dy), color=color, fontsize=fs,
                ha='left', va='center', annotation_clip=False)


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
def fig2_1():
    """WOS/CNKI 年度发文趋势（2000—2025）：“双碳”后爆发式增长、中文反超。"""
    xw, yw = ser('biblio.wos')
    xc, yc = ser('biblio.cnki')
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(xw, yw, color=PAL['blue'], marker='o', ms=3, lw=1.8)
    ax.plot(xc, yc, color=PAL['orange'], marker='s', ms=3, lw=1.8)
    ax.set_xlim(1999, 2030.8)
    ax.set_ylim(0, 14000)
    for yy, lab in [(2015, '巴黎协定'), (2020, '“双碳”目标提出')]:
        ax.axvline(yy, color=PAL['gray'], ls=':', lw=1)
        ax.annotate(lab, (yy, 13700), rotation=90, fontsize=8,
                    color=PAL['gray'], ha='right', va='top', bbox=WBOX)
    # 线末直接标注（替代图例框）
    line_end_label(ax, xc[-1], 13050, 'CNKI（中文文献）', PAL['orange'], dx=0.4)
    line_end_label(ax, xw[-1], 11950, 'WOS（英文文献）', PAL['blue'], dx=0.4)
    ax.set_xlabel('年份')
    ax.set_ylabel('年度发文量（篇）')
    ax.set_xticks(np.arange(2000, 2026, 5))
    save(fig, f'{FIG}/fig2_1.png')


# ============================ 第3章 ============================
def fig3_2():
    """EUA 与 CEA 年均价（双轴），关键事件竖线＋末年数值。"""
    xe, ye = ser('drivers.eua')
    xc, yc = ser('drivers.ets')
    fig, ax1 = plt.subplots(figsize=(6.6, 3.7))
    ax1.plot(xe, ye, color=PAL['blue'], marker='o', ms=4, lw=1.9)
    ax1.set_ylabel('欧元/吨', color=PAL['blue'])
    ax1.set_xlabel('年份')
    ax1.tick_params(axis='y', labelcolor=PAL['blue'])
    ax1.set_ylim(0, 100)
    ax1.set_xlim(2012.4, 2027.2)
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)
    ax2.plot(xc, yc, color=PAL['orange'], marker='s', ms=4, lw=1.9)
    ax2.set_ylabel('元/吨', color=PAL['orange'])
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(PAL['orange'])
    ax2.spines['right'].set_linewidth(0.9)
    ax2.tick_params(axis='y', labelcolor=PAL['orange'])
    ax2.set_ylim(20, 120)
    ax2.grid(False)
    for yy, lab in [(2021, '全国碳市场启动\n（2021年7月）'),
                    (2023.75, 'CBAM过渡期实施\n（2023年10月）')]:
        ax1.axvline(yy, color=PAL['gray'], ls='--', lw=1)
        ax1.annotate(lab, (yy - 0.15, 98), fontsize=8,
                     color=PAL['gray'], ha='right', va='top', zorder=6,
                     bbox=WBOX)
    # 末年关键数值直接标注（替代图例；轴标签已注明系列与单位）
    ax1.annotate(f'EUA {ye[-1]:.0f}', (xe[-1] + 0.25, ye[-1] + 2),
                 color=PAL['blue'], fontsize=8, ha='left', va='center')
    ax2.annotate(f'CEA {yc[-1]:.1f}', (xc[-1] + 0.25, yc[-1] - 2),
                 color=PAL['orange'], fontsize=8, ha='left', va='center')
    ax1.set_xticks(np.arange(2013, 2026, 2))
    save(fig, f'{FIG}/fig3_2.png')


def fig3_4():
    """ISO 温室气体核心标准里程碑累计（示意）＋主要经济体对比（示意口径）。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.6),
                                   gridspec_kw={'width_ratios': [1.5, 1]})
    # （a）ISO 14060 族及相关标准累计（里程碑，示意整理）
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
        ax1.annotate(lab, (y, c), textcoords='offset points', xytext=(3, -14),
                     fontsize=8, color=PAL['gray'], va='top' if '\n' in lab else 'center')
    ax1.set_xlim(2004, 2027.5)
    ax1.set_ylim(0, 9.6)
    ax1.set_xticks([2005, 2010, 2015, 2020, 2025])
    ax1.set_xlabel('年份')
    ax1.set_ylabel('ISO 温室气体核心标准累计数量（项）')
    panel_label(ax1, '（a）', x=-0.13)
    # （b）主要经济体绿色低碳标准数量对比（不同口径示意）
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
    panel_label(ax2, '（b）', x=-0.24)
    fig.text(0.01, -0.06, '注：（a）按 ISO 14060 族及相关标准里程碑整理（示意）；（b）中国为国家标准口径（本书标准数据库），\n'
                          '欧盟、美国为不同口径估计值（斜线柱，示意），仅作规模参考。',
             fontsize=NOTE_FS, color=PAL['gray'], va='top')
    fig.tight_layout()
    save(fig, f'{FIG}/fig3_4.png')


# ============================ 第4章 ============================
def fig4_1():
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
    # 事件线放在柱缝（2019/2020 之间），不压柱
    ax.axvline(2019.5, color=PAL['gray'], ls='--', lw=1)
    ax.annotate('“双碳”目标提出（2020）', (2019.2, bottom.max() * 0.97), fontsize=8,
                color=PAL['gray'], ha='right', va='top')
    # 峰值年份直接标数
    ipk = int(np.argmax(bottom))
    ax.annotate(f'峰值 {bottom[ipk]:.0f} 项', (x[ipk], bottom[ipk]),
                textcoords='offset points', xytext=(0, 4), ha='center',
                fontsize=8, color=PAL['blue'])
    ax.set_xlabel('年份')
    ax.set_ylabel('年度发布数量（项）')
    ax.set_ylim(0, bottom.max() * 1.12)
    # 图例顺序与堆积顺序一致（上层在前）
    h, l = ax.get_legend_handles_labels()
    ax.legend(h[::-1], l[::-1], loc='upper left', fontsize=8)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=9))
    save(fig, f'{FIG}/fig4_1.png')


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
    ax.annotate(f'碳排放核算、碳吸收与\n碳足迹认证三类合计仅占 {gap:.1f}%',
                (max(vals) * 0.60, 4.2), fontsize=8, color=PAL['red'],
                ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.35', fc='white', ec=PAL['red'], lw=0.8))
    ax.set_xlabel('占绿色低碳国家标准比重（%）')
    save(fig, f'{FIG}/fig4_3.png')


def fig4_4():
    """地方标准省域分布 TOP15（按区域着色：东部领跑）。"""
    prov, val = ser('local_prov', numeric=False)
    idx = np.argsort(val)[::-1]
    prov, val = prov[idx], val[idx]
    region_of = {'山东': 'east', '广东': 'east', '浙江': 'east', '江苏': 'east',
                 '河北': 'east', '福建': 'east', '北京': 'east', '上海': 'east',
                 '天津': 'east', '海南': 'east',
                 '湖北': 'central', '安徽': 'central', '湖南': 'central',
                 '河南': 'central', '江西': 'central', '山西': 'central',
                 '四川': 'west', '陕西': 'west', '重庆': 'west', '云南': 'west',
                 '贵州': 'west', '广西': 'west', '甘肃': 'west'}
    regs = [region_of.get(p, 'east') for p in prov]
    cols = [REG_C[r] for r in regs]
    fig, ax = plt.subplots(figsize=(5.8, 4.2))
    y = np.arange(len(prov))
    bars = ax.barh(y, val, color=cols, height=0.66)
    for b, r in zip(bars, regs):  # 灰度打印可辨：西部斜线纹理
        if r == 'west':
            b.set_hatch('//')
            b.set_edgecolor('white')
            b.set_linewidth(0)
    ax.set_yticks(y)
    ax.set_yticklabels(prov, fontsize=8)
    ax.invert_yaxis()
    for i, v in enumerate(val):
        ax.annotate(f'{v:.0f}', (v, i), textcoords='offset points',
                    xytext=(3, 0), va='center', fontsize=8)
    handles = [Patch(fc=REG_C['east'], label='东部'),
               Patch(fc=REG_C['central'], label='中部'),
               Patch(fc=REG_C['west'], hatch='//', ec='white', label='西部')]
    ax.legend(handles=handles, loc='lower right', fontsize=8, title=None)
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
    ax.plot(years, demand, color=PAL['red'], marker='^', ms=3.5, lw=1.9)
    ax.plot(years, supply, color=PAL['blue'], marker='o', ms=3.5, lw=1.9)
    ax.fill_between(years, supply, demand, color=PAL['red'], alpha=0.12)
    ax.set_xlim(2004.2, 2030.6)
    # 线末直接标注（替代图例框）＋末年数值
    line_end_label(ax, years[-1], demand[-1], f'标准需求指数 D\n2025年 {demand[-1]:.2f}',
                   PAL['red'], dx=0.4)
    line_end_label(ax, years[-1], supply[-1], f'标准供给指数 R\n（AHP加权）{supply[-1]:.2f}',
                   PAL['blue'], dx=0.4)
    ax.annotate('供需缺口 D-R', (2013.5, 0.335), fontsize=8, color=PAL['red'],
                ha='center', va='center')
    m15 = vm[list(xm).index(2015)]
    m25 = vm[list(xm).index(2025)]
    ax.text(0.02, 0.97, f'相对错配率 SSDMI 由 {m15:.2f}（2015年）\n'
                        f'降至 {m25:.2f}（2025年）：缺口收窄但仍存在',
            transform=ax.transAxes, fontsize=8, va='top', color=PAL['gray'])
    ax.set_xlabel('年份')
    ax.set_ylabel('指数（0—1）')
    ax.set_xticks(np.arange(2005, 2026, 5))
    fig.text(0.01, -0.04, '注：需求指数由加权综合错配指数按 SSDMI=(D-R)/D 反推，2015年前为趋势外推。',
             fontsize=NOTE_FS, color=PAL['gray'])
    save(fig, f'{FIG}/fig4_5.png')


# ============================ 第5章 ============================
def fig5_2():
    """五类标准综合指数演化（1993—2025），线末直接标注。"""
    fig, ax = plt.subplots(figsize=(6.5, 3.7))
    marks = ['o', 's', '^', 'D', 'v']
    enddy = {'acct': -0.028, 'fp': -0.022, 'prod': 0.018, 'sink': 0.0, 'fin': 0.012}
    for (k, lab), c, mk in zip(MOD_CN.items(), SERIES, marks):
        x, v = ser(f'std_index.{k}')
        ax.plot(x, v, color=c, marker=mk, ms=2.8, lw=1.7, markevery=2)
        line_end_label(ax, x[-1], v[-1] + enddy[k], f'{lab} {v[-1]:.2f}', c, dx=0.5)
    ax.axvline(2020, color=PAL['gray'], ls='--', lw=1)
    ax.annotate('“双碳”目标提出', (2019.6, 0.72), fontsize=8,
                color=PAL['gray'], ha='right', va='top')
    ax.set_xlim(1992, 2031.5)
    ax.set_ylim(-0.02, 0.75)
    ax.set_xlabel('年份')
    ax.set_ylabel('标准综合指数 $S_{it}$（0—1）')
    ax.set_xticks(np.arange(1995, 2026, 5))
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
    """状态空间模型三情景模拟（2026—2035，带置信带），线末直接标注。"""
    scen = [('ssa_scen.enhance', '强化协同情景', PAL['blue'], '-', 'o'),
            ('ssa_scen.base', '基准情景', PAL['gray'], '--', 's'),
            ('ssa_scen.stag', '停滞情景', PAL['red'], '-.', '^')]
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    for name, lab, c, ls, mk in scen:
        x, v = ser(name)
        sig = 0.008 * np.sqrt(np.maximum(x - x[0], 0))
        ax.plot(x, v, color=c, marker=mk, ms=3.5, lw=1.9, ls=ls)
        ax.fill_between(x, v - 1.96 * sig, v + 1.96 * sig, color=c, alpha=0.12)
        line_end_label(ax, x[-1], v[-1], f'{lab} {v[-1]:.2f}', c, dx=0.3)
    ax.axvline(2025, color=PAL['gray'], ls=':', lw=1)
    ax.annotate('模拟起点', (2025.15, ax.get_ylim()[0] + 0.012), fontsize=8,
                color=PAL['gray'], bbox=WBOX)
    ax.set_xlim(2024.6, 2039.2)
    ax.set_xlabel('年份')
    ax.set_ylabel('标准体系综合指数（0—1）')
    ax.set_xticks(np.arange(2025, 2036, 2))
    fig.text(0.01, -0.04, '注：阴影为 95% 置信带（卡尔曼滤波预测方差随预测期扩大）。',
             fontsize=NOTE_FS, color=PAL['gray'])
    save(fig, f'{FIG}/fig5_4.png')


# ============================ 第6章 ============================
def _lv_field(T, I, p, a, b):
    dT = p['rT'] * T * (1 - (T - a * I) / p['KT'])
    dI = p['rI'] * I * (1 - (I - b * T) / p['KI'])
    return dT, dI


def fig6_3():
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
    # 观测轨迹（2004—2025 指数序列）
    xT, vT = ser('lv.T')
    xI, vI = ser('lv.I')
    ax.plot(vT, vI, 'o', color=PAL['gold'], ms=3.2, label='观测轨迹（2004—2025）')
    ax.annotate('2004', (vT[0], vI[0]), textcoords='offset points',
                xytext=(6, -9), fontsize=8, color=PAL['gray'])
    ax.annotate('2025', (vT[-1], vI[-1]), textcoords='offset points',
                xytext=(7, -3), fontsize=8, color=PAL['gray'])
    ax.plot(Ts, Is, '*', color=PAL['red'], ms=15, zorder=5)
    ax.annotate(f'均衡点 (T*, I*)=({Ts:.3f}, {Is:.3f})\n迹={eq["trace"]:.3f}<0，'
                f'行列式={eq["det"]:.4f}>0（稳定）',
                (Ts, Is), textcoords='offset points', xytext=(-172, -40),
                fontsize=8, color=PAL['red'], bbox=WBOX, zorder=6)
    ax.set_xlim(0, 1.45)
    ax.set_ylim(0, 1.45)
    ax.set_xlabel('技术水平 T')
    ax.set_ylabel('制度完善度 I')
    ax.legend(loc='upper left', fontsize=8, frameon=True, facecolor='white',
              edgecolor='none', framealpha=0.9)
    save(fig, f'{FIG}/fig6_3.png')


def fig6_2():
    """T/I 观测与拟合轨迹（2004—2025）＋“双碳”前后互馈系数对比。"""
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
    ax1.plot(xT, vT, 'o', color=PAL['blue'], ms=4, label='技术水平 T（观测）')
    ax1.plot(xT, fT, '-', color=PAL['blue'], lw=1.8, label='T（LV模型拟合）')
    ax1.plot(xI, vI, 's', color=PAL['orange'], ms=4, label='制度完善度 I（观测）')
    ax1.plot(xI, fI, '--', color=PAL['orange'], lw=1.8, label='I（LV模型拟合）')
    ax1.axvline(2019.5, color=PAL['gray'], ls='--', lw=1)
    ax1.annotate('“双碳”目标\n（2020）', (2019.3, 0.64), fontsize=8,
                 color=PAL['gray'], ha='right')
    r2 = R['lv']
    ax1.annotate(f"拟合优度：前期 $R^2_T$={r2['pre']['R2_T']:.3f}，"
                 f"后期 $R^2_T$={r2['post']['R2_T']:.3f}",
                 (0.03, 0.95), xycoords='axes fraction', fontsize=8)
    ax1.set_xlabel('年份')
    ax1.set_ylabel('指数（0—1）')
    ax1.legend(loc='center left', fontsize=8, bbox_to_anchor=(0.02, 0.68))
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=8))
    panel_label(ax1, '（a）', x=-0.10)
    # （b）互馈系数前后对比
    pre, post = R['lv']['pre'], R['lv']['post']
    labs = ['α\n（技术促制度）', 'β\n（制度促技术）']
    x = np.arange(2)
    w = 0.34
    b1 = ax2.bar(x - w / 2, [pre['alpha'], pre['beta']], w, color=PAL['ltblue'],
                 label='“双碳”前\n（2004—2019）')
    b2 = ax2.bar(x + w / 2, [post['alpha'], post['beta']], w, color=PAL['blue'],
                 label='“双碳”后\n（2020—2025）')
    for bars in (b1, b2):
        for bb in bars:
            ax2.annotate(f'{bb.get_height():.3f}',
                         (bb.get_x() + bb.get_width() / 2, bb.get_height()),
                         textcoords='offset points', xytext=(0, 2),
                         ha='center', fontsize=8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labs, fontsize=8)
    ax2.set_ylabel('互馈系数估计值')
    ax2.set_ylim(0, 0.088)
    ax2.legend(fontsize=8, loc='upper left')
    panel_label(ax2, '（b）', x=-0.30)
    fig.tight_layout()
    save(fig, f'{FIG}/fig6_2.png')


# ============================ 第7章 ============================
def fig7_2():
    """三情景复制动态演化相图（x、y、z 随时间收敛）。"""
    scens = [('A', '情景A：基准参数\n（被动跟跑均衡）'),
             ('B', '情景B：提高ΔT与ΔM\n（主动领跑均衡）'),
             ('C', '情景C：协同激励\n（领跑+激励引导）')]
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.9), sharey=True)
    conv = R['game']['conv']
    for j, (ax, (s, tt)) in enumerate(zip(axes, scens)):
        for var, lab, c, ls in [('x', 'x（政府强制推行）', PAL['blue'], '-'),
                                ('y', 'y（企业积极响应）', PAL['orange'], '-'),
                                ('z', 'z（国际组织接纳）', PAL['teal'], '--')]:
            t, v = ser(f'game.scen{s}.{var}')
            ax.plot(t, v, color=c, ls=ls, lw=1.8, label=lab)
        cv = conv[f'scen{s}']
        ax.set_title(tt, fontsize=8.5)
        ax.set_xlabel('演化时间 t')
        ax.set_ylim(-0.05, 1.08)
        pre = '(x*, y*, z*)=' if j == 0 else ''
        ax.annotate(f"{pre}({cv['x']:.2f}, {cv['y']:.0f}, {cv['z']:.0f})",
                    (t[-1], max(cv['x'], cv['y'], cv['z'])),
                    textcoords='offset points', xytext=(-2, -13),
                    ha='right', fontsize=8, color=PAL['gray'], bbox=WBOX)
        panel_label(ax, f'（{"abc"[j]}）', x=(-0.30 if j == 0 else -0.08), y=1.24)
    axes[0].set_ylabel('策略选择概率')
    axes[0].legend(fontsize=8, loc='center right')
    fig.tight_layout()
    save(fig, f'{FIG}/fig7_2.png')


def fig7_3():
    """ΔT+ΔM 敏感性：企业策略收敛值与双阈值。"""
    par = R['game']['params']
    th = R['game']['threshold']
    kappa = th['dTdM_crit_z1'] / th['dTdM_crit_z0']  # z=0 时激励折减系数
    ratio = th['dTdM_crit_z0'] / th['dTdM_crit_z1']

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
        ax.annotate(lab, (xc + 0.05, 0.5), rotation=90, fontsize=8,
                    color=PAL['red'], va='center', bbox=WBOX)
    # 双阈值差距（结论性证据）
    ax.annotate('', xy=(th['dTdM_crit_z0'] - 0.06, 0.30),
                xytext=(th['dTdM_crit_z1'] + 0.06, 0.30),
                arrowprops=dict(arrowstyle='<->', color=PAL['red'], lw=1))
    ax.annotate(f'衔接互认使响应阈值降低 {ratio:.0f} 倍',
                ((th['dTdM_crit_z0'] + th['dTdM_crit_z1']) / 2, 0.30),
                textcoords='offset points', xytext=(0, -13), ha='center',
                fontsize=8, color=PAL['red'])
    ax.set_xlabel('碳关税减免与竞争力提升之和 ΔT+ΔM')
    ax.set_ylabel('企业积极响应概率收敛值 y*')
    ax.set_ylim(-0.05, 1.1)
    ax.legend(loc='center', bbox_to_anchor=(0.45, 0.56), fontsize=8)
    fig.text(0.01, -0.04, '注：基于表7.3基准参数（s=%.1f，$c_E$=%.1f）的复制动态数值模拟。'
             % (par['s'], par['cE']), fontsize=NOTE_FS, color=PAL['gray'])
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
    ax1.annotate('“主动领跑”均衡', (30, 1.0), textcoords='offset points',
                 xytext=(0, -13), fontsize=8, color=PAL['green'])
    ax1.annotate('“被动跟跑”均衡', (30, 0.0), textcoords='offset points',
                 xytext=(0, 7), fontsize=8, color=PAL['red'])
    ax1.legend(fontsize=8, loc='center right')
    panel_label(ax1, '（a）', x=-0.13)
    panel_label(ax2, '（b）', x=-0.05)
    fig.tight_layout()
    save(fig, f'{FIG}/fig7_4.png')



if __name__ == '__main__':
    fig2_1()
    print('ok fig2_1')
    fig3_2()
    print('ok fig3_2')
    fig3_4()
    print('ok fig3_4')
    fig4_1()
    print('ok fig4_1')
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
    fig6_3()
    print('ok fig6_3')
    fig6_2()
    print('ok fig6_2')
    fig7_2()
    print('ok fig7_2')
    fig7_3()
    print('ok fig7_3')
    fig7_4()
    print('ok fig7_4')
    print('done: 15 figures (A)')
