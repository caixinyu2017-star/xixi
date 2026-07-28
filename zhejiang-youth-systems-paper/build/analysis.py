# -*- coding: utf-8 -*-
"""Full analysis pipeline for the YSTS model.

Stages
  1  baseline trajectory and behaviour-reproduction validation
  2  equilibrium continuation, fold bifurcation and hysteresis
  3  loop-knockout (structural dominance) analysis
  4  Latin-hypercube Monte Carlo with uncertainty bands
  5  Sobol variance decomposition (Saltelli estimator, bootstrap CIs)
  6  logistic meta-model and cross-validated classification tree for trap risk
  7  equal-effort policy experiments, sequencing and effort-response frontier
  8  prefecture archetype analysis
Everything is written to stats.json plus CSV tables in ../data.
"""
from __future__ import annotations

import itertools
import json
import os
from multiprocessing import Pool

import numpy as np
import pandas as pd
from scipy import stats as st
from scipy.optimize import root
from scipy.stats import qmc
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import roc_auc_score
import statsmodels.api as sm

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
os.makedirs(DATA, exist_ok=True)
RNG = np.random.default_rng(20260728)

CAL = json.load(open(os.path.join(HERE, "calibrated.json")))
P = dict(CAL["params"])
Y0 = np.array(CAL["y0_2015"])
T_END = 25.0          # 2015 -> 2040
T_POL = 10.0          # policy start (2025)
DT = 1.0 / 12.0
OUT = {}
TRAP_THRESHOLD = 0.36   # twice the 2025 benchmark youth non-employment rate


def yr(t):
    return int(round(t * (1.0 / DT)))


# ============================================================ 1. baseline
def baseline():
    ts, ys = M.rk4(Y0, P, 0.0, T_END, DT)
    s = M.series(ts, ys, P)
    rows = []
    for t in range(0, 26, 5):
        i = yr(t)
        rows.append(dict(year=2015 + t, NER=s["NER"][i], SEflow=s["SEflow"][i],
                         MM=s["MM"][i], DUR=s["DUR"][i], RATIO=s["RATIO"][i],
                         THETA=s["THETA"][i], H=s["H_"][i], A=s["A_"][i],
                         GAP=s["GAP"][i], TIGHT=s["TIGHT"][i], PSI=s["PSI"][i]))
    pd.DataFrame(rows).to_csv(os.path.join(DATA, "table_baseline.csv"), index=False)

    # behaviour-reproduction test against published series
    obs = [
        ("Digital core industries, share of GRP, 2025", 0.130, s["PSI"][yr(10)]),
        ("Youth non-employment rate, 2015", 0.115, s["NER"][0]),
        ("Youth non-employment rate, 2025", 0.180, s["NER"][yr(10)]),
        ("Slow-employment share of entrants, 2025", 0.191, s["SEflow"][yr(10)]),
        ("Vertical mismatch share, 2025", 0.240, s["MM"][yr(10)]),
        ("Queue-to-seat ratio, 2026 cycle", 96.0, s["RATIO"][yr(10)]),
        ("Vacancy-to-seeker ratio, 2015", 1.50, s["TIGHT"][0]),
    ]
    val = [dict(indicator=k, observed=o, simulated=float(m),
                rel_error=float((m - o) / o)) for k, o, m in obs]
    # Theil inequality statistics on the seven paired points
    o = np.array([x[1] for x in obs]); mm = np.array([float(x[2]) for x in obs])
    rmse = float(np.sqrt(np.mean(((mm - o) / o) ** 2)))
    OUT["validation"] = dict(points=val, rmspe=rmse,
                             bias=float(np.mean((mm - o) / o)))
    OUT["baseline"] = rows
    return ts, ys, s


# ============================================ 2. continuation / bifurcation
def eq_at(p, guess, t=T_END):
    sol = root(lambda z: M.rhs(t, np.abs(z), p), guess, method="hybr", tol=1e-12)
    y = np.abs(sol.x)
    ok = float(np.max(np.abs(M.rhs(t, y, p)))) < 1e-7
    return y, ok


