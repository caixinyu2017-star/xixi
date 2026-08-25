# -*- coding: utf-8 -*-
"""论文一（《词元价格下行与智能服务支出的背离》）图件。

图内不写图题与资料来源（由 Word 排在图下方）；图例一律置于绘图区下方。
一切数值取自 data/results.json（主要是 figdata 节），不得硬编码。

版面：按 14 cm 版心排版，画布宽 5.5 英寸 ≈ 13.97 cm，故图内字号即印刷字号，
最小字号 7.5 pt。负号一律用减号 U+2212。
"""
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

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
    'axes.unicode_minus': True,          # 刻度负号用 U+2212
    'font.size': 9,
    'axes.labelsize': 9,
    'axes.titlesize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
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
     'gray': '#7F7F7F', 'red': '#A02020', 'green': '#548235',
     'plum': '#7B4173', 'lgray': '#BFBFBF'}

MINUS = '−'

R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))
FD = R['figdata']


def num(x, nd=3, signed=False):
    """数值转字符串：负号用 U+2212；signed=True 时正数带正号。"""
    s = f'{abs(x):.{nd}f}'
    if x < 0:
        return MINUS + s
    return ('+' + s) if signed else s


def pct(x, nd=1, signed=False):
    return num(x, nd, signed) + '%'


def save(fig, name):
    fig.savefig(os.path.join(FIG, name), facecolor='white')
    plt.close(fig)
    print('ok', name)


def grid_y(ax):
    ax.grid(axis='y', linestyle='-', color='#B0B0B0', alpha=0.22, linewidth=0.6)
    ax.set_axisbelow(True)


# ---------------------------------------------- 图1 名义价格指数与质量调整价格指数
def fig1():
    d = FD['fig1']
    months = d['months']
    npi = np.array(d['NPI'], dtype=float)
    stpi = np.array(d['STPI'], dtype=float)
    x = np.arange(len(months))
    brk = months.index(d['break_month'])          # 2026-07，结构转向首月
    i06 = months.index('2026-06')
    iend = len(months) - 1

    fig, ax = plt.subplots(figsize=(5.5, 3.3))

    ax.axvspan(brk - 0.5, iend + 0.4, color=C['red'], alpha=0.055, linewidth=0)
    ax.axvline(brk - 0.5, color=C['red'], linestyle='--', linewidth=0.9, alpha=0.85)

    ax.plot(x, npi, color=C['blue'], linewidth=1.6, marker='o', markersize=2.6,
            markevery=3, label='名义价格指数 NPI（单位价值口径）')
    ax.plot(x, stpi, color=C['orange'], linewidth=1.6, marker='s', markersize=2.6,
            markevery=3, label='质量调整价格指数 STPI（标准词元）')

    ax.set_yscale('log')
    ax.set_ylim(1.0, 155)
    ticks = [1, 2, 5, 10, 20, 50, 100]
    ax.set_yticks(ticks)
    ax.set_yticklabels([str(t) for t in ticks])
    ax.set_yticks([], minor=True)
    ax.set_ylabel('价格指数（2023 年 1 月 ＝ 100，对数刻度）')
    ax.set_xlabel('月份')

    step = 3
    ax.set_xticks(x[::step])
    ax.set_xticklabels([months[i] for i in x[::step]], rotation=45, ha='right')
    ax.set_xlim(-0.8, iend + 0.8)
    ax.grid(axis='y', linestyle='-', color='#B0B0B0', alpha=0.22, linewidth=0.6)
    ax.set_axisbelow(True)

    # 期末（2026-06）水平标注
    ax.annotate(f'{npi[i06]:.2f}', (i06, npi[i06]), textcoords='offset points',
                xytext=(-2, 7), ha='right', fontsize=7.5, color=C['blue'])
    ax.annotate(f'{stpi[i06]:.2f}', (i06, stpi[i06]), textcoords='offset points',
                xytext=(-3, 6), ha='right', va='bottom', fontsize=7.5,
                color=C['orange'])

    # 结构转向标注
    bk = R['index']['break_2026']
    ax.annotate('2026 年结构转向：\nNPI ' + pct(bk['NPI_change_pct'], 1, True)
                + '、STPI ' + pct(bk['STPI_change_pct'], 1, True),
                xy=(brk - 0.5, 34), xytext=(brk - 4.2, 34),
                fontsize=7.5, color=C['red'], ha='right', va='center',
                arrowprops=dict(arrowstyle='->', color=C['red'], linewidth=0.8,
                                shrinkA=3, shrinkB=1))

    # 累计降幅标注（2023-01→2026-06）
    rt = R['index']['rates']
    ax.text(1.0, 2.05,
            'NPI 累计 ' + pct(rt['NPI']['total_pct']) + '（年均 '
            + f"{rt['NPI']['annual_fold']:.3f}" + ' 倍）\nSTPI 累计 '
            + pct(rt['STPI']['total_pct']) + '（年均 '
            + f"{rt['STPI']['annual_fold']:.3f}" + ' 倍）',
            fontsize=7.5, color='#333333', ha='left', va='center')

    h, l = ax.get_legend_handles_labels()
    h.append(Line2D([0], [0], color=C['red'], linestyle='--', linewidth=0.9))
    l.append('结构转向起点（2026 年 7 月）')
    fig.legend(h, l, loc='lower center', ncol=2, bbox_to_anchor=(0.52, -0.19),
               handlelength=2.2, labelspacing=0.4, columnspacing=1.6)
    fig.tight_layout()
    save(fig, 'fig1.png')


