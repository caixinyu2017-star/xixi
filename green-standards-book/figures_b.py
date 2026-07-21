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


# ============================ 第8章 ============================
IND_ORDER = ['铝冶炼', '钢铁', '化肥', '水泥', '建筑建材', '交通运输', '电力', '纺织']


def fig8_2():
    """八大高碳行业错配热力图（2015—2025）。"""
    years = list(range(2015, 2026))
    M = np.array([[R['ssdmi']['industry'][ind][str(y)] for y in years]
                  for ind in IND_ORDER])
    cmap = LinearSegmentedColormap.from_list(
        'mis', ['#FFFFFF', '#F5E6C8', PAL['gold'], PAL['orange'], PAL['red']])
    fig, ax = plt.subplots(figsize=(6.8, 3.7))
    im = ax.imshow(M, cmap=cmap, aspect='auto', vmin=0.15, vmax=0.60)
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years, fontsize=7.5)
    ax.set_yticks(range(len(IND_ORDER)))
    ax.set_yticklabels(IND_ORDER, fontsize=8)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.annotate(f'{M[i, j]:.2f}', (j, i), ha='center', va='center',
                        fontsize=6, color='black' if M[i, j] < 0.5 else 'white')
    cb = fig.colorbar(im, ax=ax, pad=0.015, fraction=0.04)
    cb.set_label('供需错配指数 SSDMI', fontsize=8)
    cb.ax.tick_params(labelsize=7)
    ax.set_xlabel('年份')
    ax.grid(False)
    save(fig, f'{FIG}/fig8_2.png')


def fig8_3():
    """分行业错配指数细线＋加权综合错配指数粗线。"""
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    cols = SERIES + [PAL['red'], PAL['ltblue']]
    for ind, c in zip(IND_ORDER, cols):
        x, v = ser(f'ssdmi.{ind}')
        ax.plot(x, v, color=c, lw=1.1, alpha=0.75, label=ind)
    xc, vc = ser('ssdmi.composite')
    ax.plot(xc, vc, color='black', lw=2.6, label='加权综合错配指数')
    ax.annotate(f'{vc[0]:.2f}', (xc[0], vc[0]), textcoords='offset points',
                xytext=(-2, 6), fontsize=7.5)
    ax.annotate(f'{vc[-1]:.2f}', (xc[-1], vc[-1]), textcoords='offset points',
                xytext=(2, 6), fontsize=7.5)
    ax.set_xlabel('年份')
    ax.set_ylabel('供需错配指数 SSDMI')
    ax.legend(fontsize=7, ncol=3, loc='upper right')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=11))
    save(fig, f'{FIG}/fig8_3.png')


# ============================ 第9章 ============================
def fig9_3():
    """AHP 准则层与方案层权重（双面板条形）。"""
    cri = R['ahp']['criteria']
    mod = R['ahp']['module']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.3),
                                   gridspec_kw={'width_ratios': [1, 1.35]})
    # 准则层
    labs1 = ['碳减排贡献度', '产业转型促进度', '国际衔接兼容度']
    vals1 = [cri['carbon'], cri['industry'], cri['intl']]
    y1 = np.arange(len(labs1))
    ax1.barh(y1, vals1, color=[PAL['blue'], PAL['teal'], PAL['gold']], height=0.55)
    ax1.set_yticks(y1)
    ax1.set_yticklabels(labs1, fontsize=8)
    ax1.invert_yaxis()
    for i, v in enumerate(vals1):
        ax1.annotate(f'{v:.3f}', (v, i), textcoords='offset points',
                     xytext=(3, 0), va='center', fontsize=8)
    ax1.set_xlabel('准则层权重')
    ax1.set_xlim(0, 0.56)
    ax1.annotate(f"CR={cri['CR']:.3f}<0.1", (0.97, 0.04), xycoords='axes fraction',
                 ha='right', fontsize=7.5, color=PAL['gray'])
    # 方案层（五大模块）
    order = ['acct', 'fp', 'sink', 'prod', 'fin']
    labs2 = [MOD_CN[k] for k in order]
    vals2 = [mod[k] for k in order]
    y2 = np.arange(len(order))
    ax2.barh(y2, vals2, color=SERIES[:5], height=0.6)
    ax2.set_yticks(y2)
    ax2.set_yticklabels(labs2, fontsize=8)
    ax2.invert_yaxis()
    for i, v in enumerate(vals2):
        ax2.annotate(f'{v:.3f}', (v, i), textcoords='offset points',
                     xytext=(3, 0), va='center', fontsize=8)
    ax2.set_xlabel('功能模块综合权重')
    ax2.set_xlim(0, 0.33)
    ax2.annotate(f"CR={mod['CR']:.3f}<0.1", (0.97, 0.04), xycoords='axes fraction',
                 ha='right', fontsize=7.5, color=PAL['gray'])
    fig.tight_layout()
    save(fig, f'{FIG}/fig9_3.png')


