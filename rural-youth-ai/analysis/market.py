# -*- coding: utf-8 -*-
"""The simulated rural labor micro-market.

THIS MODULE GENERATES SIMULATED DATA. No young person and no village post
described here exists; the corpus is a modelling instrument, and the paper
that uses it says so in the abstract and the methods. Marginal distributions
are anchored to published statistics where a published statistic exists and
are declared modelling choices where none does; the anchor table is written
out by ``describe()`` so the manuscript's corpus section is generated from
the same code that generates the corpus.

Design decisions that matter for the honesty of the evaluation:

*   The ground-truth retention process is deliberately NOT of the model
    family any evaluated engine assumes. Hazards are regime-switching
    (a settling-in regime in months 1-6 and a consolidation regime in
    months 7-24 with different drivers), contain a hard wage-expectation
    threshold, and contain multiplicative interactions (mentorship helps
    mainly when skill fit is poor; distance hurts mainly when the youth
    has school-age children). An additive scorer therefore cannot win by
    specification identity, and a mismatched-generator check re-runs the
    whole evaluation under a structurally different oracle.
*   Training data come from a logged behaviour policy (the wage-rank
    administrative matcher with epsilon exploration), never from the
    oracle. Retention outcomes are observed only for matches that were
    actually formed, which is the selection problem the engines must face.
*   Generative-AI profiling sits upstream in the deployment pipeline; its
    imperfection is represented by an explicit extraction-noise channel
    on the profile features, with a dial the experiments sweep.
"""
from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------
# skill space: four groups, twelve skills
# ---------------------------------------------------------------------------
SKILLS = [
    # agronomy and production
    "crop_husbandry", "facility_agriculture", "agri_machinery",
    # digital commerce
    "ecommerce_ops", "livestream_marketing", "brand_design",
    # operations and management
    "supply_chain", "finance_accounting", "project_management",
    # governance and community
    "grassroots_governance", "community_mediation", "cultural_tourism",
]
K = len(SKILLS)
GROUPS = {"agri": [0, 1, 2], "digital": [3, 4, 5],
          "ops": [6, 7, 8], "gov": [9, 10, 11]}

POST_CATS = ["modern_agriculture", "rural_ecommerce", "agritourism",
             "village_governance", "digital_agriculture"]
# skill emphasis of each post category over the four groups
CAT_EMPH = {
    "modern_agriculture":  {"agri": .60, "digital": .10, "ops": .20, "gov": .10},
    "rural_ecommerce":     {"agri": .10, "digital": .55, "ops": .25, "gov": .10},
    "agritourism":         {"agri": .15, "digital": .25, "ops": .30, "gov": .30},
    "village_governance":  {"agri": .10, "digital": .15, "ops": .20, "gov": .55},
    "digital_agriculture": {"agri": .35, "digital": .35, "ops": .20, "gov": .10},
}

T_HORIZON = 24          # months of observed retention
REGIME_SPLIT = 6        # settling-in months 1..6, consolidation 7..24

EDU_LEVELS = ["junior_secondary", "senior_secondary", "college", "bachelor_up"]
# anchored: education structure of rural young adults (see describe())
EDU_P = np.array([0.28, 0.34, 0.24, 0.14])


