# -*- coding: utf-8 -*-
"""Paper 7 — system dynamics model of generative-AI entry-task automation and the
expertise pipeline of a knowledge-service occupational system.

STOCKS
  J   junior (entry-level) professionals employed        [thousand persons]
  S   senior (proficient) professionals employed         [thousand persons]
  P   entrants seeking entry-level work (incl. NEET)     [thousand persons]
  Q   employability capital held by the pool             [thousand skill units]
      average pool skill Kp = Q / P (1 = fresh graduate, dimensionless)
  W   perceived senior-scarcity signal (dimensionless)

EXOGENOUS
  D(t) demand for professional work        [thousand task units per year]
  G    inflow of qualified entrants        [thousand persons per year]
  A(t) depth of generative-AI automation of the routine (entry) task bundle,
       logistic diffusion from A0 toward A_max

WORK STRUCTURE
  complex work  C = sigma * D          performed by seniors only
  routine work  R = (1 - sigma) * D    performed by juniors, by AI (subject to
                                       senior verification), or by seniors

SENIOR TIME ALLOCATION  [senior-years per year], strict priority
  1. complex work            c_need = C / piS
  2. verification of AI       v_need = nu * A * R
  3. residual routine work    r_need = (R - piJ*J - A*R*q) / piS
  4. mentoring of juniors     m_need = mstar * J   <- residual claimant; it is
     drawn from the non-delivery budget (1 - ustar) * S, which delivery
     encroaches upon whenever delivery need exceeds ustar * S

LEARNING
  tau = tau0 / (Lm * Le * Lk)                        time to proficiency [yr]
  Lm  = ((m + mf) / (mstar + mf)) ** a_ment          mentoring multiplier
  Le  = 1 - theta * A + lam * A                      practice displacement vs.
                                                     AI-as-tutor
  Lk  = Kp ** c_qual                                 entry-cohort quality

FEEDBACK LOOPS (Figure 1 of the manuscript)
  B1 cost-driven entry substitution     R1 seed-corn pipeline erosion
  R2 practice displacement              B2 verification bottleneck
  R3 scarring of the entrant pool       R4 training crowd-out under delivery
  B3 delayed scarcity correction           pressure

All manuscript numbers derive from this script (p7_model.json, p7_traj.json).
"""
import json, os
import numpy as np
from scipy import stats as st

HERE = os.path.dirname(os.path.abspath(__file__))
DT = 0.05
HORIZON = 30.0
POLICY_START = 3.0


# ----------------------------------------------------------------- parameters
def base_params():
    return dict(
        # --- environment
        D0=822.7,        # demand for professional work [10^3 task units/yr]
        g=0.0,           # demand growth rate [1/yr] (stationary base case)
        G=40.0,          # qualified entrant inflow [10^3 persons/yr]
        sigma=0.30,      # complex-work share of demand
        # --- AI diffusion
        A0=0.05,
        A_max=0.70,
        c_diff=0.40,
        # --- production technology
        piJ=1.60,        # junior output [task units per junior-year]
        piS=2.70,        # senior output [task units per senior-year]
        ustar=0.88,      # senior delivery-utilisation norm
        j0=0.13497,      # junior requirement at A=0 [junior-yr per task unit]
        phi=0.605,       # substitutability of AI for junior labour (Study 1)
        nu=0.136,        # verification load [senior-yr per AI output unit] (Study 1)
        # --- human-capital pipeline
        tau0=6.02,       # reference time to proficiency [yr] (Study 1)
        mstar=0.102,     # reference mentoring intensity [senior-yr/junior] (Study 1)
        mfloor=0.30,     # informal-learning floor, as a share of mstar
        a_ment=0.446,    # mentoring elasticity of proficiency (Study 1)
        theta=0.574,     # practice-displacement coefficient (Study 1)
        lam=0.265,       # AI-as-tutor coefficient at mean practice (Study 1)
        c_qual=0.40,     # entry-cohort quality elasticity
        tauJ=5.0,        # junior exit time (quits out of the occupation) [yr]
        tauS=17.0,       # senior exit time (retirement/exit) [yr]
        back=0.55,       # share of junior quits returning to the pool
        tauH=1.20,       # hiring adjustment time [yr]
        tauM=0.60,       # pool-to-vacancy matching time [yr]
        tauP=6.0,        # discouragement exit time from the pool [yr]
        delta=0.115,     # skill-decay rate of pooled entrants [1/yr]
        # --- delayed scarcity correction (B3)
        w_sens=0.55,
        tauW=5.0,
        # --- policy levers (inactive at baseline)
        p_sub=0.0, p_ment=0.0, p_appr=0.0, p_ver=0.0,
    )


