"""Turn the raw experiment CSVs into the tables inserted in the revision.

Every table is returned as a list of rows (list of strings) so that
build_revision.py can drop it straight into the manuscript, and is also
written to results/table_*.csv for the record.
"""
import collections
import csv
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')

from bench import FUNCTION_CLASS, CLASS_ORDER            # noqa: E402


# --------------------------------------------------------------- utilities
def load(study):
    path = os.path.join(RES, f'cec_{study}.csv')
    if not os.path.exists(path):
        return None
    d = collections.defaultdict(list)
    with open(path, newline='') as fh:
        for r in csv.DictReader(fh):
            d[(r['algo'], int(r['dim']), r['func'])].append(float(r['error']))
    return d


def complete(d, algos, dim, min_runs=30):
    """Functions for which every algorithm has at least `min_runs` runs."""
    funcs = sorted({k[2] for k in d if k[1] == dim},
                   key=lambda f: int(f[1:]))
    return [f for f in funcs
            if all(len(d[(a, dim, f)]) >= min_runs for a in algos)]


def friedman(d, algos, dim, funcs):
    """Mean Friedman rank per algorithm plus the test p-value."""
    R = np.zeros((len(funcs), len(algos)))
    for i, f in enumerate(funcs):
        R[i] = stats.rankdata([np.mean(d[(a, dim, f)]) for a in algos])
    try:
        p = stats.friedmanchisquare(
            *[[np.mean(d[(a, dim, f)]) for f in funcs] for a in algos]).pvalue
    except Exception:
        p = float('nan')
    return R.mean(axis=0), p


def wilcoxon_counts(d, ref, other, dim, funcs, alpha=0.05):
    """(+, =, -) of `ref` against `other` over `funcs`."""
    w = e = l = 0
    for f in funcs:
        a, b = d[(ref, dim, f)], d[(other, dim, f)]
        try:
            p = stats.ranksums(a, b).pvalue
        except Exception:
            p = 1.0
        if p >= alpha or not np.isfinite(p):
            e += 1
        elif np.mean(a) < np.mean(b):
            w += 1
        else:
            l += 1
    return w, e, l


def _save(name, rows):
    with open(os.path.join(RES, f'table_{name}.csv'), 'w', newline='') as fh:
        csv.writer(fh).writerows(rows)
    return rows


# ------------------------------------------- Table: SBOA variants / MS-TSA
VARIANT_ORDER = ['MSSBOA', 'MISBOA', 'CGSBOA', 'LTSBOA', 'MS-TSA', 'I-CPA',
                 'SBOA', 'TSA', 'CPA']


def table_variants(min_runs=30):
    d = load('variants')
    if d is None:
        return None
    dims = sorted({k[1] for k in d})
    algos = [a for a in VARIANT_ORDER if any(k[0] == a for k in d)]
    rows = [['Algorithm'] + [f'{dm}D rank' for dm in dims]
            + ['Average rank', 'Overall rank']
            + [f'MSSBOA vs. ({dm}D, +/=/-)' for dm in dims]]
    ranks = {}
    pvals = {}
    for dm in dims:
        funcs = complete(d, algos, dm, min_runs)
        if not funcs:
            continue
        r, p = friedman(d, algos, dm, funcs)
        ranks[dm] = dict(zip(algos, r))
        pvals[dm] = p
    if not ranks:
        return None
    used = sorted(ranks)
    avg = {a: float(np.mean([ranks[dm][a] for dm in used])) for a in algos}
    order = {a: i + 1 for i, a in enumerate(sorted(algos, key=lambda x: avg[x]))}
    for a in algos:
        row = [a] + [f'{ranks[dm][a]:.3f}' for dm in used]
        row += [f'{avg[a]:.3f}', str(order[a])]
        for dm in used:
            if a == 'MSSBOA':
                row.append('-')
            else:
                w, e, l = wilcoxon_counts(d, 'MSSBOA', a, dm,
                                          complete(d, algos, dm, min_runs))
                row.append(f'{w}/{e}/{l}')
        rows.append(row)
    rows.append(['Friedman p-value'] + [f'{pvals[dm]:.3E}' for dm in used]
                + ['N/A', 'N/A'] + ['N/A'] * len(used))
    meta = {'funcs': {dm: len(complete(d, algos, dm, min_runs)) for dm in used},
            'dims': used}
    return _save('variants', rows), meta