class Market:
    """One draw of the micro-market: youth, posts, and the latent oracle."""

    def __init__(self, n_youth=2400, n_posts=360, n_villages=60, seed=0,
                 oracle="regime"):
        self.rng = np.random.default_rng(seed)
        self.n, self.m, self.v = n_youth, n_posts, n_villages
        self.oracle = oracle
        self._youth()
        self._posts()

    # ------------------------------------------------------------------
    def _youth(self):
        rng, n = self.rng, self.n
        self.age = rng.integers(18, 36, n).astype(float)
        self.edu = rng.choice(4, n, p=EDU_P).astype(float)
        self.returnee = (rng.random(n) < 0.55).astype(float)
        # skills: education raises ops/digital, farm upbringing raises agri
        base = rng.beta(2.0, 3.5, (n, K))
        edu_lift = np.zeros((n, K))
        for g, idx in GROUPS.items():
            lift = {"agri": -0.02, "digital": 0.06, "ops": 0.05,
                    "gov": 0.03}[g]
            for j in idx:
                edu_lift[:, j] = lift * self.edu
        farm = rng.random(n) < 0.62
        for j in GROUPS["agri"]:
            base[:, j] += 0.18 * farm
        self.skill = np.clip(base + edu_lift, 0.0, 1.0)
        # digital / generative-AI literacy: anchored to internet penetration
        # and declared modelling shape (rises with education, falls with age)
        z = (0.45 + 0.16 * self.edu - 0.012 * (self.age - 18)
             + rng.normal(0, 0.12, n))
        self.dig = np.clip(z, 0.02, 0.98)
        self.gai = np.clip(self.dig - 0.22 + rng.normal(0, 0.08, n),
                           0.01, 0.95)
        # monthly wage expectation, thousand CNY
        self.wexp = np.clip(3.2 + 0.55 * self.edu + 0.35 * self.dig
                            + rng.normal(0, 0.55, n), 2.2, 8.5)
        self.home = rng.integers(0, self.v, n)          # home village
        self.child = (rng.random(n) < 0.31).astype(float)
        self.ties = np.clip(rng.beta(3, 2, n) + 0.10 * self.returnee, 0, 1)

    # ------------------------------------------------------------------
    def _posts(self):
        rng, m = self.rng, self.m
        self.cat = rng.choice(len(POST_CATS), m,
                              p=[0.30, 0.24, 0.16, 0.16, 0.14])
        self.village = rng.integers(0, self.v, m)
        self.cap = rng.integers(2, 9, m)                # 2..8 openings
        # requirement profile from category emphasis plus noise
        self.req = np.zeros((m, K))
        for j in range(m):
            emph = CAT_EMPH[POST_CATS[self.cat[j]]]
            for g, idx in GROUPS.items():
                for k in idx:
                    self.req[j, k] = np.clip(
                        emph[g] * 1.5 + rng.normal(0, 0.10), 0, 1)
        self.wage = np.clip(3.0 + 0.9 * (self.cat == 4) + 0.5 * (self.cat == 1)
                            + rng.normal(0, 0.6, m), 2.4, 7.5)
        self.mentor = (rng.random(m) < 0.38).astype(float)
        self.house = (rng.random(m) < 0.30).astype(float)
        # village amenity level (schooling/medical), shared by co-located posts
        vam = rng.beta(2.5, 2.5, self.v)
        self.amen = vam[self.village]
        # distance between home village and post village, in tens of km
        ang = rng.uniform(0, 2 * np.pi, self.v)
        rad = rng.uniform(0.2, 1.0, self.v)
        self.vx, self.vy = rad * np.cos(ang) * 4.0, rad * np.sin(ang) * 4.0

    def dist(self, i, j):
        """Distance (tens of km) between youth i's home and post j."""
        hv, pv = self.home[i], self.village[j]
        return np.hypot(self.vx[hv] - self.vx[pv], self.vy[hv] - self.vy[pv])

    # ------------------------------------------------------------------
    # pairwise primitives
    # ------------------------------------------------------------------
    def fit(self, i, j):
        """Requirement-weighted skill fit in [0, 1]."""
        r = self.req[j]
        return float(self.skill[i] @ r / (r.sum() + 1e-9))

    def wage_gap(self, i, j):
        return float(self.wage[j] - self.wexp[i])

    # ------------------------------------------------------------------
    # the latent oracle: acceptance and retention
    # ------------------------------------------------------------------
    def accept_prob(self, i, j):
        """Probability the youth accepts an offer of post j."""
        u = (0.9 * self.wage_gap(i, j) - 0.55 * self.dist(i, j)
             + 0.8 * self.house[j] + 0.9 * self.amen[j] * self.child[i]
             + 0.5 * self.ties[i] * (self.home[i] == self.village[j])
             + 0.4 * (self.fit(i, j) - 0.5))
        return float(1.0 / (1.0 + np.exp(-u)))

    def _hazard(self, i, j, t, style=None):
        """Monthly separation hazard of the formed match at month t."""
        style = style or self.oracle
        wg, d, f = self.wage_gap(i, j), self.dist(i, j), self.fit(i, j)
        men, am = self.mentor[j], self.amen[j]
        gai_use = self.gai[i] * (self.cat[j] in (1, 4))
        if style == "regime":
            # regime 1: settling in — expectation shock and distance dominate;
            # a hard threshold when the wage falls short of 80% of expectation
            if t <= REGIME_SPLIT:
                base = 0.055
                x = (0.050 * max(0.0, -wg)
                     + 0.030 * d * (0.5 + 1.1 * self.child[i])
                     + 0.055 * (self.wage[j] < 0.8 * self.wexp[i])
                     - 0.040 * men * (1.0 - f)      # mentorship helps misfits
                     - 0.020 * self.house[j])
            # regime 2: consolidation — embedding, growth, amenities dominate
            else:
                base = 0.028
                x = (- 0.030 * f - 0.012 * self.ties[i]
                     - 0.018 * am * (0.4 + 1.2 * self.child[i])
                     - 0.014 * gai_use - 0.008 * men * f
                     + 0.020 * max(0.0, -wg))
            return float(np.clip(base + x, 0.004, 0.60))
        # mismatched generator for the validity check: single smooth
        # logistic hazard, no regimes, no threshold, no interactions
        u = (-3.2 - 0.55 * wg + 0.28 * d - 1.3 * f - 0.35 * men
             - 0.45 * am - 0.25 * self.ties[i])
        return float(np.clip(1.0 / (1.0 + np.exp(-u)), 0.004, 0.60))

    def survive_months(self, i, j, rng, style=None):
        """Sample the number of completed months (censored at T_HORIZON)."""
        for t in range(1, T_HORIZON + 1):
            if rng.random() < self._hazard(i, j, t, style):
                return t - 1, False           # separated during month t
        return T_HORIZON, True                # retained through horizon

    def true_retention(self, i, j, style=None):
        """Exact 24-month retention probability under the oracle."""
        s = 1.0
        for t in range(1, T_HORIZON + 1):
            s *= 1.0 - self._hazard(i, j, t, style)
        return s

    # ------------------------------------------------------------------
    # logged behaviour policy: wage-rank administrative matching
    # ------------------------------------------------------------------
    def log_episodes(self, epsilon=0.15, style=None):
        """Historical matching rounds under the administrative policy.

        Youth are processed in random order; each is shown the feasible
        post with the highest wage among those with residual capacity
        (with probability epsilon a uniformly random feasible post), and
        accepts according to the oracle. Formed matches yield observed
        survival; propensities of the shown post are recorded exactly.
        """
        rng = self.rng
        order = rng.permutation(self.n)
        cap = self.cap.copy()
        rows = []
        wage_order = np.argsort(-self.wage)
        for i in order:
            feas = [j for j in wage_order if cap[j] > 0]
            if not feas:
                break
            greedy = feas[0]
            if rng.random() < epsilon:
                j = feas[int(rng.integers(len(feas)))]
            else:
                j = greedy
            # exact logging propensity of the shown post
            p_show = (1 - epsilon) * (j == greedy) + epsilon / len(feas)
            a = rng.random() < self.accept_prob(i, j)
            if a:
                months, censored = self.survive_months(i, j, rng, style)
                cap[j] -= 1
            else:
                months, censored = 0, False
            rows.append((i, j, p_show, int(a), months, int(censored)))
        return rows


