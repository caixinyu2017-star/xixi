# -*- coding: utf-8 -*-
"""Estimation toolkit.

Two-way fixed-effects least squares, Poisson pseudo-maximum likelihood with
two absorbed effect dimensions, absorbed two-stage least squares, stacked
cross-equation tests, the wild cluster bootstrap, dynamic difference in
differences and Oster bounds.  Everything reports standard errors clustered
on the firm unless stated otherwise.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pyhdfe
from scipy import stats
from linearmodels.iv import IV2SLS, IVGMM
from linearmodels.panel import PanelOLS


# ---------------------------------------------------------------------------
def stars(p):
    return "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.10 else ""))


def fmt(b, se, p, d=3):
    return "%.*f%s" % (d, b, stars(p)), "(%.*f)" % (d, se)


class Res:
    """Uniform container for a regression result."""

    def __init__(self, params, se, tstat, pval, nobs, r2, extra=None, cov=None):
        self.params, self.se = pd.Series(params), pd.Series(se)
        self.tstat, self.pval = pd.Series(tstat), pd.Series(pval)
        self.nobs, self.r2 = int(nobs), float(r2)
        self.extra = extra or {}
        self.cov = cov

    def cell(self, name, d=3):
        if name not in self.params.index:
            return "", ""
        return fmt(self.params[name], self.se[name], self.pval[name], d)


def _cluster_cov(X, u, groups, dof_extra=0):
    """Cluster-robust sandwich for a linear score X'u."""
    XtX_inv = np.linalg.pinv(X.T @ X)
    codes = pd.factorize(groups)[0]
    G = codes.max() + 1
    S = np.zeros((X.shape[1], X.shape[1]))
    S_g = np.zeros((G, X.shape[1]))
    np.add.at(S_g, codes, X * u[:, None])
    S = S_g.T @ S_g
    n, k = X.shape
    adj = (G / (G - 1.0)) * ((n - 1.0) / (n - k - dof_extra))
    return XtX_inv @ S @ XtX_inv * adj, G


# ---------------------------------------------------------------------------
def twfe(df, y, xs, entity="firm", time="year", cluster="firm", weights=None,
         other_effects=None, time_effects=True, two_way_cluster=False):
    """Two-way fixed-effects least squares, standard errors clustered by firm.

    `other_effects` replaces the year effects, because at most two effect
    dimensions can be absorbed at once and an industry-by-year effect nests
    the year effect.
    """
    d = df.dropna(subset=[y] + list(xs)).copy()
    d = d.set_index([entity, time])
    if other_effects is not None:
        time_effects = False
    mod = PanelOLS(d[y], d[list(xs)], entity_effects=True,
                   time_effects=time_effects, drop_absorbed=True,
                   weights=None if weights is None else d[weights],
                   other_effects=None if other_effects is None
                   else d[other_effects])
    r = mod.fit(cov_type="clustered", cluster_entity=True,
                cluster_time=two_way_cluster)

    # within R-squared against the absorbed-effects transform of y; the
    # package's own rsquared_within is defined relative to an entity-demeaned
    # model and can be negative once a second effect set is absorbed
    ids = np.column_stack([
        pd.factorize(d.index.get_level_values(0))[0],
        pd.factorize(d.index.get_level_values(1))[0]
        if other_effects is None else
        pd.factorize(d[other_effects[0]])[0]]).astype("int64")
    yd = pyhdfe.create(ids, drop_singletons=False).residualize(
        d[[y]].to_numpy(float))[:, 0]
    sst = float((yd ** 2).sum())
    ssr = float((np.asarray(r.resids) ** 2).sum())
    r2 = 1.0 - ssr / sst if sst > 0 else float("nan")
    return Res(r.params, r.std_errors, r.tstats, r.pvalues, r.nobs, r2,
               cov=r.cov)


