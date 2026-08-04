# -*- coding: utf-8 -*-
"""Manuscript text.

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
PV = S["pvar"]
PV2 = S["pvar2"]


def n(key, d=3, sign=False):
    return ("%+.*f" if sign else "%.*f") % (d, S[key])


def a(key, d=3):
    return "%.*f" % (d, abs(S[key]))


def hv(z, field, d=3):
    return "%.*f" % (d, HET[z][field])


def hva(z, field, d=3):
    return "%.*f" % (d, abs(HET[z][field]))


def mv(z, field, d=3):
    return "%.*f" % (d, MED[z][field])


def mva(z, field, d=3):
    return "%.*f" % (d, abs(MED[z][field]))


def gc(eq, cause, field, d=3):
    return "%.*f" % (d, PV["gc"]["%s<-%s" % (eq, cause)][field])


def gca(eq, cause, field, d=3):
    return "%.*f" % (d, abs(PV["gc"]["%s<-%s" % (eq, cause)][field]))


TITLE = ("Eroding the First Rung: Generative Artificial Intelligence, "
         "Organizational Learning, and the Self-Reinforcing Decline of Youth "
         "Employment in Chinese Listed Firms")

AUTHORS = [("Xinyu Cai ", False), ("1", True), (" and Tiantian Mo ", False),
           ("1,*", True)]

AFFILIATIONS = [
    ("1", "College of Business, Jiaxing University, Jiaxing 314001, China; "
          "caixinyu@zjxu.edu.cn"),
    ("*", "Correspondence: 00008227@zjxu.edu.cn"),
]

ABSTRACT = (
    "Entry-level work is the first rung of the workforce development ladder, "
    "and generative artificial intelligence is now most capable at precisely "
    "the tasks that rung is made of. This study examines how the adoption of "
    "generative artificial intelligence by firms reshapes the youth "
    "employment share, and asks whether the effect is a one-way shock or a "
    "self-reinforcing loop within the firm's socio-technical system of skill "
    "formation. The analysis uses "
    f"{S['n_obs']:,} firm-year observations for {S['n_firms']:,} Chinese "
    f"A-share listed firms over {S['years']}, with generative-AI application "
    "intensity measured from annual-report text. A two-way fixed-effects "
    "panel model is estimated as the benchmark, three-step mediation with "
    "firm-block bootstrapping identifies the transmission channels, "
    "instrumental variables, propensity score matching and entropy balancing "
    "address endogeneity, and a bias-corrected panel vector autoregression "
    "with orthogonalized impulse responses tests the feedback structure. A "
    f"one-standard-deviation increase in adoption lowers the youth employment "
    f"share by {a('effect_sd', 2)} percentage points, or "
    f"{a('effect_sd_pct', 1)} percent of its mean, while employment of workers "
    "aged 31 to 50 is barely affected. Falling training investment and a "
    f"contracting routine task base jointly account for "
    f"{a('share_both', 1)} percent of the total effect. The effect is weaker "
    "where organizational learning capability is stronger and sharper where "
    "relative labor costs are higher. Critically, the erosion feeds back: "
    "weaker training and a smaller youth share raise subsequent adoption, and "
    f"this reinforcing loop amplifies the eight-year cumulative "
    f"displacement by {100 * (S['amp'] - 1):.0f} percent. Policy should therefore target the loop rather "
    "than the shock.")

KEYWORDS = ("generative artificial intelligence; youth employment; "
            "organizational learning; socio-technical systems; feedback loop; "
            "capability trap; workforce development; panel vector "
            "autoregression")

# ---------------------------------------------------------------------------
BLOCKS = [
    ("h1", "1. Introduction"),

    ("p",
     "Youth employment has become one of the most closely watched indicators "
     "of economic health in the world's large economies, and it is "
     "deteriorating faster than any other segment of the labor market. The "
     "International Labour Organization reports that young people constitute "
     "roughly one-sixth of the global working-age population but close to "
     "two-fifths of the unemployed, and that their labor force participation "
     "fell more than three times as fast as that of the working-age "
     "population as a whole over the past decade [[ilo2025]]. In China the "
     "pressure is acute. The number of new college graduates reached 12.22 "
     "million in 2025, the highest on record [[moe2025]], while the surveyed "
     "urban unemployment rate of the population aged 16 to 24 excluding "
     "students remained above 17 percent through much of the year, more than "
     "three times the national rate [[nbs2025]]. The scale of the cohort and "
     "the persistence of the gap have made the absorption of young workers a central objective of industrial and employment policy [[ilo2024],[wef2025]]. "
     "What is at stake is not only the current year of joblessness. Cohorts that "
     "enter the labor market in slack conditions carry measurable earnings and "
     "employment penalties for a decade or more, and the penalty is largest for "
     "those who never secure a first foothold [[kahn2010],[oreopoulos2012],"
     "[schwandt2019],[vonwachter2020]]."),

    ("p",
     "Over the same period the technological environment facing firms changed "
     "abruptly. Generative artificial intelligence, which produces language, "
     "code and images rather than merely classifying them, moved from "
     "laboratory demonstration to routine workplace tool within two years of "
     "the release of large conversational models [[bick2024]]. Its capability "
     "profile is unusual. Field and experimental evidence shows that "
     "generative models raise the productivity of writing, customer support, "
     "consulting and software work substantially, and that the gains are "
     "largest for the least experienced workers, whose output moves closest "
     "to that of their more senior colleagues [[brynjolfsson2025],[noy2023],"
     "[dellacqua2026],[peng2023]]. Task-level exposure measures point in the "
     "same direction: the occupations most exposed are cognitive and "
     "white-collar rather than manual, and within them the most exposed tasks "
     "are the codifiable, supervised ones that junior staff are normally "
     "hired to perform [[eloundou2024],[felten2021]]. Early aggregate "
     "evidence is consistent with a distributional consequence. Employment of "
     "workers aged 22 to 25 in the most exposed occupations has declined "
     "relative to that of experienced workers in the same occupations, while "
     "senior employment has not [[canaries2025],[liu2025]]."),

    ("p",
     "Existing scholarship reads this as a labor demand problem. In the "
     "task-based framework, a technology that automates a set of tasks "
     "displaces the labor previously allocated to them and, where it also "
     "creates new tasks, reinstates demand elsewhere [[acemoglu2018],"
     "[acemoglu2022],[autor2024]]. Because generative models are a "
     "general-purpose technology whose complementary investments arrive "
     "with a lag, the composition of the adjustment may differ sharply "
     "from its eventual level [[bresnahan1995],[agrawal2019],"
     "[jcurve2021]]. Applied to generative artificial "
     "intelligence, this yields a clear and testable prediction about the "
     "level of entry-level hiring, and firm-level studies in several "
     "countries have begun to confirm it [[babina2024],[hui2024],"
     "[humlum2025]]. Yet the framework treats the firm's technology choice as "
     "exogenous to the composition of its workforce, and treats each year's "
     "adjustment as independent of the last. Neither assumption is innocuous "
     "when the resource being displaced is the input to the firm's own future "
     "capability."),

    ("p",
     "Entry-level positions are not only jobs; they are the mechanism by "
     "which firms manufacture the experienced workers they will need later. "
     "Human capital theory and the literature on internal labor markets "
     "describe a ladder along which workers acquire task-specific and "
     "firm-specific skill through supervised practice, and along which the "
     "firm recovers its training outlay in later periods [[becker1964],"
     "[doeringer1971],[gibbons2004],[acemoglu1998]]. Organization theory adds "
     "that this ladder is also the firm's absorptive capacity: the stock of "
     "people able to recognize, assimilate and apply new external knowledge "
     "[[cohen1990],[argote2011]]. When a technology substitutes for the "
     "bottom rung, the firm does not simply buy the same output more cheaply. "
     "It stops producing an input it cannot buy on the market, and it does so "
     "in a period in which the consequence is invisible because the existing "
     "stock of experienced staff still suffices."),

    ("p",
     "This is the structure that system dynamics calls a capability trap. "
     "Repenning and Sterman [[repenning2002]] showed that when a short-run "
     "fix and a long-run capability investment compete for the same "
     "resources, and when the returns to the investment are delayed, "
     "organizations reliably choose the fix, thereby degrading the capability "
     "that would have reduced the need for the fix, and so raising the pull "
     "toward the fix again in the next period. Rahmandad and Repenning "
     "[[rahmandad2016]] formalized the resulting erosion dynamics; Levinthal "
     "and March [[levinthal1993]] described the same pathology as the myopia "
     "of learning. The behavior is not irrational at any single decision "
     "point. It is the emergent property of a reinforcing loop with a delay, "
     "and it is invisible to any analysis that estimates one arrow of the loop at "
     "a time. This is the sense in which the firm is a complex adaptive "
     "system rather than a production function: its behavior over time is "
     "generated by the interaction of its parts, not by any of them "
     "separately [[bertalanffy1968],[holland1995]]. Socio-technical systems theory makes the same "
     "structural claim in different language: a technical subsystem and a "
     "social subsystem are jointly optimized or jointly degraded, and an "
     "intervention in one that ignores the other produces outcomes that "
     "neither designer intended [[trist1951],[emery1965]]."),

    ("p",
     "Although existing studies have thoroughly documented the exposure of "
     "young workers to generative artificial intelligence and the "
     "productivity gains the technology delivers, they have predominantly "
     "treated the relationship as a unidirectional shock running from "
     "technology to employment, neglecting the possibility that the "
     "employment response itself changes the firm's subsequent technology "
     "choice. Three gaps follow. First, the mechanisms are asserted rather "
     "than measured: displacement is attributed to task substitution without "
     "a test of whether the firm's investment in skill formation also falls. "
     "Second, the moderating role of the firm's own learning capability is "
     "rarely examined, even though it is the most obvious leverage point for "
     "management. Third, and most importantly, no firm-level study has "
     "estimated the return arc of the loop, so the literature cannot say "
     "whether the observed displacement is a level shift that will exhaust "
     "itself or a self-reinforcing process that accumulates."),

    ("p",
     "Based on this, this study uses a sample of Chinese A-share listed firms "
     f"over {S['years']} to examine how generative artificial intelligence "
     "adoption reshapes the youth employment share, why it does so, what "
     "conditions the effect, and whether it feeds back on itself. Adoption "
     "intensity is measured from annual-report text; the youth employment "
     "share is taken from the disclosed age structure of the workforce; "
     "training expenditure per employee and the routine task base serve as "
     "the two mediators; research and development intensity and relative "
     "labor cost serve as the two moderators. The benchmark is a two-way "
     "fixed-effects panel model. Mechanisms are identified by three-step "
     "mediation with firm-block bootstrapped indirect effects. Endogeneity is "
     "addressed by an overidentified instrumental-variable design, propensity "
     "score matching and entropy balancing. The feedback structure is "
     "estimated by a bias-corrected panel vector autoregression with Granger "
     "causality tests, a stability check and orthogonalized impulse "
     "responses, from which the amplification attributable to the loop is "
     "computed by comparing the closed system with a counterfactual system in "
     "which the return arcs are switched off."),

    ("p",
     "Accordingly, this study makes marginal contributions in the following "
     "aspects. First, it moves the analysis of generative artificial "
     "intelligence and youth employment from a unidirectional treatment "
     "effect to a feedback structure, and provides what appears to be the "
     "first firm-level estimate of the return arc that closes the loop, "
     "together with a quantification of how much the loop adds to the "
     "cumulative displacement. Second, it opens the mechanism, showing that "
     "the erosion of the firm's skill-formation investment is a distinct and "
     "measurable channel alongside the task-substitution channel that the "
     "task-based framework emphasizes, and thereby connects the labor "
     "economics of automation to the organizational learning literature. "
     "Third, it identifies organizational learning capability as a leverage "
     "point in the systems sense: the same technology, adopted at the same "
     "intensity, displaces markedly less youth employment in firms that have "
     "built the capacity to absorb it, which turns an apparently "
     "technological outcome into a manageable one. Fourth, it supplies "
     "evidence from the largest developing labor market at a moment when the "
     "policy question is live, and translates the estimates into leverage "
     "points that firms and regulators can act on."),

    ("p",
     "The remainder of this paper proceeds as follows. Section 2 reviews the "
     "related literature and develops the hypotheses. Section 3 describes the "
     "materials and methods, while Section 4 presents the empirical results. "
     "Section 5 discusses the findings and their implications, and, finally, "
     "Section 6 concludes."),

    # =====================================================================
    ("h1", "2. Literature Review and Hypothesis Development"),
    ("h2", "2.1. Generative Artificial Intelligence and the Demand for "
           "Entry-Level Labor"),

    ("p",
     "The task-based framework treats production as a continuum of tasks "
     "allocated between capital and labor, so that a technology which "
     "automates a range of tasks reduces the labor demanded at given wages "
     "unless it simultaneously creates new tasks in which labor holds the "
     "comparative advantage [[acemoglu2018],[acemoglu2022],[autor2015]]. The "
     "framework has organized a large body of evidence on earlier waves of "
     "automation. Ref. [[acemoglu2020]] found that each additional industrial "
     "robot per thousand workers reduced the employment-to-population ratio "
     "in exposed United States commuting zones, and Ref. [[bonfiglioli2024]] "
     "documented similar firm-level adjustments following robot imports. Ref. "
     "[[autor2003]] established the prior result on which this literature "
     "rests, namely that computerization substitutes for routine tasks and "
     "complements non-routine analytic ones."),

    ("p",
     "Generative artificial intelligence inverts part of that pattern. Ref. "
     "[[eloundou2024]] estimated that roughly four-fifths of the United "
     "States workforce could have at least a tenth of their work tasks "
     "affected by large language models, and that exposure rises rather than "
     "falls with education and wages. Ref. [[felten2021]] reached a "
     "comparable ranking of occupational exposure using a different mapping "
     "of model capabilities to work activities. What the exposed tasks share "
     "is not manual repetition but codifiability: drafting standard "
     "correspondence, summarizing documents, writing boilerplate code, "
     "conducting preliminary research and preparing first-pass analysis. "
     "These are the tasks that firms customarily assign to new entrants, "
     "partly because they are valuable and partly because performing them "
     "under supervision is how entrants learn [[beane2019],[kellogg2020]]."),

    ("p",
     "The productivity evidence sharpens the implication. Ref. "
     "[[brynjolfsson2025]] found that a generative assistant deployed to more "
     "than five thousand customer support agents raised resolutions per hour "
     "by about fourteen percent, with gains concentrated among novice and "
     "low-skilled agents and no measurable gain for the most experienced. "
     "Ref. [[noy2023]] and Ref. [[dellacqua2026]] reported the same "
     "compression of the performance distribution in writing and consulting "
     "tasks, and Ref. [[peng2023]] in software development; Refs. "
     "[[cui2026]] and [[otis2026]] report the same compression in three "
     "field experiments with software developers and among Kenyan "
     "entrepreneurs respectively. A technology that "
     "raises the output of a novice toward that of an expert lowers the price "
     "the firm is willing to pay for novices, because what the firm was "
     "purchasing was partly the option on the expert the novice would become "
     "[[raisch2021],[krakowski2023]]. Consistent with this reading, Ref. "
     "[[canaries2025]] documented a relative decline in employment among "
     "workers aged 22 to 25 in the most exposed occupations after generative "
     "models diffused, with no corresponding decline for experienced workers, "
     "and Ref. [[liu2025]] found weakening entry-level vacancy postings in "
     "exposed occupations across several developing economies. Firm-level "
     "studies of adoption report reduced junior hiring without measurable "
     "effects on senior headcount [[hui2024],[humlum2025],[babina2024]]. "
     "The asymmetry is not new to generative models: Ref. [[forsythe2022]] "
     "showed that firms adjust to adverse conditions primarily by suspending "
     "entry-level recruitment rather than by dismissing incumbents, so the "
     "entry port is the margin that moves first. Work in this journal has "
     "begun to trace the organizational consequences of artificial-intelligence "
     "adoption in Chinese firms along adjacent dimensions [[xuejin2025],"
     "[xue2025],[machucho2025],[liang2025]]. "
     "Therefore, the following hypothesis is proposed:"),

    ("hyp", "H1.", "Generative artificial intelligence adoption reduces the "
                   "youth employment share of the adopting firm."),

    ("h2", "2.2. The Training Channel: Adoption and the Erosion of "
           "Skill-Formation Capability"),

    ("p",
     "Why a firm hires young workers is not the same question as what young "
     "workers produce. In the human capital tradition, the firm bears part of "
     "the cost of general and specific training and recovers it from the "
     "wedge between later productivity and later wages, a wedge that "
     "imperfect labor markets sustain [[becker1964],[acemoglu1998],"
     "[acemoglu1999]]. In the internal labor market tradition, entry ports "
     "and promotion ladders are institutional devices for producing skill "
     "that cannot be purchased ready-made [[doeringer1971],[lazear2009]]. "
     "Both traditions imply that the firm's demand for entrants is derived "
     "not only from current tasks but from an anticipated future stock of "
     "experienced staff."),

    ("p",
     "Generative artificial intelligence disturbs this calculation from two "
     "sides. On the benefit side, if a model performs the entrant's current "
     "tasks, the marginal product that the training investment is meant to "
     "raise is smaller, so the expected return on training falls. On the cost "
     "side, the model offers an immediate and certain saving whereas training "
     "yields an uncertain and delayed one; under the standard discounting of "
     "delayed and uncertain returns, the immediate fix dominates "
     "[[levinthal1993],[march1991]]. The prediction is that adoption reduces "
     "the firm's own investment in employee training, and that the reduction "
     "in turn depresses the youth employment share, because a firm that is no "
     "longer investing in skill formation has correspondingly less reason to "
     "hold the people who were to be formed. Recent evidence on deskilling "
     "and reskilling pathways under artificial intelligence is consistent "
     "with the first link [[yang2026],[beane2019]], while the literature on "
     "learning by doing and on the accumulation of organizational capability "
     "supports the second [[arrow1962],[argote2011],[nelson1982]]. In "
     "summary, this paper proposes the following hypothesis:"),

    ("hyp", "H2.", "Generative artificial intelligence adoption reduces the "
                   "youth employment share by suppressing the firm's "
                   "investment in employee training."),

    ("h2", "2.3. The Task Channel: Adoption and the Contraction of the "
           "Routine Task Base"),

    ("p",
     "The second channel is the one the task-based framework describes "
     "directly. Entry-level positions are disproportionately composed of "
     "codifiable, supervised and repeatable work, and it is this portion of "
     "the firm's task portfolio that generative models absorb first "
     "[[autor2003],[eloundou2024],[acemoglu2022jole]]. As the routine share "
     "of the firm's occupational structure contracts, the number of positions "
     "into which an inexperienced worker can be placed at all contracts with "
     "it, independently of any decision about training budgets. The two "
     "channels are therefore conceptually distinct: the first operates "
     "through the firm's willingness to invest in people, the second through "
     "the availability of work those people could do. Evidence from online "
     "vacancy postings shows that establishments exposed to artificial "
     "intelligence restructure their advertised task bundles rather than "
     "simply posting fewer vacancies [[acemoglu2022jole]], which is the "
     "observable signature of this channel. Therefore, the following "
     "hypothesis is proposed:"),

    ("hyp", "H3.", "Generative artificial intelligence adoption reduces the "
                   "youth employment share by contracting the routine task "
                   "base that entry-level positions occupy."),

    ("h2", "2.4. Organizational Learning Capability and Relative Labor Cost "
           "as Boundary Conditions"),

    ("p",
     "If the displacement of entry-level labor were purely technological, it "
     "would be uniform across firms adopting at the same intensity. Systems "
     "thinking suggests otherwise: the same technical subsystem produces "
     "different outcomes depending on the social subsystem it is embedded in "
     "[[trist1951],[emery1965],[checkland1981]]. The relevant property of the "
     "social subsystem here is the firm's capacity to recognize, assimilate "
     "and apply new knowledge, which Cohen and Levinthal [[cohen1990]] termed "
     "absorptive capacity and which the dynamic capabilities literature "
     "treats as the firm's ability to reconfigure its resource base "
     "[[teece1997],[nelson1982]]. A firm with high absorptive capacity has an "
     "alternative to substitution: it can redeploy junior labor toward the "
     "complementary tasks that the technology creates, such as prompt design, "
     "output verification, data curation and the integration of model output "
     "into existing workflows [[raisch2021],[autorai2024],[vaccaro2024]]. A "
     "firm without that capacity has only the substitution margin available."),

    ("p",
     "The opposing boundary condition is the relative price of the labor "
     "being replaced. Where the firm's wage bill per employee is high "
     "relative to the sector, the saving from substituting a model for an "
     "entry-level worker is correspondingly larger, so factor prices sharpen "
     "the incentive to substitute rather than to redeploy [[acemoglu2018],"
     "[bloom2007]]. The two conditions are therefore expected to work in "
     "opposite directions. In line with this, the following hypotheses are "
     "developed:"),

    ("hyp", "H4a.", "The negative effect of generative artificial "
                    "intelligence adoption on the youth employment share is "
                    "weaker in firms with stronger organizational learning "
                    "capability."),
    ("hyp", "H4b.", "The negative effect of generative artificial "
                    "intelligence adoption on the youth employment share is "
                    "stronger in firms facing higher relative labor costs."),

    ("h2", "2.5. Closing the Loop: The Capability Trap as a Reinforcing "
           "Feedback Structure"),

    ("p",
     "The four hypotheses stated so far describe a chain that runs in one "
     "direction. The systems claim of this paper is that the chain is not "
     "open. Consider what the firm observes one period after adoption. Its "
     "training expenditure is lower, its entry cohort is smaller, and "
     "therefore the internal supply of workers able to perform the tasks that "
     "juniors used to perform has begun to thin. The immediate managerial "
     "response to a thinner internal supply is to lean harder on the "
     "technology that made the thinning tolerable, because the alternative, "
     "rebuilding the cohort and the training system, has a delay attached to "
     "it that the substitution does not [[repenning2002],[sterman2000]]. The "
     "return arc therefore carries a negative sign in both directions: lower "
     "training and a lower youth share at $t-1$ raise adoption at $t$, which "
     "lowers training and the youth share again."),

    ("p",
     "This structure is a reinforcing loop with a delay, and its behavior "
     "differs qualitatively from that of a one-off shock. A shock produces a "
     "level shift that decays at the rate of the system's own mean reversion. "
     "A reinforcing loop feeds part of each period's displacement back into "
     "the driver, so the cumulative response exceeds the sum of the impulse "
     "responses that would be observed if the return arcs were absent "
     "[[forrester1961],[meadows2008],[senge1990]]. Whether the loop is "
     "explosive or merely amplifying is an empirical question about the "
     "product of the gains around the circuit, which is why the eigenvalues "
     "of the estimated system carry substantive rather than merely technical "
     "meaning [[sims1980],[love2006]]. Two implications follow that no "
     "one-directional design can deliver: the total effect of adoption on "
     "youth employment is larger than any single-equation estimate of it, and "
     "the effective leverage point is the return arc rather than the initial "
     "adoption decision [[meadows2008],[ashby1956]]. Accordingly, this paper "
     "proposes the following hypothesis:"),

    ("hyp", "H5.", "The erosion of the skill-formation subsystem feeds back "
                   "on technology choice: lower training investment and a "
                   "lower youth employment share raise subsequent generative "
                   "artificial intelligence adoption, so that the "
                   "adoption-capability-youth system contains a reinforcing "
                   "loop that amplifies the cumulative displacement."),

    ("h2", "2.6. Research Gap and Contribution"),

    ("p",
     "Despite the rapid accumulation of evidence on generative artificial "
     "intelligence and work, significant gaps remain. First, most existing "
     "analyses estimate an average effect of exposure or adoption on "
     "employment without opening the firm-level mechanism, so it is not known "
     "whether displacement operates through the availability of tasks, "
     "through the willingness to invest in people, or through both. Second, "
     "the boundary conditions of the effect are rarely modeled, which leaves "
     "the impression that the outcome is a technological inevitability rather "
     "than the joint product of a technical and a social subsystem. Third, "
     "the feedback from the employment outcome back to the technology "
     "decision is not estimated anywhere in the firm-level literature, even "
     "though the systems and organizational learning traditions predict it "
     "and even though its presence changes the magnitude of the total effect. "
     "To bridge these gaps, this study combines a conventional panel design "
     "with an explicitly dynamic system estimator, tests both mechanisms and "
     "both boundary conditions within a single sample, and measures the "
     "amplification attributable to the loop by comparing the estimated "
     "system with a counterfactual in which the return arcs are switched off."),

    ("h2", "2.7. Conceptual Framework"),

    ("p",
     "The conceptual framework of this study is illustrated in Figure 1. The "
     "framework provides a theoretical foundation and structure for "
     "understanding the relationships between the variables under "
     "investigation. Solid arrows represent the forward chain from adoption "
     "to the youth employment share, directly and through the two mediators; "
     "the gray lines terminating in a disc on the direct path represent the "
     "two boundary conditions that govern it; and the dashed arcs represent "
     "the return paths that close the reinforcing loop, marked R1, with the "
     "double stroke denoting the one-year delay on the return."),

    ("fig", "fig1"),

    # =====================================================================
    ("h1", "3. Materials and Methods"),
    ("h2", "3.1. Sample and Data"),

    ("p",
     "The sample consists of Chinese A-share firms listed on the Shanghai and "
     f"Shenzhen stock exchanges over the period {S['years']}. The starting "
     "year is chosen because firm disclosure of artificial-intelligence "
     "related technology becomes systematic from the mid-2010s, and the "
     "window closes with the most recent complete disclosure year. Following "
     "established research conventions, the sample was processed as follows: "
     "financial and insurance firms were excluded; firms designated as "
     "special treatment or particular transfer in any sample year were "
     "excluded; firms with missing values for the principal variables were "
     "excluded; and all continuous variables were winsorized at the first and "
     "ninety-ninth percentiles to limit the influence of outliers. The final "
     f"sample contains {S['n_obs']:,} firm-year observations for "
     f"{S['n_firms']:,} firms distributed across {S['n_ind']} industries and "
     f"{S['n_prov']} provincial units. Financial and governance data are "
     "drawn from the China Stock Market and Accounting Research database, the "
     "workforce age and occupational structure and employee education and "
     "training expenditure from the corresponding human-capital files, and "
     "annual-report text from the disclosure archives of the two exchanges. "
     "Provincial and prefectural macroeconomic series are taken from the "
     "China Statistical Yearbook."),

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
     "The youth employment share (Youth) is measured as the number of "
     "employees aged 30 or below divided by the firm's total workforce, "
     "expressed in percentage points. The threshold follows the definition of "
     "youth employment used in Chinese labor policy and captures the "
     "population that enters the firm through the entry port of the internal "
     "labor market. As a placebo outcome, the share of employees aged 31 to "
     "50 (Exper) is constructed in the same way; the argument of this paper "
     "implies a large effect on the first and a negligible effect on the "
     "second."),

    ("h3", "3.2.2. Explanatory Variable"),

    ("p",
     "Generative artificial intelligence application intensity (GenAI) is "
     "measured by textual analysis of the management discussion and analysis "
     "section of the annual report, following the word-frequency approach now "
     "standard in the Chinese firm-level literature on digital and "
     "intelligent transformation [[wu2021],[yuan2021],[zhaoc2021]]. The "
     "keyword dictionary covers generative and foundation-model terminology "
     "together with its immediate technical prerequisites, and the variable "
     "is the natural logarithm of one plus the total frequency of dictionary "
     "terms. Text-based measures of this kind capture the intensity with "
     "which a firm reports applying the technology rather than the fact of a "
     "single purchase, which is the relevant margin for a study of workforce "
     "composition."),

    ("h3", "3.2.3. Mediating Variables"),

    ("p",
     "Training investment (Train) is the natural logarithm of employee "
     "education and training expenditure per employee, taken from the "
     "employee-benefits note to the financial statements. It is the most "
     "direct available measure of the firm's own investment in skill "
     "formation. The routine task base (Routine) is the share of the "
     "workforce employed in occupational categories that the firm classifies "
     "as routine in its disclosed professional composition, expressed in "
     "percentage points; it measures the stock of codifiable work into which "
     "an inexperienced worker could be placed."),

    ("h3", "3.2.4. Moderating Variables"),

    ("p",
     "Organizational learning capability (Absorp) is proxied by research and "
     "development expenditure as a percentage of operating revenue, the "
     "conventional empirical counterpart of absorptive capacity [[cohen1990]]. "
     "Relative labor cost (Wage) is the natural logarithm of cash paid to and "
     "on behalf of employees divided by the number of employees. Both "
     "moderators are standardized before interactions are formed, so that the "
     "coefficient on GenAI in an interacted model is the marginal effect at "
     "the sample mean of the moderator [[aiken1991]]."),

    ("h3", "3.2.5. Control Variables"),

    ("p",
     "The control set follows the firm-level literature on technology "
     "adoption and employment structure and comprises firm size (Size), "
     "leverage (Lev), profitability (ROA), revenue growth (Growth), operating "
     "cash flow (Cashflow), market valuation (TobinQ), ownership "
     "concentration (Top1), board independence (Indep), chief executive "
     "duality (Dual), board size (Board) and capital intensity (CapInt). Full "
     "definitions of every variable are reported in Table 1."),

    ("table", "table1"),

    ("h2", "3.3. Model Specification"),

    ("p",
     "The benchmark specification is a two-way fixed-effects panel model, "
     "which absorbs all time-invariant firm heterogeneity and all common "
     "annual shocks, so that identification comes from within-firm variation "
     "in adoption relative to the contemporaneous average:"),

    ("eq", r"Youth_{it}=\alpha_{0}+\alpha_{1}GenAI_{it}"
           r"+\sum_{k}\gamma_{k}Control_{k,it}+\mu_{i}+\lambda_{t}"
           r"+\varepsilon_{it}", 1),

    ("p",
     "where $i$ indexes firms and $t$ years, $\\mu_{i}$ and $\\lambda_{t}$ "
     "are firm and year effects, and standard errors are clustered at the "
     "firm level to accommodate arbitrary serial correlation within firms "
     "[[petersen2009],[abadie2023]]. The coefficient of interest is "
     "$\\alpha_{1}$, which H1 predicts to be negative."),

    ("p",
     "The two mechanisms are examined by the three-step procedure of Baron "
     "and Kenny [[baron1986]] as refined by Zhao, Lynch and Chen "
     "[[zhao2010]]. Equation (1) estimates the total effect; Equation (2) "
     "regresses each mediator on adoption; and Equation (3) reintroduces the "
     "mediator alongside adoption:"),

    ("eq", r"Med_{it}=\beta_{0}+\beta_{1}GenAI_{it}"
           r"+\sum_{k}\gamma_{k}Control_{k,it}+\mu_{i}+\lambda_{t}+\eta_{it}",
     2),

    ("eq", r"Youth_{it}=\delta_{0}+\delta_{1}GenAI_{it}+\delta_{2}Med_{it}"
           r"+\sum_{k}\gamma_{k}Control_{k,it}+\mu_{i}+\lambda_{t}+\xi_{it}",
     3),

    ("p",
     "where $Med_{it}$ is either $Train_{it}$ or $Routine_{it}$. Because the "
     "product $\\beta_{1}\\delta_{2}$ is not normally distributed, its "
     "confidence interval is obtained from a bootstrap that resamples whole "
     "firms rather than individual observations, which preserves the "
     "within-firm dependence of the panel [[preacher2008]]."),

    ("p",
     "The boundary conditions are tested by adding interactions between "
     "adoption and each standardized moderator:"),

    ("eq", r"Youth_{it}=\theta_{0}+\theta_{1}GenAI_{it}"
           r"+\theta_{2}GenAI_{it}\times Absorp_{it}"
           r"+\theta_{3}GenAI_{it}\times Wage_{it}"
           r"+\sum_{k}\gamma_{k}Control_{k,it}+\mu_{i}+\lambda_{t}+\nu_{it}",
     4),

    ("p",
     "H4a predicts $\\theta_{2}>0$ and H4b predicts $\\theta_{3}<0$. The "
     "levels of the two moderators are absorbed by the firm effects to the "
     "extent that they are persistent, and their within-firm variation is "
     "retained in the control set."),

    ("p",
     "Adoption is a choice, so Equation (1) may confound the effect of "
     "adoption with the characteristics that led the firm to adopt. Two "
     "excluded instruments are used. The first is the number of fixed-line "
     "telephones per hundred residents in the firm's prefecture in 1984, "
     "interacted with the national generative-AI diffusion index, an "
     "application of the historical-infrastructure design widely used in the "
     "Chinese digital-economy literature; historical telecommunications "
     "density predicts the cost of adopting information technology today but "
     "has no direct bearing on a listed firm's current age structure once "
     "firm and year effects are absorbed. The second is the mean adoption "
     "intensity of firms in the same industry located outside the firm's own "
     "province, which captures industry-wide technological opportunity while "
     "excluding local labor market conditions. The first-stage equation is"),

    ("eq", r"GenAI_{it}=\pi_{0}+\pi_{1}IV^{hist}_{it}+\pi_{2}IV^{peer}_{it}"
           r"+\sum_{k}\gamma_{k}Control_{k,it}+\mu_{i}+\lambda_{t}+\omega_{it}",
     5),

    ("p",
     "and the design is overidentified, so the exclusion restriction can be "
     "assessed by the Hansen J statistic while instrument strength is "
     "assessed by the Kleibergen-Paap rank Wald statistic [[kleibergen2006],"
     "[stockyogo2005]]. Because two-stage least squares can be fragile in "
     "exactly the settings in which it is most often applied, the "
     "instrumental-variable estimates are reported alongside, rather than "
     "in place of, the least-squares benchmark and two "
     "selection-on-observables designs [[young2022],[wooldridge2010]]."),

    ("h2", "3.4. Estimating the Feedback System"),

    ("p",
     "H5 concerns a structure that no single equation can represent, because "
     "each of its three variables is simultaneously an outcome and a driver. "
     "The system is therefore estimated as a panel vector autoregression "
     "[[holtzeakin1988],[love2006],[abrigo2016]]. Let "
     "$z_{it}=(GenAI_{it},Train_{it},Youth_{it})'$. The system is"),

    ("eq", r"z_{it}=A z_{i,t-1}+f_{i}+d_{t}+u_{it}", 6),

    ("p",
     "where $A$ is the matrix of dynamic coefficients, $f_{i}$ collects unit "
     "effects and $d_{t}$ common time effects. Common time effects are "
     "removed first by cross-sectional demeaning within each year, so the "
     "estimated dynamics are those of firm-level departures from the "
     "aggregate diffusion path; unit effects are then removed by the within "
     "transformation. Because the within transformation of a dynamic panel "
     "induces the bias described by Ref. [[nickell1981]], and because the "
     "lagged-level instruments of the difference and system generalized "
     "method of moments estimators are weak when the series are as persistent "
     "as adoption is here [[arellano1991],[arellano1995],[blundell1998]], the "
     "leading term of the bias is removed by the half-panel jackknife of "
     "Chudik, Pesaran and Yang [[chudik2018]],"),

    ("eq", r"\hat{A}_{HPJ}=2\hat{A}-\frac{1}{2}"
           r"\left(\hat{A}_{(1)}+\hat{A}_{(2)}\right)", 7),

    ("p",
     "where $\\hat{A}_{(1)}$ and $\\hat{A}_{(2)}$ are estimated on the first "
     "and second halves of each firm's series. Inference is by a bootstrap "
     "that resamples whole firms. Stability requires that every eigenvalue of "
     "$A$ lie inside the unit circle; the loop then amplifies without "
     "exploding. Impulse responses are orthogonalized by a Cholesky "
     "factorization $\\Sigma=PP'$ with the variables ordered as written "
     "above, so adoption may move training and the youth share within the "
     "year while the reverse requires a lag, and the response at horizon $h$ "
     "is"),

    ("eq", r"\Psi_{h}=A^{h}P", 8),

    ("p",
     "Finally, the contribution of the loop itself is isolated by "
     "constructing a counterfactual matrix $A^{o}$ that is identical to "
     "$\\hat{A}_{HPJ}$ except that the two return coefficients of the "
     "adoption equation are set to zero, and comparing the cumulative "
     "responses of the two systems. The ratio"),

    ("eq", r"\Lambda_{H}=\frac{\sum_{h=0}^{H}\Psi_{h}^{(Youth,GenAI)}}"
           r"{\sum_{h=0}^{H}\Psi_{h}^{o,(Youth,GenAI)}}", 9),

    ("p",
     "measures how much of the cumulative displacement at horizon $H$ is "
     "attributable to the reinforcing loop rather than to the direct "
     "response. A value above unity confirms the systems claim of H5."),

    # =====================================================================
    ("h1", "4. Empirical Results"),
    ("h2", "4.1. Descriptive Statistics and Correlations"),

    ("p",
     "Table 2 reports the descriptive statistics. The youth employment share "
     f"averages {n('mean_Youth', 2)} percent with a standard deviation of "
     f"{n('sd_Youth', 2)}, indicating substantial dispersion in the age "
     "composition of listed-firm workforces. Generative-AI application "
     f"intensity averages {n('mean_GenAI', 3)} with a standard deviation of "
     f"{n('sd_GenAI', 3)}. Its time profile is the expected one: the annual "
     f"mean rises gradually from {n('genai_2016', 2)} in {S['y0']} to "
     f"{n('genai_2022', 2)} in 2022 and then jumps to {n('genai_2024', 2)} by "
     f"{S['y1']}, a {n('genai_growth', 1)}-fold increase over the two years "
     "following the diffusion of large conversational models. Training "
     f"expenditure per employee averages {n('mean_Train', 3)} in logarithms "
     f"and the routine task base {n('mean_Routine', 2)} percent."),

    ("table", "table2"),

    ("p",
     "Table 3 reports the pairwise Pearson correlations together with the "
     "variance inflation factors of the benchmark regressors computed after "
     "the two-way within transformation. Adoption is negatively correlated "
     f"with the youth employment share ({n('corr_gy', 3)}), with training "
     f"expenditure ({n('corr_gt', 3)}) and with the routine task base "
     f"({n('corr_gr', 3)}), which is the raw pattern the hypotheses predict. "
     f"The largest variance inflation factor is {n('vif_max', 2)}, far below "
     "the conventional threshold of five, so multicollinearity does not "
     "threaten the estimates."),

    ("table", "table3"),

    ("h2", "4.2. Benchmark Regression"),

    ("p",
     "Table 4 reports the benchmark results. Column (1) includes firm effects "
     "only, column (2) adds year effects, and column (3) is the full "
     "specification of Equation (1). Across all three the coefficient on "
     "adoption is negative and significant at the one percent level. In the "
     f"benchmark column the estimate is {n('b_main', 3)} with a standard "
     f"error of {n('se_main', 3)}, a t-statistic of {a('t_main', 1)} and a "
     f"within R-squared of {n('r2_main', 3)}. The magnitude is economically "
     "meaningful: a one-standard-deviation increase in generative-AI "
     f"application intensity lowers the youth employment share by "
     f"{a('effect_sd', 2)} percentage points, equivalent to "
     f"{a('effect_sd_pct', 1)} percent of its sample mean, and a movement "
     "from the twenty-fifth to the seventy-fifth percentile of adoption "
     f"lowers it by {a('effect_iqr', 2)} percentage points. H1 is supported."),

    ("p",
     "The estimate is not an artefact of the fixed-effect structure. "
     "Replacing the year effects with industry-by-year effects, which absorb "
     "every shock common to an industry in a year, leaves the coefficient at "
     f"{n('b_indyear', 3)}; replacing them with province-by-year effects, "
     "which absorb every regional labor market shock, leaves it at "
     f"{n('b_provyear', 3)}. The controls behave as the literature would "
     "lead one to expect: larger, more profitable and faster-growing firms "
     "employ a higher share of young workers, while more leveraged firms "
     "employ fewer."),

    ("table", "table4"),

    ("h2", "4.3. Examination of the Mediating Mechanisms"),

    ("p",
     "Table 5 reports the three-step mediation tests. Column (1) repeats the "
     "total effect. Column (2) shows that adoption reduces training "
     f"expenditure per employee by {mva('Train', 'a', 3)} log points, "
     "significant at the one percent level, which is the first link of the "
     "training channel. Column (3) reintroduces training alongside adoption: "
     f"training enters positively at {mv('Train', 'b', 3)} and the direct "
     f"effect of adoption falls in absolute value from {a('b_main', 3)} to "
     f"{mva('Train', 'direct', 3)}. Column (4) shows that adoption contracts "
     f"the routine task base by {mva('Routine', 'a', 3)} percentage points, "
     "and column (5) that the routine base enters the youth equation "
     f"positively at {mv('Routine', 'b', 3)}, with the direct effect falling "
     f"to {mva('Routine', 'direct', 3)}. Column (6) includes both mediators "
     f"together; the direct effect is {a('direct_both', 3)} and remains "
     "significant at the one percent level, so both channels operate and "
     "neither exhausts the total effect."),

    ("table", "table5"),

    ("p",
     "Table 6 quantifies the decomposition. The indirect effect through "
     f"training is {mv('Train', 'indirect', 3)}, with a bootstrap confidence "
     f"interval of [{mv('Train', 'ci_low', 3)}, "
     f"{mv('Train', 'ci_high', 3)}] that excludes zero, and accounts for "
     f"{a('share_train', 1)} percent of the total effect. The indirect effect "
     f"through the routine task base is {mv('Routine', 'indirect', 3)}, with "
     f"an interval of [{mv('Routine', 'ci_low', 3)}, "
     f"{mv('Routine', 'ci_high', 3)}], accounting for "
     f"{a('share_rout', 1)} percent. Together the two channels account for "
     f"{a('share_both', 1)} percent of the total effect, leaving the "
     "remainder to the direct margin. H2 and H3 are both supported. The "
     "relative sizes are informative in their own right: the task channel is "
     "the larger of the two, but the training channel is not a residual, and "
     "it is the training channel that carries the dynamic consequences "
     "examined in Section 4.8."),

    ("table", "table6"),

    ("h2", "4.4. Endogeneity Tests"),

    ("p",
     "Table 7 addresses the concern that adoption is chosen rather than "
     "assigned. Column (1) reports the first stage of Equation (5). Both "
     "instruments enter with the expected positive sign and are significant "
     "at the one percent level, and the Kleibergen-Paap rank Wald statistic "
     f"is {n('kp_f', 1)}, far above the conventional weak-instrument "
     "threshold. Column (2) reports the second stage. The coefficient on "
     f"adoption is {n('b_iv', 3)}, slightly larger in absolute value than the "
     "least-squares estimate, which is consistent with a positive omitted "
     "factor such as an unobserved expansion drive that raises both adoption "
     "and junior hiring. The Hansen J statistic does not reject the "
     f"exclusion restriction (p = {n('hansen_p', 3)}), and the "
     "Durbin-Wu-Hausman statistic does not reject the exogeneity of adoption "
     f"(p = {n('wu_p', 3)}), so the least-squares estimate may be read as "
     "consistent and the two estimates are statistically indistinguishable."),

    ("p",
     "Column (3) replaces contemporaneous adoption with its one-year lag, "
     "which cannot be caused by the current year's employment decisions; the "
     f"coefficient is {n('b_lag1', 3)} and remains significant at the one "
     "percent level, although it is smaller in absolute value than the "
     "contemporaneous estimate, as the mean reversion of the youth share "
     "implies. Column (4) re-estimates the benchmark on a sample matched one "
     "to one on the propensity score, formed from pre-period firm "
     "characteristics [[rosenbaum1983]]; matching reduces the largest "
     f"standardized bias across the matching covariates from "
     f"{n('bal_max_before', 1)} percent to {n('bal_max_after', 1)} percent, "
     f"and the coefficient on the matched sample is {n('b_psm', 3)}. Column "
     "(5) reweights the full sample by entropy-balancing weights that equate "
     "the first two moments of the covariate distributions, giving "
     f"{n('b_eb', 3)}. The four approaches bracket the benchmark closely."),

    ("table", "table7"),

    ("h2", "4.5. Robustness Checks"),

    ("p",
     "Table 8 reports seven robustness checks, each of which retains the full "
     "control set and both sets of fixed effects. Excluding the pandemic "
     "years 2020 and 2021, restricting the sample to firms observed in every "
     "year, replacing the continuous adoption measure with an indicator for "
     "adoption above the annual median, redefining the outcome as the youth "
     "share of the age-classified workforce, clustering by firm and year "
     "simultaneously, and winsorizing the outcome more aggressively all leave "
     "the conclusion intact; the estimated coefficient ranges between "
     f"{n('robust_min', 3)} and {n('robust_max', 3)} in absolute value and is "
     "significant at the one percent level throughout."),

    ("p",
     "The final row is the placebo. If the mechanism is the substitution of "
     "generative models for the codifiable work that entrants perform, then "
     "employment of workers aged 31 to 50, who hold the supervisory and "
     "judgement-intensive positions the technology does not reach, should be "
     f"largely unaffected. The estimated coefficient is {n('b_placebo', 3)} "
     f"(p = {n('p_placebo', 3)}), an order of magnitude smaller than the "
     f"youth coefficient; the ratio of the two is {n('ratio_age', 1)}. The "
     "displacement is specific to the age group the theory names, which no "
     "generic technology shock or firm downsizing story would produce."),

    ("p",
     "Two further diagnostics are reported here rather than in the table. "
     "Applying the coefficient-stability bounds of Ref. [[oster2019]], "
     "selection on unobservables would have to be "
     f"{abs(OST['delta']):.1f} times as strong as selection on the observed "
     "controls, and of the opposite sign, to overturn the result; the "
     "identified set runs from the controlled estimate to "
     f"{OST['beta_star']:+.3f} and does not contain zero. A restricted wild "
     "cluster bootstrap with Rademacher weights and "
     f"{S['wild']['reps']:,.0f} replications, which imposes the null before "
     "resampling and is reliable when the regressor of interest is unevenly "
     "distributed across clusters [[cameron2008],[roodman2019]], returns a "
     f"p-value of {S['wild']['p']:.3f}."),

    ("table", "table8"),

    ("h2", "4.6. Moderating Effects"),

    ("p",
     "Table 9 reports the tests of the boundary conditions. In column (1) the "
     "interaction between adoption and organizational learning capability is "
     f"{n('b_gxa', 3, sign=True)} and significant at the one percent level, "
     "so the displacement is weaker where absorptive capacity is greater; H4a "
     "is supported. In column (2) the interaction with relative labor cost is "
     f"{n('b_gxw', 3)}, also significant at the one percent level, so the "
     "displacement is sharper where labor is expensive relative to the "
     "sample; H4b is supported. Column (3) includes both interactions "
     "simultaneously and the two coefficients are essentially unchanged, "
     "which indicates that the two boundary conditions operate independently "
     "rather than proxying for one another."),

    ("p",
     "The economic content of these interactions is best read off the "
     "marginal effects, which are plotted in Figure 2. At one standard "
     "deviation below the mean of organizational learning capability the "
     f"marginal effect of adoption is {S['margin_absorp'][4]['effect']:.3f}; "
     "at one standard deviation above the mean it is "
     f"{S['margin_absorp'][12]['effect']:.3f}, a reduction of "
     f"{abs(S['margin_absorp'][12]['effect'] - S['margin_absorp'][4]['effect']):.3f} "
     "percentage points, or roughly half the effect at the mean. The pattern "
     "for relative labor cost runs the other way: the marginal effect moves "
     f"from {S['margin_wage'][4]['effect']:.3f} at one standard deviation "
     f"below the mean to {S['margin_wage'][12]['effect']:.3f} at one standard "
     "deviation above it. The effect remains negative and significant across "
     "the whole observed range of both moderators, so neither condition "
     "eliminates the displacement; what they change is its size. The strip "
     "beneath each panel of Figure 2 shows the observed density of the "
     "moderator on that axis, so the range over which the estimate is "
     "supported can be read from the figure rather than taken on trust; the "
     "estimate is drawn only over that range."),

    ("fig", "fig2"),

    ("p",
     "Column (4) of Table 9 examines whether the relationship changed with "
     "the arrival of generative models proper. Interacting adoption with an "
     "indicator for the years from 2023 onwards yields a coefficient of "
     f"{n('b_gxpost', 3)}, significant at the five percent level, so the "
     f"displacement after the break is {n('post_ratio', 2)} times its earlier "
     "magnitude. This is consistent with the capability profile that "
     "distinguishes generative models from the previous generation of "
     "predictive artificial intelligence: what changed in late 2022 was "
     "precisely the ability of the technology to perform the codifiable cognitive work that entry-level positions are composed "
     "of. The professional debate that followed the release of large "
     "conversational models anticipated this shift without being able to "
     "measure it [[dwivedi2023]]."),

    ("table", "table9"),

    ("h2", "4.7. Heterogeneity Analysis"),

    ("p",
     "Table 10 splits the sample along four dimensions and tests the equality "
     "of the adoption coefficient across each pair of subsamples. The effect "
     f"is {hva('Labor-intensive', 'a', 3)} in labor-intensive industries "
     f"against {hva('Labor-intensive', 'b', 3)} in capital-intensive ones, "
     f"and the difference is significant (p = {hv('Labor-intensive', 'p', 3)}); "
     "the displacement is concentrated where the routine task base was large "
     "to begin with, which corroborates the task channel of Section 4.3. The "
     f"effect is {hva('Eastern region', 'a', 3)} in the eastern coastal "
     f"provinces against {hva('Eastern region', 'b', 3)} inland "
     f"(p = {hv('Eastern region', 'p', 3)}), consistent with the relative "
     "labor cost moderator, since coastal wages are higher. The effect is "
     f"{hva('State-owned', 'a', 3)} in state-owned enterprises against "
     f"{hva('State-owned', 'b', 3)} in non-state firms "
     f"(p = {hv('State-owned', 'p', 3)}); state ownership attenuates the "
     "displacement, which is what the employment-stabilization obligations "
     "carried by these firms would predict. The split between high-technology "
     "and other industries yields coefficients of "
     f"{hva('High-technology', 'a', 3)} and {hva('High-technology', 'b', 3)}, "
     f"whose difference is not statistically significant "
     f"(p = {hv('High-technology', 'p', 3)}); the relevant firm-level "
     "attribute appears to be learning capability, which Section 4.6 measures "
     "directly, rather than industry classification, which proxies for it "
     "only loosely."),

    ("table", "table10"),

    ("h2", "4.8. The Feedback System"),

    ("p",
     "The results so far describe a chain running from adoption to "
     "employment. Table 11 estimates the system of Equation (6) and asks "
     "whether the chain closes. The rows are equations and the columns are "
     "the lagged variables entering them. The forward arcs replicate the "
     "single-equation findings: lagged adoption enters the training equation "
     f"at {gc('Train', 'GenAI', 'coef')} and the youth equation at "
     f"{gc('Youth', 'GenAI', 'coef')}, both significant at the one percent "
     "level. The return arcs are the new result. Lagged training investment "
     f"enters the adoption equation at {gc('GenAI', 'Train', 'coef')} and "
     f"lagged youth employment at {gc('GenAI', 'Youth', 'coef')}, both "
     "significant at the one percent level in the panel Granger causality "
     "tests. A firm whose skill-formation subsystem has been depleted adopts "
     "more generative artificial intelligence in the following year, not "
     "less. H5 is supported in its causal content."),

    ("p",
     "The system is dynamically stable. The moduli of the companion "
     f"eigenvalues are {PV['eig'][0]:.3f}, {PV['eig'][1]:.3f} and "
     f"{PV['eig'][2]:.3f}, all inside the unit circle, so the reinforcing "
     "loop amplifies disturbances without setting off an explosive "
     "trajectory. This is the substantively important case: the trap is real "
     "but bounded, which means that the accumulated displacement is finite "
     "and that an intervention on the return arc can reverse it. A two-lag "
     f"specification, estimated on {PV2['nobs']:,} observations, returns the "
     "same signs on both return arcs "
     f"({PV2['fb_train']:+.3f} and {PV2['fb_youth']:+.3f}, both p < 0.01) and "
     f"a largest modulus of {PV2['max_eig']:.3f}."),

    ("table", "table11"),

    ("p",
     "Figure 3 plots the orthogonalized impulse responses with ninety percent "
     "bootstrap bands. A one-standard-deviation innovation to adoption lowers "
     f"the youth employment share by {a('impact', 3)} percentage points on "
     "impact, deepens to its trough in the following year, and decays "
     "thereafter without changing sign; the response of training investment "
     "follows the same shape. The lower panels display the return arcs: an "
     "innovation that raises training investment, or that raises the youth "
     "employment share, lowers adoption from the following year onward, and "
     "the bands exclude zero over the whole visible horizon."),

    ("fig", "fig3"),

    ("p",
     "Table 12 converts the responses into the quantity that matters for the "
     "systems claim. Cumulated over eight years, the response of the youth "
     f"employment share to an adoption innovation is {n('cum8', 3)} "
     f"percentage points, {n('cum_ratio', 1)} times the impact response. When "
     "the two return coefficients of the adoption equation are set to zero "
     "and the system is re-simulated, the same cumulative response is "
     f"{S['cum_open'][-1]:.3f}. The ratio defined in Equation (9) is "
     f"therefore {n('amp', 3)}: the reinforcing loop adds "
     f"{100 * (S['amp'] - 1):.1f} percent to the eight-year cumulative "
     "displacement of young workers. The amplification is absent by "
     "construction in the first two years, because the return arc carries a "
     "one-period delay and the loop must travel the full circuit before it "
     "contributes, and it grows monotonically thereafter. This is the "
     "signature of a reinforcing feedback structure rather than of a "
     "persistent shock, and it is not recoverable from any single-equation "
     "estimate."),

    ("table", "table12"),

    # =====================================================================
    ("h1", "5. Discussion and Implications"),
    ("h2", "5.1. The Displacement of Entry-Level Labor (H1)"),

    ("p",
     "Hypothesis 1 was confirmed. Generative artificial intelligence adoption "
     "reduces the youth employment share of the adopting firm, by "
     f"{a('effect_sd', 2)} percentage points per standard deviation of "
     "adoption intensity, and the estimate survives the replacement of the "
     "year effects with industry-by-year and province-by-year effects, an "
     "overidentified instrumental-variable design, propensity score matching, "
     "entropy balancing and six robustness specifications. The result is "
     "consistent with the exposure evidence of Refs. [[eloundou2024]] and "
     "[[felten2021]] and with the aggregate relative decline in young "
     "workers' employment documented by Ref. [[canaries2025]], and it locates "
     "that decline inside the firm, where the hiring decision is actually "
     "taken. The placebo result is what gives the finding its interpretive "
     f"force: the effect on employees aged 31 to 50 is {n('ratio_age', 1)} "
     "times smaller, so what the estimates capture is not a general "
     "contraction of employment but a change in its age composition."),

    ("h2", "5.2. Two Mechanisms of Displacement (H2 and H3)"),

    ("p",
     "Hypotheses 2 and 3 were both supported, and their relative sizes carry "
     "a message that neither hypothesis alone conveys. The contraction of the "
     f"routine task base accounts for {a('share_rout', 1)} percent of the "
     "total effect, which is the mechanism the task-based framework of Refs. "
     "[[acemoglu2018]] and [[autor2003]] predicts and which most of the "
     "existing literature assumes to be the whole story. The suppression of "
     f"training investment accounts for a further {a('share_train', 1)} "
     "percent, a channel that the task-based framework does not contain at "
     "all, because it treats labor as an input to be allocated rather than an "
     "asset to be produced. This second channel is the point at which the "
     "labor economics of automation meets the organizational learning "
     "tradition of Refs. [[cohen1990]] and [[levinthal1993]]. A firm that "
     "reduces its training outlay when it adopts is not merely hiring fewer "
     "juniors this year; it is dismantling the apparatus by which it converts "
     "juniors into seniors, which is precisely the asset that Refs. "
     "[[becker1964]] and [[doeringer1971]] identified as unavailable on the "
     "external market."),

    ("h2", "5.3. What Weakens and What Sharpens the Effect (H4a and H4b)"),

    ("p",
     "Hypotheses 4a and 4b were both validated. The displacement is roughly "
     "halved in firms one standard deviation above the mean of organizational "
     "learning capability and correspondingly deepened in firms above the "
     "mean of relative labor cost, and the two conditions operate "
     "independently. This is the empirical content of the socio-technical "
     "proposition that the technical and social subsystems must be jointly "
     "optimized [[trist1951],[emery1965]]: the same technology, adopted at "
     "the same measured intensity, produces materially different employment "
     "outcomes depending on the organizational capacity that receives it. The "
     "heterogeneity results in Section 4.7 reinforce the reading. Industry "
     "classification, which proxies for learning capability only loosely, "
     "does not discriminate between firms, whereas the direct measure does; "
     "and the labor-intensity split, which proxies for the size of the "
     "routine task base, discriminates sharply. The determinants of the "
     "outcome are firm-level and, in the case of learning capability, "
     "constructible."),

    ("h2", "5.4. The Reinforcing Loop and the Capability Trap (H5)"),

    ("p",
     "Hypothesis 5 is strongly supported by the system estimates, and it is "
     "the finding on which the contribution of this paper rests. The two "
     "return arcs are negative and significant: a firm whose training "
     "investment has fallen, and whose youth cohort has thinned, adopts more "
     "generative artificial intelligence in the following year. The structure "
     "is exactly the capability trap described by Ref. [[repenning2002]] and "
     "formalized by Ref. [[rahmandad2016]]. A short-run fix and a long-run "
     "capability investment compete for the same managerial attention; the "
     "fix pays immediately and the investment pays late; choosing the fix "
     "degrades the capability whose weakness makes the fix attractive; and "
     "the pull toward the fix is therefore stronger next period than it was "
     "this period. No step in this sequence requires a mistake. The pathology "
     "is a property of the loop, not of the decision-maker, which is why the "
     f"loop and not the decision is the object of intervention [[meadows2008]]."),

    ("p",
     "The quantitative content is that the loop adds "
     f"{100 * (S['amp'] - 1):.1f} percent to the eight-year cumulative "
     "displacement. Two readings follow. The first is methodological: any "
     "estimate of the effect of generative artificial intelligence on youth "
     "employment obtained from a single equation understates the total effect "
     "by roughly this margin, because it holds constant a variable that the "
     "outcome itself moves. The second is substantive: because the largest "
     f"eigenvalue is {PV['max_eig']:.3f} rather than greater than one, the "
     "trap is bounded, the accumulation converges, and an intervention that "
     "cuts the return arc, rather than one that resists the initial adoption, "
     "returns the system to the smaller open-loop path. This is what a "
     "leverage point means in the systems sense: a place where a small "
     "structural change produces a large behavioral change, identified from "
     "the structure of the loop rather than from the size of any single "
     "coefficient [[meadows2008],[sterman2000],[senge1990]]."),

    ("h2", "5.5. Theoretical Contributions"),

    ("p",
     "This study makes three theoretical contributions. First, it "
     "reconceptualizes the relationship between generative artificial "
     "intelligence and youth employment as a feedback structure rather than a "
     "treatment effect, and supplies the first firm-level estimate of the "
     "return arc together with a measure of the amplification it produces. "
     "This extends the task-based framework of Refs. [[acemoglu2018]] and "
     "[[acemoglu2022]] in a direction that framework does not itself provide, "
     "because the framework has no representation of the firm's technology "
     "choice as a function of its own workforce composition. Second, it "
     "brings the capability trap of Refs. [[repenning2002]] and "
     "[[rahmandad2016]], previously demonstrated for process improvement and "
     "maintenance, to bear on human capital, and shows that the same "
     "structure governs the erosion of a firm's skill-formation system. "
     "Third, it operationalizes the socio-technical proposition of Refs. "
     "[[trist1951]] and [[emery1965]] in a form that can be estimated, by "
     "showing that the employment consequence of a fixed technical intensity "
     "varies systematically with a measurable property of the social "
     "subsystem."),

    ("h2", "5.6. Managerial and Policy Implications"),

    ("p",
     "For firm managers, the results argue against evaluating generative "
     "artificial intelligence deployments on the cost saving of the period in "
     "which they are made. The saving is real, and so is the erosion of the "
     "pipeline that produces the firm's future senior staff; the second is "
     "delayed and therefore systematically underweighted. Three concrete "
     "practices follow: ring-fence the training budget from the "
     "productivity savings that adoption generates, so that the two decisions "
     "are not made against one another; redesign entry-level roles around the "
     "complementary tasks that the technology creates, namely prompt design, "
     "output verification, data curation and workflow integration, rather "
     "than eliminating the roles whose original tasks the technology absorbs; "
     "and monitor the age structure of the workforce as a leading indicator "
     "of capability, not as a by-product of hiring."),

    ("p",
     "For human resource and workforce development functions, the moderation "
     "results identify organizational learning capability as the leverage "
     "point. Because the same adoption intensity displaces roughly half as "
     "much youth employment in firms with strong absorptive capacity, "
     "investment in that capacity is not a competing use of funds but the "
     "condition under which adoption and youth employment cease to be "
     "substitutes."),

    ("p",
     "For policymakers, the implications are addressed to specific actors. "
     "Employment ministries and local labor bureaux should recognize that "
     "subsidies attached to the act of hiring a graduate operate on the "
     "forward arc of the loop and will be partly undone by the return arc; "
     "instruments that condition support on verified training provision, "
     "rather than on headcount alone, act on the arc that closes the loop and "
     "are correspondingly more durable. Industrial and technology regulators "
     "implementing national artificial-intelligence strategies "
     "[[statecouncil2025],[janssen2025]] should incorporate workforce "
     "development conditions into deployment incentives, since the evidence "
     "here indicates that adoption and skill formation are not automatically "
     "complementary at the firm level. Education authorities facing record "
     "graduate cohorts [[moe2025]] should note that the tasks disappearing "
     "from entry-level roles are the codifiable ones, so curricula that "
     "certify verification, judgement and model-integration skills address "
     "the margin that is actually moving. Finally, state-owned enterprises, "
     "whose displacement coefficient is the smallest in Table 10, are already "
     "functioning as a partial buffer; the finding argues for making that "
     "role explicit and time-limited rather than incidental, since a buffer "
     "that is not accompanied by training provision postpones the trap "
     "without disarming it."),

    ("h2", "5.7. Limitations and Future Research Directions"),

    ("p",
     "Several limitations qualify these findings and point to further work. "
     "First, adoption is measured from annual-report text, which captures the "
     "intensity with which a firm reports applying the technology rather than "
     "verified deployment; firms may over-report to signal modernity, and "
     "although firm fixed effects absorb persistent differences in "
     "disclosure style, time-varying strategic disclosure would remain. "
     "Linking the text measure to procurement records or to model-usage "
     "telemetry would sharpen the measurement. Second, the sample covers "
     "listed firms, which are larger and more formal than the enterprises "
     "that employ most young Chinese workers; the direction of the bias is "
     "not obvious, since listed firms adopt earlier but also carry more "
     "structured internal labor markets, and extending the design to survey "
     "data on small and medium enterprises would settle it. Third, the panel "
     f"covers {S['y1'] - S['y0'] + 1} years, of which only the last two lie "
     "after the generative-AI break, so the impulse responses beyond a "
     "three-year horizon are extrapolations of the estimated dynamics rather "
     "than direct observations; re-estimating the system as the post-break "
     "window lengthens is the natural next step. Fourth, the analysis stops "
     "at the firm boundary and therefore cannot say whether the young workers "
     "not hired by adopting firms are absorbed elsewhere in the economy; "
     "combining firm-level adoption with matched employer-employee records "
     "would identify the destination of the displaced. Fifth, the "
     "identification of the return arc rests on a recursive ordering of the "
     "system, and although the ordering is the conventional one for a "
     "technology variable that is decided before the annual workforce plan is "
     "executed, a design with an external shifter of training investment "
     "would provide a stronger test. Finally, the mediators measured here do "
     "not exhaust the mechanism; organizational structure, supervisory "
     "capacity and the internal promotion ladder are plausible additional "
     "channels that richer personnel data would allow future research to "
     "examine."),

    # =====================================================================
    ("h1", "6. Conclusions"),

    ("p",
     "Entry-level work is the first rung of the ladder by which economies "
     "produce experienced workers, and generative artificial intelligence is "
     "most capable at exactly the tasks that rung is made of. Using "
     f"{S['n_obs']:,} firm-year observations for {S['n_firms']:,} Chinese "
     f"A-share listed firms over {S['years']}, this study finds that a "
     "one-standard-deviation increase in generative-AI application intensity "
     f"lowers the youth employment share by {a('effect_sd', 2)} percentage "
     f"points, or {a('effect_sd_pct', 1)} percent of its mean, while "
     "employment of workers aged 31 to 50 is barely affected. The "
     "displacement operates through two measurable channels: a contracting "
     f"routine task base, which accounts for {a('share_rout', 1)} percent of "
     "the total effect, and suppressed investment in employee training, which "
     f"accounts for a further {a('share_train', 1)} percent. It is weaker "
     "where organizational learning capability is stronger and sharper where "
     "relative labor costs are higher, and it is about a quarter larger after "
     "the generative-AI break of late 2022 than before it."),

    ("p",
     "The central finding is structural rather than marginal. The "
     "adoption-capability-youth relationship is not a one-way shock but a "
     "reinforcing loop: firms whose training investment and youth cohort have "
     "contracted adopt more generative artificial intelligence in the "
     "following year, and this return arc amplifies the eight-year cumulative "
     f"displacement by {100 * (S['amp'] - 1):.1f} percent relative to a "
     "system in which the loop is switched off. Because the largest "
     f"eigenvalue of the estimated system is {PV['max_eig']:.3f}, the trap is "
     "bounded rather than explosive, which is what makes it addressable. The "
     "policy conclusion follows from the structure: interventions aimed at "
     "the moment of adoption operate on the forward arc and are partly undone "
     "by the return arc, whereas instruments that protect training provision "
     "act on the arc that closes the loop. For a country entering a decade of "
     "record graduate cohorts, the difference between the two is the "
     "difference between slowing the erosion of the first rung and stopping "
     "it."),

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
     "archives of the Shanghai and Shenzhen stock exchanges under license and "
     "are therefore not publicly available. The estimation code that "
     "reproduces every table and figure is available from the corresponding "
     "author upon reasonable request."),

    ("h1b", "Conflicts of Interest"),
    ("stmt2", "", "The authors declare no conflicts of interest."),
]
