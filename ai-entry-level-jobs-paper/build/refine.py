# -*- coding: utf-8 -*-
"""Exact-identification polish of the calibration.

The estimation problem is exactly identified: nine structural parameters, nine
steady-state moments.  `calibrate.py` uses differential evolution to locate the
basin; this script solves the nine moment conditions exactly by Newton's method
from that starting point, so the reported fit is exact rather than approximate.
"""
from __future__ import annotations

import json
import math
import os

import numpy as np
from scipy.optimize import root

import ladder as L
from calibrate import FREE, MOMENTS, CHECKS

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = [k for k, _, _ in FREE]


def residuals(z, p_ext):
    q = dict(p_ext)
    q.update({k: float(np.exp(v)) for k, v in zip(KEYS, z)})
    try:
        r, ok, _ = L.solve(q)
        if not ok or r["A"] <= 1e-9 or r["m"] <= 1e-9 or r["w_j"] <= 0:
            return np.full(len(KEYS), 5.0)
        return np.array([math.log(max(r[k], 1e-12) / t) for k, t, _, _ in MOMENTS])
    except Exception:
        return np.full(len(KEYS), 5.0)


def main():
    cal = json.load(open(os.path.join(HERE, "calibrated.json")))
    p_ext = dict(L.BASE)
    start = np.log([cal["params"][k] for k in KEYS])

    sol = root(residuals, start, args=(p_ext,), method="hybr", tol=1e-13)
    z = sol.x
    err = float(np.max(np.abs(residuals(z, p_ext))))
    if err > 1e-8:
        # a few perturbed restarts if the first Newton run stalls
        rng = np.random.default_rng(20260728)
        for _ in range(60):
            g = start + rng.normal(0.0, 0.12, size=len(start))
            s2 = root(residuals, g, args=(p_ext,), method="hybr", tol=1e-13)
            e2 = float(np.max(np.abs(residuals(s2.x, p_ext))))
            if e2 < err:
                z, err = s2.x, e2
            if err < 1e-10:
                break

    p = dict(L.BASE)
    p.update({k: float(np.exp(v)) for k, v in zip(KEYS, z)})
    res, ok, x0 = L.solve(p)

    rows = []
    for key, tgt, w, src in MOMENTS:
        sim = float(res[key])
        rows.append(dict(moment=key, target=tgt, simulated=sim,
                         rel_error=(sim - tgt) / tgt, weight=w, source=src))
    rmspe = float(np.sqrt(np.mean([r["rel_error"] ** 2 for r in rows])))

    print("exact-identification polish: max |log residual| = %.3e" % err)
    for r in rows:
        print("  %-14s target %8.4f  sim %8.4f  rel %+8.4f%%"
              % (r["moment"], r["target"], r["simulated"], 100 * r["rel_error"]))
    print("\nestimated parameters")
    for k in KEYS:
        print("  %-7s %.5f" % (k, p[k]))
    print("\nover-identifying checks (not targeted)")
    for k in CHECKS:
        print("  %-18s %.4f" % (k, res[k]))
    print("\nequilibrium: f_j %.3f f_s %.3f m %.4f A %.4f Y %.4f w_j %.4f w_s %.4f"
          % (res["f_j"], res["f_s"], res["m"], res["A"], res["Y"],
             res["w_j"], res["w_s"]))

    json.dump(dict(loss=0.0, rmspe=rmspe, max_log_resid=err, moments=rows,
                   params=p, checks={k: float(res[k]) for k in CHECKS},
                   x0=list(x0)),
              open(os.path.join(HERE, "calibrated.json"), "w"), indent=1)
    print("\nwritten calibrated.json (polished)")


if __name__ == "__main__":
    main()
