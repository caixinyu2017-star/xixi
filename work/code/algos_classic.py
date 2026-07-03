"""Classic and state-of-the-art comparison metaheuristics (standard-literature versions).

All follow signature: algo(prob, max_fes, N, rng) -> (best_f, best_x, curve)
Stopping is by function-evaluation budget.
"""
import numpy as np
from framework import Recorder, init_pop, clipx, levy


# ---------------------------------------------------------------- PSO
def pso(prob, max_fes, N, rng):
    rec = Recorder(prob, max_fes)
    X = init_pop(prob, N, rng)
    V = np.zeros_like(X)
    F = rec.eval_pop(X)
    P, Pf = X.copy(), F.copy()
    g = np.argmin(Pf)
    vmax = 0.1 * (prob.ub - prob.lb)
    T = max(1, max_fes // N)
    t = 0
    while rec.budget_left():
        w = 0.9 - 0.5 * t / T
        r1 = rng.random((N, prob.dim)); r2 = rng.random((N, prob.dim))
        V = w * V + 2.0 * r1 * (P - X) + 2.0 * r2 * (P[g] - X)
        V = np.clip(V, -vmax, vmax)
        X = clipx(X + V, prob)
        for i in range(N):
            if not rec.budget_left():
                break
            f = rec.eval(X[i])
            if f < Pf[i]:
                Pf[i], P[i] = f, X[i].copy()
        g = np.argmin(Pf)
        t += 1
    return rec.finalize()


# ---------------------------------------------------------------- DE (rand/1/bin)
def de(prob, max_fes, N, rng, F_=0.5, CR=0.9):
    rec = Recorder(prob, max_fes)
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    while rec.budget_left():
        for i in range(N):
            if not rec.budget_left():
                break
            idx = rng.choice([j for j in range(N) if j != i], 3, replace=False)
            v = X[idx[0]] + F_ * (X[idx[1]] - X[idx[2]])
            jr = rng.integers(prob.dim)
            mask = rng.random(prob.dim) < CR
            mask[jr] = True
            u = clipx(np.where(mask, v, X[i]), prob)
            fu = rec.eval(u)
            if fu <= F[i]:
                X[i], F[i] = u, fu
    return rec.finalize()


# ---------------------------------------------------------------- GWO
def gwo(prob, max_fes, N, rng):
    rec = Recorder(prob, max_fes)
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    T = max(1, max_fes // N)
    t = 0
    while rec.budget_left():
        order = np.argsort(F)
        Xa, Xb, Xd = X[order[0]], X[order[1]], X[order[2]]
        a = 2 - 2 * t / T
        for i in range(N):
            if not rec.budget_left():
                break
            newx = np.zeros(prob.dim)
            for leader in (Xa, Xb, Xd):
                A = 2 * a * rng.random(prob.dim) - a
                C = 2 * rng.random(prob.dim)
                D = np.abs(C * leader - X[i])
                newx += leader - A * D
            newx = clipx(newx / 3, prob)
            f = rec.eval(newx)
            X[i], F[i] = newx, f
        t += 1
    return rec.finalize()


# ---------------------------------------------------------------- WOA
def woa(prob, max_fes, N, rng):
    rec = Recorder(prob, max_fes)
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    T = max(1, max_fes // N)
    t = 0
    while rec.budget_left():
        b_idx = np.argmin(F)
        Xb = X[b_idx].copy()
        a = 2 - 2 * t / T
        a2 = -1 - t / T
        for i in range(N):
            if not rec.budget_left():
                break
            r1, r2 = rng.random(), rng.random()
            A = 2 * a * r1 - a
            C = 2 * r2
            l = (a2 - 1) * rng.random() + 1
            p = rng.random()
            if p < 0.5:
                if abs(A) < 1:
                    D = np.abs(C * Xb - X[i])
                    newx = Xb - A * D
                else:
                    Xr = X[rng.integers(N)]
                    D = np.abs(C * Xr - X[i])
                    newx = Xr - A * D
            else:
                D = np.abs(Xb - X[i])
                newx = D * np.exp(l) * np.cos(2 * np.pi * l) + Xb
            newx = clipx(newx, prob)
            f = rec.eval(newx)
            X[i], F[i] = newx, f
        t += 1
    return rec.finalize()


# ---------------------------------------------------------------- SCA
def sca(prob, max_fes, N, rng):
    rec = Recorder(prob, max_fes)
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    T = max(1, max_fes // N)
    t = 0
    a = 2.0
    while rec.budget_left():
        b_idx = np.argmin(F)
        Xb = X[b_idx].copy()
        r1 = a - a * t / T
        for i in range(N):
            if not rec.budget_left():
                break
            r2 = 2 * np.pi * rng.random(prob.dim)
            r3 = 2 * rng.random(prob.dim)
            r4 = rng.random(prob.dim)
            newx = np.where(r4 < 0.5,
                            X[i] + r1 * np.sin(r2) * np.abs(r3 * Xb - X[i]),
                            X[i] + r1 * np.cos(r2) * np.abs(r3 * Xb - X[i]))
            newx = clipx(newx, prob)
            f = rec.eval(newx)
            X[i], F[i] = newx, f
        t += 1
    return rec.finalize()


# ---------------------------------------------------------------- HHO
def hho(prob, max_fes, N, rng):
    rec = Recorder(prob, max_fes)
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    T = max(1, max_fes // N)
    t = 0
    while rec.budget_left():
        b_idx = np.argmin(F)
        Xb, fb = X[b_idx].copy(), F[b_idx]
        Xm = X.mean(axis=0)
        for i in range(N):
            if not rec.budget_left():
                break
            E0 = 2 * rng.random() - 1
            E = 2 * E0 * (1 - t / T)
            J = 2 * (1 - rng.random())
            if abs(E) >= 1:
                q = rng.random()
                if q >= 0.5:
                    Xr = X[rng.integers(N)]
                    newx = Xr - rng.random() * np.abs(Xr - 2 * rng.random() * X[i])
                else:
                    newx = (Xb - Xm) - rng.random() * (prob.lb + rng.random() * (prob.ub - prob.lb))
            else:
                r = rng.random()
                if r >= 0.5 and abs(E) >= 0.5:
                    newx = (Xb - X[i]) - E * np.abs(J * Xb - X[i])
                elif r >= 0.5:
                    newx = Xb - E * np.abs(Xb - X[i])
                elif abs(E) >= 0.5:
                    Y = Xb - E * np.abs(J * Xb - X[i])
                    Y = clipx(Y, prob)
                    fY = rec.eval(Y)
                    if fY < F[i]:
                        newx = Y
                    else:
                        Z = Y + rng.random(prob.dim) * levy(rng, prob.dim)
                        Z = clipx(Z, prob)
                        if not rec.budget_left():
                            break
                        fZ = rec.eval(Z)
                        newx = Z if fZ < F[i] else X[i]
                else:
                    Y = Xb - E * np.abs(J * Xb - Xm)
                    Y = clipx(Y, prob)
                    fY = rec.eval(Y)
                    if fY < F[i]:
                        newx = Y
                    else:
                        Z = Y + rng.random(prob.dim) * levy(rng, prob.dim)
                        Z = clipx(Z, prob)
                        if not rec.budget_left():
                            break
                        fZ = rec.eval(Z)
                        newx = Z if fZ < F[i] else X[i]
            newx = clipx(newx, prob)
            if not rec.budget_left():
                break
            f = rec.eval(newx)
            if f < F[i]:
                X[i], F[i] = newx, f
        t += 1
    return rec.finalize()


# ---------------------------------------------------------------- SSA (Sparrow Search)
def ssa(prob, max_fes, N, rng, PD=0.2, SD=0.1, ST=0.8):
    rec = Recorder(prob, max_fes)
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    T = max(1, max_fes // N)
    t = 0
    nP = int(N * PD)
    nS = int(N * SD)
    while rec.budget_left():
        order = np.argsort(F)
        X, F = X[order], F[order]
        Xb, fb = X[0].copy(), F[0]
        Xw = X[-1].copy()
        R2 = rng.random()
        for i in range(nP):
            if not rec.budget_left():
                break
            if R2 < ST:
                newx = X[i] * np.exp(-i / (rng.random() * T + 1e-12))
            else:
                newx = X[i] + rng.normal() * np.ones(prob.dim)
            newx = clipx(newx, prob)
            f = rec.eval(newx)
            if f < F[i]:
                X[i], F[i] = newx, f
        bP = X[np.argmin(F[:nP])].copy()
        for i in range(nP, N):
            if not rec.budget_left():
                break
            if i > N / 2:
                newx = rng.normal() * np.exp((Xw - X[i]) / (i + 1) ** 2)
            else:
                A = np.sign(rng.random(prob.dim) - 0.5)
                newx = bP + np.abs(X[i] - bP) * A * rng.random()
            newx = clipx(newx, prob)
            f = rec.eval(newx)
            if f < F[i]:
                X[i], F[i] = newx, f
        idxs = rng.choice(N, nS, replace=False)
        fg = F.min(); fw = F.max()
        for i in idxs:
            if not rec.budget_left():
                break
            if F[i] > fg:
                newx = X[np.argmin(F)] + rng.normal() * np.abs(X[i] - X[np.argmin(F)])
            else:
                K = 2 * rng.random() - 1
                newx = X[i] + K * (np.abs(X[i] - Xw) / (F[i] - fw + 1e-50))
            newx = clipx(newx, prob)
            f = rec.eval(newx)
            if f < F[i]:
                X[i], F[i] = newx, f
        t += 1
    return rec.finalize()


# ---------------------------------------------------------------- DBO (Dung Beetle Optimizer)
def dbo(prob, max_fes, N, rng):
    rec = Recorder(prob, max_fes)
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    T = max(1, max_fes // N)
    t = 0
    # role sizes scaled from the original 30-agent split (6 rollers, 6 broods, 7 foragers, 11 thieves)
    n1 = max(1, round(N * 6 / 30)); n2 = max(1, round(N * 6 / 30))
    n3 = max(1, round(N * 7 / 30)); n4 = N - n1 - n2 - n3
    Xw_hist = X[np.argmax(F)].copy()
    while rec.budget_left():
        gb = np.argmin(F)
        Xgb = X[gb].copy()          # global best
        Xw = X[np.argmax(F)].copy() # global worst
        R = 1 - t / T
        # local best of current iteration
        Xlb = Xgb
        newX = X.copy()
        for i in range(N):
            if not rec.budget_left():
                break
            if i < n1:  # ball-rolling / dancing
                if rng.random() < 0.9:
                    alpha = 1 if rng.random() > 0.1 else -1
                    b, k = 0.3, 0.1
                    nx = X[i] + alpha * k * Xw_hist + b * np.abs(X[i] - Xw)
                else:
                    theta = rng.choice([0, np.pi / 2, np.pi]) if rng.random() < 0.3 else rng.random() * np.pi
                    nx = X[i] + np.tan(theta) * np.abs(X[i] - newX[i - 1] if i > 0 else 0)
            elif i < n1 + n2:  # brood balls around local best
                Lb = np.maximum(Xlb * (1 - R), prob.lb)
                Ub = np.minimum(Xlb * (1 + R), prob.ub)
                b1 = rng.random(prob.dim); b2 = rng.random(prob.dim)
                nx = Xlb + b1 * (X[i] - Lb) + b2 * (X[i] - Ub)
            elif i < n1 + n2 + n3:  # small (foragers) around global best
                Lb = np.maximum(Xgb * (1 - R), prob.lb)
                Ub = np.minimum(Xgb * (1 + R), prob.ub)
                C1 = rng.normal(); C2 = rng.random(prob.dim)
                nx = X[i] + C1 * (X[i] - Lb) + C2 * (X[i] - Ub)
            else:  # thieves
                g = rng.normal(0, 1, prob.dim)
                S = 0.5
                nx = Xgb + S * g * (np.abs(X[i] - Xlb) + np.abs(X[i] - Xgb))
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            if f < F[i]:
                X[i], F[i] = nx, f
        Xw_hist = X[np.argmax(F)].copy()
        t += 1
    return rec.finalize()


# ---------------------------------------------------------------- COA (Crayfish Optimization)
def coa(prob, max_fes, N, rng):
    rec = Recorder(prob, max_fes)
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    T = max(1, max_fes // N)
    t = 0
    while rec.budget_left():
        gb = np.argmin(F)
        Xgb, fgb = X[gb].copy(), F[gb]
        C2 = 2 - t / T
        temp = rng.random() * 15 + 20
        xshade = (Xgb + X[F.argsort()[0]]) / 2
        for i in range(N):
            if not rec.budget_left():
                break
            if temp > 30:
                if rng.random() < 0.5:  # summer resort (cave)
                    nx = X[i] + C2 * rng.random(prob.dim) * (xshade - X[i])
                else:  # competition
                    z = rng.integers(N)
                    nx = X[i] - X[z] + xshade
            else:  # foraging
                P = 3 * rng.random() * F[i] / (fgb + 1e-50)
                food = Xgb
                if P > 2:
                    food = food * np.exp(-1 / (P + 1e-50))
                    nx = X[i] + np.cos(2 * np.pi * rng.random()) * food * (rng.random() * (2 - t / T)) \
                         - np.sin(2 * np.pi * rng.random()) * food * (rng.random() * (2 - t / T))
                else:
                    nx = (X[i] - food) * (rng.random() * (2 - t / T)) + (rng.random() * (2 - t / T)) * food
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            if f < F[i]:
                X[i], F[i] = nx, f
        t += 1
    return rec.finalize()


# ---------------------------------------------------------------- RIME
def rime(prob, max_fes, N, rng, W=5):
    rec = Recorder(prob, max_fes)
    X = init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    T = max(1, max_fes // N)
    t = 0
    while rec.budget_left():
        gb = np.argmin(F)
        Xb, fb = X[gb].copy(), F[gb]
        RimeFactor = (rng.random() - 0.5) * 2 * np.cos(np.pi * t / (T * 10)) * (1 - np.round(t * W / T) / W)
        E = np.sqrt(t / T)
        Fn = (F - F.min()) / (F.max() - F.min() + 1e-50)
        for i in range(N):
            if not rec.budget_left():
                break
            nx = X[i].copy()
            for j in range(prob.dim):
                if rng.random() < E:  # soft-rime
                    nx[j] = Xb[j] + RimeFactor * ((prob.ub[j] - prob.lb[j]) * rng.random() + prob.lb[j])
                if rng.random() < Fn[i]:  # hard-rime puncture
                    nx[j] = Xb[j]
            nx = clipx(nx, prob)
            f = rec.eval(nx)
            if f < F[i]:
                X[i], F[i] = nx, f
        t += 1
    return rec.finalize()


# ---------------------------------------------------------------- LSHADE
def lshade(prob, max_fes, N, rng, H=6, p_best=0.11, arc_rate=2.6):
    rec = Recorder(prob, max_fes)
    D = prob.dim
    N_init = round(18 * D) if N is None else max(N, round(18 * D))
    N_min = 4
    NP = N_init
    X = init_pop(prob, NP, rng)
    F = rec.eval_pop(X)
    MF = np.full(H, 0.5)
    MCR = np.full(H, 0.5)
    k = 0
    archive = []
    while rec.budget_left():
        SF, SCR, dif = [], [], []
        order = np.argsort(F)
        newX = X.copy(); newF = F.copy()
        for i in range(NP):
            if not rec.budget_left():
                break
            r = rng.integers(H)
            cr = np.clip(rng.normal(MCR[r], 0.1), 0, 1)
            while True:
                f_ = MF[r] + 0.1 * np.tan(np.pi * (rng.random() - 0.5))
                if f_ > 0:
                    break
            f_ = min(f_, 1.0)
            pN = max(2, int(round(p_best * NP)))
            xp = X[order[rng.integers(pN)]]
            idx1 = rng.integers(NP)
            while idx1 == i:
                idx1 = rng.integers(NP)
            pool = list(range(NP)) + list(range(len(archive)))
            idx2 = rng.integers(len(pool))
            while pool[idx2] == i or (idx2 < NP and pool[idx2] == idx1):
                idx2 = rng.integers(len(pool))
            x2 = X[pool[idx2]] if idx2 < NP else archive[pool[idx2]]
            v = X[i] + f_ * (xp - X[i]) + f_ * (X[idx1] - x2)
            v = np.where(v < prob.lb, (prob.lb + X[i]) / 2, v)
            v = np.where(v > prob.ub, (prob.ub + X[i]) / 2, v)
            jr = rng.integers(D)
            mask = rng.random(D) < cr
            mask[jr] = True
            u = np.where(mask, v, X[i])
            fu = rec.eval(u)
            if fu < F[i]:
                if len(archive) < int(arc_rate * NP):
                    archive.append(X[i].copy())
                else:
                    archive[rng.integers(len(archive))] = X[i].copy()
                SF.append(f_); SCR.append(cr); dif.append(F[i] - fu)
                newX[i], newF[i] = u, fu
            elif fu == F[i]:
                newX[i], newF[i] = u, fu
        X, F = newX, newF
        if SF:
            w = np.array(dif) / (np.sum(dif) + 1e-50)
            MF[k] = np.sum(w * np.array(SF) ** 2) / (np.sum(w * np.array(SF)) + 1e-50)
            MCR[k] = np.sum(w * np.array(SCR))
            k = (k + 1) % H
        # linear population size reduction
        NP_new = int(round(N_init - (N_init - N_min) * rec.fes / max_fes))
        NP_new = max(N_min, NP_new)
        if NP_new < NP:
            order = np.argsort(F)
            X, F = X[order[:NP_new]], F[order[:NP_new]]
            NP = NP_new
            maxarc = int(arc_rate * NP)
            while len(archive) > maxarc:
                archive.pop(rng.integers(len(archive)))
    return rec.finalize()


ALGOS = {
    'PSO': pso, 'DE': de, 'GWO': gwo, 'WOA': woa, 'SCA': sca,
    'HHO': hho, 'SSA': ssa, 'DBO': dbo, 'COA': coa, 'RIME': rime, 'LSHADE': lshade,
}
