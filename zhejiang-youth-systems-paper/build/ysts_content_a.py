# -*- coding: utf-8 -*-
"""Manuscript content, part A: front matter, introduction, theory, methods."""

TITLE = ("A Moving Target, Not a Tipping Point: Attractor Drift, Queue Congestion and "
         "Policy Sequencing in the Youth School-to-Work Transition System of China\u2019s "
         "Prefecture-Level Cities")

ABSTRACT = (
    "Youth non-employment has risen in China even where labour markets remain tight "
    "and the digital economy is expanding, which conventional shortage-of-jobs and "
    "shortage-of-skills accounts explain poorly. We model the graduate school-to-work "
    "transition of China’s prefecture-level cities as a six-state feedback system in "
    "which search, exam-oriented queueing, matched and mismatched employment, "
    "employability capital and aspirations co-evolve with an employer skill threshold "
    "that rises with digitalisation. Six structural parameters are estimated by "
    "simulated method of moments against seven published national moments, all "
    "reproduced within 1.7 per cent. Continuation and a multi-start search across "
    "forty parameter cells find a unique stable fixed point, so the system has no "
    "tipping point. Instead its attractor drifts: the equilibrium rate rises from "
    "0.117 to 0.637 between 2015 and 2040 while the realised state lags it by 1.7 "
    "years, so measured indicators understate structural deterioration. A three-year "
    "demand shock decays with a half-life of 1.5 years, whereas the threshold drift "
    "does not decay. A Sobol decomposition attributes 66.3 per cent of output "
    "variance to threshold sensitivity and 0.1 per cent to training intensity. At "
    "equal standardised effort, moderating threshold escalation lowers the 2040 rate "
    "by 0.157, roughly nineteen times the effect of vacancy creation, and deployment "
    "sequencing matters at unchanged cumulative effort."
)

KEYWORDS = ("youth employment; school-to-work transition; system dynamics; feedback loop "
            "dominance; slow employment; skill mismatch; digital economy; global "
            "sensitivity analysis; policy sequencing; prefecture-level cities")

