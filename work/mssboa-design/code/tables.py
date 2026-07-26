"""Generate every table of the revised manuscript from the regenerated runs.

One implementation, one set of runs, one generator: no two numbers in the
paper can disagree because all of them come from ``results/r_*.csv``.

Tables produced
    T1   parameter settings                      (static, mirrors the code)
    T2   N_min grid                              from r_sens
    T3   p_m grid                                from r_sens
    T4   strategy map of the ablation            (static)
    T5   ablation Friedman rankings              from r_ablation
    T6   main Friedman rankings                  from r_main
    T7   Wilcoxon rank-sum summary               from r_main
    T8   colour-harmony scores                   from r_design_color
    T9   layout problem set                      (static)
    T10  layout aesthetic scores                 from r_design_layout
    A1-A4 ablation per-function statistics       from r_ablation
    A5-A8 main per-function statistics           from r_main
    new  factorial, variants, extra grids, loss distribution, weights, scale
"""
import collections
import csv
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')

from bench import FUNCTION_CLASS, CLASS_ORDER, CEC2017_IDS      # noqa: E402
from design_problems import LAYOUT_PROBLEMS                      # noqa: E402
from run_all import (MAIN_ORDER, VARIANT_ORDER, NMIN_GRID, PM_GRID,
                     EXTRA_GRID, COLOR_K, SCALE_N, WEIGHT_SETS,
                     WEIGHT_ALGOS, SCALE_ALGOS, POP, RUNS,
                     DIMS_FULL, DIMS_SHORT)                      # noqa: E402
from algos_mssboa import FACTORIAL                               # noqa: E402

ABL_MAIN = ['SBOA', 'SBOA-GPSI', 'SBOA-LOBL', 'SBOA-ACGM', 'MSSBOA']
ALPHA = 0.05


# ------------------------------------------------------------------ loading
def load(study):
    path = os.path.join(RES, f'r_{study}.csv')
    if not os.path.exists(path):
        return None
    d = collections.defaultdict(list)
    with open(path, newline='') as fh:
        for row in csv.DictReader(fh):
            d[(row['algo'], row['problem'], int(row['dim']))].append(
                float(row['value']))
    return d


def usable(d, algos, problems, dim, floor=5):
    n = min((len(d[(a, p, dim)]) for a in algos for p in problems), default=0)
    return n if n >= floor else 0


def _fr(d, algos, problems, dim, n):
    """Friedman mean rank per algorithm and the test p-value."""
    R = np.zeros((len(problems), len(algos)))
    cols = []
    for a in algos:
        cols.append([np.mean(d[(a, p, dim)][:n]) for p in problems])
    for i in range(len(problems)):
        R[i] = stats.rankdata([c[i] for c in cols])
    try:
        p = stats.friedmanchisquare(*cols).pvalue
    except Exception:
        p = float('nan')
    return R.mean(axis=0), p


def _wil(d, ref, other, problems, dim, n):
    w = e = l = 0
    for p in problems:
        a, b = d[(ref, p, dim)][:n], d[(other, p, dim)][:n]
        try:
            pv = stats.ranksums(a, b).pvalue
        except Exception:
            pv = 1.0
        if not np.isfinite(pv) or pv >= ALPHA:
            e += 1
        elif np.mean(a) < np.mean(b):
            w += 1
        else:
            l += 1
    return w, e, l


def _save(name, rows):
    with open(os.path.join(RES, f'T_{name}.csv'), 'w', newline='') as fh:
        csv.writer(fh).writerows(rows)
    return rows


def _fmt(v):
    return f'{v:.3E}'


