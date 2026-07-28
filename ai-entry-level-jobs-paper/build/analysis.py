# -*- coding: utf-8 -*-
"""Counterfactuals, efficiency analysis and policy evaluation for the job-ladder
model.  Every number reported in the manuscript is produced here.

Outputs
-------
stats.json        every scalar result, keyed by section
../data/*.csv     the series behind each figure and table
"""
from __future__ import annotations

import itertools
import json
import math
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from scipy.optimize import brentq, least_squares, root
from scipy.stats import qmc

import ladder as L
from calibrate import FREE

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
os.makedirs(DATA, exist_ok=True)

CAL = json.load(open(os.path.join(HERE, "calibrated.json")))
FREE_KEYS = [k for k, _, _ in FREE]
LO = np.array([lo for _, lo, _ in FREE])
HI = np.array([hi for _, _, hi in FREE])
MOM = [(m["moment"], m["target"]) for m in CAL["moments"]]

BUDGET = 0.0005         # common fiscal envelope, as a share of output
GAMMA_W = 0.800         # baseline real rigidity of the entry wage
AI_TARGET = 0.500       # counterfactual share of entry-level tasks done by AI

P0 = dict(L.BASE)
P0.update({k: CAL["params"][k] for k in FREE_KEYS})
P0["gamma_w"], P0["w_ref"] = 0.0, 0.0
X0 = np.array(CAL["x0"], float)
_ref, _ok, X0 = L.solve(P0, x0=X0)           # reference entry wage
assert _ok, "reference equilibrium did not converge"
P0["w_ref"] = float(_ref["w_j"])
P0["gamma_w"] = GAMMA_W

S = {}


def dump(name, df):
    df.to_csv(os.path.join(DATA, name), index=False)
    return df


def pset(**kw):
    p = dict(P0)
    p.update(kw)
    return p


def enrich(r):
    """Outcome variables used throughout: rates and ladder throughput."""
    r = dict(r)
    r["emp_rate_j"] = 1.0 - r["u_rate_j"]
    r["throughput"] = r["pi"] * r["e_j"]          # promotions per unit time
    r["mentoring"] = r["m"] * r["e_j"]            # aggregate senior training time
    r["U_total"] = r["u_j"] + r["u_s"]
    return r


def eq(p, x0=None):
    res, ok, x = L.solve(p, x0=X0 if x0 is None else x0)
    if not ok:
        raise RuntimeError("market equilibrium did not converge")
    return enrich(res), x


def pl(p, x0=None):
    res, ok, x = L.solve_planner(p, x0=X0 if x0 is None else x0)
    if not ok:
        raise RuntimeError("planner problem did not converge")
    return enrich(res), x


KEYS = ("theta_j", "theta_s", "m", "pi", "promo_years", "f_j", "f_s",
        "u_rate_j", "emp_rate_j", "u_rate_s", "e_j", "e_s", "u_j", "u_s",
        "U_total", "H_j", "throughput", "mentoring", "w_j", "w_s",
        "wage_ratio", "A", "ai_share", "Y", "welfare", "labour_share",
        "J_j", "J_s", "U_j", "U_s", "W_s", "Sj", "Ss", "F_s", "G_j",
        "train_share", "mentor_share", "senior_emp_share", "hire_cost_j",
        "hire_cost_s", "repl_rate", "search_months_j")


