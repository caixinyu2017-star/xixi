# -*- coding: utf-8 -*-
"""Paper 9 — calibration.

The calibration is deliberately anchored on the economy *before* the technology shock,
not on the economy we observe today.  The reason is substantive rather than technical.
In this model a field with a high marginal product posts more vacancies, so it pays a
higher wage *and* has a lower unemployment rate; the configuration observed in
computing since 2023 — a high early-career wage together with an unusually high
new-graduate unemployment rate — is therefore not a stationary equilibrium of the model
at all.  It is what the model produces part-way through an adjustment, when a cohort
sized for the old demand meets the new one.  Calibrating to the pre-shock economy and
then asking whether the shock reproduces today's configuration turns the current data
from a target into a test.

Two normalisations come first.  Matching efficiency and the vacancy cost enter every
equilibrium object only through their ratio, so the vacancy cost is set to one; only
relative field productivity matters, so the unexposed field's is set to one.

Estimated:  mu    matching efficiency
            A0    relative productivity of the exposed field
            beta  intensity of choice in the field decision
            amen  relative amenity of the exposed field, a flow

Targeted:   the share of the cohort entering the exposed field
            the new-graduate unemployment rate outside the exposed field
            the early-career wage premium of the exposed field
            the elasticity of field choice to the relative wage

Not targeted, and therefore available as checks: the new-graduate unemployment rate
*inside* the exposed field, the whole transition after the shock, and every dynamic
property of the system.
"""
import json
import os

import numpy as np
from scipy.optimize import least_squares

import p9_model as M

HERE = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------- pre-shock targets
TARGETS = dict(
    share=0.055,        # computing's share of the graduating cohort before the shock
    u_other=0.055,      # new-graduate unemployment rate outside computing
    premium=1.350,      # early-career wage of computing, relative to other fields
    supply_elast=0.600  # d log share / d log relative wage
)

EXTERNAL = dict(D=4, r=0.04, alpha=0.5, eta=0.5, delta=0.10, gam=1.0/7.0,
                sigma=2.0, b=0.40)

KEYS = ['share', 'u_other', 'premium', 'supply_elast']


def new_grad_unemployment(p, E):
    """Share of a field's graduating cohort still searching after one year."""
    return np.exp(-M.market(p, E)['f'])


def moments(p):
    s_star, st, mkt = M.steady_state(p)
    u = new_grad_unemployment(p, st.E)
    m = dict(share=s_star,
             u_exposed=float(u[0]),
             u_other=float(u[1]),
             premium=float(mkt['w'][0] / mkt['w'][1]),
             supply_elast=float(M.supply_elasticity(p, s_star)))
    return m, s_star, st, mkt


def _params(x):
    mu, A0, beta = np.exp(x[:3])
    p = M.Params(**EXTERNAL)
    p.mu, p.beta, p.amen, p.kappa = mu, beta, x[3], 1.0
    p.A = np.array([A0, 1.0])
    return p


def residuals(x, targets):
    try:
        m, _, _, _ = moments(_params(x))
    except Exception:
        return np.full(len(KEYS), 10.0)
    return np.array([np.log(m[k] / targets[k]) for k in KEYS])


def calibrate(targets=None, external=None, verbose=True):
    targets = dict(targets or TARGETS)
    global EXTERNAL
    if external is not None:
        saved, EXTERNAL = EXTERNAL, dict(external)
    try:
        x0 = np.array([np.log(2.8), np.log(0.12), np.log(0.6), -0.5])
        sol = least_squares(residuals, x0, args=(targets,), xtol=3e-16, ftol=3e-16,
                            gtol=3e-16, max_nfev=6000)
        p = _params(sol.x)
        m, s_star, st, mkt = moments(p)
    finally:
        if external is not None:
            EXTERNAL = saved
    err = float(np.max(np.abs(sol.fun)))
    if verbose:
        print('max abs log deviation %.3e' % err)
        for k in KEYS:
            print('   %-13s target %8.4f   model %8.4f' % (k, targets[k], m[k]))
        print('   %-13s   (check) %8s   model %8.4f' % ('u_exposed', '-', m['u_exposed']))
    return p, m, s_star, st, mkt, err


def diagnostics(p, s_star, st, mkt):
    """Objects the calibration did not target.

    The dominant mode is measured by perturbing the stationary state and reading the
    response, which works whether or not the belief system is switching; under anchored
    beliefs it agrees with the D-th roots of the loop gain, which is the analytical
    benchmark reported alongside it.
    """
    g = float(M.loop_gain(p, s_star))
    dm = M.dominant_mode(p, st)
    mod = dm['modulus']
    half = float('inf') if mod >= 1 or mod <= 0 else float(np.log(0.5) / np.log(mod))
    return dict(loop_gain=g,
                analytical_modulus=float(abs(g) ** (1.0 / p.D)),
                analytical_period=float(2.0 * p.D),
                dominant_modulus=float(mod),
                dominant_period=float(dm['period']),
                adjustment_half_life=half,
                job_finding=[float(v) for v in mkt['f']],
                tightness=[float(v) for v in mkt['theta']],
                employment=[float(v) for v in st.E],
                searchers=[float(v) for v in st.U],
                wages=[float(v) for v in mkt['w']],
                output=float(mkt['Y']),
                value=[float(v) for v in mkt['V']],
                relative_demand=float(p.A[0] ** ((p.sigma - 1.0) / p.sigma)))


if __name__ == '__main__':
    p, m, s_star, st, mkt, err = calibrate()
    d = diagnostics(p, s_star, st, mkt)
    print()
    print('estimated: mu %.4f  A0 %.5f  beta %.4f  amen %.4f'
          % (p.mu, p.A[0], p.beta, p.amen))
    print('loop gain %.4f | analytical modulus %.4f | dominant modulus %.4f'
          % (d['loop_gain'], d['analytical_modulus'], d['dominant_modulus']))
    print('adjustment half-life %.1f y' % d['adjustment_half_life'])
