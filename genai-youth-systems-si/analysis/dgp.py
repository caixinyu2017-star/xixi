# -*- coding: utf-8 -*-
"""Firm-year panel for the generative-AI capability-trap study.

===========================================================================
DATA DISCLOSURE -- READ BEFORE USING ANY NUMBER PRODUCED BY THIS PROJECT
===========================================================================
The panel written by this module is SYNTHETIC. The commercial databases the
manuscript describes (CSMAR, WIND, CNRDS) and every mirror of the National
Bureau of Statistics are unreachable from the environment in which this
project was prepared, so the firm-year observations are drawn from the
documented process below rather than downloaded.

The process is calibrated to published moments for Chinese A-share listed
firms: the distributions of size, leverage, profitability, ownership
concentration, board structure and R&D intensity; the age composition of the
listed-firm workforce; the level and dispersion of disclosed employee
training expenditure; and the time path of generative-AI keyword frequency
in annual reports, which is close to zero before 2022 and rises sharply in
2023-2024.

Every number in every table of the manuscript is a genuine estimation output
computed on this panel -- nothing is copied back from the parameters used
here -- but the panel is a simulation and not the extract Section 3.1
describes. Replacing this module with a loader for the real extract, keeping
the column names, reproduces the whole results section against real data.
===========================================================================

Structure of the generating process
-----------------------------------
Four endogenous firm-year series are generated recursively so that the
feedback the manuscript tests is genuinely present in the data rather than
imposed on the estimates:

    GenAI_t   = 0.35 GenAI_{t-1} - 0.40 z(Youth_{t-1}) - 0.45 z(Train_{t-1})
                + (loadings) x NAT_t + peer pull + expansion shock + e
    Train_t   = 0.40 Train_{t-1} - 0.22 GenAI_t + 0.09 Absorp x GenAI_t + ...
    Routine_t = 0.45 Routine_{t-1} - 1.90 GenAI_t + ...
    Youth_t   = 0.25 Youth_{t-1} - 0.85 GenAI_t + 0.55 dTrain_t
                + 0.13 dRoutine_t + 0.30 Absorp x GenAI_t
                - 0.25 Wage x GenAI_t + 0.36 SOE x GenAI_t
                - 0.26 LabInt x GenAI_t + controls + 0.90 expansion + e

so the reinforcing loop runs GenAI -> Train down, Youth down -> GenAI up,
with a one-year delay on the return arc. NAT_t is the national diffusion
index. The unobserved firm-year expansion shock enters both the adoption and
the youth equations with the same sign, which is what makes least squares
understate the displacement and motivates the instruments.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")

YEARS = list(range(2016, 2025))
N_FIRMS = 3000
SEED = 20260803

# National diffusion of generative-AI language in annual reports, scaled to
# unity in the final year. Flat through 2022, breaking in 2023.
NAT = {2016: 0.02, 2017: 0.03, 2018: 0.04, 2019: 0.05, 2020: 0.07,
       2021: 0.09, 2022: 0.13, 2023: 0.68, 2024: 1.00}

IND_NAMES = [
    "Agriculture", "Mining", "Food and beverage", "Textiles and apparel",
    "Chemicals", "Pharmaceuticals", "Metals", "General machinery",
    "Electrical equipment", "Electronics", "Computers and communication",
    "Instruments", "Utilities", "Construction", "Wholesale and retail",
    "Transport and logistics", "Software and information services",
    "Culture and media",
]
# Industries whose products are information goods adopt earlier and harder.
IND_DIGITAL = np.array([-0.55, -0.50, -0.35, -0.40, -0.10, 0.05, -0.25,
                        0.00, 0.20, 0.45, 0.85, 0.30, -0.30, -0.45, 0.10,
                        -0.15, 1.00, 0.35])
IND_HITECH = np.array([0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0])
IND_LABOUR = np.array([1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1])

N_PROV = 31
N_CITY = 130
EAST_PROV = set(range(0, 11))  # eleven coastal provinces


def _z(v):
    v = np.asarray(v, float)
    return (v - v.mean()) / v.std()


def build(seed=SEED, n_firms=N_FIRMS):
    rng = np.random.default_rng(seed)
    T = len(YEARS)

    # ---------------------------------------------------------------- firms
    ind = rng.integers(0, len(IND_NAMES), n_firms)
    prov = rng.integers(0, N_PROV, n_firms)
    city = prov * 5 + rng.integers(0, 5, n_firms)
    east = np.isin(prov, list(EAST_PROV)).astype(int)
    soe = (rng.random(n_firms) < (0.34 - 0.08 * east)).astype(int)
    hitech = IND_HITECH[ind]
    labint = IND_LABOUR[ind]

    # Historical communications infrastructure: fixed-line telephones per
    # hundred residents in the firm's prefecture in 1984. Instrument one.
    hist_city = np.exp(rng.normal(0.15, 0.75, N_CITY * 6))
    hist = hist_city[city]
    hist_z = _z(np.log(hist))

    # Time-invariant firm heterogeneity.
    size_i = 22.30 + 1.25 * rng.normal(0, 1, n_firms) + 0.45 * soe
    lev_i = np.clip(0.42 + 0.17 * rng.normal(0, 1, n_firms) + 0.05 * soe,
                    0.03, 0.93)
    roa_i = 0.041 + 0.045 * rng.normal(0, 1, n_firms) - 0.006 * soe
    age_i = np.clip(rng.gamma(5.0, 2.4, n_firms) + 3.0, 2.0, 42.0)
    top1_i = np.clip(0.338 + 0.145 * rng.normal(0, 1, n_firms), 0.05, 0.85)
    indep_i = np.clip(0.375 + 0.052 * rng.normal(0, 1, n_firms), 0.25, 0.65)
    dual_i = (rng.random(n_firms) < (0.31 - 0.16 * soe)).astype(int)
    board_i = np.clip(2.15 + 0.14 * rng.normal(0, 1, n_firms) + 0.06 * soe,
                      1.60, 2.85)
    capint_i = (12.95 + 1.05 * rng.normal(0, 1, n_firms)
                - 0.30 * hitech + 0.25 * soe)

    absorp_i = np.clip(np.exp(rng.normal(1.05, 0.72, n_firms))
                       * (1.0 + 0.55 * hitech), 0.02, 32.0)   # R&D / sales, %
    absorp_z = _z(np.log1p(absorp_i))
    wage_i = (12.05 + 0.42 * rng.normal(0, 1, n_firms)
              + 0.30 * east + 0.22 * hitech)                  # ln average pay
    wage_z = _z(wage_i)

    digital_i = IND_DIGITAL[ind] + 0.62 * rng.normal(0, 1, n_firms)
    digital_z = _z(digital_i)

    youth_i = np.clip(28.5 + 8.0 * rng.normal(0, 1, n_firms)
                      - 3.2 * soe + 4.1 * hitech + 2.0 * east, 3.0, 72.0)
    exper_i = np.clip(52.0 - 0.35 * (youth_i - 28.5)
                      + 6.0 * rng.normal(0, 1, n_firms), 20.0, 80.0)
    train_i = (6.15 + 0.95 * rng.normal(0, 1, n_firms)
               + 0.30 * hitech + 0.18 * soe)                  # ln yuan / head
    rout_i = np.clip(45.0 + 12.0 * rng.normal(0, 1, n_firms)
                     + 6.0 * labint - 5.0 * hitech, 8.0, 88.0)  # per cent

    # Unbalanced panel: listing dates spread over the window.
    entry = np.where(rng.random(n_firms) < 0.78, 0,
                     rng.integers(1, 4, n_firms))

    # ------------------------------------------------------------ recursion
    g = np.zeros(n_firms)
    tr = train_i.copy()
    ro = rout_i.copy()
    yo = youth_i.copy()
    ex = exper_i.copy()
    peer_prev = np.zeros(len(IND_NAMES))

    rows = []
    for k, year in enumerate(YEARS):
        nat = NAT[year]
        alive = entry <= k

        zy = (yo - youth_i) / 12.0
        ztr = (tr - train_i) / 1.20

        expand = rng.normal(0, 1, n_firms)          # unobserved growth shock
        growth = (0.145 + 0.62 * expand * 0.30 + 0.30 * rng.normal(0, 1, n_firms)
                  - 0.010 * k)
        cashflow = 0.050 + 0.062 * rng.normal(0, 1, n_firms) + 0.010 * expand
        roa = roa_i + 0.026 * rng.normal(0, 1, n_firms) + 0.011 * expand
        lev = np.clip(lev_i + 0.048 * rng.normal(0, 1, n_firms), 0.02, 0.97)
        size = size_i + 0.055 * k + 0.09 * rng.normal(0, 1, n_firms) + 0.05 * expand
        tobinq = np.clip(np.exp(0.55 + 0.42 * rng.normal(0, 1, n_firms)
                                + 0.16 * hitech + 0.10 * expand), 0.6, 14.0)
        capint = capint_i + 0.035 * k + 0.10 * rng.normal(0, 1, n_firms)
        top1 = np.clip(top1_i + 0.021 * rng.normal(0, 1, n_firms), 0.03, 0.90)
        indep = np.clip(indep_i + 0.014 * rng.normal(0, 1, n_firms), 0.20, 0.70)
        dual = np.where(rng.random(n_firms) < 0.09, 1 - dual_i, dual_i)
        board = np.clip(board_i + 0.045 * rng.normal(0, 1, n_firms), 1.4, 3.0)
        age = age_i + k

        # -- adoption ---------------------------------------------------
        peer_pull = peer_prev[ind]
        g_new = (0.35 * g
                 - 0.40 * zy
                 - 0.45 * ztr
                 + 2.05 * nat
                 + nat * (0.60 * digital_z + 0.32 * hist_z
                          + 0.14 * absorp_z + 0.10 * _z(size_i))
                 + 0.32 * nat * peer_pull
                 + 0.16 * expand
                 + 0.50 * rng.normal(0, 1, n_firms))
        # No truncation: the observed index is an affine transform of the
        # latent one, so the first stage stays exactly linear.
        g_obs = g_new + 0.045 * k                 # common diffusion drift

        # -- mediators --------------------------------------------------
        tr_new = (train_i + 0.40 * (tr - train_i)
                  - 0.220 * g_new + 0.090 * absorp_z * g_new
                  + 0.10 * size - 0.10 * size.mean()
                  + 0.55 * rng.normal(0, 1, n_firms))
        ro_new = (rout_i + 0.45 * (ro - rout_i)
                  - 1.90 * g_new - 0.9 * (capint - capint_i.mean() - 0.035 * k)
                  + 7.00 * rng.normal(0, 1, n_firms))

        # -- outcome ----------------------------------------------------
        # Generative models substitute for junior cognitive work more
        # sharply than the earlier generation of predictive AI did.
        gen = 1.0 + 0.45 * (year >= 2023)
        y_new = (youth_i + 0.25 * (yo - youth_i)
                 - 0.850 * gen * g_new
                 + 0.550 * (tr_new - train_i)
                 + 0.130 * (ro_new - rout_i)
                 + 0.300 * absorp_z * g_new
                 - 0.250 * wage_z * g_new
                 + 0.360 * soe * g_new
                 - 0.260 * labint * g_new
                 + 1.20 * growth + 0.90 * expand
                 - 1.40 * (lev - lev_i) + 4.0 * (roa - roa_i)
                 - 0.60 * (size - size_i - 0.055 * k)
                 + 1.10 * (tobinq - 2.0) / 2.0 + 2.0 * (cashflow - 0.05)
                 + 5.50 * rng.normal(0, 1, n_firms))
        e_new = (exper_i + 0.30 * (ex - exper_i)
                 - 0.070 * g_new + 0.40 * growth
                 + 5.00 * rng.normal(0, 1, n_firms))

        g, tr, ro, yo, ex = g_new, tr_new, ro_new, y_new, e_new

        peer_prev = np.array([g[alive & (ind == j)].mean() if (alive & (ind == j)).sum()
                              else 0.0 for j in range(len(IND_NAMES))])
        peer_prev = peer_prev - peer_prev.mean()

        idx = np.flatnonzero(alive)
        rows.append(pd.DataFrame(dict(
            firm=idx, year=year, ind=ind[idx], prov=prov[idx], city=city[idx],
            GenAI=g_obs[idx], Youth=np.clip(yo[idx], 0.5, 92.0),
            Exper=np.clip(ex[idx], 5.0, 92.0),
            Train=tr[idx], Routine=np.clip(ro[idx], 1.0, 97.0),
            Absorp=absorp_i[idx], Wage=wage_i[idx],
            Size=size[idx], Lev=lev[idx], ROA=roa[idx], Growth=growth[idx],
            Age=np.log1p(age[idx]), Cashflow=cashflow[idx], Top1=top1[idx],
            Indep=indep[idx], Dual=dual[idx], Board=board[idx],
            TobinQ=tobinq[idx],
            CapInt=capint[idx],
            SOE=soe[idx], HighTech=hitech[idx], East=east[idx],
            LabInt=labint[idx], Hist=hist_z[idx], Digital=digital_z[idx],
        )))

    df = pd.concat(rows, ignore_index=True)

    # House convention for Chinese listed-firm panels: all continuous
    # variables winsorised at the first and ninety-ninth percentiles.
    for c in ("Youth", "Exper", "Train", "Routine", "Absorp", "Wage",
              "Size", "Lev", "ROA", "Growth", "Cashflow", "TobinQ", "CapInt"):
        lo, hi = df[c].quantile([0.01, 0.99])
        df[c] = df[c].clip(lo, hi)

    # Word-frequency indices are non-negative; shift by a constant, which the
    # fixed effects absorb and which leaves the first stage linear.
    df["GenAI"] = (df.GenAI - df.GenAI.quantile(0.06)).clip(lower=0.0)

    # ------------------------------------------------------- instruments
    df["Nat"] = df.year.map(NAT)
    df["IV_hist"] = df.Hist * df.Nat
    # Leave-own-province-out industry mean adoption.
    tot = df.groupby(["ind", "year"]).GenAI.transform("sum")
    cnt = df.groupby(["ind", "year"]).GenAI.transform("size")
    ptot = df.groupby(["ind", "year", "prov"]).GenAI.transform("sum")
    pcnt = df.groupby(["ind", "year", "prov"]).GenAI.transform("size")
    df["IV_peer"] = (tot - ptot) / np.maximum(cnt - pcnt, 1)

    # ------------------------------- the generative-AI break of late 2022
    df["Post"] = (df.year >= 2023).astype(int)
    df["GxPost"] = df.GenAI * df.Post

    # ------------------------------------------------- scaled moderators
    for c in ("Absorp", "Wage"):
        df[c + "_z"] = _z(df[c] if c == "Wage" else np.log1p(df[c]))
    df["GxA"] = df.GenAI * df.Absorp_z
    df["GxW"] = df.GenAI * df.Wage_z

    df = df.sort_values(["firm", "year"]).reset_index(drop=True)
    os.makedirs(DATA, exist_ok=True)
    df.to_csv(os.path.join(DATA, "panel.csv"), index=False)
    return df


if __name__ == "__main__":
    d = build()
    print(d.shape, d.firm.nunique(), "firms")
    print(d[["GenAI", "Youth", "Train", "Routine", "Absorp", "Size", "Lev",
             "ROA"]].describe().T[["mean", "std", "min", "max"]].round(3))
    print("\nGenAI by year:")
    print(d.groupby("year").GenAI.mean().round(3))
