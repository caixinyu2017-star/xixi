# -*- coding: utf-8 -*-
"""Firm-year panel used by the empirical section.

IMPORTANT — status of the data
------------------------------
The panel produced here is SYNTHETIC.  It is generated from a fully documented
data-generating process whose marginal moments are matched to the published
descriptive statistics of Chinese A-share listed firms and whose structure
reproduces the identification problem the paper has to solve (an unobserved
firm-level confounder that raises both generative-AI adoption and the youth
employment share, plus two excluded instruments).  Its purpose is to let the
estimation pipeline in `analysis/` be executed end to end, so that every number
in every table and figure of the manuscript is a genuine estimation output
rather than a hand-typed placeholder, and so that the design can be checked
before it is taken to the real CSMAR/Wind extraction.

The seed is fixed so that the panel, and therefore every reported estimate, is
exactly reproducible.

It is NOT real data and the manuscript must not be submitted with these tables.
Replace `panel.csv` with the real extraction and re-run `analysis/run_all.py`;
the table and figure files, and therefore the manuscript, regenerate unchanged
in structure.

Moment targets (Chinese A-share listed firms, from the published literature)
    Size   ln total assets                mean 22.42  sd 1.33
    ROE    net profit / equity            mean 0.061  sd 0.132
    Lev    total liabilities / assets     mean 0.421  sd 0.192
    Growth revenue growth                 mean 0.122  sd 0.370
    Age    ln(1 + years since founding)   mean 2.97   sd 0.31
    Board  ln board size                  mean 2.11   sd 0.20
    Indep  independent director share     mean 0.377  sd 0.054
    Dual   CEO duality                    mean 0.304
    TobinQ                                mean 2.00   sd 1.31
    Fixed  net fixed assets / assets      mean 0.192  sd 0.143
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "data"))
os.makedirs(OUT, exist_ok=True)

SEED = 202
YEARS = list(range(2016, 2026))     # 2016-2025
SHOCK_YEAR = 2023                   # first full reporting year after ChatGPT
N_FIRMS = 3400

# --- structural parameters of the data-generating process -------------------
TRUE = dict(
    # mediator equations
    a_RTI=-0.900,      # GenAI -> routine-task intensity (pp per unit)
    b_HCU=+0.620,      # GenAI -> human-capital upgrading (pp per unit)
    # outcome equation
    c_direct=-1.105,   # direct effect of GenAI on the youth share
    c_RTI=+0.320,      # routine-task intensity -> youth share
    c_HCU=+0.185,      # human-capital upgrading -> youth share
    d_OLC=+0.120,      # GenAI x organisational learning capability
    d_GOV=+0.330,      # GenAI x AI governance disclosure
    d_SOE=+0.520,      # GenAI x state ownership: the employment-stability
                       # mandate of state-owned enterprises blunts adjustment
    # confounding
    xi_on_genai=+0.55,
    xi_on_youth=+1.60,
    # time-varying confounder: a firm-year demand/expansion shock that raises
    # both generative-AI adoption and the hiring of young workers, and that
    # firm and year fixed effects therefore cannot absorb
    nu_on_genai=+0.40,
    nu_on_youth=+1.05,
)
TRUE["beta_total"] = (TRUE["c_direct"]
                      + TRUE["a_RTI"] * TRUE["c_RTI"]
                      + TRUE["b_HCU"] * TRUE["c_HCU"])


def _wins(x, lo=0.01, hi=0.99):
    a, b = np.nanquantile(x, lo), np.nanquantile(x, hi)
    return np.clip(x, a, b)


def build(seed=SEED, n_firms=N_FIRMS):
    rng = np.random.default_rng(seed)

    # ---------------- firm-level fixed characteristics ----------------------
    prov = rng.integers(0, 31, n_firms)
    ind = rng.integers(0, 18, n_firms)
    soe = (rng.random(n_firms) < 0.34).astype(float)
    east = (prov < 11).astype(float)                       # eastern provinces
    hitech = (rng.random(n_firms) < 0.42).astype(float)

    # province digital infrastructure, and the historical instrument that
    # predicts it (1984 fixed-telephone penetration per 100 people)
    phone84_p = rng.gamma(2.0, 1.1, 31) + 0.6 * (np.arange(31) < 11)
    digi_p = 0.55 * (phone84_p - phone84_p.mean()) / phone84_p.std() + rng.normal(0, 1, 31)
    phone84 = phone84_p[prov]
    digi = digi_p[prov]

    # unobserved firm-level "digital ambition": confounds adoption and youth
    xi = rng.normal(0, 1, n_firms)

    # ex-ante task exposure to generative AI (share-weighted occupational score).
    # Exposure has an industry component, which is what makes the leave-one-out
    # peer instrument relevant.
    ind_exposure = rng.normal(0, 0.125, 18)
    exposure = (0.44 + ind_exposure[ind] + 0.055 * hitech + 0.03 * east
                + 0.055 * rng.normal(0, 1, n_firms))
    exposure = np.clip(exposure, 0.08, 0.92)

    # organisational learning capability (standardised training intensity).
    # It is drawn independently of industry task exposure and of regional
    # digital infrastructure, so that neither excluded instrument shifts a
    # sub-population with a systematically different treatment effect; this
    # keeps the two instruments identifying the same estimand and makes the
    # overidentification test informative about exclusion rather than about
    # effect heterogeneity.
    olc = rng.normal(0, 1, n_firms)
    olc = (olc - olc.mean()) / olc.std()

    # AI governance disclosure propensity (firm level, time varying below)
    gov_lat = 0.30 * soe + 0.35 * olc + rng.normal(0, 1, n_firms)

    mu_y = rng.normal(0, 6.2, n_firms)      # firm effect, youth share
    mu_r = rng.normal(0, 5.0, n_firms)      # firm effect, routine intensity
    mu_h = rng.normal(0, 6.0, n_firms)      # firm effect, human capital
    size0 = 22.42 + 1.15 * rng.normal(0, 1, n_firms) + 0.28 * soe
    age0 = 2.60 + 0.30 * rng.normal(0, 1, n_firms)

    # ---------------- national shifter for the shift-share instrument -------
    # national generative-AI diffusion index, rebased so that it equals one in
    # every pre-shock year: the technology did not exist before 2023, so the
    # shifter -- and therefore the shift-share instrument -- is flat until then
    _rev = dict(zip(YEARS, [1.0, 1.28, 1.62, 2.05, 2.55, 3.20, 4.05,
                            5.30, 7.40, 9.60]))
    ai_rev = {y: max(1.0, _rev[y] / _rev[SHOCK_YEAR - 1]) for y in YEARS}

    rows = []
    for k, t in enumerate(YEARS):
        alive = rng.random(n_firms) < (0.90 + 0.008 * k)   # unbalanced panel
        disclose = rng.random(n_firms) < 0.86              # age composition disclosed
        keep = alive & disclose
        idx = np.where(keep)[0]
        n = idx.size

        # ---- covariates --------------------------------------------------
        size = size0[idx] + 0.055 * k + rng.normal(0, 0.32, n)
        lev = np.clip(0.421 + 0.16 * rng.normal(0, 1, n) + 0.03 * soe[idx], 0.03, 0.95)
        roe = 0.061 + 0.125 * rng.normal(0, 1, n) - 0.010 * k / 9
        growth = 0.122 + 0.35 * rng.normal(0, 1, n)
        age = age0[idx] + np.log1p(k) * 0.10 + rng.normal(0, 0.05, n)
        board = 2.11 + 0.19 * rng.normal(0, 1, n)
        indep = np.clip(0.377 + 0.052 * rng.normal(0, 1, n), 0.30, 0.65)
        dual = (rng.random(n) < 0.304).astype(float)
        tobinq = np.clip(2.00 + 1.25 * rng.normal(0, 1, n), 0.6, 18.0)
        fixed = np.clip(0.192 + 0.135 * rng.normal(0, 1, n), 0.002, 0.85)

        # ---- generative-AI adoption intensity ------------------------------
        # essentially zero before the shock; afterwards it scales with ex-ante
        # task exposure, firm size, regional digital infrastructure and the
        # unobserved digital ambition xi
        post = 1.0 if t >= SHOCK_YEAR else 0.0
        nu = rng.normal(0, 1, n)          # time-varying confounder
        depth = {2023: 1.00, 2024: 1.45, 2025: 1.72}.get(t, 0.0)
        lat = (-1.15 + 2.35 * exposure[idx]
               + 0.28 * (size - size.mean()) / size.std()
               + 0.95 * digi[idx] / 3 + TRUE["xi_on_genai"] * xi[idx]
               + 0.30 * hitech[idx] + TRUE["nu_on_genai"] * nu
               + rng.normal(0, 0.45, n))
        # the vocabulary is absent from annual reports before the shock, and
        # the disclosure index is bounded above, so the measure is censored at
        # both ends by construction rather than by ex post winsorisation
        genai = post * depth * np.clip(lat + 1.35, 0, 2.80)

        # ---- mediators -----------------------------------------------------
        rti = (42.0 + mu_r[idx] - 0.9 * k
               + TRUE["a_RTI"] * genai
               - 3.1 * hitech[idx] + 2.0 * soe[idx]
               + 1.6 * (size - 22.4) + rng.normal(0, 4.4, n))
        rti = np.clip(rti, 3, 92)

        hcu = (38.0 + mu_h[idx] + 0.85 * k
               + TRUE["b_HCU"] * genai
               + 7.5 * hitech[idx] + 3.2 * (size - 22.4) + 2.4 * olc[idx]
               + rng.normal(0, 5.2, n))
        hcu = np.clip(hcu, 4, 96)

        # ---- AI governance disclosure (drawn before the outcome so that it
        # ---- can moderate the effect of adoption) ---------------------------
        # disclosure propensity is predetermined with respect to the
        # outcome and does not respond to the firm's own adoption, so the
        # moderator in H5 is not a bad control
        aigov0 = ((gov_lat[idx] + 0.9 * post
                   + rng.normal(0, 1, n)) > 1.15).astype(float)

        # ---- outcome: share of employees aged 30 or below (%) --------------
        youth = (24.5 + mu_y[idx] - 0.42 * k
                 + TRUE["c_direct"] * genai
                 + TRUE["d_OLC"] * genai * olc[idx] * 4.0
                 + TRUE["d_GOV"] * genai * aigov0
                 + TRUE["d_SOE"] * genai * soe[idx]
                 + TRUE["c_RTI"] * (rti - 42.0)
                 + TRUE["c_HCU"] * (hcu - 38.0)
                 + TRUE["xi_on_youth"] * xi[idx]
                 + TRUE["nu_on_youth"] * nu
                 - 2.6 * soe[idx] + 1.9 * hitech[idx]
                 - 1.7 * (age - 2.97) + 0.9 * (size - 22.4) - 2.2 * lev
                 + rng.normal(0, 4.6, n))
        youth = np.clip(youth, 1.0, 78.0)

        youth35 = np.clip(youth * 1.62 + rng.normal(0, 2.0, n), 2.0, 92.0)
        n_emp = np.exp(6.6 + 0.75 * (size - 22.4) + rng.normal(0, 0.45, n))
        ln_young = np.log1p(n_emp * youth / 100.0)

        aigov = aigov0

        rows.append(pd.DataFrame(dict(
            firm=idx, year=t, prov=prov[idx], ind=ind[idx],
            Youth=youth, Youth35=youth35, LnYoung=ln_young,
            GenAI=genai, Exposure=exposure[idx], Post=post,
            RTI=rti, HCU=hcu, OLC=olc[idx], AIGov=aigov, Digi=digi[idx],
            Phone84=phone84[idx], AIrev=ai_rev[t],
            SOE=soe[idx], HiTech=hitech[idx], East=east[idx],
            Size=size, Lev=lev, ROE=roe, Growth=growth, Age=age,
            Board=board, Indep=indep, Dual=dual, TobinQ=tobinq, Fixed=fixed,
        )))

    df = pd.concat(rows, ignore_index=True)

    # keep firms observed at least four years and at least twice before the shock
    g = df.groupby("firm")["year"]
    ok = g.count() >= 4
    pre = df[df.year < SHOCK_YEAR].groupby("firm")["year"].count() >= 2
    keep = ok.index[ok.reindex(ok.index, fill_value=False)
                    & pre.reindex(ok.index, fill_value=False)]
    df = df[df.firm.isin(keep)].copy()

    # winsorise continuous variables at the 1st and 99th percentiles
    for c in ["Youth", "Youth35", "LnYoung", "RTI", "HCU", "Size", "Lev", "ROE",
              "Growth", "Age", "Board", "Indep", "TobinQ", "Fixed"]:
        df[c] = _wins(df[c].values)

    # instruments
    df["IV_Bartik"] = (df.Phone84 - df.Phone84.mean()) / df.Phone84.std() * np.log(df.AIrev)
    loo = (df.groupby(["ind", "prov", "year"])["GenAI"].transform("sum")
           - df.GenAI) / np.maximum(
        df.groupby(["ind", "prov", "year"])["GenAI"].transform("count") - 1, 1)
    df["IV_Peer"] = loo.fillna(0.0)

    # firm-level treatment indicator for the matching estimators
    postmean = (df[df.year >= SHOCK_YEAR].groupby("firm")["GenAI"].mean()
                .rename("PostGenAI"))
    df = df.merge(postmean, on="firm", how="left")
    df["PostGenAI"] = df["PostGenAI"].fillna(0.0)
    df["Treat"] = (df["PostGenAI"] > df["PostGenAI"].median()).astype(float)
    df["DID"] = df["Treat"] * df["Post"]
    df["ExpPost"] = df["Exposure"] * df["Post"]

    df = df.sort_values(["firm", "year"]).reset_index(drop=True)
    return df


if __name__ == "__main__":
    d = build()
    d.to_csv(os.path.join(OUT, "panel.csv"), index=False)
    print("firms", d.firm.nunique(), "obs", len(d), "years",
          d.year.min(), "-", d.year.max())
    print(d[["Youth", "GenAI", "RTI", "HCU", "Size", "ROE", "Lev", "Growth",
             "Age", "Board", "Indep", "Dual", "TobinQ", "Fixed"]]
          .describe().T[["count", "mean", "std", "min", "max"]].round(3))
    print("\ntrue total effect of GenAI on Youth:",
          round(TRUE["beta_total"], 4))
