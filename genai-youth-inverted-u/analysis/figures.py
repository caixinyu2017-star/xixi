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
PUR = "#7D3C98"

S = json.load(open(os.path.join(TAB, "summary.json"), encoding="utf-8"))


def save(fig, name):
    p = os.path.join(FIG, name)
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ---------------------------------------------------------------------------
def figure1():
    """Conceptual framework: two channels, one curve, three moderators."""
    fig, axes = plt.subplots(1, 2, figsize=(W, W * 0.44),
                             gridspec_kw=dict(width_ratios=[1.30, 1.0],
                                              wspace=0.20))
    ax = axes[0]
    ax.set_xlim(0.0, 12.6)
    ax.set_ylim(0.3, 7.6)
    ax.axis("off")
    ax.set_title("(a) Mechanism", fontsize=8.0, pad=2)

    def box(x, y, w, h, text, fc, fs=6.5):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.05,rounding_size=0.10",
                                    fc=fc, ec=GREY, lw=0.9, zorder=3))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4,
                linespacing=1.35)

    def arrow(p, q, color=GREY, ls="-", lw=1.15):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=9,
                                     lw=lw, color=color, linestyle=ls,
                                     shrinkA=0, shrinkB=0, zorder=2))

    box(1.85, 3.95, 3.3, 1.55, "Generative AI\nadoption\ndepth", "#EAF2F8")
    box(10.75, 3.95, 3.3, 1.55, "Youth\nemployment\nshare", "#FEF9E7")
    box(6.30, 6.55, 4.0, 1.15, "Augmentation of\nentry-level work", "#E8F6F3")
    box(6.30, 1.35, 4.0, 1.15, "Automation of the\nentry task bundle", "#FDEDEC")

    arrow((1.85, 4.75), (4.15, 6.10), POS)
    ax.text(3.60, 5.85, "concave", ha="right", va="center", fontsize=6.2,
            color=POS, style="italic")
    arrow((8.45, 6.10), (10.75, 4.75), POS)
    ax.text(9.30, 5.85, "+", ha="left", va="center", fontsize=8.4, color=POS,
            fontweight="bold")
    arrow((1.85, 3.15), (4.15, 1.80), NEG)
    ax.text(3.60, 2.05, "convex", ha="right", va="center", fontsize=6.2,
            color=NEG, style="italic")
    arrow((8.45, 1.80), (10.75, 3.15), NEG)
    ax.text(9.30, 2.05, "\u2212", ha="left", va="center", fontsize=8.4,
            color=NEG, fontweight="bold")

    arrow((3.55, 3.95), (9.05, 3.95), GREY, ls=(0, (4, 2)), lw=1.0)
    ax.text(6.30, 4.14, "H1: inverted U", ha="center", va="bottom",
            fontsize=6.8, color=GREY, fontweight="bold")

    # ---- panel (b): the curve and the three moderators --------------------
    ax = axes[1]
    ax.set_title("(b) Displacement of the turning point", fontsize=8.0, pad=2)
    x = np.linspace(0, 4.6, 200)
    for shift, col, ls, lab in ((-0.55, NEG, "--", "peak brought forward (H2c)"),
                                (0.0, GREY, "-", "baseline"),
                                (0.55, ACC, "-.", "peak delayed (H2a, H2b)")):
        tau = 2.15 + shift
        y = 2.0 * tau * x - 1.0 * x ** 2
        ax.plot(x, y, color=col, ls=ls, lw=1.3, label=lab)
        ax.plot([tau], [tau ** 2], marker="o", ms=3.2, color=col)
    ax.axhline(0, color="black", lw=0.7)
    ax.set_xlabel("Adoption depth")
    ax.set_ylabel("Youth employment share")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=1,
              fontsize=6.4, frameon=False, handlelength=2.4,
              labelspacing=0.25)
    save(fig, "figure1_framework.png")


def figure2():
    df = pd.read_csv(os.path.join(DATA, "panel.csv"))
    g = df.groupby("year").agg(depth=("AI", "mean"),
                               share=("AI", lambda s: 100 * (s > 0).mean()),
                               youth=("Youth", "mean"))
    fig, ax = plt.subplots(figsize=(W, W * 0.50))
    ax2 = ax.twinx()
    l1, = ax.plot(g.index, g.youth, color=NEG, marker="o", ms=3.6,
                  label="Youth employment share (left axis)")
    l2, = ax2.plot(g.index, g.depth, color=POS, marker="s", ms=3.6, ls="--",
                   label="Mean adoption depth (right axis)")
    l3, = ax2.plot(g.index, g.share / 100 * 3, color=ACC, marker="^", ms=3.6,
                   ls="-.", label="Share of firms reporting adoption (right axis, ×3)")
    ax.axvline(2022.5, color=GREY, lw=0.9, ls=":")
    ax.text(2022.35, 0.97, "public release of\nlarge language models",
            transform=ax.get_xaxis_transform(), fontsize=6.6, color=GREY,
            ha="right", va="top")
    ax.set_xlabel("Year")
    ax.set_ylabel("Share of employees aged 30 or below (%)")
    ax2.set_ylabel("Adoption depth")
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(handles=[l1, l2, l3], loc="upper center",
              bbox_to_anchor=(0.5, -0.19), ncol=1, fontsize=6.8,
              frameon=False, handlelength=2.6, labelspacing=0.3)
    save(fig, "figure2_trends.png")


