# -*- coding: utf-8 -*-
"""A 型分析图（第 2—6 章，13 幅，全部黑白）。数据取 results.json / survey.csv / facts_fig.json。"""
import json
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figstyle_bw import BARS, GRAY, LINES, grid_y, panel_label, save

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))
DF = pd.read_csv(os.path.join(HERE, 'data', 'survey.csv'))
FJ = json.load(open(os.path.join(HERE, 'data', 'facts_fig.json'), encoding='utf-8'))

MAJORS = ['工学', '理学', '经济管理', '文学法学', '教育艺术', '医学农学']


def bar_kw(i):
    d = dict(BARS[i])
    d.setdefault('edgecolor', '#000000')
    d['linewidth'] = 0.7
    return d


# ---------------------------------------------------------------- 图3.1 毕业生规模
def fig3_1():
    d = FJ['grads_national']            # {届: 万人}
    yrs = sorted(int(k) for k in d)
    vals = [d[str(y)] for y in yrs]
    fig, ax = plt.subplots(figsize=(5.8, 3.0))
    kw = bar_kw(0)
    ax.bar([str(y) for y in yrs], vals, width=0.62, **kw)
    for i, v in enumerate(vals):
        ax.annotate(f'{v:.0f}', (i, v), textcoords='offset points', xytext=(0, 3),
                    ha='center', fontsize=7.5)
    ax.set_xlabel('届别')
    ax.set_ylabel('普通高校毕业生规模（万人）')
    ax.set_ylim(0, max(vals) * 1.15)
    grid_y(ax)
    fig.tight_layout()
    save(fig, f'{FIG}/fig3_1.png')


# ---------------------------------------------------------------- 图3.2 苏浙沪皖高教与留存
def fig3_2():
    u = FJ['provinces_universities']    # {省: 高校数}
    ret = FJ['retention']               # [[名, 值, 标签], ...]，口径见 facts_fig.json
    fig, axes = plt.subplots(1, 2, figsize=(6.0, 2.7))
    ax = axes[0]
    provs = list(u)
    for i, pr in enumerate(provs):
        ax.bar(pr, u[pr], width=0.6, **bar_kw(i))
        ax.annotate(f'{u[pr]}', (i, u[pr]), textcoords='offset points', xytext=(0, 2.5),
                    ha='center', fontsize=7.5)
    ax.set_ylabel('普通高校数（所）', fontsize=8)
    ax.set_ylim(0, max(u.values()) * 1.18)
    ax.tick_params(axis='x', labelsize=8)
    grid_y(ax)
    ax = axes[1]
    for i, (name, v, lab) in enumerate(ret):
        ax.bar(name, v, width=0.55, **bar_kw(i))
        ax.annotate(lab, (i, v), textcoords='offset points', xytext=(0, 2.5),
                    ha='center', fontsize=7.5)
    ax.set_ylabel('毕业生就业留存率（%）', fontsize=8)
    ax.set_ylim(0, 100)
    ax.tick_params(axis='x', labelsize=8)
    grid_y(ax)
    fig.tight_layout()
    save(fig, f'{FIG}/fig3_2.png')


# ---------------------------------------------------------------- 图3.3 青年失业率
def fig3_3():
    d = FJ['youth_unemp']               # [[label, value], ...] 时间序列
    labs = [x[0] for x in d]
    vals = [x[1] for x in d]
    fig, ax = plt.subplots(figsize=(6.0, 2.9))
    ax.plot(range(len(vals)), vals, **LINES[0], lw=1.5)
    for i, v in enumerate(vals):
        ax.annotate(f'{v:.1f}', (i, v), textcoords='offset points', xytext=(0, 5),
                    ha='center', fontsize=7)
    ax.set_xticks(range(len(labs)))
    ax.set_xticklabels(labs, fontsize=7, rotation=30, ha='right')
    ax.set_ylabel('16—24岁城镇调查失业率（%）')
    ax.axvline(FJ['youth_unemp_break'] - 0.5, color=GRAY['g2'], ls='--', lw=1.0)
    ax.annotate('自此为不含在校生口径', (FJ['youth_unemp_break'] - 0.35, max(vals) * 0.95),
                fontsize=7.5, color=GRAY['g1'])
    ax.set_ylim(0, max(vals) * 1.16)
    grid_y(ax)
    fig.tight_layout()
    save(fig, f'{FIG}/fig3_3.png')


