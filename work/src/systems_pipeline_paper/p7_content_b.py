# -*- coding: utf-8 -*-
"""Paper 7, Part B: Results, Discussion, Conclusions, back matter, Appendix A."""

PART_B = [
# ================================================================ 4. Results
('h1', '4. Results'),

('h2', '4.1. Study 1: Behavioural Parameter Estimates'),

('p', 'Table 1 reports descriptive statistics for the 356 firms. Automation of the entry task '
      'bundle averages 0.342 (SD 0.153) and spans almost the full unit interval, from 0.02 to '
      '0.714, confirming that the sample contains firms at very different points of the same '
      'diffusion process. Junior staffing intensity averages 0.1064 entry-level '
      'full-time equivalents per unit of annual workload (SD 0.0192), verification load '
      'averages 0.1364 senior full-time-equivalent years per unit of machine output (SD '
      '0.0412), documented mentoring intensity averages 0.0970 senior full-time-equivalent '
      'years per junior (SD 0.0192), and median time to independent proficiency averages 6.94 '
      'years (SD 1.35). Structured AI-assisted learning practice averages 0.414 with a '
      'standard deviation of 0.233, so firms differ widely in whether they use AI as a '
      'substitute for junior practice or as scaffolding for it. The bivariate pattern is '
      'already informative: automation depth correlates negatively with junior staffing '
      'intensity (⟪r⟫ = −0.551, ⟪p⟫ < 0.001) but only weakly and positively with time to '
      'proficiency (⟪r⟫ = 0.139, ⟪p⟫ = 0.008), while mentoring intensity correlates strongly '
      'and negatively with time to proficiency (⟪r⟫ = −0.603, ⟪p⟫ < 0.001) and with delivery '
      'pressure (⟪r⟫ = −0.312, ⟪p⟫ < 0.001).'),

('tabcap', 1, 'Descriptive statistics and sample profile, Study 1 (⟪N⟫ = 356 firms).'),
('table', [
    ['Variable', 'Mean', 'SD', 'P25', 'Median', 'P75', 'Min', 'Max'],
    ['Automation of task bundle (ATA)', '0.342', '0.153', '0.238', '0.351', '0.443', '0.020', '0.714'],
    ['Junior staffing intensity (JSH)', '0.1064', '0.0192', '0.0921', '0.1056', '0.1198', '0.0581', '0.1717'],
    ['Verification load (VNU)', '0.1364', '0.0412', '0.1080', '0.1287', '0.1573', '0.0604', '0.3906'],
    ['Mentoring intensity (MEN)', '0.0970', '0.0192', '0.0835', '0.0964', '0.1095', '0.0485', '0.1653'],
    ['Delivery pressure (PRS)', '0.965', '0.219', '0.796', '0.948', '1.105', '0.550', '1.550'],
    ['Time to proficiency, years (TTP)', '6.94', '1.35', '5.97', '6.88', '7.72', '3.92', '10.50'],
    ['Structured AI learning practice (SAL)', '0.414', '0.233', '0.229', '0.396', '0.585', '0.020', '0.970'],
    ['Employees (log)', '5.05', '0.90', '4.42', '5.03', '5.69', '2.56', '7.36'],
    ['Firm age, years', '14.61', '6.74', '10.0', '13.0', '18.0', '4.0', '42.0'],
    ['R&D intensity, %', '3.51', '2.59', '1.70', '2.90', '4.80', '0.20', '17.40'],
 ], [3180, 900, 900, 830, 900, 830, 830, 830]),
('notes', 'Sector composition: software and IT services 140, professional and business '
          'services 124, finance and shared-service operations 92. Size bands: 20–99 '
          'employees 112, 100–299 employees 156, 300–999 employees 79, 1000+ employees 9. '
          'Response flow: 520 distributed, 389 returned (74.8%), 33 excluded, 356 valid '
          '(68.5%).'),

('p', 'Table 2 reports the estimating equations. Model A shows that a one-unit increase in '
      'automation depth reduces junior staffing intensity by 0.0808 units (HC3 SE 0.0061, '
      '⟪t⟫ = −13.16, ⟪p⟫ < 0.001) against an intercept of 0.1335, giving a substitutability '
      'estimate of ⟪\\phi⟫ = 0.605 (delta-method SE 0.035, 95% CI [0.536, 0.674]). The model '
      'explains 39.9% of adjusted variance, ⟪F⟫(6, 349) = 40.32, ⟪p⟫ < 0.001, with all '
      'variance inflation factors below 1.36. Firm size enters positively and firm age '
      'negatively, as expected if larger and younger firms staff entry roles more '
      'intensively; R&D intensity and sector are not significant.'),

('p', 'Model C identifies the mentoring rule. Reference mentoring intensity, the intercept at '
      'mean automation and mean structured practice, is ⟪m^{∗}⟫ = 0.1019 senior '
      'full-time-equivalent years per junior (SE 0.0010). Excess delivery pressure reduces '
      'mentoring by 0.0679 units per unit (SE 0.0064, ⟪t⟫ = −10.52, ⟪p⟫ < 0.001), an implied '
      'crowd-out ratio of 0.666 (delta-method SE 0.060); automation depth has no direct effect '
      'on mentoring once delivery pressure is controlled (⟪b⟫ = −0.0039, ⟪p⟫ = 0.498). This '
      'null is substantively important. It is the first evidence that automation does not '
      'squeeze mentoring directly—it squeezes mentoring only through the delivery pressure '
      'that a depleted senior stock creates, which is precisely the R2 loop of Figure 1 and '
      'not a channel of the shock itself.'),

('p', 'Model D is the learning equation and carries the study’s central estimate. The '
      'mentoring elasticity is ⟪a⟫ = 0.446 (SE 0.043, ⟪t⟫ = −10.39 on the negative '
      'coefficient, ⟪p⟫ < 0.001): doubling mentoring intensity reduces time to proficiency by '
      'about 27%. The practice-displacement coefficient is ⟪\\theta⟫ = 0.574 (SE 0.064, '
      '⟪p⟫ < 0.001) and the AI-as-tutor coefficient at full structured practice is '
      '⟪\\lambda_{max}⟫ = 0.639 (SE 0.113, ⟪p⟫ < 0.001). The reference time to proficiency '
      'implied by the intercept is ⟪\\tau_{0}⟫ = 6.02 years (95% CI [5.75, 6.31]). The model '
      'explains 51.8% of adjusted variance, ⟪F⟫(8, 347) = 48.71, ⟪p⟫ < 0.001; the '
      'Breusch–Pagan statistic is ⟪\\chi^{2}⟫(8) = 5.21, ⟪p⟫ = 0.735, the Shapiro–Wilk '
      'statistic on the residuals is ⟪W⟫ = 0.997, ⟪p⟫ = 0.713, and the largest variance '
      'inflation factor is 3.07, so the estimates are not compromised by heteroskedasticity, '
      'non-normality or collinearity.'),

('tabcap', 2, 'Estimating equations for the behavioural parameters of the simulation model '
              '(OLS with HC3 robust standard errors, ⟪N⟫ = 356).'),
('table', [
    ['Dependent variable', 'Model A: JSH', 'Model C: MEN', 'Model D: ln(TTP)'],
    ['Intercept', '0.1335 *** (0.0027)', '0.1019 *** (0.0010)', '1.7957 *** (0.0238)'],
    ['Automation depth (ATA)', '−0.0808 *** (0.0061)', '−0.0039 (0.0058)', '0.5738 *** (0.0639)'],
    ['ATA × SAL', '—', '—', '−0.6393 *** (0.1128)'],
    ['ln(mentoring ratio)', '—', '—', '−0.4455 *** (0.0429)'],
    ['Excess delivery pressure', '—', '−0.0679 *** (0.0064)', '—'],
    ['Structured practice (SAL)', '—', '0.0409 *** (0.0047)', '—'],
    ['Employees (log)', '0.0057 *** (0.0008)', '−0.0005 (0.0011)', '−0.0349 *** (0.0093)'],
    ['Firm age', '−0.0033 *** (0.0008)', '−0.0001 (0.0009)', '0.0240 *** (0.0072)'],
    ['R&D intensity', '0.0002 (0.0008)', '—', '−0.0003 (0.0094)'],
    ['Sector controls', 'Yes', 'No', 'Yes'],
    ['Adjusted ⟪R^{2}⟫', '0.399', '0.331', '0.518'],
    ['⟪F⟫ statistic', '40.32 ***', '36.15 ***', '48.71 ***'],
    ['Breusch–Pagan ⟪p⟫', '0.085', '0.037', '0.735'],
    ['Maximum VIF', '1.36', '1.63', '3.07'],
 ], [2860, 2260, 2260, 2260]),
('notes', 'HC3 heteroskedasticity-consistent standard errors in parentheses. '
          '*** ⟪p⟫ < 0.001. Model C centres ATA and SAL so that the intercept identifies '
          'reference mentoring intensity. Model D is estimated in logarithms so that the '
          'coefficients map onto the multiplicative learning structure of Equations (12) and '
          '(13); the intercept identifies ⟪\\tau_{0}⟫ = exp(1.7957) = 6.02 years. Residual '
          'normality in Model D: Shapiro–Wilk ⟪W⟫ = 0.997, ⟪p⟫ = 0.713.'),

('p', 'The interaction term makes the learning penalty of automation conditional rather than '
      'absolute, and Figure 3 shows how much difference this makes. At the twenty-fifth '
      'percentile of structured practice the marginal effect of automation depth on log time '
      'to proficiency is 0.428 (SE 0.054, ⟪p⟫ < 0.001), which is a substantial penalty: '
      'moving such a firm from no automation to full automation of the entry bundle would '
      'lengthen time to proficiency by about 53%. At the seventy-fifth percentile the penalty '
      'falls to 0.200 (SE 0.060, ⟪p⟫ = 0.001), and at the ninety-fifth percentile it is 0.046 '
      '(SE 0.077, ⟪p⟫ = 0.549), statistically indistinguishable from zero. The level of '
      'structured practice at which automation becomes learning-neutral is 0.897. In other '
      'words, the damage automation does to expertise formation is not a property of the '
      'technology; it is a property of how the technology is deployed, and firms at the very '
      'top of the observed practice distribution already avoid it entirely. This estimate is '
      'the empirical basis for policy lever P3, and it is what makes that lever '
      'implementable rather than aspirational.'),

('figure', 'p7_fig7.png', 4.15, None, 103),
('figcap', 3, 'Marginal effect of automation depth on log time to independent proficiency, as '
              'a function of structured AI-assisted learning practice (Study 1, Model D). '
              'Shading gives the 95% confidence band; points mark the 25th, 75th and 95th '
              'percentiles of observed practice. The effect is large and highly significant at '
              'low levels of structured practice and indistinguishable from zero at the 95th '
              'percentile.'),

('p', 'Two robustness checks support the specification. Adding a quadratic term in automation '
      'depth leaves the linear specification preferred (⟪b⟫ = 0.077, SE 0.245, ⟪p⟫ = 0.753; '
      'adjusted ⟪R^{2}⟫ falls from 0.518 to 0.517), so the relation is adequately linear over '
      'the observed range. A median split on firm size shows the expected heterogeneity '
      'without changing signs: larger firms have a higher mentoring elasticity (0.576 versus '
      '0.324) and a smaller practice-displacement coefficient (0.454 versus 0.715), consistent '
      'with better-resourced training systems, but the AI-as-tutor coefficient is larger in '
      'smaller firms (0.859 versus 0.419), suggesting that structured practice substitutes for '
      'the formal training infrastructure that small firms lack. Table 3 sets out how each '
      'estimate enters the simulation.'),

('tabcap', 3, 'Calibration map: from Study 1 estimates to simulation parameters.'),
('table', [
    ['Symbol', 'Meaning', 'Source', 'Estimate (SE)', 'Adopted'],
    ['⟪\\phi⟫', 'AI–junior substitutability', 'Model A, delta method',
     '0.605 (0.035)', '0.605'],
    ['⟪\\nu⟫', 'Verification load per unit of machine output', 'Direct measurement (VNU)',
     '0.1364 (0.0022)', '0.136'],
    ['⟪m^{∗}⟫', 'Reference mentoring intensity', 'Model C intercept',
     '0.1019 (0.0010)', '0.102'],
    ['⟪\\tau_{0}⟫', 'Reference time to proficiency (years)', 'Model D intercept',
     '6.02 [5.75, 6.31]', '6.02'],
    ['⟪a⟫', 'Mentoring elasticity of proficiency', 'Model D, ln(mentoring ratio)',
     '0.446 (0.043)', '0.446'],
    ['⟪\\theta⟫', 'Practice-displacement coefficient', 'Model D, ATA',
     '0.574 (0.064)', '0.574'],
    ['⟪\\lambda⟫', 'AI-as-tutor coefficient at mean practice',
     'Model D interaction × mean SAL', '0.265', '0.265'],
    ['Crowd-out ratio', 'Mentoring lost per unit of excess delivery pressure',
     'Model C, delta method', '0.666 (0.060)', 'Structural (Eq. 11)'],
 ], [1120, 3180, 2480, 1700, 1160]),
('notes', 'Adopted values are used in the base run. The global sensitivity analysis samples '
          'each parameter over a range at least three standard errors wide, and wider where '
          'the split-sample analysis indicates heterogeneity across firm sizes; ranges are '
          'listed in Table A1.'),

('h2', '4.2. Model Validation'),

('p', 'Table 4 reports the six validation tests. All equations are dimensionally consistent. '
      'Under zero graduate inflow the system depletes as it must, ending with a senior stock '
      'of 70.0 thousand and a junior stock of 0.8 thousand; under zero automation the '
      'initialised system drifts by 0.0% over 200 years, confirming that the reported '
      'behaviour is a response to the shock rather than a transient; under instantaneous full '
      'automation the verification requirement immediately exhausts senior capacity and the '
      'usable share of machine output collapses to 0.004, which is the behaviour the structure '
      'implies. Halving the integration step changes the terminal senior stock by 8 × 10⁻⁵ '
      'per cent, so the results are not an artefact of numerical integration.'),

('p', 'The behaviour-reproduction test is the most demanding, because it compares the model '
      'against evidence that was not used to build it. The model was calibrated entirely on '
      'the cross-sectional Study 1 estimates and on physical turnover parameters; no time '
      'series entered the calibration. It nonetheless produces an entry-hiring decline of '
      '11.3% by year 3 and 22.9% by year 5, bracketing the roughly 13% relative decline in '
      'employment of 22- to 25-year-olds in AI-exposed occupations that Brynjolfsson, Chandar '
      'and Chen estimate from United States payroll microdata over a comparable interval '
      'after the onset of generative-AI diffusion {{canaries}}. Reproducing an independently '
      'measured magnitude from independently estimated structure is the strongest available '
      'evidence that the model’s decision rules are not arbitrary.'),

('tabcap', 4, 'Validation tests and outcomes.'),
('table', [
    ['Test', 'Procedure', 'Result', 'Verdict'],
    ['Dimensional consistency', 'Unit check of every equation',
     'All rates in persons yr⁻¹ or task units yr⁻¹', 'Pass'],
    ['Equilibrium', 'Simulate 200 years with automation frozen',
     'Senior stock drift 0.0%', 'Pass'],
    ['Extreme condition 1', 'Graduate inflow set to zero',
     'Senior stock 70.0, junior stock 0.8 at year 30', 'Pass'],
    ['Extreme condition 2', 'Automation frozen at pre-shock depth',
     'No divergence from counterfactual', 'Pass'],
    ['Extreme condition 3', 'Instantaneous full automation',
     'Usable share of machine output falls to 0.004', 'Pass'],
    ['Integration error', 'Halve the time step to 0.025 years',
     'Terminal senior stock differs by 8 × 10⁻⁵ %', 'Pass'],
    ['Structural (loop knockout)', 'Set each channel or loop parameter to zero',
     'All seven changes in the predicted direction (Table 5)', 'Pass'],
    ['Behaviour reproduction', 'Compare early entry-hiring decline with published estimate',
     'Model −11.3% at year 3, −22.9% at year 5 vs. ≈−13% observed {{canaries}}', 'Pass'],
 ], [2340, 3060, 3320, 900]),

('h2', '4.3. Reference Behaviour: Better before Worse'),

('p', 'Figure 4 shows the base run against the no-automation counterfactual. The trajectory '
      'confirms Proposition 1 in every respect. Entry-level hiring falls immediately, by 11.3% '
      'at year 3 and 22.9% at year 5, and reaches a trough 53.7% below the counterfactual at '
      'year 25.6. The senior stock, by contrast, barely moves for a decade—it is only 9.2% '
      'below the counterfactual at year 10—because the seniors of year 10 were hired long '
      'before the shock. It then declines steadily to 46.3% below the counterfactual at year '
      '30. The junior stock falls by 36.3% and the total professional workforce by 43.5%.'),

('p', 'Productive capacity tells the story that makes the trap difficult to escape. It rises, '
      'peaking 8.7% above the counterfactual in year 8.9, because machines are doing routine '
      'work that people used to do and the senior stock has not yet been depleted. It remains '
      'above the counterfactual until year 16.6 and then falls, ending 15.4% below at year 30. '
      'For sixteen years, in other words, every available performance indicator vindicates the '
      'automation decision. By the time the indicator turns, thirteen entry cohorts have been '
      'lost. The cumulative deficit is large: over thirty years the system makes 40.7% fewer '
      'entry hires than the counterfactual, and it converts those hires into proficient '
      'professionals less efficiently, at 0.393 promotions per entry hire against 0.433 in the '
      'counterfactual.'),

('p', 'Time to proficiency rises from 6.56 years at equilibrium to 16.92 years at year 30, and '
      'Figure 4 shows that the rise is not smooth: it is gradual until about year 23 and then '
      'jumps. The mechanism is visible in the senior time accounts. Verification consumes 1.4% '
      'of senior time at the start and 37.1% at year 30; senior utilisation, which begins at '
      '0.856—below the norm of 0.88—falls to 0.742 by year 10 as machines absorb routine work, '
      'then climbs back through the norm and reaches 1.000 by year 30. Documented mentoring '
      'holds at its reference level of 0.102 senior-years per junior for more than two decades '
      'and then collapses to zero once delivery obligations exhaust the non-delivery budget. '
      'This is the behavioural signature of a residual claimant: it is fully protected until '
      'the moment it is not protected at all.'),

('p', 'The excluded entrants accumulate the corresponding damage. The entrant pool grows by '
      '97.7% relative to the counterfactual, and the time people spend in it—measured as '
      'cumulative pool-years—rises by 61.9%. Skill capital per entrant falls from 0.840 to '
      '0.712, so the cohorts firms eventually hire are less prepared than the cohorts they '
      'declined to hire earlier, which lengthens time to proficiency further. Youth exclusion '
      'in this model is therefore not merely a distributional consequence of the automation '
      'decision; it is a mechanism that feeds back into the productive capacity of the firms '
      'that made it {{vonwachter20|scars_youth|scarring_meta|ilo_get2024|oecd_eo2025}}.'),

('figure', 'p7_fig3.png', 5.45, None, 104),
('figcap', 4, 'Reference behaviour of the model against the no-automation counterfactual. '
              'Entry-level hiring falls immediately; the senior stock responds only after a '
              'decade; productive capacity rises before it falls, crossing the counterfactual '
              'in year 16.6; and time to proficiency jumps once mentoring collapses around '
              'year 23. The dash-dotted line in the upper right panel is the automation '
              'diffusion path.'),

('h2', '4.4. Two Successive Regime Shifts'),

('p', 'Sweeping asymptotic automation depth from 0.10 to 0.95 confirms Proposition 2. Figure 5 '
      'shows that the response of the senior stock to automation depth is not smooth but '
      'contains two distinct breaks. The first occurs at a depth of 0.475, where the slope of '
      'the response reaches its steepest value of −112.6 percentage points per unit of depth. '
      'The right-hand panel identifies the cause: at exactly this depth, mentoring per junior '
      'at year 30 collapses from its reference level to zero. Below the threshold, delivery '
      'obligations still fit inside the utilisation norm and the non-delivery budget protects '
      'mentoring; above it, they do not, and the residual claimant is extinguished. The second '
      'break occurs at a depth of 0.725, where senior time is no longer sufficient to verify '
      'the volume of machine output the system produces, and the usable share of that output '
      'begins to fall below one. Beyond this point additional automation delivers progressively '
      'less usable work, because the constraint has moved from the machine to the human who '
      'must certify it.'),

('p', 'The two thresholds have different policy implications and this distinction matters for '
      'the design of interventions. The first is a time-allocation threshold and can be moved '
      'by a management decision at zero technological cost, simply by ring-fencing '
      'non-delivery time. The second is a technological threshold and can be moved only by '
      'improving the verifiability of machine output. The ordering also matters: because the '
      'mentoring threshold binds at a much lower depth than the verification threshold, most '
      'firms will encounter the manageable constraint first and will encounter it without '
      'warning, since nothing in the system deteriorates gradually as the threshold '
      'approaches. Consistent with this, the aggregate response is convex: the damage between '
      'depths of 0.475 and 0.95 is 1.76 times the damage between 0.10 and 0.475.'),

('figure', 'p7_fig4.png', 5.45, None, 105),
('figcap', 5, 'Response of the system to asymptotic automation depth. Left: deviation of the '
              'senior stock and of productive capacity from the no-automation counterfactual '
              'at year 30. Right: the two mechanisms that break, showing mentoring per junior '
              'collapsing at a depth of 0.475 and the verifiable share of machine output '
              'falling below one at 0.725.'),

('h2', '4.5. Structural Decomposition: Which Channel, Which Loop'),

('p', 'Table 5 reports the loop-knockout experiments, which test Proposition 3 and produce the '
      'paper’s most counter-intuitive result. Against the full-model gap of −46.3% at year 30, '
      'removing the substitution channel leaves a gap of only −24.4%: task substitution alone '
      'accounts for 21.9 percentage points, almost half the total damage. Removing the '
      'practice-displacement channel leaves −27.0%, so the degradation of learning content in '
      'the entry work that survives accounts for a further 19.3 percentage points. Together, '
      'the two channels that operate directly on entry-level work account for 41.2 of the 46.3 '
      'percentage points. The mentoring loops R1 and R2, by contrast, account for 5.7 '
      'percentage points, and the verification channel for 0.6.'),

('p', 'This ordering contradicts the account that dominates practitioner commentary, in which '
      'AI is said to erode training because it leaves seniors with no time to teach. In this '
      'model automation initially does the opposite: by absorbing routine work it lowers senior '
      'utilisation from 0.856 to 0.742 by year 10, which is why documented mentoring holds at '
      'its reference level for two decades. The mentoring squeeze is real but it is an '
      'amplifier that engages late, once the senior stock has been depleted enough for delivery '
      'obligations to encroach on the non-delivery budget. The policy implication is direct: '
      'interventions aimed at protecting senior teaching time address the third-largest '
      'mechanism, not the first.'),

('p', 'Two further results in Table 5 deserve comment. Channel C2 appears as two rows because '
      'its components pull in opposite directions. Removing the AI-as-tutor component C2b—that is, '
      'assuming firms use AI without any structured learning protocol—deepens the gap from '
      '−46.3% to −55.1%. The offsetting effect of structured practice at the sample mean is '
      'therefore already worth 8.8 percentage points, which is more than the mentoring loops '
      'and the verification channel combined, and it is achieved with no change in headcount '
      'or budget. Removing pool scarring reduces the gap to −39.2%, confirming that the '
      'external, societal consequence of exclusion returns to the firm as a 7.1 percentage '
      'point cost through the quality of the entrants it later hires.'),

('p', 'The last row is the most surprising. Removing the balancing loop B1—the system’s only '
      'self-correcting mechanism—improves the year-30 outcome, from −46.3% to −43.6%. The '
      'scarcity correction is self-defeating. When a shortage of proficient professionals '
      'becomes visible, firms raise desired junior headcount and hire more entrants; but they '
      'hire them into a system whose mentoring capacity is already exhausted, so each '
      'additional junior dilutes the mentoring available to all juniors, lengthens time to '
      'proficiency for the whole cohort, and delays rather than accelerates the recovery of '
      'the senior stock. This is a fixes-that-fail structure of exactly the kind that '
      'Repenning and Sterman describe in process improvement {{capability_traps|nobody_credit}}, '
      'and it explains why the intuitive managerial response to an expertise shortage—hire '
      'more graduates—can make the shortage worse. It also explains why the entry-hiring '
      'subsidy P1, examined next, is effective but inefficient.'),

('tabcap', 5, 'Structural decomposition: contribution of each channel and feedback loop to the '
              'year-30 senior-stock gap.'),
('table', [
    ['Structure removed', 'Parameter set to zero', 'Senior gap at year 30',
     'Contribution'],
    ['Full model (none)', '—', '−46.28%', '—'],
    ['C1 substitution channel', '⟪\\phi⟫', '−24.37%', '21.91 pp of damage'],
    ['C2a practice displacement', '⟪\\theta⟫', '−26.98%', '19.30 pp of damage'],
    ['C2b AI-as-tutor offset', '⟪\\lambda⟫', '−55.12%', '8.84 pp of mitigation'],
    ['C3 verification load', '⟪\\nu⟫', '−45.72%', '0.56 pp of damage'],
    ['R1 and R2 mentoring loops', '⟪a⟫', '−40.55%', '5.73 pp of damage'],
    ['R3 entrant-pool scarring', '⟪\\delta⟫', '−39.16%', '7.12 pp of damage'],
    ['B1 scarcity correction', '⟪w⟫', '−43.57%', '2.71 pp of damage'],
 ], [2800, 1900, 2320, 2600]),
('notes', 'Each row reports the deviation of the senior stock from the no-automation '
          'counterfactual at year 30 when the named structure is disabled. Contributions are '
          'the difference from the full model in percentage points (pp); a positive '
          'contribution of damage means that removing the structure improves the outcome. '
          'Note that the balancing loop B1 contributes damage: hiring more juniors into a '
          'mentoring-constrained system dilutes mentoring and slows recovery.'),

('h2', '4.6. Policy Experiments and Leverage'),

('p', 'Figure 6 and Table 6 report the four policy levers and their combination, each '
      'activated from year 3. All four improve the year-30 senior stock relative to the '
      'unmanaged baseline, but they differ sharply in efficiency, and it is the efficiency '
      'comparison that tests Proposition 4.'),

('p', 'The entry-hiring subsidy P1 raises the senior stock by 24.2% over baseline. It does so '
      'by brute force: it generates 137.8 thousand additional entry hires over thirty years to '
      'produce 450.9 thousand additional senior-years, a ratio of 0.306 additional hires per '
      'additional senior-year. Its conversion rate rises only slightly, from 0.393 to 0.403 '
      'promotions per hire, and remains below the counterfactual value of 0.433, because the '
      'additional juniors enter a pipeline whose learning content is still degraded and whose '
      'mentoring is still constrained. The AI-augmented apprenticeship P3 achieves a slightly '
      'larger gain of 26.0% using 50.4 thousand additional hires to produce 412.6 thousand '
      'additional senior-years—0.122 additional hires per senior-year, or 2.5 times the '
      'efficiency of the subsidy. Its conversion rate rises to 0.453, above the counterfactual, '
      'and its terminal time to proficiency is 6.82 years against 8.65 years under the subsidy '
      'and 16.92 years under the baseline. P3 is the only single lever that leaves the pipeline '
      'structurally better than it would have been without automation at all.'),

('p', 'Protected mentoring time P2 delivers 10.7%. It works exactly as the structural analysis '
      'predicts it should: it prevents the year-23 collapse and it costs almost nothing, but '
      'because the mentoring loops account for only 5.7 percentage points of the damage, its '
      'ceiling is low. Automated verification P4 delivers 7.2% and is the only lever with a '
      'perverse side effect: although it raises the year-30 stock, it yields 22.9 thousand '
      'fewer cumulative senior-years than the baseline, because freeing senior time weakens '
      'the perceived-scarcity signal that drives the balancing loop, so firms hire fewer '
      'juniors in the intervening decades even as capacity improves. This is a clean '
      'illustration of a policy that improves the symptom while removing the information the '
      'system needs to correct itself.'),

('p', 'The integrated portfolio P5 delivers 35.3%, restores conversion efficiency to 0.451 and '
      'is the only configuration whose productive capacity at year 30 exceeds the '
      'no-automation counterfactual, by 4.9%. Its gain is 32.8 percentage points less than the '
      'sum of the four single-lever gains, a sub-additivity that is itself informative: the '
      'levers compete for the same binding constraints, so once mentoring no longer collapses '
      'and learning content is restored, the marginal value of adding entry positions falls. '
      'Under parameter uncertainty, however, the ranking changes in an important way. Over 160 '
      'randomised parameterisations (Table 6, final column), P1 and P3 are positive in 100% of '
      'runs, P2 in 83.1% and P4 in only 63.1%, while P5 averages a gain of 59.8%—larger than '
      'the base-case value and larger than the sum of the individual means. When the location '
      'of the thresholds is uncertain, the portfolio is worth more than the sum of its parts, '
      'because at least one of its components is binding in every draw. For a decision maker '
      'who does not know where the thresholds lie, this is the decisive argument for the '
      'portfolio.'),

('figure', 'p7_fig5.png', 5.35, None, 106),
('figcap', 6, 'Policy experiments. Upper panel: trajectories of the senior stock under four '
              'single levers and the integrated portfolio, all activated in year 3. Lower '
              'left: mean and 5th–95th percentile gain over baseline across 160 randomised '
              'parameterisations. Lower right: conversion efficiency of the pipeline, in '
              'promotions per entry hire, against the no-automation counterfactual.'),

('tabcap', 6, 'Policy experiments: outcomes at year 30, efficiency and robustness.'),
('table', [
    ['Lever', 'Senior stock vs. baseline', 'Capacity vs. baseline',
     'Time to proficiency (yr)', 'Conversion (promotions per hire)',
     'Extra hires per extra senior-year', 'Robustness: mean gain (share positive)'],
    ['P0 baseline', '—', '—', '16.92', '0.393', '—', '—'],
    ['P1 entry-hiring subsidy', '+24.20%', '+11.98%', '8.65', '0.403', '0.306',
     '+22.2% (100%)'],
    ['P2 protected mentoring time', '+10.67%', '+3.01%', '8.76', '0.410', '0.409',
     '+9.8% (83.1%)'],
    ['P3 AI-augmented apprenticeship', '+26.01%', '+10.49%', '6.82', '0.453', '0.122',
     '+21.2% (100%)'],
    ['P4 automated verification', '+7.17%', '+8.39%', '8.79', '0.413', 'undefined',
     '+2.7% (63.1%)'],
    ['P5 integrated portfolio', '+35.30%', '+24.00%', '6.78', '0.451', '0.171',
     '+59.8% (100%)'],
 ], [2060, 1300, 1200, 1150, 1250, 1080, 1600]),
('notes', 'The no-automation counterfactual has a conversion rate of 0.433 promotions per '
          'entry hire and a time to proficiency of 6.56 years. The efficiency ratio is '
          'undefined for P4 because both of its components are negative: relative to the '
          'baseline it yields 22.9 thousand fewer cumulative senior-years and 9.6 thousand '
          'fewer entry hires, even though it raises the year-30 stock, since freeing senior '
          'time weakens the perceived-scarcity signal that drives hiring. Robustness is '
          'computed over '
          '160 Latin-hypercube parameterisations. The sum of the four single-lever base-case '
          'gains is 68.05%, so P5 is sub-additive at the base case (−32.75 pp) but '
          'super-additive in the randomised ensemble.'),

('h2', '4.7. Global Sensitivity and Robustness'),

('p', 'Figure 7 reports the global sensitivity analysis over 500 Latin-hypercube draws across '
      'fifteen parameters. The qualitative conclusion is invariant: the senior-stock gap at '
      'year 30 is negative in 99.6% of runs, with a median of −43.4% and a 5th–95th percentile '
      'range of −58.7% to −24.0%; the capacity gap is negative in 96.8% of runs, with a median '
      'of −30.7%. The entry-hiring decline at year 5 is negative in 98.2% of runs. No '
      'plausible parameter combination in the sampled space produces a system that is better '
      'off in expertise terms after the automation shock.'),

('p', 'The partial rank correlations identify where uncertainty matters. Substitutability '
      'dominates (PRCC = −0.563, ⟪p⟫ < 0.001), followed by asymptotic automation depth '
      '(−0.486), the practice-displacement coefficient (−0.479), the AI-as-tutor coefficient '
      '(+0.402), the reference time to proficiency (+0.359), demand growth (+0.313) and '
      'diffusion speed (−0.293). Three features of this ranking are worth noting. First, the '
      'top four parameters are precisely the four estimated in Study 1 or set by the '
      'technology, which is why estimating rather than assuming them was necessary. Second, '
      'the AI-as-tutor coefficient is the only large positive term: it is the one parameter '
      'that managers can move upward without changing headcount, budget or technology. Third, '
      'the verification load, the mentoring elasticity and the pool-decay rate have partial '
      'rank correlations indistinguishable from zero (⟪p⟫ = 0.974, 0.775 and 0.948 '
      'respectively), even though the knockout tests show that these structures matter. The '
      'apparent contradiction is instructive: their effects are threshold effects, which '
      'appear as discrete switches rather than as monotone gradients, and a rank-correlation '
      'measure is by construction blind to them. Structural tests and sensitivity indices '
      'answer different questions, and a model of this kind requires both.'),

('figure', 'p7_fig6.png', 5.45, None, 107),
('figcap', 7, 'Global sensitivity analysis over 500 Latin-hypercube draws. Left: partial rank '
              'correlation coefficients between each sampled parameter and the year-30 '
              'senior-stock gap; faded bars are not significant at the 5% level. Right: '
              'distribution of the year-30 gap in the senior stock and in productive capacity '
              'relative to the no-automation counterfactual.'),

# ============================================================= 5. Discussion
('h1', '5. Discussion'),

('h2', '5.1. Theoretical Implications'),

('p', 'The paper’s first theoretical contribution is to specify the accumulation that '
      'automation of entry-level work depletes. The literature on the labour-market effects of '
      'generative AI has established, with increasing precision, that exposure is '
      'concentrated on young workers in cognitive routine occupations {{canaries|'
      'seniority_biased|ladder_eig|eloundou_gpts|albanesi_newtech}}. What it has not been able '
      'to establish, because the technology is too new, is what happens to the stock of '
      'expertise when that flow is interrupted for a decade. By modelling time to proficiency '
      'as an endogenous variable that depends on mentoring, on learning content and on cohort '
      'quality, and by letting the senior stock feed back into all three, this paper shows '
      'that the interruption is not merely additive. It converts a transitory hiring shock '
      'into a persistent capability deficit through three reinforcing loops, only one of which '
      'is internal to the firm. This complements the firm-level literature on digital '
      'transformation and labour structure, which measures how adoption changes the '
      'composition of employment but treats the human-capital stock as a contemporaneous '
      'outcome rather than as an accumulation with its own dynamics {{digitrans_emp_firm|'
      'im_hc|career2}}.'),

('p', 'The second contribution is to correct the causal story. The mentoring-squeeze account '
      'is intuitive and is wrong as a description of the initiating mechanism. Study 1 finds '
      'no direct effect of automation depth on mentoring intensity once delivery pressure is '
      'controlled (⟪p⟫ = 0.498), and the simulation shows that automation initially reduces '
      'senior utilisation rather than raising it. The damage is done first by removing entry '
      'positions and second by removing learning content from the positions that remain; the '
      'mentoring squeeze engages only after the senior stock has fallen far enough for '
      'delivery to encroach on the non-delivery budget, at which point it produces an abrupt '
      'regime shift. Distinguishing an initiating mechanism from a late-stage amplifier is not '
      'a semantic refinement. It determines which intervention is worth making, and when.'),

('p', 'The third contribution concerns policy resistance. The finding that the system’s only '
      'balancing loop makes the year-30 outcome worse—by 2.7 percentage points—adds a case to '
      'the capability-trap literature in which the trap is not merely a failure to invest but '
      'an active perversion of the corrective response {{capability_traps|nobody_credit|'
      'capability_erosion}}. The corrective response is the right response to the symptom '
      '(there are too few proficient professionals, so hire more entrants) and the wrong '
      'response to the structure (the constraint is not entrants but the capacity to convert '
      'them). This is the general form of the leverage-point problem: the place where the '
      'symptom appears is rarely the place where the system yields {{leverage_points|'
      'thinking_systems}}. Here the yielding point is the learning content of entry work, a '
      'variable that appears on no organisational chart and in no budget. The result also '
      'qualifies the emerging literature on AI-assisted managerial decision making, which has '
      'concentrated on whether machine advice improves the quality of individual decisions '
      '{{aidm1|csaszar_ai|systems_ai_dm}}. The present analysis shows that a sequence of '
      'individually improved decisions can still produce a systemically worse outcome when '
      'the accumulation being depleted lies outside the decision’s measured horizon.'),

('h2', '5.2. Implications for Leadership and Decision Making'),

('p', 'For executives navigating digital transformation, the results reframe a decision that '
      'is currently framed as a cost question. The relevant question is not how much entry-'
      'level work to automate but how much learning-bearing practice to preserve while '
      'automating it, and these are separable choices. The evidence for their separability is '
      'the interaction term in Study 1: firms at the ninety-fifth percentile of structured '
      'AI-assisted practice suffer no measurable learning penalty from automation at all, and '
      'the practice level at which the penalty vanishes—0.897—lies inside the observed '
      'distribution. Structured practice means specific, auditable protocols: requiring the '
      'junior to attempt the task before consulting the model, requiring review of the '
      'model’s reasoning rather than acceptance of its output, and withdrawing assistance on a '
      'graded schedule as competence develops. None of these requires additional headcount and '
      'all of them are decisions a middle manager can implement. Because these protocols sit '
      'in the social rather than the technical subsystem, they are exactly the class of '
      'complementary redesign that the socio-technical literature identifies as the condition '
      'for technology to raise joint performance, and that digital-leadership research finds '
      'to be the scarcest capability in transforming firms {{sts_ai|sts4|dl1|ceo_digital}}.'),

('p', 'The second implication concerns measurement. The system’s defining feature is that its '
      'damage is invisible for sixteen years on the indicators that firms actually track. '
      'Productive capacity, the closest analogue to a firm-level performance measure in this '
      'model, is above the counterfactual until year 16.6 while entry hiring is already 40% '
      'below it. Any governance system that relies on output measures alone will therefore '
      'receive confirming evidence throughout the period in which the damage is being done. '
      'The model identifies three leading indicators that turn much earlier and can be '
      'monitored at low cost: the ratio of entry hires to promotions, which falls immediately; '
      'the share of senior time absorbed by verification of machine output, which rises from '
      '1.4% to 37.1% and is directly measurable from timesheets; and documented mentoring '
      'hours per junior, which is the residual claimant and therefore the first thing to '
      'disappear when delivery pressure rises. Boards that wish to know whether their firm is '
      'entering the trap should ask for these three series rather than for productivity.'),

('p', 'The third implication is about the timing of intervention. Because mentoring is a '
      'residual claimant, it does not degrade gradually; it holds at its reference level for '
      'two decades and then collapses within a year or two once the threshold is crossed. A '
      'management system that waits for a deterioration signal will receive none until the '
      'regime has already shifted. Protection of non-delivery time must therefore be '
      'established before it appears necessary—which is precisely the class of decision that '
      'delivery-focused performance measurement is least likely to authorise '
      '{{people_mgmt|managers_productivity}}.'),

('h2', '5.3. Implications for Policy'),

('p', 'For public policy, the efficiency comparison in Table 6 argues against the instrument '
      'that is currently most popular. Entry-hiring subsidies work—they are positive in 100% '
      'of randomised runs—but they require 0.306 additional entry hires per additional '
      'senior-year created, against 0.122 for an intervention that restores the learning '
      'content of entry work, and they leave the pipeline’s conversion rate below its '
      'pre-automation value. A subsidy adds throughput to a pipeline whose yield has fallen; '
      'the alternative repairs the yield. Since the fiscal cost of a hiring subsidy scales '
      'with the number of hires and the cost of a practice standard does not, the difference '
      'in real resource terms is larger than the ratio suggests.'),

('p', 'The policy instrument the analysis supports is therefore closer to a training standard '
      'than to a wage subsidy: certification of AI-assisted apprenticeship protocols, '
      'conditioning of existing training subsidies on documented structured practice, and '
      'sectoral agreements on protected non-delivery time. This has a precedent in the '
      'apprenticeship systems whose cost–benefit structure is well documented, where the '
      'public role is to make firm-level training investments recoverable rather than to pay '
      'for headcount {{appr_roi|appr_cycle|appr_costs}}. The analysis also strengthens the '
      'case for treating youth exclusion as an efficiency problem and not only an equity '
      'problem: pool scarring returns 7.1 percentage points of the senior-stock deficit back '
      'to firms through the declining employability of the cohorts they later hire, so the '
      'social cost of a long queue is partly borne by the firms that created it '
      '{{scarring_meta|vonwachter20|ilo_get2024|oecd_eo2025}}. This connects the analysis to '
      'the substantial literature on youth transitions, which shows that the institutional '
      'design of the school-to-work interface, the coverage of vocational tracks and the '
      'reach of activation programmes determine how long the queue becomes and who joins it '
      '{{stw|vet1|yg|ilo2}}.'),

('p', 'Finally, the robustness results argue for a portfolio rather than a single instrument. '
      'No single lever is positive in all randomised parameterisations except P1 and P3, and '
      'the portfolio outperforms the sum of its parts under uncertainty precisely because the '
      'binding constraint differs across parameter draws. When the location of a threshold is '
      'unknown, redundancy in the policy mix is not waste but insurance.'),

('h2', '5.4. Limitations and Future Research'),

('p', 'Four limitations bound the claims. First, Study 1 is cross-sectional, so the parameters '
      'it supplies are associations conditioned on observables rather than causal effects; '
      'firms that automate more deeply may differ in unmeasured ways from firms that do not. '
      'We mitigate this by controlling for size, age, R&D intensity and sector, by using '
      'administrative quantities rather than perceptions, and by sampling each parameter over '
      'wide ranges in the sensitivity analysis, but a panel or a staggered-adoption design '
      'would be stronger. Second, automation depth is exogenous in the simulation. This is '
      'conservative, since endogenising the pressure to automate under senior scarcity would '
      'close an additional reinforcing loop and worsen the outcome, but it means the model '
      'cannot represent firms that slow adoption in response to a training shortage. Third, '
      'the model has a single occupational system with no wage mechanism and no inter-regional '
      'mobility; in reality a firm facing senior scarcity can bid seniors away from other '
      'firms, which redistributes the shortage without resolving it and would require a '
      'multi-firm or multi-region extension to represent properly. Fourth, the sample is drawn '
      'from one region of one country, and institutional context plausibly moderates the '
      'crowd-out ratio and the mentoring elasticity; replication in economies with strong '
      'formal apprenticeship institutions, or in settings where youth labour-market entry is '
      'organised differently, would be a direct test of whether those institutions raise the '
      'mentoring threshold {{stw|basol|china_youth2}}.'),

('p', 'Three extensions follow naturally. The most valuable would be a longitudinal '
      'parameterisation: as more years of AI-exposure data accumulate, the model’s early '
      'trajectory can be tested against observed hiring and promotion series rather than '
      'against a single published magnitude. A second extension would endogenise the '
      'technology by letting verifiability improve with cumulative use, which would move the '
      'second threshold and might reverse the ranking of P3 and P4. A third would embed the '
      'model in a participatory setting with firms and regional authorities, using it as a '
      'boundary object for negotiating training standards—the use for which small, transparent '
      'system dynamics models are best suited {{small_models|workforce_multimethod}}.'),

# ============================================================ 6. Conclusions
('h1', '6. Conclusions'),

('p', 'Generative artificial intelligence automates the tasks through which professions '
      'reproduce themselves. This paper has asked what that does to the stock of expertise '
      'over three decades, and which decisions can repair it. Combining an enterprise survey '
      'of 356 knowledge-intensive firms with a validated five-stock system dynamics model, we '
      'find that the erosion is severe, delayed and initially invisible. The stock of '
      'proficient professionals ends 46.3% below the no-automation counterfactual, but '
      'productive capacity first rises 8.7% above it and does not cross back below until year '
      '16.6, by which time more than a decade of entry cohorts has been foregone. The system '
      'contains two regime shifts, at automation depths of 0.475 and 0.725, at which mentoring '
      'and verification capacity respectively give way without prior warning.'),

('p', 'The structural decomposition relocates the mechanism. Task substitution and the loss of '
      'learning content in surviving entry work account for 41.2 of the 46.3 percentage-point '
      'deficit; the mentoring squeeze, which dominates practitioner commentary, accounts for '
      '5.7 and engages only after year 23. The system’s only self-correcting loop is '
      'self-defeating, worsening the year-30 outcome by 2.7 percentage points, because hiring '
      'more graduates into a mentoring-constrained pipeline dilutes the resource that converts '
      'them.'),

('p', 'The leverage point follows directly. Restoring the learning content of entry work is '
      '2.5 times more efficient than subsidising entry hiring per additional senior-year '
      'created, raises the pipeline’s conversion rate above its pre-automation level, and '
      'requires no additional headcount—only auditable protocols governing how AI assistance '
      'is used while juniors learn. Study 1 shows that the firms already at the top of the '
      'observed practice distribution suffer no measurable learning penalty from automation at '
      'all. The choice facing leaders is therefore not whether to automate entry-level work. '
      'It is whether to preserve the practice inside it, and that choice is still open.'),

# ============================================================== back matter
('back', 'Author Contributions:',
 'Conceptualization, X.C. and T.M.; methodology, X.C.; software, X.C.; validation, X.C., D.H. '
 'and T.M.; formal analysis, X.C.; investigation, D.H.; resources, T.M.; data curation, D.H.; '
 'writing—original draft preparation, X.C.; writing—review and editing, T.M.; visualization, '
 'X.C. and D.H.; supervision, T.M.; project administration, T.M.; funding acquisition, X.C. '
 'All authors have read and agreed to the published version of the manuscript.'),
('back', 'Funding:',
 'This research was funded by the Zhejiang Provincial Philosophy and Social Sciences Planning '
 'Special Project on Higher Education Basic Research Funding Reform (Grant Number: '
 '25NDJC153YBMS) and the Major Humanities and Social Sciences Research Projects in Zhejiang '
 'Higher Education Institutions (Grant Number: 2024QN018).'),
('back', 'Institutional Review Board Statement:',
 'The study was conducted in accordance with the Declaration of Helsinki and approved by the '
 'Academic Ethics Committee of the College of Business, Jiaxing University (protocol code '
 'JXU-BUS-2026-034, approved on 18 February 2026).'),
('back', 'Informed Consent Statement:',
 'Informed consent was obtained from all respondents involved in the study.'),
('back', 'Data Availability Statement:',
 'The simulation model, the complete parameter set, the survey instrument and the code that '
 'generates every figure and table in this paper are available from the corresponding author '
 'on reasonable request. Firm-level survey responses cannot be shared because respondents were '
 'assured of confidentiality.'),
('back', 'Conflicts of Interest:', 'The authors declare no conflicts of interest.'),

('h1', 'Abbreviations'),
('p', 'The following abbreviations are used in this manuscript: AI, artificial intelligence; '
      'ATA, automation of the entry task bundle; CI, confidence interval; HC3, '
      'heteroskedasticity-consistent covariance estimator of type 3; JSH, junior staffing '
      'intensity; LHS, Latin hypercube sampling; MEN, mentoring intensity; OLS, ordinary least '
      'squares; PRCC, partial rank correlation coefficient; PRS, delivery pressure; SAL, '
      'structured AI-assisted learning practice; SD, standard deviation; TTP, time to '
      'proficiency; VIF, variance inflation factor; VNU, verification load; YRD, Yangtze River '
      'Delta.'),

# ============================================================== Appendix A
('h1', 'Appendix A'),
('p', 'Table A1 lists every parameter of the simulation model, its base-case value, its source '
      'and the range over which the global sensitivity analysis samples it. Behavioural '
      'parameters are estimated in Study 1; physical parameters are set from published sources '
      'or derived so that the pre-shock system is in equilibrium. Sampling ranges are at least '
      'three standard errors wide for estimated parameters and are widened where the '
      'split-sample analysis in Section 4.1 indicates heterogeneity across firm sizes.'),

('tabcap', 'A1', 'Parameters of the system dynamics model.'),
('table', [
    ['Symbol', 'Meaning', 'Unit', 'Base case', 'Source', 'Sensitivity range'],
    ['⟪D_{0}⟫', 'Professional workload', '10³ task units yr⁻¹', '822.7', 'Derived (equilibrium)', '—'],
    ['⟪g⟫', 'Workload growth rate', 'yr⁻¹', '0.000', 'Stationary base case', '0.000–0.018'],
    ['⟪G⟫', 'Qualified graduate inflow', '10³ persons yr⁻¹', '40.0', 'Derived (equilibrium)', '—'],
    ['⟪\\sigma⟫', 'Complex-work share of workload', 'share', '0.30', 'Published task studies', '0.24–0.36'],
    ['⟪A_{0}⟫', 'Pre-shock automation depth', 'share', '0.05', 'Study 1 lower decile', '—'],
    ['⟪A_{max}⟫', 'Asymptotic automation depth', 'share', '0.70', 'Task-exposure estimates', '0.55–0.85'],
    ['⟪c⟫', 'Diffusion speed', 'yr⁻¹', '0.40', 'Logistic fit to adoption', '0.28–0.55'],
    ['⟪\\pi_{J}⟫', 'Junior output per year', 'task units', '1.60', 'Derived (equilibrium)', '—'],
    ['⟪\\pi_{S}⟫', 'Senior output per year', 'task units', '2.70', 'Derived (equilibrium)', '—'],
    ['⟪u^{∗}⟫', 'Senior delivery-utilisation norm', 'share', '0.88', 'Study 1 (PRS)', '0.84–0.92'],
    ['⟪j_{0}⟫', 'Junior requirement at zero automation', 'junior-yr per task unit', '0.13497', 'Study 1 (JSH)', '—'],
    ['⟪\\phi⟫', 'AI–junior substitutability', 'dimensionless', '0.605', 'Study 1, Model A', '0.45–0.78'],
    ['⟪\\nu⟫', 'Verification load', 'senior-yr per output unit', '0.136', 'Study 1 (VNU)', '0.08–0.185'],
    ['⟪\\tau_{0}⟫', 'Reference time to proficiency', 'yr', '6.02', 'Study 1, Model D', '5.0–7.2'],
    ['⟪m^{∗}⟫', 'Reference mentoring intensity', 'senior-yr per junior', '0.102', 'Study 1, Model C', '0.075–0.13'],
    ['⟪m_{f}⟫', 'Informal-learning floor', 'share of ⟪m^{∗}⟫', '0.30', 'Assumption', '—'],
    ['⟪a⟫', 'Mentoring elasticity of proficiency', 'dimensionless', '0.446', 'Study 1, Model D', '0.30–0.62'],
    ['⟪\\theta⟫', 'Practice-displacement coefficient', 'dimensionless', '0.574', 'Study 1, Model D', '0.35–0.75'],
    ['⟪\\lambda⟫', 'AI-as-tutor coefficient at mean practice', 'dimensionless', '0.265', 'Study 1, Model D', '0.08–0.38'],
    ['⟪\kappa⟫', 'Cohort-quality elasticity', 'dimensionless', '0.40', 'Assumption', '—'],
    ['⟪\\tau_{J}⟫', 'Junior exit time', 'yr', '5.0', 'Turnover statistics', '—'],
    ['⟪\\tau_{S}⟫', 'Senior exit time', 'yr', '17.0', 'Turnover statistics', '14.0–20.0'],
    ['⟪b⟫', 'Junior quits returning to the pool', 'share', '0.55', 'Assumption', '—'],
    ['⟪\\tau_{H}⟫', 'Hiring adjustment time', 'yr', '1.20', 'Assumption', '—'],
    ['⟪\\tau_{M}⟫', 'Pool-to-vacancy matching time', 'yr', '0.60', 'Assumption', '—'],
    ['⟪\\tau_{P}⟫', 'Discouragement exit time from pool', 'yr', '6.0', 'Scarring literature', '—'],
    ['⟪\\delta⟫', 'Skill-decay rate in the pool', 'yr⁻¹', '0.115', 'Scarring literature', '0.07–0.165'],
    ['⟪w⟫', 'Scarcity response of desired juniors', 'dimensionless', '0.55', 'Assumption', '0.30–0.80'],
    ['⟪\\tau_{W}⟫', 'Scarcity perception delay', 'yr', '5.0', 'Assumption', '—'],
 ], [1000, 3080, 1700, 1000, 1580, 1280]),
('notes', 'Parameters marked “Derived (equilibrium)” are set jointly so that the pre-shock '
          'system is stationary at a senior utilisation of 0.856 and a capacity-to-workload '
          'ratio of 1.095. Integration is by fourth-order Runge–Kutta with a step of 0.05 '
          'years over a 30-year horizon; the model is initialised by simulating to equilibrium '
          'for 200 years with automation frozen at ⟪A_{0}⟫.'),
]
