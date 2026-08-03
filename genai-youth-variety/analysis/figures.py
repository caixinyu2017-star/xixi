# -*- coding: utf-8 -*-
"""The three figures reported in the manuscript.

Layout rule applied throughout: every label, arrow and legend is placed in a
region of the canvas that no other element occupies, so nothing is ever drawn
over anything else.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
os.makedirs(FIG, exist_ok=True)

CM = 1 / 2.54
W = 13.8 * CM

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "font.size": 8.0, "axes.labelsize": 8.0, "legend.fontsize": 7.0,
    "xtick.labelsize": 7.2, "ytick.labelsize": 7.2,
    "axes.linewidth": 0.7, "xtick.major.width": 0.7,
    "ytick.major.width": 0.7, "lines.linewidth": 1.3,
    "legend.framealpha": 1.0, "legend.fancybox": False,
    "legend.edgecolor": "0.75", "legend.borderpad": 0.35,
    "figure.dpi": 400, "savefig.dpi": 400,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.04,
})

INK = "#1f1f1f"
GREY = "#6f6f6f"
BLUE = "#2f5d8c"
RED = "#a6362d"
GOLD = "#9a7a2e"


def load():
    with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
        return json.load(fh)


# ===========================================================================
def figure1_framework():
    fig, ax = plt.subplots(figsize=(W, W * 0.80))
    ax.set_xlim(0, 10)
    ax.set_ylim(0.2, 8.30)
    ax.axis("off")

    def box(cx, cy, w, h, lines, fc="white", ec=INK, lw=0.9, fs=7.4):
        ax.add_patch(FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec,
            lw=lw, zorder=3))
        ax.text(cx, cy, "\n".join(lines), ha="center", va="center",
                fontsize=fs, color=INK, zorder=4, linespacing=1.35)

    def arrow(p0, p1, color=INK, lw=1.0):
        ax.add_patch(FancyArrowPatch(
            p0, p1, arrowstyle="-|>", mutation_scale=8.5, lw=lw,
            color=color, shrinkA=0, shrinkB=0, zorder=2))

    box(5.00, 7.60, 3.60, 1.05,
        ["Workforce skill variety (Variety)", "= RelVar + UnrelVar"])
    box(1.30, 5.75, 2.40, 0.80, ["Digital capability"], fc="#f7f4ee", ec=GREY)
    box(8.70, 5.75, 2.40, 0.80, ["Financial slack"], fc="#f7f4ee", ec=GREY)
    box(1.50, 4.10, 2.60, 1.05, ["Industry demand", "shock (Shock)"],
        fc="#f6eeec")
    box(8.50, 4.10, 2.60, 1.05, ["Youth employment", "share (Youth)"],
        fc="#eef2f7")
    box(5.00, 2.30, 3.05, 0.85, ["Internal redeployment"])
    box(5.00, 0.75, 3.05, 0.85, ["Workforce churn"])

    # the disturbance
    arrow((2.82, 4.10), (7.18, 4.10), lw=1.25)
    ax.text(3.60, 4.24, "(−)", ha="center", va="bottom", fontsize=7.4)

    # the regulatory capacity, gated at the requisite level
    arrow((5.00, 7.06), (5.00, 4.26), lw=1.15)
    ax.text(4.78, 6.86, "H2 (+), H3", ha="right", va="center", fontsize=7.2)
    for y in (6.30, 6.16):
        ax.plot([4.79, 5.21], [y, y], color=RED, lw=1.3, zorder=4)
    ax.text(4.70, 6.23, "H5: gate at γ", ha="right", va="center",
            fontsize=7.2, color=RED)

    # H1
    arrow((6.55, 7.06), (7.62, 4.66))
    ax.text(7.58, 6.55, "H1 (+)", ha="left", va="center", fontsize=7.2)

    # the two enabling conditions
    arrow((2.50, 5.55), (4.80, 4.76), color=GREY, lw=0.9)
    arrow((7.50, 5.55), (5.20, 4.76), color=GREY, lw=0.9)
    ax.text(3.55, 5.02, "H6a (+)", ha="center", va="top", fontsize=7.2,
            color=GREY)
    ax.text(6.45, 5.02, "H6b (+)", ha="center", va="top", fontsize=7.2,
            color=GREY)

    # the two channels
    arrow((1.82, 3.56), (3.42, 2.58))
    arrow((1.48, 3.56), (3.42, 0.98))
    arrow((6.55, 2.58), (8.28, 3.60))
    arrow((6.55, 0.98), (8.52, 3.54))
    ax.text(2.62, 2.98, "H4", ha="center", va="center", fontsize=7.2)

    fig.savefig(os.path.join(FIG, "figure1_framework.png"))
    plt.close(fig)


# ===========================================================================
def figure2_margins(S):
    """Marginal effect of the demand shock across the variety measures."""
    d = pd.read_csv(os.path.join(DATA, "panel.csv"))
    fig, axes = plt.subplots(1, 2, figsize=(W, W * 0.46))

    ax = axes[0]
    rows = S["margin_variety"]
    z = np.array([r["z"] for r in rows])
    m = np.array([r["effect"] for r in rows])
    se = np.array([r["se"] for r in rows])
    ax.fill_between(z, m - 1.645 * se, m + 1.645 * se, color=BLUE,
                    alpha=0.16, lw=0)
    ax.plot(z, m, color=BLUE, lw=1.4)
    ax.axhline(0.0, color=GREY, lw=0.8, ls=(0, (3, 2)))
    g = S["thr"]["gamma"]
    ax.axvline(g, color=RED, lw=1.0, ls=(0, (5, 2)))
    ymin, ymax = ax.get_ylim()
    ax.text(g - 0.06, ymin + 0.08 * (ymax - ymin),
            "$\\hat{\\gamma}$ = %.2f" % g, ha="right", va="bottom",
            fontsize=7.2, color=RED)
    ax.set_xlabel("Workforce skill variety")
    ax.set_ylabel("Marginal effect of the shock on the\nyouth employment "
                  "share (p.p.)")
    ax.set_xlim(z.min(), z.max())
    ax.tick_params(direction="in", length=2.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.03, 0.93, "(a)", transform=ax.transAxes, fontsize=7.6,
            ha="left", va="top")

    ax = axes[1]
    for key, col, lab, mu, sd in (
            ("margin_rel", BLUE, "Related variety", S["mean_RelVar"],
             S["sd_RelVar"]),
            ("margin_unrel", GOLD, "Unrelated variety", S["mean_UnrelVar"],
             S["sd_UnrelVar"])):
        rows = S[key]
        x = mu + np.array([r["z"] for r in rows]) * sd
        m = np.array([r["effect"] for r in rows])
        se = np.array([r["se"] for r in rows])
        keep = x >= 0.0
        ax.fill_between(x[keep], (m - 1.645 * se)[keep],
                        (m + 1.645 * se)[keep], color=col, alpha=0.14, lw=0)
        ax.plot(x[keep], m[keep], color=col, lw=1.4, label=lab)
    ax.axhline(0.0, color=GREY, lw=0.8, ls=(0, (3, 2)))
    ax.set_xlabel("Variety component (bits)")
    ax.set_xlim(0.0, 2.4)
    ax.tick_params(direction="in", length=2.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(loc="lower right", frameon=True)
    ax.text(0.03, 0.93, "(b)", transform=ax.transAxes, fontsize=7.6,
            ha="left", va="top")

    fig.subplots_adjust(wspace=0.30)
    fig.savefig(os.path.join(FIG, "figure2_margins.png"))
    plt.close(fig)


# ===========================================================================
def figure3_threshold(S):
    """The requisite-variety threshold and the regime coefficients."""
    T = S["thr"]
    fig, axes = plt.subplots(1, 2, figsize=(W, W * 0.50))

    ax = axes[0]
    g = np.array(T["grid"])
    lr = np.array(T["lr"])
    ok = np.isfinite(lr)
    ax.plot(g[ok], lr[ok], color=BLUE, lw=1.3)
    ax.axhline(T["crit"], color=RED, lw=1.0, ls=(0, (5, 2)))
    ax.axvspan(T["ci_low"], T["ci_high"], color=RED, alpha=0.10, lw=0)
    ax.axvline(T["gamma"], color=RED, lw=1.0)
    ax.set_xlabel("Candidate threshold (bits)")
    ax.set_ylabel("Likelihood-ratio statistic")
    ax.set_xlim(g.min(), g.max())
    ax.tick_params(direction="in", length=2.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.03, 0.27, "95%% critical\nvalue = %.2f" % T["crit"],
            transform=ax.transAxes, ha="left", va="bottom", fontsize=7.0,
            color=RED)
    ax.set_title("(a)", loc="left", fontsize=7.6, pad=3.0)

    ax = axes[1]
    pts = [(0, T["b_low"], T["se_low"], "Variety $\\leq\\ \\hat{\\gamma}$"),
           (1, T["b_high"], T["se_high"], "Variety $>\\ \\hat{\\gamma}$")]
    for x, b, se, lab in pts:
        ax.errorbar(x, b, yerr=1.96 * se, fmt="o", ms=4.2, color=BLUE,
                    ecolor=BLUE, elinewidth=1.1, capsize=3.0)
    ax.axhline(0.0, color=GREY, lw=0.8, ls=(0, (3, 2)))
    ax.set_xticks([0, 1])
    ax.set_xticklabels([p[3] for p in pts])
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylabel("Effect of the shock (p.p.)")
    ax.tick_params(direction="in", length=2.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("(b)", loc="left", fontsize=7.6, pad=3.0)

    fig.subplots_adjust(wspace=0.32)
    fig.savefig(os.path.join(FIG, "figure3_threshold.png"))
    plt.close(fig)


if __name__ == "__main__":
    S = load()
    figure1_framework()
    figure2_margins(S)
    figure3_threshold(S)
    print("figures written to", FIG)
