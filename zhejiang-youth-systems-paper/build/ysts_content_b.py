# -*- coding: utf-8 -*-
"""Manuscript content, part B: results, discussion, conclusions, back matter."""

PART_B = [

    # =====================================================================
    ('h1', '4. Results'),

    ('h2', '4.1. Baseline Behaviour and Validation'),

    ('p', 'Figure 3 and Table 5 report the baseline run under unchanged structure. Three '
          'features deserve emphasis. First, the model reproduces the observed '
          'deterioration without any exogenous deterioration being imposed on it: the '
          'youth non-employment rate rises from 0.117 in 2015 to 0.178 in 2025, the '
          'slow-employment share of entrants from 0.060 to 0.191, and the vertical '
          'mismatch share from 0.178 to 0.243, all within 1.7 per cent of their published '
          'counterparts. Second, this happens while the market remains tight: the '
          'vacancy-to-seeker ratio falls only from 1.53 to 1.43 over the same decade, and '
          'is 1.36 in 2040. The system generates rising non-employment in a market '
          'that never becomes slack, which is the empirical puzzle set out in Section 1. '
          'Third, the mechanism is visible in panel (c). Employability capital is '
          'essentially flat, moving from 0.592 to 0.596 across twenty-five years, because '
          'cohort renewal continually replenishes it. What moves is the employer '
          'threshold, from 0.527 to 0.857. The skill–threshold gap consequently narrows, '
          'changes sign in 2021, and reaches −0.261 by 2040.'),

    ('figure', 'fig3_baseline.png', 6.55, None, 103),
    ('figcap', 3, 'Baseline behaviour, 2015–2040. (a) The realised non-employment rate '
                  'against its instantaneous (frozen-driver) equilibrium; circles are '
                  'published benchmarks. (b) Slow-employment and mismatch shares against '
                  'their 2025 benchmarks. (c) The employer threshold rises while '
                  'employability capital stays flat and aspirations fall, so the '
                  'skill–threshold gap changes sign in 2022. (d) Queue congestion on a '
                  'logarithmic scale against the vacancy-to-seeker ratio.'),

    ('tabcap', 5, 'Baseline trajectory of the calibrated system under unchanged '
                  'structure.'),
    ('table', [
        ['Year', 'NER', 'SE flow', 'Mismatch', 'Duration (yr)', 'Queue ratio',
         'Threshold ⟪\\theta⟫', 'Capital ⟪H⟫', 'Aspiration ⟪A⟫', 'Gap ⟪x⟫', 'Tightness'],
        ['2015', '0.117', '0.060', '0.178', '0.72', '35.7', '0.527', '0.592', '0.651',
         '+0.066', '1.53'],
        ['2020', '0.137', '0.097', '0.197', '0.84', '48.1', '0.581', '0.593', '0.643',
         '+0.012', '1.56'],
        ['2025', '0.178', '0.191', '0.243', '1.22', '96.3', '0.652', '0.590', '0.620',
         '−0.062', '1.43'],
        ['2030', '0.261', '0.380', '0.301', '2.28', '237.2', '0.730', '0.587', '0.587',
         '−0.143', '1.33'],
        ['2035', '0.390', '0.517', '0.360', '4.78', '496.3', '0.801', '0.590', '0.555',
         '−0.211', '1.34'],
        ['2040', '0.517', '0.542', '0.411', '8.63', '753.8', '0.857', '0.596', '0.531',
         '−0.261', '1.36'],
    ], [700, 800, 900, 950, 1150, 1000, 1050, 950, 1050, 800, 1000]),
    ('notes', 'NER is the youth non-employment rate; SE flow is the share of each '
              'entering cohort that chooses delayed entry. The 2030–2040 values are a '
              'structure-unchanged counterfactual, not a forecast: they describe where '
              'the present configuration of feedbacks leads if nothing in it changes.'),

    ('h2', '4.2. The Attractor Moves and the State Lags It'),

    ('p', 'Panel (a) of Figure 3 plots, alongside the realised trajectory, the '
          'instantaneous equilibrium of the system—the state to which it would converge '
          'if the exogenous drivers were frozen at their values in that year. This moving '
          'attractor rises from a non-employment rate of 0.117 in 2015 to 0.187 in 2025 '
          'and 0.637 in 2040. The realised state never reaches it. By 2040 the vertical '
          'gap between the two is 0.120, and the horizontal lag—the number of years by '
          'which the realised state trails the attractor—averages 1.72 years over the '
          'period and reaches 5.00 years at the end of the horizon.'),

    ('p', 'This is not a modelling artefact but a direct consequence of the system’s '
          'time constants. The eigenvalues of the Jacobian at the 2040 fixed point are '
          'all real and negative (Table 6), so the fixed point is a stable node, but they '
          'differ by a factor of twenty. The slowest mode has a relaxation time of '
          'exactly eight years, equal to the reciprocal of the exit rate from the youth '
          'window: the system cannot adjust faster than a cohort can pass through it. '
          'Two further modes have relaxation times of 5.78 years. Since a first-order '
          'system requires roughly three time constants to complete 95 per cent of its '
          'adjustment, the transition system needs about a quarter of a century to '
          'express fully any change in its structure. The practical implication is that '
          'measured youth non-employment is a lagging indicator of structural '
          'deterioration by a knowable margin, and that policy evaluated on a three- or '
          'five-year horizon will systematically under-record both the damage already '
          'accumulated and the benefit of any correction.'),

    ('tabcap', 6, 'Eigenvalue spectrum of the frozen-driver system at 2040 and the '
                  'associated relaxation times.'),
    ('table', [
        ['Mode', 'Eigenvalue (yr⁻¹)', 'Relaxation time (yr)', 'Interpretation'],
        ['⟪\\lambda_{1}⟫', '−2.459', '0.41', 'Search-flow equilibration'],
        ['⟪\\lambda_{2}⟫', '−1.752', '0.57', 'Aspiration and offer adjustment'],
        ['⟪\\lambda_{3}⟫', '−0.401', '2.49', 'Queue turnover'],
        ['⟪\\lambda_{4}⟫', '−0.173', '5.78', 'Mismatched-employment turnover'],
        ['⟪\\lambda_{5}⟫', '−0.173', '5.78', 'Matched-employment turnover'],
        ['⟪\\lambda_{6}⟫', '−0.125', '8.00', 'Cohort passage through the youth window'],
    ], [1300, 2200, 2400, 3740]),
    ('notes', 'All eigenvalues are real and negative, so the fixed point is a stable '
              'node. The slowest mode equals ⟪-\\omega⟫ exactly.'),

    ('h2', '4.3. No Fold, No Hysteresis: A Negative Result'),

    ('p', 'A natural hypothesis, and the one we began with, is that the transition system '
          'possesses two stable regimes—a fluid one and a trapped one—separated by an '
          'unstable threshold, so that a sufficiently large disturbance would flip it '
          'irreversibly. The hypothesis is not supported. Two-directional continuation in '
          'the threshold sensitivity ⟪\\kappa⟫ over [0.5, 5.0] and in the value of an '
          'institutional post ⟪\\Pi⟫ over [0.4, 2.6] produces forward and backward '
          'branches that coincide to within 10⁻¹⁴ in non-employment rate at every grid '
          'point at which both sweeps converge (241 of 241 points for ⟪\\kappa⟫ and 232 '
          'of 241 for ⟪\\Pi⟫), so no fold and no hysteresis loop exists in either '
          'direction (Figure 4a). A multi-start search from six widely separated initial '
          'guesses across forty parameter cells—a 6 × 4 grid spanning endogenous '
          'threshold escalation from 0 to 2.5 and screening sharpness from 3 to 22, plus '
          'eight values each of ⟪\\kappa⟫ and ⟪\\Pi⟫—returns exactly one admissible '
          'fixed point in every cell.'),

    ('p', 'The system is therefore globally monostable over the region examined, and the '
          'language of tipping points, critical transitions and early-warning signals '
          '{{scheffer2009}} does not apply to it. This is worth stating explicitly '
          'because that language has become common in policy discussion of youth '
          'exclusion. What generates persistence here is not multiplicity of equilibria '
          'but the conjunction of a monotonically drifting attractor with a slow state, '
          'which produces behaviour that superficially resembles a trap—deterioration '
          'that does not reverse itself—without any of a trap’s formal properties, a pattern '
          'also visible in empirical work on the slow evolution of human-capital '
          'mismatch and youth employment quality in Chinese regions '
          '{{zhao2023|liang2024}}. The '
          'distinction matters for policy: in a bistable system the objective is to '
          'avoid or escape a basin, and timing dominates magnitude; in a drifting '
          'monostable system the objective is to slow or reverse the drift, and sustained '
          'pressure on the driver dominates one-off intervention.'),

    ('figure', 'fig4_structure.png', 6.55, None, 104),
    ('figcap', 4, 'Structural properties. (a) Forward (solid) and backward (dotted) '
                  'continuation in two control parameters; the branches coincide, so no '
                  'fold exists. Circles mark the calibrated values. (b) Excess '
                  'non-employment after a temporary three-year demand shock, with the '
                  'shock window shaded. (c) Relaxation times implied by the eigenvalue '
                  'spectrum at the 2040 fixed point.'),

    ('h2', '4.4. Transitory Shocks Decay; Structural Drift Does Not'),

    ('p', 'To separate cyclical from structural persistence we impose a temporary adverse '
          'demand shock: the elasticity of vacancies to digitalisation is cut by 25 per '
          'cent for three years from 2026, after which the original structure is '
          'restored. The shock is large by historical standards, and its immediate effect '
          'is substantial: excess non-employment peaks at 0.125 in 2029, more than half '
          'the contemporaneous baseline rate. Recovery, however, is brisk. '
          'The excess falls to half its peak within 1.50 years of the shock ending and to '
          '0.0050—about four per cent of the peak—ten years after. Figure 4b shows the '
          'full path.'),

    ('p', 'The contrast with the baseline drift is the substantive point. A large '
          'cyclical disturbance leaves almost no trace after a decade, whereas the slow '
          'upward march of the employer threshold produces a permanent and compounding '
          'deterioration. Youth non-employment in a digital-frontrunner region is '
          'therefore a structural problem wearing cyclical clothes. Counter-cyclical '
          'measures will appear to work—because the cycle would have reverted anyway—and '
          'will leave the underlying trajectory untouched.'),

    ('h2', '4.5. Which Loops Dominate'),

    ('p', 'Loop dominance is assessed by deactivation. Each candidate link is held at its '
          '2015 value, so that the feedback passing through it cannot operate while its '
          'level effect is retained; the resulting change in the 2040 outcome measures '
          'that loop’s contribution to observed behaviour {{ford1999}}. Table 7 reports '
          'the results. The signs recover exactly the polarities derived analytically in '
          'Section 2.3, which is itself a structure-oriented validation test: '
          'deactivating a reinforcing loop lowers non-employment, deactivating a '
          'balancing loop raises it.'),

    ('tabcap', 7, 'Loop-deactivation experiments: contribution of each feedback loop to '
                  'the 2040 outcome.'),
    ('table', [
        ['Loop', 'Polarity', 'Link held at its 2015 value', '2040 NER',
         '⟪\\Delta⟫NER', '⟪\\Delta⟫Duration (yr)', 'Share of total effect'],
        ['B2 Aspiration adjustment', 'Balancing', 'Aspiration level',
         '0.5791', '+0.0618', '+2.55', '30.3%'],
        ['R3 Threshold escalation', 'Reinforcing', 'Observed mismatch share',
         '0.4606', '−0.0567', '−2.28', '27.8%'],
        ['B3 Exam-queue congestion', 'Balancing', 'Realised exam success rate',
         '0.5530', '+0.0357', '+0.84', '17.5%'],
        ['R1 Skill decay while searching', 'Reinforcing', 'Searcher stock in renewal term',
         '0.4883', '−0.0290', '−1.19', '14.2%'],
        ['R4 Thin-market offer quality', 'Reinforcing', 'Offered job quality',
         '0.5061', '−0.0112', '−0.32', '5.5%'],
        ['R2 Queue–skill erosion', 'Reinforcing', 'Skill retention while queueing',
         '0.5079', '−0.0094', '−0.27', '4.6%'],
    ], [2600, 1250, 2600, 900, 900, 1300, 1090]),
    ('notes', 'The baseline 2040 non-employment rate is 0.5173 and the baseline mean '
              'transition duration 8.63 years. A positive ⟪\\Delta⟫ means that '
              'deactivating the loop worsens the outcome, identifying a balancing loop. '
              'Shares are absolute effects normalised to sum to unity.'),

    ('p', 'Three readings follow. First, the two balancing loops together account for '
          'almost half of the total deactivation effect: without aspiration adjustment '
          'and exam-queue congestion the 2040 non-employment rate would be 0.58 and 0.55 '
          'rather than 0.52. Congestion in particular is an unlovely but powerful '
          'brake—the fact that success rates collapse as the queue lengthens is what '
          'stops the queue absorbing the whole cohort. Policies that expand institutional '
          'recruitment without expanding anything else would weaken precisely this brake. '
          'Second, among the reinforcing loops, threshold escalation is the dominant '
          'amplifier by a wide margin, accounting for 27.8 per cent of the total '
          'deactivation effect—six times the queue-erosion loop—and adding 2.28 years to '
          'the mean transition. Third, the two loops most emphasised in the policy '
          'literature, skill decay during search and erosion while queueing, together '
          'account for under nineteen per cent. The scarring mechanism is real but it is '
          'not where the leverage is.'),

    ('h2', '4.6. Uncertainty and Global Sensitivity'),

    ('p', 'Twelve parameters are treated as uncertain over the ranges in Table 2. '
          'Propagating them through a Latin-hypercube design of 4096 draws gives a 2040 '
          'non-employment rate with mean 0.546, standard deviation 0.151 and a 95 per '
          'cent interval of [0.227, 0.795]; the median is 0.558 and the interquartile '
          'range [0.453, 0.662]. Mean transition duration has mean 16.06 years and a 95 '
          'per cent interval of [1.90, 57.28] years, the extreme right skew reflecting '
          'the multiplicative structure of the reinforcing loops. Appendix Table A1 '
          'reports the full distributions. The point to note is how little of the '
          'parameter space is benign: the 2.5th percentile of the 2040 distribution, '
          '0.227, already exceeds the realised 2025 value of 0.178, so under essentially '
          'the entire uncertainty range the system continues to deteriorate rather than '
          'stabilising on its own.'),

    ('p', 'The Sobol decomposition (Table 8, Figure 5a) attributes variance rather than '
          'merely ranking parameters, and the concentration is striking. The sensitivity '
          'of the employer threshold to digitalisation alone accounts for 66.3 per cent '
          'of the total output variance, six times the next parameter. Endogenous '
          'threshold escalation contributes 11.0 per cent, the probability-weighting '
          'curvature 8.9 per cent, cohort growth 7.3 per cent and aspiration anchoring '
          '5.0 per cent. Matching efficiency contributes 3.7 per cent and training '
          'intensity 0.1 per cent. First- and total-order indices sum to 0.927 and 1.062 '
          'respectively, so the response surface is close to additive and interaction '
          'effects account for roughly six per cent of the variance. Taken together, the '
          'two threshold parameters explain more than three quarters of everything the '
          'model does not know.'),

    ('tabcap', 8, 'Sobol variance decomposition of the 2040 non-employment rate '
                  '(base sample 1024; 14,336 model evaluations; 800 bootstrap '
                  'resamples).'),
    ('table', [
        ['Parameter', 'Meaning', 'First order ⟪S_{i}⟫', '95% CI',
         'Total order ⟪S_{Ti}⟫', '95% CI'],
        ['⟪\\kappa⟫', 'Threshold sensitivity to digitalisation', '0.583',
         '[0.352, 0.850]', '0.663', '[0.611, 0.721]'],
        ['⟪\\kappa_{2}⟫', 'Endogenous threshold escalation', '0.099',
         '[−0.005, 0.208]', '0.110', '[0.099, 0.122]'],
        ['⟪\\varepsilon⟫', 'Probability-weighting curvature', '0.060',
         '[−0.038, 0.158]', '0.089', '[0.078, 0.100]'],
        ['⟪g_{\\Phi}⟫', 'Graduate cohort growth', '0.076', '[−0.010, 0.164]', '0.073',
         '[0.067, 0.081]'],
        ['⟪\\zeta⟫', 'Aspiration anchoring weight', '0.059', '[−0.017, 0.131]', '0.050',
         '[0.045, 0.057]'],
        ['⟪\\mu⟫', 'Matching efficiency', '0.035', '[−0.029, 0.099]', '0.037',
         '[0.033, 0.041]'],
        ['⟪\\Pi⟫', 'Perceived value of a public post', '0.001', '[−0.048, 0.045]',
         '0.019', '[0.015, 0.022]'],
        ['⟪\\delta_{H}⟫', 'Skill decay while searching', '0.006', '[−0.033, 0.046]',
         '0.015', '[0.013, 0.017]'],
        ['⟪\\phi⟫', 'Vacancy elasticity to digitalisation', '0.003', '[−0.016, 0.021]',
         '0.003', '[0.003, 0.004]'],
        ['⟪\\chi⟫', 'Skill retention while queueing', '0.002', '[−0.010, 0.013]',
         '0.001', '[0.001, 0.002]'],
        ['⟪\\lambda⟫', 'Aspiration adjustment speed', '0.000', '[−0.011, 0.013]', '0.001',
         '[0.001, 0.001]'],
        ['⟪\\tau⟫', 'Training intensity', '0.003', '[−0.007, 0.013]', '0.001',
         '[0.001, 0.001]'],
        ['Sum', '', '0.927', '', '1.062', ''],
    ], [1150, 3350, 1450, 1450, 1350, 1490]),
    ('notes', 'Slightly negative lower bounds on small first-order indices are a known '
              'small-sample property of the Saltelli estimator and indicate indices '
              'statistically indistinguishable from zero. The excess of the total-order '
              'sum over unity measures interaction.'),

    ('p', 'The policy reading of Table 8 is uncomfortable for the standard toolkit. The '
          'two parameters that public programmes address most directly—training intensity '
          'and, through hiring subsidies, the vacancy elasticity—jointly explain three '
          'tenths of one per cent of the outcome variance. The parameters that dominate '
          'describe how employers set the bar, how young people weight small probabilities, '
          'and how firmly aspirations are anchored. None of these is conventionally '
          'treated as a policy variable, and all three are in principle governable.'),

    ('h2', '4.7. What Separates Trapped from Fluid Futures'),

    ('p', 'To characterise the boundary between good and bad futures we define a binary '
          'outcome—a 2040 non-employment rate above 0.36, twice the 2025 benchmark—and '
          'model it on the twelve standardised parameters. In the Monte Carlo sample 86.5 '
          'per cent of draws cross that line, which is itself a result: under the great '
          'majority of the uncertainty range the rate at least doubles within fifteen '
          'years. The logistic meta-model (Table 9) fits extremely well: area under the '
          'receiver operating characteristic curve 0.998, Nagelkerke pseudo-⟪R^{2}⟫ '
          '0.928, McFadden 0.895, likelihood-ratio ⟪\\chi^{2}⟫(12) = 2900.56 with '
          '⟪p⟫ < 0.001. Calibration is excellent: the Hosmer–Lemeshow statistic is 4.07 '
          'on eight degrees of freedom with ⟪p⟫ = 0.851, so the null of good fit is not '
          'rejected.'),

    ('tabcap', 9, 'Logistic meta-model of trap risk in the Monte Carlo sample '
                  '(⟪n⟫ = 4096; outcome: 2040 non-employment rate above 0.36).'),
    ('table', [
        ['Parameter', 'Coefficient', 'SE', '⟪z⟫', '⟪p⟫', 'Odds ratio', '95% CI'],
        ['⟪\\kappa⟫ Threshold sensitivity', '+13.125', '0.996', '+13.17', '<0.001',
         '5.0 × 10⁵', '[7.1 × 10⁴, 3.5 × 10⁶]'],
        ['⟪\\varepsilon⟫ Probability weighting', '−7.046', '0.550', '−12.80', '<0.001',
         '0.001', '[0.000, 0.003]'],
        ['⟪\\kappa_{2}⟫ Endogenous escalation', '+4.560', '0.369', '+12.35', '<0.001',
         '95.6', '[46.4, 197.2]'],
        ['⟪g_{\\Phi}⟫ Cohort growth', '+4.461', '0.363', '+12.27', '<0.001', '86.5',
         '[42.5, 176.4]'],
        ['⟪\\zeta⟫ Aspiration anchoring', '+3.905', '0.326', '+12.00', '<0.001', '49.7',
         '[26.2, 94.0]'],
        ['⟪\\Pi⟫ Value of a public post', '+2.957', '0.267', '+11.10', '<0.001', '19.2',
         '[11.4, 32.4]'],
        ['⟪\\mu⟫ Matching efficiency', '−2.615', '0.240', '−10.89', '<0.001', '0.073',
         '[0.046, 0.117]'],
        ['⟪\\delta_{H}⟫ Skill decay', '+1.800', '0.199', '+9.02', '<0.001', '6.05',
         '[4.09, 8.94]'],
    ], [3050, 1350, 900, 900, 900, 1200, 1940]),
    ('notes', 'Coefficients are per standard deviation of the corresponding prior. The '
              'four parameters with the smallest absolute ⟪z⟫ statistics '
              '(⟪\\phi⟫, ⟪\\tau⟫, ⟪\\lambda⟫, ⟪\\chi⟫) are omitted for space and '
              'are reported in Appendix Table A2. Model fit: AUC 0.998; Nagelkerke '
              '⟪R^{2}⟫ 0.928; Hosmer–Lemeshow ⟪\\chi^{2}⟫ = 4.07, ⟪p⟫ = 0.851.'),

    ('p', 'A cross-validated classification tree recovers the same ordering in '
          'interpretable form (cross-validated AUC 0.923, fifteen leaves). The root split '
          'is on the threshold sensitivity at ⟪\\kappa⟫ = 1.456, and the calibrated '
          'value of 1.855 lies above it, that is, the estimated economy sits in the '
          'high-risk branch of the tree rather than on the boundary. Within the low-risk '
          'branch the next split is on the probability-weighting curvature at 0.526 and '
          'thereafter on endogenous escalation at 0.106 and on cohort growth at 0.047; '
          'within the high-risk branch the tree splits again on ⟪\\kappa⟫ at 1.758 and '
          'then on cohort growth at 0.054 and aspiration anchoring at 0.612 and 0.507. '
          'The structure of the decision rules therefore reproduces, in a calibrated '
          'dynamic model of the Chinese transition system, the threshold-type '
          'relationships that Grigorescu and colleagues detected cross-sectionally in '
          'European NEET data {{grigorescu2025}}.'),

    ('figure', 'fig5_sensitivity.png', 6.55, None, 105),
    ('figcap', 5, 'Uncertainty and sensitivity. (a) Sobol first- and total-order indices '
                  'for the 2040 non-employment rate with bootstrap 95 per cent intervals. '
                  '(b) Monte Carlo distribution of the 2040 non-employment rate; dotted '
                  'lines mark the 2.5th and 97.5th percentiles and the dashed line the '
                  'trap threshold. (c) Standardised logistic coefficients for trap risk '
                  'with 95 per cent intervals.'),

    ('h2', '4.8. Policy Experiments at Equal Effort'),

    ('p', 'Five instrument families are compared at one prior standard deviation of '
          'effort each, introduced in 2025 and evaluated on the 2040 outcome, with '
          'parameter uncertainty propagated through 400 Latin-hypercube draws so that '
          'each comparison is within-draw and paired. Table 10 and Figure 6 report the '
          'results. Differences across instruments are highly significant '
          '(Kruskal–Wallis ⟪H⟫ = 245.22, ⟪p⟫ = 7.0 × 10⁻⁵²), and every instrument '
          'improves on the baseline in every draw (Wilcoxon signed-rank ⟪p⟫ < 10⟪^{-60}⟫ '
          'throughout), so the interesting question is not whether they work but by how '
          'much.'),

    ('tabcap', 10, 'Policy experiments at one prior standard deviation of effort '
                   '(400 paired draws; baseline mean 2040 non-employment rate 0.5441).'),
    ('table', [
        ['Instrument', 'Parameter moved', '⟪\\Delta⟫NER', '95% interval',
         '⟪\\Delta⟫Duration (yr)', 'Cliff’s ⟪\\delta⟫', 'Relative to P4'],
        ['P5 Threshold moderation', '⟪\\kappa⟫ ↓, ⟪\\kappa_{2}⟫ ↓', '−0.1565',
         '[−0.2403, −0.0857]', '−9.77', '1.00', '19.1×'],
        ['P3 Expectation guidance', '⟪\\lambda⟫ ↑, ⟪\\zeta⟫ ↓', '−0.0283',
         '[−0.0621, −0.0098]', '−1.67', '1.00', '3.5×'],
        ['P2 Matching efficiency', '⟪\\mu⟫ ↑', '−0.0264', '[−0.0428, −0.0160]', '−1.84',
         '1.00', '3.2×'],
        ['P4 Vacancy creation', '⟪\\phi⟫ ↑', '−0.0082', '[−0.0131, −0.0046]', '−0.55',
         '1.00', '1.0×'],
        ['P1 Skill upgrading', '⟪\\tau⟫ ↑', '−0.0039', '[−0.0087, −0.0015]', '−0.35',
         '1.00', '0.5×'],
    ], [2650, 2100, 1150, 1750, 1400, 1050, 1240]),
    ('notes', 'Negative values denote improvement. Cliff’s ⟪\\delta⟫ of unity indicates '
              'that the instrument improves on the baseline in every paired draw. The '
              'final column expresses the mean effect relative to vacancy creation.'),

    ('p', 'The ranking is stark and stable. Moderating the escalation of the employer '
          'threshold is roughly nineteen times as effective as vacancy creation and '
          'forty times as effective as raising training intensity, at the same '
          'standardised effort. Expectation guidance—raising the speed at which '
          'aspirations adapt and loosening their anchor, the policy analogue of the '
          'employability-thinking competences measured by Chacón-Cuberos and colleagues '
          '{{chacon2025}}—and improving matching efficiency come next and are '
          'statistically indistinguishable from one another. The two instruments that '
          'dominate public spending come last.'),

    ('p', 'This result must be read with its normalisation in mind. Equal standardised '
          'effort means equal movement in units of the prior standard deviation, not '
          'equal fiscal cost, and we make no claim about the relative expense of moving '
          'these parameters. What the comparison establishes is where the system is '
          'responsive, not where money is cheap. Panel (a) of Figure 6 shows the full '
          'effort–response curves and confirms that the ranking is not an artefact of the '
          'chosen effort level: the threshold-moderation curve dominates the others over '
          'the entire range from zero to three standard deviations, and the vacancy and '
          'training curves remain almost flat throughout.'),

    ('p', 'Combining instruments at a fixed total effort of two units confirms the '
          'pattern. The best available combination is a double dose of threshold '
          'moderation, which lowers the 2040 rate to 0.193 (⟪\\Delta⟫ = −0.324), '
          'followed by threshold moderation paired with expectation guidance at 0.274 '
          '(⟪\\Delta⟫ = −0.243) and with matching efficiency at 0.291 '
          '(⟪\\Delta⟫ = −0.226). Every combination that includes threshold moderation '
          'outperforms every combination that does not, and the best combination without '
          'it reaches only 0.458.'),

    ('h2', '4.9. Sequencing at Equal Cumulative Effort'),

    ('p', 'Because the system’s modes differ by a factor of twenty in speed, the '
          'order in which instruments are deployed should matter even when the total '
          'effort is held constant. We test this with three pairs, comparing '
          'simultaneous deployment of one unit of each throughout with front-loading two '
          'units of one instrument until 2032.5 and then switching. Table 11 reports both '
          'the terminal rate and the mean rate over 2025–2040, the latter being '
          'proportional to cumulative person-years of non-employment and therefore the '
          'welfare-relevant quantity.'),

    ('tabcap', 11, 'Policy sequencing at identical cumulative effort (two units over '
                   'fifteen years, switch date 2032.5).'),
    ('table', [
        ['Instrument pair', 'Deployment order', 'Mean NER 2025–2040', 'NER in 2040'],
        ['P3 guidance and P1 skill', 'P3 first, then P1', '0.2893', '0.4807'],
        ['P3 guidance and P1 skill', 'Both throughout', '0.3027', '0.4806'],
        ['P3 guidance and P1 skill', 'P1 first, then P3', '0.3149', '0.4750'],
        ['P1 skill and P2 matching', 'P1 first, then P2', '0.3106', '0.4699'],
        ['P1 skill and P2 matching', 'Both throughout', '0.3072', '0.4865'],
        ['P1 skill and P2 matching', 'P2 first, then P1', '0.3070', '0.5066'],
        ['P3 guidance and P2 matching', 'P3 first, then P2', '0.2752', '0.4422'],
        ['P3 guidance and P2 matching', 'Both throughout', '0.2857', '0.4583'],
        ['P3 guidance and P2 matching', 'P2 first, then P3', '0.2965', '0.4719'],
    ], [3200, 3200, 1900, 1740]),
    ('notes', 'The mean rate over the period is proportional to cumulative person-years '
              'of youth non-employment and is the welfare-relevant criterion; the '
              'terminal rate describes the state bequeathed to the following period.'),

    ('p', 'Two results emerge. First, sequencing matters materially. For the guidance and '
          'matching pair, front-loading expectation guidance yields a mean rate of 0.2752 '
          'against 0.2965 when matching efficiency comes first, a difference of 0.021, or '
          'about seven per cent of the level, and it also produces the better terminal '
          'state, so for this pair the ordering is unambiguous. Second, the criterion can '
          'reverse the ranking. For the guidance and skill pair, guidance-first minimises '
          'the cumulative burden (0.2893) but skill-first leaves the marginally better '
          'terminal state (0.4750 against 0.4807). This is a genuine intertemporal '
          'trade-off rather than a modelling artefact: guidance acts on a fast state and '
          'relieves the current cohort, whereas training acts on a slow state and '
          'accumulates. A government optimising the electoral cycle and one optimising '
          'the state bequeathed to its successor will make different choices from the '
          'same model.'),

    ('figure', 'fig6_policy.png', 6.55, None, 106),
    ('figcap', 6, 'Policy analysis. (a) Effort–response curves for the five instrument '
                  'families over zero to three prior standard deviations of effort. '
                  '(b) Effects at one unit of effort with 95 per cent paired intervals. '
                  '(c) Sequencing at identical cumulative effort, measured by the mean '
                  'non-employment rate over 2025–2040.'),

    ('h2', '4.10. Prefecture Archetypes'),

    ('p', 'China’s prefecture-level cities are not homogeneous, and the model’s '
          'parameters differ systematically across them. We define three archetypes: a '
          'digital-core metropolitan type, with the fastest digital expansion, the '
          'strongest vacancy response, the steepest threshold escalation, the largest '
          'graduate inflow and the most efficient matching; an advanced-manufacturing '
          'type, intermediate on all counts; and a peripheral labour-exporting type, with '
          'slower digitalisation, weaker matching and a higher valuation of institutional '
          'posts. Table 12 and Figure 7 report the outcomes.'),

    ('tabcap', 12, 'Prefecture-level city archetypes: trajectories and policy '
                   'responsiveness.'),
    ('table', [
        ['Archetype', 'NER 2025', 'NER 2040', 'SE flow 2040', 'Mismatch 2040',
         'Duration 2040 (yr)', 'Best instrument', 'NER 2040 under policy', 'Gain'],
        ['A. Digital-core metropolitan city', '0.251', '0.732', '0.658', '0.548', '31.99',
         'P5', '0.578', '0.155'],
        ['B. Advanced-manufacturing city', '0.173', '0.489', '0.539', '0.403', '7.53',
         'P5', '0.288', '0.201'],
        ['C. Peripheral labour-exporting city', '0.157', '0.251', '0.342', '0.303',
         '2.09', 'P5', '0.169', '0.082'],
    ], [3350, 950, 950, 1050, 1150, 1250, 1150, 1350, 800]),
    ('notes', 'Archetypes are parameterised illustratively rather than estimated on '
              'city-level data; they are intended to show how the same structure '
              'generates different behaviour under different parameterisations, not to '
              'rank actual cities.'),

    ('p', 'The ordering is the opposite of what a simple demand account predicts. The '
          'most digitally advanced archetype, which creates the most jobs and matches '
          'most efficiently, ends the horizon with by far the highest youth '
          'non-employment rate (0.732 against 0.251 in the periphery) and a mean '
          'transition duration of nearly thirty-two years, which is to say that in that '
          'parameterisation the cohort effectively never clears. The reason is visible in '
          'the parameterisation: the same digital dynamism that generates vacancies also '
          'drives the employer threshold upward, and in the calibrated system the '
          'threshold effect dominates the vacancy effect by more than two orders of '
          'magnitude (Table 8). The frontrunner runs faster and falls further behind its '
          'own bar.'),

    ('p', 'The policy reading is more encouraging, and more specific than the '
          'deterioration ranking suggests. The largest absolute dividend accrues not to '
          'the digital core but to the intermediate manufacturing archetype, where '
          'threshold moderation lowers the 2040 rate by 0.201 against 0.155 in the core '
          'and 0.082 in the periphery. The core is the most damaged but also the most '
          'saturated: its threshold has risen so far by 2040 that a one-standard-deviation '
          'moderation cannot bring it back. The implication for a national programme is '
          'that intervention should be targeted at cities in the middle of the digital '
          'transition, where the bar is rising fast but has not yet run away.'),

    ('figure', 'fig7_archetypes.png', 6.55, None, 107),
    ('figcap', 7, 'Prefecture-level city archetypes. (a) Non-employment trajectories under '
                  'the three '
                  'parameterisations. (b) The 2040 rate without new policy and under the '
                  'best single instrument at one unit of effort.'),

    # =====================================================================
    ('h1', '5. Discussion'),

    ('h2', '5.1. A Moving Target Rather Than a Tipping Point'),

    ('p', 'The principal theoretical contribution of this study is a negative one with '
          'positive consequences. Youth employment deterioration in a rapidly '
          'digitalising economy behaves like a trap but is not one. The system has a '
          'single stable equilibrium throughout the parameter region examined; what '
          'changes is the location of that equilibrium, which drifts upward as the '
          'employer skill threshold rises with digitalisation and with the mismatch it '
          'produces. Because the slowest mode of the system equals the duration of the '
          'youth window, the observed state trails this moving target by 1.7 years on '
          'average and by five years by the end of the horizon.'),

    ('p', 'This distinction has three consequences. It disciplines the language: '
          'early-warning indicators designed to detect critical slowing down before a '
          'fold {{scheffer2009}} are not informative here, because there is no fold to '
          'anticipate. It changes the diagnosis: persistence arises from slow states '
          'chasing a moving equilibrium, not from lock-in, so recovery does not require '
          'escaping a basin and is not subject to irreversibility. And it relocates the '
          'urgency: in a bistable system delay risks crossing a threshold, whereas here '
          'delay simply allows the target to move further away, which is less dramatic '
          'but, because the drift compounds and adjustment is slow, no less costly. The '
          'measured indicator understating the structural position is the mechanism by '
          'which such a system escapes attention until the gap is large.'),

    ('h2', '5.2. Why Job Creation Is Not the Binding Constraint'),

    ('p', 'That vacancy creation is nearly inert in this model is the result most likely '
          'to attract objection, so its logic deserves to be stated carefully. Vacancies '
          'enter the model in two places: they raise meetings through the matching '
          'function, and they raise offered quality through market tightness. Neither '
          'channel is blocked. What limits them is that meetings only become hires after '
          'passing a screen whose stringency is itself rising, and after being accepted '
          'by a searcher whose reservation threshold adjusts only slowly. When the '
          'skill–threshold gap has turned negative, additional meetings mostly generate '
          'additional rejections. Formally, the elasticity of hires with respect to '
          'vacancies is bounded above by the screening and acceptance probabilities, '
          'both of which fall as the drift proceeds. Empirically, this is why the '
          'vacancy-to-seeker ratio can stay above unity while non-employment doubles: the '
          'constraint is not the number of doors but the height of the sill.'),

    ('p', 'The finding is consistent with the broader evaluation literature, which reports '
          'modest and heterogeneous average effects for youth employment programmes and '
          'better results for interventions that change what employers or participants do '
          'rather than simply subsidising a transaction {{alm1|alm2|caliendo2016}}. It '
          'also aligns with evidence that the returns to training depend on whether the '
          'skills acquired are the ones employers are screening on '
          '{{training1|reskill2024|vet1}}. Our result sharpens rather than contradicts '
          'that literature: training raises employability capital, but in this system '
          'employability capital is not the state that is moving. The threshold is.'),

    ('h2', '5.3. The Queue as an Institution'),

    ('p', 'The examination queue turns out to be central in a way we did not anticipate. '
          'Its congestion loop is the second strongest stabiliser in the system after '
          'aspiration adjustment, accounting for 17.5 per cent of the total '
          'loop-deactivation effect: because success rates collapse as the queue '
          'lengthens, the queue is self-limiting. At the same time the queue is a major '
          'channel of delayed entry and of skill erosion, and the curvature of the '
          'probability-weighting function that sustains it is the third most important '
          'parameter in the variance decomposition (8.9 per cent of total-order '
          'variance). The queue is therefore simultaneously a safety valve and a '
          'sink.'),

    ('p', 'The policy implication is a warning against the obvious intervention. '
          'Expanding institutional recruitment raises the realised success rate, which '
          'weakens exactly the congestion feedback that prevents the queue from absorbing '
          'a larger share of each cohort. In the model this operates as a partial offset: '
          'more posts are filled, but the queue grows. The productive lever is not the '
          'number of posts but the decision weight attached to a small probability, which '
          'is addressable through information—publishing realised success rates by post '
          'and by cohort, and integrating them into career education—rather than through '
          'recruitment quotas. This is one concrete route by which the '
          'employability-thinking construct validated by Chacón-Cuberos and colleagues '
          '{{chacon2025}} becomes a system-level lever: what their analytical-thinking and '
          'information-handling factor measures is precisely the capacity that reduces '
          'the over-weighting of small probabilities.'),

    ('h2', '5.4. The Digital Paradox of a Frontrunner Region'),

    ('p', 'The archetype analysis produces the paper’s most counter-intuitive result: the '
          'city archetype with the fastest digital growth, most vacancies and best '
          'matching ends with the worst youth outcome. This is not an argument against digital '
          'transformation, which raises output, wages and job quality in this model as in '
          'the evidence {{ses_regional|digital_emp1|liu2024sus|wangguan2024|im_hc|gig1|robots_china2}}. '
          'It is an '
          'argument about the joint distribution of its effects. Digitalisation shifts '
          'demand towards higher-order competences {{skill_demand|sbtc1|rikala2024}}, and '
          'in doing so it raises the bar that entrants must clear at exactly the moment '
          'when it raises the number of doors. Where the first effect outruns the second, '
          'entrants face more opportunities they cannot access.'),

    ('p', 'For Chinese cities specifically this suggests that a local policy advantage '
          'in digital-industry development {{zhoupolicy2024}} and an aggressive '
          'talent-attraction regime {{talent}} are, from the perspective of local '
          'entrants, double-edged. Attracting experienced talent from elsewhere raises '
          'the observed competence distribution that employers screen against, which is '
          'formally equivalent in this model to raising the threshold. A '
          'common-prosperity agenda that treats youth transition quality as an objective '
          'alongside industrial upgrading {{tong2026|digital_emp2}} would need to monitor '
          'the skill–threshold gap directly rather than inferring it from vacancy counts, '
          'and would need to differentiate its instruments by where a city sits in the '
          'digital transition rather than applying one national package.'),

    ('h2', '5.5. Implications for Policy Design'),

    ('p', 'Four design implications follow from the results, stated in decreasing order '
          'of the confidence we attach to them. First, govern the bar. Instruments that '
          'slow the escalation of employer screening standards dominate every alternative '
          'at equal standardised effort. Concretely, this means competence-based rather '
          'than credential-based recruitment standards for public and state-owned '
          'employers, publicly certified micro-credentials that make competence legible '
          'so that employers do not over-screen on proxies, regulation of degree and '
          'experience requirements in advertised vacancies, and subsidised structured '
          'internships that let employers observe ability directly rather than inferring '
          'it. Second, manage expectations early. Expectation guidance is the second most '
          'effective instrument and, in two of the three pairs tested, should be '
          'front-loaded rather than run in parallel. Third, treat matching efficiency as '
          'a complement rather than a substitute: it is third in effectiveness and pairs '
          'well with threshold moderation, but it cannot compensate for a rising bar. '
          'Fourth, do not expand the queue. Enlarging institutional recruitment weakens '
          'the strongest stabilising feedback in the system.'),

    ('p', 'A fifth implication concerns measurement rather than instruments. Because the '
          'realised state lags its equilibrium by two to five years, national and city '
          'monitoring that tracks only the youth unemployment rate will detect '
          'deterioration late and will credit interventions late as well. A monitoring '
          'system built on this model would track the skill–threshold gap—operationalised '
          'as the distance between the competence distribution of entrants and the '
          'requirements stated in vacancy postings—alongside the realised rate, because '
          'the gap is a leading indicator and the rate is a lagging one.'),

    ('h2', '5.6. Contribution to Systems Practice in the Social Sciences'),

    ('p', 'Methodologically, this study joins three techniques that are usually applied '
          'separately. Loop deactivation {{ford1999}} establishes which feedbacks generate '
          'the observed behaviour; variance-based sensitivity analysis '
          '{{sobol2001|saltelli2010}} establishes which parameters generate the '
          'uncertainty; and statistical meta-modelling of the simulation output '
          'establishes where in parameter space the qualitative outcome changes. Applied '
          'to the same calibrated object, the three agree: threshold escalation is the '
          'strongest reinforcing loop, threshold sensitivity is the largest variance '
          'contributor, and threshold sensitivity is the root split of the classification '
          'tree. That agreement is not automatic—structural dominance and variance '
          'contribution answer different questions—and its presence is itself evidence '
          'that the model’s behaviour is driven by a mechanism rather than by a '
          'parameterisation. We would encourage this triangulation as a routine step in '
          'simulation-based social science, alongside the reporting standards already '
          'proposed {{rahmandad2012|barlas1996}}. Recent systems-theoretic work published in '
          'this journal on digital adoption, decision-making and regional digital '
          'dividends {{wangzhang2025|systems_ai_dm|dl4}} shares the same premise—that '
          'organisational and regional outcomes are properties of configurations rather '
          'than of variables—and could be linked to the transition system modelled here '
          'through the employer-threshold equation.'),

    ('p', 'Substantively, the study complements the two recent contributions in this '
          'journal that motivated it. Grigorescu and colleagues {{grigorescu2025}} '
          'establish, cross-sectionally and spatially, that youth exclusion is an '
          'emergent property of interacting digital and socio-economic subsystems and '
          'that its determinants act through thresholds; we show what such a system does '
          'over time and which of its couplings dominates. Chacón-Cuberos and colleagues '
          '{{chacon2025}} establish that employability thinking is a coherent, measurable '
          'latent construct; we show the system-level pathway through which that '
          'construct operates—by accelerating aspiration adjustment and by reducing the '
          'over-weighting of small probabilities—and quantify its policy value relative '
          'to alternatives. Recent system-dynamics work on Chinese employment '
          '{{chen2026}} identifies the education–technology–human-capital complex as the '
          'critical state variable at the macroeconomic level; our result that '
          'employability capital is flat while the threshold moves suggests that at the '
          'level of the transition itself the binding state is the requirement, not the '
          'endowment.'),

    ('h2', '5.7. Limitations'),

    ('p', 'Five limitations bound the claims. First, the model is specified and '
          'estimated at the national level, so its parameters are population-weighted '
          'averages across China’s prefecture-level cities; the archetype analysis shows '
          'how much behaviour varies once those averages are relaxed, but city-level '
          'point predictions should not be read off it. Second, the projections beyond '
          '2026 are structure-unchanged counterfactuals, not forecasts. They answer the '
          'question "where does this configuration of feedbacks lead?" and are '
          'meaningless as predictions, since the whole point of the paper is that the '
          'configuration is governable. Third, the model is deterministic and '
          'representative-agent within each stock; it cannot speak to heterogeneity by '
          'field of study, gender, institution tier or family background, all of which '
          'the mismatch literature shows to be substantial {{mismatch2|pan2025|ilo3}}. '
          'Fourth, firms are not optimising agents; the threshold responds to '
          'digitalisation and mismatch through a reduced form whose parameters are '
          'estimated rather than derived, and a micro-founded screening model could '
          'change the elasticities though we would not expect it to change their sign. '
          'Fifth, the archetype analysis is illustrative: its parameterisations are '
          'stipulated to represent recognisable city types, not estimated on city data.'),

    ('p', 'Three extensions follow naturally. Estimating the threshold equation directly '
          'from the text of vacancy postings would replace the reduced form with a '
          'measured one and would supply the leading indicator that Section 5.5 calls '
          'for. Disaggregating the model by field of study would let it speak to the '
          'humanities–science employment gap that graduate destination data show. And '
          'embedding the '
          'transition system in a spatial framework across China’s prefecture-level '
          'cities, in the manner of the spatial NEET analysis of Grigorescu and '
          'colleagues {{grigorescu2025}}, would allow inter-city migration of graduates '
          'to be treated endogenously rather than as a parameter difference, and would '
          'let the model speak to whether the digital core exports its threshold '
          'escalation to the cities that supply it with graduates.'),

    # =====================================================================
    ('h1', '6. Conclusions'),

    ('p', 'This paper asked why youth employment outcomes deteriorate in an economy where '
          'jobs are plentiful and the digital economy is expanding, and what to do about '
          'it. Treating the graduate school-to-work transition as a feedback system and '
          'calibrating it to seven published national moments, we find that the answer is '
          'neither a shortage of jobs nor a shortage of skills but the speed at which '
          'employers raise the bar. The system has no tipping point; it has a drifting '
          'attractor and a slow state, a combination that produces persistent '
          'deterioration while the measured indicator understates the structural position '
          'by two to five years.'),

    ('p', 'Three findings are directly actionable. Cyclical shocks decay with a half-life '
          'of one and a half years and are not the problem; the threshold drift does not '
          'decay and is. Among five policy families compared at equal standardised '
          'effort, moderating threshold escalation is roughly nineteen times as effective '
          'as vacancy creation and forty times as effective as training intensity, and '
          'every effective combination contains it. Sequencing matters at unchanged '
          'cumulative effort: front-loading expectation guidance before '
          'matching-efficiency investment lowers cumulative youth non-employment by about '
          'seven per cent relative to the reverse order, though the ranking can invert '
          'when the terminal rather than the cumulative state is the criterion. A fourth '
          'result is spatial: the largest dividend accrues to cities in the middle of the '
          'digital transition rather than to those furthest along it.'),

    ('p', 'The wider point is about where policy attention sits. Youth employment policy '
          'in China and elsewhere is organised around two levers—create jobs and train '
          'people—that this analysis places last among five. The levers that dominate '
          'concern how employers screen, how young people weight small probabilities, and '
          'how firmly aspirations are anchored. None of these has a budget line, and all '
          'three are governable. For a country whose stated ambition is common '
          'prosperity, the youth transition offers a case in which the binding constraint '
          'is not resources but the rules by which opportunity is rationed.'),

    ('back', 'Author Contributions:',
     'Conceptualization, methodology, formal analysis, software and writing—original '
     'draft preparation, X.C.; validation, data curation and visualization, D.H.; '
     'investigation, writing—review and editing, supervision and project administration, '
     'T.M. All authors have read and agreed to the published version of the manuscript.'),
    ('back', 'Funding:',
     'This research received no external funding.'),
    ('back', 'Institutional Review Board Statement:',
     'Not applicable. The study is a simulation analysis calibrated to published '
     'aggregate statistics and involves no human participants or animals.'),
    ('back', 'Informed Consent Statement:',
     'Not applicable.'),
    ('back', 'Data Availability Statement:',
     'The model is fully specified by Equations (1)–(15) and Table 2. No individual-level '
     'data were used. All calibration targets are drawn from publicly available sources '
     'cited in Table 3. The simulation code, the calibration routine, the sensitivity and '
     'policy experiments and the scripts that generate every figure and table in this '
     'article are available from the corresponding author on reasonable request.'),
    ('back', 'Acknowledgments:',
     'The authors thank the editors and the anonymous reviewers for comments that '
     'improved the manuscript.'),
    ('back', 'Conflicts of Interest:',
     'The authors declare no conflicts of interest.'),

    # =====================================================================
    ('h1', 'Appendix A'),

    ('tabcap', 'A1', 'Monte Carlo distributions of the 2040 outcomes over the twelve '
                     'uncertain parameters (Latin hypercube, ⟪n⟫ = 4096).'),
    ('table', [
        ['Outcome', 'Mean', 'SD', '2.5%', '25%', 'Median', '75%', '97.5%'],
        ['Youth non-employment rate', '0.546', '0.151', '0.227', '0.453', '0.558',
         '0.662', '0.795'],
        ['Mean transition duration (yr)', '16.06', '14.86', '1.90', '5.88', '11.04',
         '21.21', '57.28'],
        ['Slow-employment share of entrants', '0.560', '0.147', '0.174', '0.480', '0.579',
         '0.664', '0.779'],
        ['Vertical mismatch share', '0.438', '0.067', '0.317', '0.384', '0.441', '0.492',
         '0.555'],
    ], [3000, 950, 950, 950, 950, 950, 950, 950]),

    ('tabcap', 'A2', 'Remaining coefficients of the logistic meta-model of trap risk.'),
    ('table', [
        ['Parameter', 'Coefficient', 'SE', '⟪z⟫', '⟪p⟫', 'Odds ratio'],
        ['⟪\\phi⟫ Vacancy elasticity to digitalisation', '−1.057', '0.163', '−6.46',
         '<0.001', '0.348'],
        ['⟪\\tau⟫ Training intensity', '−0.616', '0.152', '−4.05', '<0.001', '0.540'],
        ['⟪\\lambda⟫ Aspiration adjustment speed', '−0.484', '0.150', '−3.23', '0.001',
         '0.617'],
        ['⟪\\chi⟫ Skill retention while queueing', '−0.473', '0.148', '−3.20', '0.001',
         '0.623'],
    ], [3600, 1400, 1000, 1000, 1000, 1650]),
    ('notes', 'Coefficients are per standard deviation of the corresponding prior; signs '
              'are as expected but the magnitudes are an order of magnitude smaller than '
              'those of the dominant parameters in Table 9.'),

    ('tabcap', 'A3', 'Principal splits of the cross-validated classification tree for '
                     'trap risk.'),
    ('table', [
        ['Depth', 'Splitting parameter', 'Threshold', 'Observations at the node'],
        ['1 (root)', '⟪\\kappa⟫ Threshold sensitivity', '1.456', '4096'],
        ['2', '⟪\\varepsilon⟫ Probability-weighting curvature', '0.526', '859'],
        ['2', '⟪\\kappa⟫ Threshold sensitivity', '1.758', '3237'],
        ['3', '⟪\\kappa_{2}⟫ Endogenous escalation', '0.106', '408'],
        ['3', '⟪g_{\\Phi}⟫ Cohort growth', '0.054', '451'],
        ['4', '⟪g_{\\Phi}⟫ Cohort growth', '0.047', '307'],
        ['4', '⟪\\zeta⟫ Aspiration anchoring', '0.612', '251'],
        ['5', '⟪\\zeta⟫ Aspiration anchoring', '0.507', '200'],
    ], [1300, 4300, 1600, 2440]),
    ('notes', 'Cost-complexity penalty selected by five-fold cross-validated AUC; '
              'cross-validated AUC 0.923, fifteen terminal leaves. The calibrated value '
              'of ⟪\\kappa⟫ = 1.855 lies above both ⟪\\kappa⟫ splits, placing the '
              'estimated economy in the highest-risk region of the tree.'),
]
