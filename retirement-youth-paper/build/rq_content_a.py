# -*- coding: utf-8 -*-
"""Manuscript content, part A: front matter, introduction, theory, calibration."""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
CAL = json.load(open(os.path.join(_HERE, "calibrated.json")))
_P, _C = CAL["params"], CAL["checks"]


def _n(x, d=3):
    return (("%%.%df" % d) % x).replace("-", "−")


def _t1_rows():
    return [
        ["Parameter", "Symbol", "Value", "Source or justification"],
        ["Discount rate", "⟪r⟫", "0.040", "Annual real rate"],
        ["Age at labour-market entry", "⟪a_{0}⟫", "23.0",
         "Mean age of a graduating cohort"],
        ["Length of the young tier", "⟪T_{y}⟫", "7.0",
         "Ages 23–30; the examination age ceiling binds thereafter"],
        ["Effective retirement age, pre-reform", "⟪R⟫", "56.3",
         "Employment-weighted average of 60 for men, 55 and 50 for women"],
        ["Separation rate, rationed sector", "⟪\\delta_{Q}⟫", "0.020",
         "Establishment posts are seldom lost"],
        ["Separation rate, market sector", "⟪\\delta_{M}⟫", "0.180",
         "Turnover of urban private employment {{topel1992}}"],
        ["Matching elasticity", "⟪\\eta⟫", "0.500",
         "Consensus range of the matching-function literature "
         "{{petrongolo2001}}"],
        ["Worker bargaining power", "⟪\\beta⟫", "0.500",
         "Hosios condition imposed, ⟪\\beta = \\eta⟫ {{hosios1990}}"],
        ["Market productivity", "⟪p_{M}⟫", "1.000", "Numeraire"],
        ["Rationed-sector productivity", "⟪p_{Q}⟫", "1.000",
         "Set equal to ⟪p_{M}⟫, so the administered premium is a pure rent; "
         "varied in Section 5.8"],
        ["Matching efficiency, prime tier", "—", "1.000",
         "Normalisation: only ⟪\\mu_{i}^{2}/c_{M}⟫ is identified"],
        ["Entrant cohort", "⟪n⟫", "1.000",
         "Normalisation; results are scaled to 12.7 million where stated"],
    ]


def _t2_rows():
    ident = {
        "u_rate_y": "⟪\\mu_{y}⟫ matching efficiency of the young",
        "u_rate_p": "⟪c_{M}⟫ market vacancy cost",
        "quota_share": "⟪\\bar{N}⟫ size of the establishment",
        "wage_premium": "⟪w_{Q}⟫ administered wage",
        "queue_share": "⟪\\kappa_{q}⟫ flow value while queueing",
        "repl_rate": "⟪b⟫ flow value of open search",
    }
    est = {"u_rate_y": _P["mu_y"], "u_rate_p": _P["c_M"],
           "quota_share": _P["N_bar"], "wage_premium": _P["w_Q"],
           "queue_share": _P["kappa_q"], "repl_rate": _P["b"]}
    label = {
        "u_rate_y": "Youth unemployment rate",
        "u_rate_p": "Prime-age unemployment rate",
        "quota_share": "Rationed share of employment",
        "wage_premium": "Compensation premium of a rationed job",
        "queue_share": "Queue share of youth non-employment",
        "repl_rate": "Flow value of open search, relative to the entry wage",
    }
    rows = [["Moment", "Target", "Model", "Estimate", "Parameter identified"]]
    for m in CAL["moments"]:
        k = m["moment"]
        rows.append([label[k], _n(m["target"], 3), _n(m["simulated"], 3),
                     _n(est[k], 3), ident[k]])
    return rows


def _t3_rows():
    return [
        ["Statistic", "Model", "External benchmark"],
        ["Expected duration of queueing (years)", _n(_C["queue_years"], 2),
         "Candidates commonly sit the annual examinations two or three times"],
        ["Chance that a cohort member ever holds a rationed job (%)",
         _n(100 * _C["cohort_entry_Q"], 1),
         "Consistent with a sector of 12 per cent of employment and a mean "
         "tenure of about twenty years"],
        ["Mean duration of open search by the young (months)",
         _n(_C["search_months_y"], 1),
         "Graduate surveys report a first-job search of four to six months"],
        ["Rationed hires per year, scaled (millions)",
         _n(_C["cohort_entry_Q"] * 12.7, 2),
         "Central and provincial civil-service, public-institution and "
         "public-teaching intakes combined"],
        ["Queueing entrants, scaled (millions)", _n(_C["u_q"] * 12.7, 2),
         "3.7 million sat the 2026 central examination alone, before "
         "provincial and public-institution examinations"],
        ["Market wage, prime relative to young", _n(_C["w_p"] / _C["w_y"], 3),
         "Not separately targeted; the market sector is homogeneous by "
         "construction, so this understates the true experience premium"],
    ]