# =====================================================================  1
def section_baseline():
    base, xb = eq(P0)
    plan, xp = pl(P0, xb)

    S["baseline"] = {k: float(base[k]) for k in KEYS}
    S["planner"] = {k: float(plan[k]) for k in KEYS if k in plan}
    S["planner"].update({k: float(plan[k]) for k in
                         ("lam_uj", "lam_ej", "lam_us", "lam_es")})

    gap = {k: float(plan[k] / base[k] - 1.0) for k in
           ("theta_j", "theta_s", "m", "pi", "mentoring", "throughput",
            "e_j", "e_s", "H_j", "Y", "U_total")}
    gap["welfare_pct"] = float(100.0 * (plan["welfare"] / base["welfare"] - 1.0))
    gap["promo_years_diff"] = float(plan["promo_years"] - base["promo_years"])
    S["wedge"] = gap

    # attribute the mentoring gap to its two sources by a Shapley decomposition
    def market_with(remove):
        q = dict(P0)
        if "poach" in remove:
            q["phi"] = 0.0
        if "holdup" in remove:
            q["train_mode"] = "joint"
        return eq(q)[0]

    v, names = {}, ("poach", "holdup")
    for k in range(len(names) + 1):
        for combo in itertools.combinations(names, k):
            v[frozenset(combo)] = math.log(market_with(set(combo))["mentoring"])
    full, shap = frozenset(names), {}
    for i in names:
        tot = 0.0
        for k in range(len(full - {i}) + 1):
            for combo in itertools.combinations(full - {i}, k):
                Ss = frozenset(combo)
                w = (math.factorial(len(Ss)) *
                     math.factorial(len(full) - len(Ss) - 1) /
                     math.factorial(len(full)))
                tot += w * (v[Ss | {i}] - v[Ss])
        shap[i] = float(tot)
    tot_gap = v[full] - v[frozenset()]
    S["wedge_sources"] = dict(
        total_log_gap=float(tot_gap), poaching=shap["poach"],
        holdup=shap["holdup"],
        poaching_share=float(shap["poach"] / tot_gap),
        holdup_share=float(shap["holdup"] / tot_gap),
        removed_both_pct=float(100 * (math.exp(tot_gap) - 1)),
        residual_to_planner_pct=float(
            100 * (S["planner"]["mentoring"] / math.exp(v[full]) - 1)))

    gaps, ok = L.efficiency_check(dict(P0), verbose=False)
    S["efficiency_check"] = dict(converged=bool(ok),
                                 max_rel_gap=float(max(gaps.values())),
                                 **{k: float(x) for k, x in gaps.items()})
    return base, xb, plan, xp


