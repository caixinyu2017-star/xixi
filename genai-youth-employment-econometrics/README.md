# The Narrowing Entry Port

Manuscript and full estimation pipeline for a submission to the MDPI *Systems*
Special Issue **“Systems Approaches to Generative AI: Workforce Development,
Organisational Learning, and Economic Transformation”**.

**Title.** The Narrowing Entry Port: Generative Artificial Intelligence
Adoption, Task Routinisation and Youth Employment in Chinese Listed Firms

**Deliverables**

| File | What it is |
| --- | --- |
| `Narrowing_Entry_Port_Systems_manuscript.docx` | 25-page manuscript on the official MDPI *Systems* template |
| `Cover_Letter.docx` | one-page A4 cover letter |
| `preview/*.pdf` | PDF renderings used for proofing |

## ⚠️ Status of the data

**The panel in `data/panel.csv` is synthetic and the manuscript must not be
submitted with the tables as they stand.**

No firm-level Chinese data source was reachable from the build environment, so
`analysis/dgp.py` generates a firm-year panel from a fully documented
data-generating process whose marginal moments are matched to the published
descriptive statistics of Chinese A-share listed firms and whose structure
reproduces the identification problem the design has to solve — an unobserved
firm-level confounder that raises both adoption and the youth share, a
time-varying demand shock, two mediators, two moderators and two excluded
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
   Section 3.1 (it is the single `("stmt", …)` entry in `build/content.py`).

Every number in the prose is interpolated from `tables/summary.json`, so the
text cannot drift away from the tables when the data change.

## Research design

* **Outcome** `Youth` — share of employees aged 30 or below (%), from the
  employee-structure disclosure of annual reports.
* **Treatment** `GenAI` — text-based adoption intensity from the management
  discussion and analysis section; zero before 2023, so the two-way
  fixed-effects specification is a continuous difference-in-differences design
  around the public release of large language models.
* **Mechanisms** task routinisation (`RTI`) and human-capital upgrading (`HCU`),
  estimated in stepwise form with a firm-block bootstrap.
* **Moderators** organisational learning capability (`OLC`) and AI governance
  disclosure (`AIGov`).
* **Identification** event study on ex-ante task exposure; absorbed 2SLS with a
  shift-share instrument (1984 provincial telephone penetration × the national
  generative-AI diffusion index) and a leave-one-out peer-diffusion instrument;
  propensity-score matching; entropy balancing; Oster coefficient-stability
  bounds; a 500-draw randomisation placebo.

## Layout

```
analysis/
  dgp.py         data-generating process for the placeholder panel
  econtools.py   TWFE, absorbed 2SLS, bootstrap mediation, PSM,
                 entropy balancing, Oster bounds, coefficient equality
  run_all.py     every table in the paper, plus tables/summary.json
  figures.py     the six figures
build/
  content.py     manuscript text; all numbers read from summary.json
  refs.py        69 references, MDPI Systems format
  tables_spec.py table and figure specifications
  omml.py        OMML (Word equation) writer
  l2omml.py      LaTeX subset -> OMML
  build_docx.py  assembles the manuscript on systemstemplate.dot
  build_cover_letter.py
data/ tables/ figures/ preview/
```

## Formatting notes

The manuscript is built directly on the official MDPI *Systems* Word template,
so the page geometry, the continuous left-margin line numbers and every named
style come from the journal. Beyond that:

* equations are **native Word (OMML) objects**, centred in the body zone with
  right-aligned numbers in the template's two-column layout;
* citations are live Word `REF` fields pointing at bookmarks on the reference
  list, numbered in order of first appearance;
* table captions sit above three-line (booktabs) tables, figure captions below
  the figure, and both notes sit at the body-zone left edge with no indent and
  single line spacing;
* references are set across the full text width with a 425-twip hanging indent,
  matching the published articles rather than the body zone.

## Requirements

`python-docx`, `lxml`, `numpy`, `pandas`, `scipy`, `statsmodels`,
`linearmodels`, `pyhdfe`, `matplotlib`. LibreOffice is used only to render the
PDF previews.
