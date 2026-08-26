# -*- coding: utf-8 -*-
"""后半部 A 型分析图（15 幅，matplotlib，nature 风格，中文）。
数据一律读取 data/series.csv 与 data/results.json；不得手写模型数字。
输出 figs/figN_M.png（400 dpi）。图内不含图名、图注与资料来源。
"""
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
from matplotlib import font_manager as _fm
from figstyle import save, PAL, SERIES, CJK

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)

DF = pd.read_csv(os.path.join(HERE, 'data', 'series.csv'), dtype={'x': str})
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))

# ---- 局部样式辅助 ----
_BOLD_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
_fm.fontManager.addfont(_BOLD_PATH)
BOLD_FP = _fm.FontProperties(fname=_BOLD_PATH, size=10.5)
BOLD_S = _fm.FontProperties(fname=_BOLD_PATH, size=8.5)

WBOX = dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85)

ABI_CN = {'base': '基础素养', 'tech': '技术能力', 'eng': '工程实践',
          'innov': '创新应用', 'ethic': '伦理治理'}
JOB_CN = {'algo': '算法', 'meng': '模型工程', 'data': '数据',
          'prod': '产品应用', 'gov': '治理安全'}
TYPE3 = ['部属高校', '地方本科', '高职高专']
TYPE_C = {'部属高校': PAL['blue'], '地方本科': PAL['teal'], '高职高专': PAL['orange']}


def panel_label(ax, s, x=-0.12, y=1.02):
    ax.text(x, y, s, transform=ax.transAxes, fontproperties=BOLD_FP,
            ha='left', va='bottom')


def ser(name, numeric=True):
    """按 series 名取 (x, value)；numeric=True 时 x 转 float 并排序。"""
    d = DF[DF.series == name]
    if numeric:
        x = d.x.astype(float).values
        v = d.value.astype(float).values
        idx = np.argsort(x)
        return x[idx], v[idx]
    return d.x.values, d.value.astype(float).values


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


def kde(v, xs):
    """一维高斯核密度（Silverman 带宽），避免额外依赖。"""
    v = np.asarray(v, float)
    n = len(v)
    sd = v.std(ddof=1)
    iqr = np.subtract(*np.percentile(v, [75, 25]))
    h = 0.9 * min(sd, iqr / 1.34) * n ** (-0.2)
    z = (xs[:, None] - v[None, :]) / h
    return np.exp(-0.5 * z ** 2).sum(axis=1) / (n * h * np.sqrt(2 * np.pi))


# ============================ 第7章 ============================
def fig7_2():
    """图7.2 教育生产函数 OLS 系数条形＋95%CI＋显著性星号。"""
    ols = R['prodfn']['ols']
    keys = ['lnK', 'lnL', 'lnF']
    labs = ['物质资本投入\n$\\ln K$', '师资人力投入\n$\\ln L$', '产教融合投入\n$\\ln F$']
    coef = np.array([ols[k]['coef'] for k in keys])
    se = np.array([ols[k]['se'] for k in keys])
    ci = 1.96 * se
    sig = [stars(ols[k]['p']) for k in keys]
    cols = [PAL['blue'], PAL['teal'], PAL['orange']]
    fig, ax = plt.subplots(figsize=(5.0, 3.5))
    x = np.arange(3)
    ax.bar(x, coef, width=0.52, color=cols, alpha=0.88,
           edgecolor=[PAL['blue'], PAL['teal'], PAL['orange']], lw=1.0)
    ax.errorbar(x, coef, yerr=ci, fmt='none', ecolor='#303030', elinewidth=1.2,
                capsize=4, capthick=1.2)
    for i, (c, w, s) in enumerate(zip(coef, ci, sig)):
        ax.annotate(f'{c:.3f}{s}', (i, c + w), textcoords='offset points',
                    xytext=(0, 4), ha='center', fontsize=9)
        ax.annotate(f'SE={se[i]:.3f}', (i, 0.012), ha='center', va='bottom',
                    fontsize=7.5, color='white')
    ax.set_xticks(x)
    ax.set_xticklabels(labs, fontsize=8.5)
    ax.set_ylabel('产出弹性系数')
    ax.set_ylim(0, 0.62)
    ax.annotate(f"$R^2$={ols['R2']:.2f}，N={ols['N']}",
                (0.03, 0.96), xycoords='axes fraction', va='top', ha='left',
                fontsize=8.5, bbox=WBOX)
    save(fig, f'{FIG}/fig7_2.png')


