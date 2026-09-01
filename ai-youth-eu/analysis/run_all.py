# -*- coding: utf-8 -*-
"""The full estimation pipeline for the EU-27 study.

Order of stages
---------------
1.  descriptives and the country-level correlation structure;
2.  four parallel single-predictor multivariate GLMs (MANOVA-type) of the
    two youth labour-market indicators on each AI-readiness indicator,
    with univariate parameter estimates, diagnostics (Shapiro-Wilk on
    residuals, leverage, Cook's distance) and an influential-country
    robustness re-estimation;
3.  supplementary bivariate correlations of the AI indicators with four
    structural context variables;
4.  exploratory factor analysis (Principal Axis Factoring, one factor)
    of the four AI indicators, followed by two simple regressions of the
    youth outcomes on the factor score;
5.  hierarchical clustering (Pearson proximity, average linkage) of the
    countries on the six standardized analysis variables, a two-cluster
    k-means solution, cluster ANOVA, silhouette coefficients and the
    membership listing.

Every table in the manuscript is written as a .tsv next to a summary.json
that the build scripts interpolate from, so the prose cannot drift away
from the estimates.
"""
from __future__ import annotations

import json
import os

import numpy as np
from scipy import stats as st
from scipy.cluster import hierarchy as sch

import data
import stats as tools

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
os.makedirs(TAB, exist_ok=True)

COUNTRIES, D = data.frame()
N = len(COUNTRIES)
AI_VARS = ["AIENT", "GAIY", "DSKY", "ICTS"]
DV_VARS = ["NEET", "YUR"]
CTX_VARS = ["TERT", "GDPC", "RDI", "ELET"]
CLUSTER_VARS = AI_VARS + DV_VARS

A = {k: np.array(v, float) for k, v in D.items()}
SUMMARY = {"n": N}


def w(name, header, rows):
    with open(os.path.join(TAB, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(c) for c in r) + "\n")
    print("  wrote", name)


def f3(x):
    return "%.3f" % x


def sig(p):
    return "0.000" if p < 0.0005 else "%.3f" % p


# ===========================================================================
# 1. descriptives
# ===========================================================================
desc_rows = []
for v in AI_VARS + DV_VARS + CTX_VARS:
    a = A[v]
    desc_rows.append([v, f3(a.mean()), f3(a.std(ddof=1)),
                      "%.1f" % a.min(), "%.1f" % a.max()])
w("t00_descriptives.tsv", ["Variable", "Mean", "SD", "Min", "Max"],
  desc_rows)
SUMMARY["desc"] = {v: dict(mean=float(A[v].mean()),
                           sd=float(A[v].std(ddof=1)),
                           min=float(A[v].min()), max=float(A[v].max()))
                   for v in AI_VARS + DV_VARS + CTX_VARS}

# ===========================================================================
# 2. four multivariate GLMs
# ===========================================================================
Y = np.column_stack([A[v] for v in DV_VARS])
SUMMARY["models"] = {}
for mi, xvar in enumerate(AI_VARS, start=1):
    x = A[xvar]
    res = tools.manova_single(Y, x)
    m = dict(pillai=float(res["pillai"]), wilks=float(res["wilks"]),
             F=float(res["F"]), df1=res["df1"], df2=res["df2"],
             p=float(res["p"]), uni={})
    rows = []
    for j, dv in enumerate(DV_VARS):
        o = res["uni"][j]
        lo, hi = o.ci()
        eta = o.partial_eta2()
        sw_p = float(st.shapiro(o.resid)[1])
        cooks = o.cooks()
        infl = COUNTRIES[int(np.argmax(cooks))]
        m["uni"][dv] = dict(
            b=float(o.b[1]), se=float(o.se[1]), t=float(o.t[1]),
            p=float(o.p[1]), lo=float(lo[1]), hi=float(hi[1]),
            eta2=float(eta[1]), r2=float(o.r2),
            b0=float(o.b[0]), se0=float(o.se[0]), t0=float(o.t[0]),
            p0=float(o.p[0]), lo0=float(lo[0]), hi0=float(hi[0]),
            eta20=float(eta[0]),
            shapiro_p=sw_p, cooks_max=float(cooks.max()),
            cooks_country=infl)
        rows.append([dv, "Intercept", f3(o.b[0]), f3(o.se[0]), f3(o.t[0]),
                     sig(o.p[0]), f3(lo[0]), f3(hi[0]), f3(eta[0])])
        rows.append([dv, xvar, f3(o.b[1]), f3(o.se[1]), f3(o.t[1]),
                     sig(o.p[1]), f3(lo[1]), f3(hi[1]), f3(eta[1])])
    w("t%02d_glm_%s.tsv" % (mi + 1, xvar.lower()),
      ["Dependent Variable", "Parameter", "B", "Std. Error", "t", "Sig.",
       "95% CI Lower", "95% CI Upper", "Partial Eta Squared"], rows)
    SUMMARY["models"][xvar] = m

