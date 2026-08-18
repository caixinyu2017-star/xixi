# -*- coding: utf-8 -*-
"""前半部 A 型分析图（12 幅，matplotlib，nature 风格，中文）。

数据一律读取 data/series.csv 与 data/results.json（fig4_5 另据 data/facts.md 核实口径）；
不得手写模型数字。输出 figs/figN_M.png（400 dpi）。
图内不含图名、图注与资料来源文字——图名图注由 Word 排版添加。
符号约定：物理词元 T、标准词元 T̃、效值系数 η、三维效值 P/R/S、标准词元价格 p̃＝p/η。
模型一律用档位名（轻量蒸馏级／中型通用级／开源旗舰级／旗舰闭源级／推理增强级／多模态级）。
"""
import json
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

from figstyle import save, PAL, SERIES, CJK

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)

DF = pd.read_csv(os.path.join(HERE, 'data', 'series.csv'), dtype={'x': str})
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))

# ---------------------------- 局部样式辅助 ----------------------------
_BOLD_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
_fm.fontManager.addfont(_BOLD_PATH)
BOLD_FP = _fm.FontProperties(fname=_BOLD_PATH, size=10.5)
BOLD_NUM = _fm.FontProperties(fname=_BOLD_PATH, size=19)

# 注记白底衬垫（避免文字被网格线／数据线穿越）
WBOX = dict(boxstyle='round,pad=0.22', fc='white', ec='none', alpha=0.88)


def kbox(ec):
    """带描边的注记框（浅色填充＋深色描边）。"""
    return dict(boxstyle='round,pad=0.34', fc='white', ec=ec, lw=0.8, alpha=0.95)


TIERS = ['light', 'mid', 'open', 'flag', 'reason', 'multi']
TIER_CN = R['ste']['tier_cn']
TIER_LAB = [TIER_CN[t] for t in TIERS]
TIER_C = {t: c for t, c in zip(TIERS, SERIES)}

SCENE_CN = {'agent_coding': 'Agent与编程', 'chat': '对话问答',
            'content': '内容生成', 'other': '其他'}
SCENE_KEYS = ['agent_coding', 'chat', 'content', 'other']

QUARTERS = ['2024Q1', '2024Q2', '2024Q3', '2024Q4', '2025Q1',
            '2025Q2', '2025Q3', '2025Q4', '2026Q1', '2026Q2']


def panel_label(ax, s, x=-0.13, y=1.02):
    """多面板黑体面板标签（a）（b）。"""
    ax.text(x, y, s, transform=ax.transAxes, fontproperties=BOLD_FP,
            ha='left', va='bottom')


def ser(name, numeric=True):
    """按 series 名取 (x, value)；numeric=True 时 x 转 float 并升序排列。"""
    d = DF[DF.series == name]
    if numeric:
        x = d.x.astype(float).values
        v = d.value.astype(float).values
        idx = np.argsort(x)
        return x[idx], v[idx]
    return d.x.values, d.value.astype(float).values


def by_tier(name):
    """按六档位固定次序取值，保证各图档位顺序一致。"""
    d = DF[DF.series == name].set_index('x')['value'].astype(float)
    return np.array([float(d[t]) for t in TIERS])


def by_quarter(name):
    d = DF[DF.series == name].set_index('x')['value'].astype(float)
    return np.array([float(d[q]) for q in QUARTERS])


def grid_y(ax):
    ax.set_axisbelow(True)
    ax.grid(axis='y', alpha=0.25, lw=0.6)
    ax.grid(axis='x', visible=False)


def grid_x(ax):
    ax.set_axisbelow(True)
    ax.grid(axis='x', alpha=0.25, lw=0.6)
    ax.grid(axis='y', visible=False)


def twin_right(ax1, color):
    """双轴图：右轴轴线、刻度、轴标签齐全（与左轴对称）。"""
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(color)
    ax2.spines['right'].set_linewidth(0.9)
    ax2.tick_params(axis='y', labelcolor=color, color=color)
    ax2.grid(False)
    return ax2


def plain_log(ax, axis='y'):
    """对数轴用普通数字刻度标签（避免 10^n 上标）。"""
    a = ax.yaxis if axis == 'y' else ax.xaxis
    a.set_major_formatter(FuncFormatter(
        lambda v, p: ('%g' % v) if v >= 1 else ('%.2f' % v).rstrip('0')))
    ax.minorticks_off()


