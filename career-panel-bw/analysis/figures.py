# -*- coding: utf-8 -*-
"""The three figures, in the plain black-and-white idiom this journal uses.

No figure carries an explanatory note. Whatever a note would say is stated in
the body text instead, so that each figure stands or falls on what it shows.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                               # noqa: E402
import numpy as np                                            # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import grid as G                                              # noqa: E402

TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
os.makedirs(FIG, exist_ok=True)

with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
    S = json.load(fh)
R = S["results"]

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 8.2,
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


def illustrative():
    """The case drawn in Figure 3, chosen by a stated rule.

    Among hypotheses whose equality test survives the multiplicity
    correction, that are free of the experience–calendar-time collinearity
    of the balanced men's panel, and whose two estimates carry opposite
    signs, take the one where the divergence is largest once expressed per
    within-person standard deviation of the career input.
    """
    cand = [k for k in R
            if R[k]["equality"]["q"] < .05
            and not R[k]["collinear"]
            and np.sign(R[k]["between"]["b"]) != np.sign(R[k]["within"]["b"])]
    return max(cand, key=lambda k: abs(R[k]["equality"]["diff"])
               * R[k]["sd_within_focal"])


def short(k):
    h = R[k]["hypothesis"]
    return "%s × %s" % (G.LABEL[h["focal"]], G.LABEL[h["mod"]])


# ==========================================================================
def figure1():
    """Single-wave estimates against the two panel estimates, four cases."""
    keys = sorted(R, key=lambda k: R[k]["equality"]["q"])[:4]
    fig, axes = plt.subplots(2, 2, figsize=(6.3, 4.5))
    for ax, k in zip(axes.ravel(), keys):
        r = R[k]
        w = np.array([c["wave"] for c in r["cs"]], float)
        b = np.array([c["b"] for c in r["cs"]])
        se = np.array([c["se"] for c in r["cs"]])
        ax.axhline(0, color="0.75", lw=0.6, zorder=1)
        ax.errorbar(w, b, yerr=1.96 * se, fmt="o", ms=2.8, mfc="white",
                    mec="black", ecolor="0.45", elinewidth=0.7, capsize=1.6,
                    zorder=3, label="single wave")
        ax.axhline(r["between"]["b"], color="black", lw=1.0, ls="--",
                   zorder=2, label="between-person")
        ax.axhline(r["within"]["b"], color="black", lw=1.4, zorder=2,
                   label="within-person")
        ax.set_title("%s   %s" % (k, short(k)), fontsize=8.0, pad=4)
        ax.set_xlabel("Survey year")
        ax.set_ylabel("Interaction estimate")
        ax.margins(x=0.06)
    axes[0, 0].legend(frameon=False, fontsize=7.2, loc="upper left",
                      handlelength=1.6, borderaxespad=0.2)
    fig.tight_layout(pad=0.5, w_pad=1.6, h_pad=1.4)
    save(fig, "figure1_waves")


# ==========================================================================
def figure2():
    """Every hypothesis: the between-person and within-person estimate."""
    keys = [h["key"] for h in G.H]
    lab, bw, ww, flag = [], [], [], []
    for k in keys:
        r = R[k]
        sd = r["sd_within_focal"]
        bw.append(r["between"]["b"] * sd)
        ww.append(r["within"]["b"] * sd)
        lab.append("%s  %s" % (k, short(k)))
        flag.append(r["equality"]["q"] < .05)
    y = np.arange(len(keys))[::-1]
    bw, ww = np.array(bw), np.array(ww)

    fig, ax = plt.subplots(figsize=(6.3, 4.6))
    ax.axvline(0, color="0.75", lw=0.6, zorder=1)
    for i, yi in enumerate(y):
        ax.plot([bw[i], ww[i]], [yi, yi], color="0.55", lw=0.8, zorder=2)
    ax.scatter(bw, y, s=20, facecolor="white", edgecolor="black",
               linewidth=0.8, zorder=3, label="between-person")
    ax.scatter(ww, y, s=20, facecolor="black", edgecolor="black",
               linewidth=0.8, zorder=3, label="within-person")
    ax.set_yticks(y)
    ax.set_yticklabels([l + ("  †" if f else "")
                        for l, f in zip(lab, flag)], fontsize=7.4)
    ax.set_xlabel("Difference in log hourly wage per one within-person "
                  "SD of the career input")
    ax.set_ylim(-0.8, len(keys) - 0.2)
    ax.legend(frameon=False, fontsize=7.6, loc="lower right",
              handlelength=1.0, borderaxespad=0.4)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout(pad=0.4)
    save(fig, "figure2_between_within")


# ==========================================================================
def figure3():
    """The illustrative case, drawn as the wage profile each estimator
    implies."""
    k = illustrative()
    r = R[k]
    h = r["hypothesis"]
    mod = G.LABEL[h["mod"]]
    lo, hi = r["focal_range"]
    t = np.linspace(0, hi, 120)

    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.7), sharey=True)
    for ax, tag, title in ((axes[0], "between", "Between-person"),
                           (axes[1], "within", "Within-person")):
        c = r["profile"][tag]
        for w, ls, name in ((0.0, "--", "not %s" % mod),
                            (1.0, "-", mod)):
            y = (c["focal"] + c["int"] * w) * t + c["sq"] * t ** 2
            ax.plot(t, y, color="black", lw=1.3 if w else 1.0, ls=ls,
                    label=name)
        ax.set_title(title, fontsize=8.4, pad=4)
        ax.set_xlabel("Years of %s" % G.LABEL[h["focal"]])
        ax.margins(x=0.02)
    axes[0].set_ylabel("Predicted log hourly wage,\nrelative to zero tenure")
    axes[1].legend(frameon=False, fontsize=7.4, loc="lower right",
                   handlelength=1.8, borderaxespad=0.4)
    fig.tight_layout(pad=0.4, w_pad=1.2)
    save(fig, "figure3_profile")
    return k


if __name__ == "__main__":
    print("figures:")
    figure1()
    figure2()
    print("   illustrative case:", figure3())
