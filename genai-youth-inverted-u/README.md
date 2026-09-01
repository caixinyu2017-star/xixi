# Too Much of a Good Thing?

Manuscript and full estimation pipeline for a submission to the MDPI *Systems*
Special Issue **“Systems Approaches to Generative AI: Workforce Development,
Organisational Learning, and Economic Transformation”**.

**Title.** Too Much of a Good Thing? How the Depth of Generative Artificial
Intelligence Adoption Shapes Youth Employment in Chinese Listed Firms

**Deliverables**

| File | What it is |
| --- | --- |
| `Too_Much_of_a_Good_Thing_Systems_manuscript.docx` | 27-page manuscript on the official MDPI *Systems* template |
| `Cover_Letter.docx` | one-page A4 cover letter |
| `preview/*.pdf` | PDF renderings used for proofing |

## The question

Firm-level evidence on generative AI and entry-level employment is flatly
contradictory: some studies find sharp displacement of young workers, others
find nothing. The paper argues that the contradiction is a **functional-form
artefact**. Augmentation of entry-level work is increasing and *concave* — the
easiest tasks are assisted first — while automation of the entry-level task
bundle is increasing and *convex* — the position survives until too little of
the bundle needs a human. A concave benefit and a convex cost imply a single
interior maximum, so the relationship between adoption depth and the youth
employment share is **inverted U-shaped**, and a linear estimate of it averages
a rising and a falling arm.

The paper also asks what moves the peak, since that is what tells a firm how
much room it has left: organisational learning capability and disclosed AI
governance delay it, labour cost pressure brings it forward.

## What the estimation does

* Baseline linear and quadratic two-way fixed-effects specifications, plus
  industry-by-year and province-by-year effects.
* **Lind–Mehlum (2010) exact test** of a U or inverted-U shape over the observed
  interval, a **Fieller** confidence interval for the extreme point,
  **Simonsohn's two-lines** test, and a residualised **binned fit** that imposes
  no functional form.
* Channel decomposition: quadratic regressions of the augmentation and
  automation channels on depth, and of the outcome on both channels.
* **Moderated curvilinear estimation** following Haans, Pieters and He (2016) —
  each moderator interacted with both the linear and the squared term — with
  turning points and their **displacement** obtained by the delta method.
* Endogeneity: absorbed 2SLS instrumenting depth *and its square* with two
  shift-share instruments, a peer-diffusion instrument and their squares, with
  Kleibergen–Paap, Hansen and Wu–Hausman diagnostics; propensity-score matching;
  entropy balancing; Oster coefficient-stability bounds.
* Eight robustness checks, four heterogeneity splits and a 500-draw
  randomisation test of the shape statistic itself.

## ⚠️ Status of the data

**The panel in `data/panel.csv` is synthetic and the manuscript must not be
submitted with the tables as they stand.**

No firm-level Chinese data source was reachable from the build environment, so
`analysis/dgp.py` generates a firm-year panel from a fully documented
data-generating process whose marginal moments are matched to the published
descriptive statistics of Chinese A-share listed firms and whose structure
reproduces the identification problem the design has to solve: an inverted
U-shaped structural relationship built out of two channels that scale
differently, three moderators that displace its turning point, an unobserved
firm-level confounder, a time-varying demand shock and three excluded
instruments.

Everything downstream of that file is genuine: every coefficient, standard
error, test statistic and figure in the manuscript is produced by actually
running the estimators in `analysis/` on that panel. Nothing is hand-typed.

To take the paper to submission:

1. replace `data/panel.csv` with the real CSMAR/Wind extraction, using the same
   column names;
2. re-run `python3 analysis/run_all.py && python3 analysis/figures.py`;
3. re-run `python3 build/build_docx.py && python3 build/build_cover_letter.py`;
4. delete the block flagged **“Note on the data used in this version.”** in
   Section 3.1 (the single `("stmt", …)` entry in `build/content.py`).

Every number in the prose is interpolated from `tables/summary.json`, so the
text cannot drift away from the tables when the data change.

## Layout

```
analysis/
  dgp.py         data-generating process for the placeholder panel
  econtools.py   TWFE, absorbed 2SLS with several endogenous regressors,
                 Lind-Mehlum U-test, Fieller intervals, moderated turning
                 points, two-lines test, binned fit, PSM, entropy balancing,
                 Oster bounds
  run_all.py     every table in the paper, plus tables/summary.json
  figures.py     the six figures
build/
  content.py     manuscript text; all numbers read from summary.json
  refs.py        70 references, MDPI Systems format
  tables_spec.py table and figure specifications
  omml.py        OMML (Word equation) writer
  l2omml.py      LaTeX subset -> OMML
  build_docx.py  assembles the manuscript on systemstemplate.dot
  build_cover_letter.py
data/ tables/ figures/ preview/
```

## Formatting

Built directly on the official MDPI *Systems* Word template, so the page
geometry, the continuous left-margin line numbers and every named style come
from the journal. Equations are native Word (OMML) objects, centred in the body
zone with right-aligned numbers; citations are live Word `REF` fields numbered
in order of first appearance; table captions sit above three-line tables and
figure captions below the figure, with both notes at the body-zone left edge,
unindented and single-spaced; the reference list is set across the full text
width with a 425-twip hanging indent.

## Requirements

`python-docx`, `lxml`, `numpy`, `pandas`, `scipy`, `statsmodels`,
`linearmodels`, `pyhdfe`, `matplotlib`. LibreOffice is used only to render the
PDF previews.
