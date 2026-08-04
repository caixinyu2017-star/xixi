# -*- coding: utf-8 -*-
"""Figure style and diagram primitives, following Nature Portfolio conventions.

The house rules a Nature figure editor enforces, encoded once:

*   A single sans-serif family throughout, mathematics included. Liberation
    Sans is metrically identical to Arial, which is what the guidelines ask
    for; ``mathtext.fontset = "custom"`` keeps symbols in the same family
    rather than dropping into Computer Modern.
*   Three type sizes only: 7 pt for axis titles and box labels, 6 pt for tick
    labels and annotation, 8 pt bold lower case for panel letters. Nothing
    below 6 pt.
*   Left and bottom spines only, outward ticks, no gridlines. Every mark on
    the page carries information.
*   The Okabe and Ito colourblind-safe palette for data; ink, grey and a
    single accent for schematics.
*   Direct labelling in preference to a legend.
*   Vector PDF and SVG alongside a 600 dpi PNG, the raster being only for
    placement inside the Word file.

**Figures are constructed at their true final size.** ``savefig`` is never
allowed to crop: a figure declared 132 mm wide is written 132 mm wide, and
axes are positioned in millimetres from the lower-left corner. This is what
makes the point sizes above mean anything. Cropping to the ink, which is
matplotlib's convenient default, silently rescales the figure when Word
stretches it back to the column width, and every stated type size becomes a
fiction.
"""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

# --------------------------------------------------------------------- sizes
MM = 1 / 25.4
SINGLE = 89.0             # Nature single column, mm
ONE_HALF = 120.0          # Nature 1.5 column, mm
DOUBLE = 183.0            # Nature double column, mm
TEXT = 132.0              # the width at which the Word file places a figure

# ------------------------------------------------------------------ palette
# Okabe, M.; Ito, K. Color Universal Design (2008). Legible under the three
# common forms of colour vision deficiency and in greyscale.
BLACK = "#000000"
ORANGE = "#E69F00"
SKY = "#56B4E9"
GREEN = "#009E73"
YELLOW = "#F0E442"
BLUE = "#0072B2"
VERMILION = "#D55E00"
PURPLE = "#CC79A7"

INK = "#1A1A1A"           # text and axes: near-black, never pure black at 6 pt
GREY = "#767676"          # secondary rules, conditions, reference lines
FAINT = "#BFBFBF"
ACCENT = VERMILION        # the one accent, shared by schematics and data

CYCLE = [BLUE, VERMILION, GREEN, ORANGE, PURPLE, SKY, YELLOW]


def tint(hexcol, f, bg="#FFFFFF"):
    """A pre-blended opaque tint of ``hexcol`` at fraction ``f`` over paper.

    Nothing transparent is allowed to reach a deliverable. Alpha writes a
    transparency group into the PDF, which Word's EMF conversion flattens
    unpredictably and which some print workflows rasterise, so a confidence
    band drawn with alpha can arrive at the journal as a grey box. The blend
    is therefore done once, here, in RGB.
    """
    import matplotlib.colors as _mc
    import numpy as _np
    c = _np.array(_mc.to_rgb(hexcol))
    b = _np.array(_mc.to_rgb(bg))
    return _mc.to_hex(f * c + (1 - f) * b)


BAND = {c: tint(c, 0.30) for c in (BLUE, VERMILION, GREEN, ORANGE)}
SHADE = "#ECECEC"         # a neutral opaque wash for a reference interval

# ------------------------------------------------------------------- type
PT_LABEL = 7.0            # axis titles, box labels
PT_TICK = 6.0             # tick labels, annotation, edge labels
PT_PANEL = 8.0            # panel letters, bold

SANS = ["Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"]

