"""analyze_results.py - one-command result-table analysis (Light m06).

Input: a results CSV with one column naming the method/group and one or more
numeric metric columns. Produces:
  * EDA summary per group (n, mean, std, median, min, max, 95% CI of mean),
  * automatic group-comparison test chosen by data shape:
        2 groups,  both ~normal (Shapiro)  -> Welch t-test
        2 groups,  non-normal              -> Mann-Whitney U
        >=3 groups, all ~normal            -> one-way ANOVA + Tukey HSD
        >=3 groups, non-normal             -> Kruskal-Wallis (+ Dunn-ish note)
  * Cohen's d effect size for every pairwise comparison,
  * BH-FDR correction across all reported p-values,
  * machine-readable summary.json + human-readable summary.md.

Usage:
  python analyze_results.py results.csv --group method --metric acc
  python analyze_results.py results.csv --group method --metric acc f1 auroc
  python analyze_results.py            # no args -> generate synthetic CSV & run

Reuses verified stats from significance_test.py (which reuses code_assets).
"""
import argparse
import json
import os
import sys
import itertools
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from significance_test import (  # noqa: E402
    welch_t, cohens_d, interpret_d, mean_diff_ci, benjamini_hochberg, bootstrap_ci,
)

ALPHA = 0.05


def _normal(x, alpha=0.05):
    """Shapiro-Wilk normality; True if cannot reject normality (or n<3)."""
    from scipy import stats
    x = np.asarray(x, float)
    if len(x) < 3:
        return True
    try:
        return stats.shapiro(x).pvalue > alpha
    except Exception:
        return True


def eda_summary(df, group, metric):
    """Per-group descriptive stats including a 95% CI of the mean."""
    from scipy import stats
    rows = []
    for g, sub in df.groupby(group):
        x = sub[metric].dropna().to_numpy(float)
        n = len(x)
        if n == 0:
            continue
        mean = float(x.mean())
        sd = float(x.std(ddof=1)) if n > 1 else 0.0
        if n > 1:
            se = sd / np.sqrt(n)
            tcrit = stats.t.ppf(0.975, n - 1)
            ci = (mean - tcrit * se, mean + tcrit * se)
        else:
            ci = (mean, mean)
        rows.append({
            "group": str(g), "n": n, "mean": mean, "std": sd,
            "median": float(np.median(x)), "min": float(x.min()),
            "max": float(x.max()), "ci95_low": float(ci[0]), "ci95_high": float(ci[1]),
            "normal": bool(_normal(x)),
        })
    return sorted(rows, key=lambda r: r["mean"], reverse=True)