# ---------------------------------------------------------------- 图3.4 样本结构
def fig3_4():
    fig, axes = plt.subplots(1, 4, figsize=(6.4, 2.4))
    panels = [
        ('省份', {'江苏': 1236, '浙江': 1418, '上海': 612, '安徽': 580}),
        ('院校层次', {k.replace('“双一流”高校', '双一流').replace('高校', '').replace('院校', ''): v
                   for k, v in R['profile']['tier'].items()}),
        ('学历层次', R['profile']['degree']),
        ('学科门类', {k[:2]: v for k, v in R['profile']['major'].items()}),
    ]
    for ax, (t, d) in zip(axes, panels):
        keys = list(d)
        vals = list(d.values())
        if max(vals) <= 1.01:
            vals = [v * 100 for v in vals]
            ax.set_ylabel('占比（%）', fontsize=7.5)
        else:
            ax.set_ylabel('样本量（份）', fontsize=7.5)
        for i, (kk, v) in enumerate(zip(keys, vals)):
            ax.bar(kk, v, width=0.6, **bar_kw(i % len(BARS)))
        ax.set_title(t, fontsize=8.5)
        ax.tick_params(axis='x', labelsize=6.6, rotation=28)
        ax.tick_params(axis='y', labelsize=7)
        grid_y(ax)
    fig.tight_layout()
    save(fig, f'{FIG}/fig3_4.png')


# ---------------------------------------------------------------- 图4.1 渠道
def fig4_1():
    ch = R['behavior']['channels']
    keys = sorted(ch, key=ch.get)
    vals = [ch[k] * 100 for k in keys]
    fig, ax = plt.subplots(figsize=(5.5, 2.9))
    ax.barh(keys, vals, height=0.58, **bar_kw(0))
    for i, v in enumerate(vals):
        ax.annotate(f'{v:.1f}', (v, i), textcoords='offset points', xytext=(4, -3),
                    fontsize=7.6)
    ax.set_xlabel('使用率（%）')
    ax.set_xlim(0, max(vals) * 1.14)
    ax.grid(axis='x', linestyle='-', color='#AAAAAA', alpha=0.35, linewidth=0.6)
    ax.grid(axis='y', visible=False)
    ax.set_axisbelow(True)
    fig.tight_layout()
    save(fig, f'{FIG}/fig4_1.png')


# ---------------------------------------------------------------- 图4.2 成本与周期
def fig4_2():
    fig, axes = plt.subplots(1, 2, figsize=(6.0, 2.7))
    ax = axes[0]
    ax.hist(DF.search_cost, bins=36, color=GRAY['g3'], edgecolor='#000', linewidth=0.4)
    ax.axvline(DF.search_cost.mean(), color='#000', ls='--', lw=1.2)
    ax.annotate(f'均值 {DF.search_cost.mean():.0f} 元',
                (DF.search_cost.mean() * 1.05, ax.get_ylim()[1] * 0.9), fontsize=7.6)
    ax.set_xlabel('求职直接成本（元）')
    ax.set_ylabel('人数')
    grid_y(ax)
    panel_label(ax, '（a）')
    ax = axes[1]
    groups = [DF[DF.prov == p].search_months for p in ('js', 'zj', 'sh', 'ah')]
    bp = ax.boxplot(groups, tick_labels=['江苏', '浙江', '上海', '安徽'], widths=0.5,
                    patch_artist=True, medianprops=dict(color='#000', lw=1.3),
                    flierprops=dict(marker='.', markersize=2, markerfacecolor='#666'))
    for b in bp['boxes']:
        b.set(facecolor='#DDDDDD', edgecolor='#000', linewidth=0.8)
    ax.set_ylabel('求职周期（月）')
    grid_y(ax)
    panel_label(ax, '（b）')
    fig.tight_layout()
    save(fig, f'{FIG}/fig4_2.png')


