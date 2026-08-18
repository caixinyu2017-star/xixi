# -*- coding: utf-8 -*-
"""Table and figure specifications.

Numeric content is read from the experimental output written by
model/run_experiments.py, so the manuscript cannot drift away from the
measured values. Tables and figures are numbered by the order in which
the text first mentions them.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
with open(os.path.join(TAB, "results.json"), encoding="utf-8") as _fh:
    R = json.load(_fh)

MINUS = "−"
BASELINE_ORDER = [
    ("Aggregated logistic regression", "[[trull2013]]"),
    ("Gated recurrent encoder", "[[cho2014]]"),
    ("Self-attentive encoder", "[[vaswani2017]]"),
    ("Temporal graph encoder", "[[zhao2020]]"),
    ("Attentive diagnostic model", "[[koh2020]]"),
]
PROPOSED = "DP-APT (proposed)"


def f3(x):
    return ("%.3f" % x).replace("-", MINUS)


def pm(model, key):
    m = R["models"][model]
    if key not in m:
        return "—"
    return "%s (%s)" % (f3(m[key]), f3(m[key + "_sd"]))


# ---------------------------------------------------------------------------
def table1():
    """Regulation-profile prediction performance."""
    rows = []
    for name, ref in BASELINE_ORDER:
        rows.append([name + " " + ref, pm(name, "auc_roc"),
                     pm(name, "auc_pr")])
    rows.append(["DP-APT (ours)", pm(PROPOSED, "auc_roc"),
                 pm(PROPOSED, "auc_pr")])
    return dict(number=1,
                caption="Regulation Profile Prediction Performance "
                        "(Test Set)",
                header=["Model", "AUC-ROC", "AUC-PR"],
                rows=rows, align=["left", "center", "center"])


def table2():
    """Explanation faithfulness and justification alignment."""
    rows = []
    labels = {
        "Gated recurrent encoder": "Gated recurrent encoder + "
                                   "integrated gradients [[cho2014]], "
                                   "[[sundararajan2017]]",
        "Self-attentive encoder": "Self-attentive encoder + integrated "
                                  "gradients [[vaswani2017]], "
                                  "[[sundararajan2017]]",
        "Attentive diagnostic model": "Attentive diagnostic model "
                                      "(score decomposition) "
                                      "[[koh2020]]",
        "Temporal graph encoder": "Temporal graph encoder (score "
                                  "decomposition) [[zhao2020]]",
    }
    for key, lab in labels.items():
        rows.append([lab, pm(key, "comprehensiveness"),
                     pm(key, "sufficiency"), pm(key, "alignment")])
    # the attention row is read entirely through the attention
    # distribution, so all three of its columns come from that reading
    av = R["ablation"]["with attention over episodes"]
    rows.append(["DP-APT with attention (attention distribution)",
                 "%s (%s)" % (f3(av["comprehensiveness_attention"]),
                              f3(av["comprehensiveness_attention_sd"])),
                 "%s (%s)" % (f3(av["sufficiency_attention"]),
                              f3(av["sufficiency_attention_sd"])),
                 "%s (%s)" % (f3(av["alignment_attention"]),
                              f3(av["alignment_attention_sd"]))])
    rows.append(["DP-APT (ours, score decomposition)",
                 pm(PROPOSED, "comprehensiveness"),
                 pm(PROPOSED, "sufficiency"),
                 pm(PROPOSED, "alignment")])
    rows.append(["Chance level (marginal deployment rate)", "—", "—",
                 f3(R["corpus"]["chance_alignment"])])
    rows.append(["Oracle ceiling (supervised episode probe)", "—", "—",
                 f3(R["corpus"]["oracle_alignment"])])
    return dict(number=2,
                caption="Explanation Faithfulness and Justification "
                        "Alignment (Test Set)",
                header=["Model (explanation method)",
                        "Comprehen-\nsiveness ↑", "Sufficiency\n↓",
                        "Alignment\n↑"],
                rows=rows, widths=[0.37, 0.21, 0.21, 0.21],
                align=["left", "center", "center", "center"])


def table3():
    """Ablation study."""
    order = ["without the ontology parser",
             "without the temporal graph",
             "without the item anchoring term",
             "with attention over episodes",
             "full model"]
    pretty = {
        "without the ontology parser":
            "w/o RPOP (free concept embeddings)",
        "without the temporal graph":
            "w/o TAGN (gated sequence encoder)",
        "without the item anchoring term":
            "w/o anchoring (μ = 0)",
        "with attention over episodes":
            "+ attention over episodes",
        "full model": "Full DP-APT",
    }
    def sd(a, key):
        return "%s (%s)" % (f3(a[key]), f3(a[key + "_sd"]))

    rows = []
    for k in order:
        a = R["ablation"][k]
        rows.append([pretty[k], sd(a, "auc_roc"), sd(a, "sufficiency"),
                     sd(a, "alignment")])
    return dict(number=3,
                caption="Ablation Study Results (Test Set)",
                header=["Model variant", "AUC-ROC\n↑", "Sufficiency\n↓",
                        "Alignment\n↑"],
                rows=rows, widths=[0.37, 0.21, 0.21, 0.21],
                align=["left", "center", "center", "center"])


def table4():
    """Convergent validity against trait questionnaires."""
    rows = []
    names = {"ERQCA_reappraisal": "ERQ-CA reappraisal [[gullone2012]]",
             "ERQCA_suppression": "ERQ-CA suppression [[gullone2012]]",
             "ERC_teacher": "ERC, teacher-reported [[shields1997]]"}
    for label, v in R["validity"].items():
        p = v["p"]
        ptxt = "< .001" if p < 0.001 else ("%.3f" % p).lstrip("0")
        rows.append([label, names[v["criterion"]], f3(v["r"]), ptxt])
    return dict(number=4,
                caption="Convergent Validity of the Inferred "
                        "Regulation Profile (Test Set)",
                header=["Model output", "Criterion measure", "r", "p"],
                rows=rows, widths=[0.34, 0.34, 0.16, 0.16],
                align=["left", "left", "center", "center"])


TABLES = {"table1": table1, "table2": table2, "table3": table3,
          "table4": table4}

FIGURES = {
    "fig1": dict(number=1, file="figure1_pipeline.png", width_cm=8.6,
                 caption="The assessment pipeline in which the proposed "
                         "engine is deployed. Momentary self-reports and "
                         "context channels collected across the school "
                         "day enter the engine, which returns both a "
                         "regulation profile and the episode-level "
                         "evidence trail that a class teacher audits."),
    "fig2": dict(number=2, file="figure2_architecture.png",
                 width_cm=8.6,
                 caption="Internal architecture of the Dual-Pathway "
                         "Affective Process Tracing engine."),
    "fig3": dict(number=3, file="figure3_alignment.png", width_cm=8.6,
                 caption="Evidence trail of the proposed model over the "
                         "momentary reports of one test pupil. "
                         "Open squares mark the family actually "
                         "deployed in each episode."),
    "fig4": dict(number=4, file="figure4_tradeoff.png", width_cm=8.6,
                 caption="Predictive accuracy, explanation "
                         "comprehensiveness and justification alignment "
                         "across the sparsity weight. The dashed line "
                         "marks the alignment attained by a random "
                         "explanation."),
}