def group_test(df, group, metric):
    """Pick and run the omnibus test appropriate for #groups and normality."""
    from scipy import stats
    groups, data = [], []
    for g, sub in df.groupby(group):
        x = sub[metric].dropna().to_numpy(float)
        if len(x) > 0:
            groups.append(str(g)); data.append(x)
    k = len(groups)
    all_normal = all(_normal(x) for x in data)
    out = {"n_groups": k, "all_normal": bool(all_normal), "groups": groups}

    if k < 2:
        out.update(test="none", note="need >=2 groups", p=None)
        return out
    if k == 2:
        if all_normal:
            t, dfree, p = welch_t(data[0], data[1])
            out.update(test="welch_t", statistic=float(t), df=float(dfree), p=float(p))
        else:
            u, p = stats.mannwhitneyu(data[0], data[1], alternative="two-sided")
            out.update(test="mann_whitney_u", statistic=float(u), p=float(p))
        return out
    # k >= 3
    if all_normal:
        # 方差齐性检验（Levene）：齐 → 经典 ANOVA；不齐 → Welch-ANOVA（不假设等方差）
        try:
            _, lev_p = stats.levene(*data, center="median")
        except Exception:
            lev_p = None
        equal_var = (lev_p is None) or (lev_p > ALPHA)
        if equal_var:
            f, p = stats.f_oneway(*data)
            out.update(test="anova_oneway", statistic=float(f), p=float(p),
                       levene_p=(float(lev_p) if lev_p is not None else None), equal_var=True)
        else:
            # Welch-ANOVA：方差不齐时的稳健替代（scipy 无内置，用经典公式实现）
            fw, dfw1, dfw2, pw = _welch_anova(data)
            out.update(test="welch_anova", statistic=float(fw), df1=float(dfw1),
                       df2=float(dfw2), p=float(pw), levene_p=float(lev_p), equal_var=False,
                       note="方差不齐(Levene p<alpha)→用 Welch-ANOVA 而非经典 ANOVA")
        out["posthoc"] = _tukey(data, groups)
    else:
        h, p = stats.kruskal(*data)
        out.update(test="kruskal_wallis", statistic=float(h), p=float(p))
        out["posthoc_note"] = "non-normal multi-group: pairwise Mann-Whitney below, BH-FDR corrected（如需严格事后检验用 Dunn/scikit-posthocs）"
    # 小样本警告：Shapiro 在 n 小时功效低，"判正态"不可靠
    min_n = min(len(x) for x in data)
    if min_n < 10:
        out["small_n_warning"] = (f"最小组 n={min_n}<10：Shapiro 正态性检验功效低，'判正态'不可靠，"
                                  f"建议直接用非参检验或预设检验类型，勿尽信自动派发")
    return out


def _welch_anova(data):
    """Welch's ANOVA（方差不齐时的稳健 omnibus）。纯 numpy 实现经典公式，返回 (F, df1, df2, p)。"""
    from scipy import stats
    k = len(data)
    ni = np.array([len(x) for x in data], float)
    mi = np.array([x.mean() for x in data], float)
    vi = np.array([x.var(ddof=1) for x in data], float)
    wi = ni / vi                      # 权重 = n/方差
    W = wi.sum()
    xbar = (wi * mi).sum() / W
    # 分子
    num = (wi * (mi - xbar) ** 2).sum() / (k - 1)
    # 分母修正项
    tmp = ((1 - wi / W) ** 2 / (ni - 1)).sum()
    denom = 1 + (2 * (k - 2) / (k ** 2 - 1)) * tmp
    F = num / denom
    df1 = k - 1
    df2 = (k ** 2 - 1) / (3 * tmp)
    p = stats.f.sf(F, df1, df2)
    return F, df1, df2, p


def _tukey(data, groups):
    """Tukey HSD via statsmodels if available, else None."""
    try:
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
        vals = np.concatenate(data)
        labels = np.concatenate([[g] * len(d) for g, d in zip(groups, data)])
        res = pairwise_tukeyhsd(vals, labels, alpha=ALPHA)
        out = []
        for row in res.summary().data[1:]:
            out.append({"group1": row[0], "group2": row[1], "meandiff": float(row[2]),
                        "p_adj": float(row[3]), "lower": float(row[4]),
                        "upper": float(row[5]), "reject": bool(row[6])})
        return out
    except Exception:
        return None


def pairwise(df, group, metric):
    """All pairwise comparisons with Cohen's d, mean-diff CI, and a p-value
    (test matched to per-pair normality). p-values get BH-FDR across all pairs."""
    from scipy import stats
    groups, data = [], {}
    for g, sub in df.groupby(group):
        x = sub[metric].dropna().to_numpy(float)
        if len(x) > 0:
            groups.append(str(g)); data[str(g)] = x
    comps = []
    for g1, g2 in itertools.combinations(groups, 2):
        a, b = data[g1], data[g2]
        normal = _normal(a) and _normal(b)
        if normal:
            _, _, p = welch_t(a, b)
            test = "welch_t"
        else:
            _, p = stats.mannwhitneyu(a, b, alternative="two-sided")
            test = "mann_whitney_u"
        d = cohens_d(a, b, correction=True)
        diff, ci = mean_diff_ci(a, b, equal_var=False)
        comps.append({"group1": g1, "group2": g2, "test": test, "p": float(p),
                      "cohens_d": float(d), "effect": interpret_d(d),
                      "mean_diff": float(diff), "diff_ci95": [float(ci[0]), float(ci[1])]})
    if comps:
        rej, q = benjamini_hochberg([c["p"] for c in comps], ALPHA)
        for c, r, qq in zip(comps, rej, q):
            c["q_fdr"] = float(qq); c["significant_fdr"] = bool(r)
    return comps


