"""Reproducibility diagnostic.

A faithful implementation of Eqs. (9)-(14) does not reproduce the MSSBOA-over-
SBOA margin reported in the manuscript.  Section 3.2 describes N_min as the
size of the inferior subpopulation that LOBL refracts, but Table 1 lists it
next to the population size in the form "N = 30, N_min = 0.2N", which is the
notation used for *linear population size reduction* (LPSR).  This script
tests both readings against the plain SBOA so that the discrepancy can be
attributed.

Configurations
    SBOA          basic algorithm
    MSSBOA        N_min = LOBL subpopulation ratio  (Section 3.2 reading)
    MSSBOA-free   same, but LOBL/ACGM evaluations are not charged to the
                  budget (tests whether a margin could come from FE accounting)
    SBOA+LPSR     linear population size reduction alone
    MSSBOA+LPSR   N_min = minimum population size   (Table 1 reading)
"""
import csv
import os
import sys
import time
import zlib
from multiprocessing import Pool

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')

from framework import Recorder, clipx, levy                 # noqa: E402
from bench import cec2017_problem, CEC2017_IDS              # noqa: E402
from algos_mssboa import (good_point_set, lens_k, lens_refract, acgm,
                          sboa, mssboa)                     # noqa: E402

RUNS = 12
POP = 30


def mssboa_lpsr(prob, max_fes, N0, rng, n_min_ratio=0.2, p_m=0.5,
                rho_lobl=0.2, lpsr=True, charge=True):
    """MSSBOA with optional linear population size reduction."""
    rec = Recorder(prob, max_fes)
    D, lb, ub = prob.dim, prob.lb, prob.ub
    N_min = max(4, int(round(n_min_ratio * N0)))
    X = good_point_set(N0, D, lb, ub)
    F = rec.eval_pop(X)
    gb = int(np.argmin(F))
    Xbest, fbest = X[gb].copy(), F[gb]
    n_lobl0 = int(np.ceil(rho_lobl * N0))
    per_iter = 2 * N0 + (n_lobl0 + p_m if charge else 0)
    T = max(1, int(max_fes / per_iter))
    t, N = 0, N0
    while rec.budget_left():
        t += 1
        tt = min(t / T, 1.0)
        if lpsr:
            N_new = max(N_min, int(round(N0 - (N0 - N_min) * tt)))
            if N_new < N:
                order = np.argsort(F)[:N_new]
                X, F, N = X[order], F[order], N_new
        for i in range(N):
            if not rec.budget_left():
                break
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
        n_lobl = int(np.ceil(rho_lobl * N))
        if n_lobl:
            k = lens_k(t, T)
            for i in np.argsort(F)[-n_lobl:]:
                if not rec.budget_left():
                    break
                nx = clipx(lens_refract(X[i], lb, ub, k), prob)
                f = rec.eval(nx)
                if f <= F[i]:
                    X[i], F[i] = nx, f
                    if f < fbest:
                        Xbest, fbest = nx.copy(), f
        if rec.budget_left() and p_m and rng.random() < p_m:
            nx = clipx(acgm(Xbest, t, T, rng), prob)
            f = rec.eval(nx)
            if f < fbest:
                Xbest, fbest = nx.copy(), f
                w = int(np.argmax(F))
                X[w], F[w] = nx.copy(), f
    return rec.finalize()


def sboa_lpsr(prob, max_fes, N0, rng):
    return mssboa_lpsr(prob, max_fes, N0, rng, p_m=0.0, rho_lobl=0.0, lpsr=True)


CONFIGS = {
    'SBOA': lambda p, mf, N, r: sboa(p, mf, N, r),
    'MSSBOA': lambda p, mf, N, r: mssboa(p, mf, N, r),
    'MSSBOA-free': lambda p, mf, N, r: mssboa_lpsr(p, mf, N, r, lpsr=False,
                                                   charge=False),
    'SBOA+LPSR': sboa_lpsr,
    'MSSBOA+LPSR': lambda p, mf, N, r: mssboa_lpsr(p, mf, N, r, lpsr=True),
}


def _task(args):
    cfg, fid, dim, run = args
    prob = cec2017_problem(fid, dim)
    seed = int(zlib.crc32(f'{cfg}|{fid}|{dim}|{run}'.encode()) % (2 ** 32))
    bf, _, _ = CONFIGS[cfg](prob, 1000 * dim, POP, np.random.default_rng(seed))
    return cfg, fid, dim, run, float(bf - 100 * fid)


def main(dim=10, workers=2):
    tasks = [(c, f, dim, r) for c in CONFIGS for f in CEC2017_IDS
             for r in range(RUNS)]
    out = {}
    t0 = time.time()
    with Pool(workers) as pool:
        for cfg, fid, d, run, err in pool.imap_unordered(_task, tasks, chunksize=4):
            out.setdefault((cfg, fid), []).append(err)
    with open(os.path.join(RES, f'diagnose_D{dim}.csv'), 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['config', 'func', 'run', 'error'])
        for (cfg, fid), v in sorted(out.items()):
            for i, e in enumerate(v):
                wr.writerow([cfg, f'F{fid}', i, f'{e:.10e}'])

    names = list(CONFIGS)
    R = np.zeros((len(CEC2017_IDS), len(names)))
    for i, fid in enumerate(CEC2017_IDS):
        R[i] = stats.rankdata([np.mean(out[(c, fid)]) for c in names])
    print(f'\nCEC2017 D={dim}, {RUNS} runs, {len(CEC2017_IDS)} functions '
          f'({time.time() - t0:.0f}s)')
    print('Friedman mean rank (lower is better):')
    for c, r in sorted(zip(names, R.mean(axis=0)), key=lambda x: x[1]):
        print(f'   {c:14s} {r:.3f}')
    print('\nWilcoxon rank-sum against plain SBOA (+/=/-):')
    for c in names:
        if c == 'SBOA':
            continue
        w = e = l = 0
        for fid in CEC2017_IDS:
            a, b = out[(c, fid)], out[('SBOA', fid)]
            p = stats.ranksums(a, b).pvalue
            if not np.isfinite(p) or p >= 0.05:
                e += 1
            elif np.mean(a) < np.mean(b):
                w += 1
            else:
                l += 1
        print(f'   {c:14s} {w}/{e}/{l}')


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10,
         int(sys.argv[2]) if len(sys.argv) > 2 else 2)