def fig7_3():
    """图7.3 院校培养效率 TE：核密度（a）＋小提琴与类型均值（b）。"""
    samples = {t: ser(f'te_sample.{t}')[1] for t in TYPE3}
    byt = R['prodfn']['sfa']['te']['by_type']
    mean_all = R['prodfn']['sfa']['te']['mean']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.4),
                                   gridspec_kw={'width_ratios': [1.3, 1]})
    xs = np.linspace(0.38, 1.02, 400)
    for t in TYPE3:
        d = kde(samples[t], xs)
        ax1.plot(xs, d, color=TYPE_C[t], lw=1.9,
                 label=f'{t}（均值 {byt[t]:.2f}）')
        ax1.fill_between(xs, d, color=TYPE_C[t], alpha=0.10, lw=0)
    ax1.axvline(mean_all, color=PAL['gray'], ls='--', lw=1.2)
    ax1.annotate(f'全样本均值 TE={mean_all:.2f}', (mean_all + 0.012, 6.28),
                 fontsize=7.5, color=PAL['gray'], ha='left', va='top')
    ax1.set_xlabel('技术效率 TE')
    ax1.set_ylabel('核密度')
    ax1.set_xlim(0.38, 1.02)
    ax1.set_ylim(0, 6.5)
    ax1.legend(loc='upper left', fontsize=7.5)
    panel_label(ax1, '（a）', x=-0.13)
    # （b）小提琴＋类型均值标记
    pos = np.arange(1, 4)
    vp = ax2.violinplot([samples[t] for t in TYPE3], positions=pos,
                        widths=0.72, showextrema=False)
    for body, t in zip(vp['bodies'], TYPE3):
        body.set_facecolor(TYPE_C[t])
        body.set_alpha(0.28)
        body.set_edgecolor(TYPE_C[t])
        body.set_linewidth(1.1)
    for p, t in zip(pos, TYPE3):
        q1, q3 = np.percentile(samples[t], [25, 75])
        ax2.vlines(p, q1, q3, color=TYPE_C[t], lw=4, alpha=0.9)
        ax2.plot(p, byt[t], 'D', color=PAL['red'], ms=5, zorder=6)
        ax2.annotate(f'{byt[t]:.2f}', (p + 0.16, byt[t]), va='center',
                     ha='left', fontsize=8, color=PAL['red'])
    ax2.axhline(mean_all, color=PAL['gray'], ls='--', lw=1.1)
    ax2.annotate(f'{mean_all:.2f}', (3.62, mean_all), va='bottom', ha='right',
                 fontsize=7.5, color=PAL['gray'])
    ax2.set_xticks(pos)
    ax2.set_xticklabels(TYPE3, fontsize=8.5)
    ax2.set_xlim(0.45, 3.7)
    ax2.set_ylabel('技术效率 TE')
    ax2.set_ylim(0.38, 1.0)
    ax2.legend(handles=[
        Line2D([], [], marker='D', color='none', mfc=PAL['red'], ms=5,
               label='SFA 类型均值'),
        Line2D([], [], color=TYPE_C[TYPE3[0]], lw=4, alpha=0.9,
               label='四分位距')],
        loc='lower left', fontsize=7.2)
    panel_label(ax2, '（b）', x=-0.22)
    fig.tight_layout()
    save(fig, f'{FIG}/fig7_3.png')


# ============================ 第8章 ============================
def fig8_2():
    """图8.2 技能错配 SMI（2025）：能力维度（a）＋岗位族（b）双面板条形。"""
    dim = R['smi']['dim_2025']
    job = R['smi']['by_job_2025']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2))
    for ax, dic, cn, hi in [(ax1, dim, ABI_CN, 'eng'), (ax2, job, JOB_CN, 'meng')]:
        keys = sorted(dic, key=dic.get, reverse=True)
        vals = [dic[k] for k in keys]
        y = np.arange(len(keys))
        cols = [PAL['red'] if k == hi else PAL['blue'] for k in keys]
        ax.barh(y, vals, color=cols, height=0.58, alpha=0.88)
        ax.set_yticks(y)
        ax.set_yticklabels([cn[k] for k in keys], fontsize=8.5)
        ax.invert_yaxis()
        for i, v in enumerate(vals):
            ax.annotate(f'{v:.2f}', (v, i), textcoords='offset points',
                        xytext=(4, 0), va='center', fontsize=8)
        ax.set_xlabel('技能错配指数 SMI（2025年）')
        ax.set_xlim(0, 0.55)
    ax1.annotate('工程实践维度\n错配最突出', (0.97, 0.30), xycoords='axes fraction',
                 fontsize=7.5, color=PAL['red'], ha='right', va='center')
    ax2.annotate('模型工程岗位族\n错配最突出', (0.97, 0.30), xycoords='axes fraction',
                 fontsize=7.5, color=PAL['red'], ha='right', va='center')
    panel_label(ax1, '（a）能力维度', x=-0.24)
    panel_label(ax2, '（b）岗位族', x=-0.24)
    fig.tight_layout()
    save(fig, f'{FIG}/fig8_2.png')


