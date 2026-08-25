# -*- coding: utf-8 -*-
"""Where the cooling goes.

A fixed planting budget, expressed in hectares of new tree canopy, is allocated
across the city under competing rules. Each rule is a weighting of cells; the
budget is distributed in proportion to the weights, subject to a per-cell
ceiling on how much canopy a cell can carry, by water-filling.

The rules are the ones a city actually chooses between:

    uniform          spread evenly over plantable land
    population       in proportion to residents, the amenity default
    deprivation      in proportion to residents weighted by deprivation, the
                     environmental-justice default
    population_heat  in proportion to residents weighted by local heat, the
                     heat-aware residential rule
    exposure         in proportion to heat-exposed jobs weighted by local heat
    youth            in proportion to heat-exposed YOUNG workers weighted by heat
    greedy           chosen to minimise young workers' lost hours directly

The first three are sited by where people live or are disadvantaged. The last
three are sited by where exposed work happens.

population_heat exists to keep the comparison honest. The exposure rules weight
by local heat as well as by workplace, so comparing them with a plain
population rule would confound two separate ideas: targeting the hottest places
and targeting workplaces rather than homes. The clean test of the spatial
question is exposure against population_heat, because those two differ only in
whose location is counted.
"""
from __future__ import annotations

import numpy as np

import city as C
import labour as LB
import microclimate as MC
import params as PA

CELL_HA = (C.CELL_M / 100.0) ** 2          # 250 m cell = 6.25 ha
CANOPY_CAP = 0.60                           # most canopy a built cell can carry

RULES = ("uniform", "population", "deprivation", "population_heat",
         "exposure", "youth", "greedy")


def plantable(city):
    """Mask and headroom: how much extra canopy each cell can take."""
    ok = ~np.isin(city.land_use, ["water"])
    head = np.where(ok, np.clip(CANOPY_CAP - city.canopy, 0.0, None), 0.0)
    return ok, head


def water_fill(weights, head, budget_ha):
    """Allocate a canopy budget in proportion to weights, respecting caps.

    Returns the per-cell canopy INCREMENT. Weight mass that cannot be placed
    because a cell is already full is redistributed over the remaining cells,
    so the whole budget is spent whenever there is headroom for it.
    """
    w = np.array(weights, dtype=float)
    w[head <= 0] = 0.0
    if w.sum() <= 0 or budget_ha <= 0:
        return np.zeros_like(head)

    inc = np.zeros_like(head)
    remaining = float(budget_ha)
    active = head > 0

    for _ in range(60):
        ww = np.where(active, w, 0.0)
        if ww.sum() <= 0 or remaining <= 1e-9:
            break
        share = ww / ww.sum()
        want = share * remaining / CELL_HA          # desired canopy increment
        room = np.where(active, head - inc, 0.0)
        take = np.minimum(want, room)
        inc += take
        spent = take.sum() * CELL_HA
        remaining -= spent
        active = active & ((head - inc) > 1e-12)
        if spent <= 1e-12:
            break
    return inc


def _heat_weight(city, climate):
    """Local heat, used to concentrate planting where it is hottest."""
    w = MC.wbgt_field(city, climate)
    m = w.mean(axis=2)
    return np.clip(m - m.min(), 0.0, None)


def weights(city, climate, rule):
    ok, head = plantable(city)
    if rule == "uniform":
        return ok.astype(float)
    if rule == "population":
        return city.residents * ok
    if rule == "deprivation":
        return city.residents * city.deprivation * ok
    if rule == "population_heat":
        return city.residents * _heat_weight(city, climate) * ok
    if rule == "exposure":
        exposed = city.jobs["high"] + city.jobs["moderate"]
        return exposed * _heat_weight(city, climate) * ok
    if rule == "youth":
        return city.exposed_youth() * _heat_weight(city, climate) * ok
    raise KeyError(rule)


def allocate(city, climate, rule, budget_ha, erf="hothaps"):
    """Canopy increment field for a rule."""
    ok, head = plantable(city)
    if rule == "greedy":
        return _greedy(city, climate, budget_ha, erf, head)
    return water_fill(weights(city, climate, rule), head, budget_ha)


