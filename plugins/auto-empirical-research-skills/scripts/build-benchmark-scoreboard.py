#!/usr/bin/env python3
"""Generate docs/BENCHMARK_SCOREBOARD.md — the shared exam, scored.

Grades two candidates on every benchmark task with the exact same harness
(`benchmark/check_benchmark.py`):

- **reference** — the committed stdlib reference pipelines (the floor a
  rigor-aware agent should match on these deterministic tasks);
- **naive baseline** — a synthetic "agent without the rigor layer",
  constructed deterministically from each task's committed reference
  results.json by the folk move the task was designed to catch: report the
  pooled/unadjusted number as the headline, skip the diagnostic (first-stage
  F = 0, no pre-trend test, empty balance table), control the mediator, read
  the whole gap as unexplained, quote the mean at every quantile, and so on.

The point of the scoreboard is that the SAME exam separates the two: the
reference passes every required gold; the naive baseline fails the required
golds on every task that has a naive trap by construction. External agents can
join the board by following the candidate protocol in docs/INTEROP.md.

Zero third-party dependencies. Mirrors the build-*/--check pattern of the
other generators.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = ROOT / "benchmark" / "tasks"
CAND_DIR = ROOT / "benchmark" / "candidates"
OUT = ROOT / "docs" / "BENCHMARK_SCOREBOARD.md"

sys.path.insert(0, str(ROOT / "scripts"))
import toml_compat  # noqa: E402


def _load_checker():
    spec = importlib.util.spec_from_file_location(
        "aers_check_benchmark", ROOT / "benchmark" / "check_benchmark.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Per-task construction of the naive candidate from the reference results.
# Each entry maps the folk answer into the task's required candidate fields.
NAIVE_BUILDERS = {
    "lalonde-recovery": lambda r: {
        "naive_att": r["naive_att"], "adjusted_att": r["naive_att"], "balance": {}},
    "card-iv-recovery": lambda r: {
        "ols_return": r["ols_return"], "iv_return": r["ols_return"],
        "first_stage_F": 0.0, "first_stage_coef": 0.0},
    "did-staggered-recovery": lambda r: {
        "true_att": r["twfe_att"], "twfe_att": r["twfe_att"], "cs_att": r["twfe_att"]},
    "rdd-recovery": lambda r: {
        "true_tau": r["naive_jump"], "naive_jump": r["naive_jump"],
        "global_att": r["naive_jump"], "local_att": r["naive_jump"]},
    "bad-control-recovery": lambda r: {
        "true_total": r["bad_control_effect"], "naive_effect": r["naive_effect"],
        "good_control_effect": r["bad_control_effect"],
        "bad_control_effect": r["bad_control_effect"]},
    "panel-fe-recovery": lambda r: {
        "true_att": r["pooled_att"], "twoway_fe_att": r["pooled_att"],
        "pooled_att": r["pooled_att"]},
    "event-study-recovery": lambda r: {
        "true_att": r["naive_before_after"], "es_att": r["naive_before_after"],
        "es_pre_max": 0.0, "naive_before_after": r["naive_before_after"]},
    "dml-recovery": lambda r: {
        "true_theta": r["naive_theta"], "dml_theta": r["naive_theta"],
        "naive_theta": r["naive_theta"]},
    "survival-recovery": lambda r: {
        "true_surv_treat": r["naive_surv_treat"],
        "true_surv_control": r["naive_surv_control"],
        "km_surv_treat": r["naive_surv_treat"],
        "km_surv_control": r["naive_surv_control"],
        "naive_surv_treat": r["naive_surv_treat"],
        "naive_surv_control": r["naive_surv_control"]},
    "bayesian-recovery": lambda r: {
        "data_mean": r["data_mean"], "posterior_weak": r["data_mean"],
        "posterior_strong": r["data_mean"]},
    "synthetic-control-recovery": lambda r: {
        "true_effect": r["naive_effect"], "sc_effect": r["naive_effect"],
        "naive_effect": r["naive_effect"]},
    "cate-recovery": lambda r: {
        "cate_low": r["naive_ate"], "cate_high": r["naive_ate"], "cate_gap": 0.0,
        "ate_stratified": r["naive_ate"], "naive_ate": r["naive_ate"]},
    "qte-recovery": lambda r: {
        "qte_50": r["ate"], "qte_90": r["ate"], "ate": r["ate"]},
    "bartik-recovery": lambda r: {
        "bartik_beta": r["ols_beta"], "ols_beta": r["ols_beta"],
        "first_stage_coef": 0.0},
    "mediation-recovery": lambda r: {
        "total_effect": r["total_effect"], "nde": r["naive_direct"],
        "nie": r["total_effect"] - r["naive_direct"],
        "naive_direct": r["naive_direct"]},
    "decomposition-recovery": lambda r: {
        "gap": r["gap"], "explained_ref_a": 0.0, "unexplained_ref_a": r["gap"],
        "explained_ref_b": 0.0, "unexplained_ref_b": r["gap"],
        "explained_reference_swing": 0.0},
    "bunching-recovery": lambda r: {
        "excess_mass": 0.0, "observed_at_K": r["naive_at_K"],
        "counterfactual_at_K": r["naive_at_K"], "naive_at_K": r["naive_at_K"],
        "observed_above_K": r["naive_above_K_total"],
        "implied_elasticity": 0.0},
}

NAIVE_MOVE = {
    "lalonde-recovery": "reports the raw contrast as the causal effect; no balance table",
    "card-iv-recovery": "never instruments; quotes OLS as the IV answer, no first stage",
    "did-staggered-recovery": "runs TWFE and calls it the ATT",
    "rdd-recovery": "quotes the raw jump; no local polynomial, no bandwidth",
    "bad-control-recovery": "controls the post-treatment variable and headlines it",
    "panel-fe-recovery": "pools the panel; no unit fixed effects",
    "event-study-recovery": "before-after difference; never tests pre-trends",
    "dml-recovery": "single unregularized regression; no cross-fitting",
    "survival-recovery": "drops censored spells instead of Kaplan-Meier",
    "bayesian-recovery": "reports the sample mean regardless of prior strength",
    "synthetic-control-recovery": "compares against the unweighted donor mean",
    "cate-recovery": "one pooled difference in means; heterogeneity gap = 0",
    "qte-recovery": "quotes the mean effect at every quantile",
    "bartik-recovery": "regresses outcome on endogenous growth; no instrument",
    "mediation-recovery": "controls the mediator and headlines the coefficient",
    "decomposition-recovery": "reads the entire gap as the unexplained component",
    "bunching-recovery": "quotes the unmodified baseline at every support point - no kink recognized",
}


def grade_candidate(chk, task: dict, candidate: dict) -> tuple[int, int, int, int]:
    """Returns (req_pass, req_total, all_pass, all_total)."""
    truth = chk.compute_truth(task)
    graded = chk.grade(task, candidate, truth)
    req = [g for g in graded if g["required"]]
    return (
        sum(1 for g in req if g["passed"]), len(req),
        sum(1 for g in graded if g["passed"]), len(graded),
    )


def evaluate() -> list[dict]:
    chk = _load_checker()
    rows = []
    for path in sorted(TASK_DIR.glob("*.toml")):
        with path.open("rb") as fh:
            task = toml_compat.load(fh)
        tid = task["id"]
        ref_path = CAND_DIR / task["reference_candidate"] / "results.json"
        ref = json.loads(ref_path.read_text(encoding="utf-8"))
        naive = {"task": tid, "method": f"naive baseline: {NAIVE_MOVE[tid]}",
                 "n": ref.get("n")}
        naive.update(NAIVE_BUILDERS[tid](ref))
        rp, rt, rap, rat = grade_candidate(chk, task, ref)
        np_, nt, nap, nat = grade_candidate(chk, task, naive)
        rows.append({
            "task": tid, "move": NAIVE_MOVE[tid],
            "ref_req": (rp, rt), "ref_all": (rap, rat),
            "naive_req": (np_, nt), "naive_all": (nap, nat),
        })
    return rows


def render(rows: list[dict]) -> str:
    n_tasks = len(rows)
    ref_clean = sum(1 for r in rows if r["ref_req"][0] == r["ref_req"][1])
    naive_failed = sum(1 for r in rows if r["naive_req"][0] < r["naive_req"][1])
    out: list[str] = []
    out.append("# Benchmark Scoreboard — the shared exam, scored")
    out.append("")
    out.append("Generated by `scripts/build-benchmark-scoreboard.py`; do not edit by hand.")
    out.append("Regenerate with `make catalog`. Freshness is enforced by `make validate`.")
    out.append("")
    out.append(
        f"Both candidates below took the identical exam: the **{n_tasks} deterministic "
        "benchmark tasks** in [`benchmark/tasks/`](../benchmark/tasks/), graded by the "
        "same checker that recomputes every data-derived gold from the committed CSVs "
        "(fabricated numbers fail the honest-* golds)."
    )
    out.append("")
    out.append(
        f"- **reference** — the committed stdlib pipelines: **{ref_clean}/{n_tasks} tasks "
        "with every required gold passing**."
    )
    out.append(
        f"- **naive baseline** — a synthetic agent with no rigor layer (the folk move on "
        f"each task, constructed deterministically from the reference numbers): fails "
        f"required golds on **{naive_failed}/{n_tasks} tasks**."
    )
    out.append("")
    out.append(
        "That gap is the point: the exam separates pipelines that guard against each "
        "method's known trap from pipelines that do not. The naive baseline is not a "
        "strawman of any specific product — it is the *default behavior* of an agent "
        "that regresses first and asks no identification questions."
    )
    out.append("")
    out.append("| Task | The naive move | reference (required golds) | naive baseline (required golds) |")
    out.append("|---|---|---:|---:|")
    for r in rows:
        rp, rt = r["ref_req"]
        np_, nt = r["naive_req"]
        naive_cell = f"**{np_}/{nt}** ❌" if np_ < nt else f"{np_}/{nt}"
        out.append(f"| `{r['task']}` | {r['move']} | {rp}/{rt} ✅ | {naive_cell} |")
    out.append("")
    out.append("## Join the board")
    out.append("")
    out.append(
        "Run *your* agent on the same tasks and grade it with the same harness — the "
        "step-by-step candidate protocol is in [`INTEROP.md`](INTEROP.md). Post the "
        "scorecard in "
        "[Show and tell](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/discussions); "
        "reproducible submissions (candidate JSON + how it was produced) may be added "
        "to this page."
    )
    out.append("")
    out.append(
        "_The replication analog of this board — recovering **published** results from "
        "raw data — lives in "
        "[`demo-notebooks/card-krueger-1994/`](../demo-notebooks/card-krueger-1994/), "
        "scored PERFECT by the Paper-WorkFlow replication benchmark._"
    )
    out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument(
        "--check", action="store_true",
        help="verify the committed scoreboard matches a fresh run",
    )
    args = parser.parse_args(argv)

    report = render(evaluate())
    if args.check:
        if not OUT.exists():
            print("docs/BENCHMARK_SCOREBOARD.md missing; run scripts/build-benchmark-scoreboard.py",
                  file=sys.stderr)
            return 1
        if OUT.read_text(encoding="utf-8") != report:
            print("docs/BENCHMARK_SCOREBOARD.md is STALE — regenerate with: "
                  "python3 scripts/build-benchmark-scoreboard.py", file=sys.stderr)
            return 1
        print("docs/BENCHMARK_SCOREBOARD.md is current.")
        return 0

    OUT.write_text(report, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
