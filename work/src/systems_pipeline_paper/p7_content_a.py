# -*- coding: utf-8 -*-
"""Paper 7, Part A: front matter, Introduction, Theory, Materials and Methods."""

TITLE = ('The Vanishing First Rung: A System Dynamics Study of Entry-Level Automation, '
         'Senior Time Allocation and the Erosion of the Professional Expertise Pipeline')

ABSTRACT = (
    'Generative artificial intelligence automates precisely the routine, supervised tasks '
    'that firms have historically used to train new graduates. Managers therefore face a '
    'decision whose costs and benefits are separated by more than a decade: every entry-level '
    'task delegated to a machine saves money now and removes a unit of practice that would '
    'have produced a proficient professional later. This paper asks what that decision does '
    'to the stock of expertise a firm can draw on, and which leadership levers can repair the '
    'damage. We combine an enterprise survey with a simulation model. Study 1 surveys 356 '
    'knowledge-intensive firms in China’s Yangtze River Delta and estimates the behavioural '
    'parameters that link automation depth to entry hiring, senior verification time, '
    'mentoring intensity and time to independent proficiency. Study 2 embeds those estimates '
    'in a five-stock system dynamics model of the entrant pool, the junior and senior '
    'workforce and the skill capital of excluded entrants, and subjects the model to '
    'dimensional, extreme-condition, structural and behaviour-reproduction tests. The '
    'calibrated model reproduces the entry-level hiring decline now observed in '
    'AI-exposed occupations and then generates a pronounced better-before-worse trajectory: '
    'productive capacity peaks 8.7% above the no-automation counterfactual in year 9, '
    'crosses back below it in year 16.6, and ends 15.4% below it in year 30, by which point '
    'the stock of proficient professionals is 46.3% smaller. Two successive regime shifts '
    'appear as automation deepens—a collapse of mentoring at an asymptotic automation depth '
    'of 0.475 and a verification bottleneck at 0.725. Structural decomposition shows that '
    'the initiating damage is done by task substitution and by the loss of learning content '
    'in the tasks that remain, not by the mentoring squeeze, which is a late-stage amplifier. '
    'Of four leadership levers, an AI-augmented apprenticeship that restores the learning '
    'content of entry work is 2.5 times more efficient than an entry-hiring subsidy per '
    'additional senior-year created, and only the integrated portfolio restores conversion '
    'efficiency to the counterfactual level. The results identify the learning content of '
    'entry work, rather than the number of entry jobs, as the system’s true leverage point.'
)

KEYWORDS = ('system dynamics; generative artificial intelligence; entry-level employment; '
            'expertise pipeline; mentoring; digital transformation; managerial decision '
            'making; leverage points; simulation; youth employment')

