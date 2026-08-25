# -*- coding: utf-8 -*-
"""Biophysical core: humid-heat indices and heat-induced work-capacity loss.

Everything in this module is an algebraic implementation of a published form.
Nothing is fitted here.

Heat index
----------
The simplified ("Australian") wet bulb globe temperature is a widely used
shade approximation of WBGT requiring only dry-bulb temperature and
water-vapour pressure:

    sWBGT = 0.567 Ta + 0.393 e + 3.94                       (Ta in C, e in hPa)

Vapour pressure follows from relative humidity through the August-Roche-Magnus
saturation formula. Outdoor work is not in the shade, so a radiant increment is
added that grows with the short-wave radiation actually reaching the worker
(incident radiation weighted by the sky view factor) and falls with
ventilation. That increment is the one genuinely tunable piece of the
biophysics and is declared as an assumed parameter in params.py and swept.

Exposure-response functions
---------------------------
Five published functions map WBGT to physical work capacity. All five were
transcribed from open-source reference implementations and cross-checked
against each other:

    hothaps  PWC = 0.1 + 0.9 / (1 + (WBGT/a1)^a2)
             a1, a2 = 30.94, 16.64 (high) | 32.93, 17.81 (moderate)
                    | 34.64, 22.72 (low)
             Foster et al. (2021); see also Smallcombe et al. (2022).

    iso      WBGT_lim = 34.9 - M/46, rest = 34.9 - 117/46
             PWC = clip((rest - WBGT) / (rest - WBGT_lim), 0, 1)
             Kjellstrom et al. (2014), after Kjellstrom et al. (2009).

    niosh    WBGT_lim = 56.7 - 11.5 log10(M), rest = 56.7 - 11.5 log10(117)
             PWC = clip((rest - WBGT) / (rest - WBGT_lim), 0, 1)
             Broede et al. (2018); Jacklitsch et al. (2016).

    dunne    PWC = clip(1 - 0.25 max(0, WBGT - 25)^(2/3), 0, 1) * f,
             f = 1 (heavy), 2 (moderate), 4 (light), re-clipped to 1.
             Dunne, Stouffer and John (2013).

    foster   PWC = 1 / (1 + (33.63/WBGT)^-6.33)
             Foster et al. (2021), Table 3. Workload-independent.

Metabolic classes follow Kjellstrom et al. (2009): 200 W for office and
service work, 300 W for manufacturing, 400 W for construction and agriculture,
117 W for rest. The labels "high", "moderate" and "low" are nominal.

The five functions disagree substantially in the WBGT band in which European
summers sit, which is why the model carries all of them rather than choosing
one, and why the choice of function is treated as the leading source of
uncertainty rather than as a modelling detail.
"""
from __future__ import annotations

import numpy as np

# metabolic rate, watts, by nominal workload class (Kjellstrom et al. 2009)
METABOLIC = {"low": 200.0, "moderate": 300.0, "high": 400.0}
M_REST = 117.0

ERF_NAMES = ("hothaps", "iso", "niosh", "dunne", "foster")

_HOTHAPS = {"high": (30.94, 16.64),
            "moderate": (32.93, 17.81),
            "low": (34.64, 22.72)}

_DUNNE_FACTOR = {"high": 1.0, "moderate": 2.0, "low": 4.0}


# ---------------------------------------------------------------------------
# humidity and heat indices
# ---------------------------------------------------------------------------
def saturation_vapour_pressure(ta_c):
    """Saturation vapour pressure in hPa (August-Roche-Magnus)."""
    ta = np.asarray(ta_c, dtype=float)
    return 6.1094 * np.exp(17.625 * ta / (ta + 243.04))


def vapour_pressure(ta_c, rh_pct):
    """Actual water-vapour pressure in hPa."""
    return saturation_vapour_pressure(ta_c) * np.asarray(rh_pct, float) / 100.0


def swbgt(ta_c, rh_pct):
    """Simplified (shade) wet bulb globe temperature, degrees Celsius."""
    e = vapour_pressure(ta_c, rh_pct)
    return 0.567 * np.asarray(ta_c, float) + 0.393 * e + 3.94


def radiant_increment(solar_wm2, wind_ms, sky_view, gain, wind_floor):
    """Outdoor radiant load added to the shade index, degrees Celsius."""
    solar = np.asarray(solar_wm2, float) * np.asarray(sky_view, float)
    wind = np.maximum(np.asarray(wind_ms, float), wind_floor)
    return gain * np.sqrt(np.maximum(solar, 0.0)) / np.sqrt(wind)


def wbgt_outdoor(ta_c, rh_pct, solar_wm2, wind_ms, sky_view, gain, wind_floor):
    """Outdoor WBGT: the shade index plus the radiant increment."""
    return swbgt(ta_c, rh_pct) + radiant_increment(
        solar_wm2, wind_ms, sky_view, gain, wind_floor)


