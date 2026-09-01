# -*- coding: utf-8 -*-
"""A first-principles two-step System GMM estimator (Blundell-Bond) for
the balanced dynamic panel used in the paper.

Model:  y_it = alpha * y_i,t-1 + x_it' beta + mu_i + eps_it

Moment conditions, deliberately parsimonious (collapsed a la Roodman):

*   difference equation (t = 3..T): collapsed lagged levels of y
    (y_{i,t-2}, y_{i,t-3}) as instruments for Delta y_{i,t-1}; the
    exogenous regressors instrument themselves in differences;
*   levels equation (t = 3..T): the collapsed lagged difference
    Delta y_{i,t-1} as instrument for y_{i,t-1}, plus the constant
    (or the period dummies). The substantive regressors do NOT serve
    as level-equation instruments, because they may be correlated
    with the country effects.

Inference: two-step GMM with the Windmeijer (2005) finite-sample
correction; Arellano-Bond tests for first- and second-order serial
correlation in the differenced residuals; Hansen J test of the
overidentifying restrictions. The module also provides an IPS-type
panel unit-root statistic and the Pesaran CD test, and a Monte Carlo
self-test that recovers known parameters (run this file directly).
"""
from __future__ import annotations

import numpy as np
from scipy import stats as st


# ---------------------------------------------------------------------------
def _blocks(Y, X, dummies):
    """Per-country data blocks for the system estimator.

    Y: (N, T) levels of the dependent variable.
    X: (N, T, K) levels of the exogenous regressors.
    Rows of each country block: first the difference equation for
    t = 3..T (0-indexed 2..T-1), then the levels equation for the same
    periods.

    Parameters: [alpha, beta_1..K, const] without period dummies, or
    [alpha, beta_1..K, lambda_2..lambda_{T-1}] with them (the dummies
    span the constant). Period dummies are treated as exogenous and
    instrument themselves in the levels equation only, keeping the
    instrument count parsimonious.
    """
    N, T = Y.shape
    K = X.shape[2]
    n_d = T - 2
    nd_dum = n_d if dummies else 0
    P = K + 1 + (nd_dum if dummies else 1)
    nz = (2 + K) + 1 + (nd_dum if dummies else 1)
    dumidx = {t: K + 1 + (t - 2) for t in range(2, T)}
    blocks = []
    for i in range(N):
        y, x = Y[i], X[i]
        rows_W, rows_y, rows_Z = [], [], []
        # difference equation
        for t in range(2, T):
            w = np.zeros(P)
            w[0] = y[t - 1] - y[t - 2]
            w[1:K + 1] = x[t] - x[t - 1]
            if dummies:
                w[dumidx[t]] += 1.0
                if t - 1 >= 2:
                    w[dumidx[t - 1]] -= 1.0
            rows_W.append(w)
            rows_y.append(y[t] - y[t - 1])
            z = np.zeros(nz)
            z[0] = y[t - 2]                      # collapsed lag-2 level
            z[1] = y[t - 3] if t >= 3 else 0.0   # collapsed lag-3 level
            z[2:2 + K] = x[t] - x[t - 1]         # exogenous in diffs
            rows_Z.append(z)
        # levels equation; the substantive regressors may be correlated
        # with the country effects, so only the lagged difference of y
        # and the deterministic terms enter as level-equation instruments
        for t in range(2, T):
            w = np.zeros(P)
            w[0] = y[t - 1]
            w[1:K + 1] = x[t]
            if dummies:
                w[dumidx[t]] = 1.0
            else:
                w[K + 1] = 1.0
            rows_W.append(w)
            rows_y.append(y[t])
            z = np.zeros(nz)
            z[2 + K] = y[t - 1] - y[t - 2]       # collapsed lagged diff
            if dummies:
                z[3 + K + (t - 2)] = 1.0         # period dummy
            else:
                z[3 + K] = 1.0                   # constant
            rows_Z.append(z)
        blocks.append((np.array(rows_W), np.array(rows_y),
                       np.array(rows_Z), n_d))
    return blocks, P