# ---------------------------------------------------------------------------
def ppml(df, y, xs, absorb=("firm", "year"), cluster="firm", offset=None,
         tol=1e-9, maxiter=120):
    """Poisson pseudo-maximum likelihood with two absorbed effect dimensions.

    The fixed effects are profiled out: for a given slope vector the Poisson
    effects solve a set of adding-up conditions in closed form, so the score
    and Hessian for the slopes are those of the weighted within transform.
    Iterating the two steps is the algorithm of Correia, Guimaraes and Zylkin.
    Standard errors are the clustered sandwich, which is what makes the
    estimator a quasi-likelihood one and robust to any variance-mean relation.
    """
    cols = [y] + list(xs) + list(absorb) + [cluster] + \
           ([offset] if offset else [])
    d = df.dropna(subset=list(dict.fromkeys(cols))).copy()
    yv = d[y].to_numpy(float)
    X = d[list(xs)].to_numpy(float)
    off = d[offset].to_numpy(float) if offset else np.zeros(len(d))
    ids = [pd.factorize(d[a])[0] for a in absorb]
    sizes = [c.max() + 1 for c in ids]

    b = np.zeros(X.shape[1])
    fe = [np.zeros(s) for s in sizes]
    fe[0] = np.log(np.maximum(yv.mean(), 1e-6)) * np.ones(sizes[0])
    eta = off + X @ b + sum(f[c] for f, c in zip(fe, ids))
    dev_old = np.inf

    for _ in range(maxiter):
        mu = np.exp(np.clip(eta, -30, 30))
        # exact update of each effect given the others (Poisson closed form)
        for _ in range(6):
            for j, c in enumerate(ids):
                num = np.bincount(c, weights=yv, minlength=sizes[j])
                den = np.bincount(c, weights=np.exp(np.clip(
                    off + X @ b + sum(f[cc] for k, (f, cc)
                                      in enumerate(zip(fe, ids)) if k != j),
                    -30, 30)), minlength=sizes[j])
                fe[j] = np.log(np.maximum(num, 1e-10)
                               / np.maximum(den, 1e-10))
        eta = off + X @ b + sum(f[c] for f, c in zip(fe, ids))
        mu = np.exp(np.clip(eta, -30, 30))

        # weighted within transform of X, weights mu
        Xw = _wdemean(X, ids, sizes, mu)
        score = Xw.T @ (yv - mu)
        H = Xw.T @ (Xw * mu[:, None])
        step = np.linalg.solve(H + 1e-10 * np.eye(H.shape[0]), score)
        b = b + np.clip(step, -1.0, 1.0)
        eta = off + X @ b + sum(f[c] for f, c in zip(fe, ids))

        mu = np.exp(np.clip(eta, -30, 30))
        dev = 2 * np.sum(np.where(yv > 0, yv * np.log(np.maximum(yv, 1e-12) / mu),
                                  0.0) - (yv - mu))
        if abs(dev_old - dev) < tol * (abs(dev) + 1e-6):
            break
        dev_old = dev

    Xw = _wdemean(X, ids, sizes, mu)
    H = Xw.T @ (Xw * mu[:, None])
    H_inv = np.linalg.pinv(H)
    codes = pd.factorize(d[cluster])[0]
    G = codes.max() + 1
    S_g = np.zeros((G, X.shape[1]))
    np.add.at(S_g, codes, Xw * (yv - mu)[:, None])
    n, k = X.shape
    adj = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    V = H_inv @ (S_g.T @ S_g) @ H_inv * adj
    se = np.sqrt(np.diag(V))
    t = b / se
    p = 2 * (1 - stats.norm.cdf(np.abs(t)))

    ybar = np.bincount(ids[0], weights=yv, minlength=sizes[0])
    ll = np.sum(yv * np.log(np.maximum(mu, 1e-12)) - mu)
    r2 = 1.0 - dev / max(dev0(yv, ids, sizes, off), 1e-12)
    idx = list(xs)
    return Res(pd.Series(b, index=idx), pd.Series(se, index=idx),
               pd.Series(t, index=idx), pd.Series(p, index=idx), n, r2,
               extra=dict(loglik=float(ll), deviance=float(dev),
                          n_clusters=int(G), converged=bool(abs(step).max() < 1e-4)),
               cov=pd.DataFrame(V, index=idx, columns=idx))


