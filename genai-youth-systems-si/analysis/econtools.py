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
from scipy.optimize import minimize
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


# ---------------------------------------------------------------------------
# mediation and feedback
# ---------------------------------------------------------------------------
def mediation(df, y, x, med, controls, entity="firm", time="year",
              n_boot=500, seed=7, cluster="firm"):
    """Three-step mediation with a block-bootstrapped indirect effect.

    Step 1 regresses the outcome on the treatment, step 2 the mediator on the
    treatment, step 3 the outcome on both.  The indirect effect is the product
    of the step-2 coefficient and the mediator coefficient in step 3, and its
    confidence interval comes from a bootstrap that resamples whole firms, so
    the within-firm dependence of the panel is preserved.
    """
    s1 = twfe(df, y, [x] + list(controls), entity=entity, time=time)
    s2 = twfe(df, med, [x] + list(controls), entity=entity, time=time)
    s3 = twfe(df, y, [x, med] + list(controls), entity=entity, time=time)
    a, b = float(s2.params[x]), float(s3.params[med])
    point = a * b

    rng = np.random.default_rng(seed)
    codes, units = pd.factorize(df[cluster].to_numpy())
    order = np.argsort(codes, kind="stable")
    lo = np.searchsorted(codes[order], np.arange(units.size))
    hi = np.searchsorted(codes[order], np.arange(units.size), side="right")
    blocks = [order[i:j] for i, j in zip(lo, hi)]
    sizes = np.array([b_.size for b_ in blocks])
    cols = [y, x, med] + list(controls)
    base = df[cols].to_numpy(float)
    yrs = df[time].to_numpy()

    draws = np.empty(n_boot)
    for r in range(n_boot):
        pick = rng.integers(0, units.size, units.size)
        idx = np.concatenate([blocks[p] for p in pick])
        s = pd.DataFrame(base[idx], columns=cols)
        s[time] = yrs[idx]
        s[entity] = np.repeat(np.arange(pick.size), sizes[pick])
        try:
            aa = twfe(s, med, [x] + list(controls), entity=entity,
                      time=time).params[x]
            bb = twfe(s, y, [x, med] + list(controls), entity=entity,
                      time=time).params[med]
            draws[r] = aa * bb
        except Exception:
            draws[r] = np.nan
    draws = draws[~np.isnan(draws)]
    lo_ci, hi_ci = np.percentile(draws, [2.5, 97.5])
    tot = float(s1.params[x])
    return dict(total=tot, se_total=float(s1.se[x]), p_total=float(s1.pval[x]),
                a=a, se_a=float(s2.se[x]), p_a=float(s2.pval[x]),
                b=b, se_b=float(s3.se[med]), p_b=float(s3.pval[med]),
                direct=float(s3.params[x]), se_direct=float(s3.se[x]),
                p_direct=float(s3.pval[x]),
                indirect=float(point), ci_low=float(lo_ci),
                ci_high=float(hi_ci), n_boot=int(draws.size),
                share=float(100 * point / tot) if tot != 0 else float("nan"),
                res=(s1, s2, s3))


def helmert(d, cols, entity="firm", time="year"):
    """Forward orthogonal deviations.

    Subtracting the mean of all *future* observations and rescaling removes the
    unit effect without correlating the transformed error with lagged levels,
    which is what makes lagged levels admissible instruments in a dynamic
    panel.  This is the transformation used in the panel vector autoregression
    literature in place of first differencing.
    """
    out = []
    for _, g in d.sort_values([entity, time]).groupby(entity, sort=False):
        v = g[cols].to_numpy(float)
        T = len(g)
        if T < 3:
            continue
        z = np.empty((T - 1, len(cols)))
        for t in range(T - 1):
            fut = v[t + 1:].mean(axis=0)
            c = np.sqrt((T - t - 1) / (T - t))
            z[t] = c * (v[t] - fut)
        h = g.iloc[:T - 1].copy()
        for k, c in enumerate(cols):
            h[c + "_h"] = z[:, k]
        out.append(h)
    return pd.concat(out, ignore_index=True)


