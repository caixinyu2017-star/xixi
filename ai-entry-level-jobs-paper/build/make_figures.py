# -*- coding: utf-8 -*-
"""Publication figures 3-7 for the job-ladder paper.  600 dpi, serif."""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
FIGS = os.path.abspath(os.path.join(HERE, "..", "figs"))
os.makedirs(FIGS, exist_ok=True)

S = json.load(open(os.path.join(HERE, "stats.json")))

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "DejaVu Serif", "Times New Roman"],
    "font.size": 9, "axes.labelsize": 8.6, "axes.titlesize": 9.2,
    "legend.fontsize": 7.6, "xtick.labelsize": 7.8, "ytick.labelsize": 7.8,
    "axes.linewidth": 0.7, "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "lines.linewidth": 1.4, "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 120, "savefig.dpi": 600, "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

NAVY, RUST, TEAL, GOLD, GREY = "#1f3b73", "#b5432c", "#2e7d74", "#c58b1e", "#6b6b6b"
CYC = [TEAL, NAVY, RUST, GOLD]


def save(fig, name):
    fig.savefig(os.path.join(FIGS, name))
    plt.close(fig)
    print("  ", name)


def idx(s):
    return 100.0 * s / s.iloc[0]


# ------------------------------------------------------------------ fig 3
def fig_ai_path():
    d = pd.read_csv(os.path.join(DATA, "ai_path.csv"))
    x = 100 * d["ai_share"]
    fig, ax = plt.subplots(2, 2, figsize=(6.9, 4.9))

    a = ax[0, 0]
    a.plot(x, idx(d["emp_rate_j"]), color=NAVY, label="Entry-level employment rate")
    a.plot(x, idx(d["w_j"]), color=RUST, ls="--", label="Entry wage")
    a.axhline(100, color=GREY, lw=0.6, ls=":")
    a.set_ylabel("Index, baseline = 100")
    a.set_title("(a) Where the shock lands", loc="left")
    a.legend(frameon=False, loc="lower left")

    a = ax[0, 1]
    a.plot(x, idx(d["m"]), color=TEAL, label="Mentoring per entrant")
    a.plot(x, idx(d["promo_years"]), color=GOLD, ls="--",
           label="Years to promotion")
    a.axhline(100, color=GREY, lw=0.6, ls=":")
    a.set_ylabel("Index, baseline = 100")
    a.set_title("(b) The training response", loc="left")
    a.legend(frameon=False, loc="center left")

    a = ax[1, 0]
    a.plot(x, idx(d["throughput"]), color=TEAL, label="Promotion flow")
    a.plot(x, idx(d["e_s"]), color=NAVY, ls="--", label="Experienced workers")
    a.axhline(100, color=GREY, lw=0.6, ls=":")
    a.set_ylabel("Index, baseline = 100")
    a.set_ylim(95, 106)
    a.set_title("(c) The ladder's output", loc="left")
    a.legend(frameon=False, loc="lower right")

    a = ax[1, 1]
    a.plot(x, 1.0 + d["wedge_mentoring"], color=TEAL,
           label="Efficient / market mentoring")
    a.set_ylabel("Ratio")
    a.set_title("(d) The training wedge", loc="left")
    a2 = a.twinx()
    a2.plot(x, d["welfare_gap_pct"], color=RUST, ls="--", label="Welfare gap")
    a2.set_ylabel("Welfare gap (%)")
    a2.spines["top"].set_visible(False)
    h1, l1 = a.get_legend_handles_labels()
    h2, l2 = a2.get_legend_handles_labels()
    a.legend(h1 + h2, l1 + l2, frameon=False, loc="upper right")

    for a in ax.ravel():
        a.set_xlabel("AI share of the entry-level task bundle (%)")
        a.margins(x=0.02)
    fig.tight_layout(w_pad=2.0, h_pad=1.3)
    save(fig, "fig3_ai_path.png")


