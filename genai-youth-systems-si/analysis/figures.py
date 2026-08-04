# -*- coding: utf-8 -*-
"""The three figures reported in the manuscript.

Drawn to the Nature Portfolio conventions encoded in ``natureplot``: a single
sans-serif family at fixed print sizes, bold lower-case panel letters, left and
bottom spines only with outward ticks, the Okabe and Ito colourblind-safe
palette, direct labelling in place of legends, and vector output alongside the
raster used for placement in the Word file.

Every figure is built at the width at which the Word file places it, and every
panel is positioned in millimetres, so a 6 pt tick label is 6 pt on the printed
page rather than 6 pt multiplied by whatever scale factor a cropped bounding
box happened to imply.

Two further habits are borrowed from the journal. Where a figure carries a
quantitative claim the number is written into the panel, so a reader takes the
result from the figure rather than from the caption. And where an effect is
plotted against a moderator the observed distribution of that moderator is
shown underneath it, so the reader can see over what range the estimate is
supported.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd

import natureplot as N

N.use()

import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
os.makedirs(FIG, exist_ok=True)


def load():
    with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
        return json.load(fh)


def _rug(ax, values, frac=0.075, color=N.FAINT):
    """A shallow density strip along the foot of the axes showing the support
    of the moderator. It occupies the bottom ``frac`` of the panel and is drawn
    beneath everything else."""
    lo, hi = ax.get_ylim()
    span = hi - lo
    ax.set_ylim(lo - frac * span * 1.35, hi)
    lo2, hi2 = ax.get_ylim()
    xs = np.linspace(*ax.get_xlim(), 160)
    kde = np.histogram(values, bins=xs)[0].astype(float)
    kde = np.convolve(kde, np.ones(9) / 9.0, mode="same")
    if kde.max() > 0:
        kde = kde / kde.max()
    base = lo2 + 0.012 * (hi2 - lo2)
    ax.fill_between(xs[:-1], base, base + kde * frac * span,
                    color=color, lw=0, zorder=0.2)


# ===========================================================================
def figure1_framework():
    """The conceptual framework.

    The layout is a construction rather than a drawing. The canvas is one grid
    unit to the millimetre; every box is placed on a five-row grid, and every
    edge begins and ends at a named point on a box boundary, so no endpoint is
    a hand-typed coordinate and no arrow touches the box it points at.

    The grammar is carried by line style. A solid arrow is a path the model
    estimates; a grey line ending in a disc on another path is a condition
    governing that path; a dashed arrow is the lagged return; and the double
    stroke is the one-year delay on that return. The two return arcs merge
    onto a single bus above the diagram, because they act on the same driver,
    and the loop they close is named once rather than labelled twice.

    The layout has no edge crossings.
    """
    W, H = N.TEXT, 87.0
    fig, ax = N.canvas(W, H)

    Y_PATH, Y_ROU, Y_TRA = 45.0, 59.0, 71.0
    Y_COND, Y_BUS, Y_KEY = 19.0, 82.0, 3.5

    gen = N.dbox(ax, 21, Y_PATH, 34, 13, ["Generative AI", "adoption"],
                 focal=True)
    you = N.dbox(ax, 111, Y_PATH, 34, 13, ["Youth employment", "share"],
                 focal=True)
    rou = N.dbox(ax, 66, Y_ROU, 34, 9, ["Routine task base"], edge=N.INK)
    tra = N.dbox(ax, 66, Y_TRA, 34, 9, ["Training investment"], edge=N.INK)
    olc = N.dbox(ax, 30, Y_COND, 46, 10,
                 ["Organizational learning", "capability"])
    rlc = N.dbox(ax, 88, Y_COND, 42, 10, ["Relative labor cost"])

    # ---- the direct path -------------------------------------------------
    N.dpath(ax, N.anchor(gen, "r"), N.anchor(you, "l"))
    N.hlabel(ax, 85.0, Y_PATH, "H1 (−)")

    # ---- the two mediating channels, stacked above the direct path -------
    for src_frac, box, dst_frac, lab in (
            (0.529, tra, 0.389, "H2 (−)"),
            (0.794, rou, 0.389, "H3 (−)")):
        a, b = N.anchor(gen, "t", src_frac), N.anchor(box, "l", dst_frac)
        N.dpath(ax, a, b, lw=N.W_SUB)
        N.hlabel(ax, *N.mid(a, b), lab)
    for box, src_frac, side, dst_frac in (
            (tra, 0.389, "t", 0.294),
            (rou, 0.389, "l", 0.654)):
        a, b = N.anchor(box, "r", src_frac), N.anchor(you, side, dst_frac)
        N.dpath(ax, a, b, lw=N.W_SUB)
        N.hlabel(ax, *N.mid(a, b), "(+)")

    # ---- the two boundary conditions, entering the clear lower half ------
    for box, frac, x, lab in ((olc, 0.891, 48.0, "H4a (+)"),
                              (rlc, 0.214, 76.0, "H4b (−)")):
        N.dcond(ax, N.anchor(box, "t", frac), (x, Y_PATH))
        ax.text(x + 2.0, 34.0, lab, fontsize=N.PT_TICK, color=N.GREY,
                ha="left", va="center")

    # ---- the return arcs, merging onto one bus ---------------------------
    for box, frac in ((you, 0.706), (tra, 0.324)):
        p = N.anchor(box, "t", frac)
        ax.plot([p[0], p[0]], [p[1] + 0.6, Y_BUS], color=N.ACCENT,
                lw=N.W_FEED, ls=N.DASH, zorder=2)
    xy = N.anchor(you, "t", 0.706)[0]
    xt = N.anchor(tra, "t", 0.324)[0]
    ax.plot([xy, 8.0], [Y_BUS, Y_BUS], color=N.ACCENT, lw=N.W_FEED,
            ls=N.DASH, zorder=2)
    N.dpath(ax, (48.0, Y_BUS), (42.0, Y_BUS), color=N.ACCENT, lw=N.W_FEED,
            shrink=0.0)                       # the direction of travel
    N.junction(ax, xt, Y_BUS)
    N.dpath(ax, (8.0, Y_BUS), N.anchor(gen, "t", 0.118), color=N.ACCENT,
            lw=N.W_FEED, ls=N.DASH, shrink=0.0)
    N.dgate(ax, 8.0, 60.0, angle=0.0)
    N.hlabel(ax, 95.0, Y_BUS, "H5 (−)", color=N.ACCENT)
    ax.text(20.0, Y_BUS + 1.4, "reinforcing loop R1", ha="left", va="bottom",
            fontsize=N.PT_TICK, color=N.ACCENT, fontstyle="italic")

    N.keystrip(ax, Y_KEY, [4.0, 34.0, 66.0, 98.0], [
        ("solid", "estimated path"),
        ("cond", "moderation"),
        ("dashed", "lagged feedback"),
        ("gate", "one-year delay"),
    ])

    return N.save(fig, os.path.join(FIG, "figure1_framework"))


# ===========================================================================
def figure2_moderation(S):
    """Marginal effect of adoption on the youth employment share across each
    boundary condition, with the observed support of the moderator beneath."""
    d = pd.read_csv(os.path.join(DATA, "panel.csv"))
    fig = N.figure(N.TEXT, 58.0)
    axes = N.row(fig, 2, left=17.0, bottom=15.0, height=38.0, gutter=13.0)

    panels = [
        (S["margin_absorp"], d.Absorp_z, "Organizational learning capability",
         N.BLUE, "a"),
        (S["margin_wage"], d.Wage_z, "Relative labor cost", N.VERMILION, "b"),
    ]
    drawn = []
    for ax, (rows, support, xlab, col, letter) in zip(axes, panels):
        z = np.array([r["z"] for r in rows])
        m = np.array([r["effect"] for r in rows])
        se = np.array([r["se"] for r in rows])
        ax.fill_between(z, m - 1.645 * se, m + 1.645 * se, color=col,
                        alpha=0.20, lw=0, zorder=1.5)
        ax.plot(z, m, color=col, lw=1.1, zorder=2)
        N.zeroline(ax)
        ax.set_xlim(z.min(), z.max())
        ax.set_xlabel(xlab + "\n(standard deviations from the mean)")
        lo = float(m[np.argmin(np.abs(z + 1.0))])
        hi = float(m[np.argmin(np.abs(z - 1.0))])
        for zz, vv in ((-1.0, lo), (1.0, hi)):
            ax.plot([zz], [vv], marker="o", ms=2.6, color=col, zorder=3,
                    mec="white", mew=0.4)
        drawn.append((ax, support.to_numpy(), col, lo, hi))

    # one shared vertical range, fixed before anything is annotated, so the
    # two panels are directly comparable and the support strips share a base
    top = max(a.get_ylim()[1] for a, *_ in drawn)
    bot = min(a.get_ylim()[0] for a, *_ in drawn)
    for ax, support, col, lo, hi in drawn:
        ax.set_ylim(bot, top)
        ax.annotate(N.num(lo, 2), xy=(-1.0, lo),
                    xytext=(-0.82, lo - 0.055 * (top - bot)),
                    ha="left", va="top", fontsize=N.PT_TICK, color=col)
        ax.annotate(N.num(hi, 2), xy=(1.0, hi),
                    xytext=(0.82, hi + 0.055 * (top - bot)),
                    ha="right", va="bottom", fontsize=N.PT_TICK, color=col)
        _rug(ax, support)
    axes[1].set_yticklabels([])

    axes[0].set_ylabel("Marginal effect on the youth\n"
                       "employment share (p.p.)")
    N.panel(fig, axes[0], "a", dx=-14.0)
    N.panel(fig, axes[1], "b", dx=-6.0)
    return N.save(fig, os.path.join(FIG, "figure2_moderation"))


# ===========================================================================
def figure3_irf(S):
    """Orthogonalized impulse responses of the three-variable system."""
    keys = [("Youth<-GenAI", "Youth employment share\nto an adoption shock",
             "percentage points", "a"),
            ("Train<-GenAI", "Training investment\nto an adoption shock",
             "log points", "b"),
            ("GenAI<-Train", "Adoption\nto a training shock",
             "index points", "c"),
            ("GenAI<-Youth", "Adoption\nto a youth employment shock",
             "index points", "d")]
    fig = N.figure(N.TEXT, 88.0)
    axes = [N.axes_mm(fig, x, y, 48.0, 24.5)
            for y in (53.5, 12.0) for x in (16.0, 81.0)]

    for ax, (k, title, unit, letter) in zip(axes, keys):
        r = S["irf"][k]
        h = np.arange(len(r["m"]))
        m = np.array(r["m"])
        ax.fill_between(h, r["lo"], r["hi"], color=N.BLUE, alpha=0.20, lw=0,
                        zorder=1.5)
        ax.plot(h, m, color=N.BLUE, lw=1.1, zorder=2)
        N.zeroline(ax)
        ax.set_xlim(0, h.max())
        ax.set_title(title, fontsize=N.PT_TICK, loc="left", pad=2.5)
        ax.set_ylabel(unit, fontsize=N.PT_TICK)
        N.panel(fig, ax, letter, dx=-13.0, dy=5.6)

        # mark the extremum and state it in the quadrant the curve vacates,
        # so the number is readable without a caption and collides with
        # nothing
        j = int(np.argmax(np.abs(m)))
        ax.plot([h[j]], [m[j]], marker="o", ms=2.6, color=N.BLUE,
                mec="white", mew=0.4, zorder=3)
        ax.text(0.97, 0.08, "peak %s at year %d" % (N.num(m[j]), h[j]),
                transform=ax.transAxes, ha="right", va="bottom",
                fontsize=N.PT_TICK, color=N.BLUE)

    for ax in axes[2:]:
        ax.set_xlabel("Years after the shock")
    return N.save(fig, os.path.join(FIG, "figure3_irf"))


if __name__ == "__main__":
    S = load()
    for out in (figure1_framework(), figure2_moderation(S), figure3_irf(S)):
        print(" ", os.path.basename(out[0]))
    print("figures written to", FIG)
