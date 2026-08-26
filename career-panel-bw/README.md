# Between-person and within-person estimates of career moderations

A secondary analysis of two public longitudinal microdata sets on young
workers, prepared for *Behavioral Sciences* (MDPI).

## The question

Career development theories describe what happens to a person as a career
unfolds. The evidence about the contingencies in those theories is mostly
gathered by comparing people at a moment. That the two can differ has been
argued on theoretical grounds for decades. What has not been established is
how far they actually differ **for interaction terms** — which is where the
interesting theoretical claims live — in real career data, for hypotheses of
the kind the field reports.

Sixteen moderation hypotheses were fixed in advance, each stating that the
wage return to a career input depends on a characteristic of the worker or the
job, and each estimated four ways in two cohorts.

## The data — real, public, and checked

| | source | size |
|---|---|---|
| **NLS Young Women** | U.S. Bureau of Labor Statistics; extract shipped with Stata as `nlswork.dta` and with the R package `sampleSelection` | 28,534 person-years, 4,711 women, 15 waves 1968–1988 |
| **NLSY79 young men** | U.S. Bureau of Labor Statistics; Vella & Verbeek (1998) replication file, shipped with the R packages `wooldridge` and `plm` | 4,360 person-years, 545 men, balanced 1980–1987 |

Nothing in this project is simulated. `analysis/data.py` re-derives, from the
loaded files, the person fixed-effects wage equation Wooldridge reports for the
men's extract (Example 14.4) and matches all three published coefficients to
four decimal places — `expersq` −0.0052, `married` +0.0467, `union` +0.0800.
That is the check that the files were read as intended, and it runs as part of
every full run.

## Estimators

Implemented from first principles in `analysis/estimators.py`, all clustering
on the person:

- **cross-section** — one wave at a time, which is the design most career
  studies use;
- **pooled** — all waves stacked;
- **within** — person fixed effects, by the within transformation;
- **hybrid** — Mundlak's device: each time-varying term enters twice, as the
  deviation from the person's own mean and as that mean, so the within-person
  and between-person slopes are estimated jointly and their difference tested
  inside one model.

The self-test recovers known between- and within-person slopes from synthetic
data, shows pooled OLS biased under sorting while the within estimator is not,
and checks that clustered standard errors exceed naive ones.

## What it found

- The between-person and within-person estimates **carried opposite signs in
  8 of 16** hypotheses and supported **different substantive conclusions in
  12**; their equality was **rejected in 6** after controlling the false
  discovery rate.
- The median disagreement was **1.42 times the size of the within-person
  estimate itself** — the gap between the two answers was typically larger
  than the answer.
- Of **160 single-wave estimates**, 26 reached significance and **6 of those
  (23%) pointed the opposite way** to the within-person estimate of the same
  quantity. Single-wave estimates scatter around the *between-person* value,
  so another cross-section reproduces the same quantity rather than closing
  the gap.
- The within-person estimate **kept its sign under all three robustness
  variations in 14 of 16** hypotheses, so the divergence is not an artefact of
  the transformation used to remove the person.
- Worked case (W1), employer tenure × college graduate: between-person
  −0.013 (p < .001), within-person +0.004 (p = .087), difference 0.017
  (t = 4.12, p < .001, q < .001). Read across people, graduates gain markedly
  less from tenure; read within people, slightly more.

Neither estimator is presented as correct. They answer different questions,
and the paper says so throughout.

## Layout

```
data/           the two extracts as downloaded
analysis/       data.py  estimators.py  grid.py  run.py  figures.py
tables/         t1–t7 TSVs and summary.json
figures/        three figures, none carrying a note
build/          content.py  tables_spec.py  bibliography.py  refs.py
                build_docx.py  build_cover_letter.py  behavscitemplate.dot
```

## Reproducing

```
python3 analysis/data.py          # loads both panels, reproduces the benchmark
python3 analysis/estimators.py    # estimator self-test
python3 analysis/run.py           # ~35 s; writes tables/
python3 analysis/figures.py       # writes figures/
python3 build/build_docx.py       # the manuscript
python3 build/build_cover_letter.py
```

## Notes on interpretation

Both cohorts were surveyed between 1968 and 1988, so the specific interactions
are not current estimates of anything. The claim is about how two estimators
behave on the same panel, which does not depend on the period; these two
cohorts were chosen because they are among the few career panels with many
waves that are public, documented and redistributable, so the analysis can be
checked. Four of the sixteen hypotheses concern the return to experience in
the balanced men's panel, where experience and calendar time coincide within a
person; those within-person estimates absorb the wage trend of the 1980s and
are flagged in the manuscript.

## References

`build/bibliography.py` holds 27 entries. Each author list, year, title and
journal was checked against a retrieved record; volume and page ranges that
could not be confirmed are omitted rather than guessed at.
