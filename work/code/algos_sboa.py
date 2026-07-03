"""Secretary Bird Optimization Algorithm (Fu et al., 2024, Artif. Intell. Rev.,
doi:10.1007/s10462-024-10729-y) and the proposed multi-strategy variant MSSBOA.

Faithful to the authors' MATLAB reference implementation (File Exchange #164456):
per iteration each individual performs one hunting sub-update (three time-gated
stages) followed by one escape sub-update, each with greedy acceptance.

MSSBOA adds three strategies:
  GPS - good point set initialization
  EDS - elite-guided differential search: in hunting stage 1 the differential
        move is guided by an elite pool (three best individuals + centroid of
        the top 10%) and combined with the parent through dimension-wise
        binomial crossover (CR = 0.5)
  ERM - elite refinement mechanism: the global best is refined once per
        iteration, alternating an adaptive t-distribution perturbation (odd
        iterations) with a three-point quadratic interpolation (even
        iterations); the refined solution replaces the worst individual when
        it improves upon it
"""
import numpy as np
from framework import Recorder, init_pop, clipx, levy

TAU = (np.sqrt(5) - 1) / 2  # golden ratio coefficient


def _good_point_set(N, D, lb, ub):
    """Hua-Wang good point set: p = smallest prime >= 2D+3, r_j = 2cos(2*pi*j/p)."""
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
    pts = np.mod(r * i, 1.0)
    return lb + pts * (ub - lb)


def _qi_point(xa, xb, xc, fa, fb, fc):
    """Dimension-wise three-point quadratic interpolation minimum."""
    num = (xb ** 2 - xc ** 2) * fa + (xc ** 2 - xa ** 2) * fb + (xa ** 2 - xb ** 2) * fc
    den = (xb - xc) * fa + (xc - xa) * fb + (xa - xb) * fc
    den = np.where(np.abs(den) < 1e-50, 1e-50, den)
    return 0.5 * num / den


def _hunt_escape_loop(prob, max_fes, N, rng, use_gps=False, use_eds=False, use_erm=False):
    rec = Recorder(prob, max_fes)
    D = prob.dim
    # ---------------- initialization ----------------
    if use_gps:
        X = _good_point_set(N, D, prob.lb, prob.ub)
    else:
        X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    gb = np.argmin(F)
    Xbest, fbest = X[gb].copy(), F[gb]
    # 2 evals per individual per iteration (+1 for ERM)
    T = max(1, max_fes // (2 * N + (1 if use_erm else 0)))
    t = 0
    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)
        if use_eds:
            order = np.argsort(F)
            elites = [X[order[0]], X[order[1]], X[order[2]],
                      X[order[:max(3, N // 10)]].mean(axis=0)]
        # ---------------- hunting strategy (exploration) ----------------
        for i in range(N):
            if not rec.budget_left():
                break
            if t < T / 3:
                if use_eds:
                    # elite-guided differential move + binomial crossover
                    Xe = elites[rng.integers(len(elites))]
                    cand = [j for j in range(N) if j != i]
                    a, b = rng.choice(cand, 2, replace=False)
                    v = X[i] + rng.random(D) * (Xe - X[i]) + rng.random(D) * (X[a] - X[b])
                    mask = rng.random(D) < 0.5
                    mask[rng.integers(D)] = True
                    nx = np.where(mask, v, X[i])
                else:
                    cand = [j for j in range(N) if j != i]
                    a, b = rng.choice(cand, 2, replace=False)
                    R1 = rng.random(D)
                    nx = X[i] + (X[a] - X[b]) * R1
            elif t < 2 * T / 3:
                RB = rng.normal(0, 1, D)
                nx = Xbest + np.exp(tt ** 4) * (RB - 0.5) * (Xbest - X[i])
            else:
                RL = 0.5 * levy(rng, D)
                CF = (1 - tt) ** (2 * tt)
                nx = Xbest + CF * X[i] * RL
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            if f <= F[i]:
                X[i], F[i] = nx, f
                if f < fbest:
                    Xbest, fbest = nx.copy(), f
        # ---------------- escape strategy (exploitation) ----------------
        for i in range(N):
            if not rec.budget_left():
                break
            if rng.random() < 0.5:
                RB = rng.normal(0, 1, D)
                nx = Xbest + (1 - tt) ** 2 * (2 * RB - 1) * X[i]
            else:
                R2 = rng.random(D)
                K = int(np.round(1 + rng.random()))
                Xr = X[rng.integers(N)]
                nx = X[i] + R2 * (Xr - K * X[i])
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            if f <= F[i]:
                X[i], F[i] = nx, f
                if f < fbest:
                    Xbest, fbest = nx.copy(), f
        # ---------------- elite refinement mechanism ----------------
        if use_erm and rec.budget_left():
            if t % 2 == 1:
                # adaptive t-distribution perturbation
                df = max(1, t)
                step = rng.standard_t(df, D)
                nx = Xbest * (1 + 0.5 * (1 - tt) * step)
            else:
                # three-point quadratic interpolation
                a, b = rng.choice(N, 2, replace=False)
                nx = _qi_point(Xbest, X[a], X[b], fbest, F[a], F[b])
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            w = np.argmax(F)
            if f < F[w]:
                X[w], F[w] = nx.copy(), f
                if f < fbest:
                    Xbest, fbest = nx.copy(), f
    return rec.finalize()


def sboa(prob, max_fes, N, rng):
    return _hunt_escape_loop(prob, max_fes, N, rng)


def mssboa(prob, max_fes, N, rng):
    return _hunt_escape_loop(prob, max_fes, N, rng, use_gps=True, use_eds=True, use_erm=True)


def sboa_gps(prob, max_fes, N, rng):
    return _hunt_escape_loop(prob, max_fes, N, rng, use_gps=True)


def sboa_eds(prob, max_fes, N, rng):
    return _hunt_escape_loop(prob, max_fes, N, rng, use_eds=True)


def sboa_erm(prob, max_fes, N, rng):
    return _hunt_escape_loop(prob, max_fes, N, rng, use_erm=True)
