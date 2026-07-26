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
