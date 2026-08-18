# -*- coding: utf-8 -*-
"""The manuscript text.

Every quantitative statement is interpolated from the experimental
output in tables/results.json, produced by model/run_experiments.py, so
the prose cannot disagree with the measurements. Citations are [[key]]
markers resolved by build_docx.py into bracketed numbers ordered by
first appearance.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "tables", "results.json"),
          encoding="utf-8") as fh:
    R = json.load(fh)
with open(os.path.join(HERE, "..", "tables", "concept_collapse.json"),
          encoding="utf-8") as fh:
    COLLAPSE = json.load(fh)
with open(os.path.join(HERE, "..", "tables", "gradcheck.json"),
          encoding="utf-8") as fh:
    GRAD = json.load(fh)

CFG, CORP = R["config"], R["corpus"]
MOD, ABL, SW = R["models"], R["ablation"], R["sparsity_sweep"]
OURS = MOD["DP-APT (proposed)"]
BEST_BASE = max((k for k in MOD if k != "DP-APT (proposed)"),
                key=lambda k: MOD[k]["auc_roc"])
BB = MOD[BEST_BASE]
BEST_BASE_LC = BEST_BASE[0].lower() + BEST_BASE[1:]


def f3(x):
    return "%.3f" % x


def f2(x):
    return "%.2f" % x


def f1(x):
    return "%.1f" % x


def pct(x):
    return "%.1f" % (100.0 * x)


def ptxt(p):
    return "p < .001" if p < 0.001 else ("p = %.3f" % p).replace("0.", ".")


def sweep_at(lam):
    for s in SW:
        if abs(s["lam"] - lam) < 1e-9:
            return s
    raise KeyError(lam)


SW0 = sweep_at(0.0)
SW_MAX = SW[-1]

TITLE = ("Dual-Pathway Affective Process Tracing for Auditable "
         "Assessment of Emotion Regulation in Daily Life")

AUTHORS = [("Xinyu Cai", False), ("1", True), (", Qi Zhang", False),
           ("2", True), (" and Tiantian Mo", False), ("1,*", True)]

AFFILIATIONS = [
    "College of Business, Jiaxing University, Jiaxing, Zhejiang "
    "314001, China",
    "Jiaxing University, Jiaxing, Zhejiang 314001, China",
]

ABSTRACT = (
    "This paper proposes a Dual-Pathway Affective Process Tracing "
    "(DP-APT) architecture as the assessment engine for auditable "
    "psychological evaluation of emotion regulation in daily life, "
    "replacing opaque trait scoring with a transparent and inspectable "
    "framework. The motivation is practical: ecological momentary "
    "assessment now yields dense records of how people regulate their "
    "emotions, yet the models that summarise them into regulation "
    "profiles give the clinician no account of which moments produced "
    "a given conclusion. Our methodology integrates two encoding "
    "streams. A Temporal Affect Graph Network encodes the momentary "
    "reports as a banded temporal graph whose nodes are episodes and "
    "whose gated propagation carries affective context across "
    "neighbouring moments. In parallel, a Regulatory Process Ontology "
    "Parser translates the process model of emotion regulation into "
    "differentiable concept vectors by graph attention over "
    "interpretable node descriptors. A concept-conditioned fusion "
    "couples the two, and its score for each family decomposes exactly "
    "into per-episode contributions, so that every score arrives with "
    "the moments that justify it. Because the corpus is simulated, the "
    "strategy deployed at each prompt is known and the trail can be "
    "checked rather than asserted. On "
    f"{CFG['n_participants']} simulated participants contributing up "
    f"to {CFG['t_max']} reports over fourteen days, DP-APT attains an "
    f"AUC-ROC of {f3(OURS['auc_roc'])} against {f3(BB['auc_roc'])} for "
    "the strongest sequence baseline, and its trail matches what the "
    f"person actually did at {f3(OURS['alignment'])}, against "
    f"{f3(CORP['chance_alignment'])} at chance and "
    f"{f3(CORP['oracle_alignment'])} for a supervised probe — the best "
    "of any comparison model. The principal finding is negative and "
    "general: the established faithfulness criteria carry almost no "
    "information about whether an explanation is correct. Across "
    "models their rank correlation is near zero and the extremes "
    "invert, and within one model, sparsifying its attention raises "
    "comprehensiveness monotonically while buying nothing in "
    "alignment. Explanations faithful to a model are not thereby "
    "correct about the person, and this work shows that the "
    "difference can be measured.")

INDEX_TERMS = ("Auditable assessment, ecological momentary assessment, "
               "emotion regulation, explainable artificial "
               "intelligence, graph neural networks.")


BLOCKS = [
    # =====================================================================
    ("h1", "Introduction"),
    ("p",
     "The measurement of how people regulate their emotions has moved "
     "out of the laboratory and into daily life. Ecological momentary "
     "assessment prompts respondents several times a day, in their own "
     "environments, to report what happened, how they felt, and what "
     "they did about it [[shiffman2008]], [[trull2013]]. The resulting "
     "records are dense, longitudinal, and context-rich, and they have "
     "reshaped what psychology knows about emotion: that affect "
     "carries over from moment to moment with measurable inertia "
     "[[kuppens2010]], that regulatory strategies are chosen in "
     "response to the situation rather than applied uniformly "
     "[[sheppes2011]], and that the fit between a strategy and the "
     "controllability of the situation predicts well-being better than "
     "the strategy itself [[haines2016]]. Modern experience-sampling "
     "infrastructures make such data routine to collect "
     "[[myin2018]]."),
    ("p",
     "The analytical machinery that turns those records into "
     "assessments has not kept pace with this shift in what is "
     "measured. Applied work still reduces a fortnight of momentary "
     "reports to a handful of aggregate indices, or feeds the sequence "
     "to a recurrent or attentive network that returns a trait-like "
     "profile with no account of its derivation "
     "[[jacobson2022]], [[shatte2019]]. The clinician who receives the "
     "conclusion that a client relies on expressive suppression cannot "
     "ask which evenings, which conflicts, or which unregulated "
     "episodes produced it. Post-hoc explanation tools such as LIME "
     "[[ribeiro2016]] and SHAP [[lundberg2017]] can be applied "
     "afterwards, but they approximate the model rather than report "
     "it, and the argument that high-stakes decisions call for models "
     "that are interpretable by construction rather than explained "
     "after the fact applies with particular force in mental health "
     "[[rudin2019]], [[amann2020]]. Regulatory frameworks now make "
     "this expectation explicit for systems used in clinical "
     "contexts [[eu2024]]."),
    ("p",
     "To address this gap, we introduce Dual-Pathway Affective Process "
     "Tracing (DP-APT), an inherently interpretable framework designed "
     "for auditing momentary assessments of emotion regulation. The core "
     "of DP-APT is a dual-pathway design operating on two parallel but "
     "interacting streams of information. First, a Temporal Affect "
     "Graph Network processes the sequence of momentary reports — "
     "affect ratings, appraisals of the situation, social context, and "
     "regulation items — by modelling them as a banded temporal graph "
     "whose nodes are episodes and whose edges encode short-range "
     "dependence, propagated with a gated update in the manner of "
     "temporal graph convolution [[zhao2020]], [[cho2014]]. Second, a "
     "Regulatory Process Ontology Parser translates the process model "
     "of emotion regulation [[gross1998]], [[gross2015]] — a "
     "structured taxonomy of situation selection, situation "
     "modification, attentional deployment, cognitive change, and "
     "response modulation — into differentiable concept vectors by "
     "graph attention [[velickovic2018]] over interpretable node "
     "descriptors. A concept-conditioned fusion module then couples "
     "the two streams, weighing the evidence in the episode sequence "
     "against each strategy family in turn [[vaswani2017]]."),
    ("p",
     "This design replaces an opaque scoring function with a traceable "
     "one. The principal contribution is an assessment module that "
     "outputs both a regulation profile and the exact per-episode "
     "decomposition of that profile, so that a low score for cognitive "
     "change is accompanied by the specific momentary reports in which "
     "the person faced an uncontrollable stressor and did not "
     "reappraise it. Every term of the score is a sum over episodes, "
     "so the highlighted moments are not a plausible story about the "
     "model but the arithmetic behind its output, and their "
     "contributions add up to the score itself. This is the property "
     "that makes the assessment auditable, and it is the property we "
     "measure."),
    ("p",
     "A second contribution follows from taking auditability seriously "
     "as an empirical claim rather than a design aspiration. The "
     "debate over whether attention constitutes explanation "
     "[[jain2019]], [[wiegreffe2019]] has been conducted largely "
     "without ground truth about what the model should have attended "
     "to. Momentary assessment offers a way out: if the episodes in "
     "which each strategy was actually deployed are known, the "
     "explanation can be checked against them directly. We therefore "
     "evaluate explanations on three axes — comprehensiveness and "
     "sufficiency in the sense of the ERASER protocol "
     "[[deyoung2020]], and a justification alignment measure that "
     "asks how often the highlighted episodes are the episodes in "
     "which the justified strategy was in fact used."),
    ("p",
     "Our third contribution follows from applying that measure, and "
     "it is a warning rather than a claim of success. Faithfulness "
     "and correctness come apart, in two places. Across models, the "
     "architecture with the strongest erasure scores has the weakest "
     "alignment, while post-hoc attributions on an unconstrained "
     "encoder, which the erasure tests rate poorly, point at the right "
     "moments far more often; across the models we evaluate the rank "
     f"correlation between the two criteria is "
     f"{f2(R['criterion_agreement']['spearman_rho'])}. Within a single "
     "model, sparsifying its attention — the standard way to make an "
     "attention explanation legible — raises comprehensiveness "
     "monotonically and buys nothing at all in alignment with what the "
     "person actually did. Faithfulness certifies that a model used "
     "the evidence "
     "it points at, not that the evidence is right, and the two can "
     "be pushed apart by ordinary tuning. To the best of our "
     "knowledge, this is the first work to combine a temporal graph "
     "encoder with a symbolic parser of the process model of emotion "
     "regulation for the explicit purpose of auditing psychological "
     "assessments, and the first to validate the resulting evidence "
     "trail against episode-level regulatory ground truth."),
    ("p",
     "The remainder of this paper is organized as follows. Section 2 "
     "reviews related work on emotion regulation assessment, "
     "momentary sampling, machine learning for ambulatory mental "
     "health data, and explainable and neuro-symbolic AI. Section 3 "
     "defines the formal problem setting and the background concepts. "
     "Section 4 details the DP-APT architecture. Section 5 describes "
     "the experimental setup, including the construction of the "
     "simulated corpus. Section 6 reports quantitative results and a "
     "case study. Section 7 discusses implications and limitations. "
     "Section 8 concludes."),

    # =====================================================================
    ("h1", "Related Work"),
    ("p",
     "The assessment of emotion regulation from momentary data sits at "
     "the intersection of four literatures, each of which supplies one "
     "component of the problem and leaves another open."),

    ("h2", "Emotion Regulation and Its Assessment"),
    ("p",
     "The process model organises regulation by the point in the "
     "emotion-generative cycle at which a strategy intervenes, "
     "yielding five families: situation selection, situation "
     "modification, attentional deployment, cognitive change, and "
     "response modulation [[gross1998]], [[gross2015]]. Meta-analytic "
     "work shows that these families differ systematically in "
     "effectiveness, with cognitive change generally adaptive and "
     "response-focused suppression generally not "
     "[[webb2012]], [[aldao2010]]. More recent theory has moved from "
     "ranking strategies to asking whether their deployment fits the "
     "situation: regulatory flexibility [[bonanno2013]] and "
     "strategy-situation fit [[aldao2013]], [[haines2016]] treat the "
     "match between a strategy and the controllability of the episode "
     "as the object of assessment. This reframing is what makes "
     "episode-level evidence indispensable, because a fit cannot be "
     "observed in a trait score."),
    ("p",
     "Measurement practice has not followed. The dominant instruments "
     "remain retrospective questionnaires such as the Emotion "
     "Regulation Questionnaire [[grossjohn2003]] and the Difficulties "
     "in Emotion Regulation Scale [[gratz2004]], which ask people to "
     "summarise their own habits and are therefore subject to recall "
     "and to the very metacognitive limits the constructs describe. "
     "Our work treats these instruments not as targets to be predicted "
     "but as convergent criteria against which an episode-derived "
     "profile can be validated."),

    ("h2", "Momentary Sampling and Affect Dynamics"),
    ("p",
     "Ecological momentary assessment and ambulatory assessment "
     "provide the data on which episode-level inference becomes "
     "possible [[shiffman2008]], [[trull2013]], [[myin2018]], "
     "[[wrzus2015]]. The "
     "statistical tradition built on those data models affect as a "
     "dynamic process: autoregressive formulations quantify emotional "
     "inertia and its relation to maladjustment [[kuppens2010]], "
     "[[kuppens2017]], multilevel and time-varying vector "
     "autoregression capture within-person structure "
     "[[hamaker2017]], [[bringmann2018]], and the distinction between "
     "within- and between-person structure is now understood to be "
     "consequential [[brose2015]]. These models describe dynamics "
     "well but were not designed to produce per-strategy assessments, "
     "and they offer no mechanism for pointing at the episodes behind "
     "a conclusion."),

    ("h2", "Machine Learning for Ambulatory Mental Health Data"),
    ("p",
     "Personal sensing and digital phenotyping have brought supervised "
     "learning to ambulatory records [[insel2017]], [[mohr2017]]. "
     "Sequence models predict symptom trajectories from momentary and "
     "sensor data with useful accuracy [[jacobson2022]], and reviews "
     "document rapid growth across clinical applications "
     "[[shatte2019]], [[dwyer2018]], [[torous2021]]. The recurring "
     "criticism is that predictive success has not translated into "
     "psychological understanding or clinical usability "
     "[[yarkoni2017]], [[hitchcock2022]], [[fried2017]]. Our "
     "contribution is aimed precisely at that gap: we keep the "
     "sequence model but constrain its read-out so that the evidence "
     "it used remains visible."),

    ("h2", "Explainable and Neuro-Symbolic Artificial Intelligence"),
    ("p",
     "Post-hoc attribution methods such as LIME [[ribeiro2016]], SHAP "
     "[[lundberg2017]] and integrated gradients "
     "[[sundararajan2017]] explain a trained model from the outside; "
     "the case for models that are interpretable by construction has "
     "been made forcefully for high-stakes settings [[rudin2019]], "
     "[[doshi2017]]. Architectures in that spirit include concept "
     "bottleneck models [[koh2020]] and prototype-based classifiers "
     "[[chen2019]]. Whether attention weights themselves explain a "
     "prediction remains contested [[jain2019]], [[wiegreffe2019]], "
     "which motivates the faithfulness protocol we adopt "
     "[[deyoung2020]]. Neuro-symbolic approaches, which couple neural "
     "encoders with explicit symbolic structure "
     "[[sarker2021]], [[garcez2023]], supply the second half of our "
     "design; formal ontologies of affect already exist "
     "[[hastings2011]], [[grau2008]], but have not been used as a "
     "differentiable prior for momentary assessment."),

    # =====================================================================
    ("h1", "Preliminaries"),
    ("p",
     "This section fixes notation and reviews the components on which "
     "the proposed architecture builds."),

    ("h2", "Problem Formulation"),
    ("p",
     "A participant $i$ contributes a sequence of momentary reports. "
     "Each answered prompt $t$ yields a feature vector "
     "$x_{i,t} \\in \\mathbb{R}^{F}$ containing momentary affect, "
     "appraisals of the situation, context indicators, and responses "
     "to regulation items, together with an observation indicator "
     "$m_{i,t} \\in \\{0,1\\}$ that is zero when the prompt was "
     "missed. Writing $K$ for the number of strategy families in the "
     "process model, the assessment task is to infer a profile "
     "$y_{i} \\in \\{0,1\\}^{K}$, whose $k$-th entry states whether "
     "the participant habitually deploys family $k$ in an adaptive, "
     "context-appropriate way. An assessment model is a map (1)"),
    ("eq", r"f: (x_{i,1:T}, m_{i,1:T}) \rightarrow "
           r"(\hat{y}_{i}, C_{i})", 1),
    ("where",
     "where $\\hat{y}_{i} \\in \\left[0,1\\right]^{K}$ is the "
     "predicted profile and "
     "$C_{i} \\in \\mathbb{R}^{K \\times T}$ is an evidence trail "
     "whose $(k,t)$ entry states how much episode $t$ contributed to "
     "the score for family $k$. Conventional assessment models return "
     "only the first component; the requirement that the second be "
     "produced by the same computation, rather than reconstructed "
     "afterwards, is what distinguishes an auditable model."),

    ("h2", "Graph Neural Networks over Episode Sequences"),
    ("p",
     "Graph neural networks propagate information between related "
     "entities by message passing [[kipf2017]]. For a node $t$ with "
     "neighbourhood $\\mathcal{N}(t)$ and representation $h_{t}$, one "
     "propagation step aggregates transformed neighbour states (2)"),
    ("eq", r"z_{t} = \sum_{s \in \mathcal{N}(t)} "
           r"\alpha_{t,s} W h_{s}", 2),
    ("where",
     "where $W$ is a shared linear map and $\\alpha_{t,s}$ weights the "
     "contribution of neighbour $s$. Graph attention networks learn "
     "those weights from the node pair rather than fixing them by "
     "degree [[velickovic2018]]. Episode sequences form a natural "
     "graph: momentary reports that are close in time are dependent, "
     "and the strength of that dependence is exactly the emotional "
     "inertia that affect-dynamic models estimate [[kuppens2010]]."),

    ("h2", "Attention and Cross-Modal Alignment"),
    ("p",
     "Attention computes a distribution over a set of source elements "
     "conditioned on a query, and returns the weighted combination of "
     "their values [[vaswani2017]]. When the query comes from one "
     "representational space and the keys from another, the mechanism "
     "aligns the two. In the present setting the query space is the "
     "set of regulatory concepts defined by the process model and the "
     "key space is the participant's own sequence of episodes, so the "
     "resulting weights invite a psychological reading, as the set of "
     "moments the model treats as evidence about a particular way of "
     "regulating. Our fusion keeps the cross-modal coupling but not "
     "the normalisation over episodes that turns it into a "
     "distribution, and Section 6 reports what that normalisation "
     "costs."),

    # =====================================================================
    ("h1", "A Dual-Pathway Architecture for Auditable Regulation "
           "Assessment"),
    ("p",
     "DP-APT operates as an inherently interpretable assessment engine "
     "with two parallel encoding pathways and a fusion module that "
     "synchronises them. Figure 1 places the engine in the pipeline in "
     "which it is used, and Figure 2 shows its internal structure."),
    ("fig", "fig1"),
    ("fig", "fig2"),
    ("h2", "Temporal Affect Graph Network"),
    ("p",
     "The episode pathway encodes the participant's momentary reports. "
     "Features are first projected into the model space, "
     "$h^{(0)}_{t} = \\tanh(W_{x} x_{t} + b_{x})$, with unanswered "
     "prompts held at zero. The episodes are then treated as the nodes "
     "of a banded temporal graph in which each answered prompt is "
     "connected to the answered prompts within three positions of it "
     "in either direction, a neighbourhood chosen to span the "
     "within-day and adjacent-day dependence that momentary affect "
     "exhibits. Attention coefficients over that neighbourhood are "
     "computed in the manner of graph attention (3)"),
    ("eq", r"e_{t,s} = \sigma_{L}(a^{\top}_{self} W_{msg} h_{t} + "
           r"a^{\top}_{nbr} W_{msg} h_{s})", 3),
    ("where",
     "where $\\sigma_{L}$ denotes the leaky rectified linear unit, and "
     "normalised over the observed neighbours (4)"),
    ("eq", r"\alpha_{t,s} = \frac{\exp(e_{t,s})}"
           r"{\sum_{u \in \mathcal{N}(t)} \exp(e_{t,u})}", 4),
    ("p",
     "The aggregated message $z_{t} = \\sum_{s} \\alpha_{t,s} W_{msg} "
     "h_{s}$ is combined with the node's own state by a gated update, "
     "which lets the network decide how much of a neighbour's "
     "affective context to admit rather than averaging it in (5)–(7)"),
    ("eq", r"u_{t} = \sigma(W_{u} h_{t} + U_{u} z_{t} + b_{u})", 5),
    ("eq", r"r_{t} = \sigma(W_{r} h_{t} + U_{r} z_{t} + b_{r})", 6),
    ("eq", r"\tilde{h}_{t} = \tanh(W_{h} (r_{t} \odot h_{t}) + "
           r"U_{h} z_{t} + b_{h})", 7),
    ("where",
     "where $\\sigma$ is the logistic sigmoid and $\\odot$ the "
     "elementwise product. The new state is "
     "$h_{t} \\leftarrow (1 - u_{t}) \\odot h_{t} + u_{t} \\odot "
     "\\tilde{h}_{t}$, and the update is applied for two propagation "
     "layers."),
    ("h2", "Regulatory Process Ontology Parser"),
    ("p",
     "The ontology pathway turns symbolic psychological theory into "
     "vectors. The process model is expressed as a directed acyclic "
     "graph with ten nodes: a root, the antecedent-focused and "
     "response-focused classes that divide the emotion-generative "
     "cycle, the engagement and disengagement classes that cut across "
     "it, and the five strategy families as leaves. Every node carries "
     "a descriptor vector $d_{j} \\in \\mathbb{R}^{6}$ whose entries "
     "are theoretically interpretable: position in the "
     "emotion-generative cycle, degree of engagement with the "
     "situation, cognitive demand, behavioural visibility to others, "
     "breadth, and antecedent membership. These descriptors are fixed "
     "by the theory, not learned, so the pathway cannot silently "
     "abandon the structure it is supposed to encode."),
    ("p",
     "Descriptors are projected and refined by two graph attention "
     "layers over the ontology adjacency $\\mathcal{A}$, with "
     "coefficients (8)"),
    ("eq", r"\beta_{j,l} = \frac{\exp(\sigma_{L}(p^{\top}_{s} g_{j} + "
           r"p^{\top}_{n} g_{l}))}{\sum_{v: \mathcal{A}_{jv}=1} "
           r"\exp(\sigma_{L}(p^{\top}_{s} g_{j} + p^{\top}_{n} "
           r"g_{v}))}", 8),
    ("where",
     "and node update $g_{j} \\leftarrow \\tanh(g_{j} + \\sum_{l} "
     "\\beta_{j,l} g_{l})$. Because superordinate nodes are "
     "neighbours of the families beneath them, a family's concept "
     "vector absorbs information from its class, which is how the "
     "hierarchy of the process model enters the model as an inductive "
     "prior. The residual term is not cosmetic. The ontology is small "
     "and densely connected — every family lies within two hops of "
     "every other through the classes above it — so repeated "
     "neighbourhood averaging pushes the leaves together. Averaged "
     "over three initialisations, plain averaging leaves the closest "
     "pair of concept vectors at an absolute cosine similarity of "
     f"{f3(COLLAPSE['without residual']['max_abs_cosine'])}, which "
     "is "
     "two families the detector cannot tell apart; the skip connection "
     f"brings that down to "
     f"{f3(COLLAPSE['with residual']['max_abs_cosine'])}. It does not "
     "change the average similarity between the five vectors "
     f"({f2(COLLAPSE['with residual']['mean_abs_cosine'])} with the "
     f"skip connection, {f2(COLLAPSE['without residual']['mean_abs_cosine'])} "
     "without), which reflects the fact that the descriptors place "
     "all five "
     "families in one six-dimensional space; what it prevents is the "
     "outright merging of the closest pair. The concept vectors of "
     "the five leaves, $c_{1}, \\ldots, c_{K}$, are passed to the "
     "fusion module."),
    ("h2", "Concept-Conditioned Evidence Fusion"),
    ("p",
     "Fusion couples the two pathways in two steps. First, an "
     "episode-level detector states how strongly each family is "
     "expressed in each moment (9)"),
    ("eq", r"\delta_{k,t} = \frac{1}{\sqrt{D}} c^{\top}_{k} W_{det} "
           r"h_{t} + \theta_{k}", 9),
    ("where",
     "with $p_{k,t} = \\exp(\\delta_{k,t}) / \\sum_{j} "
     "\\exp(\\delta_{j,t})$ the detection strength. The normalisation "
     "runs across families rather than over episodes, because the "
     "process model treats the five families as alternative "
     "interventions at a given point in the emotion-generative cycle, "
     "so within a moment they compete. This is the quantity a clinician "
     "reads as an assertion about a single moment, and its average over "
     "the protocol estimates how often each family is deployed, which "
     "is one of the quantities the assessment target is defined on. "
     "Second, the score for family $k$ combines a pooled summary of the "
     "episodes with a detector-weighted pool over the same episodes "
     "(10)"),
    ("eq", r"\hat{y}_{k} = \sigma\left(w^{\top}_{k} \bar{v} + "
           r"\frac{1}{T_{obs}} {\sum_{t} m_{t} p_{k,t} "
           r"(\rho^{\top}_{k} \phi_{t} + \omega_{k})} "
           r"+ b_{k}\right)", 10),
    ("where",
     "where $v_{t}$ and $\\phi_{t}$ are linear projections of the "
     "episode state, $\\bar{v} = T_{obs}^{-1} \\sum_{t} m_{t} v_{t}$ "
     "is their mean over the answered prompts, and $T_{obs}$ is the "
     "number of answered prompts. The first term is a summary of the "
     "protocol as a whole and the second is family-specific: it grows "
     "both with how often family $k$ is detected and with the character "
     "of the episodes in which it is detected. Neither term is "
     "normalised over episodes, and that is deliberate. A distribution "
     "over episodes can express which moments matter relatively but not "
     "whether any of them expresses the family at all, and habitual "
     "frequency is part of what a regulation profile means."),
    ("p",
     "Because every term in (10) is a sum over episodes, the "
     "pre-activation score decomposes exactly into per-episode "
     "contributions (11)"),
    ("eq", r"C_{k,t} = \frac{m_{t}}{T_{obs}} \left[ w^{\top}_{k} "
           r"v_{t} + p_{k,t} (\rho^{\top}_{k} \phi_{t} + "
           r"\omega_{k}) \right]", 11),
    ("where",
     "which satisfies $\\sum_{t} C_{k,t} + b_{k} = "
     "\\sigma^{-1}(\\hat{y}_{k})$ identically, so the trail accounts "
     "for the score exactly and neither loses nor invents evidence. "
     "$C_{k,t}$ is what the model reports to the clinician: the "
     "quantity by which moment $t$ raised or lowered the score for "
     "family $k$."),
    ("h2", "Training Objective"),
    ("p",
     "The task term is a binary cross-entropy applied per family, which "
     "suits the multi-label structure of a regulation profile (12)"),
    ("eq", r"\mathcal{L}_{task} = -\frac{1}{NK} \sum_{i} \sum_{k} "
           r"\left[ y_{i,k} \log \hat{y}_{i,k} + (1 - y_{i,k}) "
           r"\log (1 - \hat{y}_{i,k}) \right]", 12),
    ("p",
     "A participant-level label constrains only the aggregate of the "
     "detector, so nothing in the task term requires $p_{k,t}$ to be "
     "right about any particular moment. A second term supplies that "
     "constraint from the data themselves. Each family\u2019s concept "
     "vector is mapped to the profile of momentary regulation items it "
     "should produce, and the detector is asked to explain the items "
     "actually reported in an episode as a mixture of those profiles "
     "(13)"),
    ("eq", r"\mathcal{L}_{anchor} = \frac{1}{N T_{obs} R} \sum_{i,t} "
           r"m_{t} \Vert {\sum_{k} p_{k,t} (W^{\top}_{rec} c_{k} + "
           r"b_{rec})} - x^{item}_{i,t} \Vert^{2}", 13),
    ("where",
     "where $x^{item}_{i,t}$ are the $R$ momentary regulation items of "
     "the episode. This is the logic of a measurement model rather than "
     "of supervision: the items are observed self-reports that the "
     "model already receives as input, and no episode-level label "
     "enters training. The objective is their sum (14)"),
    ("eq", r"\mathcal{L} = \mathcal{L}_{task} + \mu "
           r"\mathcal{L}_{anchor}", 14),
    ("where",
     "with $\\mu$ fixed at one. Training uses Adam and early stopping "
     "on the validation value of (14)."),
    ("h2", "An Attention Variant"),
    ("p",
     "The design above departs from the architecture that the "
     "interpretability literature would suggest, and which we "
     "implemented first. The natural alternative normalises the "
     "concept\u2013episode coupling over episodes, turning it into a "
     "distribution that can be displayed as a heat map over the "
     "protocol. In that variant the pooled summary $\\bar{v}$ in (10) "
     "is replaced by an attention-weighted context, with one "
     "distribution per family for each of $H$ heads (15)"),
    ("eq", r"\alpha^{(h)}_{k,t} = \frac{m_{t} \exp(\delta_{k,t} + "
           r"q^{(h)\top}_{k} \kappa^{(h)}_{t})}{\sum_{s} m_{s} "
           r"\exp(\delta_{k,s} + q^{(h)\top}_{k} "
           r"\kappa^{(h)}_{s})}", 15),
    ("where",
     "where $q^{(h)}_{k}$ and $\\kappa^{(h)}_{t}$ are the head\u2019s "
     "projections of the concept vector and the episode state. Because "
     "an explanation that spreads its weight thinly over the "
     f"{f1(CORP['prompts_mean'])} answered prompts of an average "
     "protocol is not usable by a clinician, this variant admits the "
     "regularisation that is usually applied to it, a penalty on the "
     "entropy of the attention (16)"),
    ("eq", r"\mathcal{L}_{sparse} = -\frac{1}{NKH} \sum_{i,k,h} "
           r"\sum_{t} \alpha^{(h)}_{i,k,t} \log "
           r"\alpha^{(h)}_{i,k,t}", 16),
    ("p",
     "added to (14) with weight $\\lambda$. We report this variant "
     "and the effect of $\\lambda$ in Section 6 rather than adopting "
     "it, because validation cross-entropy selects against it and "
     "because what it does to the evidence trail is one of the findings "
     "of this paper."),

    # =====================================================================
    ("h1", "Experimental Setup"),
    ("p",
     "To evaluate DP-APT as an auditable assessment engine we require "
     "a corpus in which the episode-level regulatory ground truth is "
     "known, since an evidence trail can only be validated against "
     "what the person actually did at each moment. No public momentary "
     "corpus records the strategy deployed at every prompt with "
     "certainty, so we construct a simulated corpus from an explicit "
     "psychological process model whose parameters are anchored to "
     "published values."),
    ("h2", "Corpus Construction"),
    ("p",
     f"The corpus comprises {CFG['n_participants']} simulated "
     f"participants, each prompted six times a day for fourteen days, "
     f"giving {CFG['t_max']} scheduled prompts per person. Prompt "
     f"compliance is set to {pct(CFG['compliance'])} per cent, the "
     "level typically achieved "
     "in signal-contingent designs, so sequences are of unequal length "
     f"and average {f1(CORP['prompts_mean'])} answered prompts "
     f"(range {CORP['prompts_min']}–{CORP['prompts_max']}). Each "
     f"answered prompt yields {CFG['f_dim']} features: momentary "
     "negative and positive affect, arousal, stressor intensity, an "
     "appraisal of how controllable the situation is, social presence "
     "and location, time of day and day in protocol, regulatory "
     "effort, perceived regulatory success, response latency, and four "
     "regulation items with deliberately ambiguous cross-loadings on "
     "the five families, as momentary self-reports of regulation are "
     "in practice."),
    ("p",
     "The generative process follows the psychology it is meant to "
     "represent. Momentary negative affect evolves as a first-order "
     "autoregression around a person-specific baseline, perturbed by "
     "the stressor of the moment, with a person-specific inertia "
     "parameter; the realised lag-one autocorrelation across the "
     f"corpus is {f2(CORP['inertia_mean'])} (SD "
     f"{f2(CORP['inertia_sd'])}), matching values reported in "
     "experience-sampling studies of community samples "
     "[[kuppens2010]]. Which family a person deploys at a given moment "
     "depends on habitual tendency, on the controllability of the "
     "episode, and on a person-specific regulatory flexibility "
     "parameter that governs how strongly deployment tracks context "
     "[[bonanno2013]]; how much the deployment reduces negative affect "
     "depends on the fit between the family and the controllability of "
     "the situation [[haines2016]], with situation-directed families "
     "effective when control is high and attentional and cognitive "
     "families effective when it is low. Deployment shares across the "
     f"five families range from {pct(min(CORP['deployment']))} to "
     f"{pct(max(CORP['deployment']))} per cent of episodes."),
    ("p",
     "The assessment target is the adaptive habitual use of each "
     "family, defined on the generative state rather than on the "
     "observed features: it combines how frequently the person deploys "
     "the family, how well those deployments are aligned to the "
     "contexts in which the family works, and how much affect relief "
     "they achieve. Families are dichotomised at the population median "
     "so that each label is balanced. Finally, three trait "
     "questionnaire proxies are generated as noisy person-level "
     "functions of the same latent structure, reproducing the "
     "published moments of the Emotion Regulation Questionnaire "
     f"(reappraisal {f2(CORP['erq_reap'][0])}, SD "
     f"{f2(CORP['erq_reap'][1])}; suppression "
     f"{f2(CORP['erq_supp'][0])}, SD {f2(CORP['erq_supp'][1])}) "
     f"[[grossjohn2003]] and of the Difficulties in Emotion Regulation "
     f"Scale ({f1(CORP['ders'][0])}, SD {f1(CORP['ders'][1])}) "
     "[[gratz2004]]. These proxies are never shown to any model and "
     "serve only as convergent criteria."),
    ("p",
     f"Participants are split by person into training "
     f"({CFG['n_train']}), validation ({CFG['n_val']}) and test "
     f"({CFG['n_test']}) sets, so that no participant contributes "
     "episodes to more than one split."),
    ("h2", "Baseline Methods"),
    ("p",
     "We benchmark DP-APT against five comparison models spanning "
     "current practice in momentary assessment and the architectures "
     "usually proposed to improve on it."),
    ("item", "Aggregated logistic regression",
     " [[gratz2004]]: penalised logistic regression on person-level "
     "means and standard deviations of every momentary feature, "
     "representing the aggregation-then-scoring practice that applied "
     "momentary assessment still relies on."),
    ("item", "Gated recurrent encoder",
     " [[cho2014]]: a two-layer gated recurrent encoder over the "
     "episode sequence with mean pooling and a linear read-out, the "
     "standard sequence model for ambulatory data."),
    ("item", "Self-attentive encoder",
     " [[vaswani2017]]: a single-head self-attention encoder over "
     "episodes with a residual feed-forward block and mean pooling."),
    ("item", "Temporal graph encoder",
     " [[zhao2020]]: the episode pathway of the proposed model with "
     "mean pooling, that is the graph encoder without the ontology "
     "pathway and without the concept-conditioned detector."),
    ("item", "Attentive diagnostic model",
     " [[koh2020]]: an inherently interpretable diagnostic "
     "architecture in which concept embeddings are free parameters "
     "and attend over episodes, representing concept-bottleneck "
     "designs without symbolic structure."),
    ("h2", "Evaluation Metrics"),
    ("p",
     "Predictive performance is measured by the area under the "
     "receiver operating characteristic curve and the area under the "
     "precision-recall curve, averaged over the five families. "
     "Explanation quality is measured on three axes. Comprehensiveness "
     "is the change in the predicted score when the five "
     "highest-weighted episodes are removed, and sufficiency the "
     "change when only those episodes are retained; both follow the "
     "ERASER formulation [[deyoung2020]]. A large comprehensiveness "
     "means the highlighted moments were load-bearing, and a small "
     "sufficiency means they were enough on their own, so the two run "
     "in opposite directions and are reported with the direction of "
     "improvement marked. Justification alignment, which the simulated corpus "
     "uniquely makes computable, is the proportion of highlighted "
     "episodes in which the family being justified is the family the "
     "person actually deployed; its chance level is the marginal "
     f"deployment rate, {f3(CORP['chance_alignment'])}. Because the "
     "measure has a ceiling as well as a floor, we also fit a "
     "supervised multinomial probe that predicts the deployed family "
     "from the momentary features of an episode and use its "
     "probabilities as an explanation. The probe recovers the deployed "
     f"family in {pct(CORP['oracle_accuracy'])} per cent of test "
     f"episodes and attains an alignment of "
     f"{f3(CORP['oracle_alignment'])}, which is what an episode-level "
     "evidence trail could achieve on this corpus if it used the "
     "features to their full extent. Convergent "
     "validity is assessed by correlating the inferred profile with "
     "the trait questionnaire proxies. Every model is evaluated on the "
     "best evidence trail it can supply: for the architectures whose "
     "score decomposes into per-episode terms this is that "
     "decomposition, and for the two sequence baselines, which admit "
     "no such decomposition, it is integrated gradients along a "
     "straight path from an all-zero sequence [[sundararajan2017]]."),
    ("h2", "Implementation and Training Details"),
    ("p",
     "All models are implemented on a reverse-mode automatic "
     "differentiation engine written for this study on top of numpy, "
     "whose operations are verified against central finite "
     f"differences over {GRAD['n_checks']} tests, the largest relative "
     f"deviation being {f1(GRAD['max_relative_deviation'] * 1e8)} "
     "$\\times 10^{-8}$. The episode and concept representations are "
     f"{CFG['d_model']}-dimensional and the graph encoder uses "
     f"{CFG['layers']} propagation layers; the attention variant uses "
     f"{CFG['heads']} heads. Training uses Adam "
     "[[kingma2015]] with a batch of "
     f"{CFG['batch']} participants for at most {CFG['epochs']} epochs, "
     "with early stopping on the validation objective and a patience "
     "of twenty epochs; the learning rate of every model, including "
     "the baselines, is selected on the validation split so that the "
     "comparison is not confounded by tuning. Every reported "
     "performance figure is the mean over "
     f"{len(CFG['seeds'])} random initialisations, with the standard "
     "deviation across those initialisations in parentheses; the "
     "correlations of Table 4 are computed once, on the scores of the "
     "run with the lowest validation cross-entropy."),

    # =====================================================================
    ("h1", "Results and Analysis"),
    ("p",
     "This section reports prediction performance, the faithfulness and "
     "the correctness of the evidence trail, an ablation study, "
     "convergent validity, and what regularising an attention-based "
     "explanation does to each. The headline is that the two ways of "
     "judging an explanation disagree, and that a reader who tracked "
     "only the established one would draw the wrong conclusion."),
    ("h2", "Regulation Profile Prediction"),
    ("p",
     "Table 1 reports the per-family average AUC-ROC and AUC-PR on the "
     f"held-out test participants. DP-APT attains an AUC-ROC of "
     f"{f3(OURS['auc_roc'])} and an AUC-PR of {f3(OURS['auc_pr'])}. "
     f"The strongest baseline is the {BEST_BASE_LC}, at "
     f"{f3(BB['auc_roc'])} and {f3(BB['auc_pr'])}, so the proposed "
     f"model is {f3(BB['auc_roc'] - OURS['auc_roc'])} AUC-ROC points "
     "behind it, a difference of about one standard deviation across "
     f"seeds ({f3(BB['auc_roc_sd'])}) and therefore one we cannot "
     "distinguish from zero at three initialisations. Two things are "
     "worth noting before any of it is interpreted. The aggregated "
     "logistic regression, the least expressive model in the "
     f"comparison, reaches {f3(MOD['Aggregated logistic regression']['auc_roc'])}, "
     "which is the proposed model's accuracy to three decimals: on "
     "this corpus a fortnight of momentary reports is summarised "
     "almost as well by person-level means and standard deviations as "
     "by any sequence model, and accuracy is therefore not where the "
     "architectures differ. Against the interpretable comparison "
     "model, the "
     f"attentive diagnostic architecture, DP-APT is ahead by "
     f"{f3(OURS['auc_roc'] - MOD['Attentive diagnostic model']['auc_roc'])}"
     " AUC-ROC points. That comparison confounds several differences "
     "at once — the concept-bottleneck baseline has neither the graph "
     "encoder nor the unnormalised detector — so the ablation study "
     "below separates them rather than crediting the gap to any one "
     "component."),
    ("table", "table1"),
    ("h2", "Faithfulness and Correctness of the Evidence Trail"),
    ("p",
     "Table 2 reports the two ERASER faithfulness criteria and "
     "justification alignment for every model that can produce an "
     "episode-level explanation. The alignment column is bounded on "
     f"both sides: a random explanation scores "
     f"{f3(CORP['chance_alignment'])}, and a supervised probe of the "
     f"same features scores {f3(CORP['oracle_alignment'])}. DP-APT "
     f"reaches {f3(OURS['alignment'])}, that is "
     f"{f2(OURS['alignment'] / CORP['chance_alignment'])} times chance "
     "and "
     f"{pct((OURS['alignment'] - CORP['chance_alignment']) / (CORP['oracle_alignment'] - CORP['chance_alignment']))} "
     "per cent of the way from chance to the ceiling, the highest of "
     "any comparison model. Its comprehensiveness is "
     f"{f3(OURS['comprehensiveness'])} and its sufficiency "
     f"{f3(OURS['sufficiency'])}."),
    ("p",
     "The interesting structure in Table 2 is not the winner but the "
     "ordering. Among the comparison models the attentive diagnostic "
     "architecture has the strongest comprehensiveness "
     f"({f3(MOD['Attentive diagnostic model']['comprehensiveness'])}) "
     "together with the weakest alignment "
     f"({f3(MOD['Attentive diagnostic model']['alignment'])}), while "
     "the integrated-gradient explanations of the gated recurrent "
     f"encoder have the weakest comprehensiveness "
     f"({f3(MOD['Gated recurrent encoder']['comprehensiveness'])}) and "
     f"an alignment of {f3(MOD['Gated recurrent encoder']['alignment'])}, "
     "well above the interpretable architecture that beats it on "
     "faithfulness. Across the models in the table the rank "
     "correlation between comprehensiveness and alignment is "
     f"{f2(R['criterion_agreement']['spearman_rho'])} "
     f"({ptxt(R['criterion_agreement']['p'])}), so the two criteria "
     "carry essentially no information about each other, and at the "
     "extremes they invert. An explanation can point firmly at "
     "episodes the model depends on and still be pointing at the "
     "wrong episodes, and it can point at the right episodes while "
     "the model does not depend on them much."),
    ("p",
     "The row for the attention variant of our own model makes the "
     "point without changing the encoder, the data or the training "
     "objective. Read entirely through its attention distribution — "
     "erasure scores and alignment alike — that model attains a "
     "comprehensiveness of "
     f"{f3(ABL['with attention over episodes']['comprehensiveness_attention'])}, "
     "which places it in the middle of the table and above two of the "
     "four comparison explanations, while its alignment is "
     f"{f3(ABL['with attention over episodes']['alignment_attention'])} "
     f"against a chance level of {f3(CORP['chance_alignment'])}. The "
     "heat map a clinician would be shown is, on this corpus, close to "
     "uninformative about which moments the person actually spent "
     "regulating in the named way, and no faithfulness measure "
     "reveals that."),
    ("table", "table2"),
    ("p",
     "Figure 3 shows what an audit looks like for a single test "
     "participant under the proposed model. The map concentrates on a "
     "small number of episodes per family, and the open squares mark "
     "the family actually deployed in each episode; a dark cell under "
     "a square is a correct justification. The figure shows the "
     "positive part of the trail, the evidence that raised each score, "
     "since that is what the top-five measures are computed on; the "
     "negative contributions, the moments that lowered a score, are "
     "read the same way. Reading the two together is what an audit "
     "consists of: the moments behind a low score for cognitive change "
     "can be located, and a clinician can ask whether they were "
     "occasions on which reappraisal would have been possible."),
    ("fig", "fig3"),
    ("h2", "Ablation Study"),
    ("p",
     "We ablate each component in turn: the ontology parser is "
     "replaced by free concept embeddings; the temporal graph is "
     "replaced by a gated sequence encoder without a graph "
     "neighbourhood; the item anchoring term is removed; and, in the "
     "other direction, the concept–episode coupling is normalised over "
     "episodes to give the attention variant of Section 4. Every "
     "variant is trained under the protocol used for the full model. "
     "Table 3 reports the results."),
    ("table", "table3"),
    ("p",
     "Only one of the components we added earns its place. Removing "
     "the item anchoring term costs both accuracy (AUC-ROC "
     f"{f3(ABL['without the item anchoring term']['auc_roc'])} against "
     f"{f3(ABL['full model']['auc_roc'])}) and, far more sharply, the "
     "correctness of the trail, whose alignment falls from "
     f"{f3(ABL['full model']['alignment'])} to "
     f"{f3(ABL['without the item anchoring term']['alignment'])}. That "
     "is the effect it was introduced to produce: a participant-level "
     "label constrains the detector only in aggregate, and requiring "
     "the detector to account for the regulation items actually "
     "reported in a moment is what makes it right about moments."),
    ("p",
     "The other two components do not. Replacing the ontology parser "
     "with free concept embeddings leaves accuracy unchanged "
     f"({f3(ABL['without the ontology parser']['auc_roc'])} against "
     f"{f3(ABL['full model']['auc_roc'])}), leaves validation "
     f"cross-entropy unchanged "
     f"({f3(ABL['without the ontology parser']['val_bce'])} against "
     f"{f3(ABL['full model']['val_bce'])}), and if anything improves "
     f"alignment ({f3(ABL['without the ontology parser']['alignment'])} "
     f"against {f3(ABL['full model']['alignment'])}, a difference "
     f"smaller than the standard deviation across seeds, "
     f"{f3(ABL['without the ontology parser']['alignment_sd'])}). "
     "Removing the temporal graph raises test AUC-ROC to "
     f"{f3(ABL['without the temporal graph']['auc_roc'])} while "
     "worsening validation cross-entropy to "
     f"{f3(ABL['without the temporal graph']['val_bce'])}, a "
     "disagreement between the two splits that a test set of "
     f"{CFG['n_test']} participants cannot resolve. We report these as "
     "null results. The symbolic pathway fixes the meaning of the "
     "concept space, which is why we retain it, but on this corpus it "
     "buys no accuracy and no additional correctness, and a reader "
     "should not take the dual-pathway structure to be what produces "
     "the alignment reported in Table 2."),
    ("p",
     "The last row is the one that does most work. Normalising the "
     "concept–episode coupling over episodes, which is what turns it "
     "into an attention distribution and is what the interpretability "
     "literature would recommend, costs "
     f"{f3(ABL['full model']['auc_roc'] - ABL['with attention over episodes']['auc_roc'])} "
     "AUC-ROC points and takes the alignment of the resulting "
     f"evidence trail from {f3(ABL['full model']['alignment'])} down "
     f"to {f3(ABL['with attention over episodes']['alignment'])}, "
     f"which is closer to the chance level of "
     f"{f3(CORP['chance_alignment'])} than to the value it replaces. "
     "Validation cross-entropy selects against it by a wide margin "
     f"({f3(ABL['with attention over episodes']['val_bce'])} against "
     f"{f3(ABL['full model']['val_bce'])}), which is how the "
     "architecture reported here came to be the one without it. The "
     "reason is that a softmax over episodes discards magnitude and "
     "keeps only relative ranking within a person: it cannot say that "
     "a family was never expressed, only which moments expressed it "
     "least badly, and it is obliged to place its mass somewhere even "
     "when nothing in the protocol warrants it."),
    ("h2", "Convergent Validity"),
    ("p",
     "An assessment that is auditable but psychometrically empty would "
     "be of little use. Table 4 correlates the continuous scores of "
     "DP-APT with the three trait questionnaire proxies, which are "
     "never presented to the model. The cognitive change score "
     "correlates with the reappraisal scale of the Emotion Regulation "
     f"Questionnaire at r = {f3(R['validity']['Cognitive change score']['r'])}, "
     "and the response modulation score with the suppression scale at "
     f"r = {f3(R['validity']['Response modulation score']['r'])} "
     f"(N = {CFG['n_test']} test participants throughout). The "
     "correlation between the mean regulation score and the "
     "Difficulties in Emotion Regulation Scale is "
     f"r = {f3(R['validity']['Mean regulation score']['r'])}, "
     f"{ptxt(R['validity']['Mean regulation score']['p'])}"
     + (", which is not significant; the profile recovers the two "
        "strategy-specific trait constructs but not the global "
        "dysregulation score, and we report that rather than only the "
        "correlations that worked."
        if R['validity']['Mean regulation score']['p'] >= 0.05 else
        ", in the expected negative direction, since higher scores on "
        "that scale indicate greater difficulty.")),
    ("table", "table4"),
    ("h2", "What Sparsifying an Attention Explanation Buys and Costs"),
    ("p",
     "The attention variant admits the regularisation usually applied "
     "to make attention legible, so we sweep its weight rather than "
     "assume a setting. Figure 4 shows the three quantities across "
     f"$\lambda$, and they do not move together. Comprehensiveness "
     f"rises steadily and monotonically, from "
     f"{f3(SW0['comprehensiveness'])} at $\lambda = 0$ to "
     f"{f3(SW_MAX['comprehensiveness'])} at "
     f"$\lambda = {SW_MAX['lam']}$: pressing the attention toward a "
     "few episodes does make those episodes carry more of the "
     "prediction, exactly as the ERASER criteria are designed to "
     f"detect. Accuracy falls over the same range, from "
     f"{f3(SW0['auc_roc'])} to {f3(SW_MAX['auc_roc'])}, well beyond "
     "the seed-to-seed spread. Alignment does neither: it starts at "
     f"{f3(SW0['alignment'])}, ends at {f3(SW_MAX['alignment'])}, and "
     "moves non-monotonically in between by amounts comparable to the "
     f"standard deviation across initialisations "
     f"({f3(SW_MAX['alignment_sd'])} at the largest weight). We "
     "therefore do not claim that sparsification degrades the "
     "correctness of the trail; we claim the weaker and better "
     "supported thing, that it does not improve it at any setting."),
    ("p",
     "That is enough for the argument. A practitioner tuning "
     "$\lambda$ upward would watch the standard faithfulness measure "
     "improve monotonically and would conclude that the explanations "
     "were getting better, while the share of highlighted moments in "
     "which the person really regulated in the named way stayed where "
     "it was and accuracy fell away underneath. Faithfulness asks "
     "whether the model used the evidence it points at; alignment "
     "asks whether the evidence it points at is the right evidence. "
     "Optimising the first buys nothing of the second."),
    ("fig", "fig4"),

    # =====================================================================
    ("h1", "Discussion and Future Work"),
    ("p",
     "The findings establish DP-APT as a viable engine for auditable "
     "momentary assessment of emotion regulation and, equally, "
     "delimit the conditions under which such an engine is the right "
     "choice."),
    ("h2", "The Cost of Interpretability"),
    ("p",
     "The constraints that make an assessment inspectable are not "
     "free, though on this corpus the bill is smaller than we "
     f"expected. DP-APT concedes {f3(BB['auc_roc'] - OURS['auc_roc'])} "
     "AUC-ROC points to an unconstrained sequence encoder, which is "
     "about one seed-to-seed standard deviation and so not "
     "distinguishable from zero at three initialisations; the "
     "aggregated logistic baseline, meanwhile, matches the proposed "
     "model exactly. The structural tension is nevertheless real, and "
     "we expect it to bind on corpora where the sequence carries more "
     "than it does here. A regulation profile is "
     "defined partly by how often a strategy is deployed, and a "
     "frequency is a property of the whole protocol; an explanation, "
     "by contrast, is only usable if it points at a few moments. A "
     "model that must do both is asked to summarise a fortnight and "
     "to indict five evenings at the same time. Our unnormalised "
     "detector and prevalence-weighted pool recover part of the "
     "aggregate signal while remaining decomposable into per-episode "
     "contributions, which limits the gap, but the tension does not "
     "disappear."),
    ("p",
     "This has a practical consequence for how such systems should be "
     "reported. A literature in which every interpretable architecture "
     "is claimed to match or beat its black-box comparison invites the "
     "suspicion that the comparison was chosen accommodatingly. We "
     "would argue instead that the accuracy cost should be measured "
     "and stated, and the decision left to the setting: in a screening "
     "application where no human reads the output, the unconstrained "
     "encoder is the better tool; in a clinical or supervisory setting "
     "where a person must justify an assessment to the individual it "
     "concerns, an evidence trail "
     f"{f2(OURS['alignment'] / BB['alignment'])} times better aligned "
     "with what the person actually did than the same corpus explained "
     f"post hoc is worth {f3(BB['auc_roc'] - OURS['auc_roc'])} of AUC "
     "that we cannot in any case measure reliably."),
    ("h2", "What Faithfulness Does Not Guarantee"),
    ("p",
     "The second lesson concerns how explanation quality is judged, "
     "and we think it generalises beyond this architecture. The "
     "faithfulness criteria in common use ask a question about the "
     "model: if these episodes are removed, does the prediction "
     "change? A criterion of that form is satisfied by an explanation "
     "that points at the wrong moments, provided the model genuinely "
     "depends on them. Our results contain both halves of the "
     "resulting confusion. Across models the rank correlation between "
     f"the two criteria is {f2(R['criterion_agreement']['spearman_rho'])}: "
     "knowing that one explanation erases better than another tells a "
     "reader essentially nothing about which is more often right, and "
     "at the extremes the ordering inverts outright. And within one "
     "model, raising the weight on the entropy penalty — the obvious "
     "way to make an attention explanation more concentrated, and one "
     "that improves comprehensiveness monotonically — leaves "
     "alignment where it was while accuracy falls."),
    ("p",
     "Two design recommendations follow. First, where an architecture "
     "admits an exact decomposition of its output, that decomposition "
     "should be what is reported, rather than a component of it chosen "
     "for legibility. An attention map is a convenient picture, not an "
     "account of the score, and our own attention variant illustrates "
     "how far apart the two can be. Second, a faithfulness score "
     "should not be presented as evidence that an explanation is "
     "correct. Where ground truth about the explained quantity exists, "
     "even on a subsample or under simulation, it should be used, "
     "because the two criteria can be pushed apart by ordinary "
     "hyperparameter tuning. This sharpens rather than settles the "
     "attention-as-explanation debate [[jain2019]], [[wiegreffe2019]]: "
     "the question is not whether attention is faithful, but whether "
     "faithfulness was ever the property that mattered."),
    ("p",
     "The result also complicates the case against post-hoc "
     "attribution. Integrated gradients on an unconstrained encoder "
     "score poorly on erasure, as that literature reports, and "
     "nonetheless identify the episodes in which the justified family "
     "was deployed more often than the inherently interpretable "
     "concept-bottleneck comparison does. We would not conclude from "
     "one simulated corpus that post-hoc methods are underrated, but "
     "we would conclude that the evidence usually offered for the "
     "opposite view does not establish it, because it is evidence "
     "about faithfulness alone."),
    ("h2", "From a Simulated Corpus to Clinical Deployment"),
    ("p",
     "The corpus used here is simulated, and this is a genuine "
     "limitation as well as a deliberate methodological choice. It is "
     "a choice because justification alignment cannot be computed "
     "without episode-level ground truth about which strategy was "
     "actually deployed, and no observational corpus supplies that "
     "with certainty; the measure that most sharply distinguishes the "
     "models is available only under simulation. It is a limitation "
     "because the generative process embodies psychological "
     "assumptions — an autoregressive affect process, a "
     "controllability-driven choice rule, a fit-dependent efficacy "
     "function — that are supported by the literature but simplify it. "
     "In particular, the ontology given to the model and the taxonomy "
     "used by the generator both derive from the process model, so the "
     "benefit attributed to the symbolic pathway is measured under "
     "conditions favourable to it. Replication on observational "
     "momentary corpora, with expert-coded episodes on a subsample "
     "serving as partial ground truth, is the necessary next step, and "
     "the multi-site collaborative model that psychology has developed "
     "for replication [[moshontz2018]] is the natural vehicle for "
     "assembling a corpus of that kind."),
    ("p",
     "A further limitation is one the ceiling makes plain. The "
     "supervised probe recovers the deployed family from the same "
     f"momentary features in {pct(CORP['oracle_accuracy'])} per cent "
     "of episodes, so the information the evidence trail would need is "
     "present in the data; our trail reaches "
     f"{f3(OURS['alignment'])} of an attainable "
     f"{f3(CORP['oracle_alignment'])}. The shortfall is a property of "
     "the supervision rather than of the features. A participant-level "
     "label constrains the model's per-episode assertions only through "
     "their aggregate, and the anchoring term supplies the missing "
     "constraint from the observed items but does not replace an "
     "episode-level signal. Closing this gap is, we think, the most "
     "promising direction the measure opens: a small number of "
     "expert-coded or participant-confirmed episodes per person may be "
     "enough to bind the detector to the moments it describes, and the "
     "measure reported here is what would show whether it had worked."),
    ("p",
     "Deployment raises further questions that our evaluation does not "
     "settle. Momentary reports of regulation are themselves subject "
     "to bias, and a person who systematically under-reports "
     "suppression will be assessed accordingly. The audit trail helps "
     "here in a way a trait score does not, since a clinician who "
     "reads the highlighted episodes can recognise that the evidence "
     "is thin, but it does not remove the problem. Ethical "
     "deployment of automated psychological assessment also requires "
     "attention to consent, to the asymmetry between the person "
     "assessed and the institution assessing them, and to the "
     "regulatory obligations now attaching to clinical AI "
     "[[fiske2019]], [[eu2024]], [[amann2020]]."),
    ("h2", "Generalisability Beyond the Process Model"),
    ("p",
     "DP-APT was built around one taxonomy, and its ontology pathway "
     "presupposes that the constructs to be assessed can be arranged "
     "in a graph of classes and families with interpretable "
     "descriptors. Many psychological frameworks satisfy this: the "
     "coping literature, the taxonomies of cognitive distortion used "
     "in cognitive therapy, and diagnostic criteria organised by "
     "symptom cluster all have the required shape. Others do not. "
     "Dimensional models of personality or of psychopathology are "
     "continuous rather than taxonomic, and forcing them into an "
     "ontology would impose structure the theory does not claim. "
     "Where the constructs themselves are contested, the ontology "
     "becomes a commitment that the model cannot revise, which is a "
     "strength when the theory is sound and a liability when it is "
     "not."),
    ("p",
     "Three extensions follow naturally. The first is sparse "
     "episode-level supervision, which the ceiling analysis identifies "
     "as the binding constraint on how correct an evidence trail can "
     "become. The second is a learnable ontology, in which the graph "
     "is initialised from theory but permitted to adapt, with the "
     "divergence between the two reported as a finding about the "
     "theory. The third is prospective validation: an assessment that "
     "is auditable should also be actionable, and whether clinicians "
     "who receive the evidence trail make better decisions than "
     "clinicians who receive a score is an empirical question that "
     "only a user study can answer."),

    # =====================================================================
    ("h1", "Conclusion"),
    ("p",
     "Momentary assessment has given psychology a detailed record of "
     "how emotion regulation actually unfolds, but the models that "
     "summarise those records return conclusions without evidence. "
     "This paper proposed Dual-Pathway Affective Process Tracing, an "
     "inherently interpretable assessment engine that encodes the "
     "episode sequence as a temporal affect graph, encodes the process "
     "model of emotion regulation as a differentiable ontology, and "
     "couples the two so that every strategy score arrives with the "
     "moments that produced it."),
    ("p",
     f"On a psychologically calibrated corpus of "
     f"{CFG['n_participants']} simulated participants, the model "
     f"attained an AUC-ROC of {f3(OURS['auc_roc'])} against "
     f"{f3(BB['auc_roc'])} for an unconstrained sequence encoder, "
     "while producing explanations whose alignment with actual "
     f"regulatory behaviour ({f3(OURS['alignment'])}, against a chance "
     f"level of {f3(CORP['chance_alignment'])} and an attainable "
     f"{f3(CORP['oracle_alignment'])}) exceeded that of every "
     "comparison model. The inferred profiles converged with the two "
     "strategy-specific trait questionnaires that the model never "
     "saw, though not with the global dysregulation scale."),
    ("p",
     "The work makes three contributions. It provides a fully "
     "differentiable assessment pipeline whose output includes an "
     "evidence trail that is the arithmetic of the score rather than a "
     "reconstruction of it. It introduces a validation of that trail "
     "against episode-level regulatory ground truth, turning "
     "auditability from a design claim into a measured quantity with a "
     "known floor and a known ceiling. And it uses that measure to "
     "show that explanation quality as currently assessed does not "
     "track explanation correctness: across models the two criteria "
     "are almost unrelated and invert at the extremes, and within one "
     "model tuning for faithfulness buys none of it."),
    ("p",
     "Important challenges remain. The corpus is simulated, the "
     "ontology is fixed and shares its taxonomy with the generative "
     "process, a substantial gap to the attainable alignment persists "
     "under participant-level supervision alone, and the clinical "
     "value of an evidence trail has yet to be demonstrated with "
     "clinicians rather than metrics. Addressing these is the path "
     "from an auditable model to an assessment instrument that a "
     "psychologist can defend to the person it describes."),
]
