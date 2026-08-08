# -*- coding: utf-8 -*-
"""The three figures reported in the manuscript. All three are data figures.

Drawn to the Nature Portfolio conventions encoded in ``natureplot``: one
sans-serif family at fixed print sizes, bold lower-case panel letters placed
from the measured extent of each panel, left and bottom spines with outward
ticks, opaque confidence bands with hairline limits, the Okabe and Ito
colourblind-safe palette, and direct labelling everywhere — no figure carries
a boxed legend, so nothing can occlude the data. Every figure is constructed
at the 132 mm width at which the Word file places it, with panels positioned
in millimetres.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd

import natureplot as N

N.use()

import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
FIG = os.path.abspath(os.path.join(HERE, "..", "figures"))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
os.makedirs(FIG, exist_ok=True)


def load():
    with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
        return json.load(fh)


def _panel_pair(fig, H):
    """Two main panels over two density strips, positioned in millimetres."""
    wide = (N.TEXT - 18.0 - 3.0 - 16.0) / 2.0
    main, strip = [], []
    for i in range(2):
        x = 18.0 + i * (wide + 16.0)
        st = N.axes_mm(fig, x, 11.5, wide, 3.2)
        mn = N.axes_mm(fig, x, 15.2, wide, 32.5)
        mn.sharex(st)
        mn.tick_params(axis="x", labelbottom=False, length=0)
        mn.spines["bottom"].set_visible(False)
        main.append(mn)
        strip.append(st)
    return main, strip


def _density(ax, S, label="density"):
    from scipy.stats import gaussian_kde
    lo, hi = S["grid_lo"], S["grid_hi"]
    d = np.array(S["anx_density"], float)
    edges = np.linspace(lo, hi, len(d) + 1)
    mids = 0.5 * (edges[:-1] + edges[1:])
    grid = np.linspace(lo, hi, 300)
    kd = gaussian_kde(mids, weights=d, bw_method=0.25)(grid)
    ax.fill_between(grid, 0.0, kd / kd.max(), color=N.FAINT, lw=0)
    ax.set_ylim(0, 1.08)
    ax.set_yticks([])
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_ylabel(label, fontsize=N.PT_TICK, color=N.GREY, rotation=0,
                  ha="right", va="center", labelpad=3.0)


def _curve(ax, rows, color=N.BLUE):
    z = np.array([r["z"] for r in rows])
    m = np.array([r["effect"] for r in rows])
    se = np.array([r["se"] for r in rows])
    N.band(ax, z, m - 1.96 * se, m + 1.96 * se, color=color)
    ax.plot(z, m, color=color, lw=1.1, zorder=2)
    return z, m


# ===========================================================================
def figure1_dual(S):
    """The dual response: adaptation follows an inverted U in anxiety while
    avoidance rises monotonically. The two panels share one vertical scale so
    the asymmetry can be read directly, and the observed distribution of
    anxiety sits beneath each panel."""
    H = 56.0
    fig = N.figure(N.TEXT, H)
    main, strip = _panel_pair(fig, H)

    # ---- a: adaptation ---------------------------------------------------
    ax = main[0]
    z, m = _curve(ax, S["curve_adp"])
    ax.set_xlim(z.min(), z.max())
    N.zeroline(ax)
    tp = S["tp"]
    ax.axvspan(tp["ci_low"], tp["ci_high"], color=N.SHADE, lw=0, zorder=0.3)
    j = int(np.argmin(np.abs(z - tp["tau"])))
    ax.plot([tp["tau"]], [m[j]], marker="o", ms=3.2, color=N.BLUE,
            mec="white", mew=0.5, zorder=3)
    ax.annotate("turning point %.2f\n95%% CI [%.2f, %.2f]"
                % (tp["tau"], tp["ci_low"], tp["ci_high"]),
                xy=(tp["ci_high"] + 0.10, 0.06),
                xycoords=("data", "axes fraction"), ha="left", va="bottom",
                fontsize=N.PT_TICK, color=N.INK)
    ax.set_title("Occupational adaptation", fontsize=N.PT_LABEL, loc="left",
                 pad=3.0)
    ax.set_ylabel("Predicted outcome\n(SD units; 0 = sample mean)")

    # ---- b: avoidance ----------------------------------------------------
    ax = main[1]
    z2, m2 = _curve(ax, S["curve_avd"])
    ax.set_xlim(z2.min(), z2.max())
    N.zeroline(ax)
    ax.set_title("Career avoidance", fontsize=N.PT_LABEL, loc="left",
                 pad=3.0)

    lo = min(a.get_ylim()[0] for a in main)
    hi = max(a.get_ylim()[1] for a in main)
    for a, st in zip(main, strip):
        a.set_ylim(lo, hi)
        N.snap(a, x=False)
        _density(st, S)
        N.snap(st, y=False)
    main[1].set_yticklabels([])
    fig.text((18.0 + N.TEXT - 3.0) / 2.0 / N.TEXT, 2.6 / H,
             "AI-related career anxiety (SD from the mean)",
             ha="center", va="bottom", fontsize=N.PT_LABEL, color=N.INK)
    N.panels(fig, [(main[0], "a"), (main[1], "b")])
    return N.save(fig, os.path.join(FIG, "figure1_dual"))


# ===========================================================================
def figure2_boundaries(S):
    """The two boundary conditions. Panel a: generative-AI literacy shifts
    the turning point of the adaptation response outward without changing its
    curvature; the series are labelled directly at their peaks, so there is
    no legend to collide with the data. Panel b: employability support
    flattens the first stage."""
    H = 56.0
    fig = N.figure(N.TEXT, H)
    main, strip = _panel_pair(fig, H)

    # ---- a: second stage at low and high literacy ------------------------
    ax = main[0]
    tps = {m["z"]: m for m in S["tp_lit"]}
    for rows, col, lv, lab in (
            (S["curve_adp_litlo"], N.ORANGE, -1.0, "literacy −1 SD"),
            (S["curve_adp_lithi"], N.BLUE, +1.0, "literacy +1 SD")):
        z = np.array([r["z"] for r in rows])
        m = np.array([r["effect"] for r in rows])
        se = np.array([r["se"] for r in rows])
        N.band(ax, z, m - 1.96 * se, m + 1.96 * se, color=col)
        ax.plot(z, m, color=col, lw=1.1, zorder=2)
        t = tps[lv]["tau"]
        j = int(np.argmin(np.abs(z - t)))
        ax.plot([t], [m[j]], marker="o", ms=3.0, color=col, mec="white",
                mew=0.5, zorder=3)
        # label each series at its left-hand end, anchored at its own band
        # limit rather than its mean, so the text clears the band entirely:
        # the low-literacy label above its band, the high-literacy label
        # below its band, both over bare paper
        if lv < 0:
            ax.annotate(lab, xy=(z[0], m[0] + 1.96 * se[0]), xytext=(2, 4),
                        textcoords="offset points", ha="left", va="bottom",
                        fontsize=N.PT_TICK, color=col)
        else:
            ax.annotate(lab, xy=(z[0], m[0] - 1.96 * se[0]), xytext=(2, -4),
                        textcoords="offset points", ha="left", va="top",
                        fontsize=N.PT_TICK, color=col)
        ax.set_xlim(z.min(), z.max())
    N.zeroline(ax)
    ax.set_title("Adaptation, by literacy", fontsize=N.PT_LABEL, loc="left",
                 pad=3.0)
    ax.set_ylabel("Predicted adaptation (SD units)")
    _density(strip[0], S)

    # ---- b: first stage across support -----------------------------------
    ax = main[1]
    rows = S["firststage"]
    z = np.array([r["z"] for r in rows])
    m = np.array([r["effect"] for r in rows])
    se = np.array([r["se"] for r in rows])
    N.band(ax, z, m - 1.96 * se, m + 1.96 * se)
    ax.plot(z, m, color=N.BLUE, lw=1.1, zorder=2)
    ax.set_xlim(z.min(), z.max())
    N.zeroline(ax)
    for sv, key in ((-1.0, "fslo"), (1.0, "fshi")):
        e = S[key]
        j = int(np.argmin(np.abs(z - sv)))
        ax.plot([sv], [m[j]], marker="o", ms=2.8, color=N.BLUE, mec="white",
                mew=0.4, zorder=3)
        # anchored at the band's upper limit, so the number sits on paper
        ax.annotate("%.2f" % e["est"], xy=(sv, m[j] + 1.96 * se[j]),
                    xytext=(0, 3), textcoords="offset points", ha="center",
                    va="bottom", fontsize=N.PT_TICK, color=N.INK)
    ax.set_title("First stage, by support", fontsize=N.PT_LABEL, loc="left",
                 pad=3.0)
    ax.set_ylabel("Effect of depreciation on\nanxiety (SD units)")
    ax.set_ylim(bottom=0.0)

    # the strip under panel b shows the support distribution
    st = strip[1]
    d = pd.read_csv(os.path.join(DATA, "survey.csv"))
    d = d[d.retained == 1]
    sup = d[["sup1", "sup2", "sup3", "sup4"]].mean(axis=1)
    supz = (sup - sup.mean()) / sup.std()
    from scipy.stats import gaussian_kde
    grid = np.linspace(-2, 2, 200)
    kd = gaussian_kde(supz.to_numpy())(grid)
    st.fill_between(grid, 0, kd / kd.max(), color=N.FAINT, lw=0)
    st.set_ylim(0, 1.08)
    st.set_yticks([])
    for side in ("left", "right", "top"):
        st.spines[side].set_visible(False)
    st.set_ylabel("density", fontsize=N.PT_TICK, color=N.GREY, rotation=0,
                  ha="right", va="center", labelpad=3.0)

    for a in main:
        N.snap(a, x=False)
    for stx in strip:
        N.snap(stx, y=False)
    strip[0].set_xlabel("AI-related career anxiety (SD)")
    strip[1].set_xlabel("Perceived employability support (SD)")
    N.panels(fig, [(main[0], "a"), (main[1], "b")])
    return N.save(fig, os.path.join(FIG, "figure2_boundaries"))


# ===========================================================================
def figure3_generality(S):
    """Panel a: the marginal effect of anxiety on adaptation at the sample
    mean, subgroup by subgroup — the mechanism is a property of the cohort,
    not of one stratum. Panel b: the single sufficient configuration from the
    fuzzy-set analysis, each respondent a point; sufficiency is the scarcity
    of points below the diagonal."""
    H = 64.0
    fig = N.figure(N.TEXT, H)
    ax1 = N.axes_mm(fig, 34.0, 13.0, 40.0, 44.0)
    ax2 = N.axes_mm(fig, 95.0, 13.0, 34.0, 44.0)

    # ---- a: forest -------------------------------------------------------
    ax = ax1
    F = S["forest"]
    ys = []
    y = 0.0
    for i, f in enumerate(F):
        if i % 2 == 0 and i > 0:
            y -= 0.6                        # gap between pairs
        ys.append(y)
        y -= 1.0
    for f, yy in zip(F, ys):
        lo, hi = f["me"] - 1.96 * f["se"], f["me"] + 1.96 * f["se"]
        ax.plot([lo, hi], [yy, yy], color=N.BLUE, lw=1.0,
                solid_capstyle="butt", zorder=2)
        ax.plot([f["me"]], [yy], marker="o", ms=2.8, color=N.BLUE,
                mec="white", mew=0.4, zorder=3)
    ax.axvline(0.0, color=N.GREY, lw=0.5, ls=(0, (2.6, 1.8)), zorder=0.5)
    ax.set_yticks(ys)
    ax.set_yticklabels([f["group"].split(": ")[1] for f in F])
    ax.set_ylim(min(ys) - 0.8, 0.8)
    for side in ("left",):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Marginal effect of anxiety on\nadaptation at the mean (SD)")
    N.snap(ax, y=False)

    # ---- b: sufficiency scatter -----------------------------------------
    ax = ax2
    mem = np.load(os.path.join(TAB, "qca_top_mem.npy"))
    ax.plot([0, 1], [0, 1], color=N.GREY, lw=0.6, zorder=1)
    ax.scatter(mem[:, 0], mem[:, 1], s=2.2, color=N.tint(N.BLUE, 0.65),
               edgecolors="none", zorder=2)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel("Membership in ANX · LIT · SUP")
    ax.set_ylabel("Membership in\nhigh adaptation")
    # no in-panel annotation: with 914 points there is no empty paper for
    # one, and the consistency and coverage are stated in Table 14 and in
    # the body text, where the house rules put them
    N.snap(ax)

    N.panels(fig, [(ax1, "a"), (ax2, "b")])
    return N.save(fig, os.path.join(FIG, "figure3_generality"))


if __name__ == "__main__":
    S = load()
    for out in (figure1_dual(S), figure2_boundaries(S),
                figure3_generality(S)):
        print(" ", os.path.basename(out[0]))
    print("figures written to", FIG)
