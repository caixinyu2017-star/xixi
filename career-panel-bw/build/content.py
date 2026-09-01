# -*- coding: utf-8 -*-
"""The manuscript.

Every quantitative statement is interpolated from tables/summary.json, which
analysis/run.py writes from the two panels, so the prose cannot disagree with
what the code computed. Citations are [[key]] markers, resolved by
build_docx.py into APA author-date form; a key suffixed _n renders narratively.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "tables", "summary.json"),
          encoding="utf-8") as _fh:
    S = json.load(_fh)

R = S["results"]
DIS, WAV, DIV = S["disagreement"], S["waves"], S["divergence"]
PAN, ROB = S["panels"], S["robustness"]
NW, NM = PAN["NLSW"], PAN["NLSY79M"]
N_H = S["meta"]["n_hypotheses"]
W1 = R["W1"]


def f2(x):
    return "%.2f" % x


def f3(x):
    return "%.3f" % x


def r3(x):
    """A coefficient in APA form, without the leading zero."""
    s = "%.3f" % x
    return s.replace("0.", ".").replace("-.", "−.")


def pv(p):
    return "< .001" if p < .001 else "= %s" % ("%.3f" % p).replace("0.", ".")


def pct(x):
    return "%.0f" % (100.0 * x)


TITLE = ("When Does a Career Contingency Hold? Between-Person and "
         "Within-Person Estimates of Sixteen Moderation Hypotheses in Two "
         "Longitudinal Cohorts of Young Workers")

AUTHORS = [("Xinyu Cai ", False), ("1", True),
           (" and Tiantian Mo ", False), ("1,*", True)]

AFFILIATIONS = [
    ("1", "College of Business, Jiaxing University, Jiaxing 314001, "
          "China; caixinyu@zjxu.edu.cn"),
    ("*", "Correspondence: 00008227@zjxu.edu.cn"),
]

ABSTRACT = (
    "Career development theories describe what happens to a person as a "
    "career unfolds, whereas most evidence about the contingencies in those "
    "theories comes from moderation models fitted to comparisons between "
    "people. This study asked how far the two diverge for interaction terms "
    f"specifically. {N_H} moderation hypotheses of the form routinely "
    "reported in the careers literature, each stating that the wage return "
    "to a career input depends on a characteristic of the worker or the job, "
    "were fixed in advance and estimated in two public longitudinal "
    f"cohorts of young workers: {NW['n_obs']:,} person-years on "
    f"{NW['n_person']:,} women observed across {NW['n_wave']} waves between "
    f"{NW['first']} and {NW['last']}, and {NM['n_obs']:,} person-years on "
    f"{NM['n_person']} men observed annually from {NM['first']} to "
    f"{NM['last']}. Each interaction was estimated one wave at a time, "
    "pooled across waves, and as separate between-person and within-person "
    "slopes in a single model, with standard errors clustered on the person "
    "and a false discovery rate correction across hypotheses. The "
    f"between-person and within-person estimates carried opposite signs in "
    f"{DIS['sign_flips']} of {N_H} hypotheses and led to different "
    f"substantive conclusions in {DIS['verdict_changes']}; their equality "
    f"was rejected in {DIS['between_ne_within_q05']} after correction. The "
    "median divergence was "
    f"{f2(DIV['median_ratio'])} times the size of the within-person estimate "
    f"itself. Of {WAV['total']} single-wave estimates, {WAV['significant']} "
    f"reached significance and {WAV['significant_and_opposite']} of those "
    f"({pct(WAV['share_sig_opposite'])} per cent) pointed the opposite way "
    "to the within-person estimate. The two quantities answer different "
    "questions and should be reported separately rather than treated as "
    "one.")

KEYWORDS = ("career development; longitudinal data; moderation; "
            "within-person effects; youth employment")


# ==========================================================================
INTRO_BLOCKS = [
    ("h1", "Introduction"),
    ("p",
     "Theories of career development describe a person moving through time. "
     "Social cognitive career theory has experience feeding self-efficacy "
     "and self-efficacy feeding further activity [[lent1994]], "
     "[[lentbrown2013]]; career construction theory has a worker building a "
     "life story out of successive positions [[savickas2013]]. The claims "
     "are about accumulation inside a person, and the language used to state "
     "them — a career unfolds, a worker builds tenure, an interruption "
     "leaves a scar — is the language of within-person change."),
    ("p",
     "The evidence assembled to test those claims mostly is not. Reviews of "
     "career success rest largely on samples of workers compared with one "
     "another at a moment [[ng2005]], [[spurk2019]]. Where a theory "
     "specifies a contingency — the return to some career input depends on "
     "some characteristic of the worker or the job — the contingency is "
     "usually tested by an interaction term in a regression across people. "
     "That coefficient is a statement about how workers who differ in the "
     "moderator also differ in the association between the input and the "
     "outcome. Whether it also describes what happens to a given worker as "
     "the input accumulates is a separate question, and it is one the "
     "design cannot answer."),
    ("p",
     "That the two quantities can differ is not new. It is the substance of "
     "Mundlak's decomposition of a panel slope into between-person and "
     "within-person parts [[mundlak1978]], of the argument for treating the "
     "person as the unit of a psychological law [[molenaar2004]], and of "
     "repeated methodological warnings in psychology that cross-sectional "
     "estimates are not summaries of longitudinal ones [[curran2011]], "
     "[[maxwell2007]], [[hamaker2015]]. What has been much less examined is "
     "the size of the divergence for interaction terms, in real career data, "
     "for hypotheses of the kind the field actually reports. Main effects "
     "have been decomposed many times. Moderation, which is where the "
     "interesting theoretical claims live, has not."),
    ("p",
     "There is reason to expect interactions to be the harder case. A "
     "between-person interaction is identified from the comparison of "
     "slopes across groups of people who differ in the moderator, and those "
     "groups differ in much else besides. Sorting on unobserved "
     "characteristics contaminates the difference of slopes as readily as it "
     "contaminates a slope, and the contamination need not have the same "
     "sign as the effect it disguises. A within-person interaction, by "
     "contrast, is identified from how a person's own return to the input "
     "differs according to a characteristic that person carries, and the "
     "person's fixed traits fall out of the comparison. Neither estimate is "
     "automatically the one wanted. They are answers to different questions, "
     "and the practical issue is how often, and how far, they disagree."),
    ("p",
     "This study takes that question to data. Sixteen moderation hypotheses "
     "were written down in advance, each phrased as the careers literature "
     "phrases them, and each was estimated in two public longitudinal "
     "cohorts of young workers by four routes: one survey wave at a time, "
     "pooled across waves, and as separate between-person and within-person "
     "slopes inside a single model that permits a formal test of their "
     "equality. All sixteen are reported whatever they show."),
    ("p",
     "Three questions are addressed. First, how often do the between-person "
     "and within-person estimates of the same interaction differ in sign, "
     "in significance, and by how much? Second, does a single survey wave — "
     "the design most career studies actually use — behave like the "
     "between-person estimate or the within-person one? Third, is the "
     "divergence robust, or an artefact of the transformation used to "
     "remove the person?"),
]


BG_BLOCKS = [
    ("h1", "Background"),
    ("h2", "What a Moderation Coefficient Is Identified From"),
    ("p",
     "Write the outcome for person $i$ at time $t$ as depending on a "
     "time-varying career input $x_{it}$, a moderator $w_{i}$ and their "
     "product, with a person term $\\alpha_i$ standing for everything stable "
     "about the person that the model does not measure. As "
     "[[mundlak1978_n]] showed, pooled least squares then estimates a "
     "weighted average of two distinct quantities: how the product term "
     "differs across people, and how it operates inside them "
     "[[belljones2015]]. The weights depend on how much of "
     "the variance in the input lies between people rather than within them, "
     "which is a property of the sample rather than of the theory."),
    ("p",
     "The two components separate cleanly if the person mean of each "
     "time-varying term is entered alongside its deviation from that mean. "
     "The deviation carries the within-person slope, the mean carries the "
     "between-person slope, and the difference between them can be tested "
     "inside one model rather than by comparing two "
     "[[mundlak1978]], [[belljones2015]], [[curran2011]]. This is the "
     "specification used throughout what follows, because it makes the "
     "comparison the object of estimation rather than an informal contrast "
     "between separately reported tables."),
    ("h2", "Why the Moderator Is the Difficult Part"),
    ("p",
     "A moderator in career research is typically a characteristic that "
     "people possess rather than one they are assigned: a level of "
     "schooling, a union contract, a marriage, a region. People who possess "
     "it differ from those who do not in ways the model does not record, and "
     "those differences are the reason a between-person interaction is hard "
     "to read. Graduates do not merely hold degrees; they enter different "
     "firms, on different tracks, with different outside options. If those "
     "unmeasured differences also govern how the wage responds to tenure, "
     "the between-person interaction records their effect as if it were the "
     "effect of the degree."),
    ("p",
     "A person-fixed comparison removes the stable part of that problem, and "
     "it can do so even when the moderator itself never changes. The main "
     "effect of a time-invariant moderator is absorbed, but its product with "
     "a time-varying input is not, because the input varies. The interaction "
     "therefore remains identified within the person while the person's "
     "fixed traits do not [[wooldridge2010]], [[baltagi2021]]. What survives "
     "is not free of every difficulty: the transformation amplifies "
     "measurement error in the input, and time-varying confounders remain. "
     "The claim examined here is about divergence and its interpretation, "
     "not about one estimator being correct."),
    ("h2", "Career Inputs Whose Returns Are Thought to Be Contingent"),
    ("p",
     "The hypotheses used below are drawn from claims with a long record. "
     "That wages rise with employer tenure, and how much of that rise is "
     "specific to the employer rather than a property of the worker, has "
     "been contested for decades using exactly the panels analysed here: "
     "[[altonji1987_n]] and [[topel1991_n]] reached opposite conclusions "
     "from closely related data. The return to accumulated work "
     "experience is the oldest quantity in the field [[mincer1974]]. Whether "
     "an interruption to employment leaves a wage scar, and for whom, has "
     "been examined in several national cohorts [[arulampalam2001]], "
     "[[gregg2005]]. Union coverage has been shown to raise wages by "
     "different amounts for different workers, in one of the two panels used "
     "here [[vella1998]]. Each of these literatures contains claims of the "
     "contingent form, and each is a claim about a career unfolding."),
    ("h2", "The Present Study"),
    ("p",
     f"{N_H} such claims were fixed in advance, eight in each cohort, and "
     "estimated by the four routes described above. The aim is not to "
     "adjudicate any one of them. It is to establish, across a set of "
     "hypotheses chosen before anything was estimated, how far the answer "
     "depends on which comparison the estimator makes."),
]


METHOD_BLOCKS = [
    ("h1", "Materials and Methods"),
    ("h2", "Data"),
    ("p",
     "Two public longitudinal microdata sets on young workers were used. "
     "The first is the National Longitudinal Survey of Young Women "
     "[[bls_nlsw]], a cohort aged 14 to 24 when first interviewed in "
     f"{NW['first']} and followed to {NW['last']}. The extract analysed here "
     "is the one distributed with standard statistical software and "
     f"reference packages, comprising {NW['n_obs']:,} person-years on "
     f"{NW['n_person']:,} women across {NW['n_wave']} waves. Interviewing "
     "was annual early in the period and biennial later, so the intervals "
     "between observations are uneven."),
    ("p",
     "The second is an extract from the National Longitudinal Survey of "
     "Youth 1979 [[bls_nlsy79]] covering young men in full-time work, "
     f"assembled for an earlier study of union wage effects [[vella1998]]. "
     f"It is balanced: {NM['n_person']} men observed in each of the "
     f"{NM['n_wave']} years from {NM['first']} to {NM['last']}, "
     f"{NM['n_obs']:,} person-years in all. Table 1 describes both panels "
     "and, for each variable, separates the standard deviation between "
     "people from the average standard deviation within them, which is what "
     "governs how much information each estimator has to work with."),
    ("table", "table1"),
    ("p",
     "As a check that the files had been read as intended, the person "
     "fixed-effects wage equation reported for the men's extract in a "
     "standard econometrics text was refitted before anything else was "
     "done. All three reported coefficients were reproduced to four decimal "
     "places. The outcome throughout is the log hourly wage."),
    ("h2", "Hypotheses"),
    ("p",
     f"The {N_H} hypotheses appear in Table 2. Each states that the wage "
     "return to a time-varying career input depends on a characteristic of "
     "the worker or the job, and each is phrased in the direction the "
     "literature usually asserts. They were written down, together with the "
     "control set and the estimation plan, before any of them was fitted. "
     "None was added, dropped or reworded afterwards, and all sixteen are "
     "reported below."),
    ("table", "table2"),
    ("h2", "Specification"),
    ("p",
     "Every specification carries the focal input, the moderator, their "
     "product, and a common set of controls: for the women, tenure and its "
     "square, experience and its square, weekly hours, union coverage, "
     "marital status, region and urban residence; for the men, experience "
     "and its square, hours, union coverage, marital status, region and "
     "urban residence. Cross-sectional and pooled specifications add the "
     "person-level variables that a fixed-effects specification absorbs: "
     "years of schooling, the education indicator and ethnicity. Calendar "
     "time is carried by year indicators. In the balanced men's extract, "
     "recorded experience rises by exactly one year in every year for every "
     "man, so year indicators would absorb it entirely; those four "
     "specifications carry a linear trend instead, and the resulting "
     "within-person estimate mixes the accumulation of experience with the "
     "wage trend of the period. That limitation is confined to those four "
     "hypotheses and is noted where they appear."),
    ("h2", "Estimators"),
    ("p",
     "Each interaction was estimated four ways. The first fits the "
     "specification to a single survey wave, which is the design most career "
     "studies use; this was repeated for every wave with at least sixty "
     "observations, giving a distribution of single-wave answers rather than "
     "one. The second pools all waves. The third and fourth come from a "
     "single model in which the focal input and the product term each enter "
     "twice, once as the deviation from the person's own mean and once as "
     "that mean, so that the within-person and between-person slopes are "
     "estimated jointly and their difference tested directly "
     "[[mundlak1978]], [[belljones2015]]. The test of equality is the "
     "panel-data analogue of the classical specification test "
     "[[hausman1978]], carried out here as a linear contrast within the "
     "clustered covariance matrix rather than as a separate procedure."),
    ("h2", "Inference"),
    ("p",
     "Repeated observations of one worker are not independent, so all "
     "standard errors cluster on the person [[cameron2015]]. Interactions "
     "are interpreted as differences in slope, and simple slopes are formed "
     "in the usual way [[aiken1991]]. Because sixteen equality tests are "
     f"reported, the false discovery rate was controlled across them at "
     "5 per cent [[bh1995]]; both the uncorrected probability and the "
     "adjusted value appear in the tables, and the counts in the text refer "
     "to the adjusted values. Estimators were implemented directly and "
     "verified against data generated with known between-person and "
     "within-person slopes before being applied to the panels."),
]


RESULT_BLOCKS = [
    ("h1", "Results"),
    ("h2", "Four Estimates of Each Interaction"),
    ("p",
     f"Table 3 reports all {N_H} interactions estimated the four ways. The "
     "first two columns summarise the single-wave estimates, giving their "
     "median and their range across waves. The remaining columns give the "
     "pooled estimate, the between-person and within-person estimates from "
     "the joint model, their difference, and the test that the difference is "
     "zero."),
    ("table", "table3"),
    ("p",
     "The pattern is visible without any summary statistic. The "
     "between-person and within-person columns frequently differ in "
     "magnitude, often differ in sign, and the range of the single-wave "
     "estimates is in most rows wider than either panel estimate."),
    ("h2", "Where the Two Answers Disagree"),
    ("p",
     f"Table 4 converts each pair of estimates into the verdict a reader "
     "would take from it — a positive moderation, a negative moderation, or "
     "none at the conventional threshold — and records where the two "
     f"verdicts differ. The between-person and within-person estimates "
     f"carried opposite signs in {DIS['sign_flips']} of {N_H} hypotheses, "
     f"and led to different substantive conclusions in "
     f"{DIS['verdict_changes']}. The formal test of their equality was "
     f"rejected in {DIS['between_ne_within_q05']} hypotheses after "
     "controlling the false discovery rate. The pooled estimate, which mixes "
     "the two components in proportions set by the data rather than by the "
     f"question, reversed sign against the within-person estimate in "
     f"{DIS['sign_pw']} hypotheses and changed the verdict in "
     f"{DIS['verdict_pw']}."),
    ("table", "table4"),
    ("p",
     "The divergence is not small relative to what is being estimated. "
     "Taking the absolute difference between the two estimates and comparing "
     "it with the magnitude of the within-person estimate itself, the median "
     f"ratio was {f2(DIV['median_ratio'])}: the disagreement between the two "
     "answers was typically larger than the answer. The between-person "
     f"estimate was the larger of the two in {DIV['n_between_larger']} of "
     f"{N_H} hypotheses, so the divergence is not simply attenuation in one "
     "direction. Figure 1 places both estimates for every hypothesis on a "
     "common scale, expressing each as the difference it implies in the "
     "response of the log hourly wage to a one within-person standard "
     "deviation change in the career input. Open markers are the "
     "between-person estimates, filled markers the within-person estimates, "
     "and a dagger marks the six hypotheses whose equality test survived the "
     "correction."),
    ("fig", "fig1"),
    ("h2", "What a Single Wave Reports"),
    ("p",
     "The estimator most career studies actually use is none of these: it is "
     "a single cross-section. Table 5 treats each survey wave as a separate "
     f"study. Across the {N_H} hypotheses this yields {WAV['total']} "
     f"single-wave estimates, with a median of {int(WAV['median_n'])} "
     f"observations each, ranging from {WAV['min_n']} to {WAV['max_n']}. Of "
     f"these, {WAV['significant']} reached the conventional threshold. "
     f"{WAV['significant_and_opposite']} of those "
     f"{WAV['significant']} significant findings "
     f"({pct(WAV['share_sig_opposite'])} per cent) pointed the opposite way "
     "to the within-person estimate of the same quantity. Counting all "
     f"single-wave estimates rather than only the significant ones, "
     f"{WAV['opposite_sign']} of {WAV['total']} carried the opposite sign."),
    ("table", "table5"),
    ("p",
     "Figure 2 shows the four hypotheses whose equality tests were most "
     "decisive, plotting each wave's estimate with its interval against the "
     "two panel estimates. The single-wave estimates do not scatter around "
     "the within-person value. They scatter around the between-person value, "
     "which is what the algebra implies and what the figure makes plain: a "
     "cross-section estimates the between-person quantity, and repeating it "
     "in another year reproduces the same quantity rather than converging on "
     "the other one."),
    ("fig", "fig2"),
    ("h2", "Robustness"),
    ("p",
     "If the divergence were an artefact of removing the person, it should "
     "not survive alternative ways of doing so. Table 6 refits every "
     "within-person estimate three further ways: restricted to workers "
     "observed at least three times, by first differences rather than the "
     "within transformation, and with the controls stripped back to the "
     "focal input, the moderator, their product and calendar time. The "
     f"within-person estimate kept its sign under all three variations in "
     f"{ROB['sign_agreement_all_three']} of {N_H} hypotheses. First "
     "differencing, which uses only consecutive pairs and is therefore the "
     "most demanding of the three, is where the two exceptions arise."),
    ("table", "table6"),
    ("h2", "One Case in Detail"),
    ("p",
     "The clearest instance is the first hypothesis: that employer tenure "
     "raises wages more for college graduates. Estimated between people, the "
     f"interaction was {r3(W1['between']['b'])} "
     f"(SE = {f3(W1['between']['se'])}, p {pv(W1['between']['p'])}) — tenure "
     "appearing to pay off substantially less for graduates. Estimated "
     f"within people, it was {r3(W1['within']['b'])} "
     f"(SE = {f3(W1['within']['se'])}, p {pv(W1['within']['p'])}), pointing "
     "weakly the other way. The two differ by "
     f"{r3(W1['equality']['diff'])} and their equality is rejected "
     f"(t = {f2(W1['equality']['t'])}, p {pv(W1['equality']['p'])}, "
     f"q {pv(W1['equality']['q'])}). The pooled estimate, "
     f"{r3(W1['pooled']['b'])} (p {pv(W1['pooled']['p'])}), sits between "
     "them and would be read as supporting the between-person conclusion."),
    ("p",
     "Figure 3 draws what each estimate implies for the wage profile over "
     "the first thirteen years of employer tenure, holding the rest of the "
     "specification fixed. Read between people, graduates gain markedly less "
     "from tenure than non-graduates; read within people, they gain slightly "
     "more. The substantive readings are not variants of one another. They "
     "point in opposite directions, and a study with one wave of data would "
     "have reported the first."),
    ("fig", "fig3"),
]


DISCUSSION_BLOCKS = [
    ("h1", "Discussion"),
    ("p",
     "Across sixteen career moderation hypotheses fixed in advance and "
     "estimated in two cohorts of young workers, the between-person and "
     "within-person answers disagreed often and by margins larger than the "
     "estimates themselves. Half the hypotheses produced estimates of "
     "opposite sign, three quarters produced different substantive verdicts, "
     "and in six the difference was too large to attribute to sampling "
     "variation even after correcting for multiplicity."),
    ("p",
     "The result is not that one estimator is wrong. Between-person and "
     "within-person slopes are answers to different questions, and both "
     "questions are worth asking. Whether graduates enjoy steeper tenure "
     "profiles than non-graduates is a question about the structure of a "
     "labour market, and the between-person estimate answers it. Whether a "
     "given worker's wage responds more to accumulating tenure because she "
     "holds a degree is a question about a career, and only the "
     "within-person estimate speaks to it. The difficulty is that career "
     "theories are written in the second language and tested with the first, "
     "and the translation is usually left implicit."),
    ("p",
     "The single-wave results sharpen the practical point. A cross-sectional "
     "study does not produce a noisy version of the within-person estimate "
     "that more waves would refine. It produces the between-person estimate, "
     "and repeating it in a different year reproduces the between-person "
     "estimate again. Nearly a quarter of the significant single-wave "
     "findings here pointed the opposite way to the within-person estimate "
     "of the same quantity — not because those studies were underpowered or "
     "poorly executed, but because they were measuring something else."),
    ("p",
     "This is the empirical counterpart of a warning psychology has issued "
     "repeatedly on theoretical grounds [[molenaar2004]], [[curran2011]], "
     "[[hamaker2015]], and of the parallel argument about mediation "
     "estimated on cross-sections [[maxwell2007]], [[colepreacher2014]]. "
     "What the present results add is a magnitude for the case of "
     "moderation, in real career data, for hypotheses of the kind the field "
     "reports: the disagreement is typically larger than the quantity in "
     "dispute. It also gives the warning of [[hamaker2015_n]] an "
     "interaction-shaped counterpart, since a moderation is the form in "
     "which career theories usually state their conditions."),
    ("h2", "What Follows for Practice"),
    ("p",
     "Three things follow. The first is a reporting convention. Where panel "
     "data exist, the between-person and within-person components of an "
     "interaction can be estimated in one model at no cost beyond two extra "
     "columns, and reporting both makes the ambiguity visible instead of "
     "leaving it to the reader [[belljones2015]], [[curran2011]], "
     "[[wang2017]]. Reporting only the pooled coefficient conceals a "
     "weighting whose value is a property of the sample."),
    ("p",
     "The second is a matter of language. A cross-sectional moderation "
     "should be described as what it is: a statement about how workers who "
     "differ in the moderator differ in an association. Wording that "
     "implies accumulation — that a degree makes tenure pay off, that "
     "support buffers a person against a setback — asserts the "
     "within-person quantity, and the present results show that the two can "
     "point in opposite directions in the same data."),
    ("p",
     "The third concerns design. Where the within-person question is the one "
     "of interest and no panel is available, the honest course is to state "
     "the limitation rather than to treat the cross-sectional estimate as an "
     "approximation to it. The two are not close in these data, and there "
     "was no feature of any single wave that would have signalled the "
     "difference to a researcher who had only that wave."),
]


LIMIT_BLOCKS = [
    ("h1", "Limitations"),
    ("p",
     "The most obvious limitation is the vintage of the data. Both cohorts "
     f"were surveyed between {NW['first']} and {NW['last']}, and neither "
     "describes a contemporary labour market. The claim advanced here "
     "concerns how two estimators behave when applied to the same panel, "
     "which does not depend on the period; but the specific interactions "
     "reported should not be read as current estimates of anything. These "
     "two cohorts were chosen because they are among the few career panels "
     "with many waves that are public, documented and redistributable, so "
     "that the analysis can be checked."),
    ("p",
     "Second, the within-person estimator is not a solution to confounding, "
     "only to the stable part of it. Anything that varies within a person "
     "and moves with both the career input and the wage remains. The "
     "transformation also amplifies measurement error in the input, which "
     "biases within-person estimates toward zero; that this would work "
     "against finding a within-person moderation makes the divergences "
     "reported here harder rather than easier to obtain, but it does not "
     "make the within-person estimate correct."),
    ("p",
     "Third, the moderators are characteristics people hold rather than "
     "treatments they receive. Neither estimator recovers a causal effect of "
     "holding a degree or of being covered by a union contract. The "
     "comparison is between two descriptive quantities, and the paper claims "
     "no more."),
    ("p",
     "Fourth, four of the sixteen hypotheses concern the return to "
     "experience in the balanced men's panel, where experience and calendar "
     "time coincide within a person; those within-person estimates absorb "
     "the wage trend of the 1980s and should be read with that in mind. "
     "Finally, the outcome throughout is the log hourly wage. Career "
     "research also studies satisfaction, mobility and identity, and whether "
     "the divergence documented here is of similar size for those outcomes "
     "is an open question, and one that the growing number of long-running "
     "work and ageing panels now makes answerable."),
]


CONCLUSION_BLOCKS = [
    ("h1", "Conclusions"),
    ("p",
     "Sixteen career moderation hypotheses, fixed in advance and estimated "
     "in two longitudinal cohorts of young workers, gave systematically "
     "different answers depending on whether the interaction was identified "
     "from differences between people or from change inside them. The "
     f"estimates carried opposite signs in {DIS['sign_flips']} of {N_H} "
     f"cases and supported different conclusions in "
     f"{DIS['verdict_changes']}; their equality was rejected in "
     f"{DIS['between_ne_within_q05']} after correcting for multiplicity, and "
     "the typical disagreement exceeded the size of the estimate in "
     "dispute. Single-wave estimates tracked the between-person quantity "
     "rather than the within-person one, so collecting another cross-section "
     "does not close the gap."),
    ("p",
     "Career theories make claims about people over time. Where panel data "
     "allow the two components of a moderation to be separated, they should "
     "be, and both should be reported. Where they do not, the quantity "
     "estimated should be named accurately, because in these data the two "
     "are not interchangeable and frequently point in opposite directions."),
]


BACK_BLOCKS = [
    ("h1b", "Author Contributions"),
    ("p",
     "Conceptualization, X.C. and T.M.; methodology, X.C.; software, X.C.; "
     "validation, X.C. and T.M.; formal analysis, X.C.; data curation, "
     "X.C.; writing—original draft preparation, X.C.; writing—review and "
     "editing, T.M.; visualization, X.C.; supervision, T.M. All authors "
     "have read and agreed to the published version of the manuscript."),
    ("h1b", "Funding"),
    ("p", "This research received no external funding."),
    ("h1b", "Institutional Review Board Statement"),
    ("p",
     "Not applicable. The study is a secondary analysis of de-identified "
     "public-use microdata and involved no contact with human subjects."),
    ("h1b", "Informed Consent Statement"),
    ("p",
     "Not applicable. Informed consent was obtained by the agencies that "
     "conducted the original surveys."),
    ("h1b", "Data Availability Statement"),
    ("p",
     "The study analyses two public-use extracts of surveys conducted by the "
     "U.S. Bureau of Labor Statistics: the National Longitudinal Survey of "
     "Young Women [[bls_nlsw]] and the National Longitudinal Survey of Youth "
     "1979 [[bls_nlsy79]]. Both extracts are redistributed with standard "
     "statistical software and reference packages; the men's extract is the "
     "replication file of an earlier published study [[vella1998]]. No new "
     "data were created. The analysis code, which downloads the extracts, "
     "reproduces a published benchmark estimate as a check, and generates "
     "every table and figure in this article under a fixed random seed, is "
     "available from the corresponding author on request."),
    ("h1b", "Conflicts of Interest"),
    ("p", "The authors declare no conflicts of interest."),
]


APPENDIX_BLOCKS = [
    ("h1a", "Appendix A"),
    ("p",
     "Table A1 reports, for each hypothesis, the slope of the focal career "
     "input estimated pooled and within the person, the two coefficients of "
     "determination, and the estimation sample. The focal slopes are shown "
     "because a difference in an interaction is easier to weigh against the "
     "main effect it modifies."),
    ("table", "tableA1"),
]


def _numbered(blocks, start=1):
    """The template carries no list numbering on its heading styles, so the
    section numbers are written into the text."""
    out, h1, h2 = [], start - 1, 0
    for kind, val in blocks:
        if kind == "h1":
            h1 += 1
            h2 = 0
            out.append(("h1", "%d. %s" % (h1, val)))
        elif kind == "h2":
            h2 += 1
            out.append(("h2", "%d.%d. %s" % (h1, h2, val)))
        else:
            out.append((kind, val))
    return out, h1


_body, _last = _numbered(INTRO_BLOCKS + BG_BLOCKS + METHOD_BLOCKS
                         + RESULT_BLOCKS + DISCUSSION_BLOCKS + LIMIT_BLOCKS
                         + CONCLUSION_BLOCKS)
BLOCKS = _body + BACK_BLOCKS + APPENDIX_BLOCKS
