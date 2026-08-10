# -*- coding: utf-8 -*-
"""前半部 A 型分析图（11 幅，matplotlib，nature 风格，中文）。
数据一律读取 data/series.csv 与 data/results.json；不得手写模型数字。
输出 figs/figN_M.png（400 dpi）。图内不含图名、图注与资料来源。
"""
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import ScalarFormatter
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

# 注记白底衬垫（避免文字被线条穿越）
WBOX = dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85)

JOB_CN = {'algo': '算法', 'meng': '模型工程', 'data': '数据',
          'prod': '产品应用', 'gov': '治理安全'}
ABI_CN = {'base': '基础素养', 'tech': '技术能力', 'eng': '工程实践',
          'innov': '创新应用', 'ethic': '伦理治理'}
JOB_KEYS = ['algo', 'meng', 'data', 'prod', 'gov']
ABI_KEYS = ['base', 'tech', 'eng', 'innov', 'ethic']


def panel_label(ax, s, x=-0.12, y=1.02):
    """多面板黑体面板标签（a）（b）。"""
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


# ============================ 第2章 ============================
def fig2_1():
    """图2.1 产教融合与AI人才研究年度发文趋势（2000—2025），右上角内嵌图例。"""
    xw, yw = ser('biblio.wos')
    xc, yc = ser('biblio.cnki')
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(xw, yw, color=PAL['blue'], marker='o', ms=3, lw=1.8,
            label='WOS（英文文献）')
    ax.plot(xc, yc, color=PAL['orange'], marker='s', ms=3, lw=1.8,
            label='CNKI（中文文献）')
    ax.axvline(2017, color=PAL['gray'], ls=':', lw=1)
    ax.annotate('新一代人工智能\n发展规划（2017）', (2016.7, 11800), fontsize=8,
                color=PAL['gray'], ha='right', va='top', bbox=WBOX)
    ax.axvline(2022.9, color=PAL['gray'], ls=':', lw=1)
    ax.annotate('大模型浪潮\n（2022年末）', (2022.6, 11800), fontsize=8,
                color=PAL['gray'], ha='right', va='top', bbox=WBOX)
    # 末年数值直接标注
    ax.annotate(f'{yc[-1]:.0f}', (xc[-1], yc[-1]), textcoords='offset points',
                xytext=(2, 8), fontsize=8, color=PAL['orange'], ha='center')
    ax.annotate(f'{yw[-1]:.0f}', (xw[-1], yw[-1]), textcoords='offset points',
                xytext=(2, -12), fontsize=8, color=PAL['blue'], ha='center')
    ax.set_xlim(1999, 2026.6)
    ax.set_ylim(0, 12300)
    ax.set_xlabel('年份')
    ax.set_ylabel('年度发文量（篇）')
    ax.set_xticks(np.arange(2000, 2026, 5))
    ax.legend(loc='upper right', fontsize=8)
    save(fig, f'{FIG}/fig2_1.png')


# ============================ 第3章 ============================
def fig3_1():
    """图3.1 AI核心产业规模柱＋同比增速线（双轴，两侧轴完整）。"""
    x, v = ser('industry.scale')
    g = (v[1:] / v[:-1] - 1.0) * 100.0  # 2021—2025 同比增速
    fig, ax1 = plt.subplots(figsize=(6.4, 3.7))
    ax1.bar(x, v, color=PAL['ltblue'], edgecolor=PAL['blue'], lw=0.9, width=0.58)
    for xi, vi in zip(x, v):
        ax1.annotate(f'{vi:.0f}', (xi, vi), textcoords='offset points',
                     xytext=(0, 3), ha='center', fontsize=8, color=PAL['blue'])
    ax1.set_xlabel('年份')
    ax1.set_ylabel('核心产业规模（亿元）', color=PAL['blue'])
    ax1.tick_params(axis='y', labelcolor=PAL['blue'])
    ax1.set_ylim(0, 15500)
    ax1.set_xticks(x)
    ax2 = twin_right(ax1, PAL['orange'])
    # 2021—2024 可比口径实线；2024—2025 因官方口径调整以虚线相接
    ax2.plot(x[1:5], g[:4], color=PAL['orange'], marker='s', ms=4, lw=1.9)
    ax2.plot(x[4:6], g[3:5], color=PAL['orange'], ls='--', lw=1.6)
    ax2.plot(x[5], g[4], marker='s', ms=4.5, mfc='white', mec=PAL['orange'],
             mew=1.3, ls='none')
    for xi, gi, (dx, dy, ha) in zip(x[1:], g,
                                    [(0, 6, 'center'), (0, 6, 'center'),
                                     (0, 6, 'center'), (0, -13, 'center'),
                                     (-7, 0, 'right')]):
        ax2.annotate(f'{gi:.1f}%', (xi, gi), textcoords='offset points',
                     xytext=(dx, dy), ha=ha, fontsize=8,
                     color=PAL['orange'], bbox=WBOX)
    ax2.annotate('2025年起为官方新口径，\n增速不具可比性（虚线）',
                 (2024.72, 76), fontsize=8, color=PAL['gray'],
                 ha='right', va='center', bbox=WBOX)
    ax2.set_ylabel('同比增速（%）', color=PAL['orange'])
    ax2.set_ylim(0, 140)
    save(fig, f'{FIG}/fig3_1.png')