def figure3():
    c = np.load(os.path.join(TAB, "curve.npy"))
    b = pd.read_csv(os.path.join(TAB, "bins.csv"))
    x, fit, se = c[:, 0], c[:, 1], c[:, 2]
    fig, ax = plt.subplots(figsize=(W, W * 0.50))
    ax.axhline(0, color="black", lw=0.7)
    ax.plot(x, fit, color=NEG, lw=1.6, label="Fitted quadratic")
    ax.fill_between(x, fit - 1.96 * se, fit + 1.96 * se, color=NEG, alpha=0.14,
                    label="95% confidence band")

    tau = S["tau"]
    ax.axvline(tau, color=ACC, lw=1.1, ls="--")
    ax.axvspan(S["tau_lo"], S["tau_hi"], color=ACC, alpha=0.12)
    peak = S["b1"] * tau + S["b2"] * tau ** 2
    ax.plot([tau], [peak], marker="o", ms=4.2, color=ACC, zorder=5)

    # binned means, re-based on the lowest bin so that they sit on the same
    # "relative to no adoption" scale as the fitted curve
    by = b["y"] - b["y"].iloc[0] + np.interp(b["x"].iloc[0], x, fit)
    ax.plot(b["x"], by, ls="none", marker="D", ms=3.0, color=GREY, alpha=0.8,
            label="Residualised binned means")

    ax.annotate("extreme point %.2f  [%.2f, %.2f]"
                % (tau, S["tau_lo"], S["tau_hi"]),
                xy=(tau, peak), xytext=(10, 14), textcoords="offset points",
                fontsize=6.8, color=ACC, ha="left",
                arrowprops=dict(arrowstyle="-", lw=0.7, color=ACC))
    ax.set_xlabel("Generative AI adoption depth")
    ax.set_ylabel("Effect on the youth employment share (pp)")
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.19), ncol=2,
              fontsize=6.8, frameon=False)
    save(fig, "figure3_curve.png")


def figure4():
    d = np.load(os.path.join(TAB, "decomp.npy"))
    x, aug, aut = d[:, 0], d[:, 1], d[:, 2]
    fig, ax = plt.subplots(figsize=(W, W * 0.50))
    ax.axhline(0, color="black", lw=0.7)
    ax.plot(x, aug, color=ACC, lw=1.4, label="Augmentation channel (concave)")
    ax.plot(x, aut, color=NEG, lw=1.4, ls="--",
            label="Automation channel (convex)")
    ax.plot(x, aug + aut, color=GREY, lw=1.8, ls="-",
            label="Net effect")
    xt = x[np.argmax(aug + aut)]
    ax.axvline(xt, color=GREY, lw=0.9, ls=":")
    ax.annotate("the two channels cross", xy=(xt, 0), xytext=(8, 30),
                textcoords="offset points", fontsize=6.8, color=GREY,
                arrowprops=dict(arrowstyle="-", lw=0.7, color=GREY))
    ax.set_xlabel("Generative AI adoption depth")
    ax.set_ylabel("Contribution to the youth\nemployment share (pp)")
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.19), ncol=1,
              fontsize=6.8, frameon=False, labelspacing=0.3)
    save(fig, "figure4_channels.png")


def figure5():
    m = np.load(os.path.join(TAB, "modcurves.npy"))
    labs = [("Organisational learning capability", "−1 SD", "+1 SD"),
            ("AI governance", "not disclosed", "disclosed"),
            ("Labour cost pressure", "−1 SD", "+1 SD")]
    keys = ["OLC", "AIGov", "LCP"]
    fig, axes = plt.subplots(1, 3, figsize=(W, W * 0.36), sharey=True)
    for k, (ax, (title, lo, hi), key) in enumerate(zip(axes, labs, keys)):
        taus = [S["moderation"][key]["taus"][0]["tau"],
                S["moderation"][key]["taus"][-1]["tau"]]
        # the later-peaking curve is always drawn solid and in the accent
        # colour, so that the same colour carries the same meaning in all three
        # panels irrespective of which level of the moderator delays the peak
        later = int(taus[1] > taus[0])
        for j, lab in enumerate((lo, hi)):
            col, ls = (ACC, "-") if j == later else (NEG, "--")
            x, y = m[k, j, :, 0], m[k, j, :, 1]
            ax.plot(x, y, color=col, ls=ls, lw=1.3, label=lab)
            ax.plot([taus[j]], [np.interp(taus[j], x, y)], marker="o", ms=3.4,
                    color=col)
        ax.axhline(0, color="black", lw=0.6)
        ax.set_title(title, fontsize=6.9, pad=3)
        ax.set_xlabel("Adoption depth", fontsize=7.0)
        ax.grid(alpha=0.25, lw=0.5)
        ax.legend(loc="lower left", fontsize=6.2, frameon=False,
                  handlelength=1.8, labelspacing=0.2)
    axes[0].set_ylabel("Effect on the youth\nshare (pp)", fontsize=7.0)
    fig.subplots_adjust(wspace=0.10)
    save(fig, "figure5_moderators.png")


def figure6():
    d = np.load(os.path.join(TAB, "placebo.npy"))
    fig, ax = plt.subplots(figsize=(W, W * 0.46))
    ax.hist(d, bins=32, color="#5D6D7E", ec="white", lw=0.4, density=True)
    ax.axvline(S["u_t"], color=NEG, lw=1.6)
    ax.annotate("actual statistic\n%.2f" % S["u_t"],
                (S["u_t"], ax.get_ylim()[1] * 0.6),
                textcoords="offset points", xytext=(-8, 0), fontsize=7.0,
                color=NEG, ha="right")
    ax.set_xlabel("Lind–Mehlum statistic under random reassignment")
    ax.set_ylabel("Density")
    ax.grid(alpha=0.25, lw=0.5)
    ax.text(0.02, 0.95, "%d permutations of adoption depth within year"
            % S["placebo_n"], transform=ax.transAxes, fontsize=6.8, va="top")
    save(fig, "figure6_placebo.png")


if __name__ == "__main__":
    figure1(); figure2(); figure3(); figure4(); figure5(); figure6()