# =====================================================================  2
def ai_path(base, xb, xp, n=41, floor=0.55):
    pa0 = P0["p_a"]
    grid = np.linspace(pa0, floor * pa0, n)
    rows, xm, xpp = [], xb.copy(), xp.copy()
    for pa in grid:
        p = pset(p_a=float(pa))
        try:
            r, xm = eq(p, xm)
        except RuntimeError:
            r, xm = eq(p)
        try:
            q, xpp = pl(p, xpp)
        except RuntimeError:
            q, xpp = pl(p)
        rows.append(dict(
            p_a=float(pa), ai_share=r["ai_share"], A=r["A"],
            theta_j=r["theta_j"], m=r["m"], pi=r["pi"],
            promo_years=r["promo_years"], e_j=r["e_j"], e_s=r["e_s"],
            H_j=r["H_j"], emp_rate_j=r["emp_rate_j"], u_rate_j=r["u_rate_j"],
            u_rate_s=r["u_rate_s"], throughput=r["throughput"],
            mentoring=r["mentoring"], w_j=r["w_j"], w_s=r["w_s"],
            wage_ratio=r["wage_ratio"], U_j=r["U_j"], U_s=r["U_s"],
            Y=r["Y"], welfare=r["welfare"], U_total=r["U_total"],
            plan_m=q["m"], plan_mentoring=q["mentoring"],
            plan_welfare=q["welfare"], plan_throughput=q["throughput"],
            wedge_mentoring=q["mentoring"] / r["mentoring"] - 1.0,
            wedge_throughput=q["throughput"] / r["throughput"] - 1.0,
            welfare_gap_pct=100.0 * (q["welfare"] / r["welfare"] - 1.0)))
    df = dump("ai_path.csv", pd.DataFrame(rows))

    pa_star = float(np.interp(AI_TARGET, df["ai_share"], df["p_a"]))
    shock, _ = eq(pset(p_a=pa_star))
    plan_s, _ = pl(pset(p_a=pa_star))
    flex, _ = eq(pset(p_a=pa_star, gamma_w=0.0))

    def d(a, b_, key):
        return float(math.log(a[key] / b_[key]))

    S["shock"] = dict(
        target_ai_share=AI_TARGET, p_a=pa_star,
        p_a_fall_pct=float(100.0 * (pa_star / P0["p_a"] - 1.0)),
        d_ln_emp_rate_j=d(shock, base, "emp_rate_j"),
        d_ln_w_j=d(shock, base, "w_j"),
        d_ln_w_s=d(shock, base, "w_s"),
        incidence_ratio=float(d(shock, base, "emp_rate_j") /
                              d(shock, base, "w_j")),
        d_ln_H_j=d(shock, base, "H_j"),
        d_ln_e_j=d(shock, base, "e_j"),
        d_ln_e_s=d(shock, base, "e_s"),
        d_ln_m=d(shock, base, "m"),
        d_ln_mentoring=d(shock, base, "mentoring"),
        d_ln_throughput=d(shock, base, "throughput"),
        d_u_rate_j_pp=float(100 * (shock["u_rate_j"] - base["u_rate_j"])),
        d_u_rate_s_pp=float(100 * (shock["u_rate_s"] - base["u_rate_s"])),
        d_promo_years=float(shock["promo_years"] - base["promo_years"]),
        d_Y_pct=float(100 * (shock["Y"] / base["Y"] - 1)),
        d_welfare_pct=float(100 * (shock["welfare"] / base["welfare"] - 1)),
        d_U_j_pct=float(100 * (shock["U_j"] / base["U_j"] - 1)),
        d_U_s_pct=float(100 * (shock["U_s"] / base["U_s"] - 1)),
        d_W_s_pct=float(100 * (shock["W_s"] / base["W_s"] - 1)),
        wedge_mentoring_before=float(S["wedge"]["mentoring"]),
        wedge_mentoring_after=float(plan_s["mentoring"] / shock["mentoring"] - 1),
        welfare_gap_before=float(S["wedge"]["welfare_pct"]),
        welfare_gap_after=float(100 * (plan_s["welfare"] / shock["welfare"] - 1)),
        flex_d_ln_emp_rate_j=d(flex, base, "emp_rate_j"),
        flex_d_ln_w_j=d(flex, base, "w_j"),
        flex_incidence_ratio=float(d(flex, base, "emp_rate_j") /
                                   d(flex, base, "w_j")))
    return df, pa_star, shock


# =====================================================================  3
def channels(base, pa_star):
    names = ("training", "promotion_value", "senior_scarcity")
    frozen = dict(training=dict(m=base["m"]),
                  promotion_value=dict(J_s=base["J_s"], W_s=base["W_s"]),
                  senior_scarcity=dict(F_s=base["F_s"]))

    def run(active):
        frz = {}
        for nm in names:
            if nm not in active:
                frz.update(frozen[nm])
        p = pset(p_a=pa_star)
        p["_frz"] = frz
        return eq(p)[0]

    v = {}
    for k in range(len(names) + 1):
        for combo in itertools.combinations(names, k):
            v[frozenset(combo)] = math.log(run(set(combo))["emp_rate_j"] /
                                           base["emp_rate_j"])
    full, shap = frozenset(names), {}
    for i in names:
        tot = 0.0
        for k in range(len(full - {i}) + 1):
            for combo in itertools.combinations(full - {i}, k):
                Ss = frozenset(combo)
                w = (math.factorial(len(Ss)) *
                     math.factorial(len(full) - len(Ss) - 1) /
                     math.factorial(len(full)))
                tot += w * (v[Ss | {i}] - v[Ss])
        shap[i] = float(tot)

    direct, total = float(v[frozenset()]), float(v[full])
    rows = [dict(channel="direct task substitution", contribution=direct,
                 share=direct / total)]
    for nm in names:
        rows.append(dict(channel=nm.replace("_", " "), contribution=shap[nm],
                         share=shap[nm] / total))
    rows.append(dict(channel="total", contribution=total, share=1.0))
    dump("channels.csv", pd.DataFrame(rows))
    S["channels"] = dict(total=total, direct=direct, **shap,
                         check=float(direct + sum(shap.values()) - total))
    return rows


