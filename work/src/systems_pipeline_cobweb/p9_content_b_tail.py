# -*- coding: utf-8 -*-
"""Paper 9, Part B tail: Discussion, Conclusions, back matter, Appendix."""

TAIL = [
# ============================================================== 6. Discussion
('h1', '6. Discussion'),

('h2', '6.1. What the Delay Does, and What It Does Not Do'),

('p', 'The classical reading of a cobweb is that the delay causes the cycle. That is '
      'not quite what this model says. A four-year delay with anchored beliefs produces '
      'an overshoot, but a modest one: the entering share undershoots its long-run '
      'value, recovers, and settles, and the excess is a margin rather than a multiple. '
      'The delay is necessary but it is not sufficient. What converts a manageable '
      'adjustment into a large one is that the rule entrants use is itself chosen, and '
      'chosen on recent performance. During a downturn in a field the extrapolative '
      'rule is the accurate one, so its weight rises, so more entrants project the '
      'decline forward, so the decline deepens and the rule is vindicated again. The '
      'loop that selects the forecasting rule is reinforcing even though the loop that '
      'allocates students is balancing, and the reinforcing one operates on a much '
      'shorter timescale than the four years the balancing one needs.'),

('p', 'This is worth stating plainly because it changes what one would do about it. If '
      'the delay were the whole story the only remedies would be to shorten degrees or '
      'to make students forward-looking, neither of which is available. Because the '
      'amplification runs through rule selection, it responds to the information '
      'environment, which is available. That is the practical content of the '
      'distinction, and it is why Section 5.5 is the part of the paper a ministry could '
      'act on.'),

('h2', '6.2. Why More Information Can Make Things Worse'),

('p', 'The result that a sharper signal about current wages destabilises the system '
      'sits awkwardly beside a literature which finds that correcting students’ beliefs '
      'about earnings changes their choices and does so in the direction of better '
      'decisions {{wiswall_zafar|conlon_major}}. The two are not in conflict, and the '
      'reason is worth being precise about. Those studies are partial-equilibrium and '
      'static: one student is given better information, holding everyone else’s '
      'behaviour fixed, and she chooses better. The present model is neither. When '
      'every student receives the sharper signal simultaneously, the thing that is '
      'sharpened is the input to a rule that projects the present forward, and the '
      'aggregate response arrives four years later against a market that has moved. '
      'Better information about a variable makes an individual forecast better and can '
      'make a population forecast worse, because the population’s response is part of '
      'what has to be forecast.'),

('p', 'The literature on information provision has begun to record the same asymmetry '
      'from the empirical side: information interventions are not reliably effective '
      'once the setting has general-equilibrium content, and a centralised system in '
      'which everyone is informed at once behaves differently from a field experiment '
      'in which one arm is {{haaland|ajayi_info}}. The systems literature reached the '
      'same conclusion decades earlier and stated it as a general property: the '
      'leverage in a system with delays lies in the structure of its information flows '
      'rather than in the strength of its signals {{meadows_ts|forrester71}}, and '
      'people managing a stock with a long supply line systematically over-correct when '
      'they can see the stock but not the line {{sterman_misperc}}. The contribution '
      'here is to price that claim in a market where the supply line is a cohort of '
      'students and the over-correction is a career.'),

('h2', '6.3. What Should Be Published'),

('p', 'The stabilising information in this model is the pipeline: how many students are '
      'currently enrolled in each field and when they will graduate. That is not a new '
      'survey. Every education ministry and every national statistical office already '
      'holds it, because enrolment is how institutions are funded. What is missing is '
      'publication in a form a seventeen-year-old or her adviser can use—by field, by '
      'expected graduation year, and alongside the size of the market those graduates '
      'will enter.'),

('p', 'Three series would do most of the work, and all three are constructible from '
      'existing administrative data. The first is enrolment by field and expected '
      'graduation year, which is the pipeline itself. The second is the ratio of the '
      'expected graduating cohort in a field to current entry-level hiring in the '
      'occupations that field feeds, which is the congestion an entrant will actually '
      'meet. The third is the same ratio’s recent history, so that a student can see '
      'whether the field she is considering is one that others are also leaving. None '
      'of these is a forecast, which matters: a ministry that publishes a forecast '
      'takes on a liability and invites the criticism that it got the forecast wrong, '
      'whereas a ministry that publishes the pipeline is publishing a fact.'),

('p', 'The measurement point generalises beyond the instrument. The statistic that '
      'currently governs this debate is the graduate unemployment rate by field, which '
      'is a lagging indicator of a stock. By the time it moves, the cohorts that will '
      'respond to it have already chosen. An indicator chosen because it is available '
      'and comparable comes to define the problem, and this one defines it as a '
      'question about the graduates who already exist rather than about the ones being '
      'produced {{meadows_ts}}.'),

('h2', '6.4. Implications for Systems with Administered Enrolment'),

('p', 'The model assumes that entrants allocate themselves and that capacity '
      'accommodates them. Several important systems do not work that way. In China the '
      'Ministry of Education sets and adjusts programme quotas directly, so the '
      'planner holds an instrument the model’s planner does not: it can move the '
      'entering share without persuading anyone. That is a genuine advantage and it '
      'comes with a genuine hazard, and the model speaks to both.'),

('p', 'The advantage is that quota smoothing does not require students to change how '
      'they forecast; it simply limits how far the aggregate can move in a year, which '
      'is exactly the variable the amplification operates on. The hazard is that an '
      'administrative system responds to the same lagging indicator that students do, '
      'with its own decision lag on top of the degree lag. A planner who expands '
      'programme places in the fields where graduate unemployment is currently low, and '
      'contracts them where it is currently high, is running the extrapolative rule '
      'with a larger instrument and a longer delay. The literature on China’s '
      'higher-education expansion documents how durable such capacity decisions are '
      'once taken {{li_whalley|ou_zhao|huang_returns}}, and the durability is precisely '
      'what makes an over-correction expensive. The model’s advice to an administrative '
      'system is therefore the mirror image of its advice to a market one: the '
      'instrument to use is the one that damps the aggregate swing, and the indicator '
      'to avoid steering on is the one that arrives late.'),

('h2', '6.5. Limitations'),

('p', 'Five limitations bound these conclusions. The first is the one that matters '
      'most: the belief block’s three parameters—the strength of trend extrapolation, '
      'the intensity of choice over rules and the cost of the anchored rule—are set '
      'rather than estimated, because the data that would identify them are individual '
      'expectations of field-specific returns over time, and we know of no panel that '
      'contains them. We therefore report behaviour across the whole plausible range of '
      'these parameters rather than at a point, and the qualitative results—overshoot, '
      'amplification rising in the intensity of choice, the sign of the two information '
      'instruments—hold throughout that range. The magnitudes do not, and should be '
      'read as illustrative of a mechanism rather than as forecasts.'),

('p', 'Second, the model has two fields. Real students choose among dozens, and the '
      'substitution patterns among them are not symmetric: a student leaving computing '
      'is more likely to enter engineering than nursing. A richer field structure would '
      'dilute the congestion effect for any one field and would let the shock '
      'propagate unevenly, which is a first-order extension rather than a refinement. '
      'Third, we hold the size of the entering cohort fixed, so the model cannot speak '
      'to the margin between higher education and no higher education, which is where '
      'much of the recent adjustment in some countries has occurred.'),

('p', 'Fourth, the shock is permanent and unanticipated, and it is calibrated to a '
      'single observable. A shock that agents expect to reverse would produce a smaller '
      'response, and one that arrives gradually would produce a smoother one; the '
      'evidence on whether the contraction in entry-level technical hiring is permanent '
      'is, at the time of writing, exactly what is in dispute {{canaries|still_waters}}. '
      'Fifth, the model has no on-the-job mobility: a graduate who trained in one field '
      'never works in the other. That assumption makes the congestion effect stronger '
      'than it should be, and relaxing it would damp the cycle. It also, however, '
      'understates the cost of the mismatch, since in the data field-switching involves '
      'a substantial earnings penalty {{kirkeboen|deming_noray}}.'),

# ============================================================== 7. Conclusions
('h1', '7. Conclusions'),

('p', 'Demand for a field of study can change in a year. The supply of graduates in '
      'that field cannot change in less than the length of a degree. This paper asks '
      'what an education system does with that mismatch, and answers it with a model in '
      'which the labour market is frictional, the two kinds of graduate are imperfect '
      'substitutes, and entrants forecast the return to a field using rules whose '
      'popularity depends on how well they have recently worked.'),

('p', 'The central finding is that the enrolment response to a demand shock overshoots '
      'its own long-run value by a large multiple, so that most of the collapse in '
      'enrolment observed after such a shock is transitional rather than warranted. The '
      'overshoot is not produced by the delay alone; it is produced by the delay '
      'together with the endogenous selection of forecasting rules, and it grows '
      'monotonically in the sharpness with which students imitate what has recently '
      'worked. Past a critical sharpness the stationary state loses stability '
      'altogether. Nothing in that sequence requires anyone to behave irrationally: '
      'each rule is reasonable, each student is responding sensibly to what she can '
      'see, and the aggregate is nonetheless worse than it needs to be.'),

('p', 'The policy conclusion is about which information is supplied rather than how '
      'much. Sharpening what students know about current returns feeds the rule that '
      'projects the present forward and moves the system towards instability. '
      'Publishing what is already in the pipeline—the cohorts enrolled and not yet '
      'graduated—moves it away, because it lets an entrant price the congestion she '
      'will actually meet rather than the one she can currently see. That series is an '
      'administrative by-product every education system already holds. The obstacle to '
      'using it is not measurement.'),

('p', 'The wider point concerns what a labour-market indicator can be asked to do. The '
      'graduate unemployment rate by field describes the graduates who already exist. '
      'The decision that determines the next cohort is taken four years before that '
      'rate will register it, by people who cannot observe one another. A system that '
      'steers on the indicator it has will keep arriving late, and will keep mistaking '
      'the size of its own correction for the size of the shock it is correcting for.'),

# =============================================================== back matter
('back', 'Author Contributions:',
 'Conceptualization, methodology, formal analysis, software and writing—original draft '
 'preparation, X.C.; validation, data curation and visualization, D.H.; investigation, '
 'writing—review and editing, and supervision, T.M. All authors have read and agreed '
 'to the published version of the manuscript.'),
('back', 'Funding:',
 'This research was funded by the Zhejiang Provincial Philosophy and Social Sciences '
 'Planning Special Project on Higher Education Basic Research Funding Reform (Grant '
 'Number: 25NDJC153YBMS) and the Major Humanities and Social Sciences Research Projects '
 'in Zhejiang Higher Education Institutions (Grant Number: 2024QN018).'),
('back', 'Institutional Review Board Statement:',
 'Not applicable. The study is a structural simulation calibrated to published '
 'aggregate statistics and involves no human participants or animals.'),
('back', 'Informed Consent Statement:', 'Not applicable.'),
('back', 'Data Availability Statement:',
 'The model is fully specified by Equations (1)–(16). No individual-level data were '
 'used; every calibration target is drawn from the published sources listed in Table 3. '
 'The code that solves, calibrates and simulates the model and that generates every '
 'figure and table in this paper is available from the corresponding author on '
 'reasonable request.'),
('back', 'Acknowledgments:',
 'The authors thank the editors and the anonymous reviewers for comments that improved '
 'the manuscript.'),
('back', 'Conflicts of Interest:', 'The authors declare no conflicts of interest.'),

('h1', 'Abbreviations'),
('p', 'The following abbreviations are used in this manuscript: ABS, adaptive belief '
      'system; AI, artificial intelligence; CES, constant elasticity of substitution; '
      'DMP, Diamond–Mortensen–Pissarides; LHS, Latin hypercube sampling.'),
]
