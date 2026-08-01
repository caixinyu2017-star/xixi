# -*- coding: utf-8 -*-
"""Estimation toolkit: two-way fixed effects, absorbed 2SLS, mediation,
propensity-score matching, entropy balancing and Oster bounds."""
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


# ---------------------------------------------------------------------------
def twfe(df, y, xs, entity="firm", time="year", cluster="firm", weights=None,
         other_effects=None, time_effects=True, two_way_cluster=False):
    """Two-way fixed-effects OLS with standard errors clustered by firm.

    `other_effects` replaces the year effects (an industry-by-year or
    province-by-year effect nests them), because at most two effect dimensions
    can be absorbed at once.
    """
    d = df.dropna(subset=[y] + list(xs)).copy()
    d = d.set_index([entity, time])
    if other_effects is not None:
        time_effects = False
    mod = PanelOLS(d[y], d[list(xs)], entity_effects=True,
                   time_effects=time_effects,
                   drop_absorbed=True,
                   weights=None if weights is None else d[weights],
                   other_effects=None if other_effects is None else d[other_effects])
    r = mod.fit(cov_type="clustered", cluster_entity=True,
                cluster_time=two_way_cluster)

    # within R-squared computed against the absorbed-effects transformation of
    # the dependent variable.  linearmodels' own rsquared_within is defined
    # relative to an entity-demeaned model and can be negative once a second
    # set of effects is absorbed, which is not a quantity to report.
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


def absorbed_2sls(df, y, endog, exog, instr, absorb=("firm", "year"),
                  cluster="firm", gmm=False):
    """2SLS (or two-step GMM) after absorbing firm and year fixed effects.

    `endog` may be a single column name or a list, so that a quadratic
    specification can instrument the level and the square jointly.
    """
    endog = [endog] if isinstance(endog, str) else list(endog)
    cols = [y] + endog + list(exog) + list(instr) + list(absorb) + [cluster]
    d = df.dropna(subset=[c for c in dict.fromkeys(cols)]).copy()
    ids = d[list(absorb)].astype("int64").to_numpy()
    algo = pyhdfe.create(ids, drop_singletons=False)
    mat = d[[y] + endog + list(exog) + list(instr)].to_numpy(float)
    res = algo.residualize(mat)
    names = [y] + endog + list(exog) + list(instr)
    R = pd.DataFrame(res, columns=names, index=d.index)

    Model = IVGMM if gmm else IV2SLS
    fit = Model(R[y], R[list(exog)], R[endog], R[list(instr)]).fit(
        cov_type="clustered", clusters=d[cluster])

    # degrees-of-freedom adjustment for the absorbed effects
    n, k = len(d), len(exog) + len(endog)
    dof_abs = algo.degrees
    adj = (n - k) / max(n - k - dof_abs, 1)
    se = fit.std_errors * np.sqrt(adj)
    t = fit.params / se
    p = pd.Series(2 * (1 - stats.norm.cdf(np.abs(t.to_numpy()))),
                  index=t.index)

    # first stage: cluster-robust Wald F on the excluded instruments, computed
    # for each endogenous regressor; the weakest one is the binding case
    fstats, fcoef = {}, {}
    for e in endog:
        fs = IV2SLS(R[e], R[list(exog) + list(instr)], None, None).fit(
            cov_type="clustered", clusters=d[cluster])
        Rmat = np.zeros((len(instr), len(fs.params)))
        for i, nm in enumerate(instr):
            Rmat[i, list(fs.params.index).index(nm)] = 1.0
        b = Rmat @ fs.params.to_numpy()
        V = Rmat @ fs.cov.to_numpy() @ Rmat.T
        fstats[e] = float(b @ np.linalg.solve(V, b)) / len(instr)
        fcoef[e] = {nm: (fs.params[nm], fs.std_errors[nm], fs.pvalues[nm])
                    for nm in instr}

    extra = dict(first_stage_F=min(fstats.values()), first_stage_F_by=fstats,
                 first_stage_coef=fcoef[endog[0]], first_stage_coef_by=fcoef,
                 n_clusters=d[cluster].nunique())
    try:
        extra["wu_hausman_p"] = float(fit.wu_hausman().pval)
    except Exception:
        pass
    if gmm:
        try:
            j = fit.j_stat
            extra["hansen_J"], extra["hansen_p"] = float(j.stat), float(j.pval)
        except Exception:
            pass
    else:
        try:
            sg = fit.sargan
            extra["sargan"], extra["sargan_p"] = float(sg.stat), float(sg.pval)
        except Exception:
            pass
    return Res(fit.params, se, t, p, len(d), fit.rsquared, extra,
               cov=fit.cov)


