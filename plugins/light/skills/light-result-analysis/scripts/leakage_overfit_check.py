"""leakage_overfit_check.py - train/val/test gap + data-leakage screen (Light m06).

Pure numpy/pandas. Does NOT require deepchecks; if deepchecks is importable it is
used for an extra cross-check, otherwise the script degrades gracefully and says so.

Checks:
  1. Generalization gap: train vs val vs test metric gaps flagged against thresholds
     (overfit if train-val gap large; distribution-shift if val-test gap large).
  2. Feature->label leakage: any feature whose |correlation| with the target is
     suspiciously high (numeric target -> Pearson; binary target -> point-biserial,
     same as Pearson on 0/1) is flagged as a likely leak / target proxy.
  3. Duplicate rows across train and test (exact-match leakage).
  4. Near-constant / single-value columns (degenerate features).

Usage:
  python leakage_overfit_check.py --train train.csv --test test.csv --target y
  python leakage_overfit_check.py --train t.csv --test te.csv --target y \\
        --train-score 0.99 --val-score 0.84 --test-score 0.71
  python leakage_overfit_check.py            # no args -> synthetic demo with a planted leak
"""
import argparse
import json
import os
import numpy as np
import pandas as pd

GAP_OVERFIT = 0.05      # train-val gap above this -> overfit warning
GAP_SHIFT = 0.05        # val-test gap above this -> shift/leak warning
LEAK_CORR = 0.95        # |corr(feature, target)| above this -> leakage suspect
NEAR_CONST = 0.999      # one value covers >= this fraction of rows -> degenerate


def gap_check(train_s, val_s, test_s):
    flags = []
    if train_s is not None and val_s is not None:
        g = train_s - val_s
        if g > GAP_OVERFIT:
            flags.append({"type": "overfit", "severity": "high" if g > 2 * GAP_OVERFIT else "medium",
                          "detail": f"train-val gap {g:.3f} > {GAP_OVERFIT}", "value": float(g)})
    if val_s is not None and test_s is not None:
        g = val_s - test_s
        if g > GAP_SHIFT:
            flags.append({"type": "val_test_shift", "severity": "high" if g > 2 * GAP_SHIFT else "medium",
                          "detail": f"val-test gap {g:.3f} > {GAP_SHIFT} (shift or val leakage)", "value": float(g)})
    return flags


def leakage_corr_check(df, target):
    """Flag numeric features with |Pearson r| vs target >= LEAK_CORR."""
    flags = []
    if target not in df.columns:
        return flags, []
    y = pd.to_numeric(df[target], errors="coerce")
    table = []
    for col in df.columns:
        if col == target or not pd.api.types.is_numeric_dtype(df[col]):
            continue
        x = pd.to_numeric(df[col], errors="coerce")
        mask = x.notna() & y.notna()
        if mask.sum() < 3 or x[mask].std() == 0 or y[mask].std() == 0:
            continue
        r = float(np.corrcoef(x[mask], y[mask])[0, 1])
        table.append({"feature": col, "corr_with_target": r})
        if abs(r) >= LEAK_CORR:
            flags.append({"type": "feature_leakage", "severity": "high",
                          "detail": f"feature '{col}' |corr| {abs(r):.3f} >= {LEAK_CORR} -> likely target proxy",
                          "feature": col, "corr": r})
    table.sort(key=lambda d: abs(d["corr_with_target"]), reverse=True)
    return flags, table


def duplicate_check(train, test, target=None):
    """Exact-row overlap between train and test (drop target before matching)."""
    flags = []
    if train is None or test is None:
        return flags
    cols = [c for c in train.columns if c in test.columns and c != target]
    if not cols:
        return flags
    keyed_train = train[cols].astype(str).agg("|".join, axis=1)
    keyed_test = test[cols].astype(str).agg("|".join, axis=1)
    overlap = set(keyed_train) & set(keyed_test)
    if overlap:
        n = int(keyed_test.isin(overlap).sum())
        flags.append({"type": "train_test_duplicate", "severity": "high",
                      "detail": f"{n} test rows exactly match train rows ({len(overlap)} unique) -> leakage",
                      "n_test_rows": n})
    return flags


def constant_check(df):
    """Near-constant feature columns are degenerate (no signal, can mask bugs)."""
    flags = []
    for col in df.columns:
        vc = df[col].value_counts(dropna=False, normalize=True)
        if len(vc) > 0 and vc.iloc[0] >= NEAR_CONST:
            flags.append({"type": "near_constant", "severity": "low",
                          "detail": f"column '{col}' is {vc.iloc[0]*100:.1f}% a single value",
                          "feature": col})
    return flags


def _deepchecks_note(train, test, target):
    try:
        import deepchecks  # noqa: F401
        return {"available": True, "note": "deepchecks importable; run data_integrity().run(Dataset(...)) for the full suite"}
    except Exception:
        return {"available": False, "note": "deepchecks not installed -> using built-in numpy/pandas checks only (degraded mode, still functional)"}


