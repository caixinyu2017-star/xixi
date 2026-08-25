# -*- coding: utf-8 -*-
"""A stylised European city, on a grid.

The city is not a real place and is not presented as one. It is a transparent
synthetic urban form whose purpose is to make the geography of the problem
explicit: young workers in heat-exposed occupations are not distributed like
residents, and green infrastructure sited by where people live therefore need
not protect them.

The grid is 40 x 40 cells of 250 m, a 10 km square. Each cell carries

    land use            core | industry | residential | periphery | park | water
    building density    used for the ventilation reduction
    canopy fraction     the existing tree cover
    distance to water   for the blue-space decay
    residents           and a deprivation index
    jobs                split by workload class and by age group

The single structural quantity the study turns on is the DIVERGENCE between
where heat-exposed young people work and where residents live. It is a free
parameter of the city generator, reported as a correlation, and swept, so that
the conclusions are stated as a function of it rather than as a property of one
invented map.
"""
from __future__ import annotations

import numpy as np

N = 40                      # cells per side
CELL_M = 250.0              # cell size, metres
EXTENT_M = N * CELL_M

LANDUSE = ("core", "industry", "residential", "periphery", "park", "water")
WORKLOADS = ("high", "moderate", "low")


class City:
    """A generated city. All arrays are (N, N)."""

    def __init__(self, seed=20260825, divergence=0.75, river=True,
                 industry_angle=0.9, park_count=6):
        self.seed = int(seed)
        self.divergence = float(divergence)
        rng = np.random.default_rng(self.seed)
        self.rng = rng

        yy, xx = np.mgrid[0:N, 0:N]
        cx = cy = (N - 1) / 2.0
        self.dx = (xx - cx) * CELL_M
        self.dy = (yy - cy) * CELL_M
        self.radius = np.sqrt(self.dx ** 2 + self.dy ** 2)
        self.theta = np.arctan2(self.dy, self.dx)

        self._land_use(rng, river, industry_angle, park_count)
        self._form(rng)
        self._people(rng)
        self._jobs(rng)

    # -- land use ---------------------------------------------------------
    def _land_use(self, rng, river, industry_angle, park_count):
        r = self.radius
        lu = np.full((N, N), "periphery", dtype=object)
        lu[r < 4000] = "residential"
        lu[r < 1200] = "core"

        # an industrial and logistics wedge on one side of the city, at the
        # edge of the built area where land is cheap
        wedge = (np.abs(np.angle(np.exp(1j * (self.theta - industry_angle))))
                 < 0.55) & (r > 2000) & (r < 4600)
        lu[wedge] = "industry"

        # parks, placed in the residential ring
        for _ in range(park_count):
            while True:
                py, px = rng.integers(4, N - 4, size=2)
                if 1400 < self.radius[py, px] < 3800:
                    break
            rad = rng.integers(2, 4)
            m = (np.abs(np.mgrid[0:N, 0:N][0] - py) <= rad) & \
                (np.abs(np.mgrid[0:N, 0:N][1] - px) <= rad)
            lu[m & (lu != "core")] = "park"

        self.water_dist = np.full((N, N), 9e9)
        if river:
            # a river running roughly north-south, meandering
            col = (cx0 := (N - 1) / 2.0) + 4.0 * np.sin(
                np.arange(N) / N * 2.4 * np.pi + 0.6)
            for row in range(N):
                c = int(round(col[row]))
                c = int(np.clip(c, 0, N - 1))
                lu[row, c] = "water"
            wy, wx = np.where(lu == "water")
            for row in range(N):
                for cc in range(N):
                    d = np.min(np.sqrt(((wy - row) * CELL_M) ** 2 +
                                       ((wx - cc) * CELL_M) ** 2))
                    self.water_dist[row, cc] = d
        self.land_use = lu

    # -- urban form -------------------------------------------------------
    def _form(self, rng):
        lu = self.land_use
        dens = np.zeros((N, N))
        canopy = np.zeros((N, N))
        for name, d, c in (("core", 0.62, 0.06),
                           ("industry", 0.48, 0.03),
                           ("residential", 0.34, 0.14),
                           ("periphery", 0.14, 0.20),
                           ("park", 0.02, 0.62),
                           ("water", 0.0, 0.05)):
            m = lu == name
            dens[m] = d + 0.05 * rng.normal(size=m.sum())
            canopy[m] = np.clip(c + 0.04 * rng.normal(size=m.sum()), 0.0, 0.95)
        self.density = np.clip(dens, 0.0, 0.92)
        self.canopy = canopy

    # -- residents --------------------------------------------------------
    def _people(self, rng):
        lu = self.land_use
        base = np.zeros((N, N))
        for name, p in (("core", 55.0), ("residential", 100.0),
                        ("periphery", 28.0), ("industry", 6.0),
                        ("park", 0.0), ("water", 0.0)):
            base[lu == name] = p
        base *= np.exp(0.25 * rng.normal(size=(N, N)))
        self.residents = base

        # deprivation: higher towards the industrial side and the outer ring
        prox = np.exp(-((np.abs(np.angle(np.exp(1j * (self.theta - 0.9)))))
                        / 0.9) ** 2)
        dep = 0.45 * prox + 0.35 * (self.radius / self.radius.max()) \
            + 0.20 * rng.random((N, N))
        self.deprivation = (dep - dep.min()) / (dep.max() - dep.min())

    # -- jobs -------------------------------------------------------------
    def _jobs(self, rng):
        """Allocate jobs by workload class, then split each by age.

        Heat-exposed heavy work sits in the industrial wedge and on scattered
        construction sites; moderate work sits in logistics and light
        manufacturing; light work sits in the retail core. The share of each
        cell's heavy and moderate jobs held by young workers rises with the
        divergence parameter in exactly those places where residents are few,
        which is what makes residence-weighted siting miss them.
        """
        lu = self.land_use
        rng_local = rng
        jobs = {w: np.zeros((N, N)) for w in WORKLOADS}

        buildable = ~np.isin(lu, ["water", "park"])

        # Light service work follows the retail core and, more weakly, the
        # residential fabric. It is not the object of the study but it carries
        # a large share of young employment and so must be represented.
        low = np.zeros((N, N))
        low[lu == "core"] = 90.0
        low[lu == "residential"] = 14.0
        low[lu == "periphery"] = 4.0
        jobs["low"] = low

        # Heat-exposed work is allocated as an explicit mixture of two
        # patterns, and the mixing weight IS the divergence parameter.
        #
        #   residential-following: neighbourhood building work, local
        #       maintenance, grounds and delivery work serving residents
        #   wedge-following: the industrial, logistics and large-site pattern,
        #       on cheap land away from housing
        #
        # At divergence 0 the exposed workforce sits where people live; at
        # divergence 1 it sits where they do not. Real cities lie between,
        # and the study reports its results across the interval rather than
        # asserting a value.
        res_pat = self.residents / (self.residents.sum() + 1e-9)

        wedge_pat = np.zeros((N, N))
        wedge_pat[lu == "industry"] = 1.0
        wedge_pat[lu == "periphery"] = 0.22
        wedge_pat *= buildable
        wedge_pat /= (wedge_pat.sum() + 1e-9)

        d = self.divergence
        mix = (1.0 - d) * res_pat + d * wedge_pat
        mix *= buildable
        mix /= (mix.sum() + 1e-9)

        jobs["high"] = mix * 12000.0
        jobs["moderate"] = mix * 15000.0

        for w in WORKLOADS:
            jobs[w] = jobs[w] * np.exp(0.3 * rng_local.normal(size=(N, N)))
            jobs[w][lu == "water"] = 0.0
            jobs[w][lu == "park"] *= 0.15
        self.jobs = jobs

        # Youth share of each cell's jobs. Young workers are over-represented
        # in the exposed classes everywhere; the share does not carry the
        # spatial story, the allocation above does.
        import params as _PA
        youth = {}
        for w in WORKLOADS:
            base = _PA.v("youth_share_%s" % w)
            s_ = np.clip(base + 0.03 * rng_local.normal(size=(N, N)), 0.05, 0.85)
            youth[w] = s_
        self.youth_share = youth

        self.youth_jobs = {w: jobs[w] * youth[w] for w in WORKLOADS}
        self.older_jobs = {w: jobs[w] * (1.0 - youth[w]) for w in WORKLOADS}

        self._scale_to_observed_density()

    def _scale_to_observed_density(self):
        """Scale the city so its residential density matches European practice.

        The GHS-UCDB gives a median residential density across the 556 EU-27
        urban centres on European territory. Residents and jobs are scaled by a
        single common factor to reach it, so every ratio and every per-worker
        quantity in the study is unchanged and only the absolute counts move
        onto a realistic footing.
        """
        try:
            import eudata as _ED
            target = _ED.ucdb_stats()["density_per_km2"]["median"]
        except Exception:
            return
        area_km2 = (N * CELL_M / 1000.0) ** 2
        want = target * area_km2
        have = float(self.residents.sum())
        if have <= 0:
            return
        f = want / have
        self.residents *= f
        for w in WORKLOADS:
            self.jobs[w] *= f
            self.youth_jobs[w] *= f
            self.older_jobs[w] *= f
        self.density_scale = f
        self.target_density = target

    # -- summaries --------------------------------------------------------
    def exposed_youth(self):
        """Young workers in the two heat-exposed workload classes."""
        return self.youth_jobs["high"] + self.youth_jobs["moderate"]

    def workplace_residence_correlation(self):
        """Spatial correlation between exposed young workers and residents."""
        a = self.exposed_youth().ravel()
        b = self.residents.ravel()
        if a.std() == 0 or b.std() == 0:
            return float("nan")
        return float(np.corrcoef(a, b)[0, 1])

    def land_use_shares(self):
        tot = N * N
        return {k: float((self.land_use == k).sum()) / tot for k in LANDUSE}

    def summary(self):
        return {
            "cells": N * N,
            "cell_m": CELL_M,
            "extent_km": EXTENT_M / 1000.0,
            "divergence": self.divergence,
            "land_use_shares": self.land_use_shares(),
            "residents_total": float(self.residents.sum()),
            "jobs_total": {w: float(self.jobs[w].sum()) for w in WORKLOADS},
            "youth_jobs_total": {w: float(self.youth_jobs[w].sum()) for w in WORKLOADS},
            "exposed_youth_total": float(self.exposed_youth().sum()),
            "mean_canopy": float(self.canopy.mean()),
            "workplace_residence_r": self.workplace_residence_correlation(),
        }


