# -*- coding: utf-8 -*-
"""Generate the expected-results dataset.

THIS FILE PRODUCES SIMULATED DATA. No person answered any of these items.
The dataset exists so that the analysis pipeline can be written and tested,
the sample size checked against the effects the study expects to find, and
the shape of the eventual result tables agreed before fieldwork starts. It
must be replaced by the collected data before anything is reported.

The generating model is the one the study hypothesises, so the dataset shows
what the data would look like *if the hypotheses are right*. That is its
purpose and also its limit: it cannot corroborate them.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "design"))
import items as I                                             # noqa: E402

SEED = 20260826
N_COLLECTED = 468        # what is fielded
N_VALID = 400            # what survives screening

# --------------------------------------------------------------------------
# the structural model the study hypothesises
# --------------------------------------------------------------------------
# correlations among the exogenous latents
EXO = ["CA", "PA", "PD", "PF"]
EXO_R = {
    ("CA", "PA"): -0.15, ("CA", "PD"): 0.22, ("CA", "PF"): 0.05,
    ("PA", "PD"): 0.12, ("PA", "PF"): 0.55, ("PD", "PF"): 0.50,
}

# structural paths, on standardised latents
B_CE = dict(CA=-0.24, PA=0.30, PD=-0.08)
B_SE = dict(CE=0.42, CA=-0.16, PA=0.20, PD=-0.10)
B_CD = dict(CA=0.36, SE=-0.22, CE=-0.18, PD=0.06, PA=-0.04)

# the three moderation terms the study is designed to separate: help that
# must be used amplifies, help that substitutes buffers, and the frequency
# of help — which is what instruments usually record — does neither
B_INT = {"CAxPA": 0.13, "CAxPD": -0.14, "CAxPF": 0.02}

# small effects of the background variables, so the controls are not inert
B_DEMO_CD = {"D9": -0.09, "D10": -0.14}
B_DEMO_CA = {"D1": 0.11, "D10": -0.10}

LOADING_RANGE = (0.62, 0.84)
CARELESS_SHARE = 0.055


def _exo_corr():
    k = len(EXO)
    R = np.eye(k)
    for (a, b), r in EXO_R.items():
        i, j = EXO.index(a), EXO.index(b)
        R[i, j] = R[j, i] = r
    return R


def _z(x):
    return (x - x.mean()) / x.std(ddof=0)


def latents(rng, n):
    """Draw the latent variables from the hypothesised structural model."""
    R = _exo_corr()
    L = np.linalg.cholesky(R)
    E = (rng.standard_normal((n, len(EXO))) @ L.T)
    v = {k: _z(E[:, i]) for i, k in enumerate(EXO)}

    # background variables, drawn to plausible marginals for a cohort of
    # final-year students at a non-elite mainland university
    d = {}
    d["D1"] = rng.choice([1, 2], n, p=[0.42, 0.58])
    d["D2"] = rng.choice([1, 2, 3, 4], n, p=[0.18, 0.56, 0.11, 0.15])
    d["D3"] = rng.choice([1, 2, 3, 4, 5], n, p=[0.24, 0.31, 0.28, 0.07, 0.10])
    d["D4"] = rng.choice([1, 2, 3], n, p=[0.14, 0.68, 0.18])
    d["D5"] = rng.choice([1, 0], n, p=[0.38, 0.62])
    d["D6"] = rng.choice([1, 2, 3], n, p=[0.34, 0.39, 0.27])
    d["D7"] = rng.choice([1, 2, 3, 4, 5], n, p=[0.21, 0.34, 0.22, 0.19, 0.04])
    d["D8"] = rng.choice([1, 2, 3, 4, 5], n, p=[0.22, 0.33, 0.28, 0.11, 0.06])
    d["D9"] = rng.choice([0, 1, 2], n, p=[0.29, 0.42, 0.29])
    d["D10"] = rng.choice([1, 2, 3, 4, 5], n, p=[0.14, 0.33, 0.25, 0.17, 0.11])

    for k, b in B_DEMO_CA.items():
        v["CA"] = v["CA"] + b * _z(d[k].astype(float))
    v["CA"] = _z(v["CA"])

    def build(paths, resid):
        y = np.zeros(n)
        for k, b in paths.items():
            y = y + b * v[k]
        return _z(y + resid * rng.standard_normal(n))

    v["CE"] = build(B_CE, 0.90)
    v["SE"] = build(B_SE, 0.84)

    cd = np.zeros(n)
    for k, b in B_CD.items():
        cd = cd + b * v[k]
    for term, b in B_INT.items():
        a, w = term.split("x")
        cd = cd + b * v[a] * v[w]
    for k, b in B_DEMO_CD.items():
        cd = cd + b * _z(d[k].astype(float))
    v["CD"] = _z(cd + 0.86 * rng.standard_normal(n))

    v["MK"] = _z(rng.standard_normal(n))          # unrelated by construction
    return v, d


def responses(rng, theta, con):
    """Turn a latent score into integer item responses on the item's scale."""
    n = theta.size
    _, k = I.SCALES[con.scale]
    out = {}
    for code, _, rev in con.items:
        lam = rng.uniform(*LOADING_RANGE)
        x = lam * theta + np.sqrt(1.0 - lam ** 2) * rng.standard_normal(n)
        spread = 1.02 if k == 5 else 1.70
        centre = con.loc if k == 5 else con.loc
        y = np.rint(centre + spread * x)
        y = np.clip(y, 1, k).astype(int)
        out[code] = (k + 1 - y) if rev else y      # store as presented
    return out


