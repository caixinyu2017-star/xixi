# -*- coding: utf-8 -*-
"""Cheap derived quantities the prose quotes, appended to summary.json.

Everything here is a deterministic function of the estimation sample and the
already-fitted models; nothing involves resampling, so this script re-runs the
measurement model and the point regressions only. Run after run_all.py.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd
from scipy import stats

import qca
import semtools
from run_all import (CONTROLS, SPEC_ALL, MAIN, AVDM, m4, m5, c2_, cfa, ret,
                     ols, TAB, TP, UT)

S = json.load(open(os.path.join(TAB, "summary.json"), encoding="utf-8"))

# marginal effects of anxiety on adaptation at chosen anxiety levels
for tag, m in (("melo", -1.0), ("mehi", 1.0)):
    g = np.array([1.0, 2.0 * m])
    b = np.array([MAIN.params["ANX"], MAIN.params["ANX2"]])
    V = MAIN.cov.loc[["ANX", "ANX2"], ["ANX", "ANX2"]].to_numpy()
    S[tag] = dict(est=round(float(g @ b), 3),
                  se=round(float(np.sqrt(g @ V @ g)), 3))

# predicted adaptation: peak versus two SD of anxiety (curve heights)
b1, b2 = float(MAIN.params["ANX"]), float(MAIN.params["ANX2"])
tp = TP["tau"]
S["peak_height"] = round(b1 * tp + b2 * tp ** 2, 3)
S["height_p2"] = round(b1 * 2 + b2 * 4, 3)
S["drop_tp_to_p2"] = round((b1 * tp + b2 * tp ** 2) - (b1 * 2 + b2 * 4), 3)

# avoidance quadratic magnitude (for honest reporting of the near-null)
S["c2quad_b"] = round(float(c2_.params["ANX2"]), 3)

# anxiety equation on the full Time-1 sample: key coefficient
S["a1_full"] = round(float(m5.params["PHCD"]), 3)
S["a3_full"] = round(float(m5.params["PHCDxSUP"]), 3)

# first-stage slope of ANX in PHCD at SUP = -1 and +1
for tag, sv in (("fslo", -1.0), ("fshi", 1.0)):
    g = np.array([1.0, sv])
    b = np.array([m4.params["PHCD"], m4.params["PHCDxSUP"]])
    V = m4.cov.loc[["PHCD", "PHCDxSUP"], ["PHCD", "PHCDxSUP"]].to_numpy()
    S[tag] = dict(est=round(float(g @ b), 3),
                  se=round(float(np.sqrt(g @ V @ g)), 3))

# heterogeneity difference p-values from the table
rows = [l.rstrip("\n").split("\t")
        for l in open(os.path.join(TAB, "t11_heterogeneity.tsv"),
                      encoding="utf-8")][1:]
diffs = [float(r[3]) for r in rows if r[0].strip().startswith("difference")]
S["het_p_min"] = round(min(diffs), 3)
S["het_p_all"] = [round(d, 3) for d in diffs]

# discriminant validity: smallest sqrt(AVE) against largest latent correlation
tab = cfa.table()
S["sqrt_ave_min"] = round(min(np.sqrt(tab[n]["ave"]) for n in cfa.names), 3)

# fsQCA near-misses: highest-consistency rows that fail only PRI
conds = ["PHCD", "ANX", "LIT", "SUP", "EXPO"]
M = np.zeros((len(ret), len(conds)))
for j, c in enumerate(conds):
    x = ret[c].to_numpy()
    M[:, j] = qca.calibrate(x, *np.percentile(x, [95, 50, 5]))
yq = qca.calibrate(ret.ADP.to_numpy(), *np.percentile(ret.ADP, [95, 50, 5]))
tt = qca.truth_table(M, yq, freq_min=10, cons_min=0.80, pri_min=0.70)
near = [r for r in tt if r["n"] >= 10 and r["cons"] >= 0.80
        and r["pri"] < 0.70 and r["outcome"] == 0]
near = sorted(near, key=lambda r: -r["cons"])[:3]
S["qca_near"] = [dict(bits=dict(zip(conds, r["bits"])), n=r["n"],
                      cons=round(r["cons"], 3), pri=round(r["pri"], 3))
                 for r in near]
neg_rows = [r for r in qca.truth_table(M, 1 - yq, 10, 0.8, 0.7)
            if r["n"] >= 10]
best_neg = max(neg_rows, key=lambda r: r["cons"])
S["neg_cons_max"] = round(float(best_neg["cons"]), 3)
S["neg_pri_best"] = round(float(best_neg["pri"]), 3)

# occupation-level exposure descriptives for the sample section
S["expo_mean"] = round(float(ret.exposure.mean()), 2)
S["expo_sd"] = round(float(ret.exposure.std()), 2)
S["n_occ"] = int(ret.occupation.nunique())

with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
    json.dump(S, fh, indent=1)
print("summary extended to %d keys" % len(S))