def fit_origin(x, y):
    """过原点最小二乘 y＝kx，返回 (k, R²)（以均值为基准的决定系数）。"""
    k = float((x * y).sum() / (x * x).sum())
    ss_res = float(((y - k * x) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return k, 1.0 - ss_res / ss_tot


# ============================== 第2章 ==============================
def fig2_1():
    """图2.1 词元经济相关研究年度发文趋势（2015—2026）：WOS／CNKI 双线。"""
    xw, yw = ser('biblio.wos')
    xc, yc = ser('biblio.cnki')
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(xc, yc, color=PAL['orange'], marker='s', ms=3.4, lw=1.8,
            label='CNKI（中文文献）')
    ax.plot(xw, yw, color=PAL['blue'], marker='o', ms=3.4, lw=1.8,
            label='WOS（英文文献）')
    ax.axvline(2022.9, color=PAL['gray'], ls=':', lw=1.0)
    ax.annotate('大模型浪潮\n（2022年末）', (2022.7, 9300), fontsize=8,
                color=PAL['gray'], ha='right', va='top', bbox=WBOX)
    ax.annotate(f'{yc[-1]:.0f}', (xc[-1], yc[-1]), textcoords='offset points',
                xytext=(-2, 8), fontsize=8, color=PAL['orange'], ha='center')
    ax.annotate(f'{yw[-1]:.0f}', (xw[-1], yw[-1]), textcoords='offset points',
                xytext=(-2, 8), fontsize=8, color=PAL['blue'], ha='center')
    r_c = yc[-1] / yc[list(xc).index(2022.0)]
    r_w = yw[-1] / yw[list(xw).index(2022.0)]
    ax.annotate(f'2022→2026年：\nCNKI 增至 {r_c:.1f} 倍、WOS 增至 {r_w:.1f} 倍',
                (2016.0, 6200), fontsize=8, color=PAL['blue'],
                ha='left', va='center', bbox=kbox(PAL['blue']))
    ax.set_xlim(2014.4, 2026.7)
    ax.set_ylim(0, 10200)
    ax.set_xlabel('年份')
    ax.set_ylabel('年度发文量（篇）')
    ax.set_xticks(np.arange(2015, 2027, 1))
    ax.tick_params(axis='x', labelrotation=0)
    grid_y(ax)
    ax.legend(loc='upper left', fontsize=8)
    save(fig, f'{FIG}/fig2_1.png')
    print('ok fig2_1')


# ============================== 第3章 ==============================
def fig3_2():
    """图3.2 六档位模型的单词元算力强度 P 与推理质量 R（分组条形）。"""
    P, Rq = by_tier('ste.P'), by_tier('ste.R')
    x = np.arange(len(TIERS))
    w = 0.36
    fig, ax = plt.subplots(figsize=(6.6, 3.7))
    b1 = ax.bar(x - w / 2, P, w, color=PAL['ltblue'], edgecolor=PAL['blue'],
                lw=0.9, label='$P$  算力强度')
    b2 = ax.bar(x + w / 2, Rq, w, color='#F2C8A0', edgecolor=PAL['orange'],
                lw=0.9, label='$R$  推理质量')
    for xi, v in zip(x - w / 2, P):
        ax.annotate(f'{v:.2f}', (xi, v), textcoords='offset points',
                    xytext=(0, 2.5), ha='center', fontsize=7.5,
                    color=PAL['blue'])
    for xi, v in zip(x + w / 2, Rq):
        ax.annotate(f'{v:.2f}', (xi, v), textcoords='offset points',
                    xytext=(0, 2.5), ha='center', fontsize=7.5,
                    color=PAL['orange'])
    ax.axhline(1.0, color=PAL['gray'], ls='--', lw=0.9)
    ax.annotate('基准档归一\n$P$＝$R$＝1', (-0.55, 1.85), ha='left',
                va='center', fontsize=7.5, color=PAL['gray'])
    ax.set_xticks(x)
    ax.set_xticklabels(TIER_LAB, fontsize=8)
    ax.set_xlim(-0.62, 5.62)
    ax.set_ylim(0, 10.0)
    ax.set_ylabel('相对基准档的效值维度取值（中型通用级＝1）')
    ax.set_xlabel('模型档位')
    grid_y(ax)
    ax.legend(loc='upper left', fontsize=8, handles=[b1, b2])
    save(fig, f'{FIG}/fig3_2.png')
    print('ok fig3_2')


def fig3_3():
    """图3.3 物理词元的不可比性：单价对效值 η 的散点与等值参考线。"""
    eta = by_tier('ste.eta')
    p = by_tier('price.market')
    k, _ = fit_origin(eta, p)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    xs = np.linspace(0, 4.75, 50)
    l1, = ax.plot(xs, k * xs, color=PAL['blue'], lw=1.5,
                  label='实际拟合（过原点等比例线）')
    l2 = ax.axhline(p.mean(), color=PAL['red'], ls='--', lw=1.4,
                    label='词元等值假设下应有的水平线')
    for t, e, v in zip(TIERS, eta, p):
        ax.scatter(e, v, s=52, color=TIER_C[t], edgecolor='white',
                   lw=0.8, zorder=5)
    offs = {'light': (9, 0), 'mid': (9, -2), 'open': (9, -3),
            'flag': (9, -4), 'reason': (-9, 0), 'multi': (9, -12)}
    for t, e, v in zip(TIERS, eta, p):
        ax.annotate(f'{TIER_CN[t]} {v:.2f}', (e, v),
                    textcoords='offset points', xytext=offs[t],
                    ha='right' if t == 'reason' else 'left',
                    va='center', fontsize=7.5, color=TIER_C[t])
    ratio_p = p.max() / p.min()
    ratio_e = eta.max() / eta.min()
    ax.annotate(f'同为 1 枚物理词元 $T$：\n单价相差 {ratio_p:.0f} 倍'
                f'（{p.max():.2f} ／ {p.min():.2f}）\n'
                f'效值 $\\eta$ 相差 {ratio_e:.1f} 倍',
                (2.42, 1.35), fontsize=8, color=PAL['blue'],
                ha='left', va='center', bbox=kbox(PAL['blue']))
    ax.annotate('等值假设与事实不符：\n单价随 $\\eta$ 系统性上升',
                (0.52, 12.6), fontsize=8, color=PAL['red'],
                ha='left', va='center', bbox=kbox(PAL['red']))
    ax.set_xlim(0, 4.85)
    ax.set_ylim(0, 16.2)
    ax.set_xlabel('效值系数 $\\eta$（中型通用级＝1）')
    ax.set_ylabel('市场单价（元／百万物理词元）')
    ax.set_axisbelow(True)
    ax.grid(alpha=0.25, lw=0.6)
    ax.legend(handles=[l1, l2], loc='upper left', fontsize=8)
    save(fig, f'{FIG}/fig3_3.png')
    print('ok fig3_3')


# ============================== 第4章 ==============================
def fig4_1():
    """图4.1 日均词元调用量的演进（对数纵轴，官方锚点与插值点区分）。"""
    v = by_quarter('usage.daily').copy()
    off = R['usage']['official_points']            # 官方发布点位优先
    is_off = np.array([q in off for q in QUARTERS])
    for i, q in enumerate(QUARTERS):
        if q in off:
            v[i] = float(off[q])
    x = np.arange(len(QUARTERS))
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ax.plot(x, v, color=PAL['blue'], lw=1.6, zorder=2)
    ax.plot(x[~is_off], v[~is_off], ls='none', marker='o', ms=5.2,
            mfc='white', mec=PAL['blue'], mew=1.2, zorder=3)
    ax.plot(x[is_off], v[is_off], ls='none', marker='o', ms=8.0,
            color=PAL['red'], zorder=4)
    lab_off = {'2024Q1': (0, 12, 'center'), '2025Q2': (-6, 10, 'right'),
               '2025Q4': (-6, 10, 'right'), '2026Q1': (2, -16, 'left')}
    for i, q in enumerate(QUARTERS):
        if q in off:
            dx, dy, ha = lab_off[q]
            ax.annotate(f'{v[i]:.2f}'.rstrip('0').rstrip('.'),
                        (i, v[i]), textcoords='offset points',
                        xytext=(dx, dy), ha=ha, fontsize=8,
                        color=PAL['red'], bbox=WBOX)
    gx = R['usage']['growth_x']
    ax.annotate(f'2024年初→2026年3月\n日均调用量增至约 {gx:.0f} 倍',
                (1.05, 60), fontsize=8, color=PAL['blue'],
                ha='left', va='center', bbox=kbox(PAL['blue']))
    h1 = Line2D([], [], ls='none', marker='o', ms=7, color=PAL['red'],
                label='官方发布点位')
    h2 = Line2D([], [], ls='none', marker='o', ms=5.2, mfc='white',
                mec=PAL['blue'], mew=1.2, label='校准复算插值')
    ax.legend(handles=[h1, h2], loc='lower right', fontsize=8)
    ax.set_yscale('log')
    ax.set_ylim(0.05, 600)
    ax.set_yticks([0.1, 1, 10, 100])
    plain_log(ax, 'y')
    ax.set_xticks(x)
    ax.set_xticklabels(QUARTERS, fontsize=7.5, rotation=45, ha='right')
    ax.set_xlim(-0.5, 9.5)
    ax.set_xlabel('季度')
    ax.set_ylabel('日均词元调用量（万亿枚／日，对数刻度）')
    ax.set_axisbelow(True)
    ax.grid(axis='y', alpha=0.25, lw=0.6)
    ax.grid(axis='x', visible=False)
    save(fig, f'{FIG}/fig4_1.png')
    print('ok fig4_1')


def fig4_2():
    """图4.2 中国模型周调用量与全球占比（2026年7—8月）。"""
    wk = R['facts_seed']['openrouter_weeks']
    keys = list(wk)
    cn = np.array([wk[k]['cn'] for k in keys])
    gl = [wk[k]['global'] for k in keys]
    x = np.arange(len(keys))

    fig, ax = plt.subplots(figsize=(6.6, 3.7))
    ax.bar(x, cn, width=0.52, color=PAL['blue'], alpha=0.88,
           edgecolor='white', lw=0.6, label='中国模型周调用量')
    for xi, v in zip(x, cn):
        ax.annotate(f'{v:.2f}', (xi, v), textcoords='offset points',
                    xytext=(0, 3), ha='center', fontsize=8, color=PAL['blue'])
    # 有全球总量披露的周次：叠加空心柱表示全球总量
    for xi, g in zip(x, gl):
        if g:
            ax.bar(xi, g, width=0.52, facecolor='none',
                   edgecolor=PAL['gray'], lw=1.1, ls='--', zorder=1)
            ax.annotate(f'全球 {g:.0f}', (xi, g), textcoords='offset points',
                        xytext=(0, 3), ha='center', fontsize=7.5, color=PAL['gray'])
    ax.set_xticks(x)
    ax.set_xticklabels(keys, fontsize=8)
    ax.set_ylabel('周调用量（万亿枚）')
    ax.set_xlabel('统计周次（2026年）')
    ax.set_ylim(0, 82)
    ax.set_xlim(-0.62, len(keys) - 0.38)
    grid_y(ax)

    ax2 = ax.twinx()
    sh = [(wk[k]['cn'] / wk[k]['global'] * 100) if wk[k]['global'] else np.nan
          for k in keys]
    ax2.plot(x, sh, color=PAL['orange'], marker='o', ms=5.5, lw=1.6,
             label='中国模型全球占比')
    for xi, v in zip(x, sh):
        if not np.isnan(v):
            ax2.annotate(f'{v:.1f}%', (xi, v), textcoords='offset points',
                         xytext=(9, -2), fontsize=8, color=PAL['orange'])
    ax2.axhline(50, color=PAL['orange'], ls=':', lw=0.9, alpha=0.7)
    ax2.annotate('50%（与美国持平线）', (len(keys) - 0.55, 51.5), ha='right',
                 fontsize=7.2, color=PAL['orange'])
    ax2.set_ylabel('全球占比（%）', color=PAL['orange'])
    ax2.set_ylim(0, 100)
    ax2.tick_params(axis='y', colors=PAL['orange'])
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(PAL['orange'])

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc='upper left', fontsize=7.6)
    fig.tight_layout()
    save(fig, f'{FIG}/fig4_2.png')
    print('ok fig4_2')


def fig4_3():
    """图4.3 词元消耗的场景结构：应用数量占比与词元用量占比对照。"""
    app = np.array([DF[(DF.series == 'usage.scene_app') & (DF.x == k)]
                    .value.iloc[0] for k in SCENE_KEYS]) * 100
    tok = np.array([DF[(DF.series == 'usage.scene_token') & (DF.x == k)]
                    .value.iloc[0] for k in SCENE_KEYS]) * 100
    x = np.arange(len(SCENE_KEYS))
    w = 0.36
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.bar(x - w / 2, app, w, color=PAL['ltblue'], edgecolor=PAL['blue'],
           lw=0.9, label='应用数量占比')
    ax.bar(x + w / 2, tok, w, color='#F2C8A0', edgecolor=PAL['orange'],
           lw=0.9, label='词元用量占比')
    for xi, v in zip(x - w / 2, app):
        ax.annotate(f'{v:.1f}%', (xi, v), textcoords='offset points',
                    xytext=(0, 2.5), ha='center', fontsize=8,
                    color=PAL['blue'])
    for xi, v in zip(x + w / 2, tok):
        ax.annotate(f'{v:.1f}%', (xi, v), textcoords='offset points',
                    xytext=(0, 2.5), ha='center', fontsize=8,
                    color=PAL['orange'])
    ax.annotate(f'{app[0]:.0f}% 的应用\n消耗了 {tok[0]:.1f}% 的词元',
                xy=(w / 2, tok[0]), xytext=(1.15, 72),
                fontsize=8, color=PAL['orange'], ha='left', va='center',
                bbox=kbox(PAL['orange']),
                arrowprops=dict(arrowstyle='->', color=PAL['orange'],
                                lw=1.0, shrinkA=2, shrinkB=3))
    ax.set_xticks(x)
    ax.set_xticklabels([SCENE_CN[k] for k in SCENE_KEYS], fontsize=8.5)
    ax.set_xlim(-0.6, 3.6)
    ax.set_ylim(0, 92)
    ax.set_ylabel('占比（%）')
    ax.set_xlabel('应用场景类别')
    grid_y(ax)
    ax.legend(loc='upper right', fontsize=8)
    save(fig, f'{FIG}/fig4_3.png')
    print('ok fig4_3')


def fig4_4():
    """图4.4 双面板：（a）词元价格指数的表观下行；（b）六档位市场价（对数）。

    第4章只呈现"表观价格"这一可观测事实；标准词元价格指数 STPI 与两指数
    背离的分解属第7章内容（图7.3、图7.4），此处不重复绘制。
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 3.7),
                                   gridspec_kw={'width_ratios': [1.35, 1]})
    tpi = by_quarter('price.tpi')
    x = np.arange(len(QUARTERS))
    drop = (1.0 - tpi[-1] / tpi[0]) * 100
    ax1.axhline(100, color=PAL['gray'], ls=(0, (4, 3)), lw=0.9, zorder=1)
    ax1.fill_between(x, tpi, 0, color=PAL['blue'], alpha=0.10, lw=0, zorder=1)
    ax1.plot(x, tpi, color=PAL['blue'], marker='o', ms=3.8, lw=1.9, zorder=3,
             label='词元价格指数 TPI（物理词元口径）')
    ax1.annotate(f'{tpi[0]:.0f}', (x[0], tpi[0]), textcoords='offset points',
                 xytext=(7, 3), ha='left', va='bottom', fontsize=8,
                 color=PAL['blue'])
    ax1.annotate(f'{tpi[-1]:.0f}', (x[-1], tpi[-1]),
                 textcoords='offset points', xytext=(-1, 9), ha='center',
                 fontsize=8, color=PAL['blue'])
    ax1.annotate(f'2024Q1—2026Q2\n表观单价累计下降 {drop:.0f}%',
                 (4.75, 66), fontsize=8, color=PAL['blue'],
                 ha='left', va='center', bbox=kbox(PAL['blue']))
    ax1.set_xticks(x)
    ax1.set_xticklabels(QUARTERS, fontsize=7.5, rotation=45, ha='right')
    ax1.set_xlim(-0.4, 9.4)
    ax1.set_ylim(0, 112)
    ax1.set_xlabel('季度')
    ax1.set_ylabel('价格指数（2024Q1＝100）')
    ax1.set_axisbelow(True)
    ax1.grid(axis='y', alpha=0.25, lw=0.6)
    ax1.grid(axis='x', visible=False)
    ax1.legend(loc='upper right', fontsize=8)
    panel_label(ax1, '（a）', x=-0.15)

    p = by_tier('price.market')
    xp = np.arange(len(TIERS))
    ax2.bar(xp, p, width=0.58, color=[TIER_C[t] for t in TIERS], alpha=0.88,
            edgecolor='white', lw=0.6)
    for xi, v in zip(xp, p):
        ax2.annotate(f'{v:.2f}', (xi, v), textcoords='offset points',
                     xytext=(0, 3), ha='center', fontsize=7.5)
    ax2.set_yscale('log')
    ax2.set_ylim(0.2, 42)
    ax2.set_yticks([0.3, 1, 3, 10, 30])
    plain_log(ax2, 'y')
    ax2.set_xticks(xp)
    ax2.set_xticklabels(TIER_LAB, fontsize=7.5, rotation=25, ha='right')
    ax2.set_xlim(-0.62, 5.62)
    ax2.set_ylabel('市场单价（元／百万物理词元，对数刻度）')
    ax2.set_xlabel('模型档位')
    ax2.set_axisbelow(True)
    ax2.grid(axis='y', alpha=0.25, lw=0.6)
    ax2.grid(axis='x', visible=False)
    panel_label(ax2, '（b）', x=-0.24)
    fig.tight_layout()
    save(fig, f'{FIG}/fig4_4.png')
    print('ok fig4_4')


def fig4_5():
    """图4.5 智能算力供给格局（嘉兴底数）：（a）智算规模口径；（b）底数卡片。

    数据口径以 data/facts.md 第 3.2 节核实结论为准：智算规模（低精度折算的
    PFLOPS 口径）与超算峰值（FP64 口径）分列，不并轴、不折算、不相加。
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 3.5),
                                   gridspec_kw={'width_ratios': [1.5, 1]})
    labs = ['约2025年\n已投运', '2026年5月\n已投运',
            '2026年\n已投运', '规划建成后\n（目标值）']
    vals = np.array([4.37, 8.50, 11.80, 27.60])
    y = np.arange(len(labs))[::-1]
    cols = [PAL['ltblue'], PAL['ltblue'], PAL['blue'], 'white']
    for yi, v, c in zip(y, vals, cols):
        ax1.barh(yi, v, height=0.56, color=c, edgecolor=PAL['blue'], lw=0.9,
                 hatch='///' if c == 'white' else None)
    for yi, v in zip(y, vals):
        ax1.annotate(f'{v:.2f}'.rstrip('0').rstrip('.'), (v, yi),
                     textcoords='offset points', xytext=(4, 0), va='center',
                     fontsize=8, color=PAL['blue'])
    ax1.set_yticks(y)
    ax1.set_yticklabels(labs, fontsize=7.5)
    ax1.set_xlim(0, 33)
    ax1.set_ylim(-0.6, 3.6)
    ax1.set_xlabel('智算规模（万 PFLOPS，低精度折算口径）')
    grid_x(ax1)
    panel_label(ax1, '（a）', x=-0.30)

    jx = R['facts_seed']['jiaxing']
    cards = [(f"{jx['万卡级算力中心']:d}", '个', '万卡级智算中心'),
             (f"{jx['算力占浙江省比重'] * 100:.0f}", '%',
              '占浙江省已投运算力（约2025年口径）'),
             (f"{jx['超算峰值(亿亿次/秒)']:d}", '亿亿次／秒',
              '超算中心峰值算力（FP64 口径）')]
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    ec = [PAL['blue'], PAL['teal'], PAL['orange']]
    for i, ((num, unit, name), c) in enumerate(zip(cards, ec)):
        y0 = 0.70 - i * 0.335
        ax2.add_patch(FancyBboxPatch((0.03, y0), 0.94, 0.27,
                                     boxstyle='round,pad=0.012,rounding_size=0.03',
                                     fc='#F5F8FB', ec=c, lw=1.0,
                                     transform=ax2.transAxes, clip_on=False))
        ax2.text(0.10, y0 + 0.155, num, transform=ax2.transAxes,
                 fontproperties=BOLD_NUM, color=c, ha='left', va='center')
        ax2.text(0.10 + 0.055 * len(num) + 0.03, y0 + 0.135, unit,
                 transform=ax2.transAxes, fontsize=8.5, color=c,
                 ha='left', va='center')
        ax2.text(0.10, y0 + 0.055, name, transform=ax2.transAxes,
                 fontsize=8, color='#333333', ha='left', va='center')
    panel_label(ax2, '（b）', x=-0.02)
    fig.tight_layout()
    save(fig, f'{FIG}/fig4_5.png')
    print('ok fig4_5')


