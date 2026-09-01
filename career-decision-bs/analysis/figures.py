# -*- coding: utf-8 -*-
"""The three figures, in the plain idiom this journal uses.

The sample article for this journal carries a conceptual path diagram, a
statistical path diagram bearing coefficients, and a simple-slope plot, all in
black and white with no decoration. These follow the same conventions, with
one deliberate departure: no explanatory note is set beneath any figure.
Anything a note would carry is stated in the body text instead, so that each
figure stands or falls on what it shows.
"""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)

with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
    S = json.load(fh)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 8.5,
    "axes.linewidth": 0.7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "savefig.dpi": 600,
})


def save(fig, name):
    p = os.path.join(FIG, name + ".png")
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("   ", os.path.basename(p))
    return p


def _box(ax, x, y, w, h, label, fs=8.5):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fill=False,
                           linewidth=0.9, edgecolor="black"))
    ax.text(x, y, label, ha="center", va="center", fontsize=fs)
    return dict(l=x - w / 2, r=x + w / 2, t=y + h / 2, b=y - h / 2, x=x, y=y)


def _elbow(ax, pts, dashed=False):
    """An orthogonal path through pts, with the head on the final segment."""
    for a, b in zip(pts[:-2], pts[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color="black", linewidth=0.9,
                linestyle="--" if dashed else "-", solid_capstyle="round")
    _arrow(ax, pts[-2], pts[-1], dashed=dashed)


def _arrow(ax, p0, p1, style="-|>", dashed=False, rad=0.0):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=9,
                                 linewidth=0.9, color="black",
                                 linestyle="--" if dashed else "-",
                                 connectionstyle="arc3,rad=%.2f" % rad,
                                 shrinkA=0, shrinkB=0))


# ===========================================================================
def figure1():
    """The process the model represents: a loop, not a chain."""
    fig, ax = plt.subplots(figsize=(6.1, 3.9))
    ax.set_xlim(-11, 102); ax.set_ylim(1, 66); ax.axis("off")

    anx = _box(ax, 14, 44, 22, 10, "Career\nanxiety")
    exp = _box(ax, 50, 44, 22, 10, "Career\nexploration")
    eff = _box(ax, 87, 44, 24, 10, "Decision-making\nself-efficacy", fs=7.4)
    unc = _box(ax, 50, 13, 24, 10, "Unresolved\nuncertainty")
    dif = _box(ax, 88, 13, 20, 10, "Decision\ndifficulty")
    sup = _box(ax, 12, 13, 20, 10, "Parental\ninvolvement")

    # across the top: anxiety suppresses looking, looking builds efficacy,
    # efficacy makes more looking possible
    _arrow(ax, (anx["r"], 45.6), (exp["l"], 45.6))
    ax.text(32.5, 47.1, "avoidance", ha="center", fontsize=7.0, style="italic")
    _arrow(ax, (exp["r"], 45.6), (eff["l"], 45.6))
    ax.text(68.5, 47.1, "mastery", ha="center", fontsize=7.0, style="italic")
    _arrow(ax, (eff["l"], 42.4), (exp["r"], 42.4))
    ax.text(68.5, 39.2, "capability", ha="center", fontsize=7.0, style="italic")

    # anxiety degrades the yield of looking: a moderation of the mastery path
    _arrow(ax, (anx["x"] + 4, anx["t"]), (68.5, 51.4), dashed=True, rad=-0.26)
    ax.text(68.5, 57.6, "interference with yield", ha="center", fontsize=7.0,
            style="italic")

    # the loop closes through uncertainty
    _arrow(ax, (exp["x"], exp["b"]), (unc["x"], unc["t"]))
    ax.text(51.8, 28.0, "resolves", ha="left", fontsize=7.0, style="italic")
    # the return leg is routed outside the frame: any diagonal from
    # uncertainty back to anxiety would cross the scaffolding path
    _elbow(ax, [(unc["x"], unc["b"]), (unc["x"], 3.5), (-4.5, 3.5),
                (-4.5, anx["y"]), (anx["l"], anx["y"])])
    ax.text(-6.9, 30.0, "sustains", ha="center", fontsize=7.0, style="italic",
            rotation=90)

    _arrow(ax, (unc["r"], unc["y"]), (dif["l"], dif["y"]))

    # parental involvement enters three times, and which of the three
    # predominates is what the study varies
    _arrow(ax, (5.0, sup["t"]), (5.0, anx["b"]), dashed=True)
    ax.text(1.8, 28.0, "reassures", ha="center", fontsize=7.0, style="italic",
            rotation=90)
    _arrow(ax, (sup["r"], 11.4), (unc["l"], 11.4), dashed=True)
    ax.text(30.0, 13.8, "takes over", ha="center", fontsize=7.0, style="italic")
    _arrow(ax, (sup["r"] - 3, sup["t"]), (exp["l"] + 1, exp["b"]), dashed=True,
           rad=-0.22)
    ax.text(27.8, 30.8, "scaffolds", ha="right", fontsize=7.0, style="italic")
    return save(fig, "figure1_model")


