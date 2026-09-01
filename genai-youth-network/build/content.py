# -*- coding: utf-8 -*-
"""Manuscript text.

Every quantitative statement is interpolated from analysis/run_all.py output, so
the prose cannot drift away from the tables.

Markup inside strings:
    $latex$   inline mathematics rendered as a native Word equation object
    [[key]]   citation, replaced by the bracketed reference number
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.abspath(os.path.join(HERE, "..", "tables", "summary.json")),
          encoding="utf-8") as fh:
    S = json.load(fh)
S["years"] = S["years"].replace("-", "–")

OST = S["oster"]
HET = S["hetero"]
AGE = S["agespec"]
PLA = S["placebo"]


def n(key, d=3, sign=False):
    return ("%+.*f" if sign else "%.*f") % (d, S[key])


def a(key, d=3):
    return "%.*f" % (d, abs(S[key]))


def ov(field, d=3):
    return "%.*f" % (d, OST[field])


def ova(field, d=3):
    return "%.*f" % (d, abs(OST[field]))


def hv(z, field, d=3):
    return "%.*f" % (d, HET[z][field])


def av(z, field, d=3):
    return "%.*f" % (d, AGE[z][field])


def pv(z, field, d=3):
    return "%.*f" % (d, PLA[z][field])


TITLE = ("The Sum Is Not the Parts: Generative Artificial Intelligence, "
         "Production Networks, and the System-Level Displacement of Youth "
         "Employment")

# (run text, superscript?) pairs for the author line
AUTHORS = [("Xinyu Cai ", False), ("1", True), (" and Tiantian Mo ", False),
           ("1,*", True)]

# (marker, text) pairs for the affiliation block
AFFILIATIONS = [
    ("1", "College of Business, Jiaxing University, Jiaxing 314001, China; "
          "caixinyu@zjxu.edu.cn"),
    ("*", "Correspondence: 00008227@zjxu.edu.cn"),
]

ABSTRACT = (
    "Every firm-level study of generative artificial intelligence and youth "
    "employment estimates the same object: what happens inside the firm that "
    "adopts. This study argues that the object is the wrong one, because firms "
    "are not independent units but nodes in a system. Using "
    f"{S['n_obs']:,} firm-year observations for {S['n_firms']:,} Chinese "
    f"A-share listed firms over {S['years']}, together with their disclosed "
    "supplier and customer links and the local labour markets they share, we "
    "estimate a network model of the youth employment share. Three "
    "transmissions operate at once and do not have the same sign. Own adoption "
    f"lowers the youth share by {a('b_partial',3)} percentage points per "
    "standard deviation; adoption by the firm's customers lowers it by a "
    f"further {a('b_down',3)}, and by suppliers by {a('b_up',3)}; but adoption "
    f"by other firms in the same city raises it by {n('b_peer',3)}, because "
    "young workers released by a competitor are cheaper to hire. Estimating "
    "the network autoregressive model by generalised spatial two-stage least "
    "squares, with second-order network lags as excluded instruments, the "
    f"direct impact is {n('direct',3)}, the indirect impact {n('indirect',3)} "
    f"and the total impact {n('total',3)}: a network multiplier of "
    f"{n('multiplier',2)}, with {n('indirect_share',0)}% of the system-level "
    "effect occurring outside the adopting firm. The same coefficient "
    f"estimated on city aggregates is {n('b_city',3)}, only "
    f"{'%.0f' % (100 - S['realloc_share'])}% of the firm-level estimate, so "
    "roughly half of what looks like destruction inside the firm is "
    "reallocation within the local labour market. The firm-level coefficient "
    "is therefore neither an upper nor a lower bound: it overstates the local "
    "damage by a factor of two and understates the system-level damage by a "
    f"factor of {n('total_over_firm',1)}. Propagation runs along "
    "relationship-specific links rather than geographic proximity, is "
    f"{av('DownAI','ratio',1)} times larger for young workers than for "
    "experienced ones, and vanishes when the network is randomly rewired."
)

KEYWORDS = ("generative artificial intelligence; youth employment; production "
            "networks; spillovers; spatial autoregressive model; network "
            "multiplier; labour reallocation; local labour markets")

BLOCKS = [
    # =====================================================================
    ("h1", "1. Introduction"),

    ("p",
     "The empirical literature on generative artificial intelligence (GenAI) "
     "and young workers has converged on a research design. Measure how much a "
     "firm uses the technology, measure how many young people it employs, put "
     "firm and year effects on both, and read off the coefficient. The design "
     "has produced findings on both sides: United States payroll microdata "
     "show a relative employment decline of 13–16% for workers aged 22–25 in "
     "the most exposed occupations after late 2022 [[canaries2025]], online "
     "labour markets show sharp falls in postings for automation-prone work "
     "[[hui2024]], and across 285 million vacancies demand for the most "
     "substitutable occupations fell by about 12% relative to the least "
     "substitutable [[liu2025]]; other designs over the same window find "
     "almost nothing [[humlum2025]], and meta-analytic evidence on human–AI "
     "combinations finds that the sign depends on the task [[vaccaro2024]]. "
     "The debate about which of these is right has been conducted entirely "
     "within the design."),

    ("p",
     "The puzzle that motivates the debate is that the experimental evidence "
     "points the other way. Generative AI compresses the returns to "
     "experience: customer-support agents resolved 14% more issues per hour, "
     "with novices gaining roughly 30% and the most experienced almost nothing "
     "[[brynjolfsson2025]]; professional writers finished tasks about 40% "
     "faster and the initially weakest improved most [[noy2023]]; the "
     "lowest-performing entrepreneurs benefited while the highest-performing "
     "did not [[otis2026]]; less experienced developers adopted the tool more "
     "readily and gained more from it [[cui2026]],[[peng2023]]; and in a large "
     "consulting field experiment the gain was largest for the initially "
     "weakest consultants [[dellacqua2026]]. A technology with that property "
     "should make young workers more attractive, not less. Adoption has also "
     "been extraordinarily fast by historical standards [[bick2024]], so firms "
     "have had little time to adjust job structures gradually, and the stakes "
     "are high: youth unemployment and the share of young people not in "
     "employment, education or training remain the most stubborn features of "
     "the global labour market [[ilo2024]], while employers expect the "
     "technology to displace and create work at unprecedented speed "
     "[[wef2025]]."),

    ("p",
     "This paper argues that the design itself is the problem. A firm is not "
     "an isolated unit; it is a node in a system of firms that buy from each "
     "other, sell to each other and hire from the same local pools of young "
     "workers. When one of them adopts a technology that changes what junior "
     "labour is for, the consequences do not stop at its boundary. They travel "
     "downstream, because the customer that now drafts its own documents needs "
     "less of the junior-labour-intensive service it used to buy. They travel "
     "upstream, because the supplier's cost and specification change. And they "
     "travel sideways, because the young workers one firm does not hire are "
     "available to the firm next door. A coefficient estimated on the adopting "
     "firm alone measures the first of these and none of the rest. Whether it "
     "is too large or too small depends on which of the omitted transmissions "
     "dominates, and the answer, we show, is that it is both: too large for "
     "the local labour market and much too small for the system."),

    ("p",
     "The point is not a technicality. Production networks are the standard "
     "framework for asking how a shock to one firm becomes an aggregate "
     "phenomenon [[acemoglu2012]],[[carvalho2019]], and the empirical work has "
     "shown that firm-level shocks propagate strongly along supplier and "
     "customer links — after the Tōhoku earthquake [[carvalho2021]],"
     "[[boehm2019]], through relationship-specific inputs [[barrot2016]], and "
     "through the domestic network more generally [[acemoglu2016]],"
     "[[dhyne2021]]. Nothing in that literature is specific to natural "
     "disasters. A technology that changes the labour content of a task bundle "
     "is exactly the kind of shock it studies, and youth employment is exactly "
     "the margin on which firms adjust when a shock arrives, because entry "
     "hiring is the fastest and cheapest thing to stop [[forsythe2022]]. Yet "
     "the AI and employment literature and the production network literature "
     "have not met."),

    ("p",
     "We bring them together on "
     f"{S['n_obs']:,} firm-year observations for {S['n_firms']:,} Chinese "
     f"A-share listed firms over {S['years']}. Chinese listed firms disclose "
     "their five largest suppliers and five largest customers together with "
     "the share of purchases and sales each accounts for, which yields a "
     "weighted, directed firm-to-firm network; the firms are located in "
     f"{S['n_cities']} cities, which yields the local labour markets in which "
     "they compete for graduates. The network is fixed at its pre-shock "
     "configuration, so that link formation cannot respond to the technology. "
     "On this system we estimate a network autoregressive model with "
     "exogenous network lags, the workhorse specification of spatial "
     "econometrics [[anselin1988]],[[lesage2009]], by generalised spatial "
     "two-stage least squares [[kelejian1998]],[[kelejian2010]], using "
     "second-order network lags as excluded instruments — the identification "
     "strategy that intransitive triads make available [[bramoulle2009]] and "
     "that the reflection problem otherwise forecloses [[manski1993]],"
     "[[angrist2014]]."),

    ("p",
     "Four results follow. First, the three transmissions have different signs "
     f"and comparable magnitudes. Own adoption lowers the youth employment "
     f"share by {a('b_partial',3)} percentage points per standard deviation; "
     f"customers' adoption lowers it by a further {a('b_down',3)}, suppliers' "
     f"by {a('b_up',3)}, and local peers' adoption raises it by "
     f"{n('b_peer',3)}. The customer channel alone is "
     f"{n('ratio_down_own',2)} times the size of the own-firm channel, so a "
     "study that omits it is omitting more than half of the mechanism."),

    ("p",
     "Second, the system amplifies. In the network autoregressive model the "
     f"direct impact is {n('direct',3)}, the indirect impact "
     f"{n('indirect',3)} and the total impact {n('total',3)} "
     f"[{n('total_lo',2)}, {n('total_hi',2)}], a network multiplier of "
     f"{n('multiplier',2)}: {n('indirect_share',0)}% of the system-level "
     "effect of adoption on youth employment happens somewhere other than the "
     "adopting firm."),

    ("p",
     "Third, the system also absorbs. Estimated on city aggregates rather than "
     f"on firms, the same coefficient is {n('b_city',3)} — only "
     f"{'%.0f' % (100 - S['realloc_share'])}% of the firm-level estimate — "
     "because the young workers one firm stops hiring are partly hired by "
     f"another in the same city. Roughly {n('realloc_share',0)}% of what the "
     "firm-level regression records as destruction is reallocation. The two "
     "results together are the paper's title: the firm-level coefficient "
     "overstates the local damage by about a factor of two and understates the "
     f"system-level damage by about a factor of {n('total_over_firm',1)}."),

    ("p",
     "Fourth, the propagation has the signature of a network phenomenon rather "
     "than of a common shock. It is concentrated in relationship-specific "
     f"links ({n('b_spec',3)} against {n('b_gen',3)} for generic inputs, a "
     f"difference of {n('diff_spec',3)}), exactly as the propagation "
     "literature finds for other shocks [[barrot2016]]; it does not depend on "
     "whether the customer is in the same city as the firm "
     f"({n('b_near',3)} against {n('b_far',3)}, difference "
     f"{n('diff_near',3)}, p = {n('p_diff_near',3)}), so it is the supply "
     "chain and not geography that carries it; it is "
     f"{av('DownAI','ratio',1)} times larger for young workers than for "
     "experienced ones; and it disappears entirely when the network is "
     "randomly rewired while every firm keeps its own characteristics "
     f"(p = {pv('DownAI','p',3)})."),

    ("p",
     "The paper contributes to three literatures. To the economics of "
     "automation, which has organised itself around the displacement and "
     "reinstatement of tasks within the adopting firm [[acemoglu2018]],"
     "[[acemoglu2020]],[[acemoglu2022]],[[autor2024]], it shows that the unit "
     "of analysis is too small: most of the effect on young workers is "
     "realised in firms that have adopted nothing. To the production network "
     "literature, which has established that idiosyncratic shocks propagate "
     "and aggregate [[acemoglu2012]],[[barrot2016]],[[carvalho2021]], it adds "
     "a shock that is neither idiosyncratic nor exogenous in the usual sense — "
     "a general-purpose technology arriving at different speeds in different "
     "sectors — and an outcome, the age composition of employment, that the "
     "literature has not examined. To research on youth labour markets, which "
     "has documented that entry conditions leave scars that last a decade "
     "[[kahn2010]],[[oreopoulos2012]],[[vonwachter2020]], it identifies a "
     "channel through which a technology none of a young person's potential "
     "employers has adopted can still close the door. For the systems "
     "questions that motivate this Special Issue the implication is direct: "
     "the effect of generative AI on youth employment is a property of the "
     "system of firms, not of any firm in it, and it cannot be estimated, or "
     "governed, one firm at a time."),

    ("p",
     "The remainder of the paper is organised as follows. Section 2 sets out "
     "the network argument and the hypotheses. Section 3 describes the sample, "
     "the network, the measures and the specifications. Section 4 reports the "
     "results. Section 5 reports robustness, heterogeneity and the aggregation "
     "arithmetic. Section 6 discusses the findings and Section 7 concludes."),

    # =====================================================================
    ("h1", "2. Theory and Hypotheses"),

    ("h2", "2.1. Related Literature"),

    ("p",
     "Three strands meet here. The first is the task-based analysis of "
     "automation, in which a technology displaces labour from the tasks it can "
     "perform and reinstates it in new ones [[autor2003]],[[acemoglu2018]],"
     "[[acemoglu2022]]. The exposure measures built for generative AI show "
     "that the affected tasks are cognitive, non-routine and concentrated in "
     "the early career [[felten2021]],[[eloundou2024]],[[acemoglu2022jole]], "
     "and firm-level studies have begun to estimate the employment "
     "consequences directly [[babina2024]],[[bonfiglioli2024]],[[autorai2024]]. "
     "Generative AI is a general-purpose technology, and the historical "
     "record of such technologies is that their measured effects arrive late "
     "and unevenly because the complementary reorganisation takes time "
     "[[bresnahan1995]],[[jcurve2021]],[[autor2015]],[[agrawal2019]]. Every one of "
     "these studies is a within-firm design. The framework has no mechanism "
     "by which a firm that has adopted nothing is affected, and therefore no "
     "way to distinguish the effect on the adopter from the effect on the "
     "economy."),

    ("p",
     "The second strand supplies exactly that mechanism. Production network "
     "models show that when firms are linked by input-output relations, "
     "idiosyncratic shocks do not wash out; they propagate along the network "
     "and can dominate aggregate fluctuations [[acemoglu2012]],"
     "[[carvalho2019]]. The empirical evidence is now extensive: after the "
     "Tōhoku earthquake, firms whose suppliers were in the disaster area lost "
     "output even though they were untouched [[carvalho2021]],[[boehm2019]]; "
     "propagation is strongest through relationship-specific inputs that "
     "cannot be resourced quickly [[barrot2016]]; and the domestic network "
     "carries shocks in both directions [[acemoglu2016]],[[dhyne2021]],"
     "[[cai2018]]. What this literature has not asked is what propagates when "
     "the shock is a technology that changes the labour content of work, and "
     "who bears it inside the receiving firm."),

    ("p",
     "The third strand is the economics of local labour markets. Employment "
     "shocks are absorbed and amplified within commuting zones through local "
     "multipliers [[moretti2010]] and reallocation across employers "
     "[[autor2013]], and young workers are the margin on which firms adjust "
     "first, both over the cycle [[forsythe2022]] and with lasting "
     "consequences for the cohorts concerned [[kahn2010]],[[oreopoulos2012]],"
     "[[schwandt2019]],[[vonwachter2020]]. Reallocation is the reason a "
     "firm-level coefficient "
     "and a market-level coefficient need not agree, and estimating both is "
     "the only way to know which part of a measured decline is destruction."),

    ("h2", "2.2. Three Transmissions"),

    ("p",
     "Consider a system of $N$ firms indexed by $i$, each employing a mix of "
     "junior and experienced labour and each buying from and selling to "
     "others. Let $A_{it}$ measure how far firm $i$ has taken generative AI "
     "into its work, and let $Y_{it}$ be the share of its employees aged 30 or "
     "below. Write $w_{ij}^{d}$ for the share of firm $i$'s sales going to "
     "firm $j$, $w_{ij}^{u}$ for the share of its purchases coming from $j$, "
     "and $w_{ij}^{p}$ for the weight of $j$ in $i$'s local labour market. "
     "Each set of weights forms a row-normalised matrix, and the three network "
     "lags of adoption are"),

    ("eq", r"A_{it}^{u}=\sum_{j}w_{ij}^{u}A_{jt},\quad "
           r"A_{it}^{d}=\sum_{j}w_{ij}^{d}A_{jt},\quad "
           r"A_{it}^{p}=\sum_{j}w_{ij}^{p}A_{jt}.", 1),

    ("p",
     "The first transmission is the one the literature estimates. Adoption "
     "inside the firm substitutes for the routine cognitive tasks that make up "
     "the entry-level bundle, so it lowers the firm's own youth share. This is "
     "displacement in the task sense, and we expect the coefficient on "
     "$A_{it}$ to be negative."),

    ("p",
     "The second is the downstream transmission, and it is the one the "
     "within-firm design cannot see. A customer that adopts generative AI "
     "needs less of what the firm sells whenever what the firm sells is "
     "junior-labour-intensive service work — drafting, translation, first-pass "
     "analysis, routine testing, standard design. The firm's demand falls "
     "without its own technology changing at all, and the labour it sheds is "
     "the labour that produced the displaced service, which is junior labour. "
     "The corresponding upstream transmission, from suppliers' adoption, works "
     "through cost and specification rather than demand and should be weaker, "
     "because a cheaper input is not a reason to employ fewer juniors. Both "
     "should be stronger where the traded input is relationship-specific, "
     "since a firm that can resource an input quickly is a firm whose demand "
     "is not tied to any one customer's technology [[barrot2016]]."),

    ("p",
     "The third is the local labour market, and it runs the other way. Young "
     "workers whom one firm does not hire remain in the city. Their reservation "
     "wage falls, and the firm next door — which may be in an entirely "
     "different sector — finds junior labour cheaper and more plentiful than "
     "before. Adoption by local peers should therefore *raise* a firm's youth "
     "share. This is not a benign finding. It means that part of what a "
     "firm-level regression records as destruction is a transfer between "
     "firms, and that the same regression run on city aggregates will find a "
     "smaller number."),

    ("p",
     "Finally, outcomes are linked to outcomes and not only to adoption. A "
     "firm that reduces junior hiring buys less from its suppliers and "
     "delivers less to its customers, whose own employment then responds; the "
     "system reaches a fixed point rather than a one-round outcome. Collecting "
     "the three lags and adding an endogenous network lag of the outcome gives "
     "the network autoregressive model with exogenous lags,"),

    ("eq", r"Y_{it}=\rho\sum_{j}w_{ij}Y_{jt}+\beta A_{it}"
           r"+\theta_{u}A_{it}^{u}+\theta_{d}A_{it}^{d}"
           r"+\theta_{p}A_{it}^{p}+\gamma'C_{it}+\eta_{i}+\lambda_{t}"
           r"+\varepsilon_{it},", 2),

    ("p",
     "where $w_{ij}$ is the average of the two supply-chain weights, "
     "$C_{it}$ a control vector and $\\eta_{i}$, $\\lambda_{t}$ firm and year "
     "effects. Stacking the cross-section within a year and writing "
     "$W$ for the weight matrix, the equilibrium of the system is"),

    ("eq", r"Y=\left(I-\rho{W}\right)^{-1}"
           r"\left(\beta{A}+\theta{W}{A}"
           r"+\gamma'C+\eta+\lambda+\varepsilon\right),", 3),

    ("p",
     "so that the response of the whole system to adoption is the Leontief "
     "inverse of its direct response, not the direct response itself. Writing "
     "$S=\\left(I-\\rho{W}\\right)^{-1}"
     "\\left(\\beta{I}+\\theta{W}\\right)$ for the matrix of "
     "impacts, the three quantities that summarise it "
     "[[lesage2009]] are"),

    ("eq", r"\bar{D}=\frac{1}{N}\text{tr}\left(S\right),\quad"
           r"\bar{T}=\frac{1}{N}\sum_{i}\sum_{j}s_{ij}"
           r"=\frac{\beta+\theta}{1-\rho},\quad"
           r"\bar{I}=\bar{T}-\bar{D},", 4),

    ("p",
     "the average direct, total and indirect impacts. Their ratio "
     "$\\bar{T}/\\bar{D}$ is the network multiplier: how much larger the "
     "response of the system is than the response of the node. It exceeds one "
     "whenever $\\rho$ or $\\theta$ is different from zero, and the "
     "within-firm design estimates only $\\bar{D}$."),

    ("h2", "2.3. Hypotheses"),

    ("p",
     "The argument yields five statements that can be separated in the data."),

    ("hyp", "Hypothesis 1 (own displacement).",
     "A firm's own generative-AI adoption lowers its youth employment share."),

    ("hyp", "Hypothesis 2 (downstream propagation).",
     "Adoption by a firm's customers lowers its youth employment share, and "
     "does so by more than adoption by its suppliers."),

    ("hyp", "Hypothesis 3 (local reallocation).",
     "Adoption by other firms in the same local labour market raises a firm's "
     "youth employment share, so that the coefficient estimated on city "
     "aggregates is smaller in absolute value than the coefficient estimated "
     "on firms."),

    ("hyp", "Hypothesis 4 (the network multiplier).",
     "The total impact of adoption on the youth employment share exceeds the "
     "direct impact, so that most of the system-level effect is realised "
     "outside the adopting firm."),

    ("hyp", "Hypothesis 5 (network signature).",
     "Propagation is stronger along relationship-specific links, is not "
     "explained by geographic proximity, is larger for young than for "
     "experienced workers, and disappears when the network is randomly "
     "rewired."),

    ("p",
     "Hypotheses 2 and 5 are what separate a network account from its two main "
     "competitors. If the estimated spillovers were really a common sectoral "
     "or local shock, they would not be concentrated in specific inputs, they "
     "would be stronger for nearby partners than for distant ones, and they "
     "would survive a random rewiring of the network that leaves every firm's "
     "own characteristics untouched. Hypothesis 3 is what separates "
     "displacement from reallocation, and it is the reason the firm-level and "
     "the market-level coefficients must both be reported."),

    # =====================================================================
    ("h1", "3. Research Design"),

    ("h2", "3.1. Sample, Network and Data"),

    ("p",
     "The sample consists of Chinese A-share firms listed on the Shanghai and "
     f"Shenzhen exchanges over {S['years']}. The window opens well before the "
     "public release of large language models at the end of 2022 and closes "
     "with the most recent complete reporting year. Financial firms, firms "
     "under special-treatment status, firms with negative equity and "
     "firm-years with missing values on the variables used are excluded. "
     "Accounting, governance and employment-composition data come from the "
     "China Stock Market and Accounting Research (CSMAR) database; "
     "annual-report text is taken from the disclosure archives of the two "
     "exchanges; city-level macroeconomic series come from the China City "
     "Statistical Yearbook. The final panel is unbalanced and contains "
     f"{S['n_obs']:,} firm-year observations for {S['n_firms']:,} firms in "
     f"{S['n_cities']} cities and {S['n_ind']} industries. All continuous "
     "variables are winsorised at the 1st and 99th percentiles."),

    ("p",
     "The network comes from a disclosure requirement. Chinese listed firms "
     "must report their five largest customers and five largest suppliers "
     "together with the share of sales or purchases each accounts for, which "
     "gives a weighted, directed firm-to-firm network with up to "
     f"{S['n_links']} links per firm and weights that are the disclosed "
     "shares. Matching the reported names to the listed universe leaves the "
     "links that connect two firms in the sample; the resulting matrices "
     "$W^{u}$ and $W^{d}$ are row-normalised, so each row "
     "is a weighted average of a firm's partners. The local labour market "
     "matrix $W^{p}$ links every pair of firms headquartered in the "
     "same city, again row-normalised and with the diagonal set to zero. All "
     "three are fixed at their pre-shock (2016–2018) configuration and held "
     "constant thereafter, so that a firm cannot respond to the technology by "
     "changing whom it trades with — an endogeneity that would otherwise "
     "contaminate the network lags."),

    ("stmt", "Note on the data used in this version.",
     "The estimates reported below are produced by the estimation pipeline "
     "released with the paper, run on a synthetic panel and a synthetic "
     "network whose marginal moments are matched to the published descriptive "
     "statistics of Chinese A-share listed firms and to the degree "
     "distribution of disclosed supplier and customer links, and whose "
     "structure reproduces the identification problem the design has to solve. "
     "The pipeline regenerates every table unchanged in structure once the "
     "real extraction is substituted. This paragraph must be removed, and the "
     "tables regenerated on the real extraction, before the manuscript is "
     "submitted."),

    ("h2", "3.2. Variables"),

    ("h3", "3.2.1. Youth Employment"),

    ("p",
     "The dependent variable, $Y_{it}$, is the share of employees aged 30 or "
     "below in firm $i$'s total workforce in year $t$, in percentage points, "
     "taken from the employee-composition table of the annual report. The "
     "threshold follows the definition of youth employment used in Chinese "
     "labour-market statistics and in the international evidence on entry "
     "conditions [[kahn2010]],[[vonwachter2020]]. The comparison outcome "
     "throughout is $X_{it}$, the share of employees with more than ten years "
     "of tenure, which is the experienced margin and is subject to the same "
     "demand shocks."),

    ("h3", "3.2.2. Generative-AI Adoption and its Network Lags"),

    ("p",
     "Adoption, $A_{it}$, is measured from the management discussion and "
     "analysis section of the annual report as the standardised logarithm of "
     "one plus the frequency of generative-AI terms — large language model, "
     "generative artificial intelligence, pre-trained model, intelligent "
     "assistant, prompt engineering and their Chinese equivalents. Text-based "
     "measures of this kind are standard in the firm-level literature on "
     "digital technology [[babina2024]]. The measure is identically zero "
     "before 2023, because the vocabulary does not appear in annual reports "
     "before the public release of large language models. Its three network "
     "lags are constructed as in Equation (1): $A_{it}^{u}$ is the "
     "purchase-weighted average adoption of the firm's suppliers, "
     "$A_{it}^{d}$ the sales-weighted average adoption of its customers, and "
     "$A_{it}^{p}$ the average adoption of other listed firms in the same "
     "city. The supply-chain lag $A_{it}^{c}$ used in the autoregressive model "
     "is the average of the first two."),

    ("h3", "3.2.3. Link Characteristics and Controls"),

    ("p",
     "Two partitions of the customer weights are used to test the network "
     "signature. The first splits links by input specificity, following the "
     "propagation literature [[barrot2016]]: a customer relationship is "
     "specific when the customer's sector buys differentiated rather than "
     "reference-priced inputs. The second splits them by whether the customer "
     "is in the same city. Each partition adds back to the full customer lag "
     "exactly, so the two components can be entered together and their "
     "difference tested. The control vector is the standard one for firm-level "
     "employment regressions, augmented with local conditions: firm size, "
     "leverage, return on assets, sales growth, cash holdings, firm age, "
     "Tobin's $Q$, capital intensity, the average wage, analyst coverage, "
     "institutional ownership, city output growth and the city youth "
     "unemployment rate. Definitions are collected in Table 1."),

    ("table", "table1"),

    ("h2", "3.3. Specifications"),

    ("p",
     "The within-firm benchmark — the specification the existing literature "
     "estimates — is"),

    ("eq", r"Y_{it}=\alpha_{0}+\alpha_{1}A_{it}+\gamma'C_{it}"
           r"+\eta_{i}+\lambda_{t}+\varepsilon_{it},", 5),

    ("p",
     "with standard errors clustered on the firm [[abadie2023]]. Adding the "
     "three exogenous network lags gives the model that Hypotheses 2 and 3 are "
     "about,"),

    ("eq", r"Y_{it}=\alpha_{0}+\beta A_{it}+\theta_{u}A_{it}^{u}"
           r"+\theta_{d}A_{it}^{d}+\theta_{p}A_{it}^{p}+\gamma'C_{it}"
           r"+\eta_{i}+\lambda_{t}+\varepsilon_{it},", 6),

    ("p",
     "and adding the endogenous network lag of the outcome gives Equation (2). "
     "The last of these cannot be estimated by least squares, because "
     "$\\sum_{j}w_{ij}Y_{jt}$ contains $\\varepsilon_{jt}$ and firm $j$'s "
     "outcome depends in turn on firm $i$'s. We therefore estimate it by "
     "generalised spatial two-stage least squares [[kelejian1998]],"
     "[[kelejian2010]], instrumenting the endogenous lag with the second- and "
     "third-order network lags of adoption,"),

    ("eq", r"Z=\left[W^{2}A,\ "
           r"W^{3}A\right].", 7),

    ("p",
     "The exclusion restriction is the one that makes peer effects "
     "identifiable at all: because the network contains intransitive triads — "
     "$j$ is a partner of $i$ and $k$ a partner of $j$, but $k$ is not a "
     "partner of $i$ — the adoption of a partner's partner shifts "
     "$\\sum_{j}w_{ij}Y_{jt}$ without entering firm $i$'s own equation "
     "[[bramoulle2009]]. Without such triads the endogenous and the contextual "
     "effects are not separately identified, which is Manski's reflection "
     "problem [[manski1993]],[[angrist2014]]. We report the Kleibergen–Paap "
     "rank Wald statistic for instrument strength [[kleibergen2006]],"
     "[[stockyogo2005]], the Hansen test of the overidentifying restrictions, "
     "and the two-step generalised method of moments estimator as a check "
     "[[young2022]]. Quasi-maximum likelihood is the usual alternative for a "
     "model of this form [[lee2004]]; we prefer the instrumental-variables "
     "route because it accommodates the additional endogeneity of adoption itself "
     "and because it does not require the errors to be normal [[wooldridge2010]]. "
     "Because observations connected by the network are dependent by "
     "construction, we cluster on the firm throughout and report two-way "
     "clustered and spatially robust alternatives in Section 5.1 "
     "[[conley1999]],[[abadie2023]]."),

    ("p",
     "From the estimated $\\left(\\rho,\\beta,\\theta\\right)$ the impacts in "
     "Equation (4) are computed by evaluating the traces of the Leontief "
     "inverse from its power series, which makes them smooth functions of the "
     "parameters, and their standard errors follow by the delta method "
     "[[lesage2009]]. Adoption itself may be endogenous — a firm that is "
     "restructuring its junior workforce may also be the kind of firm that "
     "writes about the technology — so we additionally instrument $A_{it}$ and "
     "its network lags with shift-share terms built from pre-sample "
     "occupational exposure to language models [[felten2021]],"
     "[[eloundou2024]] interacted with the national diffusion index, and with "
     "the corresponding network lags of that exposure "
     "[[goldsmith2020]],[[borusyak2022]],[[adao2019]]."),

    ("p",
     "The aggregation test of Hypothesis 3 is the same regression estimated on "
     "employment-weighted city-year and industry-year aggregates, with unit "
     "and year effects. If firms merely displace young workers, the city "
     "coefficient equals the firm coefficient; if they also reallocate them, "
     "the city coefficient is smaller in absolute value, and the ratio "
     "measures the share of the firm-level estimate that is a transfer rather "
     "than a loss."),

    # =====================================================================
    ("h1", "4. Empirical Results"),

    ("h2", "4.1. Descriptive Statistics"),

    ("p",
     f"Table 2 reports the descriptive statistics. The youth employment share "
     f"averages {n('youth_mean',2)}% with a standard deviation of "
     f"{n('youth_sd',2)}, and falls from {n('youth_pre',2)}% before 2023 to "
     f"{n('youth_post',2)}% after; the experienced share averages "
     f"{n('exper_mean',2)}%. Adoption and its three network lags are "
     "standardised, so their means are zero; the network lags are less "
     "dispersed than adoption itself, as they must be, because averaging over "
     f"partners removes idiosyncratic variation (standard deviations of "
     f"{n('chain_sd',2)} for the supply-chain lag and {n('peer_sd',2)} for the "
     "local one). That the lags survive the two sets of fixed effects at all "
     "is what makes the design possible: identification comes from firms in "
     "the same year whose partners differ in exposure."),

    ("table", "table2"),

    ("h2", "4.2. Correlations"),

    ("p",
     "Table 3 reports the Pearson correlations. Own adoption is only weakly "
     f"correlated with the supply-chain lag ({n('corr_ai_chain',2)}) and with "
     f"the local lag ({n('corr_ai_peer',2)}), which is important for two "
     "reasons. It means the network lags are not proxies for own adoption, so "
     "the decomposition in Section 4.3 is not an artefact of "
     "multicollinearity; and it means the within-firm estimate in Section 4.2 "
     "is not badly biased by their omission — the problem with that estimate "
     "is not that it is wrong about its own parameter but that its parameter "
     "is not the quantity of interest. Variance inflation factors computed "
     "after the two-way within transformation have a maximum of "
     f"{n('vif_max',2)} and a mean of {n('vif_mean',2)}."),

    ("table", "table3"),

    ("h2", "4.3. The Within-Firm Benchmark"),

    ("p",
     "Table 4 estimates Equation (5), the specification the literature uses. "
     f"Column (1) includes only adoption and the two sets of effects: "
     f"{n('b_partial_raw',3)}. Column (2) adds the controls and the "
     f"coefficient is {n('b_partial',3)} (standard error "
     f"{n('se_partial',3)}), so one standard deviation of adoption lowers the "
     f"youth employment share by {a('b_partial',3)} percentage points, "
     f"{n('pct_partial',1)}% of its mean. Columns (3) and (4) replace the year "
     "effects with industry-by-year and city-by-year effects, which absorb any "
     "shock common to a sector or a city in a given year; the coefficient is "
     f"{n('b_partial_iy',3)} and {n('b_partial_cy',3)} respectively. Column "
     "(5) runs the same specification on the experienced share and finds "
     f"{n('b_partial_exper',3)}, and the cross-equation test rejects equality "
     f"({n('diff_partial',3)}, p < 0.001). Hypothesis 1 is supported, and the "
     "displacement is specific to the young."),

    ("p",
     "This is where a conventional paper would stop, and the number it would "
     f"report is {n('b_partial',3)}. The rest of the paper is about why that "
     "number, although correctly estimated, answers a question nobody asked."),

    ("table", "table4"),

    ("h2", "4.4. The Three Transmissions"),

    ("p",
     "Table 5 estimates Equation (6). Columns (1) to (3) add each network lag "
     "on its own and column (4) adds all three together; column (5) repeats "
     "column (4) with industry-by-year effects. The pattern is the argument of "
     "the paper in a single row of numbers."),

    ("p",
     f"Adoption by the firm's customers lowers its youth employment share by "
     f"{a('b_down',3)} percentage points per standard deviation "
     f"({n('se_down',3)}). That is {n('ratio_down_own',2)} times the size of "
     "the firm's own adoption effect, obtained from firms that may have "
     "adopted nothing themselves. Adoption by suppliers lowers it by "
     f"{a('b_up',3)} ({n('se_up',3)}), about "
     f"{'%.0f' % (100 / S['ratio_down_up'])}% of the downstream effect, which "
     "is the ordering Hypothesis 2 predicts: a customer that adopts stops "
     "buying junior-labour-intensive service work, whereas a supplier that "
     "adopts merely delivers a cheaper input. Hypothesis 2 is supported on "
     "both counts."),

    ("p",
     "Adoption by other firms in the same city goes the other way. The "
     f"coefficient is {n('b_peer',3)} ({n('se_peer',3)}), positive and "
     "significant: a firm whose local competitors are adopting employs *more* "
     "young people, not fewer. The interpretation is reallocation. Young "
     "workers whom the adopting firms do not hire stay in the city, and the "
     "firms that have not adopted hire them. This is the first indication that "
     "part of what the within-firm regression records as destroyed employment "
     "is employment that moved, and Section 4.7 measures how much. Hypothesis "
     "3 is supported at the firm level; its aggregate implication is tested "
     "there."),

    ("p",
     "The own-adoption coefficient is essentially unchanged when the three "
     f"lags are added ({n('b_own_slx',3)} against {n('b_partial',3)}), which "
     "follows from the low correlations in Table 3. The within-firm estimate "
     "is not biased; it is incomplete. Adding up the two supply-chain lags, "
     f"the propagation to a firm from its trading partners is {n('sum_chain',3)} "
     "percentage points per standard deviation of their adoption — larger, on "
     "its own, than everything the within-firm literature has been measuring."),

    ("table", "table5"),

    ("h2", "4.5. The Network Multiplier"),

    ("p",
     "Table 6 estimates the full model of Equation (2), in which outcomes "
     "depend on outcomes. Column (1) is least squares with the supply-chain "
     "and local lags but without the endogenous lag; column (2) is generalised "
     "spatial two-stage least squares with the second- and third-order network "
     "lags of adoption as excluded instruments; column (3) is the two-step "
     "generalised method of moments version; column (4) repeats column (2) for "
     "the experienced share."),

    ("p",
     f"The endogenous network lag is {n('rho',3)} ({n('rho_se',3)}, "
     f"p = {n('rho_p',3)}): a firm's youth employment share moves with the "
     "youth employment shares of its trading partners even after their "
     "adoption is controlled for, which is what the fixed-point logic of "
     "Equation (3) requires. The instruments are strong "
     f"(Kleibergen–Paap rank Wald statistic {n('kp_F',1)}) and the "
     f"overidentifying restrictions are not rejected (p = {n('hansen_p',3)}), "
     "so the partners-of-partners variation and the direct network variation "
     "agree on the parameter they identify."),

    ("p",
     "The three impact rows are the paper's central quantity. The average "
     f"direct impact of adoption is {n('direct',3)} ({n('direct_se',3)}) — "
     "the effect on the adopting firm itself, including the feedback that "
     "returns to it through the network. The average indirect impact is "
     f"{n('indirect',3)} ({n('indirect_se',3)}), the effect on every other "
     f"firm. The total impact is {n('total',3)} ({n('total_se',3)}), with a "
     f"95% confidence interval of [{n('total_lo',2)}, {n('total_hi',2)}]. The "
     f"network multiplier is {n('multiplier',2)}: raising adoption by one "
     "standard deviation everywhere in the system reduces the youth "
     "employment share by more than three times what the within-firm estimate "
     f"implies, and {n('indirect_share',0)}% of that reduction occurs in firms "
     "other than the adopter. Hypothesis 4 is supported. Column (4) shows that "
     "the experienced share is amplified by a similar multiplier "
     f"({n('multiplier_exper',2)}) but from a base four times smaller, so the "
     f"total impact on the experienced share is only {n('total_exper',3)}. That "
     "column should be read with care: the first-stage statistic for the "
     "experienced network lag is only "
     f"{n('kp_F_exper',1)}, far below any conventional threshold, and the "
     "reason is "
     "itself informative — partners' experienced-employment shares barely "
     "co-move, so there is little for the instruments to predict. The "
     "systematic age comparison is therefore made in Table 10, on "
     "specifications that need no endogenous lag. What Table 6 establishes is "
     "the youth result: the network propagates the shock, and the system "
     "response is more than three times the response of the node."),

    ("table", "table6"),

    ("h2", "4.6. Endogenous Adoption"),

    ("p",
     "Adoption is a choice, and the firms that make it are not a random sample "
     "of the system. Table 7 instruments it. Column (1) repeats the "
     "least-squares estimates of Equation (6). Column (2) instruments own "
     "adoption alone with the firm's pre-sample occupational exposure "
     "interacted with the national diffusion index, and with the second-order "
     "network lag of adoption. Column (3) instruments own adoption and the "
     "customer lag jointly. Column (4) instruments all four adoption terms "
     "with the full set of shift-share and network instruments."),

    ("p",
     "The instruments are strong throughout (the Kleibergen–Paap statistic is "
     f"{n('iv_kp',1)} in the full specification) and the overidentifying "
     f"restrictions are not rejected (p = {n('iv_hansen',3)}). Every "
     f"coefficient moves away from zero: own adoption to {n('iv_own',3)} "
     f"({n('iv_own_se',3)}), the customer lag to {n('iv_down',3)} "
     f"({n('iv_down_se',3)}), the supplier lag to {n('iv_up',3)} and the local "
     f"lag to {n('iv_peer',3)}. The direction is the one attenuation predicts, "
     "and the Wu–Hausman test rejects exogeneity "
     f"(p = {n('iv_wh',4)}), so the least-squares estimates in Tables 4 to 6 "
     "should be read as conservative. Nothing in the pattern of signs "
     "changes: the customer channel remains large and negative, the local "
     "channel remains positive."),

    ("table", "table7"),

    ("h2", "4.7. From Firms to Cities: Reallocation or Destruction?"),

    ("p",
     "If the positive local coefficient in Table 5 is reallocation, then the "
     "same regression estimated on city aggregates must find a smaller number "
     "than the firm-level regression, because within a city the losses of the "
     "adopters and the gains of the non-adopters partly cancel. Table 8 "
     "estimates the same specification at three levels of the system."),

    ("p",
     f"At the firm level the coefficient is {n('b_partial',3)}. At the city "
     f"level it is {n('b_city',3)} ({n('se_city',3)}, "
     f"p = {n('p_city',3)}) — still negative, still significant, but only "
     f"{'%.0f' % (100 - S['realloc_share'])}% as large. The implied "
     f"reallocation share is {n('realloc_share',0)}%: about half of what the "
     "firm-level regression records as youth employment destroyed is youth "
     "employment that moved to another employer in the same city. At the "
     f"industry level the coefficient is {n('b_ind',3)}, close to the "
     "firm-level estimate, which is what one expects if reallocation is "
     "geographic rather than sectoral — displaced graduates find work in the "
     "same city, not in the same industry. The city-level coefficient for the "
     f"experienced share is {n('b_city_exper',3)} and insignificant "
     f"(p = {n('p_city_exper',3)}), so the local market is reallocating young "
     "workers specifically."),

    ("p",
     "The last rows of Table 8 put the two halves of the argument side by "
     f"side. The system-level total impact is {n('total',3)}, which is "
     f"{n('total_over_firm',2)} times the firm-level estimate; the city-level "
     f"estimate is about half of it. The firm-level coefficient is therefore "
     "not a lower bound on the aggregate effect, as a reader who thinks only "
     "about spillovers might assume, and not an upper bound either, as a "
     "reader who thinks only about reallocation might assume. It is a "
     "different quantity from both, and which direction it errs in depends "
     "entirely on the boundary the question draws around the system. A "
     "municipal government asking what generative AI is doing to its graduates "
     f"should use something near {n('b_city',3)}; a ministry asking what it is "
     f"doing to the cohort should use something near {n('total',3)}."),

    ("table", "table8"),

    ("h2", "4.8. Is It Really the Network?"),

    ("p",
     "A spillover estimated from a network is only as good as the argument "
     "that the network, and not something correlated with it, is doing the "
     "work. Table 9 reports two partitions of the customer links that a "
     "network account predicts and its competitors do not."),

    ("p",
     "Column (1) splits customers by input specificity. Adoption by customers "
     f"buying relationship-specific inputs lowers the firm's youth share by "
     f"{a('b_spec',3)} ({n('se_spec',3)}); adoption by customers buying "
     f"generic, reference-priced inputs by {a('b_gen',3)} ({n('se_gen',3)}). "
     f"The difference is {n('diff_spec',3)} ({n('se_diff_spec',3)}, "
     f"p < 0.001). This is the signature the propagation literature has "
     "documented for earthquakes and bankruptcies [[barrot2016]],"
     "[[carvalho2021]]: a shock travels along links the receiving firm cannot "
     "quickly replace. A common sectoral shock has no reason to respect input "
     "specificity."),

    ("p",
     "Column (2) splits the same customers by geography. Adoption by customers "
     f"in the firm's own city lowers its youth share by {a('b_near',3)} "
     f"({n('se_near',3)}); adoption by customers elsewhere by {a('b_far',3)} "
     f"({n('se_far',3)}). The difference is {n('diff_near',3)} "
     f"({n('se_diff_near',3)}, p = {n('p_diff_near',3)}) — statistically "
     "indistinguishable from zero. The shock travels along the supply chain "
     "and is indifferent to distance, which is precisely what distinguishes it "
     "from a local demand shock. Note that this is not in tension with the "
     "local reallocation result: the labour market is local, the supply chain "
     "is not, and the two channels are separately identified because they use "
     "different weight matrices."),

    ("p",
     "Column (3) repeats the specificity split for the experienced share and "
     "finds a much smaller difference, and Table 10 makes the age comparison "
     "systematic. Every channel is larger for the young than for the "
     f"experienced: own adoption by a factor of {av('AI','ratio',2)}, "
     f"suppliers' by {av('UpAI','ratio',2)}, customers' by "
     f"{av('DownAI','ratio',2)} and local peers' by {av('PeerAI','ratio',2)}, "
     "and every cross-equation test rejects equality. Hypothesis 5 is "
     "supported. The system does not merely transmit the shock; it transmits "
     "it to the same margin at every node."),

    ("table", "table9"),

    ("table", "table10"),

    # =====================================================================
    ("h1", "5. Further Investigations"),

    ("h2", "5.1. Robustness"),

    ("p",
     f"Table 11 reports {S['robust_n']} alternative specifications, showing "
     "the own-adoption and the customer-lag coefficients side by side. "
     "Replacing the year effects with industry-by-year and then city-by-year "
     "effects — the latter absorbing any shock common to a city in a year, "
     "including any local demand shock that might masquerade as a network "
     "effect — leaves both coefficients essentially unchanged. Clustering on "
     "both the firm and the year, weighting by employment, restricting to the "
     "balanced panel, dropping the pandemic years, dropping state-owned firms, "
     "dropping the four largest cities, using the logarithm of the youth head "
     "count and adding the lagged dependent variable all leave the conclusion "
     "intact. Across the specifications measured in the units of the baseline "
     f"the own coefficient ranges from {n('robust_own_min',3)} to "
     f"{n('robust_own_max',3)} and the customer lag from "
     f"{n('robust_down_min',3)} to {n('robust_down_max',3)}."),

    ("p",
     "Two further checks address inference and omitted variables. A restricted "
     "wild cluster bootstrap with Rademacher weights and "
     f"{S['wb_reps']:,} replications gives p = {n('wb_p',3)} for the customer "
     "lag [[cameron2008]],[[roodman2019]]. The coefficient-stability bound of "
     "Oster [[oster2019]] moves the customer-lag coefficient from "
     f"{ov('beta_uncontrolled')} without controls to {ov('beta_controlled')} "
     f"with them while the R-squared rises from {ov('r2_uncontrolled')} to "
     f"{ov('r2_controlled')}; the bias-adjusted value is "
     f"{ov('beta_star')} and selection on unobservables would have to be "
     f"{ova('delta',0)} times as important as selection on the observed "
     "controls to drive the estimate to zero."),

    ("p",
     "The sharpest check is in Appendix A. Table A1 replaces the customer "
     "weights with unweighted links and with the single largest customer, "
     "shifts the customer lag two years back and two years forward, and "
     "finally rewires the customer links at random while leaving every firm's "
     "own adoption, own characteristics and own outcome untouched. The lead "
     "specification is a placebo — a firm's youth employment today should not "
     "respond to its customers' adoption two years hence — and the rewired "
     "specification is the strongest available test that the network is the "
     "conduit. We also re-estimate the whole model on "
     f"{PLA['DownAI']['reps']:,} random rewirings of all three matrices, "
     "preserving the degree distribution: the actual customer-lag coefficient "
     f"is {pv('DownAI','actual',3)} against a rewired distribution centred on "
     f"{pv('DownAI','mean',3)} with a standard deviation of "
     f"{pv('DownAI','sd',3)}, giving a randomisation p-value of "
     f"{pv('DownAI','p',3)}; the supplier and local lags give the same answer. "
     "Whatever the estimated spillovers are, they are not a property of the "
     "firms — they are a property of who is connected to whom."),

    ("table", "table11"),

    ("h2", "5.2. Heterogeneity"),

    ("p",
     "Table 12 splits the sample four ways and reports both the own effect and "
     "the customer effect. The customer channel is stronger for non-state "
     f"firms ({hv('SOE','lo_down',3)} against {hv('SOE','hi_down',3)}), which "
     "is consistent with state-owned firms adjusting employment less freely "
     "for any given demand shock, and stronger for technology-intensive firms "
     f"({hv('Tech','hi_down',3)} against {hv('Tech','lo_down',3)}), whose "
     "output is the kind of service that a customer's models can most readily "
     "replace."),

    ("p",
     "Two splits speak directly to the systems argument. Firms that are "
     "central in the network — those whose supply-chain exposure moves most "
     f"with the system — show a customer effect of {hv('Central','hi_down',3)} "
     f"against {hv('Central','lo_down',3)} for peripheral firms: position in "
     "the system, not any characteristic of the firm itself, governs how much "
     "of the shock reaches it. And in thick local labour markets the own "
     "effect is attenuated relative to thin ones "
     f"({hv('ThickCity','hi_own',3)} against {hv('ThickCity','lo_own',3)}), "
     "which is the reallocation result of Section 4.7 appearing again as a "
     "sample split: where there are many other employers, displaced graduates "
     "are absorbed."),

    ("table", "table12"),

    # =====================================================================
    ("h1", "6. Discussion"),

    ("p",
     "The claim of this paper is that the effect of generative artificial "
     "intelligence on youth employment is a property of a system of firms and "
     "cannot be recovered from any of them individually. The evidence is not "
     "one coefficient but an arithmetic. The within-firm estimate is "
     f"{n('b_partial',3)}. Add the supply chain and the total impact on the "
     f"system is {n('total',3)}, {n('total_over_firm',2)} times larger, with "
     f"{n('indirect_share',0)}% of it falling on firms that have adopted "
     f"nothing. Restrict attention to a city and the estimate is "
     f"{n('b_city',3)}, half the firm-level number, because within a city "
     "young workers move between employers rather than out of employment. The "
     "same underlying phenomenon supports three different numbers, and the "
     "only thing that determines which is right is where the boundary of the "
     "system is drawn."),

    ("p",
     "This reframes a debate that has been conducted as though it had a single "
     "answer. Studies that find large effects and studies that find none may "
     "both be correct about their own estimand: a within-firm design in a "
     "thick local labour market will find reallocation and read it as a small "
     "effect, while the same technology is removing entry-level positions from "
     "the system at three times that rate through customers who never appear "
     "in the sample. The literature's disagreement is, at least in part, a "
     "disagreement about units that has been conducted as a disagreement about "
     "facts."),

    ("p",
     "For firms, the practical implication is that exposure to the technology "
     "is not the same as adoption of it. A firm that has decided not to adopt "
     "has not thereby decided to be unaffected: if its customers adopt, its "
     "demand for junior labour falls anyway, and our estimates say that this "
     "second-hand exposure is larger than the first-hand kind. Workforce "
     "planning that looks only at the firm's own technology roadmap will "
     "therefore be wrong in a predictable direction, and the firms most "
     "exposed are those selling relationship-specific, junior-labour-intensive "
     "services to a small number of customers — precisely the firms least "
     "likely to think of themselves as being in the path of artificial "
     "intelligence."),

    ("p",
     "For policy, three things follow. The first is a measurement warning: "
     "monitoring youth employment at the city level, which is how labour "
     "market statistics are collected, will systematically understate what is "
     "happening, because the local market is where reallocation is most "
     "complete. The second is that the instruments have to match the level. "
     "Local measures — placement services, wage subsidies, thicker local "
     "markets — genuinely help, and our heterogeneity results show they are "
     "already working: thick cities absorb displaced graduates. But they "
     "redistribute the burden rather than reduce it, and they cannot touch the "
     "supply-chain channel at all, because the customer whose adoption is "
     "closing a firm's entry port is typically in another city and another "
     "sector. The third is that the natural policy unit is the network. If "
     "propagation runs along relationship-specific links, then sectoral "
     "roadmaps, standards for AI-enabled procurement and transition support "
     "targeted at supplier ecosystems reach the affected firms in a way that "
     "firm-level instruments do not [[janssen2025]],[[dwivedi2023]]. Recent "
     "systems-level work on Chinese firms points the same way, finding that "
     "the returns to artificial intelligence depend on the organisational, "
     "innovation and governance capabilities that surround it "
     "[[xuejin2025]],[[xue2025]],[[machucho2025]],[[liang2025]]."),

    ("p",
     "Three limitations bound the claims. First, the network is the disclosed "
     "one, which covers the five largest partners on each side; it is the "
     "economically important part of a firm's trade but not all of it, and "
     "measurement error in the weights will attenuate the network lags, making "
     "our multiplier a lower bound. Second, the sample is listed firms, which "
     "are the nodes of the network but not all of it; the unlisted suppliers "
     "and customers through which some of the propagation runs are invisible "
     "here, again in the direction of understatement. Third, the design "
     "identifies the effect over the four years after the shock. Whether the "
     "reallocation we document is temporary — the local market clearing while "
     "the system adjusts — or the beginning of a persistent reduction in entry "
     "positions cannot be settled with four years of data, and the answer "
     "matters, because a cohort that is reallocated is in a different position "
     "from a cohort that is displaced [[kahn2010]],[[oreopoulos2012]],"
     "[[vonwachter2020]]. Following the same network as the technology "
     "matures is the obvious next study, and the organisational literature on "
     "how firms rebuild work around a new technology suggests what to look "
     "for: absorptive capacity governs what a firm can do with a new "
     "technology [[cohen1990]],[[argote2011]], the balance between exploiting "
     "existing routines and exploring new ones governs how fast it rebuilds "
     "them [[march1991]], and the way junior work is reorganised around the "
     "technology determines whether the entry-level rung is rebuilt or removed "
     "[[beane2019]],[[kellogg2020]],[[raisch2021]],[[krakowski2023]],"
     "[[yang2026]]."),

    # =====================================================================
    ("h1", "7. Conclusions"),

    ("p",
     "This paper asked what generative artificial intelligence is doing to "
     "youth employment, and answered that the question has no firm-level "
     f"answer. Using {S['n_obs']:,} firm-year observations for "
     f"{S['n_firms']:,} Chinese A-share listed firms over {S['years']}, their "
     f"disclosed supplier and customer links and the {S['n_cities']} local "
     "labour markets they share, we estimated a network autoregressive model "
     "of the youth employment share and decomposed its impacts."),

    ("p",
     f"Own adoption lowers the youth share by {a('b_partial',3)} percentage "
     f"points per standard deviation. Customers' adoption lowers it by a "
     f"further {a('b_down',3)} and suppliers' by {a('b_up',3)}, while local "
     f"peers' adoption raises it by {n('b_peer',3)}. The direct impact is "
     f"{n('direct',3)}, the indirect impact {n('indirect',3)} and the total "
     f"impact {n('total',3)}, a network multiplier of {n('multiplier',2)} with "
     f"{n('indirect_share',0)}% of the effect outside the adopting firm; the "
     f"city-level coefficient is {n('b_city',3)}, implying that "
     f"{n('realloc_share',0)}% of the firm-level effect is local reallocation "
     "rather than destruction. Propagation is concentrated in "
     "relationship-specific links, is indifferent to geographic distance, is "
     f"{av('DownAI','ratio',1)} times larger for young workers than for "
     "experienced ones, and vanishes when the network is randomly rewired."),

    ("p",
     "The methodological conclusion is that the within-firm coefficient, which "
     "is what the literature reports, is neither an upper nor a lower bound on "
     "anything policy cares about. The substantive conclusion is that a young "
     "person's chances are being changed by technology decisions taken in "
     "firms they will never apply to. And the systems conclusion is the one in "
     "the title: for this question, the sum is not the parts, and the "
     "difference is large enough to reverse the reading of the existing "
     "evidence."),

    # =====================================================================
    ("h1", "Appendix A"),

    ("p",
     "Table A1 reports alternative constructions of the customer network and "
     "the placebo tests described in Section 5.1. Replacing the disclosed "
     "sales shares with unweighted links, and with the single largest customer "
     "only, leaves the coefficient close to the baseline, so the result is not "
     "an artefact of the weighting. Shifting the customer lag two years back "
     "leaves it negative and significant, which is what a propagating shock "
     "should do. Shifting it two years forward is a placebo, since a firm's "
     "youth employment today cannot respond to its customers' future adoption. "
     "Rewiring the customer links at random, while leaving every firm's own "
     "adoption and characteristics exactly as they are, is the strongest test "
     "available that the estimated spillover belongs to the network rather "
     "than to the firms it connects."),

    ("table", "tableA1"),

    # =====================================================================
    ("h1b", "Author Contributions"),
    ("stmt2", "",
     "Conceptualization, methodology, formal analysis, software and "
     "writing—original draft preparation, X.C.; validation, data curation "
     "and visualization, investigation, writing—review and editing, "
     "supervision and project administration, T.M. All authors have read and "
     "agreed to the published version of the manuscript."),

    ("h1b", "Funding"),
    ("stmt2", "",
     "This research was funded by the Zhejiang Provincial Philosophy and Social "
     "Sciences Planning Special Project on Higher Education Basic Research "
     "Funding Reform (Grant Number: 25NDJC153YBMS) and the Major Humanities and "
     "Social Sciences Research Projects in Zhejiang Higher Education "
     "Institutions (Grant Number: 2024QN018)."),

    ("h1b", "Institutional Review Board Statement"),
    ("stmt2", "",
     "Not applicable. The study uses firm-level accounting, disclosure and "
     "supply-chain data and involves no human participants or animals."),

    ("h1b", "Informed Consent Statement"),
    ("stmt2", "", "Not applicable."),

    ("h1b", "Data Availability Statement"),
    ("stmt2", "",
     "The financial, governance, employment-composition and supplier-customer "
     "disclosure data are commercially licensed from the China Stock Market "
     "and Accounting Research database and cannot be redistributed by the "
     "authors; they are available to subscribers. The generative-AI keyword "
     "dictionary, the code that constructs the three weight matrices, the "
     "estimation code for every specification reported in the paper, and the "
     "scripts that generate every table are available from the corresponding "
     "author on reasonable request."),

    ("h1b", "Acknowledgments"),
    ("stmt2", "",
     "The authors thank the editors and the anonymous reviewers for comments "
     "that improved the manuscript."),

    ("h1b", "Conflicts of Interest"),
    ("stmt2", "", "The authors declare no conflicts of interest."),
]
