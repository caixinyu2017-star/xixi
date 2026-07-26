"""Secretary Bird Optimization Algorithm (SBOA) and the proposed MSSBOA.

Base algorithm
--------------
SBOA: Fu, Y.; Liu, D.; Chen, J.; He, L. Secretary bird optimization algorithm:
a new metaheuristic for solving global optimization problems.
Artif. Intell. Rev. 2024, 57, 123.  doi:10.1007/s10462-024-10729-y

Per iteration each individual performs one hunting sub-update (three time-gated
stages, Eqs. 2-4) followed by one escape sub-update (Eqs. 6-7); both use greedy
acceptance (Eq. 5).

MSSBOA (this paper) adds three co-operating components:
  GPSI - good point set initialization                         (Eqs. 9-10)
  LOBL - lens opposition-based learning on the inferior subset (Eqs. 11-12)
  ACGM - adaptive Cauchy-Gaussian mutation on the elite        (Eqs. 13-14)

Everything is parameterized so that the revision's sensitivity analyses
(population size, LOBL subpopulation ratio, Levy beta, hunting-stage time
division, lens k-schedule) and the full-factorial ablation can reuse one
code path.
"""
import numpy as np

from framework import Recorder, init_pop, clipx, levy

# ----------------------------------------------------------------- defaults
DEFAULTS = dict(
    rho_lobl=0.2,      # fraction of the population refracted by LOBL (N_min = rho*N)
    p_m=0.5,           # probability of applying ACGM in an iteration
    beta=1.5,          # Levy-flight stability index
    stage=(1 / 3, 2 / 3),   # hunting-strategy time division
    k_root=0.5,        # exponent nu in k = (1 + (t/T)^nu)^mu
    k_pow=10.0,        # exponent mu
)