def dev0(yv, ids, sizes, off):
    """Deviance of the effects-only Poisson model, for a pseudo R-squared."""
    fe = [np.zeros(s) for s in sizes]
    fe[0] = np.log(np.maximum(yv.mean(), 1e-6)) * np.ones(sizes[0])
    for _ in range(60):
        for j, c in enumerate(ids):
            num = np.bincount(c, weights=yv, minlength=sizes[j])
            den = np.bincount(c, weights=np.exp(np.clip(
                off + sum(f[cc] for k, (f, cc) in enumerate(zip(fe, ids))
                          if k != j), -30, 30)), minlength=sizes[j])
            fe[j] = np.log(np.maximum(num, 1e-10) / np.maximum(den, 1e-10))
    mu = np.exp(np.clip(off + sum(f[c] for f, c in zip(fe, ids)), -30, 30))
    return 2 * np.sum(np.where(yv > 0,
                               yv * np.log(np.maximum(yv, 1e-12) / mu), 0.0)
                      - (yv - mu))


def _wdemean(X, ids, sizes, w, iters=40, tol=1e-10):
    """Alternating projections: within transform with observation weights."""
    Z = X.copy()
    for _ in range(iters):
        prev = Z
        for c, s in zip(ids, sizes):
            sw = np.bincount(c, weights=w, minlength=s)
            for j in range(Z.shape[1]):
                m = np.bincount(c, weights=w * Z[:, j], minlength=s) / \
                    np.maximum(sw, 1e-12)
                Z[:, j] = Z[:, j] - m[c]
        if np.max(np.abs(Z - prev)) < tol:
            break
    return Z


# ---------------------------------------------------------------------------
def absorbed_2sls(df, y, endog, exog, instr, absorb=("firm", "year"),
                  cluster="firm", gmm=False):
    """Two-stage least squares (or two-step GMM) after absorbing the effects."""
    endog = [endog] if isinstance(endog, str) else list(endog)
    cols = [y] + endog + list(exog) + list(instr) + list(absorb) + [cluster]
    d = df.dropna(subset=[c for c in dict.fromkeys(cols)]).copy()
    ids = np.column_stack([pd.factorize(d[a])[0] for a in absorb]).astype("int64")
    algo = pyhdfe.create(ids, drop_singletons=False)
    names = [y] + endog + list(exog) + list(instr)
    R = pd.DataFrame(algo.residualize(d[names].to_numpy(float)),
                     columns=names, index=d.index)

    Model = IVGMM if gmm else IV2SLS
    fit = Model(R[y], R[list(exog)], R[endog], R[list(instr)]).fit(
        cov_type="clustered", clusters=d[cluster])

    n, k = len(d), len(exog) + len(endog)
    adj = (n - k) / max(n - k - algo.degrees, 1)
    se = fit.std_errors * np.sqrt(adj)
    t = fit.params / se
    p = pd.Series(2 * (1 - stats.norm.cdf(np.abs(t.to_numpy()))), index=t.index)

    fstats, fcoef = {}, {}
    for e in endog:
        fs = IV2SLS(R[e], R[list(exog) + list(instr)], None, None).fit(
            cov_type="clustered", clusters=d[cluster])
        Rmat = np.zeros((len(instr), len(fs.params)))
        for i, nm in enumerate(instr):
            Rmat[i, list(fs.params.index).index(nm)] = 1.0
        bb = Rmat @ fs.params.to_numpy()
        V = Rmat @ fs.cov.to_numpy() @ Rmat.T
        fstats[e] = float(bb @ np.linalg.solve(V, bb)) / len(instr)
        fcoef[e] = {nm: (fs.params[nm], fs.std_errors[nm], fs.pvalues[nm])
                    for nm in instr}

    extra = dict(first_stage_F=min(fstats.values()),
                 first_stage_coef=fcoef[endog[0]],
                 n_clusters=int(d[cluster].nunique()))
    try:
        extra["wu_hausman_p"] = float(fit.wu_hausman().pval)
    except Exception:
        pass
    try:
        j = fit.j_stat if gmm else fit.sargan
        extra["hansen_J"], extra["hansen_p"] = float(j.stat), float(j.pval)
    except Exception:
        pass
    return Res(fit.params, se, t, p, len(d), fit.rsquared, extra, cov=fit.cov)


