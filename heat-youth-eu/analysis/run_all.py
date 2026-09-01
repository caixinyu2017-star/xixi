# -*- coding: utf-8 -*-
"""The full estimation pipeline for the heat-youth panel paper.

Stages: descriptive statistics; Pearson correlations; panel diagnostics
(IPS-type unit roots, Pesaran CD); the baseline two-step System GMM of
the NEET rate; the sensitivity estimation with the youth unemployment
rate as the dependent variable; the pre-pandemic (2010-2019) robustness
estimation; the marginal-effect profile of heat across the green
endowment; and the series behind the two descriptive figures. Every
table is a .tsv, and summary.json carries every number the manuscript
interpolates.
"""
from __future__ import annotations

import json
import os

import numpy as np
from scipy import stats as st

import data
import gmm

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
os.makedirs(TAB, exist_ok=True)

rows, D = data.frame()
COUNTRIES = sorted(data.COUNTRIES)
N, T = len(COUNTRIES), data.T
YEARS = data.YEARS

# (N, T) grids
def grid(var):
    out = np.zeros((N, T))
    for (c, y, *vals), _ in zip(rows, rows):
        pass
    idx = {c: i for i, c in enumerate(COUNTRIES)}
    ydx = {y: j for j, y in enumerate(YEARS)}
    col = data.HEADER.index(var)
    for r in rows:
        out[idx[r[0]], ydx[r[1]]] = float(r[col])
    return out

NEET = grid("NEET")
YUR = grid("YUR")
CDD = grid("CDD")
GDPG = grid("GDPG")
TERT = grid("TERT")
GRN = np.array([data.COUNTRIES[c][7] for c in COUNTRIES], float)

CDD100 = CDD / 100.0
INT = CDD100 * GRN[:, None]
X = np.stack([CDD100, INT, GDPG, TERT], axis=2)      # (N, T, K)


def demean(A):
    """Deviations from period means, removing the common period effects
    (the euro-area cycle, the pandemic, and the common component of
    European summer warming) prior to estimation."""
    return A - A.mean(axis=0, keepdims=True)


NEETd = demean(NEET)
YURd = demean(YUR)
Xd = np.stack([demean(X[:, :, k]) for k in range(X.shape[2])], axis=2)

S = {"n_countries": N, "n_years": T, "n_obs": N * T,
     "period": "2010-2024"}