# ----------------------------------------------------------- GPSI (Eqs. 9-10)
def good_point_set(N, D, lb, ub):
    """Hua-Wang good point set.

    p is the smallest prime with (p - 3) / 2 >= D, i.e. p >= 2D + 3.
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
    pts = np.mod(r * i, 1.0)          # fractional part {i r_j}
    return lb + pts * (ub - lb)


# ----------------------------------------------------------- LOBL (Eqs. 11-12)
def lens_k(t, T, root=0.5, pow_=10.0):
    """Dynamic lens scaling factor  k(t) = (1 + (t/T)^nu)^mu.        (Eq. 12)"""
    return (1.0 + (t / T) ** root) ** pow_


def lens_refract(x, lb, ub, k):
    """Convex-lens refracted opposite solution.                       (Eq. 11)

    x* = (lb + ub) / 2 + (lb + ub) / (2k) - x / k
    k = h / h* is the ratio of object height to image height; k = 1 recovers
    classical opposition-based learning (x* = lb + ub - x).
    """
    mid = (lb + ub) / 2.0
    return mid + mid / k - x / k


# ----------------------------------------------------------- ACGM (Eqs. 13-14)
def acgm(xbest, t, T, rng):
    """Adaptive Cauchy-Gaussian mutation of the elite.             (Eqs. 13-14)

    x_best' = x_best * (1 + lambda1 * Cauchy(0,1) + lambda2 * Gauss(0,1))
    lambda1 = 1 - t^2 / T^2 ,  lambda2 = t^2 / T^2
    """
    lam2 = (t / T) ** 2
    lam1 = 1.0 - lam2
    D = xbest.size
    cauchy = rng.standard_cauchy(D)
    gauss = rng.standard_normal(D)
    return xbest * (1.0 + lam1 * cauchy + lam2 * gauss)


# ------------------------------------------------------------------ main loop
def _run(prob, max_fes, N, rng, use_gpsi=False, use_lobl=False, use_acgm=False,
         **kw):
    par = dict(DEFAULTS)
    par.update(kw)
    rho, p_m = par['rho_lobl'], par['p_m']
    beta = par['beta']
    s1, s2 = par['stage']
    k_root, k_pow = par['k_root'], par['k_pow']

    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub

    X = good_point_set(N, D, lb, ub) if use_gpsi else init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    gb = int(np.argmin(F))
    Xbest, fbest = X[gb].copy(), F[gb]

    n_lobl = int(np.ceil(rho * N)) if use_lobl else 0
    # FEs consumed per iteration: 2N (hunting + escape) + LOBL subset + ACGM
    per_iter = 2 * N + n_lobl + (p_m if use_acgm else 0)
    T = max(1, int(max_fes / per_iter))
    t = 0

    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)

        # ---------------- exploration: hunting strategy (Eqs. 2-4) ----------
        for i in range(N):
            if not rec.budget_left():
                break
            if tt < s1:                                    # searching for prey
                cand = [j for j in range(N) if j != i]
                a, b = rng.choice(cand, 2, replace=False)
                nx = X[i] + (X[a] - X[b]) * rng.random(D)
            elif tt < s2:                                  # consuming prey
                RB = rng.normal(0, 1, D)
                nx = Xbest + np.exp(tt ** 4) * (RB - 0.5) * (Xbest - X[i])
            else:                                          # attacking prey
                RL = 0.5 * levy(rng, D, beta)
                CF = (1 - tt) ** (2 * tt)
                nx = Xbest + CF * X[i] * RL
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            if f <= F[i]:                                              # Eq. 5
                X[i], F[i] = nx, f
                if f < fbest:
                    Xbest, fbest = nx.copy(), f

        # ---------------- exploitation: escape strategy (Eqs. 6-7) ----------
        for i in range(N):
            if not rec.budget_left():
                break
            if rng.random() < 0.5:
                RB = rng.normal(0, 1, D)
                nx = Xbest + (1 - tt) ** 2 * (2 * RB - 1) * X[i]
            else:
                R2 = rng.random(D)
                K = int(np.round(1 + rng.random()))
                nx = X[i] + R2 * (X[rng.integers(N)] - K * X[i])
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            if f <= F[i]:
                X[i], F[i] = nx, f
                if f < fbest:
                    Xbest, fbest = nx.copy(), f

        # ---------------- LOBL on the inferior subset (Eqs. 11-12) ----------
        if use_lobl and n_lobl:
            k = lens_k(t, T, k_root, k_pow)
            worst = np.argsort(F)[-n_lobl:]
            for i in worst:
                if not rec.budget_left():
                    break
                nx = clipx(lens_refract(X[i], lb, ub, k), prob)
                f = rec.eval(nx)
                if f <= F[i]:
                    X[i], F[i] = nx, f
                    if f < fbest:
                        Xbest, fbest = nx.copy(), f

        # ---------------- ACGM on the elite (Eqs. 13-14) --------------------
        if use_acgm and rec.budget_left() and rng.random() < p_m:
            nx = clipx(acgm(Xbest, t, T, rng), prob)
            f = rec.eval(nx)
            if f < fbest:
                Xbest, fbest = nx.copy(), f
                w = int(np.argmax(F))
                X[w], F[w] = nx.copy(), f

    return rec.finalize()


# --------------------------------------------------------------- public API
def sboa(prob, max_fes, N, rng, **kw):
    return _run(prob, max_fes, N, rng, **kw)


def mssboa(prob, max_fes, N, rng, **kw):
    return _run(prob, max_fes, N, rng, True, True, True, **kw)


def sboa_gpsi(prob, max_fes, N, rng, **kw):
    return _run(prob, max_fes, N, rng, True, False, False, **kw)


def sboa_lobl(prob, max_fes, N, rng, **kw):
    return _run(prob, max_fes, N, rng, False, True, False, **kw)


def sboa_acgm(prob, max_fes, N, rng, **kw):
    return _run(prob, max_fes, N, rng, False, False, True, **kw)


# pairwise combinations - needed for the 2^3 full-factorial ablation that
# quantifies the synergy between the three components (Reviewer 3, comment 2)
def sboa_gpsi_lobl(prob, max_fes, N, rng, **kw):
    return _run(prob, max_fes, N, rng, True, True, False, **kw)


def sboa_gpsi_acgm(prob, max_fes, N, rng, **kw):
    return _run(prob, max_fes, N, rng, True, False, True, **kw)


def sboa_lobl_acgm(prob, max_fes, N, rng, **kw):
    return _run(prob, max_fes, N, rng, False, True, True, **kw)


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
    return lambda prob, mf, N, rng, **kw: _run(prob, mf, N, rng, g, l, a, **kw)
