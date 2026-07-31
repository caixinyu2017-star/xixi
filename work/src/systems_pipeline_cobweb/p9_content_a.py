# -*- coding: utf-8 -*-
"""Paper 9, Part A: front matter, Introduction, Literature, Model, Calibration."""

TITLE = ('The Pipeline Overshoots the Shock: An Adaptive-Belief Systems Model of '
         'Delayed Educational Supply and Graduate Labour-Market Adjustment')

ABSTRACT = (
    'A degree takes four years to produce, so the students who react to a labour market '
    'reach it four years late. This paper asks what that delay does to an education '
    'system when demand for a field falls abruptly, as demand for entry-level '
    'computing work has since 2023. We build a two-field model in which firms hire '
    'entry-tier graduates through a matching market with free entry, the two kinds of '
    'graduate are imperfect substitutes in production, and entrants choose a field by a '
    'discrete-choice rule after forecasting what it will be worth on graduation. '
    'Forecasts come from two competing rules—one anchored on the field’s long-run '
    'value, one that projects the recent trend—and the weight on each evolves with its '
    'recent accuracy, which makes the education system an adaptive belief system in the '
    'sense of Brock and Hommes. The labour block is calibrated to four moments of the '
    'pre-shock graduate market, matched to thirteen decimal places, and the size of the '
    'technology shock is set so that the model reproduces the new-graduate '
    'unemployment rate now observed in the exposed field; the whole transition is then '
    'free to be right or wrong. Three findings follow. The entering share overreacts on '
    'impact by a factor of 2.05: it falls 28.5 per cent when the warranted long-run '
    'fall is 13.9 per cent, so most of the enrolment collapse that follows such a shock '
    'is transitional rather than warranted. The overreaction is not produced by the '
    'delay alone but by the competition between forecasting rules, and it rises '
    'monotonically from 1.10 when beliefs are anchored to 2.48 when entrants imitate '
    'successful rules sharply. Yet the overreaction is not, on this calibration, a '
    'welfare loss: the adjustment cost falls as the response grows, because the '
    'alternative error—under-reacting and staying mis-allocated for longer—is the more '
    'expensive one. The size of a system’s correction is therefore a poor guide to how '
    'well it is behaving, and an instrument ranked on the amplitude of the swing it '
    'produces will be ranked backwards.'
)

KEYWORDS = ('education-to-work transition; adaptive belief systems; heterogeneous '
            'expectations; cobweb dynamics; field of study; search and matching; '
            'graduate labour market; artificial intelligence; delay and feedback; '
            'system stability')

