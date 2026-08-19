# -*- coding: utf-8 -*-
"""后半部 A 型分析图（16 幅，matplotlib，nature 风格，中文）。

数据一律读取 data/series.csv 与 data/results.json，不得手写数字。
输出 figs/figN_M.png（400 dpi）。图内不含图名、图注与资料来源文字。
符号遵循 DESIGN.md：物理词元 T、标准词元 $\\tilde{T}$、效值系数 $\\eta$、
标准词元价格 $\\tilde{p}$、转化效率 $\\theta$、碳强度 $\\iota$。
"""
import json
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib import font_manager as _fm
from matplotlib import patheffects as pe

from figstyle import save, PAL, SERIES, CJK

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)

DF = pd.read_csv(os.path.join(HERE, 'data', 'series.csv'), dtype={'x': str})
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))

# ---- 局部样式辅助 ----
_BOLD_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
_fm.fontManager.addfont(_BOLD_PATH)
BOLD_FP = _fm.FontProperties(fname=_BOLD_PATH, size=9.5)
BOLD_S = _fm.FontProperties(fname=_BOLD_PATH, size=8.5)

WBOX = dict(boxstyle='round,pad=0.22', fc='white', ec='none', alpha=0.86)
WBOX_E = dict(boxstyle='round,pad=0.28', fc='white', ec='#B8B8B8', lw=0.6, alpha=0.95)

# 六个模型档位（一律用档位名，不得出现商业产品名）
TIERS = ['light', 'mid', 'open', 'flag', 'reason', 'multi']
TIER_CN = {'light': '轻量蒸馏级', 'mid': '中型通用级', 'open': '开源旗舰级',
           'flag': '旗舰闭源级', 'reason': '推理增强级', 'multi': '多模态级'}
TIER_LAB = [TIER_CN[t] for t in TIERS]
# 窄面板用的两行档位标签（避免相邻标签相碰）
TIER_LAB2 = ['轻量\n蒸馏级', '中型\n通用级', '开源\n旗舰级',
             '旗舰\n闭源级', '推理\n增强级', '多模态级\n']


def panel_label(ax, s, x=-0.10, y=1.02):
    ax.text(x, y, s, transform=ax.transAxes, fontproperties=BOLD_FP,
            ha='left', va='bottom')


def ser(name, numeric=True):
    """按 series 名取 (x, value)；numeric=True 时 x 转 float 并排序。"""
    d = DF[DF.series == name]
    v = d.value.astype(float).values
    if numeric:
        x = d.x.astype(float).values
        idx = np.argsort(x)
        return x[idx], v[idx]
    return d.x.values, v


def smap(name):
    """按 series 名取 {x: value} 映射（x 为字符串）。"""
    d = DF[DF.series == name]
    return dict(zip(d.x.values, d.value.astype(float).values))


def tvals(name):
    """按六档位固定顺序取值。"""
    m = smap(name)
    return np.array([m[t] for t in TIERS])


def twin_right(ax1, color):
    """双轴图：右轴轴线、刻度、标签齐全（与左轴对称）。"""
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(True)
    ax2.spines['right'].set_color(color)
    ax2.spines['right'].set_linewidth(0.9)
    ax2.tick_params(axis='y', labelcolor=color, color=color)
    ax2.grid(False)
    return ax2


def stars(p):
    return '***' if p < 0.01 else ('**' if p < 0.05 else ('*' if p < 0.1 else ''))


def waterfall(ax, labels, tops, bottoms, kinds, cols, width=0.58):
    """通用瀑布图：tops/bottoms 为每根柱的上下沿；kinds 中 'abs' 为总量柱。"""
    n = len(labels)
    x = np.arange(n)
    for i in range(n):
        ax.bar(x[i], tops[i] - bottoms[i], width, bottom=bottoms[i],
               color=cols[i], edgecolor='white', lw=0.7, zorder=3)
    # 连接线（水平虚线）：画在「本柱结束时的累计水平」——
    # 总量柱取柱顶，流量柱取其下沿，避免连接线从柱腰引出
    for i in range(n - 1):
        yy = tops[i] if kinds[i] == 'abs' else bottoms[i]
        ax.plot([x[i] + width / 2, x[i + 1] - width / 2], [yy, yy],
                color=PAL['gray'], lw=0.8, ls=(0, (3, 2)), zorder=2)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    return x


# ============================ 第7章 ============================
def fig7_2():
    """图7.2 六档位价格三层分解（堆叠条形＋市场价合计）。"""
    floor, prem, rent = tvals('price.floor'), tvals('price.premium'), tvals('price.rent')
    mkt = tvals('price.market')
    cols = [PAL['ltblue'], PAL['teal'], PAL['gold']]
    tcol = ['#1F3864', 'white', 'white']
    labs = ['成本底价层（算力＋能源）', '效值溢价层（模型能力）', '场景租金层（可占有价值）']
    x = np.arange(6)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.9, 3.6),
                                   gridspec_kw={'width_ratios': [1.12, 1]})
    # （a）绝对值堆叠
    bot = np.zeros(6)
    for lay, c, lb in zip([floor, prem, rent], cols, labs):
        ax1.bar(x, lay, 0.58, bottom=bot, color=c, edgecolor='white', lw=0.7, label=lb)
        bot = bot + lay
    for xi, m in zip(x, mkt):
        ax1.annotate(f'{m:.2f}', (xi, m), textcoords='offset points', xytext=(0, 3.5),
                     ha='center', fontsize=8, color='#333333')
    ax1.set_xticks(x)
    ax1.set_xticklabels(TIER_LAB2, fontsize=7.6)
    ax1.set_ylabel('价格（元／百万物理词元）')
    ax1.set_ylim(0, 16.6)
    ax1.legend(loc='upper left', fontsize=7.4, handlelength=1.5, labelspacing=0.35)
    ax1.annotate('柱顶数值为市场价 $p$ 合计', (0.03, 0.62), xycoords='axes fraction',
                 fontsize=7.5, color=PAL['gray'])
    panel_label(ax1, '（a）价格水平的三层分解')
    # （b）结构占比
    sh = np.vstack([floor, prem, rent]) / mkt * 100.0
    bot = np.zeros(6)
    for i in range(3):
        ax2.bar(x, sh[i], 0.58, bottom=bot, color=cols[i], edgecolor='white', lw=0.7)
        for xi, (b, h) in enumerate(zip(bot, sh[i])):
            ax2.annotate(f'{h:.0f}%', (xi, b + h / 2), ha='center', va='center',
                         fontsize=7.4, color=tcol[i])
        bot = bot + sh[i]
    ax2.set_xticks(x)
    ax2.set_xticklabels(TIER_LAB2, fontsize=7.6)
    ax2.set_ylabel('各层占市场价的比重（%）')
    ax2.set_ylim(0, 100)
    ax2.set_yticks([0, 20, 40, 60, 80, 100])
    panel_label(ax2, '（b）价格结构的档位差异')
    fig.tight_layout(w_pad=1.8)
    save(fig, f'{FIG}/fig7_2.png')
    print('ok fig7_2')


