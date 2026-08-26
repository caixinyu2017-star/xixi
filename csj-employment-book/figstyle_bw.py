# -*- coding: utf-8 -*-
"""出版级黑白（灰度）图形统一样式。

全书铁律：图片一律黑白。系列区分依靠——
线型（实/虚/点划/点）、标记形状（○□△◇×）、灰度深浅（间距≥25%）与填充图案（hatch）。
任何像素 RGB 三通道应近似相等（饱和度≈0）。
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

for _fp in ('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc'):
    if os.path.exists(_fp):
        font_manager.fontManager.addfont(_fp)
        CJK = font_manager.FontProperties(fname=_fp).get_name()
        break
else:
    CJK = 'DejaVu Sans'

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
    'grid.alpha': 0.30,
    'grid.linewidth': 0.6,
    'grid.color': '#999999',
    'legend.frameon': False,
    'figure.dpi': 130,
    'savefig.dpi': 400,
    'savefig.bbox': 'tight',
})

# 灰度梯队（复印可辨，相邻间距 ≥25%）
GRAY = {'k': '#000000', 'g1': '#333333', 'g2': '#666666',
        'g3': '#999999', 'g4': '#CCCCCC', 'w': '#FFFFFF'}
# 条形图系列：灰度＋图案双保险
BARS = [dict(color='#333333', hatch=None),
        dict(color='#FFFFFF', hatch='///', edgecolor='#000000'),
        dict(color='#999999', hatch=None),
        dict(color='#FFFFFF', hatch='...', edgecolor='#000000'),
        dict(color='#CCCCCC', hatch='\\\\\\', edgecolor='#000000'),
        dict(color='#666666', hatch=None)]
# 折线系列：线型＋标记双保险
LINES = [dict(color='#000000', ls='-', marker='o', ms=4),
         dict(color='#333333', ls='--', marker='s', ms=4),
         dict(color='#666666', ls='-.', marker='^', ms=4.5),
         dict(color='#999999', ls=':', marker='D', ms=3.6),
         dict(color='#000000', ls='--', marker='x', ms=5)]


def save(fig, path):
    fig.savefig(path, dpi=400, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    _assert_grayscale(path)
    print('ok', os.path.basename(path))


def _assert_grayscale(path, tol=6):
    """质检：任何像素三通道差不得超过 tol（防止误用彩色）。"""
    from PIL import Image
    import numpy as np
    im = np.asarray(Image.open(path).convert('RGB'), dtype=int)
    d = max(abs(im[..., 0] - im[..., 1]).max(), abs(im[..., 1] - im[..., 2]).max())
    if d > tol:
        raise AssertionError(f'{path} 含彩色像素（通道差 {d}），违反黑白铁律')


def grid_y(ax):
    ax.grid(axis='y', linestyle='-', color='#AAAAAA', alpha=0.35, linewidth=0.6)
    ax.grid(axis='x', visible=False)
    ax.set_axisbelow(True)


def panel_label(ax, s, x=-0.12, y=1.04):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=9, fontweight='bold')
