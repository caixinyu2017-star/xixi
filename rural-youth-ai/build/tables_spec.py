# -*- coding: utf-8 -*-
"""Table and figure specifications for the RAMT manuscript.

Numeric content is read from the experimental output written by
analysis/run_all.py (tables/summary.json), so the manuscript cannot
drift away from the measured values. Tables and figures are numbered
by the order in which the text first mentions them. Cell values stack
the mean over the standard deviation so that wide comparisons fit the
journal's single-column table width.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as _fh:
    S = json.load(_fh)

MINUS = "−"

# engine keys in run_all.py -> row labels the reader saw in Section 5.4
ENGINES = [
    ("AdminRule", "Admin. rule (wage rank)"),
    ("FCFS", "First-come queue"),
    ("MLP-Acc", "Platform matcher [[yi2019]]"),
    ("Logit-Acc+DA", "Interpretable acceptance matcher"),
    ("GBM-Ret", "Boosted retention matcher"),
    ("RAMT", "RAMT (ours)"),
    ("Oracle", "Oracle (upper bound)"),
]


def _stack(pair, fmt="%.3f"):
    """mean over (SD) on two lines inside one cell."""
    m, sd = pair
    return (fmt % m + "\n(" + fmt % sd + ")").replace("-", MINUS)


def _flat(pair, fmt="%.2f"):
    m, sd = pair
    return (fmt % m + " (" + fmt % sd + ")").replace("-", MINUS)


# ---------------------------------------------------------------------------
def table1():
    """Main deployment comparison."""
    rows = []
    for key, label in ENGINES:
        a = S["main"][key]
        rows.append([label,
                     _stack(a["accept"]),
                     _stack(a["ret24"]),
                     _stack(a["yield100"], "%.2f"),
                     _stack(a["block"], "%.4f"),
                     _stack(a["parity"], "%.2f")])
    return dict(number=1,
                caption="Deployment Performance on the Simulated County "
                        "Micro-Market (Mean (SD) over %d Market "
                        "Replications)" % S["meta"]["n_seeds"],
                header=["Engine", "Accept.\nrate", "Retent.\n24 m",
                        "Stay-yield\n/100 offers", "Block.\nrate",
                        "Parity\n(high/low)"],
                rows=rows, size=8,
                widths=[0.21, 0.14, 0.14, 0.16, 0.18, 0.17],
                align=["left"] + ["center"] * 5)


# ---------------------------------------------------------------------------
AUDIT_ROWS = [
    ("RAMT (ledger)", "RAMT evidence ledger (exact)"),
    ("RAMT-MLPscore (Shapley)",
     "RAMT, neural scorer + sampled Shapley [[lundberg2017]]"),
    ("MLP-Acc (Shapley)", "Platform matcher + sampled Shapley"),
    ("GBM-Ret (Shapley)", "Boosted retention matcher + sampled Shapley"),
]


def table2():
    """Decision-level audit outcomes."""
    rows = []
    for key, label in AUDIT_ROWS:
        d = S["audit"][key]
        rows.append([label,
                     _stack(d["residual"], "%.3f"),
                     _stack(d["sufficiency"]),
                     _stack(d["minimality"]),
                     _stack(d["flip"])])
    return dict(number=2,
                caption="Decision-Level Audit Outcomes for Every Engine "
                        "That Ships a Trail (Mean (SD) over %d Market "
                        "Replications)" % S["meta"]["n_seeds_audit"],
                header=["System (trail)", "Recon.\nresidual",
                        "Sufficiency\npass", "Minimality\npass",
                        "Counterf.\nflip pass"],
                rows=rows,
                widths=[0.30, 0.16, 0.18, 0.18, 0.18],
                align=["left"] + ["center"] * 4)


# ---------------------------------------------------------------------------
ABLATIONS = [
    ("RAMT", "RAMT (full)"),
    ("GBM-Ret+DA", "Boosted-tree scorer + deferred acceptance"),
    ("RAMT-alpha1", "Acceptance objective (α = 1)"),
    ("RAMT-MLPscore", "Neural scorer in place of additive splines"),
    ("RAMT-greedy", "Greedy fill in place of deferred acceptance"),
    ("RAMT-noIPW", "No inverse-propensity weighting"),
    ("RAMT-OT", "Sinkhorn transport in place of deferred acceptance"),
]


def table3():
    """One design commitment removed at a time."""
    rows = []
    for key, label in ABLATIONS:
        a = S["main"][key]
        rows.append([label,
                     _stack(a["yield100"], "%.2f"),
                     _stack(a["ret24"]),
                     _stack(a["block"], "%.4f"),
                     _stack(a["parity"], "%.2f")])
    return dict(number=3,
                caption="Ablation Study: Effect of Removing One Design "
                        "Commitment at a Time (Mean (SD) over %d Market "
                        "Replications)" % S["meta"]["n_seeds"],
                header=["Variant", "Stay-yield\n/100 offers",
                        "24 m\nretention", "Blocking\nrate",
                        "Parity\n(high/low)"],
                rows=rows,
                widths=[0.36, 0.17, 0.15, 0.17, 0.15],
                align=["left"] + ["center"] * 4)


# ---------------------------------------------------------------------------
def table4():
    """Ordering under a structurally different generator."""
    rows = []
    for key, label in ENGINES:
        rows.append([label,
                     _flat(S["main"][key]["yield100"]),
                     _flat(S["mismatched"][key]["yield100"])])
    return dict(number=4,
                caption="Stay-Yield per 100 Offers under the "
                        "Regime-Switching Generator and the Held-Out "
                        "Smooth Logistic Generator",
                header=["Engine", "Regime-switching\ngenerator",
                        "Smooth logistic\ngenerator"],
                rows=rows,
                widths=[0.40, 0.30, 0.30],
                align=["left", "center", "center"])


TABLES = dict(table1=table1, table2=table2, table3=table3, table4=table4)

# ---------------------------------------------------------------------------
FIGURES = dict(
    fig1=dict(number=1, file="figure1_pipeline.png", width_cm=8.6,
              caption="The deployed pipeline. The generative-AI "
                      "profiling layer feeds RAMT, whose offers carry "
                      "evidence ledgers and abstentions; observed "
                      "acceptance and retention feed the next round of "
                      "training."),
    fig2=dict(number=2, file="figure2_architecture.png", width_cm=8.6,
              caption="The RAMT architecture: additive spline scoring "
                      "over the pre-registered feature ledger, retention "
                      "and acceptance heads mixed by the dial α, "
                      "capacity-constrained deferred acceptance, and "
                      "ensemble-margin abstention."),
    fig3=dict(number=3, file="figure3_ledger.png", width_cm=8.6,
              caption="The exact evidence ledger for one median-margin "
                      "match (market replication 1): the ten largest "
                      "signed contributions to the score difference "
                      "between the offered post and the best "
                      "alternative. Filled bars favour the offered "
                      "post."),
    fig4=dict(number=4, file="figure4_tradeoffs.png", width_cm=8.6,
              caption="The two policy dials. (a) Acceptance, retention "
                      "and stay-yield against the mixing weight α "
                      "(means over 10 market replications). (b) "
                      "24-month retention among auto-approved matches "
                      "against automated coverage, with one standard "
                      "deviation across replications."),
)
