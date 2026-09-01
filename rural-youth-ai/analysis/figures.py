# -*- coding: utf-8 -*-
"""The four figures, in the journal's black-and-white idiom.

No figure carries an explanatory note; whatever a note would say is stated
in the body text.
"""
from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                # noqa: E402
import numpy as np                                             # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

TAB = os.path.join(ROOT, "tables")
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

BLACK, GREY, LIGHT = "#000000", "#7F7F7F", "#E8E8E8"

plt.rcParams.update({
    "font.family": "DejaVu Serif",
    "font.size": 7.0,
    "axes.labelsize": 7.0,
    "axes.titlesize": 7.5,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
    "axes.linewidth": 0.6,
    "figure.dpi": 400,
    "savefig.dpi": 400,
})

LABELS = {
    "fit_agri": "skill fit: agronomy",
    "fit_digital": "skill fit: digital commerce",
    "fit_ops": "skill fit: operations",
    "fit_gov": "skill fit: governance",
    "wage_gap": "wage minus expectation",
    "distance": "distance to home",
    "distance_x_children": "distance × children",
    "mentorship": "mentor pairing",
    "mentorship_x_misfit": "mentor pairing × skill shortfall",
    "housing": "housing support",
    "amenity_x_children": "village amenities × children",
    "home_tie": "home-village tie",
    "gai_x_digital_post": "generative-AI literacy × digital post",
    "education": "schooling level",
    "returnee": "return migrant",
}


def save(fig, name):
    path = os.path.join(FIG, name + ".png")
    fig.savefig(path, bbox_inches="tight", pad_inches=0.02,
                facecolor="white")
    plt.close(fig)
    print("  ", os.path.basename(path))
    return path


def _box(ax, cx, cy, w, h, lines, fs=6.4, bold=True, fill="white", lw=0.8):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0,rounding_size=1.6", facecolor=fill,
        edgecolor=BLACK, linewidth=lw, zorder=3))
    ax.text(cx, cy, "\n".join(lines), ha="center", va="center",
            fontsize=fs, fontweight="bold" if bold else "normal",
            zorder=4, linespacing=1.3)
    return dict(cx=cx, cy=cy, l=cx - w / 2, r=cx + w / 2,
                t=cy + h / 2, b=cy - h / 2)


def _arrow(ax, p0, p1, lw=0.8, dashed=False):
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle="-|>,head_length=2.6,head_width=1.7",
        mutation_scale=1.0, linewidth=lw, color=BLACK,
        linestyle="--" if dashed else "-", shrinkA=1.0, shrinkB=1.0,
        zorder=2))


# ===========================================================================
def figure1_pipeline():
    """The allocation pipeline the engine is deployed in."""
    W, H = 88.0, 52.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_axis_off()

    a = _box(ax, 14.0, 41.0, 26, 13,
             ["Unstructured youth", "materials and post", "descriptions"],
             fs=5.5)
    b = _box(ax, 14.0, 20.0, 26, 12,
             ["LLM profiling layer", "(structured profiles,", "with noise)"],
             fs=5.5)
    c = _box(ax, 44.0, 30.5, 22, 16,
             ["RAMT", "matching", "engine"], fs=6.6, fill=LIGHT)
    d = _box(ax, 71.0, 41.0, 26, 12,
             ["Capacity-feasible", "offers", "(deferred acceptance)"],
             fs=5.5)
    e = _box(ax, 71.0, 20.0, 26, 12,
             ["Per-match evidence", "ledger; low-margin", "cases to review"],
             fs=5.5)

    _arrow(ax, (a["cx"], a["b"]), (b["cx"], b["t"]))
    _arrow(ax, (b["r"], b["cy"]), (c["l"], c["cy"] - 3.5))
    _arrow(ax, (c["r"], c["cy"] + 3.5), (d["l"], d["cy"]))
    _arrow(ax, (c["r"], c["cy"] - 3.5), (e["l"], e["cy"]))
    # the retention feedback loop, routed under everything along the
    # bottom of the canvas so that it crosses no box and no text
    yb = 6.0
    ax.plot([e["cx"], e["cx"], c["cx"]], [e["b"], yb, yb],
            color=BLACK, lw=0.8, ls="--", zorder=1)
    _arrow(ax, (c["cx"], yb), (c["cx"], c["b"]), dashed=True)
    ax.text((c["cx"] + e["cx"]) / 2.0, 2.9,
            "observed acceptance and retention",
            ha="center", va="center", fontsize=5.4, style="italic")
    return save(fig, "figure1_pipeline")


