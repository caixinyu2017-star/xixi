# -*- coding: utf-8 -*-
"""Calibrate the model to a published correlation matrix.

The model has no data of its own to be fitted to. What it can be held to is
the pattern of association that the empirical literature reports, and this
module does exactly that: it searches a small number of parameters so that the
simulated cross-section reproduces the six correlations among career anxiety,
career decision-making self-efficacy, perceived parental career support and
career decision-making difficulties that Pan and He report for 407 female
undergraduates.

The target is a correlation matrix from one published study, so the
calibration inherits that study's population and its limits. It is a
face-validity check, not an estimate: it establishes that the model can
produce the pattern the field observes, not that the model is true. The
parameters the search moves are recorded as "calibrated" in the registry,
with the target named, and are distinguished throughout from parameters that
were merely assumed.
"""
from __future__ import annotations

import itertools
import numpy as np

import model as M
import params as P

# Pan and He, Behavioral Sciences, 2026: correlations among the four
# constructs in a sample of 407 female undergraduates.
TARGET = {
    ("CA", "CDSE"): -0.275,
    ("CA", "PCS"): -0.281,
    ("CA", "CDD"): 0.460,
    ("CDSE", "PCS"): 0.429,
    ("CDSE", "CDD"): -0.286,
    ("PCS", "CDD"): -0.268,
}

# the parameters the search is allowed to move, and their bounds
# The substitution share is deliberately NOT calibrated. It is the quantity
# the study varies, and Section 4 shows that the correlation matrix is nearly
# uninformative about it while the interaction is not. Calibrating it here
# would assume away the paper's identification argument.
FREE = ["anxiety_interference", "expl_anxiety", "process_noise",
        "anxiety_from_efficacy", "support_reassurance", "scaffold_gain",
        "trait_anxiety_mean", "expl_efficacy", "heterogeneity",
        "sd_trait_anxiety", "efficacy_attribution", "substitute_yield"]


def correlations(n=4000, seed=11):
    st = M.simulate(n=n, seed=seed)
    obs = M.observe(st, seed=seed + 1)
    out = {}
    for x, y in itertools.combinations(("CA", "CDSE", "PCS", "CDD"), 2):
        out[(x, y)] = float(np.corrcoef(obs[x], obs[y])[0, 1])
    return out


def loss(vals, n=4000, seed=11):
    with P.override(vals):
        c = correlations(n=n, seed=seed)
    return float(np.sqrt(np.mean([(c[k] - TARGET[k]) ** 2 for k in TARGET]))), c


def search(iters=900, seed=3, n=3000):
    """Coordinate descent with shrinking steps, from the declared defaults."""
    rng = np.random.default_rng(seed)
    bounds = {k: (P._REG[k].low, P._REG[k].high) for k in FREE}
    cur = {k: P.v(k) for k in FREE}
    best, _ = loss(cur, n=n, seed=seed)
    step = {k: 0.30 * (bounds[k][1] - bounds[k][0]) for k in FREE}

    for it in range(iters):
        k = FREE[it % len(FREE)]
        lo, hi = bounds[k]
        for direction in (1.0, -1.0):
            trial = dict(cur)
            trial[k] = float(np.clip(cur[k] + direction * step[k], lo, hi))
            if trial[k] == cur[k]:
                continue
            l, _ = loss(trial, n=n, seed=seed)
            if l < best - 1e-6:
                best, cur = l, trial
                break
        else:
            step[k] *= 0.72
        if max(step.values()) < 1e-4:
            break
    return cur, best


def report(vals):
    l, c = loss(vals, n=8000, seed=101)
    rows = []
    for k in TARGET:
        rows.append((("%s-%s" % k), TARGET[k], c[k], c[k] - TARGET[k]))
    return l, rows


if __name__ == "__main__":
    base, _ = loss({k: P.v(k) for k in FREE}, n=8000, seed=101)
    print("RMSE at the declared defaults: %.4f" % base)
    vals, best = search()
    l, rows = report(vals)
    print("RMSE after calibration:        %.4f" % l)
    print()
    print("  %-12s %8s %8s %8s" % ("pair", "target", "model", "diff"))
    for name, t, m, d in rows:
        print("  %-12s %+8.3f %+8.3f %+8.3f" % (name, t, m, d))
    print()
    print("  calibrated values:")
    for k in FREE:
        print("    %-24s %.4f   (was %.4f)" % (k, vals[k], P._REG[k].value))


def identification_check(vals, shares=(0.0, 0.25, 0.5, 0.75, 1.0), n=8000):
    """Can the correlation matrix tell us how much support substitutes?

    Refit nothing: hold the calibrated parameters and vary only the
    substitution share. If the fit to the observed correlations barely moves,
    then a study that reports only a correlation matrix cannot distinguish
    supportive involvement from involvement that does the work for the young
    person.
    """
    out = []
    for pi in shares:
        v = dict(vals); v["substitution_share"] = pi
        l, c = loss(v, n=n, seed=101)
        out.append((pi, l, c))
    return out
