# -*- coding: utf-8 -*-
"""The four figures of the manuscript.

Figures 1 and 2 are schematic: the deployment context of the assessment
pipeline and the internal architecture of the proposed engine. They are
drawn as vector line art in a restrained monochrome idiom rather than
generated as images, so every label is typeset text. Figures 3 and 4 are
data figures produced from the trained model: the evidence trail of the
proposed model over one pupil's episodes, and what regularising
the attention of the attention variant does to accuracy, faithfulness
and alignment.

No figure carries a legend placed over its content; everything a note
would say is in the body text.
"""
from __future__ import annotations

import json
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
TAB = os.path.join(ROOT, "tables")
FIG = os.path.join(ROOT, "figures")
os.makedirs(FIG, exist_ok=True)

BLACK = "#000000"
GREY = "#7F7F7F"
LIGHT = "#E8E8E8"

plt.rcParams.update({
    "font.family": "DejaVu Serif",
    "font.size": 7.0,
    "axes.labelsize": 7.0,
    "axes.titlesize": 7.5,
    "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5,
    "axes.linewidth": 0.6,
    "figure.dpi": 400,
    "savefig.dpi": 400,
})

FAM = ["Situation\nselection", "Situation\nmodification",
       "Attentional\ndeployment", "Cognitive\nchange",
       "Response\nmodulation"]
FAM1 = ["SS", "SM", "AD", "CC", "RM"]


def save(fig, name):
    path = os.path.join(FIG, name + ".png")
    fig.savefig(path, bbox_inches="tight", pad_inches=0.02,
                facecolor="white")
    plt.close(fig)
    print("  ", os.path.basename(path))
    return path


def _box(ax, cx, cy, w, h, lines, fs=6.4, bold=True, fill="white",
         lw=0.8, style="round,pad=0,rounding_size=1.6"):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle=style, facecolor=fill,
                                edgecolor=BLACK, linewidth=lw,
                                zorder=3))
    ax.text(cx, cy, "\n".join(lines), ha="center", va="center",
            fontsize=fs, fontweight="bold" if bold else "normal",
            color=BLACK, zorder=4, linespacing=1.3)
    return dict(cx=cx, cy=cy, l=cx - w / 2, r=cx + w / 2,
                t=cy + h / 2, b=cy - h / 2)


def _arrow(ax, p0, p1, lw=0.8, style="-|>", dashed=False):
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle=style + ",head_length=2.6,head_width=1.7",
        mutation_scale=1.0, linewidth=lw, color=BLACK,
        linestyle="--" if dashed else "-",
        shrinkA=1.0, shrinkB=1.0, zorder=2))


