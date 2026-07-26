# MSSBOA — source code, data and results

Reference implementation and full experimental record for

> **A Multi-Strategy Secretary Bird Optimization Algorithm for Aesthetic Color
> and Layout Optimization in Visual Art Design**
> Lin Zhou, Xinyu Cai — submitted to *Biomimetics*, Special Issue
> "Advances in Biological and Bio-Inspired Algorithms: 2nd Edition".

This directory is the public code release requested by Reviewer 1 and by
Reviewer 3 (comment 5). Everything needed to re-run the experiments and
regenerate the tables and figures of the revision is here.

## Layout

```
code/
  framework.py          FE-budget runner shared by every algorithm
  algos_mssboa.py       SBOA and MSSBOA (GPSI + LOBL + ACGM), fully parameterized
  algos_variants.py     MISBOA, CGSBOA, LTSBOA, TSA, MS-TSA, CPA, I-CPA
  algos_classic.py      PSO, DE, GWO, WOA, SCA, HHO, SSA, DBO, COA, RIME, LSHADE
  design_problems.py    colour-harmony (Eqs. 15-19) and layout (Eqs. 20-22) objectives
  bench.py              CEC2017 wrapper and the function-class map
  cec2017/              vendored CEC2017 suite (see "Benchmark suite" below)
  run_cec.py            benchmark experiments (variants / factorial / params)
  run_design.py         design experiments (weights / scalability / palette)
  diagnose.py           reproducibility diagnostic, see NOTES.md
  analyze_losses.py     loss distribution over CEC2017 function classes
  make_tables.py        turns raw CSVs into the manuscript tables
  draw_figs.py          Figure 2 (lens imaging) and the redrawn Figures 4-5
  build_revision.py     builds the colour-marked revised manuscript
  build_responses.py    builds the three response letters
results/                raw per-run CSVs and the derived tables
figs/                   figures at 300 dpi
out/                    revised manuscript and response letters
src/original.docx       the submitted manuscript, used as the edit base
```

## Requirements

```
python >= 3.9
numpy scipy matplotlib python-docx
```

## Benchmark suite

The CEC2017 suite under `code/cec2017/` is vendored from
[cec2017-py](https://github.com/tilleyd/cec2017-py) by Duncan Tilley (MIT
licence, © 2022), which reproduces the official shift, rotation and shuffle
data of Awad et al. (2016). It is used rather than a hand-rolled
implementation so that the benchmark values are those of the official suite.
Correctness was verified by checking that f(o) equals the bias exactly for
F1–F20.

The 24 MB data file is not stored in git. Fetch it once with:

```bash
curl -L -o code/cec2017/data.pkl \
  https://raw.githubusercontent.com/tilleyd/cec2017-py/master/cec2017/data.pkl
```

> **Note.** The `opfunu` package's CEC2017 implementation was evaluated first
> and found to be unreliable — several functions use the wrong basic function
> or omit the per-component shrink rate, producing values off by many orders of
> magnitude (e.g. F16 returning ~1e17 at 30D). It should not be used to
> reproduce these results.

## Reproducing the experiments

```bash
cd code
python3 run_cec.py variants@10,30 params@10 factorial@10   # CEC2017 studies
python3 run_design.py scale weights palette                # design studies
python3 analyze_losses.py                                  # loss breakdown
python3 make_tables.py                                     # derived tables
python3 draw_figs.py                                       # figures
```

Every run is seeded deterministically from
`(algorithm, function, dimension, run index)`, so the CSVs in `results/` are
reproducible exactly.

## Fair-evaluation policy

Every algorithm is charged for **every** function evaluation it performs,
including those consumed by auxiliary operators. In MSSBOA the LOBL refractions
and the ACGM mutation are counted against the budget, so the number of
iterations is `max_fes / (2N + |LOBL| + p_m)` rather than `max_fes / 2N`. This
matters: not charging for auxiliary evaluations silently grants a variant more
budget than its baseline.

## Comparison algorithms

The source codes of MISBOA, CGSBOA, LTSBOA, MS-TSA and I-CPA are not publicly
distributed. Each was re-implemented from the equations, control parameters and
pseudo-code of the corresponding publication; the base algorithms TSA and CPA
are implemented as well so that each variant's gain over its own base is
visible rather than assumed. These re-implementations are our reading of the
published descriptions and are released here so that they can be audited and
corrected.

## Please read NOTES.md

`NOTES.md` records a reproducibility problem found while preparing this
release. It should be read before the results in this directory are compared
with the tables of the submitted manuscript.