POLICIES = {
    'P1': dict(name='Entry-hiring subsidy', p_sub=0.25),
    'P2': dict(name='Protected mentoring time', p_ment=0.10),
    'P3': dict(name='AI-augmented apprenticeship', p_appr=0.310),
    'P4': dict(name='Automated verification', p_ver=0.40),
    'P5': dict(name='Integrated portfolio', p_sub=0.25, p_ment=0.10,
               p_appr=0.310, p_ver=0.40),
}


# ------------------------------------------------------------------ mechanics
def ai_depth(t, p, ai_on=True):
    if not ai_on:
        return p['A0']
    A0, Am, c = p['A0'], p['A_max'], p['c_diff']
    if Am <= 1e-9:
        return 0.0
    r = A0 / Am
    e = np.exp(c * t)
    return Am * r * e / (1.0 + r * (e - 1.0))


def allocate(S, J, A, D, p, pol_on):
    """Senior time allocation. Returns dict of senior-years per year."""
    S = max(S, 1e-9)
    C = p['sigma'] * D
    R = (1.0 - p['sigma']) * D
    nu_eff = p['nu'] * (1.0 - (p['p_ver'] if pol_on else 0.0))

    cap = S
    c_act = min(C / p['piS'], cap); cap -= c_act
    v_need = nu_eff * A * R
    v_act = min(v_need, cap); cap -= v_act
    q = v_act / v_need if v_need > 1e-12 else 1.0

    routine_left = max(0.0, R - p['piJ'] * J - A * R * q)
    r_need = routine_left / p['piS']

    # mentoring draws on the non-delivery budget; delivery encroaches on it
    delivery_need = c_act + v_act + r_need
    reserve = (p['p_ment'] if pol_on else 0.0) * S           # ring-fenced
    nondelivery = max(0.0, (1.0 - p['ustar']) * S)
    encroach = max(0.0, delivery_need - p['ustar'] * S)
    ment_budget = max(reserve, nondelivery - encroach)
    ment_budget = min(ment_budget, cap)

    m_act = min(p['mstar'] * max(J, 1e-9), ment_budget)
    cap -= m_act
    r_act = min(r_need, cap)

    # productive capacity of the occupational system: work the system can
    # deliver per year given its people, its AI, and the senior time that
    # verification and mentoring consume
    capacity = (p['piJ'] * J + A * R * q
                + p['piS'] * max(0.0, S - v_act - m_act))
    delivered = min(capacity, D)
    m = m_act / max(J, 1e-9)
    return dict(c_act=c_act, v_act=v_act, r_act=r_act, m_act=m_act, m=m, q=q,
                r_need=r_need, delivery_need=delivery_need,
                util=(c_act + v_act + r_act) / S, capacity=capacity,
                delivered=delivered,
                backlog=max(0.0, r_need - r_act) * p['piS'])


def proficiency(m, A, Kp, p, pol_on):
    mf = p['mfloor'] * p['mstar']
    Lm = np.clip(((m + mf) / (p['mstar'] + mf)) ** p['a_ment'], 0.05, 2.2)
    lam_eff = p['lam'] + (p['p_appr'] if pol_on else 0.0)
    Le = np.clip(1.0 - p['theta'] * A + lam_eff * A, 0.10, 2.2)
    Lk = np.clip(max(Kp, 1e-6) ** p['c_qual'], 0.20, 1.30)
    return p['tau0'] / max(Lm * Le * Lk, 1e-6), Lm, Le, Lk


