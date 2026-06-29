"""Generate the 3 paper figures at IEEE column width (3.5in).
Reads experiments/results.csv. Outputs figures/*.pdf + *.png (300 dpi).
"""
import sys
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"; FIG.mkdir(exist_ok=True)
d = pd.read_csv(ROOT / "experiments" / "results.csv")

plt.rcParams.update({"font.size": 8, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.dpi": 300, "savefig.dpi": 300, "font.family": "serif"})
COLW = 3.5  # IEEE single column inches
ORDER = ["E0_none", "E1_smote", "E1_ros", "E1_rus", "E2_cw", "E3_smote_platt", "E3_smote_iso"]
LABELS = {"E0_none": "Baseline", "E1_smote": "SMOTE", "E1_ros": "ROS",
          "E1_rus": "RUS", "E2_cw": "ClassWt", "E3_smote_platt": "SMOTE\n+Platt",
          "E3_smote_iso": "SMOTE\n+Iso"}


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG / f"{name}.pdf")
    fig.savefig(FIG / f"{name}.png")
    plt.close(fig)
    print(f"[OK] {name}.pdf/.png  ({fig.get_size_inches()[0]:.2f}in wide)")


print("loaded", len(d), "rows")


# ---- F1: ECE by condition (main effect) ----
def fig_ece_bar():
    means = d.groupby("condition").ece.mean().reindex(ORDER)
    sems = d.groupby("condition").ece.sem().reindex(ORDER)
    fig, ax = plt.subplots(figsize=(COLW, 2.4))
    colors = ["#444"] + ["#c0392b"]*3 + ["#e67e22"] + ["#27ae60"]*2
    ax.bar(range(len(ORDER)), means.values, yerr=sems.values, capsize=2,
           color=colors, edgecolor="black", linewidth=0.4)
    ax.set_xticks(range(len(ORDER)))
    ax.set_xticklabels([LABELS[c] for c in ORDER], fontsize=6.5)
    ax.set_ylabel("ECE (lower = better)")
    ax.set_title("Calibration error by resampling / post-hoc condition", fontsize=8)
    save(fig, "fig1_ece_by_condition")


# ---- F2: reliability curves (SMOTE uncalibrated vs +isotonic) ----
def fig_reliability():
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.calibration import CalibratedClassifierCV
    import sys as _s; _s.path.insert(0, str(ROOT / "src"))
    import run_experiments as R
    mani = __import__("json").loads((ROOT/"data"/"processed"/"manifest.json").read_text(encoding="utf-8"))
    m = [x for x in mani if x["dataset"] == "credit_g"][0]
    df = pd.read_parquet(ROOT/"data"/"processed"/m["file"])
    y = df["__target__"].to_numpy().astype(int)
    X = df.drop(columns="__target__").to_numpy(dtype=float)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
    rng = np.random.default_rng(0)
    Xr, yr = R.resample(Xtr, ytr, "smote", rng)
    base = HistGradientBoostingClassifier(max_iter=200, random_state=0).fit(Xr, yr)
    p_unc = base.predict_proba(Xte)[:, 1]
    Xf, Xc, yf, yc = train_test_split(Xtr, ytr, test_size=0.3, stratify=ytr, random_state=0)
    Xrf, yrf = R.resample(Xf, yf, "smote", rng)
    b2 = HistGradientBoostingClassifier(max_iter=200, random_state=0).fit(Xrf, yrf)
    cc = CalibratedClassifierCV(b2, method="isotonic", cv="prefit").fit(Xc, yc)
    p_cal = cc.predict_proba(Xte)[:, 1]

    fig, ax = plt.subplots(figsize=(COLW, 2.6))
    ax.plot([0, 1], [0, 1], "k--", lw=0.8, label="Perfect")
    for p, lab, c in [(p_unc, "SMOTE (uncal.)", "#c0392b"), (p_cal, "SMOTE+Iso", "#27ae60")]:
        bins = np.linspace(0, 1, 11)
        idx = np.clip(np.digitize(p, bins) - 1, 0, 9)
        xs, ys = [], []
        for bb in range(10):
            mm = idx == bb
            if mm.sum() > 0:
                xs.append(p[mm].mean()); ys.append(yte[mm].mean())
        ax.plot(xs, ys, "o-", ms=3, lw=1, color=c, label=lab)
    ax.set_xlabel("Predicted probability"); ax.set_ylabel("Observed frequency")
    ax.set_title("Reliability diagram (credit-g)", fontsize=8)
    ax.legend(fontsize=6, loc="upper left")
    save(fig, "fig2_reliability")


# ---- F3: ECE inflation vs imbalance ratio ----
def fig_ece_vs_ir():
    g = d.groupby(["dataset", "ir", "condition"]).ece.mean().reset_index()
    piv = g.pivot_table(index=["dataset", "ir"], columns="condition", values="ece").reset_index()
    piv = piv.sort_values("ir")
    fig, ax = plt.subplots(figsize=(COLW, 2.4))
    ax.plot(piv["ir"], piv["E1_smote"] - piv["E0_none"], "o-", color="#c0392b", ms=4, label="SMOTE")
    ax.plot(piv["ir"], piv["E1_rus"] - piv["E0_none"], "s-", color="#8e44ad", ms=4, label="Undersampling")
    ax.set_xscale("log")
    ax.set_xlabel("Imbalance ratio (log scale)")
    ax.set_ylabel(r"$\Delta$ECE vs baseline")
    ax.set_title("Calibration damage grows with imbalance", fontsize=8)
    ax.legend(fontsize=6.5)
    save(fig, "fig3_ece_vs_ir")


if __name__ == "__main__":
    fig_ece_bar()
    fig_reliability()
    fig_ece_vs_ir()
    print("[DONE] 3 figures ->", FIG)
