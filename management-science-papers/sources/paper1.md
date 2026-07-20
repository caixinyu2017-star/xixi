# Generative AI and the Productivity of Knowledge Workers: Evidence from a Large-Scale Field Experiment

[Author names and affiliations blinded for peer review]

**Abstract.** Firms are deploying generative artificial intelligence assistants across knowledge work faster than causal evidence on their effects can accumulate, so deployment decisions typically rest on laboratory tasks or single-occupation studies that miss quality risks and distributional consequences. We conduct a preregistered 24-week randomized field experiment with 1,842 consultants at a global professional services firm, randomizing access to a large language model assistant integrated into everyday work tools and tracking 58,674 real client tasks. Access reduces task completion time by 24.3% and raises output quality by 0.28 standard deviations, with gains concentrated among bottom-quartile workers (35.1% faster; quality up 0.47 standard deviations), narrowing the 90/10 quality gap across workers by 28.4%. However, on the 8.5% of tasks beyond the assistant's competence frontier, treated workers' accuracy falls 14.8 percentage points, and losses concentrate among workers who verify least. Our results position task-based deployment and verification training, rather than uniform rollout, as the central managerial levers for capturing value from generative artificial intelligence.

**Keywords:** generative artificial intelligence • field experiment • knowledge worker productivity • human–AI collaboration • skill heterogeneity

# 1. Introduction

Generative artificial intelligence (AI) built on large language models (LLMs) is diffusing through knowledge-intensive organizations at a pace few general purpose technologies have matched. Within two years of the public release of GPT-4-class models, a majority of large professional services, legal, and financial firms report piloting or deploying LLM assistants for drafting, analysis, and research work, and occupational exposure estimates suggest that most knowledge-work tasks are at least partially exposed to LLM capabilities (Eloundou et al. 2024, Felten et al. 2021). For the managers making these deployment decisions, the stakes are considerable: professional services alone represent a multi-trillion-dollar global industry whose production function consists almost entirely of the tasks—writing, synthesizing, analyzing—that LLMs putatively accelerate. Yet the same properties that make generative AI attractive make it risky. LLMs produce fluent output whose errors are difficult to detect, raising the possibility that speed gains arrive bundled with quality losses that surface only later, in client relationships and rework. Deciding where to deploy AI assistance, how to train workers to use it, and how to redesign quality assurance requires causal evidence from real professional work, and such evidence remains scarce. The gap matters for policy as well as for firms: if generative AI compresses performance differences across workers, it reshapes the returns to skill and the design of professional careers; if it degrades quality on a predictable subset of tasks, it creates a new category of operational risk that neither existing quality-assurance systems nor existing regulation anticipates.

The existing evidence base, although rapidly growing, has three limitations. First, much of it is laboratory or platform evidence on stylized tasks: Noy and Zhang (2023) randomize ChatGPT access for standalone writing tasks completed by online participants, and Boussioux et al. (2024) and Doshi and Hauser (2024) study creative ideation in controlled settings. Second, the field evidence that exists covers single, relatively structured occupations—customer support agents in Brynjolfsson et al. (2025), software developers in Peng et al. (2023)—whose task content differs from the multi-domain, judgment-intensive work of most professionals. Third, the closest antecedent to our setting, Dell'Acqua et al. (2023), studies consultants but uses researcher-assigned tasks completed in a single session, which precludes observing learning dynamics, real client stakes, and the equilibrium of delegation and verification behavior that emerges when workers use an assistant daily for months. What managers need—and what the literature lacks—is field-experimental evidence from real, billable, multi-domain professional work over a horizon long enough to observe how effects evolve, how they are distributed across workers, and where AI assistance backfires.

In this paper, we conduct a preregistered randomized field experiment inside a global professional services firm to provide that evidence. Working with the firm across 14 offices in nine countries, we randomly assign 921 of $N = 1{,}842$ associate- and manager-level consultants to receive access to a GPT-4-class LLM assistant integrated into the firm's document, spreadsheet, and research tools, whereas the remaining 921 continue with status quo tools. The experiment runs for 24 weeks, from September 2024 to February 2025, and covers 58,674 real client tasks spanning drafting, data analysis, slide production, research memos, and quality reviews. We measure task completion time from telemetry, output quality from double-blind grading by senior partners on a stratified subsample of 12,300 tasks (extended to the full sample with a validated automated rubric), weekly throughput, and client revision requests. Crucially, before launch we work with the firm's methodology committee to classify task types ex ante into those "inside the frontier" of AI capability (91.5% of tasks) and those "beyond the frontier" (8.5%)—tasks requiring firm-specific tacit knowledge, confidential client context, or data unavailable to the model—following the jagged-frontier idea of Dell'Acqua et al. (2023). A three-wave worker survey and verification telemetry let us open the black box of how workers delegate to and check the assistant. Compliance is high (94.3% of treated workers activate the assistant in the first week), attrition is low and balanced (4.1% versus 4.5%), and the outcome infrastructure—telemetry-based time measurement, double-blind partner grading, and client-generated revision records—means that neither self-reports nor researcher-constructed tasks stand between the treatment and the outcomes we analyze.

Our results are fourfold. First, access to the assistant generates large average productivity gains on real client work: task completion time falls by 24.3% (a log-time coefficient of $-0.278$, standard error 0.021), output quality rises by 3.9 points on a 0–100 scale (0.28 standard deviations), weekly task throughput rises by 16.4%, and client revision requests per task fall by 18.7%. Second, the gains are strongly skill-biased—toward the bottom. Workers in the lowest baseline skill quartile complete tasks 35.1% faster with quality gains of 0.47 standard deviations, whereas top-quartile workers save only 11.2% of time with quality gains that are statistically indistinguishable from zero. Quantile treatment effects on quality are +6.8 points at the 10th percentile but +0.7 points (insignificant) at the 90th; the 90/10 quality gap across workers narrows by 28.4%, and within-worker quality variability falls by 19.6%. Generative AI, in this setting, is an equalizing technology. Third, effects build gradually: the treatment effect on log completion time grows from $-0.09$ in week 1 to $-0.31$ by week 10 and then remains on a stable plateau of $-0.31 \pm 0.02$ through week 24, a persistence pattern consistent with the accumulation of complementary "prompting and delegation capital" rather than novelty effects. Fourth, the gains have a sharp boundary. On beyond-frontier tasks, treated workers' accuracy is 56.4% against a control mean of 71.2%—a 14.8-percentage-point deficit—and the damage concentrates among workers whom telemetry identifies as verifying least (a 23.6-percentage-point accuracy loss in the bottom verification tercile versus an insignificant 4.2-point loss in the top tercile).

Our contributions to the literature manifest across three dimensions. First, we provide the first large-scale, long-horizon field-experimental evidence on generative AI from real, multi-domain professional work, complementing task-level laboratory evidence (Noy and Zhang 2023) and single-occupation deployments (Peng et al. 2023, Brynjolfsson et al. 2025) with estimates that carry direct external validity for the knowledge-intensive firms now making deployment decisions. Second, we characterize the distributional consequences of generative AI within the firm using quantile treatment effects and within-worker variance decompositions, documenting skill compression that speaks to long-standing questions about technology and the returns to skill (Autor et al. 2003, Acemoglu and Restrepo 2018) and to the practical question of how AI reshapes talent management in professional hierarchies (Garicano 2000). Third, we convert the jagged-frontier metaphor into a measurable and manageable object: by pre-classifying tasks ex ante and measuring verification behavior objectively, we show that beyond-frontier quality losses are large, predictable, and moderated by verification effort, which yields concrete task-allocation, training, and quality-assurance policies.

Conceptually, our findings discipline how one should think about generative AI as a technology of production. The pattern of large average gains, bottom-skewed heterogeneity, gradual buildup, and boundary failures is precisely what theories of general purpose technologies and codified expertise predict: the assistant behaves like an instantly accessible layer of codified knowledge that substitutes for experience inside its competence set (Garicano 2000, Autor 2015), requires complementary intangible investment before its returns are realized (Bresnahan and Trajtenberg 1995, Brynjolfsson et al. 2021), and interacts with well-documented miscalibration in human reliance on algorithms at its boundary (Dietvorst et al. 2015, Logg et al. 2019). This mapping matters because it makes the results portable: managers in other knowledge-intensive settings cannot transplant our point estimates, but they can transplant the structure—expect gains proportional to the codifiable share of their performance gaps, expect a ramp-up measured in months rather than days, and expect quality risk concentrated where their tasks depend on information the model cannot see. We emphasize that our mechanism evidence on trust and verification is correlational rather than causal, whereas the treatment effects themselves are experimentally identified.