def _H_matrix(n_d):
    """One-step weighting block: tridiagonal for the difference part,
    identity for the levels part (the usual xtabond2 H)."""
    H = np.zeros((2 * n_d, 2 * n_d))
    for a in range(n_d):
        H[a, a] = 2.0
        if a + 1 < n_d:
            H[a, a + 1] = H[a + 1, a] = -1.0
    for a in range(n_d, 2 * n_d):
        H[a, a] = 1.0
    return H


class SystemGMM:
    def __init__(self, Y, X, dummies=True):
        self.blocks, self.P = _blocks(Y, X, dummies)
        self.dummies = dummies
        self.N = len(self.blocks)
        self.nz = self.blocks[0][2].shape[1]
        self._estimate()

    # -- helpers ----------------------------------------------------------
    def _moments(self, theta):
        return [Z.T @ (y - W @ theta) for W, y, Z, _ in self.blocks]

    def _G(self):
        return sum(Z.T @ W for W, y, Z, _ in self.blocks) / self.N

    def _omega(self, theta):
        g = self._moments(theta)
        return sum(np.outer(a, a) for a in g) / self.N

    def _estimate(self):
        # one step
        H = _H_matrix(self.blocks[0][3])
        A1 = sum(Z.T @ H @ Z for W, y, Z, _ in self.blocks) / self.N
        W1 = np.linalg.pinv(A1)
        G = self._G()
        gy = sum(Z.T @ y for W, y, Z, _ in self.blocks) / self.N
        M1 = np.linalg.pinv(G.T @ W1 @ G)
        self.theta1 = M1 @ G.T @ W1 @ gy
        # two step
        Om1 = self._omega(self.theta1)
        W2 = np.linalg.pinv(Om1)
        M2 = np.linalg.pinv(G.T @ W2 @ G)
        self.theta = M2 @ G.T @ W2 @ gy
        # naive two-step variance and robust one-step variance
        V2 = M2 / self.N
        Om2 = self._omega(self.theta)
        B = G.T @ W1 @ Om1 @ W1 @ G
        V1r = (M1 @ B @ M1) / self.N
        # Windmeijer (2005) correction: the derivative of the two-step
        # estimator with respect to the first-step estimate, with the
        # weighting-matrix derivative evaluated at the one-step
        # residuals and the moment vector at the two-step estimate
        gbar2 = sum(self._moments(self.theta)) / self.N
        D = np.zeros((self.P, self.P))
        for j in range(self.P):
            dOm = np.zeros_like(Om1)
            for W_, y_, Z_, _ in self.blocks:
                gi = Z_.T @ (y_ - W_ @ self.theta1)
                dgi = -(Z_.T @ W_[:, j])
                dOm += np.outer(dgi, gi) + np.outer(gi, dgi)
            dOm /= self.N
            D[:, j] = -(M2 @ G.T @ W2 @ dOm @ W2 @ gbar2)
        Vw = V2 + D @ V2 + V2 @ D.T + D @ V1r @ D.T
        dg = np.diag(Vw).copy()
        # numerical safeguard: fall back to the naive two-step variance
        # on any (non-occurring in practice) negative diagonal element
        bad = dg <= 0
        if bad.any():
            dg[bad] = np.diag(V2)[bad]
        self.se = np.sqrt(dg)
        self.vcov = Vw
        self._A_influence = M2 @ G.T @ W2 / self.N
        self._V1r = V1r
        self.z = self.theta / self.se
        self.p = 2 * st.norm.sf(np.abs(self.z))
        # Hansen J at the two-step estimate
        gbar2 = sum(self._moments(self.theta)) / self.N
        W2b = np.linalg.pinv(Om2)
        self.hansen_j = float(self.N * gbar2 @ W2b @ gbar2)
        self.hansen_df = self.nz - self.P
        self.hansen_p = float(st.chi2.sf(self.hansen_j, self.hansen_df))
        self.n_instruments = self.nz
        self._ar_tests()

    def _ar_tests(self):
        """Arellano-Bond (1991) m-statistics on the differenced
        residuals, with the full three-term variance: the outer-product
        leading term, the cross term with the estimated coefficients,
        and the quadratic term in the estimator's variance."""
        n_d = self.blocks[0][3]
        out = {}
        for k in (1, 2):
            d0 = 0.0
            lead = 0.0
            b = np.zeros(self.P)                 # sum_i W_i' e_{i,-k}
            c = np.zeros(self.nz)                # sum_i (Z_i' u_i) s_i
            for W, y, Z, _ in self.blocks:
                u = y - W @ self.theta
                e = u[:n_d]                      # difference-equation part
                elag = np.zeros(n_d)
                elag[k:] = e[:-k]
                s = float(elag @ e)
                d0 += s
                lead += s * s
                b += W[:n_d].T @ elag
                c += (Z.T @ u) * s
            A = self._A_influence                # theta = A (sum Z_i'y_i)
            v = lead - 2.0 * float(b @ (A @ c)) + float(b @ self.vcov @ b)
            zstat = d0 / np.sqrt(v) if v > 0 else np.nan
            out[k] = (float(zstat), float(2 * st.norm.sf(abs(zstat))))
        self.ar1_z, self.ar1_p = out[1]
        self.ar2_z, self.ar2_p = out[2]


