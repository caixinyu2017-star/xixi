# -*- coding: utf-8 -*-
"""Confirmatory factor analysis and measurement diagnostics, from first
principles.

Maximum-likelihood CFA on the item covariance matrix, with the latent
variances fixed at one so that loadings are identified, the latent correlation
matrix parametrized through a row-normalized Cholesky factor so that it stays
positive definite, and the unique variances parametrized in logs so that they
stay positive. Fit is the standard ML discrepancy

    F = log|Sigma(theta)| + tr(S Sigma^-1) - log|S| - p,

minimized by L-BFGS-B; chi-square, CFI, TLI, RMSEA and SRMR follow from F at
the minimum against the independence baseline. The module also provides
Cronbach's alpha, composite reliability, average variance extracted, the
Fornell-Larcker matrix, the heterotrait-monotrait ratio, Bartlett factor
scores, a two-group CFA for invariance testing, and the equal-loading
unmeasured-method-factor model used in the common-method-bias diagnostics.
"""
from __future__ import annotations

import numpy as np
from scipy import optimize, stats


# --------------------------------------------------------------------- model
class CFA:
    def __init__(self, X, spec):
        """X: (n, p) item matrix. spec: ordered dict name -> item columns."""
        self.spec = {k: list(v) for k, v in spec.items()}
        self.names = list(self.spec.keys())
        self.items = [c for v in self.spec.values() for c in v]
        self.k = len(self.names)
        self.p = len(self.items)
        self.X = np.asarray(X[self.items], dtype=float)
        self.n = self.X.shape[0]
        self.S = np.cov(self.X, rowvar=False, ddof=1)
        # membership matrix: item row -> construct column
        self.M = np.zeros((self.p, self.k))
        j = 0
        for c, (name, cols) in enumerate(self.spec.items()):
            for _ in cols:
                self.M[j, c] = 1.0
                j += 1

    # ------------------------------------------------------------ parameters
    def _unpack(self, th):
        lam = th[:self.p]
        psi = np.exp(th[self.p:2 * self.p])
        L = np.eye(self.k)
        idx = 2 * self.p
        for i in range(1, self.k):
            L[i, :i] = th[idx:idx + i]
            idx += i
        L = L / np.linalg.norm(L, axis=1, keepdims=True)
        Phi = L @ L.T
        return lam, psi, Phi

    def _sigma(self, th):
        lam, psi, Phi = self._unpack(th)
        Lam = self.M * lam[:, None]
        return Lam @ Phi @ Lam.T + np.diag(psi), lam, psi, Phi

    def _F(self, th):
        Sig, *_ = self._sigma(th)
        sign, ld = np.linalg.slogdet(Sig)
        if sign <= 0:
            return 1e6
        try:
            SinvS = np.linalg.solve(Sig, self.S)
        except np.linalg.LinAlgError:
            return 1e6
        _, ldS = np.linalg.slogdet(self.S)
        return ld + np.trace(SinvS) - ldS - self.p

    def nparams(self):
        return 2 * self.p + self.k * (self.k - 1) // 2

    # -------------------------------------------------------------------- fit
    def fit(self):
        sd = np.sqrt(np.diag(self.S))
        th0 = np.concatenate([0.7 * sd, np.log(0.5 * np.diag(self.S)),
                              np.zeros(self.k * (self.k - 1) // 2)])
        res = optimize.minimize(self._F, th0, method="L-BFGS-B",
                                options=dict(maxiter=4000, maxfun=200000))
        self.theta = res.x
        self.Fmin = res.fun
        Sig, lam, psi, Phi = self._sigma(res.x)
        self.Sigma, self.lam, self.psi, self.Phi = Sig, lam, psi, Phi
        self.chi2 = (self.n - 1) * self.Fmin
        self.df = self.p * (self.p + 1) // 2 - self.nparams()
        self.pval = 1 - stats.chi2.cdf(self.chi2, self.df)
        # independence baseline
        Fb = float(np.log(np.diag(self.S)).sum()
                   - np.linalg.slogdet(self.S)[1])
        chib = (self.n - 1) * Fb
        dfb = self.p * (self.p - 1) // 2
        self.cfi = 1 - max(self.chi2 - self.df, 0) / max(chib - dfb, 1e-9)
        self.tli = ((chib / dfb - self.chi2 / self.df)
                    / max(chib / dfb - 1, 1e-9))
        self.rmsea = np.sqrt(max(self.chi2 - self.df, 0)
                             / (self.df * (self.n - 1)))
        # SRMR over the standardized residual correlations
        d = np.sqrt(np.diag(self.S))
        R = self.S / np.outer(d, d)
        Rh = self.Sigma / np.outer(np.sqrt(np.diag(self.Sigma)),
                                   np.sqrt(np.diag(self.Sigma)))
        tri = np.tril_indices(self.p, 0)
        self.srmr = float(np.sqrt(np.mean((R - Rh)[tri] ** 2)))
        return self

    # ------------------------------------------------------------ assessment
    def std_loadings(self):
        return self.lam / np.sqrt(np.diag(self.Sigma))

    def table(self):
        """Per-construct alpha, CR, AVE and the item loadings."""
        ls = self.std_loadings()
        out = {}
        j = 0
        for name, cols in self.spec.items():
            m = len(cols)
            lset = ls[j:j + m]
            j += m
            sub = self.X[:, [self.items.index(c) for c in cols]]
            C = np.cov(sub, rowvar=False, ddof=1)
            alpha = (m / (m - 1)) * (1 - np.trace(C) / C.sum())
            cr = lset.sum() ** 2 / (lset.sum() ** 2 + (1 - lset ** 2).sum())
            ave = float(np.mean(lset ** 2))
            out[name] = dict(items=cols, load=lset.tolist(),
                             alpha=float(alpha), cr=float(cr), ave=ave)
        return out

    def fornell_larcker(self):
        tab = self.table()
        rt = np.sqrt([tab[n]["ave"] for n in self.names])
        F = self.Phi.copy()
        np.fill_diagonal(F, rt)
        return F

    def htmt(self):
        """Heterotrait-monotrait ratio from the item correlation matrix."""
        R = np.corrcoef(self.X, rowvar=False)
        pos = {}
        j = 0
        for name, cols in self.spec.items():
            pos[name] = list(range(j, j + len(cols)))
            j += len(cols)
        H = np.zeros((self.k, self.k))
        for a in range(self.k):
            for b in range(a + 1, self.k):
                ia, ib = pos[self.names[a]], pos[self.names[b]]
                het = np.mean([R[i, j2] for i in ia for j2 in ib])
                mono_a = np.mean([R[i, j2] for x, i in enumerate(ia)
                                  for j2 in ia[x + 1:]])
                mono_b = np.mean([R[i, j2] for x, i in enumerate(ib)
                                  for j2 in ib[x + 1:]])
                H[a, b] = H[b, a] = abs(het) / np.sqrt(mono_a * mono_b)
        return H

    def scores(self, X=None):
        """Bartlett factor scores, standardized column-wise."""
        Xm = self.X if X is None else np.asarray(X[self.items], dtype=float)
        Lam = self.M * self.lam[:, None]
        W = np.linalg.solve(Lam.T @ np.diag(1 / self.psi) @ Lam,
                            Lam.T @ np.diag(1 / self.psi))
        sc = (Xm - self.X.mean(0)) @ W.T
        return (sc - sc.mean(0)) / sc.std(0, ddof=1)


# ------------------------------------------------------- method-factor model
class CFAMethod(CFA):
    """The equal-loading unmeasured-method-factor model: one orthogonal
    factor with a common loading on every item, one extra parameter."""

    def _sigma(self, th):
        lam, psi, Phi = self._unpack(th[:-1])
        m = th[-1]
        Lam = self.M * lam[:, None]
        Sig = Lam @ Phi @ Lam.T + m ** 2 * np.ones((self.p, self.p)) \
            + np.diag(psi)
        return Sig, lam, psi, Phi

    def nparams(self):
        return super().nparams() + 1

    def fit(self):
        sd = np.sqrt(np.diag(self.S))
        th0 = np.concatenate([0.7 * sd, np.log(0.5 * np.diag(self.S)),
                              np.zeros(self.k * (self.k - 1) // 2), [0.1]])
        res = optimize.minimize(self._F, th0, method="L-BFGS-B",
                                options=dict(maxiter=4000, maxfun=200000))
        self.theta = res.x
        self.Fmin = res.fun
        Sig, lam, psi, Phi = self._sigma(res.x)
        self.Sigma, self.lam, self.psi, self.Phi = Sig, lam, psi, Phi
        self.method_load = res.x[-1]
        self.chi2 = (self.n - 1) * self.Fmin
        self.df = self.p * (self.p + 1) // 2 - self.nparams()
        self.method_share = float(np.mean(res.x[-1] ** 2
                                          / np.diag(self.Sigma)))
        return self


# ------------------------------------------------------------ invariance
def two_group(X, groups, spec, share_loadings=False):
    """Two-group ML CFA. Returns the summed chi-square and the total df.

    With ``share_loadings`` the loading vector is common to both groups
    (metric invariance); otherwise every parameter is group-specific
    (configural). Latent correlations and unique variances are free in both.
    """
    gs = sorted(set(groups))
    assert len(gs) == 2
    subs = [CFA(X[groups == g], spec) for g in gs]

    if not share_loadings:
        chi2 = df = 0.0
        for c in subs:
            c.fit()
            chi2 += c.chi2
            df += c.df
        return chi2, int(df), subs

    p, k = subs[0].p, subs[0].k
    ntri = k * (k - 1) // 2

    def unpack(th):
        lam = th[:p]
        parts = []
        idx = p
        for _ in range(2):
            psi = np.exp(th[idx:idx + p]); idx += p
            tri = th[idx:idx + ntri]; idx += ntri
            parts.append((psi, tri))
        return lam, parts

    def F(th):
        lam, parts = unpack(th)
        tot = 0.0
        for c, (psi, tri) in zip(subs, parts):
            L = np.eye(k)
            j = 0
            for i in range(1, k):
                L[i, :i] = tri[j:j + i]
                j += i
            L = L / np.linalg.norm(L, axis=1, keepdims=True)
            Phi = L @ L.T
            Lam = c.M * lam[:, None]
            Sig = Lam @ Phi @ Lam.T + np.diag(psi)
            sign, ld = np.linalg.slogdet(Sig)
            if sign <= 0:
                return 1e6
            _, ldS = np.linalg.slogdet(c.S)
            f = ld + np.trace(np.linalg.solve(Sig, c.S)) - ldS - p
            tot += (c.n - 1) * f
        return tot

    sd = np.sqrt(np.diag(subs[0].S))
    th0 = np.concatenate(
        [0.7 * sd] + [np.concatenate([np.log(0.5 * np.diag(c.S)),
                                      np.zeros(ntri)]) for c in subs])
    res = optimize.minimize(F, th0, method="L-BFGS-B",
                            options=dict(maxiter=6000, maxfun=400000))
    chi2 = res.fun
    npar = p + 2 * (p + ntri)
    df = 2 * (p * (p + 1) // 2) - npar
    return float(chi2), int(df), subs


def cfi_pair(chi2, df, X, spec, groups):
    """CFI for a two-group statistic against the pooled baseline."""
    gs = sorted(set(groups))
    chib = dfb = 0.0
    for g in gs:
        sub = CFA(X[groups == g], spec)
        Fb = float(np.log(np.diag(sub.S)).sum()
                   - np.linalg.slogdet(sub.S)[1])
        chib += (sub.n - 1) * Fb
        dfb += sub.p * (sub.p - 1) // 2
    return 1 - max(chi2 - df, 0) / max(chib - dfb, 1e-9)
