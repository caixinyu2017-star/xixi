"""Master experiment runner: regenerates every number in the paper.

All tables and figures of the revised manuscript come from this one script and
one implementation, so no two numbers in the paper can disagree.

Studies, in the order they are run (highest value first):

  main       Tables 6, 7 and A5-A8: MSSBOA, SBOA and nine comparison
             algorithms on CEC2017 in 10, 30, 50 and 100 dimensions.
  ablation   Tables 4, 5 and A1-A4 plus the 2^3 factorial: all eight
             combinations of GPSI / LOBL / ACGM.
  sens       Tables 2 and 3: the N_min and p_m grids.
  design     Tables 8, 9 and 10: colour-harmony palettes and graphic layouts.
  variants   MSSBOA against three SBOA variants, MS-TSA and I-CPA.
  extra      Extended parameter grids: N, beta, hunting-stage division and the
             lens k-schedule.
  scale      Layout scalability from 8 to 30 elements.
  weights    Sensitivity of the layout results to the weights of Eq. (22).

Every run is seeded from (study, tag, problem, dimension, run index), so the
CSVs are reproducible exactly.  Tasks are emitted in run-major order: an
interrupted study is a complete experiment with fewer repetitions rather than
a complete one for the first few algorithms only.
"""
import csv
import os
import sys
import time
import zlib
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
os.makedirs(RES, exist_ok=True)

from bench import cec2017_problem, CEC2017_IDS                    # noqa: E402
from algos_mssboa import mssboa, sboa, FACTORIAL, _run            # noqa: E402
from algos_compare import COMPARISON                              # noqa: E402
from algos_variants import VARIANTS                               # noqa: E402
from design_problems import (color_problem, layout_problem,        # noqa: E402
                             large_layout_problem, LAYOUT_PROBLEMS)

POP = 30
RUNS = 30
DIMS_FULL = [10, 30, 50, 100]
DIMS_SHORT = [10, 30]

# ---------------------------------------------------------------- algorithms
MAIN = {'MSSBOA': mssboa, 'SBOA': sboa}
MAIN.update(COMPARISON)
MAIN_ORDER = ['MSSBOA', 'SBOA', 'GWO', 'COA', 'SCA', 'SMA', 'RIME', 'QIO',
              'MRFO', 'GKSO', 'LSHADE']

VARIANT_ORDER = ['MSSBOA', 'SBOA', 'MISBOA', 'CGSBOA', 'LTSBOA',
                 'TSA', 'MS-TSA', 'CPA', 'I-CPA']

# ------------------------------------------------------------ parameter grids
NMIN_GRID = [round(0.1 * i, 1) for i in range(1, 10)]      # 0.1N .. 0.9N
PM_GRID = [round(0.1 * i, 1) for i in range(1, 11)]        # 0.1 .. 1.0

EXTRA_GRID = {}
for _n in (10, 20, 50, 80, 100):
    EXTRA_GRID[f'N={_n}'] = ('N', _n, {})
for _b in (1.1, 1.3, 1.5, 1.7, 1.9):
    EXTRA_GRID[f'beta={_b}'] = ('kw', POP, {'beta': _b})
for _lab, _s in (('stage=T/3,2T/3', (1 / 3, 2 / 3)),
                 ('stage=T/4,3T/4', (0.25, 0.75)),
                 ('stage=T/2,3T/4', (0.50, 0.75)),
                 ('stage=T/5,4T/5', (0.20, 0.80))):
    EXTRA_GRID[_lab] = ('kw', POP, {'stage': _s})
for _lab, _kw in (('k: nu=1/2,mu=10', {'k_root': 0.5, 'k_pow': 10.0}),
                  ('k: nu=1,mu=10', {'k_root': 1.0, 'k_pow': 10.0}),
                  ('k: nu=1/3,mu=10', {'k_root': 1 / 3, 'k_pow': 10.0}),
                  ('k: nu=1/2,mu=5', {'k_root': 0.5, 'k_pow': 5.0}),
                  ('k: nu=1/2,mu=20', {'k_root': 0.5, 'k_pow': 20.0}),
                  ('k=1 (plain OBL)', {'k_root': 0.5, 'k_pow': 0.0})):
    EXTRA_GRID[_lab] = ('kw', POP, _kw)

COLOR_K = [5, 7, 10]
SCALE_N = [8, 12, 20, 30]
WEIGHT_SETS = {
    'W0 (Ngo)':       dict(BM=0.30, OV=0.22, AL=0.18, SY=0.15, DEN=0.15),
    'W1 (equal)':     dict(BM=0.20, OV=0.20, AL=0.20, SY=0.20, DEN=0.20),
    'W2 (balance)':   dict(BM=0.45, OV=0.20, AL=0.15, SY=0.10, DEN=0.10),
    'W3 (overlap)':   dict(BM=0.20, OV=0.40, AL=0.15, SY=0.15, DEN=0.10),
    'W4 (structure)': dict(BM=0.20, OV=0.20, AL=0.30, SY=0.20, DEN=0.10),
}
WEIGHT_ALGOS = ['MSSBOA', 'SBOA', 'RIME', 'LSHADE']
SCALE_ALGOS = ['MSSBOA', 'SBOA', 'RIME', 'LSHADE', 'GWO', 'COA']
DESIGN_FES = 20000


def _seed(*parts):
    return int(zlib.crc32('|'.join(map(str, parts)).encode()) % (2 ** 32))


