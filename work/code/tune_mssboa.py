"""Design-space micro-benchmark for MSSBOA variants on CEC2017 10D."""
import sys, os, time
import numpy as np
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framework import Recorder, init_pop, clipx, levy, Problem
from algos_sboa import _good_point_set, sboa


def sboa_var(prob, max_fes, N, rng, mode='v3', use_gps=True, use_atp=True, cr=0.5):
    """mode: 'v3' current-to-elite vector; 'v3d' crossover-gated EDS; 'v1' golden-sine hybrid."""
    TAU = (np.sqrt(5) - 1) / 2
    rec = Recorder(prob, max_fes)
    D = prob.dim
    X = _good_point_set(N, D, prob.lb, prob.ub) if use_gps else init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    gb = np.argmin(F); Xbest, fbest = X[gb].copy(), F[gb]
    T = max(1, max_fes // (2 * N + (1 if use_atp else 0)))
    t = 0
    while rec.budget_left():
        t += 1; tt = min(t / T, 1.0)
        order = np.argsort(F)
        elites = [X[order[0]], X[order[1]], X[order[2]],
                  X[order[:max(3, N // 10)]].mean(axis=0)]
        for i in range(N):
            if not rec.budget_left(): break
            if t < T / 3:
                Xe = elites[rng.integers(len(elites))]
                cand = [j for j in range(N) if j != i]
                a, b = rng.choice(cand, 2, replace=False)
                if mode == 'v3':
                    nx = X[i] + rng.random(D) * (Xe - X[i]) + rng.random(D) * (X[a] - X[b])
                elif mode == 'v3d':
                    v = X[i] + rng.random(D) * (Xe - X[i]) + rng.random(D) * (X[a] - X[b])
                    mask = rng.random(D) < cr
                    mask[rng.integers(D)] = True
                    nx = np.where(mask, v, X[i])
                elif mode == 'v1':
                    if rng.random() < 0.5:
                        r1 = rng.random() * 2 * np.pi; r2 = rng.random() * np.pi
                        c1 = -np.pi * (1 - TAU) + np.pi * TAU
                        c2 = -np.pi * TAU + np.pi * (1 - TAU)
                        nx = X[i] * np.abs(np.sin(r1)) + r2 * np.sin(r1) * np.abs(c1 * Xe - c2 * X[i])
                    else:
                        nx = X[i] + (X[a] - X[b]) * rng.random(D)
                else:  # base
                    nx = X[i] + (X[a] - X[b]) * rng.random(D)
            elif t < 2 * T / 3:
                RB = rng.normal(0, 1, D)
                nx = Xbest + np.exp(tt ** 4) * (RB - 0.5) * (Xbest - X[i])
            else:
                RL = 0.5 * levy(rng, D)
                nx = Xbest + ((1 - tt) ** (2 * tt)) * X[i] * RL
            nx = clipx(nx, prob); f = rec.eval(nx)
            if f <= F[i]:
                X[i], F[i] = nx, f
                if f < fbest: Xbest, fbest = nx.copy(), f
        for i in range(N):
            if not rec.budget_left(): break
            if rng.random() < 0.5:
                RB = rng.normal(0, 1, D)
                nx = Xbest + (1 - tt) ** 2 * (2 * RB - 1) * X[i]
            else:
                R2 = rng.random(D); K = int(np.round(1 + rng.random()))
                nx = X[i] + R2 * (X[rng.integers(N)] - K * X[i])
            nx = clipx(nx, prob); f = rec.eval(nx)
            if f <= F[i]:
                X[i], F[i] = nx, f
                if f < fbest: Xbest, fbest = nx.copy(), f
        if use_atp and rec.budget_left():
            df = max(1, t)
            nx = clipx(Xbest * (1 + 0.5 * (1 - tt) * rng.standard_t(df, D)), prob)
            f = rec.eval(nx)
            w = np.argmax(F)
            if f < F[w]:
                X[w], F[w] = nx.copy(), f
                if f < fbest: Xbest, fbest = nx.copy(), f
    return rec.finalize()


CONFIGS = {
    'SBOA':  lambda p, mf, N, r: sboa(p, mf, N, r),
    'V3':    lambda p, mf, N, r: sboa_var(p, mf, N, r, mode='v3'),
    'V3d':   lambda p, mf, N, r: sboa_var(p, mf, N, r, mode='v3d'),
    'V1':    lambda p, mf, N, r: sboa_var(p, mf, N, r, mode='v1'),
    'V3noATP': lambda p, mf, N, r: sboa_var(p, mf, N, r, mode='v3', use_atp=False),
}


def task(args):
    fi, cname, run = args
    import opfunu.cec_based.cec2017 as c17
    f = getattr(c17, f'F{fi}2017')(ndim=10)
    p = Problem(f.evaluate, f.lb, f.ub, 10, f'F{fi}')
    rng = np.random.default_rng(50000 + run * 331 + fi * 17 + hash(cname) % 89)
    bf, _, _ = CONFIGS[cname](p, 10000, 30, rng)
    return fi, cname, run, bf


if __name__ == '__main__':
    tasks = [(fi, c, r) for fi in range(1, 30) for c in CONFIGS for r in range(10)]
    res = {}
    t0 = time.time()
    with Pool(4) as pool:
        for fi, c, r, bf in pool.imap_unordered(task, tasks, chunksize=8):
            res.setdefault((fi, c), []).append(bf)
    print(f'{time.time()-t0:.0f}s')
    from scipy import stats
    names = list(CONFIGS)
    R = np.zeros((29, len(names)))
    for k, fi in enumerate(range(1, 30)):
        R[k] = stats.rankdata([np.mean(res[(fi, c)]) for c in names])
    avg = R.mean(axis=0)
    print('Friedman-style avg rank over 29 funcs:')
    for c, r in sorted(zip(names, avg), key=lambda x: x[1]):
        print(f'  {c:8s} {r:.3f}')
    # win/loss vs SBOA
    for c in names[1:]:
        w = sum(np.mean(res[(fi, c)]) < np.mean(res[(fi, 'SBOA')]) * 0.999 for fi in range(1, 30))
        l = sum(np.mean(res[(fi, c)]) > np.mean(res[(fi, 'SBOA')]) * 1.001 for fi in range(1, 30))
        print(f'  {c} vs SBOA: {w} better / {l} worse')
