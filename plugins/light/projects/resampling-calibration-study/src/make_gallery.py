"""Gallery of nine publication-grade figures for the showcase README.

All numbers are read verbatim from experiments/results.csv — no value is
invented or adjusted. The visual layer is produced *through the skill pack's
own figure pipeline* (this is the dogfooding statement of the gallery):

  - colours   : light-figure-drawing/scripts/color_palettes.py — Okabe-Ito
                colourblind-safe palette, one fixed condition->colour mapping
                shared by all nine charts; greyscale distinctness printed at
                run time via to_grayscale().
  - export    : light-figure-drawing/scripts/figure_export.py —
                save_publication_figure() (fonttype 42, 300 dpi PNG).
  - statistics: paired Wilcoxon signed-rank + Cliff's delta annotated on the
                charts themselves (journal idiom: every claim carries its n,
                CI and test).

  g1 radar    - 5-metric tradeoff (Base/SMOTE/RUS/+Isotonic), pentagon grid
  g2 violin   - ECE distribution per condition + mean with 95% CI + Wilcoxon p
  g3 slope    - per-dataset ECE repair (SMOTE -> +isotonic), mean delta callout
  g4 bubble   - imbalance ratio vs ECE inflation, area = dataset n, size legend
  g5 diverge  - ECE delta vs baseline by model family, value-labelled bars
  g6 heatmap  - condition x dataset ECE matrix, repair column highlighted
  g7 ridge    - ECE density per condition, median ticks
  g8 ecdf     - cumulative ECE, direct labels + linestyle redundancy (B/W safe)
  g9 lollipop - datasets ranked by ECE inflation under undersampling
Outputs figures/g1_radar.png ... g9_lollipop.png
"""
import sys
from pathlib import Path
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

ROOT = Path(__file__).resolve().parents[1]
LIGHT = Path(__file__).resolve().parents[3]
FIG = ROOT / "figures"; EXP = ROOT / "experiments"

# --- the skill pack's own figure pipeline ----------------------------------
sys.path.insert(0, str(LIGHT / "skills" / "light-figure-drawing" / "scripts"))
from color_palettes import OKABE_ITO, sequential_cmap, to_grayscale  # noqa: E402
from figure_export import save_publication_figure                    # noqa: E402

# ---------------------------------------------------------------------------
# Visual identity. Okabe-Ito (2008) colourblind-safe palette, one FIXED
# condition->colour mapping reused by every chart (cross-figure consistency is
# the first thing a journal art editor checks). Yellow is excluded (illegible
# on white); +Platt takes black.
# ---------------------------------------------------------------------------
INK   = "#1A1A1A"   # near-black — titles, emphasised text
BODY  = "#3B3B3B"
MUTED = "#7A7A7A"   # subtitles, secondary annotations
GRID  = "#E8E8E8"   # hairline grid
PAPER = "#FFFFFF"

COND = {  # condition -> (label, colour)
    "E0_none":        ("Baseline",   OKABE_ITO["blue"]),            # 0072B2
    "E1_smote":       ("SMOTE",      OKABE_ITO["orange"]),          # E69F00
    "E1_ros":         ("ROS",        OKABE_ITO["sky_blue"]),        # 56B4E9
    "E1_rus":         ("RUS",        OKABE_ITO["vermillion"]),      # D55E00
    "E2_cw":          ("Class-wt",   OKABE_ITO["reddish_purple"]),  # CC79A7
    "E3_smote_platt": ("+Platt",     OKABE_ITO["black"]),           # 000000
    "E3_smote_iso":   ("+Isotonic",  OKABE_ITO["bluish_green"]),    # 009E73
}
CC = {k: v[1] for k, v in COND.items()}
CL = {k: v[0] for k, v in COND.items()}

DS_C = {  # dataset -> colour (g3/g4 share it; yeast = the extreme case)
    "pima": OKABE_ITO["sky_blue"], "credit_g": OKABE_ITO["orange"],
    "phoneme": OKABE_ITO["blue"], "adult": OKABE_ITO["reddish_purple"],
    "yeast_ml8": OKABE_ITO["vermillion"],
}
DS_LAB = {"pima": "pima", "credit_g": "credit-g", "phoneme": "phoneme",
          "adult": "adult", "yeast_ml8": "yeast (IR 70)"}
