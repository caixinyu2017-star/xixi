# -*- coding: utf-8 -*-
"""Calibrate the rationing model to Chinese labour-market moments, 2025.

Identification.  Market productivity is the numeraire and matching efficiency
in the prime tier is normalised to one, because only the ratio of matching
efficiency to vacancy cost is identified.  Quota-sector productivity is set
equal to market productivity, so the administered wage premium is a pure rent
rather than a return to higher measured productivity; nothing in the allocation
depends on that choice, and Section 5.8 varies it.  What remains is six
parameters and six moments.  The system is square, so the moment conditions are
solved exactly rather than minimised.
"""
from __future__ import annotations

import json
import math
import os

import numpy as np
from scipy.optimize import least_squares

import rationing as Q

HERE = os.path.dirname(os.path.abspath(__file__))

MOMENTS = [
    ("u_rate_y",     0.178, "Surveyed urban unemployment rate, aged 16-24 "
                            "excluding students, July 2025 (NBS)"),
    ("u_rate_p",     0.043, "Surveyed urban unemployment rate, aged 25-59, "
                            "December 2025: labour-force-weighted average of "
                            "6.9% (25-29) and 3.9% (30-59)"),
    ("quota_share",  0.120, "Share of urban employment in government "
                            "agencies and public institutions, whose headcount "
                            "is fixed by establishment quotas; commercial "
                            "state-owned enterprises are excluded because they "
                            "hire without an establishment ceiling"),
    ("wage_premium", 1.250, "Compensation-equivalent premium of a quota job "
                            "over an entry-level market job, including "
                            "pension, housing and security provisions"),
    ("queue_share",  0.350, "Share of young non-employment whose main "
                            "activity is preparing for public-sector entrance "
                            "examinations"),
    ("repl_rate",    0.550, "Flow value of open search relative to the "
                            "entry-level market wage"),
]

CHECKS = ["queue_years", "cohort_entry_Q", "search_months_y", "lam_Q", "theta",
          "L", "young", "prime", "u_q", "u_m", "e_q", "e_m", "U_m", "E_q",
          "E_m", "w_y", "w_p", "wbar_M", "w_Q", "N", "v_M", "Y", "welfare",
          "welfare_pc", "V_entrant", "gamma", "rho"]

FREE = [
    ("c_M",     0.005, 4.00),
    ("N_bar",   0.50, 40.00),
    ("w_Q",     0.10, 5.00),
    ("b",       0.01, 3.00),
    ("kappa_q", -2.500, 0.999),
    ("mu_y",    0.05, 1.50),
]

START = dict(c_M=0.05, N_bar=3.8, w_Q=1.20, b=0.54, kappa_q=-0.30, mu_y=0.80)

LO = np.array([lo for _, lo, _ in FREE])
HI = np.array([hi for _, _, hi in FREE])


def make_params(vec):
    p = dict(Q.BASE)
    p.update({k: float(v) for (k, _, _), v in zip(FREE, vec)})
    return p


def _ok(r):
    if r is None:
        return False
    for k in ("u_q", "u_m", "e_m", "U_m", "E_m", "w_y", "theta"):
        if not np.isfinite(r[k]) or r[k] <= 0:
            return False
    return (np.isfinite(r["lam_Q"]) and r["lam_Q"] > 0
            and 0.0 < r["a_q"] < 1.0 and r["Y"] > 0)


def log_resid(vec):
    p = make_params(vec)
    try:
        r, ok = Q.solve(p)
        if not ok or not _ok(r):
            return np.full(len(FREE), 5.0)
        out = np.array([math.log(max(r[k], 1e-12) / t) for k, t, _ in MOMENTS])
        return out if np.isfinite(out).all() else np.full(len(FREE), 5.0)
    except Exception:
        return np.full(len(FREE), 5.0)


def polish(start, tries=200, seed=20260728):
    best = np.clip(np.asarray(start, float), LO, HI)
    err = float(np.max(np.abs(log_resid(best))))
    rng = np.random.default_rng(seed)
    g, span = best.copy(), HI - LO
    for i in range(tries):
        try:
            sol = least_squares(log_resid, g, bounds=(LO, HI), method="trf",
                                xtol=1e-15, ftol=1e-15, gtol=1e-15,
                                max_nfev=2000)
            e = float(np.max(np.abs(log_resid(sol.x))))
            if e < err:
                best, err = sol.x, e
        except Exception:
            pass
        if err < 1e-9:
            break
        if i < tries // 2:
            g = np.clip(best * np.exp(rng.normal(0.0, 0.05 + 0.02 * i,
                                                 size=len(FREE))), LO, HI)
        else:
            g = LO + rng.random(len(FREE)) * span
    return best, err


def main():
    start = np.array([START[k] for k, _, _ in FREE])
    vec, err = polish(start)
    p = make_params(vec)
    r, ok = Q.solve(p)

    rows = []
    for key, tgt, src in MOMENTS:
        rows.append(dict(moment=key, target=tgt, simulated=float(r[key]),
                         rel_error=float(r[key] / tgt - 1.0), source=src))
    rmspe = float(np.sqrt(np.mean([x["rel_error"] ** 2 for x in rows])))

    print("max |log residual| = %.3e   RMSPE = %.6f%%" % (err, 100 * rmspe))
    for x in rows:
        print("  %-14s target %8.4f  sim %8.4f  rel %+10.6f%%"
              % (x["moment"], x["target"], x["simulated"], 100 * x["rel_error"]))
    print("\nestimated parameters")
    for k, _, _ in FREE:
        print("  %-8s %.5f" % (k, p[k]))
    print("\nfurther model statistics (not targeted)")
    for k in CHECKS:
        print("  %-16s %.5f" % (k, r[k]))

    json.dump(dict(max_log_resid=err, rmspe=rmspe, moments=rows, params=p,
                   checks={k: float(r[k]) for k in CHECKS}),
              open(os.path.join(HERE, "calibrated.json"), "w"), indent=1)
    print("\nwritten calibrated.json")


if __name__ == "__main__":
    main()