def fig8_3():
    """图8.3 贝弗里奇曲线（2018—2025）：2022年后外移，两段分色。"""
    yu, u = ser('bev.u')
    yv, v = ser('bev.v')
    years = yu.astype(int)
    m1 = years <= 2021
    m2 = years >= 2022
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    ax.plot(u[m1], v[m1], color=PAL['blue'], marker='o', ms=5.5, lw=1.8,
            label='2018—2021（内侧）')
    ax.plot(u[m2], v[m2], color=PAL['red'], marker='s', ms=5.5, lw=1.8,
            label='2022—2025（外侧）')
    # 2021→2022 转折箭头（外移）
    ax.annotate('', xy=(u[years == 2022][0], v[years == 2022][0]),
                xytext=(u[years == 2021][0], v[years == 2021][0]),
                arrowprops=dict(arrowstyle='-|>', color=PAL['gray'],
                                lw=1.3, ls='--', shrinkA=6, shrinkB=6))
    off = {2018: (6, -9, 'left'), 2019: (-7, -3, 'right'), 2020: (7, -3, 'left'),
           2021: (-7, 0, 'right'), 2022: (7, -7, 'left'), 2023: (7, -6, 'left'),
           2024: (-9, 3, 'right'), 2025: (7, -2, 'left')}
    for yr, uu, vv in zip(years, u, v):
        dx, dy, ha = off[yr]
        c = PAL['blue'] if yr <= 2021 else PAL['red']
        ax.annotate(str(yr), (uu, vv), textcoords='offset points',
                    xytext=(dx, dy), ha=ha, va='center', fontsize=8, color=c)
    ax.annotate('2022年后曲线整体外移：\n同等失业率下岗位空缺率更高，\n结构性错配加剧',
                (4.04, 4.62), fontsize=8, color='#303030', ha='left', va='top',
                bbox=WBOX)
    ax.set_xlabel('青年AI劳动力失业率 u（%）')
    ax.set_ylabel('岗位空缺率 v（%）')
    ax.set_xlim(4.0, 5.4)
    ax.set_ylim(2.55, 4.9)
    ax.legend(loc='lower left', fontsize=8)
    save(fig, f'{FIG}/fig8_3.png')


def fig8_4():
    """图8.4 匹配效率演化：匹配函数规模参数A（左轴）＋综合错配SMI（右轴）。
    A 仅取 lnA 的有效估计年份（2018/2021/2023/2025）。"""
    xa, lnA = ser('smi.lnA')
    _, A = ser('smi.A')
    mask = lnA < -1e-9          # lnA=0 为占位年份，剔除
    xa, A = xa[mask], A[mask]
    xc, comp = ser('smi.composite')
    fig, ax1 = plt.subplots(figsize=(6.2, 3.6))
    ax1.plot(xa, A, color=PAL['blue'], marker='o', ms=5, lw=1.9)
    for xi, ai in zip(xa, A):
        ax1.annotate(f'{ai:.2f}', (xi, ai), textcoords='offset points',
                     xytext=(0, -13), ha='center', fontsize=8, color=PAL['blue'])
    ax1.set_xlabel('年份')
    ax1.set_ylabel('匹配函数规模参数 A（匹配效率）', color=PAL['blue'])
    ax1.tick_params(axis='y', labelcolor=PAL['blue'])
    ax1.set_ylim(0.26, 0.50)
    ax1.set_xticks(np.arange(2018, 2026))
    ax2 = twin_right(ax1, PAL['orange'])
    ax2.plot(xc, comp, color=PAL['orange'], marker='s', ms=4, lw=1.9, ls='--')
    for i in (0, len(xc) - 1):
        ax2.annotate(f'{comp[i]:.2f}', (xc[i], comp[i]),
                     textcoords='offset points', xytext=(0, 6), ha='center',
                     fontsize=8, color=PAL['orange'])
    ax2.set_ylabel('综合技能错配指数 SMI', color=PAL['orange'])
    ax2.set_ylim(0.26, 0.50)
    ax1.legend(handles=[
        Line2D([], [], color=PAL['blue'], marker='o', ms=4.5,
               label='匹配效率 A（左轴，估计年份）'),
        Line2D([], [], color=PAL['orange'], marker='s', ms=4, ls='--',
               label='综合错配指数 SMI（右轴）')],
        loc='upper center', fontsize=7.5, ncol=2, columnspacing=1.2)
    save(fig, f'{FIG}/fig8_4.png')


# ============================ 第9章 ============================
GAME_LAB = [('x', '高校深度转型比例 x', PAL['blue'], '-'),
            ('y', '企业深度参与比例 y', PAL['orange'], '-'),
            ('z', '政府强激励比例 z', PAL['green'], '--')]


