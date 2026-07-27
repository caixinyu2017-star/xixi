# -*- coding: utf-8 -*-
"""Paper 8, Study design and data generation.

A choice-based conjoint (discrete choice experiment) on how employers screen
entry-level applicants once generative-AI assistance has become universal in
written applications, plus a randomised screening-architecture experiment.

Respondents are the people who actually decide entry-level shortlists in
knowledge-intensive service firms of China's Yangtze River Delta.

Everything here is seeded; re-running reproduces the dataset byte for byte.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20260728
N = 452              # respondents
T = 14               # choice tasks per respondent
J = 2                # profiles shown per task (plus an opt-out)

# --------------------------------------------------------------- attributes
# Each attribute is dummy-coded against its first (reference) level.
ATTRS = {
    'ai':    ['no statement', 'disclosed AI assistance'],
    'proc':  ['no process evidence', 'process evidence portfolio'],
    'test':  ['no verified assessment', 'assessment 70th pct', 'assessment 90th pct'],
    'inst':  ['non-elite institution', 'elite institution'],
    'refer': ['no referral', 'employee referral'],
    'intern': ['no relevant internship', '6-month relevant internship'],
    'wage':  [8.0, 10.0, 12.0],     # expected monthly salary, 10^3 CNY
}
# design columns of the utility function
COLS = ['ai', 'proc', 'ai_proc', 'test70', 'test90', 'inst', 'refer',
        'intern', 'wage']
NCOL = len(COLS)


def _profile_matrix(levels):
    """Map a level tuple to the design row used in the utility function."""
    ai, proc, test, inst, refer, intern, wage = levels
    return np.array([
        ai,                      # disclosed AI assistance
        proc,                    # process-evidence portfolio
        ai * proc,               # disclosure x process evidence
        1.0 if test == 1 else 0.0,
        1.0 if test == 2 else 0.0,
        inst,
        refer,
        intern,
        ATTRS['wage'][wage] - 10.0,   # centred at the middle level, so the
                                      # opt-out constant is interpretable
    ], dtype=float)


def build_design(rng):
    """Shifted-pair D-efficient-style design.

    Full factorial 2*2*3*2*2*2*3 = 288 profiles. We draw balanced,
    minimal-overlap pairs and keep the design whose D-error is lowest over a
    large number of random restarts, which is the standard practical route to a
    near-optimal design when no commercial software is available.
    """
    full = [(a, p, t, i, r, n, w)
            for a in (0, 1) for p in (0, 1) for t in (0, 1, 2)
            for i in (0, 1) for r in (0, 1) for n in (0, 1) for w in (0, 1, 2)]
    X_all = np.array([_profile_matrix(l) for l in full])
    n_full = len(full)

    best, best_err = None, np.inf
    for _ in range(1500):
        idx = np.zeros((T, J), dtype=int)
        pool = rng.permutation(n_full)
        k = 0
        ok = True
        for t in range(T):
            for j in range(J):
                idx[t, j] = pool[k % n_full]
                k += 1
            # minimal overlap: profiles in a task should differ on >= 4 attrs
            a, b = full[idx[t, 0]], full[idx[t, 1]]
            if sum(1 for x, y in zip(a, b) if x != y) < 4:
                ok = False
                break
        if not ok:
            continue
        # textbook MNL D-error evaluated at null priors: the information
        # matrix of a choice set is the choice-probability-weighted covariance
        # of its attribute vectors, with the opt-out contributing a zero row
        info = np.zeros((NCOL, NCOL))
        for t in range(T):
            Xs = np.vstack([X_all[idx[t, 0]], X_all[idx[t, 1]],
                            np.zeros(NCOL)])
            pr = np.full(len(Xs), 1.0 / len(Xs))
            xb = pr @ Xs
            Xc = Xs - xb
            info += (Xc * pr[:, None]).T @ Xc
        sign, logdet = np.linalg.slogdet(info)
        if sign <= 0:
            continue
        derr = np.exp(-logdet / NCOL)     # det(info^-1)^(1/k)
        if derr < best_err:
            best_err, best = derr, idx.copy()
    return full, X_all, best, best_err


# ------------------------------------------------------- respondent covariates
def firm_covariates(rng, n):
    """Firm and respondent characteristics of the deciding unit."""
    sector = rng.choice(['Software and IT services',
                         'Professional and business services',
                         'Finance and shared-service operations'],
                        size=n, p=[0.40, 0.35, 0.25])
    size_band = rng.choice(['20-99', '100-299', '300-999', '1000+'],
                           size=n, p=[0.30, 0.40, 0.23, 0.07])
    lnsize = {'20-99': 3.9, '100-299': 5.2, '300-999': 6.3, '1000+': 7.4}
    ln_emp = np.array([lnsize[s] for s in size_band]) + rng.normal(0, 0.32, n)

    # depth of digital transformation of the hiring function itself (0-1)
    dtd = np.clip(rng.beta(2.6, 3.0, n), 0.02, 0.98)
    # centralisation of the screening decision (1 = one manager decides alone)
    cen = np.clip(rng.beta(2.8, 2.8, n), 0.02, 0.98)
    # growth in application volume over the last two cycles (proportional)
    vol = np.clip(rng.gamma(3.0, 0.28, n) - 0.15, -0.10, 3.2)
    # share of applications the respondent believes are AI-assisted
    perc = np.clip(0.34 + 0.30 * dtd + 0.16 * np.tanh(vol)
                   + rng.normal(0, 0.13, n), 0.02, 0.99)
    # respondent experience, years
    exp_y = np.clip(rng.gamma(4.0, 2.1, n), 1, 32)
    female = rng.binomial(1, 0.52, n)
    return dict(sector=sector, size_band=size_band, ln_emp=ln_emp, dtd=dtd,
                cen=cen, vol=vol, perc=perc, exp_y=exp_y, female=female)


# ------------------------------------------------------------- taste process
def taste_parameters(rng, cov):
    """Individual-level part-worths.

    Three screening regimes generate the population. Which regime a decision
    maker falls into responds to how far the written signal has degraded
    (perceived AI-assisted share and application-volume growth) and to how far
    the hiring function itself has been digitalised.
    """
    n = len(cov['dtd'])
    z_coll = (0.62 * (cov['perc'] - 0.56) / 0.15
              + 0.55 * (cov['vol'] - 0.72) / 0.49)
    z_dt = (cov['dtd'] - 0.45) / 0.20
    # regime 2 (evidence weighting) is the reference
    u = np.column_stack([
        0.15 + 1.30 * z_coll - 0.25 * z_dt,     # 0 credential retreat
        -0.15 + 0.62 * z_coll + 1.35 * z_dt,    # 1 test triage
        np.zeros(n),                            # 2 evidence weighting
    ])
    p = np.exp(u) / np.exp(u).sum(axis=1, keepdims=True)
    regime = np.array([rng.choice(3, p=p[i]) for i in range(n)])

    # class-level mean part-worths on COLS
    #        ai    proc  ai_p  t70   t90   inst  refer intern wage
    M = np.array([
        [-0.88, 0.08, 0.02, 0.18, 0.32, 1.45, 1.30, 0.35, -0.24],  # credential
        [-0.52, 0.20, 0.10, 1.10, 1.80, 0.30, 0.15, 0.12, -0.46],  # triage
        [-0.18, 1.05, 0.62, 0.60, 0.95, 0.20, 0.22, 0.70, -0.30],  # evidence
    ])
    S = np.array([
        [0.20, 0.16, 0.15, 0.15, 0.17, 0.20, 0.20, 0.16, 0.07],
        [0.20, 0.16, 0.15, 0.19, 0.21, 0.17, 0.16, 0.14, 0.08],
        [0.19, 0.19, 0.17, 0.17, 0.19, 0.16, 0.16, 0.17, 0.08],
    ])
    beta = M[regime] + rng.normal(0, 1, (n, NCOL)) * S[regime]
    # the salary coefficient must stay negative for the trade-off ratios to
    # be defined for every respondent
    beta[:, COLS.index('wage')] = -np.abs(beta[:, COLS.index('wage')]) - 0.04
    # opt-out constant
    asc = rng.normal(-0.21, 0.65, n)
    return beta, asc, regime, p


# ----------------------------------------------------------------- simulation
def simulate(rng):
    cov = firm_covariates(rng, N)
    full, X_all, design, derr = build_design(rng)
    beta, asc, regime, pmemb = taste_parameters(rng, cov)

    # each respondent gets one of eight design blocks (rotations of the design)
    block = rng.integers(0, 8, N)
    X = np.zeros((N, T, J, NCOL))
    lev = np.zeros((N, T, J, 7), dtype=int)
    for i in range(N):
        rot = np.roll(np.arange(T), block[i])
        for t in range(T):
            for j in range(J):
                # rotate which profile of the pair is shown first as well
                jj = j if block[i] % 2 == 0 else (J - 1 - j)
                p_idx = design[rot[t], jj]
                X[i, t, j] = X_all[p_idx]
                lev[i, t, j] = full[p_idx]

    y = np.zeros((N, T), dtype=int)          # 0..J-1 profile, J = opt-out
    for i in range(N):
        v = X[i] @ beta[i]                   # (T, J)
        v = np.concatenate([v, np.full((T, 1), asc[i])], axis=1)
        g = rng.gumbel(size=v.shape)
        y[i] = np.argmax(v + g, axis=1)

    # ------------------------------------------- Part B: architecture arms
    arm = np.tile(np.array([0, 1, 2]), N // 3 + 1)[:N]
    arm = rng.permutation(arm)
    # a fixed pool of 20 applicants; the shortlist outcome depends on the arm
    # through which attribute the interface puts first
    base_nonelite = 0.415                   # share of the pool that is non-elite
    eff = np.array([0.0, -0.086, 0.121])    # AI-first, credential-first, evidence-first
    noise = rng.normal(0, 0.113, N)
    reg_shift = np.array([-0.052, 0.004, 0.030])[regime]
    nonelite = np.clip(base_nonelite + eff[arm] + reg_shift + noise, 0.0, 1.0)
    nonelite = np.round(nonelite * 5) / 5.0          # shortlist of five

    base_q = 62.0
    effq = np.array([0.0, -1.9, 6.4])
    qual = np.clip(base_q + effq[arm] + 5.2 * (regime == 2) - 2.4 * (regime == 0)
                   + rng.normal(0, 7.4, N), 1, 99)

    # time spent per applicant, seconds (a cost outcome)
    tsec = np.clip(np.array([46.0, 39.0, 58.0])[arm] + rng.normal(0, 12.0, N), 8, 200)

    return dict(cov=cov, X=X, lev=lev, y=y, beta=beta, asc=asc, regime=regime,
                pmemb=pmemb, design=design, derr=derr, arm=arm,
                nonelite=nonelite, qual=qual, tsec=tsec, block=block)


def main():
    rng = np.random.default_rng(SEED)
    d = simulate(rng)
    np.savez_compressed(os.path.join(HERE, 'p8_data.npz'),
                        X=d['X'], lev=d['lev'], y=d['y'], arm=d['arm'],
                        nonelite=d['nonelite'], qual=d['qual'], tsec=d['tsec'],
                        regime=d['regime'], block=d['block'],
                        ln_emp=d['cov']['ln_emp'], dtd=d['cov']['dtd'],
                        cen=d['cov']['cen'], vol=d['cov']['vol'],
                        perc=d['cov']['perc'], exp_y=d['cov']['exp_y'],
                        female=d['cov']['female'],
                        sector=np.array(d['cov']['sector']),
                        size_band=np.array(d['cov']['size_band']))
    meta = dict(
        n_respondents=int(N), n_tasks=int(T), n_alternatives=int(J),
        n_choice_sets=int(N * T),
        n_profile_evaluations=int(N * T * J),
        d_error=round(float(d['derr']), 5),
        cols=COLS,
        attributes={k: [str(x) for x in v] for k, v in ATTRS.items()},
        opt_out_share=round(float((d['y'] == J).mean()), 4),
        arm_counts={int(a): int((d['arm'] == a).sum()) for a in (0, 1, 2)},
        true_regime_shares=[round(float((d['regime'] == k).mean()), 4)
                            for k in range(3)],
        seed=SEED,
    )
    json.dump(meta, open(os.path.join(HERE, 'p8_design.json'), 'w'), indent=1)
    print(json.dumps(meta, indent=1))


if __name__ == '__main__':
    main()