# ---------------------------------------------------------------------------
# exposure-response functions
# ---------------------------------------------------------------------------
def _pwc_hothaps(wbgt, workload):
    a1, a2 = _HOTHAPS[workload]
    w = np.maximum(np.asarray(wbgt, float), 0.0)
    return 0.1 + 0.9 / (1.0 + (w / a1) ** a2)


def _pwc_linear(wbgt, workload, lim_fn):
    m = METABOLIC[workload]
    lim = lim_fn(m)
    rest = lim_fn(M_REST)
    lvl = (rest - np.asarray(wbgt, float)) / (rest - lim)
    return np.clip(lvl, 0.0, 1.0)


def _pwc_iso(wbgt, workload):
    return _pwc_linear(wbgt, workload, lambda m: 34.9 - m / 46.0)


def _pwc_niosh(wbgt, workload):
    return _pwc_linear(wbgt, workload, lambda m: 56.7 - 11.5 * np.log10(m))


def _pwc_dunne(wbgt, workload):
    base = np.clip(
        1.0 - 0.25 * np.maximum(0.0, np.asarray(wbgt, float) - 25.0) ** (2.0 / 3.0),
        0.0, 1.0)
    return np.clip(base * _DUNNE_FACTOR[workload], 0.0, 1.0)


def _pwc_foster(wbgt, workload=None):
    w = np.maximum(np.asarray(wbgt, float), 1e-9)
    return 1.0 / (1.0 + (33.63 / w) ** -6.33)


_ERF = {"hothaps": _pwc_hothaps, "iso": _pwc_iso, "niosh": _pwc_niosh,
        "dunne": _pwc_dunne, "foster": _pwc_foster}


def work_capacity(wbgt_c, workload="high", erf="hothaps"):
    """Physical work capacity in [0, 1] under a named published function."""
    if erf not in _ERF:
        raise KeyError("unknown exposure-response function %r" % erf)
    return np.clip(_ERF[erf](wbgt_c, workload), 0.0, 1.0)


def capacity_loss(wbgt_c, workload="high", erf="hothaps"):
    """Share of a working hour lost to heat, in [0, 1]."""
    return 1.0 - work_capacity(wbgt_c, workload, erf)


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------
def _selftest():
    ok = True

    def chk(cond, msg):
        nonlocal ok
        if not cond:
            print("FAIL:", msg)
            ok = False

    es20 = float(saturation_vapour_pressure(20.0))
    chk(23.0 < es20 < 23.8, "es(20 C) = %.3f hPa, expected about 23.4" % es20)

    chk(float(swbgt(35, 40)) > float(swbgt(30, 40)), "sWBGT rises with temperature")
    chk(float(swbgt(30, 70)) > float(swbgt(30, 40)), "sWBGT rises with humidity")

    # every function: bounded, monotone non-increasing in WBGT
    grid = np.linspace(5, 45, 400)
    for e in ERF_NAMES:
        for wl in ("low", "moderate", "high"):
            w = work_capacity(grid, wl, e)
            chk(w.max() <= 1.0 + 1e-9 and w.min() >= -1e-9,
                "%s/%s within [0,1]" % (e, wl))
            chk(np.all(np.diff(w) <= 1e-9), "%s/%s monotone" % (e, wl))

    # Heavier work must never have more capacity than lighter work over the
    # range this study uses. The Hothaps curves cross marginally above about
    # 41.7 C, where all three workloads are already pinned to their common
    # 0.1 floor; that is a property of the published parameters, not of this
    # implementation, and it lies far outside European conditions.
    band = np.linspace(5, 40, 400)
    for e in ERF_NAMES:
        if e == "foster":
            continue
        hi = work_capacity(band, "high", e)
        mo = work_capacity(band, "moderate", e)
        lo = work_capacity(band, "low", e)
        chk(np.all(hi <= mo + 1e-9) and np.all(mo <= lo + 1e-9),
            "%s workload ordering below 40 C" % e)

    # published anchor points
    chk(abs(float(work_capacity(30.94, "high", "hothaps")) - 0.55) < 1e-6,
        "Hothaps high at a1 = 30.94 gives 0.55")
    chk(float(work_capacity(34.9 - M_REST / 46.0, "high", "iso")) == 0.0,
        "ISO reaches zero at its resting limit")
    chk(float(work_capacity(56.7 - 11.5 * np.log10(M_REST), "high", "niosh")) == 0.0,
        "NIOSH reaches zero at its resting limit")
    chk(abs(float(work_capacity(33.0, "high", "dunne"))) < 1e-6,
        "Dunne heavy reaches zero at 33 C")
    chk(float(work_capacity(25.0, "high", "dunne")) == 1.0,
        "Dunne heavy is unaffected up to 25 C")

    print("thermal.py self-test:", "PASSED" if ok else "FAILED")
    print()
    print("  heavy-work capacity LOSS (%), by function, across the European band")
    print("  WBGT   " + "".join("%9s" % e for e in ERF_NAMES))
    for t in (20, 23, 25, 27, 28, 30, 32):
        row = "".join("%8.1f " % (100 * capacity_loss(t, "high", e))
                      for e in ERF_NAMES)
        print("  %-6d %s" % (t, row))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