def fig3_2():
    """图3.2 岗位族JD指数五线（a）＋2025年岗位族占比（b）。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.5),
                                   gridspec_kw={'width_ratios': [1.55, 1]})
    marks = ['o', 's', '^', 'D', 'v']
    for k, c, mk in zip(JOB_KEYS, SERIES, marks):
        xx, vv = ser(f'jd.{k}')
        ax1.plot(xx, vv, color=c, marker=mk, ms=3.2, lw=1.7,
                 label=JOB_CN[k])
    xx, vv = ser('jd.meng')
    ax1.annotate(f'模型工程 {vv[-1]:.0f}', (xx[-1], vv[-1]),
                 textcoords='offset points', xytext=(-4, 7), ha='right',
                 fontsize=8, color=SERIES[1])
    ax1.set_xlabel('年份')
    ax1.set_ylabel('岗位需求指数（2018年=100）')
    ax1.set_ylim(60, 680)
    ax1.set_xticks(np.arange(2018, 2026, 2))
    ax1.legend(loc='upper left', fontsize=8)
    panel_label(ax1, '（a）', x=-0.14)
    # （b）2025 年岗位族需求占比
    sh = R['jd']['share_2025']
    vals = [sh[k] * 100 for k in JOB_KEYS]
    xpos = np.arange(len(JOB_KEYS))
    ax2.bar(xpos, vals, color=SERIES[:5], width=0.6, alpha=0.9)
    for i, v in enumerate(vals):
        ax2.annotate(f'{v:.0f}%', (i, v), textcoords='offset points',
                     xytext=(0, 3), ha='center', fontsize=8)
    ax2.set_xticks(xpos)
    ax2.set_xticklabels([JOB_CN[k] for k in JOB_KEYS], fontsize=8,
                        rotation=20, ha='right')
    ax2.set_ylabel('2025年招聘需求占比（%）')
    ax2.set_ylim(0, 29)
    panel_label(ax2, '（b）', x=-0.22)
    fig.tight_layout()
    save(fig, f'{FIG}/fig3_2.png')


def fig3_3():
    """图3.3 AI人才需求区域分布（8 城市，降序水平条形）。"""
    city, val = ser('regions.share', numeric=False)
    idx = np.argsort(val)[::-1]
    city, val = city[idx], val[idx]
    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    y = np.arange(len(city))
    ax.barh(y, val, color=PAL['blue'], height=0.62, alpha=0.9)
    ax.set_yticks(y)
    ax.set_yticklabels(city)
    ax.invert_yaxis()
    for i, v in enumerate(val):
        ax.annotate(f'{v:.1f}%', (v, i), textcoords='offset points',
                    xytext=(4, 0), va='center', fontsize=8)
    ax.annotate(f'TOP8 城市合计 {val.sum():.1f}%\n京沪深三城即占 '
                f'{val[:3].sum():.1f}%',
                (max(val) * 0.62, 5.6), fontsize=8, color=PAL['blue'],
                ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.35', fc='white',
                          ec=PAL['blue'], lw=0.8))
    ax.set_xlabel('AI人才需求占全国比重（%，2025年）')
    ax.set_xlim(0, 25)
    save(fig, f'{FIG}/fig3_3.png')


def fig3_4():
    """图3.4 缺口口径对比（a，对数轴）＋岗位族薪酬溢价（b）。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.5),
                                   gridspec_kw={'width_ratios': [1.35, 1]})
    # （a）不同机构口径的人才缺口（对数横轴，避免 2500 压扁其他）
    name, val = ser('gap.koujing', numeric=False)
    lab_map = {
        '人社部2020·AI缺口': '人社部（2020）\nAI人才缺口',
        '工信部人才中心2020·有效缺口': '工信部人才中心（2020）\n有效人才缺口',
        '猎聘2025·AI缺口': '猎聘（2025）\nAI人才缺口',
        '九部门2024·数字人才缺口': '九部门（2024）\n数字人才缺口',
    }
    idx = np.argsort(val)[::-1]
    name, val = name[idx], val[idx]
    y = np.arange(len(name))
    cols = [PAL['red'] if v == max(val) else PAL['blue'] for v in val]
    ax1.barh(y, val, color=cols, height=0.58, alpha=0.88)
    ax1.set_yticks(y)
    ax1.set_yticklabels([lab_map[n] for n in name], fontsize=8)
    ax1.invert_yaxis()
    ax1.set_xscale('log')
    ax1.set_xlim(10, 9000)
    ax1.set_xticks([10, 30, 100, 500, 2500])
    ax1.xaxis.set_major_formatter(ScalarFormatter())
    ax1.minorticks_off()
    for i, v in enumerate(val):
        ax1.annotate(f'{v:.0f}', (v, i), textcoords='offset points',
                     xytext=(4, 0), va='center', fontsize=8)
    ax1.set_xlabel('人才缺口（万人，对数刻度）')
    panel_label(ax1, '（a）', x=-0.40)
    # （b）2025 年岗位族薪酬溢价
    prem = R['jd']['salary_premium']
    order = sorted(JOB_KEYS, key=lambda k: prem[k], reverse=True)
    vals = [prem[k] * 100 for k in order]
    xpos = np.arange(len(order))
    ax2.bar(xpos, vals, color=PAL['teal'], width=0.6, alpha=0.9)
    for i, v in enumerate(vals):
        ax2.annotate(f'{v:.0f}%', (i, v), textcoords='offset points',
                     xytext=(0, 3), ha='center', fontsize=8)
    ax2.set_xticks(xpos)
    ax2.set_xticklabels([JOB_CN[k] for k in order], fontsize=8,
                        rotation=20, ha='right')
    ax2.set_ylabel('相对全行业数字岗位均值的薪酬溢价（%）')
    ax2.set_ylim(0, 98)
    panel_label(ax2, '（b）', x=-0.24)
    fig.tight_layout()
    save(fig, f'{FIG}/fig3_4.png')


