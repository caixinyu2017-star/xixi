# The Queue Absorbs the Shock

Manuscript prepared for the MDPI journal **Systems**, Special Issue
*"Systems Thinking and Modelling in Socio-Economic Systems"*.

**Title:** The Queue Absorbs the Shock: Administrative Job Rationing, Delayed
Retirement and the Blind Spot in Youth Unemployment Statistics

## Deliverables

| File | What it is |
| --- | --- |
| `The_Queue_Absorbs_the_Shock_Job_Rationing_Systems.docx` | The manuscript on the official *Systems* template. Every symbol and all 24 display equations are native Word equation-editor (OMML) objects. |
| `Cover_Letter_The_Queue_Absorbs_the_Shock.docx` | Cover letter, built from the author's own template. |
| `figs/fig1…fig7*.png` | The seven figures at 600 dpi. |
| `data/*.csv`, `build/stats.json`, `build/calibrated.json` | Every number reported in the paper, as produced by the pipeline. |

## The study in brief

**Question.** China began raising its statutory retirement age on 1 January 2025.
The public debate asks whether older workers staying longer will cost younger
workers their jobs. That question has a well-established answer — no — but it is
not the question young people are asking. Where part of the labour market is
rationed by administrative rule rather than cleared by price, the two questions
"will I be displaced from a job I hold?" and "will the job I am preparing for
still be there?" have different answers, and the headline indicator can see only
the first.

**Method.** A two-sector, two-age continuous-time search-and-matching model. An
establishment sector (government agencies and public institutions, ~12 % of urban
employment) has a headcount fixed at `N̄` by administrative rule, so its vacancy
flow is `v_Q = δ_Q·N̄ + ρ·E_q` — separations plus retirements, and nothing else.
A market sector has free entry and Nash-bargained wages under the Hosios
condition, so it is efficient by construction and every distortion reported comes
from rationing. Because establishment posts pay a compensation premium and are
allocated by examination, the young queue for them under a Harris–Todaro
indifference condition; an examination age ceiling means only the young queue.
Six structural parameters are estimated against six published Chinese moments;
because the system is square the moment conditions are solved **exactly**
(max |log deviation| 1.1 × 10⁻¹⁶) rather than minimised.

**Analyses.** Baseline allocation and the Harris–Todaro deadweight loss; a
break-even screening value for the examinations; the phased reform year by year;
the crowding-out coefficient; a Shapley decomposition over the three routes the
retirement hazard takes (quota, horizon, demographic); the indicator wedge; three
instruments at a common budget with MVPF; full indexation of the establishment to
the labour force; sensitivity to the size of the rationed sector and to the
premium with re-estimation at each value; Latin-hypercube uncertainty over six
externally set parameters with **re-estimation on every draw**.

## Headline results

- **The lump-of-labour hypothesis is rejected.** The crowding-out coefficient is
  **−0.0006** against −1 under lump-of-labour. Prime-age employment rises 13.6 %,
  young employment falls 0.035 %, output rises 11.1 %. This reproduces the
  international consensus in a model never calibrated to it.
- **Access falls anyway, and nobody is displaced.** The chance that a member of an
  entering cohort ever holds a rationed job falls **5.7 %**, from 17.46 % to
  16.45 % — about **127,000** young people a year at a cohort of 12.7 million. A
  Shapley decomposition attributes **100 %** of that fall to the quota route; the
  horizon and demographic routes contribute exactly zero, because by the
  establishment constraint the vacancy flow depends on the retirement hazard and
  on nothing else the reform touches.
- **The indicator is structurally blind.** The youth unemployment rate moves
  **+0.029 pp** over the whole fifteen-year reform, because three channels of
  opposite sign nearly cancel inside it: quota **−1.03**, horizon **+0.66**,
  demographic **+0.52** log points. Access falls **35×** more than the headline
  rate moves. Over a plausible range of the rationed share the indicator does not
  even get the sign right.
- **The apparent welfare gain is mechanical.** The value of being a new entrant
  rises 4.13 %, of which **+4.10** log points is the horizon route (a longer
  working life over which to collect the same flows) and **+0.002** the quota
  route.
- **The queue is expensive.** It costs **1.94 %** of output a year. Selection by
  examination would have to raise the productivity of every establishment worker
  by **45.6 %**, permanently, for the observed queue to be efficient.
- **The intuitive remedy backfires.** At a common budget of 0.1 % of output,
  expanding the establishment raises access 0.71 % but *lowers* welfare per head
  and returns an MVPF of **0.92** — worse than leaving the money alone — because a
  larger prize draws a longer line. Cutting the administered premium returns
  **1.59**; a market vacancy subsidy returns **1.13**. Full indexation restores
  177 % of the lost access but costs 1.38 % of output and lowers welfare per head
  0.10 %.
- **Robust.** Over 192 Latin-hypercube draws with re-estimation on every draw:
  access falls in **100 %** of draws (mean −5.5 %, [−7.2 %, −4.2 %]); the youth
  unemployment rate moves less than 0.5 pp in **100 %**; cutting the premium is
  best in **100 %**; expanding the establishment lowers welfare in **100 %**. The
  one parameter that governs the size of the effect is the establishment
  separation rate (correlation with the fall in access, 0.96) — a testable
  prediction.

## Over-identifying check

Three separately sourced targets — a rationed sector of 12 % of employment, a
queue accounting for 35 % of youth non-employment, and a youth unemployment rate
of 17.8 % — jointly imply an expected queueing duration of **2.50 years**. That is
not a target; it is an implication, and it matches the independent observation
that successful candidates commonly sit the annual examinations two or three
times.

## Reproducing

```bash
cd build
python calibrate.py      # exact identification -> calibrated.json
python analysis.py       # counterfactuals -> stats.json, ../data/*.csv
python schematics.py     # figures 1-2
python make_figures.py   # figures 3-7
python build_paper.py    # -> ../The_Queue_Absorbs_the_Shock_Job_Rationing_Systems.docx
python make_cover_letter.py
```

`rq_content_a.py` and `rq_content_b.py` read every reported number from
`stats.json` and `calibrated.json`, so the text cannot drift from the computation
that produced it. `rq_refs.py` reuses the reference pool verified for the two
companion papers and adds fifteen entries confirmed against the publisher record;
75 references are cited, 51 % of them from 2023–2026.
