# -*- coding: utf-8 -*-
"""Every table reported in the manuscript, plus tables/summary.json.

Run after analysis/dgp.py.  Each function writes one tab-separated file that
build/tables_spec.py turns into a Word table, and adds its headline numbers to
tables/summary.json, from which the manuscript prose is interpolated.
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
DATA = os.path.join(ROOT, "data")
os.makedirs(TAB, exist_ok=True)

CONTROLS = ["Size", "Lev", "ROE", "Growth", "Age", "Board", "Indep", "Dual",
            "TobinQ", "Fixed"]
IVS = ["IV_Bartik", "IV_Peer", "IV_Exp", "IV_Bartik2", "IV_Peer2", "IV_Exp2"]
SUM = {}


def W(name, header, rows):
    with open(os.path.join(TAB, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(c) for c in r) + "\n")


def mod_frame(df, z):
    """Panel with the two interaction terms for moderator z."""
    d = df.copy()
    d["AIxZ"] = d["AI"] * d[z]
    d["AI2xZ"] = d["AI2"] * d[z]
    return d


# ---------------------------------------------------------------------------
def t_descriptives(df):
    rows = []
    order = ["Youth", "Youth35", "LnYoung", "AI", "AUG", "AUT", "OLC", "AIGov",
             "LCP"] + CONTROLS
    for v in order:
        x = df[v].dropna()
        rows.append([v, f"{len(x):,}", f"{x.mean():.3f}", f"{x.std():.3f}",
                     f"{x.quantile(.25):.3f}", f"{x.median():.3f}",
                     f"{x.quantile(.75):.3f}", f"{x.min():.3f}",
                     f"{x.max():.3f}"])
    W("t_descriptives.tsv",
      ["Variable", "N", "Mean", "SD", "P25", "Median", "P75", "Min", "Max"],
      rows)
    SUM.update(n_obs=int(len(df)), n_firms=int(df.firm.nunique()),
               years="%d-%d" % (df.year.min(), df.year.max()),
               youth_mean=float(df.Youth.mean()), youth_sd=float(df.Youth.std()),
               ai_sd=float(df.AI.std()), ai_max=float(df.AI.max()),
               ai_post_mean=float(df.loc[df.Post == 1, "AI"].mean()),
               ai_post_sd=float(df.loc[df.Post == 1, "AI"].std()))


def t_correlation(df):
    keep = ["Youth", "AI", "AUG", "AUT", "OLC", "AIGov", "LCP", "Size", "Lev"]
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

    # variance inflation factors on the two-way demeaned regressors
    import pyhdfe
    xs = ["AI", "AI2"] + CONTROLS
    ids = df[["firm", "year"]].astype("int64").to_numpy()
    R = pyhdfe.create(ids, drop_singletons=False).residualize(
        df[xs].to_numpy(float))
    vif = []
    for k in range(R.shape[1]):
        y = R[:, k]
        X = np.delete(R, k, axis=1)
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        r2 = 1 - ((y - X @ b) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        vif.append(1 / max(1 - r2, 1e-12))
    W("t_vif.tsv", ["Variable", "VIF"],
      [[v, "%.2f" % f] for v, f in zip(xs, vif)])
    # the squared term is mechanically collinear with its own level, so the
    # reported maximum excludes it
    others = [f for v, f in zip(xs, vif) if v not in ("AI", "AI2")]
    SUM.update(vif_max=float(max(others)), vif_mean=float(np.mean(others)),
               vif_ai=float(vif[0]), vif_ai2=float(vif[1]))


# ---------------------------------------------------------------------------
def t_baseline(df):
    specs = [
        ("(1)", lambda: E.twfe(df, "Youth", ["AI"])),
        ("(2)", lambda: E.twfe(df, "Youth", ["AI"] + CONTROLS)),
        ("(3)", lambda: E.twfe(df, "Youth", ["AI", "AI2"])),
        ("(4)", lambda: E.twfe(df, "Youth", ["AI", "AI2"] + CONTROLS)),
        ("(5)", lambda: E.twfe(df, "Youth", ["AI", "AI2"] + CONTROLS,
                               other_effects=["indyear"])),
        ("(6)", lambda: E.twfe(df, "Youth", ["AI", "AI2"] + CONTROLS,
                               other_effects=["provyear"])),
    ]
    res = [(lab, f()) for lab, f in specs]
    rows = []
    for v in ["AI", "AI2"] + CONTROLS:
        a, b = [], []
        for _, r in res:
            c, s = r.cell(v)
            a.append(c)
            b.append(s)
        rows.append([v] + a)
        rows.append([""] + b)
    for lab, key in (("Controls", None), ("Firm FE", "firm"),
                     ("Year FE", "year"),
                     ("Industry x year FE", "iy"),
                     ("Province x year FE", "py")):
        if key is None:
            rows.append([lab] + ["No" if i in (0, 2) else "Yes"
                                 for i in range(len(res))])
        elif key == "firm":
            rows.append([lab] + ["Yes"] * len(res))
        elif key == "year":
            rows.append([lab] + ["Yes"] * 4 + ["No", "No"])
        elif key == "iy":
            rows.append([lab] + ["No"] * 4 + ["Yes", "No"])
        else:
            rows.append([lab] + ["No"] * 5 + ["Yes"])
    rows.append(["Observations"] + [f"{r.nobs:,}" for _, r in res])
    rows.append(["Within R2"] + ["%.3f" % r.r2 for _, r in res])
    W("t_baseline.tsv", ["Variable"] + [lab for lab, _ in res], rows)

    main = res[3][1]
    SUM.update(b1=float(main.params["AI"]), se1=float(main.se["AI"]),
               p1=float(main.pval["AI"]),
               b2=float(main.params["AI2"]), se2=float(main.se["AI2"]),
               p2=float(main.pval["AI2"]),
               r2_main=float(main.r2), n_main=int(main.nobs),
               b_linear=float(res[1][1].params["AI"]),
               se_linear=float(res[1][1].se["AI"]),
               p_linear=float(res[1][1].pval["AI"]))
    return main


def t_utest(df, main):
    lo, hi = 0.0, float(df.AI.max())
    u = E.utest(main, "AI", "AI2", lo, hi)
    tp = E.turning_point(main, "AI", "AI2")
    tl = E.two_lines(df, "Youth", "AI", CONTROLS, breakpoint=tp["tau"])
    def pv(p):
        return "p < 0.001" if p < 0.001 else "p = %.3f" % p

    rows = [
        ["Data range of AI", "[%.3f, %.3f]" % (lo, hi)],
        ["Slope at the lower extreme", "%.3f (%.3f)" % (u["slope_lo"], u["se_lo"])],
        ["Slope at the upper extreme", "%.3f (%.3f)" % (u["slope_hi"], u["se_hi"])],
        ["Lind\u2013Mehlum test for an inverted U shape",
         "t = %.2f, %s" % (u["t"], pv(u["p"]))],
        ["Extreme point", "%.3f" % tp["tau"]],
        ["Fieller 95% interval for the extreme point",
         "[%.3f, %.3f]" % (tp["ci_low"], tp["ci_high"])],
        ["Share of post-shock observations beyond the extreme point",
         "%.1f%%" % (100 * (df.loc[df.Post == 1, "AI"] > tp["tau"]).mean())],
        ["Two-lines test, slope below the break",
         "%.3f (%s)" % (tl["b_lo"], pv(tl["p_lo"]))],
        ["Two-lines test, slope above the break",
         "%.3f (%s)" % (tl["b_hi"], pv(tl["p_hi"]))],
    ]
    W("t_utest.tsv", ["Quantity", "Value"], rows)
    SUM.update(u_t=float(u["t"]), u_p=float(u["p"]),
               slope_lo=float(u["slope_lo"]), se_slope_lo=float(u["se_lo"]),
               slope_hi=float(u["slope_hi"]), se_slope_hi=float(u["se_hi"]),
               tau=float(tp["tau"]), tau_se=float(tp["se"]),
               tau_lo=float(tp["ci_low"]), tau_hi=float(tp["ci_high"]),
               beyond_pct=float(100 * (df.loc[df.Post == 1, "AI"] > tp["tau"]).mean()),
               cross=float(-main.params["AI"] / main.params["AI2"]),
               beyond_cross_pct=float(
                   100 * (df.loc[df.Post == 1, "AI"]
                          > -main.params["AI"] / main.params["AI2"]).mean()),
               p90_ai=float(df.loc[df.Post == 1, "AI"].quantile(0.90)),
               tl_lo=float(tl["b_lo"]), tl_lo_p=float(tl["p_lo"]),
               tl_hi=float(tl["b_hi"]), tl_hi_p=float(tl["p_hi"]),
               peak_gain=float(main.params["AI"] * tp["tau"]
                               + main.params["AI2"] * tp["tau"] ** 2),
               loss_at_max=float(main.params["AI"] * df.AI.max()
                                 + main.params["AI2"] * df.AI.max() ** 2))
    # fitted curve for the figure
    grid = np.linspace(0, df.AI.max(), 120)
    np.save(os.path.join(TAB, "curve.npy"),
            E.curve(main, "AI", "AI2", grid))
    E.binscatter(df, "Youth", "AI", CONTROLS, nbins=20).to_csv(
        os.path.join(TAB, "bins.csv"), index=False)
    return tp


# ---------------------------------------------------------------------------
def t_mechanism(df):
    r_aug = E.twfe(df, "AUG", ["AI", "AI2"] + CONTROLS)
    r_aut = E.twfe(df, "AUT", ["AI", "AI2"] + CONTROLS)
    r_y = E.twfe(df, "Youth", ["AI", "AI2", "AUG", "AUT"] + CONTROLS)
    res = [("(1) AUG", r_aug), ("(2) AUT", r_aut), ("(3) Youth", r_y)]
    rows = [["Dependent variable", "AUG", "AUT", "Youth"]]
    for v in ["AI", "AI2", "AUG", "AUT"] + CONTROLS:
        a, b = [], []
        for _, r in res:
            c, s = r.cell(v)
            a.append(c)
            b.append(s)
        if not any(a):
            continue
        rows.append([v] + a)
        rows.append([""] + b)
    rows.append(["Controls", "Yes", "Yes", "Yes"])
    rows.append(["Firm FE", "Yes", "Yes", "Yes"])
    rows.append(["Year FE", "Yes", "Yes", "Yes"])
    rows.append(["Observations"] + [f"{r.nobs:,}" for _, r in res])
    rows.append(["Within R2"] + ["%.3f" % r.r2 for _, r in res])
    W("t_mechanism.tsv", ["Variable", "(1)", "(2)", "(3)"], rows)

    tp_aug = E.turning_point(r_aug, "AI", "AI2")
    SUM.update(aug_b1=float(r_aug.params["AI"]), aug_b2=float(r_aug.params["AI2"]),
               aug_se2=float(r_aug.se["AI2"]), aug_turn=float(tp_aug["tau"]),
               aut_b1=float(r_aut.params["AI"]), aut_b2=float(r_aut.params["AI2"]),
               aut_se2=float(r_aut.se["AI2"]),
               ch_aug=float(r_y.params["AUG"]), ch_aug_se=float(r_y.se["AUG"]),
               ch_aut=float(r_y.params["AUT"]), ch_aut_se=float(r_y.se["AUT"]),
               ch_ai=float(r_y.params["AI"]), ch_ai2=float(r_y.params["AI2"]),
               ch_ai_p=float(r_y.pval["AI"]), ch_ai2_p=float(r_y.pval["AI2"]))
    # decomposition of the fitted curve into the two channels
    grid = np.linspace(0, df.AI.max(), 120)
    dec = np.column_stack([
        grid,
        r_y.params["AUG"] * (r_aug.params["AI"] * grid
                             + r_aug.params["AI2"] * grid ** 2),
        r_y.params["AUT"] * (r_aut.params["AI"] * grid
                             + r_aut.params["AI2"] * grid ** 2)])
    np.save(os.path.join(TAB, "decomp.npy"), dec)


# ---------------------------------------------------------------------------
MODS = [("OLC", "Organisational learning capability"),
        ("AIGov", "AI governance"),
        ("LCP", "Labour cost pressure")]


def t_moderation(df):
    cols, taus, shifts = [], [], []
    for z, _ in MODS:
        d = mod_frame(df, z)
        xs = ["AI", "AI2", "AIxZ", "AI2xZ"] + ([z] if z != "OLC" else []) + CONTROLS
        r = E.twfe(d, "Youth", xs)
        cols.append((z, r))
        zs = [0.0, 1.0] if z == "AIGov" else [-1.0, 0.0, 1.0]
        tp, dt = E.mod_turning(r, "AI", "AI2", "AIxZ", "AI2xZ", zs)
        taus.append((z, tp))
        shifts.append((z, dt))

    rows = []
    for v in ["AI", "AI2", "AIxZ", "AI2xZ", "OLC", "AIGov", "LCP"]:
        a, b = [], []
        for _, r in cols:
            c, s = r.cell(v)
            a.append(c)
            b.append(s)
        if not any(a):
            continue
        rows.append([v] + a)
        rows.append([""] + b)
    rows.append(["Controls"] + ["Yes"] * 3)
    rows.append(["Firm FE"] + ["Yes"] * 3)
    rows.append(["Year FE"] + ["Yes"] * 3)
    rows.append(["Observations"] + [f"{r.nobs:,}" for _, r in cols])
    rows.append(["Within R2"] + ["%.3f" % r.r2 for _, r in cols])
    W("t_moderation.tsv",
      ["Variable", "(1) OLC", "(2) AIGov", "(3) LCP"], rows)

    trows = []
    for (z, tp), (_, dt) in zip(taus, shifts):
        lab = {"OLC": ["Low (-1 SD)", "Mean", "High (+1 SD)"],
               "LCP": ["Low (-1 SD)", "Mean", "High (+1 SD)"],
               "AIGov": ["Without disclosure", "With disclosure"]}[z]
        for nm, t in zip(lab, tp):
            trows.append([z, nm, "%.3f" % t["tau"], "(%.3f)" % t["se"],
                          "%.3f" % t["curv"], "", ""])
        trows[-1][5] = "%.3f%s" % (dt["dtau"], E.stars(dt["p"]))
        trows[-1][6] = "(%.3f)" % dt["se"]
    W("t_turning.tsv",
      ["Moderator", "Level of the moderator", "Extreme point", "SE",
       "Curvature", "Displacement", "SE"], trows)

    SUM["moderation"] = {
        z: dict(b4=float(r.params["AIxZ"]), se4=float(r.se["AIxZ"]),
                p4=float(r.pval["AIxZ"]), b5=float(r.params["AI2xZ"]),
                se5=float(r.se["AI2xZ"]), p5=float(r.pval["AI2xZ"]),
                dtau=float(dt["dtau"]), dtau_se=float(dt["se"]),
                dtau_p=float(dt["p"]),
                taus=[dict(z=t["z"], tau=t["tau"], se=t["se"]) for t in tp])
        for (z, r), (_, tp), (_, dt) in zip(cols, taus, shifts)}

    # moderated curves for the figure
    grid = np.linspace(0, df.AI.max(), 120)
    out = {}
    for (z, r) in cols:
        lows, highs = ([0.0, 1.0] if z == "AIGov" else [-1.0, 1.0])
        arr = []
        for zv in (lows, highs):
            b1 = r.params["AI"] + r.params["AIxZ"] * zv
            b2 = r.params["AI2"] + r.params["AI2xZ"] * zv
            arr.append(np.column_stack([grid, b1 * grid + b2 * grid ** 2]))
        out[z] = np.stack(arr)
    np.save(os.path.join(TAB, "modcurves.npy"),
            np.stack([out[z] for z, _ in MODS]))


# ---------------------------------------------------------------------------
def t_endogeneity(df):
    iv = E.absorbed_2sls(df, "Youth", ["AI", "AI2"], CONTROLS, IVS,
                         absorb=["firm", "year"], cluster="firm")
    matched, bal, _ = E.psm(df, CONTROLS)
    psm_res = E.twfe(matched, "Youth", ["AI", "AI2"] + CONTROLS)
    d = E.entropy_balance(df, CONTROLS)
    eb_res = E.twfe(d, "Youth", ["AI", "AI2"] + CONTROLS, weights="ebw")

    fs = iv.extra["first_stage_coef_by"]
    rows = [["Dependent variable", "AI", "AI2", "Youth", "Youth", "Youth"]]
    for nm in IVS:
        a1, s1, p1 = fs["AI"][nm]
        a2, s2, p2 = fs["AI2"][nm]
        rows.append([nm, "%.3f%s" % (a1, E.stars(p1)),
                     "%.3f%s" % (a2, E.stars(p2)), "", "", ""])
        rows.append(["", "(%.3f)" % s1, "(%.3f)" % s2, "", "", ""])
    for v in ("AI", "AI2"):
        cells, ses = [], []
        for r in (iv, psm_res, eb_res):
            c, s = r.cell(v)
            cells.append(c)
            ses.append(s)
        rows.append([v, "", ""] + cells)
        rows.append(["", "", ""] + ses)
    rows.append(["Controls"] + ["Yes"] * 5)
    rows.append(["Firm FE"] + ["Yes"] * 5)
    rows.append(["Year FE"] + ["Yes"] * 5)
    F = iv.extra["first_stage_F_by"]
    rows.append(["Kleibergen-Paap rk Wald F", "%.1f" % F["AI"],
                 "%.1f" % F["AI2"], "", "", ""])
    rows.append(["Hansen J (p)", "", "",
                 "%.2f (%.3f)" % (iv.extra["sargan"], iv.extra["sargan_p"]),
                 "", ""])
    wh = iv.extra["wu_hausman_p"]
    rows.append(["Wu-Hausman (p)", "", "",
                 "<0.001" if wh < 0.001 else "%.3f" % wh, "", ""])
    rows.append(["Observations", f"{iv.nobs:,}", f"{iv.nobs:,}",
                 f"{iv.nobs:,}", f"{psm_res.nobs:,}", f"{eb_res.nobs:,}"])
    W("t_endogeneity.tsv",
      ["Variable", "(1) First stage", "(2) First stage", "(3) 2SLS",
       "(4) PSM", "(5) Entropy balancing"], rows)

    # the bias-reduction ratio is omitted: it is undefined in practice for
    # covariates whose unmatched bias is already close to zero
    W("t_balance.tsv",
      ["Variable", "Standardised bias, unmatched (%)",
       "Standardised bias, matched (%)", "t", "p"],
      [[r["var"], f"{r['bias_u']:.1f}", f"{r['bias_m']:.1f}",
        f"{r['t']:.2f}", f"{r['p']:.3f}"]
       for _, r in bal.iterrows()])
    bal.to_csv(os.path.join(TAB, "balance.csv"), index=False)

    for tag, r in (("iv", iv), ("psm", psm_res), ("eb", eb_res)):
        tp = E.turning_point(r, "AI", "AI2")
        u = E.utest(r, "AI", "AI2", 0.0, float(df.AI.max()))
        SUM.update({tag + "_b1": float(r.params["AI"]),
                    tag + "_se1": float(r.se["AI"]),
                    tag + "_b2": float(r.params["AI2"]),
                    tag + "_se2": float(r.se["AI2"]),
                    tag + "_tau": float(tp["tau"]),
                    tag + "_tau_lo": float(tp["ci_low"]),
                    tag + "_tau_hi": float(tp["ci_high"]),
                    tag + "_u_t": float(u["t"]), tag + "_u_p": float(u["p"])})
    SUM.update(iv_F_ai=float(F["AI"]), iv_F_ai2=float(F["AI2"]),
               hansen_p=float(iv.extra["sargan_p"]),
               wu_hausman_p=float(iv.extra["wu_hausman_p"]),
               psm_n=int(psm_res.nobs),
               max_abs_bias_matched=float(bal.bias_m.abs().max()))


def t_oster(df):
    o = E.oster_delta(df, "Youth", "AI", CONTROLS, base=["AI2"], r_max_mult=1.3)
    rows = [["Coefficient on AI without controls", "%.3f" % o["beta_uncontrolled"]],
            ["Coefficient on AI with controls", "%.3f" % o["beta_controlled"]],
            ["R-squared without controls", "%.3f" % o["r2_uncontrolled"]],
            ["R-squared with controls", "%.3f" % o["r2_controlled"]],
            ["Assumed maximum R-squared (1.3 x R-squared with controls)",
             "%.3f" % o["r_max"]],
            ["Bias-adjusted coefficient on AI", "%.3f" % o["beta_star"]],
            ["Relative degree of selection that would set it to zero",
             "%.2f" % o["delta"]]]
    W("t_oster.tsv", ["Quantity", "Value"], rows)
    SUM["oster"] = {k: float(v) for k, v in o.items()}


# ---------------------------------------------------------------------------
def t_robustness(df):
    rows = []

    def add(label, r, tp=None):
        a1, s1 = r.cell("AI")
        a2, s2 = r.cell("AI2")
        t = tp or E.turning_point(r, "AI", "AI2")
        u = E.utest(r, "AI", "AI2", 0.0, float(df.AI.max()))
        rows.append([label, a1, s1, a2, s2, "%.3f" % t["tau"],
                     "%.2f" % u["t"], f"{r.nobs:,}"])

    add("(1) Youth aged 35 or below", E.twfe(df, "Youth35", ["AI", "AI2"] + CONTROLS))
    add("(2) ln(young headcount)", E.twfe(df, "LnYoung", ["AI", "AI2"] + CONTROLS))
    d = df.copy()
    d["AIc"] = d.AI - d.AI.mean()
    d["AIc2"] = d.AIc ** 2
    rc = E.twfe(d, "Youth", ["AIc", "AIc2"] + CONTROLS)
    rc.params = rc.params.rename({"AIc": "AI", "AIc2": "AI2"})
    rc.se = rc.se.rename({"AIc": "AI", "AIc2": "AI2"})
    rc.pval = rc.pval.rename({"AIc": "AI", "AIc2": "AI2"})
    rc.cov = rc.cov.rename(index={"AIc": "AI", "AIc2": "AI2"},
                           columns={"AIc": "AI", "AIc2": "AI2"})
    tpc = E.turning_point(rc, "AI", "AI2")
    tpc["tau"] += df.AI.mean()
    add("(3) Mean-centred adoption depth", rc, tpc)
    add("(4) Two-way clustered standard errors",
        E.twfe(df, "Youth", ["AI", "AI2"] + CONTROLS, two_way_cluster=True))
    add("(5) Excluding 2020", E.twfe(df[df.year != 2020], "Youth",
                                     ["AI", "AI2"] + CONTROLS))
    add("(6) Post-shock years only", E.twfe(df[df.Post == 1], "Youth",
                                            ["AI", "AI2"] + CONTROLS))
    d5 = df.copy()
    lo, hi = d5.Youth.quantile([.05, .95])
    d5["Youth"] = d5.Youth.clip(lo, hi)
    add("(7) Winsorised at the 5th and 95th percentiles",
        E.twfe(d5, "Youth", ["AI", "AI2"] + CONTROLS))
    bal = df.groupby("firm").year.count()
    add("(8) Balanced panel",
        E.twfe(df[df.firm.isin(bal[bal == df.year.nunique()].index)], "Youth",
               ["AI", "AI2"] + CONTROLS))
    W("t_robustness.tsv",
      ["Specification", "AI", "SE", "AI2", "SE", "Extreme point",
       "U-test t", "N"], rows)


def t_placebo(df, n=500, seed=13):
    """Randomisation inference: permute adoption depth within year and re-test
    the shape.  The distribution of the U-test statistic under the null is the
    reference against which the actual statistic is read."""
    rng = np.random.default_rng(seed)
    out = np.empty(n)
    d = df.copy()
    ai = d.AI.to_numpy().copy()
    yr = d.year.to_numpy()
    idx = {y: np.flatnonzero(yr == y) for y in np.unique(yr)}
    for i in range(n):
        sim = ai.copy()
        for y, pos in idx.items():
            sim[pos] = ai[rng.permutation(pos)]
        d["AI"] = sim
        d["AI2"] = sim ** 2
        try:
            r = E.twfe(d, "Youth", ["AI", "AI2"] + CONTROLS)
            out[i] = E.utest(r, "AI", "AI2", 0.0, float(df.AI.max()))["t"]
        except Exception:
            out[i] = np.nan
    out = out[~np.isnan(out)]
    np.save(os.path.join(TAB, "placebo.npy"), out)
    SUM.update(placebo_n=int(out.size), placebo_mean=float(out.mean()),
               placebo_p=float((out >= SUM["u_t"]).mean()))


# ---------------------------------------------------------------------------
def t_heterogeneity(df):
    splits = [("State ownership", "SOE", "State-owned", "Non-state"),
              ("Technology intensity", "HiTech", "High-technology", "Other"),
              ("Region", "East", "Eastern", "Central and western"),
              ("Firm size", None, "Large", "Small")]
    rows = []
    for name, col, lab1, lab0 in splits:
        if col is None:
            med = df.Size.median()
            hi, lo = df[df.Size >= med], df[df.Size < med]
        else:
            hi, lo = df[df[col] == 1], df[df[col] == 0]
        r1 = E.twfe(hi, "Youth", ["AI", "AI2"] + CONTROLS)
        r0 = E.twfe(lo, "Youth", ["AI", "AI2"] + CONTROLS)
        t1 = E.turning_point(r1, "AI", "AI2")
        t0 = E.turning_point(r0, "AI", "AI2")
        d, se, z, p = E.coef_equality(r1, r0, "AI2")
        rows.append([name, lab1, r1.cell("AI2")[0], "%.3f" % t1["tau"],
                     f"{r1.nobs:,}", lab0, r0.cell("AI2")[0],
                     "%.3f" % t0["tau"], f"{r0.nobs:,}", "%.3f" % p])
    W("t_heterogeneity.tsv",
      ["Split", "Group 1", "AI2", "Extreme point", "N",
       "Group 2", "AI2", "Extreme point", "N", "p (equality)"], rows)


# ---------------------------------------------------------------------------
def main():
    df = pd.read_csv(os.path.join(DATA, "panel.csv"))
    df["indyear"] = df.ind * 100 + (df.year - df.year.min())
    df["provyear"] = df.prov * 100 + (df.year - df.year.min())

    print("descriptives"); t_descriptives(df)
    print("correlation"); t_correlation(df)
    print("baseline"); main_res = t_baseline(df)
    print("u-test"); t_utest(df, main_res)
    print("mechanism"); t_mechanism(df)
    print("moderation"); t_moderation(df)
    print("endogeneity"); t_endogeneity(df)
    print("oster"); t_oster(df)
    print("robustness"); t_robustness(df)
    print("heterogeneity"); t_heterogeneity(df)
    print("placebo"); t_placebo(df)

    with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(SUM, fh, indent=1)
    print("wrote", os.path.join(TAB, "summary.json"))


if __name__ == "__main__":
    main()
