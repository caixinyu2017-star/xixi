# Biomimetics manuscripts: MSSBOA and MSBKA

Two full MDPI Biomimetics manuscripts generated end-to-end:

- **Paper A (MSSBOA)** — "A Multi-Strategy Secretary Bird Optimization Algorithm for Global
  Optimization and Cardinality-Constrained Portfolio Selection". CEC2017 benchmarks (10/30D,
  30 runs) + OR-Library cardinality-constrained portfolio selection (5 markets).
- **Paper B (MSBKA)** — "An Enhanced Multi-Strategy Black-Winged Kite Algorithm for Global
  Optimization and Customer Segmentation in Marketing Management". CEC2022 benchmarks (10/20D,
  30 runs) + customer segmentation clustering (Mall customers, UCI Wholesale customers).

## Layout
- `code/` — algorithm implementations (SBOA, BKA, MSSBOA, MSBKA + 11 comparison algorithms),
  experiment runners, statistics/figures, and the Word document builder (native OMML equations
  via pandoc; MDPI template styles preserved).
- `data/` — OR-Library port1-5 (GitHub mirror of Beasley's OR-Library), Mall_Customers.csv,
  UCI Wholesale customers (GitHub mirror).
- `results/` — raw experiment CSVs and convergence curves (30 independent runs per setting).
- `figs/` — all manuscript figures (300 dpi).
- `out/` — final .docx manuscripts.

All benchmark data come from the opfunu package (CEC2017/CEC2022); base-algorithm equations
were transcribed from the original papers and their official MATLAB implementations.