# ---------------------------------------------------------------------------
# influential-country robustness: drop the country with the largest mean
# Cook's distance across the eight univariate fits
# ---------------------------------------------------------------------------
cook_sum = np.zeros(N)
for xvar in AI_VARS:
    res = tools.manova_single(Y, A[xvar])
    for j in range(2):
        cook_sum += res["uni"][j].cooks()
drop_i = int(np.argmax(cook_sum))
DROP = COUNTRIES[drop_i]
keep = np.arange(N) != drop_i
SUMMARY["robust"] = {"dropped": DROP, "models": {}}
Yk = Y[keep]
for xvar in AI_VARS:
    res = tools.manova_single(Yk, A[xvar][keep])
    entry = {"p_mv": float(res["p"]), "F": float(res["F"])}
    for j, dv in enumerate(DV_VARS):
        o = res["uni"][j]
        entry[dv] = dict(b=float(o.b[1]), p=float(o.p[1]))
    SUMMARY["robust"]["models"][xvar] = entry

# ===========================================================================
# 3. supplementary bivariate correlations
# ===========================================================================
rows = []
SUMMARY["ctx"] = {}
label = {"TERT": "Tertiary attainment 25-34 (TERT)",
         "GDPC": "GDP per capita in PPS (GDPC)",
         "RDI": "R&D intensity (RDI)",
         "ELET": "Early leavers from education and training (ELET)"}
for cv in CTX_VARS:
    cells = [label[cv]]
    SUMMARY["ctx"][cv] = {}
    for xvar in AI_VARS:
        r, p = tools.pearson_with_p(A[cv], A[xvar])
        ptxt = "p < 0.001" if p < 0.001 else "p = %.3f" % p
        cells.append("%.3f (%s)" % (r, ptxt))
        SUMMARY["ctx"][cv][xvar] = dict(r=r, p=p)
    rows.append(cells)
# and the outcomes with context, for the text
SUMMARY["ctx_dv"] = {}
for cv in CTX_VARS:
    SUMMARY["ctx_dv"][cv] = {}
    for dv in DV_VARS:
        r, p = tools.pearson_with_p(A[cv], A[dv])
        SUMMARY["ctx_dv"][cv][dv] = dict(r=r, p=p)
w("t06_context.tsv",
  ["Structural Contextual Variable"] + AI_VARS, rows)

# ===========================================================================
# 4. exploratory factor analysis + factor regressions
# ===========================================================================
Z_ai = np.column_stack([(A[v] - A[v].mean()) / A[v].std(ddof=1)
                        for v in AI_VARS])
