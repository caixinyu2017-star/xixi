# -*- coding: utf-8 -*-
"""出版级图形统一样式（nature 风格，支持中文）。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager

_FP = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_manager.fontManager.addfont(_FP)
CJK = font_manager.FontProperties(fname=_FP).get_name()

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': [CJK, 'DejaVu Sans'],
    'axes.unicode_minus': False,
    'font.size': 9,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'axes.spines.right': False,
    'axes.spines.top': False,
    'axes.linewidth': 0.9,
    'axes.grid': True,
    'grid.alpha': 0.25,
    'grid.linewidth': 0.6,
    'legend.frameon': False,
    'figure.dpi': 130,
    'savefig.dpi': 400,
    'savefig.bbox': 'tight',
})

# 专业配色（克制、印刷友好、色盲可辨）
PAL = {
    'blue': '#1F4E79', 'orange': '#C55A11', 'teal': '#2E8B8B',
    'gold': '#BF9000', 'red': '#A02020', 'gray': '#7F7F7F',
    'green': '#548235', 'purple': '#674EA7', 'ltblue': '#8FAADC',
}
SERIES = [PAL['blue'], PAL['orange'], PAL['teal'], PAL['gold'], PAL['green'], PAL['purple']]
REGION_C = {'东部': PAL['blue'], '中部': PAL['orange'], '西部': PAL['red'], '东北': PAL['teal']}


def save(fig, path):
    fig.savefig(path, dpi=400, bbox_inches='tight', facecolor='white')
    plt.close(fig)
