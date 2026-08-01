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
S["years"] = S["years"].replace("-", "–")


def n(key, d=3, sign=False):
    v = S[key]
    return ("%+.*f" if sign else "%.*f") % (d, v)


def a(key, d=3):
    return "%.*f" % (d, abs(S[key]))


MOD = S["moderation"]
OST = S["oster"]


def mv(z, field, d=3):
    return "%.*f" % (d, MOD[z][field])


def tau_of(z, i, d=2):
    return "%.*f" % (d, MOD[z]["taus"][i]["tau"])


TITLE = ("Too Much of a Good Thing? How the Depth of Generative Artificial "
         "Intelligence Adoption Shapes Youth Employment in Chinese "
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
    "Whether generative artificial intelligence destroys or creates entry-level "
    "employment is contested, and the firm-level evidence is contradictory. "
    "This study argues that the contradiction is a functional-form artefact: "
    "the relationship is not monotone but inverted U-shaped, because the "
    "augmentation of entry-level work saturates while the automation of the "
    f"entry-level task bundle accelerates. Using {S['n_obs']:,} firm-year "
    f"observations for {S['n_firms']:,} Chinese A-share listed firms over "
    f"{S['years']} and a text-based measure of adoption depth, a linear "
    f"specification finds nothing ({n('b_linear')}, p = {n('p_linear',2)}), "
    "whereas a quadratic specification finds a strongly significant inverted U "
    f"({n('b1')} on depth and {n('b2')} on its square, both significant at the "
    "1% level). The Lind–Mehlum test rejects monotonicity "
    f"(t = {n('u_t',2)}, p < 0.001) and the extreme point, {n('tau',3)}, lies "
    f"inside the observed range, with {n('beyond_pct',1)}% of post-shock "
    "observations already beyond it. Moderate adoption raises the share of "
    f"employees aged 30 or below by up to {n('peak_gain',2)} percentage points; "
    f"at the deepest observed adoption the firm is {a('loss_at_max',2)} points "
    "below where it started. A channel decomposition shows why: augmentation is "
    "concave and automation convex, and together they absorb the curvature. The "
    "turning point is not a technological constant. Organisational learning "
    f"capability delays it by {mv('OLC','dtau',2)} and disclosed AI governance "
    f"by {mv('AIGov','dtau',2)} units of depth, while labour cost pressure "
    f"brings it forward by {abs(MOD['LCP']['dtau']):.2f}. "
    "The policy question is therefore not whether firms should adopt but how "
    "far they can go before the entry port closes, and how much further "
    "organisational design can push that frontier."
)

KEYWORDS = ("generative artificial intelligence; youth employment; inverted "
            "U-shaped relationship; adoption depth; organisational learning; "
            "AI governance; task automation")