# ------------------------------------------------------------------ fig 4
def fig_channels():
    d = pd.read_csv(os.path.join(DATA, "channels.csv"))
    d = d[d["channel"] != "total"].copy()
    lab = {"direct task substitution": "Direct task\nsubstitution",
           "training": "Training\nmargin",
           "promotion value": "Promotion-value\nrevaluation",
           "senior scarcity": "Senior-scarcity\nfeedback"}
    d["lab"] = d["channel"].map(lab).fillna(d["channel"])
    total = float(S["channels"]["total"])

    fig, ax = plt.subplots(figsize=(4.5, 3.0))
    y = np.arange(len(d))[::-1]
    vals = 100 * d["contribution"].to_numpy()
    ax.barh(y, vals, color=[NAVY if v < 0 else RUST for v in vals],
            height=0.6, edgecolor="white", lw=0.5)
    for yy, v, sh in zip(y, vals, d["share"]):
        ax.text(v + (-0.12 if v < 0 else 0.12), yy, "%.2f (%.0f%%)" % (v, 100 * sh),
                va="center", ha="right" if v < 0 else "left", fontsize=7.4)
    ax.set_yticks(y)
    ax.set_yticklabels(d["lab"])
    ax.axvline(0, color="black", lw=0.7)
    ax.set_xlabel("Contribution to the change in the entry-level employment rate\n"
                  "(log points × 100)")
    ax.set_title("Total: %.2f log points × 100" % (100 * total), loc="left",
                 fontsize=8.2, color=GREY)
    ax.margins(x=0.30)
    fig.tight_layout()
    save(fig, "fig4_channels.png")


# ------------------------------------------------------------------ fig 5
def fig_exposure():
    d = pd.read_csv(os.path.join(DATA, "exposure.csv"))
    fig, ax = plt.subplots(1, 2, figsize=(6.6, 2.9))

    a = ax[0]
    a.plot(100 * d["ai_share"], 100 * d["d_ln_emp_j"], "o-", color=NAVY, ms=4,
           label="Entry-level employment rate")
    a.plot(100 * d["ai_share"], 100 * d["d_ln_e_s"], "s--", color=RUST, ms=4,
           label="Experienced employment")
    a.plot(100 * d["ai_share"], 100 * d["d_ln_w_j"], "^:", color=GOLD, ms=4,
           label="Entry wage")
    a.axhline(0, color=GREY, lw=0.6, ls=":")
    a.set_xlabel("AI share of the entry-level task bundle (%)")
    a.set_ylabel("Change since the pre-AI benchmark\n(log points × 100)")
    a.set_title("(a) Predicted exposure gradient", loc="left")
    a.legend(frameon=False, loc="lower left")

    a = ax[1]
    model = S["exposure"]["did_pct"]
    data = S["exposure"]["target_pct"]
    a.bar([0, 1], [data, model], color=[GREY, NAVY], width=0.55,
          edgecolor="white")
    for i, v in enumerate([data, model]):
        a.text(i, v - 0.6, "%.1f%%" % v, ha="center", va="top", fontsize=8.6)
    a.set_xticks([0, 1])
    a.set_xticklabels(["Held-out estimate\n(ADP payroll data)",
                       "Model\nprediction"])
    a.axhline(0, color="black", lw=0.7)
    a.set_ylabel("Entry-level relative to experienced (%)")
    a.set_title("(b) Held-out validation", loc="left")
    a.margins(y=0.24)
    fig.tight_layout(w_pad=2.0)
    save(fig, "fig5_exposure.png")


