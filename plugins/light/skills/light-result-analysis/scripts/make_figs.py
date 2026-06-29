"""make_figs.py - publication-grade matplotlib templates (Light m06).

Object-oriented matplotlib only. Every figure uses:
  * constrained_layout (no overlap, no manual tight_layout),
  * viridis / colorblind-safe palettes (never jet),
  * explicit error bars (std or 95% CI),
  * vector + raster export at dpi=300 (PDF/SVG/PNG).

Provides reusable builders:
  grouped_bar_ci(...)  - method comparison bars with CI whiskers
  box_strip(...)       - distribution box + jittered points per group
  line_with_band(...)  - learning/scaling curve with shaded CI band
  heatmap(...)         - confusion / correlation matrix, viridis

Usage as library: import the functions, pass a matplotlib Axes or let it make one.
Run standalone:  python make_figs.py   -> writes demo_figure.png/.pdf/.svg
"""
import os
import sys
import tempfile
import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless-safe
import matplotlib.pyplot as plt

# --- house style: applied on import, conservative & publication-friendly ------
plt.rcParams.update({
    "figure.dpi": 120, "savefig.dpi": 300,
    "font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.3, "grid.linewidth": 0.5,
    "legend.frameon": False, "figure.constrained_layout.use": True,
})


def _colors(n, cmap="viridis"):
    return plt.get_cmap(cmap)(np.linspace(0.1, 0.9, n))


def save_all(fig, path_noext, formats=("png", "pdf", "svg")):
    """Save one figure to several formats at dpi 300, tight bbox."""
    out = []
    for fmt in formats:
        p = f"{path_noext}.{fmt}"
        fig.savefig(p, dpi=300, bbox_inches="tight")
        out.append(p)
    return out


def grouped_bar_ci(labels, means, errs, ax=None, ylabel="metric", title=None,
                   err_label="95% CI", cmap="viridis"):
    """Bar chart with error bars. errs may be scalar-per-bar (symmetric) or
    a (2, n) array for asymmetric (low, high) half-widths."""
    if ax is None:
        _, ax = plt.subplots(figsize=(4.2, 3.0))
    x = np.arange(len(labels))
    cols = _colors(len(labels), cmap)
    ax.bar(x, means, yerr=errs, capsize=4, color=cols, edgecolor="black",
           linewidth=0.6, error_kw={"elinewidth": 1.0, "ecolor": "0.25"})
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=0)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.margins(y=0.12)
    ax.text(0.99, 0.02, f"err = {err_label}", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=7, color="0.4")
    return ax


def box_strip(groups, data, ax=None, ylabel="metric", title=None, cmap="viridis"):
    """Box plot + jittered raw points per group (shows distribution, not just mean)."""
    if ax is None:
        _, ax = plt.subplots(figsize=(4.2, 3.0))
    cols = _colors(len(groups), cmap)
    bp = ax.boxplot(data, positions=np.arange(len(groups)), widths=0.5,
                    patch_artist=True, showfliers=False)
    for patch, c in zip(bp["boxes"], cols):
        patch.set_facecolor(c); patch.set_alpha(0.5)
    for med in bp["medians"]:
        med.set_color("black")
    rng = np.random.default_rng(0)
    for i, d in enumerate(data):
        jit = rng.normal(0, 0.06, len(d))
        ax.scatter(np.full(len(d), i) + jit, d, s=14, color=cols[i],
                   edgecolor="black", linewidth=0.4, zorder=3)
    ax.set_xticks(np.arange(len(groups))); ax.set_xticklabels(groups)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    return ax


def line_with_band(x, ys, ax=None, labels=None, xlabel="x", ylabel="y",
                   title=None, cmap="viridis"):
    """Mean line with shaded CI band per series. ys: list of (n_runs, n_x) arrays."""
    if ax is None:
        _, ax = plt.subplots(figsize=(4.4, 3.0))
    cols = _colors(len(ys), cmap)
    for i, Y in enumerate(ys):
        Y = np.asarray(Y, float)
        mean = Y.mean(0)
        se = Y.std(0, ddof=1) / np.sqrt(Y.shape[0])
        ci = 1.96 * se
        lab = labels[i] if labels else f"series {i}"
        ax.plot(x, mean, color=cols[i], label=lab, linewidth=1.6)
        ax.fill_between(x, mean - ci, mean + ci, color=cols[i], alpha=0.2)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.legend()
    return ax


def heatmap(matrix, ax=None, xticks=None, yticks=None, title=None,
            cmap="viridis", annot=True, cbar_label="value"):
    """Confusion/correlation heatmap with optional cell annotations."""
    if ax is None:
        _, ax = plt.subplots(figsize=(3.8, 3.2))
    M = np.asarray(matrix, float)
    im = ax.imshow(M, cmap=cmap, aspect="auto")
    cb = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(cbar_label)
    if xticks is not None:
        ax.set_xticks(range(len(xticks))); ax.set_xticklabels(xticks, rotation=45, ha="right")
    if yticks is not None:
        ax.set_yticks(range(len(yticks))); ax.set_yticklabels(yticks)
    if annot:
        thr = (M.max() + M.min()) / 2
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                        color="white" if M[i, j] < thr else "black", fontsize=8)
    if title:
        ax.set_title(title)
    ax.grid(False)
    return ax


def demo(outdir=None):
    """Build a 2x2 publication-style panel from synthetic data and export it."""
    outdir = outdir or os.path.dirname(os.path.abspath(__file__))
    rng = np.random.default_rng(3)
    methods = ["baseline", "ablation", "ours"]
    samples = [rng.normal(m, 0.025, 8) for m in (0.80, 0.83, 0.86)]
    means = [s.mean() for s in samples]
    errs = [1.96 * s.std(ddof=1) / np.sqrt(len(s)) for s in samples]

    fig, axes = plt.subplots(2, 2, figsize=(8.2, 6.0))
    grouped_bar_ci(methods, means, errs, ax=axes[0, 0],
                   ylabel="accuracy", title="(a) Mean accuracy +/- 95% CI")
    box_strip(methods, samples, ax=axes[0, 1],
              ylabel="accuracy", title="(b) Per-seed distribution")
    x = np.arange(1, 11)
    curves = [rng.normal(np.linspace(0.6, base, 10), 0.01, (6, 10))
              for base in (0.80, 0.86)]
    line_with_band(x, curves, ax=axes[1, 0], labels=["baseline", "ours"],
                   xlabel="epoch", ylabel="val acc", title="(c) Learning curves +/- CI")
    cm = np.array([[0.92, 0.05, 0.03], [0.08, 0.86, 0.06], [0.04, 0.10, 0.86]])
    heatmap(cm, ax=axes[1, 1], xticks=["A", "B", "C"], yticks=["A", "B", "C"],
            title="(d) Norm. confusion", cbar_label="rate")
    fig.suptitle("Publication-grade figure template (viridis, CI, dpi=300)", fontsize=12)
    paths = save_all(fig, os.path.join(outdir, "demo_figure"))
    plt.close(fig)
    return paths



def _selftest() -> int:
    with tempfile.TemporaryDirectory(prefix="light_make_figs_") as tmp:
        paths = demo(tmp)
        assert len(paths) == 3, paths
        for path in paths:
            assert os.path.exists(path) and os.path.getsize(path) > 0, path
    print("[selftest] PASS make_figs")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] != "--selftest":
            raise SystemExit("usage: python make_figs.py [--selftest]")
        raise SystemExit(_selftest())
    paths = demo()
    for p in paths:
        print("wrote", p)
    print("DONE")


