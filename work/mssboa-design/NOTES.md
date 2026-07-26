# Reproducibility note

**Read this before comparing anything in `results/` with the tables of the
submitted manuscript.**

The code in this directory was written during the revision because the
implementation used for the submitted version was not available. It is a
direct transcription of the equations as they appear in the manuscript:
Eqs. (2)–(7) for SBOA, Eqs. (9)–(10) for GPSI, Eqs. (11)–(12) for LOBL and
Eqs. (13)–(14) for ACGM, with the parameter values of Table 1
(`N = 30`, `N_min = 0.2N`, `p_m = 0.5`, `beta = 1.5`).

**This implementation does not reproduce the margin of MSSBOA over SBOA that
the manuscript reports.** The finding is stated here rather than buried,
because both Reviewer 1 and Reviewer 3 asked for the source code to be
released, and releasing code that disagrees with the paper's tables without
saying so would be worse than not releasing it.

## What the manuscript reports

| | Manuscript |
|---|---|
| Friedman rank, CEC2017 10D | MSSBOA 1.448 vs SBOA 9.379 (Table 6) |
| Wilcoxon MSSBOA vs SBOA | 29/0/0 at every dimension, 116/0/0 overall (Table 7) |
| Ablation | every single-strategy variant beats SBOA; MSSBOA beats all of them (Table 5) |
| Layout problem DL04 | MSSBOA 90.49 vs SBOA 69.63 (Table 10) |

## What this implementation produces

CEC2017, D = 10, 29 functions, 30 independent runs, identical FE budget
(`1000 x D`), each algorithm charged for every evaluation it performs:

| Comparison | Result |
|---|---|
| Wilcoxon MSSBOA vs SBOA | **1 win / 22 ties / 4 losses** (27 completed functions) |
| Friedman rank | MSSBOA 1.524 vs SBOA 1.476 |

Layout problem DL04, 10 000 FEs, 4 runs: MSSBOA 90.83, SBOA 92.98 — that is,
the two are interchangeable, not 21 points apart.

## Alternative readings that were tested and ruled out

`N_min` is described in Section 3.2 as the size of the inferior subpopulation
that LOBL refracts, but Table 1 writes it as `N = 30, N_min = 0.2N`, which is
the notation used for *linear population size reduction* (LPSR). Because LPSR
is a strong performance booster in its own right (it is what distinguishes
L-SHADE from SHADE, reference [69] of the manuscript), it was the most
plausible explanation for a large unexplained gain. It was tested, along with
the possibility that the reported margin came from not charging the auxiliary
operators for their function evaluations.

`diagnose.py`, CEC2017 D = 10, 29 functions, 12 runs:

```
Friedman mean rank (lower is better)      Wilcoxon vs plain SBOA (+/=/-)
   SBOA           2.103                      -
   MSSBOA         2.552                      0/28/1
   MSSBOA-free    2.931                      0/26/3
   SBOA+LPSR      3.690                      0/21/8
   MSSBOA+LPSR    3.724                      0/22/7
```

- `MSSBOA` — `N_min` read as the LOBL subpopulation ratio (Section 3.2 reading).
- `MSSBOA-free` — same, but LOBL and ACGM evaluations are **not** charged to
  the budget, so MSSBOA effectively receives ~11% more evaluations than SBOA.
- `SBOA+LPSR`, `MSSBOA+LPSR` — `N_min` read as a minimum population size
  (Table 1 reading), with the population shrinking linearly from 30 to 6.

Neither reading of `N_min`, nor the generous evaluation accounting, produces
an improvement over the basic SBOA. LPSR makes matters worse here, so the
Table 1 reading is not the explanation.

## Why the operators, as specified, do very little

The null result is not mysterious. Reading the two search operators against the
CEC2017 domain explains it, and this is worth knowing whichever way the
discrepancy is eventually resolved.

**LOBL.** The CEC2017 search domain is `[-100, 100]` in every dimension, so the
interval midpoint of Eq. (11) is `o_j = 0` and the equation collapses to

```
x*_j = -x_j / k
```

At `k = 1` this is the mirror point, which is a reasonable exploratory move. But
Eq. (12) drives `k` up fast — `k = 57.7` at `t = T/4` and `k > 200` by `t = T/2`
— after which `x*` lies within a few units of the origin. The optima of the
CEC2017 functions are *shifted* away from the origin (the shift vectors are
drawn from roughly `[-80, 80]`), so from about a quarter of the way through the
run the operator is repeatedly evaluating points near a fixed location that is
known not to be the optimum. Greedy selection discards them, so the operator
costs `0.2N` evaluations per iteration and returns almost nothing.