def _solve_for_ai_share(target, **kw):
    """Price of AI that delivers a given task share, with a scanned bracket."""
    def f(pa):
        return eq(pset(p_a=float(pa), **kw))[0]["ai_share"] - target
    lo_v = lo_c = None
    for pa in np.geomspace(0.02, 30.0, 90):
        try:
            c = f(pa)
        except Exception:
            continue
        if lo_c is not None and lo_c * c < 0:
            return brentq(f, lo_v, pa, xtol=1e-13, rtol=1e-15)
        lo_v, lo_c = pa, c
    raise ValueError("no bracket for an AI task share of %.3f" % target)


# =====================================================================  4
def rigidity_and_sigma(base, pa_star):
    rows = []
    for g in (0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0):
        try:
            b, xg = eq(pset(gamma_w=g))
            r, _ = eq(pset(gamma_w=g, p_a=pa_star), xg)
        except RuntimeError:
            continue
        dw = math.log(r["w_j"] / b["w_j"])
        de = math.log(r["emp_rate_j"] / b["emp_rate_j"])
        rows.append(dict(gamma_w=g, d_ln_w_j=dw, d_ln_emp_rate_j=de,
                         incidence_ratio=(de / dw) if abs(dw) > 1e-9 else np.nan,
                         d_ln_mentoring=math.log(r["mentoring"] / b["mentoring"]),
                         d_welfare_pct=100 * (r["welfare"] / b["welfare"] - 1)))
    dump("rigidity.csv", pd.DataFrame(rows))
    S["rigidity"] = rows

    rows2 = []
    fall = pa_star / P0["p_a"]
    for sig in (1.5, 2.0, 2.5, 3.0, 4.0, 5.0):
        rho = 1.0 - 1.0 / sig
        try:
            # re-target the price of AI so that every economy starts from the
            # same calibrated AI task share; then apply the same price fall
            pa_sig = _solve_for_ai_share(base["ai_share"], rho=rho)
            b, xb2 = eq(pset(rho=rho, p_a=pa_sig))
            r, _ = eq(pset(rho=rho, p_a=pa_sig * fall), xb2)
            q, _ = pl(pset(rho=rho, p_a=pa_sig), xb2)
        except (RuntimeError, ValueError):
            continue
        rows2.append(dict(sigma=sig, rho=rho, p_a=float(pa_sig),
                          ai_share=b["ai_share"],
                          d_ln_emp_rate_j=math.log(r["emp_rate_j"] /
                                                   b["emp_rate_j"]),
                          d_ln_mentoring=math.log(r["mentoring"] /
                                                  b["mentoring"]),
                          wedge_mentoring=q["mentoring"] / b["mentoring"] - 1,
                          welfare_gap_pct=100 * (q["welfare"] / b["welfare"] - 1)))
    dump("sigma_sensitivity.csv", pd.DataFrame(rows2))
    S["sigma"] = rows2