TITLE = ("The Queue Absorbs the Shock: Administrative Job Rationing, Delayed "
         "Retirement and the Blind Spot in Youth Unemployment Statistics")

ABSTRACT = (
    "China raised its statutory retirement age from January 2025, and the "
    "obvious worry is that older workers will hold on to jobs the young would "
    "otherwise take. We show that the worry is misdirected and that the "
    "indicator used to monitor it cannot detect what actually happens. In a "
    "two-sector search model, an establishment sector whose headcount is fixed "
    "administratively coexists with a free-entry market sector; because the "
    "rationed sector pays a premium, young workers queue for it as in Harris "
    "and Todaro. Six parameters are estimated to match six Chinese moments "
    "exactly. Three results follow. First, the lump-of-labour hypothesis is "
    "rejected: the crowding-out coefficient is essentially zero. Second, the "
    "chance that a cohort member ever holds a rationed job nonetheless falls "
    "5.7 per cent, about 127,000 young people a year, and a Shapley "
    "decomposition attributes all of it to the establishment's shrinking "
    "replacement flow. Third, the youth unemployment rate moves by 0.03 "
    "percentage points, because three channels of opposite sign almost "
    "exactly cancel: access falls thirty-five times more than the headline "
    "rate moves. The queue itself costs 1.9 per cent of output, and expanding "
    "the establishment—the intuitive remedy—lowers welfare, because a larger "
    "prize draws a longer line."
)

KEYWORDS = ("youth unemployment; delayed retirement; job rationing; "
            "Harris–Todaro queueing; public-sector employment; search and "
            "matching; lump of labour; social indicators; rent seeking; China")

