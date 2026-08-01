# -*- coding: utf-8 -*-
"""Table and figure specifications.

Numeric content is read from the estimation output written by
analysis/run_all.py, so the manuscript cannot drift away from the estimates.
A table body is a list of ("row", [cells...]) and ("sec", "label") items.
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
    "GenAI": "GenAI", "ExpPost": "Exposure × Post", "RTI": "RTI",
    "HCU": "HCU", "OLC": "OLC", "AIGov": "AIGov",
    "GenAI_OLC": "GenAI × OLC", "GenAI_AIGov": "GenAI × AIGov",
    "GenAI_D": "GenAI (dummy)", "GenAI_lag": "GenAI (t − 1)",
    "Size": "Size", "Lev": "Lev", "ROE": "ROE", "Growth": "Growth",
    "Age": "Age", "Board": "Board", "Indep": "Indep", "Dual": "Dual",
    "TobinQ": "TobinQ", "Fixed": "Fixed", "Youth": "Youth",
    "Youth35": "Youth35", "LnYoung": "LnYoung",
}


def read(name):
    rows = [l.rstrip("\n").split("\t")
            for l in open(os.path.join(TAB, name), encoding="utf-8")]
    return rows[0], rows[1:]


_MI = re.compile(r"(?<![\w\u2013\u2014-])-(?=[\d.])")


_ZERO = re.compile(r"(?<![\w.])-(0\.0+)(?![0-9])")


def mi(s):
    """Typographic minus in front of every numeral; no signed zeros."""
    return _MI.sub(MINUS, _ZERO.sub(r"\1", s.strip()))


def lab(s):
    return NAME.get(s.strip(), s)


def R(*c):
    return ("row", [mi(str(x)) for x in c])


def S(t):
    return ("sec", t)


# ---------------------------------------------------------------------------
def table1():
    rows = [
        S("Dependent variables"),
        R("Youth", "Share of employees aged 30 or below in total employees (%)"),
        R("Youth35", "Share of employees aged 35 or below in total employees (%)"),
        R("LnYoung", "Natural logarithm of one plus the number of employees "
                     "aged 30 or below"),
        S("Explanatory variable"),
        R("GenAI", "Natural logarithm of one plus the frequency of "
                   "generative-AI keywords in the management discussion and "
                   "analysis section of the annual report"),
        R("Exposure", "Share-weighted average generative-AI exposure of the "
                      "firm's pre-shock professional composition"),
        S("Mediating variables"),
        R("RTI", "Share of employees in administrative and basic technical "
                 "categories, that is, routine-cognitive positions (%)"),
        R("HCU", "Share of employees holding a bachelor's degree or above (%)"),
        S("Moderating variables"),
        R("OLC", "Standardised pre-shock employee training and development "
                 "expenditure per employee"),
        R("AIGov", "Indicator equal to one if the annual report discloses AI or "
                   "algorithmic governance arrangements"),
        S("Control variables"),
        R("Size", "Natural logarithm of total assets"),
        R("Lev", "Total liabilities divided by total assets"),
        R("ROE", "Net profit divided by total shareholders' equity"),
        R("Growth", "Year-on-year growth rate of operating revenue"),
        R("Age", "Natural logarithm of one plus the number of years since "
                 "the firm was founded"),
        R("Board", "Natural logarithm of the number of directors"),
        R("Indep", "Number of independent directors divided by board size"),
        R("Dual", "Indicator equal to one if the CEO also chairs the board"),
        R("TobinQ", "Market value divided by the replacement cost of assets"),
        R("Fixed", "Net fixed assets divided by total assets"),
        S("Instruments"),
        R("IV_Bartik", "1984 provincial fixed-line telephone penetration rate "
                       "interacted with the national revenue index of the "
                       "artificial-intelligence industry, rebased to unity in "
                       "every pre-shock year"),
        R("IV_Peer", "Leave-one-out mean adoption intensity of other firms in "
                     "the same industry and province"),
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
                note="The sample covers Chinese A-share listed firms. All "
                     "continuous variables are winsorised at the 1st and 99th "
                     "percentiles. Variable definitions are given in Table 1.",
                italic_col=0, wide=True, align="l" + "c" * 8)


def table3():
    hdr, rows = read("t_correlation.tsv")
    keep = 8
    return dict(number=3, caption="Pairwise correlations of the main variables.",
                header=[lab(h) for h in hdr[:keep + 1]],
                rows=[R(lab(r[0]), *r[1:keep + 1]) for r in rows[:keep]],
                widths=[0.16] + [0.105] * keep,
                note=f"*** and ** denote significance at the 1% and 5% levels. "
                     "Only the first eight variables are shown; the full matrix "
                     "for all regressors is available from the authors. "
                     "Variance inflation factors for the baseline specification "
                     f"have a maximum of {SUM['vif_max']:.2f}, far below the "
                     "conventional threshold of ten.",
                italic_col=0, wide=True, align="l" + "c" * keep)


def _reg_table(fname, number, caption, note, widths=None, wide=True,
               header=None):
    hdr, rows = read(fname)
    out = []
    for r in rows:
        first = r[0].strip()
        if first in ("Firm FE", "Year FE", "Industry x year FE",
                     "Province x year FE", "Observations", "Within R2",
                     "Controls", "Dependent variable"):
            nm = {"Industry x year FE": "Industry × year FE",
                  "Province x year FE": "Province × year FE",
                  "Within R2": "Within R²"}.get(first, first)
            out.append(R(nm, *[lab(x) for x in r[1:]]))
        else:
            out.append(R(lab(first), *r[1:]))
    k = len(hdr)
    return dict(number=number, caption=caption, header=header or hdr, rows=out,
                widths=widths or [0.22] + [0.78 / (k - 1)] * (k - 1),
                note=note, italic_col=0, wide=wide,
                align="l" + "c" * (k - 1))


def table4():
    return _reg_table(
        "t_baseline.tsv", 4,
        "Benchmark regression: generative AI adoption and the youth "
        "employment share.",
        "The dependent variable is the share of employees aged 30 or below. "
        "Standard errors clustered at the firm level are in parentheses. "
        "***, ** and * denote significance at the 1%, 5% and 10% levels. "
        "Column (3) replaces the continuous adoption measure with the "
        "interaction of ex-ante task exposure and the post-2022 indicator.")


def table5():
    return _reg_table(
        "t_mechanism.tsv", 5,
        "Mechanism: task routinisation and human-capital upgrading.",
        "Columns (2) and (4) regress each mediator on adoption; columns (3) "
        "and (5) add the mediator to the outcome equation. Standard errors "
        "clustered at the firm level are in parentheses. ***, ** and * denote "
        "significance at the 1%, 5% and 10% levels.")


def table6():
    hdr, rows = read("t_mediation_boot.tsv")
    return dict(number=6,
                caption="Decomposition of the total effect into the two "
                        "mediating channels.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.26, 0.11, 0.12, 0.13, 0.16, 0.12, 0.10],
                note="Confidence intervals are bias-corrected percentile "
                     "intervals from a block bootstrap that resamples firms "
                     "with replacement (300 replications). The share of the "
                     "total effect is the indirect effect divided by the "
                     "baseline coefficient of Table 4, column (2); a negative "
                     "share indicates a channel that works against the total "
                     "effect.",
                italic_col=None, wide=True, align="lcccccc")


def table7():
    return _reg_table(
        "t_moderation.tsv", 7,
        "Moderating roles of organisational learning capability and AI "
        "governance.",
        "The dependent variable is the share of employees aged 30 or below. "
        "OLC is absorbed by the firm fixed effects because it is measured "
        "before the shock and is time invariant. Standard errors clustered at "
        "the firm level are in parentheses. ***, ** and * denote significance "
        "at the 1%, 5% and 10% levels.",
        widths=[0.31, 0.23, 0.23, 0.23])


def table8():
    return _reg_table(
        "t_endogeneity.tsv", 8,
        "Endogeneity: instrumental variables, propensity-score matching and "
        "entropy balancing.",
        "Column (1) is the first stage of the two-stage least-squares "
        "estimation and column (2) the second stage. Column (3) estimates the "
        "baseline specification on the 1:1 nearest-neighbour matched sample "
        "with a caliper of 0.02, and column (4) reweights the comparison group "
        "by entropy balancing on the first two moments of the covariates. "
        "Standard errors clustered at the firm level are in parentheses. "
        "***, ** and * denote significance at the 1%, 5% and 10% levels.",
        widths=[0.28, 0.18, 0.18, 0.18, 0.18])


def table9():
    hdr, rows = read("t_oster.tsv")
    return dict(number=9,
                caption="Bounding the scope for selection on unobservables.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.68, 0.32],
                note="Both regressions are estimated on two-way demeaned data, "
                     "so the R-squared is monotone in the set of controls. The "
                     "relative degree of selection is the ratio of selection on "
                     "unobservables to selection on observables that would be "
                     "required to drive the coefficient to zero; an absolute "
                     "value above one is conventionally read as evidence that "
                     "the result is not driven by unobserved selection, and a "
                     "negative sign indicates that the two would have to work "
                     "in opposite directions.",
                italic_col=None, wide=False, align="lc")


def table10():
    hdr, rows = read("t_robustness.tsv")
    return dict(number=10, caption="Robustness checks.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.34, 0.22, 0.16, 0.16, 0.12],
                note="Each row re-estimates the baseline specification of "
                     "Table 4, column (2), with the modification described. "
                     "Rows (1) and (2) change the dependent variable, rows (3) "
                     "and (4) the explanatory variable, and rows (5) to (8) the "
                     "inference or the sample. Standard errors are clustered at "
                     "the firm level except in row (5). ***, ** and * denote "
                     "significance at the 1%, 5% and 10% levels.",
                italic_col=None, wide=True, align="lcccc")


def table11():
    hdr, rows = read("t_heterogeneity.tsv")
    return dict(number=11, caption="Heterogeneity analysis.",
                header=["Split", "Group 1", "Coef.", "SE", "N",
                        "Group 2", "Coef.", "SE", "N", "Diff.", "p"],
                rows=[R(*r) for r in rows], fs=7.2,
                widths=[0.110, 0.115, 0.105, 0.065, 0.065, 0.125, 0.105,
                        0.065, 0.065, 0.070, 0.065],
                header_align=["l", "l", "c", "c", "c", "l", "c", "c", "c",
                              "c", "c"],
                note="Each row estimates the baseline specification separately "
                     "in the two subsamples. Coef. is the coefficient on GenAI, "
                     "Diff. is the coefficient of group 1 minus that of group 2 "
                     "and p is the p-value of the test that they are equal. Capital intensity is split at the median "
                     "of fixed-asset intensity. ***, ** and * denote "
                     "significance at the 1%, 5% and 10% levels.",
                italic_col=None, wide=True, align="ll" + "c" * 9)


def tableA1():
    hdr, rows = read("t_balance.tsv")
    return dict(number="A1",
                caption="Covariate balance before and after propensity-score "
                        "matching.",
                header=hdr, rows=[R(lab(r[0]), *r[1:]) for r in rows],
                widths=[0.18, 0.22, 0.22, 0.16, 0.11, 0.11],
                note="Standardised bias is the difference in means between the "
                     "treated and comparison groups divided by the square root "
                     "of the average of their variances, expressed in per cent. "
                     "An absolute value below ten is the conventional criterion "
                     "for adequate balance. The t-test is on the matched "
                     "sample.",
                italic_col=0, wide=True, align="lccccc")


TABLES = {"table1": table1, "table2": table2, "table3": table3,
          "table4": table4, "table5": table5, "table6": table6,
          "table7": table7, "table8": table8, "table9": table9,
          "table10": table10, "table11": table11, "tableA1": tableA1}


# ---------------------------------------------------------------------------
FIGURES = {
    "figure1": dict(
        number=1, file="figure1_framework.png", width_cm=13.8,
        caption="Conceptual framework.",
        note="Solid arrows are the hypothesised relationships and the sign "
             "next to each arrow is the expected direction. H1 is the direct "
             "effect, H2 and H3 are the two mediating channels, and H4 and H5 "
             "are the organisational moderators of the direct path."),
    "figure2": dict(
        number=2, file="figure2_trends.png", width_cm=13.8,
        caption="Generative AI adoption and the youth employment share of "
                "Chinese listed firms, 2016–2025.",
        note="Adoption intensity is the sample mean of the text-based measure "
             "defined in Equation (1). The vertical dotted line marks the "
             "public release of large language models at the end of 2022, "
             "after which the vocabulary enters annual reports."),
    "figure3": dict(
        number=3, file="figure3_eventstudy.png", width_cm=13.8,
        caption="Event-study estimates of the effect of ex-ante task exposure "
                "on the youth employment share.",
        note="Coefficients and 95% confidence intervals from Equation (4), with "
             "2022 as the omitted year and standard errors clustered at the "
             "firm level. Coefficients before the vertical line test the "
             "parallel-trends assumption; those after it trace the dynamic "
             "response."),
    "figure4": dict(
        number=4, file="figure4_marginal.png", width_cm=13.8,
        caption="Marginal effect of generative AI adoption on the youth "
                "employment share across the distribution of organisational "
                "learning capability.",
        note="Marginal effects from Equation (8) with a 95% confidence band. "
             "P25, P50 and P75 mark the quartiles of the moderator. The "
             "vertical dashed line is the point at which the effect ceases to "
             "be statistically distinguishable from zero."),
    "figure5": dict(
        number=5, file="figure5_balance.png", width_cm=13.8,
        caption="Covariate balance before and after propensity-score matching.",
        note="Standardised percentage bias for each covariate before and after "
             "1:1 nearest-neighbour matching with a caliper of 0.02. The dotted "
             "lines mark the conventional ±10% criterion for adequate balance. "
             "The corresponding t-tests are reported in Table A1."),
    "figure6": dict(
        number=6, file="figure6_placebo.png", width_cm=13.8,
        caption="Placebo distribution from random reassignment of ex-ante task "
                "exposure.",
        note="Distribution of the coefficient on the interaction of exposure "
             "and the post-2022 indicator when ex-ante exposure is randomly "
             "reassigned across firms. The vertical line is the estimate "
             "obtained with the actual assignment."),
}