def continuation(pname, lo, hi, n=241, t=T_END):
    """Forward and backward continuation in one control parameter."""
    grid = np.linspace(lo, hi, n)
    fwd, bwd = [], []
    g = Y0.copy()
    g, _ = eq_at(dict(P, **{pname: lo}), M.GUESS_LOW, t)
    for v in grid:
        y, ok = eq_at(dict(P, **{pname: v}), g, t)
        if ok:
            g = y
        ev = np.linalg.eigvals(M.jacobian(t, y, dict(P, **{pname: v})))
        fwd.append((v, M.indicators(t, y, dict(P, **{pname: v}))["NER"],
                    float(np.max(ev.real)), ok))
    g, _ = eq_at(dict(P, **{pname: hi}), M.GUESS_HIGH, t)
    for v in grid[::-1]:
        y, ok = eq_at(dict(P, **{pname: v}), g, t)
        if ok:
            g = y
        ev = np.linalg.eigvals(M.jacobian(t, y, dict(P, **{pname: v})))
        bwd.append((v, M.indicators(t, y, dict(P, **{pname: v}))["NER"],
                    float(np.max(ev.real)), ok))
    return np.array(fwd), np.array(bwd[::-1])


def bifurcation():
    """Continuation in two control parameters, and a global search for folds."""
    res = {}
    for pname, lo, hi in [("kappa", 0.5, 5.0), ("Pi", 0.4, 2.6)]:
        fwd, bwd = continuation(pname, lo, hi)
        gap = np.abs(fwd[:, 1] - bwd[:, 1])
        hyst = gap > 0.02
        rng_ = (float(fwd[hyst, 0].min()), float(fwd[hyst, 0].max())) if hyst.any() else None
        res[pname] = dict(grid=fwd[:, 0].tolist(), ner_fwd=fwd[:, 1].tolist(),
                          ner_bwd=bwd[:, 1].tolist(),
                          maxreal_fwd=fwd[:, 2].tolist(),
                          hysteresis_range=rng_, max_gap=float(gap.max()),
                          base_value=float(P[pname]))
        print("  continuation %-6s max forward-backward NER gap %.4f (fold: %s)"
              % (pname, gap.max(), bool(hyst.any())))
    OUT["bifurcation"] = res

    # multi-start uniqueness check over a coarse grid of the two strongest loops
    starts = [M.GUESS_LOW, M.GUESS_HIGH,
              np.array([5., 1., 200., 30., 0.62, 0.75]),
              np.array([150., 400., 200., 120., 0.55, 0.50]),
              np.array([40., 80., 150., 60., 0.58, 0.60]),
              np.array([300., 900., 150., 150., 0.52, 0.45])]
    multi = []
    for k2 in [0.0, 0.15, 0.30, 0.60, 1.20, 2.50]:
        for bs in [3.0, 6.0, 12.0, 22.0]:
            p = dict(P, kappa2=k2, beta_s=bs)
            found = []
            for g in starts:
                y, ok = eq_at(p, g, T_END)
                if ok and (y[:4] > 1e-4).all():
                    n = M.indicators(T_END, y, p)["NER"]
                    if not any(abs(n - f) < 1e-3 for f in found):
                        found.append(float(n))
            multi.append(dict(kappa2=k2, beta_s=bs, n_equilibria=len(found),
                              NER=sorted(found)))
    OUT["uniqueness_scan"] = dict(rows=multi,
                                  max_equilibria=max(r["n_equilibria"] for r in multi))
    print("  uniqueness scan: maximum number of fixed points found = %d"
          % OUT["uniqueness_scan"]["max_equilibria"])

    eqs = []
    for tt in range(0, 26, 1):
        y, ok = eq_at(P, M.GUESS_LOW if tt == 0 else np.array(list(eqs[-1]["state"].values())), float(tt))
        if not ok:
            continue
        ev, kind = M.classify(float(tt), y, P)
        d = M.indicators(float(tt), y, P)
        eqs.append(dict(year=2015 + tt,
                        state=dict(zip(M.STATES, y.round(4).tolist())),
                        NER=d["NER"], SEflow=d["SEflow"], MM=d["MM"], DUR=d["DUR"],
                        THETA=d["THETA"], GAP=d["GAP"],
                        max_real_eig=float(np.max(ev.real)),
                        slowest_tau=float(-1.0 / np.max(ev.real)),
                        eig_real=np.sort(ev.real).round(5).tolist(), kind=kind))
    OUT["moving_attractor"] = eqs
    pd.DataFrame([{k: v for k, v in e.items() if k not in ("state", "eig_real")}
                  for e in eqs]).to_csv(os.path.join(DATA, "table_attractor.csv"),
                                        index=False)
    print("  attractor NER* drifts %.3f (2015) -> %.3f (2040); slowest tau = %.2f yr"
          % (eqs[0]["NER"], eqs[-1]["NER"], eqs[-1]["slowest_tau"]))
    return eqs