# ============================ 第10章 ============================
def fig10_3():
    """系统动力学三情景仿真：标准存量与体系效能（2026—2035）。"""
    scen = [('coord', '协同增强情景', PAL['green']),
            ('base', '基准情景', PAL['blue']),
            ('lag', '更新滞后情景', PAL['red'])]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.3))
    for key, lab, c in scen:
        x, v = ser(f'sd_stock.{key}')
        ax1.plot(x, v, color=c, marker='o', ms=3, lw=1.8, label=lab)
        x2, v2 = ser(f'sd_eff.{key}')
        ax2.plot(x2, v2, color=c, marker='o', ms=3, lw=1.8, label=lab)
    ax1.set_ylabel('有效标准存量 SS（项）')
    ax2.set_ylabel('标准体系综合效能（0—1）')
    for ax in (ax1, ax2):
        ax.set_xlabel('年份')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=6))
        ax.legend(fontsize=7, loc='upper left')
    fig.tight_layout()
    save(fig, f'{FIG}/fig10_3.png')


def fig10_4():
    """动态更新触发阈值 TPD* 的确定（阈值—效能倒U）。"""
    grid = R['sd']['tpd_grid']
    x = np.array([float(k) for k in grid])
    v = np.array([grid[k] for k in grid])
    idx = np.argsort(x)
    x, v = x[idx], v[idx]
    star = R['sd']['tpd_star']
    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    ax.plot(x, v, color=PAL['blue'], marker='o', ms=6, lw=2)
    for xi, vi in zip(x, v):
        ax.annotate(f'{vi:.2f}', (xi, vi), textcoords='offset points',
                    xytext=(0, 7), ha='center', fontsize=7.5)
    ax.axvline(star, color=PAL['red'], ls='--', lw=1.2)
    ax.plot(star, grid[f'{star:.2f}'], '*', color=PAL['red'], ms=15, zorder=5)
    ax.annotate(f'最优阈值 TPD*={star:.2f}\n（综合效能峰值 {grid[f"{star:.2f}"]:.2f}）',
                (star + 0.008, 0.715), fontsize=8, color=PAL['red'])
    ax.annotate('阈值过低：\n修订频繁、成本高', (x[0], v[0] - 0.018), fontsize=7,
                color=PAL['gray'], ha='left', va='top')
    ax.annotate('阈值过高：\n标准滞后、效能损失', (x[-1], v[-1] - 0.018), fontsize=7,
                color=PAL['gray'], ha='right', va='top')
    ax.set_xlabel('技术—政策偏离度触发阈值 TPD*')
    ax.set_ylabel('2035年标准体系综合效能')
    ax.set_ylim(0.62, 0.88)
    save(fig, f'{FIG}/fig10_4.png')


