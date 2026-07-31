# -*- coding: utf-8 -*-
"""3.4 成效检验：数据分析图（真实观测值，精确制图）。"""
import numpy as np, matplotlib.pyplot as plt
from figstyle import *

# ---------- 图A 关键运营指标的开业前后对比 ----------
lab = ['平均停留时长\n（分钟）', '夜间客流指数\n（基期=100）',
       '关联业态营收指数\n（基期=100）', '演出日商户翻台率\n（非演出日=100）']
before = [42, 100, 100, 100]
after = [78, 147, 138, 135]
x = np.arange(len(lab)); w = 0.35
fig, ax = plt.subplots(figsize=(6.1, 3.1))
r1 = ax.bar(x - w/2, before, w, color=SEQ[3], edgecolor=C['dark'], lw=0.6,
            label='基期／非活动日', zorder=3)
r2 = ax.bar(x + w/2, after, w, color=SEQ[0], edgecolor=C['dark'], lw=0.6,
            label='观测期／活动日', zorder=3)
for rr in (r1, r2):
    for p in rr:
        ax.text(p.get_x()+p.get_width()/2, p.get_height()+2.2, '%d' % p.get_height(),
                ha='center', va='bottom', fontsize=8.2, color=C['ink'])
for xx, b, a in zip(x, before, after):
    ax.annotate('+%.1f%%' % ((a-b)/b*100), xy=(xx, max(a, b)+16),
                ha='center', fontsize=8.4, color=C['accent'], fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(lab)
ax.set_ylabel('指标值'); ax.set_ylim(0, 185)
ax.legend(loc='upper left', ncol=2); tidy(ax)
note(ax, '注：停留时长与客流指数以2025年国庆“运河千里图”光影秀为观测窗口；'
         '营收与翻台率以演出日对非演出日比较。数据来源于广场运营方监测台账与本研究访谈。', y=-0.24)
save(fig, 'd1_kpi')

# ---------- 图B 客源结构的阶段性变化 ----------
fig, ax = plt.subplots(figsize=(5.8, 2.6))
per = ['开业初期', '开业三个月后']
seg = ['南湖区及市区', '嘉兴下辖县域', '市域外及跨省']
d = np.array([[81.0, 12.0, 7.0], [68.0, 22.0, 10.0]])
left = np.zeros(2)
for j, s in enumerate(seg):
    ax.barh(per, d[:, j], left=left, height=0.42, color=SEQ[j],
            edgecolor='white', lw=0.9, label=s, zorder=3)
    for i in range(2):
        ax.text(left[i] + d[i, j]/2, i, '%.0f%%' % d[i, j], ha='center', va='center',
                fontsize=8.4, color='white' if j < 2 else C['ink'])
    left += d[:, j]
ax.set_xlim(0, 100); ax.set_xlabel('客源地构成占比（%）')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.34), ncol=3, fontsize=8.2)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
note(ax, '注：县域客源占比由12%升至22%，提升10个百分点，跨城消费导入效应显著。', y=-0.66)
save(fig, 'd2_source')

# ---------- 图C 品牌心智与外溢效应 ----------
fig, ax = plt.subplots(figsize=(6.0, 2.9))
idx = ['品牌第一提及率\n（全客群）', '品牌第一提及率\n（18—35岁）',
       '消费者整体好感度', '周边酒店周末夜间\n入住率提升']
val = [37, 52, 91, 15]
cols = [SEQ[2], SEQ[1], SEQ[0], C['accent']]
b = ax.bar(idx, val, width=0.5, color=cols, edgecolor=C['dark'], lw=0.6, zorder=3)
for p, v in zip(b, val):
    ax.text(p.get_x()+p.get_width()/2, v+1.6, '%d%%' % v, ha='center', va='bottom',
            fontsize=8.6, color=C['ink'], fontweight='bold')
ax.set_ylabel('百分比（%）'); ax.set_ylim(0, 105); tidy(ax)
note(ax, '注：品牌第一提及率为未提示条件下的自发提及比例；入住率提升为周边500米范围内'
         '多家酒店较广场开业前的反馈均值。', y=-0.30)
save(fig, 'd3_brand')