RAMP = sequential_cmap()  # skill default: cream -> orange -> deep red

_avail = {f.name for f in fm.fontManager.ttflist}
_SANS = next((f for f in ["Arial", "Helvetica", "Segoe UI", "Calibri",
                          "Liberation Sans", "DejaVu Sans"] if f in _avail),
             "sans-serif")

plt.rcParams.update({
    "font.family": _SANS, "font.size": 10,
    "text.color": BODY, "mathtext.default": "regular",
    "axes.edgecolor": MUTED, "axes.linewidth": 0.8,
    "axes.labelcolor": INK, "axes.labelsize": 10,
    "xtick.color": BODY, "ytick.color": BODY,
    "xtick.labelsize": 9, "ytick.labelsize": 9,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "xtick.major.size": 3.2, "ytick.major.size": 3.2,
    "legend.fontsize": 9, "legend.frameon": False,
    "figure.dpi": 150, "figure.facecolor": PAPER, "axes.facecolor": PAPER,
})

N = {"pima": 768, "credit_g": 1000, "phoneme": 5404, "adult": 48842,
     "yeast_ml8": 2417}
D = pd.read_csv(EXP / "results.csv")

# paired arrays (dataset x model x seed aligned) for the significance tests
PIV = D.pivot_table(index=["dataset", "model", "seed"], columns="condition",
                    values="ece")
N_RUNS = len(PIV)  # 100 = 5 datasets x 2 models x 10 seeds


def fmt_p(p):
    if p < 1e-15:
        return r"$p<10^{-15}$"
    e = int(np.floor(np.log10(p)))
    return rf"$p={p / 10 ** e:.1f}\times10^{{{e}}}$"


def cliffs_delta(a, b):
    diff = a[:, None] - b[None, :]
    return (np.sum(diff > 0) - np.sum(diff < 0)) / (len(a) * len(b))


def _titles(ax, title, subtitle, tx=0.0):
    """Two-tier heading: bold ink statement + grey reading instruction."""
    ax.set_title("")
    ax.annotate(title, xy=(tx, 1.0), xycoords="axes fraction", ha="left",
                va="bottom", fontsize=12.5, fontweight="bold", color=INK,
                annotation_clip=False, xytext=(0, 24), textcoords="offset points")
    ax.annotate(subtitle, xy=(tx, 1.0), xycoords="axes fraction", ha="left",
                va="bottom", fontsize=9, color=MUTED, annotation_clip=False,
                xytext=(0, 9), textcoords="offset points")


def _despine(ax, keep=("left", "bottom")):
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(s in keep)


def _save(fig, name):
    save_publication_figure(fig, str(FIG / name), formats=("png",), dpi=300,
                            pad_inches=0.16, close=True)
    print(f"[OK] {name}")