# ============================================================ static tables
def t1_parameters():
    rows = [['Algorithm', 'Parameter settings'],
            ['MSSBOA', f'N = {POP}, N_min = 0.2N, p_m = 0.5, beta = 1.5, '
                       'k(t) = (1 + (t/T)^(1/2))^10'],
            ['SBOA', f'N = {POP}, beta = 1.5'],
            ['GWO', f'N = {POP}, a decreases linearly from 2 to 0'],
            ['COA', f'N = {POP}, temperature-driven control parameter'],
            ['SCA', f'N = {POP}, a = 2'],
            ['SMA', f'N = {POP}, z = 0.03'],
            ['RIME', f'N = {POP}, W = 5'],
            ['QIO', f'N = {POP}, no algorithm-specific parameter'],
            ['MRFO', f'N = {POP}, somersault factor S = 2'],
            ['GKSO', f'N = {POP}, inertia weight from 0.9 to 0.4'],
            ['LSHADE', 'N_init = 18D, N_min = 4, H = 6, p = 0.11, arc rate = 2.6']]
    return _save('t1', rows)


def t4_strategies():
    rows = [['Strategy'] + ABL_MAIN]
    for s, key in (('GPSI', 0), ('LOBL', 1), ('ACGM', 2)):
        rows.append([s] + ['Yes' if FACTORIAL[a][key] else 'No' for a in ABL_MAIN])
    return _save('t4', rows)


def t9_layout_problems():
    rows = [['Problem', 'Name', 'Elements n', 'Dimension D']]
    for code, (name, sizes) in LAYOUT_PROBLEMS.items():
        rows.append([code, name, str(len(sizes)), str(2 * len(sizes))])
    return _save('t9', rows)


# ======================================================= sensitivity grids
def _grid_table(d, tags, labels, dims, name):
    rows = [['Dimension'] + labels]
    per_dim = {}
    probs = [f'F{f}' for f in CEC2017_IDS]
    for dim in dims:
        n = usable(d, tags, probs, dim)
        if not n:
            continue
        rk, _ = _fr(d, tags, probs, dim, n)
        per_dim[dim] = rk
        rows.append([f'D = {dim}'] + [f'{v:.3f}' for v in rk])
    if not per_dim:
        return None
    avg = np.mean([per_dim[k] for k in per_dim], axis=0)
    rows.append(['Average'] + [f'{v:.3f}' for v in avg])
    best = labels[int(np.argmin(avg))]
    return _save(name, rows), {'best': best, 'avg': avg, 'labels': labels,
                               'dims': list(per_dim), 'n': n}


def t2_nmin():
    d = load('sens')
    if d is None:
        return None
    tags = [f'Nmin={v}' for v in NMIN_GRID]
    return _grid_table(d, tags, [f'{v}N' for v in NMIN_GRID], DIMS_SHORT, 't2')


def t3_pm():
    d = load('sens')
    if d is None:
        return None
    tags = [f'pm={v}' for v in PM_GRID]
    return _grid_table(d, tags, [str(v) for v in PM_GRID], DIMS_SHORT, 't3')


def t_extra():
    """Extended grids: N, beta, hunting-stage division, lens schedule."""
    d = load('extra')
    if d is None:
        return None
    groups = [('Population size N', 'N='),
              ('Levy stability index beta', 'beta='),
              ('Hunting-stage time division', 'stage='),
              ('Lens scaling schedule', 'k')]
    out = []
    for title, prefix in groups:
        tags = [t for t in EXTRA_GRID if t.startswith(prefix)]
        if not tags:
            continue
        res = _grid_table(d, tags, tags, DIMS_SHORT,
                          'extra_' + prefix.strip('=').replace('/', ''))
        if res:
            out.append((title, res[0], res[1]))
    return out


# =========================================================== ablation tables
def t5_ablation(algos=None, name='t5'):
    d = load('ablation')
    if d is None:
        return None
    algos = algos or ABL_MAIN
    probs = [f'F{f}' for f in CEC2017_IDS]
    rows = [['Test suite', 'Dim'] + algos + ['p-value']]
    per_dim = {}
    for dim in DIMS_FULL:
        n = usable(d, algos, probs, dim)
        if not n:
            continue
        rk, pv = _fr(d, algos, probs, dim, n)
        per_dim[dim] = rk
        rows.append(['CEC2017' if not per_dim or dim == min(per_dim) else '',
                     str(dim)] + [f'{v:.3f}' for v in rk] + [_fmt(pv)])
    if not per_dim:
        return None
    avg = np.mean([per_dim[k] for k in per_dim], axis=0)
    order = stats.rankdata(avg)
    rows.append(['Average ranking', ''] + [f'{v:.3f}' for v in avg] + ['N/A'])
    rows.append(['Ranking', ''] + [str(int(v)) for v in order] + ['N/A'])
    return _save(name, rows), {'avg': dict(zip(algos, avg)),
                               'dims': list(per_dim), 'n': n, 'algos': algos}


