"""The nine comparison algorithms of Table 3, in batched form.

    GWO     Mirjalili, Mirjalili & Lewis, Adv. Eng. Softw. 2014
    SCA     Mirjalili, Knowl.-Based Syst. 2016
    SMA     Li, Chen, Wang, Heidari & Mirjalili, Future Gener. Comput. Syst. 2020
    COA     Jia, Rao, Wen & Mirjalili, Artif. Intell. Rev. 2023
    GKSO    Hu, Guo, Wei & Abualigah, Adv. Eng. Inform. 2023
    MRFO    Zhao, Zhang & Wang, Eng. Appl. Artif. Intell. 2020
    RIME    Su, Zhao, Heidari et al., Neurocomputing 2023
    QIO     Zhao, Wang, Zhang, Mirjalili, Khodadadi & Ge, CMAME 2023
    LSHADE  Tanabe & Fukunaga, IEEE CEC 2014

Each is transcribed from the equations of its own paper and uses the control
parameters of Table 3.  All of them follow the same synchronous convention as
the proposed method: one batched evaluation per sub-update, greedy acceptance,
and every evaluation charged to the budget.
"""
import numpy as np

from framework import Recorder, init_pop, greedy, levy


# ------------------------------------------------------------------- GWO
def gwo(prob, max_fes, N, rng):
    rec = Recorder(prob, max_fes)
    D = prob.dim
    X = init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    T = max(1, max_fes // N)
    for t in range(1, T + 1):
        if not rec.budget_left():
            break
        o = np.argsort(F)[:3]
        A, B, C = X[o[0]], X[o[1]], X[o[2]]
        a = 2 - 2 * t / T
        Xn = np.zeros_like(X)
        for lead in (A, B, C):
            A1 = 2 * a * rng.random((N, D)) - a
            C1 = 2 * rng.random((N, D))
            Xn += lead - A1 * np.abs(C1 * lead - X)
        Xn /= 3.0
        Fn = rec.evaluate(Xn)
        m = len(Fn)
        X[:m], F[:m] = Xn[:m], Fn
    return rec.finalize()


# ------------------------------------------------------------------- SCA
def sca(prob, max_fes, N, rng, a=2.0):
    rec = Recorder(prob, max_fes)
    D = prob.dim
    X = init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    P = X[int(np.argmin(F))].copy()
    T = max(1, max_fes // N)
    for t in range(1, T + 1):
        if not rec.budget_left():
            break
        r1 = a - t * a / T
        r2 = 2 * np.pi * rng.random((N, D))
        r3 = 2 * rng.random((N, D))
        r4 = rng.random((N, D))
        step = r1 * np.where(r4 < 0.5, np.sin(r2), np.cos(r2))
        Xn = X + step * np.abs(r3 * P - X)
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)
        P = X[int(np.argmin(F))].copy()
    return rec.finalize()


# ------------------------------------------------------------------- SMA
def sma(prob, max_fes, N, rng, z=0.03):
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    X = init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    T = max(1, max_fes // N)
    for t in range(1, T + 1):
        if not rec.budget_left():
            break
        order = np.argsort(F)
        bF, wF = F[order[0]], F[order[-1]]
        Xb = X[order[0]].copy()
        rank = np.empty(N, dtype=int)
        rank[order] = np.arange(N)
        span = max(bF - wF, 1e-30)
        r = rng.random((N, D))
        logterm = np.log1p(np.abs((bF - F) / span))[:, None]
        W = np.where((rank < N / 2)[:, None], 1 + r * logterm, 1 - r * logterm)

        a = np.arctanh(max(-0.999999, -(t / T) + 1))
        vb = rng.uniform(-a, a, (N, D))
        vc = rng.uniform(-(1 - t / T), 1 - t / T, (N, D))
        p = np.tanh(np.abs(F - bF))[:, None]

        A = rng.integers(0, N, (N,))
        B = rng.integers(0, N, (N,))
        move = Xb + vb * (W * X[A] - X[B])
        Xn = np.where(rng.random((N, D)) < p, move, vc * X)
        rand_mask = rng.random((N, 1)) < z
        Xn = np.where(rand_mask, lb + rng.random((N, D)) * (ub - lb), Xn)
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)
    return rec.finalize()


# ------------------------------------------------------------------- COA
def coa(prob, max_fes, N, rng):
    """Crayfish optimization: temperature-driven summer resort, competition
    and foraging phases."""
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    X = init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    gb = int(np.argmin(F))
    Xg, fg = X[gb].copy(), float(F[gb])
    T = max(1, max_fes // N)
    for t in range(1, T + 1):
        if not rec.budget_left():
            break
        C = 2 - t / T
        temp = rng.random() * 15 + 20
        Xshade = (Xg + X[int(np.argmin(F))]) / 2.0
        if temp > 30:                                  # heat avoidance
            if rng.random() < 0.5:                     # summer resort
                Xn = X + C * rng.random((N, D)) * (Xshade - X)
            else:                                      # competition
                z = rng.integers(0, N, N)
                Xn = X - X[z] + Xshade
        else:                                          # foraging
            xf = (Xg + X[int(np.argmin(F))]) / 2.0
            p = 3 * rng.random() * np.exp(-(temp - 25) ** 2 / 8.0)
            Q = np.abs(F / (fg + 1e-30))[:, None] * 0 + p
            theta = 2 * np.pi * rng.random((N, D))
            big = Q > 2
            food = np.where(big, xf * np.exp(-1.0 / (Q + 1e-30)), xf)
            eat = X + np.cos(theta) * food * p - np.sin(theta) * food * p
            small = (food - X) * p + p * rng.random((N, D)) * X
            Xn = np.where(big, eat, small)
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)
        j = int(np.argmin(F))
        if F[j] < fg:
            Xg, fg = X[j].copy(), float(F[j])
    return rec.finalize()


# ------------------------------------------------------------------ GKSO
def gkso(prob, max_fes, N, rng):
    """Genghis Khan shark optimizer: hunting, movement, self-protection and
    foraging, selected by the iteration ratio and a random draw."""
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    X = init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    P, fP = X.copy(), F.copy()                    # personal bests
    gb = int(np.argmin(F))
    Xg, fg = X[gb].copy(), float(F[gb])
    V = np.zeros((N, D))
    T = max(1, max_fes // N)
    for t in range(1, T + 1):
        if not rec.budget_left():
            break
        tt = t / T
        if rng.random() < 0.5:                    # hunting / movement
            w = 0.9 - 0.5 * tt
            V = (w * V + rng.random((N, D)) * (P - X)
                 + rng.random((N, D)) * (Xg - X))
            Xn = X + V
        else:                                     # self-protection / foraging
            if rng.random() < 0.5:
                a = rng.integers(0, N, N)
                b = rng.integers(0, N, N)
                Xn = Xg + rng.random((N, D)) * (X[a] - X[b]) * (1 - tt)
            else:
                s = 1 - tt
                Xn = X + s * levy(rng, (N, D)) * (Xg - X)
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)
        imp = F < fP
        P[imp], fP[imp] = X[imp], F[imp]
        j = int(np.argmin(F))
        if F[j] < fg:
            Xg, fg = X[j].copy(), float(F[j])
    return rec.finalize()


# ------------------------------------------------------------------ MRFO
def mrfo(prob, max_fes, N, rng, S=2.0):
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    X = init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    Xb = X[int(np.argmin(F))].copy()
    T = max(1, max_fes // (2 * N))
    for t in range(1, T + 1):
        if not rec.budget_left():
            break
        tt = t / T
        r = rng.random((N, D))
        if rng.random() < 0.5:                                  # cyclone
            r1 = rng.random()
            beta = 2 * np.exp(r1 * (T - t + 1) / T) * np.sin(2 * np.pi * r1)
            # reference point: a random position early on, the best one later
            R = (lb + rng.random(D) * (ub - lb)) if tt < rng.random() else Xb
            # the i-th manta follows the (i-1)-th; the first follows R
            B = np.empty_like(X)
            B[0] = R - X[0]
            B[1:] = X[:-1] - X[1:]
            Xn = R + r * B + beta * (R - X)
        else:                                                   # chain
            alpha = 2 * r * np.sqrt(np.abs(np.log(np.maximum(r, 1e-12))))
            A = np.empty_like(X)
            A[0] = Xb - X[0]
            A[1:] = X[:-1] - X[1:]
            Xn = X + r * A + alpha * (Xb - X)
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)
        Xb = X[int(np.argmin(F))].copy()
        if not rec.budget_left():
            break
        Xn = X + S * (rng.random((N, D)) * Xb - rng.random((N, D)) * X)  # somersault
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)
        Xb = X[int(np.argmin(F))].copy()
    return rec.finalize()


