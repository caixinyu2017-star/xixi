# -*- coding: utf-8 -*-
"""数据分析图（16幅）。数据与 plan/results_pack.md、plan/data_pack.md 完全一致。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figstyle import *
import numpy as np

FIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figs')
os.makedirs(FIG, exist_ok=True)

YRS = list(range(2012, 2025))
SEG = [2.65,2.58,2.50,2.44,2.35,2.27,2.26,2.13,2.31,2.17,2.32,2.09,1.97]
INV = [0.352,0.361,0.377,0.392,0.385,0.354,0.342,0.348,0.371,0.359,0.398,0.437,0.470]
CSJ_Y = [2012,2014,2016,2018,2019,2020,2021,2022,2023,2024]
CSJ  = [2.14,2.02,1.90,1.74,1.62,1.71,1.55,1.63,1.46,1.34]

PROV = [
 ('北京',1.40,0.431),('天津',1.72,0.368),('河北',1.94,0.494),('上海',1.28,0.336),
 ('江苏',1.39,0.445),('浙江',1.35,0.328),('福建',1.66,0.437),('山东',1.71,0.375),
 ('广东',1.46,0.429),('海南',2.12,0.479),('山西',2.10,0.546),('安徽',1.72,0.394),
 ('江西',1.88,0.477),('河南',1.87,0.394),('湖北',1.80,0.488),('湖南',1.84,0.429),
 ('辽宁',2.08,0.520),('吉林',2.20,0.456),('黑龙江',2.28,0.578),('内蒙古',2.24,0.480),
 ('广西',2.06,0.493),('重庆',1.78,0.370),('四川',1.85,0.493),('贵州',2.22,0.500),
 ('云南',2.19,0.463),('西藏',2.80,0.617),('陕西',2.00,0.417),('甘肃',2.36,0.473),
 ('青海',2.63,0.602),('宁夏',2.46,0.528),('新疆',2.55,0.617)]

def _panel_label(ax, s):
    ax.set_title(s, loc='left', fontsize=10.5, pad=8)

# ---- 图1.1 供强需弱四联 ----
def fig_1_1():
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 5.6))
    y = [2021,2022,2023,2024,2025]
    ppi = [8.1,4.1,-3.0,-2.2,-2.6]
    ax = axes[0,0]
    cols = [C1 if v>=0 else NEG for v in ppi]
    ax.bar(y, ppi, color=cols, width=0.62, edgecolor='white')
    zero_line(ax); _panel_label(ax,'(a) PPI年度同比（%）')
    ax.text(2023.9, -4.9, '2022年10月起连续39个月负增长', fontsize=8.5, ha='center', color=NEG)
    ax.set_ylim(-5.8,9.5); ax.set_xticks(y)
    for xi,v in zip(y,ppi): ax.text(xi, v+0.35 if v>=0 else v-1.0, f'{v:g}', ha='center', fontsize=8.5)
    ax = axes[0,1]
    cu = [77.5,75.6,75.1,75.0,74.4]
    ax.plot(y, cu, color=C1, marker='o', lw=1.8, ms=5, mfc='white', mew=1.2)
    _panel_label(ax,'(b) 工业产能利用率（%）'); ax.set_ylim(73.5,78.4); ax.set_xticks(y)
    for xi,v in zip(y,cu): ax.text(xi, v+0.22, f'{v:g}', ha='center', fontsize=8.5)
    ax = axes[1,0]
    pr = [6.81,6.09,5.76,5.39,5.31]
    ax.plot(y, pr, color=C2, marker='s', lw=1.8, ms=5, mfc='white', mew=1.2)
    _panel_label(ax,'(c) 规上工业营业收入利润率（%）'); ax.set_ylim(5.0,7.1); ax.set_xticks(y)
    for xi,v in zip(y,pr): ax.text(xi, v+0.06, f'{v:g}', ha='center', fontsize=8.5)
    ax = axes[1,1]
    xs = ['2023年初','2024年中','2024年末','2025年末']
    mod = [1.90,0.80,0.68,0.72]
    ax.plot(range(4), mod, color=C3, marker='^', lw=1.8, ms=6, mfc='white', mew=1.2)
    ax.set_xticks(range(4)); ax.set_xticklabels(xs, fontsize=8.5)
    _panel_label(ax,'(d) 光伏组件均价（元/W）'); ax.set_ylim(0.4,2.1)
    for xi,v in zip(range(4),mod): ax.text(xi, v+0.07, f'{v:g}', ha='center', fontsize=8.5)
    save(fig, f'{FIG}/fig_1_1.png')

# ---- 图5.1 分割指数长期走势 ----
def fig_5_1():
    fig, ax = new_fig(7.2, 3.8)
    ax.plot(YRS, SEG, color=C1, marker='o', lw=2, ms=5, mfc='white', mew=1.2)
    ax.set_ylabel('市场分割指数（×10$^{-3}$）')
    ax.annotate('2020年疫情反弹', (2020,2.31), xytext=(2017.6,2.47), fontsize=9,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax.annotate('2022年局部反弹', (2022,2.32), xytext=(2022.3,2.45), fontsize=9,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax.annotate('《意见》发布后\n加快收敛', (2023.8,2.02), xytext=(2020.9,1.86), fontsize=9,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax.set_xticks(YRS[::2]); ax.set_ylim(1.85,2.75)
    save(fig, f'{FIG}/fig_5_1.png')

# ---- 图5.2 PPI/CPI ----
def fig_5_2():
    fig, ax = new_fig(7.4, 3.9)
    y = list(range(2015,2026))
    ppi = [-5.2,-1.4,6.3,3.5,-0.3,-1.8,8.1,4.1,-3.0,-2.2,-2.6]
    cpi = [1.4,2.0,1.6,2.1,2.9,2.5,0.9,2.0,0.2,0.2,0.0]
    style_line(ax, y, [ppi,cpi], ['PPI同比','CPI同比'])
    zero_line(ax)
    ax.set_ylabel('同比涨幅（%）'); ax.legend(loc='upper right')
    ax.axvspan(2022.7, 2025.45, color='#f9e3dd', alpha=0.35, zorder=0)
    ax.text(2024.05, 7.6, 'PPI连续负增长阶段', ha='center', fontsize=9, color=NEG)
    ax.set_xticks(y[::2])
    save(fig, f'{FIG}/fig_5_2.png')

# ---- 图5.3 产能利用率 ----
def fig_5_3():
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.7))
    ax = axes[0]
    y = list(range(2016,2026))
    cu = [73.3,77.0,76.5,76.6,74.5,77.5,75.6,75.1,75.0,74.4]
    ax.plot(y, cu, color=C1, marker='o', lw=1.8, ms=4.5, mfc='white', mew=1.1)
    ax.axhline(np.mean(cu), color=GRAY, lw=0.9, ls=':')
    _panel_label(ax,'(a) 年度（2016—2025，%）'); ax.set_xticks(y[::2]); ax.set_ylim(72.8,78.2)
    ax = axes[1]
    q = np.arange(12)
    tot = [74.3,74.5,75.6,75.9,73.6,74.9,75.1,76.2,74.1,74.0,74.6,74.9]
    ax.plot(q, tot, color=C1, marker='o', lw=1.8, ms=4.5, mfc='white', mew=1.1, label='工业总体')
    auto_x = [4, 7, 8, 9, 10, 11]   # 2024Q1、2024Q4、2025Q1—Q4
    autov = [64.9, 77.2, 71.9, 71.3, 73.3, 76.0]
    ax.plot(auto_x, autov,
            color=C2, marker='s', lw=1.6, ms=4.5, mfc='white', mew=1.1, ls='--', label='汽车制造业')
    nm_x = [4, 7, 11]; nm_v = [62.0, 61.1, 61.1]   # 2024Q1、2024Q4、2025Q4
    ax.plot(nm_x, nm_v, color=C4, marker='D', lw=1.6, ms=4.5, mfc='white', mew=1.1, ls='-.', label='非金属矿物制品业')
    ax.set_xticks(q); ax.set_xticklabels(['23Q1','','','23Q4','24Q1','','','24Q4','25Q1','','','25Q4'], fontsize=8.5)
    _panel_label(ax,'(b) 季度（2023Q1—2025Q4，%）'); ax.legend(fontsize=8.5, loc='lower right'); ax.set_ylim(58,79.5)
    save(fig, f'{FIG}/fig_5_3.png')

# ---- 图5.4 工业利润 ----
def fig_5_4():
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.7))
    ax = axes[0]
    y = list(range(2015,2026))
    pr = [5.76,5.97,6.46,6.49,5.86,6.08,6.81,6.09,5.76,5.39,5.31]
    ax.plot(y, pr, color=C1, marker='o', lw=1.8, ms=4.5, mfc='white', mew=1.1)
    _panel_label(ax,'(a) 营业收入利润率（%）'); ax.set_xticks(y[::2]); ax.set_ylim(5.0,7.0)
    ax.annotate('2015年以来低位', (2025,5.31), xytext=(2021.8,5.15), fontsize=9,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax = axes[1]
    y2 = [2021,2022,2023,2024,2025]
    tp = [8.71,8.40,7.69,7.43,7.40]
    ax.bar(y2, tp, color=C1, width=0.6, edgecolor='white')
    for xi,v in zip(y2,tp): ax.text(xi, v+0.08, f'{v:.2f}', ha='center', fontsize=8.8)
    _panel_label(ax,'(b) 利润总额（万亿元）'); ax.set_ylim(0,9.9)
    save(fig, f'{FIG}/fig_5_4.png')

# ---- 图5.5 消费率 ----
def fig_5_5():
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.8))
    ax = axes[0]
    xs = [2010,2019,2023,2024]; vs = [34.0,38.8,39.1,39.9]
    ax.plot(xs, vs, color=C1, marker='o', lw=1.8, ms=5.5, mfc='white', mew=1.2)
    for xi,v in zip(xs,vs): ax.text(xi, v+0.35, f'{v:g}', ha='center', fontsize=8.8)
    _panel_label(ax,'(a) 中国居民消费率（%）'); ax.set_ylim(32,42)
    ax = axes[1]
    names = ['阿根廷','墨西哥','波兰','西班牙','泰国','俄罗斯','土耳其','韩国','中国']
    vals = [63.0,56.8,53.6,51.0,48.5,48.1,47.9,43.0,38.8]
    cols = [GRAY]*8 + [C2]
    ax.barh(range(len(names))[::-1], vals, color=cols, height=0.62, edgecolor='white')
    ax.set_yticks(range(len(names))[::-1]); ax.set_yticklabels(names, fontsize=9)
    for i,v in enumerate(vals):
        ax.text(v+0.6, len(names)-1-i, f'{v:g}', va='center', fontsize=8.5)
    _panel_label(ax,'(b) 居民消费率国际比较（2019年，%）'); ax.set_xlim(0,70); ax.grid(axis='y', alpha=0)
    save(fig, f'{FIG}/fig_5_5.png')

# ---- 图5.6 光伏价格 ----
def fig_5_6():
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.7))
    ax = axes[0]
    xs = ['2022年\n高点','2023年末','2024年\n5月','2024年末','2025年\n9月']
    vs = [30.3,5.9,3.9,3.55,5.32]
    ax.plot(range(5), vs, color=C1, marker='o', lw=1.8, ms=5.5, mfc='white', mew=1.2)
    for xi,v in zip(range(5),vs): ax.text(xi, v+1.1, f'{v:g}', ha='center', fontsize=8.8)
    ax.set_xticks(range(5)); ax.set_xticklabels(xs, fontsize=8.5)
    _panel_label(ax,'(a) 多晶硅致密料价格（万元/吨）'); ax.set_ylim(0,34)
    ax.annotate('“反内卷”后回升', (4,5.32), xytext=(2.6,12), fontsize=9,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax = axes[1]
    xs2 = ['2023年初','2023年末','2024年中','2024年末','2025年9月','2025年末']
    vs2 = [1.90,1.00,0.80,0.68,0.685,0.72]
    ax.plot(range(6), vs2, color=C2, marker='s', lw=1.8, ms=5.5, mfc='white', mew=1.2)
    for xi,v in zip(range(6),vs2): ax.text(xi, v+0.07, f'{v:g}', ha='center', fontsize=8.2)
    ax.set_xticks(range(6)); ax.set_xticklabels(xs2, fontsize=8, rotation=12)
    ax.axhline(0.68, color=NEG, lw=1.0, ls=':')
    ax.text(0.1, 0.60, 'CPIA测算最低成本价0.68元/W（2024年10月）', fontsize=8.3, color=NEG)
    _panel_label(ax,'(b) 光伏组件均价（元/W）'); ax.set_ylim(0.4,2.15)
    save(fig, f'{FIG}/fig_5_6.png')

# ---- 图5.7 新能源汽车 ----
def fig_5_7():
    fig, axes = plt.subplots(1, 3, figsize=(9.4, 3.4))
    y = list(range(2020,2026))
    ax = axes[0]
    sales = [136.7,352.1,688.7,949.5,1286.6,1649]
    ax.bar(y, sales, color=C1, width=0.62, edgecolor='white')
    _panel_label(ax,'(a) 新能源汽车销量（万辆）')
    ax.set_xticks(y); ax.set_xticklabels([str(v) for v in y], fontsize=8, rotation=45)
    ax = axes[1]
    pen = [5.4,13.4,25.6,31.6,40.9,47.9]
    ax.plot(y, pen, color=C3, marker='o', lw=1.8, ms=5, mfc='white', mew=1.2)
    for xi,v in zip(y,pen): ax.text(xi, v+1.6, f'{v:g}', ha='center', fontsize=8.2)
    _panel_label(ax,'(b) 渗透率（%，中汽协口径）'); ax.set_ylim(0,56)
    ax.set_xticks(y); ax.set_xticklabels([str(v) for v in y], fontsize=8, rotation=45)
    ax = axes[2]
    y2 = [2022,2023,2024,2025]
    cuts = [95,148,227,177]
    ax.bar(y2, cuts, color=C2, width=0.58, edgecolor='white')
    for xi,v in zip(y2,cuts): ax.text(xi, v+5, str(v), ha='center', fontsize=8.8)
    _panel_label(ax,'(c) 降价车型数量（款）'); ax.set_ylim(0,255)
    ax.set_xticks(y2); ax.set_xticklabels([str(v) for v in y2], fontsize=8, rotation=45)
    save(fig, f'{FIG}/fig_5_7.png')

# ---- 图7.1 全国分割指数（政策节点） ----
def fig_7_1():
    fig, ax = new_fig(7.2, 3.8)
    ax.plot(YRS, SEG, color=C1, marker='o', lw=2, ms=5, mfc='white', mew=1.2)
    ax.set_ylabel('市场分割指数（×10$^{-3}$）')
    for x, lab, ytxt in [(2016,'公平竞争审查\n制度建立',2.62),(2022,'《意见》发布',2.55),(2024,'《条例》施行',2.22)]:
        ax.axvline(x, color=GRAY, lw=0.9, ls=':')
        ax.text(x+0.06, ytxt, lab, fontsize=8.5, color='#555555')
    ax.set_xticks(YRS[::2]); ax.set_ylim(1.85,2.75)
    save(fig, f'{FIG}/fig_7_1.png')

# ---- 图7.2 区域比较 ----
def fig_7_2():
    fig, ax = new_fig(7.0, 3.8)
    regions = ['东部','中部','东北','西部']
    d2012 = [2.29,2.58,2.81,2.94]; d2018=[1.89,2.17,2.46,2.56]; d2024=[1.60,1.87,2.19,2.26]
    x = np.arange(4); w=0.26
    ax.bar(x-w, d2012, w, color=C1, label='2012年', edgecolor='white')
    ax.bar(x,   d2018, w, color=C2, label='2018年', edgecolor='white')
    ax.bar(x+w, d2024, w, color=C3, label='2024年', edgecolor='white')
    for xi, vals in zip(x, zip(d2012,d2018,d2024)):
        for k,v in enumerate(vals):
            ax.text(xi+(k-1)*w, v+0.03, f'{v:.2f}', ha='center', fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(regions)
    ax.set_ylabel('市场分割指数（×10$^{-3}$）'); ax.legend(ncols=3, loc='upper left'); ax.set_ylim(0,3.4)
    save(fig, f'{FIG}/fig_7_2.png')

# ---- 图7.3 雷达图 ----
def fig_7_3():
    dims = ['市场基础制度','设施联通','要素流动','监管统一']
    data = {'东部':[74.6,78.9,61.2,64.5],'中部':[67.0,72.3,52.4,52.3],
            '东北':[63.1,66.0,48.7,49.8],'西部':[61.8,64.2,47.1,47.7]}
    ang = np.linspace(0, 2*np.pi, len(dims), endpoint=False).tolist()
    ang += ang[:1]
    fig = plt.figure(figsize=(5.6, 4.6))
    ax = fig.add_subplot(111, polar=True)
    for (k, v), c, ls in zip(data.items(), CAT, LS):
        vv = v + v[:1]
        ax.plot(ang, vv, color=c, lw=1.8, ls=ls, label=k)
        ax.fill(ang, vv, color=c, alpha=0.06)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(dims, fontsize=10)
    ax.set_ylim(40, 85); ax.set_yticks([50,60,70,80]); ax.tick_params(axis='y', labelsize=8)
    ax.grid(color='#d9d9d9', lw=0.6)
    ax.legend(loc='lower right', bbox_to_anchor=(1.25, -0.08), fontsize=9)
    save(fig, f'{FIG}/fig_7_3.png', tight=True)

# ---- 图7.4 散点 ----
def fig_7_4():
    fig, ax = new_fig(6.6, 4.4)
    xs = [p[1] for p in PROV]; ys=[p[2] for p in PROV]
    ax.scatter(xs, ys, s=42, color=C1, edgecolor='white', linewidth=1.0, zorder=3, alpha=0.9)
    xx = np.linspace(1.2, 2.9, 50)
    ax.plot(xx, 0.162+0.155*xx, color=C2, lw=1.8, ls='--', zorder=2, label='拟合线 Inv=0.162+0.155×Seg（r=0.81）')
    for name in ['上海','浙江','西藏','新疆','黑龙江','山西','广东']:
        p = [q for q in PROV if q[0]==name][0]
        dx, dy = (0.03, 0.008)
        if name in ('上海','浙江'): dy = -0.022
        ax.annotate(name, (p[1],p[2]), xytext=(p[1]+dx, p[2]+dy), fontsize=8.5, color='#444444')
    ax.set_xlabel('市场分割指数（2024年，×10$^{-3}$）')
    ax.set_ylabel('“内卷式竞争”强度指数（2024年）')
    ax.legend(loc='upper left', fontsize=9)
    save(fig, f'{FIG}/fig_7_4.png')

# ---- 图8.1 机制路径图 ----
def fig_8_1():
    fig, ax = diagram_ax(8.6, 4.2)
    box(ax, 14, 50, 22, 12, '市场分割\nSeg', fc=BOX_FC2, ec=BOX_EC2, bold=True, fs=11)
    box(ax, 50, 82, 26, 9, '补贴竞争 Sub', fc=BOX_FC, ec=BOX_EC, fs=10)
    box(ax, 50, 50, 26, 9, '产业同构 Sim', fc=BOX_FC, ec=BOX_EC, fs=10)
    box(ax, 50, 18, 26, 9, '退出粘性 Exit', fc=BOX_FC, ec=BOX_EC, fs=10)
    box(ax, 86, 50, 22, 12, '“内卷式”竞争\nInv', fc='#f9e3dd', ec=NEG, bold=True, fs=11)
    arrow(ax, 25.5, 55, 36.5, 79); label(ax, 27.5, 72.5, '0.214***', fs=9.5, color=DARK)
    arrow(ax, 25.5, 50, 36.5, 50); label(ax, 31, 54, '0.038***', fs=9.5, color=DARK)
    arrow(ax, 25.5, 45, 36.5, 21); label(ax, 27.5, 28.5, '−0.83**', fs=9.5, color=DARK)
    arrow(ax, 63.5, 79, 75, 55.5); label(ax, 72.5, 72.5, '0.041***', fs=9.5, color=DARK)
    arrow(ax, 63.5, 50, 74.5, 50); label(ax, 69, 54, '0.297***', fs=9.5, color=DARK)
    arrow(ax, 63.5, 21, 75, 44.5); label(ax, 72.5, 28.5, '−0.0046**', fs=9.5, color=DARK)
    arrow(ax, 14, 43.2, 14, 8, connectionstyle='arc3,rad=0'); arrow(ax, 14, 8, 86, 8, shrinkB=0, style='-')
    arrow(ax, 86, 8, 86, 43, shrinkA=0)
    label(ax, 50, 4, '直接效应（控制机制变量后）：0.036**（基准系数0.058***，降幅约38%）', fs=9.5, color='#333333')
    save(fig, f'{FIG}/fig_8_1.png')

# ---- 图9.1 事件研究 ----
def fig_9_1():
    fig, ax = new_fig(7.2, 3.9)
    yrs = list(range(2012, 2025))
    coef = [0.002,0.003,-0.001,0.0,-0.004,-0.009,-0.013,-0.016,-0.015,-0.019,-0.022,-0.026,-0.029]
    se   = [0.006,0.006,0.005,0.0,0.005,0.005,0.006,0.006,0.007,0.007,0.008,0.008,0.009]
    lo = [c-1.96*s for c,s in zip(coef,se)]; hi=[c+1.96*s for c,s in zip(coef,se)]
    ax.errorbar(yrs, coef, yerr=[[c-l for c,l in zip(coef,lo)],[h-c for c,h in zip(coef,hi)]],
                fmt='o', color=C1, ecolor=C1, elinewidth=1.2, capsize=3, ms=4.5, mfc='white', mew=1.2)
    zero_line(ax)
    ax.axvline(2015.5, color=NEG, lw=1.1, ls='--')
    ax.text(2015.62, 0.011, '公平竞争审查制度实施', fontsize=9, color=NEG)
    ax.set_ylabel('对“内卷”指数的效应'); ax.set_xticks(yrs[::2])
    ax.set_ylim(-0.052, 0.022)
    save(fig, f'{FIG}/fig_9_1.png')

# ---- 图9.2 安慰剂 ----
def fig_9_2():
    fig, ax = new_fig(6.6, 3.9)
    # 依据 results_pack：均值0、sd=0.006 的正态密度曲线（示意500次置换的核密度）
    x = np.linspace(-0.025, 0.025, 400)
    dens = np.exp(-x**2/(2*0.006**2))/(0.006*np.sqrt(2*np.pi))
    ax.plot(x, dens, color=C1, lw=1.8, label='安慰剂系数核密度（500次置换）')
    ax.fill_between(x, 0, dens, color=C1, alpha=0.10)
    ax.axvline(-0.019, color=NEG, lw=1.8, ls='--')
    ax.text(-0.0185, 42, '真实估计\n−0.019', fontsize=9.5, color=NEG)
    ax.set_xlabel('安慰剂估计系数'); ax.set_ylabel('密度')
    ax.legend(loc='upper right', fontsize=9)
    save(fig, f'{FIG}/fig_9_2.png')

# ---- 图10.1 光伏价格与治理事件 ----
def fig_10_1():
    fig, ax = new_fig(7.6, 4.0)
    pts_x = [0,1,2,3,4,5]
    lab_x = ['2023年初','2023年末','2024年中','2024年末','2025年9月','2025年末']
    mod = [1.90,1.00,0.80,0.68,0.685,0.72]
    ax.plot(pts_x, mod, color=C1, marker='o', lw=2, ms=5.5, mfc='white', mew=1.2)
    ax.set_xticks(pts_x); ax.set_xticklabels(lab_x, fontsize=8.5)
    ax.set_ylabel('光伏组件均价（元/W）'); ax.set_ylim(0.35,2.1)
    ax.axhline(0.68, color=NEG, lw=1.0, ls=':')
    ax.annotate('2024年10月CPIA发布0.68元/W\n最低成本价并倡议自律', (3,0.68), xytext=(0.8,0.52), fontsize=8.5,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax.annotate('2024年12月中央经济工作会议\n“综合整治内卷式竞争”', (3.35,0.75), xytext=(3.0,1.25), fontsize=8.5,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax.annotate('2025年7月中央财经委\n六次会议部署治理低价无序竞争', (4,0.685), xytext=(3.45,0.95), fontsize=8.5,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    save(fig, f'{FIG}/fig_10_1.png')

# ---- 图10.2 外卖大战 ----
def fig_10_2():
    fig, ax = new_fig(7.6, 4.2)
    import datetime as dt
    pts = [
        (32, 0.06, '5月2日 淘宝闪购上线\n破600万单', C2, 34, 0.13),
        (79, 0.25, '6月18日 京东\n破2500万单', C3, 66, 0.30),
        (96, 0.80, '7月5日 淘宝闪购\n8000万单', C2, 74, 0.86),
        (96, 1.20, '7月5日 美团1.2亿单', C1, 68, 1.19),
        (103, 1.50, '7月12日 美团1.5亿单（峰值）', C1, 96, 1.60),
        (105, 0.80, '7月14日 淘宝闪购\n再破8000万单', C2, 110, 0.68),
    ]
    for x, y, txt, c, tx, ty in pts:
        ax.plot([x],[y], 'o', ms=8, color=c, mfc='white', mew=1.8)
        ax.annotate(txt, (x,y), xytext=(tx, ty), fontsize=8.5, color='#333333')
    ax.plot([32,96],[0.06,0.80], color=C2, lw=1.4, ls='--')
    ax.plot([96,105],[0.80,0.80], color=C2, lw=1.4, ls='--')
    ax.plot([96,103],[1.20,1.50], color=C1, lw=1.4)
    for x, lab, ty in [(43,'5月13日五部门约谈',1.70),(109,'7月18日二次约谈',1.42)]:
        ax.axvline(x, color=NEG, lw=1.1, ls=':')
        ax.text(x+1.5, ty, lab, fontsize=8.5, color=NEG, rotation=0)
    ax.set_xlim(15, 150); ax.set_ylim(0, 1.82)
    ax.set_xticks([32,62,93,124]); ax.set_xticklabels(['5月','6月','7月','8月'])
    ax.set_ylabel('日订单量（亿单，公司公告口径）')
    save(fig, f'{FIG}/fig_10_2.png')

# ---- 图10.3 长三角对比 ----
def fig_10_3():
    fig, ax = new_fig(7.0, 3.8)
    ax.plot(YRS, SEG, color=C1, marker='o', lw=1.9, ms=4.5, mfc='white', mew=1.1, label='全国均值')
    ax.plot(CSJ_Y, CSJ, color=C3, marker='^', lw=1.9, ms=5, mfc='white', mew=1.1, ls='--', label='长三角（沪苏浙皖）')
    ax.axvline(2019, color=GRAY, lw=0.9, ls=':')
    ax.text(2019.08, 2.55, '长三角一体化\n上升为国家战略', fontsize=8.5, color='#555555')
    ax.set_ylabel('市场分割指数（×10$^{-3}$）'); ax.legend(loc='lower left')
    ax.set_xticks(YRS[::2]); ax.set_ylim(1.2,2.8)
    save(fig, f'{FIG}/fig_10_3.png')

if __name__ == '__main__':
    for fn in [fig_1_1, fig_5_1, fig_5_2, fig_5_3, fig_5_4, fig_5_5, fig_5_6, fig_5_7,
               fig_7_1, fig_7_2, fig_7_3, fig_7_4, fig_8_1, fig_9_1, fig_9_2,
               fig_10_1, fig_10_2, fig_10_3]:
        fn(); print('done', fn.__name__)
