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
    "AI": "A", "UpAI": "A^{u}", "DownAI": "A^{d}", "PeerAI": "A^{p}",
    "ChainAI": "A^{c}", "WYouth": "WY", "WExper": "WX",
    "DownSpec": "A^{d}(specific)", "DownGen": "A^{d}(generic)",
    "DownNear": "A^{d}(same city)", "DownFar": "A^{d}(other city)",
    "DownBin": "A^{d}(unweighted)", "DownTop": "A^{d}(largest customer)",
    "DownAI_lag2": "A^{d}(t-2)", "DownAI_lead2": "A^{d}(t+2)",
    "DownFake": "A^{d}(rewired)",
    "Youth": "Y", "Exper": "X",
    "Size": "Size", "Lev": "Lev", "ROA": "ROA", "Growth": "Growth",
    "Cash": "Cash", "FirmAge": "Age", "TobinQ": "TobinQ", "CapInt": "CapInt",
    "Wage": "Wage", "Analyst": "Analyst", "InstOwn": "InstOwn",
    "GDPg": "GDPg", "YouthU": "YouthU",
}

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
        R("Y", "Share of employees aged 30 or below in total employees (%)"),
        R("X", "Share of employees with more than ten years of tenure (%)"),
        S("Adoption and its network lags"),
        R("A", "Generative-AI adoption: standardised logarithm of one plus the "
               "frequency of generative-AI terms in the management discussion "
               "and analysis section of the annual report"),
        R("A^{u}", "Purchase-weighted average adoption of the firm's disclosed "
                   "suppliers"),
        R("A^{d}", "Sales-weighted average adoption of the firm's disclosed "
                   "customers"),
        R("A^{p}", "Average adoption of the other listed firms headquartered "
                   "in the same city"),
        R("A^{c}", "Supply-chain lag: the average of the supplier and customer "
                   "lags, used in the network autoregressive model"),
        R("WY", "Network lag of the dependent variable: the same weighted "
                "average of the youth employment shares of the firm's "
                "supply-chain partners"),
        S("Partitions of the customer lag"),
        R("A^{d}(specific)", "Customer lag restricted to customers whose "
                             "sector buys differentiated rather than "
                             "reference-priced inputs"),
        R("A^{d}(generic)", "Customer lag restricted to the remaining "
                            "customers"),
        R("A^{d}(same city)", "Customer lag restricted to customers "
                              "headquartered in the firm's own city"),
        R("A^{d}(other city)", "Customer lag restricted to the remaining "
                               "customers"),
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
        R("GDPg", "Real growth rate of city gross domestic product (%)"),
        R("YouthU", "City surveyed unemployment rate of the population aged 16 "
                    "to 24 (%)"),
        S("Instruments"),
        R("W^{2}A, W^{3}A", "Second- and third-order network lags of adoption, "
                            "excluded from the own equation because the "
                            "network contains intransitive triads"),
        R("IV^{Own}", "Pre-sample occupational exposure of the firm's task "
                      "bundle to language models interacted with the national "
                      "generative-AI diffusion index"),
        R("IV^{u}, IV^{d}, IV^{p}", "The corresponding network lags of that "
                                    "pre-sample exposure"),
    ]
    return dict(number=1, caption="Definitions of variables.",
                header=["Variable", "Definition"], rows=rows,
                widths=[0.22, 0.78], note=None, italic_col=0, wide=False,
                align="ll")


def table2():
    hdr, rows = read("t_descriptives.tsv")
    return dict(number=2, caption="Descriptive statistics.",
                header=hdr, rows=[R(lab(r[0]), *r[1:]) for r in rows],
                widths=[0.16] + [0.105] * 8,
                note="The sample covers Chinese A-share listed firms over "
                     f"{SUM['years'].replace('-', '–')}. All continuous "
                     "variables are winsorised at the 1st and 99th "
                     "percentiles. Adoption and its network lags are "
                     "standardised over the estimation sample. Variable "
                     "definitions are given in Table 1.",
                italic_col=0, wide=True, align="l" + "c" * 8)


