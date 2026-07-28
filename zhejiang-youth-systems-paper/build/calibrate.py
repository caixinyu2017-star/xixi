# -*- coding: utf-8 -*-
"""Simulated-method-of-moments calibration of the YSTS model.

Six free structural parameters are chosen to minimise a weighted distance
between simulated and observed moments.  The 2015 moments are evaluated at the
model's own frozen-driver fixed point (the initial condition); the 2025 moments
are evaluated after ten years of transient dynamics driven by the observed
expansion of the digital economy and of the graduate cohort.
"""
from __future__ import annotations

import json
import os

import numpy as np
from scipy.optimize import differential_evolution

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------- moments
# key, year-index (0 = 2015 fixed point, 10 = 2025), target, weight, source tag
MOMENTS = [
    ("NER",    0, 0.115, 1.0, "NBS urban surveyed unemployment, aged 16-24, 2015"),
    ("SEflow", 0, 0.060, 1.0, "graduate destination surveys, mid-2010s"),
    ("MM",     0, 0.180, 1.0, "graduate over-education literature, mid-2010s"),
    ("NER",   10, 0.180, 1.6, "NBS 16-24 excl. students, 2025 average"),
    ("SEflow", 10, 0.191, 1.6, "Zhaopin graduate survey 2024, slow-employment share"),
    ("MM",    10, 0.240, 1.2, "vertical mismatch among Chinese graduates"),
    ("RATIO", 10, 96.00, 0.8, "national civil-service exam competition ratio, 2026"),
]

# Over-identifying checks that are NOT used in the objective (validation only).
VALIDATION = [
    ("RATIO", 0, 63.0, "national civil-service exam competition ratio, 2015 cycle"),
    ("RATIO", 10, 96.0, "national civil-service exam competition ratio, 2026 cycle"),
]

FREE = [
    ("kappa",   0.60, 4.00),
    ("mu",      1.0, 14.0),
    ("Pi",      0.20, 3.50),
    ("nu",      0.15, 6.00),
    ("sigma0",  0.00, 1.80),
    ("eps_pw",  0.20, 0.95),
]


def make_params(vec):
    p = dict(M.BASE)
    for (name, _, _), v in zip(FREE, vec):
        p[name] = float(v)
    return p


def evaluate(vec, full=False):
    p = make_params(vec)
    try:
        y0, ok = M.equilibrium(0.0, p, M.GUESS_LOW)
        if not ok or y0[0] > 1500.0 or y0[0] < 12.0:
            return (1e6, None, None) if full else 1e6
        d0 = M.indicators(0.0, y0, p)
        if not np.isfinite(list(d0.values())).all():
            return (1e6, None, None) if full else 1e6
        ts, ys = M.rk4(y0, p, 0.0, 10.0, 1.0 / 24.0)
        d10 = M.indicators(10.0, ys[-1], p)
    except Exception:
        return (1e6, None, None) if full else 1e6

    loss, rows = 0.0, []
    for key, yr, tgt, w, src in MOMENTS:
        sim = float((d0 if yr == 0 else d10)[key])
        rel = (sim - tgt) / tgt
        loss += w * rel ** 2
        rows.append(dict(moment=key, year=2015 + yr, target=tgt, simulated=sim,
                         rel_error=rel, weight=w, source=src))
    return (loss, rows, p) if full else loss


def main():
    bounds = [(lo, hi) for _, lo, hi in FREE]
    res = differential_evolution(evaluate, bounds, seed=20260728, maxiter=400,
                                 popsize=28, tol=1e-10, mutation=(0.4, 1.0),
                                 recombination=0.85, polish=True, init="sobol",
                                 workers=-1, updating="deferred")
    loss, rows, p = evaluate(res.x, full=True)
    print("calibration loss = %.6g" % loss)
    for r in rows:
        print("  %-7s %d  target %8.3f  sim %8.3f  rel %+7.2f%%"
              % (r["moment"], r["year"], r["target"], r["simulated"],
                 100 * r["rel_error"]))
    print("\ncalibrated parameters")
    for name, _, _ in FREE:
        print("  %-9s %.4f" % (name, p[name]))

    y0, ok = M.equilibrium(0.0, p, M.GUESS_LOW)
    ts, ys = M.rk4(y0, p, 0.0, 10.0, 1.0 / 24.0)
    d0, d10 = M.indicators(0.0, y0, p), M.indicators(10.0, ys[-1], p)
    print("\nover-identifying validation checks (not in the objective)")
    for key, yr, tgt, src in VALIDATION:
        sim = float((d0 if yr == 0 else d10)[key])
        print("  %-7s %d  observed %8.2f  simulated %8.2f" % (key, 2015 + yr, tgt, sim))
    print("  RATIO growth: observed %.2fx  simulated %.2fx"
          % (VALIDATION[1][2] / VALIDATION[0][2], d10["RATIO"] / d0["RATIO"]))
    print("\n2015 fixed point ok=%s: %s" % (ok, np.round(y0, 4)))
    ev, kind = M.classify(0.0, y0, p)
    print("eigenvalues:", np.round(np.sort_complex(ev), 4), "->", kind)

    out = dict(loss=loss, moments=rows, params=p, free=[f[0] for f in FREE],
               y0_2015=y0.tolist(), eig_real=np.real(ev).tolist(),
               eig_imag=np.imag(ev).tolist(), regime=kind)
    with open(os.path.join(HERE, "calibrated.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nwritten calibrated.json")


if __name__ == "__main__":
    main()
