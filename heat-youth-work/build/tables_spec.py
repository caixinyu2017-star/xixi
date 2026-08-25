# -*- coding: utf-8 -*-
"""Table specifications.

Numeric content is read from the model output written by analysis/run_all.py,
so the manuscript cannot drift away from what the code produced. Tables are
numbered by the order in which the text first mentions them. This study
reports no figures; the sample article for this Special Issue carries none,
and every quantity here is a comparison of magnitudes that a table states more
precisely than a chart would.
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
_ZERO = re.compile(r"(?<![\w.])-(0\.0+)(?![0-9])")

RULE_LABEL = {
    "uniform": "Uniform over plantable land",
    "population": "Residential population",
    "deprivation": "Residential deprivation",
    "population_heat": "Residential population × local heat",
    "exposure": "Exposed workplaces × local heat",
    "youth": "Young exposed workers × local heat",
    "greedy": "Marginal-benefit optimum",
}
ERF_LABEL = {"hothaps": "Hothaps", "iso": "ISO 7243", "niosh": "NIOSH",
             "dunne": "Dunne et al.", "foster": "Foster et al."}
CLIM_LABEL = {"maritime": "Cool maritime", "continental": "Temperate continental",
              "pannonian": "Warm continental", "mediterranean": "Hot Mediterranean"}
PROV_LABEL = {"literature": "Literature", "derived": "Derived", "assumed": "Assumed"}

SRC = " Source: authors' calculations."


def read(name):
    rows = [l.rstrip("\n").split("\t")
            for l in open(os.path.join(TAB, name), encoding="utf-8")]
    return rows[0], rows[1:]


def mi(s):
    s = str(s).strip()
    if s == "-":
        return "—"
    return _MI.sub(MINUS, _ZERO.sub(r"\1", s))


def R(*c):
    return ("row", [mi(x) for x in c])


# ---------------------------------------------------------------------------
def table1():
    """What the model contains."""
    rows = [
        R("Urban form", "Land use, building density, sky view factor and "
          "ventilation on a 40 × 40 grid of 250 m cells",
          "Synthetic, declared"),
        R("Existing cover", "Tree canopy fraction and distance to the "
          "watercourse, by cell", "Synthetic, declared"),
        R("Climate setting", "Summer air temperature, relative humidity and "
          "irradiance over the working day",
          "Declared modelling input, four settings"),
        R("WBGT", "Simplified wet bulb globe temperature plus an outdoor "
          "radiant increment, by cell and hour", "Computed"),
        R("Work capacity", "Share of the working hour a worker can work at a "
          "given metabolic rate", "Five published response functions"),
        R("Employment", "Jobs by workload class and by age group, by cell",
          "Synthetic, declared"),
        R("Lost hours", "Hours of work capacity lost to heat per working day, "
          "by age group", "Computed"),
        R("Siting rule", "Allocation of a fixed canopy budget across cells",
          "Seven rules, computed"),
    ]
    return dict(number=1,
                caption="Components of the assessment model.",
                header=["Component", "Description", "Status"],
                rows=rows, widths=[0.20, 0.52, 0.28],
                note=("The study is model-based. No component is an "
                      "observation of a named city, and the entries marked "
                      "“synthetic, declared” are transparent "
                      "constructions whose parameters are listed in "
                      "Appendix A." + SRC),
                italic_col=None, wide=False, align="llc")


def table2():
    """The reference city."""
    hdr, raw = read("t01_city.tsv")
    return dict(number=2,
                caption="Properties of the reference city.",
                header=["Quantity", "Value", "Unit"],
                rows=[R(*r) for r in raw],
                widths=[0.46, 0.22, 0.32],
                note=("The workplace–residence correlation is the "
                      "Pearson correlation across cells between the number "
                      "of young workers in heat-exposed classes and the "
                      "number of residents. It is the structural quantity "
                      "the study varies." + SRC),
                italic_col=None, wide=False, align="lcl")


def table3():
    """Baseline exposure."""
    hdr, raw = read("t02_baseline.tsv")
    rows = []
    for r in raw:
        rows.append(R(CLIM_LABEL[r[0]], ERF_LABEL[r[1]], r[2], r[3], r[4],
                      r[5], r[6]))
    return dict(number=3,
                caption="Baseline heat exposure and work capacity lost, by "
                        "climate setting and response function.",
                header=["Climate setting", "Response function",
                        "Mean WBGT", "Peak WBGT", "Young", "Older", "Gap"],
                rows=rows, widths=[0.19, 0.16, 0.12, 0.12, 0.14, 0.14, 0.13],
                note=("WBGT in degrees Celsius, averaged and maximised over "
                      "cells and working hours. The three right-hand columns "
                      "report hours of work capacity lost per worker per "
                      "working day, before any planting." + SRC),
                italic_col=None, wide=True, align="ll" + "c" * 5)


def table4():
    """The main result."""
    hdr, raw = read("t03_siting.tsv")
    rows = [R(RULE_LABEL[r[0]], r[1], r[2], r[3], r[4], r[5]) for r in raw]
    ref = SUM["reference"]
    return dict(number=4,
                caption="Hours of young workers' work capacity protected by "
                        "a fixed planting budget, by siting rule.",
                header=["Siting rule", "Young hours", "Older hours",
                        "Young hours per ha", "Ratio", "Young share"],
                rows=rows, widths=[0.30, 0.15, 0.15, 0.16, 0.11, 0.13],
                note=("A budget of %.0f hectares of new canopy, about EUR "
                      "%.1f million at the planting costs in Appendix A, "
                      "allocated across a city with a workplace–"
                      "residence correlation of %.2f, under the %s climate "
                      "setting and the %s response function. Hours are per "
                      "working day. “Ratio” is relative to the "
                      "residential-population rule. “Young share” "
                      "is the percentage of all protected hours accruing to "
                      "workers under thirty." %
                      (ref["budget_ha"], ref["budget_eur"] / 1e6,
                       SUM["city"]["workplace_residence_r"],
                       CLIM_LABEL[ref["climate"]].lower(),
                       ERF_LABEL[ref["erf"]]) + SRC),
                italic_col=None, wide=True, align="l" + "c" * 5)


def table5():
    """Rank stability."""
    hdr, raw = read("t04_stability.tsv")
    rows = []
    for r in raw:
        lab = r[0]
        if lab.startswith("Best rule in draw: "):
            lab = "Best rule in a draw: " + RULE_LABEL[lab.split(": ")[1]].lower()
        rows.append(R(lab, r[1]))
    e = SUM["ensemble"]
    return dict(number=5,
                caption="Stability of the ranking of siting rules across the "
                        "uncertainty ensemble.",
                header=["Comparison", "Probability"],
                rows=rows, widths=[0.72, 0.28],
                note=("Over %d draws, each drawing every swept parameter, "
                      "the response function, the climate setting and the "
                      "workplace–residence divergence independently. "
                      "Probabilities are the share of draws in which the "
                      "stated comparison holds." % e["n"] + SRC),
                italic_col=None, wide=False, align="lc")


def table6():
    """Loss by response function across the ensemble."""
    hdr, raw = read("t07_byerf.tsv")
    rows = [R(ERF_LABEL[r[0]], r[1], r[2], r[3], r[4]) for r in raw]
    return dict(number=6,
                caption="Predicted loss of young workers' work capacity "
                        "across the ensemble, by response function.",
                header=["Response function", "Draws", "Median", "95th pct.",
                        "Share predicting zero"],
                rows=rows, widths=[0.24, 0.14, 0.17, 0.17, 0.28],
                note=("Hours of work capacity lost per young worker per "
                      "working day, before any planting, across the draws in "
                      "which each function was selected. The final column is "
                      "the share of those draws in which the function "
                      "predicts no loss at all. The functions built on the "
                      "ISO 7243 and NIOSH occupational limits impose a "
                      "threshold below which no loss occurs and therefore "
                      "return zero in a substantial minority of draws; the "
                      "Hothaps and Foster functions, which are continuous "
                      "over the whole range, never do." + SRC),
                italic_col=None, wide=True, align="lcccc")


def table7():
    """Sensitivity."""
    hdr, raw = read("t05_sensitivity.tsv")
    pretty = {"erf": "Choice of response function",
              "climate": "Climate setting",
              "divergence": "Workplace–residence divergence"}
    rows = [R(pretty.get(r[0], r[0].replace("_", " ")), r[1], r[2])
            for r in raw]
    return dict(number=7,
                caption="First-order sensitivity of the results to each "
                        "input.",
                header=["Input", "Hours protected", "Baseline loss"],
                rows=rows, widths=[0.50, 0.25, 0.25],
                note=("Correlation ratios: the share of the variance in the "
                      "outcome that is explained by the input alone, "
                      "estimated by binning each input and decomposing the "
                      "variance between and within bins. Inputs are listed "
                      "in descending order of their influence on the hours "
                      "protected." + SRC),
                italic_col=None, wide=False, align="lcc")


def table8():
    """The threshold — the transferable result."""
    hdr, raw = read("t06_threshold.tsv")
    rows = [R(r[0], r[1], r[2], r[3], r[4]) for r in raw]
    return dict(number=8,
                caption="The advantage of workplace-weighted over "
                        "residential siting, by workplace–residence "
                        "divergence.",
                header=["Divergence", "Draws", "Correlation", "Ratio",
                        "Probability"],
                rows=rows, widths=[0.19, 0.14, 0.24, 0.22, 0.21],
                note=("“Correlation” is the mean Pearson "
                      "correlation across cells between young exposed "
                      "workers and residents in that band. "
                      "“Ratio” is the median ratio of young "
                      "workers' hours protected by the exposed-workplace "
                      "rule to those protected by the heat-weighted "
                      "residential rule, which is the comparison that holds "
                      "heat targeting fixed and varies only whose location "
                      "is counted. “Probability” is the share of "
                      "draws in which that ratio exceeds one; it reacts to "
                      "differences too small to matter and should be read "
                      "alongside the ratio, not instead of it." + SRC),
                italic_col=None, wide=True, align="lcccc")


def tableA1():
    """The parameter registry."""
    hdr, raw = read("t0B_params.tsv")
    rows = [R(r[0].replace("_", " "), r[1], r[2], "%s–%s" % (r[3], r[4]),
              PROV_LABEL[r[5]]) for r in raw]
    c = SUM["params"]["counts"]
    return dict(number="A1",
                caption="Every parameter of the model, with its sweep "
                        "interval and its provenance.",
                header=["Parameter", "Value", "Unit", "Swept over",
                        "Provenance"],
                rows=rows, widths=[0.24, 0.12, 0.28, 0.18, 0.18],
                note=("Of %d parameters, %d take a value stated in a cited "
                      "source and %d are modelling choices. The table is "
                      "generated from the registry the code reads, so it "
                      "cannot disagree with the parameters actually used. "
                      "Assumed parameters are not defended; they are swept "
                      "across the stated interval in the uncertainty "
                      "ensemble." % (SUM["params"]["n"], c["literature"],
                                     c["assumed"]) + SRC),
                italic_col=None, wide=True, align="llllc")


def tableA2():
    """The five response functions side by side."""
    hdr, raw = read("t0A_erf.tsv")
    rows = [R(*r) for r in raw]
    return dict(number="A2",
                caption="Work capacity lost to heat at a heavy metabolic "
                        "rate, by response function.",
                header=["WBGT"] + [ERF_LABEL[h] for h in hdr[1:]],
                rows=rows, widths=[0.16] + [0.168] * 5,
                note=("Percentage of the working hour lost at a nominal "
                      "400 W metabolic rate, the class used for construction "
                      "and grounds work. WBGT in degrees Celsius. The five "
                      "functions were transcribed from open-source reference "
                      "implementations and cross-checked against one "
                      "another; they disagree by an order of magnitude in "
                      "the band in which European summers sit." + SRC),
                italic_col=None, wide=True, align="c" * 6)


def tableA3():
    """The observed European data the model is anchored to."""
    hdr, raw = read("t08_eu.tsv")
    rows = [R(r[0], r[1], r[2], r[3], r[4]) for r in raw]
    eu = SUM["eu"]
    return dict(number="A3",
                caption="Observed characteristics of European urban centres "
                        "and European summers.",
                header=["Quantity", "Lower quartile", "Median",
                        "Upper quartile", "Unit"],
                rows=rows, widths=[0.36, 0.16, 0.16, 0.16, 0.16],
                note=("The first five rows describe the %d urban centres of "
                      "the EU-27 on European territory recorded in the Global "
                      "Human Settlement Layer Urban Centre Database, release "
                      "R2019A. The last row describes mean summer (June to "
                      "August) land-surface temperature across the twenty-"
                      "seven Member States over 2001-2020, from Berkeley "
                      "Earth country series. These distributions are used to "
                      "place the synthetic city and its climate settings "
                      "inside the range European cities and European summers "
                      "occupy; no relationship is estimated from them."
                      % eu["ucdb"]["n"]),
                italic_col=None, wide=True, align="lcccl")


TABLES = {"table%d" % i: fn for i, fn in enumerate(
    [table1, table2, table3, table4, table5, table6, table7, table8],
    start=1)}
TABLES["tableA1"] = tableA1
TABLES["tableA2"] = tableA2
TABLES["tableA3"] = tableA3

FIGURES = {}