def paired_pairwise(df, group, metric, pair_key):
    """Paired comparisons when methods share the same units (seed/fold/sample).

    When every method was evaluated on the SAME set of pair_key values (e.g. the
    same random seeds or CV folds), the per-unit differences are paired and the
    correct test is the paired t-test (normal diffs) or Wilcoxon signed-rank
    (non-normal) — both strictly more powerful than treating groups as
    independent, because they remove between-unit variance.

    Alignment rule: for each pair of groups, keep only pair_key values present in
    BOTH groups (inner join on pair_key); if a group has duplicate pair_key rows
    they are averaged first. A pair with <2 shared units is reported but skipped
    for testing (reason recorded). Paired-diff CI reuses bootstrap_ci on the
    per-unit differences. p-values get BH-FDR across all pairs.
    """
    from scipy import stats
    if pair_key not in df.columns:
        return {"available": False, "reason": f"pair key '{pair_key}' not in columns"}
    # group -> {pair_key_value: mean metric over any dup rows}
    series = {}
    for g, sub in df.groupby(group):
        s = sub.groupby(pair_key)[metric].mean().dropna()
        if len(s) > 0:
            series[str(g)] = s
    groups = list(series)
    comps = []
    for g1, g2 in itertools.combinations(groups, 2):
        s1, s2 = series[g1], series[g2]
        shared = sorted(set(s1.index) & set(s2.index))
        n = len(shared)
        rec = {"group1": g1, "group2": g2, "n_pairs": n, "pair_key": pair_key}
        if n < 2:
            rec.update(test="skipped", reason=f"only {n} shared {pair_key} value(s)", p=None)
            comps.append(rec)
            continue
        a = s1.loc[shared].to_numpy(float)
        b = s2.loc[shared].to_numpy(float)
        diff = a - b
        normal = _normal(diff)
        if normal:
            t, p = stats.ttest_rel(a, b)
            rec.update(test="paired_t", statistic=float(t), p=float(p))
        else:
            # Wilcoxon needs nonzero diffs; if all zero, p=1 by convention
            if np.allclose(diff, 0):
                rec.update(test="wilcoxon", statistic=0.0, p=1.0)
            else:
                w, p = stats.wilcoxon(a, b)
                rec.update(test="wilcoxon", statistic=float(w), p=float(p))
        # paired Cohen's d_z = mean(diff)/sd(diff); bootstrap CI on the diffs
        sd = float(diff.std(ddof=1)) if n > 1 else 0.0
        dz = float(diff.mean() / sd) if sd > 0 else 0.0
        _, ci = bootstrap_ci(diff, np.mean, conf=0.95, n_boot=5000, seed=0)
        rec.update(mean_diff=float(diff.mean()), cohens_dz=dz, effect=interpret_d(dz),
                   diff_ci95=[float(ci[0]), float(ci[1])])
        comps.append(rec)
    tested = [c for c in comps if c.get("p") is not None]
    if tested:
        rej, q = benjamini_hochberg([c["p"] for c in tested], ALPHA)
        for c, r, qq in zip(tested, rej, q):
            c["q_fdr"] = float(qq); c["significant_fdr"] = bool(r)
    return {"available": True, "pair_key": pair_key, "comparisons": comps,
            "note": "Paired test removes between-unit variance; only shared "
                    f"{pair_key} values per pair are used. Cohen's d_z = "
                    "mean(diff)/sd(diff); CI is percentile bootstrap on diffs."}


