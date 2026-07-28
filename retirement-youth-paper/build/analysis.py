# -*- coding: utf-8 -*-
"""Counterfactuals, decompositions and policy evaluation for the rationing model.

Every number reported in the manuscript is produced here.

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
from scipy.optimize import brentq, least_squares
from scipy.stats import qmc

import rationing as Q
from calibrate import FREE, MOMENTS, LO, HI

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
os.makedirs(DATA, exist_ok=True)

CAL = json.load(open(os.path.join(HERE, "calibrated.json")))
FREE_KEYS = [k for k, _, _ in FREE]
MOM = [(m["moment"], m["target"]) for m in CAL["moments"]]

R0 = 56.3          # effective statutory retirement age before the reform
R1 = 59.9          # after the fully phased reform
PHASE = 15.0       # years of phase-in
COHORT = 12.7      # entering cohort, millions, used only to scale the results
BUDGET = 0.0010    # common fiscal envelope, as a share of output

P0 = dict(Q.BASE)
P0.update({k: CAL["params"][k] for k in FREE_KEYS})
P0["R"] = R0

S = {}


def dump(name, df):
    df.to_csv(os.path.join(DATA, name), index=False)
    return df


def pset(**kw):
    p = dict(P0)
    p.update(kw)
    return p


def eq(p):
    r, ok = Q.solve(p)
    if not ok or r is None:
        raise RuntimeError("equilibrium did not converge")
    return r


KEYS = ("theta", "lam_Q", "queue_years", "u_rate_y", "u_rate_p", "queue_share",
        "quota_share", "wage_premium", "repl_rate", "cohort_entry_Q",
        "search_months_y", "V_entrant", "welfare", "welfare_pc", "Y", "L",
        "young", "prime", "emp", "u_q", "u_m", "e_q", "e_m", "U_m", "E_q",
        "E_m", "v_Q", "v_M", "N", "w_Q", "w_y", "w_p", "wbar_M", "f_y", "f_p",
        "W_q_y", "V_y", "V_p", "queue_loss", "rho", "gamma", "a_q")


def access(r):
    """Statistics describing what a new entrant actually faces."""
    return dict(
        entry_prob=r["cohort_entry_Q"],              # chance of an establishment job
        queue_years=r["queue_years"],
        u_rate_y=r["u_rate_y"],
        quota_share=r["quota_share"],
        f_y=r["f_y"],
        V_entrant=r["V_entrant"])


# =====================================================================  1
def section_baseline():
    base = eq(P0)
    S["baseline"] = {k: float(base[k]) for k in KEYS}
    S["scaled"] = dict(
        cohort_millions=COHORT,
        queueing_millions=float(base["u_q"] * COHORT),
        quota_hires_millions=float(base["v_Q"] * COHORT),
        young_unemployed_millions=float((base["u_q"] + base["u_m"]) * COHORT),
        establishment_millions=float(base["N"] * COHORT),
        labour_force_millions=float(base["L"] * COHORT))
    # the queue produces nothing at the margin: the establishment hires v_Q
    # however long the line is, so the queue's output cost is a pure loss
    S["queue_cost"] = dict(
        queuers=float(base["u_q"]),
        forgone_output=float(base["queue_loss"]),
        pct_of_output=float(100 * base["queue_loss"] / base["Y"]),
        pct_of_youth_nonemployment=float(100 * base["queue_share"]),
        break_even_screening=float(Q.break_even_screening(P0, base)))
    return base


# =====================================================================  2
def reform_path(base, n=37):
    rows = []
    for R in np.linspace(R0, R1, n):
        r = eq(pset(R=float(R)))
        rows.append(dict(R=float(R), year=2025.0 + PHASE * (R - R0) / (R1 - R0),
                         **{k: float(r[k]) for k in
                            ("rho", "u_rate_y", "u_rate_p", "queue_years",
                             "queue_share", "cohort_entry_Q", "quota_share",
                             "theta", "f_y", "u_q", "u_m", "v_Q", "V_entrant",
                             "welfare_pc", "L", "emp", "e_q", "e_m", "E_q",
                             "E_m", "w_y", "queue_loss", "Y")}))
    df = dump("reform_path.csv", pd.DataFrame(rows))

    end = eq(pset(R=R1))

    def d(k):
        return float(end[k] / base[k] - 1.0)

    S["reform"] = dict(
        R0=R0, R1=R1, phase_years=PHASE,
        d_rho=d("rho"),
        d_u_rate_y=d("u_rate_y"),
        u_rate_y_pp=float(100 * (end["u_rate_y"] - base["u_rate_y"])),
        d_u_rate_p=d("u_rate_p"),
        u_rate_p_pp=float(100 * (end["u_rate_p"] - base["u_rate_p"])),
        d_entry_prob=d("cohort_entry_Q"),
        entry_prob_pp=float(100 * (end["cohort_entry_Q"] -
                                   base["cohort_entry_Q"])),
        entry_lost_thousands=float(1000 * COHORT *
                                   (base["cohort_entry_Q"] -
                                    end["cohort_entry_Q"])),
        d_queue_years=d("queue_years"),
        queue_years_diff=float(end["queue_years"] - base["queue_years"]),
        d_queue_share=d("queue_share"),
        d_quota_share=d("quota_share"),
        quota_share_pp=float(100 * (end["quota_share"] - base["quota_share"])),
        d_theta=d("theta"), d_f_y=d("f_y"),
        d_V_entrant=d("V_entrant"),
        d_L=d("L"), d_emp=d("emp"), d_Y=d("Y"),
        d_welfare_pc=d("welfare_pc"),
        d_queue_loss=d("queue_loss"),
        d_w_y=d("w_y"),
        # the lump-of-labour test
        crowding_out=float((end["e_q"] + end["e_m"] - base["e_q"] - base["e_m"])
                           / (end["E_q"] + end["E_m"] - base["E_q"]
                              - base["E_m"])),
        d_young_emp=d("e_q") if False else float(
            (end["e_q"] + end["e_m"]) / (base["e_q"] + base["e_m"]) - 1.0),
        d_prime_emp=float((end["E_q"] + end["E_m"])
                          / (base["E_q"] + base["E_m"]) - 1.0),
        d_young_quota_emp=d("e_q"))
    return df, end


# =====================================================================  3
def channels(base):
    """Shapley decomposition over the three routes the retirement hazard takes."""
    names = ("quota", "value", "demo")
    _, rho0 = Q.rates(P0)

    def run(active):
        p = pset(R=R1)
        for nm in names:
            if nm not in active:
                p["_rho_" + nm] = rho0          # hold this route at its old value
        return eq(p)

    outcomes = ("cohort_entry_Q", "u_rate_y", "queue_years", "V_entrant",
                "quota_share")
    v = {}
    for k in range(len(names) + 1):
        for combo in itertools.combinations(names, k):
            r = run(set(combo))
            v[frozenset(combo)] = {o: math.log(r[o] / base[o]) for o in outcomes}

    full = frozenset(names)
    rows = []
    for o in outcomes:
        shap = {}
        for i in names:
            tot = 0.0
            for k in range(len(full - {i}) + 1):
                for combo in itertools.combinations(full - {i}, k):
                    Ss = frozenset(combo)
                    w = (math.factorial(len(Ss)) *
                         math.factorial(len(full) - len(Ss) - 1) /
                         math.factorial(len(full)))
                    tot += w * (v[Ss | {i}][o] - v[Ss][o])
            shap[i] = float(tot)
        total = v[full][o]
        rows.append(dict(outcome=o, total=total, **shap,
                         check=float(sum(shap.values()) - total)))
    dump("channels.csv", pd.DataFrame(rows))
    S["channels"] = {r["outcome"]: r for r in rows}
    return rows


# =====================================================================  4
def indicator_wedge(path):
    """How far the headline indicator moves relative to what it should track."""
    d = path.copy()
    for c in ("u_rate_y", "cohort_entry_Q", "queue_years", "V_entrant"):
        d["i_" + c] = 100.0 * d[c] / d[c].iloc[0]
    dump("indicator.csv", d[["year", "R", "i_u_rate_y", "i_cohort_entry_Q",
                             "i_queue_years", "i_V_entrant", "u_rate_y",
                             "cohort_entry_Q"]])
    S["indicator"] = dict(
        u_rate_y_range_pp=float(100 * (d["u_rate_y"].max() -
                                       d["u_rate_y"].min())),
        entry_prob_range_pct=float(100 * (d["cohort_entry_Q"].iloc[0] /
                                          d["cohort_entry_Q"].iloc[-1] - 1)),
        ratio=float(abs(100 * (d["cohort_entry_Q"].iloc[-1] /
                               d["cohort_entry_Q"].iloc[0] - 1))
                    / max(abs(100 * (d["u_rate_y"].iloc[-1] /
                                     d["u_rate_y"].iloc[0] - 1)), 1e-9)))
    return d


# =====================================================================  5
INSTR = [("s_N", "Establishment expansion"),
         ("s_v", "Market vacancy subsidy"),
         ("tau_q", "Cut in the administered premium")]


def _rate_for_budget(p_base, key, G):
    sign = -1.0 if key == "tau_q" else 1.0
    hi = 2.0 if key != "tau_q" else 0.60

    def cost(x):
        q = dict(p_base)
        q[key] = float(x)
        return sign * eq(q)["fiscal"] - G

    lo_v = lo_c = None
    for x in np.concatenate([[1e-9], np.geomspace(1e-6, hi, 70)]):
        try:
            c = cost(x)
        except Exception:
            break
        if not np.isfinite(c):
            break
        if lo_c is not None and lo_c * c < 0:
            return brentq(cost, lo_v, x, xtol=1e-13, rtol=1e-15)
        lo_v, lo_c = x, c
    raise ValueError("no bracket for %s" % key)


def budget_experiment(p_base, tag, budget_frac=BUDGET):
    base = eq(p_base)
    G = budget_frac * base["Y"]
    rows = []
    for key, label in INSTR:
        sign = -1.0 if key == "tau_q" else 1.0
        try:
            val = _rate_for_budget(p_base, key, G)
        except ValueError:
            rows.append(dict(instrument=label, key=key, rate=np.nan))
            continue
        q = dict(p_base)
        q[key] = float(val)
        r = eq(q)
        dW = r["welfare_pc"] - base["welfare_pc"]
        rows.append(dict(
            instrument=label, key=key, rate=float(val),
            fiscal_pct_Y=float(100 * sign * r["fiscal"] / base["Y"]),
            d_welfare_pc_pct=float(100 * dW / base["welfare_pc"]),
            d_entry_prob_pct=float(100 * (r["cohort_entry_Q"] /
                                          base["cohort_entry_Q"] - 1)),
            d_u_rate_y_pp=float(100 * (r["u_rate_y"] - base["u_rate_y"])),
            d_queue_years=float(r["queue_years"] - base["queue_years"]),
            d_queue_loss_pct=float(100 * (r["queue_loss"] /
                                          base["queue_loss"] - 1)),
            d_V_entrant_pct=float(100 * (r["V_entrant"] /
                                         base["V_entrant"] - 1)),
            mvpf=float(1.0 + (r["welfare"] - base["welfare"]) /
                       (sign * r["fiscal"]))))
    df = pd.DataFrame(rows).sort_values("d_welfare_pc_pct", ascending=False)
    dump("policy_%s.csv" % tag, df)
    S["policy_" + tag] = df.to_dict("records")
    return df


def indexation(base):
    """Expand the establishment in step with the labour force and see what it costs."""
    end = eq(pset(R=R1))
    growth = end["L"] / base["L"] - 1.0
    idx = eq(pset(R=R1, s_N=float(growth)))
    S["indexation"] = dict(
        labour_force_growth_pct=float(100 * growth),
        s_N=float(growth),
        entry_prob_no_index=float(end["cohort_entry_Q"]),
        entry_prob_indexed=float(idx["cohort_entry_Q"]),
        entry_prob_baseline=float(base["cohort_entry_Q"]),
        restored_pct=float(100 * (idx["cohort_entry_Q"] -
                                  end["cohort_entry_Q"]) /
                           max(base["cohort_entry_Q"] -
                               end["cohort_entry_Q"], 1e-12)),
        fiscal_pct_Y=float(100 * idx["fiscal"] / idx["Y"]),
        d_welfare_pc_pct=float(100 * (idx["welfare_pc"] /
                                      end["welfare_pc"] - 1)),
        d_queue_loss_pct=float(100 * (idx["queue_loss"] /
                                      end["queue_loss"] - 1)),
        d_u_rate_y_pp=float(100 * (idx["u_rate_y"] - end["u_rate_y"])))
    return idx


# =====================================================================  6
def sensitivity(base):
    rows = []
    for qs in (0.08, 0.10, 0.12, 0.15, 0.20):
        try:
            p = recalibrate_to({"quota_share": qs})
            if p is None:
                continue
            b = eq(p)
            e = eq(dict(p, R=R1))
        except Exception:
            continue
        rows.append(dict(quota_share=qs,
                         entry_prob=b["cohort_entry_Q"],
                         d_entry_prob=e["cohort_entry_Q"] /
                         b["cohort_entry_Q"] - 1,
                         d_u_rate_y_pp=100 * (e["u_rate_y"] - b["u_rate_y"]),
                         queue_loss_pct_Y=100 * b["queue_loss"] / b["Y"],
                         d_V_entrant=e["V_entrant"] / b["V_entrant"] - 1))
    dump("sensitivity_quota.csv", pd.DataFrame(rows))
    S["sensitivity_quota"] = rows

    rows2 = []
    for prem in (1.10, 1.20, 1.25, 1.35, 1.50):
        try:
            p = recalibrate_to({"wage_premium": prem})
            if p is None:
                continue
            b = eq(p)
            e = eq(dict(p, R=R1))
        except Exception:
            continue
        rows2.append(dict(wage_premium=prem,
                          queue_years=b["queue_years"],
                          queue_loss_pct_Y=100 * b["queue_loss"] / b["Y"],
                          d_entry_prob=e["cohort_entry_Q"] /
                          b["cohort_entry_Q"] - 1,
                          d_u_rate_y_pp=100 * (e["u_rate_y"] - b["u_rate_y"])))
    dump("sensitivity_premium.csv", pd.DataFrame(rows2))
    S["sensitivity_premium"] = rows2


def recalibrate_to(overrides, p_ext=None, start=None):
    """Re-estimate the six parameters with one or more targets replaced."""
    tgt = dict(MOM)
    tgt.update(overrides)
    keys = FREE_KEYS
    base_p = dict(P0 if p_ext is None else p_ext)

    def res(vec):
        p = dict(base_p)
        p.update({k: float(x) for k, x in zip(keys, vec)})
        try:
            r, ok = Q.solve(p)
            if not ok or r is None or r["u_q"] <= 0 or r["u_m"] <= 0:
                return np.full(len(keys), 5.0)
            out = np.array([math.log(max(r[k], 1e-12) / t)
                            for k, t in tgt.items()])
            return out if np.isfinite(out).all() else np.full(len(keys), 5.0)
        except Exception:
            return np.full(len(keys), 5.0)

    x0 = np.array([P0[k] for k in keys]) if start is None else start
    sol = least_squares(res, np.clip(x0, LO, HI), bounds=(LO, HI), method="trf",
                        xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=2000)
    if float(np.max(np.abs(res(sol.x)))) > 1e-6:
        return None
    p = dict(base_p)
    p.update({k: float(x) for k, x in zip(keys, sol.x)})
    return p


# =====================================================================  7
EXT = [("r", 0.030, 0.055), ("T_y", 5.0, 9.0), ("delta_Q", 0.010, 0.035),
       ("delta_M", 0.130, 0.240), ("eta", 0.400, 0.600), ("a0", 21.0, 24.5)]


def _draw(args):
    i, vals = args
    p = dict(P0)
    for (k, _, _), v in zip(EXT, vals):
        p[k] = float(v)
    p["beta"] = p["eta"]
    try:
        q = recalibrate_to({}, p_ext=p)
        if q is None:
            return None
        b = eq(q)
        e = eq(dict(q, R=R1))
        G = BUDGET * b["Y"]
        out = {}
        for key, _ in INSTR:
            sign = -1.0 if key == "tau_q" else 1.0
            try:
                z = dict(q)
                z[key] = float(_rate_for_budget(q, key, G))
                r = eq(z)
                out["gain_" + key] = float(100 * (r["welfare_pc"] /
                                                  b["welfare_pc"] - 1))
            except Exception:
                out["gain_" + key] = np.nan
        return dict(i=i, **{k: float(p[k]) for k, _, _ in EXT},
                    entry_prob=float(b["cohort_entry_Q"]),
                    d_entry_prob=float(e["cohort_entry_Q"] /
                                       b["cohort_entry_Q"] - 1),
                    d_u_rate_y_pp=float(100 * (e["u_rate_y"] - b["u_rate_y"])),
                    queue_loss_pct_Y=float(100 * b["queue_loss"] / b["Y"]),
                    d_V_entrant=float(e["V_entrant"] / b["V_entrant"] - 1),
                    **out)
    except Exception:
        return None


def uncertainty(n=192, seed=20260728):
    lo = np.array([a for _, a, _ in EXT])
    hi = np.array([b for _, _, b in EXT])
    draws = lo + qmc.LatinHypercube(d=len(EXT), seed=seed).random(n) * (hi - lo)
    with ProcessPoolExecutor() as ex:
        got = list(ex.map(_draw, [(i, draws[i]) for i in range(n)], chunksize=2))
    df = dump("uncertainty.csv", pd.DataFrame([g for g in got if g is not None]))
    cols = [c for c in df.columns if c.startswith("gain_")]
    ok = df.dropna(subset=cols, how="all")
    best = ok[cols].idxmax(axis=1, skipna=True) if len(ok) else pd.Series([])
    S["uncertainty"] = dict(
        n_requested=n, n_solved=int(len(df)), n_ranked=int(len(ok)),
        d_entry_prob_mean=float(df["d_entry_prob"].mean()),
        d_entry_prob_p5=float(df["d_entry_prob"].quantile(0.05)),
        d_entry_prob_p95=float(df["d_entry_prob"].quantile(0.95)),
        d_entry_prob_negative_share=float((df["d_entry_prob"] < 0).mean()),
        d_u_rate_y_pp_mean=float(df["d_u_rate_y_pp"].mean()),
        d_u_rate_y_pp_p5=float(df["d_u_rate_y_pp"].quantile(0.05)),
        d_u_rate_y_pp_p95=float(df["d_u_rate_y_pp"].quantile(0.95)),
        d_u_rate_y_small_share=float((df["d_u_rate_y_pp"].abs() < 0.5).mean()),
        queue_loss_mean=float(df["queue_loss_pct_Y"].mean()),
        queue_loss_p5=float(df["queue_loss_pct_Y"].quantile(0.05)),
        queue_loss_p95=float(df["queue_loss_pct_Y"].quantile(0.95)),
        instrument_feasible_share={c: float(df[c].notna().mean())
                                   for c in cols},
        best_instrument_shares={c: float((best == c).mean()) for c in cols}
        if len(ok) else {})
    return df


# =====================================================================  main
def main():
    print("1. baseline and the cost of the queue", flush=True)
    base = section_baseline()
    print("   queue %.2f of a cohort; forgone output %.2f%% of GDP"
          % (base["u_q"], 100 * base["queue_loss"] / base["Y"]))

    print("2. the phased reform", flush=True)
    path, end = reform_path(base)
    print("   entry probability %+.2f%%, youth unemployment %+.2f pp"
          % (100 * S["reform"]["d_entry_prob"], S["reform"]["u_rate_y_pp"]))

    print("3. channel decomposition", flush=True)
    channels(base)

    print("4. the indicator wedge", flush=True)
    indicator_wedge(path)

    print("5. equal-budget policy comparison", flush=True)
    budget_experiment(P0, "baseline")
    budget_experiment(pset(R=R1), "post_reform")
    indexation(base)

    print("6. sensitivity", flush=True)
    sensitivity(base)

    print("7. parameter uncertainty", flush=True)
    uncertainty()

    S["meta"] = dict(max_log_resid=CAL["max_log_resid"], moments=CAL["moments"],
                     params=CAL["params"], checks=CAL["checks"],
                     R0=R0, R1=R1, phase=PHASE, cohort=COHORT, budget=BUDGET)
    json.dump(S, open(os.path.join(HERE, "stats.json"), "w"), indent=1)
    print("written stats.json")


if __name__ == "__main__":
    main()
