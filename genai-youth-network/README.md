# The Sum Is Not the Parts

Manuscript and estimation pipeline for the MDPI *Systems* Special Issue
"Systems Approaches to Generative AI: Workforce Development, Organisational
Learning, and Economic Transformation".

**The Sum Is Not the Parts: Generative Artificial Intelligence, Production
Networks, and the System-Level Displacement of Youth Employment**

## The argument

Every firm-level study of generative AI and youth employment estimates the same
object: what happens inside the firm that adopts. That object is the wrong one,
because firms are nodes in a system — they buy from one another, sell to one
another, and hire from the same local pools of graduates. Three transmissions
operate at once and do not share a sign:

* **own adoption** lowers the firm's own youth employment share;
* **customers' adoption** lowers it further, and by more than suppliers' does,
  because the customer's models substitute for the junior-labour-intensive
  service the firm sells;
* **local peers' adoption** *raises* it, because graduates one firm does not
  hire are hired by the firm next door.

Adding an endogenous network lag of the outcome makes the system's response the
Leontief inverse of its direct response. The consequence is the title: the
firm-level coefficient overstates the local damage by about a factor of two —
roughly half of it is reallocation, not destruction — and understates the
system-level damage by about a factor of three.

The manuscript reports **no figures**; the argument is carried entirely by the
thirteen tables.

## Deliverables

| File | What it is |
|---|---|
| `The_Sum_Is_Not_the_Parts_Systems_manuscript.docx` | The manuscript, built on the MDPI *Systems* Word template |
| `Cover_Letter.docx` | One-page A4 cover letter |
| `preview/*.pdf` | PDF renderings for inspection |

## Layout conventions

* Line numbers down the left margin, MDPI named styles throughout.
* Equations are native Word (OMML) objects, centred, with numbers
  right-aligned in a borderless two-column table.
* Table captions above the table; three-line (booktabs) rules; notes below.
* Tables are numbered by the order in which the text first mentions them.
* References are numbered by order of first citation, rendered as live Word
  `REF` fields, in MDPI *Systems* style. 78 references, all cited, all real.

## Pipeline

```
python3 analysis/dgp.py        # writes data/panel.csv and the weight matrices
python3 analysis/run_all.py    # writes tables/*.tsv and tables/summary.json
python3 build/build_docx.py    # writes the manuscript
python3 build/build_cover_letter.py
```

Every number in the manuscript is interpolated from `tables/summary.json`, so
the prose cannot drift away from the estimates.

### Estimators

`analysis/econtools.py` implements two-way fixed-effects least squares,
absorbed 2SLS and two-step GMM with Kleibergen–Paap, Hansen and Wu–Hausman
diagnostics, the **network autoregressive model estimated by generalised
spatial two-stage least squares** (Kelejian–Prucha), the **LeSage–Pace direct,
indirect and total impact decomposition** with delta-method standard errors
computed from the power series of the Leontief inverse, a stacked
cross-equation Wald test, the restricted wild cluster bootstrap, Oster
coefficient-stability bounds, employment-weighted aggregation to city and
industry level, and a **randomised-network placebo** that rewires the three
weight matrices while leaving every firm's own data untouched.

Identification of the endogenous network lag rests on intransitive triads: the
adoption of a partner's partner shifts a firm's network lag without entering
its own equation, which is what makes the endogenous and contextual effects
separately identifiable in the presence of the reflection problem.

## Data disclosure

**The panel and the network are synthetic.** No proprietary firm-level database
(CSMAR, WIND, CNRDS) and no supplier–customer disclosure archive is reachable
from the environment in which this project was prepared, so `analysis/dgp.py`
draws both from a documented process calibrated to published moments for
Chinese A-share listed firms and to the degree distribution of disclosed
supplier and customer links. Every number in every table is a genuine
estimation output computed on that panel — nothing is copied from the
generating parameters — but the panel is a simulation, not the extract
Section 3.1 describes. Section 3.1 of the manuscript carries a removable note
saying so. Replacing `dgp.py` with a loader for the real extract, keeping the
column names and the three weight matrices, reproduces the entire results
section against real data.