# ---------------------------------------------------------------- 图4.4 备考比例
def fig4_4():
    fig, axes = plt.subplots(1, 2, figsize=(6.0, 2.6))
    ax = axes[0]
    provs = [('js', '江苏'), ('zj', '浙江'), ('sh', '上海'), ('ah', '安徽')]
    vals = [DF[DF.prov == k].civil_exam.mean() * 100 for k, _ in provs]
    for i, ((k, nm), v) in enumerate(zip(provs, vals)):
        ax.bar(nm, v, width=0.58, **bar_kw(i))
        ax.annotate(f'{v:.1f}', (i, v), textcoords='offset points', xytext=(0, 2.5),
                    ha='center', fontsize=7.5)
    ax.set_ylabel('备考比例（%）')
    ax.set_ylim(0, max(vals) * 1.2)
    grid_y(ax)
    panel_label(ax, '（a）分省份')
    ax = axes[1]
    tiers = ['双一流', '普通本科', '高职高专']
    vals = [DF[DF.tier == i].civil_exam.mean() * 100 for i in range(3)]
    for i, (nm, v) in enumerate(zip(tiers, vals)):
        ax.bar(nm, v, width=0.58, **bar_kw(i))
        ax.annotate(f'{v:.1f}', (i, v), textcoords='offset points', xytext=(0, 2.5),
                    ha='center', fontsize=7.5)
    ax.set_ylabel('备考比例（%）')
    ax.set_ylim(0, max(vals) * 1.2)
    grid_y(ax)
    panel_label(ax, '（b）分院校层次')
    fig.tight_layout()
    save(fig, f'{FIG}/fig4_4.png')


# ---------------------------------------------------------------- 图5.1 起薪
def fig5_1():
    emp = DF[DF.employed == 1]
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 2.8))
    ax = axes[0]
    for (lab, sub), ln in zip(
            [('本科', emp[emp.degree == 1]), ('专科', emp[emp.degree == 0]),
             ('硕士及以上', emp[emp.degree == 2])], LINES):
        xs = np.linspace(2500, 14000, 300)
        kde = np.zeros_like(xs)
        w = sub.wage.dropna().to_numpy()
        h = 1.06 * w.std() * len(w) ** -0.2
        for x in w[:1500]:
            kde += np.exp(-0.5 * ((xs - x) / h) ** 2)
        kde /= (len(w[:1500]) * h * np.sqrt(2 * np.pi))
        ax.plot(xs, kde * 1e4, label=lab, color=ln['color'], ls=ln['ls'], lw=1.4)
    ax.set_xlabel('月起薪（元）')
    ax.set_ylabel('密度（每万元）')
    ax.legend()
    grid_y(ax)
    panel_label(ax, '（a）分学历核密度')
    ax = axes[1]
    provs = [('js', '江苏'), ('zj', '浙江'), ('sh', '上海'), ('ah', '安徽')]
    vals = [R['quality'][f'wage_{k}'] for k, _ in provs]
    for i, ((k, nm), v) in enumerate(zip(provs, vals)):
        ax.bar(nm, v, width=0.58, **bar_kw(i))
        ax.annotate(f'{v:.0f}', (i, v), textcoords='offset points', xytext=(0, 2.5),
                    ha='center', fontsize=7.4)
    ax.set_ylabel('平均起薪（元/月）')
    ax.set_ylim(0, max(vals) * 1.17)
    grid_y(ax)
    panel_label(ax, '（b）分省份均值')
    fig.tight_layout()
    save(fig, f'{FIG}/fig5_1.png')


# ---------------------------------------------------------------- 图5.2 质量雷达
def fig5_2():
    emp = DF[DF.employed == 1]
    dims = ['工资水平', '专业匹配', '合同签订', '社会保险', '岗位稳定']
    ang = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
    ang += ang[:1]
    fig, ax = plt.subplots(figsize=(4.1, 3.6), subplot_kw=dict(polar=True))
    for (pk, nm), ln in zip([('js', '江苏'), ('zj', '浙江'), ('sh', '上海'), ('ah', '安徽')],
                            LINES):
        s = emp[emp.prov == pk]
        wp = (s.wage.mean() - 4500) / (7500 - 4500)
        vals = [np.clip(wp, 0, 1), s.match.mean(), s.contract.mean(),
                s.insurance.mean(), 1 - s.quit_intent.mean()]
        vals += vals[:1]
        ax.plot(ang, vals, label=nm, color=ln['color'], ls=ln['ls'],
                marker=ln['marker'], ms=3, lw=1.2)
    ax.set_xticks(ang[:-1])
    ax.set_xticklabels(dims, fontsize=8)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['0.25', '0.50', '0.75', '1.00'], fontsize=6.5)
    ax.grid(color='#AAAAAA', alpha=0.4, lw=0.5)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=4, fontsize=7.5)
    fig.tight_layout()
    save(fig, f'{FIG}/fig5_2.png')


