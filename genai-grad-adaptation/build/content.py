# -*- coding: utf-8 -*-
"""Manuscript text.

Every quantitative statement is interpolated from analysis/run_all.py output
(tables/summary.json), so the prose cannot drift away from the tables.

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

MED = S["med"]
UT = S["ut"]
TP = S["tp"]
CFA = S["cfa"]


def n(key, d=3):
    return "%.*f" % (d, S[key])


def a(key, d=3):
    return "%.*f" % (d, abs(S[key]))


def m(key, field="est", d=3):
    return "%.*f" % (d, MED[key][field])


def mci(key, d=3):
    e = MED[key]
    return "[%.*f, %.*f]" % (d, e["lo"], d, e["hi"])


def pfmt(x):
    """A p-value as journals set it: never a bare zero."""
    return "< 0.001" if x < 0.001 else "= %.3f" % x


TITLE = ("Early-Career Choices in the Era of Generative AI: Human Capital "
         "Depreciation, Career Anxiety, and Occupational Adaptation Among "
         "Fresh Graduates")

AUTHORS = [("Xinyu Cai ", False), ("1", True), (" and Tiantian Mo ", False),
           ("1,*", True)]

AFFILIATIONS = [
    ("1", "College of Business, Jiaxing University, Jiaxing 314001, China; "
          "caixinyu@zjxu.edu.cn"),
    ("*", "Correspondence: 00008227@zjxu.edu.cn"),
]

ABSTRACT = (
    "As generative artificial intelligence (GenAI) becomes most capable at "
    "precisely the entry-level tasks from which early careers have "
    "traditionally been built, fresh graduates must make their first "
    "occupational choices under conditions no previous cohort has faced. "
    "Drawing on socio-technical systems theory and a cybernetic control "
    "perspective, this study investigates how graduates\u2019 perceived "
    "human capital depreciation translates into AI-related career anxiety "
    "and, in turn, into occupational adaptation or career avoidance, and "
    "which combinations of conditions govern this process. Using a two-wave "
    f"survey of {S['n_t1']:,} Chinese fresh graduates within three years of "
    f"graduation ({S['n_t2']:,} matched across waves, with behavioral "
    "outcomes measured six months after their antecedents), we employ "
    "confirmatory factor analysis, bootstrapped conditional-process models, "
    "and fuzzy-set qualitative comparative analysis (fsQCA). The study "
    "finds that (1) perceived human capital depreciation significantly "
    f"raises AI-related career anxiety (\u03b2 = {n('a1')}), and perceived "
    "employability support buffers this first stage, reducing the "
    f"pass-through from {S['fslo']['est']:.2f} to {S['fshi']['est']:.2f}; "
    "(2) career anxiety exhibits an inverted U-shaped relationship with "
    "occupational adaptation, with a turning point "
    f"{TP['tau']:.2f} standard deviations above the mean anxiety level, "
    f"beyond which {n('share_beyond', 1)} percent of graduates already "
    "fall, whereas career avoidance rises monotonically; (3) GenAI "
    "literacy displaces the turning point outward from "
    f"{S['tp_lit'][0]['tau']:.2f} to {S['tp_lit'][2]['tau']:.2f} standard "
    "deviations, extending the range over which anxiety remains "
    "productive; and (4) the fsQCA identifies a single sufficient "
    "configuration for high adaptation, the conjunction of anxiety, "
    f"literacy, and support (consistency {S['qca']['sol_cons']:.3f}), "
    "with no necessary condition and no consistent configuration for its "
    "negation, so anxiety alone never suffices. This study deepens the "
    "systems understanding of GenAI-era workforce development by modeling "
    "career anxiety as the error signal of an adaptive feedback loop, and "
    "offers practical guidance for universities, employers, and "
    "policymakers seeking to convert a record cohort\u2019s anxiety into "
    "adaptation rather than avoidance.")

KEYWORDS = ("generative artificial intelligence; career anxiety; human "
            "capital depreciation; occupational adaptation; "
            "socio-technical systems")

BLOCKS = [
    # =====================================================================
    ("h1", "1. Introduction"),

    ("p",
     "Every technological transition redistributes opportunity across the "
     "age distribution, but the present one is unusual in where it strikes "
     "first. Generative artificial intelligence performs best on the "
     "codifiable, language-intensive, well-specified tasks that have "
     "traditionally been assigned to the newest members of the professions "
     "[[eloundou2024],[felten2021],[noy2023]]. Field and quasi-experimental "
     "evidence now shows entry positions contracting where the technology "
     "is adopted: junior-heavy hiring falls in exposed occupations "
     "[[canaries2025],[hui2024]], the productivity gains of the technology "
     "accrue disproportionately to novices while the demand for novices "
     "weakens [[brynjolfsson2025],[dellacqua2026]], and employers "
     "increasingly describe entry roles in terms of supervising machine "
     "output rather than producing it [[autorai2024],[autor2024]]. For the "
     "roughly twelve million students who now graduate from Chinese higher "
     "education each year [[moe2025],[li2014]], these are not abstractions. "
     "They are the conditions under which the first occupation, the first "
     "investments in skill, and the first revisions of both must be chosen."),

    ("p",
     "Economics has begun to measure what the technology does to the "
     "demand side of this market [[acemoglu2022],[autor2015],"
     "[acemoglu2018]]. Much less is known about the supply side: how the "
     "entrants themselves perceive the depreciation of their just-acquired "
     "human capital, what that perception does to them emotionally, and "
     "when the emotion converts into behavior that improves their position "
     "rather than behavior that worsens it. The question matters because "
     "early-career scarring is among the most persistent phenomena in labor "
     "economics: cohorts that stumble at entry carry lower earnings and "
     "worse matches for a decade or more [[kahn2010],[oreopoulos2012],"
     "[schwandt2019],[vonwachter2020]]. If the first cohort of the "
     "generative-AI era responds to depreciation signals with paralysis "
     "rather than adaptation, the technology's distributional effects will "
     "be amplified by the very psychology of those it displaces."),

    ("p",
     "This study asks three questions. First, how does the perception that "
     "generative artificial intelligence is depreciating one's human "
     "capital translate into AI-related career anxiety? Second, when does "
     "that anxiety mobilize occupational adaptation, and when does it tip "
     "into avoidance? Third, which combinations of psychological and "
     "contextual conditions are jointly sufficient for adaptation? The "
     "questions are posed from an explicitly systems-theoretic position, "
     "which is what distinguishes this paper from the emerging literature "
     "on artificial-intelligence anxiety [[wangwang2022],[kong2021],"
     "[brougham2018]]. The graduate is modeled as an adaptive agent inside "
     "a socio-technical labor system [[trist1951],[emery1965]]: the "
     "depreciation percept is the input, anxiety is the error signal of a "
     "control loop that compares the career one has with the career one "
     "expected [[carver1982],[ashby1956]], and reskilling, occupational "
     "repositioning or withdrawal are the actions through which the loop "
     "closes. Three properties follow from this framing, and each is "
     "testable. A control signal should transmit the input (mediation); an "
     "error signal that saturates should stop producing corrective action "
     "at high amplitude (nonlinearity); and the action should depend on "
     "the actuators available to the agent, namely capability and support "
     "(conjunction). The empirical design maps one to one onto these "
     "properties."),

    ("p",
     "Evidence comes from a two-wave survey of Chinese graduates within "
     "thirty-six months of graduation, with perceptions and psychological "
     "states measured at the first wave and adaptation behaviors measured "
     "six months later, so that the outcomes are separated from their "
     "hypothesized antecedents in time. The analysis combines a "
     "confirmatory measurement model, bootstrapped conditional-process "
     "estimation with an explicitly curvilinear second stage "
     "[[edwards2007],[hayes2015],[haans2016]], and fuzzy-set qualitative "
     "comparative analysis [[ragin2008],[fiss2011],[pappas2021]], the "
     "latter because a systems argument about conjunction cannot be tested "
     "by adding interaction terms alone [[greckhamer2018]]."),

    ("p",
     "Four results organize the paper. First, perceived human capital "
     f"depreciation converts into career anxiety at β = {n('a1')} and the "
     "conversion is buffered by perceived employability support: the "
     f"pass-through is {S['fslo']['est']:.2f} one standard deviation below "
     f"the mean of support and {S['fshi']['est']:.2f} one standard "
     "deviation above it. Second, the anxiety-adaptation relationship is "
     "an inverted U, not a slope. Adaptation peaks at "
     f"{TP['tau']:.2f} standard deviations of anxiety, and "
     f"{n('share_beyond', 1)} percent of the cohort already sits beyond "
     "the peak, in the region where additional anxiety predicts less "
     "adaptation; avoidance, by contrast, rises monotonically across the "
     "entire observed range. Third, generative-AI literacy does not merely "
     "raise adaptation, it moves the turning point: from "
     f"{S['tp_lit'][0]['tau']:.2f} standard deviations among low-literacy "
     f"graduates to {S['tp_lit'][2]['tau']:.2f} among high-literacy ones, "
     "so that literacy extends the range over which anxiety remains "
     "productive. Fourth, the configurational analysis returns exactly one "
     "sufficient recipe for high adaptation, the conjunction of anxiety "
     "with literacy and support (consistency "
     f"{S['qca']['sol_cons']:.3f}, coverage {S['qca']['sol_cov']:.3f}); no "
     "single condition is necessary, no configuration lacking either "
     "literacy or support passes the sufficiency thresholds, and no "
     "consistent recipe exists for the negation. Equifinality, the "
     "default expectation of configurational research, fails here in a "
     "theoretically informative way: there is one road to adaptation, and "
     "anxiety alone is never it."),

    ("p",
     "The contribution is threefold. To the economics and management "
     "literature on generative artificial intelligence and work "
     "[[brynjolfsson2025],[babina2024],[acemoglu2022]], the paper adds the "
     "supply-side psychology of the displaced margin: the first "
     "individual-level evidence that the entry cohort's behavioral "
     "response to depreciation is nonmonotonic, which changes what "
     "aggregate adjustment models should assume about retraining uptake. "
     "To the artificial-intelligence anxiety literature [[wangwang2022],"
     "[kong2021],[tarafdar2007]], it contributes the systems treatment: "
     "anxiety modeled and estimated as the error signal of a feedback "
     "loop, with the saturation, the actuator-dependence and the "
     "conjunction that the control-theoretic reading predicts "
     "[[carver1982],[ashby1956],[holland1995]]. To the special issue's "
     "question of how generative artificial intelligence reshapes "
     "workforce development as a system [[dwivedi2023],[janssen2025]], it "
     "offers a concrete demonstration that the productive unit of analysis "
     "is neither the individual nor the technology but the loop that "
     "couples perception, emotion, capability and institutional support, "
     "and that policy which addresses only one element of the loop, such "
     "as reassuring messaging that damps the signal, can be worse than "
     "policy which completes it."),

    ("p",
     "The remainder of the paper is organized as follows. Section 2 "
     "develops the theory and seven hypotheses. Section 3 describes the "
     "sample, the measures and the analysis strategy. Section 4 reports "
     "the measurement model, the structural estimates, the "
     "conditional-process analysis, the heterogeneity and robustness "
     "batteries and the configurational results. Section 5 discusses "
     "theoretical and practical implications, Section 6 acknowledges "
     "limitations, and Section 7 concludes."),

    # =====================================================================
    ("h1", "2. Theory and Hypotheses"),
    ("h2", "2.1. Fresh Graduates as Adaptive Agents in a Socio-Technical "
           "Labor System"),

    ("p",
     "A labor market entrant is not a passive recipient of technological "
     "change; they are an agent embedded in a system of universities, "
     "employers, technologies and institutions whose joint behavior "
     "determines early-career outcomes [[trist1951],[emery1965],"
     "[bertalanffy1968]]. Systems thinking supplies three ideas that "
     "discipline the analysis [[checkland1981]]. The first is the feedback "
     "loop [[forrester1961],[sterman2000]]: perceptions drive emotions, "
     "emotions drive actions, and actions feed back into the perceptions "
     "and the objective position from which the next round of choices is "
     "made. The second is the error signal of cybernetic control theory "
     "[[carver1982],[beer1981]]: an adaptive system monitors the "
     "discrepancy between its present trajectory and its reference "
     "trajectory, and the affective correlate of that discrepancy is what "
     "mobilizes correction. The third is requisite capability, the "
     "behavioral cousin of Ashby's law [[ashby1956]]: a control signal "
     "produces regulation only if the regulator commands actions varied "
     "enough to match the disturbance. An anxious graduate who cannot use "
     "the technology and has no institutional support has a loud error "
     "signal wired to no actuator."),

    ("p",
     "The disturbance in question is well documented on the demand side. "
     "Generative models write, summarize, draft, code and analyze at a "
     "level that overlaps heavily with entry-level professional work, the "
     "modern echo of the routine-task displacement long documented for "
     "earlier automation [[autor2003],[eloundou2024],[noy2023],"
     "[peng2023]], and the overlap is largest "
     "precisely in the occupations that hire educated entrants "
     "[[felten2021],[ilo2024]]. Adoption evidence links the "
     "technology to falling junior hiring in exposed firms and platforms "
     "[[canaries2025],[hui2024],[bick2024]], and experimental evidence "
     "shows the technology compressing the novice-expert productivity "
     "gradient that entry-level jobs exist to climb [[brynjolfsson2025],"
     "[dellacqua2026],[cui2026],[otis2026]] — even while economy-wide "
     "employment effects remain modest so far [[humlum2025]], which is "
     "precisely why the entry margin, where the effects concentrate "
     "[[forsythe2022]], deserves separate study. Chinese firm-level "
     "evidence points the same way [[liang2025],[xue2025],[xuejin2025],"
     "[yang2026],[machucho2025]]. What has not been studied is the "
     "perception of this disturbance by those on its receiving end, and "
     "the system through which perception becomes choice."),

    ("h2", "2.2. Perceived Human Capital Depreciation and Career Anxiety"),

    ("p",
     "Human capital depreciates when the market value of a skill stock "
     "falls, whether through wear, through vintage effects or through "
     "technological displacement of the tasks the skills perform "
     "[[becker1964],[degrip2002],[deming2020]]. The loss lands hardest on "
     "entrants because early careers are built by doing: skills are "
     "accumulated on the job [[arrow1962]], weighted and priced by the "
     "tasks a position offers [[lazear2009]], and advanced through "
     "internal ladders whose first rung is exactly the work the "
     "technology absorbs [[gibbons2004]]. What matters for behavior "
     "is not the depreciation itself but its perception. A graduate "
     "observes the capability of generative systems in their own domain, "
     "compares it with what they were trained to do, and forms a judgment "
     "about how fast the training is losing value [[chanhu2023],"
     "[brougham2018]]. In appraisal-theoretic terms this is a primary "
     "appraisal of threat to a central resource, the career [[lazarus1984]]; "
     "in conservation-of-resources terms it is anticipated resource loss, "
     "the most potent known elicitor of stress [[hobfoll1989],"
     "[hobfoll2018]]. Both traditions, and the cybernetic reading in which "
     "the percept is a widening discrepancy between expected and likely "
     "trajectory [[carver1982]], predict the same first link: perceived "
     "depreciation should convert into career-specific anxiety, the "
     "unpleasant activation state focused on one's occupational future "
     "[[pisarik2017],[wangwang2022],[kong2021]]. Accordingly:"),

    ("hyp", "H1.", "Perceived human capital depreciation is positively "
                   "associated with AI-related career anxiety."),

    ("h2", "2.3. The Dual Response: Adaptation and Avoidance"),

    ("p",
     "Anxiety is an activation state, and activation is behaviorally "
     "ambidextrous. The coping literature distinguishes problem-focused "
     "responses, which attack the stressor, from emotion-focused and "
     "avoidant responses, which attack the feeling [[lazarus1984]]. In the "
     "career domain the problem-focused response is occupational "
     "adaptation: enrolling in structured reskilling, pursuing "
     "credentials, deliberately practicing the new technology, and "
     "repositioning toward tasks the technology complements rather than "
     "substitutes [[savickas2012],[lent2013]]. The avoidant response is "
     "withdrawal: postponing career decisions, avoiding information about "
     "the technology, and contemplating exit from the chosen field "
     "[[kong2021],[brougham2018]]."),

    ("p",
     "The relationship between anxiety and the problem-focused response "
     "should not be monotone. At low levels, anxiety supplies the "
     "activation that overcomes the inertia of costly investment: this is "
     "the mobilizing arm familiar from the oldest result in behavioral "
     "activation research [[yerkes1908]] and from conservation-of-"
     "resources theory, in which moderate loss threat triggers resource "
     "investment [[hobfoll2018]]. At high levels, three mechanisms bend "
     "the curve down. Cognitively, high anxiety narrows attention and "
     "consumes the working memory that planning a retraining program "
     "requires. Motivationally, extreme threat triggers defensive "
     "avoidance rather than approach [[lazarus1984]]. And in resource "
     "terms, graduates deep in loss enter the defensive spiral in which "
     "conserving what remains dominates investing in what could be "
     "[[hobfoll2018]]. The general form of this argument, that a "
     "productive input becomes counterproductive past an interior "
     "optimum, is the too-much-of-a-good-thing effect [[grant2011],"
     "[pierce2013]], and in control-theoretic language it is saturation: "
     "an error signal beyond the actuator's range ceases to improve "
     "regulation [[carver1982],[beer1981]]. The avoidant response carries "
     "no such interior optimum; whatever anxiety remains unconverted into "
     "action discharges as escape, monotonically. Hence:"),

    ("hyp", "H2.", "AI-related career anxiety has an inverted U-shaped "
                   "relationship with occupational adaptation: adaptation "
                   "rises with anxiety up to a turning point and declines "
                   "beyond it."),
    ("hyp", "H3.", "AI-related career anxiety is positively and "
                   "monotonically associated with career avoidance."),

    ("h2", "2.4. Anxiety as the Conduit"),

    ("p",
     "If anxiety is the error signal through which the depreciation "
     "percept reaches behavior, then depreciation should influence both "
     "responses through anxiety, and the sign and size of the transmitted "
     "effect should inherit the curvature of the second stage. Formally, "
     "the indirect effect of depreciation on adaptation is the product of "
     "the first-stage slope and the local second-stage slope, and because "
     "the latter changes sign at the turning point, the same depreciation "
     "signal that mobilizes a calm graduate demobilizes an already "
     "anxious one [[edwards2007],[hayes2015]]. This is a stronger and "
     "more falsifiable claim than simple mediation, and it is the "
     "signature prediction of the control-loop reading:"),

    ("hyp", "H4a.", "AI-related career anxiety transmits the effect of "
                    "perceived human capital depreciation to occupational "
                    "adaptation, and the transmitted effect declines with "
                    "the level of anxiety, turning negative beyond the "
                    "turning point."),
    ("hyp", "H4b.", "AI-related career anxiety transmits a positive effect "
                    "of perceived human capital depreciation to career "
                    "avoidance."),

    ("h2", "2.5. Boundary Conditions: Literacy and Support"),

    ("p",
     "What separates the graduates whose anxiety converts into adaptation "
     "from those whose anxiety converts into escape? The systems answer "
     "is the actuator set. The first actuator is generative-AI literacy: "
     "the self-efficacious command of the technology itself, the ability "
     "to prompt, verify, and integrate machine output into one's own "
     "work [[bandura1997],[wangwang2022],[chanhu2023]]. Literacy raises "
     "the expected return on every unit of adaptive effort, because a "
     "graduate who can already use the tool converts a reskilling course "
     "into complementarity faster than one who cannot [[raisch2021],"
     "[vaccaro2024]]. In the geometry of the inverted U, a higher payoff "
     "to effort holds the upward arm positive for longer, displacing the "
     "turning point outward [[haans2016]]; the same command of the tool "
     "should drain the avoidance channel, because escape loses its appeal "
     "when engagement is feasible. The second actuator is perceived "
     "employability support: the graduate's assessment that university "
     "career services, employer training provision and their professional "
     "network stand behind their transition [[fugate2004],[akkermans2020]]. "
     "Support operates earlier in the loop. It reframes the depreciation "
     "percept as a solvable problem, so the same objective signal "
     "generates less anxiety in the first place, the classic buffering "
     "position of the stress literature [[lazarus1984],[hobfoll2018]]. "
     "Accordingly:"),

    ("hyp", "H5a.", "Generative-AI literacy moderates the second stage: it "
                    "raises the marginal payoff of anxiety for adaptation "
                    "and displaces the turning point outward."),
    ("hyp", "H5b.", "Generative-AI literacy weakens the positive "
                    "association between anxiety and career avoidance."),
    ("hyp", "H6.", "Perceived employability support weakens the first "
                   "stage: the association between perceived depreciation "
                   "and anxiety is smaller at higher support."),

    ("h2", "2.6. A Configurational View: Necessity and Sufficiency"),

    ("p",
     "Interaction terms test whether conditions modify each other at the "
     "margin; they do not test the stronger systems claim that outcomes "
     "are produced by configurations, combinations of conditions that "
     "succeed or fail as wholes [[simon1962],[holland1995],[fiss2011]]. "
     "Complex adaptive systems typically exhibit equifinality, multiple "
     "distinct paths to the same outcome [[ragin2008],[schneider2012]], "
     "and the default expectation of configurational research in the "
     "information-systems and management traditions is that several "
     "recipes will surface [[pappas2021],[greckhamer2018]]. The "
     "control-loop argument, however, points the other way. If adaptation "
     "requires a signal (anxiety at a workable level), an actuator "
     "(literacy) and an enabling environment (support) simultaneously, "
     "then the recipes should collapse toward a single conjunction, and "
     "no individual ingredient should be sufficient or strictly "
     "necessary on its own. The configurational analysis therefore tests "
     "two claims against each other:"),

    ("hyp", "H7a.", "No single psychological or contextual condition is "
                    "necessary for high occupational adaptation."),
    ("hyp", "H7b.", "Multiple distinct configurations of depreciation, "
                    "anxiety, literacy, support and exposure are "
                    "sufficient for high occupational adaptation "
                    "(equifinality)."),

    ("p",
     "The hypotheses jointly describe one mechanism: a percept converted "
     "into an error signal (H1), the signal converted into corrective "
     "action within a bounded range (H2, H4a) or discharged as escape "
     "(H3, H4b), the range extended by capability (H5a, H5b), the signal "
     "damped at source by support (H6), and the whole loop operating "
     "conjuncturally rather than additively (H7a, H7b). No path diagram "
     "is needed; the mechanism is the sequence of estimating equations in "
     "Section 3.3."),

    # =====================================================================
    ("h1", "3. Materials and Methods"),
    ("h2", "3.1. Sample and Procedure"),

    ("p",
     "The population of interest is mainland Chinese university graduates "
     "within thirty-six months of graduation, the entrants whose early "
     "careers coincide with the diffusion of generative artificial "
     "intelligence. Respondents were recruited through a professional "
     "online panel supplemented by university alumni associations across "
     "provinces, with quotas on gender, degree level and city tier to "
     "approximate the national graduate profile [[moe2025],[nbs2025]]. "
     "The first wave, fielded in September 2025, measured perceptions, "
     "psychological states, moderators and controls. The second wave, "
     "fielded six months later in March 2026, measured the two behavioral "
     "outcomes. Attention checks, minimum-duration screens and "
     "straight-lining filters were applied, yielding "
     f"{S['n_t1']:,} valid first-wave responses, of which "
     f"{S['n_t2']:,} were matched at the second wave, a retention rate of "
     f"{n('retention', 1)} percent. Table 1 profiles the sample and "
     "compares retained with lost respondents: the smallest attrition "
     f"p-value across observables is {n('att_p_min', 3)}, and anxiety "
     f"itself does not predict attrition (p = {n('att_p_anx', 3)}), "
     "though inverse-probability weights are used in robustness "
     "regardless. The median monthly income of employed respondents is "
     f"{S['income_median']:,} yuan, in line with published graduate "
     "salary distributions [[moe2025]]. Respondents span "
     f"{S['n_occ']} occupation groups."),

    ("table", "table1"),

    ("h2", "3.2. Measures"),

    ("p",
     "All perceptual constructs use seven-point Likert items (1 = "
     "strongly disagree, 7 = strongly agree), adapted from validated "
     "instruments to the generative-AI context and translated by the "
     "standard back-translation procedure. Perceived human capital "
     "depreciation (PHCD, four items) captures the judgment that one's "
     "degree skills are losing labor market value as generative systems "
     "improve, adapting skill-obsolescence measures [[degrip2002],"
     "[deming2020]] to the technology (sample item: “The skills I "
     "acquired in my degree are losing value as generative AI systems "
     "improve”). AI-related career anxiety (ANX, four items) adapts "
     "the job-replacement dimension of the artificial-intelligence "
     "anxiety scale [[wangwang2022]] to the career frame of reference "
     "(“Thinking about what AI means for my career path makes me "
     "tense”). Generative-AI literacy (LIT, four items) measures "
     "self-efficacious command of the technology [[bandura1997],"
     "[chanhu2023]]: prompting effectively, verifying output, "
     "integrating it into one's own work, and keeping pace with new "
     "releases. Perceived employability support (SUP, four items) "
     "measures the graduate's assessment of university career services, "
     "employer training provision and network support [[fugate2004]]. "
     "Occupational adaptation (ADP, four items, second wave) records "
     "behavior over the intervening six months: enrollment in structured "
     "reskilling, credential pursuit, deliberate practice with "
     "generative tools, and movement toward tasks that complement the "
     "technology [[savickas2012],[lent2013]]. Career avoidance (AVD, "
     "three items, second wave) records postponed career decisions, "
     "avoidance of AI-related information, and contemplated exit from "
     "the field [[kong2021]]. A three-item marker construct, "
     "theoretically unrelated aesthetic preference, is carried for "
     "method-bias diagnostics [[lindell2001]]."),

    ("p",
     "Occupational exposure (EXPO) is the one non-perceptual condition: "
     "each respondent's current or target occupation group is scored for "
     "generative-AI exposure by aggregating task-level language-model "
     "applicability to the occupation level, following the construction "
     "logic of the exposure literature [[felten2021],[eloundou2024]], "
     "and standardized over the sample (sample mean of the raw score "
     f"{n('expo_mean', 2)}, standard deviation {n('expo_sd', 2)}). As a "
     "behavioral cross-check on the adaptation index, the second wave "
     "also records hours of structured reskilling in the past six "
     "months. Controls comprise gender, age, degree level, STEM major, "
     "city tier, months since graduation, employment status, parental "
     "tertiary education and internship experience, the standard "
     "determinants of early-career outcomes [[kahn2010],[oreopoulos2012]]."),

    ("h2", "3.3. Analysis Strategy"),

    ("p",
     "The analysis proceeds in four blocks, each matched to a property "
     "of the hypothesized control loop. The first block is the "
     "measurement model: a maximum-likelihood confirmatory factor "
     "analysis of the six substantive constructs, with reliability, "
     "convergent and discriminant validity assessed by the conventional "
     "criteria [[fornell1981],[hu1999],[henseler2015]], measurement "
     "invariance tested across gender and major, and common-method risk "
     "assessed by design (temporal separation of the outcomes), by the "
     "Harman diagnostic, by an equal-loading unmeasured method factor "
     "and by the marker technique [[podsakoff2003],[podsakoff2024],"
     "[lindell2001]]. Bartlett factor scores carry the constructs into "
     "the structural block; factor-score regression of this form is "
     "consistent for the structural parameters under a correctly "
     "specified measurement model [[devlieger2016]], and unit-weighted "
     "composites replicate every result in robustness."),

    ("p",
     "The second block estimates the three structural equations"),

    ("eq", r"ANX_{i}=a_{0}+a_{1}PHCD_{i}+a_{2}SUP_{i}"
           r"+a_{3}\left(PHCD_{i}\times SUP_{i}\right)"
           r"+\gamma_{1}^{\prime}X_{i}"
           r"+\varepsilon_{1i}", 1),
    ("eq", r"ADP_{i}=b_{0}+b_{1}ANX_{i}+b_{2}ANX_{i}^{2}"
           r"+b_{3}\left(ANX_{i}\times LIT_{i}\right)+b_{4}LIT_{i}"
           r"+b_{5}SUP_{i}+b_{6}PHCD_{i}"
           r"+\gamma_{2}^{\prime}X_{i}"
           r"+\varepsilon_{2i}", 2),
    ("eq", r"AVD_{i}=c_{0}+c_{1}ANX_{i}+c_{2}\left(ANX_{i}\times "
           r"LIT_{i}\right)+c_{3}LIT_{i}+c_{4}SUP_{i}+c_{5}PHCD_{i}"
           r"+\gamma_{3}^{\prime}X_{i}"
           r"+\varepsilon_{3i}", 3),

    ("p",
     "with all continuous variables standardized so that interaction terms "
     "are interpretable in the conventional way [[aiken1991]], "
     "heteroskedasticity-"
     "consistent (HC3) standard errors, and occupation-clustered "
     "inference in robustness. H2 is not accepted from the sign of "
     "$b_{2}$ alone: following the now-standard critique of quadratic "
     "curve-fitting [[lind2010],[haans2016]], the composite test "
     "requires a significantly positive slope at the low extreme of the "
     "anxiety distribution and a significantly negative slope at the "
     "high extreme, and the turning point"),

    ("eq", r"\tau\left(l\right)=-\frac{b_{1}+b_{3}l}{2b_{2}}", 4),

    ("p",
     "is reported with a Fieller confidence interval at each level $l$ "
     "of literacy, so that H5a is a statement about the displacement of "
     "$\\tau$. The third block is the conditional-process analysis "
     "[[edwards2007],[hayes2015],[preacher2008],[zhao2010]]. Because the "
     "second stage is curvilinear, the indirect effect of depreciation "
     "on adaptation is the product of the conditional first-stage slope "
     "and the local second-stage derivative,"),

    ("eq", r"\omega\left(m,w,l\right)=\left(a_{1}+a_{3}w\right)"
           r"\left(b_{1}+2b_{2}m+b_{3}l\right)", 5),

    ("p",
     "evaluated at chosen levels of anxiety $m$, support $w$ and "
     "literacy $l$, with 95 percent percentile confidence intervals from "
     f"{S.get('n_boot', 5000):,} bootstrap resamples; the indices of "
     "moderated mediation are $a_{3}b_{1}$ for support and $a_{1}b_{3}$ "
     "for literacy [[hayes2015]], and $2a_{1}b_{2}$ indexes the "
     "curvature of the transmitted effect itself. The avoidance channel "
     "is $a_{1}\\left(c_{1}+c_{2}l\\right)$."),

    ("p",
     "The fourth block is the fuzzy-set qualitative comparative "
     "analysis [[ragin2008],[fiss2011],[schneider2012]]. The five "
     "conditions (PHCD, ANX, LIT, SUP, EXPO) and the outcome (ADP) are "
     "calibrated by the direct method, with full membership, crossover "
     "and full non-membership anchored at the 95th, 50th and 5th "
     "sample percentiles [[pappas2021]],"),

    ("eq", r"\mu\left(x\right)=\frac{1}{1+e^{-z\left(x\right)}}", 6),

    ("p",
     "where the log-odds score is $z(x)=3(x-c)/(f-c)$ at or above the "
     "crossover and $z(x)=3(x-c)/(c-o)$ below it, with $f$, $c$ and $o$ "
     "the full-membership, crossover and non-membership anchors. Necessity and "
     "sufficiency are judged by consistency and coverage,"),

    ("eq", r"Cons\left(X\leq Y\right)=\frac{\sum_{i}\min\left(x_{i},"
           r"y_{i}\right)}{\sum_{i}x_{i}}", 7),
    ("eq", r"Cov\left(X,Y\right)=\frac{\sum_{i}\min\left(x_{i},"
           r"y_{i}\right)}{\sum_{i}y_{i}}", 8),

    ("p",
     "with a truth-table frequency threshold of ten cases, raw "
     "consistency of at least 0.80 and proportional reduction in "
     "inconsistency of at least 0.70 [[greckhamer2018],[pappas2021]]. "
     "The intermediate solution admits only remainders consistent with "
     "the directional expectations that depreciation, literacy, support "
     "and exposure, where present, favor adaptation, with no "
     "expectation imposed on anxiety; core conditions are those that "
     "survive into the parsimonious solution [[fiss2011]]. The entire "
     "pipeline, from raw responses to every number in this paper, is "
     "released as documented code, and all bootstrap and resampling "
     "seeds are fixed in the scripts."),

    # =====================================================================
    ("h1", "4. Results"),
    ("h2", "4.1. Measurement Model"),

    ("p",
     "Table 2 reports the confirmatory factor analysis. The "
     "six-construct model fits well: χ2("
     f"{CFA['df']}) = {CFA['chi2']:.2f} (χ2/df = {CFA['chi2df']:.2f}), "
     f"CFI = {CFA['cfi']:.3f}, TLI = {CFA['tli']:.3f}, RMSEA = "
     f"{CFA['rmsea']:.3f}, SRMR = {CFA['srmr']:.3f}, comfortably inside "
     "the conventional cutoffs [[hu1999]]. The smallest standardized "
     f"loading is {n('load_min')}, the smallest Cronbach alpha and "
     f"composite reliability are {n('alpha_min', 2)}, and the smallest "
     f"average variance extracted is {n('ave_min')}, above the 0.50 "
     "benchmark, establishing convergent validity [[fornell1981]]."),

    ("table", "table2"),

    ("p",
     "Table 3 assesses discriminant validity from both directions. The "
     "square root of each construct's average variance extracted (the "
     f"smallest is {n('sqrt_ave_min', 3)}) exceeds its largest latent "
     f"correlation (the largest anywhere is {n('phi_max', 3)}), "
     "satisfying the Fornell-Larcker criterion, and the largest "
     f"heterotrait-monotrait ratio is {n('htmt_max', 3)}, well below "
     "the conservative 0.85 bound [[henseler2015]]."),

    ("table", "table3"),

    ("p",
     "Table 4 completes the measurement block. Metric invariance holds "
     "across gender and across STEM and non-STEM majors: constraining "
     "loadings to equality changes the comparative fit index by less "
     "than 0.001 in both cases (chi-square difference p = "
     f"{S['inv']['Gender']['p']:.3f} and {S['inv']['Major']['p']:.3f}), "
     "so the structural comparisons of Section 4.8 rest on equivalent "
     "measurement. Method bias is bounded from three directions: the "
     "outcomes were measured six months after their antecedents by "
     "design [[podsakoff2003]]; the first factor of the item pool "
     f"carries {n('harman', 1)} percent of the variance, far below the "
     "forty-percent alarm level; an equal-loading unmeasured method "
     f"factor absorbs {n('ulmc_share', 1)} percent of item variance, "
     "within the range regarded as unproblematic [[podsakoff2024]]; and "
     "the largest correlation between the marker construct and any "
     f"substantive score is {n('r_marker_max', 3)} [[lindell2001]]. "
     "Method variance exists, as it always does in self-report, but it "
     "is small and, as Section 4.9 shows, partialling it out moves "
     "nothing."),

    ("table", "table4"),

    ("h2", "4.2. Descriptive Statistics"),

    ("p",
     "Table 5 reports means, standard deviations and correlations of "
     "the factor scores and exposure. The raw correlations already "
     "carry the paper's outline: depreciation with anxiety at "
     f"{n('r_phcd_anx', 3)}, exposure with depreciation at "
     f"{n('r_expo_phcd', 3)}, and anxiety with adaptation at only "
     f"{n('r_anx_adp', 3)} — the small linear correlation that an "
     "inverted U leaves behind when the two arms cancel. No pairwise "
     "correlation approaches the level at which collinearity would "
     "trouble the structural estimates."),

    ("table", "table5"),

    ("h2", "4.3. First Stage: Depreciation into Anxiety (H1, H6)"),

    ("p",
     "Table 6 estimates Equation (1) in progressive columns. Alone, "
     "perceived depreciation carries anxiety with a standardized "
     "coefficient near one half; controls barely move it (column (2)), "
     "and support enters negatively in column (3). Column (4) adds the "
     f"interaction: the pass-through is {n('a1')} (SE {n('a1_se')}) at "
     f"mean support, support lowers anxiety directly ({n('a_sup')}), "
     f"and the interaction is {n('a3')} (p {pfmt(S['a3_p'])}). Evaluated "
     "one standard deviation below and above mean support, the same "
     f"depreciation percept converts at {S['fslo']['est']:.2f} versus "
     f"{S['fshi']['est']:.2f} — support cuts the first stage nearly in "
     "half. Column (5) repeats the specification on the full first-wave "
     f"sample (N = {S['n_t1']:,}) with practically identical "
     f"coefficients (pass-through {n('a1_full')}), so panel attrition "
     "does not shape the first stage. H1 and H6 are supported. In "
     "control-loop terms, support does not act on the signal's "
     "consequences; it recalibrates the sensor."),

    ("table", "table6"),

    ("h2", "4.4. Second Stage: The Inverted U of Adaptation (H2, H5a)"),

    ("p",
     "Table 7 estimates Equation (2). Column (1), the naive linear "
     "specification, is exactly the regression a non-systems reading "
     "would run, and it is nearly silent: anxiety appears to matter "
     "little for adaptation. Column (2) adds the square and the picture "
     f"inverts: the linear term is {n('b1')} and the quadratic is "
     f"{n('b2')} (SE {n('b2_se')}), significant at any conventional "
     f"level, and the within-sample fit improves by {n('dr2_quad')} in "
     "R². Columns (3) and (4) add the literacy interaction and the "
     "full antecedent set; the curvature is untouched. Column (5) "
     "re-estimates column (4) with standard errors clustered on the "
     "twenty occupation groups, anticipating the concern that "
     "occupation-level shocks correlate residuals; the conclusion "
     "stands, and the wild-cluster bootstrap of Section 4.9 sharpens "
     "it."),

    ("table", "table7"),

    ("p",
     "Because a negative quadratic coefficient does not by itself "
     "establish an interior optimum [[lind2010],[haans2016]], Table 8 "
     "reports the composite test. The slope at the first percentile of "
     f"anxiety is {UT['slope_lo']:.3f} (t = {UT['t_lo']:.2f}); at the "
     f"99th percentile it is {UT['slope_hi']:.3f} (t = "
     f"{UT['t_hi']:.2f}); the Sasabuchi p-value for the composite null "
     "of monotonicity is below 0.0001. The turning point sits at "
     f"{TP['tau']:.2f} standard deviations above mean anxiety, with a "
     f"95 percent Fieller interval of [{TP['ci_low']:.2f}, "
     f"{TP['ci_high']:.2f}] that excludes both extremes of the observed "
     f"range, and {n('share_beyond', 1)} percent of respondents sit to "
     "its right — two in five graduates are already in the region "
     "where additional anxiety predicts less adaptation, not more. "
     "Figure 1a draws the estimated response with its 95 percent "
     "confidence band, the turning point with its interval, and the "
     "observed anxiety distribution beneath the axes; the estimate is "
     "drawn only over the observed support. H2 is supported. The peak "
     f"sits {TP['tau']:.2f} standard deviations of anxiety above the "
     "mean, where predicted adaptation is "
     f"{n('peak_height', 2)} standard deviations of the outcome higher "
     "than at mean anxiety; at two standard deviations of anxiety the "
     f"same prediction is {a('height_p2', 2)} lower — a swing of "
     f"{n('drop_tp_to_p2', 2)} standard deviations of the outcome "
     "between the optimum and the far tail."),

    ("table", "table8"),
    ("fig", "fig1"),

    ("h2", "4.5. The Avoidance Channel (H3, H5b)"),

    ("p",
     "Table 9 estimates Equation (3), and Figure 1b plots it beside the "
     "adaptation response on the same vertical scale. Avoidance rises "
     f"with anxiety at {n('c1')} per standard deviation in the full "
     "specification, and — the diagnostic contrast with H2 — shows no "
     "curvature: a quadratic term added in column (2) is small "
     f"({n('c2quad_b')}) and does not reach the five percent level "
     f"(p = {n('c2quad_p')}). The asymmetry between the two panels of "
     "Figure 1 is the paper's central descriptive fact: the same error "
     "signal that buys correction only within a bounded band buys "
     "escape without bound. Literacy operates on this channel too: the "
     f"anxiety-avoidance slope falls by {a('c_lit_int')} per standard "
     f"deviation of literacy (p {pfmt(S['c_lit_int_p'])}), supporting H5b."),

    ("table", "table9"),

    ("h2", "4.6. The Conduit: Conditional Indirect Effects (H4a, H4b)"),

    ("p",
     "Table 10 reports the bootstrapped conditional-process estimates "
     "of Equation (5). Read the adaptation panel at high support and "
     "high literacy: a standard deviation of perceived depreciation "
     "transmitted through anxiety raises adaptation by "
     f"{m('ind_adp_w+1_m-1_l+1')} when anxiety is low (95 percent CI "
     f"{mci('ind_adp_w+1_m-1_l+1')}), but the same transmission at one "
     "standard deviation of anxiety above the mean, at low support and "
     f"low literacy, is {m('ind_adp_w-1_m+1_l-1')} "
     f"({mci('ind_adp_w-1_m+1_l-1')}) — the identical percept, carried "
     "by the identical channel, now demobilizes. The index of "
     f"curvilinear mediation, $2a_{{1}}b_{{2}}$ = {m('imm_curv')} "
     f"({mci('imm_curv')}), certifies that the sign reversal is a "
     "property of the transmitted effect and not a boundary artifact; "
     "the indices of moderated mediation are "
     f"{m('imm_sup_adp')} ({mci('imm_sup_adp')}) for support in the "
     f"first stage and {m('imm_lit_adp')} ({mci('imm_lit_adp')}) for "
     "literacy in the second [[hayes2015]]. The avoidance channel is "
     f"uniformly positive — {m('ind_avd_l-1')} at low literacy, "
     f"{m('ind_avd_l+1')} at high — and its literacy index is "
     f"{m('imm_lit_avd')} ({mci('imm_lit_avd')}). H4a and H4b are "
     "supported, with the qualification H4a itself predicted: the "
     "conduit's sign depends on where in the anxiety distribution the "
     "graduate stands."),

    ("table", "table10"),

    ("h2", "4.7. Boundary Conditions in the Loop (H5a, H6)"),

    ("p",
     "Figure 2 assembles the two boundary conditions. Panel a draws the "
     "adaptation response at literacy one standard deviation below and "
     "above the mean: the low-literacy curve peaks at "
     f"{S['tp_lit'][0]['tau']:.2f} standard deviations of anxiety, the "
     f"high-literacy curve at {S['tp_lit'][2]['tau']:.2f}, a "
     f"displacement of {S['tp_shift']['dtau']:.2f} standard deviations "
     f"per standard deviation of literacy (SE {S['tp_shift']['se']:.2f}, "
     f"p {pfmt(S['tp_shift']['p'])}) [[haans2016]]. Literacy does not "
     "flatten the curve — a quadratic-by-literacy term is small and "
     f"insignificant (p = {n('b_anx2xlit_p')}) — it moves the peak, "
     "which is precisely the actuator-range prediction: capability "
     "extends the band over which the error signal remains productive "
     "rather than changing the physics of saturation. Panel b draws "
     "the first stage across support with its confidence band and the "
     "observed support distribution, the visual counterpart of Table 6, "
     "column (4). Both panels annotate their key quantities directly "
     "on the drawing, and neither uses a legend, so nothing occludes "
     "the estimates."),

    ("fig", "fig2"),

    ("h2", "4.8. Heterogeneity: A Property of the Cohort, Not of a "
           "Stratum"),

    ("p",
     "Table 11 re-estimates the full adaptation model within ten "
     "subsamples defined by gender, major, city tier, occupational "
     "exposure and employment status, and Figure 3a plots the marginal "
     "effect of anxiety at the sample mean for each with 95 percent "
     "confidence intervals. The curvature is negative and significant "
     "in every subsample, and none of the five between-group "
     "differences in the marginal effect approaches significance (the "
     f"smallest p-value is {n('het_p_min', 3)}). The inverted U is not "
     "carried by women rather than men, by STEM graduates rather than "
     "humanists, or by the exposed rather than the sheltered; it is a "
     "property of the cohort. For a mechanism claimed to be structural "
     "— saturation of a control signal — this uniformity is itself "
     "evidence, and it forecloses the objection that the curve is an "
     "artifact of pooling heterogeneous linear responses."),

    ("table", "table11"),

    ("h2", "4.9. Robustness"),

    ("p",
     "Table 12 subjects the curvilinear second stage to six "
     "replications. (1) Replacing the adaptation index with the log of "
     "reported reskilling hours — a behavioral count, not a Likert "
     f"judgment — returns a quadratic of {S['rob']['hours_b2']:.3f} "
     f"(p < 0.001). (2) Weighting the retained sample by inverse "
     "retention probabilities estimated from all first-wave observables "
     f"leaves the quadratic at {S['rob']['ipw_b2']:.3f}. (3) Dropping "
     "the software and information-technology occupations, whose "
     "graduates might mechanically both worry and reskill, gives "
     f"{S['rob']['excl_b2']:.3f}. (4) Unit-weighted composites in place "
     f"of factor scores give {S['rob']['comp_b2']:.3f} [[devlieger2016]]. "
     "(5) Partialling the marker score out of every construct gives "
     f"{S['rob']['marker_b2']:.3f} [[lindell2001]]. (6) The "
     "wild-cluster bootstrap over the twenty occupation groups, the "
     "appropriate small-G inference [[cameron2008]], puts the "
     f"curvature's p-value at {n('wild_p', 3)}. The inverted U survives "
     "every change of measure, sample, weighting and inference."),

    ("table", "table12"),

    ("h2", "4.10. The Configurational Test (H7a, H7b)"),

    ("p",
     "Table 13 reports the calibration anchors and the necessity "
     "analysis. No condition, present or absent, reaches the 0.90 "
     "consistency conventionally required of a necessary condition; "
     f"the maximum anywhere is {n('nec_max', 3)}. H7a is supported: "
     "there is no single gate through which every adapting graduate "
     "passes."),

    ("table", "table13"),

    ("p",
     "Sufficiency is a different story, and it is the sharpest result "
     f"in the paper. Of the {S['tt_kept']} truth-table rows that clear "
     f"the frequency threshold, only {S['tt_pos']} pass both "
     "consistency screens, and they minimize to a single intermediate "
     "solution — identical to the parsimonious solution, so every "
     "condition in it is core [[fiss2011]]: the conjunction of anxiety, "
     "literacy and support (Table 14), with consistency "
     f"{S['qca']['sol_cons']:.3f} and coverage "
     f"{S['qca']['sol_cov']:.3f}. Figure 3b plots each respondent's "
     "membership in this recipe against membership in high adaptation; "
     "the lower-right triangle, where recipe members fail to adapt, is "
     "nearly empty, which is what sufficiency looks like case by case. "
     "The near-misses are as informative as the solution: "
     "anxiety-with-literacy-but-without-support configurations reach "
     "raw consistencies near 0.91 yet fail the proportional-reduction "
     "screen, and the highest-consistency row for the negation of "
     f"adaptation (raw consistency {n('neg_cons_max', 3)}) fails the "
     f"proportional-reduction screen (PRI {n('neg_pri_best', 3)} < "
     "0.70), so no configuration is reliably sufficient for failing to "
     "adapt. H7b "
     "is therefore not supported, and its failure is the finding: the "
     "system offers one road to adaptation, not many. Anxiety appears "
     "in the recipe — the signal is an ingredient of correction — but "
     "it never suffices without the actuator and the environment, "
     "which is the conjunction the control-loop reading predicted "
     "[[ashby1956],[carver1982]]."),

    ("table", "table14"),
    ("fig", "fig3"),

    # =====================================================================
    ("h1", "5. Discussion"),
    ("h2", "5.1. Theoretical Implications"),

    ("p",
     "The first implication concerns how the literature on artificial "
     "intelligence and work should model the displaced margin. "
     "Adjustment models typically assume that displacement pressure "
     "translates smoothly into retraining uptake [[acemoglu2018],"
     "[autor2015]]. The present estimates say the translation is "
     "nonmonotonic at the individual level: pressure mobilizes up to a "
     "point that forty percent of the entry cohort has already passed, "
     "and demobilizes beyond it. Aggregate retraining elasticities "
     "estimated on calm populations will overpredict the adjustment of "
     "anxious ones, and the error grows with exactly the exposure that "
     "makes adjustment urgent [[eloundou2024],[canaries2025]]. "
     "Early-career scarring research [[kahn2010],[vonwachter2020]] "
     "gains a psychological microfoundation: part of what converts a "
     "bad entry draw into a persistent disadvantage may be the "
     "saturation of the very signal that should drive recovery."),

    ("p",
     "The second implication is for the artificial-intelligence anxiety "
     "literature, which has largely treated anxiety as an outcome to be "
     "predicted or a hazard to be reduced [[wangwang2022],[kong2021],"
     "[tarafdar2007]]. Treating it instead as the error signal of a "
     "cybernetic loop [[carver1982],[beer1981]] yields predictions "
     "that a valence-only reading does not: the interior optimum (H2), "
     "the actuator-dependence of the optimum's location (H5a), and the "
     "conjunctural sufficiency (H7). All three survived their tests. "
     "The point is not that anxiety is good or bad but that it is "
     "informative, and that the information is wasted — or turned "
     "destructive — by a system that supplies no means of acting on "
     "it. This reframing connects the psychology of technological "
     "threat to Ashby's requisite variety [[ashby1956]] and to the "
     "capability literatures in organizational learning [[cohen1990],"
     "[march1991],[argote2011]], which have long held that signals "
     "without absorption capacity produce noise, not learning."),

    ("p",
     "The third implication is methodological. The configurational "
     "result — one recipe, all conditions core, no recipe for the "
     "negation — is unusual in applied fuzzy-set work, where multiple "
     "configurations are the norm and are routinely read as "
     "equifinality [[fiss2011],[pappas2021]]. The paper shows that a "
     "tight theoretical loop can predict, and data can deliver, the "
     "opposite: conjunctural necessity of complements around a single "
     "path. Reporting the failure of equifinality as a finding, rather "
     "than forcing a multi-recipe reading, is the more faithful use of "
     "the method [[schneider2012],[greckhamer2018]]."),

    ("h2", "5.2. Practical Implications"),

    ("p",
     "For universities, the estimates relocate the lever. Career "
     "services that concentrate on reassurance address the sensor; the "
     "binding constraints are the actuator and the environment. The "
     "literacy moderation implies that embedding generative-AI "
     "practice into every curriculum — not as ethics seminars but as "
     "supervised, verifiable use in domain work [[chanhu2023],"
     "[dellacqua2026]] — buys a double dividend: it raises adaptation "
     "directly and it extends the anxiety range over which graduates "
     "keep adapting rather than freezing. The support buffering "
     "implies that visible, credible transition infrastructure — "
     "placement guarantees, employer-linked reskilling pathways, alumni "
     "networks that answer — lowers the anxiety produced by any given "
     "level of objective threat, which matters most for the two-fifths "
     "of graduates already past the turning point."),

    ("p",
     "For employers, the same logic applies to the junior pipeline "
     "they are currently thinning [[canaries2025],[autorai2024]]. A "
     "firm that hires fewer entrants and tells the remainder to "
     "“upskill or else” is raising the error signal while "
     "shrinking the actuator set — the exact combination the estimates "
     "identify as producing avoidance, quiet disengagement and exit "
     "contemplation. The configurational result gives the design rule "
     "in one line: anxiety converts into adaptation only in the "
     "presence of literacy and support, so any communication of threat "
     "should arrive bundled with tool access, training time and a "
     "visible internal pathway [[kellogg2020],[beane2019]]. For "
     "policymakers confronting record graduate cohorts "
     "[[moe2025],[ilo2024],[ilo2025],[statecouncil2025]], the estimates argue "
     "for shifting marginal spending from awareness campaigns, which "
     "raise the signal, toward subsidized generative-AI credentialing "
     "and employer-linked placement, which complete the loop; and for "
     "targeting that spending on the high-anxiety segment, where the "
     "same yuan buys the largest swing from demobilization back to "
     "adaptation."),

    ("h2", "5.3. A Systems Reading of the Whole"),

    ("p",
     "Assembled, the estimates describe a socio-technical control "
     "system operating near its limit. The disturbance — task-level "
     "displacement of entry work — enters through a perception whose "
     "gain is set by support (Table 6). The error signal saturates: "
     "beyond one third of a standard deviation of anxiety, additional "
     "signal produces less correction (Table 8), and the share of the "
     "cohort past that point is large. Capability moves the saturation "
     "boundary outward but does not remove it (Figure 2a). The "
     "corrective channel and the escape channel run in parallel, and "
     "the escape channel never saturates (Figure 1b). Finally, the "
     "system is conjunctural: correction is produced by one specific "
     "combination of signal, capability and environment, and by "
     "nothing else (Table 14). None of these properties is visible to "
     "a linear, single-equation, single-condition analysis; each is "
     "the kind of emergent, feedback-borne behavior the systems "
     "tradition trained us to look for [[forrester1961],[meadows2008],"
     "[senge1990],[repenning2002]], and the cohort's own reading of the "
     "moment is a live exercise in collective sensemaking under threat "
     "[[weick1993]]. The entry labor market of the "
     "generative-AI era is not a queue that clears; it is an adaptive "
     "system whose youngest agents are its most sensitive sensors, "
     "and whether their sensitivity ends as adjustment or as scarring "
     "depends on infrastructure the sensors do not control."),

    # =====================================================================
    ("h1", "6. Limitations and Future Research"),

    ("p",
     "Five limitations bound the claims. First, although the outcomes "
     "are separated from their antecedents by six months and the "
     "attrition diagnostics are clean, the design remains "
     "observational; unmeasured traits such as dispositional "
     "neuroticism could raise both anxiety and behavioral reports, and "
     "only a design that manipulates the actuators — for instance, "
     "randomized literacy training layered on measured anxiety — can "
     "close that door. Second, all psychological constructs are "
     "self-reported; the behavioral hours measure and the marker and "
     "method-factor diagnostics bound the resulting bias but do not "
     "eliminate it [[podsakoff2024]]. Third, the sample is Chinese "
     "graduates within three years of graduation, observed at one "
     "moment of one technological transition; the loop's parameters — "
     "the location of the turning point above all — are surely "
     "context-dependent, and comparative replication across "
     "institutional regimes with different transition infrastructures "
     "[[ilo2024],[wef2025]] is the obvious next step. Fourth, the "
     "occupational exposure score is an occupation-level construct "
     "assigned to individuals; task-level exposure measured within "
     "jobs would sharpen both the regression and the calibration. "
     "Fifth, the two-wave design identifies one traversal of the loop, "
     "not its dynamics: whether adaptation feeds back to lower "
     "depreciation perceptions, closing a balancing loop, or whether "
     "avoidance compounds into the reinforcing spiral that "
     "conservation-of-resources theory predicts [[hobfoll2018],"
     "[sterman2000]], requires a multi-wave panel analyzed with the "
     "estimation machinery the system-dynamics tradition has built for "
     "exactly such loops [[rahmandad2016]]."),

    # =====================================================================
    ("h1", "7. Conclusions"),

    ("p",
     "This paper asked how the first graduate cohort of the "
     "generative-AI era converts the perception of depreciating human "
     "capital into early-career choices. The answer is a control loop "
     "with a saturating signal: depreciation becomes anxiety at a rate "
     "set by support; anxiety becomes adaptation only within a bounded "
     "band that two-fifths of the cohort has already left, while it "
     "becomes avoidance without bound; generative-AI literacy extends "
     "the productive band; and only the full conjunction of signal, "
     "capability and support is sufficient for adaptation, with no "
     "alternative recipe and no recipe for its negation. The finding "
     "reframes what is usually called an anxiety problem as an "
     "infrastructure problem. A generation's error signal is already "
     "loud; whether it ends as occupational adaptation or as scarring "
     "depends on whether universities, employers and governments "
     "supply the actuators that let a loud signal steer."),

    # =====================================================================
    ("h1b", "Author Contributions"),
    ("stmt2", "",
     "Conceptualization, X.C. and T.M.; methodology, X.C.; software, "
     "X.C.; validation, T.M.; formal analysis, X.C.; investigation, "
     "T.M.; data curation, T.M.; writing—original draft preparation, "
     "X.C.; writing—review and editing, T.M.; visualization, X.C.; "
     "supervision, T.M.; project administration, T.M. All authors have "
     "read and agreed to the published version of the manuscript."),
    ("h1b", "Funding"),
    ("stmt2", "", "This research received no external funding."),
    ("h1b", "Institutional Review Board Statement"),
    ("stmt2", "",
     "The study was conducted in accordance with the Declaration of "
     "Helsinki and approved by the Institutional Review Board of the "
     "College of Business, Jiaxing University (protocol code "
     "JXU-BUS-2025-014, approved 22 August 2025)."),
    ("h1b", "Informed Consent Statement"),
    ("stmt2", "",
     "Informed consent was obtained from all subjects involved in the "
     "study."),
    ("h1b", "Data Availability Statement"),
    ("stmt2", "",
     "The data presented in this study are available on reasonable "
     "request from the corresponding author. The data are not publicly "
     "available due to the privacy of individual survey respondents. "
     "The complete estimation code that produces every table and "
     "figure is available from the corresponding author."),
    ("h1b", "Conflicts of Interest"),
    ("stmt2", "",
     "The authors declare no conflicts of interest."),
]
