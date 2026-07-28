# -*- coding: utf-8 -*-
"""Publication figures 3-7 for the rationing paper.  600 dpi, serif."""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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
    "lines.linewidth": 1.5, "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 120, "savefig.dpi": 600, "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

NAVY, RUST, TEAL, GOLD, GREY = "#1f3b73", "#b5432c", "#2e7d74", "#c58b1e", "#6b6b6b"


def save(fig, name):
    fig.savefig(os.path.join(FIGS, name))
    plt.close(fig)
    print("  ", name)


# ------------------------------------------------------------------ fig 3
def fig_reform_path():
    d = pd.read_csv(os.path.join(DATA, "reform_path.csv"))
    x = d["year"]
    fig, ax = plt.subplots(2, 2, figsize=(6.9, 5.3))

    # legends sit below their panel: inside the axes they would cover the
    # series, and a flat series covered by a legend is exactly what this
    # figure is about.
    def below(a, handles, labels, ncol=2, y=-0.30, fs=7.2):
        a.legend(handles, labels, frameon=False, ncol=ncol, loc="upper center",
                 bbox_to_anchor=(0.5, y), fontsize=fs, handlelength=1.9,
                 columnspacing=1.4, borderaxespad=0.0)

    a = ax[0, 0]
    a.plot(x, 100 * d["u_rate_y"], color=NAVY, label="Youth (16–24)")
    a.plot(x, 100 * d["u_rate_p"], color=RUST, ls="--", label="Prime (25–59)")
    a.set_ylabel("Unemployment rate (%)")
    a.set_title("(a) The headline indicators", loc="left")
    a.set_ylim(0, 20)
    below(a, *a.get_legend_handles_labels())

    a = ax[0, 1]
    a.plot(x, 100 * d["cohort_entry_Q"], color=GOLD)
    a.set_ylabel("Per cent of an entering cohort")
    a.set_title("(b) Chance of ever holding a rationed job", loc="left")

    a = ax[1, 0]
    a.plot(x, d["queue_years"], color=GOLD, label="Expected years of queueing")
    a.set_ylabel("Years")
    a.set_title("(c) The queue", loc="left")
    a2 = a.twinx()
    a2.plot(x, 100 * d["queue_share"], color=NAVY, ls="--",
            label="Queue share of youth non-employment (right axis)")
    a2.set_ylabel("Per cent")
    a2.spines["top"].set_visible(False)
    h1, l1 = a.get_legend_handles_labels()
    h2, l2 = a2.get_legend_handles_labels()
    below(a, h1 + h2, l1 + l2, ncol=1, y=-0.32)

    a = ax[1, 1]
    a.plot(x, 100 * d["quota_share"], color=GOLD, label="Rationed share of employment")
    a.plot(x, 100 * (d["L"] / d["L"].iloc[0] - 1), color=GREY, ls=":",
           label="Labour-force growth")
    a.set_ylabel("Per cent")
    a.set_title("(d) A fixed establishment in a growing labour force", loc="left")
    below(a, *a.get_legend_handles_labels(), ncol=1, y=-0.32)

    for a in ax.ravel():
        a.set_xlabel("Year of the phased reform")
        a.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
        a.margins(x=0.02)
    fig.tight_layout(w_pad=2.4, h_pad=2.2)
    save(fig, "fig3_reform_path.png")


# ------------------------------------------------------------------ fig 4
def fig_channels():
    d = pd.read_csv(os.path.join(DATA, "channels.csv"))
    lab = {"cohort_entry_Q": "Chance of a\nrationed job",
           "u_rate_y": "Youth\nunemployment rate",
           "queue_years": "Years of\nqueueing",
           "V_entrant": "Value of being\na new entrant",
           "quota_share": "Rationed share\nof employment"}
    d = d[d["outcome"].isin(lab)].copy()
    d["lab"] = d["outcome"].map(lab)
    order = ["cohort_entry_Q", "u_rate_y", "queue_years", "V_entrant",
             "quota_share"]
    d = d.set_index("outcome").loc[order].reset_index()

    fig, ax = plt.subplots(figsize=(6.4, 3.1))
    y = np.arange(len(d))[::-1]
    h = 0.24
    for j, (col, c, nm) in enumerate([("quota", GOLD, "Quota route"),
                                      ("value", TEAL, "Horizon route"),
                                      ("demo", NAVY, "Demographic route")]):
        ax.barh(y + (1 - j) * h, 100 * d[col], height=h, color=c, label=nm,
                edgecolor="white", lw=0.4)
    ax.plot(100 * d["total"], y, "D", color="black", ms=4.5, ls="none",
            label="Total")
    ax.set_yticks(y)
    ax.set_yticklabels(d["lab"], fontsize=7.6)
    ax.axvline(0, color="black", lw=0.7)
    ax.set_xlabel("Contribution to the change over the full reform "
                  "(log points × 100)")
    ax.legend(frameon=False, ncol=4, loc="lower center",
              bbox_to_anchor=(0.5, -0.42), fontsize=7.2)
    ax.margins(x=0.10)
    fig.tight_layout()
    save(fig, "fig4_channels.png")


