# -*- coding: utf-8 -*-
"""Global uncertainty and sensitivity analysis.

The model rests on twenty-eight declared parameters, of which most are
modelling assumptions rather than measured quantities, and on a choice among
five published exposure-response functions that disagree substantially in the
temperature band where European summers sit. A single point estimate of the
benefit of green infrastructure would therefore be an artefact of those
choices.

This module does the honest alternative. It samples the whole parameter space
by Latin hypercube, together with the discrete choices of exposure-response
function, climate setting and workplace-residence divergence, and asks two
different questions of the resulting ensemble:

    How large is the benefit?      -- answered by a distribution, and the
                                      answer is that it is not identified

    Which siting rule is best?     -- answered by the rank of the rules in
                                      each draw, and the answer is stable

First-order sensitivity is reported as the share of the variance in the
outcome explained by each input, estimated by binning each input and
decomposing the variance between and within bins. This is the standard
correlation-ratio estimator and needs no structural assumption about the
model.
"""
from __future__ import annotations

import numpy as np

import city as C
import microclimate as MC
import params as PA
import siting as SI
import thermal as TH

RULES = SI.RULES
CLIMATES = tuple(MC.CLIMATES)
ERFS = TH.ERF_NAMES


def latin_hypercube(n, d, rng):
    """An n x d Latin hypercube on the unit cube."""
    cut = np.linspace(0, 1, n + 1)
    u = rng.random((n, d))
    lo, hi = cut[:n, None], cut[1:, None]
    pts = lo + u * (hi - lo)
    for j in range(d):
        pts[:, j] = rng.permutation(pts[:, j])
    return pts


def run(n=1500, budget_ha=300.0, seed=20260825, city_seed=11):
    """Sample the space and evaluate every siting rule in every draw."""
    rng = np.random.default_rng(seed)
    sweep = [p for p in PA.sweepable()]
    names = [p.name for p in sweep]
    d = len(names)

    pts = latin_hypercube(n, d, rng)
    erf_pick = rng.integers(0, len(ERFS), size=n)
    clim_pick = rng.integers(0, len(CLIMATES), size=n)
    div_pick = rng.random(n)                     # divergence in [0, 1]

    recs = []
    cities = {}
    for i in range(n):
        vals = {nm: sweep[j].low + pts[i, j] * (sweep[j].high - sweep[j].low)
                for j, nm in enumerate(names)}
        erf = ERFS[erf_pick[i]]
        clim = CLIMATES[clim_pick[i]]
        div = float(div_pick[i])

        with PA.override(vals):
            key = round(div, 3)
            if key not in cities:
                cities[key] = C.City(seed=city_seed, divergence=key)
            ct = cities[key]
            out = SI.compare(ct, clim, budget_ha, erf)

        rec = {"i": i, "erf": erf, "climate": clim, "divergence": div,
               "baseline_youth_h": out["baseline"]["total"]["youth"],
               "baseline_youth_per_worker": out["baseline"]["per_worker"]["youth"],
               "youth_gap": out["baseline"]["youth_gap"],
               "wr_corr": ct.workplace_residence_correlation()}
        for r in RULES:
            rec["saved_%s" % r] = out["rules"][r]["hours_saved_youth"]
            rec["perha_%s" % r] = out["rules"][r]["per_ha_youth"]
        rec.update(vals)
        recs.append(rec)

    return recs, names


def rank_stability(recs, rules=RULES):
    """How often each rule beats each other rule, and how often each wins."""
    wins = {r: 0 for r in rules}
    pair = {(a, b): 0 for a in rules for b in rules if a != b}
    for rec in recs:
        vals = {r: rec["saved_%s" % r] for r in rules}
        best = max(vals, key=vals.get)
        wins[best] += 1
        for a in rules:
            for b in rules:
                if a != b and vals[a] > vals[b]:
                    pair[(a, b)] += 1
    n = len(recs)
    return ({r: wins[r] / n for r in rules},
            {k: v / n for k, v in pair.items()})


def correlation_ratio(x, y, bins=12):
    """Share of variance in y explained by x (first-order sensitivity)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    if y.std() == 0:
        return 0.0
    if len(np.unique(x)) <= bins:
        groups = [y[x == u] for u in np.unique(x)]
    else:
        edges = np.quantile(x, np.linspace(0, 1, bins + 1))
        edges[-1] += 1e-9
        idx = np.digitize(x, edges[1:-1])
        groups = [y[idx == g] for g in range(bins)]
    groups = [g for g in groups if len(g) > 1]
    if not groups:
        return 0.0
    grand = y.mean()
    between = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
    return float(np.clip(between / (len(y) * y.var()), 0.0, 1.0))


def sensitivity(recs, names, target="saved_youth"):
    y = np.array([r[target] for r in recs], float)
    out = {}
    for nm in names:
        out[nm] = correlation_ratio([r[nm] for r in recs], y)
    out["erf"] = correlation_ratio(
        [ERFS.index(r["erf"]) for r in recs], y)
    out["climate"] = correlation_ratio(
        [CLIMATES.index(r["climate"]) for r in recs], y)
    out["divergence"] = correlation_ratio([r["divergence"] for r in recs], y)
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def _selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        if not c:
            print("FAIL:", m); ok = False

    recs, names = run(n=120, seed=3)
    chk(len(recs) == 120, "all draws returned")
    chk(all(np.isfinite(r["saved_youth"]) for r in recs), "finite savings")

    wins, pair = rank_stability(recs)
    chk(abs(sum(wins.values()) - 1.0) < 1e-9, "win shares sum to one")

    sens = sensitivity(recs, names)
    chk(all(0.0 <= v <= 1.0 for v in sens.values()), "sensitivity indices in [0,1]")

    lo = min(r["baseline_youth_per_worker"] for r in recs)
    hi = max(r["baseline_youth_per_worker"] for r in recs)
    print("uncertainty.py self-test:", "PASSED" if ok else "FAILED")
    print("  %d draws over %d swept parameters + ERF + climate + divergence"
          % (len(recs), len(names)))
    print("  baseline youth loss per worker per day: %.3f to %.3f h (factor %.1f)"
          % (lo, hi, hi / max(lo, 1e-9)))
    print("  share of draws in which each rule is best for young workers:")
    for r, w in sorted(wins.items(), key=lambda kv: -kv[1]):
        print("    %-12s %5.1f%%" % (r, 100 * w))
    print("  P(exposure-targeted beats population-weighted) = %.3f"
          % pair[("exposure", "population")])
    print("  top first-order sensitivity indices for youth hours saved:")
    for k, v in list(sens.items())[:6]:
        print("    %-26s %.3f" % (k, v))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