def g1_radar():
    """Radar on a pentagon grid: 5 metrics normalised so outer ring = better."""
    conds = ["E0_none", "E1_smote", "E1_rus", "E3_smote_iso"]
    raw = D.groupby("condition")[["auc", "f1", "pr_auc", "ece", "brier"]].mean()
    axes_lab = ["AUC", "F1", "PR-AUC", "Calibration\n(1−ECE)",
                "Brier\n(inverted)"]
    norm = pd.DataFrame(index=raw.index)
    for c in ["auc", "f1", "pr_auc"]:
        norm[c] = (raw[c] - raw[c].min()) / (raw[c].max() - raw[c].min() + 1e-9)
    for c in ["ece", "brier"]:
        norm[c] = (raw[c].max() - raw[c]) / (raw[c].max() - raw[c].min() + 1e-9)
    ang = np.linspace(0, 2 * np.pi, 5, endpoint=False)
    fig, ax = plt.subplots(figsize=(5.9, 5.9), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
    # hand-drawn pentagon grid (circular grid reads "dashboard", polygon "print")
    ax.grid(False); ax.spines["polar"].set_visible(False); ax.set_yticks([])
    closed = np.append(ang, ang[0])
    for r in (0.25, 0.5, 0.75, 1.0):
        ax.plot(closed, [r] * 6, color=GRID if r < 1 else "#D4D4D4",
                lw=0.8, zorder=1)
    for a in ang:
        ax.plot([a, a], [0, 1], color=GRID, lw=0.8, zorder=1)
    ax.text(ang[0] + 0.10, 0.53, "0.5", fontsize=7.5, color=MUTED, ha="left")
    for cond in conds:
        v = norm.loc[cond].tolist(); v += v[:1]
        ax.plot(closed, v, "-o", lw=1.8, ms=4.5, color=CC[cond],
                label=CL[cond], zorder=3, markeredgecolor="white",
                markeredgewidth=0.9)
        ax.fill(closed, v, color=CC[cond], alpha=0.05, zorder=2)
    ax.set_xticks(ang)
    ax.set_xticklabels(axes_lab, fontsize=9, color=INK)
    ax.tick_params(axis="x", pad=10)
    ax.set_ylim(0, 1.02)
    # the story annotation: the calibration vertex is where SMOTE/RUS collapse
    ax.annotate("the axis that\ncollapses", xy=(ang[3], norm.loc["E1_rus"][3:4].iloc[0] + 0.02),
                xytext=(-58, -34), textcoords="offset points", fontsize=8.5,
                color=MUTED, style="italic", ha="center",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8,
                                connectionstyle="arc3,rad=-0.25"))
    fig.text(0.5, 0.995, "Five-metric tradeoff: only calibration collapses",
             ha="center", va="bottom", fontsize=12.5, fontweight="bold", color=INK)
    fig.text(0.5, 0.955, "Mean over all runs, normalised per metric so the outer ring is always better",
             ha="center", va="bottom", fontsize=9, color=MUTED)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=4,
              columnspacing=1.3, handletextpad=0.5, labelcolor=BODY)
    _save(fig, "g1_radar")


def g2_violin():
    """Violins + raw runs + mean with 95% CI; Wilcoxon p annotated in place."""
    conds = ["E0_none", "E1_smote", "E1_ros", "E1_rus", "E2_cw",
             "E3_smote_platt", "E3_smote_iso"]
    data = [D[D.condition == c].ece.values for c in conds]
    fig, ax = plt.subplots(figsize=(8.6, 4.9))
    parts = ax.violinplot(data, showmeans=False, showextrema=False, widths=0.8)
    for pc, c in zip(parts["bodies"], conds):
        pc.set_facecolor(CC[c]); pc.set_alpha(0.10)
        pc.set_edgecolor(CC[c]); pc.set_linewidth(1.2)
    rng = np.random.default_rng(0)
    for i, (d, c) in enumerate(zip(data, conds)):
        x = rng.normal(i + 1, 0.05, size=len(d))
        ax.scatter(x, d, s=7, color=CC[c], alpha=0.40, ec="none", zorder=3)
        ci = 1.96 * d.std(ddof=1) / np.sqrt(len(d))
        ax.errorbar([i + 1], [d.mean()], yerr=[ci], fmt="D", ms=5.5,
                    color=CC[c], mec="white", mew=1.2, capsize=3.5,
                    elinewidth=1.4, zorder=5)
    base_mean = data[0].mean()
    ax.axhline(base_mean, color=MUTED, ls=(0, (4, 3)), lw=0.9, zorder=1)
    ax.text(0.52, base_mean + 0.006, "baseline mean", fontsize=8, color=MUTED)
    # paired tests, annotated where the reader is already looking
    p_rus = wilcoxon_p("E1_rus", "E0_none")
    d_rus = cliffs_delta(PIV["E1_rus"].values, PIV["E0_none"].values)
    p_iso = wilcoxon_p("E3_smote_iso", "E1_smote")
    ax.text(4, max(data[3]) + 0.022, f"vs Base: {fmt_p(p_rus)}, "
            rf"Cliff's $\delta$={d_rus:.2f}", ha="center", fontsize=8.2,
            color=BODY)
    ax.text(7, max(data[6]) + 0.022, f"vs SMOTE: {fmt_p(p_iso)}",
            ha="center", fontsize=8.2, color=BODY)
    ax.set_xticks(range(1, len(conds) + 1))
    ax.set_xticklabels([CL[c] for c in conds], color=INK)
    ax.set_ylabel("Expected Calibration Error")
    ax.set_ylim(-0.015, 0.54)
    _despine(ax)
    ax.grid(axis="y", color=GRID, lw=0.9); ax.set_axisbelow(True)
    ax.tick_params(axis="x", length=0)
    _titles(ax, "ECE spreads wide under undersampling, tight after recalibration",
            f"n = {N_RUNS} runs (5 datasets × 2 models × 10 seeds) per "
            "condition; diamonds: mean ± 95% CI; paired Wilcoxon signed-rank")
    _save(fig, "g2_violin")


