# -*- coding: utf-8 -*-
"""论文二《计量摩擦、价格离散与智能服务市场发育》图件。

图内不写图题与资料来源（由 Word 排在图下方）；图例置于绘图区下方。
一切数值取自 data/results.json（图 2 的“仅补贴／从未处理”两条分组均值由
data/panel.csv 按不随时间变化的分组还原，并与 results.json 的 fig.never_A 对账）。

版面：按 14 cm 版心排版，画布宽 5.5 英寸 ≈ 14 cm，故图内字号即印刷字号，
最小字号 7.5 pt。
"""
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
DATA = os.path.join(HERE, 'data')
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
    'axes.unicode_minus': True,          # Noto Sans CJK 含 U+2212，负号用真减号
    'font.size': 9,
    'axes.labelsize': 9,
    'axes.titlesize': 8.5,
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
     'purple': '#5B3A87'}

MINUS = '−'

R = json.load(open(os.path.join(DATA, 'results.json'), encoding='utf-8'))


def save(fig, name):
    fig.savefig(os.path.join(FIG, name), facecolor='white')
    plt.close(fig)
    print('ok', name)


def grid_y(ax):
    ax.grid(axis='y', linestyle='-', color='#B0B0B0', alpha=0.22, linewidth=0.6)
    ax.set_axisbelow(True)


def fmt(v, nd=4):
    """带真减号的定点数字符串。"""
    s = f'{v:.{nd}f}'
    return s.replace('-', MINUS)


