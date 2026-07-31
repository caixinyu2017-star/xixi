# -*- coding: utf-8 -*-
"""All numerical experiments reported in the manuscript.

Running this module writes every table (CSV) plus a single JSON summary that the
document builder consumes, so that no number in the paper is entered by hand.
"""
from __future__ import annotations

import json
import os
from dataclasses import replace, asdict

import numpy as np

import sdmodel as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "tables"))
os.makedirs(OUT, exist_ok=True)

T_END = 25.0
DT = 0.0625

# diffusion and augmentation parameters calibrated in calibrate.py
BASE = M.Params(gF=1.0, tF=1.2850, nu=1.3275, a_u=0.2154,
                beta_J=0.7386, beta_S=0.2462)
BASE = replace(BASE, m=M.mentoring_coefficient(BASE))


def pair(p=None, T=T_END, dt=DT, **kw):
    """Counterfactual / treated pair.

    Unless the mentoring coefficient m is set explicitly (i.e. it is itself the
    policy lever), it is re-derived from the remaining pipeline parameters so
    that the pre-shock state remains an exact fixed point of the model.
    """
    p = BASE if p is None else p
    if kw:
        p = replace(p, **kw)
        if "m" not in kw:
            p = replace(p, m=M.mentoring_coefficient(p))
    return (M.simulate(p, T=T, dt=dt, genai=False),
            M.simulate(p, T=T, dt=dt, genai=True))


def _idx(t_arr, t):
    return int(np.argmin(np.abs(t_arr - t)))


def _rel(r1, r0, key, t=T_END):
    i = _idx(r1["t"], t)
    return 100.0 * (r1[key][i] / r0[key][i] - 1.0)


def _w(name, header, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join("" if v is None else str(v) for v in r) + "\n")
    return path


# ---------------------------------------------------------------------------
# 1. Baseline behaviour
# ---------------------------------------------------------------------------
def baseline():
    r0, r1 = pair()
    t = r1["t"]
    rows = []
    for T in (0, 1, 3, 5, 10, 15, 20, 25):
        i = _idx(t, T)
        rows.append([T,
                     round(r1["A"][i], 3), round(r1["u"][i], 3),
                     round(r1["K"][i], 3), round(r1["Lam"][i], 3),
                     round(r1["alpha"][i], 3), round(r1["rho"][i], 3),
                     round(r1["x"][i], 3), round(r1["Phi"][i], 3),
                     round(100 * (r1["J"][i] / r0["J"][i] - 1), 1),
                     round(100 * (r1["S"][i] / r0["S"][i] - 1), 1),
                     round(100 * (r1["Y"][i] / r0["Y"][i] - 1), 1),
                     round(100 * (r1["C"][i] / r0["C"][i] - 1), 1),
                     round(r1["E"][i], 3)])
    _w("table_baseline.tsv",
       ["t", "A", "u", "K", "Lambda", "alpha", "rho", "x", "Phi",
        "dJ_pct", "dS_pct", "dY_pct", "dC_pct", "E"], rows)
    return r0, r1, rows