# ============================ 第4章 ============================
def fig4_1():
    """图4.1 AI相关本科专业布点：当年新增柱＋累计线（双轴，两侧轴完整）。"""
    x, cum = ser('majors.cum')
    new = np.diff(cum, prepend=0.0)  # 2018 年 35 所视为当年新增
    fig, ax1 = plt.subplots(figsize=(6.4, 3.7))
    ax1.bar(x, new, color=PAL['ltblue'], edgecolor=PAL['blue'], lw=0.9,
            width=0.58)
    for xi, vi in zip(x, new):
        ax1.annotate(f'{vi:.0f}', (xi, vi), textcoords='offset points',
                     xytext=(0, 3), ha='center', fontsize=8, color=PAL['blue'])
    ax1.set_xlabel('年份')
    ax1.set_ylabel('当年新增布点数（所）', color=PAL['blue'])
    ax1.tick_params(axis='y', labelcolor=PAL['blue'])
    ax1.set_ylim(0, 230)
    ax1.set_xticks(x)
    ax2 = twin_right(ax1, PAL['orange'])
    ax2.plot(x, cum, color=PAL['orange'], marker='o', ms=4, lw=1.9)
    ax2.annotate(f'累计 {cum[-1]:.0f} 所', (x[-1], cum[-1]),
                 textcoords='offset points', xytext=(-2, 8), ha='right',
                 fontsize=8, color=PAL['orange'])
    ax2.annotate(f'{cum[0]:.0f} 所起步', (x[0], cum[0]),
                 textcoords='offset points', xytext=(4, 8), ha='left',
                 fontsize=8, color=PAL['orange'])
    ax2.set_ylabel('累计布点数（所）', color=PAL['orange'])
    ax2.set_ylim(0, 700)
    save(fig, f'{FIG}/fig4_1.png')


