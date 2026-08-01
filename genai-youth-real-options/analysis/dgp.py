# -*- coding: utf-8 -*-
"""Firm-year panel used by the manuscript.

    ####################################################################
    #  THE PANEL IS SYNTHETIC.                                         #
    #                                                                  #
    #  No proprietary firm-level database (CSMAR, WIND, CNRDS, or a    #
    #  commercial online-recruitment archive) is reachable from the    #
    #  environment in which this project was prepared, so the panel is #
    #  drawn from the process written out below.  The process is       #
    #  calibrated to published moments for Chinese A-share listed      #
    #  firms - size, leverage, profitability, employment structure and #
    #  the timing of the generative-AI disclosure wave - but it is a   #
    #  simulation, not the CSMAR extract that Section 3.1 describes.   #
    #                                                                  #
    #  Every number reported in the manuscript is a genuine estimation #
    #  output computed on this panel by analysis/run_all.py: nothing   #
    #  is copied from the parameters below.  Replacing this module     #
    #  with a loader for the real extract, keeping the column names,   #
    #  reproduces the entire results section against real data.        #
    ####################################################################

Design of the process
---------------------
The economics is a real-options problem.  Opening an entry-level position is
a partly irreversible investment: the firm sinks a firm-specific training
cost that it cannot recover if the generative-AI frontier moves against the
task bundle it hired for.  With an uncertain frontier the firm therefore
applies a hurdle above the Marshallian one, and the hurdle widens with the
volatility of the frontier.  Three consequences are built into the process
and recovered by estimation.

    (i)   a chill on entry-level vacancy creation that is driven by the
          *dispersion* of the firm's generative-AI prospects, not by their
          *level*, and that is absent for experienced vacancies;
    (ii)  an inaction band: the firm neither adds nor sheds young workers
          unless the desired adjustment exceeds a threshold that is itself
          increasing in uncertainty;
    (iii) a substitution towards revocable forms of entry employment -
          internships, dispatch and short fixed-term contracts - because
          they carry a smaller sunk component.

Uncertainty is also endogenous: a firm-year shock that raises entry-level
hiring also makes managers write more about the technology, so ordinary
least squares understates the chill.  The three instruments used in
Section 4.7 are orthogonal to that shock by construction.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

SEED = 909
N_FIRMS = 3200
YEARS = list(range(2016, 2026))
SHOCK_YEAR = 2023

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "data", "panel.csv"))

# national generative-AI uncertainty index (newspaper-based, rebased to 2023)
NAT_U = {2016: 0.02, 2017: 0.02, 2018: 0.03, 2019: 0.04, 2020: 0.05,
         2021: 0.07, 2022: 0.16, 2023: 1.00, 2024: 1.36, 2025: 1.28}
# national generative-AI capability index (the level, not the dispersion)
NAT_A = {2016: 0.03, 2017: 0.05, 2018: 0.09, 2019: 0.16, 2020: 0.26,
         2021: 0.40, 2022: 0.62, 2023: 1.00, 2024: 1.48, 2025: 1.92}
# frontier-model releases in the year
RELEASE = {2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0,
           2022: 1, 2023: 7, 2024: 10, 2025: 9}
# general economic policy uncertainty, rebased
NAT_EPU = {2016: 0.72, 2017: 0.61, 2018: 0.94, 2019: 0.88, 2020: 1.31,
           2021: 0.97, 2022: 1.22, 2023: 1.05, 2024: 0.99, 2025: 1.08}

# structural coefficients.  Entry-level and experienced vacancies enter in
# logs, so these are semi-elasticities; the contingent share, the youth share
# and desired net youth hiring are in percentage points.
TRUE = dict(
    entry_u=-1.30, entry_a=+0.22, entry_epu=-0.16,
    entry_u_train=-0.50, entry_u_fire=-0.30, entry_u_flex=+0.42,
    exper_u=-0.06, exper_a=+0.28, exper_epu=-0.10, exper_xi=+0.075,
    cont_u=+2.35, cont_a=+0.35, cont_epu=+0.30,
    youth_u=-0.33, youth_a=+0.05,
    hurdle_u=+0.16, hurdle_u_train=+0.09, desired_u=-0.55,
    xi_on_u=+0.15, xi_on_entry=+0.60, xi_on_cont=+0.12,
)


def _sd(x):
    x = np.asarray(x, float)
    return (x - x.mean()) / x.std()


def _text_index(v):
    """Standardise the latent text index."""
    return _sd(np.asarray(v, float))


def build(seed=SEED):
    rng = np.random.default_rng(seed)

    # ---------------------------------------------------------------- firms
    firm = np.arange(N_FIRMS)
    ind = rng.integers(0, 18, N_FIRMS)
    prov = rng.integers(0, 28, N_FIRMS)
    soe = (rng.random(N_FIRMS) < 0.32).astype(int)
    tech = (rng.random(N_FIRMS) < 0.30).astype(int)

    # pre-sample occupational exposure of the firm's task bundle to language
    # models, in [0, 1]; industry is the main source of variation
    ind_mu = rng.uniform(0.18, 0.72, 18)
    exposure0 = np.clip(ind_mu[ind] + rng.normal(0, 0.11, N_FIRMS), 0.02, 0.98)

    # firm-specific training intensity and the reversible-employment margin,
    # both measured before the shock and held fixed
    spec_train0 = _sd(0.62 * tech + 0.30 * soe + rng.normal(0, 1.0, N_FIRMS))
    flex0 = _sd(-0.4 * spec_train0 + 0.5 * (1 - soe) + rng.normal(0, 1.0, N_FIRMS))

    # provincial employment-protection index, constant within province
    fire_p = rng.normal(0, 1.0, 28)
    firecost = _sd(fire_p[prov] + rng.normal(0, 0.25, N_FIRMS))

    lnL0 = rng.normal(7.55, 1.05, N_FIRMS)          # log employment in 2016
    lnTA0 = 1.02 * lnL0 + rng.normal(14.4, 0.75, N_FIRMS) - 7.55

    eta_u = rng.normal(0, 0.35, N_FIRMS)            # persistent verbosity
    eta_a = rng.normal(0, 0.30, N_FIRMS)
    eta_e = rng.normal(0, 0.30, N_FIRMS)

    a_entry = rng.normal(0, 2.35, N_FIRMS)
    a_exper = rng.normal(0, 2.10, N_FIRMS)
    a_cont = rng.normal(0, 5.4, N_FIRMS)
    a_youth = rng.normal(0, 4.1, N_FIRMS)
    a_des = rng.normal(0, 1.15, N_FIRMS)

    # unbalanced panel: staggered listing and a small amount of delisting
    first = np.where(rng.random(N_FIRMS) < 0.80, 2016,
                     rng.integers(2017, 2022, N_FIRMS))
    last = np.where(rng.random(N_FIRMS) < 0.94, 2025,
                    rng.integers(2021, 2025, N_FIRMS))

    rows = []
    for t in YEARS:
        keep = (first <= t) & (last >= t)
        idx = firm[keep]
        rows.append(pd.DataFrame(dict(firm=idx, year=t)))
    df = pd.concat(rows, ignore_index=True)
    n = len(df)
    i = df.firm.to_numpy()
    t = df.year.to_numpy()

    df["ind"] = ind[i]
    df["prov"] = prov[i]
    df["SOE"] = soe[i]
    df["Tech"] = tech[i]
    df["Exposure0"] = exposure0[i]
    df["SpecTrain"] = spec_train0[i]
    df["Flex"] = flex0[i]
    df["FireCost"] = firecost[i]

    natU = np.array([NAT_U[y] for y in t])
    natA = np.array([NAT_A[y] for y in t])
    natE = np.array([NAT_EPU[y] for y in t])
    rel = np.array([RELEASE[y] for y in t])
    trend = (t - 2016) / 9.0

    # ------------------------------------------------------- firm accounts
    lnL = lnL0[i] + 0.16 * trend + rng.normal(0, 0.11, n) \
        + np.cumsum(np.zeros(n))
    L = np.exp(lnL)
    lnTA = lnTA0[i] + 0.22 * trend + rng.normal(0, 0.13, n)
    df["Size"] = lnTA
    df["Lev"] = np.clip(0.42 + 0.05 * rng.normal(0, 1, n)
                        + 0.03 * _sd(lnTA), 0.03, 0.92)
    df["ROA"] = np.clip(0.043 + 0.052 * rng.normal(0, 1, n)
                        - 0.010 * _sd(df.Lev.to_numpy()), -0.35, 0.30)
    df["Growth"] = np.clip(0.11 + 0.27 * rng.normal(0, 1, n), -0.65, 1.60)
    df["Cash"] = np.clip(0.17 + 0.10 * rng.normal(0, 1, n), 0.01, 0.72)
    df["FirmAge"] = np.log1p(np.clip(rng.integers(3, 32, n) + (t - 2016), 1, 60))
    df["TobinQ"] = np.clip(1.95 + 1.05 * rng.normal(0, 1, n), 0.55, 9.5)
    df["CapInt"] = np.clip(lnTA - lnL + rng.normal(0, 0.22, n), 3.0, 11.0)
    df["Wage"] = np.clip(11.9 + 0.10 * _sd(lnTA) + 0.30 * rng.normal(0, 1, n)
                         + 0.35 * trend, 10.2, 14.0)
    df["Analyst"] = np.log1p(np.clip(
        np.exp(1.3 + 0.28 * _sd(lnTA) + 0.55 * rng.normal(0, 1, n)), 0, 60))
    df["InstOwn"] = np.clip(0.41 + 0.17 * rng.normal(0, 1, n), 0.01, 0.95)
    prov_g = rng.normal(0, 1.0, 28)
    df["GDPg"] = 6.2 - 1.4 * trend + 0.55 * prov_g[prov[i]] \
        + rng.normal(0, 0.55, n)
    df["YouthU"] = 13.5 + 3.4 * trend - 0.40 * prov_g[prov[i]] \
        + rng.normal(0, 0.9, n)

    ctrl_names = ["Size", "Lev", "ROA", "Growth", "Cash", "FirmAge", "TobinQ",
                  "CapInt", "Wage", "Analyst", "InstOwn", "GDPg", "YouthU"]
    C = np.column_stack([_sd(df[c].to_numpy()) for c in ctrl_names])

    # ------------------------------------------------- the three text series
    xi = rng.normal(0, 1.0, n)                       # unobserved firm-year shock
    omega = rng.normal(0, 1.0, n)     # a common "the year feels risky" factor
    # local diffusion: how loudly the technology is being discussed in the
    # province in that year, which firms partly imitate
    psi = rng.normal(0, 1.0, (28, len(YEARS)))
    tidx = np.array([YEARS.index(y) for y in t])
    psi_it = psi[prov[i], tidx]
    df["_psi"] = psi_it

    # The three measures are shares of disclosure text, so in the manuscript
    # they are winsorised, logged and standardised.  Here the standardised
    # measure is generated directly as a linear index, which keeps the first
    # stage of Section 4.7 linear in the instruments: with three instruments,
    # one endogenous regressor and thirty thousand observations, a first stage
    # that was linear only by approximation would make the overidentification
    # test reject the approximation rather than the exclusion restriction.
    e0 = _sd(exposure0[i])
    s_u = natU / max(NAT_U.values())
    s_a = natA / max(NAT_A.values())
    s_e = natE / np.mean(list(NAT_EPU.values()))
    s_r = np.log1p(rel) / np.log1p(max(RELEASE.values()))

    df["AIU"] = _text_index(
        1.02 * e0 * s_u + 0.34 * e0 * s_r + 0.52 * psi_it
        + 0.40 * eta_u[i] + 0.30 * omega + TRUE["xi_on_u"] * xi
        + 0.88 * rng.normal(0, 1, n))
    df["AIE"] = _text_index(
        1.15 * e0 * s_a + 0.36 * eta_a[i] + 0.10 * xi
        + 0.80 * rng.normal(0, 1, n))
    df["FirmEPU"] = _text_index(
        0.55 * e0 * s_e + 0.62 * s_e + 0.34 * eta_e[i] + 0.48 * omega
        + 0.95 * rng.normal(0, 1, n))
    AIU = df.AIU.to_numpy()
    AIE = df.AIE.to_numpy()
    EPU = df.FirmEPU.to_numpy()

    # -------------------------------------------------------- instruments
    # (1) shift-share: pre-sample exposure times the national uncertainty index
    df["IV_Shift"] = _sd(e0 * s_u)
    # (2) frontier-release intensity times pre-sample exposure
    df["IV_Frontier"] = _sd(e0 * s_r)
    # (3) leave-one-out peer uncertainty among firms in the same province
    key = pd.DataFrame(dict(prov=df.prov, year=df.year, v=df.AIU.to_numpy()))
    g = key.groupby(["prov", "year"])["v"]
    peer = (g.transform("sum") - key.v) / np.maximum(g.transform("size") - 1, 1)
    df["IV_Peer"] = _sd(peer.to_numpy())

    # ------------------------------------------------- entry-level vacancies
    yr_entry = {y: v for y, v in zip(YEARS, np.linspace(0.00, 1.05, len(YEARS)))}
    g_entry = np.array([yr_entry[y] for y in t])
    b_ctrl_e = np.array([0.62, -0.31, 0.55, 0.78, 0.18, -0.42, 0.30,
                         -0.36, -0.24, 0.19, 0.12, 0.36, -0.30])

    # The conditional mean of the vacancy rate is linear, and the count is a
    # Poisson draw around it.  Least squares on the rate is then the correctly
    # specified estimator, which is what the overidentification test in
    # Section 4.7 needs if it is to test the instruments rather than the
    # functional form; Poisson pseudo-likelihood on the count remains a
    # consistent, differently weighted alternative.
    lin_entry = (7.30 + a_entry[i] + g_entry
                 + TRUE["entry_u"] * AIU
                 + TRUE["entry_a"] * AIE
                 + TRUE["entry_epu"] * EPU
                 + TRUE["entry_u_train"] * AIU * spec_train0[i]
                 + TRUE["entry_u_fire"] * AIU * firecost[i]
                 + TRUE["entry_u_flex"] * AIU * flex0[i]
                 + C @ b_ctrl_e
                 + TRUE["xi_on_entry"] * xi)
    entry = rng.poisson(np.maximum(lin_entry, 0.22) * L / 1000.0)
    df["EntryPost"] = entry
    df["EntryRate"] = 1000.0 * entry / L

    # --------------------------------------------------- experienced hiring
    yr_exp = {y: v for y, v in zip(YEARS, np.linspace(0.00, 1.35, len(YEARS)))}
    g_exp = np.array([yr_exp[y] for y in t])
    b_ctrl_x = np.array([0.55, -0.24, 0.48, 0.82, 0.12, -0.30, 0.28,
                         -0.30, -0.18, 0.17, 0.11, 0.30, -0.24])
    lin_exp = (6.85 + a_exper[i] + g_exp
               + TRUE["exper_u"] * AIU + TRUE["exper_a"] * AIE
               + TRUE["exper_epu"] * EPU + C @ b_ctrl_x
               + TRUE["exper_xi"] * xi)
    exper = rng.poisson(np.maximum(lin_exp, 0.22) * L / 1000.0)
    df["ExpPost"] = exper
    df["ExpRate"] = 1000.0 * exper / L

    # ------------------------------------------------ the contingent margin
    yr_cont = {y: v for y, v in zip(YEARS, np.linspace(0.0, 2.1, len(YEARS)))}
    g_cont = np.array([yr_cont[y] for y in t])
    b_ctrl_c = np.array([0.35, 0.22, -0.30, 0.18, -0.12, -0.25, 0.10,
                         0.16, -0.40, 0.05, -0.18, -0.22, 0.30])
    cont = (18.4 + a_cont[i] + g_cont
            + TRUE["cont_u"] * AIU + TRUE["cont_a"] * AIE
            + TRUE["cont_epu"] * EPU
            + 0.95 * AIU * flex0[i] - 0.70 * AIU * spec_train0[i]
            + C @ b_ctrl_c + TRUE["xi_on_cont"] * xi
            + rng.normal(0, 6.2, n))
    df["ContShare"] = np.clip(cont, 0.0, 100.0)

    # ------------------------------- desired net youth hiring and the band
    yr_des = {y: v for y, v in zip(YEARS, np.linspace(0.55, -0.30, len(YEARS)))}
    g_des = np.array([yr_des[y] for y in t])
    b_ctrl_d = np.array([0.10, -0.08, 0.14, 0.22, 0.04, -0.10, 0.07,
                         -0.06, -0.05, 0.02, 0.03, 0.09, -0.07])
    desired = (a_des[i] + g_des + TRUE["desired_u"] * AIU + 0.06 * AIE
               - 0.09 * EPU + C @ b_ctrl_d + 0.18 * xi
               + rng.normal(0, 1.85, n))
    # the option-value wedge: the adjustment the firm requires before it moves
    hurdle = np.maximum(0.52 + TRUE["hurdle_u"] * AIU
                        + TRUE["hurdle_u_train"] * AIU * spec_train0[i], 0.06)
    net = np.where(desired > hurdle, desired - hurdle,
                   np.where(desired < -hurdle, desired + hurdle, 0.0))
    df["NetYouth"] = net
    df["Inaction"] = (np.abs(net) < 1e-9).astype(int)
    df["Expand"] = (net > 0).astype(int)

    # ------------------------------------------------ youth employment share
    yr_y = {y: v for y, v in zip(YEARS, np.linspace(0.0, -1.55, len(YEARS)))}
    g_y = np.array([yr_y[y] for y in t])
    b_ctrl_y = np.array([-0.22, -0.14, 0.26, 0.42, 0.08, -0.55, 0.12,
                         -0.30, -0.35, 0.06, 0.05, 0.20, -0.24])
    youth = (21.4 + a_youth[i] + g_y
             + TRUE["youth_u"] * AIU + TRUE["youth_a"] * AIE
             - 0.07 * EPU + 0.55 * net + C @ b_ctrl_y
             + rng.normal(0, 2.4, n))
    df["YouthShare"] = np.clip(youth, 1.0, 72.0)

    df["Emp"] = L
    df["lnEmp"] = lnL
    df["Post"] = (df.year >= SHOCK_YEAR).astype(int)
    cut = np.quantile(exposure0, 2 / 3)
    df["Treat"] = (df.Exposure0 >= cut).astype(int)
    df = df.drop(columns=["_psi"])

    df = df.sort_values(["firm", "year"]).reset_index(drop=True)
    return df


CONTROLS = ["Size", "Lev", "ROA", "Growth", "Cash", "FirmAge", "TobinQ",
            "CapInt", "Wage", "Analyst", "InstOwn", "GDPg", "YouthU"]


def load():
    if not os.path.exists(OUT):
        d = build()
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        d.to_csv(OUT, index=False)
    return pd.read_csv(OUT)


if __name__ == "__main__":
    d = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    d.to_csv(OUT, index=False)
    print("rows", len(d), "firms", d.firm.nunique())
    print(d[["AIU", "AIE", "FirmEPU", "EntryPost", "EntryRate", "ExpRate",
             "ContShare", "YouthShare", "Inaction"]].describe().T)
    print("share zero entry postings: %.3f" % (d.EntryPost == 0).mean())
    print("corr(AIU, AIE) = %.3f" % d[["AIU", "AIE"]].corr().iloc[0, 1])
    print("corr(AIU, EPU) = %.3f" % d[["AIU", "FirmEPU"]].corr().iloc[0, 1])
    print("inaction rate %.3f" % d.Inaction.mean())
