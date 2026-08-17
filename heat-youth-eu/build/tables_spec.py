# -*- coding: utf-8 -*-
"""Table and figure specifications.

Numeric content is read from the estimation output written by
analysis/run_all.py, so the manuscript cannot drift away from the
estimates. Tables and figures are numbered by the order in which the
text first mentions them.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as _fh:
    SUM = json.load(_fh)

MINUS = "−"
NBSP = " "
_MI = re.compile(r"(?<![\w–—-])-(?=[\d.])")
_ZERO = re.compile(r"(?<![\w.])-(0\.0+)(?![0-9])")


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


def S(t):
    return ("sec", t)


SRC = " Source: authors' calculations."


# ---------------------------------------------------------------------------
def table1():
    rows = [
        R("NEET", "Youth NEET rate (15–29 years)",
          "% of the age-group population", "edat_lfse_20"),
        R("YUR", "Youth unemployment rate (15–24 years)",
          "% of the age-group labour force", "une_rt_a"),
        R("CDD", "Cooling degree days", "Annual degree days",
          "nrg_chdd_a"),
        R("GRN", "Green infrastructure share of functional urban "
          "areas", "% of functional urban area", "Urban Atlas 2018"),
        R("GDPG", "Real GDP growth rate", "% change on previous year",
          "tec00115"),
        R("TERT", "Tertiary educational attainment (25–34 years)",
          "% of the age-group population", "edat_lfse_03"),
    ]
    return dict(number=1, caption="Description of variables used in the "
                                  "empirical analysis.",
                header=["Variable", "Description", "Measurement",
                        "Source"],
                rows=rows,
                widths=[0.13, 0.37, 0.28, 0.22],
                note=("Source: authors' design based on "
                      "[[es_neet],[es_yur],[es_cdd],[urbanatlas],"
                      "[es_gdpg],[es_tert]]. In the estimations, "
                      "cooling degree days enter as CDD100 = CDD/100."),
                italic_col=None, wide=False, align="lllc")


def table2():
    hdr, raw = read("t02_descriptives.tsv")
    return dict(number=2, caption="Descriptive statistics of the "
                                  "variables, EU-27, 2010–2024.",
                header=["Variable", "Mean", "Std. Dev.", "Minimum",
                        "Maximum", "Obs."],
                rows=[R(*r) for r in raw],
                widths=[0.16, 0.17, 0.17, 0.17, 0.17, 0.16],
                note=("The green infrastructure share is a "
                      "time-invariant country endowment; all other "
                      "variables vary by country and year." + SRC),
                italic_col=None, wide=False, align="l" + "c" * 5)


def table3():
    hdr, raw = read("t03_correlations.tsv")
    return dict(number=3,
                caption="Pearson correlation matrix of the variables.",
                header=["Variable", "NEET", "CDD100", "GRN", "GDPG",
                        "TERT"],
                rows=[R(*r) for r in raw],
                widths=[0.20] + [0.16] * 5,
                note=("Pooled correlations over the 405 country-year "
                      "observations." + SRC),
                italic_col=None, wide=False, align="l" + "c" * 5)


def table4():
    hdr, raw = read("t04_gmm_neet.tsv")
    return dict(number=4,
                caption="Dynamic panel estimation results for the youth "
                        "NEET rate using the System GMM estimator.",
                header=["Variable", "Coefficient", "p-Value",
                        "Interpretation"],
                rows=[R(*r) for r in raw],
                widths=[0.24, 0.20, 0.16, 0.40],
                note=("Two-step System GMM with the Windmeijer "
                      "finite-sample correction; all variables enter "
                      "as deviations from period means, which is "
                      "equivalent to including a full set of time "
                      "dummies." + SRC),
                italic_col=None, wide=False, align="lccl")


def table5():
    hdr, raw = read("t05_diagnostics.tsv")
    return dict(number=5,
                caption="Diagnostic tests for the System GMM estimator.",
                header=["Test", "Value"],
                rows=[R(*r) for r in raw],
                widths=[0.62, 0.38],
                note=("AR(1) and AR(2) denote the p-values of the "
                      "Arellano–Bond tests for first- and "
                      "second-order serial correlation in the "
                      "differenced residuals; the Hansen test reports "
                      "the p-value for the joint validity of the "
                      "instrument set." + SRC),
                italic_col=None, wide=False, align="lc")


def _fullnote(dep):
    return ("The dependent variable is %s. Two-step System GMM with "
            "the Windmeijer correction; variables enter as deviations "
            "from period means. AR(1) and AR(2) denote the p-values of "
            "the Arellano–Bond serial-correlation tests; the "
            "Hansen test reports the p-value for the joint validity of "
            "the instruments." % dep + SRC)


def _sens_table(number, tsv, caption, dep):
    hdr, raw = read(tsv)
    rows = []
    for r in raw:
        if r[0].startswith("SEC:"):
            rows.append(S(r[0][4:]))
        else:
            rows.append(R(*r))
    return dict(number=number, caption=caption,
                header=["Variable", "Coefficient", "Std. Error",
                        "z-Statistic", "p-Value"],
                rows=rows,
                widths=[0.30, 0.19, 0.17, 0.17, 0.17],
                note=_fullnote(dep),
                italic_col=None, wide=False, align="l" + "c" * 4)


def table6():
    return _sens_table(
        6, "t06_yur.tsv",
        "Sensitivity analysis using the youth unemployment rate as the "
        "dependent variable.",
        "the youth unemployment rate (15–24)")


def table7():
    return _sens_table(
        7, "t07_prepandemic.tsv",
        "Robustness estimation on the pre-pandemic subsample, "
        "2010–2019.",
        "the youth NEET rate (15–29)")


TABLES = {"table%d" % i: fn for i, fn in enumerate(
    [table1, table2, table3, table4, table5, table6, table7], start=1)}

FIGURES = {
    "fig1": dict(number=1, file="figure1_trends.png", width_cm=13.2,
                 caption="EU-27 averages, 2010–2024: (a) cooling "
                         "degree days; (b) youth NEET rate.",
                 note=None),
    "fig2": dict(number=2, file="figure2_cross.png", width_cm=13.2,
                 caption="Average summer heat exposure and the average "
                         "youth NEET rate across the EU-27, "
                         "2010–2024.", note=None),
    "fig3": dict(number=3, file="figure3_margins.png", width_cm=13.2,
                 caption="Estimated effect of an additional 100 cooling "
                         "degree days on the youth NEET rate across the "
                         "green infrastructure endowment of functional "
                         "urban areas.", note=None),
}