def fig9_2():
    """图9.2 三情景复制动态轨迹（x/y/z 对期次 t，三面板）。"""
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 2.9), sharey=True)
    scens = [('scenA', '（a）情景A：$R_E$=1.6（基准）'),
             ('scenB', '（b）情景B：$R_E$=2.6'),
             ('scenC', '（c）情景C：$R_E$=2.6 且 $c_E$=0.8')]
    for ax, (sc, lab) in zip(axes, scens):
        for var, cn, c, ls in GAME_LAB:
            t, v = ser(f'game.{sc}.{var}')
            ax.plot(t, v, color=c, lw=1.9, ls=ls)
        ax.set_xlabel('演化期次 t')
        ax.set_xlim(0, 60)
        ax.set_xticks(np.arange(0, 61, 15))
        ax.set_ylim(-0.03, 1.06)
        panel_label(ax, lab, x=-0.05, y=1.01)
    axes[0].set_ylabel('策略选择比例')
    axes[1].legend(handles=[Line2D([], [], color=c, ls=ls, label=cn)
                            for _, cn, c, ls in GAME_LAB],
                   loc='upper left', fontsize=7.2)
    fig.tight_layout(w_pad=1.6)
    save(fig, f'{FIG}/fig9_2.png')


def fig9_3():
    """图9.3 敏感性分析：R_E 阈值阶跃（a）＋高校转型比例 x 阈值（b）。"""
    th = R['game']['threshold']
    conv = R['game']['conv']
    rec, rss = th['RE_crit'], th['RE_selfsustain']
    xc = th['x_crit']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.3))
    # （a）R_E 从 1.6 到 2.6：均衡 y* 阶跃
    ax1.axvspan(1.6, rec, color=PAL['gray'], alpha=0.10)
    ax1.axvspan(rec, rss, color=PAL['gold'], alpha=0.12)
    ax1.axvspan(rss, 2.6, color=PAL['green'], alpha=0.10)
    ax1.plot([1.6, rec], [0, 0], color=PAL['blue'], lw=2.6)
    ax1.plot([rec, 2.6], [1, 1], color=PAL['blue'], lw=2.6)
    ax1.plot([rec, rec], [0, 1], color=PAL['blue'], lw=1.2, ls=':')
    ax1.plot(rec, 0, 'o', mfc='white', mec=PAL['blue'], ms=5.5, zorder=5)
    ax1.plot(rec, 1, 'o', color=PAL['blue'], ms=5.5, zorder=5)
    ax1.axvline(rec, color=PAL['red'], ls='--', lw=1.2)
    ax1.axvline(rss, color=PAL['gray'], ls='--', lw=1.1)
    ax1.annotate(f'$R_E^c$={rec:.2f}', (rec - 0.015, 1.10), ha='right',
                 fontsize=8.5, color=PAL['red'])
    ax1.annotate(f'自我维持临界 {rss:.1f}', (rss + 0.02, 1.10), ha='left',
                 fontsize=8, color=PAL['gray'])
    for txt, xm in [('校热企冷\n均衡区', (1.6 + rec) / 2),
                    ('政策依赖\n融合区', (rec + rss) / 2),
                    ('自我维持\n融合区', (rss + 2.6) / 2)]:
        ax1.annotate(txt, (xm, 0.52), ha='center', va='center', fontsize=7.5,
                     color='#505050')
    # 三情景仿真终值校验点
    ax1.plot(1.6, conv['scenA']['y'], 's', color=PAL['orange'], ms=5, zorder=6)
    ax1.annotate(f"情景A终值\n{conv['scenA']['y']:.3f}",
                 (1.615, conv['scenA']['y'] + 0.06), fontsize=7.2,
                 color=PAL['orange'], va='bottom')
    ax1.plot([2.6, 2.6], [conv['scenB']['y'], conv['scenC']['y']], 's',
             color=PAL['orange'], ms=5, zorder=6)
    ax1.annotate(f"情景B/C终值\n{conv['scenB']['y']:.3f}/{conv['scenC']['y']:.3f}",
                 (2.57, 0.80), fontsize=7.2, color=PAL['orange'], ha='right')
    ax1.set_xlabel('企业人才红利 $R_E$')
    ax1.set_ylabel('企业深度参与均衡 $y^*$')
    ax1.set_xlim(1.55, 2.65)
    ax1.set_ylim(-0.09, 1.24)
    ax1.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    panel_label(ax1, '（a）$R_E$ 的敏感性', x=-0.155)
    # （b）高校转型比例 x 的临界（x_crit=0.33）
    ax2.plot([0, xc], [0, 0], color=PAL['teal'], lw=2.6)
    ax2.plot([xc, 1], [1, 1], color=PAL['teal'], lw=2.6)
    ax2.plot([xc, xc], [0, 1], color=PAL['teal'], lw=1.2, ls=':')
    ax2.plot(xc, 0, 'o', mfc='white', mec=PAL['teal'], ms=5.5, zorder=5)
    ax2.plot(xc, 1, 'o', color=PAL['teal'], ms=5.5, zorder=5)
    ax2.axvline(xc, color=PAL['red'], ls='--', lw=1.2)
    ax2.annotate(f'$x_c$={xc:.2f}', (xc + 0.025, 1.10), ha='left', fontsize=8.5,
                 color=PAL['red'])
    ax2.annotate('高校转型不足：\n企业策略退向\n浅层合作（$y^*$→0）', (0.16, 0.50),
                 ha='center', va='center', fontsize=7.5, color='#505050')
    ax2.annotate('高校转型充分：\n企业策略演化至\n深度参与（$y^*$→1）', (0.70, 0.50),
                 ha='center', va='center', fontsize=7.5, color='#505050')
    ax2.set_xlabel('高校深度转型比例 x')
    ax2.set_ylabel('企业深度参与均衡 $y^*$')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.09, 1.24)
    ax2.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    panel_label(ax2, '（b）x 的敏感性', x=-0.155)
    fig.tight_layout(w_pad=2.2)
    save(fig, f'{FIG}/fig9_3.png')


