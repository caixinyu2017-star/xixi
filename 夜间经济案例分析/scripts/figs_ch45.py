# -*- coding: utf-8 -*-
import numpy as np, matplotlib.pyplot as plt
from figstyle import *

# ============ 图4-1 本章分析框架 ============
fig = plt.figure(figsize=(6.2, 3.1))
ax = blank_ax(fig)
box(ax, 0.5, 0.935, 0.90, 0.085,
    '二三线城市夜间经济痛点：有夜无景、有流无留、只逛不买',
    fc='white', ec=C['dark'], lw=1.0, fs=8.6)
cols = [(0.185, '真实性机理', '在地文脉何以成为\n场景的“本源吸引力”',
         '文化转译\n舒适物聚合\n社区联结', '流量'),
        (0.500, '戏剧性机理', '演艺造境何以将\n“流量”转化为“留量”',
         '蜂鸣聚合\n五感沉浸\n节律复访', '留量'),
        (0.815, '价值性机理', '价值认同何以将\n“留量”转化为“增量”',
         '圈层共鸣\n意义生产\n口碑裂变', '增量')]
for x, h, q, m, o in cols:
    box(ax, x, 0.775, 0.28, 0.085, h, fc=C['dark'], ec=C['dark'], color='white', fs=9.0, lw=1.0)
    box(ax, x, 0.635, 0.28, 0.125, q, fc=C['pale'], ec=C['mid'], lw=0.9, fs=8.0)
    box(ax, x, 0.415, 0.28, 0.215, m, fc='white', ec=C['mid'], lw=0.9, fs=8.2)
    box(ax, x, 0.215, 0.15, 0.085, o, fc='white', ec=C['dark'], lw=1.1, fs=9.0, bold=True)
    arrow(ax, (0.5 if x == 0.5 else x, 0.892), (x, 0.822), ec=C['gray'], lw=0.9, ms=7)
    arrow(ax, (x, 0.572), (x, 0.525), ec=C['gray2'], lw=0.9, ms=6)
    arrow(ax, (x, 0.305), (x, 0.262), ec=C['gray2'], lw=0.9, ms=6)
for x0, x1 in [(0.185, 0.500), (0.500, 0.815)]:
    arrow(ax, (x0 + 0.078, 0.215), (x1 - 0.078, 0.215), ec=C['dark'], lw=1.1, ms=9)
arrow(ax, (0.815, 0.168), (0.185, 0.168), ec=C['gray'], lw=1.0, ls='--', rad=0.10, ms=8)
ax.text(0.5, 0.055, '第4.4节  闭环机理：三维耦合的自强化“蜂鸣”正循环', ha='center',
        fontsize=8.4, color=C['gray'])
save(fig, 'fig4-1')

# ============ 图4-2 注意力磁极的形成机制 ============
fig = plt.figure(figsize=(6.0, 2.7))
ax = blank_ax(fig)
box(ax, 0.5, 0.50, 0.22, 0.16, '注意力磁极\n高密度人气聚焦', fc=C['dark'], ec=C['dark'],
    color='white', fs=8.8, lw=1.1)
box(ax, 0.145, 0.735, 0.26, 0.19, '第一重刺激：舞台机制\n驻场乐队·免费点歌\n即兴互动·合唱直播',
    fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.0)
box(ax, 0.145, 0.265, 0.26, 0.19, '第二重刺激：三级内容体系\n日常驻演—主题专场—节庆爆发\n街头快闪·即兴弹唱',
    fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.0)
arrow(ax, (0.278, 0.700), (0.392, 0.560), ec=C['gray'], lw=1.1, ms=8)
arrow(ax, (0.278, 0.300), (0.392, 0.440), ec=C['gray'], lw=1.1, ms=8)
box(ax, 0.855, 0.735, 0.26, 0.19, '“看与被看”的戏剧张力\n观众既是观看者\n也是被观看的表演者',
    fc='white', ec=C['mid'], lw=0.9, fs=8.0)
box(ax, 0.855, 0.265, 0.26, 0.19, '破解“潮汐效应”\n空间自产新鲜内容\n关联业态营收同步抬升',
    fc='white', ec=C['mid'], lw=0.9, fs=8.0)