def t_factorial():
    """Full 2^3 design with main effects and the three-way interaction."""
    d = load('ablation')
    if d is None:
        return None
    names = list(FACTORIAL)
    probs = [f'F{f}' for f in CEC2017_IDS]
    dim = DIMS_FULL[1] if usable(d, names, probs, DIMS_FULL[1]) else DIMS_FULL[0]
    n = usable(d, names, probs, dim)
    if not n:
        return None
    rk, pv = _fr(d, names, probs, dim, n)
    rank = dict(zip(names, rk))
    order = {a: int(v) for a, v in zip(names, stats.rankdata(rk))}
    rows = [['Configuration', 'GPSI', 'LOBL', 'ACGM',
             f'Friedman rank (D = {dim})', 'Rank', 'vs. SBOA (+/=/-)']]
    for a in names:
        g, l, m = FACTORIAL[a]
        w, e, ls = _wil(d, a, 'SBOA', probs, dim, n)
        rows.append([a, 'Yes' if g else 'No', 'Yes' if l else 'No',
                     'Yes' if m else 'No', f'{rank[a]:.3f}', str(order[a]),
                     '-' if a == 'SBOA' else f'{w}/{e}/{ls}'])
    rows.append(['Friedman p-value', '', '', '', _fmt(pv), 'N/A', 'N/A'])

    def rk_of(g, l, m):
        for a, fl in FACTORIAL.items():
            if fl == (bool(g), bool(l), bool(m)):
                return rank[a]
        return np.nan

    eff = {
        'GPSI': float(np.mean([rk_of(1, l, m) - rk_of(0, l, m)
                               for l in (0, 1) for m in (0, 1)])),
        'LOBL': float(np.mean([rk_of(g, 1, m) - rk_of(g, 0, m)
                               for g in (0, 1) for m in (0, 1)])),
        'ACGM': float(np.mean([rk_of(g, l, 1) - rk_of(g, l, 0)
                               for g in (0, 1) for l in (0, 1)])),
    }
    inter = float(rk_of(1, 1, 1) - rk_of(1, 1, 0) - rk_of(1, 0, 1) - rk_of(0, 1, 1)
                  + rk_of(1, 0, 0) + rk_of(0, 1, 0) + rk_of(0, 0, 1) - rk_of(0, 0, 0))
    return _save('factorial', rows), {'dim': dim, 'n': n, 'effects': eff,
                                      'interaction': inter, 'rank': rank}


# =============================================================== main tables
def t6_friedman():
    d = load('main')
    if d is None:
        return None
    probs = [f'F{f}' for f in CEC2017_IDS]
    dims = [dm for dm in DIMS_FULL if usable(d, MAIN_ORDER, probs, dm)]
    if not dims:
        return None
    rows = [['Algorithm'] + [f'{dm}D' for dm in dims] + ['Average', 'Rank']]
    rk, pv = {}, {}
    for dm in dims:
        n = usable(d, MAIN_ORDER, probs, dm)
        r, p = _fr(d, MAIN_ORDER, probs, dm, n)
        rk[dm], pv[dm] = dict(zip(MAIN_ORDER, r)), p
    avg = {a: float(np.mean([rk[dm][a] for dm in dims])) for a in MAIN_ORDER}
    order = {a: i + 1 for i, a in enumerate(sorted(MAIN_ORDER, key=lambda x: avg[x]))}
    for a in MAIN_ORDER:
        rows.append([a] + [f'{rk[dm][a]:.3f}' for dm in dims]
                    + [f'{avg[a]:.3f}', str(order[a])])
    rows.append(['Friedman p-value'] + [_fmt(pv[dm]) for dm in dims]
                + ['N/A', 'N/A'])
    n = usable(d, MAIN_ORDER, probs, dims[0])
    return _save('t6', rows), {'rank': rk, 'avg': avg, 'order': order,
                               'dims': dims, 'n': n, 'p': pv}