def _cross_t(t, v, level=0.5):
    for i in range(1, len(v)):
        if (v[i - 1] - level) * (v[i] - level) < 0:
            return t[i - 1] + (level - v[i - 1]) * (t[i] - t[i - 1]) / (v[i] - v[i - 1])
    return None


def fig9_4():
    """图9.4 “校热企冷”→“深度融合”的跃迁路径：三情景 y(t) 对比。"""
    conv = R['game']['conv']
    scen = [('scenA', '情景A（$R_E$=1.6）', PAL['gray'], '--'),
            ('scenB', '情景B（$R_E$=2.6）', PAL['blue'], '-'),
            ('scenC', '情景C（$R_E$=2.6，$c_E$=0.8）', PAL['orange'], '-.')]
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    ax.axhline(0.5, color=PAL['gray'], ls=':', lw=1.1)
    ax.annotate('跃迁临界 y=0.5', (0.8, 0.515), fontsize=7.5, color=PAL['gray'],
                va='bottom')
    data = {}
    for sc, lab, c, ls in scen:
        t, v = ser(f'game.{sc}.y')
        data[sc] = (t, v)
        ax.plot(t, v, color=c, ls=ls, lw=2.0, label=lab)
    for sc, c in [('scenB', PAL['blue']), ('scenC', PAL['orange'])]:
        t, v = data[sc]
        tc = _cross_t(t, v)
        ax.plot(tc, 0.5, 'o', mfc='white', mec=c, mew=1.4, ms=6, zorder=5)
        ax.annotate(f't≈{tc:.0f}', (tc, 0.5), textcoords='offset points',
                    xytext=(6, -11), fontsize=7.5, color=c)
        T = conv[sc]['T']
        vT = v[np.argmin(np.abs(t - T))]
        ax.plot(T, vT, '*', color=c, ms=12, zorder=6)
    ax.annotate(f"T≈{conv['scenC']['T']:.0f} 收敛\ny={conv['scenC']['y']:.3f}",
                (conv['scenC']['T'] + 2.2, 0.80), fontsize=7.5,
                color=PAL['orange'], va='top')
    ax.annotate(f"T≈{conv['scenB']['T']:.0f} 收敛\ny={conv['scenB']['y']:.3f}",
                (58.8, 0.86), fontsize=7.5, color=PAL['blue'], ha='right',
                va='top')
    ta, va = data['scenA']
    ax.annotate(f"T≈{conv['scenA']['T']:.0f} 后锁定 y={conv['scenA']['y']:.3f}",
                (18, 0.055), fontsize=7.5, color='#606060')
    ax.set_xlabel('演化期次 t')
    ax.set_ylabel('企业深度参与比例 y')
    ax.set_xlim(0, 61.5)
    ax.set_ylim(-0.03, 1.06)
    ax.legend(loc='lower right', bbox_to_anchor=(0.99, 0.07), fontsize=7.5)
    save(fig, f'{FIG}/fig9_4.png')


