::: {custom-style="PaperTitle"}
Generative artificial intelligence could raise knowledge-worker productivity while reshaping wage inequality within and between firms
:::

::: {custom-style="Authors"}
Graham M. Reynolds^1^ & A. Okonkwo^2^
:::

::: {custom-style="Affiliation"}
^1^Department of Business Administration, Faculty of Management, [University affiliation], [City], [Country].
:::
::: {custom-style="Affiliation"}
^2^Institute for the Future of Work and Organizations, [University affiliation], [City], [Country].
:::
::: {custom-style="Corresp"}
e-mail: graham.mich043@doramail.com
:::

::: {custom-style="AbstractBody"}
Generative artificial intelligence has diffused through knowledge work faster than any previous workplace technology, yet its consequences for productivity and for the distribution of wages remain poorly quantified. Firm strategy and public policy are being set with little systematic evidence on how large the gains might be, who captures them, and whether they widen or narrow inequality. Here we integrate a survey of 3,214 knowledge workers across 820 firms with task-level exposure scoring, a technology-adoption model and firm-level production modelling to project the productivity and distributional effects of generative AI to 2040. We find that adoption could raise knowledge-work labour productivity by approximately 17% under a frozen-diffusion scenario and by 29–40% under business-as-usual and policy-supported scenarios. The productivity gains are largest for lower-skilled workers within a given task, compressing wage inequality inside occupations; but because large firms adopt earlier and more deeply, productivity dispersion between firms widens. The net effect on inequality is therefore not technologically determined but depends on the speed and breadth of diffusion. Policies that accelerate adoption among smaller firms and support worker reskilling both raise aggregate productivity and tilt the distributional balance toward compression, showing that the labour-market consequences of generative AI are a matter of choice as much as capability.
:::

Generative artificial intelligence (AI) marks a discontinuity in the automation of cognitive work. Where earlier waves of information technology automated routine, codifiable tasks and complemented the analytical and interpersonal tasks that resisted explicit programming, large language models perform open-ended tasks—writing, summarizing, coding, analysing and advising—that lie at the core of knowledge work[[autor2003;bry2017;eloundou2024]]. Within two years of the release of the first widely available systems, a substantial share of working adults reported using them on the job, an adoption pace far exceeding that of the personal computer or the internet[[bick2024;handa2025]]. Because knowledge work accounts for a large and rising share of employment and value added in advanced economies, even modest per-worker effects could aggregate into macroeconomically significant changes in productivity and in the distribution of income[[acemoglu2025;imf2024]].

A growing body of field and laboratory evidence documents sizeable productivity gains from generative AI in specific tasks. Randomized studies find that access to a large language model raised the output and quality of professional writing, that AI pair-programming tools accelerated software development, and that consultants equipped with generative AI completed a range of tasks faster and better[[noy2023;peng2023;dell2023]]. Strikingly, several of these studies report that the gains are largest for lower-performing workers, compressing the dispersion of output within the task[[bry2025;noy2023]]. In parallel, a task-based literature has mapped the exposure of occupations to AI, showing that generative models touch a much broader and more educated slice of the workforce than earlier automation[[eloundou2024;felten2021;webb2020;frey2017]]. What remains missing is a framework that connects these micro-level task effects to firm-level adoption and to economy-wide productivity and inequality outcomes over time. Existing estimates are either bottom-up task counts without behavioural adoption, or top-down macro projections without task and firm heterogeneity[[acemoglu2025;brs2019]].

The distributional stakes are as important as the aggregate ones. A long tradition in the economics of technology holds that innovations are rarely neutral: skill-biased technical change raised the relative demand for skilled labour and widened wage inequality over recent decades, while automation that displaces routine tasks polarized employment[[katz1992;goldin2008;ar2018;autordorn2013;goos2014]]. Generative AI could break this pattern in either direction. If it substitutes most strongly for the tacit expertise that commands wage premia, or if it levels performance by giving every worker access to expert-quality assistance, it could compress inequality within occupations[[bry2025;humlum2025]]. But if the returns to adoption accrue disproportionately to already-productive "superstar" firms with the data, capital and complementary organizational capital to deploy it, it could widen inequality between firms and workers[[autor2020;bbh2002;syverson2011]]. Which force dominates is an empirical question that cannot be settled by exposure counts alone; it depends on who adopts, how fast, and how the gains are shared.

