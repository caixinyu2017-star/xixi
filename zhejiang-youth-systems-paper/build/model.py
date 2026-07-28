# -*- coding: utf-8 -*-
"""Youth School-to-work Transition System (YSTS): a six-state feedback model
of graduate labour-market entry, calibrated to Zhejiang / China moments.

States (10^4 persons unless noted)
    S  open searchers
    Q  exam-oriented queuers ("slow employment")
    M  well-matched employment
    U  mismatched / under-matched employment
    H  mean effective employability capital of the searching pool  (index 0-1)
    A  mean aspiration (reservation job-quality) threshold          (index 0-1)

The vector field is smooth (logistic transitions, harmonic-mean saturations),
so fixed points, Jacobians and continuation curves are well defined.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import root

EPS = 1e-9
STATES = ("S", "Q", "M", "U", "H", "A")

# --------------------------------------------------------------- parameters
BASE = dict(
    # cohort inflow ---------------------------------------------------------
    Phi0=30.0,          # degree-holding entrants at t=0 (2015), 10^4 persons
    gPhi=0.050,         # annual growth of the entrant cohort
    omega=0.125,        # exit rate from the youth window (8-year window)
    # labour demand ---------------------------------------------------------
    V0=38.0,            # open vacancies at t=0 (10^4); scale normalisation
    gV=0.030,           # autonomous vacancy growth
    phi=1.60,           # elasticity of vacancies to digital intensity
    # digital transformation (logistic) -------------------------------------
    Psi0=0.090, PsiMax=0.200, rPsi=0.080,
    # employer skill threshold ----------------------------------------------
    theta0=0.500, kappa=2.20, kappa2=0.150,
    # matching --------------------------------------------------------------
    mu=3.10, alpha=0.500,
    beta_s=6.00,        # screening sharpness
    sigma0=0.620, beta_sig=4.00,   # good-match probability
    dmin=0.25,          # minimum feasible mean search duration (years)
    # offers and acceptance -------------------------------------------------
    q0=0.560, gammaq=0.200, beta_a=7.00,
    # aspiration ------------------------------------------------------------
    Aanch=0.820, zeta=0.550, lam=0.180,
    # employability capital -------------------------------------------------
    hnew=0.620, hmax=0.880, deltaH=0.060, chi=0.880, tau=0.020,
    # exam queue ------------------------------------------------------------
    Pi=0.980,           # perceived value of a public-sector ("iron rice bowl") post
    eps_pw=0.550,       # Prelec probability-weighting curvature
    beta_c=40.0,        # sharpness of the normalised search-versus-queue choice
    nu=0.900,           # maximal rate of entry into the queue
    nur=0.450,          # discouragement rate back into open search
    xi=0.0030,          # public-sector seats per entrant
    # separations -----------------------------------------------------------
    deltaM=0.100, deltaU=0.280,
)


def logistic(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60.0, 60.0)))


def smin(a, b):
    """Smooth (harmonic) minimum: <= both arguments, C-infinity for a,b > 0."""
    return a * b / (a + b + EPS)


def prelec(pi_, eps):
    """Prelec probability-weighting function w(p) = exp(-(-ln p)^eps).

    Small objective success probabilities are over-weighted (eps < 1), which is
    what keeps a queue for scarce public-sector posts attractive even when the
    realised success rate is of the order of one per cent.
    """
    pi_ = np.clip(pi_, 1e-12, 1.0 - 1e-12)
    return np.exp(-((-np.log(pi_)) ** eps))


# ---------------------------------------------------------------- drivers
def psi(t, p):
    """Digital-economy intensity: digital core industries' share of GRP."""
    k = (p["PsiMax"] / p["Psi0"]) - 1.0
    return p["PsiMax"] / (1.0 + k * np.exp(-p["rPsi"] * t))


def inflow(t, p):
    return p["Phi0"] * (1.0 + p["gPhi"]) ** t


