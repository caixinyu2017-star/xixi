"""Experiment runner: resampling x calibration on tree ensembles.
REAL data (data/processed/*.parquet), multi-seed, leakage-safe.
Outputs experiments/results.csv (one row per dataset x model x condition x seed).
"""
import sys, json, warnings
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score, brier_score_loss

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
OUT = ROOT / "experiments"
OUT.mkdir(parents=True, exist_ok=True)
SEEDS = list(range(10))
N_SPLITS = 5


def ece(y_true, y_prob, n_bins=10):
    """Expected Calibration Error (equal-width bins)."""
    bins = np.linspace(0, 1, n_bins + 1)
    idx = np.digitize(y_prob, bins) - 1
    idx = np.clip(idx, 0, n_bins - 1)
    e = 0.0
    n = len(y_true)
    for b in range(n_bins):
        m = idx == b
        if m.sum() == 0:
            continue
        conf = y_prob[m].mean()
        acc = y_true[m].mean()
        e += (m.sum() / n) * abs(acc - conf)
    return float(e)


def resample(Xtr, ytr, method, rng, rho=1.0):
    """Leakage-safe: called ONLY on training fold. Returns resampled (X, y)."""
    if method == "none" or method == "cw":
        return Xtr, ytr
    pos = np.where(ytr == 1)[0]; neg = np.where(ytr == 0)[0]
    minority, majority = (pos, neg) if len(pos) < len(neg) else (neg, pos)
    if method == "rus":  # random undersample majority to balance
        keep = rng.choice(majority, size=len(minority), replace=False)
        idx = np.concatenate([minority, keep]); rng.shuffle(idx)
        return Xtr[idx], ytr[idx]
    if method == "ros":  # random oversample minority
        n_add = int(rho * (len(majority) - len(minority)))
        extra = rng.choice(minority, size=max(0, n_add), replace=True)
        idx = np.concatenate([np.arange(len(ytr)), extra]); rng.shuffle(idx)
        return Xtr[idx], ytr[idx]
    if method == "smote":  # SMOTE: interpolate between minority neighbors
        from sklearn.neighbors import NearestNeighbors
        Xmin = Xtr[minority]
        n_add = int(rho * (len(majority) - len(minority)))
        if n_add <= 0 or len(minority) < 2:
            return Xtr, ytr
        k = min(5, len(minority) - 1)
        nn = NearestNeighbors(n_neighbors=k + 1).fit(Xmin)
        _, nbrs = nn.kneighbors(Xmin)
        synth = np.empty((n_add, Xtr.shape[1]))
        for i in range(n_add):
            a = rng.integers(len(Xmin))
            b = nbrs[a, 1 + rng.integers(k)]
            gap = rng.random()
            synth[i] = Xmin[a] + gap * (Xmin[b] - Xmin[a])
        X2 = np.vstack([Xtr, synth])
        y2 = np.concatenate([ytr, np.ones(n_add, dtype=int)])
        idx = np.arange(len(y2)); rng.shuffle(idx)
        return X2[idx], y2[idx]
    raise ValueError(method)


def make_model(kind, cw=None, seed=0):
    if kind == "rf":
        return RandomForestClassifier(n_estimators=120, n_jobs=-1,
                                      class_weight=cw, random_state=seed)
    return HistGradientBoostingClassifier(max_iter=200, random_state=seed,
                                          class_weight=cw)


def metrics(y_true, p):
    return {"ece": ece(y_true, p), "brier": brier_score_loss(y_true, p),
            "auc": roc_auc_score(y_true, p), "pr_auc": average_precision_score(y_true, p),
            "f1": f1_score(y_true, (p >= 0.5).astype(int))}


# conditions: (name, resample_method, class_weight, calibration)
CONDITIONS = [
    ("E0_none",      "none",  None,       None),
    ("E1_smote",     "smote", None,       None),
    ("E1_ros",       "ros",   None,       None),
    ("E1_rus",       "rus",   None,       None),
    ("E2_cw",        "cw",    "balanced", None),
    ("E3_smote_platt","smote", None,      "sigmoid"),
    ("E3_smote_iso", "smote", None,       "isotonic"),
]


def run_condition(X, y, model_kind, cond, seed):
    _, method, cw, calib = cond
    rng = np.random.default_rng(seed)
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
    probs = np.zeros(len(y)); filled = np.zeros(len(y), dtype=bool)
    for tr, te in skf.split(X, y):
        Xtr, ytr, Xte = X[tr], y[tr], X[te]
        if calib is None:
            Xr, yr = resample(Xtr, ytr, method, rng)
            m = make_model(model_kind, cw=cw, seed=seed).fit(Xr, yr)
            p = m.predict_proba(Xte)[:, 1]
        else:
            # split train into fit/calib; resample ONLY the fit part (leakage-safe)
            inner = np.random.default_rng(seed).permutation(len(tr))
            cut = int(0.7 * len(tr))
            fit_idx, cal_idx = tr[inner[:cut]], tr[inner[cut:]]
            Xr, yr = resample(X[fit_idx], y[fit_idx], method, rng)
            base = make_model(model_kind, cw=cw, seed=seed).fit(Xr, yr)
            cc = CalibratedClassifierCV(base, method=calib, cv="prefit")
            cc.fit(X[cal_idx], y[cal_idx])
            p = cc.predict_proba(Xte)[:, 1]
        probs[te] = p; filled[te] = True
    return metrics(y[filled], probs[filled])


def main():
    manifest = json.loads((PROC / "manifest.json").read_text(encoding="utf-8"))
    csv_path = OUT / "results.csv"
    wrote_header = False
    total = 0
    for meta in manifest:
        name = meta["dataset"]
        df = pd.read_parquet(PROC / meta["file"])
        y = df["__target__"].to_numpy().astype(int)
        X = df.drop(columns="__target__").to_numpy(dtype=float)
        if len(y) > 8000:  # stratified subsample large sets to control CPU time
            rng = np.random.default_rng(0)
            pos = np.where(y == 1)[0]; neg = np.where(y == 0)[0]
            frac = 8000 / len(y)
            keep = np.concatenate([rng.choice(pos, int(len(pos)*frac), replace=False),
                                   rng.choice(neg, int(len(neg)*frac), replace=False)])
            X, y = X[keep], y[keep]
        for model_kind in ("rf", "histgb"):
            rows = []
            for cond in CONDITIONS:
                for seed in SEEDS:
                    r = run_condition(X, y, model_kind, cond, seed)
                    rows.append({"dataset": name, "ir": meta["imbalance_ratio"],
                                 "model": model_kind, "condition": cond[0],
                                 "seed": seed, **r})
            # checkpoint: append this block immediately so nothing is lost on timeout
            blk = pd.DataFrame(rows)
            blk.to_csv(csv_path, mode="a", header=not wrote_header, index=False)
            wrote_header = True
            total += len(blk)
            print(f"[OK] {name:10s} {model_kind:6s} 7conds x10seeds -> +{len(blk)} (total {total})", flush=True)
    print(f"\n[DONE] {total} rows -> {csv_path}")


if __name__ == "__main__":
    main()

