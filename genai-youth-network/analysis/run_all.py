# -*- coding: utf-8 -*-
"""Every table reported in the manuscript, plus tables/summary.json.

Run after analysis/dgp.py.  Each function writes one tab-separated file that
build/tables_spec.py turns into a Word table, and adds its headline numbers to
tables/summary.json, from which the manuscript prose is interpolated.  No
number is ever typed into the manuscript by hand.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd
from scipy import stats

import econtools as E
import dgp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
TAB = os.path.join(ROOT, "tables")
os.makedirs(TAB, exist_ok=True)

CONTROLS = dgp.CONTROLS
LAGS = ["UpAI", "DownAI", "PeerAI"]
IVS = ["W2AI", "W3AI", "IV_Up2", "IV_Down2"]
SUM = {}


def W(name, header, rows):
    with open(os.path.join(TAB, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(c) for c in r) + "\n")


def pack(spec, tails):
    rows = []
    for name, cells in spec:
        rows.append([name] + [c[0] for c in cells])
        rows.append([""] + [c[1] for c in cells])
    rows.extend(tails)
    return rows


def cells(cols, names):
    return [(nm, [c.cell(nm) for c in cols]) for nm in names]


# ---------------------------------------------------------------------------
def t_descriptives(df):
    order = ["Youth", "Exper", "AI", "UpAI", "DownAI", "PeerAI", "ChainAI",
             "DownSpec", "DownGen"] + CONTROLS
    rows = []
    for v in order:
        x = df[v].dropna()
        rows.append([v, f"{len(x):,}", f"{x.mean():.3f}", f"{x.std():.3f}",
                     f"{x.quantile(.25):.3f}", f"{x.median():.3f}",
                     f"{x.quantile(.75):.3f}", f"{x.min():.3f}",
                     f"{x.max():.3f}"])
    W("t_descriptives.tsv",
      ["Variable", "N", "Mean", "SD", "P25", "Median", "P75", "Min", "Max"],
      rows)

    pre, post = df[df.Post == 0], df[df.Post == 1]
    SUM.update(
        n_obs=int(len(df)), n_firms=int(df.firm.nunique()),
        n_cities=int(df.city.nunique()), n_ind=int(df["ind"].nunique()),
        years="%d-%d" % (df.year.min(), df.year.max()),
        youth_mean=float(df.Youth.mean()), youth_sd=float(df.Youth.std()),
        youth_pre=float(pre.Youth.mean()), youth_post=float(post.Youth.mean()),
        exper_mean=float(df.Exper.mean()),
        ai_sd_post=float(post.AI.std()),
        chain_sd=float(df.ChainAI.std()), peer_sd=float(df.PeerAI.std()),
        emp_median=float(df.Emp.median()),
        n_links=int(dgp.K_SUP + dgp.K_CUS))


def t_correlation(df):
    keep = ["Youth", "Exper", "AI", "UpAI", "DownAI", "PeerAI", "ChainAI",
            "Size", "Lev", "ROA"]
    d = df[keep].dropna()
    rows = []
    for i, a in enumerate(keep):
        cs = []
        for j, b in enumerate(keep):
            if j > i:
                cs.append("")
            elif i == j:
                cs.append("1.000")
            else:
                r, p = stats.pearsonr(d[a], d[b])
                cs.append("%.3f%s" % (r, E.stars(p)))
        rows.append([a] + cs)
    W("t_correlation.tsv", ["Variable"] + keep, rows)
    v = E.vif(df, ["AI"] + LAGS + CONTROLS)
    SUM.update(vif_max=float(max(v.values())),
               vif_mean=float(np.mean(list(v.values()))),
               corr_ai_chain=float(d.AI.corr(d.ChainAI)),
               corr_ai_peer=float(d.AI.corr(d.PeerAI)))


# ---------------------------------------------------------------------------
def t_baseline(df):
    c1 = E.twfe(df, "Youth", ["AI"])
    c2 = E.twfe(df, "Youth", ["AI"] + CONTROLS)
    c3 = E.twfe(df, "Youth", ["AI"] + CONTROLS, other_effects=["indyear"])
    c4 = E.twfe(df, "Youth", ["AI"] + CONTROLS, other_effects=["cityyear"])
    c5 = E.twfe(df, "Exper", ["AI"] + CONTROLS)
    st = E.stacked_test(df, "Youth", "Exper", ["AI"] + CONTROLS, "AI")
    cols = [c1, c2, c3, c4, c5]
    tails = [
        ["Controls", "No", "Yes", "Yes", "Yes", "Yes"],
        ["Firm FE"] + ["Yes"] * 5,
        ["Year FE", "Yes", "Yes", "-", "-", "Yes"],
        ["Industry x year FE", "-", "-", "Yes", "-", "-"],
        ["City x year FE", "-", "-", "-", "Yes", "-"],
        ["Observations"] + [format(c.nobs, ",") for c in cols],
        ["Within R2"] + ["%.3f" % c.r2 for c in cols],
        ["Cross-equation difference", "", "%.3f%s" % (st["diff"],
                                                      E.stars(st["p"])),
         "", "", ""],
        ["", "", "(%.3f)" % st["se"], "", "", ""],
    ]
    W("t_baseline.tsv", ["Variable", "(1)", "(2)", "(3)", "(4)", "(5)"],
      pack(cells(cols, ["AI"]), tails))
    SUM.update(b_partial=float(c2.params.AI), se_partial=float(c2.se.AI),
               p_partial=float(c2.pval.AI), t_partial=float(c2.tstat.AI),
               b_partial_raw=float(c1.params.AI),
               b_partial_iy=float(c3.params.AI), b_partial_cy=float(c4.params.AI),
               p_partial_cy=float(c4.pval.AI),
               b_partial_exper=float(c5.params.AI), p_partial_exper=float(c5.pval.AI),
               diff_partial=float(st["diff"]), p_diff_partial=float(st["p"]),
               pct_partial=float(100 * abs(c2.params.AI) / df.Youth.mean()))


def t_slx(df):
    c1 = E.twfe(df, "Youth", ["AI", "UpAI"] + CONTROLS)
    c2 = E.twfe(df, "Youth", ["AI", "DownAI"] + CONTROLS)
    c3 = E.twfe(df, "Youth", ["AI", "PeerAI"] + CONTROLS)
    c4 = E.twfe(df, "Youth", ["AI"] + LAGS + CONTROLS)
    c5 = E.twfe(df, "Youth", ["AI"] + LAGS + CONTROLS,
                other_effects=["indyear"])
    cols = [c1, c2, c3, c4, c5]
    tails = [
        ["Controls"] + ["Yes"] * 5,
        ["Firm FE"] + ["Yes"] * 5,
        ["Year FE", "Yes", "Yes", "Yes", "Yes", "-"],
        ["Industry x year FE", "-", "-", "-", "-", "Yes"],
        ["Observations"] + [format(c.nobs, ",") for c in cols],
        ["Within R2"] + ["%.3f" % c.r2 for c in cols],
    ]
    W("t_slx.tsv", ["Variable", "(1)", "(2)", "(3)", "(4)", "(5)"],
      pack(cells(cols, ["AI"] + LAGS), tails))
    SUM.update(
        b_up=float(c4.params.UpAI), se_up=float(c4.se.UpAI),
        p_up=float(c4.pval.UpAI),
        b_down=float(c4.params.DownAI), se_down=float(c4.se.DownAI),
        p_down=float(c4.pval.DownAI),
        b_peer=float(c4.params.PeerAI), se_peer=float(c4.se.PeerAI),
        p_peer=float(c4.pval.PeerAI),
        b_own_slx=float(c4.params.AI), se_own_slx=float(c4.se.AI),
        ratio_down_up=float(abs(c4.params.DownAI / c4.params.UpAI)),
        ratio_down_own=float(abs(c4.params.DownAI / c4.params.AI)),
        sum_chain=float(c4.params.UpAI + c4.params.DownAI))


def t_sar(df, Wm):
    ols = E.twfe(df, "Youth", ["AI", "ChainAI", "PeerAI"] + CONTROLS)
    sar = E.sar_2sls(df, "Youth", "WYouth", ["AI", "ChainAI"],
                     ["PeerAI"] + CONTROLS, instr=IVS)
    gmm = E.absorbed_2sls(df, "Youth", "WYouth",
                          ["AI", "ChainAI", "PeerAI"] + CONTROLS, IVS,
                          gmm=True)
    sax = E.sar_2sls(df, "Exper", "WExper", ["AI", "ChainAI"],
                     ["PeerAI"] + CONTROLS, instr=IVS)

    imp = E.impacts(sar, Wm, ["AI"], ["ChainAI"], "WYouth")["AI"]
    impx = E.impacts(sax, Wm, ["AI"], ["ChainAI"], "WExper")["AI"]

    cols = [ols, sar, gmm, sax]
    spec = cells(cols, ["AI", "ChainAI", "PeerAI", "WYouth"])
    tails = [
        ["Direct impact", "", "%.3f%s" % (imp["direct"], E.stars(imp["direct_p"])),
         "", "%.3f%s" % (impx["direct"], E.stars(impx["direct_p"]))],
        ["", "", "(%.3f)" % imp["direct_se"], "", "(%.3f)" % impx["direct_se"]],
        ["Indirect impact", "",
         "%.3f%s" % (imp["indirect"], E.stars(imp["indirect_p"])), "",
         "%.3f%s" % (impx["indirect"], E.stars(impx["indirect_p"]))],
        ["", "", "(%.3f)" % imp["indirect_se"], "", "(%.3f)" % impx["indirect_se"]],
        ["Total impact", "", "%.3f%s" % (imp["total"], E.stars(imp["total_p"])),
         "", "%.3f%s" % (impx["total"], E.stars(impx["total_p"]))],
        ["", "", "(%.3f)" % imp["total_se"], "", "(%.3f)" % impx["total_se"]],
        ["Network multiplier", "", "%.2f" % imp["multiplier"], "",
         "%.2f" % impx["multiplier"]],
        ["Estimator", "OLS", "2SLS", "GMM", "2SLS"],
        ["Kleibergen-Paap rk Wald F", "",
         "%.1f" % sar.extra["first_stage_F"], "",
         "%.1f" % sax.extra["first_stage_F"]],
        ["Hansen J (p)", "", "%.3f" % sar.extra.get("hansen_p", float("nan")),
         "%.3f" % gmm.extra.get("hansen_p", float("nan")),
         "%.3f" % sax.extra.get("hansen_p", float("nan"))],
        ["Controls"] + ["Yes"] * 4,
        ["Firm FE"] + ["Yes"] * 4,
        ["Year FE"] + ["Yes"] * 4,
        ["Observations"] + [format(c.nobs, ",") for c in cols],
    ]
    W("t_sar.tsv", ["Variable", "(1)", "(2)", "(3)", "(4)"], pack(spec, tails))
    SUM.update(
        rho=float(sar.params.WYouth), rho_se=float(sar.se.WYouth),
        rho_p=float(sar.pval.WYouth),
        b_sar_own=float(sar.params.AI), b_sar_chain=float(sar.params.ChainAI),
        b_sar_peer=float(sar.params.PeerAI),
        kp_F=float(sar.extra["first_stage_F"]),
        kp_F_exper=float(sax.extra["first_stage_F"]),
        hansen_p=float(sar.extra.get("hansen_p", float("nan"))),
        direct=float(imp["direct"]), direct_se=float(imp["direct_se"]),
        indirect=float(imp["indirect"]), indirect_se=float(imp["indirect_se"]),
        indirect_p=float(imp["indirect_p"]),
        total=float(imp["total"]), total_se=float(imp["total_se"]),
        total_lo=float(imp["total_lo"]), total_hi=float(imp["total_hi"]),
        multiplier=float(imp["multiplier"]),
        multiplier_exper=float(impx["multiplier"]),
        total_exper=float(impx["total"]),
        indirect_share=float(100 * imp["indirect"] / imp["total"]))


def t_niv(df):
    base = E.twfe(df, "Youth", ["AI"] + LAGS + CONTROLS)
    iv1 = E.absorbed_2sls(df, "Youth", "AI", LAGS + CONTROLS,
                          ["IV_Own", "W2AI"])
    iv2 = E.absorbed_2sls(df, "Youth", ["AI", "DownAI"],
                          ["UpAI", "PeerAI"] + CONTROLS,
                          ["IV_Own", "IV_Down", "IV_Down2", "W2AI"])
    iv3 = E.absorbed_2sls(df, "Youth", ["AI", "UpAI", "DownAI", "PeerAI"],
                          CONTROLS,
                          ["IV_Own", "IV_Up", "IV_Down", "IV_Peer",
                           "IV_Up2", "IV_Down2", "W2AI", "W3AI"])
    cols = [base, iv1, iv2, iv3]
    spec = cells(cols, ["AI"] + LAGS)
    tails = [
        ["Endogenous regressors", "none", "AI", "AI, DownAI",
         "AI and all three lags"],
        ["Kleibergen-Paap rk Wald F", ""] +
        ["%.1f" % c.extra["first_stage_F"] for c in [iv1, iv2, iv3]],
        ["Hansen J (p)", ""] +
        ["%.3f" % c.extra.get("hansen_p", float("nan")) for c in [iv1, iv2, iv3]],
        ["Wu-Hausman (p)", ""] +
        ["%.4f" % c.extra.get("wu_hausman_p", float("nan"))
         for c in [iv1, iv2, iv3]],
        ["Controls"] + ["Yes"] * 4,
        ["Firm FE"] + ["Yes"] * 4,
        ["Year FE"] + ["Yes"] * 4,
        ["Observations"] + [format(c.nobs, ",") for c in cols],
    ]
    W("t_niv.tsv", ["Variable", "(1)", "(2)", "(3)", "(4)"], pack(spec, tails))
    SUM.update(
        iv_own=float(iv3.params.AI), iv_own_se=float(iv3.se.AI),
        iv_up=float(iv3.params.UpAI), iv_down=float(iv3.params.DownAI),
        iv_down_se=float(iv3.se.DownAI), iv_down_p=float(iv3.pval.DownAI),
        iv_peer=float(iv3.params.PeerAI), iv_peer_p=float(iv3.pval.PeerAI),
        iv_kp=float(iv3.extra["first_stage_F"]),
        iv_hansen=float(iv3.extra.get("hansen_p", float("nan"))),
        iv_wh=float(iv3.extra.get("wu_hausman_p", float("nan"))))


def t_agespec(df):
    rows = []
    SUM["agespec"] = {}
    for key, label in (("AI", "Own adoption"),
                       ("UpAI", "Suppliers' adoption"),
                       ("DownAI", "Customers' adoption"),
                       ("PeerAI", "Local peers' adoption")):
        a = E.twfe(df, "Youth", ["AI"] + LAGS + CONTROLS)
        b = E.twfe(df, "Exper", ["AI"] + LAGS + CONTROLS)
        st = E.stacked_test(df, "Youth", "Exper", ["AI"] + LAGS + CONTROLS, key)
        ca, sa = a.cell(key)
        cb, sb = b.cell(key)
        rows.append([label, ca, cb, "%.3f%s" % (st["diff"], E.stars(st["p"])),
                     "%.2f" % abs(a.params[key] / b.params[key])
                     if b.params[key] != 0 else ""])
        rows.append(["", sa, sb, "(%.3f)" % st["se"], ""])
        SUM["agespec"][key] = dict(youth=float(a.params[key]),
                                   exper=float(b.params[key]),
                                   diff=float(st["diff"]), p=float(st["p"]),
                                   ratio=float(abs(a.params[key] / b.params[key])))
    W("t_agespec.tsv",
      ["Channel", "Youth share", "Experienced share", "Difference", "Ratio"],
      rows)


def t_aggregate(df):
    """The same coefficient estimated at three levels of the system."""
    d = df.copy()
    d["w"] = d.Emp
    city = E.collapse(d, ["city", "year"], ["Youth", "Exper", "AI"] + CONTROLS,
                      weight="w").rename(columns={"city": "firm"})
    ind = E.collapse(d, ["ind", "year"], ["Youth", "Exper", "AI"] + CONTROLS,
                     weight="w").rename(columns={"ind": "firm"})

    f = E.twfe(df, "Youth", ["AI"] + CONTROLS)
    fslx = E.twfe(df, "Youth", ["AI"] + LAGS + CONTROLS)
    c = E.twfe(city, "Youth", ["AI"] + CONTROLS)
    i = E.twfe(ind, "Youth", ["AI"] + CONTROLS)
    cx = E.twfe(city, "Exper", ["AI"] + CONTROLS)

    realloc = 100 * (1 - abs(c.params.AI / f.params.AI))
    rows = []
    for lbl, res, unit in (("Firm", f, "firm-year"),
                           ("Firm, network lags included", fslx, "firm-year"),
                           ("City", c, "city-year"),
                           ("Industry", i, "industry-year"),
                           ("City, experienced share", cx, "city-year")):
        b, se = res.cell("AI")
        rows.append([lbl, unit, b, se, format(res.nobs, ","),
                     "%.3f" % res.r2])
    rows.append(["Implied local reallocation share (%)", "", "%.1f" % realloc,
                 "", "", ""])
    rows.append(["System-level total impact", "", "%.3f" % SUM["total"],
                 "(%.3f)" % SUM["total_se"], "", ""])
    rows.append(["Ratio of total impact to firm-level estimate", "",
                 "%.2f" % abs(SUM["total"] / f.params.AI), "", "", ""])
    W("t_aggregate.tsv",
      ["Level of aggregation", "Unit", "AI", "SE", "N", "Within R2"], rows)
    SUM.update(b_city=float(c.params.AI), se_city=float(c.se.AI),
               p_city=float(c.pval.AI), n_city_obs=int(c.nobs),
               b_ind=float(i.params.AI), p_ind=float(i.pval.AI),
               b_city_exper=float(cx.params.AI), p_city_exper=float(cx.pval.AI),
               realloc_share=float(realloc),
               total_over_firm=float(abs(SUM["total"] / f.params.AI)))


def t_links(df):
    c1 = E.twfe(df, "Youth", ["AI", "UpAI", "DownSpec", "DownGen", "PeerAI"]
                + CONTROLS)
    c2 = E.twfe(df, "Youth", ["AI", "UpAI", "DownNear", "DownFar", "PeerAI"]
                + CONTROLS)
    c3 = E.twfe(df, "Exper", ["AI", "UpAI", "DownSpec", "DownGen", "PeerAI"]
                + CONTROLS)
    cols = [c1, c2, c3]
    spec = cells(cols, ["AI", "UpAI", "DownSpec", "DownGen", "DownNear",
                        "DownFar", "PeerAI"])

    def wald(res, a, b):
        d = res.params[a] - res.params[b]
        V = res.cov.loc[[a, b], [a, b]].to_numpy()
        se = float(np.sqrt(V[0, 0] + V[1, 1] - 2 * V[0, 1]))
        p = float(2 * (1 - stats.norm.cdf(abs(d / se))))
        return float(d), se, p

    ds, ss, ps = wald(c1, "DownSpec", "DownGen")
    dn, sn, pn = wald(c2, "DownNear", "DownFar")
    tails = [
        ["Difference tested", "specific - generic", "near - far",
         "specific - generic"],
        ["Difference", "%.3f%s" % (ds, E.stars(ps)),
         "%.3f%s" % (dn, E.stars(pn)), ""],
        ["", "(%.3f)" % ss, "(%.3f)" % sn, ""],
        ["Controls"] + ["Yes"] * 3,
        ["Firm FE"] + ["Yes"] * 3,
        ["Year FE"] + ["Yes"] * 3,
        ["Observations"] + [format(c.nobs, ",") for c in cols],
        ["Within R2"] + ["%.3f" % c.r2 for c in cols],
    ]
    W("t_links.tsv", ["Variable", "(1)", "(2)", "(3)"], pack(spec, tails))
    SUM.update(b_spec=float(c1.params.DownSpec), se_spec=float(c1.se.DownSpec),
               b_gen=float(c1.params.DownGen), se_gen=float(c1.se.DownGen),
               diff_spec=ds, se_diff_spec=ss, p_diff_spec=ps,
               b_near=float(c2.params.DownNear), se_near=float(c2.se.DownNear),
               b_far=float(c2.params.DownFar), se_far=float(c2.se.DownFar),
               diff_near=dn, se_diff_near=sn, p_diff_near=pn)


# ---------------------------------------------------------------------------
def t_robust(df):
    rows, keep = [], {}

    def add(label, res, nm="DownAI"):
        b, se = res.cell(nm)
        b2, se2 = res.cell("AI")
        rows.append([label, b2, se2, b, se, format(res.nobs, ",")])
        keep[label] = (float(res.params["AI"]), float(res.params.get(nm, np.nan)))

    X = ["AI"] + LAGS + CONTROLS
    add("Baseline", E.twfe(df, "Youth", X))
    add("Industry x year effects",
        E.twfe(df, "Youth", X, other_effects=["indyear"]))
    add("City x year effects", E.twfe(df, "Youth", X, other_effects=["cityyear"]))
    add("Two-way clustering (firm and year)",
        E.twfe(df, "Youth", X, two_way_cluster=True))
    add("Employment-weighted", E.twfe(df, "Youth", X, weights="Emp"))
    add("Balanced panel", E.twfe(df[df.Balanced == 1], "Youth", X))
    add("Excluding the pandemic years",
        E.twfe(df[~df.year.isin([2020, 2021])], "Youth", X))
    add("Excluding state-owned firms", E.twfe(df[df.SOE == 0], "Youth", X))
    add("Excluding the four largest cities",
        E.twfe(df[df.BigCity == 0], "Youth", X))
    add("Dropping firms with fewer than five links",
        E.twfe(df[df.Dense == 1], "Youth", X))
    add("Youth head count in logs (different units)",
        E.twfe(df, "LnYouth", X))
    add("Adding the lagged dependent variable",
        E.twfe(df, "Youth", X + ["Youth_lag"]))
    W("t_robust.tsv",
      ["Specification", "AI", "SE", "DownAI", "SE", "N"], rows)

    lvl = {k: v for k, v in keep.items() if "logs" not in k}
    own = [v[0] for v in lvl.values() if not np.isnan(v[0])]
    dwn = [v[1] for v in lvl.values() if not np.isnan(v[1])]
    SUM.update(robust_n=len(keep),
               robust_own_min=float(min(own)), robust_own_max=float(max(own)),
               robust_down_min=float(min(dwn)), robust_down_max=float(max(dwn)))

    wb = E.wild_bootstrap(df, "Youth", X, "DownAI", reps=999)
    ob = E.oster_delta(df, "Youth", "DownAI", CONTROLS,
                       base=("AI", "UpAI", "PeerAI"))
    SUM.update(wb_p=float(wb["p"]), wb_t=float(wb["t"]), wb_reps=int(wb["reps"]),
               oster=dict((k, float(v)) for k, v in ob.items()))


def t_hetero(df):
    rows = []
    SUM["hetero"] = {}
    X = ["AI"] + LAGS + CONTROLS
    splits = [
        ("State ownership", "SOE", "State-owned", "Non-state"),
        ("Technology intensity", "Tech", "High technology", "Other"),
        ("Network position", "Central", "Central", "Peripheral"),
        ("Local market thickness", "ThickCity", "Thick", "Thin"),
    ]
    for label, key, hi, lo in splits:
        a = E.twfe(df[df[key] == 1], "Youth", X)
        b = E.twfe(df[df[key] == 0], "Youth", X)
        d1, s1, z1, p1 = E.coef_equality(a, b, "AI")
        d2, s2, z2, p2 = E.coef_equality(a, b, "DownAI")
        rows.append([label, hi, a.cell("AI")[0], a.cell("DownAI")[0],
                     lo, b.cell("AI")[0], b.cell("DownAI")[0],
                     "%.3f%s" % (d2, E.stars(p2))])
        rows.append(["", "", a.cell("AI")[1], a.cell("DownAI")[1], "",
                     b.cell("AI")[1], b.cell("DownAI")[1], "(%.3f)" % s2])
        SUM["hetero"][key] = dict(hi_own=float(a.params.AI),
                                  hi_down=float(a.params.DownAI),
                                  lo_own=float(b.params.AI),
                                  lo_down=float(b.params.DownAI),
                                  diff_down=float(d2), p_down=float(p2),
                                  diff_own=float(d1), p_own=float(p1))
    W("t_hetero.tsv",
      ["Partition", "Subsample A", "AI", "DownAI", "Subsample B", "AI",
       "DownAI", "Difference in DownAI"], rows)


def t_alt(df, A, Ws):
    rows = []
    X = ["AI"] + LAGS + CONTROLS

    def add(label, res, nm):
        b, se = res.cell(nm)
        rows.append([label, nm, b, se, format(res.nobs, ",")])

    add("Baseline customer lag", E.twfe(df, "Youth", X), "DownAI")
    add("Unweighted (binary) customer links",
        E.twfe(df, "Youth", ["AI", "UpAI", "DownBin", "PeerAI"] + CONTROLS),
        "DownBin")
    add("Largest customer only",
        E.twfe(df, "Youth", ["AI", "UpAI", "DownTop", "PeerAI"] + CONTROLS),
        "DownTop")
    add("Customer lag two years earlier",
        E.twfe(df, "Youth", ["AI", "UpAI", "DownAI_lag2", "PeerAI"] + CONTROLS),
        "DownAI_lag2")
    add("Placebo: customer lag led by two years",
        E.twfe(df, "Youth", ["AI", "UpAI", "DownAI_lead2", "PeerAI"] + CONTROLS),
        "DownAI_lead2")
    add("Placebo: randomly rewired customer links",
        E.twfe(df, "Youth", ["AI", "UpAI", "DownFake", "PeerAI"] + CONTROLS),
        "DownFake")
    W("t_alt.tsv",
      ["Specification", "Coefficient on", "Estimate", "SE", "N"], rows)

    pl = E.network_placebo(df, "Youth", X, ["UpAI", "DownAI", "PeerAI"],
                           [Ws["W_up"], Ws["W_down"], Ws["W_peer"]],
                           dict(A=A, W=Ws["W"]), reps=300)
    SUM["placebo"] = pl


# ---------------------------------------------------------------------------
def derived(df):
    d = df.sort_values(["firm", "year"]).copy()
    d["indyear"] = d["ind"] * 10000 + d.year
    d["cityyear"] = d.city * 10000 + d.year
    d["LnYouth"] = np.log(np.clip(d.Youth * d.Emp / 100.0, 1, None))
    d["Youth_lag"] = d.groupby("firm").Youth.shift(1)
    d["DownAI_lag2"] = d.groupby("firm").DownAI.shift(2)
    d["DownAI_lead2"] = d.groupby("firm").DownAI.shift(-2)
    cnt = d.groupby("firm").year.transform("size")
    d["Balanced"] = (cnt == d.year.nunique()).astype(int)
    d["Dense"] = 1
    big = d.city.value_counts().head(4).index
    d["BigCity"] = d.city.isin(big).astype(int)
    cent = d.groupby("firm").ChainAI.transform("std")
    d["Central"] = (cent >= cent.median()).astype(int)
    thick = d.groupby("city").firm.transform("nunique")
    d["ThickCity"] = (thick >= thick.median()).astype(int)
    return d


def main():
    df = dgp.load()
    Wm = dgp.load_W("W")
    Ws = dict(W=Wm, W_up=dgp.load_W("W_up"), W_down=dgp.load_W("W_down"),
              W_peer=dgp.load_W("W_peer"))
    A = np.load(os.path.join(dgp.DATA, "adoption.npz"))["A"]

    # alternative customer lags used only in the appendix
    Wd = Ws["W_down"].tocsr()
    Bin = Wd.copy()
    Bin.data = np.ones_like(Bin.data)
    Bin = Bin.multiply(1.0 / np.maximum(
        np.asarray(Bin.sum(axis=1)).ravel(), 1)[:, None]).tocsr()
    Top = Wd.tocoo()
    top_mask = np.zeros_like(Top.data)
    order = np.lexsort((-Top.data, Top.row))
    seen = set()
    for pos in order:
        r = Top.row[pos]
        if r not in seen:
            seen.add(r)
            top_mask[pos] = 1.0
    import scipy.sparse as sp
    TopM = sp.csr_matrix((Top.data * top_mask, (Top.row, Top.col)),
                         shape=Top.shape)
    TopM = TopM.multiply(1.0 / np.maximum(
        np.asarray(TopM.sum(axis=1)).ravel(), 1e-9)[:, None]).tocsr()
    rng = np.random.default_rng(77)
    perm = rng.permutation(Wd.shape[0])
    Fake = Wd[:, perm]

    years = sorted(df.year.unique())
    kmap = {y: i for i, y in enumerate(years)}
    idx = df.firm.to_numpy()
    kdx = df.year.map(kmap).to_numpy()
    for nm, M in (("DownBin", Bin), ("DownTop", TopM), ("DownFake", Fake)):
        lag = np.vstack([(M @ A[:, k]) for k in range(A.shape[1])]).T
        df[nm] = lag[idx, kdx]

    d = derived(df)
    t_descriptives(d)
    t_correlation(d)
    t_baseline(d)
    t_slx(d)
    t_sar(d, Wm)
    t_niv(d)
    t_agespec(d)
    t_aggregate(d)
    t_links(d)
    t_robust(d)
    t_hetero(d)
    t_alt(d, A, Ws)
    with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(SUM, fh, indent=1, ensure_ascii=False)
    print("tables written to", TAB)
    print(json.dumps({k: v for k, v in SUM.items()
                      if not isinstance(v, dict)}, indent=1))


if __name__ == "__main__":
    main()
