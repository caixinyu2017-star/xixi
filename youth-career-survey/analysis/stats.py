# -*- coding: utf-8 -*-
"""Estimators, implemented from first principles so every number is traceable.

Contains: OLS with the usual inferential apparatus, confirmatory factor
analysis by maximum likelihood with the standard fit indices, composite
reliability, and percentile bootstrap for indirect effects.
"""
import numpy as np
from scipy import optimize, stats


# ==========================================================================
# ordinary least squares
# ==========================================================================
def ols(X, y, names=None):
    """X without an intercept column; one is added."""
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    n = X.shape[0]
    D = np.column_stack([np.ones(n), X])
    b, *_ = np.linalg.lstsq(D, y, rcond=None)
    resid = y - D @ b
    k = D.shape[1]
    dof = n - k
    s2 = resid @ resid / dof
    XtXi = np.linalg.pinv(D.T @ D)
    se = np.sqrt(np.diag(s2 * XtXi))
    t = b / se
    p = 2 * stats.t.sf(np.abs(t), dof)
    sst = ((y - y.mean()) ** 2).sum()
    r2 = 1.0 - resid @ resid / sst
    adj = 1.0 - (1.0 - r2) * (n - 1) / dof
    f = (r2 / (k - 1)) / ((1 - r2) / dof)
    return dict(b=b, se=se, t=t, p=p, r2=r2, adj_r2=adj, dof=dof, n=n,
                f=f, f_p=stats.f.sf(f, k - 1, dof), resid=resid,
                names=["(常数)"] + list(names or
                                        ["x%d" % i for i in range(X.shape[1])]))


def vif(X):
    X = np.asarray(X, float)
    out = []
    for j in range(X.shape[1]):
        other = np.delete(X, j, axis=1)
        r = ols(other, X[:, j])["r2"]
        out.append(1.0 / max(1e-12, 1.0 - r))
    return np.array(out)


def z(x):
    x = np.asarray(x, float)
    return (x - x.mean()) / x.std(ddof=1)


def delta_f(r2_full, r2_red, k_add, n, k_full):
    """F test for the increment in R squared."""
    num = (r2_full - r2_red) / k_add
    den = (1.0 - r2_full) / (n - k_full - 1)
    f = num / den
    return f, stats.f.sf(f, k_add, n - k_full - 1)


# ==========================================================================
# reliability
# ==========================================================================
def cronbach_alpha(M):
    M = np.asarray(M, float)
    k = M.shape[1]
    v = M.var(axis=0, ddof=1).sum()
    t = M.sum(axis=1).var(ddof=1)
    return k / (k - 1.0) * (1.0 - v / t)


def omega_cr_ave(loadings, residuals):
    """McDonald's omega (= composite reliability) and AVE."""
    lam = np.asarray(loadings, float)
    th = np.asarray(residuals, float)
    s = lam.sum()
    omega = s ** 2 / (s ** 2 + th.sum())
    ave = (lam ** 2).sum() / lam.size
    return float(omega), float(ave)


# ==========================================================================
# confirmatory factor analysis, maximum likelihood
# ==========================================================================
def _corr(S):
    d = np.sqrt(np.diag(S))
    return S / np.outer(d, d)


def _phi_from(par, m):
    """An unconstrained vector to a valid correlation matrix."""
    L = np.zeros((m, m))
    idx = np.tril_indices(m)
    L[idx] = par
    L[np.diag_indices(m)] = np.exp(np.clip(np.diag(L), -4, 4))
    A = L @ L.T
    d = np.sqrt(np.diag(A))
    return A / np.outer(d, d)


