"""Secretary Bird Optimization Algorithm (Fu et al., 2024, Artif. Intell. Rev.,
doi:10.1007/s10462-024-10729-y) and the proposed multi-strategy variant MSSBOA.

Faithful to the authors' MATLAB reference implementation (File Exchange #164456):
per iteration each individual performs one hunting sub-update (three time-gated
stages) followed by one escape sub-update, each with greedy acceptance.

MSSBOA adds three strategies:
  GPS  - good point set initialization
  EGS  - elite-guided golden sine search (replaces the blind differential move
         of hunting stage 1)
  ATP  - adaptive t-distribution perturbation of the global best each iteration
"""
import numpy as np
from framework import Recorder, init_pop, clipx, levy

TAU = (np.sqrt(5) - 1) / 2  # golden ratio coefficient


def _hunt_escape_loop(prob, max_fes, N, rng, use_gps=False, use_egs=False, use_atp=False):
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
    # 2 evals per individual per iteration (+1 for ATP)
    T = max(1, max_fes // (2 * N + (1 if use_atp else 0)))
    t = 0
    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)
        # ---------------- hunting strategy (exploration) ----------------
        for i in range(N):
            if not rec.budget_left():
                break
            if t < T / 3:
                if use_egs:
                    # elite-guided golden sine move
                    order = np.argsort(F)
                    elites = [X[order[0]], X[order[1]], X[order[2]],
                              X[order[:max(3, N // 10)]].mean(axis=0)]
                    Xe = elites[rng.integers(len(elites))]
                    r1 = rng.random() * 2 * np.pi
                    r2 = rng.random() * np.pi
                    c1 = -np.pi * (1 - TAU) + np.pi * TAU
                    c2 = -np.pi * TAU + np.pi * (1 - TAU)
                    nx = X[i] * np.abs(np.sin(r1)) + r2 * np.sin(r1) * np.abs(c1 * Xe - c2 * X[i])
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
        # ---------------- adaptive t-distribution perturbation ----------------
        if use_atp and rec.budget_left():
            df = max(1, t)  # degrees of freedom grow with iterations
            step = rng.standard_t(df, D)
            nx = clipx(Xbest * (1 + 0.5 * (1 - tt) * step), prob)
            f = rec.eval(nx)
            if f < fbest:
                Xbest, fbest = nx.copy(), f
                w = np.argmax(F)
                X[w], F[w] = nx.copy(), f
    return rec.finalize()


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


def sboa(prob, max_fes, N, rng):
    return _hunt_escape_loop(prob, max_fes, N, rng)


def mssboa(prob, max_fes, N, rng):
    return _hunt_escape_loop(prob, max_fes, N, rng, use_gps=True, use_egs=True, use_atp=True)


def sboa_gps(prob, max_fes, N, rng):
    return _hunt_escape_loop(prob, max_fes, N, rng, use_gps=True)


def sboa_egs(prob, max_fes, N, rng):
    return _hunt_escape_loop(prob, max_fes, N, rng, use_egs=True)


def sboa_atp(prob, max_fes, N, rng):
    return _hunt_escape_loop(prob, max_fes, N, rng, use_atp=True)