# ---------------------------------------------------------------------------
def bootstrap_mediation(df, y, x, med, controls, n_boot=400, seed=7,
                        cluster="firm"):
    """Block bootstrap by firm for the indirect effect a x b."""
    rng = np.random.default_rng(seed)
    a_hat = twfe(df, med, [x] + controls).params[x]
    b_hat = twfe(df, y, [x, med] + controls).params[med]
    point = a_hat * b_hat

    # row positions of every firm, computed once
    codes, firms = pd.factorize(df[cluster].to_numpy())
    order = np.argsort(codes, kind="stable")
    lo_i = np.searchsorted(codes[order], np.arange(firms.size))
    hi_i = np.searchsorted(codes[order], np.arange(firms.size), side="right")
    blocks = [order[a:b] for a, b in zip(lo_i, hi_i)]
    sizes = np.array([b.size for b in blocks])
    cols = [y, x, med] + list(controls)
    base = df[cols].to_numpy(float)
    years = df["year"].to_numpy()

    draws = np.empty(n_boot)
    for r in range(n_boot):
        pick = rng.integers(0, firms.size, firms.size)
        idx = np.concatenate([blocks[p] for p in pick])
        s = pd.DataFrame(base[idx], columns=cols)
        s["year"] = years[idx]
        s["firm"] = np.repeat(np.arange(pick.size), sizes[pick])
        try:
            a = twfe(s, med, [x] + controls).params[x]
            b = twfe(s, y, [x, med] + controls).params[med]
            draws[r] = a * b
        except Exception:
            draws[r] = np.nan
    draws = draws[~np.isnan(draws)]
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return dict(a=float(a_hat), b=float(b_hat), indirect=float(point),
                ci_low=float(lo), ci_high=float(hi), n_boot=int(draws.size),
                z=float(point / max(draws.std(), 1e-12)))


# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
def oster_delta(df, y, x, controls, absorb=("firm", "year"),
                r_max_mult=1.3, base=()):
    """Oster (2019) bounding.

    Both regressions are run on two-way demeaned data so that the R-squared is
    the standard one and increases when controls are added, which the bounding
    formula requires.
    """
    cols = [y, x] + list(base) + list(controls)
    d = df.dropna(subset=cols).copy()
    ids = d[list(absorb)].astype("int64").to_numpy()
    algo = pyhdfe.create(ids, drop_singletons=False)
    R = pd.DataFrame(algo.residualize(d[cols].to_numpy(float)), columns=cols)

    def ols(cols):
        X = np.column_stack([np.ones(len(R))] + [R[c].to_numpy() for c in cols])
        yv = R[y].to_numpy()
        b = np.linalg.lstsq(X, yv, rcond=None)[0]
        e = yv - X @ b
        r2 = 1 - e.var() / yv.var()
        return b[1], r2

    b0, r0 = ols([x] + list(base))
    b1, r1 = ols([x] + list(base) + list(controls))
    rmax = min(r_max_mult * r1, 0.999)
    den = r1 - r0
    beta_star = b1 - (b0 - b1) * (rmax - r1) / den if den > 1e-12 else np.nan
    delta = ((b1 - 0) * den) / ((b0 - b1) * (rmax - r1)) if (b0 - b1) != 0 \
        and (rmax - r1) > 0 else np.nan
    return dict(beta_uncontrolled=float(b0), r2_uncontrolled=float(r0),
                beta_controlled=float(b1), r2_controlled=float(r1),
                r_max=float(rmax), delta=float(delta),
                beta_star=float(beta_star))