# =============================================================== 图 1 机制概念图
def fig1():
    sp = R['fig']['spread_pre']
    npl = R['sample']['n_plat']

    fig, ax = plt.subplots(figsize=(5.5, 4.75))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    def node(x0, x1, y0, y1, title, body=(), fc='#EAF0F7', ec=C['blue'],
             tfs=8.5, bfs=7.8, tw='bold', lw=0.9, ls='solid', tcol=None):
        ax.add_patch(FancyBboxPatch(
            (x0, y0), x1 - x0, y1 - y0,
            boxstyle='round,pad=0,rounding_size=1.2',
            facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls, zorder=2))
        cx = (x0 + x1) / 2.0
        body = list(body)
        th = 3.8 if title else 0.0
        tot = th + 3.15 * len(body)
        top = (y0 + y1) / 2.0 + tot / 2.0
        y = top - th / 2.0 if title else top
        if title:
            ax.text(cx, y, title, ha='center', va='center', fontsize=tfs,
                    fontweight=tw, color=tcol or ec, zorder=3)
            y -= th / 2.0
        for ln in body:
            y -= 3.15
            ax.text(cx, y + 1.55, ln, ha='center', va='center', fontsize=bfs,
                    color='#333333', zorder=3)

    def arrow(x0, y0, x1, y1, color=C['blue'], lw=1.1, style='-|>', ls='solid'):
        ax.add_patch(FancyArrowPatch(
            (x0, y0), (x1, y1), arrowstyle=style, mutation_scale=9,
            color=color, linewidth=lw, linestyle=ls, shrinkA=0, shrinkB=0,
            zorder=4))

    # ---- A 组：计量口径不可比（分组框）
    ax.add_patch(FancyBboxPatch(
        (1, 71.5), 56, 27.5, boxstyle='round,pad=0,rounding_size=1.2',
        facecolor='#F7F9FC', edgecolor='#9AA7B4', linewidth=0.8,
        linestyle=(0, (3, 2)), zorder=1))
    ax.text(29, 96.2, '词元不是同质的计量单位', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#22303C', zorder=3)
    node(3, 28.2, 80.5, 93.5, '分词口径不可比',
         ['同一任务的词元数', '跨模型相差数倍'])
    node(29.8, 55, 80.5, 93.5, '计费口径不统一',
         ['输入、输出与缓存', '分别计价'])
    ax.text(29, 77.0, f'事前同一任务、跨 {npl} 家可比供给方的真实价差：',
            ha='center', va='center', fontsize=7.5, color='#5A6672', zorder=3)
    ax.text(29, 73.8,
            f"中位数 {sp['p50']:.2f} 倍，P90 {sp['p90']:.2f} 倍，"
            f"{sp['share_ge_10x']*100:.1f}% 的单元不低于 10 倍",
            ha='center', va='center', fontsize=7.5, color='#5A6672', zorder=3)

    # ---- B：折算不可行
    arrow(29, 71.5, 29, 68.6)
    node(2, 56, 53.5, 68.5, '折算不可行：价格信息不可比',
         ['名义单价 p 与真实单价 p/η 之间隔着未知折算因子 η，',
          '买方无法把各供给方的报价折算到同一基准上',
          '计量摩擦强度 σ² ＝ Var(ln η)'], fc='#E3ECF5')

    # ---- 两条渠道
    arrow(15, 53.5, 15, 49.6)
    arrow(43, 53.5, 43, 49.6)
    node(2, 28.2, 33.5, 49.5, '比价渠道',
         ['搜寻的边际收益下降，', '比价过早停止，', '均衡名义价格离散不收敛'],
         fc='#FDF1E7', ec=C['orange'])
    node(29.8, 56, 33.5, 49.5, '逆向选择渠道',
         ['质量不可事前验证，', '买方按平均效值出价，', '高效值供给方退出'],
         fc='#FDF1E7', ec=C['orange'])

    # ---- 结果
    arrow(15, 33.5, 15, 29.6, color=C['orange'])
    arrow(43, 33.5, 43, 29.6, color=C['orange'])
    node(2, 28.2, 18.5, 29.5, '价格离散度上升',
         ['（命题 1）'], fc='#F6E9E9', ec=C['red'])
    node(29.8, 56, 18.5, 29.5, '平均成交效值下降',
         ['市场厚度收缩（命题 2）'], fc='#F6E9E9', ec=C['red'])
    arrow(15, 18.5, 22, 15.1, color=C['red'])
    arrow(43, 18.5, 36, 15.1, color=C['red'])
    node(9, 49, 3.0, 15.0, '中小企业采纳受抑',
         ['折算能力 κ 随企业规模递增，', '中小企业受抑更强（命题 3）'],
         fc='#F6E9E9', ec=C['red'])

    # ---- 右侧：统一计量平台的作用点
    ax.add_patch(FancyBboxPatch(
        (61, 14), 38, 58, boxstyle='round,pad=0,rounding_size=1.2',
        facecolor='#F1F7EC', edgecolor=C['green'], linewidth=1.0, zorder=1))
    ax.text(80, 68.6, '统一计量平台', ha='center', va='center', fontsize=9,
            fontweight='bold', color=C['green'], zorder=3)
    ax.text(80, 65.0, '（城市词元运营中心）', ha='center', va='center',
            fontsize=8, color=C['green'], zorder=3)
    node(63, 97, 54.5, 63.5, '① 统一计量', ['折算可行，σ² 下降'],
         fc='#FFFFFF', ec=C['green'], tfs=8.2, bfs=7.8)
    node(63, 97, 36.5, 45.5, '② 统一结算', ['报价可比，效值可核验'],
         fc='#FFFFFF', ec=C['green'], tfs=8.2, bfs=7.8)
    node(63, 97, 19.0, 28.0, '③ 统一调度', ['撮合成本下降，市场厚度回升'],
         fc='#FFFFFF', ec=C['green'], tfs=8.2, bfs=7.5)
    for yy in (59.0, 41.0, 23.5):
        arrow(61.0, yy, 56.4, yy, color=C['green'], lw=1.2, style='-[')

    handles = [
        Line2D([0], [0], color=C['blue'], lw=1.2, marker='>', markersize=4,
               label='计量摩擦的形成与传导路径'),
        Line2D([0], [0], color=C['green'], lw=1.2, marker='|', markersize=6,
               label='统一计量平台的作用点（抑制该环节）'),
    ]
    fig.legend(handles=handles, loc='lower center', ncol=2,
               bbox_to_anchor=(0.5, -0.035), handlelength=1.8, columnspacing=1.4)
    fig.tight_layout()
    save(fig, 'fig1.png')


# =========================================== 图 2 四组城市的价格离散度月度均值
def _group_series():
    """返回 (第一代, 第二代, 仅补贴, 从未处理) 四条离散度月度均值与城市数。

    第一代／第二代直接取 results.json；仅补贴／从未处理由 panel.csv 按
    不随时间变化的分组还原，并与 results.json 的 fig.never_A 对账。
    """
    F = R['fig']
    coh = R['sample']['cohorts']
    n1 = sum(coh['A1'].values())
    n2 = sum(coh['A2'].values())
    gs = R['sample']['group_size']
    out = {'gen1': (np.array(F['gen1']), n1), 'gen2': (np.array(F['gen2']), n2)}
    path = os.path.join(DATA, 'panel.csv')
    if not os.path.exists(path):
        print('warn: 缺少 panel.csv，仅补贴／从未处理合并为“未上线平台”一组')
        out['never'] = (np.array(F['never_A']), gs['onlyB'] + gs['none'])
        return out
    import pandas as pd
    d = pd.read_csv(path)
    onlyb = d[d['grp'] == 'onlyB'].groupby('ym')['disp'].mean().values
    none = d[d['grp'] == 'none'].groupby('ym')['disp'].mean().values
    w = (gs['onlyB'] * onlyb + gs['none'] * none) / (gs['onlyB'] + gs['none'])
    dev = float(np.max(np.abs(w - np.array(F['never_A']))))
    assert dev < 5e-5, f'panel.csv 与 results.json 的 never_A 对不上：{dev}'
    out['onlyB'] = (onlyb, gs['onlyB'])
    out['none'] = (none, gs['none'])
    return out


def fig2():
    F = R['fig']
    months = F['months']
    x = np.arange(len(months))
    g = _group_series()

    fig, ax = plt.subplots(figsize=(5.5, 3.05))
    series = [('gen1', '第一代平台城市（算力调度型，{n} 城）', C['blue'], '-'),
              ('gen2', '第二代平台城市（词元计量型，{n} 城）', C['red'], '-'),
              ('onlyB', '仅补贴城市（未上线平台，{n} 城）', C['teal'], '--'),
              ('none', '从未处理城市（{n} 城）', C['gray'], ':')]
    if 'never' in g:
        series = series[:2] + [('never', '未上线平台城市（{n} 城）', C['gray'], '--')]
    for key, lab, col, ls in series:
        if key not in g:
            continue
        ys, n = g[key]
        ax.plot(x, ys, color=col, linewidth=1.3, linestyle=ls,
                label=lab.format(n=n))

    coh = R['sample']['cohorts']
    m1 = sorted(coh['A1'])[0]
    m2 = sorted(coh['A2'])[0]
    for mm, lab, col in ((m1, '第一代首批上线', C['blue']),
                         (m2, '第二代首批上线', C['red'])):
        xi = months.index(mm)
        ax.axvline(xi, color=col, linestyle=(0, (4, 3)), linewidth=0.9, alpha=0.65)
        ax.annotate(f'{lab}\n{mm}', (xi, 1.0), xycoords=('data', 'axes fraction'),
                    xytext=(-3 if mm == m2 else 3, -2), textcoords='offset points',
                    ha='right' if mm == m2 else 'left', va='top',
                    fontsize=7.5, color=col, linespacing=1.25)

    ax.set_xticks(x[::6])
    ax.set_xticklabels([months[i] for i in range(0, len(months), 6)])
    ax.set_xlim(-0.8, len(months) - 0.2)
    ax.set_xlabel('年份—月份')
    ax.set_ylabel('价格离散度（变异系数，无量纲）')
    lo = min(np.min(v[0]) for v in g.values())
    hi = max(np.max(v[0]) for v in g.values())
    ax.set_ylim(lo - 0.012, hi + 0.048)
    grid_y(ax)
    fig.legend(loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.155),
               columnspacing=1.6, handlelength=2.2)
    fig.tight_layout()
    save(fig, 'fig2.png')


