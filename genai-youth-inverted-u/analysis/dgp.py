# -*- coding: utf-8 -*-
"""Firm-year panel used by the empirical section.

IMPORTANT — status of the data
------------------------------
The panel produced here is SYNTHETIC.  It is generated from a fully documented
data-generating process whose marginal moments are matched to the published
descriptive statistics of Chinese A-share listed firms and whose structure
reproduces the identification problem the paper has to solve: an inverted
U-shaped structural relationship, three moderators that displace its turning
point, an unobserved firm-level confounder that raises both adoption depth and
the youth employment share, a time-varying demand shock, and two excluded
instruments.  Its purpose is to let the estimation pipeline in `analysis/` be
executed end to end, so that every number in every table and figure of the
manuscript is a genuine estimation output rather than a hand-typed placeholder.

The seed is fixed so that the panel, and therefore every reported estimate, is
exactly reproducible.

It is NOT real data and the manuscript must not be submitted with these tables.
Replace `panel.csv` with the real extraction and re-run `analysis/run_all.py`;
the table and figure files, and therefore the manuscript, regenerate unchanged
in structure.

Structure of the outcome equation
    Youth = 0.34 x AUG - 0.58 x AUT + moderation + controls + confounders
where the two channels are themselves functions of adoption depth,
    AUG = 9.576 AI - 0.679 AI^2   (increasing, concave: augmentation saturates)
    AUT = 2.114 AI + 0.809 AI^2   (increasing, convex: automation accelerates)
so that the reduced-form relationship between adoption depth and the youth
share is inverted U-shaped, with a turning point at 1.45 and a zero crossing at
2.90 for a firm at the mean of the three moderators.

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

SEED = 606
YEARS = list(range(2016, 2026))     # 2016-2025
SHOCK_YEAR = 2023                   # first full reporting year after ChatGPT
N_FIRMS = 3400

# --- structural parameters of the data-generating process -------------------
TRUE = dict(
    # channel equations, in adoption depth
    aug_lin=+9.576, aug_sq=-0.679,   # augmentation: increasing, concave
    aut_lin=+2.114, aut_sq=+0.809,   # automation:   increasing, convex
    # outcome loadings on the two channels
    p_aug=+0.340, p_aut=-0.580,
    # moderation of the curve (interactions with both AI and AI^2, as a shift
    # of the turning point requires)
    m1_olc=+0.450, m2_olc=+0.090,    # learning capability: flatter, right
    m1_gov=+0.550, m2_gov=+0.110,    # AI governance:       flatter, right
    m1_lcp=-0.350, m2_lcp=-0.100,    # labour cost pressure: steeper, left
    # confounding
    xi_on_ai=+0.55, xi_on_youth=+0.75,
    # time-varying firm-year demand shock that raises both adoption depth and
    # the hiring of young workers, and that firm and year effects cannot absorb
    nu_on_ai=+0.40, nu_on_youth=+0.60,
)
# reduced-form quadratic implied by the two channels
TRUE["b1"] = TRUE["p_aug"] * TRUE["aug_lin"] + TRUE["p_aut"] * TRUE["aut_lin"]
TRUE["b2"] = TRUE["p_aug"] * TRUE["aug_sq"] + TRUE["p_aut"] * TRUE["aut_sq"]
TRUE["turn"] = -TRUE["b1"] / (2 * TRUE["b2"])


def _wins(x, lo=0.01, hi=0.99):
    a, b = np.nanquantile(x, lo), np.nanquantile(x, hi)
    return np.clip(x, a, b)


def build(seed=SEED, n_firms=N_FIRMS):
    rng = np.random.default_rng(seed)

    # ---------------- firm-level fixed characteristics ----------------------
    prov = rng.integers(0, 31, n_firms)
    ind = rng.integers(0, 18, n_firms)
    soe = (rng.random(n_firms) < 0.34).astype(float)
    east = (prov < 11).astype(float)
    hitech = (rng.random(n_firms) < 0.42).astype(float)

    # province digital infrastructure and the historical variable that predicts
    # it (1984 fixed-telephone penetration per 100 people)
    phone84_p = rng.gamma(2.0, 1.1, 31) + 0.6 * (np.arange(31) < 11)
    digi_p = (0.55 * (phone84_p - phone84_p.mean()) / phone84_p.std()
              + rng.normal(0, 1, 31))
    phone84 = phone84_p[prov]
    digi = digi_p[prov]

    # unobserved firm-level "digital ambition": confounds depth and the youth
    # share and is not absorbed by the firm effects because it interacts with
    # the post-shock period
    xi = rng.normal(0, 1, n_firms)

    # ex-ante task exposure of the firm's pre-shock professional composition.
    # The industry component is what makes the peer instrument relevant.
    ind_exposure = rng.normal(0, 0.125, 18)
    exposure = (0.44 + ind_exposure[ind] + 0.055 * hitech + 0.03 * east
                + 0.055 * rng.normal(0, 1, n_firms))
    exposure = np.clip(exposure, 0.08, 0.92)

    # The three moderators are drawn independently of industry task exposure
    # and of regional digital infrastructure, so that neither instrument shifts
    # a sub-population with a systematically different curve.
    olc = rng.normal(0, 1, n_firms)
    olc = (olc - olc.mean()) / olc.std()
    gov_lat = 0.30 * soe + rng.normal(0, 1, n_firms)
    lcp0 = rng.normal(0, 1, n_firms)                 # labour cost pressure

    mu_y = rng.normal(0, 6.2, n_firms)      # firm effect, youth share
    mu_g = rng.normal(0, 7.5, n_firms)      # firm effect, augmentation
    mu_u = rng.normal(0, 5.0, n_firms)      # firm effect, automation
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
        disclose = rng.random(n_firms) < 0.86              # age composition
        keep = alive & disclose
        idx = np.where(keep)[0]
        n = idx.size

        # ---- covariates --------------------------------------------------
        size = size0[idx] + 0.055 * k + rng.normal(0, 0.32, n)
        lev = np.clip(0.421 + 0.16 * rng.normal(0, 1, n) + 0.03 * soe[idx],
                      0.03, 0.95)
        roe = 0.061 + 0.125 * rng.normal(0, 1, n) - 0.010 * k / 9
        growth = 0.122 + 0.35 * rng.normal(0, 1, n)
        age = age0[idx] + np.log1p(k) * 0.10 + rng.normal(0, 0.05, n)
        board = 2.11 + 0.19 * rng.normal(0, 1, n)
        indep = np.clip(0.377 + 0.052 * rng.normal(0, 1, n), 0.30, 0.65)
        dual = (rng.random(n) < 0.304).astype(float)
        tobinq = np.clip(2.00 + 1.25 * rng.normal(0, 1, n), 0.6, 18.0)
        fixed = np.clip(0.192 + 0.135 * rng.normal(0, 1, n), 0.002, 0.85)

        # ---- generative-AI adoption depth ----------------------------------
        # exactly zero before the shock; afterwards it scales with ex-ante task
        # exposure, firm size, regional digital infrastructure and the
        # unobserved digital ambition xi.  It is censored at both ends by
        # construction rather than by ex post winsorisation.
        post = 1.0 if t >= SHOCK_YEAR else 0.0
        nu = rng.normal(0, 1, n)          # time-varying confounder
        depth = {2023: 1.00, 2024: 1.45, 2025: 1.72}.get(t, 0.0)
        lat = (-1.15 + 2.35 * exposure[idx]
               + 0.28 * (size - size.mean()) / size.std()
               + 0.317 * digi[idx]
               + TRUE["xi_on_ai"] * xi[idx]
               + TRUE["nu_on_ai"] * nu
               + rng.normal(0, 0.42, n))
        ai = post * depth * np.clip(lat + 1.35, 0, 2.80)
        ai2 = ai ** 2

        # ---- the two channels ----------------------------------------------
        # augmentation: the share of entry-level tasks carried out with model
        # assistance.  Increasing and concave: the easiest gains come first.
        aug = (8.0 + mu_g[idx] + 3.1 * hitech[idx] + 0.9 * (size - 22.4)
               + TRUE["aug_lin"] * ai + TRUE["aug_sq"] * ai2
               + 1.6 * olc[idx] + rng.normal(0, 5.4, n))
        aug = np.clip(aug, 0.0, 96.0)

        # automation: the share of the entry-level routine-cognitive task
        # bundle executed with no human step.  Increasing and convex.
        aut = (4.0 + mu_u[idx] + 2.2 * hitech[idx] - 0.7 * soe[idx]
               + TRUE["aut_lin"] * ai + TRUE["aut_sq"] * ai2
               + rng.normal(0, 4.2, n))
        aut = np.clip(aut, 0.0, 92.0)

        # ---- moderators, measured in the current year ----------------------
        aigov = ((gov_lat[idx] + 0.9 * post + rng.normal(0, 1, n))
                 > 1.15).astype(float)
        lcp = lcp0[idx] + 0.25 * post + rng.normal(0, 0.55, n)

        # ---- youth employment share ---------------------------------------
        youth = (22.6 + mu_y[idx]
                 - 0.42 * k
                 + 1.9 * hitech[idx] - 2.6 * soe[idx]
                 + 0.9 * (size - 22.4) - 3.4 * (lev - 0.42)
                 + 1.1 * roe + 0.25 * growth - 1.7 * (age - 2.75)
                 + TRUE["p_aug"] * aug + TRUE["p_aut"] * aut
                 # moderation of the curve
                 + TRUE["m1_olc"] * ai * olc[idx]
                 + TRUE["m2_olc"] * ai2 * olc[idx]
                 + TRUE["m1_gov"] * ai * aigov
                 + TRUE["m2_gov"] * ai2 * aigov
                 + TRUE["m1_lcp"] * ai * lcp
                 + TRUE["m2_lcp"] * ai2 * lcp
                 # confounding
                 + TRUE["xi_on_youth"] * xi[idx] * post
                 + TRUE["nu_on_youth"] * nu
                 + rng.normal(0, 4.6, n))
        youth = np.clip(youth, 1.0, 78.0)
        youth35 = np.clip(youth * 1.62 + rng.normal(0, 2.4, n), 2.0, 92.0)
        lnyoung = np.log1p(youth / 100.0 * np.exp(size - 14.0))

        # ---- instrument ingredients ---------------------------------------
        # (i) shift-share on historical communications infrastructure and
        # (ii) shift-share on the firm's pre-shock task exposure, both
        # interacted with the national generative-AI diffusion index
        iv_bartik = ((phone84[idx] - phone84.mean()) / phone84.std()
                     * np.log(ai_rev[t]))
        iv_exp = (exposure[idx] - exposure.mean()) / exposure.std() * np.log(ai_rev[t])

        rows.append(pd.DataFrame(dict(
            firm=idx, year=t, ind=ind[idx], prov=prov[idx],
            Youth=youth, Youth35=youth35, LnYoung=lnyoung,
            AI=ai, AUG=aug, AUT=aut,
            OLC=olc[idx], AIGov=aigov, LCP=lcp,
            SOE=soe[idx], HiTech=hitech[idx], East=east[idx],
            Size=size, Lev=lev, ROE=roe, Growth=growth, Age=age,
            Board=board, Indep=indep, Dual=dual, TobinQ=tobinq, Fixed=fixed,
            Exposure=exposure[idx], Post=post, IV_Bartik=iv_bartik,
            IV_Exp=iv_exp)))

    df = pd.concat(rows, ignore_index=True)

    # ---- winsorisation of the continuous variables -------------------------
    for c in ["Youth", "Youth35", "LnYoung", "AUG", "AUT", "LCP", "Size",
              "Lev", "ROE", "Growth", "Age", "Board", "Indep", "TobinQ",
              "Fixed"]:
        df[c] = _wins(df[c].to_numpy())

    # standardise the two continuous moderators, so that the turning point of
    # the curve is read at their mean and a unit is one standard deviation
    for c in ["OLC", "LCP"]:
        df[c] = (df[c] - df[c].mean()) / df[c].std()

    df["AI2"] = df["AI"] ** 2

    # ---- peer instrument: leave-one-out industry x province x year mean ----
    g = df.groupby(["ind", "prov", "year"])["AI"]
    df["IV_Peer"] = ((g.transform("sum") - df["AI"])
                     / (g.transform("count") - 1).replace(0, np.nan))
    df["IV_Peer"] = df["IV_Peer"].fillna(0.0)

    # squared instruments identify the squared endogenous regressor
    df["IV_Bartik2"] = df["IV_Bartik"] ** 2
    df["IV_Peer2"] = df["IV_Peer"] ** 2
    df["IV_Exp2"] = df["IV_Exp"] ** 2

    # sharp difference-in-differences form used as a specification check
    df["Treat"] = (df.groupby("firm")["AI"].transform("mean")
                   > df.groupby("year")["AI"].transform("mean").mean()).astype(float)
    df["ExpPost"] = df["Exposure"] * df["Post"]

    df = df.sort_values(["firm", "year"]).reset_index(drop=True)
    df.to_csv(os.path.join(OUT, "panel.csv"), index=False)
    return df


if __name__ == "__main__":
    d = build()
    print("firms", d.firm.nunique(), "obs", len(d),
          "years", d.year.min(), "-", d.year.max())
    cols = ["Youth", "AI", "AUG", "AUT", "OLC", "AIGov", "LCP", "Size", "ROE",
            "Lev", "Growth", "Age", "Board", "Indep", "Dual", "TobinQ", "Fixed"]
    print(d[cols].describe().T[["count", "mean", "std", "min", "max"]].round(3))
    print()
    print("implied reduced form:  b1 = %+.3f   b2 = %+.3f   turning point = %.3f"
          % (TRUE["b1"], TRUE["b2"], TRUE["turn"]))
    post = d[d.Post == 1]
    print("AI in the post-shock years: mean %.3f  sd %.3f  max %.3f"
          % (post.AI.mean(), post.AI.std(), post.AI.max()))