def wilcoxon_p(cond_a, cond_b):
    from scipy.stats import wilcoxon
    return wilcoxon(PIV[cond_a].values, PIV[cond_b].values).pvalue


def _dodge(pairs, min_gap):
    """pairs: [(key, y)] -> {key: label_y} pushed apart top-down."""
    out = {}
    prev = None
    for k, v in sorted(pairs, key=lambda t: -t[1]):
        y = v if prev is None else min(v, prev - min_gap)
        out[k] = y; prev = y
    return out


def g3_slope():
    """Slope chart: per-dataset ECE, SMOTE -> +isotonic, with mean callout."""
    order = ["pima", "credit_g", "phoneme", "adult", "yeast_ml8"]
    before = D[D.condition == "E1_smote"].groupby("dataset").ece.mean()
    after = D[D.condition == "E3_smote_iso"].groupby("dataset").ece.mean()
    fig, ax = plt.subplots(figsize=(6.2, 4.9))
    yl = _dodge([(d, before[d]) for d in order], 0.0052)
    yr = _dodge([(d, after[d]) for d in order], 0.0052)
    for ds in order:
        b, a = before[ds], after[ds]
        ax.plot([0, 1], [b, a], "-", color=DS_C[ds], lw=1.9, alpha=0.95,
                zorder=3, solid_capstyle="round")
        ax.scatter([0, 1], [b, a], s=42, color=DS_C[ds], ec="white", lw=1.3,
                   zorder=4)
        ax.text(-0.05, yl[ds], f"{DS_LAB[ds]}   {b:.3f}", ha="right",
                va="center", fontsize=9, color=INK)
        ax.text(1.05, yr[ds], f"{a:.3f}", ha="left", va="center", fontsize=9,
                color=DS_C[ds], fontweight="bold")
    mb, ma = before.mean(), after.mean()
    ax.plot([0, 1], [mb, ma], color=INK, lw=3.0, alpha=0.85, zorder=5,
            solid_capstyle="round")
    ax.scatter([0, 1], [mb, ma], s=58, color=INK, ec="white", lw=1.5, zorder=6)
    ax.annotate(f"mean {100 * (ma - mb) / mb:+.0f}%",
                xy=(0.5, (mb + ma) / 2), xytext=(0, 9),
                textcoords="offset points", ha="center", fontsize=9.5,
                fontweight="bold", color=INK)
    ax.set_xlim(-0.60, 1.42); ax.set_ylim(bottom=0)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["SMOTE\n(uncalibrated)", "SMOTE\n+ isotonic"],
                       fontsize=10, color=INK)
    ax.set_ylabel("Expected Calibration Error")
    _despine(ax, keep=("left",))
    ax.grid(axis="y", color=GRID, lw=0.9); ax.set_axisbelow(True)
    ax.tick_params(axis="x", length=0)
    _titles(ax, "One calibration step pulls every dataset down",
            "Mean ECE per dataset before/after isotonic recalibration; "
            "black line: grand mean")
    _save(fig, "g3_slope")


