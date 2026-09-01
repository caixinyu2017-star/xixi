# -*- coding: utf-8 -*-
"""The five figures of the manuscript, drawn to the visual conventions of
the published articles in the target Topic.

*   Figures 1-4 are two-panel scatter charts in the statistical-package
    idiom those articles use: observed country points as filled blue
    circles, a black linear fit line, the dependent variable named in a
    bold panel title above the framed plot area, two-decimal tick labels,
    and a small legend placed entirely outside the plot area to the
    right so that it can never occlude the data.
*   Figure 5 is a horizontal dendrogram on a light-grey panel with the
    rescaled distance axis on top, country labels and case numbers on
    the left, and dotted vertical gridlines.

No figure carries a note; everything a note would say is in the body
text. Figures are built at the 132 mm width at which the Word file
places them.
"""
from __future__ import annotations

import json
import os

import numpy as np
from scipy.cluster import hierarchy as sch

import data
import natureplot as N

N.use()

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)

BLACK = "#000000"
BLUE = "#3A66A8"                      # the package's observed-point blue
PANEL_GREY = "#F0F0F0"

plt.rcParams.update({
    "axes.spines.top": True,
    "axes.spines.right": True,
    "axes.labelsize": 8.0,
    "xtick.labelsize": 7.0,
    "ytick.labelsize": 7.0,
})
N.LADDER = {7.0, 8.0}

COUNTRIES, D = data.frame()
A = {k: np.array(v, float) for k, v in D.items()}

with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
    S = json.load(fh)

RANGES = {
    "AIENT": (0, 30, [0, 10, 20, 30]),
    "GAIY": (20, 70, [20, 30, 40, 50, 60, 70]),
    "DSKY": (40, 95, [40, 50, 60, 70, 80, 90]),
    "ICTS": (2, 9, [2, 4, 6, 8]),
    "NEET": (0, 22, [0, 5, 10, 15, 20]),
    "YUR": (5, 30, [5, 10, 15, 20, 25, 30]),
}


def _fmt2(vals):
    return ["%.2f" % v for v in vals]


def _panel(ax, xvar, dv):
    x, y = A[xvar], A[dv]
    b0 = S["fits"][xvar][dv]["b0"]
    b1 = S["fits"][xvar][dv]["b1"]
    xlo, xhi, xticks = RANGES[xvar]
    ylo, yhi, yticks = RANGES[dv]
    xs = np.array([xlo, xhi])
    ax.plot(xs, b0 + b1 * xs, color=BLACK, lw=1.1, zorder=2)
    ax.scatter(x, y, s=11, facecolor=BLUE, edgecolor=BLUE, lw=0.4,
               zorder=3)
    ax.set_xlim(xlo, xhi)
    ax.set_ylim(ylo, yhi)
    ax.set_xticks(xticks)
    ax.set_xticklabels(_fmt2(xticks))
    ax.set_yticks(yticks)
    ax.set_yticklabels(_fmt2(yticks))
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(0.6)
        ax.spines[side].set_color(BLACK)
    ax.tick_params(direction="out", length=2.4, width=0.6)
    ax.set_title(dv, fontsize=8.0, fontweight="bold", pad=3)
    ax.set_xlabel(xvar)


def _legend(fig, ax):
    """Observed / Linear key, wholly outside the plot area to the right."""
    handles = [
        Line2D([], [], marker="o", linestyle="none", markersize=3.2,
               markerfacecolor=BLUE, markeredgecolor=BLUE,
               label="Observed"),
        Line2D([], [], color=BLACK, lw=1.1, label="Linear"),
    ]
    ax.legend(handles=handles, loc="upper left",
              bbox_to_anchor=(1.03, 1.0), frameon=False, fontsize=7.0,
              handlelength=1.4, handletextpad=0.5, labelspacing=0.5,
              borderaxespad=0.0)


def figure_scatter(num, xvar):
    W, H = N.TEXT, 118.0
    fig = N.figure(W, H)
    ax1 = N.axes_mm(fig, 20.0, 69.0, 82.0, 40.0)     # NEET, upper panel
    ax2 = N.axes_mm(fig, 20.0, 13.0, 82.0, 40.0)     # YUR, lower panel
    _panel(ax1, xvar, "NEET")
    _panel(ax2, xvar, "YUR")
    _legend(fig, ax1)
    _legend(fig, ax2)
    return N.save(fig, os.path.join(FIG, "figure%d_%s" % (num,
                                                          xvar.lower())))


# ===========================================================================
def figure5_dendrogram():
    """Horizontal average-linkage dendrogram, package idiom."""
    Z6 = np.column_stack([(A[v] - A[v].mean()) / A[v].std(ddof=1)
                          for v in ["AIENT", "GAIY", "DSKY", "ICTS",
                                    "NEET", "YUR"]])
    link = np.load(os.path.join(TAB, "linkage.npy"))
    n = len(COUNTRIES)
    dg = sch.dendrogram(link, no_plot=True, labels=list(range(n)))
    dmax = link[:, 2].max()
    scale = 25.0 / dmax

    W, H = N.TEXT, 128.0
    fig = N.figure(W, H)
    ax = N.axes_mm(fig, 36.0, 6.0, 88.0, 103.0)
    ax.set_facecolor(PANEL_GREY)

    leaf_order = dg["leaves"]                       # data indices, top-down
    ypos = {leaf: n - 1 - i for i, leaf in enumerate(leaf_order)}

    for xs, ys in zip(dg["dcoord"], dg["icoord"]):
        # icoord runs in leaf-position units of 5, 15, 25, ...
        yy = [n - 1 - (v - 5.0) / 10.0 for v in ys]
        xx = [v * scale for v in xs]
        ax.plot(xx, yy, color=BLACK, lw=0.7, zorder=3,
                solid_joinstyle="miter")

    ax.set_xlim(0, 25.6)
    ax.set_ylim(-0.8, n - 0.2)
    ax.set_xticks([0, 5, 10, 15, 20, 25])
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.tick_params(axis="x", direction="out", length=2.2, width=0.6,
                   labelsize=7.0, pad=1.5)
    for g in [5, 10, 15, 20, 25]:
        ax.axvline(g, color="#BBBBBB", lw=0.5, ls=(0, (1.2, 1.8)),
                   zorder=1)
    ax.set_yticks([])
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(0.6)
        ax.spines[side].set_color(BLACK)

    # country labels and case numbers, in dendrogram order, to the left
    for leaf in leaf_order:
        y = ypos[leaf]
        ax.text(-0.075, y, COUNTRIES[leaf], transform=ax.get_yaxis_transform(),
                ha="right", va="center", fontsize=7.0, color=BLACK)
        ax.text(-0.012, y, str(leaf + 1), transform=ax.get_yaxis_transform(),
                ha="right", va="center", fontsize=7.0, color=BLACK)

    fig.text(0.5, (H - 8.0) / H, "Dendrogram using Average Linkage "
             "(Between Groups)", ha="center", va="center", fontsize=8.0,
             fontweight="bold")
    fig.text(0.5, (H - 13.0) / H, "Rescaled Distance Cluster Combine",
             ha="center", va="center", fontsize=7.0, fontweight="bold")
    return N.save(fig, os.path.join(FIG, "figure5_dendrogram"))


if __name__ == "__main__":
    outs = [figure_scatter(1, "AIENT"), figure_scatter(2, "GAIY"),
            figure_scatter(3, "DSKY"), figure_scatter(4, "ICTS"),
            figure5_dendrogram()]
    for o in outs:
        print(" ", os.path.basename(o[0]))
    print("figures written to", FIG)
