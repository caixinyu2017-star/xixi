# -*- coding: utf-8 -*-
"""Every estimate reported in the manuscript.

Writes one tab-separated file per table into ``tables/`` and a single
``tables/summary.json`` holding every number the prose interpolates, so the
text cannot drift away from the estimates.
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import pandas as pd

import econtools as E

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
TAB = os.path.join(ROOT, "tables")
os.makedirs(TAB, exist_ok=True)

CTRL = ["Size", "Lev", "ROA", "Cashflow", "TobinQ", "Top1", "Indep", "Dual",
        "Board", "CapInt", "Emp"]
MAIN = ["Youth", "Variety", "RelVar", "UnrelVar", "Shock", "Redeploy",
        "Churn", "Digital", "Slack"]

LABEL = {
    "Youth": "Youth", "Exper": "Exper", "Variety": "Variety",
    "RelVar": "RelVar", "UnrelVar": "UnrelVar", "Shock": "Shock",
    "SxV": "Shock x Variety", "SxR": "Shock x RelVar",
    "SxU": "Shock x UnrelVar", "Redeploy": "Redeploy", "Churn": "Churn",
    "Digital": "Digital", "Slack": "Slack",
    "Digital_z": "Digital", "Slack_z": "Slack",
    "SxD": "Shock x Digital", "VxD": "Variety x Digital",
    "SxVxD": "Shock x Variety x Digital",
    "SxS": "Shock x Slack", "VxS": "Variety x Slack",
    "SxVxS": "Shock x Variety x Slack",
    "Size": "Size", "Lev": "Lev", "ROA": "ROA", "Cashflow": "Cashflow",
    "TobinQ": "TobinQ", "Top1": "Top1", "Indep": "Indep", "Dual": "Dual",
    "Board": "Board", "CapInt": "CapInt", "Emp": "Emp",
    "CityDiv": "CityDiv", "PeerVar": "PeerVar", "SxC": "Shock x CityDiv",
    "SxP": "Shock x PeerVar", "Variety_L1": "L.Variety",
    "SxV_L1": "L.(Shock x Variety)",
    "Shock_low": "Shock (Variety <= gamma)",
    "Shock_high": "Shock (Variety > gamma)",
}

S: dict = {}


def w(name, rows, header):
    path = os.path.join(TAB, name + ".tsv")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join("" if c is None else str(c) for c in r) + "\n")
    print("  wrote", name, "(%d rows)" % len(rows))


def stack(results, names, tail_rows):
    rows = []
    for nm in names:
        line_b, line_s = [LABEL.get(nm, nm)], [""]
        for r in results:
            b, se = r.cell(nm) if r is not None else ("", "")
            line_b.append(b)
            line_s.append(se)
        if any(x for x in line_b[1:]):
            rows.append(line_b)
            rows.append(line_s)
    rows.extend(tail_rows)
    return rows


def tail(results, extra=None):
    rows = [["Year FE"] + ["YES"] * len(results),
            ["Firm FE"] + ["YES"] * len(results)]
    if extra:
        rows.extend(extra)
    rows.append(["Observations"] + ["{:,}".format(r.nobs) for r in results])
    rows.append(["R-squared"] + ["%.3f" % r.r2 for r in results])
    return rows


def buffer_mediation(d, med, n_boot=400, seed=17):
    """Share of the buffering coefficient that passes through a mediator.

    The a-path is the coefficient on Shock x Variety in the mediator equation
    and the b-path is the coefficient on the mediator in the outcome equation
    that also contains Shock x Variety, so their product is the part of the
    buffering effect that travels through the mediator. The confidence
    interval comes from a bootstrap that resamples whole firms.
    """
    xs = ["Variety", "Shock", "SxV"] + CTRL
    s_tot = E.twfe(d, "Youth", xs)
    s_a = E.twfe(d, med, xs)
    s_b = E.twfe(d, "Youth", ["Variety", "Shock", "SxV", med] + CTRL)
    a, b = float(s_a.params["SxV"]), float(s_b.params[med])
    point = a * b
    tot = float(s_tot.params["SxV"])

    cols = ["Youth", med, "SxV", "Variety", "Shock"] + CTRL
    base = d[cols].to_numpy(float)
    fcodes = pd.factorize(d.firm.to_numpy())[0]
    tcodes = pd.factorize(d.year.to_numpy())[0]
    order = np.argsort(fcodes, kind="stable")
    n_units = fcodes.max() + 1
    lo = np.searchsorted(fcodes[order], np.arange(n_units))
    hi = np.searchsorted(fcodes[order], np.arange(n_units), side="right")
    blocks = [order[i:j] for i, j in zip(lo, hi)]
    sizes = np.array([blk.size for blk in blocks])

    rng = np.random.default_rng(seed)
    draws = np.empty(n_boot)
    for r in range(n_boot):
        pick = rng.integers(0, n_units, n_units)
        idx = np.concatenate([blocks[p] for p in pick])
        M = base[idx]
        fid = np.repeat(np.arange(n_units), sizes[pick])
        W = E._fast_within(M, fid, tcodes[idx])
        # a-path: mediator on SxV, Variety, Shock and controls
        aa = np.linalg.lstsq(W[:, 2:], W[:, 1], rcond=None)[0][0]
        # b-path: outcome on mediator, SxV, Variety, Shock and controls
        bb = np.linalg.lstsq(W[:, 1:], W[:, 0], rcond=None)[0][0]
        draws[r] = aa * bb
    ci = np.percentile(draws, [2.5, 97.5])
    return dict(total=tot, a=a, se_a=float(s_a.se["SxV"]),
                p_a=float(s_a.pval["SxV"]), b=b, se_b=float(s_b.se[med]),
                p_b=float(s_b.pval[med]),
                direct=float(s_b.params["SxV"]),
                p_direct=float(s_b.pval["SxV"]),
                indirect=point, ci_low=float(ci[0]), ci_high=float(ci[1]),
                share=float(100 * point / tot), n_boot=int(n_boot))


# ===========================================================================
def main():
    d = pd.read_csv(os.path.join(ROOT, "data", "panel.csv"))
    d["indyear"] = d.ind * 100 + d.year
    d["provyear"] = d.prov * 100 + d.year
    d["Variety_L1"] = d.groupby("firm").Variety.shift(1)
    d["SxV_L1"] = d.Shock * d.Variety_L1

    S["n_obs"] = int(len(d))
    S["n_firms"] = int(d.firm.nunique())
    S["n_ind"] = int(d.ind.nunique())
    S["n_prov"] = int(d.prov.nunique())
    S["n_city"] = int(d.city.nunique())
    S["y0"], S["y1"] = int(d.year.min()), int(d.year.max())
    S["years"] = "%d-%d" % (S["y0"], S["y1"])

    # ------------------------------------------------- Table 2 descriptives
    print("Table 2 descriptive statistics")
    rows = []
    for c in MAIN + CTRL:
        v = d[c]
        rows.append([LABEL[c], "{:,}".format(int(v.notna().sum())),
                     "%.3f" % v.mean(), "%.3f" % v.std(), "%.3f" % v.min(),
                     "%.3f" % v.quantile(0.5), "%.3f" % v.max()])
    w("t02_descriptives", rows,
      ["Variable", "N", "Mean", "S.D.", "Min", "Median", "Max"])
    for c in MAIN:
        S["mean_" + c] = float(d[c].mean())
        S["sd_" + c] = float(d[c].std())
    S["max_entropy"] = float(np.log2(15))
    S["shock_2020"] = float(d[d.year == 2020].Shock.mean())
    S["shock_2022"] = float(d[d.year == 2022].Shock.mean())
    S["shock_2015"] = float(d[d.year == 2015].Shock.mean())
    S["shock_2021"] = float(d[d.year == 2021].Shock.mean())

    # ------------------------------------- Table 3 correlations and the VIF
    print("Table 3 correlations and VIF")
    cols = MAIN + CTRL
    C = d[cols].corr(method="pearson")
    vmap = E.vif(d, ["Variety", "Shock", "SxV"] + CTRL)
    rows = []
    for i, a in enumerate(cols):
        line = [LABEL[a]]
        for j in range(len(cols)):
            line.append("%.3f" % C.iloc[i, j] if j <= i else "")
        line.append("%.2f" % vmap[a] if a in vmap else "")
        rows.append(line)
    w("t03_correlation", rows,
      ["Variable"] + [LABEL[c] for c in cols] + ["VIF"])
    S["vif_max"] = float(max(vmap.values()))
    S["corr_vy"] = float(C.loc["Variety", "Youth"])
    S["corr_sy"] = float(C.loc["Shock", "Youth"])
    S["corr_ru"] = float(C.loc["RelVar", "UnrelVar"])

    # -------------------------------------------- Table 4 benchmark: variety
    print("Table 4 benchmark")
    r1 = E.twfe(d, "Youth", ["Variety"], time_effects=False)
    r2 = E.twfe(d, "Youth", ["Variety"])
    r3 = E.twfe(d, "Youth", ["Variety"] + CTRL)
    r4 = E.twfe(d, "Youth", ["Variety"] + CTRL, other_effects=["indyear"])
    r5 = E.twfe(d, "Youth", ["Variety"] + CTRL, other_effects=["provyear"])
    res = [r1, r2, r3, r4, r5]
    rows = stack(res, ["Variety"] + CTRL, [])
    rows += [["Year FE", "NO", "YES", "YES", "--", "--"],
             ["Firm FE", "YES", "YES", "YES", "YES", "YES"],
             ["Industry x Year FE", "NO", "NO", "NO", "YES", "NO"],
             ["Province x Year FE", "NO", "NO", "NO", "NO", "YES"],
             ["Observations"] + ["{:,}".format(r.nobs) for r in res],
             ["R-squared"] + ["%.3f" % r.r2 for r in res]]
    w("t04_benchmark", rows, ["Variable", "(1)", "(2)", "(3)", "(4)", "(5)"])
    S["b_var"] = float(r3.params["Variety"])
    S["se_var"] = float(r3.se["Variety"])
    S["t_var"] = float(r3.tstat["Variety"])
    S["r2_var"] = float(r3.r2)
    S["b_var_ind"] = float(r4.params["Variety"])
    S["b_var_prov"] = float(r5.params["Variety"])
    S["var_sd_effect"] = float(S["b_var"] * S["sd_Variety"])
    S["var_sd_pct"] = float(100 * S["var_sd_effect"] / S["mean_Youth"])

    # ---------------------------------------------- Table 5 the buffer
    print("Table 5 buffering")
    q1 = E.twfe(d, "Youth", ["Shock"] + CTRL)
    q2 = E.twfe(d, "Youth", ["Shock", "Variety"] + CTRL)
    q3 = E.twfe(d, "Youth", ["Variety", "Shock", "SxV"] + CTRL)
    q4 = E.twfe(d, "Youth", ["Variety", "Shock", "SxV"] + CTRL,
                other_effects=["indyear"])
    q5 = E.twfe(d, "Youth", ["Variety", "Shock", "SxV"] + CTRL,
                other_effects=["provyear"])
    res = [q1, q2, q3, q4, q5]
    rows = stack(res, ["Shock", "Variety", "SxV"] + CTRL, [])
    rows += [["Year FE", "YES", "YES", "YES", "--", "--"],
             ["Firm FE", "YES", "YES", "YES", "YES", "YES"],
             ["Industry x Year FE", "NO", "NO", "NO", "YES", "NO"],
             ["Province x Year FE", "NO", "NO", "NO", "NO", "YES"],
             ["Observations"] + ["{:,}".format(r.nobs) for r in res],
             ["R-squared"] + ["%.3f" % r.r2 for r in res]]
    w("t05_buffer", rows, ["Variable", "(1)", "(2)", "(3)", "(4)", "(5)"])
    S["b_shock_alone"] = float(q1.params["Shock"])
    S["b_shock"] = float(q3.params["Shock"])
    S["b_sxv"] = float(q3.params["SxV"])
    S["se_sxv"] = float(q3.se["SxV"])
    S["t_sxv"] = float(q3.tstat["SxV"])
    S["r2_buffer"] = float(q3.r2)
    S["b_sxv_ind"] = float(q4.params["SxV"])
    S["b_sxv_prov"] = float(q5.params["SxV"])

    vbar, vsd = S["mean_Variety"], S["sd_Variety"]
    zs = list(np.linspace(d.Variety.quantile(0.02), d.Variety.quantile(0.98),
                          41))
    S["margin_variety"] = E.margin(q3, "Shock", "SxV", zs)
    for tag, z in (("mean", vbar), ("lo", vbar - vsd), ("hi", vbar + vsd)):
        m = E.margin(q3, "Shock", "SxV", [z])[0]
        S["marg_" + tag] = float(m["effect"])
        S["marg_" + tag + "_p"] = float(m["p"])
    S["zero_variety"] = float(-q3.params["Shock"] / q3.params["SxV"])

    # -------------------------------- Table 6 related and unrelated variety
    print("Table 6 variety decomposition")
    g1 = E.twfe(d, "Youth", ["RelVar", "Shock", "SxR"] + CTRL)
    g2 = E.twfe(d, "Youth", ["UnrelVar", "Shock", "SxU"] + CTRL)
    g3 = E.twfe(d, "Youth", ["RelVar", "UnrelVar", "Shock", "SxR", "SxU"]
                + CTRL)
    res = [g1, g2, g3]
    rows = stack(res, ["Shock", "RelVar", "UnrelVar", "SxR", "SxU"] + CTRL,
                 tail(res))
    w("t06_decomposition", rows, ["Variable", "(1)", "(2)", "(3)"])
    S["b_sxr"] = float(g3.params["SxR"])
    S["b_sxu"] = float(g3.params["SxU"])
    S["p_sxr"] = float(g3.pval["SxR"])
    S["p_sxu"] = float(g3.pval["SxU"])
    dif = g3.params["SxR"] - g3.params["SxU"]
    Vd = g3.cov.loc[["SxR", "SxU"], ["SxR", "SxU"]].to_numpy(float)
    sed = float(np.sqrt(Vd[0, 0] + Vd[1, 1] - 2 * Vd[0, 1]))
    from scipy import stats as _st
    S["diff_ru"] = float(dif)
    S["se_diff_ru"] = sed
    S["p_diff_ru"] = float(2 * (1 - _st.norm.cdf(abs(dif / sed))))
    S["ratio_ru"] = float(S["b_sxr"] / S["b_sxu"])
    rb_, ub_ = d.RelVar.mean(), d.UnrelVar.mean()
    rs_, us_ = d.RelVar.std(), d.UnrelVar.std()
    zz = np.linspace(-2, 2, 41)
    S["margin_rel"] = [dict(z=float(t_), **{k: v for k, v in m.items()
                                            if k != "z"})
                       for t_, m in zip(zz, E.margin(g1, "Shock", "SxR",
                                                     rb_ + zz * rs_))]
    S["margin_unrel"] = [dict(z=float(t_), **{k: v for k, v in m.items()
                                              if k != "z"})
                         for t_, m in zip(zz, E.margin(g2, "Shock", "SxU",
                                                       ub_ + zz * us_))]

    # ----------------------------------------------- Table 7 the mechanism
    print("Table 7 mechanism")
    h1 = E.twfe(d, "Redeploy", ["Variety", "Shock", "SxV"] + CTRL)
    h2 = E.twfe(d, "Churn", ["Variety", "Shock", "SxV"] + CTRL)
    h3 = E.twfe(d, "Youth", ["Variety", "Shock", "SxV", "Redeploy"] + CTRL)
    h4 = E.twfe(d, "Youth", ["Variety", "Shock", "SxV", "Churn"] + CTRL)
    h5 = E.twfe(d, "Youth",
                ["Variety", "Shock", "SxV", "Redeploy", "Churn"] + CTRL)
    res = [q3, h1, h3, h2, h4, h5]
    rows = stack(res, ["Shock", "Variety", "SxV", "Redeploy", "Churn"] + CTRL,
                 tail(res))
    w("t07_mechanism", rows,
      ["Variable", "Youth (1)", "Redeploy (2)", "Youth (3)", "Churn (4)",
       "Youth (5)", "Youth (6)"])

    med = {}
    rows = []
    for key, nm in (("Redeploy", "Internal redeployment"),
                    ("Churn", "Workforce churn")):
        m = buffer_mediation(d, key, n_boot=400)
        med[key] = m
        rows.append([nm, "%.3f%s" % (m["total"], E.stars(0.0)),
                     "%.3f%s" % (m["a"], E.stars(m["p_a"])),
                     "%.3f%s" % (m["b"], E.stars(m["p_b"])),
                     "%.3f%s" % (m["direct"], E.stars(m["p_direct"])),
                     "%.3f" % m["indirect"],
                     "[%.3f, %.3f]" % (m["ci_low"], m["ci_high"]),
                     "%.1f" % m["share"]])
    w("t08_indirect", rows,
      ["Mediator", "Buffering effect", "Path a", "Path b", "Direct",
       "Indirect", "95% bootstrap CI", "Share (%)"])
    S["med"] = {k: {kk: vv for kk, vv in v.items()} for k, v in med.items()}
    S["share_red"] = float(med["Redeploy"]["share"])
    S["share_chu"] = float(med["Churn"]["share"])
    S["share_both"] = S["share_red"] + S["share_chu"]

    # -------------------------------------------- Table 9 endogeneity tests
    print("Table 9 endogeneity")
    iv = E.absorbed_2sls(d, "Youth", ["Variety", "SxV"], ["Shock"] + CTRL,
                         ["CityDiv", "SxC", "PeerVar", "SxP"])
    fs = iv.extra["first_stage_all"]
    dl = d.dropna(subset=["Variety_L1"])
    lag = E.twfe(dl, "Youth", ["Variety_L1", "Shock", "SxV_L1"] + CTRL)

    dm = d.copy()
    dm["Post"] = (dm.year >= 2020).astype(int)
    pre = dm[dm.year < 2020].groupby("firm").Variety.mean()
    dm["Treat"] = dm.firm.map((pre >= pre.median()).astype(int)).fillna(0)
    dm["Treat"] = dm["Treat"].astype(int)
    matched, bal, _ = E.psm(dm, ["Size", "Lev", "ROA", "TobinQ", "Top1",
                                 "CapInt", "Emp"], treat="Treat",
                            caliper=0.05, k=1)
    psm_r = E.twfe(matched, "Youth", ["Variety", "Shock", "SxV"] + CTRL)
    eb = E.entropy_balance(dm, ["Size", "Lev", "ROA", "TobinQ", "Top1",
                                "CapInt", "Emp"], treat="Treat")
    eb_r = E.twfe(eb, "Youth", ["Variety", "Shock", "SxV"] + CTRL,
                  weights="ebw")

    rows = []
    for nm in ["CityDiv", "SxC", "PeerVar", "SxP", "Variety", "SxV",
               "Variety_L1", "SxV_L1"]:
        line_b, line_s = [LABEL[nm]], [""]
        for which in ("Variety", "SxV"):
            if nm in fs[which]:
                b, se, p = fs[which][nm]
                line_b.append("%.3f%s" % (b, E.stars(p)))
                line_s.append("(%.3f)" % se)
            else:
                line_b.append("")
                line_s.append("")
        for r, keys in ((iv, ("Variety", "SxV")),
                        (lag, ("Variety_L1", "SxV_L1")),
                        (psm_r, ("Variety", "SxV")),
                        (eb_r, ("Variety", "SxV"))):
            if nm in keys:
                b, se = r.cell(nm)
                line_b.append(b)
                line_s.append(se)
            else:
                line_b.append("")
                line_s.append("")
        if any(x for x in line_b[1:]):
            rows.append(line_b)
            rows.append(line_s)
    rows.append(["Controls"] + ["YES"] * 6)
    rows.append(["Year FE"] + ["YES"] * 6)
    rows.append(["Firm FE"] + ["YES"] * 6)
    rows.append(["Kleibergen-Paap rk F", "", "",
                 "%.1f" % iv.extra["first_stage_F"], "", "", ""])
    rows.append(["Hansen J (p-value)", "", "",
                 "%.3f (%.3f)" % (iv.extra["hansen_J"],
                                  iv.extra["hansen_p"]), "", "", ""])
    rows.append(["Durbin-Wu-Hausman (p-value)", "", "",
                 "%.3f" % iv.extra["wu_hausman_p"], "", "", ""])
    rows.append(["Observations", "{:,}".format(iv.nobs),
                 "{:,}".format(iv.nobs), "{:,}".format(iv.nobs),
                 "{:,}".format(lag.nobs), "{:,}".format(psm_r.nobs),
                 "{:,}".format(eb_r.nobs)])
    w("t09_endogeneity", rows,
      ["Variable", "(1) First stage: Variety",
       "(2) First stage: Shock x Variety", "(3) 2SLS", "(4) Lagged variety",
       "(5) PSM sample", "(6) Entropy balancing"])
    S["b_iv_var"] = float(iv.params["Variety"])
    S["b_iv_sxv"] = float(iv.params["SxV"])
    S["kp_f"] = float(iv.extra["first_stage_F"])
    S["hansen_p"] = float(iv.extra["hansen_p"])
    S["wu_p"] = float(iv.extra["wu_hausman_p"])
    S["b_lag_sxv"] = float(lag.params["SxV_L1"])
    S["b_psm_sxv"] = float(psm_r.params["SxV"])
    S["b_eb_sxv"] = float(eb_r.params["SxV"])
    S["n_psm"] = int(psm_r.nobs)
    S["bal_before"] = float(bal.bias_u.abs().max())
    S["bal_after"] = float(bal.bias_m.abs().max())

    # ------------------------------------------ Table 10 robustness checks
    print("Table 10 robustness")
    d_alt = d.copy()
    P = d_alt[["Variety"]].copy()
    d_alt["VarHHI"] = 2.0 ** d_alt.Variety            # effective number index
    d_alt["SxHHI"] = d_alt.Shock * d_alt.VarHHI
    d_alt["ShockBin"] = (d_alt.Shock > 0).astype(float)
    d_alt["SxVbin"] = d_alt.ShockBin * d_alt.Variety
    d_alt["Youth_alt"] = 100.0 * d_alt.Youth / (d_alt.Youth + d_alt.Exper)
    rb = [
        ("Excluding the pandemic years 2020 and 2021",
         E.twfe(d[~d.year.isin([2020, 2021])], "Youth",
                ["Variety", "Shock", "SxV"] + CTRL), "SxV"),
        ("Balanced panel only",
         E.twfe(d[d.firm.isin(d.groupby("firm").size()
                              .loc[lambda s: s == s.max()].index)],
                "Youth", ["Variety", "Shock", "SxV"] + CTRL), "SxV"),
        ("Effective number of skill groups in place of the entropy",
         E.twfe(d_alt, "Youth", ["VarHHI", "Shock", "SxHHI"] + CTRL),
         "SxHHI"),
        ("Binary indicator for an adverse shock",
         E.twfe(d_alt, "Youth", ["Variety", "ShockBin", "SxVbin"] + CTRL),
         "SxVbin"),
        ("Youth share of the age-classified workforce",
         E.twfe(d_alt, "Youth_alt", ["Variety", "Shock", "SxV"] + CTRL),
         "SxV"),
        ("Adding revenue growth to the control set",
         E.twfe(d.assign(Growth=d.groupby("firm").Emp.diff().fillna(0.0)),
                "Youth", ["Variety", "Shock", "SxV", "Growth"] + CTRL),
         "SxV"),
        ("Two-way clustering by firm and year",
         E.twfe(d, "Youth", ["Variety", "Shock", "SxV"] + CTRL,
                two_way_cluster=True), "SxV"),
        ("Placebo: employees aged 31 to 50",
         E.twfe(d, "Exper", ["Variety", "Shock", "SxV"] + CTRL), "SxV"),
    ]
    rows = []
    for lab, r, key in rb:
        b, se = r.cell(key)
        rows.append([lab, b, se, "{:,}".format(r.nobs), "%.3f" % r.r2])
    w("t10_robustness", rows,
      ["Specification", "Buffering effect", "S.E.", "Observations",
       "R-squared"])
    S["rb"] = {lab: dict(b=float(r.params[key]), se=float(r.se[key]),
                         p=float(r.pval[key]), n=int(r.nobs))
               for lab, r, key in rb}
    S["b_placebo"] = float(rb[-1][1].params["SxV"])
    S["p_placebo"] = float(rb[-1][1].pval["SxV"])
    S["ratio_age"] = float(S["b_sxv"] / S["b_placebo"])
    keep = [v["b"] for k, v in S["rb"].items()
            if "Placebo" not in k and "Effective" not in k
            and "Binary" not in k and "age-classified" not in k]
    S["robust_min"], S["robust_max"] = float(min(keep)), float(max(keep))
    S["oster"] = {k: float(v) for k, v in
                  E.oster_delta(d, "Youth", "SxV",
                                ["Variety", "Shock"] + CTRL).items()}
    wb = E.wild_bootstrap(d, "Youth", ["Variety", "Shock", "SxV"] + CTRL,
                          "SxV", reps=999, seed=5)
    S["wild"] = {k: float(v) for k, v in wb.items()
                 if isinstance(v, (int, float))}

    # ---------------------------------------------- Table 11 moderation
    print("Table 11 moderation")
    k1 = E.twfe(d, "Youth", ["Variety", "Shock", "SxV", "Digital_z", "SxD",
                             "VxD", "SxVxD"] + CTRL)
    k2 = E.twfe(d, "Youth", ["Variety", "Shock", "SxV", "Slack_z", "SxS",
                             "VxS", "SxVxS"] + CTRL)
    k3 = E.twfe(d, "Youth", ["Variety", "Shock", "SxV", "Digital_z", "SxD",
                             "VxD", "SxVxD", "Slack_z", "SxS", "VxS",
                             "SxVxS"] + CTRL)
    res = [k1, k2, k3]
    rows = stack(res, ["Shock", "Variety", "SxV", "Digital_z", "SxD", "VxD",
                       "SxVxD", "Slack_z", "SxS", "VxS", "SxVxS"] + CTRL,
                 tail(res))
    w("t11_moderation", rows, ["Variable", "(1)", "(2)", "(3)"])
    S["b_sxvxd"] = float(k3.params["SxVxD"])
    S["p_sxvxd"] = float(k3.pval["SxVxD"])
    S["b_sxvxs"] = float(k3.params["SxVxS"])
    S["p_sxvxs"] = float(k3.pval["SxVxS"])

    # -------------------------------------------- Table 12 heterogeneity
    print("Table 12 heterogeneity")
    splits = [("State-owned", "SOE==1", "Non-state-owned", "SOE==0"),
              ("Manufacturing", "Manuf==1", "Non-manufacturing", "Manuf==0"),
              ("Eastern region", "East==1", "Central and western region",
               "East==0"),
              ("Labor-intensive", "LabInt==1", "Capital-intensive",
               "LabInt==0")]
    rows, het = [], {}
    for la, qa, lb, qb in splits:
        ra = E.twfe(d.query(qa), "Youth", ["Variety", "Shock", "SxV"] + CTRL)
        rbb = E.twfe(d.query(qb), "Youth", ["Variety", "Shock", "SxV"] + CTRL)
        diff, sed_, z, p = E.coef_equality(ra, rbb, "SxV")
        ba, sa = ra.cell("SxV")
        bb, sb = rbb.cell("SxV")
        rows.append([la + " / " + lb, ba, sa, bb, sb, "%.3f" % diff,
                     "%.3f" % p, "{:,}".format(ra.nobs),
                     "{:,}".format(rbb.nobs)])
        het[la] = dict(a=float(ra.params["SxV"]), b=float(rbb.params["SxV"]),
                       pa=float(ra.pval["SxV"]), pb=float(rbb.pval["SxV"]),
                       diff=float(diff), p=float(p), lab_a=la, lab_b=lb)
    w("t12_heterogeneity", rows,
      ["Subsample", "Group A", "S.E.", "Group B", "S.E.", "Difference",
       "p-value", "N (A)", "N (B)"])
    S["het"] = het

    # ------------------------------------------- Table 13 threshold model
    print("Table 13 threshold model")
    th = E.panel_threshold(d, "Youth", "Shock", "Variety",
                           ["Variety"] + CTRL, n_boot=500, grid=200, seed=23)
    rows = stack([th], ["Shock_low", "Shock_high", "Variety"] + CTRL, [])
    rows += [["Threshold estimate (gamma)", "%.3f" % th.extra["gamma"]],
             ["95% confidence interval",
              "[%.3f, %.3f]" % (th.extra["ci_low"], th.extra["ci_high"])],
             ["Share of observations below gamma",
              "%.3f" % th.extra["share_low"]],
             ["Likelihood-ratio statistic F1", "%.1f" % th.extra["f1"]],
             ["Bootstrap p-value", "%.3f" % th.extra["p_boot"]],
             ["Bootstrap replications",
              "{:,}".format(th.extra["n_boot"])],
             ["Year FE", "YES"], ["Firm FE", "YES"],
             ["Observations", "{:,}".format(th.nobs)],
             ["R-squared", "%.3f" % th.r2]]
    w("t13_threshold", rows, ["Variable", "Estimate"])
    S["thr"] = dict(gamma=float(th.extra["gamma"]),
                    ci_low=float(th.extra["ci_low"]),
                    ci_high=float(th.extra["ci_high"]),
                    f1=float(th.extra["f1"]),
                    p_boot=float(th.extra["p_boot"]),
                    n_boot=int(th.extra["n_boot"]),
                    share_low=float(th.extra["share_low"]),
                    crit=float(th.extra["crit"]),
                    grid=th.extra["grid"], lr=th.extra["lr"],
                    b_low=float(th.params["Shock_low"]),
                    se_low=float(th.se["Shock_low"]),
                    p_low=float(th.pval["Shock_low"]),
                    b_high=float(th.params["Shock_high"]),
                    se_high=float(th.se["Shock_high"]),
                    p_high=float(th.pval["Shock_high"]))
    S["thr"]["pct_below"] = float(100 * (d.Variety <= th.extra["gamma"]).mean())

    with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(S, fh, indent=1, ensure_ascii=False)
    print("\nsummary.json written with %d keys" % len(S))


if __name__ == "__main__":
    main()
