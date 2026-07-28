# -*- coding: utf-8 -*-
"""Figures 1 and 2: the structure of the model and the mechanism it formalises."""
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
    "font.size": 9, "savefig.dpi": 600, "savefig.bbox": "tight",
    "savefig.pad_inches": 0.03,
})

NAVY, RUST, TEAL, GOLD, GREY = "#1f3b73", "#b5432c", "#2e7d74", "#c58b1e", "#5d5d5d"
HALO = [withStroke(linewidth=2.6, foreground="white")]
INK = "#111111"


def box(ax, x, y, w, h, text, fc="white", ec=NAVY, fs=8.4, lw=1.1, ls="-"):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle="round,pad=0.045,rounding_size=0.10",
                       fc=fc, ec=ec, lw=lw, ls=ls, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4,
            color=INK, linespacing=1.35)
    return dict(x=x, y=y, w=w, h=h)


def cloud(ax, x, y, s=0.26, color=GREY):
    for dx, dy, rr in ((-0.55, -0.05, 0.52), (0.0, 0.18, 0.62),
                       (0.55, -0.05, 0.52), (-0.28, -0.26, 0.42),
                       (0.28, -0.26, 0.42)):
        ax.add_patch(Circle((x + dx * s * 2, y + dy * s * 2), rr * s * 2,
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


def arrow(ax, p0, p1, color=NAVY, rad=0.0, lw=1.15, label=None, lpos=0.5,
          loff=(0.0, 0.16), fs=7.8, dashed=False, zorder=5):
    a = FancyArrowPatch(p0, p1, connectionstyle="arc3,rad=%.3f" % rad,
                        arrowstyle="-|>", mutation_scale=11, lw=lw,
                        color=color, zorder=zorder,
                        linestyle=(0, (4, 2.4)) if dashed else "-",
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
    fig, ax = plt.subplots(figsize=(6.9, 4.9))
    ax.set_xlim(0, 11.9)
    ax.set_ylim(0, 8.4)
    ax.axis("off")
    ax.text(0.0, 8.36, "Worker flows between the rationed and the market sector",
            fontsize=9.4, fontweight="bold", ha="left", va="top", color=INK)

    ax.add_patch(FancyBboxPatch((0.15, 4.42), 11.5, 3.45,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc="#f7f9fc", ec="none", zorder=0))
    ax.add_patch(FancyBboxPatch((0.15, 0.62), 11.5, 3.35,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc="#fbf7f4", ec="none", zorder=0))
    ax.text(0.30, 7.78, "YOUNG   ages 23–30", ha="left", va="top",
            fontsize=7.6, color=NAVY, fontweight="bold")
    ax.text(0.30, 3.88, "PRIME   until retirement at $R$", ha="left", va="top",
            fontsize=7.6, color=RUST, fontweight="bold")

    # ---------------------------------------------------------- states
    cloud(ax, 0.62, 6.20, s=0.23)
    ax.text(0.62, 5.66, "entrants\n$n$", ha="center", va="top", fontsize=7.4,
            color=GREY, linespacing=1.3)
    um = box(ax, 2.10, 7.05, 2.25, 0.70, "Open search\n$u_m$", ec=NAVY)
    emb = box(ax, 8.70, 7.05, 2.25, 0.70, "Market job\n$e_m$", ec=NAVY,
              fc="#eef2f9")
    uq = box(ax, 3.60, 5.25, 2.25, 0.70, "Queueing\n$u_q$", ec=GOLD,
             fc="#fdf6e7")
    eqb = box(ax, 6.90, 5.25, 2.25, 0.70, "Rationed job\n$e_q$", ec=GOLD,
              fc="#fdf6e7")
    Eq = box(ax, 6.90, 3.00, 2.25, 0.66, "Rationed job\n$E_q$", ec=GOLD,
             fc="#fdf6e7", fs=8.0)
    Um = box(ax, 2.10, 1.40, 2.25, 0.70, "Open search\n$U_m$", ec=RUST)
    Em = box(ax, 8.70, 1.40, 2.25, 0.70, "Market job\n$E_m$", ec=RUST,
             fc="#fbeeea")

    # ---------------------------------------------------------- entry
    arrow(ax, (1.06, 6.42), anchor(um, "l", -0.35), color=GREY, rad=-0.18)
    arrow(ax, (1.06, 5.98), anchor(uq, "l", 0.35), color=GREY, rad=0.22)

    # ---------------------------------------------------------- hiring
    arrow(ax, anchor(uq, "r"), anchor(eqb, "l"), color=GOLD, lw=1.5,
          label=r"$\lambda_Q$", loff=(0.0, 0.26))
    arrow(ax, anchor(um, "r", 0.5), anchor(emb, "l", 0.5), rad=-0.18,
          color=NAVY, label=r"$f_y=\mu_y\theta^{1-\eta}$", loff=(0.0, 0.30))
    arrow(ax, anchor(emb, "l", -0.5), anchor(um, "r", -0.5), rad=-0.18,
          color=NAVY, label=r"$\delta_M$", loff=(0.0, -0.30))
    arrow(ax, anchor(Um, "r", 0.5), anchor(Em, "l", 0.5), rad=-0.18,
          color=RUST, label=r"$f_p=\theta^{1-\eta}$", loff=(0.0, 0.30))
    arrow(ax, anchor(Em, "l", -0.5), anchor(Um, "r", -0.5), rad=-0.18,
          color=RUST, label=r"$\delta_M$", loff=(0.0, -0.30))

    # ---------------------------------------------------------- ageing
    arrow(ax, anchor(eqb, "b"), anchor(Eq, "t"), color=GOLD, lw=1.6,
          label=r"$\gamma$", loff=(0.26, 0.0))
    arrow(ax, anchor(emb, "b"), anchor(Em, "t"), color=NAVY, lw=1.6,
          label=r"$\gamma$", loff=(0.26, 0.0))
    arrow(ax, (2.75, 4.90), (2.55, 1.75), color=GREY, lw=1.0, dashed=True,
          rad=0.05)
    arrow(ax, anchor(um, "b", -0.55), anchor(Um, "t", -0.55), color=GREY,
          lw=1.0, dashed=True, rad=0.04)
    ax.text(1.02, 2.55, "ageing at\n$\\gamma=1/T_y$", ha="center", va="center",
            fontsize=7.4, color=GREY, linespacing=1.3, path_effects=HALO)
    arrow(ax, anchor(Eq, "l"), anchor(Um, "r", 0.95), color=GOLD, lw=1.0,
          rad=0.20, dashed=True, label=r"$\delta_Q$", loff=(0.60, -0.02))

    # ---------------------------------------------------------- retirement
    cloud(ax, 11.05, 2.20, s=0.20)
    ax.text(11.05, 1.66, "retirement\nrate $\\rho$", ha="center", va="top",
            fontsize=7.4, color=GREY, linespacing=1.3)
    arrow(ax, anchor(Eq, "r"), (10.68, 2.28), color=GREY, lw=0.95, dashed=True,
          rad=-0.10)
    arrow(ax, anchor(Em, "r"), (10.68, 2.06), color=GREY, lw=0.95, dashed=True,
          rad=0.14)

    # ------------------------------- the establishment's replacement flow
    vb = box(ax, 4.55, 3.85, 2.90, 0.70,
             "Establishment vacancies\n$v_Q=\\delta_Q\\bar N+\\rho E_q$",
             ec=GOLD, fc="#fdf6e7", fs=8.0, lw=1.5)
    arrow(ax, anchor(Eq, "l", 0.55), anchor(vb, "r", -0.4), color=GOLD,
          lw=1.3, rad=-0.16)
    arrow(ax, anchor(vb, "t", -0.1), (5.35, 5.25), color=GOLD, lw=1.6,
          rad=-0.18)
    ax.text(5.95, 0.22,
            "Establishment constraint  $e_q+E_q=\\bar N$, fixed "
            "administratively;  free entry fixes $\\theta$ in the market sector",
            ha="center", va="center", fontsize=8.0, color=INK)

    fig.tight_layout()
    out = os.path.join(FIGS, "fig1_structure.png")
    fig.savefig(out)
    plt.close(fig)
    print("  ", os.path.basename(out))


# ================================================================== Figure 2
def figure2():
    fig, ax = plt.subplots(figsize=(6.9, 4.2))
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 6.9)
    ax.axis("off")
    ax.text(0.0, 6.84, "Three routes from a later retirement age to the young, "
                       "and why they cancel in the headline rate",
            fontsize=9.4, fontweight="bold", ha="left", va="top", color=INK)

    src = box(ax, 1.32, 3.30, 2.10, 0.86,
              "Retirement age\n$R\\uparrow$, so $\\rho\\downarrow$", ec=INK,
              fc="#f2f2f2", fs=8.6)

    ch = [
        (5.10, 4.90, GOLD, "#fdf6e7", "QUOTA ROUTE",
         "fewer retirements $\\Rightarrow$ fewer\nestablishment vacancies $v_Q$"),
        (5.10, 3.30, TEAL, "#eaf4f2", "HORIZON ROUTE",
         "jobs last longer, so both\nsides value them more"),
        (5.10, 1.70, NAVY, "#eef2f9", "DEMOGRAPHIC ROUTE",
         "the labour force grows while\n$\\bar N$ stays fixed"),
    ]
    boxes = []
    for x, y, ec, fc, head, body in ch:
        b = box(ax, x, y, 3.55, 1.02, head + "\n" + body, ec=ec, fc=fc, fs=7.8)
        boxes.append(b)
        arrow(ax, anchor(src, "r"), anchor(b, "l"), color=ec, rad=0.0, lw=1.3)

    eff = [("$-1.03$", GOLD), ("$+0.66$", TEAL), ("$+0.52$", NAVY)]
    for (b, (val, col)) in zip(boxes, eff):
        ax.text(7.28, b["y"], val, ha="center", va="center", fontsize=9.0,
                color=col, fontweight="bold")
    ax.text(7.28, 6.02, "effect on the youth unemployment\nrate (log points × 100)",
            ha="center", va="center", fontsize=7.2, color=GREY,
            linespacing=1.35)

    ax.plot([7.90, 7.90], [1.20, 4.90], color=GREY, lw=0.8, ls=":")
    box(ax, 9.42, 3.30, 2.85, 1.02,
        "SUM $= +0.16$\nthe headline rate\nbarely moves", ec=INK, fc="white",
        fs=8.2)
    for b in boxes:
        arrow(ax, (7.62, b["y"]), anchor(dict(x=9.42, y=3.30, w=2.85, h=1.02),
                                         "l"), color=GREY, lw=0.9, rad=0.0,
              dashed=True, zorder=2)

    ax.add_patch(FancyBboxPatch((0.15, 0.10), 10.7, 0.62,
                                boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc="#fdf6e7", ec=GOLD, lw=0.9, zorder=1))
    ax.text(5.50, 0.41,
            "Only the first route reaches what a new entrant actually cares "
            "about: the chance of ever holding a rationed job falls 5.7 per "
            "cent,\nand the decomposition attributes all of that fall to the "
            "quota route. The indicator is silent because the other two routes "
            "offset it.",
            ha="center", va="center", fontsize=7.8, color=INK, linespacing=1.45)

    fig.tight_layout()
    out = os.path.join(FIGS, "fig2_mechanism.png")
    fig.savefig(out)
    plt.close(fig)
    print("  ", os.path.basename(out))


if __name__ == "__main__":
    print("schematics:")
    figure1()
    figure2()
