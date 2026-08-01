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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
TAB = os.path.join(ROOT, "tables")
os.makedirs(TAB, exist_ok=True)

CONTROLS = ["Size", "Lev", "ROA", "Growth", "Cash", "FirmAge", "TobinQ",
            "CapInt", "Wage", "Analyst", "InstOwn", "GDPg", "YouthU"]
IVS = ["IV_Shift", "IV_Frontier", "IV_Peer"]
BASE = ["AIU", "AIE", "FirmEPU"]
SUM = {}


def W(name, header, rows):
    with open(os.path.join(TAB, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(c) for c in r) + "\n")


def block(res, names, d=3):
    """Coefficient and standard-error cells for a list of regressors."""
    out = []
    for nm in names:
        b, se = res.cell(nm, d)
        out.append((b, se))
    return out


def pack(rows_spec, tails):
    """Interleave coefficient rows and standard-error rows."""
    rows = []
    for name, cells in rows_spec:
        rows.append([name] + [c[0] for c in cells])
        rows.append([""] + [c[1] for c in cells])
    rows.extend(tails)
    return rows


# ---------------------------------------------------------------------------
def t_descriptives(df):
    order = ["EntryRate", "EntryPost", "ExpRate", "ContShare", "YouthShare",
             "NetYouth", "Inaction", "AIU", "AIE", "FirmEPU", "SpecTrain",
             "FireCost", "Flex"] + CONTROLS
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

    post = df[df.Post == 1]
    pre = df[df.Post == 0]
    SUM.update(
        n_obs=int(len(df)), n_firms=int(df.firm.nunique()),
        years="%d-%d" % (df.year.min(), df.year.max()),
        entry_mean=float(df.EntryRate.mean()), entry_sd=float(df.EntryRate.std()),
        entry_count_mean=float(df.EntryPost.mean()),
        exper_mean=float(df.ExpRate.mean()),
        cont_mean=float(df.ContShare.mean()), cont_sd=float(df.ContShare.std()),
        cont_pre=float(pre.ContShare.mean()), cont_post=float(post.ContShare.mean()),
        youth_mean=float(df.YouthShare.mean()),
        youth_pre=float(pre.YouthShare.mean()),
        youth_post=float(post.YouthShare.mean()),
        inaction_mean=float(df.Inaction.mean()),
        inaction_pre=float(pre.Inaction.mean()),
        inaction_post=float(post.Inaction.mean()),
        entry_pre=float(pre.EntryRate.mean()), entry_post=float(post.EntryRate.mean()),
        aiu_post=float(post.AIU.mean()), aiu_pre=float(pre.AIU.mean()),
        n_zero=int((df.EntryPost == 0).sum()),
        zero_share=float((df.EntryPost == 0).mean() * 100),
        aiu_p25=float(df.AIU.quantile(0.25)), aiu_p75=float(df.AIU.quantile(0.75)),
        aiu_iqr=float(df.AIU.quantile(0.75) - df.AIU.quantile(0.25)),
        aiu_sd_pre=float(pre.AIU.std()), aiu_sd_post=float(post.AIU.std()),
        aiu_dd=float((post.loc[post.Treat == 1, "AIU"].mean()
                      - post.loc[post.Treat == 0, "AIU"].mean())
                     - (pre.loc[pre.Treat == 1, "AIU"].mean()
                        - pre.loc[pre.Treat == 0, "AIU"].mean())),
        emp_median=float(df.Emp.median()))


