# -*- coding: utf-8 -*-
import numpy as np, matplotlib.pyplot as plt
from figstyle import *

# ============ 图3-1 真实性维度落地路径：从本土文脉到地方认同 ============
fig = plt.figure(figsize=(6.2, 2.9))
ax = blank_ax(fig)
steps = [
    (0.135, '在地文脉', '大运河文化\n嘉禾稻作记忆\n蓝印花布·硖石灯彩'),
    (0.385, '空间转译', '“禾风九巷”街区命名\n“嘉禾印象”景观装置\n本地青砖·夯土·手工铁艺'),
    (0.635, '业态聚合', '“嘉味市集”本土优先\n老字号与非遗手作\n12组本土音乐人驻场'),
    (0.885, '社群联结', '公共空间免费开放\n摄影协会·亲子读书会\n季度居民议事会'),
]
for x, h, d in steps:
    box(ax, x, 0.735, 0.215, 0.115, h, fc=C['dark'], ec=C['dark'], color='white', fs=9.0, lw=1.0)
    box(ax, x, 0.435, 0.215, 0.245, d, fc='white', ec=C['mid'], lw=0.9, fs=7.8)
for x0 in (0.135, 0.385, 0.635):
    arrow(ax, (x0 + 0.112, 0.735), (x0 + 0.138, 0.735), ec=C['gray'], lw=1.1, ms=8)
box(ax, 0.5, 0.135, 0.90, 0.135, '地方认同的沉淀：68%受访者可说出巷道命名来源  ·  核心客群月均到访3.7次  ·  “非来不可”的差异化身份',
    fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.2)
for x, _, _ in steps:
    arrow(ax, (x, 0.312), (x, 0.205), ec=C['gray2'], lw=0.9, ms=7)
save(fig, 'fig3-1')

# ============ 图3-2 在地文化的三层转译机制 ============
fig = plt.figure(figsize=(6.0, 2.6))
ax = blank_ax(fig)
ax.text(0.5, 0.955, '抽象文化资源  →  可感知的场景语言', ha='center', fontsize=9.2,
        fontweight='bold', color=C['dark'])
lv = [
    (0.175, '叙事层', '巷道命名与尺度控制\n老照片、招牌复制品\n青石板与老砖混铺'),
    (0.500, '符号层', '“嘉禾印象”稻穗垂吊\n蓝印花布纹样导视\n硖石灯彩拱形座椅'),
    (0.825, '物质层', '本地石材与青砖\n江南夯土质感涂料\n本地匠人手工铁艺'),
]
for x, h, d in lv:
    box(ax, x, 0.665, 0.27, 0.115, h, fc=C['pale'], ec=C['dark'], lw=1.0, fs=9.0)
    box(ax, x, 0.355, 0.27, 0.245, d, fc='white', ec=C['mid'], lw=0.9, fs=7.8)
    arrow(ax, (x, 0.605), (x, 0.482), ec=C['gray2'], lw=0.9, ms=7)
ax.annotate('', xy=(0.955, 0.115), xytext=(0.045, 0.115),
            arrowprops=dict(arrowstyle='-|>', color=C['gray'], lw=1.1, mutation_scale=10))
ax.text(0.5, 0.062, '心理距离缩短  →  意义感注入  →  不可复制的场域气质', ha='center',
        fontsize=8.4, color=C['gray'])
save(fig, 'fig3-2')

# ============ 图3-5 三级演艺内容体系 ============
fig = plt.figure(figsize=(6.0, 3.0))
ax = blank_ax(fig)
rows = [
    (0.795, '节庆爆发层', '“万安夏夜音乐节”、机器人巡游、多巴胺市集', '年度峰值  ·  引爆声量', SEQ[0], 'white'),
    (0.520, '主题专场层', '“运河边的歌”独立音乐人限时创作专场', '季度稀缺  ·  强化认同', SEQ[1], 'white'),
    (0.245, '日常驻演层', '“民谣集·烧烤酒馆”每晚约3小时驻场演出', '每日常态  ·  培育习惯', SEQ[3], C['ink']),
]
for y, h, d, r, fc, tc in rows:
    box(ax, 0.30, y, 0.30, 0.155, h, fc=fc, ec=C['dark'], color=tc, fs=9.2, lw=1.0)
    box(ax, 0.625, y, 0.355, 0.155, d, fc='white', ec=C['mid'], lw=0.9, fs=7.8)
    ax.text(0.885, y, wrap_cn(r.replace('  ·  ', '\n'), 6), ha='center', va='center',
            fontsize=7.6, color=C['gray'])
ax.annotate('', xy=(0.10, 0.875), xytext=(0.10, 0.165),
            arrowprops=dict(arrowstyle='-|>', color=C['dark'], lw=1.3, mutation_scale=12))
ax.text(0.062, 0.52, '内容强度递增\n频次递减', rotation=90, ha='center', va='center',
        fontsize=8.2, color=C['dark'])