R_ai = np.corrcoef(Z_ai, rowvar=False)
kmo = float(tools.kmo(R_ai))
chi2, dfb, pb = tools.bartlett(R_ai, N)
efa = tools.paf_one_factor(Z_ai)
SUMMARY["efa"] = dict(
    kmo=kmo, bartlett_chi2=float(chi2), bartlett_df=int(dfb),
    bartlett_p=float(pb), eig1=efa["eig1"],
    var_initial=efa["var_initial"], ssl=efa["ssl"],
    var_extracted=efa["var_extracted"],
    communalities={v: dict(initial=float(efa["smc"][i]),
                           extraction=float(efa["communalities"][i]),
                           loading=float(efa["loadings"][i]))
                   for i, v in enumerate(AI_VARS)},
    min_r=float(R_ai[np.triu_indices_from(R_ai, 1)].min()),
    max_r=float(R_ai[np.triu_indices_from(R_ai, 1)].max()))
rows = [["Kaiser-Meyer-Olkin measure", "%.3f" % kmo, "", ""],
        ["Bartlett's test of sphericity",
         "χ2 = %.3f; df = %d; %s" % (chi2, dfb,
                                       "p < 0.001" if pb < 0.001
                                       else "p = %.3f" % pb), "", ""],
        ["Extraction method", "Principal Axis Factoring", "", ""],
        ["Number of factors extracted", "1", "", ""],
        ["Initial eigenvalue, Factor 1", "%.3f" % efa["eig1"], "", ""],
        ["Initial variance explained", "%.3f%%" % efa["var_initial"], "", ""],
        ["Extraction sum of squared loadings", "%.3f" % efa["ssl"], "", ""],
        ["Variance explained after extraction",
         "%.3f%%" % efa["var_extracted"], "", ""],
        ["Rotation", "No rotation", "", ""],
        ["SEC:Communalities", "Initial", "Extraction", "Factor 1"]]
for i, v in enumerate(AI_VARS):
    rows.append([v, f3(efa["smc"][i]), f3(efa["communalities"][i]),
                 f3(efa["loadings"][i])])
w("t07_efa.tsv", ["Indicator/Statistic", "Value", "", ""], rows)

FACT = efa["scores"]

SUMMARY["factreg"] = {}
for ti, dv in zip((8, 9), DV_VARS):
    X = np.column_stack([np.ones(N), FACT])
    o = tools.OLS(A[dv], X)
    beta = o.beta_std()
    SUMMARY["factreg"][dv] = dict(
        r=float(np.sqrt(o.r2)), r2=float(o.r2), adj_r2=float(o.adj_r2),
        see=float(o.see), F=float(o.f), F_p=float(o.f_p),
        ss_reg=float(o.ssr), ss_res=float(o.sse), ss_tot=float(o.sst),
        df_reg=1, df_res=int(o.df),
        b0=float(o.b[0]), se0=float(o.se[0]), t0=float(o.t[0]),
        p0=float(o.p[0]),
        b1=float(o.b[1]), se1=float(o.se[1]), beta=float(beta[1]),
        t1=float(o.t[1]), p1=float(o.p[1]))
    rows = [
        ["SEC:Model summary", "", "", "", "", ""],
        ["R", f3(np.sqrt(o.r2)), "", "", "", ""],
        ["R Square", f3(o.r2), "", "", "", ""],
        ["Adjusted R Square", f3(o.adj_r2), "", "", "", ""],
        ["Std. Error of the Estimate", "%.5f" % o.see, "", "", "", ""],
        ["SEC:ANOVA", "Sum of Squares", "df", "Mean Square", "F", "Sig."],
        ["Regression", f3(o.ssr), "1", f3(o.ssr), f3(o.f), sig(o.f_p)],
        ["Residual", f3(o.sse), str(o.df), f3(o.sse / o.df), "", ""],
        ["Total", f3(o.sst), str(N - 1), "", "", ""],
        ["SEC:Coefficients", "B", "Std. Error", "Beta", "t", "Sig."],
        ["(Constant)", f3(o.b[0]), f3(o.se[0]), "", f3(o.t[0]),
         sig(o.p[0])],
        ["FACT_AIR", f3(o.b[1]), f3(o.se[1]), f3(beta[1]), f3(o.t[1]),
         sig(o.p[1])],
    ]
    w("t%02d_factreg_%s.tsv" % (ti, dv.lower()),
      ["Statistic", "V1", "V2", "V3", "V4", "V5"], rows)

