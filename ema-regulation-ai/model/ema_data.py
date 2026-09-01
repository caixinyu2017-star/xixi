# -*- coding: utf-8 -*-
"""A simulated ecological momentary assessment (EMA) corpus of emotion
regulation among primary-school pupils.

THE CORPUS IS SIMULATED. No child was sampled. It is produced by an
explicit, seeded psychological process model, because the quantity this
study evaluates — whether an assessment model's episode-level evidence
points at the moments a child actually regulated in a given way —
requires knowing the strategy deployed at every prompt, and no
observational corpus supplies that with certainty.

Design and marginal distributions are anchored to the child EMA
literature rather than invented. Values fall into two classes, and the
manuscript reports which is which:

Sourced
    *   Sampling design: four signal-contingent prompts per school day
        across twelve school days. Youth EMA studies run 2-9 prompts a
        day over 2-42 days (Wen et al., 2017), and protocols with
        primary-school children cluster at 3-4 prompts a day.
    *   Compliance 0.77, the rate reported for non-clinical child and
        adolescent samples at four to five prompts a day (Wen et al.,
        2017). Pooled youth estimates run 0.72 (Drexl et al., 2025) to
        0.78 (Wen et al., 2017); protocols restricted to children aged
        5-11 are lower and more variable.
    *   Trait proxies reproduce the Emotion Regulation Questionnaire for
        Children and Adolescents (Gullone & Taffe, 2012), which uses ten
        items on a five-point scale, six for cognitive reappraisal and
        four for expressive suppression, with reported item means of
        3.59 and 2.64.

Chosen, and identified as such
    *   The standard deviations of the two ERQ-CA subscales. The source
        reports means; the dispersions here are set to plausible values
        for a five-point scale and are not claims about the literature.
    *   Emotional inertia. The autoregressive parameter is set so that
        the realised lag-one autocorrelation of momentary negative
        affect across the corpus lands near 0.24, below the values
        reported for adolescents, on the expectation that affect is less
        inert earlier in development. Lag-one autocorrelations are
        reported for adolescent rather than late-childhood samples, so
        this is an extrapolation and the manuscript says so.
    *   The teacher-reported regulation proxy is modelled on the Emotion
        Regulation Checklist (Shields & Cicchetti, 1997), an eight-item
        four-point scale; its moments here are chosen, not sourced.

Regulatory behaviour follows the process model of emotion regulation,
which applies at this age with a developmental qualification: cognitive
change is available to children of nine to twelve but is deployed less
often and less effectively than in adults, while attentional deployment
— distraction, going to play something else — and situation
modification, which at school includes asking a teacher or a friend for
help, are the mainstays. The generator encodes that ordering.
"""
from __future__ import annotations

import numpy as np

SEED = 20260819

N_PART = 420                 # pupils in grades four to six, ages 9-12
N_DAYS = 12                  # school days of the sampling burst
N_PROMPT = 4                 # prompts per school day
T_MAX = N_DAYS * N_PROMPT    # 48 scheduled prompts
COMPLIANCE = 0.77            # non-clinical youth, 4-5 prompts/day

# The four prompts sit in the gaps of a Chinese primary-school day, which
# is what makes the protocol deliverable at all: morning break, the long
# lunch break, afternoon break, and after school.
SLOT_NAMES = ["morning break", "lunch break", "afternoon break",
              "after school"]

FAMILIES = ["Situation selection", "Situation modification",
            "Attentional deployment", "Cognitive change",
            "Response modulation"]
FAM_SHORT = ["SS", "SM", "AD", "CC", "RM"]
K_FAM = len(FAMILIES)

# Fit between a strategy family and the perceived controllability of the
# episode. Situation selection and situation modification act on the
# situation and need controllability; attentional deployment and
# cognitive change act on the child's engagement with it and are the
# strategies of choice when nothing can be changed; response modulation
# is insensitive to controllability and least effective overall.
FIT_CENTRE = np.array([0.80, 0.85, 0.25, 0.30, 0.50])
FIT_SHARP = np.array([2.6, 2.8, 2.4, 2.2, 0.8])

# Efficacy ordering is developmental. Situation modification, which here
# includes asking an adult for help, and attentional deployment are the
# effective strategies in late childhood; cognitive change is emerging
# and works less reliably than it will in adolescence; suppression is
# least effective at any age.
FAM_EFFICACY = np.array([0.48, 0.68, 0.62, 0.50, 0.26])

# Baseline propensity to deploy each family, again developmental:
# distraction and help-seeking are common, reappraisal is not yet the
# default, and suppression is comparatively rare when unprompted.
FAM_BASE = np.array([0.02, 0.22, 0.30, -0.30, -0.45])

FEATURES = [
    "negative affect", "positive affect", "feeling intensity",
    "stressor intensity", "controllability appraisal",
    "with classmates", "adult present", "time of day (sin)",
    "time of day (cos)", "day in protocol", "regulatory effort",
    "perceived regulation success", "response latency",
    "item: I sorted it out or asked someone",
    "item: I went off and thought about something else",
    "item: I told myself it was not a big deal",
    "item: I kept it in so nobody could tell",
]
F_DIM = len(FEATURES)

