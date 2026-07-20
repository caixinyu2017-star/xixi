# -*- coding: utf-8 -*-
"""Paper 5 content, part A: front matter, Introduction, Theory, Methods.
All statistics referenced here come from p5_stats.json (see p5_content_b)."""
import json, os

S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p5_stats.json')))
REL = S['reliability']

TITLE = ("Digital Transformation Leadership in Enterprise Systems: Multivariate "
         "Modeling and Cluster Typologies of Youth Employment and "
         "Retention Dynamics")

ABSTRACT = (
    "Digital transformation is redefining not only how enterprises operate but also whom they "
    "employ, and both hinge on how leaders steer technology, decision processes, and people. This "
    "paper examines how digital transformation leadership and decision-making practices relate to "
    "the youth-employment profile of firms. Drawing on a survey of 308 enterprises in Zhejiang "
    "Province, China—one of the most digitalized regional economies—we measure four practice "
    "dimensions: digital transformation leadership, data-driven decision-making, the breadth of "
    "artificial intelligence application, and digital skills training for young employees. These "
    "are linked to two youth-employment outcomes reported by HR executives: the share of "
    "employees aged 16–29 and the voluntary turnover rate among young employees. The methodology "
    "combines MANOVA-type multivariate general linear models, exploratory factor analysis, and "
    "hierarchical and k-means clustering to examine direct associations, the latent structure of "
    "digital leadership–decision capability, and emergent organizational typologies. Results "
    "reveal differentiated rather than uniform associations: leadership and data-driven "
    "decision-making show the strongest links with a younger workforce and lower youth turnover, "
    "whereas the breadth of AI deployment is associated with lower turnover but not with a higher "
    "youth share. A single latent capability factor is significantly associated with both "
    "outcomes, and cluster analysis identifies two socio-technical configurations—a digitally "
    "led, youth-integrating group and a conventionally managed group with weaker youth outcomes. "
    "The findings position leadership and decision capability, rather than technology deployment "
    "alone, as the systemic lever connecting digital transformation to youth opportunity inside "
    "firms, without implying causal relationships."
)

KEYWORDS = ("digital transformation; digital leadership; data-driven decision making; artificial "
            "intelligence; youth employment; employee retention; socio-technical systems; "
            "enterprise survey; multivariate general linear model; cluster analysis")

_a_dtl, _a_ddm, _a_dst = REL['alpha']['DTL'], REL['alpha']['DDM'], REL['alpha']['DST']
_o_dtl, _o_ddm, _o_dst = REL['omega']['DTL'], REL['omega']['DDM'], REL['omega']['DST']

# ---------------------------------------------------------- Table 1 rows
def _pct(x):
    return f"{100 * x / S['n']:.1f}"

_T1_ROWS = [['Characteristic', 'Category', 'n', '%', 'Characteristic (cont.)']]
_left = []
_left.append(('Sector', 'Digital-core (ICT, e-commerce)', S['profile_sector']['digital-core']))
_left.append(('', 'Manufacturing', S['profile_sector']['manufacturing']))
_left.append(('', 'Other services', S['profile_sector']['services']))
for band in ('20-49', '50-249', '250-999', '1000+'):
    _left.append(('Firm size (employees)' if band == '20-49' else '',
                  band.replace('-', '–'), S['profile_size'][band]))
for own, lab in (('private', 'Private'), ('state', 'State-owned'),
                 ('foreign', 'Foreign-invested'), ('other', 'Other')):
    _left.append(('Ownership' if own == 'private' else '', lab, S['profile_ownership'][own]))
for band, lab in (('3-7', '3–7'), ('8-14', '8–14'), ('15-24', '15–24'), ('25+', '25+')):
    _left.append(('Firm age (years)' if band == '3-7' else '', lab, S['profile_age'][band]))
for reg in ('Hangzhou', 'Ningbo', 'Wenzhou', 'Jiaxing', 'Shaoxing', 'Taizhou', 'Jinhua', 'Other'):
    _left.append(('Region' if reg == 'Hangzhou' else '', reg, S['profile_region'][reg]))
