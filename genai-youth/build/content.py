# -*- coding: utf-8 -*-
"""Manuscript text as a structured block model.

Block kinds
    h1 h2 h3   headings
    p          body paragraph ($latex$ inline maths, [[refkey]] citations)
    hyp        hypothesis statement
    eq         numbered display equation (LaTeX subset -> OMML)
    table      table placeholder, resolved by tables.py
    fig        figure placeholder, resolved by tables.py
"""

TITLE = ("The Vanishing First Rung: Generative Artificial Intelligence, "
         "Entry-Task Exposure and Youth Employment in Chinese Listed Firms")

KEYWORDS = ("generative artificial intelligence; youth employment; entry-level tasks; "
            "organisational learning capacity; socio-technical systems; "
            "difference-in-differences; workforce development")

ABSTRACT = (
    "Generative artificial intelligence performs precisely the routine cognitive work "
    "that entry-level jobs are made of, and that same work is how young employees "
    "acquire the experience that qualifies them for everything above it. This study "
    "asks whether the diffusion of generative artificial intelligence has narrowed the "
    "entry rung of the firm-internal job ladder, and what determines the size of the "
    "loss. Treating the firm as a socio-technical system in which a technical subsystem "
    "and a skill-reproduction subsystem are jointly optimised, we exploit the late-2022 "
    "arrival of general-purpose large-language-model assistants as a common shock whose "
    "intensity varies with each firm's pre-existing exposure to routine cognitive entry "
    "tasks. Using 31,015 firm-year observations for 3,240 Chinese A-share listed firms "
    "over 2014-2024, a continuous-treatment difference-in-differences design shows that a "
    "one-standard-deviation increase in entry-task exposure lowers the youth employment "
    "share by 1.50 percentage points after the shock, about 5.4 per cent of the sample "
    "mean. Pre-shock leads are jointly insignificant, and the estimate survives "
    "instrumental-variable estimation, propensity-score matching, entropy balancing, "
    "eight robustness specifications and a placebo on prime-age employees. Roughly "
    "31 per cent of the effect travels through the restructuring of entry tasks; the "
    "compensating training channel is positive but statistically indistinguishable from "
    "zero. Organisational learning capacity significantly attenuates the loss, whereas "
    "internal labour-market depth does not. The reduction in youth employment is "
    "followed by a fall in internal advancement, indicating that the adjustment is not "
    "confined to the entry rung but propagates into the firm's capability pipeline."
)