def t7_wilcoxon():
    d = load('main')
    if d is None:
        return None
    probs = [f'F{f}' for f in CEC2017_IDS]
    dims = [dm for dm in DIMS_FULL if usable(d, MAIN_ORDER, probs, dm)]
    if not dims:
        return None
    rows = [['MSSBOA vs.'] + [f'{dm}D (+/=/-)' for dm in dims] + ['Total (+/=/-)']]
    detail = {}
    for a in MAIN_ORDER:
        if a == 'MSSBOA':
            continue
        tot = [0, 0, 0]
        row = [a]
        for dm in dims:
            n = usable(d, MAIN_ORDER, probs, dm)
            w, e, l = _wil(d, 'MSSBOA', a, probs, dm, n)
            row.append(f'{w}/{e}/{l}')
            tot = [tot[0] + w, tot[1] + e, tot[2] + l]
        row.append(f'{tot[0]}/{tot[1]}/{tot[2]}')
        rows.append(row)
        detail[a] = tot
    return _save('t7', rows), {'detail': detail, 'dims': dims,
                               'cases': len(probs) * len(dims)}


def t_loss_distribution():
    """Where MSSBOA loses, by CEC2017 function class."""
    d = load('main')
    if d is None:
        return None
    probs = [f'F{f}' for f in CEC2017_IDS]
    dims = [dm for dm in DIMS_FULL if usable(d, MAIN_ORDER, probs, dm)]
    if not dims:
        return None
    rows = [['Competitor'] + CLASS_ORDER + ['Total losses']]
    per = {}
    for a in MAIN_ORDER:
        if a == 'MSSBOA':
            continue
        cnt = {c: 0 for c in CLASS_ORDER}
        for dm in dims:
            n = usable(d, MAIN_ORDER, probs, dm)
            for p in probs:
                pv = stats.ranksums(d[('MSSBOA', p, dm)][:n],
                                    d[(a, p, dm)][:n]).pvalue
                if np.isfinite(pv) and pv < ALPHA and \
                        np.mean(d[('MSSBOA', p, dm)][:n]) > np.mean(d[(a, p, dm)][:n]):
                    cnt[FUNCTION_CLASS[int(p[1:])]] += 1
        per[a] = cnt
        rows.append([a] + [str(cnt[c]) for c in CLASS_ORDER]
                    + [str(sum(cnt.values()))])
    avail = {c: sum(1 for f in CEC2017_IDS if FUNCTION_CLASS[f] == c) * len(dims)
             for c in CLASS_ORDER}
    rows.append(['Cases available'] + [str(avail[c]) for c in CLASS_ORDER]
                + [str(sum(avail.values()))])
    return _save('loss', rows), {'per': per, 'avail': avail, 'dims': dims}


def t_dimension_gap():
    """Mean rank gap to the strongest competitors, per dimension."""
    d = load('main')
    t6 = t6_friedman()
    if d is None or t6 is None:
        return None
    _, meta = t6
    ranked = sorted((a for a in MAIN_ORDER if a != 'MSSBOA'),
                    key=lambda a: meta['avg'][a])[:3]
    rows = [['Dimension'] + [f'gap to {a}' for a in ranked]]
    for dm in meta['dims']:
        rows.append([f'D = {dm}']
                    + [f'{meta["rank"][dm][a] - meta["rank"][dm]["MSSBOA"]:+.3f}'
                       for a in ranked])
    return _save('gap', rows), {'top': ranked, 'dims': meta['dims'],
                                'rank': meta['rank']}