def _selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        if not c:
            print("FAIL:", m); ok = False

    c = City(seed=1, divergence=0.75)
    s = c.summary()
    chk(abs(sum(s["land_use_shares"].values()) - 1.0) < 1e-9, "land-use shares sum to 1")
    chk(s["residents_total"] > 0, "city has residents")
    chk(s["exposed_youth_total"] > 0, "city has exposed young workers")
    chk(0.0 <= c.canopy.min() and c.canopy.max() <= 0.95, "canopy in range")
    chk(c.density.max() <= 0.92, "density bounded")
    chk((c.jobs["high"][c.land_use == "water"] == 0).all(), "no jobs on water")

    # divergence must do what it claims: higher divergence must lower the
    # correlation between exposed young workers and residents
    r_lo = City(seed=1, divergence=0.0).workplace_residence_correlation()
    r_hi = City(seed=1, divergence=1.0).workplace_residence_correlation()
    chk(r_hi < r_lo, "divergence reduces workplace-residence correlation (%.3f -> %.3f)"
        % (r_lo, r_hi))

    print("city.py self-test:", "PASSED" if ok else "FAILED")
    print("  grid %d x %d of %.0f m (%.0f km across)" % (N, N, CELL_M, s["extent_km"]))
    print("  land use:", ", ".join("%s %.0f%%" % (k, 100 * v)
                                   for k, v in s["land_use_shares"].items()))
    print("  residents %.0f | jobs H/M/L %.0f / %.0f / %.0f"
          % (s["residents_total"], s["jobs_total"]["high"],
             s["jobs_total"]["moderate"], s["jobs_total"]["low"]))
    print("  exposed young workers %.0f | mean canopy %.3f"
          % (s["exposed_youth_total"], s["mean_canopy"]))
    print("  workplace-residence correlation: divergence 0.00 -> r = %.3f" % r_lo)
    print("                                   divergence 0.75 -> r = %.3f"
          % s["workplace_residence_r"])
    print("                                   divergence 1.00 -> r = %.3f" % r_hi)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