arrow(ax, (0.612, 0.560), (0.725, 0.700), ec=C['gray'], lw=1.1, ms=8)
arrow(ax, (0.612, 0.440), (0.725, 0.300), ec=C['gray'], lw=1.1, ms=8)
ax.text(0.5, 0.055, '过客 → 看客 → 顾客：注意力资源沉淀为消费行为', ha='center',
        fontsize=8.4, color=C['gray'])
save(fig, 'fig4-2')

# ============ 图4-3 五感沉浸与时间感知重塑 ============
fig = plt.figure(figsize=(6.1, 2.7))
ax = blank_ax(fig)
sens = [(0.115, '视觉', '星河步道互动光影\n运河水岸灯光秀\n裸眼3D大屏'),
        (0.345, '听觉', '驻场民谣乐队\n本土独立音乐人\n街头即兴弹唱'),
        (0.575, '味觉·嗅觉', '“嘉味市集”本地小吃\n老字号餐饮\n烟火气与食物香'),
        (0.805, '触觉·体感', '青砖夯土肌理\n非遗手作体验\n滨水微风与人群温度')]
for x, h, d in sens:
    box(ax, x, 0.775, 0.205, 0.10, h, fc=C['dark'], ec=C['dark'], color='white', fs=8.8, lw=1.0)
    box(ax, x, 0.545, 0.205, 0.215, d, fc='white', ec=C['mid'], lw=0.9, fs=7.6)
    arrow(ax, (x, 0.425), (x, 0.345), ec=C['gray2'], lw=0.9, ms=6)
box(ax, 0.5, 0.265, 0.86, 0.10, '沉浸度提升 → 时间感知钝化 → 停留时长延长（42分钟 → 78分钟）',
    fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.6)
arrow(ax, (0.5, 0.205), (0.5, 0.145), ec=C['gray'], lw=1.0, ms=7)
box(ax, 0.5, 0.075, 0.70, 0.095, '非计划性消费窗口扩大 → 客单价上限抬升 → 单客价值最大化',
    fc='white', ec=C['dark'], lw=1.0, fs=8.4)
save(fig, 'fig4-3')

# ============ 图4-4 节律复访的三重实施机制 ============
fig = plt.figure(figsize=(6.1, 2.6))
ax = blank_ax(fig)
mech = [(0.175, '时间驱动的\n逆向内容规划', '策划单元由“事件”\n置换为“时间”', '消除决策不确定性'),
        (0.500, '周期认知的\n制度化塑造', '固定时间坐标\n月度活动日历与开市仪式', '形成心智“时间地标”'),
        (0.825, '内容与商业的\n深度联动', '主题市集与商户促销同步\n借势外部赛事热点', '创造可预期客流波峰')]
for x, h, d, e in mech:
    box(ax, x, 0.775, 0.28, 0.145, h, fc=C['dark'], ec=C['dark'], color='white', fs=8.6, lw=1.0)
    box(ax, x, 0.505, 0.28, 0.185, d, fc='white', ec=C['mid'], lw=0.9, fs=7.8)
    box(ax, x, 0.265, 0.28, 0.115, e, fc=C['pale'], ec=C['mid'], lw=0.9, fs=8.0)
    arrow(ax, (x, 0.695), (x, 0.605), ec=C['gray2'], lw=0.9, ms=6)
    arrow(ax, (x, 0.405), (x, 0.330), ec=C['gray2'], lw=0.9, ms=6)
ax.annotate('', xy=(0.955, 0.115), xytext=(0.045, 0.115),
            arrowprops=dict(arrowstyle='-|>', color=C['dark'], lw=1.2, mutation_scale=11))
ax.text(0.5, 0.055, '单次到访 → 周期性复访：把“一次性烟火”变为“持续燃烧的篝火”',
        ha='center', fontsize=8.4, color=C['gray'])
save(fig, 'fig4-4')