# =====================================================================  5
def implementation(p_base, tag):
    target, _ = pl(p_base)

    def resid(z):
        p = dict(p_base)
        p["s_v"], p["s_m"], p["s_vs"] = float(z[0]), float(z[1]), float(z[2])
        r, _ = eq(p)
        return np.array([math.log(r["theta_j"] / target["theta_j"]),
                         math.log(r["m"] / target["m"]),
                         math.log(r["theta_s"] / target["theta_s"])])

    best, err = None, np.inf
    for g in ([0.1, 0.8, 0.1], [0.0, 0.9, 0.0], [0.3, 0.5, 0.2],
              [-0.2, 0.95, 0.05]):
        try:
            sol = root(resid, np.array(g), method="hybr", tol=1e-12)
            e = float(np.max(np.abs(resid(sol.x))))
            if e < err:
                best, err = sol.x, e
        except Exception:
            pass
        if err < 1e-9:
            break
    z = best
    p = dict(p_base)
    p["s_v"], p["s_m"], p["s_vs"] = map(float, z)
    r, _ = eq(p)
    base, _ = eq(p_base)
    out = dict(s_v=float(z[0]), s_m=float(z[1]), s_vs=float(z[2]),
               max_resid=float(err),
               fiscal_pct_Y=float(100 * r["fiscal"] / r["Y"]),
               welfare_gain_pct=float(100 * (r["welfare"] / base["welfare"] - 1)),
               d_mentoring_pct=float(100 * (r["mentoring"] / base["mentoring"] - 1)),
               d_emp_rate_j_pct=float(100 * (r["emp_rate_j"] /
                                             base["emp_rate_j"] - 1)),
               promo_years=float(r["promo_years"]),
               ai_share_market=float(base["ai_share"]),
               ai_share_optimum=float(target["ai_share"]))
    S["implementation_" + tag] = out
    return out


def optimal_ai_tax(p_base):
    imp = S["implementation_baseline"]
    p = dict(p_base)
    p["s_v"], p["s_m"], p["s_vs"] = imp["s_v"], imp["s_m"], imp["s_vs"]
    rows = []
    for t in np.linspace(-0.10, 0.50, 31):
        q = dict(p)
        q["t_a"] = float(t)
        try:
            r, _ = eq(q)
        except RuntimeError:
            continue
        rows.append(dict(t_a=float(t), welfare=r["welfare"],
                         emp_rate_j=r["emp_rate_j"], ai_share=r["ai_share"],
                         fiscal=r["fiscal"]))
    df = dump("ai_tax.csv", pd.DataFrame(rows))
    i = int(df["welfare"].idxmax())
    S["ai_tax"] = dict(argmax_t_a=float(df.loc[i, "t_a"]),
                       welfare_max=float(df["welfare"].max()),
                       welfare_at_zero=float(
                           df.loc[df["t_a"].abs().idxmin(), "welfare"]))
    return df


# =====================================================================  6
INSTR = [("s_m", "Mentoring / training credit"),
         ("s_v", "Entry-level vacancy subsidy"),
         ("s_w", "Entry-level wage subsidy"),
         ("t_a", "Tax on the AI input")]


def _rate_for_budget(p_base, key, G):
    """Instrument rate that costs the Treasury exactly G.

    The bracket is found by scanning, because extreme instrument values can
    leave the region in which the equilibrium exists.
    """
    sign = -1.0 if key == "t_a" else 1.0
    hi = 0.97 if key != "t_a" else 5.0

    def cost(v):
        q = dict(p_base)
        q[key] = float(v)
        return sign * eq(q)[0]["fiscal"] - G

    grid = np.concatenate([[1e-9], np.geomspace(1e-6, hi, 60)])
    lo_v = lo_c = None
    for v in grid:
        try:
            c = cost(v)
        except Exception:
            break                     # left the existence region; stop scanning
        if not np.isfinite(c):
            break
        if lo_c is not None and lo_c * c < 0:
            return brentq(cost, lo_v, v, xtol=1e-13, rtol=1e-15)
        lo_v, lo_c = v, c
    raise ValueError("no bracket for %s at budget %.3g" % (key, G))