def drift_lag(s):
    """Gap between the realised state and its instantaneous (moving) attractor."""
    eqs = OUT["moving_attractor"]
    tt = np.array([e["year"] - 2015 for e in eqs], float)
    star = np.array([e["NER"] for e in eqs])
    grid = np.arange(0.0, T_END + 1e-9, DT)
    star_i = np.interp(grid, tt, star)
    act = np.array([s["NER"][yr(t)] for t in grid])
    gap = star_i - act
    # horizontal lag: for each t, how far back in time the attractor equalled today's state
    lags = []
    for i, t in enumerate(grid):
        if act[i] <= star_i[0] or act[i] >= star_i[-1]:
            continue
        j = np.searchsorted(star_i, act[i])
        lags.append(t - grid[min(j, len(grid) - 1)])
    OUT["drift"] = dict(t=grid.tolist(), attractor=star_i.tolist(),
                        realised=act.tolist(), max_gap=float(gap.max()),
                        gap_2040=float(gap[-1]),
                        mean_lag_years=float(np.mean(lags)) if lags else None,
                        lag_2040=float(lags[-1]) if lags else None)
    print("  attractor-state gap in 2040 = %.3f; mean horizontal lag = %.2f yr"
          % (gap[-1], OUT["drift"]["mean_lag_years"] or float("nan")))


def shock_persistence(dur=3.0, size=-0.25, t0=11.0):
    """Temporary demand shock; measure overshoot and recovery half-life."""
    _, ys = M.rk4(Y0, P, 0.0, t0, DT)
    p_sh = dict(P, phi=P["phi"] * (1.0 + size), gV=P["gV"] + np.log(1.0 + size) / 5.0)
    ts1, ys1 = M.rk4(ys[-1], p_sh, t0, t0 + dur, DT)
    ts2, ys2 = M.rk4(ys1[-1], P, t0 + dur, T_END + 25.0, DT)
    s_sh = np.concatenate([M.series(ts1, ys1, p_sh)["NER"],
                           M.series(ts2, ys2, P)["NER"]])
    t_sh = np.concatenate([ts1, ts2])
    _, ys_b = M.rk4(ys[-1], P, t0, T_END + 25.0, DT)
    ts_b = np.arange(len(ys_b)) * DT + t0
    s_b = M.series(ts_b, ys_b, P)["NER"]
    dev = s_sh - np.interp(t_sh, ts_b, s_b)
    peak = float(dev.max()); ipk = int(dev.argmax())
    half = None
    for i in range(ipk, len(dev)):
        if dev[i] <= peak / 2.0:
            half = float(t_sh[i] - (t0 + dur))
            break
    OUT["shock"] = dict(shock_years=dur, shock_size=size, start=2015 + t0,
                        peak_excess_NER=peak, peak_year=float(2015 + t_sh[ipk]),
                        half_life_years=half,
                        excess_at_10yr=float(np.interp(t0 + dur + 10, t_sh, dev)),
                        t=t_sh.tolist(), dev=dev.tolist())
    print("  shock: peak excess NER %.4f in %.1f, recovery half-life %.2f yr, "
          "excess after 10 yr %.4f"
          % (peak, 2015 + t_sh[ipk], half if half else float("nan"),
             OUT["shock"]["excess_at_10yr"]))


# ============================================ 3. loop knockout
LOOPS = [
    ("R1 Skill decay while searching", "S_H"),
    ("R2 Queue-skill erosion", "chi"),
    ("R3 Threshold escalation", "mmU"),
    ("R4 Thin-market offer quality", "q"),
    ("B2 Aspiration adjustment", "A"),
    ("B3 Exam-queue congestion", "pi_e"),
]


def knockout():
    """Loop deactivation: each link is held at its 2015 value so that the loop
    running through it cannot operate.  The level effect of the link is
    preserved and only the feedback is removed."""
    a0 = M.auxiliaries(0.0, Y0, P)
    init = dict(S_H=float(Y0[0]), chi=1.0, mmU=float(Y0[3] / (Y0[2] + Y0[3])),
                q=float(a0["q"]), pi_e=float(a0["pi_e"]))
    _, ys = M.rk4(Y0, P, 0.0, T_END, DT)
    base = M.indicators(T_END, ys[-1], P)
    rows = []
    for name, link in LOOPS:
        p = dict(P)
        if link == "A":
            p["lam"] = 1e-9                     # aspiration frozen at its 2015 level
        else:
            p["_frz"] = {link: init[link]}
        _, y2 = M.rk4(Y0, p, 0.0, T_END, DT)
        d = M.indicators(T_END, y2[-1], p)
        rows.append(dict(loop=name, link=link, NER=d["NER"],
                         dNER=d["NER"] - base["NER"], DUR=d["DUR"],
                         dDUR=d["DUR"] - base["DUR"], SEflow=d["SEflow"],
                         dSEflow=d["SEflow"] - base["SEflow"],
                         polarity="reinforcing" if d["NER"] < base["NER"] else "balancing"))
        print("  deactivate %-32s NER %.4f  dNER %+0.4f  dDUR %+0.3f"
              % (name, d["NER"], rows[-1]["dNER"], rows[-1]["dDUR"]))
    tot = sum(abs(r["dNER"]) for r in rows)
    for r in rows:
        r["share"] = abs(r["dNER"]) / tot
    rows.sort(key=lambda r: -abs(r["dNER"]))
    OUT["knockout"] = dict(baseline_NER=base["NER"], baseline_DUR=base["DUR"],
                           init_links=init, rows=rows)
    pd.DataFrame(rows).to_csv(os.path.join(DATA, "table_knockout.csv"), index=False)


