# -*- coding: utf-8 -*-
"""将生成的新图替换进 draft.docx 对应媒体位置，并按新图宽高比更新版式尺寸。"""
import os, sys
from PIL import Image
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Emu

SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scratchpad
OUT = os.path.join(SP, "gen", "out")

# media 文件名 -> 新图 key（.png 在 gen/out/ 下，可被 final 覆盖：优先 <key>_final.png）
MAPPING = {
    "image1.png": "fig1_1",  "image2.png": "fig1_2",  "image3.png": "fig2_1",
    "image5.png": "fig3_1",  "image7.png": "fig3_3",  "image14.png": "fig5_1",
    "image18.png": "fig6_1", "image21.png": "fig7_1", "image25.png": "fig8_1",
    "image28.png": "fig9_1", "image32.png": "fig10_1","image33.png": "fig10_2",
    "image36.png": "fig11_1","image40.png": "fig12_1","image44.png": "fig13_1",
    "image45.png": "fig13_2","image47.png": "fig14_1",
}
MAX_H_EMU = Emu(int(8.2 * 914400))

def pick(key):
    for suffix in ("_final.png", ".png"):
        p = os.path.join(OUT, key + suffix)
        if os.path.exists(p):
            return p
    return None

def main(src, dst):
    doc = Document(src)
    replaced = {}
    for shp in doc.inline_shapes:
        try:
            rid = shp._inline.graphic.graphicData.pic.blipFill.blip.embed
            part = doc.part.related_parts[rid]
            mname = part.partname.split("/")[-1]
        except Exception:
            continue
        key = MAPPING.get(mname)
        if not key:
            continue
        newp = pick(key)
        if not newp:
            print("MISSING generated file for", key); continue
        data = open(newp, "rb").read()
        part._blob = data
        w, h = Image.open(newp).size
        cur_w = shp.width
        new_h = int(cur_w * h / w)
        if new_h > MAX_H_EMU:
            scale = MAX_H_EMU / new_h
            cur_w = int(cur_w * scale)
            new_h = int(MAX_H_EMU)
        shp.width = Emu(cur_w)
        shp.height = Emu(new_h)
        replaced[mname] = (key, os.path.basename(newp))
    doc.save(dst)
    for m, k in sorted(replaced.items()):
        print(f"{m:14s} <- {k[1]}")
    print(f"replaced {len(replaced)}/17 -> {dst}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SP, "src", "draft.docx")
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SP, "revised.docx")
    main(src, dst)
