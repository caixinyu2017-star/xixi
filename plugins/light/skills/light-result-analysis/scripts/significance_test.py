"""Significance toolkit: p-value + Cohen's d + confidence interval + BH-FDR.

Light m06 (light-result-analysis) reusable function library. Bundles the three
things you must report together for any group comparison:
  1. a hypothesis test p-value (auto-chosen by normality/#groups elsewhere),
  2. an effect size (Cohen's d, with small-sample Hedges' g correction),
  3. a confidence interval (mean-diff CI, bootstrap CI),
plus BH-FDR multiple-comparison correction.

Correctness anchor: __main__ self-tests every function against scipy /
statsmodels and prints ALL PASS / FAIL. Reuses the verified primitives in
../../../code_assets/stats_tests.py when importable, else falls back to local
copies that are numerically identical.

Run:  python significance_test.py
"""
import os
import sys
import math
import numpy as np

# ---- reuse verified primitives from code_assets if reachable -----------------
_ASSETS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "code_assets"))
if _ASSETS not in sys.path:
    sys.path.insert(0, _ASSETS)
try:
    from stats_tests import welch_t, benjamini_hochberg, wilson_ci  # noqa: F401
    _SRC = "code_assets.stats_tests"
except Exception:  # pragma: no cover - fallback keeps the file standalone
    _SRC = "local-fallback"

    def welch_t(a, b):
        from scipy import stats
        a = np.asarray(a, float); b = np.asarray(b, float)
        na, nb = len(a), len(b)
        va, vb = a.var(ddof=1), b.var(ddof=1)
        t = (a.mean() - b.mean()) / np.sqrt(va / na + vb / nb)
        df = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
        p = 2 * stats.t.sf(abs(t), df)
        return t, df, p

    def benjamini_hochberg(pvals, alpha=0.05):
        p = np.asarray(pvals, float); n = len(p)
        order = np.argsort(p); ranked = p[order]
        q = ranked * n / (np.arange(1, n + 1))
        q = np.minimum.accumulate(q[::-1])[::-1]
        q = np.clip(q, 0, 1)
        out_q = np.empty(n); out_q[order] = q
        return out_q <= alpha, out_q

    def wilson_ci(k, n, z=1.959963984540054):
        if n == 0:
            return (0.0, 0.0)
        phat = k / n; denom = 1 + z * z / n
        center = (phat + z * z / (2 * n)) / denom
        half = z * np.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / denom
        return (max(0.0, center - half), min(1.0, center + half))


# ---- effect sizes ------------------------------------------------------------
def cohens_d(a, b, correction=False):
    """Cohen's d for two independent samples, pooled SD.

    correction=True applies the Hedges' g small-sample bias factor
    J = 1 - 3/(4*(na+nb)-9). Positive d means mean(a) > mean(b).
    """
    a = np.asarray(a, float); b = np.asarray(b, float)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    sp = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if sp == 0:
        return 0.0
    d = (a.mean() - b.mean()) / sp
    if correction:
        J = 1.0 - 3.0 / (4.0 * (na + nb) - 9.0)
        d *= J
    return d


def interpret_d(d):
    """Cohen's conventional magnitude labels."""
    ad = abs(d)
    if ad < 0.2:
        return "negligible"
    if ad < 0.5:
        return "small"
    if ad < 0.8:
        return "medium"
    return "large"


# ---- confidence intervals ----------------------------------------------------
def mean_diff_ci(a, b, conf=0.95, equal_var=False):
    """CI for the difference of means (mean(a)-mean(b)). Welch df by default."""
    from scipy import stats
    a = np.asarray(a, float); b = np.asarray(b, float)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    diff = a.mean() - b.mean()
    if equal_var:
        sp2 = ((na - 1) * va + (nb - 1) * vb) / (na + nb - 2)
        se = np.sqrt(sp2 * (1.0 / na + 1.0 / nb))
        df = na + nb - 2
    else:
        se = np.sqrt(va / na + vb / nb)
        df = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    tcrit = stats.t.ppf(0.5 + conf / 2.0, df)
    return diff, (diff - tcrit * se, diff + tcrit * se)


