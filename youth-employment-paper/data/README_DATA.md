# Data package — *Artificial Intelligence Adoption and Youth Employment*

This package contains the data underlying the manuscript **"Artificial Intelligence Adoption and
Youth Employment: A Socio-Technical Systems Perspective on Business Model Innovation and
Entrepreneurial Governance."**

## ⚠️ Important — please read first (data status / honesty note)

- The manuscript's **regression tables report illustrative, internally consistent estimates** that
  instantiate the empirical design. They were **not** produced by estimating models on a real
  licensed firm micro-panel.
- The data sources described in the paper — **CSMAR** (firm financials, employees, governance),
  **Huazheng / SynTao Green Finance** (ESG), **IFR** (industrial robots), and the **China City
  Statistical Yearbook** (city GDP) — are **commercial/licensed** databases that were not accessed
  to generate these files.
- Therefore this package provides: (1) **all tabulated data that actually appears in the
  manuscript** (every table + the figure data), fully machine-readable; and (2) a **clearly
  labelled SYNTHETIC firm-level panel** you can use to test the estimation pipeline.
- **Before submission**, replace the illustrative estimates with results from your own estimation
  on the genuine licensed source data.

## Contents

### A. Manuscript tables (the real "data behind the paper")
| File | Manuscript object |
| --- | --- |
| `table1_descriptive_statistics.csv` | Table 1 — descriptive statistics |
| `table2_correlation_matrix.csv` | Table 2 — correlation matrix |
| `table3_baseline_regression.csv` | Table 3 — baseline regressions |
| `table4_robustness_checks.csv` | Table 4 — robustness (alt. measures, samples, clustering) |
| `table5_propensity_score_matching.csv` | Table 5 — PSM |
| `table6_instrumental_variable.csv` | Table 6 — 2SLS / IV |
| `table7_mechanism_analysis.csv` | Table 7 — mediation (BMI, SKILL) |
| `table8_moderation_governance.csv` | Table 8 — moderation (DEO, ESG, GOV) |
| `table9_heterogeneity.csv` | Table 9 — heterogeneity |
| `tableA1_variable_definitions.csv` | Table A1 — variable definitions (data dictionary) |
| `tableA2_vif.csv` | Table A2 — variance inflation factors |
| `figure2_psm_covariate_balance.csv` | Figure 2 — standardized mean differences (pre/post match) |
| `AI_Youth_Employment_tables.xlsx` | All of the above, one sheet per table |

In the regression CSVs, each estimate cell is formatted as `coefficient (standard error)` with
significance stars (`*`, `**`, `***` = 10%, 5%, 1%).

### B. References
| File | Contents |
| --- | --- |
| `references.csv` | The 57 references (no., authors, title, journal, year, vol, issue, pages, DOI) |
| `references.bib` | The same references as BibTeX |

### C. Synthetic panel (for pipeline testing only — NOT real data)
| File | Contents |
| --- | --- |
| `SYNTHETIC_firm_panel_2011_2023.csv` | A simulated firm-year panel (28,974 obs.) |
| `make_synthetic_panel.py` | The generator script (fixed seed, reproducible) |

The synthetic panel is calibrated to the **descriptive statistics in Table 1** (variable means,
standard deviations, and ranges) and embeds the **hypothesized signs** (AI, BMI and SKILL raise
YEMP), so you can run the baseline / mediation / moderation code end-to-end. It will **not**
reproduce the exact coefficients in the manuscript tables, and **must not** be used as real data
for submission.

Columns: `firm_id, year, YEMP, AI, L_AI, BMI, SKILL, DEO, ESG, GOV, Age, Size, Lev, RoA, Cash,
Growth, Top10, Board, Separation, SOE, lngdp` (see `tableA1_variable_definitions.csv` for
definitions). `L_AI` is the one-year lag of `AI` within firm; it is empty for each firm's first year.

## Example (Python) — run the baseline on the synthetic panel
```python
import pandas as pd, statsmodels.formula.api as smf
df = pd.read_csv("SYNTHETIC_firm_panel_2011_2023.csv")
m = smf.ols("YEMP ~ L_AI + Age + Size + Lev + RoA + Top10 + SOE + lngdp + C(firm_id) + C(year)",
            data=df.dropna(subset=["L_AI"])).fit(cov_type="cluster",
            cov_kwds={"groups": df.dropna(subset=["L_AI"])["firm_id"]})
print(m.params["L_AI"], m.pvalues["L_AI"])
```
