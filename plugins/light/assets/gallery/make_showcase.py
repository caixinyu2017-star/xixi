"""门面画廊：9 种顶刊高级图型的视觉能力秀（合成演示数据，可一键复现）。

定位与诚信边界（与案例项目九图分工明确）：
  - 本画廊回答"Light 的图表流水线能画出什么水平的图"——图型对标顶刊
    （alluvial / chord / raincloud / volcano / embedding / streamgraph /
    polar heatmap / ridgeline / Kaplan-Meier）。
  - 数据**全部为脚本内固定种子合成**，只作视觉演示，不指向任何真实研究；
    每张图右下角印 "synthetic demo data" 角注，README 同步声明。
  - 真实端到端案例（所有数字来自真跑实验）见
    projects/resampling-calibration-study/，两者互不冒充。

视觉层吃自家流水线（dogfooding）：
  - 配色  light-figure-drawing/scripts/color_palettes.py — Okabe-Ito 色盲安全
    离散色 + sequential_cmap/diverging_cmap 连续色板。
  - 导出  light-figure-drawing/scripts/figure_export.py —
    save_publication_figure()（fonttype 42、300 dpi、紧边距）。

用法：python assets/gallery/make_showcase.py   # 在 assets/gallery/ 落 9 张 PNG
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patheffects as pe
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch, FancyBboxPatch
from scipy.stats import gaussian_kde

HERE = Path(__file__).resolve().parent          # assets/gallery
LIGHT = HERE.parents[1]                          # 仓库根
sys.path.insert(0, str(LIGHT / "skills" / "light-figure-drawing" / "scripts"))
from color_palettes import OKABE_ITO, sequential_cmap, diverging_cmap  # noqa: E402
from figure_export import save_publication_figure                      # noqa: E402

# ---------------------------------------------------------------- 视觉基调
INK, BODY, MUTED, GRID = "#1A1A1A", "#3B3B3B", "#7A7A7A", "#E8E8E8"
OI = OKABE_ITO
_avail = {f.name for f in fm.fontManager.ttflist}
_SANS = next((f for f in ["Arial", "Helvetica", "Segoe UI", "Calibri",
                          "Liberation Sans", "DejaVu Sans"] if f in _avail),
             "sans-serif")
plt.rcParams.update({
    "font.family": _SANS, "text.color": BODY,
    "axes.edgecolor": MUTED, "axes.labelcolor": BODY, "axes.linewidth": 0.8,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
    "axes.labelsize": 9.5, "figure.facecolor": "white",
})


def header(fig, title, subtitle):
    fig.text(0.045, 0.965, title, fontsize=14, fontweight="bold",
             color=INK, ha="left", va="top")
    fig.text(0.045, 0.918, subtitle, fontsize=9, color=MUTED,
             ha="left", va="top")


def footer(fig):
    fig.text(0.985, 0.012, "Light · m11 figure pipeline — synthetic demo data",
             fontsize=6.2, color="#ABABAB", ha="right", va="bottom")


def save(fig, name):
    save_publication_figure(fig, str(HERE / name), formats=("png",),
                            dpi=300, close=True)
    print(f"  saved {name}.png")


def despine(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


# ============================================================ s1 alluvial
def s1_alluvial():
    """三段冲积图：化合物筛选漏斗（药物发现叙事）。"""
    rng = np.random.default_rng(11)
    stages = [
        ("Library", [("Natural products", 420), ("Synthetic", 760),
                     ("Repurposed", 240), ("In-silico hits", 380)]),
        ("Primary screen", [("Active", 510), ("Marginal", 430), ("Inactive", 860)]),
        ("Validation", [("Confirmed leads", 285), ("Not reproduced", 225),
                        ("Dropped", 1290)]),
    ]
    src_colors = [OI["blue"], OI["orange"], OI["bluish_green"], OI["reddish_purple"]]
    # 流量矩阵（合成但行列和自洽）
    f01 = np.array([[180, 130, 110], [210, 190, 360], [60, 60, 120], [60, 50, 270]])
    f12 = np.array([[225, 120, 165], [60, 105, 265], [0, 0, 860]])

    fig = plt.figure(figsize=(7.6, 5.2))
    ax = fig.add_axes([0.05, 0.06, 0.9, 0.78]); ax.axis("off")
    xs, w, gap = [0.0, 0.42, 0.84], 0.055, 0.018
    total = sum(v for _, v in stages[0][1])
    geo = []  # 每段每节点 (y0, y1)
    for si, (sname, nodes) in enumerate(stages):
        ssum = sum(v for _, v in nodes)
        scale = (1 - gap * (len(nodes) - 1)) / total
        y = 1.0
        seg = []
        for ni, (nname, v) in enumerate(nodes):
            h = v * scale * (total / ssum if si else 1)
            h = v * scale
            seg.append((y - h, y))
            color = src_colors[ni] if si == 0 else "#43506B"
            ax.add_patch(FancyBboxPatch((xs[si], y - h), w, h,
                         boxstyle="round,pad=0,rounding_size=0.008",
                         fc=color, ec="none", zorder=5))
            ax.text(xs[si] + (w + 0.012 if si < 2 else -0.012),
                    y - h / 2, f"{nname}\n{v:,}",
                    ha="left" if si < 2 else "right", va="center",
                    fontsize=8, color=INK, zorder=6,
                    path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
            y -= h + gap
        geo.append(seg)
        ax.text(xs[si] + w / 2, 1.045, sname, ha="center", fontsize=9.5,
                fontweight="bold", color=BODY)

    def ribbon(x0, x1, a0, a1, b0, b1, color, alpha):
        xm = (x0 + x1) / 2
        verts = [(x0, a1), (xm, a1), (xm, b1), (x1, b1), (x1, b0),
                 (xm, b0), (xm, a0), (x0, a0), (x0, a1)]
        codes = [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
                 MplPath.LINETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
                 MplPath.CLOSEPOLY]
        ax.add_patch(PathPatch(MplPath(verts, codes), fc=color, ec="none",
                               alpha=alpha, zorder=2))

    for flows, si in ((f01, 0), (f12, 1)):
        outs = [list(geo[si][i]) for i in range(flows.shape[0])]
        ins = [list(geo[si + 1][j]) for j in range(flows.shape[1])]
        out_top = [o[1] for o in outs]; in_top = [i[1] for i in ins]
        colsum = flows.sum(axis=0)
        for i in range(flows.shape[0]):
            h_i = geo[si][i][1] - geo[si][i][0]
            for j in range(flows.shape[1]):
                if not flows[i, j]:
                    continue
                fh_out = flows[i, j] / flows[i].sum() * h_i
                h_j = geo[si + 1][j][1] - geo[si + 1][j][0]
                fh_in = flows[i, j] / colsum[j] * h_j
                color = src_colors[i] if si == 0 else "#6B7A99"
                ribbon(xs[si] + w, xs[si + 1], out_top[i] - fh_out, out_top[i],
                       in_top[j] - fh_in, in_top[j], color, 0.42)
                out_top[i] -= fh_out; in_top[j] -= fh_in
    ax.set_xlim(-0.12, 1.0); ax.set_ylim(-0.02, 1.10)
    header(fig, "From 1,800 compounds to 285 confirmed leads",
           "Alluvial flow of a phenotypic screening campaign · ribbon width $\propto$ compound count")
    footer(fig)
    save(fig, "s1_alluvial")


# =============================================================== s2 chord
def s2_chord():
    """和弦图：跨学科合作强度。"""
    fields = ["Genomics", "AI / ML", "Imaging", "Clinical", "Chemistry",
              "Ecology", "Neuroscience"]
    colors = [OI["bluish_green"], OI["blue"], OI["sky_blue"], OI["vermillion"],
              OI["orange"], "#7A9A01", OI["reddish_purple"]]
    M = np.array([  # 对称合作矩阵（合成）
        [0, 86, 30, 52, 24, 18, 34],
        [86, 0, 74, 58, 30, 26, 66],
        [30, 74, 0, 64, 12, 8, 48],
        [52, 58, 64, 0, 22, 6, 38],
        [24, 30, 12, 22, 0, 16, 16],
        [18, 26, 8, 6, 16, 0, 6],
        [34, 66, 48, 38, 16, 6, 0],
    ], float)
    tot = M.sum(axis=1); share = tot / tot.sum()
    gap = np.deg2rad(3.2)
    spans, a = [], np.pi / 2
    for s in share:
        width = s * (2 * np.pi - gap * len(fields))
        spans.append((a, a - width)); a -= width + gap

    fig = plt.figure(figsize=(6.6, 6.4))
    ax = fig.add_axes([0.03, 0.015, 0.94, 0.86]); ax.axis("off")
    ax.set_xlim(-1.34, 1.34); ax.set_ylim(-1.3, 1.3); ax.set_aspect("equal")
    R0, R1 = 1.0, 1.07

    def arc_xy(t0, t1, r, n=40):
        t = np.linspace(t0, t1, n)
        return np.column_stack([r * np.cos(t), r * np.sin(t)])

    for (t0, t1), c, name in zip(spans, colors, fields):
        outer = arc_xy(t0, t1, R1); inner = arc_xy(t1, t0, R0)
        ax.add_patch(PathPatch(MplPath(np.vstack([outer, inner])), fc=c,
                               ec="white", lw=0.6, zorder=5))
        tm = (t0 + t1) / 2; deg = np.rad2deg(tm)
        rot = deg - 90 if -90 <= deg % 360 - 360 * (deg % 360 > 180) else deg
        rot = deg - 90
        if 90 < (deg % 360) < 270:
            rot += 180
        ax.text(1.16 * np.cos(tm), 1.16 * np.sin(tm), name, fontsize=9,
                fontweight="bold", color=c, ha="center", va="center",
                rotation=rot, rotation_mode="anchor")

    # 每段把弧长按对手方流量切片，画三次贝塞尔带
    cursors = [list(spans[i]) for i in range(len(fields))]
    drawn = set()
    order = np.dstack(np.unravel_index(np.argsort(M, axis=None)[::-1], M.shape))[0]
    for i, j in order:
        if i >= j or (i, j) in drawn or M[i, j] < 6:
            continue
        drawn.add((i, j))
        for k, other in ((i, j), (j, i)):
            w = M[k][other] / tot[k] * (spans[k][0] - spans[k][1])
            if k == i:
                ia0 = cursors[i][0]; ia1 = ia0 - w; cursors[i][0] = ia1
            else:
                ja0 = cursors[j][0]; ja1 = ja0 - w; cursors[j][0] = ja1
        p0, p1 = arc_xy(ia0, ia1, R0, 22), arc_xy(ja0, ja1, R0, 22)
        c_mix = colors[i] if tot[i] >= tot[j] else colors[j]
        verts = [tuple(p0[0])]
        codes = [MplPath.MOVETO]
        for pt in p0[1:]:
            verts.append(tuple(pt)); codes.append(MplPath.LINETO)
        verts += [(0.25 * p0[-1][0], 0.25 * p0[-1][1]),
                  (0.25 * p1[0][0], 0.25 * p1[0][1]), tuple(p1[0])]
        codes += [MplPath.CURVE4] * 3
        for pt in p1[1:]:
            verts.append(tuple(pt)); codes.append(MplPath.LINETO)
        verts += [(0.25 * p1[-1][0], 0.25 * p1[-1][1]),
                  (0.25 * p0[0][0], 0.25 * p0[0][1]), tuple(p0[0])]
        codes += [MplPath.CURVE4] * 3
        ax.add_patch(PathPatch(MplPath(verts, codes), fc=c_mix, ec="none",
                               alpha=0.40, zorder=2))
    header(fig, "Who collaborates with whom",
           "Chord diagram of cross-disciplinary co-authorship · ribbon width $\propto$ joint papers")
    footer(fig)
    save(fig, "s2_chord")


# =========================================================== s3 raincloud
def s3_raincloud():
    """雨云图：四种干预下的响应分布（半小提琴 + 箱线 + 抖动散点）。"""
    rng = np.random.default_rng(7)
    groups = [("Control", 52.0, 9.5, OI["blue"]),
              ("Drug A", 58.5, 8.0, OI["orange"]),
              ("Drug B", 63.0, 11.0, OI["bluish_green"]),
              ("A + B", 71.5, 7.0, OI["vermillion"])]
    data = [np.clip(rng.normal(m, s, 90), 20, 100) for _, m, s, _ in groups]

    fig = plt.figure(figsize=(7.6, 5.2))
    ax = fig.add_axes([0.13, 0.10, 0.83, 0.74])
    for gi, ((name, m, s, c), d) in enumerate(zip(groups, data)):
        y0 = len(groups) - 1 - gi
        kde = gaussian_kde(d); xs = np.linspace(d.min() - 4, d.max() + 4, 220)
        dens = kde(xs); dens = dens / dens.max() * 0.42
        ax.fill_between(xs, y0 + 0.06, y0 + 0.06 + dens, fc=c, alpha=0.55,
                        ec=c, lw=1.1, zorder=3)
        q1, med, q3 = np.percentile(d, [25, 50, 75])
        lo = max(d.min(), q1 - 1.5 * (q3 - q1)); hi = min(d.max(), q3 + 1.5 * (q3 - q1))
        ax.plot([lo, hi], [y0, y0], color=INK, lw=1.0, zorder=4)
        ax.add_patch(plt.Rectangle((q1, y0 - 0.055), q3 - q1, 0.11, fc="white",
                                   ec=INK, lw=1.0, zorder=5))
        ax.plot([med, med], [y0 - 0.055, y0 + 0.055], color=INK, lw=1.6, zorder=6)
        jitter = y0 - 0.13 - rng.uniform(0, 0.16, len(d))
        ax.scatter(d, jitter, s=7, fc=c, ec="none", alpha=0.55, zorder=3)
        ax.text(d.mean(), y0 + 0.56, f"{name}   n=90", fontsize=9.5,
                fontweight="bold", color=c, ha="center")
    # 顶组 vs 对照的效应注释
    ax.annotate("", xy=(85, 3.30), xytext=(85, 0.30),
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
    ax.text(86.5, 1.8, "Cliff's δ = 0.86\np < 0.001 (Mann-Whitney)",
            fontsize=8.5, color=BODY, va="center")
    ax.set_xlim(18, 102); ax.set_ylim(-0.45, 3.95)
    ax.set_yticks([]); despine(ax, keep=("bottom",))
    ax.set_xlabel("Treatment response score")
    ax.xaxis.grid(True, color=GRID, lw=0.7); ax.set_axisbelow(True)
    header(fig, "Combination therapy shifts the whole distribution",
           "Raincloud: half-violin (KDE) + box + raw observations, 90 subjects per arm")
    footer(fig)
    save(fig, "s3_raincloud")


# ============================================================= s4 volcano
def s4_volcano():
    """火山图：差异表达基因。"""
    rng = np.random.default_rng(23)
    n = 2600
    lfc = rng.normal(0, 1.05, n)
    noise = rng.uniform(0, 1, n)
    p = np.exp(-np.abs(lfc) * rng.uniform(1.0, 3.4, n)) * noise + 1e-12
    sig_up = (lfc > 1) & (p < 1e-2); sig_dn = (lfc < -1) & (p < 1e-2)
    nlp = -np.log10(p)
    genes = ["FOXM1", "CDK1", "AURKA", "TOP2A", "MKI67", "CCNB1",
             "GADD45B", "SESN2", "CDKN1A", "TP53I3"]

    fig = plt.figure(figsize=(7.0, 5.4))
    ax = fig.add_axes([0.10, 0.10, 0.86, 0.74])
    ax.scatter(lfc[~(sig_up | sig_dn)], nlp[~(sig_up | sig_dn)], s=6,
               fc="#C8CDD4", ec="none", alpha=0.6, zorder=2)
    ax.scatter(lfc[sig_dn], nlp[sig_dn], s=10, fc=OI["blue"], ec="none",
               alpha=0.75, zorder=3, label=f"Down  ({sig_dn.sum()})")
    ax.scatter(lfc[sig_up], nlp[sig_up], s=10, fc=OI["vermillion"], ec="none",
               alpha=0.75, zorder=3, label=f"Up  ({sig_up.sum()})")
    ax.axhline(2, color=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1)
    ax.axvline(-1, color=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1)
    ax.axvline(1, color=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1)
    # 标注最显著基因（带细引线）
    cand = np.argsort(nlp * ((sig_up | sig_dn)))[-10:]
    offs = [(34, 8), (-44, 10), (30, 14), (-38, -6), (36, -4),
            (-30, 16), (28, 18), (-40, 4), (32, 2), (-34, -12)]
    for gi, (idx, off) in enumerate(zip(cand[::-1], offs)):
        ax.annotate(genes[gi], (lfc[idx], nlp[idx]), textcoords="offset points",
                    xytext=off, fontsize=7.8, fontstyle="italic", color=INK,
                    arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6,
                                    shrinkA=0, shrinkB=2), zorder=6)
    ax.set_xlim(-4.6, 4.6); ax.set_ylim(-0.3, nlp.max() * 1.06)
    despine(ax); ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel("log$_2$ fold change (treated vs control)")
    ax.set_ylabel("−log$_{10}$ p (adj.)")
    ax.legend(loc="lower left", frameon=True, framealpha=0.85, edgecolor="none",
              fontsize=8.5, handletextpad=0.2)
    header(fig, "Proliferation programme switches off",
           f"Volcano of {n:,} genes · thresholds |log₂FC| > 1, p < 0.01 · top hits labelled")
    footer(fig)
    save(fig, "s4_volcano")


# =========================================================== s5 embedding
def s5_embedding():
    """UMAP 风格嵌入图：单细胞群落 + 密度等高线 + 晕圈标签。"""
    rng = np.random.default_rng(5)
    spec = [("T cells", 2600, (-4.5, 2.6), (1.6, 1.0), 24, OI["blue"]),
            ("B cells", 1500, (-1.2, 5.0), (1.0, 0.8), -18, OI["bluish_green"]),
            ("NK", 800, (-6.4, 6.0), (0.8, 0.65), 12, OI["sky_blue"]),
            ("Monocytes", 2100, (3.8, 3.4), (1.5, 1.05), 40, OI["orange"]),
            ("Dendritic", 600, (6.3, 0.2), (0.75, 0.6), 0, OI["reddish_purple"]),
            ("Erythroid", 900, (1.4, -4.2), (1.15, 0.7), -30, OI["vermillion"]),
            ("Progenitors", 700, (-2.0, -1.6), (0.9, 0.9), 0, "#8C8C00")]
    fig = plt.figure(figsize=(7.0, 5.8))
    ax = fig.add_axes([0.06, 0.05, 0.9, 0.8])
    for name, n, mu, sd, ang, c in spec:
        t = np.deg2rad(ang); R = np.array([[np.cos(t), -np.sin(t)],
                                           [np.sin(t), np.cos(t)]])
        pts = rng.normal(0, 1, (n, 2)) * sd @ R.T + mu
        pts += 0.35 * np.tanh(pts[:, [1, 0]] * 0.3)  # 轻微流形弯曲
        ax.scatter(*pts.T, s=3.2, fc=c, ec="none", alpha=0.45, zorder=2)
        kde = gaussian_kde(pts.T)
        gx, gy = np.meshgrid(
            np.linspace(pts[:, 0].min() - 1, pts[:, 0].max() + 1, 70),
            np.linspace(pts[:, 1].min() - 1, pts[:, 1].max() + 1, 70))
        dens = kde(np.vstack([gx.ravel(), gy.ravel()])).reshape(gx.shape)
        ax.contour(gx, gy, dens, levels=np.percentile(dens, [72, 90]),
                   colors=[c], linewidths=0.9, alpha=0.8, zorder=3)
        ax.text(*np.median(pts, axis=0), name, fontsize=10, fontweight="bold",
                color=INK, ha="center", va="center", zorder=6,
                path_effects=[pe.withStroke(linewidth=3, foreground="white")])
    ax.set_xticks([]); ax.set_yticks([]); despine(ax, keep=())
    # UMAP 惯例的角落坐标箭头
    ax.annotate("", xy=(0.115, 0.02), xytext=(0.02, 0.02),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.annotate("", xy=(0.02, 0.135), xytext=(0.02, 0.02),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.text(0.066, 0.032, "UMAP 1", transform=ax.transAxes, fontsize=7.5,
            color=MUTED, ha="center")
    ax.text(0.030, 0.078, "UMAP 2", transform=ax.transAxes, fontsize=7.5,
            color=MUTED, rotation=90, va="center")
    header(fig, "9,200 cells resolve into seven lineages",
           "UMAP-style embedding · per-cluster KDE contours at 72nd / 90th density percentile")
    footer(fig)
    save(fig, "s5_embedding")


# ============================================================== s6 stream
def s6_stream():
    """流图：二十年研究主题占比演化。"""
    rng = np.random.default_rng(17)
    years = np.arange(2006, 2027)
    topics = [("Deep learning", OI["blue"]), ("LLM / agents", OI["vermillion"]),
              ("Causal inference", OI["bluish_green"]), ("Single-cell omics", OI["orange"]),
              ("Graph learning", OI["sky_blue"]), ("Robotics", OI["reddish_purple"]),
              ("Quantum ML", "#8C8C00")]
    base = np.array([
        np.interp(years, [2006, 2014, 2020, 2026], [8, 30, 38, 30]),
        np.interp(years, [2006, 2018, 2022, 2026], [0, 1, 14, 34]),
        np.interp(years, [2006, 2016, 2026], [4, 9, 14]),
        np.interp(years, [2006, 2015, 2021, 2026], [2, 8, 16, 13]),
        np.interp(years, [2006, 2017, 2023, 2026], [3, 7, 13, 10]),
        np.interp(years, [2006, 2026], [6, 9]),
        np.interp(years, [2006, 2019, 2026], [0.4, 2, 5]),
    ])
    base += rng.normal(0, 0.5, base.shape)
    k = np.array([0.15, 0.45, 0.8, 0.45, 0.15]); k /= k.sum()
    smooth = np.array([np.convolve(np.pad(r, 2, mode="edge"), k, "valid")
                       for r in np.clip(base, 0.2, None)])
    fig = plt.figure(figsize=(7.8, 5.0))
    ax = fig.add_axes([0.03, 0.09, 0.83, 0.75])
    polys = ax.stackplot(years, smooth, baseline="wiggle",
                         colors=[c for _, c in topics], alpha=0.88,
                         edgecolor="white", linewidth=1.0)
    for poly, (name, c) in zip(polys, topics):  # 右缘直标
        verts = poly.get_paths()[0].vertices
        right = verts[np.isclose(verts[:, 0], years[-1])]
        ymid = right[:, 1].mean()
        ax.annotate(name, (years[-1], ymid), xytext=(8, 0),
                    textcoords="offset points", fontsize=9, fontweight="bold",
                    color=c, va="center")
    ax.set_yticks([]); despine(ax, keep=("bottom",))
    ax.set_xlim(years[0], years[-1] + 0.2)
    ax.set_xticks(np.arange(2006, 2027, 4))
    header(fig, "Twenty years of method fashion",
           "Streamgraph of topic share in published papers, 2006–2026 · band height $\propto$ share")
    footer(fig)
    save(fig, "s6_stream")


# ============================================================= s7 circos
def s7_polar_heatmap():
    """极坐标热图：物种活动的昼夜 × 季节节律。"""
    rng = np.random.default_rng(3)
    hours = np.arange(25); months = np.arange(13)
    H, Mo = np.meshgrid(hours[:-1] + 0.5, months[:-1] + 0.5)
    dawn = 6.5 + 1.8 * np.sin((Mo - 3) / 12 * 2 * np.pi)
    dusk = 18.5 - 1.8 * np.sin((Mo - 3) / 12 * 2 * np.pi)
    act = (np.exp(-((H - dawn) ** 2) / 3.2) + np.exp(-((H - dusk) ** 2) / 3.2)
           + 0.18 * np.exp(-((H - 13) ** 2) / 18))
    act *= 1 + 0.35 * np.sin((Mo - 5) / 12 * 2 * np.pi)
    act += rng.normal(0, 0.035, act.shape)
    theta = hours / 24 * 2 * np.pi
    fig = plt.figure(figsize=(6.8, 6.2))
    ax = fig.add_axes([0.06, 0.018, 0.88, 0.83], projection="polar")
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
    qm = ax.pcolormesh(theta, months + 2, act, cmap=sequential_cmap(),
                       edgecolors="white", linewidth=0.4, shading="flat")
    ax.set_xticks(np.arange(0, 24, 3) / 24 * 2 * np.pi)
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 3)], fontsize=8)
    ax.set_yticks([]); ax.spines["polar"].set_visible(False)
    ax.set_ylim(0, 15)
    for m, lab in [(2.5, "Jan"), (8.5, "Jul"), (14.5, "Dec")]:
        ax.text(np.deg2rad(2), m, lab, fontsize=7.2, color=MUTED,
                ha="left", va="center",
                path_effects=[pe.withStroke(linewidth=2, foreground="white")])
    cax = fig.add_axes([0.30, 0.075, 0.4, 0.022])
    cb = fig.colorbar(qm, cax=cax, orientation="horizontal")
    cb.set_label("Detections per camera-hour", fontsize=8, color=BODY)
    cb.ax.tick_params(labelsize=7.5); cb.outline.set_visible(False)
    header(fig, "Crepuscular, and more so in summer",
           "Polar heatmap of camera-trap activity · rings = months (inner Jan → outer Dec), angle = hour")
    footer(fig)
    save(fig, "s7_polar_heatmap")


# =========================================================== s8 ridgeline
def s8_ridgeline():
    """山脊图：12 项研究的效应量后验分布（贝叶斯 meta 叙事）。"""
    rng = np.random.default_rng(29)
    mus = np.sort(rng.uniform(-0.05, 0.78, 12))[::-1]
    sds = rng.uniform(0.06, 0.16, 12)
    cmap = sequential_cmap(colors=("#FFE8C7", "#FC8D59", "#7F1D1D"))
    fig = plt.figure(figsize=(7.0, 5.8))
    ax = fig.add_axes([0.16, 0.09, 0.78, 0.75])
    xs = np.linspace(-0.55, 1.25, 500)
    for i, (mu, sd) in enumerate(zip(mus, sds)):
        y0 = -i * 0.62
        dens = np.exp(-0.5 * ((xs - mu) / sd) ** 2)
        dens = dens / dens.max() * 1.15
        c = cmap((mu - mus.min()) / (mus.max() - mus.min()))
        ax.fill_between(xs, y0, y0 + dens, fc=c, alpha=0.92, ec="white",
                        lw=1.4, zorder=20 - i)
        lo, hi = mu - 1.96 * sd, mu + 1.96 * sd
        ax.text(-0.60, y0 + 0.05, f"Study {chr(65 + i)}", fontsize=8.6,
                ha="right", color=BODY, zorder=30)
        ax.text(1.29, y0 + 0.05, f"{mu:.2f} [{lo:.2f}, {hi:.2f}]", fontsize=7.8,
                ha="left", color=MUTED, zorder=30)
    ax.axvline(0, color=INK, lw=1.0, ls=(0, (4, 3)), zorder=25)
    ax.text(0, 1.55, "null", fontsize=8, color=INK, ha="center")
    ax.set_ylim(-7.2, 1.9); ax.set_xlim(-1.05, 1.75)
    ax.set_yticks([]); despine(ax, keep=("bottom",))
    ax.set_xticks([-0.5, 0, 0.5, 1.0])
    ax.set_xlabel("Standardised effect size (posterior)")
    header(fig, "Eleven of twelve posteriors clear zero",
           "Ridgeline of per-study effect-size posteriors · colour $\propto$ posterior mean · 95% CrI at right")
    footer(fig)
    save(fig, "s8_ridgeline")


# ================================================================= s9 KM
def s9_km():
    """Kaplan-Meier 生存曲线：三臂 + 置信带 + 删失刻度 + at-risk 表。"""
    rng = np.random.default_rng(41)
    arms = [("Combination", 0.018, OI["bluish_green"], 160),
            ("Monotherapy", 0.032, OI["blue"], 160),
            ("Control", 0.052, OI["vermillion"], 158)]

    def km(times, events):
        order = np.argsort(times); t, e = times[order], events[order]
        uniq = np.unique(t[e == 1])
        s, var_acc, surv, var = 1.0, 0.0, [(0, 1.0, 0.0)], None
        for u in uniq:
            n_at = (t >= u).sum(); d = ((t == u) & (e == 1)).sum()
            s *= 1 - d / n_at
            var_acc += d / (n_at * (n_at - d) + 1e-12)
            surv.append((u, s, 1.96 * s * np.sqrt(var_acc)))
        return np.array(surv)

    fig = plt.figure(figsize=(7.2, 5.8))
    ax = fig.add_axes([0.10, 0.30, 0.86, 0.55])
    times_all, events_all, labels_all = [], [], []
    risk_rows = []
    for name, haz, c, n in arms:
        t = rng.exponential(1 / haz, n)
        cens = rng.uniform(18, 42, n)
        obs = np.minimum(t, cens); ev = (t <= cens).astype(int)
        obs = np.clip(obs, 0, 36)
        ev[obs >= 36] = 0
        curve = km(obs, ev)
        ts = np.append(curve[:, 0], 36); ss = np.append(curve[:, 1], curve[-1, 1])
        cis = np.append(curve[:, 2], curve[-1, 2])
        ax.step(ts, ss, where="post", color=c, lw=2.0, zorder=4, label=name)
        ax.fill_between(ts, np.clip(ss - cis, 0, 1), np.clip(ss + cis, 0, 1),
                        step="post", fc=c, alpha=0.13, zorder=2)
        ct = obs[ev == 0]; ct = ct[ct < 36]
        cs = np.interp(ct, ts, ss)
        sub = slice(None, None, 3)  # 删失刻度抽稀
        ax.plot(ct[sub], cs[sub], "|", color=c, ms=7, mew=1.1, zorder=5)
        med = ts[np.searchsorted(-ss, -0.5)] if ss.min() < 0.5 else None
        if med is not None and med < 36:
            ax.plot([med, med], [0, 0.5], color=c, lw=0.8, ls=(0, (2, 3)), zorder=3)
        risk_rows.append((name, c, [int(((obs >= m)).sum()) for m in (0, 6, 12, 18, 24, 30, 36)]))
        times_all.append(obs); events_all.append(ev); labels_all.append(name)
    ax.axhline(0.5, color=MUTED, lw=0.7, ls=(0, (2, 3)), zorder=1)
    ax.set_xlim(0, 36.5); ax.set_ylim(0, 1.02)
    ax.set_ylabel("Progression-free survival")
    ax.set_xticks(np.arange(0, 37, 6)); ax.set_xticklabels([])
    despine(ax); ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.text(35.6, 0.62, "log-rank χ² = 38.4\np < 0.0001", fontsize=8.5,
            ha="right", color=BODY)
    # at-risk 表
    for ri, (name, c, counts) in enumerate(risk_rows):
        y = 0.205 - ri * 0.052
        fig.text(0.095, y, name, fontsize=8, color=c, ha="right",
                 fontweight="bold")
        for mi, m in enumerate((0, 6, 12, 18, 24, 30, 36)):
            fig.text(0.10 + 0.86 * (m / 36.5) + 0.012, y, str(counts[mi]),
                     fontsize=8, color=BODY, ha="center")
    fig.text(0.095, 0.255, "No. at risk", fontsize=8, color=MUTED, ha="right")
    fig.text(0.53, 0.085, "Months since randomisation", fontsize=9.5,
             color=BODY, ha="center")
    for m in (0, 6, 12, 18, 24, 30, 36):
        fig.text(0.10 + 0.86 * (m / 36.5) + 0.012, 0.255, str(m), fontsize=8,
                 color=MUTED, ha="center")
    header(fig, "Median PFS doubles under the combination",
           "Kaplan-Meier with 95% CI bands, censoring ticks and number-at-risk table · 478 patients")
    footer(fig)
    save(fig, "s9_km")


if __name__ == "__main__":
    print("rendering showcase gallery (synthetic demo data) ...")
    s1_alluvial(); s2_chord(); s3_raincloud(); s4_volcano(); s5_embedding()
    s6_stream(); s7_polar_heatmap(); s8_ridgeline(); s9_km()
    print("done -> assets/gallery/")