def table3():
    hdr, rows = read("t_correlation.tsv")
    return dict(number=3,
                caption="Pearson correlations of the main variables.",
                header=[lab(h) for h in hdr],
                rows=[R(lab(r[0]), *r[1:]) for r in rows],
                widths=[0.14] + [0.086] * 10,
                note="***, ** and * denote significance at the 1%, 5% and 10% "
                     "levels. Variance inflation factors computed after the "
                     "two-way within transformation have a maximum of "
                     f"{SUM['vif_max']:.2f} and a mean of "
                     f"{SUM['vif_mean']:.2f}.",
                italic_col=0, wide=True, align="l" + "c" * 10, fs=7.0)


TAILS = {"Firm FE", "Year FE", "Industry x year FE", "City x year FE",
         "Observations", "Within R2", "Controls", "Estimator",
         "Kleibergen-Paap rk Wald F", "Hansen J (p)", "Wu-Hausman (p)",
         "Cross-equation difference", "Direct impact", "Indirect impact",
         "Total impact", "Network multiplier", "Endogenous regressors",
         "Difference tested", "Difference"}

RENAME = {"Industry x year FE": "Industry × year FE",
          "City x year FE": "City × year FE",
          "Within R2": "Within R²",
          "Kleibergen-Paap rk Wald F": "Kleibergen–Paap rk Wald F",
          "Wu-Hausman (p)": "Wu–Hausman (p)"}


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
                widths=widths or [0.26] + [0.74 / (k - 1)] * (k - 1),
                note=note, italic_col=0, wide=wide, fs=fs,
                align="l" + "c" * (k - 1))


def table4():
    return _reg_table(
        "t_baseline.tsv", 4,
        "The within-firm benchmark: own adoption and the youth employment "
        "share.",
        "The dependent variable is the youth employment share in columns (1) "
        "to (4) and the experienced share in column (5); the model is Equation "
        "(5). The cross-equation difference is the coefficient on the "
        "interaction of adoption with an equation indicator in the stacked "
        "model of columns (2) and (5), whose covariance is clustered on the "
        "firm across both equations. " + CLUSTER_NOTE)


def table5():
    return _reg_table(
        "t_slx.tsv", 5,
        "The three transmissions: own adoption, the supply chain and the local "
        "labour market.",
        "The dependent variable is the youth employment share and the model is "
        "Equation (6). The network lags are defined in Equation (1) and are "
        "constructed from the pre-shock configuration of the disclosed "
        "supplier and customer network and of the city of headquarters. "
        + CLUSTER_NOTE)


def table6():
    return _reg_table(
        "t_sar.tsv", 6,
        "The network autoregressive model and the decomposition of impacts.",
        "The dependent variable is the youth employment share in columns (1) "
        "to (3) and the experienced share in column (4); the model is Equation "
        "(2). The endogenous network lag is instrumented with the second- and "
        "third-order network lags of adoption. The direct, indirect and total "
        "impacts are the quantities in Equation (4), with delta-method "
        "standard errors; the network multiplier is the ratio of the total to "
        "the direct impact. " + CLUSTER_NOTE,
        widths=[0.30, 0.175, 0.175, 0.175, 0.175])


def table7():
    return _reg_table(
        "t_niv.tsv", 7,
        "Endogenous adoption: instrumental-variables estimates.",
        "The dependent variable is the youth employment share. Column (1) is "
        "least squares; columns (2) to (4) instrument the adoption terms named "
        "in the row “Endogenous regressors” with shift-share terms "
        "built from pre-sample occupational exposure and with the second- and "
        "third-order network lags of adoption. " + CLUSTER_NOTE,
        widths=[0.28, 0.18, 0.18, 0.18, 0.18])


def table8():
    hdr, rows = read("t_aggregate.tsv")
    return dict(
        number=8,
        caption="The same coefficient at three levels of the system.",
        header=["Level of aggregation", "Unit", "A", "SE", "N", "Within R²"],
        rows=[R(*r) for r in rows],
        widths=[0.34, 0.17, 0.13, 0.13, 0.12, 0.11],
        note="Each row estimates Equation (5) on the unit named in the second "
             "column; the city and industry panels are employment-weighted "
             "aggregates with unit and year effects. The implied local "
             "reallocation share is one minus the ratio of the city-level to "
             "the firm-level coefficient. The system-level total impact is "
             "taken from column (2) of Table 6. " + CLUSTER_NOTE,
        italic_col=None, wide=True, align="llcccc")