def g4_bubble():
    """Bubble: imbalance ratio (log x) vs ECE inflation under RUS; area = n."""
    base = D[D.condition == "E0_none"].groupby(["dataset", "ir"]).ece.mean()
    rus = D[D.condition == "E1_rus"].groupby(["dataset", "ir"]).ece.mean()
    fig, ax = plt.subplots(figsize=(8.0, 5.4))
    lab_at = {"pima": (1.56, 0.095), "credit_g": (1.78, 0.150),
              "phoneme": (2.72, 0.022), "adult": (4.1, 0.158),
              "yeast_ml8": (22, 0.428)}
    for (ds, ir) in base.index:
        infl = rus[(ds, ir)] - base[(ds, ir)]
        sz = 140 + (N[ds] ** 0.5) * 6.0
        ax.scatter(ir, infl, s=sz, color=DS_C[ds], alpha=0.55, ec="white",
                   lw=1.8, zorder=3)
        lx, ly = lab_at[ds]
        ax.annotate(f"{DS_LAB[ds]}  (n={N[ds]:,})", xy=(ir, infl),
                    xytext=(lx, ly), fontsize=8.7, color=INK,
                    fontweight="bold", ha="left", va="center",
                    arrowprops=dict(arrowstyle="-", color=DS_C[ds], lw=1.0,
                                    alpha=0.7,
                                    connectionstyle="arc3,rad=0.15"))
    # bubble-area key drawn by hand (a legend box can't space unequal circles)
    ax.text(0.045, 0.975, "dataset size n", transform=ax.transAxes,
            fontsize=8.5, color=INK, va="top")
    for n_ref, lab, ky in [(1000, "1k", 0.905), (10000, "10k", 0.815),
                           (50000, "50k", 0.675)]:
        ax.scatter([0.085], [ky], transform=ax.transAxes,
                   s=140 + (n_ref ** 0.5) * 6.0, facecolor="none",
                   edgecolor=MUTED, lw=1.0, zorder=6, clip_on=False)
        ax.text(0.155, ky, lab, transform=ax.transAxes, fontsize=8,
                color=BODY, va="center")
    ax.set_xscale("log")
    ax.set_xlim(1.5, 130); ax.set_ylim(-0.02, 0.46)
    ax.set_xlabel("Imbalance ratio (log scale)")
    ax.set_ylabel("ECE inflation under undersampling")
    _despine(ax)
    ax.grid(color=GRID, lw=0.9); ax.set_axisbelow(True)
    _titles(ax, "Undersampling damage scales with imbalance",
            r"Bubble area $\propto$ dataset size; y = mean ECE(RUS) "
            r"$-$ mean ECE(baseline) per dataset")
    _save(fig, "g4_bubble")


def g5_diverge():
    """Diverging bars: ECE delta vs baseline, per model family, value labels."""
    conds = ["E1_smote", "E1_ros", "E1_rus", "E2_cw", "E3_smote_platt",
             "E3_smote_iso"]
    out = {}
    for mdl in ["histgb", "rf"]:
        sub = D[D.model == mdl]
        base = sub[sub.condition == "E0_none"].ece.mean()
        out[mdl] = np.array([sub[sub.condition == c].ece.mean() - base
                             for c in conds])
    idx = np.argsort(out["histgb"])[::-1]  # damage on top, repair at bottom
    conds = [conds[i] for i in idx]
    hg, rf = out["histgb"][idx], out["rf"][idx]
    y = np.arange(len(conds)); h = 0.36
    c_hg, c_rf = OKABE_ITO["orange"], OKABE_ITO["blue"]
    fig, ax = plt.subplots(figsize=(7.8, 4.9))
    ax.barh(y - h / 2, hg, height=h, color=c_hg, label="Gradient boosting",
            zorder=3)
    ax.barh(y + h / 2, rf, height=h, color=c_rf, label="Random forest",
            zorder=3)
    for yy, v, col in [*zip(y - h / 2, hg, [c_hg] * 6),
                       *zip(y + h / 2, rf, [c_rf] * 6)]:
        ax.text(v + (0.004 if v >= 0 else -0.004), yy, f"{v:+.3f}",
                ha="left" if v >= 0 else "right", va="center", fontsize=7.8,
                color=col)
    ax.axvline(0, color=INK, lw=1.2)
    ax.set_yticks(y); ax.set_yticklabels([CL[c] for c in conds], color=INK)
    ax.set_xlabel("Δ ECE vs. baseline   (← improves      degrades →)")
    ax.set_xlim(-0.078, 0.215)
    _despine(ax, keep=("bottom",))
    ax.grid(axis="x", color=GRID, lw=0.9); ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.legend(loc="lower right", labelcolor=BODY)
    ax.invert_yaxis()
    _titles(ax, "Resampling harms both ensembles; recalibration helps both",
            "Mean ECE shift from each model's own baseline, sorted by damage")
    _save(fig, "g5_diverge")


