# -*- coding: utf-8 -*-
"""Panel estimators, implemented from first principles.

Four ways of estimating the same interaction:

    cross_section  one wave at a time — what a single-wave study reports
    pooled         all waves stacked, person-clustered standard errors
    within         person fixed effects — the within-person estimate
    hybrid         Mundlak's device: the same regression carrying separate
                   between-person and within-person slopes, so the two can be
                   compared inside one model and their equality tested

All variance estimates cluster on the person, because repeated observations of
one worker are not independent.
"""
import numpy as np
from scipy import stats


# ==========================================================================
# building blocks
# ==========================================================================
def _prep(X):
    X = np.asarray(X, float)
    return X[:, None] if X.ndim == 1 else X


def cluster_vcov(D, resid, groups, dof_correct=True):
    """Cluster-robust covariance, clustering on `groups`."""
    n, k = D.shape
    XtXi = np.linalg.pinv(D.T @ D)
    meat = np.zeros((k, k))
    uniq = np.unique(groups)
    for g in uniq:
        m = groups == g
        s = D[m].T @ resid[m]
        meat += np.outer(s, s)
    V = XtXi @ meat @ XtXi
    if dof_correct:
        G = uniq.size
        V *= (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    return V, uniq.size


def _fit(D, y, groups, names, dof, absorbed=0):
    b, *_ = np.linalg.lstsq(D, y, rcond=None)
    resid = y - D @ b
    V, G = cluster_vcov(D, resid, groups)
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    t = np.divide(b, se, out=np.zeros_like(b), where=se > 0)
    p = 2 * stats.t.sf(np.abs(t), max(dof, 1))
    sst = ((y - y.mean()) ** 2).sum()
    r2 = 1.0 - resid @ resid / sst if sst > 0 else np.nan
    return dict(b=b, se=se, t=t, p=p, V=V, resid=resid, r2=r2,
                n=y.size, n_group=G, dof=dof, names=list(names),
                absorbed=absorbed)


def _index(res, name):
    return res["names"].index(name)


def coef(res, name):
    i = _index(res, name)
    return dict(b=float(res["b"][i]), se=float(res["se"][i]),
                t=float(res["t"][i]), p=float(res["p"][i]))


# ==========================================================================
# estimators
# ==========================================================================
def ols(X, y, groups, names=None, intercept=True):
    X = _prep(X)
    names = list(names or ["x%d" % i for i in range(X.shape[1])])
    D = np.column_stack([np.ones(X.shape[0]), X]) if intercept else X
    nm = (["(const)"] + names) if intercept else names
    G = np.unique(groups).size
    return _fit(D, y, groups, nm, dof=G - 1)


def demean(v, pid):
    """Subtract each person's own mean."""
    v = np.asarray(v, float)
    out = np.empty_like(v)
    order = np.argsort(pid, kind="stable")
    p = pid[order]
    s = v[order] if v.ndim == 1 else v[order, :]
    edges = np.flatnonzero(np.r_[True, p[1:] != p[:-1], True])
    for a, b in zip(edges[:-1], edges[1:]):
        blk = s[a:b]
        s[a:b] = blk - blk.mean(axis=0)
    out[order] = s
    return out


def person_mean(v, pid):
    """Replace each value by that person's mean of the variable."""
    v = np.asarray(v, float)
    out = np.empty_like(v)
    order = np.argsort(pid, kind="stable")
    p = pid[order]
    s = v[order] if v.ndim == 1 else v[order, :]
    edges = np.flatnonzero(np.r_[True, p[1:] != p[:-1], True])
    for a, b in zip(edges[:-1], edges[1:]):
        blk = s[a:b]
        s[a:b] = np.repeat(blk.mean(axis=0, keepdims=True), b - a, axis=0)
    out[order] = s
    return out


def within(X, y, pid, names=None):
    """Person fixed effects, by the within transformation."""
    X = _prep(X)
    names = list(names or ["x%d" % i for i in range(X.shape[1])])
    Xd, yd = demean(X, pid), demean(y, pid)
    G = np.unique(pid).size
    r = _fit(Xd, yd, pid, names, dof=G - 1, absorbed=G)
    # within R squared, on the demeaned outcome
    r["r2_within"] = r["r2"]
    return r


def hybrid(Xw, Xb, y, pid, names_w, names_b, extra=None, names_extra=None):
    """Mundlak's within-between specification.

    Xw enters twice: once demeaned (the within slope) and once as the person
    mean (which, together with the within slope, gives the between slope).
    Variables in Xb are person-level and enter once.
    """
    Xw = _prep(Xw)
    parts = [demean(Xw, pid), person_mean(Xw, pid)]
    nm = (["%s (within)" % s for s in names_w]
          + ["%s (between)" % s for s in names_b])
    if Xb is not None and np.size(Xb):
        parts.append(_prep(Xb))
        nm += list(names_extra or [])
    elif extra is not None and np.size(extra):
        parts.append(_prep(extra))
        nm += list(names_extra or [])
    D = np.column_stack([np.ones(y.size)] + parts)
    G = np.unique(pid).size
    return _fit(D, y, pid, ["(const)"] + nm, dof=G - 1)


def contrast(res, a, b):
    """Test that two coefficients are equal, using the clustered covariance."""
    i, j = _index(res, a), _index(res, b)
    d = res["b"][i] - res["b"][j]
    v = res["V"][i, i] + res["V"][j, j] - 2 * res["V"][i, j]
    se = np.sqrt(max(v, 0.0))
    t = d / se if se > 0 else 0.0
    return dict(diff=float(d), se=float(se), t=float(t),
                p=float(2 * stats.t.sf(abs(t), max(res["dof"], 1))))


def cross_section(X, y, groups, names, wave, waves):
    """One wave only, as a single-wave study would estimate it."""
    m = waves == wave
    if m.sum() < 40:
        return None
    Xi = _prep(X)[m]
    keep = [j for j in range(Xi.shape[1]) if Xi[:, j].std() > 1e-9]
    if len(keep) < Xi.shape[1]:
        return None
    return ols(Xi, y[m], groups[m], names)


# ==========================================================================
# self-test
# ==========================================================================
def _selftest():
    """Two synthetic checks with analytically known answers.

    (a) No sorting: the person effect does not enter the outcome, so the
        between and within slopes are exactly the values put in.
    (b) Sorting: the person effect enters both x and y, so pooled OLS is
        biased while the within estimator is not.
    """
    rng = np.random.default_rng(11)
    n_p, n_t = 900, 6
    pid = np.repeat(np.arange(n_p), n_t)
    alpha = rng.normal(0, 1.4, n_p)[pid]
    w = rng.normal(0, 1, n_p)[pid]
    B_W, B_B, B_INT = 0.30, 0.90, -0.25
    ok = True

    # ---- (a) no sorting: x is independent of the person effect
    x = rng.normal(0, 1, n_p)[pid] + rng.normal(0, 1, pid.size)
    xb, xw = person_mean(x, pid), demean(x, pid)
    y = B_W * xw + B_B * xb + B_INT * x * w + 0.5 * w + \
        rng.normal(0, 0.8, pid.size)
    r_w = within(np.column_stack([x, x * w]), y, pid, ["x", "xw"])
    r_h = hybrid(np.column_stack([x, x * w]), np.column_stack([w]), y, pid,
                 ["x", "xw"], ["x", "xw"], names_extra=["w"])
    bw, bb = coef(r_w, "x")["b"], coef(r_h, "x (between)")["b"]
    bi = coef(r_w, "xw")["b"]
    print("self-test (a) no sorting — true within %.2f, between %.2f, "
          "interaction %.2f" % (B_W, B_B, B_INT))
    print("      within %+.3f   between %+.3f   interaction %+.3f"
          % (bw, bb, bi))
    ok &= (abs(bw - B_W) < .04 and abs(bb - B_B) < .06
           and abs(bi - B_INT) < .04)

    # ---- (b) sorting: x depends on the person effect, which also raises y
    x = 0.7 * alpha + rng.normal(0, 1, pid.size)
    xb, xw = person_mean(x, pid), demean(x, pid)
    y = B_W * xw + B_B * xb + B_INT * x * w + 0.5 * w + alpha + \
        rng.normal(0, 0.8, pid.size)
    r_p = ols(np.column_stack([x, w, x * w]), y, pid, ["x", "w", "xw"])
    r_w = within(np.column_stack([x, x * w]), y, pid, ["x", "xw"])
    r_h = hybrid(np.column_stack([x, x * w]), np.column_stack([w]), y, pid,
                 ["x", "xw"], ["x", "xw"], names_extra=["w"])
    c = contrast(r_h, "x (within)", "x (between)")
    # the between slope now also carries the person effect that x proxies for
    expect_b = B_B + np.cov(alpha, xb)[0, 1] / np.var(xb)
    print("self-test (b) with sorting — within stays %.2f, between becomes "
          "%.2f" % (B_W, expect_b))
    print("      pooled %+.3f (biased)   within %+.3f   between %+.3f"
          % (coef(r_p, "x")["b"], coef(r_w, "x")["b"],
             coef(r_h, "x (between)")["b"]))
    print("      equality of within and between: t = %+.1f, p = %.4f"
          % (c["t"], c["p"]))
    ok &= (abs(coef(r_w, "x")["b"] - B_W) < .04
           and abs(coef(r_h, "x (between)")["b"] - expect_b) < .08
           and abs(coef(r_p, "x")["b"] - B_W) > .3
           and c["p"] < .001)

    naive = np.sqrt(np.diag(np.linalg.pinv(
        np.column_stack([np.ones(pid.size), x]).T
        @ np.column_stack([np.ones(pid.size), x]))
        * (r_p["resid"] @ r_p["resid"]) / (pid.size - 2)))[1]
    ratio = coef(r_p, "x")["se"] / naive
    print("      person-clustered SE %.4f vs naive %.4f (ratio %.2f)"
          % (coef(r_p, "x")["se"], naive, ratio))
    ok &= ratio > 1.2
    return ok


if __name__ == "__main__":
    print("PASS" if _selftest() else "FAIL")
