"""Data acquisition + health check for the calibration-under-resampling study.
Pulls REAL public datasets from OpenML (via sklearn). No synthetic labels.
Outputs: data/processed/<name>.parquet  +  data/processed/manifest.json
"""
import sys, json, warnings
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

# (name, openml_id, positive_label_strategy) — real binary classification sets, varied IR
DATASETS = [
    ("pima",        37,   "minority"),   # diabetes, ~768
    ("credit_g",    31,   "minority"),   # german credit, 1000
    ("phoneme",     1489, "minority"),   # 5404
    ("adult",       1590, "minority"),   # census income, ~48k (subsample later)
    ("yeast_ml8",   316,  "minority"),   # higher IR if available
]

def health_check(name, X, y):
    n, d = X.shape
    pos = int(y.sum()); neg = int(n - pos)
    ir = round(max(pos, neg) / max(1, min(pos, neg)), 2)
    nan_frac = float(np.isnan(X).mean())
    return {"dataset": name, "n": n, "n_features": d, "pos": pos, "neg": neg,
            "imbalance_ratio": ir, "minority_frac": round(min(pos, neg)/n, 4),
            "nan_fraction": round(nan_frac, 4)}


def load_one(name, oid):
    """Fetch a real OpenML dataset; binarize to minority-vs-rest; numeric-encode."""
    ds = fetch_openml(data_id=oid, as_frame=True, parser="auto")
    X = ds.data.copy()
    y_raw = ds.target.astype(str)
    # binarize: minority class label = positive (1)
    counts = y_raw.value_counts()
    minority_label = counts.index[-1]
    y = (y_raw == minority_label).astype(int).to_numpy()
    # encode categoricals -> numeric; impute NaN with column median
    X = pd.get_dummies(X, drop_first=True)
    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.fillna(X.median(numeric_only=True))
    Xv = X.to_numpy(dtype=float)
    return Xv, y, list(X.columns)


def main():
    manifest = []
    for name, oid, _ in DATASETS:
        try:
            X, y, cols = load_one(name, oid)
        except Exception as e:
            print(f"[SKIP] {name} (openml {oid}): {type(e).__name__}: {e}")
            continue
        hc = health_check(name, X, y)
        df = pd.DataFrame(X, columns=cols)
        df["__target__"] = y
        df.to_parquet(OUT / f"{name}.parquet")
        manifest.append({**hc, "openml_id": oid, "file": f"{name}.parquet"})
        print(f"[OK] {name}: n={hc['n']} d={hc['n_features']} IR={hc['imbalance_ratio']}")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\n[DONE] {len(manifest)} datasets -> {OUT/'manifest.json'}")
    print("IR span:", sorted(m["imbalance_ratio"] for m in manifest))


if __name__ == "__main__":
    main()