def vacancies(t, p):
    return p["V0"] * np.exp(p["gV"] * t) * (1.0 + p["phi"] * (psi(t, p) - p["Psi0"]))


def seats(t, p):
    """Public-sector / institutional recruitment seats per year (10^4)."""
    return p["xi"] * inflow(t, p)


# ---------------------------------------------------------------- auxiliaries
def auxiliaries(t, y, p):
    S, Q, M, U, H, A = y
    S = max(S, 1e-6); Q = max(Q, 1e-6)
    M = max(M, 0.0); U = max(U, 0.0)
    E = M + U
    frz = p.get("_frz") or {}

    Psi = psi(t, p)
    V = vacancies(t, p)
    Xi = seats(t, p)

    mmU = frz.get("mmU", U / (E + EPS))               # deactivatable link R3
    theta = p["theta0"] + p["kappa"] * (Psi - p["Psi0"]) + p["kappa2"] * mmU
    x = H - theta                                     # skill-threshold gap

    tight = V / S                                     # market tightness
    q = frz.get("q", p["q0"] + p["gammaq"] * np.log1p(tight))   # link R4

    m = p["mu"] * S ** p["alpha"] * V ** (1.0 - p["alpha"])
    ps = logistic(p["beta_s"] * x)
    pa = logistic(p["beta_a"] * (q - A))
    sig = logistic(p["sigma0"] + p["beta_sig"] * x)

    hires = smin(m * ps * pa, S / p["dmin"])
    hM, hU = hires * sig, hires * (1.0 - sig)

    fQM = smin(Xi, Q)                                 # successful exam takers
    pi_e = fQM / Q                                    # realised success rate
    WS = ps * pa * q                                  # value of continued search
    WQ = p["Pi"] * prelec(frz.get("pi_e", pi_e), p["eps_pw"])   # link B3
    shQ = logistic(p["beta_c"] * (WQ - WS) / (WQ + WS + EPS))
    fSQ = p["nu"] * S * shQ
    fQS = p["nur"] * Q * (1.0 - shQ)

    return dict(Psi=Psi, V=V, Xi=Xi, theta=theta, x=x, tight=tight, q=q, m=m,
                ps=ps, pa=pa, sig=sig, hires=hires, hM=hM, hU=hU, WS=WS, WQ=WQ,
                pi_e=pi_e, shQ=shQ, fSQ=fSQ, fQS=fQS, fQM=fQM, E=E)


# ---------------------------------------------------------------- vector field
def rhs(t, y, p):
    S, Q, M, U, H, A = y
    S = max(S, 1e-6); Q = max(Q, 1e-6)
    a = auxiliaries(t, y, p)
    Phi = inflow(t, p)

    dS = (Phi + a["fQS"] + p["deltaM"] * M + p["deltaU"] * U
          - a["hires"] - a["fSQ"] - p["omega"] * S)
    dQ = a["fSQ"] - a["fQS"] - a["fQM"] - p["omega"] * Q
    dM = a["hM"] + a["fQM"] - (p["deltaM"] + p["omega"]) * M
    dU = a["hU"] - (p["deltaU"] + p["omega"]) * U

    frz = p.get("_frz") or {}
    S_H = frz.get("S_H", S)                           # link R1
    chi = frz.get("chi", p["chi"])                    # link R2
    dH = ((Phi * (p["hnew"] - H) - a["fQS"] * (1.0 - chi) * H) / S_H
          - p["deltaH"] * H + p["tau"] * (p["hmax"] - H))

    Astar = p["zeta"] * p["Aanch"] + (1.0 - p["zeta"]) * a["q"] * a["ps"]
    dA = p["lam"] * (Astar - A)

    return np.array([dS, dQ, dM, dU, dH, dA])