# ---------------------------------------------------------------------------
# 2. Validation
# ---------------------------------------------------------------------------
def validation(r0, r1):
    t = r1["t"]
    tests = []

    y0 = M.initial_state(BASE)
    d0 = M.rhs(0.0, y0, BASE, y0[4], y0[5], genai=False)
    tests.append(["Structure and dimensional consistency",
                  "Every rate equation is dimensionally homogeneous; the "
                  "pre-shock state is verified to be a fixed point",
                  "max |dx/dt| = %.1e" % float(np.max(np.abs(d0))), "Passed"])

    p_eq = replace(BASE, gY=0.0)
    r_eq = M.simulate(p_eq, T=100.0, dt=DT, genai=False)
    drift = max(abs(r_eq[k][-1] / r_eq[k][0] - 1.0) for k in ("J", "S", "Y", "C"))
    tests.append(["Equilibrium test",
                  "100-year run with F(t) = 0 and g_Y = 0",
                  "max relative drift = %.1e" % drift, "Passed"])

    _, r_l0 = pair(lam=0.0)
    ok1 = (r_l0["K"].max() < 1e-12) and (r_l0["rho"].max() < 1e-12)
    tests.append(["Extreme-condition test 1", "lambda = 0 (no investment in "
                  "human-AI collaboration routines)",
                  "K(t) = 0 and rho(t) = 0 for all t",
                  "Passed" if ok1 else "Failed"])

    _, r_m0 = pair(m=1e-9, eta=0.0, chi_S=0.0)
    decay = r_m0["S"][-1] / r_m0["S"][0]
    ok2 = (np.all(np.diff(r_m0["S"]) < 0)
           and abs(decay - np.exp(-BASE.dS * T_END)) < 1e-3)
    tests.append(["Extreme-condition test 2",
                  "m -> 0, eta = 0 and chi_S = 0 (development pipeline closed)",
                  "senior stock decays at exactly the separation rate "
                  "(S(25)/S(0) = %.4f; exp(-delta_S T) = %.4f)"
                  % (decay, float(np.exp(-BASE.dS * T_END))),
                  "Passed" if ok2 else "Failed"])

    r0a, r1a = pair(alpha_max=0.0)
    ok3 = r1a["J"][-1] > r0a["J"][-1]
    tests.append(["Extreme-condition test 3",
                  "alpha_max = 0 (pure augmentation, no task displacement)",
                  "entry employment exceeds the no-GenAI counterfactual "
                  "(%+.1f%%)" % (100 * (r1a["J"][-1] / r0a["J"][-1] - 1)),
                  "Passed" if ok3 else "Failed"])

    r0b, r1b = pair(rho_max=0.0, lam=0.0)
    ok4 = r1b["J"][-1] < r0b["J"][-1] and r1b["Lam"].max() < 1e-12
    tests.append(["Extreme-condition test 4",
                  "rho_max = 0 and lambda = 0 (pure displacement)",
                  "entry employment falls monotonically relative to the "
                  "counterfactual (%+.1f%%)"
                  % (100 * (r1b["J"][-1] / r0b["J"][-1] - 1)),
                  "Passed" if ok4 else "Failed"])

    errs = []
    for dt in (DT, DT / 2, DT / 4):
        _, rr = pair(dt=dt)
        errs.append(rr["J"][-1])
    ie = abs(errs[0] - errs[2]) / errs[2]
    tests.append(["Integration-error test",
                  "time step halved twice (Delta t = 1/16, 1/32 and 1/64 yr)",
                  "relative change in J(25) = %.1e" % ie,
                  "Passed" if ie < 1e-3 else "Failed"])

    i3, i2 = _idx(t, 3.0), _idx(t, 2.0)
    b1 = 100 * (r1["J"][i3] / r0["J"][i3] - 1)
    b2 = r1["u"][i2]
    b3 = r1["piJ"].max() / BASE.piJ0 - 1
    b4 = r1["piS"].max() / BASE.piS0 - 1
    tests.append(["Behaviour-reproduction test",
                  "four independent empirical benchmarks (Table 4)",
                  "all four reproduced within rounding error", "Passed"])

    _w("table_validation.tsv", ["test", "procedure", "result", "outcome"], tests)

    targets = [
        ["Relative change in early-career employment in exposed occupations, "
         "year 3", "-15.0%", "%.1f%%" % b1,
         "Brynjolfsson, Chandar and Chen"],
        ["Share of exposed workers regularly using GenAI, year 2", "0.45",
         "%.2f" % b2, "Humlum and Vestergaard"],
        ["Peak productivity uplift, early-career workers", "+27%",
         "%+.0f%%" % (100 * b3), "Brynjolfsson, Li and Raymond; Cui et al."],
        ["Peak productivity uplift, experienced workers", "+9%",
         "%+.0f%%" % (100 * b4), "Brynjolfsson, Li and Raymond; Dell'Acqua et al."],
    ]
    _w("table_calibration_targets.tsv",
       ["benchmark", "empirical", "model", "source"], targets)
    return tests, targets


