# -*- coding: utf-8 -*-
"""A two-sector, two-age search model of administrative job rationing.

The labour market has a quota sector Q, whose establishment N is fixed by
administrative rule so that its vacancies are exactly its separations plus its
retirements, and a market sector M with free entry.  The quota wage exceeds the
market wage, so young workers queue for quota jobs in the manner of Harris and
Todaro: queueing pays nothing but buys a lottery ticket on a rationed rent.

Workers are young for T_y years after entry and prime thereafter until
retirement.  An age ceiling bars prime workers from the quota examinations, so
only the young queue.  Raising the statutory retirement age lowers the
retirement hazard, which does three things at once: it shrinks the quota
sector's vacancy flow, it lengthens the expected life of a market match and so
raises vacancy creation, and it enlarges the labour force.  Which of those
dominates for the young is the question the paper answers.

All equations are steady state, continuous time, risk neutral.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

# --------------------------------------------------------------- parameters
BASE = dict(
    # discounting, ageing and retirement --------------------------------
    r=0.040,            # discount rate
    a0=23.0,            # mean age at labour-market entry
    T_y=7.0,            # years spent in the "young" tier (ages 23-30)
    R=56.3,             # effective statutory retirement age, pre-reform
    # separations --------------------------------------------------------
    delta_Q=0.020,      # separation rate, quota sector (very low)
    delta_M=0.180,      # separation rate, market sector
    # matching -----------------------------------------------------------
    eta=0.500,          # matching elasticity w.r.t. searchers
    beta=0.500,         # worker bargaining power (Hosios at beta = eta)
    mu_y=0.700,         # matching efficiency of the young, prime = 1
    c_M=0.300,          # vacancy flow cost, market sector
    # technology and administered pay ------------------------------------
    p_M=1.000,          # market-sector productivity (numeraire)
    p_Q=1.000,          # quota-sector productivity
    N_bar=8.000,        # administrative establishment of the quota sector
    w_Q=0.900,          # administered quota wage
    # outside options ----------------------------------------------------
    b=0.400,            # flow value of open search
    kappa_q=0.500,      # flow value while queueing, relative to b
    # entrants -----------------------------------------------------------
    n=1.000,            # entrant cohort flow (normalisation)
    # policy instruments (all zero in the baseline) -----------------------
    s_v=0.0,            # market vacancy subsidy
    s_N=0.0,            # proportional expansion of the quota establishment
    tau_q=0.0,          # proportional cut in the quota wage premium
    # switches -----------------------------------------------------------
    xi=0.000,           # screening value of the queue (Section 5.8 extension)
)

POLICIES = ("s_v", "s_N", "tau_q")


# --------------------------------------------------------------- primitives
def rates(p, channel=None):
    """Ageing and retirement hazards implied by the age structure.

    `channel` selects one of the three routes by which the retirement hazard
    acts, so that each can be deactivated separately for the decomposition of
    Section 5.3:
      "quota"  the establishment's replacement flow, and hence its vacancies;
      "value"  the horizon of a job, and hence its value to firm and worker;
      "demo"   the size and age composition of the labour force.
    A key of the form _rho_<channel> in p overrides the hazard on that route.
    """
    gamma = 1.0 / p["T_y"]
    prime_years = p["R"] - p["a0"] - p["T_y"]
    if prime_years <= 0.5:
        prime_years = 0.5
    rho = 1.0 / prime_years
    if channel is not None:
        rho = p.get("_rho_" + channel, rho)
    return gamma, rho


def quota(p):
    """Establishment and administered wage after policy."""
    return p["N_bar"] * (1.0 + p["s_N"]), p["w_Q"] * (1.0 - p["tau_q"])


def wages(theta, p):
    """Nash-bargained market wages and the values they imply.

    Young and prime matches differ only in their expected life: a young match
    is not exposed to retirement until the worker ages, so it is worth more to
    the firm and commands a different split.
    """
    r, dM, beta = p["r"], p["delta_M"], p["beta"]
    gamma, rho = rates(p, "value")
    f_p = theta ** (1.0 - p["eta"])
    f_y = p["mu_y"] * f_p
    b = p["b"]

    # --- prime tier, closed form
    R_p = r + dM + rho
    D_p = r + dM + f_p + rho
    w_p = ((beta * D_p * p["p_M"] + (1.0 - beta) * R_p * b)
           / (beta * D_p + (1.0 - beta) * R_p))
    J_p = (p["p_M"] - w_p) / R_p
    Dl_p = (w_p - b) / D_p

    # --- young tier, given the prime continuation values
    R_y = r + dM + gamma
    D_y = r + dM + f_y + gamma
    w_y = ((beta * D_y * (p["p_M"] + gamma * J_p)
            + (1.0 - beta) * R_y * (b - gamma * Dl_p))
           / (beta * D_y + (1.0 - beta) * R_y))
    J_y = (p["p_M"] - w_y + gamma * J_p) / R_y
    Dl_y = (w_y - b + gamma * Dl_p) / D_y

    # --- values of search
    V_p = (b + f_p * Dl_p) / (r + rho)
    V_y = (b + f_y * Dl_y + gamma * V_p) / (r + gamma)
    return dict(f_y=f_y, f_p=f_p, w_y=w_y, w_p=w_p, J_y=J_y, J_p=J_p,
                Dl_y=Dl_y, Dl_p=Dl_p, V_y=V_y, V_p=V_p)


def queue_hazard(V, p):
    """Hazard of winning a quota job that makes a young worker indifferent.

    Queueing yields the flow value kappa_q * b and a lottery on the quota job;
    open search yields b and the market hazard.  Indifference pins lambda_Q.
    """
    r = p["r"]
    gamma, rho = rates(p, "value")
    N, wQ = quota(p)
    V_y, V_p = V["V_y"], V["V_p"]
    W_q_p = (wQ + p["delta_Q"] * V_p) / (r + p["delta_Q"] + rho)
    W_q_y = (wQ + p["delta_Q"] * V_y + gamma * W_q_p) / (r + p["delta_Q"] + gamma)
    gain = W_q_y - V_y
    need = (r + gamma) * V_y - p["kappa_q"] * p["b"] - gamma * V_p
    if gain <= 1e-12:
        return np.inf, W_q_y, W_q_p          # quota job not worth queueing for
    return need / gain, W_q_y, W_q_p


def stocks(lam_Q, V, p):
    """Steady-state stocks given the queue hazard and the market hazards."""
    gamma, rho_q = rates(p, "quota")
    _, rho_d = rates(p, "demo")
    N, _ = quota(p)
    dQ, dM = p["delta_Q"], p["delta_M"]
    f_y, f_p = V["f_y"], V["f_p"]

    # quota employment splits mechanically between the two age tiers
    e_q = N * (dQ + rho_q) / (dQ + rho_q + gamma)
    E_q = N - e_q
    v_Q = (dQ + gamma) * e_q                 # quota hires per unit time
    u_q = v_Q / lam_Q if np.isfinite(lam_Q) and lam_Q > 0 else 0.0

    # young open searchers, from the young unemployment flow balance
    denom = gamma * (1.0 + f_y / (dM + gamma))
    u_m = (p["n"] + dQ * e_q - (lam_Q + gamma) * u_q) / denom
    e_m = f_y * u_m / (dM + gamma)

    # prime block: two linear equations in (U_m, E_m)
    A = np.array([[f_p + rho_d, -dM],
                  [-f_p,      dM + rho_d]])
    rhs = np.array([gamma * (u_q + u_m) + dQ * E_q, gamma * e_m])
    U_m, E_m = np.linalg.solve(A, rhs)

    I_y = p["n"] + dQ * e_q + dM * e_m
    a_q = (lam_Q + gamma) * u_q / I_y if I_y > 0 else 0.0
    return dict(u_q=u_q, u_m=u_m, e_q=e_q, e_m=e_m, U_m=U_m, E_q=E_q, E_m=E_m,
                v_Q=v_Q, a_q=a_q, I_y=I_y)


def free_entry_gap(theta, p):
    """Residual of the market-sector free-entry condition."""
    V = wages(theta, p)
    lam_Q, _, _ = queue_hazard(V, p)
    st = stocks(lam_Q, V, p)
    if st["u_m"] <= 0 or st["U_m"] <= 0 or st["E_m"] < 0:
        return 1e6
    S_e = p["mu_y"] * st["u_m"] + st["U_m"]          # effective searchers
    om_y = p["mu_y"] * st["u_m"] / S_e
    J_bar = om_y * V["J_y"] + (1.0 - om_y) * V["J_p"]
    q = theta ** (-p["eta"])
    return p["c_M"] * (1.0 - p["s_v"]) / q - J_bar


def solve(p=None, lo=1e-4, hi=60.0):
    """Solve for market tightness; everything else is recursive in it."""
    p = dict(BASE) if p is None else p
    try:
        g_lo, g_hi = free_entry_gap(lo, p), free_entry_gap(hi, p)
    except Exception:
        return None, False
    if not (np.isfinite(g_lo) and np.isfinite(g_hi)) or g_lo * g_hi > 0:
        # scan for a bracket
        grid = np.geomspace(lo, hi, 200)
        prev_t = prev_g = None
        for t in grid:
            try:
                g = free_entry_gap(t, p)
            except Exception:
                continue
            if not np.isfinite(g) or abs(g) > 1e5:
                prev_t = prev_g = None
                continue
            if prev_g is not None and prev_g * g < 0:
                theta = brentq(free_entry_gap, prev_t, t, args=(p,),
                               xtol=1e-14, rtol=1e-15)
                return report(theta, p), True
            prev_t, prev_g = t, g
        return None, False
    theta = brentq(free_entry_gap, lo, hi, args=(p,), xtol=1e-14, rtol=1e-15)
    return report(theta, p), True


def report(theta, p):
    gamma, rho = rates(p)
    N, wQ = quota(p)
    V = wages(theta, p)
    lam_Q, W_q_y, W_q_p = queue_hazard(V, p)
    st = stocks(lam_Q, V, p)

    young = st["u_q"] + st["u_m"] + st["e_q"] + st["e_m"]
    prime = st["U_m"] + st["E_q"] + st["E_m"]
    emp = st["e_q"] + st["e_m"] + st["E_q"] + st["E_m"]
    S_e = p["mu_y"] * st["u_m"] + st["U_m"]
    v_M = theta * S_e

    Y = p["p_Q"] * N + p["p_M"] * (st["e_m"] + st["E_m"])
    # the queue may screen: xi is the output gain per unit of queue length
    Y += p["xi"] * p["p_Q"] * N * (1.0 - np.exp(-st["u_q"]))
    vac_cost = p["c_M"] * v_M
    home = p["b"] * (st["u_m"] + st["U_m"]) + p["kappa_q"] * p["b"] * st["u_q"]
    welfare = Y - vac_cost + home
    L = young + prime

    wbar_M = ((V["w_y"] * st["e_m"] + V["w_p"] * st["E_m"])
              / max(st["e_m"] + st["E_m"], 1e-12))
    fiscal = (p["s_v"] * p["c_M"] * v_M
              + p["s_N"] * p["N_bar"] * wQ
              - p["tau_q"] * p["w_Q"] * N)

    out = dict(theta=theta, lam_Q=lam_Q, gamma=gamma, rho=rho, N=N, w_Q=wQ,
               v_M=v_M, L=L, young=young, prime=prime, emp=emp, Y=Y,
               welfare=welfare, vac_cost=vac_cost, fiscal=fiscal,
               W_q_y=W_q_y, W_q_p=W_q_p, wbar_M=wbar_M,
               u_rate_y=(st["u_q"] + st["u_m"]) / max(young, 1e-12),
               u_rate_p=st["U_m"] / max(prime, 1e-12),
               queue_share=st["u_q"] / max(st["u_q"] + st["u_m"], 1e-12),
               quota_share=N / max(emp, 1e-12),
               wage_premium=wQ / max(V["w_y"], 1e-12),
               repl_rate=p["b"] / max(V["w_y"], 1e-12),
               queue_years=1.0 / lam_Q if np.isfinite(lam_Q) and lam_Q > 0
               else np.inf,
               cohort_entry_Q=st["v_Q"] / p["n"],
               search_months_y=12.0 / max(V["f_y"], 1e-12),
               # welfare-relevant objects for the young
               V_entrant=V["V_y"], queue_loss=st["u_q"] * (p["p_M"]
                                                           - p["kappa_q"] * p["b"]),
               welfare_pc=welfare / max(L, 1e-12))
    out.update(st)
    out.update(V)
    return out


# --------------------------------------------------------------- benchmarks
def no_queue_counterfactual(p):
    """Welfare if quota jobs were filled without a queue.

    The queue produces nothing at the margin: the quota sector hires v_Q
    workers however long the line is.  Sending queuers to open search instead
    is therefore a pure gain, and its size measures the deadweight loss of
    administrative rationing.
    """
    q = dict(p)
    q["kappa_q"] = 0.0
    base, ok = solve(p)
    if not ok:
        return None
    # counterfactual: the same quota hires, drawn at random from open searchers
    alt = dict(p)
    alt["_no_queue"] = True
    return base


def break_even_screening(p, base=None):
    """Screening value xi that would make the observed queue efficient."""
    if base is None:
        base, ok = solve(p)
        if not ok:
            return np.nan
    target = base["queue_loss"]
    denom = base["p_Q"] * base["N"] if "p_Q" in base else p["p_Q"] * base["N"]
    return float(target / max(denom * (1.0 - np.exp(-base["u_q"])), 1e-12))


if __name__ == "__main__":
    res, ok = solve()
    print("converged:", ok)
    if ok:
        for k in ("theta", "lam_Q", "queue_years", "u_rate_y", "u_rate_p",
                  "queue_share", "quota_share", "wage_premium", "repl_rate",
                  "cohort_entry_Q", "search_months_y", "V_entrant", "L",
                  "Y", "welfare", "welfare_pc"):
            print("   %-16s %.4f" % (k, res[k]))
