"""SHAP analysis: does resampling shift feature attributions, not just
calibration? Compares mean |SHAP| importance baseline vs SMOTE on the
boosting model. Real data. Outputs fig6 + experiments/shap_shift.json.
"""
import sys, json
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"; EXP = ROOT / "experiments"
sys.path.insert(0, str(ROOT / "src")); import run_experiments as R
plt.rcParams.update({"font.size": 8, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.dpi": 300, "savefig.dpi": 300, "font.family": "serif"})
COLW = 3.5
DATASET = "credit_g"   # interpretable, modest feature count


def mean_abs_shap(model, X_sample):
    expl = shap.TreeExplainer(model)
    sv = expl.shap_values(X_sample)
    if isinstance(sv, list):      # some versions return [neg, pos]
        sv = sv[1]
    sv = np.asarray(sv)
    if sv.ndim == 3:              # (n, features, classes)
        sv = sv[:, :, -1]
    return np.abs(sv).mean(axis=0)


def main():
    mani = json.loads((ROOT/"data"/"processed"/"manifest.json").read_text(encoding="utf-8"))
    m = [x for x in mani if x["dataset"] == DATASET][0]
    df = pd.read_parquet(ROOT/"data"/"processed"/m["file"])
    y = df["__target__"].to_numpy().astype(int)
    feats = [c for c in df.columns if c != "__target__"]
    X = df[feats].to_numpy(dtype=float)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
    rng = np.random.default_rng(0)

    # baseline model vs SMOTE model
    base = HistGradientBoostingClassifier(max_iter=200, random_state=0).fit(Xtr, ytr)
    Xr, yr = R.resample(Xtr, ytr, "smote", rng)
    smote = HistGradientBoostingClassifier(max_iter=200, random_state=0).fit(Xr, yr)

    imp_base = mean_abs_shap(base, Xte)
    imp_smote = mean_abs_shap(smote, Xte)

    # rank features by baseline importance, take top 10
    order = np.argsort(imp_base)[::-1][:10]
    top_feats = [feats[i] for i in order]
    b = imp_base[order]; s = imp_smote[order]

    # quantify ranking shift: Spearman-style rank change of full feature set
    rank_base = pd.Series(imp_base).rank(ascending=False)
    rank_smote = pd.Series(imp_smote).rank(ascending=False)
    rank_corr = float(rank_base.corr(rank_smote, method="spearman"))
    out = {"dataset": DATASET, "n_features": len(feats),
           "spearman_rank_corr_base_vs_smote": round(rank_corr, 4),
           "top_feature_base": top_feats[0],
           "mean_abs_shap_change_top10": round(float(np.mean(np.abs(s - b))), 5)}
    (EXP / "shap_shift.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))

    # fig6: grouped bar of top-10 feature importance, baseline vs SMOTE
    short = [f[:14] for f in top_feats]
    x = np.arange(len(top_feats)); w = 0.4
    fig, ax = plt.subplots(figsize=(COLW, 2.8))
    ax.barh(x - w/2, b, height=w, color="#444", label="Baseline")
    ax.barh(x + w/2, s, height=w, color="#c0392b", label="SMOTE")
    ax.set_yticks(x); ax.set_yticklabels(short, fontsize=6)
    ax.invert_yaxis()
    ax.set_xlabel("Mean |SHAP| (impact on output)")
    ax.set_title(f"Feature attribution shift under SMOTE ({DATASET})", fontsize=7.5)
    ax.legend(fontsize=6.5)
    fig.tight_layout()
    fig.savefig(FIG / "fig6_shap_shift.pdf"); fig.savefig(FIG / "fig6_shap_shift.png")
    plt.close(fig)
    print("[OK] fig6_shap_shift  | spearman rank corr =", round(rank_corr, 3))


if __name__ == "__main__":
    main()