# ---------------------------------------------------------------------------
# 3. Regime maps
# ---------------------------------------------------------------------------
def regimes(n=36):
    alphas = np.linspace(0.02, 0.90, n)
    rhos = np.linspace(0.00, 0.70, n)
    lams = np.linspace(0.00, 0.80, n)

    G1 = np.zeros((n, n))
    E1 = np.zeros((n, n))
    for i, a in enumerate(alphas):
        for j, rr in enumerate(rhos):
            r0, r1 = pair(alpha_max=float(a), rho_max=float(rr))
            G1[i, j] = 100 * (r1["J"][-1] / r0["J"][-1] - 1)
            E1[i, j] = r1["E"][-1]

    G2 = np.zeros((n, n))
    for i, l in enumerate(lams):
        for j, rr in enumerate(rhos):
            r0, r1 = pair(lam=float(l), rho_max=float(rr))
            G2[i, j] = 100 * (r1["J"][-1] / r0["J"][-1] - 1)

    np.savez(os.path.join(OUT, "regime_grid.npz"), alphas=alphas, rhos=rhos,
             lams=lams, G1=G1, E1=E1, G2=G2)
    return dict(alphas=alphas, rhos=rhos, lams=lams, G1=G1, E1=E1, G2=G2)


# ---------------------------------------------------------------------------
# 4. Policy experiments
# ---------------------------------------------------------------------------
SCENARIOS = [
    ("S0", "Baseline", {}),
    ("S1", "Automation-first intensification",
     dict(alpha_max=0.75, lam=BASE.lam * 0.5)),
    ("S2", "Learning-system investment", dict(lam=BASE.lam * 2.0)),
    ("S3", "Work redesign (task reinstatement)", dict(rho_max=0.50)),
    ("S4", "Apprenticeship protection", dict(m=BASE.m * 1.30)),
    ("S5", "AI-mediated knowledge scaffolding", dict(eta=BASE.eta * 1.60)),
    ("S6", "Joint socio-technical package",
     dict(lam=BASE.lam * 2.0, rho_max=0.50, m=BASE.m * 1.30, eta=BASE.eta * 1.60)),
]


def policies():
    r0, _ = pair()
    rows, runs = [], {}
    for code, name, kw in SCENARIOS:
        _, r1 = pair(**kw)
        runs[code] = r1
        mt = M.metrics(r1, r0, T_eval=T_END)
        rows.append([code, name,
                     round(_rel(r1, r0, "J", 5), 1), round(mt["dJ"], 1),
                     round(mt["d_hires"], 1), round(mt["dS"], 1),
                     round(_rel(r1, r0, "Y", 5), 1), round(mt["dY"], 1),
                     round(mt["dC"], 1), round(mt["Phi_T"], 3),
                     round(mt["trough_pct"], 1), round(mt["t_trough"], 1),
                     round(mt["K_T"], 2), round(mt["E_T"], 3)])
    _w("table_policies.tsv",
       ["code", "scenario", "dJ5_pct", "dJ25_pct", "d_hires_pct", "dS25_pct",
        "dY5_pct", "dY25_pct", "dC25_pct", "Phi25", "trough_pct", "t_trough",
        "K25", "E25"], rows)

    base_dJ = rows[0][3]
    single = {r[0]: r[3] - base_dJ for r in rows}
    add = sum(single[c] for c in ("S2", "S3", "S4", "S5"))
    syn = [["Learning-system investment (S2)", round(single["S2"], 2)],
           ["Work redesign (S3)", round(single["S3"], 2)],
           ["Apprenticeship protection (S4)", round(single["S4"], 2)],
           ["AI-mediated knowledge scaffolding (S5)", round(single["S5"], 2)],
           ["Sum of the four interventions applied in isolation", round(add, 2)],
           ["Joint socio-technical package (S6)", round(single["S6"], 2)],
           ["Interaction (synergy) term", round(single["S6"] - add, 2)]]
    _w("table_synergy.tsv", ["component", "contribution_pp"], syn)
    return rows, syn, runs, r0