def g6_heatmap():
    """Heatmap: condition x dataset mean ECE; the repair column outlined."""
    conds = ["E0_none", "E1_smote", "E1_ros", "E1_rus", "E2_cw",
             "E3_smote_platt", "E3_smote_iso"]
    order = ["pima", "credit_g", "phoneme", "adult", "yeast_ml8"]
    M = (D.groupby(["dataset", "condition"]).ece.mean().unstack()[conds]
         .reindex(order).values)
    fig, ax = plt.subplots(figsize=(7.8, 4.9))
    im = ax.imshow(M, aspect="auto", cmap=RAMP, vmin=0, vmax=0.4)
    ax.set_xticks(range(len(conds)))
    ax.set_xticklabels([CL[c] for c in conds], fontsize=9, color=INK)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([DS_LAB[d] for d in order], fontsize=9, color=INK)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks(np.arange(-.5, len(conds), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(order), 1), minor=True)
    ax.grid(which="minor", color=PAPER, lw=2.0)
    ax.tick_params(which="minor", length=0)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8.2,
                    color="white" if v > 0.22 else INK)
    iso_j = conds.index("E3_smote_iso")
    ax.add_patch(plt.Rectangle((iso_j - 0.5, -0.5), 1, len(order), fill=False,
                               ec=OKABE_ITO["bluish_green"], lw=2.0, zorder=5))
    ax.text(iso_j, -0.72, "repair", ha="center", fontsize=8.5,
            color=OKABE_ITO["bluish_green"], fontweight="bold")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label("Expected Calibration Error", fontsize=9, color=INK)
    cb.outline.set_visible(False); cb.ax.tick_params(length=0, labelsize=8)
    _titles(ax, "Every condition × every dataset, at a glance",
            "Mean ECE per cell (fixed scale 0–0.4); darker means worse "
            "calibration")
    _save(fig, "g6_heatmap")


def g7_ridge():
    """Ridgeline: ECE density per condition, white median ticks."""
    from scipy.stats import gaussian_kde
    conds = ["E3_smote_iso", "E3_smote_platt", "E0_none", "E2_cw",
             "E1_smote", "E1_ros", "E1_rus"]
    fig, ax = plt.subplots(figsize=(7.8, 5.2))
    xs = np.linspace(0, 0.55, 300); gap = 0.85
    for i, c in enumerate(conds):
        d = D[D.condition == c].ece.values
        dens = gaussian_kde(d, bw_method=0.35)(xs)
        dens = dens / dens.max() * 0.95
        y0 = i * gap
        ax.fill_between(xs, y0, y0 + dens, color=CC[c], alpha=0.55, lw=0,
                        zorder=len(conds) - i)
        ax.plot(xs, y0 + dens, color="white", lw=1.2, zorder=len(conds) - i)
        med = np.median(d)
        ax.plot([med, med], [y0, y0 + 0.17], color="white", lw=1.6,
                zorder=len(conds) + 1, solid_capstyle="butt")
        ax.text(-0.015, y0 + 0.10, CL[c], ha="right", va="bottom", fontsize=9.5,
                fontweight="bold", color=CC[c])
    ax.set_yticks([]); ax.set_xlabel("Expected Calibration Error")
    ax.set_xlim(-0.10, 0.56)
    _despine(ax, keep=("bottom",))
    _titles(ax, "ECE distribution shifts right as resampling gets aggressive",
            "Gaussian KDE (bw = 0.35) of per-run ECE; white tick marks the "
            "median of each condition")
    _save(fig, "g7_ridge")


