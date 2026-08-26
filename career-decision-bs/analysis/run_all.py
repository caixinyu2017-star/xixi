# -*- coding: utf-8 -*-
"""Run the study and write every number the manuscript uses.

Outputs land in ../tables as one TSV per manuscript table, plus summary.json,
which the manuscript build reads. Nothing in the paper is typed by hand.
"""
from __future__ import annotations

import itertools
import json
import os
import time

import numpy as np

import calibrate as CAL
import estimators as E
import model as M
import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
os.makedirs(TAB, exist_ok=True)

SEED = 20260826
N_STUDY = 407            # the sample size of the study being reproduced
N_LARGE = 8000
BOOTS = 5000


def log(*a):
    print(*a, flush=True)


def write_tsv(name, header, rows):
    with open(os.path.join(TAB, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    log("   wrote %s (%d rows)" % (name, len(rows)))


def virtual_study(vals, pi, n=N_STUDY, seed=41, boots=BOOTS):
    """Run one cross-sectional study on a simulated cohort."""
    v = dict(vals); v["substitution_share"] = pi
    with P.override(v):
        st = M.simulate(n=n, seed=seed)
        ob = M.observe(st, seed=seed + 1)
    est = E.standardised(ob["CA"], ob["CDSE"], ob["CDD"], ob["PCS"],
                         boots=boots, seed=seed + 2)
    est["_state"] = st
    est["_obs"] = ob
    return est


def main():
    t0 = time.time()
    S = {}
    vals = json.load(open(os.path.join(HERE, "calibrated.json")))
    S["calibrated"] = vals

    # ------------------------------------------------------- calibration
    log("checking the calibration ...")
    rmse, rows = CAL.report(vals)
    S["calibration"] = {"rmse": rmse,
                        "pairs": [{"pair": a, "target": b, "model": c,
                                   "diff": d} for a, b, c, d in rows]}
    write_tsv("t01_calibration.tsv",
              ["pair", "reported", "simulated", "difference"],
              [[a, "%.3f" % b, "%.3f" % c, "%+.3f" % d] for a, b, c, d in rows])
    log("   RMSE %.4f across the six reported correlations" % rmse)

    # ------------------------------------------------- baseline dynamics
    log("baseline dynamics ...")
    with P.override(vals):
        st = M.simulate(n=N_LARGE, seed=SEED, record=True)
    tr = st["traj"]
    weeks = tr["u"].shape[0]
    q = lambda arr, p: float(np.percentile(arr, p))
    S["dynamics"] = {
        "weeks": weeks - 1,
        "u_start": float(tr["u"][0].mean()), "u_end": float(tr["u"][-1].mean()),
        "s_start": float(tr["s"][0].mean()), "s_end": float(tr["s"][-1].mean()),
        "a_start": float(tr["a"][0].mean()), "a_end": float(tr["a"][-1].mean()),
        "u_end_p10": q(tr["u"][-1], 10), "u_end_p90": q(tr["u"][-1], 90),
        "explore_mean": float(st["explore"].mean()),
    }
    step = max(1, (weeks - 1) // 6)
    write_tsv("t02_dynamics.tsv",
              ["week", "uncertainty", "self_efficacy", "anxiety", "exploration"],
              [[w, "%.3f" % tr["u"][w].mean(), "%.3f" % tr["s"][w].mean(),
                "%.3f" % tr["a"][w].mean(), "%.3f" % tr["e"][w].mean()]
               for w in range(0, weeks, step)])
    np.save(os.path.join(TAB, "traj_mean.npy"),
            np.vstack([tr[k].mean(axis=1) for k in ("u", "s", "a", "e")]))

    # quartiles of dispositional anxiety, to show the divergence of paths
    ta = st["trait_a"]
    lo, hi = ta <= np.percentile(ta, 25), ta >= np.percentile(ta, 75)
    np.save(os.path.join(TAB, "traj_by_trait.npy"),
            np.vstack([tr["u"][:, lo].mean(axis=1), tr["u"][:, hi].mean(axis=1),
                       tr["s"][:, lo].mean(axis=1), tr["s"][:, hi].mean(axis=1)]))
    S["dynamics"]["u_end_low_trait"] = float(tr["u"][-1, lo].mean())
    S["dynamics"]["u_end_high_trait"] = float(tr["u"][-1, hi].mean())
    S["dynamics"]["s_end_low_trait"] = float(tr["s"][-1, lo].mean())
    S["dynamics"]["s_end_high_trait"] = float(tr["s"][-1, hi].mean())
    log("   uncertainty %.3f -> %.3f; low-anxiety quartile ends at %.3f, high at %.3f"
        % (S["dynamics"]["u_start"], S["dynamics"]["u_end"],
           S["dynamics"]["u_end_low_trait"], S["dynamics"]["u_end_high_trait"]))

    # --------------------------------------- the reproduced conditional model
    log("the reproduced conditional process model ...")
    ref = virtual_study(vals, P.v("substitution_share"))
    S["reference_study"] = {k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                            for k, v in ref.items()
                            if not k.startswith("_") and k not in ("se", "t")}
    write_tsv("t03_conditional.tsv",
              ["quantity", "estimate", "ci_low", "ci_high"],
              [["a (anxiety on self-efficacy)", "%.3f" % ref["a"], "", ""],
               ["b (self-efficacy on difficulty)", "%.3f" % ref["b"], "", ""],
               ["c' (direct, at mean support)", "%.3f" % ref["cdash"], "", ""],
               ["Indirect effect (a x b)", "%.3f" % ref["indirect"],
                "%.3f" % ref["indirect_ci"][0], "%.3f" % ref["indirect_ci"][1]],
               ["Anxiety x support interaction", "%.3f" % ref["inter"],
                "%.3f" % ref["inter_ci"][0], "%.3f" % ref["inter_ci"][1]],
               ["Simple slope at low support (-1 SD)", "%.3f" % ref["slope_lo"], "", ""],
               ["Simple slope at high support (+1 SD)", "%.3f" % ref["slope_hi"], "", ""]])
    log("   interaction %.3f, 95%% CI [%.3f, %.3f]"
        % (ref["inter"], ref["inter_ci"][0], ref["inter_ci"][1]))

    # ------------------------------------- the moderation across the regime
    log("the moderation across the directive share ...")
    shares = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    rows, mod = [], {}
    for pi in shares:
        e = virtual_study(vals, pi, n=N_LARGE, boots=800)
        mod[pi] = {"inter": e["inter"], "ci": e["inter_ci"],
                   "lo": e["slope_lo"], "hi": e["slope_hi"],
                   "cdash": e["cdash"], "indirect": e["indirect"]}
        rows.append([("%.1f" % pi), "%.3f" % e["cdash"], "%.3f" % e["indirect"],
                     "%.3f" % e["inter"],
                     "[%.3f, %.3f]" % e["inter_ci"],
                     "%.3f" % e["slope_lo"], "%.3f" % e["slope_hi"]])
    S["moderation"] = {str(k): v for k, v in mod.items()}
    write_tsv("t04_moderation.tsv",
              ["directive_share", "direct", "indirect", "interaction",
               "interaction_ci", "slope_low_support", "slope_high_support"],
              rows)
    log("   interaction runs %.3f -> %.3f as the directive share goes 0 to 1"
        % (mod[0.0]["inter"], mod[1.0]["inter"]))

    # ------------------------------- what has to be true for amplification
    log("the conditions for amplification ...")
    grid = {
        "substitution_share": [0.2, 0.5, 0.85],
        "conflict_weight": [0.25, 0.6, 1.0],
        "divergence_mean": [0.2, 0.5, 0.8],
        "substitute_yield": [0.15, 0.5, 0.9],
        "assertion_anxiety": [0.3, 0.8, 1.3],
    }
    keys = list(grid)
    recs = []
    for combo in itertools.product(*[grid[k] for k in keys]):
        v = dict(vals); v.update(dict(zip(keys, combo)))
        with P.override(v):
            stx = M.simulate(n=2500, seed=71)
            obx = M.observe(stx, seed=72)
        e = E.standardised(obx["CA"], obx["CDSE"], obx["CDD"], obx["PCS"],
                           boots=1, seed=73)
        rec = dict(zip(keys, combo)); rec["inter"] = float(e["inter"])
        recs.append(rec)
    amp = [r for r in recs if r["inter"] > 0]
    S["conditions"] = {"n_cells": len(recs), "n_amplifying": len(amp),
                       "share_amplifying": len(amp) / len(recs)}
    log("   amplification in %d of %d parameter combinations (%.1f%%)"
        % (len(amp), len(recs), 100 * len(amp) / len(recs)))

    def marginal(key):
        out = []
        for lvl in grid[key]:
            sub = [r for r in recs if r[key] == lvl]
            out.append((lvl, float(np.mean([r["inter"] for r in sub])),
                        float(np.mean([r["inter"] > 0 for r in sub]))))
        return out

    crows = []
    pretty = {"substitution_share": "Directive share of involvement",
              "conflict_weight": "Weight of conflict in the difficulty score",
              "divergence_mean": "Distance between preferred and endorsed option",
              "substitute_yield": "Uncertainty actually resolved by involvement",
              "assertion_anxiety": "Loss of standing per unit of anxiety"}
    S["conditions"]["marginal"] = {}
    for k in keys:
        m = marginal(k)
        S["conditions"]["marginal"][k] = m
        for lvl, mi, sh in m:
            crows.append([pretty[k], "%.2f" % lvl, "%+.3f" % mi, "%.1f" % (100 * sh)])
    write_tsv("t05_conditions.tsv",
              ["condition", "level", "mean_interaction", "percent_amplifying"],
              crows)

    # ------------------------ who can actually use autonomy-supportive help
    log("who benefits from scaffolding ...")
    v = dict(vals); v["substitution_share"] = 0.0
    with P.override(v):
        sc = M.simulate(n=20000, seed=41)
    ta, sup, dd = sc["trait_a"], sc["support"], sc["difficulty"]
    loa, hia = ta <= np.percentile(ta, 25), ta >= np.percentile(ta, 75)
    los, his = sup <= np.percentile(sup, 25), sup >= np.percentile(sup, 75)
    brows, ben = [], {}
    for lab, m in (("Low anxiety (lowest quartile)", loa),
                   ("High anxiety (highest quartile)", hia)):
        b, g = float(dd[m & los].mean()), float(dd[m & his].mean())
        ben[lab] = b - g
        brows.append([lab, "%.3f" % b, "%.3f" % g, "%+.3f" % (b - g)])
    S["scaffold_benefit"] = ben
    write_tsv("t08_scaffold.tsv",
              ["group", "difficulty_low_support", "difficulty_high_support",
               "benefit"], brows)
    log("   scaffolding reduces difficulty by %.3f for the composed and %.3f for the anxious"
        % tuple(ben.values()))

    # ------------------------------------------- precision of the interaction
    log("sampling distribution of the interaction ...")
    prows = []
    for n in (200, N_STUDY, 800, 2000):
        ests, sig = [], 0
        for rep in range(300):
            with P.override(vals):
                sx = M.simulate(n=n, seed=1000 + rep)
                ox = M.observe(sx, seed=5000 + rep)
            e = E.standardised(ox["CA"], ox["CDSE"], ox["CDD"], ox["PCS"],
                               boots=1, seed=1)
            ests.append(e["inter"])
            if abs(e["t"][4]) > 1.96:
                sig += 1
        a = np.array(ests)
        prows.append([n, "%.3f" % a.mean(), "%.3f" % a.std(ddof=1),
                      "%.3f" % np.percentile(a, 2.5),
                      "%.3f" % np.percentile(a, 97.5),
                      "%.1f" % (100 * sig / len(a))])
        if n == N_STUDY:
            S["precision"] = {"n": n, "mean": float(a.mean()),
                              "sd": float(a.std(ddof=1)),
                              "p025": float(np.percentile(a, 2.5)),
                              "p975": float(np.percentile(a, 97.5)),
                              "pct_significant": 100 * sig / len(a)}
    write_tsv("t07_precision.tsv",
              ["n", "mean_interaction", "sd", "p2.5", "p97.5",
               "percent_detected"], prows)
    log("   at n = %d the interaction is %.3f (SD %.3f), detected in %.1f%% of studies"
        % (S["precision"]["n"], S["precision"]["mean"], S["precision"]["sd"],
           S["precision"]["pct_significant"]))

    # ------------------------------------------------- what is identified
    log("what the correlation matrix identifies ...")
    idr = []
    for pi, l, c in CAL.identification_check(vals, shares=tuple(shares), n=N_LARGE):
        e = virtual_study(vals, pi, n=N_LARGE, boots=1)
        idr.append([("%.1f" % pi), "%.3f" % l,
                    "%+.3f" % c[("CA", "CDD")], "%+.3f" % c[("CDSE", "PCS")],
                    "%+.3f" % e["inter"]])
    S["identification"] = idr
    write_tsv("t06_identification.tsv",
              ["directive_share", "rmse_vs_reported", "r_anxiety_difficulty",
               "r_efficacy_support", "interaction"], idr)
    ca = [float(r[2]) for r in idr]
    S["identification_range"] = {"r_ca_cdd_min": min(ca), "r_ca_cdd_max": max(ca),
                                 "r_ca_cdd_spread": max(ca) - min(ca)}
    log("   the anxiety-difficulty correlation moves only %.3f across the whole range"
        % S["identification_range"]["r_ca_cdd_spread"])

    # ------------------------------------------------------- parameters
    write_tsv("t0A_params.tsv",
              ["parameter", "value", "unit", "low", "high", "provenance"],
              [[p.name.replace("_", " "), "%g" % (vals.get(p.name, p.value)),
                p.unit, "%g" % p.low, "%g" % p.high, p.provenance]
               for p in P.table()])
    S["params"] = {"n": len(P.table()), "counts": P.counts(),
                   "n_calibrated": len(CAL.FREE)}

    S["meta"] = {"seed": SEED, "n_study": N_STUDY, "n_large": N_LARGE,
                 "boots": BOOTS, "runtime_s": round(time.time() - t0, 1)}
    with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(S, fh, indent=1, default=float)
    log("done in %.1f s" % S["meta"]["runtime_s"])


if __name__ == "__main__":
    main()
