# Paper 7 — "The Vanishing First Rung"

Target: MDPI *Systems*, Special Issue **"Navigating Digital Transformation: Leadership
and Decision Making in Today's Systems"** (Guest Editor Prof. Dr. Maja Meško).

Full title: *The Vanishing First Rung: A System Dynamics Study of Entry-Level
Automation, Senior Time Allocation and the Erosion of the Professional Expertise
Pipeline.*

## What the paper does

A two-stage study of what happens to a profession's stock of expertise when
generative AI automates the routine, supervised tasks that firms have always used
to train new graduates.

* **Study 1** — an enterprise survey of 356 knowledge-intensive firms in the
  Yangtze River Delta. It measures administrative quantities (headcounts, hours,
  shares), not attitude scales, and estimates the six behavioural parameters the
  simulation needs: AI–junior substitutability φ, verification load ν, reference
  mentoring intensity m\*, reference time to proficiency τ₀, mentoring elasticity
  a, practice-displacement θ and the AI-as-tutor coefficient λ.
* **Study 2** — a five-stock system dynamics model (entrant pool P and its skill
  capital Q, juniors J, seniors S, perceived scarcity W) calibrated on those
  estimates, validated against the standard confidence-building protocol, and used
  for counterfactual, threshold, structural-decomposition and policy experiments
  over a 30-year horizon.

## Headline results

| Result | Value |
|---|---|
| Senior stock at year 30 vs. no-automation counterfactual | −46.3% |
| Productive capacity: peak, crossover, year 30 | +8.7% (yr 8.9), yr 16.6, −15.4% |
| Entry hiring at years 3 / 5 (matches published ≈−13%) | −11.3% / −22.9% |
| Regime shifts (asymptotic automation depth) | 0.475 mentoring collapse, 0.725 verification binds |
| Damage from substitution + practice displacement | 41.2 of 46.3 pp |
| Damage from the mentoring loops | 5.7 pp (engages only after yr 23) |
| The balancing loop's own contribution | −2.7 pp (self-defeating) |
| Efficiency: subsidy vs. AI-augmented apprenticeship | 0.306 vs. 0.122 extra hires per extra senior-year |
| Senior-stock gap negative across 500 LHS draws | 99.6% |

## Pipeline

```
python p7_survey.py      # Study 1  -> p7_survey.json
python p7_model.py       # Study 2  -> p7_model.json, p7_traj.json
python p7_figures.py     # Figures 1-7 (320 dpi) from the JSON only
python build_paper7.py   # -> Vanishing_First_Rung_Expertise_Pipeline_Systems.docx
python make_cover_letter7.py
```

Every number in the manuscript is read from the JSON outputs, so the text, the
tables and the figures cannot disagree. Display equations are OMML (Word's native
equation format), as are inline symbols.

## Files

| File | Purpose |
|---|---|
| `p7_survey.py` / `p7_survey.json` | Study 1: DGP, OLS with HC3 SEs, delta-method ratios, diagnostics |
| `p7_model.py` / `p7_model.json` / `p7_traj.json` | Study 2: RK4 integration, sweep, knockouts, extreme-condition tests, LHS/PRCC, policies |
| `p7_figures.py` / `p7_fig1-7.png` | Causal loop diagram, stock-flow map, marginal effect, reference behaviour, thresholds, policies, sensitivity |
| `p7_equations.py` | The 15 display equations as OMML |
| `p7_content_a.py` / `p7_content_b.py` | Manuscript text as structured blocks |
| `p7_refs.py` / `refs_pool.json` | 77 cited references (66% from 2023–2026) plus the verification evidence |
| `build_paper7.py` | Assembles the Systems-template .docx |
| `make_cover_letter7.py` | Cover letter from the user's template |

## Reference verification status

The 49 references new to this paper were collected through a multi-agent discovery
stage with source evidence recorded in `refs_pool.json` (`tier` field). Six passed
two independent verification rounds; the remaining 43 passed one round with cited
sources. A second adversarial round could not be completed because this session's
web-search budget was exhausted. **A spot-check of the reference list against
Google Scholar is recommended before submission.**
