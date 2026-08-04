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


def _kde(ax, values):
    """A normalised kernel density evaluated over the axis, from the full range
    of the data. Binning to the axis limits, which is the obvious shortcut,
    discards every observation outside the plotted window and makes the profile
    taper at the edges for want of observations that are in fact there."""
    from scipy.stats import gaussian_kde
    grid = np.linspace(*ax.get_xlim(), 400)
    d = gaussian_kde(values)(grid)
    return grid, d / d.max()


def _strip(ax, label="density"):
    """Dress a support strip: no vertical scale, no furniture but the x axis."""
    ax.set_ylim(0, 1.08)
    ax.set_yticks([])
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_ylabel(label, fontsize=N.PT_TICK, color=N.GREY, rotation=0,
                  ha="right", va="center", labelpad=3.0)


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
    """Marginal effect of the demand shock across the variety measures.

    Panel a carries the two x-positions the paper argues from, and both are
    written into the panel: the estimated threshold, with the effect that
    obtains there, and the point at which the effect reaches zero. A reader who
    takes only the figure should still leave with both numbers.
    """
    d = pd.read_csv(os.path.join(DATA, "panel.csv"))
    H = 56.0
    fig = N.figure(N.TEXT, H)
    wide = (N.TEXT - 18.0 - 3.0 - 16.0) / 2.0
    main, strip = [], []
    for i in range(2):
        x = 18.0 + i * (wide + 16.0)
        st = N.axes_mm(fig, x, 13.0, wide, 3.2)
        mn = N.axes_mm(fig, x, 16.7, wide, 32.5)
        mn.sharex(st)
        mn.tick_params(axis="x", labelbottom=False, length=0)
        mn.spines["bottom"].set_visible(False)
        main.append(mn)
        strip.append(st)

    # ---- a: total variety, with the threshold and the zero crossing ------
    ax = main[0]
    rows = S["margin_variety"]
    z = np.array([r["z"] for r in rows])
    m = np.array([r["effect"] for r in rows])
    se = np.array([r["se"] for r in rows])
    ax.set_xlim(z.min(), z.max())
    T = S["thr"]
    ax.axvspan(T["ci_low"], T["ci_high"], color=N.SHADE, lw=0, zorder=0.3)
    N.band(ax, z, m - 1.645 * se, m + 1.645 * se)
    ax.plot(z, m, color=N.BLUE, lw=1.1, zorder=2)
    N.zeroline(ax)
    ax.axvline(T["gamma"], color=N.INK, lw=0.6, ls=(0, (1.0, 1.5)), zorder=1.2)

    g = T["gamma"]
    eg = float(np.interp(g, z, m))
    ax.plot([g], [eg], marker="o", ms=3.0, color=N.BLUE, mec="white", mew=0.5,
            zorder=3)
    ax.annotate("%s p.p." % N.num(eg, 2), xy=(g, eg),
                xytext=(-6, -7), textcoords="offset points", ha="right",
                va="top", fontsize=N.PT_TICK, color=N.INK)
    zc = S["zero_variety"]
    ax.plot([zc], [0.0], marker="o", ms=3.2, mfc="white", mec=N.BLUE, mew=0.7,
            zorder=3)
    ax.annotate("zero at %.2f bits" % zc, xy=(zc, 0.0), xytext=(-6, 5),
                textcoords="offset points", ha="right", va="bottom",
                fontsize=N.PT_TICK, color=N.INK)
    ax.annotate("γ̂ = %.2f   95%% CI %.2f–%.2f"
                % (g, T["ci_low"], T["ci_high"]),
                xy=((T["ci_low"] + T["ci_high"]) / 2, 1.01),
                xycoords=("data", "axes fraction"), ha="center", va="bottom",
                fontsize=N.PT_TICK, color=N.INK)
    ax.set_ylabel("Marginal effect on the youth\n"
                  "employment share (p.p.)")
    strip[0].set_xlabel("Workforce skill variety (bits)")
    gr, dv = _kde(strip[0], d.Variety.to_numpy())
    strip[0].fill_between(gr, 0.0, dv, color=N.FAINT, lw=0)
    _strip(strip[0])

    # ---- b: the two components, per bit, over their observed support ------
    ax = main[1]
    ax.set_xlim(0.0, 3.05)
    series = (("margin_rel", N.BLUE, "Related", "RelVar"),
              ("margin_unrel", N.ORANGE, "Unrelated", "UnrelVar"))
    for key, col, lab, var in series:
        rr = S[key]
        mu, sd = S["mean_" + var], S["sd_" + var]
        x = mu + np.array([r["z"] for r in rr]) * sd
        mm = np.array([r["effect"] for r in rr])
        ss = np.array([r["se"] for r in rr])
        k = x >= 0.0
        N.band(ax, x[k], (mm - 1.645 * ss)[k], (mm + 1.645 * ss)[k], color=col)
        ax.plot(x[k], mm[k], color=col, lw=1.1, zorder=2)
        ax.annotate(lab, xy=(x[k][-1], mm[k][-1]), xytext=(-2, 3),
                    textcoords="offset points", color=col,
                    fontsize=N.PT_TICK, ha="right", va="bottom")
        gr, dv = _kde(strip[1], d[var].to_numpy())
        strip[1].plot(gr, dv, color=col, lw=0.5)
    N.zeroline(ax)
    ax.set_ylabel("Marginal effect on the youth\n"
                  "employment share (p.p.)")
    ax.text(0.97, 0.05, "slope ratio %.2f" % S["ratio_ru"],
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=N.PT_TICK, color=N.INK)
    strip[1].set_xlabel("Variety component (bits)")
    _strip(strip[1])

    for a in main:
        N.snap(a, x=False)
    for a in strip:
        N.snap(a, y=False)
    N.panels(fig, [(main[0], "a"), (main[1], "b")])
    return N.save(fig, os.path.join(FIG, "figure2_margins"))