# ------------------------------------------------------------------ fig 6
def fig_policy():
    b = pd.read_csv(os.path.join(DATA, "policy_baseline.csv"))
    a2 = pd.read_csv(os.path.join(DATA, "policy_post_ai.csv"))
    b, a2 = b.set_index("key"), a2.set_index("key")
    order = [k for k in ("t_a", "s_w", "s_v", "s_m")]
    lab = {"s_m": "Mentoring\ncredit", "s_v": "Entry-level\nvacancy subsidy",
           "s_w": "Entry-level\nwage subsidy", "t_a": "Tax on\nAI input"}

    fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.9))
    y = np.arange(len(order))
    h = 0.36
    panels = [("d_welfare_pct", "Welfare gain (%)", "(a) Welfare"),
              ("d_U_j_pct", "Value to a new entrant (%)", "(b) Entrants"),
              ("mvpf", "Marginal value of public funds", "(c) MVPF")]
    for j, (col, xl, title) in enumerate(panels):
        a = ax[j]
        vb = [b.loc[k, col] if k in b.index else np.nan for k in order]
        va = [a2.loc[k, col] if k in a2.index else np.nan for k in order]
        a.barh(y + h / 2, vb, height=h, color=NAVY, label="Baseline")
        a.barh(y - h / 2, va, height=h, color=RUST, label="After the AI shock")
        for i, v in enumerate(vb):
            if not np.isfinite(v):
                a.text(0.0, y[i] + h / 2, "  infeasible", va="center", ha="left",
                       fontsize=6.8, color=GREY, style="italic")
        a.set_yticks(y)
        a.set_yticklabels([lab[k] for k in order] if j == 0 else [],
                          fontsize=7.4)
        a.axvline(1 if col == "mvpf" else 0,
                  color=GREY if col == "mvpf" else "black",
                  lw=0.8, ls=":" if col == "mvpf" else "-")
        if col == "mvpf":
            a.set_xscale("symlog", linthresh=1.0)
        a.set_xlabel(xl)
        a.set_title(title, loc="left")
        if j == 0:
            a.legend(frameon=False, loc="lower right", fontsize=6.8)
    fig.tight_layout(w_pad=1.1)
    save(fig, "fig6_policy.png")


# ------------------------------------------------------------------ fig 7
def fig_uncertainty():
    rg = pd.read_csv(os.path.join(DATA, "rigidity.csv"))
    un = pd.read_csv(os.path.join(DATA, "uncertainty.csv"))
    fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.6))

    a = ax[0]
    a.plot(rg["gamma_w"], -100 * rg["d_ln_emp_rate_j"], "o-", color=NAVY, ms=4,
           label="Entry-level employment rate")
    a.plot(rg["gamma_w"], -100 * rg["d_ln_w_j"], "s--", color=RUST, ms=4,
           label="Entry wage")
    a.axvline(S["meta"]["gamma_w"], color=GREY, lw=0.8, ls=":")
    a.set_xlabel("Real rigidity of the entry wage $\\gamma_w$")
    a.set_ylabel("Fall after the shock (%)")
    a.set_title("(a) Incidence", loc="left", fontsize=8.6)
    a.legend(frameon=False, loc="upper center", fontsize=6.8)

    a = ax[1]
    a.hist(1 + un["wedge_mentoring"], bins=26, color=TEAL, alpha=0.85,
           edgecolor="white", lw=0.4)
    a.axvline(1 + S["wedge"]["mentoring"], color=RUST, lw=1.3)
    a.set_xlabel("Efficient / market mentoring")
    a.set_ylabel("Draws")
    a.set_title("(b) Training wedge", loc="left", fontsize=8.6)

    a = ax[2]
    cols = [c for c in ("gain_s_m", "gain_s_v", "gain_s_w", "gain_t_a")
            if c in un.columns]
    names = {"gain_s_m": "Mentoring\ncredit", "gain_s_v": "Vacancy\nsubsidy",
             "gain_s_w": "Wage\nsubsidy", "gain_t_a": "AI tax"}
    data = [un[c].dropna().to_numpy() for c in cols]
    keep = [i for i, dd in enumerate(data) if len(dd) > 2]
    bp = a.boxplot([data[i] for i in keep], patch_artist=True, widths=0.55,
                   showfliers=False, medianprops=dict(color="black", lw=1.0))
    for patch, c in zip(bp["boxes"], CYC):
        patch.set_facecolor(c)
        patch.set_alpha(0.8)
        patch.set_edgecolor("white")
    a.set_xticklabels([names[cols[i]] for i in keep], fontsize=6.8)
    a.axhline(0, color=GREY, lw=0.7, ls=":")
    a.set_ylabel("Welfare gain at equal budget (%)")
    a.set_title("(c) Instrument ranking", loc="left", fontsize=8.6)

    fig.tight_layout(w_pad=1.4)
    save(fig, "fig7_uncertainty.png")


if __name__ == "__main__":
    print("figures:")
    fig_ai_path()
    fig_channels()
    fig_exposure()
    fig_policy()
    fig_uncertainty()
