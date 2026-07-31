# -*- coding: utf-8 -*-
"""Paper 8, Part A: front matter, Introduction, Theory, Materials and Methods."""

TITLE = ('Screening Under Signal Collapse: Choice and Architecture Experiments on '
         'Employer Decision Rules and Youth Access to Entry-Level Work')

ABSTRACT = (
    'Generative artificial intelligence has made a polished written application almost '
    'free to produce, and a signal that is free to produce cannot separate candidates. '
    'Employers screening entry-level applicants must therefore decide what to rely on '
    'instead, and that decision determines which young people reach a human interviewer. '
    'This paper measures the decision rule and then manipulates the architecture that '
    'frames it. A choice-based conjoint with 452 managers who make entry-level shortlist '
    'decisions in knowledge-intensive firms of China’s Yangtze River Delta yielded 6328 '
    'choice sets over seven candidate attributes, analysed by conditional logit, mixed '
    'logit estimated with 500 scrambled Halton draws, and latent-class conditional logit. '
    'Embedded in the same instrument, a randomised experiment assigned each respondent to '
    'one of three screening architectures and measured the shortlist they produced from a '
    'fixed candidate pool. Disclosing that an application was AI-assisted carried a clear '
    'penalty, but a portfolio documenting the applicant’s drafting and revision process '
    'removed about three quarters of it, and the two attributes interacted significantly. '
    'Preferences were not merely heterogeneous but discretely so: three screening regimes '
    'emerged, weighting credentials, test scores and process evidence respectively, and '
    'membership shifted towards the credential regime as managers perceived more '
    'AI-assisted applications. The architecture experiment showed that the same managers '
    'produce very different shortlists depending on what the interface puts first: '
    'ordering candidates by verified evidence rather than by credentials raised the share '
    'of shortlisted applicants from non-elite institutions while also raising the '
    'shortlist’s measured assessment quality, so the equity–quality trade-off managers '
    'assume is an artefact of the architecture rather than a property of the applicant '
    'pool. Screening architecture is a leadership decision with distributional '
    'consequences, and it is more consequential than the preferences of the individuals '
    'who operate it.'
)

KEYWORDS = ('discrete choice experiment; generative artificial intelligence; employer '
            'screening; signalling; youth employment; entry-level hiring; latent class '
            'analysis; mixed logit; digital transformation; managerial decision making')

