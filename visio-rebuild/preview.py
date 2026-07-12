#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raster preview of the SAME layout that build_vsdx.py serialises to .vsdx.

The figure is sized in inches to equal the Visio page, so matplotlib point
sizes map 1:1 to Visio point sizes and the preview faithfully proxies what
Visio will draw (text wrapping is estimated).
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

import layout as LY

SCALE = LY.SCALE
DW, DH = LY.DESIGN_W, LY.DESIGN_H
PAGE_W, PAGE_H = DW / SCALE, DH / SCALE

# use any available sans font (visible text is ASCII; CJK only in metadata)
matplotlib.rcParams["font.family"] = "WenQuanYi Zen Hei"
matplotlib.rcParams["font.weight"] = "bold"

LS = {1: "-", 2: (0, (6, 4)), 3: (0, (1, 3))}
CHAR_EM = 0.51           # avg glyph advance as fraction of em (~Microsoft YaHei)
LEAD = 1.22              # line leading factor


def wrap_para(text, size_pt, avail_px):
    text = text.replace("•", "-")   # preview font lacks U+2022; Visio font has it
    if not text:
        return [""]
    char_px = CHAR_EM * size_pt / 72.0 * SCALE
    ncols = max(4, int(avail_px / char_px))
    return textwrap.wrap(text, width=ncols) or [""]


def line_h(size_pt):
    return LEAD * size_pt / 72.0 * SCALE


def draw_textblock(ax, x, y, w, h, paras, valign, lm, rm, tm, bm):
    avail = w - (lm + rm) * SCALE
    # build wrapped lines with their styling
    blocks = []          # (lines, size, color, align, spafter_px)
    total = 0.0
    for p in paras:
        lines = wrap_para(p["text"], p["size"], avail)
        sp = p.get("spafter", 0.0) * SCALE
        blocks.append((lines, p["size"], p["color"], p.get("align", 0), sp))
        total += len(lines) * line_h(p["size"]) + sp

    if valign == 0:      # top
        cur = y + tm * SCALE
    elif valign == 2:    # bottom
        cur = y + h - bm * SCALE - total
    else:                # middle
        cur = y + (h - total) / 2.0

    for lines, size, color, align, sp in blocks:
        lh = line_h(size)
        for ln in lines:
            if align == 1:
                tx, ha = x + w / 2.0, "center"
            elif align == 2:
                tx, ha = x + w - rm * SCALE, "right"
            else:
                tx, ha = x + lm * SCALE, "left"
            ax.text(tx, cur + lh * 0.5, ln, fontsize=size, color=color,
                    ha=ha, va="center", fontweight="bold")
            cur += lh
        cur += sp


def arrowstyle(ba, ea):
    if ba and ea: return "<|-|>"
    if ea: return "-|>"
    if ba: return "<|-"
    return "-"


def main():
    S = LY.build_shapes()
    fig = plt.figure(figsize=(PAGE_W, PAGE_H), dpi=110)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, DW)
    ax.set_ylim(DH, 0)          # top-left origin
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # draw in list order so preview z-order matches the .vsdx exactly
    for s in S:
        if s["kind"] == "line":
            style = arrowstyle(s.get("begin_arrow", 0), s.get("end_arrow", 0))
            asz = s.get("arrow_size", 2)
            ms = {1: 11, 2: 15}.get(asz, 13)
            fa = FancyArrowPatch(
                (s["x1"], s["y1"]), (s["x2"], s["y2"]),
                arrowstyle=style, mutation_scale=ms,
                lw=s.get("lw", 0.015) * 72, color=s.get("color", "#000000"),
                linestyle=LS.get(s.get("pattern", 1), "-"),
                shrinkA=0, shrinkB=0, joinstyle="miter", capstyle="butt")
            ax.add_patch(fa)
        else:
            x, y, w, h = s["x"], s["y"], s["w"], s["h"]
            if s["kind"] == "box":
                fill = s.get("fill", LY.WHITE)
                border = s.get("border", LY.BORDER)
                r = s.get("rounding", 0.09) * SCALE
                patch = FancyBboxPatch(
                    (x, y), w, h,
                    boxstyle=f"round,pad=0,rounding_size={r}",
                    linewidth=s.get("lw", 0.016) * 72,
                    edgecolor=border, facecolor=fill,
                    mutation_aspect=1.0)
                ax.add_patch(patch)
                lm = rm = 0.09; tm = 0.07; bm = 0.05
                valign = s.get("valign", 0)
            else:
                lm = rm = tm = bm = 0.02
                valign = s.get("valign", 1)
            draw_textblock(ax, x, y, w, h, s["paras"], valign, lm, rm, tm, bm)

    fig.savefig("preview.png", dpi=110)
    print("wrote preview.png")


if __name__ == "__main__":
    main()
