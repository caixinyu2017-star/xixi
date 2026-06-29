"""Additional figures for the expanded paper:
fig4: ECE vs oversampling ratio rho (from rho_sweep.csv)
fig5: reliability diagram on yeast_ml8 (extreme IR=70) under undersampling
"""
import sys, json
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
plt.rcParams.update({"font.size": 8, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.dpi": 300, "savefig.dpi": 300, "font.family": "serif"})
COLW = 3.5


def save(fig, name):
    fig.tight_layout(); fig.savefig(FIG / f"{name}.pdf"); fig.savefig(FIG / f"{name}.png")
    plt.close(fig); print(f"[OK] {name}")


def fig4_rho():
    d = pd.read_csv(ROOT / "experiments" / "rho_sweep.csv")
    fig, ax = plt.subplots(figsize=(COLW, 2.4))
    for name, g in d.groupby("dataset"):
        gg = g.groupby("rho").ece.mean()
        ax.plot(gg.index, gg.values, "o-", ms=3, lw=1, label=name)
    agg = d.groupby("rho").ece.mean()
    ax.plot(agg.index, agg.values, "k--", lw=2, label="mean")
    ax.set_xlabel(r"Oversampling ratio $\rho$")
    ax.set_ylabel("ECE")
    ax.set_title("Calibration error grows with oversampling ratio", fontsize=8)
    # place legend OUTSIDE the axes (upper-right) so it never covers the curves
    ax.legend(fontsize=6, loc="center left", bbox_to_anchor=(1.01, 0.5),
              borderaxespad=0, frameon=False)
    save(fig, "fig4_rho_sweep")


def fig5_yeast_reliability():
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    sys.path.insert(0, str(ROOT / "src")); import run_experiments as R
    mani = json.loads((ROOT/"data"/"processed"/"manifest.json").read_text(encoding="utf-8"))
    m = [x for x in mani if x["dataset"] == "yeast_ml8"][0]
    df = pd.read_parquet(ROOT/"data"/"processed"/m["file"])
    y = df["__target__"].to_numpy().astype(int)
    X = df.drop(columns="__target__").to_numpy(dtype=float)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
    rng = np.random.default_rng(0)
    fig, ax = plt.subplots(figsize=(COLW, 2.6))
    ax.plot([0, 1], [0, 1], "k--", lw=0.8, label="Perfect")
    for method, lab, c in [("none", "Baseline", "#444"), ("rus", "Undersample", "#8e44ad")]:
        Xr, yr = R.resample(Xtr, ytr, method, rng)
        mdl = HistGradientBoostingClassifier(max_iter=200, random_state=0).fit(Xr, yr)
        p = mdl.predict_proba(Xte)[:, 1]
        bins = np.linspace(0, 1, 11); idx = np.clip(np.digitize(p, bins)-1, 0, 9)
        xs, ys = [], []
        for b in range(10):
            mm = idx == b
            if mm.sum() > 0: xs.append(p[mm].mean()); ys.append(yte[mm].mean())
        ax.plot(xs, ys, "o-", ms=3, lw=1, color=c, label=lab)
    ax.set_xlabel("Predicted probability"); ax.set_ylabel("Observed frequency")
    ax.set_title("Reliability on yeast\\_ml8 (IR=70)", fontsize=8)
    ax.legend(fontsize=6, loc="upper left")
    save(fig, "fig5_yeast_reliability")


if __name__ == "__main__":
    fig4_rho()
    fig5_yeast_reliability()
    print("[DONE]")
