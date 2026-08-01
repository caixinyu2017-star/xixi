# -*- coding: utf-8 -*-
"""The figures reported in the manuscript.

Layout rule applied throughout: every annotation and legend is placed either
outside the axes or in a region of the axes that no plotted element occupies,
so that nothing is ever drawn over anything else.
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
W = 13.8 * CM          # body-zone width of the MDPI Systems layout

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "font.size": 8.0, "axes.labelsize": 8.0, "legend.fontsize": 7.2,
    "xtick.labelsize": 7.2, "ytick.labelsize": 7.2,
    "axes.linewidth": 0.7, "xtick.major.width": 0.7,
    "ytick.major.width": 0.7, "lines.linewidth": 1.4,
    "legend.framealpha": 1.0, "legend.fancybox": False,
    "legend.edgecolor": "0.75", "legend.borderpad": 0.35,
    "figure.dpi": 400, "savefig.dpi": 400,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.04,
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

    A single full-width diagram, so that every box is wide enough for its own
    label and no element is drawn over another.  The moderators are shown
    empirically in Figure 5 and are deliberately not crowded in here.
    """
    fig, ax = plt.subplots(figsize=(W, W * 0.42))
    ax.set_xlim(0.0, 14.0)
    ax.set_ylim(-0.3, 7.6)
    ax.axis("off")

    def box(x, y, w, h, text, fc, fs=7.0):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.07,rounding_size=0.16",
                                    fc=fc, ec=GREY, lw=0.9, zorder=3))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4,
                linespacing=1.35)

    def arrow(p, q, color=GREY, ls="-", lw=1.2):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=10,
                                     lw=lw, color=color, linestyle=ls,
                                     shrinkA=0, shrinkB=0, zorder=2))

    box(2.05, 3.65, 3.70, 1.55, "Generative AI\nadoption depth", "#EAF2F8")
    box(11.95, 3.65, 3.70, 1.55, "Youth\nemployment share", "#FEF9E7")
    box(7.00, 6.45, 5.50, 1.30,
        "Augmentation of entry-level work\n(increasing, concave)", "#E8F6F3", 6.6)
    box(7.00, 0.85, 5.50, 1.30,
        "Automation of the entry task bundle\n(increasing, convex)", "#FDEDEC", 6.6)

    arrow((3.55, 4.45), (4.62, 5.78), ACC)
    arrow((9.38, 5.78), (10.45, 4.45), ACC)
    arrow((3.55, 2.85), (4.62, 1.52), NEG)
    arrow((9.38, 1.52), (10.45, 2.85), NEG)
    # the signs are centred on the arrow they label and carry an opaque
    # background, so neither the arrow nor the sign is obscured
    sign = dict(ha="center", va="center", fontweight="bold", zorder=5,
                bbox=dict(boxstyle="round,pad=0.10", fc="white", ec="none"))
    ax.text(9.92, 5.11, "+", fontsize=9.0, color=ACC, **sign)
    ax.text(9.92, 2.19, "\u2212", fontsize=9.0, color=NEG, **sign)

    arrow((3.95, 3.65), (10.05, 3.65), GREY, ls=(0, (4, 2.5)), lw=1.1)
    ax.text(7.00, 3.86, "H1: inverted U", ha="center", va="bottom",
            fontsize=7.4, color=GREY, fontweight="bold")
    save(fig, "figure1_framework.png")


# ---------------------------------------------------------------------------
def figure2():
    df = pd.read_csv(os.path.join(DATA, "panel.csv"))
    g = df.groupby("year").agg(depth=("AI", "mean"), youth=("Youth", "mean"))
    fig, ax = plt.subplots(figsize=(W, W * 0.46))
    ax2 = ax.twinx()
    l1, = ax.plot(g.index, g.youth, color=NEG, marker="o", ms=3.6,
                  label="Youth employment share (left axis)")
    l2, = ax2.plot(g.index, g.depth, color=POS, marker="s", ms=3.6, ls="--",
                   label="Mean adoption depth (right axis)")
    ax.axvline(2022.5, color=GREY, lw=0.9, ls=":")
    # the wedge between the flat pre-shock depth series and the youth line is
    # the only empty part of the panel, so the note goes there
    ax.annotate("public release of\nlarge language models",
                xy=(2022.5, 0.02), xycoords=ax.get_xaxis_transform(),
                xytext=(2021.6, 0.12), textcoords=ax.get_xaxis_transform(),
                fontsize=6.6, color=GREY, ha="right", va="bottom",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=GREY,
                                shrinkA=3, shrinkB=1))
    ax.set_xlabel("Year")
    ax.set_ylabel("Share of employees aged\n30 or below (%)")
    ax2.set_ylabel("Mean adoption depth")
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(handles=[l1, l2], loc="upper center",
              bbox_to_anchor=(0.5, -0.22), ncol=1, fontsize=6.8,
              frameon=False, handlelength=2.6, labelspacing=0.3)
    save(fig, "figure2_trends.png")


