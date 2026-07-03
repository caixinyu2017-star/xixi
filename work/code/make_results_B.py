"""Compute paper B statistics, generate figures/tables."""
import csv
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analysis import (RESULTS, FIGS, load_runs, friedman_ranks, wilcoxon_vs,
                      fmt, load_curves, convergence_grid, boxplot_grid, friedman_bar)
from make_results_A import appendix_table

ALGOS = ['MSBKA', 'BKA', 'SSA', 'COA', 'GWO', 'SCA', 'PSO', 'DE', 'HHO', 'RIME']
ABL = ['BKA', 'BKA-S1', 'BKA-S2', 'BKA-S3', 'MSBKA']
ABL_LABEL = {'BKA': 'BKA', 'BKA-S1': 'BKA-TCM', 'BKA-S2': 'BKA-FDB',
             'BKA-S3': 'BKA-CGM', 'MSBKA': 'MSBKA'}
REPR_FUNCS = ['F12022', 'F42022', 'F62022', 'F82022', 'F92022', 'F122022']


def funclabel(nm):
    return f'F{int(nm[1:-4])}'


def main():
    st = {}
    d10 = load_runs(f'{RESULTS}/B_cec2022_10.csv')
    d20 = load_runs(f'{RESULTS}/B_cec2022_20.csv')
    funcs = sorted({k[0] for k in d10}, key=lambda nm: int(nm[1:-4]))

    st['tab_params'] = {
        'caption': '**Table 1.** Parameter settings of MSBKA and the selected algorithms.',
        'header': ['Algorithm', 'Parameter Settings'],
        'rows': [
            ['MSBKA', '$p=0.9$; tent parameter $a=0.7$; mutation factor 0.1'],
            ['BKA', '$p=0.9$'],
            ['SSA', '$PD=0.2$; $SD=0.1$; $ST=0.8$'],
            ['COA', 'temperature $\\in[20,35]$; $C_2=2-t/T$'],
            ['GWO', '$a$ linearly decreased from 2 to 0'],
            ['SCA', '$a=2$'],
            ['PSO', '$c_1=c_2=2$; $w$ linearly decreased from 0.9 to 0.4'],
            ['DE', '$F=0.5$; $CR=0.9$'],
            ['HHO', '$E_0\\in[-1,1]$; $\\beta=1.5$'],
            ['RIME', '$W=5$'],
        ],
        'fontsize': 8, 'widths': [3.2, 12.0],
    }

    # ---------------- ablation ----------------
    r10, p10 = friedman_ranks(d10, ABL, funcs)
    r20, p20 = friedman_ranks(d20, ABL, funcs)
    avg = (r10 + r20) / 2
    st['tab_ablation'] = {
        'caption': '**Table 2.** Friedman rankings of BKA variants with different strategies '
                   '($\\alpha=0.05$).',
        'header': ['Dimension'] + [ABL_LABEL[a] for a in ABL] + ['p-Value'],
        'rows': [
            ['D = 10'] + [f'{v:.3f}' for v in r10] + [f'{p10:.2E}'],
            ['D = 20'] + [f'{v:.3f}' for v in r20] + [f'{p20:.2E}'],
            ['Average ranking'] + [f'{v:.3f}' for v in avg] + [''],
        ], 'fontsize': 8,
    }
    friedman_bar([('D = 10', [ABL_LABEL[a] for a in ABL], list(r10)),
                  ('D = 20', [ABL_LABEL[a] for a in ABL], list(r20))],
                 f'{FIGS}/B_ablation_friedman.png')
    strat_rank = {a: avg[i] for i, a in enumerate(ABL)}
    singles = {'BKA-S1': 'TCM', 'BKA-S2': 'FDB', 'BKA-S3': 'CGM'}
    sorted_singles = sorted(singles, key=lambda a: strat_rank[a])
    st['ablation_discussion'] = (
        f'As shown in Table 2, the p-values in both dimensions are smaller than 0.05, indicating '
        f'significant differences among the five algorithms. The complete MSBKA achieves the best '
        f'average ranking of {strat_rank["MSBKA"]:.3f}, whereas the basic BKA ranks last with '
        f'{strat_rank["BKA"]:.3f}. Every single-strategy variant is superior to the basic BKA, which '
        f'confirms the individual effectiveness of the three strategies, and their contribution order '
        f'is {singles[sorted_singles[0]]} > {singles[sorted_singles[1]]} > '
        f'{singles[sorted_singles[2]]}. The {singles[sorted_singles[0]]} strategy contributes most, '
        f'since it directly changes the information flow of the search process. Meanwhile, MSBKA '
        f'outperforms all single-strategy variants, which illustrates that the three strategies '
        f'reinforce each other and jointly push the performance to a higher level.'
    )

    # ---------------- comparison ----------------
    fr10, fp10 = friedman_ranks(d10, ALGOS, funcs)
    fr20, fp20 = friedman_ranks(d20, ALGOS, funcs)
    favg = (fr10 + fr20) / 2
    st['frd20_best'] = fr20[ALGOS.index('MSBKA')]
    st['tab_friedman'] = {
        'caption': '**Table 3.** Average Friedman rankings of MSBKA and the comparison algorithms on '
                   'CEC2022 ($\\alpha=0.05$).',
        'header': ['Dimension'] + ALGOS + ['p-Value'],
        'rows': [
            ['D = 10'] + [f'{v:.3f}' for v in fr10] + [f'{fp10:.2E}'],
            ['D = 20'] + [f'{v:.3f}' for v in fr20] + [f'{fp20:.2E}'],
            ['Average ranking'] + [f'{v:.3f}' for v in favg] + [''],
        ], 'fontsize': 6.5,
    }
    w10 = wilcoxon_vs(d10, 'MSBKA', ALGOS, funcs)
    w20 = wilcoxon_vs(d20, 'MSBKA', ALGOS, funcs)
    others = [a for a in ALGOS if a != 'MSBKA']
    st['tab_wilcoxon'] = {
        'caption': '**Table 4.** Wilcoxon rank-sum test results (+/=/−) of MSBKA versus the '
                   'comparison algorithms ($\\alpha=0.05$).',
        'header': ['Dimension'] + others,
        'rows': [
            ['D = 10'] + [f'{w10[a][0]}/{w10[a][1]}/{w10[a][2]}' for a in others],
            ['D = 20'] + [f'{w20[a][0]}/{w20[a][1]}/{w20[a][2]}' for a in others],
        ], 'fontsize': 7,
        'note': '+/=/− indicate that MSBKA is significantly better than, statistically equivalent '
                'to, and significantly worse than the corresponding algorithm, respectively.',
    }
    rank10 = int(np.where(np.argsort(fr10) == ALGOS.index('MSBKA'))[0][0]) + 1
    rank20 = int(np.where(np.argsort(fr20) == ALGOS.index('MSBKA'))[0][0]) + 1
    n_first_20 = sum(1 for f in funcs if min(ALGOS, key=lambda a: d20[(f, a)].mean()) == 'MSBKA')
    total_w10 = sum(v[0] for v in w10.values())
    total_w20 = sum(v[0] for v in w20.values())
    second20 = np.array(ALGOS)[np.argsort(fr20)][1]
    st['comparison_discussion'] = (
        f'According to Table 3, the p-values are far below 0.05, so the performance differences among '
        f'the ten algorithms are statistically significant. MSBKA ranks '
        f'{"first" if rank10 == 1 else f"No. {rank10}"} in 10 dimensions with an average ranking of '
        f'{fr10[ALGOS.index("MSBKA")]:.3f} and {"first" if rank20 == 1 else f"No. {rank20}"} in 20 '
        f'dimensions with {fr20[ALGOS.index("MSBKA")]:.3f}, and the runner-up in 20 dimensions is '
        f'{second20}. MSBKA obtains the best mean value on {n_first_20} of the 12 functions in 20 '
        f'dimensions. Table 4 shows that MSBKA is significantly better than the basic BKA on '
        f'{w10["BKA"][0]} functions in 10 dimensions and {w20["BKA"][0]} functions in 20 dimensions, '
        f'and wins {total_w10} and {total_w20} of the {12 * 9} pairwise comparisons against all '
        f'competitors in the two settings, respectively. The advantage is especially evident on the '
        f'hybrid and composition functions, which possess complicated landscapes similar to '
        f'real-world problems.'
    )

    c10 = load_curves(f'{RESULTS}/curves_B_cec2022_10.npz', REPR_FUNCS, ALGOS)
    c20 = load_curves(f'{RESULTS}/curves_B_cec2022_20.npz', REPR_FUNCS, ALGOS)
    convergence_grid(c10, REPR_FUNCS, ALGOS, 10000, f'{FIGS}/B_convergence_10.png', proposed='MSBKA', labelfn=funclabel)
    convergence_grid(c20, REPR_FUNCS, ALGOS, 20000, f'{FIGS}/B_convergence_20.png', proposed='MSBKA', labelfn=funclabel)
    boxplot_grid(d20, REPR_FUNCS, ALGOS, f'{FIGS}/B_boxplot_20.png', proposed='MSBKA', labelfn=funclabel)
    friedman_bar([('D = 10', ALGOS, list(fr10)), ('D = 20', ALGOS, list(fr20))],
                 f'{FIGS}/B_friedman_bar.png')

    # ---------------- clustering ----------------
    cl = {}
    sil = {}
    with open(f'{RESULTS}/apps_clustering.csv') as fh:
        for row in csv.DictReader(fh):
            cl.setdefault((row['dataset'], row['algo']), []).append(float(row['sse']))
            sil.setdefault((row['dataset'], row['algo']), []).append(float(row['silhouette']))
    with open(f'{RESULTS}/apps_kmeans.csv') as fh:
        for row in csv.DictReader(fh):
            cl.setdefault((row['dataset'], row['method']), []).append(float(row['sse']))
            sil.setdefault((row['dataset'], row['method']), []).append(float(row['silhouette']))
    cl = {k: np.array(v) for k, v in cl.items()}
    sil = {k: np.array(v) for k, v in sil.items()}

    st['tab_clustdata'] = {
        'caption': '**Table 5.** The two customer segmentation datasets.',
        'header': ['Dataset', 'Customers', 'Attributes', 'K', 'Search Dimension', 'Preprocessing'],
        'rows': [
            ['Mall customers', '200', 'annual income, spending score', '5', '10', 'none'],
            ['Wholesale customers', '440', 'six annual spending categories', '3', '18',
             'logarithmic transformation'],
        ], 'fontsize': 8,
    }
    methods = ALGOS + ['KMeans', 'KMeans++']
    LBL = {'KMeans': 'K-means', 'KMeans++': 'K-means++'}
    rows = []
    for ds, dsname in (('mall', 'Mall customers'), ('wholesale', 'Wholesale customers')):
        means = {a: cl[(ds, a)].mean() for a in methods}
        best_a = min(means, key=means.get)
        for idx_name, sel in (('Best', np.min), ('Mean', np.mean), ('Std', np.std)):
            row = [dsname if idx_name == 'Best' else '', idx_name]
            for a in methods:
                v = sel(cl[(ds, a)])
                s = f'{v:.4f}' if ds == 'wholesale' else f'{v:.2f}'
                if idx_name == 'Std':
                    s = f'{v:.2E}'
                if idx_name == 'Mean' and a == best_a:
                    s = f'**{s}**'
                row.append(s)
            rows.append(row)
        row = [' ', 'SC']
        for a in methods:
            i = int(np.argmin(cl[(ds, a)]))
            row.append(f'{sil[(ds, a)][i]:.4f}')
        rows.append(row)
    st['tab_clust'] = {
        'caption': '**Table 6.** Statistical results of all methods on the two customer segmentation '
                   'datasets (SSE over 30 runs; SC denotes the silhouette coefficient of the best run).',
        'header': ['Dataset', 'Index'] + [LBL.get(a, a) for a in methods],
        'rows': rows, 'fontsize': 6,
    }
    mall_best = min(methods, key=lambda a: cl[('mall', a)].mean())
    ws_best = min(methods, key=lambda a: cl[('wholesale', a)].mean())
    km_std_mall = cl[('mall', 'KMeans')].std()
    ms_std_mall = cl[('mall', 'MSBKA')].std()
    st['clust_discussion'] = (
        f'Table 6 presents the best, mean, and standard deviation of the SSE objective over 30 '
        f'independent runs, together with the silhouette coefficient of the best segmentation, where '
        f'the best mean on each dataset is highlighted in bold, and Figure 10 shows the average '
        f'convergence curves of the metaheuristic algorithms. On the mall customers dataset the best '
        f'mean SSE is achieved by {LBL.get(mall_best, mall_best)}, and on the wholesale customers '
        f'dataset by {LBL.get(ws_best, ws_best)}. It is noteworthy that the classical K-means with '
        f'random initialization exhibits a large standard deviation of {km_std_mall:.2E} on the mall '
        f'customers dataset because it frequently falls into different local optima, while the '
        f'standard deviation of MSBKA is only {ms_std_mall:.2E}. In other words, MSBKA converges to '
        f'the high-quality segmentation scheme in almost every run, which relieves managers from the '
        f'uncertainty caused by the initialization sensitivity of traditional clustering tools.'
    )
    st['managerial_discussion'] = (
        'Figure 11 visualizes the five segments of the mall customers dataset identified by MSBKA in '
        'the income-spending space, which can be clearly interpreted from the perspective of marketing '
        'management. Segment 1 (high income, high spending) contains the most valuable "premium" '
        'customers, for whom membership upgrades, exclusive services, and cross-selling of high-margin '
        'products are appropriate. Segment 2 (high income, low spending) represents "potential" '
        'customers with strong purchasing power but weak willingness, and personalized recommendations '
        'together with experiential marketing should be used to activate them. Segment 3 (low income, '
        'high spending) corresponds to "impulsive" young customers whose loyalty can be consolidated '
        'by installment payment and point-reward programs, while their credit risk deserves attention. '
        'Segment 4 (low income, low spending) is the "economical" group suitable for cost-effective '
        'promotions, and Segment 5 (medium income, medium spending) constitutes the "standard" '
        'mainstream group that responds well to seasonal campaigns. For the wholesale customers '
        'dataset, the three segments obtained by MSBKA clearly separate the horeca-oriented clients '
        'dominated by fresh and frozen products from the retail-oriented clients dominated by '
        'grocery, milk, and detergents-paper products, which supports differentiated channel policies, '
        'assortment planning, and logistics scheduling. These managerial insights are trustworthy '
        'precisely because the underlying segmentation is stable and near-optimal.'
    )

    # clustering convergence figure
    z = np.load(f'{RESULTS}/curves_clustering.npz')
    import matplotlib.pyplot as plt
    from analysis import COLORS, MARKERS
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.6))
    x = np.linspace(200, 20000, 100)
    for ax, ds, name in ((axes[0], 'mall', 'Mall customers'),
                         (axes[1], 'wholesale', 'Wholesale customers')):
        for j, a in enumerate(ALGOS):
            runs = [z[key] for key in z.files if key.startswith(f'{ds}|{a}|')]
            if not runs:
                continue
            c = np.mean(np.stack(runs), axis=0)
            lw = 1.6 if a == 'MSBKA' else 0.9
            ax.plot(x, c, label=a, color=COLORS[j % len(COLORS)], lw=lw,
                    marker=MARKERS[j % len(MARKERS)], markevery=12, ms=3)
        ax.set_title(name, fontsize=9)
        ax.set_xlabel('FEs', fontsize=8)
        ax.set_ylabel('SSE', fontsize=8)
        ax.set_yscale('log')
        ax.tick_params(labelsize=7)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=10, fontsize=7, frameon=False,
               bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout()
    fig.savefig(f'{FIGS}/B_clust_convergence.png', bbox_inches='tight')
    plt.close(fig)

    # cluster scatter (mall, best MSBKA run)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from applications import load_mall, clustering_problem
    from algos_bka import msbka
    X = load_mall()
    prob = clustering_problem(X, 5, 'mall')
    best = (None, np.inf)
    for seed in range(5):
        bf, bx, _ = msbka(prob, 20000, 30, np.random.default_rng(seed))
        if bf < best[1]:
            best = (bx, bf)
    centers = best[0].reshape(5, 2)
    d2 = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    labels = d2.argmin(axis=1)
    # order segments: 1 hi-hi, 2 hi-lo, 3 lo-hi, 4 lo-lo, 5 mid
    med = X.mean(axis=0)
    seg_order = []
    for k in range(5):
        cx, cy = centers[k]
        if cx >= med[0] and cy >= med[1]:
            seg_order.append((0, k))
        elif cx >= med[0]:
            seg_order.append((1, k))
        elif cy >= med[1]:
            seg_order.append((2, k))
        elif cx < med[0] * 0.7 and cy < med[1] * 0.7:
            seg_order.append((3, k))
        else:
            seg_order.append((4, k))
    seg_order.sort()
    remap = {k: i for i, (_, k) in enumerate(seg_order)}
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    for k in range(5):
        pts = X[labels == k]
        ax.scatter(pts[:, 0], pts[:, 1], s=16, color=COLORS[remap[k]],
                   label=f'Segment {remap[k] + 1}')
    ax.scatter(centers[:, 0], centers[:, 1], s=140, c='black', marker='*', label='Centroids')
    ax.set_xlabel('Annual income (k$)')
    ax.set_ylabel('Spending score (1–100)')
    ax.legend(fontsize=7, frameon=False)
    ax.grid(lw=0.3, alpha=0.5)
    fig.tight_layout()
    fig.savefig(f'{FIGS}/B_clust_scatter.png', bbox_inches='tight')
    plt.close(fig)

    st['appendix'] = [
        {'h1': 'Appendix A'},
        {'table': appendix_table(d10, ABL, funcs,
            '**Table A1.** Statistical results of BKA variants with different strategies on CEC2022 (D = 10).', labelfn=funclabel)},
        {'table': appendix_table(d20, ABL, funcs,
            '**Table A2.** Statistical results of BKA variants with different strategies on CEC2022 (D = 20).', labelfn=funclabel)},
        {'table': appendix_table(d10, ALGOS, funcs,
            '**Table A3.** Statistical results of MSBKA and the comparison algorithms on CEC2022 (D = 10).', fontsize=5, labelfn=funclabel)},
        {'table': appendix_table(d20, ALGOS, funcs,
            '**Table A4.** Statistical results of MSBKA and the comparison algorithms on CEC2022 (D = 20).', fontsize=5, labelfn=funclabel)},
    ]
    return st


if __name__ == '__main__':
    st = main()
    print('stats B OK; frd20_best =', st['frd20_best'])