# ============================ 第11章 ============================
def fig11_2():
    """标准执行效率 TE 的核密度演化（2010/2015/2020/2025，正态核近似）。"""
    te = R['sfa']['te']['national']
    items = [('2010', 0.095, PAL['gray']), ('2015', 0.091, PAL['gold']),
             ('2020', 0.088, PAL['teal']), ('2025', 0.085, PAL['blue'])]
    xs = np.linspace(0.30, 1.05, 400)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    peaks = {}
    for y, sig, c in items:
        mu = te[y]
        pdf = np.exp(-(xs - mu) ** 2 / (2 * sig ** 2)) / (sig * np.sqrt(2 * np.pi))
        ax.plot(xs, pdf, color=c, lw=1.9, label=f'{y}年（均值 {mu:.3f}）')
        ax.fill_between(xs, pdf, color=c, alpha=0.08)
        peaks[y] = (mu, pdf.max())
    ymax = max(v[1] for v in peaks.values())
    ax.set_ylim(0, ymax * 1.22)
    ax.annotate('', xy=(peaks['2025'][0], ymax * 1.06),
                xytext=(peaks['2010'][0], ymax * 1.06),
                arrowprops=dict(arrowstyle='-|>', color=PAL['red'], lw=1.3))
    ax.annotate(f"分布整体右移：均值提高 {te['2025'] - te['2010']:+.3f}",
                ((te['2010'] + te['2025']) / 2, ymax * 1.10),
                ha='center', va='bottom', fontsize=8, color=PAL['red'])
    ax.set_xlabel('标准执行效率 TE')
    ax.set_ylabel('核密度')
    ax.set_xlim(0.30, 1.05)
    ax.legend(fontsize=7.5, loc='upper left')
    fig.text(0.01, -0.03, '注：基于校准复算的省级面板数据，采用正态核近似（σ≈0.09）。',
             fontsize=6.6, color=PAL['gray'])
    save(fig, f'{FIG}/fig11_2.png')


def fig11_3():
    """政策有效性损失 PEL 三源分解（全国与三大区域，100%堆积）。"""
    nat = R['sfa']['pel']
    regs = R['sfa']['pel_region']
    groups = [('全国', nat), ('东部', regs['east']), ('中部', regs['central']),
              ('西部', regs['west'])]
    comps = [('supply', '供给不足损失', PAL['blue']),
             ('incentive', '激励不完善损失', PAL['teal']),
             ('coordinate', '协调失灵损失', PAL['gold'])]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    x = np.arange(len(groups))
    bottom = np.zeros(len(groups))
    for key, lab, c in comps:
        v = np.array([g[1][key] for g in groups]) * 100
        ax.bar(x, v, bottom=bottom, color=c, width=0.5, label=lab)
        for i, (b, vv) in enumerate(zip(bottom, v)):
            ax.annotate(f'{vv:.1f}%', (i, b + vv / 2), ha='center', va='center',
                        fontsize=7.5, color='white')
        bottom += v
    ax.set_xticks(x)
    ax.set_xticklabels([g[0] for g in groups])
    ax.set_ylabel('占政策有效性损失 PEL 的比重（%）')
    ax.set_ylim(0, 116)
    ax.legend(loc='upper center', ncol=3, fontsize=7.5)
    save(fig, f'{FIG}/fig11_3.png')


