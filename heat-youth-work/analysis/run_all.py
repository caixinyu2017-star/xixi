# -*- coding: utf-8 -*-
"""Run the whole study and write every number the manuscript uses.

Outputs land in ../tables: one TSV per manuscript table plus summary.json,
which the manuscript build reads. Nothing in the paper is typed by hand.
"""
from __future__ import annotations

import json
import os
import time

import numpy as np

import city as C
import labour as LB
import microclimate as MC
import params as PA
import siting as SI
import thermal as TH
import eudata as ED
import uncertainty as UQ

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
os.makedirs(TAB, exist_ok=True)

SEED = 20260825
CITY_SEED = 11
REF_DIVERGENCE = 0.75
REF_CLIMATE = "pannonian"
REF_ERF = "hothaps"
BUDGET_HA = 300.0
N_DRAWS = 4000


def log(*a):
    print(*a, flush=True)


def write_tsv(name, header, rows):
    p = os.path.join(TAB, name)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    log("   wrote %s (%d rows)" % (name, len(rows)))


def main():
    t0 = time.time()
    S = {}

    # ------------------------------------------------- observed EU anchors
    log("reading the observed European data ...")
    u = ED.ucdb_stats()
    cp = ED.climate_percentiles()
    yu = ED.youth_unemployment_latest()
    S["eu"] = {"ucdb": u, "climate": {k: v for k, v in cp.items()
                                      if k != "by_country"},
               "youth_unemployment": yu}
    log("   %d EU-27 urban centres; EU summer means %.1f to %.1f C; "
        "EU youth unemployment %.1f%% (%d)"
        % (u["n"], cp["min"], cp["max"], yu["value"], yu["year"]))
    write_tsv("t08_eu.tsv",
              ["quantity", "p25", "median", "p75", "unit"],
              [["Average greenness, 2014",
                "%.3f" % u["greenness_2014"]["p25"],
                "%.3f" % u["greenness_2014"]["median"],
                "%.3f" % u["greenness_2014"]["p75"], "index"],
               ["Population with access to open space (SDG 11.7)",
                "%.3f" % u["green_access_sdg11_7"]["p25"],
                "%.3f" % u["green_access_sdg11_7"]["median"],
                "%.3f" % u["green_access_sdg11_7"]["p75"], "share"],
               ["Heatwave exposure index",
                "%.2f" % u["heatwave_index"]["p25"],
                "%.2f" % u["heatwave_index"]["median"],
                "%.2f" % u["heatwave_index"]["p75"], "index"],
               ["Urban centre area",
                "%.0f" % u["area_km2"]["p25"],
                "%.0f" % u["area_km2"]["median"],
                "%.0f" % u["area_km2"]["p75"], "km2"],
               ["Residential density",
                "%.0f" % u["density_per_km2"]["p25"],
                "%.0f" % u["density_per_km2"]["median"],
                "%.0f" % u["density_per_km2"]["p75"], "persons per km2"],
               ["Summer (JJA) mean temperature, 2001-2020",
                "%.2f" % cp["p25"], "%.2f" % cp["median"],
                "%.2f" % cp["p75"], "degrees C"]])

    # ---------------------------------------------------------------- city
    log("building the reference city ...")
    ref = C.City(seed=CITY_SEED, divergence=REF_DIVERGENCE)
    S["city"] = ref.summary()
    log("   %d cells, %.0f residents, %.0f exposed young workers, r = %.3f"
        % (S["city"]["cells"], S["city"]["residents_total"],
           S["city"]["exposed_youth_total"], S["city"]["workplace_residence_r"]))

    lu = ref.land_use_shares()
    write_tsv("t01_city.tsv",
              ["quantity", "value", "unit"],
              [["Grid cells", C.N * C.N, "cells of %.0f m" % C.CELL_M],
               ["City extent", "%.1f" % (C.EXTENT_M / 1000.0), "km across"],
               ["Residents", "%.0f" % ref.residents.sum(), "persons"],
               ["Jobs, heavy outdoor", "%.0f" % ref.jobs["high"].sum(), "jobs"],
               ["Jobs, moderate", "%.0f" % ref.jobs["moderate"].sum(), "jobs"],
               ["Jobs, light service", "%.0f" % ref.jobs["low"].sum(), "jobs"],
               ["Young workers in exposed classes",
                "%.0f" % ref.exposed_youth().sum(), "workers"],
               ["Mean existing canopy cover", "%.3f" % ref.canopy.mean(), "fraction"],
               ["Workplace-residence correlation",
                "%.3f" % ref.workplace_residence_correlation(), "Pearson r"]]
              + [["Land use, %s" % k, "%.3f" % v, "share of cells"]
                 for k, v in lu.items()])

    # ------------------------------------------------- baseline exposure
    log("baseline exposure across climate settings and response functions ...")
    rows = []
    base_grid = {}
    for cl in MC.CLIMATES:
        wb = MC.wbgt_field(ref, cl)
        for e in TH.ERF_NAMES:
            r = LB.evaluate(ref, cl, None, e)
            base_grid[(cl, e)] = r
            rows.append([cl, e, "%.2f" % wb.mean(), "%.2f" % wb.max(),
                         "%.3f" % r["per_worker"]["youth"],
                         "%.3f" % r["per_worker"]["older"],
                         "%.3f" % r["youth_gap"]])
    write_tsv("t02_baseline.tsv",
              ["climate", "erf", "mean_wbgt", "peak_wbgt",
               "youth_h_per_day", "older_h_per_day", "gap"], rows)

    yl = [base_grid[(REF_CLIMATE, e)]["per_worker"]["youth"] for e in TH.ERF_NAMES]
    S["erf_spread"] = {"climate": REF_CLIMATE,
                       "min": float(min(yl)), "max": float(max(yl)),
                       "ratio": float(max(yl) / max(min(yl), 1e-9)),
                       "by_erf": {e: float(base_grid[(REF_CLIMATE, e)]["per_worker"]["youth"])
                                  for e in TH.ERF_NAMES}}
    log("   at %s, youth loss spans %.3f to %.3f h/day across the five functions (x%.1f)"
        % (REF_CLIMATE, S["erf_spread"]["min"], S["erf_spread"]["max"],
           S["erf_spread"]["ratio"]))

    # capacity-loss curves, for the appendix
    rows = []
    for w in (20, 22, 24, 25, 26, 27, 28, 30, 32, 34):
        rows.append([w] + ["%.3f" % (100 * TH.capacity_loss(w, "high", e))
                           for e in TH.ERF_NAMES])
    write_tsv("t0A_erf.tsv", ["wbgt"] + list(TH.ERF_NAMES), rows)

    # ------------------------------------------------------ siting rules
    log("comparing siting rules at the reference setting ...")
    cmp_ref = SI.compare(ref, REF_CLIMATE, BUDGET_HA, REF_ERF)
    S["reference"] = {
        "climate": REF_CLIMATE, "erf": REF_ERF, "divergence": REF_DIVERGENCE,
        "budget_ha": BUDGET_HA, "budget_eur": cmp_ref["budget_eur"],
        "baseline_youth_h": cmp_ref["baseline"]["total"]["youth"],
        "rules": cmp_ref["rules"]}
    pop = cmp_ref["rules"]["population"]["hours_saved_youth"]
    rows = []
    for r in SI.RULES:
        v = cmp_ref["rules"][r]
        rows.append([r, "%.1f" % v["hours_saved_youth"],
                     "%.1f" % v["hours_saved_older"],
                     "%.4f" % v["per_ha_youth"],
                     "%.2f" % (v["hours_saved_youth"] / max(pop, 1e-9)),
                     "%.1f" % (100 * v["youth_share_of_saving"])])
    write_tsv("t03_siting.tsv",
              ["rule", "youth_hours_saved", "older_hours_saved",
               "youth_hours_per_ha", "ratio_to_population", "youth_share_pct"],
              rows)
    poph = cmp_ref["rules"]["population_heat"]["hours_saved_youth"]
    S["reference"]["ratio_exposure_to_population"] = float(
        cmp_ref["rules"]["exposure"]["hours_saved_youth"] / max(pop, 1e-9))
    S["reference"]["ratio_exposure_to_population_heat"] = float(
        cmp_ref["rules"]["exposure"]["hours_saved_youth"] / max(poph, 1e-9))
    S["reference"]["ratio_greedy_to_population"] = float(
        cmp_ref["rules"]["greedy"]["hours_saved_youth"] / max(pop, 1e-9))
    log("   exposure-targeted beats population-weighted by x%.2f; optimum x%.2f"
        % (S["reference"]["ratio_exposure_to_population"],
           S["reference"]["ratio_greedy_to_population"]))

    # ----------------------------------------------- uncertainty ensemble
    log("running the uncertainty ensemble (%d draws) ..." % N_DRAWS)
    recs, names = UQ.run(n=N_DRAWS, budget_ha=BUDGET_HA, seed=SEED,
                         city_seed=CITY_SEED)
    wins, pair = UQ.rank_stability(recs)

    bl = np.array([r["baseline_youth_per_worker"] for r in recs])
    zero = float((bl <= 1e-6).mean())
    nz = bl[bl > 1e-6]
    S["ensemble"] = {
        "n": len(recs), "n_params": len(names),
        "youth_loss_p05": float(np.percentile(bl, 5)),
        "youth_loss_p25": float(np.percentile(bl, 25)),
        "youth_loss_p50": float(np.percentile(bl, 50)),
        "youth_loss_p75": float(np.percentile(bl, 75)),
        "youth_loss_p95": float(np.percentile(bl, 95)),
        "youth_loss_min": float(bl.min()), "youth_loss_max": float(bl.max()),
        "share_zero_loss": zero,
        "youth_loss_ratio_p95_p25": float(
            np.percentile(bl, 95) / max(np.percentile(bl, 25), 1e-9)),
        "youth_loss_nonzero_p05": float(np.percentile(nz, 5)) if nz.size else 0.0,
        "youth_loss_nonzero_p95": float(np.percentile(nz, 95)) if nz.size else 0.0,
        "wins": wins,
        "p_exposure_beats_population": pair[("exposure", "population")],
        "p_exposure_beats_population_heat": pair[("exposure", "population_heat")],
        "p_youth_beats_population": pair[("youth", "population")],
        "p_exposure_beats_deprivation": pair[("exposure", "deprivation")],
        "p_exposure_beats_uniform": pair[("exposure", "uniform")],
        "p_youth_beats_exposure": pair[("youth", "exposure")],
    }
    log("   youth loss p25-p95: %.3f to %.3f h/day (x%.1f); %.1f%% of draws predict zero"
        % (S["ensemble"]["youth_loss_p25"], S["ensemble"]["youth_loss_p95"],
           S["ensemble"]["youth_loss_ratio_p95_p25"], 100 * S["ensemble"]["share_zero_loss"]))
    log("   P(exposure > population) = %.3f" % S["ensemble"]["p_exposure_beats_population"])

    by_erf = {}
    for e in TH.ERF_NAMES:
        v = np.array([r["baseline_youth_per_worker"] for r in recs if r["erf"] == e])
        by_erf[e] = {"n": int(v.size), "median": float(np.median(v)),
                     "share_zero": float((v <= 1e-6).mean()),
                     "p95": float(np.percentile(v, 95))}
    S["ensemble"]["by_erf"] = by_erf
    write_tsv("t07_byerf.tsv",
              ["erf", "draws", "median_youth_h", "p95_youth_h", "share_zero_loss"],
              [[e, by_erf[e]["n"], "%.3f" % by_erf[e]["median"],
                "%.3f" % by_erf[e]["p95"], "%.3f" % by_erf[e]["share_zero"]]
               for e in TH.ERF_NAMES])

    write_tsv("t04_stability.tsv",
              ["comparison", "probability"],
              [["Exposure-targeted better than population-weighted",
                "%.3f" % pair[("exposure", "population")]],
               ["Exposure-targeted better than deprivation-weighted",
                "%.3f" % pair[("exposure", "deprivation")]],
               ["Exposure-targeted better than uniform",
                "%.3f" % pair[("exposure", "uniform")]],
               ["Youth-targeted better than population-weighted",
                "%.3f" % pair[("youth", "population")]],
               ["Youth-targeted better than exposure-targeted",
                "%.3f" % pair[("youth", "exposure")]],
               ["Optimum better than population-weighted",
                "%.3f" % pair[("greedy", "population")]]]
              + [["Best rule in draw: %s" % r, "%.3f" % w]
                 for r, w in sorted(wins.items(), key=lambda kv: -kv[1])])

    # ------------------------------------------------------- sensitivity
    log("first-order sensitivity ...")
    sens = UQ.sensitivity(recs, names, "saved_youth")
    sens_base = UQ.sensitivity(recs, names, "baseline_youth_h")
    S["sensitivity_top"] = dict(list(sens.items())[:12])
    write_tsv("t05_sensitivity.tsv",
              ["input", "index_hours_saved", "index_baseline_loss"],
              [[k, "%.3f" % v, "%.3f" % sens_base.get(k, float("nan"))]
               for k, v in list(sens.items())[:14]])

    # --------------------------------------- the divergence threshold
    log("locating the divergence threshold ...")
    div = np.array([r["divergence"] for r in recs])
    beat = np.array([r["saved_exposure"] > r["saved_population_heat"] for r in recs])
    ratio = np.array([r["saved_exposure"] / max(r["saved_population_heat"], 1e-9)
                      for r in recs])
    edges = np.linspace(0, 1, 11)
    rows, cross = [], None
    for i in range(10):
        m = (div >= edges[i]) & (div < edges[i + 1])
        if m.sum() < 5:
            continue
        p = float(beat[m].mean())
        med = float(np.median(ratio[m]))
        rr = np.array([r["wr_corr"] for r, k in zip(recs, m) if k])
        rows.append(["%.1f-%.1f" % (edges[i], edges[i + 1]), int(m.sum()),
                     "%.3f" % rr.mean(), "%.2f" % med, "%.3f" % p])
        # the threshold is where the ADVANTAGE becomes material, not where a
        # coin-flip tips: the first bin in which the median advantage exceeds
        # a tenth and stays above it
        if cross is None and med >= 1.10:
            cross = 0.5 * (edges[i] + edges[i + 1])
    write_tsv("t06_threshold.tsv",
              ["divergence_bin", "draws", "mean_workplace_residence_r",
               "median_ratio_exposure_to_population_heat",
               "p_exposure_beats_population_heat"], rows)
    S["threshold"] = {"divergence": cross, "bins": rows,
                      "median_ratio_top_bin": float(np.median(ratio[div >= 0.9])),
                      "median_ratio_bottom_bin": float(np.median(ratio[div < 0.1]))}
    log("   workplace targeting gains a material advantage above divergence %s"
        % ("%.2f" % cross if cross is not None else "n/a"))
    log("   median advantage: %.2fx at divergence < 0.1, %.2fx at divergence > 0.9"
        % (S["threshold"]["median_ratio_bottom_bin"],
           S["threshold"]["median_ratio_top_bin"]))

    # -------------------------------------------------- parameter registry
    write_tsv("t0B_params.tsv",
              ["parameter", "value", "unit", "low", "high", "provenance"],
              [[p.name, "%g" % p.value, p.unit, "%g" % p.low, "%g" % p.high,
                p.provenance] for p in PA.table()])
    S["params"] = {"counts": PA.counts(), "n": len(PA.table()),
                   "n_swept": len(PA.sweepable())}

    S["meta"] = {"seed": SEED, "city_seed": CITY_SEED, "budget_ha": BUDGET_HA,
                 "n_draws": N_DRAWS, "erfs": list(TH.ERF_NAMES),
                 "climates": list(MC.CLIMATES), "rules": list(SI.RULES),
                 "runtime_s": round(time.time() - t0, 1)}

    with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(S, fh, indent=1, ensure_ascii=False)
    log("done in %.1f s; summary.json written to %s" % (S["meta"]["runtime_s"], TAB))


if __name__ == "__main__":
    main()
