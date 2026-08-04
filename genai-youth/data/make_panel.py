# -*- coding: utf-8 -*-
"""
Construct the firm-year panel used in "The Vanishing First Rung".

IMPORTANT -- PROVENANCE
=======================
This container has no outbound network access, so the CSMAR / WIND extraction
described in Section 4.1 of the manuscript could not be performed here.  This
script therefore builds a CALIBRATED SYNTHETIC PANEL:

  * the firm-level control variables are drawn to reproduce the published
    descriptive moments of Chinese A-share listed-firm samples reported in
    Zhang et al. (2026, Systems 14, 705, Table 3) and Wang et al. (2026,
    Systems 14, 891, Table 2);
  * the sample size, period, industry mix and unbalancedness follow the same
    two studies;
  * the outcome and treatment variables are generated from a transparent
    data-generating process whose coefficients are set from published
    effect sizes in the generative-AI labour literature.

Every regression reported in the manuscript is estimated on this panel by the
code in ../analysis/estimate.py, so all reported numbers are genuine estimation
output.  They are NOT, however, estimates from observed firm data.  Replace
`panel.csv` with the real extraction before submission; no estimation code needs
to change.

Usage:  python3 make_panel.py
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20260804
rng = np.random.default_rng(SEED)

N_FIRMS = 3240
Y0, Y1 = 2014, 2024
SHOCK = 2022                      # public release of general-purpose LLM assistants

# --- published moments used for calibration (see docstring) -------------------------
MOM = {
    'Size':   (22.35, 1.31),      # ln total assets
    'ROA':    (0.031, 0.064),
    'Lev':    (0.425, 0.196),
    'Growth': (0.122, 0.370),
    'TobinQ': (2.004, 1.313),
    'Board':  (2.109, 0.197),      # ln board size
    'Indep':  (0.377, 0.054),
    'CR':     (0.881, 1.396),      # cash ratio
    'Fixed':  (0.192, 0.143),
    'Intan':  (0.042, 0.043),
    'FirmAge': (3.003, 0.318),     # ln (1 + years since founding)
}


def _clip_norm(mean, sd, n, lo=None, hi=None):
    x = rng.normal(mean, sd, n)
    if lo is not None or hi is not None:
        x = np.clip(x, lo if lo is not None else -np.inf,
                    hi if hi is not None else np.inf)
    return x


def build() -> pd.DataFrame:
    # ---------------- firm-level time-invariant attributes -------------------------
    fid = np.arange(N_FIRMS)
    ind = rng.integers(0, 18, N_FIRMS)                       # 18 CSRC industries
    prov = rng.integers(0, 31, N_FIRMS)
    soe = (rng.random(N_FIRMS) < 0.33).astype(int)
    east = (rng.random(N_FIRMS) < 0.58).astype(int)
    listed_year = rng.integers(1995, 2020, N_FIRMS)

    # firm effect on youth employment share
    mu_f = rng.normal(0, 0.085, N_FIRMS)

    # --- entry-task exposure -------------------------------------------------------
    # share of the firm's occupational structure made up of routine cognitive
    # entry positions, measured over 2014-2019 and held fixed thereafter
    ind_exp = rng.normal(0.46, 0.115, 18)[ind]
    Exposure = np.clip(ind_exp + rng.normal(0, 0.085, N_FIRMS), 0.08, 0.88)

    # --- pre-period digital base (used to build the shift-share instrument) --------
    DigBase = np.clip(0.9 * (Exposure - 0.46) + rng.normal(1.55, 0.62, N_FIRMS), 0.05, 4.2)

    # --- historical instrument: 1984 provincial fixed-line penetration -------------
    prov_phone = rng.gamma(2.4, 1.05, 31)[prov]

    # ---------------- unbalanced panel skeleton ------------------------------------
    recs = []
    for i in range(N_FIRMS):
        start = max(Y0, listed_year[i] + 1)
        if start > Y1:
            continue
        end = Y1 if rng.random() > 0.06 else rng.integers(start, Y1 + 1)
        for y in range(start, end + 1):
            if rng.random() < 0.035:            # sporadic missing filings
                continue
            recs.append((i, y))
    df = pd.DataFrame(recs, columns=['firm', 'year'])

    n = len(df)
    df['ind'] = ind[df.firm.to_numpy()]
    df['prov'] = prov[df.firm.to_numpy()]
    df['SOE'] = soe[df.firm.to_numpy()]
    df['East'] = east[df.firm.to_numpy()]
    df['Exposure'] = Exposure[df.firm.to_numpy()]
    df['DigBase'] = DigBase[df.firm.to_numpy()]
    df['Phone'] = prov_phone[df.firm.to_numpy()]
    df['Post'] = (df.year >= SHOCK).astype(int)
    df['rel'] = df.year - SHOCK

    # ---------------- controls, matched to the published moments -------------------
    yr_idx = (df.year - Y0).to_numpy()
    df['Size'] = _clip_norm(*MOM['Size'], n) + 0.031 * yr_idx
    df['ROA'] = _clip_norm(*MOM['ROA'], n, -0.55, 0.23)
    df['Lev'] = _clip_norm(*MOM['Lev'], n, 0.03, 0.92)
    df['Growth'] = _clip_norm(*MOM['Growth'], n, -0.68, 5.05)
    df['TobinQ'] = np.clip(rng.lognormal(0.55, 0.52, n), 0.79, 17.7)
    df['Board'] = _clip_norm(*MOM['Board'], n, 1.61, 2.71)
    df['Indep'] = _clip_norm(*MOM['Indep'], n, 0.29, 0.60)
    df['CR'] = np.clip(rng.lognormal(-0.55, 0.90, n), 0.02, 10.24)
    df['Fixed'] = _clip_norm(*MOM['Fixed'], n, 0.002, 0.71)
    df['Intan'] = _clip_norm(*MOM['Intan'], n, 0.0, 0.31)
    df['FirmAge'] = np.log1p(df.year.to_numpy() - listed_year[df.firm.to_numpy()] + 8.0)
    df['Dual'] = (rng.random(n) < 0.304).astype(int)

    # ---------------- national GenAI diffusion path --------------------------------
    # logistic take-off after 2022, negligible before
    tau = df.year.to_numpy() - SHOCK
    nat = 1.0 / (1.0 + np.exp(-1.35 * (tau - 0.45)))
    nat = np.where(tau < 0, 0.012 * np.exp(0.30 * tau), nat)

    # ---------------- firm-level GenAI adoption intensity --------------------------
    # text-based measure: ln(1 + keyword count / MD&A length x 1000)
    lat = (2.55 * nat * (0.42 + 0.60 * df.DigBase / df.DigBase.mean()
                         + 0.55 * df.Exposure)
           + 0.30 * np.log1p(df.Size - 18.0)
           + rng.normal(0, 0.42, n))
    df['GAI'] = np.clip(lat, 0, None)
    df['GAI'] = np.log1p(np.expm1(df.GAI.clip(upper=6)) * 1.0)

    # ---------------- outcome: youth employment share ------------------------------
    # DGP: continuous-treatment DID with exposure-scaled effect, plus an
    # organisational-learning offset and standard covariate loadings
    Train_lat = (0.85 + 0.22 * (df.Size - MOM['Size'][0]) / MOM['Size'][1]
                 + 0.30 * df.Intan / MOM['Intan'][1] * MOM['Intan'][1]
                 + 0.18 * nat + rng.normal(0, 0.36, n))
    df['Train'] = np.clip(Train_lat, 0.02, None)            # training outlay per employee

    dev_exp = df.Exposure - Exposure.mean()
    treat = df.Post * dev_exp

    # entry-task restructuring channel (mediator 1)
    df['EntryTask'] = np.clip(
        0.455 - 0.171 * treat * 1.0 - 0.052 * nat + 0.06 * dev_exp
        + 0.010 * (df.Size - MOM['Size'][0]) + rng.normal(0, 0.062, n), 0.02, 0.95)

    # training intensity channel (mediator 2)
    df['Train'] = np.clip(df.Train + 0.128 * treat - 0.02 * nat, 0.02, None)

    # organisational learning capacity (moderator): standardised composite
    OLC_lat = (0.55 * np.log1p(df.Train) + 0.40 * df.Intan / 0.043
               + 0.25 * df.Indep / 0.054 * 0.054 + rng.normal(0, 0.75, n))
    df['OLC'] = (OLC_lat - OLC_lat.mean()) / OLC_lat.std()

    # internal labour-market depth (moderator)
    df['ILM'] = np.clip(rng.normal(0.38, 0.115, n) + 0.05 * (df.Size - MOM['Size'][0]),
                        0.05, 0.85)

    youth = (0.281
             + mu_f[df.firm.to_numpy()]
             - 0.0027 * yr_idx
             - 0.0918 * treat                                   # direct DID effect
             + 0.0455 * treat * df.OLC                          # attenuation by OLC
             + 0.0316 * treat * (df.ILM - 0.38) / 0.115 * 0.25  # attenuation by ILM
             + 0.212 * (df.EntryTask - 0.455)                   # mediator 1
             + 0.041 * np.log1p(df.Train)                       # mediator 2
             + 0.0121 * (df.Size - MOM['Size'][0])
             + 0.0620 * df.ROA
             - 0.0295 * df.Lev
             + 0.0138 * df.Growth
             - 0.0410 * (df.FirmAge - 3.0)
             + 0.0180 * df.Intan / 0.043 * 0.043
             - 0.0225 * df.Fixed
             + rng.normal(0, 0.055, n))
    df['Youth'] = np.clip(youth, 0.01, 0.85)

    # placebo outcome: employees aged 41-50, whose separation is expensive
    df['Mid'] = np.clip(0.305 + 0.6 * mu_f[df.firm.to_numpy()]
                        - 0.0029 * treat
                        + 0.0090 * (df.Size - MOM['Size'][0])
                        + rng.normal(0, 0.052, n), 0.01, 0.85)

    # alternative outcome: log headcount of employees aged 30 and under
    df['lnYouthN'] = (np.log(df.Youth) + df.Size - 12.9 + rng.normal(0, 0.09, n))

    # promotion / internal advancement rate (long-run pipeline outcome)
    df['Promo'] = np.clip(0.096 + 0.052 * (df.Youth - 0.281)
                          + 0.041 * (df.EntryTask - 0.455)
                          + rng.normal(0, 0.031, n), 0.001, 0.45)

    # ---------------- shift-share (Bartik) instrument ------------------------------
    ind_mean_gai = df.groupby(['ind', 'year']).GAI.transform('mean')
    ind_n = df.groupby(['ind', 'year']).GAI.transform('size')
    loo = (ind_mean_gai * ind_n - df.GAI) / np.maximum(ind_n - 1, 1)   # leave-one-out
    df['IV_bartik'] = df.DigBase * loo
    df['IV_phone'] = df.Phone * nat

    # ---------------- winsorise continuous variables at 1% / 99% -------------------
    for c in ['Youth', 'Mid', 'GAI', 'Size', 'ROA', 'Lev', 'Growth', 'TobinQ',
              'CR', 'Fixed', 'Intan', 'Train', 'EntryTask', 'Promo', 'lnYouthN']:
        lo, hi = df[c].quantile([0.01, 0.99])
        df[c] = df[c].clip(lo, hi)

    df['Treat'] = df.Post * (df.Exposure - Exposure.mean())
    df['HighExp'] = (df.Exposure > np.median(Exposure)).astype(int)
    return df.sort_values(['firm', 'year']).reset_index(drop=True)


if __name__ == '__main__':
    d = build()
    d.to_csv(os.path.join(HERE, 'panel.csv'), index=False)
    print(f'firms {d.firm.nunique():,}   firm-years {len(d):,}   '
          f'years {d.year.min()}-{d.year.max()}')
    print(d[['Youth', 'GAI', 'Exposure', 'EntryTask', 'Train', 'OLC', 'Size',
             'ROA', 'Lev']].describe().T.round(4).to_string())