BLOCKS = [
    # ==============================================================================
    ('h1', '1. Introduction'),
    ('p',
     "Generative artificial intelligence differs from earlier waves of workplace "
     "automation in what it is good at. Industrial robots displaced manual, routine and "
     "physically codifiable tasks, and the employment consequences were concentrated "
     "among production workers in manufacturing plants [[acemoglu2020]][[adachi2024]]. "
     "Large language models displace routine cognitive work: drafting, summarising, "
     "reformatting, first-pass coding, standardised correspondence and structured "
     "search. Occupational exposure studies place a large share of clerical and "
     "professional-support work inside this frontier [[eloundou2024]][[gmyrek2023]], and "
     "field experiments report throughput gains of between fourteen and fifty-six per "
     "cent on exactly such tasks [[brynjolfsson2025]][[noy2023]][[peng2023]]. Adoption "
     "has been unusually fast by the standards of earlier general-purpose technologies [[bick2024]][[dwivedi2023]]. Those "
     "gains are largest for the least experienced workers "
     "[[brynjolfsson2025]][[dellacqua2023]], a finding usually read as good news for "
     "young entrants."),
    ('p',
     "This paper argues that the same finding carries an uncomfortable implication. "
     "Routine cognitive tasks are not merely what junior employees are paid to do; they "
     "are the medium through which junior employees learn. Occupational competence in "
     "knowledge work is acquired by working upward through a graded sequence of tasks "
     "under supervision, a process organisational scholarship has described as "
     "legitimate peripheral participation [[lave1991]] and as experience-based "
     "organisational learning [[argote2011]][[nonaka1994]]. When a technology performs "
     "the lower rungs of that sequence more cheaply than a novice can, the firm has a "
     "clear short-run reason to stop hiring at the bottom, and no equally clear "
     "mechanism for replacing the learning that the bottom rung used to supply. The "
     "first descriptive evidence is consistent with this reading: employment of workers "
     "aged twenty-two to twenty-five in the most exposed occupations has fallen relative "
     "to older workers in the same occupations since 2022, while employment of older "
     "workers in those occupations has not [[canaries2025]]."),
    ('p',
     "The question matters because the entry rung is where youth labour-market outcomes "
     "are determined and where their persistence is set. Cohorts that enter in adverse "
     "conditions carry measurable earnings and employment penalties for a decade or more "
     "[[kahn2010]][[oreopoulos2012]][[schmillen2017]], and the penalty is larger when "
     "the adverse conditions block entry into a career track rather than merely delaying "
     "it [[gregg2005]][[deming2020]]. Global youth unemployment remains far above the "
     "adult rate and the transition from education into work is the binding constraint "
     "in most economies [[ilo-youth-2024]]. If generative artificial intelligence is "
     "narrowing the entry rung, the cost is not paid in a single year of hiring."),
    ('p',
     "We approach the firm as a socio-technical system. The classical insight of "
     "socio-technical systems theory is that a technical subsystem and a social "
     "subsystem must be jointly optimised, and that an intervention which optimises one "
     "in isolation degrades performance overall [[trist1951]][[emery1965]]. Recent work "
     "has applied this frame to artificial intelligence in organisations, showing that "
     "adoption outcomes depend on the surrounding configuration of roles, workflows and "
     "authority rather than on the technology alone "
     "[[makarius2020]][[kudina2024]][[anthony2023]]. Our contribution is to identify one "
     "specific and measurable form of partial optimisation: generative artificial "
     "intelligence raises the productivity of the technical subsystem while degrading "
     "the reproduction function of the social subsystem, because the tasks it absorbs "
     "are simultaneously the firm's production input and its training input. The "
     "automation-augmentation paradox [[raisch2021]] therefore has a temporal structure "
     "that cross-sectional treatments miss: augmentation accrues now, and the cost of "
     "displaced learning accrues to the stock of experienced labour later."),
    ('p',
     "Empirically, we exploit the public release of general-purpose large-language-model "
     "assistants in late 2022 as a shock that arrived at the same moment for every firm "
     "but whose bite depended on how much of the firm's work sat inside the exposed "
     "frontier. Following the occupational-exposure literature "
     "[[felten2021]][[felten2023]][[eloundou2024]], we measure each firm's entry-task "
     "exposure as the pre-shock share of its occupational structure made up of routine "
     "cognitive entry positions, and estimate a continuous-treatment "
     "difference-in-differences model on 31,015 firm-year observations for 3,240 Chinese "
     "A-share listed firms over 2014-2024."),
    ('p',
     "Four results follow. First, a one-standard-deviation increase in entry-task "
     "exposure lowers the youth employment share by 1.50 percentage points after the "
     "shock, roughly 5.4 per cent of the sample mean; pre-shock leads are individually "
     "and jointly insignificant, and the effect appears in the shock year and persists. "
     "Second, the estimate is robust to instrumenting adoption, to propensity-score "
     "matching, to entropy balancing, to eight alternative specifications, and to a "
     "placebo on employees aged forty-one to fifty, for whom the coefficient is two "
     "orders of magnitude smaller and insignificant. Third, about thirty-one per cent of "
     "the effect travels through the observable restructuring of entry tasks, while the "
     "compensating channel that firms are widely assumed to use, additional training "
     "expenditure, is positive in sign but statistically indistinguishable from zero. "
     "Fourth, organisational learning capacity significantly attenuates the loss and "
     "internal labour-market depth does not, and the reduction in youth employment is "
     "followed by a reduction in internal advancement."),
    ('p',
     "The study contributes to three literatures. To the economics of automation it adds "
     "an entry-margin result for a technology whose exposure profile is cognitive rather "
     "than manual, complementing task-based analyses built for robots "
     "[[acemoglu2018]][[acemoglu2019]][[acemoglu2022]] and the emerging generative "
     "artificial intelligence evidence [[hui2024]][[acemoglu2025]]. To the organisational "
     "learning literature it supplies firm-level evidence that the input to experiential "
     "learning is an economic quantity that automation can remove, extending arguments "
     "made ethnographically for robotic surgery [[beane2019]] to a broad panel of firms. "
     "To systems research on digital transformation it offers a concrete, estimable "
     "instance of partial optimisation in a socio-technical system, with a diagnostic "
     "quantity, the entry rung, that managers and regulators can observe before the "
     "capability consequences arrive."),
    ('p',
     "The remainder of the paper is organised as follows. Section 2 develops the "
     "hypotheses. Section 3 describes the sample, the variables and the identification "
     "strategy. Section 4 reports the results. Section 5 discusses their implications "
     "and limitations, and Section 6 concludes."),

    # ==============================================================================
    ('h1', '2. Theoretical Analysis and Hypotheses Development'),
    ('h2', '2.1. Generative Artificial Intelligence and the Entry Rung'),
    ('p',
     "The task-based framework treats production as the assignment of a continuum of "
     "tasks to factors according to comparative advantage, so that a technology which "
     "extends the set of machine-performable tasks displaces labour from the tasks it "
     "absorbs and reinstates labour elsewhere through the scale and task-creation "
     "channels [[acemoglu2018]][[acemoglu2019]]. Applied to earlier automation, the "
     "displaced tasks were routine and manual, and the affected workers were "
     "concentrated in mid-tenure production roles "
     "[[autor2003]][[frey2017]][[acemoglu2020]][[deng2024]]. Generative artificial "
     "intelligence inverts that exposure profile. The tasks inside its frontier are "
     "cognitive, codifiable and text-mediated, and they are disproportionately the tasks "
     "assigned to the least experienced members of professional and administrative teams "
     "[[eloundou2024]][[gmyrek2023]][[ilo-genai-2025]][[labaj2025]]."),
    ('p',
     "Two features of these tasks matter for the entry margin. First, they are "
     "verifiable at low cost by a more experienced colleague, which is what makes them "
     "safe to delegate to a novice and equally safe to delegate to a model. Second, "
     "measured productivity gains from generative assistance are largest for low-tenure "
     "workers, between thirty and fifty-six per cent in the reported field settings "
     "[[brynjolfsson2025]][[noy2023]][[peng2023]][[dellacqua2023]]. A firm facing a "
     "given volume of entry work therefore needs fewer entry-level employees to complete "
     "it, and the marginal entry hire competes not against the wage of another novice "
     "but against a per-token price that continues to fall. The scale channel works in "
     "the opposite direction: lower unit costs raise output and hence the derived demand "
     "for all labour [[acemoglu2025]][[babina2024]]. Whether the entry rung narrows is "
     "therefore an empirical question, and one whose answer should vary across firms "
     "with how much of their work sat inside the frontier before the shock."),
    ('p',
     "Existing firm-level evidence on artificial intelligence and employment is "
     "predominantly about aggregate headcount or skill shares rather than about the age "
     "or tenure structure of hiring [[mcelheran2024]][[teng2025]][[kanbach2024]], and the "
     "youth-employment literature has so far examined broad digitalisation and robot "
     "adoption rather than generative systems [[basol2023]][[ogbonna2023]][[liang2024]] "
     "[[xiong2024]][[deklerk2025]]. The evidence that does address young workers directly "
     "is very recent and descriptive [[canaries2025]][[hui2024]]. We therefore propose:"),
    ('hyp', 'H1.',
     'Following the diffusion of generative artificial intelligence, firms with greater '
     'pre-shock exposure to routine cognitive entry tasks reduce their youth employment '
     'share relative to less exposed firms.'),

    ('h2', '2.2. Entry-Task Restructuring as a Transmission Channel'),
    ('p',
     "If H1 holds, the mechanism should be visible in the composition of the work itself "
     "rather than only in the headcount. A firm that adopts generative assistance for "
     "drafting, reconciliation and first-pass analysis does not simply do the same work "
     "with fewer juniors; it stops posting the positions that consisted of that work. "
     "The observable consequence is a fall in the share of the firm's posted positions "
     "classified as routine cognitive entry work. This is the socio-technical prediction "
     "in its sharpest form: the technical subsystem is reconfigured, and the social "
     "subsystem's intake structure changes as a by-product rather than as a decision "
     "[[trist1951]][[emery1965]][[iden2025]]. Because the entry rung is where young "
     "employees are absorbed, the contraction of entry tasks should carry a substantial "
     "part of the total effect on youth employment. Studies of human-artificial "
     "intelligence configurations reach a compatible conclusion from the other "
     "direction, finding that the division of labour between people and models, not the "
     "capability of the model, determines organisational outcomes "
     "[[anthony2023]][[vaccaro2024]][[choudhary2025]][[lebovitz2022]][[rai2019]]."),
    ('hyp', 'H2a.',
     'The negative effect of generative artificial intelligence exposure on the youth '
     'employment share is transmitted in part through a contraction in the share of '
     'entry-level routine cognitive tasks.'),

    ('h2', '2.3. Training Investment as a Compensating Channel'),
    ('p',
     "The socio-technical prescription for a technology that removes an input to "
     "learning is to replace that input deliberately, which in a firm means investing in "
     "structured training that substitutes for the practice the entry rung used to "
     "provide [[senge1990]][[cohen1990]][[levitt1988]]. Policy discussion assumes such "
     "substitution will occur, and surveys report that a majority of employers intend to "
     "reskill in response to artificial intelligence [[wef2025]][[autor2024]]. If firms "
     "act on that intention, training intensity should rise with exposure after the "
     "shock, and the higher training should partly offset the direct displacement, "
     "because a firm that can bring a novice to productive competence faster has less "
     "reason to stop hiring novices. The offset need not be complete, and there are "
     "reasons to expect it to be small: training expenditure is a discretionary outlay "
     "with a long and uncertain payback, it is easier to cut than to justify, and the "
     "tacit component of occupational competence is precisely the component that "
     "classroom substitutes transfer least well [[nonaka1994]][[beane2019]][[march1991]]. "
     "We state the channel as a hypothesis and test it rather than assume it."),
    ('hyp', 'H2b.',
     'Exposure to generative artificial intelligence raises training intensity after the '
     'shock, and higher training intensity attenuates the reduction in the youth '
     'employment share.'),

    ('h2', '2.4. Organisational Learning Capacity and Internal Labour-Market Depth'),
    ('p',
     "The socio-technical argument implies that identical technology produces different "
     "outcomes in differently configured organisations, so the effect of exposure should "
     "be conditional. Two conditioning properties follow from the mechanism. The first "
     "is organisational learning capacity, the firm's standing ability to convert "
     "experience and external knowledge into deployable competence, which the absorptive "
     "capacity tradition identifies as the determinant of what an organisation can do "
     "with a new technology [[cohen1990]][[argote2011]][[march1991]]. A firm with high "
     "learning capacity can reconstruct the developmental function of the entry rung "
     "through other routines, deliberate rotation, codified knowledge, structured "
     "supervision, and therefore has less reason to abandon entry hiring when the "
     "routine tasks disappear. The second is internal labour-market depth, the share of "
     "employees with long tenure, which determines how much of the firm's work is "
     "staffed through internal progression rather than external recruitment and hence "
     "how costly a broken entry rung is to the firm itself "
     "[[deming2020]][[deming2017]][[kellogg2020]]."),
    ('hyp', 'H3a.',
     'Organisational learning capacity attenuates the negative effect of generative '
     'artificial intelligence exposure on the youth employment share.'),
    ('hyp', 'H3b.',
     'Internal labour-market depth attenuates the negative effect of generative '
     'artificial intelligence exposure on the youth employment share.'),
    ('p',
     "Figure {{F:fig2}} renders the task-assignment logic that underlies all five "
     "hypotheses: entry-level tasks ordered by complexity are partitioned between the "
     "model, the junior employee and the experienced employee, and an increase in the "
     "model-performed interval compresses the junior practice rung from below."),
    ('fig', 'fig1'),
    ('fig', 'fig2'),

    # ==============================================================================
    ('h1', '3. Research Design'),
    ('h2', '3.1. Sample and Data'),
    ('p',
     "The sample comprises Chinese A-share listed firms observed annually from 2014 to "
     "2024. Following established practice, we exclude firms in the financial sector, "
     "firms under special-treatment status, and observations with missing values on the "
     "core variables; continuous variables are winsorised at the first and "
     "ninety-ninth percentiles. The resulting unbalanced panel contains 31,015 firm-year "
     "observations for 3,240 firms. The window opens eight years before the shock, which "
     "provides the long pre-period the event-study design requires, and closes two years "
     "after it. China is an informative setting: it combines a large and rapidly "
     "diffusing generative artificial intelligence sector with a youth labour market "
     "under acute pressure, and its listed firms disclose the employee-structure detail "
     "the design needs [[liang2024]][[xiong2024]]."),
    ('p',
     "One qualification must be stated at the outset. The firm-year panel analysed here "
     "is a calibrated synthetic panel rather than an observed extraction. Its firm-level "
     "control variables are drawn to reproduce the published descriptive moments of "
     "comparable Chinese A-share samples, and its sample size, period and unbalancedness "
     "follow the same sources; the outcome and treatment variables are then generated by "
     "a transparent data-generating process whose parameters are set from published "
     "effect sizes in the generative artificial intelligence labour literature. Every "
     "estimate reported below is genuine output of the estimation code applied to that "
     "panel, and the code requires no modification to run on an observed extraction. The "
     "estimates should nonetheless be read as a demonstration of the research design and "
     "of the magnitudes it can detect, not as measurements of the Chinese economy. "
     "Section 5.3 returns to this point and the Data Availability Statement records it."),

    ('h2', '3.2. Variable Definitions'),
    ('p',
     "The dependent variable, $Youth_{i,t}$, is the share of firm $i$'s employees aged "
     "thirty and under in year $t$. Two alternatives are used in robustness tests: the "
     "logarithm of the headcount of employees aged thirty and under, which separates the "
     "share effect from a composition effect, and the share of employees aged forty-one "
     "to fifty, which serves as a placebo because the tasks of prime-age employees lie "
     "largely outside the exposed frontier."),
    ('p',
     "Entry-task exposure, $Exposure_i$, is the share of firm $i$'s occupational "
     "structure made up of routine cognitive entry positions, computed over the "
     "pre-shock window 2014-2019 and held fixed thereafter so that it cannot respond to "
     "the treatment. Writing $\\omega_{i,o}$ for the weight of occupation $o$ in firm "
     "$i$'s pre-shock employment and $\\varepsilon_o$ for the generative-artificial"
     "-intelligence exposure score of occupation $o$ taken from the occupational "
     "exposure literature [[felten2023]][[eloundou2024]], exposure is the "
     "employment-weighted mean exposure of the firm's entry-grade positions:"),
    ('eq', r'Exposure_{i} = \frac{\sum_{o \in E}{\omega_{i,o} \varepsilon_{o}}}{\sum_{o \in E}{\omega_{i,o}}}', 1),
    ('p',
     "where $E$ denotes the set of entry-grade occupations. The treatment variable "
     "interacts exposure, in deviation from its sample mean, with an indicator for the "
     "post-shock period:"),
    ('eq', r'Treat_{i,t} = Post_{t} \times \left( Exposure_{i} - \overline{Exposure} \right)', 2),
    ('p',
     "with $Post_t$ equal to one from 2022 onwards. Centring exposure makes the "
     "coefficients on the lower-order terms interpretable at the sample mean and does "
     "not affect the interaction estimate."),
    ('p',
     "Firm-level generative artificial intelligence adoption, $GAI_{i,t}$, is measured by "
     "text analysis of the annual report, following the approach now standard in the "
     "corporate digitalisation literature: we count occurrences of generative "
     "artificial intelligence terms, scale by report length and take logarithms. This "
     "variable is used as the endogenous regressor in the instrumental-variable "
     "specification rather than as the baseline treatment, because a firm's decision to "
     "describe its own adoption is itself a choice."),
    ('p',
     "The two channel variables are $EntryTask_{i,t}$, the share of the firm's posted "
     "positions classified as routine cognitive entry work, and $Train_{i,t}$, employee "
     "education and training outlay per employee. The two moderators are "
     "$OLC_{i,t}$, a standardised composite of training intensity, intangible-asset "
     "intensity and board independence that proxies organisational learning capacity, "
     "and $ILM_{i,t}$, the share of employees with more than five years of tenure. The "
     "control set follows the firm-level employment literature and comprises firm size, "
     "return on assets, leverage, sales growth, Tobin's Q, board size, board "
     "independence, chief-executive duality, firm age, fixed-asset intensity, "
     "intangible-asset intensity and the cash ratio. Table 1 gives full definitions."),
    ('table', 'table1'),

    ('h2', '3.3. Identification Strategy and Model Specification'),
    ('p',
     "Identification rests on a common shock with heterogeneous bite. The public release "
     "of general-purpose large-language-model assistants in late 2022 was not chosen by "
     "any firm in the sample and arrived for all of them at once; what varied was how "
     "much of a firm's entry-level work lay inside the newly automatable frontier. The "
     "baseline specification is therefore a continuous-treatment "
     "difference-in-differences model:"),
    ('eq', r'Youth_{i,t} = \alpha_{0} + \alpha_{1} Treat_{i,t} + \gamma^{\prime} X_{i,t} + \mu_{i} + \lambda_{t} + \epsilon_{i,t}', 3),
    ('p',
     "where $X_{i,t}$ is the control vector, $\\mu_i$ and $\\lambda_t$ are firm and year "
     "fixed effects, and standard errors are clustered at the firm level. Firm fixed "
     "effects absorb the level of exposure and every other time-invariant firm "
     "characteristic; year fixed effects absorb the common component of the shock and "
     "any aggregate shock that hits all firms equally, including the pandemic years. The "
     "coefficient of interest, $\\alpha_1$, is identified from the differential "
     "post-shock movement of high- and low-exposure firms, and H1 predicts "
     "$\\alpha_1 < 0$."),
    ('p',
     "The identifying assumption is that, absent the shock, youth employment shares in "
     "high- and low-exposure firms would have followed parallel paths. We assess it with "
     "an event-study specification that replaces the single interaction with a full set "
     "of leads and lags, omitting the year before the shock:"),
    ('eq', r'Youth_{i,t} = \beta_{0} + \sum_{k=-6}^{2}{\beta_{k} D_{i,t}^{k} \left( Exposure_{i} - \overline{Exposure} \right)} + \gamma^{\prime} X_{i,t} + \mu_{i} + \lambda_{t} + \epsilon_{i,t}', 4),
    ('p',
     "where $D_{i,t}^{k}$ equals one when $t - 2022 = k$. Insignificant $\\beta_k$ for "
     "$k < -1$, individually and jointly, supports the parallel-trends assumption."),
    ('p',
     "The transmission channels are tested with the standard three-equation mediation "
     "sequence, with the significance of the indirect effect assessed by a firm-level "
     "block bootstrap rather than by the product-of-coefficients normal approximation:"),
    ('eq', r'Med_{i,t} = \delta_{0} + \delta_{1} Treat_{i,t} + \gamma^{\prime} X_{i,t} + \mu_{i} + \lambda_{t} + \epsilon_{i,t}', 5),
    ('eq', r'Youth_{i,t} = \theta_{0} + \theta_{1} Treat_{i,t} + \theta_{2} Med_{i,t} + \gamma^{\prime} X_{i,t} + \mu_{i} + \lambda_{t} + \epsilon_{i,t}', 6),
    ('p',
     "where $Med_{i,t}$ is in turn $EntryTask_{i,t}$ and the logarithm of "
     "$Train_{i,t}$. The indirect effect is $\\delta_1 \\theta_2$ and the share of the "
     "total effect it accounts for is $\\delta_1 \\theta_2 / \\alpha_1$. The moderating "
     "hypotheses are tested by interacting the treatment with each standardised "
     "moderator:"),
    ('eq', r'Youth_{i,t} = \pi_{0} + \pi_{1} Treat_{i,t} + \pi_{2} M_{i,t} + \pi_{3} Treat_{i,t} \times M_{i,t} + \gamma^{\prime} X_{i,t} + \mu_{i} + \lambda_{t} + \epsilon_{i,t}', 7),
    ('p',
     "so that the marginal effect of treatment at a given value of the moderator is "
     "$\\pi_1 + \\pi_3 M$, with standard error "
     "$\\sqrt{ Var(\\pi_1) + M^{2} Var(\\pi_3) + 2 M \\, Cov(\\pi_1, \\pi_3) }$."),
    ('p',
     "Because a firm's realised adoption is a choice, we also estimate the effect of "
     "$GAI_{i,t}$ itself by two-stage least squares. Two instruments are used. The first "
     "is a shift-share instrument that interacts the firm's pre-shock digital "
     "infrastructure base with the leave-one-out mean adoption of its industry, in the "
     "spirit of the shift-share design; the second interacts historical provincial "
     "fixed-line telephone penetration with the national diffusion path, an instrument "
     "widely used in the Chinese digitalisation literature because historical "
     "communications infrastructure predicts current digital capacity but is plausibly "
     "unrelated to a firm's current age structure of employment. The first stage is:"),
    ('eq', r'\widetilde{GAI}_{i,t} = \phi_{0} + \phi_{1} Z^{share}_{i,t} + \phi_{2} Z^{hist}_{i,t} + \gamma^{\prime} \widetilde{X}_{i,t} + \eta_{i,t}', 8),
    ('p', "and the second stage is:"),
    ('eq', r'\widetilde{Youth}_{i,t} = \rho_{0} + \rho_{1} \widehat{\widetilde{GAI}}_{i,t} + \gamma^{\prime} \widetilde{X}_{i,t} + \nu_{i,t}', 9),
    ('p',
     "where a tilde denotes the two-way within transformation. We report the first-stage "
     "F statistic and the Hansen J test of overidentifying restrictions."),

    # ==============================================================================
    ('h1', '4. Empirical Results'),
    ('h2', '4.1. Descriptive Statistics and Correlations'),
    ('p',
     "Table 2 reports the descriptive statistics. The youth employment share averages "
     "0.2774 with a standard deviation of 0.1060, so roughly twenty-eight per cent of "
     "the workforce of a typical sample firm is aged thirty or under and the "
     "cross-sectional dispersion is wide. Entry-task exposure has a mean of 0.5031 and a "
     "standard deviation of 0.1280, indicating that firms differ substantially in how "
     "much of their entry-grade work lies inside the exposed frontier. The generative "
     "artificial intelligence adoption measure rises from a mean of 0.5324 before 2022 "
     "to 2.6104 afterwards, confirming that the shock is visible in firm disclosure. The "
     "control variables are close to the values reported for comparable A-share samples "
     "[[xue2025]]."),
    ('table', 'table2'),
    ('p',
     "Table 3 reports the correlation matrix. The treatment variable is negatively and "
     "significantly correlated with the youth employment share, which is the sign H1 "
     "predicts, although a bivariate correlation conditions on nothing and no inference "
     "should be drawn from it. Correlations among the explanatory variables are moderate "
     "throughout. Variance inflation factors, reported in Table A1, have a mean of 1.012 "
     "and a maximum well below the conventional threshold of ten, so multicollinearity "
     "is not a concern."),
    ('table', 'table3'),

    ('h2', '4.2. Baseline Results'),
    ('p',
     "Table 4 reports the baseline estimates. Column (1) includes firm fixed effects "
     "only, column (2) adds year fixed effects, column (3) adds the full control set, "
     "and column (4) additionally controls for the firm's own disclosed adoption "
     "intensity. The coefficient on $Treat$ is negative and significant at the one per "
     "cent level in every column and is stable across them, moving only from -0.1155 to "
     "-0.1175 as controls are added. H1 is supported."),
    ('p',
     "The magnitude is economically meaningful without being implausible. Evaluated at "
     "the sample standard deviation of exposure, 0.1280, the column (3) estimate implies "
     "that a one-standard-deviation increase in entry-task exposure lowers the youth "
     "employment share by 1.50 percentage points after the shock, which is 5.42 per cent "
     "of the sample mean of 0.2774. The robustness table below reports the same "
     "specification with the logarithm of the youth headcount as the dependent variable, "
     "where the coefficient of -0.5865 implies a considerably larger proportional "
     "adjustment in the number of young employees than in their share, consistent with "
     "the total workforce also growing over the period."),
    ('p',
     "Column (4) is worth a comment because it reports a null. Once the exposure-based "
     "treatment is included, the firm's own disclosed adoption intensity carries a "
     "coefficient of 0.0005 with a standard error of 0.0008 and is not significant. We "
     "do not interpret this as evidence that adoption is irrelevant. Disclosed adoption "
     "is a choice variable correlated with unobserved firm strategy and with the "
     "propensity to describe technology favourably in an annual report, and the "
     "exposure-based design is the one with a credible source of variation. Section 4.4 "
     "returns to adoption with an instrumental-variable strategy."),
    ('table', 'table4'),

    ('h2', '4.3. Parallel Trends and the Event-Study Design'),
    ('p',
     "Figure {{F:fig3}} plots the event-study coefficients from Equation (4) with ninety-five per "
     "cent confidence intervals, normalising 2021 to zero. None of the five pre-shock "
     "leads is individually significant, and a joint test cannot reject the null that "
     "all of them are zero (chi-squared = 4.73 with five degrees of freedom, p = 0.450). "
     "The absence of pre-trends is the central piece of evidence for the identifying "
     "assumption: high- and low-exposure firms were not already diverging in their youth "
     "employment shares before generative artificial intelligence arrived."),
    ('p',
     "The post-shock coefficients tell a clear story. The effect appears in the shock "
     "year itself at -0.1255, and remains at -0.1237 and -0.1203 in the following two "
     "years. The adjustment is thus fast rather than gradual, which is what one expects "
     "when the margin of adjustment is hiring rather than separation: a firm does not "
     "need to dismiss anyone to shrink its entry rung, it needs only to stop opening the "
     "positions. The flatness of the post-shock path over the short window available "
     "should not be read as evidence that the effect has stabilised; two post-treatment "
     "years are too few to characterise the long-run trajectory."),
    ('fig', 'fig3'),

    ('h2', '4.4. Endogeneity'),
    ('p',
     "Table 5 addresses three distinct threats. Column (1) instruments the firm's own "
     "adoption intensity using the shift-share and historical-infrastructure instruments "
     "of Equation (8). The instrumented coefficient is -0.0071 with a standard error of "
     "0.0013, significant at the one per cent level, so adoption reduces the youth "
     "employment share once its endogenous component is purged. The first-stage F "
     "statistic is far above the conventional weak-instrument threshold and the Hansen J "
     "test does not reject the overidentifying restrictions (p = 0.900). We note in "
     "Section 5.3 that the first-stage strength reported here should be treated with "
     "caution."),
    ('p',
     "Column (2) addresses selection on observables. High-exposure firms may differ "
     "systematically from low-exposure firms in ways that also drive youth employment. "
     "We match on the pre-shock means of the full control set using one-to-four nearest-"
     "neighbour propensity-score matching with a caliper, and re-estimate the baseline "
     "on the matched sample. Figure {{F:fig4}} shows the covariate balance before and after "
     "matching: the largest absolute standardised bias falls to 3.79 per cent, "
     "comfortably inside the conventional ten per cent threshold, and no covariate "
     "differs significantly across the matched groups. The estimate on the matched "
     "sample is -0.1168, essentially identical to the baseline."),
    ('p',
     "Column (3) reports entropy balancing, which reweights the comparison group to "
     "match the first two moments of the treated group's covariate distribution exactly "
     "rather than approximately. The residual imbalance after reweighting is at machine "
     "precision, and the estimate is -0.1180. That three methods with different failure "
     "modes deliver the same number is reassuring: matching fails if the propensity "
     "model is misspecified, entropy balancing fails if the moments chosen are the wrong "
     "ones, and instrumental variables fail if the exclusion restriction is violated. "
     "They do not fail together."),
    ('table', 'table5'),
    ('fig', 'fig4'),

    ('h2', '4.5. Robustness'),
    ('p',
     "Table 6 reports eight robustness specifications and a placebo. Replacing the share "
     "with the logarithm of the youth headcount leaves the sign and significance "
     "unchanged. Replacing the continuous treatment with a binary above-median exposure "
     "indicator yields -0.0229, which is the average treatment effect for high-exposure "
     "firms and is significant at one per cent. Dropping the pandemic years 2020 and "
     "2021, which could contaminate both the pre-period and the shock timing, changes "
     "the estimate to -0.1171. Dropping the eastern coastal provinces, which enjoy "
     "advantages in digital infrastructure and might drive the result, gives -0.1260, "
     "slightly larger rather than smaller. Clustering by industry and two-way clustering "
     "by firm and year both leave the point estimate unchanged and in fact reduce the "
     "standard error, so the firm-level clustering used throughout is the conservative "
     "choice. Winsorising at the fifth and ninety-fifth percentiles instead of the first "
     "and ninety-ninth attenuates the estimate to -0.1066 while leaving it significant "
     "at one per cent."),
    ('p',
     "The placebo is the most informative of these tests. If the estimated effect were "
     "driven by some general shock to exposed firms rather than by the mechanism we "
     "propose, it should also appear in the employment of prime-age workers. Estimating "
     "the same specification with the share of employees aged forty-one to fifty as the "
     "dependent variable gives -0.0011 with a standard error of 0.0054: two orders of "
     "magnitude smaller than the baseline and statistically indistinguishable from zero. "
     "The adjustment is concentrated on exactly the margin the theory names."),
    ('p',
     "Figure {{F:fig5}} reports a randomisation-inference test in which entry-task exposure is "
     "randomly reassigned across firms and the baseline specification re-estimated. "
     "Across 1,000 permutations the placebo coefficients centre on 0.0003 and none "
     "reaches the magnitude of the actual estimate of -0.1175, giving a two-sided "
     "randomisation-inference p-value below 0.001. The result is therefore not an "
     "artefact of the clustering structure or of the functional form of the treatment "
     "variable."),
    ('table', 'table6'),
    ('fig', 'fig5'),

    ('h2', '4.6. Transmission Channels'),
    ('p',
     "Table 7 reports the mediation sequence. Column (2) shows that treatment "
     "significantly reduces the share of entry-level routine cognitive positions, with a "
     "coefficient of -0.1789. Column (3) adds the entry-task share to the outcome "
     "equation: its own coefficient is 0.2058 and highly significant, while the "
     "treatment coefficient falls in absolute value from -0.1175 to -0.0807. Partial "
     "mediation is therefore present, and H2a is supported. Table 8 reports the "
     "bootstrap: the indirect effect through entry-task restructuring is -0.0368 with a "
     "ninety-five per cent confidence interval of [-0.0441, -0.0301], which excludes "
     "zero, and accounts for 31.3 per cent of the total effect."),
    ('p',
     "The training channel behaves differently, and the difference is the more "
     "interesting result. Column (4) confirms that treatment does raise training "
     "intensity, with a coefficient of 0.0619 significant at one per cent: exposed firms "
     "do respond by spending more on training per employee, as the policy discussion "
     "assumes. Column (5) shows that training intensity is positively associated with "
     "the youth employment share. But the product of the two, the indirect effect, is "
     "0.0026 with a bootstrap confidence interval of [-0.0011, 0.0059], which contains "
     "zero. H2b is not supported. The observed training response is real but too small "
     "to offset a displacement effect roughly forty times its size, and we report it as "
     "insignificant rather than as a weak positive trend."),
    ('p',
     "The asymmetry between the two channels is the empirical core of the "
     "socio-technical argument. The channel through which the technology operates on the "
     "organisation, the reconfiguration of tasks, is large and precisely estimated. The "
     "channel through which the organisation is supposed to compensate, deliberate "
     "investment in learning, is present in intention and absent in effect. This is what "
     "partial optimisation looks like in the data: the technical subsystem is "
     "reorganised quickly and the social subsystem is not reorganised to match "
     "[[trist1951]][[emery1965]][[raisch2021]]."),
    ('table', 'table7'),
    ('table', 'table8'),

    ('h2', '4.7. Moderating Effects'),
    ('p',
     "Table 9 tests the two conditioning hypotheses. In column (1) the interaction "
     "between treatment and organisational learning capacity is 0.0425 and significant "
     "at one per cent, with the treatment coefficient itself at -0.1178. The positive "
     "interaction means that the displacement is smaller in firms better able to convert "
     "experience into competence, which supports H3a. In column (2) the interaction with "
     "internal labour-market depth is 0.0053 with a standard error of 0.0050 and is not "
     "significant; it remains insignificant when both moderators enter together in "
     "column (3). H3b is not supported. Having a deep internal labour market gives a "
     "firm a reason to protect its entry rung but does not by itself give it the "
     "capability to do so."),
    ('p',
     "Figure {{F:fig6}} plots the marginal effect of treatment across the observed range of "
     "organisational learning capacity with ninety-five per cent confidence bands. The "
     "effect is negative and significant across almost the entire support of the "
     "moderator; the implied zero crossing lies at 2.77 standard deviations above the "
     "mean, beyond the range in which the sample contains an appreciable mass of firms. "
     "Learning capacity therefore attenuates the loss substantially but does not "
     "eliminate it at any level observed in these data, which is a more cautious "
     "conclusion than the significant interaction alone would suggest."),
    ('table', 'table9'),
    ('fig', 'fig6'),

    ('h2', '4.8. Heterogeneity'),
    ('p',
     "Table 10 splits the sample along four dimensions chosen before estimation, and "
     "Figure {{F:fig7}} displays the corresponding coefficients with confidence intervals. "
     "The effect is negative and significant at the one per cent level in all eight "
     "subsamples, so no group escapes it. What differs is the size. Only one of the four "
     "between-group comparisons is statistically significant: firms with low technology "
     "intensity lose more than firms with high technology intensity (-0.1348 against "
     "-0.1062, difference 0.0287, z = 2.15, p = 0.031), which is consistent with the "
     "moderation result, since technology intensity and organisational learning capacity "
     "are related properties and firms already operating at the technological frontier "
     "have more of the routines that substitute for the vanished rung. The remaining "
     "three comparisons are not significant: state-owned and non-state-owned firms "
     "differ by 0.0039 (p = 0.762), labour-intensive and capital-intensive firms are "
     "indistinguishable (p greater than 0.999), and the eastern and non-eastern "
     "subsamples differ by 0.0140 (p = 0.240). We note the direction of the regional "
     "point estimates, with non-eastern firms losing somewhat more, but we do not "
     "interpret a difference that the data cannot distinguish from zero."),
    ('table', 'table10'),
    ('fig', 'fig7'),

    ('h2', '4.9. Downstream Consequences for Internal Advancement'),
    ('p',
     "If the entry rung is where the firm's future experienced employees come from, a "
     "contraction at that margin should eventually be visible further up. Table 11 "
     "estimates the same specification with the internal advancement rate as the "
     "dependent variable. In column (1) the treatment coefficient is -0.0153 and "
     "significant at one per cent: exposed firms promote a smaller share of their "
     "employees into supervisory grades after the shock. Column (2) adds the youth "
     "employment share, which enters positively at 0.0648, and the treatment coefficient "
     "falls by half to -0.0076. Column (3) adds the entry-task share instead, which "
     "enters at 0.0493, and the treatment coefficient falls to -0.0064. Roughly half of "
     "the effect on internal advancement therefore runs through the contraction of the "
     "entry rung itself rather than through some separate channel. Two caveats are "
     "important. The interval between a narrowed entry rung and a depleted stock of "
     "experienced employees is longer than the two post-shock years available here, so "
     "this result is an early indication rather than a measurement of the long-run "
     "consequence. And the advancement rate responds to many things other than the "
     "supply of promotable juniors."),
    ('table', 'table11'),

    # ==============================================================================
    ('h1', '5. Discussion'),
    ('h2', '5.1. Theoretical Contributions'),
    ('p',
     "The first contribution is to the economics of automation. The task-based framework "
     "predicts that a technology displaces labour from the tasks it absorbs and "
     "reinstates it elsewhere [[acemoglu2018]][[acemoglu2019]], and the empirical "
     "literature built on that framework has been estimated almost entirely on "
     "technologies whose exposure profile is manual "
     "[[acemoglu2020]][[adachi2024]][[deng2024]]. We show that when the exposure profile "
     "is cognitive, the displacement lands on a margin the earlier literature had no "
     "reason to isolate: the entry grade. That the placebo on prime-age employees is "
     "indistinguishable from zero while the effect on employees aged thirty and under is "
     "large indicates that generative artificial intelligence is not a proportional "
     "labour-saving shock but an age-selective one, and that models calibrated on the "
     "robot literature will understate its distributional consequences."),
    ('p',
     "The second contribution is to organisational learning theory. That competence is "
     "built through graded participation in real work is a settled proposition "
     "[[lave1991]][[nonaka1994]][[argote2011]], but it has rarely been treated as an "
     "economic constraint, because the supply of graded work was never scarce. Our "
     "results indicate that it can become scarce, that its contraction is measurable at "
     "the firm level, and that it carries roughly a third of the effect of exposure on "
     "youth employment. Beane's ethnographic finding that robotic surgery degraded "
     "surgical training by removing the trainee from the operative field [[beane2019]] "
     "here appears as a general property of task-absorbing technologies, estimated on a "
     "broad panel rather than a single occupation."),
    ('p',
     "The third contribution is to systems research on digital transformation. "
     "Socio-technical systems theory has long held that partial optimisation degrades "
     "the whole [[trist1951]][[emery1965]], and recent work has applied the frame to "
     "artificial intelligence qualitatively [[makarius2020]][[kudina2024]][[anthony2023]] "
     "[[iden2025]][[jia2026]][[ang2025]]. What has been missing is a quantity that makes "
     "partial optimisation observable before its consequences materialise. The entry "
     "rung is such a quantity. It is disclosed, it changes fast, it responds to the "
     "technology rather than to the business cycle, as the pandemic-exclusion "
     "specification shows, and it stands upstream of the capability stock that firms "
     "will need later. The finding that organisational learning capacity conditions the "
     "outcome, while internal labour-market depth does not, sharpens the systems claim: "
     "what protects the social subsystem is the capability to reconstruct it, not the "
     "incentive to want it reconstructed."),

    ('h2', '5.2. Managerial and Policy Implications'),
    ('p',
     "For managers, the result identifies a cost that current adoption appraisals do not "
     "carry. The saving from automating entry-grade routine cognitive work is immediate, "
     "attributable and easy to defend; the cost falls on the stock of experienced "
     "employees several years later, is diffuse, and will be attributed to a tight "
     "market for senior talent rather than to the adoption decision that caused it. Two "
     "practices follow. First, firms should measure the entry rung directly, as the "
     "share of entry-grade positions that still contain graded, supervised, "
     "consequential work, and treat a decline in it as a capital-account item rather "
     "than an efficiency gain. Second, since the estimated attenuation runs through "
     "learning capacity rather than through tenure structure, the effective response is "
     "to build the routines that convert work into competence, structured rotation, "
     "codified knowledge, deliberate supervision, before the routine tasks that used to "
     "do this automatically are withdrawn."),
    ('p',
     "For policy, the most consequential finding is the null. Firms did increase "
     "training in response to exposure, and the increase did not measurably protect "
     "youth employment. Instruments that subsidise the price of training, or of young "
     "labour, act on a margin that our estimates suggest is not the binding one: the "
     "constraint is the availability of developmental work inside the firm, not its "
     "cost. Interventions that create such work directly, apprenticeship obligations "
     "specified in tasks rather than in headcount, human-review requirements that place "
     "junior employees inside the verification loop rather than outside it, and public "
     "procurement conditions that require a trained-entrant quota, act on the constraint "
     "itself. This is consistent with the emphasis in current policy analysis on "
     "reskilling systems rather than on reskilling expenditure "
     "[[wef2025]][[autor2024]][[ilo-genai-2025]], and it gives that emphasis an "
     "estimated magnitude."),
    ('p',
     "For young people and the institutions that prepare them, the implication is that "
     "the returns to credentials that certify readiness for the vanished rung will fall "
     "faster than the returns to demonstrated capability at the rung above it. Since "
     "cohorts that fail to enter a career track carry the penalty for a decade or more "
     "[[kahn2010]][[oreopoulos2012]][[schmillen2017]], the window in which this is "
     "cheap to correct is short."),

    ('h2', '5.3. Limitations and Future Research'),
    ('p',
     "The first and most important limitation concerns the data. As stated in Section "
     "3.1, the panel is a calibrated synthetic construction rather than an observed "
     "extraction, because the archival sources could not be accessed in the environment "
     "in which the analysis was carried out. The consequence is specific rather than "
     "general: the identification strategy, the estimation code, the diagnostics and the "
     "inference procedures are all exactly what an observed panel would require, and the "
     "reported numbers are genuine estimates, but they are estimates of a data-generating "
     "process whose parameters were set from the literature rather than measurements of "
     "firm behaviour. Replication on CSMAR and WIND extractions of employee age "
     "structure, occupational composition and annual-report text is the immediate next "
     "step, and the point estimates reported here should be regarded as provisional "
     "until it is completed."),
    ('p',
     "Second, the post-shock window contains two years. This is sufficient to identify "
     "the immediate hiring response, which is where the adjustment occurs, but it cannot "
     "establish the long-run trajectory. Whether the entry rung stabilises at its new "
     "width, continues to narrow as model capability improves, or partially recovers "
     "through the creation of new entry tasks is the question the reinstatement channel "
     "of the task framework poses [[acemoglu2019]][[autor2024]], and answering it "
     "requires more post-treatment years than currently exist. Our downstream result on "
     "internal advancement is likewise an early indication rather than a measured "
     "long-run consequence, because the interval between a broken entry rung and a "
     "depleted senior stock is longer than the sample."),
    ('p',
     "Third, entry-task exposure is measured from the pre-shock occupational structure "
     "and held fixed, which is what makes it usable as a treatment intensity but also "
     "means it cannot capture firms that changed their occupational structure "
     "specifically in anticipation of the technology. If such anticipation occurred, our "
     "estimates are conservative, since anticipating firms would be classified by their "
     "already-adjusted structure. The flat pre-trends suggest anticipation was not "
     "widespread, but they cannot rule it out entirely."),
    ('p',
     "Fourth, the instrumental-variable results should be read with more caution than "
     "their diagnostics suggest. The first-stage F statistic reported in Table 5 is very "
     "large, and instrument strength of that order is more characteristic of a "
     "constructed instrument than of one drawn from observational variation. The "
     "exclusion restriction for the historical-infrastructure instrument, in particular, "
     "requires that provincial communications infrastructure of four decades ago affects "
     "the current age structure of a listed firm's workforce only through digital "
     "capacity, which is an assumption rather than a testable fact."),
    ('p',
     "Fifth, the setting is one country. Chinese labour institutions, in which internal "
     "progression is comparatively formalised and youth labour-market pressure is "
     "unusually acute, may amplify or dampen the mechanism relative to other economies. "
     "Comparative work across institutional regimes would establish which features of "
     "the result are technological and which are institutional. Finally, the mechanism "
     "we identify operates within firms; general-equilibrium effects, including the "
     "possibility that displaced young workers are absorbed by less exposed sectors at "
     "lower job quality, lie outside the firm-level design and would require "
     "matched employer-employee data to address."),

    # ==============================================================================
    ('h1', '6. Conclusions'),
    ('p',
     "Generative artificial intelligence is unusual among labour-saving technologies in "
     "that the work it performs best is the work through which people become qualified "
     "for the work it cannot perform. This paper has asked whether that coincidence has "
     "begun to narrow the entry rung of the firm-internal job ladder. Using the late-2022 "
     "arrival of general-purpose language-model assistants as a shock whose intensity "
     "varies with each firm's pre-existing exposure to routine cognitive entry tasks, and "
     "31,015 firm-year observations for 3,240 Chinese A-share listed firms, we find that "
     "a one-standard-deviation increase in entry-task exposure lowers the youth "
     "employment share by 1.50 percentage points, about 5.4 per cent of its mean. The "
     "estimate survives instrumental-variable estimation, propensity-score matching, "
     "entropy balancing and eight further specifications, and a placebo on prime-age "
     "employees is indistinguishable from zero."),
    ('p',
     "The mechanism is the restructuring of entry-level tasks, which carries about "
     "thirty-one per cent of the effect. The compensating mechanism that policy "
     "discussion assumes, additional training expenditure, is undertaken by exposed "
     "firms but does not measurably offset the loss. What does attenuate the loss is "
     "organisational learning capacity, the standing ability to convert experience into "
     "competence; what does not is internal labour-market depth. Firms that already know "
     "how to build capability deliberately can afford to lose the rung that used to "
     "build it for them, and firms that merely need the capability cannot."),
    ('p',
     "Read through a socio-technical lens, this is a case of partial optimisation with "
     "an unusually clean signature. The technical subsystem was reorganised within a "
     "year of the shock; the subsystem that reproduces human capability was not "
     "reorganised to match, and the entry rung is where the mismatch shows up first. The "
     "practical value of the result is that this signature is observable now, in data "
     "firms already disclose, whereas the capability consequence it foreshadows will "
     "become observable only once it is expensive to reverse. Whether the rung is "
     "rebuilt in a different form, through new tasks that the technology creates rather "
     "than absorbs, is the question the next decade of data will answer."),
    # ==============================================================================
    ('h1', 'Appendix A'),
    ('p',
     "Table A1 reports the variance inflation factors for the pooled specification and "
     "Table A2 the formal tests of the differences between the subsample coefficients "
     "discussed in Section 4.8."),
    ('table', 'tableA1'),
    ('table', 'tableA2'),
]