# ---------------------------------------------- 图2 名义降价的三重分解（瀑布图）
def fig2():
    d = FD['fig2']
    items = [('真实价格效应\n（STPI）', d['real_price_ln'], d['share']['real_price']),
             ('质量效应', d['quality_ln'], d['share']['quality']),
             ('结构效应\n（档位替代）', d['structure_ln'], d['share']['structure']),
             ('残差', d['residual_ln'], d['share']['residual'])]
    total = d['total_ln']

    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    x = np.arange(len(items) + 1)
    w = 0.56
    cum = 0.0
    tops = []
    for i, (_, v, sh) in enumerate(items):
        color = C['blue'] if v < 0 else C['orange']
        ax.bar(i, v, bottom=cum, width=w, color=color, alpha=0.88,
               edgecolor=color, linewidth=0.7)
        lo, hi = min(cum, cum + v), max(cum, cum + v)
        txt = num(v) + '\n' + pct(sh * 100)
        if v < 0:
            ax.annotate(txt, (i, lo), textcoords='offset points', xytext=(0, -6),
                        ha='center', va='top', fontsize=7.5, color=color)
        else:
            ax.annotate(txt, (i, hi), textcoords='offset points', xytext=(0, 5),
                        ha='center', va='bottom', fontsize=7.5, color=color)
        cum += v
        tops.append(cum)
    # 合计
    ax.bar(len(items), total, width=w, color=C['gray'], alpha=0.9,
           edgecolor='white', linewidth=0.6)
    ax.annotate(num(total) + '\n' + pct(100.0), (len(items), total),
                textcoords='offset points', xytext=(0, -6), ha='center', va='top',
                fontsize=7.5, color='#3F3F3F')

    # 连接线
    for i in range(len(items)):
        ax.plot([i - w / 2, i + w / 2 + (1 - w)], [tops[i], tops[i]],
                color=C['lgray'], linewidth=0.8, linestyle='-', zorder=1)

    ax.axhline(0, color='#595959', linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([lab for lab, _, _ in items] + ['名义价格总变化\n（NPI_geo）'],
                       fontsize=8)
    ax.set_ylabel('对数变化 Δln（2023 年 1 月→2026 年 6 月）')
    ax.set_ylim(-5.35, 0.85)
    ax.set_xlim(-0.65, len(items) + 0.65)
    grid_y(ax)

    handles = [Patch(facecolor=C['blue'], alpha=0.88, label='压低名义价格（构成降幅）'),
               Patch(facecolor=C['orange'], alpha=0.88, label='抬高名义价格（抵消降幅）'),
               Patch(facecolor=C['gray'], alpha=0.9, label='名义价格总变化（＝100%）')]
    fig.legend(handles=handles, loc='lower center', ncol=2,
               bbox_to_anchor=(0.52, -0.13), labelspacing=0.35)
    fig.tight_layout()
    save(fig, 'fig2.png')


# ---------------------------------------------- 图3 需求价格弹性系数图
def fig3():
    src = {r['spec']: r for r in FD['fig3']}
    base = [('双向固定效应\n（质量调整价）', '双向固定效应（质量调整价）', C['blue'], 'o'),
            ('双向固定效应\n（名义价）', '双向固定效应（名义价）', C['orange'], 's'),
            ('工具变量 2SLS\n（质量调整价）', '工具变量 2SLS（质量调整价）', C['teal'], 'D')]
    het = [('分组异质性\n行业智能化基础', '智能化基础高组', '智能化基础低组',
            R['hetero']['ai_base']['diff']),
           ('分组异质性\n企业规模结构', '大型企业占比高组', '大型企业占比低组',
            R['hetero']['firm_size']['diff'])]

    rows = len(base) + len(het)
    ypos = np.arange(rows)[::-1]          # 自上而下

    fig, ax = plt.subplots(figsize=(5.5, 3.5))

    for k, (lab, key, col, mk) in enumerate(base):
        r = src[key]
        y = ypos[k]
        ax.errorbar(r['coef'], y, xerr=1.96 * r['se'], fmt=mk, color=col,
                    markersize=4.6, capsize=2.4, elinewidth=1.0, zorder=3)
        ax.annotate(num(r['coef']), (r['coef'], y), textcoords='offset points',
                    xytext=(0, 7), ha='center', fontsize=7.5, color=col)

    dy = 0.19
    for j, (lab, khi, klo, diff) in enumerate(het):
        y = ypos[len(base) + j]
        hi, lo = src[khi], src[klo]
        ax.errorbar(hi['coef'], y + dy, xerr=1.96 * hi['se'], fmt='^',
                    color=C['plum'], markersize=4.6, capsize=2.4, elinewidth=1.0,
                    zorder=3)
        ax.errorbar(lo['coef'], y - dy, xerr=1.96 * lo['se'], fmt='v',
                    color=C['plum'], markersize=4.6, capsize=2.4, elinewidth=1.0,
                    markerfacecolor='white', zorder=3)
        ax.annotate(num(hi['coef']), (hi['coef'], y + dy), textcoords='offset points',
                    xytext=(0, 6), ha='center', fontsize=7.5, color=C['plum'])
        ax.annotate(num(lo['coef']), (lo['coef'], y - dy), textcoords='offset points',
                    xytext=(0, -13), ha='center', fontsize=7.5, color=C['plum'])
        ax.annotate('组间差异 p ＝ ' + f"{diff['p']:.3f}", (-2.575, y),
                    ha='left', va='center', fontsize=7.5, color='#595959')

    ax.axvline(-1.0, color=C['red'], linestyle='--', linewidth=1.0, zorder=2)
    ax.axhline(ypos[len(base)] + 0.5, color=C['lgray'], linewidth=0.7,
               linestyle=':', zorder=1)

    ax.set_yticks(ypos)
    ax.set_yticklabels([b[0] for b in base] + [h[0] for h in het], fontsize=8)
    ax.set_ylim(-0.62, rows - 0.38)
    ax.set_xlim(-2.62, -0.66)
    ax.set_xticks(np.arange(-2.5, -0.6, 0.25))
    ax.set_xlabel('需求价格弹性 ε（点估计与 95% 置信区间）')
    ax.grid(axis='x', linestyle='-', color='#B0B0B0', alpha=0.22, linewidth=0.6)
    ax.set_axisbelow(True)

    handles = [Line2D([0], [0], color=C['blue'], marker='o', markersize=4.6,
                      linewidth=1.0, label='质量调整口径（基准）'),
               Line2D([0], [0], color=C['orange'], marker='s', markersize=4.6,
                      linewidth=1.0, label='名义口径（对照）'),
               Line2D([0], [0], color=C['teal'], marker='D', markersize=4.6,
                      linewidth=1.0, label='工具变量 2SLS'),
               Line2D([0], [0], color=C['plum'], marker='^', markersize=4.6,
                      linewidth=1.0, label='分组：高组'),
               Line2D([0], [0], color=C['plum'], marker='v', markersize=4.6,
                      linewidth=1.0, markerfacecolor='white', label='分组：低组'),
               Line2D([0], [0], color=C['red'], linestyle='--', linewidth=1.0,
                      label='ε ＝ ' + MINUS + '1 参考线')]
    fig.legend(handles=handles, loc='lower center', ncol=3,
               bbox_to_anchor=(0.52, -0.17), labelspacing=0.35, columnspacing=1.4)
    fig.tight_layout()
    save(fig, 'fig3.png')


# ---------------------------------------------- 图4 支出变化的回弹分解（瀑布图）
def fig4():
    d4 = FD['fig4']
    b = R['rebound']['full']
    v = R['rebound']['full_iv']
    total = b['total_lnE']
    keys = [('price_effect', '价格效应\n（质量调整价）'),
            ('pure_rebound', '纯回弹效应\n（ε×价格效应）'),
            ('task_complexity', '任务复杂化效应\n（γ×Δz）'),
            ('diffusion_other', '共同扩散与\n其他数量效应')]
    assert all(abs(d4[k] - b['decomp4'][k]) < 1e-9 for k, _ in keys)

    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    n = len(keys)
    w = 0.34
    gap = 0.02

    def walk(vals):
        cum, seg = 0.0, []
        for x in vals:
            seg.append((cum, x))
            cum += x
        return seg, cum

    segb, endb = walk([b['decomp4'][k] for k, _ in keys])
    segv, endv = walk([v['decomp4'][k] for k, _ in keys])

    for i in range(n):
        for seg, dx, col, alpha, hatch in (
                (segb, -(w / 2 + gap / 2), None, 0.88, None),
                (segv, +(w / 2 + gap / 2), None, 0.42, '///')):
            bottom, val = seg[i]
            cc = C['blue'] if val < 0 else C['orange']
            ax.bar(i + dx, val, bottom=bottom, width=w, color=cc, alpha=alpha,
                   edgecolor='white', linewidth=0.6, hatch=hatch, zorder=3)
    # 合计（两口径相同）
    ax.bar(n, total, width=w * 2 + gap, color=C['gray'], alpha=0.9,
           edgecolor='white', linewidth=0.6, zorder=3)

    # 数值标注：基准在左条、2SLS 在右条；两口径相同的项目只标一次
    for i, (k, _) in enumerate(keys):
        same = abs(segb[i][1] - segv[i][1]) < 1e-9
        marks = [(segb, 0.0, '#1F1F1F')] if same else \
                [(segb, -(w / 2 + gap / 2), '#1F1F1F'),
                 (segv, +(w / 2 + gap / 2), '#7F7F7F')]
        for seg, dx, col in marks:
            bottom, val = seg[i]
            hi, lo = max(bottom, bottom + val), min(bottom, bottom + val)
            if val < 0:
                ax.annotate(num(val, 2, True), (i + dx, lo),
                            textcoords='offset points', xytext=(0, -6),
                            ha='center', va='top', fontsize=7.5, color=col)
            else:
                ax.annotate(num(val, 2, True), (i + dx, hi),
                            textcoords='offset points', xytext=(0, 5),
                            ha='center', va='bottom', fontsize=7.5, color=col)
    ax.annotate(num(total, 2), (n, total), textcoords='offset points',
                xytext=(0, 5), ha='center', va='bottom', fontsize=7.5,
                color='#3F3F3F')

    # 价格通道净效应（基准口径）：价格效应 ＋ 纯回弹效应
    net = b['net_price_channel']
    ax.plot([-0.42, 1.42], [3.62, 3.62], color=C['green'], linewidth=0.9)
    for xx in (-0.42, 1.42):
        ax.plot([xx, xx], [3.39, 3.62], color=C['green'], linewidth=0.9)
    ax.annotate('价格通道净效应\n' + num(net, 3, True) + '（支出 '
                + pct(b['net_price_channel_pct'], 2, True) + '）',
                xy=(0.5, 3.89), ha='center', va='bottom', fontsize=7.5,
                color=C['green'], linespacing=1.35)

    ax.axhline(0, color='#595959', linewidth=0.8)
    ax.set_xticks(np.arange(n + 1))
    ax.set_xticklabels([lab for _, lab in keys] + ['支出总变化\n（合计）'], fontsize=7.5)
    ax.set_xlim(-0.7, n + 0.7)
    ax.set_ylim(-5.0, 8.9)
    ax.set_ylabel('对数变化 Δln（2023Q1→2026Q2）')
    grid_y(ax)

    ax2 = ax.twinx()
    ax2.spines['right'].set_visible(True)
    ax2.spines['top'].set_visible(False)
    ax2.set_ylim(ax.get_ylim()[0] / total * 100, ax.get_ylim()[1] / total * 100)
    ax2.set_yticks(np.arange(-50, 126, 25))
    ax2.set_ylabel('占支出总变化的比重（%）')

    eb = b['eps_used']
    ev = v['eps_used']
    handles = [Patch(facecolor=C['orange'], alpha=0.88,
                     label='基准口径（ε ＝ ' + num(eb) + '）：推高支出'),
               Patch(facecolor=C['blue'], alpha=0.88, label='基准口径：压低支出'),
               Patch(facecolor='#BFBFBF', alpha=0.7, hatch='///',
                     label='2SLS 弹性口径（ε ＝ ' + num(ev) + '）'),
               Patch(facecolor=C['gray'], alpha=0.9, label='支出总变化（两口径相同）')]
    fig.legend(handles=handles, loc='lower center', ncol=2,
               bbox_to_anchor=(0.52, -0.17), labelspacing=0.35, columnspacing=1.4)
    fig.tight_layout()
    save(fig, 'fig4.png')


if __name__ == '__main__':
    fig1()
    fig2()
    fig3()
    fig4()
