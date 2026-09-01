# -*- coding: utf-8 -*-
"""From urban form and green-blue cover to the heat a worker actually feels.

Two pathways carry cooling to an outdoor worker, and the model keeps them
separate because they are not interchangeable:

    the AIR pathway     canopy and water lower the air temperature of a cell,
                        which lowers the shade index everywhere in it

    the RADIANT pathway tree crowns cut the sky view factor at the work
                        location, which removes short-wave load from the
                        worker directly

For a worker standing in the sun the radiant pathway is much the larger of the
two, and separating them is what allows the model to say where a planted tree
should go: over the worker, or anywhere in the district.

Climate settings are stated as parameters, not attributed to named cities. The
four settings span the range of European summer conditions from a cool
maritime north-west to a hot Mediterranean south.
"""
from __future__ import annotations

import numpy as np

import city as C
import params as PA
import thermal as TH

# Summer climate settings, anchored to observation.
#
# The four settings are not invented temperatures. Each is placed at a
# percentile of the distribution of mean summer (JJA) land-surface temperature
# across the twenty-seven EU Member States over 2001-2020, computed from
# Berkeley Earth country series in eudata.py. The value anchored is the
# twenty-four-hour summer mean; a declared diurnal range then sets the daily
# maximum and minimum around it, and the urban heat island increment is added
# afterwards inside the model, so the anchor is the regional background rather
# than the urban value.
#
# Representative latitudes are those of a country sitting near each
# percentile, and enter only through the latitude scaling of blue-space
# cooling.
import eudata as ED

_PCT = ED.climate_percentiles()

_SETTINGS = (
    # key,            percentile, diurnal range, latitude, label
    ("maritime",      "p10",      8.0,  53.0, "cool maritime summer, tenth percentile of EU-27"),
    ("continental",   "median",  11.0,  48.7, "temperate continental summer, EU-27 median"),
    ("pannonian",     "p75",     11.5,  45.1, "warm continental summer, EU-27 upper quartile"),
    ("mediterranean", "max",     12.0,  35.1, "hot Mediterranean summer, EU-27 maximum"),
)

# Relative humidity declines as the summer mean rises across Europe; the two
# end points are declared modelling choices and are swept in params.py.
_RH_COOL, _RH_HOT = 64.0, 38.0

CLIMATES = {}
for _k, _p, _range, _lat, _lab in _SETTINGS:
    _mean = _PCT[_p]
    _span = max(_PCT["max"] - _PCT["min"], 1e-9)
    _frac = (_mean - _PCT["min"]) / _span
    CLIMATES[_k] = dict(
        tmax=_mean + _range / 2.0,
        tmin=_mean - _range / 2.0,
        rh_day=_RH_COOL + (_RH_HOT - _RH_COOL) * _frac,
        lat=_lat,
        jja_mean=_mean,
        percentile=_p,
        label=_lab)

WORK_HOURS = np.arange(8, 17)          # 08:00 to 16:00 inclusive


def diurnal(climate, hours=WORK_HOURS):
    """Air temperature, relative humidity and irradiance over the work day."""
    c = CLIMATES[climate]
    # temperature peaks mid-afternoon
    phase = np.cos((hours - 15.0) / 24.0 * 2 * np.pi)
    ta = c["tmin"] + (c["tmax"] - c["tmin"]) * (0.5 + 0.5 * phase)
    # relative humidity moves inversely to temperature
    span = (ta - ta.min()) / max(ta.max() - ta.min(), 1e-9)
    rh = c["rh_day"] + 14.0 * (0.5 - span)
    # irradiance peaks at solar noon
    solar = PA.v("solar_noon_wm2") * np.clip(
        np.cos((hours - 13.0) / 24.0 * 2 * np.pi) ** 3, 0.0, None)
    return ta, np.clip(rh, 15.0, 95.0), solar


def uhi_field(city):
    """Canopy-layer heat island increment, degrees Celsius, per cell."""
    d = city.density / max(city.density.max(), 1e-9)
    return PA.v("uhi_max_c") * d


def air_cooling(city, canopy):
    """Air-temperature reduction from canopy and from water, per cell."""
    # canopy: the literature value is stated per ten percentage points
    green = PA.v("canopy_air_cooling") * (canopy * 100.0) / 10.0

    # water: exponential decay from the nearest water cell, with the decay
    # distance scaled by latitude about the declared pivot
    blue = np.zeros_like(canopy)
    if np.isfinite(city.water_dist).any():
        blue = PA.v("blue_cool_day_c") * np.exp(
            -city.water_dist / max(city._blue_decay, 1.0))
    return green, blue


