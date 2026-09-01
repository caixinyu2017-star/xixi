# -*- coding: utf-8 -*-
"""The parameter registry.

Every quantity the model needs is declared here exactly once, with its unit,
the interval over which the uncertainty analysis sweeps it, and an explicit
statement of where the value came from. The provenance field takes one of
three values and the manuscript reports the counts:

    "literature"  a value stated in, or transcribed from, the cited source
    "derived"     computed from values stated in cited sources
    "assumed"     a modelling choice, not obtained from any source

No value is silently promoted from "assumed" to "literature". The parameter
appendix of the manuscript is generated from this registry, so the table in
the paper cannot disagree with the parameters the code actually used.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Param:
    name: str
    value: float
    unit: str
    low: float
    high: float
    provenance: str
    source: str
    note: str = ""

    def __post_init__(self):
        assert self.provenance in ("literature", "derived", "assumed"), self.provenance
        assert self.low <= self.value <= self.high, (
            "%s: value %r outside [%r, %r]" % (self.name, self.value, self.low, self.high))


_REG: dict[str, Param] = {}


def add(name, value, unit, low, high, provenance, source, note=""):
    assert name not in _REG, "duplicate parameter %s" % name
    _REG[name] = Param(name, value, unit, low, high, provenance, source, note)


_OVERRIDE: dict[str, float] = {}


def get(name):
    if name not in _REG:
        raise KeyError("undeclared parameter %r" % name)
    return _REG[name]


def v(name):
    """Current value: the override if one is in force, else the declared value."""
    if name in _OVERRIDE:
        return _OVERRIDE[name]
    return get(name).value


class override:
    """Temporarily replace parameter values, for the uncertainty analysis."""

    def __init__(self, mapping):
        for k in mapping:
            if k not in _REG:
                raise KeyError("cannot override undeclared parameter %r" % k)
        self.mapping = dict(mapping)
        self.saved = None

    def __enter__(self):
        self.saved = dict(_OVERRIDE)
        _OVERRIDE.update(self.mapping)
        return self

    def __exit__(self, *exc):
        _OVERRIDE.clear()
        _OVERRIDE.update(self.saved)
        return False


def table():
    return [_REG[k] for k in sorted(_REG)]


def counts():
    c = {"literature": 0, "derived": 0, "assumed": 0}
    for p in _REG.values():
        c[p.provenance] += 1
    return c


def sweepable():
    """Parameters whose sweep interval is non-degenerate."""
    return [p for p in table() if p.high > p.low]


# ===========================================================================
# 1. Radiation, ventilation and the outdoor heat load
# ===========================================================================
add("radiant_gain", 0.24, "C (W m-2)^-0.5 (m s-1)^0.5", 0.18, 0.36, "assumed",
    "Bulk coefficient converting absorbed short-wave radiation and wind speed "
    "into the globe-temperature increment above the shade index. Chosen so "
    "that a fully exposed worker under 700 W m-2 at 2 m s-1 sits roughly 3-6 C "
    "above the shade index, the commonly reported outdoor-minus-shade WBGT "
    "difference. Swept widely because it is not measured here.")

add("wind_floor_ms", 0.5, "m s-1", 0.3, 1.0, "assumed",
    "Lower bound on wind speed, preventing the ventilation term from "
    "diverging in still air.")

add("solar_noon_wm2", 780.0, "W m-2", 650.0, 900.0, "assumed",
    "Peak short-wave irradiance on a clear European summer day, used to scale "
    "the diurnal radiation cycle.")

# ===========================================================================
# 2. Urban form and the heat island
# ===========================================================================
add("uhi_max_c", 3.2, "C", 1.5, 5.0, "literature",
    "Canonical summer daytime canopy-layer urban heat island intensity for "
    "European cities. Swept across the range reported for cities of differing "
    "size and climate.")

add("svf_open", 0.92, "dimensionless", 0.85, 0.98, "assumed",
    "Sky view factor of an open, unshaded work location such as a yard, "
    "car park or construction site.")

add("svf_canyon", 0.45, "dimensionless", 0.30, 0.60, "assumed",
    "Sky view factor of a typical mid-rise street canyon.")

add("svf_under_canopy", 0.15, "dimensionless", 0.08, 0.28, "assumed",
    "Sky view factor beneath an established broadleaf tree crown. This is the "
    "parameter through which shade acts on the radiant load, and it is the "
    "dominant pathway by which trees protect an outdoor worker.")

add("wind_open_ms", 2.6, "m s-1", 1.8, 3.6, "assumed",
    "Daytime wind speed at an open work location.")

add("wind_canyon_ms", 1.4, "m s-1", 0.8, 2.2, "assumed",
    "Daytime wind speed within a built-up street canyon, reduced by "
    "sheltering. The ratio to the open value represents urban ventilation.")

# ===========================================================================
# 3. Green infrastructure cooling
# ===========================================================================
add("canopy_air_cooling", 0.30, "C per 10 percentage points of canopy", 0.04, 0.80,
    "literature",
    "Air-temperature cooling per ten percentage points of additional tree "
    "canopy cover. The most commonly cited central value is about 0.3 C; "
    "reported estimates span roughly 0.04 C to 0.8 C depending on background "
    "climate, urban morphology, weather and measurement method. The width of "
    "this interval is one of the two uncertainties the study is built around.")

add("park_cool_island_c", 1.1, "C", 0.5, 2.5, "literature",
    "Cooling of the air within a park relative to its built surroundings, "
    "reported for the large majority of parks studied across climates.")

add("park_decay_m", 180.0, "m", 80.0, 400.0, "literature",
    "e-folding distance over which park cooling decays into the surrounding "
    "built fabric.")

# ===========================================================================
# 4. Blue infrastructure cooling
# ===========================================================================
add("blue_cool_day_c", 2.0, "C", 0.8, 3.3, "literature",
    "Daytime air-temperature cooling adjacent to an urban water body. "
    "Reported central estimates cluster between about 2 C and 3 C, with wide "
    "variation by water-body size, morphology and background climate.")

add("blue_decay_m", 120.0, "m", 30.0, 740.0, "literature",
    "Distance over which blue-space cooling decays. The interval is very wide "
    "and strongly latitude dependent: reported effective distances fall below "
    "about 30 m for northern European rivers and reach several hundred metres "
    "in warmer settings.")

add("blue_night_warming_c", 0.6, "C", 0.0, 1.2, "literature",
    "Night-time warming adjacent to a water body, the counterpart of daytime "
    "cooling. It does not affect daytime work capacity but is carried so that "
    "the model does not credit blue infrastructure with a benefit it does not "
    "deliver around the clock.")

add("blue_latitude_pivot", 45.0, "degrees north", 40.0, 50.0, "assumed",
    "Latitude at which the blue-space cooling distance is taken at its "
    "central value, with the effect scaled down towards northern Europe and "
    "up towards the Mediterranean.")

# ===========================================================================
# 5. Cost
# ===========================================================================
add("cost_tree_eur", 450.0, "EUR per established tree", 250.0, 900.0, "assumed",
    "Planting plus three-year establishment cost of a street tree in a "
    "European city, inclusive of pit construction and early maintenance.")

add("trees_per_ha", 120.0, "trees per hectare", 80.0, 180.0, "assumed",
    "Stocking density of new street or yard planting at which the canopy "
    "targets used here are reached at maturity.")

add("cost_blue_eur_ha", 900000.0, "EUR per hectare", 400000.0, 1800000.0, "assumed",
    "Capital cost of creating an urban water feature per hectare of water "
    "surface, an order-of-magnitude figure used only to place green and blue "
    "options on a common budget line.")

# ===========================================================================
# 6. Labour
# ===========================================================================
add("work_hours_per_day", 8.0, "h", 7.0, 9.0, "assumed",
    "Length of the working day over which capacity loss is accumulated.")

add("outdoor_share_high", 0.85, "share", 0.70, 0.95, "assumed",
    "Fraction of working time spent outdoors or in unconditioned space in "
    "construction and grounds work.")

add("outdoor_share_moderate", 0.45, "share", 0.25, 0.65, "assumed",
    "Fraction of working time spent outdoors or in unconditioned space in "
    "logistics, warehousing and light manufacturing.")

add("outdoor_share_low", 0.12, "share", 0.03, 0.25, "assumed",
    "Fraction of working time spent outdoors or in unconditioned space in "
    "retail, hospitality and service work.")

add("youth_wage_eur_h", 13.5, "EUR per hour", 9.0, 20.0, "assumed",
    "Gross hourly labour cost of a young worker, used only to express lost "
    "hours in monetary terms alongside the physical measure.")

# ===========================================================================
# 7. Age composition and age-specific consequences
# ===========================================================================
add("youth_share_high", 0.34, "share of jobs held by workers under 30", 0.22, 0.45,
    "assumed",
    "Share of heavy outdoor jobs held by young workers. Young people are "
    "concentrated in entry-level, temporary and apprentice positions on "
    "construction and grounds work, but no verified European figure for the "
    "age composition of heat-exposed employment was obtainable here. The "
    "value is therefore declared as an assumption and swept across an "
    "interval that includes no over-representation at all.")

add("youth_share_moderate", 0.32, "share", 0.20, 0.42, "assumed",
    "Share of logistics, warehousing and light manufacturing jobs held by "
    "young workers. Declared and swept on the same basis.")

add("youth_share_low", 0.30, "share", 0.20, 0.40, "assumed",
    "Share of retail, hospitality and service jobs held by young workers. "
    "Declared and swept on the same basis.")

add("youth_incident_ratio", 1.60, "ratio", 1.50, 1.70, "literature",
    "Ratio of the workplace-accident incidence rate of workers aged 18-24 to "
    "that of workers aged 25-54 in the European Union: 2311 against 1416 per "
    "100 000 workers, so young people are 1.5 to 1.7 times more likely to be "
    "injured at work. It is applied here only to convert lost hours into an "
    "age-weighted harm index, and is NOT applied to physical work capacity, "
    "which the model treats as age-neutral.")
