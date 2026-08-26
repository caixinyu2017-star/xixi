# -*- coding: utf-8 -*-
"""Table and figure specifications.

Numeric content is read from the TSV files analysis/run.py writes, so the
manuscript cannot drift from what the code produced. Tables and figures are
numbered by the order in which the text first mentions them.

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
SRC = " Source: authors' calculations from the two panels."


def read(name):
    rows = [l.rstrip("\n").split("\t")
            for l in open(os.path.join(TAB, name), encoding="utf-8")]
    return rows[0], rows[1:]


def mi(s):
    s = str(s).strip()
    return "—" if s in ("-", "") else _MI.sub(MINUS, s)


def R(*c):
    return ("row", [mi(x) for x in c])


NW, NM = SUM["panels"]["NLSW"], SUM["panels"]["NLSY79M"]
DIS, WAV = SUM["disagreement"], SUM["waves"]


def table1():
    hdr, raw = read("t1_panels.tsv")
    return dict(number=1,
                caption="The two panels.",
                header=["Panel", "Variable", "Mean",
                        "SD between people", "SD within people"],
                rows=[R(*r) for r in raw],
                widths=[0.20, 0.32, 0.16, 0.16, 0.16],
                note=("Log hourly wage is the outcome throughout. The "
                      "between-person standard deviation is taken over "
                      "person means; the within-person standard deviation "
                      "is the average of each person's own standard "
                      "deviation. Weekly hours are recorded per week in the "
                      "women's panel and per hundred annual hours in the "
                      "men's. Union coverage and weeks unemployed were not "
                      "asked in every wave of the women's panel, so those "
                      "specifications use fewer observations." + SRC),
                italic_col=None, wide=False, align="llccc")


def table2():
    hdr, raw = read("t2_hypotheses.tsv")
    return dict(number=2,
                caption="The sixteen moderation hypotheses, fixed before "
                        "estimation.",
                header=["#", "Panel", "Career input", "Moderator", "Claim"],
                rows=[R(*r) for r in raw],
                widths=[0.06, 0.16, 0.16, 0.17, 0.45],
                note=("Each claim is stated in the direction the literature "
                      "usually asserts. All sixteen are reported in Table 3 "
                      "whatever they show." + SRC),
                italic_col=None, wide=True, align="lllll")


def table3():
    hdr, raw = read("t3_estimates.tsv")
    return dict(number=3,
                caption="Each interaction estimated four ways.",
                header=["#", "Single wave, median", "Single wave, range",
                        "Pooled", "Between-person", "Within-person",
                        "Difference", "p", "q"],
                rows=[R(*r) for r in raw],
                widths=[0.06, 0.13, 0.16, 0.11, 0.12, 0.12, 0.11, 0.09,
                        0.10],
                note=("Coefficients on the product of the career input and "
                      "the moderator, from the specifications described in "
                      "Section 3.3. Standard errors cluster on the person. "
                      "The difference is the between-person estimate minus "
                      "the within-person estimate; p tests that it is zero "
                      "and q is that probability after controlling the "
                      "false discovery rate across the sixteen tests. "
                      "* p < .05, ** p < .01, *** p < .001." + SRC),
                italic_col=None, wide=True, align="lcccccccc")


def table4():
    hdr, raw = read("t4_disagreement.tsv")
    return dict(number=4,
                caption="The verdict each estimate supports, and where the "
                        "verdicts differ.",
                header=["#", "Panel", "Interaction", "Pooled", "Between",
                        "Within", "Sign reversed", "Verdict changed",
                        "Equality rejected"],
                rows=[R(*r) for r in raw],
                widths=[0.05, 0.13, 0.24, 0.11, 0.11, 0.11, 0.08, 0.09,
                        0.08],
                note=("A verdict is the reading a coefficient supports at "
                      "the conventional threshold. Sign reversal and verdict "
                      "change compare the between-person estimate with the "
                      "within-person estimate; equality is rejected when the "
                      "false discovery rate adjusted probability is below "
                      ".05." + SRC),
                italic_col=None, wide=True, align="lllcccccc")


def table5():
    hdr, raw = read("t5_wave_variability.tsv")
    return dict(number=5,
                caption="Every survey wave treated as a separate study.",
                header=["#", "Waves", "Mean", "SD", "Significant",
                        "Positive", "Negative", "Within-person",
                        "Opposite sign"],
                rows=[R(*r) for r in raw],
                widths=[0.07, 0.09, 0.11, 0.10, 0.13, 0.10, 0.10, 0.15,
                        0.15],
                note=("Mean and SD are taken over the single-wave estimates "
                      "of the interaction. Significant counts the waves "
                      "reaching p < .05, split by sign in the two columns "
                      "that follow. The last column counts the waves whose "
                      "estimate carries the opposite sign to the "
                      "within-person estimate of the same quantity." + SRC),
                italic_col=None, wide=True, align="lcccccccc")


def table6():
    hdr, raw = read("t7_robustness.tsv")
    return dict(number=6,
                caption="The within-person estimate under three variations.",
                header=["#", "Baseline", "Three or more waves",
                        "First differences", "Minimal controls"],
                rows=[R(*r) for r in raw],
                widths=[0.12, 0.22, 0.22, 0.22, 0.22],
                note=("Minimal controls retains the career input, the "
                      "moderator, their product and calendar time only. "
                      "First differencing uses consecutive pairs of "
                      "observations, which in the women's panel are up to "
                      "two years apart. * p < .05, ** p < .01, "
                      "*** p < .001." + SRC),
                italic_col=None, wide=False, align="lcccc")


def tableA1():
    hdr, raw = read("t6_main_effects.tsv")
    return dict(number="A1",
                caption="The slope of the focal career input, and the "
                        "estimation sample.",
                header=["#", "Career input", "Pooled", "Within-person",
                        "Pooled R²", "Within R²", "Person-years", "People"],
                rows=[R(*r) for r in raw],
                widths=[0.07, 0.20, 0.13, 0.14, 0.11, 0.11, 0.13, 0.11],
                note=("The pooled coefficient of determination is computed "
                      "on the outcome, the within-person one on the outcome "
                      "after the person mean is removed, so the two are not "
                      "comparable with one another. * p < .05, ** p < .01, "
                      "*** p < .001." + SRC),
                italic_col=None, wide=True, align="llcccccc")


TABLES = {"table1": table1, "table2": table2, "table3": table3,
          "table4": table4, "table5": table5, "table6": table6,
          "tableA1": tableA1}

FIGURES = {
    "fig1": dict(number=1, file="figure2_between_within.png", width_cm=15.2,
                 caption="The between-person and within-person estimate of "
                         "every interaction, expressed as the difference "
                         "each implies in the response of the log hourly "
                         "wage to a one within-person standard deviation "
                         "change in the career input.",
                 note=None),
    "fig2": dict(number=2, file="figure1_waves.png", width_cm=15.2,
                 caption="Single-wave estimates of four interactions, with "
                         "95% intervals, against the between-person and "
                         "within-person estimates of the same quantities.",
                 note=None),
    "fig3": dict(number=3, file="figure3_profile.png", width_cm=15.2,
                 caption="The wage profile over employer tenure that the "
                         "between-person and within-person estimates imply "
                         "for college graduates and non-graduates.",
                 note=None),
}
