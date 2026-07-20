# -*- coding: utf-8 -*-
"""全书统一绘图样式：印刷友好、CJK、灰度可辨。
调色板已通过 dataviz 六项校验（light surface）。
用法：from figstyle import *；然后 new_fig(...) 等。
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

for f in ['/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
          '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc']:
    try:
        font_manager.fontManager.addfont(f)
    except Exception:
        pass

CN = 'Noto Sans CJK SC'
plt.rcParams.update({
    'font.sans-serif': [CN],
    'font.family': 'sans-serif',
    'axes.unicode_minus': False,
    'figure.dpi': 200,
    'savefig.dpi': 300,
    'font.size': 10.5,
    'axes.titlesize': 11,
    'axes.labelsize': 10.5,
    'xtick.labelsize': 9.5,
    'ytick.labelsize': 9.5,
    'legend.fontsize': 9.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.edgecolor': '#8a8a8a',
    'axes.linewidth': 0.8,
    'axes.grid': True,
    'grid.color': '#d9d9d9',
    'grid.linewidth': 0.6,
    'grid.alpha': 0.8,
    'xtick.color': '#555555',
    'ytick.color': '#555555',
    'text.color': '#1a1a1a',
    'axes.labelcolor': '#1a1a1a',
    'legend.frameon': False,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})

# 分类色（固定顺序，绝不循环）：蓝、橙、青绿、紫；强调深蓝；参考灰
C1, C2, C3, C4 = '#3573ab', '#d97a2b', '#2aa584', '#a768b5'
DARK = '#1f4e79'
GRAY = '#767676'
NEG = '#c0504d'   # 状态色：警示/负值（仅用于状态，不作系列色）
CAT = [C1, C2, C3, C4]
# 线型与标记：灰度打印下的次级编码（与颜色同序固定搭配）
LS  = ['-', '--', '-.', ':']
MK  = ['o', 's', '^', 'D']

def new_fig(w=7.0, h=3.6):
    fig, ax = plt.subplots(figsize=(w, h))
    return fig, ax

def style_line(ax, xs, ys, labels, idx=None, lw=1.8, ms=4.5, markevery=None):
    """多序列折线：颜色+线型+标记三重编码。idx 指定各序列使用的槽位。"""
    idx = idx or list(range(len(ys)))
    for k, (y, lab) in enumerate(zip(ys, labels)):
        i = idx[k]
        ax.plot(xs, y, color=CAT[i], ls=LS[i], marker=MK[i], ms=ms,
                lw=lw, label=lab, markevery=markevery,
                markerfacecolor='white', markeredgewidth=1.1, markeredgecolor=CAT[i])

def zero_line(ax):
    ax.axhline(0, color='#999999', lw=0.9, zorder=1)

def pct(ax, axis='y'):
    import matplotlib.ticker as mtk
    fmt = mtk.FuncFormatter(lambda v, _: f'{v:g}')
    getattr(ax, f'{axis}axis').set_major_formatter(fmt)

def save(fig, path, tight=True):
    if tight:
        fig.tight_layout(pad=0.6)
    fig.savefig(path, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# ---------- 机制框图工具 ----------
BOX_FC   = '#eef3f8'; BOX_EC   = '#3573ab'   # 主流程框
BOX_FC2  = '#fdf1e6'; BOX_EC2  = '#d97a2b'   # 问题/扭曲框
BOX_FC3  = '#e9f5f1'; BOX_EC3  = '#2aa584'   # 效应/红利框
BOX_FC4  = '#f4ecf7'; BOX_EC4  = '#a768b5'   # 政策框
BOX_GREY = '#f2f2f2'; BOX_GEC  = '#8a8a8a'

def diagram_ax(w=8.6, h=5.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.axis('off'); ax.grid(False)
    return fig, ax

def box(ax, x, y, w, h, text, fc=BOX_FC, ec=BOX_EC, fs=10, bold=False, lw=1.2, rounded=0.9):
    """x,y 为中心坐标（0-100 画布）。"""
    b = FancyBboxPatch((x - w/2, y - h/2), w, h,
                       boxstyle=f'round,pad=0.35,rounding_size={rounded}',
                       fc=fc, ec=ec, lw=lw, zorder=3, mutation_scale=1.6)
    ax.add_patch(b)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, zorder=4,
            fontweight='bold' if bold else 'normal', linespacing=1.45)

def arrow(ax, x1, y1, x2, y2, color='#555555', lw=1.4, style='-|>', shrinkA=6, shrinkB=6,
          connectionstyle='arc3,rad=0', ls='-'):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=13,
                        color=color, lw=lw, shrinkA=shrinkA, shrinkB=shrinkB, zorder=2,
                        connectionstyle=connectionstyle, linestyle=ls)
    ax.add_patch(a)

def label(ax, x, y, text, fs=9, color='#444444', ha='center', style='normal'):
    ax.text(x, y, text, ha=ha, va='center', fontsize=fs, color=color, zorder=4,
            style=style, linespacing=1.4)
