# -*- coding: utf-8 -*-
"""Paper 9, Part B: Results, then the discussion and back matter."""
from p9_content_b_tail import TAIL

PART_B = [
# =================================================================== 4.4 checks
('h2', '4.4. Over-Identifying Checks'),

('p', 'Two implications of the calibration were never targeted. The first is the '
      'new-graduate unemployment rate inside the exposed field, which the estimated '
      'economy puts at 2.5 per cent before the shock against an all-field rate of 5.5 '
      'per cent. The direction and the ordering are right—a field with a large wage '
      'premium places its graduates faster—but the level is lower than the roughly four '
      'to five per cent that computing recorded before 2023, so the model overstates '
      'how comfortable the pre-shock position was. The second is the loop gain, which '
      'the calibration delivers as −0.307 without being asked to. Its absolute value '
      'below one means that a shock dies out under anchored beliefs; the corresponding '
      'modulus is the fourth root of 0.307, or 0.744, and the oscillation that would '
      'appear if the gain exceeded one would have period 2⟪D⟫, that is eight years.'),

('p', 'The third check is the transition itself, and it is the one that matters. The '
      'size of the shock is chosen so that the exposed field’s new-graduate '
      'unemployment rate reaches the 7.0 per cent now observed; nothing else about the '
      'path is targeted. The required fall in the relative demand index is 31.0 per '
      'cent. The model then produces, without being asked, a compression of the '
      'early-career wage premium of 31.2 per cent and a peak unemployment gap between '
      'the exposed field and the rest of 1.18 percentage points—that is, it reproduces '
      'the configuration that motivated the paper, a field that still pays well and '
      'still places its graduates badly, as a property of the transition rather than of '
      'any equilibrium.'),

# =================================================================== 5. Results
('h1', '5. Results'),

('h2', '5.1. The Estimated Economy'),

('p', 'Table 3 reports the stationary equilibrium the calibration selects. Job finding '
      'is fast in both fields, as it should be for graduates in a tight market, and '
      'faster in the exposed field, which is why its unemployment rate is lower. The '
      'entry-tier stock of the exposed field is about six times its annual graduating '
      'cohort, which is the arithmetic of a seven-year entry tier and is what makes a '
      'single cohort a modest part of the congestion it faces. That ratio is the '
      'quantity that decides how much a cobweb can do here, and it is the reason the '
      'delay alone turns out not to be enough.'),

('tabcap', 3, 'The estimated stationary equilibrium, before the shock.'),
('table', [
    ['Quantity', 'Symbol', 'Exposed field', 'Other fields'],
    ['Share of the entering cohort', '⟪s⟫', '0.055', '0.945'],
    ['Job-finding rate, per year', '⟪f⟫', '3.674', '2.900'],
    ['Market tightness', '⟪θ⟫', '0.911', '0.568'],
    ['Entry-tier employment stock', '⟪E⟫', '0.329', '5.620'],
    ['Searchers', '⟪U⟫', '0.084', '1.479'],
    ['Early-career wage', '⟪w⟫', '1.382', '1.023'],
    ['New-graduate unemployment rate', '—', '0.025', '0.055'],
], [3400, 1100, 2100, 2100]),
('notes', 'Notes: Stocks are per entering cohort of unit size. The new-graduate '
          'unemployment rate of the exposed field is an over-identifying check, not a '
          'target. The loop gain implied by this equilibrium is −0.307.'),

('figure', 'p9_fig2.png', 5.40, None, 'fig'),
('figcap', 2,
 'Left: the four targeted moments against their model counterparts; the two are '
 'indistinguishable, the maximum absolute log deviation being 1.8 × 10⁻¹³. Right: the '
 'shock is sized so that new-graduate unemployment in the exposed field reaches the 7.0 '
 'per cent now observed, which requires a 31.0 per cent fall in the relative demand '
 'index. Everything else about the path is unconstrained.'),

('h2', '5.2. The Transition: Enrolment Overreacts by a Factor of Two'),

('p', 'Table 4 and Figure 3 report the transition. The warranted change is a fall in '
      'the entering share from 5.50 to 4.74 per cent of the cohort, a decline of 13.9 '
      'per cent. What happens instead is that the share falls to 3.75 per cent on '
      'impact—a decline of 28.5 per cent, or 2.05 times the warranted one—and then '
      'recovers, settling within six years. The overreaction is on impact rather than '
      'delayed, which is worth being precise about because it distinguishes this '
      'mechanism from the textbook cobweb. Entrants observe the collapse in the '
      'field’s return immediately and revise immediately; what the four-year delay does '
      'is guarantee that their revision cannot show up in the market for four years, so '
      'nothing corrects them in the meantime.'),

('p', 'Two features of the path are worth noting because they are untargeted. The '
      'early-career wage premium compresses by 31.2 per cent at its trough and then '
      'partially recovers, and the gap between the two fields’ new-graduate '
      'unemployment rates opens to 1.18 percentage points. Both are transitional. An '
      'observer who saw only the enrolment series would conclude that students had '
      'abandoned the field; an observer who saw only the long-run equilibrium would '
      'conclude that very little had happened. Both would be reading a real number '
      'correctly and drawing the wrong inference from it. This is the configuration that '
      'the youth-employment statistics record without being able to explain '
      '{{ilo1|ogbonna|china_youth2}}.'),

('tabcap', 4, 'The transition after the technology shock.'),
('table', [
    ['Outcome', 'Value'],
    ['Entering share, before the shock', '0.0550'],
    ['Entering share, on impact', '0.0375'],
    ['Entering share, long run', '0.0474'],
    ['Change on impact (%)', '−28.45'],
    ['Change in the long run (%)', '−13.87'],
    ['Amplification (impact ÷ long run)', '2.05'],
    ['Years to the trough', '0'],
    ['Years to settle', '6'],
    ['Fall in the relative demand index (%)', '31.0'],
    ['Compression of the wage premium (%)', '−31.24'],
    ['Peak unemployment gap (percentage points)', '1.18'],
    ['Discounted output forgone (% of post-shock output)', '0.0019'],
], [6200, 2600]),
('notes', 'Notes: The long-run share is the mean of the last ten years of a ninety-year '
          'simulation. Settling is the first date after the trough from which the share '
          'stays within a tenth of the remaining gap to its long-run value.'),

('figure', 'p9_fig3.png', 5.40, None, 'fig'),
('figcap', 3,
 'The transition. Left: the entering share overshoots its long-run change by a factor '
 'of 2.05 on impact and then recovers. Centre: the early-career wage premium compresses '
 'and partially recovers. Right: the weight entrants place on the trend-projecting rule, '
 'which rises while the trend lasts and falls back once it breaks.'),

('h2', '5.3. Where the Amplification Comes From'),

('p', 'The delay is necessary for the overreaction but it is not sufficient, and Table '
      '5 separates the two. With beliefs anchored on the field’s long-run value the '
      'amplification is 1.10: the entering share falls 15.3 per cent against a '
      'warranted 13.9, which is very nearly the right answer. Introducing a '
      'trend-projecting rule alongside the anchored one raises the amplification to '
      '1.89 even with the weights on the two rules held fixed. Letting the weights '
      'respond to recent accuracy raises it further to 2.05, and sharpening that '
      'response—raising the intensity with which entrants imitate whichever rule has '
      'lately been right—raises it to 2.48.'),

('p', 'The ordering is monotone and the mechanism is transparent. While the field’s '
      'return is falling, the rule that projects the fall forward is the accurate one, '
      'so its weight rises, so more entrants project the fall forward, so the fall in '
      'enrolment deepens. The loop that selects the forecasting rule is reinforcing '
      'even though the loop that allocates students is balancing, and it operates on a '
      'timescale of a year or two rather than the four years the balancing loop needs. '
      'This is the mechanism Brock and Hommes identified {{brock_hommes97}}, and the '
      'contribution here is to show that it survives being embedded in an equilibrium '
      'labour market and calibrated.'),

('tabcap', 5, 'Belief regimes: how much of the overreaction each one produces.'),
('table', [
    ['Regime', 'Weight on the trend rule', 'Change on impact (%)',
     'Amplification', 'Output forgone (%)'],
    ['Anchored beliefs only', '0.00', '−15.31', '1.10', '0.00246'],
    ['Both rules, fixed weights', '0.50', '−26.24', '1.89', '0.00201'],
    ['Both rules, weights respond (baseline)', '0.60', '−28.45', '2.05', '0.00192'],
    ['Both rules, sharp imitation', '0.88', '−34.37', '2.48', '0.00166'],
], [3900, 1700, 1500, 1300, 1500]),
('notes', 'Notes: The weight on the trend rule is its stationary value, which depends on '
          'the intensity of choice and on the cost of the anchored rule. The four rows '
          'differ only in the belief block; the labour block and the shock are identical.'),

('figure', 'p9_fig4.png', 5.40, None, 'fig'),
('figcap', 4,
 'The overreaction by belief regime. The depth of the enrolment response and its '
 'amplification both rise monotonically as forecasting moves from anchored to strongly '
 'imitative, while the output forgone during the adjustment falls.'),

('h2', '5.4. Stability'),

('p', 'Because raising the intensity of choice raises the amplification, it is natural '
      'to ask whether it eventually destabilises the stationary state, as it does in '
      'the asset-pricing applications of this framework. In the calibrated economy it '
      'does not. Figure 5 sweeps the intensity of choice from zero to sixty and the '
      'modulus of the dominant mode rises from 0.966 to 0.971 and then saturates: it '
      'approaches a ceiling below one rather than crossing it. The reason is the '
      'ratio noted in Section 5.1. One cohort is about a sixth of the entry-tier stock '
      'it competes with, so even a population that forecasts entirely by extrapolation '
      'cannot move the congestion enough in one year to sustain a cycle.'),

('p', 'That is a negative result and we report it as one, because it bounds what the '
      'mechanism can be claimed to do. The instability is not unreachable in principle: '
      'the right panel of Figure 5 traces the loop gain across the two elasticities the '
      'literature disputes, and the gain approaches one at the top of the published '
      'range for the responsiveness of field choice combined with the bottom of the '
      'range for substitutability between fields. In the global sweep of Section 5.6, '
      '4.5 per cent of parameter draws are unstable. The honest summary is that the '
      'calibrated economy sits comfortably inside the stable region, that the education '
      'system’s slow-moving stock is what puts it there, and that a market with a '
      'shorter training period or a narrower field definition would sit closer to the '
      'boundary.'),

('figure', 'p9_fig5.png', 5.40, None, 'fig'),
('figcap', 5,
 'Left: the modulus of the dominant mode against the intensity with which entrants '
 'imitate successful forecasting rules. It rises but saturates below one, so the '
 'stationary state does not lose stability in the calibrated economy. Right: the loop '
 'gain across the elasticity of field choice and the elasticity of substitution between '
 'fields; the gain reaches one only in the corner where students are highly responsive '
 'and the two kinds of graduate are poor substitutes.'),

('h2', '5.5. Information: Two Instruments That Rank in Opposite Orders'),

('p', 'Table 6 reports two changes to the information environment. Making the signal '
      'about current returns noisier shrinks the enrolment swing substantially, from an '
      'amplification of 2.05 to 1.65, because a shrunken perceived differential makes '
      'entrants less responsive to everything, including the shock. Publishing the '
      'enrolment pipeline does the opposite: it deepens the immediate response, from '
      '−28.5 to −29.4 per cent, and raises the amplification to 2.12.'),

('p', 'On the welfare measure the ranking reverses. The noisier signal raises the '
      'discounted output forgone from 0.00192 to 0.00219 per cent, and publishing the '
      'pipeline lowers it to 0.00180, a reduction of about six per cent. The two '
      'measures disagree because the deeper response is the better-informed one. At the '
      'moment the shock lands, four large pre-shock cohorts are still enrolled and '
      'still coming; an entrant who can see them correctly infers that the field will '
      'stay crowded for years and correctly leaves harder. The swing is larger and the '
      'allocation is better.'),

('p', 'This is the paper’s most useful result and it is a warning rather than a '
      'prescription. A ministry that judged an information policy by whether it '
      'calmed enrolment swings would reject the policy that improves allocation and '
      'adopt the one that degrades it, because degrading the signal does calm the '
      'swing. Amplitude is not welfare. The systems literature has made this argument '
      'about indicators in general {{meadows_ts|forrester71}}; here it has a price.'),

('tabcap', 6, 'Two changes to the information environment.'),
('table', [
    ['Information environment', 'Change on impact (%)', 'Amplification',
     'Output forgone (%)', 'Change in loss (%)'],
    ['Baseline', '−28.45', '2.05', '0.00192', '0.0'],
    ['Noisier signal about current returns', '−22.92', '1.65', '0.00219', '+14.4'],
    ['Pipeline published, half weight', '−28.95', '2.09', '0.00185', '−3.2'],
    ['Pipeline published, full weight', '−29.44', '2.12', '0.00180', '−5.9'],
], [4100, 1700, 1400, 1500, 1400]),
('notes', 'Notes: The noisier signal shrinks the perceived return differential towards '
          'its long-run value. Publishing the pipeline replaces part of the anchored '
          'rule’s forecast with the differential implied by the cohorts already '
          'enrolled. A negative change in loss is an improvement.'),

('figure', 'p9_fig6.png', 5.40, None, 'fig'),
('figcap', 6,
 'The two information instruments ranked twice. On the amplitude of the enrolment swing '
 '(left) the noisier signal looks best and publishing the pipeline looks worst; on the '
 'output forgone during the adjustment (right) the order is exactly reversed.'),

('h2', '5.6. Global Sensitivity'),

('p', 'Six parameters are set outside the estimation, and the results above are '
      'conditional on them. We draw 192 Latin hypercube points {{mckay_lhs}} over the '
      'degree lag, the elasticity of substitution, the exit rate from the entry tier, '
      'the separation rate, the matching elasticity and the flow value of non-work, '
      're-calibrate at each draw so that all four targets continue to hold exactly, and '
      're-run the shock. Forty-four of the 192 draws admit an exact recalibration; the '
      'remainder are combinations for which no admissible parameter vector reproduces '
      'all four moments, and they are discarded rather than reported at an approximate '
      'fit. That solve rate is low and we state it plainly: the conclusions below rest '
      'on the region of the parameter space in which the model can be made to match the '
      'data exactly, not on the whole box.'),

('p', 'Within that region the central result is stable. The amplification averages 1.98 '
      'with a fifth-to-ninety-fifth-percentile range of 1.84 to 2.19, and it exceeds '
      'one in every draw, so the overreaction is a property of the mechanism rather '
      'than of the baseline calibration. The modulus of the dominant mode averages '
      '0.930 and lies below one in 95.5 per cent of draws, which locates the instability '
      'noted in Section 5.4: it exists, it is reachable, and it is not where the '
      'calibrated economy sits.'),

('figure', 'p9_fig7.png', 5.40, None, 'fig'),
('figcap', 7,
 'Global sensitivity over the six externally set parameters, across the draws that admit '
 'an exact recalibration. The amplification exceeds one in every draw; the dominant '
 'modulus lies below one in all but a twentieth of them.'),
] + TAIL
