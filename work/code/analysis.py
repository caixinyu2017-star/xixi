"""Statistics and figure generation shared by both papers."""
import csv
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
FIGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figs')
os.makedirs(FIGS, exist_ok=True)

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif'],
    'font.size': 9,
    'axes.linewidth': 0.8,
    'figure.dpi': 300,
    'savefig.dpi': 300,
})

MARKERS = ['o', 's', '^', 'v', 'D', 'p', '*', 'X', '<', '>', 'h', '+', 'x']
COLORS = plt.cm.tab10.colors + plt.cm.Dark2.colors


def load_runs(csv_path):
    """Return dict[(func, algo)] -> np.array of best_f over runs."""
    data = {}
    with open(csv_path) as fh:
        rd = csv.DictReader(fh)
        for row in rd:
            key = (row['func'], row['algo'])
            data.setdefault(key, []).append(float(row['best_f']))
    return {k: np.array(v) for k, v in data.items()}


def func_order(funcs, suite):
    def keyf(nm):
        return int(nm[1:].replace(suite, ''))
    return sorted(funcs, key=keyf)


def summarize(data, algos, suite):
    """Return funcs list and stats dict[algo][func] = (best, mean, std)."""
    funcs = sorted({k[0] for k in data}, key=lambda nm: int(nm[1:-4]))
    out = {a: {} for a in algos}
    for f in funcs:
        for a in algos:
            v = data[(f, a)]
            out[a][f] = (v.min(), v.mean(), v.std())
    return funcs, out


def friedman_ranks(data, algos, funcs):
    """Mean Friedman rank per algorithm (ranking mean error per function), plus p-value."""
    R = np.zeros((len(funcs), len(algos)))
    for i, f in enumerate(funcs):
        means = np.array([data[(f, a)].mean() for a in algos])
        R[i] = stats.rankdata(means)
    avg = R.mean(axis=0)
    try:
        stat, p = stats.friedmanchisquare(*[R[:, j] for j in range(len(algos))])
    except Exception:
        stat, p = np.nan, np.nan
    return avg, p


def wilcoxon_vs(data, proposed, algos, funcs, alpha=0.05):
    """Return dict[algo] = (win, tie, loss) counts from the proposed algorithm's view."""
    out = {}
    for a in algos:
        if a == proposed:
            continue
        w = t = l = 0
        for f in funcs:
            x = data[(f, proposed)]
            y = data[(f, a)]
            if np.allclose(x, y, rtol=1e-12, atol=1e-12):
                t += 1
                continue
            try:
                _, p = stats.ranksums(x, y)
            except Exception:
                p = 1.0
            if p >= alpha:
                t += 1
            elif x.mean() < y.mean():
                w += 1
            else:
                l += 1
        out[a] = (w, t, l)
    return out


def fmt(v):
    if v == 0:
        return '0.00E+00'
    return f'{v:.2E}'


def load_curves(npz_path, funcs, algos):
    z = np.load(npz_path)
    out = {}
    for f in funcs:
        for a in algos:
            runs = [z[k] for k in z.files if k.startswith(f'{f}|{a}|')]
            if runs:
                out[(f, a)] = np.mean(np.stack(runs), axis=0)
    return out


def convergence_grid(curves, funcs_sel, algos, max_fes, path, ncols=3, proposed=None, labelfn=None):
    n = len(funcs_sel)
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(2.9 * ncols, 2.4 * nrows))
    axes = np.atleast_1d(axes).ravel()
    x = np.linspace(max_fes / 100, max_fes, 100)
    for k, f in enumerate(funcs_sel):
        ax = axes[k]
        for j, a in enumerate(algos):
            c = curves.get((f, a))
            if c is None:
                continue
            lw = 1.6 if a == proposed else 0.9
            ax.semilogy(x, np.maximum(c, 1e-16), label=a, color=COLORS[j % len(COLORS)],
                        marker=MARKERS[j % len(MARKERS)], markevery=12, ms=3, lw=lw)
        ax.set_title(labelfn(f) if labelfn else f.replace('2017', '').replace('2022', ''), fontsize=9)
        ax.set_xlabel('FEs', fontsize=8)
        ax.set_ylabel('Fitness value', fontsize=8)
        ax.tick_params(labelsize=7)
    for k in range(n, len(axes)):
        axes[k].axis('off')
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=min(len(algos), 7),
               fontsize=8, frameon=False, bbox_to_anchor=(0.5, -0.005))
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)


def boxplot_grid(data, funcs_sel, algos, path, ncols=3, proposed=None, labelfn=None):
    n = len(funcs_sel)
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(3.0 * ncols, 2.5 * nrows))
    axes = np.atleast_1d(axes).ravel()
    for k, f in enumerate(funcs_sel):
        ax = axes[k]
        vals = [data[(f, a)] for a in algos]
        bp = ax.boxplot(vals, patch_artist=True, showfliers=True,
                        flierprops=dict(marker='+', ms=3, markeredgecolor='gray'))
        for j, box in enumerate(bp['boxes']):
            box.set(facecolor=list(COLORS[j % len(COLORS)]) + [0.6], lw=0.7)
        for med in bp['medians']:
            med.set(color='black', lw=0.9)
        ax.set_yscale('log')
        ax.set_title(labelfn(f) if labelfn else f.replace('2017', '').replace('2022', ''), fontsize=9)
        ax.set_xticklabels(algos, rotation=60, fontsize=6.5, ha='right')
        ax.tick_params(axis='y', labelsize=7)
    for k in range(n, len(axes)):
        axes[k].axis('off')
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)


def friedman_bar(rank_sets, path, colors_idx=None):
    """rank_sets: list of (title, algos, ranks). One subplot per set."""
    n = len(rank_sets)
    fig, axes = plt.subplots(1, n, figsize=(4.2 * n, 3.0))
    axes = np.atleast_1d(axes)
    for ax, (title, algos, ranks) in zip(axes, rank_sets):
        order = np.argsort(ranks)
        a_s = [algos[i] for i in order]
        r_s = [ranks[i] for i in order]
        cols = [COLORS[algos.index(a) % len(COLORS)] for a in a_s]
        bars = ax.bar(range(len(a_s)), r_s, color=cols, edgecolor='black', lw=0.5)
        ax.set_xticks(range(len(a_s)))
        ax.set_xticklabels(a_s, rotation=60, fontsize=7, ha='right')
        ax.set_ylabel('Average Friedman ranking', fontsize=8)
        ax.set_title(title, fontsize=9)
        for b, r in zip(bars, r_s):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.05, f'{r:.2f}',
                    ha='center', fontsize=6)
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