# ============================================ 4-6. uncertainty and sensitivity
UNC = [                     # name, low, high  (uniform)
    ("kappa",   1.30, 3.30),
    ("kappa2",  0.05, 0.30),
    ("deltaH",  0.030, 0.100),
    ("chi",     0.780, 0.960),
    ("zeta",    0.380, 0.740),
    ("lam",     0.090, 0.320),
    ("Pi",      0.90, 1.90),
    ("eps_pw",  0.320, 0.640),
    ("mu",      7.60, 11.8),
    ("phi",     0.90, 2.40),
    ("gPhi",    0.030, 0.070),
    ("tau",     0.008, 0.040),
]
UNC_LABEL = {
    "kappa": "Threshold sensitivity to digitalisation",
    "kappa2": "Endogenous threshold escalation",
    "deltaH": "Skill decay while searching",
    "chi": "Skill retention while queueing",
    "zeta": "Aspiration anchoring weight",
    "lam": "Aspiration adjustment speed",
    "Pi": "Perceived value of a public post",
    "eps_pw": "Probability-weighting curvature",
    "mu": "Matching efficiency",
    "phi": "Vacancy elasticity to digitalisation",
    "gPhi": "Graduate cohort growth",
    "tau": "Training intensity",
}
K = len(UNC)


def _sim(vec):
    p = dict(P)
    for (name, _, _), v in zip(UNC, vec):
        p[name] = float(v)
    try:
        _, ys = M.rk4(Y0, p, 0.0, T_END, DT)
        d = M.indicators(T_END, ys[-1], p)
        return [d["NER"], d["DUR"], d["SEflow"], d["MM"]]
    except Exception:
        return [np.nan] * 4


def montecarlo(n=4096):
    lo = np.array([a for _, a, _ in UNC]); hi = np.array([b for _, _, b in UNC])
    X = qmc.scale(qmc.LatinHypercube(d=K, seed=42).random(n), lo, hi)
    with Pool() as pool:
        Y = np.array(pool.map(_sim, X, chunksize=32))
    ok = np.isfinite(Y).all(1)
    X, Y = X[ok], Y[ok]
    q = lambda a: np.percentile(a, [2.5, 25, 50, 75, 97.5]).tolist()
    OUT["montecarlo"] = dict(
        n=int(ok.sum()),
        NER=dict(mean=float(Y[:, 0].mean()), sd=float(Y[:, 0].std(ddof=1)), q=q(Y[:, 0])),
        DUR=dict(mean=float(Y[:, 1].mean()), sd=float(Y[:, 1].std(ddof=1)), q=q(Y[:, 1])),
        SEflow=dict(mean=float(Y[:, 2].mean()), sd=float(Y[:, 2].std(ddof=1)), q=q(Y[:, 2])),
        MM=dict(mean=float(Y[:, 3].mean()), sd=float(Y[:, 3].std(ddof=1)), q=q(Y[:, 3])),
    )
    return X, Y


