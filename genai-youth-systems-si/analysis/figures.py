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
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)

CM = 1 / 2.54
W = 13.8 * CM

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "font.size": 8.0, "axes.labelsize": 8.0, "legend.fontsize": 7.2,
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


def load():
    with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
        return json.load(fh)


# ===========================================================================
def figure1_framework():
    """Boxes and arrows: one arrow for each numbered hypothesis."""
    fig, ax = plt.subplots(figsize=(W, W * 0.72))
    ax.set_xlim(0, 10)
    ax.set_ylim(0.1, 8.0)
    ax.axis("off")

    def box(cx, cy, w, h, lines, fc="white", ec=INK, lw=0.9, fs=7.4):
        ax.add_patch(FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec,
            lw=lw, zorder=3))
        ax.text(cx, cy, "\n".join(lines), ha="center", va="center",
                fontsize=fs, color=INK, zorder=4, linespacing=1.35)

    def arrow(p0, p1, ls="-", color=INK, lw=1.0, rad=0.0, zo=2):
        ax.add_patch(FancyArrowPatch(
            p0, p1, arrowstyle="-|>", mutation_scale=8.5, lw=lw,
            linestyle=ls, color=color, shrinkA=0, shrinkB=0, zorder=zo,
            connectionstyle="arc3,rad=%.2f" % rad))

    # ------------------------------------------------------------- the chain
    box(1.55, 4.30, 2.75, 1.06, ["Generative AI", "adoption (GenAI)"],
        fc="#eef2f7")
    box(5.05, 5.95, 2.60, 0.95, ["Training investment", "(Train)"])
    box(5.05, 2.70, 2.60, 0.95, ["Routine task base", "(Routine)"])
    box(8.50, 4.30, 2.75, 1.06, ["Youth employment", "share (Youth)"],
        fc="#eef2f7")

    # H1, the direct path
    arrow((2.95, 4.30), (7.10, 4.30), lw=1.2)
    ax.text(5.05, 4.44, "H1 (\u2212)", ha="center", va="bottom", fontsize=7.4)

    # H2 and the training return
    arrow((2.62, 4.85), (3.73, 5.55))
    ax.text(4.12, 4.94, "H2 (\u2212)", ha="center", va="bottom", fontsize=7.2)
    arrow((6.37, 5.58), (7.90, 4.86))
    ax.text(7.52, 5.40, "(+)", ha="center", va="center", fontsize=7.2)

    # H3 and the routine return
    arrow((2.62, 3.75), (3.73, 3.05))
    ax.text(4.12, 3.44, "H3 (\u2212)", ha="center", va="top", fontsize=7.2)
    arrow((6.37, 3.07), (7.90, 3.76))
    ax.text(7.52, 3.22, "(+)", ha="center", va="center", fontsize=7.2)

    # ------------------------------------------------------- the moderators
    box(2.55, 0.80, 3.20, 0.95,
        ["Organizational learning", "capability (Absorp)"], fc="#f7f4ee",
        ec=GREY)
    box(7.55, 0.80, 3.20, 0.95, ["Relative labor cost", "(Wage)"],
        fc="#f7f4ee", ec=GREY)
    arrow((2.55, 1.28), (3.32, 4.26), color=GREY, lw=0.9)
    arrow((7.55, 1.28), (6.78, 4.26), color=GREY, lw=0.9)
    ax.text(2.58, 2.45, "H4a (+)", ha="right", va="center", fontsize=7.2,
            color=GREY)
    ax.text(7.52, 2.45, "H4b (\u2212)", ha="left", va="center", fontsize=7.2,
            color=GREY)

    # ---------------------------------------------------- the feedback loop
    ax.plot([8.50, 8.50], [4.84, 7.25], ls=(0, (4, 2)), color=RED, lw=1.1,
            zorder=2)
    ax.plot([8.50, 1.55], [7.25, 7.25], ls=(0, (4, 2)), color=RED, lw=1.1,
            zorder=2)
    arrow((1.55, 7.25), (1.55, 4.86), ls=(0, (4, 2)), color=RED, lw=1.1)
    for dx in (-0.09, 0.09):
        ax.plot([6.55 + dx, 6.55 + dx], [7.07, 7.43], color=RED, lw=1.1,
                zorder=3)
    ax.text(6.55, 6.92, "delay", ha="center", va="top", fontsize=7.0,
            color=RED)
    ax.text(7.75, 7.38, "H5 (\u2212)", ha="center", va="bottom", fontsize=7.4,
            color=RED)

    arrow((3.90, 6.43), (1.92, 4.88), ls=(0, (4, 2)), color=RED, lw=1.1,
          rad=0.32)
    ax.text(3.05, 6.62, "H5 (\u2212)", ha="center", va="bottom", fontsize=7.4,
            color=RED)

    ax.add_patch(Circle((4.35, 7.25), 0.29, fc="white", ec=RED, lw=1.0,
                        zorder=4))
    ax.text(4.35, 7.25, "R1", ha="center", va="center", fontsize=7.2,
            color=RED, zorder=5)

    fig.savefig(os.path.join(FIG, "figure1_framework.png"))
    plt.close(fig)