def appendix(study, algos, name_prefix):
    """Per-function best / mean / std / rank tables, one per dimension."""
    d = load(study)
    if d is None:
        return None
    probs = [f'F{f}' for f in CEC2017_IDS]
    out = []
    for dm in DIMS_FULL:
        n = usable(d, algos, probs, dm)
        if not n:
            continue
        rows = [['Func', 'Index'] + algos]
        for p in probs:
            means = [np.mean(d[(a, p, dm)][:n]) for a in algos]
            rk = stats.rankdata(means)
            rows.append([p, 'Best'] + [f'{np.min(d[(a, p, dm)][:n]):.3E}' for a in algos])
            rows.append(['', 'Mean'] + [f'{m:.3E}' for m in means])
            rows.append(['', 'Std'] + [f'{np.std(d[(a, p, dm)][:n]):.3E}' for a in algos])
            rows.append(['', 'Rank'] + [str(int(v)) for v in rk])
        out.append((dm, _save(f'{name_prefix}_D{dm}', rows), n))
    return out


# ============================================================ variant table
def t_variants():
    d = load('variants')
    if d is None:
        return None
    probs = [f'F{f}' for f in CEC2017_IDS]
    dims = [dm for dm in DIMS_SHORT if usable(d, VARIANT_ORDER, probs, dm)]
    if not dims:
        return None
    rows = [['Algorithm'] + [f'{dm}D rank' for dm in dims]
            + ['Average', 'Rank'] + [f'MSSBOA vs. ({dm}D)' for dm in dims]]
    rk = {}
    for dm in dims:
        n = usable(d, VARIANT_ORDER, probs, dm)
        r, _ = _fr(d, VARIANT_ORDER, probs, dm, n)
        rk[dm] = dict(zip(VARIANT_ORDER, r))
    avg = {a: float(np.mean([rk[dm][a] for dm in dims])) for a in VARIANT_ORDER}
    order = {a: i + 1 for i, a in enumerate(sorted(VARIANT_ORDER, key=lambda x: avg[x]))}
    for a in VARIANT_ORDER:
        row = [a] + [f'{rk[dm][a]:.3f}' for dm in dims] \
            + [f'{avg[a]:.3f}', str(order[a])]
        for dm in dims:
            if a == 'MSSBOA':
                row.append('-')
            else:
                n = usable(d, VARIANT_ORDER, probs, dm)
                w, e, l = _wil(d, 'MSSBOA', a, probs, dm, n)
                row.append(f'{w}/{e}/{l}')
        rows.append(row)
    n = usable(d, VARIANT_ORDER, probs, dims[0])
    return _save('variants', rows), {'avg': avg, 'order': order,
                                     'dims': dims, 'n': n, 'rank': rk}


# ============================================================= design tables
def t8_color():
    d = load('design_color')
    if d is None:
        return None
    probs = [f'K{k}' for k in COLOR_K]
    n = usable(d, MAIN_ORDER, probs, 0)
    if not n:
        return None
    rows = [['Algorithm'] + [f'K = {k} mean' for k in COLOR_K]
            + ['K = 7 best', 'K = 7 std', 'Rank']]
    means7 = {a: np.mean(d[(a, 'K7', 0)][:n]) for a in MAIN_ORDER}
    order = {a: i + 1 for i, a in enumerate(
        sorted(MAIN_ORDER, key=lambda x: -means7[x]))}
    for a in MAIN_ORDER:
        rows.append([a] + [f'{np.mean(d[(a, f"K{k}", 0)][:n]) * 100:.2f}'
                           for k in COLOR_K]
                    + [f'{np.max(d[(a, "K7", 0)][:n]) * 100:.2f}',
                       f'{np.std(d[(a, "K7", 0)][:n]) * 100:.3f}',
                       str(order[a])])
    return _save('t8', rows), {'n': n, 'order': order,
                               'means7': {a: means7[a] * 100 for a in MAIN_ORDER}}