# =============================================================== 图 3 事件研究
def _ev(y, t, mult=1.0):
    e = R['event'][y][t]
    ks = sorted(int(k) for k in e['coefs'])
    b = np.array([e['coefs'][str(k)]['coef'] for k in ks]) * mult
    s = np.array([e['coefs'][str(k)]['se'] for k in ks]) * mult
    base = e['base']
    ks = ks + [base]
    b = np.append(b, 0.0)
    s = np.append(s, 0.0)
    o = np.argsort(ks)
    ks = np.array(ks)[o]
    return ks, b[o], s[o], e['window'], e['pretrend_joint']['p']


def fig3():
    panels = [('disp', '处理效应估计值（变异系数）', 1.0),
              ('adopt_sme', '处理效应估计值（百分点）', 100.0)]
    arms = [('A2', '处理 A：统一计量平台（第二代）', C['red'], 'o', -0.14),
            ('B', '处理 B：价格补贴', C['teal'], 's', 0.14)]

    fig, axes = plt.subplots(2, 1, figsize=(5.5, 5.1), sharex=True)
    for ax, (y, lab, mult) in zip(axes, panels):
        for t, _, col, mk, dx in arms:
            ks, b, s, win, _ = _ev(y, t, mult)
            edge = np.isin(ks, win)
            ax.errorbar(ks + dx, b, yerr=1.96 * s, fmt='none', ecolor=col,
                        elinewidth=0.9, capsize=2.0, zorder=2)
            ax.plot(ks + dx, b, color=col, linewidth=1.1, zorder=3)
            ax.plot(ks[~edge] + dx, b[~edge], linestyle='none', marker=mk,
                    markersize=3.8, color=col, zorder=4)
            ax.plot(ks[edge] + dx, b[edge], linestyle='none', marker=mk,
                    markersize=4.2, markerfacecolor='white',
                    markeredgecolor=col, markeredgewidth=0.9, zorder=4)
        ax.axhline(0, color=C['gray'], linewidth=0.8, zorder=1)
        ax.axvline(-0.5, color='#444444', linestyle='--', linewidth=0.9,
                   alpha=0.75, zorder=1)
        ax.set_ylabel(lab)
        ax.set_xlim(-6.8, 6.8)
        ax.set_xticks(range(-6, 7))
        grid_y(ax)
    axes[0].set_title('（a）价格离散度', loc='left', color='#22303C')
    axes[1].set_title('（b）中小企业采纳率', loc='left', color='#22303C')
    axes[1].set_xticklabels([f'{MINUS}6', f'{MINUS}5', f'{MINUS}4', f'{MINUS}3',
                             f'{MINUS}2', f'{MINUS}1', '0', '+1', '+2', '+3',
                             '+4', '+5', '+6'])
    axes[1].set_xlabel('相对处理时点的月份数')

    handles = [Line2D([0], [0], color=a[2], marker=a[3], markersize=3.8,
                      linewidth=1.1, label=a[1]) for a in arms]
    handles += [
        Line2D([0], [0], color='#444444', linestyle='--', linewidth=0.9,
               label=f'处理时点（基期为相对期 {MINUS}1）'),
        Line2D([0], [0], color=C['gray'], marker='o', markersize=4.2,
               markerfacecolor='white', linestyle='none',
               label='空心点为窗口两端的归并档'),
    ]
    fig.legend(handles=handles, loc='lower center', ncol=2,
               bbox_to_anchor=(0.5, -0.115), columnspacing=1.6, handlelength=2.0)
    fig.tight_layout()
    save(fig, 'fig3.png')


