"""Rebuild the two reference diagrams as a native, editable Visio (.vsdx) file.

Page 1: MSSBOA algorithm flowchart.
Page 2: Metaheuristic-algorithm classification tree.

Every shape is a real Visio shape (rectangle / rounded rectangle / diamond /
connector) with its own geometry and text -- nothing is a rasterised picture.
All text is Microsoft YaHei, bold, at a deliberately large point size, matching
the layout and colours of the reference images.

The package is assembled from the known-good part templates shipped with the
`vsdx` library (docProps, document.xml, masters, windows) plus freshly authored
page content.  Run:  python3 build_visio.py
Output: ../figs/metaheuristic_diagrams.vsdx
"""
import os
import re
import shutil
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_VSDX = os.path.join(HERE, '..', 'figs', 'metaheuristic_diagrams.vsdx')
BUILD = os.path.join(HERE, '..', 'figs', '_vsdx_build')

# Located at runtime: the vsdx library ships a real Visio file we borrow the
# boilerplate parts from (docProps, document.xml, masters, windows, .rels).
import vsdx  # noqa: E402
TEMPLATE_VSDX = os.path.join(os.path.dirname(vsdx.__file__), 'media', 'media.vsdx')

PT = 1.0 / 72.0  # points -> inches

# ----------------------------------------------------------------------------
# XML helpers
# ----------------------------------------------------------------------------

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def cell(n, v, f=None):
    if f is not None:
        return f'<Cell N="{n}" V="{v}" F="{f}"/>'
    return f'<Cell N="{n}" V="{v}"/>'


def parse_runs(text):
    """Split a label into (segment, is_subscript) runs.

    Backtick pairs mark subscript text, e.g. "X`best`" -> normal 'X', sub 'best'.
    """
    parts = text.split('`')
    runs = []
    for i, seg in enumerate(parts):
        if seg == '':
            continue
        runs.append((seg, i % 2 == 1))
    return runs


def char_section(size_in, color):
    """Character formatting: Microsoft YaHei, bold. Row 0 normal, row 1 subscript.

    The subscript row keeps the *base* Size and relies on Pos=2 to shrink+lower the
    glyphs, exactly as Visio authors subscripts. Setting a separately reduced Size
    would compound with Visio's automatic ~60% super/subscript scaling and render
    the subscript far too small.
    """
    sub = size_in
    return (
        '<Section N="Character">'
        f'<Row IX="0">'
        f'{cell("Font", "Microsoft YaHei")}{cell("AsianFont", "Microsoft YaHei")}'
        f'{cell("Color", color)}{cell("Style", "1")}{cell("Case", "0")}'
        f'{cell("Pos", "0")}{cell("Size", size_in)}'
        f'</Row>'
        f'<Row IX="1">'
        f'{cell("Font", "Microsoft YaHei")}{cell("AsianFont", "Microsoft YaHei")}'
        f'{cell("Color", color)}{cell("Style", "1")}{cell("Case", "0")}'
        f'{cell("Pos", "2")}{cell("Size", sub)}'
        f'</Row>'
        '</Section>'
    )


def para_section(align=1):
    # HorzAlign: 0 left, 1 centre, 2 right
    return f'<Section N="Paragraph"><Row IX="0">{cell("HorzAlign", align)}</Row></Section>'


def text_el(text, align=1):
    runs = parse_runs(text)
    body = f'<pp IX="0"/>'
    for seg, is_sub in runs:
        ix = 1 if is_sub else 0
        body += f'<cp IX="{ix}"/>' + esc(seg)
    return f'<Text>{body}</Text>'


def rect_geometry(w, h, nofill=0):
    return (
        f'<Section N="Geometry" IX="0">{cell("NoFill", nofill)}{cell("NoLine", 0)}'
        f'<Row T="MoveTo" IX="1">{cell("X", 0)}{cell("Y", 0)}</Row>'
        f'<Row T="LineTo" IX="2">{cell("X", round(w,5))}{cell("Y", 0)}</Row>'
        f'<Row T="LineTo" IX="3">{cell("X", round(w,5))}{cell("Y", round(h,5))}</Row>'
        f'<Row T="LineTo" IX="4">{cell("X", 0)}{cell("Y", round(h,5))}</Row>'
        f'<Row T="LineTo" IX="5">{cell("X", 0)}{cell("Y", 0)}</Row>'
        f'</Section>'
    )


