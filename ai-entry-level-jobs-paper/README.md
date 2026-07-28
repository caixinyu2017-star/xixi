# Narrowing the Gate, Not Breaking the Ladder

Manuscript prepared for the MDPI journal **Systems**, Special Issue
*"Artificial Intelligence in Socio-Technical Systems"*.

**Title:** Narrowing the Gate, Not Breaking the Ladder: Artificial Intelligence,
Entry-Level Access and the Under-Provision of On-the-Job Training

## Deliverables

| File | What it is |
| --- | --- |
| `Narrowing_the_Gate_AI_Entry_Level_Access_Systems.docx` | The manuscript on the official *Systems* template. All symbols and the 24 display equations are native Word equation-editor (OMML) objects. |
| `Cover_Letter_Narrowing_the_Gate_AI_and_Entry_Level_Access.docx` | Cover letter, built from the author's own template. |
| `figs/fig1…fig7*.png` | The seven figures at 600 dpi. |
| `data/*.csv`, `build/stats.json`, `build/calibrated.json` | Every number reported in the paper, as produced by the pipeline. |

## The study in brief

**Question.** An entry-level job is a joint product: it delivers output today and it
is the only technology that turns a novice into an experienced worker. AI substitutes
for the first component and not the second. Does it break the career ladder, who bears
the cost, and which instrument should respond?

**Method.** A two-tier search-and-matching model (entry-level and experienced
jobseekers and employees) with endogenous mentoring, Nash-bargained wages subject to
Blanchard–Galí real rigidity at the entry level, free entry on both tiers, poaching,
and an AI input that substitutes for entry-level task output but cannot mentor. Two
contracting frictions separate the private from the social return to training:
non-contractible mentoring (hold-up) and poaching. Eight parameters are estimated
against eight Chinese labour-market moments; because the system is square the moment
conditions are solved **exactly** (max |log deviation| 7.0 × 10⁻¹⁴) rather than
minimised.

**Analyses.** Constrained-planner problem with costates; exact-decentralisation check;
Shapley decomposition of the wedge into hold-up and poaching; AI price path with the
planner solved alongside; Shapley channel decomposition of the employment response;
incidence as a function of wage rigidity; held-out cross-exposure validation;
first-best implementation and the optimal AI tax; four instruments at a common budget
with MVPF; Latin-hypercube uncertainty with **re-estimation on every draw**.

## Headline results

- **A large, pre-existing training externality.** The market provides **1/7.3** of the
  efficient amount of on-the-job training, so first promotion takes **3.50** years
  instead of **0.97**, and welfare is **1.39 %** below the constrained optimum — even
  though the Hosios condition holds *exactly* by construction. Hold-up accounts for
  **96 %** of the gap, poaching for **4 %**.
- **Proposition 1 verified numerically.** With Hosios, no poaching, contractible
  training and flexible wages, market and planner agree on every reported quantity to
  a relative error of **2 × 10⁻¹⁴** — a joint test of the value functions, the
  costates and the solver.
- **Incidence is institutional, not technological.** Doubling the AI task share lowers
  the entry-level employment rate by **7.2 %** and the entry wage by **3.0 %**, a ratio
  of **2.5 to 1**. In the flexible-wage economy the ratio is **0.03**: the wage absorbs
  everything. The widely cited "employment falls, pay doesn't" fact is evidence about
  wage rigidity, not about AI.
- **The ladder does not break** (the paper's main negative result, contrary to our
  prior). Firms mentor a smaller intake **79 %** more intensively; aggregate mentoring
  **+44 %**, promotion flow **+1.4 %**, experienced stock **+1.4 %**, time to promotion
  *falls*. The training wedge **narrows** from 7.3× to 5.3×. AI does not create or
  aggravate the externality.
- **Held-out validation.** With no employment-by-exposure information used anywhere in
  estimation, the model predicts a cross-occupation entry-level employment gradient of
  **−14.8 %** against the **−16 %** estimated from US payroll microdata
  (Brynjolfsson, Chandar & Chen 2025), and reproduces the employment-not-pay pattern.
- **Policy.** At a common budget the mentoring credit dominates: MVPF **14.3** against
  **1.85** for a vacancy subsidy and **−2.34** for a wage subsidy, which is worse than
  doing nothing because it crowds mentoring out. The AI tax cannot even raise the
  required revenue (Laffer peak 0.010 % of output against a 0.05 % budget), and the
  optimal AI tax once the ladder is subsidised is **zero**. The mentoring credit is
  best in **99 %** of uncertainty draws.

## What the numbers are, and are not

This is a **steady-state, representative-agent policy model**, not a forecasting model.
It compares long-run allocations and is silent about transition paths. The labour force
and entrant flow are exogenous, so the model cannot represent discouragement or delayed
entry; the entry-level *employment rate* is the right outcome here and maps only
imperfectly onto measured youth employment. Section 4.3 records an
**over-identifying check that fails**: firm-financed mentoring is 0.11 % of the wage
bill against 1.5–2.5 % reported by Chinese enterprises. Part is definitional and part
is the model's own claim; we report it as a failure rather than reinterpret it. Only
91 of 192 uncertainty draws re-estimated successfully, and that is stated in the paper.

## Reproducing everything

```bash
cd build
python3 calibrate.py       # -> calibrated.json  (exact solve of 8 moments)
python3 analysis.py        # -> stats.json, ../data/*.csv   (~25 min on 4 cores)
python3 schematics.py      # -> ../figs/fig1, fig2
python3 make_figures.py    # -> ../figs/fig3..fig7  (600 dpi)
python3 build_paper.py     # -> ../<manuscript>.docx
python3 make_cover_letter.py
```

Dependencies: `numpy scipy pandas matplotlib pillow python-docx`.

### Files in `build/`

- `ladder.py` — the model: matching, stocks, promotion technology, CES production with
  a fixed factor, values with Nash bargaining and real rigidity, free entry, the
  mentoring FOC (hold-up and contractible variants), the planner's costates, and
  `efficiency_check()`, which is Proposition 1 as an executable test. Channel
  deactivation is supported through `_frz`.
- `calibrate.py` — the exactly-identified estimation, with the identification argument
  (the three normalisations) documented in the module docstring.
- `analysis.py` — the full pipeline listed above.
- `schematics.py` — Figures 1–2; `make_figures.py` — Figures 3–7.
- `ai_equations.py` — the 25 display equations as OMML.
- `ai_refs.py` — the reference set (74 cited, 58 % published 2023–2026), reusing the
  pool verified for the companion paper plus entries verified here.
- `ai_content_a.py` / `ai_content_b.py` — the manuscript as a block model. Part B reads
  every number from `stats.json`, so the text cannot drift from the computation.
- `build_paper.py`, `make_cover_letter.py` — document assembly.

## Author block

The author block, affiliation and corresponding-author details are inherited from the
author's own *Systems* template and should be checked before submission.