# ---------------------------------------------------------------------------
def ips_test(Y):
    """IPS-type panel unit-root statistic: the standardized average of
    country-level Dickey-Fuller t-statistics (intercept, lag 0),
    using large-T moment approximations E(t) = -1.52, V(t) = 0.80."""
    N, T = Y.shape
    ts = []
    for i in range(N):
        y = Y[i]
        dy = np.diff(y)
        ylag = y[:-1]
        Xr = np.column_stack([np.ones(T - 1), ylag])
        b, res, *_ = np.linalg.lstsq(Xr, dy, rcond=None)
        e = dy - Xr @ b
        s2 = e @ e / (T - 1 - 2)
        se = np.sqrt(s2 * np.linalg.inv(Xr.T @ Xr)[1, 1])
        ts.append(b[1] / se)
    tbar = float(np.mean(ts))
    zstat = np.sqrt(N) * (tbar - (-1.52)) / np.sqrt(0.80)
    return tbar, float(zstat), float(st.norm.sf(-zstat) if zstat < 0
                                     else st.norm.sf(zstat))


def pesaran_cd(E):
    """Pesaran CD statistic on a (N, T) residual or variable panel."""
    N, T = E.shape
    En = E - E.mean(axis=1, keepdims=True)
    total = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            num = float(En[i] @ En[j])
            den = np.sqrt(float(En[i] @ En[i]) * float(En[j] @ En[j]))
            total += num / den if den > 0 else 0.0
    cd = np.sqrt(2.0 * T / (N * (N - 1))) * total
    return float(cd), float(2 * st.norm.sf(abs(cd)))


# ---------------------------------------------------------------------------
def _monte_carlo(reps=200, N=27, T=15, seed=7):
    """Self-test: recover known parameters from a simulated panel."""
    rng = np.random.default_rng(seed)
    alpha0, beta0 = 0.70, np.array([0.50, -0.15])
    est, ses = [], []
    for _ in range(reps):
        mu = rng.normal(0, 2.0, N)
        X = rng.normal(0, 1.0, (N, T + 10, 2)) + 0.3 * mu[:, None, None]
        Y = np.zeros((N, T + 10))
        Y[:, 0] = mu / (1 - alpha0)
        for t in range(1, T + 10):
            Y[:, t] = (alpha0 * Y[:, t - 1] + X[:, t] @ beta0 + mu
                       + rng.normal(0, 1.0, N))
        Y, X = Y[:, 10:], X[:, 10:, :]
        m = SystemGMM(Y, X)
        est.append(m.theta[:3])
        ses.append(m.se[:3])
    est, ses = np.array(est), np.array(ses)
    print("Monte Carlo (%d reps): true alpha %.2f betas %s" %
          (reps, alpha0, beta0))
    for j, name in enumerate(["alpha", "beta1", "beta2"]):
        print("  %-6s mean est %7.3f  empirical SD %6.3f  "
              "mean Windmeijer SE %6.3f" %
              (name, est[:, j].mean(), est[:, j].std(ddof=1),
               ses[:, j].mean()))


if __name__ == "__main__":
    _monte_carlo()
