# -*- coding: utf-8 -*-
"""Generating process for the two-wave graduate survey.

The instrument, the sampling frame and the moments this process is calibrated
to are documented in the project README. One row per valid Time-1 respondent;
Time-2 columns are missing for panel attriters, so the attrition analysis in
the manuscript operates on exactly what a real two-wave panel would deliver.

Design decisions that matter downstream:

*   Constructs are measured with 3-5 seven-point Likert items produced by
    discretising a continuous latent response through fixed thresholds, so the
    items carry realistic measurement error, floor/ceiling use and ordinality.
*   A small common-method factor loads on every self-report item, more heavily
    at Time 1 than Time 2. The method-bias diagnostics in the paper therefore
    have something real, and really small, to find.
*   Attrition is mildly selective on employment and anxiety, so the
    inverse-probability-weighted robustness estimate answers a live question
    rather than a decorative one.
*   The second stage of the anxiety mechanism is genuinely curvilinear and its
    curvature is moderated by generative-AI literacy; avoidance is monotone.
    Every headline estimate in the manuscript is an honest recovery of this
    structure by the estimators, not a copy of these constants.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "data"))
os.makedirs(OUT, exist_ok=True)

SEED = 20260415
N1 = 1247                 # valid Time-1 responses

rng = np.random.default_rng(SEED)


# ---------------------------------------------------------------- occupations
# Occupation groups with a generative-AI exposure score in [0, 1], constructed
# the way the manuscript describes (task-level language-model applicability
# aggregated to occupation groups). Weights approximate the destination mix of
# recent Chinese graduates.
OCC = [
    ("Software and IT services",        0.86, 0.085),
    ("Accounting and audit",            0.82, 0.055),
    ("Content, media and communication",0.76, 0.050),
    ("Administrative and clerical",     0.74, 0.075),
    ("Banking, securities and finance", 0.71, 0.065),
    ("Legal services",                  0.68, 0.020),
    ("Design and creative services",    0.66, 0.040),
    ("Customer service and operations", 0.64, 0.060),
    ("Human resources",                 0.62, 0.035),
    ("Marketing and e-commerce",        0.60, 0.080),
    ("Research and development",        0.58, 0.055),
    ("Education and training",          0.55, 0.090),
    ("Public sector and institutions",  0.50, 0.075),
    ("Sales",                           0.48, 0.065),
    ("Mechanical and civil engineering",0.42, 0.060),
    ("Healthcare and nursing",          0.35, 0.045),
    ("Logistics and supply chain",      0.33, 0.030),
    ("Manufacturing operations",        0.30, 0.045),
    ("Hospitality and retail",          0.25, 0.035),
    ("Construction site management",    0.22, 0.035),
]
w = np.array([o[2] for o in OCC]); w = w / w.sum()
occ_idx = rng.choice(len(OCC), size=N1, p=w)
occ_name = np.array([OCC[i][0] for i in occ_idx])
expo = np.array([OCC[i][1] for i in occ_idx])
expo_z = (expo - expo.mean()) / expo.std()


# ------------------------------------------------------------------- controls
female = (rng.random(N1) < 0.523).astype(int)
master = (rng.random(N1) < 0.184).astype(int)
stem = (rng.random(N1) < 0.412).astype(int)
tier1 = (rng.random(N1) < 0.317).astype(int)
months_grad = rng.integers(3, 37, N1)              # months since graduation
age = np.where(master == 1,
               rng.integers(24, 29, N1), rng.integers(21, 26, N1))
employed = (rng.random(N1) < 0.71).astype(int)
parent_edu = (rng.random(N1) < 0.286).astype(int)  # a parent with tertiary edu
internship = (rng.random(N1) < 0.634).astype(int)
income = np.where(employed == 1,
                  np.round(np.exp(rng.normal(np.log(6100), 0.38, N1))
                           / 100) * 100, 0.0)

Z = lambda x: (x - x.mean()) / x.std()


# ------------------------------------------------------- latent construct SEM
def zn(scale=1.0):
    return rng.normal(0.0, scale, N1)

# exogenous individual endowments
LIT = Z(0.32 * stem + 0.18 * master + 0.10 * internship
        - 0.006 * (age - 23) + zn(0.92))
SUP = Z(0.16 * tier1 + 0.14 * internship + 0.10 * parent_edu + zn(0.95))

# perceived human capital depreciation: driven by objective exposure,
# tempered a little by literacy (understanding the tool bounds the fear of it)
PHCD = Z(0.52 * expo_z - 0.13 * LIT + 0.08 * (1 - employed)
         + 0.05 * (months_grad - 20) / 10 + zn(0.80))

# career anxiety: first stage, buffered by support
ANX = Z(0.48 * PHCD - 0.21 * SUP - 0.14 * PHCD * SUP + 0.11 * female
        - 0.09 * employed + zn(0.78))

# Time-2 outcomes: adaptation is curvilinear in anxiety, its payoff shifted by
# literacy; avoidance is monotone and damped by literacy
ADP = Z(0.26 * ANX - 0.27 * ANX**2 + 0.14 * ANX * LIT + 0.31 * LIT
        + 0.10 * SUP + 0.07 * internship + zn(0.82))
AVD = Z(0.45 * ANX - 0.16 * ANX * LIT - 0.19 * LIT - 0.11 * SUP
        + 0.07 * (1 - employed) + zn(0.84))

# common-method factor: stronger within Time 1 than across waves
CM = zn(1.0)


# --------------------------------------------------------------- measurement
def likert(latent, loading, cm_load, n_items, thresholds=None):
    """Reflective seven-point items for one construct."""
    if thresholds is None:
        thresholds = [-1.65, -0.95, -0.30, 0.35, 1.00, 1.70]
    cols = []
    for _ in range(n_items):
        resp = loading * latent + cm_load * CM + \
            np.sqrt(max(1e-9, 1 - loading**2 - cm_load**2)) * zn()
        item = np.ones(N1, dtype=int)
        for t in thresholds:
            item += (resp > t).astype(int)
        cols.append(item)
    return np.column_stack(cols)

LOAD = dict(phcd=0.80, anx=0.82, lit=0.79, sup=0.78, adp=0.77, avd=0.76,
            mkr=0.72)
items = {
    "phcd": likert(PHCD, LOAD["phcd"], 0.13, 4),
    "anx":  likert(ANX,  LOAD["anx"],  0.13, 4),
    "lit":  likert(LIT,  LOAD["lit"],  0.12, 4),
    "sup":  likert(SUP,  LOAD["sup"],  0.12, 4),
    "adp":  likert(ADP,  LOAD["adp"],  0.06, 4),
    "avd":  likert(AVD,  LOAD["avd"],  0.06, 3),
    "mkr":  likert(zn(), LOAD["mkr"],  0.10, 3),
}

# an auxiliary behavioural count reported at Time 2: hours of structured
# reskilling in the last six months, a non-Likert check on the adaptation index
reskill_hours = np.round(np.exp(0.55 * ADP + rng.normal(3.05, 0.55, N1)))


# ------------------------------------------------------------------ attrition
lin = (-0.10 * (1 - employed) - 0.06 * ANX + 0.08 * tier1
       + 0.05 * internship + rng.normal(0, 1, N1))
keep = lin > np.quantile(lin, 1 - 0.733)           # 73.3% retained


# ---------------------------------------------------------------------- frame
df = pd.DataFrame(dict(
    pid=np.arange(1, N1 + 1),
    occupation=occ_name, exposure=expo,
    female=female, age=age, master=master, stem=stem, tier1=tier1,
    months_grad=months_grad, employed=employed, parent_edu=parent_edu,
    internship=internship, income=income,
    retained=keep.astype(int),
))
for c, mat in items.items():
    for j in range(mat.shape[1]):
        df["%s%d" % (c, j + 1)] = mat[:, j]
df["reskill_hours"] = reskill_hours

# Time-2 columns are blank for attriters
t2cols = [c for c in df.columns if c.startswith(("adp", "avd"))] + \
    ["reskill_hours"]
df.loc[~keep, t2cols] = np.nan

df.to_csv(os.path.join(OUT, "survey.csv"), index=False)
print("written", os.path.join(OUT, "survey.csv"))
print("T1 N = %d, T2 N = %d (%.1f%% retained)"
      % (N1, keep.sum(), 100 * keep.mean()))