def sobol(n=1024, boot=800):
    lo = np.array([a for _, a, _ in UNC]); hi = np.array([b for _, _, b in UNC])
    S = qmc.Sobol(d=2 * K, scramble=True, seed=7).random(n)
    A = qmc.scale(S[:, :K], lo, hi)
    B = qmc.scale(S[:, K:], lo, hi)
    designs = [A, B] + [np.column_stack([B[:, :i], A[:, i], B[:, i + 1:]])
                        for i in range(K)]
    X = np.vstack(designs)
    with Pool() as pool:
        Yall = np.array(pool.map(_sim, X, chunksize=64))
    Y = Yall.reshape(K + 2, n, 4)
    res = {}
    for oi, oname in enumerate(["NER", "DUR", "SEflow", "MM"]):
        yA, yB = Y[0, :, oi], Y[1, :, oi]
        var = np.var(np.concatenate([yA, yB]), ddof=1)
        rows = []
        for i in range(K):
            yBAi = Y[2 + i, :, oi]
            si = np.mean(yA * (yBAi - yB)) / var
            sti = 0.5 * np.mean((yB - yBAi) ** 2) / var
            bs_s, bs_t = [], []
            for _ in range(boot):
                idx = RNG.integers(0, n, n)
                v = np.var(np.concatenate([yA[idx], yB[idx]]), ddof=1)
                bs_s.append(np.mean(yA[idx] * (yBAi[idx] - yB[idx])) / v)
                bs_t.append(0.5 * np.mean((yB[idx] - yBAi[idx]) ** 2) / v)
            rows.append(dict(param=UNC[i][0], label=UNC_LABEL[UNC[i][0]],
                             S1=float(si), S1_lo=float(np.percentile(bs_s, 2.5)),
                             S1_hi=float(np.percentile(bs_s, 97.5)),
                             ST=float(sti), ST_lo=float(np.percentile(bs_t, 2.5)),
                             ST_hi=float(np.percentile(bs_t, 97.5))))
        rows.sort(key=lambda r: -r["ST"])
        res[oname] = dict(rows=rows, sumS1=float(sum(r["S1"] for r in rows)),
                          sumST=float(sum(r["ST"] for r in rows)),
                          variance=float(var), n=n)
    OUT["sobol"] = res
    pd.DataFrame(res["NER"]["rows"]).to_csv(os.path.join(DATA, "table_sobol_NER.csv"),
                                            index=False)
    pd.DataFrame(res["DUR"]["rows"]).to_csv(os.path.join(DATA, "table_sobol_DUR.csv"),
                                            index=False)
    for r in res["NER"]["rows"][:5]:
        print("  Sobol NER %-9s S1=%.3f ST=%.3f" % (r["param"], r["S1"], r["ST"]))


def metamodel(X, Y, thr):
    """Logistic meta-model and pruned CART for the binary trap outcome."""
    y = (Y[:, 0] > thr).astype(int)
    names = [u[0] for u in UNC]
    Xs = (X - X.mean(0)) / X.std(0, ddof=1)
    res = sm.Logit(y, sm.add_constant(Xs)).fit(disp=0, maxiter=200)
    prob = res.predict(sm.add_constant(Xs))
    rows = []
    for i, nm in enumerate(names):
        rows.append(dict(param=nm, label=UNC_LABEL[nm], coef=float(res.params[i + 1]),
                         se=float(res.bse[i + 1]), z=float(res.tvalues[i + 1]),
                         p=float(res.pvalues[i + 1]),
                         odds_ratio=float(np.exp(res.params[i + 1])),
                         ci_lo=float(np.exp(res.conf_int()[i + 1][0])),
                         ci_hi=float(np.exp(res.conf_int()[i + 1][1]))))
    rows.sort(key=lambda r: -abs(r["z"]))
    llnull = sm.Logit(y, np.ones((len(y), 1))).fit(disp=0).llf
    mcfadden = 1 - res.llf / llnull
    cox = 1 - np.exp(2 * (llnull - res.llf) / len(y))
    nagel = cox / (1 - np.exp(2 * llnull / len(y)))
    # Hosmer-Lemeshow with 10 groups
    order = np.argsort(prob)
    g = np.array_split(order, 10)
    hl = sum(((y[gi].sum() - prob[gi].sum()) ** 2) /
             (prob[gi].sum() * (1 - prob[gi].mean()) + 1e-12) for gi in g)
    OUT["logit"] = dict(rows=rows, n=int(len(y)), trap_rate=float(y.mean()),
                        threshold=float(thr), auc=float(roc_auc_score(y, prob)),
                        mcfadden_r2=float(mcfadden), nagelkerke_r2=float(nagel),
                        llr_chi2=float(2 * (res.llf - llnull)), llr_df=K,
                        llr_p=float(st.chi2.sf(2 * (res.llf - llnull), K)),
                        hosmer_lemeshow=float(hl),
                        hl_p=float(st.chi2.sf(hl, 8)))
    pd.DataFrame(rows).to_csv(os.path.join(DATA, "table_logit.csv"), index=False)
    print("  logit AUC=%.3f  Nagelkerke R2=%.3f  trap rate=%.3f"
          % (OUT["logit"]["auc"], nagel, y.mean()))

    # cross-validated CART
    cv = StratifiedKFold(5, shuffle=True, random_state=3)
    best = None
    for a in [0.0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2]:
        clf = DecisionTreeClassifier(ccp_alpha=a, min_samples_leaf=60,
                                     max_depth=4, random_state=3)
        sc = cross_val_score(clf, X, y, cv=cv, scoring="roc_auc").mean()
        if best is None or sc > best[1]:
            best = (a, sc)
    clf = DecisionTreeClassifier(ccp_alpha=best[0], min_samples_leaf=60,
                                 max_depth=4, random_state=3).fit(X, y)
    txt = export_text(clf, feature_names=names, decimals=3)
    OUT["cart"] = dict(ccp_alpha=best[0], cv_auc=float(best[1]),
                       train_auc=float(roc_auc_score(y, clf.predict_proba(X)[:, 1])),
                       n_leaves=int(clf.get_n_leaves()), rules=txt,
                       importances=dict(zip(names, clf.feature_importances_.round(4).tolist())))
    open(os.path.join(DATA, "cart_rules.txt"), "w").write(txt)
    print("  CART cv-AUC=%.3f, %d leaves, alpha=%g" % (best[1], clf.get_n_leaves(), best[0]))
    # top split thresholds
    tr = clf.tree_
    splits = [(names[tr.feature[i]], float(tr.threshold[i]), int(tr.n_node_samples[i]))
              for i in range(tr.node_count) if tr.feature[i] >= 0]
    OUT["cart"]["splits"] = splits[:8]


