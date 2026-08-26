# -*- coding: utf-8 -*-
"""论文图件。图内不写图题与资料来源（由 Word 排在图下方）；图例置于绘图区下方。

版面：按 14 cm 宽排版，画布宽 5.5 英寸 ≈ 14 cm，故图内字号即印刷字号。
"""
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)

for cand in ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
             '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc'):
    if os.path.exists(cand):
        font_manager.fontManager.addfont(cand)
        CJK = font_manager.FontProperties(fname=cand).get_name()
        break
else:
    CJK = 'DejaVu Sans'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': [CJK, 'DejaVu Sans'],
    'axes.unicode_minus': False,
    'font.size': 9,
    'axes.labelsize': 9,
    'axes.titlesize': 9,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
    'legend.fontsize': 8.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'grid.alpha': 0.22,
    'grid.linewidth': 0.6,
    'legend.frameon': False,
    'savefig.dpi': 400,
    'savefig.bbox': 'tight',
})

C = {'blue': '#1F4E79', 'orange': '#C55A11', 'teal': '#2E8B8B',
     'gray': '#7F7F7F', 'red': '#A02020', 'green': '#548235'}

R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))
A = R['anchor']


def save(fig, name):
    fig.savefig(os.path.join(FIG, name), facecolor='white')
    plt.close(fig)
    print('ok', name)


def grid_y(ax):
    ax.grid(axis='y', linestyle='-', color='#B0B0B0', alpha=0.22, linewidth=0.6)
    ax.set_axisbelow(True)


# ------------------------------------------------- 图1 改革的现实规模（真实数据）
def fig1():
    yrs = [2020, 2021, 2022, 2023, 2024]
    per = [A['settle_persons_wan'][str(y)] / 10000.0 for y in yrs]        # 亿人次
    saved = {2023: A['settle_saved_yi']['2023'], 2024: A['settle_saved_yi']['2024']}

    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    x = np.arange(len(yrs))
    ax.bar(x, per, width=0.5, color=C['blue'], alpha=0.88,
           edgecolor='white', linewidth=0.6, label='直接结算人次（亿人次）')
    for xi, v in zip(x, per):
        ax.annotate(f'{v:.2f}', (xi, v), textcoords='offset points', xytext=(0, 3),
                    ha='center', fontsize=8, color=C['blue'])
    ax.set_ylabel('直接结算人次（亿人次）')
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in yrs])
    ax.set_xlabel('年份')
    ax.set_ylim(0, max(per) * 1.28)
    grid_y(ax)

    ax2 = ax.twinx()
    ax2.spines['right'].set_visible(True)
    ax2.spines['top'].set_visible(False)
    xs = [x[yrs.index(y)] for y in saved]
    ys = [saved[y] for y in saved]
    ax2.plot(xs, ys, color=C['orange'], marker='o', markersize=5, linewidth=1.5,
             label='减少个人垫付（亿元）')
    for xi, v in zip(xs, ys):
        ax2.annotate(f'{v:,.0f}', (xi, v), textcoords='offset points', xytext=(6, -10),
                     fontsize=8, color=C['orange'])
    ax2.set_ylabel('减少个人垫付（亿元）', color=C['orange'])
    ax2.tick_params(axis='y', colors=C['orange'])
    ax2.set_ylim(0, max(ys) * 1.45)

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    fig.legend(h1 + h2, l1 + l2, loc='lower center', ncol=2,
               bbox_to_anchor=(0.5, -0.10))
    fig.tight_layout()
    save(fig, 'fig1.png')


# ------------------------------------------------- 图2 事件研究
def fig2():
    keys = [('outflow_share', '跨区就医人次占比（百分点）', 100.0),
            ('ln_gap', '外地—本地次均费用比（%）', 100.0)]
    fig, axes = plt.subplots(1, 2, figsize=(5.9, 2.9))
    for ax, (y, lab, mult) in zip(axes, keys):
        ev = R['event'][y]
        ks = sorted(int(k) for k in ev)
        co = np.array([ev[str(k)]['coef'] for k in ks]) * mult
        se = np.array([ev[str(k)]['se'] for k in ks]) * mult
        ks_p = list(ks)
        # 基期 −1 归零，显式画出
        ks_p.append(-1); co = np.append(co, 0.0); se = np.append(se, 0.0)
        o = np.argsort(ks_p)
        ks_p = np.array(ks_p)[o]; co = co[o]; se = se[o]
        ax.axhline(0, color=C['gray'], linewidth=0.8)
        ax.axvline(-0.5, color=C['red'], linestyle='--', linewidth=0.9, alpha=0.7)
        ax.errorbar(ks_p, co, yerr=1.96 * se, fmt='o-', color=C['blue'],
                    markersize=3.6, linewidth=1.2, capsize=2.2, elinewidth=0.9)
        ax.set_xlabel('相对改革的年数')
        ax.set_ylabel(lab)
        ax.set_xticks(ks_p)
        grid_y(ax)
    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], color=C['blue'], marker='o', markersize=3.6,
                      linewidth=1.2, label='点估计及 95% 置信区间'),
               Line2D([0], [0], color=C['red'], linestyle='--', linewidth=0.9,
                      label='改革实施时点（基期为改革前一年）')]
    fig.legend(handles=handles, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.11))
    fig.tight_layout()
    save(fig, 'fig2.png')