def bootstrap_ci(x, stat=np.mean, conf=0.95, n_boot=10000, seed=0):
    """Percentile bootstrap CI for any statistic of a single sample."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float); n = len(x)
    idx = rng.integers(0, n, size=(n_boot, n))
    boots = np.array([stat(x[i]) for i in idx])
    lo = np.percentile(boots, (1 - conf) / 2 * 100)
    hi = np.percentile(boots, (1 + conf) / 2 * 100)
    return stat(x), (lo, hi)


# ---- one-call bundle ---------------------------------------------------------
def compare_two(a, b, conf=0.95, hedges=True):
    """The full three-piece report for two groups, as a dict.

    Returns p (Welch t), effect size (Cohen's d / Hedges' g), the mean-diff CI,
    and the group means. Use FDR across many such comparisons with
    benjamini_hochberg([r['p'] for r in results]).
    """
    a = np.asarray(a, float); b = np.asarray(b, float)
    t, df, p = welch_t(a, b)
    d = cohens_d(a, b, correction=hedges)
    diff, ci = mean_diff_ci(a, b, conf=conf, equal_var=False)
    return {
        "n_a": int(len(a)), "n_b": int(len(b)),
        "mean_a": float(a.mean()), "mean_b": float(b.mean()),
        "mean_diff": float(diff), "diff_ci": (float(ci[0]), float(ci[1])),
        "t": float(t), "df": float(df), "p": float(p),
        "cohens_d": float(d), "effect": interpret_d(d),
    }


def _auc_and_structural(scores, pos, neg):
    """DeLong 用的 AUC + structural components (V10, V01)。pos/neg 为正/负类得分数组。"""
    m, n = len(pos), len(neg)
    # midrank-free O(mn) 经典实现（小数据足够；大数据可换 fastDeLong）
    # V10[i] = (1/n) * sum_j [pos_i > neg_j] + 0.5*[==]; V01[j] 对称
    v10 = np.array([(np.sum(p > neg) + 0.5 * np.sum(p == neg)) / n for p in pos])
    v01 = np.array([(np.sum(pos > q) + 0.5 * np.sum(pos == q)) / m for q in neg])
    auc = v10.mean()
    return auc, v10, v01


def delong_two_auroc(y_true, score_a, score_b):
    """DeLong 检验：比较同一测试集上两个模型 AUROC 的差异是否显著（相关样本，扣除协方差）。

    医疗/分类评估常用：两条 ROC 用同一批样本算，AUC 差的方差须含协方差，普通独立检验会错。
    返回 {auc_a, auc_b, diff, z, p}（双侧）。纯 numpy，无 scipy 依赖（正态近似 p）。
    """
    y = np.asarray(y_true).astype(int)
    sa = np.asarray(score_a, float)
    sb = np.asarray(score_b, float)
    pos_mask = y == 1
    if pos_mask.sum() == 0 or (~pos_mask).sum() == 0:
        raise ValueError("DeLong 需正负类各至少 1 个样本")
    auc_a, v10a, v01a = _auc_and_structural(sa, sa[pos_mask], sa[~pos_mask])
    auc_b, v10b, v01b = _auc_and_structural(sb, sb[pos_mask], sb[~pos_mask])
    m, n = int(pos_mask.sum()), int((~pos_mask).sum())
    # 协方差矩阵（2x2）：S = S10/m + S01/n
    def _cov(x10, y10, x01, y01):
        s10 = np.cov(np.vstack([x10, y10]))[0, 1] if m > 1 else 0.0
        s01 = np.cov(np.vstack([x01, y01]))[0, 1] if n > 1 else 0.0
        return s10 / m + s01 / n
    var_a = _cov(v10a, v10a, v01a, v01a)
    var_b = _cov(v10b, v10b, v01b, v01b)
    cov_ab = _cov(v10a, v10b, v01a, v01b)
    var_diff = var_a + var_b - 2 * cov_ab
    diff = auc_a - auc_b
    if var_diff <= 0:
        z = 0.0 if diff == 0 else float("inf") * (1 if diff > 0 else -1)
        p = 1.0 if diff == 0 else 0.0
    else:
        z = diff / math.sqrt(var_diff)
        p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return {"auc_a": float(auc_a), "auc_b": float(auc_b), "diff": float(diff),
            "z": float(z), "p": float(p), "n_pos": m, "n_neg": n,
            "note": "DeLong 相关 AUROC 比较：同测试集两模型，方差已扣协方差；正态近似 p。"}


def _selftest() -> int:
    from scipy import stats
    print(f"[primitives source: {_SRC}]")
    rng = np.random.default_rng(7)
    ok = True

    a = rng.normal(0.87, 0.02, 14)
    b = rng.normal(0.82, 0.04, 16)

    # Cohen's d vs manual pooled-SD formula
    d = cohens_d(a, b)
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    d_ref = (a.mean() - b.mean()) / sp
    print(f"cohens_d   mine={d:.6f} ref={d_ref:.6f} diff={abs(d-d_ref):.2e}")
    ok &= abs(d - d_ref) < 1e-12

    # mean-diff CI (Welch) vs scipy.stats.ttest_ind confidence_interval
    diff, ci = mean_diff_ci(a, b, conf=0.95, equal_var=False)
    res = stats.ttest_ind(a, b, equal_var=False)
    rci = res.confidence_interval(0.95)
    print(f"diff_CI    mine=({ci[0]:.6f},{ci[1]:.6f}) scipy=({rci.low:.6f},{rci.high:.6f})")
    ok &= abs(ci[0] - rci.low) < 1e-9 and abs(ci[1] - rci.high) < 1e-9

    # equal-var CI vs scipy pooled
    _, ci_eq = mean_diff_ci(a, b, conf=0.95, equal_var=True)
    rci_eq = stats.ttest_ind(a, b, equal_var=True).confidence_interval(0.95)
    print(f"diff_CI_eq mine=({ci_eq[0]:.6f},{ci_eq[1]:.6f}) scipy=({rci_eq.low:.6f},{rci_eq.high:.6f})")
    ok &= abs(ci_eq[0] - rci_eq.low) < 1e-9 and abs(ci_eq[1] - rci_eq.high) < 1e-9

    # bootstrap CI vs scipy.stats.bootstrap (same seed family -> close, not exact)
    _, bci = bootstrap_ci(a, np.mean, conf=0.95, n_boot=5000, seed=1)
    sb = stats.bootstrap((a,), np.mean, confidence_level=0.95, n_resamples=5000,
                         method="percentile", random_state=1)
    print(f"boot_CI    mine=({bci[0]:.5f},{bci[1]:.5f}) scipy=({sb.confidence_interval.low:.5f},{sb.confidence_interval.high:.5f})")
    ok &= abs(bci[0] - sb.confidence_interval.low) < 5e-3 and abs(bci[1] - sb.confidence_interval.high) < 5e-3

    # compare_two p vs scipy Welch
    r = compare_two(a, b)
    _, rp = stats.ttest_ind(a, b, equal_var=False)
    print(f"compare_two p mine={r['p']:.6f} scipy={rp:.6f} | d={r['cohens_d']:.3f} ({r['effect']})")
    ok &= abs(r["p"] - rp) < 1e-9

    # BH-FDR still matches statsmodels through the re-export
    pv = [0.001, 0.012, 0.03, 0.04, 0.2, 0.7]
    rej, q = benjamini_hochberg(pv, 0.05)
    try:
        from statsmodels.stats.multitest import multipletests
        r2, q2, _, _ = multipletests(pv, alpha=0.05, method="fdr_bh")
        print(f"BH-FDR     q match statsmodels: {np.allclose(q, q2)} | reject match: {np.array_equal(rej, r2)}")
        ok &= np.allclose(q, q2) and np.array_equal(rej, r2)
    except ImportError:
        print("BH-FDR     statsmodels absent")

    # DeLong 两 AUROC 比较：构造 A 明显优于 B 的相关得分
    rng2 = np.random.default_rng(11)
    n = 200
    y = np.array([0] * (n // 2) + [1] * (n // 2))
    # A: 正类得分明显更高（强分类器）；B: 弱（接近随机）
    sa = np.where(y == 1, rng2.normal(0.75, 0.15, n), rng2.normal(0.35, 0.15, n))
    sb = np.where(y == 1, rng2.normal(0.55, 0.25, n), rng2.normal(0.45, 0.25, n))
    dl = delong_two_auroc(y, sa, sb)
    # A 的 AUC 应明显高于 B，且差异显著
    auc_ok = dl["auc_a"] > dl["auc_b"] and dl["auc_a"] > 0.85 and dl["p"] < 0.05
    # 对比 sklearn 的 roc_auc_score（若可用）核对 AUC 数值
    try:
        from sklearn.metrics import roc_auc_score
        auc_ok &= abs(dl["auc_a"] - roc_auc_score(y, sa)) < 1e-9
        auc_ok &= abs(dl["auc_b"] - roc_auc_score(y, sb)) < 1e-9
    except ImportError:
        print("DeLong     sklearn absent (跳过 AUC 数值对齐，仅验显著性)")
    # 同一得分自比：diff=0、p=1（完全相关，方差差为 0）
    dl_same = delong_two_auroc(y, sa, sa)
    same_ok = abs(dl_same["diff"]) < 1e-12 and dl_same["p"] == 1.0
    ok &= auc_ok and same_ok
    print(f"DeLong     auc_a={dl['auc_a']:.3f} auc_b={dl['auc_b']:.3f} "
          f"p={dl['p']:.4g} | self-compare p={dl_same['p']} | {'OK' if auc_ok and same_ok else 'FAIL'}")

    print("ALL PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv != ["--selftest"]:
        raise SystemExit("usage: python significance_test.py [--selftest]")
    return _selftest()


if __name__ == "__main__":
    raise SystemExit(main())