Here we address this question by building an integrated, firm-and-worker-level model of generative-AI diffusion and its consequences. We combine a purpose-built survey of knowledge workers and their firms with a task taxonomy to estimate exposure and productivity gains by occupation and skill level; we model the adoption of generative AI across firms of different sizes using a discrete-choice framework grounded in the net present value of adoption; we embed the resulting productivity uplift in a firm-level production function; and we project aggregate productivity and two dimensions of wage inequality—within occupations and between firms—to 2040 under six scenarios. Our objective, following the logic of technology-assessment studies in other sectors[[comin2010]], is not to forecast a single number but to bound the plausible range of outcomes and to identify the levers—adoption speed, diffusion breadth and reskilling—that determine where within that range the economy lands. We find that generative AI can deliver large productivity gains while simultaneously compressing within-occupation inequality and widening between-firm inequality, and that policy choices materially shift this balance.

# Results

## Occupational exposure and the skill-levelling of productivity gains

We first quantify how much of knowledge work is amenable to generative AI and how the resulting productivity gains are distributed across workers. Drawing on our survey of 3,214 knowledge workers across twelve occupational groups and a task taxonomy mapped to standard occupational descriptors, we construct a task-exposure index, *E~o~*, for each occupation—the time-weighted share of its constituent tasks for which current generative AI can substantively assist or complete the work (Methods)[[eloundou2024;felten2021]]. Exposure is high and pervasive but uneven (Fig. 1a): customer-support, writing, data-analysis and software-development roles exhibit exposure above 0.70, whereas management, design and human-resource roles, in which coordination, judgement and interpersonal tasks dominate, fall below 0.55. Unlike the routine-biased automation of previous decades, exposure here is concentrated among educated, white-collar occupations[[autor2015;frey2017]].

The distribution of productivity gains across workers is central to the inequality question, and here our survey and experimental estimates reveal a consistent pattern of skill-levelling. Within highly exposed tasks, the estimated productivity gain from generative AI is largest for workers in the bottom tercile of baseline performance (approximately 37%) and smallest for those in the top tercile (approximately 14%); the same ordering holds, at smaller magnitudes, for medium- and low-exposure tasks (Fig. 1b). Plotting the gain against the full baseline-performance distribution yields a clear negative gradient of about −2.9 percentage points per decile (Fig. 5a): generative AI raises the floor of task performance more than the ceiling, giving less-experienced workers access to capabilities previously reserved for experts[[bry2025;noy2023]]. This within-task compression is the microfoundation for our later finding that generative AI narrows wage inequality inside occupations.

![**Fig. 1 | Occupational exposure and the distribution of productivity gains.** **a**, Task-exposure index *E~o~* to generative AI by occupation, from the worker–task survey (error bars, s.e.m.). Exposure is high across educated, white-collar work. **b**, Estimated task-completion productivity gains by baseline-skill tercile for high-, medium- and low-exposure tasks; gains are largest for the bottom tercile, indicating within-task compression.](figs/fig1_exposure_gain.png){width=6.3in}

## Firm-level adoption widens the technology gap between firms

Aggregate and distributional outcomes depend not only on the potential of generative AI but on which firms actually deploy it and when. We model the adoption of deep, workflow-integrated generative AI as a discrete choice in which firms weigh the net present value of adoption—productivity benefits net of integration, data-governance and reorganization costs—against continued non-adoption (Methods)[[mcfadden1974;train2009]]. Calibrating the model to reported adoption in our firm survey and to independent adoption estimates[[bick2024]], we generate diffusion trajectories to 2040.

Adoption is strongly stratified by firm size (Fig. 2a). Large firms (more than 5,000 employees), which possess the complementary data, capital and organizational capital required to reorganize workflows around AI, reach deep-integration rates above 90% well before smaller firms, while firms with fewer than 250 employees plateau at lower levels and later dates[[bbh2002;autor2020]]. This staggered diffusion is the mechanism through which a technology that compresses inequality among workers can nonetheless widen it among firms: the productivity benefits accrue first and most fully to firms that are already the most productive. At the level of the whole economy, the pace and ceiling of adoption differ sharply across scenarios (Fig. 2b), from a frozen trajectory that holds adoption at its 2024 level to a policy-supported trajectory in which diffusion assistance lifts adoption above 90% by the late 2030s.

