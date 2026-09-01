# -*- coding: utf-8 -*-
"""Table specifications.

Numeric content is read from the estimation output written by
analysis/run_all.py, so the manuscript cannot drift away from the estimates.
A table body is a list of ("row", [cells...]) and ("sec", "label") items.

Tables are numbered by the order in which the text first mentions them.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
with open(os.path.join(TAB, "summary.json"), encoding="utf-8") as _fh:
    SUM = json.load(_fh)

MINUS = "−"

NAME = {
    "AIU": "AIU", "AIE": "AIE", "FirmEPU": "EPU",
    "AIUxSpecTrain": "AIU × SpecTrain", "AIUxFireCost": "AIU × FireCost",
    "AIUxFlex": "AIU × Flex",
    "EntryRate": "Entry", "EntryPost": "EntryPost", "ExpRate": "Exper",
    "ContShare": "Cont", "YouthShare": "Youth", "NetYouth": "NetYouth",
    "Inaction": "Inact", "SpecTrain": "SpecTrain", "FireCost": "FireCost",
    "Flex": "Flex", "Size": "Size", "Lev": "Lev", "ROA": "ROA",
    "Growth": "Growth", "Cash": "Cash", "FirmAge": "Age", "TobinQ": "TobinQ",
    "CapInt": "CapInt", "Wage": "Wage", "Analyst": "Analyst",
    "InstOwn": "InstOwn", "GDPg": "GDPg", "YouthU": "YouthU",
    "IV_Shift": "IV^{Shift}", "IV_Frontier": "IV^{Front}",
    "IV_Peer": "IV^{Peer}",
}

_MI = re.compile(r"(?<![\w–—-])-(?=[\d.])")
_ZERO = re.compile(r"(?<![\w.])-(0\.0+)(?![0-9])")


def read(name):
    rows = [l.rstrip("\n").split("\t")
            for l in open(os.path.join(TAB, name), encoding="utf-8")]
    return rows[0], rows[1:]


def mi(s):
    """Typographic minus in front of every numeral; no signed zeros."""
    return _MI.sub(MINUS, _ZERO.sub(r"\1", str(s).strip()))


def lab(s):
    return NAME.get(str(s).strip(), s)


def R(*c):
    return ("row", [mi(x) for x in c])


def S(t):
    return ("sec", t)


CLUSTER_NOTE = ("Standard errors clustered at the firm level are in "
                "parentheses. ***, ** and * denote significance at the 1%, 5% "
                "and 10% levels.")


# ---------------------------------------------------------------------------
def table1():
    rows = [
        S("Dependent variables"),
        R("Entry", "Number of distinct entry-level vacancies posted in the "
                   "year per thousand employees at the end of the previous "
                   "year. A vacancy is entry-level if it requires no prior "
                   "experience or at most one year, or is advertised as campus "
                   "recruitment"),
        R("EntryPost", "Count of entry-level vacancies posted in the year"),
        R("Exper", "Number of vacancies requiring five or more years of "
                   "experience, per thousand employees at the end of the "
                   "previous year"),
        R("Cont", "Share of the firm's entry-level vacancies advertised as "
                  "internships, agency or dispatch placements, or fixed-term "
                  "contracts of one year or less (%)"),
        R("Youth", "Share of employees aged 30 or below in total employees (%)"),
        R("NetYouth", "Net change in the number of employees aged 30 or below, "
                      "scaled by lagged total employment (%)"),
        R("Inact", "Indicator equal to one if NetYouth lies within half a "
                   "percentage point of zero"),
        S("Explanatory variables"),
        R("AIU", "Generative-AI uncertainty: standardised logarithm of the "
                 "frequency with which a generative-AI term appears within a "
                 "ten-word window of an uncertainty term in the management "
                 "discussion and risk-factor sections of the annual report, "
                 "scaled by document length"),
        R("AIE", "Generative-AI engagement: standardised logarithm of the "
                 "frequency of the same generative-AI dictionary with no "
                 "uncertainty window"),
        R("EPU", "Firm-level economic policy uncertainty: the same measure as "
                 "AIU with the generative-AI dictionary replaced by the "
                 "economic policy dictionary"),
        S("Moderating variables"),
        R("SpecTrain", "Standardised pre-shock ratio of employee education and "
                       "training expenditure to the number of employees"),
        R("FireCost", "Standardised provincial index of employment-protection "
                      "enforcement, built from labour-dispute arbitration "
                      "awards against employers per thousand employees"),
        R("Flex", "Standardised pre-shock share of dispatched and outsourced "
                  "workers in total employment"),
        S("Control variables"),
        R("Size", "Natural logarithm of total assets"),
        R("Lev", "Total liabilities divided by total assets"),
        R("ROA", "Net profit divided by total assets"),
        R("Growth", "Year-on-year growth rate of operating revenue"),
        R("Cash", "Cash and cash equivalents divided by total assets"),
        R("Age", "Natural logarithm of one plus the number of years since the "
                 "firm was founded"),
        R("TobinQ", "Market value divided by the replacement cost of assets"),
        R("CapInt", "Natural logarithm of net fixed assets per employee"),
        R("Wage", "Natural logarithm of cash paid to and on behalf of "
                  "employees divided by the number of employees"),
        R("Analyst", "Natural logarithm of one plus the number of analysts "
                     "issuing an earnings forecast for the firm in the year"),
        R("InstOwn", "Share of shares held by institutional investors"),
        R("GDPg", "Real growth rate of provincial gross domestic product (%)"),
        R("YouthU", "Provincial surveyed unemployment rate of the population "
                    "aged 16 to 24 (%)"),
        S("Instruments"),
        R("IV^{Shift}", "Pre-sample occupational exposure of the firm's task "
                        "bundle to language models interacted with the "
                        "national generative-AI uncertainty index"),
        R("IV^{Front}", "The same pre-sample exposure interacted with the "
                        "number of frontier model releases in the year"),
        R("IV^{Peer}", "Leave-one-out mean of AIU among other listed firms "
                       "headquartered in the same province"),
    ]
    return dict(number=1, caption="Definitions of variables.",
                header=["Variable", "Definition"], rows=rows,
                widths=[0.20, 0.80], note=None, italic_col=0, wide=False,
                align="ll")


def table2():
    hdr, rows = read("t_descriptives.tsv")
    return dict(number=2, caption="Descriptive statistics.",
                header=hdr, rows=[R(lab(r[0]), *r[1:]) for r in rows],
                widths=[0.16] + [0.105] * 8,
                note="The sample covers Chinese A-share listed firms over "
                     f"{SUM['years'].replace('-', '–')}. All continuous "
                     "variables are winsorised at the 1st and 99th "
                     "percentiles. AIU, AIE and EPU are standardised over the "
                     "estimation sample. Variable definitions are given in "
                     "Table 1.",
                italic_col=0, wide=True, align="l" + "c" * 8)


def table3():
    hdr, rows = read("t_correlation.tsv")
    return dict(number=3,
                caption="Pearson correlations of the main variables.",
                header=[lab(h) for h in hdr],
                rows=[R(lab(r[0]), *r[1:]) for r in rows],
                widths=[0.13] + [0.087] * 10,
                note="***, ** and * denote significance at the 1%, 5% and 10% "
                     "levels. Variance inflation factors computed after the "
                     "two-way within transformation have a maximum of "
                     f"{SUM['vif_max']:.2f} and a mean of "
                     f"{SUM['vif_mean']:.2f}.",
                italic_col=0, wide=True, align="l" + "c" * 10, fs=7.0)


TAILS = {"Firm FE", "Year FE", "Industry x year FE", "Province x year FE",
         "Observations", "Within R2", "Controls", "Estimator",
         "Kleibergen-Paap rk Wald F", "Hansen J (p)", "Wu-Hausman (p)",
         "Cross-equation difference", "Effect at moderator = -1 SD",
         "Effect at moderator = +1 SD",
         "Joint test of pre-shock leads, chi2",
         "Joint test of pre-shock leads, p",
         "Panel A: first stage, dependent variable AIU",
         "Panel B: second stage"}

RENAME = {"Industry x year FE": "Industry × year FE",
          "Province x year FE": "Province × year FE",
          "Within R2": "Within R²",
          "Kleibergen-Paap rk Wald F": "Kleibergen–Paap rk Wald F",
          "Wu-Hausman (p)": "Wu–Hausman (p)",
          "Effect at moderator = -1 SD": "Effect at moderator = −1 SD",
          "Effect at moderator = +1 SD": "Effect at moderator = +1 SD",
          "Joint test of pre-shock leads, chi2":
              "Joint test of pre-shock leads, χ²",
          "Panel A: first stage, dependent variable AIU":
              "Panel A: first stage, dependent variable AIU",
          "Panel B: second stage": "Panel B: second stage"}


def _reg_table(fname, number, caption, note, widths=None, wide=True,
               header=None, fs=None):
    hdr, rows = read(fname)
    out = []
    for r in rows:
        first = r[0].strip()
        if first in TAILS:
            out.append(R(RENAME.get(first, first), *r[1:]))
        else:
            out.append(R(lab(first), *r[1:]))
    k = len(hdr)
    return dict(number=number, caption=caption, header=header or hdr, rows=out,
                widths=widths or [0.24] + [0.76 / (k - 1)] * (k - 1),
                note=note, italic_col=0, wide=wide, fs=fs,
                align="l" + "c" * (k - 1))


def table4():
    return _reg_table(
        "t_baseline.tsv", 4,
        "Generative-AI uncertainty and entry-level vacancy creation.",
        "The dependent variable is the entry-level vacancy rate in columns (1) "
        "to (4), the entry-level vacancy count in column (5) and the share of "
        "employees aged 30 or below in column (6). Columns (1) to (4) and (6) "
        "estimate Equation (8) by least squares; column (5) estimates Equation "
        "(9) by Poisson pseudo-maximum likelihood with two absorbed effect "
        "dimensions and reports a semi-elasticity, and the statistic reported "
        "for it is a deviance-based pseudo R-squared. " + CLUSTER_NOTE)


def table5():
    return _reg_table(
        "t_agespec.tsv", 5,
        "Is the chill specific to the young? Entry-level against experienced "
        "vacancies.",
        "The dependent variable is the entry-level vacancy rate in column (1), "
        "the experienced vacancy rate in column (2), and the corresponding "
        "counts in columns (3) and (4), estimated by Poisson pseudo-maximum "
        "likelihood. The cross-equation difference is the coefficient on the "
        "interaction of AIU with the equation indicator in the stacked model of "
        "Equation (11), whose covariance is clustered on the firm across both "
        "equations. " + CLUSTER_NOTE,
        widths=[0.32, 0.17, 0.17, 0.17, 0.17])


def table6():
    return _reg_table(
        "t_irrev.tsv", 6,
        "Irreversibility: the chill and the sunk component of an entry-level "
        "hire.",
        "The dependent variable is the entry-level vacancy rate and the model "
        "is Equation (10). The two rows of marginal effects report "
        "α₁ + α₄Z evaluated one standard deviation below and above the mean of "
        "the moderator used in that column. " + CLUSTER_NOTE,
        widths=[0.34, 0.165, 0.165, 0.165, 0.165])


def table7():
    return _reg_table(
        "t_contingent.tsv", 7,
        "The contingent turn: the composition of entry-level hiring.",
        "The dependent variable is the contingent share of entry-level "
        "vacancies in columns (1) to (4) and the entry-level vacancy rate in "
        "column (5). " + CLUSTER_NOTE,
        widths=[0.30, 0.14, 0.14, 0.14, 0.14, 0.14])


def table8():
    return _reg_table(
        "t_inaction.tsv", 8,
        "The zone of inaction and its hysteresis.",
        "The dependent variable is an indicator for no adjustment to the young "
        "workforce in columns (1) to (3), an indicator for a positive net "
        "change in column (4), estimated on the subsample of firms that were "
        "inactive in the previous year, and the net change itself in column "
        "(5). Columns (1) to (4) are linear probability models with firm and "
        "year effects absorbed. " + CLUSTER_NOTE,
        widths=[0.30, 0.14, 0.14, 0.14, 0.14, 0.14])


def table9():
    return _reg_table(
        "t_iv.tsv", 9,
        "Endogeneity: instrumental-variables estimates.",
        "Panel A reports the first stage of Equation (12); Panel B reports "
        "Equation (13). The dependent variable is the entry-level vacancy rate "
        "in columns (1) to (3), the contingent share in column (4) and the "
        "experienced vacancy rate in column (5). The Hansen statistic tests the "
        "overidentifying restrictions and the Wu–Hausman statistic tests the "
        "exogeneity of AIU. " + CLUSTER_NOTE,
        widths=[0.30, 0.14, 0.14, 0.14, 0.14, 0.14])


def table10():
    return _reg_table(
        "t_did.tsv", 10,
        "Dynamic difference in differences around the frontier-model releases.",
        "The model is Equation (14). Treated firms are those in the top tertile "
        "of pre-sample occupational exposure to language models and 2021 is the "
        "reference year. The joint test of pre-shock leads is a Wald test that "
        "the interactions for 2016 to 2020 are jointly zero. " + CLUSTER_NOTE,
        widths=[0.40, 0.30, 0.30], wide=False)


def table11():
    hdr, rows = read("t_robust.tsv")
    return dict(
        number=11, caption="Robustness checks.",
        header=["Specification", "AIU", "SE", "N", "Within R²"],
        rows=[R(*r) for r in rows], widths=[0.46, 0.14, 0.14, 0.14, 0.12],
        note="Each row is a separate estimation of Equation (8) with the "
             "modification named in the first column; the coefficient reported "
             "is that on AIU. The specification in logs uses the logarithm of "
             "one plus the entry-level vacancy count and is therefore not in "
             "the units of the other rows. " + CLUSTER_NOTE,
        italic_col=None, wide=True, align="lcccc")


def table12():
    hdr, rows = read("t_hetero.tsv")
    return dict(
        number=12, caption="Heterogeneity analysis.",
        header=["Partition", "Subsample A", "AIU", "N", "Subsample B", "AIU",
                "N", "Difference"],
        rows=[R(*r) for r in rows],
        widths=[0.17, 0.14, 0.12, 0.10, 0.13, 0.12, 0.10, 0.12],
        note="Each partition re-estimates Equation (8) on the two subsamples. "
             "The difference is the coefficient in subsample A minus that in "
             "subsample B, with a standard error computed from the two "
             "independent estimates. " + CLUSTER_NOTE,
        italic_col=None, wide=True, align="llcclccc", fs=7.4)


def tableA1():
    hdr, rows = read("t_alt.tsv")
    return dict(
        number="A1", caption="Placebo tests and alternative measures.",
        header=["Specification", "Coefficient", "SE", "N", "Within R²"],
        rows=[R(*r) for r in rows], widths=[0.48, 0.14, 0.13, 0.13, 0.12],
        note="The coefficient reported is that on the variable named in the "
             "first column, or on AIU where no other variable is named. All "
             "specifications include the full control vector and firm and year "
             "effects. " + CLUSTER_NOTE,
        italic_col=None, wide=True, align="lcccc")


TABLES = {"table1": table1, "table2": table2, "table3": table3,
          "table4": table4, "table5": table5, "table6": table6,
          "table7": table7, "table8": table8, "table9": table9,
          "table10": table10, "table11": table11, "table12": table12,
          "tableA1": tableA1}

# This manuscript reports no figures: the argument is carried entirely by the
# estimates, and every quantity a plot would show is already in a table.
FIGURES = {}