def coef_equality(res_a, res_b, name):
    """Test of equality of a coefficient across two independent subsamples."""
    d = res_a.params[name] - res_b.params[name]
    se = np.sqrt(res_a.se[name] ** 2 + res_b.se[name] ** 2)
    z = d / se
    return float(d), float(se), float(z), float(2 * (1 - stats.norm.cdf(abs(z))))


# ---------------------------------------------------------------------------
# curvilinear relationships
# ---------------------------------------------------------------------------
def _quad_cov(res, lin, sq):
    """(b1, b2, 2x2 covariance) for the linear and squared terms."""
    b = np.array([res.params[lin], res.params[sq]], float)
    V = res.cov.loc[[lin, sq], [lin, sq]].to_numpy(float)
    return b, V


def utest(res, lin, sq, xl, xh):
    """Lind and Mehlum's exact test for a U or inverted-U shape.

    The composite null is that the relationship is monotone over [xl, xh].
    Under the intersection-union principle the test statistic is the smaller
    of the two one-sided statistics for the slopes at the two extremes, and
    its p-value is the larger of the two one-sided p-values.
    """
    (b1, b2), V = _quad_cov(res, lin, sq)
    out = {}
    for tag, x in (("lo", xl), ("hi", xh)):
        g = np.array([1.0, 2.0 * x])
        slope = float(g @ np.array([b1, b2]))
        se = float(np.sqrt(g @ V @ g))
        out["slope_" + tag] = slope
        out["se_" + tag] = se
        out["t_" + tag] = slope / se
    inverted = b2 < 0
    # inverted U: positive slope at the left extreme, negative at the right
    t_lo = out["t_lo"] if inverted else -out["t_lo"]
    t_hi = -out["t_hi"] if inverted else out["t_hi"]
    t = min(t_lo, t_hi)
    out.update(shape="inverted U" if inverted else "U", t=float(t),
               p=float(1 - stats.norm.cdf(t)), xl=float(xl), xh=float(xh))
    return out


def turning_point(res, lin, sq, level=0.95):
    """Extreme point of the quadratic with a delta-method standard error and
    a Fieller confidence interval, which does not require the point estimate
    of the squared term to be far from zero."""
    (b1, b2), V = _quad_cov(res, lin, sq)
    tau = -b1 / (2 * b2)
    grad = np.array([-1.0 / (2 * b2), b1 / (2 * b2 ** 2)])
    se = float(np.sqrt(grad @ V @ grad))

    # Fieller: the set of tau for which b1 + 2 b2 tau = 0 is not rejected
    z = stats.norm.ppf(0.5 + level / 2)
    A = 4 * b2 ** 2 - z ** 2 * 4 * V[1, 1]
    B = 4 * b1 * b2 - z ** 2 * 4 * V[0, 1]
    C = b1 ** 2 - z ** 2 * V[0, 0]
    disc = B ** 2 - 4 * A * C
    if A > 0 and disc > 0:
        r = np.sqrt(disc)
        lo, hi = sorted([(-B - r) / (2 * A), (-B + r) / (2 * A)])
    else:                       # unbounded: the squared term is too imprecise
        lo, hi = -np.inf, np.inf
    return dict(tau=float(tau), se=se, ci_low=float(lo), ci_high=float(hi),
                b1=float(b1), b2=float(b2))