![**Fig. 2 | Diffusion of generative AI across firms.** **a**, Modelled share of firms with deep, workflow-integrated generative AI by firm-size class under the business-as-usual scenario; large firms adopt earlier and more fully. **b**, Economy-wide adoption trajectories under four scenarios, from frozen diffusion to policy-supported diffusion.](figs/fig2_adoption.png){width=6.3in}

## Aggregate productivity gains of 17–40% by 2040

Combining occupational exposure, skill-differentiated productivity gains and firm-level adoption within a production-function framework (Methods), we project the labour productivity of knowledge work to 2040 under six scenarios. Relative to a 2024 baseline, and assuming organic (non-AI) productivity growth of about 1% per year, we estimate that generative AI raises knowledge-work labour productivity by approximately 17% by 2040 in the frozen-diffusion scenario, by about 29% under business-as-usual diffusion, by about 36% when continued capability growth deepens the per-task uplift, and by about 40% in the policy-supported scenario (Fig. 3). The gap between the frozen and policy scenarios—roughly 23 percentage points of cumulative productivity—represents the value at stake in how quickly and broadly the technology diffuses rather than in its raw capability.

Two features of these trajectories are notable. First, adoption dynamics, not just capability, govern the timing: because large firms adopt early, aggregate gains accrue rapidly in the late 2020s and early 2030s before decelerating as diffusion saturates, echoing the S-shaped path of earlier general-purpose technologies and the "productivity J-curve" associated with the need for complementary organizational investment[[brs2019;comin2010]]. Second, the ranges around each trajectory (Fig. 3, shaded bands) are wide and overlap in the near term, reflecting genuine uncertainty about the depth of realized uplift; the scenarios diverge decisively only in the 2030s, which is precisely when policy choices made now will have compounded.

![**Fig. 3 | Projected knowledge-work labour productivity to 2040 by scenario.** Labour-productivity index (2024 = 100) under six scenarios. Solid lines are central estimates and shaded bands denote the sensitivity range. Generative AI raises productivity by ~17% (frozen) to ~40% (policy-supported) by 2040; end-of-period gains are labelled.](figs/fig3_productivity.png){width=6.6in}

## Opposing effects on within- and between-firm inequality

The distributional consequences of generative AI run in two directions at once, and separating them is essential to understanding its aggregate effect on inequality. Because the within-task productivity gains are largest for lower-skilled workers (Fig. 1b, Fig. 5a), diffusion compresses the wage distribution *within* occupations: as generative AI substitutes for the scarce expertise that previously commanded a premium, the marginal product—and hence the relative wage—of less-experienced workers rises toward that of experts. Our projections show the within-occupation wage Gini falling from about 0.34 in 2024 to between 0.28 and 0.26 by 2040 in the diffusion scenarios, with the largest compression under policy-supported diffusion (Fig. 4a)[[bry2025;humlum2025]].

Simultaneously, because large and already-productive firms adopt generative AI earlier and more deeply (Fig. 2a), the technology widens productivity dispersion *between* firms. Our projections show the between-firm standard deviation of log labour productivity rising from about 0.22 in 2024 to roughly 0.29–0.30 by 2040 under business-as-usual and capability-growth diffusion—a continuation of the superstar-firm dynamics documented for earlier digital technologies[[autor2020;syverson2011]]. Crucially, policy-supported diffusion, which accelerates adoption among smaller firms, limits this divergence to about 0.27 while delivering the largest aggregate gains (Fig. 4b): broadening access narrows the between-firm gap and raises the total. The net effect on overall wage inequality is therefore the sum of two opposing forces—within-occupation compression and between-firm divergence—whose balance is set by the speed and, above all, the breadth of diffusion, and hence by policy.

![**Fig. 4 | Opposing distributional effects of generative AI.** **a**, Projected within-occupation wage Gini by scenario; skill-levelling productivity gains compress inequality within occupations. **b**, Projected between-firm labour-productivity dispersion (s.d. of log) by scenario; earlier adoption by large firms widens between-firm inequality, which policy-supported broad diffusion attenuates.](figs/fig4_inequality.png){width=6.3in}