# ---------------------------------------------------------------------------
def stacked_test(df, ya, yb, xs, key, entity="firm", time="year",
                 cluster="firm"):
    """Cross-equation test that a coefficient is equal in two outcomes.

    The two equations are stacked and every regressor is interacted with an
    equation indicator, so a single clustered covariance matrix covers both;
    the test on the interacted key regressor is then a Wald test that allows
    the two equations' errors to be correlated within the firm.
    """
    keep = list(dict.fromkeys([entity, time, cluster] + list(xs)))
    a = df[keep + [ya]].rename(columns={ya: "_y"}).assign(_eq=0)
    b = df[keep + [yb]].rename(columns={yb: "_y"}).assign(_eq=1)
    s = pd.concat([a, b], ignore_index=True).dropna().reset_index(drop=True)
    s["_unit"] = s[entity].astype("int64") * 2 + s["_eq"]
    s["_per"] = s[time].astype("int64") * 2 + s["_eq"]
    inter = []
    for c in xs:
        nm = c + "_D"
        s[nm] = s[c] * s["_eq"]
        inter.append(nm)
    d = s.set_index(["_unit", "_per"])
    # the clustered covariance uses the firm, so that the two equations'
    # errors are allowed to be correlated within the same firm
    fit = PanelOLS(d["_y"], d[list(xs) + inter], entity_effects=True,
                   time_effects=True, drop_absorbed=True).fit(
        cov_type="clustered", clusters=d[cluster])
    nm = key + "_D"
    return dict(diff=float(fit.params[nm]), se=float(fit.std_errors[nm]),
                t=float(fit.tstats[nm]), p=float(fit.pvalues[nm]),
                b_a=float(fit.params[key]),
                b_b=float(fit.params[key] + fit.params[nm]), nobs=int(fit.nobs))


# ---------------------------------------------------------------------------
def wild_bootstrap(df, y, xs, key, entity="firm", time="year", cluster="firm",
                   reps=999, seed=3, absorb=("firm", "year")):
    """Restricted wild cluster bootstrap p-value (Rademacher weights).

    The null is imposed before resampling, which is what makes the procedure
    reliable when the number of clusters is modest or the regressor of
    interest is unevenly distributed across them.
    """
    cols = [y] + list(xs)
    d = df.dropna(subset=cols + list(absorb) + [cluster]).copy()
    ids = np.column_stack([pd.factorize(d[a])[0] for a in absorb]).astype("int64")
    algo = pyhdfe.create(ids, drop_singletons=False)
    R = algo.residualize(d[cols].to_numpy(float))
    yv, X = R[:, 0], R[:, 1:]
    names = list(xs)
    kpos = names.index(key)
    codes = pd.factorize(d[cluster])[0]
    G = codes.max() + 1

    def tstat(yvec):
        b = np.linalg.lstsq(X, yvec, rcond=None)[0]
        u = yvec - X @ b
        V, _ = _cluster_cov(X, u, codes, dof_extra=algo.degrees)
        return b[kpos] / np.sqrt(V[kpos, kpos])

    t_obs = tstat(yv)
    keep = [j for j in range(X.shape[1]) if j != kpos]
    Xr = X[:, keep]
    br = np.linalg.lstsq(Xr, yv, rcond=None)[0]
    fit_r = Xr @ br
    u_r = yv - fit_r

    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(reps):
        v = rng.choice([-1.0, 1.0], size=G)[codes]
        cnt += abs(tstat(fit_r + v * u_r)) >= abs(t_obs) - 1e-12
    return dict(t=float(t_obs), p=float((cnt + 1) / (reps + 1)), reps=int(reps),
                n_clusters=int(G))


# ---------------------------------------------------------------------------
def event_study(df, y, treat, controls, base_year, years, entity="firm",
                time="year", cluster="firm"):
    """Dynamic difference in differences with the base year omitted."""
    d = df.copy()
    terms = []
    for yr in years:
        if yr == base_year:
            continue
        nm = "D%d" % yr
        d[nm] = d[treat] * (d[time] == yr).astype(float)
        terms.append((yr, nm))
    r = twfe(d, y, [nm for _, nm in terms] + list(controls), entity=entity,
             time=time, cluster=cluster)
    pre = [nm for yr, nm in terms if yr < base_year]
    b = r.params[pre].to_numpy()
    V = r.cov.loc[pre, pre].to_numpy()
    w = float(b @ np.linalg.solve(V, b))
    p = float(1 - stats.chi2.cdf(w, len(pre)))
    return r, terms, dict(pretrend_chi2=w, pretrend_df=len(pre),
                          pretrend_p=p)


