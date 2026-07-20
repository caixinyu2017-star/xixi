import sys, time, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from multiprocessing import Pool
from framework import Recorder, init_pop, clipx, levy, Problem
from algos_sboa import _good_point_set, _qi_point, sboa, TAU


def variant(prob, max_fes, N, rng, stage1='none', use_gps=True, use_erm=True):
    rec = Recorder(prob, max_fes); D = prob.dim
    X = _good_point_set(N, D, prob.lb, prob.ub) if use_gps else init_pop(prob, N, rng)
    F = rec.eval_pop(X)
    gb = np.argmin(F); Xbest, fbest = X[gb].copy(), F[gb]
    T = max(1, max_fes // (2 * N + (1 if use_erm else 0)))
    t = 0
    while rec.budget_left():
        t += 1; tt = min(t / T, 1.0)
        order = np.argsort(F)
        elites = [X[order[0]], X[order[1]], X[order[2]], X[order[:max(3, N // 10)]].mean(axis=0)]
        for i in range(N):
            if not rec.budget_left(): break
            if t < T / 3:
                Xe = elites[rng.integers(4)]
                cand = [j for j in range(N) if j != i]; a, b = rng.choice(cand, 2, replace=False)
                if stage1 == 'egs2' and rng.random() < 0.5:
                    r1 = rng.random() * 2 * np.pi; r2 = rng.random() * np.pi
                    c1 = -np.pi * (1 - TAU) + np.pi * TAU; c2 = -np.pi * TAU + np.pi * (1 - TAU)
                    nx = Xe + np.abs(np.sin(r1)) * (X[i] - Xe) + r2 * np.sin(r1) * np.abs(c1 * Xe - c2 * X[i]) * np.sign(rng.random(D) - 0.5)
                elif stage1 == 'eds':
                    v = X[i] + rng.random(D) * (Xe - X[i]) + rng.random(D) * (X[a] - X[b])
                    mask = rng.random(D) < 0.5
                    mask[rng.integers(D)] = True
                    nx = np.where(mask, v, X[i])
                else:
                    nx = X[i] + (X[a] - X[b]) * rng.random(D)
            elif t < 2 * T / 3:
                RB = rng.normal(0, 1, D)
                nx = Xbest + np.exp(tt ** 4) * (RB - 0.5) * (Xbest - X[i])
            else:
                nx = Xbest + ((1 - tt) ** (2 * tt)) * X[i] * (0.5 * levy(rng, D))
            nx = clipx(nx, prob); f = rec.eval(nx)
            if f <= F[i]:
                X[i], F[i] = nx, f
                if f < fbest: Xbest, fbest = nx.copy(), f
        for i in range(N):
            if not rec.budget_left(): break
            if rng.random() < 0.5:
                RB = rng.normal(0, 1, D); nx = Xbest + (1 - tt) ** 2 * (2 * RB - 1) * X[i]
            else:
                R2 = rng.random(D); K = int(np.round(1 + rng.random()))
                nx = X[i] + R2 * (X[rng.integers(N)] - K * X[i])
            nx = clipx(nx, prob); f = rec.eval(nx)
            if f <= F[i]:
                X[i], F[i] = nx, f
                if f < fbest: Xbest, fbest = nx.copy(), f
        if use_erm and rec.budget_left():
            if t % 2 == 1:
                nx = Xbest * (1 + 0.5 * (1 - tt) * rng.standard_t(max(1, t), D))
            else:
                a, b = rng.choice(N, 2, replace=False)
                nx = _qi_point(Xbest, X[a], X[b], fbest, F[a], F[b])
            nx = clipx(nx, prob); f = rec.eval(nx)
            w = np.argmax(F)
            if f < F[w]:
                X[w], F[w] = nx.copy(), f
                if f < fbest: Xbest, fbest = nx.copy(), f
    return rec.finalize()


CONFIGS = {
    'SBOA':   lambda p, mf, N, r: sboa(p, mf, N, r),
    'M_egs2': lambda p, mf, N, r: variant(p, mf, N, r, stage1='egs2'),
    'M_eds':  lambda p, mf, N, r: variant(p, mf, N, r, stage1='eds'),
    'EGS2':   lambda p, mf, N, r: variant(p, mf, N, r, stage1='egs2', use_gps=False, use_erm=False),
    'EDS':    lambda p, mf, N, r: variant(p, mf, N, r, stage1='eds', use_gps=False, use_erm=False),
}


def task(args):
    fi, cname, run = args
    import opfunu.cec_based.cec2017 as c17
    f = getattr(c17, f'F{fi}2017')(ndim=10)
    p = Problem(f.evaluate, f.lb, f.ub, 10, f'F{fi}')
    rng = np.random.default_rng(90000 + run * 331 + fi * 17 + hash(cname) % 89)
    bf, _, _ = CONFIGS[cname](p, 10000, 30, rng)
    return fi, cname, run, bf


if __name__ == '__main__':
    tasks = [(fi, c, r) for fi in range(1, 30) for c in CONFIGS for r in range(15)]
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
    for c, r in sorted(zip(names, R.mean(axis=0)), key=lambda x: x[1]):
        print(f'  {c:8s} {r:.3f}')
    for c in names[1:]:
        w = sum(np.mean(res[(fi, c)]) < np.mean(res[(fi, 'SBOA')]) * 0.999 for fi in range(1, 30))
        l = sum(np.mean(res[(fi, c)]) > np.mean(res[(fi, 'SBOA')]) * 1.001 for fi in range(1, 30))
        print(f'  {c} vs SBOA: {w}/{l}')
    json.dump({f'{k[0]}|{k[1]}': list(map(float, v)) for k, v in res.items()},
              open('/home/user/xixi/work/results/design_test.json', 'w'))
    print('DESIGN_TEST_DONE')
