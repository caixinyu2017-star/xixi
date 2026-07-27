# -*- coding: utf-8 -*-
import numpy as np, matplotlib.pyplot as plt
from figstyle import *

# ============ 图1-1 研究背景三层递进逻辑图 ============
fig = plt.figure(figsize=(6.1, 3.5))
ax = blank_ax(fig)
rows = [
    (0.855, '国家战略层  扩大内需·提振消费',
     '二十届三中全会《决定》：健全扩大消费长效机制\n国办发〔2023〕26号：打造消费新场景，培育多层级消费中心'),
    (0.585, '行业机遇层  夜间经济提质升级',
     '业态形态由“地摊夜市”向“演艺+商圈”“夜间文旅集聚区”跃迁\n二三线城市普遍面临“有夜无景、有流无留”的结构性困境'),
    (0.315, '企业实践层  地方国企场景运营',
     '嘉兴市戴梦得商贸集团重资产投入与长期场景运营\n以万安广场为载体探索“商业+文化+休闲+社交”融合路径'),
]
for y, t1, t2 in rows:
    box(ax, 0.5, y, 0.86, 0.185, '', fc='white', ec=C['dark'], lw=1.1)
    ax.text(0.5, y + 0.048, t1, ha='center', va='center', fontsize=9.6, fontweight='bold', color=C['dark'])
    ax.plot([0.13, 0.87], [y + 0.018, y + 0.018], color=C['gray2'], lw=0.7)
    ax.text(0.5, y - 0.043, t2, ha='center', va='center', fontsize=8.0, color=C['ink'], linespacing=1.6)
for y in (0.762, 0.492):
    arrow(ax, (0.5, y), (0.5, y - 0.077), ec=C['gray'], lw=1.1)
arrow(ax, (0.5, 0.222), (0.5, 0.145), ec=C['gray'], lw=1.1)
box(ax, 0.5, 0.082, 0.62, 0.115, '核心研究问题\n二三线城市地方国企如何通过“场景营造”驱动夜间消费升级',
    fc=C['pale'], ec=C['dark'], lw=1.2, fs=8.8, bold=False)
save(fig, 'fig1-1')

# ============ 图1-2 全国Livehouse演出场次与票房规模 ============
yr = ['2019', '2020', '2021', '2022', '2023', '2024']
cs = [2.5, 0.8, 1.2, 1.0, 5.5, 6.5]      # 万场
pf = [12.0, 3.5, 5.0, 4.5, 35.0, 40.0]   # 亿元
fig, ax = plt.subplots(figsize=(5.9, 3.1))
b = ax.bar(yr, cs, width=0.5, color=SEQ[1], edgecolor=C['dark'], linewidth=0.6,
           label='演出场次（万场）', zorder=3)
ax.set_ylabel('演出场次（万场）'); ax.set_ylim(0, 8)
tidy(ax)
for r, v in zip(b, cs):
    ax.text(r.get_x() + r.get_width() / 2, v + 0.15, '%.1f' % v, ha='center', va='bottom', fontsize=8, color=C['dark'])
ax2 = ax.twinx()
ax2.plot(yr, pf, marker='o', ms=4.5, color=C['ink'], lw=1.3, label='票房规模（亿元）', zorder=4,
         markerfacecolor='white', markeredgewidth=1.1)
ax2.set_ylabel('票房规模（亿元）'); ax2.set_ylim(0, 48)
ax2.spines['top'].set_visible(False)
for x, v in zip(yr, pf):
    ax2.annotate('%.0f' % v, (x, v), textcoords='offset points', xytext=(0, 7),
                 ha='center', fontsize=8, color=C['ink'])
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc='upper left', ncol=1, fontsize=8.2)
note(ax, '数据来源：中国演出行业协会历年《全国演出市场年度报告》。', y=-0.155)
save(fig, 'fig1-2')

# ============ 图1-3 一线与二三线城市夜间消费业态结构对比 ============
cats = ['餐饮宵夜', '购物零售', '文化演艺', '休闲娱乐', '夜游观光']
a = [31.5, 25.8, 18.2, 16.4, 8.1]
b_ = [45.6, 29.7, 6.8, 12.4, 5.5]
x = np.arange(len(cats)); w = 0.36
fig, ax = plt.subplots(figsize=(5.9, 3.0))
r1 = ax.bar(x - w / 2, a, w, color=SEQ[0], edgecolor=C['dark'], lw=0.5, label='一线及新一线城市', zorder=3)
r2 = ax.bar(x + w / 2, b_, w, color=SEQ[2], edgecolor=C['dark'], lw=0.5, label='二三线城市', zorder=3)
for rr in (r1, r2):
    for p in rr:
        ax.text(p.get_x() + p.get_width() / 2, p.get_height() + 0.6, '%.1f' % p.get_height(),
                ha='center', va='bottom', fontsize=7.6, color=C['ink'])
ax.set_xticks(x); ax.set_xticklabels(cats)
ax.set_ylabel('夜间消费支出结构占比（%）'); ax.set_ylim(0, 52)
ax.legend(loc='upper right'); tidy(ax)
note(ax, '数据来源：根据中国旅游研究院《2024中国夜间经济发展报告》与艾媒咨询相关调研数据整理测算。', y=-0.16)
save(fig, 'fig1-3')