# ---------------------------------------------------------------------------
def randomisation(df, y, xs, key, controls, reps=500, seed=17, entity="firm",
                  time="year"):
    """Randomisation inference: permute the regressor of interest within year."""
    rng = np.random.default_rng(seed)
    base = twfe(df, y, xs, entity=entity, time=time).params[key]
    d = df.copy()
    draws = np.empty(reps)
    grp = d.groupby(time).indices
    v = d[key].to_numpy(float)
    for r in range(reps):
        w = v.copy()
        for _, pos in grp.items():
            w[pos] = rng.permutation(v[pos])
        d["_perm"] = w
        try:
            xs2 = ["_perm" if c == key else c for c in xs]
            draws[r] = twfe(d, y, xs2, entity=entity, time=time).params["_perm"]
        except Exception:
            draws[r] = np.nan
    draws = draws[~np.isnan(draws)]
    p = float((np.abs(draws) >= abs(base)).sum() + 1) / (draws.size + 1)
    return dict(actual=float(base), p=p, reps=int(draws.size),
                sd=float(draws.std()))


# ---------------------------------------------------------------------------
def oster_delta(df, y, x, controls, absorb=("firm", "year"), r_max_mult=1.3,
                base=()):
    """Oster (2019) coefficient-stability bound.

    Both regressions run on two-way demeaned data so that the R-squared is the
    ordinary one and rises when controls are added, as the formula requires.
    """
    cols = [y, x] + list(base) + list(controls)
    d = df.dropna(subset=cols).copy()
    ids = np.column_stack([pd.factorize(d[a])[0] for a in absorb]).astype("int64")
    algo = pyhdfe.create(ids, drop_singletons=False)
    R = pd.DataFrame(algo.residualize(d[cols].to_numpy(float)), columns=cols)

    def ols(cc):
        X = np.column_stack([np.ones(len(R))] + [R[c].to_numpy() for c in cc])
        yv = R[y].to_numpy()
        b = np.linalg.lstsq(X, yv, rcond=None)[0]
        e = yv - X @ b
        return b[1], 1 - e.var() / yv.var()

    b0, r0 = ols([x] + list(base))
    b1, r1 = ols([x] + list(base) + list(controls))
    rmax = min(r_max_mult * r1, 0.999)
    den = r1 - r0
    beta_star = b1 - (b0 - b1) * (rmax - r1) / den if den > 1e-12 else np.nan
    delta = (b1 * den) / ((b0 - b1) * (rmax - r1)) \
        if (b0 - b1) != 0 and (rmax - r1) > 0 else np.nan
    return dict(beta_uncontrolled=float(b0), r2_uncontrolled=float(r0),
                beta_controlled=float(b1), r2_controlled=float(r1),
                r_max=float(rmax), delta=float(delta),
                beta_star=float(beta_star))


def coef_equality(res_a, res_b, name):
    """Equality of a coefficient across two independent subsamples."""
    d = res_a.params[name] - res_b.params[name]
    se = np.sqrt(res_a.se[name] ** 2 + res_b.se[name] ** 2)
    z = d / se
    return float(d), float(se), float(z), float(2 * (1 - stats.norm.cdf(abs(z))))


def margin(res, key, mod, zs):
    """Marginal effect of `key` at given values of a moderator."""
    b = np.array([res.params[key], res.params[mod]], float)
    V = res.cov.loc[[key, mod], [key, mod]].to_numpy(float)
    out = []
    for z in zs:
        g = np.array([1.0, z])
        m = float(g @ b)
        se = float(np.sqrt(g @ V @ g))
        out.append(dict(z=float(z), effect=m, se=se,
                        p=float(2 * (1 - stats.norm.cdf(abs(m / se))))))
    return out


def vif(df, cols):
    """Variance inflation factors after the two-way within transform."""
    d = df.dropna(subset=cols + ["firm", "year"]).copy()
    ids = np.column_stack([pd.factorize(d[a])[0]
                           for a in ("firm", "year")]).astype("int64")
    R = pyhdfe.create(ids, drop_singletons=False).residualize(
        d[cols].to_numpy(float))
    out = {}
    for j, c in enumerate(cols):
        Xo = np.column_stack([np.ones(len(R))] +
                             [R[:, k] for k in range(R.shape[1]) if k != j])
        yv = R[:, j]
        b = np.linalg.lstsq(Xo, yv, rcond=None)[0]
        e = yv - Xo @ b
        r2 = 1 - e.var() / yv.var()
        out[c] = float(1.0 / max(1 - r2, 1e-9))
    return out