def table9():
    return _reg_table(
        "t_links.tsv", 9,
        "Which links carry the shock: input specificity against geographic "
        "proximity.",
        "The dependent variable is the youth employment share in columns (1) "
        "and (2) and the experienced share in column (3). Each partition of "
        "the customer weights adds back to the full customer lag exactly, so "
        "the two components can be entered together. The difference is a Wald "
        "test that the two component coefficients are equal. " + CLUSTER_NOTE,
        widths=[0.34, 0.22, 0.22, 0.22])


def table10():
    hdr, rows = read("t_agespec.tsv")
    return dict(
        number=10,
        caption="Age specificity of every channel.",
        header=["Channel", "Youth share", "Experienced share", "Difference",
                "Ratio"],
        rows=[R(*r) for r in rows],
        widths=[0.30, 0.18, 0.20, 0.18, 0.14],
        note="Each row reports the coefficient on the channel named in the "
             "first column from Equation (6) estimated on the youth share and "
             "on the experienced share. The difference is the coefficient on "
             "the interaction of that channel with an equation indicator in "
             "the stacked model, whose covariance is clustered on the firm "
             "across both equations; the ratio is the youth coefficient "
             "divided by the experienced one. " + CLUSTER_NOTE,
        italic_col=None, wide=True, align="lcccc")


def table11():
    hdr, rows = read("t_robust.tsv")
    return dict(
        number=11, caption="Robustness checks.",
        header=["Specification", "A", "SE", "A^{d}", "SE", "N"],
        rows=[R(*r) for r in rows],
        widths=[0.40, 0.13, 0.13, 0.13, 0.13, 0.08],
        note="Each row is a separate estimation of Equation (6) with the "
             "modification named in the first column. The specification in "
             "logs uses the logarithm of the number of employees aged 30 or "
             "below and is therefore not in the units of the other rows. "
             + CLUSTER_NOTE,
        italic_col=None, wide=True, align="lccccc")


def table12():
    hdr, rows = read("t_hetero.tsv")
    return dict(
        number=12, caption="Heterogeneity analysis.",
        header=["Partition", "Subsample A", "A", "A^{d}", "Subsample B", "A",
                "A^{d}", "Difference in A^{d}"],
        rows=[R(*r) for r in rows],
        widths=[0.15, 0.13, 0.11, 0.11, 0.12, 0.11, 0.11, 0.16],
        note="Each partition re-estimates Equation (6) on the two subsamples. "
             "Network centrality is the within-firm standard deviation of the "
             "supply-chain lag, split at the median; local market thickness is "
             "the number of listed firms in the city, split at the median. The "
             "difference is the customer-lag coefficient in subsample A minus "
             "that in subsample B, with a standard error computed from the two "
             "independent estimates. " + CLUSTER_NOTE,
        italic_col=None, wide=True, align="llcclccc", fs=7.2)


def tableA1():
    hdr, rows = read("t_alt.tsv")
    return dict(
        number="A1",
        caption="Alternative network constructions and placebo tests.",
        header=["Specification", "Coefficient on", "Estimate", "SE", "N"],
        rows=[R(r[0], lab(r[1]), *r[2:]) for r in rows],
        widths=[0.40, 0.20, 0.15, 0.13, 0.12],
        note="Each row re-estimates Equation (6) with the customer lag "
             "replaced by the construction named in the first column; the "
             "coefficient reported is that on the replacement. The lead "
             "specification is a placebo, and the rewired specification "
             "reassigns customer links at random while leaving every firm's "
             "own adoption, characteristics and outcome unchanged. "
             + CLUSTER_NOTE,
        italic_col=None, wide=True, align="llccc")


TABLES = {"table1": table1, "table2": table2, "table3": table3,
          "table4": table4, "table5": table5, "table6": table6,
          "table7": table7, "table8": table8, "table9": table9,
          "table10": table10, "table11": table11, "table12": table12,
          "tableA1": tableA1}

# This manuscript reports no figures: the argument is carried entirely by the
# estimates, and every quantity a plot would show is already in a table.
FIGURES = {}