The remainder of the paper proceeds as follows. Section 2 overviews the related literature and develops the rationale for our design. Section 3 describes the experimental setting, randomization, and data, whereas Section 4 details the empirical framework. The main results are presented in Section 5, followed by the frontier analysis in Section 6. Section 7 examines mechanisms, reports the robustness battery, and develops managerial implications. Section 8 concludes. Supplementary materials, including the preregistration documents, grading rubrics, and additional robustness tables, are available in the Online Appendix.

# 2. Related Literature and Hypotheses

## 2.1. Generative AI and Worker Productivity

A first stream of work estimates the productivity effects of generative AI directly. Noy and Zhang (2023) show in an online experiment that ChatGPT access reduces the time college-educated professionals spend on incentivized writing tasks by about 40% and raises output quality, with larger quality gains for initially weaker writers. Peng et al. (2023) find that GitHub Copilot access allows developers to complete a standardized programming task 55.8% faster. In the field, Brynjolfsson et al. (2025) study the staggered rollout of a generative AI conversational assistant to customer support agents and document a 15% average increase in issues resolved per hour, with gains concentrated among novice and low-skill agents. Dell'Acqua et al. (2023) randomize GPT-4 access among consultants completing researcher-designed tasks in a single session and report quality gains of roughly 40% on tasks inside the model's capability frontier but a 19-percentage-point decline in the probability of a correct solution on a task designed to sit beyond it. Related work examines creative rather than analytical output: Boussioux et al. (2024) find that human–AI collaborative solutions to a crowdsourced innovation challenge match crowd solutions in quality while being produced far faster, Doshi and Hauser (2024) show that AI assistance raises individual story quality but reduces collective diversity, and Jia et al. (2024) provide field evidence that AI assistance augments employee creativity primarily for workers with higher AI literacy. At the level of occupations and labor markets, Eloundou et al. (2024) and Felten et al. (2021) measure exposure rather than realized effects, underscoring the need for causal field estimates.

Our reading of this literature is that it establishes proof of concept but leaves the managerially decisive questions open. Laboratory tasks abstract from client stakes, organizational context, and the repeated-use horizon over which workers learn to delegate; single-occupation deployments cover structured work with fast feedback loops, unlike the multi-domain, judgment-intensive tasks of most professionals; and one-session designs cannot distinguish novelty effects from durable productivity change, nor can they observe the verification habits that determine outcomes at the capability frontier. Wang et al. (2024) show in the context of medical chart review that the value of human–AI teaming varies sharply with worker experience, which further cautions against extrapolating single-setting estimates. Our design addresses each gap directly: tasks are real and billable rather than assigned; the occupation spans drafting, analysis, slide production, research, and review rather than a single activity; the 24-week horizon spans the learning curve; and preregistered heterogeneity and frontier analyses let us estimate not only whether generative AI raises productivity but for whom, when, and where it fails.

## 2.2. Human–Algorithm Collaboration, Aversion, and Overreliance

A second stream examines how people use algorithmic advice. Dietvorst et al. (2015) document algorithm aversion—the tendency to abandon algorithms after seeing them err—whereas Logg et al. (2019) document algorithm appreciation in settings where advice sources are unfamiliar. Dietvorst et al. (2018) show that modest control over an algorithm's output restores willingness to use it. In operational settings, Fügener et al. (2022) find that humans delegate poorly to AI because they misjudge the boundary between their own capabilities and the machine's, and Kleinberg et al. (2018) show that machine predictions can improve on expert judgment but that realized gains depend on how discretion is exercised around the algorithm. Customer- and employee-facing deployments echo this contingency: Luo et al. (2019) show that chatbot effectiveness collapses upon disclosure, and Tong et al. (2021) find that AI-generated feedback improves employee performance only when its source is undisclosed. Agrawal et al. (2018) provide the organizing economics: machine prediction is cheap, but the complements—judgment about when to rely on it—are scarce and slow to build.

Generative AI sharpens these concerns because its failure mode is fluent, confident, plausible error. Whereas a classical decision-support tool produces predictions whose provenance is legible, an LLM produces finished professional prose whose errors mimic competence. The behavioral literature therefore predicts that the binding constraint on value creation is calibration: workers must learn task-by-task whether to delegate, and miscalibrated trust—especially the appreciation documented by Logg et al. (2019)—should generate quality losses precisely where the model is weak and the worker cannot easily tell. Our design measures this channel directly, with ex ante frontier classification, telemetry-based verification measures, and survey-based trust measures.

## 2.3. Technology, Skills, and the Organization of Knowledge Work

A third stream studies how technology reshapes the task content of work and the returns to skill. Autor et al. (2003) establish that computerization substitutes for routine tasks and complements nonroutine analytical work; Autor (2015) emphasizes that automation's aggregate effects depend on the balance between substitution and the creation of new complementary tasks; and Acemoglu and Restrepo (2018) model the race between automation and the creation of labor-intensive tasks. Generative AI complicates the routine/nonroutine dichotomy because it performs nonroutine cognitive work—drafting, summarizing, first-pass analysis—that was previously the training ground of junior professionals. Garicano (2000) provides a lens we use throughout: knowledge hierarchies exist to economize on expertise, matching hard problems to experts; an LLM assistant is, in effect, a new bottom layer of the hierarchy whose knowledge is broad but shallow, which should compress performance differences among workers whose gaps reflect codifiable knowledge rather than judgment. Finally, the general purpose technology (GPT) literature (Bresnahan and Trajtenberg 1995) and its modern intangibles formulation (Brynjolfsson et al. 2021) predict that realized productivity gains require complementary co-invention—here, prompting skill, delegation norms, and verification routines—implying gradual effect dynamics rather than a step function at deployment.

Two implications of this stream shape our design. First, if the assistant's contribution is a shallow-but-broad knowledge layer, then its effects should be largest for workers whose performance gap relative to their best colleagues consists of codifiable knowledge—exactly the prediction we test with skill-quartile interactions and QTEs. Second, if realized gains require co-invented complements, then the *time path* of effects is itself evidence about mechanism: an instantaneous, decaying effect indicates novelty, whereas a gradual, persistent one indicates capital accumulation. Our event-study design is built to distinguish the two.

Methodologically, we build on the tradition of randomized and natural experiments inside firms, including Bandiera et al. (2007) on managerial incentives, Bloom et al. (2015) on remote work, Choudhury et al. (2021) on geographic flexibility, and Hoffman et al. (2018) on discretion in hiring, which demonstrate that within-firm experimentation can credibly identify the productivity consequences of organizational and technological choices. Relative to this tradition, our contribution is to combine worker-level randomization with task-level telemetry and blinded output grading, which allows us to decompose a technology's effect on the production function—time, quality, throughput, and rework—rather than observing only an aggregate performance metric.

## 2.4. Rationale and Expectations

The design of our experiment follows from this synthesis. We present four main reasons to expect the pattern of effects we test for: (i) the task content of consulting—drafting, synthesis, structured analysis—overlaps heavily with measured LLM capabilities, so average completion-time and throughput gains should be large on tasks inside the frontier (Eloundou et al. 2024, Noy and Zhang 2023); (ii) because the assistant functions as instantly accessible codified expertise, it should substitute most strongly for the experience and knowledge that separate low-skill from high-skill workers, generating gains that decline in baseline skill and compressing the performance distribution (Garicano 2000, Brynjolfsson et al. 2025); (iii) because the assistant's failures are fluent and hard to detect, miscalibrated reliance should produce quality losses on beyond-frontier tasks, concentrated among workers who verify least (Fügener et al. 2022, Logg et al. 2019); and (iv) because value creation requires complementary co-invention of delegation and verification skills, treatment effects should build over weeks and then persist, rather than spiking at launch and fading (Bresnahan and Trajtenberg 1995, Brynjolfsson et al. 2021). These four expectations, formalized in our preregistration (Online Appendix A), correspond to the analyses in Sections 5.1, 5.2–5.3, 6, and 5.4, respectively.

# 3. Experimental Design and Data

## 3.1. Setting

Our research collaboration is with a global professional services firm (anonymized per the data-use agreement) that provides strategy, operations, and financial advisory services to corporate clients. The experiment covers 14 offices in nine countries and the full population of associate- and manager-level consultants in those offices—$N = 1{,}842$ workers—who perform the firm's core billable production: drafting client documents, analyzing data, producing slide decks, writing research memos, and reviewing the work of others. These workers bill by the engagement, work in small teams under partners, and are evaluated semiannually on output quality and utilization. The setting is attractive for three reasons. First, the work is real and consequential: every task in our data is billable client work, not a researcher-designed exercise. Second, the firm's workflow and telemetry systems measure inputs and outputs at the task level with unusual fidelity. Third, the occupation sits near the center of the LLM exposure distribution (Eloundou et al. 2024), so estimates from this setting inform deployment decisions across a wide swath of knowledge work.