def _state(t, y, p, ai_on, pol_on_fn):
    J, S, P, Q, W = y
    J = max(J, 1e-9); S = max(S, 1e-9); P = max(P, 1e-6); Q = max(Q, 0.0)
    pol_on = bool(pol_on_fn(t)) if pol_on_fn else False
    D = p['D0'] * np.exp(p['g'] * t)
    A = ai_depth(t, p, ai_on)
    Kp = float(np.clip(Q / P, 0.05, 1.0))
    al = allocate(S, J, A, D, p, pol_on)
    tau, Lm, Le, Lk = proficiency(al['m'], A, Kp, p, pol_on)

    Jstar = p['j0'] * D * (1.0 - p['phi'] * A) * (1.0 + W * p['w_sens'])
    if pol_on:
        Jstar *= (1.0 + p['p_sub'])
    promote = J / tau
    jun_exit = J / p['tauJ']
    hire_want = max(0.0, (Jstar - J) / p['tauH'] + promote + jun_exit)
    hire = min(hire_want, P / p['tauM'])
    return (J, S, P, Q, W, D, A, Kp, al, tau, Lm, Le, Lk, Jstar,
            promote, jun_exit, hire, pol_on)


def derivs(t, y, p, ai_on=True, pol_on_fn=None):
    (J, S, P, Q, W, D, A, Kp, al, tau, Lm, Le, Lk, Jstar,
     promote, jun_exit, hire, pol_on) = _state(t, y, p, ai_on, pol_on_fn)
    disc = P / p['tauP']
    dJ = hire - promote - jun_exit
    dS = promote - S / p['tauS']
    dP = p['G'] + p['back'] * jun_exit - hire - disc
    dQ = p['G'] + p['back'] * jun_exit - (hire + disc) * Kp - p['delta'] * Q
    # perceived senior scarcity: shortfall of senior capacity against the
    # delivery workload that seniors must carry
    Sdes = al['delivery_need'] / p['ustar']
    gap = float(np.clip((Sdes - S) / max(Sdes, 1e-9), -0.6, 1.5))
    dW = (gap - W) / p['tauW']
    return np.array([dJ, dS, dP, dQ, dW])


def observe(t, y, p, ai_on=True, pol_on_fn=None):
    (J, S, P, Q, W, D, A, Kp, al, tau, Lm, Le, Lk, Jstar,
     promote, jun_exit, hire, pol_on) = _state(t, y, p, ai_on, pol_on_fn)
    return dict(t=float(t), J=J, S=S, P=P, Kp=Kp, W=W, A=A, D=D, tau=tau,
                m=al['m'], q=al['q'], util=al['util'], Y=al['capacity'],
                backlog=al['backlog'], adequacy=al['capacity'] / D,
                delivered=al['delivered'],
                hire=hire, promote=promote, Jstar=Jstar,
                ment_share=al['m_act'] / S, ver_share=al['v_act'] / S,
                Lm=Lm, Le=Le, Lk=Lk, workforce=J + S)


def rk4(y0, t1, dt, p, ai_on=True, pol_on_fn=None):
    n = int(round(t1 / dt))
    y = np.array(y0, dtype=float)
    ts = np.empty(n + 1); Y = np.empty((n + 1, 5))
    ts[0] = 0.0; Y[0] = y
    t = 0.0
    for i in range(n):
        k1 = derivs(t, y, p, ai_on, pol_on_fn)
        k2 = derivs(t + dt / 2, y + dt / 2 * k1, p, ai_on, pol_on_fn)
        k3 = derivs(t + dt / 2, y + dt / 2 * k2, p, ai_on, pol_on_fn)
        k4 = derivs(t + dt, y + dt * k3, p, ai_on, pol_on_fn)
        y = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        y = np.array([max(y[0], 1e-9), max(y[1], 1e-9), max(y[2], 1e-6),
                      max(y[3], 0.0), y[4]])
        t += dt
        ts[i + 1] = t; Y[i + 1] = y
    return ts, Y


def equilibrium(p, years=260.0, dt=0.25):
    pe = dict(p); pe['g'] = 0.0
    _, Y = rk4((110.0, 300.0, 76.0, 65.0, 0.0), years, dt, pe, ai_on=False)
    return Y[-1].copy()


def run(p, y0, horizon=HORIZON, dt=DT, ai_on=True, policy=None):
    pp = dict(p)
    if policy:
        for k, v in policy.items():
            if k != 'name':
                pp[k] = v
    fn = (lambda t: t >= POLICY_START) if policy else None
    ts, Y = rk4(y0, horizon, dt, pp, ai_on=ai_on, pol_on_fn=fn)
    obs = [observe(ts[i], Y[i], pp, ai_on=ai_on, pol_on_fn=fn) for i in range(len(ts))]
    return ts, Y, obs