# ============================================ 7. policy experiments
SD = {n: (b - a) / np.sqrt(12.0) for n, a, b in UNC}      # sd of the uniform prior

POLICIES = {
    "P1 Skill upgrading": lambda p, e: dict(p, tau=p["tau"] + e * SD["tau"]),
    "P2 Matching efficiency": lambda p, e: dict(p, mu=p["mu"] + e * SD["mu"]),
    "P3 Expectation guidance": lambda p, e: dict(
        p, lam=p["lam"] + e * SD["lam"], zeta=max(0.05, p["zeta"] - e * SD["zeta"])),
    "P4 Vacancy creation": lambda p, e: dict(p, phi=p["phi"] + e * SD["phi"]),
    "P5 Threshold moderation": lambda p, e: dict(
        p, kappa=max(0.1, p["kappa"] - e * SD["kappa"]),
        kappa2=max(0.0, p["kappa2"] - e * SD["kappa2"])),
}


def _policy_run(p_post, start=T_POL, end=T_END):
    _, ys = M.rk4(Y0, P, 0.0, start, DT)
    ts2, ys2 = M.rk4(ys[-1], p_post, start, end, DT)
    s = M.series(ts2, ys2, p_post)
    return dict(NER_T=float(s["NER"][-1]), DUR_T=float(s["DUR"][-1]),
                SE_T=float(s["SEflow"][-1]), MM_T=float(s["MM"][-1]),
                NER_mean=float(s["NER"].mean()), DUR_mean=float(s["DUR"].mean()),
                person_years=float(np.trapezoid(ys2[:, 0] + ys2[:, 1], ts2)))


def _pol_task(args):
    name, effort, draw = args
    p = dict(P)
    if draw is not None:
        for (nm, _, _), v in zip(UNC, draw):
            p[nm] = float(v)
    if name != "Baseline":
        p = POLICIES[name](p, effort)
    return _policy_run(p)


