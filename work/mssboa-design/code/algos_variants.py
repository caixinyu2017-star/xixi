"""Comparison algorithms added during revision, in batched form.

Group 1 - recent SBOA variants (Reviewer 2, comment 3)
    MISBOA  Qin et al.  - incremental-PID feedback regulation + cooperative camouflage
    CGSBOA  Wang et al. - multi-strategy fusion + Cauchy-Gaussian crossover
    LTSBOA  Mai et al.  - logistic-tent chaotic initialization + crossover

Group 2 - recent multi-strategy metaheuristics (Reviewer 3, comment 3)
    MS-TSA  Beskirli, A.; Dag, I.; Kiran, M.S., Appl. Soft Comput. 2024, 167, 112220
            (self-adaptive weighting + chaotic elite learning + experience-based learning)
    I-CPA   Beskirli, A.; Dag, I., Biomimetics 2023, 8, 569
            (carnivorous plant algorithm + teaching-factor exploitation)

The source codes of these methods are not publicly distributed, so each was
re-implemented following the equations, control parameters and pseudo-code of
the corresponding publication.  The base algorithms TSA (Kiran 2015) and CPA
(Ong et al. 2021) are implemented first and the published modifications layered
on top, so each variant's gain over its own base is reproduced rather than
assumed.
"""
import numpy as np

from framework import Recorder, init_pop, greedy, levy
from algos_mssboa import good_point_set


# =========================================================================
#  Shared SBOA skeleton
# =========================================================================
def _sboa_skeleton(prob, max_fes, N, rng, X0, hunt=None, escape=None,
                   post=None, extra_per_iter=0):
    rec = Recorder(prob, max_fes)
    D = prob.dim
    X = X0
    F = rec.evaluate(X)
    X = X[:len(F)]
    gb = int(np.argmin(F))
    Xbest, fbest = X[gb].copy(), float(F[gb])
    T = max(1, int(max_fes / (2 * N + extra_per_iter)))
    state = {}
    t = 0
    idx = np.arange(N)
    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)
        # ---- hunting ----
        Xn = None
        if hunt is not None:
            Xn = hunt(X, F, Xbest, t, T, tt, rng, D, N, state, idx)
        if Xn is None:
            if tt < 1 / 3:
                a = rng.integers(0, N, N)
                b = rng.integers(0, N, N)
                a = np.where(a == idx, (a + 1) % N, a)
                b = np.where(b == a, (b + 1) % N, b)
                Xn = X + (X[a] - X[b]) * rng.random((N, D))
            elif tt < 2 / 3:
                RB = rng.normal(0, 1, (N, D))
                Xn = Xbest + np.exp(tt ** 4) * (RB - 0.5) * (Xbest - X)
            else:
                Xn = Xbest + ((1 - tt) ** (2 * tt)) * X * (0.5 * levy(rng, (N, D)))
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)
        # ---- escape ----
        Xn = None
        if escape is not None:
            Xn = escape(X, F, Xbest, t, T, tt, rng, D, N, state, idx)
        if Xn is None:
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
        if post is not None and rec.budget_left():
            Xbest, fbest = post(rec, X, F, Xbest, fbest, t, T, tt, rng, D, N, state)
    return rec.finalize()


def misboa(prob, max_fes, N, rng):
    """MISBOA - incremental-PID feedback regulation in the first hunting stage
    plus a co-operative camouflage branch in the escape phase.

        e_t  = X_best - X_i(t)
        du_i = Kp (e_t - e_{t-1}) + Ki e_t + Kd (e_t - 2 e_{t-1} + e_{t-2})
    """
    Kp, Ki, Kd = 0.6, 0.2, 0.1
    D = prob.dim
    X0 = good_point_set(N, D, prob.lb, prob.ub)
    err = {'e1': np.zeros((N, D)), 'e2': np.zeros((N, D))}

    def hunt(X, F, Xbest, t, T, tt, rng, D, N, state, idx):
        if tt >= 1 / 3:
            return None
        e0 = Xbest - X
        du = (Kp * (e0 - err['e1']) + Ki * e0
              + Kd * (e0 - 2 * err['e1'] + err['e2']))
        err['e2'] = err['e1'].copy()
        err['e1'] = e0.copy()
        return X + du * rng.random((N, D))

    def escape(X, F, Xbest, t, T, tt, rng, D, N, state, idx):
        a = rng.integers(0, N, N)
        b = rng.integers(0, N, N)
        camo = Xbest + (1 - tt) ** 2 * (2 * rng.random((N, D)) - 1) \
            * (X[a] + X[b]) / 2
        use = (rng.random(N) < 0.5)[:, None]
        R2 = rng.random((N, D))
        K = np.round(1 + rng.random((N, 1)))
        C2 = X + R2 * (X[rng.integers(0, N, N)] - K * X)
        return np.where(use, camo, C2)

    return _sboa_skeleton(prob, max_fes, N, rng, X0, hunt, escape)