# ============================== 第5章 ==============================
def fig5_2():
    """图5.2 六档位三维效值（P/R/S 分组条形）与合成效值系数 η（右轴折线）。"""
    P, Rq, S = by_tier('ste.P'), by_tier('ste.R'), by_tier('ste.S')
    eta = by_tier('ste.eta')
    x = np.arange(len(TIERS))
    w = 0.26
    fig, ax1 = plt.subplots(figsize=(6.9, 4.0))
    b1 = ax1.bar(x - w, P, w, color=PAL['ltblue'], edgecolor=PAL['blue'],
                 lw=0.8, label='$P$  算力强度')
    b2 = ax1.bar(x, Rq, w, color='#F2C8A0', edgecolor=PAL['orange'],
                 lw=0.8, label='$R$  推理质量')
    b3 = ax1.bar(x + w, S, w, color='#A9D2D2', edgecolor=PAL['teal'],
                 lw=0.8, label='$S$  场景效用')
    ax1.set_xticks(x)
    ax1.set_xticklabels(TIER_LAB, fontsize=8)
    ax1.set_xlim(-0.62, 5.62)
    ax1.set_ylim(0, 10.4)
    ax1.set_ylabel('三维效值（中型通用级＝1）')
    ax1.set_xlabel('模型档位')
    ax1.tick_params(axis='y', labelcolor='black')
    grid_y(ax1)

    ax2 = twin_right(ax1, PAL['red'])
    l1, = ax2.plot(x, eta, color=PAL['red'], marker='D', ms=4.6, lw=1.8,
                   label='$\\eta$  合成效值系数（右轴）')
    eta_off = [(0, 9), (0, 9), (0, 9), (0, 9), (13, 3), (0, 9)]
    for xi, v, (dx, dy) in zip(x, eta, eta_off):
        ax2.annotate(f'{v:.2f}', (xi, v), textcoords='offset points',
                     xytext=(dx, dy), ha='left' if dx else 'center',
                     va='center' if dx else 'bottom', fontsize=8,
                     color=PAL['red'], bbox=WBOX)
    ax2.set_ylim(0, 5.6)
    ax2.set_ylabel('合成效值系数 $\\eta$', color=PAL['red'])
    ax1.legend(handles=[b1, b2, b3, l1], loc='upper left', fontsize=8,
               ncol=2, columnspacing=1.1)
    save(fig, f'{FIG}/fig5_2.png')
    print('ok fig5_2')