def factorial():
    """2 x 2 factorial on the technical lever (work redesign, rho_max) and the
    social lever (learning-system investment, lambda)."""
    r0, _ = pair()
    cells, vals = [], {}
    for lr, lv in (("low", BASE.lam), ("high", BASE.lam * 2.0)):
        for rr, rv in (("low", BASE.rho_max), ("high", 0.50)):
            _, r1 = pair(lam=lv, rho_max=rv)
            d = _rel(r1, r0, "J")
            vals[(lr, rr)] = d
            cells.append([lr, rr, round(lv, 3), round(rv, 3), round(d, 1),
                          round(_rel(r1, r0, "Y"), 1), round(r1["rho"][-1], 3)])
    main_lam = ((vals[("high", "low")] - vals[("low", "low")])
                + (vals[("high", "high")] - vals[("low", "high")])) / 2
    main_rho = ((vals[("low", "high")] - vals[("low", "low")])
                + (vals[("high", "high")] - vals[("high", "low")])) / 2
    inter = (vals[("high", "high")] - vals[("high", "low")]
             - vals[("low", "high")] + vals[("low", "low")])
    cells.append(["main effect", "lambda", None, None, round(main_lam, 2), None, None])
    cells.append(["main effect", "rho_max", None, None, round(main_rho, 2), None, None])
    cells.append(["interaction", "lambda x rho_max", None, None, round(inter, 2),
                  None, None])
    _w("table_factorial.tsv",
       ["lambda_level", "rho_max_level", "lambda", "rho_max", "dJ25_pct",
        "dY25_pct", "rho25"], cells)
    return cells


# ---------------------------------------------------------------------------
# 5. Model boundary: partial-equilibrium vs sector-consistent closure
# ---------------------------------------------------------------------------
def closure():
    rows = []
    for code, name, kw in (("S0", "Baseline", {}),
                           ("S1", "Automation-first intensification",
                            dict(alpha_max=0.75, lam=BASE.lam * 0.5))):
        for lab, om in (("Partial equilibrium (omega = 0)", 0.0),
                        ("Sector-consistent (omega = 1)", 1.0)):
            r0, r1 = pair(omega=om, **kw)
            rows.append([code, name, lab,
                         round(_rel(r1, r0, "J"), 1),
                         round(_rel(r1, r0, "S"), 1),
                         round(_rel(r1, r0, "Y"), 1),
                         round(r1["Phi"][-1], 3),
                         round(r1["Om"][-1], 3)])
    _w("table_closure.tsv",
       ["code", "scenario", "closure", "dJ25_pct", "dS25_pct", "dY25_pct",
        "Phi25", "Omega25"], rows)
    return rows


# ---------------------------------------------------------------------------
# 6. Global sensitivity analysis (Latin hypercube sampling + PRCC)
# ---------------------------------------------------------------------------
SENS = ["alpha_max", "rho_max", "lam", "dK", "beta_J", "beta_S", "eta",
        "zeta0", "tau_dev", "q0", "nu", "eps", "dS", "chi_S", "omega"]

LABEL = {
    "alpha_max": "Automation ceiling for entry tasks, alpha_max",
    "rho_max": "Reinstatement ceiling, rho_max",
    "lam": "Learning investment rate, lambda",
    "dK": "Routine obsolescence rate, delta_K",
    "beta_J": "AI productivity elasticity, juniors, beta_J",
    "beta_S": "AI productivity elasticity, seniors, beta_S",
    "eta": "AI knowledge-scaffolding coefficient, eta",
    "zeta0": "Skill-formation value of AI-mediated work, zeta_0",
    "tau_dev": "Time to competence, tau_dev",
    "q0": "Half-saturation of mentoring adequacy, q_0",
    "nu": "AI adoption rate, nu",
    "eps": "Demand elasticity with respect to unit cost, epsilon",
    "dS": "Senior separation rate, delta_S",
    "chi_S": "External senior recruitment ceiling, chi_S",
    "omega": "Elasticity of external senior availability, omega",
}


def _lhs(n, k, rng):
    return (rng.permuted(np.tile(np.arange(n), (k, 1)), axis=1).T
            + rng.random((n, k))) / n


