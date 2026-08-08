# -*- coding: utf-8 -*-
"""The complete estimation pipeline.

Reads data/survey.csv, runs the measurement model, the structural model with
its curvilinear second stage, the bootstrapped conditional-process analysis,
the heterogeneity and robustness batteries and the fuzzy-set configurational
analysis, and writes every table the manuscript reports to tables/*.tsv plus
a summary.json from which the prose interpolates every number it quotes.

Every random process is seeded here and nowhere else.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd
from scipy import stats

import qca
import semtools

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
os.makedirs(TAB, exist_ok=True)

SEED_BOOT = 20260501
N_BOOT = 5000
N_WILD = 999

df = pd.read_csv(os.path.join(DATA, "survey.csv"))
ret = df[df.retained == 1].reset_index(drop=True)

CONTROLS = ["female", "age", "master", "stem", "tier1", "months_grad",
            "employed", "parent_edu", "internship"]

SPEC_T1 = dict(
    PHCD=["phcd1", "phcd2", "phcd3", "phcd4"],
    ANX=["anx1", "anx2", "anx3", "anx4"],
    LIT=["lit1", "lit2", "lit3", "lit4"],
    SUP=["sup1", "sup2", "sup3", "sup4"],
)
SPEC_ALL = dict(SPEC_T1,
                ADP=["adp1", "adp2", "adp3", "adp4"],
                AVD=["avd1", "avd2", "avd3"])
LABEL = dict(PHCD="Perceived human capital depreciation",
             ANX="AI-related career anxiety",
             LIT="Generative-AI literacy",
             SUP="Perceived employability support",
             ADP="Occupational adaptation",
             AVD="Career avoidance")

S = {}          # summary.json accumulator
S["n_t1"] = int(len(df))
S["n_t2"] = int(len(ret))
S["retention"] = round(100 * len(ret) / len(df), 1)


def w(name, header, rows):
    with open(os.path.join(TAB, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(c) for c in r) + "\n")
    print("  ", name)


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def f3(x):
    return "%.3f" % x


# ===========================================================================
# OLS with HC3, cluster-robust and wild-bootstrap inference
# ===========================================================================
class Res:
    def __init__(self, names, b, V, nobs, r2):
        self.params = pd.Series(b, index=names)
        self.cov = pd.DataFrame(V, index=names, columns=names)
        self.se = pd.Series(np.sqrt(np.diag(V)), index=names)
        self.tstat = self.params / self.se
        self.pval = pd.Series(2 * (1 - stats.norm.cdf(np.abs(self.tstat))),
                              index=names)
        self.nobs, self.r2 = nobs, r2

    def cell(self, name, d=3):
        if name not in self.params.index:
            return ("", "")
        b, se, p = self.params[name], self.se[name], self.pval[name]
        return ("%.*f%s" % (d, b, stars(p)), "(%.*f)" % (d, se))


def ols(dat, y, xs, cluster=None):
    X = np.column_stack([np.ones(len(dat))] +
                        [dat[c].to_numpy(float) for c in xs])
    yv = dat[y].to_numpy(float)
    names = ["const"] + list(xs)
    b, *_ = np.linalg.lstsq(X, yv, rcond=None)
    e = yv - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    if cluster is None:                                   # HC3
        h = np.einsum("ij,jk,ik->i", X, XtXi, X)
        u = e / (1 - h)
        meat = (X * u[:, None]).T @ (X * u[:, None])
        V = XtXi @ meat @ XtXi
    else:
        cl = dat[cluster].to_numpy()
        meat = np.zeros((X.shape[1], X.shape[1]))
        for g in np.unique(cl):
            Xg, eg = X[cl == g], e[cl == g]
            sg = Xg.T @ eg
            meat += np.outer(sg, sg)
        G = len(np.unique(cl))
        n, k = X.shape
        meat *= G / (G - 1) * (n - 1) / (n - k)
        V = XtXi @ meat @ XtXi
    r2 = 1 - e.var() / yv.var()
    return Res(names, b, V, len(dat), r2)


def wild_p(dat, y, xs, target, cluster, seed=11):
    """Wild cluster bootstrap p-value (Rademacher, null imposed)."""
    rng = np.random.default_rng(seed)
    xs0 = [c for c in xs if c != target]
    X0 = np.column_stack([np.ones(len(dat))] +
                         [dat[c].to_numpy(float) for c in xs0])
    yv = dat[y].to_numpy(float)
    b0, *_ = np.linalg.lstsq(X0, yv, rcond=None)
    e0 = yv - X0 @ b0
    cl = dat[cluster].to_numpy()
    gs = np.unique(cl)
    t_obs = ols(dat, y, xs, cluster=cluster).tstat[target]
    hits = 0
    d2 = dat.copy()
    for r in range(N_WILD):
        signs = dict(zip(gs, rng.choice([-1.0, 1.0], len(gs))))
        d2[y] = X0 @ b0 + e0 * np.array([signs[g] for g in cl])
        t_b = ols(d2, y, xs, cluster=cluster).tstat[target]
        hits += abs(t_b) >= abs(t_obs)
    return (hits + 1) / (N_WILD + 1)


# ===========================================================================
# 1. Sample profile and attrition
# ===========================================================================
print("[1] sample profile")
comp = df.assign(
    phcd_m=df[SPEC_T1["PHCD"]].mean(axis=1),
    anx_m=df[SPEC_T1["ANX"]].mean(axis=1),
    lit_m=df[SPEC_T1["LIT"]].mean(axis=1),
    sup_m=df[SPEC_T1["SUP"]].mean(axis=1))
rows = []
profile = [
    ("Female (%)", "female", 100), ("Age (years)", "age", 1),
    ("Master's degree (%)", "master", 100), ("STEM major (%)", "stem", 100),
    ("Tier-1 city (%)", "tier1", 100),
    ("Months since graduation", "months_grad", 1),
    ("Employed (%)", "employed", 100),
    ("Parent with tertiary education (%)", "parent_edu", 100),
    ("Internship experience (%)", "internship", 100),
    ("Depreciation items, mean", "phcd_m", 1),
    ("Anxiety items, mean", "anx_m", 1),
]
att_ps = {}
for lab, c, scale in profile:
    a = comp.loc[comp.retained == 1, c]
    b = comp.loc[comp.retained == 0, c]
    t, p = stats.ttest_ind(a, b, equal_var=False)
    att_ps[c] = p
    rows.append([lab, "%.1f" % (scale * comp[c].mean()),
                 "%.1f" % (scale * a.mean()), "%.1f" % (scale * b.mean()),
                 "%.3f" % p])
w("t01_sample.tsv",
  ["Characteristic", "Time 1 (N = %d)" % len(df),
   "Retained (N = %d)" % len(ret),
   "Lost (N = %d)" % (len(df) - len(ret)), "p"], rows)
S["att_p_min"] = round(min(att_ps.values()), 3)
S["att_p_anx"] = round(att_ps["anx_m"], 3)
S["income_median"] = int(df.loc[df.employed == 1, "income"].median())

# ===========================================================================
# 2-3. Measurement model
# ===========================================================================
print("[2] measurement model")
cfa = semtools.CFA(ret, SPEC_ALL).fit()
S["cfa"] = dict(chi2=round(cfa.chi2, 2), df=int(cfa.df),
                chi2df=round(cfa.chi2 / cfa.df, 2),
                cfi=round(cfa.cfi, 3), tli=round(cfa.tli, 3),
                rmsea=round(cfa.rmsea, 3), srmr=round(cfa.srmr, 3))
tab = cfa.table()
rows = []
for name in cfa.names:
    t = tab[name]
    rows.append([LABEL[name] + " (%s)" % name, "", "", "", ""])
    for it, ld in zip(t["items"], t["load"]):
        rows.append(["    " + it, f3(ld), "", "", ""])
    rows[-len(t["items"])][2:] = [f3(t["alpha"]), f3(t["cr"]), f3(t["ave"])]
w("t02_measurement.tsv",
  ["Construct and items", "Loading", "α", "CR", "AVE"], rows)
S["load_min"] = round(min(min(tab[n]["load"]) for n in cfa.names), 3)
S["alpha_min"] = round(min(tab[n]["alpha"] for n in cfa.names), 3)
S["cr_min"] = round(min(tab[n]["cr"] for n in cfa.names), 3)
S["ave_min"] = round(min(tab[n]["ave"] for n in cfa.names), 3)

FL = cfa.fornell_larcker()
HT = cfa.htmt()
rows = []
for i, n in enumerate(cfa.names):
    cells = []
    for j in range(len(cfa.names)):
        if j < i:
            cells.append(f3(FL[i, j]))
        elif j == i:
            cells.append(f3(FL[i, i]))
        else:
            cells.append(f3(HT[i, j]))
    rows.append([n] + cells)
w("t03_validity.tsv", ["Construct"] + cfa.names, rows)
S["htmt_max"] = round(float(HT.max()), 3)
S["phi_max"] = round(float(np.abs(cfa.Phi - np.eye(cfa.k)).max()), 3)

# ===========================================================================
# 4. Scores, descriptives, correlations
# ===========================================================================
print("[3] factor scores and descriptives")
sc = cfa.scores()
for j, n in enumerate(cfa.names):
    ret[n] = sc[:, j]
ret["ANX2"] = ret.ANX ** 2 - (ret.ANX ** 2).mean()
ret["PHCDxSUP"] = ret.PHCD * ret.SUP
ret["ANXxLIT"] = ret.ANX * ret.LIT
ret["ANX2xLIT"] = ret.ANX ** 2 * ret.LIT - (ret.ANX ** 2 * ret.LIT).mean()
ret["EXPO"] = (ret.exposure - ret.exposure.mean()) / ret.exposure.std()

# T1-only CFA on the full sample, for attrition weighting and robustness
cfa1 = semtools.CFA(df, SPEC_T1).fit()
sc1 = cfa1.scores()
for j, n in enumerate(cfa1.names):
    df[n] = sc1[:, j]
df["PHCDxSUP"] = df.PHCD * df.SUP

vars6 = cfa.names + ["EXPO"]
rows = []
C = ret[vars6].corr().to_numpy()
for i, n in enumerate(vars6):
    rows.append([n,
                 f3(ret[n].mean()), f3(ret[n].std())] +
                [f3(C[i, j]) if j <= i else "" for j in range(len(vars6))])
w("t04_correlations.tsv",
  ["Variable", "Mean", "SD"] + vars6, rows)
S["r_anx_adp"] = round(float(ret.ANX.corr(ret.ADP)), 3)
S["r_phcd_anx"] = round(float(ret.PHCD.corr(ret.ANX)), 3)
S["r_expo_phcd"] = round(float(ret.EXPO.corr(ret.PHCD)), 3)

# ===========================================================================
# 5. Invariance and common-method diagnostics
# ===========================================================================
print("[4] invariance and method bias (slow)")
rows = []
inv = {}
for gname, gvar in (("Gender", "female"), ("Major", "stem")):
    g = ret[gvar].to_numpy()
    c_chi, c_df, _ = semtools.two_group(ret, g, SPEC_ALL, False)
    m_chi, m_df, _ = semtools.two_group(ret, g, SPEC_ALL, True)
    c_cfi = semtools.cfi_pair(c_chi, c_df, ret, SPEC_ALL, g)
    m_cfi = semtools.cfi_pair(m_chi, m_df, ret, SPEC_ALL, g)
    dchi = m_chi - c_chi
    ddf = m_df - c_df
    p = 1 - stats.chi2.cdf(dchi, ddf)
    inv[gname] = dict(dcfi=round(c_cfi - m_cfi, 4), p=round(p, 3))
    rows.append(["%s: configural" % gname, "%.1f" % c_chi, str(c_df),
                 f3(c_cfi), "", ""])
    rows.append(["%s: metric" % gname, "%.1f" % m_chi, str(m_df),
                 f3(m_cfi), "%.1f (%d)" % (dchi, ddf), f3(p)])
S["inv"] = inv

# Harman single factor share
items_all = [c for v in SPEC_ALL.values() for c in v]
Z = (ret[items_all] - ret[items_all].mean()) / ret[items_all].std()
ev = np.linalg.eigvalsh(np.corrcoef(Z.to_numpy(), rowvar=False))[::-1]
S["harman"] = round(100 * ev[0] / len(items_all), 1)

# equal-loading unmeasured method factor
ulmc = semtools.CFAMethod(ret, SPEC_ALL).fit()
d_cfi_m = None
S["ulmc_share"] = round(100 * ulmc.method_share, 1)
S["ulmc_dchi"] = round(cfa.chi2 - ulmc.chi2, 1)
rows.append(["Harman single factor: first-factor share (%)",
             "%.1f" % S["harman"], "", "", "", ""])
rows.append(["Method factor: variance share (%)",
             "%.1f" % S["ulmc_share"], "", "", "", ""])
w("t05_invariance_cmb.tsv",
  ["Model", "χ2", "df", "CFI", "Δχ2 (Δdf)", "p"], rows)

# ===========================================================================
# 6. Anxiety equation (H1, H6)
# ===========================================================================
print("[5] structural: anxiety")
m1 = ols(ret, "ANX", ["PHCD"])
m2 = ols(ret, "ANX", ["PHCD"] + CONTROLS)
m3 = ols(ret, "ANX", ["PHCD", "SUP"] + CONTROLS)
m4 = ols(ret, "ANX", ["PHCD", "SUP", "PHCDxSUP"] + CONTROLS)
m5 = ols(df, "ANX", ["PHCD", "SUP", "PHCDxSUP"] + CONTROLS)   # full T1
anx_models = [m1, m2, m3, m4, m5]


def reg_table(models, order, extra_rows=()):
    rows = []
    for v, lab in order:
        top = [lab]
        bot = [""]
        for m in models:
            c = m.cell(v)
            top.append(c[0])
            bot.append(c[1])
        rows.append(top)
        rows.append(bot)
    for er in extra_rows:
        rows.append(er)
    rows.append(["Controls", *("Yes" if "female" in m.params.index else "No"
                               for m in models)])
    rows.append(["Observations", *("{:,}".format(m.nobs) for m in models)])
    rows.append(["R²", *(f3(m.r2) for m in models)])
    return rows

w("t06_anxiety.tsv",
  ["", "(1)", "(2)", "(3)", "(4)", "(5)"],
  reg_table(anx_models, [("PHCD", "PHCD"), ("SUP", "SUP"),
                         ("PHCDxSUP", "PHCD × SUP")]))
S["a1"] = round(float(m4.params["PHCD"]), 3)
S["a1_se"] = round(float(m4.se["PHCD"]), 3)
S["a3"] = round(float(m4.params["PHCDxSUP"]), 3)
S["a3_p"] = round(float(m4.pval["PHCDxSUP"]), 3)
S["a_sup"] = round(float(m4.params["SUP"]), 3)
S["anx_r2"] = round(float(m4.r2), 3)

# ===========================================================================
# 7. Adaptation equation (H2, H5) + U validation
# ===========================================================================
print("[6] structural: adaptation")
b1_ = ols(ret, "ADP", ["ANX"] + CONTROLS)
b2_ = ols(ret, "ADP", ["ANX", "ANX2"] + CONTROLS)
b3_ = ols(ret, "ADP", ["ANX", "ANX2", "LIT", "ANXxLIT"] + CONTROLS)
b4_ = ols(ret, "ADP",
          ["ANX", "ANX2", "LIT", "ANXxLIT", "SUP", "PHCD"] + CONTROLS)
ret["occ"] = ret.occupation
b5_ = ols(ret, "ADP", ["ANX", "ANX2", "LIT", "ANXxLIT", "SUP", "PHCD"]
          + CONTROLS, cluster="occ")
adp_models = [b1_, b2_, b3_, b4_, b5_]
w("t07_adaptation.tsv",
  ["", "(1)", "(2)", "(3)", "(4)", "(5)"],
  reg_table(adp_models,
            [("ANX", "ANX"), ("ANX2", "ANX²"), ("LIT", "LIT"),
             ("ANXxLIT", "ANX × LIT"), ("SUP", "SUP"), ("PHCD", "PHCD")]))
MAIN = b4_
S["b1"] = round(float(MAIN.params["ANX"]), 3)
S["b2"] = round(float(MAIN.params["ANX2"]), 3)
S["b2_se"] = round(float(MAIN.se["ANX2"]), 3)
S["b2_p"] = round(float(MAIN.pval["ANX2"]), 4)
S["b3"] = round(float(MAIN.params["ANXxLIT"]), 3)
S["b3_p"] = round(float(MAIN.pval["ANXxLIT"]), 3)
S["b_lit"] = round(float(MAIN.params["LIT"]), 3)
S["adp_r2"] = round(float(MAIN.r2), 3)
S["dr2_quad"] = round(float(b2_.r2 - b1_.r2), 3)

# Lind-Mehlum + Fieller (port of the earlier toolkit, HC3 covariance)
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location(
    "curvetools", os.path.join(os.path.dirname(HERE), "..",
                               "genai-youth-inverted-u", "analysis",
                               "econtools.py"))
curve = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(curve)

xl, xh = float(ret.ANX.quantile(0.01)), float(ret.ANX.quantile(0.99))
UT = curve.utest(MAIN, "ANX", "ANX2", xl, xh)
TP = curve.turning_point(MAIN, "ANX", "ANX2")
S["ut"] = dict(slope_lo=round(UT["slope_lo"], 3),
               t_lo=round(UT["t_lo"], 2),
               slope_hi=round(UT["slope_hi"], 3),
               t_hi=round(UT["t_hi"], 2),
               p=round(UT["p"], 4))
S["tp"] = dict(tau=round(TP["tau"], 3), se=round(TP["se"], 3),
               ci_low=round(TP["ci_low"], 3), ci_high=round(TP["ci_high"], 3))
S["share_beyond"] = round(100 * float((ret.ANX > TP["tau"]).mean()), 1)
full_q = ols(ret, "ADP", ["ANX", "ANX2", "LIT", "ANXxLIT", "ANX2xLIT",
                          "SUP", "PHCD"] + CONTROLS)
MT, SHIFT = curve.mod_turning(full_q, "ANX", "ANX2", "ANXxLIT", "ANX2xLIT",
                              [-1.0, 0.0, 1.0])
S["tp_lit"] = [dict(z=m["z"], tau=round(m["tau"], 3), se=round(m["se"], 3))
               for m in MT]
S["tp_shift"] = dict(dtau=round(SHIFT["dtau"], 3), se=round(SHIFT["se"], 3),
                     p=round(SHIFT["p"], 3))
S["b_anx2xlit_p"] = round(float(full_q.pval["ANX2xLIT"]), 3)

rows = [
    ["Slope at the 1st percentile of ANX (%.2f)" % xl,
     "%.3f (t = %.2f)" % (UT["slope_lo"], UT["t_lo"])],
    ["Slope at the 99th percentile of ANX (%.2f)" % xh,
     "%.3f (t = %.2f)" % (UT["slope_hi"], UT["t_hi"])],
    ["Sasabuchi test of the composite null (p)",
     "< 0.0001" if UT["p"] < 1e-4 else "%.4f" % UT["p"]],
    ["Turning point (SD of ANX)", "%.3f (SE %.3f)" % (TP["tau"], TP["se"])],
    ["95% Fieller interval", "[%.3f, %.3f]" % (TP["ci_low"], TP["ci_high"])],
    ["Respondents beyond the turning point (%)", "%.1f" % S["share_beyond"]],
    ["Turning point at LIT = −1 SD", "%.3f (SE %.3f)"
     % (MT[0]["tau"], MT[0]["se"])],
    ["Turning point at LIT = +1 SD", "%.3f (SE %.3f)"
     % (MT[2]["tau"], MT[2]["se"])],
]
w("t08_utest.tsv", ["Quantity", "Estimate"], rows)

# ===========================================================================
# 8. Avoidance equation (H3, H5)
# ===========================================================================
print("[7] structural: avoidance")
c1_ = ols(ret, "AVD", ["ANX"] + CONTROLS)
c2_ = ols(ret, "AVD", ["ANX", "ANX2"] + CONTROLS)
c3_ = ols(ret, "AVD", ["ANX", "LIT", "ANXxLIT"] + CONTROLS)
c4_ = ols(ret, "AVD", ["ANX", "LIT", "ANXxLIT", "SUP", "PHCD"] + CONTROLS)
c5_ = ols(ret, "AVD", ["ANX", "LIT", "ANXxLIT", "SUP", "PHCD"] + CONTROLS,
          cluster="occ")
avd_models = [c1_, c2_, c3_, c4_, c5_]
w("t09_avoidance.tsv",
  ["", "(1)", "(2)", "(3)", "(4)", "(5)"],
  reg_table(avd_models,
            [("ANX", "ANX"), ("ANX2", "ANX²"), ("LIT", "LIT"),
             ("ANXxLIT", "ANX × LIT"), ("SUP", "SUP"), ("PHCD", "PHCD")]))
AVDM = c4_
S["c1"] = round(float(AVDM.params["ANX"]), 3)
S["c2quad_p"] = round(float(c2_.pval["ANX2"]), 3)
S["c_lit_int"] = round(float(AVDM.params["ANXxLIT"]), 3)
S["c_lit_int_p"] = round(float(AVDM.pval["ANXxLIT"]), 3)
S["avd_r2"] = round(float(AVDM.r2), 3)

# ===========================================================================
# 9. Conditional-process analysis (bootstrap)
# ===========================================================================
print("[8] bootstrap conditional-process analysis (%d reps)" % N_BOOT)
rng = np.random.default_rng(SEED_BOOT)
AX = ["PHCD", "SUP", "PHCDxSUP"] + CONTROLS
BX = ["ANX", "ANX2", "LIT", "ANXxLIT", "SUP", "PHCD"] + CONTROLS
CX = ["ANX", "LIT", "ANXxLIT", "SUP", "PHCD"] + CONTROLS
levels_m = [-1.0, 0.0, 1.0]
levels_w = [-1.0, 1.0]


def draws_once(d):
    """One estimation of every quantity the process analysis reports."""
    a = ols(d, "ANX", AX)
    b = ols(d, "ADP", BX)
    c = ols(d, "AVD", CX)
    out = {}
    for wv in levels_w:                       # first-stage a at SUP = w
        aw = a.params["PHCD"] + a.params["PHCDxSUP"] * wv
        for mv in levels_m:                   # second stage at ANX = m
            for lv in levels_w:               # ... and LIT = l
                bm = (b.params["ANX"] + 2 * b.params["ANX2"] * mv
                      + b.params["ANXxLIT"] * lv)
                out["ind_adp_w%+d_m%+d_l%+d" % (wv, mv, lv)] = aw * bm
        cw = c.params["ANX"] + c.params["ANXxLIT"] * wv
        # avoidance second stage at LIT = w (reuse wv loop for compactness)
    a0 = a.params["PHCD"]
    for lv in levels_w:
        out["ind_avd_l%+d" % lv] = a0 * (c.params["ANX"]
                                         + c.params["ANXxLIT"] * lv)
    out["imm_sup_adp"] = a.params["PHCDxSUP"] * b.params["ANX"]
    out["imm_lit_adp"] = a0 * b.params["ANXxLIT"]
    out["imm_curv"] = a0 * 2 * b.params["ANX2"]
    out["imm_lit_avd"] = a0 * c.params["ANXxLIT"]
    return out

point = draws_once(ret)
boot = {k: np.empty(N_BOOT) for k in point}
idx = np.arange(len(ret))
for r in range(N_BOOT):
    d = ret.iloc[rng.choice(idx, len(idx), replace=True)]
    for k, v in draws_once(d).items():
        boot[k][r] = v

MED = {}
for k, v in point.items():
    lo, hi = np.percentile(boot[k], [2.5, 97.5])
    MED[k] = dict(est=round(float(v), 3), lo=round(float(lo), 3),
                  hi=round(float(hi), 3),
                  sig=bool(lo > 0 or hi < 0))
S["med"] = MED

rows = []
for wv in levels_w:
    for mv in levels_m:
        for lv in levels_w:
            k = "ind_adp_w%+d_m%+d_l%+d" % (wv, mv, lv)
            e = MED[k]
            rows.append(["SUP = %+d, ANX = %+d, LIT = %+d" % (wv, mv, lv),
                         f3(e["est"]), "[%.3f, %.3f]" % (e["lo"], e["hi"])])
for lv in levels_w:
    e = MED["ind_avd_l%+d" % lv]
    rows.append(["Avoidance path, LIT = %+d" % lv, f3(e["est"]),
                 "[%.3f, %.3f]" % (e["lo"], e["hi"])])
for k, lab in (("imm_sup_adp", "IMM of SUP (first stage, adaptation)"),
               ("imm_lit_adp", "IMM of LIT (second stage, adaptation)"),
               ("imm_curv", "Index of curvilinear mediation (2·a1·b2)"),
               ("imm_lit_avd", "IMM of LIT (second stage, avoidance)")):
    e = MED[k]
    rows.append([lab, f3(e["est"]), "[%.3f, %.3f]" % (e["lo"], e["hi"])])
w("t10_process.tsv",
  ["Conditional indirect effect", "Estimate", "95% bootstrap CI"], rows)

# ===========================================================================
# 10. Heterogeneity
# ===========================================================================
print("[9] heterogeneity")
groups = [
    ("Gender", "female", {1: "Female", 0: "Male"}),
    ("Major", "stem", {1: "STEM", 0: "Non-STEM"}),
    ("City", "tier1", {1: "Tier-1 city", 0: "Other cities"}),
    ("Exposure", None, None),
    ("Employment", "employed", {1: "Employed", 0: "Not employed"}),
]
ret["hi_expo"] = (ret.exposure >= ret.exposure.median()).astype(int)
rows = []
FOREST = []
for gname, gvar, labs in groups:
    if gvar is None:
        gvar, labs = "hi_expo", {1: "High exposure", 0: "Low exposure"}
    diffs = []
    for val in (1, 0):
        sub = ret[ret[gvar] == val]
        mres = ols(sub, "ADP", ["ANX", "ANX2", "LIT", "ANXxLIT", "SUP",
                                "PHCD"] + [c for c in CONTROLS if c != gvar])
        me = float(mres.params["ANX"])            # marginal effect at ANX = 0
        g = np.array([1.0, 0.0])
        V = mres.cov.loc[["ANX", "ANX2"], ["ANX", "ANX2"]].to_numpy()
        se = float(np.sqrt(g @ V @ g))
        b2g = float(mres.params["ANX2"])
        b2p = float(mres.pval["ANX2"])
        diffs.append((me, se))
        rows.append([labs[val], "{:,}".format(mres.nobs), f3(me),
                     "(%.3f)" % se, f3(b2g) + stars(b2p)])
        FOREST.append(dict(group="%s: %s" % (gname, labs[val]), me=me, se=se,
                           b2=b2g))
    dz = (diffs[0][0] - diffs[1][0]) / np.sqrt(diffs[0][1] ** 2
                                               + diffs[1][1] ** 2)
    rows.append(["    difference (z, p)", "",
                 "%.2f" % dz, "%.3f" % (2 * (1 - stats.norm.cdf(abs(dz)))),
                 ""])
w("t11_heterogeneity.tsv",
  ["Subsample", "N", "dADP/dANX at mean", "(SE)", "ANX²"], rows)
S["forest"] = FOREST
S["het_expo_gap"] = round(FOREST[6]["me"] - FOREST[7]["me"], 3)

# ===========================================================================
# 11. Robustness
# ===========================================================================
print("[10] robustness")
rob_rows = []

# (1) behavioural outcome: log reskilling hours
ret["lhours"] = np.log(ret.reskill_hours)
r1 = ols(ret, "lhours", ["ANX", "ANX2", "LIT", "ANXxLIT", "SUP", "PHCD"]
         + CONTROLS)
rob_rows.append(["(1) log reskilling hours", *r1.cell("ANX"),
                 *r1.cell("ANX2"), "{:,}".format(r1.nobs)])

# (2) inverse-probability weighting for attrition
pr = ols(df, "retained", ["PHCD", "ANX", "LIT", "SUP"] + CONTROLS)
ph = np.clip(pr.params["const"] + df[["PHCD", "ANX", "LIT", "SUP"]
                                     + CONTROLS].to_numpy(float)
             @ pr.params[1:].to_numpy(), 0.3, 0.97)
S["ipw_anx_p"] = round(float(pr.pval["ANX"]), 3)
wts = (1.0 / ph)[df.retained == 1]
Xw = ["ANX", "ANX2", "LIT", "ANXxLIT", "SUP", "PHCD"] + CONTROLS
Xm = np.column_stack([np.ones(len(ret))] +
                     [ret[c].to_numpy(float) for c in Xw])
yv = ret.ADP.to_numpy(float)
sw = np.sqrt(np.asarray(wts))
bw, *_ = np.linalg.lstsq(Xm * sw[:, None], yv * sw, rcond=None)
ew = yv - Xm @ bw
XtXi = np.linalg.inv((Xm * sw[:, None]).T @ (Xm * sw[:, None]))
meat = (Xm * (sw ** 2 * ew)[:, None]).T @ Xm
Vw = XtXi @ ((Xm * (sw * ew)[:, None]).T @ (Xm * (sw * ew)[:, None])) @ XtXi
rw = Res(["const"] + Xw, bw, Vw, len(ret), 1 - ew.var() / yv.var())
rob_rows.append(["(2) inverse-probability weighted", *rw.cell("ANX"),
                 *rw.cell("ANX2"), "{:,}".format(rw.nobs)])

# (3) excluding software and IT occupations
sub = ret[ret.occupation != "Software and IT services"]
r3 = ols(sub, "ADP", Xw)
rob_rows.append(["(3) excluding software and IT", *r3.cell("ANX"),
                 *r3.cell("ANX2"), "{:,}".format(r3.nobs)])

# (4) unit-weighted composites instead of factor scores
comp2 = ret.copy()
for n, cols in SPEC_ALL.items():
    m = ret[cols].mean(axis=1)
    comp2[n] = (m - m.mean()) / m.std()
comp2["ANX2"] = comp2.ANX ** 2 - (comp2.ANX ** 2).mean()
comp2["ANXxLIT"] = comp2.ANX * comp2.LIT
r4 = ols(comp2, "ADP", Xw)
rob_rows.append(["(4) unit-weighted composites", *r4.cell("ANX"),
                 *r4.cell("ANX2"), "{:,}".format(r4.nobs)])

# (5) marker-partialled scores
mk = ret[["mkr1", "mkr2", "mkr3"]].mean(axis=1)
mkz = (mk - mk.mean()) / mk.std()
part = ret.copy()
for n in list(SPEC_ALL.keys()):
    b_m = np.polyfit(mkz, part[n], 1)
    part[n] = part[n] - b_m[0] * mkz
    part[n] = (part[n] - part[n].mean()) / part[n].std()
part["ANX2"] = part.ANX ** 2 - (part.ANX ** 2).mean()
part["ANXxLIT"] = part.ANX * part.LIT
r5 = ols(part, "ADP", Xw)
S["r_marker_max"] = round(float(np.abs(
    ret[list(SPEC_ALL.keys())].corrwith(mkz)).max()), 3)
rob_rows.append(["(5) marker-partialled scores", *r5.cell("ANX"),
                 *r5.cell("ANX2"), "{:,}".format(r5.nobs)])

# (6) occupation-clustered wild bootstrap for the curvature
pwild = wild_p(ret, "ADP", Xw, "ANX2", "occ")
S["wild_p"] = round(float(pwild), 3)
rob_rows.append(["(6) wild cluster bootstrap p for ANX² "
                 "(20 occupation clusters)", "", "", "%.3f" % pwild, "",
                 "{:,}".format(len(ret))])
w("t12_robustness.tsv",
  ["Specification", "ANX", "(SE)", "ANX²", "(SE)", "N"], rob_rows)
S["rob"] = dict(
    hours_b2=round(float(r1.params["ANX2"]), 3),
    hours_b2_p=round(float(r1.pval["ANX2"]), 4),
    ipw_b2=round(float(rw.params["ANX2"]), 3),
    excl_b2=round(float(r3.params["ANX2"]), 3),
    comp_b2=round(float(r4.params["ANX2"]), 3),
    marker_b2=round(float(r5.params["ANX2"]), 3))

# ===========================================================================
# 12. fsQCA
# ===========================================================================
print("[11] fsQCA")
conds = ["PHCD", "ANX", "LIT", "SUP", "EXPO"]
CAL = {}
Mm = np.zeros((len(ret), len(conds)))
anchor_rows = []
for j, c in enumerate(conds):
    x = ret[c].to_numpy()
    a95, a50, a05 = np.percentile(x, [95, 50, 5])
    Mm[:, j] = qca.calibrate(x, a95, a50, a05)
    CAL[c] = [round(a95, 2), round(a50, 2), round(a05, 2)]
    anchor_rows.append([c, "%.2f" % a95, "%.2f" % a50, "%.2f" % a05])
yq = qca.calibrate(ret.ADP.to_numpy(), *np.percentile(ret.ADP, [95, 50, 5]))
yn = 1 - yq

nec_rows = []
for j, c in enumerate(conds):
    for neg, lab in ((False, c), (True, "~" + c)):
        x = 1 - Mm[:, j] if neg else Mm[:, j]
        nec_rows.append([lab, f3(qca.consistency(y=yq, x=x)),
                         f3(qca.coverage(x=x, y=yq))])
w("t13_calibration.tsv", ["Condition", "Full (0.95)", "Cross (0.50)",
                          "Out (0.05)"], anchor_rows)
w("t13b_necessity.tsv", ["Condition", "Consistency", "Coverage"], nec_rows)
S["nec_max"] = round(max(float(r[1]) for r in nec_rows), 3)

rows_tt = qca.truth_table(Mm, yq, freq_min=10, cons_min=0.80, pri_min=0.70)
S["tt_kept"] = int(sum(1 for r in rows_tt if r["outcome"] >= 0))
S["tt_pos"] = int(sum(1 for r in rows_tt if r["outcome"] == 1))
exp = dict(PHCD=1, ANX=None, LIT=1, SUP=1, EXPO=1)
inter, ov = qca.solution(rows_tt, conds, yq, Mm, "intermediate", exp)
pars, _ = qca.solution(rows_tt, conds, yq, Mm, "parsimonious")
core = set()
for t in pars:
    for nm, v in t["term"]:
        core.add((nm, v))

sym_rows = []
for i, t in enumerate(inter, 1):
    row = ["C%d" % i]
    tdict = dict(t["term"])
    for c in conds:
        if c not in tdict:
            row.append("")
        else:
            filled = tdict[c] == 1
            is_core = (c, tdict[c]) in core
            row.append(("●" if filled else "⊗") + ("" if is_core else "°"))
    row += [f3(t["cons"]), f3(t["rawcov"]), f3(t["uniqcov"])]
    sym_rows.append(row)
sym_rows.append(["Solution", "", "", "", "", "",
                 f3(ov["cons"]), f3(ov["cov"]), ""])
w("t14_configurations.tsv",
  ["Configuration"] + conds + ["Consistency", "Raw coverage",
                               "Unique coverage"], sym_rows)
S["qca"] = dict(n_conf=len(inter), sol_cons=round(ov["cons"], 3),
                sol_cov=round(ov["cov"], 3),
                terms=[{"term": t["term"], "cons": round(t["cons"], 3),
                        "rawcov": round(t["rawcov"], 3),
                        "uniqcov": round(t["uniqcov"], 3)} for t in inter])

neg_rows = qca.truth_table(Mm, yn, freq_min=10, cons_min=0.80, pri_min=0.70)
negsol = qca.solution(neg_rows, conds, yn, Mm, "intermediate",
                      dict(PHCD=0, ANX=None, LIT=0, SUP=0, EXPO=0))
if negsol:
    ninter, nov = negsol
    S["qca_neg"] = dict(n_conf=len(ninter), sol_cons=round(nov["cons"], 3),
                        sol_cov=round(nov["cov"], 3),
                        terms=[{"term": t["term"]} for t in ninter])
else:
    S["qca_neg"] = dict(n_conf=0)

# ===========================================================================
# figure data
# ===========================================================================
print("[12] figure inputs")
grid = np.linspace(ret.ANX.quantile(0.005), ret.ANX.quantile(0.995), 121)


def curve_pred(model, lit=0.0):
    names = ["ANX", "ANX2", "ANXxLIT"]
    out = []
    for g in grid:
        gv = {"ANX": g, "ANX2": g * g - (ret.ANX ** 2).mean(),
              "ANXxLIT": g * lit}
        vec = np.array([gv[n] for n in names])
        b = np.array([model.params[n] for n in names])
        V = model.cov.loc[names, names].to_numpy()
        out.append(dict(z=float(g), effect=float(vec @ b),
                        se=float(np.sqrt(vec @ V @ vec))))
    return out

S["curve_adp"] = curve_pred(MAIN)
S["curve_adp_litlo"] = curve_pred(MAIN, -1.0)
S["curve_adp_lithi"] = curve_pred(MAIN, +1.0)


def line_pred(model, names, mk):
    out = []
    for g in grid:
        vec = np.array([mk(g)[n] for n in names])
        b = np.array([model.params[n] for n in names])
        V = model.cov.loc[names, names].to_numpy()
        out.append(dict(z=float(g), effect=float(vec @ b),
                        se=float(np.sqrt(vec @ V @ vec))))
    return out

S["curve_avd"] = line_pred(AVDM, ["ANX", "ANXxLIT"],
                           lambda g: {"ANX": g, "ANXxLIT": 0.0})

# first-stage slopes of ANX in PHCD at SUP = ±1
sgrid = np.linspace(-2, 2, 81)
fs = []
for sv in sgrid:
    b = np.array([m4.params["PHCD"], m4.params["PHCDxSUP"]])
    V = m4.cov.loc[["PHCD", "PHCDxSUP"], ["PHCD", "PHCDxSUP"]].to_numpy()
    vec = np.array([1.0, sv])
    fs.append(dict(z=float(sv), effect=float(vec @ b),
                   se=float(np.sqrt(vec @ V @ vec))))
S["firststage"] = fs

# fsQCA scatter for the highest raw-coverage configuration
top = max(inter, key=lambda t: t["rawcov"])
S["qca_top"] = dict(term=top["term"], cons=round(top["cons"], 3),
                    rawcov=round(top["rawcov"], 3))
np.save(os.path.join(TAB, "qca_top_mem.npy"),
        np.column_stack([top["mem"], yq]))

S["anx_density"] = np.histogram(ret.ANX, bins=40,
                                range=(grid[0], grid[-1]))[0].tolist()
S["grid_lo"] = float(grid[0])
S["grid_hi"] = float(grid[-1])

with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
    json.dump(S, fh, indent=1)
print("summary.json written with %d keys" % len(S))