ax.text(0.5, 0.055, '常态化 + 稀缺性 + 峰值感 → “随时有音乐”的夜间心智占位',
        ha='center', fontsize=8.4, color=C['gray'])
save(fig, 'fig3-5')

# ============ 图3-6 节律驱动三层叠加模型 ============
fig = plt.figure(figsize=(6.0, 2.9))
ax = blank_ax(fig)
lay = [(0.755, '商业节点层', '开业庆典·店庆·大促', '集中造势、引爆客流'),
       (0.500, '节庆主题层', '国庆·元旦·暑期夜经济', '周期主题、吸引复访'),
       (0.245, '日常驻场层', '民谣驻演·裸眼3D·周末市集', '培育习惯、形成基础蜂鸣')]
for y, h, d, f in lay:
    box(ax, 0.245, y, 0.26, 0.145, h, fc=C['dark'], ec=C['dark'], color='white', fs=9.0, lw=1.0)
    box(ax, 0.545, y, 0.30, 0.145, d, fc='white', ec=C['mid'], lw=0.9, fs=8.0)
    box(ax, 0.855, y, 0.26, 0.145, f, fc=C['pale'], ec=C['mid'], lw=0.9, fs=8.0)
ax.text(0.245, 0.905, '节律层级', ha='center', fontsize=8.6, fontweight='bold', color=C['dark'])
ax.text(0.545, 0.905, '代表性活动', ha='center', fontsize=8.6, fontweight='bold', color=C['dark'])
ax.text(0.855, 0.905, '功能定位', ha='center', fontsize=8.6, fontweight='bold', color=C['dark'])
ax.plot([0.10, 0.99], [0.862, 0.862], color=C['gray2'], lw=0.8)
ax.annotate('', xy=(0.055, 0.825), xytext=(0.055, 0.175),
            arrowprops=dict(arrowstyle='<|-', color=C['gray'], lw=1.2, mutation_scale=11))
ax.text(0.028, 0.50, '时间尺度放大', rotation=90, ha='center', va='center', fontsize=8.0, color=C['gray'])
ax.text(0.5, 0.06, '“到点即去”的心理预判：把偶发消费重构为周期性复访', ha='center',
        fontsize=8.4, color=C['gray'])
save(fig, 'fig3-6')

# ============ 图3-7 青年业态板块及其运营表现 ============
fig, ax = plt.subplots(figsize=(5.9, 3.0))
lab = ['潮玩集合\n（超盒算NB）', '娱乐社交\n（健身·KTV·电竞）', '商务社交\n（萬匯空间）']
v1 = [800, 0, 0]
x = np.arange(3)
ind = [45.0, 98.0, 0]
b = ax.bar(x - 0.19, [45.0, 20.0, 12.0], 0.36, color=SEQ[1], edgecolor=C['dark'], lw=0.5,
           label='品类销售额占门店营收比重（%）', zorder=3)
b2 = ax.bar(x + 0.19, [62.0, 98.0, 55.0], 0.36, color=SEQ[3], edgecolor=C['dark'], lw=0.5,
            label='周末时段预订／到店率（%）', zorder=3)
for rr in (b, b2):
    for p in rr:
        ax.text(p.get_x() + p.get_width() / 2, p.get_height() + 1.2, '%.0f' % p.get_height(),
                ha='center', va='bottom', fontsize=7.8, color=C['ink'])
ax.set_xticks(x); ax.set_xticklabels(lab)
ax.set_ylabel('比重（%）'); ax.set_ylim(0, 115)
ax.legend(loc='upper left', ncol=1); tidy(ax)
note(ax, '数据来源：万安广场运营方开业首月经营统计与本研究实地访谈整理。', y=-0.20)
save(fig, 'fig3-7')

# ============ 图3-8 两类圈层运营模式的效果对比 ============
fig, ax = plt.subplots(figsize=(5.9, 2.9))
idx = ['单场参与人次\n（百人）', '新客占比\n（%）', '社媒自发笔记\n（十篇）', '话题阅读量\n（十万次）']
a = [4.0, 60.0, 20.0, 1.2]
b_ = [20.0, 42.0, 34.0, 5.0]
y = np.arange(len(idx)); h = 0.34
r1 = ax.barh(y + h / 2, a, h, color=SEQ[0], edgecolor=C['dark'], lw=0.5, label='圈层主导型（二次元主题日）', zorder=3)
r2 = ax.barh(y - h / 2, b_, h, color=SEQ[2], edgecolor=C['dark'], lw=0.5, label='主题场景型（城市露营节）', zorder=3)
for rr in (r1, r2):
    for p in rr:
        ax.text(p.get_width() + 0.9, p.get_y() + p.get_height() / 2, '%.1f' % p.get_width(),
                va='center', fontsize=7.8, color=C['ink'])
ax.set_yticks(y); ax.set_yticklabels(idx); ax.invert_yaxis()
ax.set_xlabel('指标值（按标注量纲折算）'); ax.set_xlim(0, 72)
ax.legend(loc='lower right'); tidy(ax, grid='x')
note(ax, '注：为便于同图比较，各指标已按括号内量纲折算；数据来源于广场运营方活动复盘资料。', y=-0.24)
save(fig, 'fig3-8')

