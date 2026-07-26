"""Distribution of MSSBOA's losses over the CEC2017 function classes.

Reviewer 1 (comment 4) asks whether the 15 losses against QIO and LSHADE
concentrate on particular function types, and whether the performance gap
narrows as the dimension grows.  The analysis is derived directly from the
per-function ranks already published in Tables A5-A8 of the manuscript, so it
is consistent with the results the reviewer is reading: on a given function
MSSBOA is counted as *losing* to a competitor when the competitor's published
rank on that function is better than MSSBOA's.

Outputs
    results/loss_by_class.csv     losses per competitor x function class
    results/loss_by_dim.csv       losses and mean rank gap per dimension
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bench import FUNCTION_CLASS, CLASS_ORDER          # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'results', 'from_manuscript')
OUT = os.path.join(HERE, '..', 'results')

APPENDIX = {10: 'T37_Table_A5.csv', 30: 'T38_Table_A6.csv',
            50: 'T39_Table_A7.csv', 100: 'T40_Table_A8.csv'}


def read_ranks(path):
    """-> {func_id: {algo: rank}} and {func_id: {algo: mean}}"""
    with open(path, newline='') as fh:
        rows = list(csv.reader(fh))
    header = rows[0]
    algos = header[2:]
    ranks, means, cur = {}, {}, None
    for r in rows[1:]:
        if r[0].strip():
            cur = int(r[0].strip().lstrip('Ff'))
        if cur is None:
            continue
        idx = r[1].strip().lower()
        if idx == 'rank':
            ranks[cur] = {a: float(v) for a, v in zip(algos, r[2:]) if v.strip()}
        elif idx == 'mean':
            means[cur] = {a: float(v) for a, v in zip(algos, r[2:]) if v.strip()}
    return algos, ranks, means


def main():
    algos = None
    per_dim = {}
    for dim, fname in APPENDIX.items():
        algos, ranks, means = read_ranks(os.path.join(SRC, fname))
        per_dim[dim] = (ranks, means)

    competitors = [a for a in algos if a != 'MSSBOA']

    # ---- losses per competitor x function class (all dimensions pooled) ----
    tbl = {c: {k: 0 for k in CLASS_ORDER} for c in competitors}
    tot = {c: 0 for c in competitors}
    for dim, (ranks, _) in per_dim.items():
        for fid, rk in ranks.items():
            for c in competitors:
                if c in rk and rk[c] < rk['MSSBOA']:
                    tbl[c][FUNCTION_CLASS[fid]] += 1
                    tot[c] += 1
    with open(os.path.join(OUT, 'loss_by_class.csv'), 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['Competitor'] + CLASS_ORDER + ['Total'])
        for c in competitors:
            wr.writerow([c] + [tbl[c][k] for k in CLASS_ORDER] + [tot[c]])
        n_class = {k: 0 for k in CLASS_ORDER}
        for fid in FUNCTION_CLASS:
            n_class[FUNCTION_CLASS[fid]] += 4          # four dimensions
        wr.writerow(['Cases available'] + [n_class[k] for k in CLASS_ORDER]
                    + [sum(n_class.values())])

    # ---- losses and mean rank gap per dimension, for the three strongest ----
    focus = [c for c in ('QIO', 'LSHADE', 'RIME') if c in competitors]
    with open(os.path.join(OUT, 'loss_by_dim.csv'), 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['Competitor', 'Dim', 'Losses', 'Losses on hybrid',
                     'Losses on composition', 'Mean rank MSSBOA',
                     'Mean rank competitor', 'Rank gap'])
        for c in focus:
            for dim in sorted(per_dim):
                ranks, _ = per_dim[dim]
                loss = hyb = comp = 0
                rm = rc = 0.0
                for fid, rk in ranks.items():
                    rm += rk['MSSBOA']
                    rc += rk[c]
                    if rk[c] < rk['MSSBOA']:
                        loss += 1
                        if FUNCTION_CLASS[fid] == 'Hybrid':
                            hyb += 1
                        elif FUNCTION_CLASS[fid] == 'Composition':
                            comp += 1
                n = len(ranks)
                wr.writerow([c, dim, loss, hyb, comp, f'{rm / n:.3f}',
                             f'{rc / n:.3f}', f'{(rc - rm) / n:.3f}'])

    # ---- console summary ----
    print('Losses by function class (all four dimensions pooled, 116 cases):')
    print(f"{'':10s}" + ''.join(f'{k:>13s}' for k in CLASS_ORDER) + f"{'Total':>8s}")
    for c in competitors:
        print(f'{c:10s}' + ''.join(f'{tbl[c][k]:13d}' for k in CLASS_ORDER)
              + f'{tot[c]:8d}')
    print('\nPer-dimension detail for the strongest competitors:')
    for c in focus:
        for dim in sorted(per_dim):
            ranks, _ = per_dim[dim]
            loss = sum(1 for fid, rk in ranks.items() if rk[c] < rk['MSSBOA'])
            gap = sum(rk[c] - rk['MSSBOA'] for rk in ranks.values()) / len(ranks)
            print(f'  {c:7s} D={dim:<4d} losses={loss:2d}  mean rank gap={gap:6.3f}')


if __name__ == '__main__':
    main()
