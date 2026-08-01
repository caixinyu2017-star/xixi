# -*- coding: utf-8 -*-
"""The figures reported in the manuscript."""
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
W = 13.8 * CM          # body-zone width of the MDPI Systems layout

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "font.size": 8.0, "axes.labelsize": 8.0, "legend.fontsize": 7.2,
    "xtick.labelsize": 7.2, "ytick.labelsize": 7.2,
    "axes.linewidth": 0.7, "xtick.major.width": 0.7,
    "ytick.major.width": 0.7, "lines.linewidth": 1.4,
    "legend.framealpha": 0.93, "legend.fancybox": False,
    "legend.edgecolor": "0.75", "legend.borderpad": 0.35,
    "figure.dpi": 400, "savefig.dpi": 400,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})

NEG = "#B03A2E"
POS = "#1F618D"
GREY = "#4D4D4D"
ACC = "#117A65"

S = json.load(open(os.path.join(TAB, "summary.json"), encoding="utf-8"))


def save(fig, name):
    p = os.path.join(FIG, name)
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ---------------------------------------------------------------------------
def figure1():
    """Conceptual framework.

    Boxes, arrows and labels are laid out on an explicit grid and every label
    is anchored outside the line it annotates, so that no element overlaps
    another.
    """
    fig, ax = plt.subplots(figsize=(W, W * 0.60))
    ax.set_xlim(0.3, 12.7)
    ax.set_ylim(0.7, 7.5)
    ax.axis("off")

    def box(x, y, w, h, text, fc="white", fs=7.4, ec=GREY, lw=0.9):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.05,rounding_size=0.10",
                                    fc=fc, ec=ec, lw=lw, zorder=3))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4,
                linespacing=1.3)

    def arrow(p, q, color=GREY, ls="-", lw=1.15):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=9,
                                     lw=lw, color=color, linestyle=ls,
                                     shrinkA=0, shrinkB=0, zorder=2))

    # --- nodes -------------------------------------------------------------
    box(2.05, 4.30, 3.10, 1.05, "Generative AI\nadoption", fc="#EAF2F8")
    box(10.95, 4.30, 3.10, 1.05, "Youth employment\nshare", fc="#FEF9E7")
    box(6.50, 6.55, 3.20, 0.95, "Task routinisation\n(RTI)", fc="#FDEDEC")
    box(6.50, 2.05, 3.20, 0.95, "Human-capital\nupgrading (HCU)", fc="#E8F6F3")
    box(6.50, 5.35, 4.40, 0.90,
        "Organisational learning\ncapability and AI governance", fc="#F4ECF7",
        fs=6.9)

    # --- direct path H1, label below the line ------------------------------
    arrow((3.60, 4.30), (9.40, 4.30), NEG, lw=1.6)
    ax.text(6.50, 4.12, "H1   \u2212   direct effect", ha="center", va="top",
            fontsize=7.2, color=NEG, fontweight="bold")

    # --- moderation, pointing down at the middle of the direct path --------
    arrow((6.50, 4.88), (6.50, 4.42), "#7D3C98", ls=(0, (3, 2)), lw=1.1)
    ax.text(6.72, 4.65, "H4, H5", ha="left", va="center", fontsize=7.0,
            color="#7D3C98", style="italic")

    # --- routinisation channel (upper) -------------------------------------
    arrow((2.05, 4.85), (5.00, 6.20), NEG)
    ax.text(3.45, 5.90, "H2  \u2212", ha="right", va="center", fontsize=7.2,
            color=NEG, fontweight="bold")
    arrow((8.00, 6.20), (10.95, 4.85), POS)
    ax.text(9.60, 5.90, "+", ha="left", va="center", fontsize=8.4, color=POS,
            fontweight="bold")

    # --- human-capital channel (lower) -------------------------------------
    arrow((2.05, 3.75), (5.00, 2.45), POS)
    ax.text(3.45, 2.80, "H3  +", ha="right", va="center", fontsize=7.2,
            color=POS, fontweight="bold")
    arrow((8.00, 2.45), (10.95, 3.75), POS)
    ax.text(9.60, 2.80, "+", ha="left", va="center", fontsize=8.4, color=POS,
            fontweight="bold")
    save(fig, "figure1_framework.png")


def figure2():
    df = pd.read_csv(os.path.join(DATA, "panel.csv"))
    g = df.groupby("year").agg(adopt=("GenAI", "mean"),
                               share=("GenAI", lambda s: 100 * (s > 0).mean()),
                               youth=("Youth", "mean"))
    fig, ax = plt.subplots(figsize=(W, W * 0.52))
    ax2 = ax.twinx()
    l1, = ax.plot(g.index, g.youth, color=NEG, marker="o", ms=3.6,
                  label="Youth employment share (left axis)")
    l2, = ax2.plot(g.index, g.adopt, color=POS, marker="s", ms=3.6, ls="--",
                   label="GenAI adoption intensity (right axis)")
    l3, = ax2.plot(g.index, g.share / 100, color=ACC, marker="^", ms=3.6,
                   ls="-.", label="Share of firms reporting adoption (right axis)")
    ax.axvline(2022.5, color=GREY, lw=0.9, ls=":")
    # annotation in the empty upper-left quadrant, so nothing is occluded
    ax.text(2022.35, 0.97, "public release of\nlarge language models",
            transform=ax.get_xaxis_transform(), fontsize=6.6, color=GREY,
            ha="right", va="top")
    ax.set_xlabel("Year")
    ax.set_ylabel("Share of employees aged 30 or below (%)")
    ax2.set_ylabel("Adoption intensity / share of firms")
    ax.grid(alpha=0.25, lw=0.5)
    # the legend sits under the axes, outside the data region
    ax.legend(handles=[l1, l2, l3], loc="upper center",
              bbox_to_anchor=(0.5, -0.20), ncol=1, fontsize=6.8,
              frameon=False, handlelength=2.6, labelspacing=0.35)
    save(fig, "figure2_trends.png")