PART_A = [

    # =====================================================================
    ('h1', '1. Introduction'),

    ('p', 'On 1 January 2025 China began raising its statutory retirement age '
          'for the first time since the 1950s: from 60 to 63 for men and from '
          '55 and 50 to 58 and 55 for women, phased over fifteen years '
          '{{nbs2026}}. The reform arrived while the surveyed urban '
          'unemployment rate of 16–24-year-olds excluding students stood at '
          '18.9 per cent, and it revived an old question in a new setting: if '
          'older workers stay longer, do younger workers wait longer? The '
          'question matters beyond China. Every ageing economy is raising '
          'pension ages, and the political economy of doing so turns on '
          'whether the young are made to pay for it.'),

    ('p', 'The economics literature has a settled answer, and it is negative. '
          'Comparative evidence assembled across a dozen countries finds no '
          'systematic tendency for later retirement to displace the young '
          '{{gruber2010}}; theory shows that the two groups are complements '
          'as often as substitutes once vacancy creation is endogenous '
          '{{boeri2022}}; and quasi-experimental work on the United States '
          'finds that a slowdown in retirement did not reduce youth '
          'employment {{mohnen2025}}. The lump-of-labour hypothesis is, in '
          'short, a fallacy. We reproduce that conclusion. What we then show '
          'is that it answers the wrong question in an economy where a large '
          'share of the jobs young people actually compete for is rationed '
          'administratively rather than allocated by a market.'),

    ('p', 'That is the Chinese case, and it is not a detail. Government '
          'agencies and public institutions employ roughly an eighth of the '
          'urban labour force under an establishment system that fixes '
          'headcount by administrative rule. A unit with a full establishment '
          'cannot hire; it can only replace. Its vacancies are therefore its '
          'separations plus its retirements, and since separations are rare, '
          'retirements are the binding source of openings. Meanwhile the '
          'competition for those openings has become extraordinary: 3.718 '
          'million candidates qualified for the 2026 central civil-service '
          'examination, against 38,100 posts, and the age ceiling was raised '
          'from 35 to 38 in the same year. Provincial, public-institution and '
          'public-teaching examinations are larger still. Preparation is '
          'typically full time and frequently repeated.'),

    ('p', 'A labour market with this structure is a coupled system, not a '
          'single market, and a policy shock propagates through it in ways '
          'that a one-sector intuition does not anticipate. We formalise it as '
          'a two-sector, two-age search economy. The rationed sector pays an '
          'administered premium and cannot expand; the market sector has free '
          'entry and a bargained wage. Because the premium is real and the '
          'posts are scarce, young workers queue for them exactly as rural '
          'migrants queue for urban jobs in Harris and Todaro '
          '{{harris1970|zenou2011}}: queueing produces nothing, pays less than '
          'open search, and buys a lottery ticket on a rent. An age ceiling '
          'bars prime-age workers from the examinations, so only the young '
          'queue. Six structural parameters are estimated so that the model '
          'reproduces six Chinese labour-market moments exactly.'),

    ('p', 'Raising the retirement age then acts on the young through three '
          'routes at once, and this is the paper’s organising idea. It shrinks '
          'the establishment’s replacement flow, because fewer incumbents '
          'retire. It lengthens the horizon of every job, which raises what '
          'both sides get from a match and so changes vacancy creation. And it '
          'enlarges the labour force, while the establishment stays fixed. The '
          'three routes do not have the same sign, and they do not reach the '
          'same outcomes.'),

    ('p', 'Four results follow. The first confirms the received wisdom: the '
          'crowding-out coefficient—the change in young employment per unit '
          'change in prime-age employment—is essentially zero. Later '
          'retirement costs the young almost no jobs in aggregate. The second '
          'contradicts the comfort usually taken from that finding. The '
          'probability that a member of an entering cohort ever holds a '
          'rationed job falls by 5.7 per cent, from 17.5 to 16.4 per cent, '
          'which at a cohort of 12.7 million is about 127,000 young people a '
          'year; and a Shapley decomposition attributes the whole of that '
          'fall to the establishment route, with the other two contributing '
          'nothing. Access to the rationed sector is not a job-count question '
          'and the aggregate job count cannot see it.'),

    ('p', 'The third result is about measurement, and it is the one we regard '
          'as most consequential. The youth unemployment rate moves by 0.03 '
          'percentage points over the entire fifteen-year reform. It does so '
          'not because nothing happens but because the three routes almost '
          'exactly cancel in that particular statistic: in log points the '
          'establishment route contributes −1.03, the horizon route +0.66 and '
          'the demographic route +0.52. Access falls about thirty-five times '
          'more than the headline rate moves. A statistic that adds together '
          'people queueing for a rationed rent and people searching an open '
          'market can be insensitive to a large change in what young people '
          'actually obtain. That is a general warning about indicator design, '
          'and an instance of the counterintuitive behaviour of social systems '
          'that motivated systems thinking in the first place '
          '{{forrester1971|meadows1998}}.'),

    ('p', 'The fourth result is a policy warning. The queue is expensive: '
          'young people withdrawn from production to prepare for examinations '
          'forgo output worth 1.9 per cent of gross domestic product in the '
          'estimated economy, and the examinations would have to raise the '
          'productivity of the rationed sector by 46 per cent to justify that '
          'cost. The intuitive remedy—expand the establishment so that more '
          'young people can get in—fails. At a common budget it lowers welfare '
          'and has a marginal value of public funds below one, because a '
          'larger prize draws a longer line, in the classic manner of a '
          'rationed sector that is expanded rather than de-rationed '
          '{{harris1970|krueger1974}}. Cutting the administered premium '
          'dominates: it raises welfare, shrinks the queue, and raises revenue '
          'rather than spending it. It is best in every one of our uncertainty '
          'draws.'),

    ('p', 'The paper contributes to three literatures. To the retirement and '
          'youth employment literature {{gruber2010|boeri2022|mohnen2025}} it '
          'adds an economy in which part of labour demand is administratively '
          'rationed, and shows that the aggregate no-crowding-out result '
          'survives while a distributional result of comparable importance '
          'does not. To the literature on rationed public employment and '
          'rent-seeking queues '
          '{{harris1970|krueger1974|gelb1991|murphy1991}} it supplies a '
          'quantitative, estimated application to the largest such queue in '
          'the world, and a decomposition of what a demographic policy does to '
          'it. And to the systems literature on indicators '
          '{{forrester1971|meadows1998|goodhart1984}} it supplies a fully '
          'worked case in which a headline statistic is uninformative for a '
          'reason that can be measured rather than merely asserted.'),

    ('p', 'Section 2 places the paper in the literature. Section 3 sets out '
          'the model and defines equilibrium. Section 4 describes the '
          'calibration, its identification and its over-identifying checks. '
          'Section 5 reports the reform counterfactual, the decomposition, the '
          'indicator result, the policy comparison and the robustness '
          'analysis. Section 6 discusses interpretation and limitations, and '
          'Section 7 concludes.'),

    # =====================================================================
    ('h1', '2. Related Literature'),

    ('h2', '2.1. Retirement Age and Youth Employment'),

    ('p', 'The proposition that jobs vacated by the old are taken by the young '
          'is the lump-of-labour hypothesis, and it has been tested more '
          'thoroughly than most propositions in labour economics. The '
          'comparative project assembled by Gruber and Wise across twelve '
          'countries found no evidence that inducing older workers to retire '
          'raises youth employment, and often the reverse {{gruber2010}}. '
          'Boeri, Garibaldi and Moen showed theoretically that with endogenous '
          'vacancy creation the sign depends on whether the two groups are '
          'substitutes in production and on how firms adjust hiring, and that '
          'complementarity is the more common configuration {{boeri2022}}. '
          'Mohnen exploited the slowdown in United States retirement to '
          'estimate the effect directly and found no adverse effect on youth '
          'employment, though he documents composition effects within firms '
          '{{mohnen2025}}. Evidence from pension reforms in Norway and from '
          'ageing simulations elsewhere points the same way '
          '{{vestad2013|martins2009}}. The one setting in which displacement '
          'is reliably found is the internal labour market: exploiting the '
          '2011 Italian pension reform, Bianchi and co-authors show that '
          'delayed retirements slow the promotions of younger colleagues, but '
          'only in firms whose promotion ladders are short {{bianchi2023}}. '
          'That is the same logic as ours—a fixed number of slots—applied '
          'inside the firm rather than to a sector. For China specifically, '
          'computable general-equilibrium work finds the retirement extension '
          'raises growth without displacing the young {{jiang2025}}, and '
          'projections of the pension system make clear that the reform will '
          'not be reversed {{gao2025}}. Our contribution is not to overturn '
          'this consensus—we reproduce it—but to show that in an economy with '
          'administrative rationing the aggregate employment test is not '
          'informative about the distributional question that motivates the '
          'political debate.'),

    ('h2', '2.2. Rationed Sectors, Queues and Rent Seeking'),

    ('p', 'When a sector pays above the market-clearing wage and cannot expand '
          'to meet the resulting supply, entry to it is rationed and workers '
          'queue. Harris and Todaro built the canonical model for rural–urban '
          'migration, in which expected-income equalisation drives queueing '
          'and generates equilibrium unemployment that is a pure social cost '
          '{{harris1970}}; Zenou surveys the modern search-theoretic versions '
          '{{zenou2011}}. The activity of queueing is rent seeking in '
          'Krueger’s sense: resources are expended to capture a transfer '
          'rather than to create output {{krueger1974}}. Where the rationed '
          'sector is the state, the consequences are magnified, because the '
          'queue diverts precisely the workers whose alternative use is most '
          'productive—the allocation-of-talent problem set out by Murphy, '
          'Shleifer and Vishny {{murphy1991}}—and because public employment '
          'premia are themselves a policy choice, as Gelb, Knight and Sabot '
          'showed for developing economies {{gelb1991}} and as a ninety-one-'
          'country dataset confirms {{gindling2020}}. The empirical study of '
          'examination queues is recent and small. Mangal exploits a hiring '
          'freeze in Tamil Nadu and finds that when the odds worsen, '
          'candidates prepare longer rather than leave the queue, and that a '
          'decade later the affected cohorts have lower employment, lower '
          'earning capacity and delayed household formation {{mangal2024}}; '
          'Armijos Bravo and Vall Castelló document behavioural responses to '
          'examination competition in Spain {{armijos2025}}. Both findings '
          'are exactly what the indifference condition in our model implies. '
          'China’s examination '
          'queue is, by some margin, the largest instance of this structure '
          'now in existence, and it has grown steadily: qualified candidates '
          'for the central civil-service examination rose from about 2.6 '
          'million in 2023 to 3.718 million in 2026 while posts grew far more '
          'slowly. We supply an estimated general-equilibrium model of it.'),

    ('h2', '2.3. Search, Matching and Two-Sector Labour Markets'),

    ('p', 'The equilibrium environment is the Diamond–Mortensen–Pissarides '
          'framework {{diamond1982|mortensen1994|pissarides2000|rogerson2005}}, '
          'whose matching function is empirically well established '
          '{{petrongolo2001}} and whose efficiency properties are governed by '
          'the Hosios condition {{hosios1990}}. We impose that condition '
          'throughout, so that the market sector is efficient by construction '
          'and every distortion we report comes from the rationed sector. The '
          'two-sector structure, with one sector rationed and one free, is '
          'closer to the development literature than to the standard '
          'macro-labour setting, and the interaction between the two is what '
          'generates our results. Competitive-search alternatives '
          '{{moen1997}} would change the wage rule but not the rationing '
          'mechanism, which is administrative rather than economic. A small '
          'literature already embeds a public sector in this framework: '
          'Albrecht, Robayo-Abril and Vroman study public wage and employment '
          'policy in a calibrated Diamond–Mortensen–Pissarides economy '
          '{{albrecht2019}}, Chassamboulli and Gomes add the education '
          'decision {{chassamboulli2023}}, and Zhang shows for China that '
          'acyclical public hiring amplifies aggregate fluctuations '
          '{{zhangx2024}}. In all three the public sector chooses its '
          'employment level. Ours cannot: the headcount is an administrative '
          'constant, which is what makes the retirement hazard the binding '
          'determinant of entry.'),

    ('h2', '2.4. Indicators and the Behaviour of Social Systems'),

    ('p', 'A statistic used to steer a system eventually shapes it, and may '
          'stop measuring what it was chosen to measure '
          '{{goodhart1984|meadows1998}}. Forrester’s argument that social '
          'systems respond counterintuitively to intervention, because the '
          'observable symptoms and the causal structure are only loosely '
          'connected, is the systems-theoretic statement of the same idea '
          '{{forrester1971}}. Youth transition outcomes have increasingly been '
          'approached in this spirit, as emergent properties of interacting '
          'institutions rather than as the sum of individual choices '
          '{{grigorescu2025|chacon2025|chen2026|stw}}. Our result is a sharp, '
          'quantified instance. The measurement literature has responded to the '
          'same concern by broadening the definition of slack—Houston and '
          'Lindsay construct full-time-equivalent utilisation rates that '
          'reveal considerably more of it, particularly among the young '
          '{{houston2025}}—but a broader unemployment measure would not '
          'detect what we describe, because the people affected are employed. '
          'What is needed is a different object, not a wider one. We can say '
          'exactly why the headline rate does '
          'not move, decompose the offsetting forces, and measure how much '
          'larger the change in access is than the change in the indicator.'),

    ('h2', '2.5. The Chinese Setting'),

    ('p', 'Three features of China make the mechanism unusually visible. The '
          'entering cohort is enormous and still growing: 12.22 million '
          'graduates in 2025 and 12.7 million expected in 2026 {{moe2026}}. '
          'The rationed sector is large, stable and highly attractive, and its '
          'compensation premium is understated by wage data because pension, '
          'housing and security provisions are the larger part of it. And '
          'mismatch, over-education and delayed entry are extensively '
          'documented {{china_youth1|china_youth2|mismatch2|mismatch1|pan2025}}, '
          'so the phenomenon of full-time examination preparation is measured '
          'well enough to discipline a model. Recent international work has '
          'linked youth transition difficulties to structural rather than '
          'cyclical forces {{ilo1|oecd2025|tleppayev2025|basol}}, which is the '
          'reading our results support. Two further Chinese features matter for '
          'interpretation: vocational education offers a route into the '
          'labour market that does not run through the examination queue and '
          'that carries a measurable return {{vet1}}, and the quality rather '
          'than the quantity of youth employment has become the object of '
          'policy attention {{liang2024|liu2024sus}}.'),

    # =====================================================================
    ('h1', '3. A Two-Sector Model with Administrative Rationing'),

    ('p', 'Time is continuous, agents are risk neutral and discount at rate '
          '⟪r⟫. Workers enter the labour market at age ⟪a_{0}⟫ in a flow ⟪n⟫, '
          'are young for ⟪T_{y}⟫ years and prime-age thereafter until they '
          'retire at age ⟪R⟫. The two hazards implied by that structure are'),
    ('eq', 'eq1', 1),
    ('p', 'so that raising the statutory retirement age lowers ⟪\\rho⟫. Figure '
          '1 shows the seven states and the flows between them.'),

    ('figure', 'fig1_structure.png', 1,
     'Structure of the model. Solid arrows are matching flows, dashed arrows '
     'are ageing, separation and retirement. The rationed sector cannot '
     'expand: its headcount is fixed at ⟪\\bar{N}⟫ by administrative rule, so '
     'its only vacancies are its separations plus its retirements. An age '
     'ceiling on the examinations means that only the young queue, and the '
     'young who age out of the queue without a post join open search. The '
     'market sector has free entry, so its tightness ⟪\\theta⟫ adjusts. Every '
     'prime-age state exits to retirement at rate ⟪\\rho⟫; the figure draws '
     'the flow only from the rationed sector, which is the one the reform '
     'acts through.'),

    ('h2', '3.1. Matching and Flows'),

    ('p', 'The market sector has a constant-returns Cobb–Douglas matching '
          'function over effective searchers and vacancies. The young search '
          'less effectively than the prime-age, at relative efficiency '
          '⟪\\mu_{y}⟫:'),
    ('eq', 'eq2', 2),
    ('p', 'which gives the job-finding and vacancy-filling rates'),
    ('eq', 'eq3', 3),
    ('p', 'Young workers are distributed across queueing ⟪u_{q}⟫, open search '
          '⟪u_{m}⟫, a rationed job ⟪e_{q}⟫ and a market job ⟪e_{m}⟫; their '
          'stocks evolve as'),
    ('eq', 'eq4', 4),
    ('eq', 'eq5', 5),
    ('p', 'where ⟪I_{y}⟫ is the inflow into young non-employment and '
          '⟪a_{q}⟫ the share of it that joins the queue. Prime-age workers '
          'cannot queue, so they occupy three states:'),
    ('eq', 'eq6', 6),
    ('eq', 'eq7', 7),

    ('h2', '3.2. The Establishment Constraint'),

    ('p', 'The rationed sector is defined by an administrative ceiling on '
          'headcount rather than by a hiring decision. Its employment is fixed '
          'and its vacancies are exactly what it loses:'),
    ('eq', 'eq8', 8),
    ('p', 'The second equality is the pivot of the paper. Because separations '
          'from establishment posts are rare, retirements are the binding '
          'source of openings, and the retirement hazard enters the '
          'vacancy flow directly. A policy that lowers ⟪\\rho⟫ lowers ⟪v_{Q}⟫ '
          'mechanically, and no adjustment on the firm’s side offsets it, '
          'because there is no firm-side decision to adjust. This is what '
          'distinguishes a rationed sector from a market one: in the market '
          'sector free entry restores vacancy creation, and in the rationed '
          'sector nothing does.'),
    ('p', 'Applicants are allocated across the available posts by examination, '
          'which we treat as a lottery among those who prepare. The hazard of '
          'winning a post is therefore the ratio of openings to queuers:'),
    ('eq', 'eq9', 9),

    ('h2', '3.3. Values and Wages'),

    ('p', 'Market matches are worth more to a firm when the worker is young, '
          'because the match is not yet exposed to retirement. Writing '
          '⟪J_{i}⟫ for the firm’s value and ⟪\\Delta_{i}⟫ for the worker’s '
          'surplus,'),
    ('eq', 'eq10', 10),
    ('eq', 'eq11', 11),
    ('p', 'Wages are set by Nash bargaining over each match surplus with '
          'worker bargaining power ⟪\\beta⟫:'),
    ('eq', 'eq12', 12),
    ('p', 'and the values of search follow:'),
    ('eq', 'eq13', 13),
    ('p', 'A rationed job pays the administered wage ⟪w_{Q}⟫, which is not '
          'bargained, and is held until separation or retirement:'),
    ('eq', 'eq14', 14),

    ('h2', '3.4. The Queue'),

    ('p', 'A young worker who queues forgoes open search entirely: preparation '
          'is full time, so the two activities are mutually exclusive. '
          'Queueing yields the flow value ⟪\\kappa_{q} b⟫, which is below the '
          'value of open search and, once preparation courses are paid for, '
          'may be negative. In an interior equilibrium the two activities must '
          'be equally attractive, which is the Harris–Todaro condition:'),
    ('eq', 'eq15', 15),
    ('p', 'This pins the queue. Solving for the hazard and inverting the '
          'definition in (9) gives the queue length directly:'),
    ('eq', 'eq16', 16),
    ('p', 'The comparative statics are worth stating because they drive '
          'everything that follows. Anything that raises the value of a '
          'rationed job relative to open search lowers ⟪\\lambda_{Q}⟫, which '
          'is to say it lengthens the queue per opening. Anything that '
          'reduces the number of openings lowers ⟪u_{q}⟫ for a given hazard. '
          'A later retirement age does both at once: it makes the post more '
          'valuable, because it is held for longer, and it makes posts rarer.'),

    ('h2', '3.5. Equilibrium'),

    ('p', 'Firms in the market sector post vacancies until the expected cost '
          'of filling one equals its expected value, where the value is '
          'averaged over the composition of searchers:'),
    ('eq', 'eq17', 17),
    ('p', 'A steady-state equilibrium is a tightness ⟪\\theta⟫, a queue hazard '
          '⟪\\lambda_{Q}⟫, wages and stocks such that all stocks are '
          'stationary, wages solve the bargaining problem, the establishment '
          'constraint holds, the indifference condition (15) holds and free '
          'entry (17) holds. The system is recursive: given ⟪\\theta⟫, wages '
          'and values follow in closed form, (16) delivers the queue, the '
          'stock equations deliver the remaining states, and (17) is a single '
          'equation in ⟪\\theta⟫. Every equilibrium reported below was located '
          'by bracketing that equation on a scan of the whole admissible '
          'range, so it is a global rather than a local solution.'),

    ('h2', '3.6. Output, Welfare and the Cost of the Queue'),

    ('p', 'Output is produced by employment in both sectors, and welfare adds '
          'the value of non-market time and subtracts recruiting costs:'),
    ('eq', 'eq18', 18),
    ('eq', 'eq19', 19),
    ('p', 'The queue has a distinctive welfare status. The establishment hires '
          '⟪v_{Q}⟫ workers however long the line is, so at the margin '
          'queueing produces nothing; its whole social cost is the output the '
          'queuers would otherwise have produced, net of what they enjoy while '
          'preparing:'),
    ('eq', 'eq20', 20),
    ('p', 'This is the Harris–Todaro deadweight loss and it is the largest '
          'single distortion in the estimated economy. Because assuming that '
          'the examinations have no social value at all is strong, Section 5.8 '
          'reports the opposite calculation: the productivity gain the '
          'examinations would have to deliver, through better selection, for '
          'the observed queue to be efficient.'),
    ('p', 'Finally, the object the retirement debate is really about is the '
          'crowding-out coefficient, the change in young employment per unit '
          'change in prime-age employment:'),
    ('eq', 'eq21', 21),
    ('p', 'A lump-of-labour world has ⟪\\Xi = -1⟫; a world in which the two '
          'groups do not compete has ⟪\\Xi = 0⟫.'),

    ('p', 'Three distinct routes run from a later retirement age to the '
          'young, and Figure 2 sets them out because the rest of the paper is '
          'an accounting of their relative size. The quota route is the one '
          'just described: fewer retirements mean fewer establishment '
          'vacancies. The horizon route works through values rather than '
          'flows, since a job that will be held for longer is worth more to '
          'both sides of the match. The demographic route is the slowest and '
          'the least discussed: the labour force keeps growing while '
          '⟪\\bar{N}⟫ does not, so the rationed sector shrinks as a share of '
          'employment whatever the retirement age does. The three do not share '
          'a sign, and Section 5.4 shows that in the headline indicator they '
          'very nearly cancel.'),

    ('figure', 'fig2_mechanism.png', 2,
     'The three routes from a later retirement age to young workers, and the '
     'decomposition of Section 5.4. The figures on the right are Shapley '
     'contributions to the change in the youth unemployment rate over the '
     'full reform, in log points multiplied by one hundred. Only the quota '
     'route reaches the chance that a new entrant ever holds a rationed job; '
     'the other two routes offset it in the indicator without touching it.'),

    # =====================================================================
    ('h1', '4. Calibration'),

    ('p', 'The model is calibrated to China in 2025 at annual frequency. Three '
          'normalisations come first because they determine what can be '
          'identified. Market productivity is the numeraire. Matching '
          'efficiency in the prime tier is set to one, because matching '
          'efficiency and vacancy cost enter every equilibrium object only '
          'through ⟪\\mu_{i}^{2}/c_{M}⟫. And rationed-sector productivity is '
          'set equal to market productivity, so that the administered premium '
          'is a pure rent rather than a return to unobserved productivity; '
          'nothing in the allocation depends on that choice, and Section 5.8 '
          'varies it. What remains is six parameters and six moments. The '
          'system is square, so rather than minimising a distance that stays '
          'positive at the optimum we solve the moment conditions exactly:'),
    ('eq', 'eq22', 22),
    ('p', 'A bounded least-squares solve reaches a maximum absolute log '
          'deviation of ' + ("%.1e" % CAL["max_log_resid"]) + ' across all six '
          'conditions, so every target is matched to machine precision.'),

    ('h2', '4.1. Externally Set Parameters'),

    ('p', 'Table 1 lists what is fixed outside the estimation. The young tier '
          'runs from age 23 to 30, which is where the examination age ceiling '
          'historically bound; the 2026 relaxation of that ceiling from 35 to '
          '38 is discussed in Section 6. The pre-reform effective retirement '
          'age of 56.3 is the employment-weighted average of 60 for men, 55 '
          'for women in cadre posts and 50 for women in worker posts, and the '
          'post-reform value of 59.9 is the corresponding average of 63, 58 '
          'and 55. Separation from an establishment post is set at 2 per cent '
          'a year against 18 per cent in the market sector, which is the '
          'quantitative expression of what the phrase "iron rice bowl" '
          'describes. The matching elasticity is 0.5 and worker bargaining '
          'power is set equal to it, so the Hosios condition holds exactly and '
          'the market sector is efficient by construction; every distortion we '
          'report is therefore attributable to rationing rather than to an '
          'assumption about bargaining.'),

    ('tabcap', '1', 'Parameters set outside the estimation, and the three '
                    'normalisations that determine what is identified.'),
    ('table', _t1_rows(), [2820, 900, 800, 5120]),

    ('notes', 'Matching efficiency and the vacancy cost enter every '
              'equilibrium object only through ⟪\\mu_{i}^{2}/c_{M}⟫, so one '
              'of the two must be normalised; the units of output and of the '
              'entrant cohort are likewise free.'),

    ('h2', '4.2. Estimated Parameters and Targeted Moments'),

    ('p', 'The six estimated parameters are the market vacancy cost, the size '
          'of the establishment, the administered wage, the flow value of open '
          'search, the flow value while queueing and the matching efficiency '
          'of the young. Table 2 reports the targets, the fit and the '
          'parameter each moment principally identifies; the mapping is close '
          'to one-to-one and can be read off the recursive structure of the '
          'model. Two of the six targets deserve comment. The rationed sector '
          'is defined as government agencies and public institutions, about 12 '
          'per cent of urban employment, and deliberately excludes commercial '
          'state-owned enterprises, which hire without an establishment '
          'ceiling and so do not belong to the mechanism. And the '
          'compensation premium of 1.25 is a compensation-equivalent figure '
          'including pension, housing and security provisions, not a wage '
          'premium; the wage gap alone is much smaller.'),

    ('tabcap', '2', 'Targeted moments, the fit, and the parameter each moment '
                    'principally identifies.'),
    ('table', _t2_rows(), [2680, 820, 820, 940, 4380]),

    ('notes', 'The system is square, so the fit is exact by construction; '
              'what the table reports is that an exact solution exists inside '
              'the admissible parameter space, which is not guaranteed and '
              'which failed for a broader definition of the rationed sector '
              'that included commercial state-owned enterprises. The negative '
              'estimate of ⟪\\kappa_{q}⟫ says that a full-time candidate is '
              'worse off during preparation than an open searcher, once '
              'courses, materials and forgone casual work are counted.'),

    ('h2', '4.3. Over-Identifying Checks'),

    ('p', 'Several statistics are computed but never targeted. Table 3 reports '
          'them, and one deserves emphasis. Three separately sourced '
          'targets—a rationed sector of 12 per cent of employment, a queue '
          'accounting for 35 per cent of youth non-employment, and a youth '
          'unemployment rate of 17.8 per cent—jointly imply an expected '
          'queueing duration of ' + _n(_C["queue_years"], 2) + ' years. That '
          'is not a target; it is an implication. It matches the independent '
          'observation that successful candidates commonly sit the annual '
          'examinations two or three times, which is a genuine consistency '
          'check across data sources that had no reason to agree.'),

    ('p', 'Scaled to a cohort of 12.7 million, the estimated economy has '
          + _n(_C["u_q"] * 12.7, 1) + ' million young people queueing full '
          'time and ' + _n(_C["cohort_entry_Q"] * 12.7, 1) + ' million '
          'rationed hires a year. Both are the right order of magnitude: 3.7 '
          'million candidates qualified for the central civil-service '
          'examination alone in 2026, before provincial, public-institution '
          'and public-teaching examinations are counted. The mean duration of '
          'open search by the young comes out at '
          + _n(_C["search_months_y"], 1) + ' months, close to what graduate '
          'surveys report. One check is weak by construction: the market '
          'sector is homogeneous, so the model produces almost no experience '
          'premium within it, and the true premium is larger. That limits what '
          'the model can say about wage profiles, though not about the '
          'rationing mechanism, which is what it is built for.'),

    ('tabcap', '3', 'Over-identifying checks: model statistics that were '
                    'never targeted, against independent evidence.'),
    ('table', _t3_rows(), [3560, 900, 5180]),

    ('notes', 'Scaled figures use an entering cohort of 12.7 million, the '
              'expected size of the 2026 graduating class, and an urban '
              'labour force '
              'of 423 million.'),
]
