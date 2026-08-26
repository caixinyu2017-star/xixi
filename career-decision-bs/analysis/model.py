# -*- coding: utf-8 -*-
"""A dynamic model of youth career decision-making.

The model treats career indecision not as the end of a causal chain but as the
resting state of a feedback loop. Four quantities evolve together over the
weeks of a decision horizon for each simulated young person:

    u   unresolved uncertainty about career fit, in [0, 1]
    s   career decision-making self-efficacy, in [0, 1]
    a   career anxiety, in [0, 2]
    e   career exploration effort in the current week, in [0, 1]

and they are coupled as follows.

Exploration effort rises with self-efficacy and with unresolved uncertainty
and falls with anxiety, which is the avoidance term:

    e_t = sigmoid(b0 + b_s s_t + b_u u_t - b_a a_t)

The INFORMATION YIELD of that effort is degraded by anxiety. This is the
attentional-control pathway: an anxious person who spends an hour looking at
career options extracts less usable information from that hour, because part
of the processing capacity is taken up by the worry itself. Scaffolding
support from parents raises the yield of the young person's own looking:

    kappa_t = kappa0 (1 + g c) (1 - phi a_t)

Uncertainty falls with the information actually obtained, from the young
person's own exploration and, separately, from parental involvement that
substitutes for it, and regenerates at a slow drift rate:

    u_{t+1} = u_t (1 - (own_t + sub_t)) + delta

Self-efficacy is where substitution does its damage. Efficacy moves towards
the recent PRODUCTIVITY OF THE YOUNG PERSON'S OWN AGENCY: how much of the
progress was theirs, and how well their own effort converted into information.
Parental involvement that resolves uncertainty on the young person's behalf
lowers the first of those without touching the second, so uncertainty falls
while efficacy does not rise:

    own_share_t = own_t / (own_t + sub_t)
    s*_t        = own_share_t (1 - phi a_t)(1 + g c)
    s_{t+1}     = s_t + alpha (s*_t - s_t)

Anxiety moves towards the level implied by current uncertainty, weighted by an
approaching deadline, less the reassurance of self-efficacy:

    a*_t    = lambda_t rho u_t - sigma s_t
    a_{t+1} = a_t + eta (a*_t - a_t)

The loop is closed: anxiety lowers both the amount and the yield of
exploration, low yield lowers self-efficacy, low self-efficacy lowers
exploration further, and the uncertainty that results sustains the anxiety.

Nothing here is estimated from data. The model is a set of stated equations
evaluated at the parameters declared in params.py.
"""
from __future__ import annotations

import numpy as np

import params as P

EPS = 1e-9


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40, 40)))