# Cross-loadings of the four momentary regulation items on the five
# families. The items are deliberately ambiguous indicators: a child who
# reports going off to think about something else may have removed
# herself from the situation or merely distracted herself, and no single
# item identifies a family on its own. Situation selection is identified
# only through cross-loadings, which is the hardest case.
ITEM_LOAD = np.array([
    #  SS    SM    AD    CC    RM
    [0.55, 0.85, 0.10, 0.10, 0.05],   # sorted it out or asked someone
    [0.45, 0.10, 0.85, 0.25, 0.15],   # went off, thought about something else
    [0.05, 0.15, 0.30, 0.85, 0.10],   # told myself it was not a big deal
    [0.15, 0.05, 0.20, 0.10, 0.85],   # kept it in so nobody could tell
])

# Five-point response scales throughout: children of this age use
# five-point formats more reliably than the seven-point scales of the
# adult instruments.
SCALE_MAX = 5.0


def _fit(ctrl):
    """Strategy-situation fit for each family at a controllability level."""
    return np.exp(-FIT_SHARP * (ctrl - FIT_CENTRE) ** 2)


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    n = N_PART

    # ---- person-level latent structure --------------------------------
    # Correlated habitual tendencies: the engagement-oriented families
    # load together, suppression is largely separate.
    load = np.array([
        [0.75, 0.10], [0.80, 0.05], [0.35, 0.55],
        [0.70, 0.15], [0.10, 0.80],
    ])
    common = rng.normal(size=(n, 2))
    trait = common @ load.T + 0.55 * rng.normal(size=(n, K_FAM))
    flex = 0.5 + 0.5 * (0.6 * common[:, 0] + 0.8 * rng.normal(size=n))
    flex = np.clip(flex, 0.0, 2.0)

    # Momentary negative affect on a five-point scale.
    mu_na = 2.0 + 0.42 * rng.normal(size=n) + 0.20 * (-common[:, 0])
    inertia = np.clip(0.42 + 0.10 * rng.normal(size=n), 0.02, 0.85)
    sd_na = np.clip(0.55 + 0.14 * rng.normal(size=n), 0.20, 1.1)

    X = np.zeros((n, T_MAX, F_DIM))
    mask = np.zeros((n, T_MAX), dtype=bool)
    used = np.full((n, T_MAX), -1, dtype=int)          # family deployed
    fitv = np.zeros((n, T_MAX))                        # realised fit
    succ = np.zeros((n, T_MAX))                        # regulation success

    for i in range(n):
        na = mu_na[i]
        for t in range(T_MAX):
            day = t // N_PROMPT
            slot = t % N_PROMPT
            answered = rng.random() < COMPLIANCE

            # ---- the episode. Upsets at school cluster in the unstructured
            # parts of the day, which is also when the prompts land.
            stress = np.clip(rng.beta(2.0, 3.2) + 0.08 * (slot in (0, 2)),
                             0, 1)
            ctrl = np.clip(rng.beta(2.2, 2.2), 0.02, 0.98)
            # classmates are around at school, less so after school; an
            # adult is present in class time and at home in the evening
            peers = float(rng.random() < (0.80 if slot < 3 else 0.40))
            adult = float(rng.random() < (0.45 if slot < 3 else 0.70))

            # ---- momentary negative affect: AR(1) with inertia
            na = (mu_na[i] + inertia[i] * (na - mu_na[i])
                  + 0.95 * stress + sd_na[i] * rng.normal())
            na = float(np.clip(na, 1.0, SCALE_MAX))
            pa = float(np.clip(5.4 - 0.62 * na + 0.40 * rng.normal(),
                               1.0, SCALE_MAX))
            intensity = float(np.clip(1.7 + 0.45 * na + 0.7 * stress
                                      + 0.35 * rng.normal(),
                                      1.0, SCALE_MAX))

            # ---- strategy deployment
            f = _fit(ctrl)
            logits = 1.15 * trait[i] + flex[i] * 1.8 * (f - f.mean())
            logits = logits + 0.45 * stress * np.array(
                [0.2, 0.5, 0.3, 0.4, 0.6])
            # a teacher or parent within reach makes help-seeking easy and
            # also makes a child likelier to hold the feeling in
            logits = logits + adult * np.array(
                [-0.10, 0.45, 0.0, 0.05, 0.30])
            # in front of classmates, children hide the feeling rather
            # than walk away from the group
            logits = logits + peers * np.array(
                [-0.25, -0.05, 0.10, 0.0, 0.35])
            logits = logits + FAM_BASE
            p = np.exp(logits - logits.max())
            p = p / p.sum()
            k = int(rng.choice(K_FAM, p=p))

            effort = float(np.clip(1.8 + 0.45 * stress * 3.0
                                   + 0.4 * rng.normal(), 1.0, SCALE_MAX))
            s = float(np.clip(FAM_EFFICACY[k] * f[k] * (0.6 + 0.5 * ctrl)
                              + 0.16 * rng.normal(), 0.0, 1.0))
            na = float(np.clip(na - 1.5 * s, 1.0, SCALE_MAX))
            perceived = float(np.clip(1.0 + 4.0 * s + 0.45 * rng.normal(),
                                      1.0, SCALE_MAX))
            lat = float(np.clip(np.log(rng.lognormal(2.6, 0.5)) - 2.6
                                + 0.3 * effort / SCALE_MAX, -2.0, 3.0))

            items = ITEM_LOAD[:, k] * 3.8 + 1.0 + 0.85 * rng.normal(size=4)
            items = np.clip(items, 1.0, SCALE_MAX)

            X[i, t] = [na, pa, intensity, stress, ctrl, peers, adult,
                       np.sin(2 * np.pi * slot / N_PROMPT),
                       np.cos(2 * np.pi * slot / N_PROMPT),
                       day / (N_DAYS - 1.0), effort, perceived, lat,
                       items[0], items[1], items[2], items[3]]
            mask[i, t] = answered
            used[i, t] = k
            fitv[i, t] = f[k]
            succ[i, t] = s

    # ---- person-level targets ----------------------------------------
    # Adaptive habitual use of a family combines how often the child
    # deploys it with how well its deployment is aligned to the contexts
    # in which it works, and how much the feeling actually eased. All
    # three are latent: they are computed from the generative state, not
    # from the observed features.
    adapt = np.zeros((n, K_FAM))
    for i in range(n):
        for k in range(K_FAM):
            sel = used[i] == k
            if sel.sum() < 3:
                adapt[i, k] = -1.5
                continue
            freq = sel.mean()
            align = float(np.mean(fitv[i, sel]))
            gain = float(np.mean(succ[i, sel]))
            adapt[i, k] = (1.6 * align + 1.3 * gain
                           + 0.7 * np.log(freq + 0.02))
    thr = np.quantile(adapt, 0.5, axis=0)
    Y = (adapt > thr).astype(float)

    # ---- questionnaire proxies (validation only) ----------------------
    # ERQ-CA item means are those reported for the instrument; the
    # dispersions are chosen. The teacher-reported scale is modelled on
    # the Emotion Regulation Checklist and its moments are chosen.
    z = lambda v: (v - v.mean()) / v.std()
    erq_reap = 3.59 + 0.75 * (0.78 * z(trait[:, 3]) +
                              0.63 * rng.normal(size=n))
    erq_supp = 2.64 + 0.85 * (0.80 * z(trait[:, 4]) +
                              0.60 * rng.normal(size=n))
    erc = 3.20 + 0.45 * (0.62 * z(adapt.mean(axis=1))
                         + 0.28 * z(flex) + 0.72 * rng.normal(size=n))
    quest = dict(ERQCA_reappraisal=np.clip(erq_reap, 1, 5),
                 ERQCA_suppression=np.clip(erq_supp, 1, 5),
                 ERC_teacher=np.clip(erc, 1, 4))

    # ---- standardise the momentary features on observed prompts -------
    obs = mask.reshape(-1)
    flat = X.reshape(-1, F_DIM)
    m = flat[obs].mean(axis=0)
    s = flat[obs].std(axis=0) + 1e-9
    Xz = (X - m) / s
    Xz = Xz * mask[:, :, None]

    return dict(X=Xz, X_raw=X, mask=mask, Y=Y, used=used, fit=fitv,
                success=succ, adapt=adapt, trait=trait, flex=flex,
                inertia=inertia, quest=quest,
                feature_names=FEATURES, families=FAMILIES,
                fam_short=FAM_SHORT)


