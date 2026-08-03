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
    s = str(s).strip()
    if s == "-":
        return "—"
    return _MI.sub(MINUS, _ZERO.sub(r"\1", s))


def R(*c):
    return ("row", [mi(x) for x in c])


def S(t):
    return ("sec", t)


SE_NOTE = ("The dependent variable is Youth, the share of employees aged 30 "
           "or below in the firm's total workforce, in percentage points. "
           "Values in parentheses are standard errors clustered at the firm "
           "level. ***, ** and * denote significance at the 1%, 5% and 10% "
           "levels, respectively. Source: authors' own calculations.")
SRC = " Source: authors' own calculations."


def _pairs(rows, ncol):
    return [R(*(r + [""] * (ncol - len(r)))) for r in rows]


# ---------------------------------------------------------------------------
def table1():
    rows = [
        S("Dependent variable"),
        R("Youth", "Share of employees aged 30 or below in the firm's total "
                   "workforce (%)"),
        S("Explanatory variables"),
        R("Variety", "Workforce skill variety: the Shannon entropy, in bits, "
                     "of the firm's workforce distributed over five "
                     "disclosed occupational categories and three education "
                     "levels"),
        R("RelVar", "Related variety: the employment-weighted mean entropy of "
                    "the education distribution within each occupational "
                    "category"),
        R("UnrelVar", "Unrelated variety: the entropy of the distribution of "
                      "employment across the five occupational categories, so "
                      "that Variety = RelVar + UnrelVar"),
        R("Shock", "Industry demand shock: the negative of the year-on-year "
                   "growth rate of national operating revenue in the firm's "
                   "two-digit industry, standardized over the sample, so that "
                   "a higher value is a more adverse shock"),
        S("Mediating variables"),
        R("Redeploy", "Internal redeployment: the index of dissimilarity "
                      "between the firm's occupational distribution this year "
                      "and last year (%)"),
        R("Churn", "Workforce churn: gross separations as a percentage of "
                   "average employment"),
        S("Moderating variables"),
        R("Digital", "Digital capability: the natural logarithm of one plus "
                     "the frequency of digital-technology terms in the "
                     "management discussion and analysis section of the "
                     "annual report"),
        R("Slack", "Financial slack: cash and cash equivalents divided by "
                   "total assets"),
        S("Control variables"),
        R("Size", "Natural logarithm of total assets"),
        R("Lev", "Total liabilities divided by total assets"),
        R("ROA", "Net profit divided by total assets"),
        R("Cashflow", "Net operating cash flow divided by total assets"),
        R("TobinQ", "Market value divided by the replacement cost of assets"),
        R("Top1", "Shareholding of the largest shareholder"),
        R("Indep", "Share of independent directors on the board"),
        R("Dual", "Indicator equal to one when the chair and the chief "
                  "executive are the same person"),
        R("Board", "Natural logarithm of the number of directors"),
        R("CapInt", "Natural logarithm of net fixed assets per employee"),
        R("Emp", "Natural logarithm of the number of employees"),
        S("Instrumental variables"),
        R("CityDiv", "Occupational diversity of the labor pool in the firm's "
                     "prefecture, from the census and the annual labor "
                     "statistics, standardized"),
        R("PeerVar", "Mean workforce skill variety of firms in the same "
                     "two-digit industry located outside the firm's own "
                     "province"),
        S("Placebo variable"),
        R("Exper", "Share of employees aged 31 to 50 in the firm's total "
                   "workforce (%)"),
    ]
    return dict(number=1, caption="Variable definitions and measurement.",
                header=["Variable", "Definition"], rows=rows,
                widths=[0.17, 0.83], note=None, italic_col=0, wide=False,
                align="ll")


def table2():
    hdr, rows = read("t02_descriptives.tsv")
    return dict(number=2, caption="Descriptive statistics.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.20] + [0.133] * 6, note=(
                    "The sample comprises %s firm-year observations for %s "
                    "Chinese A-share listed firms over %s. Variety, RelVar "
                    "and UnrelVar are measured in bits; the theoretical "
                    "maximum of Variety over fifteen skill cells is %.2f. All "
                    "continuous variables are winsorized at the first and "
                    "ninety-ninth percentiles.%s"
                    % ("{:,}".format(SUM["n_obs"]),
                       "{:,}".format(SUM["n_firms"]),
                       SUM["years"].replace("-", "–"),
                       SUM["max_entropy"], SRC)),
                italic_col=0, wide=False, align="l" + "c" * 6)