def diamond_geometry(w, h):
    return (
        f'<Section N="Geometry" IX="0">{cell("NoFill", 0)}{cell("NoLine", 0)}'
        f'<Row T="MoveTo" IX="1">{cell("X", round(w/2,5))}{cell("Y", 0)}</Row>'
        f'<Row T="LineTo" IX="2">{cell("X", round(w,5))}{cell("Y", round(h/2,5))}</Row>'
        f'<Row T="LineTo" IX="3">{cell("X", round(w/2,5))}{cell("Y", round(h,5))}</Row>'
        f'<Row T="LineTo" IX="4">{cell("X", 0)}{cell("Y", round(h/2,5))}</Row>'
        f'<Row T="LineTo" IX="5">{cell("X", round(w/2,5))}{cell("Y", 0)}</Row>'
        f'</Section>'
    )


# ----------------------------------------------------------------------------
# Shape factories.  All coordinates in inches, origin bottom-left, Y up.
# ----------------------------------------------------------------------------
_id = [0]


def next_id():
    _id[0] += 1
    return _id[0]


def box(cx, cy, w, h, text, fill, line, size_pt, *, shape='rect',
        rounding=0.09, lw_pt=1.0, text_color='#333333', align=1):
    sid = next_id()
    size_in = round(size_pt * PT, 5)
    geom = diamond_geometry(w, h) if shape == 'diamond' else rect_geometry(w, h)
    rnd = 0.0 if shape == 'diamond' else rounding
    return (
        f'<Shape ID="{sid}" Type="Shape" LineStyle="0" FillStyle="0" TextStyle="0">'
        f'{cell("PinX", round(cx,5))}{cell("PinY", round(cy,5))}'
        f'{cell("Width", round(w,5))}{cell("Height", round(h,5))}'
        f'{cell("LocPinX", round(w/2,5), "Width*0.5")}{cell("LocPinY", round(h/2,5), "Height*0.5")}'
        f'{cell("Angle", 0)}{cell("FlipX", 0)}{cell("FlipY", 0)}'
        f'{cell("FillForegnd", fill)}{cell("FillBkgnd", fill)}{cell("FillPattern", 1)}'
        f'{cell("LineColor", line)}{cell("LineWeight", round(lw_pt*PT,5))}{cell("LinePattern", 1)}'
        f'{cell("Rounding", rnd)}'
        f'{cell("VerticalAlign", 1)}{cell("LeftMargin", 0.03)}{cell("RightMargin", 0.03)}'
        f'{cell("TopMargin", 0.02)}{cell("BottomMargin", 0.02)}'
        f'{char_section(size_in, text_color)}{para_section(align)}'
        f'{geom}{text_el(text)}'
        f'</Shape>'
    )


def label(cx, cy, w, h, text, size_pt, color='#333333', angle=0.0, align=1):
    """Text-only shape (no border, no fill)."""
    sid = next_id()
    size_in = round(size_pt * PT, 5)
    ang = '' if abs(angle) < 1e-9 else cell("Angle", round(angle, 6))
    return (
        f'<Shape ID="{sid}" Type="Shape" LineStyle="0" FillStyle="0" TextStyle="0">'
        f'{cell("PinX", round(cx,5))}{cell("PinY", round(cy,5))}'
        f'{cell("Width", round(w,5))}{cell("Height", round(h,5))}'
        f'{cell("LocPinX", round(w/2,5), "Width*0.5")}{cell("LocPinY", round(h/2,5), "Height*0.5")}'
        f'{ang if ang else cell("Angle", 0)}{cell("FlipX", 0)}{cell("FlipY", 0)}'
        f'{cell("FillPattern", 0)}{cell("LinePattern", 0)}'
        f'{cell("VerticalAlign", 1)}'
        f'{char_section(size_in, color)}{para_section(align)}'
        f'{text_el(text)}'
        f'</Shape>'
    )


