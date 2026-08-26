# -*- coding: utf-8 -*-
"""A 型分析图（第 7—13 章，11 幅，全部黑白）。"""
import json
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figstyle_bw import BARS, GRAY, LINES, grid_y, panel_label, save

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))
DF = pd.read_csv(os.path.join(HERE, 'data', 'survey.csv'))
MAJORS = ['工学', '理学', '经济管理', '文学法学', '教育艺术', '医学农学']


def bar_kw(i):
    d = dict(BARS[i])
    d.setdefault('edgecolor', '#000000')
    d['linewidth'] = 0.7
    return d


# ---------------------------------------------------------------- 图7.2 供需份额
def fig7_2():
    dem = R['mismatch']['demand']
    sup = R['mismatch']['supply']
    y = np.arange(6)
    fig, ax = plt.subplots(figsize=(5.7, 2.9))
    ax.barh(y + 0.19, [dem[m] * 100 for m in MAJORS], height=0.36,
            label='产业需求份额', **bar_kw(0))
    ax.barh(y - 0.19, [sup[m] * 100 for m in MAJORS], height=0.36,
            label='毕业生供给份额', **bar_kw(1))
    ax.set_yticks(y)
    ax.set_yticklabels(MAJORS, fontsize=8)
    ax.set_xlabel('份额（%）')
    ax.legend(loc='lower right')
    ax.grid(axis='x', linestyle='-', color='#AAAAAA', alpha=0.35, linewidth=0.6)
    ax.grid(axis='y', visible=False)
    ax.set_axisbelow(True)
    ax.invert_yaxis()
    fig.tight_layout()
    save(fig, f'{FIG}/fig7_2.png')


# ---------------------------------------------------------------- 图7.3 匹配溢价分位
def fig7_3():
    taus = ['0.25', '0.5', '0.75']
    co = [R['qreg_wage'][t]['match']['coef'] * 100 for t in taus]
    se = [R['qreg_wage'][t]['match']['se'] * 100 for t in taus]
    ols = R['ols_wage']['coefs']['match']['coef'] * 100
    fig, ax = plt.subplots(figsize=(4.9, 2.8))
    ax.axhline(ols, color=GRAY['g2'], ls='--', lw=1.1)
    ax.annotate(f'OLS：{ols:.2f}', (2.05, ols), fontsize=7.8, va='bottom')
    ax.errorbar(range(3), co, yerr=[1.96 * s for s in se], fmt='o', color='#000',
                markersize=5, capsize=3, elinewidth=1.0)
    ax.set_xticks(range(3))
    ax.set_xticklabels(['第25分位', '中位数', '第75分位'])
    ax.set_ylabel('专业匹配的起薪溢价（%）')
    grid_y(ax)
    fig.tight_layout()
    save(fig, f'{FIG}/fig7_3.png')


# ---------------------------------------------------------------- 图8.1 体制内偏好画像
def fig8_1():
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 2.7))
    ax = axes[0]
    vals = [DF[DF.major == i].civil_exam.mean() * 100 for i in range(6)]
    for i, v in enumerate(vals):
        ax.bar(MAJORS[i], v, width=0.6, **bar_kw(i % 6))
    ax.set_ylabel('备考比例（%）')
    ax.tick_params(axis='x', labelsize=7, rotation=22)
    ax.set_ylim(0, max(vals) * 1.18)
    grid_y(ax)
    panel_label(ax, '（a）分学科')
    ax = axes[1]
    grp = [('城镇非党员', (DF.rural == 0) & (DF.party == 0)),
           ('城镇党员', (DF.rural == 0) & (DF.party == 1)),
           ('农村非党员', (DF.rural == 1) & (DF.party == 0)),
           ('农村党员', (DF.rural == 1) & (DF.party == 1))]
    vals = [DF[m].civil_exam.mean() * 100 for _, m in grp]
    for i, ((nm, _), v) in enumerate(zip(grp, vals)):
        ax.bar(nm, v, width=0.6, **bar_kw(i))
        ax.annotate(f'{v:.1f}', (i, v), textcoords='offset points', xytext=(0, 2.5),
                    ha='center', fontsize=7.4)
    ax.tick_params(axis='x', labelsize=7, rotation=16)
    ax.set_ylim(0, max(vals) * 1.2)
    grid_y(ax)
    panel_label(ax, '（b）分生源与政治面貌')
    fig.tight_layout()
    save(fig, f'{FIG}/fig8_1.png')