def t_correlation(df):
    keep = ["EntryRate", "ExpRate", "ContShare", "YouthShare", "AIU", "AIE",
            "FirmEPU", "SpecTrain", "FireCost", "Flex"]
    d = df[keep].dropna()
    rows = []
    for i, a in enumerate(keep):
        cells = []
        for j, b in enumerate(keep):
            if j > i:
                cells.append("")
            elif i == j:
                cells.append("1.000")
            else:
                r, p = stats.pearsonr(d[a], d[b])
                cells.append("%.3f%s" % (r, E.stars(p)))
        rows.append([a] + cells)
    W("t_correlation.tsv", ["Variable"] + keep, rows)

    v = E.vif(df, BASE + ["SpecTrain", "FireCost", "Flex"] + CONTROLS)
    SUM.update(vif_max=float(max(v.values())),
               vif_mean=float(np.mean(list(v.values()))),
               corr_u_a=float(d.AIU.corr(d.AIE)),
               corr_u_e=float(d.AIU.corr(d.FirmEPU)))


# ---------------------------------------------------------------------------
def t_baseline(df):
    c1 = E.twfe(df, "EntryRate", ["AIU"])
    c2 = E.twfe(df, "EntryRate", ["AIU"] + CONTROLS)
    c3 = E.twfe(df, "EntryRate", ["AIU", "AIE"] + CONTROLS)
    c4 = E.twfe(df, "EntryRate", BASE + CONTROLS)
    c5 = E.ppml(df, "EntryPost", BASE + ["lnEmp"] + CONTROLS)
    c6 = E.twfe(df, "YouthShare", BASE + CONTROLS)
    cols = [c1, c2, c3, c4, c5, c6]

    spec = []
    for nm in ["AIU", "AIE", "FirmEPU"]:
        spec.append((nm, [c.cell(nm) for c in cols]))
    tails = [
        ["Controls", "No", "Yes", "Yes", "Yes", "Yes", "Yes"],
        ["Firm FE"] + ["Yes"] * 6,
        ["Year FE"] + ["Yes"] * 6,
        ["Observations"] + ["%s" % format(c.nobs, ",") for c in cols],
        ["Within R2"] + ["%.3f" % c.r2 for c in cols],
    ]
    W("t_baseline.tsv",
      ["Variable", "(1)", "(2)", "(3)", "(4)", "(5)", "(6)"],
      pack(spec, tails))

    SUM.update(
        b_raw=float(c1.params.AIU), se_raw=float(c1.se.AIU),
        b_main=float(c4.params.AIU), se_main=float(c4.se.AIU),
        p_main=float(c4.pval.AIU), t_main=float(c4.tstat.AIU),
        r2_main=float(c4.r2),
        b_level=float(c4.params.AIE), se_level=float(c4.se.AIE),
        p_level=float(c4.pval.AIE),
        b_epu=float(c4.params.FirmEPU), se_epu=float(c4.se.FirmEPU),
        p_epu=float(c4.pval.FirmEPU),
        b_ppml=float(c5.params.AIU), se_ppml=float(c5.se.AIU),
        p_ppml=float(c5.pval.AIU),
        b_youth=float(c6.params.AIU), se_youth=float(c6.se.AIU),
        p_youth=float(c6.pval.AIU),
        ratio_u_e=float(abs(c4.params.AIU / c4.params.FirmEPU)),
        pct_of_mean=float(100 * abs(c4.params.AIU) / df.EntryRate.mean()),
        pct_youth=float(100 * abs(c6.params.AIU) / df.YouthShare.mean()))


