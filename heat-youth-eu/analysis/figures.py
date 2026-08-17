# -*- coding: utf-8 -*-
"""The three figures of the manuscript, drawn in the restrained
greyscale econometric idiom of the journal's empirical papers: framed
axes, black lines and markers, an opaque light-grey confidence band,
dashed reference lines, no legends placed over data and no figure
notes; everything a note would say is in the body text.
"""
from __future__ import annotations

import json
import os

import numpy as np

import natureplot as N

N.use()

import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)

BLACK = "#000000"
GREYBAND = "#D9D9D9"
GREYLINE = "#808080"

plt.rcParams.update({
    "axes.spines.top": True,
    "axes.spines.right": True,
    "axes.labelsize": 8.0,
    "xtick.labelsize": 7.0,
    "ytick.labelsize": 7.0,
})
N.LADDER = {7.0, 8.0}

with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
    S = json.load(fh)


def _frame(ax):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(0.6)
        ax.spines[side].set_color(BLACK)
    ax.tick_params(direction="out", length=2.4, width=0.6)


# ===========================================================================
def figure1_trends():
    """EU-27 averages, 2010-2024: (a) cooling degree days, (b) NEET."""
    years = [r["year"] for r in S["trend"]]
    cdd = [r["cdd"] for r in S["trend"]]
    neet = [r["neet"] for r in S["trend"]]

    fig = N.figure(N.TEXT, 62.0)
    ax1 = N.axes_mm(fig, 17.0, 13.0, 51.0, 40.0)
    ax2 = N.axes_mm(fig, 79.0, 13.0, 51.0, 40.0)

    ax1.plot(years, cdd, color=BLACK, lw=1.2, marker="o", ms=2.6,
             markerfacecolor=BLACK)
    ax1.set_ylabel("Cooling degree days (EU-27 average)")
    ax1.set_ylim(180, 420)
    ax2.plot(years, neet, color=BLACK, lw=1.2, marker="s", ms=2.6,
             markerfacecolor="white")
    ax2.set_ylabel("NEET rate, 15–29 (EU-27 average, %)")
    ax2.set_ylim(9, 16)
    for ax in (ax1, ax2):
        ax.set_xlim(2009.5, 2024.5)
        ax.set_xticks([2010, 2014, 2018, 2022])
        ax.set_xlabel("Year")
        _frame(ax)
    N.panels(fig, [(ax1, "(a)"), (ax2, "(b)")], gap=1.6)
    return N.save(fig, os.path.join(FIG, "figure1_trends"))


# ===========================================================================
def figure2_cross():
    """Country means, 2010-2024: summer heat exposure and the NEET rate."""
    pts = S["cross"]["points"]
    x = np.array([p["cdd"] for p in pts]) / 100.0
    y = np.array([p["neet"] for p in pts])
    b, a = S["cross"]["slope"], S["cross"]["intercept"]

    fig = N.figure(N.TEXT, 66.0)
    ax = N.axes_mm(fig, 24.0, 13.0, 92.0, 48.0)
    xs = np.array([0.0, 9.6])
    ax.plot(xs, a + b * 100.0 * xs, color=BLACK, lw=1.1, zorder=2)
    ax.scatter(x, y, s=13, facecolor="white", edgecolor=BLACK, lw=0.7,
               zorder=3)
    ax.set_xlim(-0.3, 9.6)
    ax.set_ylim(3, 23)
    ax.set_xlabel("Cooling degree days, country average "
                  "(hundreds)")
    ax.set_ylabel("NEET rate, country average (%)")
    _frame(ax)
    return N.save(fig, os.path.join(FIG, "figure2_cross"))


# ===========================================================================
def figure3_margins():
    """The estimated effect of +100 cooling degree days on the NEET rate
    across the urban green infrastructure endowment."""
    g = np.array([r["grn"] for r in S["margins"]])
    me = np.array([r["me"] for r in S["margins"]])
    se = np.array([r["se"] for r in S["margins"]])

    fig = N.figure(N.TEXT, 64.0)
    ax = N.axes_mm(fig, 24.0, 13.0, 92.0, 46.0)
    ax.fill_between(g, me - 1.96 * se, me + 1.96 * se,
                    facecolor=GREYBAND, edgecolor="none", zorder=1)
    ax.plot(g, me - 1.96 * se, color=GREYLINE, lw=0.5, zorder=1.5)
    ax.plot(g, me + 1.96 * se, color=GREYLINE, lw=0.5, zorder=1.5)
    ax.plot(g, me, color=BLACK, lw=1.3, zorder=2)
    ax.axhline(0.0, color=BLACK, lw=0.7, ls=(0, (5, 3)), zorder=1.8)
    if S["me_cutoff"]:
        ax.axvline(S["me_cutoff"], color=BLACK, lw=0.7,
                   ls=(0, (1.2, 1.6)), zorder=1.9)
    ax.set_xlim(10, 47)
    ax.set_ylim(-0.5, 0.7)
    ax.set_xlabel("Green infrastructure share of functional urban "
                  "areas (%)")
    ax.set_ylabel("Effect of +100 cooling degree days\n"
                  "on the NEET rate (p.p.)")
    _frame(ax)
    return N.save(fig, os.path.join(FIG, "figure3_margins"))


if __name__ == "__main__":
    for out in (figure1_trends(), figure2_cross(), figure3_margins()):
        print(" ", os.path.basename(out[0]))
    print("figures written to", FIG)
