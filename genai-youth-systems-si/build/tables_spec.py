# -*- coding: utf-8 -*-
"""Table and figure specifications.

Numeric content is read from the estimation output written by
analysis/run_all.py, so the manuscript cannot drift away from the estimates.
A table body is a list of ("row", [cells...]) and ("sec", "label") items.

Tables and figures are numbered by the order in which the text first mentions
them.
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


def read(name):
    rows = [l.rstrip("\n").split("\t")
            for l in open(os.path.join(TAB, name), encoding="utf-8")]
    return rows[0], rows[1:]


def mi(s):
    """Typographic minus in front of every numeral; no signed zeros."""
    s = str(s).strip()
    if s == "-":
        return "—"
    return _MI.sub(MINUS, _ZERO.sub(r"\1", s))


def R(*c):
    return ("row", [mi(x) for x in c])


def S(t):
    return ("sec", t)


SE_NOTE = ("The dependent variable is Youth, the share of employees aged 30 or "
           "below in the firm's total workforce, in percentage points. Values "
           "in parentheses are standard errors clustered at the firm level. "
           "***, ** and * denote significance at the 1%, 5% and 10% levels, "
           "respectively. Source: authors' own calculations.")
SRC = " Source: authors' own calculations."


def _pairs(rows, ncol):
    """Turn the coefficient/standard-error line pairs into table rows."""
    out = []
    for r in rows:
        out.append(R(*(r + [""] * (ncol - len(r)))))
    return out


# ---------------------------------------------------------------------------
def table1():
    rows = [
        S("Dependent variable"),
        R("Youth", "Share of employees aged 30 or below in the firm's total "
                   "workforce (%)"),
        S("Explanatory variable"),
        R("GenAI", "Generative artificial intelligence application intensity: "
                   "the natural logarithm of one plus the frequency of "
                   "generative-AI terms in the management discussion and "
                   "analysis section of the annual report"),
        S("Mediating variables"),
        R("Train", "Natural logarithm of employee education and training "
                   "expenditure per employee (yuan)"),
        R("Routine", "Routine task base: the share of the workforce employed "
                     "in occupational categories classified as routine (%)"),
        S("Moderating variables"),
        R("Absorp", "Organizational learning capability: research and "
                    "development expenditure as a percentage of operating "
                    "revenue"),
        R("Wage", "Relative labor cost: the natural logarithm of cash paid to "
                  "and on behalf of employees per employee"),
        S("Control variables"),
        R("Size", "Natural logarithm of total assets"),
        R("Lev", "Total liabilities divided by total assets"),
        R("ROA", "Net profit divided by total assets"),
        R("Growth", "Year-on-year growth rate of operating revenue"),
        R("Cashflow", "Net operating cash flow divided by total assets"),
        R("TobinQ", "Market value divided by the replacement cost of assets"),
        R("Top1", "Shareholding of the largest shareholder"),
        R("Indep", "Share of independent directors on the board"),
        R("Dual", "Indicator equal to one when the chair and the chief "
                  "executive are the same person"),
        R("Board", "Natural logarithm of the number of directors"),
        R("CapInt", "Natural logarithm of net fixed assets per employee"),
        S("Instrumental variables"),
        R("Telephone84 × Nat",
          "Fixed-line telephones per hundred residents in the firm's "
          "prefecture in 1984, interacted with the national generative-AI "
          "diffusion index"),
        R("PeerAI", "Mean generative-AI application intensity of firms in the "
                    "same industry located outside the firm's own province"),
        S("Placebo variable"),
        R("Exper", "Share of employees aged 31 to 50 in the firm's total "
                   "workforce (%)"),
    ]
    return dict(number=1, caption="Variable definitions and measurement.",
                header=["Variable", "Definition"], rows=rows,
                widths=[0.19, 0.81], note=None, italic_col=0, wide=False,
                align="ll")


def table2():
    hdr, rows = read("t02_descriptives.tsv")
    return dict(number=2, caption="Descriptive statistics.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.20] + [0.133] * 6, note=(
                    "The sample comprises %s firm-year observations for %s "
                    "Chinese A-share listed firms over %s. All continuous "
                    "variables are winsorized at the first and ninety-ninth "
                    "percentiles.%s"
                    % ("{:,}".format(SUM["n_obs"]),
                       "{:,}".format(SUM["n_firms"]),
                       SUM["years"].replace("-", "–"), SRC)),
                italic_col=0, wide=False, align="l" + "c" * 6)


def table3():
    hdr, rows = read("t03_correlation.tsv")
    keep = 12
    hdr = hdr[:1 + keep] + [hdr[-1]]
    rows = [r[:1 + keep] + [r[-1]] for r in rows]
    return dict(number=3, caption="Pearson correlation coefficients and "
                                  "variance inflation factors.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=([0.112] + [0.066] * 10 + [0.086, 0.066]
                        + [0.069]), note=(
                    "The lower triangle reports pairwise Pearson correlation "
                    "coefficients. The final column reports the variance "
                    "inflation factor of each regressor after the two-way "
                    "within transformation; the largest value is %.2f, far "
                    "below the conventional threshold of five, so "
                    "multicollinearity is not a concern.%s"
                    % (SUM["vif_max"], SRC)),
                italic_col=0, wide=True, align="l" + "c" * (keep + 1),
                fs=6.0)


def table4():
    hdr, rows = read("t04_benchmark.tsv")
    return dict(number=4, caption="Benchmark regression results.",
                header=hdr, rows=_pairs(rows, 6),
                widths=[0.22] + [0.156] * 5, note=(
                    "Column (1) includes firm fixed effects only; column (2) "
                    "adds year fixed effects; column (3) is the benchmark "
                    "specification; columns (4) and (5) replace the year "
                    "effects with industry-by-year and province-by-year "
                    "effects. " + SE_NOTE),
                italic_col=0, wide=False, align="l" + "c" * 5)


def table5():
    hdr, rows = read("t05_mechanism.tsv")
    return dict(number=5, caption="Tests of the mediating mechanisms.",
                header=hdr, rows=_pairs(rows, 7),
                widths=[0.20] + [0.1333] * 6, note=(
                    "The dependent variable is named in each column heading. "
                    "Youth is the share of employees aged 30 or below (%); "
                    "Train is the logarithm of training expenditure per "
                    "employee; Routine is the routine task base (%). Values in "
                    "parentheses are standard errors clustered at the firm "
                    "level. ***, ** and * denote significance at the 1%, 5% "
                    "and 10% levels, respectively." + SRC),
                italic_col=0, wide=True, align="l" + "c" * 6, fs=7.2)


def table6():
    hdr, rows = read("t06_indirect.tsv")
    return dict(number=6, caption="Bootstrapped decomposition of the total "
                                  "effect.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.16, 0.11, 0.09, 0.09, 0.11, 0.11, 0.18, 0.15],
                note=("Path a is the effect of GenAI on the mediator; path b "
                      "is the effect of the mediator on Youth conditional on "
                      "GenAI. The indirect effect is the product of the two "
                      "paths and its confidence interval is the percentile "
                      "interval of %d bootstrap replications that resample "
                      "whole firms. ***, ** and * denote significance at the "
                      "1%%, 5%% and 10%% levels, respectively.%s"
                      % (SUM["n_boot_med"], SRC)),
                italic_col=0, wide=True, align="l" + "c" * 7, fs=7.2)


def table7():
    hdr, rows = read("t07_endogeneity.tsv")
    return dict(number=7, caption="Endogeneity tests.",
                header=hdr, rows=_pairs(rows, 6),
                widths=[0.26] + [0.148] * 5, note=(
                    "Column (1) reports the first stage of the two-stage "
                    "least-squares estimation, whose dependent variable is "
                    "GenAI; the remaining columns take Youth as the dependent "
                    "variable. Column (4) uses the sample matched one to one "
                    "on the propensity score and column (5) weights the "
                    "sample by entropy-balancing weights. The null hypothesis "
                    "of the Hansen J test is that the instruments are "
                    "uncorrelated with the second-stage error; the null of "
                    "the Durbin-Wu-Hausman test is that GenAI is exogenous. "
                    + SE_NOTE),
                italic_col=0, wide=False, align="l" + "c" * 5)


def table8():
    hdr, rows = read("t08_robustness.tsv")
    return dict(number=8, caption="Robustness checks.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.38, 0.14, 0.12, 0.20, 0.16], note=(
                    "Each row is a separate regression that retains the full "
                    "set of controls and the firm and year fixed effects of "
                    "the benchmark specification. The reported coefficient is "
                    "that of the adoption measure named in the first column. "
                    + SE_NOTE),
                italic_col=0, wide=False, align="lcccc")


def table9():
    hdr, rows = read("t09_moderation.tsv")
    return dict(number=9, caption="Moderating effects of organizational "
                                  "learning capability, relative labor cost "
                                  "and the generative-AI break.",
                header=hdr, rows=_pairs(rows, 5),
                widths=[0.28] + [0.18] * 4, note=(
                    "Absorp and Wage are standardized before the interaction "
                    "is formed, so the coefficient on GenAI is the effect at "
                    "the sample mean of the moderator. Post equals one from "
                    "2023 onwards. " + SE_NOTE),
                italic_col=0, wide=False, align="l" + "c" * 4)


def table10():
    hdr, rows = read("t10_heterogeneity.tsv")
    return dict(number=10, caption="Heterogeneity analysis.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.24, 0.11, 0.09, 0.11, 0.09, 0.10, 0.09, 0.085,
                        0.085],
                note=("Each row reports two separate regressions run on the "
                      "subsamples named in the first column, both retaining "
                      "the full set of controls and the firm and year fixed "
                      "effects. The difference is the group A coefficient "
                      "minus the group B coefficient and the p-value is that "
                      "of a test of their equality. " + SE_NOTE),
                italic_col=0, wide=True, align="l" + "c" * 8, fs=7.0)


def table11():
    hdr, rows = read("t11_pvar.tsv")
    return dict(number=11, caption="Panel vector autoregression estimates and "
                                   "Granger causality tests.",
                header=hdr, rows=_pairs(rows, 4),
                widths=[0.34, 0.22, 0.22, 0.22], note=(
                    "The system is estimated on firm-level deviations from "
                    "the annual cross-sectional mean, with firm effects "
                    "removed by the within transformation and the leading "
                    "term of the dynamic-panel bias removed by the half-panel "
                    "jackknife. Values in parentheses are bootstrap standard "
                    "errors from %d replications that resample whole firms. "
                    "Figures in square brackets are the p-values of the "
                    "Granger causality Wald statistics, whose null hypothesis "
                    "is that the lag of the column variable does not enter "
                    "the row equation. ***, ** and * denote significance at "
                    "the 1%%, 5%% and 10%% levels, respectively.%s"
                    % (SUM["pvar"]["n_boot"], SRC)),
                italic_col=0, wide=False, align="lccc")


def table12():
    hdr, rows = read("t12_irf.tsv")
    return dict(number=12, caption="Impulse responses and the amplification "
                                   "attributable to the reinforcing loop.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.244] + [0.084] * 9, note=(
                    "Responses are orthogonalized by a Cholesky "
                    "decomposition with the variables ordered GenAI, Train, "
                    "Youth, so that adoption may move the other two "
                    "contemporaneously but not the reverse. Figures in square "
                    "brackets are 90% bootstrap intervals. The loop-suppressed "
                    "path sets the two return coefficients of the GenAI "
                    "equation to zero and re-simulates the system; the "
                    "amplification factor is the ratio of the two cumulative "
                    "paths." + SRC),
                italic_col=0, wide=True, align="l" + "c" * 9, fs=6.4)


TABLES = {"table1": table1, "table2": table2, "table3": table3,
          "table4": table4, "table5": table5, "table6": table6,
          "table7": table7, "table8": table8, "table9": table9,
          "table10": table10, "table11": table11, "table12": table12}

FIGURES = {
    "fig1": dict(number=1, file="figure1_framework.png", width_cm=13.2,
                 caption="Conceptual framework.", note=None),
    "fig2": dict(number=2, file="figure2_moderation.png", width_cm=13.2,
                 caption="Marginal effect of generative artificial "
                         "intelligence adoption on the youth employment "
                         "share.", note=None),
    "fig3": dict(number=3, file="figure3_irf.png", width_cm=13.2,
                 caption="Orthogonalized impulse responses of the "
                         "adoption–capability–youth system.",
                 note=None),
}
