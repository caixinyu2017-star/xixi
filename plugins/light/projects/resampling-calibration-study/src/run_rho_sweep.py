"""E4: oversampling-ratio (rho) sweep. Does calibration damage grow with
how aggressively we oversample? Real data, multi-seed, leakage-safe.
Outputs experiments/rho_sweep.csv
"""
import sys, json
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_experiments as R
from sklearn.model_selection import StratifiedKFold

PROC = R.PROC
OUT = R.OUT
RHOS = [0.0, 0.25, 0.5, 0.75, 1.0]   # 0 = baseline (no oversampling)
SEEDS = list(range(10))


def run_rho(X, y, rho, seed):
    rng = np.random.default_rng(seed)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    probs = np.zeros(len(y)); filled = np.zeros(len(y), dtype=bool)
    for tr, te in skf.split(X, y):
        Xtr, ytr, Xte = X[tr], y[tr], X[te]
        if rho == 0.0:
            Xr, yr = Xtr, ytr
        else:
            Xr, yr = R.resample(Xtr, ytr, "smote", rng, rho=rho)
        m = R.make_model("histgb", seed=seed).fit(Xr, yr)
        probs[te] = m.predict_proba(Xte)[:, 1]; filled[te] = True
    return R.metrics(y[filled], probs[filled])


def main():
    manifest = json.loads((PROC / "manifest.json").read_text(encoding="utf-8"))
    csv_path = OUT / "rho_sweep.csv"
    wrote_header = False
    total = 0
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
        rows = []
        for rho in RHOS:
            for seed in SEEDS:
                r = run_rho(X, y, rho, seed)
                rows.append({"dataset": name, "ir": meta["imbalance_ratio"],
                             "rho": rho, "seed": seed, **r})
        # checkpoint per dataset so a timeout never loses completed work
        pd.DataFrame(rows).to_csv(csv_path, mode="a", header=not wrote_header, index=False)
        wrote_header = True
        total += len(rows)
        print(f"[OK] {name} done (+{len(rows)}, total {total})", flush=True)
    print(f"[DONE] {total} rows -> {csv_path}")


if __name__ == "__main__":
    main()