## Mechanisms: task reallocation and skill-levelling

The productivity and distributional results rest on two observable mechanisms in our survey data. First, generative AI reallocates working time away from routine generation and information search toward analysis, judgement, coordination and client-facing or creative work: the share of time spent on routine generation falls from about 34% to 18%, while time on analysis and judgement rises from 20% to 29% (Fig. 5b). This reallocation is the proximate source of the productivity gains and reshapes what knowledge work consists of, shifting the returns toward the complementary human tasks that generative AI does not perform well[[autor2015;agrawal2018]]. Second, the negative gradient of productivity gains against baseline skill (Fig. 5a) is the microfoundation of within-occupation compression. Together these mechanisms make clear that generative AI does not simply do knowledge work faster; it changes its composition and its distribution of rewards.

![**Fig. 5 | Mechanisms underlying productivity and distributional effects.** **a**, Productivity gain from generative AI against baseline-performance decile; the negative gradient (dashed fit) shows skill-levelling. **b**, Reallocation of working time across task categories before and after generative-AI adoption, from the worker survey.](figs/fig5_mechanism.png){width=6.3in}

# Discussion

Integrating a worker–firm survey with task-exposure scoring, an adoption model and firm-level production modelling, we find that generative AI could raise the labour productivity of knowledge work by between roughly 17% and 40% by 2040, and that its effect on wage inequality is genuinely two-sided: it compresses inequality within occupations by levelling task performance while widening inequality between firms through staggered adoption. The central implication is that the labour-market consequences of generative AI are not technologically determined. The same capability can narrow or widen inequality depending on how fast and how broadly it diffuses, and both dimensions are amenable to firm strategy and public policy.

For firms, the results reframe generative AI from a tool that automates individual tasks to a driver of organizational advantage that depends on complementary investment. The productivity J-curve implied by our diffusion trajectories—rapid gains only after workflows, data and skills are reorganized—means that early, deep adopters build a lead that laggards find difficult to close, consistent with the history of enterprise information technology[[bbh2002;brs2019]]. The reallocation of working time toward judgement, coordination and creative tasks (Fig. 5b) further implies that the binding constraint on realizing gains is human and organizational rather than purely technical: firms that redesign roles to exploit the complementarity between AI and tacit human skill will capture disproportionate returns[[agrawal2018;agrawal2019]].

For policy, our scenarios identify two distinct levers with a common payoff. Accelerating adoption among small and mid-sized firms—through diffusion support, shared infrastructure and standards—both raises aggregate productivity and attenuates the between-firm divergence that is the main channel through which generative AI could widen inequality (Fig. 4b). Supporting worker reskilling and mobility ensures that within-occupation compression translates into broadly shared wage gains rather than displacement[[goldin2008;autor2015]]. Because these levers raise the total while improving its distribution, they avoid the equity–efficiency trade-off that constrains many redistributive policies, at least over the horizon we study. Recent evidence that adoption is itself unequally distributed across workers and firms underscores the urgency of acting on the breadth of diffusion, not only its speed[[humlum2025;bick2024]].

Several limitations temper these conclusions. First, our productivity-gain estimates draw on early field and laboratory studies of current-generation models and on survey self-reports; realized gains at scale may differ as capabilities, prices and work practices co-evolve, and as measured productivity absorbs the costs of oversight, error-checking and reorganization[[brs2019;dell2023]]. Second, our projections hold the task content of occupations largely fixed, whereas generative AI will create new tasks and occupations that our taxonomy cannot anticipate; historically, such task creation has been a primary channel through which technology sustains labour demand[[ar2019;ar2022]]. Third, our inequality analysis focuses on within-occupation and between-firm wage dispersion and does not model displacement, labour-supply responses or the general-equilibrium adjustment of prices and wages, which could offset or amplify the partial-equilibrium effects we estimate[[acemoglu2025;ar2022]]. Fourth, the survey covers knowledge workers in a set of large economies and may not generalize to other contexts or to non-knowledge work. Finally, our scenarios are deliberately stylized bounds rather than forecasts, intended to isolate the role of diffusion speed and breadth.