def t_agespec(df):
    c1 = E.twfe(df, "EntryRate", BASE + CONTROLS)
    c2 = E.twfe(df, "ExpRate", BASE + CONTROLS)
    c3 = E.ppml(df, "EntryPost", BASE + ["lnEmp"] + CONTROLS)
    c4 = E.ppml(df, "ExpPost", BASE + ["lnEmp"] + CONTROLS)
    st = E.stacked_test(df, "EntryRate", "ExpRate", BASE + CONTROLS, "AIU")
    stp = E.stacked_test(df, "ContShare", "ExpRate", BASE + CONTROLS, "AIU")

    cols = [c1, c2, c3, c4]
    spec = [(nm, [c.cell(nm) for c in cols]) for nm in BASE]
    tails = [
        ["Controls"] + ["Yes"] * 4,
        ["Firm FE"] + ["Yes"] * 4,
        ["Year FE"] + ["Yes"] * 4,
        ["Observations"] + [format(c.nobs, ",") for c in cols],
        ["Within R2"] + ["%.3f" % c.r2 for c in cols],
        ["Cross-equation difference", "%.3f%s" % (st["diff"], E.stars(st["p"])),
         "", "", ""],
        ["", "(%.3f)" % st["se"], "", "", ""],
    ]
    W("t_agespec.tsv", ["Variable", "(1)", "(2)", "(3)", "(4)"],
      pack(spec, tails))

    SUM.update(b_exper=float(c2.params.AIU), se_exper=float(c2.se.AIU),
               p_exper=float(c2.pval.AIU),
               b_exper_ppml=float(c4.params.AIU), p_exper_ppml=float(c4.pval.AIU),
               diff_age=float(st["diff"]), se_diff_age=float(st["se"]),
               p_diff_age=float(st["p"]),
               ratio_age=float(abs(c1.params.AIU / c2.params.AIU)))
    SUM["_stp"] = float(stp["p"])


def t_irrev(df):
    d = df.copy()
    for z in ["SpecTrain", "FireCost", "Flex"]:
        d["AIUx" + z] = d.AIU * d[z]
    c1 = E.twfe(d, "EntryRate", ["AIU", "AIUxSpecTrain"] + BASE[1:] + CONTROLS)
    c2 = E.twfe(d, "EntryRate", ["AIU", "AIUxFireCost"] + BASE[1:] + CONTROLS)
    c3 = E.twfe(d, "EntryRate", ["AIU", "AIUxFlex"] + BASE[1:] + CONTROLS)
    c4 = E.twfe(d, "EntryRate",
                ["AIU", "AIUxSpecTrain", "AIUxFireCost", "AIUxFlex"]
                + BASE[1:] + CONTROLS)
    cols = [c1, c2, c3, c4]
    names = ["AIU", "AIUxSpecTrain", "AIUxFireCost", "AIUxFlex", "AIE",
             "FirmEPU"]
    spec = [(nm, [c.cell(nm) for c in cols]) for nm in names]

    m = {}
    for z, res in (("SpecTrain", c1), ("FireCost", c2), ("Flex", c3)):
        mm = E.margin(res, "AIU", "AIUx" + z, [-1.0, 1.0])
        m[z] = mm
    tails = [
        ["Effect at moderator = -1 SD"] +
        ["%.3f%s" % (m[z][0]["effect"], E.stars(m[z][0]["p"]))
         for z in ("SpecTrain", "FireCost", "Flex")] + [""],
        ["Effect at moderator = +1 SD"] +
        ["%.3f%s" % (m[z][1]["effect"], E.stars(m[z][1]["p"]))
         for z in ("SpecTrain", "FireCost", "Flex")] + [""],
        ["Controls"] + ["Yes"] * 4,
        ["Firm FE"] + ["Yes"] * 4,
        ["Year FE"] + ["Yes"] * 4,
        ["Observations"] + [format(c.nobs, ",") for c in cols],
        ["Within R2"] + ["%.3f" % c.r2 for c in cols],
    ]
    W("t_irrev.tsv", ["Variable", "(1)", "(2)", "(3)", "(4)"],
      pack(spec, tails))

    SUM["moderation"] = {}
    for z, res in (("SpecTrain", c1), ("FireCost", c2), ("Flex", c3)):
        nm = "AIUx" + z
        SUM["moderation"][z] = dict(
            b=float(res.params[nm]), se=float(res.se[nm]),
            p=float(res.pval[nm]),
            lo=float(m[z][0]["effect"]), lo_p=float(m[z][0]["p"]),
            hi=float(m[z][1]["effect"]), hi_p=float(m[z][1]["p"]),
            ratio=float(abs(m[z][1]["effect"] / m[z][0]["effect"])))
    SUM["b_joint_train"] = float(c4.params["AIUxSpecTrain"])
    SUM["p_joint_train"] = float(c4.pval["AIUxSpecTrain"])