# ============ 图4-5 意义生产的三重价值层次 ============
fig = plt.figure(figsize=(5.8, 3.0))
ax = blank_ax(fig)
lv = [(0.795, '深层文化价值', '生活重构与意义再造', '把理想生活的想象\n转化为可触及的夜间仪式', SEQ[0], 'white'),
      (0.510, '核心社会价值', '青年聚类与社交归属', '同温层轻社交\n破除都市孤立感', SEQ[1], 'white'),
      (0.225, '基础情绪价值', '情感抚慰与心理庇护', '无消费门槛的公共区\n暖光与低压背景音乐', SEQ[3], C['ink'])]
for y, a, b, c, fc, tc in lv:
    box(ax, 0.155, y, 0.235, 0.155, a, fc=fc, ec=C['dark'], color=tc, fs=8.8, lw=1.0)
    box(ax, 0.435, y, 0.28, 0.155, b, fc='white', ec=C['mid'], lw=0.9, fs=8.4)
    box(ax, 0.795, y, 0.35, 0.155, c, fc='white', ec=C['mid'], lw=0.9, fs=7.8)
ax.annotate('', xy=(0.035, 0.885), xytext=(0.035, 0.145),
            arrowprops=dict(arrowstyle='-|>', color=C['dark'], lw=1.3, mutation_scale=12))
ax.text(0.012, 0.515, '价值层级跃升', rotation=90, ha='center', va='center', fontsize=8.2, color=C['dark'])
box(ax, 0.5, 0.055, 0.88, 0.08, '使用价值 → 符号价值：价格敏感度下降，场景忠诚度攀升（整体好感度91%）',
    fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.4)
save(fig, 'fig4-5')

# ============ 图4-6 “流量—留量—增量”梯次递进漏斗 ============
fig = plt.figure(figsize=(6.0, 3.3))
ax = blank_ax(fig)
levels = [
    (0.790, 0.72, 0.56, '漏斗顶端  真实性（真）：磁吸引流',
     '在地文脉与本土舒适物聚合\n形成不可复制的差异化身份，转化为到访“流量”', SEQ[3], C['ink'], 24),
    (0.500, 0.56, 0.40, '漏斗中段  戏剧性（美）：拦截留量',
     '演艺驻场·五感沉浸·高频节律\n延长现场停留，把注意力流量沉淀为“留量”', SEQ[1], 'white', 22),
    (0.210, 0.40, 0.24, '漏斗底端  价值性（善）：深度增量',
     '圈层共鸣与意义生产\n以符号消费实现当期与长期“增量”', SEQ[0], 'white', 17),
]
for y, wt, wb, h, d, fc, tc, ww in levels:
    poly = plt.Polygon([[0.46 - wt / 2, y + 0.118], [0.46 + wt / 2, y + 0.118],
                        [0.46 + wb / 2, y - 0.118], [0.46 - wb / 2, y - 0.118]],
                       facecolor=fc, edgecolor=C['dark'], lw=1.0, zorder=2)
    ax.add_patch(poly)
    ax.text(0.46, y + 0.055, h, ha='center', va='center', fontsize=8.6, color=tc,
            fontweight='bold', zorder=3)
    ax.text(0.46, y - 0.045, wrap_cn(d, ww), ha='center', va='center', fontsize=7.4,
            color=tc, zorder=3, linespacing=1.5)
for y0, y1 in [(0.672, 0.618), (0.382, 0.328)]:
    arrow(ax, (0.46, y0), (0.46, y1), ec=C['dark'], lw=1.2, ms=9)
ax.plot([0.58, 0.885], [0.092, 0.092], color=C['gray'], lw=1.0, ls='--')
ax.plot([0.885, 0.885], [0.092, 0.908], color=C['gray'], lw=1.0, ls='--')
arrow(ax, (0.885, 0.908), (0.72, 0.908), ec=C['gray'], lw=1.0, ls='--', ms=8)
ax.text(0.945, 0.50, '增量反哺“真”与“美”', rotation=-90, ha='center', va='center',
        fontsize=8.0, color=C['gray'])
ax.text(0.46, 0.038, '真为根 · 美为形 · 善为魂：结构衔接、时序递进、功能反哺', ha='center',
        fontsize=8.4, color=C['gray'])