# --------------------------------------------- Table: full-factorial ablation
def table_factorial(min_runs=30):
    d = load('factorial')
    if d is None:
        return None
    names = ['SBOA', 'SBOA-GPSI', 'SBOA-LOBL', 'SBOA-ACGM', 'SBOA-GPSI-LOBL',
             'SBOA-GPSI-ACGM', 'SBOA-LOBL-ACGM', 'MSSBOA']
    names = [n for n in names if any(k[0] == n for k in d)]
    dims = sorted({k[1] for k in d})
    dm = dims[0]
    funcs = complete(d, names, dm, min_runs)
    if not funcs:
        return None
    r, p = friedman(d, names, dm, funcs)
    rank = dict(zip(names, r))
    order = {a: i + 1 for i, a in enumerate(sorted(names, key=lambda x: rank[x]))}
    rows = [['Configuration', 'GPSI', 'LOBL', 'ACGM',
             f'Friedman rank (D={dm})', 'Rank', 'vs. SBOA (+/=/-)']]
    flags = {'SBOA': ('No', 'No', 'No'), 'SBOA-GPSI': ('Yes', 'No', 'No'),
             'SBOA-LOBL': ('No', 'Yes', 'No'), 'SBOA-ACGM': ('No', 'No', 'Yes'),
             'SBOA-GPSI-LOBL': ('Yes', 'Yes', 'No'),
             'SBOA-GPSI-ACGM': ('Yes', 'No', 'Yes'),
             'SBOA-LOBL-ACGM': ('No', 'Yes', 'Yes'),
             'MSSBOA': ('Yes', 'Yes', 'Yes')}
    for n in names:
        g, l_, a_ = flags[n]
        w, e, l = wilcoxon_counts(d, n, 'SBOA', dm, funcs)
        rows.append([n, g, l_, a_, f'{rank[n]:.3f}', str(order[n]),
                     '-' if n == 'SBOA' else f'{w}/{e}/{l}'])
    rows.append(['Friedman p-value', '', '', '', f'{p:.3E}', 'N/A', 'N/A'])

    # main effects and the three-way interaction on the mean Friedman rank
    def rk(g, l_, a_):
        for n, fl in flags.items():
            if fl == ('Yes' if g else 'No', 'Yes' if l_ else 'No',
                      'Yes' if a_ else 'No') and n in rank:
                return rank[n]
        return float('nan')

    eff = {
        'GPSI': np.mean([rk(1, l_, a_) - rk(0, l_, a_)
                         for l_ in (0, 1) for a_ in (0, 1)]),
        'LOBL': np.mean([rk(g, 1, a_) - rk(g, 0, a_)
                         for g in (0, 1) for a_ in (0, 1)]),
        'ACGM': np.mean([rk(g, l_, 1) - rk(g, l_, 0)
                         for g in (0, 1) for l_ in (0, 1)]),
    }
    inter = (rk(1, 1, 1) - rk(1, 1, 0) - rk(1, 0, 1) - rk(0, 1, 1)
             + rk(1, 0, 0) + rk(0, 1, 0) + rk(0, 0, 1) - rk(0, 0, 0))
    meta = {'dim': dm, 'nfuncs': len(funcs), 'effects': eff,
            'interaction': float(inter), 'rank': rank}
    return _save('factorial', rows), meta


# ------------------------------------------------ Table: parameter grids
GROUPS = [
    ('Population size N', 'N=', 'N = 30 (adopted)'),
    ('LOBL subpopulation ratio', 'rho=', 'rho = 0.2 (adopted)'),
    ('Levy stability index beta', 'beta=', 'beta = 1.5 (adopted)'),
    ('Hunting-stage time division', 'stage=', 'T/3, 2T/3 (adopted)'),
    ('Lens scaling schedule k(t)', 'k', 'nu = 1/2, mu = 10 (adopted)'),
]


