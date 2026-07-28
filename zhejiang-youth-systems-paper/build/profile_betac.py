# -*- coding: utf-8 -*-
"""Profile the calibration loss over the choice-sharpness parameter beta_c."""
import json
import numpy as np
from scipy.optimize import differential_evolution

import model as M
import calibrate as C

FREE0 = list(C.FREE)
rows = []
for bc in [6, 10, 15, 20, 25, 30, 40]:
    C.FREE = [f for f in FREE0 if f[0] != "beta_c"]
    orig = M.BASE
    M.BASE = dict(orig, beta_c=bc)
    r = differential_evolution(C.evaluate, [(lo, hi) for _, lo, hi in C.FREE],
                               seed=11, maxiter=250, popsize=22, tol=1e-11,
                               polish=True, init="sobol")
    loss, _, p = C.evaluate(r.x, full=True)
    M.BASE = orig
    rows.append(dict(beta_c=bc, loss=loss, **{k: p[k] for k, _, _ in C.FREE}))
    print("beta_c=%5.1f loss=%.6f  mu=%.2f Pi=%.3f nu=%.3f sigma0=%.3f eps=%.3f"
          % (bc, loss, p["mu"], p["Pi"], p["nu"], p["sigma0"], p["eps_pw"]),
          flush=True)
json.dump(rows, open("profile_betac.json", "w"), indent=1)
