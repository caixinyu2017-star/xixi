# -*- coding: utf-8 -*-
"""The manuscript text.

Every quantitative statement is interpolated from the model output in
tables/summary.json, produced by analysis/run_all.py, so the prose cannot
disagree with what the code computed. Citations are [[key]] markers, resolved
by build_docx.py into APA author-date form; a key suffixed with _n is
rendered narratively.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "tables", "summary.json"),
          encoding="utf-8") as _fh:
    S = json.load(_fh)

CAL, DYN, REF = S["calibration"], S["dynamics"], S["reference_study"]
MOD, CON, PRE = S["moderation"], S["conditions"], S["precision"]
BEN, PAR = S["scaffold_benefit"], S["params"]


def f2(x):
    return "%.2f" % x


def f3(x):
    return "%.3f" % x


def pct(x):
    return "%.1f" % (100.0 * x)


def r2(x):
    """A correlation or coefficient in APA form, without the leading zero."""
    s = "%.2f" % x
    return s.replace("0.", ".").replace("-.", "−.")


def r3(x):
    s = "%.3f" % x
    return s.replace("0.", ".").replace("-.", "−.")


BEN_LO = BEN["Low anxiety (lowest quartile)"]
BEN_HI = BEN["High anxiety (highest quartile)"]

TITLE = ("Does Parental Career Support Buffer or Amplify the Association "
         "Between Career Anxiety and Career Decision-Making Difficulties? "
         "A Simulation Study of a Reported Moderation")

AUTHORS = [("Xinyu Cai ", False), ("1", True),
           (" and Tiantian Mo ", False), ("1,*", True)]

AFFILIATIONS = [
    ("1", "College of Business, Jiaxing University, Jiaxing 314001, "
          "China; caixinyu@zjxu.edu.cn"),
    ("*", "Correspondence: 00008227@zjxu.edu.cn"),
]

ABSTRACT = (
    "A recent study of Chinese female undergraduates reported that the "
    "association between career anxiety and career decision-making "
    "difficulties was stronger, not weaker, among students reporting more "
    "frequent parental career support. The present study asks what would "
    "have to be true of the underlying process for such a pattern to arise. "
    "A dynamic model was specified in which career anxiety reduces both the "
    "amount and the informational yield of career exploration, exploration "
    "builds career decision-making self-efficacy, and self-efficacy sustains "
    "further exploration, with parental involvement entering as reassurance, "
    "as scaffolding of the student's own exploration, and as involvement that "
    "takes the decision over. The model was calibrated so that a simulated "
    "cross-section reproduced the six correlations reported in that study, "
    f"which it did with a root mean squared error of {f3(CAL['rmse'])}. "
    "Simulated cross-sectional studies were then analysed with the same "
    "conditional process procedure the original used. Across the plausible "
    "parameter space, amplification was uncommon, arising in "
    f"{pct(CON['share_amplifying'])} per cent of "
    f"{CON['n_cells']:d} parameter combinations, and involvement that took "
    "the decision over produced buffering rather than amplification. "
    "Amplification arose instead where involvement scaffolded exploration "
    "the student was too anxious to undertake: scaffolding reduced simulated "
    f"difficulty by {f3(BEN_LO)} for the least anxious quartile and by "
    f"{f3(BEN_HI)} for the most anxious. The reported moderation is "
    "therefore more consistent with autonomy-supportive help that anxious "
    "students cannot use than with directive involvement, and distinguishing "
    "the two requires measuring the kind of support rather than its "
    "frequency.")

KEYWORDS = ("career decision-making difficulties; career anxiety; career "
            "decision-making self-efficacy; parental career support; "
            "computational modeling")


INTRO_BLOCKS = [
    ("h1", "Introduction"),
    ("p",
     "Career decision-making difficulties are among the most consistently "
     "studied outcomes in vocational psychology, and the constructs that "
     "accompany them are by now familiar. Career anxiety is associated with "
     "greater difficulty in deciding [[fuqua1987]], [[campagna2007]], "
     "[[saka2007]]; career decision-making self-efficacy is associated with "
     "less [[choi2012]], [[udayar2020]]; and the social context in which a "
     "young person decides, parental involvement in particular, is "
     "associated with both [[dietrich2009]], [[zhou2024]]. Social Cognitive "
     "Career Theory supplies the framework within which these associations "
     "are usually interpreted [[lent1994]], [[lent2000]]."),
    ("p",
     "Within that framework, one recent finding is difficult to accommodate. "
     "In a mixed-methods study of 407 female undergraduates at four non-elite "
     "Chinese universities, [[panhe2026_n]] reported that the association "
     "between career anxiety and career decision-making difficulties was "
     "stronger among students who reported more frequent parental career "
     "support. Support, on that estimate, did not buffer the "
     "relationship between anxiety and difficulty; it accompanied a steeper "
     "one. Their qualitative phase suggested that what mattered was not how "
     "often parents were involved but how that involvement was experienced, "
     "and specifically whether it left the student any autonomy."),
    ("p",
     "That interpretation is plausible, and it is consistent with a long "
     "line of work distinguishing autonomy-supportive from controlling "
     "career involvement [[guay2003]], [[dietrich2009]]. It is also, on "
     "cross-sectional evidence, difficult to test. A moderation coefficient "
     "estimated at one point in time is a summary of a process that has been "
     "running for years, and several quite different processes can leave the "
     "same summary behind. The question the present study asks is therefore "
     "not whether the reported moderation is correct, which its authors are "
     "better placed to judge, but what would have to be true of the "
     "underlying process for a pattern of that kind to arise at all."),
    ("p",
     "Answering a question of that form calls for a different method from "
     "the one that raised it. We specify a dynamic model of the process, "
     "calibrate it so that a simulated cross-section reproduces the "
     "correlations actually reported, and then run on the simulated data "
     "exactly the analysis the original study ran. Because the generating "
     "process is known by construction, the relationship between what is "
     "happening and what a cross-sectional analysis reports can be examined "
     "directly. The approach follows a small tradition of formalising social "
     "cognitive theory as an executable system [[riley2016]], [[mozahem2022]] "
     "rather than as a set of paths, and it inherits that tradition's central "
     "caution: what a simulation establishes is what follows from a set of "
     "assumptions, not what is the case."),
    ("p",
     "The model rests on three propositions, each with independent empirical "
     "support. First, career anxiety reduces not only how much a student "
     "explores but how much they get out of exploring, because anxiety "
     "occupies the attentional resources that interpreting new information "
     "requires [[eysenck1992]], [[eysenck2007]], [[shi2019]]. Second, "
     "exploration is the principal route by which career decision-making "
     "self-efficacy is built, and self-efficacy in turn sustains exploration, "
     "so the two form a reinforcing pair [[bandura1997]], [[lentbrown2013]], "
     "[[kleine2021]], [[guan2017]]. Third, parental involvement can enter "
     "this system in more than one way: it can reassure, it can support the "
     "student's own exploring, or it can conduct the exploration on the "
     "student's behalf [[dietrich2009]]. These are not variants of a single "
     "quantity, and the study turns on the difference between them."),
    ("p",
     "Several gaps motivate the present analysis. First, the moderating role "
     "of parental support in the anxiety–difficulty association has been "
     "estimated but not explained: no account has been offered of a process "
     "that would produce amplification rather than buffering. Second, the "
     "distinction between supportive and directive involvement is drawn "
     "verbally in this literature but is rarely represented in a way that "
     "generates differing predictions. Third, the instruments in common use "
     "measure the frequency of parental career behaviours rather than their "
     "kind, so the two accounts are not separated by the measurement. "
     "Fourth, and more generally, conditional process models in this field "
     "are estimated on cross-sections of processes that unfold over years, "
     "and, as [[maxwell2007_n]] showed, the correspondence between the two "
     "is assumed rather than examined."),
    ("p",
     "Building on these gaps, the present study addresses three research "
     "questions."),
    ("p",
     "RQ1: Can a dynamic model in which anxiety degrades career exploration, "
     "exploration builds self-efficacy, and self-efficacy sustains "
     "exploration reproduce the pattern of cross-sectional correlations "
     "reported among career anxiety, career decision-making self-efficacy, "
     "perceived parental career support and career decision-making "
     "difficulties?"),
    ("p",
     "RQ2: Within such a model, under what conditions does parental "
     "involvement amplify rather than buffer the association between career "
     "anxiety and career decision-making difficulties?"),
    ("p",
     "RQ3: What do the resulting patterns imply for the measurement of "
     "parental career support and for the interpretation of conditional "
     "process models estimated on cross-sectional data?"),
    ("p",
     "The contribution is accordingly a conditional one. The study does not "
     "establish how parental involvement operates among Chinese "
     "undergraduates, and it collects no data from any student. It "
     "establishes what a process would have to look like for a reported "
     "pattern to follow from it, and what measurement would be needed to "
     "tell the candidate processes apart."),

    # =====================================================================
    ("h1", "Literature Review"),

    ("h2", "Social Cognitive Career Theory as a System Rather Than a Path"),
    ("p",
     "Social Cognitive Career Theory holds that self-efficacy beliefs, "
     "outcome expectations and goals jointly shape career behaviour, and "
     "that these are formed and revised through experience "
     "[[lent1994]], [[lent2000]]. In its career self-management form the "
     "theory is explicit that adaptive career behaviours and the beliefs "
     "supporting them influence one another over time [[lentbrown2013]]. "
     "Empirical work has followed: reciprocal relations between career "
     "exploration and the developing sense of a future working self have "
     "been shown across waves [[guan2017]], and meta-analytic evidence "
     "places self-efficacy for exploration among the strongest correlates of "
     "exploration itself [[kleine2021]]."),
    ("p",
     "Most applications nonetheless estimate the theory as a path model on a "
     "single cross-section. That practice is not mistaken, but it "
     "represents a system of mutual influence as a sequence of one-way "
     "arrows, and the two need not agree about anything beyond the sign of a "
     "correlation [[maxwell2007]], [[colepreacher2014]]. Where a theory says "
     "that A shapes B and B shapes A, a cross-section reports one number "
     "where the theory implies a loop. Representing the theory as an "
     "executable dynamic system, as [[riley2016_n]] have done for social "
     "cognitive theory in health behaviour and [[mozahem2022_n]] for career "
     "choice, makes the difference visible."),

    ("h2", "Career Anxiety, Exploration and the Yield of Looking"),
    ("p",
     "That career anxiety accompanies career decision-making difficulty is "
     "among the older findings in this literature [[fuqua1987]] and among "
     "the better replicated [[campagna2007]], [[saka2007]], [[udayar2020]]. "
     "The mechanism usually proposed is avoidance: anxious students postpone "
     "the decision and the activities that would inform it [[anderson2003]]. "
     "Career anxiety has also been linked to broader adjustment outcomes in "
     "student samples [[mucel2025]]."),
    ("p",
     "Attentional control theory suggests a second and less discussed "
     "mechanism. Anxiety consumes the executive resources that complex "
     "processing requires, so performance falls further than effort does "
     "[[eysenck1992]], [[eysenck2007]]; meta-analytic evidence supports an "
     "association between anxiety and reduced attentional control "
     "[[shi2019]]. Applied to career exploration, the implication is that an "
     "anxious student who does spend an afternoon reading about occupations "
     "extracts less usable information from that afternoon than a composed "
     "student would. Anxiety would then reduce not only the amount of "
     "exploration but its yield, and the two have different consequences: "
     "reduced amount can be compensated by prompting the student to look, "
     "whereas reduced yield cannot."),

    ("h2", "Self-Efficacy as a Consequence of Exploration"),
    ("p",
     "Career decision-making self-efficacy is negatively associated with "
     "career indecision across many samples [[choi2012]], [[udayar2020]], "
     "[[bi2023]], and it is generally modelled as a mediator between "
     "affective or dispositional inputs and decision outcomes. Its status as "
     "an outcome is less often modelled. In social cognitive theory the "
     "principal source of efficacy beliefs is mastery experience "
     "[[bandura1997]], which in this domain means exploring and finding that "
     "the exploring produced something. Efficacy is therefore downstream of "
     "exploration as well as upstream of it, and the reinforcing pair this "
     "creates is what allows small differences in initial anxiety to "
     "accumulate into large differences in eventual indecision "
     "[[jaensch2015]]. Meta-analytic work on the antecedents of career "
     "decision self-efficacy points to the same breadth of inputs "
     "[[wang2023]], and the longitudinal evidence reported by "
     "[[liu2024_n]] supports treating it as a quantity that moves."),

    ("h2", "Parental Involvement: Three Functions, One Measure"),
    ("p",
     "Career-specific parental behaviours are conventionally distinguished "
     "into support, interference and lack of engagement [[dietrich2009]], "
     "and self-determination theory adds the distinction between "
     "autonomy-supportive and controlling involvement, which predicts career "
     "indecision even when the amount of involvement does not "
     "[[guay2003]], [[guay2006]]. Social support more broadly is associated "
     "with lower decision-making difficulty, with self-efficacy among the "
     "mediating routes [[zhou2024]]."),
    ("p",
     "For the present purpose these distinctions can be organised by what "
     "the involvement does to the student's own exploring. Involvement may "
     "reassure, lowering anxiety without altering the informational "
     "situation. It may scaffold, raising what the student's own exploration "
     "yields. Or it may substitute, resolving the uncertainty on the "
     "student's behalf. The three have the same sign in a correlation with "
     "difficulty and quite different implications for self-efficacy, because "
     "only the second leaves the student with a mastery experience to "
     "attribute to themselves. Instruments measuring the reported frequency "
     "of parental career behaviours do not separate them, which is the "
     "measurement problem this study ends by describing."),

    ("h2", "The Present Study"),
    ("p",
     "The study proceeds in four steps. A dynamic model of the "
     "anxiety–exploration–efficacy system is specified, with parental "
     "involvement entering through the three functions above. The model is "
     "calibrated so that a simulated cross-section reproduces the "
     "correlations reported by [[panhe2026_n]]. Simulated "
     "cross-sectional studies are then analysed with the same conditional "
     "process procedure used in that study [[hayes2018]], [[aiken1991]]. "
     "Finally, the parameter space is searched for the conditions under "
     "which the analysis returns amplification rather than buffering. "
     "Figure 1 shows the process the model represents."),
    ("fig", "fig1"),
]


METHOD_BLOCKS = [
    ("h1", "Materials and Methods"),

    ("h2", "Design and the Status of the Data"),
    ("p",
     "This is a simulation study. No students were recruited, no "
     "questionnaire was administered, and no dataset describing real people "
     "was analysed. Every number reported below is produced by executing the "
     "study code under a fixed random seed, and re-executing that code "
     "reproduces the tables exactly. The one empirical quantity the study "
     "uses is the correlation matrix [[panhe2026_n]] reported for their "
     f"sample of {REF.get('n', 407) if isinstance(REF.get('n', 407), int) else 407} "
     "female undergraduates, which serves as the calibration "
     "target and is described as such wherever it appears."),
    ("p",
     "The design is accordingly conditional rather than descriptive. It "
     "cannot establish how parental involvement operates in any population. "
     "What it can establish is which processes are capable of producing a "
     "reported pattern and which are not, and that is a question about the "
     "logical relations among assumptions, for which a simulation is the "
     "appropriate instrument rather than a substitute for data."),

    ("h2", "The Dynamic Model"),
    ("p",
     "Four quantities evolve together over the weeks of a decision horizon "
     "for each simulated student: unresolved uncertainty about career fit, "
     "career decision-making self-efficacy, career anxiety, and the "
     "exploration undertaken in the current week. The horizon is set at "
     f"{DYN['weeks']:d} weeks, approximately one academic year."),
    ("p",
     "Exploration effort in a given week rises with self-efficacy and with "
     "unresolved uncertainty and falls with anxiety, the last of these "
     "representing avoidance of the decision situation [[anderson2003]]. The "
     "informational yield of that effort is then degraded by anxiety, "
     "following attentional control theory [[eysenck2007]], [[shi2019]]: the "
     "same hour of looking returns less usable information to an anxious "
     "student. Uncertainty falls with the information actually obtained and "
     "regenerates slowly, since options and requirements change."),
    ("p",
     "Self-efficacy is where the three functions of parental involvement "
     "come apart. Efficacy moves towards the recent productivity of the "
     "student's own agency: how much of the progress was theirs, and how "
     "well their own effort converted into information. Involvement that "
     "resolves uncertainty on the student's behalf lowers the first quantity "
     "without raising the second, so uncertainty falls while efficacy does "
     "not, which is the formal counterpart of the observation that doing "
     "something for a young person and helping them do it are not the same "
     "act [[bandura1997]], [[guay2003]]. Anxiety, finally, moves towards the "
     "level implied by current uncertainty, weighted by an approaching "
     "deadline, less the reassurance that self-efficacy and parental "
     "involvement provide. A stable dispositional component is retained "
     "alongside the responsive one, without which the loop always unwinds "
     "and no simulated student remains undecided."),
    ("p",
     "Measured career decision-making difficulty is formed from two "
     "components, in keeping with instruments that score both a lack of "
     "information and internal or external conflict [[gati1996]], "
     "[[levin2023]]: the unresolved uncertainty just described, and conflict "
     "between the option the student has come to prefer and the option the "
     "family endorses. Conflict requires all three of a formed preference, a "
     "divergent family position, and too little standing to reconcile them, "
     "the last being lower for anxious students. Table 1 lists the "
     f"quantities and Table A1 the {PAR['n']:d} parameters, each with the "
     "interval over which the analysis varies it and a statement of where "
     "its value came from."),
    ("table", "table1"),

    ("h2", "Calibration"),
    ("p",
     "The model has no data of its own to be fitted to, and it is not fitted "
     "to any. What it is held to is the pattern of association the empirical "
     "literature reports. A subset of parameters was searched by coordinate "
     "descent so that the six correlations among the four constructs in a "
     "simulated cross-section approached those [[panhe2026_n]] reported. "
     "Observed variables were formed by adding classical "
     "measurement error to the latent quantities, with the error share "
     "bounded by the composite reliabilities reported for those four scales, "
     "so that the calibration could not buy agreement by assuming "
     "implausibly unreliable measurement [[colepreacher2014]]."),
    ("p",
     "One parameter was deliberately excluded from the search: the share of "
     "parental involvement that takes the decision over rather than "
     "supporting the student's own exploring. That quantity is what the "
     "study varies, and calibrating it against the same correlations that "
     "are later used to assess it would assume the answer."),

    ("h2", "Simulated Studies and Their Analysis"),
    ("p",
     "Simulated cohorts were analysed exactly as the original study analysed "
     "its sample. A conditional process model was estimated in which career "
     "anxiety predicts difficulty both directly and through self-efficacy, "
     "with perceived parental involvement moderating the direct path "
     "[[hayes2018]]. Variables were mean-centred before the product term was "
     "formed [[aiken1991]], the indirect effect and the interaction were "
     f"bracketed by {S['meta']['boots']:d} percentile bootstrap samples, and "
     "simple slopes were computed at one standard deviation either side of "
     "the moderator. The estimator was written for this study rather than "
     "taken from a package, so that what the simulated analyst does is fully "
     "specified; it was verified by recovering known coefficients from data "
     "generated with those coefficients."),
    ("p",
     "Three analyses follow. The first estimates the conditional process "
     "model on a cohort the size of the original sample. The second varies "
     "the share of involvement that takes the decision over, from none to "
     "all, and records what the same analysis then reports. The third "
     "searches a factorial grid over the parameters governing conflict and "
     "involvement, and records in what fraction of that space the analysis "
     "returns amplification. A fourth examines how precisely an interaction "
     "of this kind is estimated at the sample sizes this literature uses."),
]


RESULT_BLOCKS = [
    ("h1", "Results"),

    ("h2", "Calibration Against the Reported Correlations"),
    ("p",
     "Table 2 compares the correlations produced by the calibrated model "
     "with those reported for the original sample. The root mean squared "
     f"difference is {f3(CAL['rmse'])}. Five of the six correlations are "
     "reproduced closely, including the association between career anxiety "
     "and decision difficulty, which is the one the study's central question "
     "concerns."),
    ("p",
     "The exception is the association between parental support and "
     "self-efficacy, which the model reproduces at "
     f"{r2([p for p in CAL['pairs'] if p['pair'] == 'CDSE-PCS'][0]['model'])} "
     "against a reported "
     f"{r2([p for p in CAL['pairs'] if p['pair'] == 'CDSE-PCS'][0]['target'])}. "
     "The shortfall is informative rather than incidental. In the model, "
     "involvement raises self-efficacy only to the extent that it scaffolds "
     "the student's own exploring; a population in which involvement is "
     "substantially directive cannot generate an association as strong as "
     "the one reported. Either the families in that sample were unusually "
     "autonomy-supportive, or the reported association reflects something "
     "the model does not represent, such as students with higher efficacy "
     "perceiving the same parental behaviour more favourably, or shared "
     "method variance between self-reported constructs [[podsakoff2003]]. Both "
     "possibilities are returned to in the Discussion."),
    ("table", "table2"),

    ("h2", "The Behaviour of the Modelled Process"),
    ("p",
     "Before any cross-sectional analysis is applied, it is worth recording "
     "what the model does over the horizon. Averaged across simulated "
     f"students, unresolved uncertainty falls from {f2(DYN['u_start'])} to "
     f"{f2(DYN['u_end'])} over the horizon, and self-efficacy falls as well, "
     f"from {f2(DYN['s_start'])} to {f2(DYN['s_end'])}, because the "
     "attribution of progress to one's own effort is modest at the "
     "calibrated value and the exploring most students do returns less "
     "mastery than their starting belief presumes. Neither average is the "
     "feature that matters. Students in the least anxious quartile of the "
     f"dispositional distribution end the year at "
     f"{f2(DYN['u_end_low_trait'])} of their initial uncertainty and at "
     f"{f2(DYN['s_end_low_trait'])} on self-efficacy, while those in the "
     f"most anxious quartile end at {f2(DYN['u_end_high_trait'])} and "
     f"{f2(DYN['s_end_high_trait'])}, having explored less and having "
     "extracted less from what exploring they did. Figure 2 shows the two "
     "pairs of trajectories."),
    ("p",
     "The divergence is not produced by a difference in the strength of any "
     "single path. It is produced by the loop: a student who begins more "
     "anxious explores less, learns less from exploring, builds less "
     "self-efficacy, and therefore explores less again, so that a modest "
     "initial difference is compounded over the horizon. This is what the "
     "reinforcing structure of social cognitive theory implies when it is "
     "allowed to run [[bandura1997]], [[lentbrown2013]], and it is not "
     "visible in a cross-section."),
    ("fig", "fig2"),

    ("h2", "The Conditional Process Model, as the Original Estimated It"),
    ("p",
     "Table 3 reports the conditional process model estimated on a simulated "
     "cohort at the calibrated parameters. Career anxiety is negatively "
     f"associated with self-efficacy (a = {r3(REF['a'])}), self-efficacy is "
     f"negatively associated with difficulty (b = {r3(REF['b'])}), and the "
     f"indirect path is {r3(REF['indirect'])}, with a bootstrap interval of "
     f"[{r3(REF['indirect_ci'][0])}, {r3(REF['indirect_ci'][1])}] that "
     "excludes zero. So far the simulated study recovers the qualitative "
     "structure the original reported."),
    ("p",
     "The moderation does not follow that pattern. The interaction between "
     f"anxiety and involvement is {r3(REF['inter'])}, with a bootstrap "
     f"interval of [{r3(REF['inter_ci'][0])}, {r3(REF['inter_ci'][1])}], and "
     "it is negative. The simple slope of anxiety on difficulty is "
     f"{r3(REF['slope_lo'])} at one standard deviation below the mean of "
     f"involvement and {r3(REF['slope_hi'])} at one standard deviation "
     "above. In the calibrated model, in other words, parental involvement "
     "buffers the association between anxiety and difficulty, which is the "
     "opposite of what was reported for the sample the model was calibrated "
     "to reproduce."),
    ("table", "table3"),

    ("h2", "What the Kind of Involvement Does"),
    ("p",
     "Table 4 and the left panel of Figure 3 vary the share of involvement "
     "that takes the decision over rather than supporting the student's own "
     "exploring, holding everything else at the calibrated values. The "
     f"interaction runs from {r3(MOD['0.0']['inter'])} where involvement is "
     f"wholly scaffolding to {r3(MOD['1.0']['inter'])} where it is wholly "
     "directive. The direction is the reverse of the one we anticipated. "
     "Directive involvement does not amplify the association between anxiety "
     "and difficulty; it buffers it most strongly of all, because it "
     "resolves uncertainty irrespective of whether the student is in any "
     "condition to resolve it themselves."),
    ("p",
     "The amplifying pattern appears at the other end, where involvement is "
     "wholly scaffolding, and the reason is visible in Table 5. Scaffolding "
     "raises what the student's own exploration yields, and a student too "
     "anxious to explore has little for it to multiply. Among the least "
     "anxious quartile, moving from low to high involvement reduces simulated "
     f"difficulty by {f3(BEN_LO)}; among the most anxious quartile the same "
     f"movement reduces it by {f3(BEN_HI)}. Help of this kind reaches those "
     "already able to use it, and the gap between the composed and the "
     "anxious therefore widens as it is provided, which is precisely what a "
     "positive interaction between anxiety and support records."),
    ("table", "table4"),
    ("table", "table5"),
    ("fig", "fig3"),

    ("h2", "How Often Amplification Occurs"),
    ("p",
     "Table 6 reports a factorial search over the parameters governing "
     "conflict and involvement. Amplification, defined as a positive "
     f"interaction, arises in {CON['n_amplifying']:d} of "
     f"{CON['n_cells']:d} parameter combinations, or "
     f"{pct(CON['share_amplifying'])} per cent of the space searched. It is "
     "concentrated where involvement is predominantly scaffolding and where "
     "that scaffolding resolves comparatively little uncertainty on its own "
     "account; it does not occur at all where the directive share reaches "
     "one half. Amplification is therefore a possible outcome of this "
     "process but an uncommon one, and it carries a specific signature."),
    ("table", "table6"),

    ("h2", "How Precisely Such an Interaction Is Estimated"),
    ("p",
     "One explanation for a discrepant moderation is that interactions are "
     "estimated imprecisely, so a single study may report one by chance. "
     "Table 7 examines this directly by drawing repeated simulated studies "
     "at the calibrated parameters. At a cohort of "
     f"{PRE['n']:d}, the size of the original sample, the estimated "
     f"interaction has a mean of {r3(PRE['mean'])} and a standard deviation "
     f"of {r3(PRE['sd'])} across studies, with a central 95 per cent range "
     f"of [{r3(PRE['p025'])}, {r3(PRE['p975'])}], and it is detected at the "
     f"conventional threshold in {f2(PRE['pct_significant'])} per cent of "
     "studies. Sampling variability of that magnitude does not span zero, "
     "let alone reach a positive value of the size reported. Within this "
     "model, chance is not a sufficient account of the discrepancy."),
    ("table", "table7"),
]


DISCUSSION_BLOCKS = [
    ("h1", "Discussion"),
    ("p",
     "The study asked what would have to be true for parental career support "
     "to accompany a steeper rather than a shallower association between "
     "career anxiety and career decision-making difficulties. The model "
     "returns an answer, and it is not the answer we expected."),

    ("h2", "Amplification Is a Signature of Help That Must Be Used"),
    ("p",
     "Involvement that takes the decision over buffers the anxiety–"
     "difficulty association, and buffers it strongly. It does so for an "
     "uninteresting reason: it lowers uncertainty whether or not the student "
     "is in a state to lower it themselves, and so it helps the anxious at "
     "least as much as the composed. Involvement that scaffolds the "
     "student's own exploring behaves differently, because scaffolding "
     "multiplies a quantity that anxiety has already suppressed. In the "
     "model, moving from low to high scaffolding involvement reduced "
     f"difficulty by {f3(BEN_LO)} among the least anxious quartile and by "
     f"{f3(BEN_HI)} among the most anxious. Support of that kind widens the "
     "distance between the two groups, and a moderation analysis records "
     "that widening as a positive interaction."),
    ("p",
     "If this is right, the reported moderation is not evidence that "
     "parental involvement was intrusive. It is more consistent with "
     "involvement that was well intentioned and autonomy-supportive in "
     "exactly the way the literature recommends [[guay2003]], "
     "[[dietrich2009]], and that for that reason failed the students who "
     "were least able to act on it. The implication is uncomfortable, "
     "because autonomy-supportive help is what practitioners are advised to "
     "provide, and it appears to be the form of help whose benefit is most "
     "unequally distributed with respect to anxiety."),
    ("p",
     "This reading is consistent with what the original study's interview "
     "phase reported, though it locates the difficulty elsewhere. Those "
     "interviews described support that was emotionally present but "
     "constraining, and [[panhe2026_n]] concluded that quality rather than "
     "frequency was what mattered. The present analysis agrees that "
     "frequency is the wrong measurement while suggesting that the relevant "
     "quality may not be intrusiveness but the demand that the help places "
     "on the recipient's own capacity to act."),

    ("h2", "What a Cross-Section Can and Cannot Separate"),
    ("p",
     "The calibration exercise is instructive in a second way. A model in "
     "which involvement is substantially directive reproduces five of the "
     "six reported correlations closely while producing an interaction of "
     "the wrong sign. A model in which involvement is wholly scaffolding "
     "produces an interaction of the right sign while reproducing the "
     "support–efficacy correlation less well. The reported correlation "
     "matrix and the reported interaction, in other words, point towards "
     "different accounts of the same construct, and no reweighting of the "
     "model's parameters made both fit comfortably at once."),
    ("p",
     "That tension is not a defect of the original study, which reported "
     "both quantities as it found them. It is a property of measuring "
     "parental involvement by frequency. A frequency score sums behaviours "
     "with opposite implications for self-efficacy, and a single such score "
     "cannot separate a parent who reads vacancy listings aloud from one who "
     "sits with their child while the child reads them. Distinguishing the "
     "accounts requires instruments that record the kind of involvement, of "
     "which the autonomy-support tradition already provides examples "
     "[[guay2003]], [[guay2006]], [[dietrich2009]]."),

    ("h2", "Loops, Paths and the Interpretation of Mediation"),
    ("p",
     "The modelled process is a loop, and the analysis applied to it is a "
     "path model. Over the horizon, a modest difference in initial anxiety "
     "compounds through reduced exploration, reduced mastery experience and "
     "reduced self-efficacy into a substantial difference in eventual "
     f"uncertainty, {f2(DYN['u_end_low_trait'])} against "
     f"{f2(DYN['u_end_high_trait'])} between the extreme quartiles. A "
     "cross-sectional mediation estimated at the end of that process "
     "recovers an indirect effect through self-efficacy, and the estimate is "
     "not meaningless, but it is a summary of accumulated history rather "
     "than a measurement of a transmission occurring at the moment of "
     "measurement [[maxwell2007]], [[colepreacher2014]]. The practical "
     "consequence is that the size of an indirect effect in this literature "
     "should not be read as the size of an effect that an intervention could "
     "expect to move."),

    ("h2", "Implications for Practice"),
    ("p",
     "Three implications follow, each conditional on the model. First, "
     "career services that work through parents should attend to whether the "
     "student is in a condition to use what is offered. Where anxiety is "
     "high, the model suggests that reducing it, or providing help that does "
     "not depend on the student's own exploratory capacity, will reach "
     "students that autonomy-supportive guidance alone will not."),
    ("p",
     "Second, the apparent superiority of directive involvement in these "
     "simulations should not be read as a recommendation. Directive "
     "involvement buffers the anxiety–difficulty association while leaving "
     "self-efficacy unbuilt, and self-efficacy is what the student carries "
     "into the next decision [[bandura1997]]. The model measures one year; "
     "the cost of substitution falls outside it."),
    ("p",
     "Third, and most concretely, instruments used to assess parental career "
     "support in studies of this kind should record the kind of involvement "
     "alongside its frequency. The two accounts the present study "
     "distinguishes make opposite predictions about the interaction, and a "
     "frequency measure cannot tell them apart."),

    # =====================================================================
    ("h1", "Limitations and Future Directions"),
    ("p",
     "The principal limitation is the one the design entails. The study is a "
     "simulation, and its conclusions are conditional on a set of equations "
     f"and on {PAR['n']:d} parameters, of which "
     f"{PAR['counts']['assumed']:d} are modelling choices rather than "
     "measured quantities. A simulation establishes what follows from "
     "assumptions; it cannot establish that the assumptions hold of any "
     "student. Where a parameter could not be grounded, it was swept across "
     "a declared interval rather than defended, and the parameter appendix "
     "records which is which."),
    ("p",
     "Second, the calibration target is a single correlation matrix from one "
     "sample of female undergraduates at four non-elite universities in one "
     "Chinese province [[panhe2026]]. Correlations from a sample of that "
     "size carry sampling error of roughly a tenth in themselves, the sample "
     "was purposive, and nothing about it licenses generalisation. The model "
     "inherits every one of those limits."),
    ("p",
     "Third, the model represents parental involvement as a quantity with a "
     "fixed composition over the horizon. Real families adjust, and "
     "involvement that begins as scaffolding may become directive as a "
     "deadline approaches. A version in which the composition responds to "
     "the student's progress was examined and did not by itself produce "
     "amplification, but the space of such feedbacks is larger than what was "
     "searched."),
    ("p",
     "Fourth, the difficulty measure combines missing information with "
     "conflict in fixed proportion, whereas the instruments used in practice "
     "score the several categories that [[gati1996_n]] set out "
     "[[levin2023]], and the accounts compared here may bear differently on "
     "each. Fifth, the model contains no interpersonal process beyond the "
     "parent, no institutional context, and no labour market, all of which "
     "the original study treated as central to its population."),
    ("p",
     "One property of the calibrated set deserves to be stated rather than "
     "left to be noticed. Mean self-efficacy declines over the simulated "
     f"horizon, from {f2(DYN['s_start'])} to {f2(DYN['s_end'])}, because "
     "calibration to a cross-section fixes the associations among the "
     "constructs and not their trends, and the parameter values that "
     "reproduce those associations happen to place the sustainable level of "
     "self-efficacy below the value the cohort starts from. Longitudinal "
     "studies of undergraduate cohorts more often report a rise. Nothing in "
     "the analysis turns on the direction of the mean, which does not enter "
     "any estimate reported here, but a correlation matrix cannot pin a "
     "trend down, and a study seeking to identify one would have to target "
     "the trend as well."),
    ("p",
     "Three directions follow. The most direct is measurement: a study "
     "recording the kind as well as the frequency of parental career "
     "involvement, alongside anxiety and self-efficacy, would test the "
     "distinction the model draws. The second is longitudinal: the "
     "compounding this model produces is observable across waves, and "
     "reciprocal designs in this literature already exist [[guan2017]]. The "
     "third is experimental: the model predicts that scaffolding help "
     "benefits low-anxiety students more than high-anxiety ones, which is a "
     "testable and falsifiable claim about an intervention."),

    # =====================================================================
    ("h1", "Conclusions"),
    ("p",
     "A reported finding that parental career support accompanied a steeper "
     "association between career anxiety and career decision-making "
     "difficulties was examined by asking what process could produce it. A "
     "dynamic model of career exploration, self-efficacy and anxiety was "
     "specified, calibrated so that a simulated cross-section reproduced the "
     "reported correlations, and analysed with the same conditional process "
     "procedure the original used."),
    ("p",
     "Within that model, involvement that takes the decision over buffers "
     "the association rather than amplifying it, and amplification is "
     f"uncommon, arising in {pct(CON['share_amplifying'])} per cent of the "
     "parameter combinations searched. Where it arises, it arises from help "
     "that scaffolds the student's own exploration: such help multiplies a "
     "capacity that anxiety has suppressed, so it reaches the composed and "
     f"not the anxious, reducing simulated difficulty by {f3(BEN_LO)} in the "
     f"least anxious quartile and by {f3(BEN_HI)} in the most anxious."
     ),
    ("p",
     "The reported moderation is therefore more consistent with "
     "autonomy-supportive help that anxious students were not in a position "
     "to use than with involvement that was intrusive. The two accounts "
     "differ in what they recommend and cannot be separated by an instrument "
     "that counts how often parents are involved. Recording what kind of "
     "involvement it is would separate them, and that is the measurement "
     "this literature now needs."),
]

BACK_BLOCKS = [
    ("h1b", "Author Contributions"),
    ("p",
     "Conceptualisation, X.C. and T.M.; methodology, X.C.; software, X.C.; "
     "formal analysis, X.C.; writing—original draft preparation, X.C.; "
     "writing—review and editing, T.M.; supervision, T.M. All authors have "
     "read and agreed to the published version of the manuscript."),
    ("h1b", "Funding"),
    ("p", "This research received no external funding."),
    ("h1b", "Institutional Review Board Statement"),
    ("p",
     "Not applicable. The study is a simulation and involves no human "
     "participants, no animals and no personal data."),
    ("h1b", "Informed Consent Statement"),
    ("p", "Not applicable."),
    ("h1b", "Data Availability Statement"),
    ("p",
     "No empirical data were collected for this study. The manuscript "
     "reports the output of a simulation model, and every number in it is "
     "produced by executing the study code under a fixed random seed, so "
     "that re-execution reproduces the tables exactly. The one empirical "
     "input is the correlation matrix [[panhe2026_n]] reported for their "
     "sample of 407 female undergraduates, which is used as a "
     "calibration target and is reproduced in Table 2 alongside the "
     "simulated values. The model code, the calibrated parameter set and the "
     "complete output on which every table is built are available from the "
     "corresponding author on request."),
    ("h1b", "Conflicts of Interest"),
    ("p", "The authors declare no conflicts of interest."),
    ("h1b", "Appendix A"),
    ("p",
     "Table A1 lists every parameter of the model with the interval over "
     "which the analysis varies it and a statement of its provenance. "
     f"Of the {PAR['n']:d} parameters, {PAR['counts']['literature']:d} take a "
     f"value bounded by a cited source and {PAR['counts']['assumed']:d} are "
     "modelling choices; the calibration search moved "
     f"{PAR['n_calibrated']:d} of them."),
    ("table", "tableA1"),
]

_RAW = INTRO_BLOCKS + METHOD_BLOCKS + RESULT_BLOCKS + DISCUSSION_BLOCKS + BACK_BLOCKS


def _numbered(blocks):
    out, h1, h2 = [], 0, 0
    for b in blocks:
        if b[0] == "h1":
            h1 += 1; h2 = 0
            out.append(("h1", "%d. %s" % (h1, b[1])))
        elif b[0] == "h2":
            h2 += 1
            out.append(("h2", "%d.%d. %s" % (h1, h2, b[1])))
        else:
            out.append(b)
    return out


BLOCKS = _numbered(_RAW)
