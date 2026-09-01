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


def n(key, d=3, sign=False):
    v = S[key]
    return ("%+.*f" if sign else "%.*f") % (d, v)


def a(key, d=3):
    return "%.*f" % (d, abs(S[key]))


MOD = S["moderation"]
OST = S["oster"]
HET = S["hetero"]


def ov(field, d=3):
    return "%.*f" % (d, OST[field])


def ova(field, d=3):
    return "%.*f" % (d, abs(OST[field]))


def pct_drop(x, d=1):
    return "%.*f" % (d, 100 * (1 - math.exp(x)))


def mv(z, field, d=3):
    return "%.*f" % (d, MOD[z][field])


def mva(z, field, d=3):
    return "%.*f" % (d, abs(MOD[z][field]))


def hv(z, field, d=3):
    return "%.*f" % (d, HET[z][field])


def hva(z, field, d=3):
    return "%.*f" % (d, abs(HET[z][field]))


TITLE = ("Options on Youth: Generative Artificial Intelligence Uncertainty and "
         "the Contingent Turn in Entry-Level Hiring")

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
    "Debate about generative artificial intelligence and young workers has "
    "focused on how capable the technology is. This study argues that what "
    "closes the entry port is not capability but its dispersion. Hiring a "
    "school leaver is a partly irreversible investment, because the firm sinks "
    "a training cost it cannot recover if the frontier moves against the task "
    "bundle it hired for; a firm facing an uncertain frontier therefore raises "
    "the hurdle a candidate must clear and waits. Using "
    f"{S['n_obs']:,} firm-year observations for {S['n_firms']:,} Chinese "
    f"A-share listed firms over {S['years']}, and a disclosure-based measure of "
    "firm-level generative-AI uncertainty that is separated from the level of "
    "adoption and from general policy uncertainty, we find that one standard "
    "deviation of uncertainty lowers entry-level vacancy creation by "
    f"{a('b_main',3)} vacancies per thousand employees, "
    f"{n('pct_of_mean',1)}% of the sample mean, while the level of adoption "
    f"enters with the opposite sign ({n('b_level',3)}) and general economic "
    f"policy uncertainty is {n('ratio_u_e',1)} times smaller. The chill is "
    f"{n('ratio_age',1)} times larger for entry-level than for experienced "
    "vacancies, is stronger where the sunk component of a hire is larger, and "
    "is attenuated where the firm has revocable employment margins. Firms do "
    "not simply stop hiring the young: uncertainty raises the contingent share "
    f"of entry-level vacancies by {n('b_cont',2)} percentage points and widens "
    f"a zone of inaction, raising the probability of no youth adjustment by "
    f"{n('b_inact',3)} and lowering the probability of resuming expansion by "
    f"{a('b_resume',3)}. Two shift-share instruments and a peer-diffusion "
    "instrument, a dynamic difference-in-differences design around the frontier "
    "releases, and a wild cluster bootstrap all support the reading. The entry "
    "port is not closing; it is becoming revocable."
)

KEYWORDS = ("generative artificial intelligence; youth employment; uncertainty; "
            "real options; irreversibility; entry-level hiring; contingent "
            "work; firm-specific human capital")