def sky_view(city, canopy):
    """Sky view factor at the work location, given built form and canopy."""
    base = np.where(city.density > 0.40, PA.v("svf_canyon"), PA.v("svf_open"))
    under = PA.v("svf_under_canopy")
    # a worker is shaded in proportion to the canopy cover of the cell
    return base * (1.0 - canopy) + under * canopy


def wind_field(city):
    lo, hi = PA.v("wind_canyon_ms"), PA.v("wind_open_ms")
    return hi - (hi - lo) * np.clip(city.density / 0.7, 0.0, 1.0)


def wbgt_field(city, climate, canopy=None, hours=WORK_HOURS):
    """Outdoor WBGT per cell per work hour. Returns (N, N, H)."""
    canopy = city.canopy if canopy is None else canopy
    ta, rh, solar = diurnal(climate, hours)

    lat = CLIMATES[climate]["lat"]
    scale = np.clip(1.0 - (lat - PA.v("blue_latitude_pivot")) / 25.0, 0.25, 1.9)
    city._blue_decay = PA.v("blue_decay_m") * scale

    green, blue = air_cooling(city, canopy)
    uhi = uhi_field(city)
    svf = sky_view(city, canopy)
    wind = wind_field(city)

    dta = (uhi - green - blue)[:, :, None]
    ta_cell = ta[None, None, :] + dta
    rh_cell = np.broadcast_to(rh[None, None, :], ta_cell.shape)

    shade = TH.swbgt(ta_cell, rh_cell)
    inc = TH.radiant_increment(
        solar[None, None, :], wind[:, :, None], svf[:, :, None],
        PA.v("radiant_gain"), PA.v("wind_floor_ms"))
    return shade + inc


def _selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        if not c:
            print("FAIL:", m); ok = False

    ct = C.City(seed=3, divergence=0.75)

    for name in CLIMATES:
        w = wbgt_field(ct, name)
        chk(np.isfinite(w).all(), "%s WBGT finite" % name)
        chk(w.shape == (C.N, C.N, len(WORK_HOURS)), "%s shape" % name)

    # hotter climate must give higher WBGT
    m = wbgt_field(ct, "maritime").mean()
    d = wbgt_field(ct, "mediterranean").mean()
    chk(d > m, "Mediterranean hotter than maritime (%.2f vs %.2f)" % (d, m))

    # adding canopy must never raise WBGT
    base = wbgt_field(ct, "pannonian")
    more = wbgt_field(ct, "pannonian", np.clip(ct.canopy + 0.25, 0, 0.95))
    chk(more.mean() < base.mean(), "extra canopy cools (%.2f -> %.2f)"
        % (base.mean(), more.mean()))

    # the radiant pathway must dominate the air pathway for an exposed worker
    can0 = np.zeros_like(ct.canopy)
    can1 = np.full_like(ct.canopy, 0.5)
    only_air_cool = (PA.v("canopy_air_cooling") * 50.0 / 10.0)
    full = wbgt_field(ct, "pannonian", can0).mean() - \
        wbgt_field(ct, "pannonian", can1).mean()
    chk(full > only_air_cool,
        "shade adds to air cooling (total %.2f C vs air-only %.2f C)"
        % (full, only_air_cool))

    # The outdoor radiant increment for a fully exposed worker must land in
    # the 3-6 C band the parameter was declared to reproduce. This test is the
    # reason the parameter carries the value it does.
    inc = float(TH.radiant_increment(PA.v("solar_noon_wm2"), PA.v("wind_open_ms"),
                                     PA.v("svf_open"), PA.v("radiant_gain"),
                                     PA.v("wind_floor_ms")))
    chk(3.0 <= inc <= 6.0,
        "exposed radiant increment %.2f C inside the declared 3-6 C band" % inc)

    print("microclimate.py self-test:", "PASSED" if ok else "FAILED")
    print("  mean work-hour WBGT by climate setting:")
    for name in CLIMATES:
        w = wbgt_field(ct, name)
        print("    %-14s %5.2f C   (peak cell-hour %5.2f C)"
              % (name, w.mean(), w.max()))
    print("  canopy 0 -> 0.5 lowers mean WBGT by %.2f C, of which air-only %.2f C"
          % (full, only_air_cool))
    print("  radiant increment, fully exposed worker at solar noon: %.2f C" % inc)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