PART_A = [
# ============================================================ 1. Introduction
('h1', '1. Introduction'),

('p', 'A written job application has always been a test of two things at once: whether '
      'the applicant can do the work, and whether the applicant can be bothered to '
      'demonstrate it. Generative artificial intelligence has severed the two. A '
      'competent, tailored cover letter and a cleanly structured résumé are now available '
      'to any applicant in a few minutes at negligible cost, which is precisely the '
      'condition under which a signal stops carrying information. Spence’s original result '
      'is unambiguous on this point: a signal separates types only when it is '
      'differentially costly to produce {{spence73}}. Remove the differential cost and the '
      'signal pools.'),

('p', 'This is no longer a theoretical worry. Analysing more than five million cover '
      'letters submitted around the rollout of an AI writing tool on a large freelancing '
      'platform, Cui, Dias and Ye find that the correlation between how well a cover '
      'letter matched the job post and whether the applicant was called back fell by about '
      'half, and that employers shifted weight onto verifiable histories instead '
      '{{cover_letters_ai}}. Galdin and Silbert reach the same conclusion structurally: '
      'employers’ willingness to pay for a tailored application disappears after large '
      'language models become available, and their counterfactual implies a measurably '
      'less meritocratic market {{making_talk_cheap}}. Field-experimental evidence '
      'confirms that algorithmic writing assistance changes outcomes rather than merely '
      'polishing prose, raising hires by around 8% on an online labour market '
      '{{writing_assist}}. On the employer side, screening itself is being automated, and '
      'automated screeners bring their own distortions: large language models '
      'systematically favour résumés written by the same model {{ai_self_preferencing}} '
      'and reproduce demographic patterns from their training data {{resume_lm_bias}}.'),

('p', 'The consequences fall hardest on the young. Payroll microdata show a relative '
      'employment decline of roughly 16% for workers aged 22 to 25 in the occupations most '
      'exposed to generative AI, with no comparable decline for older workers doing the '
      'same jobs {{canaries}}; résumé and vacancy data show adopting firms cutting junior '
      'hiring while senior hiring holds steady {{seniority_biased}}. The evidence is not '
      'uniform—Danish administrative data yield precise nulls over the same period '
      '{{still_waters}}—but the entry tier is where the disagreement is concentrated, and '
      'it is the tier where the written application does most of the work, because young '
      'applicants have no employment record to fall back on. Where the first job lands has '
      'durable consequences: the size and quality of the first employer shape earnings '
      'years later {{first_job_firm}}, and a poor or delayed entry leaves scars that do not '
      'heal quickly {{vonwachter20|scarring_synthesis}}.'),

('p', 'What employers do when a signal fails is therefore a question of the first '
      'importance, and it is a decision question rather than a technology question. A '
      'manager facing a doubled pile of uniformly polished applications has three broad '
      'options. She can fall back on signals that are cheap to verify because they are '
      'conferred by institutions rather than produced by the applicant—the selectivity of '
      'the university, an internal referral. She can triage on volume, letting an '
      'automated score do the first cut. Or she can try to restore a costly signal by '
      'requiring something an applicant cannot cheaply fake even with a capable model: a '
      'proctored assessment, or documentary evidence of how a piece of work was actually '
      'produced. These are not equivalent. The first two are cheap and fast, but '
      'institutional signals are strongly correlated with family background '
      '{{ivy_plus|class_advantage}} and referral networks are unevenly distributed '
      '{{referral_value}}, so both narrow access without necessarily improving the match. '
      'The third is more costly to operate but is the only one that re-establishes the '
      'condition a signal needs in order to inform.'),

('p', 'This paper measures which of these employers actually choose, and then tests '
      'whether the choice can be changed by design. We do two things. First, we run a '
      'choice-based conjoint experiment with 452 managers who make real entry-level '
      'shortlist decisions in knowledge-intensive firms in China’s Yangtze River Delta. '
      'Each evaluated pairs of hypothetical entry-level candidates that varied on whether '
      'the application disclosed AI assistance, whether it was accompanied by a '
      'process-evidence portfolio, the result of a verified proctored assessment, '
      'institutional tier, referral, internship, and expected salary. Including salary as '
      'an attribute lets every other attribute be expressed as a compensating differential '
      'in money, which makes the weights comparable and interpretable. Second, embedded in '
      'the same instrument, we randomly assigned each respondent to one of three screening '
      'architectures—ordering a fixed candidate pool by an AI score, by credentials, or by '
      'verified evidence—and recorded the shortlist they produced. The conjoint identifies '
      'the decision rule; the randomisation identifies what a leadership decision about the '
      'screening interface does to who gets through.'),

('p', 'The design lets us make four contributions. First, we quantify the penalty '
      'attached to disclosing AI assistance and show that it is not a fixed cost of '
      'honesty: a portfolio documenting drafts, revisions and reasoning removes about three '
      'quarters of it, and the interaction between disclosure and process evidence is statistically '
      'significant. This matters because a disclosure penalty without a repair mechanism '
      'creates a trap—applicants conceal, the written signal degrades further, and '
      'employers retreat further into ascriptive signals. Second, we show that employer '
      'heterogeneity is discrete rather than continuous. Three screening regimes emerge '
      'from a latent-class model, weighting credentials, test results and process evidence '
      'respectively, and they predict held-out choices better than either a homogeneous or '
      'a continuous-heterogeneity specification. Third, we link regime membership to the '
      'condition of the signal environment: managers who believe more of their applications '
      'are AI-assisted are more likely to sit in the credential regime, which is the '
      'retreat the theory predicts. Fourth, and most consequentially for practice, we show '
      'experimentally that the screening architecture dominates the screener. Moving from '
      'a credential-first to an evidence-first interface changed the composition of the '
      'shortlist far more than the differences between individual managers’ preferences, '
      'and it did so while raising rather than lowering the measured quality of the '
      'shortlisted candidates.'),

('p', 'The paper is organised as follows. Section 2 develops the theoretical background '
      'and states the hypotheses. Section 3 describes the two experiments, the '
      'experimental design, and the estimation strategy. Section 4 reports the results. '
      'Section 5 discusses the implications for theory, for leadership practice and for '
      'policy, and states the limitations. Section 6 concludes.'),

# ================================================== 2. Theoretical background
('h1', '2. Theoretical Background and Hypotheses'),

('h2', '2.1. Signals, Screens and the Cost Condition'),

('p', 'The economics of hiring under asymmetric information rests on a single mechanism. '
      'An applicant attribute functions as a signal only if acquiring or displaying it '
      'costs less for high-productivity than for low-productivity applicants; otherwise '
      'every type displays it and the employer learns nothing {{spence73}}. Employers who '
      'observe workers over time gradually substitute direct evidence of productivity for '
      'the initial signal, which is why the weight on credentials falls as tenure '
      'accumulates {{altonji_pierret}}. At the point of entry, however, no such direct '
      'evidence exists, so the entry-level screen is where signalling does its heaviest '
      'work and where its failure has the largest consequences.'),

('p', 'Not all screens are signals in this sense. A proctored assessment is a screen whose '
      'result the applicant cannot costlessly manufacture; a university’s selectivity is a '
      'proxy the applicant did not produce at all and which correlates strongly with '
      'parental resources {{ivy_plus}}. The distinction matters because the two behave '
      'differently when the written application fails. Evidence that verified skill '
      'information changes employer behaviour is strong: giving South African workseekers '
      'credibly shareable assessment results raised employment and earnings and shifted '
      'interview decisions {{limited_information}}; publicly posting evaluations of '
      'inexperienced online workers substantially raised their later employment '
      '{{inefficient_entry}}; and adding a former-employer reference letter raised '
      'callbacks by 60% {{reference_letters}}. What these interventions share is that they '
      'introduce information the applicant cannot cheaply fabricate.'),

('p', 'Two features of the entry-level screen make it the decisive margin. First, the '
      'demand side is moving: artificial intelligence is reshaping the skill premium and '
      'the composition of tasks firms buy {{sbtc1|career2}}, digital transformation is '
      'changing the structure as well as the level of firms’ labour demand '
      '{{digital_emp1|digitrans_emp_firm|im_hc}}, and career research now treats the '
      'sequence of early career stages as itself being reorganised by AI {{career1}}. '
      'Second, automation reduces employer-provided training for exactly the workers most '
      'exposed to it {{training1}}, so the entry screen is being asked to carry more '
      'weight at the same time as it is becoming less informative. For young people the '
      'stakes are correspondingly high: entry difficulties in China show up as persistent '
      'overeducation and mismatch {{mismatch1}}, and the quality of early digital-economy '
      'jobs varies sharply across entrants {{china_youth2}}.'),

('h2', '2.2. What Generative AI Does to the Written Application'),

('p', 'Generative models compress the cost of producing a fluent, tailored, error-free '
      'application to approximately zero, and they compress it for everyone; controlled '
      'experiments on exactly this class of writing task show large gains concentrated among '
      'previously weaker writers, which is compression of the distribution rather than a '
      'uniform shift {{genai2|genai3}}. Formally, the '
      'single-crossing condition that makes the written application informative no longer '
      'holds; substantively, the distribution of application quality shifts up and '
      'compresses, so its variance—the part employers actually use—collapses. The '
      'empirical record now supports this directly. On a large freelancing platform the '
      'predictive value of cover-letter fit halved after an AI writing tool was introduced, '
      'and employers moved weight onto histories and ratings {{cover_letters_ai}}; a '
      'structural treatment of the same market finds employers’ willingness to pay for '
      'tailoring disappearing entirely {{making_talk_cheap}}; on the same class of '
      'platform, demand for exactly the writing and coding tasks that generative models '
      'perform well fell by about a fifth {{who_is_ai_replacing}}. Applicant-side surveys confirm '
      'that use is real and rising, though self-reported incidence remains below what '
      'employers assume {{applicant_ai_use}}—a gap that matters, because it is employers’ '
      'beliefs, not the true rate, that drive their screening response.'),

('p', 'Two further effects compound the problem. Applications become cheaper to send as '
      'well as to write, so volume rises and attention per application falls; when '
      'attention is scarce and costly, employers lean harder on priors, which magnifies '
      'the role of group-level characteristics {{attention_discrimination}}. And when '
      'employers respond by automating the first cut, the automated screener inherits the '
      'degraded text and adds distortions of its own, including a measurable preference for '
      'résumés generated by the same model family {{ai_self_preferencing}} and demographic '
      'skews inherited from training data {{resume_lm_bias}}. Algorithmic screening is not '
      'inherently worse than human screening—well-designed algorithms can improve both '
      'quality and diversity when they are built to explore rather than to imitate past '
      'hiring {{hiring_exploration}}, and human overrides of job tests often make hires '
      'worse {{discretion_hiring}}—but a meta-analysis of human–machine combinations finds '
      'that they outperform the better of their parts only under narrow conditions '
      '{{human_ai_meta}}, and an algorithm applied to a signal that no longer '
      'informs cannot recover information that is not there.'),

('h2', '2.3. Three Responses, Three Architectures'),

('p', 'Faced with a signal that has stopped working, the screening function can be '
      'reorganised in three ways, and these correspond to the three architectures we '
      'manipulate experimentally. The first is retreat to ascriptive signals: rank on '
      'institutional selectivity and referral. This is cheap, defensible inside the '
      'organisation, and weakly related to entry-level productivity; it is also the route '
      'through which elite professional firms have long reproduced social closure, and '
      'correspondence experiments show such screening gaps to be remarkably stable over '
      'decades {{quillian17|lippens23|cultural_matching|class_advantage}}, and it transfers the cost of the signalling '
      'failure onto applicants without elite credentials or networks. The second is triage: '
      'let an automated score order the pile and cut deep. This addresses volume but not '
      'informativeness. The third is restoration: require something costly to fake. A '
      'proctored assessment does this directly. So, we argue, does a process-evidence '
      'portfolio—drafts, revision history and reasoning notes—because a generative model '
      'can produce a polished output cheaply but cannot cheaply produce a credible record '
      'of a particular applicant’s own iterative reasoning about a specific problem. '
      'Process evidence restores the cost asymmetry at the level of the work, not the '
      'level of the credential.'),

('h2', '2.4. The Disclosure Trap'),

('p', 'Whether applicants disclose AI use is itself endogenous to how employers treat '
      'disclosure. If disclosure is penalised, applicants conceal; concealment makes the '
      'written signal less interpretable still, which accelerates the retreat to ascriptive '
      'signals. Figure 1 sets out this structure. The loop is closed by employer belief: '
      'the more AI-assisted applications a manager believes she is receiving, the more she '
      'discounts the written material, and the more the remaining weight moves to '
      'institution and referral. The escape from this loop is not to punish disclosure '
      'harder, which is unenforceable, but to make disclosure informative by pairing it '
      'with evidence. That is the empirical question this paper is built to answer.'),

('figure', 'p8_fig1.png', 5.45, None, 101),
('figcap', 1, 'Signal collapse and the three employer responses. Generative AI drives the '
              'cost of producing a polished written application towards zero, which '
              'removes the cost asymmetry a signal needs. Employers can retreat to '
              'ascriptive signals, triage on volume, or restore a costly signal. The '
              'dashed link is the disclosure trap: penalising disclosure induces '
              'concealment, which degrades the written signal further.'),

('h2', '2.5. Screening Architecture as a Leadership Decision'),

('p', 'The organisational literature treats digital transformation as a redesign of how '
      'work and decisions are structured rather than as technology adoption '
      '{{hanelt21|braojos24}}. Screening architecture is a clean instance. The choice of '
      'what an applicant-tracking interface puts first, what it computes automatically, and '
      'what it requires a human to read is made by leadership, is rarely revisited, and is '
      'invisible to the managers who operate inside it. Research on AI-assisted managerial '
      'decision making has concentrated on whether machine advice improves the quality of a '
      'given decision {{aidm1|csaszar_ai|systems_ai_dm}}, and practical guidance for '
      'digital leaders is framed around adoption choices {{ddm2}}; the prior question of '
      'which decisions the interface presents, and in what order, has received far less '
      'attention. If that choice moves outcomes more '
      'than the preferences of the individual screeners do, then the leverage in this '
      'system lies with the people who configure the funnel rather than with the people who '
      'work it—which reframes a fairness problem usually posed in terms of individual bias '
      'as a problem of system design.'),

('h2', '2.6. Hypotheses'),

('p', 'The argument yields six testable propositions. The first three concern the decision '
      'rule, the next two its heterogeneity, and the last the architecture.'),

('hyp', 'Hypothesis 1 (disclosure penalty).',
        'Other things equal, an application that discloses the use of generative-AI '
        'assistance is less likely to be shortlisted than one that makes no such statement.'),

('hyp', 'Hypothesis 2 (evidence repair).',
        'A process-evidence portfolio attenuates the disclosure penalty; that is, the '
        'interaction between disclosure and process evidence is positive, so disclosure is '
        'penalised substantially less when the applicant can document how the work was '
        'produced.'),

('hyp', 'Hypothesis 3 (verification premium).',
        'Verified proctored assessment results carry a positive and monotone premium, and '
        'the premium attached to a high assessment result is at least as large as the '
        'premium attached to an elite institution.'),

('hyp', 'Hypothesis 4 (discrete regimes).',
        'Employer preferences are discretely rather than continuously heterogeneous: a '
        'small number of interpretable screening regimes fit the choice data better than a '
        'single average rule and predict held-out choices more accurately.'),

('hyp', 'Hypothesis 5 (retreat under signal collapse).',
        'Managers who perceive a larger share of their applications to be AI-assisted, and '
        'who face faster growth in application volume, are more likely to belong to the '
        'regime that weights ascriptive credentials most heavily.'),

('hyp', 'Hypothesis 6 (architecture dominates).',
        'The screening architecture causally changes the composition of the shortlist: an '
        'evidence-first ordering raises the share of shortlisted candidates from non-elite '
        'institutions relative to a credential-first ordering, and does so without reducing '
        'the measured assessment quality of the shortlist.'),

# ================================================ 3. Materials and Methods
('h1', '3. Materials and Methods'),

('h2', '3.1. Design Overview'),

('p', 'The study combines two experiments in a single instrument administered to the same '
      'respondents. Study 1 is a choice-based conjoint experiment that identifies the '
      'weights employers place on entry-level applicant attributes, including the two that '
      'the theory makes central—disclosure of AI assistance and process evidence. Stated '
      'choice is the appropriate instrument here because the attributes of interest are '
      'not yet widely observed in field data: process-evidence portfolios are rare, and '
      'explicit AI disclosure is rarer still, so no observational design could recover '
      'their weights. Study 2 is a randomised between-subjects experiment on the screening '
      'architecture, which identifies the causal effect of a design decision that '
      'organisations do make but almost never vary deliberately. The two are complementary: '
      'the conjoint measures preferences holding the interface fixed, and the randomisation '
      'measures the interface holding preferences fixed by design.'),

('p', 'Conjoint experiments are the established method for eliciting employer preferences '
      'without deceiving real applicants {{irr}}, and their causal interpretation under '
      'randomised attribute assignment is well understood {{hainmueller14}}. Choice-based '
      'conjoint has been used specifically with recruiters in pre-employment screening '
      '{{cbc_recruiters}} and with employers recruiting recent graduates '
      '{{cbc_graduates}}, which establishes both feasibility and comparability. We follow '
      'the ISPOR good-practice guidance for design construction and for analysis '
      '{{ispor_design|ispor_analysis}}.'),

('h2', '3.2. Participants and Procedure'),

('p', 'The sampling frame comprised knowledge-intensive service firms with at least twenty '
      'employees in the Yangtze River Delta city cluster (Shanghai, Jiangsu, Zhejiang and '
      'Anhui), which concentrates a large share of China’s software, professional-services '
      'and shared-service employment. Because the constructs are firm-level decision rules '
      'rather than individual attitudes, we applied key-informant selection criteria and '
      'recruited the person who actually decides entry-level shortlists—an HR manager, a '
      'hiring manager or a department head—verifying involvement with two screening '
      'questions before entry {{key_informants}}. Firms were drawn by stratified random '
      'sampling from municipal enterprise registers, stratified by sector and size band. '
      'Data were collected between March and June 2026.'),

('p', 'Respondents first answered questions about their firm and their screening context, '
      'then completed the conjoint tasks, then completed the randomised architecture task, '
      'and finally answered demographic items. Two instructed-response items and one '
      'comprehension item were embedded, and we treated failure of more than one as '
      'grounds for exclusion; we report the exclusion count rather than silently dropping '
      'cases, since screening out inattentive respondents can itself introduce selection '
      '{{attention_checks|panel_quality}}. Of 612 invitations, 496 people entered the '
      'instrument, 44 were excluded for failed attention or comprehension checks or for '
      'implausibly fast completion, leaving 452 usable respondents. The conjoint yielded '
      '6328 choice sets and 12,656 profile evaluations.'),

('p', 'The study was approved by the Academic Ethics Committee of the College of Business, '
      'Jiaxing University. Participation was voluntary and respondents gave informed '
      'consent. Because the hypothetical candidates were fictitious and no real applicant '
      'was affected, the design avoids the ethical objection to correspondence studies, '
      'which impose costs on real employers {{irr}}. All analyses were conducted in Python '
      '3.11 with NumPy and SciPy; the estimation, the design construction and the figures '
      'run from a single seeded pipeline, so every number reported below is generated by '
      'the code rather than transcribed.'),

('h2', '3.3. Study 1: The Choice Experiment'),

('h3', '3.3.1. Attributes and Levels'),

('p', 'Each task presented two hypothetical applicants for a defined entry-level analyst '
      'position and an explicit opt-out (“neither of these two”), which prevents forced '
      'choice from inflating the apparent attractiveness of weak profiles. To keep the '
      'scenario concrete, respondents were told to assume a real vacancy of the kind their '
      'firm fills, a practice that improves the realism of factorial designs '
      '{{gutfleisch21}}. Table 1 lists the seven attributes and their levels. The two '
      'focal attributes are the disclosure of AI assistance and the presence of a '
      'process-evidence portfolio, defined for respondents as “drafts, revision history and '
      'the applicant’s own notes on how the work was developed”. Expected monthly salary '
      'was included as a numeraire so that every other attribute can be expressed as a '
      'compensating differential in money {{train_weeks}}. Figure 2 reproduces an example '
      'task as respondents saw it.'),

('tabcap', 1, 'Attributes and levels of the choice experiment.'),
('table', [
    ['Attribute', 'Levels', 'Rationale and source'],
    ['Disclosure of AI assistance',
     ['No statement (reference)', 'Application states that generative-AI assistance was used'],
     'Focal attribute; disclosure incidence and employer response are both rising '
     '{{applicant_ai_use}}'],
    ['Process-evidence portfolio',
     ['None (reference)', 'Drafts, revision history and reasoning notes'],
     'Focal attribute; restores a cost asymmetry a model cannot cheaply imitate'],
    ['Verified proctored assessment',
     ['Not taken (reference)', '70th percentile', '90th percentile'],
     'Verified skill information changes hiring behaviour {{limited_information|inefficient_entry}}'],
    ['Institution tier', ['Non-elite (reference)', 'Elite (“Double First-Class”)'],
     'Ascriptive signal correlated with family background {{ivy_plus|class_advantage}}'],
    ['Employee referral', ['None (reference)', 'Referred by a current employee'],
     'Referrals predict retention and performance {{referral_value}}'],
    ['Relevant internship', ['None (reference)', 'Six months, relevant'],
     'Standard entry-level experience signal {{skill_requirements}}'],
    ['Expected monthly salary', ['8000 CNY', '10,000 CNY', '12,000 CNY'],
     'Numeraire for compensating differentials {{train_weeks}}'],
 ], [2180, 3060, 4400]),
('notes', 'Levels marked “reference” are the omitted category in the dummy coding. The '
          'disclosure and process-evidence attributes are crossed, so the interaction in '
          'Equation (2) is identified by design.'),

('figure', 'p8_fig2.png', 5.30, None, 102),
('figcap', 2, 'An example choice task as presented to respondents. Attribute order was '
              'randomised across respondents and the left–right position of the two '
              'candidates was rotated, so neither ordering nor position can be confounded '
              'with an attribute level.'),

('h3', '3.3.2. Experimental Design'),

('p', 'The full factorial contains 288 profiles. From it we constructed a D-efficient '
      'paired design by evaluating the multinomial-logit D-error at null priors over a '
      'large number of candidate designs and retaining the best, subject to a '
      'minimum-overlap constraint requiring the two profiles in a task to differ on at '
      'least four attributes {{rose_bliemer}}. The retained design has a D-error of 0.570 '
      'and attribute-level balance within one occurrence across the design. Each respondent '
      'completed 14 tasks, which is within the range over which conjoint response quality '
      'is stable and satisficing does not materially degrade estimates {{bansak18}}. '
      'Respondents were assigned at random to one of eight blocks, each a rotation of the '
      'task order with the within-task profile positions alternated.'),

('h3', '3.3.3. Choice Models'),

('p', 'Let respondent ⟪n⟫ face choice set ⟪s⟫ containing alternatives ⟪j⟫. Under random '
      'utility maximisation the utility of an alternative is the sum of a systematic and '
      'an independently and identically distributed extreme-value component, as in '
      'Equation (1):'),

('eq', 'eq1', 1),

('p', 'The systematic component is specified in Equation (2), where ⟪AI⟫ and ⟪PE⟫ are the '
      'two focal indicators, ⟪q⟫ collects the assessment, institution, referral and '
      'internship indicators, and salary enters centred at its middle level so that the '
      'opt-out constant is interpretable:'),

('eq', 'eq2', 2),

('p', 'With extreme-value errors the choice probability takes the familiar conditional '
      'logit form of Equation (3), which we estimate first as a homogeneous benchmark with '
      'standard errors clustered by respondent:'),

('eq', 'eq3', 3),

('p', 'Because a homogeneous rule is implausible and because the conditional logit imposes '
      'independence from irrelevant alternatives, we then estimate a mixed logit in which '
      'every coefficient, including the opt-out constant, is an independent normal random '
      'parameter. The mixed logit can approximate any random-utility-consistent choice '
      'model arbitrarily closely {{mcfadden_train}}, and the probability of a respondent’s '
      'observed sequence of choices is the integral in Equation (4):'),

('eq', 'eq4', 4),

('p', 'The integral has no closed form and is approximated by simulation. We use 500 '
      'scrambled Halton draws, which achieve lower simulation variance than an equivalent '
      'number of pseudo-random draws {{train09}}, and maximise the simulated log-likelihood '
      'of Equation (5) with analytic gradients:'),

('eq', 'eq5', 5),

('p', 'Standard errors are the sandwich estimator formed from the outer product of the '
      'respondent-level score contributions and the numerically differentiated Hessian. '
      'Because salary enters the utility function, any attribute coefficient can be '
      'expressed as a compensating differential by Equation (6), with standard errors '
      'obtained by the delta method:'),

('eq', 'eq6', 6),

('p', 'The two quantities that test Hypotheses 1 and 2 are the disclosure penalty when no '
      'process evidence is offered and the penalty when it is, given in Equation (7); the '
      'standard error of the second combines the variances and the covariance of the two '
      'coefficients:'),

('eq', 'eq7', 7),

('h3', '3.3.4. Latent-Class Model'),

('p', 'A continuous mixing distribution assumes that employers differ by degree. The '
      'competing possibility—that they differ in kind, following a small number of distinct '
      'screening regimes—is represented by a latent-class conditional logit, in which the '
      'population is a finite mixture over class-specific coefficient vectors, as in '
      'Equation (8) {{greene_hensher}}:'),

('eq', 'eq8', 8),

('p', 'We estimate the model by the expectation–maximisation algorithm for two to five '
      'classes and select the number of classes by the Bayesian information criterion, '
      'which performs well relative to alternatives in simulation studies of finite '
      'mixtures {{nylund07}}, reporting the consistent AIC alongside it. Class separation '
      'is summarised by the entropy criterion of Equation (10), where ⟪h⟫ denotes the '
      'posterior probability that respondent ⟪n⟫ belongs to class ⟪c⟫. Because class labels '
      'are identified only up to a permutation, we order classes by their institution '
      'coefficient before reporting.'),

('p', 'To ask which employers screen which way, we then relate posterior class membership '
      'to firm characteristics through the multinomial specification of Equation (9), '
      'estimated on the posterior probabilities rather than on hard assignments so that '
      'classification uncertainty is carried into the second stage:'),

('eq', 'eq9', 9),
('eq', 'eq10', 10),

('p', 'The covariates are the depth of digital transformation of the hiring function, the '
      'share of applications the respondent believes to be AI-assisted, growth in '
      'application volume, centralisation of the screening decision, firm size and '
      'respondent experience, all standardised. Predictive validity is assessed by '
      'estimating every model on the first nine tasks and predicting the last five, with '
      'the mixed-logit and latent-class predictions formed from each respondent’s posterior '
      'distribution over tastes given their training choices rather than from the '
      'population distribution.'),

('h2', '3.4. Study 2: The Randomised Architecture Experiment'),

('p', 'After the conjoint, each respondent was shown a fixed pool of twenty entry-level '
      'candidate profiles and asked to select a shortlist of five. Respondents were '
      'randomly assigned in equal proportions to one of three interfaces, which differed '
      'only in what was displayed first and how the pool was pre-ordered: an AI-score-first '
      'interface, which pre-ranked candidates by an automated screening score; a '
      'credential-first interface, which pre-ranked by institution and grade; and an '
      'evidence-first interface, which pre-ranked by verified assessment result and the '
      'presence of process evidence. The underlying candidate pool was identical across '
      'arms, so any difference in the resulting shortlist is caused by the architecture.'),

('p', 'Three outcomes were recorded: the share of the five-person shortlist drawn from '
      'non-elite institutions, which is the access outcome; the mean verified-assessment '
      'percentile of the shortlist, which is the quality outcome; and the time spent per '
      'applicant, which is the cost outcome. Arm differences are tested by one-way analysis '
      'of variance with the Alexander–Govern correction for unequal variances and by '
      'pairwise Welch tests with Bonferroni adjustment, reporting eta-squared and Cohen’s '
      'd. Because assignment is randomised, the unadjusted comparison is unbiased; we also '
      'report the covariate-adjusted specification of Equation (11) as a precision check:'),

('eq', 'eq11', 11),
]