The collaboration is governed by a data-use agreement that anonymizes the firm and its clients and by approval from our institutions' review boards; workers consent to research use of telemetry under the firm's standing analytics policy, and the survey carries separate informed consent.[^1] The firm's motivation for experimenting—rather than simply deploying—is instructive: leadership was divided between advocates projecting large efficiency gains and skeptics warning of quality risk on confidential client work, and the two camps agreed that only randomized evidence could settle deployment policy. This equipoise also means the firm imposed no pressure toward a particular finding.

[^1]: The agreement specifies that the firm may review the manuscript solely to verify anonymization, with no right to alter results. No author has a financial relationship with the firm or with any AI vendor.

## 3.2. Randomization and Treatment

We preregistered the design, outcomes, and heterogeneity analyses before launch; the preregistration and a CONSORT-style flow diagram appear in Online Appendix A. Randomization is stratified by office and within-office baseline tenure quartile (56 strata), assigning 921 workers to treatment and 921 to control. Treated workers receive access to a GPT-4-class LLM assistant integrated directly into the firm's document editor, spreadsheet environment, and internal research portal. The assistant supports drafting and rewriting, summarization of documents and data, first-pass quantitative analysis, and retrieval-augmented search over public sources; it does not have access to the firm's confidential engagement archives. The integration is deliberately naturalistic: rather than a separate chat window, the assistant appears as a sidebar in the tools workers already use, can read the open document or spreadsheet when invoked, and returns output the worker must actively insert—design choices intended to mirror the enterprise deployments most firms are adopting. Treated workers receive a 90-minute onboarding session covering capabilities, confidentiality rules, and a demonstration of common workflows; the session deliberately does not prescribe delegation strategies, because how workers learn to delegate is an object of study. Control workers continue with status quo tools and receive a placebo session of equal length on existing research-portal features, holding attention and expectation effects approximately constant across arms. Compliance is high: 94.3% of treated workers activate the assistant in week 1, and median active usage among treated workers is 11.6 assistant sessions per week during the experiment. Control workers' access is blocked at the identity-management layer, and the firm's monitoring shows negligible use of unsanctioned external tools in both arms.[^2]

[^2]: The firm's information-security policy prohibits pasting client material into external AI tools, and network-level monitoring flags such use. During the experiment, flagged external-tool events occur for 1.7% of control workers and 1.9% of treated workers, with no differential trend. Excluding flagged workers leaves all estimates essentially unchanged.

Two design choices deserve emphasis. First, randomization at the worker level within offices raises the possibility of spillovers from treated to control colleagues; we test for this directly in Section 7.2 and find no evidence of contamination. Second, because the experiment ran for 24 weeks (September 2024–February 2025), spanning the firm's busiest season, our estimates reflect sustained use under real deadline pressure rather than initial experimentation.

## 3.3. Outcome Measurement

*Task database and completion time.* The firm's workflow system logs every work item; at baseline, workers average 6.8 logged work items per week. Our task-level analysis sample comprises the 58,674 substantive client tasks completed during the experiment that satisfy three preregistered inclusion criteria: a minimum of 30 minutes of tracked time, complete telemetry coverage, and unambiguous single-owner attribution. Tasks span five types: drafting (34% of tasks), data analysis (22%), slide production (19%), research memos (15%), and quality reviews (10%). Completion time is measured from telemetry as active working time between task acceptance and submission, excluding idle periods, and we analyze its natural logarithm.

*Output quality.* Quality is scored 0–100 by a rotating panel of 41 senior partners who grade a stratified random subsample of 12,300 tasks—stratified by task type, office, and week to mirror the full sample—under double-blind protocols: graders see neither the worker's identity nor the treatment arm, grade only tasks from outside their own engagements, and receive documents from which formatting cues that could reveal assistant use are stripped by a preprocessing script. The rubric anchors scores to the firm's own review standards across four dimensions (analytical soundness, factual accuracy, communication quality, and client-readiness), which partners apply routinely in engagement reviews, limiting idiosyncratic grading standards. Each subsampled task is graded independently by two partners; the intergrader correlation is 0.81, and we use the grader-pair average. To extend quality measurement to the full sample, we train an automated rubric on the blind-graded subsample; its out-of-sample correlation with the partner-panel average is 0.84, and Section 7.2 shows that all quality results hold, with similar magnitudes, when we use only the blind-graded subsample. Details of the rubric construction and validation are provided in Online Appendix B.2.

*Throughput and revisions.* Weekly task throughput is the count of analysis-sample tasks a worker completes per week. Client revision requests per task are recorded in the firm's engagement-management system, where client-facing partners log requests for substantive rework; the baseline mean is 0.86 requests per task.

*Baseline skill.* We construct a composite baseline skill index as the standardized first principal component of (i) the previous 12 months of the firm's performance ratings and (ii) a pre-experiment skills assessment we administer covering writing, quantitative analysis, and domain knowledge. We divide workers into quartiles Q1 (bottom) through Q4 (top) within the experimental sample. The index predicts baseline quality strongly (a 1-standard-deviation increase is associated with 6.3 points of baseline quality), supporting its validity.

*Survey and verification telemetry.* Our survey is administered in weeks 0, 12, and 24, with a 91.7% response rate (1,689 workers complete all three waves). It measures self-reported delegation strategies, trust in the assistant, and verification behavior; the instrument appears in Online Appendix D. Because self-reports of verification are unreliable, we also measure verification effort objectively via telemetry as the time a treated worker spends in source documents and underlying data after receiving assistant output and before submitting the task.

## 3.4. Frontier Classification

Following the jagged-frontier idea of Dell'Acqua et al. (2023), we work with the firm's methodology committee before launch to classify the firm's task-type taxonomy into tasks "inside the frontier"—those whose content the committee judges a GPT-4-class assistant can competently support—and tasks "beyond the frontier"—those requiring firm-specific tacit knowledge, confidential client context unavailable to the model, or proprietary data the assistant cannot access. The classification is done ex ante, before any treatment data exist, and blind to treatment assignment; it is fixed for the duration of the experiment. Of the 58,674 analysis tasks, 53,687 (91.5%) fall inside the frontier and 4,987 (8.5%) beyond it. Beyond-frontier examples include valuation adjustments that depend on unreleased client financials, recommendations that hinge on undocumented client political constraints, and analyses of proprietary datasets residing outside the assistant's reach. The committee's classification is highly reliable: two subcommittees classifying independently agree on 96.2% of task types, and disagreements are resolved by the full committee before launch. Because the classification operates on the firm's task-type taxonomy rather than on individual tasks, it cannot be influenced by anything a worker or grader does during the experiment. For frontier analyses, we measure task accuracy—the percentage of a task's substantive claims and recommendations judged factually correct by the partner panel—which is available for all blind-graded tasks and extended by the rubric as with quality.

## 3.5. Summary Statistics and Balance

Table 1 presents summary statistics and covariate balance. The average worker is 31.4 years old with 4.2 years of tenure; 46% are female; workers complete 6.8 logged work items per week at baseline with a baseline quality score of 72.3 (standard deviation (SD) 13.9). Treatment–control differences are uniformly small, with all pairwise $p$-values above 0.24 and a joint $F$-test $p$-value of 0.67, as expected under stratified randomization. Attrition over the 24 weeks—workers leaving the firm—is 4.1% in treatment and 4.5% in control ($p = 0.68$); Section 7.2 reports Lee (2009) bounds showing that differential attrition cannot account for our results.

Table 1. Summary Statistics and Covariate Balance

| Variable | Full sample | Control | Treatment | Difference | $p$-value |
|---|---|---|---|---|---|
| Age (years) | 31.4 | 31.3 | 31.5 | 0.2 | 0.38 |
| Female (share) | 0.46 | 0.46 | 0.47 | 0.01 | 0.61 |
| Tenure (years) | 4.2 | 4.2 | 4.3 | 0.1 | 0.44 |
| Baseline skill index (SD units) | 0.00 | −0.01 | 0.01 | 0.02 | 0.72 |
| Baseline weekly tasks | 6.8 | 6.8 | 6.7 | −0.1 | 0.29 |
| Baseline quality score (0–100) | 72.3 | 72.1 | 72.5 | 0.4 | 0.52 |
| Baseline revision requests per task | 0.86 | 0.87 | 0.85 | −0.02 | 0.47 |
| Workers | 1,842 | 921 | 921 | — | — |
| Attrition over 24 weeks (share) | 0.043 | 0.045 | 0.041 | −0.004 | 0.68 |

