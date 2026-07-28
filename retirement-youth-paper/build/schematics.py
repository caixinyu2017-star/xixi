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
def poly(ax, pts, color=NAVY, lw=1.15, dashed=False, label=None, lxy=None,
         fs=7.6, zorder=5, head=True):
    """An orthogonal connector: straight segments, arrowhead on the last one."""
    ls = (0, (4.5, 2.6)) if dashed else "-"
    for i in range(len(pts) - 2):
        ax.plot([pts[i][0], pts[i + 1][0]], [pts[i][1], pts[i + 1][1]],
                color=color, lw=lw, ls=ls, solid_capstyle="round",
                zorder=zorder)
    p0, p1 = pts[-2], pts[-1]
    if head:
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>",
                                     mutation_scale=11, lw=lw, color=color,
                                     linestyle=ls, shrinkA=0, shrinkB=3.0,
                                     zorder=zorder))
    else:
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw, ls=ls,
                solid_capstyle="round", zorder=zorder)
    if label:
        ax.text(lxy[0], lxy[1], label, ha="center", va="center", fontsize=fs,
                color=color, zorder=9, path_effects=HALO)


def figure1():
    fig, ax = plt.subplots(figsize=(7.2, 4.7))
    ax.set_xlim(0, 15.2)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    A, B, C, D = 2.7, 6.0, 9.3, 12.6          # columns
    W, H = 2.35, 0.86                         # box size
    YY, YP = 7.0, 3.1                         # young and prime rows
    hw, hh = W / 2, H / 2
    LQ, LD = 1.62, 1.00                       # the two lower routing lanes
    XQ = 7.57                                 # the queue's descent corridor

    ax.add_patch(FancyBboxPatch((0.15, 5.80), 14.9, 3.10,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc="#f7f9fc", ec="none", zorder=0))
    ax.add_patch(FancyBboxPatch((0.15, 2.30), 14.9, 2.10,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                fc="#fbf7f4", ec="none", zorder=0))
    ax.text(0.32, 8.82, "YOUNG   ages $a_0$ to $a_0+T_y$", ha="left", va="top",
            fontsize=7.8, color=NAVY, fontweight="bold")
    ax.text(0.32, 4.32, "PRIME-AGE   until retirement at $R$", ha="left",
            va="top", fontsize=7.8, color=RUST, fontweight="bold")

    # ------------------------------------------------------------- states
    box(ax, A, YY, W, H, "Open search\n$u_m$", ec=NAVY)
    box(ax, B, YY, W, H, "Market job\n$e_m$", ec=NAVY, fc="#eef2f9")
    box(ax, C, YY, W, H, "Queueing\n$u_q$", ec=GOLD, fc="#fdf6e7")
    box(ax, D, YY, W, H, "Rationed job\n$e_q$", ec=GOLD, fc="#fdf6e7")
    box(ax, A, YP, W, H, "Open search\n$U_m$", ec=RUST)
    box(ax, B, YP, W, H, "Market job\n$E_m$", ec=RUST, fc="#fbeeea")
    box(ax, D, YP, W, H, "Rationed job\n$E_q$", ec=GOLD, fc="#fdf6e7")

    # the establishment constraint, between the two rationed-job boxes
    box(ax, C, YP, W + 0.30, H + 0.20,
        "$e_q+E_q=\\bar N$\n$v_Q=\\delta_Q\\bar N+\\rho E_q$",
        ec=GOLD, fc="white", fs=8.0, lw=1.0, ls=(0, (3.5, 2.2)))
    ax.text(C, YP - hh - 0.34, "the establishment cannot expand",
            ha="center", va="top", fontsize=7.0, color=GOLD, style="italic")

    # ------------------------------------------------------------- entry
    cloud(ax, 0.78, YY, s=0.21)
    ax.text(0.78, YY - 0.62, "entrants\n$n$", ha="center", va="top",
            fontsize=7.4, color=GREY, linespacing=1.3)
    poly(ax, [(1.16, YY), (A - hw, YY)], color=GREY, lw=1.05)
    poly(ax, [(0.78, YY + 0.40), (0.78, 8.55), (C, 8.55), (C, YY + hh)],
         color=GREY, lw=1.05,
         label="a share $a_q$ prepares for the examination",
         lxy=(7.4, 8.82), fs=7.4)

    # ------------------------------------------------------------- matching
    poly(ax, [(A + hw, YY + 0.20), (B - hw, YY + 0.20)], color=NAVY,
         label="$f_y=\\mu_y\\theta^{1-\\eta}$", lxy=(4.35, YY + 0.56))
    poly(ax, [(B - hw, YY - 0.20), (A + hw, YY - 0.20)], color=NAVY,
         label="$\\delta_M$", lxy=(4.35, YY - 0.54))
    poly(ax, [(A + hw, YP + 0.20), (B - hw, YP + 0.20)], color=RUST,
         label="$f_p=\\theta^{1-\\eta}$", lxy=(4.35, YP + 0.56))
    poly(ax, [(B - hw, YP - 0.20), (A + hw, YP - 0.20)], color=RUST,
         label="$\\delta_M$", lxy=(4.35, YP - 0.54))
    poly(ax, [(C + hw, YY), (D - hw, YY)], color=GOLD, lw=1.6,
         label="$\\lambda_Q=v_Q/u_q$", lxy=(10.95, YY + 0.66))

    # ------------------------------------------------------------- ageing
    for x, col in ((A, GREY), (B, GREY), (D, GOLD)):
        poly(ax, [(x, YY - hh), (x, YP + hh)], color=col, lw=1.05, dashed=True)
    ax.text(B + 0.30, (YY + YP) / 2 + 0.15, "ageing\n$\\gamma=1/T_y$",
            ha="left", va="center", fontsize=7.6, color=GREY,
            linespacing=1.3, path_effects=HALO)
    poly(ax, [(C - hw, YY), (XQ, YY), (XQ, LQ), (A + 0.62, LQ),
              (A + 0.62, YP - hh)],
         color=GREY, lw=1.05, dashed=True, label="$\\gamma$",
         lxy=(5.6, LQ + 0.26), fs=7.6)

    # ---------------------------------------- separations from the quota
    poly(ax, [(D, YP - hh), (D, LD), (A - 0.62, LD), (A - 0.62, YP - hh)],
         color=GOLD, lw=1.05, dashed=True, label="$\\delta_Q$",
         lxy=(9.9, LD + 0.26), fs=7.6)

    # ------------------------------------------------------------- exit
    cloud(ax, 14.42, YP, s=0.20)
    ax.text(14.42, YP - 0.58, "retirement\n$\\rho$", ha="center", va="top",
            fontsize=7.4, color=GREY, linespacing=1.3)
    poly(ax, [(D + hw, YP), (14.06, YP)], color=GREY, lw=1.05, dashed=True)

    ax.text(7.6, 9.28,
            "Worker flows between the rationed and the market sector",
            fontsize=9.6, fontweight="bold", ha="center", va="center",
            color=INK)
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

    # the three contributions are summed at an explicit junction: a short
    # feeder from each value, one vertical spine, one arrow out.  Three
    # separate arrows converging on the same point were unreadable.
    XF, XS = 7.62, 8.24
    for b in boxes:
        ax.plot([XF, XS], [b["y"], b["y"]], color=GREY, lw=1.0,
                solid_capstyle="round", zorder=2)
    ax.plot([XS, XS], [boxes[-1]["y"], boxes[0]["y"]], color=GREY, lw=1.0,
            solid_capstyle="round", zorder=2)
    for b in boxes:
        ax.add_patch(Circle((XS, b["y"]), 0.055, fc=GREY, ec=GREY, zorder=3))

    sm = box(ax, 9.80, 3.30, 2.18, 1.02,
             "SUM $= +0.16$\nthe headline rate\nbarely moves", ec=INK,
             fc="white", fs=8.2)
    arrow(ax, (XS, 3.30), anchor(sm, "l"), color=GREY, lw=1.2, rad=0.0,
          zorder=4)

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