# ===========================================================================
def figure2():
    """Two trajectories: the composed and the anxious quartile."""
    tr = np.load(os.path.join(TAB, "traj_by_trait.npy"))
    u_lo, u_hi, s_lo, s_hi = tr
    w = np.arange(u_lo.size)

    fig, axes = plt.subplots(1, 2, figsize=(6.1, 2.6))
    for ax, (a, b, lab) in zip(axes, [(u_lo, u_hi, "Unresolved uncertainty"),
                                      (s_lo, s_hi, "Decision-making self-efficacy")]):
        ax.plot(w, a, color="black", lw=1.4, label="Lowest anxiety quartile")
        ax.plot(w, b, color="black", lw=1.4, ls="--",
                label="Highest anxiety quartile")
        ax.set_xlabel("Week of the decision horizon")
        ax.set_ylabel(lab)
        ax.set_xlim(0, w[-1])
        ax.margins(y=0.12)
    axes[0].legend(frameon=False, fontsize=7.4, loc="upper right",
                   handlelength=2.2, borderaxespad=0.4)
    fig.tight_layout()
    return save(fig, "figure2_trajectories")


# ===========================================================================
def figure3():
    """How the moderation depends on the kind of involvement, and what the
    two extreme kinds imply for the anxiety slope."""
    rows = [l.rstrip("\n").split("\t") for l in
            open(os.path.join(TAB, "t04_moderation.tsv"), encoding="utf-8")]
    body = rows[1:]
    pi = np.array([float(r[0]) for r in body])
    inter = np.array([float(r[3]) for r in body])
    lo = np.array([float(r[5]) for r in body])
    hi = np.array([float(r[6]) for r in body])

    fig, axes = plt.subplots(1, 2, figsize=(6.1, 2.7))

    ax = axes[0]
    ax.plot(pi, inter, color="black", lw=1.4, marker="o", ms=3.4)
    ax.axhline(0, color="black", lw=0.6, ls=":")
    ax.set_xlabel("Directive share of parental involvement")
    ax.set_ylabel("Anxiety × involvement interaction")
    ax.set_xlim(-0.04, 1.04)

    # simple slopes at low and high involvement, under the calibrated regime
    ref = S["reference_study"]
    ax = axes[1]
    x = np.array([-1.0, 0.0, 1.0])
    for slope, ls, lab in ((ref["slope_lo"], "-", "Low involvement (−1 SD)"),
                           (ref["slope_hi"], "--", "High involvement (+1 SD)")):
        ax.plot(x, slope * x, color="black", lw=1.4, ls=ls, label=lab)
    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels(["−1 SD", "Mean", "+1 SD"])
    ax.set_xlabel("Career anxiety")
    ax.set_ylabel("Predicted decision difficulty")
    ax.axhline(0, color="black", lw=0.6, ls=":")
    ax.legend(frameon=False, fontsize=7.2, loc="upper left",
              handlelength=2.2, borderaxespad=0.3)
    ax.margins(y=0.22)
    fig.tight_layout()
    return save(fig, "figure3_slopes")


if __name__ == "__main__":
    print("figures:")
    figure1(); figure2(); figure3()
    print("written to", FIG)
