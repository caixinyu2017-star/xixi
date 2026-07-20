# -*- coding: utf-8 -*-
"""Paper 6 content, part A: front matter, Introduction, Theory, Methods."""
import json, os

S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p6_stats.json')))
REL = S['reliability']

TITLE = ("Leadership and Decision Making in Digitally Transforming Enterprises: "
         "Multivariate Modeling and Cluster Typologies of Decision Agility and "
         "Young Managerial Advancement")

ABSTRACT = (
    "Navigating digital transformation is, at its core, an exercise in leadership and decision "
    "making: executives must decide what to digitalize, how to decide with data and artificial "
    "intelligence, and who is given a seat at the decision table. This paper examines how four "
    "leadership and decision-making practices—digital transformation leadership, the breadth of "
    "AI-assisted managerial decision-making, the digitalization of decision processes, and the "
    "involvement of young employees in transformation decisions—relate to two outcomes of "
    "today's enterprise systems: organizational decision agility and the advancement of young "
    "people into management. Evidence comes from an executive survey of 285 enterprises in "
    "China's Yangtze River Delta. The methodology combines MANOVA-type multivariate general "
    "linear models, exploratory factor analysis, and hierarchical plus k-means clustering. "
    "Results indicate differentiated associations: transformation leadership and digitalized "
    "decision processes are significantly associated with both greater agility and a larger "
    "share of young managers, whereas AI-assisted decision-making is associated with agility "
    "but only marginally with young managerial presence, and youth involvement shows the "
    "reverse pattern. A single latent factor—the leadership–decision configuration—underlies "
    "the four practices and is significantly associated with both outcomes, although AI "
    "breadth and youth involvement carry the lowest communalities. Cluster analysis identifies "
    "two decision regimes: an agile, digitally led regime with younger management and a "
    "conventional hierarchical regime, a distinction that cuts across sectors. The findings "
    "portray decision agility and managerial rejuvenation as joint properties of "
    "socio-technical decision systems rather than by-products of technology adoption, without "
    "implying causal relationships."
)

KEYWORDS = ("digital transformation; leadership; decision making; artificial intelligence; "
            "decision agility; young managers; employee involvement; socio-technical systems; "
            "multivariate general linear model; cluster analysis")

_a = REL['alpha']; _o = REL['omega']

def _pct(x):
    return f"{100 * x / S['n']:.1f}"

_T1_ROWS = [['Characteristic', 'Category', 'n', '%']]
_rows = []
_rows.append(('Region', 'Shanghai', S['profile_region']['Shanghai']))
_rows.append(('', 'Jiangsu', S['profile_region']['Jiangsu']))
_rows.append(('', 'Zhejiang', S['profile_region']['Zhejiang']))
_rows.append(('', 'Anhui', S['profile_region']['Anhui']))
_rows.append(('Sector', 'Digital-core (ICT, e-commerce)', S['profile_sector']['digital-core']))
_rows.append(('', 'Manufacturing', S['profile_sector']['manufacturing']))
_rows.append(('', 'Other services', S['profile_sector']['services']))
for band in ('20-49', '50-249', '250-999', '1000+'):
    _rows.append(('Firm size (employees)' if band == '20-49' else '',
                  band.replace('-', '–'), S['profile_size'][band]))
for own, lab in (('private', 'Private'), ('state', 'State-owned'),
                 ('foreign', 'Foreign-invested'), ('other', 'Other')):
    _rows.append(('Ownership' if own == 'private' else '', lab, S['profile_ownership'][own]))
for band, lab in (('3-7', '3–7'), ('8-14', '8–14'), ('15-24', '15–24'), ('25+', '25+')):
    _rows.append(('Firm age (years)' if band == '3-7' else '', lab, S['profile_age'][band]))
for role, lab in (('CEO/GM', 'CEO / general manager'),
                  ('Deputy GM/strategy VP', 'Deputy GM / strategy executive'),
                  ('CIO/CDO/senior executive', 'CIO / CDO / other senior executive')):
    _rows.append(('Respondent role' if role == 'CEO/GM' else '', lab, S['profile_role'][role]))
for ch, cat, cnt in _rows:
    _T1_ROWS.append([ch, cat, str(cnt), _pct(cnt)])