# ===========================================================================
def figure2_architecture():
    """Internal architecture of the engine."""
    W, H = 88.0, 64.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_axis_off()

    x1 = _box(ax, 24.0, 58.0, 44, 8,
              ["Pre-registered pair-feature ledger"], fs=6.0)
    x2 = _box(ax, 24.0, 46.5, 44, 9,
              ["Per-feature piecewise-linear", "splines (additive score)"],
              fs=6.0)
    y1 = _box(ax, 69.0, 58.0, 32, 8,
              ["Logged episodes", "(IPW weights)"], fs=5.8)
    h1 = _box(ax, 24.0, 34.5, 44, 9,
              ["Discrete-time retention", "hazard head"], fs=6.0,
              fill=LIGHT)
    a1 = _box(ax, 69.0, 34.5, 32, 9,
              ["Acceptance head", "(youth-side utility)"], fs=5.8)
    da = _box(ax, 44.0, 21.0, 52, 8,
              ["Capacity-constrained deferred acceptance"], fs=6.2,
              fill=LIGHT)
    o1 = _box(ax, 20.0, 7.5, 34, 9,
              ["Offers and exact", "per-match ledger"], fs=6.0)
    o2 = _box(ax, 63.0, 7.5, 40, 9,
              ["Ensemble margin;", "abstain to human review"], fs=6.0)

    _arrow(ax, (x1["cx"], x1["b"]), (x2["cx"], x2["t"]))
    _arrow(ax, (x2["cx"], x2["b"]), (h1["cx"], h1["t"]))
    _arrow(ax, (y1["cx"], y1["b"]), (a1["cx"], a1["t"]))
    _arrow(ax, (y1["l"], y1["cy"]), (x2["r"], x2["cy"] + 1.0))
    _arrow(ax, (h1["cx"], h1["b"]), (34.0, da["t"]))
    _arrow(ax, (a1["cx"], a1["b"]), (56.0, da["t"]))
    _arrow(ax, (30.0, da["b"]), (o1["cx"], o1["t"]))
    _arrow(ax, (58.0, da["b"]), (o2["cx"], o2["t"]))
    return save(fig, "figure2_architecture")