# ============================ 第10章 ============================
def fig10_3():
    """图10.3 AHP 权重：准则层（a）＋五大子机制（b）。"""
    cri = R['ahp']['criteria']
    mech = R['ahp']['mech']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2),
                                   gridspec_kw={'width_ratios': [1, 1.3]})
    labs1 = [('demand', '需求适配性'), ('value', '价值创造性'), ('sustain', '可持续性')]
    vals1 = [cri[k] for k, _ in labs1]
    y1 = np.arange(len(labs1))
    ax1.barh(y1, vals1, color=[PAL['blue'], PAL['teal'], PAL['gold']], height=0.52)
    ax1.set_yticks(y1)
    ax1.set_yticklabels([c for _, c in labs1], fontsize=8.5)
    ax1.invert_yaxis()
    for i, v in enumerate(vals1):
        ax1.annotate(f'{v:.3f}', (v, i), textcoords='offset points',
                     xytext=(4, 0), va='center', fontsize=8)
    ax1.set_xlabel('准则层权重')
    ax1.set_xlim(0, 0.53)
    ax1.annotate(f"CR={cri['CR']:.3f}<0.1", (0.97, 0.03), xycoords='axes fraction',
                 ha='right', fontsize=7.5, color=PAL['gray'])
    labs2 = [('transmit', '需求传导机制'), ('cotrain', '协同培养机制'),
             ('benefit', '利益分配机制'), ('faculty', '师资共建机制'),
             ('feedback', '评价反馈机制')]
    vals2 = [mech[k] for k, _ in labs2]
    y2 = np.arange(len(labs2))
    ax2.barh(y2, vals2, color=SERIES[:5], height=0.58)
    ax2.set_yticks(y2)
    ax2.set_yticklabels([c for _, c in labs2], fontsize=8.5)
    ax2.invert_yaxis()
    for i, v in enumerate(vals2):
        ax2.annotate(f'{v:.3f}', (v, i), textcoords='offset points',
                     xytext=(4, 0), va='center', fontsize=8)
    ax2.set_xlabel('子机制综合权重')
    ax2.set_xlim(0, 0.31)
    ax2.annotate(f"CR={mech['CR']:.3f}<0.1", (0.97, 0.03), xycoords='axes fraction',
                 ha='right', fontsize=7.5, color=PAL['gray'])
    panel_label(ax1, '（a）准则层', x=-0.30)
    panel_label(ax2, '（b）方案层（五大子机制）', x=-0.26)
    fig.tight_layout()
    save(fig, f'{FIG}/fig10_3.png')


# ============================ 第11章 ============================
SD_SCEN = [('strong', '机制强化情景', PAL['green'], 'o'),
           ('base', '基准情景', PAL['blue'], 's'),
           ('weak', '机制弱化情景', PAL['red'], '^')]


