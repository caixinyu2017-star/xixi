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

CTRL = ["Size", "Lev", "ROA", "Growth", "Cashflow", "TobinQ", "Top1", "Indep",
        "Dual", "Board", "CapInt"]
MAIN = ["GenAI", "Youth", "Train", "Routine", "Absorp", "Wage"]

LABEL = {
    "GenAI": "GenAI", "Youth": "Youth", "Train": "Train",
    "Routine": "Routine", "Absorp": "Absorp", "Wage": "Wage",
    "Size": "Size", "Lev": "Lev", "ROA": "ROA", "Growth": "Growth",
    "Cashflow": "Cashflow", "TobinQ": "TobinQ", "Top1": "Top1",
    "Indep": "Indep", "Dual": "Dual", "Board": "Board", "CapInt": "CapInt",
    "GxA": "GenAI x Absorp", "GxW": "GenAI x Wage",
    "GxPost": "GenAI x Post", "Exper": "Exper", "GenAI_L1": "L.GenAI",
    "GenAI_L2": "L2.GenAI", "IV_hist": "Telephone84 x Nat",
    "IV_peer": "PeerAI",
}

S: dict = {}


def w(name, rows, header):
    """Write one table as a tab-separated file."""
    path = os.path.join(TAB, name + ".tsv")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join("" if c is None else str(c) for c in r) + "\n")
    print("  wrote", name, "(%d rows)" % len(rows))


def col(res, names, extra_rows=()):
    """A coefficient column: estimate with stars over the standard error."""
    out = []
    for nm in names:
        b, se = res.cell(nm)
        out.append((b, se))
    return out


def stack(results, names, tail_rows):
    """Assemble a multi-column coefficient block."""
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
    """The Cons / fixed-effects / N / R-squared block every table carries."""
    rows = []
    for lab, key in (("Year FE", None), ("Firm FE", None)):
        rows.append([lab] + ["YES"] * len(results))
    if extra:
        rows.extend(extra)
    rows.append(["Observations"] + ["{:,}".format(r.nobs) for r in results])
    rows.append(["R-squared"] + ["%.3f" % r.r2 for r in results])
    return rows