def cfa(data, blocks, maxiter=800):
    """Congeneric CFA with simple structure.

    data    n x p matrix of item responses
    blocks  ordered dict-like list of (factor name, list of column indices)
    Factor variances are fixed at one and every loading is free.
    """
    X = np.asarray(data, float)
    n, p = X.shape
    S = np.cov(X, rowvar=False, ddof=1)
    R = _corr(S)
    m = len(blocks)
    cols = [c for _, c in blocks]
    assign = np.zeros(p, int)
    for f, c in enumerate(cols):
        for j in c:
            assign[j] = f

    # starting values from the first principal component of each block
    lam0 = np.zeros(p)
    for f, c in enumerate(cols):
        w, V = np.linalg.eigh(R[np.ix_(c, c)])
        v = V[:, -1] * np.sqrt(w[-1])
        if v.sum() < 0:
            v = -v
        lam0[c] = np.clip(np.abs(v), 0.35, 0.92)
    th0 = np.log(np.clip(1.0 - lam0 ** 2, 0.05, 0.95))
    ph0 = np.zeros(m * (m + 1) // 2)
    di = [i * (i + 3) // 2 for i in range(m)]
    ph0[di] = 0.0
    x0 = np.concatenate([lam0, th0, ph0])

    ldS = np.linalg.slogdet(R)[1]

    def unpack(par):
        lam = par[:p]
        th = np.exp(np.clip(par[p:2 * p], -6, 2))
        phi = _phi_from(par[2 * p:], m)
        return lam, th, phi

    def sigma(par):
        lam, th, phi = unpack(par)
        L = np.zeros((p, m))
        L[np.arange(p), assign] = lam
        return L @ phi @ L.T + np.diag(th)

    def fml(par):
        Sg = sigma(par)
        try:
            c = np.linalg.cholesky(Sg)
        except np.linalg.LinAlgError:
            return 1e6
        ld = 2.0 * np.log(np.diag(c)).sum()
        sol = np.linalg.solve(Sg, R)
        return ld + np.trace(sol) - ldS - p

    res = optimize.minimize(fml, x0, method="L-BFGS-B",
                            options=dict(maxiter=maxiter, maxfun=200000))
    lam, th, phi = unpack(res.x)
    Sg = sigma(res.x)

    n_par = p + p + m * (m - 1) // 2
    df = p * (p + 1) // 2 - n_par
    chi2 = (n - 1) * max(res.fun, 0.0)

    # independence model
    f_null = np.log(np.prod(np.diag(R))) - ldS
    chi2_n = (n - 1) * f_null
    df_n = p * (p - 1) // 2

    d1 = max(chi2 - df, 0.0)
    d0 = max(chi2_n - df_n, d1, 1e-9)
    cfi = 1.0 - d1 / d0
    tli = ((chi2_n / df_n) - (chi2 / df)) / ((chi2_n / df_n) - 1.0)
    rmsea = np.sqrt(d1 / (df * (n - 1)))
    resid = R - _corr(Sg)
    tri = np.tril_indices(p)
    srmr = np.sqrt((resid[tri] ** 2).mean())

    return dict(loadings=lam, residuals=th, phi=phi, assign=assign,
                chi2=float(chi2), df=int(df), ratio=float(chi2 / df),
                cfi=float(np.clip(cfi, 0, 1)), tli=float(np.clip(tli, 0, 1)),
                rmsea=float(rmsea), srmr=float(srmr), fmin=float(res.fun),
                names=[b for b, _ in blocks], converged=bool(res.success))


def htmt(data, blocks):
    """Heterotrait–monotrait ratio, for discriminant validity."""
    X = np.asarray(data, float)
    R = np.abs(_corr(np.cov(X, rowvar=False, ddof=1)))
    m = len(blocks)
    out = np.eye(m)
    for i in range(m):
        ci = blocks[i][1]
        mi = R[np.ix_(ci, ci)][np.triu_indices(len(ci), 1)].mean()
        for j in range(i + 1, m):
            cj = blocks[j][1]
            mj = R[np.ix_(cj, cj)][np.triu_indices(len(cj), 1)].mean()
            het = R[np.ix_(ci, cj)].mean()
            out[i, j] = out[j, i] = het / np.sqrt(mi * mj)
    return out


# ==========================================================================
# common method bias
# ==========================================================================
def harman(X):
    """Share of variance taken by the first unrotated component."""
    R = _corr(np.cov(np.asarray(X, float), rowvar=False, ddof=1))
    w = np.linalg.eigvalsh(R)[::-1]
    return float(w[0] / w.sum()), [float(v) for v in w[:5]]


def partial_corr(a, b, c):
    """Correlation of a and b with c partialled out."""
    ra, rb = a - np.polyval(np.polyfit(c, a, 1), c), \
        b - np.polyval(np.polyfit(c, b, 1), c)
    return float(np.corrcoef(ra, rb)[0, 1])


# ==========================================================================
# mediation
# ==========================================================================
def serial_mediation(x, m1, m2, y, cov=None, boots=5000, seed=7):
    """x -> m1 -> m2 -> y, with all three indirect paths."""
    rng = np.random.default_rng(seed)
    n = x.size
    cov = np.zeros((n, 0)) if cov is None else np.asarray(cov, float)

    def fit(xi, m1i, m2i, yi, ci):
        a1 = ols(np.column_stack([xi, ci]), m1i)["b"][1]
        pm2 = ols(np.column_stack([xi, m1i, ci]), m2i)["b"]
        a2, d21 = pm2[1], pm2[2]
        py = ols(np.column_stack([xi, m1i, m2i, ci]), yi)["b"]
        cp, b1, b2 = py[1], py[2], py[3]
        return dict(a1=a1, a2=a2, d21=d21, b1=b1, b2=b2, cdash=cp,
                    ind_m1=a1 * b1, ind_m2=a2 * b2, ind_serial=a1 * d21 * b2,
                    total_ind=a1 * b1 + a2 * b2 + a1 * d21 * b2)

    point = fit(x, m1, m2, y, cov)
    keys = ["ind_m1", "ind_m2", "ind_serial", "total_ind"]
    draws = {k: np.empty(boots) for k in keys}
    for b in range(boots):
        i = rng.integers(0, n, n)
        f = fit(x[i], m1[i], m2[i], y[i], cov[i])
        for k in keys:
            draws[k][b] = f[k]
    point["ci"] = {k: (float(np.percentile(draws[k], 2.5)),
                       float(np.percentile(draws[k], 97.5))) for k in keys}
    point["total"] = ols(np.column_stack([x, cov]), y)["b"][1]
    return point


def simple_slopes(x, w, y, cov=None):
    """Slope of y on x at minus and plus one standard deviation of w."""
    n = x.size
    cov = np.zeros((n, 0)) if cov is None else np.asarray(cov, float)
    D = np.column_stack([x, w, x * w, cov])
    r = ols(D, y)
    b_x, b_int = r["b"][1], r["b"][3]
    sd = w.std(ddof=1)
    return dict(low=float(b_x - b_int * sd), high=float(b_x + b_int * sd),
                inter=float(b_int), fit=r)


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    n = 4000
    f1 = rng.standard_normal(n)
    f2 = 0.5 * f1 + np.sqrt(1 - 0.25) * rng.standard_normal(n)
    X = np.column_stack(
        [0.8 * f1 + 0.6 * rng.standard_normal(n) for _ in range(4)]
        + [0.75 * f2 + np.sqrt(1 - 0.5625) * rng.standard_normal(n)
           for _ in range(4)])
    r = cfa(X, [("F1", [0, 1, 2, 3]), ("F2", [4, 5, 6, 7])])
    print("自检 CFA：载荷均值 %.2f（真值 0.80/0.75），因子相关 %.2f（真值 0.50）"
          % (r["loadings"].mean(), r["phi"][0, 1]))
    print("        CFI %.3f  TLI %.3f  RMSEA %.3f  SRMR %.3f"
          % (r["cfi"], r["tli"], r["rmsea"], r["srmr"]))

    x = rng.standard_normal(n)
    m1 = 0.5 * x + rng.standard_normal(n)
    m2 = 0.4 * m1 + 0.2 * x + rng.standard_normal(n)
    yv = -0.3 * m2 + 0.25 * x + rng.standard_normal(n)
    s = serial_mediation(x, m1, m2, yv, boots=400, seed=1)
    print("自检 中介：a1=%.2f(0.50) b2=%.2f(-0.30) 链式=%.3f(%.3f)"
          % (s["a1"], s["b2"], s["ind_serial"], 0.5 * 0.4 * -0.3))