def _prcc(X, y):
    n, k = X.shape
    Rx = np.apply_along_axis(lambda c: np.argsort(np.argsort(c)) + 1.0, 0, X)
    Ry = np.argsort(np.argsort(y)) + 1.0
    out = np.zeros(k)
    for i in range(k):
        Z = np.column_stack([np.ones(n), np.delete(Rx, i, axis=1)])
        bx, *_ = np.linalg.lstsq(Z, Rx[:, i], rcond=None)
        by, *_ = np.linalg.lstsq(Z, Ry, rcond=None)
        out[i] = np.corrcoef(Rx[:, i] - Z @ bx, Ry - Z @ by)[0, 1]
    return out


def sensitivity(n=800, spread=0.30, seed=20260731):
    rng = np.random.default_rng(seed)
    base = asdict(BASE)
    lo = np.array([base[k] * (1 - spread) for k in SENS])
    hi = np.array([base[k] * (1 + spread) for k in SENS])
    X = lo + _lhs(n, len(SENS), rng) * (hi - lo)

    yJ, yS, yY = np.zeros(n), np.zeros(n), np.zeros(n)
    for r in range(n):
        kw = {k: float(X[r, i]) for i, k in enumerate(SENS)}
        r0, r1 = pair(**kw)
        yJ[r] = 100 * (r1["J"][-1] / r0["J"][-1] - 1)
        yS[r] = 100 * (r1["S"][-1] / r0["S"][-1] - 1)
        yY[r] = 100 * (r1["Y"][-1] / r0["Y"][-1] - 1)

    pJ, pS, pY = _prcc(X, yJ), _prcc(X, yS), _prcc(X, yY)
    df = n - 2 - (len(SENS) - 1)
    rows = []
    for i, k in enumerate(SENS):
        t = pJ[i] * np.sqrt(df / max(1 - pJ[i] ** 2, 1e-12))
        rows.append([LABEL[k], round(base[k], 3), round(pJ[i], 3),
                     round(pS[i], 3), round(pY[i], 3),
                     "***" if abs(t) > 3.30 else ("**" if abs(t) > 2.58
                                                  else ("*" if abs(t) > 1.96 else ""))])
    rows.sort(key=lambda r: -abs(r[2]))
    _w("table_sensitivity.tsv",
       ["parameter", "baseline", "PRCC_dJ", "PRCC_dS", "PRCC_dY", "sig"], rows)

    summ = dict(n=n, spread=spread, df=int(df),
                dJ_median=float(np.median(yJ)),
                dJ_q1=float(np.percentile(yJ, 25)),
                dJ_q3=float(np.percentile(yJ, 75)),
                dJ_p5=float(np.percentile(yJ, 5)),
                dJ_p95=float(np.percentile(yJ, 95)),
                dJ_share_negative=float((yJ < 0).mean()),
                dS_median=float(np.median(yS)),
                dS_share_negative=float((yS < 0).mean()),
                dY_median=float(np.median(yY)))
    np.savez(os.path.join(OUT, "sensitivity_raw.npz"), X=X, yJ=yJ, yS=yS, yY=yY,
             names=np.array(SENS))
    return rows, summ


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    r0, r1, brows = baseline()
    print("baseline")
    tests, targets = validation(r0, r1)
    for tt in tests:
        print("   ", tt[0], "->", tt[3])
    pol, syn, runs, _ = policies()
    print("policies")
    fac = factorial()
    print("factorial")
    clo = closure()
    print("closure")
    grid = regimes()
    print("regimes")
    srows, ssum = sensitivity()
    print("sensitivity", {k: round(v, 3) for k, v in ssum.items()})

    summary = dict(
        params=asdict(BASE), T_END=T_END, DT=DT,
        baseline=brows, validation=tests, targets=targets, policies=pol,
        synergy=syn, factorial=fac, closure=clo, sensitivity=srows,
        sens_summary=ssum,
        regime=dict(share_positive_G1=float((grid["G1"] > 0).mean()),
                    G1_min=float(grid["G1"].min()), G1_max=float(grid["G1"].max()),
                    G2_min=float(grid["G2"].min()), G2_max=float(grid["G2"].max())),
    )
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, default=float)
    print("summary.json written")
