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
    "AI": "AI", "AI2": "AI^{2}", "AIxZ": "AI × Z", "AI2xZ": "AI^{2} × Z",
    "AUG": "AUG", "AUT": "AUT", "OLC": "OLC", "AIGov": "AIGov", "LCP": "LCP",
    "Size": "Size", "Lev": "Lev", "ROE": "ROE", "Growth": "Growth",
    "Age": "Age", "Board": "Board", "Indep": "Indep", "Dual": "Dual",
    "TobinQ": "TobinQ", "Fixed": "Fixed", "Youth": "Youth",
    "Youth35": "Youth35", "LnYoung": "LnYoung",
    "IV_Bartik": "IV^{Phone}", "IV_Peer": "IV^{Peer}", "IV_Exp": "IV^{Exp}",
    "IV_Bartik2": "(IV^{Phone})^{2}", "IV_Peer2": "(IV^{Peer})^{2}",
    "IV_Exp2": "(IV^{Exp})^{2}",
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


# ---------------------------------------------------------------------------
def table1():
    rows = [
        S("Dependent variables"),
        R("Youth", "Share of employees aged 30 or below in total employees (%)"),
        R("Youth35", "Share of employees aged 35 or below in total employees (%)"),
        R("LnYoung", "Natural logarithm of one plus the number of employees "
                     "aged 30 or below"),
        S("Explanatory variable"),
        R("AI", "Depth of generative AI adoption: the natural logarithm of one "
                "plus the frequency of generative-AI terms in the management "
                "discussion and analysis section of the annual report"),
        R("AI^{2}", "Square of the adoption depth"),
        S("Channel variables"),
        R("AUG", "Augmentation: share of entry-level positions in which model "
                 "assistance is reported (%)"),
        R("AUT", "Automation: share of the entry-level routine-cognitive task "
                 "bundle executed with no human step (%)"),
        S("Moderating variables"),
        R("OLC", "Organisational learning capability: standardised pre-shock "
                 "employee training and development expenditure per employee"),
        R("AIGov", "Indicator equal to one if the annual report discloses AI or "
                   "algorithmic governance arrangements"),
        R("LCP", "Labour cost pressure: standardised ratio of cash paid to and "
                 "on behalf of employees to operating revenue"),
        S("Control variables"),
        R("Size", "Natural logarithm of total assets"),
        R("Lev", "Total liabilities divided by total assets"),
        R("ROE", "Net profit divided by total shareholders' equity"),
        R("Growth", "Year-on-year growth rate of operating revenue"),
        R("Age", "Natural logarithm of one plus the number of years since the "
                 "firm was founded"),
        R("Board", "Natural logarithm of the number of directors"),
        R("Indep", "Number of independent directors divided by board size"),
        R("Dual", "Indicator equal to one if the CEO also chairs the board"),
        R("TobinQ", "Market value divided by the replacement cost of assets"),
        R("Fixed", "Net fixed assets divided by total assets"),
        S("Instruments"),
        R("IV^{Phone}", "1984 provincial fixed-line telephone penetration rate "
                        "interacted with the national generative-AI diffusion "
                        "index, rebased to unity in every pre-shock year"),
        R("IV^{Exp}", "Pre-shock task exposure of the firm's professional "
                      "composition interacted with the same index"),
        R("IV^{Peer}", "Leave-one-out mean adoption depth of other firms in the "
                       "same industry and province"),
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
    return dict(number=3, caption="Pearson correlations of the main variables.",
                header=[lab(h) for h in hdr],
                rows=[R(lab(r[0]), *r[1:]) for r in rows],
                widths=[0.14] + [0.0956] * 9,
                note="***, ** and * denote significance at the 1%, 5% and 10% "
                     "levels. Excluding the mechanical correlation between "
                     "adoption depth and its own square, variance inflation "
                     f"factors have a maximum of {SUM['vif_max']:.2f} and a "
                     f"mean of {SUM['vif_mean']:.2f}.",
                italic_col=0, wide=True, align="l" + "c" * 9)


def _reg_table(fname, number, caption, note, widths=None, wide=True,
               header=None, fs=None):
    hdr, rows = read(fname)
    out = []
    for r in rows:
        first = r[0].strip()
        if first in ("Firm FE", "Year FE", "Industry x year FE",
                     "Province x year FE", "Observations", "Within R2",
                     "Controls", "Dependent variable",
                     "Kleibergen-Paap rk Wald F", "Hansen J (p)",
                     "Wu-Hausman (p)"):
            nm = {"Industry x year FE": "Industry × year FE",
                  "Province x year FE": "Province × year FE",
                  "Within R2": "Within R²",
                  "Kleibergen-Paap rk Wald F": "Kleibergen–Paap rk Wald F",
                  "Hansen J (p)": "Hansen J (p)",
                  "Wu-Hausman (p)": "Wu–Hausman (p)"}.get(first, first)
            out.append(R(nm, *[lab(x) for x in r[1:]]))
        else:
            out.append(R(lab(first), *r[1:]))
    k = len(hdr)
    return dict(number=number, caption=caption, header=header or hdr, rows=out,
                widths=widths or [0.22] + [0.78 / (k - 1)] * (k - 1),
                note=note, italic_col=0, wide=wide, fs=fs,
                align="l" + "c" * (k - 1))


def table4():
    return _reg_table(
        "t_baseline.tsv", 4,
        "Baseline regressions: adoption depth and the youth employment share.",
        "The dependent variable is the share of employees aged 30 or below. "
        "Columns (1) and (2) estimate the linear specification of Equation (2) "
        "and columns (3) to (6) the quadratic specification of Equation (3). "
        "Standard errors clustered at the firm level are in parentheses. "
        "***, ** and * denote significance at the 1%, 5% and 10% levels.")


def table5():
    hdr, rows = read("t_utest.tsv")
    return dict(number=5,
                caption="Testing the shape of the relationship.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.62, 0.38],
                note="The Lind–Mehlum test is the exact test of a U or "
                     "inverted-U shape over a specified interval; its composite "
                     "null is that the relationship is monotone. The Fieller "
                     "interval for the extreme point does not require the "
                     "squared term to be far from zero. The two-lines test "
                     "fits a separate slope on each side of the extreme point.",
                italic_col=None, wide=False, align="lc")


def table6():
    return _reg_table(
        "t_mechanism.tsv", 6,
        "Mechanism: augmentation is concave, automation is convex.",
        "Columns (1) and (2) regress each channel on adoption depth and its "
        "square; column (3) adds both channels to the outcome equation. "
        "Standard errors clustered at the firm level are in parentheses. "
        "***, ** and * denote significance at the 1%, 5% and 10% levels.",
        widths=[0.34, 0.22, 0.22, 0.22])


def table7():
    hdr, rows = read("t_robustness.tsv")
    return dict(number=7, caption="Robustness checks.",
                header=[lab(h) for h in hdr],
                rows=[R(lab(r[0]), *r[1:]) for r in rows],
                widths=[0.30, 0.115, 0.095, 0.115, 0.095, 0.12, 0.09, 0.07],
                note="Each row re-estimates Equation (3) with the modification "
                     "described and reports the two coefficients, the extreme "
                     "point and the Lind–Mehlum statistic. Standard errors are "
                     "clustered at the firm level except in row (4). ***, ** "
                     "and * denote significance at the 1%, 5% and 10% levels.",
                italic_col=None, wide=True, fs=7.4, align="lccccccc")


def table8():
    return _reg_table(
        "t_endogeneity.tsv", 8,
        "Endogeneity: instrumental variables, propensity-score matching and "
        "entropy balancing.",
        "Columns (1) and (2) are the two first stages of the two-stage "
        "least-squares estimation and column (3) the second stage. Column (4) "
        "estimates Equation (3) on the 1:1 nearest-neighbour matched sample "
        "with a caliper of 0.02, and column (5) reweights the comparison group "
        "by entropy balancing on the first two moments of the covariates. "
        "Standard errors clustered at the firm level are in parentheses. "
        "***, ** and * denote significance at the 1%, 5% and 10% levels.",
        widths=[0.26, 0.148, 0.148, 0.148, 0.148, 0.148], fs=7.6)


def table9():
    hdr, rows = read("t_oster.tsv")
    return dict(number=9,
                caption="Bounding the scope for selection on unobservables.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.68, 0.32],
                note="Both regressions are estimated on two-way demeaned data "
                     "with the squared term retained in each, so that the "
                     "R-squared is monotone in the set of controls. The "
                     "relative degree of selection is the ratio of selection on "
                     "unobservables to selection on observables that would be "
                     "required to drive the coefficient to zero; an absolute "
                     "value above one is conventionally read as evidence that "
                     "the result is not driven by unobserved selection.",
                italic_col=None, wide=False, align="lc")


def table10():
    return _reg_table(
        "t_moderation.tsv", 10,
        "Moderating roles of organisational learning capability, AI governance "
        "and labour cost pressure.",
        "Z denotes the moderator named in the column heading. OLC is measured "
        "before the shock and is time invariant, so it is absorbed by the firm "
        "fixed effects and enters only through its interactions. Standard "
        "errors clustered at the firm level are in parentheses. ***, ** and * "
        "denote significance at the 1%, 5% and 10% levels.",
        widths=[0.31, 0.23, 0.23, 0.23])


def table11():
    hdr, rows = read("t_turning.tsv")
    return dict(number=11,
                caption="Extreme points and their displacement across the "
                        "three moderators.",
                header=["Moderator", "Level", "Extreme point", "SE",
                        "Curvature", "Displacement", "SE"],
                rows=[R(lab(r[0]), *r[1:]) for r in rows],
                widths=[0.16, 0.20, 0.14, 0.10, 0.13, 0.16, 0.11],
                note="The extreme point is evaluated from Equation (7) at the "
                     "level of the moderator shown; the displacement is "
                     "Equation (8), the change in the extreme point per unit of "
                     "the moderator evaluated at its mean, with a delta-method "
                     "standard error. Curvature is the coefficient on the "
                     "squared term at that level of the moderator. ***, ** and "
                     "* denote significance at the 1%, 5% and 10% levels.",
                italic_col=None, wide=True, align="llccccc")


def table12():
    hdr, rows = read("t_heterogeneity.tsv")
    return dict(number=12, caption="Heterogeneity analysis.",
                header=["Split", "Group 1", "AI^{2}", "Extreme point", "N",
                        "Group 2", "AI^{2}", "Extreme point", "N", "p"],
                rows=[R(*r) for r in rows],
                widths=[0.125, 0.130, 0.100, 0.105, 0.075, 0.135, 0.100,
                        0.105, 0.075, 0.050], fs=7.4,
                note="Each row estimates Equation (3) separately in the two "
                     "subsamples. The p-value tests the equality of the "
                     "coefficient on the squared term across the two groups. "
                     "Firm size is split at the median of total assets. ***, ** "
                     "and * denote significance at the 1%, 5% and 10% levels.",
                italic_col=None, wide=True, align="ll" + "c" * 8)


def tableA1():
    hdr, rows = read("t_balance.tsv")
    return dict(number="A1",
                caption="Covariate balance before and after propensity-score "
                        "matching.",
                header=hdr, rows=[R(lab(r[0]), *r[1:]) for r in rows],
                widths=[0.22, 0.26, 0.26, 0.13, 0.13],
                note="Standardised bias is the difference in means between the "
                     "deeply and less deeply adopting groups divided by the "
                     "square root of the average of their variances, expressed "
                     "in per cent. An absolute value below ten is the "
                     "conventional criterion for adequate balance. The t-test "
                     "is on the matched sample.",
                italic_col=0, wide=True, align="lcccc")


TABLES = {"table1": table1, "table2": table2, "table3": table3,
          "table4": table4, "table5": table5, "table6": table6,
          "table7": table7, "table8": table8, "table9": table9,
          "table10": table10, "table11": table11, "table12": table12,
          "tableA1": tableA1}


# ---------------------------------------------------------------------------
# Figures are numbered by order of first mention in the text and carry no
# notes: what the reader needs to know is stated in the body.
FIGURES = {
    "figure1": dict(
        number=1, file="figure1_trends.png", width_cm=13.8,
        caption="Generative AI adoption depth and the youth employment share "
                "of Chinese listed firms, 2016\u20132025.", note=None),
    "figure2": dict(
        number=2, file="figure2_curve.png", width_cm=13.8,
        caption="The inverted U-shaped relationship between adoption depth and "
                "the youth employment share.", note=None),
    "figure3": dict(
        number=3, file="figure3_channels.png", width_cm=13.8,
        caption="Decomposition of the curve into the augmentation and "
                "automation channels.", note=None),
    "figure4": dict(
        number=4, file="figure4_placebo.png", width_cm=13.8,
        caption="Randomisation distribution of the Lind\u2013Mehlum statistic.",
        note=None),
    "figure5": dict(
        number=5, file="figure5_moderators.png", width_cm=13.8,
        caption="The curve at low and high levels of each moderator.",
        note=None),
}
