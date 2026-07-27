"""Design-application experiments added during revision.

weights   Sensitivity of the layout results to the aesthetic weight vector of
          Eq. (22) (Reviewer 1, comment 6).  Five weight configurations are
          applied to all eight design problems; the question is whether the
          ranking of the algorithms - not just the absolute score - survives a
          change of weights.

scale     Scalability of the layout problem to 8, 12, 20 and 30 elements,
          i.e. up to D = 60 (Reviewer 1, comment 12).

palette   One long MSSBOA run per palette size, used to draw the hue-wheel /
          harmonic-template figure.

Usage:  python3 run_design.py <study> [study ...] [--workers K]
"""
import csv
import json
import os
import sys
import time
import zlib
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
os.makedirs(RESULTS, exist_ok=True)

from design_problems import (layout_problem, large_layout_problem,          # noqa: E402
                             color_problem, palette_score, LAYOUT_PROBLEMS,
                             W_LAYOUT, disharmony)
from algos_mssboa import mssboa, sboa                                        # noqa: E402
from algos_classic import gwo, sca, coa, rime, lshade                        # noqa: E402

ALGOS = {'MSSBOA': mssboa, 'SBOA': sboa, 'RIME': rime, 'LSHADE': lshade,
         'GWO': gwo, 'COA': coa, 'SCA': sca}

# Five weight configurations.  W0 is the Ngo-based setting used in the paper.
WEIGHT_SETS = {
    'W0 (paper)':     dict(BM=0.30, OV=0.22, AL=0.18, SY=0.15, DEN=0.15),
    'W1 (equal)':     dict(BM=0.20, OV=0.20, AL=0.20, SY=0.20, DEN=0.20),
    'W2 (balance)':   dict(BM=0.45, OV=0.20, AL=0.15, SY=0.10, DEN=0.10),
    'W3 (overlap)':   dict(BM=0.20, OV=0.40, AL=0.15, SY=0.15, DEN=0.10),
    'W4 (structure)': dict(BM=0.20, OV=0.20, AL=0.30, SY=0.20, DEN=0.10),
}

WEIGHT_ALGOS = ['MSSBOA', 'SBOA', 'RIME', 'LSHADE']
SCALE_ALGOS = ['MSSBOA', 'SBOA', 'RIME', 'LSHADE', 'GWO', 'COA']
SCALE_N = [8, 12, 20, 30]
RUNS_W, RUNS_S = 15, 20
POP = 30


def _seed(*parts):
    s = '|'.join(map(str, parts))
    return int(zlib.crc32(s.encode()) % (2 ** 32))


def _w_task(args):
    wname, code, algo, run = args
    prob = layout_problem(code, WEIGHT_SETS[wname])
    rng = np.random.default_rng(_seed('w', wname, code, algo, run))
    bf, _, _ = ALGOS[algo](prob, 10000, POP, rng)
    return wname, code, algo, run, -float(bf)


def _s_task(args):
    n, algo, run = args
    prob = large_layout_problem(n)
    rng = np.random.default_rng(_seed('s', n, algo, run))
    bf, bx, curve = ALGOS[algo](prob, 1000 * prob.dim, POP, rng)
    return n, algo, run, -float(bf), bx.tolist()


def study_weights(pool):
    tasks = [(w, c, a, r) for w in WEIGHT_SETS for c in LAYOUT_PROBLEMS
             for a in WEIGHT_ALGOS for r in range(RUNS_W)]
    t0 = time.time()
    with open(f'{RESULTS}/design_weights.csv', 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['weights', 'problem', 'algo', 'run', 'score'])
        for i, res in enumerate(pool.imap_unordered(_w_task, tasks, chunksize=4), 1):
            wr.writerow([res[0], res[1], res[2], res[3], f'{res[4]:.8f}'])
            if i % 200 == 0:
                fh.flush()
                print(f'  weights {i}/{len(tasks)} {time.time() - t0:.0f}s', flush=True)
    print(f'weights done {time.time() - t0:.0f}s', flush=True)


def study_scale(pool):
    tasks = [(n, a, r) for n in SCALE_N for a in SCALE_ALGOS for r in range(RUNS_S)]
    t0 = time.time()
    best = {}
    with open(f'{RESULTS}/design_scale.csv', 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['n_elements', 'dim', 'algo', 'run', 'score'])
        for i, res in enumerate(pool.imap_unordered(_s_task, tasks, chunksize=2), 1):
            n, algo, run, sc, bx = res
            wr.writerow([n, 2 * n, algo, run, f'{sc:.8f}'])
            key = f'{algo}|{n}'
            if key not in best or sc > best[key][0]:
                best[key] = (sc, bx)
            if i % 50 == 0:
                fh.flush()
                print(f'  scale {i}/{len(tasks)} {time.time() - t0:.0f}s', flush=True)
    json.dump({k: {'score': v[0], 'x': v[1]} for k, v in best.items()},
              open(f'{RESULTS}/design_scale_best.json', 'w'))
    print(f'scale done {time.time() - t0:.0f}s', flush=True)


def study_palette(pool=None):
    out = {}
    for K in (5, 7, 10):
        prob = color_problem(K)
        rng = np.random.default_rng(_seed('pal', K))
        bf, bx, _ = mssboa(prob, 20000, POP, rng)
        p = np.asarray(bx).reshape(K, 3)
        e, key = disharmony(p[:, 0] % 360.0, np.clip(p[:, 1], 0, 1))
        out[K] = {'score': -float(bf), 'palette': p.tolist(),
                  'template': key[0], 'alpha': key[1]}
        print(f'  K={K} score={-bf:.4f} template={key[0]} alpha={key[1]:.1f}',
              flush=True)
    json.dump(out, open(f'{RESULTS}/design_palette.json', 'w'), indent=1)


def main(argv):
    workers = 2
    if '--workers' in argv:
        i = argv.index('--workers')
        workers = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    studies = argv or ['weights', 'scale', 'palette']
    if studies == ['palette']:
        study_palette()
        return
    with Pool(workers) as pool:
        for s in studies:
            if s == 'weights':
                study_weights(pool)
            elif s == 'scale':
                study_scale(pool)
            elif s == 'palette':
                study_palette(pool)


if __name__ == '__main__':
    main(sys.argv[1:])
