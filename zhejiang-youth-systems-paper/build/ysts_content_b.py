# -*- coding: utf-8 -*-
"""Manuscript content, part B: results, discussion, conclusions, back matter."""

PART_B = [

    # =====================================================================
    ('h1', '4. Results'),

    ('h2', '4.1. Baseline Behaviour and Validation'),

    ('p', 'Figure 3 and Table 5 report the baseline run under unchanged structure. Three '
          'features deserve emphasis. First, the model reproduces the observed '
          'deterioration without any exogenous deterioration being imposed on it: the '
          'youth non-employment rate rises from 0.119 in 2015 to 0.175 in 2025, the '
          'slow-employment share of entrants from 0.060 to 0.191, and the vertical '
          'mismatch share from 0.183 to 0.236, all within 3.5 per cent of their published '
          'counterparts. Second, this happens while the market remains tight: the '
          'vacancy-to-seeker ratio falls only from 1.50 to 1.41 over the same decade, and '
          'is still 1.24 in 2040. The system generates rising non-employment in a market '
          'that never becomes slack, which is the empirical puzzle set out in Section 1. '
          'Third, the mechanism is visible in panel (c). Employability capital is '
          'essentially flat, moving from 0.592 to 0.587 across twenty-five years, because '
          'cohort renewal continually replenishes it. What moves is the employer '
          'threshold, from 0.528 to 0.730. The skill–threshold gap consequently narrows, '
          'changes sign in 2022, and reaches −0.142 by 2040.'),

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
        ['2015', '0.119', '0.060', '0.183', '0.74', '35.1', '0.528', '0.592', '0.650',
         '+0.064', '1.50'],
        ['2020', '0.139', '0.104', '0.201', '0.86', '49.7', '0.574', '0.593', '0.643',
         '+0.019', '1.52'],
        ['2025', '0.175', '0.191', '0.236', '1.15', '96.6', '0.621', '0.590', '0.625',
         '−0.031', '1.41'],
        ['2030', '0.232', '0.327', '0.273', '1.72', '194.3', '0.665', '0.587', '0.602',
         '−0.078', '1.32'],
        ['2035', '0.309', '0.452', '0.306', '2.69', '343.9', '0.701', '0.586', '0.581',
         '−0.115', '1.27'],
        ['2040', '0.389', '0.520', '0.334', '3.97', '509.7', '0.730', '0.587', '0.564',
         '−0.142', '1.24'],
    ], [700, 800, 900, 950, 1150, 1000, 1050, 950, 1050, 800, 1000]),
    ('notes', 'NER is the youth non-employment rate; SE flow is the share of each '
              'entering cohort that chooses delayed entry. The 2030–2040 values are a '
              'structure-unchanged counterfactual, not a forecast: they describe where '
              'the present configuration of feedbacks leads if nothing in it changes.'),

    ('h2', '4.2. The Attractor Moves and the State Lags It'),

    ('p', 'Panel (a) of Figure 3 plots, alongside the realised trajectory, the '
          'instantaneous equilibrium of the system—the state to which it would converge '
          'if the exogenous drivers were frozen at their values in that year. This moving '
          'attractor rises from a non-employment rate of 0.119 in 2015 to 0.188 in 2025 '
          'and 0.478 in 2040. The realised state never reaches it. By 2040 the vertical '
          'gap between the two is 0.089, and the horizontal lag—the number of years by '
          'which the realised state trails the attractor—averages 2.00 years over the '
          'period and reaches 5.08 years at the end of the horizon.'),

    ('p', 'This is not a modelling artefact but a direct consequence of the system’s '
          'time constants. The eigenvalues of the Jacobian at the 2040 fixed point are '
          'all real and negative (Table 6), so the fixed point is a stable node, but they '
          'differ by a factor of forty-five. The slowest mode has a relaxation time of '
          'exactly eight years, equal to the reciprocal of the exit rate from the youth '
          'window: the system cannot adjust faster than a cohort can pass through it. '
          'Two further modes have relaxation times of 5.93 years. Since a first-order '
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
        ['⟪\\lambda_{1}⟫', '−5.577', '0.18', 'Search-flow equilibration'],
        ['⟪\\lambda_{2}⟫', '−1.755', '0.57', 'Aspiration and offer adjustment'],
        ['⟪\\lambda_{3}⟫', '−0.415', '2.41', 'Queue turnover'],
        ['⟪\\lambda_{4}⟫', '−0.169', '5.93', 'Mismatched-employment turnover'],
        ['⟪\\lambda_{5}⟫', '−0.169', '5.93', 'Matched-employment turnover'],
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
          'branches that coincide to within 10⁻⁴ in non-employment rate at every grid '
          'point, so no fold and no hysteresis loop exists in either direction '
          '(Figure 4a). A multi-start search from six widely separated initial guesses '
          'across a 6 × 4 grid spanning endogenous threshold escalation from 0 to 2.5 and '
          'screening sharpness from 3 to 22 returns exactly one admissible fixed point in '
          'all twenty-four cells.'),

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
          'is substantial: excess non-employment peaks at 0.137 in 2029, that is, it '
          'nearly doubles the contemporaneous baseline rate. Recovery, however, is brisk. '
          'The excess falls to half its peak within 1.67 years of the shock ending and to '
          '0.0043—about three per cent of the peak—ten years after. Figure 4b shows the '
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
        ['B3 Exam-queue congestion', 'Balancing', 'Realised exam success rate',
         '0.4909', '+0.1020', '+1.80', '32.5%'],
        ['B2 Aspiration adjustment', 'Balancing', 'Aspiration level',
         '0.4662', '+0.0773', '+1.51', '24.6%'],
        ['R3 Threshold escalation', 'Reinforcing', 'Observed mismatch share',
         '0.3462', '−0.0428', '−0.81', '13.6%'],
        ['R4 Thin-market offer quality', 'Reinforcing', 'Offered job quality',
         '0.3542', '−0.0348', '−0.55', '11.1%'],
        ['R1 Skill decay while searching', 'Reinforcing', 'Searcher stock in renewal term',
         '0.3580', '−0.0310', '−0.59', '9.9%'],
        ['R2 Queue–skill erosion', 'Reinforcing', 'Skill retention while queueing',
         '0.3629', '−0.0260', '−0.49', '8.3%'],
    ], [2600, 1250, 2600, 900, 900, 1300, 1090]),
    ('notes', 'The baseline 2040 non-employment rate is 0.3889 and the baseline mean '
              'transition duration 3.97 years. A positive ⟪\\Delta⟫ means that '
              'deactivating the loop worsens the outcome, identifying a balancing loop. '
              'Shares are absolute effects normalised to sum to unity.'),

    ('p', 'Three readings follow. First, the two balancing loops are doing most of the '
          'work: without exam-queue congestion and aspiration adjustment the 2040 '
          'non-employment rate would be 0.49 and 0.47 rather than 0.39. Congestion in '
          'particular is an unlovely but powerful brake—the fact that success rates '
          'collapse as the queue lengthens is what stops the queue absorbing the whole '
          'cohort. Policies that expand institutional recruitment without expanding '
          'anything else would weaken precisely this brake. Second, among the reinforcing '
          'loops, threshold escalation is the strongest single amplifier, accounting for '
          '13.6 per cent of the total deactivation effect and adding 0.81 years to the '
          'mean transition. Third, the two loops most emphasised in the policy '
          'literature—skill decay during search and erosion while queueing—together '
          'account for just over eighteen per cent. The scarring mechanism is real but it '
          'is not where the leverage is.'),

    ('h2', '4.6. Uncertainty and Global Sensitivity'),

    ('p', 'Twelve parameters are treated as uncertain over the ranges in Table 2. '
          'Propagating them through a Latin-hypercube design of 4096 draws gives a 2040 '
          'non-employment rate with mean 0.386, standard deviation 0.140 and a 95 per '
          'cent interval of [0.160, 0.649]; the median is 0.378 and the interquartile '
          'range [0.265, 0.500]. Mean transition duration has mean 5.04 years and a 95 '
          'per cent interval of [1.05, 14.56] years, the strong right skew reflecting the '
          'multiplicative structure of the reinforcing loops. Appendix Table A1 reports '
          'the full distributions. The point to note is that the qualitative conclusion '
          'is robust: even the 2.5th percentile of the distribution, 0.160, lies below '
          'but close to the 2025 realised value of 0.175, so under essentially the whole '
          'parameter space the system does not improve on its own.'),

    ('p', 'The Sobol decomposition (Table 8, Figure 5a) attributes variance rather than '
          'merely ranking parameters. The sensitivity of the employer threshold to '
          'digitalisation alone accounts for 35.8 per cent of the total output variance, '
          'more than twice the next parameter. The probability-weighting curvature '
          'contributes a total-order 18.4 per cent, cohort growth 13.2 per cent, '
          'aspiration anchoring '
          '11.8 per cent and endogenous threshold escalation 11.6 per cent. Matching '
          'efficiency contributes 4.9 per cent and training intensity 0.1 per cent. First- '
          'and total-order indices sum to 0.957 and 1.053 respectively, so the response '
          'surface is close to additive and interaction effects account for roughly ten '
          'per cent of the variance.'),

    ('tabcap', 8, 'Sobol variance decomposition of the 2040 non-employment rate '
                  '(base sample 1024; 14,336 model evaluations; 800 bootstrap '
                  'resamples).'),
    ('table', [
        ['Parameter', 'Meaning', 'First order ⟪S_{i}⟫', '95% CI',
         'Total order ⟪S_{Ti}⟫', '95% CI'],
        ['⟪\\kappa⟫', 'Threshold sensitivity to digitalisation', '0.357',
         '[0.204, 0.513]', '0.358', '[0.328, 0.390]'],
        ['⟪\\varepsilon⟫', 'Probability-weighting curvature', '0.146',
         '[0.034, 0.263]', '0.184', '[0.165, 0.205]'],
        ['⟪g_{\\Phi}⟫', 'Graduate cohort growth', '0.113', '[0.024, 0.203]', '0.132',
         '[0.120, 0.145]'],
        ['⟪\\zeta⟫', 'Aspiration anchoring weight', '0.113', '[0.020, 0.199]', '0.118',
         '[0.106, 0.131]'],
        ['⟪\\kappa_{2}⟫', 'Endogenous threshold escalation', '0.101', '[0.022, 0.196]',
         '0.116', '[0.103, 0.129]'],
        ['⟪\\Pi⟫', 'Perceived value of a public post', '0.049', '[−0.015, 0.117]',
         '0.066', '[0.057, 0.075]'],
        ['⟪\\mu⟫', 'Matching efficiency', '0.044', '[−0.014, 0.102]', '0.049',
         '[0.044, 0.054]'],
        ['⟪\\delta_{H}⟫', 'Skill decay while searching', '0.026', '[−0.010, 0.063]',
         '0.022', '[0.019, 0.025]'],
        ['⟪\\chi⟫', 'Skill retention while queueing', '0.005', '[−0.011, 0.020]',
         '0.003', '[0.003, 0.004]'],
        ['⟪\\phi⟫', 'Vacancy elasticity to digitalisation', '0.001', '[−0.010, 0.012]',
         '0.002', '[0.002, 0.002]'],
        ['⟪\\lambda⟫', 'Aspiration adjustment speed', '0.000', '[−0.009, 0.011]', '0.002',
         '[0.002, 0.002]'],
        ['⟪\\tau⟫', 'Training intensity', '0.002', '[−0.007, 0.010]', '0.001',
         '[0.001, 0.001]'],
        ['Sum', '', '0.957', '', '1.053', ''],
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
          'model it on the twelve standardised parameters. In the Monte Carlo sample 54.1 '
          'per cent of draws cross that line. The logistic meta-model (Table 9) fits '
          'extremely well: area under the receiver operating characteristic curve 0.994, '
          'Nagelkerke pseudo-⟪R^{2}⟫ 0.929, McFadden 0.861, likelihood-ratio '
          '⟪\\chi^{2}⟫(12) = 4866.58 with ⟪p⟫ < 0.001. Calibration is adequate: the '
          'Hosmer–Lemeshow statistic is 7.37 on eight degrees of freedom with ⟪p⟫ = 0.497, '
          'so the null of good fit is not rejected.'),

    ('tabcap', 9, 'Logistic meta-model of trap risk in the Monte Carlo sample '
                  '(⟪n⟫ = 4096; outcome: 2040 non-employment rate above 0.36).'),
    ('table', [
        ['Parameter', 'Coefficient', 'SE', '⟪z⟫', '⟪p⟫', 'Odds ratio', '95% CI'],
        ['⟪\\kappa⟫ Threshold sensitivity', '+7.817', '0.410', '+19.07', '<0.001',
         '2483.6', '[1112.0, 5547.2]'],
        ['⟪\\varepsilon⟫ Probability weighting', '−6.318', '0.336', '−18.83', '<0.001',
         '0.002', '[0.001, 0.003]'],
        ['⟪g_{\\Phi}⟫ Cohort growth', '+4.697', '0.257', '+18.28', '<0.001', '109.6',
         '[66.2, 181.4]'],
        ['⟪\\zeta⟫ Aspiration anchoring', '+4.444', '0.247', '+18.03', '<0.001', '85.1',
         '[52.5, 138.0]'],
        ['⟪\\kappa_{2}⟫ Endogenous escalation', '+4.210', '0.235', '+17.88', '<0.001',
         '67.4', '[42.5, 106.9]'],
        ['⟪\\Pi⟫ Value of a public post', '+3.593', '0.209', '+17.22', '<0.001', '36.4',
         '[24.2, 54.7]'],
        ['⟪\\mu⟫ Matching efficiency', '−2.642', '0.166', '−15.91', '<0.001', '0.071',
         '[0.051, 0.099]'],
        ['⟪\\delta_{H}⟫ Skill decay', '+1.824', '0.131', '+13.95', '<0.001', '6.20',
         '[4.80, 8.01]'],
    ], [3050, 1350, 900, 900, 900, 1200, 1940]),
    ('notes', 'Coefficients are per standard deviation of the corresponding prior. The '
              'four parameters with the smallest absolute ⟪z⟫ statistics '
              '(⟪\\chi⟫, ⟪\\phi⟫, ⟪\\lambda⟫, ⟪\\tau⟫) are omitted for space and are '
              'reported in Appendix Table A2. Model fit: AUC 0.994; Nagelkerke '
              '⟪R^{2}⟫ 0.929; Hosmer–Lemeshow ⟪\\chi^{2}⟫ = 7.37, ⟪p⟫ = 0.497.'),

    ('p', 'A cross-validated classification tree recovers the same ordering in '
          'interpretable form (cross-validated AUC 0.862, sixteen leaves). The root split '
          'is on the threshold sensitivity at ⟪\\kappa⟫ = 2.22, close to the calibrated '
          'value of 2.20: the calibrated economy sits almost exactly on the boundary '
          'between the two halves of the parameter space. Below that value the next split '
          'is on the probability-weighting curvature at 0.446, and thereafter on cohort '
          'growth at 0.0479 and on the value of an institutional post at 1.34 and 1.21. '
          'Above it the tree splits first on cohort growth at 0.0534 and then on '
          'aspiration anchoring at 0.687 and 0.577. The '
          'structure of the decision rules therefore reproduces, in a calibrated dynamic '
          'model of a Chinese province, the threshold-type relationships that Grigorescu '
          'and colleagues detected cross-sectionally in European NEET data '
          '{{grigorescu2025}}.'),

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
          '(Kruskal–Wallis ⟪H⟫ = 162.44, ⟪p⟫ = 4.4 × 10⁻³⁴), and every instrument '
          'improves on the baseline in every draw (Wilcoxon signed-rank ⟪p⟫ < 10⟪^{-60}⟫ '
          'throughout), so the interesting question is not whether they work but by how '
          'much.'),

    ('tabcap', 10, 'Policy experiments at one prior standard deviation of effort '
                   '(400 paired draws; baseline mean 2040 non-employment rate 0.3835).'),
    ('table', [
        ['Instrument', 'Parameter moved', '⟪\\Delta⟫NER', '95% interval',
         '⟪\\Delta⟫Duration (yr)', 'Cliff’s ⟪\\delta⟫', 'Relative to P4'],
        ['P5 Threshold moderation', '⟪\\kappa⟫ ↓, ⟪\\kappa_{2}⟫ ↓', '−0.1066',
         '[−0.1866, −0.0288]', '−2.44', '1.00', '17.8×'],
        ['P3 Expectation guidance', '⟪\\lambda⟫ ↑, ⟪\\zeta⟫ ↓', '−0.0410',
         '[−0.0788, −0.0103]', '−0.83', '1.00', '6.8×'],
        ['P2 Matching efficiency', '⟪\\mu⟫ ↑', '−0.0277', '[−0.0477, −0.0122]', '−0.63',
         '1.00', '4.6×'],
        ['P4 Vacancy creation', '⟪\\phi⟫ ↑', '−0.0060', '[−0.0089, −0.0026]', '−0.13',
         '1.00', '1.0×'],
        ['P1 Skill upgrading', '⟪\\tau⟫ ↑', '−0.0044', '[−0.0102, −0.0012]', '−0.12',
         '1.00', '0.7×'],
    ], [2650, 2100, 1150, 1750, 1400, 1050, 1240]),
    ('notes', 'Negative values denote improvement. Cliff’s ⟪\\delta⟫ of unity indicates '
              'that the instrument improves on the baseline in every paired draw. The '
              'final column expresses the mean effect relative to vacancy creation.'),

    ('p', 'The ranking is stark and stable. Moderating the escalation of the employer '
          'threshold is roughly eighteen times as effective as vacancy creation and '
          'twenty-four times as effective as raising training intensity, at the same '
          'standardised effort. Expectation guidance—raising the speed at which '
          'aspirations adapt and loosening their anchor, the policy analogue of the '
          'employability-thinking competences measured by Chacón-Cuberos and colleagues '
          '{{chacon2025}}—is second, and improving matching efficiency third. The two '
          'instruments that dominate public spending come last.'),

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
          'moderation, which lowers the 2040 rate to 0.185 (⟪\\Delta⟫ = −0.204), followed '
          'by threshold moderation paired with expectation guidance at 0.209 '
          '(⟪\\Delta⟫ = −0.180) and with matching efficiency at 0.230 '
          '(⟪\\Delta⟫ = −0.158). Every combination that includes threshold moderation '
          'outperforms every combination that does not.'),

    ('h2', '4.9. Sequencing at Equal Cumulative Effort'),

    ('p', 'Because the system’s modes differ by a factor of forty-five in speed, the '
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
        ['P3 guidance and P1 skill', 'P3 first, then P1', '0.2228', '0.3359'],
        ['P3 guidance and P1 skill', 'Both throughout', '0.2372', '0.3297'],
        ['P3 guidance and P1 skill', 'P1 first, then P3', '0.2495', '0.3123'],
        ['P1 skill and P2 matching', 'P1 first, then P2', '0.2520', '0.3385'],
        ['P1 skill and P2 matching', 'Both throughout', '0.2488', '0.3560'],
        ['P1 skill and P2 matching', 'P2 first, then P1', '0.2492', '0.3777'],
        ['P3 guidance and P2 matching', 'P3 first, then P2', '0.2094', '0.2982'],
        ['P3 guidance and P2 matching', 'Both throughout', '0.2210', '0.3079'],
        ['P3 guidance and P2 matching', 'P2 first, then P3', '0.2316', '0.3101'],
    ], [3200, 3200, 1900, 1740]),
    ('notes', 'The mean rate over the period is proportional to cumulative person-years '
              'of youth non-employment and is the welfare-relevant criterion; the '
              'terminal rate describes the state bequeathed to the following period.'),

    ('p', 'Two results emerge. First, sequencing matters materially. For the guidance and '
          'matching pair, front-loading expectation guidance yields a mean rate of 0.2094 '
          'against 0.2316 when matching efficiency comes first, a difference of 0.022, or '
          'about ten per cent of the level. Front-loading guidance also produces the '
          'better terminal state, so for this pair the ordering is unambiguous. Second, '
          'the criterion can reverse the ranking. For the guidance and skill pair, '
          'guidance-first minimises the cumulative burden (0.2228) but skill-first leaves '
          'the better terminal state (0.3123 against 0.3359). This is a genuine '
          'intertemporal trade-off rather than a modelling artefact: guidance acts on a '
          'fast state and relieves the current cohort, whereas training acts on a slow '
          'state and accumulates. A government optimising the electoral cycle and one '
          'optimising the state bequeathed to its successor will make different choices '
          'from the same model.'),

    ('figure', 'fig6_policy.png', 6.55, None, 106),
    ('figcap', 6, 'Policy analysis. (a) Effort–response curves for the five instrument '
                  'families over zero to three prior standard deviations of effort. '
                  '(b) Effects at one unit of effort with 95 per cent paired intervals. '
                  '(c) Sequencing at identical cumulative effort, measured by the mean '
                  'non-employment rate over 2025–2040.'),

    ('h2', '4.10. Prefecture Archetypes'),

    ('p', 'Zhejiang is not homogeneous, and the model’s parameters differ systematically '
          'across its prefectures. We define three archetypes: a digital core of the '
          'Hangzhou type, with the fastest digital expansion, the strongest vacancy '
          'response, the steepest threshold escalation, the largest graduate inflow and '
          'the most efficient matching; an advanced-manufacturing type of the Ningbo and '
          'Jiaxing kind, intermediate on all counts; and a peripheral labour-exporting '
          'type found in the south and west of the province, with slower digitalisation, '
          'weaker matching and a higher valuation of institutional posts. Table 12 and '
          'Figure 7 report the outcomes.'),

    ('tabcap', 12, 'Prefecture archetypes: trajectories and policy responsiveness.'),
    ('table', [
        ['Archetype', 'NER 2025', 'NER 2040', 'SE flow 2040', 'Mismatch 2040',
         'Duration 2040 (yr)', 'Best instrument', 'NER 2040 under policy', 'Gain'],
        ['A. Digital core (Hangzhou type)', '0.234', '0.582', '0.544', '0.407', '9.67',
         'P5', '0.447', '0.134'],
        ['B. Advanced manufacturing (Ningbo–Jiaxing type)', '0.170', '0.361', '0.501',
         '0.328', '3.49', 'P5', '0.233', '0.128'],
        ['C. Peripheral labour-exporting (south-west type)', '0.163', '0.220', '0.290',
         '0.268', '1.58', 'P5', '0.163', '0.057'],
    ], [3350, 950, 950, 1050, 1150, 1250, 1150, 1350, 800]),
    ('notes', 'Archetypes are parameterised illustratively rather than estimated on '
              'prefecture data; they are intended to show how the same structure '
              'generates different behaviour under different parameterisations, not to '
              'rank actual prefectures.'),

    ('p', 'The ordering is the opposite of what a simple demand account predicts. The '
          'most digitally advanced archetype, which creates the most jobs and matches '
          'most efficiently, ends the horizon with the highest youth non-employment rate '
          '(0.582 against 0.220 in the periphery) and the longest mean transition (9.67 '
          'against 1.58 years). The reason is visible in the parameterisation: the same '
          'digital dynamism that generates vacancies also drives the employer threshold '
          'upward, and in the calibrated system the threshold effect dominates the '
          'vacancy effect by roughly two orders of magnitude (Table 8). The frontrunner '
          'runs faster and falls further behind its own bar.'),

    ('p', 'The mirror image of this result is encouraging. The digital core also has by '
          'far the largest policy dividend: threshold moderation lowers its 2040 rate by '
          '0.134 against 0.057 in the periphery. Regions with the steepest deterioration '
          'are also the most responsive, because the parameter driving their '
          'deterioration is the one policy can address.'),

    ('figure', 'fig7_archetypes.png', 6.55, None, 107),
    ('figcap', 7, 'Prefecture archetypes. (a) Non-employment trajectories under the three '
                  'parameterisations. (b) The 2040 rate without new policy and under the '
                  'best single instrument at one unit of effort.'),

    # =====================================================================
    ('h1', '5. Discussion'),

    ('h2', '5.1. A Moving Target Rather Than a Tipping Point'),

    ('p', 'The principal theoretical contribution of this study is a negative one with '
          'positive consequences. Youth employment deterioration in a digital-frontrunner '
          'region behaves like a trap but is not one. The system has a single stable '
          'equilibrium throughout the parameter region examined; what changes is the '
          'location of that equilibrium, which drifts upward as the employer skill '
          'threshold rises with digitalisation and with the mismatch it produces. Because '
          'the slowest mode of the system equals the duration of the youth window, the '
          'observed state trails this moving target by about two years on average and by '
          'more than five years by the end of the horizon.'),

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
          'Its congestion loop is the single strongest stabiliser in the system, '
          'accounting for 32.5 per cent of the total loop-deactivation effect: because '
          'success rates collapse as the queue lengthens, the queue is self-limiting. At '
          'the same time the queue is a major channel of delayed entry and of skill '
          'erosion, and the curvature of the probability-weighting function that sustains '
          'it is the second most important parameter in the entire variance decomposition '
          '(18.4 per cent). The queue is therefore simultaneously a safety valve and a '
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
          'archetype with the fastest digital growth, most vacancies and best matching '
          'ends with the worst youth outcome. This is not an argument against digital '
          'transformation, which raises output, wages and job quality in this model as in '
          'the evidence {{ses_regional|digital_emp1|liu2024sus|wangguan2024|im_hc|gig1|robots_china2}}. '
          'It is an '
          'argument about the joint distribution of its effects. Digitalisation shifts '
          'demand towards higher-order competences {{skill_demand|sbtc1|rikala2024}}, and '
          'in doing so it raises the bar that entrants must clear at exactly the moment '
          'when it raises the number of doors. Where the first effect outruns the second, '
          'entrants face more opportunities they cannot access.'),

    ('p', 'For Zhejiang specifically this suggests that the province’s policy advantage '
          'in digital-industry development {{zhoupolicy2024}} and its aggressive '
          'talent-attraction regime {{talent}} are, from the perspective of local '
          'entrants, double-edged. Attracting experienced talent from elsewhere raises '
          'the observed competence distribution that employers screen against, which is '
          'formally equivalent in this model to raising the threshold. A common-prosperity '
          'agenda that treats youth transition quality as an objective alongside '
          'industrial upgrading {{tong2026|digital_emp2}} would need to monitor the '
          'skill–threshold gap directly rather than inferring it from vacancy counts.'),

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
          'realised state lags its equilibrium by two to five years, provincial '
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

    ('p', 'Five limitations bound the claims. First, the model is calibrated to seven '
          'moments, of which several are national rather than provincial because Zhejiang '
          'does not publish a youth unemployment series on the international definition. '
          'The model represents a Zhejiang-like digital-frontrunner economy; provincial '
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
          'stipulated to represent recognisable prefecture types, not estimated on '
          'prefecture data.'),

    ('p', 'Three extensions follow naturally. Estimating the threshold equation directly '
          'from the text of vacancy postings would replace the reduced form with a '
          'measured one and would supply the leading indicator that Section 5.5 calls '
          'for. Disaggregating the model by field of study would let it speak to the '
          'humanities–science employment gap that provincial data show. And embedding the '
          'transition system in a spatial framework across the eleven prefectures, in the '
          'manner of the spatial NEET analysis of Grigorescu and colleagues '
          '{{grigorescu2025}}, would allow migration between prefectures to be treated '
          'endogenously rather than as a parameter difference.'),

    # =====================================================================
    ('h1', '6. Conclusions'),

    ('p', 'This paper asked why youth employment outcomes deteriorate in a region where '
          'jobs are plentiful and the digital economy is expanding, and what to do about '
          'it. Treating the graduate school-to-work transition as a feedback system and '
          'calibrating it to seven published moments, we find that the answer is neither '
          'a shortage of jobs nor a shortage of skills but the speed at which employers '
          'raise the bar. The system has no tipping point; it has a drifting attractor '
          'and a slow state, a combination that produces persistent deterioration while '
          'the measured indicator understates the structural position by two to five '
          'years.'),

    ('p', 'Three findings are directly actionable. Cyclical shocks decay with a half-life '
          'under two years and are not the problem; the threshold drift does not decay '
          'and is. Among five policy families compared at equal standardised effort, '
          'moderating threshold escalation is roughly eighteen times as effective as '
          'vacancy creation and twenty-four times as effective as training intensity, and '
          'every effective combination contains it. Sequencing matters at unchanged '
          'cumulative effort: front-loading expectation guidance before '
          'matching-efficiency investment lowers cumulative youth non-employment by about '
          'ten per cent relative to the reverse order, though the ranking can invert when '
          'the terminal rather than the cumulative state is the criterion.'),

    ('p', 'The wider point is about where policy attention sits. Youth employment policy '
          'in China and elsewhere is organised around two levers—create jobs and train '
          'people—that this analysis places last among five. The levers that dominate '
          'concern how employers screen, how young people weight small probabilities, and '
          'how firmly aspirations are anchored. None of these has a budget line, and all '
          'three are governable. For a province whose stated ambition is common '
          'prosperity, the youth transition offers a case in which the binding constraint '
          'is not resources but the rules by which opportunity is rationed.'),

    # =====================================================================
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
        ['Youth non-employment rate', '0.386', '0.140', '0.160', '0.265', '0.378',
         '0.500', '0.649'],
        ['Mean transition duration (yr)', '5.04', '3.67', '1.05', '2.22', '3.98', '6.98',
         '14.56'],
        ['Slow-employment share of entrants', '0.422', '0.197', '0.052', '0.255', '0.482',
         '0.566', '0.726'],
        ['Vertical mismatch share', '0.355', '0.050', '0.269', '0.316', '0.354', '0.391',
         '0.454'],
    ], [3000, 950, 950, 950, 950, 950, 950, 950]),

    ('tabcap', 'A2', 'Remaining coefficients of the logistic meta-model of trap risk.'),
    ('table', [
        ['Parameter', 'Coefficient', 'SE', '⟪z⟫', '⟪p⟫', 'Odds ratio'],
        ['⟪\\chi⟫ Skill retention while queueing', '−0.809', '0.102', '−7.91', '<0.001',
         '0.445'],
        ['⟪\\phi⟫ Vacancy elasticity to digitalisation', '−0.629', '0.097', '−6.48',
         '<0.001', '0.533'],
        ['⟪\\lambda⟫ Aspiration adjustment speed', '−0.560', '0.095', '−5.86', '<0.001',
         '0.571'],
        ['⟪\\tau⟫ Training intensity', '−0.413', '0.095', '−4.33', '<0.001', '0.661'],
    ], [3600, 1400, 1000, 1000, 1000, 1650]),
    ('notes', 'Coefficients are per standard deviation of the corresponding prior; signs '
              'are as expected but the magnitudes are an order of magnitude smaller than '
              'those of the dominant parameters in Table 9.'),

    ('tabcap', 'A3', 'Principal splits of the cross-validated classification tree for '
                     'trap risk.'),
    ('table', [
        ['Depth', 'Splitting parameter', 'Threshold', 'Observations at the node'],
        ['1 (root)', '⟪\\kappa⟫ Threshold sensitivity', '2.220', '4096'],
        ['2', '⟪\\varepsilon⟫ Probability-weighting curvature', '0.446', '1883'],
        ['2', '⟪g_{\\Phi}⟫ Cohort growth', '0.0534', '1138'],
        ['3', '⟪g_{\\Phi}⟫ Cohort growth', '0.0479', '745'],
        ['3', '⟪\\zeta⟫ Aspiration anchoring', '0.687', '650'],
        ['4', '⟪\\Pi⟫ Value of an institutional post', '1.338', '352'],
        ['4', '⟪\\Pi⟫ Value of an institutional post', '1.215', '393'],
        ['4', '⟪\\zeta⟫ Aspiration anchoring', '0.577', '488'],
    ], [1300, 4300, 1600, 2440]),
    ('notes', 'Cost-complexity penalty selected by five-fold cross-validated AUC; '
              'cross-validated AUC 0.862, sixteen terminal leaves. The root threshold of '
              '2.220 lies within one per cent of the calibrated value of 2.20.'),
]