RC = {
    "font.family": "sans-serif",
    "font.sans-serif": SANS,
    "font.size": PT_LABEL,
    "axes.labelsize": PT_LABEL,
    "axes.titlesize": PT_LABEL,
    "xtick.labelsize": PT_TICK,
    "ytick.labelsize": PT_TICK,
    "legend.fontsize": PT_TICK,

    # mathematics in the figure's own family, not in Computer Modern
    "mathtext.fontset": "custom",
    "mathtext.rm": "Liberation Sans",
    "mathtext.it": "Liberation Sans:italic",
    "mathtext.bf": "Liberation Sans:bold",
    "mathtext.cal": "Liberation Sans:italic",
    "mathtext.sf": "Liberation Sans",
    "mathtext.tt": "DejaVu Sans Mono",
    "mathtext.default": "it",

    "axes.labelcolor": INK,
    "axes.edgecolor": INK,
    "text.color": INK,
    "xtick.color": INK,
    "ytick.color": INK,

    "axes.linewidth": 0.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "axes.axisbelow": True,
    "axes.titlepad": 3.0,
    "axes.labelpad": 2.0,

    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 2.0,
    "ytick.major.size": 2.0,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.pad": 1.8,
    "ytick.major.pad": 1.8,
    "xtick.minor.visible": False,
    "ytick.minor.visible": False,

    "lines.linewidth": 1.0,
    "lines.markersize": 3.0,
    "lines.solid_capstyle": "round",
    "patch.linewidth": 0.5,

    "legend.frameon": False,
    "legend.handlelength": 1.4,
    "legend.handletextpad": 0.5,
    "legend.labelspacing": 0.3,
    "legend.borderaxespad": 0.2,

    "figure.dpi": 600,
    "savefig.dpi": 1000,   # MDPI line-art minimum
    "savefig.bbox": None,      # never crop: the declared size is the size
    "savefig.pad_inches": 0.0,
    "savefig.transparent": False,
    "pdf.fonttype": 42,        # embed TrueType so the text stays selectable
    "ps.fonttype": 42,
    "svg.fonttype": "none",    # keep text as text in the SVG
    "axes.unicode_minus": True,
}


def use():
    """Install the style. Call once at import time in a figure module."""
    plt.rcParams.update(RC)


# ===========================================================================
# Construction in millimetres
# ===========================================================================
def figure(width=TEXT, height=60.0):
    """A figure of exactly ``width`` by ``height`` millimetres."""
    return plt.figure(figsize=(width * MM, height * MM))


def axes_mm(fig, x, y, w, h):
    """Axes placed at (x, y) with size (w, h), all in millimetres measured
    from the lower-left corner of the figure."""
    W = fig.get_figwidth() / MM
    H = fig.get_figheight() / MM
    return fig.add_axes([x / W, y / H, w / W, h / H])


def row(fig, n, left, bottom, height, gutter, right=3.0):
    """``n`` equal panels in a row, laid out in millimetres."""
    W = fig.get_figwidth() / MM
    w = (W - left - right - (n - 1) * gutter) / n
    return [axes_mm(fig, left + i * (w + gutter), bottom, w, height)
            for i in range(n)]


def panels(fig, items, gap=1.2):
    """Bold lower-case panel letters, placed from the measured extent of each
    panel rather than from a hand-tuned offset.

    Each letter sits flush with the leftmost ink of its own panel — which is
    the y-axis title where there is one and the spine where there is not — and
    every letter in a row shares one baseline. Nature sets these without
    parentheses and without a full stop.
    """
    fig.draw_without_rendering()
    inv = fig.transFigure.inverted()
    r = fig.canvas.get_renderer()
    meas = [(ax, letter,
             ax.get_tightbbox(r).transformed(inv),
             round(ax.get_position().y1, 3)) for ax, letter in items]
    tops = {}
    for _, _, bb, key in meas:
        tops[key] = max(tops.get(key, 0.0), bb.y1)
    dy = gap / (fig.get_figheight() / MM)
    for _, letter, bb, key in meas:
        fig.text(bb.x0, tops[key] + dy, letter, fontsize=PT_PANEL,
                 fontweight="bold", va="bottom", ha="left", color=INK)


def snap(ax, x=True, y=True):
    """Trim each spine to its outermost tick, so the axis states the range the
    data occupy instead of running past it into empty paper."""
    if y:
        t = [v for v in ax.get_yticks() if ax.get_ylim()[0] <= v <= ax.get_ylim()[1]]
        if t:
            ax.spines["left"].set_bounds(min(t), max(t))
    if x:
        t = [v for v in ax.get_xticks() if ax.get_xlim()[0] <= v <= ax.get_xlim()[1]]
        if t:
            ax.spines["bottom"].set_bounds(min(t), max(t))


def band(ax, x, lo, hi, color=BLUE, z=1.5, edge=0.35):
    """A confidence band: an opaque tint with its limits stroked as hairlines.

    The hairlines are what carry the interval in greyscale, where a 30 percent
    tint of any of these hues collapses to about 1.6:1 against paper.
    """
    ax.fill_between(x, lo, hi, facecolor=BAND[color], edgecolor="none", lw=0,
                    zorder=z)
    if edge:
        ax.plot(x, lo, color=color, lw=edge, zorder=z + 0.1)
        ax.plot(x, hi, color=color, lw=edge, zorder=z + 0.1)


