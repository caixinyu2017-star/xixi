# -*- coding: utf-8 -*-
"""A two-tier search-and-matching model of the job ladder with AI and training.

Workers are junior (entry level) or senior (experienced).  Entry-level jobs are
a joint product: they produce output *and* they are the only technology by which
seniors are created.  Artificial intelligence substitutes for junior tasks in
production but cannot mentor, so it degrades the first component of that joint
product without touching the second.  Two wedges separate the private from the
social return to entry-level hiring and training:

  * hold-up  - mentoring intensity is chosen after the wage is set and is not
    contractible, so the firm bears the whole cost and keeps only its
    bargaining share of the return;
  * poaching - a trained senior is lost to rival firms at rate phi, which the
    firm discounts but the planner does not, because the worker keeps the job.

Under the Hosios condition, with no poaching and with contractible training the
decentralised steady state coincides exactly with the constrained planner's;
that identity is used as an internal validity check (see `efficiency_check`).

All equations are steady state, continuous time, risk neutral.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, root

# --------------------------------------------------------------- parameters
BASE = dict(
    # discounting and demography ------------------------------------------
    r=0.040,            # discount rate
    omega=0.025,        # retirement / labour-force exit rate (40-year career)
    # separations ----------------------------------------------------------
    delta_j=0.220,      # junior separation rate
    delta_s=0.085,      # senior separation rate
    phi=0.180,          # poaching rate: trained seniors lost to rival firms
    # matching -------------------------------------------------------------
    mu_j=1.000,         # matching efficiency, junior tier (normalisation)
    mu_s=1.000,         # matching efficiency, senior tier (normalisation)
    eta=0.500,          # matching elasticity w.r.t. unemployment
    beta=0.500,         # worker bargaining power (Hosios at beta = eta)
    c_j=0.320,          # junior vacancy flow cost
    c_s=0.520,          # senior vacancy flow cost
    # production -----------------------------------------------------------
    Z=1.000,            # total factor productivity
    alpha=0.400,        # weight on the junior-task bundle
    z_j=1.000,          # entry-level task units per entry-level worker (norm.)
    rho=0.600,          # CES substitution parameter (sigma = 1/(1-rho) = 2.5)
    s_y=0.650,          # output elasticity of the labour-AI bundle (fixed factor)
    chi=1.000,          # AI efficiency in junior tasks (normalisation)
    p_a=0.300,          # price of one efficiency unit of AI
    # training -------------------------------------------------------------
    pibar=0.520,        # promotion scale
    psi=0.400,          # elasticity of promotion to mentoring
    train_mode="holdup",  # "holdup" (non-contractible) or "joint" (contractible)
    # wage setting ---------------------------------------------------------
    gamma_w=0.800,      # real rigidity of the entry wage (0 = flexible Nash)
    w_ref=0.0,          # reference entry wage; 0 switches rigidity off
    # outside option -------------------------------------------------------
    b=0.320,            # flow value of non-employment
    # policy instruments (all zero in the baseline) ------------------------
    s_w=0.0,            # junior wage subsidy (share of the junior wage bill)
    s_m=0.0,            # mentoring / training credit (share of mentoring cost)
    s_v=0.0,            # junior vacancy-cost subsidy
    s_vs=0.0,           # senior vacancy-cost subsidy (implementation exercise only)
    t_a=0.0,            # tax on the AI input
)

POLICIES = ("s_w", "s_m", "s_v", "s_vs", "t_a")

STOCKS = ("u_j", "e_j", "u_s", "e_s")


# --------------------------------------------------------------- primitives
def rates(theta, p, tier="j"):
    """Job-finding and vacancy-filling rates of a Cobb-Douglas matching function."""
    theta = min(max(theta, 1e-9), 1e9)
    mu = p["mu_j"] if tier == "j" else p["mu_s"]
    f = mu * theta ** (1.0 - p["eta"])
    q = mu * theta ** (-p["eta"])
    return f, q


def promotion(m, p):
    """Promotion hazard and its derivative for mentoring intensity m."""
    m = max(m, 1e-12)
    pi = p["pibar"] * m ** p["psi"]
    dpi = p["pibar"] * p["psi"] * m ** (p["psi"] - 1.0)
    return pi, dpi


def steady_stocks(f_j, f_s, pi, p):
    """Stationary distribution over the four labour-market states."""
    w, dj, ds = p["omega"], p["delta_j"], p["delta_s"]
    # u_j: inflow w (entrants) + dj e_j ; outflow (f_j + w) u_j
    # e_j: inflow f_j u_j            ; outflow (dj + pi + w) e_j
    # u_s: inflow ds e_s             ; outflow (f_s + w) u_s
    # e_s: inflow pi e_j + f_s u_s   ; outflow (ds + w) e_s
    A = np.array([
        [-(f_j + w),      dj,             0.0,          0.0],
        [f_j,            -(dj + pi + w),  0.0,          0.0],
        [0.0,             0.0,           -(f_s + w),    ds],
        [1.0,             1.0,            1.0,          1.0],   # adding up
    ])
    rhs = np.array([-w, 0.0, 0.0, 1.0])
    x = np.linalg.solve(A, rhs)
    return dict(zip(STOCKS, x))


# --------------------------------------------------------------- production
def production(Ej, Es, m, A, p):
    """CES over an AI-augmented junior-task bundle and effective senior labour.

    One entry-level worker supplies z_j efficiency units of entry-level task
    input and one efficiency unit of AI supplies chi, so 1/z_j (with chi = 1)
    is the number of entry-level workers one unit of AI displaces.  Mentoring
    absorbs m units of senior time per junior employee per unit time, so
    effective senior input is Es - m*Ej.  The bundle enters output with
    elasticity s_y < 1; the residual accrues to a fixed factor (physical and
    organisational capital) that is not modelled explicitly.
    """
    rho, s = p["rho"], p["s_y"]
    Xj = max(p["z_j"] * Ej + p["chi"] * A, 1e-12)
    Xs = max(Es - m * Ej, 1e-12)
    inner = p["alpha"] * Xj ** rho + (1.0 - p["alpha"]) * Xs ** rho
    Y = p["Z"] * inner ** (s / rho)
    common = p["Z"] * s * inner ** (s / rho - 1.0)
    Fj = common * p["alpha"] * Xj ** (rho - 1.0)
    Fs = common * (1.0 - p["alpha"]) * Xs ** (rho - 1.0)
    return Y, Fj, Fs, Xj, Xs


def ai_demand(Ej, Es, m, p, taxed=True):
    """AI input from the first-order condition chi * dY/dXj = p_a (1 + t_a)."""
    price = p["p_a"] * (1.0 + (p["t_a"] if taxed else 0.0))

    def gap(A):
        _, Fj, _, _, _ = production(Ej, Es, m, A, p)
        return p["chi"] * Fj - price

    if gap(0.0) <= 0.0:
        return 0.0
    hi = 1.0
    while gap(hi) > 0.0 and hi < 1e8:
        hi *= 2.0
    return brentq(gap, 0.0, hi, xtol=1e-13, rtol=1e-14)


# --------------------------------------------------------------- values
def values(Fj, Fs, f_j, f_s, pi, m, p):
    """Firm and worker values with Nash-bargained wages.

    beta is the worker's bargaining power, so the firm keeps a share 1 - beta
    of each match surplus.  The firm discounts the senior job by the poaching
    rate phi; the worker does not, because a poached worker keeps a senior job
    at the going wage.  That asymmetry is the poaching wedge.
    """
    r, w_, dj, ds, ph = p["r"], p["omega"], p["delta_j"], p["delta_s"], p["phi"]
    beta = p["beta"]
    mcost = (1.0 - p["s_m"]) * m * Fs        # flow mentoring cost per junior

    # --- senior tier ------------------------------------------------------
    Rs_f = r + ds + w_ + ph                  # firm's effective senior discount
    denom_s = r + ds + w_ + f_s              # worker's surplus discount

    def nash_s(w_s):
        return beta * (Fs - w_s) / Rs_f - (1.0 - beta) * (w_s - p["b"]) / denom_s

    w_s = brentq(nash_s, p["b"] - 20.0, Fs + 20.0, xtol=1e-14, rtol=1e-14)
    Js = (Fs - w_s) / Rs_f
    Ws_Us = (w_s - p["b"]) / denom_s
    Us = (p["b"] + f_s * Ws_Us) / (r + w_)
    Ws = Us + Ws_Us

    # channel deactivation: hold the promotion pay-off at its reference value
    frz = p.get("_frz") or {}
    if "J_s" in frz:
        Js = frz["J_s"]
    if "W_s" in frz:
        Ws = frz["W_s"]

    # --- junior tier ------------------------------------------------------
    Rj = r + dj + w_ + pi

    def junior(w_j):
        Jj = (Fj - w_j * (1.0 - p["s_w"]) - mcost + pi * Js) / Rj
        # r W_j = w_j + pi (W_s - W_j) + dj (U_j - W_j) - omega W_j
        # r U_j = b + f_j (W_j - U_j) - omega U_j
        M = np.array([[r + pi + dj + w_, -dj],
                      [-f_j,             r + f_j + w_]])
        v = np.array([w_j + pi * Ws, p["b"]])
        Wj, Uj = np.linalg.solve(M, v)
        return Jj, Wj - Uj, Wj, Uj

    def nash_j(w_j):
        Jj, Wj_Uj, _, _ = junior(w_j)
        return beta * Jj - (1.0 - beta) * Wj_Uj

    lo, hi = p["b"] - 30.0, Fj + pi * Js + 30.0
    w_j = brentq(nash_j, lo, hi, xtol=1e-14, rtol=1e-14)
    # Real rigidity of the entry wage in the manner of Blanchard and Gali: the
    # posted wage is a geometric average of the bargained wage and a reference
    # wage anchored by statutory minima and compressed graduate pay scales.
    # gamma_w = 0 is the flexible Nash economy and gamma_w = 1 a fixed entry
    # wage.  At the reference point the rule is an identity, so the calibration
    # is unaffected by the value of gamma_w.
    w_ref, g = p.get("w_ref", 0.0), p.get("gamma_w", 0.0)
    if w_ref > 0.0 and g > 0.0:
        w_j = max(w_j, 1e-9) ** (1.0 - g) * w_ref ** g
    Jj, Wj_Uj, Wj, Uj = junior(w_j)

    Sj = Jj + Wj_Uj
    Ss = Js + Ws_Us
    return dict(w_j=w_j, w_s=w_s, J_j=Jj, J_s=Js, W_j=Wj, W_s=Ws, U_j=Uj, U_s=Us,
                Sj=Sj, Ss=Ss, Wj_Uj=Wj_Uj, Ws_Us=Ws_Us)


def mentoring_gap(V, Fs, m, p):
    """Firm's mentoring first-order condition, written as a residual.

    holdup: the wage is set before mentoring is chosen and mentoring is not
    contractible, so the firm maximises J_j taking w_j as given,
        pi'(m) (J_s - J_j) = (1 - s_m) F_s.
    joint:  mentoring is contractible and the pair maximises the joint surplus,
        pi'(m) [(J_s + W_s - U_j) - S_j] = (1 - s_m) F_s.
    """
    _, dpi = promotion(m, p)
    rhs = (1.0 - p["s_m"]) * Fs
    if p.get("train_mode", "holdup") == "joint":
        ret = (V["J_s"] + V["W_s"] - V["U_j"]) - V["Sj"]
    else:
        ret = V["J_s"] - V["J_j"]
    return dpi * ret - rhs


# --------------------------------------------------------------- equilibrium
def _core(theta_j, theta_s, m, p):
    f_j, q_j = rates(theta_j, p, "j")
    f_s, q_s = rates(theta_s, p, "s")
    pi, dpi = promotion(m, p)
    st = steady_stocks(f_j, f_s, pi, p)
    A = ai_demand(st["e_j"], st["e_s"], m, p)
    Y, Fj, Fs, Xj, Xs = production(st["e_j"], st["e_s"], m, A, p)
    frz = p.get("_frz") or {}
    Fj = frz.get("F_j", Fj)
    Fs = frz.get("F_s", Fs)
    Gj = p["z_j"] * Fj              # marginal product of one entry-level worker
    return f_j, q_j, f_s, q_s, pi, dpi, st, A, Y, Fj, Fs, Xj, Xs, Gj


def residuals(x, p):
    """Free entry on both tiers plus the firm's mentoring first-order condition.

    Any entry of p["_frz"] holds the named object at a reference value; the
    corresponding equilibrium condition is replaced by the pinning condition.
    This is the device used for the channel decomposition of Section 4.
    """
    theta_j, theta_s, m = np.exp(np.clip(x, -30.0, 20.0))
    f_j, q_j, f_s, q_s, pi, dpi, st, A, Y, Fj, Fs, Xj, Xs, Gj = _core(
        theta_j, theta_s, m, p)
    V = values(Gj, Fs, f_j, f_s, pi, m, p)
    frz = p.get("_frz") or {}
    r1 = p["c_j"] * (1.0 - p["s_v"]) / q_j - V["J_j"]
    if "theta_s" in frz:
        r2 = np.log(theta_s) - np.log(frz["theta_s"])
    else:
        r2 = p["c_s"] * (1.0 - p["s_vs"]) / q_s - V["J_s"]
    if "m" in frz:
        r3 = np.log(m) - np.log(frz["m"])
    else:
        r3 = mentoring_gap(V, Fs, m, p)
    return np.array([r1, r2, r3])


STARTS = ([6.00, 3.50, 0.011], [0.90, 0.60, 0.35], [0.40, 0.30, 0.20],
          [1.60, 1.10, 0.60], [0.20, 0.15, 0.10], [3.00, 2.00, 0.90],
          [0.06, 0.05, 0.05], [12.0, 7.00, 0.05], [0.50, 0.50, 0.02],
          [20.0, 10.0, 0.003], [2.00, 1.00, 0.002])

# multiplicative perturbations applied around a supplied starting point
_JITTER = ((1.0, 1.0, 1.0), (2.0, 1.5, 3.0), (0.5, 0.7, 0.3),
           (4.0, 2.0, 8.0), (1.5, 1.0, 0.2), (8.0, 3.0, 20.0),
           (1.0, 1.0, 0.05), (1.0, 1.0, 20.0))


def _guesses(x0):
    """Starting points: perturbations of x0 first, then a fixed coarse grid."""
    out = []
    if x0 is not None:
        x0 = np.asarray(x0, float)
        for f in _JITTER:
            out.append(x0 + np.log(np.array(f)))
    out.extend(np.log(np.array(s)) for s in STARTS)
    return out


def solve(p=None, x0=None, tol=1e-9):
    p = dict(BASE) if p is None else p
    best, best_err = None, np.inf
    for g in _guesses(x0):
        try:
            sol = root(residuals, g, args=(p,), method="hybr", tol=1e-13)
            err = float(np.max(np.abs(residuals(sol.x, p))))
        except Exception:
            continue
        if err < best_err:
            best, best_err = sol.x, err
        if err < tol:
            break
    if best is None:
        raise RuntimeError("no solution attempt succeeded")
    return report(best, p), bool(best_err < tol), best


def report(x, p):
    theta_j, theta_s, m = np.exp(np.clip(x, -30.0, 20.0))
    f_j, q_j, f_s, q_s, pi, dpi, st, A, Y, Fj, Fs, Xj, Xs, Gj = _core(
        theta_j, theta_s, m, p)
    V = values(Gj, Fs, f_j, f_s, pi, m, p)

    v_j, v_s = theta_j * st["u_j"], theta_s * st["u_s"]
    H_j = f_j * st["u_j"]
    ai_cost = p["p_a"] * A
    vac_cost = p["c_j"] * v_j + p["c_s"] * v_s
    train_cost = m * Fs * st["e_j"]
    welfare = Y - vac_cost - ai_cost + p["b"] * (st["u_j"] + st["u_s"])
    fiscal = (p["s_w"] * V["w_j"] * st["e_j"] + p["s_m"] * m * Fs * st["e_j"]
              + p["s_v"] * p["c_j"] * v_j + p["s_vs"] * p["c_s"] * v_s
              - p["t_a"] * p["p_a"] * A)
    wagebill = V["w_j"] * st["e_j"] + V["w_s"] * st["e_s"]

    out = dict(theta_j=theta_j, theta_s=theta_s, m=m, pi=pi, dpi=dpi,
               f_j=f_j, f_s=f_s, q_j=q_j, q_s=q_s, A=A, Y=Y, F_j=Fj, F_s=Fs,
               X_j=Xj, X_s=Xs, G_j=Gj, H_j=H_j, v_j=v_j, v_s=v_s, welfare=welfare,
               ai_cost=ai_cost, vac_cost=vac_cost, train_cost=train_cost,
               fiscal=fiscal, wagebill=wagebill,
               ai_share=p["chi"] * A / Xj, wage_ratio=V["w_s"] / V["w_j"],
               u_rate_j=st["u_j"] / (st["u_j"] + st["e_j"]),
               u_rate_s=st["u_s"] / (st["u_s"] + st["e_s"]),
               labour_share=wagebill / Y,
               hire_cost_j=(p["c_j"] * (1.0 - p["s_v"]) / q_j) / V["w_j"],
               hire_cost_s=(p["c_s"] / q_s) / V["w_s"],
               repl_rate=p["b"] / V["w_j"],
               # over-identifying checks, not targeted in estimation
               senior_emp_share=st["e_s"] / (st["e_s"] + st["e_j"]),
               mentor_share=m * st["e_j"] / max(st["e_s"], 1e-12),
               search_months_j=12.0 / f_j,
               train_share=train_cost / max(wagebill, 1e-12),
               promo_years=1.0 / pi)
    out.update(st)
    out.update(V)
    return out


# --------------------------------------------------------------- planner
def costates(f_j, f_s, pi, m, Gj, Fs, p):
    """Steady-state costates of the constrained planner's Hamiltonian."""
    r, w_, dj, ds, eta = p["r"], p["omega"], p["delta_j"], p["delta_s"], p["eta"]
    # order: lam_uj, lam_ej, lam_us, lam_es
    M = np.array([
        [r + w_ + eta * f_j, -eta * f_j,        0.0,                0.0],
        [-dj,                r + dj + pi + w_,  0.0,               -pi],
        [0.0,                0.0,               r + w_ + eta * f_s, -eta * f_s],
        [0.0,                0.0,              -ds,                 r + ds + w_],
    ])
    rhs = np.array([p["b"], Gj - m * Fs, p["b"], Fs])
    lam = np.linalg.solve(M, rhs)
    return dict(zip(("lam_uj", "lam_ej", "lam_us", "lam_es"), lam))