# ===========================================================================
def figure3_threshold(S):
    """The requisite-variety threshold and the regime coefficients.

    Panel a is drawn on a symmetric-log vertical scale. On a linear axis the
    likelihood ratio spans nought to over four hundred, which presses the
    critical value of 7.35 and both of its crossings onto the axis floor and
    makes the confidence interval impossible to read off the curve that
    defines it. The reference geometry is set in text black with two distinct
    dash patterns, so the distinction between the critical value and the
    threshold survives greyscale; colour is reserved for the estimates.
    """
    import matplotlib.ticker as mticker

    T = S["thr"]
    H = 56.0
    fig = N.figure(N.TEXT, H)
    ax1 = N.axes_mm(fig, 18.0, 17.0, 56.0, 32.0)
    ax2 = N.axes_mm(fig, 93.0, 17.0, 36.0, 32.0)

    # ---- a: the likelihood-ratio profile ---------------------------------
    ax = ax1
    g = np.array(T["grid"])
    lr = np.array(T["lr"])
    ok = np.isfinite(lr)
    ax.axvspan(T["ci_low"], T["ci_high"], color=N.SHADE, lw=0, zorder=0.3)
    ax.plot(g[ok], np.clip(lr[ok], 0.0, None), color=N.BLUE, lw=1.0, zorder=2)
    ax.axhline(T["crit"], color=N.INK, lw=0.6, ls=(0, (3.0, 1.8)), zorder=1.2)
    ax.axvline(T["gamma"], color=N.INK, lw=0.6, ls=(0, (1.0, 1.5)), zorder=1.4)
    ax.set_yscale("symlog", linthresh=1.0, linscale=0.4)
    ax.set_ylim(0.0, 500.0)
    ax.set_yticks([0, 1, 10, 100, 400])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: "%g" % v))
    ax.minorticks_off()
    ax.set_xlim(g.min(), g.max())
    ax.set_xlabel("Candidate threshold in workforce skill variety (bits)")
    ax.set_ylabel("Likelihood ratio")
    ax.annotate("95%% critical value %.2f" % T["crit"],
                xy=(g.min(), T["crit"]), xytext=(2, 2),
                textcoords="offset points", ha="left", va="bottom",
                fontsize=N.PT_TICK, color=N.INK)
    ax.annotate("γ̂ = %.2f   95%% CI %.2f–%.2f"
                % (T["gamma"], T["ci_low"], T["ci_high"]),
                xy=((T["ci_low"] + T["ci_high"]) / 2, 1.01),
                xycoords=("data", "axes fraction"), ha="center", va="bottom",
                fontsize=N.PT_TICK, color=N.INK)

    # ---- b: the regime coefficients --------------------------------------
    ax = ax2
    pts = [(0.0, T["b_low"], T["se_low"], "below γ̂"),
           (1.0, T["b_high"], T["se_high"], "above γ̂")]
    for x, b, se, lab in pts:
        ax.plot([x, x], [b - 1.96 * se, b + 1.96 * se], color=N.BLUE, lw=1.0,
                solid_capstyle="butt", zorder=2)
        ax.plot([x], [b], marker="o", ms=3.4, color=N.BLUE, mec="white",
                mew=0.5, zorder=3)
        ax.annotate(N.num(b, 2), xy=(x, b), xytext=(4, -2),
                    textcoords="offset points", fontsize=N.PT_TICK,
                    color=N.INK, ha="left", va="top")
    N.zeroline(ax)
    ax.set_xticks([0.0, 1.0])
    ax.set_xticklabels([p[3] for p in pts])
    ax.set_xlim(-0.45, 1.62)
    ax.set_xlabel("Regime")
    ax.set_ylabel("Effect on the youth\nemployment share (p.p.)")

    N.snap(ax1, y=False)
    ax1.spines["left"].set_bounds(0.0, 400.0)
    N.snap(ax2, x=False)
    ax2.spines["bottom"].set_bounds(0.0, 1.0)
    N.panels(fig, [(ax1, "a"), (ax2, "b")])
    return N.save(fig, os.path.join(FIG, "figure3_threshold"))


if __name__ == "__main__":
    S = load()
    for out in (figure1_framework(), figure2_margins(S),
                figure3_threshold(S)):
        print(" ", os.path.basename(out[0]))
    print("figures written to", FIG)
