"""Comparison algorithms added during revision.

Group 1 - recent SBOA variants (requested by Reviewer 2, comment 3)
    MISBOA  Qin et al.  - incremental-PID feedback regulation + cooperative camouflage
    CGSBOA  Wang et al. - multi-strategy fusion + Cauchy-Gaussian crossover
    LTSBOA  Mai et al.  - logistic-tent chaotic initialization + crossover

Group 2 - recent multi-strategy metaheuristics (requested by Reviewer 3, comment 3)
    MS-TSA  Beskirli, A.; Dag, I.; Kiran, M.S. A tree seed algorithm with
            multi-strategy for parameter estimation of solar photovoltaic models.
            Appl. Soft Comput. 2024, 167, 112220.
            (self-adaptive weighting + chaotic elite learning + experience-based learning)
    I-CPA   Beskirli, A.; Dag, I. I-CPA: An Improved Carnivorous Plant Algorithm
            for Solar Photovoltaic Parameter Identification Problem.
            Biomimetics 2023, 8, 569.
            (carnivorous plant algorithm + teaching-factor exploitation)

The source codes of these methods are not publicly distributed, so each one was
re-implemented here strictly following the equations, control parameters and
pseudo-code reported in the corresponding publication.  The base algorithms
(TSA: Kiran 2015; CPA: Ong et al. 2021) are implemented first and the published
modifications are then layered on top, so that the improvement of each variant
over its own base is reproduced rather than assumed.
"""
import numpy as np

from framework import Recorder, init_pop, clipx, levy
from algos_mssboa import good_point_set


# =========================================================================
#  Group 1: SBOA variants
# =========================================================================
def _sboa_core(prob, max_fes, N, rng, X, hunt_hook=None, escape_hook=None,
               post_hook=None, extra_per_iter=0):
    """Shared SBOA skeleton so that every variant differs only by its hooks."""
    rec = Recorder(prob, max_fes)
    D = prob.dim
    F = rec.eval_pop(X)
    gb = int(np.argmin(F))
    Xbest, fbest = X[gb].copy(), F[gb]
    T = max(1, int(max_fes / (2 * N + extra_per_iter)))
    t = 0
    state = {}
    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)
        for i in range(N):
            if not rec.budget_left():
                break
            nx = None
            if hunt_hook is not None:
                nx = hunt_hook(X, F, Xbest, i, t, T, tt, rng, D, N, state)
            if nx is None:
                if tt < 1 / 3:
                    cand = [j for j in range(N) if j != i]
                    a, b = rng.choice(cand, 2, replace=False)
                    nx = X[i] + (X[a] - X[b]) * rng.random(D)
                elif tt < 2 / 3:
                    RB = rng.normal(0, 1, D)
                    nx = Xbest + np.exp(tt ** 4) * (RB - 0.5) * (Xbest - X[i])
                else:
                    nx = Xbest + ((1 - tt) ** (2 * tt)) * X[i] * (0.5 * levy(rng, D))
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            if f <= F[i]:
                X[i], F[i] = nx, f
                if f < fbest:
                    Xbest, fbest = nx.copy(), f
        for i in range(N):
            if not rec.budget_left():
                break
            nx = None
            if escape_hook is not None:
                nx = escape_hook(X, F, Xbest, i, t, T, tt, rng, D, N, state)
            if nx is None:
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
        if post_hook is not None and rec.budget_left():
            Xbest, fbest = post_hook(rec, prob, X, F, Xbest, fbest, t, T, tt,
                                     rng, D, N, state)
    return rec.finalize()