def table_params(min_runs=30):
    d = load('params')
    if d is None:
        return None
    dm = sorted({k[1] for k in d})[0]
    out = []
    for title, prefix, default_label in GROUPS:
        tags = ['MSSBOA'] + sorted(a for a in {k[0] for k in d}
                                   if a.startswith(prefix))
        if len(tags) < 2:
            continue
        funcs = complete(d, tags, dm, min_runs)
        if not funcs:
            continue
        r, p = friedman(d, tags, dm, funcs)
        rows = [['Setting', f'Friedman rank (CEC2017, D={dm})', 'Rank',
                 'vs. adopted setting (+/=/-)']]
        order = {t: i + 1 for i, t in enumerate(sorted(tags, key=lambda x: dict(zip(tags, r))[x]))}
        rk = dict(zip(tags, r))
        for t in tags:
            lab = default_label if t == 'MSSBOA' else t
            if t == 'MSSBOA':
                cmp_ = '-'
            else:
                w, e, l = wilcoxon_counts(d, 'MSSBOA', t, dm, funcs)
                cmp_ = f'{w}/{e}/{l}'
            rows.append([lab, f'{rk[t]:.3f}', str(order[t]), cmp_])
        rows.append(['Friedman p-value', f'{p:.3E}', 'N/A', 'N/A'])
        out.append((title, _save('param_' + prefix.strip('=') or 'k', rows),
                    {'dim': dm, 'nfuncs': len(funcs)}))
    return out


# ------------------------------------------------ Table: design experiments
def table_weights(min_runs=15):
    path = os.path.join(RES, 'design_weights.csv')
    if not os.path.exists(path):
        return None
    d = collections.defaultdict(list)
    with open(path, newline='') as fh:
        for r in csv.DictReader(fh):
            d[(r['weights'], r['problem'], r['algo'])].append(float(r['score']))
    wsets = sorted({k[0] for k in d})
    probs = sorted({k[1] for k in d})
    algos = ['MSSBOA', 'SBOA', 'RIME', 'LSHADE']
    algos = [a for a in algos if any(k[2] == a for k in d)]
    rows = [['Weight configuration'] + [f'{a} (mean x100)' for a in algos]
            + ['Best algorithm', "Kendall tau vs. W0"]]
    base_rank = None
    for w in wsets:
        good = [p for p in probs
                if all(len(d[(w, p, a)]) >= min_runs for a in algos)]
        if not good:
            continue
        means = {a: np.mean([np.mean(d[(w, p, a)]) for p in good]) for a in algos}
        rk = stats.rankdata([-means[a] for a in algos])
        if base_rank is None:
            base_rank, tau = rk, 1.0
        else:
            tau = stats.kendalltau(base_rank, rk).statistic
        best = algos[int(np.argmax([means[a] for a in algos]))]
        rows.append([w] + [f'{means[a] * 100:.2f}' for a in algos]
                    + [best, f'{tau:.3f}'])
    return _save('weights', rows), {'nprob': len(probs)}


def table_scale(min_runs=20):
    path = os.path.join(RES, 'design_scale.csv')
    if not os.path.exists(path):
        return None
    d = collections.defaultdict(list)
    with open(path, newline='') as fh:
        for r in csv.DictReader(fh):
            d[(int(r['n_elements']), r['algo'])].append(float(r['score']))
    ns = sorted({k[0] for k in d})
    algos = ['MSSBOA', 'SBOA', 'RIME', 'LSHADE', 'GWO', 'COA']
    algos = [a for a in algos if any(k[1] == a for k in d)]
    ns = [n for n in ns if all(len(d[(n, a)]) >= min_runs for a in algos)]
    if not ns:
        return None
    rows = [['Elements n (D = 2n)'] + algos + ['MSSBOA rank']]
    for n in ns:
        means = [np.mean(d[(n, a)]) * 100 for a in algos]
        rk = stats.rankdata([-m for m in means])
        rows.append([f'{n} (D = {2 * n})'] + [f'{m:.2f}' for m in means]
                    + [str(int(rk[algos.index("MSSBOA")]))])
    rows.append(['Std. dev. of MSSBOA']
                + [f'{np.std(d[(n, "MSSBOA")]) * 100:.2f}' if a == 'MSSBOA'
                   else '' for a in algos][:len(algos)] + [''])
    return _save('scale', rows), {'ns': ns}


if __name__ == '__main__':
    for name, fn in (('variants', table_variants), ('factorial', table_factorial),
                     ('weights', table_weights), ('scale', table_scale)):
        r = fn()
        print(f'--- {name} ---')
        if r is None:
            print('  (no data yet)')
            continue
        rows = r[0]
        for row in rows:
            print('   ' + ' | '.join(str(c) for c in row))
        print('   meta:', r[1])
    p = table_params()
    if p:
        for title, rows, meta in p:
            print(f'--- {title} ---')
            for row in rows:
                print('   ' + ' | '.join(str(c) for c in row))
