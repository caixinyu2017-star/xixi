"""worked_example.py - end-to-end demo (Light m06 light-result-analysis).

Runs the full pipeline on synthetic experiment data, exactly as a user would
chain the tools after their experiments finish:

  1. EDA + auto significance test      (analyze_results.run)
  2. p + Cohen's d + CI + BH-FDR        (significance_test.compare_two / benjamini_hochberg)
  3. publication figures                (make_figs builders)
  4. leakage / overfit screen           (leakage_overfit_check.run)
  5. filled-in analysis report          (assets template -> example_report.md)

Everything writes into ./example_out/. Run:  python worked_example.py
"""
import os
import sys
import json
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.normpath(os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, SCRIPTS)

import analyze_results as AR          # noqa: E402
import significance_test as ST        # noqa: E402
import make_figs as MF                # noqa: E402
import leakage_overfit_check as LC    # noqa: E402

OUT = os.path.join(HERE, "example_out")
os.makedirs(OUT, exist_ok=True)


def make_data(seed=42):
    """Three methods x 8 seeds, two metrics. 'ours' is genuinely better."""
    rng = np.random.default_rng(seed)
    specs = {"baseline": (0.795, 0.022), "ablation": (0.822, 0.025), "ours": (0.861, 0.020)}
    rows = []
    for method, (mu, sd) in specs.items():
        for s in range(8):
            acc = float(np.clip(rng.normal(mu, sd), 0, 1))
            f1 = float(np.clip(acc - rng.normal(0.018, 0.008), 0, 1))
            rows.append({"method": method, "seed": s, "acc": round(acc, 4), "f1": round(f1, 4)})
    df = pd.DataFrame(rows)
    csv = os.path.join(OUT, "results.csv")
    df.to_csv(csv, index=False)
    return df, csv


def main():
    print("=" * 60)
    print("STEP 1-2: EDA + auto significance (analyze_results)")
    df, csv = make_data()
    report, jpath, mpath = AR.run(csv, group="method", metrics=["acc", "f1"], outdir=OUT)
    for res in report["results"]:
        ob = res["omnibus"]
        best = res["eda"][0]
        print(f"  metric={res['metric']:<4} {ob['test']} p={ob['p']:.3g}  top={best['group']} ({best['mean']:.3f})")

    print("\nSTEP 2b: explicit ours-vs-baseline three-piece report")
    ours = df[df.method == "ours"]["acc"].to_numpy()
    base = df[df.method == "baseline"]["acc"].to_numpy()
    r = ST.compare_two(ours, base)
    print(f"  acc ours vs baseline: p={r['p']:.3g}, Cohen's d={r['cohens_d']:.2f} ({r['effect']}), "
          f"diff={r['mean_diff']:.3f} CI={tuple(round(x,3) for x in r['diff_ci'])}")

    print("\nSTEP 3: publication figures (make_figs)")
    methods = [e["group"] for e in report["results"][0]["eda"]]
    means = [e["mean"] for e in report["results"][0]["eda"]]
    errs = [(e["ci95_high"] - e["ci95_low"]) / 2 for e in report["results"][0]["eda"]]
    samples = [df[df.method == m]["acc"].to_numpy() for m in methods]
    fig, axes = MF.plt.subplots(1, 2, figsize=(8, 3))
    MF.grouped_bar_ci(methods, means, errs, ax=axes[0], ylabel="accuracy", title="(a) mean +/- 95% CI")
    MF.box_strip(methods, samples, ax=axes[1], ylabel="accuracy", title="(b) per-seed dist")
    figpaths = MF.save_all(fig, os.path.join(OUT, "fig_methods"))
    MF.plt.close(fig)
    for p in figpaths:
        print(f"  wrote {p}")

    print("\nSTEP 4: leakage / overfit screen (leakage_overfit_check)")
    lc = LC.run(target="y", scores=(0.99, 0.86, 0.72), **dict(zip(["train_df", "test_df"], LC._synth())))
    lcpath = os.path.join(OUT, "leakage_report.json")
    with open(lcpath, "w", encoding="utf-8") as f:
        json.dump(lc, f, indent=2, ensure_ascii=False)
    print(f"  verdict={lc['verdict']} ({lc['n_flags']} flags) -> {lcpath}")
    for fl in lc["flags"]:
        print(f"    [{fl['severity']}] {fl['type']}")

    print("\nSTEP 5: filled analysis report (example_report.md)")
    _write_report(report, r, lc, figpaths)
    print(f"  wrote {os.path.join(OUT, 'example_report.md')}")
    print("\nDONE - all outputs in", OUT)