def _revenue_peak(p_base, key="t_a"):
    """Largest revenue the AI tax can raise, and the rate that raises it."""
    best = (0.0, -np.inf)
    for t in np.geomspace(1e-4, 5.0, 120):
        q = dict(p_base)
        q[key] = float(t)
        try:
            rev = -eq(q)[0]["fiscal"]
        except Exception:
            break
        if rev > best[1]:
            best = (float(t), float(rev))
    return best


def budget_experiment(p_base, tag, budget_frac=BUDGET):
    base, _ = eq(p_base)
    G = budget_frac * base["Y"]
    rows = []
    for key, label in INSTR:
        sign = -1.0 if key == "t_a" else 1.0
        try:
            val = _rate_for_budget(p_base, key, G)
        except ValueError:
            peak = _revenue_peak(p_base, key) if key == "t_a" else None
            rows.append(dict(instrument=label, key=key, rate=np.nan,
                             note=("maximum attainable revenue %.4f%% of output"
                                   % (100 * peak[1] / base["Y"]))
                             if peak else "no feasible rate"))
            if peak:
                S["ai_tax_laffer"] = dict(
                    t_a_at_peak=float(peak[0]),
                    peak_revenue_pct_Y=float(100 * peak[1] / base["Y"]),
                    budget_pct_Y=float(100 * budget_frac))
            continue
        q = dict(p_base)
        q[key] = float(val)
        r, _ = eq(q)
        dW = r["welfare"] - base["welfare"]
        rows.append(dict(
            instrument=label, key=key, rate=float(val),
            fiscal_pct_Y=float(100 * sign * r["fiscal"] / base["Y"]),
            d_welfare_pct=float(100 * dW / base["welfare"]),
            d_emp_rate_j_pct=float(100 * (r["emp_rate_j"] /
                                          base["emp_rate_j"] - 1)),
            d_f_j_pct=float(100 * (r["f_j"] / base["f_j"] - 1)),
            d_theta_j_pct=float(100 * (r["theta_j"] / base["theta_j"] - 1)),
            d_mentoring_pct=float(100 * (r["mentoring"] / base["mentoring"] - 1)),
            d_throughput_pct=float(100 * (r["throughput"] /
                                          base["throughput"] - 1)),
            d_U_j_pct=float(100 * (r["U_j"] / base["U_j"] - 1)),
            d_promo_years=float(r["promo_years"] - base["promo_years"]),
            mvpf=float(1.0 + dW / (sign * r["fiscal"]))))
    df = pd.DataFrame(rows).sort_values("d_welfare_pct", ascending=False)
    dump("policy_%s.csv" % tag, df)
    S["policy_" + tag] = df.to_dict("records")
    return df


# =====================================================================  7
EXT = [("r", 0.030, 0.055), ("omega", 0.020, 0.032),
       ("delta_j", 0.170, 0.280), ("delta_s", 0.065, 0.110),
       ("phi", 0.100, 0.280), ("eta", 0.400, 0.600),
       ("rho", 0.350, 0.800), ("psi", 0.250, 0.600)]


def recalibrate(p_ext, start):
    keys = FREE_KEYS

    def res(v):
        q = dict(p_ext)
        q.update({k: float(x) for k, x in zip(keys, v)})
        q["gamma_w"], q["w_ref"] = 0.0, 0.0
        try:
            r, ok, _ = L.solve(q, x0=X0)
            if (not ok or r["A"] <= 1e-9 or r["m"] <= 1e-9 or r["w_j"] <= 0
                    or not np.isfinite(r["Y"]) or r["Y"] <= 0):
                return np.full(len(keys), 5.0)
            out = np.array([math.log(max(r[k], 1e-12) / t) for k, t in MOM])
            return out if np.isfinite(out).all() else np.full(len(keys), 5.0)
        except Exception:
            return np.full(len(keys), 5.0)

    sol = least_squares(res, np.clip(start, LO, HI), bounds=(LO, HI),
                        method="trf", xtol=1e-14, ftol=1e-14, gtol=1e-14,
                        max_nfev=1200)
    return sol.x, float(np.max(np.abs(res(sol.x))))