def g8_ecdf():
    """ECDF: direct curve labels + linestyle redundancy (greyscale-safe)."""
    conds = [("E3_smote_iso", "solid", 0.30), ("E0_none", (0, (5, 2)), 0.90),
             ("E1_smote", (0, (2, 1.5)), 0.62), ("E1_rus", (0, (6, 2, 2, 2)), 0.80)]
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.axhline(0.5, color=GRID, lw=0.9, zorder=1)
    ax.text(0.492, 0.51, "median", fontsize=7.5, color=MUTED, ha="right")
    for cond, ls, qy in conds:
        d = np.sort(D[D.condition == cond].ece.values)
        y = np.arange(1, len(d) + 1) / len(d)
        ax.step(np.concatenate([[0], d]), np.concatenate([[0], y]),
                where="post", lw=2.2, color=CC[cond], ls=ls, zorder=3,
                solid_capstyle="round")
        med = np.median(d)
        ax.scatter([med], [0.5], s=46, color=CC[cond], ec="white", lw=1.4,
                   zorder=4)
        xq = np.quantile(d, qy)
        ax.text(min(xq, 0.46) + 0.010, qy, CL[cond], color=CC[cond],
                fontsize=9.5, fontweight="bold", va="center", zorder=5)
    ax.set_xlabel("Expected Calibration Error")
    ax.set_ylabel("Cumulative fraction of runs")
    ax.set_xlim(0, 0.5); ax.set_ylim(0, 1.02)
    _despine(ax)
    ax.grid(color=GRID, lw=0.9); ax.set_axisbelow(True)
    _titles(ax, "Cumulative ECE: the undersampling curve sits far to the right",
            f"n = {N_RUNS} runs per condition; dots mark medians; line "
            "styles stay legible in greyscale")
    _save(fig, "g8_ecdf")


def g9_lollipop():
    """Lollipop: datasets ranked by ECE inflation under undersampling."""
    base = D[D.condition == "E0_none"].groupby("dataset").ece.mean()
    rus = D[D.condition == "E1_rus"].groupby("dataset").ece.mean()
    infl = (rus - base).sort_values()
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    cols = [RAMP(0.30 + 0.55 * i / (len(infl) - 1)) for i in range(len(infl))]
    pad = infl.max() * 0.022
    for i, (ds, v) in enumerate(infl.items()):
        ax.plot([0, v], [i, i], color=cols[i], lw=2.6, zorder=2,
                solid_capstyle="round")
        ax.scatter(v, i, s=130, color=cols[i], ec="white", lw=1.8, zorder=3)
        ax.text(v + pad, i, f"+{v:.3f}", ha="left", va="center", fontsize=8.7,
                fontweight="bold", color=cols[i], zorder=4)
    ax.set_yticks(range(len(infl)))
    ax.set_yticklabels([DS_LAB[d] for d in infl.index], fontsize=10, color=INK)
    ax.set_xlabel("ECE inflation under undersampling (vs. baseline mean)")
    ax.set_xlim(0, infl.max() * 1.30)
    _despine(ax, keep=("bottom",))
    ax.grid(axis="x", color=GRID, lw=0.9); ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    _titles(ax, "Which datasets suffer most? Ranked by calibration damage",
            "Difference in mean ECE, undersampling minus baseline; colour "
            "follows rank")
    _save(fig, "g9_lollipop")


if __name__ == "__main__":
    greys = {CL[c]: to_grayscale(CC[c]) for c in CC}
    print(f"setup ok  font={_SANS}  rows={len(D)}  paired runs={N_RUNS}")
    print(f"okabe-ito mapping: " + ", ".join(f"{k}={CC[k]}" for k in CC))
    print(f"greyscale check (distinct luma per condition): {greys}")
    g1_radar(); g2_violin(); g3_slope(); g4_bubble(); g5_diverge()
    g6_heatmap(); g7_ridge(); g8_ecdf(); g9_lollipop()
    print("[DONE] gallery — palette/export via light-figure-drawing pipeline")
