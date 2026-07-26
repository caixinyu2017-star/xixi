"""Does correcting the two diagnosed defects actually make MSSBOA work?

The operators as printed in the manuscript fail for identifiable reasons:

  LOBL  Eq. (11) refracts about the midpoint of the *static* search interval.
        On CEC2017 that midpoint is the origin, while every optimum is shifted
        away from it, so once k grows the operator re-samples a fixed useless
        point.  Correction: take the optical centre from the *current
        population*, o_j(t) = (min_i x_ij + max_i x_ij)/2, so the lens tracks
        where the swarm actually is.

  ACGM  Eq. (13) is multiplicative, x' = x_best (1 + l1 C + l2 G), so with
        |x_best| ~ 50 even the late-stage "refinement" displaces the elite by
        tens of units.  Correction: make the perturbation additive and scale it
        by the population's own per-dimension spread, which decays as the swarm
        converges.

Both corrections stay inside the paper's own conceptual framework - a lens
image and an adaptive Cauchy-Gaussian perturbation - and neither introduces a
new mechanism.  This script measures whether they matter.
"""
import sys
import os
import time
import zlib
from multiprocessing import Pool

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framework import Recorder, init_pop, greedy, levy         # noqa: E402
from bench import cec2017_problem, CEC2017_IDS                 # noqa: E402
from algos_mssboa import good_point_set, lens_k, sboa          # noqa: E402

RUNS = 10
POP = 30


def run(prob, max_fes, N, rng, gpsi=True, lobl=True, acgm=True,
        adaptive_lens=True, additive_acgm=True,
        rho=0.2, p_m=0.5, beta=1.5, k_root=0.5, k_pow=10.0):
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    X = good_point_set(N, D, lb, ub) if gpsi else init_pop(prob, N, rng)
    F = rec.evaluate(X)
    X = X[:len(F)]
    gb = int(np.argmin(F))
    Xbest, fbest = X[gb].copy(), float(F[gb])
    n_lobl = int(np.ceil(rho * N)) if lobl else 0
    T = max(1, int(max_fes / (2 * N + n_lobl + (p_m if acgm else 0))))
    t = 0
    idx = np.arange(N)
    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)
        if tt < 1 / 3:
            a = rng.integers(0, N, N); b = rng.integers(0, N, N)
            a = np.where(a == idx, (a + 1) % N, a)
            b = np.where(b == a, (b + 1) % N, b)
            Xn = X + (X[a] - X[b]) * rng.random((N, D))
        elif tt < 2 / 3:
            Xn = Xbest + np.exp(tt ** 4) * (rng.normal(0, 1, (N, D)) - 0.5) * (Xbest - X)
        else:
            Xn = Xbest + ((1 - tt) ** (2 * tt)) * X * (0.5 * levy(rng, (N, D), beta))
        X, F = greedy(X, F, Xn, rec.evaluate(Xn))

        use_c1 = rng.random(N) < 0.5
        C1 = Xbest + (1 - tt) ** 2 * (2 * rng.normal(0, 1, (N, D)) - 1) * X
        K = np.round(1 + rng.random((N, 1)))
        C2 = X + rng.random((N, D)) * (X[rng.integers(0, N, N)] - K * X)
        Xn = np.where(use_c1[:, None], C1, C2)
        X, F = greedy(X, F, Xn, rec.evaluate(Xn))
        j = int(np.argmin(F))
        if F[j] < fbest:
            Xbest, fbest = X[j].copy(), float(F[j])

        if n_lobl and rec.budget_left():
            k = lens_k(t, T, k_root, k_pow)
            centre = ((X.min(axis=0) + X.max(axis=0)) / 2.0 if adaptive_lens
                      else (lb + ub) / 2.0)
            worst = np.argsort(F)[-n_lobl:]
            Xr = centre + centre / k - X[worst] / k if not adaptive_lens else \
                centre + (centre - X[worst]) / k
            Fr = rec.evaluate(Xr)
            m = len(Fr)
            if m:
                sel = worst[:m]
                imp = Fr <= F[sel]
                X[sel[imp]] = np.clip(Xr[:m][imp], lb, ub)
                F[sel[imp]] = Fr[imp]

        if acgm and rec.budget_left() and rng.random() < p_m:
            lam2 = tt ** 2
            lam1 = 1.0 - lam2
            pert = lam1 * rng.standard_cauchy(D) + lam2 * rng.standard_normal(D)
            if additive_acgm:
                scale = np.maximum(X.std(axis=0), 1e-12)
                cand = Xbest + scale * pert
            else:
                cand = Xbest * (1.0 + pert)
            fm = rec.evaluate(cand)
            if len(fm) and fm[0] < fbest:
                Xbest, fbest = np.clip(cand, lb, ub), float(fm[0])
                w = int(np.argmax(F))
                X[w], F[w] = Xbest.copy(), fbest
        j = int(np.argmin(F))
        if F[j] < fbest:
            Xbest, fbest = X[j].copy(), float(F[j])
    return rec.finalize()


CONFIGS = {
    'SBOA':          dict(gpsi=False, lobl=False, acgm=False),
    'MSSBOA-printed': dict(adaptive_lens=False, additive_acgm=False),
    'MSSBOA-lensfix': dict(adaptive_lens=True, additive_acgm=False),
    'MSSBOA-acgmfix': dict(adaptive_lens=False, additive_acgm=True),
    'MSSBOA-both':    dict(adaptive_lens=True, additive_acgm=True),
}


def _task(args):
    cfg, fid, dim, r = args
    prob = cec2017_problem(fid, dim)
    seed = int(zlib.crc32(f'{cfg}|{fid}|{dim}|{r}'.encode()) % (2 ** 32))
    bf, _, _ = run(prob, 1000 * dim, POP, np.random.default_rng(seed),
                   **CONFIGS[cfg])
    return cfg, fid, dim, float(bf - 100 * fid)


def main(dims=(10, 30), workers=2):
    tasks = [(c, f, d, r) for d in dims for r in range(RUNS)
             for c in CONFIGS for f in CEC2017_IDS]
    out = {}
    t0 = time.time()
    with Pool(workers) as pool:
        for cfg, fid, dim, v in pool.imap_unordered(_task, tasks, chunksize=8):
            out.setdefault((cfg, fid, dim), []).append(v)
    names = list(CONFIGS)
    for dim in dims:
        R = np.zeros((len(CEC2017_IDS), len(names)))
        for i, fid in enumerate(CEC2017_IDS):
            R[i] = stats.rankdata([np.mean(out[(c, fid, dim)]) for c in names])
        print(f'\nD={dim}, {RUNS} runs, {len(CEC2017_IDS)} functions '
              f'({time.time() - t0:.0f}s)')
        for c, v in sorted(zip(names, R.mean(axis=0)), key=lambda x: x[1]):
            print(f'   {c:16s} {v:.3f}')
        print('   Wilcoxon vs SBOA (+/=/-):')
        for c in names[1:]:
            w = e = l = 0
            for fid in CEC2017_IDS:
                a, b = out[(c, fid, dim)], out[('SBOA', fid, dim)]
                p = stats.ranksums(a, b).pvalue
                if not np.isfinite(p) or p >= 0.05:
                    e += 1
                elif np.mean(a) < np.mean(b):
                    w += 1
                else:
                    l += 1
            print(f'      {c:16s} {w}/{e}/{l}')


if __name__ == '__main__':
    main()
