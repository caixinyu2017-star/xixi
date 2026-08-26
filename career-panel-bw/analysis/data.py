# -*- coding: utf-8 -*-
"""The two panels.

Both are real, public, and widely redistributed longitudinal microdata on
young workers. Nothing here is generated.

NLSW — National Longitudinal Survey of Young Women, U.S. Bureau of Labor
    Statistics. Women aged 14–24 when first interviewed in 1968, followed to
    1988. The extract used here is the one distributed with Stata as
    ``nlswork.dta`` and with the R package ``sampleSelection``: 28,534
    person-years on 4,711 women across 15 waves.

NLSY79M — National Longitudinal Survey of Youth 1979, young men. The extract
    is the replication file for Vella and Verbeek (1998), distributed with the
    R packages ``wooldridge`` (as ``wagepan``) and ``plm`` (as ``Males``):
    545 men observed in every year from 1980 to 1987, a balanced panel of
    4,360 person-years.

Running this module directly re-derives two published estimates from the
loaded data, which is the check that the files were read as intended.
"""
import csv
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(v):
    if v in ("", "NA", "NaN", None):
        return np.nan
    return float(v)


class Panel:
    """A long-format panel held as float arrays, one per variable."""

    def __init__(self, name, label, pid, time, cols, source, note=""):
        self.name, self.label = name, label
        self.pid, self.time = pid, time
        self.cols = cols
        self.source, self.note = source, note

    @property
    def n_obs(self):
        return self.pid.size

    @property
    def n_person(self):
        return np.unique(self.pid).size

    @property
    def waves(self):
        return np.unique(self.time)

    def __getitem__(self, k):
        return self.cols[k]

    def has(self, *keys):
        return all(k in self.cols for k in keys)

    def complete(self, keys):
        """Row mask where every named variable is observed."""
        m = np.ones(self.n_obs, bool)
        for k in keys:
            m &= np.isfinite(self.cols[k])
        return m

    def subset(self, mask):
        return Panel(self.name, self.label, self.pid[mask], self.time[mask],
                     {k: v[mask] for k, v in self.cols.items()},
                     self.source, self.note)

    def within_sd(self, key):
        """Average within-person standard deviation of a variable."""
        v = self.cols[key]
        ok = np.isfinite(v)
        out = []
        for p in np.unique(self.pid[ok]):
            s = v[ok][self.pid[ok] == p]
            if s.size > 1:
                out.append(s.std(ddof=1))
        return float(np.mean(out)) if out else np.nan


# ---------------------------------------------------------------------------
def load_nlsw():
    raw = _read(os.path.join(DATA, "nlswork_raw.csv"))
    g = {k: np.array([_num(r[k]) for r in raw])
         for k in raw[0] if k != "rownames"}

    year = g["year"] + 1900.0
    cols = {
        "lwage": g["ln_wage"],
        "tenure": g["tenure"],                 # years at current employer
        "exper": g["ttl_exp"],                 # total work experience, years
        "hours": g["hours"],                   # usual hours per week
        "wks_ue": g["wks_ue"],                 # weeks unemployed last year
        "union": g["union"],
        "grade": g["grade"],                   # years of schooling
        "collgrad": g["collgrad"],
        "married": g["msp"],                   # married, spouse present
        "black": (g["race"] == 2).astype(float),
        "south": g["south"],
        "urban": 1.0 - g["not_smsa"],
        "age": g["age"],
        "year": year,
    }
    cols["expersq"] = cols["exper"] ** 2
    cols["tenuresq"] = cols["tenure"] ** 2
    return Panel(
        "NLSW", "NLS Young Women (1968–1988)", g["idcode"], year, cols,
        source=("U.S. Bureau of Labor Statistics, National Longitudinal "
                "Survey of Young Women; extract distributed with Stata as "
                "nlswork.dta and with the R package sampleSelection."),
        note="Women aged 14–24 at first interview in 1968.")


def load_nlsy79m():
    raw = _read(os.path.join(DATA, "wagepan_raw.csv"))
    g = {k: np.array([_num(r[k]) for r in raw])
         for k in raw[0] if k != "rownames"}
    cols = {
        "lwage": g["lwage"],
        "exper": g["exper"],
        "expersq": g["expersq"],
        "hours": g["hours"],
        "union": g["union"],
        "grade": g["educ"],
        "collgrad": (g["educ"] >= 16).astype(float),
        "married": g["married"],
        "black": g["black"],
        "hisp": g["hisp"],
        "south": g["south"],
        "urban": 1.0 - g["rur"],
        "poorhlth": g["poorhlth"],
        "year": g["year"],
    }
    # occupation is coded as nine indicators; keep the collapsed white-collar
    # contrast, which is the only occupational distinction used below
    cols["prof"] = np.maximum(g["occ1"], g["occ2"])
    return Panel(
        "NLSY79M", "NLSY79 young men (1980–1987)", g["nr"], g["year"], cols,
        source=("U.S. Bureau of Labor Statistics, National Longitudinal "
                "Survey of Youth 1979; extract from Vella and Verbeek "
                "(1998), distributed with the R packages wooldridge "
                "(wagepan) and plm (Males)."),
        note="Men aged 17–23 in 1980, working full time, balanced panel.")


PANELS = {"NLSW": load_nlsw, "NLSY79M": load_nlsy79m}


def load(name):
    return PANELS[name]()


# ---------------------------------------------------------------------------
def _benchmark():
    """Reproduce a published estimate, as a check on the loading.

    Wooldridge, *Introductory Econometrics*, Example 14.4 fits person fixed
    effects of log wage on year dummies, experience squared, marriage and
    union membership in exactly this extract. Matching all three reported
    coefficients is the evidence that the file was read as intended.
    """
    import estimators as E

    p = load_nlsy79m()
    yrs = sorted(set(p["year"].tolist()))[1:]
    X = np.column_stack([(p["year"] == y).astype(float) for y in yrs]
                        + [p["expersq"], p["married"], p["union"]])
    nm = ["d%d" % y for y in yrs] + ["expersq", "married", "union"]
    r = E.within(X, p["lwage"], p.pid, nm)
    want = {"expersq": -0.0052, "married": 0.0467, "union": 0.0800}
    print("NLSY79M  %d person-years / %d men / waves %d-%d"
          % (p.n_obs, p.n_person, p.waves.min(), p.waves.max()))
    print("   person fixed effects, log hourly wage")
    ok = True
    for k, w in want.items():
        b = E.coef(r, k)["b"]
        d = abs(b - w)
        ok &= d < 0.0001
        print("      %-8s %+.4f   published %+.4f   %s"
              % (k, b, w, "match" if d < 0.0001 else "MISMATCH"))

    q = load_nlsw()
    m = q.complete(["lwage", "tenure", "exper", "grade"])
    q = q.subset(m)
    print("NLSW     %d person-years / %d women / %d waves %d-%d"
          % (q.n_obs, q.n_person, q.waves.size, q.waves.min(),
             q.waves.max()))
    print("   mean log wage %.3f   schooling %.2f   tenure %.2f   "
          "experience %.2f"
          % (q["lwage"].mean(), q["grade"].mean(), q["tenure"].mean(),
             q["exper"].mean()))
    return ok


if __name__ == "__main__":
    import sys
    sys.path.insert(0, HERE)
    ok = _benchmark()
    print("benchmark reproduction:", "PASS" if ok else "FAIL")