def pvar(df, cols, entity="firm", time="year", lags=1, n_boot=400, seed=13,
         horizon=8, time_demean=True, jackknife=True):
    """Panel vector autoregression for firm-level deviations.

    Each equation of the k-variate system is estimated on data from which the
    common time effects have been removed by cross-sectional demeaning within
    each year and the firm effects by within transformation, so the dynamics
    are those of firm-level departures from the aggregate diffusion path.
    Because the series are persistent, the lagged-level instruments of the
    difference and forward-orthogonal-deviation estimators are weak here, so
    the leading term of the dynamic-panel bias is removed instead by the
    half-panel jackknife of Chudik, Pesaran and Yang (2018),

        A_hpj = 2 A_full - (A_first half + A_second half) / 2,

    and inference is by a bootstrap that resamples whole firms.  The routine
    returns the corrected coefficient matrix with bootstrap standard errors,
    panel Granger causality Wald tests for every ordered pair, the moduli of
    the companion eigenvalues, and orthogonalised impulse responses with
    bootstrap bands.
    """
    k = len(cols)
    d = df[[entity, time] + list(cols)].dropna().sort_values(
        [entity, time]).reset_index(drop=True)
    if time_demean:
        for c in cols:
            d[c] = d[c] - d.groupby(time)[c].transform("mean")
    for c in cols:
        for L in range(1, lags + 1):
            d[c + "_L%d" % L] = d.groupby(entity)[c].shift(L)
    xlist = [c + "_L%d" % L for L in range(1, lags + 1) for c in cols]
    d = d.dropna(subset=xlist).reset_index(drop=True)
    # firms need at least three usable periods for the jackknife split
    n_per = d.groupby(entity)[time].transform("size")
    d = d[n_per >= 3].reset_index(drop=True)

    def _within(frame):
        """Within-firm demeaning of the outcomes and the regressors."""
        M = frame[list(cols) + xlist].to_numpy(float)
        codes, uniq = pd.factorize(frame[entity])
        sums = np.zeros((len(uniq), M.shape[1]))
        np.add.at(sums, codes, M)
        cnt = np.bincount(codes, minlength=len(uniq)).astype(float)
        return M - (sums / cnt[:, None])[codes], codes, len(uniq)

    def _fit(frame):
        W, codes, G = _within(frame)
        Y, X = W[:, :k], W[:, k:]
        XtX = X.T @ X
        B = np.linalg.solve(XtX, X.T @ Y)          # (k*lags) x k
        U = Y - X @ B
        return B.T, U, X, codes, G                 # A is k x (k*lags)

    A_full, U, X, codes, G = _fit(d)
    nobs = len(d)

    if jackknife:
        rank = d.groupby(entity)[time].rank(method="first")
        size = d.groupby(entity)[time].transform("size")
        half = np.ceil(size / 2.0)
        lo = d[rank <= half]
        hi = d[rank > size - half]
        try:
            A_lo = _fit(lo)[0]
            A_hi = _fit(hi)[0]
            A = 2.0 * A_full - 0.5 * (A_lo + A_hi)
        except Exception:
            A = A_full
    else:
        A = A_full

    S = (U.T @ U) / max(nobs - k * lags - 1, 1)

    def companion(Amat):
        if lags == 1:
            return Amat
        C = np.zeros((k * lags, k * lags))
        C[:k] = Amat
        C[k:, :-k] = np.eye(k * (lags - 1))
        return C

    eig = np.abs(np.linalg.eigvals(companion(A)))

    def irf_of(Amat, Pmat):
        C = companion(Amat)
        out = np.zeros((horizon + 1, k, k))
        M = np.eye(k * lags)
        for h in range(horizon + 1):
            out[h] = M[:k, :k] @ Pmat
            M = M @ C
        return out

    P = np.linalg.cholesky(S + 1e-12 * np.eye(k))
    IRF = irf_of(A, P)

    # ------------------------------------------------------------ bootstrap
    rng = np.random.default_rng(seed)
    units = d[entity].unique()
    pos = {u: g.to_numpy() for u, g in d.groupby(entity).indices.items()} \
        if False else {u: np.flatnonzero(d[entity].to_numpy() == u)
                       for u in units}
    draws = np.empty((n_boot, horizon + 1, k, k))
    coefs = np.empty((n_boot, k, k * lags))
    ok = 0
    for _ in range(n_boot):
        pick = rng.choice(units, units.size, replace=True)
        rows = np.concatenate([pos[u] for u in pick])
        fr = d.iloc[rows].copy()
        fr[entity] = np.repeat(np.arange(units.size),
                               [len(pos[u]) for u in pick])
        try:
            Ab = _fit(fr)[0]
            if jackknife:
                rk = fr.groupby(entity)[time].rank(method="first")
                sz = fr.groupby(entity)[time].transform("size")
                hf = np.ceil(sz / 2.0)
                Ab = 2.0 * Ab - 0.5 * (_fit(fr[rk <= hf])[0]
                                       + _fit(fr[rk > sz - hf])[0])
            Ub = _fit(fr)[1]
            Sb = (Ub.T @ Ub) / max(len(fr) - k * lags - 1, 1)
            draws[ok] = irf_of(Ab, np.linalg.cholesky(Sb + 1e-12 * np.eye(k)))
            coefs[ok] = Ab
            ok += 1
        except Exception:
            pass
    draws, coefs = draws[:ok], coefs[:ok]
    lo_b = np.percentile(draws, 5, axis=0)
    hi_b = np.percentile(draws, 95, axis=0)
    se = coefs.std(axis=0, ddof=1)

    # ------------------------------------------- panel Granger causality
    gc = {}
    for i in range(k):
        for j, cj in enumerate(cols):
            idx = [L * k + j for L in range(lags)]
            b = A[i, idx]
            V = np.cov(coefs[:, i, idx], rowvar=False)
            V = np.atleast_2d(V)
            w = float(b @ np.linalg.solve(V + 1e-14 * np.eye(len(idx)), b))
            gc[(cols[i], cj)] = dict(
                chi2=w, df=lags, p=float(1 - stats.chi2.cdf(w, lags)),
                coef=float(A[i, idx[0]]), se=float(se[i, idx[0]]))
    return dict(A=A, A_uncorrected=A_full, se=se, cols=list(cols), eig=eig,
                max_eig=float(eig.max()), irf=IRF, irf_lo=lo_b, irf_hi=hi_b,
                gc=gc, nobs=int(nobs), n_firms=int(G), n_boot=int(ok),
                horizon=int(horizon), sigma=S)