save(fig, 'fig4-6')

# ============ 图4-7 “真·美·善”三维闭环正反馈 ============
fig = plt.figure(figsize=(5.6, 3.2))
ax = blank_ax(fig)
P = {'A': (0.235, 0.735), 'D': (0.765, 0.735), 'V': (0.5, 0.245)}
box(ax, *P['A'], 0.30, 0.13, '真实性（真）\n源头供给', fc=SEQ[0], ec=C['dark'], color='white', fs=8.8, lw=1.1)
box(ax, *P['D'], 0.30, 0.13, '戏剧性（美）\n体验转化', fc=SEQ[1], ec=C['dark'], color='white', fs=8.8, lw=1.1)
box(ax, *P['V'], 0.30, 0.13, '价值性（善）\n生态反哺', fc=SEQ[2], ec=C['dark'], color=C['ink'], fs=8.8, lw=1.1)
arrow(ax, (0.385, 0.755), (0.615, 0.755), ec=C['dark'], lw=1.2, rad=-0.20, ms=9)
arrow(ax, (0.775, 0.665), (0.605, 0.300), ec=C['dark'], lw=1.2, rad=-0.20, ms=9)
arrow(ax, (0.395, 0.300), (0.225, 0.665), ec=C['dark'], lw=1.2, rad=-0.20, ms=9)
ax.text(0.5, 0.885, '提供不可复制的内容底色', ha='center', fontsize=8.0, color=C['gray'])
ax.text(0.845, 0.50, '提供最直观的\n体验入口', ha='center', va='center', fontsize=8.0, color=C['gray'])
ax.text(0.145, 0.50, '反哺文化土壤\n与内容迭代', ha='center', va='center', fontsize=8.0, color=C['gray'])
box(ax, 0.5, 0.53, 0.20, 0.10, '蜂鸣放大', fc='white', ec=C['dark'], lw=1.0, fs=8.8)
ax.text(0.5, 0.06, '自我造血能力与抗周期风险能力：场景由静态外壳成长为有机生态系统',
        ha='center', fontsize=8.2, color=C['gray'])
save(fig, 'fig4-7')

# ============ 图4-8 光影秀期间关键运营指标变化 ============
fig, ax = plt.subplots(figsize=(5.6, 2.8))
idx = ['平均停留时长\n（分钟）', '夜间客流指数\n（基期=100）', '关联业态夜间营收指数\n（基期=100）']
before = [42.0, 100.0, 100.0]
after = [78.0, 147.0, 138.0]
x = np.arange(3); w = 0.35
r1 = ax.bar(x - w / 2, before, w, color=SEQ[3], edgecolor=C['dark'], lw=0.5, label='光影秀推出前', zorder=3)
r2 = ax.bar(x + w / 2, after, w, color=SEQ[0], edgecolor=C['dark'], lw=0.5, label='光影秀推出期间', zorder=3)
for rr in (r1, r2):
    for p in rr:
        if p.get_height() > 0:
            ax.text(p.get_x() + p.get_width() / 2, p.get_height() + 2.0, '%.0f' % p.get_height(),
                    ha='center', va='bottom', fontsize=8.0, color=C['ink'])
for xx, bv, av in zip(x, before, after):
    ax.annotate('+%.1f%%' % ((av - bv) / bv * 100), xy=(xx, max(av, bv) + 13),
                ha='center', fontsize=8.2, color=C['accent'])
ax.set_xticks(x); ax.set_xticklabels(idx)
ax.set_ylabel('指标值'); ax.set_ylim(0, 185)
ax.legend(loc='upper left'); tidy(ax)
note(ax, '注：以2025年国庆“运河千里图”主题光影秀为观测窗口，数据来源于广场运营方客流监测与本研究访谈。', y=-0.22)
save(fig, 'fig4-8')