def fig5_3():
    """图5.3 折算前后单位价格离散度对照（双面板箱线图，同对数刻度）。"""
    raw = [ser(f'pxraw.{t}')[1] for t in TIERS]
    ste = [ser(f'pxste.{t}')[1] for t in TIERS]
    disp = R['ste']['dispersion']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 3.9), sharey=True)

    def draw(ax, data, title_unit):
        bp = ax.boxplot(data, positions=np.arange(1, 7), widths=0.56,
                        patch_artist=True, showfliers=True,
                        medianprops=dict(color='#222222', lw=1.2),
                        whiskerprops=dict(color='#555555', lw=0.9),
                        capprops=dict(color='#555555', lw=0.9),
                        flierprops=dict(marker='o', ms=2.6, mfc='none',
                                        mec='#888888', mew=0.6))
        for patch, t in zip(bp['boxes'], TIERS):
            patch.set_facecolor(TIER_C[t])
            patch.set_alpha(0.32)
            patch.set_edgecolor(TIER_C[t])
            patch.set_linewidth(1.0)
        ax.set_xticks(np.arange(1, 7))
        ax.set_xticklabels(TIER_LAB, fontsize=7.5, rotation=25, ha='right')
        ax.set_xlim(0.4, 6.6)
        ax.set_xlabel('模型档位')
        ax.set_ylabel(title_unit)
        ax.set_axisbelow(True)
        ax.grid(axis='y', alpha=0.25, lw=0.6)
        ax.grid(axis='x', visible=False)

    draw(ax1, raw, '物理词元单价 $p$（元／百万词元，对数刻度）')
    draw(ax2, ste, '标准词元单价 $\\tilde{p}=p/\\eta$（元／百万 STE，对数刻度）')
    ax1.set_yscale('log')
    ax1.set_ylim(0.08, 60)
    ax1.set_yticks([0.1, 0.3, 1, 3, 10, 30])
    plain_log(ax1, 'y')
    ax2.tick_params(axis='y', labelleft=True)
    ax2.set_ylabel('标准词元单价 $\\tilde{p}=p/\\eta$（元／百万 STE，对数刻度）')

    ax1.annotate(f"折算前  CV＝{disp['price_cv_raw']:.2f}", (0.62, 34),
                 fontsize=9, color=PAL['red'], ha='left', va='center',
                 bbox=kbox(PAL['red']))
    ax2.annotate(f"折算后  CV＝{disp['price_cv_ste']:.2f}", (0.62, 34),
                 fontsize=9, color=PAL['green'], ha='left', va='center',
                 bbox=kbox(PAL['green']))
    ax2.annotate('折算后各档位单价\n向同一水平收敛', (6.42, 0.19),
                 fontsize=8, color=PAL['green'], ha='right', va='center',
                 bbox=WBOX)
    panel_label(ax1, '（a）', x=-0.15)
    panel_label(ax2, '（b）', x=-0.15)
    fig.tight_layout()
    save(fig, f'{FIG}/fig5_3.png')
    print('ok fig5_3')