def table3():
    hdr, rows = read("t03_correlation.tsv")
    keep = 12
    hdr = hdr[:1 + keep] + [hdr[-1]]
    rows = [r[:1 + keep] + [r[-1]] for r in rows]
    return dict(number=3, caption="Pearson correlation coefficients and "
                                  "variance inflation factors.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.112] + [0.066] * 10 + [0.086, 0.066] + [0.069],
                note=("The lower triangle reports pairwise Pearson "
                      "correlation coefficients. The final column reports the "
                      "variance inflation factor of each regressor of the "
                      "buffering specification after the two-way within "
                      "transformation; the largest value is %.2f, below the "
                      "conventional threshold of five.%s"
                      % (SUM["vif_max"], SRC)),
                italic_col=0, wide=True, align="l" + "c" * (keep + 1),
                fs=6.0)


def table4():
    hdr, rows = read("t04_benchmark.tsv")
    return dict(number=4, caption="Workforce skill variety and the youth "
                                  "employment share.",
                header=hdr, rows=_pairs(rows, 6),
                widths=[0.22] + [0.156] * 5, note=(
                    "Column (1) includes firm fixed effects only; column (2) "
                    "adds year fixed effects; column (3) is the benchmark "
                    "specification; columns (4) and (5) replace the year "
                    "effects with industry-by-year and province-by-year "
                    "effects. " + SE_NOTE),
                italic_col=0, wide=False, align="l" + "c" * 5)


def table5():
    hdr, rows = read("t05_buffer.tsv")
    return dict(number=5, caption="The buffering of demand shocks by "
                                  "workforce skill variety.",
                header=hdr, rows=_pairs(rows, 6),
                widths=[0.24] + [0.152] * 5, note=(
                    "Shock is standardized, so its coefficient is the effect "
                    "of a one-standard-deviation adverse demand shock at a "
                    "workforce skill variety of zero; the effect at the "
                    "sample mean of Variety is reported in the text and "
                    "plotted in Figure 2. " + SE_NOTE),
                italic_col=0, wide=False, align="l" + "c" * 5)


def table6():
    hdr, rows = read("t06_decomposition.tsv")
    return dict(number=6, caption="Related and unrelated variety.",
                header=hdr, rows=_pairs(rows, 4),
                widths=[0.34, 0.22, 0.22, 0.22], note=(
                    "RelVar is the employment-weighted mean entropy of the "
                    "education distribution within occupational categories "
                    "and UnrelVar is the entropy of the distribution across "
                    "those categories, so that their sum is Variety. "
                    + SE_NOTE),
                italic_col=0, wide=False, align="lccc")


def table7():
    hdr, rows = read("t07_mechanism.tsv")
    return dict(number=7, caption="Tests of the redeployment and churn "
                                  "channels.",
                header=hdr, rows=_pairs(rows, 7),
                widths=[0.202] + [0.133] * 6, note=(
                    "The dependent variable is named in each column heading. "
                    "Redeploy is the index of dissimilarity between "
                    "successive occupational distributions and Churn is the "
                    "gross separation rate, both in percentage points. Values "
                    "in parentheses are standard errors clustered at the firm "
                    "level. ***, ** and * denote significance at the 1%, 5% "
                    "and 10% levels, respectively." + SRC),
                italic_col=0, wide=True, align="l" + "c" * 6, fs=7.2)


def table8():
    hdr, rows = read("t08_indirect.tsv")
    return dict(number=8, caption="Bootstrapped decomposition of the "
                                  "buffering effect.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.17, 0.12, 0.10, 0.09, 0.10, 0.10, 0.17, 0.15],
                note=("Path a is the coefficient on Shock x Variety in the "
                      "mediator equation and path b is the coefficient on the "
                      "mediator in an outcome equation that also contains "
                      "Shock x Variety, so their product is the part of the "
                      "buffering effect that travels through the mediator. "
                      "The confidence interval is the percentile interval of "
                      "%d bootstrap replications that resample whole firms. "
                      "***, ** and * denote significance at the 1%%, 5%% and "
                      "10%% levels, respectively.%s"
                      % (SUM["med"]["Redeploy"]["n_boot"], SRC)),
                italic_col=0, wide=True, align="l" + "c" * 7, fs=7.2)