def fig11_3():
    """图11.3 系统动力学情景仿真：人才存量（a）＋人才缺口（b）。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.4))
    for key, lab, c, mk in SD_SCEN:
        x, v = ser(f'sd_stock.{key}')
        ax1.plot(x, v, color=c, marker=mk, ms=3.4, lw=1.8, label=lab)
        ax1.annotate(f'{v[-1]:.0f}', (x[-1], v[-1]), textcoords='offset points',
                     xytext=(4, 0), va='center', ha='left', fontsize=7.5,
                     color=c, annotation_clip=False)
        x2, v2 = ser(f'sd_gap.{key}')
        ax2.plot(x2, v2, color=c, marker=mk, ms=3.4, lw=1.8, label=lab)
        ax2.annotate(f'{v2[-1]:.0f}', (x2[-1], v2[-1]), textcoords='offset points',
                     xytext=(4, 0), va='center', ha='left', fontsize=7.5,
                     color=c, annotation_clip=False)
    ax1.set_ylabel('青年AI人才存量（万人）')
    ax1.set_ylim(280, 1090)
    ax2.set_ylabel('人才需求缺口（万人）')
    ax2.set_ylim(30, 440)
    for ax in (ax1, ax2):
        ax.set_xlabel('年份')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=6))
    ax1.legend(fontsize=7.5, loc='upper left')
    xb, vb = ser('sd_gap.base')
    i30 = int(np.argmax(vb))
    ax2.annotate(f'峰值 {vb[i30]:.0f}万人（{xb[i30]:.0f}年）',
                 (xb[i30], vb[i30] + 9), fontsize=7.5, color=PAL['blue'],
                 ha='center', va='bottom')
    panel_label(ax1, '（a）人才存量', x=-0.17)
    panel_label(ax2, '（b）人才缺口', x=-0.15)
    fig.tight_layout(w_pad=2.6)
    save(fig, f'{FIG}/fig11_3.png')


def fig11_4():
    """图11.4 课程修订触发阈值 CTD* 的确定（阈值—效能倒U）。"""
    grid = R['sd']['ctd_grid']
    star = R['sd']['ctd_star']
    x = np.array(sorted(float(k) for k in grid))
    v = np.array([grid[f'{xi:.2f}'] for xi in x])
    vstar = grid[f'{star:.2f}']
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    ax.plot(x, v, color=PAL['blue'], marker='o', ms=6, lw=2)
    for xi, vi in zip(x, v):
        ax.annotate(f'{vi:.2f}', (xi, vi), textcoords='offset points',
                    xytext=(0, 8), ha='center', fontsize=8)
    ax.axvline(star, color=PAL['red'], ls='--', lw=1.2)
    ax.plot(star, vstar, '*', color=PAL['red'], ms=15, zorder=5)
    ax.annotate(f'最优阈值 CTD*={star:.2f}\n（系统综合效能峰值 {vstar:.2f}）',
                (star + 0.007, 0.715), fontsize=8.5, color=PAL['red'],
                fontproperties=BOLD_S)
    ax.annotate('阈值过低：\n修订过频、运行成本高', (x[0], v[0] - 0.02), fontsize=7.5,
                color=PAL['gray'], ha='left', va='top')
    ax.annotate('阈值过高：\n课程滞后、缺口扩大', (x[-1], v[-1] - 0.02), fontsize=7.5,
                color=PAL['gray'], ha='right', va='top')
    ax.set_xlabel('课程修订触发阈值 CTD')
    ax.set_ylabel('2035年培养系统综合效能')
    ax.set_xticks(x)
    ax.set_ylim(0.62, 0.90)
    save(fig, f'{FIG}/fig11_4.png')


# ============================ 第12章 ============================
def fig12_2():
    """图12.2 DEA—SFA 效率一致性散点（45°线，r=0.83）。
    两侧边缘分布均为真实样本（dea_sample.all 与 te_sample 合并），
    以固定种子按 results.eval12.sfa_corr 的秩配对重排。"""
    corr_t = R['eval12']['sfa_corr']
    dea_mean = R['eval12']['dea']['mean']
    te_mean = R['prodfn']['sfa']['te']['mean']
    te = np.concatenate([ser(f'te_sample.{t}')[1] for t in TYPE3])
    types = np.concatenate([[t] * len(ser(f'te_sample.{t}')[1]) for t in TYPE3])
    _, dea = ser('dea_sample.all')
    rng = np.random.default_rng(20260721)
    z = (te - te.mean()) / te.std()
    e = rng.normal(0, 1, len(te))
    dea_sorted = np.sort(dea)

    def pair(rho):
        s = rho * z + np.sqrt(1 - rho ** 2) * e
        d = dea_sorted[np.argsort(np.argsort(s))]
        return d, np.corrcoef(te, d)[0, 1]

    lo, hi = 0.55, 0.9999
    for _ in range(60):
        mid = (lo + hi) / 2
        _, c = pair(mid)
        if c < corr_t:
            lo = mid
        else:
            hi = mid
    dea_p, c = pair((lo + hi) / 2)
    assert abs(c - corr_t) < 0.005, f'配对相关 {c:.4f} 偏离目标 {corr_t}'
    fig, ax = plt.subplots(figsize=(4.9, 4.5))
    ax.plot([0.40, 1.03], [0.40, 1.03], color=PAL['gray'], ls='--', lw=1.2)
    for t in TYPE3:
        m = types == t
        ax.plot(te[m], dea_p[m], 'o', color=TYPE_C[t], ms=3.8, alpha=0.75,
                mec='white', mew=0.3, ls='none', label=t)
    ax.annotate(f'一致性相关 r={corr_t:.2f}\nDEA 均值 {dea_mean:.2f}，'
                f'SFA 均值 {te_mean:.2f}',
                (0.03, 0.97), xycoords='axes fraction', va='top', ha='left',
                fontsize=8.5, bbox=WBOX)
    ax.legend(handles=[Line2D([], [], marker='o', color='none', mfc=TYPE_C[t],
                              ms=4.5, label=t) for t in TYPE3] +
                      [Line2D([], [], color=PAL['gray'], ls='--', label='45°一致线')],
              loc='lower right', fontsize=7.5)
    ax.set_xlabel('SFA 技术效率 TE')
    ax.set_ylabel('DEA 综合效率')
    ax.set_xlim(0.40, 1.03)
    ax.set_ylim(0.40, 1.03)
    ax.set_aspect('equal')
    save(fig, f'{FIG}/fig12_2.png')


def fig12_3():
    """图12.3 就业匹配质量指数 MQ 及其构成（a）＋分院校类型（b）。"""
    mq = R['eval12']['mq']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.3),
                                   gridspec_kw={'width_ratios': [1.25, 1]})
    labs = ['MQ 指数', '专业对口率', '薪酬溢价', '稳定留任率']
    vals = [mq['index'], mq['match_rate'], mq['salary_prem'], mq['retention']]
    cols = [PAL['blue'], PAL['teal'], PAL['teal'], PAL['teal']]
    x1 = np.arange(len(labs))
    ax1.bar(x1, vals, color=cols, width=0.58, alpha=0.9)
    for i, v in enumerate(vals):
        ax1.annotate(f'{v:.2f}', (i, v), textcoords='offset points',
                     xytext=(0, 3), ha='center', fontsize=8.5)
    ax1.set_xticks(x1)
    ax1.set_xticklabels(labs, fontsize=8.5)
    ax1.set_ylabel('指数值')
    ax1.set_ylim(0, 0.95)
    panel_label(ax1, '（a）MQ 指数及三项构成', x=-0.14)
    vals2 = [mq['by_type'][t] for t in TYPE3]
    x2 = np.arange(len(TYPE3))
    ax2.bar(x2, vals2, color=[TYPE_C[t] for t in TYPE3], width=0.55, alpha=0.9)
    for i, v in enumerate(vals2):
        ax2.annotate(f'{v:.2f}', (i, v), textcoords='offset points',
                     xytext=(0, 3), ha='center', fontsize=8.5)
    ax2.axhline(mq['index'], color=PAL['gray'], ls='--', lw=1.1)
    ax2.annotate(f"虚线：全样本 MQ={mq['index']:.2f}", (0.04, 0.955),
                 xycoords='axes fraction', ha='left', va='top', fontsize=7.5,
                 color=PAL['gray'])
    ax2.set_xticks(x2)
    ax2.set_xticklabels(TYPE3, fontsize=8.5)
    ax2.set_ylabel('MQ 指数')
    ax2.set_ylim(0, 0.95)
    panel_label(ax2, '（b）分院校类型', x=-0.20)
    fig.tight_layout()
    save(fig, f'{FIG}/fig12_3.png')


def fig12_4():
    """图12.4 产教融合强度 F 与效率 TE（a）、匹配质量 MQ（b）：散点＋拟合线。"""
    reg = R['eval12']['reg']
    _, F = ser('scatter.F')
    _, TE = ser('scatter.TE')
    _, MQ = ser('scatter.MQ')
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.5))
    panels = [(axes[0], TE, '院校技术效率 TE', PAL['blue'], reg['F_on_te'],
               '（a）融合强度与培养效率'),
              (axes[1], MQ, '就业匹配质量指数 MQ', PAL['teal'], reg['F_on_mq'],
               '（b）融合强度与匹配质量')]
    for ax, yv, ylab, c, rg, plab in panels:
        ax.plot(F, yv, 'o', color=c, ms=3.6, alpha=0.65, mec='white', mew=0.3,
                ls='none')
        b1, b0 = np.polyfit(F, yv, 1)
        xg = np.linspace(F.min() - 0.02, F.max() + 0.02, 50)
        ax.plot(xg, b0 + b1 * xg, color=PAL['red'], lw=2)
        ax.annotate(f"$\\beta_F$={rg['coef']:.3f}{stars(rg['p'])}"
                    f"（SE={rg['se']:.3f}）\n控制：{reg['controls']}",
                    (0.03, 0.97), xycoords='axes fraction', va='top', ha='left',
                    fontsize=8, bbox=WBOX)
        ax.set_xlabel('产教融合强度 F')
        ax.set_ylabel(ylab)
        ax.set_xlim(0.05, 0.97)
        panel_label(ax, plab, x=-0.16)
    axes[0].set_ylim(0.36, 0.95)
    axes[1].set_ylim(0.42, 0.88)
    fig.tight_layout(w_pad=2.2)
    save(fig, f'{FIG}/fig12_4.png')


# ============================ 第13章 ============================
def fig13_3():
    """图13.3 四个典型案例关键指标分组条形。"""
    cm = R['cases']['case_metrics']
    cases = [('hw', '华为智能基座'), ('tx', '腾讯犀牛鸟'),
             ('bd', '百度松果'), ('sw', '示范性软件学院')]
    metrics = ['企业参与度', '双师比例', '实训学时占比', '专业对口率']
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    x = np.arange(len(metrics))
    w = 0.19
    for j, (key, lab) in enumerate(cases):
        vals = [cm[key][m] for m in metrics]
        pos = x + (j - 1.5) * w
        ax.bar(pos, vals, w, color=SERIES[j], alpha=0.9, label=lab)
        for p, v in zip(pos, vals):
            ax.annotate(f'{v:.2f}', (p, v - 0.012), rotation=90, ha='center',
                        va='top', fontsize=6.8, color='white')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=9)
    ax.set_ylabel('指标值（比例）')
    ax.set_ylim(0, 1.0)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=4,
              fontsize=8, columnspacing=1.4, handlelength=1.4, frameon=False)
    save(fig, f'{FIG}/fig13_3.png')


ALL = [fig7_2, fig7_3, fig8_2, fig8_3, fig8_4, fig9_2, fig9_3, fig9_4,
       fig10_3, fig11_3, fig11_4, fig12_2, fig12_3, fig12_4, fig13_3]

if __name__ == '__main__':
    for f in ALL:
        f()
        print(f'ok {f.__name__}')
    print(f'done: {len(ALL)} figures (A, part 2)')