def simulate(n=407, seed=20260826, weeks=None, support=None, substitution=None,
             record=False):
    """Run the model for n young people. Returns the final state, and the
    weekly trajectories when record is set."""
    rng = np.random.default_rng(seed)
    T = int(P.v("weeks") if weeks is None else weeks)
    supp = P.v("support_intensity") if support is None else support
    pi = P.v("substitution_share") if substitution is None else substitution

    b0, bs, bu, ba = (P.v("expl_intercept"), P.v("expl_efficacy"),
                      P.v("expl_uncertainty"), P.v("expl_anxiety"))
    het = P.v("heterogeneity")
    reassure = P.v("support_reassurance")
    pressure = P.v("support_pressure")
    k0, phi0, delta = (P.v("yield_rate"), P.v("anxiety_interference"),
                       P.v("uncertainty_drift"))
    alpha, attrib = P.v("efficacy_learning"), P.v("efficacy_attribution")
    eta, rho, sigma = (P.v("anxiety_learning"), P.v("anxiety_from_uncertainty"),
                       P.v("anxiety_from_efficacy"))
    dslope = P.v("deadline_slope")
    gain, subyield = P.v("scaffold_gain"), P.v("substitute_yield")

    # Parental involvement varies between families; its split into scaffolding
    # and substituting parts is the quantity the study manipulates.
    c_base = np.clip(supp + 0.30 * rng.normal(size=n), 0.0, 2.0)
    c_tot = c_base.copy()
    responsive = P.v("support_responsiveness")

    # People differ in the strength of the pathways, not only in their
    # starting values. A single set of coefficients applied to everyone makes
    # the model far more deterministic than the phenomenon.
    def vary(x):
        return np.clip(x * (1.0 + het * rng.normal(size=n)), 0.0, None)

    ba_i, bs_i, bu_i = vary(ba), vary(bs), vary(bu)
    phi = np.clip(vary(phi0), 0.0, 1.2)

    # How far the option the young person comes to prefer sits from the one
    # the family endorses. It only bites once they have explored enough to
    # have a preference of their own, and only where involvement is directive.
    divergence = np.clip(P.v("divergence_mean")
                         + P.v("divergence_sd") * rng.normal(size=n), 0.0, 1.5)
    # scaffold and substitute are recomputed each week when involvement
    # responds to the young person's situation

    # Career anxiety is modelled as a stable dispositional component plus a
    # state component that responds to the current situation. Without the
    # stable part the loop always unwinds and no one remains undecided, which
    # is not what the field observes.
    trait_a = np.clip(P.v("trait_anxiety_mean")
                      + P.v("sd_trait_anxiety") * rng.normal(size=n), 0.0, 1.6)
    u = np.clip(0.78 + 0.12 * rng.normal(size=n), 0.10, 1.0)
    s = np.clip(0.45 + P.v("sd_trait_efficacy") * 0.30 * rng.normal(size=n),
                0.02, 1.0)
    state_a = np.zeros(n)
    a = np.clip(trait_a + state_a, 0.0, 2.0)

    traj = {k: np.zeros((T + 1, n)) for k in ("u", "s", "a", "e")} if record else None
    if record:
        traj["u"][0], traj["s"][0], traj["a"][0] = u, s, a

    expl_sum = np.zeros(n)
    own_progress = np.zeros(n)
    conflict = np.zeros(n)
    for t in range(T):
        lam = 1.0 + (dslope - 1.0) * (t / max(T - 1, 1))

        # Parents who watch their child struggle tend to step in. When this
        # is switched on, involvement is partly a consequence of the very
        # difficulty it will later be used to predict.
        if responsive > 0:
            c_tot = np.clip(c_base + responsive * (u - 0.5) + 0.25 * responsive * a,
                            0.0, 2.5)
        scaffold = c_tot * (1.0 - pi)
        substitute = c_tot * pi

        e = sigmoid(b0 + bs_i * s + bu_i * u - ba_i * a)
        expl_sum += e

        kappa = k0 * (1.0 + gain * scaffold) * np.clip(1.0 - phi * a, 0.0, 1.0)
        own = np.clip(e * kappa, 0.0, 0.85)
        sub = np.clip(substitute * subyield * k0, 0.0, 0.85)
        total = np.clip(own + sub, 0.0, 0.90)

        own_share = own / (own + sub + EPS)
        s_star = np.clip(attrib * own_share
                         * np.clip(1.0 - phi * a, 0.0, 1.0)
                         * (1.0 + gain * scaffold), 0.0, 1.0)
        # Directive involvement raises the weight that unresolved uncertainty
        # carries: the decision now also carries someone else's expectation.
        lam_i = lam * (1.0 + pressure * substitute)
        state_star = np.clip(lam_i * rho * u - sigma * s - reassure * c_tot,
                             -1.0, 2.0)

        nz = P.v("process_noise")
        u = np.clip(u * (1.0 - total) + delta + nz * rng.normal(size=n),
                    0.02, 1.0)
        s = np.clip(s + alpha * (s_star - s) + nz * rng.normal(size=n),
                    0.0, 1.0)
        state_a = state_a + eta * (state_star - state_a)
        a = np.clip(trait_a + state_a, 0.0, 2.0)

        # Conflict: a preference of one's own, an endorsed alternative, and
        # too little standing to reconcile them. It needs all three.
        own_progress = np.clip(own_progress + own, 0.0, 1.0)
        assertion = np.clip(P.v("assertion_efficacy") * s
                            - P.v("assertion_anxiety") * a, 0.0, 1.0)
        conflict = np.clip(substitute * divergence * own_progress
                           * (1.0 - assertion), 0.0, 2.0)

        if record:
            traj["u"][t + 1], traj["s"][t + 1] = u, s
            traj["a"][t + 1], traj["e"][t + 1] = a, e

    wc = P.v("conflict_weight")
    difficulty = np.clip((1.0 - wc) * u + wc * conflict, 0.0, 2.0)
    out = {"u": u, "s": s, "a": a, "trait_a": trait_a, "conflict": conflict,
           "difficulty": difficulty, "explore": expl_sum / T,
           "support": c_tot, "scaffold": scaffold, "substitute": substitute,
           "n": n, "weeks": T, "substitution_share": pi}
    if record:
        out["traj"] = traj
    return out


