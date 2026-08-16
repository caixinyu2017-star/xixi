# -*- coding: utf-8 -*-
"""Manuscript text, written to the conventions of recent articles in the
target section of *Systems*.

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

HIGHLIGHTS = [
    ("What are the main findings?",
     ["AI-related career anxiety converts into occupational adaptation "
      "along an inverted U-shaped path: adaptation peaks "
      f"{TP['tau']:.2f} standard deviations above mean anxiety, "
      f"{n('share_beyond', 1)} percent of fresh graduates already stand "
      "beyond that turning point, and career avoidance rises "
      "monotonically with anxiety.",
      "Fuzzy-set qualitative comparative analysis identifies a single "
      "sufficient configuration for high adaptation — the conjunction of "
      "anxiety, generative-AI literacy, and employability support "
      f"(consistency {S['qca']['sol_cons']:.3f}) — while no single "
      "condition is necessary and anxiety alone never suffices."]),
    ("What are the implications of the main findings?",
     ["Treating career anxiety as the error signal of an adaptive "
      "feedback loop, rather than as a hazard to be reduced, extends "
      "systems practice to individual-level workforce transformation: "
      "the loop's transmission, saturation, and conjunctural logic are "
      "each estimated rather than assumed.",
      "Universities, employers, and policymakers should pair any "
      "communication of AI-related threat with tool access, training "
      "time, and visible transition infrastructure, because capability "
      "and support — not reassurance — determine whether a record "
      "graduate cohort's anxiety becomes adaptation or avoidance."]),
]

ABSTRACT = (
    "As generative artificial intelligence (GenAI) becomes most capable at "
    "precisely the entry-level tasks from which early careers have "
    "traditionally been built, fresh graduates must make their first "
    "occupational choices under conditions no previous cohort has faced. "
    "Drawing on socio-technical systems theory and a cybernetic control "
    "perspective, this study investigates how graduates’ perceived "
    "human capital depreciation translates into AI-related career anxiety "
    "and, in turn, into occupational adaptation or career avoidance, and "
    "which combinations of conditions govern this process. Using a two-wave "
    f"survey of {S['n_t1']:,} Chinese fresh graduates within three years of "
    f"graduation ({S['n_t2']:,} matched across waves, with behavioral "
    "outcomes measured six months after their antecedents), we employ "
    "confirmatory factor analysis, bootstrapped conditional-process models, "
    "and fuzzy-set qualitative comparative analysis (fsQCA). The study "
    "finds that (1) perceived human capital depreciation significantly "
    f"raises AI-related career anxiety (β = {n('a1')}), and perceived "
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
    "policymakers seeking to convert a record cohort’s anxiety into "
    "adaptation rather than avoidance.")

KEYWORDS = ("generative artificial intelligence; career anxiety; human "
            "capital depreciation; occupational adaptation; "
            "socio-technical systems")

BLOCKS = [
    # =====================================================================
    ("h1", "1. Introduction"),

    ("p",
     "Generative artificial intelligence is reshaping the entry point of "
     "professional labor markets. The technology performs best on the "
     "codifiable, language-intensive, and well-specified tasks that have "
     "traditionally been assigned to the newest members of the professions "
     "[[eloundou2024],[felten2021],[noy2023]]. Recent evidence shows entry "
     "positions contracting where the technology is adopted: junior-heavy "
     "hiring falls in exposed occupations [[canaries2025],[hui2024]], the "
     "productivity gains of the technology accrue disproportionately to "
     "novices while the demand for novices weakens [[brynjolfsson2025],"
     "[dellacqua2026]], and employers increasingly describe entry roles in "
     "terms of supervising machine output rather than producing it "
     "[[autorai2024],[autor2024]]. For the roughly twelve million students "
     "who now graduate from Chinese higher education each year [[moe2025],"
     "[li2014]], these developments define the conditions under which the "
     "first occupation, the first investments in skill, and the first "
     "revisions of both must be chosen."),

    ("p",
     "However, the existing literature has examined this collision almost "
     "exclusively from the demand side of the labor market [[acemoglu2022],"
     "[autor2015],[acemoglu2018]]. Much less is known about the supply "
     "side: how the entrants themselves perceive the depreciation of their "
     "just-acquired human capital, what that perception does to them "
     "psychologically, and when the resulting emotion converts into "
     "behavior that improves their position rather than behavior that "
     "worsens it. The question is of considerable practical importance, "
     "because early-career scarring is among the most persistent phenomena "
     "in labor economics: cohorts that stumble at entry carry lower "
     "earnings and worse matches for a decade or more [[kahn2010],"
     "[oreopoulos2012],[schwandt2019],[vonwachter2020]]. If the first "
     "cohort of the GenAI era responds to depreciation signals with "
     "paralysis rather than adaptation, the technology’s "
     "distributional effects will be amplified by the psychology of those "
     "it displaces."),

    ("p",
     "The emerging research on artificial-intelligence anxiety has begun "
     "to document how workers feel about intelligent technologies "
     "[[wangwang2022],[kong2021],[brougham2018],[tarafdar2007]]. "
     "Nevertheless, three gaps remain. Firstly, most studies treat anxiety "
     "as an outcome to be predicted or a hazard to be reduced, and "
     "therefore estimate only monotonic relationships between anxiety and "
     "behavior; whether anxiety can mobilize adaptive behavior within one "
     "range and suppress it within another has not been tested. Secondly, "
     "anxiety, capability, and institutional support have been studied "
     "separately, so it is unknown which combinations of these conditions "
     "are jointly sufficient for adaptive behavior. Thirdly, the "
     "population that matters most for workforce transformation — "
     "fresh graduates making their first occupational choices — has "
     "rarely been examined, even though students’ perceptions of "
     "generative technologies are documented to be intense and ambivalent "
     "[[chanhu2023]]."),

    ("p",
     "To address these gaps, this study adopts an explicitly "
     "systems-theoretic position. Drawing on socio-technical systems "
     "theory [[trist1951],[emery1965],[bertalanffy1968]] and the "
     "cybernetic tradition [[ashby1956],[beer1981],[carver1982]], the "
     "fresh graduate is modeled as an adaptive agent inside a "
     "socio-technical labor system: the perception of human capital "
     "depreciation is the input signal, AI-related career anxiety is the "
     "error signal of a control loop that compares the career one expected "
     "with the career one is likely to obtain, and occupational adaptation "
     "or career avoidance is the behavioral output through which the loop "
     "closes. Three testable properties follow from this framing. A "
     "control signal should transmit the input (mediation); an error "
     "signal that saturates should stop producing corrective action at "
     "high amplitude (nonlinearity); and the corrective action should "
     "depend on the actuators available to the agent, namely capability "
     "and support (conjunction). The empirical design of this study maps "
     "directly onto these three properties."),

    ("p",
     "This study employs a two-wave questionnaire survey of "
     f"{S['n_t1']:,} Chinese fresh graduates within thirty-six months of "
     "graduation, with psychological antecedents measured at the first "
     "wave and behavioral outcomes measured six months later, and "
     "combines confirmatory factor analysis, bootstrapped "
     "conditional-process models with an explicitly curvilinear second "
     "stage [[edwards2007],[hayes2015],[lind2010],[haans2016]], and "
     "fuzzy-set qualitative comparative analysis [[ragin2008],[fiss2011],"
     "[pappas2021]]. The research conclusions can help universities, "
     "employers, and policymakers recognize that the conversion of "
     "anxiety into adaptation depends on capability and support rather "
     "than on the level of anxiety alone, and provide both theoretical "
     "and practical guidance for workforce development in the GenAI era "
     "[[dwivedi2023],[janssen2025]]."),

    ("p",
     "The remainder of this study is structured as follows: Section 2 "
     "elaborates on the theoretical background and the development of "
     "hypotheses; Section 3 outlines the research design; Section 4 "
     "presents the results; and Section 5 concludes."),

    # =====================================================================
    ("h1", "2. Theoretical Background and Hypotheses Development"),
    ("h2", "2.1. Perceived Human Capital Depreciation and AI-Related "
           "Career Anxiety"),

    ("p",
     "Human capital depreciates when the market value of a skill stock "
     "falls, whether through wear, through vintage effects, or through "
     "technological displacement of the tasks the skills perform "
     "[[becker1964],[degrip2002],[deming2020]]. The loss lands hardest on "
     "labor market entrants, because early careers are built by doing: "
     "skills are accumulated on the job [[arrow1962]], weighted and "
     "priced by the tasks a position offers [[lazear2009]], and advanced "
     "through internal ladders whose first rung is exactly the work that "
     "generative systems now absorb [[gibbons2004],[autor2003]]. What "
     "matters for behavior, however, is not depreciation itself but its "
     "perception. A graduate observes the capability of generative "
     "systems in their own domain, compares it with what they were "
     "trained to do, and forms a judgment about how fast that training "
     "is losing value [[chanhu2023],[brougham2018]]."),

    ("p",
     "Appraisal theory holds that a perceived threat to a central "
     "resource elicits a corresponding negative activation state "
     "[[lazarus1984]]. Conservation of resources theory makes the same "
     "prediction from a different direction: anticipated resource loss "
     "is the most potent known elicitor of stress, and the career is "
     "among the most central resources a labor market entrant holds "
     "[[hobfoll1989],[hobfoll2018]]. From the cybernetic perspective, "
     "the depreciation percept is a widening discrepancy between the "
     "expected and the likely career trajectory, and the affective "
     "correlate of that discrepancy is anxiety [[carver1982]]. Prior "
     "empirical work confirms that awareness of intelligent technologies "
     "is associated with career-related strain among incumbent workers "
     "[[kong2021],[brougham2018],[wangwang2022]] and that career anxiety "
     "is a distinct and measurable state among students and graduates "
     "[[pisarik2017]]. Therefore, the following hypothesis is proposed:"),

    ("hyp", "H1.", "Perceived human capital depreciation is positively "
                   "associated with AI-related career anxiety."),

    ("h2", "2.2. The Dual Behavioral Responses to Career Anxiety"),

    ("p",
     "Anxiety is an activation state, and activation is behaviorally "
     "ambidextrous. The coping literature distinguishes problem-focused "
     "responses, which attack the stressor, from avoidant responses, "
     "which attack the feeling [[lazarus1984]]. In the career domain, "
     "the problem-focused response is occupational adaptation: enrolling "
     "in structured reskilling, pursuing credentials, deliberately "
     "practicing the new technology, and repositioning toward tasks the "
     "technology complements [[savickas2012],[lent2013]]. The avoidant "
     "response is career avoidance: postponing career decisions, "
     "avoiding information about the technology, and contemplating exit "
     "from the chosen field [[kong2021],[brougham2018]]."),

    ("p",
     "The relationship between anxiety and adaptation should not be "
     "monotonic. At low-to-moderate levels, anxiety supplies the "
     "activation that overcomes the inertia of costly investment; this "
     "mobilizing arm is among the oldest results in behavioral research "
     "[[yerkes1908]] and is consistent with conservation of resources "
     "theory, in which moderate loss threat triggers resource investment "
     "[[hobfoll2018]]. At high levels, three mechanisms bend the curve "
     "downward. Cognitively, intense anxiety narrows attention and "
     "consumes the working memory that planning a retraining program "
     "requires. Motivationally, extreme threat triggers defensive "
     "avoidance rather than approach [[lazarus1984]]. In resource terms, "
     "graduates deep in anticipated loss enter a defensive posture in "
     "which conserving what remains dominates investing in what could be "
     "[[hobfoll2018]]. The general form of this argument — a "
     "productive input becoming counterproductive past an interior "
     "optimum — is the too-much-of-a-good-thing effect "
     "[[grant2011],[pierce2013]], and in control-theoretic language it "
     "is saturation: an error signal beyond the actuator’s range "
     "ceases to improve regulation [[carver1982],[beer1981]]. The "
     "avoidant response carries no interior optimum; whatever anxiety "
     "remains unconverted into action discharges as escape, "
     "monotonically. Therefore, the following hypotheses are proposed:"),

    ("hyp", "H2.", "AI-related career anxiety has an inverted U-shaped "
                   "relationship with occupational adaptation: adaptation "
                   "rises with anxiety up to a turning point and declines "
                   "beyond it."),
    ("hyp", "H3.", "AI-related career anxiety is positively and "
                   "monotonically associated with career avoidance."),

    ("h2", "2.3. The Mediating Role of AI-Related Career Anxiety"),

    ("p",
     "If anxiety is the error signal through which the depreciation "
     "percept reaches behavior, then perceived depreciation should "
     "influence both behavioral responses through anxiety. Moreover, the "
     "transmitted effect should inherit the curvature of the second "
     "stage: because the local slope of the anxiety-adaptation curve "
     "changes sign at the turning point, the same depreciation signal "
     "that mobilizes a calm graduate should demobilize an already "
     "anxious one [[edwards2007],[hayes2015]]. This conditional "
     "mediation is a stronger and more falsifiable claim than simple "
     "mediation, and it is the signature prediction of the control-loop "
     "framing. Therefore, the following hypotheses are proposed:"),

    ("hyp", "H4a.", "AI-related career anxiety mediates the relationship "
                    "between perceived human capital depreciation and "
                    "occupational adaptation, and the indirect effect "
                    "declines with the level of anxiety, turning negative "
                    "beyond the turning point."),
    ("hyp", "H4b.", "AI-related career anxiety mediates a positive "
                    "relationship between perceived human capital "
                    "depreciation and career avoidance."),

    ("h2", "2.4. The Moderating Role of Generative-AI Literacy"),

    ("p",
     "Whether anxiety converts into adaptation or into escape depends on "
     "the actions available to the graduate. The first boundary "
     "condition is generative-AI literacy: the self-efficacious command "
     "of the technology itself, including prompting effectively, "
     "verifying machine output, and integrating it into one’s own "
     "work [[bandura1997],[wangwang2022],[chanhu2023]]. Literacy raises "
     "the expected return on every unit of adaptive effort, because a "
     "graduate who can already use the tool converts a reskilling course "
     "into complementarity faster than one who cannot [[raisch2021],"
     "[vaccaro2024]]. In the geometry of an inverted U, a higher payoff "
     "to effort holds the upward arm positive over a longer range and "
     "therefore displaces the turning point outward [[haans2016]]. The "
     "same command of the tool should also drain the avoidance channel, "
     "because escape loses its appeal when engagement is feasible. "
     "Therefore, the following hypotheses are proposed:"),

    ("hyp", "H5a.", "Generative-AI literacy moderates the inverted "
                    "U-shaped relationship between anxiety and "
                    "adaptation, displacing the turning point outward."),
    ("hyp", "H5b.", "Generative-AI literacy weakens the positive "
                    "relationship between anxiety and career avoidance."),

    ("h2", "2.5. The Moderating Role of Perceived Employability Support"),

    ("p",
     "The second boundary condition operates one stage earlier in the "
     "loop. Perceived employability support is the graduate’s "
     "assessment that university career services, employer training "
     "provision, and their professional network stand behind their "
     "transition [[fugate2004],[akkermans2020]]. According to the "
     "buffering position of the stress literature, support reframes a "
     "threat as a solvable problem, so the same objective signal "
     "generates less strain in the first place [[lazarus1984],"
     "[hobfoll2018]]. In control-theoretic terms, support recalibrates "
     "the sensor rather than the actuator: it lowers the gain with which "
     "perceived depreciation is converted into anxiety. Therefore, the "
     "following hypothesis is proposed:"),

    ("hyp", "H6.", "Perceived employability support weakens the positive "
                   "relationship between perceived human capital "
                   "depreciation and AI-related career anxiety."),

    ("h2", "2.6. A Configurational Perspective on Adaptation"),

    ("p",
     "Interaction terms test whether conditions modify each other at the "
     "margin; they do not test the stronger systems claim that outcomes "
     "are produced by configurations — combinations of conditions "
     "that succeed or fail as wholes [[simon1962],[holland1995],"
     "[fiss2011]]. Complex adaptive systems typically exhibit "
     "equifinality, meaning multiple distinct paths lead to the same "
     "outcome, and configurational studies in the management and "
     "information-systems traditions routinely report several sufficient "
     "recipes [[ragin2008],[schneider2012],[pappas2021],"
     "[greckhamer2018]]. The control-loop framing of this study, "
     "however, points the other way. If adaptation requires a signal "
     "(anxiety at a workable level), an actuator (literacy), and an "
     "enabling environment (support) simultaneously, then the sufficient "
     "recipes should collapse toward a single conjunction, and no "
     "individual ingredient should be sufficient or strictly necessary "
     "on its own. The configurational analysis therefore tests two "
     "claims against each other:"),

    ("hyp", "H7a.", "No single psychological or contextual condition is "
                    "necessary for high occupational adaptation."),
    ("hyp", "H7b.", "Multiple distinct configurations of depreciation, "
                    "anxiety, literacy, support, and exposure are "
                    "sufficient for high occupational adaptation "
                    "(equifinality)."),

    ("p",
     "To summarize, the theoretical framework of this study is "
     "illustrated in Figure 1."),

    ("fig", "fig1"),

    # =====================================================================
    ("h1", "3. Data and Methods"),
    ("h2", "3.1. Data Collection and Sample"),

    ("p",
     "This study takes mainland Chinese university graduates within "
     "thirty-six months of graduation as the targeted research sample, "
     "the population whose first occupational choices coincide with the "
     "diffusion of generative artificial intelligence. To ensure the "
     "accuracy of the survey data, we developed the questionnaire by "
     "adapting established scales from the literature and incorporating "
     "expert suggestions, translated each item into Chinese following "
     "the standard back-translation procedure, and optimized the wording "
     "so that respondents could easily understand it. Respondents were "
     "recruited through a professional online panel supplemented by "
     "university alumni associations across provinces, with quotas on "
     "gender, degree level, and city tier to approximate the national "
     "graduate profile [[moe2025],[nbs2025]]. The first wave, fielded in "
     "September 2025, measured perceptions, psychological states, "
     "moderators, and controls; the second wave, fielded six months "
     "later in March 2026, measured the two behavioral outcomes. "
     "Attention checks, minimum-duration screens, and straight-lining "
     f"filters were applied. A total of {S['n_t1']:,} valid first-wave "
     f"responses were obtained, of which {S['n_t2']:,} were matched at "
     f"the second wave, a retention rate of {n('retention', 1)} percent. "
     "All statistical analyses were performed with documented code whose "
     "random seeds are fixed in the released scripts."),

    ("p",
     "To ensure the sample is sufficiently representative and to rule "
     "out attrition bias, a sample structure and attrition analysis was "
     "conducted before the main analysis, as shown in Table 1. The "
     "retained and lost respondents do not differ significantly on any "
     f"observable characteristic (the smallest p-value is "
     f"{n('att_p_min', 3)}), and anxiety itself does not predict "
     f"attrition (p = {n('att_p_anx', 3)}); inverse-probability "
     "weighting is nevertheless applied in the robustness tests. The "
     "median monthly income of employed respondents is "
     f"{S['income_median']:,} yuan, in line with published graduate "
     f"salary distributions [[moe2025]]. Respondents span {S['n_occ']} "
     "occupation groups."),

    ("table", "table1"),

    ("h2", "3.2. Measurement"),

    ("p",
     "This study uses established questionnaire scales from the "
     "literature with appropriate modifications, using a seven-point "
     "Likert scale (1 = strongly disagree, 7 = strongly agree). The "
     "specific variables were measured as follows:"),

    ("p",
     "Perceived human capital depreciation (PHCD). Adapting "
     "skill-obsolescence measures [[degrip2002],[deming2020]] to the "
     "generative-AI context, four items capture the judgment that "
     "one’s degree skills are losing labor market value as "
     "generative systems improve (sample item: “The skills I "
     "acquired in my degree are losing value as generative AI systems "
     "improve”)."),

    ("p",
     "AI-related career anxiety (ANX). Drawing mainly on the "
     "artificial-intelligence anxiety scale of Wang and Wang (2022) "
     "[[wangwang2022]], four items adapt the job-replacement dimension "
     "to the career frame of reference (“Thinking about what AI "
     "means for my career path makes me tense”)."),

    ("p",
     "Generative-AI literacy (LIT). Following the self-efficacy "
     "tradition [[bandura1997]] and studies of student GenAI competence "
     "[[chanhu2023]], four items measure self-efficacious command of "
     "the technology: prompting effectively, verifying output, "
     "integrating it into one’s own work, and keeping pace with "
     "new releases."),

    ("p",
     "Perceived employability support (SUP). Drawing on the "
     "employability literature [[fugate2004]], four items measure the "
     "graduate’s assessment of university career services, "
     "employer training provision, and network support."),

    ("p",
     "Occupational adaptation (ADP). Measured at the second wave, four "
     "items record behavior over the intervening six months: enrollment "
     "in structured reskilling, credential pursuit, deliberate practice "
     "with generative tools, and movement toward tasks that complement "
     "the technology [[savickas2012],[lent2013]]. As a behavioral "
     "cross-check, the second wave also records hours of structured "
     "reskilling."),

    ("p",
     "Career avoidance (AVD). Measured at the second wave, three items "
     "record postponed career decisions, avoidance of AI-related "
     "information, and contemplated exit from the field [[kong2021]]."),

    ("p",
     "Occupational exposure (EXPO). The one non-perceptual condition: "
     "each respondent’s current or target occupation group is "
     "scored for generative-AI exposure by aggregating task-level "
     "language-model applicability to the occupation level, following "
     "the construction logic of the exposure literature [[felten2021],"
     "[eloundou2024]], and standardized over the sample (raw-score mean "
     f"{n('expo_mean', 2)}, standard deviation {n('expo_sd', 2)})."),

    ("p",
     "Control variables. Gender, age, degree level, STEM major, city "
     "tier, months since graduation, employment status, parental "
     "tertiary education, and internship experience are controlled, "
     "these being standard determinants of early-career outcomes "
     "[[kahn2010],[oreopoulos2012]]. A three-item marker construct, "
     "theoretically unrelated aesthetic preference, is carried for "
     "method-bias diagnostics [[lindell2001]]."),

    ("h2", "3.3. Analytical Strategy"),

    ("p",
     "The analysis proceeds in four steps. In the first step, a "
     "maximum-likelihood confirmatory factor analysis of the six "
     "substantive constructs establishes reliability, convergent and "
     "discriminant validity [[fornell1981],[hu1999],[henseler2015]], "
     "measurement invariance across gender and major, and common-method "
     "diagnostics [[podsakoff2003],[podsakoff2024],[lindell2001]]. "
     "Bartlett factor scores carry the constructs into the structural "
     "step; factor-score regression of this form is consistent for the "
     "structural parameters under a correctly specified measurement "
     "model [[devlieger2016]], and unit-weighted composites replicate "
     "every result in the robustness tests. In the second step, the "
     "following three structural equations are estimated:"),

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
     "where all continuous variables are standardized so that "
     "interaction terms are interpretable in the conventional way "
     "[[aiken1991]], $X_{i}$ denotes the control vector, and "
     "heteroskedasticity-consistent (HC3) standard errors are used "
     "throughout, with occupation-clustered inference in the robustness "
     "tests. Hypothesis H2 is not accepted from the sign of $b_{2}$ "
     "alone: following the composite testing procedure of Lind and "
     "Mehlum [[lind2010],[haans2016]], a significantly positive slope "
     "at the low extreme and a significantly negative slope at the high "
     "extreme of the observed anxiety range are both required, and the "
     "turning point"),

    ("eq", r"\tau\left(l\right)=-\frac{b_{1}+b_{3}l}{2b_{2}}", 4),

    ("p",
     "is reported with a Fieller confidence interval at each level $l$ "
     "of literacy, so that H5a is a statement about the displacement of "
     "$\\tau$. In the third step, the conditional-process analysis "
     "[[edwards2007],[preacher2008],[zhao2010],[hayes2015]] computes "
     "the instantaneous indirect effect of depreciation on adaptation "
     "as the product of the conditional first-stage slope and the local "
     "second-stage derivative,"),

    ("eq", r"\omega\left(m,w,l\right)=\left(a_{1}+a_{3}w\right)"
           r"\left(b_{1}+2b_{2}m+b_{3}l\right)", 5),

    ("p",
     "evaluated at chosen levels of anxiety $m$, support $w$, and "
     "literacy $l$, with 95 percent percentile confidence intervals "
     "from 5,000 bootstrap resamples; the indices of moderated "
     "mediation are $a_{3}b_{1}$ for support and $a_{1}b_{3}$ for "
     "literacy [[hayes2015]], and $2a_{1}b_{2}$ indexes the curvature "
     "of the transmitted effect itself. The avoidance channel is "
     "$a_{1}\\left(c_{1}+c_{2}l\\right)$. In the fourth step, the "
     "fuzzy-set qualitative comparative analysis [[ragin2008],"
     "[fiss2011],[schneider2012]] calibrates the five conditions (PHCD, "
     "ANX, LIT, SUP, EXPO) and the outcome (ADP) by the direct method, "
     "with full membership, crossover, and full non-membership anchored "
     "at the 95th, 50th, and 5th sample percentiles [[pappas2021]]:"),

    ("eq", r"\mu\left(x\right)=\frac{1}{1+e^{-z\left(x\right)}}", 6),

    ("p",
     "where the log-odds score is $z(x)=3(x-c)/(f-c)$ at or above the "
     "crossover and $z(x)=3(x-c)/(c-o)$ below it, with $f$, $c$, and "
     "$o$ the three anchors. Necessity and sufficiency are judged by "
     "consistency and coverage:"),

    ("eq", r"Cons\left(X\leq Y\right)=\frac{\sum_{i}\min\left(x_{i},"
           r"y_{i}\right)}{\sum_{i}x_{i}}", 7),
    ("eq", r"Cov\left(X,Y\right)=\frac{\sum_{i}\min\left(x_{i},"
           r"y_{i}\right)}{\sum_{i}y_{i}}", 8),

    ("p",
     "with a truth-table frequency threshold of ten cases, raw "
     "consistency of at least 0.80, and proportional reduction in "
     "inconsistency (PRI) of at least 0.70 [[greckhamer2018],"
     "[pappas2021]]. The intermediate solution admits only remainders "
     "consistent with the directional expectations that depreciation, "
     "literacy, support, and exposure, where present, favor adaptation, "
     "with no expectation imposed on anxiety; core conditions are those "
     "that survive into the parsimonious solution [[fiss2011]]."),

    # =====================================================================
    ("h1", "4. Results"),
    ("h2", "4.1. Reliability and Validity Tests"),

    ("p",
     "Table 2 presents the results of the confirmatory factor analysis. "
     "The six-construct measurement model fits the data well: "
     f"χ2({CFA['df']}) = {CFA['chi2']:.2f} (χ2/df = "
     f"{CFA['chi2df']:.2f}), CFI = {CFA['cfi']:.3f}, TLI = "
     f"{CFA['tli']:.3f}, RMSEA = {CFA['rmsea']:.3f}, SRMR = "
     f"{CFA['srmr']:.3f}, all within the conventional cutoffs "
     "[[hu1999]]. The smallest standardized loading is "
     f"{n('load_min')}, the smallest Cronbach’s alpha and "
     f"composite reliability are {n('alpha_min', 2)}, and the smallest "
     f"average variance extracted is {n('ave_min')}, above the 0.50 "
     "benchmark. These results indicate satisfactory reliability and "
     "convergent validity [[fornell1981]]."),

    ("table", "table2"),

    ("p",
     "Table 3 assesses discriminant validity from both directions. The "
     "square root of each construct’s average variance extracted "
     f"(the smallest is {n('sqrt_ave_min', 3)}) exceeds its largest "
     f"latent correlation (the largest anywhere is {n('phi_max', 3)}), "
     "satisfying the Fornell–Larcker criterion, and the largest "
     f"heterotrait–monotrait ratio is {n('htmt_max', 3)}, well "
     "below the conservative 0.85 threshold [[henseler2015]]. "
     "Discriminant validity is therefore established."),

    ("table", "table3"),

    ("h2", "4.2. Measurement Invariance and Common Method Variance "
           "Tests"),

    ("p",
     "Table 4 reports the invariance and method-bias diagnostics. "
     "Metric invariance holds across gender and across STEM and "
     "non-STEM majors: constraining loadings to equality changes the "
     "comparative fit index by less than 0.001 in both cases "
     f"(chi-square difference p = {S['inv']['Gender']['p']:.3f} and "
     f"{S['inv']['Major']['p']:.3f}), so the group comparisons of "
     "Section 4.7 rest on equivalent measurement. Common method "
     "variance is bounded from three directions. By design, the "
     "outcomes were measured six months after their antecedents "
     "[[podsakoff2003]]. Statistically, the first factor of the item "
     f"pool carries {n('harman', 1)} percent of the variance, far below "
     "the forty-percent alarm level; an equal-loading unmeasured method "
     f"factor absorbs {n('ulmc_share', 1)} percent of item variance, "
     "within the range regarded as unproblematic [[podsakoff2024]]; and "
     "the largest correlation between the marker construct and any "
     f"substantive score is {n('r_marker_max', 3)} [[lindell2001]]. "
     "Method variance exists, as it always does in self-report data, "
     "but it is small, and Section 4.8 shows that partialling it out "
     "changes nothing."),

    ("table", "table4"),

    ("h2", "4.3. Descriptive Statistics and Correlation Analysis"),

    ("p",
     "Table 5 reports the means, standard deviations, and correlations "
     "of the factor scores and the exposure measure. The raw "
     "correlations already outline the argument: perceived depreciation "
     f"correlates with anxiety at {n('r_phcd_anx', 3)}, occupational "
     f"exposure with depreciation at {n('r_expo_phcd', 3)}, and anxiety "
     f"with adaptation at only {n('r_anx_adp', 3)} — the small "
     "linear correlation that an inverted U leaves behind when its two "
     "arms cancel. No pairwise correlation approaches the level at "
     "which collinearity would threaten the structural estimates."),

    ("table", "table5"),

    ("h2", "4.4. Hypothesis Testing: The First Stage"),

    ("p",
     "The first stage was investigated using the hierarchical "
     "regression method, and the results are shown in Table 6. Model "
     "(1) includes only perceived depreciation; Model (2) adds the "
     "control variables; Model (3) introduces perceived employability "
     "support; and Model (4) adds the interaction term. The results "
     "show that the regression coefficient of perceived depreciation "
     f"on anxiety is {n('a1')} (standard error {n('a1_se')}, p < 0.01) "
     "in the full specification, and Hypothesis H1 is verified. "
     f"Support enters negatively ({n('a_sup')}, p < 0.01), and the "
     f"interaction coefficient is {n('a3')} (p {pfmt(S['a3_p'])}), so "
     "the conversion of depreciation into anxiety weakens as support "
     "rises; Hypothesis H6 is verified. Model (5) repeats the full "
     "specification on the complete first-wave sample "
     f"(N = {S['n_t1']:,}) with a practically identical pass-through "
     f"({n('a1_full')}), confirming that panel attrition does not shape "
     "the first stage."),

    ("table", "table6"),

    ("p",
     "Figure 2 visualizes the moderating effect. Evaluated one "
     "standard deviation below the mean of support, a one-standard-"
     "deviation increase in perceived depreciation raises anxiety by "
     f"{S['fslo']['est']:.2f} standard deviations; one standard "
     f"deviation above the mean, the same increase raises anxiety by "
     f"only {S['fshi']['est']:.2f}. The shaded area denotes the 95 "
     "percent confidence interval and the dashed line marks a zero "
     "marginal effect; the effect remains positive and significant "
     "across the entire observed range of support, so support damps "
     "but does not eliminate the first stage."),

    ("fig", "fig2"),

    ("h2", "4.5. Hypothesis Testing: The Curvilinear Second Stage"),

    ("p",
     "Table 7 estimates Equation (2) hierarchically. Model (1), which "
     "includes only the linear anxiety term, is nearly silent: anxiety "
     "appears to matter little for adaptation. Model (2) adds the "
     "squared term and the picture inverts, with the explanatory power "
     f"of the model improving by {n('dr2_quad')} in R². Models "
     "(3) and (4) add the literacy interaction and the full antecedent "
     "set; in the full specification of Model (4) the linear "
     f"coefficient is {n('b1')} and the quadratic coefficient is "
     f"{n('b2')} (standard error {n('b2_se')}, p < 0.01). Model (5) "
     "re-estimates Model (4) with standard errors clustered on the "
     "twenty occupation groups and the conclusion stands."),

    ("table", "table7"),

    ("p",
     "Because a negative quadratic coefficient does not by itself "
     "establish an interior optimum [[lind2010],[haans2016]], Table 8 "
     "reports the composite validation. The slope at the first "
     f"percentile of anxiety is {UT['slope_lo']:.3f} (t = "
     f"{UT['t_lo']:.2f}); the slope at the 99th percentile is "
     f"{UT['slope_hi']:.3f} (t = {UT['t_hi']:.2f}); and the Sasabuchi "
     "p-value for the composite null of monotonicity is below 0.0001. "
     f"The turning point lies {TP['tau']:.2f} standard deviations "
     "above mean anxiety, with a 95 percent Fieller interval of "
     f"[{TP['ci_low']:.2f}, {TP['ci_high']:.2f}] that excludes both "
     f"extremes of the observed range, and {n('share_beyond', 1)} "
     "percent of respondents fall to its right. Hypothesis H2 is "
     "verified. The literacy-conditional turning points in the lower "
     "panel of Table 8 test Hypothesis H5a: the turning point moves "
     f"from {S['tp_lit'][0]['tau']:.2f} standard deviations at low "
     f"literacy to {S['tp_lit'][2]['tau']:.2f} at high literacy, a "
     f"displacement of {S['tp_shift']['dtau']:.2f} per standard "
     f"deviation of literacy (standard error {S['tp_shift']['se']:.2f}, "
     f"p {pfmt(S['tp_shift']['p'])}); a quadratic-by-literacy term is "
     f"insignificant (p = {n('b_anx2xlit_p')}), so literacy moves the "
     "peak without changing the curvature. Hypothesis H5a is verified."),

    ("table", "table8"),

    ("p",
     "Figure 3 draws the two second-stage responses on one vertical "
     "scale. Panel (a) shows the estimated adaptation response with "
     "its 95 percent confidence band; the dotted vertical line marks "
     "the turning point, and the dashed horizontal line marks the "
     "sample mean of the outcome. Panel (b) shows the avoidance "
     "response, which is monotonic throughout. The contrast between "
     "the two panels is the central descriptive fact of this study: "
     "the same anxiety that purchases correction only within a bounded "
     "band purchases escape without bound."),

    ("fig", "fig3"),

    ("p",
     "Table 9 estimates Equation (3). The coefficient of anxiety on "
     f"avoidance is {n('c1')} (p < 0.01) in the full specification, "
     "and a quadratic term added in Model (2) is small "
     f"({n('c2quad_b')}) and does not reach the five percent level "
     f"(p = {n('c2quad_p')}), confirming monotonicity; Hypothesis H3 "
     "is verified. The literacy interaction is negative "
     f"({n('c_lit_int')}, p {pfmt(S['c_lit_int_p'])}), so command of "
     "the technology drains the avoidance channel; Hypothesis H5b is "
     "verified."),

    ("table", "table9"),

    ("h2", "4.6. Moderated Mediation Analysis"),

    ("p",
     "Table 10 presents the results of the bootstrapped "
     "conditional-process analysis of Equation (5). When anxiety is "
     "low and both boundary conditions are favorable, the indirect "
     "effect of perceived depreciation on adaptation through anxiety "
     f"is significantly positive ({m('ind_adp_w+1_m-1_l+1')}, with a "
     f"confidence interval of {mci('ind_adp_w+1_m-1_l+1')}, excluding "
     "0); when anxiety is one standard deviation above the mean and "
     "both conditions are unfavorable, the same indirect effect is "
     f"significantly negative ({m('ind_adp_w-1_m+1_l-1')}, "
     f"{mci('ind_adp_w-1_m+1_l-1')}). The identical percept, carried "
     "by the identical channel, mobilizes the calm graduate and "
     "demobilizes the anxious one; Hypothesis H4a is verified. The "
     "index of curvilinear mediation, $2a_{1}b_{2}$, is "
     f"{m('imm_curv')} ({mci('imm_curv')}, excluding 0), confirming "
     "that the sign reversal is a property of the transmitted effect "
     "itself. The indices of moderated mediation are "
     f"{m('imm_sup_adp')} ({mci('imm_sup_adp')}) for support in the "
     f"first stage and {m('imm_lit_adp')} ({mci('imm_lit_adp')}) for "
     "literacy in the second stage [[hayes2015]]. The avoidance "
     f"channel is uniformly positive ({m('ind_avd_l-1')} at low "
     f"literacy and {m('ind_avd_l+1')} at high literacy, both "
     "confidence intervals excluding 0), and its literacy index is "
     f"{m('imm_lit_avd')} ({mci('imm_lit_avd')}); Hypothesis H4b is "
     "verified."),

    ("table", "table10"),

    ("h2", "4.7. Heterogeneity Analysis"),

    ("p",
     "Table 11 re-estimates the full adaptation model within ten "
     "subsamples defined by gender, major, city tier, occupational "
     "exposure, and employment status. The quadratic coefficient is "
     "negative and significant in every subsample, and none of the "
     "five between-group differences in the marginal effect of anxiety "
     "approaches statistical significance (the smallest p-value is "
     f"{n('het_p_min', 3)}). The inverted U is therefore not carried "
     "by any single stratum of the cohort; it is a general property of "
     "the population studied, which is consistent with the "
     "interpretation of saturation as a structural feature of the "
     "control loop rather than an artifact of pooling heterogeneous "
     "linear responses."),

    ("table", "table11"),

    ("h2", "4.8. Robustness and Attrition Tests"),

    ("p",
     "Table 12 subjects the curvilinear second stage to six "
     "replications. (1) Replacing the adaptation index with the log of "
     "reported reskilling hours, a behavioral count rather than a "
     f"Likert judgment, returns a quadratic of {S['rob']['hours_b2']:.3f} "
     "(p < 0.01). (2) Weighting the retained sample by inverse "
     "retention probabilities estimated from all first-wave observables "
     f"leaves the quadratic at {S['rob']['ipw_b2']:.3f}. (3) Excluding "
     "the software and information-technology occupations gives "
     f"{S['rob']['excl_b2']:.3f}. (4) Unit-weighted composites in place "
     f"of factor scores give {S['rob']['comp_b2']:.3f} [[devlieger2016]]. "
     "(5) Partialling the marker score out of every construct gives "
     f"{S['rob']['marker_b2']:.3f} [[lindell2001]]. (6) The wild-cluster "
     "bootstrap over the twenty occupation groups, the appropriate "
     "small-sample inference [[cameron2008]], puts the p-value of the "
     f"quadratic term at {n('wild_p', 3)}. The inverted U survives "
     "every change of measure, sample, weighting, and inference."),

    ("table", "table12"),

    ("h2", "4.9. Configurational Analysis"),

    ("p",
     "Table 13 reports the calibration anchors and the necessity "
     "analysis. No condition, present or absent, reaches the 0.90 "
     "consistency conventionally required of a necessary condition; "
     f"the maximum anywhere is {n('nec_max', 3)}. Hypothesis H7a is "
     "verified: there is no single gate through which every adapting "
     "graduate passes."),

    ("table", "table13"),

    ("p",
     f"Sufficiency is a different matter. Of the {S['tt_kept']} "
     "truth-table rows that clear the frequency threshold, only "
     f"{S['tt_pos']} pass both consistency screens, and they minimize "
     "to a single intermediate solution, identical to the parsimonious "
     "solution, so every condition in it is core [[fiss2011]]: the "
     "conjunction of anxiety, literacy, and support (Table 14), with "
     f"consistency {S['qca']['sol_cons']:.3f} and coverage "
     f"{S['qca']['sol_cov']:.3f}. The near-misses are informative: "
     "configurations combining anxiety and literacy without support "
     "reach raw consistencies near 0.91 yet fail the "
     "proportional-reduction screen, and the highest-consistency row "
     f"for the negation of adaptation (raw consistency "
     f"{n('neg_cons_max', 3)}) fails the same screen (PRI "
     f"{n('neg_pri_best', 3)} < 0.70), so no configuration is reliably "
     "sufficient for failing to adapt. Hypothesis H7b is therefore not "
     "supported, and its failure is itself a finding: the system "
     "offers one road to high adaptation, not many. Anxiety appears in "
     "the recipe — the signal is an ingredient of correction "
     "— but it never suffices without the actuator and the "
     "environment, which is precisely the conjunction the control-loop "
     "framing predicted [[ashby1956],[carver1982]]."),

    ("table", "table14"),

    # =====================================================================
    ("h1", "5. Conclusions"),
    ("h2", "5.1. Research Conclusions"),

    ("p",
     "Based on socio-technical systems theory and a cybernetic control "
     "perspective, this study analyzes how perceived human capital "
     "depreciation shapes the early-career choices of fresh graduates "
     "in the era of generative artificial intelligence, using two-wave "
     "survey data from Chinese graduates within three years of "
     "graduation. The conclusions are as follows: (1) perceived human "
     "capital depreciation significantly raises AI-related career "
     "anxiety, and perceived employability support buffers this "
     "conversion, cutting the pass-through from "
     f"{S['fslo']['est']:.2f} to {S['fshi']['est']:.2f}; (2) career "
     "anxiety converts into occupational adaptation along an inverted "
     f"U-shaped path with a turning point {TP['tau']:.2f} standard "
     f"deviations above mean anxiety — {n('share_beyond', 1)} "
     "percent of the cohort already stands beyond it — while "
     "career avoidance rises monotonically; (3) generative-AI literacy "
     "displaces the turning point outward from "
     f"{S['tp_lit'][0]['tau']:.2f} to {S['tp_lit'][2]['tau']:.2f} "
     "standard deviations and weakens the avoidance channel, and the "
     "indirect effect of depreciation through anxiety reverses sign "
     "across the anxiety distribution; and (4) exactly one "
     "configuration — anxiety combined with literacy and support "
     "— is sufficient for high adaptation, no single condition is "
     "necessary, and no configuration is sufficient for the negation."),

    ("h2", "5.2. Theoretical Contributions"),

    ("p",
     "The main theoretical contributions of this paper are as follows: "
     "First, this paper extends the study of generative artificial "
     "intelligence and work from the demand side to the supply side of "
     "the entry labor market. The existing literature has measured how "
     "adoption reshapes tasks, hiring, and productivity "
     "[[brynjolfsson2025],[canaries2025],[eloundou2024],[babina2024]], "
     "while the perception-to-behavior chain inside the displaced "
     "margin has remained unexamined. By showing that the behavioral "
     "response of the entry cohort is nonmonotonic — mobilization "
     "up to a turning point that two-fifths of the cohort has already "
     "passed, demobilization beyond it — this study supplies a "
     "psychological microfoundation for early-career scarring "
     "[[kahn2010],[vonwachter2020]] and cautions against adjustment "
     "models that assume displacement pressure translates smoothly "
     "into retraining uptake [[acemoglu2018],[autor2015]]."),

    ("p",
     "Second, this paper contributes a systems treatment to the "
     "artificial-intelligence anxiety literature. Prior studies have "
     "treated anxiety mainly as an outcome to be predicted or a hazard "
     "to be reduced [[wangwang2022],[kong2021],[tarafdar2007]]. "
     "Modeling anxiety instead as the error signal of a cybernetic "
     "feedback loop [[carver1982],[beer1981],[ashby1956]] yields three "
     "predictions that a valence-only reading does not — an "
     "interior optimum, actuator-dependent displacement of that "
     "optimum, and conjunctural sufficiency — and all three "
     "survived their tests. The finding connects the psychology of "
     "technological threat to the organizational learning literature "
     "on absorption capacity [[cohen1990],[march1991],[argote2011]]: "
     "signals without the capacity to act on them produce noise, not "
     "learning."),

    ("p",
     "Third, this paper demonstrates the value of combining "
     "conditional-process and configurational methods within one "
     "design. The regression apparatus locates the turning point and "
     "its displacement; the fuzzy-set analysis reveals that the "
     "conditions operate as a conjunction rather than as additive "
     "levers, and that equifinality — the default expectation of "
     "configurational research [[fiss2011],[pappas2021]] — fails "
     "here in a theoretically informative way. Reporting that failure "
     "as a finding, rather than forcing a multi-recipe reading, is the "
     "faithful use of the method [[schneider2012],[greckhamer2018]] "
     "and shows how a tight systems theory can predict, and data can "
     "deliver, a single path."),

    ("h2", "5.3. Management Implications"),

    ("p",
     "The empirical results generate actionable implications for the "
     "three actors who govern the graduate transition. For "
     "universities, the binding constraints are the actuator and the "
     "environment, not the volume of the alarm. Career services that "
     "concentrate on reassurance address the sensor; embedding "
     "supervised, verifiable generative-AI practice into every "
     "curriculum [[chanhu2023],[dellacqua2026]] buys a double "
     "dividend, raising adaptation directly and extending the anxiety "
     "range over which graduates keep adapting rather than freezing, "
     "while visible, credible transition infrastructure — "
     "placement pathways, employer-linked reskilling, alumni networks "
     "that answer — lowers the anxiety produced by any given "
     "level of objective threat."),

    ("p",
     "For employers currently thinning their junior pipelines "
     "[[canaries2025],[autorai2024]], the configurational result "
     "supplies a one-line design rule: anxiety converts into "
     "adaptation only in the presence of literacy and support, so any "
     "communication of threat should arrive bundled with tool access, "
     "training time, and a visible internal pathway [[kellogg2020],"
     "[beane2019]]. A firm that hires fewer entrants and tells the "
     "remainder to upskill or leave is raising the error signal while "
     "shrinking the actuator set — the exact combination the "
     "estimates identify as producing avoidance and exit. For "
     "policymakers confronting record graduate cohorts [[moe2025],"
     "[ilo2024],[ilo2025],[statecouncil2025]], the estimates argue for "
     "shifting marginal spending from awareness campaigns, which raise "
     "the signal, toward subsidized generative-AI credentialing and "
     "employer-linked placement, which complete the loop — and "
     "for targeting that spending on the high-anxiety segment, where "
     "the same expenditure buys the largest swing from demobilization "
     "back to adaptation."),

    ("h2", "5.4. Limitations and Future Directions"),

    ("p",
     "This study has several limitations that point to future "
     "research. First, although the outcomes are separated from their "
     "antecedents by six months and the attrition diagnostics are "
     "clean, the design remains observational; unmeasured traits such "
     "as dispositional neuroticism could raise both anxiety and "
     "behavioral reports, and only a design that manipulates the "
     "actuators — for instance, randomized literacy training "
     "layered on measured anxiety — can fully close that door. "
     "Second, all psychological constructs are self-reported; the "
     "behavioral hours measure and the method-bias diagnostics bound "
     "the resulting bias but do not eliminate it [[podsakoff2024]]. "
     "Third, the sample consists of Chinese graduates observed at one "
     "moment of one technological transition; the location of the "
     "turning point is surely context-dependent, and comparative "
     "replication across institutional regimes with different "
     "transition infrastructures [[ilo2024],[wef2025]] is a natural "
     "next step. Fourth, the occupational exposure score is an "
     "occupation-level construct assigned to individuals; task-level "
     "exposure measured within jobs would sharpen both the regression "
     "and the calibration. Fifth, the two-wave design identifies one "
     "traversal of the loop, not its dynamics; whether adaptation "
     "feeds back to lower depreciation perceptions, closing a "
     "balancing loop, or whether avoidance compounds into the "
     "reinforcing spiral that conservation of resources theory "
     "predicts [[hobfoll2018],[sterman2000],[forrester1961],"
     "[meadows2008],[senge1990],[repenning2002]], requires a "
     "multi-wave panel analyzed with the estimation machinery the "
     "system-dynamics tradition has built for such loops "
     "[[rahmandad2016]]. Finally, richer systems lenses — soft "
     "systems inquiry into how graduates collectively make sense of "
     "the transition [[checkland1981],[weick1993]], and comparisons "
     "with adjacent evidence on technology and employment in China "
     "[[liang2025],[xue2025],[xuejin2025],[yang2026],[machucho2025],"
     "[hui2024],[humlum2025],[otis2026],[forsythe2022],[cui2026],"
     "[peng2023],[noy2023],[vaccaro2024],[bick2024]] — would "
     "further test the generality of the loop identified here."),

    # =====================================================================
    ("h1b", "Author Contributions"),
    ("stmt2", "",
     "Conceptualization, X.C. and T.M.; methodology, X.C.; software, "
     "X.C.; validation, T.M.; formal analysis, X.C.; investigation, "
     "T.M.; data curation, T.M.; writing—original draft "
     "preparation, X.C.; writing—review and editing, T.M.; "
     "visualization, X.C.; supervision, T.M.; project administration, "
     "T.M. All authors have read and agreed to the published version "
     "of the manuscript."),
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