def connector(points, color='#4A4A4A', lw_pt=1.1, end_arrow=4, begin_arrow=0):
    """Open polyline connector with an arrowhead at the final point."""
    sid = next_id()
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    w = max(maxx - minx, 0.001)
    h = max(maxy - miny, 0.001)
    # local coords relative to bbox bottom-left
    rows = []
    for i, (px, py) in enumerate(points):
        t = 'MoveTo' if i == 0 else 'LineTo'
        rows.append(f'<Row T="{t}" IX="{i+1}">{cell("X", round(px-minx,5))}{cell("Y", round(py-miny,5))}</Row>')
    geom = (f'<Section N="Geometry" IX="0">{cell("NoFill", 1)}{cell("NoLine", 0)}'
            + ''.join(rows) + '</Section>')
    return (
        f'<Shape ID="{sid}" Type="Shape" LineStyle="0" FillStyle="0" TextStyle="0">'
        f'{cell("PinX", round(minx + w/2,5))}{cell("PinY", round(miny + h/2,5))}'
        f'{cell("Width", round(w,5))}{cell("Height", round(h,5))}'
        f'{cell("LocPinX", round(w/2,5), "Width*0.5")}{cell("LocPinY", round(h/2,5), "Height*0.5")}'
        f'{cell("Angle", 0)}{cell("FlipX", 0)}{cell("FlipY", 0)}'
        f'{cell("FillPattern", 0)}'
        f'{cell("LineColor", color)}{cell("LineWeight", round(lw_pt*PT,5))}{cell("LinePattern", 1)}'
        f'{cell("BeginArrow", begin_arrow)}{cell("EndArrow", end_arrow)}'
        f'{cell("BeginArrowSize", 2)}{cell("EndArrowSize", 2)}'
        f'{geom}'
        f'</Shape>'
    )


def dashed_frame(cx, cy, w, h, line, lw_pt=1.0):
    sid = next_id()
    return (
        f'<Shape ID="{sid}" Type="Shape" LineStyle="0" FillStyle="0" TextStyle="0">'
        f'{cell("PinX", round(cx,5))}{cell("PinY", round(cy,5))}'
        f'{cell("Width", round(w,5))}{cell("Height", round(h,5))}'
        f'{cell("LocPinX", round(w/2,5), "Width*0.5")}{cell("LocPinY", round(h/2,5), "Height*0.5")}'
        f'{cell("Angle", 0)}{cell("FlipX", 0)}{cell("FlipY", 0)}'
        f'{cell("FillPattern", 0)}'
        f'{cell("LineColor", line)}{cell("LineWeight", round(lw_pt*PT,5))}{cell("LinePattern", 2)}'
        f'{cell("Rounding", 0.06)}'
        f'{rect_geometry(w, h, nofill=1)}'
        f'</Shape>'
    )


# ----------------------------------------------------------------------------
# Word wrap for classification item boxes
# ----------------------------------------------------------------------------

def wrap(text, max_chars):
    words = text.split(' ')
    lines, cur = [], ''
    for wd in words:
        trial = wd if not cur else cur + ' ' + wd
        if len(trial) <= max_chars or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# ============================================================================
# PAGE 1 -- MSSBOA flowchart
# ============================================================================
GREEN_F, GREEN_L = '#D5E8D4', '#82B366'
BLUE_F, BLUE_L = '#DAE8FC', '#6C8EBF'
ORANGE_F, ORANGE_L = '#FFE6CC', '#D79B00'
RED_F, RED_L = '#F8CECC', '#B85450'
DARK = '#333333'