def t10_layout():
    d = load('design_layout')
    if d is None:
        return None
    probs = list(LAYOUT_PROBLEMS)
    n = usable(d, MAIN_ORDER, probs, 0)
    if not n:
        return None
    rows = [['Problem'] + MAIN_ORDER]
    R = []
    for p in probs:
        means = [np.mean(d[(a, p, 0)][:n]) * 100 for a in MAIN_ORDER]
        R.append(stats.rankdata([-m for m in means]))
        rows.append([p] + [f'{m:.2f}' for m in means])
    avg_rank = np.mean(R, axis=0)
    rows.append(['Average rank'] + [f'{v:.2f}' for v in avg_rank])
    return _save('t10', rows), {'n': n,
                                'avg_rank': dict(zip(MAIN_ORDER, avg_rank))}


def t_scale():
    d = load('scale')
    if d is None:
        return None
    probs = [f'N{n}' for n in SCALE_N]
    ns = [n for n in SCALE_N if usable(d, SCALE_ALGOS, [f'N{n}'], 2 * n)]
    if not ns:
        return None
    rows = [['Elements n (D = 2n)'] + SCALE_ALGOS + ['MSSBOA rank', 'MSSBOA std']]
    for n in ns:
        k = usable(d, SCALE_ALGOS, [f'N{n}'], 2 * n)
        means = [np.mean(d[(a, f'N{n}', 2 * n)][:k]) * 100 for a in SCALE_ALGOS]
        rk = stats.rankdata([-m for m in means])
        rows.append([f'{n} (D = {2 * n})'] + [f'{m:.2f}' for m in means]
                    + [str(int(rk[SCALE_ALGOS.index("MSSBOA")])),
                       f'{np.std(d[("MSSBOA", f"N{n}", 2 * n)][:k]) * 100:.2f}'])
    return _save('scale', rows), {'ns': ns, 'algos': SCALE_ALGOS,
                                  'runs': usable(d, SCALE_ALGOS, [f'N{ns[0]}'], 2 * ns[0])}


def t_weights():
    d = load('weights')
    if d is None:
        return None
    probs = [f'{w}|{c}' for w in WEIGHT_SETS for c in LAYOUT_PROBLEMS]
    n = usable(d, WEIGHT_ALGOS, probs, 0)
    if not n:
        return None
    rows = [['Weight configuration'] + [f'{a} (x100)' for a in WEIGHT_ALGOS]
            + ['Best', 'Kendall tau vs. W0']]
    base = None
    for w in WEIGHT_SETS:
        means = [np.mean([np.mean(d[(a, f'{w}|{c}', 0)][:n])
                          for c in LAYOUT_PROBLEMS]) for a in WEIGHT_ALGOS]
        rk = stats.rankdata([-m for m in means])
        if base is None:
            base, tau = rk, 1.0
        else:
            tau = stats.kendalltau(base, rk).statistic
        rows.append([w] + [f'{m * 100:.2f}' for m in means]
                    + [WEIGHT_ALGOS[int(np.argmax(means))], f'{tau:.3f}'])
    return _save('weights', rows), {'n': n, 'algos': WEIGHT_ALGOS}


ALL = {
    't1': t1_parameters, 't2': t2_nmin, 't3': t3_pm, 't4': t4_strategies,
    't5': t5_ablation, 't6': t6_friedman, 't7': t7_wilcoxon,
    't8': t8_color, 't9': t9_layout_problems, 't10': t10_layout,
    'factorial': t_factorial, 'variants': t_variants, 'loss': t_loss_distribution,
    'gap': t_dimension_gap, 'scale': t_scale, 'weights': t_weights,
}


if __name__ == '__main__':
    for k, fn in ALL.items():
        try:
            r = fn()
        except Exception as exc:
            print(f'--- {k}: ERROR {type(exc).__name__}: {exc}')
            continue
        print(f'--- {k} ---')
        if r is None:
            print('   (no data yet)')
            continue
        rows = r[0] if isinstance(r, tuple) else r
        for row in rows[:14]:
            print('   ' + ' | '.join(str(c) for c in row))
        if len(rows) > 14:
            print(f'   ... {len(rows) - 14} more rows')