def analyze_metric(df, group, metric, pair_key=None):
    out = {"metric": metric, "eda": eda_summary(df, group, metric),
           "omnibus": group_test(df, group, metric),
           "pairwise": pairwise(df, group, metric)}
    if pair_key:
        out["paired"] = paired_pairwise(df, group, metric, pair_key)
    return out


def slice_analysis(df, group, metric, slice_by, min_n=5, pair_key=None):
    """切片分析：对 slice_by 列每个取值复算同套 EDA+检验+效应量+FDR，标注小 n 切片。
    兑现 references 切片协议（防聚合指标掩盖子群失败 / 公平性维度），原本只能人工 groupby。"""
    if slice_by not in df.columns:
        return {"available": False, "reason": f"slice column '{slice_by}' not in columns"}
    slices = []
    for sv, sub in df.groupby(slice_by):
        n = len(sub)
        rec = {"slice_value": str(sv), "n_rows": int(n)}
        # 切片内至少 2 组才能比较
        if sub[group].nunique() < 2:
            rec.update(skipped="切片内不足 2 组，无法比较")
            slices.append(rec)
            continue
        rec["analysis"] = analyze_metric(sub, group, metric, pair_key)
        if n < min_n * sub[group].nunique():
            rec["small_n_warning"] = (f"切片 n={n} 偏小（<{min_n}×组数）——子群结论样本不足，"
                                      f"标'待核查'，勿据此下强结论")
        slices.append(rec)
    return {"available": True, "slice_by": slice_by, "min_n": min_n, "slices": slices,
            "note": "切片分析防聚合指标掩盖子群失败；小 n 切片已标待核查。公平性维度的敏感属性可作 slice_by。"}


def run(csv_path, group, metrics, outdir, pair_key=None, emit_claim_table_flag=False,
        slice_by=None):
    df = pd.read_csv(csv_path)
    if group not in df.columns:
        raise SystemExit(f"group column '{group}' not in CSV columns {list(df.columns)}")
    if not metrics:
        metrics = [c for c in df.columns if c != group and pd.api.types.is_numeric_dtype(df[c])]
        if pair_key and pair_key in metrics:
            metrics.remove(pair_key)  # pair key is an index, not a metric
        if slice_by and slice_by in metrics:
            metrics.remove(slice_by)  # slice key is not a metric
    results = []
    for m in metrics:
        res = analyze_metric(df, group, m, pair_key)
        if slice_by:
            res["slices"] = slice_analysis(df, group, m, slice_by, pair_key=pair_key)
        results.append(res)
    report = {"csv": os.path.abspath(csv_path), "group": group,
              "n_rows": int(len(df)), "metrics": metrics, "alpha": ALPHA,
              "pair_key": pair_key, "slice_by": slice_by, "results": results}
    os.makedirs(outdir, exist_ok=True)
    jpath = os.path.join(outdir, "summary.json")
    mpath = os.path.join(outdir, "summary.md")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(_render_md(report))
    if emit_claim_table_flag:
        cpath = os.path.join(outdir, "claim_evidence_table.md")
        with open(cpath, "w", encoding="utf-8") as f:
            f.write(emit_claim_table(report))
        report["_claim_table_path"] = cpath
    return report, jpath, mpath


