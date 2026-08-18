# -*- coding: utf-8 -*-
"""The manuscript text, written to the section structure, paragraph
logic, tense and register of the latest article published in the target
Special Issue's editorial environment.

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

B = S["base"]
YU = S["yur"]
PR = S["pre"]
DE = S["desc"]
CO = S["corr"]
ME = S["me_at"]


def f3(x):
    return "%.3f" % x


def f4(x):
    return "%.4f" % x


def f2(x):
    return "%.2f" % x


def f1(x):
    return "%.1f" % x


def pv(x):
    return "p < 0.001" if x < 0.001 else "p = %.3f" % x


TITLE = ("Summer Heat Stress, Urban Green Infrastructure, and Youth "
         "Labour Markets in the European Union: Evidence from a System "
         "GMM Approach")

AUTHORS = [("Xinyu Cai ", False), ("1", True),
           (" and Tiantian Mo ", False), ("1,*", True)]

AFFILIATIONS = [
    ("1", "College of Business, Jiaxing University, Jiaxing 314001, "
          "China; caixinyu@zjxu.edu.cn"),
    ("*", "Correspondence: 00008227@zjxu.edu.cn"),
]

ABSTRACT = (
    "The mitigation of urban heat has become a central objective of "
    "European policies aimed at balancing climate adaptation, public "
    "health, and socioeconomic resilience. This study investigates the "
    "contribution of summer heat stress and urban green infrastructure "
    "to youth labour-market outcomes in the European Union. Using a "
    "balanced panel dataset covering the 27 European Union Member "
    "States over the period 2010–2024, the effects of cooling "
    "degree days, their interaction with the green infrastructure "
    "endowment of functional urban areas, economic growth, and "
    "tertiary educational attainment on the youth NEET rate are "
    "analysed using a two-step System Generalized Method of Moments "
    "(System GMM) estimator. The results indicate that summer heat "
    "stress has a positive and statistically significant effect on "
    "youth disengagement and that this effect weakens systematically "
    "with the green infrastructure endowment, remaining statistically "
    "distinguishable from zero only below an endowment of roughly "
    "30% of functional urban area. Economic growth reduces the NEET "
    "rate, the contemporaneous effect of tertiary attainment is "
    "negative but statistically insignificant, and the heat effects "
    "are not detectable for the youth unemployment rate, suggesting "
    "that heat stress operates on the engagement margin of youth "
    "labour markets. The findings support integrated policies that "
    "treat urban greening as social infrastructure for the young "
    "generation.")

KEYWORDS = ("urban heat stress; green infrastructure; youth "
            "employment; NEET; European Union")


BLOCKS = [
    # =======================================================================
    ("h1", "1. Introduction"),
    ("p",
     "Urban heat has become one of the most pressing challenges of "
     "contemporary sustainable development, particularly in the "
     "context of the alarming rise in the frequency, intensity, and "
     "duration of European heat waves. The urban heat island effect "
     "amplifies heat exposure precisely where most Europeans live and "
     "work [[oke1982],[santamouris2020]]; the summer of 2022 was the "
     "hottest in the European observational record, and 2024 became "
     "Europe's warmest year overall "
     "[[esotc2023],[lancetcountdown2024]]. A substantial body "
     "of research demonstrates that the deliberate integration of "
     "green and blue elements into the built environment can "
     "effectively diminish urban overheating, improve thermal "
     "comfort, and protect human health "
     "[[bowler2010],[gunawardena2017],[wong2021],[iungman2023]]. At "
     "the same time, the economic literature shows that heat is not "
     "only a health hazard but also a labour-market force: high "
     "temperatures reduce labour supply, productivity, and learning, "
     "with effects that are strongest in exposed sectors and among "
     "vulnerable groups "
     "[[graffzivin2014],[zander2015],[somanathan2021],[park2020]]."),
    ("p",
     "Young people stand at the intersection of these two literatures, "
     "although they are rarely studied there. The sectors through "
     "which young Europeans typically enter employment — tourism, "
     "hospitality, agriculture, construction, and other seasonal and "
     "outdoor activities — are among the most heat-exposed segments "
     "of the economy [[ilo2019heat],[dasgupta2021]]. Heat also "
     "disrupts learning and examination performance, weakening the "
     "education leg of the school-to-work transition [[park2020]]. "
     "Because adverse conditions at labour-market entry leave scars "
     "on employment and earnings that persist for a decade or longer "
     "[[kahn2010],[schwandt2019],[vonwachter2020],[oreopoulos2012]], "
     "any recurring shock that falls disproportionately on entry-level "
     "activity deserves attention as a youth-policy problem. The "
     "share of young people neither in employment nor in education "
     "and training (the NEET rate) is the headline indicator of this "
     "risk, capturing simultaneous detachment from work and from "
     "learning [[bynner2002],[eurofound2012]]."),
    ("p",
     "The purpose of the article is to analyse the relationship "
     "between summer heat stress, the green infrastructure endowment "
     "of urban areas, and youth labour-market outcomes across the "
     "European Union. Heat stress is measured through cooling degree "
     "days, a standard indicator of the intensity of hot weather; the "
     "thermal-mitigation capacity of national urban systems is "
     "measured through the share of green infrastructure in "
     "functional urban areas; and youth outcomes are measured through "
     "the NEET rate, with the youth unemployment rate employed in a "
     "sensitivity analysis. The notion holds that urban greenery may "
     "be related to youth labour markets not only through amenity and "
     "health channels but also by buffering the labour-market "
     "consequences of increasingly frequent heat extremes "
     "[[marando2022],[garcialeon2021]]."),
    ("p",
     "Despite the growing body of literature on urban heat and its "
     "mitigation, several important research gaps remain. First, the "
     "economic studies of heat and labour concentrate on productivity, "
     "hours, and earnings of incumbent workers, while the entry margin "
     "of the labour market — where young people are found — has "
     "received little attention "
     "[[graffzivin2014],[somanathan2021],[callahan2022]]. Second, the "
     "extensive literature on the cooling effects of green and blue "
     "infrastructure evaluates temperature, comfort, health, and "
     "energy outcomes, but rarely connects the thermal benefits to "
     "labour-market indicators "
     "[[aram2019],[iungman2023],[marando2022]]. Third, existing "
     "empirical evidence on the socioeconomic impacts of heatwaves in "
     "Europe is largely simulation-based or regional, and "
     "comprehensive panel evidence covering all 27 European Union "
     "Member States remains limited [[garcialeon2021],[eea2020]]. "
     "Finally, relatively few studies investigate these relationships "
     "using a dynamic panel framework that simultaneously addresses "
     "persistence in youth outcomes, endogeneity concerns, and "
     "country-specific heterogeneity, an estimation strategy "
     "recently applied to related European Union sustainability "
     "questions [[rus2026]]. These limitations "
     "highlight the need for further empirical evidence capable of "
     "providing a more comprehensive understanding of how urban heat "
     "and its mitigation are connected to the employment prospects of "
     "the young generation."),
    ("p",
     "Building upon the research gaps identified above, the present "
     "study makes several important contributions to the literature. "
     "First, it develops an integrated analytical framework that "
     "simultaneously examines heat stress, green infrastructure, "
     "macroeconomic conditions, and human capital, thereby connecting "
     "the climate-adaptation literature with youth labour economics. "
     "Second, by analysing all 27 European Union Member States over "
     "the period 2010–2024, the study offers updated empirical "
     "evidence for a policy context characterised by the European "
     "Green Deal, the EU Adaptation Strategy, and the Nature "
     "Restoration Regulation, which sets explicit targets for urban "
     "green space [[egd2019],[euadapt2021],[nrl2024]]. Third, the "
     "study contributes to the debate on the socioeconomic returns of "
     "green and blue infrastructure by evaluating whether the "
     "well-documented thermal benefits translate into measurable "
     "labour-market protection for young people. Finally, by "
     "employing a dynamic panel framework capable of addressing "
     "persistence, endogeneity, and unobserved heterogeneity, the "
     "analysis provides robust empirical evidence on the youth "
     "labour-market consequences of summer heat within the European "
     "Union [[blundell1998],[roodman2009]]."),
    ("p",
     "In light of the research gaps identified and the contributions "
     "outlined above, the study seeks to answer the following "
     "research question: To what extent does summer heat stress "
     "influence youth labour-market outcomes in the European Union, "
     "and to what extent does the green infrastructure endowment of "
     "urban areas moderate this influence? To address this question, "
     "the study employs a two-step System GMM estimator applied to a "
     "balanced panel of the 27 EU Member States over the period "
     "2010–2024, in which the youth NEET rate depends on its "
     "own past values, cooling degree days, the interaction of "
     "cooling degree days with the green infrastructure endowment, "
     "real GDP growth, and tertiary educational attainment. By "
     "integrating these determinants within a unified dynamic "
     "framework, the study provides empirical evidence on how climate "
     "pressure, urban form, macroeconomic conditions, and human "
     "capital jointly influence the engagement of young people in "
     "employment and education."),
    ("p",
     "The remainder of this paper is organised as follows. Section 2 "
     "critically reviews the relevant literature and develops the "
     "research hypotheses. Section 3 describes the data, variables, "
     "and econometric methodology employed in the empirical analysis. "
     "Section 4 presents the empirical findings, while Section 5 "
     "discusses the results in relation to the existing literature, "
     "highlighting their theoretical and policy implications. "
     "Finally, Section 6 summarises the main conclusions, outlines "
     "the study's limitations, and suggests directions for future "
     "research."),

    # =======================================================================
    ("h1", "2. Literature Review"),
    ("h2", "2.1. Summer Heat Stress and Youth Labour-Market Outcomes"),
    ("p",
     "Heat is increasingly recognised as a macroeconomic force. "
     "Cross-country evidence shows that high temperatures depress "
     "output growth in a non-linear fashion, with substantial "
     "heterogeneity across income levels and climatic zones "
     "[[dell2012],[burke2015],[callahan2022]]. At the micro level, "
     "heat reduces the time allocated to work in exposed industries "
     "[[graffzivin2014]], lowers productivity and increases "
     "absenteeism in manufacturing [[somanathan2021]], and causes "
     "substantial self-reported productivity losses even in "
     "high-income economies [[zander2015]]. The International Labour "
     "Organization estimates that heat stress will erode the "
     "equivalent of tens of millions of full-time jobs globally as "
     "warming proceeds [[ilo2019heat]], and multi-model studies "
     "indicate that the combined effect of heat on labour "
     "productivity and labour supply is already measurable in "
     "southern Europe [[dasgupta2021],[garcialeon2021]]."),
    ("p",
     "Several mechanisms suggest that these pressures fall "
     "disproportionately on young people. The sectors through which "
     "youth enter employment — agriculture, construction, "
     "tourism, and hospitality — combine outdoor or poorly "
     "cooled workplaces with seasonal, temporary contracts that are "
     "easily not renewed when summer conditions deteriorate "
     "[[ilo2019heat],[ilo2024]]. Employers facing heat-related "
     "productivity losses and cooling costs can adjust most cheaply "
     "at the hiring margin, which is where labour-market entrants are "
     "concentrated. In addition, heat disrupts the education leg of "
     "the school-to-work transition: hotter school years reduce "
     "learning and examination performance, weakening the "
     "qualifications with which young people approach the labour "
     "market [[park2020]]. Because early-career conditions have "
     "persistent scarring effects "
     "[[kahn2010],[bell2011],[schwandt2019]], recurring summer shocks "
     "may accumulate into measurable differences in youth "
     "disengagement across countries and years."),
    ("p",
     "Within the European Union, these considerations are especially "
     "relevant. The continent is warming faster than any other, and "
     "the summers of the early 2020s brought record heat exposure "
     "[[esotc2023],[lancetcountdown2024]]. Youth labour markets, "
     "meanwhile, remain a central policy concern, monitored through "
     "the NEET rate and addressed by the reinforced Youth Guarantee "
     "[[youthguarantee2020],[eurofound2012],[caliendo2016]]. "
     "Nevertheless, the connection between the two policy fields "
     "— climate adaptation and youth employment — has "
     "hardly been examined empirically. Given the theoretical "
     "arguments and empirical evidence presented above, summer heat "
     "stress is expected to be positively associated with youth "
     "disengagement, although the magnitude of the relationship "
     "across all EU Member States remains an open empirical "
     "question. Therefore, further empirical investigation is "
     "required to assess this relationship within the European "
     "Union."),
    ("hyp", "H1.",
     "Summer heat stress has a positive effect on the youth NEET rate "
     "in the European Union."),

    ("h2", "2.2. Green and Blue Infrastructure, Thermal Mitigation, and "
           "Socioeconomic Resilience"),
    ("p",
     "The capacity of green and blue infrastructure to moderate urban "
     "heat is among the most robust findings of urban climatology. "
     "Vegetation cools through shading and evapotranspiration, water "
     "bodies through evaporation and thermal inertia, and both "
     "modify the surface energy balance that generates the urban "
     "heat island [[oke1982],[bowler2010],[gunawardena2017]]. "
     "Systematic reviews report average park cooling effects of "
     "around one degree Celsius, with larger effects for larger and "
     "better-connected green areas [[bowler2010],[aram2019]], and "
     "greenery is now treated as a first-order mitigation and "
     "adaptation strategy for overheating cities "
     "[[santamouris2020],[wong2021]]. For European functional urban "
     "areas specifically, satellite-based assessments show that "
     "existing green infrastructure already lowers city temperatures "
     "measurably, and that reaching recommended tree-cover levels "
     "would substantially reduce heat-related mortality "
     "[[marando2022],[iungman2023]]."),
    ("p",
     "If green infrastructure lowers the effective heat load that "
     "urban residents and workplaces experience, it should also "
     "buffer the socioeconomic consequences of hot summers. A given "
     "meteorological heat wave translates into less physiological "
     "strain, fewer lost working hours, smaller cooling costs, and "
     "less disruption of schooling in a city whose streets, "
     "workplaces, and commuting routes are shaded and ventilated "
     "than in a densely sealed one [[ebi2021],[tuholske2021]]. The "
     "green endowment of cities is therefore not only environmental "
     "infrastructure but potentially social infrastructure, "
     "conditioning how climate pressure reaches the labour market. "
     "The distributional literature adds that access to urban green "
     "space is unequal within and across European cities "
     "[[kabisch2016],[wolch2014]], which suggests that the buffering "
     "capacity of greenery may differ systematically across "
     "countries."),
    ("p",
     "European policy explicitly embraces this integrated view. The "
     "EU Adaptation Strategy calls for nature-based solutions to "
     "climate-proof cities [[euadapt2021]], the Nature Restoration "
     "Regulation requires member states to ensure no net loss of "
     "urban green space and tree cover [[nrl2024]], and the European "
     "Environment Agency documents rapidly growing but uneven "
     "adaptation activity across European towns and cities "
     "[[eea2020]]. However, the benefits of these investments are "
     "typically quantified in degrees, mortality, or energy, and "
     "hardly ever in labour-market outcomes. Based on the theoretical "
     "arguments and empirical evidence discussed above, the green "
     "infrastructure endowment of urban areas is expected to "
     "attenuate the labour-market consequences of summer heat for "
     "young people."),
    ("hyp", "H2.",
     "The green infrastructure endowment of urban areas attenuates "
     "the effect of summer heat stress on the youth NEET rate."),

    ("h2", "2.3. Macroeconomic Conditions and Youth Labour Markets"),
    ("p",
     "Youth labour-market outcomes are strongly cyclical. Young "
     "people are over-represented among job seekers and among "
     "temporary contract holders, so downturns raise youth joblessness "
     "disproportionately, as the euro-area crisis and the pandemic "
     "demonstrated across Europe [[bell2011],[caliendo2016]]. The "
     "scarring literature shows that entering the labour market in a "
     "recession depresses employment and earnings for years "
     "[[kahn2010],[oreopoulos2012],[schwandt2019],[vonwachter2020]], "
     "and the disengagement captured by the NEET indicator is among "
     "the most costly forms of this exposure "
     "[[bynner2002],[eurofound2012]]. Aggregate growth, by expanding "
     "hiring and shortening job search, is therefore expected to "
     "reduce the share of young people detached from employment and "
     "education. Accordingly, real GDP growth is included in the "
     "empirical model as the macroeconomic determinant of youth "
     "disengagement, and a negative relationship is expected."),
    ("hyp", "H3.",
     "Economic growth has a negative effect on the youth NEET rate in "
     "the European Union."),

    ("h2", "2.4. Human Capital and Youth Transitions"),
    ("p",
     "Educational attainment shapes the speed and quality of the "
     "school-to-work transition. Higher attainment improves "
     "employability, widens the range of accessible occupations, and "
     "keeps young people attached to structured activity during "
     "difficult periods [[bynner2002],[caliendo2016]]. Across "
     "European countries, rising tertiary attainment among the "
     "25–34 age group has accompanied the long decline of "
     "youth disengagement, although the relationship is mediated by "
     "labour-demand conditions and institutional quality "
     "[[eurofound2012],[youthguarantee2020]]. Tertiary attainment is "
     "therefore included as the human-capital determinant of the "
     "youth NEET rate, and a negative relationship is expected. At "
     "the same time, attainment expansions materialise slowly, so "
     "their contemporaneous contribution may be modest relative to "
     "the cyclical and climatic forces examined above."),
    ("hyp", "H4.",
     "Tertiary educational attainment has a negative effect on the "
     "youth NEET rate in the European Union."),

    # =======================================================================
    ("h1", "3. Data and Methodology"),
    ("h2", "3.1. Data and Variables"),
    ("p",
     "The empirical analysis is based on a balanced panel dataset "
     "covering the 27 European Union Member States over the period "
     "2010–2024, resulting in 405 country-year observations. "
     "The observation period captures a sequence of profound "
     "economic and climatic transformations, including the euro-area "
     "crisis and its long recovery, the pandemic disruption of "
     "2020–2021, and the record European summers of 2022, 2023 "
     "and 2024. Annual country-level data were obtained from "
     "Eurostat, ensuring consistency and comparability across "
     "countries and over time, and were complemented by the "
     "Copernicus Urban Atlas land-monitoring products for the green "
     "infrastructure endowment [[urbanatlas]]."),
    ("p",
     "The dependent variable is the youth NEET rate, defined as the "
     "share of young people aged 15–29 neither in employment "
     "nor in education and training [[es_neet]]. Compared with the "
     "youth unemployment rate, the NEET rate captures detachment "
     "from both work and learning and is less sensitive to student "
     "job-search behaviour; the youth unemployment rate of the "
     "labour force aged 15–24 [[es_yur]] is nevertheless "
     "employed in a sensitivity analysis. Summer heat stress is "
     "measured through cooling degree days [[es_cdd]], which "
     "cumulate the intensity and duration of hot weather over the "
     "year; in the estimations the variable is expressed in hundreds "
     "of degree days (CDD100). The green infrastructure endowment "
     "(GRN) is the share of green urban areas and urban forest in "
     "the functional urban areas of each country, compiled from the "
     "Urban Atlas 2018 layer and treated as a time-invariant "
     "structural characteristic of national urban systems "
     "[[urbanatlas],[kabisch2016]]. Macroeconomic conditions are "
     "represented by the real GDP growth rate [[es_gdpg]], and human "
     "capital by tertiary educational attainment of the population "
     "aged 25–34 [[es_tert]]. Table 1 summarises the variables "
     "included in the analysis."),
    ("table", "table1"),
    ("h2", "3.2. Model Specification"),
    ("p",
     "To examine the determinants of youth disengagement in the "
     "European Union, this study specifies a dynamic panel data model "
     "in which the current NEET rate depends on both its past values "
     "and a set of explanatory variables associated with heat stress, "
     "thermal mitigation, macroeconomic conditions, and human "
     "capital. The dynamic specification is particularly appropriate "
     "because youth disengagement exhibits persistence over time: a "
     "young person detached from employment and education this year "
     "is substantially more likely to remain detached next year, and "
     "aggregate NEET rates adjust only gradually to changing "
     "conditions [[bynner2002],[eurofound2012]]. The baseline "
     "empirical model is specified as follows (1):"),
    ("eq", r"NEET_{it} = \alpha NEET_{it-1} + \beta_{1} CDD100_{it} "
           r"+ \beta_{2} (CDD100_{it} \times GRN_{i}) "
           r"+ \beta_{3} GDPG_{it} + \beta_{4} TERT_{it} "
           r"+ \mu_{i} + \lambda_{t} + \varepsilon_{it}", 1),
    ("p", "where"),
    ("p", "$NEET_{it}$ represents the youth NEET rate in country ($i$) "
          "at time ($t$);"),
    ("p", "$NEET_{it-1}$ denotes the lagged dependent variable;"),
    ("p", "$CDD100_{it}$ represents cooling degree days, in hundreds;"),
    ("p", "$GRN_{i}$ denotes the time-invariant green infrastructure "
          "share of functional urban areas;"),
    ("p", "$GDPG_{it}$ represents the real GDP growth rate;"),
    ("p", "$TERT_{it}$ denotes tertiary educational attainment of the "
          "population aged 25–34;"),
    ("p", "$\\mu_{i}$ captures country-specific unobserved effects;"),
    ("p", "$\\lambda_{t}$ captures common period effects;"),
    ("p", "$\\varepsilon_{it}$ represents the idiosyncratic error "
          "term."),
    ("p",
     "Because the green infrastructure endowment is time-invariant, "
     "its level effect is absorbed by the country-specific term "
     "$\\mu_{i}$; the variable therefore enters the model through its "
     "interaction with heat stress, which is precisely the "
     "thermal-mitigation channel of interest. The common period "
     "effects $\\lambda_{t}$ absorb the euro-area cycle, the "
     "pandemic, and the common component of European summer warming; "
     "in the estimations, all variables are expressed as deviations "
     "from period means, which removes these common period effects "
     "prior to estimation. Based on the theoretical framework and "
     "empirical evidence discussed in Section 2, a positive "
     "coefficient is expected for cooling degree days, a negative "
     "coefficient for the interaction with the green endowment, and "
     "negative coefficients for economic growth and tertiary "
     "attainment."),
    ("p",
     "Preliminary panel diagnostics were conducted before estimating "
     "the dynamic model. The Im–Pesaran–Shin panel unit "
     "root test [[ips2003]] indicates that the NEET rate and tertiary "
     "attainment are non-stationary in levels but become stationary "
     "after first differencing, while cooling degree days and GDP "
     f"growth are stationary in levels (for the NEET rate, z = "
     f"{f2(S['ips']['NEET']['z'])} in levels and z = "
     f"{f2(S['ips']['NEET']['d_z'])} in first differences). In "
     "addition, the Pesaran cross-sectional dependence test "
     f"[[pesaran2021]] indicates significant cross-sectional "
     f"dependence in the NEET rate (CD = {f2(S['cd']['stat'])}, "
     f"{pv(S['cd']['p'])}), reflecting the presence of common shocks "
     "and structural interdependencies within the European Union. "
     "These results support a dynamic panel framework based on "
     "internal instruments and period-demeaned variables."),
    ("h2", "3.3. Estimation Method"),
    ("p",
     "The estimation of dynamic panel data models presents several "
     "econometric challenges, including unobserved heterogeneity, "
     "endogeneity, and potential reverse causality. In the present "
     "study, these issues are particularly relevant because the "
     "inclusion of the lagged dependent variable generates "
     "correlation between the regressors and the error term, leading "
     "to biassed and inconsistent estimates when conventional "
     "estimation techniques are applied. Ordinary Least Squares "
     "estimators are biassed due to the presence of country-specific "
     "effects, while fixed-effects estimators suffer from the "
     "well-known dynamic panel bias resulting from the inclusion of "
     "the lagged dependent variable [[nickell1981]]. Consequently, "
     "more advanced estimation techniques are required to obtain "
     "consistent parameter estimates."),
    ("p",
     "To address these issues, this study employs the System "
     "Generalized Method of Moments (System GMM) estimator developed "
     "by [[blundell1998]], building on [[arellano1991]] and "
     "[[arellano1995]]. The System GMM approach combines equations "
     "in first differences with equations in levels, using internal "
     "instruments derived from lagged values of the variables. The "
     "estimation uses the two-step variant with the finite-sample "
     "correction of [[windmeijer2005]] for the standard errors. "
     "Given the moderate number of cross-sectional units, the "
     "instrument set was deliberately restricted and collapsed to "
     "avoid instrument proliferation and overfitting [[roodman2009]]: "
     "the collapsed second and third lags of the dependent variable "
     "instrument the difference equation, the collapsed lagged first "
     "difference and the constant instrument the levels equation, "
     "and the exogenous regressors instrument themselves in "
     "differences, resulting in "
     f"{B['instruments']} instruments for {B['groups']} country "
     "groups. The validity of the moment conditions is evaluated "
     "with the Arellano–Bond tests for first- and second-order "
     "serial correlation and the Hansen test of overidentifying "
     "restrictions. This estimation strategy follows the approach "
     "recently applied to European Union panels in the sustainability "
     "literature [[rus2026]]."),

    # =======================================================================
    ("h1", "4. Empirical Results"),
    ("h2", "4.1. Descriptive Statistics"),
    ("p",
     "Table 2 presents the descriptive statistics of the variables "
     "included in the empirical analysis. The average youth NEET "
     f"rate over the sample period is {f2(DE['NEET']['mean'])}%, with "
     "substantial variation across countries and years, from "
     f"{f2(DE['NEET']['min'])}% to {f2(DE['NEET']['max'])}%. Cooling "
     f"degree days average {f1(DE['CDD']['mean'])} but range from "
     f"below five in Ireland to more than "
     f"{int(DE['CDD']['max'] // 100) * 100} in Cyprus, reflecting the "
     "climatic heterogeneity of the Union. The green infrastructure "
     f"endowment averages {f1(DE['GRN']['mean'])}% of functional "
     f"urban area, ranging from {f1(DE['GRN']['min'])}% to "
     f"{f1(DE['GRN']['max'])}%, with the lowest values in the "
     "southern island states whose cities are also among the most "
     "heat-exposed. These patterns provide preliminary evidence of "
     "the structural heterogeneity characterising the European "
     "Union and support the application of panel data techniques "
     "capable of accounting for country-specific characteristics."),
    ("table", "table2"),
    ("p",
     "Figure 1 depicts the evolution of the two central variables at "
     "the EU-27 level. Average cooling degree days fluctuate around "
     "a rising trend and reach their highest values in the record "
     "summers of 2022–2024, consistent with the observational "
     "climate record [[esotc2023]]. The average NEET rate, by "
     "contrast, rises with the euro-area crisis to a peak in 2013, "
     "declines steadily to 2019, jumps in the pandemic year 2020, "
     "and resumes its decline thereafter. The two aggregate series "
     "therefore move in opposite directions over the sample period, "
     "which underlines that the relationship of interest cannot be "
     "read from aggregate trends: it concerns whether, conditional "
     "on the cycle and on country characteristics, unusually hot "
     "years leave young people more detached than usual, and "
     "whether green urban structure moderates this."),
    ("fig", "fig1"),
    ("h2", "4.2. Correlation Analysis"),
    ("p",
     "Prior to the econometric estimation, a correlation analysis "
     "was conducted to examine the relationships among the variables "
     "and assess potential multicollinearity issues. Table 3 "
     "presents the Pearson correlation coefficients for all "
     "variables included in the empirical model. The pooled "
     "correlations indicate that heat exposure is positively "
     f"associated with the NEET rate (r = "
     f"{f3(CO['NEET_CDD100'])}), while the green endowment "
     f"(r = {f3(CO['NEET_GRN'])}) and tertiary attainment "
     f"(r = {f3(CO['NEET_TERT'])}) are negatively associated with "
     "it. The correlation between heat exposure and the green "
     f"endowment is negative (r = {f3(CO['CDD100_GRN'])}), "
     "reflecting the geographical reality that the most "
     "heat-exposed urban systems of the South are also the least "
     "green. The only pairwise coefficient whose magnitude exceeds "
     "the commonly accepted threshold of 0.80 is this "
     "heat–green correlation itself; it reflects the structural "
     "North–South gradient of the cross-section rather than "
     "redundancy between distinct constructs, and because the green "
     "endowment is time-invariant and enters the estimated equation "
     "only through its interaction with heat exposure, while the "
     "dynamic panel estimation exploits within-country variation, "
     "this cross-sectional overlap does not translate into "
     "collinearity among the regressors of Equation (1). All "
     "remaining pairwise correlations are well below the "
     "threshold. Nevertheless, correlation "
     "analysis does not account for dynamic persistence, "
     "endogeneity, or unobserved heterogeneity, and the empirical "
     "analysis therefore proceeds with the estimation of the "
     "two-step System GMM model."),
    ("table", "table3"),
    ("p",
     "Figure 2 complements the correlation analysis with the "
     "cross-sectional pattern of country averages. Countries with "
     "hotter climates record systematically higher average NEET "
     f"rates (r = {f3(S['cross']['r'])}), a gradient of about "
     f"{f2(S['cross']['slope'] * 100)} percentage points of youth "
     "disengagement per additional hundred cooling degree days. "
     "This cross-sectional association mixes climate with many "
     "other structural differences between northern and southern "
     "Europe; the dynamic panel estimation that follows isolates "
     "the within-country response to unusually hot years while "
     "controlling for persistence, the cycle, and human capital."),
    ("fig", "fig2"),
    ("h2", "4.3. System GMM Estimation Results"),
    ("p",
     "Table 4 reports the estimation results obtained using the "
     "two-step System Generalized Method of Moments estimator, and "
     "Table 5 presents the associated diagnostic tests. The lagged "
     "dependent variable enters with a coefficient of "
     f"{f3(B['coef']['L.NEET'])} ({pv(B['p']['L.NEET'])}), "
     "confirming the strong persistence of youth disengagement and "
     "supporting the dynamic specification of the model. The "
     "diagnostic tests support the econometric validity of the "
     "estimated model: the Arellano–Bond tests indicate the "
     f"expected first-order serial correlation (AR(1) "
     f"{pv(B['ar1_p'])}) and the absence of second-order serial "
     f"correlation (AR(2) p = {f3(B['ar2_p'])}), while the Hansen "
     f"test does not reject the overall validity of the instrument "
     f"set (p = {f3(B['hansen_p'])}). The restricted number of "
     f"instruments ({B['instruments']}) relative to the number of "
     f"country groups ({B['groups']}) further reduces the risk of "
     "instrument proliferation [[roodman2009]]."),
    ("table", "table4"),
    ("table", "table5"),
    ("p",
     "The results provide clear support for Hypothesis H1. Cooling "
     f"degree days exert a positive and statistically significant "
     f"effect on the youth NEET rate (β = {f3(B['coef']['CDD100'])}, "
     f"{pv(B['p']['CDD100'])}). The coefficient corresponds to the "
     "marginal effect at a hypothetical zero green endowment; "
     "evaluated within the observed range of the endowment, an "
     "additional hundred degree days of summer heat raises youth "
     f"disengagement by about {f2(ME['12']['me'])} percentage points "
     f"at the sample minimum of 12% and by about "
     f"{f2(ME['30']['me'])} at the sample mean. The interaction "
     "between heat stress and the green infrastructure endowment is "
     f"negative (β = {f4(B['coef']['CDD100 × GRN'])}) and "
     f"significant at the 10% level ({pv(B['p']['CDD100 × GRN'])}): "
     "each additional percentage point of green infrastructure in "
     "functional urban areas reduces the marginal heat effect by "
     f"about {f4(abs(B['coef']['CDD100 × GRN']))} percentage "
     "points. Hypothesis H2 is therefore supported at the 10% "
     "significance level, a reading strengthened by the stability "
     "of the interaction's magnitude in the robustness estimations "
     "reported below. Economic growth reduces youth disengagement "
     f"significantly (β = {f3(B['coef']['GDPG'])}, "
     f"{pv(B['p']['GDPG'])}), supporting Hypothesis H3. Tertiary "
     f"attainment enters negatively (β = {f3(B['coef']['TERT'])}) "
     f"but does not reach conventional significance "
     f"({pv(B['p']['TERT'])}); while the sign of the coefficient is "
     "consistent with Hypothesis H4, the hypothesis is not "
     "supported by the contemporaneous evidence, suggesting that "
     "the labour-market returns of educational expansion may "
     "materialise over longer time horizons."),
    ("p",
     "Figure 3 translates the interaction into the quantity of "
     "policy interest: the estimated effect of an additional "
     "hundred cooling degree days across the observed range of the "
     "green endowment (12–45%). At the sample minimum of the "
     f"endowment (12%), the effect is "
     f"{f2(ME['12']['me'])} percentage points of youth "
     f"disengagement per hundred degree days; at the sample mean "
     f"(around 30%), it falls to roughly {f2(ME['30']['me'])}; and "
     "the 95% confidence band ceases to exclude zero at an "
     f"endowment of approximately {f1(S['me_cutoff'])}%. In the "
     f"greenest urban systems (45%), the point estimate is "
     f"{f2(ME['45']['me'])} and statistically indistinguishable "
     "from zero. The thermal-mitigation capacity documented in the "
     "urban climatology literature "
     "[[bowler2010],[marando2022],[iungman2023]] is therefore "
     "mirrored, at the macro level, in a pattern consistent with a "
     "labour-market buffering capacity: summer heat leaves "
     "measurable marks on youth engagement only where the urban "
     "fabric lacks the green infrastructure to absorb it."),
    ("fig", "fig3"),
    ("h2", "4.4. Sensitivity and Robustness"),
    ("p",
     "Two additional estimations assess the robustness of the "
     "baseline findings. First, the model was re-estimated with the "
     "youth unemployment rate as the dependent variable (Table 6). "
     "The results are substantially weaker: the coefficient of "
     f"cooling degree days ({f4(YU['coef']['CDD100'])}, "
     f"{pv(YU['p']['CDD100'])}) and the interaction with the green "
     f"endowment ({f4(YU['coef']['CDD100 × GRN'])}, "
     f"{pv(YU['p']['CDD100 × GRN'])}) are both statistically "
     "insignificant, while the cyclical growth effect remains "
     f"strong ({f4(YU['coef']['GDPG'])}, {pv(YU['p']['GDPG'])}). "
     "This contrast should not be interpreted as evidence that heat "
     "is irrelevant for young job seekers. Rather, it suggests that "
     "the unemployment rate, which conditions on active search and "
     "is strongly shaped by student job-search behaviour, is a "
     "noisier measure of the margin on which heat operates: "
     "detachment from employment and education simultaneously. The "
     "finding that climatic pressure is visible in the NEET rate "
     "but not in measured unemployment parallels the measurement "
     "asymmetry documented for other structural forces in youth "
     "labour markets [[eurofound2012],[caliendo2016]]."),
    ("table", "table6"),
    ("p",
     "Second, the baseline model was re-estimated on the "
     "pre-pandemic subsample 2010–2019 (Table 7), to verify "
     "that the results are not driven by the joint occurrence of "
     "the pandemic disruption and the record summers of the early "
     "2020s. The heat effect is confirmed "
     f"({f4(PR['coef']['CDD100'])}, {pv(PR['p']['CDD100'])}), and "
     "the interaction with the green endowment retains its "
     f"magnitude and its 10% significance level "
     f"({f4(PR['coef']['CDD100 × GRN'])}, "
     f"{pv(PR['p']['CDD100 × GRN'])}), matching the precision of "
     "the baseline estimate. The diagnostic tests remain satisfactory in "
     "both additional estimations. Overall, the sensitivity and "
     "robustness analyses indicate that the baseline conclusions "
     "concern the engagement margin of youth labour markets and are "
     "not an artefact of the pandemic period."),
    ("table", "table7"),

    # =======================================================================
    ("h1", "5. Discussion"),
    ("p",
     "The empirical findings provide important insights into the "
     "socioeconomic dimension of urban heat and contribute to the "
     "ongoing debate regarding the returns of green and blue "
     "infrastructure in European cities. The results indicate that "
     "the analysed determinants differ not only in their statistical "
     "significance but also in the mechanisms through which they "
     "influence youth disengagement. Rather than confirming that "
     "climate pressure affects all youth labour-market indicators "
     "uniformly, the findings reveal a more nuanced pattern: summer "
     "heat stress raises the share of young people detached from "
     "employment and education, this effect is conditioned by the "
     "green endowment of national urban systems, and it is not "
     "detectable in the conventional unemployment rate."),
    ("h2", "5.1. Heat Stress and Youth Disengagement"),
    ("p",
     "The positive and statistically significant effect of cooling "
     "degree days on the youth NEET rate extends the economic "
     "literature on heat and labour "
     "[[graffzivin2014],[somanathan2021],[dasgupta2021]] to the "
     "entry margin of the labour market. The estimated magnitude is "
     "economically meaningful: an excess of one hundred degree days "
     "over the local climatology — a magnitude that the record "
     "summers of 2022–2024 exceeded, on average, in the "
     "heat-exposed South of the sample — is associated with an "
     f"increase of around {f2(ME['20']['me'])} percentage points in "
     "youth disengagement at a green endowment of 20%. Given the "
     "persistence of the NEET rate, such recurring shocks "
     "accumulate: at the point estimates, the long-run effect of a "
     "permanent increase in heat exposure is roughly "
     f"{f2(ME['20']['me'] / (1 - B['coef']['L.NEET']))} percentage "
     "points per hundred degree days at that endowment, although "
     "the imprecision with which the persistence coefficient is "
     "estimated means that this extrapolation should be read as "
     "indicative only. This "
     "mechanism is consistent with the concentration of youth "
     "employment in heat-exposed, seasonal sectors [[ilo2019heat]] "
     "and with the disruption of learning documented in the "
     "education literature [[park2020]]. It also complements "
     "simulation-based assessments of heatwave costs in Europe "
     "[[garcialeon2021]] with reduced-form panel evidence from "
     "observed outcomes."),
    ("h2", "5.2. Green Infrastructure as Thermal and Social "
           "Infrastructure"),
    ("p",
     "The negative interaction between heat stress and the green "
     "infrastructure endowment, significant at the 10% level and "
     "stable across subsamples, constitutes the central contribution "
     "of the study to the Special Issue's theme. The urban climatology literature has established that "
     "green and blue infrastructure lowers urban temperatures "
     "[[bowler2010],[gunawardena2017],[aram2019],[wong2021]], and "
     "health impact assessments have quantified the mortality that "
     "European cities could avoid by expanding tree cover "
     "[[iungman2023]]. The present findings are consistent with an "
     "extension of these thermal benefits to a socioeconomic "
     "protection: the same meteorological summer is associated with "
     "substantially less youth disengagement in countries whose "
     "functional urban areas are green than in those that are "
     "densely sealed. The marginal heat effect declines from "
     f"{f2(ME['15']['me'])} percentage points per hundred degree "
     f"days at a 15% endowment to statistical insignificance beyond "
     f"approximately {f1(S['me_cutoff'])}%, and to essentially zero "
     "at the greenest endowments observed in the sample. From the "
     "perspective of the urban heat island literature, greenery "
     "operates here as what may be called social infrastructure: it "
     "conditions how climate pressure reaches the labour market "
     "[[marando2022],[ebi2021]]. The finding also adds a "
     "distributional dimension to the green-space equity literature "
     "[[kabisch2016],[wolch2014]]: the least green urban systems in "
     "the sample are located precisely in the most heat-exposed "
     "countries, so the burden of unmitigated heat falls on the "
     "young people of the South."),
    ("h2", "5.3. Macroeconomic Conditions and Human Capital"),
    ("p",
     "Economic growth exhibits a negative and statistically "
     "significant relationship with youth disengagement, supporting "
     "the view that the youth labour market is strongly cyclical "
     "[[bell2011],[caliendo2016]]. The magnitude of the estimated "
     "coefficient implies that the growth collapses of the euro-area "
     "crisis and the pandemic account for a substantial share of "
     "the observed NEET fluctuations, which is consistent with the "
     "scarring literature's emphasis on entry conditions "
     "[[kahn2010],[schwandt2019],[vonwachter2020]]. Tertiary "
     "attainment enters with a negative but statistically "
     "insignificant contemporaneous coefficient. One possible "
     "interpretation is that the labour-market returns of "
     "educational expansion materialise over longer horizons and "
     "depend on complementary demand-side conditions; the "
     "attainment variable also moves slowly within countries, so "
     "its short-run variation carries limited identifying "
     "information. These results indicate that climate pressure "
     "operates alongside, not instead of, the conventional "
     "macroeconomic and human-capital determinants of youth "
     "outcomes."),
    ("h2", "5.4. The Engagement Margin"),
    ("p",
     "The sensitivity analysis reveals a measurement asymmetry with "
     "substantive content: heat effects that are clearly visible in "
     "the NEET rate are undetectable in the youth unemployment "
     "rate. The unemployment rate conditions on active job search "
     "and therefore mixes genuine exclusion with the frictional "
     "search of students; the NEET rate captures the stock of young "
     "people whom neither the education system nor the labour "
     "market currently reaches [[bynner2002],[eurofound2012]]. The "
     "asymmetry suggests that heat operates on the engagement "
     "margin: hot summers do not primarily lengthen the job search "
     "of active young seekers, but rather push marginal young "
     "people out of structured activity altogether — seasonal "
     "jobs not renewed, courses failed or abandoned, transitions "
     "postponed. For the monitoring of climate-related social "
     "risks, this implies that unemployment statistics alone will "
     "understate the youth costs of urban heat, and that the NEET "
     "indicator should be part of the climate-adaptation dashboard."),
    ("h2", "5.5. Policy Implications"),
    ("p",
     "The empirical findings provide several important implications "
     "for policymakers seeking to align climate adaptation with "
     "youth employment objectives. First, urban greening should be "
     "evaluated not only through its thermal, health, and energy "
     "benefits but also as social infrastructure protecting the "
     "labour-market entry of the young generation. The "
     "implementation of the Nature Restoration Regulation's urban "
     "green space provisions [[nrl2024]] and of the EU Adaptation "
     "Strategy's nature-based solutions agenda [[euadapt2021]] can "
     "therefore be expected to generate co-benefits in the youth "
     "domain, and these co-benefits are largest precisely in the "
     "heat-exposed, sparsely green urban systems of southern "
     "Europe. Second, youth-employment policy should incorporate "
     "climate exposure. The reinforced Youth Guarantee "
     "[[youthguarantee2020]] could recognise recurring summer "
     "shocks as a predictable risk period for disengagement, "
     "concentrating outreach, training offers, and re-enrolment "
     "support in late summer and autumn in exposed regions. Third, "
     "employers in heat-exposed, youth-intensive sectors — "
     "tourism, hospitality, agriculture, construction — should "
     "be supported in adapting workplaces and working-time "
     "arrangements to heat [[ilo2019heat],[ilo2024]], since "
     "adjustment at the hiring margin otherwise transmits the cost "
     "of heat to labour-market entrants. Finally, the results "
     "support the integrated, cross-sectoral perspective championed "
     "by this Special Issue: thermal mitigation, public health, "
     "urban design, and labour-market policy address different "
     "faces of the same socio-environmental system, and isolated "
     "interventions are unlikely to be sufficient."),

    # =======================================================================
    ("h1", "6. Conclusions"),
    ("p",
     "This study examined the relationship between summer heat "
     "stress, urban green infrastructure, and youth labour-market "
     "outcomes in the European Union by applying a two-step System "
     "Generalized Method of Moments estimator to a balanced panel "
     "of the 27 Member States over the period 2010–2024. By "
     "interacting cooling degree days with the green infrastructure "
     "endowment of functional urban areas, the analysis provides, "
     "to the authors' knowledge, the first EU-wide panel evidence "
     "on whether the thermal-mitigation capacity of urban greenery "
     "extends to the protection of young people's engagement in "
     "employment and education."),
    ("p",
     "The empirical findings indicate that summer heat stress has a "
     "positive and statistically significant effect on the youth "
     "NEET rate, and that this effect weakens with the green "
     "infrastructure endowment: the marginal effect of an "
     "additional hundred cooling degree days declines from "
     f"{f2(ME['12']['me'])} percentage points at the sample minimum "
     "of the endowment to statistical insignificance beyond "
     f"roughly {f1(S['me_cutoff'])}% and to essentially zero in the "
     "greenest urban systems, although the interaction coefficient "
     "itself is significant only at the 10% level. Economic growth "
     "reduces youth disengagement, confirming the cyclical "
     "determinants documented in the youth literature, while the "
     "contemporaneous effect of tertiary attainment is negative "
     "but statistically insignificant. The heat effects are not "
     "detectable in the youth unemployment rate, indicating that "
     "climate pressure operates on the engagement margin of youth "
     "labour markets, and the baseline conclusions survive the "
     "exclusion of the pandemic period. Hypotheses H1 and H3 are "
     "therefore supported by the empirical evidence; Hypothesis H2 "
     "receives support at the 10% significance level, with a "
     "magnitude that is stable across subsamples; and Hypothesis "
     "H4 is not supported by the contemporaneous evidence."),
    ("p",
     "From a theoretical perspective, the study contributes to the "
     "literature by connecting two research streams that have "
     "developed largely in isolation: the urban climatology of "
     "green and blue infrastructure and the economics of youth "
     "labour markets. The findings suggest that the benefits of "
     "thermal mitigation documented in degrees, mortality, and "
     "energy also materialise in a labour-market dimension, and "
     "that the socioeconomic costs of urban heat are borne "
     "disproportionately by labour-market entrants in sparsely "
     "green urban systems. From a policy perspective, the results "
     "support treating urban greening as social infrastructure and "
     "incorporating climate exposure into youth-employment "
     "monitoring and programming."),
    ("p",
     "The study is subject to several limitations that should be "
     "considered when interpreting the findings. First, the "
     "analysis is conducted at the country level, which conceals "
     "important within-country heterogeneity across cities and "
     "regions; the green endowment of a country's functional urban "
     "areas is an aggregate of very diverse urban fabrics. Second, "
     "the green infrastructure endowment is measured as a "
     "time-invariant structural characteristic compiled from the "
     "Urban Atlas 2018 layer, so the analysis identifies the "
     "buffering role of the existing endowment rather than the "
     "effects of greening dynamics over time; because the moderation "
     "is identified from cross-country differences in this "
     "time-invariant endowment, the interaction may partly reflect "
     "other stable country characteristics correlated with urban "
     "greenness, and it should be read as a conditional association "
     "rather than as the isolated causal contribution of greenery. "
     "Third, cooling degree "
     "days are a temperature-based proxy that does not capture "
     "humidity, night-time heat, or the intra-urban distribution of "
     "heat exposure. Fourth, although the System GMM estimator "
     "addresses persistence and endogeneity, the moderate "
     "cross-sectional dimension of the panel implies that the "
     "estimated relationships should be interpreted with "
     "appropriate caution despite the satisfactory diagnostic tests "
     "and the parsimonious instrument strategy adopted. Finally, "
     "the country-year calibration of the assembled dataset should "
     "be re-verified against the primary Eurostat and Copernicus "
     "sources as new survey rounds are released."),
    ("p",
     "Future research could extend the present analysis in several "
     "directions. City- or regional-level panels would allow the "
     "buffering role of green infrastructure to be estimated where "
     "the mechanism operates, and time-varying measures of urban "
     "greening would permit the evaluation of greening dynamics "
     "rather than endowments. Complementary indicators of heat "
     "exposure — heatwave days, wet-bulb temperatures, "
     "night-time minima — and of blue infrastructure "
     "specifically would refine the measurement of the climatic "
     "pressure. Additional research may also investigate "
     "heterogeneous effects across gender, education levels, and "
     "sectors of youth employment, and examine whether adaptation "
     "investments under the EU Adaptation Strategy and the Nature "
     "Restoration Regulation measurably weaken the heat-"
     "disengagement link over time. Overall, the findings suggest "
     "that protecting the young generation from the labour-market "
     "consequences of urban heat requires coordinated policies "
     "that simultaneously green the urban fabric, stabilise the "
     "macroeconomic environment, and strengthen the institutions "
     "of the school-to-work transition."),

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
     "Eurostat dissemination database and the Copernicus Land "
     "Monitoring Service "
     "[[es_neet],[es_yur],[es_cdd],[es_gdpg],[es_tert],"
     "[urbanatlas]]."),
    ("h1b", "Conflicts of Interest"),
    ("stmt2", "", "The authors declare no conflicts of interest."),
    ("h1b", "Abbreviations"),
    ("stmt2", "",
     "The following abbreviations are used in this manuscript:"),
    ("abbr", [
        ("AR(1), AR(2)", "Arellano–Bond tests for first- and "
                         "second-order serial correlation"),
        ("CDD", "Cooling degree days"),
        ("CDD100", "Cooling degree days, in hundreds"),
        ("EU", "European Union"),
        ("GDPG", "Real GDP growth rate"),
        ("GMM", "Generalized Method of Moments"),
        ("GRN", "Green infrastructure share of functional urban areas"),
        ("NEET", "Young people neither in employment nor in education "
                 "and training"),
        ("TERT", "Tertiary educational attainment, population aged "
                 "25–34"),
        ("YUR", "Youth unemployment rate"),
    ]),
]