# -------------------------------------------------------------------- tasks
def _task(args):
    study, tag, prob_id, dim, run = args
    rng = np.random.default_rng(_seed(study, tag, prob_id, dim, run))

    if study in ('main', 'ablation', 'sens', 'variants', 'extra'):
        fid = int(prob_id[1:])
        prob = cec2017_problem(fid, dim)
        mf = 1000 * dim
        if study == 'main':
            bf, _, curve = MAIN[tag](prob, mf, POP, rng)
        elif study == 'ablation':
            g, l, a = FACTORIAL[tag]
            bf, _, curve = _run(prob, mf, POP, rng, g, l, a)
        elif study == 'variants':
            fn = {'MSSBOA': mssboa, 'SBOA': sboa}.get(tag) or VARIANTS[tag]
            bf, _, curve = fn(prob, mf, POP, rng)
        elif study == 'sens':
            kind, val = tag.split('=')
            kw = ({'rho_lobl': float(val)} if kind == 'Nmin'
                  else {'p_m': float(val)})
            bf, _, curve = _run(prob, mf, POP, rng, True, True, True, **kw)
        else:
            kind, npop, kw = EXTRA_GRID[tag]
            bf, _, curve = _run(prob, mf, npop, rng, True, True, True, **kw)
        return study, tag, prob_id, dim, run, float(bf - 100 * fid), curve

    if study == 'design_color':
        prob = color_problem(int(prob_id[1:]))
        bf, bx, curve = MAIN[tag](prob, DESIGN_FES, POP, rng)
        return study, tag, prob_id, 0, run, -float(bf), curve
    if study == 'design_layout':
        prob = layout_problem(prob_id)
        bf, bx, curve = MAIN[tag](prob, DESIGN_FES, POP, rng)
        return study, tag, prob_id, 0, run, -float(bf), curve
    if study == 'scale':
        n = int(prob_id[1:])
        prob = large_layout_problem(n)
        bf, bx, curve = MAIN[tag](prob, 1000 * prob.dim, POP, rng)
        return study, tag, prob_id, 2 * n, run, -float(bf), curve
    if study == 'weights':
        wname, code = prob_id.split('|')
        prob = layout_problem(code, WEIGHT_SETS[wname])
        bf, bx, curve = MAIN[tag](prob, DESIGN_FES, POP, rng)
        return study, tag, prob_id, 0, run, -float(bf), curve
    raise ValueError(study)


def run_study(study, tasks, pool, curves_for=None):
    path = os.path.join(RES, f'r_{study}.csv')
    t0 = time.time()
    curves = {}
    with open(path, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['study', 'algo', 'problem', 'dim', 'run', 'value'])
        for i, res in enumerate(pool.imap_unordered(_task, tasks, chunksize=4), 1):
            st, tag, pid, dim, run, val, curve = res
            wr.writerow([st, tag, pid, dim, run, f'{val:.10e}'])
            if curves_for and dim in curves_for and run == 0:
                curves[f'{tag}|{pid}|{dim}'] = curve.astype(np.float32)
            if i % 1000 == 0:
                fh.flush()
                el = time.time() - t0
                print(f'  {study}: {i}/{len(tasks)} {el:.0f}s '
                      f'(eta {el / i * (len(tasks) - i):.0f}s)', flush=True)
    if curves:
        np.savez_compressed(os.path.join(RES, f'curves_{study}.npz'), **curves)
    print(f'{study} DONE: {len(tasks)} runs in {time.time() - t0:.0f}s', flush=True)


# ------------------------------------------------------------------ builders
def tasks_cec(study, tags, dims, runs=RUNS):
    return [(study, t, f'F{f}', d, r)
            for d in dims for r in range(runs) for t in tags for f in CEC2017_IDS]


STUDIES = {
    'main': lambda: ('main', tasks_cec('main', MAIN_ORDER, DIMS_FULL), [30]),
    'ablation': lambda: ('ablation', tasks_cec('ablation', list(FACTORIAL), DIMS_FULL), None),
    'sens': lambda: ('sens', tasks_cec(
        'sens', [f'Nmin={v}' for v in NMIN_GRID] + [f'pm={v}' for v in PM_GRID],
        DIMS_SHORT), None),
    'variants': lambda: ('variants', tasks_cec('variants', VARIANT_ORDER, DIMS_SHORT), None),
    'extra': lambda: ('extra', tasks_cec('extra', list(EXTRA_GRID), DIMS_SHORT), None),
    'design_color': lambda: ('design_color', [
        ('design_color', t, f'K{k}', 0, r)
        for r in range(RUNS) for t in MAIN_ORDER for k in COLOR_K], [0]),
    'design_layout': lambda: ('design_layout', [
        ('design_layout', t, c, 0, r)
        for r in range(RUNS) for t in MAIN_ORDER for c in LAYOUT_PROBLEMS], [0]),
    'scale': lambda: ('scale', [
        ('scale', t, f'N{n}', 2 * n, r)
        for r in range(RUNS) for t in SCALE_ALGOS for n in SCALE_N], None),
    'weights': lambda: ('weights', [
        ('weights', t, f'{w}|{c}', 0, r)
        for r in range(20) for t in WEIGHT_ALGOS
        for w in WEIGHT_SETS for c in LAYOUT_PROBLEMS], None),
}

ORDER = ['main', 'ablation', 'sens', 'design_color', 'design_layout',
         'variants', 'extra', 'scale', 'weights']


def main(argv):
    workers = 4
    if '--workers' in argv:
        i = argv.index('--workers')
        workers, argv = int(argv[i + 1]), argv[:i] + argv[i + 2:]
    todo = argv or ORDER
    with Pool(workers) as pool:
        for name in todo:
            study, tasks, curves_for = STUDIES[name]()
            print(f'=== {name}: {len(tasks)} runs ===', flush=True)
            run_study(study, tasks, pool, curves_for)


if __name__ == '__main__':
    main(sys.argv[1:])