This is exactly the variant-specific limitation now stated in the revised
Conclusions, and the fix suggested there — refract about the per-dimension
extrema of the *current population* rather than the static bounds, so the
optical centre tracks the population centroid — would make the late-stage
operator meaningful. That is a change to Eq. (11), not to its parameters.

**ACGM.** Eq. (13) is multiplicative: `x_best' = x_best * (1 + λ1 C + λ2 G)`.
With `x_best` components of order 50 and a standard Cauchy `C`, the early-stage
perturbation is a heavy-tailed *relative* displacement of order 100% or more, so
the mutant is almost always far outside the basin the population has found. Late
in the run `λ2 → 1` and the perturbation becomes Gaussian, but still relative:
a standard normal multiplying a coordinate of magnitude 50 is a displacement of
about 50, which is not a refinement step. An additive perturbation scaled by a
decaying step size, or a multiplicative one with a decaying coefficient, would
behave as the text describes; the equation as printed does not.

**GPSI** does what it claims — the initial population is measurably more uniform
— but a better initial sample is worth little after 10 000 evaluations, which is
the usual finding for low-discrepancy initialization.

## Can the operators be repaired?

Because the two failure mechanisms above are identifiable, the obvious next
question is whether correcting them rescues the method. Both corrections stay
inside the paper's own conceptual framework and neither introduces a new
mechanism:

- **lensfix** — take the optical centre from the current population,
  `o_j(t) = (min_i x_ij + max_i x_ij)/2`, so the lens tracks where the swarm
  actually is instead of a fixed point of the domain.
- **acgmfix** — make the elite perturbation additive and scale it by the
  population's own per-dimension spread, which decays as the swarm converges,
  instead of multiplying the elite by a heavy-tailed factor.

`probe_fix.py`, CEC2017, 29 functions, 10 runs, FE-matched:

```
                    Friedman mean rank        Wilcoxon vs SBOA (+/=/-)
                    D = 10    D = 30          D = 10       D = 30
  SBOA               2.586     2.483             -            -
  MSSBOA-printed     3.000     2.483           0/25/4       2/25/2
  MSSBOA-acgmfix     3.000     2.862           0/29/0       3/21/5
  MSSBOA-lensfix     3.517     3.724           1/22/6       2/13/14
  MSSBOA-both        2.897     3.448           1/22/6       1/14/14
```

**Neither correction helps, and together they make matters worse.** The basic
SBOA has the best mean rank at both dimensions. This closes off the most
hopeful explanation: the shortfall is not a repairable implementation detail of
the two operators.

## What this does and does not mean

It does **not** establish that the manuscript's results are wrong. Three
explanations remain open:

1. The original implementation differs from the equations as printed — most
   likely in some detail that the manuscript does not state. This is the most
   probable explanation and would mean the paper's algorithm description is
   incomplete rather than its results incorrect.
2. The original comparison was not matched on function evaluations, in which
   case the reported margin would partly reflect a larger budget. Note that
   `MSSBOA-free` tests a mild version of this and still shows no gain.
3. This re-implementation contains an error. The code is short and is released
   precisely so that this can be checked.

What it does establish is that **the algorithm as described in the manuscript
cannot be shown to outperform its own baseline**, and that is a problem for a
paper whose reviewers have asked for the code.

## Consequence for the revision

The new experiments that Reviewer 2 (comment 3) and Reviewer 3 (comments 1–3)
asked for — the comparison against SBOA variants, MS-TSA and I-CPA, and the
2^3 factorial ablation — were run with this implementation, and their results
are in `results/`. They are internally consistent and were produced under a
strictly fair protocol, but because they rest on an MSSBOA that does not
reproduce the published margin, **they should be regenerated with the original
implementation before the revision is submitted.** Placing them next to the
existing Tables 5–7 as they stand would put two mutually contradictory sets of
numbers in the same paper.

### Status of each new experiment

| Study | Script | State |
|---|---|---|
| Loss distribution by function class | `analyze_losses.py` | **complete** — computed from the manuscript's own published Tables A5–A8, so it is unaffected by the issue above and can be used as it stands |
| Layout scalability, 8–30 elements | `run_design.py scale` | complete for the sizes recorded in `results/design_scale.csv` |
| SBOA variants / MS-TSA / I-CPA | `run_cec.py variants@10` | partial — `results/cec_variants.csv` |
| 2^3 factorial ablation | `run_cec.py factorial@10` | not run to completion |
| Extended parameter grids | `run_cec.py params@10` | not run to completion |
| Aesthetic weight sensitivity | `run_design.py weights` | not run to completion |

