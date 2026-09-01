# -*- coding: utf-8 -*-
"""The manuscript text.

Every quantitative statement is interpolated from tables/summary.json,
which analysis/run_all.py writes, so the prose cannot disagree with what
the code computed. Citations are [[key]] markers resolved by build_docx.py
into bracketed numbers ordered by first appearance.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "tables", "summary.json"),
          encoding="utf-8") as _fh:
    S = json.load(_fh)

MAIN = S["main"]
AUD = S["audit"]
STR = S["strata"]
SW = S["sweep"]
RC = S["riskcov"]
NZ = S["noise"]
LOGG = S["logging"]
MM = S["mismatched"]
FF = S.get("fair_fix") or {}
AUCS = S["aucs"]
META = S["meta"]

MINUS = "−"


def f3(x):
    return ("%.3f" % x).replace("-", MINUS)


def f2(x):
    return ("%.2f" % x).replace("-", MINUS)


def f1(x):
    return ("%.1f" % x).replace("-", MINUS)


def m(name, key):
    return MAIN[name][key][0]


def pm(name, key, fmt=f3):
    a, sd = MAIN[name][key]
    return "%s (%s)" % (fmt(a), fmt(sd))


def sw_at(alpha):
    for d in SW:
        if abs(d["alpha"] - alpha) < 1e-9:
            return d
    raise KeyError(alpha)


def nz_at(eta):
    for d in NZ:
        if abs(d["eta"] - eta) < 1e-9:
            return d
    raise KeyError(eta)


ORACLE_SHARE = 100.0 * m("RAMT", "yield100") / m("Oracle", "yield100")
ADMIN_MULT = m("RAMT", "yield100") / m("AdminRule", "yield100")
_FITS = [S["main"][k]["fit"][0]
         for k in ("AdminRule", "FCFS", "MLP-Acc", "Logit-Acc+DA",
                   "GBM-Ret", "RAMT", "Oracle")]
FIT_LO, FIT_HI = min(_FITS), max(_FITS)

# stay-yield of the best mixing point on the sweep
SW_BEST = max(SW, key=lambda d: d["yield100"])

# ===========================================================================
TITLE = ("Retention-Aware Match Tracing for Auditable Allocation of "
         "Rural Youth Talent to Village Posts under Generative "
         "AI-Assisted Profiling")

AUTHORS = [("Yang Lu", False)]

AFFILIATIONS = [
    "Tongji Zhejiang College, Jiaxing, Zhejiang 314051, China",
]

ABSTRACT = (
    "County programmes that recruit young people into rural industry and "
    "village governance increasingly pair generative-AI profiling of "
    "unstructured application materials with algorithmic person-post "
    "matching, yet the matchers in use optimise immediate placement, "
    "explain themselves post hoc if at all, and are silent about the "
    "outcome the whole talent chain is built around: whether the young "
    "person is still in the village two years later. This paper proposes "
    "Retention-Aware Match Tracing (RAMT), a matching engine that is "
    "auditable by construction. The scorer is additive over a "
    "pre-registered ledger of person-post features, each passed through a "
    "piecewise-linear spline, so every match ships an evidence ledger "
    "that reconstructs its score exactly, with zero residual rather than "
    "an attribution estimate. The score feeds a discrete-time retention "
    "hazard trained on logged administrative matching records with "
    "inverse-propensity weights, and offers are formed by "
    "capacity-constrained deferred acceptance, with low-margin matches "
    "abstained to human review. Because no county authority can release "
    "youth-level records, evaluation uses a simulated labour micro-market "
    "whose marginals are anchored to published national statistics and "
    "whose ground-truth retention process is deliberately outside the "
    "model family — regime-switching, threshold-bearing and interactive. "
    f"Across {META['n_seeds']} market replications, RAMT converts "
    f"{f1(m('RAMT', 'yield100'))} of every 100 offers into matches still "
    f"in place at 24 months, {f1(ADMIN_MULT)} times the administrative "
    f"wage-rank rule and {f1(ORACLE_SHARE)} per cent of the oracle "
    "ceiling, while its ledger passes counterfactual-flip audits that "
    "sampled Shapley trails on equally accurate black-box baselines "
    "fail. The principal warning is distributional: because village "
    "wages sit below graduate expectations, a retention-optimal matcher "
    "rationally deprioritises the most educated youth, assigning them at "
    f"{f2(m('RAMT', 'parity'))} times the rate of their less-educated "
    "peers — the engine quietly gives up on exactly the people the "
    "policy is trying to attract, and repairing this costs a small, "
    "quantifiable share of total retention.")

INDEX_TERMS = ("Auditable artificial intelligence, generative artificial "
               "intelligence, person-post matching, rural revitalization, "
               "youth employment.")

# ===========================================================================
BLOCKS = [
    ("h1", "Introduction"),
    ("p",
     "Rural revitalisation runs on young people, and China's counties "
     "now compete for them. National monitoring counts nearly 300 "
     "million rural migrant workers [[nbs2024]], and county policy now "
     "works to draw part of that cohort back toward county and "
     "village employment. What a returning young person finds is a thin, "
     "fragmented market: village posts in modern agriculture, rural "
     "e-commerce, agritourism and grassroots governance are scattered "
     "across dozens of administrative villages, capacities are small, "
     "wages sit below urban expectations, and the match between what a "
     "post needs and what a young person can do is judged by whoever "
     "happens to administer the scheme. Field studies of returnee "
     "entrepreneurship show how sensitive these trajectories are to "
     "local embeddedness, prior experience and capability endowments "
     "[[wang2022returnee]], [[ding2025migrant]], [[lu2023ability]], and "
     "county governments have responded by building talent-chain "
     "programmes that recruit, train, place and — they hope — retain "
     "rural youth."),
    ("p",
     "Generative artificial intelligence is entering this chain at two "
     "points. Upstream, large language models turn unstructured "
     "application materials, training records and post descriptions "
     "into structured profiles — the digital portraiture that county "
     "programmes now build [[liu2025gai]], and a task at which "
     "structured extraction from free text is by now well demonstrated "
     "[[dagdelen2024]]. Downstream, the structured profiles feed "
     "person-post matching, for which the technical shelf offers "
     "learned person-job fit models of considerable sophistication "
     "[[qin2020]], [[mashayekhi2024]]. A county talent office that "
     "wires these two components together has, in effect, an automated "
     "employment decision system for a public programme."),
    ("p",
     "Three things are wrong with the default way of wiring it. First, "
     "the objective is wrong: recommender-style matchers are trained on "
     "immediate outcomes — clicks, applications, offer acceptance — "
     "whereas the talent chain's binding constraint is retention. "
     "The predictable failure mode follows: young people are placed, "
     "and then leave, because the placement optimised the placement "
     "rate. Second, the models "
     "are opaque: a two-tower network scores a pair and the office "
     "cannot state why this youth was routed to that post, which "
     "matters because an automated employment decision about a public "
     "programme is precisely the class of decision that regulation now "
     "expects to be explained and audited — the European Union's AI "
     "Act classifies employment-related systems as high-risk "
     "[[euaiact2024]], New York City already mandates bias audits of "
     "automated employment decision tools [[wright2024]], and China's "
     "interim measures on generative AI impose transparency duties on "
     "exactly the profiling layer upstream [[migliorini2024]]. Third, "
     "the allocation is unstable: greedy platform-style filling leaves "
     "pairs who would both prefer each other unmatched to their "
     "assigned partners, and in a small two-sided market such "
     "instability is not a technicality but churn."),
    ("p",
     "This paper proposes Retention-Aware Match Tracing (RAMT), a "
     "matching engine built so that the three failures cannot occur by "
     "construction rather than by good intentions. The scorer is "
     "additive over a pre-registered ledger of person-post features, "
     "each passed through a one-dimensional piecewise-linear spline in "
     "the tradition of intelligible additive models [[lou2012]], "
     "[[agarwal2021]]; because the score is a sum, every match ships an "
     "evidence ledger whose entries reconstruct the score exactly, with "
     "zero residual, rather than approximately in the manner of "
     "post-hoc attribution [[ribeiro2016]], [[lundberg2017]]. The "
     "score parameterises a discrete-time retention hazard "
     "[[singer1993]], trained not on placements but on what became of "
     "them, using logged records of the county's historical matching "
     "rule with inverse-propensity weights to undo the logging "
     "policy's selection [[swaminathan2015]], [[schnabel2016]]. "
     "Offers are formed by capacity-constrained deferred acceptance "
     "[[gale1962]], [[roth2008]], which leaves no blocking pair with "
     "respect to the stated preferences, and matches whose score "
     "margin is small under an ensemble are abstained to a human case "
     "worker [[geifman2017]], following the deference designs of "
     "human-AI decision making [[mozannar2023]]."),
    ("p",
     "Evaluating such an engine raises an obstacle that is itself "
     "methodologically interesting: no county authority can release "
     "youth-level administrative records with retention outcomes, and "
     "any evaluation on real logs would in any case be unable to "
     "observe the counterfactual — what would have happened under the "
     "assignment the engine did not make. We therefore evaluate on a "
     "simulated labour micro-market, stated as such in every section "
     "of this paper, in the tradition of simulation-based evaluation "
     "of decision systems [[horton2023]], [[li2024econ]]. The "
     "simulator's marginal distributions are anchored to published "
     "national statistics [[nbs2024]], [[cnnic2025]] and its "
     "ground-truth retention process is deliberately constructed "
     "outside the model family of every engine evaluated: hazards "
     "switch regimes between a settling-in phase and a consolidation "
     "phase, carry a hard wage-expectation threshold, and contain "
     "multiplicative interactions. An additive scorer cannot win on "
     "this ground truth by specification identity, and a further "
     "validity check re-runs the entire evaluation under a second, "
     "structurally different generator."),
    ("p",
     "The contributions are fourfold. (1) An auditable matching "
     "architecture that couples an exactly decomposable additive "
     "scorer to an off-policy retention hazard and a stable "
     "capacity-constrained assignment, with abstention as a "
     "first-class output. (2) A decision-level audit methodology: "
     "beyond the reconstruction residual, every evidence trail is "
     "subjected to sufficiency, minimality and counterfactual-flip "
     "checks against the runner-up post, criteria in the spirit of "
     "rationale evaluation [[deyoung2020]] and formal explanation "
     "minimality [[ignatiev2019]], applied here to allocation "
     "decisions and equally to the sampled Shapley trails of black-box "
     "baselines. (3) A quantified account, on the simulated market, "
     "of what each design choice buys: the retention objective, the "
     "additive scorer, the stable assignment and the propensity "
     "correction are ablated one at a time. (4) Two findings of "
     "direct policy relevance: optimising immediate acceptance "
     "sacrifices retention among formed matches and vice versa, so "
     "the mixing weight between the two is a policy dial rather than "
     "an engineering constant; and a retention-optimal matcher "
     "rationally deprioritises the most educated applicants because "
     "village wages fall short of their expectations — an equity "
     "failure that arises precisely when the engine is working as "
     "intended, and that a single audited priority offset repairs at "
     "a measured cost."),
    ("p",
     "The remainder of this paper is organised as follows. Section 2 "
     "reviews related work. Section 3 fixes notation and reviews the "
     "components the architecture builds on. Section 4 presents RAMT. "
     "Section 5 describes the simulated micro-market, the logged "
     "behaviour policy, the baselines and the metrics. Section 6 "
     "reports matching performance, audits, ablations, distributional "
     "analysis and validity checks. Section 7 discusses deployment and "
     "limitations, and Section 8 concludes."),

    # =====================================================================
    ("h1", "Related Work"),
    ("p",
     "The engine sits at the intersection of four literatures: digital "
     "technology in rural revitalisation, learned person-job matching, "
     "two-sided market design, and interpretable machine learning "
     "under algorithmic accountability."),
    ("h2", "Digital Technology and the Rural Youth Talent Chain"),
    ("p",
     "Province-level panels associate rural digital-economy "
     "development with composite revitalisation outcomes "
     "[[liu2024digital]], and conceptual work maps where generative AI "
     "can enter the countryside's organisational, industrial and "
     "talent processes [[liu2025gai]]. The talent link is the least "
     "automated. Studies of returnee entrepreneurship identify who "
     "returns and who succeeds: migrant work experience shifts "
     "returnees toward transformational rather than subsistence "
     "ventures [[ding2025migrant]], local embeddedness and bridging "
     "networks condition survival in marginal regions "
     "[[wang2022returnee]], and large questionnaire studies decompose "
     "the entrepreneurial capability of returning workers "
     "[[lu2023ability]]. The distributional stakes are documented "
     "too: whether rural e-commerce narrows or widens local income "
     "gaps has been shown to turn on where its gains concentrate "
     "[[liu2023ecom]]. What this literature does not contain is an "
     "allocation mechanism: given profiles and posts, who should go "
     "where. That is the gap this paper addresses, and the recent "
     "field-experimental finding that algorithmic assistance upstream "
     "of hiring shifts real labour-market outcomes [[wiles2025]] "
     "argues that the allocation layer deserves the same scrutiny."),
    ("h2", "Learned Person-Job Matching"),
    ("p",
     "Neural person-job fit models score resume-post pairs with "
     "hierarchical attention and its successors [[qin2020]], and "
     "e-recruitment recommendation has accumulated a survey-scale "
     "literature of its own [[mashayekhi2024]]. Industrial retrieval "
     "rests on two-tower architectures trained on logged engagement "
     "[[yi2019]], and large language models now both generate "
     "recommendations directly [[du2024]] and screen resumes — with "
     "measured intersectional bias when they do [[wilson2024]]. "
     "Vendor claims about de-biased algorithmic hiring have been "
     "examined and found wanting [[raghavan2020]]. Two properties are "
     "near-universal in this line and both are liabilities for a "
     "public talent programme: the training signal is an immediate "
     "engagement outcome rather than what became of the placement, "
     "and the scorer is a black box explained, if at all, after the "
     "fact. Both choices are reversed here."),
    ("h2", "Two-Sided Matching and Market Design"),
    ("p",
     "Deferred acceptance is the canonical mechanism for two-sided "
     "markets with capacities [[gale1962]]; its stability guarantee — "
     "no youth-post pair prefers each other to their assignment — has "
     "carried it from college admissions to residency matching and "
     "school choice [[roth2008]], [[roth1999]], "
     "[[abdulkadiroglu2003]]. Machine learning has recently entered "
     "matching markets from the learning side, with bandit learners "
     "converging to stable matchings [[jagadeesan2023]] and fairness "
     "analysed when the qualities being matched on are themselves "
     "uncertain predictions [[devic2023]]. Entropy-regularised "
     "optimal transport offers a continuous alternative to deferred "
     "acceptance for capacity-respecting assignment [[cuturi2013]], "
     "[[peyre2019]], and inverse optimal transport has been used to "
     "learn matching costs from observed matches [[li2019iot]]. RAMT "
     "uses deferred acceptance as its default allocation layer and "
     "reports the transport alternative as an ablation, because "
     "stability is an institutional virtue: an assignment that leaves "
     "obvious mutually preferred pairs unrealised invites exactly the "
     "informal side-dealing that a transparent programme is meant to "
     "replace."),
    ("h2", "Interpretable Models, Audits and Accountability"),
    ("p",
     "The case that high-stakes decisions call for models "
     "interpretable by construction rather than explained post hoc "
     "has been made forcefully [[rudin2019]], and additive models are "
     "its workhorse: generalised additive models with selective "
     "interactions match black-box accuracy on tabular problems "
     "[[lou2012]], [[lou2013]], and neural additive models carry the "
     "idea into deep learning [[agarwal2021]], with statistical "
     "foundations reviewed in [[allen2024]]. The post-hoc alternative "
     "— LIME, SHAP and their descendants [[ribeiro2016]], "
     "[[lundberg2017]] — approximates the model rather than reporting "
     "it, and the faithfulness of such explanations is itself a "
     "contested measurement problem [[jain2019]], [[deyoung2020]], "
     "[[atanasova2023]], [[lyu2024]]. Formal explanation research "
     "supplies sharper criteria — minimal sufficient reason sets "
     "computed abductively [[ignatiev2019]] and counterfactual "
     "explanations stating what would have had to differ "
     "[[wachter2018]]. On the accountability side, fairness in "
     "ranking and allocation is a mature field [[singh2018]], "
     "[[zehlike2022]], [[xu2024rank]], [[hu2024fair]], and the first "
     "years of mandated hiring-algorithm audits have been studied "
     "empirically, with sobering compliance rates [[wright2024]], "
     "[[groves2024]]. This paper's contribution to the line is to "
     "move the audit from the score to the decision: the checks in "
     "Section 4 ask whether a trail justifies the allocation "
     "actually made, against the alternative actually foregone."),

    # =====================================================================
    ("h1", "Preliminaries"),
    ("p",
     "This section fixes notation and reviews the three components on "
     "which the engine builds: two-sided matching with capacities, "
     "discrete-time survival, and learning from logged allocation "
     "data."),
    ("h2", "Problem Formulation"),
    ("p",
     "A matching round presents a set of young people "
     "$i \\in \\left[ N \\right]$, each described by a structured "
     "profile produced by the upstream generative-AI layer, and a set "
     "of village posts $j \\in \\left[ M \\right]$ with capacities "
     "$c_{j}$. An engine must output an assignment "
     "$\\mu : \\left[ N \\right] \\rightarrow \\left[ M \\right] "
     "\\cup \\left[ \\varnothing \\right]$ together with, for every "
     "assigned pair, an evidence trail. Writing $A_{ij}$ for the "
     "probability that youth $i$ accepts an offer of post $j$ and "
     "$R_{ij}$ for the probability that the formed match survives the "
     "full horizon of $T = 24$ months, the quantity the talent chain "
     "cares about is"),
    ("eq", r"\max_{\mu} \sum_{i : \mu(i) \neq \varnothing} "
           r"A_{i\mu(i)} R_{i\mu(i)} \quad \text{s.t.} \quad "
           r"| \mu^{-1}(j) | \leq c_{j}", 1),
    ("where",
     "where the summand is the probability that the offer to $i$ both "
     "forms and lasts, which we call the stay-yield of the offer. "
     "Neither $A$ nor $R$ is observable at decision time; the engine "
     "works from estimates, and the estimates come from logs."),
    ("h2", "Stability in Capacitated Matching"),
    ("p",
     "Given youth-side preferences $u_{i}(\\cdot)$ over posts and "
     "post-side priorities $s(\\cdot, j)$ over youth, an assignment "
     "$\\mu$ is stable if no youth-post pair $(i,j)$ would jointly "
     "deviate from it, that is, if no pair satisfies"),
    ("eq", r"u_{i}(j) > u_{i}(\mu(i)) \; \wedge \; "
           r"\left[ | \mu^{-1}(j) | < c_{j} \; \vee \; "
           r"s(i,j) > s_{\min}(j) \right]", 2),
    ("where",
     "where $s_{\\min}(j) = \\min_{i' \\in \\mu^{-1}(j)} s(i',j)$ is "
     "the weakest priority currently holding a seat at $j$, and "
     "$u_{i}(\\varnothing)$ is ranked below every acceptable post. "
     "Youth-proposing deferred acceptance produces a stable assignment "
     "in this sense and is strategy-proof for the proposing side "
     "[[gale1962]], [[roth2008]]. Stability is reported below as a "
     "measurable property — the rate of blocking pairs an assignment "
     "leaves — rather than assumed."),
    ("h2", "Discrete-Time Survival and Logged Data"),
    ("p",
     "Retention over a horizon observed monthly is a discrete-time "
     "survival problem [[cox1972]], [[singer1993]]: a formed match "
     "either survives month $t$ or ends in it, so a per-month hazard "
     "$h_{t}$ determines the survival probability "
     "$\\prod_{t} (1 - h_{t})$, and censored spells contribute only "
     "the months they were observed. Machine-learning survival "
     "modelling is a mature field [[katzman2018]], [[wiegrebe2024]], "
     "and employee-turnover prediction its best-studied industrial "
     "instance [[alakasheh2024]]. The complication here is that "
     "training data are logs of a historical allocation policy: "
     "outcomes exist only for matches that policy formed, so naive "
     "fitting inherits its selection. The standard correction weights "
     "each logged episode by the inverse of the probability the "
     "policy showed that pair [[swaminathan2015]], [[schnabel2016]], "
     "the counterfactual-learning machinery that also underlies "
     "doubly robust evaluation [[dudik2014]] and policy learning from "
     "observational data [[athey2021]]; long-horizon outcomes raise "
     "further identification questions of their own [[saito2024]]."),

    # =====================================================================
    ("h1", "Retention-Aware Match Tracing"),
    ("p",
     "Figure 1 shows the pipeline the engine is deployed in: the "
     "generative-AI layer turns unstructured materials into "
     "structured profiles, RAMT scores and allocates, offers go out "
     "with their evidence ledgers, low-margin cases are routed to a "
     "case worker, and observed acceptance and retention flow back "
     "as the next round's training data. Figure 2 shows the engine's "
     "internal structure, which the rest of this section walks "
     "through."),
    ("fig", "fig1"),
    ("fig", "fig2"),
    ("h2", "A Pre-Registered Feature Ledger"),
    ("p",
     "Every scored pair is described by a fixed vector of "
     "$D = 15$ person-post features"),
    ("eq", r"z(i,j) = \left( z_{1}(i,j), \ldots, z_{D}(i,j) \right)", 3),
    ("where",
     "comprising four requirement-weighted skill-fit scores (agronomy, "
     "digital commerce, operations, governance), the wage offered "
     "minus the wage expected, travel distance to the home village, "
     "mentor pairing, housing support, the youth's schooling level and "
     "return-migrant status, a home-village tie, the youth's "
     "generative-AI literacy interacted with whether the post is a "
     "digital one, and three interaction features fixed in advance on "
     "domain grounds: distance interacted with having children, "
     "village amenities interacted with having children, and mentor "
     "pairing interacted with skill shortfall. The ledger is "
     "pre-registered in the exact sense that its composition was "
     "frozen before any model was estimated and no term was added, "
     "removed or reweighted afterwards; the interaction whitelist is "
     "the entire concession the additive family makes to "
     "non-additivity, and it is declared rather than searched."),
    ("h2", "An Additive Spline Scorer with an Exact Ledger"),
    ("p",
     "Each feature passes through its own one-dimensional "
     "piecewise-linear spline, and the score is their sum. With hat "
     "functions $B_{kp}$ on quantile knots and weights $w_{kp}$,"),
    ("eq", r"f_{k}(z) = \sum_{p=1}^{P_{k}} w_{kp} B_{kp}(z) , \quad "
           r"s(i,j) = b + \sum_{k=1}^{D} f_{k}\left( z_{k} \right)", 4),
    ("where",
     "which is the classical shape of an intelligible additive model "
     "[[lou2012]], [[agarwal2021]]: flexible within each feature, "
     "additive across them, and linear in its parameters, so the "
     "training problems below are smooth and convex-like and run in "
     "CPU seconds. Defining each contribution against the "
     "population-mean reference profile $\\bar{z}$,"),
    ("eq", r"\varphi_{k}(i,j) = f_{k}\left( z_{k}(i,j) \right) - "
           r"f_{k}\left( \bar{z}_{k} \right) , \qquad s(i,j) = "
           r"b + \sum_{k=1}^{D} \varphi_{k}(i,j)", 5),
    ("where",
     "holds as an identity, not an approximation: the per-feature "
     "entries $\\varphi_{k}$ are the evidence ledger, and they "
     "reconstruct the score with zero residual because they are the "
     "score. This is the property post-hoc attribution methods "
     "estimate for black boxes [[lundberg2017]] and that comes free "
     "by construction, which is the architectural bet of the paper: "
     "Section 6 measures what, if anything, the bet costs in "
     "accuracy."),
    ("h2", "A Retention Hazard Trained Off-Policy"),
    ("p",
     "The score parameterises a discrete-time hazard with "
     "regime-block intercepts $a_{r(t)}$ for months 1–6, "
     "7–12 and 13–24,"),
    ("eq", r"h_{t}(i,j) = \sigma \left( a_{r(t)} - s(i,j) \right) , "
           r"\qquad \hat{S}(i,j) = \prod_{t=1}^{T} \left( 1 - "
           r"h_{t}(i,j) \right)", 6),
    ("where",
     "where $\\sigma$ is the logistic function; a higher score means "
     "a lower hazard in every month, so $s$ orders pairs by predicted "
     "retention while the intercepts absorb the calendar shape. The "
     "training data are logged episodes of the county's historical "
     "matching rule: pairs shown, offers accepted or declined, and "
     "for formed matches the observed months survived "
     "$m_{e}$ with a censoring flag $\\kappa_{e}$. Each episode "
     "carries the exact probability $\\pi_{e}$ with which the "
     "logging rule showed that pair, and the fitting criterion is "
     "the inverse-propensity-weighted negative log-likelihood"),
    ("eq", r"L_{\text{ret}} = - \frac{1}{\sum_{e} \omega_{e}} "
           r"\sum_{e} \omega_{e} \left[ \sum_{t=1}^{m_{e}} "
           r"\ln \left( 1 - h_{t}^{e} \right) + \left( 1 - "
           r"\kappa_{e} \right) \ln h_{m_{e}+1}^{e} \right]", 7),
    ("where",
     "with weights $\\omega_{e} = \\min(1/\\pi_{e}, W)$ and the "
     "clip $W = 20$ in the usual way "
     "[[swaminathan2015]]. Nothing in the training loop ever touches "
     "the simulator's latent process; the engine sees exactly what a "
     "county system would see, which is its own logs."),
    ("h2", "An Acceptance Head and a Mixing Dial"),
    ("p",
     "A second head with the same basis models the youth side: the "
     "probability an offer is accepted,"),
    ("eq", r"g(i,j) = \sigma \left( b_{a} + \sum_{k=1}^{D} "
           r"f_{k}^{a} \left( z_{k}(i,j) \right) \right)", 8),
    ("where",
     "trained on all logged offers by weighted logistic regression. "
     "Its score serves two roles: it supplies the youth-side "
     "preference orderings that deferred acceptance requires, and it "
     "provides the other end of a dial. Standardising both scores "
     "and mixing,"),
    ("eq", r"s_{\alpha}(i,j) = (1 - \alpha) \, \tilde{s}(i,j) + "
           r"\alpha \, \tilde{g}(i,j)", 9),
    ("where",
     "interpolates between a matcher that optimises predicted "
     "retention ($\\alpha = 0$, the engine's default) and one that "
     "optimises predicted acceptance ($\\alpha = 1$, the objective "
     "of deployed platforms). Section 6 traces the frontier and "
     "argues the choice of $\\alpha$ is a policy decision that "
     "should be taken in the open."),
    ("h2", "Assignment by Deferred Acceptance"),
    ("p",
     "Offers are formed by youth-proposing deferred acceptance: each "
     "youth proposes down their acceptance-utility ordering, each "
     "post tentatively holds its $c_{j}$ best proposals by the "
     "engine score, and displaced youth continue proposing. The "
     "outcome is stable in the sense of (2) with respect to the "
     "stated preferences $\\left( g, s \\right)$. As a continuous "
     "alternative we also evaluate an entropy-regularised transport "
     "plan [[cuturi2013]], [[peyre2019]] obtained by Sinkhorn "
     "scaling of"),
    ("eq", r"K_{ij} = \exp \left( s(i,j) / \varepsilon \right) , "
           r"\qquad u \leftarrow a / K v , \qquad v \leftarrow "
           r"b / K^{\top} u", 10),
    ("where",
     "with row masses $a$ uniform over youth, column masses $b$ "
     "proportional to capacities and the rounded plan used as an "
     "assignment. Transport fills every seat by construction; what "
     "it gives up, the ablations of Section 6 measure, is stability."),
    ("h2", "Decision-Level Audits and Abstention"),
    ("p",
     "An evidence trail should justify the decision actually taken, "
     "against the alternative actually foregone. For an assigned "
     "pair $(i, j^{*})$ with runner-up $j'$, the audited object is "
     "the ledger of the score difference, "
     "$\\Delta \\varphi_{k} = \\varphi_{k}(i, j^{*}) - "
     "\\varphi_{k}(i, j')$, and three checks are applied. "
     "Sufficiency asks whether a small set of entries carries the "
     "preference:"),
    ("eq", r"\min | \mathcal{S} | \quad \text{s.t.} \quad "
           r"\sum_{k \in \mathcal{S}} \Delta \varphi_{k} \geq "
           r"\frac{1}{2} \sum_{k=1}^{D} \Delta \varphi_{k} > 0", 11),
    ("where",
     "in the spirit of rationale sufficiency [[deyoung2020]]; "
     "minimality requires the selected set to be small in the sense "
     "of abductive explanation [[ignatiev2019]], here at most a "
     "third of the ledger; and the counterfactual-flip check "
     "neutralises the largest entry $k^{\\top}$ to the reference "
     "value and requires the recomputed margin to move as the "
     "ledger predicted:"),
    ("eq", r"\left| \Delta s_{k^{\top} \leftarrow \bar{z}} - "
           r"\left( \Delta s - \Delta \varphi_{k^{\top}} \right) "
           r"\right| \leq 0.25 \left| \Delta s \right|", 12),
    ("where",
     "which is a counterfactual criterion in the sense of "
     "[[wachter2018]]: a trail whose largest stated reason, when "
     "removed, does not move the decision by its stated share is a "
     "rationalisation rather than a reason. For the additive scorer "
     "the identity (5) makes all three checks pass mechanically; "
     "the point of running them is that the same checks can be "
     "applied to any engine whose trails are sampled Shapley "
     "attributions, which is how the black-box baselines are "
     "audited in Section 6."),
    ("p",
     "Finally, the engine declines to decide alone where its own "
     "evidence is thin. An ensemble of five hazard heads trained on "
     "bootstrap resamples yields a score dispersion for each "
     "assigned pair,"),
    ("eq", r"v(i) = \text{std}_{b} \left( s^{(b)} \left( i, \mu(i) "
           r"\right) \right)", 13),
    ("where",
     "and the most uncertain share $1 - q$ of matches is routed to "
     "human review rather than auto-approved, the selective-"
     "prediction pattern [[geifman2017]], [[hendrickx2024]] in its "
     "learning-to-defer form [[mozannar2023]]. Section 6 traces "
     "retention against coverage $q$; calibration of the underlying "
     "probabilities is checked with standard tools [[guo2017]], "
     "[[angelopoulos2023]]."),

    # =====================================================================
    ("h1", "Experimental Setup"),
    ("p",
     "To evaluate a matching engine one must know what would have "
     "happened under assignments the historical policy never made, "
     "and no administrative dataset contains that. The evaluation "
     "therefore runs on a simulated labour micro-market. The corpus "
     "is simulated; no young person and no village post described "
     "below exists, and every number in Section 6 is a property of "
     "the simulation. What discipline the exercise carries comes "
     "from three commitments: marginals anchored to published "
     "statistics, a ground-truth process deliberately outside every "
     "evaluated model family, and engines that see only what a "
     "deployed system would see — their own logs."),
    ("h2", "The Simulated Micro-Market"),
    ("p",
     "One market draw comprises 2,400 "
     "young people and 360 posts across 60 villages, with post "
     "capacities of two to eight and total capacity below demand, so "
     "allocation is genuinely competitive. Youth profiles carry age, "
     "schooling, a twelve-skill vector in four groups, digital and "
     "generative-AI literacy, wage expectation, home village, family "
     "ties and children; posts carry a category (modern agriculture, "
     "rural e-commerce, agritourism, village governance, digital "
     "agriculture), requirement profiles, wage, mentor pairing, "
     "housing support and village amenities. The education structure "
     "of the youth population follows the published schooling "
     "distribution of young rural migrant workers [[nbs2024]]; "
     "digital-literacy levels are a declared modelling shape "
     "consistent with rural internet penetration of roughly "
     "two-thirds [[cnnic2025]]; wage scales for posts and "
     "expectations sit below the published national migrant-worker "
     "average monthly wage of 4,961 CNY [[nbs2024]], which is what "
     "makes staying in the county an economic decision at all. Every "
     "remaining marginal — capacities, category shares, amenity "
     "levels, the share with children — is a stated modelling "
     "choice, and the full anchor table ships with the code."),
    ("p",
     "The ground-truth retention process is built to be unwinnable "
     "by specification. Monthly hazards switch regime at month six: "
     "in the settling-in regime, hazard is driven by the expectation "
     "shortfall, by distance interacted with children, and by a hard "
     "threshold that fires when the offered wage falls below 80 per "
     "cent of the youth's expectation; in the consolidation regime, "
     "by skill fit, community ties, amenities interacted with "
     "children, mentor pairing interacted with fit, and "
     "generative-AI literacy on digital posts. Mentorship helps "
     "misfits far more than good fits, and none of this structure — "
     "the switch, the threshold, the interactions — is in the "
     "hypothesis class of any engine below. Acceptance follows a "
     "separate two-sided utility with its own noise. A second, "
     "structurally different generator (a single smooth logistic "
     "hazard with no regimes, no threshold and no interactions) is "
     "held out for the validity checks of Section 6."),
    ("h2", "Logged Behaviour Policy"),
    ("p",
     "Engines train on logs of the administrative rule the "
     "programme is imagined to have run for four annual rounds: an "
     "eligibility filter followed by wage-rank greedy assignment, "
     "with a 15 per cent exploration rate, the kind of "
     "wage-led allocation county practice actually reports. Logging "
     f"yields {LOGG['episodes']:,} episodes per market, of which "
     f"{LOGG['formed']:,} formed matches with observed survival; "
     f"the logged acceptance rate is {f3(LOGG['accept_rate'])} and "
     f"{f3(LOGG['ret24_formed'])} of formed matches survive the "
     "24-month horizon. Every episode records the exact probability "
     "with which the rule showed that pair, which is what the "
     "propensity weights in (7) consume. No engine ever queries the "
     "generator."),
    ("h2", "Baseline Methods"),
    ("p",
     "Five comparison engines span current practice."),
    ("item", "Administrative rule: ",
     "the logging policy without exploration — eligibility screen "
     "plus wage-rank greedy fill. This is the incumbent."),
    ("item", "First-come queue: ",
     "youth in random order each take their most-preferred feasible "
     "post under the acceptance model; the floor that any "
     "coordination should beat."),
    ("item", "Platform matcher: ",
     "a two-hidden-layer neural scorer of the two-tower kind "
     "[[yi2019]] trained on offer acceptance, deployed greedily, as "
     "engagement-optimising platforms deploy them; audited post hoc "
     "with sampled Shapley values [[lundberg2017]]."),
    ("item", "Interpretable acceptance matcher: ",
     "the additive acceptance head (8) feeding deferred acceptance — "
     "identical machinery to RAMT with the objective swapped, so the "
     "comparison isolates the objective."),
    ("item", "Boosted retention matcher: ",
     "gradient-boosted shallow trees trained on 24-month retention "
     "with the same propensity weights, deployed greedily; the "
     "strongest tabular learner in the pool, audited with sampled "
     "Shapley values. A variant feeding deferred acceptance is "
     "reported in the ablations, so scorer and allocator are never "
     "confounded."),
    ("p",
     "An oracle upper bound runs deferred acceptance directly on the "
     "generator's true retention probabilities. It is not a "
     "competitor; it prices the headroom."),
    ("h2", "Metrics"),
    ("p",
     "Deployment metrics are computed exactly under the generator: "
     "offer acceptance, 24-month retention among formed matches, and "
     "the headline stay-yield per 100 offers — the expected number "
     "of offers that both form and survive the horizon, the "
     "objective in (1) scaled to a round of one hundred. Skill fit "
     "of assigned pairs, the blocking-pair rate of (2) estimated on "
     "sampled pairs against the retention-priority preferences, and "
     "an assignment-parity ratio — the assignment rate of youth with "
     "college education and above over that of the rest — complete "
     "the deployment picture. Audit metrics follow the checks of "
     "Section 4: "
     "reconstruction residual as a share of the score difference, "
     "and pass rates of the sufficiency, minimality and "
     "counterfactual-flip checks, computed on samples of assigned "
     "matches. Ranking quality of each scorer is summarised by "
     "pairwise AUC against true retention on random pairs. All "
     f"results aggregate {META['n_seeds']} independent market "
     f"replications (audits over {META['n_seeds_audit']}), reported "
     "as mean and standard deviation across markets."),
    ("h2", "Implementation Details"),
    ("p",
     "Every model, the simulator, the assignment algorithms, the "
     "audits and the boosting and neural training loops are "
     "implemented from first principles in NumPy for this study; "
     "there is no external learning framework, no GPU and no "
     "pretrained component. Spline scorers use six quantile knots "
     "per continuous feature; the platform matcher has hidden "
     "widths 24 and 12; boosting uses 120 depth-two trees; "
     "Sinkhorn uses regularisation 0.08. Deferred acceptance on a "
     f"2,400-by-360 market runs in under a second, a full market "
     "replication in about 20 CPU seconds, and the entire "
     f"experimental programme in {f1(META['runtime_s'] / 60.0)} "
     "minutes on commodity hardware. Code, seeds and the anchor "
     "table reproduce every number in this paper."),

    # =====================================================================
    ("h1", "Results and Analysis"),
    ("h2", "Matching Performance"),
    ("p",
     "Table 1 reports the deployment metrics. The incumbent "
     "administrative rule converts "
     f"{f2(m('AdminRule', 'yield100'))} of every 100 offers into "
     "matches still in place at 24 months; it offers everyone a "
     "post, but the posts are chosen by wage rank, accepted at only "
     f"{f3(m('AdminRule', 'accept'))}, and abandoned quickly. Every "
     "learned engine beats it by a wide margin, which is the "
     "cheapest finding here: almost any signal beats none. The "
     "informative comparisons are among the learned engines. RAMT "
     f"attains a stay-yield of {pm('RAMT', 'yield100', f2)} per 100 "
     f"offers — {f1(ADMIN_MULT)} times the incumbent and "
     f"{f1(ORACLE_SHARE)} per cent of the oracle ceiling of "
     f"{pm('Oracle', 'yield100', f2)} — with 24-month retention "
     f"among formed matches of {pm('RAMT', 'ret24')}, the highest "
     "of any learned engine, and a blocking-pair rate "
     "statistically indistinguishable from zero. Mean skill fit "
     "of assigned pairs is nearly flat across the pool (from "
     f"{f3(FIT_LO)} to {f3(FIT_HI)}), so no engine buys its yield "
     "by mismatching skills, and Table 1 omits the column. One baseline "
     "deserves a sentence of its own: the platform-style neural "
     "acceptance matcher, deployed greedily as such systems are, "
     f"yields {pm('MLP-Acc', 'yield100', f2)} and does not clear "
     f"the first-come floor of {pm('FCFS', 'yield100', f2)} — "
     "engagement-style ranking without coordination reproduces "
     "what an uncoordinated queue already achieves."),
    ("table", "table1"),
    ("p",
     "Two structural lessons sit inside the table. First, the "
     "objective matters exactly as the design argued: the "
     "interpretable acceptance matcher — RAMT's machinery with the "
     "objective swapped — fills slightly more seats "
     f"(acceptance {pm('Logit-Acc+DA', 'accept')} against "
     f"{pm('RAMT', 'accept')}) but holds them less well "
     f"(retention {pm('Logit-Acc+DA', 'ret24')} against "
     f"{pm('RAMT', 'ret24')}); on the stay-yield product the two "
     "land within one standard deviation of each other "
     f"({pm('Logit-Acc+DA', 'yield100', f2)} against "
     f"{pm('RAMT', 'yield100', f2)}), because forming more matches "
     "and keeping each formed match longer trade off almost "
     "exactly under this wage structure. The mixing dial of "
     "Section 6 spans the entire frontier between the two "
     "objectives, so where a county sits on it is a published "
     "policy parameter, not a property of the engine. Second, the "
     "allocator matters as much as the "
     "scorer: the boosted-tree scorer is the best ranker in the "
     f"pool (pairwise AUC {f3(AUCS['GBM-Ret'][0])} against "
     f"{f3(AUCS['RAMT'][0])} for the additive scorer) yet deployed "
     f"greedily it yields only {pm('GBM-Ret', 'yield100', f2)}, "
     "because greedy filling spends the best posts on whoever is "
     "processed first and leaves a "
     f"{f3(m('GBM-Ret', 'block'))} blocking-pair rate behind. A "
     "better prediction, allocated worse, loses; the ablations "
     "return to this."),
    ("h2", "Auditability"),
    ("p",
     "Table 2 applies the decision-level audits of Section 4 to "
     "every engine that ships a trail. For RAMT the trail is the "
     "ledger; for the black-box engines it is sampled Shapley "
     "attribution over the same features, with the same checks "
     "applied to the same decisions. The reconstruction residual "
     "is deliberately uninformative: the ledger reconstructs its "
     "score because (5) is an identity, and a permutation-sampled "
     "Shapley trail also telescopes exactly to the score "
     "difference, so every row reports zero and summing to the "
     "decision cannot separate a trail that is the computation "
     "from one that merely balances. The informative columns are "
     "the decision checks. The ledger passes the "
     f"counterfactual-flip check at "
     f"{f3(AUD['RAMT (ledger)']['flip'][0])}; the platform "
     "matcher's Shapley trail passes at "
     f"{f3(AUD['MLP-Acc (Shapley)']['flip'][0])} and the boosted "
     "retention scorer's at "
     f"{f3(AUD['GBM-Ret (Shapley)']['flip'][0])} — trails that read "
     "plausibly but, when their largest stated reason is removed, "
     "do not move the decision by the stated amount, because the "
     "underlying functions are not additive and the attribution "
     "pretends they are. An office that acted on such a trail — "
     "waiving a distance concern here, a wage top-up there — would "
     "be acting on reasons the model does not actually have."),
    ("table", "table2"),
    ("p",
     "Figure 3 shows what the ledger looks like for a single "
     "median-margin match: each bar is one feature's exact "
     "contribution to the preference for the offered post over the "
     "best alternative, and the bars sum to the score difference to "
     "machine precision. This is the artefact a case worker "
     "receives, and every claim in it is checkable against the "
     "profile fields it names."),
    ("fig", "fig3"),
    ("h2", "Ablation Study"),
    ("p",
     "Table 3 removes one design commitment at a time. Swapping the "
     "retention objective for acceptance costs "
     f"{f2(m('RAMT', 'ret24') * 100 - m('RAMT-alpha1', 'ret24') * 100)} "
     "points of 24-month retention among formed matches; replacing "
     "deferred acceptance with greedy filling collapses stay-yield "
     f"from {pm('RAMT', 'yield100', f2)} to "
     f"{pm('RAMT-greedy', 'yield100', f2)} and instability jumps "
     "two orders of magnitude, the single largest effect in the "
     "table and the clearest argument that allocation, not "
     "prediction, is where deployed systems lose most of their "
     "value. Dropping the propensity weights costs "
     f"{f2(m('RAMT', 'yield100') - m('RAMT-noIPW', 'yield100'))} "
     "points of stay-yield: the logging rule showed high-wage posts "
     "disproportionately, and a hazard fitted naively to its "
     "selection inherits the distortion. Replacing the additive "
     "splines with an unconstrained neural scorer — the "
     "interpretability bet — does not pay for itself: the black-box "
     f"variant yields {pm('RAMT-MLPscore', 'yield100', f2)} against "
     f"the additive {pm('RAMT', 'yield100', f2)}, so on logged "
     "samples of this size the inspectable model is not merely "
     "free, it is better, consistent with the tabular record of "
     "additive models [[lou2013]]. The boosted scorer fed through "
     "deferred acceptance recovers everything greedy filling had "
     f"cost it — {pm('GBM-Ret+DA', 'yield100', f2)} against the "
     f"additive {pm('RAMT', 'yield100', f2)}, a gap inside one "
     "standard deviation — which confirms once more that the "
     "allocator was the bottleneck; but it arrives without a "
     "ledger, fails the counterfactual-flip audit of Table 2, and "
     "leaves a blocking-pair rate two orders of magnitude above "
     "RAMT's, so its point of mean stay-yield buys neither "
     "stability nor an account a case worker can check. Sinkhorn "
     "transport fills every seat but gives up "
     f"{f2(m('RAMT', 'yield100') - m('RAMT-OT', 'yield100'))} "
     f"points of stay-yield ({pm('RAMT-OT', 'yield100', f2)}) and "
     "a measurable blocking-pair rate; where seat coverage "
     "outranks institutional stability, it remains a defensible "
     "alternative."),
    ("table", "table3"),
    ("h2", "Whom the Engine Leaves Behind"),
    ("p",
     "The distributional finding is the one a deploying county "
     "most needs to hear. Youth with college education and above "
     f"are assigned at {f2(m('RAMT', 'parity'))} times the rate of "
     "their less-educated peers under RAMT, and the pattern is no "
     "artefact of the proposed engine. It appears in every engine "
     "that allocates competitively on a learned objective — the "
     "acceptance-trained matcher shows it more strongly still "
     f"({f2(m('Logit-Acc+DA', 'parity'))}) — and most starkly in "
     f"the oracle itself ({f2(m('Oracle', 'parity'))}), which "
     "allocates on the true retention probabilities; the greedy "
     "engines in Table 1 sit near parity only because they never "
     "let a predicted stayer outbid anyone for a scarce seat. "
     "Better prediction makes the abandonment sharper, not "
     "milder. The "
     "mechanism is visible in the ledger: village wages cluster "
     "well below graduate expectations, the hard threshold in the "
     "settling-in regime makes a large expectation shortfall the "
     "strongest single predictor of early exit, and the engine — "
     "correctly, on its own terms — concludes that graduates will "
     "not stay and stops spending scarce good posts on them. The "
     "graduates who are assigned receive the leftovers: their "
     "matches' true retention averages "
     f"{f3(STR['RAMT']['high_edu_ret'][0])} against "
     f"{f3(STR['RAMT']['low_edu_ret'][0])} for everyone else. An "
     "optimiser told to maximise staying gives up on exactly the "
     "complex-skill applicants the talent programme was created to "
     "attract — an equity failure that emerges when the system "
     "works, not when it breaks, and a concrete instance of the "
     "general concern that fairness in matching runs through the "
     "uncertainty of the predictions themselves [[devic2023]]."),
    ("p",
     "Because the engine is a mechanism, the repair can be a "
     "mechanism too. Adding a single audited priority offset to "
     "the graduate stratum's scores — visible in every affected "
     "ledger as its own entry — and raising it until assignment "
     f"parity reaches 0.95 costs "
     f"{f2(max(0.0, (S['main']['RAMT']['yield100'][0] - FF.get('yield100', m('RAMT', 'yield100')))))} "
     "points of stay-yield per 100 offers "
     f"(from {f2(m('RAMT', 'yield100'))} to "
     f"{f2(FF.get('yield100', m('RAMT', 'yield100')))}). That is "
     "the measured price of not abandoning the graduates, and the "
     "point of an auditable engine is that a county can see the "
     "price, debate it, and pay it deliberately — or fix the wage "
     "structure that generates it, which the ledger identifies "
     "just as plainly."),
    ("h2", "Two Dials: the Objective and the Right to Decide"),
    ("p",
     "Figure 4(a) traces the mixing dial of (9). Pure acceptance "
     f"training ($\\alpha = 1$) accepts "
     f"{f3(sw_at(1.0)['accept'])} of offers but holds "
     f"{f3(sw_at(1.0)['ret24'])} of formed matches to 24 months; "
     f"pure retention training ($\\alpha = 0$) accepts "
     f"{f3(sw_at(0.0)['accept'])} and holds "
     f"{f3(sw_at(0.0)['ret24'])}. Stay-yield peaks at "
     f"$\\alpha = {sw_at(SW_BEST['alpha'])['alpha']:.2f}$ with "
     f"{f2(SW_BEST['yield100'])} per 100 offers, because forming "
     "and keeping are both necessary and neither objective alone "
     "maximises their product. There is no engineering answer to "
     "where on this frontier a county should sit — a programme "
     "judged on annual placement counts and a programme judged on "
     "settled talent want different points — and the contribution "
     "of the dial is to make the choice explicit rather than "
     "buried in a loss function."),
    ("fig", "fig4"),
    ("p",
     "Figure 4(b) traces the abstention dial. Auto-approving the "
     f"most certain half of matches yields 24-month retention of "
     f"{f3(RC[0]['ret24'])} among them, against "
     f"{f3(RC[-1]['ret24'])} at full automation: uncertainty "
     "concentrates real risk, so routing the uncertain minority "
     "to a case worker buys retention on the automated remainder "
     "while keeping a human in exactly the cases where the "
     "evidence is thin — the division of labour the "
     "learning-to-defer literature argues for [[mozannar2023]] "
     "and that employment-algorithm governance increasingly "
     "expects [[euaiact2024]], [[groves2024]]."),
    ("h2", "Validity: A Mismatched Generator and a Noisy Profiler"),
    ("p",
     "Two checks probe whether the conclusions are artefacts of "
     "the simulator. First, the entire evaluation was re-run under "
     "the held-out generator of Section 5 — a single smooth "
     "logistic hazard with none of the regime, threshold or "
     "interaction structure the engines could not represent. Table "
     "4 shows the engine ordering is preserved essentially intact "
     f"(rank correlation {f2(S['mismatched_rho'])} across the "
     "seven engines), with the two interpretable "
     "deferred-acceptance engines again at the top of the learned "
     "pool; the acceptance-trained variant gains the most under "
     "the smooth generator, which removes the hard "
     "wage-expectation cliff that made early churn expensive, and "
     "the design conclusions — allocator first, objective as a "
     "policy dial, audits only from the ledger — do not depend on "
     "which wrong model of the world generated the data. Second, "
     "the generative-AI profiling layer was corrupted by "
     "replacing each extracted field, with probability rising to "
     "certainty, by the corresponding field of another randomly "
     "drawn profile — the plausible-but-wrong error an extraction "
     "pipeline actually makes. The response is a threshold, not a "
     "slope. Stay-yield is essentially flat through 40 per cent "
     f"field error ({f2(nz_at(0.0)['ramt'])} clean against "
     f"{f2(nz_at(0.4)['ramt'])} at 0.4), because the additive "
     "scorer pools fifteen fields and deferred acceptance needs "
     "only the relative order of candidates to survive; but as "
     "corruption approaches totality RAMT falls to "
     f"{f2(nz_at(1.0)['ramt'])} — the level of the uncoordinated "
     f"queue ({f2(nz_at(1.0)['fcfs'])}) — while the acceptance "
     "matcher barely moves "
     f"({f2(nz_at(0.0)['logit'])} to {f2(nz_at(1.0)['logit'])}), "
     "because acceptance is driven by administrative fields the "
     "profiler does not have to extract — distance, wage, housing "
     "— whereas retention lives in exactly the fields it must: "
     "skills, expectations, ties. The entire advantage of "
     "retention-aware matching is purchased by the extraction "
     "layer, and a county that does not audit the profiler with "
     "the same seriousness as the matcher forfeits precisely that "
     "advantage — a concrete reading of the transparency duties "
     "the generative-AI measures already impose "
     "[[migliorini2024]]."),
    ("table", "table4"),

    # =====================================================================
    ("h1", "Discussion and Future Work"),
    ("h2", "What a County Talent Office Receives"),
    ("p",
     "The practical claim of the architecture is narrow and can be "
     "stated exactly. An office running RAMT receives, each "
     "matching round, a capacity-feasible offer list that no "
     "youth-post pair would jointly overturn; for every offer, a "
     "ledger whose entries sum to the decision and name the "
     "profile fields behind it; a short queue of low-margin cases "
     "with the reasons for the uncertainty attached; and one "
     "number — the position on the acceptance-retention frontier — "
     "that its principals chose in the open. Nothing in that "
     "bundle requires trusting a model's self-report: the ledger "
     "is the computation, the stability is checkable against the "
     "logs, and the frontier position is a published policy "
     "parameter. That is what auditable means here, and it is "
     "considerably less than trustworthy-by-assertion and "
     "considerably more than a SHAP plot appended to a black "
     "box."),
    ("h2", "The Direction of the Errors"),
    ("p",
     "The equity finding deserves restating as a general warning, "
     "because nothing about it is specific to this engine, this "
     "simulator or even this country: any allocator optimising a "
     "long-horizon outcome against a short-horizon budget will "
     "learn to abandon the applicants whose staying is expensive, "
     "and the abandonment will look, in every evaluation the "
     "optimiser is judged by, like performance. The graduates in "
     "this market are not mis-scored; they are correctly scored "
     "and therefore rationally deprioritised, and only an "
     "explicitly distributional audit surfaces it. The mandated "
     "bias audits now appearing in employment law "
     "[[wright2024]], [[groves2024]] look for disparate treatment "
     "of protected classes; the failure mode here — disparate "
     "abandonment of the policy's own target population, induced "
     "by the objective — is not in their templates, and it "
     "should be."),
    ("h2", "From a Simulated Market to a County Programme"),
    ("p",
     "The corpus is simulated, and this is a genuine limitation "
     "as well as a deliberate methodological choice. What the "
     "simulation establishes is internal: that the architecture "
     "extracts most of the achievable retention from its logs, "
     "that its audits mean what they claim, that its known "
     "failure modes have measurable prices, and that these "
     "conclusions survive a structurally different generator. "
     "What it cannot establish is external: the anchored "
     "marginals do not make the market real, the acceptance and "
     "retention processes of any actual county will differ in "
     "ways no held-out generator anticipates, and the logged "
     "propensities that the off-policy correction consumes are "
     "clean here in a way administrative records rarely are. A "
     "deployment would begin exactly where the simulation ends: "
     "run shadowed alongside the incumbent rule for one or two "
     "annual rounds, log its counterfactual offers, and let the "
     "observed gap between predicted and realised retention "
     "calibrate both the hazard and the abstention threshold "
     "before any offer follows the engine. The upstream "
     "profiling layer, represented here by a noise channel, "
     "must in deployment be evaluated as its own component, "
     "with extraction accuracy measured against hand-labelled "
     "profiles; the noise sweep bounds how much its errors cost "
     "downstream. And consequential decisions about people "
     "carry obligations no architecture discharges: consent to "
     "profiling, contestability of ledger entries, and periodic "
     "distributional audits are governance work "
     "[[euaiact2024]], [[wright2024]], not engineering "
     "residue."),
    ("h2", "Extensions"),
    ("p",
     "Three extensions follow naturally. The first is dynamic: "
     "matching rounds repeat, retention outcomes arrive with "
     "delay, and the exploration a learning matcher needs sits "
     "in tension with the stability an institution needs — the "
     "bandit-matching literature [[jagadeesan2023]] meets "
     "long-horizon off-policy evaluation [[saito2024]] exactly "
     "here. The second is the training side: the county controls "
     "not only who is matched but what training precedes the "
     "match, so the ledger's skill-shortfall entries define "
     "targeted curricula, coupling this engine to the cultivate "
     "link of the talent chain. The third is richer preference "
     "elicitation: the youth side is represented here by a "
     "fitted acceptance model, and replacing it with elicited "
     "or LLM-assisted preference structures [[du2024]] — with "
     "the profiling caveats of Section 6 — would let the "
     "stability guarantee bind to preferences the young people "
     "actually state."),

    # =====================================================================
    ("h1", "Conclusion"),
    ("p",
     "County talent programmes are beginning to allocate rural "
     "youth to village posts with learned matchers fed by "
     "generative-AI profiles, and the defaults they inherit from "
     "the recommendation stack — engagement objectives, opaque "
     "scorers, greedy allocation — are the wrong defaults for a "
     "public programme whose success is measured in years, not "
     "clicks. This paper built the opposite defaults into one "
     "engine: a pre-registered additive scorer whose evidence "
     "ledger reconstructs every decision exactly, a retention "
     "hazard trained off-policy from administrative logs, stable "
     "capacity-constrained assignment, decision-level audits, "
     "and abstention where the evidence is thin. On a simulated "
     "micro-market anchored to published statistics and governed "
     "by a deliberately mismatched ground truth, the engine "
     f"converted {f1(m('RAMT', 'yield100'))} of every 100 offers "
     "into matches still in place at two years — "
     f"{f1(ADMIN_MULT)} times the administrative wage-rank rule "
     f"and {f1(ORACLE_SHARE)} per cent of the oracle ceiling — "
     "while the audits that its ledger passes exposed the "
     "post-hoc trails of equally accurate black boxes as "
     "rationalisations."),
    ("p",
     "The findings that matter beyond the engine are the two "
     "dials and the warning. Forming matches and keeping them "
     "are different objectives whose mixture is a policy choice, "
     "and the frontier between them should be chosen in public. "
     "Deciding automatically and deferring to a case worker are "
     "different acts whose boundary should follow the evidence, "
     "not the throughput target. And a retention optimiser "
     "working exactly as intended will quietly abandon the "
     "educated returnees a talent programme most wants, at a "
     "price the ledger makes visible and a county can choose to "
     "pay. Simulated evidence cannot certify a deployment; it "
     "can, and here does, establish that an allocation engine "
     "for the rural talent chain can be accurate, stable, "
     "honest about its reasons and honest about its failures at "
     "the same time — and that none of these properties needs "
     "to be traded for another."),
]
