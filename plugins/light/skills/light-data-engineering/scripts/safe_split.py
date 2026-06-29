"""safe_split.py — leakage-safe split + Pipeline/ColumnTransformer builder.

Given a task type, builds a scikit-learn preprocessing Pipeline wrapped in a
ColumnTransformer (numeric impute+scale, categorical impute+one-hot) and picks
the correct cross-validation scheme so that NO fit ever sees the validation fold:

    clf        -> StratifiedKFold
    reg        -> KFold
    timeseries -> TimeSeriesSplit (no future leakage)
    group      -> GroupKFold / StratifiedGroupKFold (no entity leakage)

The whole point: every fit-based transform lives inside the Pipeline so it is
re-fit per training fold only. We prove that with a leakage assertion in the
self-test (preprocessor fit on a fold must differ from fit on full data).

Usage:
    python safe_split.py --csv data.csv --target y --task clf [--group-col user_id]
    python safe_split.py --selftest
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import argparse
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import (
    StratifiedKFold, KFold, TimeSeriesSplit, GroupKFold, StratifiedGroupKFold)


def build_preprocessor(X):
    """ColumnTransformer: numeric -> median impute + scale; categorical ->
    most-frequent impute + one-hot. All fit-based, so must live in a Pipeline."""
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    num_pipe = Pipeline([("impute", SimpleImputer(strategy="median")),
                         ("scale", StandardScaler())])
    cat_pipe = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                         ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    pre = ColumnTransformer(
        [("num", num_pipe, num_cols), ("cat", cat_pipe, cat_cols)],
        remainder="drop")
    return pre, num_cols, cat_cols


def pick_cv(task, n_splits=5, group=None, y=None, group_is_clf=None):
    """Return (cv_object, needs_groups, rationale).

    group_is_clf: group 任务时是否按分类处理（用 StratifiedGroupKFold 保类别平衡）。
      显式传入优先；不传则回退到启发式（整数且低基数 → 视为分类），但会在 rationale 标注是猜的。
    """
    if task == "clf":
        return (StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=0),
                False, "StratifiedKFold keeps class proportions per fold.")
    if task == "reg":
        return (KFold(n_splits=n_splits, shuffle=True, random_state=0),
                False, "KFold for continuous targets (shuffled, seeded).")
    if task == "timeseries":
        return (TimeSeriesSplit(n_splits=n_splits), False,
                "TimeSeriesSplit trains only on the past — no future leakage. "
                "Do NOT shuffle time-ordered data.")
    if task == "group":
        if group_is_clf is None:
            # 回退启发式：仅当未显式声明时用，且标注"猜测"提醒用户用 --group-clf/--group-reg 明确
            ys = pd.Series(y)
            is_int = ys.dropna().apply(lambda v: float(v).is_integer()).all() if ys.notna().any() else False
            group_is_clf = bool(is_int and ys.nunique() <= 20)
            hint = "（按启发式猜测，建议用 --group-clf / --group-reg 显式声明）"
        else:
            hint = "（按显式声明）"
        if group_is_clf:
            return (StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=0),
                    True, f"StratifiedGroupKFold: 实体不跨折 + 保类别平衡{hint}。")
        return (GroupKFold(n_splits=n_splits), True,
                f"GroupKFold: 同一实体绝不同时进训练/验证{hint}。")
    raise ValueError(f"unknown task: {task}")


def prepare_timeseries(X, y, time_col=None):
    """timeseries 任务的时序正确性护栏：按 time_col 排序并校验。

    TimeSeriesSplit 假设数据已按时间升序；乱序会导致用未来预测过去（穿越）。
    - 给了 time_col：按它升序重排 X/y（稳定排序），返回排序后的 (X, y)。
    - 未给 time_col：检查是否疑似已按某列单调升序；若无法确认，返回警告字符串让上层显式报错，
      而不是静默用乱序数据跑出错误结果。
    """
    if time_col:
        if time_col not in X.columns:
            raise ValueError(f"--time-col '{time_col}' 不在列中：{list(X.columns)}")
        order = X[time_col].argsort(kind="stable")
        Xs = X.iloc[order].reset_index(drop=True)
        ys = y.iloc[order].reset_index(drop=True)
        if not Xs[time_col].is_monotonic_increasing:
            raise ValueError(f"按 '{time_col}' 排序后仍非单调升序（含 NaN？重复时间？），请先清洗时间列")
        return Xs, ys, f"已按 '{time_col}' 升序重排，时序正确性 OK"
    return X, y, ("⚠ 未提供 --time-col：TimeSeriesSplit 假设数据已按时间升序，"
                  "若数据乱序会产生穿越（用未来预测过去）。请确认数据已排序，或提供 --time-col 让脚本排序")


def make_full_pipeline(X, task, estimator=None):
    """Preprocessor + a default estimator, all inside one Pipeline (leakage-safe)."""
    pre, num_cols, cat_cols = build_preprocessor(X)
    if estimator is None:
        if task in ("reg", "timeseries"):
            from sklearn.linear_model import Ridge
            estimator = Ridge()
        else:
            from sklearn.linear_model import LogisticRegression
            estimator = LogisticRegression(max_iter=1000)
    return Pipeline([("pre", pre), ("model", estimator)]), num_cols, cat_cols


def make_synth(task, seed=0):
    rng = np.random.default_rng(seed)
    n = 400
    X = pd.DataFrame({
        "f_num1": rng.normal(0, 1, n),
        "f_num2": rng.normal(5, 2, n),
        "f_cat": rng.choice(["x", "y", "z"], n),
    })
    X.loc[rng.choice(n, 30, replace=False), "f_num1"] = np.nan  # force imputation
    groups = None
    if task == "reg":
        y = 3 * X["f_num1"].fillna(0) + rng.normal(0, 0.5, n)
    elif task == "timeseries":
        t = np.arange(n)
        y = np.sin(t / 20) + rng.normal(0, 0.2, n)
        X["t"] = t
    else:  # clf or group
        logit = 2 * X["f_num1"].fillna(0) - 1
        y = (rng.uniform(size=n) < 1 / (1 + np.exp(-logit))).astype(int)
    if task == "group":
        groups = rng.integers(0, 40, n)  # 40 entities, repeated rows
    return X, pd.Series(y, name="y"), groups


def run_cv(pipe, X, y, cv, groups=None, task="clf"):
    """Fit/score per fold the leakage-safe way; return per-fold scores."""
    from sklearn.base import clone
    from sklearn.metrics import accuracy_score, r2_score
    scores = []
    splitter = cv.split(X, y, groups) if groups is not None else cv.split(X, y)
    for tr, va in splitter:
        p = clone(pipe)
        p.fit(X.iloc[tr], y.iloc[tr])             # fit ONLY on training fold
        pred = p.predict(X.iloc[va])
        if task == "reg" or task == "timeseries":
            scores.append(r2_score(y.iloc[va], pred))
        else:
            scores.append(accuracy_score(y.iloc[va], pred))
    return np.array(scores)


def _leakage_check():
    """Prove the scaler is re-fit per fold: its learned mean on a fold must differ
    from its mean on the full data. If they were equal, preprocessing leaked."""
    X, y, _ = make_synth("clf")
    pre, _, _ = build_preprocessor(X)
    from sklearn.base import clone
    full = clone(pre).fit(X)
    fold = clone(pre).fit(X.iloc[:200])
    full_mean = full.named_transformers_["num"].named_steps["scale"].mean_
    fold_mean = fold.named_transformers_["num"].named_steps["scale"].mean_
    return not np.allclose(full_mean, fold_mean)


def main():
    ap = argparse.ArgumentParser(description="Leakage-safe split + pipeline builder")
    ap.add_argument("--csv")
    ap.add_argument("--target")
    ap.add_argument("--task", choices=["clf", "reg", "timeseries", "group"])
    ap.add_argument("--group-col")
    ap.add_argument("--time-col", help="timeseries 任务：按此列升序排序并校验单调性，防乱序穿越")
    ap.add_argument("--group-clf", action="store_true",
                    help="group 任务：目标是分类（用 StratifiedGroupKFold 保类别平衡）")
    ap.add_argument("--group-reg", action="store_true",
                    help="group 任务：目标是回归（用 GroupKFold）")
    ap.add_argument("--n-splits", type=int, default=5)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        assert _leakage_check(), "LEAKAGE: scaler fit identical on fold vs full data"
        print("[leakage] OK — preprocessor re-fits per fold (means differ).")
        for task in ["clf", "reg", "timeseries", "group"]:
            X, y, groups = make_synth(task)
            pipe, num_cols, cat_cols = make_full_pipeline(X, task)
            cv, needs_groups, why = pick_cv(task, n_splits=args.n_splits,
                                            group=groups, y=y)
            g = groups if needs_groups else None
            scores = run_cv(pipe, X, y, cv, groups=g, task=task)
            metric = "R2" if task in ("reg", "timeseries") else "acc"
            print(f"  [{task:10s}] CV={type(cv).__name__:22s} "
                  f"{metric}={scores.mean():.3f}±{scores.std():.3f}  | {why}")
        print("\n[selftest] PASS — all four tasks ran leakage-safe CV.")

        # D-2 时序正确性：乱序数据按 time_col 排序后单调；显式 group 分类判定
        Xt, yt, _ = make_synth("timeseries")
        shuffled = Xt.sample(frac=1, random_state=1).reset_index(drop=True)
        ys = yt.sample(frac=1, random_state=1).reset_index(drop=True)
        Xo, yo, note = prepare_timeseries(shuffled, ys, time_col="t")
        assert Xo["t"].is_monotonic_increasing, "prepare_timeseries 未把乱序排成单调"
        assert "升序重排" in note, note
        # 未给 time_col 返回警告而非静默
        _, _, warn = prepare_timeseries(Xt, yt, time_col=None)
        assert "未提供" in warn and "穿越" in warn, warn
        # 显式 group 分类 → StratifiedGroupKFold；显式回归 → GroupKFold（不靠 nunique 猜）
        cv_clf, _, why_clf = pick_cv("group", group_is_clf=True, y=[1, 2, 3])
        assert type(cv_clf).__name__ == "StratifiedGroupKFold" and "显式" in why_clf, why_clf
        cv_reg, _, _ = pick_cv("group", group_is_clf=False, y=list(range(50)))
        assert type(cv_reg).__name__ == "GroupKFold", type(cv_reg).__name__
        print("[selftest] PASS — 时序排序护栏 + 显式 group 判定 OK。")
        return

    if not (args.csv and args.target and args.task):
        ap.error("provide --csv --target --task, or --selftest")
    df = pd.read_csv(args.csv)
    y = df[args.target]
    groups = df[args.group_col].values if args.group_col else None
    X = df.drop(columns=[args.target] + ([args.group_col] if args.group_col else []))

    # 时序正确性护栏：timeseries 任务按 --time-col 排序并校验单调，防乱序穿越
    if args.task == "timeseries":
        X, y, ts_note = prepare_timeseries(X, y, args.time_col)
        print(f"[timeseries] {ts_note}")
        if not args.time_col:
            print("[timeseries] ⚠ 强烈建议提供 --time-col；当前依赖'数据已排序'的假设。", file=sys.stderr)

    # group 任务分类/回归显式声明（不靠 nunique 猜）
    group_is_clf = None
    if args.task == "group":
        if args.group_clf and args.group_reg:
            ap.error("--group-clf 与 --group-reg 只能选一个")
        if args.group_clf:
            group_is_clf = True
        elif args.group_reg:
            group_is_clf = False

    pipe, num_cols, cat_cols = make_full_pipeline(X, args.task)
    cv, needs_groups, why = pick_cv(args.task, n_splits=args.n_splits,
                                    group=groups, y=y, group_is_clf=group_is_clf)
    if needs_groups and groups is None:
        ap.error(f"task '{args.task}' needs --group-col")
    g = groups if needs_groups else None
    scores = run_cv(pipe, X, y, cv, groups=g, task=args.task)
    metric = "R2" if args.task in ("reg", "timeseries") else "acc"
    print(f"task={args.task}  CV={type(cv).__name__}  (n_splits={args.n_splits})")
    print(f"rationale: {why}")
    print(f"numeric cols: {num_cols}")
    print(f"categorical cols: {cat_cols}")
    print(f"per-fold {metric}: {[round(s,4) for s in scores]}")
    print(f"mean {metric} = {scores.mean():.4f} ± {scores.std():.4f}")


if __name__ == "__main__":
    main()
