"""Run a single setting of the extended parameter grid and append it.

Adding one setting to EXTRA_GRID does not invalidate the settings already in
results/r_extra.csv: every run is seeded from (study, tag, problem, dimension,
run index), so the rows this script appends are bit-for-bit the rows a full
``run_all.py extra`` would produce for the same tag.  Re-running the whole
study to add one column would cost half an hour for nothing.

    python3 run_extra_tag.py 'N=30'
"""
import csv
import os
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')

from bench import CEC2017_IDS                                      # noqa: E402
from run_all import EXTRA_GRID, DIMS_SHORT, RUNS, _task            # noqa: E402


def main(tags, workers=4):
    path = os.path.join(RES, 'r_extra.csv')
    with open(path, newline='') as fh:
        have = {(r[1], r[2], r[3], r[4]) for r in csv.reader(fh)}

    tasks = [('extra', t, f'F{f}', d, r)
             for d in DIMS_SHORT for r in range(RUNS)
             for t in tags for f in CEC2017_IDS
             if (t, f'F{f}', str(d), str(r)) not in have]
    if not tasks:
        print('nothing to do: every run is already in r_extra.csv')
        return
    print(f'{len(tasks)} run(s) for {", ".join(tags)}', flush=True)
    with open(path, 'a', newline='') as fh, Pool(workers) as pool:
        wr = csv.writer(fh)
        for i, res in enumerate(pool.imap_unordered(_task, tasks, chunksize=4), 1):
            st, tag, pid, dim, run, val, _ = res
            wr.writerow([st, tag, pid, dim, run, f'{val:.10e}'])
            if i % 500 == 0:
                fh.flush()
                print(f'  {i}/{len(tasks)}', flush=True)
    print('appended', len(tasks), 'run(s) to r_extra.csv')


if __name__ == '__main__':
    args = sys.argv[1:] or [t for t in EXTRA_GRID]
    unknown = [t for t in args if t not in EXTRA_GRID]
    if unknown:
        raise SystemExit(f'not in EXTRA_GRID: {unknown}')
    main(args)