def figure3():
    e = np.load(os.path.join(TAB, "eventstudy.npy"))
    yrs, b, se = e[:, 0], e[:, 1], e[:, 2]
    fig, ax = plt.subplots(figsize=(W, W * 0.46))
    ax.axhline(0, color="black", lw=0.7)
    ax.axvline(2022.5, color=GREY, lw=0.9, ls=":")
    lo, hi = b - 1.96 * se, b + 1.96 * se
    ax.errorbar(yrs, b, yerr=1.96 * se, fmt="o", ms=4.0, color=NEG,
                ecolor=NEG, elinewidth=1.0, capsize=2.4)
    ax.fill_between(yrs, lo, hi, color=NEG, alpha=0.10)
    ax.set_xlabel("Year")
    ax.set_ylabel("Coefficient on exposure × year")
    ax.set_xticks(yrs.astype(int))
    ax.grid(alpha=0.25, lw=0.5)
    ax.text(0.985, 0.955, "post-shock", transform=ax.transAxes, fontsize=6.8,
            color=GREY, ha="right", va="top")
    save(fig, "figure3_eventstudy.png")


def figure4():
    m = np.load(os.path.join(TAB, "marginal.npy"))
    g, eff, se = m[:, 0], m[:, 1], m[:, 2]
    fig, ax = plt.subplots(figsize=(W, W * 0.46))
    ax.axhline(0, color="black", lw=0.7)
    ax.plot(g, eff, color=NEG)
    ax.fill_between(g, eff - 1.96 * se, eff + 1.96 * se, color=NEG, alpha=0.15)
    turn = S["mod_olc_turn"]
    if g.min() <= turn <= g.max():
        ax.axvline(turn, color=ACC, lw=1.0, ls="--")
        ax.annotate("effect ceases to be\nsignificant (P%.0f)"
                    % S["mod_olc_turn_pct"], (turn, 0),
                    textcoords="offset points", xytext=(-96, 16),
                    fontsize=6.8, color=ACC)
    df = pd.read_csv(os.path.join(DATA, "panel.csv"))
    for q in (25, 50, 75):
        v = np.percentile(df.OLC, q)
        ax.plot([v], [np.interp(v, g, eff)], marker="o", ms=3.6, color=GREY)
        ax.annotate("P%d" % q, (v, np.interp(v, g, eff)),
                    textcoords="offset points", xytext=(3, -9), fontsize=6.6,
                    color=GREY)
    ax.set_xlabel("Organisational learning capability (standardised)")
    ax.set_ylabel("Marginal effect of GenAI adoption\non the youth share (pp)")
    ax.grid(alpha=0.25, lw=0.5)
    save(fig, "figure4_marginal.png")


def figure5():
    bal = pd.read_csv(os.path.join(TAB, "balance.csv"))
    fig, ax = plt.subplots(figsize=(W, W * 0.50))
    y = np.arange(len(bal))
    ax.axvline(0, color="black", lw=0.7)
    for x in (-10, 10):
        ax.axvline(x, color=GREY, lw=0.7, ls=":")
    ax.scatter(bal.bias_u, y, marker="o", s=22, facecolors="none",
               edgecolors=NEG, label="Before matching")
    ax.scatter(bal.bias_m, y, marker="D", s=18, color=POS,
               label="After matching")
    for i in y:
        ax.plot([bal.bias_u[i], bal.bias_m[i]], [i, i], color=GREY, lw=0.6,
                alpha=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(bal["var"], fontsize=7.0)
    ax.set_xlabel("Standardised percentage bias")
    ax.grid(axis="x", alpha=0.25, lw=0.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2,
              fontsize=7.0, frameon=False)
    save(fig, "figure5_balance.png")


def figure6():
    d = np.load(os.path.join(TAB, "placebo.npy"))
    fig, ax = plt.subplots(figsize=(W, W * 0.46))
    ax.hist(d, bins=34, color="#5D6D7E", ec="white", lw=0.4, density=True)
    ax.axvline(S["placebo_true"], color=NEG, lw=1.6)
    ax.annotate("actual estimate\n%.3f" % S["placebo_true"],
                (S["placebo_true"], ax.get_ylim()[1] * 0.62),
                textcoords="offset points", xytext=(8, 0), fontsize=7.0,
                color=NEG)
    ax.axvline(0, color="black", lw=0.7, ls=":")
    ax.set_xlabel("Placebo estimate of the coefficient on exposure × post")
    ax.set_ylabel("Density")
    ax.grid(alpha=0.25, lw=0.5)
    ax.text(0.02, 0.95, "%d random reassignments of ex-ante exposure"
            % S["placebo_n"], transform=ax.transAxes, fontsize=6.8, va="top")
    save(fig, "figure6_placebo.png")


if __name__ == "__main__":
    figure1(); figure2(); figure3(); figure4(); figure5(); figure6()