def table9():
    hdr, rows = read("t09_endogeneity.tsv")
    return dict(number=9, caption="Endogeneity tests.",
                header=hdr, rows=_pairs(rows, 7),
                widths=[0.235] + [0.1275] * 6, note=(
                    "Columns (1) and (2) report the two first stages of the "
                    "two-stage least-squares estimation, whose dependent "
                    "variables are Variety and Shock x Variety; the remaining "
                    "columns take Youth as the dependent variable. Column (5) "
                    "uses the sample matched one to one on the propensity "
                    "score and column (6) weights the sample by "
                    "entropy-balancing weights. The null hypothesis of the "
                    "Hansen J test is that the instruments are uncorrelated "
                    "with the second-stage error; the null of the "
                    "Durbin-Wu-Hausman test is that the variety measures are "
                    "exogenous. " + SE_NOTE),
                italic_col=0, wide=True, align="l" + "c" * 6, fs=7.0)


def table10():
    hdr, rows = read("t10_robustness.tsv")
    return dict(number=10, caption="Robustness checks.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.40, 0.14, 0.11, 0.20, 0.15], note=(
                    "Each row is a separate regression that retains the full "
                    "control set and the firm and year fixed effects of the "
                    "benchmark specification. The reported coefficient is "
                    "that of the interaction between the demand shock and the "
                    "variety measure named in the first column. " + SE_NOTE),
                italic_col=0, wide=False, align="lcccc")


def table11():
    hdr, rows = read("t11_moderation.tsv")
    return dict(number=11, caption="Moderating effects of digital capability "
                                   "and financial slack.",
                header=hdr, rows=_pairs(rows, 4),
                widths=[0.40, 0.20, 0.20, 0.20], note=(
                    "Digital and Slack are standardized before the "
                    "interactions are formed. The coefficient of interest is "
                    "the triple interaction, which measures how the buffering "
                    "effect of workforce skill variety changes with the "
                    "moderator. " + SE_NOTE),
                italic_col=0, wide=False, align="lccc")


def table12():
    hdr, rows = read("t12_heterogeneity.tsv")
    return dict(number=12, caption="Heterogeneity analysis.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.24, 0.11, 0.09, 0.11, 0.09, 0.10, 0.09, 0.085,
                        0.085],
                note=("Each row reports two separate regressions run on the "
                      "subsamples named in the first column, both retaining "
                      "the full control set and the firm and year fixed "
                      "effects. The reported coefficient is that of "
                      "Shock x Variety. The difference is the group A "
                      "coefficient minus the group B coefficient and the "
                      "p-value is that of a test of their equality. "
                      + SE_NOTE),
                italic_col=0, wide=True, align="l" + "c" * 8, fs=7.0)


def table13():
    hdr, rows = read("t13_threshold.tsv")
    return dict(number=13, caption="Panel threshold estimates of the "
                                   "requisite-variety condition.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.55, 0.45], note=(
                    "The threshold variable is Variety and the slope on Shock "
                    "is allowed to differ across the two regimes it defines. "
                    "The threshold is estimated by concentrated least squares "
                    "on a grid of the trimmed empirical quantiles of Variety; "
                    "its confidence interval inverts the sequence of "
                    "likelihood ratios at the asymptotic critical value of "
                    "%.2f. The null hypothesis of the likelihood-ratio "
                    "statistic is that no threshold is present and its "
                    "p-value comes from a fixed-regressor bootstrap with %s "
                    "replications. " % (SUM["thr"]["crit"],
                                        "{:,}".format(SUM["thr"]["n_boot"]))
                    + SE_NOTE),
                italic_col=0, wide=False, align="lc")


TABLES = {"table%d" % i: fn for i, fn in enumerate(
    [table1, table2, table3, table4, table5, table6, table7, table8, table9,
     table10, table11, table12, table13], start=1)}

FIGURES = {
    "fig1": dict(number=1, file="figure1_framework.png", width_cm=13.2,
                 caption="Conceptual framework.", note=None),
    "fig2": dict(number=2, file="figure2_margins.png", width_cm=13.2,
                 caption="Marginal effect of the demand shock on the youth "
                         "employment share across workforce skill variety.",
                 note=None),
    "fig3": dict(number=3, file="figure3_threshold.png", width_cm=13.2,
                 caption="The requisite-variety threshold and the "
                         "regime-specific shock coefficients.", note=None),
}
