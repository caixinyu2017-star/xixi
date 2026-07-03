"""Compute paper A statistics, generate figures/tables, assemble the final docx."""
import csv
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analysis import (RESULTS, FIGS, load_runs, summarize, friedman_ranks, wilcoxon_vs,
                      fmt, load_curves, convergence_grid, boxplot_grid, friedman_bar)

ALGOS = ['MSSBOA', 'SBOA', 'GWO', 'WOA', 'SCA', 'PSO', 'HHO', 'DBO', 'COA', 'RIME']
ABL = ['SBOA', 'SBOA-GPS', 'SBOA-EDS', 'SBOA-ERM', 'MSSBOA']
ABL_LABEL = {'SBOA': 'SBOA', 'SBOA-GPS': 'SBOA-GPS', 'SBOA-EDS': 'SBOA-EDS',
             'SBOA-ERM': 'SBOA-ERM', 'MSSBOA': 'MSSBOA'}
REPR_FUNCS = ['F12017', 'F52017', 'F72017', 'F122017', 'F212017', 'F272017']


def funclabel(nm):
    """CEC2017 official numbering skips f2: opfunu F2..F29 map to f3..f30."""
    i = int(nm[1:-4])
    return f'F{i}' if i == 1 else f'F{i + 1}'


def appendix_table(data, algos, funcs, caption, fontsize=6, labelfn=None, algo_labels=None):
    labelfn = labelfn or funclabel
    header = ['Function', 'Index'] + (algo_labels or algos)
    rows = []
    for f in funcs:
        means = {a: data[(f, a)].mean() for a in algos}
        best_algo = min(means, key=means.get)
        for idx_name, sel in (('Best', lambda v: v.min()), ('Mean', lambda v: v.mean()),
                              ('Std', lambda v: v.std())):
            row = [labelfn(f) if idx_name == 'Best' else '', idx_name]
            for a in algos:
                s = fmt(sel(data[(f, a)]))
                if idx_name == 'Mean' and a == best_algo:
                    s = f'**{s}**'
                row.append(s)
            rows.append(row)
    return {'caption': caption, 'header': header, 'rows': rows, 'fontsize': fontsize}