# --------------------------------------------------------------------------
def std_bias(t, c, wt=None, wc=None):
    mt = np.average(t, weights=wt)
    mc = np.average(c, weights=wc)
    vt = np.average((t - mt) ** 2, weights=wt)
    vc = np.average((c - mc) ** 2, weights=wc)
    return 100 * (mt - mc) / np.sqrt((vt + vc) / 2)


def psm(df, covars, treat="Treat", caliper=0.02, k=1, seed=11):
    """Firm-level 1:k nearest-neighbour matching on the pre-shock covariates."""
    rng = np.random.default_rng(seed)
    pre = df[df.Post == 0].groupby("firm").agg(
        {**{c: "mean" for c in covars}, treat: "max"}).dropna()
    X = pre[covars].to_numpy(float)
    X = (X - X.mean(0)) / X.std(0)
    Tr = pre[treat].to_numpy(float)
    import statsmodels.api as sm
    logit = sm.Logit(Tr, sm.add_constant(X)).fit(disp=0)
    ps = logit.predict(sm.add_constant(X))
    pre = pre.assign(ps=ps)

    ti = np.flatnonzero(Tr == 1)
    ci = np.flatnonzero(Tr == 0)
    order = rng.permutation(ti)
    used, pairs = set(), []
    for i in order:
        cand = [j for j in ci if j not in used and abs(ps[j] - ps[i]) <= caliper]
        if not cand:
            continue
        cand.sort(key=lambda j: abs(ps[j] - ps[i]))
        take = cand[:k]
        used.update(take)
        pairs.append((i, take))

    keep_idx = sorted({i for i, _ in pairs} | used)
    kept = pre.index.to_numpy()[keep_idx]

    bal = []
    for c in covars:
        t_all = pre.loc[pre[treat] == 1, c].to_numpy()
        c_all = pre.loc[pre[treat] == 0, c].to_numpy()
        m = pre.loc[kept]
        t_m = m.loc[m[treat] == 1, c].to_numpy()
        c_m = m.loc[m[treat] == 0, c].to_numpy()
        b_u, b_m = std_bias(t_all, c_all), std_bias(t_m, c_m)
        tt = stats.ttest_ind(t_m, c_m, equal_var=False)
        bal.append(dict(var=c, bias_u=b_u, bias_m=b_m,
                        reduct=100 * (1 - abs(b_m) / max(abs(b_u), 1e-9)),
                        t=float(tt.statistic), p=float(tt.pvalue)))
    return df[df.firm.isin(kept)].copy(), pd.DataFrame(bal), pre.assign(kept=pre.index.isin(kept))


def entropy_balance(df, covars, treat="Treat"):
    """Hainmueller entropy balancing on the first two moments."""
    pre = df[df.Post == 0].groupby("firm").agg(
        {**{c: "mean" for c in covars}, treat: "max"}).dropna()
    T = pre[treat].to_numpy() == 1
    Z = pre[covars].to_numpy(float)
    Z = (Z - Z.mean(0)) / Z.std(0)
    M = np.column_stack([Z, Z ** 2])
    target = M[T].mean(0)
    Mc = M[~T]

    def obj(lam):
        w = np.exp(-Mc @ lam)
        w = w / w.sum()
        return np.log(np.sum(np.exp(-Mc @ lam))) + lam @ target

    out = minimize(obj, np.zeros(M.shape[1]), method="BFGS",
                   options=dict(maxiter=800))
    w = np.exp(-Mc @ out.x)
    w = w / w.sum() * T.sum()
    wts = pd.Series(1.0, index=pre.index)
    wts.loc[pre.index[~T]] = w
    return df.merge(wts.rename("ebw"), left_on="firm", right_index=True,
                    how="inner")