def policies(n_draws=400, effort=1.0):
    lo = np.array([a for _, a, _ in UNC]); hi = np.array([b for _, _, b in UNC])
    D = qmc.scale(qmc.LatinHypercube(d=K, seed=99).random(n_draws), lo, hi)

    tasks, index = [], []
    for name in ["Baseline"] + list(POLICIES):
        for d in D:
            tasks.append((name, effort, d)); index.append(name)
    with Pool() as pool:
        res = pool.map(_pol_task, tasks, chunksize=16)
    df = pd.DataFrame(res); df["policy"] = index
    df.to_csv(os.path.join(DATA, "policy_draws.csv"), index=False)

    base = df[df.policy == "Baseline"]
    rows = []
    for name in POLICIES:
        sub = df[df.policy == name]
        d_ner = sub["NER_T"].values - base["NER_T"].values
        d_dur = sub["DUR_T"].values - base["DUR_T"].values
        d_py = sub["person_years"].values - base["person_years"].values
        w = st.wilcoxon(d_ner)
        rows.append(dict(
            policy=name, NER_T=float(sub["NER_T"].mean()),
            dNER=float(d_ner.mean()),
            dNER_lo=float(np.percentile(d_ner, 2.5)),
            dNER_hi=float(np.percentile(d_ner, 97.5)),
            dDUR=float(d_dur.mean()),
            dDUR_lo=float(np.percentile(d_dur, 2.5)),
            dDUR_hi=float(np.percentile(d_dur, 97.5)),
            d_person_years=float(d_py.mean()),
            wilcoxon_p=float(w.pvalue),
            cliffs_delta=float(2 * (d_ner < 0).mean() - 1)))
    rows.sort(key=lambda r: r["dNER"])
    groups = [df[df.policy == n]["NER_T"].values for n in POLICIES]
    kw = st.kruskal(*groups)
    OUT["policies"] = dict(effort=effort, n_draws=n_draws, rows=rows,
                           baseline_NER=float(base["NER_T"].mean()),
                           kruskal_H=float(kw.statistic), kruskal_p=float(kw.pvalue))
    pd.DataFrame(rows).to_csv(os.path.join(DATA, "table_policies.csv"), index=False)
    for r in rows:
        print("  %-24s dNER %+0.4f [%+0.4f,%+0.4f]  dDUR %+0.3f  p=%.2g"
              % (r["policy"], r["dNER"], r["dNER_lo"], r["dNER_hi"],
                 r["dDUR"], r["wilcoxon_p"]))

    # Dunn post-hoc with Bonferroni correction on terminal NER
    names = list(POLICIES)
    pw = []
    for i, j in itertools.combinations(range(len(names)), 2):
        u = st.mannwhitneyu(groups[i], groups[j])
        pw.append(dict(a=names[i], b=names[j], U=float(u.statistic),
                       p=float(u.pvalue),
                       p_bonf=float(min(1.0, u.pvalue * len(names) * (len(names) - 1) / 2))))
    OUT["policies"]["pairwise"] = pw

    # effort-response frontier
    fr = {}
    for name in POLICIES:
        pts = []
        for e in np.linspace(0.0, 3.0, 13):
            p = POLICIES[name](dict(P), e)
            pts.append((float(e), _policy_run(p)["NER_T"]))
        fr[name] = pts
    OUT["frontier"] = fr

    # combinations at the same total effort (2 units)
    comb = []
    for a, b in itertools.combinations(POLICIES, 2):
        p = POLICIES[b](POLICIES[a](dict(P), 1.0), 1.0)
        r = _policy_run(p)
        comb.append(dict(combo=f"{a} + {b}", NER_T=r["NER_T"], DUR_T=r["DUR_T"],
                         dNER=r["NER_T"] - _policy_run(dict(P))["NER_T"]))
    for a in POLICIES:
        r = _policy_run(POLICIES[a](dict(P), 2.0))
        comb.append(dict(combo=f"{a} x2", NER_T=r["NER_T"], DUR_T=r["DUR_T"],
                         dNER=r["NER_T"] - _policy_run(dict(P))["NER_T"]))
    comb.sort(key=lambda r: r["dNER"])
    OUT["combinations"] = comb
    pd.DataFrame(comb).to_csv(os.path.join(DATA, "table_combinations.csv"), index=False)
    print("  best combination:", comb[0]["combo"], "dNER %.4f" % comb[0]["dNER"])


def sequencing(t_mid=17.5):
    """Same cumulative effort, different order of deployment."""
    base = _policy_run(dict(P))
    out = []
    pairs = [("P3 Expectation guidance", "P1 Skill upgrading"),
             ("P1 Skill upgrading", "P2 Matching efficiency"),
             ("P3 Expectation guidance", "P2 Matching efficiency")]
    for a, b in pairs:
        # simultaneous, 1 unit each, whole period
        p_sim = POLICIES[b](POLICIES[a](dict(P), 1.0), 1.0)
        r_sim = _policy_run(p_sim)
        for first, second, tag in [(a, b, "A-first"), (b, a, "B-first")]:
            _, ys = M.rk4(Y0, P, 0.0, T_POL, DT)
            p1 = POLICIES[first](dict(P), 2.0)
            ts1, ys1 = M.rk4(ys[-1], p1, T_POL, t_mid, DT)
            p2 = POLICIES[second](dict(P), 2.0)
            ts2, ys2 = M.rk4(ys1[-1], p2, t_mid, T_END, DT)
            s1, s2 = M.series(ts1, ys1, p1), M.series(ts2, ys2, p2)
            ner = np.concatenate([s1["NER"], s2["NER"]])
            out.append(dict(pair=f"{a} / {b}", order=tag, first=first,
                            NER_T=float(s2["NER"][-1]),
                            NER_mean=float(ner.mean()),
                            person_years=float(np.trapezoid(
                                np.concatenate([ys1[:, 0] + ys1[:, 1], ys2[:, 0] + ys2[:, 1]]),
                                np.concatenate([ts1, ts2])))))
        out.append(dict(pair=f"{a} / {b}", order="simultaneous", first="-",
                        NER_T=r_sim["NER_T"], NER_mean=r_sim["NER_mean"],
                        person_years=r_sim["person_years"]))
    OUT["sequencing"] = dict(baseline_NER_T=base["NER_T"], rows=out, t_switch=t_mid)
    pd.DataFrame(out).to_csv(os.path.join(DATA, "table_sequencing.csv"), index=False)
    for r in out:
        print("  %-52s %-13s NER_T %.4f  mean %.4f"
              % (r["pair"], r["order"], r["NER_T"], r["NER_mean"]))


