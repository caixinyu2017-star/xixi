#!/usr/bin/env python3
"""Check that the rigor stats in every locale README match the repo's reality.

The six READMEs (zh-CN default, en, zh-TW, ja, ko, plus the root README) each
carry a trust-surface stats table. Those numbers drift silently when scenarios
or benchmark tasks are added, because the table text is locale-specific and no
generator owns it. This checker keys on the locale-invariant link targets
inside each row — `[`benchmark/`](benchmark/)` and
`[`eval-harness/`](eval-harness/)` — and verifies the bolded counts in those
rows against the committed scenario/task TOMLs, in every README, so a rigor
expansion cannot ship with stale marketing numbers.

Zero third-party dependencies (TOML via scripts/toml_compat.py). Wired into
`make validate`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import toml_compat

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "eval-harness" / "scenarios"
TASK_DIR = ROOT / "benchmark" / "tasks"
READMES = (
    "README.md",
    "README-en.md",
    "README-zh-CN.md",
    "README-zh-TW.md",
    "README-ja.md",
    "README-ko.md",
)

BENCH_LINK = "[`benchmark/`](benchmark/)"
EVAL_LINK = "[`eval-harness/`](eval-harness/)"


def expected_counts() -> tuple[int, int, int]:
    n_tasks = len(list(TASK_DIR.glob("*.toml")))
    n_scenarios = 0
    n_rubric = 0
    for path in SCENARIO_DIR.glob("*.toml"):
        with path.open("rb") as fh:
            s = toml_compat.load(fh)
        n_scenarios += 1
        n_rubric += len(s.get("rubric", []))
    return n_tasks, n_scenarios, n_rubric


def check_readme(path: Path, n_tasks: int, n_scenarios: int, n_rubric: int) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    rel = path.name

    bench_rows = [ln for ln in text.splitlines() if BENCH_LINK in ln and ln.lstrip().startswith("|")]
    eval_rows = [ln for ln in text.splitlines() if EVAL_LINK in ln and ln.lstrip().startswith("|")]

    # Two row styles exist: the numbers table (`| **13** | [link] |`) and the
    # trust-surface table (`| ... | [link] · 13 tasks |`). Accept either.
    if not bench_rows:
        problems.append(f"{rel}: no stats-table row links to {BENCH_LINK}")
    for row in bench_rows:
        m = re.search(r"\*\*(\d+)\*\*", row) or re.search(r"\]\(benchmark/\)\s*·\s*(\d+)", row)
        if not m:
            problems.append(f"{rel}: benchmark row has no recognizable count: {row.strip()}")
        elif int(m.group(1)) != n_tasks:
            problems.append(
                f"{rel}: benchmark row says {m.group(1)} but benchmark/tasks has {n_tasks} tasks"
            )

    if not eval_rows:
        problems.append(f"{rel}: no stats-table row links to {EVAL_LINK}")
    for row in eval_rows:
        m = re.search(r"\*\*(\d+)\s*/\s*(\d+)\*\*", row) or re.search(
            r"\]\(eval-harness/\)\s*·\s*(\d+)\D+?(\d+)", row
        )
        if not m:
            problems.append(f"{rel}: eval-harness row has no recognizable 'scenarios / rubric' pair: {row.strip()}")
        elif (int(m.group(1)), int(m.group(2))) != (n_scenarios, n_rubric):
            problems.append(
                f"{rel}: eval-harness row says {m.group(1)} / {m.group(2)} but "
                f"eval-harness/scenarios has {n_scenarios} scenarios / {n_rubric} rubric items"
            )
    return problems


def main() -> int:
    n_tasks, n_scenarios, n_rubric = expected_counts()
    problems: list[str] = []
    for name in READMES:
        path = ROOT / name
        if not path.exists():
            problems.append(f"{name}: file missing")
            continue
        problems.extend(check_readme(path, n_tasks, n_scenarios, n_rubric))
    if problems:
        print("README rigor stats are stale:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        print(
            f"Update the stats rows to {n_tasks} benchmark tasks and "
            f"{n_scenarios} / {n_rubric} eval scenarios/rubric items in every README.",
            file=sys.stderr,
        )
        return 1
    print(
        f"README rigor stats OK across {len(READMES)} locales: "
        f"{n_tasks} benchmark tasks, {n_scenarios} / {n_rubric} eval scenarios/rubric items."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
