# -*- coding: utf-8 -*-
"""First-principles statistical tools for the EU-27 analysis.

Everything is implemented directly on numpy/scipy primitives so that each
number in the manuscript can be traced to a formula in this file:

*   single-predictor multivariate general linear models in a MANOVA-type
    framework (Pillai's Trace, Wilks' Lambda, exact F for one hypothesis
    degree of freedom, univariate parameter estimates with partial eta
    squared);
*   regression diagnostics (Shapiro-Wilk on residuals, leverage, Cook's
    distance);
*   exploratory factor analysis by Principal Axis Factoring on the
    correlation matrix (KMO, Bartlett's test of sphericity, iterated
    communalities, regression-method factor scores);
*   simple linear regression in the SPSS reporting layout (model summary,
    ANOVA block, coefficient block);
*   hierarchical agglomerative clustering with Pearson-correlation
    proximity and average linkage, k-means, cluster ANOVA and the average
    silhouette coefficient.
"""
from __future__ import annotations

import numpy as np
from scipy import stats as st


# ---------------------------------------------------------------------------
# ordinary least squares with the classical covariance (SPSS layout)
# ---------------------------------------------------------------------------
class OLS:
    def __init__(self, y, X):
        y = np.asarray(y, float)
        X = np.asarray(X, float)
        self.n, self.k = X.shape
        self.df = self.n - self.k
        XtX = X.T @ X
        self.XtX_inv = np.linalg.inv(XtX)
        self.b = self.XtX_inv @ X.T @ y
        self.fitted = X @ self.b
        self.resid = y - self.fitted
        self.sse = float(self.resid @ self.resid)
        self.sst = float(((y - y.mean()) ** 2).sum())
        self.ssr = self.sst - self.sse
        self.s2 = self.sse / self.df
        self.se = np.sqrt(np.diag(self.XtX_inv) * self.s2)
        self.t = self.b / self.se
        self.p = 2 * st.t.sf(np.abs(self.t), self.df)
        self.r2 = 1.0 - self.sse / self.sst
        self.adj_r2 = 1.0 - (1.0 - self.r2) * (self.n - 1) / self.df
        self.see = float(np.sqrt(self.s2))          # std. error of estimate
        kx = self.k - 1                             # slope terms
        self.f = (self.ssr / kx) / self.s2 if kx else np.nan
        self.f_p = st.f.sf(self.f, kx, self.df) if kx else np.nan
        self.X, self.y = X, y

    def ci(self, level=0.95):
        tcrit = st.t.ppf(0.5 + level / 2, self.df)
        return self.b - tcrit * self.se, self.b + tcrit * self.se

    def partial_eta2(self):
        """Per-coefficient partial eta squared, as SPSS GLM reports it."""
        return self.t ** 2 / (self.t ** 2 + self.df)

    def beta_std(self):
        """Standardized coefficients (slopes only make sense)."""
        sx = self.X.std(axis=0, ddof=1)
        sy = self.y.std(ddof=1)
        out = self.b * sx / sy
        out[0] = np.nan
        return out

    def leverage(self):
        return np.einsum("ij,jk,ik->i", self.X, self.XtX_inv, self.X)

    def cooks(self):
        h = self.leverage()
        return (self.resid ** 2 / (self.k * self.s2)) * h / (1 - h) ** 2