def fig5_4():
    """图5.4 效值系数与市场价格的对应关系：散点＋过原点拟合线＋失衡标注。"""
    eta = by_tier('ste.eta')
    p = by_tier('price.market')
    k, r2 = fit_origin(eta, p)
    resid = p - k * eta
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    xs = np.linspace(0, 4.75, 50)
    ax.plot(xs, k * xs, color=PAL['blue'], lw=1.5, zorder=2,
            label='过原点等比例拟合线  $p=\\tilde{p}_0\\eta$')
    for t, e, v in zip(TIERS, eta, p):
        ax.plot([e, e], [v, k * e], color=PAL['gray'], ls=':', lw=0.9,
                zorder=3)
        ax.scatter(e, v, s=54, color=TIER_C[t], edgecolor='white', lw=0.8,
                   zorder=5)
    offs = {'light': (9, 0), 'mid': (9, -2), 'open': (9, -8),
            'flag': (9, -3), 'reason': (-9, 4), 'multi': (-9, 0)}
    for t, e, v in zip(TIERS, eta, p):
        ax.annotate(TIER_CN[t], (e, v), textcoords='offset points',
                    xytext=offs[t],
                    ha='right' if t in ('reason', 'multi') else 'left',
                    va='center', fontsize=7.5, color=TIER_C[t])
    i_hi = int(np.argmax(resid))
    i_lo = int(np.argmin(resid))
    ax.annotate('效值溢价失衡：%s\n高于等比例线 %.2f 元'
                % (TIER_CN[TIERS[i_hi]], resid[i_hi]),
                xy=(eta[i_hi], (p[i_hi] + k * eta[i_hi]) / 2),
                xytext=(0.40, 9.7), fontsize=8, color=PAL['red'],
                ha='left', va='center', bbox=kbox(PAL['red']),
                arrowprops=dict(arrowstyle='->', color=PAL['red'], lw=1.0,
                                shrinkA=4, shrinkB=3))
    ax.annotate('效值溢价失衡：%s\n低于等比例线 %.2f 元'
                % (TIER_CN[TIERS[i_lo]], abs(resid[i_lo])),
                xy=(eta[i_lo], (p[i_lo] + k * eta[i_lo]) / 2),
                xytext=(3.05, 3.60), fontsize=8, color=PAL['green'],
                ha='left', va='center', bbox=kbox(PAL['green']),
                arrowprops=dict(arrowstyle='->', color=PAL['green'], lw=1.0,
                                shrinkA=4, shrinkB=3))
    fit = R['ste']['fit']
    ax.annotate('$\\tilde{p}_0$＝%.2f 元／百万 STE，$R^2$＝%.2f\n'
                '效值折算函数标定：$R^2$＝%.4f（$N$＝%d）'
                % (k, r2, fit['R2'], fit['N']),
                (0.16, 15.0), fontsize=8, color=PAL['blue'],
                ha='left', va='center', bbox=kbox(PAL['blue']))
    ax.set_xlim(0, 4.85)
    ax.set_ylim(0, 17.0)
    ax.set_xlabel('效值系数 $\\eta$（中型通用级＝1）')
    ax.set_ylabel('市场单价（元／百万物理词元）')
    ax.set_axisbelow(True)
    ax.grid(alpha=0.25, lw=0.6)
    ax.legend(loc='lower right', fontsize=8)
    save(fig, f'{FIG}/fig5_4.png')
    print('ok fig5_4')