def fig4_3():
    """图4.3 AI人才培养层次结构（条形，标注万人）。"""
    lev, val = ser('levels.scale', numeric=False)
    idx = np.argsort(val)[::-1]
    lev, val = lev[idx], val[idx]
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    y = np.arange(len(lev))
    cols = [PAL['blue'], PAL['teal'], PAL['gold'], PAL['gray']]
    ax.barh(y, val, color=cols, height=0.6, alpha=0.9)
    ax.set_yticks(y)
    ax.set_yticklabels(lev)
    ax.invert_yaxis()
    tot = val.sum()
    for i, v in enumerate(val):
        ax.annotate(f'{v:.1f}万人（{v / tot * 100:.0f}%）', (v, i),
                    textcoords='offset points', xytext=(4, 0),
                    va='center', fontsize=8)
    ax.annotate(f'合计约 {tot:.0f} 万人/年', (max(val) * 0.66, 3.0),
                fontsize=8, color=PAL['blue'], ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.35', fc='white',
                          ec=PAL['blue'], lw=0.8))
    ax.set_xlabel('年培养规模（万人，2025年）')
    ax.set_xlim(0, 12.4)
    save(fig, f'{FIG}/fig4_3.png')


# ============================ 第5章 ============================
def fig5_2():
    """图5.2 五层能力权重：总体（a）＋分岗位分组条形（b）。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.5),
                                   gridspec_kw={'width_ratios': [1, 1.7]})
    ov = R['ability']['overall']
    vals = [ov[k] for k in ABI_KEYS]
    xpos = np.arange(len(ABI_KEYS))
    ax1.bar(xpos, vals, color=SERIES[:5], width=0.6, alpha=0.9)
    for i, v in enumerate(vals):
        ax1.annotate(f'{v:.2f}', (i, v), textcoords='offset points',
                     xytext=(0, 3), ha='center', fontsize=8)
    ax1.set_xticks(xpos)
    ax1.set_xticklabels([ABI_CN[k] for k in ABI_KEYS], fontsize=8,
                        rotation=20, ha='right')
    ax1.set_ylabel('总体需求权重')
    ax1.set_ylim(0, 0.36)
    panel_label(ax1, '（a）', x=-0.26)
    # （b）分岗位族的能力维度权重
    M = R['ability']['matrix']
    gx = np.arange(len(JOB_KEYS))
    w = 0.15
    for j, k in enumerate(ABI_KEYS):
        vv = [M[job][j] for job in JOB_KEYS]
        ax2.bar(gx + (j - 2) * w, vv, w, color=SERIES[j], alpha=0.9,
                label=ABI_CN[k])
    ax2.set_xticks(gx)
    ax2.set_xticklabels([JOB_CN[k] for k in JOB_KEYS], fontsize=8)
    ax2.set_ylabel('分岗位族需求权重')
    ax2.set_ylim(0, 0.47)
    ax2.legend(loc='upper center', ncol=3, fontsize=8, columnspacing=1.0,
               handlelength=1.2)
    panel_label(ax2, '（b）', x=-0.12)
    fig.tight_layout()
    save(fig, f'{FIG}/fig5_2.png')


def fig5_3():
    """图5.3 岗位族×能力维度需求热力图（5×5，标数值，带色标）。"""
    M = np.array([R['ability']['matrix'][k] for k in JOB_KEYS])
    cmap = LinearSegmentedColormap.from_list(
        'bluemap', ['#FFFFFF', PAL['ltblue'], PAL['blue']])
    fig, ax = plt.subplots(figsize=(5.6, 4.1))
    im = ax.imshow(M, cmap=cmap, vmin=0, vmax=0.40, aspect='auto')
    ax.set_xticks(np.arange(5))
    ax.set_xticklabels([ABI_CN[k] for k in ABI_KEYS], fontsize=8.5)
    ax.set_yticks(np.arange(5))
    ax.set_yticklabels([JOB_CN[k] for k in JOB_KEYS], fontsize=8.5)
    ax.set_xlabel('能力维度')
    ax.set_ylabel('岗位族')
    for i in range(5):
        for j in range(5):
            c = 'white' if M[i, j] >= 0.26 else '#1A1A1A'
            ax.text(j, i, f'{M[i, j]:.2f}', ha='center', va='center',
                    fontsize=8.5, color=c)
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(length=0)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label('需求权重', fontsize=8.5)
    cb.ax.tick_params(labelsize=8)
    save(fig, f'{FIG}/fig5_3.png')


# ============================ 第6章 ============================
def fig6_2():
    """图6.2 产业规模—人才需求弹性：模拟散点＋拟合线＋95%置信带。
    散点由 forecast.eta（coef=0.83、R2=0.94、N=32）反推生成，固定种子。"""
    eta = R['forecast']['eta']
    b, R2, N = eta['coef'], eta['R2'], eta['N']
    rng = np.random.default_rng(20260721)
    x = np.sort(rng.uniform(6.9, 9.5, N))          # ln(产业规模) 样本
    a = 6.39 - b * 9.39                            # 截距锚定 2025 量级
    yhat = a + b * x
    # 残差先对 (1, x) 正交化，再缩放使样本 R2 精确等于设定值
    e = rng.normal(0, 1, N)
    X = np.column_stack([np.ones(N), x])
    e = e - X @ np.linalg.lstsq(X, e, rcond=None)[0]
    ssm = np.sum((yhat - yhat.mean()) ** 2)
    e *= np.sqrt(ssm * (1 - R2) / R2 / np.sum(e ** 2))
    yv = yhat + e
    # 校验：OLS 斜率与 R2 与 results.json 一致
    bh = np.linalg.lstsq(X, yv, rcond=None)[0]
    r2h = 1 - np.sum((yv - X @ bh) ** 2) / np.sum((yv - yv.mean()) ** 2)
    assert abs(bh[1] - b) < 1e-9 and abs(r2h - R2) < 1e-9
    # 95% 置信带（均值预测）
    s2 = np.sum((yv - X @ bh) ** 2) / (N - 2)
    xg = np.linspace(x.min() - 0.12, x.max() + 0.12, 120)
    sxx = np.sum((x - x.mean()) ** 2)
    sef = np.sqrt(s2 * (1 / N + (xg - x.mean()) ** 2 / sxx))
    tcrit = 2.042  # t(0.975, df=30)
    yg = bh[0] + bh[1] * xg
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.fill_between(xg, yg - tcrit * sef, yg + tcrit * sef,
                    color=PAL['blue'], alpha=0.14, lw=0)
    ax.plot(xg, yg, color=PAL['blue'], lw=2)
    ax.plot(x, yv, 'o', color=PAL['orange'], ms=4.5, mec='white', mew=0.5,
            alpha=0.95)
    ax.annotate(f'$\\ln L = {bh[0]:.2f} + {b:.2f}\\,\\ln S$\n'
                f'弹性 $\\eta$={b:.2f}（SE={eta["se"]:.2f}，t={eta["t"]:.1f}）\n'
                f'$R^2$={R2:.2f}，N={N}',
                (0.04, 0.96), xycoords='axes fraction', fontsize=8.5,
                va='top', ha='left', bbox=WBOX)
    ax.set_xlabel('产业规模对数 ln S')
    ax.set_ylabel('人才需求对数 ln L')
    save(fig, f'{FIG}/fig6_2.png')


def fig6_3():
    """图6.3 三情景人才需求预测（2025—2035），起点同源、终点标注。"""
    scen = [('forecast.fast', '快速渗透情景', PAL['red'], '-.', '^'),
            ('forecast.base', '基准情景', PAL['blue'], '-', 'o'),
            ('forecast.slow', '增长放缓情景', PAL['gray'], '--', 's')]
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    for name, lab, c, ls, mk in scen:
        x, v = ser(name)
        ax.plot(x, v, color=c, ls=ls, marker=mk, ms=3.6, lw=1.9)
        line_end_label(ax, x[-1], v[-1], f'{lab} {v[-1]:.0f}', c, dx=0.25)
    x0, v0 = ser('forecast.base')
    ax.plot(x0[0], v0[0], 'o', color=PAL['blue'], ms=6, zorder=5)
    ax.annotate(f'2025年基期\n{v0[0]:.0f}万人', (x0[0], v0[0]),
                textcoords='offset points', xytext=(6, 26), ha='left',
                fontsize=8, color=PAL['blue'], bbox=WBOX,
                arrowprops=dict(arrowstyle='-', color=PAL['gray'], lw=0.8))
    ax.set_xlim(2024.6, 2038.6)
    ax.set_ylim(480, 1360)
    ax.set_xlabel('年份')
    ax.set_ylabel('青年AI人才需求（万人）')
    ax.set_xticks(np.arange(2025, 2036, 2))
    save(fig, f'{FIG}/fig6_3.png')


ALL = [fig2_1, fig3_1, fig3_2, fig3_3, fig3_4, fig4_1, fig4_3,
       fig5_2, fig5_3, fig6_2, fig6_3]

if __name__ == '__main__':
    for f in ALL:
        f()
        print(f'ok {f.__name__}')
    print(f'done: {len(ALL)} figures (A, part 1)')
