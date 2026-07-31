# -*- coding: utf-8 -*-
"""
Socio-technical system dynamics model of generative AI, organisational learning
and youth (entry-level) employment.

Six state variables
    J    junior / early-career employees                 [persons]
    S    senior / experienced employees                   [persons]
    A    generative-AI capability stock                   [dmnl, 0-1]
    K    human-AI collaboration routine stock             [dmnl]
    Yd   desired (planned) output                         [output units/yr]
    Ch   perceived (smoothed) unit cost                   [cost/output]

The model is initialised in the pre-GenAI steady state; the mentoring
coefficient m is derived analytically so that the workforce structure implied by
the task-based labour demand equals the structure implied by the promotion /
attrition balance.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace, asdict, fields

import numpy as np


# ----------------------------------------------------------------------------
# Parameters
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    # --- task structure -----------------------------------------------------
    thE: float = 0.30       # share of entry (codified, routine-cognitive) tasks
    thC: float = 0.45       # share of core (intermediate) tasks
    thG: float = 0.25       # share of judgement (senior-only) tasks

    # --- automation frontier (displacement) ---------------------------------
    alpha_max: float = 0.60  # ceiling on automatable share of entry tasks
    a_alpha: float = 0.50    # half-saturation AI capability for automation
    gamma: float = 2.0       # Hill exponent

    # --- augmentation / reinstatement ---------------------------------------
    rho_max: float = 0.35    # ceiling on core tasks reinstated to AI-assisted juniors
    beta_J: float = 0.55     # AI productivity elasticity, juniors
    beta_S: float = 0.16     # AI productivity elasticity, seniors

    # --- utilisation and absorptive capacity --------------------------------
    u_max: float = 0.85      # ceiling on AI utilisation intensity
    a_u: float = 0.35        # half-saturation AI capability for utilisation
    k_h: float = 1.00        # half-saturation of the routine stock

    # --- learning system ----------------------------------------------------
    lam: float = 0.30        # routine accumulation (learning investment) rate [1/yr]
    dK: float = 0.20         # routine obsolescence rate [1/yr]

    # --- AI capability accumulation -----------------------------------------
    nu: float = 0.45         # adoption gap-closing rate [1/yr]
    dA: float = 0.05         # capability depreciation [1/yr]
    phi0: float = 0.25       # floor on absorptive capacity for adoption
    F_max: float = 1.00      # external GenAI frontier ceiling
    gF: float = 0.45         # frontier logistic growth rate [1/yr]
    tF: float = 5.00         # frontier inflection time [yr]

    # --- workforce pipeline -------------------------------------------------
    tau_dev: float = 3.0     # time to competence [yr]
    q0: float = 1.00         # half-saturation mentoring adequacy
    eta: float = 0.35        # AI-mediated knowledge scaffolding coefficient
    zeta0: float = 0.25      # floor on the skill-formation value of AI-mediated work
    dJ: float = 0.15         # junior separation rate [1/yr]
    dS: float = 0.08         # senior separation rate [1/yr]
    tau_J: float = 1.0       # junior hiring adjustment time [yr]
    tau_S: float = 2.0       # senior recruitment adjustment time [yr]
    chi_S: float = 0.03      # ceiling on external senior recruitment [1/yr]
    omega: float = 1.00      # elasticity of external senior availability to
                             # sector-wide senior formation (0 = partial
                             # equilibrium closure, 1 = sector-consistent closure)
    Om_max: float = 2.00     # ceiling on the external availability index

    # --- productivity and cost ----------------------------------------------
    piJ0: float = 1.00       # baseline junior productivity [output/person/yr]
    piS0: float = 1.60       # baseline senior productivity [output/person/yr]
    wJ: float = 1.00         # junior compensation [cost/person/yr]
    wS: float = 2.00         # senior compensation [cost/person/yr]
    pA: float = 0.05         # AI operating cost [cost/output at full utilisation]
    pK: float = 0.15         # learning investment cost [cost per routine unit]

    # --- demand -------------------------------------------------------------
    eps: float = 1.10        # elasticity of demand w.r.t. unit cost
    tau_Y: float = 2.0       # demand adjustment time [yr]
    tau_C: float = 1.0       # cost perception delay [yr]
    gY: float = 0.02         # autonomous demand growth [1/yr]

    # --- scale / numerics ---------------------------------------------------
    N_ref: float = 1000.0    # reference workforce size [persons]
    m: float = float("nan")  # mentoring capacity per senior (set at init)


def mentoring_coefficient(p: Params) -> float:
    """Value of m for which the task-based and pipeline-based workforce
    structures coincide in the pre-GenAI steady state.

    Pipeline balance:  psi(q) * J / tau_dev = dS * S with q = m*S/J,
    i.e. with r = S/J:  r = 1/(dS*tau_dev) - q0/m.
    Task-based demand: r = (thG + thC) / thE * piJ0 / piS0.
    """
    r = (p.thG + p.thC) / p.thE * p.piJ0 / p.piS0
    return p.q0 / (1.0 / (p.dS * p.tau_dev) - r)


def initial_state(p: Params, N0: float | None = None, A0: float = 0.0,
                  K0: float = 0.0) -> np.ndarray:
    """Pre-GenAI steady state."""
    N0 = p.N_ref if N0 is None else N0
    r = (p.thG + p.thC) / p.thE * p.piJ0 / p.piS0
    J0 = N0 / (1.0 + r)
    S0 = N0 - J0
    Y0 = p.piJ0 * J0 / p.thE
    C0 = (p.wJ * J0 + p.wS * S0) / Y0
    return np.array([J0, S0, A0, K0, Y0, C0], dtype=float)


# ----------------------------------------------------------------------------
# Auxiliary equations
# ----------------------------------------------------------------------------
def frontier(t: float, p: Params, genai: bool = True) -> float:
    """External generative-AI technological frontier (logistic)."""
    if not genai:
        return 0.0
    return p.F_max / (1.0 + math.exp(-p.gF * (t - p.tF)))


def auxiliaries(t: float, y: np.ndarray, p: Params, genai: bool = True) -> dict:
    J, S, A, K, Yd, Ch = y
    J = max(J, 1e-6)
    S = max(S, 1e-6)
    A = max(A, 0.0)
    K = max(K, 0.0)
    Yd = max(Yd, 1e-6)
    Ch = max(Ch, 1e-9)

    F = frontier(t, p, genai)

    # utilisation, absorptive capacity, automation, reinstatement
    u = p.u_max * A / (A + p.a_u)
    Lam = K / (K + p.k_h)
    Ag = A ** p.gamma
    alpha = p.alpha_max * Ag / (Ag + p.a_alpha ** p.gamma)
    rho = p.rho_max * u * Lam

    # effective productivity (experience compression: beta_J > beta_S)
    piJ = p.piJ0 * (1.0 + p.beta_J * u * Lam)
    piS = p.piS0 * (1.0 + p.beta_S * u * Lam)

    # task intensities per unit of output
    iJ = (1.0 - alpha) * p.thE + rho * p.thC          # junior-executable tasks
    iS = p.thG + (1.0 - rho) * p.thC                  # senior-executable tasks

    # desired labour, anchored on planned output
    DJ = Yd * iJ / piJ
    DS = Yd * iS / piS

    # capacity fulfilment
    PhiJ = piJ * J / (Yd * iJ)
    PhiS = piS * S / (Yd * iS)
    Phi = min(1.0, PhiJ, PhiS)
    Y = Yd * Phi

    # pipeline: mentoring adequacy per junior = human mentoring + AI scaffolding
    q = p.m * S / J + p.eta * A * Lam
    psi = q / (q + p.q0)
    # experiential quality of the junior task portfolio: unmediated entry work is
    # a full teacher, AI-mediated core work only to the extent that the firm has
    # built collaboration routines
    x = ((1.0 - alpha) * p.thE
         + rho * p.thC * (p.zeta0 + (1.0 - p.zeta0) * Lam)) / max(iJ, 1e-9)
    c = psi * x * J / p.tau_dev

    # external senior recruitment. Under the sector-consistent closure the pool
    # of experienced hires available on the external market is itself fed by the
    # sector's promotion flow, so a sector-wide collapse of the entry port also
    # closes the external option (composition fallacy).
    Om = min((c / max(p.dS * S, 1e-9)) ** p.omega, p.Om_max)
    eS = min(max((DS - S) / p.tau_S, 0.0), p.chi_S * S * Om)
    h = max((DJ - J) / p.tau_J + p.dJ * J + c, 0.0)

    # learning
    ell = 2.0 * p.lam * u * math.sqrt(J * S) / p.N_ref

    # cost and demand
    cost = p.wJ * J + p.wS * S + p.pA * u * Y + p.pK * ell * p.N_ref
    C = cost / max(Y, 1e-9)
    return dict(F=F, u=u, Lam=Lam, alpha=alpha, rho=rho, piJ=piJ, piS=piS,
                iJ=iJ, iS=iS, DJ=DJ, DS=DS, PhiJ=PhiJ, PhiS=PhiS, Phi=Phi, Y=Y,
                q=q, psi=psi, x=x, c=c, Om=Om, eS=eS, h=h, ell=ell, cost=cost,
                C=C)


def entry_port_elasticity(y: np.ndarray, aux: dict, p: Params) -> dict:
    """Decomposition of the elasticity of desired junior labour with respect to
    AI capability, holding planned output constant.

        E = (thC * d(rho)/d(lnA) - thE * d(alpha)/d(lnA)) / iJ - d(ln piJ)/d(lnA)
    """
    J, S, A, K, Yd, Ch = y
    A = max(A, 1e-9)
    Lam = aux["Lam"]
    Ag = A ** p.gamma
    aag = p.a_alpha ** p.gamma

    dalpha = p.alpha_max * p.gamma * Ag * aag / (Ag + aag) ** 2      # dalpha/dlnA
    du = p.u_max * p.a_u * A / (A + p.a_u) ** 2                      # du/dlnA
    drho = p.rho_max * Lam * du                                      # drho/dlnA
    dlnpiJ = p.beta_J * Lam * du / (1.0 + p.beta_J * aux["u"] * Lam)

    iJ = aux["iJ"]
    displacement = p.thE * dalpha / iJ
    reinstatement = p.thC * drho / iJ
    productivity = dlnpiJ
    return dict(displacement=displacement, reinstatement=reinstatement,
                productivity=productivity,
                E=reinstatement - displacement - productivity)


# ----------------------------------------------------------------------------
# Right-hand side and integration
# ----------------------------------------------------------------------------
def rhs(t: float, y: np.ndarray, p: Params, Y00: float, C00: float,
        genai: bool = True) -> np.ndarray:
    J, S, A, K, Yd, Ch = y
    aux = auxiliaries(t, y, p, genai)

    dJ = aux["h"] - aux["c"] - p.dJ * max(J, 0.0)
    dS = aux["c"] + aux["eS"] - p.dS * max(S, 0.0)

    LamA = p.phi0 + (1.0 - p.phi0) * aux["Lam"]
    dA = p.nu * LamA * (aux["F"] - max(A, 0.0)) - p.dA * max(A, 0.0)
    dK = aux["ell"] - p.dK * max(K, 0.0)

    target = Y00 * math.exp(p.gY * t) * (C00 / max(Ch, 1e-9)) ** p.eps
    dYd = (target - Yd) / p.tau_Y
    dCh = (aux["C"] - Ch) / p.tau_C
    return np.array([dJ, dS, dA, dK, dYd, dCh], dtype=float)


def simulate(p: Params, T: float = 20.0, dt: float = 0.0625,
             genai: bool = True, N0: float | None = None,
             A0: float = 0.0, K0: float = 0.0) -> dict:
    """Fourth-order Runge-Kutta integration; returns time series of states,
    auxiliaries and the entry-port elasticity decomposition."""
    if math.isnan(p.m):
        p = replace(p, m=mentoring_coefficient(p))

    y = initial_state(p, N0=N0, A0=A0, K0=K0)
    Y00, C00 = y[4], y[5]

    n = int(round(T / dt))
    ts = np.linspace(0.0, T, n + 1)
    Ys = np.zeros((n + 1, 6))
    Ys[0] = y

    for i in range(n):
        t = ts[i]
        k1 = rhs(t, y, p, Y00, C00, genai)
        k2 = rhs(t + dt / 2, y + dt / 2 * k1, p, Y00, C00, genai)
        k3 = rhs(t + dt / 2, y + dt / 2 * k2, p, Y00, C00, genai)
        k4 = rhs(t + dt, y + dt * k3, p, Y00, C00, genai)
        y = y + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        y = np.maximum(y, np.array([0.0, 0.0, 0.0, 0.0, 1e-6, 1e-9]))
        Ys[i + 1] = y

    keys = ["F", "u", "Lam", "alpha", "rho", "piJ", "piS", "iJ", "iS", "DJ",
            "DS", "PhiJ", "PhiS", "Phi", "Y", "q", "psi", "x", "c", "Om",
            "eS", "h", "ell", "C"]
    out = {k: np.zeros(n + 1) for k in keys}
    for k in ("displacement", "reinstatement", "productivity", "E"):
        out[k] = np.zeros(n + 1)
    for i, t in enumerate(ts):
        aux = auxiliaries(t, Ys[i], p, genai)
        for k in keys:
            out[k][i] = aux[k]
        el = entry_port_elasticity(Ys[i], aux, p)
        for k in ("displacement", "reinstatement", "productivity", "E"):
            out[k][i] = el[k]

    out.update(t=ts, J=Ys[:, 0], S=Ys[:, 1], A=Ys[:, 2], K=Ys[:, 3],
               Yd=Ys[:, 4], Ch=Ys[:, 5], N=Ys[:, 0] + Ys[:, 1], params=p,
               youth_share=Ys[:, 0] / np.maximum(Ys[:, 0] + Ys[:, 1], 1e-9))
    return out


# ----------------------------------------------------------------------------
# Outcome metrics
# ----------------------------------------------------------------------------
def metrics(run: dict, base: dict, T_eval: float = 20.0) -> dict:
    """Outcomes of `run` relative to the no-GenAI counterfactual `base`."""
    t = run["t"]
    i = int(np.argmin(np.abs(t - T_eval)))
    dt = t[1] - t[0]

    def rel(key):
        return 100.0 * (run[key][i] / base[key][i] - 1.0)

    cum_h = np.trapezoid(run["h"], t)
    cum_h0 = np.trapezoid(base["h"], t)

    ratio = run["J"] / base["J"]
    k_tr = int(np.argmin(ratio))
    trough = 100.0 * (ratio[k_tr] - 1.0)
    t_trough = t[k_tr]
    rec = np.where(ratio[k_tr:] >= 1.0)[0]
    t_rec = t[k_tr + rec[0]] if len(rec) else float("nan")

    return {
        "dJ": rel("J"),
        "dS": rel("S"),
        "dY": rel("Y"),
        "dC": rel("C"),
        "d_hires": 100.0 * (cum_h / cum_h0 - 1.0),
        "youth_share": 100.0 * run["youth_share"][i],
        "d_youth_share_pp": 100.0 * (run["youth_share"][i] - base["youth_share"][i]),
        "trough_pct": trough,
        "t_trough": t_trough,
        "t_recovery": t_rec,
        "K_T": run["K"][i],
        "Lam_T": run["Lam"][i],
        "E_T": run["E"][i],
        "alpha_T": run["alpha"][i],
        "rho_T": run["rho"][i],
        "psi_T": run["psi"][i],
        "x_T": run["x"][i],
        "Phi_T": run["Phi"][i],
    }