PART_A = [

    # =====================================================================
    ('h1', '1. Introduction'),

    ('p', 'Between 2015 and 2026 the number of graduates entering China’s labour market '
          'rose from roughly 7.5 million to 12.7 million a year, and the surveyed urban '
          'unemployment rate of 16–24-year-olds excluding students peaked at 18.9 per '
          'cent in August 2025 before easing to 16.3 per cent in the second quarter of '
          '2026 {{nbs2026|moe2026}}. What makes this pattern analytically awkward is that '
          'it did not occur in a slack labour market. Over the same decade the value '
          'added of China’s digital core industries rose to 10.5 per cent of gross '
          'domestic product in 2024 and is targeted to exceed 15 per cent by 2030 '
          '{{nbs2026}}, and the vacancy-to-seeker ratio recorded by the public '
          'employment service has stayed above unity throughout. Jobs are being created; '
          'entry into them has nonetheless become slower and less certain. The '
          'phenomenon is national in scope but expressed locally: China’s roughly '
          'three hundred prefecture-level cities differ sharply in how fast their '
          'digital economies grow and in how many graduates they absorb '
          '{{zhoupolicy2024|wangguan2024}}, which makes the city the natural unit at '
          'which the mechanism operates.'),

    ('p', 'Three families of explanation dominate the literature, and each captures part '
          'of the phenomenon. The first is a quantity story: higher-education expansion '
          'has outpaced the creation of graduate-suitable positions {{li2014|china_youth1}}. '
          'The second is a quality story: graduates lack the competences that a '
          'digitalising economy rewards, so mismatch and over-education rise '
          '{{mcguinness2018|zheng2021|rikala2024}}. The third is a behavioural story: '
          'young people delay entry, queue for public-sector and institutional posts, or '
          'withdraw altogether, a pattern captured in China by the term "slow employment" '
          'and in Europe by the NEET construct {{rahmani2023|ilo2|grigorescu2025|neet_cee|yg}}. Each '
          'story is supported by credible evidence. None of them, on its own, explains '
          'why the three symptoms move together, why they persist once a cyclical '
          'disturbance has passed, or why the instruments that governments actually '
          'deploy—vacancy subsidies and training programmes—produce so much less than '
          'their nominal scale would suggest.'),

    ('p', 'The reason, we argue, is that quantity, quality and behaviour are not three '
          'competing causes but three state variables of one feedback system. Employers '
          'set a hiring threshold that responds to the technology they deploy and to the '
          'mismatch they observe. Graduates accumulate and lose employability capital '
          'depending on how long they search and on what they do while waiting. '
          'Aspirations adapt to attainable job quality, but slowly and from a sticky '
          'anchor set by educational attainment and family reservation support. A queue '
          'for scarce institutional posts absorbs part of each cohort, and its '
          'attractiveness depends on a success probability that the queue itself '
          'destroys. These couplings generate behaviour that no single-cause account '
          'anticipates, and they are exactly the kind of structure that systems practice '
          'in the social sciences was developed to analyse '
          '{{forrester1961|sterman2000|ghaffarzadegan2011}}.'),

    ('p', 'This paper builds and analyses such a system. We formulate a six-state '
          'continuous-time model of the graduate school-to-work transition in China, '
          'calibrate six structural parameters by simulated method of moments '
          'against seven published moments, and subject the calibrated model to a '
          'sequence of structural and statistical tests: fixed-point continuation and a '
          'multi-start uniqueness search, eigenvalue analysis, loop-deactivation '
          'experiments in the sense of Ford {{ford1999}}, Latin-hypercube Monte Carlo, '
          'Sobol variance decomposition {{sobol2001|saltelli2010}}, logistic and '
          'tree-based meta-modelling of the simulation output, and equal-effort policy '
          'experiments including deployment sequencing. Because prefecture-level cities '
          'differ in the speed of their digital transition rather than in the structure '
          'of their transition system, city heterogeneity is represented by '
          'parameterising the same model three ways rather than by adding a spatial '
          'dimension.'),

    ('p', 'Four findings follow, and three of them are negative results that we consider '
          'as informative as the positive ones. First, the system is globally monostable '
          'over the entire plausible parameter region we searched. There is no tipping '
          'point, no second attractor and no hysteresis. Second, what the system does '
          'have is a drifting attractor: the equilibrium towards which it moves rises '
          'from a non-employment rate of 0.117 in 2015 to 0.637 in 2040, and because the '
          'slowest relaxation time of the system is exactly eight years, the observed '
          'state lags this moving target by about 1.7 years on average. Measured youth '
          'non-employment therefore understates structural deterioration, systematically '
          'and by a knowable amount. Third, transitory demand shocks are absorbed: a '
          'three-year, 25 per cent reduction in the responsiveness of vacancies to '
          'digitalisation raises non-employment by at most 0.125 and decays with a '
          'half-life of 1.5 years. The youth employment problem of a digitalising '
          'economy is not a business-cycle problem. Fourth, the instrument that matters '
          'is not the one that is usually deployed. At equal standardised effort, '
          'moderating the rate at which employers raise the hiring bar reduces the 2040 '
          'non-employment rate by 0.157, against 0.008 for vacancy creation and 0.004 '
          'for training intensity.'),

    ('p', 'The contribution is threefold. Theoretically, we show that the youth '
          'employment predicament of a rapidly digitalising economy is better described as '
          'attractor drift under a slowly adjusting state than as a trap in the '
          'bistability sense, and we identify the specific feedback—endogenous escalation '
          'of the employer skill threshold—that drives the drift. Methodologically, we '
          'combine loop-deactivation dominance analysis with a full variance-based '
          'sensitivity decomposition and a statistical meta-model of the simulation '
          'output, so that structural claims and statistical claims are made about the '
          'same object. Practically, we provide an effort-normalised ranking of five '
          'policy families, a sequencing result showing that expectation guidance should '
          'precede rather than follow matching-efficiency investment, and an archetype '
          'analysis showing that the most digitally advanced prefecture-level cities '
          'face the steepest deterioration, while the intermediate manufacturing cities '
          'offer the largest absolute policy dividend.'),

    ('p', 'The remainder of the paper is organised as follows. Section 2 sets the system '
          'boundary and derives the feedback structure. Section 3 presents the model, the '
          'calibration and the analysis design. Section 4 reports results. Section 5 '
          'discusses their theoretical, methodological and policy implications, and '
          'their limits. Section 6 concludes.'),

    # =====================================================================
    ('h1', '2. Theoretical Background and System Boundary'),

    ('h2', '2.1. Youth Non-Employment as a System-Level Outcome'),

    ('p', 'A recurring insight of recent work on youth exclusion is that the outcome is '
          'emergent rather than attributable. Grigorescu, Alistar and Lincaru '
          '{{grigorescu2025}} model NEET vulnerability across 28 European countries as '
          'the joint product of digital-skill, behavioural and territorial subsystems, '
          'and show through a decision-tree analysis that the relationship between '
          'digital agency and exclusion is threshold-like rather than linear. '
          'Chacón-Cuberos and colleagues {{chacon2025}} approach the same construct from '
          'the individual side, validating a four-factor employability-thinking scale '
          'among 949 students in training and showing that ethical self-regulation, '
          'communication, proactivity and analytical thinking form a single '
          'inter-correlated competence system rather than separable skills. Both studies '
          'point in the same direction: youth labour-market outcomes are produced by '
          'interacting components whose joint behaviour differs from the sum of their '
          'separate effects. A parallel literature on institutional variation in '
          'school-to-work transitions {{stw|oecd2025}} and on digital divides across '
          'European populations {{eu1|eu2}} reaches the same conclusion from different '
          'directions, as does work on how careers unfold under technological change '
          '{{career1|career2|devos2020}}.'),

    ('p', 'Neither study, however, is dynamic. Cross-sectional and panel designs identify '
          'which variables matter; they cannot say how the configuration of those '
          'variables evolves, how fast it responds to intervention, or which of the '
          'couplings between them dominates observed behaviour at a given moment. That is '
          'the gap this paper addresses. The natural instrument is a small, transparent '
          'feedback model of the kind Ghaffarzadegan, Lyneis and Richardson '
          '{{ghaffarzadegan2011}} advocate for public policy: small enough that every '
          'loop can be named and tested, rich enough that the couplings which generate '
          'the puzzle are present.'),

    ('h2', '2.2. Why the Received Explanations Under-Determine the Dynamics'),

    ('p', 'The quantity account holds that graduate supply has outrun graduate-suitable '
          'demand. It is consistent with the expansion evidence {{li2014}} and with '
          'cross-country panel estimates linking tertiary enrolment to youth '
          'unemployment {{tleppayev2025}}. Yet the vacancy-to-seeker ratio recorded by '
          'China’s public employment service has remained above unity, and digital-industry '
          'expansion has been rapid and job-creating in the very cities where graduate '
          'non-employment has risen fastest {{zhoupolicy2024|liu2024sus|broadband}}. A pure '
          'quantity account predicts falling market tightness alongside rising '
          'non-employment; the data show the two moving in opposite directions.'),

    ('p', 'The quality account holds that graduates lack the competences employers now '
          'require. It is supported by the mismatch literature for China '
          '{{zheng2021|mismatch2|pan2025|mismatch1}} and by evidence that digital and '
          'intelligent technologies shift demand towards higher-order skills '
          '{{skill_demand|sbtc1|rikala2024|genai1|genai3}}. But this account treats the '
          'required skill '
          'level as exogenous. If employers respond to observed mismatch by raising '
          'screening standards further—demanding more experience, higher credentials or '
          'narrower specialisation—then the gap between what graduates have and what '
          'employers require is partly self-generated, and training alone will chase a '
          'target that moves in response to being chased.'),

    ('p', 'The behavioural account holds that young people delay entry. In China this '
          'takes an institutionally specific form. The national civil-service examination '
          'attracted 3.72 million qualified applicants for 38,100 posts in the 2026 '
          'cycle, and the ratio of candidates sitting the examination to posts rose from '
          '77:1 to 98:1 over three cycles. Delayed entry of this kind is not idleness: it '
          'is a rational option purchase whose value depends on a success probability of '
          'roughly one per cent. That such a probability sustains a queue of this size '
          'is difficult to reconcile with expected-utility reasoning but entirely '
          'consistent with the systematic over-weighting of small probabilities '
          'documented in prospect theory {{tversky1992|prelec1998}}. The behavioural '
          'account therefore requires a specific functional form, not merely a taste '
          'parameter.'),

    ('h2', '2.3. The Feedback Structure of the Transition System'),

    ('p', 'Combining the three accounts as coupled state variables rather than competing '
          'causes yields the causal structure of Figure 1. Seven feedback loops are '
          'identified, four reinforcing and three balancing. Their polarities are derived '
          'analytically from the sign of the product of link polarities around each '
          'cycle, and are confirmed numerically in Section 4.5.'),

    ('figure', 'fig1_cld.png', 6.55, None, 101),
    ('figcap', 1, 'Causal loop diagram of the youth school-to-work transition system. '
                  'Shaded boxes are stocks; the shaded oval at the top left is the '
                  'exogenous driver. A plus sign denotes a same-direction link, a minus '
                  'sign an opposite-direction link. Loop polarities are the products of '
                  'the link polarities around each cycle.'),

    ('p', 'Loop R1, skill decay while searching, is the classical scarring mechanism: a '
          'larger searcher pool dilutes the renewal of employability capital by fresh '
          'graduates and lengthens exposure to depreciation, which lowers the '
          'skill–threshold gap, reduces the screening pass rate, and enlarges the '
          'searcher pool further. Loop R2, queue–skill erosion, operates through the '
          'queue: time spent preparing for examinations builds credentials that the '
          'market does not price, so discouraged returnees re-enter search with degraded '
          'market-relevant capital, which lowers the value of open search and pushes the '
          'next cohort towards the queue. Loop R3, threshold escalation, is the '
          'mechanism the quality account omits: observed mismatch raises the effective '
          'hiring bar, which produces more mismatch. Loop R4, thin-market offer quality, '
          'is a congestion externality: a larger searcher pool lowers market tightness, '
          'which lowers offered job quality, which lowers acceptance and enlarges the '
          'pool.'),

    ('p', 'Against these, three balancing loops operate. Loop B1 is the ordinary matching '
          'loop of search theory {{petrongolo2001}}: more searchers generate more '
          'meetings and therefore more hires. Loop B2 is aspiration adjustment: sustained '
          'failure lowers the reservation threshold, which raises acceptance. Loop B3 is '
          'exam-queue congestion: a longer queue lowers the realised success rate, which '
          'lowers the perceived value of queueing. Whether the system deteriorates '
          'therefore depends not on any single loop but on which loops dominate at which '
          'time—a question that can only be answered by deactivating them one at a time '
          'in a calibrated model {{ford1999}}.'),

    ('h2', '2.4. Research Questions'),

    ('p', 'The analysis is organised around four questions. RQ1: does the transition '
          'system possess multiple equilibria, so that the observed deterioration can be '
          'described as a trap in the bistability sense, or a single attractor that '
          'moves? RQ2: how fast does the system adjust, and how large is the gap between '
          'the realised state and its instantaneous equilibrium? RQ3: which feedback '
          'loops and which structural parameters dominate the behaviour, and how much of '
          'the outcome uncertainty does each explain? RQ4: at equal effort, which policy '
          'instruments move the system furthest, and does the order in which they are '
          'deployed matter?'),

    # =====================================================================
    ('h1', '3. Model and Methods'),

    ('h2', '3.1. System Boundary'),

    ('p', 'The model represents the population of degree-holding labour-market entrants '
          'in China during an eight-year youth window, indexed in units of '
          '10 thousand persons. Endogenous are the allocation of that population across '
          'search, delayed entry, well-matched and mismatched employment; the mean '
          'employability capital of searchers; and the mean aspiration threshold. '
          'Exogenous are the size and growth of the entering cohort, the growth of '
          'vacancies, the intensity of digital transformation, and the number of '
          'institutional posts. Firms are not modelled as optimising agents; their '
          'behaviour enters through the hiring threshold and the offer-quality function. '
          'Wages appear only through a composite job-quality index. Geography enters '
          'through the prefecture-level city archetypes of Section 4.10: the same '
          'structure is re-parameterised to represent the three broad city types into '
          'which China’s prefecture-level cities fall, rather than being embedded in an '
          'explicit spatial model. The horizon is 2015 to 2040 with 2025 as the '
          'policy-intervention date.'),

    ('h2', '3.2. Stocks, Flows and Rate Equations'),

    ('p', 'Six state variables are tracked. Four are population stocks: open searchers '
          '⟪S⟫, exam-oriented queuers ⟪Q⟫, well-matched employment ⟪M⟫ and mismatched '
          'employment ⟪U⟫. Two are intensive states: the mean employability capital of '
          'the searching pool ⟪H⟫ and the mean aspiration threshold ⟪A⟫, both indices on '
          'the unit interval. Table 1 defines them together with the outcome indicators. '
          'Figure 2 gives the stock-and-flow structure.'),

    ('tabcap', 1, 'State variables, auxiliary variables and outcome indicators.'),
    ('table', [
        ['Symbol', 'Name', 'Unit', 'Role'],
        ['⟪S⟫', 'Open searchers', '10⁴ persons', 'Stock'],
        ['⟪Q⟫', 'Exam-oriented queuers (delayed entry)', '10⁴ persons', 'Stock'],
        ['⟪M⟫', 'Well-matched employment', '10⁴ persons', 'Stock'],
        ['⟪U⟫', 'Mismatched (over-educated) employment', '10⁴ persons', 'Stock'],
        ['⟪H⟫', 'Mean employability capital of searchers', 'Index (0–1)', 'Stock'],
        ['⟪A⟫', 'Mean aspiration (reservation quality)', 'Index (0–1)', 'Stock'],
        ['⟪\\Psi⟫', 'Digital core industries, share of GDP', 'Share', 'Exogenous driver'],
        ['⟪\\theta⟫', 'Employer skill threshold', 'Index', 'Auxiliary'],
        ['⟪x⟫', 'Skill–threshold gap, ⟪H⟫ − ⟪\\theta⟫', 'Index', 'Auxiliary'],
        ['⟪\\vartheta⟫', 'Market tightness, vacancies per searcher', 'Ratio', 'Auxiliary'],
        ['⟪q⟫', 'Offered job quality', 'Index', 'Auxiliary'],
        ['⟪h⟫', 'Hiring rate', '10⁴ persons yr⁻¹', 'Auxiliary'],
        ['NER', 'Youth non-employment rate, (⟪S⟫+⟪Q⟫)/pool', 'Share', 'Outcome'],
        ['SE', 'Slow-employment share of entrants', 'Share', 'Outcome'],
        ['MM', 'Vertical mismatch share of employment', 'Share', 'Outcome'],
        ['⟪D⟫', 'Mean transition duration to stable employment', 'Years', 'Outcome'],
        ['⟪R⟫', 'Queue-to-seat ratio (exam congestion)', 'Ratio', 'Outcome'],
    ], [1050, 3700, 1900, 1500]),
    ('notes', 'The pool is ⟪S⟫ + ⟪Q⟫ + ⟪M⟫ + ⟪U⟫. GDP denotes gross domestic product. '
              'Transition duration is obtained from the stock–flow identity of Little’s '
              'law applied to the non-employed stock and the inflow into stable '
              'employment.'),

    ('figure', 'fig2_stockflow.png', 6.55, None, 102),
    ('figcap', 2, 'Stock-and-flow structure. Rectangles are stocks, bow-tie symbols are '
                  'rate-controlling valves, clouds are boundaries of the system. The two '
                  'intensive states and the behavioural rate equations are shown at the '
                  'right.'),

    ('p', 'Digital transformation follows a logistic path fitted by least squares to the '
          'published national share of digital core industries in gross domestic '
          'product for 2020, 2023 and 2024 together with the 2030 policy target, with a '
          'maximum absolute residual of 0.06 percentage points {{nbs2026}}:'),
    ('eq', 'eq1', 1),

    ('p', 'The employer skill threshold has an exogenous component that rises with '
          'digitalisation and an endogenous component that rises with observed mismatch, '
          'the latter being the link that closes loop R3:'),
    ('eq', 'eq2', 2),

    ('p', 'The skill–threshold gap is the difference between what searchers carry and '
          'what employers require; it is the single most consequential auxiliary in the '
          'model, and its sign change is the behavioural signature discussed in '
          'Section 4.1:'),
    ('eq', 'eq3', 3),

    ('p', 'Meetings between searchers and vacancies follow a constant-returns '
          'Cobb–Douglas matching function of the form for which the empirical support is '
          'strongest {{petrongolo2001}}, and market tightness is the vacancy-to-searcher '
          'ratio:'),
    ('eq', 'eq4', 4),

    ('p', 'Three behavioural probabilities convert meetings into hires. The screening '
          'pass rate is logistic in the skill–threshold gap; the acceptance rate is '
          'logistic in the difference between offered quality and aspiration; and the '
          'probability that a realised hire is a good match is logistic in the gap with '
          'its own intercept. Here ⟪\\Lambda⟫ denotes the standard logistic function:'),
    ('eq', 'eq5', 5),

    ('p', 'Offered job quality rises with market tightness, which is the link that closes '
          'the congestion loop R4:'),
    ('eq', 'eq6', 6),

    ('p', 'The hiring rate is the product of meetings and the two probabilities, subject '
          'to a smooth capacity limit that prevents the searcher stock from being '
          'depleted faster than the minimum feasible search duration allows. The smooth '
          'minimum preserves continuous differentiability, which is required for the '
          'Jacobian analysis of Section 3.6:'),
    ('eq', 'eq7', 7),

    ('p', 'The allocation between continued open search and entry into the examination '
          'queue is a normalised logit comparison of two values. The value of search is '
          'the expected quality of a job obtained this period. The value of queueing is '
          'the value of an institutional post weighted by a Prelec probability-weighting '
          'function of the realised success rate, the compound-invariant form for which '
          'axiomatic support exists {{prelec1998|tversky1992}}. Because the weighting '
          'function is concave near zero, a success rate of order one per cent still '
          'carries substantial decision weight, which is what allows the queue to persist:'),
    ('eq', 'eq8', 8),

    ('p', 'Entry into and exit from the queue follow from that comparison, with a '
          'discouragement rate returning queuers to open search:'),
    ('eq', 'eq9', 9),

    ('p', 'The four population stocks then obey the following accounting identities, in '
          'which ⟪\\Phi⟫ is the entering cohort, ⟪\\omega⟫ the rate of exit from the '
          'youth window, and ⟪\\delta_{M}⟫ and ⟪\\delta_{U}⟫ the separation rates from '
          'matched and mismatched employment:'),
    ('eq', 'eq10', 10),
    ('eq', 'eq11', 11),
    ('eq', 'eq12', 12),

    ('p', 'Mean employability capital of the searching pool is renewed by fresh graduates, '
          'diluted by returning queuers whose market-relevant capital has eroded by a '
          'factor ⟪\\chi⟫, depreciated at rate ⟪\\delta_{H}⟫ during search, and raised by '
          'training effort ⟪\\tau⟫. The first term carries loop R1: as the searcher stock '
          'grows, cohort renewal per searcher weakens:'),
    ('eq', 'eq13', 13),

    ('p', 'Aspirations adjust towards a target that mixes a sticky anchor—set by '
          'educational attainment, family reservation support and peer reference '
          'points—with the currently attainable quality of a job. The anchoring weight '
          '⟪\\zeta⟫ and the adjustment speed ⟪\\lambda⟫ jointly determine how quickly '
          'loop B2 operates:'),
    ('eq', 'eq14', 14),

    ('p', 'Finally, the outcome indicators reported throughout are defined as follows, '
          'where ⟪D⟫ applies Little’s law to the non-employed stock:'),
    ('eq', 'eq15', 15),

    ('h2', '3.3. Data, Calibration and Its Limits'),

    ('p', 'The model is a policy-analysis model, not a forecasting model, and we are '
          'explicit about what the numbers are. Parameters fall into three classes. '
          'Twelve are set from published statistics or from the empirical literature and '
          'held fixed. Six are estimated. The remainder are structural constants of the '
          'functional forms. Table 2 reports all of them together with the uncertainty '
          'ranges used in the Monte Carlo and Sobol analyses. Where a value could not be '
          'sourced directly it is treated as uncertain and its influence is quantified '
          'rather than assumed away, following the reporting standards for '
          'simulation-based social science research set out by Rahmandad and Sterman '
          '{{rahmandad2012}}.'),

    ('tabcap', 2, 'Model parameters: base values, uncertainty ranges and provenance.'),
    ('table', [
        ['Symbol', 'Meaning', 'Base', 'Range', 'Provenance'],
        ['⟪\\Phi_{0}⟫', 'Entering graduate cohort, 2015', '749.0', '—',
         'Set, 10⁴ persons {{moe2026}}'],
        ['⟪g_{\\Phi}⟫', 'Cohort growth rate', '0.050', '0.030–0.070', 'Uncertain {{moe2026}}'],
        ['⟪\\omega⟫', 'Exit rate from the youth window', '0.125', '—', 'Set (8-year window)'],
        ['⟪V_{0}⟫', 'Vacancies, 2015', '948.7', '—', 'Scale normalisation'],
        ['⟪g_{V}⟫', 'Autonomous vacancy growth', '0.030', '—', 'Set'],
        ['⟪\\phi⟫', 'Vacancy elasticity to digitalisation', '1.60', '0.90–2.40', 'Uncertain'],
        ['⟪\\Psi_{0}⟫, ⟪\\Psi_{max}⟫, ⟪r_{\\Psi}⟫',
         'Digital-intensity logistic', '0.0503, 0.2552, 0.1171', '—',
         'Least squares on {{nbs2026}}'],
        ['⟪\\theta_{0}⟫', 'Baseline skill threshold', '0.500', '—', 'Normalisation'],
        ['⟪\\kappa⟫', 'Threshold sensitivity to digitalisation', '1.855', '1.10–2.80',
         'Estimated'],
        ['⟪\\kappa_{2}⟫', 'Endogenous threshold escalation', '0.150', '0.05–0.30', 'Uncertain'],
        ['⟪\\mu⟫', 'Matching efficiency', '9.922', '7.80–12.1', 'Estimated'],
        ['⟪\\alpha⟫', 'Matching elasticity', '0.500', '—', 'Set {{petrongolo2001}}'],
        ['⟪\\beta_{s}⟫', 'Screening sharpness', '6.00', '—', 'Set'],
        ['⟪\\sigma_{0}⟫', 'Match-quality intercept', '0.679', '—', 'Estimated'],
        ['⟪\\beta_{\\sigma}⟫', 'Match-quality slope', '4.00', '—', 'Set'],
        ['⟪d_{min}⟫', 'Minimum feasible search duration', '0.250', '—', 'Set (years)'],
        ['⟪q_{0}⟫, ⟪\\gamma_{q}⟫', 'Offer-quality intercept and slope',
         '0.560, 0.200', '—', 'Set'],
        ['⟪\\beta_{a}⟫', 'Acceptance sharpness', '7.00', '—', 'Set'],
        ['⟪A_{anch}⟫', 'Aspiration anchor', '0.820', '—', 'Set'],
        ['⟪\\zeta⟫', 'Aspiration anchoring weight', '0.550', '0.380–0.740', 'Uncertain'],
        ['⟪\\lambda⟫', 'Aspiration adjustment speed', '0.180', '0.090–0.320', 'Uncertain'],
        ['⟪h_{new}⟫, ⟪h_{max}⟫', 'Graduate and maximum capital',
         '0.620, 0.880', '—', 'Normalisation'],
        ['⟪\\delta_{H}⟫', 'Skill decay while searching', '0.060', '0.030–0.100',
         'Uncertain {{ilo3}}'],
        ['⟪\\chi⟫', 'Skill retention while queueing', '0.880', '0.780–0.960', 'Uncertain'],
        ['⟪\\tau⟫', 'Training intensity', '0.020', '0.008–0.040', 'Uncertain {{alm1}}'],
        ['⟪\\Pi⟫', 'Perceived value of an institutional post', '1.868', '1.27–2.67',
         'Estimated'],
        ['⟪\\varepsilon⟫', 'Probability-weighting curvature', '0.526', '0.360–0.720',
         'Estimated {{prelec1998}}'],
        ['⟪\\beta_{c}⟫', 'Choice sharpness (search versus queue)', '40.0', '—', 'Set'],
        ['⟪\\nu⟫', 'Maximal queue-entry rate', '0.755', '—', 'Estimated'],
        ['⟪\\nu_{r}⟫', 'Discouragement rate', '0.450', '—', 'Set'],
        ['⟪\\xi⟫', 'Institutional posts per entrant', '0.0030', '—',
         'Set from exam statistics'],
        ['⟪\\delta_{M}⟫, ⟪\\delta_{U}⟫', 'Separation rates', '0.100, 0.280', '—',
         'Set {{pan2025}}'],
    ], [1450, 3450, 1550, 1250, 1940]),
    ('notes', 'Ranges are the supports of the independent uniform priors used in the '
              'Latin-hypercube and Sobol designs; a dash indicates a parameter held fixed '
              'in those designs. "Estimated" denotes a parameter recovered by simulated '
              'method of moments (Table 3). Population stocks are in units of 10⁴ '
              'persons, so the model is scaled to the national graduate cohort; all '
              'reported outcomes are rates, shares and durations and are therefore '
              'invariant to that scaling. The higher separation rate for mismatched '
              'employment reflects the elevated quit intentions documented among '
              'over-educated Chinese graduates {{pan2025|mismatch1}}.'),

    ('p', 'Six parameters—the sensitivity of the employer threshold to digitalisation, '
          'matching efficiency, the perceived value of an institutional post, the '
          'probability-weighting curvature, the maximal queue-entry rate and the '
          'match-quality intercept—are estimated by simulated method of moments. The '
          'objective is the weighted sum of squared relative deviations between simulated '
          'and observed moments. The 2015 moments are evaluated at the model’s own '
          'frozen-driver fixed point, which also supplies the initial condition; the 2025 '
          'moments are evaluated after ten years of transient dynamics. Minimisation uses '
          'differential evolution with a Sobol-initialised population, followed by local '
          'polishing. With seven moments and six free parameters the system is '
          'over-identified, so the fit is informative rather than mechanical.'),

    ('tabcap', 3, 'Calibration by simulated method of moments: targets, sources and fit.'),
    ('table', [
        ['Moment', 'Year', 'Observed', 'Simulated', 'Relative error', 'Source'],
        ['Youth non-employment rate', '2015', '0.115', '0.117', '+1.70%',
         'Surveyed unemployment, aged 16–24 {{nbs2026}}'],
        ['Slow-employment share of entrants', '2015', '0.060', '0.060', '−0.14%',
         'Graduate destination surveys'],
        ['Vertical mismatch share', '2015', '0.180', '0.178', '−1.25%',
         'Over-education literature {{zheng2021}}'],
        ['Youth non-employment rate', '2025', '0.180', '0.178', '−1.10%',
         'Aged 16–24 excluding students {{nbs2026}}'],
        ['Slow-employment share of entrants', '2025', '0.191', '0.191', '+0.04%',
         'Graduate destination survey, 2024'],
        ['Vertical mismatch share', '2025', '0.240', '0.243', '+1.13%',
         'Over-education literature {{mismatch1|pan2025}}'],
        ['Queue-to-seat ratio', '2026 cycle', '96.0', '96.3', '+0.31%',
         'National civil-service examination'],
    ], [3050, 1150, 1200, 1200, 1400, 1640]),
    ('notes', 'Weighted objective value 0.000804. Root-mean-square percentage error '
              'across the seven moments is 1.16 per cent and the mean signed error '
              '+0.64 per cent, so the fit is close and very nearly unbiased. All '
              'targets are national series, which is the level at which the model is '
              'specified; Section 5.7 discusses what this implies for city-level '
              'inference.'),

    ('p', 'Two limits of this calibration should be stated plainly. First, the model is '
          'specified and estimated at the national level, so its parameters are '
          'population-weighted averages over China’s prefecture-level cities. The '
          'archetype analysis of Section 4.10 shows how much behaviour differs once '
          'those averages are relaxed, but it does not substitute for city-level '
          'estimation. Second, the model aggregates all forms of delayed entry into a '
          'single queue, whereas the civil-service examination is only one of them. '
          'Consistent with this, the model reproduces the 2026 congestion ratio closely '
          'but under-predicts the 2015 ratio (36 against 63), that is, it attributes '
          'more of the growth in delayed entry to the recent period than the '
          'examination series alone implies. Neither limitation affects the qualitative '
          'results, all of which are shown in Section 4.6 to be robust across the full '
          'parameter uncertainty range.'),

    ('h2', '3.4. Validation Protocol'),

    ('p', 'Following the taxonomy of Barlas {{barlas1996}}, validity is established in '
          'three stages: direct structure tests, structure-oriented behaviour tests and '
          'behaviour-pattern tests. Direct structure tests comprise dimensional '
          'consistency of every rate equation, verification that all stocks remain '
          'non-negative and that population accounting is closed, and extreme-condition '
          'tests. Structure-oriented behaviour tests comprise integration-error tests and '
          'the loop-deactivation experiments of Section 4.5. Behaviour-pattern tests '
          'compare simulated and published series on seven indicators, three of which '
          'were not used in estimation. Table 4 reports the results.'),

    ('tabcap', 4, 'Validation tests and outcomes.'),
    ('table', [
        ['Test', 'Class', 'Procedure', 'Result'],
        ['Dimensional consistency', 'Direct structure',
         'Units checked for all 20 rate equations',
         'Passed'],
        ['Boundary adequacy', 'Direct structure',
         'Every endogenous variable has at least one feedback path',
         'Passed'],
        ['Extreme conditions', 'Direct structure',
         'Zero cohort inflow, zero vacancies, zero institutional posts',
         'Stocks converge to admissible limits; no negative stocks'],
        ['Integration error', 'Structure-oriented',
         'Time step halved from 1/6 to 1/48 year',
         'Terminal NER identical to six decimal places'],
        ['Fixed-point consistency', 'Structure-oriented',
         'Residual of the frozen-driver fixed point',
         'Maximum absolute residual < 10⁻⁷'],
        ['Loop deactivation', 'Structure-oriented',
         'Each link held at its 2015 value in turn',
         'Signs of all six effects match the analytically derived polarities'],
        ['Uniqueness of the fixed point', 'Structure-oriented',
         'Multi-start solve from six initial guesses in 40 parameter cells',
         'Exactly one admissible fixed point in every cell'],
        ['Behaviour reproduction (in sample)', 'Behaviour pattern',
         'Seven estimation moments',
         'All within 1.7 per cent'],
        ['Behaviour reproduction (out of sample)', 'Behaviour pattern',
         'Digital-industry share 2024, vacancy-to-seeker ratio 2015, exam ratio 2015',
         '+0.5 per cent, +1.9 per cent, and under-prediction as discussed'],
        ['Sign of the skill-gap reversal', 'Behaviour pattern',
         'Year in which the skill–threshold gap changes sign',
         '2021, ahead of the observed post-2022 acceleration of youth non-employment'],
    ], [2450, 1750, 3050, 2390]),
    ('notes', 'NER denotes the youth non-employment rate. Out-of-sample indicators were '
              'not used in the estimation objective.'),

    ('h2', '3.5. Analysis Design'),

    ('p', 'Eight analyses are performed on the calibrated model. First, a baseline run '
          'from 2015 to 2040 under unchanged structure, integrated by fourth-order '
          'Runge–Kutta with a monthly step. Second, fixed points of the frozen-driver '
          'system are computed for each year, together with the Jacobian and its '
          'eigenvalues, giving the moving attractor and the spectrum of relaxation times '
          'defined by'),
    ('eq', 'eq16', 16),

    ('p', 'Third, two-directional continuation in the two candidate control parameters '
          '(the threshold sensitivity ⟪\\kappa⟫ and the value of an institutional post '
          '⟪\\Pi⟫) tests for fold bifurcations, and a multi-start search from six widely '
          'separated initial guesses across forty parameter cells—a 6 × 4 grid over the '
          'two strongest reinforcing parameters plus eight values each of ⟪\\kappa⟫ and '
          '⟪\\Pi⟫—tests for multiple equilibria. Fourth, loop dominance is assessed '
          'by deactivation: each candidate link is held at its 2015 value so that the '
          'loop passing through it cannot operate, while the level effect of the link is '
          'preserved {{ford1999}}. Fifth, a temporary demand shock is applied and the '
          'recovery half-life measured. Sixth, parameter uncertainty is propagated by a '
          'Latin-hypercube design of 4096 draws over the twelve uncertain parameters. '
          'Seventh, a Sobol variance decomposition with the Saltelli estimator quantifies '
          'first- and total-order contributions {{sobol2001|saltelli2010}}, using a '
          'scrambled Sobol sequence with a base sample of 1024, hence 14,336 model '
          'evaluations per output, with bootstrap confidence intervals from 800 '
          'resamples. The estimands and their estimators are'),
    ('eq', 'eq17', 17),
    ('eq', 'eq18', 18),

    ('p', 'Eighth, the Monte Carlo output is summarised by two meta-models. A binary '
          'outcome is defined as a 2040 non-employment rate exceeding 0.36, that is twice '
          'the 2025 benchmark, and is modelled by logistic regression on the twelve '
          'standardised parameters:'),
    ('eq', 'eq19', 19),

    ('p', 'A cost-complexity-pruned classification tree with the penalty selected by '
          'five-fold cross-validated area under the receiver operating characteristic '
          'curve provides interpretable thresholds, echoing the decision-tree stage used '
          'by Grigorescu and colleagues on European NEET data {{grigorescu2025}}. '
          'Finally, policy experiments move one or more parameters by a common number of '
          'prior standard deviations, so that instruments of different units are compared '
          'at equal standardised effort:'),
    ('eq', 'eq20', 20),

    ('p', 'Five instrument families are considered: P1 skill upgrading, which raises '
          'training intensity; P2 matching efficiency, which raises the efficiency of the '
          'matching function through public placement services and information platforms; '
          'P3 expectation guidance, which raises the aspiration adjustment speed and '
          'lowers the anchoring weight through career education of the kind measured by '
          'employability-thinking instruments {{chacon2025|devos2020}}; P4 vacancy '
          'creation, which raises the elasticity of vacancies to digitalisation through '
          'hiring subsidies; and P5 threshold moderation, which lowers both the exogenous '
          'and the endogenous sensitivity of the employer hiring bar through '
          'skills-based rather than credential-based hiring standards, publicly certified '
          'competence frameworks and structured internships that let employers observe '
          'ability directly {{reskill2024|rikala2024}}. All instruments are introduced in '
          '2025 and held constant thereafter, except in the sequencing experiments, where '
          'the same cumulative effort is redistributed over time. Statistical comparison '
          'across instruments uses the Kruskal–Wallis test with Mann–Whitney post-hoc '
          'comparisons under Bonferroni correction, and paired within-draw differences '
          'are tested by the Wilcoxon signed-rank test.'),
]
