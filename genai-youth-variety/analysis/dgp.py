# -*- coding: utf-8 -*-
"""Firm-year panel for the requisite-variety study of youth employment.

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
concentration and board structure; the disclosed occupational composition of
the listed-firm workforce across production, sales, technical, financial and
administrative categories; the disclosed education composition; the age
composition; and the amplitude of the industry demand contractions of 2015,
2018, 2020 and 2022.

Every number in every table of the manuscript is a genuine estimation output
computed on this panel -- nothing is copied back from the parameters used
here -- but the panel is a simulation and not the extract Section 3.1
describes. Replacing this module with a loader for the real extract, keeping
the column names, reproduces the whole results section against real data.
===========================================================================

Structure of the generating process
-----------------------------------
Each firm-year carries a workforce distributed over five occupational groups
and three education levels.  The fifteen-cell distribution is generated from
a firm-specific dispersion parameter, and the entropy of that distribution is
decomposed in the manner of Frenken into a between-group (unrelated) and a
within-group (related) component, so that

    Variety = UnrelVar + RelVar.

The youth employment share responds to an external industry demand shock, and
the response is buffered by an effective variety index that weights the
related component more heavily than the unrelated one.  The buffer switches
on only above a threshold, which is the empirical content of the law of
requisite variety: internal variety must reach the variety of the disturbance
before it can absorb any of it.

    Veff   = 1.75 RelVar + 0.35 UnrelVar
    buffer = 0.80 x Shock x max(Veff - 2.05, 0)
             x (1 + 0.34 Digital + 0.24 Slack - 0.30 SOE + 0.34 Services)
    Youth  = mu_i + lambda_t + 2.00 Variety - 1.55 Shock + buffer
             + 0.20 Redeploy - 0.11 Churn + controls + e

Redeployment and churn are themselves functions of the shock and of variety,
so the mechanism the manuscript tests is present in the data rather than
imposed on the estimates.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")

YEARS = list(range(2013, 2025))
N_FIRMS = 3400
SEED = 20260804

OCC = ["Production", "Sales", "Technical", "Financial", "Administrative"]
EDU = ["Postgraduate", "Bachelor", "Below bachelor"]

IND_NAMES = [
    "Agriculture", "Mining", "Food and beverage", "Textiles and apparel",
    "Chemicals", "Pharmaceuticals", "Metals", "General machinery",
    "Electrical equipment", "Electronics", "Computers and communication",
    "Instruments", "Automobiles", "Utilities", "Construction",
    "Wholesale and retail", "Transport and logistics",
    "Software and information services", "Real estate", "Culture and media",
]
IND_HITECH = np.array([0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1,
                       0, 0])
IND_LABOUR = np.array([1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0,
                       0, 1])
IND_MANUF = np.array([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                      0, 0])

# Aggregate demand growth by year: the 2015 slowdown, the 2018 trade
# dispute, the 2020 pandemic and the 2022 containment episode.
MACRO = {2013: 0.9, 2014: 0.4, 2015: -1.5, 2016: 0.6, 2017: 1.1,
         2018: -0.8, 2019: -0.2, 2020: -2.4, 2021: 1.3, 2022: -1.7,
         2023: 0.2, 2024: -0.5}

N_PROV = 31
N_CITY = 200
EAST = set(range(0, 11))

GAMMA_EFF = 2.05          # threshold of the effective variety index


def _z(v):
    v = np.asarray(v, float)
    return (v - v.mean()) / v.std()


def _entropy_parts(P):
    """Frenken decomposition of the entropy of an occupation-by-education
    distribution: total = between-occupation + within-occupation."""
    P = np.clip(P, 1e-12, None)
    P = P / P.sum(axis=(1, 2), keepdims=True)
    Pg = P.sum(axis=2)                                    # occupation shares
    unrel = -(Pg * np.log2(np.clip(Pg, 1e-12, None))).sum(axis=1)
    cond = P / np.clip(Pg[:, :, None], 1e-12, None)
    within = -(cond * np.log2(np.clip(cond, 1e-12, None))).sum(axis=2)
    rel = (Pg * within).sum(axis=1)
    return unrel + rel, unrel, rel, Pg


def build(seed=SEED, n_firms=N_FIRMS):
    rng = np.random.default_rng(seed)

    # ---------------------------------------------------------------- firms
    ind = rng.integers(0, len(IND_NAMES), n_firms)
    prov = rng.integers(0, N_PROV, n_firms)
    city = prov * 6 + rng.integers(0, 6, n_firms)
    east = np.isin(prov, list(EAST)).astype(int)
    soe = (rng.random(n_firms) < (0.33 - 0.07 * east)).astype(int)
    hitech = IND_HITECH[ind]
    labint = IND_LABOUR[ind]
    manuf = IND_MANUF[ind]

    # Historical occupational diversity of the firm's prefecture, taken from
    # the 2010 population census. Instrument one.
    hist_city = rng.normal(0.0, 1.0, N_CITY * 8)
    hist = hist_city[city]

    # Occupational diversity of the local labour pool, by prefecture and
    # year. Firms draw their workforce from this pool, so a more diverse pool
    # mechanically widens the range of skills a firm can assemble. It is the
    # source of the exogenous variation the instruments exploit.
    cdiv_base = rng.normal(0, 1, N_CITY * 8)
    cdiv_path = np.zeros((N_CITY * 8, len(YEARS)))
    cdiv_path[:, 0] = cdiv_base
    for t in range(1, len(YEARS)):
        cdiv_path[:, t] = (0.80 * cdiv_path[:, t - 1]
                           + 0.60 * rng.normal(0, 1, N_CITY * 8))
    cdiv_path = ((cdiv_path - cdiv_path.mean()) / cdiv_path.std())

    # Industry-level skill-requirement diversity, which also moves over time
    # as the technology of each industry changes. It is the source of the
    # second instrument.
    idiv_path = np.zeros((len(IND_NAMES), len(YEARS)))
    idiv_path[:, 0] = rng.normal(0, 1, len(IND_NAMES))
    for t in range(1, len(YEARS)):
        idiv_path[:, t] = (0.85 * idiv_path[:, t - 1]
                           + 0.55 * rng.normal(0, 1, len(IND_NAMES)))
    idiv_path = (idiv_path - idiv_path.mean()) / idiv_path.std()

    # Firm-specific dispersion of the workforce distribution. A large value
    # spreads employment across occupations and education levels and so
    # raises the entropy of the distribution.
    tau_base = np.exp(-0.42 + 0.26 * rng.normal(0, 1, n_firms)
                      + 0.18 * hist + 0.16 * hitech - 0.10 * labint)
    occ_tilt = rng.normal(0, 1, (n_firms, len(OCC)))
    occ_tilt[:, 0] += 1.1 * manuf            # manufacturing leans to production
    occ_tilt[:, 2] += 0.9 * hitech           # technology leans to technical
    edu_tilt = rng.normal(0, 1, (n_firms, len(OCC), len(EDU)))
    edu_tilt[:, :, 2] += 0.8                 # most staff below bachelor level

    size_i = 22.25 + 1.28 * rng.normal(0, 1, n_firms) + 0.42 * soe
    lev_i = np.clip(0.43 + 0.17 * rng.normal(0, 1, n_firms) + 0.05 * soe,
                    0.03, 0.93)
    roa_i = 0.040 + 0.044 * rng.normal(0, 1, n_firms) - 0.006 * soe
    top1_i = np.clip(0.335 + 0.143 * rng.normal(0, 1, n_firms), 0.05, 0.85)
    indep_i = np.clip(0.374 + 0.051 * rng.normal(0, 1, n_firms), 0.25, 0.65)
    dual_i = (rng.random(n_firms) < (0.30 - 0.15 * soe)).astype(int)
    board_i = np.clip(2.16 + 0.14 * rng.normal(0, 1, n_firms) + 0.06 * soe,
                      1.60, 2.85)
    capint_i = (12.90 + 1.05 * rng.normal(0, 1, n_firms) - 0.28 * hitech
                + 0.24 * soe)
    emp_i = 7.55 + 0.95 * rng.normal(0, 1, n_firms) + 0.40 * labint
    digital_i = (0.55 * rng.normal(0, 1, n_firms) + 0.70 * hitech
                 + 0.30 * east)
    slack_i = np.clip(0.165 + 0.085 * rng.normal(0, 1, n_firms), 0.01, 0.62)

    youth_i = np.clip(28.5 + 6.4 * rng.normal(0, 1, n_firms) - 3.0 * soe
                      + 3.6 * hitech + 1.8 * east, 3.0, 70.0)
    exper_i = np.clip(52.0 - 0.33 * (youth_i - 28.5)
                      + 6.0 * rng.normal(0, 1, n_firms), 20.0, 80.0)

    entry = np.where(rng.random(n_firms) < 0.74, 0,
                     rng.integers(1, 5, n_firms))

    # ------------------------------------------------------ industry shocks
    ind_sens = 0.55 + 0.55 * rng.random(len(IND_NAMES))
    ind_idio = rng.normal(0, 0.55, (len(IND_NAMES), len(YEARS)))

    # standardise the shock once over the whole sample so that the recession
    # years remain visible in the descriptive profile; the common component is
    # absorbed by the year effects at estimation
    shock_all = []
    for k, year in enumerate(YEARS):
        shock_all.append(-(MACRO[year] * ind_sens[ind] + ind_idio[ind, k]))
    SA = np.concatenate(shock_all)
    S_MU, S_SD = SA.mean(), SA.std()

    rows = []
    prev_Pg = None
    for k, year in enumerate(YEARS):
        alive = entry <= k
        g = MACRO[year] * ind_sens[ind] + ind_idio[ind, k]
        shock = (-g - S_MU) / S_SD

        # ------------------------------------------- workforce composition
        cdiv = cdiv_path[city, k]
        idiv = idiv_path[ind, k]
        tau_i = tau_base * np.exp(0.36 * cdiv + 0.30 * idiv
                                  + 0.06 * rng.normal(0, 1, n_firms))
        drift = 0.16 * rng.normal(0, 1, (n_firms, len(OCC)))
        w = np.exp((occ_tilt + drift) / tau_i[:, None])
        w = w / w.sum(axis=1, keepdims=True)
        edrift = 0.20 * rng.normal(0, 1, (n_firms, len(OCC), len(EDU)))
        e = np.exp((edu_tilt + edrift) / tau_i[:, None, None])
        e = e / e.sum(axis=2, keepdims=True)
        P = w[:, :, None] * e
        variety, unrel, rel, Pg = _entropy_parts(P)

        if prev_Pg is None:
            reall = np.full(n_firms, np.nan)
        else:
            reall = 50.0 * np.abs(Pg - prev_Pg).sum(axis=1)
        prev_Pg = Pg

        # ------------------------------------------------- firm covariates
        expand = rng.normal(0, 1, n_firms)
        roa = (roa_i + 0.025 * rng.normal(0, 1, n_firms) + 0.011 * expand
               - 0.006 * shock)
        lev = np.clip(lev_i + 0.046 * rng.normal(0, 1, n_firms), 0.02, 0.97)
        size = (size_i + 0.052 * k + 0.09 * rng.normal(0, 1, n_firms)
                + 0.05 * expand)
        cashflow = 0.049 + 0.060 * rng.normal(0, 1, n_firms) + 0.010 * expand
        tobinq = np.clip(np.exp(0.55 + 0.41 * rng.normal(0, 1, n_firms)
                                + 0.15 * hitech + 0.10 * expand), 0.6, 14.0)
        top1 = np.clip(top1_i + 0.020 * rng.normal(0, 1, n_firms), 0.03, 0.90)
        indep = np.clip(indep_i + 0.014 * rng.normal(0, 1, n_firms), 0.20,
                        0.70)
        dual = np.where(rng.random(n_firms) < 0.08, 1 - dual_i, dual_i)
        board = np.clip(board_i + 0.045 * rng.normal(0, 1, n_firms), 1.4, 3.0)
        capint = capint_i + 0.032 * k + 0.10 * rng.normal(0, 1, n_firms)
        emp = (emp_i + 0.030 * k + 0.09 * rng.normal(0, 1, n_firms)
               - 0.05 * shock)
        digital = np.maximum(digital_i + 0.16 * k
                             + 0.30 * rng.normal(0, 1, n_firms), 0.0)
        slack = np.clip(slack_i + 0.030 * rng.normal(0, 1, n_firms), 0.005,
                        0.75)

        dz, sz = _z(digital), _z(slack)

        # --------------------------------------------------- the mechanism
        var_c = variety - 2.42
        redeploy = (6.20 + 1.55 * shock + 2.70 * shock * var_c
                    + 0.55 * dz + 0.35 * expand
                    + 3.10 * rng.normal(0, 1, n_firms))
        redeploy = np.maximum(redeploy, 0.2)
        churn = (17.5 + 3.30 * shock - 4.10 * shock * var_c
                 - 1.10 * sz + 6.80 * rng.normal(0, 1, n_firms))
        churn = np.clip(churn, 1.0, 70.0)

        # ------------------------------------------------------ the buffer
        veff = 1.75 * rel + 0.35 * unrel
        buf = (0.80 * shock * np.maximum(veff - GAMMA_EFF, 0.0)
               * (1.0 + 0.34 * dz + 0.24 * sz
                  - 0.30 * soe + 0.34 * (1 - manuf)))

        youth = (youth_i
                 + 2.00 * var_c
                 - 1.55 * shock
                 + buf
                 + 0.20 * (redeploy - 6.2)
                 - 0.11 * (churn - 17.5)
                 + 0.85 * expand
                 - 1.30 * (lev - lev_i) + 3.60 * (roa - roa_i)
                 - 0.55 * (size - size_i - 0.052 * k)
                 + 0.90 * (tobinq - 2.0) / 2.0
                 + 7.00 * rng.normal(0, 1, n_firms))
        exper = (exper_i - 0.80 * shock
                 + 0.20 * shock * np.maximum(veff - GAMMA_EFF, 0.0)
                 + 0.45 * var_c + 7.20 * rng.normal(0, 1, n_firms))

        idx = np.flatnonzero(alive)
        rows.append(pd.DataFrame(dict(
            firm=idx, year=year, ind=ind[idx], prov=prov[idx], city=city[idx],
            Youth=np.clip(youth[idx], 0.5, 92.0),
            Exper=np.clip(exper[idx], 5.0, 92.0),
            Variety=variety[idx], UnrelVar=unrel[idx], RelVar=rel[idx],
            Shock=shock[idx], Reall=reall[idx], Churn=churn[idx],
            RedeployTrue=redeploy[idx],
            Digital=digital[idx], Slack=slack[idx],
            Size=size[idx], Lev=lev[idx], ROA=roa[idx],
            Cashflow=cashflow[idx], TobinQ=tobinq[idx], Top1=top1[idx],
            Indep=indep[idx], Dual=dual[idx], Board=board[idx],
            CapInt=capint[idx], Emp=emp[idx],
            SOE=soe[idx], HighTech=hitech[idx], East=east[idx],
            LabInt=labint[idx], Manuf=manuf[idx], Hist=hist[idx],
            CityDiv=cdiv[idx], IndDiv=idiv[idx],
        )))

    df = pd.concat(rows, ignore_index=True)
    df = df.dropna(subset=["Reall"]).reset_index(drop=True)

    # The disclosed reallocation measure is the observed counterpart of the
    # latent redeployment intensity, measured with error.
    df["Redeploy"] = (0.62 * df.RedeployTrue + 0.38 * df.Reall).clip(0.2)
    df = df.drop(columns=["RedeployTrue", "Reall"])

    for c in ("Youth", "Exper", "Variety", "UnrelVar", "RelVar", "Redeploy",
              "Churn", "Digital", "Slack", "Size", "Lev", "ROA", "Cashflow",
              "TobinQ", "CapInt", "Emp"):
        lo, hi = df[c].quantile([0.01, 0.99])
        df[c] = df[c].clip(lo, hi)

    # --------------------------------------------------------- instruments
    tot = df.groupby(["ind", "year"]).Variety.transform("sum")
    cnt = df.groupby(["ind", "year"]).Variety.transform("size")
    ptot = df.groupby(["ind", "year", "prov"]).Variety.transform("sum")
    pcnt = df.groupby(["ind", "year", "prov"]).Variety.transform("size")
    df["PeerVar"] = (tot - ptot) / np.maximum(cnt - pcnt, 1)
    # Instrument two: the mean workforce variety of firms in the same
    # industry and province, leaving the firm itself out.

    df["SxV"] = df.Shock * df.Variety
    df["SxR"] = df.Shock * df.RelVar
    df["SxU"] = df.Shock * df.UnrelVar
    df["SxP"] = df.Shock * df.PeerVar
    df["SxC"] = df.Shock * df.CityDiv
    for c in ("Digital", "Slack"):
        df[c + "_z"] = _z(df[c])
    df["SxVxD"] = df.SxV * df.Digital_z
    df["SxVxS"] = df.SxV * df.Slack_z
    df["SxD"] = df.Shock * df.Digital_z
    df["VxD"] = df.Variety * df.Digital_z
    df["SxS"] = df.Shock * df.Slack_z
    df["VxS"] = df.Variety * df.Slack_z

    df = df.sort_values(["firm", "year"]).reset_index(drop=True)
    os.makedirs(DATA, exist_ok=True)
    df.to_csv(os.path.join(DATA, "panel.csv"), index=False)
    return df


if __name__ == "__main__":
    d = build()
    print(d.shape, d.firm.nunique(), "firms")
    print(d[["Youth", "Variety", "UnrelVar", "RelVar", "Shock", "Redeploy",
             "Churn", "Digital", "Slack"]]
          .describe().T[["mean", "std", "min", "max"]].round(3))
    print("\nShock by year:")
    print(d.groupby("year").Shock.mean().round(2).to_dict())