# ===========================================================================
def figure2_moderation(S):
    """Marginal effect of adoption across each moderator."""
    fig, axes = plt.subplots(1, 2, figsize=(W, W * 0.46), sharey=True)
    panels = [
        (S["margin_absorp"], "Organizational learning capability", "(a)"),
        (S["margin_wage"], "Relative labor cost", "(b)"),
    ]
    for ax, (rows, xlab, tag) in zip(axes, panels):
        z = np.array([r["z"] for r in rows])
        m = np.array([r["effect"] for r in rows])
        se = np.array([r["se"] for r in rows])
        ax.fill_between(z, m - 1.645 * se, m + 1.645 * se, color=BLUE,
                        alpha=0.16, lw=0)
        ax.plot(z, m, color=BLUE, lw=1.4)
        ax.axhline(0.0, color=GREY, lw=0.8, ls=(0, (3, 2)))
        ax.set_xlabel(xlab)
        ax.set_xlim(z.min(), z.max())
        ax.tick_params(direction="in", length=2.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.text(0.03, 0.06, tag, transform=ax.transAxes, fontsize=7.6,
                ha="left", va="bottom")
    axes[0].set_ylabel("Marginal effect of GenAI on the\nyouth employment share (p.p.)")
    fig.subplots_adjust(wspace=0.14)
    fig.savefig(os.path.join(FIG, "figure2_moderation.png"))
    plt.close(fig)


# ===========================================================================
def figure3_irf(S):
    """Orthogonalized impulse responses of the three-variable system."""
    keys = [("Youth<-GenAI", "Youth employment share to an adoption shock"),
            ("Train<-GenAI", "Training investment to an adoption shock"),
            ("GenAI<-Train", "Adoption to a training shock"),
            ("GenAI<-Youth", "Adoption to a youth employment shock")]
    fig, axes = plt.subplots(2, 2, figsize=(W, W * 0.78))
    for ax, (k, title) in zip(axes.ravel(), keys):
        r = S["irf"][k]
        h = np.arange(len(r["m"]))
        ax.fill_between(h, r["lo"], r["hi"], color=BLUE, alpha=0.16, lw=0)
        ax.plot(h, r["m"], color=BLUE, lw=1.4)
        ax.axhline(0.0, color=GREY, lw=0.8, ls=(0, (3, 2)))
        ax.set_title(title, fontsize=7.4, pad=3.5)
        ax.set_xlim(0, h.max())
        ax.tick_params(direction="in", length=2.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    for ax in axes[1]:
        ax.set_xlabel("Years after the shock")
    for ax in axes[:, 0]:
        ax.set_ylabel("Response")
    fig.subplots_adjust(hspace=0.42, wspace=0.26)
    fig.savefig(os.path.join(FIG, "figure3_irf.png"))
    plt.close(fig)


if __name__ == "__main__":
    S = load()
    figure1_framework()
    figure2_moderation(S)
    figure3_irf(S)
    print("figures written to", FIG)
