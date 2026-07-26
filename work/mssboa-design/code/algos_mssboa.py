"""Secretary Bird Optimization Algorithm (SBOA) and the proposed MSSBOA.

Base algorithm
--------------
Fu, Y.; Liu, D.; Chen, J.; He, L. Secretary bird optimization algorithm: a new
metaheuristic for solving global optimization problems.
Artif. Intell. Rev. 2024, 57, 123.  doi:10.1007/s10462-024-10729-y

Per iteration each individual performs one hunting sub-update (three time-gated
stages, Eqs. 2-4) followed by one escape sub-update (Eqs. 6-7); both use greedy
acceptance (Eq. 5).

MSSBOA adds three co-operating components:
  GPSI - good point set initialization                         (Eqs. 9-10)
  LOBL - lens opposition-based learning on the inferior subset (Eqs. 11-12)
  ACGM - adaptive Cauchy-Gaussian mutation on the elite        (Eqs. 13-14)

Everything is parameterized so that the sensitivity grids and the full
factorial ablation reuse a single code path, and the whole population is
evaluated in one batched call per sub-update.
"""
import numpy as np

from framework import Recorder, init_pop, greedy, levy

DEFAULTS = dict(
    rho_lobl=0.2,           # fraction of the population refracted by LOBL
    p_m=0.5,                # probability of applying ACGM in an iteration
    beta=1.5,               # Levy-flight stability index
    stage=(1 / 3, 2 / 3),   # hunting-strategy time division
    k_root=0.5,             # exponent nu in k = (1 + (t/T)^nu)^mu
    k_pow=10.0,             # exponent mu
)


# ----------------------------------------------------------- GPSI (Eqs. 9-10)
def good_point_set(N, D, lb, ub):
    """Hua-Wang good point set.

    p is the smallest prime with p >= 2D + 3;
    r_j = 2 cos(2 pi j / p),  j = 1..D                                  (Eq. 9)
    x_ij = lb_j + {i r_j} (ub_j - lb_j),  i = 1..N                      (Eq. 10)
    """
    def is_prime(n):
        if n < 2:
            return False
        for q in range(2, int(n ** 0.5) + 1):
            if n % q == 0:
                return False
        return True

    p = 2 * D + 3
    while not is_prime(p):
        p += 1
    j = np.arange(1, D + 1)
    r = 2 * np.cos(2 * np.pi * j / p)
    i = np.arange(1, N + 1).reshape(-1, 1)
    return lb + np.mod(r * i, 1.0) * (ub - lb)


# ----------------------------------------------------------- LOBL (Eqs. 11-12)
def lens_k(t, T, root=0.5, pow_=10.0):
    """Dynamic lens scaling factor  k(t) = (1 + (t/T)^nu)^mu.        (Eq. 12)"""
    return (1.0 + (t / T) ** root) ** pow_


def lens_refract(X, lb, ub, k):
    """Convex-lens refracted opposite solution.                       (Eq. 11)

    x* = (lb + ub)/2 + (lb + ub)/(2k) - x/k, where k = h/h* is the ratio of
    object height to image height.  k = 1 recovers classical opposition-based
    learning, x* = lb + ub - x.
    """
    mid = (lb + ub) / 2.0
    return mid + mid / k - X / k


# ----------------------------------------------------------- ACGM (Eqs. 13-14)
def acgm(xbest, t, T, rng):
    """Adaptive Cauchy-Gaussian mutation of the elite.             (Eqs. 13-14)

    x' = x_best (1 + lambda1 Cauchy(0,1) + lambda2 Gauss(0,1)),
    lambda1 = 1 - t^2/T^2,  lambda2 = t^2/T^2.
    """
    lam2 = (t / T) ** 2
    lam1 = 1.0 - lam2
    D = xbest.size
    return xbest * (1.0 + lam1 * rng.standard_cauchy(D)
                    + lam2 * rng.standard_normal(D))


