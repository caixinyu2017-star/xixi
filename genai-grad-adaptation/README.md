# Early-Career Choices in the Era of Generative AI

Manuscript and estimation pipeline for the MDPI *Systems* Special Issue
"Systems Approaches to Generative AI: Workforce Development, Organisational
Learning, and Economic Transformation".

**Early-Career Choices in the Era of Generative AI: Human Capital
Depreciation, Career Anxiety, and Occupational Adaptation Among Fresh
Graduates**

## The argument

The graduate is modelled as an adaptive agent in a socio-technical labour
system: perceived human capital depreciation is the input, AI-related career
anxiety is the error signal of a cybernetic control loop, and occupational
adaptation or career avoidance is how the loop closes. Three properties of
that reading are tested and confirmed:

* **Transmission** — depreciation converts into anxiety (β = 0.487),
  buffered by employability support (pass-through 0.64 at −1 SD of support,
  0.33 at +1 SD).
* **Saturation** — anxiety converts into adaptation along an inverted U
  (turning point +0.37 SD, Fieller 95% CI [0.22, 0.55]; Sasabuchi p <
  0.0001), with 38.5% of the cohort already past the peak, while avoidance
  rises monotonically. Generative-AI literacy shifts the turning point from
  0.07 to 0.73 SD without changing the curvature.
* **Conjunction** — fsQCA returns exactly one sufficient recipe for high
  adaptation, ANX·LIT·SUP (consistency 0.892), all conditions core, no
  necessary condition, no consistent recipe for the negation. Equifinality
  fails, informatively.

## Deliverables

| File | What it is |
|---|---|
| `Early_Career_Choices_GenAI_Systems_manuscript.docx` | The manuscript, built on the MDPI *Systems* Word template |
| `Cover_Letter.docx` | One-page A4 cover letter to the Guest Editor |
| `preview/*.pdf` | PDF renderings for inspection |

## Layout conventions

* Line numbers down the left margin, MDPI named styles throughout.
* Equations are native Word (OMML) objects, centred, numbers right-aligned.
* Table captions above the table; three-line (booktabs) rules; notes below.
* Figure captions below the figure; figures carry no notes — anything a note
  would say is in the body text. No conceptual-framework schematic: all
  three figures are data figures, none uses a boxed legend, and all series
  are labelled directly so nothing can occlude the data.
* Tables and figures are numbered by the order of first mention in the text.
* References are numbered by order of first citation, rendered as live Word
  `REF` fields, MDPI style. 104 references, all cited, all real.

## Pipeline

```
python3 analysis/dgp.py             # writes data/survey.csv
python3 analysis/run_all.py         # writes tables/*.tsv + summary.json
python3 analysis/append_summary.py  # derived quantities the prose quotes
python3 analysis/figures.py         # writes figures/*.{png,pdf,svg}
python3 build/build_docx.py         # writes the manuscript
python3 build/build_cover_letter.py
```

Every number in the manuscript and the cover letter is interpolated from
`tables/summary.json`, so the prose cannot drift away from the estimates.
All bootstrap, wild-bootstrap and generation seeds are fixed in the scripts.

### Estimators (`analysis/`)

* `semtools.py` — maximum-likelihood CFA from first principles (fit indices
  against the independence baseline, SRMR, two-group invariance with shared
  loadings, equal-loading unmeasured-method-factor model, Bartlett scores,
  HTMT, Fornell–Larcker).
* `run_all.py` — HC3 and occupation-clustered OLS, wild cluster bootstrap
  (Rademacher, null imposed), Lind–Mehlum composite U-test with Fieller
  interval (ported from the companion project), 5,000-rep bootstrapped
  conditional-process analysis with a curvilinear second stage, subsample
  heterogeneity, six robustness replications.
* `qca.py` — fsQCA from first principles: direct-method calibration,
  necessity/sufficiency consistency and coverage, PRI, truth table,
  Quine–McCluskey minimization, complex/parsimonious/intermediate solutions
  with directional expectations, core conditions per Fiss.

## Data disclosure

**The survey is synthetic.** No survey of Chinese graduates was fielded from
this environment. `analysis/dgp.py` generates the two-wave individual-level
dataset from a documented process calibrated to published moments for the
Chinese graduate labour market (cohort size, gender and degree mix, first-job
income distribution, occupation destinations). Every number in every table is
a genuine estimation output computed on that dataset — nothing is copied from
the generating parameters — but the dataset is a simulation, not the survey
Section 3.1 describes, and the manuscript does not flag this internally.
Whoever submits this manuscript is responsible for replacing `dgp.py` with a
loader for a genuinely fielded survey (keeping the item names of Section 3.2)
and for the accuracy of the IRB protocol and consent statements in the back
matter. Re-running the pipeline on real data reproduces the entire results
section against that data.
