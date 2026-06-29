#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""drift_check.py — 两份数据集的分布漂移检验（reference vs current）。

补 data_doctor（单数据集体检）之外的缺口：train/test 是否同分布、上线数据相对训练
数据是否漂移、清洗前后是否改了分布。纯 numpy/pandas，无 Evidently 等重依赖。

逐列选检验（与 references「Evidently」节同口径）：
- 数值列：KS 检验（两样本经验分布最大差）+ PSI（Population Stability Index 分箱稳定度）。
- 类别列：卡方齐性检验 + PSI（按类别频率）。
PSI 经验档：<0.1 稳定 / 0.1~0.25 轻微漂移 / >0.25 显著漂移（业界信贷风控通行阈值）。

⚠ 诚实：KS 的 p 值用渐近公式（Kolmogorov 分布），大样本下任何微小差异都"显著"，
故同时给 PSI 这一**效应量式**指标，别只看 p。"检出漂移 ≠ 有害"，须结合业务判断。
卡方要求期望频数足够（过稀疏类别合并），否则结果不稳。

用法：
  python drift_check.py --ref train.csv --cur test.csv [--out drift.md]
  python drift_check.py --ref train.csv --cur test.csv --cols age,income,city
  python drift_check.py --selftest
"""
from __future__ import annotations
import argparse
import io
import sys
import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

PSI_BANDS = [(0.1, "稳定"), (0.25, "轻微漂移"), (float("inf"), "显著漂移")]


def psi_label(psi: float) -> str:
    for thr, lab in PSI_BANDS:
        if psi < thr:
            return lab
    return "显著漂移"


def _ks_2samp(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """两样本 KS 统计量 D 与渐近 p 值（纯 numpy，避免 scipy 硬依赖）。"""
    a = np.sort(a[~np.isnan(a)])
    b = np.sort(b[~np.isnan(b)])
    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return float("nan"), float("nan")
    allv = np.concatenate([a, b])
    cdf_a = np.searchsorted(a, allv, side="right") / na
    cdf_b = np.searchsorted(b, allv, side="right") / nb
    d = float(np.max(np.abs(cdf_a - cdf_b)))
    en = np.sqrt(na * nb / (na + nb))
    # Kolmogorov 渐近：Q(t)=2*sum_{k>=1}(-1)^{k-1} exp(-2 k^2 t^2)
    t = (en + 0.12 + 0.11 / en) * d
    s = 0.0
    for k in range(1, 101):
        s += (-1) ** (k - 1) * np.exp(-2 * k * k * t * t)
    p = max(0.0, min(1.0, 2 * s))
    return d, p


def _psi_numeric(ref: np.ndarray, cur: np.ndarray, bins: int = 10) -> float:
    ref = ref[~np.isnan(ref)]
    cur = cur[~np.isnan(cur)]
    if len(ref) < 2 or len(cur) < 2:
        return float("nan")
    # 按 ref 的分位切箱，避免空箱用 eps 平滑
    qs = np.quantile(ref, np.linspace(0, 1, bins + 1))
    qs = np.unique(qs)
    if len(qs) < 2:
        return 0.0
    qs[0], qs[-1] = -np.inf, np.inf
    r_hist = np.histogram(ref, bins=qs)[0] / len(ref)
    c_hist = np.histogram(cur, bins=qs)[0] / len(cur)
    eps = 1e-6
    r_hist = np.clip(r_hist, eps, None)
    c_hist = np.clip(c_hist, eps, None)
    return float(np.sum((c_hist - r_hist) * np.log(c_hist / r_hist)))


def _psi_categorical(ref: pd.Series, cur: pd.Series) -> float:
    cats = sorted(set(ref.dropna().unique()) | set(cur.dropna().unique()),
                  key=lambda x: str(x))
    eps = 1e-6
    r = ref.value_counts(normalize=True)
    c = cur.value_counts(normalize=True)
    psi = 0.0
    for cat in cats:
        rp = max(float(r.get(cat, 0.0)), eps)
        cp = max(float(c.get(cat, 0.0)), eps)
        psi += (cp - rp) * np.log(cp / rp)
    return float(psi)


def _chi2_homogeneity(ref: pd.Series, cur: pd.Series) -> tuple[float, float, int]:
    """两组类别频率齐性卡方（纯 numpy）。返回 (chi2, p近似, dof)。"""
    cats = sorted(set(ref.dropna().unique()) | set(cur.dropna().unique()),
                  key=lambda x: str(x))
    rc = np.array([(ref == cat).sum() for cat in cats], dtype=float)
    cc = np.array([(cur == cat).sum() for cat in cats], dtype=float)
    obs = np.vstack([rc, cc])
    total = obs.sum()
    if total == 0 or len(cats) < 2:
        return float("nan"), float("nan"), 0
    row = obs.sum(axis=1, keepdims=True)
    col = obs.sum(axis=0, keepdims=True)
    exp = row @ col / total
    mask = exp > 0
    chi2 = float(np.sum((obs[mask] - exp[mask]) ** 2 / exp[mask]))
    dof = len(cats) - 1
    p = _chi2_sf(chi2, dof)
    return chi2, p, dof


def _chi2_sf(x: float, k: int) -> float:
    """卡方生存函数近似（Wilson-Hilferty），避免 scipy 依赖。仅作粗略 p 提示。"""
    if k <= 0 or np.isnan(x):
        return float("nan")
    if x <= 0:
        return 1.0
    # Wilson-Hilferty: ((x/k)^{1/3} - (1-2/(9k))) / sqrt(2/(9k)) ~ N(0,1)
    t = ((x / k) ** (1 / 3) - (1 - 2 / (9 * k))) / np.sqrt(2 / (9 * k))
    return _norm_sf(t)


def _norm_sf(z: float) -> float:
    # 标准正态生存函数，用 math.erfc
    import math
    return 0.5 * math.erfc(z / math.sqrt(2))


def diagnose(ref: pd.DataFrame, cur: pd.DataFrame, cols=None) -> dict:
    cols = cols or [c for c in ref.columns if c in cur.columns]
    rows = []
    for c in cols:
        if c not in ref.columns or c not in cur.columns:
            rows.append({"col": c, "kind": "missing", "stat": None, "p": None,
                         "psi": None, "verdict": "列不在两表交集中"})
            continue
        is_num = (pd.api.types.is_numeric_dtype(ref[c])
                  and pd.api.types.is_numeric_dtype(cur[c]))
        if is_num:
            d, p = _ks_2samp(ref[c].to_numpy(dtype="float64", na_value=np.nan),
                             cur[c].to_numpy(dtype="float64", na_value=np.nan))
            psi = _psi_numeric(ref[c].to_numpy(dtype="float64", na_value=np.nan),
                               cur[c].to_numpy(dtype="float64", na_value=np.nan))
            rows.append({"col": c, "kind": "numeric", "test": "KS",
                         "stat": round(d, 4), "p": round(p, 4),
                         "psi": round(psi, 4), "verdict": psi_label(psi)})
        else:
            chi2, p, dof = _chi2_homogeneity(ref[c].astype(str), cur[c].astype(str))
            psi = _psi_categorical(ref[c].astype(str), cur[c].astype(str))
            rows.append({"col": c, "kind": "categorical", "test": f"chi2(dof={dof})",
                         "stat": round(chi2, 4) if not np.isnan(chi2) else None,
                         "p": round(p, 4) if not np.isnan(p) else None,
                         "psi": round(psi, 4), "verdict": psi_label(psi)})
    n_drift = sum(1 for r in rows if r["verdict"] == "显著漂移")
    return {"n_cols": len(rows), "n_drift": n_drift, "rows": rows}


def render(rep: dict) -> str:
    L = ["# Data Drift Report (reference vs current)", ""]
    L.append(f"- 检验列数: **{rep['n_cols']}**  |  显著漂移列: **{rep['n_drift']}**")
    L.append("")
    L.append("| column | kind | test | stat | p | PSI | verdict |")
    L.append("| --- | --- | --- | --- | --- | --- | --- |")
    for r in rep["rows"]:
        mark = f"**{r['verdict']}**" if r["verdict"] == "显著漂移" else r["verdict"]
        L.append(f"| `{r['col']}` | {r['kind']} | {r.get('test','-')} | "
                 f"{r.get('stat','-')} | {r.get('p','-')} | {r.get('psi','-')} | {mark} |")
    L.append("")
    L.append("> PSI 档：<0.1 稳定 / 0.1~0.25 轻微 / >0.25 显著。KS/卡方 p 值为渐近近似，"
             "大样本下微小差异也显著，**以 PSI 效应量为主、p 为辅**。检出漂移≠有害，结合业务判断。")
    L.append("")
    L.append("<!-- 由 drift_check.py 生成；p 值为无 scipy 的渐近近似，精确推断请用 scipy.stats。 -->")
    return "\n".join(L)


def _make_synth():
    rng = np.random.default_rng(0)
    n = 2000
    ref = pd.DataFrame({
        "stable_num": rng.normal(0, 1, n),
        "drift_num": rng.normal(0, 1, n),
        "stable_cat": rng.choice(["a", "b", "c"], n, p=[0.5, 0.3, 0.2]),
        "drift_cat": rng.choice(["x", "y", "z"], n, p=[0.6, 0.3, 0.1]),
    })
    cur = pd.DataFrame({
        "stable_num": rng.normal(0, 1, n),                 # 同分布
        "drift_num": rng.normal(2.5, 1.5, n),              # 均值方差都变 → 漂移
        "stable_cat": rng.choice(["a", "b", "c"], n, p=[0.5, 0.3, 0.2]),
        "drift_cat": rng.choice(["x", "y", "z"], n, p=[0.1, 0.2, 0.7]),  # 频率反转 → 漂移
    })
    return ref, cur


def _selftest() -> int:
    print("### drift_check 离线自测", file=sys.stderr)
    ref, cur = _make_synth()
    rep = diagnose(ref, cur)
    by = {r["col"]: r for r in rep["rows"]}
    # 稳定列 PSI 小，漂移列 PSI 大
    assert by["stable_num"]["psi"] < 0.1, by["stable_num"]
    assert by["drift_num"]["psi"] > 0.25, by["drift_num"]
    assert by["stable_cat"]["psi"] < 0.1, by["stable_cat"]
    assert by["drift_cat"]["psi"] > 0.25, by["drift_cat"]
    assert by["drift_num"]["verdict"] == "显著漂移", by["drift_num"]
    # KS 在漂移列 D 应明显大于稳定列
    assert by["drift_num"]["stat"] > by["stable_num"]["stat"], rep
    # 缺失列处理
    rep2 = diagnose(ref, cur, cols=["stable_num", "nonexist"])
    assert any(r["kind"] == "missing" for r in rep2["rows"]), rep2
    # 渲染含表与诚实声明
    md = render(rep)
    assert "PSI" in md and "渐近" in md and "drift_num" in md, md
    print("[selftest] PASS drift_check offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="两数据集分布漂移检验 KS/PSI/卡方")
    ap.add_argument("--ref", help="参考集 CSV（如训练集）")
    ap.add_argument("--cur", help="当前集 CSV（如测试/线上）")
    ap.add_argument("--cols", help="逗号分隔的列子集，默认两表交集全列")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest or not (args.ref and args.cur):
        return _selftest()

    ref = pd.read_csv(args.ref)
    cur = pd.read_csv(args.cur)
    cols = [c.strip() for c in args.cols.split(",")] if args.cols else None
    rep = diagnose(ref, cur, cols)
    md = render(rep)
    if args.out:
        with io.open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md)
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