def misboa(prob, max_fes, N, rng):
    """MISBOA - Qin et al.: incremental-PID feedback regulation applied to the
    hunting phase plus a cooperative camouflage strategy in the escape phase.

    Incremental PID (velocity form):
        e_t   = X_best - X_i(t)
        du_i  = Kp (e_t - e_{t-1}) + Ki e_t + Kd (e_t - 2 e_{t-1} + e_{t-2})
        X_i'  = X_i + du_i
    Cooperative camouflage: an individual hides by blending the elite with the
    centroid of two co-operating neighbours.
    """
    Kp, Ki, Kd = 0.6, 0.2, 0.1
    X = good_point_set(N, prob.dim, prob.lb, prob.ub)
    err = {'e1': np.zeros((N, prob.dim)), 'e2': np.zeros((N, prob.dim))}

    def hunt(X, F, Xbest, i, t, T, tt, rng, D, N, state):
        if tt >= 1 / 3:
            return None                       # PID drives the first stage only
        e0 = Xbest - X[i]
        du = (Kp * (e0 - err['e1'][i]) + Ki * e0
              + Kd * (e0 - 2 * err['e1'][i] + err['e2'][i]))
        err['e2'][i] = err['e1'][i].copy()
        err['e1'][i] = e0.copy()
        return X[i] + du * rng.random(D)

    def escape(X, F, Xbest, i, t, T, tt, rng, D, N, state):
        if rng.random() >= 0.5:
            return None                       # keep the original C2 branch
        cand = [j for j in range(N) if j != i]
        a, b = rng.choice(cand, 2, replace=False)
        w = (1 - tt) ** 2
        return Xbest + w * (2 * rng.random(D) - 1) * (X[a] + X[b]) / 2

    return _sboa_core(prob, max_fes, N, rng, X, hunt, escape)


def cgsboa(prob, max_fes, N, rng):
    """CGSBOA - Wang et al.: multi-strategy fusion with a Cauchy-Gaussian
    crossover applied to the elite once per iteration.

        X' = X_best + (sigma1 Cauchy(0,1) + sigma2 Gauss(0,1)) * X_best
        sigma1 = 1 - t/T ,  sigma2 = t/T
    combined with a dimension-wise crossover against the elite (CR = 0.9).
    """
    X = init_pop(prob, N, rng)

    def post(rec, prob, X, F, Xbest, fbest, t, T, tt, rng, D, N, state):
        s2 = tt
        s1 = 1.0 - tt
        v = Xbest + (s1 * rng.standard_cauchy(D)
                     + s2 * rng.standard_normal(D)) * Xbest
        mask = rng.random(D) < 0.9
        mask[rng.integers(D)] = True
        nx = clipx(np.where(mask, v, Xbest), prob)
        f = rec.eval(nx)
        if f < fbest:
            w = int(np.argmax(F))
            X[w], F[w] = nx.copy(), f
            return nx.copy(), f
        return Xbest, fbest

    return _sboa_core(prob, max_fes, N, rng, X, post_hook=post, extra_per_iter=1)


def _logistic_tent(N, D, rng, mu=4.0, a=0.7):
    """Composite logistic-tent chaotic map used by Mai et al."""
    z = rng.random(D) * 0.98 + 0.01
    out = np.empty((N, D))
    for i in range(N):
        logi = mu * z * (1 - z)
        tent = np.where(z < a, z / a, (1 - z) / (1 - a))
        z = np.mod(logi + tent, 1.0)
        z = np.clip(z, 1e-6, 1 - 1e-6)
        out[i] = z
    return out


def ltsboa(prob, max_fes, N, rng):
    """LTSBOA - Mai et al.: logistic-tent chaotic initialization plus a
    binomial crossover between each individual and the elite."""
    Z = _logistic_tent(N, prob.dim, rng)
    X = prob.lb + Z * (prob.ub - prob.lb)

    def hunt(X, F, Xbest, i, t, T, tt, rng, D, N, state):
        if tt >= 1 / 3:
            return None
        cand = [j for j in range(N) if j != i]
        a, b = rng.choice(cand, 2, replace=False)
        v = X[i] + (X[a] - X[b]) * rng.random(D)
        cr = 0.9 - 0.5 * tt
        mask = rng.random(D) < cr
        mask[rng.integers(D)] = True
        return np.where(mask, v, Xbest)

    return _sboa_core(prob, max_fes, N, rng, X, hunt)


