# -*- coding: utf-8 -*-
"""The EU-27 country-level dataset used throughout the analysis.

One row per EU member state. Variable definitions and Eurostat source
datasets are documented in Table 1 of the manuscript and in the project
README; the README also carries the data-provenance disclosure and the
instruction to re-extract every column from the Eurostat dissemination
API before submission.

Columns
-------
AIENT   Enterprises using at least one AI technology, % of enterprises
        with 10 or more employees, 2024 (isoc_eb_ai).
GAIY    Young individuals (16-29) who used generative AI tools in the
        last three months, %, 2025 ICT survey (isoc_ci_ax_i).
DSKY    Young people (16-24) with basic or above-basic overall digital
        skills, %, 2023 (isoc_sk_dskl_i21).
ICTS    ICT specialists, % of total employment, 2024 (isoc_sks_itspt).
NEET    Young people neither in employment nor in education and
        training, % of the population aged 15-29, 2024 (edat_lfse_20).
YUR     Youth unemployment rate, % of the labour force aged 15-24,
        2024 (une_rt_a).
TERT    Tertiary educational attainment, % of the population aged
        25-34, 2024 (edat_lfse_03).
GDPC    GDP per capita in purchasing power standards, index EU-27 =
        100, 2024 (prc_ppp_ind).
RDI     Gross domestic expenditure on R&D, % of GDP, 2023 (rd_e_gerdtot).
ELET    Early leavers from education and training, % of the population
        aged 18-24, 2024 (edat_lfse_14).
"""

COLUMNS = ["AIENT", "GAIY", "DSKY", "ICTS", "NEET", "YUR",
           "TERT", "GDPC", "RDI", "ELET"]

#            country          AIENT  GAIY  DSKY  ICTS  NEET   YUR   TERT  GDPC  RDI  ELET
ROWS = [
    ("Belgium",               24.7,  55.4, 75.2,  5.6,  9.0, 16.9,  51.8, 118, 3.4,  6.7),
    ("Bulgaria",               6.5,  33.8, 52.9,  3.6, 13.8, 12.9,  33.6,  66, 0.8, 10.9),
    ("Czechia",               10.5,  51.2, 78.1,  4.5, 10.4,  8.7,  35.0,  91, 1.8,  5.7),
    ("Denmark",               27.6,  65.0, 84.3,  6.4,  7.7, 10.1,  49.0, 129, 2.9,  9.6),
    ("Germany",               19.8,  48.9, 74.4,  5.1,  8.9,  6.8,  38.1, 115, 3.1, 12.6),
    ("Estonia",               14.4,  57.5, 82.0,  6.4, 10.3, 20.4,  44.9,  79, 1.8,  9.7),
    ("Ireland",               18.3,  57.4, 76.8,  6.3,  8.3, 11.2,  63.7, 211, 0.9,  3.1),
    ("Greece",                 8.9,  49.3, 70.8,  2.6, 12.6, 22.4,  45.7,  70, 1.5,  3.9),
    ("Spain",                 11.3,  57.8, 82.9,  4.4, 12.2, 26.5,  52.1,  89, 1.4, 13.0),
    ("France",                10.9,  44.6, 77.6,  4.7, 12.4, 18.9,  50.4,  98, 2.2,  7.6),
    ("Croatia",               18.2,  50.8, 88.6,  3.9, 11.0, 15.9,  36.4,  76, 1.4,  2.2),
    ("Italy",                  8.2,  41.7, 65.7,  3.9, 15.2, 20.3,  31.6,  97, 1.3,  9.8),
    ("Cyprus",                11.6,  48.9, 68.3,  4.6, 13.5, 15.6,  61.9,  97, 0.8,  8.9),
    ("Latvia",                 8.8,  46.5, 71.4,  4.3, 10.9, 13.5,  47.9,  71, 0.7,  8.6),
    ("Lithuania",             10.0,  49.8, 76.3,  4.7,  9.5, 14.4,  58.4,  87, 1.0,  4.6),
    ("Luxembourg",            21.4,  57.0, 79.7,  7.7,  7.1, 18.8,  62.0, 237, 1.0,  7.8),
    ("Hungary",                7.0,  35.9, 68.9,  4.1, 10.6, 13.1,  32.2,  77, 1.4, 11.6),
    ("Malta",                 19.4,  58.9, 85.2,  6.6,  7.6,  8.9,  46.4, 107, 0.6, 10.1),
    ("Netherlands",           22.7,  63.6, 88.4,  7.1,  4.9,  8.8,  56.5, 130, 2.3,  7.3),
    ("Austria",               19.9,  52.7, 81.6,  4.9,  8.2, 11.5,  43.4, 123, 3.3,  8.4),
    ("Poland",                 5.9,  44.9, 69.7,  3.7,  9.2, 11.4,  46.0,  80, 1.6,  4.7),
    ("Portugal",               9.2,  55.6, 80.8,  4.7,  8.6, 20.6,  47.5,  82, 1.7,  8.0),
    ("Romania",                3.1,  26.4, 46.9,  2.7, 19.4, 24.0,  23.2,  78, 0.5, 16.8),
    ("Slovenia",              20.9,  53.5, 80.2,  4.5,  6.7,  9.6,  46.7,  91, 2.1,  4.2),
    ("Slovakia",               7.9,  41.2, 73.6,  4.2, 12.1, 20.0,  39.4,  73, 1.0,  6.6),
    ("Finland",               24.4,  61.8, 84.8,  7.6,  9.4, 17.6,  40.1, 109, 3.0,  8.6),
    ("Sweden",                25.1,  62.9, 83.4,  8.6,  5.9, 23.6,  52.6, 119, 3.6,  8.8),
]


def frame():
    """Return (countries, {column: list_of_values})."""
    countries = [r[0] for r in ROWS]
    data = {c: [r[i + 1] for r in ROWS] for i, c in enumerate(COLUMNS)}
    return countries, data


if __name__ == "__main__":
    countries, data = frame()
    print("N =", len(countries))
    for c in COLUMNS:
        v = data[c]
        print("%-6s min %6.1f  max %6.1f  mean %6.2f"
              % (c, min(v), max(v), sum(v) / len(v)))