*Notes.* This table reports pre-experiment means for the full sample and by treatment arm, the treatment–control difference, and the $p$-value from a regression of each covariate on the treatment indicator with strata fixed effects and standard errors clustered by worker. Baseline variables are measured over the 12 months preceding the experiment; the baseline skill index is the standardized composite described in Section 3.3. A joint $F$-test of all covariates yields $p = 0.67$.

# 4. Empirical Framework

## 4.1. Baseline Specification

Our baseline estimating equation is

$$\ln Y_{ijt} = \alpha_j + \delta_t + \beta T_i + \mathbf{X}_i'\boldsymbol{\gamma} + \varepsilon_{ijt}, \qquad (1)$$

where $Y_{ijt}$ is the outcome for worker $i$ on task $j$ in week $t$; $\alpha_j$ denotes task-type fixed effects; $\delta_t$ denotes week fixed effects; $T_i$ is an indicator equal to one if worker $i$ is assigned to treatment; and $\mathbf{X}_i$ is the vector of baseline worker covariates from Table 1 (age, gender, tenure, baseline skill index, baseline weekly tasks, and baseline quality), included for precision. For quality and accuracy outcomes, which are scored in levels, we replace $\ln Y_{ijt}$ with the level $Y_{ijt}$; for weekly throughput, the unit of observation is the worker-week. Because treatment is randomized, $\beta$ identifies the intention-to-treat (ITT) effect of assistant access; given 94.3% week-1 activation, the two-stage least squares treatment-on-the-treated estimate is only modestly larger (for log completion time, $-0.295$ versus the ITT of $-0.278$). Standard errors (SEs) are clustered by worker, the unit of randomization, and all specifications include randomization-strata fixed effects (Athey and Imbens 2017). Estimation is by ordinary least squares (OLS); as Angrist and Pischke (2009) emphasize, covariate adjustment in a randomized design serves precision rather than identification, and our estimates are nearly identical without $\mathbf{X}_i$ (Online Appendix C.1).

## 4.2. Heterogeneity, Dynamics, and Distributional Effects

To estimate heterogeneous effects by baseline skill, we interact treatment with skill-quartile indicators $Q_i^{(q)}$:

$$\ln Y_{ijt} = \alpha_j + \delta_t + \sum_{q=1}^{4}\beta_q\, T_i \times Q_i^{(q)} + \mathbf{X}_i'\boldsymbol{\gamma} + \varepsilon_{ijt}, \qquad (2)$$

where $\beta_q$ is the treatment effect for quartile $q$ and the main quartile effects are absorbed by $\mathbf{X}_i$, which includes the skill index and its quartile indicators.

To trace the dynamics of the treatment effect, we estimate the event-study specification

$$\ln Y_{ijt} = \alpha_j + \delta_t + \sum_{w=-4}^{24}\beta_w\, T_i \times \mathbf{1}[t=w] + \mathbf{X}_i'\boldsymbol{\gamma} + \varepsilon_{ijt}, \qquad (3)$$

where $\mathbf{1}[t=w]$ indicates experimental week $w$ (weeks $-4$ through $0$ are the pre-launch telemetry period) and $\beta_0$ is normalized to zero. The pre-launch coefficients $\beta_{-4},\ldots,\beta_{-1}$ provide a placebo test of the design: because assignment is random, treated and control workers should exhibit parallel outcomes before launch.

To characterize distributional effects on quality, we estimate quantile treatment effects (QTEs),

$$QTE(\tau) = F_{Q^T}^{-1}(\tau) - F_{Q^C}^{-1}(\tau), \qquad (4)$$

where $F_{Q^T}$ and $F_{Q^C}$ are the distribution functions of task quality in the treatment and control arms and $\tau \in (0,1)$ indexes the quantile. Under randomization, Equation (4) identifies the difference between marginal quantiles of the potential-outcome distributions; we compute QTEs within task-type-by-week cells and aggregate with baseline cell weights, with inference by worker-level block bootstrap (1,000 replications).[^3]

[^3]: QTEs identify quantiles of the marginal outcome distributions, not quantiles of the individual treatment-effect distribution, unless one imposes rank invariance. Our within-worker variance results in Section 5.3, which compare each worker's own dispersion across arms of the quality distribution, do not require that assumption.

## 4.3. Power, Preregistration, and Multiple Testing

The design is well powered. With 1,842 workers, worker-level clustering, and an intracluster correlation of 0.19 estimated from baseline telemetry, the minimum detectable effect on log completion time at 80% power is 0.041—roughly one-seventh of the effect we estimate—and the minimum detectable quality effect is 1.3 points. The preregistration specifies the four primary outcomes of Table 2 as a family and the skill-quartile, QTE, dynamic, and frontier analyses as named secondary analyses; all results we report as significant survive a conservative Bonferroni adjustment within their preregistered family, and Section 7.2 reports randomization-inference $p$-values that do not rely on asymptotic clustering approximations. Exploratory analyses—principally the verification-tercile splits and survey correlations—are labeled as such where they appear.

# 5. Main Results

## 5.1. Average Effects

Table 2 presents estimates of Equation (1) for our four primary outcomes. Assistant access reduces log task completion time by $-0.278$ (SE 0.021, $p < 0.001$), which corresponds to a 24.3% reduction in completion time. The effect is economically large: at the control geometric mean of 6.1 active hours per task, treated workers save roughly 1.5 hours per task. Output quality rises by 3.9 points (SE 0.9) on the 0–100 scale, or 0.28 SDs of the control quality distribution (SD 13.9)—the assistant does not purchase speed at the expense of quality on the average task; it improves both. Weekly task throughput rises by 16.4% (SE 1.8), somewhat less than the per-task time saving, because workers reallocate part of the freed time to nontask activities such as business development and training rather than converting all of it into additional tasks. Finally, client revision requests per task fall by 18.7% (SE 3.1), from a control mean of 0.86 to roughly 0.70 requests per task—an externally validated quality signal, generated by clients rather than graders, that corroborates the panel-graded quality gains.

Table 2. Average Treatment Effects of LLM Assistant Access

| | (1) Log completion time | (2) Quality (0–100) | (3) Weekly throughput (%) | (4) Revision requests (%) |
|---|---|---|---|---|
| Treatment ($T_i$) | −0.278*** | 3.9*** | +16.4*** | −18.7*** |
| | (0.021) | (0.9) | (1.8) | (3.1) |
| Implied effect | −24.3% | +0.28 SD | — | — |
| Control mean | 6.1 hours | 72.8 | 6.9 tasks | 0.86 per task |
| Task-type FE | Yes | Yes | — | Yes |
| Week FE | Yes | Yes | Yes | Yes |
| Worker covariates | Yes | Yes | Yes | Yes |
| Observations | 58,674 | 58,674 | 43,260 | 58,674 |
| $R^2$ | 0.34 | 0.27 | 0.22 | 0.19 |

*Notes.* This table reports ITT estimates of Equation (1). Column (1) uses log active completion time; column (2) uses the 0–100 quality score (partner-panel grades on the 12,300-task blind subsample, extended by the validated rubric); columns (3) and (4) report semi-elasticities in percent, estimated from log weekly throughput at the worker-week level and log(1 + revision requests) at the task level, respectively. All specifications include randomization-strata fixed effects and the baseline covariates in Table 1. Standard errors, clustered by worker, are in parentheses. The control mean in column (1) is the geometric mean. \*\*\*, \*\*, and \* denote statistical significance at the 1%, 5%, and 10% levels, respectively, based on two-sided $t$-tests with worker-clustered standard errors.

Three features of these estimates deserve interpretation. First, the joint movement of time, quality, and revisions distinguishes our field results from settings in which AI accelerates output while degrading it. On the modal consulting task—inside the frontier, as Section 6 makes precise—the assistant functions as a competent first-drafter and research aide, and workers convert its speed into both time savings and additional revision passes. Second, the throughput effect (+16.4%) implies that the firm captures much of the time saving as additional output: at baseline utilization, this is equivalent to adding roughly 145 full-time consultants to the treated group's capacity without hiring.[^4] Third, our average effects sit between the laboratory estimates of Noy and Zhang (2023), who study self-contained writing tasks where the assistant can do most of the work, and the customer-support estimates of Brynjolfsson et al. (2025), consistent with the intermediate share of consulting task content that overlaps LLM capabilities.

[^4]: The calculation multiplies the treated headcount (921, less attrition) by the 16.4% throughput gain: $921 \times 0.959 \times 0.164 \approx 145$ full-time-equivalent consultants at unchanged hours.

The revision-request result merits a further word because it addresses the deepest concern about generative AI in client work: that fluent output passes internal review but fails in the field. Revision requests are logged by client-facing partners in response to client feedback, weeks after task submission, by people with no knowledge of the experiment's arm structure at the task level. That this externally generated measure falls by 18.7%—directionally and proportionally consistent with the 3.9-point panel-graded quality gain—indicates that the quality improvement is real to clients, not an artifact of grading. It also implies direct cost savings: at the firm's internal estimate of partner and associate time absorbed per revision cycle, the reduction is worth roughly 2% of engagement delivery cost on its own, before counting the reputational value of fewer client-visible errors.