# ---------------------------------------------------------------------------
# vectorised oracle matrices (identical formulas to the scalar versions;
# the scalar forms are kept because the self-tests compare the two)
# ---------------------------------------------------------------------------
def pair_matrices(mk):
    """wage gap, distance, fit as (n, m) arrays from TRUE features."""
    wg = mk.wage[None, :] - mk.wexp[:, None]
    dx = mk.vx[mk.home][:, None] - mk.vx[mk.village][None, :]
    dy = mk.vy[mk.home][:, None] - mk.vy[mk.village][None, :]
    d = np.hypot(dx, dy)
    f = mk.skill @ mk.req.T / (mk.req.sum(axis=1) + 1e-9)[None, :]
    return wg, d, f


def accept_matrix(mk):
    wg, d, f = pair_matrices(mk)
    same = (mk.home[:, None] == mk.village[None, :])
    u = (0.9 * wg - 0.55 * d + 0.8 * mk.house[None, :]
         + 0.9 * mk.amen[None, :] * mk.child[:, None]
         + 0.5 * mk.ties[:, None] * same + 0.4 * (f - 0.5))
    return 1.0 / (1.0 + np.exp(-u))


def retention_matrix(mk, style=None):
    """Exact 24-month retention probability for every pair, vectorised."""
    style = style or mk.oracle
    wg, d, f = pair_matrices(mk)
    men = mk.mentor[None, :]
    am = mk.amen[None, :]
    digital_post = np.isin(mk.cat, (1, 4)).astype(float)[None, :]
    gai_use = mk.gai[:, None] * digital_post
    child = mk.child[:, None]
    ties = mk.ties[:, None]
    house = mk.house[None, :]
    below = (mk.wage[None, :] < 0.8 * mk.wexp[:, None]).astype(float)
    surv = np.ones_like(wg)
    if style == "regime":
        x1 = (0.050 * np.maximum(0.0, -wg)
              + 0.030 * d * (0.5 + 1.1 * child) + 0.055 * below
              - 0.040 * men * (1.0 - f) - 0.020 * house)
        h1 = np.clip(0.055 + x1, 0.004, 0.60)
        x2 = (- 0.030 * f - 0.012 * ties - 0.018 * am * (0.4 + 1.2 * child)
              - 0.014 * gai_use - 0.008 * men * f
              + 0.020 * np.maximum(0.0, -wg))
        h2 = np.clip(0.028 + x2, 0.004, 0.60)
        surv = (1.0 - h1) ** REGIME_SPLIT \
            * (1.0 - h2) ** (T_HORIZON - REGIME_SPLIT)
    else:
        u = (-3.2 - 0.55 * wg + 0.28 * d - 1.3 * f - 0.35 * men
             - 0.45 * am - 0.25 * ties)
        h = np.clip(1.0 / (1.0 + np.exp(-u)), 0.004, 0.60)
        surv = (1.0 - h) ** T_HORIZON
    return surv