# -------------------------------------------------------------------- driver
def _run(prob, max_fes, N, rng, use_gpsi=False, use_lobl=False, use_acgm=False,
         **kw):
    par = dict(DEFAULTS)
    par.update(kw)
    rho, p_m, beta = par['rho_lobl'], par['p_m'], par['beta']
    s1, s2 = par['stage']
    k_root, k_pow = par['k_root'], par['k_pow']

    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub

    X = good_point_set(N, D, lb, ub) if use_gpsi else init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    gb = int(np.argmin(F))
    Xbest, fbest = X[gb].copy(), float(F[gb])

    n_lobl = int(np.ceil(rho * N)) if use_lobl else 0
    per_iter = 2 * N + n_lobl + (p_m if use_acgm else 0.0)
    T = max(1, int(max_fes / per_iter))
    t = 0
    idx = np.arange(N)

    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)

        # ------------- exploration: hunting strategy (Eqs. 2-4) -------------
        if tt < s1:                                          # searching
            a = rng.integers(0, N, N)
            b = rng.integers(0, N, N)
            a = np.where(a == idx, (a + 1) % N, a)
            b = np.where(b == a, (b + 1) % N, b)
            Xn = X + (X[a] - X[b]) * rng.random((N, D))
        elif tt < s2:                                        # consuming
            RB = rng.normal(0, 1, (N, D))
            Xn = Xbest + np.exp(tt ** 4) * (RB - 0.5) * (Xbest - X)
        else:                                                # attacking
            RL = 0.5 * levy(rng, (N, D), beta)
            Xn = Xbest + ((1 - tt) ** (2 * tt)) * X * RL
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)

        # ------------- exploitation: escape strategy (Eqs. 6-7) -------------
        use_c1 = rng.random(N) < 0.5
        RB = rng.normal(0, 1, (N, D))
        C1 = Xbest + (1 - tt) ** 2 * (2 * RB - 1) * X
        K = np.round(1 + rng.random((N, 1)))
        C2 = X + rng.random((N, D)) * (X[rng.integers(0, N, N)] - K * X)
        Xn = np.where(use_c1[:, None], C1, C2)
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)

        j = int(np.argmin(F))
        if F[j] < fbest:
            Xbest, fbest = X[j].copy(), float(F[j])

        # ------------- LOBL on the inferior subset (Eqs. 11-12) -------------
        if n_lobl and rec.budget_left():
            worst = np.argsort(F)[-n_lobl:]
            Xr = lens_refract(X[worst], lb, ub, lens_k(t, T, k_root, k_pow))
            Fr = rec.evaluate(Xr)
            m = len(Fr)
            if m:
                sel = worst[:m]
                better = Fr <= F[sel]
                X[sel[better]] = np.clip(Xr[:m][better], lb, ub)
                F[sel[better]] = Fr[better]

        # ------------- ACGM on the elite (Eqs. 13-14) -----------------------
        if use_acgm and rec.budget_left() and rng.random() < p_m:
            xm = acgm(Xbest, t, T, rng)
            fm = rec.evaluate(xm)
            if len(fm) and fm[0] < fbest:
                Xbest, fbest = np.clip(xm, lb, ub), float(fm[0])
                w = int(np.argmax(F))
                X[w], F[w] = Xbest.copy(), fbest

        j = int(np.argmin(F))
        if F[j] < fbest:
            Xbest, fbest = X[j].copy(), float(F[j])

    return rec.finalize()


# ------------------------------------------------------------------- exports
def sboa(prob, max_fes, N, rng, **kw):
    return _run(prob, max_fes, N, rng, **kw)


def mssboa(prob, max_fes, N, rng, **kw):
    return _run(prob, max_fes, N, rng, True, True, True, **kw)


FACTORIAL = {
    'SBOA':            (False, False, False),
    'SBOA-GPSI':       (True, False, False),
    'SBOA-LOBL':       (False, True, False),
    'SBOA-ACGM':       (False, False, True),
    'SBOA-GPSI-LOBL':  (True, True, False),
    'SBOA-GPSI-ACGM':  (True, False, True),
    'SBOA-LOBL-ACGM':  (False, True, True),
    'MSSBOA':          (True, True, True),
}


def factorial_algo(name):
    g, l, a = FACTORIAL[name]

    def run(prob, mf, N, rng, **kw):
        return _run(prob, mf, N, rng, g, l, a, **kw)
    return run


sboa_gpsi = factorial_algo('SBOA-GPSI')
sboa_lobl = factorial_algo('SBOA-LOBL')
sboa_acgm = factorial_algo('SBOA-ACGM')
