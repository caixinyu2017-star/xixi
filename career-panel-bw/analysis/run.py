# -*- coding: utf-8 -*-
"""Estimate every hypothesis four ways and record where the answers differ.

Writes the tables the manuscript reads from. Nothing is simulated: every
number comes from the two real panels loaded in data.py.
"""
import json
import os
import sys
import time

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import data as D                                              # noqa: E402
import estimators as E                                        # noqa: E402
import grid as G                                              # noqa: E402

OUT = os.path.join(ROOT, "tables")
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
S = {}


def log(m):
    print("[%6.1fs] %s" % (time.time() - T0, m))


def tsv(name, header, rows):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(map(str, header)) + "\n")
        for r in rows:
            fh.write("\t".join(str(c) for c in r) + "\n")
    log("   wrote %s (%d rows)" % (name, len(rows)))


def star(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else ""


def f3(x):
    return "%.3f" % x


def ap(p):
    """A probability in APA form: no leading zero, and a floor at .001."""
    return "<.001" if p < .001 else ("%.3f" % p).replace("0.", ".")


# ==========================================================================
# panels
# ==========================================================================
log("loading the two panels ...")
PANEL = {}
for nm in ("NLSW", "NLSY79M"):
    p = D.load(nm)
    if nm == "NLSY79M":
        p.cols["postsec"] = (p["grade"] >= 13).astype(float)
        # hours are annual in this extract; express them in hundreds so the
        # coefficients are readable next to the weekly hours in the NLSW
        p.cols["hours"] = p.cols["hours"] / 100.0
    else:
        # weeks unemployed is recorded per week; a per-week wage coefficient
        # rounds to zero at three decimals, so it is carried in ten-week units
        p.cols["wks_ue"] = p.cols["wks_ue"] / 10.0
    PANEL[nm] = p
    log("   %-8s %d person-years, %d people, %d waves %d-%d"
        % (nm, p.n_obs, p.n_person, p.waves.size, p.waves.min(),
           p.waves.max()))

# reproduce the published benchmark as part of the run, not beside it
_bench = D._benchmark()
S["benchmark_reproduced"] = bool(_bench)
log("   published-benchmark reproduction: %s"
    % ("pass" if _bench else "FAIL"))


def build(h, kind):
    """Design matrix for one hypothesis under one estimator."""
    p = PANEL[h["panel"]]
    focal, mod = h["focal"], h["mod"]
    ctrl = [c for c in G.CONTROLS[h["panel"]] if c not in (focal, mod)]
    need = sorted(set([focal, mod, "lwage"] + ctrl
                      + (G.PERSON_LEVEL[h["panel"]] if kind != "within"
                         else [])))
    q = p.subset(p.complete(need))

    terms, names = [], []

    def add(v, nm):
        terms.append(np.asarray(v, float))
        names.append(nm)

    add(q[focal], focal)
    add(q[mod], mod)
    add(q[focal] * q[mod], "INT")
    for c in ctrl:
        add(q[c], c)
    if kind != "within":
        for c in G.PERSON_LEVEL[h["panel"]]:
            if c not in (focal, mod) and c not in ctrl:
                add(q[c], c)
    # calendar time. In the balanced NLSY79 extract experience rises by
    # exactly one year in every year for every man, so year dummies would
    # absorb it; those specifications carry a linear trend instead.
    collinear = (h["panel"] == "NLSY79M" and focal == "exper")
    yrs = sorted(set(q["year"].tolist()))[1:]
    if collinear:
        add(q["year"] - q["year"].min(), "trend")
    else:
        for y in yrs:
            add((q["year"] == y).astype(float), "d%d" % int(y))
    return q, np.column_stack(terms), names, collinear


def _profile(h, r_within, r_hyb):
    """Coefficients needed to draw the implied wage profile for a hypothesis.

    The quadratic term is carried where the specification has one, so the
    drawn profile is the one the model actually implies rather than a
    straight line through the linear term.
    """
    sq = h["focal"] + "sq"
    out = {}
    for tag, res, fo, it, qd in (
            ("within", r_within, h["focal"], "INT", sq),
            ("between", r_hyb, "%s (between)" % h["focal"],
             "INT (between)", sq)):
        d = {}
        for nm, lab in ((fo, "focal"), (it, "int"), (qd, "sq")):
            if nm in res["names"]:
                d[lab] = float(res["b"][res["names"].index(nm)])
            else:
                d[lab] = 0.0
        out[tag] = d
    return out


def drop_constant(X, names, pid=None):
    """Remove columns with no variation (after demeaning, if pid is given)."""
    Z = E.demean(X, pid) if pid is not None else X
    keep = [j for j in range(X.shape[1]) if Z[:, j].std() > 1e-9]
    dropped = [names[j] for j in range(X.shape[1]) if j not in keep]
    return X[:, keep], [names[j] for j in keep], dropped


# ==========================================================================
# estimate every hypothesis four ways
# ==========================================================================
log("estimating %d hypotheses, four ways each ..." % len(G.H))
RES = {}
for h in G.H:
    k = h["key"]
    q, X, names, collinear = build(h, "pooled")

    # ---- pooled across waves
    Xp, np_, _ = drop_constant(X, names)
    r_pool = E.ols(Xp, q["lwage"], q.pid, np_)

    # ---- within person
    q2, X2, n2, _ = build(h, "within")
    Xw, nw, drop_w = drop_constant(X2, n2, q2.pid)
    r_within = E.within(Xw, q2["lwage"], q2.pid, nw)

    # ---- hybrid: separate between and within slopes for the focal term
    #      and the interaction
    tv = [j for j, nmj in enumerate(n2) if nmj in (h["focal"], "INT")]
    rest = [j for j, nmj in enumerate(n2) if j not in tv]
    Xrest, nrest, _ = drop_constant(X2[:, rest], [n2[j] for j in rest])
    r_hyb = E.hybrid(X2[:, tv], Xrest, q2["lwage"], q2.pid,
                     [n2[j] for j in tv], [n2[j] for j in tv],
                     names_extra=nrest)
    ct = E.contrast(r_hyb, "INT (within)", "INT (between)")

    # ---- one wave at a time, as a single-wave study would do it
    cs = []
    for w in sorted(set(q["year"].tolist())):
        m = q["year"] == w
        if m.sum() < 60:
            continue
        Xi, ni, _ = drop_constant(X[m], names)
        if "INT" not in ni:
            continue
        try:
            r = E.ols(Xi, q["lwage"][m], q.pid[m], ni)
        except Exception:
            continue
        c = E.coef(r, "INT")
        cs.append(dict(wave=int(w), n=int(m.sum()), **c))

    RES[k] = dict(
        h=h, n_obs=int(q2.n_obs), n_person=int(q2.n_person),
        collinear=collinear,
        pooled=E.coef(r_pool, "INT"),
        within=E.coef(r_within, "INT"),
        between=E.coef(r_hyb, "INT (between)"),
        within_h=E.coef(r_hyb, "INT (within)"),
        equality=ct,
        focal_within=E.coef(r_within, h["focal"]),
        focal_pooled=E.coef(r_pool, h["focal"]),
        cs=cs,
        r2_pooled=float(r_pool["r2"]),
        r2_within=float(r_within["r2_within"]),
        dropped_within=drop_w,
        sd_within_focal=float(q2.within_sd(h["focal"])),
        sd_between_focal=float(np.nanstd(
            E.person_mean(q2[h["focal"]], q2.pid), ddof=1)),
        mod_share=float(np.mean(q2[h["mod"]])),
        focal_range=[float(np.percentile(q2[h["focal"]], 5)),
                     float(np.percentile(q2[h["focal"]], 95))],
        profile=_profile(h, r_within, r_hyb))
    log("   %-3s %-8s %-8s x %-9s  pooled %+.4f%-3s  within %+.4f%-3s  "
        "equal? p=%.4f"
        % (k, h["panel"], h["focal"], h["mod"],
           RES[k]["pooled"]["b"], star(RES[k]["pooled"]["p"]),
           RES[k]["within"]["b"], star(RES[k]["within"]["p"]),
           ct["p"]))

# ---- multiplicity correction on the sixteen equality tests
keys = [h["key"] for h in G.H]
praw = np.array([RES[k]["equality"]["p"] for k in keys])
order = np.argsort(praw)
m = praw.size
bh = np.empty(m)
run_min = 1.0
for i in range(m - 1, -1, -1):
    j = order[i]
    run_min = min(run_min, praw[j] * m / (i + 1))
    bh[j] = min(run_min, 1.0)
for k, q_ in zip(keys, bh):
    RES[k]["equality"]["q"] = float(q_)

# ==========================================================================
# Table 1 — the panels
# ==========================================================================
log("Table 1: the two panels ...")
rows = []
for nm in ("NLSW", "NLSY79M"):
    p = PANEL[nm]
    rows.append([G.PANEL_LABEL[nm], "person-years", "%d" % p.n_obs, "", ""])
    rows.append(["", "people", "%d" % p.n_person, "", ""])
    rows.append(["", "waves", "%d (%d-%d)"
                 % (p.waves.size, p.waves.min(), p.waves.max()), "", ""])
    for v in ["lwage", "tenure", "exper", "hours", "wks_ue", "union",
              "married", "grade", "collgrad", "postsec", "south", "urban",
              "black"]:
        if v not in p.cols:
            continue
        x = p[v]
        ok = np.isfinite(x)
        if ok.sum() == 0:
            continue
        b = float(np.nanstd(E.person_mean(np.where(ok, x, np.nan),
                                          p.pid)[ok], ddof=1))
        w = p.within_sd(v)
        rows.append(["", G.LABEL.get(v, v), "%.2f" % np.nanmean(x),
                     "%.2f" % b, "%.2f" % w])
tsv("t1_panels.tsv",
    ["panel", "variable", "mean", "between-person SD", "within-person SD"],
    rows)
S["panels"] = {nm: dict(n_obs=int(PANEL[nm].n_obs),
                        n_person=int(PANEL[nm].n_person),
                        n_wave=int(PANEL[nm].waves.size),
                        first=int(PANEL[nm].waves.min()),
                        last=int(PANEL[nm].waves.max()),
                        source=PANEL[nm].source)
              for nm in PANEL}

# ==========================================================================
# Table 2 — the hypotheses
# ==========================================================================
tsv("t2_hypotheses.tsv", ["#", "panel", "focal input", "moderator", "claim"],
    [[h["key"], G.PANEL_LABEL[h["panel"]], G.LABEL[h["focal"]],
      G.LABEL[h["mod"]], h["claim"]] for h in G.H])

# ==========================================================================
# Table 3 — the four estimates of every interaction
# ==========================================================================
log("Table 3: four estimates of each interaction ...")
rows = []
for k in keys:
    r = RES[k]
    csb = [c["b"] for c in r["cs"]]
    rows.append([
        k,
        f3(np.median(csb)) if csb else "\u2014",
        "%s to %s" % (f3(min(csb)), f3(max(csb))) if csb else "—",
        f3(r["pooled"]["b"]) + star(r["pooled"]["p"]),
        f3(r["between"]["b"]) + star(r["between"]["p"]),
        f3(r["within"]["b"]) + star(r["within"]["p"]),
        f3(r["equality"]["diff"]),
        ap(r["equality"]["p"]),
        ap(r["equality"]["q"]),
    ])
tsv("t3_estimates.tsv",
    ["#", "single wave (median)", "single wave (range)", "pooled",
     "between-person", "within-person", "between − within",
     "p (equal)", "q (BH)"], rows)

# ==========================================================================
# Table 4 — where the answers disagree
# ==========================================================================
log("Table 4: disagreement between the estimators ...")
ALPHA = .05


def verdict(c):
    if c["p"] >= ALPHA:
        return "no moderation"
    return "positive" if c["b"] > 0 else "negative"


rows = []
cnt = dict(sign_pw=0, verdict_pw=0, sign_bw=0, verdict_bw=0, opposite_sig=0)
for k in keys:
    r = RES[k]
    vp, vb, vw = (verdict(r["pooled"]), verdict(r["between"]),
                  verdict(r["within"]))
    s_pw = np.sign(r["pooled"]["b"]) != np.sign(r["within"]["b"])
    s_bw = np.sign(r["between"]["b"]) != np.sign(r["within"]["b"])
    cnt["sign_pw"] += int(s_pw)
    cnt["sign_bw"] += int(s_bw)
    cnt["verdict_pw"] += int(vp != vw)
    cnt["verdict_bw"] += int(vb != vw)
    if s_bw and "no moderation" not in (vb, vw):
        cnt["opposite_sig"] += 1
    rows.append([k, G.PANEL_LABEL[r["h"]["panel"]],
                 "%s × %s" % (G.LABEL[r["h"]["focal"]],
                              G.LABEL[r["h"]["mod"]]),
                 vp, vb, vw,
                 "yes" if s_bw else "no",
                 "yes" if vb != vw else "no",
                 "yes" if r["equality"]["q"] < .05 else "no"])
tsv("t4_disagreement.tsv",
    ["#", "panel", "interaction", "pooled verdict", "between-person verdict",
     "within-person verdict", "sign reversed", "verdict changed",
     "between \u2260 within (q<.05)"], rows)
flips, sig_change = cnt["sign_bw"], cnt["verdict_bw"]
both_sig_opposite = cnt["opposite_sig"]
q_sig = sum(1 for k in keys if RES[k]["equality"]["q"] < .05)
S["disagreement"] = dict(n=len(keys), sign_flips=int(flips),
                         verdict_changes=int(sig_change),
                         opposite_and_both_significant=int(both_sig_opposite),
                         between_ne_within_q05=int(q_sig), **cnt)
log("   sign reversed in %d of %d; verdict changed in %d; "
    "between ≠ within (q<.05) in %d"
    % (flips, len(keys), sig_change, q_sig))

# ==========================================================================
# Table 5 — how much a single wave moves the answer
# ==========================================================================
log("Table 5: wave-to-wave variability of the single-wave estimate ...")
rows = []
for k in keys:
    r = RES[k]
    b = np.array([c["b"] for c in r["cs"]])
    p = np.array([c["p"] for c in r["cs"]])
    if b.size == 0:
        continue
    rows.append([k, b.size,
                 f3(b.mean()), f3(b.std(ddof=1)),
                 "%d" % int((p < ALPHA).sum()),
                 "%d" % int(((p < ALPHA) & (b > 0)).sum()),
                 "%d" % int(((p < ALPHA) & (b < 0)).sum()),
                 f3(r["within"]["b"]),
                 "%d" % int((np.sign(b) != np.sign(r["within"]["b"])).sum())])
tsv("t5_wave_variability.tsv",
    ["#", "waves", "mean", "SD", "significant", "significant positive",
     "significant negative", "within-person estimate",
     "waves with opposite sign to within"], rows)

tot_w = sum(len(RES[k]["cs"]) for k in keys)
tot_sig = sum(sum(1 for c in RES[k]["cs"] if c["p"] < ALPHA) for k in keys)
tot_opp = sum(sum(1 for c in RES[k]["cs"]
                  if np.sign(c["b"]) != np.sign(RES[k]["within"]["b"]))
              for k in keys)
tot_sig_opp = sum(sum(1 for c in RES[k]["cs"]
                      if c["p"] < ALPHA
                      and np.sign(c["b"]) != np.sign(RES[k]["within"]["b"]))
                  for k in keys)
wave_n = [c["n"] for k in keys for c in RES[k]["cs"]]
S["waves"] = dict(total=int(tot_w), significant=int(tot_sig),
                  opposite_sign=int(tot_opp),
                  significant_and_opposite=int(tot_sig_opp),
                  share_sig_opposite=(tot_sig_opp / tot_sig
                                      if tot_sig else float("nan")),
                  median_n=float(np.median(wave_n)),
                  min_n=int(min(wave_n)), max_n=int(max(wave_n)))
log("   %d single-wave estimates (median n = %d): %d significant, of which "
    "%d point the opposite way to the within estimate (%.0f%%)"
    % (tot_w, np.median(wave_n), tot_sig, tot_sig_opp,
       100 * tot_sig_opp / max(tot_sig, 1)))

# ==========================================================================
# Table 6 — the focal main effect, for reference
# ==========================================================================
rows = []
for k in keys:
    r = RES[k]
    rows.append([k, G.LABEL[r["h"]["focal"]],
                 f3(r["focal_pooled"]["b"]) + star(r["focal_pooled"]["p"]),
                 f3(r["focal_within"]["b"]) + star(r["focal_within"]["p"]),
                 f3(r["r2_pooled"]), f3(r["r2_within"]),
                 "%d" % r["n_obs"], "%d" % r["n_person"]])
tsv("t6_main_effects.tsv",
    ["#", "focal input", "pooled slope", "within slope", "pooled R²",
     "within R²", "person-years", "people"], rows)

# ==========================================================================
# Table 7 — robustness of the within estimate
# ==========================================================================
log("Table 7: robustness ...")


def first_diff(X, y, pid, time, names):
    """First differences: an alternative to the within transformation."""
    o = np.lexsort((time, pid))
    Xs, ys, ps = X[o], y[o], pid[o]
    same = ps[1:] == ps[:-1]
    dX, dy = (Xs[1:] - Xs[:-1])[same], (ys[1:] - ys[:-1])[same]
    g = ps[1:][same]
    keep = [j for j in range(dX.shape[1]) if dX[:, j].std() > 1e-9]
    return E.ols(dX[:, keep], dy, g, [names[j] for j in keep],
                 intercept=True)


ROB = {}
rows = []
for k in keys:
    h = RES[k]["h"]
    q2, X2, n2, _ = build(h, "within")

    base = RES[k]["within"]

    # (a) people observed at least three times
    cnts = {}
    for pv in q2.pid:
        cnts[pv] = cnts.get(pv, 0) + 1
    m3 = np.array([cnts[pv] >= 3 for pv in q2.pid])
    Xa, na, _ = drop_constant(X2[m3], n2, q2.pid[m3])
    ra = E.within(Xa, q2["lwage"][m3], q2.pid[m3], na)

    # (b) first differences
    Xb_, nb, _ = drop_constant(X2, n2, q2.pid)
    rb = first_diff(Xb_, q2["lwage"], q2.pid, q2["year"], nb)

    # (c) controls stripped back to the focal term, the product and time
    tk = [j for j, nm_ in enumerate(n2)
          if nm_ in (h["focal"], h["mod"], "INT")
          or nm_.startswith("d") or nm_ == "trend"]
    Xc, nc, _ = drop_constant(X2[:, tk], [n2[j] for j in tk], q2.pid)
    rc = E.within(Xc, q2["lwage"], q2.pid, nc)

    ROB[k] = dict(base=base,
                  min3=E.coef(ra, "INT"),
                  fd=E.coef(rb, "INT"),
                  lean=E.coef(rc, "INT"))
    rows.append([k, f3(base["b"]) + star(base["p"]),
                 f3(ROB[k]["min3"]["b"]) + star(ROB[k]["min3"]["p"]),
                 f3(ROB[k]["fd"]["b"]) + star(ROB[k]["fd"]["p"]),
                 f3(ROB[k]["lean"]["b"]) + star(ROB[k]["lean"]["p"])])
tsv("t7_robustness.tsv",
    ["#", "within (baseline)", "3+ waves only", "first differences",
     "minimal controls"], rows)

agree = sum(1 for k in keys
            if np.sign(ROB[k]["base"]["b"]) == np.sign(ROB[k]["fd"]["b"])
            and np.sign(ROB[k]["base"]["b"]) == np.sign(ROB[k]["min3"]["b"])
            and np.sign(ROB[k]["base"]["b"]) == np.sign(ROB[k]["lean"]["b"]))
S["robustness"] = dict(sign_agreement_all_three=int(agree), n=len(keys),
                       detail={k: {kk: vv for kk, vv in ROB[k].items()}
                               for k in keys})
log("   the within estimate keeps its sign under all three variations in "
    "%d of %d hypotheses" % (agree, len(keys)))

# ==========================================================================
# magnitudes
# ==========================================================================
div = np.array([abs(RES[k]["equality"]["diff"]) for k in keys])
scale = np.array([max(abs(RES[k]["within"]["b"]), 1e-9) for k in keys])
S["divergence"] = dict(
    median_abs=float(np.median(div)),
    median_ratio=float(np.median(div / scale)),
    n_between_larger=int(sum(1 for k in keys
                             if abs(RES[k]["between"]["b"])
                             > abs(RES[k]["within"]["b"]))))
log("   median |between − within| = %.4f; median ratio to the within "
    "estimate = %.2f; between larger in %d of %d"
    % (S["divergence"]["median_abs"], S["divergence"]["median_ratio"],
       S["divergence"]["n_between_larger"], len(keys)))

# ==========================================================================
S["results"] = {k: {kk: vv for kk, vv in RES[k].items() if kk != "h"}
                for k in keys}
for k in keys:
    S["results"][k]["hypothesis"] = RES[k]["h"]
S["meta"] = dict(alpha=ALPHA, n_hypotheses=len(keys),
                 runtime_s=round(time.time() - T0, 1), simulated=False,
                 note=("All estimates come from the two public longitudinal "
                       "microdata sets described in data.py. No value in "
                       "this file is simulated."))
with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
    json.dump(S, fh, indent=1, default=float)
log("done in %.1f s" % (time.time() - T0))