def _draw(args):
    i, vals = args
    p = dict(P0)
    for (k, _, _), v in zip(EXT, vals):
        p[k] = float(v)
    p["beta"] = p["eta"]
    p["gamma_w"], p["w_ref"] = 0.0, 0.0
    try:
        vec, err = recalibrate(p, np.array([P0[k] for k in FREE_KEYS]))
        if err > 1e-6:
            return None
        q = dict(p)
        q.update({k: float(x) for k, x in zip(FREE_KEYS, vec)})
        ref = L.solve(q, x0=X0)[0]
        q["w_ref"], q["gamma_w"] = float(ref["w_j"]), GAMMA_W
        base = enrich(ref)
        plan = enrich(L.solve_planner(q, x0=X0)[0])
        G = BUDGET * base["Y"]
        out = {}
        for key, _ in INSTR:
            sign = -1.0 if key == "t_a" else 1.0
            try:
                z = dict(q)
                z[key] = float(_rate_for_budget(q, key, G))
                r, _ = eq(z)
                out["gain_" + key] = float(100 * (r["welfare"] /
                                                  base["welfare"] - 1))
            except Exception:
                out["gain_" + key] = np.nan
        return dict(i=i, err=err,
                    **{k: float(p[k]) for k, _, _ in EXT},
                    wedge_mentoring=float(plan["mentoring"] /
                                          base["mentoring"] - 1),
                    wedge_throughput=float(plan["throughput"] /
                                           base["throughput"] - 1),
                    welfare_gap_pct=float(100 * (plan["welfare"] /
                                                 base["welfare"] - 1)),
                    **out)
    except Exception:
        return None


def uncertainty(n=192, seed=20260728):
    lo = np.array([a for _, a, _ in EXT])
    hi = np.array([b for _, _, b in EXT])
    cached = os.path.join(DATA, "uncertainty.csv")
    if os.environ.get("REUSE_UNCERTAINTY") and os.path.exists(cached):
        df = pd.read_csv(cached)
    else:
        draws = lo + qmc.LatinHypercube(d=len(EXT), seed=seed).random(n) * (hi - lo)
        with ProcessPoolExecutor() as ex:
            got = list(ex.map(_draw, [(i, draws[i]) for i in range(n)],
                              chunksize=2))
        df = dump("uncertainty.csv",
                  pd.DataFrame([g for g in got if g is not None]))
    cols = ["gain_" + k for k, _ in INSTR]
    # an instrument that cannot raise the required revenue in a given draw is
    # simply not available there; it must not remove the draw from the ranking
    ok = df.dropna(subset=cols, how="all")
    best = ok[cols].idxmax(axis=1, skipna=True)
    S["uncertainty"] = dict(
        n_requested=n, n_solved=int(len(df)), n_ranked=int(len(ok)),
        instrument_feasible_share={c: float(df[c].notna().mean()) for c in cols},
        wedge_mentoring_mean=float(df["wedge_mentoring"].mean()),
        wedge_mentoring_p5=float(df["wedge_mentoring"].quantile(0.05)),
        wedge_mentoring_p95=float(df["wedge_mentoring"].quantile(0.95)),
        wedge_positive_share=float((df["wedge_mentoring"] > 0).mean()),
        welfare_gap_mean=float(df["welfare_gap_pct"].mean()),
        welfare_gap_p5=float(df["welfare_gap_pct"].quantile(0.05)),
        welfare_gap_p95=float(df["welfare_gap_pct"].quantile(0.95)),
        best_instrument_shares={c: float((best == c).mean()) for c in cols})
    return df


