# -*- coding: utf-8 -*-
"""对所有最终选用的图片做白边裁剪（含上下留白），输出到 out/ins/<key>.png"""
import os
from PIL import Image
import numpy as np

GEN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(GEN, "out")
INS = os.path.join(OUT, "ins")
os.makedirs(INS, exist_ok=True)

KEYS = ["fig1_1","fig1_2","fig2_1","fig2_2","fig3_1","fig3_3","fig4_2","fig5_1",
        "fig6_1","fig7_1","fig8_1","fig9_1","fig9_2","fig9_4","fig10_1","fig10_2",
        "fig11_1","fig12_1","fig13_1","fig13_2","fig13_3","fig14_1"]

PAD = 14

def pick(key):
    for suffix in ("_final.png", ".png"):
        p = os.path.join(OUT, key + suffix)
        if os.path.exists(p):
            return p
    return None

for k in KEYS:
    src = pick(k)
    if not src:
        print("MISSING", k); continue
    im = Image.open(src).convert("RGB")
    a = np.array(im.convert("L"))
    mask = a < 245
    ys, xs = np.where(mask)
    if len(ys) == 0:
        print("EMPTY?", k); continue
    y0, y1 = max(0, ys.min()-PAD), min(im.height, ys.max()+1+PAD)
    x0, x1 = max(0, xs.min()-PAD), min(im.width, xs.max()+1+PAD)
    im.crop((x0, y0, x1, y1)).save(os.path.join(INS, k + ".png"))
    print(f"{k}: {im.size} -> {(x1-x0, y1-y0)} (from {os.path.basename(src)})")
