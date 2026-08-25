# Workplace-weighted green infrastructure siting and young workers' heat exposure

Prepared for *Sustainability* (MDPI), Special Issue *Thermal Mitigation Effects
of Green and Blue Infrastructure and Urban Sustainability from an
Interdisciplinary Perspective*.

## What this study is

A model-based assessment, not an observational one. It asks where a city should
place tree canopy if the objective is to protect young workers from heat, given
that planting is in practice sited by residential amenity and deprivation while
heat-exposed entry-level work is not located where people live.

## What the data are — read this first

There is no survey and no observational panel here. The city is a transparent
synthetic urban form; the climate settings are declared modelling inputs, not
measurements of named places. Every number in the manuscript is produced by
running the code in `analysis/`, under a fixed seed.

What IS taken from the published literature, and cited as such:

* five exposure-response functions mapping WBGT to physical work capacity
  (Hothaps, ISO 7243, NIOSH, Dunne et al., Foster et al.), transcribed from
  open-source reference implementations and cross-checked against each other
* green and blue infrastructure cooling magnitudes and decay distances
* the ratio of workplace-accident incidence between workers aged 18-24 and
  25-54 in the European Union

`analysis/params.py` is the registry of every parameter the model uses. Each
carries a provenance label — `literature`, `derived` or `assumed` — and the
manuscript reports the counts and prints the whole registry as an appendix
table. Assumed parameters are swept in the uncertainty analysis rather than
defended.

## Headline results

* Weighting a planting budget by exposed workplaces rather than by residents
  protects 3.05 times as many hours of young workers' work capacity, against
  a control rule that targets the same heat but counts residents.
* That advantage is conditional: absent where workplaces and homes coincide,
  5.6-fold where they are opposed, crossing into materiality once the
  workplace-residence correlation falls below about 0.25.
* The magnitude of the loss is NOT identified. Across 4000 draws the estimate
  varies by more than an order of magnitude and is exactly zero in 6.7% of
  draws, because the five published response functions disagree about whether
  European summer conditions cause any loss at all.

## Deliverables

* `Workplace_Weighted_Green_Infrastructure_Young_Workers_Sustainability_manuscript.docx`
* `Cover_Letter.docx`

## Pipeline

```
cd heat-youth-work/analysis
python3 thermal.py        # self-test of the five response functions
python3 city.py           # self-test of the synthetic city
python3 microclimate.py   # self-test of the heat field
python3 labour.py         # self-test of the lost-hours aggregation
python3 siting.py         # self-test of the allocation rules
python3 uncertainty.py    # self-test of the ensemble
python3 run_all.py        # the study: writes ../tables/*.tsv and summary.json
cd ../build
python3 build_docx.py         # the manuscript
python3 build_cover_letter.py # the cover letter
```

Every module runs its own self-test when executed directly. `run_all.py` takes
about two and a half minutes on one core.
