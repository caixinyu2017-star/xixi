# The Vanishing First Rung?

Manuscript prepared for the MDPI journal **Systems**, Special Issue *"Systems
Approaches to Generative AI: Workforce Development, Organisational Learning, and
Economic Transformation"* (Guest Editor: Dr. Ali Ahsan; deadline 30 April 2027).

**Title.** The Vanishing First Rung? Generative AI, Organisational Learning and
Youth Entry Employment in a Socio-Technical System Dynamics Model

## Deliverables

| File | Description |
| --- | --- |
| `Vanishing_First_Rung_Systems_manuscript.docx` | The manuscript, built on the official MDPI *Systems* Word template (26 pages) |
| `Cover_Letter.docx` | One-page A4 cover letter |
| `preview/…pdf` | Rendered previews of both documents |

The manuscript uses the journal's own template, so it carries the MDPI page
geometry, the continuous left-hand line numbers and every named MDPI style.
All 20 display equations are native Word equation-editor (OMML) objects,
centred, with right-aligned numbers in the two-column layout the template
prescribes. Tables are three-line (booktabs) with the caption above and the note
below; figures carry the caption below the image and the note below the caption,
unindented and single-spaced. Citations are live Word `REF` fields pointing at
bookmarks on the reference list, and the 62 references are numbered in order of
first appearance, formatted in MDPI *Systems* style.

## The paper in one paragraph

Generative AI is diffusing fastest through the codified, routine-cognitive tasks
that form the entry port of a professional career, and early evidence shows
employment of 22–25 year-olds in exposed occupations falling while employment of
their experienced colleagues does not. The paper argues that this is a system
outcome rather than a technological verdict: the entry port is simultaneously a
factor of production and the intake stage of the firm's own capability pipeline.
A six-stock socio-technical system dynamics model — early-career staff,
experienced staff, GenAI capability, human–AI collaboration routines, planned
output and perceived unit cost — is formulated, calibrated to four independent
published benchmarks, validated against the standard battery of system dynamics
tests, and analysed over a two-dimensional design space.

Headline results (all produced by the code in `model/`):

* Baseline: entry employment −15.0% by year 3, trough −37.2% in year 7, −30.7%
  after 25 years; output fulfilment ratio settles at 0.86.
* The sign is a design variable: the 25-year effect ranges from −70.0% to
  +19.2% and is positive in 17.1% of the design space.
* Joint optimisation is measurable: work redesign × learning investment
  interact by +2.74 percentage points in a pre-specified 2 × 2 factorial.
* Automation-first is a capability trap: fastest early cost reduction, yet
  output 15.7% *below* the no-GenAI counterfactual after 25 years.

## Repository layout

```
model/      sdmodel.py      the system dynamics model (6 stocks, RK4)
            calibrate.py    nonlinear least squares against four benchmarks
            experiments.py  baseline, validation, regimes, policies, closure, PRCC
            figures.py      all seven figures
build/      refs.py         the 62-item reference database (MDPI format)
            content.py      the manuscript text (with $latex$ and [[cite]] markup)
            tables_spec.py  the nine tables, read from the simulation output
            omml.py         OMML (Word equation) element builders
            l2omml.py       LaTeX-subset -> OMML converter
            build_docx.py   assembles the manuscript on the MDPI template
            build_cover_letter.py
tables/     simulation output (TSV + npz + summary.json)
figures/    figure1 … figure7 (PNG, 400 dpi)
```

## Reproducing

```bash
cd model
python3 calibrate.py       # re-estimates the four diffusion/augmentation parameters
python3 experiments.py     # writes every table to ../tables (about 4 min)
python3 figures.py         # writes every figure to ../figures
cd ../build
python3 build_docx.py          # -> ../Vanishing_First_Rung_Systems_manuscript.docx
python3 build_cover_letter.py  # -> ../Cover_Letter.docx
```

Requirements: `python-docx`, `numpy`, `scipy`, `matplotlib`.

## Before submitting

The author block on the title page and in the back matter carries the template
placeholders; fill in the author name, affiliation, ORCID and corresponding
address. The editorial metadata block (Academic Editor, Received/Revised/
Accepted/Published, Citation) is completed by the editorial office.