def page1_shapes():
    _id[0] = 0
    s = []
    cx = 4.5
    # --- boxes -------------------------------------------------------------
    s.append(box(cx, 12.95, 2.0, 0.6, 'Start', GREEN_F, GREEN_L, 15, rounding=0.28, text_color='#2E5A2E'))
    s.append(box(cx, 11.95, 5.2, 0.95, 'Good point set initialization of X (S1);\nset t = 0, T, N',
                 GREEN_F, GREEN_L, 13, text_color='#2E5A2E'))
    s.append(box(cx, 10.95, 5.6, 0.72, 'Evaluate fitness of X; record the best X`best`',
                 BLUE_F, BLUE_L, 13, text_color='#28456B'))
    s.append(box(cx, 9.85, 2.7, 1.06, 't < T ?', ORANGE_F, ORANGE_L, 14, shape='diamond',
                 text_color='#8A5A00'))
    s.append(box(cx, 8.85, 4.4, 0.72, 'Compute the time ratio t / T', BLUE_F, BLUE_L, 13,
                 text_color='#28456B'))
    s.append(box(cx, 7.68, 3.7, 1.2, 'exploration or\nexploitation ?', ORANGE_F, ORANGE_L, 13,
                 shape='diamond', text_color='#8A5A00'))
    s.append(box(2.5, 6.2, 3.5, 1.2, 'Hunting strategy\n(searching / consuming /\nattacking the snake)',
                 RED_F, RED_L, 12.5, text_color='#7A2E2A'))
    s.append(box(6.5, 6.2, 3.5, 1.2, 'Escape strategy\n(C`1` camouflage /\nC`2` flee with Lévy flight)',
                 RED_F, RED_L, 12.5, text_color='#7A2E2A'))
    s.append(box(cx, 4.9, 6.8, 0.72, 'Lens opposition-based learning on the inferior birds (S2)',
                 GREEN_F, GREEN_L, 12.5, text_color='#2E5A2E'))
    s.append(box(cx, 3.95, 6.8, 0.72, 'Adaptive Cauchy–Gauss mutation on X`best` (S3)',
                 GREEN_F, GREEN_L, 12.5, text_color='#2E5A2E'))
    s.append(box(cx, 3.0, 6.8, 0.72, 'Greedy selection; update X and X`best`; t = t + 1',
                 BLUE_F, BLUE_L, 12.5, text_color='#28456B'))
    s.append(box(cx, 1.35, 4.6, 0.72, 'Output the best solution X`best`', GREEN_F, GREEN_L, 14,
                 rounding=0.14, text_color='#2E5A2E'))

    # --- connectors --------------------------------------------------------
    c = s.append
    c(connector([(cx, 12.65), (cx, 12.43)]))                       # start -> init
    c(connector([(cx, 11.47), (cx, 11.31)]))                       # init -> eval
    c(connector([(cx, 10.59), (cx, 10.38)]))                       # eval -> t<T
    c(connector([(cx, 9.32), (cx, 9.21)]))                         # t<T -> compute (Yes)
    c(connector([(cx, 8.49), (cx, 8.28)]))                         # compute -> explore/exploit
    c(connector([(2.8, 7.68), (2.5, 7.68), (2.5, 6.8)]))           # -> hunting (explore)
    c(connector([(6.2, 7.68), (6.5, 7.68), (6.5, 6.8)]))           # -> escape (exploit)
    c(connector([(2.5, 5.6), (2.5, 5.36), (4.35, 5.36), (4.35, 5.26)]))  # hunting -> lens
    c(connector([(6.5, 5.6), (6.5, 5.36), (4.65, 5.36), (4.65, 5.26)]))  # escape -> lens
    c(connector([(cx, 4.54), (cx, 4.31)]))                         # lens -> mutation
    c(connector([(cx, 3.59), (cx, 3.36)]))                         # mutation -> greedy
    # next-iteration loop (right, blue)
    c(connector([(7.9, 3.0), (8.55, 3.0), (8.55, 9.85), (5.85, 9.85)],
                color='#2E5A88', lw_pt=1.2))
    # No loop (left) -> output
    c(connector([(3.15, 9.85), (0.75, 9.85), (0.75, 1.35), (2.3, 1.35)],
                color='#4A4A4A', lw_pt=1.2))

    # --- edge labels -------------------------------------------------------
    c(label(1.55, 10.12, 0.7, 0.3, 'No', 12.5, color='#C0392B'))
    c(label(4.82, 9.15, 0.7, 0.3, 'Yes', 12.5, color='#2E7D32', align=0))
    c(label(3.05, 7.05, 1.1, 0.3, 'explore', 12, color=DARK))
    c(label(5.95, 7.05, 1.1, 0.3, 'exploit', 12, color=DARK))
    c(label(8.9, 6.5, 1.4, 0.3, 'next iteration', 12, color='#2E5A88', angle=1.5707963))
    return s