def mod_turning(res, lin, sq, lin_z, sq_z, zs):
    """Turning point of a moderated quadratic at given values of the moderator.

    The curve is b1 x + b2 x^2 + b4 x z + b5 x^2 z, so at moderator value z the
    extreme point is -(b1 + b4 z) / (2 (b2 + b5 z)).  Standard errors come from
    the delta method on the four coefficients.
    """
    names = [lin, sq, lin_z, sq_z]
    b = np.array([res.params[n] for n in names], float)
    V = res.cov.loc[names, names].to_numpy(float)
    out = []
    for z in zs:
        num = b[0] + b[2] * z
        den = 2 * (b[1] + b[3] * z)
        tau = -num / den
        g = np.array([-1.0 / den, 2 * num / den ** 2,
                      -z / den, 2 * z * num / den ** 2])
        se = float(np.sqrt(g @ V @ g))
        out.append(dict(z=float(z), tau=float(tau), se=se,
                        curv=float(b[1] + b[3] * z)))
    # marginal displacement of the turning point per unit of the moderator,
    # evaluated at z = 0 (Haans, Pieters and He).  With
    #     tau(z) = -(b1 + b4 z) / (2 (b2 + b5 z)),
    # the derivative at z = 0 is (b1 b5 - b4 b2) / (2 b2^2).
    b1, b2, b4, b5 = b
    dtau = (b1 * b5 - b4 * b2) / (2 * b2 ** 2)
    g = np.array([b5 / (2 * b2 ** 2),
                  (b4 * b2 - 2 * b1 * b5) / (2 * b2 ** 3),
                  -1.0 / (2 * b2),
                  b1 / (2 * b2 ** 2)])
    dse = float(np.sqrt(g @ V @ g))
    return out, dict(dtau=float(dtau), se=dse,
                     p=float(2 * (1 - stats.norm.cdf(abs(dtau) / dse))))


def curve(res, lin, sq, grid, extra=None):
    """Fitted curve and a pointwise 95% band over a grid of x."""
    names = [lin, sq] + [n for n, _ in (extra or [])]
    b = np.array([res.params[n] for n in names], float)
    V = res.cov.loc[names, names].to_numpy(float)
    out = []
    for x in grid:
        g = np.array([x, x ** 2] + [v for _, v in (extra or [])], float)
        fit = float(g @ b)
        se = float(np.sqrt(g @ V @ g))
        out.append((x, fit, se))
    return np.array(out)


def two_lines(df, y, x, controls, breakpoint=None, entity="firm", time="year"):
    """Simonsohn's two-lines check: fit a separate slope on each side of an
    interior breakpoint and require them to be significant with opposite signs.
    """
    d = df.copy()
    if breakpoint is None:
        breakpoint = float(d.loc[d[x] > 0, x].median())
    d["_lo"] = np.where(d[x] <= breakpoint, d[x], breakpoint)
    d["_hi"] = np.where(d[x] > breakpoint, d[x] - breakpoint, 0.0)
    r = twfe(d, y, ["_lo", "_hi"] + list(controls), entity=entity, time=time)
    return dict(breakpoint=float(breakpoint),
                b_lo=float(r.params["_lo"]), se_lo=float(r.se["_lo"]),
                p_lo=float(r.pval["_lo"]),
                b_hi=float(r.params["_hi"]), se_hi=float(r.se["_hi"]),
                p_hi=float(r.pval["_hi"]), nobs=r.nobs)


def binscatter(df, y, x, controls, nbins=20, entity="firm", time="year",
               positive_only=True):
    """Residualised binned means of y against the raw x.

    y is purged of the controls and the two-way effects; x is left in its own
    units so that the bins are readable on the same axis as the fitted curve.
    """
    d = df.dropna(subset=[y, x] + list(controls)).copy()
    ids = d[[entity, time]].astype("int64").to_numpy()
    algo = pyhdfe.create(ids, drop_singletons=False)
    R = pd.DataFrame(algo.residualize(d[[y] + list(controls)].to_numpy(float)),
                     columns=[y] + list(controls), index=d.index)
    C = R[list(controls)].to_numpy()
    beta, *_ = np.linalg.lstsq(C, R[y].to_numpy(), rcond=None)
    d["_r"] = R[y].to_numpy() - C @ beta + d[y].mean()
    if positive_only:
        d = d[d[x] > 0]
    q = pd.qcut(d[x].rank(method="first"), nbins, labels=False)
    g = d.groupby(q).agg(x=(x, "mean"), y=("_r", "mean"), n=("_r", "size"))
    return g.reset_index(drop=True)