# ===========================================================================
def figure1_pipeline():
    """The assessment pipeline in which the engine is deployed."""
    W, H = 88.0, 48.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_axis_off()

    a = _box(ax, 14.0, 37.0, 26, 12,
             ["Momentary", "self-reports", "(4 prompts/school day)"], fs=5.5)
    b = _box(ax, 14.0, 16.5, 26, 12,
             ["Context and", "affect channels", "(17 features)"], fs=5.8)
    c = _box(ax, 44.0, 26.8, 22, 15,
             ["DP-APT", "assessment", "engine"], fs=6.6, fill=LIGHT)
    d = _box(ax, 74.0, 37.0, 26, 12,
             ["Regulation", "profile", "(5 families)"], fs=5.8)
    e = _box(ax, 74.0, 16.5, 26, 12,
             ["Episode-level", "evidence trail", "(audit report)"], fs=5.8)

    _arrow(ax, (a["r"], a["cy"]), (c["l"], c["cy"] + 3.5))
    _arrow(ax, (b["r"], b["cy"]), (c["l"], c["cy"] - 3.5))
    _arrow(ax, (c["r"], c["cy"] + 3.5), (d["l"], d["cy"]))
    _arrow(ax, (c["r"], c["cy"] - 3.5), (e["l"], e["cy"]))
    # the teacher's feedback loop, routed below the boxes so that it
    # crosses nothing
    yb = 3.4
    ax.plot([e["cx"], e["cx"]], [e["b"], yb], color=BLACK, lw=0.8,
            ls="--", zorder=2)
    ax.plot([e["cx"], b["cx"]], [yb, yb], color=BLACK, lw=0.8, ls="--",
            zorder=2)
    _arrow(ax, (b["cx"], yb), (b["cx"], b["b"]), dashed=True)
    ax.text(44.0, yb + 1.9, "class teacher review and feedback",
            ha="center", va="bottom", fontsize=5.8, style="italic",
            bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
    return save(fig, "figure1_pipeline")


# ===========================================================================
def figure2_architecture():
    """The internal architecture of the DP-APT engine."""
    W, H = 88.0, 62.0
    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_axis_off()

    ax.text(21.0, 59.0, "Episode pathway", ha="center", fontsize=6.6,
            fontweight="bold")
    ax.text(67.0, 59.0, "Ontology pathway", ha="center", fontsize=6.6,
            fontweight="bold")

    x1 = _box(ax, 21.0, 52.0, 40, 9,
              ["Momentary EMA", "sequence"], fs=6.0)
    x2 = _box(ax, 21.0, 40.5, 40, 9,
              ["Temporal Affect", "Graph Network"], fs=6.0)
    x3 = _box(ax, 21.0, 30.0, 40, 7,
              ["Episode representations"], fs=6.0, bold=False)

    y1 = _box(ax, 67.0, 52.0, 40, 9,
              ["Process-model", "ontology"], fs=6.0)
    y2 = _box(ax, 67.0, 40.5, 40, 9,
              ["Regulatory Process", "Ontology Parser"], fs=6.0)
    y3 = _box(ax, 67.0, 30.0, 40, 7,
              ["Concept vectors"], fs=6.0, bold=False)

    f1 = _box(ax, 44.0, 18.5, 52, 8,
              ["Concept-conditioned evidence fusion"], fs=6.2,
              fill=LIGHT)
    o1 = _box(ax, 22.0, 6.5, 40, 9,
              ["Per-family", "regulation score"], fs=6.0)
    o2 = _box(ax, 66.0, 6.5, 40, 9,
              ["Per-episode", "contributions"], fs=6.0)

    for a, b in ((x1, x2), (x2, x3), (y1, y2), (y2, y3)):
        _arrow(ax, (a["cx"], a["b"]), (b["cx"], b["t"]))
    _arrow(ax, (x3["cx"], x3["b"]), (34.0, f1["t"]))
    _arrow(ax, (y3["cx"], y3["b"]), (54.0, f1["t"]))
    _arrow(ax, (34.0, f1["b"]), (o1["cx"], o1["t"]))
    _arrow(ax, (54.0, f1["b"]), (o2["cx"], o2["t"]))
    return save(fig, "figure2_architecture")


# ===========================================================================
def figure3_alignment():
    """Evidence trail of the proposed model over one pupil."""
    A = np.load(os.path.join(TAB, "example_attention.npy"))   # (K,T)
    used = np.load(os.path.join(TAB, "example_used.npy"))
    mask = np.load(os.path.join(TAB, "example_mask.npy"))
    keep = np.where(mask > 0)[0][:48]
    # the trail is signed; the map shows the evidence that raised each
    # score, which is what the top-k measures are computed on
    Ak = np.maximum(A[:, keep], 0.0)
    Ak = Ak / (Ak.max(axis=1, keepdims=True) + 1e-12)

    fig = plt.figure(figsize=(88 / 25.4, 46 / 25.4))
    ax = fig.add_axes([0.175, 0.335, 0.800, 0.615])
    im = ax.imshow(Ak, aspect="auto", cmap="Greys", vmin=0, vmax=1,
                   interpolation="nearest")
    # the family actually deployed in each episode, marked in the row of
    # the family it belongs to, so that a dark cell under a marker is a
    # correct justification and can be read off directly
    ax.plot(np.arange(len(keep)), [used[t] for t in keep],
            linestyle="none", marker="s", markersize=2.6,
            markerfacecolor="none", markeredgecolor="#C81E1E",
            markeredgewidth=0.8, clip_on=False)
    ax.set_yticks(range(5))
    ax.set_yticklabels([f.replace("\n", " ") for f in FAM], fontsize=5.8)
    ax.set_xticks(np.arange(0, len(keep), 6))
    ax.set_xticklabels([str(i + 1) for i in range(0, len(keep), 6)],
                       fontsize=5.8)
    ax.set_xlabel("Momentary report (chronological order)", fontsize=6.4,
                  labelpad=2.0)
    ax.tick_params(width=0.5, length=2.2)
    for side in ax.spines.values():
        side.set_linewidth(0.6)
    cax = fig.add_axes([0.175, 0.115, 0.800, 0.045])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_label("contribution to the family score "
                 "(scaled to the row maximum)", fontsize=5.8,
                 labelpad=1.5)
    cb.ax.tick_params(labelsize=5.4, width=0.5, length=2)
    cb.outline.set_linewidth(0.6)
    return save(fig, "figure3_alignment")


# ===========================================================================
def figure4_tradeoff():
    """Effect of sparsifying the attention of the attention variant."""
    with open(os.path.join(TAB, "results.json"), encoding="utf-8") as fh:
        R = json.load(fh)
    S = R["sparsity_sweep"]
    lam = [s["lam"] for s in S]
    x = np.arange(len(lam))
    chance = R["corpus"]["chance_alignment"]
    panels = [("AUC-ROC", [s["auc_roc"] for s in S], "o", None),
              ("comprehensiveness", [s["comprehensiveness"] for s in S],
               "s", None),
              ("justification alignment", [s["alignment"] for s in S],
               "^", chance)]

    # three panels sharing one categorical axis: a twin axis would put
    # two scales on one frame and the labels would collide at this width
    fig = plt.figure(figsize=(88 / 25.4, 40 / 25.4))
    left, gap = 0.105, 0.115
    wid = (1.0 - left - 2 * gap - 0.02) / 3.0
    labels = [("0" if l == 0 else ("%g" % l).lstrip("0")) for l in lam]
    for j, (name, ys, mk, ref) in enumerate(panels):
        ax = fig.add_axes([left + j * (wid + gap), 0.255, wid, 0.700])
        ax.plot(x, ys, color=BLACK, lw=1.0, marker=mk, ms=2.8,
                markerfacecolor="white", markeredgewidth=0.7)
        if ref is not None:
            ax.axhline(ref, color=GREY, lw=0.7, ls=(0, (4, 3)))
            ax.text(x[-1], ref, "chance ", fontsize=5.2, color=GREY,
                    va="bottom", ha="right")
            ax.set_ylim(min(ref, min(ys)) - 0.03, max(ys) + 0.03)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=5.0, rotation=90)
        ax.set_ylabel(name, fontsize=6.0, labelpad=1.5)
        ax.set_xlabel(r"$\lambda$", fontsize=6.4, labelpad=1.0)
        ax.tick_params(axis="y", labelsize=5.4, width=0.5, length=2.2)
        ax.tick_params(axis="x", width=0.5, length=2.0, pad=1.0)
        for side in ax.spines.values():
            side.set_linewidth(0.6)
    return save(fig, "figure4_tradeoff")


# ===========================================================================
if __name__ == "__main__":
    figure1_pipeline()
    figure2_architecture()
    if os.path.exists(os.path.join(TAB, "example_attention.npy")):
        figure3_alignment()
    if os.path.exists(os.path.join(TAB, "results.json")):
        figure4_tradeoff()
    print("figures written to", FIG)