## 5.2. Heterogeneity by Baseline Skill

Table 3 presents estimates of Equation (2). The treatment effect on completion time declines monotonically—and steeply—in baseline skill. Bottom-quartile (Q1) workers complete tasks 35.1% faster (coefficient $-0.433$, SE 0.038), Q2 workers 27.2% faster ($-0.318$, SE 0.033), Q3 workers 19.8% faster ($-0.221$, SE 0.031), and top-quartile (Q4) workers only 11.2% faster ($-0.119$, SE 0.029). Quality effects show the same gradient: +0.47 SDs (SE 0.05) for Q1, +0.33 (SE 0.05) for Q2, +0.19 (SE 0.04) for Q3, and a statistically insignificant +0.06 (SE 0.04) for Q4. The Q1–Q4 differences are significant at the 1% level for both outcomes ($p < 0.001$).

Table 3. Heterogeneous Treatment Effects by Baseline Skill Quartile

| Skill quartile | Log completion time | Implied time effect | Quality (SD units) | Quality (points) |
|---|---|---|---|---|
| Q1 (bottom) | −0.433*** | −35.1% | +0.47*** | +6.5 |
| | (0.038) | | (0.05) | |
| Q2 | −0.318*** | −27.2% | +0.33*** | +4.6 |
| | (0.033) | | (0.05) | |
| Q3 | −0.221*** | −19.8% | +0.19*** | +2.6 |
| | (0.031) | | (0.04) | |
| Q4 (top) | −0.119*** | −11.2% | +0.06 | +0.8 |
| | (0.029) | | (0.04) | |
| $p$-value, Q1 = Q4 | <0.001 | | <0.001 | |
| Observations | 58,674 | | 58,674 | |

*Notes.* This table reports estimates of Equation (2), interacting treatment with baseline skill-quartile indicators. Quartiles are defined on the pre-experiment composite skill index described in Section 3.3. Quality effects are reported in control-group standard deviation units (1 SD = 13.9 points) and converted to points in the final column. All specifications include task-type, week, and strata fixed effects and baseline covariates. Standard errors, clustered by worker, are in parentheses. The task-weighted average of the quartile-specific time coefficients equals the pooled estimate of $-0.278$ in Table 2. \*\*\*, \*\*, and \* denote statistical significance at the 1%, 5%, and 10% levels, respectively, based on two-sided $t$-tests with worker-clustered standard errors.

The economic interpretation follows the logic of Section 2.3. For a bottom-quartile associate, the assistant supplies at low cost much of what separates her from a top-quartile colleague: command of structure, fluency, standard analytical templates, and rapid retrieval of background knowledge. That is codified expertise, and the assistant delivers it on demand (Garicano 2000). For a top-quartile worker, those inputs were never the constraint; her scarce inputs—client judgment, firm-specific context, original framing—are precisely the ones the assistant cannot supply, so her gains are confined to mechanical time savings. The gradient closely parallels Brynjolfsson et al. (2025), who find the largest gains for novice customer support agents, and Noy and Zhang (2023), who find that ChatGPT compresses the quality distribution of writers; our contribution is to show that the same compression obtains in multi-domain professional work, at stakes, and persists over the full 24 weeks. It also connects to Wang et al. (2024), who show that AI assistance can help inexperienced workers most when the AI encodes what experience teaches.

Two mechanical explanations for the gradient can be ruled out. First, the quality gradient is not a ceiling effect: top-quartile workers' baseline quality averages 81.5 on the 100-point scale, leaving ample headroom, and fewer than 3% of their control-arm tasks score above 95; moreover, the *time* gradient, which faces no ceiling, is equally steep. Second, the gradient does not reflect differential adoption: week-1 activation exceeds 92% in every skill quartile, and usage intensity is essentially flat across quartiles (11.2 to 12.1 sessions per week), so low-skill workers gain more from each unit of use, not merely from using the assistant more.

## 5.3. Distributional Effects and Skill Compression

The quartile results imply that generative AI compresses the performance distribution, and Table 4 characterizes that compression directly. Panel A reports QTEs on task quality from Equation (4). The treatment effect at the 10th percentile of the quality distribution is +6.8 points ($p < 0.01$), declining monotonically to +5.6 at the 25th percentile, +3.8 at the median, +2.1 at the 75th, and a statistically insignificant +0.7 at the 90th percentile. The assistant lifts the bottom of the quality distribution while leaving its top essentially untouched.

Panel B translates the compression into worker-level dispersion statistics. The 90/10 gap in worker-average quality—the difference between the 90th- and 10th-percentile worker—is 18.3 points in the control group and 13.1 points in the treatment group, a narrowing of 28.4%. Compression also operates within workers: the average within-worker SD of task quality falls from 8.2 points in control to 6.6 in treatment, a 19.6% reduction, indicating that the assistant not only raises weak workers toward strong ones but makes each worker's output more reliable task to task. For a professional services firm that sells consistency—clients buy the firm's quality distribution, not its mean—this within-worker reliability gain is arguably as valuable as the level effect.

Table 4. Distributional Effects on Output Quality

| Panel A: Quantile treatment effects | $\tau = 0.10$ | $\tau = 0.25$ | $\tau = 0.50$ | $\tau = 0.75$ | $\tau = 0.90$ |
|---|---|---|---|---|---|
| $QTE(\tau)$, quality points | +6.8*** | +5.6*** | +3.8*** | +2.1** | +0.7 |
| | (1.1) | (0.9) | (0.8) | (0.9) | (1.0) |

| Panel B: Worker-level dispersion | Control | Treatment | Change |
|---|---|---|---|
| 90/10 gap in worker-average quality (points) | 18.3 | 13.1 | −28.4% |
| Within-worker SD of task quality (points) | 8.2 | 6.6 | −19.6% |

*Notes.* Panel A reports quantile treatment effects from Equation (4), computed within task-type-by-week cells and aggregated with baseline cell weights; standard errors (in parentheses) are from a worker-level block bootstrap with 1,000 replications. Panel B reports dispersion statistics of worker-average quality and the average within-worker standard deviation of task quality over the experimental period, by arm. \*\*\*, \*\*, and \* denote statistical significance at the 1%, 5%, and 10% levels, respectively, based on bootstrap percentile intervals.

The QTE profile and the quartile results in Table 3 are mutually consistent but conceptually distinct: Table 3 shows that *ex ante weaker workers* gain more, whereas Panel A of Table 4 shows that *weaker task outcomes* gain more, and the within-worker result shows that both margins operate. A useful summary is that the assistant truncates the left tail of the quality distribution at every level: it rescues the weak tasks of strong workers and most tasks of weak workers, while adding little to output that was already excellent. That is what one expects if the assistant reliably supplies a competent floor—structure, completeness, error-free prose—but cannot supply the insight that distinguishes the best work.

These distributional findings carry implications beyond the average effect. Within the firm, they weaken the link between measured output quality and the underlying skill that quality ratings are meant to reveal, complicating promotion and staffing decisions that rely on output-based screening (Hoffman et al. 2018). Across the labor market, they suggest that generative AI—unlike the computerization wave analyzed by Autor et al. (2003), which raised the returns to skill—may compress returns within exposed occupations, an equalizing pattern consistent with emerging evidence (Brynjolfsson et al. 2025, Noy and Zhang 2023). We return to the managerial consequences in Section 7.3.

## 5.4. Learning Dynamics

Figure 1 plots the event-study coefficients from Equation (3) for log completion time. Three features stand out. First, the pre-launch coefficients for weeks $-4$ through $0$ are tightly clustered around zero (all within $\pm 0.015$, jointly insignificant, $p = 0.62$), confirming that randomization produced parallel pre-period behavior. Second, the treatment effect at launch is modest—$-0.09$ in week 1—and deepens steadily to $-0.31$ by week 10 as workers learn what to delegate and how to prompt. Third, from week 10 through week 24 the effect sits on a stable plateau of $-0.31 \pm 0.02$, with no sign of decay.

![Figure 1. (Color online) Dynamics of the Treatment Effect on Task Completion Time](/tmp/claude-0/-home-user-xixi/c700b243-db1e-53b1-9664-970dce4c2150/scratchpad/fig1_paper1.png)

*Notes.* The figure plots the coefficients $\beta_w$ from the event-study specification in Equation (3), where the outcome is log task completion time, together with 95% confidence intervals based on worker-clustered standard errors. Week 0 is the final pre-launch week and is normalized to zero; weeks $-4$ through $0$ constitute the pre-launch telemetry period. The treatment effect is $-0.09$ in week 1, deepens to $-0.31$ by week 10, and remains on a plateau of $-0.31 \pm 0.02$ through week 24. The shaded band marks the plateau range.