def splits(n=N_PART, seed=SEED):
    """Pupil-level 70/15/15 training, validation and test split."""
    rng = np.random.default_rng(seed + 1)
    idx = rng.permutation(n)
    a, b = int(0.70 * n), int(0.85 * n)
    return idx[:a], idx[a:b], idx[b:]


if __name__ == "__main__":
    d = generate()
    X, mask, Y, used = d["X"], d["mask"], d["Y"], d["used"]
    print("pupils %d, scheduled prompts %d, features %d" % X.shape)
    print("answered prompts per pupil: mean %.1f (min %d, max %d)"
          % (mask.sum(1).mean(), mask.sum(1).min(), mask.sum(1).max()))
    print("compliance %.3f" % mask.mean())
    na = d["X_raw"][:, :, 0]
    ac = [np.corrcoef(na[i][mask[i]][:-1], na[i][mask[i]][1:])[0, 1]
          for i in range(X.shape[0])]
    print("emotional inertia %.3f (SD %.3f)" % (np.mean(ac), np.std(ac)))
    print("deployment shares %s"
          % np.round([((used == k) & mask).sum() / mask.sum()
                      for k in range(K_FAM)], 3))
    q = d["quest"]
    print("ERQ-CA reappraisal %.2f (%.2f), suppression %.2f (%.2f)"
          % (q["ERQCA_reappraisal"].mean(), q["ERQCA_reappraisal"].std(),
             q["ERQCA_suppression"].mean(), q["ERQCA_suppression"].std()))
    print("ERC teacher-reported %.2f (%.2f)"
          % (q["ERC_teacher"].mean(), q["ERC_teacher"].std()))
    print("label prevalence %s" % np.round(Y.mean(0), 2))
