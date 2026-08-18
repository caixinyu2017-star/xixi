# -*- coding: utf-8 -*-
"""The full experimental protocol.

Every model is trained on the same participant-level split with the same
optimiser, schedule and early-stopping rule, over three random
initialisations. The script writes the result tables consumed by the
manuscript build to ../tables/ and a machine-readable summary to
../tables/results.json. No number reported in the manuscript is entered
by hand: all of them are produced here.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

import ema_data as D
from autodiff import bce
from dpapt import DPAPT, train
import baselines as B

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.abspath(os.path.join(HERE, "..", "tables"))
os.makedirs(TAB, exist_ok=True)

SEEDS = (0, 1, 2)
D_MODEL = 32
EPOCHS = 90
BATCH = 48
LAMBDAS = (0.0, 0.005, 0.01, 0.02, 0.05, 0.10, 0.20)
LAM = 0.0           # the proposed model has no attention to sparsify
TOPK = 5
WARMUP = 0
# Learning rates selected on the validation split; the sweep is reported
# in the manuscript so that the comparison is not confounded by tuning.
LR = {"Aggregated logistic regression": 8e-3,
      "Gated recurrent encoder": 4e-3,
      "Self-attentive encoder": 4e-3,
      "Temporal graph encoder": 8e-3,
      "Attentive diagnostic model": 8e-3,
      "DP-APT (proposed)": 4e-3,
      "attention variant": 4e-3}
LR_DEFAULT = 4e-3


def log(msg):
    print(msg, flush=True)


def evaluate(model, X, M, Y, used, weights=None, topk=TOPK):
    pred, alpha = model.forward(X, M)
    S = pred.data
    roc, pr, roc_k, pr_k = B.macro_auc(Y, S)
    out = dict(auc_roc=roc, auc_pr=pr, roc_per_family=roc_k,
               pr_per_family=pr_k, scores=S)
    if weights is None and getattr(model, "_contrib", None) is not None:
        # the evidence trail is the exact per-episode decomposition of the
        # score, not the attention distribution on its own
        weights = model._contrib
    if weights is None and alpha is not None:
        weights = alpha.data
    if weights is not None:
        comp, suff = B.faithfulness(model, X, M, weights, topk=topk)
        out.update(comprehensiveness=comp, sufficiency=suff,
                   alignment=B.justification_alignment(weights, used, M,
                                                       topk=topk),
                   weights=weights)
    # For the models that expose an internal attention and detector, the
    # alignment of those two partial readings is recorded alongside that
    # of the exact decomposition, so that the manuscript can report what
    # is lost by summarising the score with its attention alone.
    if getattr(model, "_contrib", None) is not None:
        ca, sa = B.faithfulness(model, X, M, alpha.data, topk=topk)
        out["comprehensiveness_attention"] = ca
        out["sufficiency_attention"] = sa
        out["alignment_attention"] = B.justification_alignment(
            alpha.data, used, M, topk=topk)
        out["alignment_detector"] = B.justification_alignment(
            model._p_ep.data, used, M, topk=topk)
    return out


def run_variant(name, factory, data, tr, va, te, lam=LAM, ig=False,
                lr=None, mu=None):
    X, M, Y = data["X"], data["mask"].astype(float), data["Y"]
    used = data["used"]
    lr = lr if lr is not None else LR.get(name, LR_DEFAULT)
    runs = []
    for seed in SEEDS:
        t0 = time.time()
        model = factory(seed)
        info = train(model, data, tr, va, epochs=EPOCHS, batch=BATCH,
                     lr=lr, lam=lam, mu=mu, seed=seed, verbose=False,
                     patience=20, warmup=WARMUP)
        w = None
        if ig:
            w = B.integrated_gradients(model, X[te], M[te])
        ev = evaluate(model, X[te], M[te], Y[te], used[te], weights=w)
        ev["epochs"] = info["epochs_run"]
        # the pure validation cross-entropy of the restored checkpoint;
        # the value tracked during training is the full objective, which
        # is not comparable across sparsity weights
        pv, _ = model.forward(X[va], M[va])
        ev["val_bce"] = float(bce(pv, Y[va]).data)
        runs.append((model, ev))
        log("    %-34s seed %d  AUC-ROC %.3f  AUC-PR %.3f  (%.0fs, %d ep)"
            % (name, seed, ev["auc_roc"], ev["auc_pr"], time.time() - t0,
               info["epochs_run"]))
    agg = {}
    for key in ("auc_roc", "auc_pr", "comprehensiveness", "sufficiency",
                "alignment", "comprehensiveness_attention",
                "sufficiency_attention", "alignment_attention",
                "alignment_detector", "val_bce"):
        vals = [r[1][key] for r in runs if key in r[1]]
        if vals:
            agg[key] = float(np.mean(vals))
            agg[key + "_sd"] = float(np.std(vals, ddof=1))
    agg["roc_per_family"] = np.mean(
        [r[1]["roc_per_family"] for r in runs], axis=0).tolist()
    best = int(np.argmin([r[1]["val_bce"] for r in runs]))
    return agg, runs[best][0], runs[best][1]


def main():
    t_start = time.time()
    log("generating the EMA corpus ...")
    data = D.generate()
    tr, va, te = D.splits()
    X, M, Y = data["X"], data["mask"].astype(float), data["Y"]
    log("  %d participants (%d train / %d validation / %d test), "
        "%d scheduled prompts, %d features"
        % (X.shape[0], len(tr), len(va), len(te), X.shape[1], X.shape[2]))

    R = {"config": dict(n_participants=int(X.shape[0]), n_train=len(tr),
                        n_val=len(va), n_test=len(te),
                        t_max=int(X.shape[1]), f_dim=int(X.shape[2]),
                        d_model=D_MODEL, seeds=list(SEEDS),
                        epochs=EPOCHS, batch=BATCH, lam=LAM,
                        warmup=WARMUP, heads=4, layers=2,
                        topk=TOPK, compliance=float(M.mean()),
                        n_families=len(D.FAMILIES))}

    # ---------------- descriptive properties of the corpus ------------
    na = data["X_raw"][:, :, 0]
    ac = []
    for i in range(X.shape[0]):
        v = na[i][data["mask"][i]]
        ac.append(np.corrcoef(v[:-1], v[1:])[0, 1])
    q = data["quest"]
    R["corpus"] = dict(
        inertia_mean=float(np.mean(ac)), inertia_sd=float(np.std(ac)),
        prompts_mean=float(data["mask"].sum(1).mean()),
        prompts_min=int(data["mask"].sum(1).min()),
        prompts_max=int(data["mask"].sum(1).max()),
        prevalence=Y.mean(0).tolist(),
        deployment=[float(((data["used"] == k) & data["mask"]).sum()
                          / data["mask"].sum()) for k in range(5)],
        erq_reap=[float(q["ERQ_reappraisal"].mean()),
                  float(q["ERQ_reappraisal"].std())],
        erq_supp=[float(q["ERQ_suppression"].mean()),
                  float(q["ERQ_suppression"].std())],
        ders=[float(q["DERS_total"].mean()), float(q["DERS_total"].std())],
        chance_alignment=B.chance_alignment(data["used"], M))
    oa, oacc = B.oracle_alignment(X, M, data["used"], tr, te, topk=TOPK)
    R["corpus"]["oracle_alignment"] = oa
    R["corpus"]["oracle_accuracy"] = oacc
    log("  chance alignment %.3f, oracle ceiling %.3f "
        "(episode-level accuracy %.3f)"
        % (R["corpus"]["chance_alignment"], oa, oacc))

    # ---------------- baselines ---------------------------------------
    log("training baselines ...")
    R["models"] = {}
    specs = [
        ("Aggregated logistic regression",
         lambda s: B.AggregateLogistic(D.F_DIM, seed=s), False),
        ("Gated recurrent encoder",
         lambda s: B.GRUSequence(D.F_DIM, d_model=D_MODEL, seed=s), True),
        ("Self-attentive encoder",
         lambda s: B.SelfAttentive(D.F_DIM, d_model=D_MODEL, seed=s), True),
        ("Temporal graph encoder",
         lambda s: B.GraphPooled(D.F_DIM, d_model=D_MODEL, seed=s), False),
        ("Attentive diagnostic model",
         lambda s: B.AttnDiagnostic(D.F_DIM, d_model=D_MODEL, seed=s),
         False),
    ]
    # The comparison models are trained with their own objective. The
    # sparsity and anchoring terms are contributions of the proposed
    # method, so the two variants that reuse its code path are run with
    # both weights at zero rather than inheriting them.
    for name, fac, ig in specs:
        agg, _, _ = run_variant(name, fac, data, tr, va, te, lam=0.0,
                                ig=ig, mu=0.0)
        R["models"][name] = agg

    # ---------------- the proposed model ------------------------------
    # The proposed fusion couples the concept vectors to the episodes
    # through an unnormalised bilinear detector and a prevalence-weighted
    # pool. Normalising that coupling over episodes — turning it into an
    # attention distribution — is the variant reported in the ablation
    # and swept below; validation cross-entropy selects against it.
    log("training the proposed architecture ...")
    proposed = lambda s: DPAPT(D.F_DIM, d_model=D_MODEL, layers=2,
                               use_attn=False, seed=s)
    attn_variant = lambda s: DPAPT(D.F_DIM, d_model=D_MODEL, layers=2,
                                   use_attn=True, seed=s)
    agg, best_model, best_ev = run_variant(
        "DP-APT (proposed)", proposed, data, tr, va, te, lam=0.0)
    R["models"]["DP-APT (proposed)"] = agg

    # ---------------- ablations ---------------------------------------
    log("running the ablation study ...")
    R["ablation"] = {}
    abl = [
        ("without the ontology parser",
         lambda s: DPAPT(D.F_DIM, d_model=D_MODEL, layers=2,
                         use_onto=False, use_attn=False, seed=s),
         0.0, None),
        ("without the temporal graph",
         lambda s: DPAPT(D.F_DIM, d_model=D_MODEL, layers=2,
                         use_graph=False, use_attn=False, seed=s),
         0.0, None),
        ("without the item anchoring term", proposed, 0.0, 0.0),
        ("with attention over episodes", attn_variant, 0.0, None),
    ]
    for name, fac, lam, mu in abl:
        a, _, _ = run_variant(name, fac, data, tr, va, te, lam=lam, mu=mu)
        R["ablation"][name] = a
    R["ablation"]["full model"] = R["models"]["DP-APT (proposed)"]

    # ---------------- sparsity sweep on the attention variant ---------
    # The entropy penalty acts on the attention distribution, so the
    # sweep is run on the variant that has one. It is reported as an
    # analysis of what sparsifying an attention-based explanation buys
    # and costs, not as a tuning of the proposed model.
    log("sweeping the sparsity weight on the attention variant ...")
    R["sparsity_sweep"] = []
    for lam in LAMBDAS:
        a, _, _ = run_variant("attention variant", attn_variant, data,
                              tr, va, te, lam=lam)
        a["lam"] = lam
        R["sparsity_sweep"].append(a)
        log("    lambda %.3f  val BCE %.4f  AUC-ROC %.3f  "
            "comprehensiveness %.3f  alignment %.3f"
            % (lam, a["val_bce"], a["auc_roc"], a["comprehensiveness"],
               a["alignment"]))

    # ---------------- convergent validity -----------------------------
    log("assessing convergent validity ...")
    S = best_ev["scores"]
    idx = te
    pairs = [("Cognitive change score", 3, "ERQ_reappraisal"),
             ("Response modulation score", 4, "ERQ_suppression"),
             ("Mean regulation score", None, "DERS_total")]
    val = {}
    for label, k, qk in pairs:
        v = S.mean(axis=1) if k is None else S[:, k]
        r = float(np.corrcoef(v, q[qk][idx])[0, 1])
        n = len(idx)
        t = r * np.sqrt((n - 2) / max(1e-12, 1 - r * r))
        from scipy import stats as st
        p = float(2 * st.t.sf(abs(t), n - 2))
        val[label] = dict(criterion=qk, r=r, p=p, n=n)
    R["validity"] = val

    # ---------------- attention example for the figure ----------------
    W = best_ev["weights"]
    ex = int(np.argmax([W[i].max() for i in range(W.shape[0])]))
    R["example"] = dict(participant=int(idx[ex]),
                        alignment=float(B.justification_alignment(
                            W[ex:ex + 1], data["used"][idx][ex:ex + 1],
                            M[idx][ex:ex + 1], topk=TOPK)))
    np.save(os.path.join(TAB, "example_attention.npy"), W[ex])
    np.save(os.path.join(TAB, "example_used.npy"), data["used"][idx][ex])
    np.save(os.path.join(TAB, "example_mask.npy"), M[idx][ex])
    np.save(os.path.join(TAB, "test_scores.npy"), S)
    np.save(os.path.join(TAB, "test_labels.npy"), Y[te])

    # How closely do the two ways of judging an explanation agree?
    # Rank correlation across the models that supply both, so that the
    # manuscript can state the relationship instead of asserting one.
    pairs = [(m["comprehensiveness"], m["alignment"])
             for m in R["models"].values() if "alignment" in m]
    from scipy import stats as st
    rho, prho = st.spearmanr([c for c, _ in pairs], [a for _, a in pairs])
    R["criterion_agreement"] = dict(n=len(pairs), spearman_rho=float(rho),
                                    p=float(prho))
    log("  comprehensiveness vs alignment across %d models: "
        "rho = %.2f (p = %.2f)" % (len(pairs), rho, prho))

    R["runtime_seconds"] = time.time() - t_start
    with open(os.path.join(TAB, "results.json"), "w",
              encoding="utf-8") as fh:
        json.dump(R, fh, indent=1)
    log("done in %.0f s; results written to %s"
        % (R["runtime_seconds"], TAB))
    return R


if __name__ == "__main__":
    main()
