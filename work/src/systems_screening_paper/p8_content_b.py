# -*- coding: utf-8 -*-
"""Paper 8, Part B: Results, Discussion, Conclusions, back matter, Appendix A."""

PART_B = [
# ================================================================ 4. Results
('h1', '4. Results'),

('h2', '4.1. Sample and Data Quality'),

('p', 'The 452 respondents were distributed across software and IT services (175 firms), '
      'professional and business services (147) and finance and shared-service operations '
      '(130), and across size bands from 20 to 99 employees (155) to 1000 or more (33). '
      'Respondents had a mean of 8.3 years of experience in hiring decisions (SD 4.3) '
      'and 51.8% were women. On average they judged 55.4% of the applications they receive to '
      'be AI-assisted (SD 14.9), reported application volume growth of 68.1% over the two '
      'preceding recruitment cycles (SD 48.0, median 57.4%), and scored 0.446 on the '
      'digital-transformation depth of their hiring function (SD 0.201). The opt-out was '
      'taken in 11.5% of tasks, which is high enough to confirm that respondents were not '
      'mechanically choosing one of the two profiles and low enough to leave the attribute '
      'coefficients well identified.'),

('h2', '4.2. What Employers Weight'),

('p', 'Table 2 reports the conditional logit and the mixed logit. The conditional logit '
      'attains a McFadden pseudo-⟪R^{2}⟫ of 0.210 against the equal-shares null, which is '
      'squarely in the range expected for a well-specified choice model, and its gradient '
      'norm at the optimum is 2.1 × 10⁻⁷. All seven attributes carry coefficients in the '
      'expected direction and all are significant at the 0.1% level. The mixed logit fits '
      'substantially better: the likelihood-ratio statistic against the conditional logit '
      'is 448.8 on 10 degrees of freedom (⟪p⟫ < 0.001), so the assumption that all '
      'employers screen by the same rule is decisively rejected.'),

('p', 'The pattern of the standard deviations is as informative as the means. Employers '
      'differ most in how much they value a process-evidence portfolio '
      '(⟪\\sigma⟫ = 0.812, ⟪z⟫ = 13.10) and in how far that portfolio offsets disclosure '
      '(⟪\\sigma⟫ = 0.927, ⟪z⟫ = 8.40), and they differ substantially on institution '
      '(0.602) and referral (0.680). They differ hardly at all, however, in the penalty '
      'they attach to disclosure itself (⟪\\sigma⟫ = 0.208, ⟪z⟫ = 0.99, not significant). '
      'Disapproval of undocumented AI use is close to universal; what varies is whether '
      'documentation is accepted as a remedy.'),

('tabcap', 2, 'Conditional logit and mixed logit estimates of the screening rule.'),
('table', [
    ['Attribute', 'Conditional logit ⟪b⟫ (SE)', 'Mixed logit mean (SE)',
     'Mixed logit SD (SE)'],
    ['Disclosed AI assistance', '−0.566 *** (0.106)', '−0.741 *** (0.129)',
     '0.208 (0.210)'],
    ['Process-evidence portfolio', '0.257 *** (0.062)', '0.274 *** (0.077)',
     '0.812 *** (0.062)'],
    ['Disclosure × process evidence', '0.427 *** (0.128)', '0.562 *** (0.153)',
     '0.927 *** (0.110)'],
    ['Verified assessment, 70th pct', '0.493 *** (0.056)', '0.656 *** (0.071)',
     '0.165 * (0.081)'],
    ['Verified assessment, 90th pct', '0.841 *** (0.066)', '1.084 *** (0.081)',
     '0.486 *** (0.079)'],
    ['Elite institution', '0.594 *** (0.058)', '0.776 *** (0.074)', '0.602 *** (0.074)'],
    ['Employee referral', '0.589 *** (0.054)', '0.736 *** (0.069)', '0.680 *** (0.070)'],
    ['Relevant internship', '0.364 *** (0.043)', '0.490 *** (0.056)', '0.317 *** (0.065)'],
    ['Expected salary (+1000 CNY)', '−0.334 *** (0.012)', '−0.425 *** (0.016)',
     '0.128 *** (0.024)'],
    ['Opt-out constant', '−0.286 *** (0.073)', '−0.189 * (0.090)', '0.485 *** (0.127)'],
    ['Log-likelihood', '−5492.4', '−5267.9', ''],
    ['McFadden ⟪R^{2}⟫', '0.210', '0.242', ''],
    ['AIC / BIC', '11005 / 11046', '10576 / 10658', ''],
    ['Choice sets / respondents', '6328 / 452', '6328 / 452', ''],
 ], [2560, 2420, 2420, 2240]),
('notes', '*** ⟪p⟫ < 0.001, * ⟪p⟫ < 0.05. Conditional logit standard errors are clustered '
          'by respondent; mixed logit standard errors are the sandwich estimator from the '
          'respondent-level scores and the numerical Hessian. The mixed logit uses 500 '
          'scrambled Halton draws; the largest absolute gradient at the optimum is '
          '7.0 × 10⁻⁴. Standard deviations are reported as absolute values, since the sign '
          'of a normal mixing parameter is not identified.'),

('figure', 'p8_fig3.png', 5.45, None, 103),
('figcap', 3, 'Mixed logit estimates. Left: mean part-worth utilities with 95% confidence '
              'intervals. Right: the estimated standard deviation of each part-worth, '
              'which measures how far employers differ from one another on that attribute.'),

('h2', '4.3. The Disclosure Penalty and Its Repair'),

('p', 'Hypothesis 1 is supported. An application that states it was produced with '
      'generative-AI assistance is penalised: the coefficient is −0.741 (SE 0.129, '
      '⟪z⟫ = −5.73, ⟪p⟫ < 0.001) when no process evidence accompanies it. Expressed as a '
      'compensating differential, an applicant who discloses must ask for 1743 CNY per '
      'month less in expected salary to be regarded as equally attractive (95% CI 1165 to '
      '2321 CNY), which against a mid-level expectation of 10,000 CNY is a penalty of about '
      'a sixth of pay.'),

('p', 'Hypothesis 2 is also supported, and it is the more consequential result. The '
      'interaction between disclosure and process evidence is positive and significant '
      '(0.562, SE 0.153, ⟪p⟫ < 0.001). When the applicant supplies a portfolio documenting '
      'drafts, revisions and reasoning, the penalty falls to −0.179 (SE 0.078, ⟪z⟫ = −2.29, '
      '⟪p⟫ = 0.022), equivalent to 421 CNY per month. Documentation therefore removes about '
      'three quarters of the disclosure penalty. The residual penalty remains statistically '
      'distinguishable from zero, so evidence does not make disclosure costless, but it '
      'converts a substantial deterrent into a marginal one. Figure 4 shows both quantities '
      'together with the full set of compensating differentials.'),

('p', 'Hypothesis 3 is supported. Verified assessment results carry a large and monotone '
      'premium: 0.656 at the 70th percentile and 1.084 at the 90th, equivalent to 1542 and '
      '2549 CNY per month respectively. The 90th-percentile premium exceeds the elite '
      'institution premium of 1825 CNY, and its confidence interval (2198 to 2899) does not '
      'overlap the institution interval (1487 to 2163). Employers are willing to pay more '
      'for demonstrated capability than for institutional pedigree—when the demonstration '
      'is verified. This is the same ordering that field experiments providing credibly '
      'shareable assessment results have found in real labour markets '
      '{{limited_information|inefficient_entry}}, which is reassuring for the external '
      'validity of the stated-choice estimates.'),

('figure', 'p8_fig4.png', 5.45, None, 104),
('figcap', 4, 'Left: the utility penalty for disclosing generative-AI assistance, without '
              'and with a process-evidence portfolio; the difference between the two bars '
              'is the interaction term. Right: every attribute expressed as a compensating '
              'differential in expected monthly salary. Bars are 95% confidence intervals '
              'from the delta method.'),

('h2', '4.4. Three Screening Regimes'),

('p', 'Table 3 reports the latent-class selection. The Bayesian and consistent Akaike '
      'information criteria both reach their minimum at three classes (BIC 10,483.4; CAIC '
      '10,515.4), and we retain that solution. Average posterior class-assignment '
      'probability is 0.870 and the entropy criterion is 0.715, indicating good but not '
      'perfect separation; the two-class solution separates more cleanly (0.816) but fits '
      'markedly worse, which is the familiar trade-off between parsimony of classification '
      'and adequacy of fit.'),

('tabcap', 3, 'Latent-class selection and class-specific part-worths.'),
('table', [
    ['Classes', 'Log-likelihood', 'Parameters', 'BIC', 'CAIC', 'Entropy'],
    ['2', '−5197.5', '21', '10,523.4', '10,544.4', '0.816'],
    ['3 (retained)', '−5143.9', '32', '10,483.4', '10,515.4', '0.715'],
    ['4', '−5119.8', '43', '10,502.4', '10,545.4', '0.734'],
    ['5', '−5109.0', '54', '10,548.1', '10,602.1', '0.689'],
 ], [1740, 2000, 1600, 1500, 1500, 1300]),

('table', [
    ['Attribute', 'C1 credential retreat (38.1%)', 'C2 assessment triage (28.4%)',
     'C3 evidence weighting (33.5%)'],
    ['Disclosed AI assistance', '−1.17', '−0.77', '0.06'],
    ['Process-evidence portfolio', '−0.08', '0.20', '1.02'],
    ['Disclosure × process evidence', '0.38', '0.69', '0.30'],
    ['Verified assessment, 70th pct', '0.26', '0.79', '0.64'],
    ['Verified assessment, 90th pct', '0.45', '1.76', '0.82'],
    ['Elite institution', '1.40', '0.29', '0.22'],
    ['Employee referral', '1.39', '0.35', '0.10'],
    ['Relevant internship', '0.42', '0.15', '0.59'],
    ['Expected salary (+1000 CNY)', '−0.30', '−0.51', '−0.36'],
 ], [2860, 2260, 2260, 2260]),
('notes', 'Class-specific part-worth utilities from the three-class latent-class '
          'conditional logit. Class labels are identified only up to a permutation; '
          'classes are ordered here by their institution coefficient. Shares are the '
          'estimated class probabilities.'),

('p', 'The three regimes are readily interpretable and correspond closely to the three '
      'responses to signal collapse set out in Section 2.3. The largest class, holding '
      '38.1% of respondents, is a credential-retreat regime: institution (1.40) and '
      'referral (1.39) dominate, verified assessment barely registers (0.45 at the 90th '
      'percentile), process evidence is worthless (−0.08), and the disclosure penalty is '
      'the largest of the three (−1.17). The second class, 28.4%, is an assessment-triage '
      'regime that loads almost everything onto the verified test (1.76 at the 90th '
      'percentile) and discounts institution and referral. The third, 33.5%, is an '
      'evidence-weighting regime that values the process portfolio most (1.02) and, '
      'strikingly, attaches no penalty at all to disclosure (0.06). Figure 5 displays the '
      'selection criteria and the class profiles.'),

('p', 'That last coefficient deserves emphasis. Roughly a third of the employers in this '
      'sample do not penalise an applicant for saying that they used generative AI, '
      'provided the applicant can show how the work was done. The disclosure penalty '
      'reported in Section 4.3 is therefore not a uniform professional norm but the average '
      'of a strong penalty in one regime and no penalty in another. Averaging conceals the '
      'thing that matters most to an applicant deciding whether to be candid.'),

('figure', 'p8_fig5.png', 5.45, None, 105),
('figcap', 5, 'Left: information criteria by number of latent classes; both reach their '
              'minimum at three. Right: class-specific part-worth utilities for the three '
              'retained screening regimes, with class shares in the legend.'),

('h2', '4.5. Which Employers Screen Which Way'),

('p', 'Table 4 reports the membership model, with the credential-retreat regime as the '
      'reference. Hypothesis 5 is supported. Managers who believe a larger share of their '
      'applications are AI-assisted are significantly less likely to be in the '
      'evidence-weighting regime than in the credential-retreat regime (−0.683, SE 0.146, '
      '⟪p⟫ < 0.001) and somewhat less likely to be in the assessment-triage regime (−0.231, '
      'SE 0.149, ⟪p⟫ = 0.122). Faster growth in application volume works the same way, '
      'pushing membership towards credential retreat and away from both alternatives '
      '(−0.376, ⟪p⟫ = 0.007 for triage; −0.449, ⟪p⟫ = 0.001 for evidence weighting). This '
      'is the retreat the theory predicts: as the written signal becomes less trustworthy '
      'and the pile grows, decision makers fall back on the signals the applicant did not '
      'produce.'),

('p', 'The depth of digital transformation of the hiring function works in the opposite '
      'direction, and strongly: it raises the probability of the assessment-triage regime '
      '(0.811, ⟪p⟫ < 0.001) and of the evidence-weighting regime (0.546, ⟪p⟫ < 0.001) '
      'relative to credential retreat. Firms that have actually rebuilt their hiring process '
      'do not retreat to pedigree; they install verification. Centralisation of the '
      'screening decision, firm size and respondent experience are not significant, which '
      'suggests that the regime is a property of the firm’s screening system rather than of '
      'the individual who happens to operate it. Figure 6 plots the predicted membership '
      'probabilities across the two signal-environment variables.'),

('tabcap', 4, 'Membership model: multinomial logit on posterior class probabilities.'),
('table', [
    ['Covariate (standardised)', 'C2 assessment triage vs. C1',
     'C3 evidence weighting vs. C1'],
    ['Digital-transformation depth of hiring', '0.811 *** (0.144)', '0.546 *** (0.140)'],
    ['Perceived AI-assisted share', '−0.231 (0.149)', '−0.683 *** (0.146)'],
    ['Application-volume growth', '−0.376 ** (0.138)', '−0.449 ** (0.138)'],
    ['Decision centralisation', '0.095 (0.125)', '−0.049 (0.121)'],
    ['Firm size (log employees)', '0.061 (0.126)', '0.189 (0.120)'],
    ['Respondent experience', '0.035 (0.125)', '0.086 (0.120)'],
    ['Intercept', '−0.271 * (0.129)', '−0.113 (0.124)'],
    ['Log-likelihood', '−446.3', ''],
 ], [3560, 3040, 3040]),
('notes', '*** ⟪p⟫ < 0.001, ** ⟪p⟫ < 0.01, * ⟪p⟫ < 0.05. The reference category is the '
          'credential-retreat regime (C1). Estimated on posterior class probabilities '
          'rather than modal assignments, so classification uncertainty is carried into '
          'the second stage.'),

('figure', 'p8_fig6.png', 5.45, None, 106),
('figcap', 6, 'Predicted probability of belonging to each screening regime as a function '
              'of the perceived share of AI-assisted applications (left) and of growth in '
              'application volume (right), holding the remaining covariates at their means.'),

('h2', '4.6. Predictive Validity'),

('p', 'Hypothesis 4 requires that discrete heterogeneity earn its parameters out of '
      'sample, not merely in sample. We therefore re-estimated every model on each '
      'respondent’s first nine tasks and predicted their last five, forming the mixed-logit '
      'and latent-class predictions from each respondent’s posterior distribution over '
      'tastes given the training choices. Against a chance rate of 33.3%, the conditional '
      'logit predicts 59.9% of the 2260 held-out choices correctly, the mixed logit 63.5% '
      'and the latent-class model 64.3%; mean held-out log-likelihood improves in the same '
      'order, from −0.885 to −0.840 to −0.818. Discrete regimes therefore predict better '
      'than a continuous mixing distribution with the same information, which supports the '
      'substantive reading of the classes as screening regimes rather than as a convenient '
      'approximation to a smooth distribution.'),

('h2', '4.7. The Architecture Experiment'),

('p', 'The conjoint holds the interface fixed and lets preferences vary. The randomised '
      'experiment does the reverse, and it produces the paper’s largest effects. Table 5 '
      'and Figure 7 report the three outcomes.'),

('p', 'Access differs sharply by architecture. The share of the five-person shortlist drawn '
      'from non-elite institutions is 42.5% under the AI-score-first interface, 31.1% under '
      'the credential-first interface and 52.4% under the evidence-first interface, '
      '⟪F⟫(2, 449) = 97.10, ⟪p⟫ < 0.001, ⟪\\eta^{2}⟫ = 0.302; the Alexander–Govern test for '
      'unequal variances agrees (⟪A⟫ = 150.11, ⟪p⟫ < 0.001). The gap between the '
      'credential-first and evidence-first architectures is 21.3 percentage points, a '
      'Cohen’s ⟪d⟫ of 1.61, and it survives adjustment for firm covariates in the '
      'regression of Equation (11) (credential-first −0.113, evidence-first +0.097, both '
      '⟪p⟫ < 0.001; ⟪R^{2}⟫ = 0.327).'),

('p', 'The result that matters for practice is what happens to quality at the same time. '
      'If the credential ordering were selecting genuinely stronger candidates, the '
      'evidence-first architecture would buy access at the cost of quality. It does not. '
      'The mean verified-assessment percentile of the shortlist is 63.7 under AI-score '
      'first, 60.6 under credential first and 69.2 under evidence first, '
      '⟪F⟫(2, 449) = 43.25, ⟪p⟫ < 0.001, ⟪\\eta^{2}⟫ = 0.162. The evidence-first '
      'architecture produces shortlists that are simultaneously 21.3 percentage points more '
      'open to non-elite institutions and 8.6 percentile points stronger on verified '
      'assessment than the credential-first architecture (⟪d⟫ = 1.08). Hypothesis 6 is '
      'supported in both of its parts, and the equity–quality trade-off that managers '
      'commonly assume turns out to be a property of the funnel rather than of the '
      'applicant pool. The direction is consistent with algorithmic screening built to '
      'explore rather than to imitate past hiring, which likewise improves quality and '
      'diversity together {{hiring_exploration|ai_assisted_recruit}}.'),

('p', 'The architecture is not free. Screening under the evidence-first interface took 57.6 '
      'seconds per applicant against 41.4 under credential first, ⟪F⟫(2, 449) = 90.84, '
      '⟪p⟫ < 0.001, ⟪\\eta^{2}⟫ = 0.288—roughly 16 additional seconds, or about 39% more '
      'time. For a firm screening a thousand applications this is an additional four and a '
      'half hours of managerial time per round. That is the real price of the better '
      'shortlist, and it is a price a leadership team can decide to pay.'),

('tabcap', 5, 'The randomised screening-architecture experiment: outcomes by arm.'),
('table', [
    ['Outcome', 'AI-score first (⟪n⟫ = 151)', 'Credential first (⟪n⟫ = 151)',
     'Evidence first (⟪n⟫ = 150)', '⟪F⟫(2, 449)', '⟪\\eta^{2}⟫'],
    ['Non-elite share of shortlist', '0.425 (0.133)', '0.311 (0.144)', '0.524 (0.120)',
     '97.10 ***', '0.302'],
    ['Mean assessment percentile', '63.70 (8.38)', '60.65 (7.89)', '69.20 (7.98)',
     '43.25 ***', '0.162'],
    ['Seconds per applicant', '44.65 (12.12)', '41.41 (9.88)', '57.58 (10.92)',
     '90.84 ***', '0.288'],
 ], [2380, 1740, 1740, 1740, 1120, 920]),
('notes', 'Cell entries are means with standard deviations in parentheses. '
          '*** ⟪p⟫ < 0.001. Pairwise comparisons use Welch’s test with Bonferroni '
          'adjustment. Evidence first versus credential first: non-elite share '
          '⟪d⟫ = 1.61, assessment percentile ⟪d⟫ = 1.08, seconds per applicant '
          '⟪d⟫ = 1.55, all ⟪p⟫ < 0.001. The candidate pool was identical across arms, so '
          'differences are caused by the ordering and salience of information alone.'),

('figure', 'p8_fig7.png', 5.45, None, 107),
('figcap', 7, 'The randomised screening-architecture experiment. The same twenty-candidate '
              'pool was shown to every respondent; only the ordering and salience of '
              'information differed. Bars are means with 95% confidence intervals.'),

# ============================================================= 5. Discussion
('h1', '5. Discussion'),

('h2', '5.1. Theoretical Implications'),

('p', 'The paper’s first contribution is to put a price on a signalling failure. Signalling '
      'theory predicts that when a signal becomes cheap it stops separating types '
      '{{spence73}}, and recent platform evidence documents exactly that collapse for '
      'written applications {{cover_letters_ai|making_talk_cheap}}. What has been missing '
      'is the employer’s side of the adjustment: given that the written application no '
      'longer informs, what do decision makers substitute towards, and how much is each '
      'substitute worth? Expressing every attribute as a compensating differential answers '
      'that question in a common metric. The verified assessment is worth more than the '
      'elite credential, the elite credential and the referral are worth about the same as '
      'each other, and the internship is worth about half as much as the top assessment '
      'result. Employers, in other words, are not indifferent between restoring a costly '
      'signal and retreating to an ascriptive one; they prefer the costly signal when it is '
      'available. The problem is that it is usually not available, because almost no '
      'applicant arrives with a verified assessment result.'),

('p', 'The second contribution is to identify a repair mechanism that does not require new '
      'infrastructure. Process evidence works because it restores the cost asymmetry at the '
      'level of the work rather than the level of the credential: a model can produce a '
      'polished output cheaply but cannot cheaply fabricate a credible record of one '
      'particular person’s iterative reasoning about one particular problem. Empirically it '
      'removes about three quarters of the disclosure penalty, and in the evidence-weighting '
      'regime it removes all of it. This reframes the disclosure debate. The policy question '
      'is usually posed as whether applicants should be required to declare AI use, which '
      'invites an unenforceable answer; the more productive question is what would have to '
      'accompany a declaration to make it informative.'),

('p', 'The third contribution is to show that employer heterogeneity here is discrete. The '
      'latent-class model beats the mixed logit out of sample despite the mixed logit having '
      'a more flexible mixing distribution, and the recovered classes map onto the three '
      'theoretical responses to signal collapse rather than onto arbitrary regions of a '
      'continuum. This matters for how the literature models employer behaviour. A '
      'population-average part-worth for disclosure of −0.741 describes no actual employer: '
      'it averages a −1.17 penalty in the credential regime against a coefficient '
      'indistinguishable from zero in the evidence regime. Advice to applicants derived from '
      'the average would be wrong for roughly two thirds of them in one direction or the '
      'other.'),

('h2', '5.2. Implications for Leadership and Decision Making'),

('p', 'For executives navigating digital transformation, the architecture experiment is the '
      'result to act on. Three findings follow directly. First, the interface is a policy '
      'instrument. The same managers, drawing from an identical candidate pool, produced '
      'shortlists differing by 21.3 percentage points in their openness to non-elite '
      'institutions purely as a function of what the screen put first. This dwarfs the '
      'differences between individual screeners’ preferences and it is a decision that '
      'sits with whoever configures the applicant-tracking system—typically a function that '
      'never appears on a leadership agenda. Digital transformation research has argued that '
      'the organisational redesign, not the technology, is where the value and the risk lie '
      '{{hanelt21|braojos24}}; entry-level screening is a clean case in point, and '
      'interview evidence from talent-acquisition leaders points the same way: what '
      'changes outcomes is how selection is restructured around the tool, not the tool '
      'itself {{hrm_structuration|budhwar2023}}.'),

('p', 'Second, the equity–quality trade-off that justifies credential-first screening does '
      'not exist in these data. Evidence-first ordering raised both the non-elite share and '
      'the measured quality of the shortlist. A manager who believes she is protecting '
      'quality by ranking on institution is, on this evidence, sacrificing quality as well '
      'as access. The intuition that pedigree is a shortcut to ability survives because it '
      'is rarely tested against a verified alternative in the same decision.'),

('p', 'Third, the cost is real and quantifiable, which makes it a decision rather than an '
      'aspiration. Evidence-first screening cost about 16 additional seconds per applicant, '
      'roughly 39% more time. Framing the choice honestly—an additional four and a half '
      'hours per thousand applications in exchange for a shortlist that is both more open '
      'and stronger—is more useful to a leadership team than an appeal to fairness that '
      'does not price the alternative. Firms that had already digitalised their hiring '
      'function were significantly more likely to be screening on verification rather than '
      'pedigree, which suggests the capability to make this trade is built, not merely '
      'chosen. That is consistent with a digital-leadership literature which locates the '
      'scarce capability in the leadership team and its governance choices rather than in '
      'the technology stack {{dl1|ceo_digital|sts4|upper_digital}}.'),

('h2', '5.3. Implications for Policy and for Applicants'),

('p', 'For public policy, the results argue for investment in portable, verified skill '
      'signals for young labour-market entrants. The compensating differentials show '
      'employers are willing to pay substantially for verified assessment results—more than '
      'for an elite degree—yet such results are almost never in an applicant’s hands. '
      'Field experiments in other settings have shown that supplying credibly shareable '
      'assessment results raises employment and earnings for the workers who receive them '
      '{{limited_information|inefficient_entry|reference_letters}}. The distinctive '
      'contribution of the present estimates is to show that the willingness to pay is '
      'there on the employer side too, which means the binding constraint is the '
      'infrastructure rather than employer demand.'),

('p', 'A second policy implication concerns disclosure rules. A requirement to declare AI '
      'assistance, imposed without a mechanism for making the declaration informative, '
      'would impose a measurable cost on honest applicants—about a sixth of monthly pay in '
      'compensating terms—and would push the rest towards concealment. Pairing disclosure '
      'with a standard for process evidence changes the calculation: the penalty falls by '
      'about three quarters, and disappears entirely for the third of employers who already '
      'screen on evidence. Educational institutions are well placed to supply this, since '
      'coursework already generates drafts, revisions and supervision records, and '
      'vocational tracks already certify skill in a form employers read, and firms '
      'demonstrably read those certificates when they screen school leavers '
      '{{vet1|youth_demand_side}}. How far '
      'such infrastructure reaches depends on the wider architecture of the school-to-work '
      'transition, which differs markedly across institutional settings {{stw|yg}} and '
      'which shapes how many young people end up outside employment, education and '
      'training altogether {{ilo1|ilo2}}.'),

('p', 'For young applicants the practical advice that follows is unusually concrete. '
      'Disclosure is costly on average but the cost is conditional and largely repairable, '
      'and the repair—keeping and presenting a record of how the work was done—is within '
      'the applicant’s control in a way that institution and referral network are not. '
      'Given that a poor or delayed entry into the labour market leaves durable scars '
      '{{vonwachter20|first_job_firm|scarring_synthesis}}, the difference between a '
      'repairable and an unrepairable penalty is not a small matter.'),

('h2', '5.4. Limitations and Future Research'),

('p', 'Four limitations bound these conclusions. The most important is that stated choices '
      'are not hiring decisions. Conjoint and factorial designs are the standard '
      'non-deceptive instrument for eliciting employer preferences {{irr|hainmueller14}}, '
      'and they have been used with recruiters in screening scenarios before '
      '{{cbc_recruiters|cbc_graduates}}, but a careful comparison of factorial-survey '
      'estimates against real hiring behaviour finds that the two can diverge appreciably '
      '{{forster24}}. We mitigated this by recruiting people who actually make shortlist '
      'decisions, by anchoring the scenario to a vacancy of a kind their firm fills '
      '{{gutfleisch21}}, and by including an opt-out so that respondents were not forced to '
      'select from weak pairs; and the ordering we recover—verified assessment above elite '
      'credential—matches what field experiments with real vacancies find '
      '{{limited_information}}. Nevertheless the magnitudes should be read as preference '
      'weights, not as predicted callback rates. A field audit varying process evidence on '
      'real applications is the natural next step.'),

('p', 'Second, the architecture experiment manipulates ordering and salience within a '
      'research instrument, not a live applicant-tracking system, and the shortlist has no '
      'consequences for the respondent. The direction of the effect is likely robust, since '
      'ordering effects are if anything stronger under real time pressure, but the '
      'magnitude may not transfer; field experiments that alter a real selection stage '
      'find substantial behavioural responses on both sides of the market '
      '{{async_ai_assessment|voice_ai_interviews}}. Third, the sample is drawn from '
      'knowledge-intensive '
      'service firms in one region of one country. The credential-retreat regime may be '
      'larger where institutional tier is a stronger sorting device, as it is in China’s '
      'graduate market, and the results should be replicated where entry is organised '
      'through apprenticeship or occupational licensing instead. Fourth, all data come from '
      'a single informant per firm at one point in time; we used key-informant selection '
      'criteria {{key_informants}} and the choice tasks are experimental, which limits '
      'common-method concerns {{podsakoff2003|podsakoff2024}}, but the firm-level covariates are '
      'self-reported and the perceived AI-assisted share in particular is a belief rather '
      'than a measurement.'),

('p', 'Three extensions follow. The most valuable would be a field experiment in which real '
      'applications carry randomised process evidence, which would convert the compensating '
      'differentials estimated here into callback effects. A second would track the same '
      'firms over time as the perceived AI-assisted share rises, testing whether the '
      'membership shifts predicted here occur within firms rather than only across them. A '
      'third would extend the architecture manipulation to the applicant side, since the '
      'signalling equilibrium is jointly determined and applicants adjust their disclosure '
      'behaviour to the penalties they anticipate.'),

# ============================================================ 6. Conclusions
('h1', '6. Conclusions'),

('p', 'Generative artificial intelligence has made the written job application cheap to '
      'produce, and a cheap signal cannot separate candidates. This paper asked what '
      'employers do instead, and whether the answer can be changed by design. Combining a '
      'choice experiment with 452 managers who make entry-level shortlist decisions and a '
      'randomised manipulation of the screening architecture, we find that disclosure of AI '
      'assistance carries a penalty worth about 1743 CNY per month in compensating terms, '
      'that a portfolio documenting the applicant’s drafting and revision process removes '
      'about three quarters of it, and that verified assessment results are valued more '
      'highly than elite credentials.'),

('p', 'Employers do not, however, screen by a single rule. Three regimes coexist: a '
      'credential-retreat regime holding 38.1% of respondents, an assessment-triage regime '
      'holding 28.4%, and an evidence-weighting regime holding 33.5% that attaches no '
      'penalty whatever to disclosure. Membership responds to the state of the signal '
      'environment in the direction the theory predicts—managers who believe more of their '
      'applications are AI-assisted, and who face faster growth in volume, retreat towards '
      'credentials—and in the opposite direction to the depth of digital transformation of '
      'the hiring function, so firms that have genuinely rebuilt their hiring process '
      'install verification rather than pedigree.'),

('p', 'The most consequential finding is the one that does not depend on preferences at '
      'all. The same managers, drawing from an identical pool, produced shortlists differing '
      'by 21.3 percentage points in their openness to candidates from non-elite '
      'institutions according to what the interface presented first, and the evidence-first '
      'architecture that opened access also produced shortlists 8.6 percentile points '
      'stronger on verified assessment, at a cost of about 16 additional seconds per '
      'applicant. The equity–quality trade-off is an artefact of the funnel. Who reaches a '
      'human interviewer in the age of machine-written applications is therefore decided '
      'less by the preferences of the person screening than by the architecture someone '
      'else configured, and that architecture is a leadership decision that can be made '
      'deliberately.'),

# ============================================================== back matter
('back', 'Author Contributions:',
 'Conceptualization, X.C. and T.M.; methodology, X.C.; software, X.C.; validation, X.C., '
 'D.H. and T.M.; formal analysis, X.C.; investigation, D.H.; resources, T.M.; data '
 'curation, D.H.; writing—original draft preparation, X.C.; writing—review and editing, '
 'T.M.; visualization, X.C. and D.H.; supervision, T.M.; project administration, T.M.; '
 'funding acquisition, X.C. All authors have read and agreed to the published version of '
 'the manuscript.'),
('back', 'Funding:',
 'This research was funded by the Zhejiang Provincial Philosophy and Social Sciences '
 'Planning Special Project on Higher Education Basic Research Funding Reform (Grant '
 'Number: 25NDJC153YBMS) and the Major Humanities and Social Sciences Research Projects '
 'in Zhejiang Higher Education Institutions (Grant Number: 2024QN018).'),
('back', 'Institutional Review Board Statement:',
 'The study was conducted in accordance with the Declaration of Helsinki and approved by '
 'the Academic Ethics Committee of the College of Business, Jiaxing University (protocol '
 'code JXU-BUS-2026-047, approved on 21 February 2026).'),
('back', 'Informed Consent Statement:',
 'Informed consent was obtained from all respondents involved in the study.'),
('back', 'Data Availability Statement:',
 'The choice-experiment design, the estimation code, the survey instrument and the code '
 'that generates every figure and table in this paper are available from the corresponding '
 'author on reasonable request. Respondent-level data cannot be shared because '
 'participants were assured of confidentiality.'),
('back', 'Conflicts of Interest:', 'The authors declare no conflicts of interest.'),

('h1', 'Abbreviations'),
('p', 'The following abbreviations are used in this manuscript: AI, artificial '
      'intelligence; AIC, Akaike information criterion; BIC, Bayesian information '
      'criterion; CAIC, consistent Akaike information criterion; CBC, choice-based '
      'conjoint; CI, confidence interval; CNY, Chinese yuan; DCE, discrete choice '
      'experiment; EM, expectation–maximisation; MRS, marginal rate of substitution; SD, '
      'standard deviation; SE, standard error; SML, simulated maximum likelihood; YRD, '
      'Yangtze River Delta.'),

# ============================================================== Appendix A
('h1', 'Appendix A'),
('p', 'Table A1 documents the experimental design and the estimation settings in the '
      'detail required to reproduce the analysis.'),

('tabcap', 'A1', 'Design and estimation details.'),
('table', [
    ['Item', 'Value'],
    ['Respondents', '452 entry-level screening decision makers'],
    ['Choice tasks per respondent', '14'],
    ['Alternatives per task', '2 candidate profiles plus an opt-out'],
    ['Choice sets', '6328'],
    ['Profile evaluations', '12,656'],
    ['Full factorial', '288 profiles (2 × 2 × 3 × 2 × 2 × 2 × 3)'],
    ['Design construction', 'D-efficient search at null priors with a minimum-overlap '
                            'constraint of four differing attributes'],
    ['D-error of the retained design', '0.570'],
    ['Design blocks', '8 rotations, with within-task positions alternated'],
    ['Opt-out share', '11.5% of tasks'],
    ['Mixed logit draws', '500 scrambled Halton draws, all coefficients normal'],
    ['Mixed logit convergence', 'largest absolute gradient 7.0 × 10⁻⁴'],
    ['Conditional logit convergence', 'largest absolute gradient 2.1 × 10⁻⁷'],
    ['Latent-class estimation', 'expectation–maximisation, 2 to 5 classes, BIC selection'],
    ['Standard errors', 'respondent-clustered sandwich estimator'],
    ['Trade-off standard errors', 'delta method on the ratio to the salary coefficient'],
    ['Hold-out validation', 'estimate on tasks 1–9, predict tasks 10–14 from each '
                            'respondent’s posterior over tastes'],
    ['Architecture experiment', '3 arms, equal randomisation, identical 20-candidate pool'],
    ['Software', 'Python 3.11, NumPy, SciPy; single seeded pipeline'],
 ], [3560, 6080]),
]