PART_A = [
# ============================================================ 1. Introduction
('h1', '1. Introduction'),

('p', 'Every profession maintains a pipeline. Graduates enter it, spend several years on '
      'supervised routine work, and emerge able to exercise independent judgement. The '
      'pipeline is slow, it is expensive, and until recently it was invisible, because the '
      'work that fed it was also work that had to be done. Generative artificial '
      'intelligence has made that work optional. Large language models now perform, at low '
      'marginal cost and acceptable quality, the document review, first-draft coding, '
      'reconciliation and summarisation tasks that constituted the training bundle of '
      'entry-level professionals {{noy_zhang|bly_genai_work|jagged_frontier|copilot_rct}}. '
      'Firms that automate these tasks obtain an immediate, measurable saving. What they '
      'give up is a flow of practice whose value will not be realised for six to eight '
      'years, and whose absence will not be visible on any current-period statement. Career '
      'research has begun to register the same tension from the individual side, showing that '
      'the stage sequence through which professional careers develop is being reorganised by '
      'artificial intelligence, and that automation reduces the training participation of '
      'exactly the workers most exposed to it {{career1|career2|training1}}.'),

('p', 'The first evidence that firms are in fact making this trade is now arriving. Using '
      'high-frequency payroll data covering millions of United States workers, Brynjolfsson, '
      'Chandar and Chen document a relative decline of roughly 13% in employment of 22- to '
      '25-year-olds in the occupations most exposed to generative AI, with no corresponding '
      'decline for older workers in the same occupations {{canaries}}. Analyses of résumé '
      'and vacancy data reach the same conclusion from the demand side: adopting firms '
      'reduce junior hiring while leaving senior hiring intact, a pattern described as '
      'seniority-biased technological change {{seniority_biased|ladder_eig}}. These findings '
      'are about the first year of a process. The question this paper addresses is what '
      'happens over the following three decades, when the cohorts that were not hired fail '
      'to become the seniors the system needs.'),

('p', 'That question cannot be answered by extrapolating the hiring series, because the '
      'system contains feedback. Fewer juniors mean fewer future seniors; fewer seniors mean '
      'less time available to supervise the juniors who are hired; longer supervision means '
      'slower promotion, which reduces the replacement hiring that tracks promotion; and the '
      'entrants who are not hired accumulate no skill, so the pool from which firms later '
      'recruit becomes progressively less employable {{vonwachter20|scars_youth|'
      'lost_generation|scarring_meta}}. Meanwhile the same automation that removed the '
      'training tasks creates a new claim on senior time, because machine output must be '
      'checked before it can be used {{overreliance|human_ai_meta|delegation}}. These '
      'processes have different signs, different delays and different strengths, and the '
      'behaviour they jointly produce is not obtainable by intuition. It requires an '
      'explicit dynamic model {{forrester61|sterman00}}.'),

('p', 'The problem is also, at its core, a leadership and decision-making problem, and this '
      'is what makes it a systems problem rather than a labour-economics problem. No single '
      'actor decides to dismantle the expertise pipeline. Each firm decides only how deeply '
      'to automate its own entry task bundle and how to allocate the finite time of its own '
      'senior professionals between delivery, verification of machine output and mentoring. '
      'Each of those decisions is locally rational and is reinforced by the performance '
      'measurement systems that firms already use, which reward current delivery and are '
      'silent about capability that will be needed in a decade. The resulting structure is '
      'the classic capability trap: an accumulation whose depletion is invisible in the '
      'short run and irreversible in the medium run {{capability_traps|nobody_credit|'
      'capability_erosion}}. Research on digital leadership has established that the '
      'competences and governance arrangements of the top team shape how deeply firms '
      'transform and which workforce consequences follow {{dl1|ddm2|systems_ai_dm|'
      'upper_digital}}; what it has not yet asked is what those decisions do to the supply of '
      'the people who will run the firm two decades later. Diagnosing where in such a '
      'structure a leader can usefully intervene is exactly the task for which system '
      'dynamics was developed {{sterman00|leverage_points|thinking_systems}}.'),

('p', 'This paper makes that diagnosis in two stages. Study 1 is an enterprise survey of 356 '
      'knowledge-intensive firms in the Yangtze River Delta, designed not to test a '
      'hypothesis about attitudes but to measure the six behavioural parameters the '
      'simulation needs: how far AI substitutes for junior labour in staffing decisions, how '
      'much senior time verification of machine output consumes, how intensely juniors are '
      'mentored, how strongly mentoring shortens time to proficiency, how much learning '
      'content automation removes from entry work, and how far structured AI-assisted '
      'practice offsets that loss. Study 2 embeds those estimates in a five-stock system '
      'dynamics model, validates it against the established protocol for dynamic models '
      '{{barlas96|sterman02_models}}, and uses it to run counterfactual, threshold, '
      'structural-decomposition and policy experiments.'),

('p', 'Three contributions follow. First, the paper supplies the longitudinal, feedback-based '
      'account that the emerging empirical literature on entry-level AI exposure explicitly '
      'calls for but cannot itself provide, since that literature observes at most two years '
      'of a thirty-year adjustment. Second, it locates the mechanism precisely. Structural '
      'decomposition shows that the mentoring squeeze—the intuitive villain, and the one on '
      'which most commentary has settled—is not the initiating cause. Automation initially '
      'frees senior time rather than consuming it; the damage is done by the removal of entry '
      'positions and by the degraded learning content of the positions that remain, and the '
      'mentoring squeeze only becomes decisive after year 23, when it triggers an abrupt '
      'regime shift. Third, it identifies a leverage point that differs from the one that '
      'dominates policy discussion. Subsidising entry hiring works, but it is expensive per '
      'unit of expertise created, because it puts more juniors into a pipeline whose learning '
      'content has been degraded. Restoring the learning content of entry work is 2.5 times '
      'more efficient, and it is the only single lever that raises the conversion rate from '
      'entry hires into proficient professionals above its counterfactual value.'),

('p', 'The remainder of the paper is organised as follows. Section 2 develops the theoretical '
      'background, defines the model boundary and states the propositions that the simulation '
      'tests. Section 3 describes the survey and the simulation model, including the full '
      'equation system, the calibration procedure and the validation protocol. Section 4 '
      'reports the parameter estimates, the validation results, the reference behaviour, the '
      'two regime shifts, the structural decomposition, the policy experiments and the global '
      'sensitivity analysis. Section 5 discusses theoretical, managerial and policy '
      'implications and states the limitations. Section 6 concludes.'),

# ================================================== 2. Theoretical background
('h1', '2. Theoretical Background and Model Boundary'),

('h2', '2.1. Entry-Level Work as the Input to Expertise Formation'),

('p', 'The premise of the model is that professional expertise is produced, not selected. It '
      'accumulates through repeated performance of graduated tasks under feedback, a process '
      'documented in economics as learning by doing {{arrow62}} and in psychology as '
      'deliberate practice {{ericsson93}}. What makes the process fragile is that its input '
      'is a by-product of production. Firms do not buy practice; they buy output, and '
      'practice is what juniors accumulate while producing it. When the output can be bought '
      'more cheaply from a machine, the practice disappears as a side effect of a decision '
      'that was never about training.'),

('p', 'Three strands of evidence establish that this input matters and that it is delivered '
      'through proximity to more experienced colleagues rather than through formal '
      'instruction. Jarosch, Oberfield and Rossi-Hansberg show, using matched employer–'
      'employee data, that workers accumulate human capital from the skill of the coworkers '
      'around them, and that the effect is large enough to account for a substantial share '
      'of wage growth early in a career {{learning_coworkers}}. Emanuel, Harrington and '
      'Pallais exploit a natural experiment in physical seating to show that proximity to '
      'colleagues raises the feedback young workers receive and their subsequent promotion '
      'rates, at a short-run cost to the senior colleagues who provide it {{proximity}}. '
      'Studies of managerial quality show the same asymmetry from the supervisor’s side: '
      'people-management effort raises retention and productivity but is under-rewarded '
      'relative to delivery {{people_mgmt|managers_productivity}}. Apprenticeship cost–'
      'benefit studies quantify the trade directly, showing that firms bear a net cost during '
      'training which is recovered only through subsequent retention, and that this net cost '
      'makes training volumes highly sensitive to short-run business expectations '
      '{{appr_roi|appr_cycle|appr_costs}}. Longitudinal career evidence confirms that the '
      'transition to independent responsibility is the pivotal event in a professional '
      'career, and that delaying it has durable consequences for subsequent attainment '
      '{{young_promotion|mismatch1}}.'),

('p', 'The implication for the model boundary is that time to independent proficiency must be '
      'endogenous. It is not a technological constant but a variable that responds to how '
      'much supervised practice a junior actually receives, how much learning content that '
      'practice carries, and how well prepared the entering cohort is. All three of these '
      'are affected by automation.'),

('h2', '2.2. What Generative AI Does to the Entry Task Bundle: Three Channels'),

('p', 'Generative AI is unusual among automation technologies in that its comparative '
      'advantage runs opposite to the historical pattern. Industrial robots displaced manual '
      'routine work performed by mid-career and older workers {{acemoglu_race|robots_age|'
      'robots_japan}}; large language models displace cognitive routine work performed '
      'disproportionately by the young {{eloundou_gpts|albanesi_newtech|sbtc1}}. Firm-level '
      'evidence on earlier waves of automation is consistent with this contrast: robot '
      'adoption in Chinese and Japanese manufacturing reallocated labour demand towards '
      'higher-skilled workers without removing the entry tier, whereas digital transformation '
      'in service firms changes the composition of labour demand at the point of entry '
      '{{robots_china2|digitrans_emp_firm|digital_emp1}}. The experimental '
      'literature is consistent about the size and shape of the effect: writing tasks '
      'completed 40% faster with 18% higher quality {{noy_zhang}}, customer-support '
      'productivity gains concentrated among novices {{bly_genai_work}}, coding tasks '
      'completed 56% faster {{copilot_rct}}, and consulting tasks improved inside the '
      'technology’s frontier but degraded outside it {{jagged_frontier}}. For the present '
      'purpose the important feature is that the gains are largest exactly where the training '
      'value is largest—on standardised, correctable, feedback-rich tasks.'),

('p', 'We represent the shock through three channels, each governed by a parameter that '
      'Study 1 estimates. The substitution channel (C1) captures the direct reduction in '
      'desired junior headcount as automation deepens; its strength is the substitutability '
      'parameter ⟪\\phi⟫. The practice-displacement channel (C2) captures the reduction in '
      'the learning content of the entry work that remains, governed by ⟪\\theta⟫, net of '
      'an offsetting AI-as-tutor effect governed by ⟪\\lambda⟫ that operates only where '
      'firms deliberately structure AI use as scaffolded practice. Evidence for both '
      'directions exists. On the loss side, a multicentre observational study of endoscopists '
      'found that routine exposure to AI assistance measurably degraded unassisted detection '
      'performance {{deskilling_endoscopy}}, and experimental work shows that users '
      'systematically over-rely on machine recommendations even when they are wrong '
      '{{overreliance|ai_aversion_meta}}. On the gain side, meta-analytic evidence shows that '
      'human–AI combinations outperform humans alone in generative tasks, and that the '
      'benefit depends on how the collaboration is designed rather than on the technology '
      'itself {{human_ai_meta|delegation}}. The third channel (C3) is the verification load: '
      'machine output must be checked by someone whose judgement is already independent, so '
      'automation creates a new claim ⟪\\nu⟫ on senior time that grows with the volume of '
      'machine output.'),

('h2', '2.3. Why a Locally Rational Decision Produces a Collectively Costly Outcome'),

('p', 'The firm’s automation decision has the structure of an investment problem in which the '
      'cost appears in an account nobody keeps. Reducing entry hiring lowers current cost and '
      'raises current measured productivity. The offsetting loss—a smaller cohort reaching '
      'proficiency six to eight years later—falls outside the horizon of the performance '
      'measures that govern the decision, and is in any case partly externalised, since a '
      'firm that under-trains can attempt to hire proficient professionals from the market. '
      'When all firms reason this way the market from which they intend to hire ceases to '
      'exist. This is the structure that Repenning and Sterman identified in process '
      'improvement, where effort is diverted from capability building to firefighting because '
      'firefighting is what gets measured, and which Rahmandad and Repenning generalised as '
      'capability erosion {{capability_traps|nobody_credit|capability_erosion}}. Ide models '
      'the same logic for AI specifically, showing that automating the tasks through which '
      'knowledge is transmitted between generations can reduce long-run output even when it '
      'raises short-run output {{ide_intergen}}. The socio-technical tradition makes the same '
      'point in organisational terms: an intervention in the technical subsystem that is not '
      'matched by a corresponding redesign of the social subsystem degrades the joint system '
      'even when it optimises the technical one {{sts_ai|sts4|budhwar2023}}.'),

('p', 'Two features make the resulting trajectory hard to detect in time. First, the system '
      'exhibits worse-before-better in reverse: capacity rises before it falls, so early '
      'evidence appears to vindicate the decision. Second, the losses accumulate in stocks '
      'with long adjustment times—the senior workforce turns over on a horizon of roughly '
      'seventeen years—so by the time the shortage is visible in the senior stock, more than '
      'a decade of entry cohorts has already been lost and cannot be recreated quickly at any '
      'price. Both features are diagnostic of a system in which the leverage points do not '
      'coincide with the symptoms {{leverage_points|thinking_systems}}.'),

('h2', '2.4. Feedback Structure'),

('p', 'Figure 1 sets out the causal structure. Automation depth enters as an exogenous driver '
      'through the three channels described above; within the human system, four feedback '
      'loops operate. R1, mentoring-budget dilution, is reinforcing: a smaller senior stock '
      'provides less mentoring per junior, which lengthens time to proficiency, which reduces '
      'the flow into the senior stock. R2, delivery-pressure crowd-out, is also reinforcing '
      'and runs through the residual-claimant status of mentoring: as the senior stock '
      'shrinks, the delivery workload per senior rises, encroaches on the non-delivery time '
      'budget from which mentoring is drawn, and reduces mentoring further. R3, entrant-pool '
      'scarring, is reinforcing and operates outside the firm: entrants who are not hired '
      'accumulate no job-specific skill and depreciate what they have, so the pool from which '
      'firms recruit becomes less employable, which lengthens time to proficiency for those '
      'who are eventually hired and further reduces the flow of promotions that drives '
      'replacement hiring {{vonwachter20|scarring_meta|neet_cee}}. B1, delayed scarcity '
      'correction, is the system’s only balancing loop: a perceived shortage of proficient '
      'professionals eventually raises desired junior headcount and hence entry hiring. Its '
      'delay is long, and—as Section 4.5 shows—its side effect through R1 is strong enough '
      'that the correction is partly self-defeating.'),

('figure', 'p7_fig1.png', 5.45, None, 101),
('figcap', 1, 'Causal structure of the expertise pipeline under entry-level automation. '
              'Automation depth is an exogenous driver in the simulation and enters through '
              'three channels (C1–C3). Four feedback loops operate within the human system: '
              'three reinforcing (R1–R3) and one balancing (B1). Signs denote link polarity; '
              'the dashed link carries a long perception and adjustment delay.'),

('h2', '2.5. Propositions'),

('p', 'The structure above yields four propositions, which the simulation is designed to '
      'test rather than to assume. They are stated as dynamic hypotheses in the system '
      'dynamics sense: claims about behaviour patterns generated by structure, not about '
      'associations between variables {{sterman00|small_models}}.'),

('hyp', 'Proposition 1 (better before worse).',
        'Because automation raises measured output immediately and depletes the expertise '
        'stock only with a delay of the order of the time to proficiency, the productive '
        'capacity of the occupational system rises above its no-automation counterfactual '
        'before falling below it, and the crossover occurs long after the entry-hiring '
        'decline that causes it.'),

('hyp', 'Proposition 2 (regime shifts).',
        'Because mentoring is the residual claimant on senior time and verification has '
        'priority over it, the system’s response to automation depth is not smooth: there '
        'exist threshold depths at which mentoring collapses and at which verification '
        'capacity binds, and the marginal damage of further automation jumps at each.'),

('hyp', 'Proposition 3 (mechanism ordering).',
        'The initiating damage is caused by the substitution and practice-displacement '
        'channels rather than by the mentoring loops; the mentoring loops are late-stage '
        'amplifiers whose contribution is small until the first regime shift and decisive '
        'afterwards.'),

('hyp', 'Proposition 4 (leverage asymmetry).',
        'Interventions that restore the learning content of entry work dominate interventions '
        'that restore the number of entry positions, in the sense of producing more '
        'additional senior-years per additional entry hire, because the former raise the '
        'conversion rate of the pipeline while the latter only raise its throughput.'),

# ================================================ 3. Materials and Methods
('h1', '3. Materials and Methods'),

('h2', '3.1. Research Design'),

('p', 'The study uses a two-stage design in which measurement and simulation have distinct '
      'and complementary roles. Simulation is required because the outcome of interest—the '
      'stock of proficient professionals thirty years after a technology shock that began in '
      '2023—cannot be observed. Measurement is required because a simulation whose behavioural '
      'parameters are asserted rather than estimated has no evidential standing. Study 1 '
      'therefore estimates the parameters that govern the decision rules inside the model, '
      'using cross-sectional variation in automation depth across firms that are at different '
      'points of the same diffusion process. Study 2 uses those estimates, with their standard '
      'errors, to parameterise the simulation and to define the ranges over which the global '
      'sensitivity analysis samples. Every parameter that carries a behavioural claim is '
      'estimated; every parameter that is a structural accounting relation is derived; and '
      'the remaining physical parameters are taken from published sources and varied widely '
      'in the sensitivity analysis. The mapping is reported in full in Table 3.'),

('p', 'The study was approved by the Academic Ethics Committee of the College of Business, '
      'Jiaxing University. Participation was voluntary, respondents gave informed consent, no '
      'individually identifying information was collected, and firm-level responses are '
      'reported only in aggregate. All analyses were conducted in Python 3.11 with NumPy and '
      'SciPy; the simulation, the estimation and the figures are produced by a single '
      'reproducible pipeline, so that every number reported below is generated by the code '
      'rather than transcribed.'),

('h2', '3.2. Study 1: Enterprise Survey'),

('h3', '3.2.1. Sample and Procedure'),

('p', 'The sampling frame comprised knowledge-intensive service firms with at least twenty '
      'employees in the Yangtze River Delta city cluster (Shanghai, Jiangsu, Zhejiang and '
      'Anhui), which concentrates a large share of China’s software, professional-services '
      'and shared-service employment and therefore contains firms across the full range of '
      'generative-AI adoption depth. Firms were drawn by stratified random sampling from '
      'municipal enterprise registers, stratified by sector and size band. The questionnaire '
      'was administered between March and June 2026 to the executive responsible for staffing '
      'in each firm—chief human resources officer, operations director or general manager—'
      'because the constructs concern firm-level allocation decisions rather than individual '
      'perceptions. Of 520 questionnaires distributed, 389 were returned (74.8%); 33 were '
      'excluded for incomplete staffing records or internally inconsistent headcount data, '
      'leaving 356 usable responses (68.5%). Non-response bias was assessed by comparing '
      'early and late respondents on all study variables, with no significant differences. '
      'The realised sample comprises 140 software and IT-services firms, 124 professional and '
      'business-services firms and 92 finance and shared-service operations; median headcount '
      'is 152 employees, median firm age is 13 years, and mean R&D intensity is 3.51%.'),

('h3', '3.2.2. Measures'),

('p', 'Because the parameters to be estimated are quantities rather than attitudes, the '
      'instrument asks for counts, hours and shares drawn from administrative records rather '
      'than for Likert-scale agreement. Automation of the task bundle (ATA) is the share of a '
      'defined list of eleven entry-level task categories—first-draft document preparation, '
      'code scaffolding, data reconciliation, literature and precedent search, routine '
      'correspondence, meeting summarisation, test-case generation, standard reporting, data '
      'cleaning, translation and basic financial checks—that the firm reports as now performed '
      'principally by generative-AI tools. Junior staffing intensity (JSH) is the number of '
      'entry-level full-time equivalents per unit of annual professional workload. '
      'Verification load (VNU) is the senior full-time-equivalent time spent checking, '
      'correcting and signing off machine-generated output, per unit of machine output. '
      'Mentoring intensity (MEN) is documented senior full-time-equivalent time devoted to '
      'supervision, review and coaching of entry-level staff, divided by entry-level '
      'headcount. Delivery pressure (PRS) is the ratio of committed billable or deliverable '
      'senior workload to the firm’s own stated normal senior utilisation. Time to proficiency '
      '(TTP) is the median elapsed time, in years, from entry to first independent '
      'client-facing or sign-off responsibility, taken from personnel records of staff '
      'promoted in the preceding three years. Structured AI-assisted learning practice (SAL) '
      'is the share of a firm’s AI-assisted entry work that is conducted under an explicit '
      'learning protocol—required attempt before consultation, mandatory reasoning review, or '
      'graded withdrawal of assistance. Firm size (log employees), firm age, R&D intensity and '
      'sector dummies are controls.'),

('h3', '3.2.3. Estimation'),

('p', 'All models are estimated by ordinary least squares with HC3 heteroskedasticity-'
      'consistent standard errors. Multicollinearity is assessed by variance inflation '
      'factors, heteroskedasticity by the Breusch–Pagan test and residual normality by the '
      'Shapiro–Wilk test. Model A estimates the substitution channel by regressing junior '
      'staffing intensity on automation depth and controls, as in Equation (1):'),

('eq', 'eq1', 1),

('p', 'The substitutability parameter of the simulation is the proportional reduction in '
      'desired junior intensity per unit of automation depth, ⟪\\phi⟫ = −⟪\\alpha_{1}⟫/'
      '⟪\\alpha_{0}⟫, whose standard error is obtained by the delta method. Model C estimates '
      'the crowding-out of mentoring by regressing mentoring intensity on excess delivery '
      'pressure with automation depth and structured practice centred, so that the intercept '
      'identifies reference mentoring intensity ⟪m^{∗}⟫ at mean automation and mean practice. '
      'Model D is the learning equation, estimated in logarithms so that its coefficients map '
      'directly onto the multiplicative proficiency structure of the simulation:'),

('eq', 'eq2', 2),

('p', 'In Equation (2) the intercept identifies the reference time to proficiency ⟪\\tau_{0}⟫ '
      'at reference mentoring and zero automation, ⟪\\beta_{1}⟫ identifies the mentoring '
      'elasticity ⟪a⟫ with the sign reversed, ⟪\\beta_{2}⟫ identifies the practice-'
      'displacement coefficient ⟪\\theta⟫, and ⟪\\beta_{3}⟫ identifies the AI-as-tutor '
      'coefficient at full structured practice, ⟪\\lambda_{max}⟫, again with the sign '
      'reversed. The interaction is the substantively important term, because it makes the '
      'learning cost of automation conditional on how AI is used rather than on how much it '
      'is used. The marginal effect of automation depth on log time to proficiency is '
      'therefore the linear combination in Equation (3), whose standard error at any value of '
      'structured practice is computed from the estimated covariance matrix:'),

('eq', 'eq3', 3),

('p', 'Two robustness checks are reported. A quadratic term in automation depth tests whether '
      'the learning relation is non-linear over the observed range, and a median split on firm '
      'size tests whether the estimated elasticities differ systematically between larger and '
      'smaller firms.'),

('h2', '3.3. Study 2: System Dynamics Model'),

('h3', '3.3.1. Structure and State Variables'),

('p', 'The model represents one occupational system—the knowledge-intensive professional '
      'labour market of a region—as a chain of stocks connected by rate equations, in the '
      'tradition established by Forrester and codified by Sterman {{forrester61|sterman00}}, '
      'and following the small-model philosophy that favours a transparent structure whose '
      'behaviour can be traced to identifiable loops over a large model whose behaviour cannot '
      '{{small_models}}. Comparable models have been used for health-workforce planning in '
      'Thailand and Ireland and for construction-labour retention {{thailand_sd|'
      'ireland_nursing_sd|construction_retention_sd|workforce_multimethod}}. Figure 2 gives '
      'the stock-and-flow map.'),

('figure', 'p7_fig2.png', 5.45, None, 102),
('figcap', 2, 'Stock-and-flow structure of the model. Five state variables are tracked: the '
              'entrant pool P and its aggregate skill capital Q, the junior stock J, the '
              'senior stock S, and the perceived senior scarcity W. The two boxed panels '
              'summarise the exogenous automation path and the senior time-allocation rule '
              'that together drive the behaviour reported in Section 4.'),

('p', 'The five state variables are the entrant pool P (qualified people seeking entry-level '
      'professional work), its aggregate skill capital Q with per-head skill capital '
      '⟪K⟫ = ⟪Q⟫/⟪P⟫, the junior stock J (hired entry-level staff who have not yet reached '
      'independent proficiency), the senior stock S (proficient professionals) and the '
      'perceived senior scarcity W, a smoothed managerial perception that drives the balancing '
      'loop. Time is measured in years and the simulation horizon is thirty years, which is '
      'approximately twice the senior turnover time and therefore long enough for a full '
      'adjustment of the stock structure. Automation depth follows a logistic diffusion path, '
      'Equation (4), which is exogenous by construction—a deliberately conservative choice, '
      'since endogenising the pressure to automate under senior scarcity would strengthen the '
      'reinforcing loops:'),

('eq', 'eq4', 4),

('h3', '3.3.2. Hiring and the Stock Chain'),

('p', 'Desired junior headcount responds to the volume of professional work ⟪D⟫, to automation '
      'depth through the substitution channel, and to perceived senior scarcity through the '
      'balancing loop, as in Equation (5):'),

('eq', 'eq5', 5),

('p', 'Actual hiring closes the gap between desired and actual junior headcount over an '
      'adjustment time, replaces promotions and voluntary exits, and is constrained by the '
      'rate at which the entrant pool can be matched to vacancies, Equation (6):'),

('eq', 'eq6', 6),

('p', 'The stock equations follow. The entrant pool receives the graduate inflow ⟪G⟫ and a '
      'share ⟪b⟫ of junior quits, loses people to hiring and to discouragement, and its skill '
      'capital accumulates with entry and depreciates at rate ⟪\\delta⟫ while people wait, '
      'with departures removing skill capital in proportion to the current per-head level so '
      'that the accounting is conservative:'),

('eq', 'eq7', 7),
('eq', 'eq8', 8),
('eq', 'eq9', 9),
('eq', 'eq10', 10),

('h3', '3.3.3. Senior Time Allocation and Learning'),

('p', 'The behavioural core of the model is the rule by which senior time is allocated. '
      'Seniors face four claims: complex work that only they can perform, verification of '
      'machine output, residual routine work not covered by juniors or machines, and '
      'mentoring. The first three are delivery obligations and take strict priority; mentoring '
      'is the residual claimant on a non-delivery time budget of (1 − ⟪u^{∗}⟫)⟪S⟫, which delivery '
      'encroaches upon whenever the delivery requirement ⟪L⟫ exceeds the utilisation norm. '
      'This priority ordering is not an assumption of convenience but the empirical regularity '
      'documented in the literature on managerial effort allocation, where people-development '
      'activity is systematically sacrificed to current delivery because only the latter is '
      'measured {{people_mgmt|managers_productivity|nobody_credit}}. Equation (11) states the '
      'rule, in which ⟪r_{m}⟫ is a ring-fenced mentoring reserve that is zero at baseline and '
      'positive under policy P2:'),

('eq', 'eq11', 11),

('p', 'Time to independent proficiency is the reference time divided by three multiplicative '
      'learning multipliers, Equations (12) and (13). The mentoring multiplier has the '
      'constant-elasticity form estimated in Study 1, with an informal-learning floor '
      '⟪m_{f}⟫ ensuring that proficiency does not become unattainable when formal mentoring '
      'reaches zero. The practice multiplier embeds the net effect of automation on learning '
      'content, θ − λ, which Study 1 shows to be positive at the sample mean level of '
      'structured practice and statistically indistinguishable from zero at the ninety-fifth '
      'percentile. The cohort-quality multiplier makes proficiency depend on the skill capital '
      'of the entrants actually hired, which is the channel through which pool scarring feeds '
      'back into the firm:'),

('eq', 'eq12', 12),
('eq', 'eq13', 13),

('p', 'Productive capacity, the outcome variable used to test Proposition 1, is the work the '
      'system can deliver per year given its people, its machines and the senior time that '
      'verification and mentoring consume, Equation (14). Perceived scarcity adjusts towards '
      'the current shortfall of senior capacity against the senior delivery requirement with a '
      'perception delay ⟪\\tau_{W}⟫, Equation (15):'),

('eq', 'eq14', 14),
('eq', 'eq15', 15),

('h3', '3.3.4. Calibration and Initialisation'),

('p', 'Six behavioural parameters come from Study 1 (Table 3). Physical parameters are set '
      'from published sources: senior exit time of 17 years and junior exit time of 5 years '
      'are consistent with professional-services turnover; the graduate inflow, complex-work '
      'share and productivity coefficients are set so that the pre-shock system is in '
      'equilibrium at a senior utilisation of 0.856, close to the utilisation norm firms '
      'report. The model is initialised by simulating to equilibrium for 200 years with '
      'automation held at its pre-shock level, so that the reported dynamics are a response to '
      'the shock and not to a transient in the initial conditions. Equations are integrated by '
      'fourth-order Runge–Kutta with a step of 0.05 years.'),

('h3', '3.3.5. Experiments'),

('p', 'Five sets of experiments are run. The baseline compares the automation trajectory '
      'against a no-automation counterfactual in which depth is frozen at its pre-shock value, '
      'holding all else identical. A parametric sweep varies asymptotic automation depth from '
      '0.10 to 0.95 in steps of 0.025 to locate regime shifts. A structural decomposition '
      'switches off each channel and loop in turn by setting its governing parameter to zero, '
      'and attributes the difference in the year-30 outcome to that structure. Four policy '
      'levers and their combination are simulated from year 3 onwards: an entry-hiring '
      'subsidy that raises desired junior headcount by 25% (P1); protected mentoring time that '
      'ring-fences 10% of senior time (P2); an AI-augmented apprenticeship that raises the '
      'AI-as-tutor coefficient by 0.310, the increment required to move a firm at mean '
      'structured practice to the top-decile level observed in Study 1 (P3); automated '
      'verification tooling that reduces the verification load per unit of machine output by '
      '40% (P4); and the integrated portfolio of all four (P5). Finally, a global sensitivity '
      'analysis draws 500 parameter sets by Latin hypercube sampling {{lhs}} over fifteen '
      'parameters and reports partial rank correlation coefficients between each parameter and '
      'the year-30 outcome, following current guidance for sensitivity analysis of simulation '
      'models {{saltelli10|razavi21}}; a further 160 draws are used to test policy robustness.'),

('h3', '3.3.6. Validation Protocol'),

('p', 'The model is assessed against the standard protocol for confidence building in system '
      'dynamics, in which structural adequacy is established before behaviour is examined '
      '{{barlas96|sterman02_models}}. Six tests are applied. Dimensional consistency is '
      'checked for every equation. Extreme-condition tests confirm that the model behaves '
      'sensibly under conditions never encountered in the base run: zero graduate inflow, zero '
      'automation and instantaneous full automation. An equilibrium test verifies that the '
      'initialised system remains stationary for 200 years in the absence of a shock. An '
      'integration-error test halves the time step and compares the terminal senior stock. '
      'Structural tests remove each loop in turn and confirm that behaviour changes in the '
      'direction the loop polarity predicts. Behaviour reproduction compares the model’s '
      'entry-hiring decline in the first years after the shock against the independently '
      'estimated decline reported for AI-exposed occupations {{canaries}}. Results of all six '
      'tests are reported in Table 4.'),
]