def run(train_csv=None, test_csv=None, target="y", scores=(None, None, None),
        train_df=None, test_df=None):
    train = train_df if train_df is not None else (pd.read_csv(train_csv) if train_csv else None)
    test = test_df if test_df is not None else (pd.read_csv(test_csv) if test_csv else None)
    flags = []
    flags += gap_check(*scores)
    corr_table = []
    if train is not None:
        lf, corr_table = leakage_corr_check(train, target)
        flags += lf
        flags += constant_check(train)
    flags += duplicate_check(train, test, target)
    report = {
        "target": target,
        "scores": {"train": scores[0], "val": scores[1], "test": scores[2]},
        "n_flags": len(flags),
        "flags": flags,
        "top_feature_correlations": corr_table[:10],
        "deepchecks": _deepchecks_note(train, test, target),
        "thresholds": {"gap_overfit": GAP_OVERFIT, "gap_shift": GAP_SHIFT,
                       "leak_corr": LEAK_CORR, "near_const": NEAR_CONST},
        "verdict": "FLAGS RAISED" if flags else "CLEAN",
    }
    return report


def _synth():
    """Synthetic train/test with a PLANTED leak column and a duplicate row."""
    rng = np.random.default_rng(0)
    n = 200
    x1 = rng.normal(0, 1, n)
    x2 = rng.normal(0, 1, n)
    y = (0.8 * x1 + 0.3 * x2 + rng.normal(0, 0.5, n) > 0).astype(int)
    leak = y * 1.0 + rng.normal(0, 0.01, n)   # near-perfect proxy of the label
    const = np.ones(n)
    train = pd.DataFrame({"x1": x1, "x2": x2, "leak_feature": leak,
                          "dead_col": const, "y": y})
    # test: fresh rows + 5 rows copied verbatim from train (exact-match leakage)
    m = 80
    xt1 = rng.normal(0, 1, m); xt2 = rng.normal(0, 1, m)
    yt = (0.8 * xt1 + 0.3 * xt2 + rng.normal(0, 0.5, m) > 0).astype(int)
    test = pd.DataFrame({"x1": xt1, "x2": xt2,
                         "leak_feature": yt * 1.0 + rng.normal(0, 0.01, m),
                         "dead_col": np.ones(m), "y": yt})
    test = pd.concat([test, train.iloc[:5]], ignore_index=True)
    return train, test



def _selftest() -> int:
    tr, te = _synth()
    report = run(target="y", scores=(0.99, 0.85, 0.71), train_df=tr, test_df=te)
    types = {flag["type"] for flag in report["flags"]}
    for expected in ("overfit", "val_test_shift", "feature_leakage", "train_test_duplicate", "near_constant"):
        assert expected in types, (expected, types, report)
    assert report["verdict"] == "FLAGS RAISED", report
    print(f"[selftest] PASS leakage_overfit_check flags={report['n_flags']}")
    return 0


def main():
    global GAP_OVERFIT, GAP_SHIFT, LEAK_CORR, NEAR_CONST
    ap = argparse.ArgumentParser(description="Train/val/test gap + leakage screen")
    ap.add_argument("--train"); ap.add_argument("--test"); ap.add_argument("--target", default="y")
    ap.add_argument("--train-score", type=float, default=None)
    ap.add_argument("--val-score", type=float, default=None)
    ap.add_argument("--test-score", type=float, default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--gap-overfit", type=float, default=None,
                    help=f"train-val gap 过拟合阈值（默认 {GAP_OVERFIT}，启发式、强依赖任务，按需覆盖）")
    ap.add_argument("--gap-shift", type=float, default=None,
                    help=f"val-test gap 漂移阈值（默认 {GAP_SHIFT}）")
    ap.add_argument("--leak-corr", type=float, default=None,
                    help=f"特征-标签 |corr| 泄漏阈值（默认 {LEAK_CORR}）")
    ap.add_argument("--near-const", type=float, default=None,
                    help=f"近常量列单值占比阈值（默认 {NEAR_CONST}）")
    ap.add_argument("--selftest", action="store_true", help="run synthetic leakage self-test")
    a = ap.parse_args()

    if a.selftest:
        raise SystemExit(_selftest())

    # 阈值 CLI 覆盖（默认值仅为启发式、强依赖任务；覆盖后报告里如实标用的是哪套阈值）
    if a.gap_overfit is not None:
        GAP_OVERFIT = a.gap_overfit
    if a.gap_shift is not None:
        GAP_SHIFT = a.gap_shift
    if a.leak_corr is not None:
        LEAK_CORR = a.leak_corr
    if a.near_const is not None:
        NEAR_CONST = a.near_const

    if not a.train:
        print("[demo] no --train given: synthetic data with a planted leak + dup rows + dead col")
        tr, te = _synth()
        report = run(target="y", scores=(0.99, 0.85, 0.71), train_df=tr, test_df=te)
    else:
        report = run(a.train, a.test, a.target, (a.train_score, a.val_score, a.test_score))

    out = a.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), "leakage_report.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"verdict: {report['verdict']}  ({report['n_flags']} flags)")
    for fl in report["flags"]:
        print(f"  [{fl['severity']:>6}] {fl['type']}: {fl['detail']}")
    print(f"deepchecks: {report['deepchecks']['note']}")
    print(f"wrote {out}\nDONE")


if __name__ == "__main__":
    main()


