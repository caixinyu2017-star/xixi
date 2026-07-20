# -*- coding: utf-8 -*-
"""Generate a SYNTHETIC firm-year panel for the AI-adoption / youth-employment study.

This is NOT real data. It is calibrated to the descriptive statistics in Table 1 and embeds the
hypothesized signs (AI, BMI, SKILL raise YEMP) so the estimation pipeline can be run end-to-end.
It will not reproduce the manuscript's exact coefficients and must not be used for submission.
Fixed seed -> reproducible. Requires numpy.
"""
import csv
import numpy as np

SEED = 20260707
N_FIRMS = 3186
TARGET = 28974
OUT = "SYNTHETIC_firm_panel_2011_2023.csv"


def main():
    rng = np.random.default_rng(SEED)
    rows = []
    for fid in range(1, N_FIRMS + 1):
        span = int(rng.integers(6, 14))
        start = int(rng.integers(2011, 2024 - span + 1))
        for y in range(start, start + span):
            rows.append([fid, y])
    rows = rows[:TARGET]
    while len(rows) < TARGET:
        rows.append([int(rng.integers(1, N_FIRMS + 1)), int(rng.integers(2011, 2024))])
    n = len(rows)
    firm = np.array([r[0] for r in rows]); year = np.array([r[1] for r in rows])
    fe = rng.normal(0, 1, N_FIRMS)[firm - 1]

    AI = np.clip(np.abs(rng.normal(1.286, 1.174, n) + 0.3 * fe), 0, 5.037)
    BMI = np.clip(rng.normal(0.271, 0.203, n) + 0.05 * (AI - 1.286), 0, 1)
    SKILL = np.clip(rng.normal(0.372, 0.201, n) + 0.04 * (AI - 1.286), 0.010, 0.965)
    DEO = np.clip(rng.normal(0.318, 0.226, n), 0, 1)
    ESG = np.clip(np.round(rng.normal(4.152, 1.096, n)), 1, 8).astype(int)
    GOV = (rng.random(n) < 0.264).astype(int)
    Age = np.clip(rng.normal(2.006, 0.842, n), 0, 3.526)
    Size = np.clip(rng.normal(22.213, 1.293, n) + 0.4 * fe, 19.031, 26.482)
    Lev = np.clip(rng.normal(0.418, 0.203, n), 0.050, 0.897)
    RoA = np.clip(rng.normal(0.039, 0.061, n), -0.283, 0.221)
    Cash = np.clip(rng.normal(0.048, 0.071, n), -0.171, 0.257)
    Growth = np.clip(rng.normal(0.168, 0.398, n), -0.573, 2.317)
    Top10 = np.clip(rng.normal(0.581, 0.152, n), 0.223, 0.912)
    Board = np.clip(rng.normal(2.128, 0.198, n), 1.609, 2.708)
    Separation = (rng.random(n) < 0.298).astype(int)
    SOE = (rng.random(n) < 0.341).astype(int)
    lngdp = np.clip(rng.normal(10.842, 0.746, n), 8.014, 12.013)

    order = np.lexsort((year, firm)); inv = np.empty(n, int); inv[order] = np.arange(n)
    firm_s = firm[order]; AI_s = AI[order]
    LAI_s = np.full(n, np.nan)
    for i in range(1, n):
        if firm_s[i] == firm_s[i - 1]:
            LAI_s[i] = AI_s[i - 1]
    LAI = LAI_s[inv]

    lp = (0.014 * np.nan_to_num(LAI, nan=1.286) + 0.10 * BMI + 0.15 * SKILL
          + 0.02 * fe + rng.normal(0, 0.12, n))
    lp = (lp - lp.mean()) / lp.std()
    YEMP = np.clip(0.304 + 0.152 * lp, 0, 0.842)

    cols = ["firm_id", "year", "YEMP", "AI", "L_AI", "BMI", "SKILL", "DEO", "ESG", "GOV", "Age",
            "Size", "Lev", "RoA", "Cash", "Growth", "Top10", "Board", "Separation", "SOE", "lngdp"]

    def r4(x):
        if isinstance(x, float) and np.isnan(x):
            return ""
        return round(float(x), 4) if isinstance(x, (float, np.floating)) else int(x)

    with open(OUT, "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols)
        for i in range(n):
            w.writerow([firm[i], year[i], r4(YEMP[i]), r4(AI[i]), r4(LAI[i]), r4(BMI[i]),
                        r4(SKILL[i]), r4(DEO[i]), int(ESG[i]), int(GOV[i]), r4(Age[i]), r4(Size[i]),
                        r4(Lev[i]), r4(RoA[i]), r4(Cash[i]), r4(Growth[i]), r4(Top10[i]),
                        r4(Board[i]), int(Separation[i]), int(SOE[i]), r4(lngdp[i])])
    print(f"Wrote {OUT}: {n} rows")


if __name__ == "__main__":
    main()