PART_A = [
# ============================================================ 1. Introduction
('h1', '1. Introduction'),

('p', 'A degree is a slow product. A student who decides in 2026 that computing is '
      'where the work is will reach the labour market in 2030, carrying a skill chosen '
      'for a market that no longer exists in the form she observed. Every education '
      'system in the world runs this delay, and it is long relative to the shocks that '
      'now move labour demand. This paper asks what the delay does when demand for one '
      'field falls abruptly, and finds that the answer is largely a matter of how '
      'students form expectations rather than how large the shock was.'),

('p', 'The setting is live. Enrolment in computing rose in the United States for '
      'sixteen consecutive years and degree production reached an all-time high in '
      '2022–23; then it fell, and the fall in autumn 2025 was the steepest of any '
      'field and the first national decline in about two decades. The market that '
      'caused the reversal moved first. High-frequency payroll data show employment of '
      '22-to-25-year-olds in the occupations most exposed to generative artificial '
      'intelligence falling by roughly a sixth relative to older workers doing the '
      'same jobs {{canaries}}, and résumé and vacancy data show junior hiring falling '
      'in adopting firms through slower recruitment rather than through separations '
      '{{seniority_biased}}. The evidence is contested—Danish administrative data '
      'yield precise nulls over a comparable window {{still_waters}}, and the '
      'identification of an AI effect against a concurrent interest-rate shock is '
      'genuinely hard—but the model below does not need the shock to be AI. It needs '
      'only that entry-level demand in one field fell, which is not in dispute.'),

('p', 'What is in dispute, and what matters for policy, is what happens next. The '
      'reflex reading of falling enrolment is that the system is correcting: students '
      'observed a worse market and are reallocating towards better ones, which is what '
      'a price system is supposed to do, and the stakes for young people are high enough '
      'that getting it right matters {{ilo1|neet_cee|basol}}. That reading is right '
      'about the direction and '
      'can be badly wrong about the magnitude, because the correction is made by '
      'people who cannot see the correction being made by everyone else. Each entrant '
      'observes today’s market, not the market that the four cohorts already enrolled '
      'will produce. When enough of them revise at once, the field is under-supplied '
      'four years later, its return recovers, and the next cohorts pile back in. This '
      'is the cobweb, and it has been understood since Ezekiel {{ezekiel}} and applied '
      'to educated labour since Freeman’s model of the engineering market '
      '{{freeman76|freeman75}}.'),

('p', 'We add the ingredient that the classical cobweb lacks and that fifty years of '
      'work on expectations says is decisive. In the classical model everyone forecasts '
      'the same way, so the system is stable or unstable once and for all, according to '
      'a ratio of elasticities. In practice forecasting rules compete: some students '
      'anchor on what a field is worth in the long run, others project the recent trend, '
      'and the popularity of each rule depends on how well it has just performed. Brock '
      'and Hommes showed that this endogenous selection is itself a source of '
      'instability—that as agents imitate successful rules more sharply, a stable '
      'equilibrium can lose stability and give way to cycles and worse, with no change '
      'in fundamentals and no irrationality on anyone’s part {{brock_hommes97}}. Their '
      'adaptive belief system has been applied to asset markets, to macroeconomic '
      'expectations and to commodity markets with production lags '
      '{{brock_hommes98|hommes_jel|hommes_delays}}. It has not, as far as we can '
      'establish, been applied to the choice of what to study, which is the market with '
      'the longest production lag of all and the one where the consequences of a bad '
      'forecast are least reversible.'),

('p', 'The paper builds that model and takes it to data. Two fields are imperfect '
      'substitutes in production, so the marginal product of a field falls as its '
      'entry-tier stock grows. Firms post vacancies under free entry, so a field whose '
      'graduates are plentiful is a field in which they are hard to place as well as '
      'poorly paid. Entrants choose by a logit rule on the forecast value differential; '
      'the forecast is a weighted average of an anchored and an extrapolative rule, and '
      'the weights follow the rules’ recent accuracy with intensity of choice ψ. The '
      'labour block is calibrated to four moments of the graduate market as it stood '
      'before the shock and matches them to twelve decimal places; the size of the '
      'shock is then chosen so that the model reproduces the new-graduate unemployment '
      'rate now observed in the exposed field, which leaves everything else—the '
      'enrolment path, the wage path, the dynamics—free to be right or wrong.'),

('p', 'Three findings follow. The first is the paper’s title. The entering share '
      'overreacts on impact: it falls 28.5 per cent against a warranted long-run fall '
      'of 13.9 per cent, an amplification of 2.05. Most of the enrolment collapse that '
      'follows a demand shock of this size is therefore transitional, and it is '
      'manufactured by the adjustment process rather than required by the shock. The '
      'second concerns where the amplification comes from. It is not the delay alone: '
      'with beliefs anchored on the field’s long-run value the amplification is 1.10, '
      'which is to say the response is almost exactly what is warranted. It is the '
      'competition between forecasting rules that does the work, and the amplification '
      'rises monotonically to 1.89 when a trend-projecting rule is present and to 2.48 '
      'when entrants imitate the recently successful rule sharply.'),

('p', 'The third finding is the one we did not expect, and it cuts against the framing '
      'the first two invite. The overreaction is not a welfare loss on this '
      'calibration. The discounted output forgone during the adjustment falls as the '
      'response grows—from 0.0025 per cent of output under anchored beliefs to 0.0017 '
      'per cent under strong imitation—because the alternative error is under-reaction, '
      'and a system that adjusts too little stays mis-allocated for longer than one '
      'that adjusts too much and comes back. The same reversal shows up in the '
      'information experiments: a noisier signal about current returns makes entrants '
      'less responsive and shrinks the swing from 2.05 to 1.65, and it raises the '
      'adjustment cost; publishing the enrolment pipeline makes the immediate response '
      'deeper, and lowers it. The two rankings are opposite because the pipeline tells '
      'entrants something true—at the moment of the shock four large pre-shock cohorts '
      'are still coming—so the larger response is the better-informed one. The '
      'practical implication is a warning about measurement rather than a policy '
      'prescription: the amplitude of a correction is not a measure of how badly a '
      'system is doing, and an indicator built on it will rank interventions the wrong '
      'way round.'),

('p', 'The paper contributes to three literatures. To the cobweb tradition in educated '
      'labour markets {{freeman76|ryoo_rosen|blume_kohout}} it adds endogenous '
      'expectation formation and an equilibrium labour block, which converts a '
      'reduced-form stability condition into a calibrated statement about magnitudes. '
      'To the adaptive-belief-systems literature {{brock_hommes97|hommes_book|'
      'hommes_jel}} it adds an application in which the production lag is four years '
      'rather than one period and the traded object is a person’s twenties. To the '
      'policy debate about steering students towards shortage occupations '
      '{{brunello_mismatch|haaland}} it adds the observation that the stabilising '
      'information is not about prices at all.'),

('p', 'Section 2 places the paper in the literature. Section 3 sets out the model and '
      'defines equilibrium and stability. Section 4 describes the calibration and its '
      'over-identifying checks. Section 5 reports the results. Section 6 discusses what '
      'follows for measurement and policy and states the limitations. Section 7 '
      'concludes.'),

# ============================================================ 2. Literature
('h1', '2. Related Literature'),

('h2', '2.1. Cobwebs in Markets for Educated Labour'),

('p', 'The cobweb theorem is the observation that when supply is decided one production '
      'period before it is sold, and producers forecast the future price by the current '
      'one, quantity oscillates {{ezekiel|kaldor34}}. Whether the oscillation dies out, '
      'persists or explodes depends on the ratio of the supply to the demand elasticity, '
      'and Nerlove showed that replacing naive with adaptive expectations damps it '
      '{{nerlove}}. Recent work has returned to the structure with nonlinear methods, '
      'establishing the bifurcation structures that regime-switching expectations '
      'produce in a cobweb map {{gardini_cobweb}}, the effect of asymmetric beliefs on '
      'stability {{berardi_cobweb}}, and—closest to the present paper—the dynamics that '
      'production delays generate when technology choice is endogenous '
      '{{dieci_delays|hommes_delays}}, and the switching mechanism has been estimated '
      'directly in macroeconomic data {{kukacka|gusella}}. Poitras provides the '
      'intellectual history {{poitras}}.'),

('p', 'The application to educated labour is Freeman’s. His model of the market for new '
      'engineers found a supply response to lagged starting salaries strong enough to '
      'sustain oscillation rather than damp it {{freeman76}}, and he argued the same '
      'structure explained the swing in the returns to college training in the 1970s '
      '{{freeman75}}. Ryoo and Rosen later modelled the engineering market with '
      'forward-looking entrants and found a high supply elasticity but a market that '
      'clears sensibly {{ryoo_rosen}}. Blume-Kohout and Clack tested cobweb against '
      'rational expectations directly in the market for biomedical scientists, using the '
      'doubling of the National Institutes of Health budget as the demand shock and the '
      'six-year doctorate as the lag, and could not reject the cobweb '
      '{{blume_kohout}}. What has not been done, on our reading, is to bring this '
      'tradition to the field-of-study margin with modern expectation formation and a '
      'labour market that generates unemployment as well as wages.'),

('h2', '2.2. Field of Study, Its Return and Its Lag'),

('p', 'That students respond to the returns to a field is well established, though the '
      'size of the response is not. Long, Goldhaber and Huntington-Klein find that '
      'completed majors track wages observed about three years earlier—that is, wages '
      'at the time the student matriculated—which is direct evidence both of a response '
      'and of a lag {{long_majors}}. Beffy, Fougère and Maurel find the elasticity of '
      'field choice to expected earnings to be significant but small in France, and '
      'argue that non-pecuniary considerations dominate {{beffy}}. Blom, Cadena and Keys '
      'show that cohorts who experience high unemployment while studying select into '
      'higher-earning fields, a compensating behaviour large enough to offset a '
      'meaningful share of the cost of graduating in a recession {{blom_cycle}}. Because '
      'the published elasticities range from near zero to above one, we treat the '
      'elasticity as an externally set parameter, adopt a central value, and map the '
      'model’s behaviour across the whole published range rather than resting the '
      'results on any single estimate.'),

('p', 'The returns themselves are neither stable nor uniform. Field of study explains '
      'more of the variance in graduate earnings than institution does '
      '{{kirkeboen|bleemer}}, entry conditions have persistent effects that differ '
      'sharply by field {{altonji_cashier}}, and the STEM premium in particular decays '
      'over a career as the specific skills it rests on are displaced by newer ones '
      '{{deming_noray}}, and graduate over-education and field mismatch are persistent in '
      'the large systems where they have been measured {{mismatch1|vet1}}. That last '
      'finding matters here: it establishes that the '
      'quantity students are trying to forecast is itself moving, which is what makes '
      'the extrapolative rule attractive and dangerous at the same time.'),

('h2', '2.3. Heterogeneous Expectations and Adaptive Belief Systems'),

('p', 'The modelling apparatus is Brock and Hommes’s. Agents choose among a small set '
      'of forecasting rules; the population weight on a rule is a logit in its recent '
      'realised accuracy net of its cost; and the parameter governing how sharply agents '
      'switch—the intensity of choice—is the bifurcation parameter of the system '
      '{{brock_hommes97|brock_hommes98}}. The central result is that raising it '
      'destabilises: a costly but accurate rule is driven out by a free but naive one '
      'precisely when the system is at rest, so the rest point stops being an attractor. '
      'The framework is surveyed in {{hommes_book|hommes_jel}}, has repeated support in '
      'laboratory experiments where subjects coordinate on trend-following rules '
      '{{hommes_lab}}, and has been extended and estimated in a variety of settings '
      'since {{kukacka|gusella|boehl_hommes|difrancesco|evans_ltf}}. Moll’s recent '
      'assessment of what should replace rational expectations in applied macroeconomics '
      'is a useful statement of why this class of models is worth taking to data '
      '{{moll_re}}.'),

('p', 'The apparatus has been applied to markets with production lags—agricultural and '
      'commodity markets are the natural case {{hommes_delays|dieci_delays}}—but not, '
      'so far as repeated searching can establish, to the education market. That gap is '
      'the paper’s opening, and it is not merely an unoccupied box: the education market '
      'differs from a commodity market in ways that matter for the mechanism. The lag is '
      'four years rather than one season, the decision is taken once and is expensive to '
      'reverse, and the good being produced ages into a stock that persists for a career.'),

('h2', '2.4. The Shock to Entry-Level Demand'),

('p', 'The demand shock the paper feeds in is the contraction in entry-level technical '
      'hiring since 2023. Generative artificial intelligence raises productivity most on '
      'exactly the tasks that entry-level knowledge work consists of '
      '{{genai2|genai3}}, its exposure is concentrated in occupations rather '
      'than spread evenly {{genai1}}, and the macroeconomic accounting suggests '
      'the aggregate effect over a decade is modest even where the occupational effect '
      'is large {{acemoglu_ai|sbtc1}}; comparable displacement patterns appear for earlier '
      'automation technologies {{robots_china_firm|robots_china2|prod1}}. Whether the '
      'observed collapse in junior technical '
      'hiring is caused by AI is contested; the payroll evidence {{canaries}} and the '
      'firm-level résumé evidence {{seniority_biased}} point one way, Danish '
      'administrative data another {{still_waters}}, and part of the movement coincides '
      'with a monetary tightening that hit the same sector. Our model is agnostic about '
      'the source. It takes as given that the relative demand for entry-tier workers in '
      'one field fell, and asks what an education system does with that.'),

('h2', '2.5. Delays, Feedback and the Behaviour of Social Systems'),

('p', 'The systems tradition arrived at a compatible conclusion from a different '
      'direction. Forrester’s argument that complex social systems respond '
      'counter-intuitively to intervention rests on delays and feedback of exactly this '
      'kind {{forrester71}}, and the experimental work on stock management shows that '
      'people misperceive feedback and accumulation systematically, over-ordering when '
      'supply lines are long and thereby producing the oscillation they are trying to '
      'avoid {{sterman_misperc|sterman_mgr}}. That literature identifies the same '
      'culprit as the economics does—decisions taken on a state variable that the '
      'decision itself will change, with a delay in between—and it supplies the '
      'vocabulary for the policy section: the leverage in such a system is often in the '
      'structure of its information flows rather than in the strength of its incentives '
      '{{meadows_ts|sterman_bd}}. Recent work in this journal has applied the same systemic '
      'framing to employment and to the digital economy '
      '{{ses_urban|ses_regional|systems_ai_dm}}. The contribution here is to make that claim '
      'quantitative in a market where the delay is a degree.'),
]