def _greedy(city, climate, budget_ha, erf, head, steps=16):
    """Allocate in slices, filling the cells with the best marginal return.

    Marginal return is measured directly: how many young workers' hours a small
    canopy increment in a cell would save, per hectare of canopy that increment
    consumes. Each slice is spent by filling the best-ranked cells to their
    ceiling in turn, which is what makes this a benchmark rather than another
    proportional weighting. It is an upper reference, not a proposal — no city
    plants by numerical optimisation.
    """
    inc = np.zeros_like(head)
    slice_ha = budget_ha / steps
    probe = 0.05

    for _ in range(steps):
        canopy = np.clip(city.canopy + inc, 0.0, CANOPY_CAP)
        base = LB.lost_hours_field(
            city, MC.wbgt_field(city, climate, canopy), erf, "youth")
        room = np.clip(head - inc, 0.0, None)
        bump = np.where(room > 0, np.minimum(probe, room), 0.0)
        alt = LB.lost_hours_field(
            city, MC.wbgt_field(city, climate, np.clip(canopy + bump, 0, CANOPY_CAP)),
            erf, "youth")
        # hours saved per hectare of canopy actually consumed by the probe
        consumed = bump * CELL_HA
        gain = np.where(consumed > 0, np.clip(base - alt, 0.0, None) / np.maximum(consumed, 1e-12), 0.0)

        order = np.argsort(gain.ravel())[::-1]
        remaining = slice_ha
        flat_room = room.ravel()
        flat_inc = inc.ravel()
        for idx in order:
            if remaining <= 1e-9 or gain.ravel()[idx] <= 0:
                break
            can_take_ha = flat_room[idx] * CELL_HA
            if can_take_ha <= 0:
                continue
            take_ha = min(can_take_ha, remaining)
            flat_inc[idx] += take_ha / CELL_HA
            remaining -= take_ha
        inc = flat_inc.reshape(head.shape)
        if remaining > slice_ha - 1e-9:
            break
    return inc


def budget_from_cost(eur):
    """Hectares of canopy that a euro budget buys."""
    per_ha = PA.v("cost_tree_eur") * PA.v("trees_per_ha")
    return eur / per_ha


def compare(city, climate, budget_ha, erf="hothaps", rules=RULES):
    """Evaluate every rule against the do-nothing baseline."""
    base = LB.evaluate(city, climate, None, erf)
    out = {"baseline": base, "budget_ha": budget_ha,
           "budget_eur": budget_ha * PA.v("cost_tree_eur") * PA.v("trees_per_ha"),
           "rules": {}}
    for r in rules:
        inc = allocate(city, climate, r, budget_ha, erf)
        canopy = np.clip(city.canopy + inc, 0.0, CANOPY_CAP)
        res = LB.evaluate(city, climate, canopy, erf)
        saved_y = base["total"]["youth"] - res["total"]["youth"]
        saved_o = base["total"]["older"] - res["total"]["older"]
        placed = float(inc.sum() * CELL_HA)
        out["rules"][r] = {
            "hours_saved_youth": float(saved_y),
            "hours_saved_older": float(saved_o),
            "hours_saved_total": float(saved_y + saved_o),
            "per_ha_youth": float(saved_y / max(placed, 1e-9)),
            "ha_placed": placed,
            "youth_share_of_saving": float(saved_y / max(saved_y + saved_o, 1e-9)),
            "residual_youth_gap": res["youth_gap"],
        }
    return out


def _selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        if not c:
            print("FAIL:", m); ok = False

    ct = C.City(seed=7, divergence=0.75)
    _, head = plantable(ct)

    # water-filling must spend the budget and respect caps
    inc = water_fill(ct.residents, head, 300.0)
    chk(abs(inc.sum() * CELL_HA - 300.0) < 1.0, "budget spent (%.2f ha)"
        % (inc.sum() * CELL_HA))
    chk((inc <= head + 1e-9).all(), "per-cell caps respected")
    chk((inc[ct.land_use == "water"] == 0).all(), "nothing planted on water")

    r = compare(ct, "pannonian", 300.0)
    for name, v in r["rules"].items():
        chk(v["hours_saved_youth"] >= -1e-9, "%s saves non-negative hours" % name)
        chk(abs(v["ha_placed"] - 300.0) < 1.0, "%s places the budget" % name)

    best = max(r["rules"], key=lambda k: r["rules"][k]["hours_saved_youth"])
    chk(r["rules"]["greedy"]["hours_saved_youth"]
        >= r["rules"]["population"]["hours_saved_youth"] - 1e-9,
        "greedy is at least as good as population weighting")

    print("siting.py self-test:", "PASSED" if ok else "FAILED")
    print("  budget %.0f ha (about EUR %.1f million)"
          % (r["budget_ha"], r["budget_eur"] / 1e6))
    print("  baseline youth loss %.0f h/day" % r["baseline"]["total"]["youth"])
    print("  %-12s %12s %12s %10s" % ("rule", "youth h saved", "per ha", "youth share"))
    for name in RULES:
        v = r["rules"][name]
        print("  %-12s %12.1f %12.4f %9.1f%%"
              % (name, v["hours_saved_youth"], v["per_ha_youth"],
                 100 * v["youth_share_of_saving"]))
    print("  best rule for young workers: %s" % best)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
