# -*- coding: utf-8 -*-
import numpy as np, matplotlib.pyplot as plt
from figstyle import *

# ============ 图2-2 “钻石精神”企业文化内核 ============
fig = plt.figure(figsize=(5.9, 3.3))
ax = blank_ax(fig)
box(ax, 0.5, 0.80, 0.30, 0.145, '核心价值观\n如钻石般坚守品质·追求卓越·创造价值',
    fc=C['dark'], ec=C['dark'], fs=8.4, color='white', lw=1.0)
box(ax, 0.20, 0.52, 0.30, 0.13, '企业精神\n开拓·求实·高效·创新', fc=C['pale'], ec=C['dark'], fs=8.4)
box(ax, 0.80, 0.52, 0.30, 0.13, '服务理念\n品质·生活·享受', fc=C['pale'], ec=C['dark'], fs=8.4)
arrow(ax, (0.42, 0.735), (0.27, 0.60), ec=C['gray'], lw=1.0)
arrow(ax, (0.58, 0.735), (0.73, 0.60), ec=C['gray'], lw=1.0)
pil = [('品质\n立业之本', 0.14), ('创新\n发展之源', 0.38), ('服务\n价值体现', 0.62), ('责任\n国企担当', 0.86)]
for t, x in pil:
    box(ax, x, 0.235, 0.20, 0.135, t, fc='white', ec=C['mid'], lw=0.9, fs=8.2)
    arrow(ax, (x, 0.44), (x, 0.315), ec=C['gray2'], lw=0.9, ms=7)
ax.plot([0.20, 0.80], [0.44, 0.44], color=C['gray2'], lw=0.9)
ax.plot([0.20, 0.20], [0.455, 0.44], color=C['gray2'], lw=0.9)
ax.plot([0.80, 0.80], [0.455, 0.44], color=C['gray2'], lw=0.9)
box(ax, 0.5, 0.075, 0.80, 0.075, '文化理念驱动商业转型：由商品经营向生活方式服务、由空间提供向场景运营延伸',
    fc='white', ec=C['dark'], lw=1.0, fs=8.2)
for x in pil:
    pass
arrow(ax, (0.5, 0.165), (0.5, 0.115), ec=C['gray'], lw=1.0, ms=7)
save(fig, 'fig2-2')

# ============ 图2-3 发展历程与能力跃升 ============
fig = plt.figure(figsize=(6.3, 3.0))
ax = blank_ax(fig)
ax.annotate('', xy=(0.975, 0.50), xytext=(0.035, 0.50),
            arrowprops=dict(arrowstyle='-|>', color=C['dark'], lw=1.4, mutation_scale=13))
st = [
    (0.165, '1999—2009', '筑基零售\n铸就商誉', '购物中心成立并落位核心商圈\n集团化整合，跻身市十强商贸企业'),
    (0.395, '2010—2019', '革新业态\n蝶变跃升', '改造纳入市“三个千亿”工程\n营业面积1.8万㎡扩至近4万㎡'),
    (0.625, '2020—2024', '焕新空间\n拓展场景', '建成嘉兴首块裸眼3D大屏\n夜市、后备箱集市等运营试水'),
    (0.855, '2025—至今', '布局夜间\n开启新篇', '万安广场启幕，体量近8万㎡\n“商业+文化+休闲+社交”融合'),
]
for x, yr, tt, dd in st:
    ax.plot([x], [0.50], marker='o', ms=7, color=C['dark'], markerfacecolor='white', mew=1.4, zorder=5)
    box(ax, x, 0.735, 0.205, 0.155, tt, fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.6)
    ax.text(x, 0.585, yr, ha='center', va='center', fontsize=8.6, fontweight='bold', color=C['dark'])
    ax.plot([x, x], [0.515, 0.655], color=C['gray2'], lw=0.8)
    box(ax, x, 0.245, 0.215, 0.185, wrap_cn(dd, 11), fc='white', ec=C['mid'], lw=0.8, fs=7.3)
    ax.plot([x, x], [0.485, 0.34], color=C['gray2'], lw=0.8)
ax.text(0.035, 0.42, '能力主线：商品经营 → 空间运营 → 内容运营 → 场景运营',
        fontsize=8.2, color=C['gray'], ha='left')
save(fig, 'fig2-3')

# ============ 图2-4 2024年嘉兴市消费市场结构与增速 ============
fig, ax = plt.subplots(figsize=(5.6, 3.1))
lab = ['社会消费品零售总额', '其中：商品零售', '其中：餐饮收入']
val = [2647.4, 2464.1, 183.3]
gr = [5.3, 5.1, 8.0]
x = np.arange(3)
b = ax.bar(x, val, width=0.46, color=[SEQ[0], SEQ[1], SEQ[2]], edgecolor=C['dark'], lw=0.6, zorder=3)
for r, v in zip(b, val):
    ax.text(r.get_x() + r.get_width() / 2, v + 45, '%.1f' % v, ha='center', va='bottom', fontsize=8.2, color=C['ink'])
ax.set_xticks(x); ax.set_xticklabels(lab)
ax.set_ylabel('绝对额（亿元）'); ax.set_ylim(0, 3050)
tidy(ax)
ax2 = ax.twinx()
ax2.plot(x, gr, ls='none', marker='D', ms=6, color=C['accent'], zorder=6, label='同比增速（%）')
for xx, g in zip(x, gr):
    ax2.annotate('%.1f%%' % g, (xx, g), textcoords='offset points', xytext=(0, 8),
                 ha='center', fontsize=8.2, color=C['accent'])
ax2.set_ylabel('同比增速（%）', color=C['accent'], labelpad=2); ax2.set_ylim(0, 11)
ax2.tick_params(axis='y', colors=C['accent']); ax2.spines['top'].set_visible(False)
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h2, l2, loc='upper center', bbox_to_anchor=(0.62, 1.0))
note(ax, '数据来源：嘉兴市统计局《2024年嘉兴市国民经济和社会发展统计公报》。', y=-0.17)
save(fig, 'fig2-4')

# ============ 图2-5 案例典型性的三重维度 ============
fig = plt.figure(figsize=(6.1, 2.7))
ax = blank_ax(fig)
box(ax, 0.5, 0.88, 0.44, 0.14, '典型样本价值\n国资属性·文化禀赋·区域普适', fc=C['dark'], ec=C['dark'],
    color='white', fs=8.8, lw=1.0)
tri = [
    (0.175, '国资担当的稀缺性', '重资产投入与长期场景运营\n经营价值向城市消费价值延伸\n“稳消费、兴城市”的公共路径'),
    (0.500, '文商融合的独特禀赋', '江南嘉禾文脉为底蕴\n叠加民谣演艺与特色市集\n差异化、高辨识度的场景范式'),
    (0.825, '中等体量的示范价值', '约8万㎡体量与中等城市禀赋\n盘活存量、内生驱动\n与数百个同级城市高度契合'),
]
for x, h, d in tri:
    box(ax, x, 0.535, 0.29, 0.12, h, fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.6)
    box(ax, x, 0.215, 0.29, 0.245, d, fc='white', ec=C['mid'], lw=0.8, fs=7.6)
    arrow(ax, (0.5, 0.805), (x, 0.605), ec=C['gray'], lw=1.0, ms=7)
    arrow(ax, (x, 0.472), (x, 0.345), ec=C['gray2'], lw=0.9, ms=6)
save(fig, 'fig2-5')