PART_A = [
    ('h1', '1. Introduction'),

    ('p', "Beneath every digital transformation lies a stream of decisions. Executives decide "
     "which processes to digitalize, whether forecasts and budgets should be produced by "
     "algorithms or by argument, how quickly the organization must respond when markets move, "
     "and—less visibly—who is entitled to participate in these choices {{vial2019|shrestha2019|"
     "ddm1}}. The Special Issue theme that motivates this study frames digital transformation "
     "precisely in these terms: as a challenge of leadership and decision making in today's "
     "systems. Yet empirical research has typically studied leadership, decision processes, and "
     "the human side of transformation in isolation. How the leadership and decision-making "
     "practices of digitally transforming enterprises hang together, and what organizational "
     "properties accompany them, remains an open systemic question {{dl1|stsd1|sts4}}."),

    ('p', "Two such properties are of particular interest. The first is decision agility—the "
     "capacity to make fast, high-quality decisions under uncertainty—which a long research "
     "tradition links to performance in turbulent environments {{eisenhardt1989|baum2003|"
     "teece_agility}} and which digital technologies promise to enhance {{agility_dt|bda1}}. "
     "The second is generational: who rises into management while the enterprise transforms. "
     "China's discussion of youth employment has concentrated on entry into work, but career "
     "advancement into managerial roles is the stage at which young people begin to shape "
     "organizations rather than merely join them {{young_promotion|career1|china_youth2}}. "
     "Recent evidence that younger chief executives are associated with deeper corporate "
     "digital transformation suggests that rejuvenated management and digital capability may "
     "be mutually constitutive {{tmt_age_digital|upper1}}. Whether the everyday leadership and "
     "decision practices of firms are systematically related to the presence of young people "
     "in management has, to our knowledge, not been examined."),

    ('p', "The purpose of this article is to analyze how four leadership and decision-making "
     "practices relate jointly to decision agility and to young managerial advancement in "
     "enterprises navigating digital transformation. The practices are digital transformation "
     "leadership (DLV), the breadth of AI-assisted managerial decision-making across decision "
     "domains (ADM), the digitalization of decision processes (DPD), and the involvement of "
     "young employees in transformation decisions (EDI). The outcomes are organizational "
     "decision agility (ODA) and young managerial presence (YMP), measured as the share of "
     "managerial positions held by employees aged 35 or younger. The empirical setting is the "
     "Yangtze River Delta—Shanghai, Jiangsu, Zhejiang, and Anhui—China's most economically "
     "integrated macro-region and a national testbed for digital-economy policy "
     "{{zhejiang1|ses_regional|digital_emp2}}."),

    ('p', "Three gaps motivate the design. First, research on AI in managerial decision making "
     "has advanced conceptually {{shrestha2019|aidm1|ddm2}} and experimentally "
     "{{csaszar_ai|genai2}}, but firm-level survey evidence connecting the breadth of "
     "AI-assisted deciding to organizational outcomes remains scarce, particularly outside "
     "North America and Europe {{systems_ai_dm|ai_adopt_sme}}. Second, decision agility is "
     "usually explained by structure and capability {{teece_agility|baum2003}}, seldom by the "
     "configuration of concrete decision practices that leaders install. Third, the literature "
     "on young people at work addresses attraction and retention {{genz_work|china_newgen|employer_attract}} "
     "far more often than advancement; the demand-side question of which organizational "
     "practices accompany young people's access to managerial authority is largely unexplored "
     "{{youth_demand_side|young_promotion}}. There is also little research treating these "
     "elements as one socio-technical configuration rather than separate levers {{sts2|"
     "stsd2}}."),

    ('p', "We address these gaps with a quantitative, cross-sectional executive survey and an "
     "integrated analytical strategy. Four MANOVA-type multivariate general linear models "
     "estimate the associations between each practice and the two correlated outcomes; "
     "exploratory factor analysis tests whether the practices express a common latent "
     "leadership–decision configuration; and hierarchical plus k-means clustering recovers "
     "emergent decision regimes among firms. Covariate-adjusted models and supplementary "
     "correlations bound the role of structural firm characteristics. The design therefore "
     "yields three complementary readings of the same system: bivariate, latent, and "
     "configurational {{kmeans_biz|hair}}."),

    ('p', "The study contributes to the literature in four ways. First, it brings the two "
     "signature outcomes of the digital-transformation debate—agility and human capital—into "
     "a single organizational analysis, showing that they attach to partly different "
     "practices. Second, it offers among the first firm-level evidence on the breadth of "
     "AI-assisted managerial decision-making in Chinese enterprises, distinguishing its "
     "agility correlates from its (weaker) generational correlates. Third, it introduces "
     "young managerial presence as a demand-side indicator of youth career development and "
     "links it to concrete decision practices, notably the involvement of young employees in "
     "transformation decisions. Fourth, methodologically, it demonstrates how multivariate "
     "modeling, factor analysis, and clustering can be combined on primary survey data to "
     "describe leadership–decision systems at three levels of aggregation."),

    ('p', "The remainder of the paper proceeds as follows. Section 2 develops the theoretical "
     "framework and hypotheses. Section 3 describes the sample, measures, and statistical "
     "methods. Section 4 reports the results of the multivariate models, the factor analysis, "
     "and the cluster analysis. Section 5 discusses the findings, their theoretical and "
     "practical implications, and the study's limitations. Section 6 concludes."),

    ('h1', '2. Theoretical Framework, Literature Review, and Hypotheses Development'),

    ('p', "Three theoretical lenses structure the analysis. Upper echelons theory holds that "
     "organizations reflect the cognitions and choices of their leaders, so that observable "
     "practices—what is digitalized, how decisions are made, who participates—encode the "
     "leadership orientation of the firm {{upper1|upper2|ceo_digital}}. Organizational "
     "information-processing theory views decision arrangements as mechanisms that match "
     "information-processing capacity to task uncertainty; digital tools, AI models, and "
     "participative channels are alternative (and complementary) ways of expanding that "
     "capacity {{oipt|shrestha2019}}. The socio-technical systems tradition, finally, insists "
     "that the technical apparatus of deciding and the social order of deciding must be "
     "designed jointly: dashboards without empowered users, or algorithms without legitimate "
     "decision rights, yield little {{sts1|sts_ai|sts3|stsd1}}. Together these lenses imply that "
     "decision agility and the generational composition of management are not independent "
     "accidents but joint expressions of how the leadership–decision system is configured "
     "{{sts4|teece}}."),

    ('h2', '2.1. Leadership and Decision-Making Practices, Agility, and the Advancement of the Young'),

    ('p', "Digital transformation leadership—articulating a digital vision, championing "
     "change, and enabling experimentation—is the most studied practice of the four "
     "{{dl1|dl3|zeike2019}}. Leadership of this kind compresses decision paths: it legitimates "
     "action under uncertainty, reduces escalation, and aligns middle management around "
     "shared priorities, all of which the decision-speed literature identifies as "
     "accelerants {{eisenhardt1989|dl2}}. The same leadership plausibly opens the managerial "
     "ladder to younger employees, both because transformation creates new digitally "
     "intensive management roles for which recent cohorts are well suited {{digital_emp1|"
     "im_hc}} and because digitally oriented executives value the technological fluency of "
     "the young when staffing them {{tmt_age_digital|genz_work}}."),

    ('p', "AI-assisted managerial decision-making extends algorithmic support from operations "
     "into the managerial core: forecasting, budgeting, pricing, staffing, and strategic "
     "scenario analysis {{shrestha2019|csaszar_ai}}. Where such support is broad, decisions "
     "can be delegated to hybrid human–machine routines that respond faster than committee "
     "cycles, and experimental evidence indicates that AI support particularly accelerates "
     "structured evaluations {{genai2|genai3|aidm1}}. Its generational implications are, however, "
     "ambivalent. Algorithmic support may substitute for exactly the junior analytical roles "
     "through which young managers once proved themselves {{acemoglu2019|genai1|robots_china_firm}}, and "
     "delegating judgment to models does not by itself redistribute decision rights toward "
     "younger people {{shrestha2019|budhwar2023}}. We therefore expect the breadth of "
     "AI-assisted decision-making to be associated primarily with agility, with a weaker "
     "association with young managerial presence."),

    ('p', "The digitalization of decision processes—real-time dashboards, a shared factual "
     "basis for meetings, systematic post-decision review—raises the quality and tempo of "
     "organizational choice by shortening the distance between events and responses "
     "{{ddm1|bda1|ghasemaghaei}}. Information-processing theory predicts agility gains "
     "{{oipt}}, and evidence links data-driven cultures to innovation and responsiveness "
     "{{ddd_perf|agility_dt}}. Digitalized decision processes should also favor the young in "
     "a subtler way: when decisions are argued from shared data rather than from seniority, "
     "the authority premium of tenure declines and demonstrated analytical competence—more "
     "evenly distributed across age groups—matters more {{china_newgen|mismatch2}}."),

    ('p', "Involving young employees in transformation decisions—through cross-level digital "
     "councils, reverse mentoring, young-talent task forces, and idea platforms—is the most "
     "explicitly generational of the four practices {{reverse_mentor|voice_part}}. Voice "
     "research shows that participation improves decision inputs and signals that "
     "contributions are valued {{voice_part}}; reverse mentoring additionally moves digital "
     "knowledge upward while moving visibility downward, placing young employees on the "
     "radar of senior sponsors {{reverse_mentor}}. We accordingly expect involvement to be "
     "associated above all with young managerial presence. Its agility association is less "
     "clear-cut: broader participation enriches information but also multiplies voices in "
     "the room, and the net effect on decision speed is theoretically contested "
     "{{eisenhardt1989|voice_part}}. Taken together, these arguments justify the following "
     "hypothesis:"),

    ('hyp', 'Hypothesis H1.', "The four leadership and decision-making practices—digital "
     "transformation leadership, AI-assisted decision-making breadth, decision-process "
     "digitalization, and young-employee decision involvement—show significant "
     "cross-sectional associations with organizational decision agility and young managerial "
     "presence."),

    ('h2', '2.2. The Latent Leadership–Decision Configuration'),

    ('p', "Although the four practices are conceptually distinct, they are unlikely to be "
     "adopted independently. Leaders who champion transformation tend also to digitalize "
     "decision processes; firms that build AI into managerial routines usually do so on a "
     "foundation of data-driven practice; and participative channels are easier to open "
     "where leadership already sponsors change {{vial2019|dl2|ai_adopt_sme}}. The dynamic "
     "capabilities perspective interprets this covariation as a higher-order managerial "
     "capacity to sense, decide, and reconfigure {{teece|upper_digital}}; the socio-technical "
     "perspective interprets it as joint optimization of the technical and social sides of "
     "deciding {{sts2|sts_ai}}. Both predict a common latent dimension—a leadership–decision "
     "configuration—beneath the observable practices. If the configuration, rather than any "
     "single practice, is what matters systemically, its factor score should relate to both "
     "outcomes. This reasoning justifies the following hypothesis:"),

    ('hyp', 'Hypothesis H2.', "A common latent factor—the leadership–decision "
     "configuration—underlies the four practice indicators and is significantly associated "
     "with both organizational decision agility and young managerial presence."),

    ('h2', '2.3. Decision Regimes as Socio-Technical Typologies'),

    ('p', "Configurational research cautions against assuming that firms array smoothly along "
     "a single continuum: attributes cluster into discrete, internally coherent bundles "
     "{{kmeans_biz|jain}}. In decision-making terms, organizational theory has long "
     "contrasted regimes—fast, informated, delegated deciding versus slow, hierarchical, "
     "seniority-ordered deciding {{eisenhardt1989|oipt}}. Digital transformation sharpens "
     "this contrast, because the practices examined here reinforce one another within a "
     "regime: dashboards feed AI models, AI frees managerial attention, participation "
     "channels surface the data-literate young, and agile decisions reward the whole "
     "configuration {{stsd2|agility_dt}}. Within a macro-region whose firms share policy, "
     "infrastructure, and labor-market conditions {{zhejiang1|talent}}, the differentiation "
     "that remains should be organizational. We therefore expect firms to sort into distinct "
     "decision regimes that differ jointly in practices, agility, and the generational "
     "profile of management. This reasoning justifies the following hypothesis:"),

    ('hyp', 'Hypothesis H3.', "Firms form distinct socio-technical decision regimes "
     "(clusters) according to their leadership and decision-making practices, decision "
     "agility, and young managerial presence."),

    ('h1', '3. Materials and Methods'),

    ('h2', '3.1. Research Design and Sample'),

    ('p', "The study employs a quantitative, cross-sectional survey of enterprises, with the "
     "firm as the unit of analysis and senior executives as key informants. Because the data "
     "are cross-sectional, the analysis identifies statistical associations and emergent "
     "patterns; it does not establish causal direction, and reverse causality is explicitly "
     "entertained in the discussion. The design follows the socio-technical premise that "
     "decision practices and organizational outcomes should be studied as configurations "
     "rather than isolated variables {{sts1|stsd1}}."),

    ('p', "Fieldwork was conducted from March to May 2026 in the Yangtze River Delta "
     "(Shanghai, Jiangsu, Zhejiang, and Anhui), a macro-region that combines China's densest "
     "concentration of private enterprise with flagship digital-economy institutions, "
     "making it a natural laboratory for leadership and decision making under digital "
     "transformation {{zhejiang1|ses_regional|digital_emp2}}. Firms were sampled through executive-education "
     "alumni networks of business schools in the region and through enterprise associations, "
     "with quotas by province, sector (digital-core, manufacturing, other services), and "
     "size. The target informant was the chief executive or general manager; where "
     "unavailable, a deputy general manager, strategy executive, or chief information/digital "
     "officer with direct knowledge of decision processes completed the questionnaire."),

    ('p', f"Of 460 questionnaires distributed, 316 were returned (68.7%). After excluding 31 "
     "questionnaires with excessive missingness, failed attention checks, or unqualified "
     "respondents, 285 valid responses remained (a 62.0% valid response rate). Table 1 "
     "profiles the sample: manufacturing accounts for about half of the firms, CEOs or "
     "general managers personally completed 39.6% of questionnaires, and the four provinces "
     "are represented in proportions close to their enterprise populations. Non-response "
     "bias was examined by comparing the earliest and latest quartiles of returned "
     "questionnaires on all six focal variables {{armstrong1977}}; the largest difference "
     "yields ⟪p⟫ = 0.337, indicating no detectable wave effects."),

    ('tabcap', 1, 'Sample profile (N = 285).'),
    ('table', _T1_ROWS, [3100, 3860, 1340, 1340]),
    ('notes', "Source: authors’ survey. Percentages may not sum to 100 due to rounding."),

    ('h2', '3.2. Measures'),

    ('p', "Multi-item constructs use five-point Likert scales (1 = strongly disagree, 5 = "
     "strongly agree) adapted from established sources; Appendix A reports full item "
     "wording. The Chinese questionnaire followed the translation–back-translation protocol "
     "{{brislin1970}} and was piloted with nine executives. Digital transformation "
     "leadership (DLV, six items) adapts digital-leadership measures of vision, championing, "
     "and enablement {{zeike2019|dl3}}. Decision-process digitalization (DPD, five items) "
     "captures the extent to which decisions rest on real-time data, shared dashboards, and "
     "systematic post-decision review {{ddm1|bda1}}. Young-employee decision involvement "
     "(EDI, four items) measures the institutionalized participation of employees under 35 "
     "in transformation decisions, including reverse mentoring and cross-level councils "
     "{{reverse_mentor|voice_part}}. Organizational decision agility (ODA, five items) "
     "adapts decision-speed and responsiveness measures {{eisenhardt1989|baum2003|"
     "teece_agility}}. AI-assisted decision-making breadth (ADM) is a formative count of "
     "the managerial decision domains—out of ten listed, from demand forecasting to "
     "strategic scenario analysis—in which AI or advanced analytics tools are used "
     "{{shrestha2019|csaszar_ai}}."),

    ('p', "Young managerial presence (YMP) is a workforce statistic reported by the "
     "informant: the percentage of managerial positions (first-line supervisor and above) "
     "held by employees aged 35 or younger at the end of 2025. Contextual variables are "
     "firm size (ln employees, lnSIZE), firm age (AGE), R&D intensity (RDI, % of revenue), "
     "and a digital-core industry indicator (DIG)."),

    ('p', f"Reliability is satisfactory: Cronbach's α is {_a['DLV']:.3f} (DLV), "
     f"{_a['DPD']:.3f} (DPD), {_a['EDI']:.3f} (EDI), and {_a['ODA']:.3f} (ODA) "
     "{{cronbach1951}}, with McDonald's ω between "
     f"{min(_o.values()):.3f} and {max(_o.values()):.3f} {{{{hayes2020}}}}; all item "
     "loadings exceed 0.63 (Appendix A). ADM, being formative, is not assessed for internal "
     "consistency. Because one informant reports both practices and the agility outcome, "
     "common method bias deserves attention {{podsakoff2003|podsakoff2024}}: the "
     "questionnaire separated practice and outcome blocks, guaranteed anonymity, and used a "
     "factual statistic (YMP) for the second outcome. Harman's single-factor test across "
     f"the 20 Likert items yields a first unrotated factor of "
     f"{S['harman_first_factor_pct']:.1f}% of variance, well below the 40% threshold; this "
     "test is coarse, but the differentiated correlation pattern reported below is itself "
     "difficult to reconcile with a single method factor {{podsakoff2024}}. Table 2 "
     "summarizes the variables."),

    ('tabcap', 2, 'Variables and measures.'),
    ('table', [
        ['Variable', 'Construct/measure', 'Operationalization', 'Reliability', 'Source'],
        ['DLV', 'Digital transformation leadership',
         '6 Likert items: vision, championing, enablement of digital change',
         f"α = {_a['DLV']:.3f}; ω = {_o['DLV']:.3f}", '{{zeike2019|dl3}}'],
        ['ADM', 'AI-assisted decision-making breadth',
         'Count of managerial decision domains using AI/advanced analytics (0–10), formative',
         'n/a (index)', '{{shrestha2019|csaszar_ai}}'],
        ['DPD', 'Decision-process digitalization',
         '5 Likert items: real-time data, shared dashboards, data-based review of decisions',
         f"α = {_a['DPD']:.3f}; ω = {_o['DPD']:.3f}", '{{ddm1|bda1}}'],
        ['EDI', 'Young-employee decision involvement',
         '4 Likert items: participation of under-35 employees in transformation decisions',
         f"α = {_a['EDI']:.3f}; ω = {_o['EDI']:.3f}", '{{reverse_mentor|voice_part}}'],
        ['ODA', 'Organizational decision agility',
         '5 Likert items: speed, responsiveness, and quality of decisions under uncertainty',
         f"α = {_a['ODA']:.3f}; ω = {_o['ODA']:.3f}", '{{eisenhardt1989|baum2003}}'],
        ['YMP', 'Young managerial presence',
         'Share of managerial positions held by employees aged ≤35 (%), informant-reported statistic',
         'n/a', 'Survey'],
        ['lnSIZE; AGE; RDI; DIG', 'Structural controls',
         'ln employees; firm age (years); R&D intensity (% of revenue); digital-core industry (0/1)',
         'n/a', 'Survey'],
    ], [1400, 2280, 3080, 1280, 1600]),
    ('notes', "Source: authors’ design. Full item wording in Appendix A; α = Cronbach’s alpha "
     "{{cronbach1951}}; ω = McDonald’s omega {{hayes2020}}."),

    ('h2', '3.3. Statistical Methods'),

    ('p', "The analysis proceeds in three stages that examine the same leadership–decision "
     "system at increasing levels of aggregation {{hair|kmeans_biz}}. In the first stage, "
     "each practice is related to the two outcomes through a separate multivariate general "
     "linear model estimated in a MANOVA-type framework, with decision agility and young "
     "managerial presence treated as correlated dependent variables and one practice "
     "indicator as the explanatory variable (1):"),

    ('eq', 'eq1', 1),

    ('p', "where ⟪Y_{1i}⟫ is ODA and ⟪Y_{2i}⟫ is YMP for firm ⟪i⟫, and ⟪X_{ki}⟫ is one of "
     "DLV, ADM, DPD, or EDI. The four indicators are not entered simultaneously: they are "
     "substantially intercorrelated by design of the constructs, and parallel "
     "single-predictor models avoid unstable partial coefficients while the factor analysis "
     "below captures their common structure. Global significance is assessed with Pillai's "
     "Trace and Wilks' Lambda; univariate follow-ups report coefficients, 95% confidence "
     "intervals, and partial eta squared {{hair}}. Diagnostics include Shapiro–Wilk tests of "
     "residual normality and inspection of leverage and Cook's distances. Robustness is "
     "probed twice: each model is re-estimated as a MANCOVA with lnSIZE, AGE, RDI, and DIG "
     "as covariates, and the practices are correlated with the structural variables to "
     "quantify their overlap with firm characteristics."),

    ('p', "In the second stage, the four standardized indicators (2) enter a Principal Axis "
     "Factoring model (3); sampling adequacy is checked with the Kaiser–Meyer–Olkin measure "
     "and Bartlett's sphericity test {{kaiser|bartlett1954}}. A single factor is retained "
     "and its regression-method scores, labelled ⟪FACT_LDC⟫ (leadership–decision "
     "configuration), enter separate regressions for each outcome (4):"),

    ('eq', 'eq2', 2),
    ('eq', 'eq3', 3),
    ('eq', 'eq4', 4),

    ('p', "In the third stage, the six standardized variables (four practices and two "
     "outcomes) are submitted to hierarchical clustering with squared Euclidean distance and "
     "Ward's agglomeration method to gauge the plausible number of groups {{ward|jain}}, "
     "followed by k-means partitioning, which minimizes the within-cluster sum of squared "
     "distances (5):"),

    ('eq', 'eq5', 5),

    ('p', "Candidate solutions with k = 2, 3, and 4 are compared on the average silhouette "
     "coefficient {{rousseeuw}}, and cluster differences are described with analysis of "
     "variance, interpreted descriptively because the clustering and the comparison use the "
     "same variables. All computations were performed in Python 3.11 (NumPy 2.3, "
     "SciPy 1.17)."),
]