# ============================================================================
# PAGE 2 -- Metaheuristic classification
# ============================================================================
COLS = [
    dict(name='Mathematically-based\nAlgorithms', hfill='#EBB731', bfill='#F4D571',
         border='#C89A1E', items=[
             'Sine Cosine Algorithm (SCA)',
             'Arithmetic Optimization Algorithm (AOA)',
             'Quasi-random Fractal Search (QRFS)',
             'Weighted Average Algorithm (WAA)',
             'Triangulation Topology Aggregation Optimizer (TTAO)',
             'Exponential-Trigonometric Optimization Algorithm (ETOA)']),
    dict(name='Evolutionary-based\nAlgorithms', hfill='#4FB6A1', bfill='#82CBBB',
         border='#3B9684', items=[
             'Genetic Algorithms (GA)',
             'Evolution Strategy (ES)',
             'Differential Evolution (DE)',
             'Covariance Matrix Adaptation Evolution Strategy (CMA-ES)',
             'Human Evolutionary Optimization Algorithm (HEOA)',
             'Chaotic Evolution Optimization (CEO)']),
    dict(name='Swarm-based\nAlgorithms', hfill='#3DBFDA', bfill='#74D2E6',
         border='#2896B8', items=[
             'Particle Swarm Optimization (PSO)',
             'Ant Colony Optimization (ACO)',
             'Grey Wolf Optimizer (GWO)',
             'Artificial Lemming Algorithm (ALA)',
             'Crayfish Optimization Algorithm (COA)',
             'Dwarf Mongoose Optimization (DMO)',
             'Sled Dog Optimizer (SDO)',
             'Slime Mould Algorithm (SMA)',
             'Arctic Puffin Optimization (APO)',
             'Genghis Khan Shark Optimizer (GKSO)',
             'Prairie Dog Optimization Algorithm (PDOA)',
             'Secretary Bird Optimization Algorithm (SBOA)']),
    dict(name='Physics-based\nAlgorithms', hfill='#9EC3C1', bfill='#BAD4D2',
         border='#7BA6A3', items=[
             'Multi-Verse Optimizer (MVO)',
             "Fick's Law Algorithm (FLA)",
             'Snow Ablation Optimization (SAO)',
             'Polar Lights Optimizer (PLO)',
             'Special Relativity Search (SRS)',
             'Mirage Search Optimization (MSO)',
             'Kepler Optimization Algorithm (KOA)']),
]

P2_W = 11.8
COL_CX = [1.7, 4.5, 7.3, 10.1]
BOX_W = 2.42
FRAME_W = 2.64
ITEM_PT = 11.0
ITEM_MAXCHARS = 23
LINE_H = ITEM_PT * PT * 1.32
BOX_PAD = 0.16
ITEM_GAP = 0.14
DASH_TOP = 9.98
FIRST_TOP = 9.80          # top edge of first item box (all columns aligned)


def page2_shapes():
    _id[0] = 0
    s = []
    # --- title bar ---------------------------------------------------------
    title_cy = 11.85
    s.append(box(P2_W / 2, title_cy, 9.8, 0.9, 'Metaheuristic algorithms',
                 '#E8E8E8', '#BFBFBF', 28, rounding=0.05, text_color='#1A1A1A'))
    # --- headers + arrows + columns ---------------------------------------
    head_cy = 10.62
    head_h = 0.72
    frame_bottoms = []
    for col, cxx in zip(COLS, COL_CX):
        # arrow from title bottom down to header top
        s.append(connector([(cxx, title_cy - 0.45), (cxx, head_cy + head_h / 2 + 0.02)],
                            color='#2B2B2B', lw_pt=1.4, end_arrow=4))
        # header
        s.append(box(cxx, head_cy, BOX_W + 0.12, head_h, col['name'],
                     col['hfill'], col['border'], 14.5, rounding=0.05, lw_pt=1.2,
                     text_color='#1A1A1A'))
        # items
        top = FIRST_TOP
        for it in col['items']:
            lines = wrap(it, ITEM_MAXCHARS)
            bh = round(len(lines) * LINE_H + BOX_PAD, 4)
            cyy = top - bh / 2
            s.append(box(cxx, cyy, BOX_W, bh, '\n'.join(lines),
                         col['bfill'], col['border'], ITEM_PT, rounding=0.05,
                         lw_pt=1.0, text_color='#123033'))
            top = cyy - bh / 2 - ITEM_GAP
        frame_bottoms.append(top + ITEM_GAP)  # bottom edge of last box
    # dashed frames (drawn last so they sit behind conceptually is fine either way)
    for col, cxx, fb in zip(COLS, COL_CX, frame_bottoms):
        fcy = (DASH_TOP + (fb - BOX_PAD)) / 2
        fh = DASH_TOP - (fb - BOX_PAD)
        s.append(dashed_frame(cxx, fcy, FRAME_W, fh, col['border'], lw_pt=1.1))
    return s, P2_W, 12.6


