# -*- coding: utf-8 -*-
"""Real European data, used to anchor the model.

Two observational sources are read here. Neither is used to estimate a
relationship; both are used to place the synthetic city and its climate
settings inside the range that European cities and European summers actually
occupy, and to describe how green provision is currently distributed.

    GHS-UCDB R2019A   the Global Human Settlement Layer Urban Centre
                      Database of the European Commission Joint Research
                      Centre. 556 urban centres on the European territory of
                      the EU-27, cross-sectional. Fields used: average
                      greenness in 2014, the SDG 11.7 indicator of population
                      share with convenient access to public open space, the
                      heatwave-exposure index, urban-centre area, built-up
                      area and population.

    Berkeley Earth    country monthly land-surface temperature. Summer (JJA)
                      country means for the EU-27 over 2001-2020 are used to
                      set the four climate settings at real percentiles of the
                      European summer distribution rather than at invented
                      values.
"""
from __future__ import annotations

import csv
import os
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))

UCDB = os.path.join(DATA, "ucdb_r2019a_eu27_urban_centres.csv")
BERK = os.path.join(DATA, "berkeley_earth_eu27_summer_JJA_temperature.csv")
WDI = os.path.join(DATA, "wdi_eu27_youth_unemployment_1524.csv")

JJA_FROM, JJA_TO = 2001, 2020


def _f(v):
    v = (v or "").strip()
    if v in ("", "nan", "NaN", "None"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _q(sorted_vals, p):
    if not sorted_vals:
        return None
    return sorted_vals[int(p * (len(sorted_vals) - 1))]


def urban_centres():
    """EU-27 urban centres on the European territory."""
    rows = list(csv.DictReader(open(UCDB, encoding="utf-8")))
    return [r for r in rows
            if (r.get("EU27_EUROPEAN_TERRITORY", "1") or "1").strip()
            not in ("0", "0.0")]


def ucdb_stats():
    rs = urban_centres()
    out = {"n": len(rs)}
    fields = {
        "greenness_2014": "E_GR_AV14",
        "green_access_sdg11_7": "SDG_A2G14",
        "heatwave_index": "EX_HW_IDX",
        "area_km2": "AREA",
        "builtup_km2": "B15",
        "population_2015": "P15",
    }
    for name, col in fields.items():
        v = sorted(x for x in (_f(r.get(col)) for r in rs) if x is not None)
        out[name] = {"n": len(v), "min": v[0], "p25": _q(v, .25),
                     "median": _q(v, .50), "p75": _q(v, .75), "max": v[-1],
                     "mean": st.mean(v)}
    dens = sorted(p / a for p, a in
                  ((_f(r.get("P15")), _f(r.get("AREA"))) for r in rs)
                  if p and a)
    out["density_per_km2"] = {"n": len(dens), "min": dens[0],
                              "p25": _q(dens, .25), "median": _q(dens, .50),
                              "p75": _q(dens, .75), "max": dens[-1],
                              "mean": st.mean(dens)}
    out["area_percentile_of_100km2"] = sum(
        1 for r in rs if (_f(r.get("AREA")) or 0) <= 100.0) / len(rs)
    return out


def jja_by_country():
    rows = list(csv.DictReader(open(BERK, encoding="utf-8")))
    by = {}
    for r in rows:
        y = r.get("year", "")
        t = _f(r.get("jja_temperature_C"))
        if y.isdigit() and JJA_FROM <= int(y) <= JJA_TO and t is not None:
            by.setdefault(r["country_name"], []).append(t)
    return {k: st.mean(v) for k, v in by.items() if len(v) >= 15}


def climate_percentiles():
    """The EU-27 summer distribution the four climate settings sit on."""
    m = jja_by_country()
    v = sorted(m.values())
    return {"n_countries": len(v), "min": v[0], "p10": _q(v, .10),
            "p25": _q(v, .25), "median": _q(v, .50), "p75": _q(v, .75),
            "p90": _q(v, .90), "max": v[-1], "by_country": m}


def youth_unemployment_latest():
    """EU aggregate youth unemployment rate, latest available year."""
    rows = list(csv.DictReader(open(WDI, encoding="utf-8")))
    eu = [r for r in rows if r.get("country_code") == "EUU"
          and _f(r.get("value")) is not None]
    if not eu:
        return None
    latest = max(eu, key=lambda r: int(r["year"]))
    return {"year": int(latest["year"]), "value": _f(latest["value"]),
            "indicator": latest.get("indicator_name", "")}


def _selftest():
    u = ucdb_stats()
    c = climate_percentiles()
    y = youth_unemployment_latest()
    print("eudata.py")
    print("  GHS-UCDB urban centres, EU-27 European territory: %d" % u["n"])
    for k in ("greenness_2014", "green_access_sdg11_7", "heatwave_index",
              "area_km2", "density_per_km2"):
        d = u[k]
        print("    %-22s n=%3d  p25 %8.2f  median %8.2f  p75 %8.2f"
              % (k, d["n"], d["p25"], d["median"], d["p75"]))
    print("    a 100 km2 city is at the %.0fth percentile of urban-centre area"
          % (100 * u["area_percentile_of_100km2"]))
    print("  Berkeley Earth JJA country means %d-%d, %d countries:"
          % (JJA_FROM, JJA_TO, c["n_countries"]))
    print("    min %.2f  p10 %.2f  median %.2f  p75 %.2f  max %.2f C"
          % (c["min"], c["p10"], c["median"], c["p75"], c["max"]))
    if y:
        print("  World Bank youth unemployment, EU aggregate, %d: %.1f%%"
              % (y["year"], y["value"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
