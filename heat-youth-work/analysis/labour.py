# -*- coding: utf-8 -*-
"""From the microclimate field to hours of work lost, by age.

Lost hours are accumulated cell by cell, hour by hour and workload class by
workload class:

    L = sum_c sum_h sum_w  J(c,w) * o(w) * [1 - PWC(WBGT(c,h), w)]

where J is the number of jobs of class w in cell c, o(w) the share of working
time that class spends outdoors or in unconditioned space, and PWC the physical
work capacity given by whichever published exposure-response function is in
force. The sum is taken separately over young and older workers, which is the
only thing the age split changes.

The result is expressed per summer working day. A season multiplier converts it
to an annual figure where the manuscript needs one.
"""
from __future__ import annotations

import numpy as np

import microclimate as MC
import params as PA
import thermal as TH

WORKLOADS = ("high", "moderate", "low")


def outdoor_shares():
    return {w: PA.v("outdoor_share_%s" % w) for w in WORKLOADS}


def lost_hours_field(city, wbgt, erf="hothaps", group="youth"):
    """Hours lost per cell per working day, for one age group."""
    jobs = city.youth_jobs if group == "youth" else city.older_jobs
    o = outdoor_shares()
    total = np.zeros(wbgt.shape[:2])
    for w in WORKLOADS:
        loss = TH.capacity_loss(wbgt, workload=w, erf=erf)   # (N, N, H)
        # each modelled hour stands for one hour of the working day
        hours = loss.sum(axis=2) * (PA.v("work_hours_per_day") / wbgt.shape[2])
        total += jobs[w] * o[w] * hours
    return total


def lost_hours(city, wbgt, erf="hothaps"):
    """Total hours lost per working day, by group."""
    return {g: float(lost_hours_field(city, wbgt, erf, g).sum())
            for g in ("youth", "older")}


def per_worker(city, totals):
    """Hours lost per worker per day, by group — the comparable measure."""
    ny = sum(float(city.youth_jobs[w].sum()) for w in WORKLOADS)
    no = sum(float(city.older_jobs[w].sum()) for w in WORKLOADS)
    return {"youth": totals["youth"] / max(ny, 1e-9),
            "older": totals["older"] / max(no, 1e-9)}


def evaluate(city, climate, canopy=None, erf="hothaps"):
    wbgt = MC.wbgt_field(city, climate, canopy)
    tot = lost_hours(city, wbgt, erf)
    pw = per_worker(city, tot)
    return {"total": tot, "per_worker": pw,
            "mean_wbgt": float(wbgt.mean()),
            "youth_gap": pw["youth"] - pw["older"]}


def _selftest():
    import city as C
    ok = True

    def chk(c, m):
        nonlocal ok
        if not c:
            print("FAIL:", m); ok = False

    ct = C.City(seed=5, divergence=0.75)

    base = evaluate(ct, "pannonian")
    chk(base["total"]["youth"] > 0, "young workers lose hours")
    chk(base["per_worker"]["youth"] > base["per_worker"]["older"],
        "young workers lose more per head than older workers (%.3f vs %.3f)"
        % (base["per_worker"]["youth"], base["per_worker"]["older"]))

    # more canopy must never increase lost hours
    more = evaluate(ct, "pannonian", np.clip(ct.canopy + 0.2, 0, 0.95))
    chk(more["total"]["youth"] <= base["total"]["youth"],
        "canopy reduces youth lost hours")

    # a hotter climate must cost more hours
    hot = evaluate(ct, "mediterranean")
    cool = evaluate(ct, "maritime")
    chk(hot["total"]["youth"] > cool["total"]["youth"], "hotter climate costs more")

    print("labour.py self-test:", "PASSED" if ok else "FAILED")
    print("  hours lost per worker per working day, %s corpus" % "pannonian")
    for e in TH.ERF_NAMES:
        r = evaluate(ct, "pannonian", erf=e)
        print("    %-8s youth %6.3f  older %6.3f  gap %+.3f"
              % (e, r["per_worker"]["youth"], r["per_worker"]["older"],
                 r["youth_gap"]))
    print("  across climate settings (hothaps):")
    for cl in MC.CLIMATES:
        r = evaluate(ct, cl)
        print("    %-14s youth %6.3f h/day  (mean WBGT %5.2f C)"
              % (cl, r["per_worker"]["youth"], r["mean_wbgt"]))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