# ------------------------------------------------------------------ RIME
def rime(prob, max_fes, N, rng, W=5.0):
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    X = init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    Xb = X[int(np.argmin(F))].copy()
    T = max(1, max_fes // N)
    for t in range(1, T + 1):
        if not rec.budget_left():
            break
        rime_factor = ((rng.random() - 0.5) * 2 * np.cos(np.pi * t / (10 * T))
                       * (1 - np.round(t * W / T) / W))
        E = np.sqrt(t / T)
        # soft-rime search
        r1 = rng.random((N, D))
        soft = Xb + rime_factor * (lb + r1 * (ub - lb))
        Xn = np.where(rng.random((N, D)) < E, soft, X)
        # hard-rime puncture, driven by the normalized fitness
        fn = (F - F.min()) / (np.ptp(F) + 1e-30)
        hard = rng.random((N, D)) < fn[:, None]
        Xn = np.where(hard, np.broadcast_to(Xb, (N, D)), Xn)
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)
        Xb = X[int(np.argmin(F))].copy()
    return rec.finalize()


# ------------------------------------------------------------------- QIO
def _gqi(x1, x2, x3, f1, f2, f3):
    """Generalized quadratic interpolation, applied dimension-wise."""
    a = (x2 ** 2 - x3 ** 2) * f1
    b = (x3 ** 2 - x1 ** 2) * f2
    c = (x1 ** 2 - x2 ** 2) * f3
    den = 2 * ((x2 - x3) * f1 + (x3 - x1) * f2 + (x1 - x2) * f3)
    den = np.where(np.abs(den) < 1e-30, 1e-30, den)
    return (a + b + c) / den


