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
def poly(ax, pts, color=NAVY, lw=1.15, dashed=False, label=None, lxy=None,
         fs=7.8, zorder=5):
    """An orthogonal connector: straight segments, arrowhead on the last one."""
    ls = (0, (4.5, 2.6)) if dashed else "-"
    for i in range(len(pts) - 2):
        ax.plot([pts[i][0], pts[i + 1][0]], [pts[i][1], pts[i + 1][1]],
                color=color, lw=lw, ls=ls, solid_capstyle="round",
                zorder=zorder)
    ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>",
                                 mutation_scale=11, lw=lw, color=color,
                                 linestyle=ls, shrinkA=0, shrinkB=3.0,
                                 zorder=zorder))
    if label:
        ax.text(lxy[0], lxy[1], label, ha="center", va="center", fontsize=fs,
                color=color, zorder=9, path_effects=HALO)


def figure1():
    fig, ax = plt.subplots(2, 1, figsize=(7.2, 8.0),
                           gridspec_kw=dict(height_ratios=[1.0, 1.12]))

    # ------------------------------------------------------- panel (a)
    a = ax[0]
    a.set_xlim(0, 14.4); a.set_ylim(0, 8.0); a.axis("off")
    a.text(0.0, 7.92, "(a)  Worker flows across the two tiers of the ladder",
           fontsize=9.6, fontweight="bold", ha="left", va="top", color=INK)

    C1, C2, W, H = 3.4, 10.0, 3.4, 1.05
    R1, R2 = 5.7, 2.4
    hw, hh = W / 2, H / 2

    a.add_patch(FancyBboxPatch((0.15, 4.85), 14.1, 2.15,
                               boxstyle="round,pad=0.02,rounding_size=0.10",
                               fc="#f7f9fc", ec="none", zorder=0))
    a.add_patch(FancyBboxPatch((0.15, 1.15), 14.1, 2.15,
                               boxstyle="round,pad=0.02,rounding_size=0.10",
                               fc="#fbf7f4", ec="none", zorder=0))
    a.text(0.32, 6.92, "ENTRY-LEVEL TIER", ha="left", va="top", fontsize=7.6,
           color=NAVY, fontweight="bold")
    a.text(0.32, 3.22, "EXPERIENCED TIER", ha="left", va="top", fontsize=7.6,
           color=RUST, fontweight="bold")

    box(a, C1, R1, W, H, "Entry-level jobseekers\n$u_j$", ec=NAVY)
    box(a, C2, R1, W, H, "Entry-level employed\n$e_j$", ec=NAVY, fc="#eef2f9")
    box(a, C1, R2, W, H, "Experienced jobseekers\n$u_s$", ec=RUST)
    box(a, C2, R2, W, H, "Experienced employed\n$e_s$", ec=RUST, fc="#fbeeea")

    cloud(a, 0.80, R1, s=0.22)
    a.text(0.80, R1 - 0.66, "new entrants\n$\\omega$", ha="center", va="top",
           fontsize=7.4, color=GREY, linespacing=1.3)
    poly(a, [(1.22, R1), (C1 - hw, R1)], color=GREY, lw=1.05)

    poly(a, [(C1 + hw, R1 + 0.24), (C2 - hw, R1 + 0.24)], color=NAVY,
         label="hiring  $f_j=\\mu_j\\theta_j^{1-\\eta}$", lxy=(6.7, R1 + 0.60))
    poly(a, [(C2 - hw, R1 - 0.24), (C1 + hw, R1 - 0.24)], color=NAVY,
         label="separation  $\\delta_j$", lxy=(6.7, R1 - 0.58))
    poly(a, [(C1 + hw, R2 + 0.24), (C2 - hw, R2 + 0.24)], color=RUST,
         label="hiring  $f_s=\\mu_s\\theta_s^{1-\\eta}$", lxy=(6.7, R2 + 0.60))
    poly(a, [(C2 - hw, R2 - 0.24), (C1 + hw, R2 - 0.24)], color=RUST,
         label="separation  $\\delta_s$", lxy=(6.7, R2 - 0.58))

    poly(a, [(C2, R1 - hh), (C2, R2 + hh)], color=TEAL, lw=1.9,
         label="promotion\n$\\pi(m)=\\bar\\pi m^{\\psi}$", lxy=(11.9, 4.05),
         fs=8.0)

    poly(a, [(C2 + hw, R2), (12.45, R2)], color=GOLD, lw=1.15)
    a.text(12.65, R2, "poached by\nrivals at $\\phi$", ha="left", va="center",
           fontsize=7.4, color=GOLD, linespacing=1.3)

    a.text(7.2, 0.42,
           "Promotion is the only source of experienced workers.  "
           "All four states exit the labour force at rate $\\omega$.",
           ha="center", va="center", fontsize=8.0, color=INK)

    # ------------------------------------------------------- panel (b)
    b = ax[1]
    b.set_xlim(0, 14.4); b.set_ylim(0, 9.0); b.axis("off")
    b.text(0.0, 8.92, "(b)  Technology: the joint product of an entry-level job",
           fontsize=9.6, fontweight="bold", ha="left", va="top", color=INK)

    K1, K2, K3 = 2.9, 7.9, 12.2
    BW, BH = 3.6, 1.05
    bhw, bhh = BW / 2, BH / 2

    b.add_patch(FancyBboxPatch((0.15, 3.05), 14.1, 4.55,
                               boxstyle="round,pad=0.02,rounding_size=0.10",
                               fc="#f7f9fc", ec="none", zorder=0))
    b.add_patch(FancyBboxPatch((0.15, 0.70), 14.1, 1.85,
                               boxstyle="round,pad=0.02,rounding_size=0.10",
                               fc="#eef6f4", ec="none", zorder=0))
    b.text(0.32, 7.52, "PRODUCTION", ha="left", va="top", fontsize=7.6,
           color=NAVY, fontweight="bold")
    b.text(0.32, 2.48, "TRAINING", ha="left", va="top", fontsize=7.6,
           color=TEAL, fontweight="bold")

    ej = box(b, K1, 6.55, BW, BH, "Entry-level labour\n$e_j$", ec=NAVY)
    ai = box(b, K1, 4.95, BW, BH, "Artificial intelligence\n$A$", ec=GOLD,
             fc="#fdf6e7")
    xj = box(b, K2, 5.75, BW, BH, "Entry-level tasks\n$X_j=e_j+\\chi A$",
             ec=NAVY, fc="#eef2f9")
    xs = box(b, K2, 3.65, BW, BH, "Experienced tasks\n$X_s=e_s-m\\,e_j$",
             ec=RUST, fc="#fbeeea")
    yy = box(b, K3, 4.70, BW - 0.3, BH + 0.20,
             "Output\n$Y=Z[\\alpha X_j^{\\rho}+(1-\\alpha)X_s^{\\rho}]^{s/\\rho}$",
             ec=INK, fs=8.0)
    es = box(b, K1, 1.55, BW, BH, "Experienced labour\n$e_s$", ec=RUST)
    mm = box(b, K2, 1.55, BW, BH, "Mentoring\n$m$ hours per entrant", ec=TEAL,
             fc="#eaf4f2")
    box(b, K3, 1.55, BW - 0.3, BH, "Promotion hazard\n$\\pi(m)=\\bar\\pi m^{\\psi}$",
        ec=TEAL, fc="#eaf4f2")

    poly(b, [(K1 + bhw, 6.55), (5.55, 6.55), (5.55, 5.75), (K2 - bhw, 5.75)],
         color=NAVY, lw=1.15)
    poly(b, [(K1 + bhw, 4.95), (5.55, 4.95), (5.55, 5.75 - 0.30),
             (K2 - bhw, 5.75 - 0.30)], color=GOLD, lw=1.15,
         label="substitutes", lxy=(5.45, 4.52), fs=7.6)
    poly(b, [(K1, 1.55 + bhh), (K1, 3.65), (K2 - bhw, 3.65)], color=RUST,
         lw=1.15)
    poly(b, [(K2 + bhw, 5.75), (10.25, 5.75), (10.25, 4.70 + 0.28),
             (K3 - bhw + 0.15, 4.70 + 0.28)], color=NAVY, lw=1.15)
    poly(b, [(K2 + bhw, 3.65), (10.25, 3.65), (10.25, 4.70 - 0.28),
             (K3 - bhw + 0.15, 4.70 - 0.28)], color=RUST, lw=1.15)

    poly(b, [(K1 + bhw, 1.55), (K2 - bhw, 1.55)], color=TEAL, lw=1.15,
         label="diverts senior time", lxy=(5.40, 2.24), fs=7.6)
    poly(b, [(K2 + bhw, 1.55), (K3 - bhw + 0.15, 1.55)], color=TEAL, lw=1.6,
         label="the only source of\nexperienced workers", lxy=(10.05, 2.34),
         fs=7.4)
    poly(b, [(K2 - 1.15, 1.55 + bhh), (K2 - 1.15, 3.65 - bhh)], color=TEAL,
         lw=1.05, dashed=True, label="$-\\,m\\,e_j$", lxy=(7.42, 2.72),
         fs=7.6)

    b.text(7.2, 0.28,
           "Artificial intelligence raises $X_j$ but cannot raise $\\pi$: it "
           "enters the production block and never the training block.",
           ha="center", va="center", fontsize=8.0, color=INK)

    fig.tight_layout(h_pad=1.2)
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
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 6.25)
    ax.axis("off")

    ax.text(0.0, 6.18, "The return to an entry-level match, and the two "
                       "wedges that shrink it",
            fontsize=9.4, fontweight="bold", ha="left", va="top", color=INK)

    W, BASE_Y = 2.00, 1.25
    XS, XP = 2.10, 8.70
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
    hb = box(ax, 5.15, 3.42, 3.00, 0.80,
             "hold-up: mentoring is chosen\nafter the wage is set, so the firm\n"
             "keeps only a share $1-\\beta$", ec=TEAL, fc="#eaf4f2", fs=7.0)
    pb = box(ax, 5.15, 4.72, 3.00, 0.80,
             "poaching: the trained worker is lost\nto rivals at rate $\\phi$, which "
             "the firm\ndiscounts and society does not", ec=GOLD,
             fc="#fdf6e7", fs=7.0)
    LH, LP = 6.95, 7.25            # two lanes, so the connectors never meet
    poly(ax, [anchor(hb, "r"), (LH, 3.42), (LH, y_hold),
              (XP - W / 2 - 0.02, y_hold)], color=TEAL, lw=1.15, zorder=6)
    poly(ax, [anchor(pb, "r"), (LP, 4.72), (LP, y_poach),
              (XP - W / 2 - 0.02, y_poach)], color=GOLD, lw=1.15, zorder=6)
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

    ax.add_patch(FancyBboxPatch((0.10, 0.06), 11.80, 0.62,
                                boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc="#f4f4f4", ec=GREY, lw=0.8, zorder=1))
    ax.text(6.00, 0.37,
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
