"""Render a PNG preview of the generated .vsdx by parsing its page geometry.

This does NOT depend on Visio/LibreOffice: it reads the shape cells we authored
(PinX/PinY/Width/Height, Geometry rows, Fill/Line colours, Rounding, Text) and
draws them with matplotlib, so we can eyeball the layout vs. the reference
images.  It intentionally mirrors what a Visio renderer does with the same data.
"""
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch

NS = '{http://schemas.microsoft.com/office/visio/2012/main}'
HERE = os.path.dirname(os.path.abspath(__file__))
VSDX = os.path.join(HERE, '..', 'figs', 'metaheuristic_diagrams.vsdx')


def cells(shape):
    d = {}
    for c in shape.findall(f'{NS}Cell'):
        d[c.get('N')] = c.get('V')
    return d


def geom_rows(shape):
    sec = shape.find(f'{NS}Section[@N="Geometry"]')
    if sec is None:
        return None, None
    nofill = sec.find(f'{NS}Cell[@N="NoFill"]')
    nofill = (nofill is not None and nofill.get('V') == '1')
    rows = []
    for r in sec.findall(f'{NS}Row'):
        rc = {c.get('N'): float(c.get('V')) for c in r.findall(f'{NS}Cell')}
        rows.append((r.get('T'), rc.get('X', 0.0), rc.get('Y', 0.0)))
    return nofill, rows


def get_text(shape):
    t = shape.find(f'{NS}Text')
    if t is None:
        return ''
    # join all text pieces (ignore cp/pp tags, keep tail text and newlines)
    parts = []
    if t.text:
        parts.append(t.text)
    for ch in t:
        if ch.tail:
            parts.append(ch.tail)
    return ''.join(parts)


def char_size(shape):
    sec = shape.find(f'{NS}Section[@N="Character"]')
    if sec is None:
        return 12
    row = sec.find(f'{NS}Row[@IX="0"]')
    sz = row.find(f'{NS}Cell[@N="Size"]')
    color = row.find(f'{NS}Cell[@N="Color"]')
    return float(sz.get('V')) * 72.0, (color.get('V') if color is not None else '#333333')


def render_page(page_xml, out_png, pw, ph, title):
    root = ET.fromstring(page_xml)
    shapes = root.find(f'{NS}Shapes')
    scale = 6.0
    fig, ax = plt.subplots(figsize=(pw * scale / 6.5, ph * scale / 6.5))
    ax.set_xlim(0, pw)
    ax.set_ylim(0, ph)
    ax.set_aspect('equal')
    ax.axis('off')
    for sh in shapes.findall(f'{NS}Shape'):
        c = cells(sh)
        pinx = float(c.get('PinX', 0)); piny = float(c.get('PinY', 0))
        w = float(c.get('Width', 0)); h = float(c.get('Height', 0))
        lpx = float(c.get('LocPinX', w / 2)); lpy = float(c.get('LocPinY', h / 2))
        angle = float(c.get('Angle', 0))
        ox, oy = pinx - lpx, piny - lpy   # bbox bottom-left (angle 0)
        fill = c.get('FillForegnd'); fillpat = c.get('FillPattern', '0')
        line = c.get('LineColor'); linepat = c.get('LinePattern', '1')
        rounding = float(c.get('Rounding', 0))
        end_arrow = c.get('EndArrow')
        nofill, rows = geom_rows(sh)

        is_connector = end_arrow is not None
        if rows and is_connector:
            pts = [(ox + x, oy + y) for (_t, x, y) in rows]
            for i in range(len(pts) - 1):
                ax.plot([pts[i][0], pts[i + 1][0]], [pts[i][1], pts[i + 1][1]],
                        color=line or '#4A4A4A', lw=1.1, solid_capstyle='round')
            a, b = pts[-2], pts[-1]
            ax.annotate('', xy=b, xytext=a,
                        arrowprops=dict(arrowstyle='-|>', color=line or '#4A4A4A', lw=1.1))
        elif rows:
            # detect diamond (5 rows, first MoveTo at mid-bottom) vs rectangle
            is_diamond = len(rows) == 5 and abs(rows[0][1] - w / 2) < 1e-6 and abs(rows[0][2]) < 1e-6
            fc = fill if fillpat != '0' else 'none'
            ls = '--' if linepat == '2' else '-'
            if is_diamond:
                verts = [(ox + x, oy + y) for (_t, x, y) in rows[:4]]
                ax.add_patch(Polygon(verts, closed=True, facecolor=fc,
                                     edgecolor=line, lw=1.1, linestyle=ls))
            else:
                pad = min(rounding, w / 2, h / 2)
                ax.add_patch(FancyBboxPatch((ox + pad, oy + pad), w - 2 * pad, h - 2 * pad,
                             boxstyle=f'round,pad={pad},rounding_size={max(pad,1e-3)}',
                             facecolor=fc, edgecolor=(line if line else 'none'),
                             lw=(1.1 if line else 0), linestyle=ls, mutation_aspect=1))
        # text
        txt = get_text(sh)
        if txt.strip():
            fs, col = char_size(sh)
            rot = 90 if angle > 1.0 else 0
            ax.text(pinx, piny, txt, ha='center', va='center',
                    fontsize=fs * scale / 6.5 * 0.72, color=col, rotation=rot,
                    fontweight='bold', wrap=True, zorder=5)
    fig.suptitle(title, y=0.995, fontsize=9, color='#888')
    fig.savefig(out_png, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print('wrote', out_png)


def main():
    with zipfile.ZipFile(VSDX) as z:
        pages = z.read('visio/pages/pages.xml').decode('utf-8')
        p1 = z.read('visio/pages/page1.xml').decode('utf-8')
        p2 = z.read('visio/pages/page2.xml').decode('utf-8')
    # page sizes from pages.xml
    dims = re.findall(r'PageWidth" V="([\d.]+)".*?PageHeight" V="([\d.]+)"', pages)
    (w1, h1), (w2, h2) = [(float(a), float(b)) for a, b in dims]
    out = os.path.join(HERE, '..', 'figs')
    render_page(p1, os.path.join(out, 'preview_page1_flowchart.png'), w1, h1, 'Page 1 preview')
    render_page(p2, os.path.join(out, 'preview_page2_classification.png'), w2, h2, 'Page 2 preview')


if __name__ == '__main__':
    main()
