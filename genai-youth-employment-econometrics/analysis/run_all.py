# -*- coding: utf-8 -*-
"""Every estimate reported in the manuscript.

Writes one tab-separated file per table into ../tables and a summary.json that
the document builder consumes, so no number in the paper is typed by hand.
"""
from __future__ import annotations

import json
import os
import warnings

import numpy as np
import pandas as pd
from scipy import stats

import econtools as E

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))
os.makedirs(TAB, exist_ok=True)

CONTROLS = ["Size", "Lev", "ROE", "Growth", "Age", "Board", "Indep", "Dual",
            "TobinQ", "Fixed"]
BASE_YEAR = 2022
SUM = {}


def W(name, header, rows):
    with open(os.path.join(TAB, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join("" if v is None else str(v) for v in r) + "\n")


def load():
    df = pd.read_csv(os.path.join(DATA, "panel.csv"))
    df["GenAI_OLC"] = df.GenAI * df.OLC
    df["GenAI_AIGov"] = df.GenAI * df.AIGov
    df["GenAI_D"] = (df.GenAI > df.loc[df.Post == 1, "GenAI"].median()).astype(float)
    df["IndYear"] = df.ind * 10000 + df.year
    df["ProvYear"] = df.prov * 10000 + df.year
    df = df.sort_values(["firm", "year"])
    df["GenAI_lag"] = df.groupby("firm")["GenAI"].shift(1)
    return df


# ---------------------------------------------------------------------------
def t_descriptives(df):
    keep = ["Youth", "Youth35", "GenAI", "RTI", "HCU", "OLC", "AIGov"] + CONTROLS
    rows = []
    for v in keep:
        s = df[v].dropna()
        rows.append([v, f"{len(s):,}", f"{s.mean():.3f}", f"{s.std():.3f}",
                     f"{s.quantile(.25):.3f}", f"{s.median():.3f}",
                     f"{s.quantile(.75):.3f}", f"{s.min():.3f}",
                     f"{s.max():.3f}"])
    W("t_descriptives.tsv",
      ["Variable", "N", "Mean", "SD", "P25", "Median", "P75", "Min", "Max"], rows)
    SUM["n_obs"] = int(len(df))
    SUM["n_firms"] = int(df.firm.nunique())
    SUM["years"] = f"{int(df.year.min())}-{int(df.year.max())}"
    SUM["youth_mean"] = float(df.Youth.mean())
    SUM["youth_sd"] = float(df.Youth.std())
    SUM["genai_sd"] = float(df.GenAI.std())
    SUM["genai_post_mean"] = float(df.loc[df.Post == 1, "GenAI"].mean())


def t_correlation(df):
    keep = ["Youth", "GenAI", "RTI", "HCU"] + CONTROLS
    C = df[keep].corr()
    n = len(df)
    rows = []
    for i, a in enumerate(keep):
        cells = []
        for j, b in enumerate(keep):
            if j > i:
                cells.append("")
            elif j == i:
                cells.append("1.000")
            else:
                r = C.loc[a, b]
                t = r * np.sqrt((n - 2) / max(1 - r ** 2, 1e-12))
                p = 2 * (1 - stats.norm.cdf(abs(t)))
                cells.append(f"{r:.3f}{E.stars(p)}")
        rows.append([a] + cells)
    # variance inflation factors
    import statsmodels.api as sm
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    X = sm.add_constant(df[["GenAI"] + CONTROLS].dropna().to_numpy(float))
    vifs = [variance_inflation_factor(X, k) for k in range(1, X.shape[1])]
    SUM["vif_max"] = float(max(vifs))
    SUM["vif_mean"] = float(np.mean(vifs))
    W("t_correlation.tsv", ["Variable"] + keep, rows)
    W("t_vif.tsv", ["Variable", "VIF"],
      [[v, f"{x:.2f}"] for v, x in zip(["GenAI"] + CONTROLS, vifs)])


# ---------------------------------------------------------------------------
def t_baseline(df):
    specs = [
        ("(1)", dict(xs=["GenAI"], other=None)),
        ("(2)", dict(xs=["GenAI"] + CONTROLS, other=None)),
        ("(3)", dict(xs=["ExpPost"] + CONTROLS, other=None)),
        ("(4)", dict(xs=["GenAI"] + CONTROLS, other="IndYear")),
        ("(5)", dict(xs=["GenAI"] + CONTROLS, other="ProvYear")),
    ]
    res = {}
    for lab, s in specs:
        res[lab] = E.twfe(df, "Youth", s["xs"], other_effects=s["other"])

    order = ["GenAI", "ExpPost"] + CONTROLS
    rows = []
    for v in order:
        top, bot = [v], [""]
        for lab, _ in specs:
            a, b = res[lab].cell(v)
            top.append(a)
            bot.append(b)
        if any(x for x in top[1:]):
            rows.append(top)
            rows.append(bot)
    rows.append(["Firm FE"] + ["Yes"] * len(specs))
    rows.append(["Year FE"] + ["Yes"] * len(specs))
    rows.append(["Industry x year FE"] + ["No", "No", "No", "Yes", "No"])
    rows.append(["Province x year FE"] + ["No", "No", "No", "No", "Yes"])
    rows.append(["Observations"] + [f"{res[l].nobs:,}" for l, _ in specs])
    rows.append(["Within R2"] + [f"{res[l].r2:.3f}" for l, _ in specs])
    W("t_baseline.tsv", ["Variable"] + [l for l, _ in specs], rows)

    b = res["(2)"].params["GenAI"]
    SUM["beta_baseline"] = float(b)
    SUM["se_baseline"] = float(res["(2)"].se["GenAI"])
    SUM["p_baseline"] = float(res["(2)"].pval["GenAI"])
    SUM["econ_sd"] = float(b * SUM["genai_sd"])
    SUM["econ_pct"] = float(100 * b * SUM["genai_sd"] / SUM["youth_mean"])
    SUM["beta_expost"] = float(res["(3)"].params["ExpPost"])
    SUM["se_expost"] = float(res["(3)"].se["ExpPost"])
    return res


def t_eventstudy(df):
    d = df.copy()
    yrs = sorted(d.year.unique())
    names = []
    for y in yrs:
        if y == BASE_YEAR:
            continue
        nm = f"E{y}"
        d[nm] = d.Exposure * (d.year == y)
        names.append(nm)
    r = E.twfe(d, "Youth", names + CONTROLS)
    rows = []
    for y in yrs:
        if y == BASE_YEAR:
            rows.append([str(y), "0.000", "(—)", "—", "—"])
            continue
        nm = f"E{y}"
        b, se = r.params[nm], r.se[nm]
        rows.append([str(y), f"{b:.3f}{E.stars(r.pval[nm])}", f"({se:.3f})",
                     f"{b - 1.96 * se:.3f}", f"{b + 1.96 * se:.3f}"])
    W("t_eventstudy.tsv",
      ["Year", "Coefficient", "SE", "CI low", "CI high"], rows)

    pre = [f"E{y}" for y in yrs if y < BASE_YEAR]
    b = r.params[pre].to_numpy()
    V = r.cov.loc[pre, pre].to_numpy()
    wald = float(b @ np.linalg.solve(V, b))
    SUM["pretrend_chi2"] = wald
    SUM["pretrend_df"] = len(pre)
    SUM["pretrend_p"] = float(1 - stats.chi2.cdf(wald, len(pre)))
    np.save(os.path.join(TAB, "eventstudy.npy"),
            np.array([[y, (0.0 if y == BASE_YEAR else r.params[f"E{y}"]),
                       (0.0 if y == BASE_YEAR else r.se[f"E{y}"])]
                      for y in yrs]))
    return r


# ---------------------------------------------------------------------------
def t_mechanism(df):
    cols = {}
    cols["(1)"] = E.twfe(df, "Youth", ["GenAI"] + CONTROLS)
    cols["(2)"] = E.twfe(df, "RTI", ["GenAI"] + CONTROLS)
    cols["(3)"] = E.twfe(df, "Youth", ["GenAI", "RTI"] + CONTROLS)
    cols["(4)"] = E.twfe(df, "HCU", ["GenAI"] + CONTROLS)
    cols["(5)"] = E.twfe(df, "Youth", ["GenAI", "HCU"] + CONTROLS)

    dep = ["Youth", "RTI", "Youth", "HCU", "Youth"]
    rows = [["Dependent variable"] + dep]
    for v in ["GenAI", "RTI", "HCU"] + CONTROLS:
        top, bot = [v], [""]
        for lab in ["(1)", "(2)", "(3)", "(4)", "(5)"]:
            a, b = cols[lab].cell(v)
            top.append(a)
            bot.append(b)
        if any(x for x in top[1:]):
            rows.append(top)
            rows.append(bot)
    rows.append(["Firm FE"] + ["Yes"] * 5)
    rows.append(["Year FE"] + ["Yes"] * 5)
    rows.append(["Observations"] + [f"{cols[l].nobs:,}" for l in cols])
    rows.append(["Within R2"] + [f"{cols[l].r2:.3f}" for l in cols])
    W("t_mechanism.tsv", ["Variable", "(1)", "(2)", "(3)", "(4)", "(5)"], rows)

    tot = SUM["beta_baseline"]
    boot = {}
    for med in ["RTI", "HCU"]:
        boot[med] = E.bootstrap_mediation(df, "Youth", "GenAI", med, CONTROLS,
                                          n_boot=300)
        boot[med]["share"] = 100 * boot[med]["indirect"] / tot
    W("t_mediation_boot.tsv",
      ["Channel", "a (X → M)", "b (M → Y | X)", "Indirect a × b",
       "95% CI", "Share of total effect", "Direct effect"],
      [["Task routinisation (RTI)",
        f"{boot['RTI']['a']:.3f}", f"{boot['RTI']['b']:.3f}",
        f"{boot['RTI']['indirect']:.3f}",
        f"[{boot['RTI']['ci_low']:.3f}, {boot['RTI']['ci_high']:.3f}]",
        f"{boot['RTI']['share']:.1f}%",
        f"{cols['(3)'].params['GenAI']:.3f}"],
       ["Human-capital upgrading (HCU)",
        f"{boot['HCU']['a']:.3f}", f"{boot['HCU']['b']:.3f}",
        f"{boot['HCU']['indirect']:.3f}",
        f"[{boot['HCU']['ci_low']:.3f}, {boot['HCU']['ci_high']:.3f}]",
        f"{boot['HCU']['share']:.1f}%",
        f"{cols['(5)'].params['GenAI']:.3f}"]])
    SUM["mediation"] = boot
    return cols


def t_moderation(df):
    m1 = E.twfe(df, "Youth", ["GenAI", "GenAI_OLC"] + CONTROLS)
    m2 = E.twfe(df, "Youth", ["GenAI", "GenAI_AIGov", "AIGov"] + CONTROLS)
    m3 = E.twfe(df, "Youth",
                ["GenAI", "GenAI_OLC", "GenAI_AIGov", "AIGov"] + CONTROLS)
    cols = {"(1)": m1, "(2)": m2, "(3)": m3}
    rows = []
    for v in ["GenAI", "GenAI_OLC", "GenAI_AIGov", "AIGov"] + CONTROLS:
        top, bot = [v], [""]
        for lab in cols:
            a, b = cols[lab].cell(v)
            top.append(a)
            bot.append(b)
        if any(x for x in top[1:]):
            rows.append(top)
            rows.append(bot)
    rows.append(["Firm FE"] + ["Yes"] * 3)
    rows.append(["Year FE"] + ["Yes"] * 3)
    rows.append(["Observations"] + [f"{cols[l].nobs:,}" for l in cols])
    rows.append(["Within R2"] + [f"{cols[l].r2:.3f}" for l in cols])
    W("t_moderation.tsv", ["Variable", "(1)", "(2)", "(3)"], rows)

    b1, b3 = m1.params["GenAI"], m1.params["GenAI_OLC"]
    V = np.array([[m1.se["GenAI"] ** 2, 0], [0, m1.se["GenAI_OLC"] ** 2]])
    grid = np.percentile(df.OLC, [5, 10, 25, 50, 75, 90, 95])
    me = []
    for q, g in zip([5, 10, 25, 50, 75, 90, 95], grid):
        eff = b1 + b3 * g
        se = np.sqrt(V[0, 0] + g ** 2 * V[1, 1])
        p = 2 * (1 - stats.norm.cdf(abs(eff / se)))
        me.append([f"P{q}", f"{g:.2f}", f"{eff:.3f}{E.stars(p)}", f"({se:.3f})",
                   f"[{eff - 1.96 * se:.3f}, {eff + 1.96 * se:.3f}]"])
    W("t_marginal.tsv",
      ["Percentile of OLC", "OLC", "Marginal effect", "SE", "95% CI"], me)
    SUM["mod_olc_b1"] = float(b1)
    SUM["mod_olc_b3"] = float(b3)
    SUM["mod_olc_se3"] = float(m1.se["GenAI_OLC"])
    SUM["mod_olc_turn"] = float(-b1 / b3)
    SUM["mod_olc_turn_pct"] = float(stats.percentileofscore(df.OLC, -b1 / b3))
    SUM["mod_gov_b1"] = float(m2.params["GenAI"])
    SUM["mod_gov_b3"] = float(m2.params["GenAI_AIGov"])
    SUM["mod_gov_se3"] = float(m2.se["GenAI_AIGov"])
    SUM["mod_gov_effect"] = float(m2.params["GenAI"] + m2.params["GenAI_AIGov"])
    np.save(os.path.join(TAB, "marginal.npy"),
            np.array([[g, b1 + b3 * g,
                       np.sqrt(V[0, 0] + g ** 2 * V[1, 1])]
                      for g in np.linspace(df.OLC.quantile(.02),
                                           df.OLC.quantile(.98), 120)]))
    return cols


# ---------------------------------------------------------------------------
def t_endogeneity(df):
    iv = E.absorbed_2sls(df, "Youth", "GenAI", CONTROLS,
                         ["IV_Bartik", "IV_Peer"])
    matched, bal, ps = E.psm(df, CONTROLS)
    psm_res = E.twfe(matched, "Youth", ["GenAI"] + CONTROLS)
    eb = E.entropy_balance(df, CONTROLS)
    eb_res = E.twfe(eb, "Youth", ["GenAI"] + CONTROLS, weights="ebw")
    ost = E.oster_delta(df, "Youth", "GenAI", CONTROLS)

    fs = iv.extra["first_stage_coef"]
    rows = [["Dependent variable", "GenAI", "Youth", "Youth", "Youth"]]
    rows.append(["IV_Bartik",
                 f"{fs['IV_Bartik'][0]:.3f}{E.stars(fs['IV_Bartik'][2])}",
                 "", "", ""])
    rows.append(["", f"({fs['IV_Bartik'][1]:.3f})", "", "", ""])
    rows.append(["IV_Peer",
                 f"{fs['IV_Peer'][0]:.3f}{E.stars(fs['IV_Peer'][2])}",
                 "", "", ""])
    rows.append(["", f"({fs['IV_Peer'][1]:.3f})", "", "", ""])
    a, b = iv.cell("GenAI")
    ap, bp = psm_res.cell("GenAI")
    ae, be = eb_res.cell("GenAI")
    rows.append(["GenAI", "", a, ap, ae])
    rows.append(["", "", b, bp, be])
    rows.append(["Controls", "Yes", "Yes", "Yes", "Yes"])
    rows.append(["Firm FE", "Yes", "Yes", "Yes", "Yes"])
    rows.append(["Year FE", "Yes", "Yes", "Yes", "Yes"])
    rows.append(["Kleibergen–Paap rk Wald F", f"{iv.extra['first_stage_F']:.1f}",
                 "", "", ""])
    rows.append(["Stock–Yogo 10% critical value", "19.93", "", "", ""])
    rows.append(["Sargan–Hansen J (p)", "",
                 f"{iv.extra['sargan']:.2f} ({iv.extra['sargan_p']:.3f})",
                 "", ""])
    wh = iv.extra["wu_hausman_p"]
    rows.append(["Wu–Hausman (p)", "",
                 "<0.001" if wh < 0.001 else f"{wh:.3f}", "", ""])
    rows.append(["Observations", f"{iv.nobs:,}", f"{iv.nobs:,}",
                 f"{psm_res.nobs:,}", f"{eb_res.nobs:,}"])
    W("t_endogeneity.tsv",
      ["Variable", "(1) First stage", "(2) 2SLS", "(3) PSM", "(4) Entropy balancing"],
      rows)

    W("t_balance.tsv",
      ["Variable", "Standardised bias, unmatched (%)",
       "Standardised bias, matched (%)", "Bias reduction (%)",
       "t", "p"],
      [[r["var"], f"{r['bias_u']:.1f}", f"{r['bias_m']:.1f}",
        f"{r['reduct']:.1f}", f"{r['t']:.2f}", f"{r['p']:.3f}"]
       for _, r in bal.iterrows()])

    W("t_oster.tsv",
      ["Quantity", "Value"],
      [["Coefficient without controls", f"{ost['beta_uncontrolled']:.3f}"],
       ["R-squared without controls", f"{ost['r2_uncontrolled']:.3f}"],
       ["Coefficient with controls", f"{ost['beta_controlled']:.3f}"],
       ["R-squared with controls", f"{ost['r2_controlled']:.3f}"],
       ["Assumed maximum R-squared (1.3 × R-squared with controls)",
        f"{ost['r_max']:.3f}"],
       ["Bias-adjusted coefficient", f"{ost['beta_star']:.3f}"],
       ["Relative degree of selection that would set the coefficient to zero",
        f"{ost['delta']:.2f}"]])

    np.save(os.path.join(TAB, "balance.npy"),
            bal[["bias_u", "bias_m"]].to_numpy())
    bal.to_csv(os.path.join(TAB, "balance.csv"), index=False)
    SUM["iv_beta"] = float(iv.params["GenAI"])
    SUM["iv_se"] = float(iv.se["GenAI"])
    SUM["iv_p"] = float(iv.pval["GenAI"])
    SUM["iv_F"] = float(iv.extra["first_stage_F"])
    SUM["sargan_p"] = float(iv.extra["sargan_p"])
    SUM["wu_hausman_p"] = float(iv.extra["wu_hausman_p"])
    SUM["psm_beta"] = float(psm_res.params["GenAI"])
    SUM["psm_se"] = float(psm_res.se["GenAI"])
    SUM["psm_n"] = int(psm_res.nobs)
    SUM["eb_beta"] = float(eb_res.params["GenAI"])
    SUM["eb_se"] = float(eb_res.se["GenAI"])
    SUM["oster"] = ost
    SUM["max_abs_bias_matched"] = float(bal.bias_m.abs().max())
    return iv


# ---------------------------------------------------------------------------
def t_robustness(df):
    specs = [
        ("(1) Youth ≤ 35", lambda: E.twfe(df, "Youth35", ["GenAI"] + CONTROLS)),
        ("(2) ln(young headcount)", lambda: E.twfe(df, "LnYoung", ["GenAI"] + CONTROLS)),
        ("(3) Adoption dummy", lambda: E.twfe(df, "Youth", ["GenAI_D"] + CONTROLS)),
        ("(4) One-year lag", lambda: E.twfe(df, "Youth", ["GenAI_lag"] + CONTROLS)),
        ("(5) Two-way clustering", lambda: _twoway(df)),
        ("(6) Excluding 2020", lambda: E.twfe(df[df.year != 2020], "Youth",
                                              ["GenAI"] + CONTROLS)),
        ("(7) Winsorised at 5%", lambda: E.twfe(_wins5(df), "Youth",
                                                ["GenAI"] + CONTROLS)),
        ("(8) Balanced panel", lambda: E.twfe(_balanced(df), "Youth",
                                              ["GenAI"] + CONTROLS)),
    ]
    rows = []
    for lab, f in specs:
        r = f()
        key = "GenAI_D" if "dummy" in lab else ("GenAI_lag" if "lag" in lab else "GenAI")
        a, b = r.cell(key)
        rows.append([lab, a, b, f"{r.nobs:,}", f"{r.r2:.3f}"])
    W("t_robustness.tsv",
      ["Specification", "Coefficient on GenAI", "SE", "Observations",
       "Within R2"], rows)


def _twoway(df):
    from linearmodels.panel import PanelOLS
    d = df.dropna(subset=["Youth", "GenAI"] + CONTROLS).set_index(["firm", "year"])
    r = PanelOLS(d["Youth"], d[["GenAI"] + CONTROLS], entity_effects=True,
                 time_effects=True, drop_absorbed=True).fit(
        cov_type="clustered", cluster_entity=True, cluster_time=True)
    return E.Res(r.params, r.std_errors, r.tstats, r.pvalues, r.nobs,
                 r.rsquared_within)


def _wins5(df):
    d = df.copy()
    for c in ["Youth", "GenAI"] + CONTROLS:
        lo, hi = d[c].quantile([.05, .95])
        d[c] = d[c].clip(lo, hi)
    return d


def _balanced(df):
    n = df.groupby("firm")["year"].count()
    full = n[n == df.year.nunique()].index
    return df[df.firm.isin(full)]


def t_heterogeneity(df):
    splits = [
        ("State ownership", "SOE", "State-owned", "Non-state"),
        ("Technology intensity", "HiTech", "High-technology", "Other"),
        ("Region", "East", "Eastern", "Central and western"),
        ("Capital intensity", None, "Capital-intensive", "Labour-intensive"),
    ]
    rows = []
    for name, col, lab1, lab0 in splits:
        if col is None:
            med = df.Fixed.median()
            hi, lo = df[df.Fixed >= med], df[df.Fixed < med]
        else:
            hi, lo = df[df[col] == 1], df[df[col] == 0]
        r1 = E.twfe(hi, "Youth", ["GenAI"] + CONTROLS)
        r0 = E.twfe(lo, "Youth", ["GenAI"] + CONTROLS)
        d, se, z, p = E.coef_equality(r1, r0, "GenAI")
        a1, b1 = r1.cell("GenAI")
        a0, b0 = r0.cell("GenAI")
        rows.append([name, lab1, a1, b1, f"{r1.nobs:,}", lab0, a0, b0,
                     f"{r0.nobs:,}", f"{d:.3f}", f"{p:.3f}"])
    W("t_heterogeneity.tsv",
      ["Split", "Group 1", "Coefficient 1", "SE 1", "N 1",
       "Group 2", "Coefficient 2", "SE 2", "N 2",
       "Difference", "p (equality)"], rows)


def t_placebo(df, n_perm=500, seed=5):
    rng = np.random.default_rng(seed)
    firms = df.firm.unique()
    expo = df.groupby("firm")["Exposure"].first()
    true = E.twfe(df, "Youth", ["ExpPost"] + CONTROLS).params["ExpPost"]
    draws = np.empty(n_perm)
    for k in range(n_perm):
        perm = pd.Series(rng.permutation(expo.to_numpy()), index=expo.index)
        d = df.copy()
        d["ExpPost"] = d.firm.map(perm) * d.Post
        try:
            draws[k] = E.twfe(d, "Youth", ["ExpPost"] + CONTROLS).params["ExpPost"]
        except Exception:
            draws[k] = np.nan
    draws = draws[~np.isnan(draws)]
    np.save(os.path.join(TAB, "placebo.npy"), draws)
    SUM["placebo_true"] = float(true)
    SUM["placebo_mean"] = float(draws.mean())
    SUM["placebo_sd"] = float(draws.std())
    SUM["placebo_p"] = float(np.mean(np.abs(draws) >= abs(true)))
    SUM["placebo_n"] = int(draws.size)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    df = load()
    t_descriptives(df); print("descriptives")
    t_correlation(df); print("correlation")
    t_baseline(df); print("baseline")
    t_eventstudy(df); print("event study")
    t_mechanism(df); print("mechanism")
    t_moderation(df); print("moderation")
    t_endogeneity(df); print("endogeneity")
    t_robustness(df); print("robustness")
    t_heterogeneity(df); print("heterogeneity")
    t_placebo(df); print("placebo")

    with open(os.path.join(TAB, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(SUM, fh, indent=1, default=float)
    print("\nsummary.json written")
    for k in ["beta_baseline", "se_baseline", "iv_beta", "iv_se", "iv_F",
              "mod_olc_b3", "mod_olc_turn_pct", "placebo_p"]:
        print(f"  {k:22s} {SUM[k]:.4f}")