# ---------------------------------------------------------------------------
def figure3():
    c = np.load(os.path.join(TAB, "curve.npy"))
    b = pd.read_csv(os.path.join(TAB, "bins.csv"))
    x, fit, se = c[:, 0], c[:, 1], c[:, 2]
    fig, ax = plt.subplots(figsize=(W, W * 0.52))
    ax.axhline(0, color="black", lw=0.7)
    ax.plot(x, fit, color=NEG, lw=1.6, label="Fitted quadratic")
    ax.fill_between(x, fit - 1.96 * se, fit + 1.96 * se, color=NEG, alpha=0.14,
                    label="95% confidence band")

    tau = S["tau"]
    peak = S["b1"] * tau + S["b2"] * tau ** 2
    ax.axvline(tau, color=ACC, lw=1.1, ls="--")
    ax.axvspan(S["tau_lo"], S["tau_hi"], color=ACC, alpha=0.12)
    ax.plot([tau], [peak], marker="o", ms=4.2, color=ACC, zorder=5)

    by = b["y"] - b["y"].iloc[0] + np.interp(b["x"].iloc[0], x, fit)
    ax.plot(b["x"], by, ls="none", marker="D", ms=3.0, color=GREY, alpha=0.8,
            label="Residualised binned means")

    # the quadrant below the zero line and left of the peak carries no data at
    # all, so the label goes there and crosses nothing
    ax.text(tau * 0.55, min(fit) * 0.62,
            "extreme point %.2f\n[%.2f, %.2f]" % (tau, S["tau_lo"], S["tau_hi"]),
            fontsize=6.8, color=ACC, ha="center", va="center")
    ax.set_xlim(-0.12, S["ai_max"] + 0.12)
    ax.set_xlabel("Generative AI adoption depth")
    ax.set_ylabel("Effect on the youth\nemployment share (pp)")
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2,
              fontsize=6.8, frameon=False)
    save(fig, "figure3_curve.png")


# ---------------------------------------------------------------------------
def figure4():
    d = np.load(os.path.join(TAB, "decomp.npy"))
    x, aug, aut = d[:, 0], d[:, 1], d[:, 2]
    net = aug + aut
    fig, ax = plt.subplots(figsize=(W, W * 0.52))
    ax.axhline(0, color="black", lw=0.7)
    ax.plot(x, aug, color=ACC, lw=1.4, label="Augmentation channel (concave)")
    ax.plot(x, aut, color=NEG, lw=1.4, ls="--",
            label="Automation channel (convex)")
    ax.plot(x, net, color=GREY, lw=1.9, label="Net effect")

    xt = float(x[np.argmax(net)])
    ax.axvline(xt, color=GREY, lw=0.9, ls=":")
    # written vertically beside the marker line, in the empty band at the foot
    # of the panel through which no curve passes
    lo, hi = ax.get_ylim()
    ax.text(xt + 0.10, lo + 0.03 * (hi - lo), "net effect peaks",
            rotation=90, ha="left", va="bottom", fontsize=6.6, color=GREY)
    ax.set_xlim(-0.12, S["ai_max"] + 0.12)
    ax.set_xlabel("Generative AI adoption depth")
    ax.set_ylabel("Contribution to the youth\nemployment share (pp)")
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=1,
              fontsize=6.8, frameon=False, labelspacing=0.3)
    save(fig, "figure4_channels.png")


# ---------------------------------------------------------------------------
def figure5():
    m = np.load(os.path.join(TAB, "modcurves.npy"))
    labs = [("Organisational learning\ncapability", "−1 SD", "+1 SD"),
            ("AI governance", "not disclosed", "disclosed"),
            ("Labour cost pressure", "−1 SD", "+1 SD")]
    keys = ["OLC", "AIGov", "LCP"]
    fig, axes = plt.subplots(1, 3, figsize=(W, W * 0.48), sharey=True)
    for k, (ax, (title, lo, hi), key) in enumerate(zip(axes, labs, keys)):
        taus = [S["moderation"][key]["taus"][0]["tau"],
                S["moderation"][key]["taus"][-1]["tau"]]
        # the later-peaking curve is always solid and in the accent colour, so
        # that the same colour carries the same meaning in all three panels
        later = int(taus[1] > taus[0])
        for j, lab in enumerate((lo, hi)):
            col, ls = (ACC, "-") if j == later else (NEG, "--")
            x, y = m[k, j, :, 0], m[k, j, :, 1]
            ax.plot(x, y, color=col, ls=ls, lw=1.3, label=lab)
            ax.plot([taus[j]], [np.interp(taus[j], x, y)], marker="o", ms=3.4,
                    color=col)
        ax.axhline(0, color="black", lw=0.6)
        ax.set_title(title, fontsize=7.0, pad=3, linespacing=1.25)
        ax.set_xlabel("Adoption depth", fontsize=7.0)
        ax.grid(alpha=0.25, lw=0.5)
        # each panel's key sits below its own axis, outside the data region
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=1,
                  fontsize=6.4, frameon=False, handlelength=2.0,
                  labelspacing=0.22, borderaxespad=0.0)
    axes[0].set_ylabel("Effect on the youth\nshare (pp)", fontsize=7.0)
    fig.subplots_adjust(wspace=0.12)
    save(fig, "figure5_moderators.png")


# ---------------------------------------------------------------------------
def figure6():
    d = np.load(os.path.join(TAB, "placebo.npy"))
    fig, ax = plt.subplots(figsize=(W, W * 0.42))
    ax.hist(d, bins=32, color="#5D6D7E", ec="white", lw=0.4, density=True,
            label="Placebo draws")
    ax.axvline(S["u_t"], color=NEG, lw=1.8, label="Actual statistic")
    lo, hi = ax.get_ylim()
    # to the left of the line, in the empty middle of the panel
    ax.text(S["u_t"] - 0.4, hi * 0.55, "%.2f" % S["u_t"], fontsize=7.4,
            color=NEG, ha="right", va="center")
    ax.set_xlabel("Lind–Mehlum statistic under random reassignment")
    ax.set_ylabel("Density")
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.26), ncol=2,
              fontsize=6.8, frameon=False)
    save(fig, "figure6_placebo.png")


if __name__ == "__main__":
    figure1(); figure2(); figure3(); figure4(); figure5(); figure6()