# ===========================================================================
def main():
    d = pd.read_csv(os.path.join(ROOT, "data", "panel.csv"))
    d["indyear"] = d.ind * 100 + d.year
    d["provyear"] = d.prov * 100 + d.year
    for L in (1, 2):
        d["GenAI_L%d" % L] = d.groupby("firm").GenAI.shift(L)

    S["n_obs"] = int(len(d))
    S["n_firms"] = int(d.firm.nunique())
    S["n_ind"] = int(d.ind.nunique())
    S["n_prov"] = int(d.prov.nunique())
    S["y0"], S["y1"] = int(d.year.min()), int(d.year.max())
    S["years"] = "%d-%d" % (S["y0"], S["y1"])

    # ------------------------------------------------- Table 2. descriptives
    print("Table 2 descriptive statistics")
    rows = []
    for c in MAIN + CTRL:
        v = d[c]
        rows.append([LABEL[c], "{:,}".format(int(v.notna().sum())),
                     "%.3f" % v.mean(), "%.3f" % v.std(),
                     "%.3f" % v.min(), "%.3f" % v.quantile(0.5),
                     "%.3f" % v.max()])
    w("t02_descriptives", rows,
      ["Variable", "N", "Mean", "S.D.", "Min", "Median", "Max"])
    for c in MAIN:
        S["mean_" + c] = float(d[c].mean())
        S["sd_" + c] = float(d[c].std())
    S["genai_2016"] = float(d[d.year == S["y0"]].GenAI.mean())
    S["genai_2022"] = float(d[d.year == 2022].GenAI.mean())
    S["genai_2024"] = float(d[d.year == S["y1"]].GenAI.mean())
    S["youth_2016"] = float(d[d.year == S["y0"]].Youth.mean())
    S["youth_2024"] = float(d[d.year == S["y1"]].Youth.mean())
    S["genai_growth"] = S["genai_2024"] / S["genai_2022"]

    # --------------------------------- Table 3. correlations and collinearity
    print("Table 3 correlations and VIF")
    cols = MAIN + CTRL
    C = d[cols].corr(method="pearson")
    vmap = E.vif(d, ["GenAI"] + CTRL)
    rows = []
    for i, a in enumerate(cols):
        line = [LABEL[a]]
        for j, b in enumerate(cols):
            line.append("%.3f" % C.iloc[i, j] if j <= i else "")
        line.append("%.2f" % vmap[a] if a in vmap else "")
        rows.append(line)
    w("t03_correlation", rows,
      ["Variable"] + [LABEL[c] for c in cols] + ["VIF"])
    S["vif_max"] = float(max(vmap.values())) if vmap else float("nan")
    S["vif_genai"] = float(vmap.get("GenAI", float("nan")))
    S["corr_gy"] = float(C.loc["GenAI", "Youth"])
    S["corr_gt"] = float(C.loc["GenAI", "Train"])
    S["corr_gr"] = float(C.loc["GenAI", "Routine"])

    # ------------------------------------------- Table 4. benchmark regression
    print("Table 4 benchmark regression")
    r1 = E.twfe(d, "Youth", ["GenAI"], time_effects=False)
    r2 = E.twfe(d, "Youth", ["GenAI"])
    r3 = E.twfe(d, "Youth", ["GenAI"] + CTRL)
    r4 = E.twfe(d, "Youth", ["GenAI"] + CTRL, other_effects=["indyear"])
    r5 = E.twfe(d, "Youth", ["GenAI"] + CTRL, other_effects=["provyear"])
    res = [r1, r2, r3, r4, r5]
    extra = [["Industry x Year FE", "NO", "NO", "NO", "YES", "NO"],
             ["Province x Year FE", "NO", "NO", "NO", "NO", "YES"]]
    rows = stack(res, ["GenAI"] + CTRL, [])
    fe = [["Year FE", "NO", "YES", "YES", "--", "--"],
          ["Firm FE", "YES", "YES", "YES", "YES", "YES"]]
    rows += fe + extra
    rows.append(["Observations"] + ["{:,}".format(r.nobs) for r in res])
    rows.append(["R-squared"] + ["%.3f" % r.r2 for r in res])
    w("t04_benchmark", rows, ["Variable", "(1)", "(2)", "(3)", "(4)", "(5)"])
    S["b_main"] = float(r3.params["GenAI"])
    S["se_main"] = float(r3.se["GenAI"])
    S["t_main"] = float(r3.tstat["GenAI"])
    S["p_main"] = float(r3.pval["GenAI"])
    S["r2_main"] = float(r3.r2)
    S["b_nocontrol"] = float(r2.params["GenAI"])
    S["b_indyear"] = float(r4.params["GenAI"])
    S["b_provyear"] = float(r5.params["GenAI"])
    S["effect_sd"] = float(-S["b_main"] * S["sd_GenAI"])
    S["effect_sd_pct"] = float(100 * S["effect_sd"] / S["mean_Youth"])
    S["effect_iqr"] = float(-S["b_main"] *
                            (d.GenAI.quantile(0.75) - d.GenAI.quantile(0.25)))

    # ------------------------------------------- Table 5. mediating mechanisms
    print("Table 5 mediating mechanisms")
    m1 = E.twfe(d, "Train", ["GenAI"] + CTRL)
    m2 = E.twfe(d, "Youth", ["GenAI", "Train"] + CTRL)
    m3 = E.twfe(d, "Routine", ["GenAI"] + CTRL)
    m4 = E.twfe(d, "Youth", ["GenAI", "Routine"] + CTRL)
    m5 = E.twfe(d, "Youth", ["GenAI", "Train", "Routine"] + CTRL)
    res = [r3, m1, m2, m3, m4, m5]
    rows = stack(res, ["GenAI", "Train", "Routine"] + CTRL, tail(res))
    w("t05_mechanism", rows,
      ["Variable", "Youth (1)", "Train (2)", "Youth (3)", "Routine (4)",
       "Youth (5)", "Youth (6)"])
    S["a_train"] = float(m1.params["GenAI"])
    S["b_train"] = float(m2.params["Train"])
    S["a_rout"] = float(m3.params["GenAI"])
    S["b_rout"] = float(m4.params["Routine"])
    S["direct_both"] = float(m5.params["GenAI"])
    S["p_direct_both"] = float(m5.pval["GenAI"])

    # ---------------------------------------- Table 6. indirect decomposition
    print("Table 6 bootstrapped indirect effects")
    med = {}
    rows = []
    for key, nm in (("Train", "Training investment"),
                    ("Routine", "Routine task base")):
        r = E.mediation(d, "Youth", "GenAI", key, CTRL, n_boot=400, seed=11)
        med[key] = {k: v for k, v in r.items() if k != "res"}
        rows.append([nm,
                     "%.3f%s" % (r["total"], E.stars(r["p_total"])),
                     "%.3f%s" % (r["a"], E.stars(r["p_a"])),
                     "%.3f%s" % (r["b"], E.stars(r["p_b"])),
                     "%.3f%s" % (r["direct"], E.stars(r["p_direct"])),
                     "%.3f" % r["indirect"],
                     "[%.3f, %.3f]" % (r["ci_low"], r["ci_high"]),
                     "%.1f" % r["share"]])
    w("t06_indirect", rows,
      ["Mediator", "Total effect", "Path a", "Path b", "Direct effect",
       "Indirect effect", "95% bootstrap CI", "Share of total (%)"])
    S["med"] = med
    S["share_train"] = float(med["Train"]["share"])
    S["share_rout"] = float(med["Routine"]["share"])
    S["share_both"] = float(S["share_train"] + S["share_rout"])
    S["n_boot_med"] = int(med["Train"]["n_boot"])

    # -------------------------------------------- Table 7. endogeneity tests
    print("Table 7 endogeneity")
    iv = E.absorbed_2sls(d, "Youth", ["GenAI"], CTRL, ["IV_hist", "IV_peer"])
    fs = iv.extra["first_stage_coef"]
    dl = d.dropna(subset=["GenAI_L1"])
    lag1 = E.twfe(dl, "Youth", ["GenAI_L1"] + CTRL)

    # propensity score matching on pre-2022 firm averages
    dm = d.copy()
    dm["Post"] = (dm.year >= 2023).astype(int)
    hi = dm[dm.year >= 2023].groupby("firm").GenAI.mean()
    dm["Treat"] = dm.firm.map((hi >= hi.median()).astype(int)).fillna(0)
    dm["Treat"] = dm["Treat"].astype(int)
    matched, bal, ps = E.psm(dm, ["Size", "Lev", "ROA", "Growth", "TobinQ",
                                  "Top1", "CapInt"], treat="Treat",
                             caliper=0.05, k=1)
    psm_r = E.twfe(matched, "Youth", ["GenAI"] + CTRL)
    eb = E.entropy_balance(dm, ["Size", "Lev", "ROA", "Growth", "TobinQ",
                                "Top1", "CapInt"], treat="Treat")
    eb_r = E.twfe(eb, "Youth", ["GenAI"] + CTRL, weights="ebw")

    body = []
    for nm in ["IV_hist", "IV_peer", "GenAI", "GenAI_L1"]:
        line_b, line_s = [LABEL[nm]], [""]
        if nm in fs:
            b, se, p = fs[nm]
            line_b.append("%.3f%s" % (b, E.stars(p)))
            line_s.append("(%.3f)" % se)
        else:
            line_b.append("")
            line_s.append("")
        for r, key in ((iv, "GenAI"), (lag1, "GenAI_L1"), (psm_r, "GenAI"),
                       (eb_r, "GenAI")):
            if nm == key:
                b, se = r.cell(nm)
                line_b.append(b)
                line_s.append(se)
            else:
                line_b.append("")
                line_s.append("")
        if any(x for x in line_b[1:]):
            body.append(line_b)
            body.append(line_s)
    rows = body
    rows.append(["Controls", "YES", "YES", "YES", "YES", "YES"])
    rows.append(["Year FE", "YES", "YES", "YES", "YES", "YES"])
    rows.append(["Firm FE", "YES", "YES", "YES", "YES", "YES"])
    rows.append(["Kleibergen-Paap rk F", "%.1f" % iv.extra["first_stage_F"],
                 "", "", "", ""])
    rows.append(["Hansen J (p-value)", "",
                 "%.3f (%.3f)" % (iv.extra["hansen_J"],
                                  iv.extra["hansen_p"]), "", "", ""])
    rows.append(["Durbin-Wu-Hausman (p-value)", "",
                 "%.3f" % iv.extra["wu_hausman_p"], "", "", ""])
    rows.append(["Observations", "{:,}".format(iv.nobs),
                 "{:,}".format(iv.nobs), "{:,}".format(lag1.nobs),
                 "{:,}".format(psm_r.nobs), "{:,}".format(eb_r.nobs)])
    w("t07_endogeneity", rows,
      ["Variable", "(1) First stage", "(2) 2SLS", "(3) One-year lag",
       "(4) PSM sample", "(5) Entropy balancing"])
    S["b_iv"] = float(iv.params["GenAI"])
    S["se_iv"] = float(iv.se["GenAI"])
    S["kp_f"] = float(iv.extra["first_stage_F"])
    S["hansen_p"] = float(iv.extra["hansen_p"])
    S["wu_p"] = float(iv.extra["wu_hausman_p"])
    S["b_lag1"] = float(lag1.params["GenAI_L1"])
    S["b_eb"] = float(eb_r.params["GenAI"])
    S["b_psm"] = float(psm_r.params["GenAI"])
    S["n_psm"] = int(psm_r.nobs)
    S["n_psm_firms"] = int(matched.firm.nunique())
    S["bal_max_after"] = float(bal.bias_m.abs().max())
    S["bal_max_before"] = float(bal.bias_u.abs().max())
    S["bal_min_p"] = float(bal.p.min())

    # ------------------------------------------- Table 8. robustness checks
    print("Table 8 robustness")
    d_alt = d.copy()
    d_alt["GenAI_bin"] = (d_alt.GenAI > d_alt.groupby("year").GenAI
                          .transform("median")).astype(float)
    d_alt["Youth_alt"] = 100.0 * d_alt.Youth / (d_alt.Youth + d_alt.Exper)
    rb = [
        ("Excluding 2020 and 2021",
         E.twfe(d[~d.year.isin([2020, 2021])], "Youth", ["GenAI"] + CTRL),
         "GenAI"),
        ("Balanced panel only",
         E.twfe(d[d.firm.isin(d.groupby("firm").size()
                              .loc[lambda s: s == s.max()].index)],
                "Youth", ["GenAI"] + CTRL), "GenAI"),
        ("Adoption above the yearly median",
         E.twfe(d_alt, "Youth", ["GenAI_bin"] + CTRL), "GenAI_bin"),
        ("Youth share of the age-classified workforce",
         E.twfe(d_alt, "Youth_alt", ["GenAI"] + CTRL), "GenAI"),
        ("Two-way clustering by firm and year",
         E.twfe(d, "Youth", ["GenAI"] + CTRL, two_way_cluster=True), "GenAI"),
        ("Winsorizing the outcome at 5 per cent",
         E.twfe(d.assign(Youth=d.Youth.clip(*d.Youth.quantile([.05, .95]))),
                "Youth", ["GenAI"] + CTRL), "GenAI"),
        ("Placebo: employees aged 31 to 50",
         E.twfe(d, "Exper", ["GenAI"] + CTRL), "GenAI"),
    ]
    rows = []
    for lab, r, key in rb:
        b, se = r.cell(key)
        rows.append([lab, b, se, "{:,}".format(r.nobs), "%.3f" % r.r2])
    w("t08_robustness", rows,
      ["Specification", "GenAI", "S.E.", "Observations", "R-squared"])
    S["rb"] = {lab: dict(b=float(r.params[key]), se=float(r.se[key]),
                         p=float(r.pval[key]), n=int(r.nobs))
               for lab, r, key in rb}
    S["b_placebo"] = float(rb[-1][1].params["GenAI"])
    S["p_placebo"] = float(rb[-1][1].pval["GenAI"])
    S["ratio_age"] = float(S["b_main"] / S["b_placebo"])
    rr = [abs(v["b"]) for k, v in S["rb"].items()
          if "Placebo" not in k and "median" not in k and "age-cl" not in k]
    S["robust_min"], S["robust_max"] = float(min(rr)), float(max(rr))
    S["oster"] = {k: float(v) for k, v in
                  E.oster_delta(d, "Youth", "GenAI", CTRL).items()}
    wb = E.wild_bootstrap(d, "Youth", ["GenAI"] + CTRL, "GenAI", reps=999,
                          seed=5)
    S["wild"] = {k: float(v) for k, v in wb.items()
                 if isinstance(v, (int, float))}

    # ------------------------------------------- Table 9. moderating effects
    print("Table 9 moderation")
    q1 = E.twfe(d, "Youth", ["GenAI", "GxA"] + CTRL)
    q2 = E.twfe(d, "Youth", ["GenAI", "GxW"] + CTRL)
    q3 = E.twfe(d, "Youth", ["GenAI", "GxA", "GxW"] + CTRL)
    q4 = E.twfe(d, "Youth", ["GenAI", "GxPost"] + CTRL)
    res = [q1, q2, q3, q4]
    rows = stack(res, ["GenAI", "GxA", "GxW", "GxPost"] + CTRL, tail(res))
    w("t09_moderation", rows, ["Variable", "(1)", "(2)", "(3)", "(4)"])
    S["b_gxa"] = float(q3.params["GxA"])
    S["p_gxa"] = float(q3.pval["GxA"])
    S["b_gxw"] = float(q3.params["GxW"])
    S["p_gxw"] = float(q3.pval["GxW"])
    S["b_q3"] = float(q3.params["GenAI"])
    S["b_gxpost"] = float(q4.params["GxPost"])
    S["p_gxpost"] = float(q4.pval["GxPost"])
    S["b_pre"] = float(q4.params["GenAI"])
    S["post_ratio"] = float((S["b_pre"] + S["b_gxpost"]) / S["b_pre"])
    zs = list(np.linspace(-2.0, 2.0, 17))
    S["margin_absorp"] = E.margin(q3, "GenAI", "GxA", zs)
    S["margin_wage"] = E.margin(q3, "GenAI", "GxW", zs)

    # ------------------------------------------ Table 10. heterogeneity
    print("Table 10 heterogeneity")
    splits = [("State-owned", "SOE==1", "Non-state-owned", "SOE==0"),
              ("High-technology", "HighTech==1", "Non-high-technology",
               "HighTech==0"),
              ("Eastern region", "East==1", "Central and western region",
               "East==0"),
              ("Labor-intensive", "LabInt==1", "Capital-intensive",
               "LabInt==0")]
    rows, het = [], {}
    for la, qa, lb, qb in splits:
        ra = E.twfe(d.query(qa), "Youth", ["GenAI"] + CTRL)
        rb_ = E.twfe(d.query(qb), "Youth", ["GenAI"] + CTRL)
        diff, sed_, z, p = E.coef_equality(ra, rb_, "GenAI")
        ba, sa = ra.cell("GenAI")
        bb, sb = rb_.cell("GenAI")
        rows.append([la + " / " + lb, ba, sa, bb, sb, "%.3f" % diff,
                     "%.3f" % p, "{:,}".format(ra.nobs),
                     "{:,}".format(rb_.nobs)])
        het[la] = dict(a=float(ra.params["GenAI"]), b=float(rb_.params["GenAI"]),
                       pa=float(ra.pval["GenAI"]), pb=float(rb_.pval["GenAI"]),
                       diff=float(diff), p=float(p), na=int(ra.nobs),
                       nb=int(rb_.nobs), lab_a=la, lab_b=lb)
    w("t10_heterogeneity", rows,
      ["Subsample", "Group A", "S.E.", "Group B", "S.E.", "Difference",
       "p-value", "N (A)", "N (B)"])
    S["het"] = het

    # ---------------------------------- Table 11. panel vector autoregression
    print("Table 11 panel VAR")
    v = E.pvar(d, ["GenAI", "Train", "Youth"], lags=1, n_boot=400, seed=13,
               horizon=8)
    cols3 = v["cols"]
    rows = []
    for i, eq in enumerate(cols3):
        line_b, line_s = ["%s equation" % LABEL[eq]], [""]
        for j, cj in enumerate(cols3):
            g = v["gc"][(eq, cj)]
            line_b.append("%.3f%s" % (g["coef"], E.stars(g["p"])))
            line_s.append("(%.3f)" % g["se"])
        rows.append(line_b)
        rows.append(line_s)
    rows.append(["Granger chi-squared", "", "", ""])
    for i, eq in enumerate(cols3):
        rows.append(["  %s equation" % LABEL[eq]] +
                    ["%.2f [%.3f]" % (v["gc"][(eq, cj)]["chi2"],
                                      v["gc"][(eq, cj)]["p"])
                     for cj in cols3])
    rows.append(["Modulus of companion eigenvalues",
                 *["%.3f" % x for x in np.sort(v["eig"])[::-1]]])
    rows.append(["Observations", "{:,}".format(v["nobs"]), "", ""])
    rows.append(["Firms", "{:,}".format(v["n_firms"]), "", ""])
    rows.append(["Bootstrap replications", "{:,}".format(v["n_boot"]), "", ""])
    w("t11_pvar", rows,
      ["Equation", "L.GenAI", "L.Train", "L.Youth"])

    S["pvar"] = dict(
        A=[[float(x) for x in row] for row in v["A"]],
        se=[[float(x) for x in row] for row in v["se"]],
        cols=cols3, eig=[float(x) for x in np.sort(v["eig"])[::-1]],
        max_eig=float(v["max_eig"]), nobs=int(v["nobs"]),
        n_firms=int(v["n_firms"]), n_boot=int(v["n_boot"]),
        gc={"%s<-%s" % k: dict(coef=float(g["coef"]), se=float(g["se"]),
                               chi2=float(g["chi2"]), p=float(g["p"]))
            for k, g in v["gc"].items()})
    S["fb_train"] = float(v["gc"][("GenAI", "Train")]["coef"])
    S["fb_train_p"] = float(v["gc"][("GenAI", "Train")]["p"])
    S["fb_youth"] = float(v["gc"][("GenAI", "Youth")]["coef"])
    S["fb_youth_p"] = float(v["gc"][("GenAI", "Youth")]["p"])
    S["fw_youth"] = float(v["gc"][("Youth", "GenAI")]["coef"])
    S["fw_youth_p"] = float(v["gc"][("Youth", "GenAI")]["p"])
    S["fw_train"] = float(v["gc"][("Train", "GenAI")]["coef"])
    S["fw_train_p"] = float(v["gc"][("Train", "GenAI")]["p"])

    # ------------------------------- Table 12. impulse responses and the loop
    print("Table 12 impulse responses")
    irf, lo, hi = v["irf"], v["irf_lo"], v["irf_hi"]
    H = v["horizon"]
    ix = {c: i for i, c in enumerate(cols3)}
    rows = []
    pairs = [("Youth", "GenAI"), ("Train", "GenAI"), ("GenAI", "Train"),
             ("GenAI", "Youth")]
    for resp, shock in pairs:
        i, j = ix[resp], ix[shock]
        rows.append(["%s to a %s shock" % (LABEL[resp], LABEL[shock])] +
                    ["%.3f" % irf[h, i, j] for h in range(H + 1)])
        rows.append([""] + ["[%.3f, %.3f]" % (lo[h, i, j], hi[h, i, j])
                            for h in range(H + 1)])
    # closed versus open loop: shut the return arcs and re-simulate
    A = np.array(v["A"], float)
    A_open = A.copy()
    A_open[ix["GenAI"], ix["Train"]] = 0.0
    A_open[ix["GenAI"], ix["Youth"]] = 0.0
    P = np.linalg.cholesky(v["sigma"] + 1e-12 * np.eye(3))

    def path(Amat):
        out, M = [], np.eye(3)
        for _ in range(H + 1):
            out.append((M @ P)[ix["Youth"], ix["GenAI"]])
            M = M @ Amat
        return np.array(out)

    closed, open_ = path(A), path(A_open)
    rows.append(["Cumulative Youth response, closed loop"] +
                ["%.3f" % x for x in np.cumsum(closed)])
    rows.append(["Cumulative Youth response, loop suppressed"] +
                ["%.3f" % x for x in np.cumsum(open_)])
    rows.append(["Amplification factor"] +
                ["%.3f" % (a / b) for a, b in
                 zip(np.cumsum(closed), np.cumsum(open_))])
    w("t12_irf", rows,
      ["Response"] + ["h = %d" % h for h in range(H + 1)])

    S["irf"] = {"%s<-%s" % (r_, s_): dict(
        m=[float(irf[h, ix[r_], ix[s_]]) for h in range(H + 1)],
        lo=[float(lo[h, ix[r_], ix[s_]]) for h in range(H + 1)],
        hi=[float(hi[h, ix[r_], ix[s_]]) for h in range(H + 1)])
        for r_, s_ in pairs}
    S["cum_closed"] = [float(x) for x in np.cumsum(closed)]
    S["cum_open"] = [float(x) for x in np.cumsum(open_)]
    S["amp"] = float(np.cumsum(closed)[-1] / np.cumsum(open_)[-1])
    S["impact"] = float(closed[0])
    S["cum8"] = float(np.cumsum(closed)[-1])
    S["cum_ratio"] = float(np.cumsum(closed)[-1] / closed[0])
    S["horizon"] = int(H)

    v2 = E.pvar(d, ["GenAI", "Train", "Youth"], lags=2, n_boot=200, seed=13,
                horizon=8)
    S["pvar2"] = dict(max_eig=float(v2["max_eig"]), nobs=int(v2["nobs"]),
                      fb_train=float(v2["gc"][("GenAI", "Train")]["coef"]),
                      fb_train_p=float(v2["gc"][("GenAI", "Train")]["p"]),
                      fb_youth=float(v2["gc"][("GenAI", "Youth")]["coef"]),
                      fb_youth_p=float(v2["gc"][("GenAI", "Youth")]["p"]),
                      fw_youth=float(v2["gc"][("Youth", "GenAI")]["coef"]),
                      fw_youth_p=float(v2["gc"][("Youth", "GenAI")]["p"]))

    with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(S, fh, indent=1, ensure_ascii=False)
    print("\nsummary.json written with %d keys" % len(S))


if __name__ == "__main__":
    main()