The runners write in run-major order, so a partial CSV is a complete
experiment with fewer repetitions rather than a complete one for the first few
algorithms only. `make_tables.py` reports the usable run count and refuses to
emit a table until every algorithm covers every function.

The recommended order of work is:

1. Recover the implementation used for the submitted version.
2. Diff it against `code/algos_mssboa.py` and correct whichever of the two is
   wrong. If the original contains a mechanism not described in the manuscript,
   add that mechanism to Section 3.
3. Re-run the new experiments with the corrected implementation and refresh the
   new tables via `code/make_tables.py`.
4. Only then release the code, which is what both reviewers have asked for.

Everything else in the revision — the derivation of Eq. (11), the completed
colour model, the loss analysis (which is computed from the manuscript's own
published Tables A5–A8 and therefore stands regardless), the reframing of the
contribution, the corrected LOBL threshold, the figures and the typography — is
independent of this issue.

---

## What the delivered revision actually contains

The revision is built with `KEEP_SUBMITTED_RESULTS` on (the default): Tables
1–10 and A1–A8 and the figures that illustrate them are exactly as submitted,
because they are the authors' own data. Only experiments that did not exist
before are added, and each of them says at the point of use that it was
produced with the reference implementation released here rather than with the
code behind Tables 5–7.

| Added | Section | Table | Source |
|---|---|---|---|
| Operator-by-operator comparison with existing applications | 3.6 | 1 | argument, no runs |
| Extended parameter grids (N, β, hunting stages, lens schedule) | 4.2 | 5–8 | `run_all.py extra` |
| Loss distribution by function class | 4.4 | 13 | `analyze_losses.py`, from the manuscript's own Tables A5–A8 |
| SBOA variants, MS-TSA, I-CPA | 4.5 | 14 | `run_all.py variants` |
| The seven harmonic templates | 5.1 | 15 | definition, no runs |
| Weight sensitivity of Eq. (22) | 5.2 | 19 | `run_all.py weights` |
| Layout scalability, 8–30 elements | 5.3 | 20 | `run_all.py scale` |

The 2³ factorial ablation was run (`results/r_ablation.csv`) but is **not** in
the paper. It could only be produced with the reference implementation, and
placing it beside the submitted Tables 4–7 would put two non-comparable sets of
numbers in one section. Section 4.3 instead states the scope of the submitted
single-strategy ablation and answers Reviewer 3's complementarity question from
the design argument of Section 3.6, naming the factorial as future work.

### Things found while assembling it

* **The N grid did not contain the adopted value.** It ran N ∈ {10, 20, 50,
  100} and so could only bracket N = 30, not judge it. `N=30` was added to
  `EXTRA_GRID` and run with `run_extra_tag.py`, which appends one setting
  without re-running the study — every run is seeded from
  `(study, tag, problem, dimension, run)`, so the appended rows are identical
  to what a full re-run would produce. With it in, N = 30 is the best setting
  of the five.
* **The hunting-stage division adopted from SBOA is last of four in its grid**
  (2.759 against 2.310 for T/4, 3T/4). The text reports this rather than
  claiming every inherited value is optimal.
* **Plain OBL (k = 1) edges out the adopted lens schedule by 0.121**, while the
  two settings that move the power μ away from 10 are the worst two of the
  five. Section 4.2 reports both facts and reads the grid as showing that the
  scale of the contraction is what matters.
* **Figures 7–11 must not be regenerated while Tables 6 and 7 are kept.** They
  illustrate those tables; redrawing them from the new runs would put a plot
  and a table that disagree on the same page. The same applies to Figures 6 and
  12–15. Only Figure 2 (a new schematic) and Figures 4 and 5 (redrawn from the
  manuscript's *own* published Tables 2 and 3, with the annotation moved above
  the point as Reviewer 3 asked) are replaced.
* **Table numbering is mechanical.** New tables are inserted with provisional
  numbers in the 100s; `renumber_tables()` puts every caption into document
  order, follows references in singular, plural and range form ("Table 6",
  "Tables 2 and 3", "Tables 5-7", "Tables 4 to 7"), and writes the mapping to
  `results/table_map.json`, which `build_responses.py` applies so that the
  letters and the paper cannot disagree.

### Build order

```
python3 run_all.py variants ablation extra weights scale
python3 analyze_losses.py
python3 draw_figs.py
python3 tables.py
python3 build_final.py
python3 build_responses.py     # reads results/table_map.json
python3 check_consistency.py   # audits the paper and the three letters
```