# ---------------------------------------------------------------------------
# the generative-AI profiling channel
# ---------------------------------------------------------------------------
def extraction_noise(mk, eta, seed=0):
    """Corrupt profile features as an imperfect extraction pipeline would.

    eta is the field error rate: with probability eta a continuous field
    is replaced by the corresponding field of another randomly drawn
    profile — a plausible but wrong extraction — and a binary field is
    flipped with probability eta. Returns a shallow copy of the market
    with corrupted OBSERVED features; the oracle keeps the true ones,
    which is the point: matching runs on what the profiling layer
    reports, outcomes follow what is actually true.
    """
    rng = np.random.default_rng(10_000 + seed)
    import copy
    obs = copy.copy(mk)
    for name in ("skill", "dig", "gai", "wexp", "ties"):
        x = getattr(mk, name).copy()
        donor = rng.integers(0, x.shape[0], x.shape[0])
        if x.ndim == 1:
            mask = rng.random(x.shape[0]) < eta
            x[mask] = x[donor][mask]
        else:
            mask = rng.random(x.shape) < eta
            x[mask] = x[donor, :][mask]
        setattr(obs, name, x)
    for name in ("returnee", "child"):
        x = getattr(mk, name).copy()
        flip = rng.random(x.shape) < eta
        x[flip] = 1 - x[flip]
        setattr(obs, name, x)
    return obs


# ---------------------------------------------------------------------------
def describe(mk):
    """Marginals with their anchors, for the corpus table in the paper."""
    rows = [
        ("youth", mk.n, "modelling choice (scale of one county cohort)"),
        ("posts / villages", "%d / %d" % (mk.m, mk.v), "modelling choice"),
        ("education shares", ", ".join("%.2f" % p for p in EDU_P),
         "anchored: census/statistical-yearbook education structure of "
         "rural young adults"),
        ("share returnees", "%.2f" % mk.returnee.mean(),
         "anchored: national returnee-entrepreneur counts (order of "
         "magnitude); exact share a modelling choice"),
        ("digital literacy mean", "%.2f" % mk.dig.mean(),
         "anchored: rural internet penetration ~66-68%"),
        ("wage expectation (kCNY)", "%.2f (%.2f)" % (mk.wexp.mean(),
                                                     mk.wexp.std()),
         "anchored: Zhejiang rural income statistics; spread a choice"),
        ("post wage (kCNY)", "%.2f (%.2f)" % (mk.wage.mean(), mk.wage.std()),
         "modelling choice consistent with the same statistics"),
        ("total capacity", int(mk.cap.sum()), "modelling choice: scarce"),
        ("share with children", "%.2f" % mk.child.mean(), "modelling choice"),
        ("mentorship share", "%.2f" % mk.mentor.mean(),
         "modelling choice informed by county mentor-pairing programmes"),
    ]
    return rows


if __name__ == "__main__":
    mk = Market(seed=1)
    print("youth %d, posts %d, capacity %d" % (mk.n, mk.m, mk.cap.sum()))
    for r in describe(mk):
        print("  %-26s %-14s %s" % (r[0], str(r[1]), r[2][:60]))
    rows = mk.log_episodes()
    acc = np.mean([r[3] for r in rows])
    kept = [r for r in rows if r[3]]
    ret = np.mean([r[4] >= T_HORIZON for r in kept])
    print("logged episodes %d, acceptance %.3f, 24m retention of formed "
          "matches %.3f" % (len(rows), acc, ret))
    # oracle sanity: mentorship should matter more for poor fits
    i = 0
    fits = sorted(range(mk.m), key=lambda j: mk.fit(i, j))
    lo, hi = fits[5], fits[-5]
    for j, tag in ((lo, "poor fit"), (hi, "good fit")):
        base = mk.true_retention(i, j)
        mk.mentor[j] = 1 - mk.mentor[j]
        alt = mk.true_retention(i, j)
        mk.mentor[j] = 1 - mk.mentor[j]
        print("  mentor toggle at %s: |delta retention| = %.3f"
              % (tag, abs(alt - base)))