# ---------------------------------------------------------------------------
# single-predictor multivariate GLM (MANOVA-type)
# ---------------------------------------------------------------------------
def manova_single(Y, x):
    """Multivariate regression of Y (n x p) on one predictor x.

    Returns multivariate statistics for the predictor term and the two
    univariate OLS fits. With one hypothesis degree of freedom Pillai's
    Trace, Wilks' Lambda, Hotelling's trace and Roy's root all reduce to
    functions of the same eigenvalue, and the F transform is exact with
    (p, n - 1 - p) degrees of freedom.
    """
    Y = np.asarray(Y, float)
    x = np.asarray(x, float)
    n, p = Y.shape
    X = np.column_stack([np.ones(n), x])
    B = np.linalg.lstsq(X, Y, rcond=None)[0]
    E = (Y - X @ B).T @ (Y - X @ B)                 # residual SSCP
    # hypothesis SSCP for the slope term: difference against the
    # intercept-only model
    Y0 = Y - Y.mean(axis=0)
    T = Y0.T @ Y0
    H = T - E
    lam = np.linalg.eigvals(np.linalg.solve(E, H)).real
    lam = lam[np.argmax(np.abs(lam))]               # single non-zero root
    pillai = lam / (1.0 + lam)
    wilks = 1.0 / (1.0 + lam)
    df1, df2 = p, n - 1 - p
    F = (df2 / df1) * lam
    pval = st.f.sf(F, df1, df2)
    uni = [OLS(Y[:, j], X) for j in range(p)]
    return dict(pillai=pillai, wilks=wilks, F=F, df1=df1, df2=df2,
                p=pval, uni=uni)


# ---------------------------------------------------------------------------
# exploratory factor analysis: Principal Axis Factoring, one factor
# ---------------------------------------------------------------------------
def kmo(R):
    """Kaiser-Meyer-Olkin measure of sampling adequacy (overall)."""
    Rinv = np.linalg.inv(R)
    D = np.diag(1.0 / np.sqrt(np.diag(Rinv)))
    partial = -D @ Rinv @ D                          # partial correlations
    np.fill_diagonal(partial, 0.0)
    r2 = R.copy()
    np.fill_diagonal(r2, 0.0)
    return (r2 ** 2).sum() / ((r2 ** 2).sum() + (partial ** 2).sum())


def bartlett(R, n):
    p = R.shape[0]
    chi2 = -(n - 1 - (2 * p + 5) / 6.0) * np.log(np.linalg.det(R))
    df = p * (p - 1) // 2
    return chi2, df, st.chi2.sf(chi2, df)


def paf_one_factor(Z, tol=1e-6, itmax=500):
    """Principal Axis Factoring with a one-factor solution.

    Z is the n x p matrix of standardized observed variables. Initial
    communalities are squared multiple correlations; the reduced
    correlation matrix is re-eigendecomposed until the communalities
    converge. Factor scores use the regression (Thurstone) method.
    """
    n, p = Z.shape
    R = np.corrcoef(Z, rowvar=False)
    Rinv = np.linalg.inv(R)
    smc = 1.0 - 1.0 / np.diag(Rinv)                 # initial communalities
    h = smc.copy()
    for _ in range(itmax):
        Rr = R.copy()
        np.fill_diagonal(Rr, h)
        w, V = np.linalg.eigh(Rr)
        lam1, v1 = w[-1], V[:, -1]
        load = v1 * np.sqrt(max(lam1, 0.0))
        if load.sum() < 0:
            load = -load
        h_new = load ** 2
        if np.max(np.abs(h_new - h)) < tol:
            h = h_new
            break
        h = h_new
    eig_initial = np.linalg.eigvalsh(R)[::-1]
    ssl = float((load ** 2).sum())                  # extraction sum of squares
    scores_w = Rinv @ load                          # regression method
    scores = Z @ scores_w
    scores = scores / scores.std(ddof=1)            # unit-variance scores
    return dict(R=R, loadings=load, communalities=h, smc=smc,
                eig1=float(eig_initial[0]),
                var_initial=float(eig_initial[0] / p * 100),
                ssl=ssl, var_extracted=float(ssl / p * 100),
                scores=scores)


# ---------------------------------------------------------------------------
# hierarchical clustering (Pearson proximity, average linkage) + k-means
# ---------------------------------------------------------------------------
def pearson_distance(Z):
    """Condensed distance vector 1 - r between row profiles of Z."""
    R = np.corrcoef(Z)
    n = Z.shape[0]
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            out.append(1.0 - R[i, j])
    return np.array(out)


