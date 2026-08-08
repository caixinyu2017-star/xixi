# -*- coding: utf-8 -*-
"""Table and figure specifications.

Numeric content is read from the estimation output written by
analysis/run_all.py, so the manuscript cannot drift away from the estimates.
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


SRC = " Source: authors' own calculations."
STARS = ("***, ** and * denote significance at the 1%, 5% and 10% levels, "
         "respectively.")
SE_HC3 = ("Values in parentheses are heteroskedasticity-consistent (HC3) "
          "standard errors. ")


# ---------------------------------------------------------------------------
def table1():
    hdr, rows = read("t01_sample.tsv")
    return dict(number=1, caption="Sample profile and attrition analysis.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.34, 0.20, 0.20, 0.16, 0.10],
                note=("Continuous characteristics are means; binary "
                      "characteristics are percentages. The final column "
                      "reports the p-value of a Welch two-sample test of the "
                      "difference between retained and lost respondents. "
                      "Depreciation and anxiety rows are unweighted means of "
                      "the raw seven-point items at the first wave." + SRC),
                italic_col=None, wide=False, align="l" + "c" * 4)


def table2():
    hdr, rows = read("t02_measurement.tsv")
    return dict(number=2,
                caption="Constructs, items, and convergent validity.",
                header=["Construct and items", "Standardized loading",
                        "Cronbach's α", "CR", "AVE"],
                rows=[R(*r) for r in rows],
                widths=[0.40, 0.17, 0.15, 0.13, 0.15],
                note=("Maximum-likelihood confirmatory factor analysis on "
                      "the matched sample (N = %s). Model fit: χ2(%d) = "
                      "%.2f, CFI = %.3f, TLI = %.3f, RMSEA = %.3f, SRMR = "
                      "%.3f. CR is composite reliability; AVE is average "
                      "variance extracted. All loadings are significant at "
                      "the 1%% level.%s"
                      % ("{:,}".format(SUM["n_t2"]), SUM["cfa"]["df"],
                         SUM["cfa"]["chi2"], SUM["cfa"]["cfi"],
                         SUM["cfa"]["tli"], SUM["cfa"]["rmsea"],
                         SUM["cfa"]["srmr"], SRC)),
                italic_col=None, wide=False, align="l" + "c" * 4)


def table3():
    hdr, rows = read("t03_validity.tsv")
    return dict(number=3, caption="Discriminant validity.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.16] + [0.14] * 6,
                note=("Diagonal (bold position): square root of the average "
                      "variance extracted. Below the diagonal: latent "
                      "correlations from the confirmatory model. Above the "
                      "diagonal: heterotrait–monotrait ratios. The "
                      "Fornell–Larcker criterion and the HTMT < 0.85 "
                      "criterion are both satisfied for every pair." + SRC),
                italic_col=0, wide=False, align="l" + "c" * 6)


def table4():
    hdr, rows = read("t05_invariance_cmb.tsv")
    return dict(number=4,
                caption="Measurement invariance and common-method "
                        "diagnostics.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.40, 0.14, 0.08, 0.12, 0.15, 0.11],
                note=("Configural and metric two-group models estimated by "
                      "maximum likelihood; the metric model constrains "
                      "loadings to equality across groups. The Harman row "
                      "reports the share of item variance carried by the "
                      "first principal component; the method-factor row "
                      "reports the variance share of an equal-loading "
                      "unmeasured method factor added to the measurement "
                      "model." + SRC),
                italic_col=None, wide=False, align="l" + "c" * 5)


def table5():
    hdr, rows = read("t04_correlations.tsv")
    return dict(number=5,
                caption="Descriptive statistics and correlations of the "
                        "factor scores.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.13, 0.10, 0.08] + [0.098] * 7,
                note=("Bartlett factor scores, standardized; EXPO is the "
                      "standardized occupational exposure score. Lower "
                      "triangle: Pearson correlations (N = %s). "
                      "Correlations of magnitude 0.07 or larger are "
                      "significant at the 5%% level.%s"
                      % ("{:,}".format(SUM["n_t2"]), SRC)),
                italic_col=0, wide=False, align="l" + "c" * 9)


def _regnote(dep):
    return ("The dependent variable is %s, standardized. All models include "
            "the full control set (gender, age, degree level, STEM major, "
            "city tier, months since graduation, employment status, "
            "parental tertiary education, internship experience). "
            % dep + SE_HC3 + STARS + SRC)


def table6():
    hdr, rows = read("t06_anxiety.tsv")
    return dict(number=6,
                caption="First stage: perceived depreciation into career "
                        "anxiety (H1, H6).",
                header=["", "(1)", "(2)", "(3)", "(4)", "(5)"],
                rows=[R(*r) for r in rows],
                widths=[0.25] + [0.15] * 5,
                note=("The dependent variable is AI-related career anxiety, "
                      "standardized. Column (1) omits controls; columns "
                      "(2)–(4) add controls, support, and the interaction "
                      "on the matched sample; column (5) repeats column (4) "
                      "on the full first-wave sample. " + SE_HC3 + STARS
                      + SRC),
                italic_col=None, wide=False, align="l" + "c" * 5)


def table7():
    hdr, rows = read("t07_adaptation.tsv")
    return dict(number=7,
                caption="Second stage: the curvilinear conversion of "
                        "anxiety into adaptation (H2, H5a).",
                header=["", "(1)", "(2)", "(3)", "(4)", "(5)"],
                rows=[R(*r) for r in rows],
                widths=[0.25] + [0.15] * 5,
                note=("The dependent variable is occupational adaptation at "
                      "the second wave, standardized. Columns (1)–(4) use "
                      "HC3 standard errors; column (5) repeats column (4) "
                      "with standard errors clustered on the 20 occupation "
                      "groups. " + STARS + SRC),
                italic_col=None, wide=False, align="l" + "c" * 5)


def table8():
    hdr, rows = read("t08_utest.tsv")
    return dict(number=8,
                caption="Formal validation of the inverted U.",
                header=["Quantity", "Estimate"],
                rows=[R(*r) for r in rows],
                widths=[0.62, 0.38],
                note=("Slopes and tests follow Lind and Mehlum's composite "
                      "procedure on the full specification of Table 7, "
                      "column (4); the turning point interval is a Fieller "
                      "construction, and the literacy-conditional turning "
                      "points come from the specification that adds the "
                      "quadratic-by-literacy term." + SRC),
                italic_col=None, wide=False, align="lc")


def table9():
    hdr, rows = read("t09_avoidance.tsv")
    return dict(number=9,
                caption="The avoidance channel (H3, H5b).",
                header=["", "(1)", "(2)", "(3)", "(4)", "(5)"],
                rows=[R(*r) for r in rows],
                widths=[0.25] + [0.15] * 5,
                note=("The dependent variable is career avoidance at the "
                      "second wave, standardized. Column (2) adds the "
                      "quadratic term, which is insignificant; columns "
                      "(3)–(4) add literacy and its interaction; column (5) "
                      "clusters standard errors on occupation groups. "
                      + SE_HC3 + STARS + SRC),
                italic_col=None, wide=False, align="l" + "c" * 5)


def table10():
    hdr, rows = read("t10_process.tsv")
    return dict(number=10,
                caption="Conditional indirect effects of perceived "
                        "depreciation, through anxiety (H4a, H4b).",
                header=["Path and conditioning values", "Estimate",
                        "95% bootstrap CI"],
                rows=[R(*r) for r in rows],
                widths=[0.46, 0.22, 0.32],
                note=("Instantaneous indirect effects ω(m, w, l) of "
                      "Equation (5), with SUP, ANX and LIT set to the "
                      "stated values in standard deviations. Confidence "
                      "intervals are percentile intervals from 5,000 "
                      "bootstrap resamples of individuals; the seed is "
                      "fixed in the released code. IMM denotes an index of "
                      "moderated mediation." + SRC),
                italic_col=None, wide=False, align="lcc")


def table11():
    hdr, rows = read("t11_heterogeneity.tsv")
    return dict(number=11,
                caption="Subsample estimates: the mechanism across the "
                        "cohort.",
                header=hdr, rows=[R(*r) for r in rows],
                widths=[0.28, 0.14, 0.22, 0.14, 0.22],
                note=("Each pair of rows re-estimates the full adaptation "
                      "model within the stated subsample; the third column "
                      "is the marginal effect of anxiety at the sample "
                      "mean, the final column the subsample quadratic "
                      "coefficient. Difference rows report a two-sample "
                      "z-test of the marginal effects. " + STARS + SRC),
                italic_col=None, wide=False, align="l" + "c" * 4)


def table12():
    hdr, rows = read("t12_robustness.tsv")
    return dict(number=12, caption="Robustness of the curvilinear second "
                                   "stage.",
                header=["Specification", "ANX", "(SE)", "ANX²", "(SE)", "N"],
                rows=[R(*r) for r in rows],
                widths=[0.40, 0.12, 0.12, 0.12, 0.12, 0.12],
                note=("Each row replicates the full adaptation "
                      "specification under the stated change. Row (2) "
                      "weights by inverse retention probabilities from a "
                      "first-wave linear probability model; row (6) reports "
                      "the wild-cluster bootstrap p-value for the quadratic "
                      "term with Rademacher weights and the null imposed, "
                      "999 replications. " + STARS + SRC),
                italic_col=None, wide=False, align="l" + "c" * 5)


def table13():
    hdr_a, rows_a = read("t13_calibration.tsv")
    hdr_b, rows_b = read("t13b_necessity.tsv")
    rows = [S("Panel A: calibration anchors (raw score at membership "
              "0.95 / 0.50 / 0.05)")]
    rows += [R(*r) for r in rows_a]
    rows.append(S("Panel B: necessity analysis for high adaptation"))
    rows.append(R("Condition", "Consistency", "Coverage", ""))
    rows += [R(r[0], r[1], r[2], "") for r in rows_b]
    return dict(number=13,
                caption="Fuzzy-set calibration and necessity analysis.",
                header=["Condition", "Full (0.95)", "Crossover (0.50)",
                        "Out (0.05)"],
                rows=rows,
                widths=[0.34, 0.22, 0.22, 0.22],
                note=("Direct-method calibration with anchors at the 95th, "
                      "50th and 5th sample percentiles of each standardized "
                      "score. ~ denotes negation. No consistency reaches "
                      "the 0.90 threshold conventionally required of a "
                      "necessary condition." + SRC),
                italic_col=None, wide=False, align="l" + "c" * 3)


def table14():
    hdr, rows = read("t14_configurations.tsv")
    return dict(number=14,
                caption="Sufficient configuration for high occupational "
                        "adaptation.",
                header=["", "PHCD", "ANX", "LIT", "SUP", "EXPO",
                        "Consistency", "Raw cov.", "Unique cov."],
                rows=[R(*r) for r in rows],
                widths=[0.16] + [0.084] * 5 + [0.14, 0.12, 0.16],
                note=("● indicates the presence of a condition and ⊗ its "
                      "absence; a blank cell means the condition is "
                      "irrelevant to the configuration. All marked "
                      "conditions are core: the parsimonious and "
                      "intermediate solutions coincide. Truth-table "
                      "thresholds: frequency ≥ 10 cases, raw consistency "
                      "≥ 0.80, PRI ≥ 0.70. No configuration passes the "
                      "same thresholds for the negation of adaptation."
                      + SRC),
                italic_col=None, wide=False, align="l" + "c" * 8)


TABLES = {"table%d" % i: fn for i, fn in enumerate(
    [table1, table2, table3, table4, table5, table6, table7, table8, table9,
     table10, table11, table12, table13, table14], start=1)}

FIGURES = {
    "fig1": dict(number=1, file="figure1_dual.png", width_cm=13.2,
                 caption="The dual response to AI-related career anxiety: "
                         "(a) occupational adaptation; (b) career "
                         "avoidance.", note=None),
    "fig2": dict(number=2, file="figure2_boundaries.png", width_cm=13.2,
                 caption="Boundary conditions of the control loop: (a) the "
                         "adaptation response at low and high generative-AI "
                         "literacy; (b) the first stage across employability "
                         "support.", note=None),
    "fig3": dict(number=3, file="figure3_generality.png", width_cm=13.2,
                 caption="Generality and sufficiency: (a) the marginal "
                         "effect of anxiety on adaptation by subsample; "
                         "(b) case-level sufficiency of the single "
                         "configuration.", note=None),
}