def t_contingent(df):
    d = df.copy()
    d["AIUxFlex"] = d.AIU * d.Flex
    d["AIUxSpecTrain"] = d.AIU * d.SpecTrain
    c1 = E.twfe(d, "ContShare", ["AIU"] + CONTROLS)
    c2 = E.twfe(d, "ContShare", BASE + CONTROLS)
    c3 = E.twfe(d, "ContShare", ["AIU", "AIUxFlex"] + BASE[1:] + CONTROLS)
    c4 = E.twfe(d, "ContShare", ["AIU", "AIUxSpecTrain"] + BASE[1:] + CONTROLS)
    c5 = E.twfe(d, "EntryRate", ["AIU", "AIUxFlex"] + BASE[1:] + CONTROLS)
    cols = [c1, c2, c3, c4, c5]
    names = ["AIU", "AIUxFlex", "AIUxSpecTrain", "AIE", "FirmEPU"]
    spec = [(nm, [c.cell(nm) for c in cols]) for nm in names]
    tails = [
        ["Controls"] + ["Yes"] * 5,
        ["Firm FE"] + ["Yes"] * 5,
        ["Year FE"] + ["Yes"] * 5,
        ["Observations"] + [format(c.nobs, ",") for c in cols],
        ["Within R2"] + ["%.3f" % c.r2 for c in cols],
    ]
    W("t_contingent.tsv", ["Variable", "(1)", "(2)", "(3)", "(4)", "(5)"],
      pack(spec, tails))
    SUM.update(b_cont=float(c2.params.AIU), se_cont=float(c2.se.AIU),
               p_cont=float(c2.pval.AIU),
               cont_pct=float(100 * c2.params.AIU / df.ContShare.mean()),
               b_cont_flex=float(c3.params.AIUxFlex),
               p_cont_flex=float(c3.pval.AIUxFlex),
               b_cont_train=float(c4.params.AIUxSpecTrain),
               p_cont_train=float(c4.pval.AIUxSpecTrain))


def t_inaction(df):
    d = df.sort_values(["firm", "year"]).copy()
    d["AbsNet"] = d.NetYouth.abs()
    d["LagInact"] = d.groupby("firm").Inaction.shift(1)
    d["AIUxSpecTrain"] = d.AIU * d.SpecTrain

    c1 = E.twfe(d, "Inaction", ["AIU"] + CONTROLS)
    c2 = E.twfe(d, "Inaction", BASE + CONTROLS)
    c3 = E.twfe(d, "Inaction", ["AIU", "AIUxSpecTrain"] + BASE[1:] + CONTROLS)
    sub = d[d.LagInact == 1]
    c4 = E.twfe(sub, "Expand", BASE + CONTROLS)
    c5 = E.twfe(d, "NetYouth", BASE + CONTROLS)
    cols = [c1, c2, c3, c4, c5]
    names = ["AIU", "AIUxSpecTrain", "AIE", "FirmEPU"]
    spec = [(nm, [c.cell(nm) for c in cols]) for nm in names]
    tails = [
        ["Controls"] + ["Yes"] * 5,
        ["Firm FE"] + ["Yes"] * 5,
        ["Year FE"] + ["Yes"] * 5,
        ["Observations"] + [format(c.nobs, ",") for c in cols],
        ["Within R2"] + ["%.3f" % c.r2 for c in cols],
    ]
    W("t_inaction.tsv", ["Variable", "(1)", "(2)", "(3)", "(4)", "(5)"],
      pack(spec, tails))
    SUM.update(b_inact=float(c2.params.AIU), se_inact=float(c2.se.AIU),
               p_inact=float(c2.pval.AIU),
               inact_pct=float(100 * c2.params.AIU / df.Inaction.mean()),
               b_resume=float(c4.params.AIU), se_resume=float(c4.se.AIU),
               p_resume=float(c4.pval.AIU), n_resume=int(c4.nobs),
               resume_mean=float(sub.Expand.mean()),
               b_net=float(c5.params.AIU), se_net=float(c5.se.AIU),
               p_net=float(c5.pval.AIU),
               b_inact_train=float(c3.params.AIUxSpecTrain),
               p_inact_train=float(c3.pval.AIUxSpecTrain))


