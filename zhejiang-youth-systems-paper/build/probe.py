import json

import numpy as np
from scipy.optimize import root

import model as M

P = dict(json.load(open("calibrated.json"))["params"])

STARTS = [M.GUESS_LOW, M.GUESS_HIGH,
          np.array([125., 25., 4993., 749., 0.62, 0.75]),
          np.array([3745., 9987., 4993., 2996., 0.55, 0.50]),
          np.array([999., 1997., 3745., 1498., 0.58, 0.60]),
          np.array([7490., 22470., 3745., 3745., 0.52, 0.45])]


def eqs(p, t):
    found = []
    for g in STARTS:
        s = root(lambda z: M.rhs(t, np.abs(z), p), g, method="hybr", tol=1e-12)
        y = np.abs(s.x)
        if float(np.max(np.abs(M.rhs(t, y, p)))) < 1e-7 and (y[:4] > 1e-4).all():
            ner = M.indicators(t, y, p)["NER"]
            if not any(abs(ner - f[0]) < 1e-3 for f in found):
                ev = np.linalg.eigvals(M.jacobian(t, y, p))
                found.append((float(ner), float(np.max(ev.real))))
    return sorted(found)


def scan(name, values, t=25.0):
    print("--- scan %s at t=%.0f" % (name, t))
    for v in values:
        f = eqs(dict(P, **{name: v}), t)
        print("  %s=%.3f n=%d %s" % (name, v, len(f),
                                     [(round(a, 3), round(b, 3)) for a, b in f]))


scan("kappa2", [0.0, 0.15, 0.3, 0.5, 0.8, 1.2, 1.8, 2.5])
scan("beta_s", [3, 6, 9, 12, 16, 22])
scan("beta_a", [3, 7, 12, 18, 25])
scan("zeta", [0.30, 0.45, 0.55, 0.70, 0.85])
scan("beta_c", [10, 20, 40, 70])

print("--- beta_c flatness of the calibration loss")
import calibrate as C
for bc in [10, 20, 30, 40, 60, 90]:
    orig = M.BASE
    M.BASE = dict(orig, beta_c=bc)
    v = [P[n] if n != "beta_c" else bc for n, _, _ in C.FREE]
    print("  beta_c=%3d loss=%.5f" % (bc, C.evaluate(v)))
    M.BASE = orig
