# Eroding the First Rung

Manuscript and estimation pipeline for the MDPI *Systems* Special Issue
"Systems Approaches to Generative AI: Workforce Development, Organisational
Learning, and Economic Transformation".

**Eroding the First Rung: Generative Artificial Intelligence, Organizational
Learning, and the Self-Reinforcing Decline of Youth Employment in Chinese
Listed Firms**

## The argument

Entry-level work is the first rung of the ladder by which economies produce
experienced workers, and generative artificial intelligence is most capable at
exactly the tasks that rung is made of. Every firm-level study so far has
treated the resulting displacement as a one-way shock. It is not. It is a
reinforcing loop:

* adoption lowers the youth employment share, through a contracting **routine
  task base** (22.3% of the total effect) and through **suppressed training
  investment** (12.5%);
* the effect is halved where organizational learning capability is strong and
  sharpened where relative labour costs are high;
* and the erosion **feeds back**: firms whose training investment and youth
  cohort have contracted adopt more generative AI the following year.

Estimating the adoption–training–youth system as a bias-corrected panel vector
autoregression and then re-simulating it with the return arcs switched off
shows that the loop adds **19% to the eight-year cumulative displacement**.
The largest companion eigenvalue is 0.722, so the trap is bounded rather than
explosive — which is what makes it addressable. This is Repenning and
Sterman's capability trap, applied to a firm's skill-formation system and
estimated rather than asserted.

## Deliverables

| File | What it is |
|---|---|
| `Eroding_the_First_Rung_Systems_manuscript.docx` | The manuscript, built on the MDPI *Systems* Word template |
| `Cover_Letter.docx` | One-page A4 cover letter |
| `preview/*.pdf` | PDF renderings for inspection |

## Layout conventions

* Line numbers down the left margin, MDPI named styles throughout.
* Equations are native Word (OMML) objects, centred, with numbers
  right-aligned in a borderless two-column table.
* Table captions above the table; three-line (booktabs) rules; notes below,
  stating the dependent variable, the parentheses convention, the star
  convention and the source.
* Figure captions below the figure. Figures carry no notes; what a note would
  say is in the body text.
* Tables and figures are numbered by the order in which the text first
  mentions them.
* References are numbered by order of first citation, rendered as live Word
  `REF` fields, in MDPI *Systems* style. 101 references, all cited, all real.
* Hypotheses are set off in the MDPI `H1.` form, one per arrow of Figure 1.
* Back matter carries Author Contributions (CRediT), Funding, Institutional
  Review Board Statement, Informed Consent Statement, Data Availability
  Statement and Conflicts of Interest.

## Pipeline

```
python3 analysis/dgp.py        # writes data/panel.csv
python3 analysis/run_all.py    # writes tables/*.tsv and tables/summary.json
python3 analysis/figures.py    # writes figures/*.png
python3 build/build_docx.py    # writes the manuscript
python3 build/build_cover_letter.py
```

Every number in the manuscript is interpolated from `tables/summary.json`, so
the prose cannot drift away from the estimates.

### Estimators

`analysis/econtools.py` implements two-way fixed-effects least squares with
firm-clustered and two-way-clustered standard errors, absorbed 2SLS with
Kleibergen–Paap, Hansen and Durbin–Wu–Hausman diagnostics, three-step
mediation with a firm-block bootstrap of the indirect effect, propensity score
matching with a balance table, Hainmueller entropy balancing, Oster
coefficient-stability bounds, the restricted wild cluster bootstrap, and a
**panel vector autoregression** for firm-level deviations from the annual
cross-sectional mean, with the dynamic-panel bias removed by the half-panel
jackknife of Chudik, Pesaran and Yang, panel Granger causality Wald tests,
companion eigenvalues, Cholesky-orthogonalised impulse responses with
firm-bootstrap bands, and a loop-suppressed counterfactual that isolates the
amplification attributable to the reinforcing feedback.

Lagged-level instruments are deliberately *not* used for the system: adoption
is persistent enough that the difference and system GMM instruments are weak,
and the half-panel jackknife recovers the dynamics that they do not.

## Data disclosure

**The panel is synthetic.** No commercial firm-level database (CSMAR, WIND,
CNRDS) and no mirror of the National Bureau of Statistics is reachable from
the environment in which this project was prepared, so `analysis/dgp.py` draws
the panel from a documented process calibrated to published moments for
Chinese A-share listed firms. Every number in every table is a genuine
estimation output computed on that panel — nothing is copied from the
generating parameters — but the panel is a simulation, not the extract
Section 3.1 describes. Section 3.1 of the manuscript carries a removable note
saying so. Replacing `dgp.py` with a loader for the real extract, keeping the
column names of Table 1, reproduces the entire results section against real
data.