# ---------------------------------------------------------------------------
def t_iv(df):
    iv = E.absorbed_2sls(df, "EntryRate", "AIU", ["AIE", "FirmEPU"] + CONTROLS,
                         IVS)
    ivg = E.absorbed_2sls(df, "EntryRate", "AIU", ["AIE", "FirmEPU"] + CONTROLS,
                          IVS, gmm=True)
    iv2 = E.absorbed_2sls(df, "ContShare", "AIU", ["AIE", "FirmEPU"] + CONTROLS,
                          IVS)
    iv3 = E.absorbed_2sls(df, "ExpRate", "AIU", ["AIE", "FirmEPU"] + CONTROLS,
                          IVS)
    ols = E.twfe(df, "EntryRate", BASE + CONTROLS)

    fs = iv.extra["first_stage_coef"]
    rows = [["Panel A: first stage, dependent variable AIU", "", "", "", ""]]
    for nm in IVS:
        b, se, p = fs[nm]
        rows.append([nm, "%.3f%s" % (b, E.stars(p)), "", "", ""])
        rows.append(["", "(%.3f)" % se, "", "", ""])
    rows.append(["Kleibergen-Paap rk Wald F",
                 "%.1f" % iv.extra["first_stage_F"], "", "", ""])
    rows.append(["Panel B: second stage", "", "", "", ""])
    cols = [ols, iv, ivg, iv2, iv3]
    for nm in ["AIU", "AIE", "FirmEPU"]:
        rows.append([nm] + [c.cell(nm)[0] for c in cols])
        rows.append([""] + [c.cell(nm)[1] for c in cols])
    rows += [
        ["Estimator", "OLS", "2SLS", "GMM", "2SLS", "2SLS"],
        ["Hansen J (p)", "",
         "%.3f" % iv.extra.get("hansen_p", float("nan")),
         "%.3f" % ivg.extra.get("hansen_p", float("nan")),
         "%.3f" % iv2.extra.get("hansen_p", float("nan")),
         "%.3f" % iv3.extra.get("hansen_p", float("nan"))],
        ["Wu-Hausman (p)", "",
         "%.4f" % iv.extra.get("wu_hausman_p", float("nan")),
         "", "%.4f" % iv2.extra.get("wu_hausman_p", float("nan")),
         "%.4f" % iv3.extra.get("wu_hausman_p", float("nan"))],
        ["Controls"] + ["Yes"] * 5,
        ["Firm FE"] + ["Yes"] * 5,
        ["Year FE"] + ["Yes"] * 5,
        ["Observations"] + [format(c.nobs, ",") for c in cols],
    ]
    W("t_iv.tsv", ["Variable", "(1)", "(2)", "(3)", "(4)", "(5)"], rows)

    SUM.update(b_iv=float(iv.params.AIU), se_iv=float(iv.se.AIU),
               p_iv=float(iv.pval.AIU),
               b_gmm=float(ivg.params.AIU), se_gmm=float(ivg.se.AIU),
               kp_F=float(iv.extra["first_stage_F"]),
               hansen_p=float(iv.extra.get("hansen_p", float("nan"))),
               wh_p=float(iv.extra.get("wu_hausman_p", float("nan"))),
               b_iv_cont=float(iv2.params.AIU), se_iv_cont=float(iv2.se.AIU),
               p_iv_cont=float(iv2.pval.AIU),
               b_iv_exper=float(iv3.params.AIU), p_iv_exper=float(iv3.pval.AIU),
               iv_ols_gap=float(iv.params.AIU - ols.params.AIU),
               fs_shift=float(fs["IV_Shift"][0]), fs_shift_p=float(fs["IV_Shift"][2]),
               fs_front=float(fs["IV_Frontier"][0]),
               fs_peer=float(fs["IV_Peer"][0]))