def ser(obs, key):
    return np.array([o[key] for o in obs])


# =============================================================== main analysis
def main():
    rng = np.random.default_rng(20260722)
    p = base_params()
    out = {'parameters': p, 'policy_start_year': POLICY_START,
           'dt': DT, 'horizon': HORIZON}

    y0 = equilibrium(p)
    out['initial_state'] = dict(J=round(float(y0[0]), 3), S=round(float(y0[1]), 3),
                                P=round(float(y0[2]), 3), Q=round(float(y0[3]), 3),
                                Kp=round(float(y0[3] / y0[2]), 4))
    ts, _, oc = run(p, y0, ai_on=False)
    _, _, ob = run(p, y0, ai_on=True)
    out['initial_aux'] = {k: round(float(oc[0][k]), 4) for k in
                          ('tau', 'm', 'util', 'q', 'Y', 'adequacy', 'hire',
                           'promote', 'ment_share', 'Lm', 'Le', 'Lk')}

    idx = lambda yr: int(round(yr / DT))
    VARS = ('A', 'S', 'J', 'P', 'Kp', 'tau', 'm', 'q', 'util', 'hire',
            'promote', 'Y', 'adequacy', 'ment_share', 'ver_share', 'workforce')
    for tag, o in (('counterfactual', oc), ('baseline', ob)):
        out[tag] = {str(yr): {k: round(float(o[idx(yr)][k]), 4) for k in VARS}
                    for yr in (0, 5, 10, 15, 20, 25, 30)}

    Sb, Sc = ser(ob, 'S'), ser(oc, 'S')
    Yb, Yc = ser(ob, 'Y'), ser(oc, 'Y')
    Hb, Hc = ser(ob, 'hire'), ser(oc, 'hire')
    rel = lambda a, b: 100.0 * (a - b) / b

    dY = Yb - Yc
    cross = None
    for i in range(1, len(ts)):
        if dY[i - 1] > 0 >= dY[i]:
            cross = round(float(ts[i - 1] + DT * dY[i - 1] / (dY[i - 1] - dY[i])), 2)
            break
    k = dict(
        output_crossover_year=cross,
        peak_output_gain_pct=round(float(np.max(rel(Yb, Yc))), 2),
        peak_output_gain_year=round(float(ts[int(np.argmax(rel(Yb, Yc)))]), 2),
        output_gap_year30_pct=round(float(rel(Yb, Yc)[-1]), 2),
        senior_gap_year30_pct=round(float(rel(Sb, Sc)[-1]), 2),
        senior_gap_year10_pct=round(float(rel(Sb, Sc)[idx(10)]), 2),
        junior_gap_year30_pct=round(float(rel(ser(ob, 'J'), ser(oc, 'J'))[-1]), 2),
        workforce_gap_year30_pct=round(float(rel(ser(ob, 'workforce'),
                                                 ser(oc, 'workforce'))[-1]), 2),
        hiring_gap_year3_pct=round(float(rel(Hb, Hc)[idx(3)]), 2),
        hiring_gap_year5_pct=round(float(rel(Hb, Hc)[idx(5)]), 2),
        hiring_trough_pct=round(float(np.min(rel(Hb, Hc))), 2),
        hiring_trough_year=round(float(ts[int(np.argmin(rel(Hb, Hc)))]), 2),
        tau_year0=round(float(ser(ob, 'tau')[0]), 3),
        tau_year30=round(float(ser(ob, 'tau')[-1]), 3),
        util_year30=round(float(ser(ob, 'util')[-1]), 4),
        ment_share_year0=round(float(ser(ob, 'ment_share')[0]), 4),
        ment_share_year30=round(float(ser(ob, 'ment_share')[-1]), 4),
        q_year30=round(float(ser(ob, 'q')[-1]), 4),
        Kp_year30=round(float(ser(ob, 'Kp')[-1]), 4),
        pool_gap_year30_pct=round(float(rel(ser(ob, 'P'), ser(oc, 'P'))[-1]), 2),
        adequacy_year30=round(float(ser(ob, 'adequacy')[-1]), 4),
        promote_year30=round(float(ser(ob, 'promote')[-1]), 3),
        promote_year0=round(float(ser(ob, 'promote')[0]), 3),
        cum_hires_base=round(float(np.trapezoid(Hb, ts)), 1),
        cum_hires_cf=round(float(np.trapezoid(Hc, ts)), 1),
        cum_hires_lost_pct=round(float(rel(np.trapezoid(Hb, ts),
                                           np.trapezoid(Hc, ts))), 2),
        cum_promotions_base=round(float(np.trapezoid(ser(ob, 'promote'), ts)), 1),
        conversion_base=round(float(np.trapezoid(ser(ob, 'promote'), ts)
                                    / np.trapezoid(Hb, ts)), 4),
        conversion_cf=round(float(np.trapezoid(ser(oc, 'promote'), ts)
                                  / np.trapezoid(Hc, ts)), 4),
        pool_years_base=round(float(np.trapezoid(ser(ob, 'P'), ts)), 1),
        pool_years_cf=round(float(np.trapezoid(ser(oc, 'P'), ts)), 1),
        pool_years_excess_pct=round(float(rel(np.trapezoid(ser(ob, 'P'), ts),
                                              np.trapezoid(ser(oc, 'P'), ts))), 2),
        capacity_year10_pct=round(float(rel(Yb, Yc)[idx(10)]), 2),
        capacity_year20_pct=round(float(rel(Yb, Yc)[idx(20)]), 2),
    )
    out['key_results'] = k

    # ------------------------------------------------------- tipping analysis
    grid = np.round(np.arange(0.10, 0.9501, 0.025), 4)
    sweep = []
    for Am in grid:
        pa = dict(p); pa['A_max'] = float(Am)
        _, _, o = run(pa, y0, ai_on=True)
        sweep.append(dict(
            A_max=float(Am),
            S_rel=round(float(rel(ser(o, 'S'), Sc)[-1]), 3),
            Y_rel=round(float(rel(ser(o, 'Y'), Yc)[-1]), 3),
            tau30=round(float(ser(o, 'tau')[-1]), 3),
            q30=round(float(ser(o, 'q')[-1]), 4),
            hire_rel=round(float(rel(ser(o, 'hire'), Hc)[-1]), 3),
            ment_ratio=round(float(ser(o, 'm')[-1] / p['mstar']), 4)))
    out['sweep'] = sweep
    srel = np.array([r['S_rel'] for r in sweep])
    yrel = np.array([r['Y_rel'] for r in sweep])
    d1 = np.gradient(srel, grid)
    out['tipping'] = dict(
        steepest_A_max=round(float(grid[int(np.argmin(d1))]), 3),
        steepest_slope=round(float(np.min(d1)), 2),
        A_at_S_minus10=next((float(g) for g, v in zip(grid, srel) if v <= -10), None),
        A_at_S_minus25=next((float(g) for g, v in zip(grid, srel) if v <= -25), None),
        A_at_Y_negative=next((float(g) for g, v in zip(grid, yrel) if v <= 0), None),
        curvature_ratio=round(float(abs(np.min(d1)) / abs(np.median(d1))), 2),
        A_training_collapse=next((float(g) for g, r in zip(grid, sweep)
                                  if r['ment_ratio'] < 0.20), None),
        A_verification_binds=next((float(g) for g, r in zip(grid, sweep)
                                   if r['q30'] < 0.995), None))

    # ------------------------------------------------------ policy experiments
    pol = {}
    for tag, spec in POLICIES.items():
        _, _, o = run(p, y0, ai_on=True, policy=spec)
        S30, Y30 = ser(o, 'S')[-1], ser(o, 'Y')[-1]
        cum_h = float(np.trapezoid(ser(o, 'hire'), ts))
        cum_p = float(np.trapezoid(ser(o, 'promote'), ts))
        pol[tag] = dict(
            name=spec['name'],
            S30=round(float(S30), 2),
            S_vs_base_pct=round(float(rel(S30, Sb[-1])), 2),
            S_vs_cf_pct=round(float(rel(S30, Sc[-1])), 2),
            Y_vs_base_pct=round(float(rel(Y30, Yb[-1])), 2),
            Y_vs_cf_pct=round(float(rel(Y30, Yc[-1])), 2),
            tau30=round(float(ser(o, 'tau')[-1]), 3),
            q30=round(float(ser(o, 'q')[-1]), 4),
            Kp30=round(float(ser(o, 'Kp')[-1]), 4),
            pool30=round(float(ser(o, 'P')[-1]), 2),
            cum_hires=round(cum_h, 1),
            cum_promotions=round(cum_p, 1),
            conversion=round(cum_p / max(cum_h, 1e-9), 4),
            ment_share30=round(float(ser(o, 'ment_share')[-1]), 4),
            J30=round(float(ser(o, 'J')[-1]), 2),
            pool_years=round(float(np.trapezoid(ser(o, 'P'), ts)), 1),
            senior_years_gained=round(float(np.trapezoid(ser(o, 'S'), ts)
                                            - np.trapezoid(Sb, ts)), 1),
            extra_hires=round(cum_h - float(np.trapezoid(Hb, ts)), 1))
    base_cum_h = float(np.trapezoid(Hb, ts))
    base_cum_p = float(np.trapezoid(ser(ob, 'promote'), ts))
    pol['P0'] = dict(name='Baseline (no policy)', S30=round(float(Sb[-1]), 2),
                     S_vs_base_pct=0.0,
                     S_vs_cf_pct=round(float(rel(Sb[-1], Sc[-1])), 2),
                     Y_vs_base_pct=0.0,
                     Y_vs_cf_pct=round(float(rel(Yb[-1], Yc[-1])), 2),
                     tau30=k['tau_year30'], q30=k['q_year30'],
                     Kp30=k['Kp_year30'], pool30=round(float(ser(ob, 'P')[-1]), 2),
                     cum_hires=round(base_cum_h, 1),
                     cum_promotions=round(base_cum_p, 1),
                     conversion=round(base_cum_p / base_cum_h, 4),
                     ment_share30=k['ment_share_year30'],
                     J30=round(float(ser(ob, 'J')[-1]), 2),
                     pool_years=round(float(np.trapezoid(ser(ob, 'P'), ts)), 1),
                     senior_years_gained=0.0, extra_hires=0.0)
    singles = sum(pol[t_]['S_vs_base_pct'] for t_ in ('P1', 'P2', 'P3', 'P4'))
    pol['P5']['sum_of_singles_pct'] = round(float(singles), 2)
    pol['P5']['synergy_pp'] = round(float(pol['P5']['S_vs_base_pct'] - singles), 2)
    out['policies'] = pol

    # ------------------------------------------------- structural loop tests
    knock = {}
    for tag, mod in (('R2_off_no_practice_displacement', dict(theta=0.0)),
                     ('R2_off_no_ai_tutoring', dict(lam=0.0)),
                     ('B2_off_no_verification', dict(nu=0.0)),
                     ('R3_off_no_scarring', dict(delta=0.0)),
                     ('R4_off_no_mentoring_channel', dict(a_ment=0.0)),
                     ('B3_off_no_scarcity_correction', dict(w_sens=0.0)),
                     ('B1_off_no_substitution', dict(phi=0.0))):
        pk = dict(p); pk.update(mod)
        yk = equilibrium(pk)
        _, _, o = run(pk, yk, ai_on=True)
        _, _, o0 = run(pk, yk, ai_on=False)
        knock[tag] = dict(S_gap_pct=round(float(rel(ser(o, 'S')[-1],
                                                    ser(o0, 'S')[-1])), 2))
    knock['full_model'] = dict(S_gap_pct=k['senior_gap_year30_pct'])
    out['loop_knockout'] = knock

    # ------------------------------------------------ extreme-condition tests
    ext = {}
    pz = dict(p); pz['G'] = 0.0
    _, _, o = run(pz, y0, ai_on=True)
    ext['no_entrant_inflow'] = dict(S30=round(float(ser(o, 'S')[-1]), 2),
                                    J30=round(float(ser(o, 'J')[-1]), 2),
                                    hire30=round(float(ser(o, 'hire')[-1]), 3))
    pz = dict(p); pz['A0'] = 0.0; pz['A_max'] = 0.0
    yz = equilibrium(pz)
    _, _, o = run(pz, yz, ai_on=True)
    ext['zero_automation'] = dict(
        S_drift_pct=round(float(rel(ser(o, 'S')[-1], ser(o, 'S')[0])), 4),
        q=round(float(ser(o, 'q')[-1]), 3))
    pz = dict(p); pz['A_max'] = 1.0; pz['c_diff'] = 5.0
    _, _, o = run(pz, y0, ai_on=True)
    ext['instant_full_automation'] = dict(
        S30=round(float(ser(o, 'S')[-1]), 2),
        J30=round(float(ser(o, 'J')[-1]), 2),
        q30=round(float(ser(o, 'q')[-1]), 4))
    _, _, o = run(p, y0, horizon=200.0, ai_on=False)
    ext['equilibrium_drift_200yr_pct'] = round(
        float(rel(ser(o, 'S')[-1], ser(o, 'S')[0])), 5)
    # integration-error check: halve the step
    _, _, oh = run(p, y0, dt=DT / 2, ai_on=True)
    ext['halved_step_S30_diff_pct'] = round(
        float(rel(ser(oh, 'S')[-1], Sb[-1])), 5)
    out['extreme_conditions'] = ext

    # -------------------------------------------- LHS sensitivity with PRCC
    keys = ['phi', 'nu', 'theta', 'lam', 'a_ment', 'tau0', 'mstar', 'delta',
            'A_max', 'c_diff', 'sigma', 'tauS', 'w_sens', 'ustar', 'g']
    lo = np.array([0.45, 0.080, 0.35, 0.08, 0.30, 5.00, 0.075, 0.070,
                   0.55, 0.28, 0.24, 14.0, 0.30, 0.84, 0.000])
    hi = np.array([0.78, 0.185, 0.75, 0.38, 0.62, 7.20, 0.130, 0.165,
                   0.85, 0.55, 0.36, 20.0, 0.80, 0.92, 0.018])
    N = 500
    kk = len(keys)
    Xu = np.empty((N, kk))
    for j in range(kk):
        Xu[:, j] = (rng.permutation(N) + rng.random(N)) / N
    X = lo + Xu * (hi - lo)
    resp = np.empty((N, 4))
    for i in range(N):
        pi_ = dict(p)
        for j, key in enumerate(keys):
            pi_[key] = float(X[i, j])
        yi = equilibrium(pi_)
        _, _, o1 = run(pi_, yi, ai_on=True)
        _, _, o0 = run(pi_, yi, ai_on=False)
        resp[i, 0] = rel(ser(o1, 'S')[-1], ser(o0, 'S')[-1])
        resp[i, 1] = rel(ser(o1, 'Y')[-1], ser(o0, 'Y')[-1])
        resp[i, 2] = ser(o1, 'tau')[-1]
        resp[i, 3] = rel(ser(o1, 'hire')[int(round(5 / DT))],
                         ser(o0, 'hire')[int(round(5 / DT))])

    def ranks(v):
        return (np.argsort(np.argsort(v)) + 1).astype(float)

    def prcc(Xm, y):
        Xr = np.column_stack([ranks(Xm[:, j]) for j in range(Xm.shape[1])])
        yr = ranks(y)
        Z = np.column_stack([np.ones(len(yr)), Xr])
        res = {}
        for j in range(Xm.shape[1]):
            cols = [c for c in range(Z.shape[1]) if c != j + 1]
            Zo = Z[:, cols]
            rx = Xr[:, j] - Zo @ np.linalg.lstsq(Zo, Xr[:, j], rcond=None)[0]
            ry = yr - Zo @ np.linalg.lstsq(Zo, yr, rcond=None)[0]
            r = float(np.corrcoef(rx, ry)[0, 1])
            dfree = len(yr) - 2 - (Xm.shape[1] - 1)
            tv = r * np.sqrt(max(dfree, 1) / max(1 - r ** 2, 1e-12))
            res[keys[j]] = dict(prcc=round(r, 4),
                                p=round(float(2 * st.t.sf(abs(tv), max(dfree, 1))), 6))
        return res

    def dist(v):
        return dict(mean=round(float(v.mean()), 2), sd=round(float(v.std(ddof=1)), 2),
                    p05=round(float(np.percentile(v, 5)), 2),
                    p50=round(float(np.percentile(v, 50)), 2),
                    p95=round(float(np.percentile(v, 95)), 2),
                    share_negative=round(float((v < 0).mean()), 4))

    out['sensitivity'] = dict(
        n_runs=N, method='Latin hypercube sampling with partial rank correlation',
        ranges={key: [float(lo[j]), float(hi[j])] for j, key in enumerate(keys)},
        senior_gap=dist(resp[:, 0]), output_gap=dist(resp[:, 1]),
        hiring_gap_year5=dist(resp[:, 3]),
        tau30=dict(mean=round(float(resp[:, 2].mean()), 2),
                   sd=round(float(resp[:, 2].std(ddof=1)), 2)),
        prcc_senior=prcc(X, resp[:, 0]), prcc_output=prcc(X, resp[:, 1]))

    # ------------------------------------------- policy robustness under LHS
    sub = rng.choice(N, 160, replace=False)
    rob = {t_: [] for t_ in ('P1', 'P2', 'P3', 'P4', 'P5')}
    for i in sub:
        pi_ = dict(p)
        for j, key in enumerate(keys):
            pi_[key] = float(X[i, j])
        yi = equilibrium(pi_)
        _, _, o0 = run(pi_, yi, ai_on=True)
        s0 = ser(o0, 'S')[-1]
        for t_ in rob:
            _, _, o1 = run(pi_, yi, ai_on=True, policy=POLICIES[t_])
            rob[t_].append(float(rel(ser(o1, 'S')[-1], s0)))
    out['policy_robustness'] = {
        t_: dict(mean=round(float(np.mean(v)), 2), sd=round(float(np.std(v, ddof=1)), 2),
                 p05=round(float(np.percentile(v, 5)), 2),
                 p95=round(float(np.percentile(v, 95)), 2),
                 share_positive=round(float(np.mean(np.array(v) > 0)), 4), n=len(v))
        for t_, v in rob.items()}

    # ---------------------------------------------------------- trajectories
    step = 10
    traj = {'t': [round(float(x), 3) for x in ts[::step]]}
    for tag, o in (('cf', oc), ('base', ob)):
        for v in ('S', 'J', 'P', 'Kp', 'A', 'tau', 'm', 'q', 'hire', 'promote',
                  'Y', 'ment_share', 'util', 'adequacy', 'workforce'):
            traj[f'{tag}_{v}'] = [round(float(x), 5) for x in ser(o, v)[::step]]
    for tag in POLICIES:
        _, _, o = run(p, y0, ai_on=True, policy=POLICIES[tag])
        for v in ('S', 'J', 'Y', 'tau', 'hire', 'promote'):
            traj[f'{tag}_{v}'] = [round(float(x), 5) for x in ser(o, v)[::step]]
    json.dump(traj, open(os.path.join(HERE, 'p7_traj.json'), 'w'))
    json.dump(out, open(os.path.join(HERE, 'p7_model.json'), 'w'), indent=1)

    # ------------------------------------------------------------- console
    print('equilibrium:', out['initial_state'])
    print('initial aux:', out['initial_aux'])
    print('\nkey results:'); [print('  %-28s %s' % (a, b)) for a, b in k.items()]
    print('\ntipping:', out['tipping'])
    print('\npolicies:')
    for t_ in ('P0', 'P1', 'P2', 'P3', 'P4', 'P5'):
        d = pol[t_]
        print('  %s %-30s S30=%7.2f  vsBase %+6.2f%%  tau %5.2f  conv %.3f  J %6.2f'
              % (t_, d['name'], d['S30'], d['S_vs_base_pct'], d['tau30'],
                 d['conversion'], d['J30']))
    print('  synergy %+.2f pp (sum of singles %.2f)'
          % (pol['P5']['synergy_pp'], pol['P5']['sum_of_singles_pct']))
    print('\nknockouts:', json.dumps(knock))
    print('extreme:', json.dumps(ext))
    print('\nsensitivity senior:', json.dumps(out['sensitivity']['senior_gap']))
    print('sensitivity output:', json.dumps(out['sensitivity']['output_gap']))
    print('PRCC senior:', json.dumps({a: b['prcc'] for a, b in
                                      out['sensitivity']['prcc_senior'].items()}))
    print('robustness:', json.dumps(out['policy_robustness']))


if __name__ == '__main__':
    main()