def w(name, header, tab_rows):
    with open(os.path.join(TAB, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in tab_rows:
            fh.write("\t".join(str(c) for c in r) + "\n")
    print("  wrote", name)


def f(x, d=3):
    return ("%%.%df" % d) % x


def sig(p):
    return "0.000" if p < 0.0005 else f(p)


# ===========================================================================
# descriptive statistics
# ===========================================================================
VARS = [("NEET", NEET.ravel()), ("YUR", YUR.ravel()),
        ("CDD", CDD.ravel()), ("GRN", np.repeat(GRN, T)),
        ("GDPG", GDPG.ravel()), ("TERT", TERT.ravel())]
t2 = []
S["desc"] = {}
for name, v in VARS:
    t2.append([name, f(v.mean(), 2), f(v.std(ddof=1), 2),
               f(v.min(), 2), f(v.max(), 2), str(v.size)])
    S["desc"][name] = dict(mean=float(v.mean()), sd=float(v.std(ddof=1)),
                           min=float(v.min()), max=float(v.max()))
w("t02_descriptives.tsv",
  ["Variable", "Mean", "Std. Dev.", "Minimum", "Maximum",
   "Observations"], t2)

# ===========================================================================
# correlations
# ===========================================================================
M = np.column_stack([NEET.ravel(), CDD100.ravel(), np.repeat(GRN, T),
                     GDPG.ravel(), TERT.ravel()])
NAMES = ["NEET", "CDD100", "GRN", "GDPG", "TERT"]
R = np.corrcoef(M, rowvar=False)
t3 = []
for i, nm in enumerate(NAMES):
    t3.append([nm] + [f(R[i, j]) if j <= i else f(R[i, j])
                      for j in range(len(NAMES))])
w("t03_correlations.tsv", ["Variable"] + NAMES, t3)
S["corr"] = {"%s_%s" % (NAMES[i], NAMES[j]): float(R[i, j])
             for i in range(len(NAMES)) for j in range(len(NAMES)) if i < j}

# ===========================================================================
# panel diagnostics
# ===========================================================================
S["ips"] = {}
for nm, Yv in (("NEET", NEET), ("CDD100", CDD100), ("GDPG", GDPG),
               ("TERT", TERT)):
    tbar, zst, p = gmm.ips_test(Yv)
    dbar, dz, dp = gmm.ips_test(np.diff(Yv, axis=1))
    S["ips"][nm] = dict(tbar=tbar, z=zst, p=p, d_z=dz, d_p=dp)
cd, cdp = gmm.pesaran_cd(NEET)
S["cd"] = dict(stat=cd, p=cdp)

# ===========================================================================
# baseline System GMM: NEET
# ===========================================================================
LBL = ["L.NEET", "CDD100", "CDD100 × GRN", "GDPG", "TERT",
       "Constant"]
SHOW = LBL[:-1]                     # the constant is not tabulated


def interp(b, p):
    d = "positive" if b > 0 else "negative"
    if p < 0.01 or p < 0.05:
        s = "significant"
    elif p < 0.10:
        s = "weakly significant"
    else:
        s = "not significant"
    return "%s, %s" % (d, s)


def run_model(Y, X, key, years_mask=None):
    Yv, Xv = Y, X
    if years_mask is not None:
        Yv, Xv = Y[:, years_mask], X[:, years_mask, :]
        Yv = Yv - Yv.mean(axis=0, keepdims=True)
        Xv = np.stack([Xv[:, :, k] - Xv[:, :, k].mean(axis=0,
                                                      keepdims=True)
                       for k in range(Xv.shape[2])], axis=2)
    m = gmm.SystemGMM(Yv, Xv, dummies=False)
    entry = dict(
        coef={LBL[j]: float(m.theta[j]) for j in range(len(LBL))},
        se={LBL[j]: float(m.se[j]) for j in range(len(LBL))},
        z={LBL[j]: float(m.z[j]) for j in range(len(LBL))},
        p={LBL[j]: float(m.p[j]) for j in range(len(LBL))},
        ar1_p=m.ar1_p, ar2_p=m.ar2_p, hansen_j=m.hansen_j,
        hansen_df=m.hansen_df, hansen_p=m.hansen_p,
        instruments=int(m.n_instruments), groups=N)
    S[key] = entry
    return m, entry


m_base, e_base = run_model(NEETd, Xd, "base")
t4 = [[LBL[j], f(m_base.theta[j]), sig(m_base.p[j]),
       interp(m_base.theta[j], m_base.p[j])] for j in range(len(SHOW))]
w("t04_gmm_neet.tsv",
  ["Variable", "Coefficient", "p-Value", "Interpretation"], t4)

t5 = [["AR(1) p-value", sig(m_base.ar1_p)],
      ["AR(2) p-value", sig(m_base.ar2_p)],
      ["Hansen p-value", sig(m_base.hansen_p)],
      ["Instruments", str(m_base.n_instruments)],
      ["Number of countries/groups", str(N)]]
w("t05_diagnostics.tsv", ["Test", "Value"], t5)

# ===========================================================================
# sensitivity: youth unemployment rate as the dependent variable
# ===========================================================================
m_yur, e_yur = run_model(YURd, Xd, "yur")
LBLY = ["L.YUR"] + LBL[1:]


def full_table(m, labels):
    out = []
    for j, lb in enumerate(labels[:-1]):
        out.append([lb, "%.4f" % m.theta[j], "%.4f" % m.se[j],
                    "%.4f" % m.z[j], "%.4f" % m.p[j]])
    out.append(["SEC:Diagnostic Test", "Value", "", "", ""])
    out.append(["Arellano–Bond AR(1), p-value", "%.4f" % m.ar1_p,
                "", "", ""])
    out.append(["Arellano–Bond AR(2), p-value", "%.4f" % m.ar2_p,
                "", "", ""])
    out.append(["Hansen test, p-value", "%.4f" % m.hansen_p, "", "", ""])
    out.append(["Number of instruments", str(m.n_instruments),
                "", "", ""])
    out.append(["Number of countries/groups", str(N), "", "", ""])
    return out


w("t06_yur.tsv",
  ["Variable", "Coefficient", "Std. Error", "z-Statistic", "p-Value"],
  full_table(m_yur, LBLY))

# ===========================================================================
# robustness: pre-pandemic subsample 2010-2019
# ===========================================================================
mask = np.array([y <= 2019 for y in YEARS])
m_pre, e_pre = run_model(NEET, X, "pre", years_mask=mask)
w("t07_prepandemic.tsv",
  ["Variable", "Coefficient", "Std. Error", "z-Statistic", "p-Value"],
  full_table(m_pre, LBL))

# ===========================================================================
# marginal effect of heat across the green endowment
# ===========================================================================
gr = np.arange(12.0, 45.0 + 0.1, 0.5)
b1, b2 = m_base.theta[1], m_base.theta[2]
V = m_base.vcov
me = b1 + b2 * gr
sev = np.sqrt(V[1, 1] + gr ** 2 * V[2, 2] + 2 * gr * V[1, 2])
S["margins"] = [dict(grn=float(g), me=float(a), se=float(s))
                for g, a, s in zip(gr, me, sev)]
# the endowment at which the heat effect ceases to differ from zero
zcrit = 1.96
sig_mask = me - zcrit * sev > 0
S["me_cutoff"] = float(gr[sig_mask][-1]) if sig_mask.any() else None
S["me_at"] = {str(int(g)): dict(me=float(b1 + b2 * g),
                                se=float(np.sqrt(V[1, 1] + g * g * V[2, 2]
                                                 + 2 * g * V[1, 2])))
              for g in (12, 15, 20, 25, 30, 35, 40, 45)}

# ===========================================================================
# series for the descriptive figures
# ===========================================================================
S["trend"] = [dict(year=int(y), cdd=float(CDD[:, j].mean()),
                   neet=float(NEET[:, j].mean()))
              for j, y in enumerate(YEARS)]
cmean_cdd = CDD.mean(axis=1)
cmean_neet = NEET.mean(axis=1)
b, a = np.polyfit(cmean_cdd, cmean_neet, 1)
r_cs = float(np.corrcoef(cmean_cdd, cmean_neet)[0, 1])
S["cross"] = dict(slope=float(b), intercept=float(a), r=r_cs,
                  points=[dict(c=c, cdd=float(x), neet=float(y))
                          for c, x, y in zip(COUNTRIES, cmean_cdd,
                                             cmean_neet)])

with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
    json.dump(S, fh, indent=1)

print("\nbaseline: " + "  ".join(
    "%s %.3f (p %.3f)" % (LBL[j], m_base.theta[j], m_base.p[j])
    for j in range(len(SHOW))))
print("AR1 %.4f AR2 %.4f Hansen %.4f instr %d" %
      (m_base.ar1_p, m_base.ar2_p, m_base.hansen_p,
       m_base.n_instruments))
print("YUR heat: %.3f (p %.3f), int %.4f (p %.3f)" %
      (m_yur.theta[1], m_yur.p[1], m_yur.theta[2], m_yur.p[2]))
print("pre-COVID heat: %.3f (p %.3f), int %.4f (p %.3f)" %
      (m_pre.theta[1], m_pre.p[1], m_pre.theta[2], m_pre.p[2]))
print("ME cutoff GRN:", S["me_cutoff"], " r cross-sectional:", r_cs)
