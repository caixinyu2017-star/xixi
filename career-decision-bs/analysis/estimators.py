# -*- coding: utf-8 -*-
"""The analysis a researcher would actually run on a cross-section.

This module implements, from first principles, the procedure that dominates
the career decision-making literature and that the study being reproduced
used: a conditional process analysis combining an indirect path through
career decision-making self-efficacy with a moderated direct path, estimated
by ordinary least squares with percentile bootstrap confidence intervals.

It is implemented here rather than taken from a package so that what the
simulated researcher does is fully specified and auditable, and so that it can
be applied thousands of times inside the sensitivity analysis.

Model, in the notation of the conditional process literature:

    M = i1 + a X + e1                            (X -> M)
    Y = i2 + c' X + b M + w W + z (X * W) + e2   (direct, mediated, moderated)

with X career anxiety, M self-efficacy, Y decision difficulty and W perceived
parental support. The indirect effect is a*b; the moderated direct effect at a
given level of W is c' + z W.
"""
from __future__ import annotations

import numpy as np


def ols(X, y):
    """Least squares with an intercept prepended. Returns (beta, se, t)."""
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    n = X.shape[0]
    A = np.column_stack([np.ones(n), X])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ beta
    dof = n - A.shape[1]
    s2 = float(resid @ resid) / dof
    xtxi = np.linalg.pinv(A.T @ A)
    se = np.sqrt(np.clip(np.diag(xtxi) * s2, 0, None))
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(se > 0, beta / se, np.nan)
    return beta, se, t, dof


def _z(x):
    x = np.asarray(x, float)
    sd = x.std(ddof=1)
    return (x - x.mean()) / (sd if sd > 0 else 1.0)


def conditional_process(X, M, Y, W, boots=5000, seed=17, center=True):
    """Estimate the conditional process model and bootstrap the key effects."""
    X = np.asarray(X, float); M = np.asarray(M, float)
    Y = np.asarray(Y, float); W = np.asarray(W, float)
    if center:
        Xc, Mc, Wc = X - X.mean(), M - M.mean(), W - W.mean()
    else:
        Xc, Mc, Wc = X, M, W

    def fit(xi, mi, yi, wi):
        ba, *_ = ols(xi, mi)                      # a path
        a = ba[1]
        des = np.column_stack([xi, mi, wi, xi * wi])
        bb, se, t, dof = ols(des, yi)
        return dict(a=a, cdash=bb[1], b=bb[2], w=bb[3], inter=bb[4],
                    se=se, t=t, dof=dof, indirect=a * bb[2])

    est = fit(Xc, Mc, Y, Wc)

    rng = np.random.default_rng(seed)
    n = X.size
    ind = np.empty(boots)
    intr = np.empty(boots)
    for i in range(boots):
        k = rng.integers(0, n, n)
        f = fit(Xc[k], Mc[k], Y[k], Wc[k])
        ind[i] = f["indirect"]
        intr[i] = f["inter"]
    est["indirect_ci"] = (float(np.percentile(ind, 2.5)),
                          float(np.percentile(ind, 97.5)))
    est["inter_ci"] = (float(np.percentile(intr, 2.5)),
                       float(np.percentile(intr, 97.5)))

    # simple slopes of X on Y at the conventional +/- 1 SD of the moderator
    sdw = W.std(ddof=1)
    est["slope_lo"] = est["cdash"] + est["inter"] * (-sdw)
    est["slope_hi"] = est["cdash"] + est["inter"] * (sdw)
    est["sd_w"] = float(sdw)
    est["total"] = est["cdash"] + est["indirect"]
    return est


def standardised(X, M, Y, W, **kw):
    """The same model on standardised variables, for comparability."""
    return conditional_process(_z(X), _z(M), _z(Y), _z(W), **kw)


def _selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        if not c:
            print("FAIL:", m); ok = False

    rng = np.random.default_rng(0)
    n = 4000
    X = rng.normal(size=n)
    W = rng.normal(size=n)
    # known truth: a = 0.5, b = -0.4, c' = 0.3, interaction = 0.25
    M = 0.5 * X + rng.normal(size=n) * 0.6
    Y = 0.3 * X - 0.4 * M + 0.1 * W + 0.25 * X * W + rng.normal(size=n) * 0.5
    e = conditional_process(X, M, Y, W, boots=400, seed=1)

    chk(abs(e["a"] - 0.5) < 0.05, "a recovered: %.3f" % e["a"])
    chk(abs(e["b"] + 0.4) < 0.05, "b recovered: %.3f" % e["b"])
    chk(abs(e["cdash"] - 0.3) < 0.05, "c' recovered: %.3f" % e["cdash"])
    chk(abs(e["inter"] - 0.25) < 0.05, "interaction recovered: %.3f" % e["inter"])
    chk(abs(e["indirect"] + 0.2) < 0.05, "indirect recovered: %.3f" % e["indirect"])
    lo, hi = e["indirect_ci"]
    chk(lo < -0.2 < hi, "indirect CI covers the truth")
    chk(e["slope_hi"] > e["slope_lo"], "positive interaction steepens the slope")

    # OLS must agree with the closed-form simple regression slope
    b, se, t, dof = ols(X, Y)
    chk(abs(b[1] - np.cov(X, Y)[0, 1] / np.var(X, ddof=1)) < 1e-9,
        "OLS slope matches the covariance formula")

    print("estimators.py self-test:", "PASSED" if ok else "FAILED")
    print("  recovered a %.3f (0.500)  b %.3f (-0.400)  c' %.3f (0.300)"
          % (e["a"], e["b"], e["cdash"]))
    print("  interaction %.3f (0.250), 95%% CI [%.3f, %.3f]"
          % (e["inter"], e["inter_ci"][0], e["inter_ci"][1]))
    print("  indirect    %.3f (-0.200), 95%% CI [%.3f, %.3f]"
          % (e["indirect"], lo, hi))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