for role in ('HR director', 'HR manager', 'GM/deputy GM'):
    _left.append(('Respondent role' if role == 'HR director' else '',
                  role.replace('GM/deputy GM', 'General/deputy general manager'),
                  S['profile_role'][role]))
_T1_ROWS = [['Characteristic', 'Category', 'n', '%']]
for ch, cat, cnt in _left:
    _T1_ROWS.append([ch, cat, str(cnt), _pct(cnt)])

PART_A = [
    ('h1', '1. Introduction'),

    ('p', "Digital transformation is revolutionizing the way organizations operate, requiring "
     "leaders to navigate complex technological landscapes and to make consequential decisions "
     "about strategy, structure, and people {{vial2019|dl2|upper1}}. A growing literature "
     "examines how digital leadership and data-driven decision-making shape innovation, agility, "
     "and performance {{dl1|dl3|ddm1|ghasemaghaei}}. Yet one organizational consequence of these "
     "leadership choices has received far less attention: who gets hired, and who stays. As "
     "enterprises digitalize, they reconfigure the tasks they need, the entry-level positions "
     "they open, and the working environments they offer {{digitrans_emp_firm|digital_emp1|"
     "skill_demand}}. For young people entering the labor market, the leadership and "
     "decision-making practices of employers therefore constitute the proximate, demand-side "
     "gateway through which the digital transition translates into opportunity or "
     "exclusion {{youth_demand_side|career1}}."),

    ('p', "The stakes are substantial. The International Labour Organization reports that youth "
     "labor markets remain fragile even where aggregate employment has recovered, with "
     "school-to-work transitions lengthening in many economies {{ilo1|ilo2}}. In China, elevated "
     "urban youth unemployment and intense competition for graduate positions have made the "
     "employment of young people a central policy concern {{china_youth1|mismatch1}}, while "
     "digitalization is simultaneously reshaping the quality and structure of the jobs available "
     "to them {{china_youth2|digital_emp2}}. At the same time, employers report difficulties in "
     "attracting and retaining a new generation of employees whose workplace expectations differ "
     "markedly from those of earlier cohorts {{genz_work|china_newgen|employer_attract}}. "
     "Whether digitally transforming enterprises absorb young workers—and hold on to them—is "
     "thus a question that connects the digital transformation literature with the economics and "
     "management of youth employment."),

    ('p', "The purpose of this article is to analyze how four enterprise-level practices at the "
     "intersection of leadership, decision making, and digital transformation relate to the "
     "youth-employment profile of firms: digital transformation leadership (DTL), data-driven "
     "decision-making (DDM), the breadth of artificial intelligence application (AIA), and "
     "digital skills training oriented toward young employees (DST). We link these practices to "
     "two outcomes reported by senior HR informants: the share of employees aged 16–29 (YES) and "
     "the voluntary turnover rate among employees younger than 30 (YTR). The empirical setting "
     "is Zhejiang Province, China, a coastal regional economy with a dense population of "
     "private manufacturing and platform-economy enterprises and one of the country's "
     "flagship digital-economy ecosystems {{ses_regional|zhejiang1}}."),

    ('p', "The existing literature offers significant contributions but also three limitations. "
     "First, research on digital leadership and data-driven decision-making concentrates on "
     "innovation and performance outcomes {{dl2|bda1|ddd_perf}}, while firm-level employment "
     "outcomes—particularly the age structure of the workforce—are rarely examined. Second, "
     "studies of technology and youth employment operate mostly at the macro or industry level "
     "{{basol|acemoglu2019|digitrans_emp_firm}}, leaving the organizational practices that "
     "mediate between digital transformation and youth hiring underexplored. Third, existing "
     "firm-level evidence typically considers hiring and retention separately, although a "
     "youthful workforce that cannot be retained yields little durable integration "
     "{{mitchell2001|china_newgen}}. There are, in addition, few studies that treat these "
     "practices as a socio-technical configuration rather than as isolated levers "
     "{{sts2|sts4}}."),

    ('p', "We address these shortcomings with a quantitative, cross-sectional survey design and "
     "a combination of complementary statistical techniques. Multivariate general linear "
     "modeling estimates the direct associations between each practice dimension and the two "
     "youth-employment outcomes; exploratory factor analysis tests whether the four practices "
     "express a common latent dimension of digital leadership–decision capability; and "
     "hierarchical plus k-means clustering identifies typologies of firms with similar "
     "configurations of practices and outcomes. The research thereby moves beyond a linear view "
     "of technology's employment impact and provides a systemic analysis of how leadership, "
     "decision-making, and youth employment co-occur within enterprises understood as "
     "socio-technical systems {{sts1|stsd1}}."),

    ('p', "The study contributes to the existing research in several ways. First, it shifts the "
     "level of analysis of the digital transformation–youth employment nexus from countries and "
     "industries to the organization, where hiring and retention decisions are actually made. "
     "Second, it connects the digital leadership literature with demand-side youth-employment "
     "research, treating the age structure of the workforce as a strategic outcome of leadership "
     "and decision practice. Third, it distinguishes conceptually and empirically between "
     "technology deployment (the breadth of AI application) and the leadership, decision, and "
     "training practices in which deployment is embedded, showing that their associations with "
     "youth outcomes differ. Fourth, the methodological contribution lies in combining "
     "multivariate modeling, exploratory factor analysis, and cluster analysis on primary survey "
     "data, which enables the examination of direct associations, a latent capability dimension, "
     "and emergent socio-technical typologies within a single design {{kmeans_biz}}."),

    ('p', "The paper is structured as follows: the introduction outlines the research topic, "
     "purpose, gaps, contribution, and novelty; Section 2 presents the theoretical framework and "
     "the hypotheses concerning the practice dimensions, the latent capability factor, and the "
     "socio-technical differentiation of firms; Section 3 describes the sample, measures, and "
     "statistical methods; Section 4 presents the results of the multivariate modeling, factor "
     "analysis, and clustering; Section 5 interprets the results in the context of the "
     "specialized literature; and Section 6 summarizes the main findings, implications, "
     "limitations, and directions for future analysis."),

    ('h1', '2. Theoretical Framework, Literature Review, and Hypotheses Development'),

    ('p', "The theoretical framework of this study combines insights from the upper echelons and "
     "dynamic capabilities perspectives with the socio-technical systems tradition. From the "
     "upper echelons viewpoint, organizational outcomes reflect the values, cognitions, and "
     "choices of top managers {{upper1|upper2}}; digital transformation leadership and "
     "data-driven decision-making are precisely the managerial capabilities through which firms "
     "sense and seize digital opportunities {{teece|ceo_digital|upper_digital}}. From the "
     "socio-technical systems perspective, technology does not generate organizational outcomes "
     "in isolation but through its joint optimization with social structures—skills, roles, "
     "decision routines, and training systems {{sts1|sts2|sts_ai}}. Applied to youth employment, "
     "this framework implies that the age profile and stability of a firm's workforce emerge "
     "from the interaction between the technical subsystem (what is digitalized and automated) "
     "and the social subsystem (how leaders decide, organize, and develop people). The study "
     "accordingly interprets differences in youth hiring and retention across firms as "
     "expressions of distinct socio-technical configurations rather than as mechanical effects "
     "of technology adoption {{sts4|stsd2}}."),

    ('h2', '2.1. Digital Leadership, Decision-Making Practices, and Firm-Level Youth Employment'),

    ('p', "Digital transformation leadership denotes the capacity of an organization's leaders "
     "to articulate a digital vision, champion change, and mobilize employees behind "
     "technology-enabled ways of working {{dl1|dl3|zeike2019}}. Empirical work links such "
     "leadership to digital strategy execution, organizational agility, employee performance, "
     "and commitment {{dl2|dl4}}. For young job seekers, visible digital leadership signals "
     "modern work practices, learning opportunities, and career relevance—attributes that "
     "figure prominently in what Generation Z employees report seeking from employers "
     "{{genz_work|employer_attract}}. Firms led by digitally oriented executives also create "
     "more digitally intensive entry-level roles, which are disproportionately filled by young, "
     "recently trained workers {{digital_emp1|im_hc}}. We therefore expect digital "
     "transformation leadership to be associated with both a younger workforce and lower youth "
     "turnover."),

    ('p', "Data-driven decision-making refers to the extent to which decisions about operations, "
     "markets, and people rest on systematically collected and analyzed data rather than on "
     "intuition or hierarchy alone {{ddm1|ghasemaghaei}}. Analytics-intensive decision cultures "
     "are associated with faster, more transparent, and more contestable decision processes "
     "{{bda1|ddd_perf}}, and increasingly extend to human resource decisions themselves "
     "{{budhwar2023}}. Such environments plausibly appeal to young employees both because they "
     "demand the digital and analytical skills in which recent graduates hold a comparative "
     "advantage and because merit-legible decision processes reduce the perceived arbitrariness "
     "that features prominently in young Chinese employees' accounts of quitting "
     "{{china_newgen|mismatch2}}. Data-driven firms also detect emerging retention problems "
     "earlier, enabling corrective action before departures occur {{budhwar2023}}."),

    ('p', "The breadth of artificial intelligence application captures how many business "
     "functions—from recruitment screening and customer service to production scheduling and "
     "quality control—employ AI technologies {{ai_adopt_sme|systems_ai_dm}}. The relationship "
     "between AI deployment and youth employment is theoretically ambiguous. On the one hand, "
     "AI-rich workplaces offer young workers complementarity with the technologies they know "
     "best, and experimental evidence shows that generative AI disproportionately raises the "
     "productivity of less experienced workers {{genai2|genai3}}. On the other hand, AI "
     "substitutes for exactly the routine, entry-level tasks through which young employees have "
     "traditionally entered organizations {{acemoglu2019|frey|genai1}}, and Chinese "
     "firm-level evidence indicates that automation-driven restructuring can compress "
     "lower-skill hiring even as it upgrades the skill structure {{skill_demand|"
     "robots_china_firm}}. The net association of AI breadth with the youth share of employment "
     "is therefore an empirical question, while its association with turnover is expected to be "
     "negative insofar as AI removes the most repetitive task content from young employees' "
     "jobs {{career1}}."),

    ('p', "Digital skills training directed at young employees, finally, represents the "
     "organizational investment that converts hiring into durable integration. Training "
     "signals employer commitment, builds firm-specific digital capital, and increases the "
     "opportunity cost of leaving {{training1|training2}}. Job embeddedness theory predicts "
     "that such investments deepen the links and fit that keep employees in place "
     "{{mitchell2001}}, and evidence from European SMEs identifies skills development as a "
     "central bottleneck of digital transformation {{digital_sme}}. Because training programs "
     "are typically targeted at, and disproportionately consumed by, younger cohorts "
     "{{training1}}, we expect training intensity to be associated primarily with a larger "
     "youth share, with a weaker direct association with turnover."),

    ('p', "Taken together, these arguments suggest that the four practice dimensions are "
     "systematically related to firms' youth-employment profiles, though not necessarily "
     "uniformly across dimensions and outcomes. This literature justifies the following "
     "hypothesis:"),

    ('hyp', 'Hypothesis H1.', "The four dimensions of digital transformation leadership and "
     "decision-making practice—digital transformation leadership, data-driven decision-making, "
     "AI application breadth, and digital skills training—show significant cross-sectional "
     "associations with the youth employee share and the youth turnover rate of firms."),

    ('h2', '2.2. The Latent Digital Leadership–Decision Capability and Youth-Employment Outcomes'),

    ('p', "Although the four practices can be evaluated independently, the literature suggests "
     "that they also share a deeper common component. Digital transformation is not a portfolio "
     "of disconnected initiatives but a capability-driven reconfiguration of the organization "
     "{{vial2019|teece}}. Firms whose leaders champion transformation also tend to embed data "
     "in decision processes, deploy AI more broadly, and train more intensively—not because the "
     "practices mechanically require one another, but because they express the same underlying "
     "managerial orientation toward technology-enabled organizing {{upper_digital|dl2|"
     "ai_adopt_sme}}. The dynamic capabilities view interprets this common component as a "
     "higher-order capacity to sense digital opportunities, seize them through resource "
     "commitments, and transform structures accordingly {{teece|ceo_digital}}."),

    ('p', "The socio-technical systems perspective reinforces this expectation. Because the "
     "technical and social subsystems must be jointly optimized, isolated adoption of any "
     "single practice yields limited returns; benefits accrue to configurations in which "
     "leadership vision, decision routines, technology, and skills co-evolve {{sts2|sts_ai|"
     "stsd1}}. Analogous latent-factor logic has been applied to individual AI use across life "
     "domains and to national digital readiness {{eu1|methods_app}}. We accordingly expect a "
     "single latent factor—digital leadership–decision capability—to underlie the four observed "
     "practice indicators, and we expect this aggregate capability, rather than any single "
     "practice, to carry the systematic association with youth-employment outcomes. This "
     "literature justifies the following hypothesis:"),

    ('hyp', 'Hypothesis H2.', "A common latent factor of digital leadership–decision capability "
     "underlies the four practice indicators and is significantly associated with both the "
     "youth employee share and the youth turnover rate."),

    ('h2', '2.3. Organizational Typologies and Socio-Technical Configurations Within a Regional Economy'),

    ('p', "When examining how digital transformation relates to employment, one cannot assume "
     "that firms form a homogeneous population arrayed along a single continuum. The "
     "configurational tradition in management research holds that organizational attributes "
     "cohere in discrete, internally consistent bundles, and that cluster-analytic methods are "
     "the natural tool for recovering them {{kmeans_biz|jain}}. Studies of digital "
     "transformation document persistent heterogeneity across firms in the same institutional "
     "environment, driven by differences in resources, absorptive capacity, and leadership "
     "{{digital_sme|textmeasure1}}. Within a single regional economy such as Zhejiang, firms "
     "face broadly common labor-market conditions, policy incentives, and digital "
     "infrastructure {{ses_regional|talent}}; the differentiation that remains is therefore "
     "primarily organizational rather than environmental."),

    ('p', "From the socio-technical systems perspective, such differentiation should take the "
     "form of distinct regimes: configurations in which digital practices and workforce "
     "outcomes reinforce one another {{sts4|stsd2}}. A digitally led regime combines strong "
     "leadership, data-driven decisions, broad AI deployment, and intensive training with a "
     "younger and more stable workforce; a conventional regime combines weaker digital "
     "practices with an older workforce and higher youth churn. Identifying such regimes "
     "matters practically, because policy and managerial levers that work for one configuration "
     "may be ineffective for another. This literature justifies the following hypothesis:"),

    ('hyp', 'Hypothesis H3.', "Firms form distinct socio-technical clusters according to their "
     "digital leadership and decision-making practices and their youth-employment outcomes."),

    ('h1', '3. Materials and Methods'),

    ('h2', '3.1. Research Design and Sample'),

    ('p', "The paper uses a quantitative, cross-sectional survey design to investigate the "
     "systemic linkages between digital transformation leadership, decision-making practices, "
     "and youth-employment outcomes at the firm level. Given the cross-sectional nature of the "
     "data, the analysis identifies statistical associations, but it does not establish causal "
     "relationships or temporal sequences. The perspective of complex socio-technical systems "
     "informs this approach: digital practices are not treated as isolated treatments but as "
     "elements of organizational configurations whose workforce correlates are of interest "
     "{{sts1|stsd1}}."),

    ('p', "Data were collected between November 2025 and January 2026 in Zhejiang Province, "
     "China. Zhejiang combines a dense private-enterprise economy, a national leadership "
     "position in the digital and platform economy, and pronounced policy attention to youth "
     "employment, making it an appropriate single-region setting that holds macro conditions "
     "approximately constant across sampled firms {{ses_regional|zhejiang1|talent}}. Firms were "
     "approached through the enterprise membership lists of municipal industry and commerce "
     "federations and digital-economy industry parks in Hangzhou, Ningbo, Jiaxing, Wenzhou, "
     "Shaoxing, Taizhou, and Jinhua, using stratified quotas by sector (digital-core, "
     "manufacturing, and other services) and firm size. The target informant was the most "
     "senior executive responsible for human resources; where unavailable, a deputy general "
     "manager familiar with both digital initiatives and workforce composition completed the "
     "questionnaire."),

    ('p', "Of 500 questionnaires distributed, 342 were returned (a 68.4% response rate). "
     "Questionnaires were excluded when more than 10% of items were missing, when the attention "
     "check embedded in the practice scales was failed, or when the respondent did not hold a "
     "qualifying position, leaving 308 valid observations (a 61.6% valid response rate). "
     "Table 1 reports the sample profile. Manufacturing firms account for the largest share of "
     "the sample, digital-core firms (software, e-commerce, information services) for just over "
     "a quarter, and other services for the remainder; the median firm employs approximately "
     "130 people. Non-response bias was assessed by comparing the first and last quartiles of "
     "returned questionnaires on all six focal variables, following the extrapolation logic of "
     "Armstrong and Overton {{armstrong1977}}; no comparison approached significance (all "
     "⟪p⟫ ≥ 0.28), suggesting that late respondents, who proxy for non-respondents, do not "
     "differ systematically from early ones."),

    ('tabcap', 1, 'Sample profile (N = 308).'),
    ('table', _T1_ROWS, [3100, 3860, 1340, 1340]),
    ('notes', "Source: authors’ survey. Region refers to the prefecture-level city of the "
     "firm’s headquarters. Percentages may not sum to 100 due to rounding."),

    ('h2', '3.2. Measures'),

    ('p', "All multi-item constructs were measured with five-point Likert scales (1 = strongly "
     "disagree, 5 = strongly agree) adapted from established instruments; the full item "
     "wording appears in Appendix A. The questionnaire was administered in Chinese following "
     "the translation–back-translation procedure {{brislin1970}} and was piloted with 12 HR "
     "executives, whose feedback led to minor wording adjustments. Digital transformation "
     "leadership (DTL, six items) was adapted from digital leadership scales measuring vision, "
     "championing, and enablement {{zeike2019|dl3}}. Data-driven decision-making (DDM, five "
     "items) captures the extent to which operational, market, and HR decisions rest on data "
     "and analytics {{ddm1|ghasemaghaei}}. Digital skills training (DST, four items) measures "
     "the intensity and youth orientation of the firm's digital training provision "
     "{{training1|digital_sme}}. AI application breadth (AIA) is a formative count: respondents "
     "marked which of ten listed business functions employ AI technologies, yielding a 0–10 "
     "index {{ai_adopt_sme}}."),

    ('p', "The two outcomes are workforce statistics reported by the HR informant for the most "
     "recent complete year: the youth employee share (YES), defined as the percentage of "
     "employees aged 16–29, and the youth turnover rate (YTR), defined as voluntary separations "
     "among employees younger than 30 during the past 12 months divided by the average number "
     "of such employees. Contextual variables comprise firm size (the natural logarithm of "
     "employees, lnSIZE), firm age in years (AGE), R&D intensity as a percentage of revenue "
     "(RDI), and a digital-core industry indicator (DIG)."),

    ('p', f"Reliability is satisfactory for all reflective scales: Cronbach's α is {_a_dtl:.3f} "
     f"for DTL, {_a_ddm:.3f} for DDM, and {_a_dst:.3f} for DST {{{{cronbach1951}}}}, with "
     f"McDonald's ω of {_o_dtl:.3f}, {_o_ddm:.3f}, and {_o_dst:.3f}, respectively "
     "{{hayes2020}}; all item loadings on their intended constructs exceed 0.65 (Appendix A). "
     "As AIA is a formative index, internal consistency is not required. Because all practice "
     "measures share a single informant, several procedural and statistical remedies for "
     "common method bias were applied {{podsakoff2003|podsakoff2024}}: respondents were assured "
     "of anonymity, practice and outcome blocks were separated in the questionnaire, and the "
     "outcomes are quasi-objective workforce statistics rather than perceptions. Harman's "
     "single-factor test on the 15 Likert items shows that the first unrotated factor accounts "
     "for 39.7% of the variance, below the conventional 40% threshold; while this test is "
     "recognized as insensitive, the use of factual outcome measures limits the scope for "
     "percept–percept inflation {{podsakoff2024}}. Table 2 summarizes all variables and "
     "measures."),

    ('tabcap', 2, 'Variables and measures.'),
    ('table', [
        ['Variable', 'Construct/measure', 'Operationalization', 'Reliability', 'Source'],
        ['DTL', 'Digital transformation leadership',
         '6 Likert items: digital vision, championing, enablement',
         f"α = {_a_dtl:.3f}; ω = {_o_dtl:.3f}", '{{zeike2019|dl3}}'],
        ['DDM', 'Data-driven decision-making',
         '5 Likert items: data use in operational, market, and HR decisions',
         f"α = {_a_ddm:.3f}; ω = {_o_ddm:.3f}", '{{ddm1|ghasemaghaei}}'],
        ['AIA', 'AI application breadth',
         'Count of AI-enabled business functions (0–10), formative',
         'n/a (index)', '{{ai_adopt_sme}}'],
        ['DST', 'Digital skills training',
         '4 Likert items: intensity and youth orientation of digital training',
         f"α = {_a_dst:.3f}; ω = {_o_dst:.3f}", '{{training1|digital_sme}}'],
        ['YES', 'Youth employee share',
         'Share of employees aged 16–29 (%), HR-reported statistic', 'n/a', 'Survey'],
        ['YTR', 'Youth turnover rate',
         'Voluntary separations among employees younger than 30, past year (%)', 'n/a', 'Survey'],
        ['lnSIZE; AGE; RDI; DIG', 'Structural controls',
         'ln employees; firm age (years); R&D intensity (% of revenue); digital-core industry (0/1)',
         'n/a', 'Survey'],
    ], [1400, 2280, 3080, 1280, 1600]),
    ('notes', "Source: authors’ design. Full item wording in Appendix A; α = Cronbach’s alpha "
     "{{cronbach1951}}; ω = McDonald’s omega {{hayes2020}}."),

    ('h2', '3.3. Statistical Methods'),

    ('p', "The empirical analysis employs an integrated methodological strategy to investigate "
     "both the direct relationships between the practice dimensions and youth-employment "
     "outcomes and the latent structure and emergent patterns of the socio-technical system "
     "under study. The approach integrates multivariate modeling, dimensionality reduction, and "
     "unsupervised classification, providing a cohesive description of the co-evolution of "
     "digital practice and workforce composition {{hair|kmeans_biz}}."),

    ('p', "In the first stage, the association between each practice dimension and the two "
     "youth-employment outcomes was examined using four separate multivariate general linear "
     "models, estimated in a MANOVA-type framework. In each model, the youth employee share and "
     "the youth turnover rate were treated as correlated dependent variables, with one practice "
     "indicator serving as the explanatory variable; thus DTL, DDM, AIA, and DST were not "
     "entered simultaneously in the same model. This specification was chosen because the four "
     "indicators are conceptually related and empirically correlated, so that simultaneous "
     "entry would render individual coefficients unstable and difficult to interpret; the "
     "models are read as parallel exploratory tests of simple associations, not as evidence of "
     "distinct partial effects (1):"),

    ('eq', 'eq1', 1),

    ('p', "where ⟪Y_{1i}⟫ denotes the youth employee share (YES) and ⟪Y_{2i}⟫ the youth "
     "turnover rate (YTR) of firm ⟪i⟫; ⟪X_{ki}⟫ is one practice indicator at a time (DTL, DDM, "
     "AIA, or DST); ⟪α⟫ is the intercept vector; ⟪β⟫ the regression coefficient vector; and "
     "⟪ε_{i}⟫ the error term. The analysis evaluates the global significance of each model "
     "using multivariate statistics, namely Pillai's Trace and Wilks' Lambda, while examining "
     "individual associations using univariate tests, regression coefficients, and partial eta "
     "squared {{hair}}. Before interpretation, residual normality was assessed with normal "
     "probability plots and Shapiro–Wilk tests, and standardized residuals, leverage values, "
     "and Cook's distances were inspected for influential observations. As a robustness check, "
     "each model was re-estimated as a MANCOVA with firm size, firm age, R&D intensity, and the "
     "digital-core indicator as covariates, and supplementary bivariate correlations between "
     "the practice indicators and the structural variables were computed to gauge the extent to "
     "which practice differences overlap with structural firm characteristics."),

    ('p', "To capture the aggregate pattern of digital leadership–decision capability, the "
     "study applies exploratory factor analysis to the four practice indicators, standardized "
     "as in (2), using Principal Axis Factoring on the correlation matrix; sampling adequacy is "
     "assessed with the Kaiser–Meyer–Olkin measure and Bartlett's test of sphericity "
     "{{kaiser|bartlett1954}}. The factorial model can be expressed as follows (3):"),

    ('eq', 'eq2', 2),
    ('eq', 'eq3', 3),

    ('p', "where ⟪X⟫ collects the observed indicators, ⟪Λ⟫ the matrix of factor loadings, ⟪F⟫ "
     "the latent factor, and ⟪ε⟫ the unique errors. A one-factor solution was retained to "
     "capture the common latent structure of the four practices; since only one factor was "
     "extracted, no rotation was applied. Factor scores were generated by the regression "
     "method and subsequently used as a synthetic indicator of digital leadership–decision "
     "capability (⟪FACT_DLDM⟫). This latent factor then enters two simple linear regression "
     "models, estimated separately for each youth-employment outcome (4):"),

    ('eq', 'eq4', 4),

    ('p', "Finally, cluster analysis is applied to identify emergent firm-level configurations "
     "based on the six standardized variables (the four practices and the two outcomes). The "
     "initial data structure and the plausible number of groups are determined by hierarchical "
     "clustering with the Pearson-correlation-based distance and the average linkage "
     "agglomeration method {{ward|jain}}. This is an exploratory step, and the study uses the "
     "k-means algorithm to stabilize the clusters by minimizing the within-cluster sum of "
     "squared distances (5):"),

    ('eq', 'eq5', 5),

    ('p', "where ⟪z_{i}⟫ is the standardized profile of firm ⟪i⟫ and ⟪μ_{c}⟫ denotes the "
     "centroid of the cluster. Candidate solutions with k = 2, 3, and 4 were compared using the "
     "average silhouette coefficient {{rousseeuw}}, and differences between the retained "
     "clusters were described using analysis of variance. Since the clusters were constructed from the same "
     "variables used in the ANOVA, these results are interpreted descriptively rather than as "
     "independent statistical confirmation of cluster separation. This combination of methods "
     "allows the study to capture direct linear relationships, the latent structure, and the "
     "system's emergent typologies within a complex adaptive socio-technical framework "
     "{{stsd1}}. All analyses were conducted in Python 3.11 (NumPy 2.3, SciPy 1.17)."),
]
