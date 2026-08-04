# -*- coding: utf-8 -*-
"""The three figures reported in the manuscript.

Drawn to the Nature Portfolio conventions encoded in ``natureplot``: a single
sans-serif family at fixed print sizes, bold lower-case panel letters, left and
bottom spines only with outward ticks, the Okabe and Ito colourblind-safe
palette, direct labelling in place of legends, and vector output alongside the
raster used for placement in the Word file.

Every figure is built at the width at which the Word file places it, and every
panel is positioned in millimetres, so a 6 pt tick label is 6 pt on the printed
page rather than 6 pt multiplied by whatever scale factor a cropped bounding
box happened to imply.

Where a figure carries a quantitative claim the number is written into the
panel, and where an effect is plotted against a moderator the observed
distribution of that moderator is shown underneath it, so a reader can see over
what range the estimate is supported.
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


def _rug(ax, values, frac=0.075, color=N.FAINT):
    lo, hi = ax.get_ylim()
    span = hi - lo
    ax.set_ylim(lo - frac * span * 1.35, hi)
    lo2, hi2 = ax.get_ylim()
    xs = np.linspace(*ax.get_xlim(), 160)
    dens = np.histogram(values, bins=xs)[0].astype(float)
    dens = np.convolve(dens, np.ones(9) / 9.0, mode="same")
    if dens.max() > 0:
        dens = dens / dens.max()
    base = lo2 + 0.012 * (hi2 - lo2)
    ax.fill_between(xs[:-1], base, base + dens * frac * span,
                    color=color, lw=0, zorder=0.2)


# ===========================================================================
def figure1_framework():
    """The conceptual framework.

    The layout is a construction rather than a drawing. The canvas is one grid
    unit to the millimetre; every edge begins and ends at a named point on a
    box boundary, so no endpoint is a hand-typed coordinate and no arrow
    touches the box it points at.

    The grammar is carried by line style: a solid arrow is a path the model
    estimates, a grey line ending in a disc on another path is a condition
    that governs that path, and the double stroke is the requisite-variety
    gate, which is the one feature of this framework a reader must not mistake
    for an ordinary moderator.

    The two enabling conditions are stacked on the left and the two absorption
    channels below, which leaves the right-hand corridor clear for the direct
    path from variety to the outcome. The layout has no edge crossings.
    """
    W, H = N.TEXT, 94.0
    fig, ax = N.canvas(W, H)

    Y_PATH, Y_VAR, Y_GATE, Y_KEY = 46.0, 84.0, 53.0, 3.0
    X_GATE = 52.0

    var = N.dbox(ax, X_GATE, Y_VAR, 58, 11,
                 ["Workforce skill variety",
                  "= related variety + unrelated variety"], focal=True)
    dig = N.dbox(ax, 19, 72.0, 30, 8, ["Digital capability"])
    sla = N.dbox(ax, 19, 61.0, 30, 8, ["Financial slack"])
    sho = N.dbox(ax, 20, Y_PATH, 32, 11, ["Industry demand", "shock"],
                 focal=True)
    you = N.dbox(ax, 112, Y_PATH, 36, 12, ["Youth employment", "share"],
                 focal=True)
    red = N.dbox(ax, 64, 25.0, 36, 8.5, ["Internal redeployment"], edge=N.INK)
    chu = N.dbox(ax, 64, 13.0, 36, 8.5, ["Workforce churn"], edge=N.INK)

    # ---- the disturbance -------------------------------------------------
    N.dpath(ax, N.anchor(sho, "r"), N.anchor(you, "l"))
    N.hlabel(ax, 43.0, Y_PATH, "(−)")

    # ---- the regulatory capacity, switched on at the requisite level -----
    N.dcond(ax, N.anchor(var, "b", 0.5), (X_GATE, Y_PATH), color=N.INK,
            lw=N.W_SUB, r=0.8)
    N.dgate(ax, X_GATE, Y_GATE, angle=0.0, half=2.2)
    N.hlabel(ax, X_GATE + 3.0, 74.0, "H2 (+), H3", ha="left")
    N.hlabel(ax, X_GATE + 3.0, Y_GATE, "H5: gate at $\\gamma$", ha="left",
             color=N.ACCENT)

    # ---- variety also raises the level of the outcome --------------------
    N.dpath(ax, N.anchor(var, "r"), N.anchor(you, "t", 0.5), rad=-0.16)
    N.hlabel(ax, 103.0, 70.0, "H1 (+)")

    # ---- the two enabling conditions, entering from the clear left -------
    for box, lab in ((dig, "H6a (+)"), (sla, "H6b (+)")):
        p = N.anchor(box, "r")
        N.dcond(ax, p, (X_GATE, p[1]))
        N.hlabel(ax, (p[0] + X_GATE) / 2, p[1] + 2.6, lab, color=N.GREY)

    # ---- the two absorption channels -------------------------------------
    for box, src_frac, dst_frac in ((red, 0.28, 0.17), (chu, 0.08, 0.5)):
        a, b = N.anchor(sho, "b", src_frac), N.anchor(box, "l", 0.5)
        N.dpath(ax, a, b, lw=N.W_SUB)
        N.hlabel(ax, *N.mid(a, b), "H4") if box is red else None
        c, d = N.anchor(box, "r", 0.5), N.anchor(you, "b", dst_frac)
        N.dpath(ax, c, d, lw=N.W_SUB)

    N.keystrip(ax, Y_KEY, [4.0, 42.0, 84.0], [
        ("solid", "estimated path"),
        ("cond", "enabling condition"),
        ("gate", "requisite-variety gate"),
    ])

    return N.save(fig, os.path.join(FIG, "figure1_framework"))


# ===========================================================================
def figure2_margins(S):
    """Marginal effect of the demand shock across the variety measures."""
    d = pd.read_csv(os.path.join(DATA, "panel.csv"))
    fig = N.figure(N.TEXT, 58.0)
    axes = N.row(fig, 2, left=18.0, bottom=15.0, height=38.0, gutter=16.0)

    # ---- a: total variety, with the estimated threshold marked ------------
    ax = axes[0]
    rows = S["margin_variety"]
    z = np.array([r["z"] for r in rows])
    m = np.array([r["effect"] for r in rows])
    se = np.array([r["se"] for r in rows])
    ax.fill_between(z, m - 1.645 * se, m + 1.645 * se, color=N.BLUE,
                    alpha=0.20, lw=0, zorder=1.5)
    ax.plot(z, m, color=N.BLUE, lw=1.1, zorder=2)
    N.zeroline(ax)
    ax.set_xlim(z.min(), z.max())
    g = S["thr"]["gamma"]
    ax.axvline(g, color=N.ACCENT, lw=0.7, ls=(0, (3.0, 1.8)), zorder=1.2)
    lo, hi = ax.get_ylim()
    ax.annotate("$\\hat{\\gamma}$ = %.2f" % g, xy=(g, hi),
                xytext=(g - 0.08, hi - 0.03 * (hi - lo)),
                ha="right", va="top", fontsize=N.PT_TICK, color=N.ACCENT)
    ax.set_xlabel("Workforce skill variety (bits)")
    ax.set_ylabel("Marginal effect on the youth\n"
                  "employment share (p.p.)")
    _rug(ax, d.Variety.to_numpy())

    # ---- b: the two components, per bit, over their observed support ------
    ax = axes[1]
    for key, col, lab, mu, sd in (
            ("margin_rel", N.BLUE, "Related", S["mean_RelVar"],
             S["sd_RelVar"]),
            ("margin_unrel", N.ORANGE, "Unrelated", S["mean_UnrelVar"],
             S["sd_UnrelVar"])):
        rr = S[key]
        x = mu + np.array([r["z"] for r in rr]) * sd
        mm = np.array([r["effect"] for r in rr])
        ss = np.array([r["se"] for r in rr])
        keep = x >= 0.0
        ax.fill_between(x[keep], (mm - 1.645 * ss)[keep],
                        (mm + 1.645 * ss)[keep], color=col, alpha=0.16, lw=0,
                        zorder=1.5)
        ax.plot(x[keep], mm[keep], color=col, lw=1.1, zorder=2)
        xe, ye = x[keep][-1], mm[keep][-1]
        ax.annotate(lab, xy=(xe, ye), xytext=(xe - 0.08, ye + 0.06), color=col,
                    fontsize=N.PT_TICK, ha="right", va="bottom",
                    annotation_clip=False)
    N.zeroline(ax)
    ax.set_xlim(0.0, 3.05)
    ax.set_xlabel("Variety component (bits)")
    ax.set_ylabel("Marginal effect on the youth\n"
                  "employment share (p.p.)")
    ax.text(0.97, 0.05, "slope ratio %.2f" % S["ratio_ru"],
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=N.PT_TICK, color=N.INK)

    N.panel(fig, axes[0], "a", dx=-15.0)
    N.panel(fig, axes[1], "b", dx=-15.0)
    return N.save(fig, os.path.join(FIG, "figure2_margins"))


# ===========================================================================
def figure3_threshold(S):
    """The requisite-variety threshold and the regime coefficients."""
    T = S["thr"]
    fig = N.figure(N.TEXT, 58.0)
    ax1 = N.axes_mm(fig, 18.0, 15.0, 57.0, 38.0)
    ax2 = N.axes_mm(fig, 93.0, 15.0, 36.0, 38.0)

    # ---- a: the likelihood-ratio profile ---------------------------------
    ax = ax1
    g = np.array(T["grid"])
    lr = np.array(T["lr"])
    ok = np.isfinite(lr)
    ax.axvspan(T["ci_low"], T["ci_high"], color=N.ACCENT, alpha=0.10, lw=0,
               zorder=0.4)
    ax.plot(g[ok], lr[ok], color=N.BLUE, lw=1.0, zorder=2)
    ax.axhline(T["crit"], color=N.ACCENT, lw=0.7, ls=(0, (3.0, 1.8)),
               zorder=1.2)
    ax.axvline(T["gamma"], color=N.ACCENT, lw=0.7, zorder=1.4)
    ax.set_xlim(g.min(), g.max())
    ax.set_xlabel("Candidate threshold in workforce\nskill variety (bits)")
    ax.set_ylabel("Likelihood ratio")
    ax.text(0.40, 0.88, "95%% critical value %.2f" % T["crit"],
            transform=ax.transAxes, ha="left", va="bottom",
            fontsize=N.PT_TICK, color=N.ACCENT,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.0))
    ax.text(0.40, 0.80,
            "$\\hat{\\gamma}$ = %.2f  [%.2f, %.2f]"
            % (T["gamma"], T["ci_low"], T["ci_high"]),
            transform=ax.transAxes, ha="left", va="bottom",
            fontsize=N.PT_TICK, color=N.ACCENT,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.0))

    # ---- b: the regime coefficients --------------------------------------
    ax = ax2
    pts = [(0.0, T["b_low"], T["se_low"], "below $\\hat{\\gamma}$"),
           (1.0, T["b_high"], T["se_high"], "above $\\hat{\\gamma}$")]
    for x, b, se, lab in pts:
        ax.plot([x, x], [b - 1.96 * se, b + 1.96 * se], color=N.BLUE, lw=1.0,
                solid_capstyle="butt", zorder=2)
        ax.plot([x], [b], marker="o", ms=3.4, color=N.BLUE, mec="white",
                mew=0.5, zorder=3)
        ax.annotate(N.num(b, 2), xy=(x, b), xytext=(x + 0.16, b),
                    fontsize=N.PT_TICK, color=N.BLUE, ha="left", va="center")
    N.zeroline(ax)
    ax.set_xticks([0.0, 1.0])
    ax.set_xticklabels([p[3] for p in pts])
    ax.set_xlim(-0.45, 1.62)
    ax.set_xlabel("Regime")
    ax.set_ylabel("Effect on the youth\nemployment share (p.p.)")

    N.panel(fig, ax1, "a", dx=-15.0)
    N.panel(fig, ax2, "b", dx=-15.0)
    return N.save(fig, os.path.join(FIG, "figure3_threshold"))


if __name__ == "__main__":
    S = load()
    for out in (figure1_framework(), figure2_margins(S),
                figure3_threshold(S)):
        print(" ", os.path.basename(out[0]))
    print("figures written to", FIG)