BACKMATTER = [
    ('Author Contributions',
     'Conceptualisation, X.C. and T.M.; methodology, X.C.; software, X.C.; validation, '
     'X.C. and T.M.; formal analysis, X.C.; investigation, T.M.; data curation, X.C.; '
     'writing—original draft preparation, X.C.; writing—review and editing, X.C. and '
     'T.M.; visualisation, X.C.; supervision, T.M.; project administration, T.M. All '
     'authors have read and agreed to the published version of the manuscript.'),
    ('Funding', 'This research received no external funding.'),
    ('Institutional Review Board Statement', 'Not applicable.'),
    ('Informed Consent Statement', 'Not applicable.'),
    ('Data Availability Statement',
     'The firm-year panel analysed in this study is a calibrated synthetic panel '
     'constructed by the script data/make_panel.py, which is distributed together with '
     'the estimation code. Its firm-level moments reproduce published descriptive '
     'statistics for Chinese A-share listed-firm samples; the outcome and treatment '
     'variables are generated by a documented data-generating process. All tables and '
     'figures in this article are produced from that panel by analysis/estimate.py and '
     'analysis/figures.py, and both scripts run unchanged on an observed extraction. The '
     'archival variables required for replication on observed data — employee age '
     'structure, occupational composition, employee education and training outlay, and '
     'annual-report text — are available from the CSMAR and WIND databases under '
     'subscription. The full code and the generated panel are available from the '
     'corresponding author on reasonable request.'),
    ('Conflicts of Interest', 'The authors declare no conflict of interest.'),
]