# ------------------------------------------------- 图3 估计量对照与安慰剂
def fig3():
    fig, axes = plt.subplots(1, 2, figsize=(5.9, 2.9))

    ax = axes[0]
    ys = [('outflow_share', '跨区就医占比'), ('ln_cost_inp', '本地次均费用'),
          ('ln_gap', '费用缺口'), ('local_adm_rate', '本地住院率')]
    ests = [('TWFE', lambda y: (R['baseline'][y]['full']['coef']['post'],
                                R['baseline'][y]['full']['se']['post'])),
            ('CS', lambda y: (R['cs'][y]['overall']['coef'], R['cs'][y]['overall']['se'])),
            ('城市趋势', lambda y: (R['citytrend'][y]['coef'], R['citytrend'][y]['se']))]
    cols = [C['blue'], C['orange'], C['teal']]
    off = np.linspace(-0.22, 0.22, len(ests))
    for (nm, f), dx, cc in zip(ests, off, cols):
        xs, es = [], []
        for i, (y, _) in enumerate(ys):
            b, s = f(y)
            xs.append(b * 100); es.append(s * 100)
        ax.errorbar(np.arange(len(ys)) + dx, xs, yerr=1.96 * np.array(es), fmt='o',
                    color=cc, markersize=4, capsize=2.2, elinewidth=0.9, label=nm)
    ax.axhline(0, color=C['gray'], linewidth=0.8)
    ax.set_xticks(np.arange(len(ys)))
    ax.set_xticklabels([l for _, l in ys], rotation=18, ha='right')
    ax.set_ylabel('处理效应（百分点／%）')
    grid_y(ax)
    h3, l3 = ax.get_legend_handles_labels()

    ax = axes[1]
    pl = R['placebo']['ln_gap']
    xs = np.linspace(-4 * pl['sd'], 4 * pl['sd'], 400)
    dens = np.exp(-0.5 * (xs / pl['sd']) ** 2) / (pl['sd'] * np.sqrt(2 * np.pi))
    ax.plot(xs * 100, dens / 100, color=C['blue'], linewidth=1.3)
    ax.fill_between(xs * 100, dens / 100, color=C['blue'], alpha=0.16)
    ax.axvline(pl['true'] * 100, color=C['red'], linewidth=1.4, linestyle='--')
    ax.annotate(f"实际估计\n{pl['true']*100:.2f}", (pl['true'] * 100, ax.get_ylim()[1] * 0.55),
                fontsize=8, color=C['red'], ha='right',
                xytext=(-6, 0), textcoords='offset points')
    ax.set_xlabel('随机化处理年份的估计系数（%）')
    ax.set_ylabel('核密度')
    grid_y(ax)
    from matplotlib.lines import Line2D
    h3 = h3 + [Line2D([0], [0], color=C['red'], linestyle='--', linewidth=1.4)]
    l3 = l3 + ['实际估计值']
    fig.legend(h3, l3, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.13))
    fig.tight_layout()
    save(fig, 'fig3.png')


# ------------------------------------------------- 图4 异质性与政策模拟
def fig4():
    fig, axes = plt.subplots(1, 2, figsize=(5.9, 2.9))

    ax = axes[0]
    H = R['hetero']
    items = [('liquidity', '居民医保占比', '跨区就医'),
             ('competition', '医院集中度', '本地费用'),
             ('externality', '净流入城市', '费用缺口')]
    x = np.arange(len(items))
    hi = [H[k]['high']['coef'] * 100 for k, _, _ in items]
    lo = [H[k]['low']['coef'] * 100 for k, _, _ in items]
    hse = [H[k]['high']['se'] * 100 for k, _, _ in items]
    lse = [H[k]['low']['se'] * 100 for k, _, _ in items]
    ax.bar(x - 0.19, hi, 0.36, yerr=1.96 * np.array(hse), color=C['blue'], alpha=0.88,
           capsize=2.2, error_kw=dict(elinewidth=0.8), label='高于中位数组')
    ax.bar(x + 0.19, lo, 0.36, yerr=1.96 * np.array(lse), color=C['orange'], alpha=0.88,
           capsize=2.2, error_kw=dict(elinewidth=0.8), label='低于中位数组')
    ax.axhline(0, color=C['gray'], linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([f'{a}\n（{b}）' for _, a, b in items], fontsize=8.2)
    ax.set_xlim(-0.55, len(items) - 0.45)
    ax.set_ylabel('处理效应（百分点／%）')
    grid_y(ax)
    h4, l4 = ax.get_legend_handles_labels()

    ax = axes[1]
    P = R['policy_sim']
    rhos = [0.5, 0.75, 1.0]
    vals = [P[f'unify_{int(r*100)}']['fund_saved_yi'] for r in rhos]
    ax.bar([f'{int(r*100)}%' for r in rhos], vals, width=0.5, color=C['green'],
           alpha=0.88, edgecolor='white', linewidth=0.6)
    for i, v in enumerate(vals):
        ax.annotate(f'{v:.1f}', (i, v), textcoords='offset points', xytext=(0, 3),
                    ha='center', fontsize=8.5, color=C['green'])
    ax.set_xlabel('监管统一后费用缺口被压缩的比例 ρ')
    ax.set_ylabel('基金可节约规模（亿元／年）')
    ax.set_ylim(0, max(vals) * 1.22)
    grid_y(ax)
    fig.legend(h4, l4, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout()
    save(fig, 'fig4.png')


if __name__ == '__main__':
    fig1(); fig2(); fig3(); fig4()