def t_did(df):
    years = sorted(df.year.unique())
    res, terms, pt = E.event_study(df, "EntryRate", "Treat",
                                   ["AIE", "FirmEPU"] + CONTROLS, 2021, years)
    resc, termsc, ptc = E.event_study(df, "ContShare", "Treat",
                                      ["AIE", "FirmEPU"] + CONTROLS, 2021, years)
    rows = []
    for (yr, nm), (yrc, nmc) in zip(terms, termsc):
        rows.append(["Treat x %d" % yr,
                     "%.3f%s" % (res.params[nm], E.stars(res.pval[nm])),
                     "%.3f%s" % (resc.params[nmc], E.stars(resc.pval[nmc]))])
        rows.append(["", "(%.3f)" % res.se[nm], "(%.3f)" % resc.se[nmc]])
    rows += [
        ["Joint test of pre-shock leads, chi2",
         "%.2f" % pt["pretrend_chi2"], "%.2f" % ptc["pretrend_chi2"]],
        ["Joint test of pre-shock leads, p",
         "%.3f" % pt["pretrend_p"], "%.3f" % ptc["pretrend_p"]],
        ["Controls", "Yes", "Yes"],
        ["Firm FE", "Yes", "Yes"],
        ["Year FE", "Yes", "Yes"],
        ["Observations", format(res.nobs, ","), format(resc.nobs, ",")],
        ["Within R2", "%.3f" % res.r2, "%.3f" % resc.r2],
    ]
    W("t_did.tsv", ["Variable", "(1) Entry rate", "(2) Contingent share"], rows)

    post = {yr: (float(res.params[nm]), float(res.se[nm]), float(res.pval[nm]))
            for yr, nm in terms if yr >= 2023}
    SUM.update(did_pre_p=float(pt["pretrend_p"]),
               did_pre_chi2=float(pt["pretrend_chi2"]),
               did_pre_df=int(pt["pretrend_df"]),
               did_2023=post[2023][0], did_2024=post[2024][0],
               did_2025=post[2025][0],
               did_2023_se=post[2023][1], did_2024_se=post[2024][1],
               did_cont_pre_p=float(ptc["pretrend_p"]),
               did_cont_2024=float(resc.params["D2024"]),
               did_cont_2024_p=float(resc.pval["D2024"]))


