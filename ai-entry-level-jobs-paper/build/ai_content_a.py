# -*- coding: utf-8 -*-
"""Manuscript content, part A: front matter, introduction, theory, calibration."""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
CAL = json.load(open(os.path.join(_HERE, "calibrated.json")))
_P = CAL["params"]
_C = CAL["checks"]
_M = {m["moment"]: m for m in CAL["moments"]}


def _n(x, d=3):
    return (("%%.%df" % d) % x).replace("-", "\u2212")


def _t2_rows():
    ident = {
        "u_rate_j": "⟪c_{j}⟫ entry-level vacancy cost",
        "u_rate_s": "⟪c_{s}⟫ experienced vacancy cost",
        "wage_ratio": "⟪\\alpha⟫ weight on entry-level tasks",
        "pi": "⟪\\bar{\\pi}⟫ promotion scale",
        "ai_share": "⟪p_{a}⟫ price of artificial intelligence",
        "labour_share": "⟪s⟫ output elasticity of the bundle",
        "repl_rate": "⟪b⟫ flow value of non-employment",
        "Y": "⟪Z⟫ total factor productivity",
    }
    est = {
        "u_rate_j": _P["c_j"], "u_rate_s": _P["c_s"], "wage_ratio": _P["alpha"],
        "pi": _P["pibar"], "ai_share": _P["p_a"], "labour_share": _P["s_y"],
        "repl_rate": _P["b"], "Y": _P["Z"],
    }
    label = {
        "u_rate_j": "Entry-level unemployment rate",
        "u_rate_s": "Experienced unemployment rate",
        "wage_ratio": "Experience wage premium",
        "pi": "Promotion hazard",
        "ai_share": "AI share of entry-level tasks",
        "labour_share": "Labour share of value added",
        "repl_rate": "Flow value of non-employment, relative to the entry wage",
        "Y": "Output per member of the labour force",
    }
    rows = [["Moment", "Target", "Model", "Estimate", "Parameter identified"]]
    for m in CAL["moments"]:
        k = m["moment"]
        rows.append([label[k], _n(m["target"], 3), _n(m["simulated"], 3),
                     _n(est[k], 3), ident[k]])
    return rows


def _t3_rows():
    rows = [["Statistic", "Model", "External benchmark"]]
    rows.append(["Mean duration of entry-level job search (months)",
                 _n(_C["search_months_j"], 1),
                 "Graduate surveys report a first-job search of four to six "
                 "months"])
    rows.append(["Share of employment held by experienced workers (%)",
                 _n(100 * _C["senior_emp_share"], 1),
                 "Implied by a 3.5-year entry tier in a 40-year career"])
    rows.append(["Recruiting cost per entry-level hire (months of the entry wage)",
                 _n(12 * _C["hire_cost_j"], 1),
                 "Upper end of the international range for skilled hires"])
    rows.append(["Recruiting cost per experienced hire (months of the senior wage)",
                 _n(12 * _C["hire_cost_s"], 1),
                 "Upper end of the international range for skilled hires"])
    rows.append(["Mentoring time as a share of experienced working time (%)",
                 _n(100 * _C["mentor_share"], 2),
                 "Not separately measured"])
    rows.append(["Firm-financed training as a share of the wage bill (%)",
                 _n(100 * _C["train_share"], 2),
                 "Chinese enterprises report 1.5 to 2.5 per cent of the wage "
                 "bill as employee-education expenditure; the model "
                 "under-predicts this (Section 4.3)"])
    return rows


TITLE = ("Narrowing the Gate, Not Breaking the Ladder: Artificial Intelligence, "
         "Entry-Level Access and the Under-Provision of On-the-Job Training")

ABSTRACT = (
    "An entry-level job is a joint product: it delivers output today and it is the "
    "only technology that turns a novice into an experienced worker. Artificial "
    "intelligence substitutes for the first component and not for the second, which "
    "has made the fate of the career ladder an urgent question. We build a two-tier "
    "search-and-matching model with endogenous mentoring, Nash bargaining, free "
    "entry, poaching and real rigidity of the entry wage, and estimate eight "
    "parameters that reproduce eight Chinese labour-market moments exactly. Three "
    "results follow. The market provides about one seventh of the efficient amount "
    "of on-the-job training even though the Hosios condition holds exactly, so "
    "promotion takes three and a half years instead of one: Hosios decentralises "
    "vacancy creation but never training. Cheaper artificial intelligence is borne "
    "by entry-level access rather than entry-level pay, and only because entry wages "
    "are rigid; with flexible wages the same shock is absorbed by pay. Contrary to "
    "our prior, the technology neither breaks the ladder nor widens the training "
    "wedge, because firms mentor a smaller intake far more intensively: promotions "
    "and the stock of experienced workers barely change and the wedge narrows. Held "
    "out of estimation, the model reproduces the entry-level employment gradient "
    "across exposure found in payroll microdata. The efficient response is to price "
    "training, not to tax technology."
)

KEYWORDS = ("entry-level employment; artificial intelligence; search and matching; "
            "on-the-job training; poaching externality; job ladder; wage rigidity; "
            "constrained efficiency; Hosios condition; youth unemployment")