# ================================================================== 3. Model
PART_A += [
('h1', '3. The Model'),

('h2', '3.1. Environment'),

('p', 'Time is discrete and a period is a year. There are two fields of study, indexed '
      '⟪j⟫, of which field 1 is the one exposed to the technology shock and field 2 is '
      'everything else. Each year a cohort of size ⟪N⟫ chooses a field. A degree takes '
      '⟪D⟫ years, so the cohort that enters in year ⟪t⟫ reaches the labour market in '
      'year ⟪t+D⟫; the ⟪D⟫ cohorts in between are the pipeline, and they are the '
      'model’s memory. Graduates search for work in the market for their field, are '
      'matched, hold a job until they separate, and leave the entry tier at rate ⟪γ⟫, '
      'which fixes the length of the entry tier and hence the speed at which the stock '
      'of recent graduates can change.'),

('p', 'Restricting attention to the entry tier is a modelling choice with consequences, '
      'so it is worth defending. A new graduate competes for entry-level positions with '
      'other recent graduates rather than with mid-career staff, the evidence on the '
      'current shock is specifically about workers in their early twenties '
      '{{canaries|seniority_biased}}, and the stock a cohort actually crowds is the one '
      'that turns over in years rather than decades. Modelling the whole career instead '
      'would make the congested stock forty years deep, and a single cohort would then '
      'be too small a part of it to matter—which is a statement about the model, not '
      'about the world.'),

('h2', '3.2. Production and the Entry-Level Market'),

('p', 'The two kinds of entry-tier graduate are imperfect substitutes with elasticity '
      '⟪σ⟫, as in Equation (1), so the marginal product of a field falls in its own '
      'employment stock at rate ⟪1/σ⟫, given in Equation (2). This is the only channel '
      'through which one cohort’s decision reaches the next, and ⟪σ⟫ is therefore the '
      'parameter that decides how much a crowded field punishes those who crowd it '
      '{{katz_murphy|ciccone_peri}}:'),
('eq', 'eq1', 1),
('eq', 'eq2', 2),

('p', 'Hiring is frictional. Field ⟪j⟫ has a constant-returns matching function over '
      'searchers and vacancies, Equation (3), which delivers a job-finding rate that '
      'depends only on tightness:'),
('eq', 'eq3', 3),

('p', 'The surplus of a match is the marginal product net of the flow value of '
      'non-work, capitalised over the rate at which the match ends and adjusted for the '
      'fact that the worker’s share raises the value of continued search, Equation (4). '
      'Firms post vacancies until the expected cost of a hire equals the firm’s share '
      'of that surplus, Equation (5). Together these make tightness—and so the '
      'job-finding rate—a decreasing function of the field’s employment stock: an '
      'over-supplied field is one in which graduates are both poorly paid and hard to '
      'place, which is what distinguishes this from a market-clearing cobweb:'),
('eq', 'eq4', 4),
('eq', 'eq5', 5),

('p', 'The wage that implements the Nash split and the value of entering the field as a '
      'new graduate follow in Equation (6). The second object is what a prospective '
      'student is trying to forecast:'),
('eq', 'eq6', 6),

('h2', '3.3. Stocks and the Pipeline'),

('p', 'Employment and search evolve as in Equations (7) and (8), written in annual '
      'transition probabilities ⟪F=1−exp(−f)⟫, ⟪d=1−exp(−δ)⟫ and ⟪g=1−exp(−γ)⟫ rather '
      'than in rates, because a job-finding rate above one is not a probability and '
      'treating it as one manufactures a spurious two-year oscillation:'),
('eq', 'eq7', 7),
('eq', 'eq8', 8),

('p', 'The inflow of new graduates is the delay, Equation (9). The share entering field '
      '1 today determines the graduating cohort ⟪D⟫ years from now, and nothing an '
      'entrant does can change the ⟪D−1⟫ cohorts already enrolled:'),
('eq', 'eq9', 9),

('h2', '3.4. What Entrants Decide, and How'),

('p', 'Entrants compare the annuitised value of the two fields plus a constant amenity '
      'differential, Equation (10), and choose by a logit rule with intensity ⟪β⟫, '
      'Equation (11). The amenity absorbs everything that makes a field attractive for '
      'reasons other than its labour-market return, which the literature finds to be '
      'substantial {{beffy|wiswall_zafar}}:'),
('eq', 'eq10', 10),
('eq', 'eq11', 11),

('p', 'The forecast is where the paper departs from the classical cobweb. Two rules are '
      'available, Equation (12). The anchored rule reports the differential that would '
      'prevail if the field’s supply were at its long-run level: it is right on average '
      'but requires knowing that level, so it carries a cost ⟪c⟫. The extrapolative '
      'rule takes the most recent observation and projects the recent change forward '
      'with strength ⟪φ⟫: it is free, and while a trend lasts it is the more accurate '
      'of the two:'),
('eq', 'eq12', 12),

('p', 'The population weight on each rule is a logit in its recent realised accuracy, '
      'net of its cost, with intensity of choice ⟪ψ⟫, Equation (13); the population '
      'forecast is the weighted average, Equation (14). This is the adaptive belief '
      'system of Brock and Hommes {{brock_hommes97}}, and ⟪ψ⟫ is its bifurcation '
      'parameter. At ⟪ψ=0⟫ the weights never move and the system behaves as though '
      'beliefs were fixed. As ⟪ψ⟫ rises, entrants imitate what has recently worked more '
      'sharply, and because both rules forecast correctly when the system is at rest, '
      'the only thing separating them there is the cost of the anchored one. The free '
      'rule therefore crowds out the costly one precisely at the rest point, which is '
      'the mechanism by which a sensible individual decision rule destabilises a '
      'sensible aggregate:'),
('eq', 'eq13', 13),
('eq', 'eq14', 14),

('p', 'Two further parameters describe the information environment and are set to their '
      'neutral values in the baseline. The precision ⟪ω⟫ shrinks the perceived '
      'differential towards its long-run value, so a lower ⟪ω⟫ is a noisier signal '
      'about current conditions. The pipeline transparency ⟪p⟫ replaces part of the '
      'anchored rule’s forecast with the differential implied by the cohorts already '
      'enrolled: it is what a published enrolment series would give an entrant. Section '
      '5.5 varies both.'),

('figure', 'p9_fig1.png', 5.35, None, 'fig'),
('figcap', 1,
 'The structure of the model. A technology shock moves entry-level demand in the '
 'exposed field; the observed return feeds the forecasts on which this year’s entrants '
 'choose; their choice reaches the market only after the degree lag, and then adds to '
 'the entry-tier stock whose congestion determines the return. The loop is balancing, '
 'and the delay is what makes it slow enough to overshoot.'),

('h2', '3.5. Equilibrium, Stability and the Loop Gain'),

('p', 'A stationary equilibrium is an entering share, a pair of stocks and a pair of '
      'tightnesses such that the stocks reproduce themselves, free entry holds in both '
      'fields, and the share is the one the logit rule returns when both forecasting '
      'rules are correct. The stationary state is independent of ⟪ψ⟫ and ⟪φ⟫, which '
      'affect only the dynamics; that separation is what makes it possible to calibrate '
      'the labour block on stationary moments and then study the belief block without '
      'recalibrating.'),

('p', 'Local behaviour is summarised by the loop gain of Equation (15): the derivative '
      'of the entering share with respect to the share that entered ⟪D⟫ years before, '
      'holding the belief system at the anchored rule. It is the product of three '
      'elasticities—how much an extra cohort depresses a field’s marginal product, how '
      'much that lowers the value of entering it, and how strongly entrants respond—and '
      'it is negative, because crowding a field makes it less attractive. Under the '
      'anchored rule the map is a pure ⟪D⟫-period delay, so the eigenvalues are the '
      '⟪D⟫-th roots of the gain, the modulus is the ⟪D⟫-th root of its absolute value, '
      'and the oscillation that appears when stability fails has period ⟪2D⟫:'),
('eq', 'eq15', 15),

('p', 'With endogenous rule selection the state includes the belief system’s own memory '
      'and the algebra stops being informative, so we measure the dominant mode '
      'numerically: perturb the stationary state, simulate, and read the modulus off '
      'the slope of the log envelope of the response. Under anchored beliefs this '
      'agrees with the analytical benchmark, which is the check that the numerical '
      'procedure is measuring what it claims to.'),

('h2', '3.6. The Cost of Adjustment'),

('p', 'The welfare object is the output forgone while the system adjusts, Equation '
      '(16). The benchmark is the economy that moves to its new stationary share the '
      'moment the shock lands. The difference between that path and the realised one is '
      'what the adjustment itself costs: output lost because too many graduates hold '
      'the skills the economy has stopped wanting and too few hold the ones it now '
      'wants. It is a pure mismatch loss, and it is zero by construction if entrants '
      'forecast correctly:'),
('eq', 'eq16', 16),

# ============================================================ 4. Calibration
('h1', '4. Calibration'),

('h2', '4.1. Strategy'),

('p', 'The calibration is anchored on the economy before the technology shock rather '
      'than on the economy we observe today, and the reason is substantive. In this '
      'model a field with a high marginal product posts more vacancies, so it pays a '
      'higher wage and has a lower unemployment rate. The configuration observed in '
      'computing since 2023—an early-career wage premium that remains large alongside a '
      'new-graduate unemployment rate above the all-field average—is therefore not a '
      'stationary equilibrium of the model at all. It is what the model produces '
      'part-way through an adjustment, when a cohort sized for the old demand meets the '
      'new one. Calibrating to the pre-shock economy and then asking whether the shock '
      'reproduces today’s configuration turns the current data from a target into a '
      'test, and that test is reported in Section 4.4.'),

('p', 'Two normalisations come first because they determine what is identified. '
      'Matching efficiency and the vacancy cost enter every equilibrium object only '
      'through their ratio, so the vacancy cost is set to one. Only relative field '
      'productivity matters, so the unexposed field’s is set to one. The level of ⟪A₁⟫ '
      'that results is not interpretable on its own—the two labour inputs are different '
      'kinds of worker and are not measured in comparable units—so we report the '
      'implied relative demand index alongside it.'),

('h2', '4.2. Externally Set Parameters'),

('p', 'Table 1 lists what is fixed outside the estimation. Three entries carry the '
      'weight. The degree lag is four years, the institutional length of a bachelor’s '
      'degree; the empirical response of completed majors to wages peaks at about three '
      'years, because the decision is effectively taken at matriculation rather than at '
      'entry into the major {{long_majors}}, and Section 5.6 varies the lag from three '
      'to five; career-stage research has begun to treat the whole sequence of early '
      'career steps as itself being reorganised by the technology '
      '{{career1|career2}}. The elasticity of substitution between the two kinds of '
      'graduate is set '
      'to two, in the range the literature on substitution between skill groups '
      'supports {{katz_murphy|ciccone_peri}}, and is varied from 1.5 to 4; recent work on '
      'digital transformation and labour-structure upgrading suggests the two kinds of '
      'graduate are becoming less substitutable, not more '
      '{{digital_emp1|im_hc|training1}}. The entry '
      'tier lasts seven years, so a cohort is about a seventh of the stock it competes '
      'with.'),

('tabcap', 1,
 'Parameters set outside the estimation, and the two normalisations that determine '
 'what is identified.'),
('table', [
    ['Parameter', 'Symbol', 'Value', 'Source or justification'],
    ['Degree lag', '⟪D⟫', '4', 'Length of a bachelor’s degree; varied 3–5 in Section 5.6'],
    ['Discount rate', '⟪r⟫', '0.040', 'Annual real rate'],
    ['Matching elasticity', '⟪α⟫', '0.500', 'Consensus range of the matching-function literature'],
    ['Worker bargaining power', '⟪η⟫', '0.500', 'Hosios condition imposed at ⟪η=α⟫'],
    ['Separation rate', '⟪δ⟫', '0.100', 'Turnover of early-career employment'],
    ['Exit rate from the entry tier', '⟪γ⟫', '0.143', 'A seven-year entry tier, ages 22–29'],
    ['Elasticity of substitution', '⟪σ⟫', '2.000', 'Substitution between skill groups; varied 1.5–4'],
    ['Flow value of non-work', '⟪b⟫', '0.400', 'Standard range relative to the wage'],
    ['Trend extrapolation', '⟪φ⟫', '1.500', 'Belief block; varied in Sections 5.3–5.4'],
    ['Intensity of choice over rules', '⟪ψ⟫', '20.0', 'Belief block; swept 0–60 in Section 5.4'],
    ['Cost of the anchored rule', '⟪c⟫', '0.020', 'Belief block'],
    ['Memory in the fitness measure', '⟪m⟫', '0.500', 'Belief block; smooths rule switching'],
    ['Vacancy cost', '⟪κ⟫', '1.000', 'Normalisation: only ⟪μ/κ⟫ is identified'],
    ['Productivity, unexposed field', '⟪A₂⟫', '1.000', 'Normalisation: only relative productivity matters'],
], [2300, 900, 1000, 5300]),
('notes', 'Notes: The belief parameters govern the dynamics but not the stationary '
          'state, so the labour block can be calibrated on stationary moments without '
          'reference to them.'),

('h2', '4.3. Estimated Parameters and Targeted Moments'),

('p', 'Four parameters are estimated by matching four moments of the pre-shock '
      'graduate market. Matching efficiency governs the level of new-graduate '
      'unemployment; relative productivity governs the early-career wage premium; the '
      'amenity differential governs the share of the cohort that enters the exposed '
      'field, since a field can be both well paid and small; and the intensity of '
      'choice governs how strongly the share responds to the relative wage. The system '
      'is square, so the fit is exact by construction. What Table 2 reports is that an '
      'exact solution exists inside the admissible parameter space, which is not '
      'guaranteed, and that it is reached to twelve decimal places.'),

('p', 'The elasticity of field choice to the relative wage deserves a word, because it '
      'is the parameter the results are most sensitive to and the literature does not '
      'agree on it. Estimates run from near zero {{beffy}} through the response '
      'documented by Long, Goldhaber and Huntington-Klein {{long_majors}} to values '
      'above one in Freeman’s engineering market {{freeman76}}. We adopt 0.60 as a '
      'central value and, rather than defend it, map the model’s behaviour across the '
      'range 0.2 to 1.4 in Section 5.4. That range is wide enough to contain every '
      'published estimate we could verify, and the paper’s qualitative conclusions do '
      'not turn on where in it the truth lies.'),

('tabcap', 2,
 'Targeted moments, the fit, and the parameter each moment principally identifies.'),
('table', [
    ['Moment', 'Target', 'Model', 'Estimate', 'Parameter identified'],
    ['Share of the cohort in the exposed field', '0.055', '0.055', '−6.418',
     '⟪a⟫ amenity differential'],
    ['New-graduate unemployment, other fields', '0.055', '0.055', '3.848',
     '⟪μ⟫ matching efficiency'],
    ['Early-career wage premium of the exposed field', '1.350', '1.350', '0.106',
     '⟪A₁⟫ relative productivity'],
    ['Elasticity of field choice to the relative wage', '0.600', '0.600', '0.468',
     '⟪β⟫ intensity of choice'],
], [3900, 1000, 1000, 1100, 2500]),
('notes', 'Notes: The maximum absolute log deviation across the four conditions is '
          '1.8 × 10⁻¹³, so every target is matched to machine precision. The vacancy '
          'cost and the unexposed field’s productivity are normalised to one.'),
]