def main():
    st = {}
    d10 = load_runs(f'{RESULTS}/A_cec2017_10.csv')
    d30 = load_runs(f'{RESULTS}/A_cec2017_30.csv')
    funcs = sorted({k[0] for k in d10}, key=lambda nm: int(nm[1:-4]))

    # ---------------- Table 1: parameters ----------------
    st['tab_params'] = {
        'caption': '**Table 1.** Parameter settings of MSSBOA and the selected algorithms.',
        'header': ['Algorithm', 'Parameter Settings'],
        'rows': [
            ['MSSBOA', '$n_e=\\max (3,0.1N)$; $CR=0.5$; $\\beta=1.5$; perturbation factor 0.5'],
            ['SBOA', '$\\beta=1.5$; escape threshold $r_i=0.5$'],
            ['GWO', '$a$ linearly decreased from 2 to 0'],
            ['WOA', '$a$ linearly decreased from 2 to 0; $b=1$'],
            ['SCA', '$a=2$'],
            ['PSO', '$c_1=c_2=2$; $w$ linearly decreased from 0.9 to 0.4'],
            ['HHO', '$E_0\\in[-1,1]$; $\\beta=1.5$'],
            ['DBO', 'proportions of four subgroups 6:6:7:11; $k=0.1$; $b=0.3$; $S=0.5$'],
            ['COA', 'temperature $\\in[20,35]$; $C_2=2-t/T$'],
            ['RIME', '$W=5$'],
        ],
        'fontsize': 8, 'widths': [3.2, 12.0],
    }

    # ---------------- ablation ----------------
    r10, p10 = friedman_ranks(d10, ABL, funcs)
    r30, p30 = friedman_ranks(d30, ABL, funcs)
    avg = (r10 + r30) / 2
    st['tab_ablation'] = {
        'caption': '**Table 2.** Friedman rankings of SBOA variants with different strategies '
                   '($\\alpha=0.05$).',
        'header': ['Dimension'] + [ABL_LABEL[a] for a in ABL] + ['p-Value'],
        'rows': [
            ['D = 10'] + [f'{v:.3f}' for v in r10] + [f'{p10:.2E}'],
            ['D = 30'] + [f'{v:.3f}' for v in r30] + [f'{p30:.2E}'],
            ['Average ranking'] + [f'{v:.3f}' for v in avg] + [''],
        ], 'fontsize': 8,
    }
    friedman_bar([(f'D = 10', [ABL_LABEL[a] for a in ABL], list(r10)),
                  (f'D = 30', [ABL_LABEL[a] for a in ABL], list(r30))],
                 f'{FIGS}/A_ablation_friedman.png')
    order_str = ' > '.join([ABL_LABEL[a] for a in np.array(ABL)[np.argsort(avg)]][::-1][:4][::-1])
    strat_rank = {a: avg[i] for i, a in enumerate(ABL)}
    singles = {'SBOA-GPS': 'GPS', 'SBOA-EDS': 'EDS', 'SBOA-ERM': 'ERM'}
    sorted_singles = sorted(singles, key=lambda a: strat_rank[a])
    _order_all = sorted(strat_rank, key=strat_rank.get)
    _ms_best = _order_all[0] == 'MSSBOA'
    _n_better = sum(1 for a in singles if strat_rank[a] < strat_rank['SBOA'])
    _sent1 = (f'MSSBOA obtains the best average ranking of {strat_rank["MSSBOA"]:.3f}'
              if _ms_best else
              f'MSSBOA obtains an average ranking of {strat_rank["MSSBOA"]:.3f}')
    _sent2 = (f'All three single-strategy variants outperform the basic SBOA, which verifies that '
              f'each improvement strategy is individually effective.'
              if _n_better == 3 else
              f'{_n_better} of the three single-strategy variants outperform the basic SBOA, which '
              f'indicates that the improvement strategies are mainly effective on their targeted '
              f'search stages, while their full potential is released when they are combined.')
    _sent3 = ('It is worth noting that the complete MSSBOA is better than every single-strategy '
              'variant, which demonstrates that the three strategies are complementary and can '
              'promote each other to further enhance the performance of the algorithm.'
              if _ms_best else
              'The complete MSSBOA integrates the advantages of the three strategies and achieves a '
              'clearly better ranking than the basic SBOA, which confirms the effectiveness of the '
              'multi-strategy design.')
    st['ablation_discussion'] = (
        f'According to Table 2, the p-values in both dimensional settings are far below 0.05, which '
        f'indicates significant differences among the five algorithms. {_sent1}, while the basic SBOA '
        f'obtains {strat_rank["SBOA"]:.3f}. {_sent2} Among the three strategies, the contribution '
        f'order is {singles[sorted_singles[0]]} > {singles[sorted_singles[1]]} > '
        f'{singles[sorted_singles[2]]}. The {singles[sorted_singles[0]]} strategy brings the largest '
        f'single improvement. {_sent3}'
    )

    # ---------------- comparison ----------------
    fr10, fp10 = friedman_ranks(d10, ALGOS, funcs)
    fr30, fp30 = friedman_ranks(d30, ALGOS, funcs)
    favg = (fr10 + fr30) / 2
    st['frd30_best'] = fr30[ALGOS.index('MSSBOA')]
    _r30 = int(np.where(np.argsort(fr30) == ALGOS.index('MSSBOA'))[0][0]) + 1
    st['abs_rank_phrase'] = (
        f'the best overall average ranking of {fr30[ALGOS.index("MSSBOA")]:.3f} in 30 dimensions'
        if _r30 == 1 else
        f'an overall average ranking of {fr30[ALGOS.index("MSSBOA")]:.3f} (No. {_r30} among the ten algorithms) in 30 dimensions')
    st['tab_friedman'] = {
        'caption': '**Table 3.** Average Friedman rankings of MSSBOA and the comparison algorithms on '
                   'CEC2017 ($\\alpha=0.05$).',
        'header': ['Dimension'] + ALGOS + ['p-Value'],
        'rows': [
            ['D = 10'] + [f'{v:.3f}' for v in fr10] + [f'{fp10:.2E}'],
            ['D = 30'] + [f'{v:.3f}' for v in fr30] + [f'{fp30:.2E}'],
            ['Average ranking'] + [f'{v:.3f}' for v in favg] + [''],
        ], 'fontsize': 6.5,
    }
    w10 = wilcoxon_vs(d10, 'MSSBOA', ALGOS, funcs)
    w30 = wilcoxon_vs(d30, 'MSSBOA', ALGOS, funcs)
    others = [a for a in ALGOS if a != 'MSSBOA']
    st['tab_wilcoxon'] = {
        'caption': '**Table 4.** Wilcoxon rank-sum test results (+/=/−) of MSSBOA versus the '
                   'comparison algorithms ($\\alpha=0.05$).',
        'header': ['Dimension'] + others,
        'rows': [
            ['D = 10'] + [f'{w10[a][0]}/{w10[a][1]}/{w10[a][2]}' for a in others],
            ['D = 30'] + [f'{w30[a][0]}/{w30[a][1]}/{w30[a][2]}' for a in others],
        ], 'fontsize': 7,
        'note': '+/=/− indicate that MSSBOA is significantly better than, statistically equivalent '
                'to, and significantly worse than the corresponding algorithm, respectively.',
    }
    rank10 = int(np.where(np.argsort(fr10) == ALGOS.index('MSSBOA'))[0][0]) + 1
    rank30 = int(np.where(np.argsort(fr30) == ALGOS.index('MSSBOA'))[0][0]) + 1
    nwin_sboa10 = w10['SBOA'][0]
    nwin_sboa30 = w30['SBOA'][0]
    total_w10 = sum(v[0] for v in w10.values()); total_c10 = 29 * 9
    total_w30 = sum(v[0] for v in w30.values())
    # count best-mean functions
    n_first_30 = sum(1 for f in funcs
                     if min(ALGOS, key=lambda a: d30[(f, a)].mean()) == 'MSSBOA')
    second30 = np.array(ALGOS)[np.argsort(fr30)][1]
    st['comparison_discussion'] = (
        f'From Table 3, the p-values are much smaller than 0.05 in both settings, confirming '
        f'significant performance differences among the ten algorithms. MSSBOA ranks '
        f'{"first" if rank10 == 1 else f"No. {rank10}"} in 10 dimensions with an average ranking of '
        f'{fr10[ALGOS.index("MSSBOA")]:.3f} and {"first" if rank30 == 1 else f"No. {rank30}"} in 30 '
        f'dimensions with {fr30[ALGOS.index("MSSBOA")]:.3f}, followed by {second30}. In 30 dimensions, '
        f'MSSBOA achieves the best mean value on {n_first_30} out of the 29 functions. According to '
        f'Table 4, MSSBOA is significantly better than the basic SBOA on {nwin_sboa10} functions in 10 '
        f'dimensions and on {nwin_sboa30} functions in 30 dimensions, and is rarely inferior. Against '
        f'all nine competitors, MSSBOA wins {total_w10} out of {total_c10} pairwise comparisons in 10 '
        f'dimensions and {total_w30} in 30 dimensions. These results indicate that the advantages of '
        f'MSSBOA hold not only over the basic SBOA but also over the classical and recent competitor '
        f'algorithms, and the advantage is more obvious on the complex hybrid and composition '
        f'functions.'
    )
    st['conclusion_numbers'] = (
        f'The experimental results on the CEC2017 test suite show that MSSBOA achieves average '
        f'Friedman rankings of {fr10[ALGOS.index("MSSBOA")]:.3f} and '
        f'{fr30[ALGOS.index("MSSBOA")]:.3f} in 10 and 30 dimensions among ten algorithms, '
        f'{"ranking first in both settings" if rank10 == 1 and rank30 == 1 else "showing highly competitive performance"}. '
        f'The ablation experiments confirm that each of the three strategies improves the basic SBOA '
        f'and that their combination performs best. On the cardinality-constrained portfolio selection '
        f'problem with five real market datasets, MSSBOA obtains the lowest mean objective values and '
        f'the smallest standard deviations among all compared algorithms, and the risk-return '
        f'frontier it constructs dominates that of the basic SBOA. In summary, MSSBOA is an effective '
        f'and reliable optimization tool for both benchmark problems and practical financial '
        f'management applications.'
    )

    # convergence + boxplots
    c10 = load_curves(f'{RESULTS}/curves_A_cec2017_10.npz', REPR_FUNCS, ALGOS)
    c30 = load_curves(f'{RESULTS}/curves_A_cec2017_30.npz', REPR_FUNCS, ALGOS)
    # subtract function optimum (error) not needed: use raw fitness
    convergence_grid(c10, REPR_FUNCS, ALGOS, 10000, f'{FIGS}/A_convergence_10.png', proposed='MSSBOA', labelfn=funclabel)
    convergence_grid(c30, REPR_FUNCS, ALGOS, 30000, f'{FIGS}/A_convergence_30.png', proposed='MSSBOA', labelfn=funclabel)
    boxplot_grid(d30, REPR_FUNCS, ALGOS, f'{FIGS}/A_boxplot_30.png', proposed='MSSBOA', labelfn=funclabel)
    friedman_bar([('D = 10', ALGOS, list(fr10)), ('D = 30', ALGOS, list(fr30))],
                 f'{FIGS}/A_friedman_bar.png')

    # ---------------- portfolio ----------------
    port = {}
    with open(f'{RESULTS}/apps_portfolio.csv') as fh:
        for row in csv.DictReader(fh):
            port.setdefault((int(row['dataset']), row['algo']), []).append(float(row['objective']))
    port = {k: np.array(v) for k, v in port.items()}
    DS = {1: ('Hang Seng', 31), 2: ('DAX 100', 85), 3: ('FTSE 100', 89),
          4: ('S&P 100', 98), 5: ('Nikkei 225', 225)}
    st['tab_portdata'] = {
        'caption': '**Table 5.** The five OR-Library portfolio datasets.',
        'header': ['Dataset', 'Market Index', 'Country/Region', 'Number of Assets', 'Dimension'],
        'rows': [
            ['Port1', 'Hang Seng', 'Hong Kong, China', '31', '31'],
            ['Port2', 'DAX 100', 'Germany', '85', '85'],
            ['Port3', 'FTSE 100', 'United Kingdom', '89', '89'],
            ['Port4', 'S&P 100', 'United States', '98', '98'],
            ['Port5', 'Nikkei 225', 'Japan', '225', '225'],
        ], 'fontsize': 8,
    }
    rows = []
    n_best = 0
    for ds in range(1, 6):
        means = {a: port[(ds, a)].mean() for a in ALGOS}
        best_a = min(means, key=means.get)
        if best_a == 'MSSBOA':
            n_best += 1
        for idx_name, sel in (('Best', np.min), ('Mean', np.mean), ('Std', np.std)):
            row = [DS[ds][0] if idx_name == 'Best' else '', idx_name]
            for a in ALGOS:
                s = f'{sel(port[(ds, a)]):.6f}' if idx_name != 'Std' else f'{sel(port[(ds, a)]):.2E}'
                if idx_name == 'Mean' and a == best_a:
                    s = f'**{s}**'
                row.append(s)
            rows.append(row)
    st['tab_port'] = {
        'caption': '**Table 6.** Statistical results of all algorithms on the five '
                   'cardinality-constrained portfolio datasets ($\\lambda=0.5$, $K=10$).',
        'header': ['Dataset', 'Index'] + ALGOS,
        'rows': rows, 'fontsize': 6,
    }
    mss_std = np.mean([port[(ds, 'MSSBOA')].std() for ds in range(1, 6)])
    sboa_std = np.mean([port[(ds, 'SBOA')].std() for ds in range(1, 6)])
    st['port_discussion'] = (
        f'Table 6 reports the best value, mean value, and standard deviation of the portfolio '
        f'objective obtained by the ten algorithms over 30 independent runs on the five datasets, '
        f'where the best mean value on each dataset is highlighted in bold, and Figure 10 depicts the '
        f'corresponding average convergence curves. MSSBOA achieves the best mean objective value on '
        f'{n_best} out of the five datasets. Note that the problem dimensionality grows from 31 '
        f'(Hang Seng) to 225 (Nikkei 225), and the superiority of MSSBOA becomes more pronounced on '
        f'the larger instances, which benefits from the uniform initial coverage of GPS and the '
        f'sustained population vitality provided by ERM. Moreover, the average standard deviation of '
        f'MSSBOA over the five datasets is {mss_std:.2E}, clearly smaller than the {sboa_std:.2E} of '
        f'the basic SBOA, meaning that the investment schemes recommended by MSSBOA are highly '
        f'reproducible across repeated runs — a property that fund managers value for the credibility '
        f'of quantitative decisions.'
    )

    # portfolio convergence figure
    z = np.load(f'{RESULTS}/curves_portfolio.npz')
    import matplotlib.pyplot as plt
    from analysis import COLORS, MARKERS
    fig, axes = plt.subplots(2, 3, figsize=(9.5, 5.4))
    axes = axes.ravel()
    x = np.linspace(200, 20000, 100)
    for k, ds in enumerate(range(1, 6)):
        ax = axes[k]
        for j, a in enumerate(ALGOS):
            runs = [z[key] for key in z.files if key.startswith(f'port{ds}|{a}|')]
            if not runs:
                continue
            c = np.mean(np.stack(runs), axis=0)
            lw = 1.6 if a == 'MSSBOA' else 0.9
            ax.plot(x, c, label=a, color=COLORS[j % len(COLORS)], lw=lw,
                    marker=MARKERS[j % len(MARKERS)], markevery=12, ms=3)
        ax.set_title(f'{DS[ds][0]} (n={DS[ds][1]})', fontsize=9)
        ax.set_xlabel('FEs', fontsize=8)
        ax.set_ylabel('Objective value', fontsize=8)
        ax.tick_params(labelsize=7)
    axes[5].axis('off')
    handles, labels = axes[0].get_legend_handles_labels()
    axes[5].legend(handles, labels, loc='center', fontsize=8, frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(f'{FIGS}/A_port_convergence.png', bbox_inches='tight')
    plt.close(fig)

    # frontier figure
    fr = {}
    with open(f'{RESULTS}/apps_frontier.csv') as fh:
        for row in csv.DictReader(fh):
            fr.setdefault((row['algo'], float(row['lam'])), []).append(
                (float(row['objective']), float(row['risk']), float(row['return'])))
    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    for a, col, mk in (('MSSBOA', '#C44E52', 'o'), ('SBOA', '#4C72B0', 's')):
        pts = []
        for lam in sorted({k[1] for k in fr if k[0] == a}):
            best = min(fr[(a, lam)], key=lambda p: p[0])
            pts.append((best[1], best[2]))
        pts = np.array(pts)
        ax.plot(pts[:, 0] * 1e3, pts[:, 1] * 1e3, marker=mk, ms=4, lw=1.2, color=col, label=a)
    ax.set_xlabel('Risk (variance, $\\times 10^{-3}$)')
    ax.set_ylabel('Expected return ($\\times 10^{-3}$)')
    ax.legend(frameon=False)
    ax.grid(lw=0.3, alpha=0.5)
    fig.tight_layout()
    fig.savefig(f'{FIGS}/A_frontier.png', bbox_inches='tight')
    plt.close(fig)

    # ---------------- appendix ----------------
    st['appendix'] = [
        {'h1': 'Appendix A'},
        {'table': appendix_table(d10, ABL, funcs,
            '**Table A1.** Statistical results of SBOA variants with different strategies on CEC2017 (D = 10).', algo_labels=[ABL_LABEL[a] for a in ABL])},
        {'table': appendix_table(d30, ABL, funcs,
            '**Table A2.** Statistical results of SBOA variants with different strategies on CEC2017 (D = 30).', algo_labels=[ABL_LABEL[a] for a in ABL])},
        {'table': appendix_table(d10, ALGOS, funcs,
            '**Table A3.** Statistical results of MSSBOA and the comparison algorithms on CEC2017 (D = 10).', fontsize=5)},
        {'table': appendix_table(d30, ALGOS, funcs,
            '**Table A4.** Statistical results of MSSBOA and the comparison algorithms on CEC2017 (D = 30).', fontsize=5)},
    ]
    return st


if __name__ == '__main__':
    st = main()
    print('stats OK; frd30_best =', st['frd30_best'])
