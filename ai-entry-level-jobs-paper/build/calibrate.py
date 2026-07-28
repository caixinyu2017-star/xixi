# -*- coding: utf-8 -*-
"""Calibrate the job-ladder model to Chinese labour-market moments, 2025.

Identification.  Matching efficiency and vacancy cost enter every equilibrium
object only through the ratio mu_i^2 / c_i, so mu_j = mu_s = 1 is a
normalisation and the vacancy costs carry that dimension.  Task units are also
free, so z_j = chi = 1; only relative changes in chi (the exposure experiments
of Section 5.5) have content.  Recruiting cost per hire equals J_i / w_i by free
entry and is therefore implied rather than targeted, which makes it available as
an over-identifying check.  What remains is eight parameters and eight
conditions: seven data moments and the output normalisation Y = 1.  The system
is square, so a bounded least-squares solve satisfies every condition exactly
rather than minimising a distance that stays positive at the optimum.
"""
from __future__ import annotations

import json
import math
import os

import numpy as np
from scipy.optimize import differential_evolution, least_squares

import ladder as L

HERE = os.path.dirname(os.path.abspath(__file__))

# key, target, weight, source
MOMENTS = [
    ("u_rate_j",     0.178, 2.0,
     "Surveyed urban unemployment rate, aged 16-24 excluding students, July "
     "2025 (National Bureau of Statistics)"),
    ("u_rate_s",     0.043, 2.0,
     "Surveyed urban unemployment rate, aged 25-59, December 2025: "
     "labour-force-weighted average of 6.9% (25-29) and 3.9% (30-59)"),
    ("wage_ratio",   1.700, 2.0,
     "Experience wage premium: earnings of experienced workers relative to "
     "first-job earnings, urban China"),
    ("pi",           0.286, 1.5,
     "Promotion hazard implied by a mean 3.5 years to first promotion"),
    ("ai_share",     0.250, 1.5,
     "Share of the entry-level task bundle performed by artificial "
     "intelligence, from enterprise adoption and task-usage surveys, 2025"),
    ("labour_share", 0.550, 1.5,
     "Labour compensation share of value added, China"),
    ("repl_rate",    0.550, 1.0,
     "Flow value of non-employment relative to the entry-level wage"),
    ("Y",            1.000, 1.0,
     "Normalisation: output per member of the labour force"),
]

CHECKS = ["hire_cost_j", "hire_cost_s", "train_share", "mentor_share",
          "senior_emp_share", "search_months_j", "promo_years", "m",
          "theta_j", "theta_s", "f_j", "f_s", "w_j", "w_s", "A", "F_s", "G_j"]

FREE = [
    ("Z",     0.10, 12.00),
    ("c_j",   0.002, 3.00),
    ("c_s",   0.002, 4.00),
    ("alpha", 0.01, 0.90),
    ("pibar", 0.02, 8.00),
    ("p_a",   0.005, 4.00),
    ("s_y",   0.25, 0.98),
    ("b",     0.005, 3.00),
]

# analytic starting point derived from the block recursion of the moment system
START = dict(Z=1.281, c_j=0.0555, c_s=0.1083, alpha=0.1972, pibar=1.719,
             p_a=0.382, s_y=0.6193, b=0.1955)

LO = np.array([lo for _, lo, _ in FREE])
HI = np.array([hi for _, _, hi in FREE])
BAD = 1e6


def make_params(vec):
    p = dict(L.BASE)
    p.update({k: float(v) for (k, _, _), v in zip(FREE, vec)})
    return p


def _ok(r, ok):
    return (ok and r["A"] > 1e-9 and r["m"] > 1e-9 and r["w_j"] > 0
            and r["X_s"] > 1e-9 and r["Sj"] > 0 and r["Ss"] > 0
            and np.isfinite(r["Y"]) and r["Y"] > 0)


def evaluate(vec, full=False):
    p = make_params(vec)
    fail = (BAD, None, None) if full else BAD
    try:
        res, ok, _ = L.solve(p)
        if not _ok(res, ok):
            return fail
        if not np.isfinite([res[k] for k, _, _, _ in MOMENTS]).all():
            return fail
    except Exception:
        return fail
    loss, rows = 0.0, []
    for key, tgt, w, src in MOMENTS:
        sim = float(res[key])
        rel = (sim - tgt) / tgt
        loss += w * rel ** 2
        rows.append(dict(moment=key, target=tgt, simulated=sim, rel_error=rel,
                         weight=w, source=src))
    return (loss, rows, p) if full else loss


def log_resid(vec):
    """Log deviation of each moment from its target; the system is square."""
    p = make_params(vec)
    try:
        r, ok = L.solve(p)[:2]
        if not _ok(r, ok):
            return np.full(len(FREE), 5.0)
        out = np.array([math.log(max(r[k], 1e-12) / t) for k, t, _, _ in MOMENTS])
        return out if np.isfinite(out).all() else np.full(len(FREE), 5.0)
    except Exception:
        return np.full(len(FREE), 5.0)


def polish(start, tries=80, seed=20260728):
    """Bounded least-squares solve of the square system, with restarts."""
    best = np.clip(np.asarray(start, float), LO, HI)
    err = float(np.max(np.abs(log_resid(best))))
    rng = np.random.default_rng(seed)
    g, span = best.copy(), HI - LO
    for i in range(tries):
        try:
            sol = least_squares(log_resid, g, bounds=(LO, HI), method="trf",
                                xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
            e = float(np.max(np.abs(log_resid(sol.x))))
            if e < err:
                best, err = sol.x, e
        except Exception:
            pass
        if err < 1e-9:
            break
        if i < tries // 2:
            g = np.clip(best * np.exp(rng.normal(0.0, 0.05 + 0.03 * i,
                                                 size=len(FREE))), LO, HI)
        else:
            g = LO + rng.random(len(FREE)) * span
    return best, err


def main():
    start = np.array([START[k] for k, _, _ in FREE])
    vec, err = polish(start)
    if err > 1e-7:
        print("local stage insufficient (%.2e); running a global search" % err,
              flush=True)
        opt = differential_evolution(
            evaluate, [(lo, hi) for _, lo, hi in FREE],
            seed=20260728, maxiter=400, popsize=24, tol=1e-13,
            mutation=(0.3, 1.0), recombination=0.9,
            polish=True, init="sobol", workers=-1, updating="deferred")
        vec2, err2 = polish(opt.x)
        if err2 < err:
            vec, err = vec2, err2

    loss, rows, p = evaluate(vec, full=True)
    rmspe = float(np.sqrt(np.mean([r["rel_error"] ** 2 for r in rows])))
    print("max |log residual| = %.3e   RMSPE = %.6f%%" % (err, 100 * rmspe))
    for r in rows:
        print("  %-14s target %8.4f  sim %8.4f  rel %+10.6f%%"
              % (r["moment"], r["target"], r["simulated"], 100 * r["rel_error"]))
    print("\nestimated parameters")
    for k, _, _ in FREE:
        print("  %-7s %.5f" % (k, p[k]))

    eq, ok, x0 = L.solve(p)
    print("\nover-identifying checks and further model statistics")
    for k in CHECKS:
        print("  %-18s %.5f" % (k, eq[k]))

    json.dump(dict(loss=loss, rmspe=rmspe, max_log_resid=err, moments=rows,
                   params=p, checks={k: float(eq[k]) for k in CHECKS},
                   x0=list(x0)),
              open(os.path.join(HERE, "calibrated.json"), "w"), indent=1)
    print("\nwritten calibrated.json")


if __name__ == "__main__":
    main()