# ============================================================================
# Assemble the package
# ============================================================================

def page_content(shapes):
    return (
        "<?xml version='1.0' encoding='utf-8' ?>\n"
        '<PageContents xmlns="http://schemas.microsoft.com/office/visio/2012/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xml:space="preserve"><Shapes>'
        + ''.join(shapes) + '</Shapes></PageContents>'
    )


def pages_xml(pages):
    """pages: list of dict(id,name,w,h,rid)."""
    out = ["<?xml version='1.0' encoding='utf-8' ?>\n",
           '<Pages xmlns="http://schemas.microsoft.com/office/visio/2012/main" '
           'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
           'xml:space="preserve">']
    for p in pages:
        vscale = round(min(10.0 / p["w"], 7.2 / p["h"]), 3)
        out.append(
            f'<Page ID="{p["id"]}" NameU="{esc(p["name"])}" Name="{esc(p["name"])}" '
            f'ViewScale="{vscale}" ViewCenterX="{p["w"]/2:.4f}" ViewCenterY="{p["h"]/2:.4f}">'
            f'<PageSheet LineStyle="0" FillStyle="0" TextStyle="0">'
            f'{cell("PageWidth", round(p["w"],4))}{cell("PageHeight", round(p["h"],4))}'
            f'{cell("ShdwOffsetX", 0.1181)}{cell("ShdwOffsetY", -0.1181)}'
            f'{cell("PageScale", 1)}{cell("DrawingScale", 1)}'
            f'{cell("DrawingSizeType", 3)}{cell("DrawingScaleType", 0)}'
            f'{cell("InhibitSnap", 0)}{cell("PageLockReplace", 0)}'
            f'{cell("PageLockDuplicate", 0)}{cell("UIVisibility", 0)}'
            f'{cell("ShdwType", 0)}{cell("ShdwObliqueAngle", 0)}{cell("ShdwScaleFactor", 1)}'
            f'{cell("DrawingResizeType", 2)}{cell("PageShapeSplit", 1)}'
            f'</PageSheet><Rel r:id="{p["rid"]}"/></Page>')
    out.append('</Pages>')
    return ''.join(out)


PAGES_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="page1.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.microsoft.com/visio/2010/relationships/page" Target="page2.xml"/>'
    '</Relationships>'
)

CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="emf" ContentType="image/x-emf"/>'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/visio/document.xml" ContentType="application/vnd.ms-visio.drawing.main+xml"/>'
    '<Override PartName="/visio/masters/masters.xml" ContentType="application/vnd.ms-visio.masters+xml"/>'
    '<Override PartName="/visio/masters/master1.xml" ContentType="application/vnd.ms-visio.master+xml"/>'
    '<Override PartName="/visio/pages/pages.xml" ContentType="application/vnd.ms-visio.pages+xml"/>'
    '<Override PartName="/visio/pages/page1.xml" ContentType="application/vnd.ms-visio.page+xml"/>'
    '<Override PartName="/visio/pages/page2.xml" ContentType="application/vnd.ms-visio.page+xml"/>'
    '<Override PartName="/visio/windows.xml" ContentType="application/vnd.ms-visio.windows+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
    '<Override PartName="/docProps/custom.xml" ContentType="application/vnd.openxmlformats-officedocument.custom-properties+xml"/>'
    '</Types>'
)