# ===========================================================================
# 5. clustering
# ===========================================================================
Z6 = np.column_stack([(A[v] - A[v].mean()) / A[v].std(ddof=1)
                      for v in CLUSTER_VARS])
d = tools.pearson_distance(Z6)
Zlink = tools.average_linkage(d, N)
Zref = sch.linkage(d, method="average")
assert np.allclose(np.sort(Zlink[:, 2]), np.sort(Zref[:, 2]), atol=1e-9), \
    "average-linkage implementation disagrees with scipy"

# dendrogram geometry (country order + rescaled merge heights, SPSS style)
dg = sch.dendrogram(Zref, no_plot=True, labels=COUNTRIES)
hmax = Zref[:, 2].max()
hmin = Zref[:, 2].min()
SUMMARY["dendro_order"] = dg["ivl"]
np.save(os.path.join(TAB, "linkage.npy"), Zref)

labels_h = tools.cut_two(Zref, N)
labels_km, centers_km, _ = tools.kmeans(Z6, 2)
# align k-means labels with the hierarchical two-group cut and order the
# clusters so that Cluster 1 is the high-adoption profile
m0 = A["AIENT"][labels_km == 0].mean()
m1 = A["AIENT"][labels_km == 1].mean()
if m1 > m0:
    labels_km = 1 - labels_km
agree = float((labels_km == labels_h).mean())
agree = max(agree, 1 - agree)
SUMMARY["cluster_agreement"] = agree

centers = {}
for c in (0, 1):
    centers["cluster%d" % (c + 1)] = {
        v: float(A[v][labels_km == c].mean()) for v in CLUSTER_VARS}
    centers["cluster%d" % (c + 1)]["n"] = int((labels_km == c).sum())
SUMMARY["centers"] = centers

sil = tools.silhouette(Z6, labels_km)
SUMMARY["silhouette"] = dict(
    overall=float(sil.mean()),
    c1=float(sil[labels_km == 0].mean()),
    c2=float(sil[labels_km == 1].mean()))

rows = []
SUMMARY["anova"] = {}
for v in CLUSTER_VARS:
    an = tools.cluster_anova(A[v], labels_km)
    SUMMARY["anova"][v] = {k: float(x) for k, x in an.items()}
    rows.append([v, f3(an["ms_cluster"]), str(int(an["df_cluster"])),
                 f3(an["ms_error"]), str(int(an["df_error"])),
                 f3(an["F"]), sig(an["p"])])
w("t10_anova.tsv",
  ["Variable", "Cluster Mean Square", "df", "Error Mean Square", "df",
   "F", "Sig."], rows)

members1 = sorted(c for c, l in zip(COUNTRIES, labels_km) if l == 0)
members2 = sorted(c for c, l in zip(COUNTRIES, labels_km) if l == 1)
SUMMARY["members"] = {"cluster1": members1, "cluster2": members2}
rows = [[c, "1" if l == 0 else "2"]
        for c, l in sorted(zip(COUNTRIES, labels_km))]
w("tA1_members.tsv", ["Country", "Cluster"], rows)

# scatter/fit data for the four figures
SUMMARY["fits"] = {}
for xvar in AI_VARS:
    x = A[xvar]
    entry = {}
    for dv in DV_VARS:
        o = tools.OLS(A[dv], np.column_stack([np.ones(N), x]))
        entry[dv] = dict(b0=float(o.b[0]), b1=float(o.b[1]),
                         r2=float(o.r2))
    SUMMARY["fits"][xvar] = entry

# correlations among the AI indicators, for the text
SUMMARY["ai_corr"] = {}
for i, a in enumerate(AI_VARS):
    for b in AI_VARS[i + 1:]:
        r, p = tools.pearson_with_p(A[a], A[b])
        SUMMARY["ai_corr"]["%s_%s" % (a, b)] = dict(r=r, p=p)

with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
    json.dump(SUMMARY, fh, indent=1)
print("summary.json written; dropped country for robustness:", DROP)