# ============================================ 8. prefecture archetypes
ARCHETYPES = {
    "A. Digital core (Hangzhou-type)": dict(phi=2.30, rPsi=0.105, kappa=2.85,
                                            gPhi=0.065, mu=P["mu"] * 1.10),
    "B. Advanced manufacturing (Ningbo-Jiaxing-type)": dict(phi=1.55, rPsi=0.080,
                                                            kappa=2.10, gPhi=0.048),
    "C. Peripheral labour-exporting (south-west Zhejiang-type)":
        dict(phi=0.95, rPsi=0.055, kappa=1.65, gPhi=0.030, mu=P["mu"] * 0.86,
             Pi=P["Pi"] * 1.14),
}


def archetypes():
    rows = []
    for name, over in ARCHETYPES.items():
        p = dict(P, **over)
        y0, ok = eq_at(p, M.GUESS_LOW, 0.0)
        _, ys = M.rk4(y0 if ok else Y0, p, 0.0, T_END, DT)
        d25 = M.indicators(T_END, ys[-1], p)
        d10 = M.indicators(T_POL, M.rk4(y0 if ok else Y0, p, 0.0, T_POL, DT)[1][-1], p)
        # policy responsiveness: best single instrument at effort 1
        best, bestv = None, 1e9
        for nm, f in POLICIES.items():
            _, yy = M.rk4(Y0, p, 0.0, T_POL, DT)
            _, yy2 = M.rk4(yy[-1], f(p, 1.0), T_POL, T_END, DT)
            v = M.indicators(T_END, yy2[-1], f(p, 1.0))["NER"]
            if v < bestv:
                best, bestv = nm, v
        rows.append(dict(archetype=name, NER_2025=d10["NER"], NER_2040=d25["NER"],
                         SEflow_2040=d25["SEflow"], MM_2040=d25["MM"],
                         DUR_2040=d25["DUR"], best_instrument=best,
                         NER_2040_best=bestv, gain=d25["NER"] - bestv))
        print("  %-50s NER2040 %.3f -> %.3f via %s"
              % (name[:50], d25["NER"], bestv, best))
    OUT["archetypes"] = rows
    pd.DataFrame(rows).to_csv(os.path.join(DATA, "table_archetypes.csv"), index=False)


# ============================================ numerical robustness
def step_check():
    out = {}
    for dt in [1 / 6, 1 / 12, 1 / 24, 1 / 48]:
        _, ys = M.rk4(Y0, P, 0.0, T_END, dt)
        out["dt=1/%d" % round(1 / dt)] = float(M.indicators(T_END, ys[-1], P)["NER"])
    ref = out["dt=1/48"]
    OUT["integration_check"] = dict(values=out,
                                    max_rel_dev=float(max(abs(v - ref) / ref
                                                          for v in out.values())))
    print("  integration check:", {k: round(v, 6) for k, v in out.items()})


# ============================================ main
if __name__ == "__main__":
    print("[1] baseline and validation")
    ts, ys, s = baseline()
    print("    NER 2025 = %.4f, NER 2040 = %.4f, RMSPE = %.4f"
          % (s["NER"][yr(10)], s["NER"][-1], OUT["validation"]["rmspe"]))
    step_check()

    print("[2] moving attractor, continuation and shock persistence")
    bifurcation()
    drift_lag(s)
    shock_persistence()
    thr = TRAP_THRESHOLD

    print("[3] loop knockout")
    knockout()

    print("[4] Monte Carlo")
    X, Y = montecarlo()
    print("    NER 2040: mean %.4f, 95%% CI [%.4f, %.4f]"
          % (OUT["montecarlo"]["NER"]["mean"], OUT["montecarlo"]["NER"]["q"][0],
             OUT["montecarlo"]["NER"]["q"][-1]))

    print("[5] Sobol indices")
    sobol()

    print("[6] meta-models")
    metamodel(X, Y, thr)

    print("[7] policy experiments")
    policies()
    sequencing()

    print("[8] archetypes")
    archetypes()

    OUT["params"] = P
    OUT["calibration"] = CAL
    OUT["unc_ranges"] = {n: [a, b] for n, a, b in UNC}
    with open(os.path.join(HERE, "stats.json"), "w") as f:
        json.dump(OUT, f, indent=1)
    print("\nwritten stats.json")