def cgsboa(prob, max_fes, N, rng):
    """CGSBOA - multi-strategy fusion with a Cauchy-Gaussian crossover applied
    to the elite once per iteration.

        X' = X_best + (sigma1 Cauchy(0,1) + sigma2 Gauss(0,1)) X_best,
        sigma1 = 1 - t/T, sigma2 = t/T, then binomial crossover with CR = 0.9.
    """
    X0 = init_pop(prob, N, rng)

    def post(rec, X, F, Xbest, fbest, t, T, tt, rng, D, N, state):
        v = Xbest + ((1 - tt) * rng.standard_cauchy(D)
                     + tt * rng.standard_normal(D)) * Xbest
        mask = rng.random(D) < 0.9
        mask[rng.integers(D)] = True
        cand = np.where(mask, v, Xbest)
        f = rec.evaluate(cand)
        if len(f) and f[0] < fbest:
            w = int(np.argmax(F))
            X[w], F[w] = np.clip(cand, rec.prob.lb, rec.prob.ub), float(f[0])
            return X[w].copy(), float(f[0])
        return Xbest, fbest

    return _sboa_skeleton(prob, max_fes, N, rng, X0, post=post, extra_per_iter=1)


def _logistic_tent(N, D, rng, mu=4.0, a=0.7):
    """Composite logistic-tent chaotic map used by Mai et al."""
    z = rng.random(D) * 0.98 + 0.01
    out = np.empty((N, D))
    for i in range(N):
        logi = mu * z * (1 - z)
        tent = np.where(z < a, z / a, (1 - z) / (1 - a))
        z = np.clip(np.mod(logi + tent, 1.0), 1e-6, 1 - 1e-6)
        out[i] = z
    return out


def ltsboa(prob, max_fes, N, rng):
    """LTSBOA - logistic-tent chaotic initialization plus a binomial crossover
    between each individual and the elite in the first hunting stage."""
    Z = _logistic_tent(N, prob.dim, rng)
    X0 = prob.lb + Z * (prob.ub - prob.lb)

    def hunt(X, F, Xbest, t, T, tt, rng, D, N, state, idx):
        if tt >= 1 / 3:
            return None
        a = rng.integers(0, N, N)
        b = rng.integers(0, N, N)
        a = np.where(a == idx, (a + 1) % N, a)
        b = np.where(b == a, (b + 1) % N, b)
        v = X + (X[a] - X[b]) * rng.random((N, D))
        cr = 0.9 - 0.5 * tt
        mask = rng.random((N, D)) < cr
        mask[np.arange(N), rng.integers(0, D, N)] = True
        return np.where(mask, v, Xbest)

    return _sboa_skeleton(prob, max_fes, N, rng, X0, hunt)


