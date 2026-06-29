"""data_doctor.py — CSV in, Markdown health report out.

A no-network, pure pandas/numpy data health checker. Profiles shape, dtypes,
real memory, missing/duplicate rows, constant + high-cardinality columns,
numeric outliers (IQR), and strong correlations. Designed to be the first
thing you run on a new table before any modeling.

Usage:
    python data_doctor.py --csv data.csv [--out report.md] [--target y] \
        [--corr-thresh 0.9] [--card-thresh 0.5] [--sample 200000]

Self-test (no data needed):
    python data_doctor.py --selftest

Writes a Markdown report to --out (default: stdout). Honest by design: every
number is computed from the data, nothing is hardcoded.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import argparse
import io
import numpy as np
import pandas as pd


def _human_bytes(n):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(n) < 1024.0:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"


def _md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def diagnose(df, target=None, corr_thresh=0.9, card_thresh=0.5, outlier_cap=20):
    """Return a dict of findings. Pure computation, no I/O."""
    n_rows, n_cols = df.shape
    f = {"n_rows": n_rows, "n_cols": n_cols}

    # memory
    mem = df.memory_usage(deep=True)
    f["mem_total"] = int(mem.sum())
    f["mem_per_col"] = {c: int(mem[c]) for c in df.columns}

    # dtypes
    f["dtypes"] = {c: str(df[c].dtype) for c in df.columns}

    # missing
    miss = df.isna().sum()
    f["missing"] = {c: (int(miss[c]), float(miss[c] / n_rows) if n_rows else 0.0)
                    for c in df.columns if miss[c] > 0}

    # duplicate rows
    f["dup_rows"] = int(df.duplicated().sum())

    # constant columns (1 unique non-null, or all null)
    f["constant_cols"] = []
    f["allnull_cols"] = []
    for c in df.columns:
        nun = df[c].nunique(dropna=True)
        if nun == 0:
            f["allnull_cols"].append(c)
        elif nun == 1:
            f["constant_cols"].append(c)

    # high-cardinality (object/category): unique ratio over threshold
    # card_thresh 随行数自适应：小表天然高基数比例高，阈值放宽避免误报（n<200 用 0.9，否则用传入值）
    eff_card_thresh = max(card_thresh, 0.9) if n_rows < 200 else card_thresh
    f["card_thresh_used"] = eff_card_thresh
    f["high_card"] = []
    obj_cols = df.select_dtypes(include=["object", "category", "string"]).columns
    for c in obj_cols:
        non_null = df[c].notna().sum()
        if non_null == 0:
            continue
        ratio = df[c].nunique(dropna=True) / non_null
        if ratio >= eff_card_thresh:
            f["high_card"].append((c, df[c].nunique(dropna=True), round(ratio, 3)))

    # ID-like 列：unique_ratio≈1（几乎每行唯一），数值或类别皆查。
    # 这类列（行号/自增 ID/哈希/时间戳唯一键）通常无泛化价值，且若与采集顺序相关易造成泄漏，
    # 入模型前应剔除或显式说明。区别于 high_card：ID-like 看的是"近乎唯一"而非"较高基数"。
    f["id_like"] = []
    for c in df.columns:
        non_null = df[c].notna().sum()
        if non_null < 10:
            continue
        ratio = df[c].nunique(dropna=True) / non_null
        if ratio >= 0.98:
            f["id_like"].append((c, str(df[c].dtype), round(ratio, 3)))

    # 无穷值（inf/-inf）：CSV 里常来自除零/log(0)，会让缩放/统计直接爆，单列计数
    f["inf_cols"] = []
    num_cols = df.select_dtypes(include=[np.number]).columns
    for c in num_cols:
        n_inf = int(np.isinf(df[c].to_numpy(dtype="float64", na_value=np.nan)).sum())
        if n_inf > 0:
            f["inf_cols"].append((c, n_inf))

    # 混合类型 object 列：同列里既有数字又有字符串（常是脏数据/编码不一），抽样判断
    f["mixed_type"] = []
    for c in df.select_dtypes(include=["object"]).columns:
        s = df[c].dropna()
        if len(s) == 0:
            continue
        sample = s.head(1000)
        kinds = set()
        for v in sample:
            kinds.add("num" if isinstance(v, (int, float, np.integer, np.floating))
                      else "str")
            if len(kinds) > 1:
                break
        if len(kinds) > 1:
            f["mixed_type"].append(c)

    # 偏态：|skew|>1 的数值列（强偏，提示对数/分位变换或稳健统计）
    f["skewed"] = []
    for c in num_cols:
        s = df[c].dropna()
        if len(s) < 8 or s.nunique() < 3:
            continue
        sk = float(s.skew())
        if pd.notna(sk) and abs(sk) > 1.0:
            f["skewed"].append((c, round(sk, 3)))
    f["skewed"].sort(key=lambda x: -abs(x[1]))

    # 类不均衡：低基数列（疑似标签/分类）最大类占比 >=0.9，或不平衡比 >=10:1
    f["imbalance"] = []
    for c in df.columns:
        s = df[c].dropna()
        nun = s.nunique()
        if nun < 2 or nun > 20 or len(s) < 10:
            continue
        vc = s.value_counts(normalize=True)
        top = float(vc.iloc[0])
        ratio = float(vc.iloc[0] / vc.iloc[-1]) if vc.iloc[-1] > 0 else float("inf")
        if top >= 0.9 or ratio >= 10:
            f["imbalance"].append((c, round(top, 3), round(ratio, 1), nun))

    # 稀有类别：object/category 列里占比 <1% 的取值数（过多稀有类影响编码与泛化）
    f["rare_cat"] = []
    for c in df.select_dtypes(include=["object", "category", "string"]).columns:
        s = df[c].dropna()
        if len(s) < 50:
            continue
        vc = s.value_counts(normalize=True)
        n_rare = int((vc < 0.01).sum())
        if n_rare > 0:
            f["rare_cat"].append((c, n_rare, vc.shape[0]))

    # numeric outliers via IQR
    f["outliers"] = []
    for c in num_cols:
        s = df[c].dropna()
        if len(s) < 4:
            continue
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_out = int(((s < lo) | (s > hi)).sum())
        if n_out > 0:
            f["outliers"].append((c, n_out, round(100 * n_out / len(s), 2),
                                  round(float(lo), 4), round(float(hi), 4)))
    f["outliers"].sort(key=lambda x: -x[2])
    f["outliers"] = f["outliers"][:outlier_cap]

    # correlations (numeric, abs over threshold, upper triangle)
    f["high_corr"] = []
    if len(num_cols) >= 2:
        corr = df[num_cols].corr(numeric_only=True)
        cols = corr.columns
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                v = corr.iloc[i, j]
                if pd.notna(v) and abs(v) >= corr_thresh:
                    f["high_corr"].append((cols[i], cols[j], round(float(v), 4)))
        f["high_corr"].sort(key=lambda x: -abs(x[2]))

    # target leakage hint: 覆盖数值目标(高相关) + 分类目标(单特征近乎可分)
    f["leakage_hint"] = []
    if target and target in df.columns:
        # 目标是否按"数值回归"处理：在数值列 且 不是低基数整数编码的分类目标
        ty = df[target]
        is_int_like = ty.dropna().apply(lambda v: float(v).is_integer()).all() if ty.notna().any() else False
        treat_numeric = (target in num_cols) and not (is_int_like and ty.nunique(dropna=True) <= 20)
        if treat_numeric:
            # 数值目标：特征与目标 |pearson|≥0.98 视为疑似泄漏
            tcorr = df[num_cols].corr(numeric_only=True)[target].drop(target)
            for c, v in tcorr.items():
                if pd.notna(v) and abs(v) >= 0.98:
                    f["leakage_hint"].append((c, f"|corr|={round(float(v),4)} 与数值目标近乎共线"))
        else:
            # 分类目标：数值特征用"相关比 η"(组间方差占比)，类别特征用"条件纯度"近似预测力。
            # η²≈1 或 某特征值几乎决定某个类 → 单特征近乎可分，疑似泄漏(纯 numpy/pandas)。
            y = df[target]
            for c in num_cols:
                if c == target:
                    continue  # 跳过目标自身（self-η²=1 非泄漏）
                sub = df[[c]].assign(_y=y).dropna()
                if sub[c].nunique() < 2 or sub["_y"].nunique() < 2:
                    continue
                grand = sub[c].mean()
                ss_tot = ((sub[c] - grand) ** 2).sum()
                if ss_tot == 0:
                    continue
                ss_between = sub.groupby("_y")[c].apply(
                    lambda g: len(g) * (g.mean() - grand) ** 2).sum()
                eta2 = ss_between / ss_tot
                if eta2 >= 0.98:
                    f["leakage_hint"].append((c, f"η²={round(float(eta2),4)} 数值特征几乎完全分离各类目标"))
            cat_cols = [c for c in df.columns
                        if c != target and c not in num_cols]
            for c in cat_cols:
                sub = df[[c]].assign(_y=y).dropna()
                if sub[c].nunique() < 2 or len(sub) < 10:
                    continue
                # 条件纯度：按特征值分组，每组目标是否近乎单一类（加权平均最大类占比）
                purity = sub.groupby(c)["_y"].apply(
                    lambda g: g.value_counts(normalize=True).max() * len(g)).sum() / len(sub)
                if purity >= 0.99 and sub[c].nunique() < len(sub):
                    f["leakage_hint"].append((c, f"条件纯度={round(float(purity),4)} 类别特征几乎决定目标类"))
    return f


def render(df, f, target=None):
    """Render findings dict to a Markdown string."""
    L = []
    L.append("# Data Health Report")
    L.append("")
    L.append(f"- Rows: **{f['n_rows']:,}**  |  Columns: **{f['n_cols']}**  "
             f"|  Memory (deep): **{_human_bytes(f['mem_total'])}**")
    if target:
        L.append(f"- Declared target: `{target}`")
    L.append("")

    # severity-ranked issue summary up top
    issues = []
    if f["allnull_cols"]:
        issues.append(("HIGH", f"{len(f['allnull_cols'])} all-null column(s): "
                       f"{', '.join(f['allnull_cols'])}"))
    if f["constant_cols"]:
        issues.append(("HIGH", f"{len(f['constant_cols'])} constant column(s): "
                       f"{', '.join(f['constant_cols'])}"))
    if f["dup_rows"]:
        issues.append(("MED", f"{f['dup_rows']:,} duplicate row(s) "
                       f"({100*f['dup_rows']/max(f['n_rows'],1):.2f}%)"))
    hi_miss = [c for c, (_, r) in f["missing"].items() if r >= 0.5]
    if hi_miss:
        issues.append(("HIGH", f"{len(hi_miss)} column(s) >=50% missing: "
                       f"{', '.join(hi_miss)}"))
    if f["leakage_hint"]:
        issues.append(("HIGH", "possible target leakage（单特征近乎决定目标）: "
                       f"{', '.join(c for c, _ in f['leakage_hint'])}"))
    if f.get("inf_cols"):
        issues.append(("HIGH", f"{len(f['inf_cols'])} 列含 inf/-inf（会让缩放与统计爆）: "
                       f"{', '.join(c for c, _ in f['inf_cols'])}"))
    if f.get("mixed_type"):
        issues.append(("MED", f"{len(f['mixed_type'])} 个混合类型 object 列（数字与字符串混存）: "
                       f"{', '.join(f['mixed_type'])}"))
    if f.get("imbalance"):
        issues.append(("MED", f"{len(f['imbalance'])} 个低基数列严重不均衡（最大类≥90%或≥10:1）: "
                       f"{', '.join(c for c, *_ in f['imbalance'])}"))
    if f.get("id_like"):
        issues.append(("MED", f"{len(f['id_like'])} 个 ID-like 列（近乎逐行唯一，无泛化价值/疑似泄漏）: "
                       f"{', '.join(c for c, *_ in f['id_like'])}"))
    if f["high_corr"]:
        issues.append(("MED", f"{len(f['high_corr'])} highly-correlated numeric pair(s)"))
    if f["high_card"]:
        issues.append(("LOW", f"{len(f['high_card'])} high-cardinality categorical col(s)"))
    if f.get("skewed"):
        issues.append(("LOW", f"{len(f['skewed'])} 个强偏态数值列（|skew|>1，考虑变换）: "
                       f"{', '.join(c for c, _ in f['skewed'])}"))
    if f.get("rare_cat"):
        issues.append(("LOW", f"{len(f['rare_cat'])} 个类别列含稀有类（占比<1%）"))

    L.append("## Issue Summary")
    if issues:
        order = {"HIGH": 0, "MED": 1, "LOW": 2}
        issues.sort(key=lambda x: order[x[0]])
        for sev, msg in issues:
            L.append(f"- **[{sev}]** {msg}")
    else:
        L.append("- No structural issues flagged by the heuristics. Still verify semantics.")
    L.append("")

    # dtypes + memory + missing combined
    L.append("## Columns (dtype / memory / missing)")
    rows = []
    for c in df.columns:
        miss_n, miss_r = f["missing"].get(c, (0, 0.0))
        rows.append([f"`{c}`", f["dtypes"][c], _human_bytes(f["mem_per_col"][c]),
                     f"{miss_n:,}", f"{100*miss_r:.2f}%"])
    L.append(_md_table(["column", "dtype", "memory", "missing", "missing%"], rows))
    L.append("")

    if f["outliers"]:
        L.append("## Numeric Outliers (IQR, top by %)")
        L.append(_md_table(
            ["column", "n_outliers", "%", "lower_fence", "upper_fence"],
            [[f"`{c}`", n, f"{p}%", lo, hi] for c, n, p, lo, hi in f["outliers"]]))
        L.append("")

    if f["high_corr"]:
        L.append("## Highly-Correlated Numeric Pairs")
        L.append(_md_table(["col_a", "col_b", "pearson_r"],
                           [[f"`{a}`", f"`{b}`", v] for a, b, v in f["high_corr"][:30]]))
        L.append("")

    if f["high_card"]:
        L.append("## High-Cardinality Categoricals")
        L.append(_md_table(["column", "n_unique", "unique_ratio"],
                           [[f"`{c}`", n, r] for c, n, r in f["high_card"]]))
        L.append(f"> 高基数阈值（已随行数自适应）= {f.get('card_thresh_used', '?')}")
        L.append("")

    if f.get("id_like"):
        L.append("## ID-like 列（近乎逐行唯一）")
        L.append(_md_table(["column", "dtype", "unique_ratio"],
                           [[f"`{c}`", dt, r] for c, dt, r in f["id_like"]]))
        L.append("> 这类列通常应在建模前剔除（行号/自增ID/哈希）；若与采集顺序相关还可能泄漏。")
        L.append("")

    if f["leakage_hint"]:
        L.append("## ⚠ 疑似目标泄漏（单特征近乎决定目标）")
        L.append(_md_table(["column", "信号"],
                           [[f"`{c}`", sig] for c, sig in f["leakage_hint"]]))
        L.append("> 单个特征几乎完全决定目标，常是泄漏（把答案当输入）或同义重复列。"
                 "务必核查该特征是否在预测时点真实可得，否则剔除。")
        L.append("")

    if f.get("inf_cols"):
        L.append("## 无穷值（inf/-inf）")
        L.append(_md_table(["column", "n_inf"], [[f"`{c}`", n] for c, n in f["inf_cols"]]))
        L.append("> inf 多来自除零/log(0)，缩放与统计会爆；建议替 NaN 后按缺失处理或剔除。")
        L.append("")

    if f.get("mixed_type"):
        L.append("## 混合类型列（数字与字符串混存）")
        L.append("- " + ", ".join(f"`{c}`" for c in f["mixed_type"]))
        L.append("> 同列混类型常是脏数据/编码不一，建议先统一类型再入模型。")
        L.append("")

    if f.get("imbalance"):
        L.append("## 类不均衡（低基数列）")
        L.append(_md_table(["column", "top_ratio", "imbalance_ratio", "n_classes"],
                           [[f"`{c}`", t, r, k] for c, t, r, k in f["imbalance"]]))
        L.append("> 若为标签列：考虑分层划分、重采样(只训练折)、类权重；评测看 PR/F1 而非 acc。")
        L.append("")

    if f.get("skewed"):
        L.append("## 强偏态数值列（|skew|>1）")
        L.append(_md_table(["column", "skew"], [[f"`{c}`", s] for c, s in f["skewed"]]))
        L.append("> 强偏态影响线性模型与基于均值的统计，考虑 log/分位变换或稳健方法。")
        L.append("")

    if f.get("rare_cat"):
        L.append("## 稀有类别（占比<1%）")
        L.append(_md_table(["column", "n_rare", "n_total_cat"],
                           [[f"`{c}`", n, t] for c, n, t in f["rare_cat"]]))
        L.append("> 过多稀有类影响 one-hot 维度与泛化，考虑合并入 'other' 桶。")
        L.append("")

    L.append("## Verdict (fill in after review)")
    L.append("- [ ] Usable as-is  - [ ] Needs cleaning  - [ ] Insufficient  - [ ] Needs more collection")
    L.append("")
    L.append("> Generated by data_doctor.py. Heuristic flags are hypotheses, "
             "not conclusions — confirm against domain knowledge.")
    return "\n".join(L)


def make_synth(seed=0):
    rng = np.random.default_rng(seed)
    n = 500
    df = pd.DataFrame({
        "id": np.arange(n),                              # high cardinality
        "age": rng.normal(45, 12, n).round(1),
        "income": rng.lognormal(10, 0.5, n).round(2),    # outliers
        "city": rng.choice(["A", "B", "C"], n),
        "const": 1,                                      # constant
        "empty": np.nan,                                 # all null
        "score": rng.normal(0, 1, n),
    })
    df["score_copy"] = df["score"] * 2 + 1e-9            # ~perfect corr
    # 分类目标 + 泄漏特征：label 为二分类，leak_num 按 label 完全分离（数值，η²≈1），
    # leak_cat 的取值几乎决定 label（条件纯度≈1）——用于验证分类目标泄漏检测。
    df["label"] = (df["score"] > 0).astype(int)
    df["leak_num"] = df["label"] * 1000.0 + rng.normal(0, 0.01, n)
    df["leak_cat"] = df["label"].map({0: "neg", 1: "pos"})
    df.loc[rng.choice(n, 60, replace=False), "income"] = np.nan  # missing
    df.loc[rng.choice(n, 5, replace=False), "income"] = 5e6      # extreme outliers
    # 新检测器的触发数据：
    df["ratio"] = df["score"] / df["age"]                        # 偶发 inf（age 可能为0附近极小？用显式）
    df.loc[rng.choice(n, 3, replace=False), "ratio"] = np.inf    # 显式 inf
    df["mixed"] = df["city"].astype(object)
    df.loc[rng.choice(n, 20, replace=False), "mixed"] = 999      # object 列混入数字 → 混合类型
    df["imb"] = 0
    df.loc[rng.choice(n, 10, replace=False), "imb"] = 1          # 10/500 → 严重不均衡
    df["skewed_col"] = rng.exponential(1.0, n)                   # 指数分布 → 强右偏
    rare = rng.choice(["common"] * 95 + ["r1", "r2", "r3", "r4", "r5"], n)
    df["rare_c"] = rare                                          # 含 <1% 稀有类
    df = pd.concat([df, df.iloc[:10]], ignore_index=True)        # duplicates
    return df


def main():
    ap = argparse.ArgumentParser(description="CSV -> Markdown data health report")
    ap.add_argument("--csv")
    ap.add_argument("--out")
    ap.add_argument("--target")
    ap.add_argument("--corr-thresh", type=float, default=0.9)
    ap.add_argument("--card-thresh", type=float, default=0.5)
    ap.add_argument("--sample", type=int, default=0,
                    help="random-sample N rows before profiling (0=all)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        df = make_synth()
        f = diagnose(df, target="score", corr_thresh=args.corr_thresh,
                     card_thresh=args.card_thresh)
        md = render(df, f, target="score")
        # assertions prove the detectors actually fire
        assert "empty" in f["allnull_cols"], "all-null detector failed"
        assert "const" in f["constant_cols"], "constant detector failed"
        assert f["dup_rows"] == 10, f"dup count wrong: {f['dup_rows']}"
        assert any(c == "income" for c, *_ in f["outliers"]), "outlier detector failed"
        assert any({a, b} == {"score", "score_copy"} for a, b, _ in f["high_corr"]), \
            "correlation detector failed"
        # ID-like 检测：id 列近乎逐行唯一
        assert any(c == "id" for c, *_ in f["id_like"]), "id-like 检测失败"
        # 分类目标泄漏：用 label 当目标，leak_num(数值η²≈1)与 leak_cat(条件纯度≈1)都应命中
        fc = diagnose(df, target="label")
        leak_cols = {c for c, _ in fc["leakage_hint"]}
        assert "leak_num" in leak_cols, f"分类目标-数值特征泄漏检测失败: {leak_cols}"
        assert "leak_cat" in leak_cols, f"分类目标-类别特征泄漏检测失败: {leak_cols}"
        # 新增检测器断言
        assert any(c == "ratio" for c, _ in f["inf_cols"]), "inf 检测失败"
        assert "mixed" in f["mixed_type"], "混合类型检测失败"
        assert any(c == "imb" for c, *_ in f["imbalance"]), "类不均衡检测失败"
        assert any(c == "skewed_col" for c, _ in f["skewed"]), "偏态检测失败"
        assert any(c == "rare_c" for c, *_ in f["rare_cat"]), "稀有类检测失败"
        print(md)
        print("\n[selftest] PASS — all detectors fired on synthetic data.",
              file=sys.stderr)
        return

    if not args.csv:
        ap.error("provide --csv or --selftest")
    df = pd.read_csv(args.csv)
    if args.sample and len(df) > args.sample:
        df = df.sample(args.sample, random_state=0)
    f = diagnose(df, target=args.target, corr_thresh=args.corr_thresh,
                 card_thresh=args.card_thresh)
    md = render(df, f, target=args.target)
    if args.out:
        with io.open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md)
        print(f"Wrote report to {args.out}", file=sys.stderr)
    else:
        print(md)


if __name__ == "__main__":
    main()