# ===========================================================================
def figure3_ledger():
    """One match's evidence ledger against its runner-up."""
    import market as M
    import engine as E
    import run_all as RA

    mk = M.Market(seed=1)
    Zall = E.all_pair_features(mk, mk).astype(np.float32)
    ep = RA.episodes_arrays(mk, Zall, RA.LOG_ROUNDS)
    basis = E.Basis(ep["Z"])
    formed = ep["acc"] > 0.5
    hz = E.HazardScorer(basis).fit(
        ep["Z"][formed], ep["months"][formed], ep["cens"][formed],
        ep["iw"][formed], seed=1)
    s_acc = E.LogisticHead(basis).fit(ep["Z"], ep["acc"])
    Zflat = Zall.reshape(-1, E.D).astype(float)
    s_ret = hz.score(Zflat).reshape(mk.n, mk.m)
    pref = s_acc.score(Zflat).reshape(mk.n, mk.m)
    asg = E.deferred_acceptance(pref, s_ret, mk.cap)

    # a youth whose decision is clear but multi-causal: median margin case
    offered = np.flatnonzero(asg >= 0)
    margins = []
    for i in offered:
        row = s_ret[i]
        j = asg[i]
        alt = np.argsort(-row)
        j2 = alt[0] if alt[0] != j else alt[1]
        margins.append((row[j] - row[j2], i, j, int(j2)))
    margins.sort()
    _, i, j, j2 = margins[len(margins) // 2]

    phi = hz.ledger(np.stack([Zall[i, j].astype(float),
                              Zall[i, j2].astype(float)]))
    dphi = phi[0] - phi[1]
    order = np.argsort(np.abs(dphi))[::-1]
    keep = [k for k in order if abs(dphi[k]) > 1e-6][:10]

    fig = plt.figure(figsize=(88 / 25.4, 52 / 25.4))
    ax = fig.add_axes([0.44, 0.13, 0.53, 0.84])
    ypos = np.arange(len(keep))[::-1]
    vals = dphi[keep]
    ax.barh(ypos, vals, height=0.62,
            color=["#3A3A3A" if v > 0 else "white" for v in vals],
            edgecolor=BLACK, linewidth=0.7)
    ax.axvline(0, color=BLACK, lw=0.7)
    ax.set_yticks(ypos)
    ax.set_yticklabels([LABELS[E.FEATURES[k]] for k in keep], fontsize=5.9)
    ax.set_xlabel("Ledger contribution to the score difference\n"
                  "(offered post minus best alternative)", fontsize=6.3,
                  labelpad=2.0)
    ax.tick_params(width=0.5, length=2.2)
    for side in ax.spines.values():
        side.set_linewidth(0.6)
    tot = dphi.sum()
    strue = float(s_ret[i, j] - s_ret[i, j2])
    ax.text(0.02, 0.12,
            "ledger total = %.4f\nscore difference = %.4f" % (tot, strue),
            transform=ax.transAxes, ha="left", va="bottom", fontsize=5.0,
            bbox=dict(facecolor="white", edgecolor=BLACK, linewidth=0.5,
                      pad=1.1))
    return save(fig, "figure3_ledger")


# ===========================================================================
def figure4_tradeoffs():
    """The mixing-weight frontier and the abstention risk-coverage curve."""
    with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as fh:
        S = json.load(fh)
    sw, rc = S["sweep"], S["riskcov"]

    fig, axes = plt.subplots(1, 2, figsize=(88 / 25.4, 40 / 25.4))
    fig.subplots_adjust(left=0.105, right=0.985, bottom=0.30, top=0.90,
                        wspace=0.52)

    ax = axes[0]
    al = [d["alpha"] for d in sw]
    ax.plot(al, [d["accept"] for d in sw], marker="o", ms=2.6, lw=0.9,
            color=BLACK, label="offer acceptance")
    ax.plot(al, [d["ret24"] for d in sw], marker="s", ms=2.6, lw=0.9,
            color=BLACK, ls="--", label="24-month retention")
    ax.plot(al, [d["yield100"] / 100.0 for d in sw], marker="^", ms=2.8,
            lw=0.9, color=GREY, label="stay-yield / 100")
    ax.set_xlabel("Mixing weight α\n(0 = retention, 1 = acceptance)",
                  fontsize=6.4)
    ax.set_ylabel("Rate", fontsize=6.6)
    ax.set_ylim(0.24, 0.66)
    ax.set_title("(a)", fontsize=7.0, loc="left")
    ax.legend(fontsize=5.2, frameon=False, loc="center",
              bbox_to_anchor=(0.56, 0.34), handlelength=1.6)
    ax.tick_params(width=0.5, length=2.2)

    ax = axes[1]
    cov = [d["coverage"] for d in rc]
    ret = [d["ret24"] for d in rc]
    sd = [d["sd"] for d in rc]
    ax.errorbar(cov, ret, yerr=sd, marker="o", ms=2.6, lw=0.9,
                color=BLACK, elinewidth=0.6, capsize=1.6)
    ax.set_xlabel("Coverage\n(share auto-approved)", fontsize=6.4)
    ax.set_ylabel("24-month retention", fontsize=6.6)
    ax.set_title("(b)", fontsize=7.0, loc="left")
    ax.tick_params(width=0.5, length=2.2)
    for a_ in axes:
        for side in a_.spines.values():
            side.set_linewidth(0.6)
    return save(fig, "figure4_tradeoffs")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "static"):
        figure1_pipeline()
        figure2_architecture()
    if which in ("all", "data"):
        figure3_ledger()
        figure4_tradeoffs()