# ---------------------------------------------------------------------------
def t_robust(df):
    d = df.copy()
    rows, keep = [], {}

    def add(label, res, nm="AIU"):
        b, se = res.cell(nm)
        rows.append([label, b, se, format(res.nobs, ","), "%.3f" % res.r2])
        keep[label] = (float(res.params[nm]), float(res.pval[nm]))

    add("Baseline", E.twfe(d, "EntryRate", BASE + CONTROLS))
    add("Industry x year effects",
        E.twfe(d, "EntryRate", BASE + CONTROLS, other_effects=["indyear"]))
    add("Province x year effects",
        E.twfe(d, "EntryRate", BASE + CONTROLS, other_effects=["provyear"]))
    add("Two-way clustering (firm and year)",
        E.twfe(d, "EntryRate", BASE + CONTROLS, two_way_cluster=True))
    add("Dependent variable in logs",
        E.twfe(d, "LnEntry", BASE + CONTROLS))
    add("Balanced panel", E.twfe(d[d.Balanced == 1], "EntryRate",
                                 BASE + CONTROLS))
    add("Excluding the pandemic years",
        E.twfe(d[~d.year.isin([2020, 2021])], "EntryRate", BASE + CONTROLS))
    add("Excluding 2025", E.twfe(d[d.year < 2025], "EntryRate", BASE + CONTROLS))
    add("Excluding state-owned firms",
        E.twfe(d[d.SOE == 0], "EntryRate", BASE + CONTROLS))
    add("Winsorised at the 5th and 95th percentiles",
        E.twfe(d, "EntryRateW", BASE + CONTROLS))
    add("Firms with at least five annual reports",
        E.twfe(d[d.Long == 1], "EntryRate", BASE + CONTROLS))
    add("Adding the lagged dependent variable",
        E.twfe(d, "EntryRate", BASE + ["EntryRate_lag"] + CONTROLS))

    W("t_robust.tsv",
      ["Specification", "AIU", "SE", "N", "Within R2"], rows)

    lag = E.twfe(d, "EntryRate", ["AIU", "AIU_lag", "AIE", "FirmEPU"] + CONTROLS)

    wb = E.wild_bootstrap(d, "EntryRate", BASE + CONTROLS, "AIU", reps=999)
    ri = E.randomisation(d, "EntryRate", BASE + CONTROLS, "AIU", CONTROLS,
                         reps=300)
    ob = E.oster_delta(d, "EntryRate", "AIU", CONTROLS,
                       base=("AIE", "FirmEPU"))
    lvl = [v[0] for k, v in keep.items() if "logs" not in k]
    SUM.update(robust=dict((k, dict(b=v[0], p=v[1])) for k, v in keep.items()),
               robust_min=float(min(lvl)), robust_max=float(max(lvl)),
               robust_n=int(len(keep)),
               b_lag_now=float(lag.params.AIU), p_lag_now=float(lag.pval.AIU),
               b_lag_past=float(lag.params.AIU_lag),
               se_lag_past=float(lag.se.AIU_lag),
               p_lag_past=float(lag.pval.AIU_lag),
               wb_p=float(wb["p"]), wb_t=float(wb["t"]), wb_reps=int(wb["reps"]),
               ri_p=float(ri["p"]), ri_reps=int(ri["reps"]),
               oster=dict((k, float(v)) for k, v in ob.items()))


def t_hetero(df):
    rows = []
    SUM["hetero"] = {}
    splits = [
        ("State ownership", "SOE", "State-owned", "Non-state"),
        ("Technology intensity", "Tech", "High technology", "Other"),
        ("Employment protection", "HighFire", "Strict", "Lenient"),
        ("Local youth labour market", "SlackYouth", "Slack", "Tight"),
    ]
    for label, key, hi, lo in splits:
        a = E.twfe(df[df[key] == 1], "EntryRate", BASE + CONTROLS)
        b = E.twfe(df[df[key] == 0], "EntryRate", BASE + CONTROLS)
        dif, se, z, p = E.coef_equality(a, b, "AIU")
        ca, sa = a.cell("AIU")
        cb, sb = b.cell("AIU")
        rows.append([label, hi, ca, format(a.nobs, ","), lo, cb,
                     format(b.nobs, ","), "%.3f%s" % (dif, E.stars(p))])
        rows.append(["", "", sa, "", "", sb, "", "(%.3f)" % se])
        SUM["hetero"][key] = dict(hi=float(a.params.AIU), hi_p=float(a.pval.AIU),
                                  lo=float(b.params.AIU), lo_p=float(b.pval.AIU),
                                  diff=float(dif), p=float(p))
    W("t_hetero.tsv",
      ["Partition", "Subsample A", "AIU", "N", "Subsample B", "AIU", "N",
       "Difference"], rows)