# ============================== 第6章 ==============================
def fig6_3():
    """图6.3 同量标准词元在不同场景的价值密度（降序水平条形）。"""
    name, val = ser('price.scene_value', numeric=False)
    idx = np.argsort(val)[::-1]
    name, val = name[idx], val[idx]
    y = np.arange(len(name))[::-1]
    cols = []
    for v in val:
        if v == val.max():
            cols.append(PAL['orange'])
        elif v == val.min():
            cols.append(PAL['gray'])
        else:
            cols.append(PAL['ltblue'])
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.barh(y, val, height=0.62, color=cols, edgecolor=PAL['blue'], lw=0.8)
    for yi, v in zip(y, val):
        ax.annotate(f'{v:.1f}', (v, yi), textcoords='offset points',
                    xytext=(4, 0), va='center', fontsize=8, color='#333333')
    ax.set_yticks(y)
    ax.set_yticklabels(name, fontsize=8.5)
    ax.set_ylim(-0.65, 7.65)
    ax.set_xlim(0, 14.6)
    ax.set_xlabel('单位标准词元的场景价值密度（元／万 STE）')
    ax.set_ylabel('应用场景')
    ratio = val.max() / val.min()
    ax.annotate(f'同为 1 万枚标准词元 $\\tilde{{T}}$：\n'
                f'{name[0]} {val.max():.1f} ／ {name[-1]} {val.min():.1f}'
                f'＝{ratio:.1f} 倍',
                (6.05, 1.75), fontsize=8, color=PAL['orange'],
                ha='left', va='center', bbox=kbox(PAL['orange']))
    grid_x(ax)
    save(fig, f'{FIG}/fig6_3.png')
    print('ok fig6_3')


ALL = [fig2_1, fig3_2, fig3_3, fig4_1, fig4_2, fig4_3, fig4_4, fig4_5,
       fig5_2, fig5_3, fig5_4, fig6_3]

if __name__ == '__main__':
    for f in ALL:
        f()