def observe(state, seed=7, error=None):
    """Add measurement error, as the self-report scales in this field carry.

    Each latent quantity is observed with classical error of the declared
    share of variance, which is what a reliability coefficient below one
    means. The observed variables are the model's counterparts of the four
    constructs the empirical literature measures.
    """
    rng = np.random.default_rng(seed)
    err = P.v("measurement_error") if error is None else error
    out = {}
    for key, name in (("a", "CA"), ("s", "CDSE"), ("difficulty", "CDD"),
                      ("support", "PCS")):
        x = np.asarray(state[key], float)
        sd = x.std()
        if err <= 0 or sd == 0:
            out[name] = x.copy()
        else:
            # var(obs) = var(true) + var(err), with var(err) a share of the total
            noise_sd = sd * np.sqrt(err / max(1.0 - err, 1e-6))
            out[name] = x + noise_sd * rng.normal(size=x.size)
    return out


def _selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        if not c:
            print("FAIL:", m); ok = False

    st = simulate(n=2000, seed=1, record=True)
    for k in ("u", "s", "a"):
        chk(np.isfinite(st[k]).all(), "%s finite" % k)
    chk((st["u"] >= 0).all() and (st["u"] <= 1).all(), "u bounded")
    chk((st["s"] >= 0).all() and (st["s"] <= 1).all(), "s bounded")
    chk((st["a"] >= 0).all() and (st["a"] <= 2).all(), "a bounded")

    # uncertainty must fall on average over the horizon
    tr = st["traj"]
    chk(tr["u"][-1].mean() < tr["u"][0].mean(), "uncertainty resolves on average")

    # more anxious people must end more uncertain, holding the rest random
    hi = st["a"] > np.quantile(st["a"], 0.75)
    lo = st["a"] < np.quantile(st["a"], 0.25)
    chk(st["u"][hi].mean() > st["u"][lo].mean(),
        "anxious young people end more uncertain (%.3f vs %.3f)"
        % (st["u"][hi].mean(), st["u"][lo].mean()))

    # substitution must lower self-efficacy while still lowering uncertainty
    sc = simulate(n=2000, seed=1, substitution=0.0)
    sb = simulate(n=2000, seed=1, substitution=1.0)
    chk(sb["s"].mean() < sc["s"].mean(),
        "substituting support lowers efficacy (%.3f vs %.3f)"
        % (sb["s"].mean(), sc["s"].mean()))

    print("model.py self-test:", "PASSED" if ok else "FAILED")
    print("  horizon %d weeks, n = %d" % (st["weeks"], st["n"]))
    print("  end state: u %.3f (%.3f)  s %.3f (%.3f)  a %.3f (%.3f)"
          % (st["u"].mean(), st["u"].std(), st["s"].mean(), st["s"].std(),
             st["a"].mean(), st["a"].std()))
    print("  pure scaffolding  -> u %.3f  s %.3f" % (sc["u"].mean(), sc["s"].mean()))
    print("  pure substitution -> u %.3f  s %.3f" % (sb["u"].mean(), sb["s"].mean()))
    obs = observe(st)
    import itertools
    ks = ["CA", "CDSE", "PCS", "CDD"]
    print("  observed correlations:")
    for x, y in itertools.combinations(ks, 2):
        print("    r(%-4s, %-4s) = %+.3f" % (x, y, np.corrcoef(obs[x], obs[y])[0, 1]))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