APP_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
    'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
    '<Template></Template><Application>Microsoft Visio</Application><ScaleCrop>false</ScaleCrop>'
    '<HeadingPairs><vt:vector size="4" baseType="variant">'
    '<vt:variant><vt:lpstr>Pages</vt:lpstr></vt:variant><vt:variant><vt:i4>2</vt:i4></vt:variant>'
    '<vt:variant><vt:lpstr>Masters</vt:lpstr></vt:variant><vt:variant><vt:i4>1</vt:i4></vt:variant>'
    '</vt:vector></HeadingPairs>'
    '<TitlesOfParts><vt:vector size="3" baseType="lpstr">'
    '<vt:lpstr>MSSBOA Flowchart</vt:lpstr><vt:lpstr>Algorithm Classification</vt:lpstr>'
    '<vt:lpstr>Dynamic connector</vt:lpstr></vt:vector></TitlesOfParts>'
    '<Manager></Manager><Company></Company><LinksUpToDate>false</LinksUpToDate>'
    '<SharedDoc>false</SharedDoc><HyperlinkBase></HyperlinkBase>'
    '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>'
)


def add_facename(document_xml):
    yahei = ('<FaceName NameU="Microsoft YaHei" UnicodeRanges="-1610612545 1073750107 9 0" '
             'CharSets="-2147483648 0" Panose="2 11 5 3 2 2 4 2 2 4" Flags="325"/>')
    return document_xml.replace('</FaceNames>', yahei + '</FaceNames>', 1)


def build():
    if os.path.isdir(BUILD):
        shutil.rmtree(BUILD)
    os.makedirs(BUILD)
    # 1. extract template boilerplate
    with zipfile.ZipFile(TEMPLATE_VSDX) as z:
        z.extractall(BUILD)
    # remove template's page content + per-page rels (we author our own)
    for rel in [os.path.join(BUILD, 'visio/pages/_rels/page1.xml.rels')]:
        if os.path.exists(rel):
            os.remove(rel)

    def write(rel_path, content):
        full = os.path.join(BUILD, rel_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)

    # 2. content types, app props
    write('[Content_Types].xml', CONTENT_TYPES)
    write('docProps/app.xml', APP_XML)

    # 3. document.xml with the Microsoft YaHei face registered
    with open(os.path.join(BUILD, 'visio/document.xml'), encoding='utf-8') as f:
        doc = f.read()
    write('visio/document.xml', add_facename(doc))

    # 4. pages
    p1 = page1_shapes()
    p2, p2w, p2h = page2_shapes()
    write('visio/pages/page1.xml', page_content(p1))
    write('visio/pages/page2.xml', page_content(p2))
    write('visio/pages/pages.xml', pages_xml([
        dict(id=0, name='MSSBOA Flowchart', w=9.0, h=13.6, rid='rId1'),
        dict(id=1, name='Algorithm Classification', w=p2w, h=p2h, rid='rId2'),
    ]))
    write('visio/pages/_rels/pages.xml.rels', PAGES_RELS)

    # 5. zip it back up ([Content_Types].xml first, stored/deflate)
    if os.path.exists(OUT_VSDX):
        os.remove(OUT_VSDX)
    files = []
    for root, _dirs, fnames in os.walk(BUILD):
        for fn in fnames:
            full = os.path.join(root, fn)
            arc = os.path.relpath(full, BUILD).replace(os.sep, '/')
            files.append((arc, full))
    files.sort(key=lambda a: (a[0] != '[Content_Types].xml', a[0]))
    with zipfile.ZipFile(OUT_VSDX, 'w', zipfile.ZIP_DEFLATED) as z:
        for arc, full in files:
            z.write(full, arc)
    shutil.rmtree(BUILD)  # drop the intermediate unzipped tree
    print(f'Wrote {OUT_VSDX}')
    print(f'  page1 shapes: {len(p1)}   page2 shapes: {len(p2)}')


if __name__ == '__main__':
    build()