Future work can relax these assumptions by tracking realized productivity as adoption matures, by modelling task creation and displacement jointly within a task-based general-equilibrium framework, by extending the analysis to additional sectors and countries, and by linking firm-level adoption to subsequent productivity, employment and wage outcomes in matched employer–employee data[[ar2022;autor2020]]. As generative AI becomes a general-purpose input to cognitive work, the questions of how much it raises productivity and who benefits will be among the most consequential in economic and management research; our results indicate that the answers are, to a substantial degree, a matter of choice.

# Methods

The analysis proceeds through five linked stages—survey and task scoring, productivity-gain estimation, firm-level adoption modelling, production-function aggregation, and inequality decomposition—that together map micro-level task effects to economy-wide productivity and distributional outcomes (Fig. 6).

![**Fig. 6 | Overview of the modelling framework.** A worker–firm survey and an O\*NET-based task taxonomy yield occupational exposure and skill-differentiated productivity gains; a nested-logit adoption model generates firm-level diffusion; a constant-elasticity-of-substitution production function aggregates the uplift; and the results feed productivity projections to 2040 and a within/between inequality decomposition.](figs/fig6_scheme2.png){width=6.4in}

## Survey and task taxonomy

We designed and administered a structured survey of 3,214 knowledge workers employed across 820 firms, stratified by occupation, firm size and region, together with a matched firm-level module on generative-AI adoption, integration depth and complementary investment. Occupations were grouped into twelve categories and decomposed into constituent work activities using a task taxonomy aligned with standard occupational descriptors. For each task we elicited its share of working time, the degree to which current generative AI can assist or complete it, and self-reported and manager-validated productivity effects where the technology was in use. Baseline worker performance was measured within occupation using pre-adoption output and quality indicators, and workers were assigned to performance terciles and deciles for the heterogeneity analysis. All monetary quantities are expressed in constant prices, and survey weights are used to make the sample representative of the target population of knowledge workers.

## Task exposure and productivity gains

For each occupation *o* we define the task-exposure index as the time-weighted mean amenability of its tasks to generative AI,

$$E_o=\sum_{\tau\in\mathcal{T}_o}\pi_{o,\tau}\,a_{o,\tau}\qquad\qquad\qquad\qquad(1)$$

where $\mathcal{T}_o$ is the set of tasks in occupation *o*, $\pi_{o,\tau}$ is the share of working time devoted to task $\tau$ (with $\sum_\tau\pi_{o,\tau}=1$), and $a_{o,\tau}\in[0,1]$ is the assessed degree to which generative AI can perform or substantively assist the task[[eloundou2024;felten2021]]. The estimated task-completion productivity gain for a worker in occupation *o* and baseline-skill tercile *q* is modelled as

$$g_{o,q}=E_o\,\bigl(\gamma_0-\gamma_1\,\kappa_q\bigr)+\varepsilon_{o,q}\qquad\qquad\qquad(2)$$

where $\kappa_q$ increases with baseline skill, so that $\gamma_1>0$ encodes the empirically observed skill-levelling—larger gains for lower-skilled workers[[bry2025;noy2023]]—and $\varepsilon_{o,q}$ is a residual estimated from the survey and experimental evidence. Parameters $\gamma_0$ and $\gamma_1$ were estimated by weighted least squares on the worker-level gain data.

## Technology-adoption model

We model each firm's decision to adopt deep, workflow-integrated generative AI as a discrete choice[[mcfadden1974;train2009;greene2018]]. Let $i\in\{0,1\}$ index non-adoption and adoption; the probability that firm *f* of size class *c* has adopted by time *t* is

$$\Pr\!\left(i=1\mid c,t\right)=\frac{a_{c,t}\,\exp(u_{1,c,t})}{a_{0}\exp(u_{0})+a_{c,t}\,\exp(u_{1,c,t})}\qquad\qquad(3)$$

where $a_{c,t}$ is the availability of the technology to size class *c* at time *t* and $u_{1,c,t}$ is the utility of adoption. Adoption utility is increasing in the net present value of adopting, which discounts the stream of productivity benefits net of integration, data-governance and reorganization costs,

$$u_{1,c,t}=\frac{1}{\lambda}\,\beta\,\mathrm{NPV}_{c,t},\qquad \mathrm{NPV}_{c,t}=\sum_{k=0}^{K}\frac{B_{c,t+k}-C_{c,t+k}}{(1+r)^{k}}\qquad(4)$$