def planner_residuals(x, p):
    """Planner optimality: two vacancy conditions and the mentoring condition.

    The planner faces the undistorted cost of every instrument, so the policy
    parameters s_v, s_m, s_w and t_a are switched off.
    """
    q = dict(p)
    for k in POLICIES:
        q[k] = 0.0
    theta_j, theta_s, m = np.exp(np.clip(x, -30.0, 20.0))
    f_j, q_j, f_s, q_s, pi, dpi, st, A, Y, Fj, Fs, Xj, Xs, Gj = _core(
        theta_j, theta_s, m, q)
    L = costates(f_j, f_s, pi, m, Gj, Fs, q)
    one_eta = 1.0 - q["eta"]
    r1 = one_eta * q_j * (L["lam_ej"] - L["lam_uj"]) - q["c_j"]
    r2 = one_eta * q_s * (L["lam_es"] - L["lam_us"]) - q["c_s"]
    r3 = dpi * (L["lam_es"] - L["lam_ej"]) - Fs
    return np.array([r1, r2, r3])


def solve_planner(p=None, x0=None, tol=1e-9):
    p = dict(BASE) if p is None else p
    best, best_err = None, np.inf
    for g in _guesses(x0):
        try:
            sol = root(planner_residuals, g, args=(p,), method="hybr", tol=1e-13)
            err = float(np.max(np.abs(planner_residuals(sol.x, p))))
        except Exception:
            continue
        if err < best_err:
            best, best_err = sol.x, err
        if err < tol:
            break
    if best is None:
        raise RuntimeError("no planner solution attempt succeeded")
    q = dict(p)
    for k in POLICIES:
        q[k] = 0.0
    out = report(best, q)
    theta_j, theta_s, m = np.exp(np.clip(best, -30.0, 20.0))
    f_j, q_j, f_s, q_s, pi, dpi, st, A, Y, Fj, Fs, Xj, Xs, Gj = _core(
        theta_j, theta_s, m, q)
    out.update(costates(f_j, f_s, pi, m, Gj, Fs, q))
    return out, bool(best_err < tol), best


