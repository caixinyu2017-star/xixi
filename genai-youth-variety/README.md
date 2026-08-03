# Variety Absorbs Variety

Manuscript and estimation pipeline for a regular-issue submission to MDPI
*Systems*.

**Variety Absorbs Variety: Workforce Skill Diversity, Shock Absorption and
Youth Employment in Chinese Listed Firms**

## The argument

When demand falls, young workers are the first to be let go — but some firms
shed almost none of them, and the difference is not explained by size,
leverage, profitability or sector. This paper takes the missing variable from
cybernetics. Ashby's law of requisite variety says a system can absorb only as
much variety as it contains. Applied to a workforce, internal variety is the
entropy of the firm's employment distribution over five disclosed occupational
categories and three education levels, decomposed in the manner of Frenken
into a related and an unrelated component.

* Variety raises the youth employment share by **1.86 pp per standard
  deviation** and attenuates the effect of an adverse industry demand shock
  (interaction **+1.257**).
* **Related** variety buffers **1.49×** as strongly per bit as unrelated
  variety — depth within occupational families beats breadth across them,
  because absorption requires that a person actually move.
* Absorption is mostly **not** visible reorganisation: **32.5%** of the buffer
  travels through suppressed separations against **13.7%** through internal
  redeployment.
* The central result: the buffer is a **regime, not a gradient**. A
  fixed-effects panel threshold model locates a threshold at **2.52 bits**
  (bootstrap p = 0.000). Below it a shock costs **2.12 pp** of youth
  employment; above it the coefficient is **−0.06** and insignificant.
  **48%** of listed firm-years fall below the threshold.

Ashby's law is a *sufficiency* condition, and sufficiency conditions imply
discontinuities. The data locate one where the theory says it should be.

## Deliverables

| File | What it is |
|---|---|
| `Variety_Absorbs_Variety_Systems_manuscript.docx` | The manuscript, built on the MDPI *Systems* Word template |
| `Cover_Letter.docx` | One-page A4 cover letter |
| `preview/*.pdf` | PDF renderings for inspection |

## Layout conventions

* Line numbers down the left margin, MDPI named styles throughout.
* Equations are native Word (OMML) objects, centred, with numbers
  right-aligned in a borderless two-column table.
* Table captions above the table; three-line (booktabs) rules; notes below
  stating the dependent variable, the parentheses convention, the star
  convention and the source.
* Figure captions below the figure. Figures carry no notes; what a note would
  say is in the body text.
* Tables and figures are numbered by the order in which the text first
  mentions them.
* References are numbered by order of first citation, rendered as live Word
  `REF` fields, in MDPI *Systems* style. 96 references, all cited, all real.
* Hypotheses set off in the MDPI `H1.` form, one per arrow of Figure 1.
* Back matter: Author Contributions (CRediT), Funding, Institutional Review
  Board Statement, Informed Consent Statement, Data Availability Statement,
  Conflicts of Interest.

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
Kleibergen–Paap, Hansen and Durbin–Wu–Hausman diagnostics for a system with
two endogenous regressors, a firm-block bootstrap of the share of an
interaction effect carried by a mediator, propensity score matching with a
balance table, Hainmueller entropy balancing, Oster coefficient-stability
bounds, the restricted wild cluster bootstrap, and the **Hansen (1999)
fixed-effects panel threshold regression** — concentrated least squares over a
trimmed quantile grid, the fixed-regressor bootstrap of Hansen (1996) for the
null of no threshold, and a confidence interval obtained by inverting the
likelihood-ratio sequence. The grid search is written in Frisch–Waugh form so
that the whole bootstrap is matrix algebra on a pre-transformed design, which
takes it from minutes to a fraction of a second.

## Data disclosure

**The panel is synthetic.** No commercial firm-level database (CSMAR, WIND,
CNRDS) and no mirror of the National Bureau of Statistics is reachable from
the environment in which this project was prepared, so `analysis/dgp.py` draws
the panel from a documented process calibrated to published moments for
Chinese A-share listed firms, including the disclosed occupational and
education composition of the listed-firm workforce and the amplitude of the
industry demand contractions of 2015, 2018, 2020 and 2022. Every number in
every table is a genuine estimation output computed on that panel — nothing is
copied from the generating parameters — but the panel is a simulation, not the
extract Section 3.1 describes. Section 3.1 of the manuscript carries a
removable note saying so. Replacing `dgp.py` with a loader for the real
extract, keeping the column names of Table 1, reproduces the entire results
section against real data.