def average_linkage(d, n):
    """Plain average-linkage agglomeration on a condensed distance vector.

    Returns the scipy-style linkage matrix (n-1) x 4.
    """
    D = np.zeros((n, n))
    idx = 0
    for i in range(n):
        for j in range(i + 1, n):
            D[i, j] = D[j, i] = d[idx]
            idx += 1
    active = {i: [i] for i in range(n)}             # cluster id -> members
    ids = {i: i for i in range(n)}                  # cluster id -> linkage id
    Dc = {(min(a, b), max(a, b)): D[a, b]
          for a in range(n) for b in range(a + 1, n)}
    Z = []
    nxt = n
    keys = list(active)
    for step in range(n - 1):
        pair = min(((a, b) for a in keys for b in keys if a < b),
                   key=lambda ab: Dc[ab])
        a, b = pair
        dist = Dc[pair]
        na, nb = len(active[a]), len(active[b])
        Z.append([ids[a], ids[b], dist, na + nb])
        merged = active[a] + active[b]
        for c in keys:
            if c in (a, b):
                continue
            key_a = (min(a, c), max(a, c))
            key_b = (min(b, c), max(b, c))
            dnew = (na * Dc[key_a] + nb * Dc[key_b]) / (na + nb)
            Dc[(min(a, c), max(a, c))] = dnew
        active[a] = merged
        ids[a] = nxt
        nxt += 1
        del active[b]
        keys = list(active)
        Dc = {k: v for k, v in Dc.items() if b not in k}
    return np.array(Z)


def cut_two(Z, n):
    """Membership vector for the two-cluster cut of a linkage matrix."""
    children = {n + i: (int(Z[i, 0]), int(Z[i, 1])) for i in range(n - 1)}

    def leaves(node):
        if node < n:
            return [node]
        a, b = children[node]
        return leaves(a) + leaves(b)

    root_a, root_b = children[2 * n - 2]
    members = np.zeros(n, int)
    for leaf in leaves(root_b):
        members[leaf] = 1
    return members


def kmeans(Z, k, seed=20260817, iters=200, starts=50):
    rng = np.random.default_rng(seed)
    n = Z.shape[0]
    best = None
    for _ in range(starts):
        centers = Z[rng.choice(n, k, replace=False)].copy()
        for _ in range(iters):
            dist = ((Z[:, None, :] - centers[None]) ** 2).sum(-1)
            lab = dist.argmin(1)
            new = np.array([Z[lab == j].mean(0) if (lab == j).any()
                            else centers[j] for j in range(k)])
            if np.allclose(new, centers):
                break
            centers = new
        sse = float(((Z - centers[lab]) ** 2).sum())
        if best is None or sse < best[0]:
            best = (sse, lab.copy(), centers.copy())
    return best[1], best[2], best[0]


def silhouette(Z, labels):
    n = Z.shape[0]
    D = np.sqrt(((Z[:, None, :] - Z[None]) ** 2).sum(-1))
    s = np.zeros(n)
    for i in range(n):
        own = labels == labels[i]
        a = D[i, own & (np.arange(n) != i)].mean()
        b = min(D[i, labels == c].mean() for c in set(labels)
                if c != labels[i])
        s[i] = (b - a) / max(a, b)
    return s


def cluster_anova(v, labels):
    """One-way ANOVA of variable v across cluster labels, SPSS layout."""
    v = np.asarray(v, float)
    groups = [v[labels == c] for c in sorted(set(labels))]
    grand = v.mean()
    ss_b = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
    ss_w = sum(((g - g.mean()) ** 2).sum() for g in groups)
    df_b = len(groups) - 1
    df_w = len(v) - len(groups)
    ms_b, ms_w = ss_b / df_b, ss_w / df_w
    F = ms_b / ms_w
    return dict(ms_cluster=ms_b, df_cluster=df_b, ms_error=ms_w,
                df_error=df_w, F=F, p=st.f.sf(F, df_b, df_w))


def pearson_with_p(x, y):
    r, p = st.pearsonr(np.asarray(x, float), np.asarray(y, float))
    return float(r), float(p)