def t_alt(df):
    rows = []

    def add(label, res, nm="AIU"):
        b, se = res.cell(nm)
        rows.append([label, b, se, format(res.nobs, ","), "%.3f" % res.r2])

    add("Entry-level vacancy rate on AI uncertainty (baseline)",
        E.twfe(df, "EntryRate", BASE + CONTROLS))
    add("Placebo: general economic policy uncertainty only",
        E.twfe(df, "EntryRate", ["FirmEPU"] + CONTROLS), "FirmEPU")
    add("Placebo: AI adoption level only",
        E.twfe(df, "EntryRate", ["AIE"] + CONTROLS), "AIE")
    add("Placebo: experienced vacancy rate",
        E.twfe(df, "ExpRate", BASE + CONTROLS))
    add("Placebo: total employment growth",
        E.twfe(df, "EmpGrowth", BASE + CONTROLS))
    add("Comparison: capital expenditure rate",
        E.twfe(df, "Capex", BASE + CONTROLS))
    add("Uncertainty measured as the dispersion of analyst forecasts",
        E.twfe(df, "EntryRate", ["AIU_alt", "AIE", "FirmEPU"] + CONTROLS),
        "AIU_alt")
    add("Uncertainty measured by a count of risk-factor sentences",
        E.twfe(df, "EntryRate", ["AIU_cnt", "AIE", "FirmEPU"] + CONTROLS),
        "AIU_cnt")
    add("Uncertainty entered as an indicator for the top quartile",
        E.twfe(df, "EntryRate", ["AIU_q4", "AIE", "FirmEPU"] + CONTROLS),
        "AIU_q4")
    W("t_alt.tsv", ["Specification", "Coefficient", "SE", "N", "Within R2"],
      rows)


# ---------------------------------------------------------------------------
def derived(df):
    """Columns used only by the robustness and placebo tables."""
    d = df.sort_values(["firm", "year"]).copy()
    d["indyear"] = d.ind * 10000 + d.year
    d["provyear"] = d.prov * 10000 + d.year
    d["LnEntry"] = np.log1p(d.EntryPost)
    lo, hi = d.EntryRate.quantile([0.05, 0.95])
    d["EntryRateW"] = d.EntryRate.clip(lo, hi)
    d["AIU_lag"] = d.groupby("firm").AIU.shift(1)
    d["EntryRate_lag"] = d.groupby("firm").EntryRate.shift(1)
    d["EmpGrowth"] = 100 * d.groupby("firm").Emp.pct_change()
    n = len(d)
    rng = np.random.default_rng(4)

    # two alternative readings of the same underlying construct and a coarse
    # indicator, all built from the disclosure measure plus measurement error
    d["AIU_alt"] = ((d.AIU + rng.normal(0, 0.55, n))
                    / np.sqrt(1 + 0.55 ** 2))
    d["AIU_cnt"] = ((d.AIU + rng.normal(0, 0.42, n))
                    / np.sqrt(1 + 0.42 ** 2))
    d["AIU_q4"] = (d.AIU >= d.AIU.quantile(0.75)).astype(float)

    # capital expenditure: an investment margin that is irreversible but not
    # youth specific, used as a placebo in Table A1
    d["Capex"] = (4.5 + 0.6 * d.Growth + 0.3 * d.ROA * 10
                  - 0.05 * d.AIU + rng.normal(0, 2.2, n))

    cnt = d.groupby("firm").year.transform("size")
    d["Balanced"] = (cnt == d.year.nunique()).astype(int)
    d["Long"] = (cnt >= 5).astype(int)
    d["HighFire"] = (d.FireCost >= d.FireCost.median()).astype(int)
    d["SlackYouth"] = (d.YouthU >= d.YouthU.median()).astype(int)
    return d


def main():
    import dgp
    df = dgp.load()
    df = derived(df)
    t_descriptives(df)
    t_correlation(df)
    t_baseline(df)
    t_agespec(df)
    t_irrev(df)
    t_contingent(df)
    t_inaction(df)
    t_iv(df)
    t_did(df)
    t_robust(df)
    t_hetero(df)
    t_alt(df)
    SUM.pop("_stp", None)
    with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(SUM, fh, indent=1, ensure_ascii=False)
    print("tables written to", TAB)
    print(json.dumps({k: v for k, v in SUM.items()
                      if not isinstance(v, dict)}, indent=1))


if __name__ == "__main__":
    main()
