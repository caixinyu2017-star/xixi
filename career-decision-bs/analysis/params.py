# -*- coding: utf-8 -*-
"""The parameter registry.

Every quantity the model uses is declared here once, with the interval over
which the sensitivity analysis varies it and an explicit statement of where
the value came from:

    "literature"  a value stated in, or computed from, a cited source
    "calibrated"  chosen so that the simulated cross-section reproduces a
                  published statistic, with that statistic named
    "assumed"     a modelling choice, not obtained from any source

No value is silently promoted between categories. The parameter appendix of
the manuscript is generated from this registry, so the table in the paper
cannot disagree with the values the code used.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Param:
    name: str
    value: float
    unit: str
    low: float
    high: float
    provenance: str
    source: str

    def __post_init__(self):
        assert self.provenance in ("literature", "calibrated", "assumed")
        assert self.low <= self.value <= self.high, self.name


_REG: dict[str, Param] = {}
_OVERRIDE: dict[str, float] = {}


def add(name, value, unit, low, high, provenance, source):
    assert name not in _REG, "duplicate parameter %s" % name
    _REG[name] = Param(name, value, unit, low, high, provenance, source)


def v(name):
    if name in _OVERRIDE:
        return _OVERRIDE[name]
    if name not in _REG:
        raise KeyError("undeclared parameter %r" % name)
    return _REG[name].value


class override:
    def __init__(self, mapping):
        for k in mapping:
            if k not in _REG:
                raise KeyError("cannot override undeclared parameter %r" % k)
        self.mapping = dict(mapping)

    def __enter__(self):
        self.saved = dict(_OVERRIDE)
        _OVERRIDE.update(self.mapping)
        return self

    def __exit__(self, *exc):
        _OVERRIDE.clear()
        _OVERRIDE.update(self.saved)
        return False


def table():
    return [_REG[k] for k in sorted(_REG)]


def sweepable():
    return [p for p in table() if p.high > p.low]


def counts():
    c = {"literature": 0, "calibrated": 0, "assumed": 0}
    for p in _REG.values():
        c[p.provenance] += 1
    return c


# ===========================================================================
# 1. Exploration effort
# ===========================================================================
add("expl_intercept", -0.40, "logit", -1.20, 0.40, "assumed",
    "Baseline propensity to engage in career exploration in a given week, "
    "before the influence of self-efficacy, uncertainty or anxiety.")

add("expl_efficacy", 1.60, "logit per unit", 0.40, 3.20, "assumed",
    "Increase in exploration effort per unit of career decision-making "
    "self-efficacy. Positive by the central claim of social cognitive career "
    "theory, that efficacy beliefs drive goal-directed activity; the "
    "magnitude is a modelling choice.")

add("expl_uncertainty", 0.90, "logit per unit", 0.20, 1.80, "assumed",
    "Increase in exploration effort per unit of unresolved career "
    "uncertainty: not knowing is itself a motive to look.")

add("expl_anxiety", 1.30, "logit per unit", 0.40, 2.40, "assumed",
    "Reduction in exploration effort per unit of career anxiety, "
    "representing avoidance of the decision situation.")

# ===========================================================================
# 2. Information yield of exploration
# ===========================================================================
add("yield_rate", 0.22, "share of uncertainty per unit effort", 0.10, 0.40,
    "assumed",
    "Fraction of remaining uncertainty that a full week of exploration would "
    "resolve for a person under no anxiety.")

add("anxiety_interference", 0.55, "share lost per unit anxiety", 0.20, 0.85,
    "assumed",
    "Degradation of the information yield of exploration per unit of "
    "anxiety. This is the attentional-control-theory pathway: anxiety "
    "consumes processing resources, so the same amount of looking returns "
    "less usable information.")

add("uncertainty_drift", 0.020, "units per week", 0.005, 0.045, "assumed",
    "Rate at which career uncertainty regenerates as options, requirements "
    "and self-knowledge change, in the absence of exploration.")

# ===========================================================================
# 3. Self-efficacy updating
# ===========================================================================
add("efficacy_learning", 0.16, "per week", 0.06, 0.32, "assumed",
    "Speed with which career decision-making self-efficacy moves towards the "
    "level implied by recent experience of exploration.")

add("efficacy_attribution", 0.75, "share", 0.20, 1.00, "assumed",
    "Share of an episode of progress that the young person attributes to "
    "their own agency when they did the exploring themselves. Values below "
    "one represent incomplete self-attribution of success.")

# ===========================================================================
# 4. Anxiety dynamics
# ===========================================================================
add("trait_anxiety_mean", 0.45, "units", 0.10, 1.00, "assumed",
    "Population mean of the stable, dispositional component of career "
    "anxiety. Separating a stable component from a state component is what "
    "allows the model to reproduce the persistence of career anxiety over an "
    "academic year that the test-retest literature reports.")

add("anxiety_learning", 0.14, "per week", 0.05, 0.30, "assumed",
    "Speed with which anxiety moves towards the level implied by current "
    "uncertainty and self-efficacy.")

add("anxiety_from_uncertainty", 1.05, "units per unit", 0.50, 1.80, "assumed",
    "Anxiety generated per unit of unresolved uncertainty, before deadline "
    "weighting.")

add("anxiety_from_efficacy", 0.60, "units per unit", 0.05, 1.40, "assumed",
    "Reduction in anxiety per unit of career decision-making self-efficacy.")

add("deadline_slope", 1.30, "multiplier over the horizon", 1.00, 2.40,
    "assumed",
    "Factor by which the anxiety generated by a given level of uncertainty "
    "grows between the start and the end of the decision horizon, "
    "representing the approach of graduation.")

# ===========================================================================
# 5. Parental career involvement
# ===========================================================================
add("support_intensity", 0.45, "units", 0.00, 1.00, "assumed",
    "Overall level of parental career involvement in the population, on the "
    "scale of the exploration variable.")

add("support_responsiveness", 0.00, "units per unit of difficulty", 0.00, 1.60,
    "assumed",
    "Degree to which parents increase their involvement in response to the "
    "young person's visible distress and lack of progress. At zero, "
    "involvement is exogenous. Above zero it is partly a consequence of the "
    "difficulty it is later used to predict, which is the competing "
    "explanation of the reported moderation and is tested against the "
    "substitution account in Section 4.")

add("substitution_share", 0.55, "share", 0.00, 1.00, "assumed",
    "Share of parental involvement that acts in place of the young person's "
    "own exploration rather than supporting it. This is the parameter the "
    "study varies to reproduce and explain the reported moderation anomaly.")

add("support_reassurance", 0.35, "units per unit", 0.00, 0.90, "assumed",
    "Direct reduction in the state component of career anxiety per unit of "
    "parental involvement. This is the emotional-support function of "
    "involvement, which operates whether or not the involvement also "
    "substitutes for the young person's own exploration, and it is why "
    "support can be reassuring and still be counterproductive.")

add("heterogeneity", 0.35, "share of each coefficient", 0.00, 0.90, "assumed",
    "Between-person standard deviation of the individual coefficients, as a "
    "share of their population value. Young people differ in how strongly "
    "anxiety interferes with their thinking and in how much they explore; "
    "without that variation the model produces associations far stronger "
    "than any observed in this literature.")

add("scaffold_gain", 0.55, "multiplier", 0.05, 2.00, "assumed",
    "Increase in the information yield of the young person's own exploration "
    "per unit of scaffolding support.")

add("support_pressure", 0.60, "multiplier per unit", 0.00, 1.60, "assumed",
    "Increase in the weight that unresolved uncertainty carries in generating "
    "anxiety, per unit of directive parental involvement. Directive "
    "involvement does not only take the decision over; it attaches an "
    "expectation to it, so the same objective uncertainty is experienced as "
    "more threatening. This is the channel through which involvement can "
    "amplify rather than buffer the link between anxiety and difficulty, and "
    "the model required it: a version carrying only the reassurance and "
    "substitution channels produced buffering only.")

add("substitute_yield", 0.55, "share of own yield", 0.15, 1.00, "assumed",
    "Uncertainty resolved by substituting support, per unit of that support, "
    "relative to what the young person's own exploration would resolve.")

# ===========================================================================
# 5b. Conflict between the young person's own preference and the endorsed one
# ===========================================================================
add("divergence_mean", 0.45, "units", 0.15, 0.80, "assumed",
    "Average distance between the option a young person comes to prefer "
    "through their own exploration and the option their family endorses. "
    "Zero would mean families and children always want the same thing.")

add("divergence_sd", 0.25, "units", 0.10, 0.45, "assumed",
    "Between-family variation in that distance.")

add("assertion_efficacy", 0.85, "units per unit", 0.30, 1.40, "assumed",
    "Contribution of career decision-making self-efficacy to the capacity to "
    "hold one's own position against a family preference.")

add("assertion_anxiety", 0.70, "units per unit", 0.20, 1.30, "assumed",
    "Reduction in that capacity per unit of career anxiety. An anxious young "
    "person can hold a preference and still be unable to act on it against "
    "family expectation.")

add("conflict_weight", 0.55, "share of measured difficulty", 0.10, 1.00,
    "assumed",
    "Weight of unresolved conflict, relative to missing information, in the "
    "measured difficulty score. Instruments in this field score both, since "
    "career decision-making difficulty covers lack of information and "
    "internal and external conflict alike.")

# ===========================================================================
# 6. Population and horizon
# ===========================================================================
add("weeks", 30.0, "weeks", 16.0, 44.0, "assumed",
    "Length of the modelled decision horizon, about one academic year.")

add("sd_trait_anxiety", 0.55, "units", 0.30, 0.85, "assumed",
    "Between-person standard deviation of the initial anxiety level.")

add("sd_trait_efficacy", 0.55, "units", 0.30, 0.85, "assumed",
    "Between-person standard deviation of the initial self-efficacy level.")

add("process_noise", 0.055, "units per week", 0.010, 0.120, "assumed",
    "Standard deviation of the weekly idiosyncratic shock to uncertainty and "
    "to self-efficacy. It represents everything that moves a young person's "
    "career situation from week to week and that the model does not "
    "represent: a chance conversation, an internship rejection, a course "
    "that turns out to suit them.")

add("measurement_error", 0.06, "share of variance", 0.04, 0.12, "literature",
    "Share of observed variance that is measurement error. Bounded by the "
    "composite reliabilities Pan and He report for the four scales in their "
    "407-student sample — .947, .949, .957 and .901 — which imply error "
    "variance shares between about .04 and .10. Fixing this from the "
    "published reliabilities stops the calibration from buying fit with "
    "implausibly unreliable measurement.")
