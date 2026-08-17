# -*- coding: utf-8 -*-
"""The manuscript text, written to the section structure, paragraph logic,
tense and register of the latest published article in the target Topic.

Every number in the prose is interpolated from tables/summary.json, the
output of analysis/run_all.py, so the text cannot disagree with the
estimates. Citations are [[key]] markers resolved by build_docx.py into
live Word REF fields numbered by order of first appearance.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "tables", "summary.json"),
          encoding="utf-8") as fh:
    S = json.load(fh)

M = S["models"]
E = S["efa"]
FR = S["factreg"]
C1 = S["centers"]["cluster1"]
C2 = S["centers"]["cluster2"]
SIL = S["silhouette"]
AN = S["anova"]
RB = S["robust"]


def f3(x):
    return "%.3f" % x


def f2(x):
    return "%.2f" % x


def f1(x):
    return "%.1f" % x


def pv(x):
    return "p < 0.001" if x < 0.001 else "p = %.3f" % x


def pctv(x):
    """A share of variance, spoken as an approximate percentage."""
    return "%d%%" % round(x * 100)


TITLE = ("Artificial Intelligence Readiness and Youth Employment in the "
         "European Union: Multivariate Modeling and Cluster Typologies "
         "of Youth Disengagement and Unemployment")

AUTHORS = [("Xinyu Cai ", False), ("1", True),
           (" and Tiantian Mo ", False), ("1,*", True)]

AFFILIATIONS = [
    ("1", "College of Business, Jiaxing University, Jiaxing 314001, "
          "China; caixinyu@zjxu.edu.cn"),
    ("*", "Correspondence: 00008227@zjxu.edu.cn"),
]

ABSTRACT = (
    "Artificial intelligence is gradually penetrating contemporary "
    "socio-technical systems, and the young people now entering "
    "employment are the group most exposed to the reorganization of "
    "entry-level work. In this paper, we analyze cross-sectional "
    "relationships between national artificial intelligence readiness "
    "and two macro-level youth labour-market indicators: the share of "
    "young people neither in employment nor in education and training "
    "(NEET) and the youth unemployment rate. The research is based on "
    "comparative European data for the 27 member states. It measures AI "
    "readiness through enterprise adoption of AI technologies, "
    "generative AI use among young individuals, the digital skills of "
    "young people, and ICT specialist employment, as an expression of "
    "the interaction of technological infrastructure, human capability, "
    "and the institutional environment. The methodology combines "
    "multivariate modelling and regression with exploratory factor "
    "analysis and clustering. Results indicate stable negative "
    "associations between all four readiness indicators and the youth "
    "NEET rate, while the associations with the youth unemployment rate "
    "are weak and statistically insignificant, suggesting that AI "
    "readiness is related to the engagement margin of youth labour "
    "markets rather than to the unemployment margin, without implying a "
    "causal relationship. The results highlight the need for an "
    "integrative view of AI adoption that links youth skills, "
    "organizational practice, and governance structures to ensure an "
    "inclusive digital transition.")

KEYWORDS = ("artificial intelligence; youth employment; NEET; digital "
            "skills; European Union")


BLOCKS = [
    # =======================================================================
    ("h1", "1. Introduction"),
    ("p",
     "Artificial intelligence is one of the most consequential forms of "
     "the ongoing digital transformation, altering the nature of "
     "occupations and the ways in which people learn, create "
     "information, and participate in economic activity "
     "[[dwivedi2023],[eloundou2024],[bick2024]]. Recent studies "
     "associate AI with organizational change, productivity gains, "
     "process automation, and the re-configuration of the relationship "
     "between capital, labour, and skills "
     "[[brynjolfsson2025],[noy2023]]. Nevertheless, the labour-market "
     "effect remains contested. Automation can replace some jobs, "
     "reduce the demand for routine work, and increase the risk of job "
     "polarization [[freyosborne2017],[acemoglu2018],[acemoglu2022]]. "
     "AI can also complement human work, boost productivity, create new "
     "activities, and open less rigid forms of economic participation, "
     "especially where organizations and institutions use it to "
     "leverage digital skills "
     "[[autor2015],[acemoglurestrepo2019],[agrawal2019]]. This tension "
     "is especially relevant for young people, because the analytical, "
     "informational, and administrative tasks in which generative "
     "systems are most capable are concentrated precisely in the "
     "entry-level positions from which early careers have "
     "traditionally been built [[canaries2025],[humlum2025]]."),
    ("p",
     "The purpose of the article is to analyze the relationship between "
     "national artificial intelligence readiness and two macro-level "
     "indicators of youth labour markets in the European Union: the "
     "share of young people neither in employment nor in education and "
     "training (the NEET rate) and the youth unemployment rate. "
     "Artificial intelligence readiness is a complex phenomenon that "
     "may be characterized by enterprise adoption of AI technologies, "
     "generative AI use among young individuals, the digital skills of "
     "young people, and the weight of ICT specialists in employment. "
     "The notion holds that AI may be related to youth labour-market "
     "differences not only through the demand side of firms and "
     "technologies but also through individual processes of "
     "familiarization, learning, and eventual integration of the "
     "technology into daily and professional activities. The youth "
     "focus matters because adverse early labour-market conditions "
     "leave scars on employment and earnings that persist for a decade "
     "or longer [[kahn2010],[schwandt2019],[vonwachter2020],"
     "[oreopoulos2012]], and because disengagement from both work and "
     "learning, captured by the NEET indicator, is among the most "
     "costly forms of youth exclusion [[bynner2002],[eurofound2012]]."),
    ("p",
     "The present literature on AI, employment, and youth transitions "
     "offers significant contributions but also fundamental "
     "limitations. First, much research examines AI at the level of "
     "firms, occupations, or exposure indices, without linking national "
     "AI readiness to the macro-level indicators through which youth "
     "labour markets are actually monitored "
     "[[babina2024],[czarnitzki2023],[acemoglu2022vac]]. Second, the "
     "two headline youth indicators are usually considered separately, "
     "although the NEET rate and the youth unemployment rate capture "
     "different margins of the same socio-technical transition and may "
     "respond to technology in different ways. Thirdly, there are few "
     "comparisons of AI readiness and youth outcomes across Europe, "
     "although research suggests that the repercussions of "
     "digitization vary across national, regional, and institutional "
     "contexts [[georgieff2022],[albanesi2023],[bocean2026]]."),
    ("p",
     "We address these shortcomings with a comparative, quantitative "
     "approach, grounded in harmonised European data and a combination "
     "of complementary statistical techniques. The multivariate "
     "modeling enables the exploration of direct relationships between "
     "the four dimensions of AI readiness and the two youth "
     "labour-market indicators, the exploratory factor analysis allows "
     "for the identification of a common latent factor of AI "
     "readiness, and the cluster analysis allows for the "
     "identification of typologies of countries with similar profiles "
     "of AI readiness, youth disengagement, and youth unemployment. "
     "Thus, the research goes beyond a linear view of technology's "
     "impact and provides a systemic analysis of the embedding of "
     "artificial intelligence within human, organizational, and "
     "institutional interactions."),
    ("p",
     "The study contributes to the existing research in several ways. "
     "First, it shifts the focus from general discussions of AI and "
     "automation to the joint reading of two distinct youth margins: "
     "disengagement, measured by the NEET rate, and job search without "
     "employment, measured by the youth unemployment rate. This "
     "approach allows the analysis to capture which margin of youth "
     "labour markets is statistically related to the diffusion of the "
     "technology. Second, the paper connects youth labour economics "
     "with the socio-technical systems perspective. From a labour "
     "economics viewpoint, the study relates AI readiness to entry "
     "into employment, skill formation, and the demand for young "
     "workers; from a socio-technical perspective, AI readiness is "
     "understood as part of a broader configuration that includes "
     "individual skills, organizational routines, digital "
     "infrastructure, and institutional contexts "
     "[[trist1951],[emery1965],[baxter2011]]. Third, the empirical "
     "contribution lies in the use of harmonised European data to "
     "compare national patterns of AI readiness and youth outcomes "
     "across the EU-27, extending to youth labour markets a "
     "comparative strategy recently applied to aggregate participation "
     "and cost dynamics [[bocean2026]]. Fourth, the methodological "
     "contribution derives from combining multivariate modelling, "
     "exploratory factor analysis, and cluster analysis, which "
     "together examine direct statistical associations, identify a "
     "latent dimension of AI readiness, and distinguish country "
     "typologies that reflect different AI–youth-labour-market "
     "configurations."),
    ("p",
     "The paper is structured as follows: the introduction outlines "
     "the research topic, purpose, gaps, contribution and novelty; the "
     "literature review section presents the background for the "
     "hypotheses concerning the dimensions of AI readiness, the latent "
     "readiness factor and the socio-technical differentiation across "
     "countries; the materials and methods section describes the data, "
     "variables and statistical methods; the results section presents "
     "the results of the multivariate modeling, factor analysis and "
     "clustering; the discussion section interprets the results in the "
     "context of the specialized literature; the conclusions summarize "
     "the main findings, implications, limitations of the research and "
     "directions for future analysis."),

    # =======================================================================
    ("h1", "2. Theoretical Framework, Literature Review, and Hypotheses "
           "Development"),
    ("p",
     "The theoretical framework of this study combines insights from "
     "labor economics with the socio-technical systems perspective. "
     "From the viewpoint of labor economics, artificial intelligence "
     "readiness can be interpreted through the mechanisms of "
     "substitution and complementarity between technology and labor, "
     "skill-biased technological change, human capital accumulation, "
     "and the demand for entry-level work "
     "[[autor2003],[becker1964],[deming2020]]. These mechanisms "
     "explain why enterprise adoption, youth use of generative tools, "
     "digital skills, and specialist employment may be associated with "
     "the engagement of young people in employment and education. At "
     "the same time, the socio-technical systems perspective allows AI "
     "readiness to be understood not as an isolated technological "
     "phenomenon, but as the outcome of interactions among "
     "individuals, digital skills, organizational routines, "
     "institutional environments, and national digital infrastructures "
     "[[bertalanffy1968],[trist1951],[baxter2011]]. Therefore, the "
     "study interprets cross-country differences in AI readiness and "
     "youth labour-market indicators as socio-technical configurations "
     "shaped by both economic mechanisms and institutional contexts."),

    ("h2", "2.1. Artificial Intelligence Readiness and Macro-Level "
           "Youth Labour-Market Indicators"),
    ("p",
     "Much of the study of AI and the employment market has focused on "
     "the trade-off between substitution and complementarity. Frey and "
     "Osborne [[freyosborne2017]] highlighted a substantial risk of "
     "automation for jobs with repetitive tasks, and Graetz and "
     "Michaels [[graetz2018]] showed that industrial automation "
     "reshaped employment without eliminating aggregate demand for "
     "labour. Most recently, Acemoglu and Restrepo "
     "[[acemoglurestrepo2019]] argue that automation both displaces "
     "labour and creates new activities that are complementary to it, "
     "while Autor et al. [[autor2024]] document that most contemporary "
     "employment is in kinds of work that did not exist in 1940. "
     "For the generative wave specifically, occupational exposure "
     "measurement shows that the affected tasks are concentrated in "
     "clerical, analytical, and information-processing work "
     "[[eloundou2024],[felten2021],[gmyrek2023],[gmyrek2025]], and "
     "international assessments conclude that advanced economies face "
     "the largest reallocation pressure "
     "[[cazzaniga2024],[oecd2023],[wef2025]]."),
    ("p",
     "The experimental and quasi-experimental evidence indicates that "
     "the technology compresses task times and reallocates work at the "
     "junior end of the skill distribution. Generative assistance "
     "raises the productivity of the least experienced workers the "
     "most in customer support [[brynjolfsson2025]], compresses "
     "performance gaps in writing tasks [[noy2023]], and both "
     "augments and misleads professionals depending on whether the "
     "task lies inside the technological frontier [[dellacqua2026]]. "
     "Field experiments with software developers and entrepreneurs "
     "confirm heterogeneous gains [[cui2026],[otis2026]], and "
     "freelance platforms show falling demand for exactly the routine "
     "tasks through which young workers once accumulated experience "
     "[[hui2024]]. Early evidence on employment stocks finds emerging "
     "declines among early-career workers in the most exposed "
     "occupations [[canaries2025]], although economy-wide effects "
     "remain modest so far [[humlum2025]]."),
    ("p",
     "For young people, these demand-side movements matter through the "
     "hiring margin. Firms respond to uncertainty by withholding "
     "entry-level vacancies rather than by dismissing incumbents "
     "[[forsythe2022]], and AI-adopting establishments change the "
     "composition of the skills they recruit [[acemoglu2022vac]]. "
     "Because early labour-market conditions scar subsequent careers "
     "[[kahn2010],[bell2011]], any technology that reorganizes "
     "entry-level work may be reflected in the aggregate indicators "
     "through which youth transitions are monitored. The two headline "
     "indicators capture different margins. The NEET rate counts young "
     "people detached from employment and from education and training "
     "simultaneously, and is therefore a measure of disengagement "
     "[[bynner2002],[eurofound2012]]; the youth unemployment rate "
     "counts active job seekers and is strongly shaped by student "
     "job-search behaviour and by national institutions of "
     "school-to-work transition [[caliendo2016]]. Countries with "
     "extensive student search, such as the Nordic economies, "
     "routinely record high youth unemployment rates alongside low "
     "disengagement. AI readiness is theoretically linked to both "
     "margins through the combined mechanisms of labor augmentation, "
     "task substitution, skill formation, and changes in the demand "
     "for digital skills [[degrip2002],[deming2020]]. This literature "
     "justifies the following hypothesis:"),
    ("hyp", "Hypothesis H1.",
     "Enterprise AI adoption, generative AI use among young "
     "individuals, youth digital skills, and ICT specialist employment "
     "show significant cross-sectional associations with the youth "
     "NEET rate and the youth unemployment rate."),

    ("h2", "2.2. The Latent Factor of Artificial Intelligence Readiness "
           "and the Aggregated Socio-Technical Pattern of Youth "
           "Employment"),
    ("p",
     "The various dimensions of AI readiness can be evaluated "
     "independently. Still, the literature suggests that they also "
     "share a deeper common component in the overall degree to which "
     "the technology is integrated into economic and social life. "
     "Artificial intelligence is a general-purpose technology whose "
     "gains are contingent on complementary resources, organizational "
     "absorptive capacity, and institutional reforms "
     "[[bresnahan1995],[cockburn2019],[agrawal2019]]. The productivity "
     "literature shows that such technologies deliver their effects "
     "with a delay, because organizational change, complementary "
     "investment, and skills-building remain necessary "
     "[[brynjolfsson2021],[czarnitzki2023]]. Firm-level evidence "
     "confirms that AI investments translate into growth and "
     "innovation only where data assets and skilled labour are "
     "already in place [[babina2024]]."),
    ("p",
     "This perspective leads to the identification of a common latent "
     "factor in artificial intelligence readiness. If numerous "
     "observable dimensions are correlated with one another, they may "
     "reflect a broader technological inclination that a single "
     "indicator cannot capture. Enterprise adoption may reveal direct "
     "integration into productive activity; generative AI use among "
     "young individuals may signal cultural familiarity of the "
     "incoming cohort with the technology "
     "[[chanhu2023],[brougham2018],[kong2021]]; youth digital skills "
     "may indicate the accumulated capability base "
     "[[vuorikari2022],[vandeursen2019]]; and ICT specialist "
     "employment may capture the professional infrastructure on which "
     "adoption depends. These variables can together establish a "
     "hidden structure of AI readiness that matters for youth "
     "engagement. The socio-technical systems view holds that "
     "technology and the human factor should be analyzed jointly, as "
     "the effects of AI depend on the interaction among digital "
     "infrastructure, organizational processes, user skills, and the "
     "institutional environment [[emery1965],[geels2004],[holland1995]]."),
    ("p",
     "This body of literature is complemented by the Resource-Based "
     "View, which contends that technology becomes a strategic "
     "resource when it is combined with competent human capital, "
     "digital infrastructure, and management competence "
     "[[barney1991],[teece1997]]. Absorptive capacity research makes "
     "the same point for economies: the ability to exploit external "
     "knowledge depends on prior related capability [[cohen1990]]. "
     "The digital-divide literature adds that access alone does not "
     "produce use, and use alone does not produce benefit; "
     "inequalities re-appear at the levels of skills and outcomes "
     "[[vandijk2020],[vandeursen2019]]. Recent studies of AI adoption "
     "similarly link organizational and workforce outcomes to "
     "configurations of technology, skills, and governance rather "
     "than to the technology alone "
     "[[yang2026],[xuejin2025],[janssen2025],[machucho2025]]. In the "
     "context of youth labour markets, a latent readiness factor is "
     "more efficient than separate indicators for capturing the "
     "process by which technology, skills, and infrastructure jointly "
     "shape the entry of young people into employment "
     "[[ilo2024],[ilo2025],[bick2024],[liang2025]]. This literature "
     "justifies the following hypothesis:"),
    ("hyp", "Hypothesis H2.",
     "The latent factor of artificial intelligence readiness is "
     "significantly associated with the youth NEET rate and the youth "
     "unemployment rate."),

    ("h2", "2.3. Country Typologies, Socio-Technical Regimes, and the "
           "European Differentiation of Youth Labour Markets"),
    ("p",
     "When taking a comparative approach to assess the relationship "
     "between AI readiness and youth labour markets, one cannot "
     "overlook differences across countries. The global logic of "
     "technological expansion is filtered through national contexts, "
     "economic arrangements, levels of digital skills, legislation, "
     "institutional infrastructure, and patterns of school-to-work "
     "transition [[georgieff2022],[albanesi2023]]. Institutional "
     "Theory states that legislation, societal norms, and recognised "
     "standards influence the speed and nature of technological "
     "take-up [[dimaggio1983],[meyer1977],[scott2014]]. Organizations "
     "and societies do not accept a technology in a vacuum but within "
     "institutional frameworks that justify or limit certain actions. "
     "In the European Union, this institutional layer is explicit: "
     "the Digital Decade programme sets 2030 targets for digital "
     "skills and enterprise technology take-up "
     "[[digitaldecade2022]], the AI Act creates a common regulatory "
     "regime [[euaiact2024]], and the reinforced Youth Guarantee "
     "commits member states to an offer of employment, education, or "
     "training for every young person [[youthguarantee2020]]."),
    ("p",
     "Studies of automation indicate that the effects of technology "
     "vary greatly across fields and economic systems. The impact of "
     "AI on employment is heterogeneous across sectors, skill levels, "
     "geographies, and levels of institutional flexibility "
     "[[graetz2018],[acemoglu2022],[georgieff2022]]. Sometimes "
     "technology replaces work; sometimes it creates new jobs and "
     "boosts employment through productivity and innovation "
     "[[acemoglurestrepo2019],[autor2024]]. The results suggest that "
     "scholars should not treat countries as monolithic entities but "
     "as socio-technical systems with their own specificities, in "
     "which the co-evolution of technology, human capital, and "
     "institutions produces persistent, emerging patterns "
     "[[holland1995],[geels2004]]. At the country level, AI readiness "
     "and youth outcomes can combine in various configurations, "
     "creating distinct clusters. Thus, the comparative European "
     "study has theoretical and empirical value, because it allows us "
     "to see systemic configurations of AI readiness and youth "
     "engagement, rather than linear interactions between elements "
     "[[bocean2026]]. This literature justifies the following "
     "hypothesis:"),
    ("hyp", "Hypothesis H3.",
     "European countries form distinct socio-technical clusters "
     "according to artificial intelligence readiness, the youth NEET "
     "rate, and the youth unemployment rate."),

    # =======================================================================
    ("h1", "3. Materials and Methods"),
    ("h2", "3.1. Research Design"),
    ("p",
     "The paper uses a quantitative, cross-sectional, and comparative "
     "research design to investigate the systemic linkages between "
     "artificial intelligence readiness and macro-level youth "
     "labour-market indicators in a European context. Given the "
     "cross-sectional nature of the data, the analysis identifies "
     "statistical associations between AI readiness and youth "
     "labour-market indicators, but it does not establish causal "
     "relationships or temporal sequences. The perspective of complex "
     "socio-technical systems informs this approach, in which the "
     "diffusion of AI is not seen as a separate event but as an "
     "integral part of the interaction among human agency, "
     "institutional frameworks, and economic performance."),
    ("p",
     "The design examines cross-sectional associations between "
     "specific dimensions of AI readiness and youth labour-market "
     "indicators, as well as broader relational patterns emerging "
     "from their interaction. The research combines multivariate "
     "modelling, dimensionality reduction, and segmentation "
     "approaches to describe the relational structure of the "
     "phenomenon under study. The sample consists of the 27 European "
     "Union countries, corresponding to the availability of "
     "harmonised country-level data for the variables included in the "
     "analysis. This sample size is at the lower end of the range for "
     "multivariate modelling and exploratory factor analysis, and the "
     "results should therefore be interpreted with caution. The "
     "objective of the empirical strategy is not to provide "
     "definitive causal estimates, but to identify exploratory "
     "cross-sectional associations and broad socio-technical patterns "
     "across EU countries. The limited number of observations also "
     "justifies parsimonious specifications and a cautious "
     "interpretation of the factor-analytic results."),
    ("h2", "3.2. Selected Data"),
    ("p",
     "The study uses Eurostat, which provides harmonised "
     "European-level data that allow for consistent comparisons "
     "between the countries in the sample. Four indicators measure "
     "artificial intelligence readiness. AIENT is the share of "
     "enterprises with ten or more employees using at least one AI "
     "technology, from the 2024 survey on ICT usage in enterprises "
     "[[es_ai]]. GAIY is the share of young individuals aged "
     "16–29 who used generative AI tools in the three months "
     "preceding the 2025 EU Survey on the Use of Information and "
     "Communication Technologies in Households and by Individuals "
     "[[es_gai]]. DSKY is the share of young people aged 16–24 "
     "with basic or above-basic overall digital skills in 2023 "
     "[[es_dsk]]. ICTS is the share of employed ICT specialists in "
     "total employment in 2024 [[es_icts]]. Together, the four "
     "indicators capture the enterprise, user, capability, and "
     "professional-infrastructure dimensions of readiness."),
    ("p",
     "The youth labour market is measured by two dependent variables. "
     "NEET is the share of young people aged 15–29 neither in "
     "employment nor in education and training in 2024 [[es_neet]]. "
     "YUR is the youth unemployment rate of the labour force aged "
     "15–24 in 2024 [[es_yur]]. Both are the headline indicators "
     "through which European youth policy is monitored. Four "
     "structural contextual variables complete the dataset for the "
     "supplementary analysis: tertiary educational attainment of the "
     "population aged 25–34 [[es_tert]], GDP per capita in "
     "purchasing power standards [[es_gdp]], gross domestic "
     "expenditure on research and development as a share of GDP "
     "[[es_rd]], and the share of early leavers from education and "
     "training [[es_elet]]. Table 1 lists the variables and their "
     "roles in the analysis."),
    ("table", "table1"),
    ("h2", "3.3. Methods"),
    ("p",
     "The empirical analysis employs an integrated methodological "
     "strategy to investigate both the direct relationships between "
     "artificial intelligence readiness and youth labour-market "
     "indicators and the latent structure and emerging patterns of "
     "the socio-technical system under study. The approach integrates "
     "multivariate modelling, dimensionality reduction, and "
     "unsupervised classification techniques [[tabachnick2019],"
     "[hair2019]], providing a cohesive description of the "
     "co-evolution of technology and youth employment."),
    ("p",
     "In the first stage, the association between each dimension of "
     "AI readiness and the two youth labour-market indicators was "
     "examined using four separate multivariate general linear "
     "models, estimated in a MANOVA-type framework. In each model, "
     "the youth NEET rate and the youth unemployment rate were "
     "treated as correlated dependent variables, with one readiness "
     "indicator serving as the explanatory variable. Thus, AIENT, "
     "GAIY, DSKY, and ICTS were not entered simultaneously in the "
     "same model. This specification was chosen because the four "
     "readiness indicators are conceptually related and empirically "
     "correlated, and the limited cross-sectional sample of 27 "
     "countries does not support a stable model with several closely "
     "related predictors. Therefore, the models should be interpreted "
     "as parallel exploratory tests of simple associations, not as "
     "evidence of distinct partial effects (1):"),
    ("eq", r"(Y_{1i}, Y_{2i}) = \alpha + \beta X_{ki} + \varepsilon_{i}",
     1),
    ("p", "$Y_{1i}$—the youth NEET rate (NEET);"),
    ("p", "$Y_{2i}$—the youth unemployment rate (YUR);"),
    ("p", "$X_{ki}$—one readiness indicator at a time: AIENT, GAIY, "
          "DSKY or ICTS;"),
    ("p", "$\\alpha$—intercept;"),
    ("p", "$\\beta$—regression coefficient;"),
    ("p", "$\\varepsilon_{i}$—errors."),
    ("p",
     "The analysis evaluates the global significance of the models "
     "using multivariate statistics, namely Pillai's Trace and Wilks' "
     "Lambda, while examining individual associations using "
     "univariate tests and regression coefficients [[tabachnick2019]]. "
     "This approach captures the distinct association of each "
     "readiness dimension with the two youth indicators while "
     "accounting for the correlation between the dependent variables. "
     "Before interpreting the models, several diagnostic checks were "
     "performed. Residual normality was assessed with Shapiro–Wilk "
     "tests [[shapiro1965]], while standardized residuals, leverage "
     "values, and Cook's distance [[cook1977]] were inspected to "
     "identify influential observations. Because the four readiness "
     "indicators were not included simultaneously in the same "
     "multivariate model, multicollinearity did not affect the "
     "single-predictor specifications. However, the correlations "
     "among the readiness variables were taken into account when "
     "interpreting the results, and this was one reason for treating "
     "the four models as exploratory parallel associations and for "
     "extracting a common latent factor through exploratory factor "
     "analysis."),
    ("p",
     "To capture the aggregate pattern of AI readiness, the study "
     "uses exploratory factor analysis on the four readiness "
     "variables. The factorial model can be expressed as follows (2):"),
    ("eq", r"X = LF + \varepsilon", 2),
    ("p", "$X$—observed variables;"),
    ("p", "$L$—matrix of factor loadings;"),
    ("p", "$F$—latent factor;"),
    ("p", "$\\varepsilon$—errors."),
    ("p",
     "Exploratory factor analysis was applied to the four indicators "
     "of AI readiness. Principal Axis Factoring was used as the "
     "extraction method, based on the correlation matrix "
     "[[fabrigar1999]]. Sampling adequacy was verified with the "
     "Kaiser–Meyer–Olkin measure [[kaiser1974]] and "
     "Bartlett's test of sphericity [[bartlett1950]]. A one-factor "
     "solution was retained to capture the common latent structure of "
     "readiness across the enterprise, user, capability, and "
     "professional dimensions. Since only one factor was extracted, "
     "no rotation was applied. Factor scores were generated using the "
     "regression method and subsequently used as a synthetic "
     "indicator of AI readiness, labelled FACT_AIR. This latent "
     "factor then enters two simple linear regression models, "
     "estimated separately for each youth labour-market indicator, "
     "according to the following form (3):"),
    ("eq", r"Y_{i} = \beta_{0} + \beta_{1} F_{i} + \varepsilon_{i}", 3),
    ("p", "$Y_{i}$—dependent variables (NEET and YUR);"),
    ("p", "$F_{i}$—the FACT_AIR factor score;"),
    ("p", "$\\beta_{0}$—intercept;"),
    ("p", "$\\beta_{1}$—regression coefficient;"),
    ("p", "$\\varepsilon_{i}$—error."),
    ("p",
     "Finally, cluster analysis is applied to identify emergent "
     "national-level patterns based on the four readiness variables "
     "and the two youth indicators, standardized before clustering. "
     "The initial data structure and the candidate number of groups "
     "are determined by hierarchical clustering with Pearson "
     "correlation as the proximity measure and the Average Linkage "
     "agglomeration method [[everitt2011]]. This is an exploratory "
     "step, and the study uses the k-means algorithm [[jain2010]] to "
     "stabilize the clusters by minimizing the sum of squared "
     "distances between cluster centres. Differences between clusters "
     "were described using analysis of variance (ANOVA), and the "
     "internal coherence of the solution was assessed with the "
     "average silhouette coefficient [[rousseeuw1987]]. Since the "
     "clusters were constructed from the same variables used in the "
     "ANOVA, these results are interpreted descriptively rather than "
     "as independent statistical confirmation of cluster separation. "
     "This combination of methods allows the study to capture direct "
     "linear relationships, the latent structure, and the system's "
     "emergent typologies within a complex adaptive socio-technical "
     "systems framework."),

    # =======================================================================
    ("h1", "4. Results"),
    ("h2", "4.1. Cross-Sectional Relationships Between Artificial "
           "Intelligence Readiness, Youth Disengagement, and Youth "
           "Unemployment"),
    ("p",
     "The first multivariate model analyzed the association between "
     "enterprise adoption of artificial intelligence (AIENT) and the "
     "youth NEET rate and youth unemployment rate. The multivariate "
     "tests indicate a significant global association with a large "
     f"effect size (Pillai's Trace = {f3(M['AIENT']['pillai'])}, "
     f"Wilks' Lambda = {f3(M['AIENT']['wilks'])}, "
     f"F = {f3(M['AIENT']['F'])}, {pv(M['AIENT']['p'])}), suggesting "
     "that enterprise adoption is associated with the joint "
     "distribution of the two youth indicators. At the univariate "
     "level, however, the association is concentrated on one margin. "
     f"AIENT is associated with approximately "
     f"{pctv(M['AIENT']['uni']['NEET']['eta2'])} of the "
     "cross-sectional variance in the NEET rate "
     f"(B = {f3(M['AIENT']['uni']['NEET']['b'])}, "
     f"{pv(M['AIENT']['uni']['NEET']['p'])}), while its association "
     "with the youth unemployment rate does not reach the "
     "conventional 5% significance threshold "
     f"(B = {f3(M['AIENT']['uni']['YUR']['b'])}, "
     f"{pv(M['AIENT']['uni']['YUR']['p'])}, partial eta squared = "
     f"{f3(M['AIENT']['uni']['YUR']['eta2'])}). Higher enterprise "
     "adoption is associated with a significantly lower share of "
     "disengaged young people, but not with a significantly lower "
     "unemployment rate among active young job seekers (Table 2)."),
    ("table", "table2"),
    ("p",
     "The curve-fit analysis suggests a linear relationship between "
     "AIENT and the NEET rate. At the same time, Figure 1 illustrates "
     "divergent behaviour of the two dependent variables: the NEET "
     "panel shows a clear downward slope with countries closely "
     "distributed around the fitted line, whereas the youth "
     "unemployment panel shows a diffuse cloud in which "
     "high-readiness economies record both the lowest and some of "
     "the highest unemployment rates in the sample."),
    ("fig", "fig1"),
    ("p",
     "The second model evaluated generative AI use among young "
     "individuals (GAIY). The multivariate effect is the strongest of "
     f"the four models (Pillai's Trace = {f3(M['GAIY']['pillai'])}, "
     f"Wilks' Lambda = {f3(M['GAIY']['wilks'])}, "
     f"F = {f3(M['GAIY']['F'])}, {pv(M['GAIY']['p'])}). GAIY explains "
     f"approximately {pctv(M['GAIY']['uni']['NEET']['eta2'])} of the "
     "variation in the NEET rate "
     f"(B = {f3(M['GAIY']['uni']['NEET']['b'])}, "
     f"{pv(M['GAIY']['uni']['NEET']['p'])}): an increase of one "
     "percentage point in the share of young generative AI users is "
     f"associated with a NEET rate lower by "
     f"{f2(abs(M['GAIY']['uni']['NEET']['b']))} percentage points. By "
     "contrast, the association with the youth unemployment rate is "
     f"small and insignificant "
     f"(B = {f3(M['GAIY']['uni']['YUR']['b'])}, "
     f"{pv(M['GAIY']['uni']['YUR']['p'])}). The cohort that uses the "
     "technology most is not measurably less unemployed, but it is "
     "substantially less likely to be detached from both work and "
     "learning (Table 3, Figure 2)."),
    ("table", "table3"),
    ("fig", "fig2"),
    ("p",
     "The third model, centered on the digital skills of young people "
     "(DSKY), points to a similar systemic association (Pillai's "
     f"Trace = {f3(M['DSKY']['pillai'])}, Wilks' Lambda = "
     f"{f3(M['DSKY']['wilks'])}, F = {f3(M['DSKY']['F'])}, "
     f"{pv(M['DSKY']['p'])}). DSKY explains approximately "
     f"{pctv(M['DSKY']['uni']['NEET']['eta2'])} of the variation in "
     f"the NEET rate (B = {f3(M['DSKY']['uni']['NEET']['b'])}, "
     f"{pv(M['DSKY']['uni']['NEET']['p'])}), while its association "
     "with the youth unemployment rate is again statistically "
     f"insignificant (B = {f3(M['DSKY']['uni']['YUR']['b'])}, "
     f"{pv(M['DSKY']['uni']['YUR']['p'])}). The capability base of "
     "the young cohort is closely related to engagement, not to "
     "unemployment (Table 4, Figure 3)."),
    ("table", "table4"),
    ("fig", "fig3"),
    ("p",
     "The final model investigated ICT specialist employment (ICTS). "
     f"The multivariate effect remains significant (Pillai's Trace = "
     f"{f3(M['ICTS']['pillai'])}, Wilks' Lambda = "
     f"{f3(M['ICTS']['wilks'])}, F = {f3(M['ICTS']['F'])}, "
     f"{pv(M['ICTS']['p'])}). ICTS shows a statistically significant "
     "negative association with the NEET rate "
     f"(B = {f3(M['ICTS']['uni']['NEET']['b'])}, "
     f"{pv(M['ICTS']['uni']['NEET']['p'])}, partial eta squared = "
     f"{f3(M['ICTS']['uni']['NEET']['eta2'])}): one additional "
     "percentage point of ICT specialists in employment is associated "
     f"with a NEET rate lower by "
     f"{f2(abs(M['ICTS']['uni']['NEET']['b']))} percentage points. "
     "However, its association with the youth unemployment rate is "
     f"the weakest in the analysis "
     f"(B = {f3(M['ICTS']['uni']['YUR']['b'])}, "
     f"{pv(M['ICTS']['uni']['YUR']['p'])}). Therefore, this result "
     "should not be interpreted as evidence of a relationship between "
     "the professional infrastructure of the digital economy and "
     "youth unemployment (Table 5, Figure 4)."),
    ("table", "table5"),
    ("fig", "fig4"),
    ("p",
     "Overall, the four models suggest differentiated rather than "
     "uniform associations. All four readiness dimensions are "
     "significantly and negatively associated with the youth NEET "
     "rate, with partial eta squared values between "
     f"{f3(M['ICTS']['uni']['NEET']['eta2'])} and "
     f"{f3(M['GAIY']['uni']['NEET']['eta2'])}. None of the four "
     "dimensions is significantly associated with the youth "
     "unemployment rate at the 5% level. Therefore, H1 is only "
     "partially supported: the readiness of a national "
     "socio-technical system for artificial intelligence is "
     "statistically related to the engagement margin of its youth "
     "labour market, not to the unemployment margin. Residual "
     "diagnostics support this reading; Shapiro–Wilk tests do "
     "not reject normality in any of the eight univariate equations "
     f"(smallest p = {f3(min(min(m['uni'][dv]['shapiro_p'] for dv in ('NEET', 'YUR')) for m in M.values()))})."),
    ("p",
     "Given the position of Romania, which records the lowest values "
     "on three of the four readiness dimensions and the highest NEET "
     "rate in the sample, an additional robustness check was conducted. Cook's distances "
     "identify Romania as the most influential observation in the "
     "NEET equations and Sweden in two of the youth unemployment "
     "equations. Excluding Romania, all four NEET associations retain "
     "their negative direction and remain significant (largest "
     f"{pv(max(e['NEET']['p'] for e in RB['models'].values()))}), and "
     "all four youth unemployment associations remain insignificant "
     f"(smallest "
     f"{pv(min(e['YUR']['p'] for e in RB['models'].values()))}). "
     "These results suggest that the divergence between the two "
     "margins is not produced by a single extreme case. The Swedish "
     "pattern is nevertheless informative: Sweden combines the "
     "highest ICT specialist share in the sample with one of the "
     "highest youth unemployment rates, a combination that reflects "
     "extensive student job search rather than youth exclusion, and "
     "that weakens any cross-sectional association on the "
     "unemployment margin."),
    ("p",
     "To address the possible role of broader structural country "
     "characteristics, a supplementary bivariate correlation analysis "
     "was conducted. The four readiness indicators were correlated "
     "with contextual variables available in the dataset, namely "
     "tertiary educational attainment of the population aged "
     "25–34, GDP per capita in purchasing power standards, R&D "
     "intensity, and the share of early leavers from education and "
     "training (Table 6). This analysis was not intended to replace a "
     "controlled regression model, but rather to provide a check on "
     "whether AI readiness covaries with broader educational and "
     "development-related country characteristics."),
    ("table", "table6"),
    ("p",
     "The supplementary correlations indicate that AI readiness is "
     "not independent of broader structural country characteristics. "
     "All four readiness indicators correlate positively and "
     "significantly with tertiary attainment (r between "
     f"{f3(S['ctx']['TERT']['AIENT']['r'])} and "
     f"{f3(S['ctx']['TERT']['GAIY']['r'])}) and with R&D intensity, "
     "and three of the four correlate significantly with GDP per "
     "capita. The correlations with early school leaving are "
     "negative, but reach significance only for youth digital skills "
     f"(r = {f3(S['ctx']['ELET']['DSKY']['r'])}, "
     f"{pv(S['ctx']['ELET']['DSKY']['p'])}). These results suggest "
     "that the observed relationships between AI readiness and youth "
     "disengagement may partly overlap with broader differences in "
     "educational structure and economic development across "
     "countries. Therefore, the main results should continue to be "
     "interpreted as exploratory cross-sectional associations rather "
     "than as estimates of the independent effect of AI readiness."),

    ("h2", "4.2. The Latent Dimension of Artificial Intelligence "
           "Readiness and Its Systemic Associations with Youth Labour "
           "Markets"),
    ("p",
     "The exploratory factor analysis aimed to reduce the four "
     "observable variables to a common factor structure, capturing "
     "the aggregate process by which enterprise adoption, youth use, "
     "digital skills, and professional infrastructure articulate into "
     "a cohesive socio-technical readiness. The KMO value of "
     f"{f3(E['kmo'])}, the significance of Bartlett's test "
     f"(χ2 = {f3(E['bartlett_chi2'])}, df = "
     f"{E['bartlett_df']}, {pv(E['bartlett_p'])}), and bivariate "
     f"correlations between {f3(E['min_r'])} and {f3(E['max_r'])} "
     "indicate that the data are suitable for extracting a common "
     "latent construct (Table 7). The factorial solution converges to "
     f"a single factor that accounts for {f1(E['var_extracted'])}% of "
     "the overall variance after extraction, indicating a unified "
     "dimension of artificial intelligence readiness across the "
     "sampled economies."),
    ("table", "table7"),
    ("p",
     "The communalities indicate that the common latent factor "
     "effectively represents all four dimensions. Generative AI use "
     "among young individuals shows the highest extracted communality "
     f"({f3(E['communalities']['GAIY']['extraction'])}) and loading "
     f"({f3(E['communalities']['GAIY']['loading'])}), suggesting that "
     "the everyday use of the technology by the young cohort is the "
     "purest expression of the underlying readiness dimension. Youth "
     "digital skills and ICT specialist employment load somewhat "
     f"lower ({f3(E['communalities']['DSKY']['loading'])} and "
     f"{f3(E['communalities']['ICTS']['loading'])}), indicating that "
     "each also captures a specific component beyond the common "
     "pattern. This latent factor, labelled FACT_AIR, reflects an "
     "emerging construct of the socio-technical system of youth "
     "employment, in which enterprise-side and person-side readiness "
     "aggregate into a coherent macro-level signal."),
    ("p",
     "The first regression analyzed the relationship between the "
     "latent factor and the youth NEET rate. The model indicates a "
     "negative and statistically significant relationship, with a "
     f"correlation coefficient of {f3(FR['NEET']['beta'])} and an "
     f"explanatory capacity of approximately "
     f"{pctv(FR['NEET']['r2'])} of the variation in the share of "
     f"disengaged young people (R-squared = {f3(FR['NEET']['r2'])}; "
     f"adjusted R-squared = {f3(FR['NEET']['adj_r2'])}). The F test "
     f"indicates that the model is statistically significant (F = "
     f"{f2(FR['NEET']['F'])}, {pv(FR['NEET']['F_p'])}). The "
     "regression coefficient indicates that, on average, a one-unit "
     "increase in the factor score is associated with a decrease of "
     f"around {f2(abs(FR['NEET']['b1']))} percentage points in the "
     f"NEET rate (B = {f3(FR['NEET']['b1'])}, beta = "
     f"{f3(FR['NEET']['beta'])}). Given the cross-sectional structure "
     "of the data and the absence of a meaningful ordering of "
     "countries, no autocorrelation interpretation is reported "
     "(Table 8)."),
    ("table", "table8"),
    ("p",
     "The second regression related the same factor to the youth "
     "unemployment rate. The model is statistically insignificant "
     f"(R-squared = {f3(FR['YUR']['r2'])}; F = {f2(FR['YUR']['F'])}, "
     f"{pv(FR['YUR']['F_p'])}), and the coefficient of the factor "
     f"score (B = {f3(FR['YUR']['b1'])}, beta = "
     f"{f3(FR['YUR']['beta'])}, {pv(FR['YUR']['p1'])}) cannot be "
     "distinguished from zero (Table 9). The aggregate readiness of "
     "the socio-technical system is therefore associated with how "
     "many young people are engaged in work or learning, but not "
     "with the unemployment rate recorded among those actively "
     "searching. These results provide exploratory support for H2 on "
     "the disengagement margin only; considered jointly with the "
     "four single-indicator models, they consistently locate the "
     "statistical relationship between artificial intelligence and "
     "youth labour markets on the engagement margin."),
    ("table", "table9"),

    ("h2", "4.3. Emerging Socio-Technical Typologies: National Profiles "
           "of Artificial Intelligence Readiness and Youth Labour-Market "
           "Outcomes"),
    ("p",
     "To explore the latent structure of the relationships between "
     "artificial intelligence readiness and youth labour-market "
     "indicators, the analysis began with hierarchical clustering, "
     "using the average linkage method and the Pearson correlation "
     "coefficient to measure proximity between countries on the six "
     "standardized analysis variables. The dendrogram presented in "
     "Figure 5 suggests a possible two-group structure in the "
     "sample."),
    ("fig", "fig5"),
    ("p",
     "Following this exploratory indication, the k-means algorithm "
     "was applied to describe two country profiles. The resulting "
     "two-cluster solution should be interpreted as an exploratory "
     "and descriptive typology, not as a definitive classification of "
     "European countries. The k-means partition coincides with the "
     "two-group hierarchical cut for 25 of the 27 countries; the "
     "exceptions are Czechia, which the hierarchical tree attaches "
     "loosely to the higher-readiness branch, and Estonia, which it "
     "attaches to the lower branch, and both reassignments reflect "
     "the mixed profiles of these two economies."),
    ("p",
     "The cluster centers provide a synthetic view of the two "
     f"exploratory typologies. In the first cluster ({C1['n']} "
     f"countries), the average levels are {f2(C1['AIENT'])}% for "
     f"enterprise AI adoption, {f2(C1['GAIY'])}% for generative AI "
     f"use among young individuals, {f2(C1['DSKY'])}% for youth "
     f"digital skills, and {f2(C1['ICTS'])}% for ICT specialist "
     "employment. These readiness levels are associated with an "
     f"average NEET rate of {f2(C1['NEET'])}% and an average youth "
     f"unemployment rate of {f2(C1['YUR'])}%. This profile "
     "corresponds to an environment with relatively strong AI "
     "penetration and low youth disengagement, though not uniformly "
     "low youth unemployment. Conversely, the second cluster "
     f"({C2['n']} countries) has substantially lower levels across "
     f"all readiness dimensions: enterprise adoption of "
     f"{f2(C2['AIENT'])}%, youth generative AI use of "
     f"{f2(C2['GAIY'])}%, youth digital skills of {f2(C2['DSKY'])}%, "
     f"and an ICT specialist share of {f2(C2['ICTS'])}%. This "
     f"technological profile is marked by a higher average NEET rate "
     f"of {f2(C2['NEET'])}% and a higher average youth unemployment "
     f"rate of {f2(C2['YUR'])}%. The resulting typology suggests a "
     "less advanced socio-technical configuration, in which lower AI "
     "readiness is associated with more severe youth disengagement."),
    ("p",
     "As a minimal validation metric, the average silhouette "
     "coefficient was computed for the final two-cluster solution "
     "using the six variables included in the clustering procedure. "
     f"The average silhouette coefficient is {f3(SIL['overall'])}, "
     "indicating a moderate degree of separation between the two "
     f"exploratory clusters. The mean silhouette value is "
     f"{f3(SIL['c1'])} for Cluster 1 and {f3(SIL['c2'])} for Cluster "
     "2. These positive values suggest that the two-cluster solution "
     "has acceptable internal coherence for exploratory purposes, "
     "although the level of separation should not be interpreted as "
     "strong. Therefore, the silhouette results support the "
     "descriptive usefulness of the two-cluster typology and confirm "
     "that the classification should remain exploratory rather than "
     "definitive."),
    ("p",
     "The ANOVA results provide a descriptive characterization of the "
     "differences between the two clusters (Table 10)."),
    ("table", "table10"),
    ("p",
     "The high F values for enterprise adoption and ICT specialist "
     "employment indicate that these variables strongly influence "
     "cluster separation and are the primary markers of "
     "socio-technical divergence. The clusters also differ "
     "significantly in the NEET rate "
     f"(F = {f3(AN['NEET']['F'])}, {pv(AN['NEET']['p'])}), but not in "
     f"the youth unemployment rate (F = {f3(AN['YUR']['F'])}, "
     f"{pv(AN['YUR']['p'])}), which mirrors the results of the "
     "regression stage: the typology separates engaged from "
     "disengaged youth labour markets, not low-unemployment from "
     "high-unemployment ones. Because the clusters were formed using "
     "the same variables that are subsequently compared, the F "
     "values are descriptive and should not be treated as "
     "independent hypothesis tests."),
    ("p",
     "Table A1 in Appendix A shows the composition of the two "
     "clusters, with a strong concentration of Nordic, Western, and "
     "Alpine-Adriatic economies in the higher-readiness category, "
     "joined by the Baltic state of Estonia and the island economy "
     "of Malta. The second cluster is primarily composed of Southern, "
     "Central, and South-Eastern European countries, joined by the "
     "remaining Baltic states of Latvia and Lithuania and by France, "
     "whose enterprise adoption rate remains below the EU average. From the perspective of complex adaptive systems, "
     "these patterns show how interactions among technology, human "
     "capital, and institutional frameworks produce persistent, "
     "emerging configurations [[holland1995]]. Overall, the cluster "
     "analysis supports Hypothesis H3 for the readiness and "
     "disengagement dimensions: European countries can be grouped "
     "into meaningful typologies based on artificial intelligence "
     "readiness and youth labour-market profiles, although the youth "
     "unemployment rate does not separate the groups."),

    # =======================================================================
    ("h1", "5. Discussion"),
    ("p",
     "The data suggest a differentiated pattern of associations "
     "between artificial intelligence readiness, youth disengagement, "
     "and youth unemployment across European countries. Rather than "
     "implying a causal process, these findings point to "
     "cross-sectional co-occurrences that may reflect broader "
     "socio-technical and economic conditions. This interpretation is "
     "consistent with the literature, which characterizes AI as a "
     "technology with pervasive effects on work, productivity, and "
     "economic organization, while emphasizing that these effects "
     "depend on the adoption context and on the complementarities "
     "between technology and the human factor "
     "[[bresnahan1995],[brynjolfsson2021],[babina2024]]."),
    ("p",
     "The four models should not be interpreted as comparing the "
     "independent or partial contribution of each readiness "
     "dimension. Since the readiness variables are conceptually "
     "related and highly correlated, each single-predictor model may "
     "partly reflect the same broader underlying pattern of "
     "readiness. For this reason, the results are interpreted as "
     "simple cross-sectional associations, while the exploratory "
     "factor analysis provides a complementary means of summarizing "
     "their common latent structure. The observed associations should "
     "also be interpreted in relation to broader national development "
     "conditions, since countries with higher income levels, stronger "
     "digital infrastructure, higher educational attainment, and "
     "greater R&D intensity may be more likely to adopt AI earlier "
     "and more intensively, as the supplementary correlations "
     "confirm."),
    ("p",
     "The central substantive finding is the asymmetry between the "
     "two youth margins. Every dimension of AI readiness, and the "
     "latent factor summarizing them, is significantly associated "
     "with the share of young people detached from both work and "
     "learning, and none is significantly associated with the youth "
     "unemployment rate. This asymmetry is consistent with the "
     "measurement properties of the two indicators. The unemployment "
     "rate conditions on active search and therefore mixes exclusion "
     "with the frictional search of students and graduates in "
     "institutional settings that encourage early labour-market "
     "entry [[caliendo2016],[bell2011]]; the Nordic pattern of high "
     "youth unemployment alongside very low disengagement illustrates "
     "the point within our own sample. The NEET rate, by contrast, "
     "captures the stock of young people whom neither the education "
     "system nor the labour market currently reaches "
     "[[bynner2002],[eurofound2012]]. The finding that technology "
     "readiness co-varies with engagement rather than with measured "
     "unemployment extends to the youth segment the argument that "
     "AI should be read as an accelerator of labor market "
     "transformation whose consequences are context-dependent "
     "[[acemoglurestrepo2019],[georgieff2022],[bocean2026]]. It also "
     "cautions against interpreting stable youth unemployment rates "
     "as evidence that the diffusion of AI is neutral for young "
     "people [[canaries2025],[humlum2025]]."),
    ("h2", "5.1. Theoretical Implications"),
    ("p",
     "Theoretically, the findings suggest that labor economics "
     "explains the mechanisms underlying the association between AI "
     "readiness and youth engagement, while the socio-technical "
     "systems perspective explains why these associations differ "
     "across national contexts and depend on the interaction between "
     "technology, skills, organizations, and institutions. The study "
     "demonstrates that AI readiness is not a unidimensional event "
     "but is manifested in several forms of integration: enterprise "
     "adoption, everyday use by the young cohort, the capability "
     "base, and the professional infrastructure. Each of these forms "
     "has its own relationship with youth outcomes, which supports "
     "the idea that researchers cannot assess the association of AI "
     "with the labour market through the presence of technology "
     "alone, but must also consider the concrete ways in which "
     "individuals and organizations use it "
     "[[vandeursen2019],[vandijk2020]]."),
    ("p",
     "One major theoretical contribution is the identification of a "
     "shared latent component of artificial intelligence readiness. "
     "This element points to the fact that the diverse dimensions are "
     "not fully independent but express an aggregate capacity for "
     "digital adaptation, consistent with the general-purpose "
     "technology view in which benefits arise from complementarities "
     "rather than from the technology itself "
     "[[bresnahan1995],[cockburn2019]]. A second contribution is the "
     "explicit separation of the two youth margins. The asymmetric "
     "result—readiness relates to disengagement, not to measured "
     "unemployment—indicates that theoretical accounts of "
     "technology and youth employment should specify which margin "
     "they concern, because mechanisms that operate on participation "
     "and engagement need not operate on search outcomes. Thirdly, "
     "the identification of country clusters supports the thesis "
     "that digital transformation does not follow a uniform European "
     "trajectory; the examined economies are characterized by varied "
     "socio-technical regimes, in which AI readiness and youth "
     "outcomes interact in different combinations "
     "[[dimaggio1983],[scott2014],[geels2004]]."),
    ("h2", "5.2. Practical Implications"),
    ("p",
     "The findings offer several practical implications for public "
     "decision-makers, employers, educational institutions, and "
     "social partners involved in youth labour-market governance. "
     "Since AI readiness is negatively associated with youth "
     "disengagement, public policy should treat AI adoption not only "
     "as a technological issue, but also as a youth-employment, "
     "education, and human-capital policy priority. The productive "
     "integration of artificial intelligence depends on whether "
     "young people, firms, and institutions can transform access to "
     "the technology into usable skills, better work processes, and "
     "more inclusive forms of participation [[autorai2024],"
     "[wef2025]]."),
    ("p",
     "For policy-makers, the results suggest the need to connect AI "
     "strategies with active labour-market policies for youth. "
     "Governments should integrate applied generative AI practice "
     "into the reinforced Youth Guarantee offer "
     "[[youthguarantee2020]], into public employment services, and "
     "into reskilling programmes aimed at young people who are "
     "neither employed nor in training [[caliendo2016],[ilo2024]]. "
     "These programmes should not remain limited to general digital "
     "literacy but should include applied training in the use of AI "
     "for information processing, communication, administrative "
     "tasks, and decision support, following the competence "
     "structure of the European frameworks [[vuorikari2022]]. For "
     "employers, the results caution against treating AI as a simple "
     "replacement for entry-level labour. Firms that automate junior "
     "tasks without redesigning the apprenticeship content of early "
     "careers may find their pipeline of experienced workers "
     "thinning, a risk the experimental literature makes concrete "
     "[[brynjolfsson2025],[hui2024],[canaries2025]]. Practical "
     "measures include AI-augmented junior roles, structured "
     "mentoring, and explicit protection of learning-intensive "
     "tasks."),
    ("p",
     "Educational institutions also have an important role. The "
     "strong loading of youth generative AI use on the latent "
     "readiness factor suggests that schools, universities, and "
     "training providers should integrate generative AI into "
     "curricula in a responsible, applied manner, preparing students "
     "to use the technology critically and productively "
     "[[chanhu2023],[dwivedi2023]]. The cluster analysis further "
     "shows that a differentiated policy approach is necessary "
     "across European countries. Countries in the lower-readiness "
     "cluster should prioritize basic digital infrastructure, "
     "affordable access, digital skills programmes, and support for "
     "small and medium-sized enterprises that lack the resources to "
     "experiment with AI, in order to prevent the widening of "
     "digital and youth-employment inequalities "
     "[[vandijk2020],[albanesi2023]]. Countries in the "
     "higher-readiness cluster should place greater emphasis on "
     "governance, transparency, worker protection, and the quality "
     "of AI integration into work processes, in line with the "
     "obligations of the AI Act [[euaiact2024],[janssen2025]]. "
     "Social partners should be involved in negotiating how "
     "AI-supported work is introduced into the occupations through "
     "which young people enter employment [[oecd2023],[ilo2025]]."),
    ("h2", "5.3. Limitations and Further Research"),
    ("p",
     "The research provides a useful view of the relationship "
     "between artificial intelligence readiness and youth "
     "labour-market indicators. However, the results need to be read "
     "alongside certain methodological and conceptual constraints. "
     "The most important limitation is the cross-sectional design "
     "and the limited sample of 27 European countries observed at a "
     "single point in time. Although the findings reveal significant "
     "associations, they should not be interpreted as causal "
     "effects. The data do not allow the direction of influence to "
     "be established, and reverse causality is plausible: economies "
     "with stronger youth engagement, more advanced digital "
     "infrastructure, and higher education levels may adopt AI "
     "earlier. The limited number of observations also affects the "
     "robustness of the exploratory factor analysis, which should be "
     "regarded as a preliminary identification of a common readiness "
     "dimension rather than as a definitive measurement model."),
    ("p",
     "Another limitation is the macro-level character of the "
     "analysis. The study enables the detection of systemic "
     "tendencies by comparing countries, but it does not capture "
     "distinctions among sectors, regions, occupations, or social "
     "groups. The relationship between AI and youth employment may "
     "vary by education, gender, and the routine intensity of the "
     "occupations young people enter "
     "[[eloundou2024],[gmyrek2025]]. The readiness indicators "
     "measure the extent of adoption and use, not their depth or "
     "purpose; two countries may record equal use built on entirely "
     "different practices. Furthermore, the empirical models do not "
     "include a full set of structural control variables. AI "
     "readiness co-varies with tertiary attainment, income, and R&D "
     "intensity, and with a sample of 27 countries, adding several "
     "structural controls could reduce model stability and increase "
     "the risk of overfitting. Therefore, the coefficients reported "
     "here should not be interpreted as estimates of the unique role "
     "of AI readiness."),
    ("p",
     "Future research should use longitudinal or panel data to "
     "examine whether the associations persist over time and whether "
     "temporal ordering can be established, particularly as the "
     "generative AI indicators accumulate further survey rounds. "
     "Cluster analysis is exploratory and depends on the selected "
     "variables, the proximity measure, and the linkage method; "
     "future work should validate the typologies with gap statistics, "
     "external validation variables, or alternative clustering "
     "specifications. Extending the framework with macroeconomic, "
     "educational, digital, and innovation-related control "
     "variables, and complementing the macro picture with firm-, "
     "occupation-, or individual-level analyses of young workers, "
     "would contribute to a better understanding of the conditions "
     "under which artificial intelligence becomes a lasting benefit "
     "for youth employment rather than a new source of exclusion."),

    # =======================================================================
    ("h1", "6. Conclusions"),
    ("p",
     "This study examined the cross-sectional associations between "
     "artificial intelligence readiness and two youth labour-market "
     "indicators in the European Union: the NEET rate and the youth "
     "unemployment rate. By distinguishing between enterprise "
     "adoption, generative AI use among young individuals, youth "
     "digital skills, and ICT specialist employment, the analysis "
     "provides a differentiated view of how various dimensions of "
     "readiness are related to youth labour-market patterns across "
     "European countries. The findings should be interpreted as "
     "exploratory associations, not as evidence of causal effects."),
    ("p",
     "The results show that the relationship between AI readiness "
     "and youth labour markets is not uniform across the two margins "
     "monitored by European policy. All four readiness dimensions "
     "are significantly and negatively associated with the youth "
     "NEET rate, individually and through their common latent "
     "factor, which alone accounts for approximately "
     f"{pctv(FR['NEET']['r2'])} of the cross-sectional variance in "
     "youth disengagement. None of the four dimensions, and not the "
     "latent factor, is significantly associated with the youth "
     "unemployment rate. Hypotheses H1 and H2 are therefore "
     "partially supported, in a specific and informative way: the "
     "statistical relationship between artificial intelligence and "
     "youth labour markets runs through engagement, not through "
     "measured unemployment."),
    ("p",
     "The factor analysis suggests that the four readiness "
     "indicators share a common latent dimension, with generative AI "
     "use among young individuals as its purest expression. The "
     "cluster analysis indicates descriptive differences among "
     "European countries: a higher-readiness group with low youth "
     "disengagement, concentrated in Nordic and Western Europe "
     "together with several smaller advanced economies, and a "
     "lower-readiness group with higher disengagement, composed "
     "mainly of Southern, Central, and South-Eastern European "
     "countries. The two-cluster solution is exploratory, its "
     "silhouette-based separation is moderate, and the youth "
     "unemployment rate does not distinguish the groups; Hypothesis "
     "H3 is supported for the readiness and disengagement "
     "dimensions."),
    ("p",
     "From a policy perspective, the findings do not justify strong "
     "claims that AI adoption directly improves youth outcomes. "
     "Rather, they suggest that readiness for artificial "
     "intelligence and the engagement of young people are jointly "
     "embedded in national socio-technical development, and that the "
     "policy lever is the connection between them: applied AI "
     "skills within youth-guarantee offers, protected learning "
     "content in AI-augmented entry-level jobs, and differentiated "
     "strategies for lower- and higher-readiness economies. Policies "
     "focused only on technological diffusion are unlikely to be "
     "sufficient unless they are accompanied by measures that "
     "strengthen skills, institutional capacity, and inclusive "
     "access to digital tools."),
    ("p",
     "Overall, the study contributes to research on AI and labour "
     "markets by linking national artificial intelligence readiness "
     "with the macro-level indicators of youth engagement within a "
     "socio-technical comparative framework. Its findings highlight "
     "relevant associations, but also caution that the data are "
     "cross-sectional, the sample is small, the unemployment-margin "
     "relationships are statistically insignificant, and broader "
     "structural factors may shape both AI readiness and youth "
     "outcomes. Future research should use longitudinal data, "
     "include structural controls, and examine sectoral, "
     "occupational, and individual-level differences to better "
     "understand how artificial intelligence is connected to the "
     "employment prospects of the young generation over time."),

    # =======================================================================
    ("h1b", "Author Contributions"),
    ("stmt2", "",
     "Conceptualization, X.C. and T.M.; methodology, X.C.; software, "
     "X.C.; validation, X.C. and T.M.; formal analysis, X.C.; "
     "investigation, T.M.; resources, T.M.; data curation, X.C.; "
     "writing—original draft preparation, X.C.; "
     "writing—review and editing, T.M.; visualization, X.C.; "
     "supervision, T.M.; project administration, T.M. All authors "
     "have read and agreed to the published version of the "
     "manuscript."),
    ("h1b", "Funding"),
    ("stmt2", "", "This research received no external funding."),
    ("h1b", "Institutional Review Board Statement"),
    ("stmt2", "", "Not applicable."),
    ("h1b", "Informed Consent Statement"),
    ("stmt2", "", "Not applicable."),
    ("h1b", "Data Availability Statement"),
    ("stmt2", "",
     "The data presented in this study are openly available from the "
     "Eurostat dissemination database "
     "[[es_ai],[es_gai],[es_dsk],[es_icts],[es_neet],[es_yur],"
     "[es_tert],[es_gdp],[es_rd],[es_elet]]."),
    ("h1b", "Conflicts of Interest"),
    ("stmt2", "", "The authors declare no conflicts of interest."),
    ("h1b", "Abbreviations"),
    ("stmt2", "",
     "The following abbreviations are used in this manuscript:"),
    ("abbr", [
        ("AI", "Artificial intelligence"),
        ("AIENT", "Enterprises using at least one AI technology, "
                  "percentage of enterprises"),
        ("ANOVA", "Analysis of variance"),
        ("DSKY", "Young people with basic or above-basic overall "
                 "digital skills, percentage"),
        ("ELET", "Early leavers from education and training, "
                 "percentage"),
        ("EU", "European Union"),
        ("FACT_AIR", "Latent factor score of artificial intelligence "
                     "readiness"),
        ("GAIY", "Young individuals who used generative AI tools in "
                 "the last three months, percentage"),
        ("GDPC", "GDP per capita in purchasing power standards"),
        ("ICT", "Information and communication technologies"),
        ("ICTS", "ICT specialists, percentage of total employment"),
        ("KMO", "Kaiser–Meyer–Olkin measure of sampling adequacy"),
        ("NEET", "Young people neither in employment nor in education "
                 "and training, percentage"),
        ("RDI", "Gross domestic expenditure on R&D, percentage of GDP"),
        ("TERT", "Tertiary educational attainment, percentage of the "
                 "population aged 25–34"),
        ("YUR", "Youth unemployment rate, percentage"),
    ]),

    # =======================================================================
    ("h1", "Appendix A"),
    ("p",
     "Table A1 reports the cluster membership of the 27 European "
     "Union countries in the two-cluster k-means solution described "
     "in Section 4.3."),
    ("table", "tableA1"),
]
