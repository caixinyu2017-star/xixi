#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render scene.py to a self-contained HTML file for visual QA.
A headless-Chromium screenshot of this HTML is a faithful proxy for the .vsdx
layout because both are generated from the same BOXES/CONNS data.
"""
import os
from html import escape
import scene as SC

PPI = 100.0 / 72.0        # 1400px == 14in == 100px/in ; pt -> px

def fpx(pt):
    return round(pt * PPI, 2)

ALIGN = {0: "left", 1: "center", 2: "right"}
JUSTIFY = {"top": "flex-start", "middle": "center", "bottom": "flex-end"}


def box_div(b):
    l, t, r, bot = b["px"]
    w, h = r - l, bot - t
    style = [
        "position:absolute", f"left:{l}px", f"top:{t}px",
        f"width:{w}px", f"height:{h}px", "box-sizing:border-box",
        "display:flex", "flex-direction:column",
        f"justify-content:{JUSTIFY[b['valign']]}",
        "padding:5px 7px", "overflow:hidden",
    ]
    if b["fill"]:
        style.append(f"background:{b['fill']}")
    if b["line"]:
        style.append(f"border:{b['line_w']}px solid {b['line']}")
        style.append(f"border-radius:{b['rounding']}px")
    paras = []
    for st_name, txt in b["paras"]:
        s = SC.STYLES[st_name]
        pstyle = (f"text-align:{ALIGN[s['align']]};color:{s['color']};"
                  f"font-size:{fpx(s['size'])}px;line-height:1.16;margin:0.5px 0;"
                  f"white-space:pre-wrap")
        paras.append(f'<div style="{pstyle}">{escape(txt) or "&nbsp;"}</div>')
    return f'<div style="{";".join(style)}">' + "".join(paras) + "</div>"


def markers():
    defs = []
    for name, col in (("bk", SC.BLACK), ("bl", SC.DASH_BLUE)):
        for d, refx, pts in (("e", 9, "0,0 10,3.5 0,7"), ("s", 1, "10,0 0,3.5 10,7")):
            defs.append(
                f'<marker id="ar_{name}_{d}" markerWidth="10" markerHeight="7" '
                f'refX="{refx}" refY="3.5" orient="auto" markerUnits="userSpaceOnUse">'
                f'<polygon points="{pts}" fill="{col}"/></marker>')
    return "<defs>" + "".join(defs) + "</defs>"


def conn_svg():
    lines = []
    for c in SC.CONNS:
        col = c["color"]
        mk = "bl" if col == SC.DASH_BLUE else ("bk" if col == SC.BLACK else None)
        pts = " ".join(f"{x},{y}" for x, y in c["points"])
        attrs = [f'points="{pts}"', 'fill="none"', f'stroke="{col}"',
                 f'stroke-width="{c["w"]}"']
        if c["dash"]:
            attrs.append('stroke-dasharray="5,4"')
        if mk and c["end"]:
            attrs.append(f'marker-end="url(#ar_{mk}_e)"')
        if mk and c["begin"]:
            attrs.append(f'marker-start="url(#ar_{mk}_s)"')
        lines.append(f'<polyline {" ".join(attrs)}/>')
    return (f'<svg style="position:absolute;left:0;top:0" width="{int(SC.IMG_W)}" '
            f'height="{int(SC.IMG_H)}" viewBox="0 0 {int(SC.IMG_W)} {int(SC.IMG_H)}">'
            + markers() + "".join(lines) + "</svg>")


def html():
    body = "".join(box_div(b) for b in SC.BOXES) + conn_svg()
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        "*{margin:0;padding:0}"
        "body{font-family:'Microsoft YaHei','WenQuanYi Zen Hei','Noto Sans CJK SC',sans-serif;"
        "font-weight:700}"
        f"#page{{position:relative;width:{int(SC.IMG_W)}px;height:{int(SC.IMG_H)}px;background:#fff}}"
        "</style></head><body>"
        f"<div id='page'>{body}</div></body></html>"
    )


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "preview.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html())
    print("wrote", out)