def fig7_3():
    """图7.3 词元价格指数 TPI 与标准词元价格指数 STPI（含背离阴影）。"""
    m_t, m_s = smap('price.tpi'), smap('price.stpi')
    qs = list(m_t.keys())
    tpi = np.array([m_t[q] for q in qs])
    stpi = np.array([m_s[q] for q in qs])
    x = np.arange(len(qs))
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    ax.fill_between(x, tpi, stpi, color=PAL['gray'], alpha=0.16, lw=0, zorder=1)
    ax.axhline(100, color=PAL['gray'], lw=0.8, ls=(0, (4, 3)), zorder=1)
    ax.plot(x, tpi, color=PAL['orange'], marker='o', ms=4.2, lw=1.9, zorder=4,
            label='词元价格指数 TPI（物理词元口径）')
    ax.plot(x, stpi, color=PAL['blue'], marker='s', ms=4.0, lw=1.9, zorder=4,
            label='标准词元价格指数 STPI（效值折算口径）')
    ax.annotate(f'{tpi[-1]:.0f}', (x[-1], tpi[-1]), textcoords='offset points',
                xytext=(0, -13), ha='center', fontsize=9, color=PAL['orange'])
    ax.annotate(f'{stpi[-1]:.0f}', (x[-1], stpi[-1]), textcoords='offset points',
                xytext=(0, 7), ha='center', fontsize=9, color=PAL['blue'])
    gap = stpi[-1] - tpi[-1]
    ax.annotate('', xy=(x[-1] + 0.42, tpi[-1]), xytext=(x[-1] + 0.42, stpi[-1]),
                arrowprops=dict(arrowstyle='<->', color='#555555', lw=0.9))
    ax.annotate(f'背离\n{gap:.0f} 个\n指数点', (x[-1] + 0.58, (tpi[-1] + stpi[-1]) / 2),
                ha='left', va='center', fontsize=7.8, color='#555555')
    ax.annotate('阴影＝两指数背离，\n即效值提升带来的表观降价部分',
                xy=(4.6, 56), xytext=(3.5, 84), fontsize=8, color='#444444',
                bbox=WBOX, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', color=PAL['gray'], lw=0.8))
    ax.set_xticks(x)
    ax.set_xticklabels(qs, fontsize=7.6)
    ax.set_xlim(-0.45, len(qs) + 0.75)
    ax.set_ylim(0, 112)
    ax.set_xlabel('季度')
    ax.set_ylabel('价格指数（2024Q1＝100）')
    ax.legend(loc='lower left', fontsize=8)
    save(fig, f'{FIG}/fig7_3.png')
    print('ok fig7_3')


def fig7_4():
    """图7.4 表观降价的来源分解（瀑布图）。"""
    m_t = smap('price.tpi')
    qs = list(m_t.keys())
    start, end = m_t[qs[0]], m_t[qs[-1]]
    dec = R['price']['decomp']
    drop = start - end                       # 79 个指数点
    d_eta = drop * dec['eta_gain']           # 效值提升贡献
    d_cut = drop * dec['pure_price_cut']     # 真实降价贡献
    tops = [start, start, start - d_eta, end]
    bots = [0.0, start - d_eta, end, 0.0]
    kinds = ['abs', 'flow', 'flow', 'abs']
    cols = [PAL['ltblue'], PAL['teal'], PAL['orange'], PAL['blue']]
    labs = [f'{qs[0]}\n物理词元\n价格指数', '效值提升贡献\n（同价买到\n更强词元）',
            '真实降价贡献\n（单位效值\n实际降价）', f'{qs[-1]}\n物理词元\n价格指数']
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    x = waterfall(ax, labs, tops, bots, kinds, cols)
    ax.set_xticklabels(labs, fontsize=7.8)
    ax.annotate(f'{start:.0f}', (x[0], start), textcoords='offset points',
                xytext=(0, 4), ha='center', fontsize=9, color='#333333')
    ax.annotate(f'{end:.0f}', (x[3], end), textcoords='offset points',
                xytext=(0, 4), ha='center', fontsize=9, color='#333333')
    ax.annotate(f'−{d_eta:.1f} 点\n（{dec["eta_gain"]*100:.0f}%）',
                (x[1], (tops[1] + bots[1]) / 2), ha='center', va='center',
                fontsize=8.4, color='white')
    ax.annotate(f'−{d_cut:.1f} 点\n（{dec["pure_price_cut"]*100:.0f}%）',
                (x[2], (tops[2] + bots[2]) / 2), ha='center', va='center',
                fontsize=8.4, color='white')
    # 累计降幅括号
    ax.annotate('', xy=(3.52, end), xytext=(3.52, start),
                arrowprops=dict(arrowstyle='<->', color='#555555', lw=0.9))
    ax.plot([3.0, 3.52], [start, start], color='#999999', lw=0.7, ls=(0, (3, 2)))
    ax.plot([3.0, 3.52], [end, end], color='#999999', lw=0.7, ls=(0, (3, 2)))
    ax.annotate(f'累计降幅\n{drop:.0f} 个指数点\n（−{drop:.0f}%）', (3.62, (start + end) / 2),
                ha='left', va='center', fontsize=8, color='#444444')
    ax.set_ylabel('价格指数（2024Q1＝100）')
    ax.set_ylim(0, 116)
    ax.set_xlim(-0.55, 4.55)
    save(fig, f'{FIG}/fig7_4.png')
    print('ok fig7_4')


# ============================ 第8章 ============================
def fig8_2():
    """图8.2 企业词元需求曲线与价格弹性（内嵌分行业弹性）。"""
    _, lnp = ser('demand.lnp')
    _, lnq = ser('demand.lnq')
    el = R['price']['elasticity']
    b, lo, hi = el['coef'], el['ci'][0], el['ci'][1]
    mp, mq = lnp.mean(), lnq.mean()
    xs = np.linspace(lnp.min() - 0.12, lnp.max() + 0.12, 60)
    yfit = mq + b * (xs - mp)
    ylo = mq + lo * (xs - mp)
    yhi = mq + hi * (xs - mp)
    fig, ax = plt.subplots(figsize=(6.3, 4.0))
    ax.scatter(lnp, lnq, s=15, color=PAL['blue'], alpha=0.42, lw=0, zorder=2)
    ax.fill_between(xs, np.minimum(ylo, yhi), np.maximum(ylo, yhi),
                    color=PAL['orange'], alpha=0.14, lw=0, zorder=1)
    ax.plot(xs, yfit, color=PAL['orange'], lw=2.0, zorder=3)
    ax.set_xlabel('词元价格对数 $\\ln p$（元／百万物理词元）')
    ax.set_ylabel('企业词元需求量对数 $\\ln T$')
    ax.set_xlim(lnp.min() - 0.25, lnp.max() + 0.25)
    ax.set_ylim(lnq.min() - 0.4, lnq.max() + 1.5)
    ax.annotate(f'需求价格弹性 $\\varepsilon$＝{b:.2f}\n'
                f'（SE {el["se"]:.2f}，t＝{el["t"]:.2f}）\n'
                f'95% 置信区间 [{lo:.2f}, {hi:.2f}]\n'
                f'$R^2$＝{el["R2"]:.2f}，N＝{el["N"]}（回归样本）',
                (0.025, 0.045), xycoords='axes fraction', fontsize=8,
                ha='left', va='bottom', bbox=WBOX_E)
    ax.legend(handles=[
        Line2D([], [], color=PAL['blue'], marker='o', ms=4, ls='none', alpha=0.5,
               label='企业—季度观测'),
        Line2D([], [], color=PAL['orange'], lw=2.0, label='对数需求拟合线'),
        Patch(fc=PAL['orange'], alpha=0.18, ec='none', label='弹性 95% 置信带')],
        loc='lower left', bbox_to_anchor=(0.0, 0.30), fontsize=7.6)
    # 内嵌小图：分行业弹性绝对值
    ins = ax.inset_axes([0.545, 0.575, 0.435, 0.395])
    names, vals = ser('price.elas', numeric=False)
    order = np.argsort(np.abs(vals))
    names, vals = names[order], vals[order]
    yy = np.arange(len(names))
    ins.barh(yy, np.abs(vals), 0.6, color=PAL['teal'], alpha=0.85,
             edgecolor=PAL['teal'], lw=0.7)
    for i, v in enumerate(vals):
        ins.annotate(f'{v:.2f}', (abs(v), i), textcoords='offset points',
                     xytext=(3, 0), va='center', fontsize=6.8, color='#333333')
    ins.axvline(abs(b), color=PAL['orange'], lw=1.1, ls=(0, (3, 2)))
    ins.annotate(f'总体 {b:.2f}', (abs(b), len(names) - 0.35), fontsize=6.6,
                 color=PAL['orange'], ha='center', va='bottom')
    ins.set_yticks(yy)
    ins.set_yticklabels(names, fontsize=7)
    ins.set_xlim(0, 2.25)
    ins.set_ylim(-0.6, len(names) - 0.05)
    ins.set_xlabel('分行业弹性绝对值 |$\\varepsilon$|', fontsize=7)
    ins.tick_params(axis='x', labelsize=6.6)
    ins.grid(axis='x', alpha=0.2)
    ins.set_facecolor('white')
    for sp in ('top', 'right'):
        ins.spines[sp].set_visible(False)
    save(fig, f'{FIG}/fig8_2.png')
    print('ok fig8_2')


def fig8_3():
    """图8.3 市场集中度演化（左）与长期平均成本曲线（右）。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 3.5),
                                   gridspec_kw={'width_ratios': [0.85, 1.15]})
    # （a）HHI
    xh, hhi = ser('market.hhi')
    y0, y1 = 0.08, 0.42
    bands = [(0.25, 0.42, '#F2DCDC', '高度集中'), (0.15, 0.25, '#F5EBD8', '中度集中'),
             (0.0, 0.15, '#E3EFE3', '竞争性市场')]
    for lo, hi, c, lab in bands:
        ax1.axhspan(lo, hi, color=c, alpha=0.75, lw=0, zorder=0)
        ymid = (max(lo, y0) + min(hi, y1)) / 2
        ax1.annotate(lab, (2026.42, ymid), fontsize=7.2, color='#666666',
                     ha='right', va='center', zorder=1)
    ax1.plot(xh, hhi, color=PAL['blue'], marker='o', ms=5.5, lw=2.0, zorder=3)
    for xi, vi in zip(xh, hhi):
        ax1.annotate(f'{vi:.2f}', (xi, vi), textcoords='offset points', xytext=(0, 7),
                     ha='center', fontsize=8.2, color=PAL['blue'], bbox=WBOX)
    ax1.set_xticks(xh.astype(int))
    ax1.set_xlim(2023.7, 2026.45)
    ax1.set_ylim(0.08, 0.42)
    ax1.set_xlabel('年份')
    ax1.set_ylabel('赫芬达尔—赫希曼指数 HHI')
    ax1.grid(axis='y', alpha=0.2)
    panel_label(ax1, '（a）模型服务市场集中度')
    # （b）长期平均成本
    q, lac = ser('market.lac_q')
    mes = R['market']['mes']['daily_ste_yi']
    lmes = R['market']['mes']['lac_at_mes']
    ax2.axvspan(q.min(), mes, color=PAL['ltblue'], alpha=0.14, lw=0)
    ax2.plot(q, lac, color=PAL['blue'], lw=2.0, zorder=3)
    ax2.plot([mes], [lmes], marker='o', ms=6, mfc='white', mec=PAL['red'], mew=1.6,
             ls='none', zorder=4)
    ax2.axvline(mes, color=PAL['red'], lw=0.9, ls=(0, (3, 2)), zorder=2)
    ax2.axhline(lmes, color=PAL['red'], lw=0.9, ls=(0, (3, 2)), zorder=2)
    ax2.annotate(f'最小有效规模 MES＝{mes:.1f} 亿枚／日\n'
                 f'（此处 LAC＝{lmes:.2f} 元／百万 $\\tilde{{T}}$）',
                 xy=(mes, lmes), xytext=(1.5, 1.86), fontsize=8, color='#333333',
                 ha='left', va='top',
                 arrowprops=dict(arrowstyle='-', color=PAL['gray'], lw=0.8,
                                 shrinkB=6))
    ax2.annotate('规模经济区', (0.62, 0.40), fontsize=7.6, color=PAL['blue'], ha='center')
    ax2.annotate('规模不经济区', (2.6, 0.40), fontsize=7.6, color=PAL['gray'], ha='center')
    ax2.set_xlabel('日产标准词元规模（亿枚／日）')
    ax2.set_ylabel('长期平均成本 LAC（元／百万 $\\tilde{T}$）')
    ax2.set_xlim(0, 4.15)
    ax2.set_ylim(0.3, 2.05)
    panel_label(ax2, '（b）词元工厂的长期平均成本', x=-0.09)
    fig.tight_layout(w_pad=2.0)
    save(fig, f'{FIG}/fig8_3.png')
    print('ok fig8_3')


# ============================ 第9章 ============================
def fig9_2():
    """图9.2 算力利用率的四项损失分解（相对损失率逐级相乘的瀑布图）。"""
    e = R['eff']
    nom = e['nominal_util'] * 100
    keys = [('idle', '空转损失'), ('batch', '批次损失'),
            ('match', '匹配损失'), ('value', '效值损失')]
    rates = [e['losses'][k] for k, _ in keys]
    run = nom
    tops, bots, cols, labs, kinds = [nom], [0.0], [PAL['ltblue']], ['名义算力\n利用率'], ['abs']
    drops = []
    for (k, cn), r in zip(keys, rates):
        nxt = run * (1 - r)
        tops.append(run)
        bots.append(nxt)
        cols.append(PAL['orange'])
        labs.append(cn)
        kinds.append('flow')
        drops.append(run - nxt)
        run = nxt
    eff = e['effective_util'] * 100
    tops.append(eff)
    bots.append(0.0)
    cols.append(PAL['teal'])
    labs.append('有效效值\n利用率')
    kinds.append('abs')
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    x = waterfall(ax, labs, tops, bots, kinds, cols)
    ax.set_xticklabels(labs, fontsize=8)
    ax.annotate(f'{nom:.0f}%', (x[0], nom), textcoords='offset points', xytext=(0, 4),
                ha='center', fontsize=9, color='#333333')
    ax.annotate(f'{eff:.0f}%', (x[-1], eff), textcoords='offset points', xytext=(0, 4),
                ha='center', fontsize=9, color='#333333')
    for i, (r, d) in enumerate(zip(rates, drops), start=1):
        ax.annotate(f'−{r*100:.0f}%', (x[i], (tops[i] + bots[i]) / 2), ha='center',
                    va='center', fontsize=8.4, color='white')
        ax.annotate(f'−{d:.1f} pp', (x[i], bots[i]), textcoords='offset points',
                    xytext=(0, -11), ha='center', va='center', fontsize=7.4,
                    color='#555555')
    ax.annotate('各项为相对损失率，逐级相乘：\n'
                '$0.62\\times(1-0.18)(1-0.09)(1-0.12)(1-0.07)\\approx 0.38$',
                (0.985, 0.965), xycoords='axes fraction', fontsize=7.8,
                ha='right', va='top', color='#444444', bbox=WBOX_E)
    ax.set_ylabel('算力利用率（%）')
    ax.set_ylim(0, 78)
    ax.set_xlim(-0.6, len(labs) - 0.4)
    save(fig, f'{FIG}/fig9_2.png')
    print('ok fig9_2')


def fig9_3():
    """图9.3 统一调度的效率改进（分档位分组条形＋总体参考线）。"""
    now, sched = tvals('eff.util_now') * 100, tvals('eff.util_sched') * 100
    s = R['eff']['sched']
    over_now = R['eff']['effective_util'] * 100
    over_sch = s['matched_util'] * 100
    ub = s['upper_bound'] * 100
    x = np.arange(6)
    w = 0.36
    fig, ax = plt.subplots(figsize=(6.9, 3.9))
    ax.bar(x - w / 2, now, w, color=PAL['ltblue'], edgecolor=PAL['blue'], lw=0.8,
           label='现状：分档位有效效值利用率', zorder=3)
    ax.bar(x + w / 2, sched, w, color=PAL['teal'], edgecolor='#1F5F5F', lw=0.8,
           label='统一调度后：任务—模型最优匹配', zorder=3)
    lbox = dict(boxstyle='round,pad=0.24', fc='white', ec='none', alpha=1.0)
    for xi, a, b in zip(x, now, sched):
        ax.annotate(f'{a:.0f}', (xi - w / 2, a), textcoords='offset points',
                    xytext=(0, 2.5), ha='center', fontsize=7.4, color=PAL['blue'],
                    bbox=lbox, zorder=5)
        ax.annotate(f'{b:.0f}', (xi + w / 2, b), textcoords='offset points',
                    xytext=(0, 2.5), ha='center', fontsize=7.4, color='#1F5F5F',
                    bbox=lbox, zorder=5)
        ax.annotate(f'＋{b - a:.0f} pp', (xi + w / 2, b - 2.0), ha='center', va='top',
                    fontsize=7.2, color='white', rotation=90, zorder=5)
    for yv, c, lab in [(over_now, PAL['blue'], f'总体现状 {over_now:.0f}%'),
                       (over_sch, PAL['teal'], f'统一调度后 {over_sch:.0f}%'),
                       (ub, PAL['red'], f'理论上界 {ub:.0f}%')]:
        ax.axhline(yv, color=c, lw=0.9, ls=(0, (4, 3)), zorder=2, xmax=0.79)
        ax.annotate(lab, (5.55, yv), fontsize=7.6, color=c, ha='left', va='center')
    ax.set_xticks(x)
    ax.set_xticklabels(TIER_LAB, fontsize=8)
    ax.set_ylabel('有效效值利用率（%）')
    ax.set_ylim(0, 74)
    ax.set_xlim(-0.6, 6.85)
    ax.legend(loc='upper left', fontsize=7.8, ncol=1)
    save(fig, f'{FIG}/fig9_3.png')
    print('ok fig9_3')


def fig9_4():
    """图9.4 推理服务的时延—成本权衡（双轴两侧完整）。"""
    b, lat = ser('eff.batch_lat')
    _, cost = ser('eff.batch_cost')
    # 最优区间判据：等权归一化「时延＋成本」综合指标最小的相邻两点
    nl = (lat - lat.min()) / (lat.max() - lat.min())
    nc = (cost - cost.min()) / (cost.max() - cost.min())
    obj = nl + nc
    i0 = int(np.argmin(obj))
    j = i0 + 1 if (i0 + 1 < len(obj) and obj[i0 + 1] <= obj[i0 - 1]) else i0 - 1
    lo, hi = sorted([b[i0], b[j]])
    fig, ax1 = plt.subplots(figsize=(6.6, 3.9))
    ax1.axvspan(lo, hi, color=PAL['gold'], alpha=0.13, lw=0, zorder=0)
    ax1.plot(b, lat, color=PAL['blue'], marker='o', ms=4.4, lw=1.9, zorder=3)
    ax1.set_xscale('log', base=2)
    ax1.set_xticks(b)
    ax1.set_xticklabels([f'{int(v)}' for v in b])
    ax1.set_xlabel('推理批大小（对数刻度，请求数／批）')
    ax1.set_ylabel('平均时延（ms）', color=PAL['blue'])
    ax1.tick_params(axis='y', labelcolor=PAL['blue'])
    ax1.set_ylim(0, 830)
    ax1.set_xlim(0.75, 340)
    ax1.spines['left'].set_color(PAL['blue'])
    ax2 = twin_right(ax1, PAL['orange'])
    ax2.plot(b, cost, color=PAL['orange'], marker='s', ms=4.2, lw=1.9, ls='--', zorder=3)
    ax2.set_ylabel('相对单位成本（批大小 256 时＝1）', color=PAL['orange'])
    ax2.set_ylim(0.6, 4.4)
    ilo, ihi = min(i0, j), max(i0, j)
    ax1.annotate(f'{lat[ilo]:.0f} ms', (b[ilo], lat[ilo]), textcoords='offset points',
                 xytext=(-5, 10), ha='right', fontsize=7.6, color=PAL['blue'])
    ax1.annotate(f'{lat[ihi]:.0f} ms', (b[ihi], lat[ihi]), textcoords='offset points',
                 xytext=(-5, 10), ha='right', fontsize=7.6, color=PAL['blue'])
    ax2.annotate(f'{cost[ilo]:.2f}', (b[ilo], cost[ilo]), textcoords='offset points',
                 xytext=(-5, -13), ha='right', fontsize=7.6, color=PAL['orange'])
    ax2.annotate(f'{cost[ihi]:.2f}', (b[ihi], cost[ihi]), textcoords='offset points',
                 xytext=(6, -11), ha='left', fontsize=7.6, color=PAL['orange'])
    ax1.annotate(f'最优批大小区间 {int(lo)}—{int(hi)}\n'
                 f'（成本已降至下界的 {cost[max(i0, j)]:.2f} 倍以内，\n'
                 f'平均时延仍低于 {lat[max(i0, j)]:.0f} ms）',
                 (np.sqrt(lo * hi), 640), ha='center', va='center', fontsize=7.8,
                 color='#444444', bbox=WBOX_E)
    ax1.legend(handles=[
        Line2D([], [], color=PAL['blue'], marker='o', ms=4.2, label='平均时延（左轴）'),
        Line2D([], [], color=PAL['orange'], marker='s', ms=4.0, ls='--',
               label='相对单位成本（右轴）')],
        loc='lower left', bbox_to_anchor=(0.012, 0.145), fontsize=7.8)
    save(fig, f'{FIG}/fig9_4.png')
    print('ok fig9_4')


# ============================ 第10章 ============================
GAME_LAB = [('x', '$x$ 平台深度运营', PAL['blue'], '-'),
            ('y', '$y$ 企业深度采纳', PAL['orange'], '-'),
            ('z', '$z$ 政府强激励', PAL['green'], '--')]


def fig10_3():
    """图10.3 三方演化博弈的三情景轨迹。"""
    p = R['game']['params']
    conv = R['game']['conv']
    scens = [('scenA', f'（a）情景A：$R_F$＝{p["RF_base"]}（基准）'),
             ('scenB', f'（b）情景B：$R_F$＝{p["RF_hi"]}'),
             ('scenC', f'（c）情景C：$R_F$＝{p["RF_hi"]} 且 $c_F$＝0.7')]
    fig, axes = plt.subplots(1, 3, figsize=(8.8, 3.0), sharey=True)
    for ax, (sc, lab) in zip(axes, scens):
        for var, cn, c, ls in GAME_LAB:
            t, v = ser(f'game.{sc}.{var}')
            ax.plot(t, v, color=c, lw=1.8, ls=ls)
        cv = conv[sc]
        if sc == 'scenA':
            thr = R['game']['threshold']['RF_crit']
            ax.annotate(f'$R_F$＝{p["RF_base"]}＜临界值 $R_F^c$＝{thr}\n'
                        '窗口内未收敛\n（$z\\to$0.995，补贴无法退出）',
                        (40, 0.50), ha='center', va='center', fontsize=7.4,
                        color='#444444', bbox=WBOX)
        else:
            ax.axvline(cv['T'], color=PAL['gray'], lw=0.9, ls=(0, (2, 2)))
            ax.annotate(f'收敛期 T≈{cv["T"]:.1f}', (cv['T'] + 1.2, 0.44), fontsize=7.4,
                        color='#444444', ha='left', va='center', bbox=WBOX)
        ax.annotate(f'终值 $x$＝{cv["x"]:.3f}，$y$＝{cv["y"]:.3f}，$z$＝{cv["z"]:.3f}',
                    (0.5, -0.30), xycoords='axes fraction', ha='center', va='top',
                    fontsize=7.2, color='#444444')
        ax.set_xlabel('演化期次 $t$')
        ax.set_xlim(0, 60)
        ax.set_xticks(np.arange(0, 61, 15))
        ax.set_ylim(-0.04, 1.08)
        panel_label(ax, lab, x=-0.02, y=1.02)
    axes[0].set_ylabel('选择该策略的主体比例')
    axes[0].legend(handles=[Line2D([], [], color=c, ls=ls, lw=1.8, label=cn)
                            for _, cn, c, ls in GAME_LAB],
                   loc='lower right', bbox_to_anchor=(0.99, 0.04), fontsize=7.4)
    fig.tight_layout(w_pad=1.5)
    fig.subplots_adjust(bottom=0.30)
    save(fig, f'{FIG}/fig10_3.png')
    print('ok fig10_3')


def fig10_4():
    """图10.4 制度要件的 AHP 权重（准则层＋「五个统一」组合权重）。"""
    cri, itm = R['ahp']['criteria'], R['ahp']['items']
    cn_c, cn_i = R['ahp']['criteria_cn'], dict(R['ahp']['item_cn'])
    # 方案层名称与 RESULTS_SPEC／图10.2「五个统一」表述保持一致（标签不用西文缩写）
    cn_i['entry'] = '统一入口'
    ck, cv = ser('ahp.criteria', numeric=False)
    ik, iv = ser('ahp.items', numeric=False)
    oc = np.argsort(cv)          # 横条自下而上升序＝视觉上降序
    oi = np.argsort(iv)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.9, 3.4),
                                   gridspec_kw={'width_ratios': [1, 1.12]})
    y1 = np.arange(len(ck))
    ax1.barh(y1, cv[oc], 0.55, color=PAL['ltblue'], edgecolor=PAL['blue'], lw=0.8)
    for i, v in enumerate(cv[oc]):
        ax1.annotate(f'{v:.3f}', (v, i), textcoords='offset points', xytext=(4, 0),
                     va='center', fontsize=8, color='#333333')
    ax1.set_yticks(y1)
    ax1.set_yticklabels([cn_c[ck[i]] for i in oc], fontsize=8.5)
    ax1.set_xlim(0, 0.52)
    ax1.set_ylim(-1.35, len(ck) - 0.35)
    ax1.set_xlabel('准则层权重')
    ax1.grid(axis='x', alpha=0.2)
    ax1.grid(axis='y', visible=False)
    ax1.annotate(f'CR＝{cri["CR"]:.3f}＜0.1，$\\lambda_{{max}}$＝{cri["lambda_max"]:.3f}\n'
                 f'专家 N＝{R["ahp"]["experts"]["n"]}，'
                 f'肯德尔 $W$＝{R["ahp"]["experts"]["kendall_w"]:.2f}',
                 (0.005, -0.72), ha='left', va='center',
                 fontsize=7.6, color='#444444')
    panel_label(ax1, '（a）准则层', x=-0.30)
    y2 = np.arange(len(ik))
    ax2.barh(y2, iv[oi], 0.55, color=PAL['teal'], edgecolor='#1F5F5F', lw=0.8)
    for i, v in enumerate(iv[oi]):
        ax2.annotate(f'{v:.3f}', (v, i), textcoords='offset points', xytext=(4, 0),
                     va='center', fontsize=8, color='#333333')
    ax2.set_yticks(y2)
    ax2.set_yticklabels([cn_i[ik[i]] for i in oi], fontsize=8.5)
    ax2.set_xlim(0, 0.35)
    ax2.set_ylim(-1.35, len(ik) - 0.35)
    ax2.set_xlabel('方案层组合权重')
    ax2.grid(axis='x', alpha=0.2)
    ax2.grid(axis='y', visible=False)
    ax2.annotate(f'CR＝{itm["CR"]:.3f}＜0.1（通过一致性检验）', (0.005, -0.72),
                 ha='left', va='center', fontsize=7.6, color='#444444')
    panel_label(ax2, '（b）“五个统一”制度要件', x=-0.34)
    fig.tight_layout(w_pad=2.6)
    save(fig, f'{FIG}/fig10_4.png')
    print('ok fig10_4')


# ============================ 第11章 ============================
def fig11_2():
    """图11.2 分档位能耗强度与碳强度（双轴两侧完整）。"""
    en = tvals('green.energy')
    io = tvals('green.iota')
    gf = R['green']['carbon']['green_factor']
    grid = R['green']['carbon']['grid_factor']
    io_g = en * gf                       # 全绿电供电口径（由排放因子折算）
    io_top = 15.6                        # 右轴量程：使折线与柱顶拉开距离
    x = np.arange(6)
    fig, ax1 = plt.subplots(figsize=(6.8, 3.9))
    ax1.bar(x, en, 0.56, color=PAL['ltblue'], edgecolor=PAL['blue'], lw=0.8, zorder=3)
    for xi, v in zip(x, en):
        ax1.annotate(f'{v:.1f}', (xi, v), textcoords='offset points', xytext=(0, 3),
                     ha='center', fontsize=7.6, color=PAL['blue'])
    ax1.set_xticks(x)
    ax1.set_xticklabels(TIER_LAB, fontsize=8)
    ax1.set_ylabel('能耗强度（kWh／百万 $\\tilde{T}$）', color=PAL['blue'])
    ax1.tick_params(axis='y', labelcolor=PAL['blue'])
    ax1.spines['left'].set_color(PAL['blue'])
    ax1.set_ylim(0, 21)
    ax1.set_xlim(-0.62, 5.62)
    ax2 = twin_right(ax1, PAL['orange'])
    ax2.plot(x, io, color=PAL['orange'], marker='o', ms=4.6, lw=1.9, zorder=4)
    ax2.plot(x, io_g, color=PAL['green'], marker='^', ms=4.4, lw=1.6, ls='--', zorder=4)
    halo = [pe.withStroke(linewidth=2.6, foreground='white')]
    for xi, v in zip(x, io):
        # 贴近横轴的点改为向右上标注，避免压住刻度标签与全绿电折线
        if v / io_top < 0.08:
            kw = dict(xytext=(8, 7), ha='left', va='bottom')
        else:
            kw = dict(xytext=(0, -9), ha='center', va='top')
        # 用白色描边光晕代替实心白框，避免在柱体上「挖洞」、遮住折线
        ax2.annotate(f'{v:.2f}', (xi, v), textcoords='offset points',
                     fontsize=7.4, color=PAL['orange'], path_effects=halo,
                     zorder=6, **kw)
    ax2.set_ylabel('碳强度 $\\iota$（gCO$_2$e／千 $\\tilde{T}$）', color=PAL['orange'])
    ax2.set_ylim(0, io_top)
    ax2.annotate(f'电网排放因子 {grid} kgCO$_2$／kWh；绿电 {gf} kgCO$_2$／kWh，\n'
                 f'全绿电供电可将碳强度降至电网口径的 {gf / grid * 100:.1f}%',
                 (0.02, 0.985), xycoords='axes fraction', ha='left', va='top',
                 fontsize=7.6, color='#444444', bbox=WBOX_E)
    ax1.legend(handles=[
        Patch(fc=PAL['ltblue'], ec=PAL['blue'], label='能耗强度（左轴）'),
        Line2D([], [], color=PAL['orange'], marker='o', ms=4.4,
               label='碳强度 $\\iota$：电网供电口径（右轴）'),
        Line2D([], [], color=PAL['green'], marker='^', ms=4.2, ls='--',
               label='碳强度 $\\iota$：全绿电供电口径（右轴）')],
        loc='upper left', bbox_to_anchor=(0.02, 0.855), fontsize=7.6)
    save(fig, f'{FIG}/fig11_2.png')
    print('ok fig11_2')


def fig11_3():
    """图11.3 绿电占比提升下的碳强度情景（2026—2035）。"""
    th = R['green']['threshold_iota']
    scen = [('green.scen_base', '基准情景：绿电占比按现有趋势提高', PAL['orange'], '-', 'o'),
            ('green.scen_green', '绿色情景：绿电直供＋PUE 优化', PAL['green'], '--', 's'),
            ('green.scen_deep', '深度情景：绿电直供＋算效跃升＋余热利用', PAL['blue'], '-.', '^')]
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ax.axhspan(0, th, color=PAL['green'], alpha=0.08, lw=0, zorder=0)
    ax.axhline(th, color=PAL['red'], lw=1.1, ls=(0, (5, 3)), zorder=2)
    ax.annotate(f'绿色词元阈值 $\\iota^{{*}}$＝{th} gCO$_2$e／千 $\\tilde{{T}}$',
                (2035.5, th + 0.06), fontsize=8, color=PAL['red'], ha='right', va='bottom')
    cross = []
    for name, lab, c, ls, mk in scen:
        yr, v = ser(name)
        ax.plot(yr, v, color=c, lw=1.9, ls=ls, marker=mk, ms=4.0, label=lab, zorder=3)
        ax.annotate(f'{v[-1]:.2f}', (yr[-1], v[-1]), textcoords='offset points',
                    xytext=(7, 0), ha='left', va='center', fontsize=8.5, color=c)
        below = np.where(v < th)[0]
        if len(below):
            i = below[0]
            yc = yr[i - 1] + (v[i - 1] - th) / (v[i - 1] - v[i])
            ax.plot([yc], [th], marker='o', ms=5.5, mfc='white', mec=c, mew=1.4,
                    ls='none', zorder=4)
            cross.append(f'{lab[:4]}：{int(np.ceil(yc))} 年')
    ax.annotate('跨越阈值年份　' + '；'.join(cross) + '\n基准情景至 2035 年仍高于阈值',
                (0.03, 0.30), xycoords='axes fraction', ha='left', va='bottom',
                fontsize=7.8, color='#444444', bbox=WBOX_E)
    ax.set_xlabel('年份')
    ax.set_ylabel('碳强度 $\\iota$（gCO$_2$e／千 $\\tilde{T}$）')
    ax.set_xlim(2025.7, 2035.7)
    ax.set_xticks(np.arange(2026, 2036))
    ax.set_ylim(0, 2.9)
    ax.legend(loc='upper right', fontsize=7.8)
    save(fig, f'{FIG}/fig11_3.png')
    print('ok fig11_3')


# ============================ 第12章 ============================
def fig12_2():
    """图12.2 智能经济生产函数的估计系数（95% 置信区间＋显著性）。"""
    pf = R['growth']['prodfn']
    keys = ['lnK', 'lnL', 'lnD', 'lnT']
    labs = ['资本投入\n$\\ln K$', '劳动投入\n$\\ln L$', '数据投入\n$\\ln D$',
            '标准词元流量\n$\\ln \\tilde{T}$']
    elas = ['$\\alpha_K$', '$\\alpha_L$', '$\\alpha_D$', '$\\alpha_T$']
    coef = np.array([pf[k]['coef'] for k in keys])
    se = np.array([pf[k]['se'] for k in keys])
    ci = 1.96 * se
    cols = [PAL['ltblue'], PAL['teal'], PAL['gold'], PAL['orange']]
    ecs = [PAL['blue'], '#1F5F5F', '#8A6A00', '#8C3F0C']
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.bar(x, coef, 0.5, color=cols, edgecolor=ecs, lw=0.9, zorder=3)
    ax.errorbar(x, coef, yerr=ci, fmt='none', ecolor='#303030', elinewidth=1.1,
                capsize=4, capthick=1.1, zorder=4)
    for i in range(4):
        ax.annotate(f'{elas[i]}＝{coef[i]:.3f}{stars(pf[keys[i]]["p"])}',
                    (i, coef[i] + ci[i]), textcoords='offset points', xytext=(0, 4),
                    ha='center', fontsize=8.6)
        ax.annotate(f'SE＝{se[i]:.3f}', (i, 0.012), ha='center', va='bottom',
                    fontsize=7.2, color='white')
    ax.set_xticks(x)
    ax.set_xticklabels(labs, fontsize=8.2)
    ax.set_ylabel('产出弹性估计值')
    ax.set_ylim(0, 0.47)
    ax.set_xlim(-0.62, 3.62)
    ax.annotate(f'$R^2$＝{pf["R2"]:.2f}，N＝{pf["N"]}\n'
                f'误差线为 95% 置信区间；*** 表示 1% 水平显著',
                (0.975, 0.965), xycoords='axes fraction', ha='right', va='top',
                fontsize=7.8, color='#444444', bbox=WBOX_E)
    save(fig, f'{FIG}/fig12_2.png')
    print('ok fig12_2')


def fig12_3():
    """图12.3 增长贡献分解（堆叠条形）＋词元贡献占比（右轴，双轴两侧完整）。"""
    dec = R['growth']['decomp']
    yrs = sorted(dec.keys())
    comp = [('cK', '资本贡献', PAL['ltblue']), ('cL', '劳动贡献', PAL['teal']),
            ('cD', '数据贡献', PAL['gold']), ('cT', '标准词元流量贡献', PAL['orange']),
            ('tfp', '全要素生产率残差', '#B7B7B7')]
    x = np.arange(len(yrs))
    fig, ax1 = plt.subplots(figsize=(6.7, 4.0))
    bot = np.zeros(len(yrs))
    for k, lab, c in comp:
        _, v = ser(f'growth.{k}')
        ax1.bar(x, v, 0.52, bottom=bot, color=c, edgecolor='white', lw=0.7,
                label=lab, zorder=3)
        bot = bot + v
    for i, (xi, tot) in enumerate(zip(x, bot)):
        txt = f'$g_Y$＝{tot:.1f}' if i == 0 else f'{tot:.1f}'
        ax1.annotate(txt, (xi, tot), textcoords='offset points', xytext=(0, 3),
                     ha='center', fontsize=8, color='#333333')
    ax1.set_xticks(x)
    ax1.set_xticklabels(yrs)
    ax1.set_xlabel('年份')
    ax1.set_ylabel('对产出增长率的贡献（百分点）')
    ax1.set_ylim(0, 8.6)
    ax1.set_xlim(-0.62, len(yrs) - 0.38)
    ax2 = twin_right(ax1, PAL['red'])
    sh = np.array([dec[y]['share_T'] * 100 for y in yrs])
    ax2.plot(x, sh, color=PAL['red'], marker='D', ms=4.6, lw=1.9, zorder=5,
             mfc='white', mew=1.3)
    halo = [pe.withStroke(linewidth=2.6, foreground='white')]
    for i, (xi, v) in enumerate(zip(x, sh)):
        off = (11, 1) if i == len(sh) - 1 else (0, 9)
        ha = 'left' if i == len(sh) - 1 else 'center'
        ax2.annotate(f'{v:.1f}%', (xi, v), textcoords='offset points', xytext=off,
                     ha=ha, va='center', fontsize=7.6, color=PAL['red'],
                     path_effects=halo, zorder=6)
    ax2.set_ylabel('标准词元贡献占实际增长率的比重（%）', color=PAL['red'])
    ax2.set_ylim(0, 12.5)
    h1, l1 = ax1.get_legend_handles_labels()
    h1.append(Line2D([], [], color=PAL['red'], marker='D', ms=4.2, mfc='white',
                     label='词元贡献占比（右轴）'))
    l1.append('词元贡献占比（右轴）')
    ax1.legend(handles=h1, labels=l1, loc='upper left', fontsize=7.4, ncol=2,
               columnspacing=1.0, handlelength=1.4)
    save(fig, f'{FIG}/fig12_3.png')
    print('ok fig12_3')


def fig12_4():
    """图12.4 引入词元前后 TFP 残差对照（左）与分区域贡献率（右）。"""
    tb = R['growth']['tfp_bias']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.5),
                                   gridspec_kw={'width_ratios': [1, 1.05]})
    # （a）TFP 残差对照
    vals = [tb['without_token'], tb['with_token']]
    labs = ['传统核算\n（$K$、$L$）', '本书核算\n（$K$、$L$、$D$、$\\tilde{T}$）']
    cols = [PAL['gray'], PAL['blue']]
    x = np.arange(2)
    ax1.bar(x, vals, 0.46, color=[PAL['gray'], PAL['ltblue']],
            edgecolor=cols, lw=0.9, zorder=3)
    for xi, v in zip(x, vals):
        ax1.annotate(f'{v:.2f}%', (xi, v), textcoords='offset points', xytext=(0, 3.5),
                     ha='center', fontsize=9, color='#333333')
    ax1.axhline(vals[1], color=PAL['gray'], lw=0.8, ls=(0, (3, 2)), zorder=2)
    ax1.annotate('', xy=(1.42, vals[0]), xytext=(1.42, vals[1]),
                 arrowprops=dict(arrowstyle='<->', color=PAL['red'], lw=1.0))
    ax1.plot([1.0, 1.42], [vals[0], vals[0]], color='#999999', lw=0.7, ls=(0, (3, 2)))
    ax1.annotate(f'残差高估\n{tb["overstate"]:.2f} 个百分点', (1.50, (vals[0] + vals[1]) / 2),
                 ha='left', va='center', fontsize=8, color=PAL['red'])
    ax1.set_xticks(x)
    ax1.set_xticklabels(labs, fontsize=8)
    ax1.set_ylabel('年均全要素生产率增长率（%）')
    ax1.set_ylim(0, 3.1)
    ax1.set_xlim(-0.55, 2.25)
    panel_label(ax1, '（a）TFP 残差的口径对照', x=-0.20)
    # （b）分区域贡献率
    reg_cn = {'east': '东部', 'central': '中部', 'west': '西部'}
    reg_c = {'east': PAL['blue'], 'central': PAL['orange'], 'west': PAL['red']}
    ks, vs = ser('growth.region', numeric=False)
    vs = vs * 100
    xr = np.arange(len(ks))
    ax2.bar(xr, vs, 0.5, color=[reg_c[k] for k in ks], alpha=0.85,
            edgecolor=[reg_c[k] for k in ks], lw=0.9, zorder=3)
    for xi, v in zip(xr, vs):
        ax2.annotate(f'{v:.1f}%', (xi, v), textcoords='offset points', xytext=(0, 3.5),
                     ha='center', fontsize=9, color='#333333')
    ax2.set_xticks(xr)
    ax2.set_xticklabels([reg_cn[k] for k in ks], fontsize=9)
    ax2.set_xlabel('区域')
    ax2.set_ylabel('标准词元流量对增长的贡献率（%）')
    ax2.set_ylim(0, 10.2)
    ax2.set_xlim(-0.6, len(ks) - 0.4)
    panel_label(ax2, '（b）2026 年分区域词元贡献率', x=-0.20)
    fig.tight_layout(w_pad=2.4)
    save(fig, f'{FIG}/fig12_4.png')
    print('ok fig12_4')


# ============================ 第13章 ============================
def fig13_2():
    """图13.2 五城词元运营中心的能力画像（雷达图）。"""
    cities = R['cases']['cities']
    order = ['jx', 'sz', 'wz', 'gz', 'sh']
    dims = list(cities['jx']['scores'].keys())
    n = len(dims)
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    ang_c = np.concatenate([ang, ang[:1]])
    mks = ['o', 's', '^', 'D', 'v']
    fig = plt.figure(figsize=(5.6, 5.0))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    for i, k in enumerate(order):
        _, v = ser(f'cases.{k}', numeric=False)
        vv = np.concatenate([v, v[:1]])
        ax.plot(ang_c, vv, color=SERIES[i], lw=1.7, marker=mks[i], ms=4.2,
                label=f'{cities[k]["name"]}（{cities[k]["subject"]}）', zorder=3)
        ax.fill(ang_c, vv, color=SERIES[i], alpha=0.05, lw=0, zorder=2)
    ax.set_thetagrids(ang * 180 / np.pi, dims, fontsize=9)
    ax.tick_params(axis='x', pad=8)
    ax.set_ylim(0.58, 0.95)
    ax.set_yticks([0.6, 0.7, 0.8, 0.9])
    ax.set_yticklabels(['0.6', '0.7', '0.8', '0.9'], fontsize=7.2, color='#666666')
    ax.set_rlabel_position(198)
    for t in ax.get_yticklabels():
        t.set_bbox(dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.85))
    ax.grid(alpha=0.35, lw=0.6)
    ax.spines['polar'].set_color('#BBBBBB')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=7.8,
              handlelength=1.6, columnspacing=1.4, labelspacing=0.4)
    fig.subplots_adjust(top=0.94, bottom=0.16)
    save(fig, f'{FIG}/fig13_2.png')
    print('ok fig13_2')


ALL = [fig7_2, fig7_3, fig7_4, fig8_2, fig8_3, fig9_2, fig9_3, fig9_4,
       fig10_3, fig10_4, fig11_2, fig11_3, fig12_2, fig12_3, fig12_4, fig13_2]

if __name__ == '__main__':
    for f in ALL:
        f()
