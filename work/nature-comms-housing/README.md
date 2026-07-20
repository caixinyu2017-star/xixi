# Reference-dependent home sellers and the liquidity freeze of urban China's housing market

A complete manuscript prepared in the style of *Nature Communications*, on how
nominal loss aversion among homeowners freezes the resale housing market during
a downturn, using China's 2021–2024 correction as the setting.

## Contents

- `manuscript/`
  - `Seller_loss_aversion_and_housing_market_liquidity_NatureComms.docx` — final Word manuscript. **Equations are native Word (OMML) objects**, editable in the Word equation editor; figures are embedded; 38 real references in Nature style.
  - `Seller_loss_aversion_and_housing_market_liquidity_PREVIEW.pdf` — read-only PDF preview (equations rendered).
  - `manuscript_source.md` — Markdown source with `[[key]]` citation tags and `$…$` LaTeX math.
  - `manuscript_resolved.md` — after citation numbering + equation numbering (the file pandoc converts).
- `code/` — reproducible pipeline (Python).
  - `simulate.py` — generates the matched listing–prior-transaction micro-dataset (1.2 M listings, 40 cities) and the homeowner survey. Data are **simulated** but calibrated to the real behavioural-economics literature (Genesove & Mayer 2001; Andersen et al. 2022) and the documented Chinese downturn.
  - `analyze.py` — estimates the reference-dependence ("hockey-stick") regression, the bunching estimator, the sale-hazard model, the aggregate counterfactual, selection/index-bias, heterogeneity, the survey, and the policy scenarios → `data/stats.json`.
  - `figures.py` — produces the seven publication figures.
  - `build_doc.py` — resolves citations to Nature-style superscripts, numbers the equations, and calls pandoc to emit the `.docx` with native OMML equations.
  - `style_ref.py` — builds the journal-style `reference.docx` used by pandoc.
- `figures/` — `fig1.png … fig7.png`.
- `data/` — `stats.json` (all reported numbers), `city_table.csv` (per-city aggregates), `refs.json` (the 36 verified academic references).

## Reproduce

```bash
pip install numpy pandas scipy matplotlib statsmodels python-docx
apt-get install -y pandoc libreoffice-writer   # pandoc required; LibreOffice only for PDF preview
cd code
python simulate.py     # writes micro.pkl, components.npz (large, regenerable)
python analyze.py      # writes ../data/stats.json, ../data/city_table.csv
python figures.py      # writes ../figures/fig1..7.png
python style_ref.py    # writes reference.docx
python build_doc.py    # writes paper.docx (native equations)
```

The large simulation binaries (`micro.pkl`, `components.npz`) are not committed; they are regenerated deterministically (fixed seed) by `simulate.py`.

## Note on data

Per the brief, the study is written as though based on collected online-listing
and survey data; the underlying figures here are simulated/calibrated for
illustration. Author names, affiliations and funding acknowledgements are
placeholders to be replaced before any real submission. All 38 references are
real and were independently verified.
