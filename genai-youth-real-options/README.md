# Options on Youth

Manuscript and estimation pipeline for the MDPI *Systems* Special Issue
"Systems Approaches to Generative AI: Workforce Development, Organisational
Learning, and Economic Transformation".

**Options on Youth: Generative Artificial Intelligence Uncertainty and the
Contingent Turn in Entry-Level Hiring**

## The argument

Hiring a school leaver is a partly irreversible investment: the firm sinks a
firm-specific training cost it cannot recover if the generative-AI frontier
moves against the task bundle it hired for. The theory of investment under
uncertainty then implies a hurdle above the Marshallian one, widening with the
volatility of the frontier. The paper measures firm-level generative-AI
*uncertainty* separately from the *level* of adoption and from general economic
policy uncertainty, and finds five patterns that only an option-value account
produces jointly: a chill driven by dispersion rather than level; concentration
on the margin with the largest sunk component; scaling with irreversibility and
attenuation by reversibility; a compositional shift towards revocable contracts;
and a zone of inaction with hysteresis.

The manuscript reports **no figures** — the argument is carried entirely by the
thirteen tables.

## Deliverables

| File | What it is |
|---|---|
| `Options_on_Youth_Systems_manuscript.docx` | The manuscript, built on the MDPI *Systems* Word template |
| `Cover_Letter.docx` | One-page A4 cover letter |
| `preview/*.pdf` | PDF renderings for inspection |

## Layout conventions

* Line numbers down the left margin, MDPI named styles throughout.
* Equations are native Word (OMML) objects, centred, with numbers
  right-aligned in a borderless two-column table.
* Table captions above the table; three-line (booktabs) rules; notes below.
* Tables are numbered by the order in which the text first mentions them.
* References are numbered by order of first citation, rendered as live Word
  `REF` fields, in MDPI *Systems* style. 86 references, all cited, all real.

## Pipeline

```
python3 analysis/dgp.py        # writes data/panel.csv
python3 analysis/run_all.py    # writes tables/*.tsv and tables/summary.json
python3 build/build_docx.py    # writes the manuscript
python3 build/build_cover_letter.py
```

Every number in the manuscript is interpolated from `tables/summary.json`, so
the prose cannot drift away from the estimates.

### Estimators

`analysis/econtools.py` implements two-way fixed-effects least squares,
Poisson pseudo-maximum likelihood with two absorbed effect dimensions
(the `ppmlhdfe` algorithm of Correia, Guimarães and Zylkin), absorbed 2SLS and
two-step GMM with Kleibergen–Paap, Hansen and Wu–Hausman diagnostics, a stacked
cross-equation Wald test, the restricted wild cluster bootstrap, dynamic
difference in differences with a joint pre-trend test, randomisation inference
and Oster coefficient-stability bounds.

## Data disclosure

**The panel is synthetic.** No proprietary firm-level database (CSMAR, WIND,
CNRDS, or a commercial online-recruitment archive) is reachable from the
environment in which this project was prepared, so `analysis/dgp.py` draws the
panel from a documented process calibrated to published moments for Chinese
A-share listed firms. Every number in every table is a genuine estimation
output computed on that panel — nothing is copied from the generating
parameters — but the panel is a simulation, not the extract Section 3.1
describes. Section 3.1 of the manuscript carries a removable note saying so.
Replacing `dgp.py` with a loader for the real extract, keeping the column
names, reproduces the entire results section against real data.
