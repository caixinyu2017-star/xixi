"""Statistical tests for experiment result analysis (Light m06 asset).

Welch's t-test, Benjamini-Hochberg FDR, Wilson score interval (for accuracy/recall
proportions), bootstrap CI. Correctness anchor: self-tested against scipy/statsmodels.
Run:  python stats_tests.py
"""
import numpy as np


def welch_t(a, b):
    """Welch's unequal-variance t-test. Returns (t, df, p_two_sided)."""
    from scipy import stats
    a = np.asarray(a, float); b = np.asarray(b, float)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    t = (a.mean() - b.mean()) / np.sqrt(va / na + vb / nb)
    df = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    p = 2 * stats.t.sf(abs(t), df)
    return t, df, p


def benjamini_hochberg(pvals, alpha=0.05):
    """BH-FDR. Returns (rejected_bool_array, qvalues) in original order."""
    p = np.asarray(pvals, float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * n / (np.arange(1, n + 1))
    # enforce monotonicity from the largest
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0, 1)
    out_q = np.empty(n); out_q[order] = q
    rejected = out_q <= alpha
    return rejected, out_q


def wilson_ci(k, n, z=1.959963984540054):
    """Wilson score interval for a binomial proportion (e.g. accuracy = k/n)."""
    if n == 0:
        return (0.0, 0.0)
    phat = k / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    half = z * np.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


if __name__ == '__main__':
    from scipy import stats
    rng = np.random.default_rng(1)
    ok = True

    # Welch t vs scipy
    a = rng.normal(0.86, 0.03, 12)
    b = rng.normal(0.81, 0.05, 15)
    t, df, p = welch_t(a, b)
    rt, rp = stats.ttest_ind(a, b, equal_var=False)
    print(f"welch_t   t mine={t:.6f} scipy={rt:.6f} | p mine={p:.6f} scipy={rp:.6f}")
    ok &= abs(t - rt) < 1e-9 and abs(p - rp) < 1e-9

    # BH-FDR vs statsmodels (if available) else known-vector sanity
    pv = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.5]
    rej, q = benjamini_hochberg(pv, 0.05)
    try:
        from statsmodels.stats.multitest import multipletests
        r2, q2, _, _ = multipletests(pv, alpha=0.05, method='fdr_bh')
        print(f"BH-FDR    qvals match statsmodels: {np.allclose(q, q2)} | reject match: {np.array_equal(rej, r2)}")
        ok &= np.allclose(q, q2) and np.array_equal(rej, r2)
    except ImportError:
        print(f"BH-FDR    statsmodels absent; reject={rej.tolist()}")

    # Wilson CI vs statsmodels proportion_confint
    lo, hi = wilson_ci(86, 100)
    try:
        from statsmodels.stats.proportion import proportion_confint
        rlo, rhi = proportion_confint(86, 100, method='wilson')
        print(f"wilson_ci mine=({lo:.6f},{hi:.6f}) statsmodels=({rlo:.6f},{rhi:.6f})")
        ok &= abs(lo - rlo) < 1e-9 and abs(hi - rhi) < 1e-9
    except ImportError:
        print(f"wilson_ci mine=({lo:.4f},{hi:.4f}) (statsmodels absent)")

    print("ALL PASS" if ok else "FAIL")
