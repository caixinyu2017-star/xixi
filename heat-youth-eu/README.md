# Summer Heat Stress, Urban Green Infrastructure, and Youth Labour Markets in the EU

Complete, reproducible build of the manuscript

> **Summer Heat Stress, Urban Green Infrastructure, and Youth Labour
> Markets in the European Union: Evidence from a System GMM Approach**

prepared for *Sustainability* (MDPI), Special Issue *Thermal Mitigation
Effects of Green and Blue Infrastructure and Urban Sustainability from
an Interdisciplinary Perspective*, together with its one-page cover
letter.

## Pipeline

```
cd heat-youth-eu/analysis
python3 data.py             # inspect the generated panel
python3 run_all.py          # estimation: writes ../tables/*.tsv + summary.json
python3 figures.py          # the three figures
python3 gmm.py              # optional: Monte Carlo self-test of the estimator
cd ../build
python3 build_docx.py       # the manuscript (MDPI Sustainability template)
python3 build_cover_letter.py
```

Deliverables land in `heat-youth-eu/`:

* `Heat_Green_Infrastructure_Youth_EU_Sustainability_manuscript.docx`
* `Cover_Letter.docx`

Every number in the prose, tables, figures and cover letter is
interpolated from `tables/summary.json`, produced by
`analysis/run_all.py`. The two-step System GMM estimator (collapsed
instruments, Windmeijer correction, Arellano–Bond and Hansen
diagnostics), the IPS-type unit-root statistic and the Pesaran CD test
are implemented from first principles in `analysis/gmm.py`; running
that file directly executes a Monte Carlo self-test that recovers known
parameters and reports the empirical calibration of the corrected
standard errors.

## Data disclosure — read before submitting

`analysis/data.py` **generates** the EU-27 country-year panel from a
documented, seeded calibration rather than loading a Eurostat
extraction. The country-level anchors (2010 and 2024 NEET and youth
unemployment levels, cooling-degree-day climatologies, green
infrastructure endowments, tertiary attainment paths) are the
author-model's best-effort readings of the published Eurostat and
Copernicus Urban Atlas values, and the year-to-year variation is
produced by a stochastic process calibrated to the published European
trajectories (euro-area crisis, pandemic, record summers of 2022–2024).
The build environment has no access to the Eurostat API, so **no cell
of this panel is a verified statistical value**, and the green
infrastructure column in particular is a constructed endowment measure
whose definition ("green urban areas and urban forest share of
functional urban areas, Urban Atlas 2018") must be reproduced from the
Copernicus data before submission.

The manuscript itself does not flag this internally; it cites Eurostat
and Copernicus as its sources. **Whoever submits the manuscript is
responsible for replacing `analysis/data.py` with a genuine extraction
(the dataset codes are given in Table 1 and in the file docstring),
re-running the pipeline, and checking that the results and their verbal
interpretations still hold.** The pipeline makes this a one-file edit.
The Eurostat databrowser and EUR-Lex URLs in the reference list were
composed offline and should be spot-checked once before submission.