# ---------------------------------------------------------------- 图8.3 机会成本瀑布
def fig8_3():
    c = R['civil_cost']
    wage = R['quality']['wage_mean']
    fig, axes = plt.subplots(1, 2, figsize=(6.0, 2.7),
                             gridspec_kw=dict(width_ratios=[1.35, 1]))
    ax = axes[0]
    steps = [('平均月薪', wage), (f'等待 {c["extra_months"]:.1f} 个月',
                              c['forgone_wage'] - wage), ('放弃收入合计', 0)]
    cum = [0, wage, 0]
    vals = [wage, c['forgone_wage'] - wage, c['forgone_wage']]
    for i, ((nm, _), b, v) in enumerate(zip(steps, cum, vals)):
        ax.bar(nm, v, bottom=b, width=0.55, **bar_kw(0 if i == 2 else 1 + i % 2))
    ax.annotate(f'{c["forgone_wage"]:.0f} 元', (2, c['forgone_wage']),
                textcoords='offset points', xytext=(0, 3), ha='center', fontsize=8)
    ax.set_ylabel('金额（元）')
    ax.tick_params(axis='x', labelsize=7.2)
    grid_y(ax)
    panel_label(ax, '（a）备考等待的直接机会成本')
    ax = axes[1]
    grp = [('未备考', DF[DF.civil_exam == 0].employed.mean() * 100),
           ('备考', DF[DF.civil_exam == 1].employed.mean() * 100)]
    for i, (nm, v) in enumerate(grp):
        ax.bar(nm, v, width=0.5, **bar_kw(i))
        ax.annotate(f'{v:.1f}', (i, v), textcoords='offset points', xytext=(0, 2.5),
                    ha='center', fontsize=7.8)
    ax.set_ylabel('落实率（%）')
    ax.set_ylim(0, 105)
    grid_y(ax)
    panel_label(ax, '（b）落实率对照')
    fig.tight_layout()
    save(fig, f'{FIG}/fig8_3.png')


# ---------------------------------------------------------------- 图9.2 服务使用与评价
def fig9_2():
    # 服务链四环节的使用率与有效性评价（R['service']，与正文同源）
    SV = R['service']
    items = list(SV['use'])
    use = [SV['use'][k] for k in items]
    eff = [SV['eff'][k] for k in items]
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=(5.6, 2.9))
    ax.bar(x, use, width=0.5, label='使用率（左轴，%）', **bar_kw(0))
    ax.set_ylabel('使用率（%）')
    ax.set_ylim(0, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(items, fontsize=8)
    grid_y(ax)
    ax2 = ax.twinx()
    ax2.spines['right'].set_visible(True)
    ax2.plot(x, eff, label='有效性评价（右轴，1—5分）', **LINES[1], lw=1.4)
    for xi, v in zip(x, eff):
        ax2.annotate(f'{v:.2f}', (xi, v), textcoords='offset points', xytext=(0, 5),
                     ha='center', fontsize=7.4)
    ax2.set_ylabel('有效性评价（1—5分）')
    ax2.set_ylim(1, 5)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    fig.legend(h1 + h2, l1 + l2, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.10))
    fig.tight_layout()
    save(fig, f'{FIG}/fig9_2.png')