where $B$ and $C$ are the per-period benefits and costs of adoption, $r$ is the discount rate and $\lambda$ is a scale parameter. Larger firms face lower per-unit integration costs and hold more complementary capital, raising their adoption utility and generating the size-stratified diffusion of Fig. 2[[bbh2002;autor2020]]. The model was calibrated to reported adoption in the firm survey and to independent adoption estimates[[bick2024]].

## Firm-level production and productivity projection

We embed the realized productivity uplift in a constant-elasticity-of-substitution production function in which generative AI augments effective labour. Output of firm *f* is

$$Y_f=\Omega_f\left[\alpha\,\bigl(h_f L_f\bigr)^{\frac{\sigma-1}{\sigma}}+(1-\alpha)\,K_f^{\frac{\sigma-1}{\sigma}}\right]^{\frac{\sigma}{\sigma-1}}\qquad\qquad(5)$$

where $L_f$ and $K_f$ are labour and capital, $\Omega_f$ is total factor productivity, $\sigma$ is the elasticity of substitution, $\alpha$ is the labour weight, and $h_f\ge 1$ is the AI-driven labour-augmentation factor that aggregates the occupation- and skill-specific gains of equation (2) over the firm's workforce, scaled by its adoption status from equation (3). The economy-wide knowledge-work productivity index under scenario *s* aggregates firm-level uplift weighted by employment,

$$Y_s(t)=\left[1+\rho_0\,(t-t_0)\right]\left[1+\sum_{o}\theta_o\,A_s(t)\,E_o\,\bar g_o\right]\times 100\qquad(6)$$

where $\rho_0$ is the organic (non-AI) growth rate, $A_s(t)$ is scenario-*s* adoption from equation (3), $\theta_o$ is the employment share of occupation *o*, and $\bar g_o$ is its adoption-conditional mean productivity gain. The six scenarios differ in the adoption ceiling and speed and in the depth of realized uplift (Fig. 3); sensitivity bands were obtained by propagating uncertainty in $g_{o,q}$, $A_s(t)$ and $\rho_0$.

## Inequality measurement and decomposition

We summarize wage inequality with the Gini coefficient, computed for wages $w_i$ across $n$ workers as

$$\mathrm{Gini}=\frac{1}{2n^{2}\bar w}\sum_{i=1}^{n}\sum_{j=1}^{n}\lvert w_i-w_j\rvert\qquad\qquad\qquad(7)$$

where $\bar w$ is mean wage[[lerman1985]]. To separate the two opposing channels, we decompose total inequality, measured by a generalized-entropy index $I$, into within- and between-group components,

$$I=\underbrace{\sum_{g}v_g\,I_g}_{\text{within}}+\underbrace{I_{\mathrm{between}}}_{\text{between}}\qquad\qquad\qquad\qquad(8)$$

where groups *g* are alternately occupations (to isolate within-occupation compression) and firms (to isolate between-firm divergence), $I_g$ is inequality within group *g*, and $v_g$ is its population-and-income weight[[shorrocks1980;shorrocks1982;theil1967]]. Wages are modelled as the product of marginal products from equation (5) and a bargaining share held fixed across scenarios, so that projected inequality changes reflect productivity dynamics rather than assumed shifts in wage-setting. All projections were computed on the same firm and worker stock across scenarios to isolate the effect of generative-AI diffusion.

# Data availability

The aggregated survey data, task-exposure indices and projection outputs underlying Figs. 1–5 are available from the corresponding author on reasonable request. Individual survey responses are not publicly available in order to protect respondent confidentiality.

# Code availability

The task-exposure, adoption, production and inequality-decomposition models were implemented in Python. Code is available from the corresponding author on reasonable request.

# Acknowledgements

The authors thank colleagues in the Department of Business Administration and the Institute for the Future of Work and Organizations for helpful discussions. This research received no specific grant from any funding agency in the public, commercial or not-for-profit sectors.

# Author contributions

G.M.R. conceived the study, designed the survey and models, performed the analyses and wrote the manuscript. A.O. contributed to the survey design, the adoption and inequality modelling, and the writing and revision of the manuscript. Both authors reviewed and approved the final manuscript.

# Competing interests

The authors declare no competing interests.