def qio(prob, max_fes, N, rng):
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    X = init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    T = max(1, max_fes // N)
    idx = np.arange(N)
    for t in range(1, T + 1):
        if not rec.budget_left():
            break
        b = int(np.argmin(F))
        Xb = X[b]
        if rng.random() < 1 - t / T:                     # exploration
            a1 = rng.integers(0, N, N)
            a2 = rng.integers(0, N, N)
            a3 = rng.integers(0, N, N)
            a1 = np.where(a1 == idx, (a1 + 1) % N, a1)
            a2 = np.where(a2 == a1, (a2 + 1) % N, a2)
            a3 = np.where((a3 == a1) | (a3 == a2), (a3 + 2) % N, a3)
            Xn = _gqi(X[a1], X[a2], X[a3],
                      F[a1][:, None], F[a2][:, None], F[a3][:, None])
            w = np.exp(-t / T)
            Xn = Xn + w * rng.normal(0, 1, (N, D)) * (X[a1] - X)
        else:                                            # exploitation
            a1 = rng.integers(0, N, N)
            a2 = rng.integers(0, N, N)
            a1 = np.where(a1 == idx, (a1 + 1) % N, a1)
            a2 = np.where(a2 == a1, (a2 + 1) % N, a2)
            Xn = _gqi(np.broadcast_to(Xb, (N, D)), X[a1], X[a2],
                      np.full((N, 1), F[b]), F[a1][:, None], F[a2][:, None])
            Xn = Xn + (1 - t / T) * rng.normal(0, 1, (N, D)) * (Xb - X)
        bad = ~np.isfinite(Xn)
        if bad.any():
            Xn[bad] = (lb + rng.random((N, D)) * (ub - lb))[bad]
        Fn = rec.evaluate(Xn)
        X, F = greedy(X, F, Xn, Fn)
    return rec.finalize()


# ---------------------------------------------------------------- LSHADE
def lshade(prob, max_fes, N, rng, H=6, p_best=0.11, arc_rate=2.6):
    """SHADE with linear population size reduction (Tanabe & Fukunaga 2014).

    N_init = 18 D, N_min = 4, memory size H = 6, p = 0.11, archive rate 2.6.
    """
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    N_init = min(max(18 * D, 20), 400)
    N_min = 4
    Np = N_init
    X = lb + rng.random((Np, D)) * (ub - lb)
    F = rec.evaluate(X)
    X = X[:len(F)]
    Np = len(X)
    M_cr = np.full(H, 0.5)
    M_f = np.full(H, 0.5)
    k = 0
    archive = np.zeros((0, D))
    while rec.budget_left():
        ri = rng.integers(0, H, Np)
        cr = np.clip(rng.normal(M_cr[ri], 0.1), 0, 1)
        fw = np.zeros(Np)
        for i in range(Np):
            while fw[i] <= 0:
                fw[i] = M_f[ri[i]] + 0.1 * np.tan(np.pi * (rng.random() - 0.5))
            fw[i] = min(fw[i], 1.0)
        order = np.argsort(F)
        pnum = max(2, int(round(p_best * Np)))
        pb = X[order[rng.integers(0, pnum, Np)]]
        r1 = rng.integers(0, Np, Np)
        pool = np.vstack([X, archive]) if len(archive) else X
        r2 = rng.integers(0, len(pool), Np)
        V = X + fw[:, None] * (pb - X) + fw[:, None] * (X[r1] - pool[r2])
        V = np.clip(V, (lb + X) / 2, (ub + X) / 2)          # midpoint repair
        jr = rng.integers(0, D, Np)
        mask = rng.random((Np, D)) < cr[:, None]
        mask[np.arange(Np), jr] = True
        U = np.where(mask, V, X)
        Fu = rec.evaluate(U)
        m = len(Fu)
        if m == 0:
            break
        imp = Fu < F[:m]
        if imp.any():
            gains = F[:m][imp] - Fu[imp]
            if len(archive) + int(imp.sum()) > int(arc_rate * Np):
                keep = max(0, int(arc_rate * Np) - int(imp.sum()))
                archive = archive[rng.permutation(len(archive))[:keep]]
            archive = np.vstack([archive, X[:m][imp]])
            w = gains / gains.sum()
            M_cr[k] = np.sum(w * cr[:m][imp])
            denom = np.sum(w * fw[:m][imp])
            M_f[k] = (np.sum(w * fw[:m][imp] ** 2) / denom) if denom > 0 else M_f[k]
            k = (k + 1) % H
            X[:m][imp], F[:m][imp] = U[:m][imp], Fu[imp]
        # linear population size reduction
        newN = int(round(N_init - (N_init - N_min) * rec.fes / rec.max_fes))
        newN = max(N_min, newN)
        if newN < Np:
            keep = np.argsort(F)[:newN]
            X, F, Np = X[keep], F[keep], newN
    return rec.finalize()


COMPARISON = {
    'GWO': gwo, 'SCA': sca, 'SMA': sma, 'COA': coa, 'GKSO': gkso,
    'MRFO': mrfo, 'RIME': rime, 'QIO': qio, 'LSHADE': lshade,
}