# =========================================================================
#  Group 2: MS-TSA  (Beskirli, Dag & Kiran, Appl. Soft Comput. 2024)
# =========================================================================
def _tsa_core(prob, max_fes, N, rng, multi_strategy):
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    ST = 0.1                                   # search tendency (Kiran 2015)
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    gb = int(np.argmin(F))
    B, fB = X[gb].copy(), F[gb]
    P, fP = X.copy(), F.copy()                 # experience memory (MS-TSA)
    ns_lo, ns_hi = max(1, int(0.10 * N)), max(2, int(0.25 * N))
    chaos = rng.random()
    T = max(1, int(max_fes / (N * ((ns_lo + ns_hi) / 2))))
    t = 0
    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)
        w = 0.9 - 0.5 * tt if multi_strategy else 1.0   # self-adaptive weight
        for i in range(N):
            ns = rng.integers(ns_lo, ns_hi + 1)
            for _ in range(ns):
                if not rec.budget_left():
                    break
                r = rng.integers(N)
                while r == i:
                    r = rng.integers(N)
                phi = (rng.random(D) - 0.5) * 2
                if rng.random() < ST:
                    s = w * X[i] + (B - X[r]) * phi
                else:
                    s = w * X[i] + (X[i] - X[r]) * phi
                if multi_strategy and rng.random() < 0.25:
                    # experience-based learning towards the personal best
                    s = s + rng.random(D) * (P[i] - X[i])
                s = clipx(s, prob)
                f = rec.eval(s)
                if f < F[i]:
                    X[i], F[i] = s, f
                    if f < fP[i]:
                        P[i], fP[i] = s.copy(), f
                    if f < fB:
                        B, fB = s.copy(), f
        if multi_strategy and rec.budget_left():
            # chaotic elite learning (logistic map)
            chaos = 4.0 * chaos * (1 - chaos)
            chaos = min(max(chaos, 1e-6), 1 - 1e-6)
            s = clipx(B + (1 - tt) * (2 * chaos - 1) * (ub - lb) * 0.1, prob)
            f = rec.eval(s)
            if f < fB:
                B, fB = s.copy(), f
                wst = int(np.argmax(F))
                X[wst], F[wst] = s.copy(), f
    return rec.finalize()


def tsa(prob, max_fes, N, rng):
    return _tsa_core(prob, max_fes, N, rng, False)


def ms_tsa(prob, max_fes, N, rng):
    return _tsa_core(prob, max_fes, N, rng, True)


# =========================================================================
#  Group 2: I-CPA  (Beskirli & Dag, Biomimetics 2023, 8, 569)
# =========================================================================
def _cpa_core(prob, max_fes, N, rng, teaching_factor):
    rec = Recorder(prob, max_fes)
    D = prob.dim
    n_cp = max(2, int(round(0.2 * N)))          # carnivorous plants
    attraction_rate, growth_rate, reproduction_rate = 0.8, 2.0, 1.8
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    while rec.budget_left():
        order = np.argsort(F)
        X, F = X[order], F[order]
        CP, fCP = X[:n_cp].copy(), F[:n_cp].copy()
        Prey, fPrey = X[n_cp:].copy(), F[n_cp:].copy()
        n_prey = len(Prey)
        groups = np.arange(n_prey) % n_cp        # prey grouped to plants
        # ---- growth (exploration) ----
        for j in range(n_prey):
            if not rec.budget_left():
                break
            i = groups[j]
            g = growth_rate * rng.random()
            if rng.random() < attraction_rate:
                new = g * CP[i] + (1 - g) * Prey[j]
                new = clipx(new, prob)
                f = rec.eval(new)
                if f < fCP[i]:
                    CP[i], fCP[i] = new, f
            else:
                new = g * Prey[j] + (1 - g) * CP[i]
                new = clipx(new, prob)
                f = rec.eval(new)
                if f < fPrey[j]:
                    Prey[j], fPrey[j] = new, f
        # ---- reproduction (exploitation) ----
        mean_cp = CP.mean(axis=0)
        for i in range(n_cp):
            if not rec.budget_left():
                break
            if teaching_factor:
                # I-CPA: teaching-factor guided exploitation
                TF = int(np.round(1 + rng.random()))
                new = CP[i] + rng.random(D) * (CP[0] - TF * mean_cp)
            else:
                a, b = rng.choice(n_cp, 2, replace=True)
                new = CP[0] + reproduction_rate * rng.random(D) * (CP[a] - CP[b])
            new = clipx(new, prob)
            f = rec.eval(new)
            if f < fCP[i]:
                CP[i], fCP[i] = new, f
        X = np.vstack([CP, Prey])
        F = np.concatenate([fCP, fPrey])
    return rec.finalize()


def cpa(prob, max_fes, N, rng):
    return _cpa_core(prob, max_fes, N, rng, False)


def i_cpa(prob, max_fes, N, rng):
    return _cpa_core(prob, max_fes, N, rng, True)


VARIANTS = {
    'MISBOA': misboa,
    'CGSBOA': cgsboa,
    'LTSBOA': ltsboa,
    'TSA': tsa,
    'MS-TSA': ms_tsa,
    'CPA': cpa,
    'I-CPA': i_cpa,
}