def _write_report(report, r, lc, figpaths):
    acc = report["results"][0]
    pw = next((c for c in acc["pairwise"] if {c["group1"], c["group2"]} == {"ours", "baseline"}), None)
    eda_tbl = "\n".join(
        f"| {e['group']} | {e['mean']:.4f}±{e['std']:.4f} | [{e['ci95_low']:.4f}, {e['ci95_high']:.4f}] | {e['n']} |"
        for e in acc["eda"])
    q = pw["q_fdr"] if pw else float("nan")
    sig = "仍显著" if (pw and pw["significant_fdr"]) else "不显著"
    md = f"""# 结果分析报告 — worked example (synthetic)

## 0. 元信息
- 实验：method in [baseline, ablation, ours]，metric acc/f1，8 seeds/组（合成数据）。
- 结果表：`results.csv` | 统计：`summary.json` / `summary.md` | 体检：`leakage_report.json`
- 公平比较：同数据同设置（合成时控制）。

## 1. 描述层（acc）
| 方法 | 均值±std | 95% CI | n |
|---|---|---|---|
{eda_tbl}

## 2. 关键发现（四段式）

### 发现 1：ours 在 acc 上显著优于 baseline
- **现象**：ours 均值 {acc['eda'][0]['mean']:.3f} vs baseline {[e['mean'] for e in acc['eda'] if e['group']=='baseline'][0]:.3f}。
- **原因**：核心组件带来稳定提升（消融见发现 2）。
- **证据**：omnibus {acc['omnibus']['test']} p={acc['omnibus']['p']:.3g}；ours-vs-baseline Welch p={r['p']:.3g}，Cohen's d={r['cohens_d']:.2f}（{r['effect']}），mean_diff={r['mean_diff']:.3f} CI=[{r['diff_ci'][0]:.3f}, {r['diff_ci'][1]:.3f}]；BH-FDR 后 q={q:.3g}（{sig}）。
- **对论文的意义**：可作为主 claim；效应量大且 FDR 后稳健。局限：单（合成）数据集、n=8。

### 发现 2：消融自洽
- **现象**：移除组件后 ablation 介于 baseline 与 ours 之间。
- **证据**：见 summary.md 的 Tukey/pairwise 表。
- **对论文的意义**：支撑组件必要性，方向符合预期。

## 3. 亮点清单
- [x] ours 提升效应量 large 且 FDR 后显著。
- [ ] 跨真实数据集复现（待补）。

## 4. 问题 / 异常清单（来自 leakage 体检：{lc['verdict']}）
""" + "\n".join(f"- [{fl['severity']}] {fl['type']}: {fl['detail']}" for fl in lc["flags"]) + f"""

## 5. 待补实验
- [ ] 增加到 ≥10 seeds 收紧 CI。
- [ ] 真实数据集 + 错例分析。
- [ ] 移除 leak_feature 后重训（体检发现标签代理泄漏）。

## 6. 推荐图表
- {os.path.basename(figpaths[0])}（柱状图+CI 与 box+strip）。

## 7. 诚实标注
- 已验证：统计检验与效应量由 significance_test.py（对齐 scipy）算出，脚本可复现。
- 推测：组件因果归因仅基于消融关联，非因果证明。
- 不能过度声称：合成数据 + 单设置，泛化性未验证。
"""
    with open(os.path.join(OUT, "example_report.md"), "w", encoding="utf-8") as f:
        f.write(md)


if __name__ == "__main__":
    main()