# =============================================================== 图 4 安慰剂检验
def fig4():
    items = [('disp_A', '（a）价格离散度 · 统一计量平台', 1.0),
             ('disp_B', '（b）价格离散度 · 价格补贴', 1.0),
             ('adopt_sme_A', '（c）中小企业采纳率 · 统一计量平台', 100.0),
             ('adopt_sme_B', '（d）中小企业采纳率 · 价格补贴', 100.0)]
    units = {1.0: '估计系数（变异系数）', 100.0: '估计系数（百分点）'}

    fig, axes = plt.subplots(2, 2, figsize=(5.5, 4.35))
    for ax, (key, ttl, mult) in zip(axes.ravel(), items):
        P = R['placebo'][key]
        dr = np.array(P['draws']) * mult
        true = P['true'] * mult
        q95 = P['q95_abs'] * mult
        cnt, _, _ = ax.hist(dr, bins=28, color=C['blue'], alpha=0.55,
                            edgecolor='white', linewidth=0.4, zorder=2)
        ax.axvline(-q95, color=C['gray'], linestyle=':', linewidth=1.0, zorder=3)
        ax.axvline(q95, color=C['gray'], linestyle=':', linewidth=1.0, zorder=3)
        ax.axvline(true, color=C['red'], linestyle='--', linewidth=1.4, zorder=4)
        lo = min(dr.min(), true)
        hi = max(dr.max(), true)
        pad = (hi - lo) * 0.16
        ax.set_xlim(lo - pad, hi + pad)
        ax.set_ylim(0, cnt.max() * 1.34)
        ax.set_title(ttl, loc='left', fontsize=8, color='#22303C')
        nd = 4 if mult == 1.0 else 2
        right = true < (lo + hi) / 2.0
        ax.annotate(f'真实系数 {fmt(true, nd)}\n经验 p ＝ {P["p_two_sided"]:.4f}',
                    (true, 0.97), xycoords=('data', 'axes fraction'),
                    xytext=(5 if right else -5, 0), textcoords='offset points',
                    ha='left' if right else 'right', va='top',
                    fontsize=7.5, color=C['red'], linespacing=1.3, zorder=6,
                    bbox=dict(facecolor='white', alpha=0.82, edgecolor='none',
                              boxstyle='square,pad=0.28'))
        grid_y(ax)
        ax.set_xlabel(units[mult])
    for ax in axes[:, 0]:
        ax.set_ylabel('频数（次）')
    for ax in axes.ravel():
        ax.tick_params(axis='both', labelsize=7.5)

    reps = R['placebo']['disp_A']['reps']
    handles = [
        Patch(facecolor=C['blue'], alpha=0.55, edgecolor='white',
              label=f'安慰剂系数分布（随机化处理时点 {reps} 次）'),
        Line2D([0], [0], color=C['red'], linestyle='--', linewidth=1.4,
               label='真实估计值'),
        Line2D([0], [0], color=C['gray'], linestyle=':', linewidth=1.0,
               label='安慰剂系数绝对值的 95% 分位'),
    ]
    fig.legend(handles=handles, loc='lower center', ncol=2,
               bbox_to_anchor=(0.5, -0.135), columnspacing=1.6, handlelength=2.0)
    fig.tight_layout()
    save(fig, 'fig4.png')


if __name__ == '__main__':
    fig1()
    fig2()
    fig3()
    fig4()
