"""Statistical analysis: paired tests + effect sizes on results.csv.
Tests H1 (resampling degrades ECE), H2 (post-hoc calibration fixes ECE w/o hurting AUC).
Outputs experiments/analysis.json + console tables.
"""
import sys, json, itertools
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments"
d = pd.read_csv(EXP / "results.csv")

# pair by (dataset, model, seed) so each comparison is matched
KEYS = ["dataset", "model", "seed"]


def cliffs_delta(a, b):
    a = np.asarray(a); b = np.asarray(b)
    gt = sum((x > y) for x in a for y in b)
    lt = sum((x < y) for x in a for y in b)
    return (gt - lt) / (len(a) * len(b))


def paired(metric, cond_a, cond_b):
    """Return paired arrays for cond_a vs cond_b aligned on KEYS."""
    pa = d[d.condition == cond_a].set_index(KEYS)[metric]
    pb = d[d.condition == cond_b].set_index(KEYS)[metric]
    common = pa.index.intersection(pb.index)
    return pa.loc[common].to_numpy(), pb.loc[common].to_numpy()


def compare(metric, a, b, alt="two-sided"):
    xa, xb = paired(metric, a, b)
    diff = xb - xa
    try:
        stat, p = wilcoxon(xa, xb, alternative=alt)
    except ValueError:
        p = float("nan")
    return {"metric": metric, "a": a, "b": b, "n_pairs": len(xa),
            "mean_a": round(float(xa.mean()), 4), "mean_b": round(float(xb.mean()), 4),
            "mean_diff": round(float(diff.mean()), 4),
            "wilcoxon_p": round(float(p), 5), "cliffs_delta": round(cliffs_delta(xb, xa), 3)}


def holm_correct(results, alpha=0.05):
    """Holm-Bonferroni on a list of result dicts with 'wilcoxon_p'."""
    valid = [r for r in results if r["wilcoxon_p"] == r["wilcoxon_p"]]  # drop NaN
    ordered = sorted(valid, key=lambda r: r["wilcoxon_p"])
    m = len(ordered)
    for i, r in enumerate(ordered):
        thresh = alpha / (m - i)
        r["holm_sig"] = bool(r["wilcoxon_p"] < thresh)
        r["holm_thresh"] = round(thresh, 5)
    return ordered


def main():
    out = {"H1_resampling_degrades_ece": [], "H2_calibration_fixes_ece": [],
           "H2_auc_not_hurt": [], "H3_undersampling_worst": []}

    # H1: each resampling vs baseline, ECE should INCREASE (b > a) -> test 'greater'
    for r in ["E1_smote", "E1_ros", "E1_rus"]:
        out["H1_resampling_degrades_ece"].append(compare("ece", "E0_none", r, alt="less"))

    # H2: post-hoc calibration vs SMOTE-uncalibrated, ECE should DECREASE
    for c in ["E3_smote_platt", "E3_smote_iso"]:
        out["H2_calibration_fixes_ece"].append(compare("ece", "E1_smote", c, alt="greater"))
        # and AUC vs baseline should not be hurt (two-sided; we want NON-significance)
        out["H2_auc_not_hurt"].append(compare("auc", "E0_none", c, alt="two-sided"))

    # H3: undersampling worst-calibrated among resamplers
    out["H3_undersampling_worst"].append(compare("ece", "E1_smote", "E1_rus", alt="less"))

    # Holm correction across the primary H1+H2 ECE family
    fam = out["H1_resampling_degrades_ece"] + out["H2_calibration_fixes_ece"]
    holm_correct(fam)

    (EXP / "analysis.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    def show(title, rows):
        print(f"\n### {title}")
        for r in rows:
            sig = r.get("holm_sig")
            tag = "" if sig is None else ("  [Holm-SIG]" if sig else "  [Holm-ns]")
            print(f"  {r['a']:14s} -> {r['b']:16s} | {r['metric']} "
                  f"{r['mean_a']:.4f}->{r['mean_b']:.4f} d(diff)={r['mean_diff']:+.4f} "
                  f"p={r['wilcoxon_p']:.4g} delta={r['cliffs_delta']:+.3f}{tag}")

    show("H1: resampling degrades calibration (ECE up vs baseline)", out["H1_resampling_degrades_ece"])
    show("H2: post-hoc calibration repairs ECE (vs SMOTE)", out["H2_calibration_fixes_ece"])
    show("H2: AUC not hurt by calibration (want p>0.05 = no harm)", out["H2_auc_not_hurt"])
    show("H3: undersampling worst among resamplers", out["H3_undersampling_worst"])
    print(f"\n[DONE] -> {EXP/'analysis.json'}")


if __name__ == "__main__":
    main()