# ---------------------------------------------------------------- 图5.3 匹配与离职
def fig5_3():
    emp = DF[DF.employed == 1]
    m = [emp[emp.major == i].match.mean() * 100 for i in range(6)]
    q = [emp[emp.major == i].quit_intent.mean() * 100 for i in range(6)]
    x = np.arange(6)
    fig, ax = plt.subplots(figsize=(5.8, 2.9))
    ax.bar(x, m, width=0.52, label='专业相关度（左轴）', **bar_kw(0))
    ax.set_ylabel('专业相关度（%）')
    ax.set_ylim(0, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(MAJORS, fontsize=7.6)
    grid_y(ax)
    ax2 = ax.twinx()
    ax2.spines['right'].set_visible(True)
    ax2.plot(x, q, label='一年内离职意向（右轴）', **LINES[1], lw=1.4)
    ax2.set_ylabel('一年内离职意向（%）')
    ax2.set_ylim(0, max(q) * 1.5)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    fig.legend(h1 + h2, l1 + l2, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.10))
    fig.tight_layout()
    save(fig, f'{FIG}/fig5_3.png')


# ---------------------------------------------------------------- 图6.1 满意度结构
def fig6_1():
    fig, axes = plt.subplots(1, 2, figsize=(6.0, 2.7))
    ax = axes[0]
    dims = [('收入报酬', R['satisfaction']['pay']), ('发展前景', R['satisfaction']['dev']),
            ('工作环境', R['satisfaction']['env']), ('总体', R['satisfaction']['overall'])]
    for i, (nm, v) in enumerate(dims):
        ax.bar(nm, v, width=0.56, **bar_kw(i))
        ax.annotate(f'{v:.2f}', (i, v), textcoords='offset points', xytext=(0, 2.5),
                    ha='center', fontsize=7.6)
    ax.set_ylabel('满意度（1—5分）')
    ax.set_ylim(0, 5)
    grid_y(ax)
    panel_label(ax, '（a）分维度均值')
    ax = axes[1]
    ax.hist(DF.sat_overall, bins=25, color=GRAY['g3'], edgecolor='#000', linewidth=0.4)
    ax.axvline(DF.sat_overall.mean(), color='#000', ls='--', lw=1.2)
    ax.set_xlabel('总体满意度（1—5分）')
    ax.set_ylabel('人数')
    grid_y(ax)
    panel_label(ax, '（b）总体分布')
    fig.tight_layout()
    save(fig, f'{FIG}/fig6_1.png')


# ---------------------------------------------------------------- 图6.2 期望落差
def fig6_2():
    g = DF.exp_gap * 100
    fig, ax = plt.subplots(figsize=(5.4, 2.9))
    ax.hist(g, bins=40, color=GRAY['g3'], edgecolor='#000', linewidth=0.4)
    ax.axvline(0, color='#000', lw=1.0)
    ax.axvline(g.mean(), color='#000', ls='--', lw=1.3)
    ax.annotate(f'均值 {g.mean():.1f}', (g.mean() + 2, ax.get_ylim()[1] * 0.92), fontsize=7.8)
    share = (g > 10).mean() * 100
    ax.annotate(f'落差超过10个对数点：{share:.1f}%', (32, ax.get_ylim()[1] * 0.70),
                fontsize=7.8)
    ax.set_xlabel('期望—实际起薪落差（对数点×100）')
    ax.set_ylabel('人数')
    grid_y(ax)
    fig.tight_layout()
    save(fig, f'{FIG}/fig6_2.png')


if __name__ == '__main__':
    for f in (fig3_1, fig3_2, fig3_3, fig3_4, fig4_1, fig4_2, fig4_4,
              fig5_1, fig5_2, fig5_3, fig6_1, fig6_2):
        f()