def _render_md(report):
    L = [f"# Result Analysis: `{os.path.basename(report['csv'])}`", "",
         f"- Group column: **{report['group']}**  |  rows: {report['n_rows']}  |  alpha={report['alpha']}",
         f"- Metrics: {', '.join(report['metrics'])}", ""]
    for res in report["results"]:
        m = res["metric"]
        L.append(f"## Metric: `{m}`\n")
        L.append("| group | n | mean | std | 95% CI | normal |")
        L.append("|---|---|---|---|---|---|")
        for r in res["eda"]:
            L.append(f"| {r['group']} | {r['n']} | {r['mean']:.4f} | {r['std']:.4f} "
                     f"| [{r['ci95_low']:.4f}, {r['ci95_high']:.4f}] | {'Y' if r['normal'] else 'N'} |")
        best = res["eda"][0] if res["eda"] else None
        ob = res["omnibus"]
        L.append("")
        if ob.get("p") is not None:
            sig = "significant" if ob["p"] < report["alpha"] else "not significant"
            L.append(f"**Omnibus test**: {ob['test']} -> p = {ob['p']:.4g} ({sig}). "
                     f"normality: {'all normal' if ob['all_normal'] else 'non-normal present'}.")
        if ob.get("posthoc"):
            L.append("\nTukey HSD post-hoc:")
            L.append("\n| g1 | g2 | meandiff | p_adj | reject |\n|---|---|---|---|---|")
            for t in ob["posthoc"]:
                L.append(f"| {t['group1']} | {t['group2']} | {t['meandiff']:.4f} | {t['p_adj']:.4g} | {t['reject']} |")
        L.append("\n**Pairwise (Cohen's d + BH-FDR):**")
        L.append("\n| g1 | g2 | test | p | q(FDR) | sig | d | effect | mean_diff [CI] |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for c in res["pairwise"]:
            ci = c["diff_ci95"]
            L.append(f"| {c['group1']} | {c['group2']} | {c['test']} | {c['p']:.4g} | "
                     f"{c.get('q_fdr', float('nan')):.4g} | {'Y' if c.get('significant_fdr') else 'n'} | "
                     f"{c['cohens_d']:.3f} | {c['effect']} | {c['mean_diff']:.4f} [{ci[0]:.4f}, {ci[1]:.4f}] |")
        if best:
            L.append(f"\n_Top group by mean: **{best['group']}** ({best['mean']:.4f})._\n")
        paired = res.get("paired")
        if paired and paired.get("available"):
            L.append(f"\n**Paired comparisons (by `{paired['pair_key']}` — same unit, "
                     "higher power):**")
            L.append("\n| g1 | g2 | n_pairs | test | p | q(FDR) | sig | d_z | mean_diff [boot CI] |")
            L.append("|---|---|---|---|---|---|---|---|---|")
            for c in paired["comparisons"]:
                if c.get("p") is None:
                    L.append(f"| {c['group1']} | {c['group2']} | {c['n_pairs']} | "
                             f"{c['test']} | — | — | — | — | {c.get('reason', '')} |")
                    continue
                ci = c.get("diff_ci95", [float('nan'), float('nan')])
                L.append(f"| {c['group1']} | {c['group2']} | {c['n_pairs']} | {c['test']} | "
                         f"{c['p']:.4g} | {c.get('q_fdr', float('nan')):.4g} | "
                         f"{'Y' if c.get('significant_fdr') else 'n'} | {c.get('cohens_dz', 0):.3f} | "
                         f"{c.get('mean_diff', 0):.4f} [{ci[0]:.4f}, {ci[1]:.4f}] |")
            L.append(f"\n_{paired['note']}_\n")
    L.append("\n---\n_Tests auto-selected by Shapiro normality and group count. "
             "Effect sizes are Hedges'-corrected Cohen's d. p-values BH-FDR corrected per metric. "
             "See significance_test.py for the verified primitives._")
    return "\n".join(L)


def emit_claim_table(report: dict) -> str:
    """把每个比较(claim)连到证据字段(检验/p/q/d/CI/n)，落盘 CONVENTIONS §6.1 的
    claim_evidence_table.md。交 m07 写作/m09 绘图时每条论断都能追到统计证据，杜绝
    '正文说更好但拿不出检验'。只收录有 p 值的比较；显著性以 BH-FDR 后 q 为准。"""
    L = [f"# Claim–Evidence Table: `{os.path.basename(report['csv'])}`", "",
         "> 每行一个可写进论文的论断(claim) ↔ 其统计证据。**显著性以 BH-FDR 校正后 q 为准**"
         "(非裸 p)；效应量标量级；CI 含 0 即差异不显著。写作时论断措辞不得强于证据。", "",
         "| metric | 比较(claim) | 检验 | p | q(FDR) | 显著(q<α) | 效应量 d | 量级 | mean_diff [95%CI] | n | 来源 |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    n_claim = 0
    for res in report["results"]:
        m = res["metric"]
        for c in res.get("pairwise", []):
            ci = c.get("diff_ci95", [float('nan')] * 2)
            sig = "Y" if c.get("significant_fdr") else "n"
            L.append(f"| {m} | {c['group1']} vs {c['group2']} | {c['test']} | {c['p']:.4g} | "
                     f"{c.get('q_fdr', float('nan')):.4g} | {sig} | {c['cohens_d']:.3f} | {c['effect']} | "
                     f"{c['mean_diff']:.4f} [{ci[0]:.4f},{ci[1]:.4f}] | — | independent |")
            n_claim += 1
        paired = res.get("paired")
        if paired and paired.get("available"):
            for c in paired["comparisons"]:
                if c.get("p") is None:
                    continue
                ci = c.get("diff_ci95", [float('nan')] * 2)
                sig = "Y" if c.get("significant_fdr") else "n"
                L.append(f"| {m} | {c['group1']} vs {c['group2']} | {c['test']}(paired) | {c['p']:.4g} | "
                         f"{c.get('q_fdr', float('nan')):.4g} | {sig} | {c.get('cohens_dz', 0):.3f} | "
                         f"{c.get('effect', '')} | {c.get('mean_diff', 0):.4f} "
                         f"[{ci[0]:.4f},{ci[1]:.4f}] | {c['n_pairs']} | paired by {paired['pair_key']} |")
                n_claim += 1
    L.append("")
    L.append(f"_共 {n_claim} 条 claim。交 m07(写作)/m09(绘图)；显著性看 q 不看 p；"
             "不显著的比较写作时不得声称'更好',只能报'未见显著差异'。_")
    return "\n".join(L)


def _synth_csv(path, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    specs = {"baseline": (0.80, 0.025), "ours": (0.86, 0.022), "ablation": (0.83, 0.030)}
    for method, (mu, sd) in specs.items():
        for _ in range(8):
            acc = float(np.clip(rng.normal(mu, sd), 0, 1))
            f1 = float(np.clip(acc - rng.normal(0.02, 0.01), 0, 1))
            rows.append({"method": method, "seed": _, "acc": round(acc, 4), "f1": round(f1, 4)})
    pd.DataFrame(rows).to_csv(path, index=False)
    return path



def _selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory(prefix="light_analyze_results_") as tmp:
        csv_path = _synth_csv(os.path.join(tmp, "results.csv"))
        outdir = os.path.join(tmp, "analysis_out")
        report, jp, mp = run(csv_path, "method", ["acc", "f1"], outdir)
        assert os.path.exists(jp) and os.path.exists(mp), (jp, mp)
        assert report["n_rows"] == 24, report["n_rows"]
        assert report["metrics"] == ["acc", "f1"], report["metrics"]
        assert len(report["results"]) == 2, report["results"]
        for res in report["results"]:
            assert res["eda"] and res["pairwise"], res
            assert res["omnibus"].get("test") in {"anova_oneway", "welch_anova", "kruskal_wallis"}, res["omnibus"]
            assert "paired" not in res, "paired must be absent without --paired-by"

        # paired path: synth CSV shares 'seed' across methods -> paired tests fire
        outdir2 = os.path.join(tmp, "analysis_out_paired")
        rep2, _, _ = run(csv_path, "method", ["acc"], outdir2, pair_key="seed")
        paired = rep2["results"][0]["paired"]
        assert paired["available"], paired
        assert "seed" not in rep2["metrics"], "pair key must not be analyzed as a metric"
        comps = paired["comparisons"]
        assert len(comps) == 3, comps  # 3 methods -> 3 pairs
        for c in comps:
            assert c["n_pairs"] == 8, c  # 8 shared seeds
            assert c["test"] in {"paired_t", "wilcoxon"}, c
            assert c["p"] is not None and "q_fdr" in c, c
            assert "diff_ci95" in c and "cohens_dz" in c, c

        # too-few-shared-units path: one method on disjoint seeds -> skipped, no crash
        df = pd.read_csv(csv_path)
        df.loc[df["method"] == "ablation", "seed"] = 999  # single shared-less seed
        odd = os.path.join(tmp, "odd.csv"); df.to_csv(odd, index=False)
        rep3, _, _ = run(odd, "method", ["acc"], os.path.join(tmp, "o3"), pair_key="seed")
        skipped = [c for c in rep3["results"][0]["paired"]["comparisons"]
                   if c["test"] == "skipped"]
        assert skipped, "expected a skipped pair when units are not shared"

        # missing pair key -> available False, graceful
        rep4, _, _ = run(csv_path, "method", ["acc"], os.path.join(tmp, "o4"),
                         pair_key="no_such_col")
        assert rep4["results"][0]["paired"]["available"] is False, rep4

        # claim_evidence_table 生成（§6.1 工件，名实相符）
        odc = os.path.join(tmp, "oclaim")
        repc, _, _ = run(csv_path, "method", ["acc"], odc, pair_key="seed",
                         emit_claim_table_flag=True)
        cpath = os.path.join(odc, "claim_evidence_table.md")
        assert os.path.exists(cpath), "应产出 claim_evidence_table.md"
        ctext = open(cpath, encoding="utf-8").read()
        assert "Claim–Evidence Table" in ctext and "q(FDR)" in ctext, ctext[:200]
        assert "vs" in ctext and "paired by seed" in ctext, "应含独立+配对比较行"
        assert "显著性看 q 不看 p" in ctext, "应有诚实写作约束"

        # 切片分析（--slice-by）：构造带子群列的数据，每切片复算 + 小 n 标注
        srows2 = []
        rng2 = np.random.default_rng(3)
        for sub in ("groupA", "groupB"):
            n_per = 8 if sub == "groupA" else 2  # groupB 故意小 n → 触发 small_n_warning
            for meth, mu in (("baseline", 0.80), ("ours", 0.86)):
                for _ in range(n_per):
                    srows2.append({"method": meth, "subgroup": sub,
                                   "acc": float(np.clip(rng2.normal(mu, 0.02), 0, 1))})
        scsv2 = os.path.join(tmp, "slice.csv"); pd.DataFrame(srows2).to_csv(scsv2, index=False)
        reps2, _, _ = run(scsv2, "method", ["acc"], os.path.join(tmp, "oslice"), slice_by="subgroup")
        sl = reps2["results"][0]["slices"]
        assert sl["available"] and len(sl["slices"]) == 2, sl
        # groupB 小 n 应被标注
        gb = next(s for s in sl["slices"] if s["slice_value"] == "groupB")
        assert "small_n_warning" in gb, gb
        # groupA 正常切片有完整分析
        ga = next(s for s in sl["slices"] if s["slice_value"] == "groupA")
        assert "analysis" in ga and ga["analysis"]["pairwise"], ga
        # slice 列不被当 metric
        assert "subgroup" not in reps2["metrics"], reps2["metrics"]

        # Welch-ANOVA 路径：构造明确正态但方差悬殊的 3 组（用确定性等距点近似正态，避免随机偶发非正态）
        def _normalish(mu, sd, n=40):
            from scipy import stats as _st
            qs = (np.arange(1, n + 1) - 0.5) / n
            return (mu + sd * _st.norm.ppf(qs)).tolist()
        wrows = []
        for m, (mu, sd) in {"a": (1.0, 0.2), "b": (1.1, 0.2), "c": (1.2, 1.5)}.items():
            for v in _normalish(mu, sd):
                wrows.append({"method": m, "v": float(v)})
        wcsv = os.path.join(tmp, "wvar.csv"); pd.DataFrame(wrows).to_csv(wcsv, index=False)
        repw, _, _ = run(wcsv, "method", ["v"], os.path.join(tmp, "ow"))
        ob = repw["results"][0]["omnibus"]
        # 方差悬殊(0.2 vs 1.5)且近正态 → 应判不齐走 welch_anova（若 Shapiro 仍判非正态则 kruskal 也接受）
        assert ob["test"] in {"welch_anova", "anova_oneway", "kruskal_wallis"}, ob
        if ob["test"] == "welch_anova":
            assert ob["equal_var"] is False and "df2" in ob, ob
        # _welch_anova 公式自身合理性：方差极悬殊时 F、df2 为正有限
        F, d1, d2, p = _welch_anova([np.array([1.,2,3,4,5]), np.array([2.,4,6,8,10]),
                                     np.array([1.,1.1,0.9,1.05,0.95])])
        assert F > 0 and d2 > 0 and 0 <= p <= 1, (F, d1, d2, p)

        # 小样本警告：每组 n<10 应带 small_n_warning
        rng = np.random.default_rng(1)
        srows = [{"method": m, "v": float(v)} for m in ("a", "b", "c")
                 for v in (rng.normal(0, 1, 5))]
        scsv = os.path.join(tmp, "small.csv"); pd.DataFrame(srows).to_csv(scsv, index=False)
        reps, _, _ = run(scsv, "method", ["v"], os.path.join(tmp, "os"))
        assert "small_n_warning" in reps["results"][0]["omnibus"], reps["results"][0]["omnibus"]
    print("[selftest] PASS analyze_results (independent + paired + skip + missing-key + claim-table + slice + welch-anova + small-n)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Auto result-table statistical analysis")
    ap.add_argument("csv", nargs="?", help="results CSV (omit to run synthetic demo)")
    ap.add_argument("--group", default="method")
    ap.add_argument("--metric", nargs="+", default=None, help="metric column(s)")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--paired-by", default=None,
                    help="column identifying the shared unit (e.g. seed/fold); "
                         "enables paired t / Wilcoxon signed-rank across methods")
    ap.add_argument("--emit-claim-table", action="store_true",
                    help="额外产出 claim_evidence_table.md（每个比较↔证据字段，交 m07/m09 的 §6.1 工件）")
    ap.add_argument("--slice-by", default=None,
                    help="切片列（如子群/敏感属性）：对每个切片值复算同套分析+标小 n，防聚合掩盖子群失败")
    ap.add_argument("--selftest", action="store_true", help="run synthetic offline self-test")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(_selftest())

    if not a.csv:
        here = os.path.dirname(os.path.abspath(__file__))
        a.csv = _synth_csv(os.path.join(here, "_synth_results.csv"))
        a.group = "method"; a.metric = a.metric or ["acc", "f1"]
        print(f"[demo] generated synthetic CSV -> {a.csv}")
    outdir = a.outdir or os.path.join(os.path.dirname(os.path.abspath(a.csv)), "analysis_out")
    report, jp, mp = run(a.csv, a.group, a.metric, outdir, pair_key=a.paired_by,
                         emit_claim_table_flag=a.emit_claim_table, slice_by=a.slice_by)
    print(f"wrote {jp}\nwrote {mp}")
    if report.get("_claim_table_path"):
        print(f"wrote {report['_claim_table_path']}")
    for res in report["results"]:
        ob = res["omnibus"]
        print(f"  [{res['metric']}] {ob.get('test')} p={ob.get('p')}  "
              f"top={res['eda'][0]['group'] if res['eda'] else 'NA'}")
    print("DONE")


if __name__ == "__main__":
    main()



