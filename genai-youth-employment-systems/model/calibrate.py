# -*- coding: utf-8 -*-
"""Calibrate the diffusion parameters of the model to documented stylised facts.

Targets
  T1  relative decline of early-career employment 3 years after the shock:
      -15 %   [Brynjolfsson, Chandar & Chen 2025: 13-16 % for ages 22-25 in
               AI-exposed occupations]
  T2  share of workers regularly using GenAI 2 years after the shock: 0.45
      [Humlum & Vestergaard 2025: widespread adoption within two years]
  T3  peak productivity uplift of early-career workers: ~0.25-0.30
      [Brynjolfsson, Li & Raymond 2025; Cui et al. 2026; Noy & Zhang 2023]
"""
from dataclasses import replace

import numpy as np
from scipy.optimize import brentq, least_squares

import sdmodel as M


def run_pair(p, T=25.0, dt=0.0625):
    return (M.simulate(p, T=T, dt=dt, genai=False),
            M.simulate(p, T=T, dt=dt, genai=True))


def diagnostics(p, T=25.0, dt=0.0625):
    r0, r1 = run_pair(p, T, dt)
    idx = lambda t: int(round(t / dt))
    return {
        "J3": 100.0 * (r1["J"][idx(3)] / r0["J"][idx(3)] - 1.0),
        "u2": r1["u"][idx(2)],
        "piJ_peak": r1["piJ"].max() / p.piJ0 - 1.0,
        "piS_peak": r1["piS"].max() / p.piS0 - 1.0,
        "alpha25": r1["alpha"][-1],
        "C10": 100.0 * (r1["C"][min(idx(10), len(r1["C"]) - 1)]
                        / r0["C"][min(idx(10), len(r0["C"]) - 1)] - 1.0),
        "J_end": 100.0 * (r1["J"][-1] / r0["J"][-1] - 1.0),
        "S_end": 100.0 * (r1["S"][-1] / r0["S"][-1] - 1.0),
    }, r0, r1


TARGETS = {"J3": -15.0, "u2": 0.45, "piJ_peak": 0.27, "piS_peak": 0.090}
COMPRESSION = 3.0   # novice / expert productivity-gain ratio


def make(z, base):
    tF, nu, a_u, beta_J = z
    return replace(base, tF=float(tF), nu=float(nu), a_u=float(a_u),
                   beta_J=float(beta_J), beta_S=float(beta_J) / COMPRESSION,
                   m=M.mentoring_coefficient(base))


def residuals(z, base):
    d, _, _ = diagnostics(make(z, base), T=25.0)
    return [(d[k] - v) / abs(v) for k, v in TARGETS.items()]


if __name__ == "__main__":
    base = M.Params(gF=1.0)
    sol = least_squares(residuals, x0=[1.5, 1.0, 0.30, 0.55], args=(base,),
                        bounds=([0.0, 0.2, 0.10, 0.10], [6.0, 4.0, 0.90, 1.20]))
    p = make(sol.x, base)
    print("tF=%.4f nu=%.4f a_u=%.4f beta_J=%.4f beta_S=%.4f  cost=%.3e"
          % (p.tF, p.nu, p.a_u, p.beta_J, p.beta_S, sol.cost))
    d, r0, r1 = diagnostics(p)
    for k, v in d.items():
        tgt = TARGETS.get(k)
        print("  %-9s %9.4f %s" % (k, v, "" if tgt is None else "(target %.3f)" % tgt))
