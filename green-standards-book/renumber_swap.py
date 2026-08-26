# -*- coding: utf-8 -*-
"""一次性脚本：修正图表编号顺序（按出现顺序重编号，六组互换）。

互换组：图2.1↔图2.2、图4.1↔图4.2、表4.1↔表4.2、图6.2↔图6.3、表6.1↔表6.2、
图11.3↔图11.4、图13.2↔图13.3；同步互换 fig 文件 token（生成器函数名、
保存路径、正文引用路径）并重命名 PNG 文件。
"""
import glob
import os

PAIRS = [
    ('图2.1', '图2.2'), ('fig2_1', 'fig2_2'),
    ('图4.1', '图4.2'), ('fig4_1', 'fig4_2'), ('表4.1', '表4.2'),
    ('图6.2', '图6.3'), ('fig6_2', 'fig6_3'), ('表6.1', '表6.2'),
    ('图11.3', '图11.4'), ('fig11_3', 'fig11_4'),
    ('图13.2', '图13.3'), ('fig13_2', 'fig13_3'),
]
FILES = sorted(glob.glob('content_ch*.py')) + [
    'figures_a.py', 'figures_b.py', 'diagrams.py',
    'data/figures_manifest.md', 'DESIGN.md']

TMP = '@@SWAPTMP@@'


def swap(text, a, b):
    return text.replace(a, TMP).replace(b, a).replace(TMP, b)


def main():
    for fp in FILES:
        s = open(fp, encoding='utf-8').read()
        orig = s
        for a, b in PAIRS:
            s = swap(s, a, b)
        if s != orig:
            open(fp, 'w', encoding='utf-8').write(s)
            print('swapped in', fp)
    for a, b in [('fig2_1', 'fig2_2'), ('fig4_1', 'fig4_2'), ('fig6_2', 'fig6_3'),
                 ('fig11_3', 'fig11_4'), ('fig13_2', 'fig13_3')]:
        pa, pb, pt = f'figs/{a}.png', f'figs/{b}.png', 'figs/_tmp_.png'
        os.rename(pa, pt)
        os.rename(pb, pa)
        os.rename(pt, pb)
        print('renamed', pa, '<->', pb)


if __name__ == '__main__':
    main()