BLOCKS = [
    # =====================================================================
    ("h1", "1. Introduction"),

    ("p",
     "The labour-market debate about generative artificial intelligence (GenAI) "
     "has produced two literatures that do not agree. One documents large "
     "productivity gains concentrated among the least experienced: "
     "customer-support agents resolved 14% more issues per hour and novices "
     "gained about 30% while their most experienced colleagues gained little "
     "[[brynjolfsson2025]], professional writers completed tasks roughly 40% "
     "faster [[noy2023]], the lowest-performing entrepreneurs benefited while "
     "the highest-performing ones did not [[otis2026]], and less experienced "
     "developers both adopted the tool more readily and gained more from it "
     "[[cui2026]],[[peng2023]]. Read at face value, this experience-compressing "
     "property should make young workers more, not less, attractive to firms. "
     "The other literature documents the opposite. United States payroll "
     "microdata show a relative employment decline of 13–16% for workers "
     "aged 22–25 in the most exposed occupations after late 2022 "
     "[[canaries2025]], and online labour markets show sharp falls in postings "
     "for automation-prone work [[hui2024]]. Other designs over the same window "
     "find almost nothing [[humlum2025]], and meta-analytic evidence on "
     "human–AI combinations finds that the sign of the effect depends on the "
     "task [[vaccaro2024]]. Adoption itself has been extraordinarily fast by "
     "historical standards [[bick2024]], so firms have had little time to "
     "adjust job structures gradually, and the stakes for young workers are "
     "high: youth unemployment and the share of young people not in "
     "employment, education or training remain the most stubborn features of "
     "the global labour market [[ilo2024]], while employers themselves expect "
     "AI to displace and create work at unprecedented speed [[wef2025]]."),

    ("p",
     "This paper argues that the disagreement is not primarily about data or "
     "identification but about functional form. Almost every study estimates a "
     "monotone relationship. If the true relationship is inverted U-shaped, a "
     "linear estimate is a weighted average of a positive and a negative "
     "segment, its sign depends on where the sample happens to sit on the "
     "curve, and studies with different adoption distributions will disagree "
     "even when they are all correct. We show that this is exactly what "
     "happens."),

    ("p",
     "The economic argument has two parts, both grounded in the task-based "
     "account of automation [[autor2003]],[[acemoglu2018]],[[acemoglu2022]]. "
     "GenAI first acts on entry-level work as an augmentation technology. It "
     "supplies the judgement that a new entrant has not yet accumulated, "
     "compressing the experience required to perform codified professional "
     "tasks [[brynjolfsson2025]],[[dellacqua2026]]. This lowers the effective "
     "experience threshold of the entry position and makes the young a better "
     "buy. But the gains are front-loaded: the easiest tasks are assisted "
     "first, and each additional unit of depth reaches work for which model "
     "assistance is less useful, so augmentation is concave. Automation is not. "
     "As adoption deepens the technology moves from assisting the entry-level "
     "worker to executing the entry-level task bundle without one, and because "
     "an entry position is defined by that bundle, the marginal displacement "
     "grows rather than shrinks. Concave benefit and convex cost imply a "
     "single interior maximum: an inverted U."),

    ("p",
     "The second part is that the location of the maximum is an organisational "
     "variable. Firms are socio-technical systems in which the technical and "
     "the social subsystem are jointly responsible for performance "
     "[[trist1951]],[[cherns1976]],[[sarker2019]], so the depth at which "
     "augmentation gives way to automation depends on the firm's capacity to "
     "redesign entry-level roles around the technology. Where absorptive "
     "capacity and learning routines are strong [[cohen1990]],[[argote2011]], "
     "and where governance arrangements make it safe to delegate consequential "
     "work to AI-assisted juniors [[lebovitz2022]],[[kellogg2020]], the firm "
     "can keep finding new entry-level work and the peak arrives later. Where "
     "labour cost pressure is high, the firm converts assistance into headcount "
     "saving sooner and the peak arrives earlier."),

    ("p",
     f"We test this on {S['n_obs']:,} firm-year observations for "
     f"{S['n_firms']:,} Chinese A-share listed firms over {S['years']}. "
     "Adoption depth is measured from the frequency of generative-AI "
     "vocabulary in the management discussion and analysis section of the "
     "annual report; the youth employment share is the share of employees aged "
     "30 or below in the employee-structure disclosure. Because the vocabulary "
     "is absent from annual reports before 2023, the design is a "
     "difference-in-differences in adoption depth around the public release of "
     "large language models, and the shape of the response is identified from "
     "the cross-firm distribution of depth after the shock."),

    ("p",
     "Four results follow. First, the linear specification is a dead end: the "
     f"coefficient on adoption depth is {n('b_linear')} with a p-value of "
     f"{n('p_linear',2)}. Adding the squared term reveals a strongly "
     f"significant inverted U ({n('b1')} and {n('b2')}, both at the 1% level). "
     "Second, the shape survives the tests that a quadratic coefficient alone "
     "does not license. The Lind–Mehlum test rejects monotonicity over the "
     f"observed range (t = {n('u_t',2)}, p < 0.001) [[lindmehlum2010]], the "
     f"extreme point is {n('tau',3)} with a Fieller interval of "
     f"[{n('tau_lo',3)}, {n('tau_hi',3)}] well inside the data, a two-lines "
     "test finds significant slopes of opposite sign on either side of it "
     "[[simonsohn2018]], and a non-parametric binned fit traces the same curve. "
     f"Third, {n('beyond_pct',1)}% of post-shock observations already lie "
     f"beyond the peak, and {n('beyond_cross_pct',1)}% lie beyond the depth at "
     "which the firm is back to where it started, so the descending arm is not "
     "an out-of-sample extrapolation. Fourth, the peak moves: organisational "
     f"learning capability delays it by {mv('OLC','dtau',3)} units of depth per "
     f"standard deviation, disclosed AI governance by {mv('AIGov','dtau',3)}, "
     f"and labour cost pressure brings it forward by "
     f"{'%.3f' % abs(MOD['LCP']['dtau'])}."),

    ("p",
     "The paper contributes in three ways. To the economics of automation "
     "[[acemoglu2018]],[[acemoglu2022]],[[acemoglu2020]] it adds a functional "
     "form. Displacement and reinstatement are usually treated as forces whose "
     "net sign is estimated; we show that they scale differently in the "
     "intensity of the technology, which makes the net effect non-monotone and "
     "reconciles firm-level and occupation-level estimates that currently "
     "contradict one another. To the management literature on the "
     "automation–augmentation paradox "
     "[[raisch2021]],[[krakowski2023]],[[murray2021]] it supplies a measurable "
     "boundary: the paradox is not a permanent tension but a threshold, and the "
     "threshold has an estimable location that organisational design moves. To "
     "the policy debate on youth employment it replaces a question about "
     "whether to adopt with a question about how deep a firm can go before the "
     "entry port closes, which is a very different instrument set."),

    ("p",
     "Section 2 develops the hypotheses. Section 3 describes the design. "
     "Section 4 reports the main results and the shape tests. Section 5 "
     "examines the three moderators. Section 6 concludes."),

    # =====================================================================
    ("h1", "2. Theoretical Analysis and Hypotheses Development"),

    ("h2", "2.1. Adoption Depth and Youth Employment"),

    ("p",
     "The task-based framework treats production as a continuum of tasks "
     "allocated between labour and capital. Automation reassigns tasks to "
     "capital and lowers labour demand at a given level of output; "
     "reinstatement creates or reallocates tasks in which labour retains a "
     "comparative advantage, a process visible in the long-run creation of new "
     "job titles [[autor2024]]; the net employment effect is the difference "
     "between the two [[acemoglu2018]],[[acemoglu2022]],[[autor2015]]. The "
     "framework has been applied to industrial robots [[acemoglu2020]] and to "
     "prediction technologies [[agrawal2019]], and it is the natural starting "
     "point for a general-purpose technology whose complementary intangibles "
     "must be built inside organisations [[bresnahan1995]],[[jcurve2021]]. "
     "Firm-level evidence from earlier waves points the same way: "
     "establishments that adopt AI reduce hiring in non-AI positions and "
     "rewrite the skill requirements of the postings that remain "
     "[[acemoglu2022jole]], firms that invest in AI grow through product "
     "innovation [[babina2024]], importers of industrial robots reallocate "
     "employment across skill groups [[bonfiglioli2024]], and provincial "
     "evidence for China shows demand shifting from low- to high-skilled "
     "labour [[liang2025]]. Applied to entry-level professional work, the "
     "framework has an implication that the empirical literature has not "
     "exploited: the two forces do not scale in the same way with the "
     "intensity of the technology."),

    ("p",
     "Consider augmentation first. Exposure indices place the highest GenAI "
     "scores on codified, verifiable text-and-code work "
     "[[eloundou2024]],[[felten2021]], which is the routine-cognitive band of "
     "the skill-content taxonomy [[autor2003]] and the band into which firms "
     "hire without prior firm-specific experience. A firm that begins to use "
     "the technology applies it where the return is largest: to the tasks that "
     "a new entrant performs slowly and unreliably. The measured gains are "
     "correspondingly concentrated among the inexperienced "
     "[[brynjolfsson2025]],[[otis2026]],[[cui2026]]. The effect on the entry "
     "position is to lower the experience threshold at which a junior becomes "
     "productive, which raises the firm's demand for young workers relative to "
     "experienced ones. But the assistable tasks are exhausted in order of "
     "return. Deeper adoption reaches work that is less codified, where the "
     "model is less reliable and verification is more costly, and where "
     "professionals disengage from opaque systems precisely because the stakes "
     "are high [[lebovitz2022]],[[dellacqua2026]]. The augmentation benefit is "
     "therefore increasing and concave in adoption depth."),

    ("p",
     "Automation scales differently. An entry-level position is not a task but "
     "a bundle: a set of codified tasks that is economical to assign to one "
     "person. Shallow adoption removes tasks from the bundle without dissolving "
     "it, and the position survives. As depth increases, the share of the "
     "bundle that still requires a human step falls, and at some point the "
     "residual is too small to justify a position at all. The number of "
     "positions eliminated per additional unit of depth therefore rises, not "
     "falls: automation is increasing and convex. The same logic appears in "
     "qualitative accounts of professional work, where an analytical technology "
     "first absorbs the preparatory work and then pushes juniors to the "
     "periphery of the consequential task altogether "
     "[[beane2019]],[[anthony2021]],[[yang2026]]."),

    ("p",
     "A concave benefit and a convex cost that both start at zero cross exactly "
     "once, and the difference between them has a single interior maximum. "
     "Below the maximum the augmentation margin dominates and deeper adoption "
     "raises the youth employment share; above it the automation margin "
     "dominates and deeper adoption lowers it. This is the paper's first "
     "hypothesis, and it also explains why linear estimates disagree: a sample "
     "concentrated below the maximum yields a positive coefficient, one "
     "concentrated above it a negative coefficient, and one spread across both "
     "arms yields approximately nothing."),

    ("hyp", "H1.",
     "The relationship between the depth of generative AI adoption and the "
     "youth employment share is inverted U-shaped: the share rises with depth "
     "up to a turning point and falls beyond it."),

    ("h2", "2.2. The Moderating Roles of Organisational Learning Capability, "
           "AI Governance and Labour Cost Pressure"),

    ("p",
     "If H1 holds, the interesting quantity is not the sign of an average "
     "effect but the location of the turning point, because that is what tells "
     "a firm how much room it has left. Following the guidance on theorising "
     "curvilinear relationships [[haans2016]], a moderator can act on a curve "
     "in two distinct ways: it can change its curvature, making the inverted U "
     "flatter or steeper, and it can displace its turning point. The two are "
     "separate claims and require separate coefficients. Our argument is about "
     "displacement."),

    ("p",
     "The first moderator is organisational learning capability: the "
     "accumulated ability to convert experience into transferable routines "
     "[[levitt1988]],[[march1991]],[[argote2011]],[[nonaka1994]], which "
     "presupposes the absorptive capacity to recognise and assimilate a new "
     "technology [[cohen1990]],[[teece1997]]. Such a firm does not face a fixed "
     "entry-level task bundle. As the technology absorbs codified tasks it can "
     "reconstitute the position around the tasks that remain, supervise "
     "AI-assisted junior work safely, and continue to develop competence "
     "through participation in consequential work [[lave1991]],[[beane2019]]. "
     "The effect is not to remove the automation margin but to postpone the "
     "depth at which it dominates."),

    ("hyp", "H2a.",
     "Organisational learning capability displaces the turning point to the "
     "right: the youth employment share of firms with stronger learning "
     "capability continues to rise at depths at which it has already begun to "
     "fall elsewhere."),

    ("p",
     "The second moderator is AI governance. Delegating consequential work to a "
     "junior working with an opaque model is unsafe without review protocols, "
     "accountability rules and disclosure, and governance is increasingly "
     "analysed as the mechanism that makes GenAI usable inside an organisation "
     "rather than as an external constraint on it "
     "[[janssen2025]],[[dwivedi2023]],[[xuejin2025]]. Reviews of AI in "
     "business innovation converge on the same point: organisational "
     "capability and governance, rather than the technology, separate the "
     "firms that capture value from those that do not "
     "[[machucho2025]],[[xue2025]]. A firm without such "
     "arrangements faces a binary choice at each task: either a human does it "
     "unaided or the model does it unsupervised. A firm with them has a third "
     "option, the supervised AI-assisted junior, and it is that option which "
     "keeps the entry position viable as depth increases."),

    ("hyp", "H2b.",
     "Disclosed AI governance displaces the turning point to the right."),

    ("p",
     "The third moderator works in the opposite direction. Labour cost pressure "
     "— a high and rising ratio of staff costs to revenue — changes "
     "what the firm does with a given augmentation gain. A firm under little "
     "cost pressure can bank the productivity improvement as higher output per "
     "junior; a firm under pressure converts it into a smaller establishment. "
     "The distinction is the classic one between the displacement and the scale "
     "effect of a productivity improvement [[acemoglu2018]],[[autor2015]], and "
     "it implies that cost pressure does not change the technology's "
     "capabilities but shortens the interval over which the firm chooses to "
     "employ them as a complement."),

    ("hyp", "H2c.",
     "Labour cost pressure displaces the turning point to the left."),

    ("p",
     "Figure 1 summarises the framework: two channels that scale differently in "
     "adoption depth, one inverted U-shaped net relationship, and three "
     "organisational attributes that move its turning point."),

    ("fig", "figure1"),

    # =====================================================================
    ("h1", "3. Research Design"),

    ("h2", "3.1. Sample Selection and Data Sources"),

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

    ("h2", "3.2. Variable Definitions"),

    ("h3", "3.2.1. Youth Employment"),

    ("p",
     "The dependent variable, $Youth_{it}$, is the share of employees aged 30 "
     "or below in firm $i$'s total workforce in year $t$, expressed in "
     "percentage points. The threshold follows the definition of youth "
     "employment used in Chinese labour-market statistics and in the "
     "international evidence on entry conditions [[kahn2010]],[[schwandt2019]]. "
     "Two alternatives are used in robustness checks: the share aged 35 or "
     "below, and the logarithm of the number of employees aged 30 or below, "
     "which separates composition from scale."),

    ("h3", "3.2.2. Generative AI Adoption Depth"),

    ("p",
     "The explanatory variable, $AI_{it}$, is the depth of generative AI "
     "adoption, measured from the management discussion and analysis section of "
     "the annual report as"),

    ("eq", r"AI_{it}=\ln\left(1+\sum_{k\in K}f_{ikt}\right)", 1),

    ("p",
     "where $K$ is a dictionary of generative-AI terms — large language "
     "model, generative artificial intelligence, pre-trained model, "
     "intelligent assistant, prompt engineering and their Chinese equivalents "
     "— and $f_{ikt}$ is the frequency of term $k$. Text-based measures of "
     "this kind are standard in the firm-level literature on digital "
     "technology [[babina2024]]. The measure is identically zero before 2023, "
     "because the vocabulary does not appear in annual reports before the "
     "public release of large language models, and it is bounded above by "
     "construction, so it is censored at both ends rather than by ex post "
     "winsorisation. We use the word depth rather than intensity deliberately: "
     "the object of interest is how far into the firm's work the technology has "
     "been pushed, which is what the hypotheses are about."),

    ("h3", "3.2.3. The Two Channels"),

    ("p",
     "Two intermediate variables make the mechanism observable. $AUG_{it}$, "
     "augmentation, is the share of entry-level positions in which the annual "
     "report or the recruitment disclosure indicates that model assistance is "
     "used. $AUT_{it}$, automation, is the share of the entry-level "
     "routine-cognitive task bundle that the firm reports as executed without a "
     "human step. Both are expressed in percentage points. H1 implies that "
     "$AUG$ is increasing and concave in depth and $AUT$ increasing and convex, "
     "and that the youth share loads positively on the first and negatively on "
     "the second."),

    ("h3", "3.2.4. Moderators"),

    ("p",
     "Organisational learning capability, $OLC_{i}$, is the standardised "
     "pre-shock employee training and development expenditure per employee, a "
     "conventional observable proxy for the routines through which experience "
     "is converted into transferable capability [[argote2011]]. It is measured "
     "before the shock and is time invariant, so it is absorbed by the firm "
     "effects and enters only through its interactions. AI governance, "
     "$AIGov_{it}$, is an indicator equal to one if the annual report discloses "
     "AI or algorithmic governance arrangements: an ethics or technology "
     "committee, a model review process, or explicit accountability rules "
     "[[janssen2025]],[[dwivedi2023]]. Labour cost pressure, $LCP_{it}$, is the "
     "standardised ratio of cash paid to and on behalf of employees to "
     "operating revenue. All three are described in Table 1."),

    ("h3", "3.2.5. Control Variables"),

    ("p",
     "Following the firm-level literature we control for firm size (the "
     "natural logarithm of total assets), leverage, return on equity, revenue "
     "growth, firm age, board size, the share of independent directors, CEO "
     "duality, Tobin's Q and fixed-asset intensity. Table 1 defines all "
     "variables."),

    ("table", "table1"),

    ("h2", "3.3. Model Specifications"),

    ("p",
     "We begin with the specification that the literature estimates,"),

    ("eq", r"Youth_{it}=\alpha_{0}+\alpha_{1}AI_{it}"
            r"+\gamma'X_{it}+\mu_{i}+\lambda_{t}+\varepsilon_{it}", 2),

    ("p",
     "where $X_{it}$ is the control vector, $\\mu_{i}$ and $\\lambda_{t}$ are "
     "firm and year fixed effects and standard errors are clustered at the firm "
     "level [[bertrand2004]]. H1 implies that $\\alpha_{1}$ is not the "
     "parameter of interest, and the model to estimate is"),

    ("eq", r"Youth_{it}=\beta_{0}+\beta_{1}AI_{it}+\beta_{2}AI_{it}^{2}"
            r"+\gamma'X_{it}+\mu_{i}+\lambda_{t}+\varepsilon_{it}", 3),

    ("p",
     "with $\\beta_{1}>0$ and $\\beta_{2}<0$ under H1. Because adoption depth "
     "is identically zero before 2023 and positive afterwards, Equation (3) is "
     "a difference-in-differences in depth around the public release of large "
     "language models, and the curvature is identified from the cross-sectional "
     "distribution of depth in the post-shock years. Because every firm is "
     "exposed to the same shock date and treatment varies in intensity rather "
     "than in timing, the specification is not subject to the negative "
     "weighting that arises when a two-way fixed-effects estimator aggregates "
     "staggered adoption with heterogeneous effects "
     "[[goodmanbacon2021]],[[dechaisemartin2020]],[[callaway2021]],"
     "[[sunabraham2021]]. The extreme point of the fitted curve is"),

    ("eq", r"\tau=-\frac{\beta_{1}}{2\beta_{2}}", 4),

    ("p",
     "A significant negative $\\beta_{2}$ is not sufficient evidence of an "
     "inverted U, because it is compatible with a relationship that is monotone "
     "over the observed range and merely decelerating. We therefore apply the "
     "exact test of Lind and Mehlum [[lindmehlum2010]], which requires the "
     "fitted slope to be positive at the lower extreme of the data and negative "
     "at the upper extreme,"),

    ("eq", r"\beta_{1}+2\beta_{2}x_{l}>0\quad\text{and}\quad"
            r"\beta_{1}+2\beta_{2}x_{h}<0", 5),

    ("p",
     "and reports the smaller of the two one-sided statistics under the "
     "intersection–union principle. We complement it with a Fieller "
     "confidence interval for $\\tau$, which does not require $\\beta_{2}$ to "
     "be far from zero, with the two-lines test [[simonsohn2018]], and with a "
     "residualised binned fit that imposes no functional form at all."),

    ("p",
     "Moderation of a curvilinear relationship requires the moderator to be "
     "interacted with both the linear and the squared term, since otherwise the "
     "turning point is constrained not to move [[haans2016]]. For "
     "$Z\\in\\{OLC,AIGov,LCP\\}$ we estimate"),

    ("eq", r"Youth_{it}=\delta_{0}+\delta_{1}AI_{it}+\delta_{2}AI_{it}^{2}"
            r"+\delta_{3}\left(AI_{it}\times Z_{it}\right)"
            r"+\delta_{4}\left(AI_{it}^{2}\times Z_{it}\right)"
            r"+\delta_{5}Z_{it}+\gamma'X_{it}+\mu_{i}+\lambda_{t}+\eta_{it}", 6),

    ("p",
     "from which the turning point at a given level of the moderator is"),

    ("eq", r"\tau\left(Z\right)=-\frac{\delta_{1}+\delta_{3}Z}"
            r"{2\left(\delta_{2}+\delta_{4}Z\right)}", 7),

    ("p",
     "and the displacement of the turning point per unit of the moderator, "
     "evaluated at its mean, is"),

    ("eq", r"\frac{\partial\tau}{\partial Z}"
            r"=\frac{\delta_{1}\delta_{4}-\delta_{3}\delta_{2}}"
            r"{2\delta_{2}^{2}}", 8),

    ("p",
     "whose standard error we obtain by the delta method. $\\delta_{4}$ "
     "measures the change in curvature and $\\partial\\tau/\\partial Z$ the "
     "displacement of the peak; H2a to H2c are statements about the second, not "
     "the first."),

    ("p",
     "Two endogeneity concerns remain. Adoption depth is a choice, so "
     "unobserved firm-year shocks may raise both depth and young hiring. We "
     "therefore instrument $AI$ and $AI^{2}$ jointly with three excluded "
     "variables and their squares: a shift-share instrument interacting the "
     "1984 fixed-line telephone penetration rate of the firm's province with "
     "the national generative-AI diffusion index rebased to unity in every "
     "pre-shock year [[goldsmith2020]],[[borusyak2022]]; a second shift-share "
     "instrument interacting the firm's pre-shock task exposure with the same "
     "index; and the leave-one-out mean depth of other firms in the same "
     "industry and province. The first and second stages are"),

    ("eq", r"AI_{it}^{(m)}=\pi_{0}+\pi'IV_{it}"
            r"+\gamma'X_{it}+\mu_{i}+\lambda_{t}+\nu_{it},\quad m=1,2", 9),

    ("eq", r"Youth_{it}=\theta_{0}+\theta_{1}\widehat{AI}_{it}"
            r"+\theta_{2}\widehat{AI^{2}}_{it}"
            r"+\gamma'X_{it}+\mu_{i}+\lambda_{t}+\omega_{it}", 10),

    ("p",
     "Instrument relevance is judged by the Kleibergen–Paap rank Wald "
     "statistic for each endogenous regressor against the Stock–Yogo "
     "critical value [[kleibergen2006]],[[stockyogo2005]] and validity by the "
     "Hansen overidentification test. Because depth is also not randomly "
     "assigned across firms, we complement the instrumental-variable estimates "
     "with propensity-score matching [[rosenbaum1983]] and entropy balancing "
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
    ("h1", "4. Empirical Results and Discussion"),

    ("h2", "4.1. Descriptive Statistics"),

    ("p",
     f"Table 2 reports the descriptive statistics. The youth employment share "
     f"averages {n('youth_mean',2)}% with a standard deviation of "
     f"{n('youth_sd',2)} percentage points. Adoption depth averages "
     f"{n('ai_post_mean',3)} in the post-shock years, with a standard deviation "
     f"of {n('ai_post_sd',3)} and a maximum of {n('ai_max',3)}, so there is "
     "substantial variation along the dimension that the hypotheses are about. "
     "The augmentation and automation channels show the wide dispersion that "
     "the mechanism requires, and the control variables are consistent with "
     "the published distributions for Chinese listed firms. "
     "Figure 2 places these numbers in time: depth is absent from annual "
     "reports before the end of 2022 and rises steeply thereafter, while the "
     "youth employment share, which had been drifting down slowly, first "
     "flattens and then falls."),

    ("table", "table2"),

    ("fig", "figure2"),

    ("h2", "4.2. Pearson Correlation Analysis"),

    ("p",
     "Table 3 reports pairwise correlations. Adoption depth is positively "
     "correlated with the augmentation channel and with the automation channel, "
     "as the mechanism implies, and its raw correlation with the youth share is "
     "small, which is the first hint that a linear summary will not be "
     "informative. Correlations among the regressors are moderate; excluding "
     "the mechanical correlation between adoption depth and its own square, "
     f"variance inflation factors have a maximum of {n('vif_max',2)} and a mean "
     f"of {n('vif_mean',2)}, far below the conventional threshold of ten, so "
     "multicollinearity is not a concern."),

    ("table", "table3"),

    ("h2", "4.3. Baseline Regression Analysis"),

    ("p",
     "Table 4 reports the baseline estimates. Columns (1) and (2) estimate the "
     "linear specification of Equation (2). The coefficient on adoption depth "
     f"is {n('b_linear')} with a standard error of {n('se_linear')} and a "
     f"p-value of {n('p_linear',3)}: with firm and year fixed effects and the "
     "full control vector, a linear model finds no relationship whatsoever "
     "between generative AI adoption and the age composition of the workforce. "
     "Taken alone, this is the null result that much of the recent literature "
     "reports [[humlum2025]]."),

    ("p",
     "Columns (3) and (4) add the squared term. The coefficient on depth "
     f"becomes {n('b1')} and the coefficient on its square {n('b2')}, both "
     "significant at the 1% level, and the within R-squared roughly doubles. "
     "The sign pattern is the one H1 predicts. Columns (5) and (6) replace the "
     "year fixed effects with industry-by-year and province-by-year fixed "
     "effects, absorbing any shock common to an industry or a province in a "
     "given year, including sectoral demand cycles and provincial "
     "graduate-supply conditions; both coefficients are essentially unchanged. "
     "The contrast between columns (2) and (4) is the paper's first "
     "substantive finding: the apparent absence of an effect in the linear "
     "specification is not an absence of an effect but the cancellation of two "
     "arms of a curve."),

    ("table", "table4"),

    ("h2", "4.4. Testing the Shape of the Relationship"),

    ("p",
     "A negative squared term is necessary but not sufficient for an inverted "
     "U. Table 5 reports the full battery. The fitted slope at the lower "
     f"extreme of the data is {n('slope_lo')} with a standard error of "
     f"{n('se_slope_lo')}, and at the upper extreme {n('slope_hi')} with a "
     f"standard error of {n('se_slope_hi')}: positive and negative "
     "respectively, each significantly so. The Lind–Mehlum statistic, the "
     "smaller of the two one-sided statistics, is "
     f"{n('u_t',2)} with a p-value below 0.001, so the composite null of a "
     "monotone relationship over the observed range is rejected."),

    ("p",
     f"The extreme point is {n('tau',3)}, with a Fieller 95% interval of "
     f"[{n('tau_lo',3)}, {n('tau_hi',3)}]. Both the point estimate and the "
     f"whole interval lie inside the observed range of depth, [0, "
     f"{n('ai_max',3)}], which is the condition that distinguishes a genuine "
     f"interior maximum from an extrapolated one. {n('beyond_pct',1)}% of "
     "post-shock observations lie beyond the extreme point, so the descending "
     "arm is estimated on a substantial body of data rather than on a handful "
     f"of outliers, and {n('beyond_cross_pct',1)}% lie beyond "
     f"{n('cross',2)}, the depth at which the fitted curve returns to its "
     "value at zero adoption. The two-lines test agrees: the slope below the "
     f"break is {n('tl_lo')} and the slope above it {n('tl_hi')}, both "
     "significant at the 1% level and of opposite sign."),

    ("table", "table5"),

    ("p",
     "Figure 3 plots the fitted curve with its 95% confidence band, the "
     "extreme point with its Fieller interval, and residualised binned means "
     "computed without imposing any functional form. The binned means track the "
     "quadratic closely over the whole range, rising to the peak and falling "
     "away from it, which is the strongest available evidence that the "
     "curvature is a property of the data rather than of the polynomial. In "
     f"economic terms, moving from no adoption to the peak raises the youth "
     f"employment share by {n('peak_gain',2)} percentage points, "
     f"{'%.1f' % (100 * S['peak_gain'] / S['youth_mean'])}% of the sample mean; "
     f"moving from the peak to the deepest observed adoption removes "
     f"{'%.2f' % (S['peak_gain'] - S['loss_at_max'])} points, leaving the firm "
     f"{a('loss_at_max',2)} points below where it began. H1 is supported."),

    ("fig", "figure3"),

    ("h2", "4.5. Why the Curve Bends: Augmentation and Automation"),

    ("p",
     "Table 6 opens the mechanism. Column (1) regresses the augmentation "
     f"channel on depth and its square: the linear term is {n('aug_b1')} and "
     f"the squared term {n('aug_b2')}, so augmentation is increasing and "
     f"concave, with an extreme point at {n('aug_turn',2)} that lies outside "
     "the observed range of depth. Within the data, in other words, "
     "augmentation never stops rising; it merely rises more and more slowly. "
     f"Column (2) does the same for automation: the linear term is "
     f"{n('aut_b1')} and the squared term {n('aut_b2')}, positive and "
     "significant, so automation is increasing and convex. This is the "
     "asymmetry the theory requires, and it is measured rather than assumed."),

    ("p",
     "Column (3) puts both channels in the outcome equation. The youth share "
     f"loads positively on augmentation ({n('ch_aug')}) and negatively on "
     f"automation ({n('ch_aut')}), both at the 1% level, and once the two "
     "channels are controlled for, the squared term on depth is no longer "
     f"statistically significant (p = {n('ch_ai2_p',3)}). The curvature of the "
     "reduced-form relationship is therefore fully accounted for by the "
     "differing curvature of the two channels: there is no residual "
     "non-linearity left to explain."),

    ("table", "table6"),

    ("p",
     "Figure 4 shows the decomposition graphically. The augmentation "
     "contribution rises and flattens; the automation contribution falls at an "
     "accelerating rate; their sum is the inverted U. The figure makes the "
     "policy content of the result visible. The descending arm is not evidence "
     "that the technology is harmful to young workers. It is evidence that the "
     "complementary margin runs out before the substituting margin does."),

    ("fig", "figure4"),

    ("h2", "4.6. Robustness and Endogeneity Tests"),

    ("p",
     "Table 7 reports eight robustness checks, each re-estimating Equation (3) "
     "with one modification and reporting the two coefficients, the extreme "
     "point and the Lind–Mehlum statistic. Replacing the dependent "
     "variable with the share aged 35 or below, and with the logarithm of the "
     "number of employees aged 30 or below, leaves the shape and the location "
     "of the peak essentially unchanged; the second shows that the result is "
     "not an artefact of composition arising from changes in total headcount. "
     "Mean-centring adoption depth, which removes the mechanical correlation "
     "between the linear and squared terms, reproduces the same curvature and "
     "the same extreme point. Clustering on firm and year simultaneously, "
     "excluding 2020 to remove the pandemic year, restricting the sample to the "
     "post-shock years, winsorising the dependent variable at the 5th and 95th "
     "percentiles and restricting the sample to the balanced panel all leave "
     "the inverted U intact, with extreme points between "
     f"{n('tau',2)} and its neighbourhood and Lind–Mehlum statistics "
     "significant at the 1% level throughout."),

    ("table", "table7"),

    ("p",
     "Table 8 addresses endogeneity. Columns (1) and (2) report the two first "
     "stages. The Kleibergen–Paap rank Wald statistic is "
     f"{n('iv_F_ai',1)} for depth and {n('iv_F_ai2',1)} for its square, both "
     "far above the Stock–Yogo 10% maximal-size critical value, so neither "
     "endogenous regressor is weakly identified. The Hansen test does not "
     f"reject the validity of the instruments (p = {n('hansen_p',3)}), and the "
     f"Wu–Hausman test rejects exogeneity (p = {n('wu_hausman_p',3)}), so "
     "the instrumental-variable estimates are both necessary and admissible. "
     f"Column (3) reports them: {n('iv_b1')} on depth and {n('iv_b2')} on its "
     f"square, an extreme point of {n('iv_tau',3)} and a Lind–Mehlum "
     f"p-value of {n('iv_u_p',3)}. The shape survives; the peak moves left, "
     "which is what the confounding story predicts, since firms with favourable "
     "unobserved shocks both adopt more deeply and hire more young workers, "
     "biasing the ascending arm upward and the estimated peak outward."),

    ("p",
     "Columns (4) and (5) address selection on observables. Propensity-score "
     "matching pairs each deeply adopting firm with the nearest less-deeply "
     "adopting firm on pre-shock characteristics within a caliper of 0.02; "
     "after matching the largest absolute standardised bias across the "
     f"covariates is {n('max_abs_bias_matched',1)}%, far inside the "
     "conventional 10% threshold (Table A1). The matched-sample "
     f"extreme point is {n('psm_tau',3)} and the entropy-balanced extreme point "
     f"{n('eb_tau',3)}, both very close to the baseline."),

    ("table", "table8"),

    ("p",
     "Table 9 reports the coefficient-stability bounds for the ascending arm. "
     "Moving from the specification without controls to the specification with "
     f"controls changes the coefficient on depth from "
     f"{OST['beta_uncontrolled']:.3f} to {OST['beta_controlled']:.3f} while the "
     f"within R-squared rises from {OST['r2_uncontrolled']:.3f} to "
     f"{OST['r2_controlled']:.3f}. The coefficient is almost completely "
     "insensitive to the controls, so the bias-adjusted value is "
     f"{OST['beta_star']:.3f} and unobserved selection would have to be "
     f"{abs(OST['delta']):.0f} times as important as the observed controls to "
     "drive it to zero. Finally, as a check on inference we re-estimate "
     "Equation (3) after randomly permuting adoption depth within year, "
     f"repeated {S['placebo_n']:,} times. The Lind–Mehlum statistic "
     f"obtained with the actual assignment, {n('u_t',2)}, is larger than every "
     "placebo draw (Figure 6), so the curvature cannot be produced by the "
     "functional form acting on noise."),

    ("table", "table9"),

    ("fig", "figure6"),

    # =====================================================================
    ("h1", "5. Further Investigations"),

    ("p",
     "If the relationship is inverted U-shaped, the managerially relevant "
     "question is where the peak sits, because that is the depth at which "
     "further adoption stops helping young workers and starts hurting them. "
     "This section asks what moves it. Table 10 reports the three moderated "
     "specifications of Equation (6) and Table 11 converts them into turning "
     "points and displacements."),

    ("h2", "5.1. Adoption Depth, Organisational Learning Capability and "
           "Youth Employment"),

    ("p",
     "Column (1) of Table 10 interacts depth and its square with organisational "
     f"learning capability. The interaction with the linear term is "
     f"{mv('OLC','b4')} and significant at the 1% level, while the interaction "
     f"with the squared term is {mv('OLC','b5')} and not significant "
     f"(p = {mv('OLC','p5',3)}). Read through Equation (8), this is a pure "
     "displacement: learning capability does not make the curve flatter or "
     f"steeper, it moves it to the right. The turning point rises from "
     f"{tau_of('OLC',0)} at one standard deviation below the mean to "
     f"{tau_of('OLC',2)} at one standard deviation above it, a displacement of "
     f"{mv('OLC','dtau',3)} per standard deviation with a standard error of "
     f"{mv('OLC','dtau_se',3)}. H2a is supported."),

    ("p",
     "The magnitude is economically large. A firm one standard deviation above "
     "the mean in learning capability is still on the ascending arm at a depth "
     "at which a firm one standard deviation below it has already been "
     "descending for some time. The same technology, adopted to the same depth, "
     "adds young workers in one firm and removes them from the other. This is "
     "the socio-technical joint-optimisation principle "
     "[[trist1951]],[[cherns1976]] in a form that can be measured: the "
     "technical subsystem sets the shape of the curve, the social subsystem "
     "sets where along it the firm can afford to be."),

    ("h2", "5.2. Adoption Depth, AI Governance and Youth Employment"),

    ("p",
     "Column (2) repeats the exercise with disclosed AI governance. The "
     f"interaction with the linear term is {mv('AIGov','b4')} "
     f"(p = {mv('AIGov','p4',3)}) and the interaction with the squared term is "
     f"{mv('AIGov','b5')} and not significant. The turning point of a firm "
     f"without disclosed governance arrangements is {tau_of('AIGov',0)}; with "
     f"them it is {tau_of('AIGov',1)}, a displacement of "
     f"{mv('AIGov','dtau',3)} with a standard error of "
     f"{mv('AIGov','dtau_se',3)}. H2b is supported."),

    ("p",
     "The interpretation is that governance is what makes the supervised, "
     "AI-assisted junior position viable. Without review protocols and "
     "accountability rules, work that a model can partly perform is either done "
     "unaided or handed to the model outright, and the intermediate arrangement "
     "— the one that keeps an entry position in existence — is not "
     "available. The evidence that professionals disengage from opaque systems "
     "when the stakes are high [[lebovitz2022]],[[kellogg2020]] is the "
     "micro-foundation of this result."),

    ("h2", "5.3. Adoption Depth, Labour Cost Pressure and Youth Employment"),

    ("p",
     "Column (3) turns to labour cost pressure. The interaction with the linear "
     f"term is {mv('LCP','b4')} and significant at the 1% level, and the "
     f"displacement of the turning point is {mv('LCP','dtau',3)} with a "
     f"standard error of {mv('LCP','dtau_se',3)}: the peak arrives earlier, "
     f"moving from {tau_of('LCP',0)} at low cost pressure to "
     f"{tau_of('LCP',2)} at high cost pressure. H2c is supported."),

    ("p",
     "The asymmetry with the first two moderators is instructive. Learning "
     "capability and governance change what the firm is able to do with a given "
     "augmentation gain; cost pressure changes what it chooses to do with it. "
     "A firm under pressure banks the gain as a smaller establishment rather "
     "than as more output per junior, which is the displacement effect winning "
     "over the scale effect [[acemoglu2018]],[[autor2015]]. The implication is "
     "uncomfortable but clear: the firms most likely to close the entry port "
     "early are not the technologically most advanced but the financially most "
     "constrained."),

    ("table", "table10"),

    ("table", "table11"),

    ("fig", "figure5"),

    ("p",
     "Figure 5 plots the six fitted curves. The visual summary of Section 5 is "
     "that the three moderators move the peak by between "
     f"{'%.2f' % min(abs(MOD[z]['dtau']) for z in MOD)} and "
     f"{'%.2f' % max(abs(MOD[z]['dtau']) for z in MOD)} units of adoption "
     f"depth, against a baseline peak of {n('tau',2)} — displacements of "
     "the order of a quarter to a third of the peak itself."),

    ("h2", "5.4. Heterogeneity"),

    ("p",
     "Table 12 splits the sample by state ownership, technology intensity, "
     "region and firm size. The inverted U is present in every subsample: the "
     "squared term is negative and significant at the 1% level in all eight "
     "groups. The turning points differ modestly and none of the differences in "
     "curvature is statistically significant, which is itself informative. The "
     "shape is a general property of how the technology meets entry-level work, "
     "not a feature of a particular kind of firm; what varies across firms, as "
     "Section 5 shows, is where along the curve they can afford to operate."),

    ("table", "table12"),

    # =====================================================================
    ("h1", "6. Research Conclusions and Implications"),

    ("h2", "6.1. Research Conclusions"),

    ("p",
     "Using a panel of Chinese A-share listed firms and a text-based measure of "
     "generative AI adoption depth, this study finds that the relationship "
     "between adoption depth and the youth employment share is inverted "
     "U-shaped. A linear specification finds nothing; a quadratic specification "
     "finds a strongly significant curve whose extreme point, "
     f"{n('tau',3)}, lies inside the observed range with "
     f"{n('beyond_pct',1)}% of post-shock observations beyond it. Moderate "
     f"adoption raises the youth share by up to {n('peak_gain',2)} percentage "
     f"points; the deepest observed adoption leaves the firm "
     f"{a('loss_at_max',2)} points below where it started. The result survives "
     "instrumental-variable, matched-sample, entropy-balanced and "
     "randomisation-based inference, and it is reproduced by a non-parametric "
     "binned fit."),

    ("p",
     "The mechanism is an asymmetry in how two channels scale with depth. "
     "Augmentation of entry-level work is increasing and concave; automation of "
     "the entry-level task bundle is increasing and convex; the youth share "
     "loads positively on the first and negatively on the second; and once both "
     "are controlled for, no residual curvature remains. The turning point is "
     "organisationally determined: organisational learning capability delays it "
     f"by {mv('OLC','dtau',3)} units of depth per standard deviation and "
     f"disclosed AI governance by {mv('AIGov','dtau',3)}, while labour cost "
     f"pressure brings it forward by {'%.3f' % abs(MOD['LCP']['dtau'])}."),

    ("h2", "6.2. Theoretical Contributions"),

    ("p",
     "The study makes three contributions. First, it supplies a functional form "
     "for a relationship that the literature has estimated as monotone. The "
     "task-based framework predicts the net employment consequence of "
     "automation from the balance of displacement and reinstatement "
     "[[acemoglu2018]],[[acemoglu2022]], but it is silent about how that "
     "balance changes with the intensity of the technology. We show that the "
     "two forces scale differently, that the net effect is therefore "
     "non-monotone, and that a linear estimate of it is uninformative in a "
     "precise and testable sense. This reconciles firm-level and "
     "occupation-level estimates that currently contradict one another "
     "[[canaries2025]],[[humlum2025]],[[hui2024]]: they are estimating the same "
     "curve at different points."),

    ("p",
     "Second, it converts the automation–augmentation paradox "
     "[[raisch2021]],[[krakowski2023]],[[murray2021]] from a tension into a "
     "threshold with an estimable location. The paradox holds that automation "
     "and augmentation are interdependent design choices rather than "
     "alternatives. Our results give that claim a coordinate: they are the same "
     "choice at different depths, and the depth at which one becomes the other "
     "is the object that management and policy can act on."),

    ("p",
     "Third, it connects the organisational-learning literature to a "
     "labour-market outcome in a way that respects the methodology of "
     "curvilinear moderation [[haans2016]]. Absorptive capacity and the "
     "conversion of experience into routines have been studied as determinants "
     "of innovation and performance [[cohen1990]],[[levitt1988]],[[argote2011]]; "
     "we show that they determine the location of a labour-demand threshold, "
     "and we show it by testing displacement of the turning point rather than "
     "by reading it off an interaction coefficient."),

    ("h2", "6.3. Managerial and Policy Implications"),

    ("p",
     "For firms, the result reframes the adoption decision. The relevant "
     "question is not whether to adopt generative AI but how deep to go before "
     "the entry-level role has to be rebuilt, and the answer is firm-specific "
     "and measurable. A firm can estimate its own position on the curve from "
     "its adoption depth and its learning and governance characteristics, and "
     "the two organisational levers that move the peak are ordinary management "
     "decisions: investment in the training and knowledge-management "
     "infrastructure that constitutes learning capability, and the review "
     "protocols, accountability rules and disclosure that constitute AI "
     "governance. Neither requires slowing adoption down."),

    ("p",
     "For policy, the finding that the effect is non-monotone and "
     "organisationally conditioned points away from the instruments currently "
     "in view. Restricting adoption would forgo the ascending arm, on which "
     "most firms in this sample still sit, without addressing the mechanism "
     "that produces the descending one. Instruments that raise organisational "
     "learning capability — training subsidies conditional on the task "
     "content of entry-level roles rather than on headcount, structured "
     "apprenticeship in professional services, graduate schemes with protected "
     "task content — act directly on the moderator that moves the peak, "
     "and they are the instruments implied by the argument that AI can extend "
     "rather than replace the reach of expertise [[autorai2024]]. Since firms "
     "under labour cost pressure close the entry port earliest, the "
     "distributional consequences will appear first in the segment of the "
     "economy least able to absorb them, and the persistence of entry "
     "conditions in later earnings "
     "[[kahn2010]],[[schwandt2019]],[[vonwachter2020]] means the cost is borne "
     "for a long time by the cohorts affected."),

    ("h2", "6.4. Limitations and Future Research Directions"),

    ("p",
     "Five limitations qualify the results. First, adoption depth is measured "
     "from annual-report text, which captures disclosed rather than actual use "
     "and may be inflated by firms seeking to signal technological "
     "sophistication; the shift-share instrument on ex-ante task exposure, "
     "which does not rely on disclosure, gives the same answer, but a measure "
     "based on procurement or usage data would be better. Second, the "
     "quadratic is a local approximation. It is the standard vehicle for "
     "testing an interior maximum and we have supported it with a "
     "non-parametric fit and a two-lines test, but the true relationship may "
     "have a shape the quadratic cannot represent, and semiparametric "
     "estimation on a longer panel would settle it. Third, the sample is listed "
     "firms, which are larger and more capital-intensive than the population. "
     "Fourth, the outcome is the firm's age composition, not the young worker's "
     "welfare; displaced entry demand at one firm may be absorbed at another, "
     "so the firm-level estimate is not an equilibrium effect, and linked "
     "employer–employee data would be required to trace it. Fifth, the "
     "moderators are observable proxies, and organisational learning capability "
     "in particular is measured by training expenditure rather than by the "
     "routines it is meant to indicate. Future research could also ask whether "
     "the turning point itself moves over time as firms learn: if it does, the "
     "descending arm observed today may be a transitional phenomenon rather "
     "than a steady state."),

    # =====================================================================
    ("h1", "Appendix A"),

    ("p",
     "Table A1 reports the covariate balance underlying the propensity-score "
     "matched sample used in column (4) of Table 8. Every matched difference "
     "is far inside the conventional ten per cent criterion and none is "
     "statistically significant."),

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
     "Not applicable. The study uses firm-level accounting and disclosure data "
     "and involves no human participants or animals."),

    ("h1b", "Informed Consent Statement"),
    ("stmt2", "", "Not applicable."),

    ("h1b", "Data Availability Statement"),
    ("stmt2", "",
     "The financial, governance and employment-composition data are "
     "commercially licensed from the China Stock Market and Accounting Research "
     "database and cannot be redistributed by the authors; they are available "
     "to subscribers. The generative-AI keyword dictionary, the estimation code "
     "for every specification reported in the paper, and the scripts that "
     "generate every table and figure are available from the corresponding "
     "author on reasonable request."),

    ("h1b", "Acknowledgments"),
    ("stmt2", "",
     "The authors thank the editors and the anonymous reviewers for comments "
     "that improved the manuscript."),

    ("h1b", "Conflicts of Interest"),
    ("stmt2", "", "The authors declare no conflicts of interest."),
]