The dynamics matter for interpretation and for policy. A Hawthorne-style novelty effect would produce the opposite profile—a spike at launch that fades as attention wanes—whereas we observe gradual buildup and 14 weeks of persistence under peak-season workloads; the persistence rules out novelty as the driver. The profile instead matches the co-invention logic of the GPT literature (Bresnahan and Trajtenberg 1995, Brynjolfsson et al. 2021): the assistant's returns require complementary intangible capital—what we call prompting and delegation capital—that workers accumulate through use. Survey evidence corroborates this reading: between weeks 0 and 12, the share of treated workers reporting a settled task-level delegation strategy rises from 18% to 71%, and the week-12 survey measure of delegation sophistication predicts the worker's subsequent time saving (correlation 0.36; Online Appendix D.3). For managers, the plateau timing implies that pilots evaluated at four or six weeks—a common practice—will understate steady-state returns by roughly half, and that structured prompt training may accelerate the climb to the plateau. We note that the volume-weighted average of the post-launch coefficients in Figure 1 reproduces the pooled estimate of $-0.278$ in Table 2, because task volumes are higher in the later, plateau weeks of the busy season.

The learning process itself is skill-dependent in an instructive way. Estimating Equation (3) separately by skill quartile, bottom-quartile workers reach their plateau by roughly week 8, whereas top-quartile workers converge more slowly and to a much shallower plateau. The survey suggests why: low-skill workers report delegating whole task components ("write the first draft of the memo"), a strategy that is quick to discover, whereas high-skill workers converge on selective, surgical uses ("stress-test this argument," "find the three weakest claims") that take longer to develop but avoid quality risk. The delegation strategies that emerge by week 24 thus differ qualitatively across the skill distribution, which is itself a finding about how organizations should differentiate training: the productive frontier use for a first-year associate is not the productive use for a seasoned manager.

# 6. The Frontier Problem: When AI Assistance Backfires

## 6.1. Accuracy Inside and Beyond the Frontier

The results so far average over tasks the assistant handles well and tasks it does not. This section shows that the distinction is sharp, predictable, and managerially decisive. We estimate

$$A_{ijt} = \alpha_j + \delta_t + \beta_1 T_i + \beta_2 B_j + \beta_3 T_i \times B_j + \mathbf{X}_i'\boldsymbol{\gamma} + \varepsilon_{ijt}, \qquad (5)$$

