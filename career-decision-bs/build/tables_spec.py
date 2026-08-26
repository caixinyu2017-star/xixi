# -*- coding: utf-8 -*-
"""Table and figure specifications.

Numeric content is read from the model output written by analysis/run_all.py,
so the manuscript cannot drift away from what the code produced. Tables and
figures are numbered by the order in which the text first mentions them.

Figures carry no explanatory notes. Whatever a note would say is stated in the
body text instead, so that the reader meets it in the argument rather than in
small type beneath a picture.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as _fh:
    SUM = json.load(_fh)

MINUS = "−"
_MI = re.compile(r"(?<![\w–—-])-(?=[\d.])")


def read(name):
    rows = [l.rstrip("\n").split("\t")
            for l in open(os.path.join(TAB, name), encoding="utf-8")]
    return rows[0], rows[1:]


def mi(s):
    s = str(s).strip()
    return "—" if s in ("-", "") else _MI.sub(MINUS, s)


def R(*c):
    return ("row", [mi(x) for x in c])


SRC = " Source: authors' simulation."
PAIR = {"CA-CDSE": "Career anxiety with self-efficacy",
        "CA-PCS": "Career anxiety with parental involvement",
        "CA-CDD": "Career anxiety with decision difficulty",
        "CDSE-PCS": "Self-efficacy with parental involvement",
        "CDSE-CDD": "Self-efficacy with decision difficulty",
        "PCS-CDD": "Parental involvement with decision difficulty"}


def table1():
    rows = [
        R("Unresolved uncertainty", "How much about career fit the student "
          "has still to settle", "Evolves weekly"),
        R("Career exploration", "Effort spent gathering career information "
          "in the current week", "Evolves weekly"),
        R("Decision-making self-efficacy", "Belief in one's capacity to "
          "carry out career decision tasks", "Evolves weekly"),
        R("Career anxiety", "A stable dispositional component plus a "
          "component responding to the situation", "Evolves weekly"),
        R("Parental involvement", "Reassurance, scaffolding of the student's "
          "own exploring, and taking the decision over", "Fixed per family"),
        R("Preference divergence", "Distance between the option the student "
          "comes to prefer and the one the family endorses",
          "Fixed per family"),
        R("Decision difficulty", "Unresolved uncertainty combined with "
          "unreconciled conflict", "Outcome"),
    ]
    return dict(number=1, caption="Quantities represented in the model.",
                header=["Quantity", "Meaning", "Status"],
                rows=rows, widths=[0.27, 0.53, 0.20],
                note=("The model is a set of stated equations, not an "
                      "estimate from data. Appendix A lists every parameter "
                      "with its provenance." + SRC),
                italic_col=None, wide=False, align="llc")


def table2():
    hdr, raw = read("t01_calibration.tsv")
    rows = [R(PAIR.get(r[0], r[0]), r[1], r[2], r[3]) for r in raw]
    return dict(number=2,
                caption="Correlations reported for the original sample and "
                        "reproduced by the calibrated model.",
                header=["Association", "Reported", "Simulated", "Difference"],
                rows=rows, widths=[0.46, 0.18, 0.18, 0.18],
                note=("Reported values are those given by Pan and He (2026) "
                      "for 407 female undergraduates and are used here as the "
                      "calibration target. Root mean squared difference "
                      "%.3f. Correlations from a sample of that size carry "
                      "sampling error of roughly a tenth in themselves."
                      % SUM["calibration"]["rmse"] + SRC),
                italic_col=None, wide=False, align="lccc")


def table3():
    hdr, raw = read("t03_conditional.tsv")
    rows = [R(r[0], r[1], ("[%s, %s]" % (r[2], r[3])) if r[2] else "—")
            for r in raw]
    return dict(number=3,
                caption="The conditional process model estimated on a "
                        "simulated cohort at the calibrated parameters.",
                header=["Quantity", "Estimate", "95% bootstrap interval"],
                rows=rows, widths=[0.52, 0.22, 0.26],
                note=("Standardised coefficients. Career anxiety predicts "
                      "difficulty directly and through self-efficacy, with "
                      "parental involvement moderating the direct path. "
                      "Intervals are percentile bootstrap intervals from "
                      "%d resamples." % SUM["meta"]["boots"] + SRC),
                italic_col=None, wide=False, align="lcc")


def table4():
    hdr, raw = read("t04_moderation.tsv")
    rows = [R(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in raw]
    return dict(number=4,
                caption="The conditional process model as the kind of "
                        "parental involvement varies.",
                header=["Directive\nshare", "Direct", "Indirect",
                        "Interaction", "95% interval", "Slope at\nlow support",
                        "Slope at\nhigh support"],
                rows=rows,
                widths=[0.12, 0.11, 0.11, 0.13, 0.21, 0.16, 0.16],
                note=("The directive share is the fraction of parental "
                      "involvement that resolves uncertainty on the "
                      "student's behalf rather than supporting the student's "
                      "own exploring; everything else is held at the "
                      "calibrated values. Simple slopes are of anxiety on "
                      "difficulty at one standard deviation either side of "
                      "the mean of involvement." + SRC),
                italic_col=None, wide=True, align="l" + "c" * 6)


def table5():
    hdr, raw = read("t08_scaffold.tsv")
    rows = [R(*r) for r in raw]
    return dict(number=5,
                caption="Reduction in simulated decision difficulty from "
                        "scaffolding involvement, by dispositional anxiety.",
                header=["Group", "Low involvement", "High involvement",
                        "Benefit"],
                rows=rows, widths=[0.40, 0.20, 0.20, 0.20],
                note=("Involvement wholly scaffolding, that is with a "
                      "directive share of zero. Groups are the extreme "
                      "quartiles of the dispositional anxiety distribution, "
                      "and involvement is compared between its extreme "
                      "quartiles." + SRC),
                italic_col=None, wide=False, align="lccc")


def table6():
    hdr, raw = read("t05_conditions.tsv")
    rows = [R(*r) for r in raw]
    c = SUM["conditions"]
    return dict(number=6,
                caption="Where amplification arises in the parameter space.",
                header=["Condition", "Level", "Mean interaction",
                        "Amplifying (%)"],
                rows=rows, widths=[0.44, 0.14, 0.22, 0.20],
                note=("A factorial search over %d combinations of the five "
                      "parameters governing conflict and involvement. "
                      "Amplification, a positive interaction, arises in %d "
                      "of them. Each row averages over the other four "
                      "parameters." % (c["n_cells"], c["n_amplifying"]) + SRC),
                italic_col=None, wide=False, align="lccc")


def table7():
    hdr, raw = read("t07_precision.tsv")
    rows = [R(r[0], r[1], r[2], "[%s, %s]" % (r[3], r[4]), r[5]) for r in raw]
    return dict(number=7,
                caption="How precisely the interaction is estimated, by "
                        "cohort size.",
                header=["Cohort", "Mean", "SD across studies",
                        "Central 95% range", "Detected (%)"],
                rows=rows, widths=[0.14, 0.16, 0.22, 0.26, 0.22],
                note=("300 simulated studies at each size, drawn at the "
                      "calibrated parameters. Detection is at the "
                      "conventional two-tailed threshold." + SRC),
                italic_col=None, wide=True, align="ccccc")


def tableA1():
    hdr, raw = read("t0A_params.tsv")
    rows = [R(r[0], r[1], r[2], "%s–%s" % (r[3], r[4]), r[5].title())
            for r in raw]
    c = SUM["params"]["counts"]
    return dict(number="A1",
                caption="Every parameter of the model, with its sweep "
                        "interval and its provenance.",
                header=["Parameter", "Value", "Unit", "Swept over",
                        "Provenance"],
                rows=rows, widths=[0.26, 0.11, 0.29, 0.16, 0.18],
                note=("Of %d parameters, %d are bounded by a cited source "
                      "and %d are modelling choices. The table is generated "
                      "from the registry the code reads, so it cannot "
                      "disagree with the values actually used."
                      % (SUM["params"]["n"], c["literature"], c["assumed"])
                      + SRC),
                italic_col=None, wide=True, align="llllc")


TABLES = {"table%d" % i: fn for i, fn in enumerate(
    [table1, table2, table3, table4, table5, table6, table7], start=1)}
TABLES["tableA1"] = tableA1

FIGURES = {
    "fig1": dict(number=1, file="figure1_model.png", width_cm=14.0,
                 caption="The process the model represents. Solid arrows are "
                         "the loop through which career anxiety, career "
                         "exploration, decision-making self-efficacy and "
                         "unresolved uncertainty influence one another. "
                         "Dashed arrows are the three functions through which "
                         "parental involvement enters, together with the "
                         "interference of anxiety with what exploration "
                         "yields, which acts on the mastery path rather than "
                         "adding to it.",
                 note=None),
    "fig2": dict(number=2, file="figure2_trajectories.png", width_cm=14.0,
                 caption="Simulated trajectories of unresolved uncertainty "
                         "and decision-making self-efficacy over the "
                         "decision horizon, for the extreme quartiles of the "
                         "dispositional anxiety distribution.",
                 note=None),
    "fig3": dict(number=3, file="figure3_slopes.png", width_cm=14.0,
                 caption="The anxiety by involvement interaction as the "
                         "directive share of parental involvement varies, "
                         "and the simple slopes of career anxiety on "
                         "decision difficulty at low and high involvement "
                         "under the calibrated parameters.",
                 note=None),
}
