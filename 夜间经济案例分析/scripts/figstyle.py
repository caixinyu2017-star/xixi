# -*- coding: utf-8 -*-
"""学术风格绘图基础设置：黑白灰+低饱和蓝，无图标，符合统计学制图规范。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np, os

FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(FONT)
_fp = font_manager.FontProperties(fname=FONT)
FNAME = _fp.get_name()

plt.rcParams.update({
    'font.family': FNAME,
    'font.sans-serif': [FNAME],
    'axes.unicode_minus': False,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.linewidth': 0.8,
    'axes.edgecolor': '#333333',
    'axes.labelsize': 9,
    'axes.titlesize': 10,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
    'legend.fontsize': 8.5,
    'legend.frameon': False,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.06,
})

# 低饱和学术配色（灰阶为主，蓝色系为辅）
C = {
    'ink':   '#1a1a1a',
    'dark':  '#2f4858',
    'mid':   '#5b7c99',
    'light': '#a8bfd0',
    'pale':  '#dce6ed',
    'gray':  '#7a7a7a',
    'gray2': '#b5b5b5',
    'grayl': '#e6e6e6',
    'accent':'#8c5a3c',
    'white': '#ffffff',
}
SEQ = ['#2f4858', '#5b7c99', '#8fb0c4', '#c3d5df', '#e6eef3']
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig')
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    p = os.path.join(OUT, name + '.png')
    fig.savefig(p, facecolor='white')
    plt.close(fig)
    print('saved', p)
    return p


def box(ax, x, y, w, h, text, fc='white', ec=C['dark'], lw=1.0, fs=8.5,
        color=C['ink'], bold=False, radius=0.012, ls='-', va='center', ha='center'):
    """圆角矩形文本框，坐标为中心点。"""
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle="round,pad=0,rounding_size=%.4f" % radius,
                       linewidth=lw, edgecolor=ec, facecolor=fc, linestyle=ls, zorder=2)
    ax.add_patch(p)
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=color, zorder=3,
            fontweight='bold' if bold else 'normal', linespacing=1.5)
    return p


def arrow(ax, p0, p1, ec=C['dark'], lw=1.0, style='-|>', ls='-', rad=0.0, ms=8, zorder=1):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms,
                        linewidth=lw, color=ec, linestyle=ls,
                        connectionstyle="arc3,rad=%.3f" % rad, zorder=zorder,
                        shrinkA=1.5, shrinkB=1.5)
    ax.add_patch(a)
    return a


def blank_ax(fig, rect=(0, 0, 1, 1)):
    ax = fig.add_axes(rect)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    return ax


def tidy(ax, grid='y'):
    """统计图通用清理：去顶右框线，加浅色网格。"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if grid == 'y':
        ax.yaxis.grid(True, color='#dddddd', linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)
    elif grid == 'x':
        ax.xaxis.grid(True, color='#dddddd', linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)


def note(ax, text, y=-0.20, fs=7.2, x=0.0):
    """图下方资料来源说明（置于坐标轴下方，随 tight bbox 一并保存）。"""
    ax.text(x, y, text, fontsize=fs, color=C['gray'], ha='left', va='top',
            transform=ax.transAxes)


def wrap_cn(s, n):
    """按字符数折行（中文等宽近似）。"""
    out, line, cnt = [], '', 0
    for ch in s:
        if ch == '\n':
            out.append(line); line = ''; cnt = 0; continue
        w = 1 if ord(ch) < 128 else 2
        if cnt + w > n * 2 and line:
            out.append(line); line = ''; cnt = 0
        line += ch; cnt += w
    if line:
        out.append(line)
    return '\n'.join(out)