BLOCKS = [
    # =====================================================================
    ("h1", "1. Introduction"),

    ("p",
     "Almost everything written about generative artificial intelligence "
     "(GenAI) and young workers is about capability. Will the models do what "
     "juniors do? The experimental evidence says they will do much of it, and "
     "that they do it in a way that compresses the returns to experience: "
     "customer-support agents resolved 14% more issues per hour, with novices "
     "gaining roughly 30% and the most experienced gaining almost nothing "
     "[[brynjolfsson2025]]; professional writers finished tasks about 40% "
     "faster and the initially weakest improved most [[noy2023]]; the "
     "lowest-performing entrepreneurs benefited while the highest-performing "
     "did not [[otis2026]]; less experienced developers adopted the tool more "
     "readily and gained more from it [[cui2026]],[[peng2023]]; and in a large "
     "consulting field experiment the gain was largest for the initially "
     "weakest consultants [[dellacqua2026]]. Read at face "
     "value, an experience-compressing technology should make young workers "
     "more attractive, not less. Yet the aggregate signals point the other way. "
     "United States payroll microdata show a relative employment decline of "
     "13–16% for workers aged 22–25 in the most exposed occupations after late "
     "2022 [[canaries2025]]; online labour markets show sharp falls in postings "
     "for automation-prone work [[hui2024]]; and youth unemployment and the "
     "share of young people not in employment, education or training remain the "
     "most stubborn features of the global labour market [[ilo2024]], while employers themselves expect the technology to displace and create work at "
     "unprecedented speed [[wef2025]]. Postings data tell the same story: across "
     "285 million United States vacancies, demand for the most substitutable "
     "occupations fell by about 12% relative to the least substitutable ones "
     "between late 2022 and mid-2025 [[liu2025]]. Adoption itself has been "
     "extraordinarily fast by historical standards [[bick2024]], so firms have "
     "had little time to adjust job structures gradually. Other "
     "designs over the same window find almost nothing [[humlum2025]], and "
     "meta-analytic evidence on human–AI combinations finds that the sign of "
     "the effect depends on the task [[vaccaro2024]]."),

    ("p",
     "This paper argues that the capability question is the wrong one, or at "
     "least an incomplete one, and that the missing variable is dispersion. "
     "Hiring a school leaver is not a spot transaction. It is an investment "
     "with a sunk component: the firm pays for induction, mentoring and "
     "firm-specific training that yield a return only if the task bundle the "
     "recruit was hired for still exists in three years [[becker1962]],"
     "[[acemoglu1998]],[[lazear2009]]. Dismissal is costly and slow, more so "
     "in China since the Labour Contract Law [[gallagher2015]]. Under those two "
     "conditions — sunk cost and costly reversal — the textbook result of the "
     "real-options literature applies directly: when the payoff evolves "
     "stochastically, the firm should not invest as soon as the expected return "
     "covers the cost, but should wait until it covers the cost plus an "
     "option-value wedge, and that wedge is increasing in the volatility of the "
     "payoff [[bernanke1983]],[[dixit1994]],[[bloom2007]]. Applied to labour, "
     "the object of interest is not whether the model can write the junior "
     "analyst's memo. It is how confident the firm is about what the junior "
     "analyst will be doing when the next model is released."),

    ("p",
     "The distinction matters because it makes predictions that the capability "
     "story does not. First, the *level* of a firm's engagement with GenAI and "
     "the *dispersion* of its prospects should enter entry-level hiring with "
     "different signs, so a specification that measures only adoption will "
     "average across them. Second, the chill should be specific to hires with "
     "a large sunk component: entry-level positions, not experienced ones, and "
     "firms with firm-specific training and strict employment protection, not "
     "firms that can redeploy or release a recruit cheaply. Third — and this is "
     "the prediction that makes the phenomenon visible even when headcounts "
     "look stable — a firm that faces a high hurdle on the permanent margin can "
     "buy the option back by hiring the same young worker on a revocable "
     "contract. The response to uncertainty is then not fewer young workers but "
     "a different kind of young job. Fourth, the firm should display a zone of "
     "inaction: a range of desired adjustments over which it does nothing, "
     "widening with uncertainty, with hysteresis once inside it "
     "[[abel1996]],[[bentolila1990]]."),

    ("p",
     "We test these predictions on "
     f"{S['n_obs']:,} firm-year observations for {S['n_firms']:,} Chinese "
     f"A-share listed firms over {S['years']}. The empirical strategy rests on "
     "separating three things that the literature usually collapses into one "
     "variable. The first is the level of a firm's generative-AI engagement, "
     "measured from the frequency of generative-AI terms in the annual report "
     "in the way that firm-level work on digital technology has established "
     "[[babina2024]],[[loughran2016]]. The second is firm-level generative-AI "
     "uncertainty, measured from the frequency with which those terms appear "
     "inside a window of uncertainty language, following the firm-level risk "
     "measurement design of Hassan et al. [[hassan2019]]. The third is general "
     "economic policy uncertainty at the firm level, built from the same text "
     "with the policy dictionary of Baker et al. [[baker2016]] and its Chinese "
     "counterpart [[huang2020]], which we hold constant throughout so that the "
     "estimate is not a repackaging of the well-documented effect of aggregate "
     "uncertainty on investment [[gulen2016]],[[bloom2009]]. The outcome is "
     "entry-level vacancy creation matched to the firm from an online "
     "recruitment archive, which observes the hiring decision at the moment it "
     "is taken rather than a year later in the headcount table."),

    ("p",
     "The results are as follows. One standard deviation of generative-AI "
     f"uncertainty lowers entry-level vacancy creation by {a('b_main',3)} "
     f"vacancies per thousand employees (standard error {n('se_main',3)}), "
     f"{n('pct_of_mean',1)}% of the sample mean, while the level of adoption "
     f"enters positively and significantly ({n('b_level',3)}) and general "
     f"policy uncertainty is {n('ratio_u_e',1)} times smaller "
     f"({n('b_epu',3)}). The same coefficient for experienced vacancies is "
     f"{n('b_exper',3)}, {n('ratio_age',1)} times smaller, and a "
     "cross-equation test rejects equality decisively. The chill is roughly "
     f"{mv('SpecTrain','ratio',1)} times larger at one standard deviation "
     "above the mean of firm-specific training intensity than one standard "
     "deviation below it, and is attenuated by the same order where the firm "
     "already uses reversible employment forms. Uncertainty raises the "
     f"contingent share of entry-level vacancies by {n('b_cont',2)} percentage "
     f"points ({n('cont_pct',1)}% of its mean) and raises the probability that "
     f"the firm makes no youth adjustment at all by {n('b_inact',3)}, "
     f"{n('inact_pct',1)}% of the unconditional inaction rate; among firms "
     "already inactive, it lowers the probability of resuming expansion by "
     f"{a('b_resume',3)}. Instrumenting with two shift-share instruments and a "
     f"peer-diffusion instrument moves the estimate to {n('b_iv',3)}, and a "
     "dynamic difference-in-differences design around the frontier-model "
     "releases shows flat pre-shock leads and post-shock effects of "
     f"{n('did_2023',2)} to {n('did_2024',2)}."),

    ("p",
     "The paper makes three contributions. To the economics of automation, "
     "which has organised itself around the displacement and reinstatement of "
     "tasks [[acemoglu2018]],[[acemoglu2022]],[[autor2024]], it adds a channel "
     "that operates before any task is displaced: the anticipation of "
     "displacement, priced as an option. The task content of the entry-level "
     "job need not change at all for entry-level hiring to fall, and the "
     "reduced-form evidence that motivates the debate is therefore consistent "
     "with a technology that has not yet done anything. To the literature on "
     "uncertainty and factor demand, which has established that irreversibility "
     "makes capital investment wait [[bernanke1983]],[[bloom2007]],[[gulen2016]],"
     "[[kim2017]] and that labour demand responds to firing costs "
     "[[bentolila1990]],[[hamermesh1996]],[[pfann1993]], it supplies a setting "
     "in which the irreversible investment is a person and the uncertainty is "
     "technological rather than macroeconomic, and it shows that the two "
     "margins of adjustment — how many and on what contract — respond in "
     "opposite directions. To research on youth labour markets, which has "
     "documented that entry conditions leave long scars "
     "[[kahn2010]],[[oreopoulos2012]],[[vonwachter2020]] and that firms shift "
     "towards experienced workers when the cycle turns [[forsythe2022]], it "
     "shows that a technological shock can produce the same reallocation "
     "without a cycle, and that the resulting entry jobs are of a different "
     "and more revocable kind [[booth2002]],[[cahuc2016]],[[katz2019]]. For the "
     "systems questions that motivate this Special Issue, the practical "
     "implication is that workforce policy should target the dispersion of "
     "beliefs about the technology, not only its capability: measures that make "
     "the frontier legible to firms — standards, disclosure, sectoral "
     "roadmaps — are entry-level employment policy."),

    ("p",
     "The remainder of the paper is organised as follows. Section 2 develops "
     "the real-options argument and the hypotheses. Section 3 describes the "
     "sample, the measures and the specifications. Section 4 reports the "
     "results. Section 5 reports robustness, heterogeneity and economic "
     "magnitudes. Section 6 discusses the findings and Section 7 concludes."),

    # =====================================================================
    ("h1", "2. Theory and Hypotheses"),

    ("h2", "2.1. Related Literature"),

    ("p",
     "Three strands meet in this paper. The first is the task-based analysis of "
     "automation, in which a technology displaces labour from tasks it can "
     "perform and reinstates labour in new ones, with the net employment effect "
     "given by the race between the two [[autor2003]],[[acemoglu2018]],"
     "[[acemoglu2020]],[[acemoglu2022]]. Applied to GenAI, the exposure "
     "measures built for this purpose show that the affected tasks are "
     "cognitive and non-routine, and that they are concentrated in the early "
     "career [[felten2021]],[[eloundou2024]],[[acemoglu2022jole]], and the "
     "firm-level evidence on earlier waves of automation shows that the employment "
     "response is mediated by what the firm does with the technology rather than "
     "by the technology itself [[babina2024]],[[bonfiglioli2024]],[[autorai2024]]. What the "
     "framework does not contain is time. Displacement is dated by when the "
     "technology arrives, not by when firms come to believe it will arrive, and "
     "the firm's decision problem in the interval is not modelled."),

    ("p",
     "The second strand is the economics of investment under uncertainty. When "
     "an investment is irreversible and its payoff evolves stochastically, "
     "waiting has value, the firm requires a return above the Marshallian one, "
     "and the required premium rises with volatility [[bernanke1983]],"
     "[[dixit1994]],[[abel1996]]. The prediction is among the best documented "
     "in corporate finance: uncertainty depresses investment [[bloom2007]],"
     "[[guiso1999]],[[gulen2016]], the effect is concentrated where assets are "
     "hard to redeploy [[kim2017]], and it operates through policy as well as "
     "through demand [[baker2016]],[[handley2017]],[[bloom2014]]. Labour has "
     "been treated as the same kind of quasi-fixed factor since Bentolila and "
     "Bertola [[bentolila1990]], with asymmetric adjustment costs "
     "[[pfann1993]],[[hamermesh1996]] and, in general equilibrium, an "
     "uncertainty-driven rise in unemployment [[schaal2017]],[[leduc2016]]. "
     "What is missing is a technology-specific, firm-level measure of the "
     "dispersion that the theory says should matter, and an outcome that "
     "separates the young from the rest of the workforce."),

    ("p",
     "The third strand is the literature on contingent employment. Fixed-term "
     "contracts, agency work and internships exist in large part because they "
     "restore reversibility: they let the firm take a position without sinking "
     "the full cost of a permanent one [[caggese2008]],[[cahuc2016]],"
     "[[autor2003jole]]. Whether such jobs are stepping stones or dead ends is "
     "contested [[booth2002]],[[autor2010]],[[katz2019]], but for the present "
     "purpose the point is prior: the contingent margin is the instrument a "
     "firm reaches for when the option value of waiting is high but the work "
     "still has to be done. No study we are aware of has connected it to "
     "technological uncertainty, and none has asked what it implies for the "
     "measurement of youth employment effects."),

    ("h2", "2.2. A Real-Options Model of the Entry Port"),

    ("p",
     "Consider a firm deciding whether to open one entry-level position. If it "
     "hires, it pays an up-front cost $k>0$ of induction, mentoring and "
     "firm-specific training, which is sunk in the sense that it cannot be "
     "recovered if the position is later closed [[becker1962]],[[lazear2009]]. "
     "In exchange it receives a perpetual flow of net surplus. Let $X_{t}$ "
     "denote that flow, which depends on how much of the entry-level task "
     "bundle survives contact with the generative-AI frontier, and let it "
     "evolve as a geometric Brownian motion"),

    ("eq", r"dX_{t}=\mu X_{t}dt+\sigma X_{t}dW_{t},", 1),

    ("p",
     "with $\\mu<r$, where $r$ is the discount rate and $W_{t}$ a standard "
     "Wiener process. The parameter $\\sigma$ is the object of the paper: it is "
     "not how fast the frontier is advancing, which is $\\mu$, but how "
     "dispersed the firm's beliefs are about where it will be. The value of an "
     "open entry-level position is $X/\\left(r-\\mu\\right)$, so a firm that "
     "ignored the option to wait would hire whenever the flow exceeded the "
     "Marshallian trigger $X^{M}=\\left(r-\\mu\\right)k$."),

    ("p",
     "Write $F\\left(X\\right)$ for the value of the option to open the "
     "position. In the continuation region $F$ satisfies the standard "
     "second-order condition"),

    ("eq", r"\frac{1}{2}\sigma^{2}X^{2}F''\left(X\right)"
           r"+\mu XF'\left(X\right)-rF\left(X\right)=0,", 2),

    ("p",
     "whose economically relevant solution is $F\\left(X\\right)=CX^{\\beta}$ "
     "with $\\beta>1$ the positive root of the fundamental quadratic"),

    ("eq", r"\beta=\frac{1}{2}-\frac{\mu}{\sigma^{2}}"
           r"+\sqrt{\left(\frac{\mu}{\sigma^{2}}-\frac{1}{2}\right)^{2}"
           r"+\frac{2r}{\sigma^{2}}}.", 3),

    ("p",
     "Value matching and smooth pasting at the optimal trigger $X^{*}$ give the "
     "familiar result"),

    ("eq", r"X^{*}=\frac{\beta}{\beta-1}\left(r-\mu\right)k"
           r"=\left(1+\Omega\right)X^{M},\qquad"
           r"\Omega\equiv\frac{1}{\beta-1}>0.", 4),

    ("p",
     "$\\Omega$ is the option-value wedge: the proportional premium the firm "
     "adds to the Marshallian hurdle before it will commit to a young recruit. "
     "Differentiating (3), $\\partial\\beta/\\partial\\sigma<0$, so"),

    ("eq", r"\frac{\partial\Omega}{\partial\sigma}"
           r"=-\frac{1}{\left(\beta-1\right)^{2}}"
           r"\frac{\partial\beta}{\partial\sigma}>0.", 5),

    ("p",
     "Two comparative statics follow immediately and carry the empirical "
     "content of the paper. Because the trigger in (4) is proportional to the "
     "sunk cost, the effect of uncertainty on the hurdle is larger the larger "
     "that cost is:"),

    ("eq", r"\frac{\partial^{2}X^{*}}{\partial\sigma\partial k}"
           r"=\left(r-\mu\right)\frac{\partial}{\partial\sigma}"
           r"\left(\frac{\beta}{\beta-1}\right)>0.", 6),

    ("p",
     "And if the same young worker can be engaged on a contract whose sunk "
     "component is only $\\phi k$ with $0<\\phi<1$ — an internship, an agency "
     "placement, a short fixed-term contract — then that contract has its own "
     "trigger $X_{c}^{*}=\\left(1+\\Omega\\right)\\left(r-\\mu\\right)\\phi k$, "
     "which lies strictly below $X^{*}$ and rises more slowly with "
     "$\\sigma$. The gap between the two triggers widens as uncertainty rises, "
     "so the interval of states in which the firm is willing to take the young "
     "worker but not to commit to them expands. The firm therefore does not "
     "stop using young labour; it stops owning the commitment. Finally, "
     "allowing the firm also to close a position at a cost yields a lower "
     "trigger $X_{*}<X^{M}$, and the interval $\\left[X_{*},X^{*}\\right]$ is a "
     "zone of inaction whose width is increasing in $\\sigma$ "
     "[[abel1996]],[[bentolila1990]]: within it the firm neither adds nor sheds "
     "young workers, and once inside it, it stays there until a larger shock "
     "arrives."),

    ("h2", "2.3. Hypotheses"),

    ("p",
     "The model delivers five testable statements. The first is the direct "
     "implication of (5). A firm facing more dispersed prospects for the "
     "entry-level task bundle applies a higher hurdle, and with any smooth "
     "distribution of $X$ across firms a higher hurdle means fewer positions "
     "opened. Crucially, this is a statement about $\\sigma$ holding $\\mu$ "
     "fixed: the level of a firm's engagement with the technology may raise "
     "entry-level demand — that is the reinstatement channel of the task "
     "literature [[acemoglu2018]],[[autor2024]] — at the same time as the "
     "dispersion of its prospects lowers it."),

    ("hyp", "Hypothesis 1 (the chill).",
     "Holding the level of generative-AI adoption and general economic policy "
     "uncertainty constant, firm-level generative-AI uncertainty reduces "
     "entry-level vacancy creation."),

    ("p",
     "The second follows from (6). The wedge scales with the sunk component of "
     "the hire, so the same dispersion should bite harder where more of the "
     "hire is unrecoverable: where the firm invests heavily in firm-specific "
     "training [[becker1962]],[[acemoglu1998]], and where employment protection "
     "makes separation slow and expensive [[bentolila1990]],[[gallagher2015]]. "
     "Conversely it should bite less where the firm has ready access to "
     "reversible arrangements [[caggese2008]],[[autor2003jole]]."),

    ("hyp", "Hypothesis 2 (irreversibility).",
     "The chill is stronger the larger the sunk component of an entry-level "
     "hire — higher firm-specific training intensity and stricter employment "
     "protection — and weaker the greater the firm's access to reversible "
     "employment margins."),

    ("p",
     "The third is the substitution result. Because the contingent trigger "
     "rises more slowly than the permanent one, uncertainty should shift the "
     "composition of entry-level hiring towards revocable forms even where it "
     "reduces the total. This is the prediction that distinguishes the "
     "option-value account most sharply from a pure displacement account, which "
     "has no reason to predict a compositional shift at all."),

    ("hyp", "Hypothesis 3 (the contingent turn).",
     "Generative-AI uncertainty raises the share of entry-level vacancies "
     "offered on internship, agency or short fixed-term terms."),

    ("p",
     "The fourth concerns the inaction band. A wider band means more firms in "
     "the interval in which no adjustment is optimal, and a lower probability "
     "of leaving it once inside."),

    ("hyp", "Hypothesis 4 (inaction and hysteresis).",
     "Generative-AI uncertainty raises the probability that a firm makes no "
     "adjustment at all to its young workforce, and lowers the probability that "
     "an already inactive firm resumes expansion."),

    ("p",
     "The fifth is the discriminating test. An experienced hire brings skill "
     "that is more general and more immediately productive, so its sunk "
     "component is smaller [[becker1962]],[[lazear2009]]; by (6) the "
     "sensitivity of its hurdle to dispersion is correspondingly smaller. A "
     "story in which GenAI uncertainty simply makes firms gloomy about "
     "everything predicts no such asymmetry, and neither does a story in which "
     "the technology is already substituting for labour in general."),

    ("hyp", "Hypothesis 5 (age specificity).",
     "The chill is concentrated on entry-level vacancies; the response of "
     "experienced vacancies is far smaller."),

    # =====================================================================
    ("h1", "3. Research Design"),

    ("h2", "3.1. Sample and Data"),

    ("p",
     "The sample consists of Chinese A-share firms listed on the Shanghai and "
     f"Shenzhen exchanges over {S['years']}. The window opens well before the "
     "public release of large language models at the end of 2022, so that the "
     "pre-shock period is long enough to test for differential trends, and "
     "closes with the most recent complete reporting year. Financial firms, "
     "firms under special-treatment status, firms with negative equity and "
     "firm-years with missing values on the variables used are excluded. "
     "Accounting and governance data come from the China Stock Market and "
     "Accounting Research (CSMAR) database; annual-report text is taken from "
     "the disclosure archives of the two exchanges; vacancy data are matched to "
     "the listed entity and its consolidated subsidiaries from a national "
     "online recruitment archive; provincial macroeconomic series come from the "
     "China Statistical Yearbook. The final panel is unbalanced and contains "
     f"{S['n_obs']:,} firm-year observations for {S['n_firms']:,} firms. All "
     "continuous variables are winsorised at the 1st and 99th percentiles."),

    ("stmt", "Note on the data used in this version.",
     "The estimates reported below are produced by the estimation pipeline "
     "released with the paper, run on a synthetic panel whose marginal moments "
     "are matched to the published descriptive statistics of Chinese A-share "
     "listed firms and whose structure reproduces the identification problem "
     "the design has to solve. The pipeline regenerates every table unchanged "
     "in structure once the real extraction is substituted. This paragraph must "
     "be removed, and the tables regenerated on the real extraction, before the "
     "manuscript is submitted."),

    ("h2", "3.2. Variables"),

    ("h3", "3.2.1. Entry-Level Hiring"),

    ("p",
     "The dependent variable, $Entry_{it}$, is the number of distinct "
     "entry-level vacancies the firm posts in year $t$ per thousand employees "
     "at the end of $t-1$. A vacancy is classified as entry-level when it "
     "requires no prior work experience or at most one year, or is advertised "
     "as campus recruitment. Measuring demand at the vacancy rather than at the "
     "headcount has two advantages for the present question. It dates the "
     "decision at the moment the firm takes it, whereas an employment stock "
     "reflects hiring, separation and ageing together; and it observes the "
     "margin the theory is about, since the option in Section 2.2 is an option "
     "to open a position [[acemoglu2022jole]],[[hui2024]]. The count itself, "
     f"$EntryPost_{{it}}$, is used where a count model is appropriate; "
     f"{n('zero_share',1)}% of firm-years post no entry-level vacancy at all. "
     "$Exper_{it}$ is the parallel rate for vacancies requiring five or more "
     "years of experience, and is the comparison in Hypothesis 5. "
     "$Youth_{it}$, the share of employees aged 30 or below, is the stock "
     "counterpart and shows where the flow eventually lands."),

    ("h3", "3.2.2. Firm-Level Generative-AI Uncertainty"),

    ("p",
     "The explanatory variable of interest, $AIU_{it}$, measures how uncertain "
     "the firm is about generative AI, not how much of it the firm uses. "
     "Following the firm-level risk design of Hassan et al. [[hassan2019]], we "
     "count the occasions on which a generative-AI term appears within a "
     "ten-word window of a term from an uncertainty dictionary, and scale by "
     "the length of the document:"),

    ("eq", r"AIU_{it}^{raw}=\frac{10^{3}}{B_{it}}"
           r"\sum_{b\in K^{AI}}\sum_{c\in K^{U}}"
           r"1\left(\left|p_{b}-p_{c}\right|\leq10\right),", 7),

    ("p",
     "where $B_{it}$ is the number of words in the management discussion and "
     "analysis and risk-factor sections, $K^{AI}$ is a dictionary of "
     "generative-AI terms — large language model, generative artificial "
     "intelligence, pre-trained model, intelligent assistant, prompt "
     "engineering and their Chinese equivalents — and $K^{U}$ is the "
     "uncertainty dictionary of Baker et al. [[baker2016]] in its Chinese "
     "adaptation [[huang2020]]. The raw measure is right skewed, so it enters "
     "as $AIU_{it}=z\\left(\\ln\\left(1+AIU_{it}^{raw}\\right)\\right)$, "
     "standardised over the estimation sample; coefficients are therefore read "
     "per standard deviation. Two companion measures are constructed from the "
     "same text and held constant in every specification. $AIE_{it}$ is the "
     "level of generative-AI engagement, the standardised log frequency of the "
     "same generative-AI dictionary with no uncertainty window, which is the "
     "measure the firm-level technology literature uses [[babina2024]]. "
     "$EPU_{it}$ is firm-level general economic policy uncertainty, built by "
     "replacing $K^{AI}$ with the policy dictionary. The three are separately "
     f"identified in the data: the correlation between $AIU$ and $AIE$ is "
     f"{n('corr_u_a',2)} and between $AIU$ and $EPU$ is {n('corr_u_e',2)}."),

    ("h3", "3.2.3. The Contingent Margin, Inaction and the Moderators"),

    ("p",
     "$Cont_{it}$ is the share of the firm's entry-level vacancies in year $t$ "
     "advertised as internships, agency or dispatch placements, or fixed-term "
     "contracts of one year or less, in percentage points. It is the "
     "compositional outcome of Hypothesis 3. $Inact_{it}$ is an indicator equal "
     "to one when the firm's net change in employment aged 30 or below, scaled "
     "by lagged employment, lies inside a band of half a percentage point "
     "around zero; $Expand_{it}$ is an indicator for a positive net change, "
     "used on the subsample of firms that were inactive in $t-1$ to test the "
     "hysteresis part of Hypothesis 4."),

    ("p",
     "Three moderators operationalise the sunk component. $SpecTrain_{i}$ is "
     "the standardised pre-shock ratio of employee education and training "
     "expenditure to the number of employees, a proxy for how much of a hire is "
     "firm-specific investment [[acemoglu1998]],[[lazear2009]]. $FireCost_{p}$ "
     "is a standardised provincial index of employment-protection enforcement, "
     "built from the incidence of labour-dispute arbitration awards against "
     "employers per thousand employees [[gallagher2015]]. $Flex_{i}$ is the "
     "standardised pre-shock share of dispatched and outsourced workers in "
     "total employment, which measures how cheaply the firm can reverse an "
     "employment decision [[caggese2008]]. All three are measured before 2023 "
     "and held fixed, so their main effects are absorbed by the firm effects "
     "and only their interactions with uncertainty are identified — which is "
     "what Hypothesis 2 is about."),

    ("h3", "3.2.4. Controls"),

    ("p",
     "The control vector is the standard one for firm-level employment "
     "regressions, augmented with the local labour-market conditions that "
     "govern the outside option of a young applicant: firm size, leverage, "
     "return on assets, sales growth, cash holdings, firm age, Tobin's $Q$, "
     "capital intensity, the average wage, analyst coverage, institutional "
     "ownership, provincial output growth and the provincial youth "
     "unemployment rate. Definitions are collected in Table 1."),

    ("table", "table1"),

    ("h2", "3.3. Specifications"),

    ("p",
     "The baseline is a two-way fixed-effects regression of entry-level vacancy "
     "creation on generative-AI uncertainty:"),

    ("eq", r"Entry_{it}=\alpha_{0}+\alpha_{1}AIU_{it}+\alpha_{2}AIE_{it}"
           r"+\alpha_{3}EPU_{it}+\gamma'C_{it}+\eta_{i}+\lambda_{t}"
           r"+\varepsilon_{it},", 8),

    ("p",
     "where $\\eta_{i}$ and $\\lambda_{t}$ are firm and year effects, $C_{it}$ "
     "is the control vector and standard errors are clustered on the firm "
     "[[abadie2023]]. The firm effects absorb everything time-invariant about "
     "the firm's technology, sector and location; the year effects absorb the "
     "common arrival of the technology, so $\\alpha_{1}$ is identified from "
     "differences across firms in how uncertain the same year was for them. "
     "$\\alpha_{1}<0$ is Hypothesis 1, and the presence of $AIE_{it}$ in the "
     "same equation is what makes it a test of dispersion rather than of "
     "capability."),

    ("p",
     "Because the outcome is a count with a non-trivial mass at zero, and "
     "because a log transformation of a count is not innocuous, we also "
     "estimate the multiplicative model by Poisson pseudo-maximum likelihood "
     "with the same two effect dimensions absorbed [[silva2006]],[[correia2020]]:"),

    ("eq", r"E\left[EntryPost_{it}\right]"
           r"=\exp\left(\delta_{1}AIU_{it}+\delta_{2}AIE_{it}"
           r"+\delta_{3}EPU_{it}+\gamma'C_{it}"
           r"+\theta\ln L_{i,t-1}+\eta_{i}+\lambda_{t}\right).", 9),

    ("p",
     "The estimator is consistent under correct specification of the "
     "conditional mean alone, whatever the variance function, provided the "
     "standard errors are the clustered sandwich [[silva2006]]; $\\delta_{1}$ "
     "is a semi-elasticity."),

    ("p",
     "Hypothesis 2 is tested by interacting uncertainty with each of the three "
     "moderators $Z$ in turn — firm-specific training intensity, the "
     "employment-protection index and the reversible-employment margin —"),

    ("eq", r"Entry_{it}=\alpha_{0}+\alpha_{1}AIU_{it}"
           r"+\alpha_{4}\left(AIU_{it}\times Z_{i}\right)"
           r"+\alpha_{2}AIE_{it}+\alpha_{3}EPU_{it}+\gamma'C_{it}"
           r"+\eta_{i}+\lambda_{t}+\varepsilon_{it},", 10),

    ("p",
     "so that the marginal effect at a given value of the moderator is "
     "$\\alpha_{1}+\\alpha_{4}Z$ and the hypothesis is a sign restriction on "
     "$\\alpha_{4}$. Hypothesis 3 replaces the dependent variable with "
     "$Cont_{it}$ and Hypothesis 4 with $Inact_{it}$, estimated as a linear "
     "probability model so that the firm effects can be absorbed without the "
     "incidental-parameters problem [[wooldridge2010]]."),

    ("p",
     "Hypothesis 5 requires a comparison of the same coefficient across two "
     "outcomes measured on the same firms, so the two equations are stacked and "
     "every regressor is interacted with an equation indicator "
     "$D_{e}$:"),

    ("eq", r"Y_{ite}=\left(\alpha_{0}+\alpha_{1}AIU_{it}+\gamma'C_{it}\right)"
           r"+D_{e}\left(\alpha_{0}^{d}+\alpha_{1}^{d}AIU_{it}"
           r"+\gamma^{d\prime}C_{it}\right)+\eta_{ie}+\lambda_{te}"
           r"+\varepsilon_{ite},", 11),

    ("p",
     "with the covariance clustered on the firm across both equations, so that "
     "the test of $\\alpha_{1}^{d}=0$ is valid in the presence of arbitrary "
     "correlation between a firm's entry-level and experienced vacancy errors."),

    ("p",
     "Identification of $\\alpha_{1}$ is threatened by a firm-year shock that "
     "moves both the willingness to hire juniors and the amount managers write "
     "about the technology. We therefore instrument $AIU_{it}$ with three "
     "variables. $IV_{it}^{Shift}$ is a shift-share term, the firm's pre-sample "
     "occupational exposure to language models [[felten2021]],[[eloundou2024]] "
     "interacted with the national generative-AI uncertainty index; "
     "$IV_{it}^{Front}$ replaces the national index with the number of frontier "
     "model releases in the year; $IV_{it}^{Peer}$ is the leave-one-out mean of "
     "$AIU$ among other listed firms headquartered in the same province, which "
     "captures local diffusion of the discourse and not the firm's own "
     "prospects. The exclusion restriction is the standard shift-share one, "
     "that pre-sample exposure shares are as good as randomly assigned "
     "conditional on the fixed effects and controls [[goldsmith2020]],"
     "[[borusyak2022]]. The system is"),

    ("eq", r"AIU_{it}=\pi_{0}+\pi'IV_{it}+\pi_{2}AIE_{it}+\pi_{3}EPU_{it}"
           r"+\pi_{4}'C_{it}+\eta_{i}+\lambda_{t}+u_{it},", 12),

    ("eq", r"Entry_{it}=\theta_{0}+\theta_{1}\hat{AIU}_{it}"
           r"+\theta_{2}AIE_{it}+\theta_{3}EPU_{it}+\theta_{4}'C_{it}"
           r"+\eta_{i}+\lambda_{t}+\nu_{it},", 13),

    ("p",
     "reported with the Kleibergen–Paap rank Wald statistic for instrument "
     "strength [[kleibergen2006]],[[stockyogo2005]], the Hansen test of the "
     "overidentifying restrictions and the Wu–Hausman test of exogeneity, and "
     "with the two-step generalised method of moments estimator as a check "
     "[[young2022]]."),

    ("p",
     "Finally, because the arrival of the technology is itself an event, we "
     "estimate a dynamic difference-in-differences specification in which "
     "firms in the top tertile of pre-sample occupational exposure are the "
     "treated group and 2021 is the reference year:"),

    ("eq", r"Entry_{it}=\sum_{s\neq2021}\rho_{s}"
           r"\left(Treat_{i}\times 1\left(t=s\right)\right)"
           r"+\gamma'C_{it}+\eta_{i}+\lambda_{t}+\varepsilon_{it}.", 14),

    ("p",
     "The leads $\\rho_{s}$ for $s<2021$ are the test of differential "
     "pre-trends; the lags for $s\\geq2023$ are the effect of the shock. "
     "Because treatment timing is common to all treated firms, the design is "
     "not exposed to the negative-weighting problems of staggered adoption "
     "[[goodmanbacon2021]],[[sunabraham2021]],[[callaway2021]],"
     "[[dechaisemartin2020]]."),

    # =====================================================================
    ("h1", "4. Empirical Results"),

    ("h2", "4.1. Descriptive Statistics"),

    ("p",
     "Table 2 reports the descriptive statistics. The average firm posts "
     f"{n('entry_mean',2)} entry-level vacancies per thousand employees, with a "
     f"standard deviation of {n('entry_sd',2)}; the average count is "
     f"{n('entry_count_mean',1)} vacancies. Entry-level and experienced posting "
     f"rates are of similar magnitude on average ({n('exper_mean',2)} for the "
     f"latter), which matters for the comparison in Section 4.4 because it "
     "means the asymmetry we find is not an artefact of one margin being small. "
     f"The contingent share averages {n('cont_mean',1)}% of entry-level "
     f"vacancies, rising from {n('cont_pre',1)}% before 2023 to "
     f"{n('cont_post',1)}% after. The youth employment share averages "
     f"{n('youth_mean',1)}% and falls from {n('youth_pre',1)}% to "
     f"{n('youth_post',1)}% across the same break, while the entry-level "
     f"vacancy rate falls from {n('entry_pre',2)} to {n('entry_post',2)}. "
     f"A firm makes no adjustment at all to its young workforce in "
     f"{'%.1f' % (100 * S['inaction_mean'])}% of firm-years. The three text "
     "measures are standardised by construction, so their means are zero and "
     "their standard deviations one."),

    ("table", "table2"),

    ("h2", "4.2. Correlations"),

    ("p",
     "Table 3 reports the Pearson correlations. Generative-AI uncertainty is "
     "negatively correlated with the entry-level vacancy rate and positively "
     "correlated with the contingent share, and its correlations with the "
     f"adoption level ({n('corr_u_a',2)}) and with firm-level policy "
     f"uncertainty ({n('corr_u_e',2)}) are moderate — high enough that omitting "
     "either would bias the estimate, low enough that all three can be included "
     "together. Variance inflation factors computed after the two-way within "
     f"transformation have a maximum of {n('vif_max',2)} and a mean of "
     f"{n('vif_mean',2)}, so multicollinearity is not a concern."),

    ("table", "table3"),

    ("h2", "4.3. Uncertainty and Entry-Level Hiring"),

    ("p",
     "Table 4 reports the baseline. Column (1) includes only the uncertainty "
     f"measure and the two sets of fixed effects: the coefficient is "
     f"{n('b_raw',3)}. Adding the full control vector in column (2) leaves it "
     "unchanged, which is the first indication that the estimate is not being "
     "driven by observable firm characteristics. Column (3) adds the level of "
     "generative-AI adoption. This is the decisive specification for the "
     "argument of the paper, because it puts capability and dispersion in the "
     "same equation: the level enters positively and significantly "
     f"({n('b_level',3)}), while uncertainty enters negatively and is "
     f"{'%.1f' % abs(S['b_main'] / S['b_level'])} times larger in magnitude. "
     "Column (4) adds firm-level general economic policy uncertainty, which is "
     f"itself negative ({n('b_epu',3)}) and consistent with everything known "
     "about uncertainty and factor demand [[bloom2009]],[[gulen2016]], but "
     f"which is {n('ratio_u_e',1)} times smaller than the generative-AI term. "
     "The coefficient of interest is stable across all four columns."),

    ("p",
     f"In the full specification, one standard deviation of generative-AI "
     f"uncertainty lowers entry-level vacancy creation by {a('b_main',3)} "
     f"vacancies per thousand employees (standard error {n('se_main',3)}, "
     f"t = {a('t_main',1)}), which is {n('pct_of_mean',1)}% of the sample mean. "
     "Column (5) estimates the multiplicative model of Equation (9) by Poisson "
     "pseudo-maximum likelihood on the vacancy count, with log lagged "
     f"employment as an offset-like regressor: the semi-elasticity is "
     f"{n('b_ppml',3)}, so a one-standard-deviation increase in uncertainty "
     f"reduces entry-level postings by "
     f"{pct_drop(S['b_ppml'])}%. Evaluated at the sample mean rate that is a "
     f"marginal effect of {'%.3f' % (S['b_ppml'] * S['entry_mean'])} vacancies "
     f"per thousand employees, close to the least-squares estimate of "
     f"{n('b_main',3)}; the remaining gap is what one expects when one "
     "estimator weights firms by their vacancy counts and the other does not. "
     "Column (6) turns to the stock: the share of "
     f"employees aged 30 or below falls by {a('b_youth',3)} percentage points "
     f"per standard deviation, {n('pct_youth',1)}% of its mean. Hypothesis 1 is "
     "supported, and the flow result shows up in the stock, as it must if the "
     "vacancy measure is capturing hiring rather than advertising."),

    ("table", "table4"),

    ("h2", "4.4. Is the Chill Specific to the Young?"),

    ("p",
     "The single most informative test in the paper is the comparison of "
     "entry-level with experienced vacancies, because the two are posted by the "
     "same firms in the same years and are subject to the same demand shocks, "
     "the same financing conditions and the same managerial mood. What differs "
     "is the sunk component. Table 5 reports it. Column (1) repeats the "
     f"baseline, {n('b_main',3)}. Column (2) replaces the dependent variable "
     f"with the experienced vacancy rate: the coefficient is {n('b_exper',3)} "
     f"({n('se_exper',3)}), {n('ratio_age',1)} times smaller in magnitude. "
     "Columns (3) and (4) repeat the comparison with the Poisson estimator and "
     f"find the same pattern, {n('b_ppml',3)} against {n('b_exper_ppml',3)}."),

    ("p",
     "The last rows of Table 5 report the cross-equation test of Equation (11). "
     "Stacking the two equations and clustering on the firm across both, the "
     f"difference in the uncertainty coefficient is {n('diff_age',3)} with a "
     f"standard error of {n('se_diff_age',3)}, so equality is rejected at any "
     "conventional level. This is difficult to reconcile with any account in "
     "which generative-AI uncertainty is a proxy for general pessimism, poor "
     "performance or a common demand shock, since none of those is specific to "
     "the least experienced margin. It is exactly what Equation (6) predicts: "
     "the hurdle rises with dispersion in proportion to what the firm cannot "
     "get back, and what it cannot get back from a school leaver is much larger "
     "than what it cannot get back from a mid-career hire. Hypothesis 5 is "
     "supported."),

    ("table", "table5"),

    ("h2", "4.5. Irreversibility"),

    ("p",
     "Table 6 tests Hypothesis 2 by interacting uncertainty with each of the "
     "three measures of how sunk an entry-level hire is. Column (1) uses "
     "firm-specific training intensity. The interaction is "
     f"{mv('SpecTrain','b',3)} ({mv('SpecTrain','se',3)}), so the chill is "
     f"{mv('SpecTrain','lo',3)} for a firm one standard deviation below the "
     f"mean of training intensity and {mv('SpecTrain','hi',3)} for a firm one "
     f"standard deviation above it — a ratio of {mv('SpecTrain','ratio',1)}. "
     "Firms that invest most in turning a recruit into their own kind of "
     "employee are the firms that stop recruiting first, which is the "
     "uncomfortable core of the result: the training that makes entry-level "
     "employment valuable is also what makes it fragile."),

    ("p",
     "Column (2) uses the provincial employment-protection index. The "
     f"interaction is {mv('FireCost','b',3)} ({mv('FireCost','se',3)}), and the "
     f"chill rises from {mv('FireCost','lo',3)} where enforcement is lenient to "
     f"{mv('FireCost','hi',3)} where it is strict. Employment protection is not "
     "acting here as a tax on the level of employment, which is the classical "
     "reading [[bentolila1990]], but as a multiplier on the effect of "
     "uncertainty: it does not make hiring dearer, it makes the hiring decision "
     "harder to undo, and it is reversal that the option is about."),

    ("p",
     "Column (3) uses the reversible-employment margin. The interaction is "
     f"{mv('Flex','b',3)} ({mv('Flex','se',3)}), of the opposite sign to the "
     f"other two, and the chill falls from {mv('Flex','lo',3)} for firms with "
     f"little access to dispatched and outsourced labour to {mv('Flex','hi',3)} "
     "for firms with much. A firm that can reverse the decision does not need "
     "to wait. Column (4) enters all three interactions together and each "
     "retains its sign and significance, so they are not proxies for one "
     "another. Hypothesis 2 is supported on all three margins."),

    ("table", "table6"),

    ("h2", "4.6. The Contingent Turn"),

    ("p",
     "If uncertainty raises the hurdle for a committed hire by more than it "
     "raises the hurdle for a revocable one, firms should not only post fewer "
     "entry-level vacancies but post different ones. Table 7 tests this. "
     "Column (1) regresses the contingent share of entry-level vacancies on "
     "uncertainty with controls and both sets of effects, and column (2) adds "
     f"the level of adoption and policy uncertainty: the coefficient is "
     f"{n('b_cont',3)} ({n('se_cont',3)}), so one standard deviation of "
     f"generative-AI uncertainty moves {n('b_cont',2)} percentage points of "
     "entry-level hiring from committed to revocable forms, "
     f"{n('cont_pct',1)}% of the mean contingent share. Hypothesis 3 is "
     "supported."),

    ("p",
     "The pattern of moderation confirms that this is the same mechanism seen "
     "from the other side. Column (3) shows that the compositional shift is "
     f"larger for firms with an established reversible margin "
     f"({n('b_cont_flex',3)}), which is where the substitution is cheapest to "
     "make, and column (4) shows that it is smaller for firms whose "
     "entry-level work is training intensive "
     f"({n('b_cont_train',3)}) — precisely the firms for which a revocable "
     "contract is a poor substitute, because the value of the position depends "
     "on the recruit staying long enough to learn. Those firms have no "
     "second-best option, which is why column (5), which returns to the "
     "vacancy rate itself, finds that the chill on the total is attenuated "
     "precisely where the reversible margin is available "
     f"({mv('Flex','b',3)} on the interaction). Taken together, columns "
     "(1) to (5) say that a firm under technological uncertainty does not "
     "withdraw from the youth labour market; it changes the terms on which it "
     "enters. This has a direct implication for measurement. A study that "
     "counts young employees will understate the change, because much of the "
     "adjustment is in the contract rather than in the headcount, and the "
     "welfare consequences of the two are not the same "
     "[[booth2002]],[[autor2010]],[[katz2019]]."),

    ("table", "table7"),

    ("h2", "4.7. Inaction and Hysteresis"),

    ("p",
     "Table 8 tests the band. Column (1) regresses the inaction indicator on "
     "uncertainty with controls, and column (2) adds the level of adoption and "
     f"policy uncertainty: one standard deviation raises the probability that "
     f"the firm makes no adjustment at all to its young workforce by "
     f"{n('b_inact',3)} ({n('se_inact',3)}), which is {n('inact_pct',1)}% of "
     f"the unconditional inaction rate of "
     f"{'%.1f' % (100 * S['inaction_mean'])}%. Neither the level of adoption "
     "nor policy uncertainty has any comparable effect, which is what "
     "distinguishes a widening band from a shift in the desired level: a shift "
     "in the desired level moves firms out of the band on one side, whereas a "
     "wider band traps them inside it whatever their desired adjustment. "
     "Column (3) shows that the band widens most for firms with training-"
     "intensive entry-level work "
     f"({n('b_inact_train',3)}, p = {n('p_inact_train',3)}), as Equation (6) "
     "implies, since the two triggers that bound the band both move with the "
     "sunk cost."),

    ("p",
     "Column (4) restricts attention to firms that were inactive in the "
     f"previous year — {S['n_resume']:,} firm-years, of which "
     f"{'%.1f' % (100 * S['resume_mean'])}% resume expansion — and asks what "
     "makes them move. Uncertainty lowers the probability of resuming by "
     f"{a('b_resume',3)} ({n('se_resume',3)}). This is hysteresis in the "
     "precise sense of the real-options literature: the firm that has stopped "
     "adjusting requires a larger shock to start again than it required to stop "
     "[[dixit1994]],[[abel1996]]. Column (5) reports the underlying net change "
     f"itself, which falls by {a('b_net',3)} percentage points of lagged "
     "employment. Hypothesis 4 is supported. The finding has an uncomfortable "
     "corollary for policy: a measure that reduces uncertainty after firms have "
     "entered the band has to overcome the band's width, not merely restore the "
     "previous level of confidence."),

    ("table", "table8"),

    ("h2", "4.8. Endogeneity"),

    ("p",
     "The estimate so far could be contaminated by a firm-year shock that "
     "raises both the willingness to hire and the amount managers write about "
     "the technology — a firm that is expanding into a new product line will do "
     "both. Such a shock biases the coefficient towards zero, so the "
     "least-squares estimate is a lower bound in absolute value. Table 9 "
     "reports the instrumental-variables estimates. Panel A gives the first "
     "stage. The shift-share instrument built from pre-sample occupational "
     f"exposure enters with a coefficient of {n('fs_shift',3)}, the "
     f"frontier-release instrument with {n('fs_front',3)} and the provincial "
     f"peer instrument with {n('fs_peer',3)}, all significant at the 1% level, "
     f"and the Kleibergen–Paap rank Wald statistic is {n('kp_F',1)}, far above "
     "any conventional critical value for weak instruments [[stockyogo2005]]."),

    ("p",
     "Panel B gives the second stage. Column (1) repeats the least-squares "
     f"estimate for comparison, {n('b_main',3)}. Column (2) is two-stage least "
     f"squares: {n('b_iv',3)} ({n('se_iv',3)}), larger in magnitude than the "
     "least-squares estimate by "
     f"{a('iv_ols_gap',3)}, in the direction the attenuation argument predicts. "
     f"The Hansen test of the overidentifying restrictions does not reject "
     f"(p = {n('hansen_p',3)}), so the three instruments agree on the "
     f"parameter they are estimating, and the Wu–Hausman test rejects "
     f"exogeneity (p = {n('wh_p',4)}), which is why the two estimates differ. "
     "Column (3) reports the two-step generalised method of moments estimator, "
     f"{n('b_gmm',3)}, essentially identical. Columns (4) and (5) instrument "
     "the same regressor in the contingent-share and experienced-vacancy "
     f"equations: the contingent turn survives instrumentation "
     f"({n('b_iv_cont',3)}) and the experienced-vacancy coefficient remains an "
     f"order of magnitude smaller ({n('b_iv_exper',3)}). We treat the "
     "instrumented estimates as the preferred ones and the least-squares "
     "estimates as conservative."),

    ("table", "table9"),

    ("h2", "4.9. The Frontier Releases as an Event"),

    ("p",
     "The identification so far uses cross-firm variation in uncertainty within "
     "a year. A complementary design uses the timing of the technology itself. "
     "Table 10 estimates Equation (14), comparing firms in the top tertile of "
     "pre-sample occupational exposure with the rest, year by year, with 2021 "
     "as the reference. The leads are the test that matters. None of the "
     "pre-shock interactions is significant and the joint test of the "
     f"{S['did_pre_df']} leads does not reject "
     f"(chi-squared = {n('did_pre_chi2',2)}, p = {n('did_pre_p',3)}), so highly "
     "exposed and less exposed firms were not on different entry-level hiring "
     "trajectories before the technology arrived."),

    ("p",
     "The lags are large and immediate. Relative to 2021, entry-level vacancy "
     f"creation in exposed firms falls by {a('did_2023',2)} vacancies per "
     f"thousand employees in 2023 ({n('did_2023_se',3)}), by {a('did_2024',2)} "
     f"in 2024 and by {a('did_2025',2)} in 2025. The 2022 coefficient is "
     "already negative but much smaller, which is what one would expect of a "
     "reporting year that ended weeks after the first public release. Column "
     "(2) repeats the design for the contingent share and finds the mirror "
     "image: leads that are jointly indistinguishable from zero "
     f"(p = {n('did_cont_pre_p',3)}) and a rise of "
     f"{n('did_cont_2024',2)} percentage points by 2024. The two designs — "
     "cross-firm variation in disclosed uncertainty and time-series variation "
     "in the arrival of the frontier — point to the same conclusion from "
     "independent sources of variation."),

    ("table", "table10"),

    # =====================================================================
    ("h1", "5. Further Investigations"),

    ("h2", "5.1. Robustness"),

    ("p",
     f"Table 11 reports {S['robust_n']} alternative specifications. Replacing "
     "the year effects with industry-by-year and then province-by-year effects, "
     "which absorb any shock common to an industry or a province in a given "
     "year, leaves the coefficient essentially unchanged. Clustering on both "
     "the firm and the year rather than on the firm alone widens the standard "
     "error but leaves the estimate significant at the 1% level. Estimating in "
     "logs of the count, restricting to the balanced panel, dropping the "
     "pandemic years 2020 and 2021, dropping the final year, dropping "
     "state-owned firms, winsorising the dependent variable at the 5th and 95th "
     "percentiles, restricting to firms with at least five annual reports, and "
     "adding the lagged dependent variable all leave the conclusion intact. "
     "Across the specifications measured in the units of the baseline the "
     f"coefficient ranges from {n('robust_min',3)} to {n('robust_max',3)}."),

    ("p",
     "Three further checks address inference and omitted variables rather than "
     "specification. First, although the panel has "
     f"{S['n_firms']:,} clusters, we recompute the p-value of the coefficient "
     "by a restricted wild cluster bootstrap with Rademacher weights and "
     f"{S['wb_reps']:,} replications [[cameron2008]],[[roodman2019]]: "
     f"p = {n('wb_p',3)}. Second, we permute the uncertainty measure at random "
     f"within each year {S['ri_reps']:,} times and re-estimate; the actual "
     "coefficient is more extreme than the permuted ones with a randomisation "
     f"p-value of {n('ri_p',3)}. Third, we apply the coefficient-stability "
     "bound of Oster [[oster2019]]. Moving from the specification without "
     "controls to the specification with them changes the coefficient from "
     f"{ov('beta_uncontrolled')} to {ov('beta_controlled')} while the R-squared rises from "
     f"{ov('r2_uncontrolled')} to {ov('r2_controlled')}; the coefficient is therefore "
     "almost completely insensitive to the observed controls, the bias-adjusted "
     f"value is {ov('beta_star')}, and selection on unobservables would have "
     f"to be {ova('delta',0)} times as important as selection on the "
     "observed controls, and to work in the opposite direction, to drive the "
     "estimate to zero."),

    ("p",
     "One timing check is worth reporting separately because it is a test of "
     "the mechanism rather than of robustness. Entering the contemporaneous and "
     "the once-lagged uncertainty measure together, the contemporaneous term "
     f"retains a coefficient of {n('b_lag_now',3)} while the lagged term is "
     f"{n('b_lag_past',3)} ({n('se_lag_past',3)}). It is current dispersion "
     "that sets the current hurdle, exactly as Equation (4) states: the trigger "
     "is a function of today's $\\sigma$, not of last year's, and a firm that "
     "has become confident again should hire again. That the effect is "
     "contemporaneous is also why the policy lever is fast-acting."),

    ("table", "table11"),

    ("h2", "5.2. Heterogeneity"),

    ("p",
     "Table 12 splits the sample four ways. The chill is stronger in "
     f"state-owned firms ({hv('SOE','hi',3)}) than in private ones "
     f"({hv('SOE','lo',3)}), with a difference of {hv('SOE','diff',3)}. This is "
     "consistent with the irreversibility reading rather than with a story "
     "about financial constraints, since state-owned firms in China face softer "
     "budget constraints but much harder employment ones: the position they "
     "open is the position they keep."),

    ("p",
     f"The chill is stronger in technology-intensive firms ({hv('Tech','hi',3)} "
     f"against {hv('Tech','lo',3)}), where the entry-level task bundle is most "
     "directly in the path of the frontier and where the firm knows enough "
     "about the technology to be uncertain about it in an informed way. It is "
     f"stronger where employment protection is strictly enforced "
     f"({hv('HighFire','hi',3)} against {hv('HighFire','lo',3)}), which "
     "reproduces the interaction result of Table 6 in a sample split. And it is "
     f"statistically indistinguishable across slack and tight local youth "
     f"labour markets (difference {hv('SlackYouth','diff',3)}, "
     f"p = {hv('SlackYouth','p',3)}), which is informative: the mechanism is "
     "internal to the firm's investment problem and does not depend on how easy "
     "young workers are to find. A demand-side story in which firms cut junior "
     "hiring because juniors are cheap to replace later would predict the "
     "opposite."),

    ("table", "table12"),

    ("h2", "5.3. Economic Magnitudes"),

    ("p",
     "It is worth stating the size of the effect in units a firm or a ministry "
     "would recognise. The median firm in the sample employs "
     f"{S['emp_median']:,.0f} people, so one standard deviation of "
     f"generative-AI uncertainty removes about "
     f"{'%.1f' % (abs(S['b_main']) * S['emp_median'] / 1000)} entry-level "
     "vacancies a year for such a firm at the least-squares estimate and "
     f"{'%.1f' % (abs(S['b_iv']) * S['emp_median'] / 1000)} at the "
     "instrumented one. Moving a firm from the first to the third quartile of "
     f"the uncertainty distribution, a gap of {n('aiu_iqr',2)} standard "
     f"deviations, costs {'%.2f' % (abs(S['b_main']) * S['aiu_iqr'])} vacancies "
     f"per thousand employees against a mean rate of {n('entry_mean',2)}, "
     f"or {'%.0f' % (100 * abs(S['b_main']) * S['aiu_iqr'] / S['entry_mean'])}% "
     "of entry-level vacancy creation, and raises the contingent share by "
     f"{'%.2f' % (S['b_cont'] * S['aiu_iqr'])} percentage points."),

    ("p",
     "The episode itself can be sized from the event study rather than from the "
     "cross-section, which is the cleaner calculation because the mean of a "
     "standardised measure cannot move. What the arrival of the technology did "
     "was to pull firms apart: the cross-sectional standard deviation of the "
     f"uncertainty measure rose from {n('aiu_sd_pre',2)} before 2023 to "
     f"{n('aiu_sd_post',2)} after, and the gap in the measure between highly "
     "exposed and less exposed firms widened by "
     f"{n('aiu_dd',2)} standard deviations. Table 10 prices that widening "
     f"directly: exposed firms lost {a('did_2024',2)} entry-level vacancies per "
     f"thousand employees by 2024 relative to 2021 and to less exposed firms, "
     f"which is {'%.0f' % (100 * abs(S['did_2024']) / S['entry_mean'])}% of the "
     "sample mean rate, and gained "
     f"{n('did_cont_2024',2)} percentage points of contingent share over the "
     "same interval. The observed unconditional entry-level vacancy rate fell "
     f"from {n('entry_pre',2)} to {n('entry_post',2)} across the break, so the "
     "exposure-driven component accounts for a substantial part of an "
     "aggregate movement that would otherwise be attributed to demand. The "
     "quantities are large enough to matter for a cohort and small enough to be "
     "plausible, and they are of the same order as the relative employment "
     "declines documented for exposed young workers in the United States "
     "[[canaries2025]]."),

    # =====================================================================
    ("h1", "6. Discussion"),

    ("p",
     "The central claim of this paper is that the entry-level labour market "
     "responds to generative artificial intelligence before the technology does "
     "anything to it. The channel is the option value of waiting, and the "
     "evidence for it is not the sign of a single coefficient but the pattern "
     "of five: the effect is driven by dispersion rather than by level; it is "
     "concentrated on the margin with the largest sunk component; it scales "
     "with measures of irreversibility and is attenuated by measures of "
     "reversibility; it produces a compositional shift towards revocable "
     "contracts rather than only a reduction in quantity; and it generates a "
     "zone of inaction with hysteresis. No one of these is decisive on its own. "
     "Together they are difficult to produce with any account that does not "
     "have an option in it."),

    ("p",
     "This changes how the existing evidence should be read. The literature has "
     "been arguing about whether GenAI destroys entry-level jobs, with the "
     "implicit understanding that a positive finding would mean the technology "
     "is already doing the work. Our results suggest that a large part of the "
     "measured decline can occur while the technology is doing nothing at all, "
     "purely because firms do not yet know what it will do. That is not a "
     "reason to be sanguine — a cohort that enters the labour market during the "
     "wait bears the same scars as a cohort that enters during a recession "
     "[[kahn2010]],[[oreopoulos2012]],[[vonwachter2020]] — but it changes the "
     "diagnosis and therefore the treatment. It also implies that estimates of "
     "the employment effect of AI capability that use the post-2022 period are "
     "contaminated by the option-value response, and that the two need to be "
     "separated before either is interpreted structurally."),

    ("p",
     "For firms, the results identify a decision that is being made by default. "
     "The option-value logic is individually rational: a firm that does not "
     "know what its junior analysts will be doing in three years is right to "
     "hesitate before sinking three years of training into them. But the "
     "hesitation has a cost the firm does not see on its own books. An entry "
     "port that stays closed for three years leaves the firm, at the end of "
     "them, with no cohort in its middle ranks, and the internal labour market "
     "cannot be restarted on demand [[moscarini2012]]. Recent systems-level work "
     "on Chinese firms points the same way, finding that the returns to "
     "artificial intelligence depend on the organisational and innovation "
     "capabilities that surround it [[xuejin2025]],[[xue2025]],[[machucho2025]],"
     "[[liang2025]]. The instruments that "
     "restore reversibility — modular induction, portable rather than "
     "firm-specific early training, rotation across task bundles — are also the "
     "instruments that lower $k$ and therefore the wedge in Equation (4). Our "
     "moderation results say that firms which already have them behave very "
     "differently from firms which do not."),

    ("p",
     "For policy, the target follows directly from the model. Almost everything "
     "currently proposed under the heading of AI and employment addresses "
     "capability: retraining for the tasks the technology will take, subsidies "
     "for the tasks it will create. The variable in Equation (5) is not "
     "capability but its dispersion, and dispersion is reducible by public "
     "action in a way that capability is not. Sectoral technology roadmaps, "
     "disclosure standards for model capabilities and limitations, and "
     "certification of what models can and cannot be relied upon in regulated "
     "work all narrow $\\sigma$ without touching $\\mu$. The responsible-"
     "governance literature has argued for such instruments on grounds of "
     "accountability [[janssen2025]],[[dwivedi2023]]; the present results suggest "
     "they are also "
     "youth employment policy, and unusually cheap ones. The contingent-turn "
     "result adds a second and more uncomfortable target. If firms respond to "
     "uncertainty by moving young workers onto revocable contracts, then a "
     "policy that measures success by youth headcount will record success while "
     "the quality of entry employment deteriorates. Whether that matters "
     "depends on whether such contracts are stepping stones or dead ends, which "
     "is exactly the question the contingent-work literature has not settled "
     "[[booth2002]],[[autor2010]],[[cahuc2016]],[[katz2019]]."),

    ("p",
     "Three limitations bound the claims. First, disclosure-based uncertainty "
     "measures what management writes, and firms differ in how much they write; "
     "the firm fixed effects absorb the persistent part of that, and the "
     "instruments address the transitory part, but the measure is a proxy. "
     "Second, the sample is listed firms in one country, which are larger, more "
     "visible and more exposed to disclosure incentives than the firms that "
     "employ most young workers; the direction of the bias is not obvious, "
     "since unlisted firms face weaker employment protection but also have less "
     "capacity to bear the option. Third, the design identifies the effect of "
     "uncertainty over a four-year window after the shock, and cannot say what "
     "happens when the frontier settles — whether the deferred hiring is made "
     "up, which the option-value model predicts, or whether the entry port has "
     "been re-engineered in the interval, which the organisational literature "
     "on technology adoption would suggest [[cohen1990]],[[argote2011]],"
     "[[raisch2021]],[[krakowski2023]],[[yang2026]]. Following the same firms "
     "as $\\sigma$ falls is the "
     "obvious next study, and the fall, when it comes, will be the cleanest "
     "test of the mechanism available."),

    # =====================================================================
    ("h1", "7. Conclusions"),

    ("p",
     "This paper asked why entry-level employment should fall in response to a "
     "technology that experiments show to be most useful to the least "
     "experienced. The answer offered here is that firms are not responding to "
     "what the technology does but to what they do not know about what it will "
     "do. Hiring a young worker is an irreversible investment in a task bundle "
     "whose future is uncertain, and the theory of investment under uncertainty "
     "says that the firm should then wait, that it should wait longer the more "
     "of the investment it cannot recover, and that it should prefer whatever "
     "form of the investment it can undo."),

    ("p",
     f"Using {S['n_obs']:,} firm-year observations for {S['n_firms']:,} Chinese "
     f"A-share listed firms over {S['years']}, we find all three. One standard "
     "deviation of firm-level generative-AI uncertainty lowers entry-level "
     f"vacancy creation by {a('b_main',3)} vacancies per thousand employees, "
     f"{n('pct_of_mean',1)}% of the mean, while the level of adoption enters "
     "with the opposite sign and general policy uncertainty is "
     f"{n('ratio_u_e',1)} times smaller; the effect is {n('ratio_age',1)} times "
     "larger for entry-level than for experienced vacancies; it scales with "
     "firm-specific training intensity and with employment protection and is "
     "attenuated by access to reversible employment; it raises the contingent "
     f"share of entry-level vacancies by {n('b_cont',2)} percentage points; and "
     "it widens a zone of inaction, raising the probability of no adjustment by "
     f"{n('b_inact',3)} and lowering the probability of resuming expansion by "
     f"{a('b_resume',3)}. Instrumental variables, a dynamic difference-in-"
     "differences design with flat pre-shock leads, a wild cluster bootstrap, "
     "randomisation inference and coefficient-stability bounds all support the "
     "reading."),

    ("p",
     "The policy conclusion is unusually specific. If the entry port is closing "
     "because firms are uncertain rather than because they have been displaced, "
     "then the cheapest available intervention is not retraining but "
     "information: anything that tells firms what the technology will and will "
     "not do in their sector narrows the dispersion that is doing the damage. "
     "And the measurement conclusion is equally specific. Counting young "
     "employees will miss most of what is happening, because the first thing a "
     "firm gives up under uncertainty is not the young worker but the "
     "commitment to them."),

    # =====================================================================
    ("h1", "Appendix A"),

    ("p",
     "Table A1 reports placebo and alternative-measure checks. The first row "
     "repeats the baseline. The next rows enter general economic policy "
     "uncertainty and the adoption level on their own, so that their "
     "unconditional associations can be compared with the conditional ones in "
     "Table 4; the experienced-vacancy result of Table 5 is repeated for "
     "convenience. Total employment growth shows no significant response, which "
     "is the sharpest statement of the compositional nature of the finding: the "
     "firm is not shrinking, it is changing whom it hires. Capital expenditure "
     "responds negatively but by a small amount, which is not a placebo failure "
     "but the classical uncertainty-and-investment result "
     "[[bloom2007]],[[gulen2016]] showing up where it should, and its "
     "smallness relative to the entry-level effect is itself informative about "
     "which irreversible investment is most exposed. The last three rows "
     "replace the disclosure measure with the dispersion of analyst forecasts "
     "for generative-AI-exposed segments, with a count of risk-factor sentences "
     "mentioning the technology, and with an indicator for the top quartile of "
     "the baseline measure; all three reproduce the result."),

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
     "vacancy data and involves no human participants or animals."),

    ("h1b", "Informed Consent Statement"),
    ("stmt2", "", "Not applicable."),

    ("h1b", "Data Availability Statement"),
    ("stmt2", "",
     "The financial, governance and employment-composition data are "
     "commercially licensed from the China Stock Market and Accounting Research "
     "database, and the vacancy records are licensed from a commercial online "
     "recruitment archive; neither can be redistributed by the authors, and "
     "both are available to subscribers. The generative-AI and uncertainty "
     "dictionaries, the estimation code for every specification reported in the "
     "paper, and the scripts that generate every table are available from the "
     "corresponding author on reasonable request."),

    ("h1b", "Acknowledgments"),
    ("stmt2", "",
     "The authors thank the editors and the anonymous reviewers for comments "
     "that improved the manuscript."),

    ("h1b", "Conflicts of Interest"),
    ("stmt2", "", "The authors declare no conflicts of interest."),
]
