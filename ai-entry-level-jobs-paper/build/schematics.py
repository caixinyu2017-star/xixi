# -*- coding: utf-8 -*-
"""Figures 1 and 2: the structure of the model and the mechanism it formalises.

Drawn programmatically so that every arrow corresponds to an equation in the
text.  Labels carry a white halo and arrows are routed on explicit anchors so
that nothing is occluded.
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.abspath(os.path.join(HERE, "..", "figs"))
os.makedirs(FIGS, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "DejaVu Serif", "Times New Roman"],
    "font.size": 9,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.03,
})

NAVY, RUST, TEAL, GOLD, GREY = "#1f3b73", "#b5432c", "#2e7d74", "#c58b1e", "#5d5d5d"
HALO = [withStroke(linewidth=2.6, foreground="white")]
INK = "#111111"


def box(ax, x, y, w, h, text, fc="white", ec=NAVY, fs=8.6, lw=1.1, bold=False):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle="round,pad=0.045,rounding_size=0.10",
                       fc=fc, ec=ec, lw=lw, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4,
            color=INK, linespacing=1.35,
            fontweight="bold" if bold else "normal")
    return dict(x=x, y=y, w=w, h=h)


def cloud(ax, x, y, s=0.30, color=GREY):
    for dx, dy, r in ((-0.55, -0.05, 0.52), (0.0, 0.18, 0.62),
                      (0.55, -0.05, 0.52), (-0.28, -0.26, 0.42),
                      (0.28, -0.26, 0.42)):
        ax.add_patch(Circle((x + dx * s * 2, y + dy * s * 2), r * s * 2,
                            fc="white", ec=color, lw=0.9, zorder=2))


def anchor(b, side, frac=0.0):
    x, y, w, h = b["x"], b["y"], b["w"], b["h"]
    if side == "r":
        return (x + w / 2, y + frac * h / 2)
    if side == "l":
        return (x - w / 2, y + frac * h / 2)
    if side == "t":
        return (x + frac * w / 2, y + h / 2)
    return (x + frac * w / 2, y - h / 2)


def arrow(ax, p0, p1, color=NAVY, rad=0.0, lw=1.15, ls="-", label=None,
          lpos=0.5, loff=(0.0, 0.16), fs=8.2, dashed=False, zorder=5):
    a = FancyArrowPatch(p0, p1, connectionstyle="arc3,rad=%.3f" % rad,
                        arrowstyle="-|>", mutation_scale=11, lw=lw,
                        color=color, zorder=zorder,
                        linestyle=(0, (4, 2.4)) if dashed else ls,
                        shrinkA=2.5, shrinkB=3.5)
    ax.add_patch(a)
    if label:
        cx = (p0[0] + p1[0]) / 2 + rad * (p1[1] - p0[1])
        cy = (p0[1] + p1[1]) / 2 - rad * (p1[0] - p0[0])
        t = lpos
        bx = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * cx + t ** 2 * p1[0]
        by = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * cy + t ** 2 * p1[1]
        ax.text(bx + loff[0], by + loff[1], label, ha="center", va="center",
                fontsize=fs, color=color, zorder=8, path_effects=HALO)


# ================================================================== Figure 1
def figure1():
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(6.9, 6.5),
                                 gridspec_kw=dict(height_ratios=[1.0, 1.06]))

    # ---------------------------------------------------------- panel (a)
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0.0, 5.4)
    ax.axis("off")
    ax.text(0.0, 5.32, "(a)  Worker flows across the two tiers of the ladder",
            fontsize=9.2, fontweight="bold", ha="left", va="top", color=INK)

    uj = box(ax, 2.75, 4.05, 2.25, 0.82,
             "Entry-level\njobseekers  $u_j$", ec=NAVY)
    ej = box(ax, 6.75, 4.05, 2.25, 0.82,
             "Entry-level\nemployed  $e_j$", ec=NAVY, fc="#eef2f9")
    us = box(ax, 2.75, 1.50, 2.25, 0.82,
             "Experienced\njobseekers  $u_s$", ec=RUST)
    es = box(ax, 6.75, 1.50, 2.25, 0.82,
             "Experienced\nemployed  $e_s$", ec=RUST, fc="#fbeeea")

    cloud(ax, 0.52, 4.05, s=0.26)
    ax.text(0.52, 3.42, "new\nentrants", ha="center", va="top", fontsize=7.8,
            color=GREY)
    arrow(ax, (0.98, 4.05), anchor(uj, "l"), color=GREY, label=r"$\omega$",
          loff=(0.0, 0.24))

    arrow(ax, anchor(uj, "r", 0.55), anchor(ej, "l", 0.55), rad=-0.26,
          color=NAVY, label=r"hiring  $f_j=\mu_j\theta_j^{1-\eta}$",
          loff=(0.0, 0.28))
    arrow(ax, anchor(ej, "l", -0.55), anchor(uj, "r", -0.55), rad=-0.26,
          color=NAVY, label=r"separation  $\delta_j$", loff=(0.0, -0.28))

    arrow(ax, anchor(us, "r", 0.55), anchor(es, "l", 0.55), rad=-0.26,
          color=RUST, label=r"hiring  $f_s=\mu_s\theta_s^{1-\eta}$",
          loff=(0.0, 0.28))
    arrow(ax, anchor(es, "l", -0.55), anchor(us, "r", -0.55), rad=-0.26,
          color=RUST, label=r"separation  $\delta_s$", loff=(0.0, -0.28))

    arrow(ax, anchor(ej, "b"), anchor(es, "t"), color=TEAL, lw=1.9,
          label=r"promotion  $\pi(m)=\bar\pi m^{\psi}$", loff=(1.72, 0.0),
          fs=8.4)

    # poaching loop on the senior box
    a = FancyArrowPatch((7.88, 1.82), (7.88, 1.18),
                        connectionstyle="arc3,rad=-1.25", arrowstyle="-|>",
                        mutation_scale=10, lw=1.15, color=GOLD, zorder=5,
                        shrinkA=2, shrinkB=2)
    ax.add_patch(a)
    ax.text(9.45, 1.50, "poached by\nrival firms\nat rate $\\phi$",
            ha="center", va="center", fontsize=7.8, color=GOLD,
            path_effects=HALO)

    for b, sgn in ((uj, -1), (ej, 1), (us, -1), (es, 1)):
        arrow(ax, anchor(b, "b", 0.72 * sgn),
              (b["x"] + 0.62 * sgn, b["y"] - 0.95), color=GREY, lw=0.85,
              dashed=True)
    ax.text(5.30, 0.28, r"dashed arrows: exit from the labour force at rate "
                        r"$\omega$",
            ha="center", va="center", fontsize=7.8, color=GREY)

    # ---------------------------------------------------------- panel (b)
    bx.set_xlim(0, 10.4)
    bx.set_ylim(0.0, 5.3)
    bx.axis("off")
    bx.text(0.0, 5.22, "(b)  Technology: the joint product of an entry-level job",
            fontsize=9.2, fontweight="bold", ha="left", va="top", color=INK)

    esb = box(bx, 1.45, 4.30, 2.30, 0.60, "Experienced labour  $e_s$", ec=RUST,
              fs=8.2)
    men = box(bx, 5.00, 4.30, 2.85, 0.62,
              "Mentoring:  $m$ senior hours\nper entry-level worker", ec=TEAL,
              fc="#eaf4f2", fs=7.8)
    pro = box(bx, 8.65, 4.30, 2.75, 0.60,
              "Promotion  $\\pi(m)=\\bar\\pi m^{\\psi}$", ec=TEAL, fc="#eaf4f2",
              fs=8.2)
    arrow(bx, anchor(esb, "r"), anchor(men, "l"), color=RUST, fs=7.4,
          label="senior time", loff=(0.0, 0.22))
    arrow(bx, anchor(men, "r"), anchor(pro, "l"), color=TEAL, lw=1.6, fs=7.4,
          label="the only source of seniors", loff=(0.0, 0.62))
    bx.text(8.65, 3.86, "$\\rightarrow$ feeds the promotion flow in panel (a)",
            ha="center", va="top", fontsize=7.4, color=TEAL)

    ejb = box(bx, 1.45, 2.72, 2.30, 0.56, "Entry-level labour  $e_j$", ec=NAVY,
              fs=8.2)
    ai = box(bx, 1.45, 1.62, 2.30, 0.56, "AI input  $A$", ec=GOLD, fs=8.2,
             fc="#fdf6e7")
    xj = box(bx, 5.60, 2.20, 2.60, 0.68,
             "Entry-level tasks\n$X_j=e_j+\\chi A$", ec=NAVY, fc="#eef2f9",
             fs=8.2)
    xs = box(bx, 5.60, 0.62, 2.60, 0.68,
             "Experienced tasks\n$X_s=e_s-m\\,e_j$", ec=RUST, fc="#fbeeea",
             fs=8.2)
    yb = box(bx, 8.90, 1.42, 2.50, 0.82,
             "Output\n$Y=Z\\,[\\alpha X_j^{\\rho}+(1-\\alpha)"
             "X_s^{\\rho}]^{s/\\rho}$", ec=INK, fs=7.6)

    arrow(bx, anchor(ejb, "r"), anchor(xj, "l", 0.55), color=NAVY, rad=-0.10)
    arrow(bx, anchor(ai, "r"), anchor(xj, "l", -0.55), color=GOLD, rad=0.10,
          label="substitutes", loff=(0.20, -0.26), fs=7.4)
    arrow(bx, anchor(xj, "r"), anchor(yb, "l", 0.55), color=NAVY, rad=-0.10)
    arrow(bx, anchor(xs, "r"), anchor(yb, "l", -0.55), color=RUST, rad=0.10)
    # mentoring diverts senior time: routed through the free left corridor
    arrow(bx, (3.66, 4.00), (4.30, 0.68), color=TEAL, rad=0.40, dashed=True,
          lw=1.0, label="diverts\n$m\\,e_j$ hours", loff=(-0.80, -0.22), fs=7.4)
    bx.text(1.45, 0.62, "AI raises $X_j$\nbut cannot raise $\\pi$",
            ha="center", va="center", fontsize=8.2, color=GOLD, style="italic")

    fig.tight_layout(h_pad=1.0)
    out = os.path.join(FIGS, "fig1_structure.png")
    fig.savefig(out)
    plt.close(fig)
    print("  ", os.path.basename(out))


# ================================================================== Figure 2
def figure2():
    """The joint product, its two wedges, and where AI bites.

    Block heights are illustrative; the estimated magnitudes are reported in
    Section 4 and shown in Figure 3.
    """
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 6.25)
    ax.axis("off")

    ax.text(0.0, 6.18, "The return to an entry-level match, and the two wedges "
                       "that shrink it",
            fontsize=9.4, fontweight="bold", ha="left", va="top", color=INK)

    W, BASE_Y = 2.00, 1.25
    XS, XP = 2.10, 7.05
    OUT_H, SOC_H = 1.55, 2.05
    PRIV_H, HOLD_H, POACH_H = 0.86, 0.72, 0.47

    def block(x, y0, h, txt, fc, ec, hatch=None, fs=7.6):
        ax.add_patch(FancyBboxPatch(
            (x - W / 2, y0), W, h,
            boxstyle="round,pad=0.015,rounding_size=0.05",
            fc=fc, ec=ec, lw=1.0, hatch=hatch, zorder=3))
        if txt:
            ax.text(x, y0 + h / 2, txt, ha="center", va="center", fontsize=fs,
                    zorder=4, color=INK, linespacing=1.3)

    # --- social column
    block(XS, BASE_Y, OUT_H, "current output\n$F_j$", "#9fb3d1", NAVY)
    block(XS, BASE_Y + OUT_H, SOC_H,
          "value of creating\nan experienced\nworker\n"
          "$\pi'(m)\,(\lambda_{es}-\lambda_{ej})$", "#a8cfc9", TEAL, fs=7.4)
    ax.text(XS, 4.95, "SOCIAL RETURN", ha="center", va="bottom", fontsize=8.6,
            fontweight="bold", color=INK)
    ax.text(XS, 1.10, "what the planner values", ha="center", va="top",
            fontsize=7.6, color=GREY, style="italic")

    # --- private column, same total height, with the losses shown as hatching
    y = BASE_Y
    block(XP, y, OUT_H, "current output\n$F_j$", "#9fb3d1", NAVY)
    y += OUT_H
    block(XP, y, PRIV_H, "firm's share", "#a8cfc9", TEAL, fs=7.6)
    y += PRIV_H
    block(XP, y, HOLD_H, "", "white", TEAL, hatch="////")
    y_hold = y + HOLD_H / 2
    y += HOLD_H
    block(XP, y, POACH_H, "", "white", GOLD, hatch="\\\\\\\\")
    y_poach = y + POACH_H / 2
    ax.text(XP, 4.95, "PRIVATE RETURN", ha="center", va="bottom", fontsize=8.6,
            fontweight="bold", color=INK)
    ax.text(XP, 1.10, "what the firm captures", ha="center", va="top",
            fontsize=7.6, color=GREY, style="italic")

    # --- the two wedges, explained between the columns
    hb = box(ax, 4.56, 3.42, 2.52, 0.80,
             "hold-up: mentoring is chosen\nafter the wage is set, so the firm\n"
             "keeps only a share $1-\\beta$", ec=TEAL, fc="#eaf4f2", fs=7.0)
    pb = box(ax, 4.56, 4.72, 2.52, 0.80,
             "poaching: the trained worker is lost\nto rivals at rate $\\phi$, which "
             "the firm\ndiscounts and society does not", ec=GOLD,
             fc="#fdf6e7", fs=7.0)
    arrow(ax, anchor(hb, "r"), (XP - W / 2 - 0.03, y_hold), color=TEAL,
          lw=1.0, dashed=True, rad=-0.14, zorder=6)
    arrow(ax, anchor(pb, "r"), (XP - W / 2 - 0.03, y_poach), color=GOLD,
          lw=1.0, dashed=True, rad=0.14, zorder=6)
    ax.text(XP + W / 2 + 0.16, y_hold, "lost to\nhold-up", ha="left",
            va="center", fontsize=7.4, color=TEAL, linespacing=1.3)
    ax.text(XP + W / 2 + 0.16, y_poach, "lost to\npoaching", ha="left",
            va="center", fontsize=7.4, color=GOLD, linespacing=1.3)

    # --- where AI bites
    ax.text(0.58, BASE_Y + OUT_H / 2, "AI\nsubstitutes\nfor this",
            ha="center", va="center", fontsize=7.4, color=GOLD,
            fontweight="bold", linespacing=1.35)
    ax.text(0.58, BASE_Y + OUT_H + SOC_H / 2, "AI cannot\nsubstitute\nfor this",
            ha="center", va="center", fontsize=7.4, color=TEAL,
            fontweight="bold", linespacing=1.35)

    ax.add_patch(FancyBboxPatch((0.10, 0.06), 10.40, 0.62,
                                boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc="#f4f4f4", ec=GREY, lw=0.8, zorder=1))
    ax.text(5.30, 0.37,
            "AI shrinks the block that firms price correctly and leaves "
            "untouched the block they under-price. The case for hiring an\n"
            "entry-level worker therefore comes to rest entirely on the "
            "return that the market fails to reward.",
            ha="center", va="center", fontsize=7.9, color=INK, linespacing=1.45)

    fig.tight_layout()
    out = os.path.join(FIGS, "fig2_mechanism.png")
    fig.savefig(out)
    plt.close(fig)
    print("  ", os.path.basename(out))


if __name__ == "__main__":
    print("schematics:")
    figure1()
    figure2()