def num(v, d=3):
    """A number with a typographic minus, which is what the journal sets and
    what matplotlib applies only to tick labels."""
    return ("%.*f" % (d, v)).replace("-", "−")


def zeroline(ax, y=0.0, **kw):
    """A reference line at zero, thinner and greyer than the data."""
    kw.setdefault("color", GREY)
    kw.setdefault("lw", 0.5)
    kw.setdefault("ls", (0, (2.6, 1.8)))
    kw.setdefault("zorder", 0.5)
    ax.axhline(y, **kw)


LADDER = {PT_TICK, PT_LABEL, PT_PANEL}


def _check(fig):
    """The two contracts that make every other number in this module mean
    something, asserted before anything is written to disk."""
    import matplotlib.text as _mt
    w = fig.get_figwidth() / MM
    assert abs(w - TEXT) < 0.05, "figure is %.2f mm wide, not %.2f" % (w, TEXT)
    bad = sorted({t.get_fontsize() for t in fig.findobj(_mt.Text)
                  if t.get_text().strip()} - LADDER)
    assert not bad, "type sizes off the ladder %s: %s" % (sorted(LADDER), bad)


def save(fig, path_stem, formats=("png", "pdf", "svg")):
    """Write the figure once per format at its declared size."""
    _check(fig)
    os.makedirs(os.path.dirname(path_stem), exist_ok=True)
    out = []
    for ext in formats:
        p = "%s.%s" % (path_stem, ext)
        fig.savefig(p, bbox_inches=None, pad_inches=0.0)
        out.append(p)
    plt.close(fig)
    return out


# ===========================================================================
# Conceptual-framework diagrams
# ===========================================================================
# A framework diagram encodes its grammar in line style rather than in
# decoration, so that the structure is visible before a single label is read:
#
#     solid arrow            a causal path the model estimates
#     grey line, disc end    a condition acting on the path it lands on
#     dashed arrow           a lagged or feedback path
#     double stroke          a delay or a gate on the path it crosses
#
# Every box is white with a hairline stroke; the two constructs that anchor
# the argument are distinguished by stroke weight, not by fill, because a fill
# is a second visual channel spent on something a weight already says.
#
# The canvas is one grid unit to the millimetre with an equal aspect, so a
# coordinate in a layout is a physical position on the printed page, and every
# edge endpoint is taken from ``anchor`` rather than typed as a literal.

W_FOCAL = 1.0             # stroke of a focal construct
W_PLAIN = 0.6             # stroke of an ordinary construct
W_PATH = 1.0              # an estimated path
W_SUB = 0.7               # a secondary estimated path
W_COND = 0.5              # a conditioning path
W_FEED = 0.7              # a feedback path

STAND = 1.5               # standoff of an arrow from its box, in points
DASH = (0, (2.4, 1.6))

_HALO = dict(facecolor="white", edgecolor="none", pad=0.8)


def canvas(width=TEXT, height=90.0):
    """A blank diagram canvas: one grid unit to the millimetre, filling the
    whole figure, with an equal aspect so circles are circles."""
    fig = figure(width, height)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect("equal")
    ax.set_axis_off()
    return fig, ax


def dbox(ax, cx, cy, w, h, lines, focal=False, edge=None, size=PT_LABEL,
         z=3):
    """A construct box: white, hairline, centred label. Focal constructs carry
    a heavier stroke; conditions carry a grey one."""
    lw = W_FOCAL if focal else W_PLAIN
    ec = edge if edge is not None else (INK if focal else GREY)
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0,rounding_size=1.0",
        facecolor="white", edgecolor=ec, linewidth=lw, zorder=z))
    ax.text(cx, cy, "\n".join(lines), ha="center", va="center",
            fontsize=size, color=INK, zorder=z + 1, linespacing=1.30)
    return dict(cx=cx, cy=cy, w=w, h=h,
                l=cx - w / 2, r=cx + w / 2, t=cy + h / 2, b=cy - h / 2)


def anchor(box, side, frac=0.5):
    """A point on the boundary of ``box``. ``frac`` runs left to right on the
    horizontal sides and bottom to top on the vertical sides.

    Every edge in a diagram starts and ends at one of these, so moving a box
    moves its edges with it and no endpoint is ever a hand-typed literal.
    """
    if side == "l":
        return (box["l"], box["b"] + frac * box["h"])
    if side == "r":
        return (box["r"], box["b"] + frac * box["h"])
    if side == "t":
        return (box["l"] + frac * box["w"], box["t"])
    if side == "b":
        return (box["l"] + frac * box["w"], box["b"])
    raise ValueError("side must be one of l, r, t, b")