PART_A = [

    # =====================================================================
    ('h1', '1. Introduction'),

    ('p', 'A labour market has to reproduce itself. Experienced workers are not '
          'endowed; they are manufactured, and the factory is the entry-level job. A '
          'firm that hires a novice buys two things at once: the output the novice '
          'produces today, and an option on an experienced worker tomorrow. Every '
          'economy therefore depends on a quiet inter-temporal arrangement in which '
          'today’s employers carry the cost of producing tomorrow’s skilled labour '
          'force. Artificial intelligence acts on exactly one side of that '
          'arrangement. Large language models are good at the codifiable, supervised, '
          'low-context tasks that make up the junior job, and they are of no use for '
          'the thing that makes the junior job valuable to the system as a whole, '
          'which is turning a person into someone who no longer needs supervision '
          '{{eloundou2024|acemoglu2025macro}}. The obvious worry is that the ladder '
          'will break.'),

    ('p', 'The empirical record has begun to show the asymmetry the worry rests on. '
          'Using payroll records covering millions of United States workers, '
          'Brynjolfsson, Chandar and Chen {{brynjolfsson2025canaries}} document a '
          'relative employment decline of about sixteen per cent for workers aged 22 '
          'to 25 in the occupations most exposed to generative artificial '
          'intelligence, with no comparable decline for experienced workers in the '
          'same occupations, and with adjustment running through headcount rather '
          'than through pay. In China the same pressure meets a much larger cohort. A '
          'record 12.22 million graduates entered the labour market in 2025 and 12.7 '
          'million are expected in 2026, the surveyed urban unemployment rate of '
          '16–24-year-olds excluding students reached 18.9 per cent in August 2025, '
          'and graduate-facing job postings fell by more than a fifth in the first '
          'half of that year, while enterprise adoption of artificial-intelligence '
          'agents rose from under a tenth to roughly half of industrial enterprises '
          'within a single year {{nbs2026|moe2026}}. Evidence from other settings is '
          'more muted—Danish administrative data show precise nulls for earnings and '
          'hours two years after chatbot adoption {{humlum2025}}—which is itself '
          'informative: the margin that moves first is not the price of labour but '
          'the decision to open the entry-level door.'),

    ('p', 'Three questions follow, and none of them can be answered by an elasticity. '
          'Is the market’s provision of on-the-job training efficient to begin with? '
          'What determines whether a technology shock to junior tasks is absorbed by '
          'entry wages or by entry-level hiring? And does the shock damage the '
          'mechanism that produces experienced workers, or merely reallocate who '
          'passes through it? These are questions about a feedback structure and its '
          'prices, so they need a model in which the structure is explicit and the '
          'prices are estimated.'),

    ('p', 'This paper supplies one. We treat the career ladder as a socio-technical '
          'system with a single reproduction loop: entry-level hiring produces '
          'experienced workers, experienced workers supply the mentoring without '
          'which no further entrants can be promoted, and the loop closes. We embed '
          'the loop in a two-tier search-and-matching economy with free entry on both '
          'tiers, Nash-bargained wages subject to real rigidity at the entry level, '
          'endogenous mentoring intensity, and an artificial-intelligence input that '
          'substitutes for entry-level task output but cannot mentor. Two frictions '
          'separate the private from the social return to training. Mentoring is '
          'chosen after the wage is agreed and is not contractible, so the firm bears '
          'its whole cost while keeping only its bargaining share of the return; and '
          'a trained worker is poached by rival firms at a positive rate, which the '
          'firm discounts and the planner does not, because the worker keeps the job '
          '{{acemoglupischke1999|stevens1994}}. Eight structural parameters are '
          'estimated to reproduce eight Chinese labour-market moments exactly, and '
          'the model is then asked a question it was never fitted to answer.'),

    ('p', 'Four results follow. The first is an efficiency result. Under the Hosios '
          'condition, with no poaching and with contractible training, the '
          'decentralised steady state coincides exactly with the constrained '
          'planner’s allocation—a property we verify numerically to machine '
          'precision and use as an internal validity check on the entire system of '
          'value functions and costates. Relaxing the contracting frictions breaks '
          'efficiency on the training margin while leaving vacancy creation '
          'efficient, so a single condition cannot decentralise two margins. In the '
          'calibrated economy, where the Hosios condition holds exactly by '
          'construction, the market nevertheless provides about one seventh of the '
          'efficient amount of mentoring, and first promotion takes three and a half '
          'years instead of one.'),

    ('p', 'The second is a result about incidence, and it is conditional in an '
          'informative way. When entry wages are flexible, a fall in the price of '
          'artificial intelligence is absorbed almost entirely by the entry wage and '
          'entry-level employment scarcely moves; when entry wages are rigid, the '
          'same shock is absorbed almost entirely by entry-level hiring. The observed '
          'pattern—large employment effects for the young, negligible pay '
          'effects—therefore does not follow from the technology alone. It requires '
          'the wage floor, which in China is provided by binding provincial minimum '
          'wages and heavily compressed graduate pay scales {{mayneris2018}}. The '
          'incidence of automation on young workers is an institutional outcome, not '
          'a technological one.'),

    ('p', 'The third result contradicts the premise we began with, and is the paper’s '
          'main substantive contribution. Cheaper artificial intelligence does not '
          'break the ladder. Firms respond to a smaller intake by mentoring each '
          'entrant far more intensively, so the flow of promotions and the stock of '
          'experienced workers are almost unchanged, and time to first promotion '
          'falls rather than rises. Nor does the technology aggravate the market '
          'failure: the gap between market and efficient training narrows as '
          'artificial intelligence spreads, because scarcer entrants are individually '
          'more worth training. The training externality is large, but it is '
          'pre-existing and is not created or worsened by artificial intelligence. '
          'Aggregate welfare rises while the cohort waiting to enter loses, so what '
          'the technology produces is a distributional problem sitting on top of an '
          'efficiency problem that was already there.'),

    ('p', 'The fourth is a policy result. At a common fiscal cost, a mentoring credit '
          'dominates entry-level wage and vacancy subsidies on welfare, on '
          'entry-level access and on the marginal value of public funds, and a tax on '
          'artificial intelligence is dominated by all of them. Once the ladder '
          'subsidies are in place the optimal artificial-intelligence tax is zero: '
          'the input is efficiently priced conditional on the allocation, and taxing '
          'it destroys output without repairing the externality it is blamed for.'),

    ('p', 'The paper speaks to three literatures at once. To the task-based literature '
          'on automation {{acemoglurestrepo2018|acemoglu2019|acemoglu2022}} it adds a '
          'joint-product structure in which the automatable component and the '
          'skill-formation component of the same job are separable and are priced '
          'differently by the market, and it shows that the second component is far '
          'more robust to automation than the first. To the literature on training in '
          'imperfect labour markets {{becker1964|acemoglupischke1998|acemoglupischke1999}} '
          'it adds a general-equilibrium environment in which the return to training '
          'is endogenous to a technology shock, and a quantification of the resulting '
          'under-provision. To the emerging empirical literature on generative '
          'artificial intelligence and employment '
          '{{brynjolfsson2025canaries|genai3|humlum2025|eloundou2024}} it offers a '
          'structural account of why the young are affected first, why the '
          'adjustment runs through hiring rather than wages, and why that fact is '
          'evidence about wage-setting institutions rather than about the technology.'),

    ('p', 'Section 2 places the paper in the literature. Section 3 sets out the model, '
          'defines equilibrium, characterises the constrained optimum and states the '
          'two propositions. Section 4 describes the calibration, its identification '
          'and its over-identifying checks. Section 5 reports the counterfactuals, the '
          'channel decomposition, the incidence analysis, the held-out validation, the '
          'policy comparison and the robustness analysis. Section 6 discusses '
          'interpretation and limitations, and Section 7 concludes.'),

    # =====================================================================
    ('h1', '2. Related Literature and Contribution'),

    ('h2', '2.1. Automation, Tasks and the Level of Employment'),

    ('p', 'The task-based framework treats technology as reallocating tasks between '
          'labour and capital, with a displacement effect that lowers labour demand '
          'and a reinstatement effect that creates new labour-intensive tasks '
          '{{acemoglurestrepo2018|acemoglu2019}}. Applied to robots, it has delivered '
          'credible negative employment estimates in the United States {{robots_us}}, '
          'sharply smaller ones in Japan {{robots_japan}}, and mixed firm-level '
          'results in China, where adoption often coincides with expansion '
          '{{prod1|robots_china_firm|robots_china2|zhejiang2}}. Age is where these '
          'studies come closest to the present paper: German production-unit data '
          'show that robot adoption reduces the hiring of young workers while leaving '
          'incumbents largely untouched {{robots_age}}, and Chinese evidence points '
          'the same way for youth employment quality {{liang2024}}. Closest of all is '
          'the evidence that technological and organisational change reshapes '
          'the internal career paths of incumbent workers rather than only the '
          'level of employment {{career2}}, and firm-level Chinese evidence that '
          'intelligent manufacturing upgrades the human capital of the workforce '
          'it retains {{im_hc|pilot2}}. Generative '
          'artificial intelligence differs from robotics in exposing cognitive and '
          'codifiable work {{eloundou2024|frey}}, which is disproportionately what '
          'junior employees do. Macroeconomic magnitudes remain contested '
          '{{acemoglu2025macro}}, and micro-evidence ranges from large productivity '
          'gains in specific occupations {{genai3|genai2}} to precise nulls on '
          'earnings and hours {{humlum2025}}; numerical work on the skill premium points '
          'to the same tension between displacement and complementarity '
          '{{sbtc1}}. Our contribution is not another estimate '
          'of a displacement elasticity but a statement about which margin the '
          'elasticity operates on, what determines that, and whether the margin has an '
          'externality attached to it.'),

    ('h2', '2.2. Training, Poaching and the Job Ladder'),

    ('p', 'In a frictionless labour market firms never pay for general training, '
          'because the worker captures its whole return {{becker1964}}. Acemoglu and '
          'Pischke showed that once wages are compressed by labour-market frictions '
          'firms do pay, because part of the return accrues to them, and that the same '
          'frictions generate a poaching externality, so that firm-sponsored training '
          'is positive but inefficiently low '
          '{{acemoglupischke1998|acemoglupischke1999}}. Stevens made the '
          'under-investment explicit as a property of imperfect competition '
          '{{stevens1994}}. Empirically, training raises productivity by more than it '
          'raises wages {{training2}}, and automation shifts who receives it '
          '{{training1}}. The complementary literature on internal labour markets '
          'models promotion as the mechanism converting learning into rank and pay '
          '{{gibbons1999}}, and the early-career mobility literature documents how '
          'much of lifetime wage growth is produced in the first years of work '
          '{{topel1992|kambourov2009}}, while the skills literature documents how fast '
          'the content of entry-level competence is now moving '
          '{{rikala2024|reskill2024}} and how unevenly formal vocational '
          'training pays off in China {{vet1|zhao2023}}. We combine the two '
          'strands: training is '
          'firm-sponsored, non-contractible and subject to poaching, and its output is '
          'the stock of experienced workers on which the whole economy’s production '
          'function depends. That general-equilibrium closure is what allows us to ask '
          'whether a technology shock damages the mechanism itself.'),

    ('h2', '2.3. Search, Matching, Efficiency and the Wage Rule'),

    ('p', 'The equilibrium environment is the Diamond–Mortensen–Pissarides framework '
          '{{diamond1982|mortensen1994|pissarides2000}}, whose empirical matching '
          'function is well established {{petrongolo2001}} and whose efficiency '
          'properties are governed by the Hosios condition: the decentralised '
          'allocation is constrained-efficient when the worker’s bargaining power '
          'equals the elasticity of the matching function with respect to '
          'unemployment {{hosios1990}}. Extensions with on-the-job search change the '
          'bargaining problem materially '
          '{{burdett1998|postelvinay2002|cahuc2006}}. A second strand is central to '
          'our incidence result: the volatility literature established that the '
          'response of employment to a productivity shock depends almost entirely on '
          'how much of the shock the wage absorbs '
          '{{shimer2005|hall2008|hagedorn2008|pissarides2009}}. We adopt the '
          'geometric real-rigidity rule of Blanchard and Galí {{blanchard2007}}, which '
          'nests flexible Nash bargaining and a fixed entry wage in a single '
          'parameter and, at the calibration point, is an identity—so the estimated '
          'economy is unaffected by the value that parameter takes, and only the '
          'responses differ. Our efficiency statement is more restrictive than the '
          'classical one: Hosios continues to decentralise vacancy creation but '
          'cannot, on its own, decentralise the training margin.'),

    ('h2', '2.4. Youth Labour Markets and the Chinese Setting'),

    ('p', 'China provides an unusually sharp test bed. Cohort size is large and '
          'rising, the surveyed youth unemployment rate is published monthly under a '
          'methodology that excludes students, mismatch and over-education are '
          'extensively documented, adoption of generative artificial intelligence by '
          'enterprises has been exceptionally fast, and provincial minimum wages bind '
          'for entry-level urban positions '
          '{{china_youth1|china_youth2|mismatch2|pan2025|mayneris2018|mismatch1}}. The '
          'international comparators matter too: youth transitions have '
          'deteriorated across many economies at once {{ilo1|oecd2025}}, and '
          'cross-country work links that deterioration to digitalisation '
          '{{basol|ogbonna|tleppayev2025}}. The '
          'system-oriented literature has approached youth transition outcomes as '
          'emergent properties of interacting institutions rather than as the sum of '
          'individual choices {{grigorescu2025|chacon2025|chen2026|stw}}, and recent '
          'work in this journal has examined how artificial intelligence reshapes '
          'organisational decision systems and career structures '
          '{{systems_ai_dm|career1|sts_ai|sts2}}. The present paper is complementary: '
          'it supplies the price-theoretic mechanism that determines whether the '
          'reproduction loop of the career ladder is operated at, above or below its '
          'socially efficient intensity, and it quantifies how a technology shock '
          'moves that intensity and who bears the cost.'),

    ('h2', '2.5. What This Paper Adds'),

    ('p', 'Three things are new. The first is the joint-product formalisation of the '
          'entry-level job, in which one technology shock hits the priced component '
          'and spares the under-priced one, together with the finding that the '
          'under-priced component is the robust one: the ladder narrows rather than '
          'breaks. The second is the efficiency characterisation—an exact statement of '
          'when the decentralised economy attains the constrained optimum, verified '
          'numerically to machine precision, with the residual wedge decomposed into a '
          'hold-up and a poaching component and quantified against an economy that is '
          'Hosios-efficient by construction. The third is that the incidence of the '
          'shock is shown to be an institutional rather than a technological fact, '
          'which reconciles the conflicting empirical findings in the literature and '
          'yields an instrument ranking with a marginal value of public funds attached '
          'to each instrument, before and after the shock, with the uncertainty '
          'quantified.'),

    # =====================================================================
    ('h1', '3. A Two-Tier Model of the Job Ladder'),

    ('p', 'Time is continuous and agents are risk neutral and discount at rate ⟪r⟫. '
          'The labour force is normalised to one and is partitioned into four states: '
          'entry-level jobseekers ⟪u_{j}⟫, entry-level employed ⟪e_{j}⟫, experienced '
          'jobseekers ⟪u_{s}⟫ and experienced employed ⟪e_{s}⟫. Workers leave the '
          'labour force at rate ⟪\\omega⟫ and are replaced by an equal flow of '
          'entrants, who arrive as entry-level jobseekers. Figure 1 shows the '
          'structure.'),

    ('figure', 'fig1_structure.png', 1,
     'Structure of the model. Panel (a) shows the flows of workers across the four '
     'labour-market states; the promotion flow from entry-level to experienced '
     'employment is the only source of experienced workers in the economy. Panel (b) '
     'shows the technology: entry-level labour and artificial intelligence are '
     'substitutes inside the entry-level task bundle, whereas mentoring diverts '
     'experienced time away from production and is the sole input into the promotion '
     'hazard. Artificial intelligence therefore raises ⟪X_{j}⟫ without raising '
     '⟪\\pi⟫.'),

    ('h2', '3.1. Matching and Flows'),

    ('p', 'Each tier has its own matching market. Meetings on tier ⟪i \\in \\{j,s\\}⟫ '
          'are produced by a constant-returns Cobb–Douglas matching function, so flow '
          'rates depend only on market tightness {{petrongolo2001}}:'),
    ('eq', 'eq1', 1),
    ('p', 'where ⟪\\eta⟫ is the elasticity of matching with respect to unemployment. '
          'The job-finding and vacancy-filling rates follow:'),
    ('eq', 'eq2', 2),
    ('p', 'Entry-level matches dissolve at rate ⟪\\delta_{j}⟫ and experienced matches '
          'at rate ⟪\\delta_{s}⟫, with ⟪\\delta_{j} > \\delta_{s}⟫. An entry-level '
          'employee is promoted at hazard ⟪\\pi⟫, which is where the ladder is '
          'climbed. The four stocks evolve as'),
    ('eq', 'eq3', 3),
    ('eq', 'eq4', 4),
    ('p', 'and sum to one. The promotion flow ⟪\\pi e_{j}⟫ is the only inflow into the '
          'experienced tier from outside it: an economy that stops promoting entrants '
          'stops producing experienced workers, with a delay equal to the average time '
          'to promotion. This is the reproduction loop that the rest of the paper is '
          'about. Because the entrant flow is exogenous and the labour force is fixed, '
          'the correct measure of entry-level access is the entry-level employment '
          'rate rather than the entry-level employment stock, and the correct measure '
          'of the ladder’s output is the promotion flow ⟪\\pi e_{j}⟫; we report both '
          'throughout.'),

    ('h2', '3.2. Mentoring and the Promotion Technology'),

    ('p', 'Promotion is produced, not received. Each entry-level employee absorbs ⟪m⟫ '
          'units of experienced worker time per unit of time, and the promotion hazard '
          'is increasing and concave in that intensity:'),
    ('eq', 'eq5', 5),
    ('p', 'with ⟪\\psi < 1⟫ so that the marginal product of mentoring is diminishing. '
          'Mentoring is costly in the only currency that matters here: experienced '
          'time withdrawn from production. Because ⟪m⟫ is a flow chosen by the firm '
          'after the wage has been agreed, and because training intensity is not '
          'verifiable by a third party, the firm cannot commit to it and the worker '
          'cannot be made to pay for it through a lower wage. This is the hold-up '
          'friction of Acemoglu and Pischke {{acemoglupischke1999|stevens1994}}; '
          'Section 3.6 reports the contractible benchmark in which it is switched off.'),

    ('h2', '3.3. Technology: The Entry-Level Job as a Joint Product'),

    ('p', 'Output is produced from two task bundles. The entry-level bundle combines '
          'entry-level labour with artificial intelligence; one entry-level worker '
          'supplies ⟪z_{j}⟫ efficiency units of entry-level task input and one '
          'efficiency unit of artificial intelligence supplies ⟪\\chi⟫, so that '
          '⟪\\chi/z_{j}⟫ is the number of entry-level workers displaced by one unit of '
          'artificial intelligence and is the natural measure of exposure. The '
          'experienced bundle is experienced labour net of the time it spends '
          'mentoring:'),
    ('eq', 'eq6', 6),
    ('p', 'The two bundles combine in a constant-elasticity-of-substitution aggregate '
          'with substitution parameter ⟪\\rho⟫, hence elasticity of substitution '
          '⟪\\sigma = 1/(1-\\rho)⟫. The bundle enters output with elasticity ⟪s < 1⟫; '
          'the residual share accrues to a fixed factor—physical, organisational and '
          'land capital—that is not modelled explicitly. This is the standard '
          'span-of-control device and is what allows the model to reproduce an '
          'aggregate labour share below unity:'),
    ('eq', 'eq7', 7),
    ('p', 'with marginal products'),
    ('eq', 'eq8', 8),
    ('p', 'Artificial intelligence is a rented input available at price ⟪p_{a}⟫ per '
          'efficiency unit, taxed at rate ⟪t_{a}⟫. Firms hire it until its marginal '
          'product equals its price:'),
    ('eq', 'eq9', 9),
    ('p', 'Two features of this technology carry the argument. First, artificial '
          'intelligence enters ⟪X_{j}⟫ and not ⟪X_{s}⟫: it does the junior job, not '
          'the senior one. Second, and more important, it does not enter ⟪\\pi⟫ at '
          'all. Hiring an entry-level worker therefore delivers a joint product—'
          'current task output plus an option on an experienced worker—and the '
          'technology shock reduces the first component while leaving the second '
          'intact. Because the market prices these two components very differently, a '
          'shock that would be neutral in a one-component world is not neutral here. '
          'Which way it is not neutral is a quantitative question and the answer, '
          'reported in Section 5, is not the one we expected.'),

    ('h2', '3.4. Values, Wage Determination and Real Rigidity'),

    ('p', 'Let ⟪J_{i}⟫ denote the value to the firm of a filled job on tier ⟪i⟫, '
          '⟪W_{i}⟫ the value to the worker of holding it and ⟪U_{i}⟫ the value of '
          'searching on that tier. Experienced matches are lost to separation at rate '
          '⟪\\delta_{s}⟫ and to rival firms at the poaching rate ⟪\\phi⟫. Poaching is '
          'the asymmetry that matters: the firm loses the match, whereas the worker '
          'moves to an identical job at the going wage and loses nothing, and the '
          'economy as a whole loses nothing either. The firm therefore discounts the '
          'experienced job at ⟪r + \\delta_{s} + \\omega + \\phi⟫ and the worker at '
          '⟪r + \\delta_{s} + \\omega⟫:'),
    ('eq', 'eq10', 10),
    ('eq', 'eq11', 11),
    ('p', 'An entry-level match yields the marginal product of an entry-level worker, '
          'net of the wage and of the mentoring it absorbs, and it delivers the '
          'experienced job on promotion. Writing ⟪s_{w}⟫ for a wage subsidy and '
          '⟪s_{m}⟫ for a mentoring credit,'),
    ('eq', 'eq12', 12),
    ('p', 'while the entry-level worker’s values satisfy'),
    ('eq', 'eq13', 13),
    ('p', 'Wages are bargained over the match surplus with worker bargaining power '
          '⟪\\beta⟫, which yields the familiar sharing rule:'),
    ('eq', 'eq14', 14),
    ('p', 'Entry wages, however, are not fully flexible. Provincial minimum wages bind '
          'for entry-level urban positions in China {{mayneris2018}}, graduate pay '
          'scales are heavily compressed, and the search literature has long held that '
          'how much of a shock the wage absorbs is decisive for how much employment '
          'moves {{shimer2005|hall2008|hagedorn2008|pissarides2009}}. We therefore '
          'adopt the geometric real-rigidity rule of Blanchard and Galí '
          '{{blanchard2007}}, in which the posted entry wage is a weighted geometric '
          'average of the bargained wage ⟪w_{j}^{N}⟫ and a reference wage '
          '⟪\\bar{w}_{j}⟫ anchored by those institutions:'),
    ('eq', 'eq25', 25),
    ('p', 'The parameter ⟪\\gamma_{w}⟫ nests the flexible Nash economy at zero and a '
          'fixed entry wage at one. Two properties make it convenient. At the '
          'reference point the rule is an identity, so the estimated economy of '
          'Section 4 is numerically identical for every value of ⟪\\gamma_{w}⟫ and the '
          'calibration cannot be tuned through it; and the parameter has an observable '
          'implication, namely the split of a shock between pay and employment, which '
          'Section 5.4 uses to ask what value the data require. Experienced wages are '
          'left flexible, since neither minimum wages nor graduate pay scales bind for '
          'them.'),
    ('p', 'Firms post vacancies until the expected cost of filling one equals its '
          'value, which closes the model on both tiers:'),
    ('eq', 'eq15', 15),
    ('p', 'The remaining decision is how much to mentor. Because the wage has already '
          'been set and mentoring is not contractible, the firm maximises ⟪J_{j}⟫ over '
          '⟪m⟫ taking ⟪w_{j}⟫ as given, which gives'),
    ('eq', 'eq16', 16),
    ('p', 'The left-hand side is the private return to mentoring: the marginal '
          'increase in the promotion hazard multiplied by the difference between what '
          'the firm holds after promotion and what it holds before. The right-hand '
          'side is the marginal cost in experienced time. Both terms move when '
          'artificial intelligence becomes cheaper, and in opposite directions, which '
          'is why the training response to the shock cannot be signed a priori. The '
          'contractible benchmark, in which the pair chooses ⟪m⟫ to maximise the joint '
          'surplus ⟪S_{j}⟫, replaces (16) by'),
    ('eq', 'eq17', 17),

    ('h2', '3.5. Equilibrium'),

    ('p', 'A steady-state equilibrium is a triple ⟪(\\theta_{j}, \\theta_{s}, m)⟫, an '
          'artificial-intelligence input ⟪A⟫, wages ⟪(w_{j}, w_{s})⟫ and stocks '
          '⟪(u_{j}, e_{j}, u_{s}, e_{s})⟫ such that the stocks are stationary given '
          'the flow rates, wages satisfy the bargaining problem and the rigidity rule, '
          'artificial intelligence satisfies (9), both free-entry conditions in (15) '
          'hold and the mentoring condition (16) holds. The three conditions in '
          '⟪(\\theta_{j}, \\theta_{s}, m)⟫ are solved numerically; every equilibrium '
          'reported below was located from at least eleven independent starting '
          'points and its residuals driven below ⟪10^{-9}⟫.'),

    ('h2', '3.6. The Constrained Planner and the Two Wedges'),

    ('p', 'The relevant welfare benchmark is a planner who faces the same matching and '
          'promotion technologies and chooses vacancies on both tiers, mentoring '
          'intensity and the artificial-intelligence input to maximise the present '
          'value of output net of recruiting and technology costs plus the flow value '
          'of non-employment:'),
    ('eq', 'eq18', 18),
    ('p', 'subject to the four laws of motion. Poaching does not appear in the '
          'planner’s problem, because a poached worker remains employed in an '
          'identical job: the flow is a private loss and not a social one. Denoting by '
          '⟪\\lambda_{uj}, \\lambda_{ej}, \\lambda_{us}, \\lambda_{es}⟫ the costates of '
          'the four stocks, the steady-state costate equations are'),
    ('eq', 'eq19', 19),
    ('eq', 'eq20', 20),
    ('p', 'and the planner’s optimality conditions for vacancies and for mentoring are'),
    ('eq', 'eq21', 21),
    ('p', 'Comparing these with the decentralised conditions (15) and (16) isolates the '
          'two wedges, which Figure 2 illustrates. The vacancy conditions differ by the '
          'familiar factor ⟪(1-\\eta)⟫ against the firm’s share ⟪(1-\\beta)⟫, so '
          'search externalities cancel exactly when ⟪\\beta = \\eta⟫. The mentoring '
          'conditions differ by two further factors: the firm captures only '
          '⟪(1-\\beta)⟫ of the promotion surplus but pays the whole mentoring cost, '
          'and it values the experienced job at a discount rate inflated by ⟪\\phi⟫. '
          'This yields the two propositions.'),

    ('figure', 'fig2_mechanism.png', 2,
     'The return to an entry-level match and the two wedges that shrink it. Block '
     'heights are illustrative; estimated magnitudes are reported in Section 5. The '
     'lower block is current task output, which artificial intelligence substitutes '
     'for; the upper block is the value of producing an experienced worker, which it '
     'does not. Hold-up removes the share ⟪\\beta⟫ of the upper block from the firm’s '
     'calculation and poaching discounts what remains, so a technology that shrinks '
     'only the lower block shifts the hiring decision onto the part of the return the '
     'market fails to reward.'),

    ('h3', 'Proposition 1 (exact decentralisation).'),
    ('p', 'If the Hosios condition holds ⟪(\\beta = \\eta)⟫, there is no poaching '
          '⟪(\\phi = 0)⟫, mentoring is contractible and entry wages are flexible '
          '⟪(\\gamma_{w} = 0)⟫, then the decentralised steady state coincides with the '
          'constrained planner’s allocation and no intervention can raise welfare. If '
          'either contracting friction is present, the decentralised allocation '
          'under-provides mentoring even when ⟪\\beta = \\eta⟫.'),
    ('p', 'The proof is by direct comparison of the two systems: under these '
          'conditions the costates satisfy '
          '⟪\\lambda_{ei} - \\lambda_{ui} = S_{i}⟫ and ⟪\\lambda_{ui} = U_{i}⟫ on both '
          'tiers, which converts each planner condition into the corresponding market '
          'condition. Because the argument runs through a simultaneous system of eight '
          'equations, we also verify it numerically: at the parameter values of '
          'Section 4, market and planner tightness, mentoring, stocks, output and '
          'welfare agree to a relative error below ⟪10^{-13}⟫. That agreement is a '
          'joint test of the value functions, the costates and the numerical solver, '
          'and it is why the wedges reported below can be attributed to economics '
          'rather than to arithmetic.'),

    ('h3', 'Proposition 2 (incidence depends on the wage rule).'),
    ('p', 'A fall in the price of artificial intelligence lowers the marginal product '
          'of an entry-level worker. Under flexible bargaining the entry wage absorbs '
          'the fall and the surplus, and hence entry-level tightness, is nearly '
          'unchanged; as ⟪\\gamma_{w}⟫ rises the wage absorbs progressively less and '
          'the free-entry condition transmits progressively more of the shock into '
          'entry-level hiring. The employment consequences of automation for young '
          'workers are therefore not a property of the technology alone but of the '
          'wage-setting institutions it meets. Section 5.4 traces the whole mapping '
          'and asks which values of ⟪\\gamma_{w}⟫ are consistent with the observed '
          'pattern.'),

    # =====================================================================
    ('h1', '4. Calibration'),

    ('p', 'The model is calibrated to China in 2025 at annual frequency. Parameters '
          'divide into those set outside the model from external evidence and those '
          'estimated inside it. Three normalisations come first, because they '
          'determine what can be identified at all. Matching efficiency and vacancy '
          'cost enter every equilibrium object only through the ratio '
          '⟪\\mu_{i}^{2}/c_{i}⟫, so ⟪\\mu_{j} = \\mu_{s} = 1⟫ and the vacancy costs '
          'carry that dimension; consequently market tightness is measured in '
          'normalised units and only its changes are meaningful. Task units are also '
          'free, so ⟪z_{j} = \\chi = 1⟫, and only relative changes in ⟪\\chi⟫—the '
          'exposure experiments of Section 5.5—have content. Finally, recruiting cost '
          'per hire equals ⟪J_{i}/w_{i}⟫ by free entry and is therefore implied rather '
          'than free, which makes it available as an over-identifying check.'),

    ('p', 'What remains is eight parameters and eight conditions: seven data moments '
          'and the output normalisation. The system is square, so rather than '
          'minimising a distance that stays positive at the optimum we solve the '
          'moment conditions exactly. A bounded least-squares solve started from a '
          'point derived analytically from the block recursion of the moment system '
          'reaches a maximum absolute log deviation of '
          '' + ("%.1e" % CAL["max_log_resid"]) + ' across all eight conditions. The '
          'criterion used by the global fallback stage is'),
    ('eq', 'eq22', 22),
    ('p', 'where ⟪m_{k}(\\Theta)⟫ is the model counterpart of the target ⟪m_{k}⟫.'),

    ('h2', '4.1. Externally Set Parameters'),

    ('p', 'Table 1 lists the parameters fixed outside the estimation. The discount rate '
          'is 4 per cent and the labour-force exit rate 2.5 per cent, corresponding to '
          'a forty-year career. Separation rates are 0.22 for entry-level matches and '
          '0.085 for experienced matches, reflecting the much higher turnover of first '
          'jobs {{topel1992}}. The poaching rate is 0.18, in the range implied by '
          'job-to-job transition rates among early-career experienced workers '
          '{{cahuc2006}}. The matching elasticity is 0.5, within the consensus range '
          'of the matching-function literature {{petrongolo2001}}, and worker '
          'bargaining power is set equal to it, so the Hosios condition holds exactly '
          'in the baseline. That is a deliberately conservative choice: it removes the '
          'classical search externality by construction, so every wedge we report is '
          'attributable to training and poaching rather than to an assumption about '
          'bargaining power. The elasticity of substitution between the task bundles '
          'is 2.5 and the elasticity of the promotion hazard with respect to mentoring '
          '0.4; both are varied widely in Section 5.8. Real rigidity of the entry wage '
          'is set to ⟪\\gamma_{w}⟫ = 0.8 {{blanchard2007}}, and because the rule is an '
          'identity at the calibration point this choice does not affect any estimated '
          'parameter—only the responses in Section 5, which are reported across the '
          'whole range.'),

    ('tabcap', '1', 'Parameters set outside the estimation, and the three '
                    'normalisations.'),
    ('table', [
        ['Parameter', 'Symbol', 'Value', 'Source or justification'],
        ['Discount rate', '⟪r⟫', '0.040', 'Annual real rate'],
        ['Labour-force exit rate', '⟪\\omega⟫', '0.025',
         'Forty-year working life'],
        ['Entry-level separation rate', '⟪\\delta_{j}⟫', '0.220',
         'High turnover of first jobs {{topel1992}}'],
        ['Experienced separation rate', '⟪\\delta_{s}⟫', '0.085',
         'Separation rates of established matches {{pissarides2000}}'],
        ['Poaching rate', '⟪\\phi⟫', '0.180',
         'Job-to-job transitions of early-career experienced workers '
         '{{cahuc2006}}'],
        ['Matching elasticity', '⟪\\eta⟫', '0.500',
         'Consensus range of the matching-function literature {{petrongolo2001}}'],
        ['Worker bargaining power', '⟪\\beta⟫', '0.500',
         'Hosios condition imposed: ⟪\\beta = \\eta⟫ {{hosios1990}}'],
        ['Elasticity of substitution', '⟪\\sigma⟫', '2.500',
         'Varied from 1.5 to 5.0 in Section 5.8'],
        ['Elasticity of promotion to mentoring', '⟪\\psi⟫', '0.400',
         'Varied from 0.25 to 0.60 in Section 5.8'],
        ['Real rigidity of the entry wage', '⟪\\gamma_{w}⟫', '0.800',
         'Blanchard–Galí rule {{blanchard2007}}; an identity at the '
         'calibration point, so it affects no estimate'],
        ['Matching efficiency, both tiers', '⟪\\mu_{j}=\\mu_{s}⟫', '1.000',
         'Normalisation: only ⟪\\mu_{i}^{2}/c_{i}⟫ is identified'],
        ['Entry-level task efficiency', '⟪z_{j}⟫', '1.000',
         'Normalisation of task units'],
        ['Efficiency of artificial intelligence', '⟪\\chi⟫', '1.000',
         'Normalisation of task units; only changes in ⟪\\chi⟫ have content'],
    ], [3300, 1150, 900, 4290]),

    ('h2', '4.2. Estimated Parameters and Targeted Moments'),

    ('p', 'The eight estimated parameters are total factor productivity, the two '
          'vacancy costs, the weight on the entry-level bundle, the promotion scale, '
          'the price of artificial intelligence, the output elasticity of the labour '
          'bundle and the flow value of non-employment. Table 2 lists the targets, '
          'their sources and the fit, which is exact by construction. Identification '
          'is close to one-to-one and can be read off the block recursion of the '
          'model: the two vacancy costs are pinned by the two unemployment rates, the '
          'flow value of non-employment by the replacement rate, the weight on the '
          'entry-level bundle by the experience wage premium, the promotion scale by '
          'the promotion hazard, the price of artificial intelligence by its task '
          'share, the output elasticity by the labour share, and total factor '
          'productivity by the output normalisation.'),

    ('tabcap', '2', 'Targeted moments, the fit, and the parameter each moment '
                    'principally identifies.'),
    ('table', _t2_rows(), [3600, 1000, 1000, 1000, 3040]),
    ('notes', 'The system is square, so the fit is exact by construction; the '
              'largest absolute log deviation across all eight conditions is '
              '%s. The final column reports the parameter that the block '
              'recursion of the model makes primarily responsible for each '
              'moment; the mapping is not exactly triangular but is close to it.'
              % ("%.1e" % CAL["max_log_resid"])),

    ('h2', '4.3. Over-Identifying Checks and the Held-Out Test'),

    ('p', 'Several statistics are computed but never targeted and are therefore '
          'available as checks; Table 3 reports them. The mean duration of entry-level '
          'job search implied by the estimated economy is '
          '' + _n(_C["search_months_j"], 1) + ' months, which is close to what '
          'graduate-survey evidence reports. The share of employment held by '
          'experienced workers is ' + _n(100 * _C["senior_emp_share"], 1) + ' per '
          'cent, consistent with a labour force in which entrants spend three and a '
          'half years in the entry tier out of a forty-year career. Recruiting cost '
          'per hire is ' + _n(12 * _C["hire_cost_j"], 1) + ' months of the entry '
          'wage and ' + _n(12 * _C["hire_cost_s"], 1) + ' months of the experienced '
          'wage; these sit at the upper end of the international range for skilled '
          'hires, which is a genuine tension we record rather than resolve.'),

    ('tabcap', '3', 'Over-identifying checks: model statistics that were never '
                    'targeted.'),
    ('table', _t3_rows(), [3800, 1500, 4340]),

    ('p', 'One check fails informatively. Firm-financed mentoring in the estimated '
          'economy costs ' + _n(100 * _C["train_share"], 2) + ' per cent of the wage '
          'bill, an order of magnitude below the one-and-a-half to two-and-a-half per '
          'cent that Chinese enterprises report as employee-education expenditure. '
          'Part of the gap is definitional—reported spending covers compliance '
          'training and the upskilling of incumbents, not only the mentoring of '
          'entrants, and much of it is publicly subsidised—but part of it is the '
          'model’s central claim, that firm-financed training of entrants is small '
          'because firms capture little of its return. We flag the check as failed '
          'rather than reinterpreting it as evidence: a model in which the marginal '
          'private return to mentoring is this low will understate observed training '
          'expenditure, and the results of Section 5 should be read with that in mind.'),

    ('p', 'Held out entirely from the estimation is the relationship between '
          'artificial-intelligence exposure and entry-level employment. No information '
          'about employment by exposure enters the calibration at any point, so the '
          'cross-occupation gradient the model predicts in Section 5.5 is a genuine '
          'out-of-sample test against the payroll-based estimate of Brynjolfsson, '
          'Chandar and Chen {{brynjolfsson2025canaries}}.'),

    ('p', 'Two limitations of the calibration should be stated at the outset. The '
          'model is a steady-state, representative-agent structure: it compares '
          'long-run allocations, is silent about transition paths, and cannot address '
          'heterogeneity by field of study, institution or region. And the '
          'artificial-intelligence task share is the least well measured of the eight '
          'targets, since adoption surveys record whether a technology is used rather '
          'than what fraction of entry-level task content it performs; Section 5.2 '
          'therefore reports the whole path rather than a single counterfactual point.'),
]
