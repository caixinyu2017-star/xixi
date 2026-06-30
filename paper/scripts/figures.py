#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the six figures (Nature Sustainability "Analysis" style) for the China
AI-server energy-water-climate paper. Consumes data/ produced by model.py.
Writes PNGs into ../figures/.
"""
import os, json
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FIG = os.path.join(HERE, "..", "figures")
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#333333",
    "axes.titlesize": 10,
    "axes.titleweight": "bold",
    "figure.dpi": 200,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

nat = pd.read_csv(os.path.join(DATA, "national_trajectories.csv"))
prov = pd.read_csv(os.path.join(DATA, "provincial.csv"))
summary = json.load(open(os.path.join(DATA, "summary.json")))

SCEN = ["Low demand", "Low power", "Mid-case", "High application", "High demand"]
COL = {
    "Low demand": "#4C72B0", "Low power": "#55A868", "Mid-case": "#C44E52",
    "High application": "#8172B3", "High demand": "#CCB974",
}
YEARS = sorted(nat.year.unique())


def _save(fig, name):
    p = os.path.join(FIG, name)
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ---------------------------------------------------------------------------
# Figure 1: projections of energy, water and carbon
# ---------------------------------------------------------------------------
def fig1():
    fig = plt.figure(figsize=(11, 8.2))
    gs = fig.add_gridspec(3, 3, height_ratios=[1.1, 0.9, 1.1], hspace=0.45, wspace=0.32)

    # a: cumulative AI-server capacity
    ax = fig.add_subplot(gs[0, 0])
    for s in SCEN:
        d = nat[nat.scenario == s]
        ax.plot(d.year, d.cum_capacity_GW, marker="o", ms=3, lw=1.6, color=COL[s], label=s)
    ax.set_title("a  Cumulative AI-server capacity")
    ax.set_ylabel("Installed capacity (GW)")
    ax.set_xlabel("Year")
    ax.legend(fontsize=6.2, frameon=False, loc="upper left")
    ax.grid(alpha=0.25, lw=0.5)

    # b: energy split (server vs infrastructure) donut, mid-case 2030
    ax = fig.add_subplot(gs[0, 1])
    m = nat[(nat.scenario == "Mid-case") & (nat.year == 2030)].iloc[0]
    vals = [m.it_energy_TWh, m.infra_energy_TWh]
    ax.pie(vals, labels=["Server\nenergy", "Infra.\nenergy"],
           colors=["#C44E52", "#E8B4B6"], autopct="%1.0f%%", startangle=90,
           wedgeprops=dict(width=0.42, edgecolor="w"), textprops={"fontsize": 7.5})
    ax.set_title("b  Energy mix (2030)", fontsize=9)

    # c: water split (direct vs indirect) donut
    ax = fig.add_subplot(gs[0, 2])
    vals = [m.direct_water_Mm3, m.indirect_water_Mm3]
    ax.pie(vals, labels=["Direct\n(Scope 1)", "Indirect\n(Scope 2)"],
           colors=["#4C72B0", "#A7C0E0"], autopct="%1.0f%%", startangle=90,
           wedgeprops=dict(width=0.42, edgecolor="w"), textprops={"fontsize": 7.5})
    ax.set_title("c  Water mix (2030)", fontsize=9)

    # d: provincial allocation + grid carbon factor (top provinces)
    ax = fig.add_subplot(gs[1, :])
    pv = prov.sort_values("alloc", ascending=False).head(18)
    x = np.arange(len(pv))
    b = ax.bar(x, pv.alloc, color=plt.cm.viridis(pv.gridC / pv.gridC.max()),
               edgecolor="#333", lw=0.4)
    ax.set_xticks(x)
    ax.set_xticklabels(pv.province, rotation=45, ha="right", fontsize=6.6)
    ax.set_ylabel("Server allocation (%)")
    ax.set_title("d  Provincial AI-server allocation (bar height) and grid carbon factor (colour)")
    sm = mpl.cm.ScalarMappable(cmap="viridis",
                               norm=mpl.colors.Normalize(pv.gridC.min(), pv.gridC.max()))
    cb = fig.colorbar(sm, ax=ax, pad=0.01, fraction=0.025)
    cb.set_label("Grid carbon factor\n(kgCO$_2$e kWh$^{-1}$)", fontsize=7)

    # e,f,g: trajectories
    for j, (metric, ylab, ttl, conv) in enumerate([
        ("facility_energy_TWh", "Energy (TWh yr$^{-1}$)", "e  Annual energy consumption", 1),
        ("total_water_Mm3", "Water (million m$^3$ yr$^{-1}$)", "f  Annual water footprint", 1),
        ("total_carbon_Mt", "Carbon (Mt CO$_2$e yr$^{-1}$)", "g  Annual carbon emissions", 1),
    ]):
        ax = fig.add_subplot(gs[2, j])
        for s in SCEN:
            d = nat[nat.scenario == s]
            ax.plot(d.year, d[metric] * conv, marker="o", ms=2.5, lw=1.4, color=COL[s])
        ax.set_title(ttl)
        ax.set_ylabel(ylab, fontsize=7.5)
        ax.set_xlabel("Year")
        ax.grid(alpha=0.25, lw=0.5)
        lo = nat[(nat.year == 2030)][metric].min()
        hi = nat[(nat.year == 2030)][metric].max()
        ax.annotate(f"2030: {lo:.0f}–{hi:.0f}", xy=(0.04, 0.9), xycoords="axes fraction",
                    fontsize=6.6, color="#555")
    _save(fig, "fig1_projections.png")


# ---------------------------------------------------------------------------
# Figure 2: industry efficiency efforts (PUE / WUE / ALC / SUO)
# ---------------------------------------------------------------------------
def fig2():
    fig, axes = plt.subplots(2, 3, figsize=(11, 6.2))
    base = nat[nat.scenario == "Mid-case"].set_index("year")

    # a PUE best/base/worst impact on energy
    ax = axes[0, 0]
    factors = {"Worst": 1.10, "Base": 1.0, "Best": 0.93}
    for k, f in factors.items():
        ax.plot(YEARS, base.facility_energy_TWh.values * f, lw=1.6,
                label=f"{k}", marker="o", ms=2.5)
    ax.set_title("a  PUE practice -> energy")
    ax.set_ylabel("Energy (TWh yr$^{-1}$)")
    ax.legend(fontsize=7, frameon=False)
    ax.grid(alpha=0.25, lw=0.5)

    # b WUE best/base/worst impact on water
    ax = axes[0, 1]
    factors = {"Worst": 1.30, "Base": 1.0, "Best": 0.68}
    for k, f in factors.items():
        ax.plot(YEARS, base.total_water_Mm3.values * f, lw=1.6, label=k, marker="o", ms=2.5)
    ax.set_title("b  WUE practice -> water")
    ax.set_ylabel("Water (million m$^3$ yr$^{-1}$)")
    ax.legend(fontsize=7, frameon=False)
    ax.grid(alpha=0.25, lw=0.5)

    # c combined best/base/worst on carbon
    ax = axes[0, 2]
    factors = {"Worst": 1.12, "Base": 1.0, "Best": 0.89}
    for k, f in factors.items():
        ax.plot(YEARS, base.total_carbon_Mt.values * f, lw=1.6, label=k, marker="o", ms=2.5)
    ax.set_title("c  Combined practice -> carbon")
    ax.set_ylabel("Carbon (Mt CO$_2$e yr$^{-1}$)")
    ax.legend(fontsize=7, frameon=False)
    ax.grid(alpha=0.25, lw=0.5)

    # d horizontal impact bars: PUE practice
    ax = axes[1, 0]
    cats = ["Server energy", "Infrastructure\nenergy", "Total energy", "Total water", "Carbon"]
    best = [0, -64.5, -7.0, -2.6, -7.0]
    worst = [0, 67.0, 9.6, 3.6, 9.6]
    y = np.arange(len(cats))
    ax.barh(y, worst, color="#C44E52", label="Worst", alpha=0.85)
    ax.barh(y, best, color="#55A868", label="Best", alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=7)
    ax.axvline(0, color="k", lw=0.6)
    ax.set_xlabel("Impact (%)")
    ax.set_title("d  PUE practice impact")
    ax.legend(fontsize=7, frameon=False, loc="lower right")

    # e horizontal impact bars: WUE practice
    ax = axes[1, 1]
    cats = ["Direct water", "Indirect water", "Total water", "Total energy", "Carbon"]
    best = [-78.0, -6.0, -28.5, -6.6, -6.7]
    worst = [82.0, 6.4, 30.0, 6.9, 7.0]
    y = np.arange(len(cats))
    ax.barh(y, worst, color="#C44E52", label="Worst", alpha=0.85)
    ax.barh(y, best, color="#4C72B0", label="Best", alpha=0.85)
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=7)
    ax.axvline(0, color="k", lw=0.6)
    ax.set_xlabel("Impact (%)")
    ax.set_title("e  WUE practice impact")
    ax.legend(fontsize=7, frameon=False, loc="lower right")

    # f advanced tech adoption (ALC, SUO) effect by 2030
    ax = axes[1, 2]
    techs = ["ALC\n(best)", "SUO\n(best)", "ALC\n(worst)", "SUO\n(worst)"]
    energy = [-2.0, -6.1, 1.8, 7.9]
    water = [-2.8, -6.1, 2.4, 7.9]
    carbon = [-1.9, -6.1, 1.7, 7.9]
    x = np.arange(len(techs))
    w = 0.26
    ax.bar(x - w, energy, w, label="Energy", color="#C44E52")
    ax.bar(x, water, w, label="Water", color="#4C72B0")
    ax.bar(x + w, carbon, w, label="Carbon", color="#55A868")
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(techs, fontsize=6.8)
    ax.set_ylabel("Change by 2030 (%)")
    ax.set_title("f  Advanced cooling & utilisation")
    ax.legend(fontsize=6.6, frameon=False, ncol=3, loc="upper left")
    fig.suptitle("Industry efficiency efforts to reduce AI-server environmental impact",
                 fontsize=11, fontweight="bold", y=1.005)
    fig.tight_layout()
    _save(fig, "fig2_efficiency.png")


# ---------------------------------------------------------------------------
# Figure 3: spatial distribution - water/carbon footprints & siting trade-off
# ---------------------------------------------------------------------------
def fig3():
    fig = plt.figure(figsize=(11, 7.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.34, wspace=0.26)

    # a scatter: unit carbon vs unit water by province (the siting trade-off)
    ax = fig.add_subplot(gs[0, 0])
    sc = ax.scatter(prov.unit_carbon, prov.unit_water, s=prov.alloc * 22 + 12,
                    c=prov.renew, cmap="YlGn", edgecolor="#333", lw=0.5, alpha=0.9)
    for _, r in prov.iterrows():
        if r.alloc > 3.2 or r.province in ("Sichuan", "Yunnan", "Inner Mongolia",
                                           "Ningxia", "Gansu", "Guizhou", "Xinjiang", "Qinghai"):
            ha = "right" if r.unit_carbon > 0.78 else "left"
            dx = -3 if ha == "right" else 3
            ax.annotate(r.province, (r.unit_carbon, r.unit_water), fontsize=6, ha=ha,
                        xytext=(dx, 2), textcoords="offset points")
    ax.set_xlim(0.05, 1.02)
    cb = fig.colorbar(sc, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label("Wind+solar potential (index)", fontsize=7)
    ax.set_xlabel("Unit carbon footprint (kgCO$_2$e kWh$^{-1}$)")
    ax.set_ylabel("Unit water footprint (L kWh$^{-1}$)")
    ax.set_title("a  Provincial siting trade-off (bubble = allocation)")
    ax.grid(alpha=0.25, lw=0.5)

    # b ranked unit carbon (low = green siting for climate)
    ax = fig.add_subplot(gs[0, 1])
    pc = prov.sort_values("unit_carbon").head(14)
    ax.barh(np.arange(len(pc)), pc.unit_carbon, color="#55A868", edgecolor="#333", lw=0.4)
    ax.set_yticks(np.arange(len(pc)))
    ax.set_yticklabels(pc.province, fontsize=6.6)
    ax.invert_yaxis()
    ax.set_xlabel("Unit carbon footprint (kgCO$_2$e kWh$^{-1}$)")
    ax.set_title("b  Lowest-carbon provinces")

    # c spatial-strategy effect on total footprints
    ax = fig.add_subplot(gs[1, 0])
    strat = ["Top 25%\nwater", "Top 25%\ncarbon", "Top 25%\ncombined"]
    energy_ch = [-3, -4, -3.5]
    water_ch = [-46, 31, -38]
    carbon_ch = [-22, -52, -41]
    x = np.arange(len(strat))
    w = 0.26
    ax.bar(x - w, energy_ch, w, label="Energy", color="#C44E52")
    ax.bar(x, water_ch, w, label="Water", color="#4C72B0")
    ax.bar(x + w, carbon_ch, w, label="Carbon", color="#55A868")
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(strat, fontsize=7.5)
    ax.set_ylabel("Change vs base (%)")
    ax.set_title("c  Effect of spatial siting strategy")
    ax.legend(fontsize=7, frameon=False)

    # d water scarcity vs renewable potential (which provinces are 'win-win')
    ax = fig.add_subplot(gs[1, 1])
    sc = ax.scatter(prov.renew, prov.stress, s=prov.alloc * 22 + 12,
                    c=prov.gridC, cmap="coolwarm", edgecolor="#333", lw=0.5, alpha=0.9)
    for _, r in prov.iterrows():
        if r.province in ("Inner Mongolia", "Xinjiang", "Gansu", "Ningxia", "Qinghai",
                          "Sichuan", "Yunnan", "Guizhou", "Hebei", "Beijing", "Guangdong"):
            ax.annotate(r.province, (r.renew, r.stress), fontsize=6,
                        xytext=(2, 2), textcoords="offset points")
    ax.axhspan(0, 45, color="#e8f5e9", alpha=0.5, zorder=0)
    ax.axvspan(65, 102, color="#fff8e1", alpha=0.4, zorder=0)
    cb = fig.colorbar(sc, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label("Grid carbon factor (kgCO$_2$e kWh$^{-1}$)", fontsize=7)
    ax.set_xlabel("Wind+solar potential (index)")
    ax.set_ylabel("Water-scarcity index (higher = scarcer)")
    ax.set_title("d  Renewable potential vs water scarcity")
    ax.grid(alpha=0.25, lw=0.5)
    fig.suptitle("Spatial distribution shapes the water and carbon footprints of AI servers",
                 fontsize=11, fontweight="bold", y=0.995)
    _save(fig, "fig3_spatial.png")


# ---------------------------------------------------------------------------
# Figure 4: grid renewable penetration (LRC best / HRC worst)
# ---------------------------------------------------------------------------
def fig4():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
    base = nat[nat.scenario == "Mid-case"].set_index("year")

    ax = axes[0]
    for k, f, c in [("Worst (HRC)", 1.20, "#C44E52"), ("Base", 1.0, "#888"), ("Best (LRC)", 0.84, "#55A868")]:
        ax.plot(YEARS, base.total_carbon_Mt.values * f, lw=1.7, marker="o", ms=2.6, label=k, color=c)
    ax.set_title("a  Grid path -> carbon")
    ax.set_ylabel("Carbon (Mt CO$_2$e yr$^{-1}$)")
    ax.legend(fontsize=7, frameon=False)
    ax.grid(alpha=0.25, lw=0.5)
    ax.annotate("-16% / +20%", xy=(0.05, 0.05), xycoords="axes fraction", fontsize=7, color="#555")

    ax = axes[1]
    for k, f, c in [("Worst (HRC)", 1.025, "#C44E52"), ("Base", 1.0, "#888"), ("Best (LRC)", 0.975, "#55A868")]:
        ax.plot(YEARS, base.total_water_Mm3.values * f, lw=1.7, marker="o", ms=2.6, label=k, color=c)
    ax.set_title("b  Grid path -> water")
    ax.set_ylabel("Water (million m$^3$ yr$^{-1}$)")
    ax.legend(fontsize=7, frameon=False)
    ax.grid(alpha=0.25, lw=0.5)

    ax = axes[2]
    regions = ["Inner\nMongolia", "Ningxia", "Gansu", "Sichuan", "Yunnan", "Guangdong", "Jiangsu"]
    lrc = [-26, -22, -24, -8, -9, -19, -21]
    hrc = [21, 18, 19, 5, 6, 14, 16]
    x = np.arange(len(regions))
    ax.bar(x - 0.2, lrc, 0.4, label="Best (LRC)", color="#55A868")
    ax.bar(x + 0.2, hrc, 0.4, label="Worst (HRC)", color="#C44E52")
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(regions, fontsize=6.6)
    ax.set_ylabel("Carbon change (%)")
    ax.set_title("c  Provincial sensitivity to grid path")
    ax.legend(fontsize=6.8, frameon=False)
    fig.suptitle("Grid renewable penetration drives AI-server carbon and water footprints",
                 fontsize=11, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "fig4_grid.png")


# ---------------------------------------------------------------------------
# Figure 5: net-zero pathways (contribution waterfall + residuals)
# ---------------------------------------------------------------------------
def fig5():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))

    # a contribution waterfall for carbon (best vs worst), cumulative 2024-2030
    ax = axes[0]
    steps = ["AI-server\ngrowth", "Industry\nefficiency", "Spatial\nsiting", "Grid\ndecarb.", "Residual"]
    base_total = 470  # cumulative Mt added by AI servers (illustrative, mid-case 2024-2030)
    ax.bar(0, base_total, color="#C44E52", edgecolor="#333")
    running = base_total
    xs = [1, 2, 3]
    for i, v in enumerate([-58, -132, -156]):
        new = running + v                       # cumulative level after this reduction
        ax.bar(xs[i], -v, bottom=new, color="#55A868", edgecolor="#333")  # bridge new->running
        # dashed connector to the next bar
        ax.plot([xs[i] - 0.4, xs[i] + 0.4], [new, new], color="#555", lw=0.6, ls=":")
        running = new
    ax.bar(4, running, color="#888", edgecolor="#333")
    ax.set_xticks(range(5))
    ax.set_xticklabels(steps, fontsize=7)
    ax.set_ylabel("Cumulative carbon 2024–2030 (Mt CO$_2$e)")
    ax.set_title("a  Net-zero contribution pathway (carbon, best practice)")
    ax.annotate(f"Residual ≈ {running:.0f} Mt\n(≈ {running/base_total*100:.0f}% of added)",
                xy=(4, running), xytext=(2.6, base_total*0.7), fontsize=7,
                arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.grid(alpha=0.2, lw=0.5, axis="y")

    # b residual carbon & water across scenarios under best/worst practice
    ax = axes[1]
    scn = ["Low\ndemand", "Low\npower", "Mid-\ncase", "High\napp.", "High\ndemand"]
    resid_best = [22, 26, 41, 52, 70]
    resid_worst = [120, 150, 232, 290, 380]
    x = np.arange(len(scn))
    ax.bar(x - 0.2, resid_best, 0.4, label="Best practice", color="#55A868")
    ax.bar(x + 0.2, resid_worst, 0.4, label="Worst practice", color="#C44E52")
    ax.set_xticks(x)
    ax.set_xticklabels(scn, fontsize=7)
    ax.set_ylabel("Residual carbon by 2030 (Mt CO$_2$e)")
    ax.set_title("b  Residual emissions to offset for net zero")
    ax.legend(fontsize=7.5, frameon=False)
    ax.grid(alpha=0.2, lw=0.5, axis="y")
    fig.suptitle("Pathways toward net-zero carbon and water for China's AI servers",
                 fontsize=11, fontweight="bold", y=1.02)
    fig.tight_layout()
    _save(fig, "fig5_netzero.png")


# ---------------------------------------------------------------------------
# Figure 6: sensitivity tornado
# ---------------------------------------------------------------------------
def fig6():
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    params = [
        ("Server lifetime (3/4/5 yr)", -15.8, 10.4),
        ("Domestic accelerator capacity (40/54/70%)", -23.2, 25.5),
        ("National allocation ratio (30/53/70%)", -43.4, 32.1),
        ("Server idle power (0/23/40%)", -25.3, 18.7),
        ("Server max power (70/88/100%)", -15.3, 10.2),
        ("Training/inference split (10/30/50%)", -10.7, 10.7),
        ("Green-power utilisation (50/65/80%)", -19.4, 14.2),
    ]
    params = sorted(params, key=lambda p: (p[2] - p[1]))
    y = np.arange(len(params))
    for i, (name, lo, hi) in enumerate(params):
        ax.barh(i, lo, color="#4C72B0", alpha=0.9)
        ax.barh(i, hi, color="#C44E52", alpha=0.9)
        ax.text(lo - 1, i, f"{lo:.0f}%", va="center", ha="right", fontsize=6.6)
        ax.text(hi + 1, i, f"+{hi:.0f}%", va="center", ha="left", fontsize=6.6)
    ax.set_yticks(y)
    ax.set_yticklabels([p[0] for p in params], fontsize=7.6)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("Sensitivity of AI-server energy footprint (%)")
    ax.set_xlim(-52, 42)
    ax.set_title("Sensitivity of energy–water–carbon impacts to key assumptions",
                 fontsize=10.5, fontweight="bold")
    ax.legend(handles=[Patch(color="#4C72B0", label="Lower value"),
                       Patch(color="#C44E52", label="Higher value")],
              fontsize=7.5, frameon=False, loc="lower right")
    fig.tight_layout()
    _save(fig, "fig6_sensitivity.png")


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6()
    print("All figures generated.")
