"""Full CEC benchmark experiment runner (multiprocessing, resumable).

Usage:
  python3 run_cec.py --paper A          # CEC2017 10/30D, SBOA family
  python3 run_cec.py --paper B          # CEC2022 10/20D, BKA family
Writes results incrementally to ../results/<paper>_<suite>_<dim>.csv
and convergence curves to ../results/curves_<paper>_<suite>_<dim>.npz
"""
import argparse, csv, os, sys, time
import numpy as np
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
os.makedirs(RESULTS, exist_ok=True)

RUNS = 30
POP = 30


def get_algos(paper):
    from algos_classic import ALGOS as C
    if paper == 'A':
        from algos_sboa import sboa, mssboa, sboa_gps, sboa_egs, sboa_atp
        return {
            'MSSBOA': mssboa, 'SBOA': sboa,
            'SBOA-GPS': sboa_gps, 'SBOA-EGS': sboa_egs, 'SBOA-ATP': sboa_atp,
            'GWO': C['GWO'], 'WOA': C['WOA'], 'SCA': C['SCA'], 'PSO': C['PSO'],
            'HHO': C['HHO'], 'DBO': C['DBO'], 'RIME': C['RIME'], 'LSHADE': C['LSHADE'],
        }
    else:
        from algos_bka import bka, msbka, bka_s1, bka_s2, bka_s3
        return {
            'MSBKA': msbka, 'BKA': bka,
            'BKA-S1': bka_s1, 'BKA-S2': bka_s2, 'BKA-S3': bka_s3,
            'SSA': C['SSA'], 'COA': C['COA'], 'GWO': C['GWO'], 'SCA': C['SCA'],
            'PSO': C['PSO'], 'DE': C['DE'], 'HHO': C['HHO'], 'RIME': C['RIME'],
        }


def get_suite(paper, dim):
    from framework import Problem
    if paper == 'A':
        import opfunu.cec_based.cec2017 as mod
        names = [f'F{i}2017' for i in range(1, 30)]
        suite = 'cec2017'
    else:
        import opfunu.cec_based.cec2022 as mod
        names = [f'F{i}2022' for i in range(1, 13)]
        suite = 'cec2022'
    probs = []
    for nm in names:
        f = getattr(mod, nm)(ndim=dim)
        probs.append(Problem(f.evaluate, f.lb, f.ub, dim, nm))
    return suite, probs


def get_one_problem(paper, dim, fidx):
    from framework import Problem
    if paper == 'A':
        import opfunu.cec_based.cec2017 as mod
        nm = f'F{fidx + 1}2017'
    else:
        import opfunu.cec_based.cec2022 as mod
        nm = f'F{fidx + 1}2022'
    f = getattr(mod, nm)(ndim=dim)
    return Problem(f.evaluate, f.lb, f.ub, dim, nm)


def one_task(args):
    import zlib
    paper, dim, fidx, algo_name, run = args
    algos = get_algos(paper)
    prob = get_one_problem(paper, dim, fidx)
    max_fes = 1000 * dim
    seed = 7 + run * 100003 + fidx * 1009 + (zlib.crc32(algo_name.encode()) % 997) * 11
    rng = np.random.default_rng(seed)
    t0 = time.time()
    bf, bx, curve = algos[algo_name](prob, max_fes, POP, rng)
    return (paper, dim, fidx, prob.name, algo_name, run, bf, curve, time.time() - t0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--paper', required=True, choices=['A', 'B'])
    ap.add_argument('--dims', default=None)
    ap.add_argument('--procs', type=int, default=4)
    a = ap.parse_args()
    dims = [int(d) for d in a.dims.split(',')] if a.dims else ([10, 30] if a.paper == 'A' else [10, 20])
    algos = list(get_algos(a.paper).keys())
    for dim in dims:
        suite, probs = get_suite(a.paper, dim)
        csv_path = f'{RESULTS}/{a.paper}_{suite}_{dim}.csv'
        npz_path = f'{RESULTS}/curves_{a.paper}_{suite}_{dim}.npz'
        done = set()
        if os.path.exists(csv_path):
            with open(csv_path) as fh:
                for row in csv.reader(fh):
                    if row and row[0] != 'func':
                        done.add((row[0], row[1], int(row[2])))
        tasks = []
        for fidx, p in enumerate(probs):
            for alg in algos:
                for run in range(RUNS):
                    if (p.name, alg, run) not in done:
                        tasks.append((a.paper, dim, fidx, alg, run))
        print(f'[{suite} {dim}D] {len(tasks)} tasks remaining ({len(done)} done)', flush=True)
        if not tasks:
            continue
        curves = {}
        if os.path.exists(npz_path):
            curves = {k: v for k, v in np.load(npz_path).items()}
        new_file = not os.path.exists(csv_path)
        fh = open(csv_path, 'a', newline='')
        wr = csv.writer(fh)
        if new_file:
            wr.writerow(['func', 'algo', 'run', 'best_f', 'seconds'])
        t_start = time.time()
        with Pool(a.procs) as pool:
            for k, res in enumerate(pool.imap_unordered(one_task, tasks, chunksize=4)):
                _, _, fidx, fname, alg, run, bf, curve, secs = res
                wr.writerow([fname, alg, run, f'{bf:.10e}', f'{secs:.2f}'])
                curves[f'{fname}|{alg}|{run}'] = curve.astype(np.float32)
                if (k + 1) % 200 == 0:
                    fh.flush()
                    np.savez_compressed(npz_path, **curves)
                    el = time.time() - t_start
                    print(f'  {k+1}/{len(tasks)} done, {el/60:.1f} min elapsed, '
                          f'ETA {el/(k+1)*(len(tasks)-k-1)/60:.1f} min', flush=True)
        fh.close()
        np.savez_compressed(npz_path, **curves)
        print(f'[{suite} {dim}D] complete.', flush=True)


if __name__ == '__main__':
    main()
