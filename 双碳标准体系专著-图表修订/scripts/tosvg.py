# -*- coding: utf-8 -*-
"""把 out/ins/ 的最终图放大2倍后矢量化为 SVG"""
import os, vtracer
from PIL import Image
INS='out/ins'; SVG='out/svg'; TMP='out/svg_tmp'
os.makedirs(SVG, exist_ok=True); os.makedirs(TMP, exist_ok=True)
NAMES={'fig1_1':'图1.1','fig1_2':'图1.2','fig2_1':'图2.1','fig2_2':'图2.2','fig3_1':'图3.1',
'fig3_3':'图3.3','fig4_2':'图4.2','fig5_1':'图5.1','fig6_1':'图6.1','fig7_1':'图7.1',
'fig8_1':'图8.1','fig9_1':'图9.1','fig9_2':'图9.2','fig9_4':'图9.4','fig10_1':'图10.1',
'fig10_2':'图10.2','fig11_1':'图11.1','fig12_1':'图12.1','fig13_1':'图13.1','fig13_2':'图13.2',
'fig13_3':'图13.3','fig14_1':'图14.1'}
for k, cn in sorted(NAMES.items()):
    src=f'{INS}/{k}.png'
    im=Image.open(src).convert('RGB')
    up=f'{TMP}/{k}_2x.png'
    im.resize((im.width*2, im.height*2), Image.LANCZOS).save(up)
    dst=f'{SVG}/{cn}.svg'
    vtracer.convert_image_to_svg_py(up, dst, colormode='color', filter_speckle=1,
        mode='spline', color_precision=8, corner_threshold=60,
        length_threshold=3.5, splice_threshold=45, path_precision=1)
    print(cn, os.path.getsize(dst)//1024, 'KB', flush=True)