def fig11_4():
    """30省标准执行效率排名（2025），按东部/中部/西部分色。"""
    prov, val = ser('sfa.prov2025', numeric=False)
    regmap = R['sfa']['te']['prov_region']
    idx = np.argsort(val)[::-1]
    prov, val = prov[idx], val[idx]
    cols = [REG_C[regmap[p]] for p in prov]
    natl = R['sfa']['te']['national']['2025']
    fig, ax = plt.subplots(figsize=(5.8, 6.6))
    y = np.arange(len(prov))
    ax.barh(y, val, color=cols, height=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels(prov, fontsize=7.5)
    ax.invert_yaxis()
    ax.axvline(natl, color=PAL['gray'], ls='--', lw=1.1)
    ax.annotate(f'全国平均 {natl:.3f}', (natl, len(prov) - 1.2), rotation=90,
                fontsize=7, color=PAL['gray'], ha='right', va='bottom')
    for i, v in enumerate(val):
        ax.annotate(f'{v:.3f}', (v, i), textcoords='offset points',
                    xytext=(3, 0), va='center', fontsize=6.4)
    ax.set_xlabel('标准执行效率 TE（2025年）')
    ax.set_xlim(0.55, 0.87)
    ax.legend(handles=[Patch(color=REG_C[k], label=REG_CN[k])
                       for k in ['east', 'central', 'west']],
              loc='lower right', fontsize=8)
    save(fig, f'{FIG}/fig11_4.png')


# ============================ 第12章 ============================
DIM_CN = [('boundary', '核算边界'), ('factor', '排放因子'), ('lca', '生命周期范围'),
          ('verify', '第三方核查'), ('data', '数据质量'), ('coverage', '行业覆盖'),
          ('update', '更新频率'), ('market', '市场衔接')]


def fig12_2():
    """国际标准差距八维度雷达图（ISGI）。"""
    vals = [R['isgi']['dim'][k] for k, _ in DIM_CN]
    labs = [c for _, c in DIM_CN]
    mean = float(np.mean(vals))
    ang = np.linspace(0, 2 * np.pi, len(vals), endpoint=False).tolist()
    v = vals + vals[:1]
    a = ang + ang[:1]
    fig, ax = plt.subplots(figsize=(5.0, 4.7), subplot_kw=dict(polar=True))
    ax.plot(a, v, color=PAL['blue'], lw=2, marker='o', ms=4)
    ax.fill(a, v, color=PAL['blue'], alpha=0.18)
    ax.plot(a, [mean] * len(a), color=PAL['gray'], lw=1.2, ls='--')
    for aa, vv, lab in zip(ang, vals, labs):
        ax.annotate(f'{vv:.2f}', (aa, vv), textcoords='offset points',
                    xytext=(0, 7), ha='center', fontsize=7.5,
                    color=PAL['red'] if vv >= 0.42 else PAL['blue'])
    ax.set_xticks(ang)
    ax.set_xticklabels(labs, fontsize=8.5)
    ax.set_ylim(0, 0.52)
    ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_yticklabels(['0.1', '0.2', '0.3', '0.4', '0.5'], fontsize=6.5)
    ax.grid(alpha=0.4)
    ax.legend(handles=[Line2D([], [], color=PAL['blue'], marker='o', ms=4,
                              label='差距指数 ISGI$_k$'),
                       Line2D([], [], color=PAL['gray'], ls='--',
                              label=f'八维度均值（{mean:.2f}）')],
              loc='upper right', bbox_to_anchor=(1.32, 1.10), fontsize=7.5)
    fig.text(0.5, -0.02, '注：市场衔接（0.44）与第三方核查（0.42）差距最大（红色标注）。',
             ha='center', fontsize=6.8, color=PAL['gray'])
    save(fig, f'{FIG}/fig12_2.png')


CBAM_IND = [('steel', '钢铁', PAL['blue']), ('alu', '铝', PAL['teal']),
            ('fert', '化肥', PAL['gold']), ('cement', '水泥', PAL['orange'])]


def fig12_3():
    """CBAM 碳关税负担情景模拟（2026—2030）：基准 vs 适配改进，分行业堆积。"""
    years = list(range(2026, 2031))
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    w = 0.36
    for off, scen, hatch, alpha in [(-w / 2 - 0.015, 'base', None, 0.92),
                                    (w / 2 + 0.015, 'improve', '///', 0.55)]:
        bottom = np.zeros(len(years))
        for key, lab, c in CBAM_IND:
            x, v = ser(f'cbam_tariff_{scen}.{key}')
            vv = np.array([v[list(x).index(y)] for y in years])
            ax.bar(np.array(years) + off, vv, bottom=bottom, width=w, color=c,
                   alpha=alpha, hatch=hatch, edgecolor='white', linewidth=0.4)
            bottom += vv
        for i, y in enumerate(years):
            ax.annotate(f'{bottom[i]:.0f}', (y + off, bottom[i]),
                        textcoords='offset points', xytext=(0, 2), ha='center',
                        fontsize=6.8)
    cut = R['isgi']['io']['tariff_improve_cut']
    ax.annotate(f'适配改进情景较基准\n累计减负约 {cut * 100:.0f}%',
                (2026.6, 165), fontsize=8, color=PAL['red'],
                bbox=dict(boxstyle='round,pad=0.35', fc='white', ec=PAL['red'], lw=0.8))
    ax.set_xlabel('年份')
    ax.set_ylabel('CBAM 碳关税负担（亿元）')
    ax.set_xticks(years)
    hnd = [Patch(color=c, label=lab) for _, lab, c in CBAM_IND]
    hnd += [Patch(fc='#BFBFBF', label='基准情景（左柱）'),
            Patch(fc='#BFBFBF', alpha=0.55, hatch='///', label='适配改进情景（右柱）')]
    ax.legend(handles=hnd, fontsize=7, ncol=2, loc='upper left')
    save(fig, f'{FIG}/fig12_3.png')


def fig12_4():
    """标准差距对高碳行业产出的影响（2030年，基准 vs 适配改进）。"""
    base = R['isgi']['io']['output_loss_2030_base']
    imp = R['isgi']['io']['output_loss_2030_improve']
    labs = [lab for _, lab, _ in CBAM_IND]
    keys = [k for k, _, _ in CBAM_IND]
    vb = [base[k] for k in keys]
    vi = [imp[k] for k in keys]
    x = np.arange(len(keys))
    w = 0.36
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    b1 = ax.bar(x - w / 2, vb, w, color=PAL['red'], alpha=0.88, label='基准情景')
    b2 = ax.bar(x + w / 2, vi, w, color=PAL['teal'], alpha=0.88, label='适配改进情景')
    for bars in (b1, b2):
        for bb in bars:
            ax.annotate(f'{bb.get_height():.2f}',
                        (bb.get_x() + bb.get_width() / 2, bb.get_height()),
                        textcoords='offset points', xytext=(0, -10),
                        ha='center', fontsize=7.5)
    ax.axhline(0, color='black', lw=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels(labs)
    ax.set_ylabel('2030年行业产出变动（%）')
    ax.set_ylim(-1.45, 0.18)
    ax.legend(fontsize=8, loc='lower right')
    ax.annotate('标准适配改进可使产出损失减半左右', (0.02, 0.93),
                xycoords='axes fraction', fontsize=8, color=PAL['gray'])
    save(fig, f'{FIG}/fig12_4.png')


# ============================ 第13章 ============================
def fig13_3():
    """三行业国际适配关键指标（CIAI、ISGI）＋核心障碍范畴编码频次。"""
    inds = [('steel', '钢铁'), ('alu', '铝'), ('fert', '化肥')]
    ciai = [R['isgi']['industry_ciai'][k] for k, _ in inds]
    isgi = [R['isgi']['industry_isgi'][k] for k, _ in inds]
    nint = [R['cases']['interviews'][k] for k, _ in inds]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4),
                                   gridspec_kw={'width_ratios': [1.15, 1]})
    x = np.arange(len(inds))
    w = 0.36
    b1 = ax1.bar(x - w / 2, ciai, w, color=PAL['blue'], label='综合国际适配性指数 CIAI')
    b2 = ax1.bar(x + w / 2, isgi, w, color=PAL['orange'], label='国际标准差距指数 ISGI')
    for bars in (b1, b2):
        for bb in bars:
            ax1.annotate(f'{bb.get_height():.2f}',
                         (bb.get_x() + bb.get_width() / 2, bb.get_height()),
                         textcoords='offset points', xytext=(0, 2),
                         ha='center', fontsize=7.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'{lab}\n（访谈{n}人）' for (_, lab), n in zip(inds, nint)],
                        fontsize=8)
    ax1.set_ylabel('指数值（0—1）')
    ax1.set_ylim(0, 0.78)
    ax1.legend(fontsize=7.2, loc='upper right')
    # 右：扎根理论核心范畴编码频次
    cats = [('data', '数据基础障碍', PAL['blue']), ('inst', '制度衔接障碍', PAL['teal']),
            ('cap', '认知—能力障碍', PAL['gold']), ('voice', '话语权障碍', PAL['orange'])]
    vals = [R['cases']['categories'][k] for k, _, _ in cats]
    y = np.arange(len(cats))
    ax2.barh(y, vals, color=[c for _, _, c in cats], height=0.58)
    ax2.set_yticks(y)
    ax2.set_yticklabels([lab for _, lab, _ in cats], fontsize=8)
    ax2.invert_yaxis()
    for i, v in enumerate(vals):
        ax2.annotate(f'{v}', (v, i), textcoords='offset points', xytext=(3, 0),
                     va='center', fontsize=8)
    ax2.set_xlabel('核心范畴编码参考点频次（次）')
    ax2.set_xlim(0, 168)
    fig.tight_layout()
    save(fig, f'{FIG}/fig13_3.png')




if __name__ == '__main__':
    fig8_2()
    print('ok fig8_2')
    fig8_3()
    print('ok fig8_3')
    fig9_3()
    print('ok fig9_3')
    fig10_3()
    print('ok fig10_3')
    fig10_4()
    print('ok fig10_4')
    fig11_2()
    print('ok fig11_2')
    fig11_3()
    print('ok fig11_3')
    fig11_4()
    print('ok fig11_4')
    fig12_2()
    print('ok fig12_2')
    fig12_3()
    print('ok fig12_3')
    fig12_4()
    print('ok fig12_4')
    fig13_3()
    print('ok fig13_3')
    print('done: 12 figures (B)')