# ============ 图4-9 三维耦合演化的数值模拟 ============
t = np.linspace(0, 24, 400)
A = 0.28 + 0.52 * (1 - np.exp(-t / 5.2))
D = 0.18 + 0.60 * (1 - np.exp(-t / 7.0)) * (0.55 + 0.45 * A)
V = 0.08 + 0.72 * (1 - np.exp(-((t / 11.0) ** 1.9)))
S = (A * D * V) ** (1 / 3)
Cd = np.sqrt(S * (A + D + V) / 3)
fig, ax = plt.subplots(figsize=(5.9, 3.0))
ax.plot(t, A, color=SEQ[0], lw=1.5, label='真实性存量 $A(t)$')
ax.plot(t, D, color=SEQ[1], lw=1.5, ls='--', label='戏剧性强度 $D(t)$')
ax.plot(t, V, color=C['accent'], lw=1.5, ls='-.', label='价值认同 $V(t)$')
ax.plot(t, Cd, color=C['ink'], lw=1.8, ls=':', label='耦合协调度 $C(t)$')
ax.axvline(6.0, color=C['gray2'], lw=0.8)
ax.axvline(13.0, color=C['gray2'], lw=0.8)
ax.text(3.0, 1.05, 'Ⅰ 引流期', ha='center', fontsize=8.0, color=C['gray'])
ax.text(9.5, 1.05, 'Ⅱ 留量期', ha='center', fontsize=8.0, color=C['gray'])
ax.text(18.5, 1.05, 'Ⅲ 增量与反哺期', ha='center', fontsize=8.0, color=C['gray'])
ax.set_xlabel('运营时间 $t$（月）'); ax.set_ylabel('维度水平（归一化）')
ax.set_xlim(0, 24); ax.set_ylim(0, 1.14)
ax.legend(loc='lower right', ncol=2, columnspacing=1.0); tidy(ax)
note(ax, '注：依据式（4-4）至式（4-8）设定参数进行数值模拟，用于刻画三维耦合的阶段性演化特征。', y=-0.20)
save(fig, 'fig4-9')

# ============ 图5-1 “嘉夜场景”模式的可推广框架 ============
fig = plt.figure(figsize=(6.2, 3.3))
ax = blank_ax(fig)
box(ax, 0.5, 0.935, 0.86, 0.085, '“嘉夜场景”模式：可迁移的三维工具箱与适配条件',
    fc=C['dark'], ec=C['dark'], color='white', fs=9.2, lw=1.0)
tools = [(0.185, '真·工具箱', '在地文脉清单化\n本土舒适物优先招商\n公共空间社群让渡'),
         (0.500, '美·工具箱', '内容锚点轻资产合作\n光影节点动线化布局\n三级节律活动日历'),
         (0.815, '善·工具箱', '目标客群反向配置业态\n低门槛表达场景\n城市级品牌IP运营')]
for x, h, d in tools:
    box(ax, x, 0.755, 0.28, 0.09, h, fc=C['pale'], ec=C['dark'], lw=1.0, fs=8.8)
    box(ax, x, 0.545, 0.28, 0.23, d, fc='white', ec=C['mid'], lw=0.9, fs=8.0)
    arrow(ax, (x, 0.708), (x, 0.665), ec=C['gray2'], lw=0.9, ms=6)
    arrow(ax, (x, 0.428), (x, 0.375), ec=C['gray2'], lw=0.9, ms=6)
cond = [(0.185, '资源条件', '可识别的在地文脉\n与非遗、老字号存量'),
        (0.500, '主体条件', '具备长期主义的运营主体\n（国资或长周期资本）'),
        (0.815, '市场条件', '30万以上城区常住人口\n且存在青年消费外流缺口')]
for x, h, d in cond:
    box(ax, x, 0.315, 0.28, 0.09, h, fc='white', ec=C['dark'], lw=1.0, fs=8.6)
    box(ax, x, 0.155, 0.28, 0.16, d, fc='white', ec=C['gray2'], lw=0.9, ls='--', fs=7.8)
    arrow(ax, (x, 0.268), (x, 0.238), ec=C['gray2'], lw=0.8, ms=6)
ax.text(0.5, 0.045, '适配条件同时满足时，模式可迁移；条件缺失时，须以“先内容后重资产”的次序渐进推进',
        ha='center', fontsize=8.2, color=C['gray'])
save(fig, 'fig5-1')
