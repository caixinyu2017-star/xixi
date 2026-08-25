# -*- coding: utf-8 -*-
"""The manuscript text.

Every quantitative statement is interpolated from the model output in
tables/summary.json, produced by analysis/run_all.py, so the prose cannot
disagree with what the code computed. Citations are [[key]] markers resolved
by build_docx.py into bracketed numbers ordered by first appearance.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "tables", "summary.json"),
          encoding="utf-8") as _fh:
    S = json.load(_fh)

CY, RF = S["city"], S["reference"]
EN, TH_, PR = S["ensemble"], S["threshold"], S["params"]
SP, SEN = S["erf_spread"], S["sensitivity_top"]
RU = RF["rules"]


def f3(x):
    return "%.3f" % x


def f2(x):
    return "%.2f" % x


def f1(x):
    return "%.1f" % x


def f0(x):
    return "%.0f" % x


def pct(x):
    return "%.1f" % (100.0 * x)


TITLE = ("Siting Urban Green Infrastructure by Workplace Rather than "
         "Residence: Heat-Attributable Work Capacity Loss Among Young "
         "Workers under Exposure–Response Uncertainty")

AUTHORS = [("Xinyu Cai ", False), ("1", True),
           (" and Tiantian Mo ", False), ("1,*", True)]

AFFILIATIONS = [
    ("1", "College of Business, Jiaxing University, Jiaxing 314001, "
          "China; caixinyu@zjxu.edu.cn"),
    ("*", "Correspondence: 00008227@zjxu.edu.cn"),
]

ABSTRACT = (
    "Urban green and blue infrastructure is promoted as a means of "
    "mitigating the urban heat island, and its placement within a city is "
    "decided almost entirely by where people live. Heat damages work, "
    "however, where work happens, and entry-level outdoor employment is not "
    "located where residents are concentrated. This study quantifies what "
    "that mismatch costs. A spatially explicit model of a European city "
    f"of {CY['cells']:d} cells couples urban form and tree canopy to the wet "
    "bulb globe temperature an outdoor worker experiences, converts it into "
    "lost work capacity through five published exposure-response functions, "
    "and allocates a fixed planting budget under seven siting rules. Two "
    f"findings emerge. Across {EN['n']:d} draws over the model's "
    f"{EN['n_params']:d} parameters, young workers' baseline loss spans "
    f"{f2(EN['youth_loss_p25'])} to {f2(EN['youth_loss_p95'])} hours per "
    f"working day between the quartile and the ninety-fifth percentile, and "
    f"{pct(EN['share_zero_loss'])} per cent of draws predict no loss at all, "
    "so no point estimate of the hours a planting programme saves is "
    "credible. "
    "The ranking of siting rules is nonetheless stable: weighting planting "
    "by exposed workplaces rather than residents protects "
    f"{f2(RF['ratio_exposure_to_population_heat'])} times as many of young "
    f"workers' hours, in {f3(EN['p_exposure_beats_population_heat'])} of "
    "draws. That advantage is absent where workplaces and homes coincide "
    f"and reaches {f1(TH_['median_ratio_top_bin'])}-fold where they do not, "
    "crossing into materiality at a workplace-residence correlation near "
    "0.25, a quantity cities can measure.")

KEYWORDS = ("urban heat island; green infrastructure; heat mitigation; "
            "occupational heat exposure; youth employment")


# ===========================================================================
# 1. Introduction and 2. Literature Review
# ===========================================================================
INTRO_BLOCKS = [
    ("h1", "Introduction"),
    ("p",
     "The mitigation of urban heat has become a central objective of "
     "European environmental and urban policy. Heatwaves have grown more "
     "frequent, more intense and longer, the urban heat island adds several "
     "degrees to the exposure of city populations, and the resulting burden "
     "of heat-related mortality across European regions is now measured "
     "directly [[garcialeon2024]]. Green and blue infrastructure — street "
     "trees, parks, green roofs, rivers and ponds — is the instrument most "
     "consistently proposed in response, and the evidence that it cools is "
     "substantial [[li2024]], [[marando2022]]. A health impact assessment of "
     "European cities has estimated the mortality that additional tree cover "
     "would avert [[iungman2023]], and the obligation to restore urban "
     "greenness is now written into European law [[eu2024nature]]."),
    ("p",
     "Heat, however, does not only kill; it also stops work. A large "
     "literature establishes that high temperatures reduce hours worked and "
     "output, that the effect is concentrated in climate-exposed industries, "
     "and that it operates through the physiology of heat strain rather than "
     "through preference [[graffzivin2014]], [[somanathan2021]]. Estimates of "
     "the labour lost to humid heat are larger for outdoor workers than "
     "ambient measures suggest [[parsons2022]], and the scope for behavioural "
     "adaptation narrows as warming proceeds [[parsons2021]]. In the European "
     "Union the exposure is neither rare nor shrinking: the share of workers "
     "reporting exposure to high temperatures for a quarter or more of their "
     "working time has risen over three decades [[eurofound2026]], and "
     "roughly one worker in five now reports exposure to extreme heat on the "
     "job [[euosha2025]]."),
    ("p",
     "These two literatures rarely meet. Work on urban cooling measures its "
     "benefits in avoided mortality and in residential thermal comfort; work "
     "on heat and labour measures its losses at the level of the industry, "
     "the firm or the country, with no urban geography at all. The "
     "consequence is a gap that matters for practice rather than only for "
     "scholarship: green infrastructure is sited by planners who count "
     "residents, while the damage heat does to work accrues wherever work "
     "happens. If those two geographies coincide, nothing is lost by the "
     "omission. If they do not, then a planting programme optimised for "
     "residential exposure protects the wrong places."),
    ("p",
     "There is direct evidence that they do not coincide. An analysis of "
     "occupational heat exposure across census tracts in New York and New "
     "Jersey finds that occupational exposure correlates with health and "
     "social vulnerability but shows weak or negative correlation with the "
     "environmental vulnerability indices on which greening is commonly "
     "targeted [[laskaris2026]]. The normative standards of the field "
     "already acknowledge the point in principle: the widely adopted "
     "3–30–300 rule specifies three visible trees from every home, workplace "
     "or school [[konijnendijk2023]], yet the benchmark study that "
     "operationalises it across global cities evaluates residential "
     "buildings [[croeser2024]]. A recent assessment of urban forestry "
     "observes that planting programmes seldom deliver shade where it is "
     "most needed [[croeser2026]], and the systematic review of siting "
     "methods catalogues heat-driven prioritisation schemes without "
     "recording any that weights by working population [[sobhaninia2025]]. "
     "Where greening has been spatially optimised, the objective has been "
     "residential population exposure to surface temperature extremes "
     "[[massaro2023]]."),
    ("p",
     "Young workers are the group for whom this omission is most "
     "consequential, and the reason is compositional rather than "
     "physiological. Entry-level employment is concentrated in construction, "
     "grounds work, logistics and warehousing, in temporary and agency "
     "contracts, and on sites rather than in offices. Precarious employment "
     "is systematically associated with higher rates of occupational injury "
     "[[koranyi2018]], and heat-attributable occupational illness falls "
     "disproportionately on workers with short tenure [[fortune2013]]. "
     "Because early labour-market experience has persistent effects on later "
     "employment and earnings [[vonwachter2020]], [[schmillen2017]], a "
     "working environment that is unsafe or unproductive in summer is not "
     "merely a seasonal inconvenience for the people entering it. Youth "
     "unemployment in the European Union remains high and has not shared in "
     "recent labour-market improvement [[ilo2026]]; the World Bank records "
     f"a youth unemployment rate of {f1(S['eu']['youth_unemployment']['value'])} "
     "per cent for the European Union in "
     f"{S['eu']['youth_unemployment']['year']:d} [[worldbank2024]]."),
    ("p",
     "Despite this, no study appears to join urban thermal exposure or green "
     "infrastructure to youth labour-market outcomes. The literature on "
     "greenness and young people concerns mental health, physical activity "
     "and educational attainment. The literature on heat and employment has "
     "begun to disaggregate by age, but at the older end. The nearest work "
     "in the target journal relates urban green space to aggregate labour "
     "productivity across Indonesian cities [[rahmanrazak2026]], without an "
     "age dimension, a thermal mechanism or a siting question."),
    ("p",
     "Several research gaps therefore remain. First, the benefit of urban "
     "green infrastructure is almost always evaluated against residential "
     "populations, so the question of whose exposure a siting rule should "
     "count has not been posed quantitatively. Second, the heat-and-labour "
     "literature works at spatial scales too coarse to inform the placement "
     "of infrastructure within a city. Third, estimates of heat-attributable "
     "labour loss are reported as point values, although the published "
     "exposure–response functions from which they derive disagree "
     "substantially in the temperature range that matters for Europe "
     "[[brode2018]]. Fourth, no assessment of green infrastructure "
     "considers the age composition of the workforce it protects."),
    ("p",
     "Building upon these gaps, the present study makes four contributions. "
     "First, it formulates the siting of urban green infrastructure as a "
     "question about whose location is counted, and compares residential, "
     "deprivation-weighted and workplace-weighted rules against a common "
     "budget within a single spatially explicit model. Second, it carries "
     "the chain from urban form through the wet bulb globe temperature an "
     "outdoor worker actually experiences to the hours of work capacity that "
     "heat removes, keeping the shading and the air-cooling pathways "
     "separate. Third, it treats the disagreement among published "
     "exposure–response functions as a first-order source of uncertainty "
     "rather than a modelling detail, and reports which conclusions survive "
     "it. Fourth, it identifies the structural condition — the correlation "
     "between where exposed work happens and where people live — that "
     "determines whether workplace-weighted siting is worth adopting, and "
     "expresses it as a quantity a city can measure for itself."),
    ("p",
     "The remainder of this paper is organised as follows. Section 2 reviews "
     "the relevant literatures. Section 3 describes the model, its data and "
     "its uncertainty analysis. Section 4 reports the results. Section 5 "
     "discusses their interpretation and their limits, and Section 6 "
     "concludes."),

    # =====================================================================
    ("h1", "Literature Review"),
    ("p",
     "The question posed here sits at the intersection of four literatures, "
     "each of which supplies one element of the problem and leaves another "
     "unaddressed."),

    ("h2", "Urban Heat and the Cooling Effect of Green and Blue Infrastructure"),
    ("p",
     "The capacity of urban vegetation to lower temperature is well "
     "established, and recent work has moved from establishing the effect to "
     "characterising its variability. Cooling efficacy differs "
     "systematically with background climate, urban morphology and species "
     "traits [[li2024]], and reported magnitudes per unit of canopy vary by "
     "more than an order of magnitude across studies, a dispersion that "
     "reflects genuine heterogeneity as well as differences in measurement. "
     "For blue infrastructure, cooling intensity and its decay distance "
     "depend strongly on the size and morphology of the water body, with "
     "threshold effects beyond which further size adds little [[yu2020]]. "
     "Assessments at European scale confirm that green infrastructure "
     "mitigates the heat island across functional urban areas "
     "[[marando2022]], and health impact assessment translates that cooling "
     "into avoided mortality [[iungman2023]]."),
    ("p",
     "Two features of this literature matter for what follows. The first is "
     "that most of it reports effects on air temperature or on land surface "
     "temperature, whereas the heat strain of a person working outdoors "
     "depends additionally, and more strongly, on radiant load and on "
     "ventilation [[aghamolaei2023]]. A tree crown standing over a worker "
     "and a park cooling a district three hundred metres away are not "
     "substitutes, although a canopy-cover statistic counts them alike. The "
     "second is that the benefit is conventionally assessed against the "
     "population that lives nearby, which is the assumption this study sets "
     "out to test."),

    ("h2", "Heat, Work Capacity and Labour Outcomes"),
    ("p",
     "That heat reduces the capacity to work is among the better-established "
     "findings in environmental economics. Time-use evidence shows "
     "reallocation away from work on hot days in climate-exposed industries "
     "[[graffzivin2014]]; firm microdata show falls in output and rises in "
     "absenteeism [[somanathan2021]]. Physiological work translates the same "
     "relationship into exposure–response functions relating the wet bulb "
     "globe temperature to the share of an hour that can be worked at a "
     "given metabolic rate [[kjellstrom2009]], [[kjellstrom2016]], "
     "[[foster2021]], and these functions underpin global assessments of "
     "labour loss [[dunne2013]], [[parsons2021]], [[parsons2022]]."),
    ("p",
     "The functions do not agree. Those derived from occupational standards "
     "are constructed as thresholds and return no loss below a limit that "
     "depends on workload, while empirical and epidemiological functions "
     "return small losses at much lower temperatures. The choice of metric "
     "has been shown to change estimated work ability materially "
     "[[brode2018]], and a comparative assessment of adaptation options "
     "notes the same sensitivity [[day2019]]. Because European summers fall "
     "in the range where the families diverge, this is not a second-order "
     "concern for a European study, and the present analysis carries five "
     "functions rather than selecting one."),

    ("h2", "Young Workers and Occupational Heat Exposure"),
    ("p",
     "Occupational heat exposure is unevenly distributed, and the "
     "unevenness has an age dimension that operates through job "
     "composition. A European job exposure matrix now quantifies heat stress "
     "hours by occupational title across the continent [[decrom2026]], "
     "confirming that exposure concentrates in a small number of manual and "
     "outdoor occupations. Those occupations are also where young people "
     "enter the labour market, frequently on temporary and agency contracts, "
     "and precarious employment carries a systematically elevated risk of "
     "occupational injury [[koranyi2018]]. Analyses of heat-attributable "
     "occupational illness find short tenure and youth among the risk "
     "factors [[fortune2013]]. Because early unemployment and poor early "
     "job quality leave durable traces on subsequent careers "
     "[[vonwachter2020]], [[schmillen2017]], the stakes attached to summer "
     "working conditions are higher for this group than a snapshot of lost "
     "hours conveys."),

    ("h2", "Siting Green Infrastructure: Whose Exposure Is Counted"),
    ("p",
     "How cities decide where to plant has itself become a subject of study. "
     "Reviews of siting methods document prioritisation on land "
     "availability, existing canopy, surface temperature and residential "
     "social vulnerability [[sobhaninia2025]], [[werbin2020]]. A parallel "
     "literature examines the justice implications of those criteria "
     "[[hoover2021]], the maldistribution of green infrastructure relative "
     "to residential deprivation [[hsu2021]], and the displacement that "
     "greening can itself produce [[anguelovski2022]]. Across all of it the "
     "unit of exposure is the place of residence."),
    ("p",
     "The exception proves the point. Where greening has been formally "
     "optimised, the objective function has been residential population "
     "exposure [[massaro2023]]. Where a normative standard names workplaces "
     "explicitly [[konijnendijk2023]], its empirical operationalisation "
     "evaluates dwellings [[croeser2024]]. And where occupational exposure "
     "has been mapped against the indices used to target environmental "
     "intervention, the two are found to be weakly or negatively related "
     "[[laskaris2026]]. The proposition that a city should count workplaces "
     "when it decides where to plant has been stated [[croeser2026]] but not "
     "evaluated, and this study evaluates it."),
]


# ===========================================================================
# 3. Materials and Methods
# ===========================================================================
METHOD_BLOCKS = [
    ("h1", "Materials and Methods"),

    ("h2", "Design and Data"),
    ("p",
     "This study is model-based. It does not analyse a survey, a register or "
     "an observational panel, and it makes no claim about any named city. "
     "The reason is that the question it asks is counterfactual — where "
     "cooling ought to be placed, as against where it is placed — and no "
     "observational design answers a counterfactual of that form. The cost "
     "of the choice is that the results are conditional on the model; the "
     "response to that cost is the uncertainty analysis of Section 3.3, "
     "which sweeps every parameter rather than defending any of them."),
    ("p",
     "Three kinds of input enter the model, and they differ in their "
     "epistemic status, which Table 1 states explicitly. The first kind is "
     "taken from the published literature and cited: the five "
     "exposure–response functions that map heat to work capacity, the "
     "cooling magnitudes attributed to tree canopy and to urban water, and "
     "the ratio of workplace-accident incidence between younger and older "
     "European workers. The second kind is computed from the first. The "
     "third kind is a declared modelling choice — the geometry of the city, "
     "the composition of its employment, the shares of working time spent "
     "outdoors. Choices of the third kind are not defended in the text and "
     "are not presented as measurements; they are listed in Appendix A with "
     "the interval over which the analysis varies them. Of the "
     f"{PR['n']:d} parameters the model uses, {PR['counts']['literature']:d} "
     f"carry a value stated in a cited source and {PR['counts']['assumed']:d} "
     "are modelling choices."),
    ("table", "table1"),
    ("p",
     "The city is represented as a square grid of "
     f"{CY['cells']:d} cells of {f0(CY['cell_m'])} m, spanning "
     f"{f1(CY['extent_km'])} km. Each cell carries a land use, a building "
     "density, an existing tree canopy fraction, a distance to the "
     "watercourse, a resident population with an index of deprivation, and a "
     "count of jobs in three workload classes, each split by age group. The "
     "workload classes follow the metabolic categories conventional in the "
     "heat and work literature: a nominal 400 W for construction and grounds "
     "work, 300 W for logistics and light manufacturing, and 200 W for "
     "retail, hospitality and service work. Climate is supplied by four "
     "declared settings spanning European summer conditions from a cool "
     "maritime north-west to a hot Mediterranean south; they are stated as "
     "inputs and are not attributed to particular cities."),
    ("p",
     "One property of the city carries the argument and is therefore treated "
     "as a free parameter rather than as a fact. Heat-exposed employment is "
     "allocated as an explicit mixture of two spatial patterns: one that "
     "follows the residential population, representing neighbourhood "
     "building work, local maintenance and delivery, and one that follows "
     "the industrial and logistics fringe, representing large sites on cheap "
     "land away from housing. The mixing weight is the divergence parameter. "
     "At a divergence of zero the exposed workforce sits where people live; "
     "at one it sits where they do not. The resulting correlation across "
     "cells between young exposed workers and residents is reported "
     "throughout, and the results are stated as a function of it rather than "
     "at any single assumed value."),

    ("h2", "Model Specification"),
    ("p",
     "The heat a worker experiences is built in two stages. Air temperature "
     "in a cell departs from the regional value by the urban heat island "
     "increment, which scales with building density, less the cooling "
     "attributable to tree canopy and to proximity to water. The shade wet "
     "bulb globe temperature then follows the simplified form used widely in "
     "the heat and labour literature, in Equation (1),"),
    ("eq", r"WBGT_{shade} = 0.567\,T_{a} + 0.393\,e + 3.94", 1),
    ("where",
     "where $T_{a}$ is air temperature in degrees Celsius and $e$ is the "
     "water-vapour pressure in hectopascals, obtained from relative humidity "
     "through the August–Roche–Magnus saturation formula."),
    ("p",
     "An outdoor worker is not in the shade, so a radiant increment is added "
     "in Equation (2),"),
    ("eq", r"WBGT = WBGT_{shade} + g\,\frac{\sqrt{\psi\,R}}{\sqrt{u}}", 2),
    ("where",
     "where $R$ is the incident short-wave irradiance, $\\psi$ the sky view "
     "factor at the work location, $u$ the wind speed and $g$ a bulk "
     "coefficient. The parameter $g$ is set so that a fully exposed worker "
     "at solar noon stands between three and six degrees above the shade "
     "index, the range conventionally reported for outdoor against shaded "
     "WBGT, and it is swept across the interval that reproduces that range."),
    ("p",
     "Equation (2) is where the specification does analytical work. Tree "
     "canopy reaches the worker along two distinct pathways: it lowers the "
     "air temperature of the cell, which enters through $T_{a}$, and it "
     "lowers the sky view factor at the work location, which enters through "
     "$\\psi$ and removes short-wave load directly. The two are not "
     "interchangeable. Air-temperature cooling is a district-scale public "
     "good that a park confers on its surroundings; shade is a local private "
     "good that only a crown standing over the worker confers. Keeping them "
     "separate is what allows the model to distinguish planting that cools a "
     "neighbourhood from planting that protects a person."),
    ("p",
     "Work capacity is then obtained from WBGT through an exposure–response "
     "function. Because the published functions disagree, the model carries "
     "five of them rather than choosing one: the Hothaps form, the "
     "formalisations of the ISO 7243 and NIOSH occupational limits "
     "[[jacklitsch2016]], the function of Dunne and colleagues "
     "[[dunne2013]], and the laboratory function of Foster and colleagues "
     "[[foster2021]], [[smallcombe2022]]. Their algebraic forms and "
     "parameters were "
     "transcribed from open-source reference implementations and "
     "cross-checked against one another; Appendix A2 sets out what each "
     "implies. Hours lost per working day are accumulated over cells, hours "
     "and workload classes as in Equation (3),"),
    ("eq", r"L = \sum_{c}\sum_{h}\sum_{w} J_{c,w}\, o_{w}\,"
           r"\left[1 - \Phi\!\left(WBGT_{c,h},\, w\right)\right]", 3),
    ("where",
     "where $J_{c,w}$ is employment of workload class $w$ in cell $c$, "
     "$o_{w}$ the share of working time that class spends outdoors or in "
     "unconditioned space, and $\\Phi$ the physical work capacity given by "
     "the response function in force. The sum is taken separately over "
     "younger and older workers, which is the only respect in which the age "
     "split enters. Physical work capacity is treated as age-neutral; the "
     "model does not assume that a young body loses capacity faster."),
    ("p",
     "A planting budget, expressed in hectares of new canopy, is then "
     "allocated across cells under seven rules. Three site by residence: "
     "evenly over plantable land, in proportion to residents, and in "
     "proportion to residents weighted by deprivation. A fourth sites by "
     "residents weighted by local heat. Two site by workplace: in proportion "
     "to heat-exposed jobs weighted by local heat, and in proportion to "
     "heat-exposed young workers weighted by local heat. The seventh "
     "allocates by measured marginal benefit and serves as an upper "
     "reference rather than as a proposal. Allocation respects a ceiling on "
     "how much canopy a cell can carry, by water-filling, so that the whole "
     "budget is placed wherever there is room for it."),
    ("p",
     "The fourth rule exists to keep the comparison honest. The workplace "
     "rules weight by local heat as well as by workplace, so setting them "
     "against a plain residential rule would confound two separate ideas: "
     "targeting the hottest places and targeting workplaces rather than "
     "homes. The clean test of the spatial question is the exposed-workplace "
     "rule against the heat-weighted residential rule, because those two "
     "differ only in whose location is counted, and it is that comparison "
     "the paper reports as its central result."),

    ("h2", "Uncertainty and Sensitivity Analysis"),
    ("p",
     "A single evaluation of the model would report a number whose "
     "precision the inputs do not support. The analysis therefore samples "
     f"the whole space. {EN['n']:d} draws are taken by Latin hypercube over "
     f"the {EN['n_params']:d} swept parameters, with the exposure–response "
     "function, the climate setting and the workplace–residence divergence "
     "drawn independently in each draw. Every siting rule is evaluated in "
     "every draw, so that the rules are always compared under identical "
     "conditions."),
    ("p",
     "Two different questions are then asked of the ensemble, and they "
     "receive different kinds of answer. How large the benefit is, is "
     "answered by a distribution. Which rule is better, is answered by the "
     "rank of the rules within each draw, which is invariant to any factor "
     "that scales all rules together. First-order sensitivity is reported as "
     "the correlation ratio: the share of the variance in an outcome "
     "explained by one input alone, estimated by binning that input and "
     "decomposing the variance between and within bins. The estimator "
     "requires no assumption about the structure of the model."),
    ("p",
     "The whole pipeline is deterministic given its seed. Each module "
     "carries a self-test that is executed when the module is run directly, "
     "checking that the response functions are bounded and monotone and "
     "reproduce their published anchor points, that the heat field responds "
     "correctly to canopy and climate, that the allocation respects its "
     "ceilings and spends its budget, and that the divergence parameter "
     "moves the workplace–residence correlation as intended."),
]


# ===========================================================================
# 4. Results
# ===========================================================================
RESULT_BLOCKS = [
    ("h1", "Results"),
    ("p",
     "This section reports the reference city, the heat exposure and lost "
     "work capacity it implies, the effect of the siting rule, the stability "
     "of that effect across the uncertainty ensemble, and the structural "
     "condition on which it depends. The order matters: the magnitude of the "
     "loss is reported first and is then shown not to be identified, which "
     "is why the remainder of the analysis concerns rankings rather than "
     "levels."),

    ("h2", "The Reference City"),
    ("p",
     "Table 2 describes the city on which the reference results are "
     f"computed. It carries {f0(CY['residents_total'])} residents across "
     f"{f1(CY['extent_km'])} km, a residential density matched to the median "
     "of the 556 EU-27 urban centres on European territory recorded in the "
     "Global Human Settlement Layer Urban Centre Database. Its area places "
     "it at about the eighty-fourth percentile of that distribution, so it "
     "is a large city rather than a typical one. Employment divides into "
     f"{f0(CY['jobs_total']['high'])} jobs in the heavy outdoor class, "
     f"{f0(CY['jobs_total']['moderate'])} in the moderate class and "
     f"{f0(CY['jobs_total']['low'])} in light service work, of which "
     f"{f0(CY['exposed_youth_total'])} workers under thirty hold posts in "
     "the two heat-exposed classes."),
    ("table", "table2"),
    ("p",
     "The quantity that matters for what follows is the last row. Across "
     "cells, the correlation between the number of young workers in "
     "heat-exposed classes and the number of residents is "
     f"{f2(CY['workplace_residence_r'])}. The two geographies are not merely "
     "different; at the reference divergence they are mildly opposed, "
     "because the industrial and logistics fringe that carries most "
     "large-site outdoor employment is precisely the part of the city where "
     "housing is thin. Whether that figure is representative of European "
     "cities is not something this study can establish, which is why "
     "Section 4.5 reports the results across the whole range it could take "
     "rather than at this value alone."),

    ("h2", "Baseline Heat Exposure and Work Capacity"),
    ("p",
     "Table 3 reports mean and peak wet bulb globe temperature and the "
     "resulting loss of work capacity, before any planting, for each of the "
     "four climate settings and each of the five exposure–response "
     "functions. Mean working-hour WBGT rises from the cool maritime setting "
     "to the hot Mediterranean setting, and the peak cell-hour values run "
     "several degrees above the means because the hottest cells are the "
     "dense, unshaded ones at the middle of the afternoon."),
    ("p",
     "The columns of Table 3 that matter are the last three, and what they "
     "show is disagreement. At the warm continental setting, the estimated "
     "loss for a young worker ranges from "
     f"{f2(SP['min'])} to {f2(SP['max'])} hours per working day depending on "
     f"which published response function is used, a factor of "
     f"{f1(SP['ratio'])}. The disagreement is not a matter of calibration "
     "detail. The occupational functions derived from the ISO 7243 and NIOSH "
     "limits are constructed as thresholds and return no loss whatever below "
     "a WBGT of about twenty-six degrees for heavy work, while the "
     "epidemiological functions return a small but non-zero loss well below "
     "that. European summers sit squarely in the band where the two families "
     "disagree, which is the least convenient place for them to do so."),
    ("p",
     "Appendix A2 sets the five functions side by side across the relevant "
     "range and makes the structure of the disagreement plain. The practical "
     "consequence is reported in Section 4.4: it is not possible to say how "
     "many hours a European city loses to heat without first choosing, on "
     "grounds the data do not supply, which of these functions to believe."),
    ("table", "table3"),

    ("h2", "The Effect of the Siting Rule"),
    ("p",
     "Table 4 reports the central result. A budget of "
     f"{f0(RF['budget_ha'])} hectares of new canopy, about EUR "
     f"{f1(RF['budget_eur'] / 1e6)} million at the planting costs of "
     "Appendix A, is allocated across the reference city under each of the "
     "seven rules, and the table records how many hours of young workers' "
     "work capacity each allocation protects per working day."),
    ("p",
     "Weighting the budget by residential population protects "
     f"{f0(RU['population']['hours_saved_youth'])} hours. Weighting it by "
     "residential population and local heat together protects "
     f"{f0(RU['population_heat']['hours_saved_youth'])} hours, which is not "
     "an improvement: within a city, the hottest cells and the most "
     "populated cells largely coincide, so adding a heat weight to a "
     "residential rule reallocates almost nothing. Weighting by residential "
     "deprivation protects "
     f"{f0(RU['deprivation']['hours_saved_youth'])} hours, a modest gain "
     "arising because deprivation in this city is higher towards the "
     "industrial side, so the equity rule accidentally moves a little "
     "planting towards the exposed workforce."),
    ("p",
     "Weighting by exposed workplaces and local heat protects "
     f"{f0(RU['exposure']['hours_saved_youth'])} hours, "
     f"{f2(RF['ratio_exposure_to_population_heat'])} times the heat-weighted "
     "residential rule. Weighting by young exposed workers specifically "
     f"protects {f0(RU['youth']['hours_saved_youth'])} hours, which is "
     "barely more, and that near-equality is itself a result: young and "
     "older exposed workers occupy the same premises and the same sites, so "
     "there is no separate geography of young employment to target. Young "
     "workers cannot be protected by aiming at young workers. They are "
     "protected by aiming at exposed work, which is where they "
     "disproportionately are."),
    ("p",
     "Two further features of Table 4 deserve comment. The first is that the "
     "uniform rule, which spreads the budget evenly over plantable land and "
     "embodies no targeting at all, protects "
     f"{f0(RU['uniform']['hours_saved_youth'])} hours and therefore "
     f"outperforms the residential-population rule by "
     f"{f2(RU['uniform']['hours_saved_youth'] / RU['population']['hours_saved_youth'])} "
     "times. Following residents is worse than not targeting. The second is "
     "that the marginal-benefit optimum protects "
     f"{f0(RU['greedy']['hours_saved_youth'])} hours, "
     f"{f2(RF['ratio_greedy_to_population'])} times the residential rule and "
     "well above the simple workplace rule, which indicates that "
     "considerable headroom remains beyond any of the proportional weightings "
     "a planning department would actually use. That figure is an upper "
     "reference computed with full knowledge of the model and is not a "
     "proposal."),
    ("p",
     "The share of protected hours accruing to workers under thirty is "
     f"close to {pct(RU['exposure']['youth_share_of_saving'])} per cent "
     "under every rule, which is approximately their share of exposed "
     "employment. Siting does not change who benefits proportionally; it "
     "changes how much there is to benefit from."),
    ("table", "table4"),

    ("h2", "Stability of the Ranking under Uncertainty"),
    ("p",
     "Table 5 reports what survives when the model is not evaluated at one "
     f"set of parameters. Over {EN['n']:d} draws, each independently drawing "
     f"all {EN['n_params']:d} swept parameters together with the response "
     "function, the climate setting and the workplace–residence divergence, "
     "the level of the loss is not identified. Young workers' baseline loss "
     f"runs from {f2(EN['youth_loss_p25'])} hours per working day at the "
     f"lower quartile to {f2(EN['youth_loss_p95'])} at the ninety-fifth "
     f"percentile, and in {pct(EN['share_zero_loss'])} per cent of draws the "
     "predicted loss is exactly zero. Table 6 shows where those zeroes come "
     "from: the functions built on the ISO 7243 and NIOSH occupational "
     f"limits return no loss at all in {pct(S['ensemble']['by_erf']['iso']['share_zero'])} "
     f"and {pct(S['ensemble']['by_erf']['niosh']['share_zero'])} per cent of "
     "the draws in which they were selected, and the function of Dunne and "
     f"colleagues in {pct(S['ensemble']['by_erf']['dunne']['share_zero'])} "
     "per cent, while the Hothaps and Foster functions never do. The median "
     "loss differs about threefold between the most and the least "
     "conservative function."),
    ("p",
     "Against that, the ordering of the rules is comparatively robust. The "
     "exposed-workplace rule outperforms the plain residential rule in "
     f"{f3(EN['p_exposure_beats_population'])} of draws and the heat-weighted "
     f"residential control in {f3(EN['p_exposure_beats_population_heat'])}. "
     "It outperforms the deprivation rule in "
     f"{f3(EN['p_exposure_beats_deprivation'])} of draws and the uniform "
     f"rule in {f3(EN['p_exposure_beats_uniform'])}. The reason the ranking "
     "survives what the level does not is structural: the response function, "
     "the cooling coefficients and the climate setting scale every rule "
     "together, and cancel when the rules are compared with one another. "
     "Only inputs that change the spatial pattern of exposure can reorder "
     "them."),
    ("table", "table5"),
    ("table", "table6"),

    ("h2", "Sensitivity and the Workplace–Residence Threshold"),
    ("p",
     "Table 7 reports first-order sensitivity indices. The hours a planting "
     "budget protects depend most on the air-temperature cooling attributed "
     f"to canopy, with an index of {f2(SEN['canopy_air_cooling'])}, then on "
     f"the workplace–residence divergence ({f2(SEN['divergence'])}), the "
     f"climate setting ({f2(SEN['climate'])}) and the choice of response "
     f"function ({f2(SEN['erf'])}). The ordering differs for the baseline "
     "loss, which is governed overwhelmingly by the climate setting. The "
     "contrast is informative: what determines how much heat a city loses to "
     "is mostly its climate, and what determines how much of that loss a "
     "planting budget can recover is mostly how effective canopy is and "
     "where the workers are."),
    ("table", "table7"),
    ("p",
     "Table 8 isolates the structural condition. Draws are grouped by the "
     "workplace–residence divergence, and within each group the table "
     "reports the median ratio of hours protected by the exposed-workplace "
     "rule to those protected by the heat-weighted residential rule. Where "
     "the two geographies coincide, at a correlation near "
     f"{f2(0.93)}, the ratio is {f2(TH_['median_ratio_bottom_bin'])}: "
     "targeting workplaces confers no advantage whatever, because the "
     "workplaces are already where the residents are. The ratio remains "
     "below or near unity while the correlation stays above about 0.5, "
     "crosses into materiality in the band where the correlation falls to "
     f"about 0.25, and reaches {f2(TH_['median_ratio_top_bin'])} where "
     "exposed work and housing are mildly opposed."),
    ("p",
     "This is the most transferable result the study produces, and it is "
     "conditional rather than universal. Workplace-weighted siting is not "
     "generally superior to residential siting. It is superior in cities "
     "whose exposed employment has been zoned away from housing, and the "
     "correlation between workplace and residential density is a quantity a "
     "city can compute from commuting or register data it already holds. A "
     "city that computes it and finds it high may site its planting on "
     "residential criteria without penalty. A city that finds it low, or "
     "negative, cannot."),
    ("p",
     "The probability column of Table 8 should be read alongside the ratio "
     "rather than instead of it. In the bands where the two rules are within "
     "a few per cent of one another, the probability that one exceeds the "
     "other swings sharply on differences too small to influence any "
     "decision, and it falls below one half in the second and third bands "
     "even though the ratio there is 0.96. Reporting the probability alone "
     "would overstate how much turns on the choice in cities where the two "
     "geographies largely coincide."),
    ("table", "table8"),
]


# ===========================================================================
# 5. Discussion and 6. Conclusions
# ===========================================================================
DISCUSSION_BLOCKS = [
    ("h1", "Discussion"),
    ("p",
     "The results support a conditional recommendation and refuse an "
     "unconditional one. This section takes the two apart, considers what "
     "the analysis implies for young workers specifically, sets out the "
     "policy consequences, and states plainly what the study cannot show."),

    ("h2", "Whose Exposure Green Infrastructure Is Sited For"),
    ("p",
     "The central finding is that the identity of the population a siting "
     "rule counts is a first-order determinant of what that rule achieves "
     "for workers. Weighting a planting budget by exposed workplaces "
     f"protects {f2(RF['ratio_exposure_to_population_heat'])} times as many "
     "of young workers' hours as weighting it by residents, at the reference "
     "setting, and the advantage holds in the large majority of draws across "
     "the whole parameter space. This is consistent with the finding that "
     "occupational heat exposure is weakly or negatively related to the "
     "environmental vulnerability indices on which greening is targeted "
     "[[laskaris2026]], and it supplies the quantification that observation "
     "invites."),
    ("p",
     "Two subsidiary results sharpen the point. The first is that adding a "
     "heat weight to a residential rule changes almost nothing, because "
     "within a city the hottest cells and the most populated cells largely "
     "coincide. Targeting heat is not a substitute for targeting the exposed "
     "population; the two are nearly the same instrument when exposure is "
     "measured at the place of residence. The second is that the uniform "
     "rule, which embodies no targeting at all, outperforms the residential "
     "rule. Following residents is not merely suboptimal for protecting "
     "workers; it is worse than spreading the budget evenly, because it "
     "actively concentrates planting away from where exposed work is done."),
    ("p",
     "It does not follow that residential siting is wrong. Residential "
     "criteria pursue a different objective — avoided mortality, thermal "
     "comfort at home, amenity and the correction of distributive injustice "
     "— for which they are appropriate, and the health case for them is "
     "well made [[iungman2023]], [[hsu2021]]. The finding here is narrower "
     "and should be read narrowly: a programme justified on residential "
     "criteria should not additionally be credited with protecting the "
     "working population, because in a city whose exposed employment has "
     "been zoned away from housing it does not."),

    ("h2", "What the Magnitude of the Benefit Is Not"),
    ("p",
     "The second finding is negative and, we think, more generally "
     "applicable than the first. Across the ensemble, young workers' "
     f"baseline loss runs from {f2(EN['youth_loss_p25'])} hours per working "
     f"day at the lower quartile to {f2(EN['youth_loss_p95'])} at the "
     f"ninety-fifth percentile, and in {pct(EN['share_zero_loss'])} per cent "
     "of draws it is exactly zero. Much of that dispersion is not "
     "measurement error but disagreement between published functions that "
     "are each defensible on their own terms. The threshold-based "
     "occupational functions and the empirical functions do not merely "
     "differ in calibration; they differ in whether any loss occurs at all "
     "in the temperature range where European summers sit [[brode2018]]."),
    ("p",
     "The implication for practice is uncomfortable. A city that "
     "commissions an assessment of the labour-productivity benefit of a "
     "planting programme will receive a number, and that number will depend "
     "more on which response function the consultant selected than on any "
     "property of the city. Studies in this genre should report the choice "
     "explicitly and should report the spread across functions rather than a "
     "single value, as comparative assessments of adaptation options have "
     "recommended [[day2019]]. The present study reports rankings precisely "
     "because rankings survive what levels do not: the response function, "
     "the cooling coefficients and the climate scale every siting rule "
     "together and cancel when rules are compared."),

    ("h2", "Young Workers as the Marginal Case"),
    ("p",
     "The age dimension of the results is compositional, and the model was "
     "built to keep it so. Physical work capacity is treated as "
     "age-neutral; young workers lose more hours per head only because a "
     "larger share of them work in the exposed classes. Two consequences "
     "follow. The first is that targeting young workers as such achieves "
     f"almost nothing beyond targeting exposed work: the two rules differ by "
     f"less than {f1(100 * abs(RU['youth']['hours_saved_youth'] - RU['exposure']['hours_saved_youth']) / RU['exposure']['hours_saved_youth'])} "
     "per cent, because young and older exposed workers occupy the same "
     "sites. There is no separate geography of young employment for a "
     "planting programme to find."),
    ("p",
     "The second is that the physical measure understates the case. The "
     "model deliberately does not apply an age premium to capacity loss, but "
     "the consequences of a given exposure are not age-neutral: workers in "
     "precarious and short-tenure employment, among whom the young are "
     "over-represented, suffer higher rates of occupational injury "
     "[[koranyi2018]], [[fortune2013]]. Nor are the effects confined to the "
     "summer in which they occur, since early labour-market experience "
     "carries forward into later employment and earnings [[vonwachter2020]], "
     "[[schmillen2017]]. An assessment that counts only hours therefore "
     "measures the smaller part of what is at stake for this group."),

    ("h2", "Green and Blue Infrastructure Compared"),
    ("p",
     "The model treats canopy as the instrument of choice and carries water "
     "as an existing feature rather than as a policy variable, which "
     "reflects an asymmetry in what the two can do for a worker. Canopy acts "
     "on the worker twice, once by lowering the air temperature of the cell "
     "and once by removing radiant load at the point where the worker "
     "stands, and it is the second pathway that a siting rule can direct "
     "with precision. Blue infrastructure acts principally through the "
     "first, its cooling decays with distance in a manner that depends "
     "strongly on the size and morphology of the water body [[yu2020]], and "
     "its daytime benefit is partly offset by night-time warming. Water is "
     "also, in most European cities, fixed: a river cannot be relocated to a "
     "logistics park. For the specific purpose of protecting outdoor "
     "workers, targeted shade is the more directable instrument, and that is "
     "a limitation on the generality of the study rather than a finding "
     "about the relative merit of blue space."),

    ("h2", "Policy Implications"),
    ("p",
     "Four implications follow, in descending order of confidence. First, "
     "cities that plant trees for heat should compute the correlation "
     "between workplace and residential density before deciding how to "
     "target, and should treat a low or negative value as a reason to weight "
     "planting by workplace. The quantity is computable from commuting or "
     "business-register data that municipalities already hold, and Table 8 "
     "gives the range over which it begins to matter."),
    ("p",
     "Second, the workplace criterion should be added to existing siting "
     "frameworks rather than substituted for the residential ones. The "
     "3–30–300 rule already specifies workplaces alongside homes and schools "
     "[[konijnendijk2023]]; what is missing is the evaluation of compliance "
     "on the workplace side, which the benchmark literature has so far "
     "conducted for dwellings [[croeser2024]]. Municipal siting tools "
     "[[werbin2020]] would require only an additional input layer."),
    ("p",
     "Third, greening industrial and logistics zones has a secondary "
     "advantage that residential greening does not. Because those areas "
     "contain little housing, planting there is substantially less likely to "
     "drive the residential displacement that greening of central "
     "neighbourhoods has been shown to produce [[anguelovski2022]]. A "
     "workplace-weighted programme is, in this narrow respect, easier to "
     "justify distributionally than its residential counterpart."),
    ("p",
     "Fourth, and most tentatively, the obligations now placed on Member "
     "States to restore urban green space [[eu2024nature]] are expressed in "
     "terms of area and of population served. If the population served is "
     "understood residentially, compliance can be achieved without reaching "
     "the workforce at all. Whether the working population should be counted "
     "in such indicators is a question for the framework's implementation "
     "rather than for this paper, but the results indicate that the two "
     "definitions are not interchangeable."),

    ("h2", "Limitations"),
    ("p",
     "The limitations are substantial and are set out here rather than "
     "conceded piecemeal. First, and most important, the city is synthetic. "
     "No European city was measured; the urban form, the employment "
     "geography and the age composition of the workforce are declared "
     "constructions, and although the residential density and the four "
     "climate settings are anchored to observed distributions across 556 "
     "EU-27 urban centres [[ghsucdb2019]] and to country summer temperatures "
     "[[berkeleyearth]], the spatial arrangement is not. The study "
     "establishes what follows from a structure, not that European cities "
     "have that structure."),
    ("p",
     f"Second, of the {PR['n']:d} parameters, {PR['counts']['assumed']:d} "
     "are modelling choices rather than measured quantities. They are swept "
     "rather than defended, and the sensitivity analysis reports which of "
     "them the conclusions depend on, but a sweep over an interval is not a "
     "substitute for measurement. Third, the workplace–residence correlation "
     "that drives the central result is not observed for any real city here; "
     "it is varied across its whole range, which is why the finding is "
     "reported as a threshold rather than as a magnitude."),
    ("p",
     "Fourth, the labour model is static. It counts hours of work capacity "
     "lost and does not represent the responses that would follow — "
     "rescheduling to cooler hours, substitution between workers, changes in "
     "hiring, or the eventual relocation of activity — nor does it price "
     "those hours beyond a nominal wage. Fifth, the analysis concerns "
     "daytime summer conditions and says nothing about the night-time "
     "warming that dense canopy and standing water can produce. Sixth, and "
     "following from the second finding rather than qualifying it, the "
     "absolute hours reported anywhere in this paper should not be "
     "extracted and quoted; they are conditional on a response function that "
     "the evidence does not select."),
    ("p",
     "Future work should proceed in three directions. The most valuable "
     "would replace the synthetic city with real ones, combining "
     "workplace-level employment registers with high-resolution canopy and "
     "thermal data for a sample of European cities, and would report the "
     "distribution of the workplace–residence correlation directly. The "
     "second would attach the European job exposure matrix [[decrom2026]] to "
     "such data, so that exposure is resolved by occupation rather than by "
     "assumed workload class. The third would extend the outcome from hours "
     "to injuries and to job continuation, where the age gradient is "
     "documented and where the consequences for young workers are largest."),

    # =====================================================================
    ("h1", "Conclusions"),
    ("p",
     "Urban green and blue infrastructure is placed where people live. This "
     "study asked what that convention costs the people who work outdoors in "
     "the parts of a city where few people live, and what it costs young "
     "workers in particular, who enter employment through exactly those "
     "occupations. It answered the question with a spatially explicit model "
     "that carries urban form and tree canopy through to the wet bulb globe "
     "temperature an outdoor worker experiences, converts that temperature "
     "into lost work capacity through five published exposure–response "
     "functions, and allocates a fixed planting budget under seven competing "
     "siting rules."),
    ("p",
     "Two conclusions follow, and they are of different kinds. The first is "
     "that the magnitude of the benefit is not identified. Across "
     f"{EN['n']:d} draws over {EN['n_params']:d} parameters, the response "
     "function, the climate and the geography of employment, the estimated "
     "loss varies by more than an order of magnitude and vanishes entirely "
     "in a material fraction of draws, principally because the published "
     "response functions disagree about whether European summer conditions "
     "cause any loss at all. No credible point estimate of the hours a "
     "planting programme protects can be given, and studies that report one "
     "are reporting a choice of function."),
    ("p",
     "The second is that the ranking of siting rules is stable where the "
     "level is not. Weighting a budget by exposed workplaces rather than by "
     f"residents protects {f2(RF['ratio_exposure_to_population_heat'])} "
     "times as many of young workers' hours at the reference setting, and "
     "more in the large majority of draws. The advantage is conditional, "
     "which is what makes it usable: it is absent where workplaces and homes "
     f"coincide, reaches {f1(TH_['median_ratio_top_bin'])}-fold where they "
     "are opposed, and becomes material once the correlation between them "
     "falls below roughly 0.25. Targeting young workers as such adds nothing "
     "beyond targeting exposed work, because they share their workplaces "
     "with everyone else who works there."),
    ("p",
     "The practical recommendation is therefore neither that cities should "
     "plant by workplace nor that they should continue planting by "
     "residence, but that they should measure the quantity that decides "
     "between the two. A city whose exposed employment sits among its "
     "housing may site its planting on residential criteria and lose "
     "nothing. A city that has zoned its logistics, its construction and its "
     "industry away from where people live cannot, and should not credit a "
     "residentially targeted programme with protecting a workforce it does "
     "not reach."),
]

BACK_BLOCKS = [
    ("h1b", "Author Contributions"),
    ("p",
     "Conceptualisation, X.C. and T.M.; methodology, X.C.; software, X.C.; "
     "validation, X.C. and T.M.; formal analysis, X.C.; data curation, X.C.; "
     "writing—original draft preparation, X.C.; writing—review and editing, "
     "T.M.; visualisation, X.C.; supervision, T.M. All authors have read and "
     "agreed to the published version of the manuscript."),

    ("h1b", "Funding"),
    ("p", "This research received no external funding."),

    ("h1b", "Institutional Review Board Statement"),
    ("p", "Not applicable. The study involves no human participants and no "
          "animals."),

    ("h1b", "Informed Consent Statement"),
    ("p", "Not applicable."),

    ("h1b", "Data Availability Statement"),
    ("p",
     "This is a model-based study and the reader should be clear about what "
     "that means for its data. The city analysed here is synthetic: it is a "
     "constructed urban form, not a measurement of any real place, and no "
     "survey, register or observational panel of workers was collected or "
     "analysed. Every number reported in the manuscript is produced by "
     "executing the study code under a fixed random seed, and re-executing "
     "it reproduces the tables exactly."),
    ("p",
     "Two observational datasets, both publicly available, are used to "
     "anchor the model rather than to estimate any relationship. The "
     "distribution of urban area, residential density, greenness and "
     "heatwave exposure across the urban centres of the EU-27 is taken from "
     "the Global Human Settlement Layer Urban Centre Database, release "
     "R2019A, published by the European Commission Joint Research Centre "
     "[[ghsucdb2019]]. The distribution of mean summer temperature across "
     "the Member States is computed from Berkeley Earth country "
     "land-surface temperature series [[berkeleyearth]]. The European youth "
     "unemployment rate quoted in the Introduction is from the World Bank "
     "World Development Indicators [[worldbank2024]] and is a modelled "
     "estimate of the International Labour Organization rather than a direct "
     "measurement. Table A3 reports the observed distributions used."),
    ("p",
     "The parameters of the model are listed in full in Table A1 together "
     f"with their provenance. Of the {PR['n']:d} parameters, "
     f"{PR['counts']['literature']:d} take a value stated in a cited source "
     f"and {PR['counts']['assumed']:d} are modelling choices that are swept "
     "across a declared interval rather than defended. The parameter table "
     "in this manuscript is generated from the same registry the code reads, "
     "so it cannot disagree with the values actually used. The five "
     "exposure–response functions were transcribed from open-source "
     "reference implementations and cross-checked against one another before "
     "use."),
    ("p",
     "The model code, the two anchoring datasets and the complete output on "
     "which every table is built are available from the corresponding author "
     "on request."),

    ("h1b", "Conflicts of Interest"),
    ("p", "The authors declare no conflicts of interest."),

    # =====================================================================
    ("h1b", "Appendix A"),
    ("p",
     "Table A1 lists every parameter of the model with the interval over "
     "which the uncertainty analysis varies it and a statement of where its "
     "value came from. Table A2 sets the five exposure–response functions "
     "side by side across the range of wet bulb globe temperature relevant "
     "to European summers. Table A3 reports the observed European "
     "distributions to which the synthetic city and the climate settings are "
     "anchored."),
    ("table", "tableA1"),
    ("table", "tableA2"),
    ("table", "tableA3"),
]

_RAW = (INTRO_BLOCKS + METHOD_BLOCKS + RESULT_BLOCKS + DISCUSSION_BLOCKS
        + BACK_BLOCKS)


def _numbered(blocks):
    """Prefix section headings with their MDPI section numbers.

    The template does not carry list numbering on the heading styles, so the
    numbers are written into the text here, where the order of the blocks is
    the single source of truth for them.
    """
    out, h1, h2 = [], 0, 0
    for b in blocks:
        if b[0] == "h1":
            h1 += 1
            h2 = 0
            out.append(("h1", "%d. %s" % (h1, b[1])))
        elif b[0] == "h2":
            h2 += 1
            out.append(("h2", "%d.%d. %s" % (h1, h2, b[1])))
        else:
            out.append(b)
    return out


BLOCKS = _numbered(_RAW)
