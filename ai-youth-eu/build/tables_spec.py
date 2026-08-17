# -*- coding: utf-8 -*-
"""Table and figure specifications.

Numeric content is read from the estimation output written by
analysis/run_all.py, so the manuscript cannot drift away from the
estimates. Tables and figures are numbered by the order in which the text
first mentions them.
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


SRC = " Source: authors' calculations."
GLM_NOTE = ("N = 27. CI = confidence interval. The two dependent variables "
            "are modelled jointly in a multivariate general linear "
            "model." + SRC)


# ---------------------------------------------------------------------------
def table1():
    rows = [
        R("AIENT", "Enterprises using at least one artificial "
          "intelligence technology", "Percentage of enterprises with 10 "
          "or more employees, 2024", "isoc_eb_ai"),
        R("GAIY", "Use of generative AI tools in the last three months, "
          "young individuals", "Percentage of individuals aged 16–29, "
          "2025", "ICT survey 2025"),
        R("DSKY", "Young people with basic or above-basic overall "
          "digital skills", "Percentage of individuals aged 16–24, "
          "2023", "isoc_sk_dskl_i21"),
        R("ICTS", "Employed ICT specialists",
          "Percentage of total employment, 2024", "isoc_sks_itspt"),
        R("NEET", "Young people neither in employment nor in education "
          "and training", "Percentage of the population aged "
          "15–29, 2024", "edat_lfse_20"),
        R("YUR", "Youth unemployment rate",
          "Percentage of the labour force aged 15–24, 2024",
          "une_rt_a"),
        R("TERT", "Tertiary educational attainment",
          "Percentage of the population aged 25–34, 2024",
          "edat_lfse_03"),
        R("GDPC", "GDP per capita in purchasing power standards",
          "Index, EU-27 = 100, 2024", "prc_ppp_ind"),
        R("RDI", "Gross domestic expenditure on R&D",
          "Percentage of GDP, 2023", "rd_e_gerdtot"),
        R("ELET", "Early leavers from education and training",
          "Percentage of the population aged 18–24, 2024",
          "edat_lfse_14"),
    ]
    return dict(number=1, caption="Variables and measures.",
                header=["Variable", "Dataset", "Measure",
                        "Eurostat Code"],
                rows=rows,
                widths=[0.11, 0.36, 0.35, 0.18],
                note=("Source: authors' design based on "
                      "[[es_ai],[es_gai],[es_dsk],[es_icts],[es_neet],"
                      "[es_yur],[es_tert],[es_gdp],[es_rd],[es_elet]]."),
                italic_col=None, wide=False, align="lllc")


def _glm_table(number, tsv, xvar, caption):
    hdr, raw = read(tsv)
    rows = []
    last_dv = None
    for r in raw:
        dv = r[0] if r[0] != last_dv else ""
        last_dv = r[0]
        rows.append(R(dv, *r[1:]))
    return dict(number=number, caption=caption,
                header=["Dependent Variable", "Parameter", "B",
                        "Std. Error", "t", "Sig.", "95% CI Lower",
                        "95% CI Upper", "Partial Eta Squared"],
                rows=rows,
                widths=[0.135, 0.125, 0.09, 0.10, 0.09, 0.085, 0.105,
                        0.105, 0.13],
                note=GLM_NOTE, italic_col=None, wide=False,
                align="lc" + "c" * 7, fs=7.5)


def table2():
    return _glm_table(2, "t02_glm_aient.tsv", "AIENT",
                      "Parameter estimates for the relationship between "
                      "enterprise adoption of artificial intelligence "
                      "and youth labour-market indicators.")


def table3():
    return _glm_table(3, "t03_glm_gaiy.tsv", "GAIY",
                      "Parameter estimates for the relationship between "
                      "generative AI use among young individuals and "
                      "youth labour-market indicators.")


def table4():
    return _glm_table(4, "t04_glm_dsky.tsv", "DSKY",
                      "Parameter estimates for the relationship between "
                      "the digital skills of young people and youth "
                      "labour-market indicators.")


def table5():
    return _glm_table(5, "t05_glm_icts.tsv", "ICTS",
                      "Parameter estimates for the relationship between "
                      "ICT specialist employment and youth labour-market "
                      "indicators.")


def table6():
    hdr, raw = read("t06_context.tsv")
    return dict(number=6,
                caption="Supplementary bivariate correlations with "
                        "structural contextual variables.",
                header=["Structural Contextual Variable", "AIENT",
                        "GAIY", "DSKY", "ICTS"],
                rows=[R(*r) for r in raw],
                widths=[0.30] + [0.175] * 4,
                note=("Pearson correlation coefficients with p-values in "
                      "parentheses; N = 27. TERT—population aged "
                      "25–34 with tertiary education; GDPC—GDP "
                      "per capita in purchasing power standards; "
                      "RDI—gross domestic expenditure on R&D as a "
                      "percentage of GDP; ELET—early leavers from "
                      "education and training." + SRC),
                italic_col=None, wide=False, align="l" + "c" * 4,
                fs=7.5)


def table7():
    hdr, raw = read("t07_efa.tsv")
    rows = []
    for r in raw:
        if r[0].startswith("SEC:"):
            rows.append(S(r[0][4:]))
            rows.append(R("Factor", r[1], r[2], r[3]))
        else:
            rows.append(R(*r))
    return dict(number=7,
                caption="Exploratory factor analysis of the artificial "
                        "intelligence readiness indicators.",
                header=["Indicator/Statistic", "Value", "", ""],
                rows=rows,
                widths=[0.40, 0.28, 0.16, 0.16],
                note=("Principal Axis Factoring on the correlation "
                      "matrix of the four AI-readiness indicators; "
                      "factor scores are generated with the regression "
                      "method." + SRC),
                italic_col=None, wide=False, align="l" + "c" * 3)


def _factreg_table(number, dv, dvname):
    f = SUM["factreg"][dv]

    def s3(x):
        return mi("%.3f" % x)

    def p3(x):
        return "0.000" if x < 0.0005 else "%.3f" % x

    rows = [
        R("1", s3(f["r"]), s3(f["r2"]), s3(f["adj_r2"]),
          "%.5f" % f["see"], ""),
        S("ANOVA"),
        R("", "Sum of Squares", "df", "Mean Square", "F", "Sig."),
        R("Regression", s3(f["ss_reg"]), "1", s3(f["ss_reg"]),
          s3(f["F"]), p3(f["F_p"])),
        R("Residual", s3(f["ss_res"]), str(f["df_res"]),
          s3(f["ss_res"] / f["df_res"]), "", ""),
        R("Total", s3(f["ss_tot"]), str(SUM["n"] - 1), "", "", ""),
        S("Coefficients"),
        R("", "B", "Std. Error", "Beta", "t", "Sig."),
        R("(Constant)", s3(f["b0"]), s3(f["se0"]), "", s3(f["t0"]),
          p3(f["p0"])),
        R("FACT_AIR", s3(f["b1"]), s3(f["se1"]), s3(f["beta"]),
          s3(f["t1"]), p3(f["p1"])),
    ]
    return dict(number=number,
                caption="Regression results for the relationship between "
                        "the latent factor of artificial intelligence "
                        "readiness and %s." % dvname,
                header=["Model", "R", "R Square", "Adjusted R-Square",
                        "Std. Error of the Estimate", ""],
                rows=rows,
                widths=[0.19, 0.17, 0.14, 0.17, 0.20, 0.13],
                note=("The dependent variable is %s; the predictor is "
                      "the regression-method factor score FACT_AIR. "
                      "N = 27." % dv + SRC),
                italic_col=None, wide=False, align="l" + "c" * 5,
                fs=8.0)


def table8():
    return _factreg_table(8, "NEET", "the youth NEET rate")


def table9():
    return _factreg_table(9, "YUR", "the youth unemployment rate")


def table10():
    hdr, raw = read("t10_anova.tsv")
    return dict(number=10,
                caption="Differences between clusters for artificial "
                        "intelligence readiness and youth labour-market "
                        "indicators (ANOVA).",
                header=["Variable", "Cluster Mean Square", "df",
                        "Error Mean Square", "df", "F", "Sig."],
                rows=[R(*r) for r in raw],
                widths=[0.14, 0.185, 0.09, 0.185, 0.09, 0.15, 0.16],
                note=("Because the clusters were formed on the same "
                      "variables, the F statistics are descriptive and "
                      "are not treated as independent hypothesis "
                      "tests." + SRC),
                italic_col=None, wide=False, align="l" + "c" * 6)


def tableA1():
    hdr, raw = read("tA1_members.tsv")
    # three country/cluster column pairs of nine rows each
    rows = []
    third = 9
    for i in range(third):
        cells = []
        for k in range(3):
            j = i + k * third
            if j < len(raw):
                cells.extend(raw[j])
            else:
                cells.extend(["", ""])
        rows.append(R(*cells))
    return dict(number="A1",
                caption="Cluster membership of the EU-27 countries.",
                header=["Country", "Cluster", "Country", "Cluster",
                        "Country", "Cluster"],
                rows=rows,
                widths=[0.21, 0.115, 0.21, 0.115, 0.23, 0.12],
                note=("Cluster 1 is the higher-adoption profile and "
                      "Cluster 2 the lower-adoption profile of the "
                      "two-cluster k-means solution." + SRC),
                italic_col=None, wide=False, align="lclclc")


TABLES = {"table%s" % k: fn for k, fn in
          [("1", table1), ("2", table2), ("3", table3), ("4", table4),
           ("5", table5), ("6", table6), ("7", table7), ("8", table8),
           ("9", table9), ("10", table10), ("A1", tableA1)]}

FIGURES = {
    "fig1": dict(number=1, file="figure1_aient.png", width_cm=13.2,
                 caption="Youth NEET rate and youth unemployment rate "
                         "according to enterprise adoption of artificial "
                         "intelligence.", note=None),
    "fig2": dict(number=2, file="figure2_gaiy.png", width_cm=13.2,
                 caption="Youth NEET rate and youth unemployment rate "
                         "according to generative AI use among young "
                         "individuals.", note=None),
    "fig3": dict(number=3, file="figure3_dsky.png", width_cm=13.2,
                 caption="Youth NEET rate and youth unemployment rate "
                         "according to the digital skills of young "
                         "people.", note=None),
    "fig4": dict(number=4, file="figure4_icts.png", width_cm=13.2,
                 caption="Youth NEET rate and youth unemployment rate "
                         "according to ICT specialist employment.",
                 note=None),
    "fig5": dict(number=5, file="figure5_dendrogram.png", width_cm=13.2,
                 caption="Dendrogram of the hierarchical clustering of "
                         "European countries based on artificial "
                         "intelligence readiness and youth labour-market "
                         "indicators.", note=None),
}
