# -*- coding: utf-8 -*-
"""Paper 2 content, part A: front matter, Introduction, Theory, Methods."""

TITLE = ("Enterprise Digital Leadership, Data-Driven Decision Making, and Youth "
         "Labor-Market Outcomes in Europe: Multivariate Modeling and "
         "Socio-Technical Country Typologies")

ABSTRACT = (
    "Digital transformation confronts organizational leaders with consequential decisions about "
    "building digital capabilities—whether to employ dedicated ICT specialists, invest in the "
    "digital training of personnel, adopt artificial intelligence, and embed data analytics in "
    "decision processes. This paper analyzes how the aggregate footprint of such leadership "
    "decisions across enterprises relates to youth labor-market outcomes at the country level. "
    "Using harmonized Eurostat data for the 27 European Union countries, we link four "
    "enterprise-level indicators of digital leadership and data-driven decision making—the shares "
    "of enterprises employing ICT specialists, providing ICT training, using AI technologies, and "
    "performing data analytics—to the youth employment rate and the NEET rate (ages 15–29). The "
    "methodology combines MANOVA-type multivariate general linear models, exploratory factor "
    "analysis, and hierarchical and k-means clustering to examine direct associations, the latent "
    "structure of digital leadership, and emergent country typologies. Results indicate a clear "
    "gradient of associations: the employment of ICT specialists and the provision of ICT training "
    "show the strongest links with higher youth employment and lower NEET rates, while AI use and "
    "data analytics show weaker yet significant associations. A single latent factor of "
    "organizational digital leadership capability explains about three-quarters of the shared "
    "variance and is strongly associated with both youth outcomes. Cluster analysis identifies two "
    "socio-technical regimes—a digitally led, youth-inclusive group and a lagging group with "
    "weaker youth outcomes. The findings highlight leadership capability building, rather than "
    "technology adoption alone, as the systemic lever connecting digital transformation to youth "
    "opportunity, without implying causal relationships."
)

KEYWORDS = ("digital transformation; digital leadership; data-driven decision making; youth "
            "employment; NEET; artificial intelligence; socio-technical systems; exploratory "
            "factor analysis; cluster analysis; European Union")