# ============ 图1-4 场景五要素与“真·美·善”三维分析框架映射 ============
fig = plt.figure(figsize=(6.2, 3.6))
ax = blank_ax(fig)
ax.text(0.19, 0.955, '场景五大构成要素', ha='center', fontsize=9.4, fontweight='bold', color=C['dark'])
ax.text(0.585, 0.955, '文化意义三维度', ha='center', fontsize=9.4, fontweight='bold', color=C['dark'])
ax.text(0.885, 0.955, '消费转化环节', ha='center', fontsize=9.4, fontweight='bold', color=C['dark'])
els = ['邻里（在地空间载体）', '物质设施（舒适物）', '多样人群（主体构成）',
       '活动（演艺·市集·展览）', '价值观（生活理念）']
ys = np.linspace(0.80, 0.16, 5)
for y, t in zip(ys, els):
    box(ax, 0.19, y, 0.33, 0.105, t, fc='white', ec=C['mid'], lw=0.9, fs=8.0)
dims = [(0.755, '真实性（真）\n本源之根·文脉铸真', 0.20),
        (0.485, '戏剧性（美）\n表征之形·演艺塑形', 0.20),
        (0.215, '价值性（善）\n价值之魂·价值润心', 0.20)]
for y, t, h in dims:
    box(ax, 0.585, y, 0.29, 0.155, t, fc=C['pale'], ec=C['dark'], lw=1.1, fs=8.4)
conv = [(0.755, '引流·聚流\n（本源吸引力）'), (0.485, '留客·留量\n（停留与黏性）'),
        (0.215, '增量·反哺\n（复购与品牌资产）')]
for y, t in conv:
    box(ax, 0.885, y, 0.20, 0.135, t, fc='white', ec=C['mid'], lw=0.9, fs=8.0)
link = {0: [0], 1: [0, 1], 2: [0, 2], 3: [1], 4: [2]}
for i, js in link.items():
    for j in js:
        arrow(ax, (0.355, ys[i]), (0.44, dims[j][0]), ec=C['gray2'], lw=0.8, ms=6)
for y, _, _ in dims:
    arrow(ax, (0.73, y), (0.785, y), ec=C['gray'], lw=1.0, ms=7)
arrow(ax, (0.885, 0.148), (0.585, 0.06), ec=C['gray'], lw=0.9, ls='--', rad=0.18, ms=7)
arrow(ax, (0.585, 0.06), (0.585, 0.135), ec=C['gray'], lw=0.9, ls='--', ms=7)
ax.text(0.735, 0.045, '增量反哺', fontsize=7.6, color=C['gray'], ha='center')
save(fig, 'fig1-4')

# ============ 图1-5 技术路线图 ============
fig = plt.figure(figsize=(6.2, 4.5))
ax = blank_ax(fig)
stages = [('提出问题\n（第一章）', 0.905), ('案例分析\n（第二、三章）', 0.665),
          ('机理解析\n（第四章）', 0.415), ('总结启示\n（第五章）', 0.155)]
for t, y in stages:
    box(ax, 0.115, y, 0.175, 0.135, t, fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.4)
mids = [
    (0.905, '现实背景与政策牵引', ['扩大内需与消费提质', '夜间经济提质升级', '国企场景运营担当']),
    (0.665, '案例情境与实践呈现', ['企业概况与发展历程', '真：文脉铸真·在地筑景', '美：演艺塑形·沉浸活景', '善：价值润心·认同立景']),
    (0.415, '三维作用机理与闭环', ['真实性：本源吸引力', '戏剧性：流量向留量转化', '价值性：留量向增量跃升', '闭环：自强化“蜂鸣”循环']),
    (0.155, '“嘉夜场景”模式输出', ['理论贡献与实践启示', '可推广性与适配条件']),
]
for y, head, items in mids:
    n = len(items)
    w_item = 0.145 if n >= 4 else 0.185
    box(ax, 0.545, y + 0.055, 0.60, 0.058, head, fc=C['dark'], ec=C['dark'], lw=0.8, fs=8.6, color='white')
    xs = np.linspace(0.545 - (n - 1) * (w_item + 0.012) / 2, 0.545 + (n - 1) * (w_item + 0.012) / 2, n)
    for xx, it in zip(xs, items):
        box(ax, xx, y - 0.035, w_item, 0.085, wrap_cn(it, 7), fc='white', ec=C['mid'], lw=0.8, fs=7.0)
    arrow(ax, (0.205, y), (0.243, y), ec=C['gray'], lw=1.0, ms=7)
meth = [('文献研究法', 0.905), ('深度访谈法', 0.665), ('理论演绎法', 0.415), ('单案例研究法', 0.155)]
for t, y in meth:
    box(ax, 0.925, y, 0.135, 0.10, t, fc='white', ec=C['gray'], lw=0.9, ls='--', fs=8.0)
    arrow(ax, (0.848, y), (0.857, y), ec=C['gray2'], lw=0.8, ms=6)
for y0, y1 in [(0.905, 0.665), (0.665, 0.415), (0.415, 0.155)]:
    arrow(ax, (0.115, y0 - 0.068), (0.115, y1 + 0.068), ec=C['gray'], lw=1.1, ms=8)
save(fig, 'fig1-5')