# ---------------------------------------------------------------- integration
def rk4(y0, p, t0=0.0, t1=25.0, dt=1.0 / 24.0):
    n = int(round((t1 - t0) / dt))
    ts = np.empty(n + 1)
    ys = np.empty((n + 1, 6))
    t, y = float(t0), np.asarray(y0, float).copy()
    ts[0], ys[0] = t, y
    for i in range(1, n + 1):
        k1 = rhs(t, y, p)
        k2 = rhs(t + dt / 2, y + dt / 2 * k1, p)
        k3 = rhs(t + dt / 2, y + dt / 2 * k2, p)
        k4 = rhs(t + dt, y + dt * k3, p)
        y = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        y[:4] = np.maximum(y[:4], 1e-6)
        y[4] = np.clip(y[4], 1e-3, 2.0)
        y[5] = np.clip(y[5], 1e-3, 2.0)
        t = t0 + i * dt
        ts[i], ys[i] = t, y
    return ts, ys


# ---------------------------------------------------------------- equilibria
GUESS_LOW = np.array([14.0, 5.5, 82.0, 20.0, 0.605, 0.700])    # fluid regime
GUESS_HIGH = np.array([60.0, 40.0, 40.0, 25.0, 0.560, 0.620])  # trapped regime


def equilibrium(t, p, guess=None):
    """Fixed point of the system with drivers frozen at time t."""
    g = GUESS_LOW if guess is None else np.asarray(guess, float)
    sol = root(lambda z: rhs(t, np.abs(z), p), g, method="hybr", tol=1e-11)
    y = np.abs(sol.x)
    return y, bool(sol.success) and float(np.max(np.abs(rhs(t, y, p)))) < 1e-6


def jacobian(t, y, p, h=1e-6):
    J = np.empty((6, 6))
    for j in range(6):
        e = np.zeros(6); e[j] = h * max(1.0, abs(y[j]))
        J[:, j] = (rhs(t, y + e, p) - rhs(t, y - e, p)) / (2 * e[j])
    return J


def classify(t, y, p):
    ev = np.linalg.eigvals(jacobian(t, y, p))
    return ev, ("stable" if np.max(ev.real) < 0 else
                "saddle" if np.min(ev.real) < 0 < np.max(ev.real) else "unstable")


# ---------------------------------------------------------------- indicators
def indicators(t, y, p):
    S, Q, M, U, H, A = y
    a = auxiliaries(t, y, p)
    pool = S + Q + M + U
    stable_in = a["hires"] * a["sig"] + a["fQM"]
    return dict(
        NER=(S + Q) / pool,                        # youth non-employment rate
        SEstock=Q / pool,                          # slow-employment stock share
        SEflow=a["fSQ"] / inflow(t, p),            # entrants choosing the queue
        MM=U / (M + U + EPS),                      # mismatch share of employment
        DUR=(S + Q) / (stable_in + EPS),           # mean transition duration (yr)
        RATIO=Q / (a["Xi"] + EPS),                 # queue-to-seat ratio
        MQ=M / (M + U + EPS),
        TIGHT=a["tight"], THETA=a["theta"], GAP=a["x"], PS=a["ps"], PA=a["pa"],
        SIG=a["sig"], PSI=a["Psi"], HIRE=a["hires"], Q_=Q, S_=S, H_=H, A_=A,
    )


IND_KEYS = tuple(indicators(0.0, GUESS_LOW, BASE).keys())


def series(ts, ys, p):
    out = {k: np.empty(len(ts)) for k in IND_KEYS}
    for i, (t, y) in enumerate(zip(ts, ys)):
        d = indicators(t, y, p)
        for k in IND_KEYS:
            out[k][i] = d[k]
    return out


def run(p=None, t1=25.0, y0=None, dt=1.0 / 24.0, t0=0.0):
    p = dict(BASE) if p is None else p
    if y0 is None:
        y0, _ = equilibrium(t0, p)
    ts, ys = rk4(y0, p, t0, t1, dt)
    return ts, ys, series(ts, ys, p)