# =====================================================================  8
def exposure_validation(base, shares=(0.05, 0.12, 0.25, 0.40, 0.55)):
    rows = []
    for sh in shares:
        def gap(chi):
            return eq(pset(chi=float(chi)))[0]["ai_share"] - sh
        chi = brentq(gap, 1e-3, 40.0, xtol=1e-11, rtol=1e-13)
        with_ai, _ = eq(pset(chi=float(chi)))
        no_ai, _ = eq(pset(chi=float(chi), p_a=1e5))
        rows.append(dict(ai_share=float(sh), chi=float(chi),
                         emp_rate_j=float(with_ai["emp_rate_j"]),
                         emp_rate_j_preAI=float(no_ai["emp_rate_j"]),
                         e_s=float(with_ai["e_s"]),
                         e_s_preAI=float(no_ai["e_s"]),
                         d_ln_emp_j=float(math.log(with_ai["emp_rate_j"] /
                                                   no_ai["emp_rate_j"])),
                         d_ln_e_s=float(math.log(with_ai["e_s"] / no_ai["e_s"])),
                         d_ln_w_j=float(math.log(with_ai["w_j"] / no_ai["w_j"])),
                         promo_years=float(with_ai["promo_years"])))
    df = dump("exposure.csv", pd.DataFrame(rows))
    top, bot = df.iloc[-1], df.iloc[0]
    did = float((top["d_ln_emp_j"] - top["d_ln_e_s"])
                - (bot["d_ln_emp_j"] - bot["d_ln_e_s"]))
    S["exposure"] = dict(
        share_lo=float(shares[0]), share_hi=float(shares[-1]),
        did_log=did, did_pct=float(100 * (math.exp(did) - 1.0)),
        target_pct=-16.0,
        top_d_ln_emp_j=float(top["d_ln_emp_j"]),
        bottom_d_ln_emp_j=float(bot["d_ln_emp_j"]),
        wage_did_pct=float(100 * (math.exp(top["d_ln_w_j"] -
                                           bot["d_ln_w_j"]) - 1)),
        gradient_per_10pp=float(100 * np.polyfit(df["ai_share"],
                                                 df["d_ln_emp_j"], 1)[0] * 0.10))
    return df


# =====================================================================  main
def main():
    print("1. baseline and the efficiency wedge", flush=True)
    base, xb, plan, xp = section_baseline()
    print("   mentoring gap to the optimum: %+.0f%%   welfare gap %+.2f%%"
          % (100 * S["wedge"]["mentoring"], S["wedge"]["welfare_pct"]))

    print("2. the AI price path", flush=True)
    path, pa_star, shock = ai_path(base, xb, xp)
    print("   at an AI task share of %.2f: entry-level employment rate %+.1f%%, "
          "entry wage %+.1f%%"
          % (AI_TARGET, 100 * (math.exp(S["shock"]["d_ln_emp_rate_j"]) - 1),
             100 * (math.exp(S["shock"]["d_ln_w_j"]) - 1)))

    print("3. channel decomposition", flush=True)
    channels(base, pa_star)

    print("4. wage rigidity and substitutability", flush=True)
    rigidity_and_sigma(base, pa_star)

    print("5. implementing the optimum", flush=True)
    implementation(P0, "baseline")
    implementation(pset(p_a=pa_star), "post_ai")
    optimal_ai_tax(P0)

    print("6. equal-budget policy comparison", flush=True)
    budget_experiment(P0, "baseline")
    budget_experiment(pset(p_a=pa_star), "post_ai")

    print("7. held-out exposure gradient", flush=True)
    exposure_validation(base)

    print("8. parameter uncertainty", flush=True)
    uncertainty()

    S["meta"] = dict(max_log_resid=CAL["max_log_resid"], moments=CAL["moments"],
                     params=CAL["params"], checks=CAL["checks"],
                     gamma_w=GAMMA_W, budget=BUDGET, ai_target=AI_TARGET)
    json.dump(S, open(os.path.join(HERE, "stats.json"), "w"), indent=1)
    print("written stats.json")


if __name__ == "__main__":
    main()
