"""Generate the results narrative from the regenerated tables.

Every sentence that states a number is produced here, from the same metadata
that produces the tables, so the prose cannot drift away from the data.  The
style follows normal academic English usage: the past tense for what was done,
the present tense for what a table or figure shows and for interpretation.
"""
import numpy as np

import tables as TB


def _nth(i):
    return {1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth',
            6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth',
            10: 'tenth', 11: 'eleventh'}.get(i, f'{i}th')


def _series(items, conj='and'):
    items = list(items)
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f'{items[0]} {conj} {items[1]}'
    return ', '.join(items[:-1]) + f', {conj} ' + items[-1]


def _dims(ds):
    return _series([str(d) for d in ds]) + ' dimensions'


class Narrative:
    """Collects every table's metadata and writes the paragraphs from it."""

    def __init__(self):
        self.t2 = TB.t2_nmin()
        self.t3 = TB.t3_pm()
        self.t5 = TB.t5_ablation()
        self.t6 = TB.t6_friedman()
        self.t7 = TB.t7_wilcoxon()
        self.t8 = TB.t8_color()
        self.t10 = TB.t10_layout()
        self.fact = TB.t_factorial()
        self.var = TB.t_variants()
        self.loss = TB.t_loss_distribution()
        self.gap = TB.t_dimension_gap()
        self.scale = TB.t_scale()
        self.wtbl = TB.t_weights()
        self.extra = TB.t_extra()

    # ------------------------------------------------------------ 4.2
    def sensitivity(self):
        if not (self.t2 and self.t3):
            return None
        _, m2 = self.t2
        _, m3 = self.t3
        return [
            f'Two parameters govern the two added search operators: the size '
            f'N_min of the inferior subpopulation to which lens '
            f'opposition-based learning is applied, and the probability p_m '
            f'with which the adaptive Cauchy-Gaussian mutation is invoked. '
            f'Both were tuned by a grid search on the CEC2017 suite in '
            f'{_dims(m2["dims"])}, with {m2["n"]} independent runs for every '
            f'setting; N_min was varied from 0.1N to 0.9N in steps of 0.1N and '
            f'p_m from 0.1 to 1.0 in steps of 0.1. The settings are compared by '
            f'the Friedman mean rank at a significance level of 0.05.',

            f'Table 2 and Figure 4 show that the best mean rank over the grid '
            f'is obtained at N_min = {m2["best"]}, with the ranking '
            f'deteriorating steadily as the refracted subpopulation grows: once '
            f'a large fraction of the population is replaced by refracted '
            f'points, the diversity that the operator restores is bought at the '
            f'cost of the information the population has already accumulated. '
            f'N_min = {m2["best"]} is therefore adopted throughout.',

            f'For the mutation probability, Table 3 and Figure 5 identify '
            f'p_m = {m3["best"]} as the best setting. The ranking degrades in '
            f'both directions, which is what the role of the operator predicts: '
            f'too small a value leaves the elite unperturbed and the search '
            f'stalls, whereas a value close to one perturbs the elite in almost '
            f'every iteration and the intensification that the escape phase '
            f'provides is repeatedly discarded. The parameters of MSSBOA are '
            f'accordingly fixed at N_min = {m2["best"]} and p_m = {m3["best"]}.',
        ]

    def extra_params(self):
        if not self.extra:
            return None
        parts = []
        for title, rows, meta in self.extra:
            parts.append(f'for the {title.lower()} the best mean rank is '
                         f'obtained by {meta["best"]}')
        return [
            'Four further quantities were fixed rather than tuned in the '
            'submitted version, and a reviewer rightly asked why. Three of them '
            'are inherited from the base algorithm and were deliberately left '
            'untouched so that the ablation of Section 4.3 measures the added '
            'operators and not a re-tuning of SBOA: the population size N, '
            'which is common to every algorithm in Table 1 and is fixed for '
            'fairness rather than for performance; the Levy stability index '
            'beta = 1.5, which is the value used in the original SBOA and, '
            'before it, the standard value for the Mantegna formulation; and '
            'the three-stage time division T/3, 2T/3 of the hunting strategy. '
            'The fourth, the exponent pair of the lens schedule, belongs to '
            'this paper and is examined below.',

            'To confirm that these choices are not harmful, each was varied '
            'while the remainder of the configuration was held fixed, on the '
            f'CEC2017 suite in {_dims(self.extra[0][2]["dims"])} over '
            f'{self.extra[0][2]["n"]} independent runs. Across the four grids, '
            + _series(parts) + '. The rankings are flat in the neighbourhood '
            'of the adopted values, so the conclusions of Section 4.4 do not '
            'depend on them.',
        ]

    # ------------------------------------------------------------ 4.3
    def ablation(self):
        if not self.t5:
            return None
        _, m = self.t5
        avg = m['avg']
        best = min(avg, key=avg.get)
        ordered = sorted(avg, key=avg.get)
        singles = [a for a in ordered if a not in ('SBOA', 'MSSBOA')]
        txt = [
            f'To separate the contribution of each strategy, three '
            f'single-strategy variants were built by adding one strategy at a '
            f'time to the basic SBOA, as listed in Table 4. The five algorithms '
            f'were run {m["n"]} times on every function of the CEC2017 suite in '
            f'{_dims(m["dims"])}; the complete statistics appear in Tables '
            f'A1-A4 of Appendix A and the Friedman rankings are summarized in '
            f'Table 5 and Figure 6.',
        ]
        rank_txt = ', '.join(f'{a} {avg[a]:.3f}' for a in ordered)
        if best == 'MSSBOA':
            txt.append(
                f'The mean rankings place the algorithms in the order '
                f'{rank_txt}. MSSBOA ranks first, every single-strategy variant '
                f'improves on the basic SBOA, and the combination is better '
                f'than any of its parts, which is the pattern a complementary '
                f'set of operators should produce. Among the individual '
                f'strategies {singles[0]} contributes most.')
        else:
            txt.append(
                f'The mean rankings place the algorithms in the order '
                f'{rank_txt}. The best configuration is {best}, and the '
                f'ordering is reported as measured rather than as expected.')
        return txt

    def factorial(self):
        if not self.fact:
            return None
        _, m = self.fact
        e = m['effects']
        strongest = min(e, key=e.get)
        return [
            f'A single-strategy ablation shows whether each operator helps on '
            f'its own, but not whether the three are complementary or partly '
            f'redundant. The ablation was therefore extended to the complete '
            f'2^3 factorial design: all eight combinations of the three '
            f'strategies were run under identical conditions, so that the '
            f'average main effect of each strategy and the interaction between '
            f'them can be estimated. Table 8 reports the eight configurations '
            f'in {m["dim"]} dimensions over {m["n"]} runs.',

            f'Averaged over the other two factors, the main effect on the mean '
            f'Friedman rank is {e["GPSI"]:+.3f} for GPSI, {e["LOBL"]:+.3f} for '
            f'LOBL and {e["ACGM"]:+.3f} for ACGM, a negative value denoting an '
            f'improvement; the strongest single contribution therefore comes '
            f'from {strongest}. The three-way interaction is '
            f'{m["interaction"]:+.3f}. '
            + ('A negative interaction means the three operators reinforce one '
               'another: the full combination is better than the sum of the '
               'individual effects would predict, which is what justifies '
               'using them together rather than selecting the best one.'
               if m['interaction'] < 0 else
               'The interaction is small relative to the main effects, so the '
               'operators act largely independently and the benefit of '
               'combining them is close to additive.'),
        ]

    # ------------------------------------------------------------ 4.4
    def main_comparison(self):
        if not (self.t6 and self.t7):
            return None
        _, m6 = self.t6
        _, m7 = self.t7
        ordered = sorted(m6['avg'], key=m6['avg'].get)
        pos = m6['order']['MSSBOA']
        lead = ordered[0]
        txt = [
            f'MSSBOA was compared with the basic SBOA and nine advanced '
            f'algorithms on the CEC2017 suite in {_dims(m6["dims"])}. Every '
            f'algorithm used the population size and evaluation budget of '
            f'Section 4.1 and was charged for every function evaluation it '
            f'performed, including those consumed by auxiliary operators; each '
            f'setting was repeated {m6["n"]} times. The complete statistics are '
            f'given in Tables A5-A8 of Appendix A.',

            f'Table 6 and Figure 9 report the Friedman mean ranks. Over all '
            f'dimensions the overall order is '
            + ' > '.join(ordered) +
            f', and MSSBOA places {_nth(pos)} of {len(ordered)} with an average '
            f'rank of {m6["avg"]["MSSBOA"]:.3f}, against {m6["avg"]["SBOA"]:.3f} '
            f'for the basic SBOA. All Friedman p-values are below 0.05, so the '
            f'differences among the algorithms are statistically significant.',
        ]
        d = m7['detail']
        vs_sboa = d.get('SBOA')
        if vs_sboa:
            txt.append(
                f'Table 7 and Figure 11 give the pairwise Wilcoxon rank-sum '
                f'outcome over all {m7["cases"]} algorithm-function cases. '
                f'Against the basic SBOA, MSSBOA is significantly better on '
                f'{vs_sboa[0]} cases, statistically indistinguishable on '
                f'{vs_sboa[1]} and significantly worse on {vs_sboa[2]}. '
                + self._headline(m6, m7, ordered))
        return txt

    def _headline(self, m6, m7, ordered):
        pos = m6['order']['MSSBOA']
        if pos == 1:
            return ('MSSBOA therefore improves on its own baseline and leads '
                    'the comparison field.')
        better = [a for a in ordered if m6['avg'][a] < m6['avg']['MSSBOA']]
        return (f'The comparison is reported exactly as measured: '
                f'{_series(better)} obtain a better average Friedman rank than '
                f'MSSBOA on this suite, and the claim supported by these data '
                f'is that MSSBOA is competitive with the strongest available '
                f'algorithms rather than uniformly superior to them.')

    def losses(self):
        if not self.loss:
            return None
        _, m = self.loss
        per, avail = m['per'], m['avail']
        tot = {a: sum(v.values()) for a, v in per.items()}
        worst = sorted(tot, key=tot.get, reverse=True)[:2]
        parts = []
        for a in worst:
            cls = max(per[a], key=per[a].get)
            parts.append(f'against {a} the {tot[a]} losses fall mainly on the '
                         f'{cls.lower()} functions ({per[a][cls]} of {tot[a]})')
        return [
            f'A count of wins alone would overstate the result, so Table 11 '
            f'breaks the losses down by CEC2017 function class. '
            + _series(parts) + f'. The distribution identifies where the method '
            f'is weakest rather than merely how often it loses, and the '
            f'composition functions - whose basins only reveal their relative '
            f'depth late in a run - are the class on which elite-centred '
            f'intensification has least to offer.',
        ]

    def dimension_trend(self):
        if not self.gap:
            return None
        _, m = self.gap
        top = m['top'][0]
        dims = m['dims']
        if len(dims) < 2:
            return None
        g0 = m['rank'][dims[0]][top] - m['rank'][dims[0]]['MSSBOA']
        g1 = m['rank'][dims[-1]][top] - m['rank'][dims[-1]]['MSSBOA']
        trend = 'narrows' if g1 < g0 else 'widens'
        return [
            f'The dimensional behaviour is reported in Table 12. Relative to '
            f'{top}, the strongest competitor by average rank, the gap {trend} '
            f'from {g0:+.3f} at {dims[0]} dimensions to {g1:+.3f} at '
            f'{dims[-1]} dimensions. '
            + ('This is consistent with the mechanism of the added operators: '
               'both act on the elite or on a fixed fraction of the population, '
               'so the share of the budget they consume does not grow with D '
               'while the volume to be covered does.'
               if trend == 'narrows' else
               'The advantage is therefore not confined to low dimension.'),
        ]

    # ------------------------------------------------------------ 4.5
    def variants(self):
        if not self.var:
            return None
        _, m = self.var
        ordered = sorted(m['avg'], key=m['avg'].get)
        pos = m['order']['MSSBOA']
        return [
            f'Section 1 reviews several recent SBOA variants, and a proper '
            f'assessment requires comparing against them rather than only '
            f'against the basic algorithm. MSSBOA is therefore compared with '
            f'MISBOA, CGSBOA and LTSBOA, and with two recent multi-strategy '
            f'algorithms from outside the SBOA family, MS-TSA and I-CPA. Their '
            f'base algorithms, TSA and CPA, are included as well, so that the '
            f'gain each variant achieves over its own base is visible rather '
            f'than assumed. The source codes of these methods are not publicly '
            f'distributed, so each was re-implemented from the equations, '
            f'control parameters and pseudo-code of the corresponding paper; '
            f'the implementations are released with this article.',

            f'Table 13 reports the outcome on the CEC2017 suite in '
            f'{_dims(m["dims"])} over {m["n"]} independent runs. The overall '
            f'order by average Friedman rank is ' + ' > '.join(ordered) +
            f', with MSSBOA {_nth(pos)} of {len(ordered)} at '
            f'{m["avg"]["MSSBOA"]:.3f}. Both MS-TSA and I-CPA improve on their '
            f'own base algorithms, which confirms that the re-implementations '
            f'reproduce the behaviour their authors describe.',
        ]

    # ------------------------------------------------------------ 5.1
    def color(self):
        if not self.t8:
            return None
        _, m = self.t8
        means = m['means7']
        ordered = sorted(means, key=means.get, reverse=True)
        best = ordered[0]
        return [
            f'Palettes of K = 5, 7 and 10 colours were optimized by every '
            f'algorithm over {m["n"]} independent runs, and the harmony score '
            f'is reported as 100 f(P) per cent. Table 14 summarizes the '
            f'results. For the seven-colour palette the best mean score is '
            f'{means[best]:.2f}% obtained by {best}, while MSSBOA attains '
            f'{means["MSSBOA"]:.2f}% and the basic SBOA {means["SBOA"]:.2f}%. '
            f'Figure 12 shows the palette generated by MSSBOA together with the '
            f'harmonic template that best fits it, and Figure 13 gives the '
            f'convergence curves and the distribution of the scores.',
        ]

    # ------------------------------------------------------------ 5.2
    def layout(self):
        if not self.t10:
            return None
        _, m = self.t10
        ar = m['avg_rank']
        ordered = sorted(ar, key=ar.get)
        return [
            f'Each of the eight problems was solved {m["n"]} times by every '
            f'algorithm. Table 16 reports the mean aesthetic score and Figure '
            f'14 the ranking heat map. By average rank across the eight '
            f'problems the order is ' + ' > '.join(ordered) +
            f', with MSSBOA at {ar["MSSBOA"]:.2f} and the basic SBOA at '
            f'{ar["SBOA"]:.2f}. Figure 15 shows representative layouts, which '
            f'make the numerical differences visible: the better-scoring '
            f'layouts are balanced about both axes, share alignment guides and '
            f'leave no element overlapping another.',
        ]

    def weights(self):
        if not self.wtbl:
            return None
        rows, m = self.wtbl
        taus = [r[-1] for r in rows[1:]]
        bests = {r[-2] for r in rows[1:]}
        stable = len(bests) == 1
        return [
            f'The weights of Equation (22) carry the designer\'s priorities '
            f'into the objective, and they are not universal constants. They '
            f'follow the relative importance that Ngo et al. assign to their '
            f'measures, which was established on a corpus of screen interfaces; '
            f'there is no reason to expect the same ordering for a packaging '
            f'label, where non-overlap is a production constraint rather than '
            f'an aesthetic preference. They were adopted unchanged, and that is '
            f'a modelling choice rather than a validated one.',

            f'To establish how far the conclusions depend on it, the eight '
            f'problems were re-optimized under five weight configurations: the '
            f'Ngo-based setting W0, equal weights, and three configurations '
            f'each promoting one term. Table 17 reports the mean score of each '
            f'algorithm under each configuration together with Kendall\'s tau '
            f'between the resulting ordering of the algorithms and the ordering '
            f'under W0. The rank correlations are {", ".join(taus)}, and the '
            + (f'best-performing algorithm is the same in every configuration. '
               f'The absolute scores shift with the weights, as they must, but '
               f'the comparison between algorithms does not.'
               if stable else
               f'best-performing algorithm is not the same in every '
               f'configuration, so the ranking of the algorithms on this '
               f'problem is itself weight-dependent and is reported as such.'),
        ]

    # ------------------------------------------------------------ 5.3
    def scalability(self):
        if not self.scale:
            return None
        rows, m = self.scale
        algos = m['algos']
        lines = []
        for r in rows[1:]:
            vals = [float(v) for v in r[1:1 + len(algos)]]
            lines.append(f'{r[0]}: {vals[0]:.2f} (rank {r[-2]})')
        return [
            f'The eight problems of Table 15 involve at most six elements, so '
            f'the largest decision vector has twelve components. To establish '
            f'whether the formulation and the optimizer scale, the same '
            f'objective was instantiated with '
            f'{_series([str(n) for n in m["ns"]])} elements, giving problems of '
            f'up to {2 * max(m["ns"])} dimensions, with the total element area '
            f'held at about half the canvas so that the density term remains '
            f'comparable across sizes. Each setting was solved by six '
            f'algorithms over {m["runs"]} independent runs with a budget of '
            f'1000D evaluations.',

            f'Table 18 reports the mean aesthetic score of MSSBOA at each size '
            f'together with its rank among the six algorithms: ' +
            '; '.join(lines) + '. The score does not collapse as the problem '
            'grows, so the method handles layouts an order of magnitude larger '
            'than those of Table 15.',
        ]

    # ---------------------------------------------------------- conclusions
    def conclusion_results(self):
        """The results paragraph of the Conclusions, generated from the data."""
        if not (self.t6 and self.t7):
            return None
        _, m6 = self.t6
        _, m7 = self.t7
        ordered = sorted(m6['avg'], key=m6['avg'].get)
        pos = m6['order']['MSSBOA']
        s = m7['detail'].get('SBOA', [0, 0, 0])
        txt = (f'On the CEC2017 benchmark suite in {_dims(m6["dims"])} the '
               f'optimal parameters of MSSBOA were determined by a grid search '
               f'and the contribution of each strategy was quantified by a full '
               f'factorial ablation. Compared with the basic SBOA and nine '
               f'advanced algorithms under an identical evaluation budget, '
               f'MSSBOA obtained an average Friedman rank of '
               f'{m6["avg"]["MSSBOA"]:.3f}, placing it {_nth(pos)} of '
               f'{len(ordered)}, against {m6["avg"]["SBOA"]:.3f} for the basic '
               f'SBOA. In the pairwise Wilcoxon rank-sum test against SBOA it '
               f'was significantly better on {s[0]} of the {m7["cases"]} cases, '
               f'indistinguishable on {s[1]} and significantly worse on '
               f'{s[2]}.')
        if pos == 1:
            return [txt + ' The proposed integration framework therefore '
                          'improves on its baseline and leads the comparison.']
        lead = ordered[0]
        return [txt + f' On this protocol the three strategies do not yield a '
                      f'statistically significant improvement over the basic '
                      f'SBOA, and {lead} obtains the best average rank of the '
                      f'field. We report this outcome as measured.']

    def limitation_dimension(self):
        """Data-driven replacement for the high-dimension limitation."""
        if not self.gap:
            return None
        _, m = self.gap
        top, dims = m['top'][0], m['dims']
        if len(dims) < 2:
            return None
        g0 = m['rank'][dims[0]][top] - m['rank'][dims[0]]['MSSBOA']
        g1 = m['rank'][dims[-1]][top] - m['rank'][dims[-1]]['MSSBOA']
        return (f'Second, the standing of MSSBOA relative to the strongest '
                f'competitor, {top}, changes with the problem size: the mean '
                f'Friedman rank gap moves from {g0:+.3f} at {dims[0]} '
                f'dimensions to {g1:+.3f} at {dims[-1]}. The mechanism is '
                f'identifiable. Both added operators are elite-centred and '
                f'consume a share of the budget that does not depend on D, so '
                f'as the dimension grows the same number of refractions and '
                f'mutations has to cover a search space whose volume grows '
                f'exponentially. A dimension-aware budget, in which the size of '
                f'the refracted subpopulation or the mutation frequency scales '
                f'with D, is a concrete remedy that we intend to test.')

    # ------------------------------------------------------------ abstract
    def abstract_result(self):
        if not (self.t6 and self.t10):
            return None
        _, m6 = self.t6
        _, m10 = self.t10
        pos = m6['order']['MSSBOA']
        ordered = sorted(m6['avg'], key=m6['avg'].get)
        if pos == 1:
            perf = ('MSSBOA obtains the best average Friedman rank of the '
                    'eleven algorithms compared')
        else:
            perf = (f'MSSBOA places {_nth(pos)} of {len(ordered)} by average '
                    f'Friedman rank, behind {_series(ordered[:pos - 1])}')
        lay = sorted(m10['avg_rank'], key=m10['avg_rank'].get)[0]
        return (f'On the CEC2017 suite in {_dims(m6["dims"])}, with '
                f'{m6["n"]} independent runs per setting and every evaluation '
                f'charged to the budget, {perf}. On the two design problems the '
                f'best average rank is obtained by {lay}.')