# ============ 图3-9 客源地结构变化 ============
fig, ax = plt.subplots(figsize=(5.4, 2.5))
per = ['开业初期', '开业三个月后']
seg = ['南湖区及市区', '嘉兴下辖县域', '市域外及跨省']
d = np.array([[81.0, 12.0, 7.0], [68.0, 22.0, 10.0]])
left = np.zeros(2)
for j, s in enumerate(seg):
    ax.barh(per, d[:, j], left=left, height=0.45, color=SEQ[j], edgecolor='white', lw=0.8, label=s, zorder=3)
    for i in range(2):
        ax.text(left[i] + d[i, j] / 2, i, '%.0f%%' % d[i, j], ha='center', va='center',
                fontsize=8.0, color='white' if j < 2 else C['ink'])
    left += d[:, j]
ax.set_xlim(0, 100); ax.set_xlabel('客源地构成占比（%）')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.30), ncol=3, fontsize=8.0)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
note(ax, '数据来源：万安广场消费者到访调研（开业首月与开业第三个月两轮）。', y=-0.62)
save(fig, 'fig3-9')

# ============ 图3-10 品牌建设完整闭环 ============
fig = plt.figure(figsize=(5.3, 3.3))
ax = blank_ax(fig)
cx, cy, r = 0.5, 0.50, 0.235
box(ax, cx, cy, 0.24, 0.13, '品牌即城市名片', fc=C['dark'], ec=C['dark'], color='white', fs=9.2, lw=1.0)
nodes = [(cx, cy + r + 0.075, '识别体系\n（定义自身）'),
         (cx + r + 0.055, cy, '事件运营\n（嵌入城市）'),
         (cx, cy - r - 0.075, '区域辐射\n（价值外溢）'),
         (cx - r - 0.055, cy, '传播矩阵\n（放大声量）')]
for x, y, t in nodes:
    box(ax, x, y, 0.245, 0.125, t, fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.4)
th = np.linspace(0, 2 * np.pi, 400)
for k in range(4):
    a0 = np.pi / 2 - k * np.pi / 2
    a1 = a0 - np.pi / 2
    aa = np.linspace(a0 - 0.42, a1 + 0.42, 60)
    ax.plot(cx + 0.325 * np.cos(aa), cy + 0.325 * np.sin(aa), color=C['gray'], lw=1.0)
    ax.annotate('', xy=(cx + 0.325 * np.cos(aa[-1]), cy + 0.325 * np.sin(aa[-1])),
                xytext=(cx + 0.325 * np.cos(aa[-4]), cy + 0.325 * np.sin(aa[-4])),
                arrowprops=dict(arrowstyle='-|>', color=C['gray'], lw=1.0, mutation_scale=9))
ax.text(0.5, 0.035, '每一轮传播与辐射，都反向强化品牌识别体系与城市名片认知',
        ha='center', fontsize=8.0, color=C['gray'])
save(fig, 'fig3-10')

# ============ 图3-11 “嘉夜场景”三维联动模型 ============
fig = plt.figure(figsize=(6.0, 3.4))
ax = blank_ax(fig)
tri = [(0.19, 0.66, '真（真实性）\n在地文脉·舒适物聚合·社群共建', SEQ[0], 'white'),
       (0.81, 0.66, '美（戏剧性）\n演艺驻场·光影造景·节律驱动', SEQ[1], 'white'),
       (0.50, 0.20, '善（价值性）\n青年圈层·慢生活倡导·品牌铸魂', SEQ[2], C['ink'])]
for x, y, t, fc, tc in tri:
    box(ax, x, y, 0.345, 0.155, t, fc=fc, ec=C['dark'], color=tc, fs=8.4, lw=1.1)
box(ax, 0.50, 0.485, 0.22, 0.115, '蜂鸣\nBuzz', fc='white', ec=C['dark'], lw=1.2, fs=9.6, bold=True)
arrow(ax, (0.365, 0.66), (0.635, 0.66), ec=C['gray'], lw=1.1, rad=-0.22, ms=9)
arrow(ax, (0.735, 0.585), (0.585, 0.265), ec=C['gray'], lw=1.1, rad=-0.22, ms=9)
arrow(ax, (0.375, 0.245), (0.20, 0.578), ec=C['gray'], lw=1.1, rad=-0.22, ms=9)
ax.text(0.50, 0.775, '不可复制的内容底色', ha='center', fontsize=8.0, color=C['gray'])
ax.text(0.845, 0.395, '滋养并刺激', ha='center', fontsize=8.0, color=C['gray'], rotation=-62)
ax.text(0.155, 0.395, '口碑与消费回流', ha='center', fontsize=8.0, color=C['gray'], rotation=62)
box(ax, 0.50, 0.045, 0.86, 0.075, '真为根·美为形·善为魂：以景留人、因夜兴城的“嘉夜场景”路径',
    fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.4)
save(fig, 'fig3-11')
