"""CEC2017 experiment runner for the revision.

Three studies, written to results/ as they finish so partial output is usable:

  variants   MSSBOA vs. three recent SBOA variants (Reviewer 2, comment 3) and
             vs. MS-TSA / I-CPA (Reviewer 3, comment 3), with their own base
             algorithms (TSA, CPA) included so that each variant's gain over
             its own base is visible.
  factorial  2^3 full-factorial ablation of GPSI / LOBL / ACGM, which supports
             the synergy analysis requested by Reviewer 3 (comments 1-2).
  params     extended parameter sensitivity: population size N, LOBL
             subpopulation ratio, Levy beta, hunting-stage time division and
             the lens k-schedule (Reviewer 1, comments 2 and 5).

Usage:  python3 run_cec.py <study> [study ...]
"""
import csv
import os
import sys
import time
import zlib
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
os.makedirs(RESULTS, exist_ok=True)

RUNS = 30
POP = 30

# The two headline studies keep the 30 independent runs used throughout the
# paper; the supplementary parameter grid uses 20, which is stated in the text.
RUNS_BY_STUDY = {'variants': 30, 'factorial': 30, 'params': 20}

from bench import cec2017_problem, CEC2017_IDS          # noqa: E402
from algos_mssboa import mssboa, sboa, FACTORIAL, _run  # noqa: E402
from algos_variants import VARIANTS                     # noqa: E402


# --------------------------------------------------------------- study specs
VARIANT_ALGOS = {
    'MSSBOA': lambda p, mf, N, r: mssboa(p, mf, N, r),
    'SBOA': lambda p, mf, N, r: sboa(p, mf, N, r),
    'MISBOA': VARIANTS['MISBOA'],
    'CGSBOA': VARIANTS['CGSBOA'],
    'LTSBOA': VARIANTS['LTSBOA'],
    'TSA': VARIANTS['TSA'],
    'MS-TSA': VARIANTS['MS-TSA'],
    'CPA': VARIANTS['CPA'],
    'I-CPA': VARIANTS['I-CPA'],
}

# Parameter grids.  'MSSBOA' (the default configuration) is run once and reused
# as the reference column of every grid.
PARAM_GRID = {}
for _n in (20, 50, 100):
    PARAM_GRID[f'N={_n}'] = ('N', _n, {})
for _r in (0.1, 0.3, 0.5):
    PARAM_GRID[f'rho={_r}'] = ('kw', POP, {'rho_lobl': _r})
for _b in (1.1, 1.3, 1.7, 1.9):
    PARAM_GRID[f'beta={_b}'] = ('kw', POP, {'beta': _b})
for _lab, _s in (('stage=1/4,3/4', (0.25, 0.75)),
                 ('stage=1/2,3/4', (0.50, 0.75)),
                 ('stage=1/5,4/5', (0.20, 0.80))):
    PARAM_GRID[_lab] = ('kw', POP, {'stage': _s})
for _lab, _kw in (('k: nu=1,mu=10', {'k_root': 1.0, 'k_pow': 10.0}),
                  ('k: nu=1/3,mu=10', {'k_root': 1 / 3, 'k_pow': 10.0}),
                  ('k: nu=1/2,mu=5', {'k_root': 0.5, 'k_pow': 5.0}),
                  ('k: nu=1/2,mu=20', {'k_root': 0.5, 'k_pow': 20.0}),
                  ('k=1 (plain OBL)', {'k_root': 0.5, 'k_pow': 0.0})):
    PARAM_GRID[_lab] = ('kw', POP, _kw)


def _seed(tag, fid, dim, run):
    return int((zlib.crc32(tag.encode()) % 100003) * 7919
               + run * 4013 + fid * 131 + dim * 17) % (2 ** 32)


def _task(args):
    study, tag, fid, dim, run = args
    prob = cec2017_problem(fid, dim)
    rng = np.random.default_rng(_seed(tag, fid, dim, run))
    max_fes = 1000 * dim
    if study == 'variants':
        bf, _, _ = VARIANT_ALGOS[tag](prob, max_fes, POP, rng)
    elif study == 'factorial':
        g, l, a = FACTORIAL[tag]
        bf, _, _ = _run(prob, max_fes, POP, rng, g, l, a)
    else:
        kind, npop, kw = PARAM_GRID[tag] if tag != 'MSSBOA' else ('N', POP, {})
        bf, _, _ = _run(prob, max_fes, npop, rng, True, True, True, **kw)
    return study, tag, fid, dim, run, float(bf - 100 * fid)


def run_study(study, tags, dims, pool):
    path = os.path.join(RESULTS, f'cec_{study}.csv')
    runs = RUNS_BY_STUDY.get(study, RUNS)
    tasks = [(study, t, f, d, r)
             for d in dims for t in tags for f in CEC2017_IDS for r in range(runs)]
    t0 = time.time()
    done = 0
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['study', 'algo', 'func', 'dim', 'run', 'error'])
        for res in pool.imap_unordered(_task, tasks, chunksize=4):
            wr.writerow([res[0], res[1], f'F{res[2]}', res[3], res[4], f'{res[5]:.10e}'])
            done += 1
            if done % 500 == 0:
                fh.flush()
                el = time.time() - t0
                print(f'  {study}: {done}/{len(tasks)}  {el:.0f}s '
                      f'(eta {el / done * (len(tasks) - done):.0f}s)', flush=True)
    print(f'{study} done: {len(tasks)} runs in {time.time() - t0:.0f}s', flush=True)


STUDY_SPEC = {
    'variants': (lambda: list(VARIANT_ALGOS), [10, 30]),
    'factorial': (lambda: list(FACTORIAL), [10]),
    'params': (lambda: ['MSSBOA'] + list(PARAM_GRID), [10]),
}


def main(studies, workers=4):
    """studies may be given as "name" or "name@10,30" to override dimensions."""
    with Pool(workers) as pool:
        for spec in studies:                       # honour the requested order
            study, _, dimspec = spec.partition('@')
            tags, dims = STUDY_SPEC[study]
            if dimspec:
                dims = [int(x) for x in dimspec.split(',')]
            run_study(study, tags(), dims, pool)


if __name__ == '__main__':
    main(sys.argv[1:] or ['variants', 'factorial', 'params'])