def mid(p0, p1, dx=0.0, dy=0.0):
    """The midpoint of an edge, optionally displaced, for its label."""
    return ((p0[0] + p1[0]) / 2 + dx, (p0[1] + p1[1]) / 2 + dy)


def dpath(ax, p0, p1, color=INK, lw=W_PATH, rad=0.0, ls="-", head=True, z=2,
          shrink=STAND):
    """An estimated path. The standoff is uniform, so no arrow ever touches or
    enters the box it points at."""
    ax.add_patch(FancyArrowPatch(
        p0, p1,
        arrowstyle="-|>,head_length=3.0,head_width=1.9" if head else "-",
        mutation_scale=1.0, linewidth=lw, linestyle=ls, color=color,
        shrinkA=shrink, shrinkB=shrink, zorder=z,
        connectionstyle="arc3,rad=%.3f" % rad))


def dcond(ax, p0, p1, color=GREY, lw=W_COND, rad=0.0, z=2, r=0.6,
          shrink=STAND):
    """A conditioning path: it lands on another path and carries a filled disc
    instead of an arrowhead, which is the convention that separates a
    moderator from a mediator at a glance."""
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle="-", mutation_scale=1.0, linewidth=lw,
        color=color, shrinkA=shrink, shrinkB=0.0, zorder=z,
        connectionstyle="arc3,rad=%.3f" % rad))
    ax.add_patch(Circle(p1, r, facecolor=color, edgecolor="none", zorder=z + 1))


def dgate(ax, x, y, angle=0.0, color=ACCENT, lw=0.8, half=2.0, gap=1.1):
    """A double stroke across a path: a gate, or a delay. ``angle`` is the
    direction of the strokes, so a vertical path takes ``angle=0``."""
    import numpy as _np
    a = _np.deg2rad(angle)
    ux, uy = _np.cos(a), _np.sin(a)           # along the strokes
    vx, vy = -uy, ux                          # along the path
    for s in (-gap / 2, gap / 2):
        ax.plot([x + vx * s - ux * half, x + vx * s + ux * half],
                [y + vy * s - uy * half, y + vy * s + uy * half],
                color=color, lw=lw, solid_capstyle="butt", zorder=5)


def junction(ax, x, y, color=ACCENT, r=0.7, z=5):
    """Where two paths merge into one."""
    ax.add_patch(Circle((x, y), r, facecolor=color, edgecolor="none",
                        zorder=z))


def hlabel(ax, x, y, text, color=INK, size=PT_TICK, ha="center", va="center",
           halo=True, style="normal"):
    """A label set on its own path, haloed so the line does not run through
    the glyphs."""
    return ax.text(x, y, text, ha=ha, va=va, fontsize=size, color=color,
                   zorder=6, fontstyle=style,
                   bbox=dict(**_HALO) if halo else None)


def keystrip(ax, y, cols, items, size=PT_TICK, dx=4.0, pad=1.6):
    """A key stating the line grammar, set on a fixed column grid beneath the
    diagram. A framework whose grammar a referee has to infer is a framework
    that gets misread."""
    for x, (kind, text) in zip(cols, items):
        if kind == "solid":
            ax.add_patch(FancyArrowPatch(
                (x, y), (x + dx, y),
                arrowstyle="-|>,head_length=3.0,head_width=1.9",
                mutation_scale=1.0, linewidth=W_PATH, color=INK,
                shrinkA=0, shrinkB=0, zorder=3))
        elif kind == "dashed":
            ax.add_patch(FancyArrowPatch(
                (x, y), (x + dx, y),
                arrowstyle="-|>,head_length=3.0,head_width=1.9",
                mutation_scale=1.0, linewidth=W_FEED, color=ACCENT,
                linestyle=DASH, shrinkA=0, shrinkB=0, zorder=3))
        elif kind == "cond":
            ax.plot([x, x + dx], [y - 0.9, y + 0.6], color=GREY, lw=W_COND,
                    zorder=3)
            ax.add_patch(Circle((x + dx, y + 0.6), 0.6, facecolor=GREY,
                                edgecolor="none", zorder=4))
        elif kind == "gate":
            ax.plot([x, x + dx], [y, y], color=ACCENT, lw=W_FEED, zorder=3)
            dgate(ax, x + dx / 2, y, angle=90, half=1.3, gap=1.0)
        ax.text(x + dx + pad, y, text, fontsize=size, color=INK,
                ha="left", va="center", zorder=3)
