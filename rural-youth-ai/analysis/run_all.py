# -*- coding: utf-8 -*-
"""Train every engine, deploy it on the market, audit it, and write the
tables the manuscript reads. Every number in the paper comes from here.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import market as M                                            # noqa: E402
import engine as E                                            # noqa: E402

TAB = os.path.join(ROOT, "tables")
os.makedirs(TAB, exist_ok=True)
T0 = time.time()

N_SEEDS = 20            # main comparison
N_SEEDS_AUDIT = 8       # audits and the mismatched-oracle check
LOG_ROUNDS = 4          # years of logged administrative matching
ALPHAS = [0.0, 0.25, 0.5, 0.75, 1.0]
ETAS = [0.0, 0.1, 0.2, 0.3]

MIN_EDU = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2}    # admin eligibility by category


def log(msg):
    print("[%7.1fs] %s" % (time.time() - T0, msg), flush=True)


def tsv(name, header, rows):
    with open(os.path.join(TAB, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(map(str, header)) + "\n")
        for r in rows:
            fh.write("\t".join(str(c) for c in r) + "\n")
    log("   wrote %s (%d rows)" % (name, len(rows)))


# ===========================================================================
# per-seed pipeline
# ===========================================================================
def episodes_arrays(mk, Zall, rounds, style=None):
    """Logged history under the administrative policy, as arrays."""
    rows = []
    for _ in range(rounds):
        rows += mk.log_episodes(style=style)
    i_idx = np.array([r[0] for r in rows])
    j_idx = np.array([r[1] for r in rows])
    p_show = np.array([r[2] for r in rows])
    acc = np.array([r[3] for r in rows], float)
    months = np.array([r[4] for r in rows])
    cens = np.array([r[5] for r in rows])
    Z = Zall[i_idx, j_idx].astype(float)
    iw = np.clip(1.0 / np.maximum(p_show, 1e-3), None, 20.0)
    return dict(i=i_idx, j=j_idx, Z=Z, acc=acc, months=months,
                cens=cens, iw=iw)


def train_engines(ep, basis, seed):
    """All learned scorers, on the same logged history."""
    formed = ep["acc"] > 0.5
    Zf = ep["Z"][formed]
    ret24 = (ep["months"][formed] >= M.T_HORIZON).astype(float)
    out = {}
    out["hazard"] = E.HazardScorer(basis).fit(
        Zf, ep["months"][formed], ep["cens"][formed], ep["iw"][formed],
        seed=seed)
    out["hazard_noipw"] = E.HazardScorer(basis).fit(
        Zf, ep["months"][formed], ep["cens"][formed],
        np.ones(formed.sum()), seed=seed)
    out["acc_spline"] = E.LogisticHead(basis).fit(ep["Z"], ep["acc"])
    out["mlp_acc"] = E.MLP(E.D, seed=seed).fit(
        ep["Z"], ep["acc"], epochs=250, seed=seed)
    out["mlp_ret"] = E.MLP(E.D, seed=seed + 1).fit(
        Zf, ret24, iw=ep["iw"][formed], epochs=250, seed=seed)
    out["gbm_ret"] = E.GBM(seed=seed).fit(
        Zf, ret24, iw=ep["iw"][formed], seed=seed)
    return out


def deploy_metrics(oracle_mats, assign):
    """Oracle evaluation of a proposed assignment (vectorised)."""
    ACC, RET, FIT = oracle_mats
    offered = np.flatnonzero(assign >= 0)
    if offered.size == 0:
        return dict(n_offer=0, accept=0, ret24=0, yield100=0, fit=0)
    acc = ACC[offered, assign[offered]]
    ret = RET[offered, assign[offered]]
    fit = FIT[offered, assign[offered]]
    return dict(
        n_offer=int(offered.size),
        accept=float(acc.mean()),
        ret24=float((acc * ret).sum() / acc.sum()),
        yield100=float(100.0 * (acc * ret).mean()),
        fit=float(fit.mean()),
    )


def zsc(x):
    return (x - x.mean()) / (x.std() + 1e-9)


def one_seed(seed, eta=0.0, oracle="regime", do_audit=False,
             do_sweeps=False):
    mk = M.Market(seed=seed, oracle=oracle)
    obs = M.extraction_noise(mk, eta, seed) if eta > 0 else mk
    Zall = E.all_pair_features(mk, obs).astype(np.float32)
    n, m = mk.n, mk.m
    rng = np.random.default_rng(500 + seed)
    ACC = M.accept_matrix(mk)
    RET = M.retention_matrix(mk, oracle)
    _, _, FIT = M.pair_matrices(mk)
    oracle_mats = (ACC, RET, FIT)

    ep = episodes_arrays(mk, Zall, LOG_ROUNDS)
    basis = E.Basis(ep["Z"])
    eng = train_engines(ep, basis, seed)

    Zflat = Zall.reshape(-1, E.D).astype(float)
    s_ret = eng["hazard"].score(Zflat).reshape(n, m)
    s_ret_noipw = eng["hazard_noipw"].score(Zflat).reshape(n, m)
    s_acc = eng["acc_spline"].score(Zflat).reshape(n, m)
    s_mlp_acc = eng["mlp_acc"].score(Zflat).reshape(n, m)
    s_mlp_ret = eng["mlp_ret"].score(Zflat).reshape(n, m)
    s_gbm = eng["gbm_ret"].score(Zflat).reshape(n, m)

    youth_pref = s_acc                    # common youth side for DA engines
    cap = mk.cap

    # ---- ranking quality of the retention scorers (pair-level AUC)
    samp = rng.integers(0, n * m, 6000)
    truth = RET.reshape(-1)[samp]
    med = np.median(truth)
    lab = truth > med

    def auc(scores):
        s = scores.reshape(-1)[samp]
        pos, neg = s[lab], s[~lab]
        return float((pos[:, None] > neg[None, :]).mean())

    aucs = {"RAMT": auc(s_ret), "GBM-Ret": auc(s_gbm),
            "MLP-Ret": auc(s_mlp_ret), "Acc-spline": auc(s_acc)}

    # ---- assignments -------------------------------------------------
    assigns = {}
    # B1 administrative rule: eligibility + wage-rank greedy
    elig = np.ones((n, m), bool)
    for j in range(m):
        elig[:, j] = mk.edu >= MIN_EDU[mk.cat[j]]
    wage_score = np.where(elig, np.broadcast_to(mk.wage[None, :], (n, m)),
                          -1e9)
    assigns["AdminRule"] = E.greedy_fill(wage_score, cap,
                                         rng.permutation(n))
    # B5 first-come queue on the youth's own preferences
    assigns["FCFS"] = E.greedy_fill(youth_pref, cap, rng.permutation(n))
    # B2 platform-style: black-box acceptance score, greedy
    assigns["MLP-Acc"] = E.greedy_fill(s_mlp_acc, cap, rng.permutation(n))
    # B3 interpretable acceptance + DA
    assigns["Logit-Acc+DA"] = E.deferred_acceptance(youth_pref, s_acc, cap)
    # B4 boosted retention, greedy
    assigns["GBM-Ret"] = E.greedy_fill(s_gbm, cap, rng.permutation(n))
    # proposed
    assigns["RAMT"] = E.deferred_acceptance(youth_pref, s_ret, cap)
    # oracle upper bound: DA on the true retention matrix
    assigns["Oracle"] = E.deferred_acceptance(youth_pref, RET, cap)

    # ablation variants
    assigns["GBM-Ret+DA"] = E.deferred_acceptance(youth_pref, s_gbm, cap)
    assigns["RAMT-greedy"] = E.greedy_fill(s_ret, cap, rng.permutation(n))
    assigns["RAMT-noIPW"] = E.deferred_acceptance(youth_pref, s_ret_noipw,
                                                  cap)
    assigns["RAMT-MLPscore"] = E.deferred_acceptance(youth_pref, s_mlp_ret,
                                                     cap)
    assigns["RAMT-alpha1"] = assigns["Logit-Acc+DA"]
    assigns["RAMT-OT"] = E.sinkhorn_assign(zsc(s_ret.reshape(-1))
                                           .reshape(n, m), cap)

    res = {}
    high = mk.edu >= 2                    # college and above
    strata = {}
    for name, a in assigns.items():
        met = deploy_metrics(oracle_mats, a)
        # instability against the retention-priority market: blocking pairs
        # w.r.t. (youth acceptance utility, retention priority), the same
        # normative benchmark for every engine
        met["block"] = E.blocking_pairs(
            a, youth_pref, s_ret, cap, sample=3000,
            rng=np.random.default_rng(900 + seed))
        r_hi = float((a[high] >= 0).mean())
        r_lo = float((a[~high] >= 0).mean())
        met["parity"] = r_hi / (r_lo + 1e-9)
        res[name] = met
        if name in ("RAMT", "Logit-Acc+DA", "MLP-Acc", "AdminRule"):
            st = {}
            for tag, mask in (("high_edu", high), ("low_edu", ~high)):
                got = a[mask]; off = got >= 0
                idx = np.flatnonzero(mask)[off]
                st[tag] = dict(
                    rate=float(off.mean()),
                    ret=float(RET[idx, got[off]].mean()) if off.any()
                    else 0.0,
                    wage=float(mk.wage[got[off]].mean()) if off.any()
                    else 0.0)
            strata[name] = st
    out = dict(metrics=res, aucs=aucs, strata=strata)

    # ---- alpha sweep and abstention ----------------------------------
    if do_sweeps:
        sweep = []
        for a_ in ALPHAS:
            s_mix = (1 - a_) * zsc(s_ret.reshape(-1)) \
                + a_ * zsc(s_acc.reshape(-1))
            asg = E.deferred_acceptance(youth_pref,
                                        s_mix.reshape(n, m), cap)
            met = deploy_metrics(oracle_mats, asg)
            sweep.append(dict(alpha=a_, accept=met["accept"],
                              ret24=met["ret24"],
                              yield100=met["yield100"]))
        out["sweep"] = sweep

        # ensemble abstention on the RAMT assignment
        boots = []
        formed = ep["acc"] > 0.5
        Zf = ep["Z"][formed]
        mn, cn, wn = (ep["months"][formed], ep["cens"][formed],
                      ep["iw"][formed])
        for b in range(5):
            bidx = np.random.default_rng(70 + b).integers(
                0, Zf.shape[0], Zf.shape[0])
            hz = E.HazardScorer(basis).fit(Zf[bidx], mn[bidx], cn[bidx],
                                           wn[bidx], epochs=200,
                                           seed=100 + b)
            boots.append(hz)
        asg = assigns["RAMT"]
        offered = np.flatnonzero(asg >= 0)
        Zoff = np.stack([Zall[i, asg[i]] for i in offered]).astype(float)
        preds = np.stack([hz.score(Zoff) for hz in boots])
        unc = preds.std(axis=0)
        ret = RET[offered, asg[offered]]
        accp = ACC[offered, asg[offered]]
        order = np.argsort(unc)             # most certain first
        rc = []
        for cov in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
            keep = order[:int(round(cov * len(order)))]
            rc.append(dict(coverage=cov,
                           ret24=float((accp[keep] * ret[keep]).sum()
                                       / accp[keep].sum())))
        out["riskcov"] = rc

        # coverage repair: a single priority offset for the graduate
        # stratum, raised until its assignment rate reaches parity
        best = None
        for delta in np.linspace(0.0, 3.0, 31):
            s_adj = s_ret + delta * high[:, None]
            asg2 = E.deferred_acceptance(youth_pref, s_adj, cap)
            r_hi = float((asg2[high] >= 0).mean())
            r_lo = float((asg2[~high] >= 0).mean())
            par = r_hi / (r_lo + 1e-9)
            met2 = deploy_metrics(oracle_mats, asg2)
            if par >= 0.95:
                best = dict(delta=float(delta), parity=par,
                            yield100=met2["yield100"],
                            ret24=met2["ret24"])
                break
        out["fair_fix"] = best

    # ---- audits ------------------------------------------------------
    if do_audit:
        out["audit"] = run_audits(mk, Zall, assigns, eng, basis, rng)
    return out


# ===========================================================================
# audits: reconstruction residual + three decision-level checks
# ===========================================================================
def run_audits(mk, Zall, assigns, eng, basis, rng, n_cases=120):
    ref = Zall.reshape(-1, E.D).astype(float).mean(axis=0)

    def runner_up(score_row, j_star):
        order = np.argsort(-score_row)
        for j in order:
            if j != j_star:
                return int(j)
        return int(order[0])

    systems = {
        "RAMT (ledger)": ("ledger", eng["hazard"], None),
        "RAMT-MLPscore (Shapley)": ("shap", eng["mlp_ret"],
                                    "RAMT-MLPscore"),
        "MLP-Acc (Shapley)": ("shap", eng["mlp_acc"], "MLP-Acc"),
        "GBM-Ret (Shapley)": ("shap", eng["gbm_ret"], "GBM-Ret"),
    }
    out = {}
    for label, (kind, model, aname) in systems.items():
        aname = aname or "RAMT"
        asg = assigns[aname]
        offered = np.flatnonzero(asg >= 0)
        cases = rng.choice(offered, min(n_cases, offered.size),
                           replace=False)
        suff = mini = flip = 0.0
        resid = []
        n_run = 0
        for i in cases:
            j_star = asg[i]
            row = Zall[i].astype(float)
            if kind == "ledger":
                score_fn = lambda X: model.score(X)
            else:
                score_fn = lambda X: model.score(X)
            srow = score_fn(row)
            j_alt = runner_up(srow, j_star)
            d_true = float(srow[j_star] - srow[j_alt])
            if d_true <= 0:
                continue
            n_run += 1
            x, xa = row[j_star], row[j_alt]
            if kind == "ledger":
                phi = model.ledger(np.stack([x, xa]))
                dphi = phi[0] - phi[1]
                resid.append(abs(d_true - dphi.sum())
                             / (abs(d_true) + 1e-9))
            else:
                p1 = E.sampled_shapley(score_fn, x, ref, n_perm=48,
                                       rng=rng)
                p2 = E.sampled_shapley(score_fn, xa, ref, n_perm=48,
                                       rng=rng)
                dphi = p1 - p2
                resid.append(abs(d_true - dphi.sum())
                             / (abs(d_true) + 1e-9))

            def flip_fn(k, x=x, xa=xa, score_fn=score_fn):
                xm, xam = x.copy(), xa.copy()
                xm[k] = ref[k]; xam[k] = ref[k]
                return float(score_fn(xm[None])[0]
                             - score_fn(xam[None])[0])

            s_, m_, f_ = E.audit_trail(dphi, d_true, flip_fn=flip_fn)
            suff += s_; mini += m_; flip += f_
        if n_run:
            out[label] = dict(residual=float(np.mean(resid)),
                              sufficiency=suff / n_run,
                              minimality=mini / n_run,
                              flip=flip / n_run, n=n_run)
    return out


# ===========================================================================
def aggregate(per_seed, key_order):
    rows = {}
    for name in key_order:
        vals = {k: [] for k in ("accept", "ret24", "yield100", "fit",
                                "block", "parity")}
        for ps in per_seed:
            met = ps["metrics"].get(name)
            if met:
                for k in vals:
                    vals[k].append(met[k])
        rows[name] = {k: (float(np.mean(v)), float(np.std(v)))
                      for k, v in vals.items()}
    return rows


def main():
    S = {}
    log("=== main comparison over %d seeds ===" % N_SEEDS)
    per_seed = []
    for s in range(1, N_SEEDS + 1):
        r = one_seed(s, do_sweeps=(s <= 10), do_audit=False)
        per_seed.append(r)
        log("seed %2d: RAMT yield %.2f vs Admin %.2f vs MLP-Acc %.2f "
            "Oracle %.2f"
            % (s, r["metrics"]["RAMT"]["yield100"],
               r["metrics"]["AdminRule"]["yield100"],
               r["metrics"]["MLP-Acc"]["yield100"],
               r["metrics"]["Oracle"]["yield100"]))

    MAIN = ["AdminRule", "FCFS", "MLP-Acc", "Logit-Acc+DA", "GBM-Ret",
            "RAMT", "Oracle"]
    agg = aggregate(per_seed, MAIN + ["GBM-Ret+DA", "RAMT-greedy",
                                      "RAMT-noIPW", "RAMT-MLPscore",
                                      "RAMT-alpha1", "RAMT-OT"])
    S["main"] = agg
    rows = []
    for name in MAIN:
        a = agg[name]
        rows.append([name,
                     "%.3f (%.3f)" % a["accept"],
                     "%.3f (%.3f)" % a["ret24"],
                     "%.2f (%.2f)" % a["yield100"],
                     "%.3f (%.3f)" % a["fit"],
                     "%.4f (%.4f)" % a["block"],
                     "%.2f (%.2f)" % a["parity"]])
    tsv("t1_matching.tsv",
        ["Engine", "Offer acceptance", "24m retention (formed)",
         "Stay-yield per 100 offers", "Mean skill fit",
         "Blocking-pair rate", "Parity (high/low schooling)"], rows)

    # strata quality by engine
    st_agg = {}
    for name in ("RAMT", "Logit-Acc+DA", "MLP-Acc", "AdminRule"):
        st_agg[name] = {}
        for tag in ("high_edu", "low_edu"):
            for f in ("rate", "ret", "wage"):
                vals = [ps["strata"][name][tag][f] for ps in per_seed]
                st_agg[name]["%s_%s" % (tag, f)] = (
                    float(np.mean(vals)), float(np.std(vals)))
    S["strata"] = st_agg

    # AUCs
    auc_named = {}
    for k in per_seed[0]["aucs"]:
        vals = [ps["aucs"][k] for ps in per_seed]
        auc_named[k] = (float(np.mean(vals)), float(np.std(vals)))
    S["aucs"] = auc_named

    # ---- ablation table ----------------------------------------------
    ABL = [("RAMT (full)", "RAMT"),
           ("boosted-tree scorer with deferred acceptance", "GBM-Ret+DA"),
           ("acceptance-trained scorer (alpha = 1)", "RAMT-alpha1"),
           ("MLP scorer in place of additive splines", "RAMT-MLPscore"),
           ("greedy fill in place of deferred acceptance", "RAMT-greedy"),
           ("no inverse-propensity weighting", "RAMT-noIPW"),
           ("Sinkhorn transport in place of deferred acceptance",
            "RAMT-OT")]
    rows = []
    for label, key in ABL:
        a = agg[key]
        rows.append([label,
                     "%.2f (%.2f)" % a["yield100"],
                     "%.3f (%.3f)" % a["ret24"],
                     "%.4f (%.4f)" % a["block"],
                     "%.2f (%.2f)" % a["parity"]])
    tsv("t3_ablation.tsv",
        ["Variant", "Stay-yield per 100 offers", "24m retention (formed)",
         "Blocking-pair rate", "Parity"], rows)

    # ---- sweeps -------------------------------------------------------
    sw_seeds = [ps for ps in per_seed if "sweep" in ps]
    sweep_avg = []
    for k, a_ in enumerate(ALPHAS):
        acc = np.mean([ps["sweep"][k]["accept"] for ps in sw_seeds])
        ret = np.mean([ps["sweep"][k]["ret24"] for ps in sw_seeds])
        yl = np.mean([ps["sweep"][k]["yield100"] for ps in sw_seeds])
        ysd = np.std([ps["sweep"][k]["yield100"] for ps in sw_seeds])
        sweep_avg.append(dict(alpha=a_, accept=float(acc),
                              ret24=float(ret), yield100=float(yl),
                              yield_sd=float(ysd)))
    S["sweep"] = sweep_avg
    rc_avg = []
    for k, cov in enumerate((0.5, 0.6, 0.7, 0.8, 0.9, 1.0)):
        vals = [ps["riskcov"][k]["ret24"] for ps in sw_seeds]
        rc_avg.append(dict(coverage=cov, ret24=float(np.mean(vals)),
                           sd=float(np.std(vals))))
    S["riskcov"] = rc_avg
    fixes = [ps["fair_fix"] for ps in sw_seeds if ps.get("fair_fix")]
    if fixes:
        S["fair_fix"] = dict(
            n=len(fixes),
            delta=float(np.mean([f["delta"] for f in fixes])),
            parity=float(np.mean([f["parity"] for f in fixes])),
            yield100=float(np.mean([f["yield100"] for f in fixes])),
            ret24=float(np.mean([f["ret24"] for f in fixes])))

    # ---- audits over N_SEEDS_AUDIT seeds ------------------------------
    log("=== audits over %d seeds ===" % N_SEEDS_AUDIT)
    audit_acc = {}
    for s in range(1, N_SEEDS_AUDIT + 1):
        r = one_seed(s, do_audit=True)
        for k, v in r["audit"].items():
            audit_acc.setdefault(k, []).append(v)
        log("audit seed %d done" % s)
    rows = []
    S["audit"] = {}
    for k, vs in audit_acc.items():
        d = {f: (float(np.mean([v[f] for v in vs])),
                 float(np.std([v[f] for v in vs])))
             for f in ("residual", "sufficiency", "minimality", "flip")}
        S["audit"][k] = d
        rows.append([k,
                     "%.4f (%.4f)" % d["residual"],
                     "%.3f (%.3f)" % d["sufficiency"],
                     "%.3f (%.3f)" % d["minimality"],
                     "%.3f (%.3f)" % d["flip"]])
    tsv("t2_audit.tsv",
        ["System (trail)", "Reconstruction residual",
         "Sufficiency pass", "Minimality pass", "Counterfactual flip pass"],
        rows)

    # ---- mismatched-generator validity --------------------------------
    log("=== mismatched-oracle validity over %d seeds ===" % N_SEEDS_AUDIT)
    mm_seed = []
    for s in range(1, N_SEEDS_AUDIT + 1):
        mm_seed.append(one_seed(s, oracle="logistic"))
        log("mismatched seed %d done" % s)
    agg_mm = aggregate(mm_seed, MAIN)
    S["mismatched"] = agg_mm
    rows = []
    for name in MAIN:
        a, b = agg[name], agg_mm[name]
        rows.append([name,
                     "%.2f (%.2f)" % a["yield100"],
                     "%.2f (%.2f)" % b["yield100"]])
    tsv("t4_validity.tsv",
        ["Engine", "Stay-yield, regime-switching oracle",
         "Stay-yield, smooth logistic oracle"], rows)
    # rank concordance between the two oracles
    r1 = [agg[n]["yield100"][0] for n in MAIN]
    r2 = [agg_mm[n]["yield100"][0] for n in MAIN]

    def rankvec(v):
        return np.argsort(np.argsort(v))
    rho = float(np.corrcoef(rankvec(r1), rankvec(r2))[0, 1])
    S["mismatched_rho"] = rho

    # ---- extraction-noise sweep ---------------------------------------
    log("=== extraction-noise sweep ===")
    noise = []
    for eta in ETAS:
        vals_r, vals_m = [], []
        for s in range(1, 7):
            r = one_seed(s, eta=eta)
            vals_r.append(r["metrics"]["RAMT"]["yield100"])
            vals_m.append(r["metrics"]["MLP-Acc"]["yield100"])
        noise.append(dict(eta=eta,
                          ramt=float(np.mean(vals_r)),
                          ramt_sd=float(np.std(vals_r)),
                          mlp=float(np.mean(vals_m)),
                          mlp_sd=float(np.std(vals_m))))
        log("eta %.1f: RAMT %.2f MLP %.2f" % (eta, noise[-1]["ramt"],
                                              noise[-1]["mlp"]))
    S["noise"] = noise

    # ---- corpus description ------------------------------------------
    mk = M.Market(seed=1)
    S["corpus"] = [[str(a), str(b), c] for a, b, c in M.describe(mk)]
    Zc = E.all_pair_features(mk, mk).astype(np.float32)
    ep = episodes_arrays(mk, Zc, LOG_ROUNDS)
    S["logging"] = dict(
        episodes=int(len(ep["acc"])),
        formed=int((ep["acc"] > 0.5).sum()),
        accept_rate=float(ep["acc"].mean()),
        ret24_formed=float(np.mean(
            ep["months"][ep["acc"] > 0.5] >= M.T_HORIZON)))

    S["meta"] = dict(n_seeds=N_SEEDS, n_seeds_audit=N_SEEDS_AUDIT,
                     log_rounds=LOG_ROUNDS, alphas=ALPHAS, etas=ETAS,
                     horizon=M.T_HORIZON,
                     runtime_s=round(time.time() - T0, 1),
                     simulated=True)
    with open(os.path.join(TAB, "summary.json"), "w",
              encoding="utf-8") as fh:
        json.dump(S, fh, indent=1, default=float)
    log("done in %.1f s" % (time.time() - T0))


if __name__ == "__main__":
    main()