def simulate(n_valid=None, seed=None):
    rng = np.random.default_rng(SEED if seed is None else seed)
    n_valid = N_VALID if n_valid is None else n_valid
    n = int(round(n_valid * N_COLLECTED / N_VALID))
    v, demo = latents(rng, n)

    cols = {}
    cols.update({k: val for k, val in demo.items()})
    for con in I.CONSTRUCTS:
        cols.update(responses(rng, v[con.key], con))

    # attention checks: answered correctly by attentive respondents
    cols["AC1"] = np.full(n, 4)
    cols["AC2"] = np.full(n, 5)

    # completion time in seconds, log-normal around about seven minutes
    dur = np.rint(np.exp(rng.normal(np.log(430), 0.42, n))).astype(int)

    # careless respondents: straightlining or near-random, wrong on the
    # checks, and fast
    n_bad = int(round(CARELESS_SHARE * n))
    bad = rng.choice(n, n_bad, replace=False)
    item_codes = [c for con in I.CONSTRUCTS for c in con.codes]
    for i in bad:
        if rng.random() < 0.55:                     # straightliner
            for con in I.CONSTRUCTS:
                _, k = I.SCALES[con.scale]
                pick = int(rng.integers(1, k + 1))
                for code in con.codes:
                    cols[code][i] = pick
        else:                                       # random responder
            for con in I.CONSTRUCTS:
                _, k = I.SCALES[con.scale]
                for code in con.codes:
                    cols[code][i] = int(rng.integers(1, k + 1))
        cols["AC1"][i] = int(rng.choice([1, 2, 3, 5]))
        cols["AC2"][i] = int(rng.choice([1, 2, 3, 4, 6, 7, 8, 9]))
        dur[i] = int(rng.integers(70, 175))

    # a few attentive respondents also rush or slip a check
    for i in rng.choice(np.setdiff1d(np.arange(n), bad), 14, replace=False):
        if rng.random() < 0.5:
            cols["AC1"][i] = 3
        else:
            dur[i] = int(rng.integers(95, 178))

    cols["duration_s"] = dur
    cols["straightline_sd"] = np.array(
        [np.std([cols[c][i] for c in item_codes]) for i in range(n)])

    # -------------------------------------------------- screening
    keep = ((cols["AC1"] == 4) & (cols["AC2"] == 5)
            & (cols["duration_s"] >= 180)
            & (cols["straightline_sd"] > 0.30))
    idx = np.where(keep)[0]
    excl = {"注意力检测未通过": int(((cols["AC1"] != 4)
                                    | (cols["AC2"] != 5)).sum()),
            "作答时长不足 180 秒": int((cols["duration_s"] < 180).sum()),
            "全部条目作答无变异": int((cols["straightline_sd"] <= 0.30).sum())}

    if idx.size > n_valid:                       # trim to the planned n
        idx = np.sort(rng.choice(idx, n_valid, replace=False))

    data = {k: np.asarray(val)[idx] for k, val in cols.items()}
    data["ID"] = np.arange(1, idx.size + 1)
    truth = {k: val[idx] for k, val in v.items()}
    meta = dict(seed=SEED if seed is None else seed,
                n_collected=n, n_valid=int(idx.size),
                excluded=excl, careless_planted=n_bad,
                structural={"CE": B_CE, "SE": B_SE, "CD": B_CD,
                            "interactions": B_INT},
                exogenous_corr={"%s-%s" % k: v_ for k, v_ in EXO_R.items()})
    return data, truth, meta


ORDER = (["ID"] + I.CONTROLS
         + [c for con in I.CONSTRUCTS for c in con.codes]
         + ["AC1", "AC2", "duration_s"])


if __name__ == "__main__":
    d, t, m = simulate()
    print("拟发放 %d 份，有效 %d 份（%.1f%%）"
          % (m["n_collected"], m["n_valid"],
             100.0 * m["n_valid"] / m["n_collected"]))
    for k, val in m["excluded"].items():
        print("   剔除：%s %d" % (k, val))
    print("变量 %d 个" % len(ORDER))
    print(json.dumps(m["structural"], ensure_ascii=False))