# ---------------------------------------------------------------- 图10.1 Logit AME
def fig10_1():
    pe = R['probit_employ']['coefs']
    items = [('intern', '实习经历（次）'), ('cert', '技能证书（项）'), ('sns', '社会网络强度'),
             ('tier1flag', '“双一流”高校'), ('female', '女性'), ('rural', '农村生源'),
             ('civil_exam', '备考公务员'), ('slow_emp', '慢就业')]
    ame = [pe[k]['ame'] * 100 for k, _ in items]
    se = [pe[k]['se'] * 100 * abs(pe[k]['ame'] / pe[k]['coef']) for k, _ in items]
    y = np.arange(len(items))
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.axvline(0, color='#000', lw=0.9)
    ax.errorbar(ame, y, xerr=[1.96 * s for s in se], fmt='o', color='#000',
                markersize=4.5, capsize=2.6, elinewidth=0.9)
    ax.set_yticks(y)
    ax.set_yticklabels([n for _, n in items], fontsize=8)
    ax.set_xlabel('对落实概率的平均边际效应（百分点）')
    ax.grid(axis='x', linestyle='-', color='#AAAAAA', alpha=0.35, linewidth=0.6)
    ax.grid(axis='y', visible=False)
    ax.set_axisbelow(True)
    ax.invert_yaxis()
    fig.tight_layout()
    save(fig, f'{FIG}/fig10_1.png')


# ---------------------------------------------------------------- 图10.2 工资方程
def fig10_2():
    ow = R['ols_wage']['coefs']
    items = [('tier1flag', '“双一流”'), ('master', '硕士及以上'), ('match', '专业匹配'),
             ('female', '女性'), ('intern', '实习/次'), ('zj', '浙江'), ('js', '江苏')]
    x = np.arange(len(items))
    fig, ax = plt.subplots(figsize=(5.8, 2.9))
    off = [-0.27, -0.09, 0.09, 0.27]
    series = [('OLS', None, 0)] + [(f'第{int(float(t)*100)}分位', t, i + 1)
                                   for i, t in enumerate(['0.25', '0.5', '0.75'])]
    marks = ['o', 's', '^', 'D']
    shades = ['#000000', '#444444', '#777777', '#AAAAAA']
    for (nm, t, j) in series:
        if t is None:
            co = [ow[k]['coef'] * 100 for k, _ in items]
            er = [ow[k]['se'] * 100 * 1.96 for k, _ in items]
        else:
            co = [R['qreg_wage'][t][k]['coef'] * 100 for k, _ in items]
            er = [R['qreg_wage'][t][k]['se'] * 100 * 1.96 for k, _ in items]
        ax.errorbar(x + off[j], co, yerr=er, fmt=marks[j], color=shades[j],
                    markersize=3.8, capsize=1.8, elinewidth=0.8, label=nm, ls='none')
    ax.axhline(0, color='#000', lw=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels([n for _, n in items], fontsize=7.6)
    ax.set_ylabel('对数起薪效应（%）')
    grid_y(ax)
    fig.legend(loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.10))
    fig.tight_layout()
    save(fig, f'{FIG}/fig10_2.png')


# ---------------------------------------------------------------- 图10.3 差异分解
def fig10_3():
    emp = DF[DF.employed == 1].copy()
    emp['lnw'] = np.log(emp.wage)
    raw_g = (emp[emp.female == 0].lnw.mean() - emp[emp.female == 1].lnw.mean()) * 100
    cond_g = -R['ols_wage']['coefs']['female']['coef'] * 100
    raw_r = (emp[emp.rural == 0].lnw.mean() - emp[emp.rural == 1].lnw.mean()) * 100
    cond_r = -R['ols_wage']['coefs']['rural']['coef'] * 100
    x = np.arange(2)
    fig, ax = plt.subplots(figsize=(4.9, 2.8))
    ax.bar(x - 0.18, [raw_g, raw_r], width=0.34, label='原始差距', **bar_kw(0))
    ax.bar(x + 0.18, [cond_g, cond_r], width=0.34, label='条件差距（控制可观测特征）',
           **bar_kw(1))
    for xi, v in zip(x - 0.18, [raw_g, raw_r]):
        ax.annotate(f'{v:.1f}', (xi, v), textcoords='offset points', xytext=(0, 2.5),
                    ha='center', fontsize=7.5)
    for xi, v in zip(x + 0.18, [cond_g, cond_r]):
        ax.annotate(f'{v:.1f}', (xi, v), textcoords='offset points', xytext=(0, 2.5),
                    ha='center', fontsize=7.5)
    ax.set_xticks(x)
    ax.set_xticklabels(['性别（男−女）', '城乡（城镇−农村）'])
    ax.set_ylabel('对数起薪差距（%）')
    ax.legend()
    grid_y(ax)
    fig.tight_layout()
    save(fig, f'{FIG}/fig10_3.png')


