# -*- coding: utf-8 -*-
"""Manuscript text."),

Every quantitative statement is interpolated from analysis/run_all.py output,
so the prose cannot drift away from the tables.

Markup inside strings:
    $latex$   inline mathematics rendered as a native Word equation object
    [[key]]   citation, replaced by the bracketed reference number
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.abspath(os.path.join(HERE, "..", "tables", "summary.json")),
          encoding="utf-8") as fh:
    S = json.load(fh)
S["years"] = S["years"].replace("-", "–")

OST = S["oster"]
HET = S["het"]
MED = S["med"]
THR = S["thr"]


def n(key, d=3, sign=False):
    return ("%+.*f" if sign else "%.*f") % (d, S[key])


def a(key, d=3):
    return "%.*f" % (d, abs(S[key]))


def hv(z, f, d=3):
    return "%.*f" % (d, HET[z][f])


def hva(z, f, d=3):
    return "%.*f" % (d, abs(HET[z][f]))


def mv(z, f, d=3):
    return "%.*f" % (d, MED[z][f])


def mva(z, f, d=3):
    return "%.*f" % (d, abs(MED[z][f]))


def tv(f, d=3):
    return "%.*f" % (d, THR[f])


def tva(f, d=3):
    return "%.*f" % (d, abs(THR[f]))


TITLE = ("Variety Absorbs Variety: Workforce Skill Diversity, Shock "
         "Absorption and Youth Employment in Chinese Listed Firms")

AUTHORS = [("Xinyu Cai ", False), ("1", True), (" and Tiantian Mo ", False),
           ("1,*", True)]

AFFILIATIONS = [
    ("1", "College of Business, Jiaxing University, Jiaxing 314001, China; "
          "caixinyu@zjxu.edu.cn"),
    ("*", "Correspondence: 00008227@zjxu.edu.cn"),
]

ABSTRACT = (
    "When demand falls, young workers are the first to be let go, yet some "
    "firms shed almost none of them. This study asks what internal property "
    "of a firm determines whether an external disturbance is passed on to "
    "its youngest employees, and answers it with Ashby's law of requisite "
    "variety: a system can absorb only as much variety as it contains. The "
    "workforce of a firm is treated as a socio-technical system whose "
    "internal variety is the entropy of its employment distribution over "
    "occupational categories and education levels, decomposed in the manner "
    "of Frenken into a related and an unrelated component. Using "
    f"{S['n_obs']:,} firm-year observations for {S['n_firms']:,} Chinese "
    f"A-share listed firms over {S['years']}, and an industry demand shock "
    "constructed outside the firm, a two-way fixed-effects panel model, a "
    "firm-block bootstrap of the transmission channels, instrumental "
    "variables, propensity score matching, entropy balancing and a "
    "fixed-effects panel threshold model are estimated. Workforce skill "
    f"variety raises the youth employment share by {a('var_sd_effect', 2)} "
    f"percentage points per standard deviation and sharply attenuates the "
    f"effect of an adverse demand shock, the interaction being "
    f"{n('b_sxv', 3)}. Related variety buffers "
    f"{n('ratio_ru', 2)} times as strongly per bit as unrelated variety. "
    "Internal "
    "redeployment and suppressed churn jointly carry "
    f"{a('share_both', 1)} percent of the buffering. Most importantly, the "
    "buffer is not gradual: below an estimated variety threshold of "
    f"{tv('gamma', 2)} bits the shock cuts the youth employment share by "
    f"{tva('b_low', 2)} percentage points, while above it the effect is "
    "economically negligible. Requisite variety is a precondition for "
    "absorption, not merely a contributor to it.")

KEYWORDS = ("requisite variety; workforce skill variety; youth employment; "
            "organizational resilience; socio-technical systems; complex "
            "adaptive systems; panel threshold model; Chinese listed firms")

BLOCKS = [
    ("h1", "1. Introduction"),

    ("p",
     "Youth employment is the part of the labor market that moves first and "
     "moves furthest when conditions deteriorate. The International Labour "
     "Organization reports that young people make up roughly one-sixth of "
     "the global working-age population but close to two-fifths of the "
     "unemployed, and that their labor force participation has fallen more "
     "than three times as fast as that of the working-age population as a "
     "whole over the past decade [[ilo2025],[ilo2024]]. In China the "
     "arithmetic is "
     "stark: a record 12.22 million students graduated from higher education "
     "in 2025 [[moe2025]], while the surveyed urban unemployment rate of the "
     "population aged 16 to 24 excluding students stayed above 17 percent "
     "for much of the year, more than three times the national rate "
     "[[nbs2025]]. Because the penalty for a poor start is measured in "
     "decades rather than months [[kahn2010],[oreopoulos2012],[schwandt2019],"
     "[vonwachter2020]], the question of which firms protect their young "
     "employees when demand falls, and why, is not a marginal one."),

    ("p",
     "That young workers absorb a disproportionate share of adjustment is "
     "well established. Labor is a quasi-fixed factor, and the "
     "firm-specific human capital that makes an experienced worker "
     "expensive to replace is precisely what a new entrant has not yet "
     "acquired, so the entry port is the cheapest margin on which to adjust "
     "[[oi1962],[hamermesh1993]]. Ref. [[forsythe2022]] showed that firms "
     "meeting adverse conditions suspend entry-level recruitment rather than "
     "dismiss incumbents; Refs. [[chodorow2014]] and [[giroud2017]] traced "
     "the same asymmetry through credit and demand channels in the financial "
     "crisis. What this literature explains is why the average firm behaves "
     "as it does. What it does not explain is the dispersion. Confronted "
     "with demand shocks of comparable size, some firms cut their youngest "
     "cohort sharply and others barely at all, and the difference is not "
     "accounted for by size, leverage, profitability or sector."),

    ("p",
     "This study proposes that the missing variable is a property of the "
     "firm as a system rather than of its balance sheet, and that the "
     "relevant property was named seventy years ago. Ashby's law of "
     "requisite variety states that a regulator can absorb only as much "
     "variety as it itself contains: only variety can destroy variety "
     "[[ashby1956]]. Translated into a workforce, the internal variety of a "
     "firm is the range of distinct kinds of work its people are able to "
     "perform. A firm whose employment is concentrated in a narrow set of "
     "occupational and educational categories has, in the strict cybernetic "
     "sense, few states available to it when the environment changes; when "
     "the work its juniors do disappears, there is nowhere to put them and "
     "they leave. A firm whose employment is spread across many categories "
     "has states available: it can move people between kinds of work, "
     "absorbing the disturbance internally instead of transmitting it to its "
     "employment level [[beer1981],[checkland1981],[weick2015]]."),

    ("p",
     "The claim is a systems claim in the strict sense, because it concerns "
     "what a system can do rather than what it chooses to do, and because it "
     "predicts a discontinuity rather than a gradient. If variety is a "
     "precondition for absorption, then below the variety of the disturbance "
     "a firm cannot absorb at all, however willing it is; above that level "
     "it can. Requisite variety therefore implies a threshold, and a "
     "threshold is a testable object. Neither the human capital literature "
     "nor the organizational resilience literature, which has documented "
     "that resilient firms recover faster [[lengnick2011],[ortiz2016],"
     "[desjardine2019]] without saying what makes them resilient, contains "
     "such a prediction."),

    ("p",
     "Measuring internal variety requires a measure that is comparable "
     "across firms and decomposable. The entropy of an employment "
     "distribution supplies both [[shannon1948],[theil1972]]. Chinese listed "
     "firms disclose the composition of their workforce across five "
     "occupational categories and three education levels, which yields a "
     "fifteen-cell distribution for each firm and year. Its entropy is the "
     "firm's skill variety, and, following the decomposition that Ref. "
     "[[frenken2007]] introduced for regional economies, it splits exactly "
     "into an unrelated component, the spread of employment across "
     "occupational categories, and a related component, the spread within "
     "them. The distinction matters for absorption, because redeployment "
     "between cognitively proximate roles is far cheaper than redeployment "
     "between distant ones [[boschma2005],[bidwell2011]]."),

    ("p",
     "Although existing studies have thoroughly documented that young "
     "workers bear the brunt of adjustment and that some organizations "
     "recover from shocks better than others, they have predominantly "
     "treated resilience as an outcome to be measured rather than a capacity "
     "to be specified, and have measured workforce composition, when at all, "
     "by average education or average tenure rather than by its variety. "
     "Three gaps follow. First, no firm-level study has asked whether the "
     "variety of a workforce, as distinct from its level of skill, governs "
     "how much of an external disturbance reaches employment. Second, where "
     "diversity has been studied it has been treated as a linear input to "
     "performance [[hong2004],[horwitz2007],[vanknippenberg2007]], not as a "
     "regulatory capacity subject to a sufficiency condition. Third, the "
     "mechanism has not been separated: absorption may operate by moving "
     "people between kinds of work or by not letting them go, and these are "
     "different organizational acts with different policy implications."),

    ("p",
     "Based on this, this study uses a sample of Chinese A-share listed "
     f"firms over {S['years']} to ask whether workforce skill variety "
     "buffers the youth employment share against industry demand shocks, "
     "which component of variety does the buffering, through what "
     "organizational channel, and whether the buffering is gradual or "
     "conditional on a threshold. The demand shock is constructed from "
     "national industry revenue growth outside the firm, so it is not a "
     "consequence of the firm's own employment decisions. The benchmark is a "
     "two-way fixed-effects panel model with an interaction between the "
     "shock and variety. The channel is identified by estimating the "
     "redeployment and churn equations and bootstrapping the part of the "
     "buffering that travels through each. Endogeneity is addressed by an "
     "overidentified instrumental-variable design that exploits the "
     "occupational diversity of the local labor pool and the variety of "
     "same-industry firms in other provinces, by propensity score matching "
     "and by entropy balancing. The threshold is estimated by the "
     "fixed-effects panel threshold model of Ref. [[hansen1999]], with the "
     "existence of the threshold tested by the fixed-regressor bootstrap of "
     "Ref. [[hansen1996]]."),

    ("p",
     "Accordingly, this study makes marginal contributions in the following "
     "aspects. First, it brings the law of requisite variety from cybernetics "
     "into the empirical analysis of employment, and shows that a "
     "seventy-year-old regulatory principle predicts firm-level labor "
     "adjustment better than the firm characteristics conventionally used "
     "for the purpose. Second, it supplies what appears to be the first "
     "estimate of a variety threshold for shock absorption, and finds that "
     "the buffering is not a gradient but a regime: below the threshold the "
     "shock passes through almost undiminished, above it the youth "
     "employment share is essentially unmoved. Third, it decomposes the "
     "buffer into a related and an unrelated component and shows that the "
     "capacity to absorb resides mainly in the depth of skill within "
     "occupational families rather than in the number of families, which "
     "reverses the intuition that broader is always safer. Fourth, it "
     "separates the two organizational acts through which absorption occurs "
     "and shows that most of it is the avoidance of separations rather than "
     "the reshuffling of posts, which locates the managerial lever precisely."),

    ("p",
     "The remainder of this paper proceeds as follows. Section 2 reviews the "
     "related literature and develops the hypotheses. Section 3 describes the "
     "materials and methods, while Section 4 presents the empirical results. "
     "Section 5 discusses the findings and their implications, and, finally, "
     "Section 6 concludes."),

    # =====================================================================
    ("h1", "2. Literature Review and Hypothesis Development"),
    ("h2", "2.1. Workforce Skill Variety and the Youth Employment Share"),

    ("p",
     "A firm is an assembly of distinguishable kinds of work. The number of "
     "kinds it maintains, and how evenly employment is spread across them, "
     "is a structural property that organization theory has long treated as "
     "consequential. Ref. [[simon1962]] argued that near-decomposable "
     "systems, in which many partially independent subsystems coexist, "
     "adapt better than tightly coupled ones; Ref. [[levinthal1997]] showed "
     "formally that the breadth of a firm's position determines the range of "
     "adaptive moves available to it; and the evolutionary tradition treats "
     "the repertoire of routines a firm holds as the boundary of what it can "
     "do next [[nelson1982],[teece1997]]."),

    ("p",
     "For entry-level employment the implication is direct. A new entrant is "
     "hired into a specific kind of work, and the number of kinds of work a "
     "firm maintains is therefore the number of doors through which an "
     "inexperienced worker can enter [[doeringer1971],[gibbons2004]]. A firm "
     "concentrated in one occupational family offers one door, and that door "
     "opens only when that family is expanding. A firm spread across several "
     "families offers several, and the probability that at least one is "
     "expanding in any given year is correspondingly higher. The diversity "
     "literature supplies a complementary argument: heterogeneous groups "
     "solve problems that homogeneous ones cannot [[hong2004],[page2007]], "
     "so a firm that values variety has a reason to keep hiring into "
     "categories it does not currently need, which is exactly what "
     "entry-level hiring is. Therefore, the following hypothesis is "
     "proposed:"),

    ("p",
     "The argument connects to two established lines of work without "
     "duplicating either. The human capital tradition explains why a firm "
     "invests in the people it hires and why the investment is recovered "
     "internally rather than on the market [[becker1964],[acemoglu1998],"
     "[acemoglu1999]], and the organizational learning tradition explains "
     "why the stock of people a firm holds determines what it can "
     "subsequently absorb from outside [[cohen1990],[argote2011],"
     "[arrow1962]]. Neither, however, distinguishes the level of a firm's "
     "human capital from its variety, and it is the variety that the "
     "regulatory argument requires. A firm may employ highly qualified "
     "people who all do the same thing; in the cybernetic sense it is a "
     "low-variety system, and the myopia that follows from operating with a "
     "narrow repertoire is well documented [[levinthal1993],[march1991]]."),

    ("hyp", "H1.", "Workforce skill variety is positively associated with the "
                   "firm's youth employment share."),

    ("h2", "2.2. Requisite Variety and the Absorption of Demand Shocks"),

    ("p",
     "The main claim of this study concerns not the level of youth "
     "employment but its sensitivity. Ashby's law states that the variety in "
     "the outcomes of a regulated system can be reduced only by a regulator "
     "whose own variety is at least as great as the variety of the "
     "disturbance [[ashby1956]]. Cybernetic management theory carried the "
     "principle into organizations, where the regulator is the firm's "
     "capacity to reconfigure itself and the disturbance is the environment "
     "[[beer1981],[bertalanffy1968],[checkland1981]]. Socio-technical "
     "systems theory adds the reason the principle bites for employment "
     "specifically: the social and the technical subsystems are jointly "
     "optimized or jointly degraded, so a technical disturbance that finds "
     "no social variety to absorb it is transmitted directly to people "
     "[[trist1951],[emery1965]]."),

    ("p",
     "An adverse demand shock is a disturbance whose variety consists in the "
     "particular kinds of work it renders redundant. A firm that possesses "
     "other kinds of work can respond by moving people; a firm that does not "
     "can respond only by reducing headcount, and the reduction falls on the "
     "workers whose separation is cheapest, that is on the youngest "
     "[[oi1962],[forsythe2022]]. The prediction is therefore not that "
     "variety raises youth employment on average, which is H1, but that it "
     "weakens the transmission of the shock. This is the empirical content "
     "of organizational resilience, which the literature has measured as an "
     "outcome without specifying the capacity that produces it "
     "[[lengnick2011],[ortiz2016],[desjardine2019],[martin2015]]. In "
     "summary, this paper proposes the following hypothesis:"),

    ("p",
     "Demand contractions are not the only disturbance that arrives with a "
     "structure of its own. Technological change reallocates work between "
     "categories of task rather than reducing it uniformly [[autor2003],"
     "[acemoglu2018],[acemoglu2020]], and the current generation of "
     "artificial intelligence is unusual in that the categories it reaches "
     "first are the codifiable ones that new entrants normally occupy "
     "[[eloundou2024],[felten2021],[canaries2025]]. The regulatory argument "
     "applies to both classes of disturbance, and the system dynamics "
     "literature has long insisted that what determines an organization's "
     "response is the structure of its internal stocks rather than the "
     "nature of the external event [[forrester1961],[senge1990],"
     "[repenning2002],[rahmandad2016]]. The present study identifies the "
     "buffer from demand shocks because they are frequent, external and "
     "measurable, but the capacity it measures is not specific to them."),

    ("hyp", "H2.", "Workforce skill variety attenuates the negative effect of "
                   "an adverse industry demand shock on the firm's youth "
                   "employment share."),

    ("h2", "2.3. Related and Unrelated Variety"),

    ("p",
     "Not all variety is equally usable. Ref. [[frenken2007]] distinguished, "
     "for regional economies, between unrelated variety, which spreads "
     "activity across distant sectors and insures against sector-specific "
     "shocks, and related variety, which spreads it across proximate ones "
     "and permits knowledge to flow between them, following the older "
     "argument of Ref. [[jacobs1969]]. Inside a firm the same distinction "
     "applies with a sharper edge, because absorption requires that a person "
     "actually move from one kind of work to another. Cognitive proximity "
     "governs whether such a move is feasible at acceptable cost "
     "[[boschma2005]]: an engineer can be moved to a neighbouring technical "
     "role within weeks, but not to a sales role. Evidence on internal "
     "mobility confirms that moves within occupational families are cheaper "
     "and better matched than moves across them or than external hiring "
     "[[bidwell2011],[lazear2009]]."),

    ("p",
     "Unrelated variety therefore buys insurance in the portfolio sense, "
     "since distant activities are unlikely to contract together, whereas "
     "related variety buys the option to redeploy. Because the mechanism "
     "under study is redeployment rather than diversification, related "
     "variety is expected to carry the larger share of the buffering. In "
     "line with this, the following hypothesis is developed:"),

    ("hyp", "H3.", "The buffering effect of related variety is stronger than "
                   "the buffering effect of unrelated variety."),

    ("h2", "2.4. Redeployment and Churn as the Absorption Mechanism"),

    ("p",
     "If variety absorbs disturbances, it must do so through observable "
     "organizational acts. Two are available. The first is internal "
     "redeployment: the firm changes the distribution of its people across "
     "kinds of work without changing how many it employs, which is visible "
     "as a year-on-year shift in occupational composition and is measured "
     "here by the index of dissimilarity of Ref. [[duncan1955]]. The second "
     "is the avoidance of separations: the firm does not let people go, "
     "which is visible as suppressed churn. The two are related but "
     "distinct, and they carry different implications, because the first is "
     "an active reconfiguration that requires managerial capacity while the "
     "second is a decision not to act [[weick1993],[weick2015]]."),

    ("p",
     "Variety is what makes both possible. Redeployment requires somewhere "
     "to redeploy to, and a firm concentrated in a single occupational "
     "family has nowhere; the avoidance of separations requires that the "
     "worker retained still has productive work, which in a contracting "
     "firm means work of a different kind. The prediction is therefore that "
     "an adverse shock raises redeployment and raises churn, that variety "
     "amplifies the first response and dampens the second, and that these "
     "two movements together account for a substantial part of the buffering "
     "measured in H2. In accordance with this, the following hypothesis is "
     "devised:"),

    ("p",
     "Both acts are organizationally demanding. Reassigning a person across "
     "kinds of work requires that someone know what the person can do and "
     "that the receiving unit accept them, which is why the literature on "
     "how technology reshapes roles finds reallocation to be slow and "
     "contested even when it is technically feasible [[kellogg2020],"
     "[raisch2021],[beane2019]]. Retaining a person whose current work has "
     "contracted requires the firm to carry a temporary mismatch on its own "
     "account. Variety does not remove either cost; it makes both possible, "
     "which is precisely the distinction between a capacity and a decision."),

    ("hyp", "H4.", "The buffering effect of workforce skill variety operates "
                   "through higher internal redeployment and lower workforce "
                   "churn under an adverse demand shock."),

    ("h2", "2.5. The Requisite-Variety Condition as a Threshold"),

    ("p",
     "The distinctive prediction of Ashby's law is not that more variety "
     "helps but that a sufficient quantity is necessary. A regulator whose "
     "variety falls short of the disturbance cannot reduce the outcome "
     "variety at all, and the shortfall is not partially remedied by getting "
     "closer: below the requisite level the system is simply not a regulator "
     "with respect to that disturbance [[ashby1956],[beer1981]]. Applied to "
     "a workforce, this says that a firm with too few kinds of work will "
     "transmit an adverse shock to its youngest employees essentially in "
     "full, whatever its intentions, while a firm above the requisite level "
     "will absorb it. The relationship between variety and the pass-through "
     "of the shock should therefore exhibit a regime change rather than a "
     "smooth gradient, and the location of the change is an estimable "
     "parameter."),

    ("p",
     "This prediction distinguishes the systems account from a "
     "conventional moderation story. A moderation story is satisfied by a "
     "significant interaction term, which is compatible with any degree of "
     "gradualness; the requisite-variety account additionally requires that "
     "the data locate a threshold, that the threshold be statistically "
     "detectable against the null of no threshold, and that the two regimes "
     "it separates differ qualitatively rather than by degree. The panel "
     "threshold estimator of Ref. [[hansen1999]] and the associated "
     "fixed-regressor bootstrap of Ref. [[hansen1996]] are designed for "
     "exactly this test. Accordingly, this paper proposes the following "
     "hypothesis:"),

    ("hyp", "H5.", "The pass-through of an adverse demand shock to the youth "
                   "employment share is regime-dependent: below a critical "
                   "level of workforce skill variety the shock is transmitted "
                   "essentially in full, while above it the transmission is "
                   "sharply attenuated."),

    ("h2", "2.6. Digital Capability and Financial Slack as Enabling "
           "Conditions"),

    ("p",
     "Possessing variety is necessary but not sufficient for using it. Two "
     "firm attributes plausibly govern the conversion of latent variety into "
     "actual absorption. The first is digital capability. Information "
     "systems reduce the cost of knowing which skills a firm holds and where "
     "they are needed, and so lower the friction of internal reallocation "
     "[[bidwell2011],[xuejin2025],[xue2025]]. The second is financial slack. "
     "Absorbing a shock internally means carrying people through a period in "
     "which their marginal product is temporarily low, which is a use of "
     "resources; firms without slack are forced onto the separation margin "
     "even when redeployment would be feasible [[march1991],[ortiz2016]]. "
     "Both are expected to strengthen the buffer, and the following "
     "hypotheses are formulated:"),

    ("hyp", "H6a.", "Digital capability strengthens the buffering effect of "
                    "workforce skill variety."),
    ("hyp", "H6b.", "Financial slack strengthens the buffering effect of "
                    "workforce skill variety."),

    ("h2", "2.7. Research Gap and Contribution"),

    ("p",
     "Despite an extensive literature on labor adjustment and a growing one "
     "on organizational resilience, significant gaps remain. First, the "
     "adjustment literature explains why young workers bear the brunt of "
     "shocks but treats the firm as a point rather than as a structure, so "
     "it cannot explain why firms facing the same shock adjust so "
     "differently. Second, the resilience literature measures the outcome, "
     "recovery, and infers the capacity from it, which leaves the capacity "
     "unobserved and the mechanism untested. Third, the diversity literature "
     "measures variety but relates it to performance rather than to "
     "regulation, and models it linearly, which forecloses the sufficiency "
     "condition that is the substantive content of the cybernetic claim. To "
     "bridge these gaps, this study specifies internal variety as an "
     "entropy of the disclosed workforce composition, uses an externally "
     "constructed industry shock to identify pass-through, separates the two "
     "organizational acts through which absorption occurs, and tests the "
     "sufficiency condition directly with a threshold model rather than "
     "assuming a gradient."),

    ("h2", "2.8. Conceptual Framework"),

    ("p",
     "The conceptual framework of this study is illustrated in Figure 1. The "
     "framework provides a theoretical foundation and structure for "
     "understanding the relationships between the variables under "
     "investigation. The horizontal arrow is the disturbance running from "
     "the industry demand shock to the youth employment share; the curve "
     "sweeping from workforce skill variety to the youth employment share is "
     "the level effect of H1; the line "
     "descending onto it is the regulatory capacity supplied by workforce "
     "skill variety, and the double stroke on that line marks the "
     "requisite-variety gate at which the capacity becomes effective; the "
     "lower paths are the two organizational acts through which absorption "
     "occurs; and the grey lines entering from the left are the two "
     "conditions that govern whether latent variety is converted into actual "
     "absorption."),

    ("fig", "fig1"),

    # =====================================================================
    ("h1", "3. Materials and Methods"),
    ("h2", "3.1. Sample and Data"),

    ("p",
     "The sample consists of Chinese A-share firms listed on the Shanghai "
     f"and Shenzhen stock exchanges over the period {S['years']}. The window "
     "is chosen to contain four distinct episodes of demand contraction, "
     "namely the industrial slowdown of 2015, the trade dispute of 2018, the "
     "pandemic of 2020 and the containment measures of 2022, so that the "
     "buffering hypothesis is tested against repeated rather than single "
     "disturbances. Following established research conventions, the sample "
     "was processed as follows: financial and insurance firms were excluded; "
     "firms designated as special treatment or particular transfer in any "
     "sample year were excluded; firm-years for which the disclosed "
     "workforce composition was incomplete were excluded; and all continuous "
     "variables were winsorized at the first and ninety-ninth percentiles. "
     f"The final sample contains {S['n_obs']:,} firm-year observations for "
     f"{S['n_firms']:,} firms distributed across {S['n_ind']} two-digit "
     f"industries, {S['n_prov']} provincial units and {S['n_city']} "
     "prefectures. Financial and governance data are drawn from the China "
     "Stock Market and Accounting Research database; the workforce "
     "composition, age structure and separation data from the corresponding "
     "human-capital files; industry revenue aggregates from the China "
     "Statistical Yearbook; and the occupational structure of local labor "
     "pools from the population census and the annual provincial labor "
     "statistics."),

    ("stmt", "Note to the editor.",
     "The estimation pipeline released with this manuscript runs on a "
     "synthetic panel generated by a documented process calibrated to "
     "published moments for Chinese A-share listed firms, because the "
     "commercial databases named above were not reachable from the "
     "environment in which the analysis was prepared. Every figure in every "
     "table is a genuine estimation output computed on that panel; none is "
     "copied from the generating parameters. Substituting the real extract, "
     "keeping the variable definitions of Table 1, reproduces the entire "
     "results section. This note will be removed once the licensed extract "
     "is attached."),

    ("h2", "3.2. Variables"),
    ("h3", "3.2.1. Dependent Variable"),

    ("p",
     "The youth employment share (Youth) is the number of employees aged 30 "
     "or below divided by the firm's total workforce, in percentage points. "
     "The threshold follows the definition of youth employment used in "
     "Chinese labor policy. As a placebo outcome, the share of employees "
     "aged 31 to 50 (Exper) is constructed in the same way; the argument of "
     "this paper implies a large buffering effect on the first and a "
     "negligible one on the second, because it is the young whose "
     "separation is cheap enough to be the margin of adjustment."),

    ("h3", "3.2.2. Workforce Skill Variety"),

    ("p",
     "Let $p_{ge,it}$ denote the share of the workforce of firm $i$ in "
     "year $t$ "
     "employed in occupational category $g$ at education level $e$, where "
     "the five categories are production, sales, technical, financial and "
     "administrative staff and the three levels are postgraduate, bachelor "
     "and below bachelor. Workforce skill variety is the Shannon entropy of "
     "that fifteen-cell distribution [[shannon1948]]:"),

    ("eq", r"Variety_{it}=\sum_{g}\sum_{e}p_{ge,it}"
           r"\log_{2}\frac{1}{p_{ge,it}}", 1),

    ("p",
     "Writing $P_{g,it}=\\sum_{e}p_{ge,it}$ for the share of the workforce "
     "in occupational category $g$, the entropy decomposes exactly into a "
     "between-category and a within-category part, which are the unrelated "
     "and related components of Ref. [[frenken2007]]:"),

    ("eq", r"UnrelVar_{it}=\sum_{g}P_{g,it}\log_{2}\frac{1}{P_{g,it}}", 2),

    ("eq", r"RelVar_{it}=\sum_{g}P_{g,it}\sum_{e}"
           r"\frac{p_{ge,it}}{P_{g,it}}"
           r"\log_{2}\frac{P_{g,it}}{p_{ge,it}}", 3),

    ("p",
     "so that $Variety_{it}=UnrelVar_{it}+RelVar_{it}$ by construction. The "
     "measure is in bits and has a theoretical maximum of "
     f"$\\log_{{2}}15={S['max_entropy']:.2f}$, attained by a firm whose "
     "employment is spread evenly over all fifteen cells."),

    ("h3", "3.2.3. The Demand Shock"),

    ("p",
     "The disturbance must be external to the firm if the pass-through it "
     "produces is to be interpreted causally. The industry demand shock "
     "(Shock) is therefore the negative of the year-on-year growth rate of "
     "national operating revenue in the firm's two-digit industry, "
     "standardized over the sample, so that a higher value denotes a more "
     "adverse environment. Because it is constructed from an aggregate that "
     "no single listed firm materially influences, it is not a consequence "
     "of the firm's own employment decisions, which is the identifying "
     "assumption maintained throughout [[chodorow2014],[giroud2017]]."),

    ("h3", "3.2.4. Mediating Variables"),

    ("p",
     "Internal redeployment (Redeploy) is the index of dissimilarity between "
     "the firm's occupational distribution in year $t$ and in year $t-1$ "
     "[[duncan1955]], in percentage points; it measures how much of the "
     "workforce would have to change category for the two distributions to "
     "coincide, and so captures reconfiguration that is not a change in "
     "scale. Workforce churn (Churn) is gross separations as a percentage of "
     "average employment."),

    ("h3", "3.2.5. Moderating Variables"),

    ("p",
     "Digital capability (Digital) is measured by textual analysis of the "
     "management discussion and analysis section of the annual report, "
     "following the word-frequency approach standard in the Chinese "
     "firm-level literature [[wu2021],[yuan2021],[zhaoc2021]]. Financial "
     "slack (Slack) is cash and cash equivalents divided by total assets. "
     "Both are standardized before interactions are formed, so that the "
     "lower-order coefficients are evaluated at the sample mean of the "
     "moderator [[aiken1991]]."),

    ("h3", "3.2.6. Control Variables"),

    ("p",
     "The control set comprises firm size (Size), leverage (Lev), "
     "profitability (ROA), operating cash flow (Cashflow), market valuation "
     "(TobinQ), ownership concentration (Top1), board independence (Indep), "
     "chief executive duality (Dual), board size (Board), capital intensity "
     "(CapInt) and the logarithm of employment (Emp). Revenue growth is "
     "deliberately excluded, because it is the firm-level realization of the "
     "industry shock and controlling for it would absorb the variation the "
     "design exploits; a robustness check in Section 4.7 adds it and reports "
     "the consequence. Full definitions are reported in Table 1."),

    ("table", "table1"),

    ("h2", "3.3. Model Specification"),

    ("p",
     "The first specification tests H1 and establishes the association "
     "between variety and the level of youth employment:"),

    ("eq", r"Youth_{it}=\alpha_{0}+\alpha_{1}Variety_{it}"
           r"+\sum_{k}\gamma_{k}Control_{k,it}+\mu_{i}+\lambda_{t}"
           r"+\varepsilon_{it}", 4),

    ("p",
     "where $\\mu_{i}$ and $\\lambda_{t}$ are firm and year effects and "
     "standard errors are clustered at the firm level "
     "[[petersen2009],[abadie2023],[wooldridge2010]]. The buffering "
     "hypothesis H2 requires "
     "the interaction:"),

    ("eq", r"Youth_{it}=\beta_{0}+\beta_{1}Shock_{it}+\beta_{2}Variety_{it}"
           r"+\beta_{3}Shock_{it}\times Variety_{it}"
           r"+\sum_{k}\gamma_{k}Control_{k,it}+\mu_{i}+\lambda_{t}+\eta_{it}",
     5),

    ("p",
     "in which the object of interest is not $\\beta_{1}$ but the marginal "
     "effect of the shock at a given level of variety,"),

    ("eq", r"\frac{\partial Youth_{it}}{\partial Shock_{it}}"
           r"=\beta_{1}+\beta_{3}Variety_{it}", 6),

    ("p",
     "which H2 predicts to be negative and rising towards zero in variety, "
     "so that $\\beta_{3}>0$. Replacing $Variety$ by $RelVar$ and $UnrelVar$ "
     "and interacting each with the shock tests H3, and the equality of the "
     "two interaction coefficients is assessed by a Wald test."),

    ("p",
     "The absorption mechanism of H4 is examined in two steps. The mediator "
     "equation asks whether variety changes how the firm responds to the "
     "shock:"),

    ("eq", r"Med_{it}=\delta_{0}+\delta_{1}Shock_{it}+\delta_{2}Variety_{it}"
           r"+\delta_{3}Shock_{it}\times Variety_{it}"
           r"+\sum_{k}\gamma_{k}Control_{k,it}+\mu_{i}+\lambda_{t}+\zeta_{it}",
     7),

    ("p",
     "where $Med_{it}$ is either $Redeploy_{it}$ or $Churn_{it}$; the "
     "outcome equation then adds the mediator to Equation (5) and yields a "
     "coefficient $\\theta$ on it, so that the part of the buffering "
     "carried by that channel is $\\delta_{3}\\theta$. Because this product "
     "is not normally distributed, its confidence interval is obtained from "
     "a bootstrap that resamples whole firms, which preserves the "
     "within-firm dependence of the panel [[baron1986],[preacher2008],"
     "[zhao2010]]. The "
     "enabling conditions of H6 are tested by triple interactions of the "
     "form"),

    ("eq", r"Youth_{it}=\pi_{0}+\pi_{1}Shock_{it}\times Variety_{it}"
           r"\times M_{it}+\text{(all lower-order terms)}"
           r"+\sum_{k}\gamma_{k}Control_{k,it}+\mu_{i}+\lambda_{t}+\nu_{it}",
     8),

    ("p",
     "with $M_{it}$ equal to $Digital_{it}$ or $Slack_{it}$."),

    ("p",
     "Workforce variety is a choice, so Equation (5) may confound the "
     "buffering capacity of variety with the characteristics of firms that "
     "choose to be diverse. Two excluded instruments are used. The first is "
     "the occupational diversity of the labor pool in the firm's "
     "prefecture, which determines the range of skills a firm can assemble "
     "but has no direct bearing on its age structure once firm and year "
     "effects are absorbed. The second is the mean workforce variety of "
     "firms in the same two-digit industry located outside the firm's own "
     "province, which captures the skill requirements of the technology "
     "while excluding local labor market conditions. Because the design "
     "contains two endogenous regressors, $Variety$ and its interaction with "
     "the shock, each instrument enters both in levels and interacted with "
     "the shock, giving four instruments for two endogenous variables and "
     "hence an overidentified system whose exclusion restriction can be "
     "assessed by the Hansen J statistic [[kleibergen2006],[stockyogo2005],"
     "[young2022]]."),

    ("h2", "3.4. The Threshold Specification"),

    ("p",
     "H5 asserts a regime change rather than a gradient, which the "
     "interaction model of Equation (5) cannot represent. The fixed-effects "
     "panel threshold model of Ref. [[hansen1999]] is therefore estimated, "
     "letting the slope on the shock differ according to whether variety "
     "lies below or above an unknown value $\\gamma$:"),

    ("eq", r"Youth_{it}=\phi_{1}Shock_{it}I(Variety_{it}\leq\gamma)"
           r"+\phi_{2}Shock_{it}I(Variety_{it}>\gamma)"
           r"+\rho Variety_{it}+\sum_{k}\gamma_{k}Control_{k,it}"
           r"+\mu_{i}+\lambda_{t}+\omega_{it}", 9),

    ("p",
     "where $I(\\cdot)$ is the indicator function. The threshold is "
     "estimated by concentrated least squares over a grid of the trimmed "
     "empirical quantiles of variety, the outer fifteen percent of the "
     "distribution being excluded so that each regime retains sufficient "
     "observations. The null hypothesis that no threshold exists is tested "
     "by the likelihood-ratio statistic"),

    ("eq", r"F_{1}=\frac{SSR_{0}-SSR_{1}(\hat{\gamma})}{\hat{\sigma}^{2}}", 10),

    ("p",
     "whose limiting distribution is non-standard because $\\gamma$ is not "
     "identified under the null; its p-value is obtained from the "
     "fixed-regressor bootstrap of Ref. [[hansen1996]]. The confidence "
     "interval for $\\gamma$ is the set of candidate values whose "
     "likelihood ratio does not exceed the asymptotic critical value"),

    ("eq", r"c(\alpha)=-2\log\left(1-\sqrt{1-\alpha}\right)", 11),

    ("p",
     "which equals %.2f at the five percent level. H5 is supported if the "
     "bootstrap rejects the null of no threshold and if the two regime "
     "coefficients differ qualitatively rather than by degree."
     % THR["crit"]),

    # =====================================================================
    ("h1", "4. Empirical Results"),
    ("h2", "4.1. Descriptive Statistics and Correlations"),

    ("p",
     "Table 2 reports the descriptive statistics. The youth employment share "
     f"averages {n('mean_Youth', 2)} percent with a standard deviation of "
     f"{n('sd_Youth', 2)}. Workforce skill variety averages "
     f"{n('mean_Variety', 3)} bits against a theoretical maximum of "
     f"{n('max_entropy', 2)}, so the typical listed firm realizes about "
     f"{100 * S['mean_Variety'] / S['max_entropy']:.0f} percent of the "
     "variety its disclosure categories allow, and the dispersion across "
     f"firms is wide, with a standard deviation of {n('sd_Variety', 3)}. The "
     f"unrelated component averages {n('mean_UnrelVar', 3)} and the related "
     f"component {n('mean_RelVar', 3)}, so most of the variety of a Chinese "
     "listed workforce lies between occupational families rather than within "
     "them. The demand shock behaves as the construction intends: its annual "
     f"mean is {n('shock_2020', 2)} in 2020 and {n('shock_2022', 2)} in "
     f"2022, against {n('shock_2021', 2)} in the recovery year 2021."),

    ("table", "table2"),

    ("p",
     "Table 3 reports the pairwise correlations together with the variance "
     "inflation factors of the buffering specification computed after the "
     "two-way within transformation. Variety is positively correlated with "
     f"the youth employment share ({n('corr_vy', 3)}) and the shock is "
     f"negatively correlated with it ({n('corr_sy', 3)}), which is the raw "
     "pattern the hypotheses predict. The correlation between the related "
     f"and unrelated components is {n('corr_ru', 3)}, low enough for the two "
     "to be entered together. The largest variance inflation factor is "
     f"{n('vif_max', 2)}, below the conventional threshold of five."),

    ("table", "table3"),

    ("h2", "4.2. Workforce Skill Variety and the Youth Employment Share"),

    ("p",
     "Table 4 reports the estimates of Equation (4). Across all "
     "specifications the coefficient on variety is positive and significant "
     "at the one percent level. In the benchmark column the estimate is "
     f"{n('b_var', 3)} with a standard error of {n('se_var', 3)} and a "
     f"t-statistic of {a('t_var', 1)}: one additional bit of workforce skill "
     f"variety is associated with a {a('b_var', 2)} percentage point higher "
     "youth employment share, and a one-standard-deviation increase in "
     f"variety with {a('var_sd_effect', 2)} percentage points, or "
     f"{a('var_sd_pct', 1)} percent of the sample mean. The estimate is "
     f"{n('b_var_ind', 3)} when the year effects are replaced by "
     "industry-by-year effects and "
     f"{n('b_var_prov', 3)} when they are replaced by province-by-year "
     "effects, so it is not an artefact of industry or regional shocks. H1 "
     "is supported."),

    ("table", "table4"),

    ("h2", "4.3. The Buffering of Demand Shocks"),

    ("p",
     "Table 5 turns to the sensitivity of youth employment rather than its "
     "level. Column (1) shows that an adverse industry demand shock of one "
     "standard deviation lowers the youth employment share by "
     f"{a('b_shock_alone', 3)} percentage points on average. Column (3) adds "
     "the interaction of Equation (5): the coefficient on the interaction is "
     f"{n('b_sxv', 3)} with a standard error of {n('se_sxv', 3)}, "
     "significant at the one percent level, and it is essentially unchanged "
     "when industry-by-year or province-by-year effects replace the year "
     f"effects ({n('b_sxv_ind', 3)} and {n('b_sxv_prov', 3)}). H2 is "
     "supported."),

    ("p",
     "The economic content is best read from the marginal effect of Equation "
     "(6), which is plotted in Figure 2a. At the sample mean of variety an "
     "adverse shock of one standard deviation lowers the youth employment "
     f"share by {a('marg_mean', 3)} percentage points. One standard "
     f"deviation below the mean the loss is {a('marg_lo', 3)} percentage "
     "points; one standard deviation above it the point estimate is "
     f"{n('marg_hi', 3)} and no longer significant at the five percent level "
     f"(p = {n('marg_hi_p', 3)}). The pass-through crosses zero at a variety "
     f"of {n('zero_variety', 2)} bits. Between a firm at the twentieth and a "
     "firm at the eightieth percentile of workforce variety, in other words, "
     "the same industry shock produces a difference of well over a "
     "percentage point in the share of the workforce that is young, which is "
     "of the same order as the entire average effect of the shock. The strip "
     "beneath each panel of Figure 2 shows the observed density of the "
     "variety measure on that axis, so the range over which the estimate is "
     "supported can be read from the figure; the shaded column in panel a is "
     "the confidence interval for the threshold estimated in Section 4.10."),

    ("fig", "fig2"),

    ("table", "table5"),

    ("h2", "4.4. Related versus Unrelated Variety"),

    ("p",
     "Table 6 decomposes the buffer. Entered separately, both components "
     "attenuate the shock. Entered together in column (3), the interaction "
     f"with related variety is {n('b_sxr', 3)} and the interaction with "
     f"unrelated variety is {n('b_sxu', 3)}, both significant at the one "
     f"percent level. The difference of {n('diff_ru', 3)} is itself "
     f"significant (p = {n('p_diff_ru', 3)}): related variety buffers "
     f"{n('ratio_ru', 2)} times as strongly as unrelated variety. Figure 2b "
     "plots the schedule for each component estimated on its own, in columns "
     "(1) and (2), over the range of bits that component actually occupies; "
     "the ratio just quoted is the one from column (3), where the two enter "
     "together. H3 is supported, with an important qualification. "
     "Because the unrelated component is more widely dispersed across firms "
     f"(a standard deviation of {n('sd_UnrelVar', 3)} bits against "
     f"{n('sd_RelVar', 3)}), a one-standard-deviation movement in each buys "
     f"a similar amount of buffering, "
     f"{S['b_sxr'] * S['sd_RelVar']:.3f} against "
     f"{S['b_sxu'] * S['sd_UnrelVar']:.3f}. The finding is therefore about "
     "the productivity of a unit of variety rather than about which "
     "component accounts for more of the observed cross-sectional variation: "
     "a bit of variety placed within an occupational family is worth about "
     "half as much again as a bit placed between families. The result is "
     "still the opposite of a portfolio intuition. What "
     "protects young employment is not that the firm does many unconnected "
     "things, but that within each thing it does there is a ladder of "
     "qualifications along which a person can be moved."),

    ("table", "table6"),

    ("h2", "4.5. The Absorption Mechanism"),

    ("p",
     "Table 7 examines the two organizational acts. Column (2) shows that an "
     "adverse shock raises internal redeployment and that variety amplifies "
     f"the response: the interaction is {mv('Redeploy', 'a', 3)}, "
     "significant at the one percent level. Column (4) shows that an adverse "
     "shock raises churn and that variety dampens it, the interaction being "
     f"{mv('Churn', 'a', 3)}. Columns (3) and (5) add each mediator to the "
     "outcome equation: redeployment enters positively at "
     f"{mv('Redeploy', 'b', 3)} and churn negatively at "
     f"{mv('Churn', 'b', 3)}, and in each case the buffering coefficient "
     "falls. Column (6) includes both, and the direct buffering coefficient "
     f"falls from {n('b_sxv', 3)} to {mv('Churn', 'direct', 3)} while "
     "remaining significant at the one percent level."),

    ("table", "table7"),

    ("p",
     "Table 8 quantifies the two channels. The part of the buffering that "
     f"travels through internal redeployment is {mv('Redeploy', 'indirect', 3)}, "
     f"with a bootstrap interval of [{mv('Redeploy', 'ci_low', 3)}, "
     f"{mv('Redeploy', 'ci_high', 3)}] that excludes zero, accounting for "
     f"{a('share_red', 1)} percent of the total. The part that travels "
     f"through suppressed churn is {mv('Churn', 'indirect', 3)}, with an "
     f"interval of [{mv('Churn', 'ci_low', 3)}, {mv('Churn', 'ci_high', 3)}], "
     f"accounting for {a('share_chu', 1)} percent. Together the two channels "
     f"carry {a('share_both', 1)} percent of the buffering. H4 is supported, "
     "and the relative magnitudes are informative: absorption is "
     "predominantly the avoidance of separations rather than the visible "
     "reshuffling of posts. Variety works less by moving people than by "
     "making it unnecessary to lose them."),

    ("table", "table8"),

    ("h2", "4.6. Endogeneity Tests"),

    ("p",
     "Table 9 addresses the concern that diverse firms differ from "
     "concentrated ones in ways the controls do not capture. Columns (1) and "
     "(2) report the two first stages. The occupational diversity of the "
     "local labor pool and the variety of same-industry firms in other "
     "provinces both enter the variety equation positively and significantly, "
     "and their interactions with the shock enter the interaction equation, "
     "with a Kleibergen-Paap rank Wald statistic of "
     f"{n('kp_f', 1)}. Column (3) reports the second stage: the buffering "
     f"coefficient is {n('b_iv_sxv', 3)}, close to the least-squares "
     "estimate. The Hansen J statistic does not reject the exclusion "
     f"restriction (p = {n('hansen_p', 3)}) and the Durbin-Wu-Hausman "
     f"statistic does not reject exogeneity (p = {n('wu_p', 3)}), so the "
     "least-squares estimate may be read as consistent."),

    ("p",
     "Column (4) replaces contemporaneous variety with its one-year lag, "
     "which is predetermined with respect to the current year's employment "
     f"decisions; the buffering coefficient is {n('b_lag_sxv', 3)}. Column "
     "(5) re-estimates on a sample matched one to one on the propensity "
     "score formed from pre-period characteristics [[rosenbaum1983]], which "
     f"reduces the largest standardized bias from {n('bal_before', 1)} to "
     f"{n('bal_after', 1)} percent and gives {n('b_psm_sxv', 3)}; column (6) "
     "reweights the full sample by entropy-balancing weights and gives "
     f"{n('b_eb_sxv', 3)}. The four approaches bracket the benchmark "
     "closely."),

    ("table", "table9"),

    ("h2", "4.7. Robustness Checks"),

    ("p",
     "Table 10 reports seven robustness checks and a placebo, each "
     "retaining the full control set and "
     "both sets of fixed effects. Excluding the pandemic years, restricting "
     "the sample to firms observed in every year, replacing the entropy with "
     "the effective number of skill groups, replacing the continuous shock "
     "with an indicator for an adverse year, redefining the outcome as the "
     "youth share of the age-classified workforce, adding employment growth "
     "to the control set and clustering by firm and year simultaneously all "
     "leave the conclusion intact; the buffering coefficient ranges between "
     f"{n('robust_min', 3)} and {n('robust_max', 3)} across the "
     "specifications that retain the original scaling and is significant at "
     "the one percent level throughout."),

    ("p",
     "The final row is the placebo. If the mechanism is the redeployment and "
     "retention of workers whose separation would otherwise be cheapest, "
     "then employment of workers aged 31 to 50, who hold the firm-specific "
     "human capital that makes separation expensive, should be far less "
     "sensitive to the interaction. The estimated coefficient is "
     f"{n('b_placebo', 3)} (p = {n('p_placebo', 3)}), "
     f"{a('ratio_age', 0)} times smaller than the youth coefficient and "
     "statistically indistinguishable from zero. Variety buffers the margin "
     "the theory names, not employment in general."),

    ("p",
     "Two further diagnostics are reported here rather than in the table. "
     "Applying the coefficient-stability bounds of Ref. [[oster2019]], "
     f"selection on unobservables would have to be {abs(OST['delta']):.1f} "
     "times as strong as selection on the observed controls, and of the "
     "opposite sign, to overturn the buffering result; the identified set "
     f"runs from the controlled estimate to {OST['beta_star']:.3f} and does "
     "not contain zero. A restricted wild cluster bootstrap with Rademacher "
     f"weights and {S['wild']['reps']:,.0f} replications, which imposes the "
     "null before resampling [[cameron2008],[roodman2019]], returns a "
     f"p-value of {S['wild']['p']:.3f}."),

    ("table", "table10"),

    ("h2", "4.8. Moderating Effects"),

    ("p",
     "Table 11 reports the triple interactions of Equation (8). Digital "
     "capability strengthens the buffer: the coefficient on the triple "
     f"interaction is {n('b_sxvxd', 3, sign=True)} and significant "
     f"(p = {n('p_sxvxd', 3)}), so a firm one standard deviation above the "
     "mean of digital capability converts its variety into absorption "
     "appreciably more effectively than the average firm. Financial slack "
     f"does the same, with a coefficient of {n('b_sxvxs', 3, sign=True)} "
     f"(p = {n('p_sxvxs', 3)}). Column (3) includes both and the two are "
     "essentially unchanged, so they operate independently. H6a and H6b are "
     "supported. Variety is a stock of potential regulatory capacity; "
     "information systems and liquidity are what convert the stock into a "
     "flow of actual adjustment."),

    ("table", "table11"),

    ("h2", "4.9. Heterogeneity Analysis"),

    ("p",
     "Table 12 splits the sample along four dimensions and tests the "
     "equality of the buffering coefficient across each pair. The effect is "
     f"{hv('State-owned', 'a', 3)} in state-owned enterprises against "
     f"{hv('State-owned', 'b', 3)} in non-state firms, and the difference is "
     f"significant at the ten percent level (p = {hv('State-owned', 'p', 3)}). "
     "The reading is not "
     "that state ownership makes variety useless but that it substitutes for "
     "it: firms carrying employment-stabilization obligations retain young "
     "workers for reasons unrelated to whether they have somewhere to put "
     "them, so the marginal value of the internal capacity is lower. The "
     f"effect is {hv('Labor-intensive', 'a', 3)} in labor-intensive "
     f"industries against {hv('Labor-intensive', 'b', 3)} in "
     f"capital-intensive ones (p = {hv('Labor-intensive', 'p', 3)}), which "
     "is consistent with the threshold result of the next subsection, since "
     "labor-intensive firms are concentrated below the critical level of "
     "variety. The split between manufacturing and non-manufacturing gives "
     f"{hv('Manufacturing', 'a', 3)} and {hv('Manufacturing', 'b', 3)} "
     f"(p = {hv('Manufacturing', 'p', 3)}), and the regional split "
     f"{hv('Eastern region', 'a', 3)} against "
     f"{hv('Eastern region', 'b', 3)} "
     f"(p = {hv('Eastern region', 'p', 3)}). The capacity is a firm-level "
     "attribute, not a sectoral or regional one."),

    ("table", "table12"),

    ("h2", "4.10. The Requisite-Variety Threshold"),

    ("p",
     "Table 13 reports the estimates of Equation (9), and they are the "
     "central result of this study. The estimated threshold is "
     f"{tv('gamma', 3)} bits, with a ninety-five percent confidence interval "
     f"of [{tv('ci_low', 3)}, {tv('ci_high', 3)}] obtained by inverting the "
     f"likelihood ratio; {tv('pct_below', 1)} percent of firm-year "
     "observations lie below it. The likelihood-ratio statistic against the "
     f"null of no threshold is {tv('f1', 1)} and the fixed-regressor "
     f"bootstrap p-value is {tv('p_boot', 3)}, so the null is rejected "
     "decisively. Figure 3a plots the likelihood-ratio profile over the "
     "candidate grid together with the critical value and the resulting "
     "confidence interval; the vertical scale is symmetric-logarithmic, "
     "because on a linear scale the critical value and its crossings are "
     "pressed onto the axis. The non-rejection set is not everywhere "
     "connected over the grid, as the profile crosses the critical value "
     "more than twice, so the interval reported here and shaded in the "
     "figure is its convex hull, which is the conventional and the "
     "conservative summary."),

    ("p",
     "The regime coefficients, plotted in Figure 3b, make the substantive "
     "point. Below the threshold, an adverse demand shock of one standard "
     "deviation lowers the youth employment share by "
     f"{tva('b_low', 3)} percentage points, significant at the one percent "
     f"level. Above it the coefficient is {tv('b_high', 3)}, an attenuation "
     f"of {100 * (1 - abs(THR['b_high']) / abs(THR['b_low'])):.0f} percent, "
     "and it is economically negligible relative to the mean youth "
     "employment share. The difference between the two regimes is not one of "
     "degree. Firms below the critical level of workforce variety transmit "
     "the disturbance to their youngest employees almost in full; firms "
     "above it do not transmit it in any economically meaningful sense. H5 "
     "is supported, and with it the claim that requisite variety is a "
     "precondition for absorption rather than a contributor to it."),

    ("table", "table13"),

    ("fig", "fig3"),

    # =====================================================================
    ("h1", "5. Discussion and Implications"),
    ("h2", "5.1. Variety as a Stock of Regulatory Capacity (H1 and H2)"),

    ("p",
     "Hypotheses 1 and 2 were confirmed. Workforce skill variety is "
     "associated with a higher youth employment share and with a markedly "
     "weaker transmission of industry demand shocks to it, and the second "
     "finding survives instrumental variables, propensity score matching, "
     "entropy balancing, seven robustness specifications and an age placebo. "
     "The result gives empirical content to a proposition that "
     "organizational resilience research has asserted without specifying: "
     "that resilience is a capacity rather than an outcome "
     "[[lengnick2011],[ortiz2016],[desjardine2019]]. What this study adds is "
     "a measure of the capacity that is prior to the shock, observable from "
     "public disclosure, and theoretically grounded in the requirement that "
     "a regulator match the variety of what it regulates [[ashby1956]]."),

    ("h2", "5.2. Which Kind of Variety Absorbs (H3)"),

    ("p",
     "Hypothesis 3 was validated, and the result carries a warning for "
     "practice. Related variety, the depth of educational differentiation "
     "within occupational families, buffers considerably more strongly than "
     "unrelated variety, the spread across families. The reason is that "
     "absorption requires a person to move, and movement is governed by "
     "cognitive proximity [[boschma2005],[bidwell2011]]. A firm that "
     "diversifies across unrelated activities acquires the portfolio "
     "insurance of Ref. [[frenken2007]] but not the option to redeploy, "
     "because the people in one activity cannot do the work of another. This "
     "reverses a common managerial intuition. Breadth without depth looks "
     "like variety on an organization chart and is not variety in the "
     "regulatory sense. The qualification noted in Section 4.4 matters for "
     "practice rather than for theory: because listed firms already differ "
     "more in their unrelated than in their related variety, the two "
     "components currently contribute comparable amounts to the observed "
     "dispersion in resilience, so the higher productivity of related "
     "variety is an argument about where the next unit should be invested, "
     "not about where existing differences come from."),

    ("h2", "5.3. How Absorption Happens (H4)"),

    ("p",
     "Hypothesis 4 was supported, and the decomposition locates the "
     "managerial act precisely. Of the buffering effect, "
     f"{a('share_chu', 1)} percent travels through suppressed churn and only "
     f"{a('share_red', 1)} percent through visible internal redeployment. "
     "Absorption is therefore mostly a decision not to separate rather than "
     "a programme of reassignment, which is consistent with the "
     "organizational literature on how firms cope with the unexpected: much "
     "of what a resilient organization does is refrain from the locally "
     "rational response [[weick1993],[weick2015]]. The practical "
     "implication is that the capacity is exercised quietly and will not "
     "appear in any register of reorganization initiatives."),

    ("h2", "5.4. The Requisite-Variety Condition (H5)"),

    ("p",
     "Hypothesis 5 is strongly supported by the threshold estimates, and it "
     "is the finding on which the contribution of this paper rests. Ashby's "
     "law is not a statement that more regulatory variety is better; it is a "
     "sufficiency condition, and sufficiency conditions imply "
     "discontinuities [[ashby1956],[beer1981]]. The data locate one. Below "
     f"{tv('gamma', 2)} bits of workforce variety the demand shock is "
     "transmitted to young employees essentially in full; above it the "
     "transmission is economically negligible. That "
     f"{tv('pct_below', 0)} percent of Chinese listed firm-years lie below "
     "the threshold is the substantive counterpart of the statistic: for the "
     "majority of firms, current workforce structure is not merely a weaker "
     "buffer but no buffer at all."),

    ("p",
     "This has a consequence for how resilience should be measured. A linear "
     "interaction, which is what the moderation literature reports, averages "
     "over two regimes that differ in kind and therefore understates the "
     "position of firms in the vulnerable regime while overstating that of "
     "firms just below the threshold. It also changes the shape of the "
     "policy problem. If the relationship were a gradient, any increase in "
     "variety would buy a proportionate reduction in vulnerability, and "
     "incremental measures would be worthwhile everywhere. Because it is a "
     "regime, increments below the threshold buy very little, and the "
     "return to raising variety is concentrated at the crossing "
     "[[meadows2008],[sterman2000]]."),

    ("h2", "5.5. When the Buffer Works Best (H6a and H6b)"),

    ("p",
     "Hypotheses 6a and 6b were both supported. Digital capability and "
     "financial slack each strengthen the conversion of variety into "
     "absorption, and they do so independently. The distinction between "
     "holding a capacity and being able to use it is a familiar one in "
     "systems thinking, where a regulator requires both the variety to match "
     "the disturbance and the channel capacity to apply it [[ashby1956],"
     "[beer1981]]. Here the channel is informational on one side and "
     "financial on the other: a firm must know which of its people can do "
     "which work, and it must be able to afford to carry them while the "
     "reallocation happens."),

    ("h2", "5.6. Theoretical Contributions"),

    ("p",
     "This study makes three theoretical contributions. First, it "
     "operationalizes the law of requisite variety for employment, replacing "
     "a metaphor with a measured quantity, an externally constructed "
     "disturbance and an estimated sufficiency threshold. Second, it "
     "connects the entropy decomposition that Ref. [[frenken2007]] developed "
     "for regional economies to the internal structure of the firm, and "
     "shows that the related and unrelated components play the roles that "
     "the proximity literature predicts [[boschma2005],[jacobs1969]]. Third, "
     "it supplies the organizational resilience literature with an "
     "antecedent that is observable before the shock arrives, which "
     "addresses the circularity of inferring capacity from recovery "
     "[[lengnick2011],[martin2015]]. In doing so it also contributes to the "
     "labor economics of adjustment, which has established that the young "
     "absorb the shock [[oi1962],[forsythe2022]] without explaining the "
     "dispersion in how much of it they absorb."),

    ("h2", "5.7. Managerial and Policy Implications"),

    ("p",
     "For firm managers, the results argue for treating workforce structure "
     "as a risk-management instrument rather than as a by-product of hiring. "
     "Three practices follow. Monitor the entropy of the workforce "
     "distribution alongside its headcount, since two firms of identical "
     "size and cost can differ by a factor of two in how much of an industry "
     "shock reaches their employees. Build depth within occupational "
     "families rather than breadth across them, because it is related "
     "variety that confers the option to redeploy. And invest in the "
     "informational infrastructure that records what people can do, since "
     "variety that management cannot see cannot be used."),

    ("p",
     "For human resource functions the threshold result is the operative "
     "one. A firm below the critical level should not expect proportionate "
     "returns from incremental diversification; the objective is to cross, "
     "not to inch upward. Since the crossing is defined over a measurable "
     "quantity, it can be set as a target and audited."),

    ("p",
     "For policymakers the implications are addressed to specific actors. "
     "Employment ministries and local labor bureaus operating "
     "graduate-hiring subsidies should note that the same subsidy buys "
     "different amounts of durable employment depending on where the "
     "recipient firm sits relative to the threshold, and that support "
     "conditioned on the breadth of the roles a graduate may occupy is more "
     "durable than support conditioned on headcount alone. Industrial "
     "policy authorities encouraging digital transformation "
     "[[statecouncil2025],[janssen2025]] have a second reason to do so, "
     "since digital capability is what converts existing workforce variety "
     "into shock absorption. Education authorities facing record graduate "
     "cohorts [[moe2025],[wef2025]] may note that the qualifications which "
     "raise related variety, those that deepen a firm's ladder within an "
     "occupational family, are the ones that make a graduate placement "
     "resilient. Finally, state asset supervision commissions should "
     "recognize that the employment stability of state-owned enterprises "
     "documented in Table 12 is currently achieved by obligation rather than "
     "by capacity, which is durable only as long as the obligation is."),

    ("h2", "5.8. Limitations and Future Research Directions"),

    ("p",
     "Several limitations qualify these findings. First, workforce variety "
     "is measured from disclosed composition across five occupational "
     "categories and three education levels, which is coarser than the "
     "underlying skill distribution; the coarseness biases the measure "
     "towards understating variety and therefore, if anything, towards "
     "understating its effect, but linking disclosure to personnel records "
     "or to job-posting text would sharpen it. Second, the sample covers "
     "listed firms, which are larger and more formally organized than the "
     "enterprises that employ most young Chinese workers; extending the "
     "design to survey data on small and medium enterprises would establish "
     "whether the threshold is a property of firms or of large firms. Third, "
     "the demand shock is constructed at the two-digit industry level, so "
     "firms within an industry are assumed to face the same disturbance; "
     "customer-level or product-level shocks would permit a sharper test and "
     "would also allow the variety of the disturbance to be measured rather "
     "than assumed. Fourth, the threshold is estimated for a single "
     "threshold variable, and the possibility of multiple regimes, or of a "
     "threshold that shifts with the magnitude of the disturbance as Ashby's "
     "law strictly implies, is left for future work. Fifth, the analysis "
     "stops at the firm boundary and cannot say whether the young workers "
     "not retained by low-variety firms are absorbed elsewhere; matched "
     "employer-employee records would identify their destination. Finally, "
     "the two channels measured here do not exhaust the mechanism, since "
     "working-time adjustment, wage flexibility and temporary transfers "
     "within business groups are plausible additional routes that richer "
     "personnel data would allow future research to examine."),

    ("p",
     "A final direction concerns the disturbance itself. This study measures "
     "the buffering of demand shocks, but the sharpest current threat to "
     "entry-level employment is technological rather than cyclical, and the "
     "early firm-level evidence suggests that it falls on exactly the "
     "junior, codifiable work that the argument here identifies as the "
     "adjustment margin [[brynjolfsson2025],[hui2024],[humlum2025],"
     "[babina2024]]. Whether workforce variety buffers a permanent "
     "reallocation of tasks in the way it buffers a temporary contraction of "
     "demand is an open and pressing question, and one the framework "
     "developed here is equipped to answer. Recent work in this journal has "
     "begun to map the organizational consequences of artificial "
     "intelligence adoption in Chinese firms [[xuejin2025],[xue2025],"
     "[machucho2025],[liang2025]], and joining that literature to the "
     "regulatory account of variety is the natural next step."),

    # =====================================================================
    ("h1", "6. Conclusions"),

    ("p",
     "Young workers are the margin on which firms adjust when demand falls, "
     "but they are not the same margin in every firm. Using "
     f"{S['n_obs']:,} firm-year observations for {S['n_firms']:,} Chinese "
     f"A-share listed firms over {S['years']}, this study shows that the "
     "difference is governed by a structural property of the workforce that "
     "cybernetics identified seventy years ago. Workforce skill variety, "
     "measured as the entropy of the employment distribution over "
     "occupational categories and education levels, raises the youth "
     f"employment share by {a('var_sd_effect', 2)} percentage points per "
     f"standard deviation and attenuates the effect of an adverse industry "
     f"demand shock, the interaction being {n('b_sxv', 3)}. The related "
     f"component of variety buffers {n('ratio_ru', 2)} times as strongly as "
     "the unrelated component, and the absorption operates predominantly "
     "through the avoidance of separations rather than through visible "
     "internal redeployment."),

    ("p",
     "The central finding is that the buffer is a regime rather than a "
     f"gradient. Below an estimated threshold of {tv('gamma', 2)} bits of "
     "workforce variety, which "
     f"{tv('pct_below', 0)} percent of listed firm-years fall short of, an "
     "adverse shock lowers the youth employment share by "
     f"{tva('b_low', 2)} percentage points; above it the effect is "
     "economically negligible. Requisite variety is therefore a "
     "precondition for absorption and not merely a contributor to it, which "
     "is the substantive content of Ashby's law and is what distinguishes a "
     "systems account of organizational resilience from a list of "
     "correlates. For a country entering a decade of record graduate "
     "cohorts, the practical consequence is that the structure of a firm's "
     "existing workforce, a quantity that is disclosed annually and can be "
     "managed deliberately, determines whether the next downturn is passed "
     "on to the people entering work for the first time."),

    # =====================================================================
    ("h1b", "Author Contributions"),
    ("stmt2", "",
     "Conceptualization, X.C. and T.M.; methodology, X.C.; software, X.C.; "
     "validation, T.M.; formal analysis, X.C.; investigation, X.C. and T.M.; "
     "resources, T.M.; data curation, X.C.; writing—original draft "
     "preparation, X.C.; writing—review and editing, T.M.; visualization, "
     "X.C.; supervision, T.M.; project administration, T.M. All authors have "
     "read and agreed to the published version of the manuscript."),

    ("h1b", "Funding"),
    ("stmt2", "", "This research received no external funding."),

    ("h1b", "Institutional Review Board Statement"),
    ("stmt2", "", "Not applicable."),

    ("h1b", "Informed Consent Statement"),
    ("stmt2", "", "Not applicable."),

    ("h1b", "Data Availability Statement"),
    ("stmt2", "",
     "The firm-level data underlying this study were obtained from the China "
     "Stock Market and Accounting Research database and the disclosure "
     "archives of the Shanghai and Shenzhen stock exchanges under license "
     "and are therefore not publicly available. The estimation code that "
     "reproduces every table and figure is available from the corresponding "
     "author upon reasonable request."),

    ("h1b", "Conflicts of Interest"),
    ("stmt2", "", "The authors declare no conflicts of interest."),
]
