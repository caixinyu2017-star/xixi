#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation engine for:
  "Compound energy-water-climate impacts and net-zero pathways for AI servers in China, 2024-2030"

Modelled on Xiao et al. (2025) Nature Sustainability (US AI servers).
Provincial attributes are grounded in publicly reported China facts (regional grid
emission factors, the East-Data-West-Computing / 东数西算 hubs, provincial water stress
and wind/solar potential). Server-capacity trajectories are scenario-based projections
constrained by the domestic AI-accelerator packaging bottleneck (analogue to CoWoS/TSMC).

Outputs:
  data/national_trajectories.csv
  data/provincial.csv
  data/summary.json
"""
import json, os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
os.makedirs(DATA, exist_ok=True)

YEARS = list(range(2024, 2031))
SCENARIOS = ["Low demand", "Low power", "Mid-case", "High application", "High demand"]

# ----------------------------------------------------------------------------
# 1. National cumulative AI-server power-capacity trajectories (GW, installed)
#    Driven by domestic AI-accelerator (Huawei Ascend via SMIC advanced packaging)
#    output plus constrained imported accelerators. Calibrated so the mid-case
#    facility energy reaches ~160 TWh by 2030 (consistent with CAICT/IEA-scale
#    China data-centre electricity growth dominated by intelligent computing).
# ----------------------------------------------------------------------------
# cumulative installed capacity (GW) by year for each scenario
CUM_CAP = {
    "Low demand":       np.array([6.0, 9.0, 12.5, 16.0, 19.5, 23.0, 26.5]),
    "Low power":        np.array([6.0, 9.5, 13.5, 18.0, 22.5, 27.0, 31.5]),
    "Mid-case":         np.array([6.0, 10.0, 15.0, 21.0, 28.0, 35.0, 42.0]),
    "High application": np.array([6.0, 10.5, 16.5, 24.0, 32.5, 41.0, 50.0]),
    "High demand":      np.array([6.0, 11.0, 18.0, 28.0, 40.0, 53.0, 66.0]),
}
# annual shipment (first difference, for the headline like Xiao Fig.1a)
ANNUAL_SHIP = {s: np.diff(np.concatenate([[3.5], CUM_CAP[s]])) for s in SCENARIOS}

# Effective load factor: fraction of rated cumulative capacity drawn on average
# (utilisation x duty-cycle; lower in low-power scenario reflecting efficient HW).
LOAD_FACTOR = {
    "Low demand": 0.290, "Low power": 0.265, "Mid-case": 0.335,
    "High application": 0.340, "High demand": 0.345,
}
HOURS = 8760.0

# Average facility PUE (national, allocation-weighted) declining slightly with
# efficiency improvements and policy caps; base scenario.
PUE_NAT = {y: v for y, v in zip(YEARS, [1.33, 1.32, 1.31, 1.30, 1.29, 1.28, 1.27])}

# National allocation-weighted grid CARBON factor (kgCO2e/kWh), base grid path,
# declining as the power system decarbonises toward the dual-carbon goals.
GRID_C_NAT = {y: v for y, v in zip(YEARS, [0.575, 0.560, 0.545, 0.525, 0.505, 0.485, 0.470])}
# National allocation-weighted grid WATER factor (L/kWh, Scope-2 indirect),
# slowly declining as thermal share falls (but hydro keeps it elevated).
GRID_W_NAT = {y: v for y, v in zip(YEARS, [4.35, 4.28, 4.20, 4.12, 4.05, 3.98, 3.92])}
# On-site (Scope-1) water-use effectiveness, L/kWh facility, base.
WUE_NAT = {y: v for y, v in zip(YEARS, [1.62, 1.60, 1.58, 1.56, 1.54, 1.52, 1.50])}
# Scope-3 embodied carbon as a fraction of operational carbon (manufacturing).
SCOPE3_C_FRAC = 0.14
SCOPE3_W_FRAC = 0.06

def national_trajectories():
    rows = []
    for s in SCENARIOS:
        for i, y in enumerate(YEARS):
            it_energy = CUM_CAP[s][i] * LOAD_FACTOR[s] * HOURS / 1000.0   # TWh (GW*h/1000)
            fac_energy = it_energy * PUE_NAT[y]                            # TWh facility
            infra_energy = fac_energy - it_energy
            # TWh * (L/kWh): 1 TWh = 1e9 kWh; L -> million m3 divides by 1e9 -> factor 1
            direct_water = fac_energy * WUE_NAT[y]                         # million m3
            indirect_water = fac_energy * GRID_W_NAT[y]                    # million m3
            total_water = direct_water + indirect_water
            # TWh * (kg/kWh): 1 TWh = 1e9 kWh; kg -> Mt divides by 1e9 -> factor 1
            scope2_c = fac_energy * GRID_C_NAT[y]                          # Mt CO2e
            scope3_c = scope2_c * SCOPE3_C_FRAC
            total_c = scope2_c + scope3_c
            rows.append(dict(scenario=s, year=y,
                             cum_capacity_GW=round(CUM_CAP[s][i], 2),
                             annual_shipment_GW=round(ANNUAL_SHIP[s][i], 2),
                             it_energy_TWh=round(it_energy, 2),
                             infra_energy_TWh=round(infra_energy, 2),
                             facility_energy_TWh=round(fac_energy, 2),
                             direct_water_Mm3=round(direct_water, 1),
                             indirect_water_Mm3=round(indirect_water, 1),
                             total_water_Mm3=round(total_water, 1),
                             scope2_carbon_Mt=round(scope2_c, 2),
                             scope3_carbon_Mt=round(scope3_c, 2),
                             total_carbon_Mt=round(total_c, 2)))
    return pd.DataFrame(rows)

# ----------------------------------------------------------------------------
# 2. Provincial attributes (31 mainland provinces)
#    cols: region, hub(node of East-Data-West-Computing or ""), alloc(% share),
#          gridC(kgCO2/kWh), gridW(L/kWh indirect), pue, wue(L/kWh direct),
#          renew(0-100 wind+solar technical-potential index),
#          stress(0-100 water-scarcity index, higher = scarcer)
# ----------------------------------------------------------------------------
PROV = [
    # name, region, hub, alloc, gridC, gridW, pue, wue, renew, stress
    ("Beijing",        "North",     "Beijing-Tianjin-Hebei", 6.0, 0.60, 3.0, 1.28, 1.2, 35, 95),
    ("Tianjin",        "North",     "Beijing-Tianjin-Hebei", 2.0, 0.68, 3.1, 1.30, 1.3, 38, 95),
    ("Hebei",          "North",     "Beijing-Tianjin-Hebei", 7.0, 0.72, 3.0, 1.25, 1.3, 55, 92),
    ("Shanxi",         "North",     "",                      2.0, 0.74, 2.8, 1.24, 1.0, 50, 88),
    ("Inner Mongolia", "North",     "Inner Mongolia",        9.0, 0.76, 2.5, 1.20, 0.8, 100, 80),
    ("Shandong",       "East",      "",                      4.0, 0.68, 3.2, 1.32, 1.4, 45, 88),
    ("Liaoning",       "Northeast", "",                      2.0, 0.66, 3.0, 1.26, 1.2, 48, 70),
    ("Jilin",          "Northeast", "",                      1.0, 0.56, 3.0, 1.24, 1.1, 50, 55),
    ("Heilongjiang",   "Northeast", "",                      1.0, 0.66, 3.0, 1.22, 1.0, 48, 45),
    ("Shanghai",       "East",      "Yangtze River Delta",   5.0, 0.56, 3.5, 1.35, 1.8, 25, 60),
    ("Jiangsu",        "East",      "Yangtze River Delta",   7.0, 0.64, 3.5, 1.35, 1.9, 30, 55),
    ("Zhejiang",       "East",      "Yangtze River Delta",   6.0, 0.51, 3.8, 1.34, 1.9, 28, 45),
    ("Anhui",          "East",      "Yangtze River Delta",   3.0, 0.69, 3.3, 1.36, 1.7, 35, 50),
    ("Fujian",         "East",      "",                      1.5, 0.42, 4.0, 1.40, 2.0, 35, 30),
    ("Jiangxi",        "Central",   "",                      1.5, 0.62, 4.2, 1.40, 1.9, 30, 30),
    ("Henan",          "Central",   "",                      3.0, 0.61, 3.4, 1.34, 1.7, 35, 85),
    ("Hubei",          "Central",   "",                      3.0, 0.33, 5.5, 1.38, 2.0, 35, 30),
    ("Hunan",          "Central",   "",                      2.0, 0.42, 4.8, 1.40, 2.0, 32, 28),
    ("Guangdong",      "South",     "Guangdong-HK-Macau",    9.0, 0.40, 3.5, 1.42, 2.2, 30, 35),
    ("Guangxi",        "South",     "",                      1.0, 0.40, 5.0, 1.42, 1.9, 35, 28),
    ("Hainan",         "South",     "",                      0.5, 0.45, 4.0, 1.48, 2.1, 40, 30),
    ("Chongqing",      "Southwest", "Chengdu-Chongqing",     3.0, 0.50, 4.5, 1.42, 1.9, 30, 30),
    ("Sichuan",        "Southwest", "Chengdu-Chongqing",     5.0, 0.10, 8.0, 1.30, 1.8, 65, 25),
    ("Guizhou",        "Southwest", "Guizhou",               6.0, 0.50, 4.5, 1.25, 1.6, 45, 30),
    ("Yunnan",         "Southwest", "",                      1.5, 0.11, 7.0, 1.25, 1.6, 60, 25),
    ("Shaanxi",        "Northwest", "",                      2.0, 0.66, 3.0, 1.26, 1.0, 50, 78),
    ("Gansu",          "Northwest", "Gansu",                 4.0, 0.49, 3.0, 1.22, 0.9, 85, 85),
    ("Qinghai",        "Northwest", "",                      1.5, 0.16, 6.0, 1.18, 0.8, 80, 50),
    ("Ningxia",        "Northwest", "Ningxia",               5.0, 0.65, 3.0, 1.20, 1.0, 70, 90),
    ("Xinjiang",       "Northwest", "",                      2.5, 0.65, 2.8, 1.22, 0.9, 95, 82),
    ("Tibet",          "Southwest", "",                      0.0, 0.10, 5.0, 1.20, 0.7, 90, 20),
]
PROV_COLS = ["province", "region", "hub", "alloc", "gridC", "gridW", "pue", "wue", "renew", "stress"]

def provincial_frame():
    df = pd.DataFrame(PROV, columns=PROV_COLS)
    df["alloc"] = df["alloc"] / df["alloc"].sum() * 100.0   # normalise to 100%
    # unit (per-kWh) water and carbon footprint of server energy in each province
    df["unit_carbon"] = df["gridC"] * (1 + SCOPE3_C_FRAC)             # kgCO2e/kWh
    df["unit_water"] = (df["wue"] + df["gridW"]) * (1 + SCOPE3_W_FRAC)  # L/kWh
    return df

def main():
    nat = national_trajectories()
    nat.to_csv(os.path.join(DATA, "national_trajectories.csv"), index=False)
    prov = provincial_frame()
    prov.round(4).to_csv(os.path.join(DATA, "provincial.csv"), index=False)

    # headline summary across scenarios at 2030 and annual averages 2024-2030
    def rng(metric):
        sub = nat[nat.year == 2030]
        return [round(sub[metric].min(), 1), round(sub[metric].max(), 1)]
    avg = nat.groupby("scenario").mean(numeric_only=True)
    summary = dict(
        years=[YEARS[0], YEARS[-1]],
        scenarios=SCENARIOS,
        energy_2030_TWh=rng("facility_energy_TWh"),
        water_2030_Mm3=rng("total_water_Mm3"),
        carbon_2030_Mt=rng("total_carbon_Mt"),
        annual_avg_energy_TWh=[round(avg["facility_energy_TWh"].min(), 1), round(avg["facility_energy_TWh"].max(), 1)],
        annual_avg_water_Mm3=[round(avg["total_water_Mm3"].min(), 1), round(avg["total_water_Mm3"].max(), 1)],
        annual_avg_carbon_Mt=[round(avg["total_carbon_Mt"].min(), 1), round(avg["total_carbon_Mt"].max(), 1)],
        midcase_2030=nat[(nat.scenario == "Mid-case") & (nat.year == 2030)]
                       .drop(columns=["scenario"]).iloc[0].round(2).to_dict(),
        direct_indirect_water_share=[round(nat[nat.year==2030]["direct_water_Mm3"].mean() /
                                           nat[nat.year==2030]["total_water_Mm3"].mean()*100,1),
                                     round(nat[nat.year==2030]["indirect_water_Mm3"].mean() /
                                           nat[nat.year==2030]["total_water_Mm3"].mean()*100,1)],
    )
    with open(os.path.join(DATA, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
