# -*- coding: utf-8 -*-
"""The three figures reported in the manuscript, drawn to the visual
conventions of recent articles in the target section of *Systems*.

*   Figure 1 is a minimalist monochrome theoretical framework: white
    rounded boxes with hairline black borders, bold construct names, thin
    black arrows, and moderator boxes above the paths they act on.
*   The data figures are greyscale in the marginsplot idiom the journal's
    empirical papers use: a black estimate line, an opaque light-grey 95
    percent confidence band, a dashed horizontal zero line, a dotted
    vertical reference where a turning point is marked, and a fully framed
    plot area.

No figure carries a note or a legend; everything a note would say is in
the body text. Figures are built at the 132 mm width at which the Word
file places them, panels positioned in millimetres.
"""
from __future__ import annotations

import json
import os

import numpy as np

import natureplot as N

N.use()

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)

BLACK = "#000000"
GREYBAND = "#D9D9D9"          # opaque light grey for confidence bands
GREYLINE = "#808080"

plt.rcParams.update({
    "axes.spines.top": True,          # the journal's figures are framed
    "axes.spines.right": True,
    "axes.labelsize": 8.0,
    "xtick.labelsize": 7.0,
    "ytick.labelsize": 7.0,
})
N.LADDER = {7.0, 8.0}


def load():
    with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
        return json.load(fh)


# ===========================================================================
def figure1_framework():
    """The theoretical research framework, in the journal's plain idiom."""
    W, H = N.TEXT, 46.0
    fig = N.figure(W, H)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.set_axis_off()

    def box(cx, cy, w, h, lines):
        ax.add_patch(FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0,rounding_size=2.2",
            facecolor="white", edgecolor=BLACK, linewidth=0.8, zorder=3))
        ax.text(cx, cy, "\n".join(lines), ha="center", va="center",
                fontsize=7.0, fontweight="bold", color=BLACK, zorder=4,
                linespacing=1.25)
        return dict(cx=cx, cy=cy, l=cx - w / 2, r=cx + w / 2,
                    t=cy + h / 2, b=cy - h / 2)

    def arrow(p0, p1, lw=0.8):
        ax.add_patch(FancyArrowPatch(
            p0, p1, arrowstyle="-|>,head_length=3.2,head_width=2.0",
            mutation_scale=1.0, linewidth=lw, color=BLACK,
            shrinkA=1.0, shrinkB=1.0, zorder=2))

    Y = 12.0
    phcd = box(19.0, Y, 34, 12, ["Perceived Human", "Capital Depreciation"])
    anx = box(64.0, Y, 30, 12, ["AI-Related", "Career Anxiety"])
    adp = box(113.0, 19.0, 32, 10, ["Occupational", "Adaptation"])
    avd = box(113.0, 5.5, 32, 10, ["Career", "Avoidance"])
    sup = box(41.5, 36.0, 32, 10, ["Perceived", "Employability Support"])
    lit = box(88.5, 36.0, 30, 10, ["Generative-AI", "Literacy"])

    arrow((phcd["r"], Y), (anx["l"], Y))
    arrow((anx["r"], Y + 2.5), (adp["l"], adp["cy"]))
    arrow((anx["r"], Y - 2.5), (avd["l"], avd["cy"]))
    # moderators descend onto the paths they govern
    arrow((sup["cx"], sup["b"]), ((phcd["r"] + anx["l"]) / 2, Y + 0.8))
    arrow((lit["cx"], lit["b"]),
          ((anx["r"] + adp["l"]) / 2, (Y + 2.5 + adp["cy"]) / 2 + 0.4))

    return N.save(fig, os.path.join(FIG, "figure1_framework"))


# ===========================================================================
def _frame(ax):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(0.6)
        ax.spines[side].set_color(BLACK)


def figure2_firststage(S):
    """Marginal effect of perceived depreciation on anxiety across support,
    in the journal's marginsplot idiom."""
    fig = N.figure(N.TEXT, 62.0)
    ax = N.axes_mm(fig, 24.0, 13.0, 92.0, 44.0)

    rows = S["firststage"]
    z = np.array([r["z"] for r in rows])
    m = np.array([r["effect"] for r in rows])
    se = np.array([r["se"] for r in rows])
    ax.fill_between(z, m - 1.96 * se, m + 1.96 * se, facecolor=GREYBAND,
                    edgecolor="none", zorder=1)
    ax.plot(z, m - 1.96 * se, color=GREYLINE, lw=0.5, zorder=1.5)
    ax.plot(z, m + 1.96 * se, color=GREYLINE, lw=0.5, zorder=1.5)
    ax.plot(z, m, color=BLACK, lw=1.3, zorder=2)
    ax.axhline(0.0, color=BLACK, lw=0.7, ls=(0, (5, 3)), zorder=1.8)
    ax.set_xlim(-2.0, 2.0)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_ylim(-0.2, 1.0)
    ax.set_xlabel("Perceived Employability Support (standardized)")
    ax.set_ylabel("Marginal Effect of PHCD on ANX")
    _frame(ax)
    return N.save(fig, os.path.join(FIG, "figure2_firststage"))


# ===========================================================================
def figure3_dual(S):
    """Predicted adaptation (a) and avoidance (b) across anxiety, greyscale,
    framed, with the turning point marked by a dotted vertical line."""
    fig = N.figure(N.TEXT, 63.0)
    ax1 = N.axes_mm(fig, 17.0, 13.0, 51.0, 40.0)
    ax2 = N.axes_mm(fig, 79.0, 13.0, 51.0, 40.0)

    for ax, key in ((ax1, "curve_adp"), (ax2, "curve_avd")):
        rows = S[key]
        z = np.array([r["z"] for r in rows])
        m = np.array([r["effect"] for r in rows])
        se = np.array([r["se"] for r in rows])
        ax.fill_between(z, m - 1.96 * se, m + 1.96 * se, facecolor=GREYBAND,
                        edgecolor="none", zorder=1)
        ax.plot(z, m - 1.96 * se, color=GREYLINE, lw=0.5, zorder=1.5)
        ax.plot(z, m + 1.96 * se, color=GREYLINE, lw=0.5, zorder=1.5)
        ax.plot(z, m, color=BLACK, lw=1.3, zorder=2)
        ax.axhline(0.0, color=BLACK, lw=0.7, ls=(0, (5, 3)), zorder=1.8)
        ax.set_xlim(z.min(), z.max())
        ax.set_xticks([-2, -1, 0, 1, 2])
        ax.set_xlabel("AI-Related Career Anxiety")
        _frame(ax)

    tp = S["tp"]
    ax1.axvline(tp["tau"], color=BLACK, lw=0.7, ls=(0, (1.2, 1.6)),
                zorder=1.9)
    lo, hi = ax1.get_ylim()
    ax1.set_ylim(min(lo, -1.7), max(hi, 1.1))
    ax2.set_ylim(*ax1.get_ylim())
    ax1.set_ylabel("Predicted Occupational Adaptation")
    ax2.set_ylabel("Predicted Career Avoidance")
    N.panels(fig, [(ax1, "(a)"), (ax2, "(b)")], gap=1.6)
    return N.save(fig, os.path.join(FIG, "figure3_dual"))


if __name__ == "__main__":
    S = load()
    for out in (figure1_framework(), figure2_firststage(S),
                figure3_dual(S)):
        print(" ", os.path.basename(out[0]))
    print("figures written to", FIG)
