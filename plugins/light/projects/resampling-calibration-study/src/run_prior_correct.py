"""E5: analytic prior correction (Saerens 2002 / Elkan 2001) as a
data-free alternative to post-hoc calibration for resampled models.

When a model is trained on a resampled (balanced) set with prior
pi_train=0.5 but deployed on the true prior pi_test, the posterior can be
corrected in closed form WITHOUT a held-out calibration set:

    p_corr = (p * r) / (p * r + (1 - p) * s)
    r = pi_test / pi_train,  s = (1 - pi_test) / (1 - pi_train)

This costs no data (unlike Platt/isotonic) and is monotone (no AUC loss).
Compares: baseline / SMOTE-uncalibrated / SMOTE+isotonic / SMOTE+prior-correct.
Outputs experiments/prior_correct.csv
"""
import sys, json
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_experiments as R
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV

PROC = R.PROC; OUT = R.OUT
SEEDS = list(range(10))


def prior_correct(p, pi_train, pi_test):
    """Saerens/Elkan closed-form posterior correction for a prior shift."""
    r = pi_test / pi_train
    s = (1.0 - pi_test) / (1.0 - pi_train)
    num = p * r
    return num / (num + (1.0 - p) * s + 1e-12)


def run_one(X, y, seed):
    """Returns dict of metrics for the four conditions on one seed."""
    pi_test = float(y.mean())            # true minority prior
    rng = np.random.default_rng(seed)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    n = len(y)
    p_base = np.zeros(n); p_smote = np.zeros(n)
    p_iso = np.zeros(n); p_prior = np.zeros(n)
    for tr, te in skf.split(X, y):
        Xtr, ytr, Xte = X[tr], y[tr], X[te]
        # baseline (no resampling)
        mb = HistGradientBoostingClassifier(max_iter=200, random_state=seed).fit(Xtr, ytr)
        p_base[te] = mb.predict_proba(Xte)[:, 1]
        # SMOTE-trained model (pi_train becomes 0.5 after full balancing)
        Xr, yr = R.resample(Xtr, ytr, "smote", rng)
        ms = HistGradientBoostingClassifier(max_iter=200, random_state=seed).fit(Xr, yr)
        ps = ms.predict_proba(Xte)[:, 1]
        p_smote[te] = ps
        # analytic prior correction: data-free, monotone
        p_prior[te] = prior_correct(ps, pi_train=float(yr.mean()), pi_test=pi_test)
        # isotonic post-hoc (costs a held-out split) -- split must be SHUFFLED,
        # otherwise the calibration fold is class-degenerate and isotonic breaks
        perm = np.random.default_rng(seed + 1000).permutation(len(tr))
        cut = int(0.7 * len(tr))
        fit_idx = tr[perm[:cut]]; cal_idx = tr[perm[cut:]]
        Xrf, yrf = R.resample(X[fit_idx], y[fit_idx], "smote", rng)
        bf = HistGradientBoostingClassifier(max_iter=200, random_state=seed).fit(Xrf, yrf)
        cc = CalibratedClassifierCV(bf, method="isotonic", cv="prefit").fit(X[cal_idx], y[cal_idx])
        p_iso[te] = cc.predict_proba(Xte)[:, 1]
    out = {}
    for tag, p in [("base", p_base), ("smote", p_smote),
                   ("smote_iso", p_iso), ("smote_prior", p_prior)]:
        m = R.metrics(y, p)
        for k, v in m.items():
            out[f"{tag}_{k}"] = v
    return out


def main():
    manifest = json.loads((PROC / "manifest.json").read_text(encoding="utf-8"))
    csv_path = OUT / "prior_correct.csv"
    rows = []
    for meta in manifest:
        name = meta["dataset"]
        df = pd.read_parquet(PROC / meta["file"])
        y = df["__target__"].to_numpy().astype(int)
        X = df.drop(columns="__target__").to_numpy(dtype=float)
        if len(y) > 8000:
            rng = np.random.default_rng(0)
            pos = np.where(y == 1)[0]; neg = np.where(y == 0)[0]
            frac = 8000 / len(y)
            keep = np.concatenate([rng.choice(pos, int(len(pos)*frac), replace=False),
                                   rng.choice(neg, int(len(neg)*frac), replace=False)])
            X, y = X[keep], y[keep]
        for seed in SEEDS:
            r = run_one(X, y, seed)
            rows.append({"dataset": name, "ir": meta["imbalance_ratio"], "seed": seed, **r})
        pd.DataFrame(rows).to_csv(csv_path, index=False)   # checkpoint each dataset
        print(f"[OK] {name} done (total {len(rows)})", flush=True)
    print(f"[DONE] {len(rows)} rows -> {csv_path}")


if __name__ == "__main__":
    main()