def efficiency_check(p=None, verbose=True):
    """Hosios + no poaching + contractible training must decentralise the optimum."""
    p = dict(BASE if p is None else p)
    p["phi"] = 0.0
    p["beta"] = p["eta"]
    p["train_mode"] = "joint"
    p["w_ref"] = 0.0                 # flexible Nash wages
    for k in POLICIES:
        p[k] = 0.0
    mkt, ok1, _ = solve(p)
    pla, ok2, _ = solve_planner(p)
    gaps = {k: abs(mkt[k] - pla[k]) / max(abs(pla[k]), 1e-12)
            for k in ("theta_j", "theta_s", "m", "e_j", "e_s", "Y", "welfare")}
    if verbose:
        print("efficiency check (Hosios, phi = 0, contractible training)")
        for k, v in gaps.items():
            print("   %-9s market %12.8f  planner %12.8f  rel gap %.2e"
                  % (k, mkt[k], pla[k], v))
    return gaps, ok1 and ok2


if __name__ == "__main__":
    res, ok, x = solve()
    print("converged:", ok)
    for k in ("theta_j", "theta_s", "m", "pi", "promo_years", "u_rate_j",
              "u_rate_s", "wage_ratio", "ai_share", "labour_share",
              "hire_cost_j", "hire_cost_s", "repl_rate", "senior_emp_share",
              "Y", "welfare"):
        print("   %-17s %.4f" % (k, res[k]))
    print()
    efficiency_check()
