# A Moving Target, Not a Tipping Point

Manuscript prepared for the MDPI journal **Systems**, Special Issue
*"Systems Thinking for Real-World Problem Solving"* (Guest Editor: Dr. Natalie Clewley,
Cranfield University; Section *Systems Practice in Social Science*; deadline
31 August 2026).

**Title:** A Moving Target, Not a Tipping Point: Attractor Drift, Queue Congestion and
Policy Sequencing in the Youth School-to-Work Transition System of China's
Prefecture-Level Cities

## Deliverables

| File | What it is |
| --- | --- |
| `Youth_School_to_Work_Transition_System_China_Systems.docx` | The manuscript, on the official *Systems* template. All symbols and the 20 display equations are native Word equation-editor (OMML) objects. |
| `Cover_Letter_Youth_School_to_Work_Transition_System_China.docx` | Cover letter, built from the author's own template. |
| `figs/fig1…fig7*.png` | The seven figures at 600 dpi. |
| `data/*.csv`, `build/stats.json` | Every number reported in the paper, as produced by the analysis pipeline. |

## The study in brief

**Question.** Why do youth employment outcomes deteriorate in an economy where jobs are
plentiful and the digital economy is expanding, and which policy levers actually move
the system?

**Method.** A six-state continuous-time feedback model (open searchers, exam-oriented
queuers, matched employment, mismatched employment, employability capital, aspirations)
coupled to an employer skill threshold that rises with digitalisation and with observed
mismatch. Six structural parameters are estimated by simulated method of moments against
seven published national moments; the calibrated model reproduces all seven within
1.7 per cent (RMSPE 1.16 per cent). The unit of analysis is national; heterogeneity
across China's roughly three hundred prefecture-level cities is represented by
re-parameterising the same structure as three city archetypes.

**Analyses.** Fixed-point continuation and a multi-start uniqueness search over 40
parameter cells; eigenvalue and relaxation-time analysis; loop-deactivation dominance
analysis (Ford 1999); shock persistence; Latin-hypercube Monte Carlo (n = 4096); Sobol
variance decomposition (Saltelli estimator, 14,336 runs, bootstrap CIs); logistic and
cross-validated CART meta-models of the simulation output; equal-effort policy
experiments with sequencing; city archetypes.

**Headline results.**

- The system is **globally monostable** — no fold, no hysteresis anywhere searched.
  What generates persistence is a *drifting attractor* (equilibrium non-employment rate
  0.117 → 0.637, 2015–2040) combined with a slow state (slowest relaxation time exactly
  8 years), so the realised state lags its own equilibrium by ~1.7 years.
- A three-year demand shock decays with a **half-life of 1.5 years**; the threshold drift
  does not decay. The problem is structural, not cyclical.
- Loop dominance: aspiration adjustment (30.3 %) and exam-queue congestion (17.5 %) are
  the brakes; threshold escalation (27.8 %) is the dominant amplifier.
- Sobol: threshold sensitivity to digitalisation explains **66.3 %** of output variance;
  training intensity **0.1 %**.
- At equal standardised effort, moderating threshold escalation lowers the 2040 rate by
  **0.157**, ~19× vacancy creation and ~40× training intensity.
- Sequencing matters at unchanged cumulative effort: guidance-before-matching beats the
  reverse by 0.021 in the mean 2025–2040 rate.
- The digital-core city archetype ends with the **worst** outcome (0.732 vs 0.251), but
  the largest absolute policy dividend accrues to the intermediate manufacturing
  archetype (0.201), which is where intervention should be targeted.

## What the numbers are, and are not

The model is a **policy-analysis model, not a forecasting model**. Values for 2030–2040
are structure-unchanged counterfactuals. Calibration targets are published national
aggregate statistics; the digital-intensity driver is a logistic fitted by least squares
to the NBS series for 2020, 2023 and 2024 plus the 2030 policy target (maximum residual
0.06 pp). No individual-level data were used and none were fabricated. All simulation
results in the paper are outputs of the code in `build/`. Sections 3.3 and 5.7 of the
manuscript state these limits explicitly.

## Reproducing everything

```bash
cd build
python3 calibrate.py        # -> calibrated.json  (SMM, differential evolution)
python3 analysis.py         # -> stats.json, ../data/*.csv   (~15 min on 4 cores)
python3 sd_figures.py       # -> ../figs/fig1, fig2  (Vensim-convention SD diagrams)
python3 make_figures.py     # -> ../figs/fig3..fig7  (600 dpi result figures)
python3 build_paper.py      # -> ../<manuscript>.docx
python3 make_cover_letter.py
```

Dependencies: `numpy scipy pandas statsmodels scikit-learn matplotlib pillow`.

### Files in `build/`

- `model.py` — the six-state model: drivers, auxiliaries, vector field, RK4 integrator,
  fixed-point solver, Jacobian, indicators. Supports link deactivation via `_frz`.
- `calibrate.py` — simulated method of moments; 7 moments, 6 free parameters.
- `probe.py`, `probe_pi.py` — the multi-start searches that established monostability
  (including the check that ruled out an apparent fold in Π as a continuation artefact).
- `analysis.py` — the full pipeline (baseline, attractor drift, continuation, knockout,
  Monte Carlo, Sobol, meta-models, policies, sequencing, archetypes).
- `sd_figures.py` — Figures 1–2 in the Vensim idiom; `make_figures.py` — Figures 3–7.
- `ysts_equations.py` — the 20 display equations as OMML.
- `ysts_refs.py` — the reference set (65 cited; 65 % published 2023–2026).
- `ysts_content_a.py` / `ysts_content_b.py` — the manuscript text as a block model.
- `build_paper.py`, `make_cover_letter.py` — document assembly.

## Figures

Figures 1 and 2 follow standard system-dynamics (Vensim) convention: auxiliary and rate
variables are plain text with no enclosing box, stocks are rectangles, material flows are
double-line pipes with hourglass valves and cloud boundaries, information links are thin
curved blue arrows, and every label carries a white halo so that no link is occluded.
They are drawn programmatically so that each arrow and polarity sign matches the model
exactly. `figs/ai_cld.png` and `figs/probe_cld.png` are gpt-image-2 renderings kept for
reference: the typography is clean but the generated causal structure does not match the
model, which is why the vector versions are the ones used in the manuscript.

## Author block

The author block, affiliation and corresponding-author details are inherited from the
author's own *Systems* template and should be checked before submission.