# ------------------------------------------------------------------ fig 5
def fig_indicator():
    d = pd.read_csv(os.path.join(DATA, "indicator.csv"))
    fig, ax = plt.subplots(1, 2, figsize=(6.6, 2.9))

    a = ax[0]
    a.plot(d["year"], d["i_u_rate_y"], color=NAVY,
           label="Youth unemployment rate")
    a.plot(d["year"], d["i_cohort_entry_Q"], color=GOLD,
           label="Chance of a rationed job")
    a.plot(d["year"], d["i_queue_years"], color=TEAL, ls="--",
           label="Years of queueing")
    a.axhline(100, color=GREY, lw=0.6, ls=":")
    a.set_xlabel("Year of the phased reform")
    a.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
    a.set_ylabel("Index, 2025 = 100")
    a.set_title("(a) What the indicator misses", loc="left")
    a.legend(frameon=False, loc="lower left", fontsize=7.0)

    a = ax[1]
    vals = [S["indicator"]["u_rate_y_range_pp"],
            abs(S["reform"]["entry_prob_pp"])]
    a.bar([0, 1], vals, color=[NAVY, GOLD], width=0.55, edgecolor="white")
    for i, v in enumerate(vals):
        a.text(i, v + 0.03, "%.2f pp" % v, ha="center", va="bottom",
               fontsize=8.6)
    a.set_xticks([0, 1])
    a.set_xticklabels(["Youth unemployment\nrate", "Chance of a\nrationed job"])
    a.set_ylabel("Change over the reform (percentage points)")
    a.set_title("(b) Movement, side by side", loc="left")
    a.margins(y=0.22)
    fig.tight_layout(w_pad=2.0)
    save(fig, "fig5_indicator.png")


# ------------------------------------------------------------------ fig 6
def fig_policy():
    b = pd.read_csv(os.path.join(DATA, "policy_baseline.csv")).set_index("key")
    a2 = pd.read_csv(os.path.join(DATA, "policy_post_reform.csv")).set_index("key")
    order = ["s_N", "s_v", "tau_q"]
    lab = {"s_N": "Expand the\nestablishment",
           "s_v": "Market vacancy\nsubsidy",
           "tau_q": "Cut the administered\npremium"}
    fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.9))
    y = np.arange(len(order))
    h = 0.36
    panels = [("d_welfare_pc_pct", "Welfare per head (%)", "(a) Welfare"),
              ("d_entry_prob_pct", "Chance of a rationed job (%)",
               "(b) Access"),
              ("mvpf", "Marginal value of public funds", "(c) MVPF")]
    for j, (col, xl, title) in enumerate(panels):
        a = ax[j]
        vb = [b.loc[k, col] if k in b.index else np.nan for k in order]
        va = [a2.loc[k, col] if k in a2.index else np.nan for k in order]
        a.barh(y + h / 2, vb, height=h, color=NAVY, label="Before the reform")
        a.barh(y - h / 2, va, height=h, color=RUST, label="After the reform")
        a.set_yticks(y)
        a.set_yticklabels([lab[k] for k in order] if j == 0 else [],
                          fontsize=7.2)
        a.axvline(1 if col == "mvpf" else 0,
                  color=GREY if col == "mvpf" else "black",
                  lw=0.8, ls=":" if col == "mvpf" else "-")
        a.set_xlabel(xl)
        a.set_title(title, loc="left")
        if j == 0:
            a.legend(frameon=False, loc="lower right", fontsize=6.8)
    fig.tight_layout(w_pad=1.1)
    save(fig, "fig6_policy.png")


# ------------------------------------------------------------------ fig 7
def fig_robustness():
    un = pd.read_csv(os.path.join(DATA, "uncertainty.csv"))
    sq = pd.read_csv(os.path.join(DATA, "sensitivity_quota.csv"))
    fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.6))

    a = ax[0]
    a.hist(100 * un["d_entry_prob"], bins=26, color=GOLD, alpha=0.9,
           edgecolor="white", lw=0.4)
    a.axvline(100 * S["reform"]["d_entry_prob"], color=RUST, lw=1.3)
    a.set_xlabel("Change in the chance of a rationed job (%)")
    a.set_ylabel("Draws")
    a.set_title("(a) Access always falls", loc="left", fontsize=8.6)

    a = ax[1]
    a.hist(un["d_u_rate_y_pp"], bins=26, color=NAVY, alpha=0.9,
           edgecolor="white", lw=0.4)
    a.axvline(S["reform"]["u_rate_y_pp"], color=RUST, lw=1.3)
    a.axvline(0, color=GREY, lw=0.7, ls=":")
    a.set_xlabel("Change in the youth unemployment rate (pp)")
    a.set_title("(b) The indicator never does", loc="left", fontsize=8.6)

    a = ax[2]
    a.plot(100 * sq["quota_share"], sq["queue_loss_pct_Y"], "o-", color=TEAL,
           ms=4)
    a.axvline(100 * S["baseline"]["quota_share"], color=RUST, lw=0.9, ls=":")
    a.set_xlabel("Rationed share of employment (%)")
    a.set_ylabel("Output forgone by the queue (% of GDP)")
    a.set_title("(c) The cost of the queue", loc="left", fontsize=8.6)

    fig.tight_layout(w_pad=1.5)
    save(fig, "fig7_robustness.png")


if __name__ == "__main__":
    print("figures:")
    fig_reform_path()
    fig_channels()
    fig_indicator()
    fig_policy()
    fig_robustness()
