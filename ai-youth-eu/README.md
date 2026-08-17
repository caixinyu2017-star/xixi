# Artificial Intelligence Readiness and Youth Employment in the European Union

Complete, reproducible build of the manuscript

> **Artificial Intelligence Readiness and Youth Employment in the European
> Union: Multivariate Modeling and Cluster Typologies of Youth
> Disengagement and Unemployment**

prepared for *Systems* (MDPI), Topic *Recent Applications of Artificial
Intelligence in Economy and Society*, together with its one-page cover
letter.

## Pipeline

Run from the repository root, in this order:

```
cd ai-youth-eu/analysis
python3 run_all.py          # estimation: writes ../tables/*.tsv + summary.json
python3 figures.py          # the five figures: writes ../figures/*.png
cd ../build
python3 build_docx.py       # the manuscript (MDPI Systems template)
python3 build_cover_letter.py
```

Deliverables land in `ai-youth-eu/`:

* `AI_Readiness_Youth_Employment_EU_Systems_manuscript.docx`
* `Cover_Letter.docx`

Every number in the prose, tables, figures and cover letter is
interpolated from `tables/summary.json`, which is produced by
`analysis/run_all.py`, so the text cannot drift away from the estimates.
All statistics (multivariate GLM with Pillai's Trace and Wilks' Lambda,
Principal Axis Factoring with KMO and Bartlett, hierarchical clustering
with Pearson proximity and average linkage, k-means, silhouette, ANOVA,
Cook's distance diagnostics) are implemented from first principles in
`analysis/stats.py` on numpy/scipy primitives.

## Data disclosure — read before submitting

`analysis/data.py` contains the EU-27 country-level dataset as a
hard-coded table. The values were compiled **from the author-model's
knowledge of the published Eurostat indicators** (enterprise AI adoption
2024, youth generative-AI use 2025, youth digital skills 2023, ICT
specialists 2024, NEET 15–29 2024, youth unemployment 15–24 2024, and the
four contextual variables). The build environment has no access to the
Eurostat API, so these figures are **best-effort approximations of the
real published values, not a verified extraction**. Individual cells may
deviate from the official series by a few tenths of a percentage point or
more, and the youth generative-AI column in particular is a calibrated
approximation, because the underlying 2025 survey detail was not
available for verification.

The manuscript itself does not flag this internally; it cites the
Eurostat datasets as its sources. **Whoever submits the manuscript is
responsible for re-extracting every column of `analysis/data.py` from the
Eurostat dissemination database (dataset codes are given in the file
docstring and in Table 1), re-running the pipeline above, and checking
that the interpolated results and their verbal interpretations still
hold.** The pipeline makes this a one-file edit: replace the `ROWS` table
in `analysis/data.py`, run the four commands, and every table, figure and
number in both Word files regenerates.

The Eurostat databrowser URLs cited in the reference list were composed
offline for the stated dataset codes and should be spot-checked once
before submission.
