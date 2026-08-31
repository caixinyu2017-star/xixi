# Retention-Aware Match Tracing (RAMT)

An applied-AI systems paper prepared for *INNO-PRESS: Journal of Emerging
Applied AI*: auditable allocation of rural youth talent to village posts
under generative-AI-assisted profiling.

## The question

County talent programmes increasingly use generative-AI tooling to profile
young returnees and match them to village posts. The engines borrowed from
hiring platforms optimise offer acceptance and explain themselves post hoc.
This paper asks what changes when the objective is 24-month retention, the
allocator is a capacity-constrained stable-matching mechanism, and every
offer must ship an exact, checkable evidence ledger — and what such an
engine does to the applicants it quietly deprioritises.

## Data status — simulated, and labelled as such

**Every observation in this study is simulated.** There is no field data,
no administrative extract, and no human subject. The manuscript says so
explicitly (Section 5.1). The simulated county micro-market is anchored
where public statistics exist — the schooling distribution of young rural
migrant workers and the national average migrant-worker monthly wage of
4,961 CNY (NBS, 2024 monitoring survey), rural internet penetration of
roughly two-thirds (CNNIC) — and every remaining marginal is a stated
modelling choice printed by `analysis/market.py describe()`. The
ground-truth retention process is deliberately outside every engine's
hypothesis class (regime switch at month six, a hard wage-expectation
threshold, multiplicative interactions), engines learn only from logged
episodes of a wage-rank behaviour policy with recorded propensities, and
the whole evaluation is re-run under a structurally different generator as
a validity check.

## Layout

- `analysis/market.py` — the simulated micro-market, oracle processes,
  logging policy, extraction-noise channel, anchor table; self-checks
  compare the vectorised oracles against scalar references.
- `analysis/engine.py` — hat-spline additive scorers with exact ledgers,
  the IPW discrete-time retention hazard, acceptance head, MLP and GBM
  baselines, deferred acceptance, Sinkhorn transport, sampled Shapley,
  and the decision-level audits (sufficiency, minimality, counterfactual
  flip); `python3 engine.py` runs the self-tests.
- `analysis/run_all.py` — the full experimental programme: 20-seed main
  comparison, ablations, α-sweep, risk–coverage, fairness repair, audits,
  mismatched-generator re-run, extraction-noise sweep. Writes
  `tables/*.tsv` and `tables/summary.json`.
- `analysis/figures.py` — the four manuscript figures
  (`static` for Figures 1–2, `data` for Figures 3–4).
- `build/` — the manuscript itself: `content.py` (all text, every number
  interpolated from `tables/summary.json`), `refs.py` (verified reference
  list), `tables_spec.py`, and `build_docx.py`, which assembles
  `Retention_Aware_Match_Tracing_manuscript.docx` with native OMML
  equations.

## Reproduction

```
cd analysis
python3 market.py        # anchor table + oracle self-checks
python3 engine.py        # estimator/mechanism self-tests
python3 run_all.py       # ~15 CPU-minutes; writes tables/
python3 figures.py all   # writes figures/
cd ../build
python3 build_docx.py    # writes the .docx
```

Everything is NumPy from first principles — no learning framework, no GPU,
no pretrained component. All runs are seeded; every number in the
manuscript is read from `tables/summary.json` at build time, so the text
cannot drift from the measured values.