# =========================================================================
#  TSA / MS-TSA
# =========================================================================
def _tsa_core(prob, max_fes, N, rng, multi_strategy):
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    ST = 0.1                                    # search tendency (Kiran 2015)
    X = init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    B = X[int(np.argmin(F))].copy()
    fB = float(F.min())
    P, fP = X.copy(), F.copy()                  # experience memory (MS-TSA)
    ns = max(2, int(0.175 * N))                 # seeds per tree, 10-25% of N
    T = max(1, int(max_fes / (N * ns)))
    chaos = rng.random()
    t = 0
    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)
        w = 0.9 - 0.5 * tt if multi_strategy else 1.0
        for _ in range(ns):
            if not rec.budget_left():
                break
            r = rng.integers(0, N, N)
            phi = (rng.random((N, D)) - 0.5) * 2
            use_best = rng.random((N, 1)) < ST
            S = np.where(use_best, w * X + (B - X[r]) * phi,
                         w * X + (X - X[r]) * phi)
            if multi_strategy:
                exp_mask = rng.random((N, 1)) < 0.25
                S = np.where(exp_mask, S + rng.random((N, D)) * (P - X), S)
            Fs = rec.evaluate(S)
            m = len(Fs)
            if not m:
                break
            imp = Fs < F[:m]
            X[:m][imp], F[:m][imp] = S[:m][imp], Fs[imp]
            bp = F < fP
            P[bp], fP[bp] = X[bp], F[bp]
            j = int(np.argmin(F))
            if F[j] < fB:
                B, fB = X[j].copy(), float(F[j])
        if multi_strategy and rec.budget_left():
            chaos = min(max(4.0 * chaos * (1 - chaos), 1e-6), 1 - 1e-6)
            cand = B + (1 - tt) * (2 * chaos - 1) * (ub - lb) * 0.1
            f = rec.evaluate(cand)
            if len(f) and f[0] < fB:
                B, fB = np.clip(cand, lb, ub), float(f[0])
                wst = int(np.argmax(F))
                X[wst], F[wst] = B.copy(), fB
    return rec.finalize()


def tsa(prob, max_fes, N, rng):
    return _tsa_core(prob, max_fes, N, rng, False)


def ms_tsa(prob, max_fes, N, rng):
    return _tsa_core(prob, max_fes, N, rng, True)


# =========================================================================
#  CPA / I-CPA
# =========================================================================
def _cpa_core(prob, max_fes, N, rng, teaching_factor):
    rec = Recorder(prob, max_fes)
    D = prob.dim
    n_cp = max(2, int(round(0.2 * N)))
    attraction, growth_rate, repro_rate = 0.8, 2.0, 1.8
    X = init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    while rec.budget_left():
        order = np.argsort(F)
        X, F = X[order], F[order]
        CP, fCP = X[:n_cp].copy(), F[:n_cp].copy()
        Prey, fPrey = X[n_cp:].copy(), F[n_cp:].copy()
        n_prey = len(Prey)
        grp = np.arange(n_prey) % n_cp
        # ---- growth (exploration) ----
        g = growth_rate * rng.random((n_prey, 1))
        attract = (rng.random((n_prey, 1)) < attraction)
        new = np.where(attract, g * CP[grp] + (1 - g) * Prey,
                       g * Prey + (1 - g) * CP[grp])
        Fn = rec.evaluate(new)
        m = len(Fn)
        if m:
            a = attract[:m, 0]
            for i in range(m):
                if a[i]:
                    if Fn[i] < fCP[grp[i]]:
                        CP[grp[i]], fCP[grp[i]] = new[i], Fn[i]
                elif Fn[i] < fPrey[i]:
                    Prey[i], fPrey[i] = new[i], Fn[i]
        if not rec.budget_left():
            X = np.vstack([CP, Prey]); F = np.concatenate([fCP, fPrey]); break
        # ---- reproduction (exploitation) ----
        if teaching_factor:
            TF = np.round(1 + rng.random((n_cp, 1)))
            cand = CP + rng.random((n_cp, D)) * (CP[0] - TF * CP.mean(axis=0))
        else:
            a = rng.integers(0, n_cp, n_cp)
            b = rng.integers(0, n_cp, n_cp)
            cand = CP[0] + repro_rate * rng.random((n_cp, D)) * (CP[a] - CP[b])
        Fc = rec.evaluate(cand)
        m = len(Fc)
        if m:
            imp = Fc < fCP[:m]
            CP[:m][imp], fCP[:m][imp] = cand[:m][imp], Fc[imp]
        X = np.vstack([CP, Prey])
        F = np.concatenate([fCP, fPrey])
    return rec.finalize()


def cpa(prob, max_fes, N, rng):
    return _cpa_core(prob, max_fes, N, rng, False)


def i_cpa(prob, max_fes, N, rng):
    return _cpa_core(prob, max_fes, N, rng, True)


VARIANTS = {
    'MISBOA': misboa, 'CGSBOA': cgsboa, 'LTSBOA': ltsboa,
    'TSA': tsa, 'MS-TSA': ms_tsa, 'CPA': cpa, 'I-CPA': i_cpa,
}
