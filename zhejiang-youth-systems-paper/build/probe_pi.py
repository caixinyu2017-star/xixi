import json
import numpy as np
from scipy.optimize import root
import model as M

P = dict(json.load(open("calibrated.json"))["params"])
STARTS = [M.GUESS_LOW, M.GUESS_HIGH,
          np.array([125., 25., 4993., 749., 0.62, 0.75]),
          np.array([3745., 9987., 4993., 2996., 0.55, 0.50]),
          np.array([999., 1997., 3745., 1498., 0.58, 0.60]),
          np.array([7490., 22470., 3745., 3745., 0.52, 0.45]),
          np.array([300., 60., 4200., 900., 0.60, 0.66]),
          np.array([15000., 40000., 2000., 2000., 0.50, 0.40])]

def eqs(p, t):
    found = []
    for g in STARTS:
        s = root(lambda z: M.rhs(t, np.abs(z), p), g, method="hybr", tol=1e-12)
        y = np.abs(s.x)
        if float(np.max(np.abs(M.rhs(t, y, p)))) < 1e-6 and (y[:4] > 1e-3).all():
            n = M.indicators(t, y, p)["NER"]
            if not any(abs(n - f[0]) < 2e-3 for f in found):
                ev = np.linalg.eigvals(M.jacobian(t, y, p))
                found.append((float(n), float(np.max(ev.real))))
    return sorted(found)

print("multi-start equilibria vs Pi at t=25 (base Pi=%.3f)" % P["Pi"])
for pi in [0.4, 0.7, 1.0, 1.3, 1.6, 1.87, 2.0, 2.2, 2.4, 2.6]:
    f = eqs(dict(P, Pi=pi), 25.0)
    tag = "  <-- BISTABLE" if sum(1 for _, e in f if e < 0) > 1 else ""
    print("  Pi=%.2f  n=%d  %s%s" % (pi, len(f),
          [(round(a, 4), round(b, 4)) for a, b in f], tag))