PART_A = [
    ('h1', '1. Introduction'),

    ('p', "Digital transformation is revolutionizing the way organizations operate, and it does so "
     "through the decisions of their leaders. Whether an enterprise employs dedicated ICT "
     "specialists, invests in the digital training of its personnel, adopts artificial intelligence "
     "(AI), or embeds data analytics in its decision processes reflects deliberate strategic "
     "choices made by executives navigating complex technological landscapes "
     "{{dl1|upper1|ddm1}}. These leadership decisions do not remain inside the firm. Aggregated "
     "across the enterprise population of a country, they shape the structure of labor demand, the "
     "kinds of entry-level jobs available, and the skills that young people must bring to the "
     "labor market {{acemoglu2019|eu1}}. How the collective footprint of enterprise digital "
     "leadership relates to the labor-market prospects of young people is therefore a question of "
     "first-order importance for both management research and employment policy."),

    ('p', "Young people occupy a paradoxical position in the digital transition. On the one hand, "
     "the International Labour Organization reports that youth unemployment and the share of "
     "young people not in employment, education, or training (NEET) remain persistent concerns "
     "even where overall labor markets have tightened {{ilo1|ilo2}}. School-to-work transitions in "
     "Europe remain slow and uneven across countries {{ilo3|stw}}. On the other hand, as digital "
     "natives, young workers hold a comparative advantage in exactly the digitally intensive tasks "
     "that transforming enterprises create, and cross-country evidence suggests that "
     "digitalization is associated with lower youth unemployment {{basol|ogbonna|azu}}. Which of "
     "these forces dominates plausibly depends on the organizational side of the transition: "
     "enterprises whose leaders build digital capabilities—specialist teams, training systems, "
     "AI applications, and data-driven decision routines—create the complementary structures "
     "through which young people can be absorbed into digitally transformed work "
     "{{dl2|training1}}."),

    ('p', "This study addresses this question from a socio-technical systems perspective combined "
     "with an upper-echelons view of organizational decision making. Socio-technical systems "
     "theory conceptualizes technological change as effective only when technical and social "
     "subsystems are jointly optimized {{sts1|sts2|sts3}}. Upper-echelons theory adds that "
     "organizational outcomes reflect the characteristics and choices of top decision makers "
     "{{upper1|upper2|ceo_digital}}: digital capability building is not an automatic response to technological "
     "opportunity but a leadership decision taken under uncertainty {{ddm1|aidm1}}. From this "
     "perspective, the four enterprise indicators analyzed here—employment of ICT specialists, "
     "provision of ICT training, use of AI technologies, and performance of data analytics—are "
     "observable traces of digital leadership and data-driven decision making within national "
     "enterprise populations. Youth employment and NEET rates, in turn, are system-level outcomes "
     "that emerge from the interaction between these organizational choices and national "
     "institutions {{sts4|stsd1}}."),

    ('p', "The present literature offers significant contributions but also limitations. First, "
     "research on digital leadership concentrates on firm-level outcomes—innovation, performance, "
     "and transformation success—and rarely traces its aggregate labor-market consequences "
     "{{dl1|dl3}}. Second, the labor-economics literature on technology and employment usually "
     "measures technology exposure through robots, patents, or occupational task content, paying "
     "less attention to the organizational decision structures—specialists, training, and "
     "data-driven decision making—through which technology is actually deployed "
     "{{acemoglu2019|frey|genai1}}. Third, although European digitalization is known to be highly "
     "uneven, few studies analyze how configurations of enterprise digital capability and youth "
     "labor-market outcomes cluster across countries {{eu1|eu2}}."),

    ('p', "We address these shortcomings with a comparative, quantitative approach grounded in "
     "harmonized Eurostat data for the 27 European Union countries and a combination of "
     "complementary statistical techniques. Multivariate general linear models explore the direct "
     "relationships between the four dimensions of enterprise digital leadership and two youth "
     "labor-market indicators; exploratory factor analysis tests for a common latent factor of "
     "organizational digital leadership capability; and hierarchical and k-means cluster analyses "
     "identify typologies of countries with similar profiles. The research thus moves beyond a "
     "linear view of technology's impact and provides a systemic analysis of the embedding of "
     "digital leadership within organizational, institutional, and labor-market interactions."),

    ('p', "The study contributes to the existing research in several ways. First, it shifts the "
     "focus of the digital-leadership literature from firm performance to youth labor-market "
     "outcomes, connecting management research on leadership and decision making with labor "
     "economics {{dl1|alm1}}. Second, it conceptualizes and measures digital leadership at the "
     "level of national enterprise populations through four complementary, harmonized indicators, "
     "distinguishing capability building (specialists, training) from technology deployment (AI, "
     "data analytics). Third, it identifies a latent dimension of organizational digital "
     "leadership capability and shows that it is strongly associated with youth employment and "
     "NEET rates. Fourth, it derives socio-technical country typologies that reveal how digital "
     "leadership and youth outcomes co-occur in distinct European regimes, informing "
     "differentiated policy responses {{eu2|stsd2}}."),

    ('p', "The paper is structured as follows: the introduction outlines the research topic, "
     "purpose, gaps, contribution, and novelty; Section 2 presents the theoretical framework and "
     "the hypotheses concerning the four dimensions of enterprise digital leadership, the latent "
     "capability factor, and the socio-technical differentiation across countries; Section 3 "
     "describes the data, variables, and statistical methods; Section 4 presents the results of "
     "the multivariate modeling, factor analysis, and clustering; Section 5 interprets the results "
     "in the context of the specialized literature; and Section 6 summarizes the main findings, "
     "implications, and limitations of the research and directions for future analysis."),

    ('h1', '2. Theoretical Framework, Literature Review, and Hypotheses Development'),

    ('p', "The theoretical framework of this study combines the upper-echelons perspective on "
     "strategic decision making with the socio-technical systems perspective on digital "
     "transformation. From the upper-echelons viewpoint, the digital capabilities observable in an "
     "enterprise population condense sequences of leadership decisions: hiring dedicated digital "
     "specialists, allocating budgets to ICT training, approving AI adoption, and institutionalizing "
     "data-driven decision routines {{upper1|upper2|ddm1}}. From the socio-technical viewpoint, "
     "these decisions succeed or fail depending on how the technical subsystem is aligned with "
     "skills, work organization, and institutional context {{sts1|sts4}}. The study therefore "
     "interprets cross-country differences in enterprise digital leadership and youth labor-market "
     "indicators as socio-technical configurations shaped by both organizational decision making "
     "and institutional environments."),

    ('h2', '2.1. Enterprise Digital Leadership, Data-Driven Decision Making, and Youth Labor-Market Outcomes'),

    ('p', "Digital leadership refers to the capacity of organizational leaders to initiate, "
     "resource, and govern digital transformation {{dl1|dl2}}. Recent reviews emphasize that "
     "effective digital leadership combines a transformational vision with concrete capability "
     "investments: recruiting digital talent, developing the digital skills of the existing "
     "workforce, and redesigning decision processes around data {{dl3|dl4|ddm2}}. The employment of "
     "ICT specialists and the provision of ICT training are the most direct observable traces of "
     "such investments in enterprise surveys, while the adoption of AI technologies and the use of "
     "data analytics capture the extent to which decision making itself has been transformed "
     "{{ddm1|aidm1|systems_ai_dm}}."),

    ('p', "Each of these leadership choices carries a distinct implication for young workers. "
     "First, enterprises that employ ICT specialists create professional digital roles for which "
     "recent graduates—the primary carriers of up-to-date digital skills—are natural candidates "
     "{{eu1|basol}}. Second, enterprises that train their personnel signal a "
     "human-capital-augmenting rather than labor-displacing transformation strategy; training "
     "systems lower the effective cost of hiring inexperienced young workers and ease their "
     "integration {{training1|training2}}. Third, AI adoption reallocates tasks from routine "
     "execution toward supervision, analysis, and human–machine collaboration, task categories in "
     "which young digital natives hold a comparative advantage, although displacement risks for "
     "entry-level routine positions cut in the opposite direction {{acemoglu2019|genai1|genai2}}. "
     "Fourth, data analytics embodies data-driven decision making, which is associated with "
     "higher productivity and growth—and expanding, data-driven organizations recruit "
     "disproportionately from the external labor market where young job seekers are concentrated "
     "{{ddm1|bda1}}."),

    ('p', "The macro-level counterpart of these micro-level mechanisms is a cross-country "
     "association between the prevalence of digitally capable enterprises and youth labor-market "
     "performance. Cross-country studies find that digitalization is associated with lower youth "
     "unemployment in Europe and beyond {{basol|ogbonna|azu}}, and that innovation can create "
     "employment through firm growth {{ses_urban}}. At the same time, associations may differ "
     "across the four dimensions: capability-building indicators (specialists, training) are "
     "direct employment channels, whereas deployment indicators (AI, data analytics) affect youth "
     "employment more indirectly through task reallocation and productivity {{acemoglu2022|eu2}}. "
     "This literature justifies the following hypothesis:"),

    ('hyp', 'H1.', "The four enterprise-level dimensions of digital leadership and data-driven "
     "decision making show significant cross-sectional associations with the youth employment "
     "rate and the NEET rate across European Union countries."),

    ('h2', '2.2. The Latent Dimension of Organizational Digital Leadership Capability'),

    ('p', "The four dimensions of enterprise digital leadership can be evaluated independently, "
     "but the literature suggests that they also share a deeper common component. Digital "
     "leadership is theorized as a coherent managerial capability in which vision, talent, "
     "skills development, and data-driven decision routines reinforce one another "
     "{{dl1|dl3|ddm2}}. Enterprises that employ ICT specialists are more likely to train their "
     "personnel, to experiment with AI, and to analyze data; at the country level, these choices "
     "co-vary with digital infrastructure, managerial quality, and institutional support "
     "{{eu1|eu3}}. From a socio-technical systems perspective, such co-variation reflects the "
     "systemic character of digital transformation: isolated technology adoption without "
     "complementary skills and decision structures rarely persists {{sts2|sts4|sts_ai}}."),

    ('p', "If the four indicators share a common latent factor, this factor can be interpreted as "
     "the aggregate organizational digital leadership capability of a country's enterprise "
     "population. Its association with youth labor-market outcomes then provides a synthetic test "
     "of whether digitally led enterprise systems are also youth-inclusive ones. Prior "
     "factor-analytic work on country-level digitalization indicators supports the existence of "
     "such common dimensions {{eu2|methods_app}}. This literature justifies the following "
     "hypothesis:"),

    ('hyp', 'H2.', "The four dimensions of enterprise digital leadership share a common latent "
     "factor, and this latent capability factor is significantly associated with the youth "
     "employment rate and the NEET rate."),

    ('h2', '2.3. Socio-Technical Typologies of Digital Leadership and Youth Employment in Europe'),

    ('p', "European digital transformation is highly uneven. Northern and Western European "
     "countries systematically lead in enterprise digitalization, digital skills, and AI adoption, "
     "while Southern and Eastern European countries lag, reflecting differences in industrial "
     "structure, investment capacity, institutions, and digital infrastructure {{eu1|eu2|eu3}}. "
     "Youth labor markets are similarly heterogeneous, with NEET rates ranging from around four "
     "percent to just above twenty percent across member states {{neet_panel|neet_cee}}. From a complex "
     "adaptive systems perspective, such joint heterogeneity is unlikely to be random: "
     "technology, human capital, organizational decision making, and institutions co-evolve into "
     "persistent national configurations {{stsd1|stsd2|sts4}}."),

    ('p', "The clustering approach therefore connects management research on digital leadership "
     "with labor economics through the identification of socio-technical regimes: groups of "
     "countries in which similar levels of enterprise digital capability co-occur with similar "
     "youth labor-market outcomes. Identifying such typologies has direct policy value, because "
     "interventions that work in digitally led, youth-inclusive regimes may be ineffective in "
     "lagging regimes where complementary capabilities are missing {{alm1|alm2|eu2}}. This "
     "literature justifies the following hypothesis:"),

    ('hyp', 'H3.', "European Union countries form distinct socio-technical clusters according to "
     "enterprise digital leadership, data-driven decision making, and youth labor-market "
     "outcomes."),

    ('h1', '3. Materials and Methods'),

    ('h2', '3.1. Research Design'),

    ('p', "The paper uses a quantitative, cross-sectional, and comparative research design to "
     "investigate the systemic linkages between enterprise digital leadership and youth "
     "labor-market outcomes in a European context. Given the cross-sectional nature of the data, "
     "the analysis identifies statistical associations between digital-leadership indicators and "
     "youth labor-market indicators, but it does not establish causal relationships or temporal "
     "sequences. The perspective of complex socio-technical systems informs this approach: the "
     "digital capability profile of an enterprise population is not seen as a separate event but "
     "as an integral part of the interaction among managerial decision making, human agency, "
     "institutional frameworks, and economic performance {{sts4|stsd1}}."),

    ('p', "The design examines cross-sectional associations between specific dimensions of "
     "enterprise digital leadership and youth labor-market indicators, as well as broader "
     "relational patterns emerging from their interaction. The research combines multivariate "
     "modeling, dimensionality reduction, and segmentation approaches to describe the relational "
     "dynamics and latent structure of the phenomenon under study. The resulting analysis provides "
     "an integrated description of how digital leadership is statistically linked to youth "
     "labor-market characteristics at the system level, without implying causal direction."),

    ('p', "The sample consists of the 27 European Union countries, corresponding to the "
     "availability of harmonized country-level data for the variables included in the analysis. "
     "This sample size is at the lower end of the range for multivariate modeling and exploratory "
     "factor analysis, and the results should therefore be interpreted with caution. The objective "
     "of the empirical strategy is not to provide definitive causal estimates, but to identify "
     "exploratory cross-sectional associations and broad socio-technical patterns across EU "
     "countries. The limited number of observations also justifies parsimonious specifications and "
     "a cautious interpretation of the factor-analytic results."),

    ('h2', '3.2. Selected Data'),

    ('p', "The study uses Eurostat, which provides harmonized European-level data that allow for "
     "consistent comparisons between the countries in the sample. Enterprise digital-leadership "
     "data come from the EU survey on ICT usage and e-commerce in enterprises, which covers "
     "enterprises with ten or more persons employed. Four indicators are used: the share of "
     "enterprises that employ ICT specialists (⟪EDL_SPEC⟫), the share that provided training to "
     "develop or upgrade the ICT skills of their personnel (⟪EDL_TRAIN⟫), the share that use at "
     "least one AI technology (⟪EDL_AI⟫), and the share that perform data analytics (⟪EDL_DA⟫) "
     "{{ds_ict}}. The first two indicators capture leadership decisions to build digital human "
     "capital; the latter two capture the deployment of AI and data-driven decision making in "
     "organizational processes."),

    ('p', "The micro image is supplemented by a macro interpretation using youth labor-market "
     "data. The youth employment rate (⟪YER⟫) refers to employed persons aged 15–29 as a "
     "percentage of the same-age population {{ds_yth}}. The NEET rate (⟪NEET⟫) is the share of "
     "persons aged 15–29 neither in employment nor in education and training {{ds_neet}}. Both "
     "indicators are widely used markers of youth labor-market performance and school-to-work "
     "transition quality {{ilo2|ilo3}}. All variables refer to the most recent available reference "
     "year, so that the enterprise and labor-market data are temporally compatible. Table 1 lists "
     "the variables and their roles in the analysis."),

    ('tabcap', 1, 'Variables and measures.'),
    ('table', [
        ['Variable', 'Dataset', 'Measures', 'Source'],
        ['EDL_SPEC', 'Enterprises that employ ICT specialists',
         'Percentage of enterprises (10+ persons employed)', '{{ds_ict}}'],
        ['EDL_TRAIN', 'Enterprises that provided ICT training to their personnel',
         'Percentage of enterprises (10+ persons employed)', '{{ds_ict}}'],
        ['EDL_AI', 'Enterprises using at least one artificial intelligence technology',
         'Percentage of enterprises (10+ persons employed)', '{{ds_ict}}'],
        ['EDL_DA', 'Enterprises performing data analytics',
         'Percentage of enterprises (10+ persons employed)', '{{ds_ict}}'],
        ['YER', 'Youth employment rate (15–29)',
         'Percentage of the population aged 15–29', '{{ds_yth}}'],
        ['NEET', 'Young people neither in employment nor in education and training (15–29)',
         'Percentage of the population aged 15–29', '{{ds_neet}}'],
    ], [1360, 3480, 3160, 1640]),
    ('notes', "Source: authors’ design based on Eurostat datasets {{ds_ict|ds_yth|ds_neet}}."),

    ('h2', '3.3. Methods'),

    ('p', "The empirical analysis employs an integrated methodological strategy to investigate "
     "both the direct relationships between enterprise digital leadership and youth labor-market "
     "indicators and the latent structure and emerging patterns of the socio-technical system "
     "under study. The approach integrates multivariate modeling, dimensionality reduction, and "
     "unsupervised classification techniques, providing a cohesive explanation of the "
     "co-evolutionary processes of organizational decision making and youth employment "
     "{{hair|methods_app}}."),

    ('p', "In the first stage, the association between each dimension of enterprise digital "
     "leadership and the two youth labor-market indicators was examined using four separate "
     "multivariate general linear models, estimated in a MANOVA-type framework. In each model, "
     "the youth employment rate and the NEET rate were treated as correlated dependent variables, "
     "with one digital-leadership indicator serving as the explanatory variable, according to "
     "Equation (1):"),

    ('eq', 'eq1', 1),

    ('p', "where ⟪Y_{1i}⟫ is the youth employment rate (⟪YER⟫) and ⟪Y_{2i}⟫ the NEET rate of "
     "country ⟪i⟫; ⟪X_{ki}⟫ is one digital-leadership indicator at a time (⟪EDL_SPEC⟫, "
     "⟪EDL_TRAIN⟫, ⟪EDL_AI⟫, or ⟪EDL_DA⟫); ⟪α⟫ is the intercept vector; ⟪β⟫ is the vector of "
     "regression coefficients; and ⟪ε_{i}⟫ is the error term. The four indicators were not "
     "entered simultaneously in the same model because they are conceptually related and "
     "empirically correlated, and the limited cross-sectional sample of 27 countries does not "
     "support a stable model with several closely related predictors. Therefore, the models "
     "should be interpreted as parallel exploratory tests of simple associations, not as evidence "
     "of distinct partial effects. The analysis evaluates the global significance of the models "
     "using multivariate statistics, namely Pillai's Trace and Wilks' Lambda, while examining "
     "individual associations using univariate tests and regression coefficients {{hair}}. Before "
     "interpreting the models, residual normality was assessed using normal probability plots and "
     "Shapiro–Wilk tests, while standardized residuals, leverage values, and Cook's distance were "
     "inspected to identify influential observations."),

    ('p', "To capture the aggregate pattern of digital leadership, the study uses exploratory "
     "factor analysis on the four indicators. Prior to extraction, all variables were "
     "standardized according to Equation (2):"),

    ('eq', 'eq2', 2),

    ('p', "where ⟪z_{ij}⟫ is the standardized value of indicator ⟪j⟫ in country ⟪i⟫, and "
     "⟪x̄_{j}⟫ and ⟪s_{j}⟫ are the sample mean and standard deviation of indicator ⟪j⟫. The "
     "factorial model can be expressed as in Equation (3):"),

    ('eq', 'eq3', 3),

    ('p', "where ⟪X⟫ is the vector of observed variables, ⟪Λ⟫ is the matrix of factor loadings, "
     "⟪F⟫ is the latent factor, and ⟪ε⟫ is the vector of unique errors. Principal Axis Factoring "
     "was used as the extraction method, based on the correlation matrix, with sampling adequacy "
     "assessed by the Kaiser–Meyer–Olkin measure and Bartlett's test of sphericity "
     "{{kaiser|hair}}. A one-factor solution was retained to capture the common latent structure "
     "of digital leadership across the capability-building and deployment domains. Since only one "
     "factor was extracted, no rotation was applied. Factor scores were generated using the "
     "regression method and subsequently used as a synthetic indicator of organizational digital "
     "leadership capability (⟪FACT_EDL⟫). This latent factor then enters two simple linear "
     "regression models, estimated separately for each youth labor-market indicator, according to "
     "Equation (4):"),

    ('eq', 'eq4', 4),

    ('p', "where ⟪Y_{i}⟫ alternatively denotes the youth employment rate and the NEET rate, "
     "⟪β_{0}⟫ is the intercept, ⟪β_{1}⟫ is the regression coefficient of the factor score, and "
     "⟪ε_{i}⟫ is the error term. Such models enable the evaluation of the overall association of "
     "digital leadership capability with youth labor-market performance, providing a synthetic "
     "perspective on the correlation between organizational decision making and youth "
     "opportunity."),

    ('p', "Finally, cluster analysis is applied to identify emergent national-level typologies "
     "based on the four digital-leadership indicators and the two youth labor-market indicators. "
     "The initial data structure and the candidate number of groups are determined by "
     "hierarchical clustering with a correlation-based proximity measure and the average linkage "
     "agglomeration method {{ward|hair}}. This is an exploratory step, and the study then uses the "
     "k-means algorithm to stabilize the clusters by minimizing the within-cluster sum of squared "
     "distances between standardized profiles and cluster centres, according to Equation (5):"),

    ('eq', 'eq5', 5),

    ('p', "where ⟪K⟫ is the number of clusters, ⟪C_{k}⟫ denotes the set of countries assigned to "
     "cluster ⟪k⟫, ⟪z_{i}⟫ is the standardized profile of country ⟪i⟫, and ⟪μ_{k}⟫ is the centre "
     "of cluster ⟪k⟫ {{jain}}. Cluster separation is assessed with the average silhouette "
     "coefficient {{rousseeuw}}, and differences between clusters are described using analysis of "
     "variance (ANOVA). Since the clusters were constructed from the same variables used in the "
     "ANOVA, these results are interpreted descriptively rather than as independent statistical "
     "confirmation of cluster separation. This combination of methods allows the study to capture "
     "direct linear relationships, the latent structure, and the system's emergent typologies, "
     "providing an integrated reading of the relationship among enterprise digital leadership, "
     "data-driven decision making, and youth labor-market dynamics within a complex adaptive "
     "socio-technical systems framework {{stsd1|sts4}}."),
]