# ---------------------------------------------------------------- 图11.2 事件研究
def fig11_2():
    ev = R['did']['event']
    ks = sorted(int(k) for k in ev)
    co = np.array([ev[str(k)]['coef'] for k in ks]) * 100
    se = np.array([ev[str(k)]['se'] for k in ks]) * 100
    ks_p = np.array(ks + [-1])
    co = np.append(co, 0.0)
    se = np.append(se, 0.0)
    o = np.argsort(ks_p)
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    ax.axhline(0, color=GRAY['g2'], lw=0.9)
    ax.axvline(-0.5, color='#000', ls='--', lw=1.0)
    ax.errorbar(ks_p[o], co[o], yerr=1.96 * se[o], fmt='o-', color='#000',
                markersize=4, lw=1.2, capsize=2.4, elinewidth=0.9)
    ax.set_xlabel('相对政策实施的年数（基期为前一年）')
    ax.set_ylabel('对落实率的效应（百分点）')
    ax.set_xticks(ks_p[o])
    grid_y(ax)
    fig.tight_layout()
    save(fig, f'{FIG}/fig11_2.png')


# ---------------------------------------------------------------- 图11.3 安慰剂
def fig11_3():
    pl = R['did']['placebo']
    att = R['did']['att']['coef'] * 100
    xs = np.linspace(-4 * pl['sd'] * 100, 4 * pl['sd'] * 100, 300)
    dens = np.exp(-0.5 * (xs / (pl['sd'] * 100)) ** 2) / (pl['sd'] * 100 * np.sqrt(2 * np.pi))
    fig, ax = plt.subplots(figsize=(4.9, 2.8))
    ax.plot(xs, dens, color='#000', lw=1.3)
    ax.fill_between(xs, dens, color='#CCCCCC', alpha=0.7)
    ax.axvline(att, color='#000', ls='--', lw=1.4)
    ax.annotate(f'实际估计 {att:.2f}', (att, ax.get_ylim()[1] * 0.9), fontsize=7.8,
                ha='right', xytext=(-5, 0), textcoords='offset points')
    ax.set_xlabel('随机化政策年份的估计系数（百分点）')
    ax.set_ylabel('密度')
    grid_y(ax)
    fig.tight_layout()
    save(fig, f'{FIG}/fig11_3.png')


# ---------------------------------------------------------------- 图13.2 政策模拟
def fig13_2():
    ps = R['policy_sim']
    items = [('学科结构调整\n（错配下降20%）', ps['mismatch_cut20']['wage_gain'], '平均起薪提升（%）'),
             ('实习扩容\n（人均+1次）', ps['intern_plus1']['demploy'] * 100, '落实概率提升（pp）'),
             ('期望校准\n（落差收窄10对数点）', abs(ps['expect_calib']['dsat']) * 20, '满意度提升（%）')]
    fig, ax = plt.subplots(figsize=(5.4, 2.8))
    for i, (nm, v, lab) in enumerate(items):
        ax.bar(nm, v, width=0.5, **bar_kw(i))
        ax.annotate(f'{v:.2f}', (i, v), textcoords='offset points', xytext=(0, 3),
                    ha='center', fontsize=8)
    ax.set_ylabel('边际效果（各自口径）')
    ax.tick_params(axis='x', labelsize=7.6)
    grid_y(ax)
    fig.tight_layout()
    save(fig, f'{FIG}/fig13_2.png')


if __name__ == '__main__':
    for f in (fig7_2, fig7_3, fig8_1, fig8_3, fig9_2, fig10_1, fig10_2, fig10_3,
              fig11_2, fig11_3, fig13_2):
        f()