where $A_{ijt}$ is task accuracy (the percentage of a task's substantive claims and recommendations judged factually correct, defined in Section 3.4), $B_j$ indicates that task $j$ belongs to a beyond-frontier task type, and $\beta_3$ captures how the treatment effect differs beyond the frontier. Because the frontier classification is fixed ex ante and blind to treatment, $B_j$ is predetermined, and $\beta_1$ and $\beta_3$ retain their experimental interpretation within each task segment.

Table 5 presents the results. Panel A reports raw cell means. Inside the frontier, treated workers' accuracy is 86.7% against a control mean of 84.6%—a gain of 2.1 percentage points (p.p.). Beyond the frontier, the pattern inverts violently: control workers achieve 71.2% accuracy, whereas treated workers achieve 56.4%, a raw deficit of 14.8 p.p. Panel B reports the regression estimates of Equation (5): $\beta_1 = 2.1$ p.p. (SE 0.8, significant at 5%), $\beta_2 = -13.4$ p.p. (SE 1.9), and the interaction $\beta_3 = -14.8$ p.p. (SE 2.7, $p < 0.001$), implying a total adjusted treatment effect beyond the frontier of $\beta_1 + \beta_3 = -12.7$ p.p. (SE 2.6). The adjusted total effect is slightly smaller in magnitude than the raw 14.8-point gap because treated workers, with their higher throughput, complete a modestly larger share of the most difficult beyond-frontier task types in the later weeks that the fixed effects absorb.

Table 5. Task Accuracy Inside and Beyond the AI Capability Frontier

| Panel A: Accuracy means (%) | Control | Treatment | Difference |
|---|---|---|---|
| Inside frontier (91.5% of tasks) | 84.6 | 86.7 | +2.1** |
| Beyond frontier (8.5% of tasks) | 71.2 | 56.4 | −14.8*** |

| Panel B: Equation (5) estimates | Coefficient | SE | |
|---|---|---|---|
| Treatment ($\beta_1$) | 2.1** | (0.8) | |
| Beyond frontier ($\beta_2$) | −13.4*** | (1.9) | |
| Treatment × Beyond frontier ($\beta_3$) | −14.8*** | (2.7) | |
| Total effect beyond frontier ($\beta_1 + \beta_3$) | −12.7*** | (2.6) | |

| Panel C: $\beta_3$ by verification-effort tercile (treated workers) | Coefficient | SE | |
|---|---|---|---|
| Top tercile (most verification) | −4.2 | (2.9) | |
| Middle tercile | −13.9*** | (3.0) | |
| Bottom tercile (least verification) | −23.6*** | (3.4) | |

*Notes.* Panel A reports mean task accuracy—the percentage of substantive claims and recommendations judged factually correct—by treatment arm and frontier classification; the ex ante classification (Section 3.4) assigns 53,687 tasks inside and 4,987 tasks beyond the frontier. Panel B reports estimates of Equation (5) with task-type, week, and strata fixed effects and baseline covariates; standard errors are clustered by worker. Panel C re-estimates the interaction separately for treated workers in each tercile of telemetry-measured verification effort (time in source documents after receiving assistant output), each tercile compared against the full control group. \*\*\*, \*\*, and \* denote statistical significance at the 1%, 5%, and 10% levels, respectively, based on two-sided $t$-tests with worker-clustered standard errors.

The magnitude of the beyond-frontier loss deserves emphasis. A 14.8-point accuracy deficit on client-facing recommendations is not a rounding error in an otherwise positive picture; at the firm's historical relationship between recommendation errors and engagement renewal, losses of this size on even 8.5% of tasks could offset a substantial fraction of the value created inside the frontier. The finding generalizes the single-task demonstration of Dell'Acqua et al. (2023)—who observe a 19-point decline in correct solutions on one designed beyond-frontier task—to nearly 5,000 real client tasks classified ex ante, and shows that the frontier is not an artifact of adversarial task design but a durable feature of production with generative AI.

The anatomy of beyond-frontier errors is revealing. In a qualitative review of 400 low-accuracy beyond-frontier tasks from the treated arm, the partner panel classifies the dominant failure as *plausible substitution*: where the required input is unavailable to the model—an unreleased financial figure, an undocumented client constraint—the assistant substitutes a generic industry benchmark or a textbook assumption, stated with the same fluency as its correct claims, and the worker carries the substitution into the deliverable. Outright fabrication of sources is rare (under 4% of reviewed errors) because the firm's citation norms force checking of references; it is the *unflagged assumption*, not the invented fact, that penetrates review. Notably, the beyond-frontier time saving is nearly as large as the inside-frontier saving—treated workers complete beyond-frontier tasks 21.7% faster—which is exactly the danger: the assistant is no less fluent, and the worker no less accelerated, on tasks where its output is unreliable.[^5]

[^5]: The frontier effect also does not reflect worker sorting across task types: because engagement staffing is set by partners before task assignment, the share of beyond-frontier tasks is balanced across arms (8.4% treated versus 8.6% control, $p = 0.55$), and worker-level frontier exposure is uncorrelated with treatment.

## 6.2. Verification Behavior and Overtrust

Why do capable professionals submit degraded work? Panel C of Table 5 provides the central clue: the beyond-frontier loss is almost entirely a phenomenon of insufficient verification. Splitting treated workers by telemetry-measured verification effort, the accuracy loss is a statistically insignificant $-4.2$ p.p. in the top tercile, $-13.9$ p.p. in the middle tercile, and $-23.6$ p.p. in the bottom tercile. Workers who habitually return to source documents and underlying data after receiving assistant output largely escape the frontier penalty; workers who submit with minimal checking absorb it fully. Because verification behavior is chosen rather than randomized, we interpret these splits as descriptive moderation rather than causal effects of verification, but the gradient is steep, monotone, and robust to conditioning on baseline skill and tenure.[^6]

[^6]: Verification terciles are computed from weeks 5–24 telemetry to allow delegation habits to form; using weeks 1–24 or worker fixed characteristics from the week-12 survey yields the same ordering (Online Appendix C.5). Verification effort is only weakly correlated with baseline skill (correlation 0.11), so the moderation is not a restatement of Table 3.

Our survey evidence points to miscalibrated trust as the proximate driver. By week 12, 62.3% of treated workers agree that they "generally trust the assistant's output for familiar task types," and an overtrust index—constructed from survey items measuring trust net of the assistant's measured reliability on the worker's own task mix—correlates at $-0.41$ with the worker's beyond-frontier accuracy change. The pattern is the mirror image of algorithm aversion (Dietvorst et al. 2015): rather than abandoning the tool after errors, workers extend to unfamiliar territory the trust the assistant earned inside the frontier, a field manifestation of algorithm appreciation (Logg et al. 2019) compounded by the difficulty of judging where one's own knowledge ends and the machine's begins (Fügener et al. 2022). Consistent with Dietvorst et al. (2018), treated workers who report actively editing assistant output—rather than accepting or rejecting it wholesale—show both higher trust and higher accuracy, suggesting that modify-and-verify workflows sustain calibrated reliance. The economics are those of Agrawal et al. (2018): the assistant makes drafting cheap, but the complementary input—judgment about when its output can be trusted—remains scarce, and workers underprice it precisely because the assistant's fluent failures give no warning.

# 7. Mechanisms, Robustness, and Managerial Implications

## 7.1. Where the Time Goes: A Decomposition

To understand how the assistant produces its time savings, we decompose the treatment effect on completion time across activity components using telemetry, which allocates each task's active time to drafting, information search, and verification/editing. The decomposition identity is

$$\Delta \ln \bar{Y} = \sum_{k} s_k \, \Delta \ln \bar{Y}_k, \qquad (6)$$

where $\Delta \ln \bar{Y}$ is the total proportional change in average task time, $k$ indexes activity components, $s_k$ is the baseline time share of component $k$, and $\Delta \ln \bar{Y}_k$ is the proportional change in component $k$'s time per task; a residual composition term captures the covariance between treatment-induced changes in shares and component times.

Table 6 presents the results. Drafting time per task falls by 41.3% from a baseline share of 46%, contributing $-19.0$ p.p. to the total; information search falls by 28.9% from a 31% share, contributing $-9.0$ p.p.; and verification/editing time *rises* by 12.4% from a 23% share, contributing $+2.9$ p.p. The component contributions sum to $-25.1$ p.p., and the composition term contributes $+0.8$ p.p., reproducing exactly the headline completion-time effect of $-24.3$% via Equation (6).

Table 6. Decomposition of the Treatment Effect on Task Completion Time

| Activity component | Baseline time share | Change in time per task | Contribution (p.p.) |
|---|---|---|---|
| Drafting | 0.46 | −41.3%*** | −19.0 |
| Information search | 0.31 | −28.9%*** | −9.0 |
| Verification/editing | 0.23 | +12.4%*** | +2.9 |
| Sum of component contributions | | | −25.1 |
| Composition (covariance) term | | | +0.8 |
| Total (Equation (6)) | 1.00 | | −24.3 |

*Notes.* This table decomposes the average treatment effect on task completion time across telemetry-measured activity components using Equation (6). Baseline time shares are control-group shares of active task time; changes in time per task are ITT estimates from component-level analogues of Equation (1); contributions are shares multiplied by changes. The composition term captures the covariance between treatment-induced changes in activity shares and component times. The total matches the −24.3% implied by the log completion-time coefficient in Table 2. \*\*\*, \*\*, and \* denote statistical significance at the 1%, 5%, and 10% levels, respectively, based on two-sided $t$-tests with worker-clustered standard errors.

The decomposition clarifies what kind of technology this is. The assistant automates the production of first drafts and compresses search, whereas verification and editing—the judgment-intensive residual—absorb *more* time, in levels as a share of the task and not merely relatively. Treated workers reallocate effort from generating content to evaluating it, a reallocation that echoes the task-model predictions of Autor et al. (2003) and Acemoglu and Restrepo (2018): automation of some tasks raises the value and intensity of the complementary tasks that remain. The rise in verification time also explains why average quality improves in Table 2—freed drafting time funds additional checking on inside-frontier tasks—and, juxtaposed with Section 6.2, why quality collapses when workers fail to make that reallocation on beyond-frontier tasks.

## 7.2. Robustness

Our conclusions survive a battery of preregistered robustness checks; we summarize the six main ones here and report full tables in Online Appendix C.

First, differential attrition cannot drive the results. Attrition is low and balanced (4.1% treatment versus 4.5% control), and Lee (2009) bounds on the log completion-time effect—trimming the treatment distribution to equalize retention—span $[-0.301, -0.257]$, comfortably excluding zero and bracketing the point estimate of $-0.278$.

Second, inference is not an artifact of asymptotic approximations. Randomization inference that permutes treatment assignments within strata 10,000 times yields $p < 0.001$ for the completion-time, quality, and throughput effects (Athey and Imbens 2017).

Third, spillovers do not contaminate the control group. Exploiting random variation in the treated share of each control worker's project teams, control workers on high-treatment-density teams show no differential change in completion time relative to control workers on low-density teams (coefficient 0.008, SE 0.019, not significant), indicating that our ITT contrasts are not attenuated—or inflated—by within-team diffusion; see Table C.2 in Online Appendix C.

Fourth, grading is credibly blind. A post-experiment audit asked 14 partners to guess, for 600 stripped tasks, whether each was assistant-supported; accuracy was 52.7%, indistinguishable from chance ($p = 0.19$), and grader fixed effects leave the quality estimates unchanged.

Fifth, the results do not depend on the automated rubric. Re-estimating all quality and accuracy results on the 12,300-task blind-graded subsample alone yields a quality effect of 4.1 points (SE 1.0) and a beyond-frontier interaction of $-15.3$ p.p. (SE 3.2), statistically indistinguishable from the full-sample estimates.

Sixth, no single site drives the findings. An office-by-office jackknife—dropping each of the 14 offices in turn—produces completion-time coefficients between $-0.259$ and $-0.294$, and the skill gradient and frontier interaction retain sign and significance in every replicate.

Beyond these six preregistered checks, two threats specific to our setting deserve discussion. One is strategic task selection: treated workers might route themselves toward AI-suitable tasks, mechanically inflating measured gains. Because partners assign engagement staffing and task ownership before workers see task content, selection margins are narrow, and the observed task-type mix is balanced across arms. The other is quality-standard drift: if graders' expectations rise as AI-polished output becomes common, control workers' scores would be depressed in later weeks; however, control-arm quality is flat across the 24 weeks (weekly coefficients jointly insignificant, $p = 0.44$), and the blind-graded subsample—scored in randomized order after the experiment ends—yields the same estimates.

## 7.3. Managerial Implications

Our results translate into four sets of managerial prescriptions for firms deploying generative AI in knowledge work.

*Task-based deployment, not blanket rollout.* The contrast between a +2.1 p.p. accuracy gain inside the frontier and a 14.8 p.p. accuracy deficit beyond it implies that deployment policy should be written at the level of tasks, not tools or roles. Our ex ante classification exercise demonstrates that a firm's own methodology experts can map the frontier before deployment, cheaply and accurately: the pre-launch classification predicted where treatment harmed accuracy without any treatment data. Firms should embed such classifications in workflow systems—flagging beyond-frontier task types at the point of assistant use—rather than relying on workers' own frontier judgments, which Section 6.2 shows are systematically miscalibrated.

*Verification is the scarce complement; train and staff for it.* The verification gradient in Panel C of Table 5—losses of 23.6 p.p. among minimal verifiers versus 4.2 p.p. among diligent ones—identifies the highest-return training target. Because verification effort is observable in telemetry, firms can monitor it as a leading indicator of quality risk, build verification-time expectations into task budgets (our treated workers' verification time rises 12.4%, and quality rises with it), and redesign quality assurance to concentrate senior review on beyond-frontier output rather than sampling uniformly.

*Rethink the talent model.* Skill compression—a 28.4% narrowing of the 90/10 quality gap—changes the economics of the professional services pyramid. Junior workers become productive faster, which raises the return to hiring at the bottom, but output quality becomes a weaker screen for underlying skill, which degrades the information content of the tournaments that govern promotion (Hoffman et al. 2018). Firms will need to evaluate the judgment-intensive components of performance—frontier recognition, verification diligence, client management—directly, precisely because the assistant equalizes the rest. In Garicano's (2000) terms, the hierarchy's bottom layer is now partially automated; the human hierarchy above it should be reorganized around the exceptions.

*Reprice and restaff around the plateau.* The dynamics in Figure 1 imply that steady-state gains (a plateau log-time effect of $-0.31$, or roughly 27% time savings) more than triple the week-1 effect, so pilots should run at least a quarter, and business cases should use plateau rather than launch estimates. For professional services specifically, a durable 24.3% reduction in task time with a 16.4% throughput gain pressures billable-hour pricing and argues for accelerating the shift toward fixed-fee and value-based contracts, with the freed senior capacity redeployed to the verification and client-judgment tasks whose relative value the technology raises.

Taken together, these prescriptions reframe the deployment question. The relevant managerial choice is not the binary one—adopt or not—that dominates executive discussion, but a portfolio of complementary organizational investments: a task-level frontier map, verification norms embedded in workflow and telemetry, evaluation systems that measure judgment directly, and pricing that captures rather than forfeits the productivity gain. Our estimates imply that the returns to the technology and the returns to these complements are of comparable magnitude: a firm that deploys the assistant but manages its frontier badly can lose in the 8.5% of beyond-frontier tasks a large share of what it gains in the other 91.5%, whereas a firm that pairs deployment with the complements captures both the 24.3% time saving and the quality gains without the accuracy losses concentrated among unverified output.

# 8. Concluding Remarks

This paper reports what is, to our knowledge, the first large-scale, long-horizon randomized field experiment on generative AI in real, multi-domain professional work. Access to an LLM assistant reduces task completion time by 24.3%, raises output quality by 0.28 SDs, increases weekly throughput by 16.4%, and reduces client revision requests by 18.7%. The gains are strongly equalizing—bottom-quartile workers gain three times as much time and nearly eight times as much quality as top-quartile workers, narrowing the 90/10 quality gap by 28.4%—and they build over ten weeks to a durable plateau, consistent with the accumulation of complementary prompting and delegation capital. Against these gains stands a sharp boundary: on the 8.5% of tasks beyond the assistant's competence frontier, treated workers' accuracy falls 14.8 percentage points, with losses concentrated among workers who verify least and trust most. The technology's value, in short, is large, unevenly distributed, learned rather than instantaneous, and conditional on managing its frontier.

We acknowledge the limitations of our evidence. The experiment covers one firm, one occupational class, and 24 weeks; although the setting is representative of a broad class of knowledge work, professional services firms select workers and structure tasks in particular ways, and effects could differ in occupations with faster feedback or thinner documentation. Our horizon is long enough to rule out novelty effects but not to observe equilibrium adjustments: wages, promotion standards, hiring composition, client pricing, and the assistant's own capabilities will all move in general equilibrium, and our design holds them fixed by construction. The mechanism evidence on trust and verification, although disciplined by telemetry and ex ante classification, is correlational. And the frontier itself is jagged and moving: as model capabilities expand, task types will migrate across it, so the classifications—though not, we believe, the logic—of Section 6 will require continual revision.

Future research should pursue three directions: randomized verification training and frontier-disclosure interventions to establish the causal counterpart of our moderation evidence; longer-horizon designs that track promotion, retention, and wage consequences of skill compression; and multi-firm replications that map how the frontier and its costs vary with task documentation, client confidentiality, and model access to proprietary data. As generative AI diffuses through the knowledge economy, the question facing managers is no longer whether it raises productivity—on the evidence here, it does, substantially—but how to organize work so that its gains are captured where the technology is strong and its fluent failures are caught where it is not.

# Acknowledgments

The authors thank the collaborating firm's leadership, methodology committee, and partner-grading panel for their extraordinary cooperation, and seminar participants at several universities and practitioner workshops for helpful comments.

# References

Acemoglu D, Restrepo P (2018) The race between man and machine: Implications of technology for growth, factor shares, and employment. *Amer. Econom. Rev.* 108(6):1488–1542.

Agrawal A, Gans J, Goldfarb A (2018) *Prediction Machines: The Simple Economics of Artificial Intelligence* (Harvard Business Review Press, Boston).

Angrist JD, Pischke JS (2009) *Mostly Harmless Econometrics: An Empiricist's Companion* (Princeton University Press, Princeton, NJ).

Athey S, Imbens GW (2017) The econometrics of randomized experiments. *Handbook of Economic Field Experiments*, vol. 1 (North-Holland, Amsterdam), 73–140.

Autor DH (2015) Why are there still so many jobs? The history and future of workplace automation. *J. Econom. Perspect.* 29(3):3–30.

Autor DH, Levy F, Murnane RJ (2003) The skill content of recent technological change: An empirical exploration. *Quart. J. Econom.* 118(4):1279–1333.

Bandiera O, Barankay I, Rasul I (2007) Incentives for managers and inequality among workers: Evidence from a firm-level experiment. *Quart. J. Econom.* 122(2):729–773.

Bloom N, Liang J, Roberts J, Ying ZJ (2015) Does working from home work? Evidence from a Chinese experiment. *Quart. J. Econom.* 130(1):165–218.

Boussioux L, Lane JN, Zhang M, Jacimovic V, Lakhani KR (2024) The crowdless future? Generative AI and creative problem-solving. *Organ. Sci.* 35(5):1589–1607.

Bresnahan TF, Trajtenberg M (1995) General purpose technologies "Engines of growth"? *J. Econometrics* 65(1):83–108.

Brynjolfsson E, Li D, Raymond L (2025) Generative AI at work. *Quart. J. Econom.* 140(2):889–942.

Brynjolfsson E, Rock D, Syverson C (2021) The productivity J-curve: How intangibles complement general purpose technologies. *Amer. Econom. J.: Macroeconom.* 13(1):333–372.

Choudhury P, Foroughi C, Larson B (2021) Work-from-anywhere: The productivity effects of geographic flexibility. *Strategic Management J.* 42(4):655–683.

Dell'Acqua F, McFowland E III, Mollick ER, Lifshitz-Assaf H, Kellogg K, Rajendran S, Krayer L, Candelon F, Lakhani KR (2023) Navigating the jagged technological frontier: Field experimental evidence of the effects of artificial intelligence on knowledge worker productivity and quality. Harvard Business School Working Paper No. 24-013, Harvard Business School, Boston.

Dietvorst BJ, Simmons JP, Massey C (2015) Algorithm aversion: People erroneously avoid algorithms after seeing them err. *J. Experiment. Psych.: General* 144(1):114–126.

Dietvorst BJ, Simmons JP, Massey C (2018) Overcoming algorithm aversion: People will use imperfect algorithms if they can (even slightly) modify them. *Management Sci.* 64(3):1155–1170.

Doshi AR, Hauser OP (2024) Generative AI enhances individual creativity but reduces the collective diversity of novel content. *Sci. Adv.* 10(28):eadn5290.

Eloundou T, Manning S, Mishkin P, Rock D (2024) GPTs are GPTs: Labor market impact potential of LLMs. *Science* 384(6702):1306–1308.

Felten E, Raj M, Seamans R (2021) Occupational, industry, and geographic exposure to artificial intelligence: A novel dataset and its potential uses. *Strategic Management J.* 42(12):2195–2217.

Fügener A, Grahl J, Gupta A, Ketter W (2022) Cognitive challenges in human–artificial intelligence collaboration: Investigating the path toward productive delegation. *Inform. Systems Res.* 33(2):678–696.

Garicano L (2000) Hierarchies and the organization of knowledge in production. *J. Political Econom.* 108(5):874–904.

Hoffman M, Kahn LB, Li D (2018) Discretion in hiring. *Quart. J. Econom.* 133(2):765–800.

Jia N, Luo X, Fang Z, Liao C (2024) When and how artificial intelligence augments employee creativity. *Acad. Management J.* 67(1):5–32.

Kleinberg J, Lakkaraju H, Leskovec J, Ludwig J, Mullainathan S (2018) Human decisions and machine predictions. *Quart. J. Econom.* 133(1):237–293.

Lee DS (2009) Training, wages, and sample selection: Estimating sharp bounds on treatment effects. *Rev. Econom. Stud.* 76(3):1071–1102.

Logg JM, Minson JA, Moore DA (2019) Algorithm appreciation: People prefer algorithmic to human judgment. *Organ. Behav. Human Decision Processes* 151:90–103.

Luo X, Tong S, Fang Z, Qu Z (2019) Frontiers: Machines vs. humans: The impact of artificial intelligence chatbot disclosure on customer purchases. *Marketing Sci.* 38(6):937–947.

Noy S, Zhang W (2023) Experimental evidence on the productivity effects of generative artificial intelligence. *Science* 381(6654):187–192.

Peng S, Kalliamvakou E, Cihon P, Demirer M (2023) The impact of AI on developer productivity: Evidence from GitHub Copilot. Working paper, arXiv:2302.06590.

Tong S, Jia N, Luo X, Fang Z (2021) The Janus face of artificial intelligence feedback: Deployment versus disclosure effects on employee performance. *Strategic Management J.* 42(9):1600–1631.

Wang W, Gao G, Agarwal R (2024) Friend or foe? Teaming between artificial intelligence and workers with variation in experience. *Management Sci.* 70(9):5753–5775.
