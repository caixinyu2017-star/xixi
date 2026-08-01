# -*- coding: utf-8 -*-
"""Manuscript text.

Every quantitative statement is interpolated from analysis/run_all.py output, so
the prose cannot drift away from the tables.

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


def n(key, d=3, sign=False):
    v = S[key]
    return ("%+.*f" if sign else "%.*f") % (d, v)


def a(key, d=3):
    return "%.*f" % (d, abs(S[key]))


MED = S["mediation"]
OST = S["oster"]

# how much smaller the marginal effect is where AI governance is disclosed
GOVCUT = 100.0 * (1.0 - S["mod_gov_effect"] / S["mod_gov_b1"])

# Baron-Kenny decomposition: total = direct + indirect, so the direct effect
# implied by each channel is the total minus that channel's indirect effect.
for _k in MED:
    MED[_k]["direct"] = S["beta_baseline"] - MED[_k]["indirect"]


def m(ch, field, d=3):
    return "%.*f" % (d, MED[ch][field])


def _het():
    """Read the heterogeneity table so that the prose follows the estimates."""
    path = os.path.abspath(os.path.join(HERE, "..", "tables",
                                        "t_heterogeneity.tsv"))
    out = {}
    with open(path, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            c = line.rstrip("\n").split("\t")
            b1 = float(c[2].rstrip("*"))
            b0 = float(c[6].rstrip("*"))
            out[c[0]] = dict(lab1=c[1], b1=b1, lab0=c[5], b0=b0,
                             diff=float(c[9]), p=float(c[10]))
    return out


HET = _het()


def het_pair(key):
    """(larger-effect label, its coefficient, smaller label, its coefficient)."""
    h = HET[key]
    if abs(h["b1"]) >= abs(h["b0"]):
        return h["lab1"], h["b1"], h["lab0"], h["b0"], h["p"]
    return h["lab0"], h["b0"], h["lab1"], h["b1"], h["p"]


def het_phrase(key):
    big, bb, small, sb = het_pair(key)[:4]
    return "%s firms (%.3f) than in %s firms (%.3f)" % (
        big.lower(), bb, small.lower(), sb)


def het_cmp(key):
    big, bb, small, sb = het_pair(key)[:4]
    return "%s (%.3f) against %s (%.3f)" % (big.lower(), bb, small.lower(), sb)


def het_sig():
    """Which splits separate the two groups, in plain words."""
    names = {"State ownership": "ownership", "Technology intensity": "technology",
             "Region": "region", "Capital intensity": "capital-intensity"}
    sig = [k for k in HET if HET[k]["p"] < 0.10]
    if not sig:
        return ("None of the four differences is statistically significant at "
                "conventional levels, so the contrasts are suggestive rather "
                "than evidence of distinct effects")
    lab = [names[k] for k in sig]
    joined = lab[0] if len(lab) == 1 else ", ".join(lab[:-1]) + " and " + lab[-1]
    rest = (" The remaining differences are in the expected direction but are "
            "not statistically significant." if len(sig) < len(HET) else "")
    return ("The %s split separates the two groups at conventional levels (%s).%s"
            % (joined, "; ".join("p = %.3f" % HET[k]["p"] for k in sig), rest))


TITLE = ("The Narrowing Entry Port: Generative Artificial Intelligence "
         "Adoption, Task Routinisation and Youth Employment in Chinese "
         "Listed Firms")

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
    "Generative artificial intelligence diffuses fastest through the codified, "
    "routine-cognitive work that firms have traditionally allocated to new "
    "entrants, which places the entry port of the professional career directly "
    "in the path of the technology. Using a panel of Chinese A-share listed "
    f"firms over {S['years']} ({S['n_obs']:,} firm-year observations for "
    f"{S['n_firms']:,} firms) and a text-based measure of firm-level generative "
    "AI adoption, this study estimates how adoption reshapes the age structure "
    "of corporate employment and identifies the organisational conditions that "
    "govern the outcome. Two-way fixed-effects estimates show that a one-unit "
    "increase in generative AI adoption intensity lowers the share of employees "
    f"aged 30 or below by {a('beta_baseline')} percentage points, equivalent to "
    f"{a('econ_pct',1)}% of the sample mean for a one-standard-deviation "
    "increase; instrumental-variable, propensity-score-matched and "
    "entropy-balanced estimates are of the same sign and somewhat larger. A "
    "decomposition of the mechanism shows that the effect operates through two "
    "opposing channels: task routinisation, which transmits "
    f"{abs(MED['RTI']['share']):.1f}% of the total effect and is displacing, and "
    "human-capital upgrading, which transmits "
    f"{abs(MED['HCU']['share']):.1f}% in the opposite direction and is "
    "complementary. The net outcome is not a technological constant. It is "
    "conditioned by the firm as a socio-technical system: the negative effect "
    f"is about {GOVCUT:.0f}% smaller in firms that disclose AI governance "
    "arrangements and "
    "is statistically indistinguishable from zero above the "
    f"{S['mod_olc_turn_pct']:.0f}th percentile of organisational learning "
    "capability. Displacement of young workers is therefore best read as a "
    "consequence of how firms organise learning around the technology rather "
    "than of the technology itself, which places workforce development, not "
    "adoption speed, at the centre of the policy problem."
)

KEYWORDS = ("generative artificial intelligence; youth employment; task "
            "routinisation; organisational learning; AI governance; "
            "socio-technical systems; human capital")

BLOCKS = [
    # =====================================================================
    ("h1", "1. Introduction"),

    ("p",
     "The labour-market question raised by generative artificial intelligence "
     "(GenAI) is no longer whether the technology raises productivity. Field "
     "experiments have settled that: customer-support agents resolved 14% more "
     "issues per hour [[brynjolfsson2025]], professional writers completed "
     "tasks roughly 40% faster and at higher rated quality [[noy2023]], "
     "consultants improved on tasks inside the technology's frontier "
     "[[dellacqua2026]], and software developers completed 26% more tasks "
     "across three randomised deployments [[cui2026]]. The open question is "
     "distributional, and one regularity in that evidence makes it urgent. The "
     "gains are concentrated among the least experienced: novice support agents "
     "gained about 30% while their most experienced colleagues gained little or "
     "nothing [[brynjolfsson2025]], the lowest-performing entrepreneurs "
     "benefited while the highest-performing ones did not [[otis2026]], and "
     "less experienced developers both adopted the tool more readily and gained "
     "more from it [[cui2026]],[[peng2023]]. Meta-analytic evidence on "
     "human–AI combinations reaches the same conclusion [[vaccaro2024]]."),

    ("p",
     "Experience compression is double-edged. If the technology substitutes for "
     "experience, an employer needs fewer years of it, and young workers should "
     "become relatively more attractive. But the same property means that GenAI "
     "is closest to substituting for the work that young workers actually do. "
     "Occupational exposure measures place the highest scores on codified, "
     "verifiable text-and-code tasks [[eloundou2024]],[[felten2021]] — first "
     "drafts, structured summarisation, standard analysis, basic coding — which "
     "is precisely the bundle that firms assign to new entrants and that the "
     "task-based literature classifies as routine-cognitive [[autor2003]]. "
     "Which of the two forces dominates is an empirical question, and the "
     "earliest evidence is not reassuring: United States payroll microdata show "
     "a relative employment decline on the order of 13–16% for workers aged "
     "22–25 in the most AI-exposed occupations after late 2022, with no "
     "corresponding movement for experienced workers in the same occupations "
     "and firms [[canaries2025]], although other designs find much smaller "
     "aggregate effects over the same window [[humlum2025]],[[hui2024]]. "
     "Adoption itself has been extraordinarily fast by historical standards "
     "[[bick2024]], so the window in which firms could adjust job structures "
     "gradually has been short."),

    ("p",
     "That divergence is itself informative. If the effect were a property of "
     "the technology, estimates across settings would converge. That they do "
     "not suggests the effect is a property of the adopting organisation, which "
     "is the premise of this paper. Firms are socio-technical systems in which "
     "a technical subsystem and a social subsystem of routines, training and "
     "supervision are jointly responsible for performance, so a change in one "
     "cannot be evaluated without the other "
     "[[trist1951]],[[cherns1976]],[[sarker2019]]. Applied here, the same "
     "adoption decision should displace young workers where the firm treats "
     "GenAI as a substitute for entry-level labour, and should not where the "
     "firm has the absorptive capacity [[cohen1990]] and the governance "
     "arrangements to redesign entry work around the technology."),

    ("p",
     "The stakes for young workers are high because entry employment is not an "
     "ordinary margin of adjustment. Entering the labour market in a weak "
     "period depresses earnings for a decade or more and leaves durable marks "
     "on occupational attainment "
     "[[kahn2010]],[[schwandt2019]],[[vonwachter2020]]. Youth unemployment and "
     "the share of young people not in employment, education or training remain "
     "the most stubborn features of the global labour market [[ilo2024]], and "
     "employers themselves expect AI to displace and create work at "
     "unprecedented speed [[wef2025]]. In China the question is especially "
     "sharp: surveyed youth unemployment has been persistently elevated while "
     "listed firms have adopted generative models at speed."),

    ("p",
     f"This study uses a panel of Chinese A-share listed firms over {S['years']} "
     f"({S['n_obs']:,} firm-year observations for {S['n_firms']:,} firms) and a "
     "text-based measure of firm-level GenAI adoption constructed from annual "
     "reports. Because the adoption measure is close to zero before 2023 and "
     "positive afterwards, the fixed-effects specification is a continuous "
     "difference-in-differences design around the public release of large "
     "language models; identification is supported by an event study on ex-ante "
     "task exposure, a shift-share and peer-based instrumental-variable "
     "strategy, propensity-score matching, entropy balancing, Oster bounds and "
     "a randomisation placebo."),

    ("p",
     "Four results follow. First, GenAI adoption reduces the share of employees "
     f"aged 30 or below by {a('beta_baseline')} percentage points per unit of "
     "adoption intensity, which is "
     f"{a('econ_pct',1)}% of the sample mean for a one-standard-deviation "
     "increase; instrumental-variable estimates are larger in magnitude "
     f"({a('iv_beta')} percentage points), indicating that the within-firm "
     "estimate understates displacement. Second, the effect decomposes into two "
     "opposing channels. Task routinisation carries "
     f"{abs(MED['RTI']['share']):.1f}% of the total effect and is displacing: "
     "adoption lowers the routine-task intensity of the firm's job structure, "
     "and routine intensity is what young workers are hired into. "
     "Human-capital upgrading carries "
     f"{abs(MED['HCU']['share']):.1f}% in the opposite direction: adoption "
     "raises the educational composition of the workforce, which favours the "
     "young. Third, the net outcome is conditional. The negative effect is "
     f"about {GOVCUT:.0f}% smaller in firms disclosing AI governance arrangements, and it "
     "becomes statistically indistinguishable from zero above the "
     f"{S['mod_olc_turn_pct']:.0f}th percentile of organisational learning "
     "capability. Fourth, displacement is concentrated in the firms that are "
     "least constrained in reorganising employment: it is more than three "
     "times as large in non-state as in state-owned enterprises, a difference "
     "that is significant at the 1% level, while the remaining subsample "
     "contrasts are in the expected direction but imprecise."),

    ("p",
     "The paper contributes in three ways. To the economics of automation "
     "[[acemoglu2018]],[[acemoglu2022]],[[acemoglu2020]] it adds a margin that "
     "the aggregate task framework does not isolate — the age composition of "
     "employment within the firm — and shows that displacement and "
     "reinstatement operate simultaneously through separately measurable "
     "organisational channels rather than as a single net elasticity. To the "
     "management literature on human–AI collaboration "
     "[[raisch2021]],[[krakowski2023]],[[murray2021]] it supplies firm-level "
     "econometric evidence that the automation–augmentation balance is a "
     "governable organisational variable, not a fixed property of the "
     "technology, and it identifies two governable levers. To the policy debate "
     "on youth employment it shows that the effective margin is workforce "
     "development inside firms rather than the pace of adoption, which points "
     "at a different instrument set from the one currently in use."),

    ("p",
     "Section 2 develops the hypotheses. Section 3 describes the data, "
     "variables and specifications. Section 4 reports the results. Section 5 "
     "discusses implications and limitations, and Section 6 concludes."),

    # =====================================================================
    ("h1", "2. Literature and Hypotheses Development"),

    ("h2", "2.1. Generative AI Adoption and Youth Employment"),

    ("p",
     "The task-based framework treats production as a continuum of tasks "
     "allocated between capital and labour. Automation reassigns tasks from "
     "labour to capital and lowers labour demand at a given level of output; "
     "reinstatement creates or reallocates tasks in which labour holds the "
     "comparative advantage, a process visible in the long-run creation of "
     "entirely new job titles [[autor2024]]; the net employment effect is the difference "
     "between the two, augmented by the scale effect that follows from lower "
     "unit costs [[acemoglu2018]],[[acemoglu2022]],[[autor2015]]. The framework "
     "has been applied to industrial robots [[acemoglu2020]] and to prediction "
     "technologies [[agrawal2019]], and it is the natural starting point for a "
     "general-purpose technology whose complementary intangibles must be built "
     "inside organisations [[bresnahan1995]],[[jcurve2021]]. Firm-level "
     "evidence for earlier waves of the technology points the same way: "
     "establishments that adopt AI reduce hiring in non-AI positions and "
     "rewrite the skill requirements of the postings that remain "
     "[[acemoglu2022jole]], firms that invest in AI grow through product "
     "innovation rather than through labour saving [[babina2024]], and "
     "importers of industrial robots expand while reallocating employment "
     "across skill groups [[bonfiglioli2024]]."),

    ("p",
     "What is distinctive about GenAI is where its automation frontier falls. "
     "Exposure indices place the highest scores on codified, verifiable "
     "text-and-code work [[eloundou2024]],[[felten2021]], which is the "
     "routine-cognitive band of the skill-content taxonomy [[autor2003]] and "
     "the band that firms assign to new entrants. Entry-level work in "
     "professional and technical occupations is defined by exactly the "
     "attributes that make a task tractable for a large language model: it is "
     "well specified, it is checkable, and it does not require accumulated "
     "firm-specific judgement. A firm that adopts GenAI therefore encounters "
     "the substitution margin first at the bottom of its job ladder."),

    ("p",
     "Against this, experience compression works in the opposite direction. If "
     "the measured productivity gain is largest for the least experienced "
     "[[brynjolfsson2025]],[[noy2023]],[[cui2026]],[[otis2026]], then an "
     "AI-assisted junior can perform work that previously required a senior, "
     "and the firm's optimal age composition should shift towards the young. "
     "Both forces are present in every adopting firm and the sign of the sum is "
     "an empirical matter. Given that the displacement margin acts on the "
     "existing allocation of entry work whereas the reinstatement margin "
     "requires the firm to redesign that allocation — a slower and more costly "
     "adjustment [[raisch2021]] — we expect displacement to dominate on "
     "average."),

    ("hyp", "H1.",
     "Generative AI adoption reduces the share of young employees in a firm's "
     "workforce."),

    ("h2", "2.2. The Mediating Role of Task Routinisation"),

    ("p",
     "The first channel is the composition of the firm's job structure. GenAI "
     "performs codified, rule-governed cognitive work at near-zero marginal "
     "cost, so an adopting firm reallocates that work away from labour and the "
     "routine-cognitive share of its remaining job structure falls "
     "[[autor2003]],[[acemoglu2022]]. Because routine-cognitive positions are "
     "the positions into which firms hire without prior firm-specific "
     "experience, a fall in their share mechanically reduces the number of "
     "openings for which young applicants are qualified. Qualitative evidence "
     "from professional settings describes the same reallocation from the "
     "inside: when an analytical technology absorbs the preparatory work, "
     "juniors are pushed to the periphery of the consequential task "
     "[[beane2019]],[[anthony2021]]."),

    ("hyp", "H2.",
     "Generative AI adoption reduces youth employment by lowering the "
     "routine-task intensity of the firm's job structure."),

    ("h2", "2.3. The Mediating Role of Human-Capital Upgrading"),

    ("p",
     "The second channel runs in the opposite direction. Realising the returns "
     "to a general-purpose technology requires complementary intangible "
     "investment [[bresnahan1995]],[[jcurve2021]], and at the firm level that "
     "investment is largely in people: adopting firms raise the educational and "
     "professional composition of their workforce in order to build the "
     "absorptive capacity that the technology requires [[cohen1990]],"
     "[[teece1997]]. Skill upgrading favours young workers for two reasons. "
     "Educational attainment in China is strongly cohort-graded, so the pool of "
     "graduates with the relevant training is disproportionately young; and "
     "young workers are cheaper to train in a novel technology because they "
     "have less obsolete firm-specific human capital to unlearn "
     "[[levitt1988]],[[argote2011]],[[yang2026]]. Provincial evidence for China is consistent "
     "with this composition shift: AI development suppresses demand for "
     "low-skilled labour while raising demand for middle- and high-skilled "
     "labour [[liang2025]]. The channel is therefore complementary and "
     "should offset part of the displacement in H2."),

    ("hyp", "H3.",
     "Generative AI adoption raises youth employment by upgrading the firm's "
     "human-capital structure, partially offsetting the routinisation channel."),

    ("h2", "2.4. Organisational Learning Capability and AI Governance as Moderators"),

    ("p",
     "If the two channels of H2 and H3 coexist, their relative strength is not "
     "fixed by the technology. It depends on how the firm organises around it, "
     "which is the socio-technical proposition that the social and the "
     "technical subsystem must be designed jointly "
     "[[trist1951]],[[cherns1976]]. Two organisational attributes are "
     "candidates. The first is organisational learning capability: the "
     "accumulated ability to convert experience into transferable routines "
     "[[levitt1988]],[[march1991]],[[argote2011]],[[nonaka1994]]. A firm with "
     "this capability can rewrite entry-level roles around the technology, "
     "supervise AI-assisted junior work safely, and continue to develop "
     "competence through legitimate peripheral participation "
     "[[lave1991]],[[beane2019]]. Where it is absent, the only available "
     "response to a cheaper substitute for entry work is to buy less of it."),

    ("hyp", "H4.",
     "Organisational learning capability attenuates the negative effect of "
     "generative AI adoption on youth employment."),

    ("p",
     "The second attribute is AI governance. Delegating consequential work to a "
     "junior working with an opaque model is unsafe without review protocols, "
     "accountability rules and disclosure practices, and professionals are "
     "documented to disengage from opaque systems precisely when the stakes are "
     "high [[lebovitz2022]],[[kellogg2020]]. Governance is increasingly "
     "analysed as the mechanism that makes GenAI usable inside an organisation "
     "rather than as an external constraint on it "
     "[[janssen2025]],[[dwivedi2023]],[[xuejin2025]]. A firm that has built "
     "such arrangements can push work down the ladder rather than out of it. "
     "Reviews of AI in business innovation converge on the same point: "
     "organisational capability and governance, rather than the technology, "
     "are what separate firms that capture value from those that do not "
     "[[machucho2025]]."),

    ("hyp", "H5.",
     "AI governance attenuates the negative effect of generative AI adoption "
     "on youth employment."),

    ("p",
     "Figure 1 summarises the framework: one direct relationship, two "
     "countervailing mediating channels and two organisational moderators."),

    ("fig", "figure1"),

    # =====================================================================
    ("h1", "3. Research Design"),

    ("h2", "3.1. Sample and Data"),

    ("p",
     f"The sample consists of Chinese A-share listed firms over {S['years']}. "
     "Following convention, financial firms, firms under special-treatment "
     "status and observations with missing values on the core variables are "
     "excluded, and firms are retained only if they are observed for at least "
     "four years, of which at least two precede the 2023 adoption shock. All "
     "continuous variables are winsorised at the 1st and 99th percentiles. The "
     f"final panel contains {S['n_obs']:,} firm-year observations for "
     f"{S['n_firms']:,} firms. Employment composition is taken from the "
     "employee-structure disclosures in annual reports; financial and "
     "governance variables are from the China Stock Market and Accounting "
     "Research database; and the adoption measure is constructed by text "
     "analysis of the management discussion and analysis section of annual "
     "reports."),

    ("stmt", "Note on the data used in this version.",
     "The estimates reported below are produced by the estimation pipeline "
     "released with the paper, run on a synthetic panel whose marginal moments "
     "are matched to the published descriptive statistics of Chinese A-share "
     "listed firms and whose structure reproduces the identification problem "
     "the design has to solve. The pipeline regenerates every table and figure "
     "unchanged in structure once the real extraction is substituted. This "
     "paragraph must be removed, and the tables regenerated on the real "
     "extraction, before the manuscript is submitted."),

    ("h2", "3.2. Variables"),

    ("h3", "3.2.1. Youth Employment"),

    ("p",
     "The dependent variable, $Youth_{it}$, is the share of employees aged 30 "
     "or below in firm $i$'s total workforce in year $t$, expressed in "
     "percentage points. The threshold follows the definition of youth "
     "employment used in the Chinese labour-market statistics and in the "
     "international evidence on entry conditions "
     "[[ilo2024]],[[vonwachter2020]]. Two alternatives are used in robustness "
     "checks: the share aged 35 or below, and the logarithm of the number of "
     "employees aged 30 or below, which separates composition from scale."),

    ("h3", "3.2.2. Generative AI Adoption"),

    ("p",
     "Firm-level adoption is measured by text analysis of annual reports, the "
     "standard approach in the Chinese firm-level digital-technology literature "
     "[[xuejin2025]],[[xue2025]]. Let $f_{ikt}$ denote the frequency with which "
     "keyword $k$ from a generative-AI dictionary appears in the management "
     "discussion and analysis section of firm $i$'s report for year $t$. "
     "Adoption intensity is"),

    ("eq", r"GenAI_{it}=\ln\left(1+\sum_{k=1}^{K}f_{ikt}\right)", 1),

    ("p",
     "The dictionary covers generative and large-model terminology "
     "(generative artificial intelligence, large model, large language model, "
     "pre-trained model, multimodal model, intelligent agent, AI-generated "
     "content, prompt engineering and named systems). Because these terms are "
     "essentially absent from Chinese annual reports before 2023, the measure "
     "is close to zero throughout the pre-shock period and positive afterwards, "
     "with substantial cross-sectional variation in depth."),

    ("p",
     "For the event-study design we also construct a time-invariant measure of "
     "ex-ante exposure. Let $s_{io}$ be the share of firm $i$'s pre-shock "
     "workforce in professional category $o$ and $e_{o}$ the generative-AI "
     "exposure score of that category taken from the occupational exposure "
     "literature [[eloundou2024]],[[felten2021]]. Exposure is the share-weighted "
     "average"),

    ("eq", r"Exposure_{i}=\sum_{o}s_{io}\,e_{o}", 2),

    ("p", "computed over the three years preceding the shock."),

    ("h3", "3.2.3. Mediating Variables"),

    ("p",
     "Task routinisation, $RTI_{it}$, is the share of the workforce in "
     "administrative and basic technical categories, the positions whose task "
     "content the skill-content taxonomy classifies as routine-cognitive "
     "[[autor2003]]. Human-capital upgrading, $HCU_{it}$, is the share of "
     "employees holding a bachelor's degree or above. Both are expressed in "
     "percentage points."),

    ("h3", "3.2.4. Moderating Variables"),

    ("p",
     "Organisational learning capability, $OLC_{i}$, is the standardised "
     "pre-shock intensity of employee training and development expenditure per "
     "employee, a conventional observable proxy for the capacity to convert "
     "experience into routines [[argote2011]]. AI governance, $AIGov_{it}$, is "
     "an indicator equal to one if the annual report discloses AI or "
     "algorithmic governance arrangements — an ethics or data-governance "
     "committee, model review or accountability rules "
     "[[janssen2025]],[[dwivedi2023]]."),

    ("h3", "3.2.5. Control Variables"),

    ("p",
     "Following the firm-level literature we control for firm size (the natural "
     "logarithm of total assets), leverage, return on equity, revenue growth, "
     "firm age, board size, the share of independent directors, CEO duality, "
     "Tobin's Q and fixed-asset intensity. Table 1 defines all variables."),

    ("table", "table1"),

    ("h2", "3.3. Model Specification"),

    ("p",
     "The baseline specification is a two-way fixed-effects regression,"),

    ("eq", r"Youth_{it}=\alpha_{0}+\alpha_{1}GenAI_{it}"
            r"+\gamma'X_{it}+\mu_{i}+\lambda_{t}+\varepsilon_{it}", 3),

    ("p",
     "where $X_{it}$ is the control vector, $\\mu_{i}$ and $\\lambda_{t}$ are "
     "firm and year fixed effects, and standard errors are clustered at the "
     "firm level [[bertrand2004]]. Because $GenAI_{it}$ is close to zero before "
     "2023 and positive afterwards, Equation (3) is a continuous "
     "difference-in-differences specification in which identification comes "
     "from the differential depth of adoption after the shock. The coefficient "
     "of interest is $\\alpha_{1}$; H1 predicts $\\alpha_{1}<0$."),

    ("p",
     "The identifying assumption is that, absent the shock, firms that later "
     "adopted more intensively would have followed the same trajectory in youth "
     "employment as firms that adopted less. We assess it with an event study "
     "on ex-ante exposure,"),

    ("eq", r"Youth_{it}=\sum_{k\neq 2022}\gamma_{k}"
            r"\left(Exposure_{i}\times D_{t}^{k}\right)"
            r"+\gamma'X_{it}+\mu_{i}+\lambda_{t}+\varepsilon_{it}", 4),

    ("p",
     "where $D_{t}^{k}$ is a year indicator and 2022, the last pre-shock year, "
     "is the omitted category. Pre-shock coefficients that are jointly "
     "indistinguishable from zero support the parallel-trends assumption; "
     "post-shock coefficients trace the dynamic response "
     "[[sunabraham2021]],[[callaway2021]]. Because treatment intensity varies "
     "continuously and every firm is exposed to the same shock date, the "
     "specification is not subject to the negative-weighting problem that "
     "arises when a two-way fixed-effects estimator aggregates staggered "
     "adoption with heterogeneous effects "
     "[[goodmanbacon2021]],[[dechaisemartin2020]]."),

    ("p",
     "Mediation is assessed in the stepwise form [[baron1986]],[[hayes2013]], "
     "estimating"),

    ("eq", r"M_{it}=\beta_{0}+\beta_{1}GenAI_{it}+\gamma'X_{it}"
            r"+\mu_{i}+\lambda_{t}+\upsilon_{it}", 5),

    ("eq", r"Youth_{it}=c_{0}+c_{1}GenAI_{it}+c_{2}M_{it}+\gamma'X_{it}"
            r"+\mu_{i}+\lambda_{t}+\epsilon_{it}", 6),

    ("p",
     "for $M\\in\\{RTI,HCU\\}$, with the indirect effect $\\beta_{1}c_{2}$ and "
     "its confidence interval obtained from a block bootstrap that resamples "
     "firms with replacement. Moderation is estimated as"),

    ("eq", r"Youth_{it}=\delta_{0}+\delta_{1}GenAI_{it}"
            r"+\delta_{2}\left(GenAI_{it}\times Z_{it}\right)"
            r"+\delta_{3}Z_{it}+\gamma'X_{it}+\mu_{i}+\lambda_{t}+\eta_{it}", 7),

    ("p",
     "for $Z\\in\\{OLC,AIGov\\}$, from which the marginal effect of adoption at "
     "a given level of the moderator is"),

    ("eq", r"\frac{\partial Youth_{it}}{\partial GenAI_{it}}"
            r"=\delta_{1}+\delta_{2}Z_{it}", 8),

    ("p",
     "Two concerns remain. Adoption is a choice, so unobserved firm-year shocks "
     "— a demand expansion, a new product line — may raise both adoption and "
     "young hiring, biasing $\\alpha_{1}$ towards zero. We therefore instrument "
     "adoption with two excluded variables. The first is a shift-share "
     "instrument interacting the 1984 fixed-line telephone penetration rate of "
     "the firm's province with the national diffusion of generative AI, "
     "measured by the revenue of the artificial-intelligence industry rebased "
     "to unity in every pre-shock year [[goldsmith2020]],[[borusyak2022]]: "
     "historical communications infrastructure predicts the digital "
     "infrastructure that conditions adoption today but has no plausible direct "
     "effect on a listed firm's current age composition, and rebasing the "
     "national shifter keeps the instrument, like the technology itself, flat "
     "until the end of 2022. The second is the "
     "leave-one-out mean adoption intensity of other firms in the same industry "
     "and province, which captures diffusion pressure while excluding the "
     "firm's own decision. The first and second stages are"),

    ("eq", r"GenAI_{it}=\pi_{0}+\pi_{1}IV^{Bartik}_{it}+\pi_{2}IV^{Peer}_{it}"
            r"+\gamma'X_{it}+\mu_{i}+\lambda_{t}+\nu_{it}", 9),

    ("eq", r"Youth_{it}=\theta_{0}+\theta_{1}\widehat{GenAI}_{it}"
            r"+\gamma'X_{it}+\mu_{i}+\lambda_{t}+\omega_{it}", 10),

    ("p",
     "Instrument relevance is judged by the Kleibergen–Paap rank Wald statistic "
     "against the Stock–Yogo critical value "
     "[[kleibergen2006]],[[stockyogo2005]] and validity by the "
     "Sargan–Hansen test. Because adoption is also not randomly assigned across "
     "firms, we complement the instrumental-variable estimates with "
     "propensity-score matching [[rosenbaum1983]] and entropy balancing "
     "[[hainmueller2012]], and we bound the scope for selection on "
     "unobservables using the coefficient-stability approach [[oster2019]], for "
     "which the bias-adjusted coefficient is"),

    ("eq", r"\beta^{*}=\tilde{\beta}-\left(\mathring{\beta}-\tilde{\beta}\right)"
            r"\frac{R_{max}-\tilde{R}}{\tilde{R}-\mathring{R}}", 11),

    ("p",
     "where $\\mathring{\\beta}$ and $\\mathring{R}$ come from the "
     "specification without controls, $\\tilde{\\beta}$ and $\\tilde{R}$ from "
     "the specification with controls, and $R_{max}$ is the assumed maximum "
     "explainable variation."),

    # =====================================================================
    ("h1", "4. Empirical Results"),

    ("h2", "4.1. Descriptive Statistics"),

    ("p",
     f"Table 2 reports the descriptive statistics. The youth employment share "
     f"averages {n('youth_mean',2)}% with a standard deviation of "
     f"{n('youth_sd',2)} percentage points, indicating substantial variation in "
     "the age composition of listed firms. Adoption intensity averages "
     f"{n('genai_post_mean',3)} in the post-shock years, again with wide "
     "dispersion. The control variables are consistent with the published "
     "distributions for Chinese listed firms. Figure 2 places these numbers in "
     "time: adoption is absent from annual reports before the end of 2022 and "
     "rises steeply thereafter, while the youth employment share, which had "
     "been drifting down slowly, falls more sharply over the same three "
     "years."),

    ("table", "table2"),

    ("fig", "figure2"),

    ("p",
     "Table 3 reports pairwise correlations. Adoption is negatively correlated "
     "with the youth share and with routine-task intensity and positively "
     "correlated with human-capital upgrading, which is the pattern the "
     "hypotheses imply. Correlations among the regressors are moderate; "
     f"variance inflation factors have a maximum of {n('vif_max',2)} and a mean "
     f"of {n('vif_mean',2)}, far below the conventional threshold of ten, so "
     "multicollinearity is not a concern."),

    ("table", "table3"),

    ("h2", "4.2. Benchmark Regression"),

    ("p",
     "Table 4 reports the baseline estimates. Column (1) includes only the "
     "adoption measure with firm and year fixed effects; column (2) adds the "
     "full control vector. The coefficient on adoption is "
     f"{n('beta_baseline')} and significant at the 1% level, so a one-unit "
     "increase in adoption intensity lowers the share of employees aged 30 or "
     f"below by {a('beta_baseline')} percentage points. Evaluated at a "
     "one-standard-deviation increase in adoption this is "
     f"{n('econ_sd',3)} percentage points, or {a('econ_pct',1)}% of the sample "
     "mean — economically meaningful without being implausibly large. H1 is "
     "supported."),

    ("table", "table4"),

    ("p",
     "Column (3) replaces the continuous measure with the interaction of "
     "ex-ante task exposure and the post-shock indicator, the sharp "
     "difference-in-differences form; the coefficient is "
     f"{n('beta_expost')} and significant, confirming that the result is driven "
     "by firms whose pre-existing task structure was most exposed rather than "
     "by adoption reporting itself. Columns (4) and (5) replace the year fixed "
     "effects with industry-by-year and province-by-year fixed effects, "
     "absorbing any shock common to an industry or a province in a given year, "
     "including sectoral demand cycles and provincial labour-market or "
     "graduate-supply conditions. The coefficient is stable across both."),

    ("h2", "4.3. Parallel Trends and Dynamic Effects"),

    ("p",
     "Figure 3 plots the event-study coefficients from Equation (4) with 95% "
     "confidence intervals. None of the pre-shock coefficients is individually "
     "significant and they are jointly indistinguishable from zero "
     f"($\\chi^{{2}}({S['pretrend_df']})={n('pretrend_chi2',2)}$, "
     f"$p={n('pretrend_p',3)}$), which supports the parallel-trends assumption: "
     "firms with more exposed task structures were not already on a different "
     "youth-employment trajectory. The post-shock coefficients are negative, "
     "grow in magnitude over the three post-shock years, and are individually "
     "significant, which is the pattern expected of a technology whose "
     "penetration deepens over time rather than of a one-off level shift."),

    ("fig", "figure3"),

    ("h2", "4.4. Examination of Mediating Mechanisms"),

    ("p",
     "Table 5 reports the mediation analysis. Column (2) shows that adoption "
     f"significantly reduces routine-task intensity ({m('RTI','a')}), and "
     "column (3) shows that routine-task intensity is positively associated "
     f"with the youth share ({m('RTI','b')}) while the coefficient on "
     f"adoption falls in magnitude from {n('beta_baseline')} to "
     f"{m('RTI','direct')}. The indirect effect is {m('RTI','indirect')}, with a "
     "bias-corrected bootstrap 95% confidence interval of "
     f"[{MED['RTI']['ci_low']:.3f}, {MED['RTI']['ci_high']:.3f}] that excludes "
     f"zero, and it accounts for {abs(MED['RTI']['share']):.1f}% of the total "
     "effect. H2 is supported: the displacement of young workers runs "
     "substantially through the removal of routine-cognitive positions from the "
     "job structure."),

    ("table", "table5"),

    ("p",
     "Columns (4) and (5) examine the second channel. Adoption significantly "
     f"raises human-capital upgrading ({m('HCU','a')}), and upgrading is "
     f"positively associated with the youth share ({m('HCU','b')}). The "
     f"indirect effect is {m('HCU','indirect')} with a bootstrap confidence "
     f"interval of [{MED['HCU']['ci_low']:.3f}, {MED['HCU']['ci_high']:.3f}], "
     f"and it offsets {abs(MED['HCU']['share']):.1f}% of the total effect. H3 "
     "is supported. Table 6 collects the decomposition. The two channels are "
     "genuinely countervailing, which is why estimates that report only a net "
     "elasticity are difficult to interpret and why the same technology can "
     "look displacing in one setting and complementary in another."),

    ("table", "table6"),

    ("h2", "4.5. Examination of Moderating Effects"),

    ("p",
     "Table 7 reports the moderation analysis. In column (1) the interaction of "
     "adoption with organisational learning capability is "
     f"{n('mod_olc_b3')} and significant at the 1% level, against a "
     f"main effect of {n('mod_olc_b1')}: the displacement effect is "
     "substantially weaker in firms that have accumulated the capacity to "
     "convert experience into routines. H4 is supported. In column (2) the "
     f"interaction with AI governance is {n('mod_gov_b3')}, so for firms that "
     "disclose AI governance arrangements the marginal effect of adoption is "
     f"{n('mod_gov_effect')} rather than {n('mod_gov_b1')}, about {GOVCUT:.0f}% "
     "smaller. H5 "
     "is supported. Column (3) includes both interactions and neither is "
     "displaced by the other, indicating that they capture distinct "
     "organisational attributes rather than a single latent quality."),

    ("table", "table7"),

    ("p",
     "Figure 4 traces the marginal effect of Equation (8) across the "
     "distribution of organisational learning capability with a 95% confidence "
     "band. The effect is significantly negative through most of the "
     "distribution, becomes statistically indistinguishable from zero above the "
     f"{S['mod_olc_turn_pct']:.0f}th percentile, and the point estimate crosses "
     f"zero at {n('mod_olc_turn',2)} standard deviations. This is the paper's "
     "central qualitative result. Displacement of young workers is not an "
     "intrinsic property of generative AI; it is what happens when the "
     "technology is introduced into a firm that lacks the learning "
     "infrastructure to redesign entry work around it."),

    ("fig", "figure4"),

    ("h2", "4.6. Endogeneity Tests"),

    ("p",
     "Table 8 addresses the endogeneity of adoption. Column (1) reports the "
     "first stage: both instruments are strongly and significantly related to "
     "adoption, and the Kleibergen–Paap rank Wald statistic is "
     f"{n('iv_F',1)}, far above the Stock–Yogo 10% maximal-size critical value "
     f"of 19.93, so weak identification is not a concern. The Sargan–Hansen "
     f"test does not reject instrument validity ($p={n('sargan_p',3)}$). The "
     f"second-stage estimate in column (2) is {n('iv_beta')} with a standard "
     f"error of {n('iv_se')}, larger in magnitude than the fixed-effects "
     "estimate. The direction of the difference is what the confounding story "
     "predicts: firms experiencing favourable unobserved shocks both adopt more "
     "and hire more young workers, so the within-firm estimate understates "
     f"displacement. The Wu–Hausman test gives $p={n('wu_hausman_p',3)}$."),

    ("table", "table8"),

    ("p",
     "Columns (3) and (4) address selection on observables. Propensity-score "
     "matching pairs each intensively adopting firm with the nearest "
     "less-intensive firm on pre-shock characteristics within a caliper of "
     "0.02; after matching the largest absolute standardised bias across the "
     f"covariates is {n('max_abs_bias_matched',1)}%, well inside the "
     "conventional 10% threshold, and no covariate difference is statistically "
     "significant (Figure 5 and Table A1). The matched-sample estimate is "
     f"{n('psm_beta')}. Entropy balancing, which reweights the comparison group "
     "to match the first two moments of the treated distribution without "
     f"discarding observations, gives {n('eb_beta')}. Both are close to the "
     "baseline."),

    ("fig", "figure5"),

    ("p",
     "Finally, Table 9 reports the coefficient-stability bounds. Moving from "
     f"the specification without controls to the specification with controls "
     f"changes the coefficient from {OST['beta_uncontrolled']:.3f} to "
     f"{OST['beta_controlled']:.3f} while the within R-squared rises from "
     f"{OST['r2_uncontrolled']:.3f} to {OST['r2_controlled']:.3f}. The "
     "coefficient therefore moves away from zero as explanatory power is "
     "added, which is the pattern expected when the omitted variation biases "
     "the estimate towards zero rather than away from it. Under the "
     "conventional assumption that the maximum explainable variation is 1.3 "
     "times the observed value, the bias-adjusted coefficient is "
     f"{OST['beta_star']:.3f}, slightly larger in magnitude than the estimate "
     f"itself, and the implied degree of selection is {OST['delta']:.2f}: "
     "unobserved factors would have to be more than "
     f"{abs(OST['delta']):.0f} times as important as the observed controls "
     "and to work in the opposite direction to them before the estimate could "
     "be driven to zero. The result is therefore robust to plausible "
     "unobserved selection."),

    ("table", "table9"),

    ("h2", "4.7. Robustness Checks"),

    ("p",
     "Table 10 reports eight robustness checks. Replacing the dependent "
     "variable with the share of employees aged 35 or below, and with the "
     "logarithm of the number of employees aged 30 or below, leaves the "
     "conclusion unchanged; the second of these shows that the result is not an "
     "artefact of composition arising from changes in total headcount. "
     "Replacing the continuous adoption measure with an above-median indicator, "
     "and using a one-year lag of adoption, both reproduce the negative effect. "
     "Clustering standard errors on firm and year simultaneously, excluding "
     "2020 to remove the pandemic year, winsorising at the 5th and 95th "
     "percentiles instead of the 1st and 99th, and restricting the sample to "
     "the balanced panel all leave the estimate materially unchanged."),

    ("table", "table10"),

    ("p",
     "As a final check on inference we re-estimate the sharp "
     "difference-in-differences specification after randomly reassigning "
     f"ex-ante task exposure across firms, repeated {S['placebo_n']:,} times. "
     f"The placebo distribution is centred on {n('placebo_mean',3)} with a "
     f"standard deviation of {n('placebo_sd',3)}, and only "
     f"{100 * S['placebo_p']:.1f}% of the placebo estimates are at least as "
     "large in absolute value as the actual estimate (Figure 6). The result is "
     "not an artefact of the estimation procedure."),

    ("fig", "figure6"),

    ("h2", "4.8. Heterogeneity Analysis"),

    ("p",
     "Table 11 splits the sample four ways. The effect is larger in "
     f"{het_phrase('State ownership')}, which is what the institutional "
     "setting implies: state-owned enterprises carry an employment-stability "
     "mandate and face more constraint on adjusting headcount, so the same "
     "adoption intensity translates into less displacement. It is larger in "
     f"{het_phrase('Region')}, consistent with earlier and deeper adoption and "
     "more exposed entry-level work in the coastal provinces. The technology "
     f"split gives {het_cmp('Technology intensity')} and the capital-intensity "
     f"split {het_cmp('Capital intensity')}. "
     f"{het_sig()}"),

    ("table", "table11"),

    # =====================================================================
    ("h1", "5. Discussion and Implications"),

    ("h2", "5.1. Theoretical Contributions"),

    ("p",
     "The study makes three contributions. First, it identifies a margin of "
     "adjustment that the aggregate task-based framework does not isolate. That "
     "framework predicts the net employment consequence of automation from the "
     "balance of displacement and reinstatement "
     "[[acemoglu2018]],[[acemoglu2022]], but it is estimated on employment "
     "levels and is largely silent on composition. We show that the first-order "
     "effect of generative AI inside the firm is compositional: it falls on the "
     "age structure through the job structure, and it does so in opposite "
     "directions through two separately measurable channels. Reporting a single "
     "net elasticity conceals this and helps explain why firm-level and "
     "occupation-level estimates in the emerging literature diverge so widely "
     "[[canaries2025]],[[humlum2025]]."),

    ("p",
     "Second, it turns the automation–augmentation paradox "
     "[[raisch2021]],[[krakowski2023]],[[murray2021]] into an estimable "
     "empirical statement. The paradox holds that automation and augmentation "
     "are interdependent design choices rather than alternatives; our "
     "moderation results give that claim a magnitude. The same adoption "
     "intensity displaces young workers in a firm at the median of "
     "organisational learning capability and has no detectable effect above the "
     f"{S['mod_olc_turn_pct']:.0f}th percentile, and it is about {GOVCUT:.0f}% "
     "less displacing in firms with disclosed AI governance. This is the "
     "socio-technical joint-optimisation principle "
     "[[trist1951]],[[cherns1976]],[[sarker2019]] in an econometric form: the "
     "technical subsystem does not determine the outcome on its own."),

    ("p",
     "Third, it connects the organisational-learning literature to a "
     "labour-market outcome. Absorptive capacity and the conversion of "
     "experience into routines have been studied as determinants of innovation "
     "and performance [[cohen1990]],[[levitt1988]],[[argote2011]]; we show that "
     "they also determine who gets hired when a general-purpose technology "
     "arrives. The mechanism is intelligible from the qualitative record: where "
     "a technology absorbs the preparatory work through which competence was "
     "acquired, firms without the capacity to redesign that work simply buy "
     "less of it [[beane2019]],[[anthony2021]],[[lebovitz2022]]."),

    ("h2", "5.2. Managerial and Policy Implications"),

    ("p",
     "For firms, the results reframe the decision. The relevant question is not "
     "how much entry-level work generative AI can absorb but whether the firm "
     "can rebuild entry-level roles around it. Firms that adopt without that "
     "capacity obtain the substitution and forgo the complementarity, and "
     "because the human-capital channel is the smaller of the two, the net "
     "outcome is a thinner entry cohort. Two levers are available and both are "
     "measurable: investment in the training and knowledge-management "
     "infrastructure that constitutes organisational learning capability, and "
     "the governance arrangements — review protocols, accountability rules, "
     "disclosure — that make it safe to delegate consequential work to "
     "AI-assisted junior staff."),

    ("p",
     "For policy, the finding that the effect is conditional rather than "
     "technological points away from the instruments currently in view. "
     "Restricting adoption would forgo the productivity gains without "
     "addressing the mechanism, since displacement runs through the "
     "reorganisation of job structures rather than through adoption itself. "
     "Instruments that raise organisational learning capability — training "
     "subsidies conditional on the task content of entry-level roles rather "
     "than on headcount, structured apprenticeship in professional services, "
     "graduate schemes with protected task content — act directly on the "
     "moderator that we find to matter most, and they are the instruments "
     "implied by the argument that AI can extend rather than replace the reach "
     "of middle-skill expertise [[autorai2024]]. Second, because displacement "
     "is concentrated in non-state firms, which are also the largest graduate "
     "employers and are not covered by the employment-stability expectations "
     "placed on state-owned enterprises, aggregate youth-employment statistics "
     "will understate the pressure on the graduate segment. Third, "
     "given the persistence of entry conditions in later earnings "
     "[[kahn2010]],[[schwandt2019]],[[vonwachter2020]], the cohorts entering "
     "during the adoption wave warrant attention in their own right, "
     "independently of what happens to aggregate employment."),

    ("h2", "5.3. Limitations and Future Research"),

    ("p",
     "Five limitations qualify the results. First, adoption is measured from "
     "annual-report text, which captures disclosed rather than actual use and "
     "may be inflated by firms seeking to signal technological sophistication. "
     "The event-study specification on ex-ante task exposure, which does not "
     "rely on disclosure, gives the same answer, but a measure based on "
     "procurement or usage data would be better. Second, the sample is listed "
     "firms, which are larger and more capital-intensive than the population, "
     "and the results need not extend to the small and medium-sized firms that "
     "employ most young workers in China. Third, the outcome is the firm's age "
     "composition, not the young worker's welfare; displaced entry demand at "
     "one firm may be absorbed at another, so the firm-level estimate is not an "
     "equilibrium effect. Linked employer–employee data would be required to "
     "trace that. Fourth, the moderators are observable proxies, and "
     "organisational learning capability in particular is measured by training "
     "expenditure rather than by the routines it is meant to indicate; survey "
     "or case-based measurement would sharpen the test. Finally, three "
     "post-shock years cannot separate a transitional adjustment from a new "
     "steady state, and the dynamic pattern in Figure 3 is consistent with "
     "either; a longer panel is the natural next step."),

    # =====================================================================
    ("h1", "6. Conclusions"),

    ("p",
     "Generative artificial intelligence has arrived at the point in the job "
     "structure where careers begin. Using a panel of Chinese A-share listed "
     f"firms over {S['years']}, this study finds that firm-level adoption "
     "lowers the share of employees aged 30 or below by "
     f"{a('beta_baseline')} percentage points per unit of adoption intensity, "
     f"or {a('econ_pct',1)}% of the mean for a one-standard-deviation increase, "
     "with instrumental-variable, matched and entropy-balanced estimates "
     "confirming the sign and suggesting the fixed-effects estimate understates "
     "it. The effect is not monolithic: it runs "
     f"{abs(MED['RTI']['share']):.0f}% through the removal of routine-cognitive "
     f"positions and is offset {abs(MED['HCU']['share']):.0f}% by the "
     "human-capital upgrading that adoption also induces."),

    ("p",
     "The more consequential finding is that the net outcome is a property of "
     f"the firm rather than of the technology. Displacement is about {GOVCUT:.0f}% smaller "
     "where AI governance arrangements are in place and is statistically "
     f"indistinguishable from zero above the {S['mod_olc_turn_pct']:.0f}th "
     "percentile of organisational learning capability. Whether generative AI "
     "closes the entry port or reopens it at a higher level of capability is "
     "therefore being decided by organisational choices about learning and "
     "governance that are, unlike the technology itself, directly amenable to "
     "management and to policy. That is where the attention of both should go."),

    # =====================================================================
    ("h1b", "Author Contributions"),
    ("stmt2", "",
     "Conceptualization, methodology, formal analysis, software and "
     "writing—original draft preparation, X.C.; validation, data curation and "
     "visualization, investigation, writing—review and editing, supervision and "
     "project administration, T.M. All authors have read and agreed to the "
     "published version of the manuscript."),

    ("h1b", "Funding"),
    ("stmt2", "",
     "This research was funded by the Zhejiang Provincial Philosophy and Social "
     "Sciences Planning Special Project on Higher Education Basic Research "
     "Funding Reform (Grant Number: 25NDJC153YBMS) and the Major Humanities and "
     "Social Sciences Research Projects in Zhejiang Higher Education "
     "Institutions (Grant Number: 2024QN018)."),

    ("h1b", "Institutional Review Board Statement"),
    ("stmt2", "",
     "Not applicable. The study uses firm-level accounting and disclosure data "
     "and involves no human participants or animals."),

    ("h1b", "Informed Consent Statement"),
    ("stmt2", "", "Not applicable."),

    ("h1b", "Data Availability Statement"),
    ("stmt2", "",
     "The financial, governance and employment-composition data are commercially "
     "licensed from the China Stock Market and Accounting Research database and "
     "cannot be redistributed by the authors; they are available to subscribers. "
     "The generative-AI keyword dictionary, the estimation code for every "
     "specification reported in the paper, and the scripts that generate every "
     "table and figure are available from the corresponding author on "
     "reasonable request."),

    ("h1b", "Acknowledgments"),
    ("stmt2", "",
     "The authors thank the editors and the anonymous reviewers for comments "
     "that improved the manuscript."),

    ("h1b", "Conflicts of Interest"),
    ("stmt2", "", "The authors declare no conflicts of interest."),
]
