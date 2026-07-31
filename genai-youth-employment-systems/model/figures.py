# -*- coding: utf-8 -*-
"""Every figure in the manuscript, drawn from the simulation output."""
from __future__ import annotations

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch, Ellipse
from matplotlib.lines import Line2D

import experiments as X

FIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "figures"))
os.makedirs(FIG, exist_ok=True)

CM = 1 / 2.54
W = 17.0 * CM          # full text width of the MDPI Systems layout

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 8.0,
    "axes.labelsize": 8.0,
    "axes.titlesize": 8.5,
    "legend.fontsize": 7.2,
    "legend.framealpha": 0.93,
    "legend.fancybox": False,
    "legend.edgecolor": "0.75",
    "legend.borderpad": 0.35,
    "legend.labelspacing": 0.28,
    "legend.handlelength": 1.9,
    "xtick.labelsize": 7.2,
    "ytick.labelsize": 7.2,
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "lines.linewidth": 1.4,
    "figure.dpi": 400,
    "savefig.dpi": 400,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

C_DISP = "#B03A2E"      # displacement / balancing
C_REIN = "#1F618D"      # reinstatement / augmentation
C_LEARN = "#117A65"     # learning
C_PIPE = "#7D3C98"      # pipeline
C_SCALE = "#B7770B"     # scale
GREY = "#4D4D4D"


def _save(fig, name):
    path = os.path.join(FIG, name)
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)
    return path


def _panel_tag(ax, tag, dx=-0.115, dy=1.06):
    ax.text(dx, dy, tag, transform=ax.transAxes, fontweight="bold",
            fontsize=8.5, va="top", ha="left")


# ===========================================================================
# Figure 1 - causal loop diagram
# ===========================================================================
class Node:
    def __init__(self, ax, x, y, text, w, h=0.78, fc="white", fs=7.1):
        self.x, self.y, self.w, self.h = x, y, w, h
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.04,rounding_size=0.10",
                                    fc=fc, ec=GREY, lw=0.85, zorder=3))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4,
                linespacing=1.25)

    def anchor(self, tx, ty, pad=0.10):
        """Point on the box boundary in the direction of (tx, ty)."""
        dx, dy = tx - self.x, ty - self.y
        if abs(dx) < 1e-9 and abs(dy) < 1e-9:
            return self.x, self.y
        sx = (self.w / 2 + pad) / abs(dx) if abs(dx) > 1e-9 else np.inf
        sy = (self.h / 2 + pad) / abs(dy) if abs(dy) > 1e-9 else np.inf
        s = min(sx, sy)
        return self.x + s * dx, self.y + s * dy


def _link(ax, n1, n2, sign="+", color=GREY, rad=0.0, lab_t=0.5, lab_off=(0, 0),
          lw=1.15, nudge=0.30):
    """Curved causal link between two nodes, anchored on their boundaries.

    The polarity marker is placed beside the curve (perpendicular offset) so
    that it never breaks the arrow.
    """
    p = n1.anchor(n2.x, n2.y)
    q = n2.anchor(n1.x, n1.y)
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle="arc3,rad=%.3f" % rad,
                                 arrowstyle="-|>", mutation_scale=9.5, lw=lw,
                                 color=color, shrinkA=0.5, shrinkB=0.5,
                                 zorder=2))
    cx = (p[0] + q[0]) / 2 + rad * (q[1] - p[1])
    cy = (p[1] + q[1]) / 2 - rad * (q[0] - p[0])
    t = lab_t
    lx = (1 - t) ** 2 * p[0] + 2 * (1 - t) * t * cx + t ** 2 * q[0]
    ly = (1 - t) ** 2 * p[1] + 2 * (1 - t) * t * cy + t ** 2 * q[1]
    # tangent -> outward normal
    tx = 2 * (1 - t) * (cx - p[0]) + 2 * t * (q[0] - cx)
    ty = 2 * (1 - t) * (cy - p[1]) + 2 * t * (q[1] - cy)
    n = max((tx ** 2 + ty ** 2) ** 0.5, 1e-9)
    nx, ny = -ty / n, tx / n
    ax.text(lx + nx * nudge + lab_off[0], ly + ny * nudge + lab_off[1], sign,
            ha="center", va="center", fontsize=8.6, color=color,
            fontweight="bold", zorder=6,
            bbox=dict(fc="white", ec="none", pad=0.35))


def _loop_label(ax, xy, text, color, rx=0.78, ry=0.44):
    ax.add_patch(Ellipse(xy, rx * 2, ry * 2, fc="white", ec=color, lw=1.0,
                         zorder=6))
    ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=7.4,
            color=color, fontweight="bold", zorder=7)


def figure1():
    fig, ax = plt.subplots(figsize=(W, W * 0.72))
    ax.set_xlim(0.55, 16.15)
    ax.set_ylim(-0.30, 10.35)
    ax.axis("off")

    A = Node(ax, 3.1, 9.7, "GenAI capability\n$A$", 2.65, fc="#EAF2F8")
    K = Node(ax, 10.6, 9.7, "Human–AI collaboration\nroutines  $K$", 3.55,
             fc="#E8F6F3")
    AL = Node(ax, 3.1, 7.3, "Automation of\nentry tasks  $\\alpha$", 2.65,
              fc="#FDEDEC")
    RH = Node(ax, 10.6, 7.3, "Task reinstatement\nto juniors  $\\rho$", 3.05,
              fc="#EAF2F8")
    PI = Node(ax, 3.1, 4.9, "Junior effective\nproductivity  $\\pi_J$", 2.65)
    IJ = Node(ax, 6.9, 6.1, "Entry-port task\nvolume  $i_J Y$", 2.60)
    JJ = Node(ax, 6.9, 3.3, "Early-career\nemployment  $J$", 2.60, fc="#FEF9E7")
    CC = Node(ax, 3.1, 2.5, "Unit cost  $C$", 2.20, h=0.62)
    YY = Node(ax, 6.9, 0.7, "Output  $Y$", 2.20, h=0.62)
    PR = Node(ax, 10.9, 3.3, "Promotions  $c$", 2.35, h=0.62, fc="#F4ECF7")
    SS = Node(ax, 14.4, 5.3, "Experienced\nstaff  $S$", 2.35, fc="#F4ECF7")
    QQ = Node(ax, 10.9, 1.0, "Mentoring\nadequacy  $q$", 2.35, fc="#F4ECF7")

    # B1 entry-port displacement
    _link(ax, A, AL, "+", C_DISP, nudge=-0.34)
    _link(ax, AL, IJ, "−", C_DISP, nudge=0.34)
    _link(ax, IJ, JJ, "+", C_DISP, nudge=-0.30)
    _link(ax, JJ, K, "+", C_LEARN, rad=-0.26, lab_t=0.16, nudge=-0.42)
    _link(ax, K, A, "+", C_LEARN, nudge=0.34)
    # B2 productivity and headcount
    _link(ax, A, PI, "+", C_SCALE, rad=0.42, lab_t=0.80, nudge=0.42)
    _link(ax, PI, JJ, "−", C_SCALE, nudge=0.32)
    # R4 scale and competitiveness
    _link(ax, PI, CC, "−", C_SCALE, nudge=-0.32)
    _link(ax, CC, YY, "−", C_SCALE, nudge=0.34)
    _link(ax, YY, IJ, "+", C_SCALE, rad=-0.70, lab_t=0.5, nudge=0.55)
    # R1 task reinstatement
    _link(ax, K, RH, "+", C_LEARN, nudge=-0.36)
    _link(ax, RH, IJ, "+", C_REIN, lab_t=0.62, nudge=-0.34)
    # R2 learning engine
    _link(ax, SS, K, "+", C_LEARN, rad=0.26, lab_t=0.5, nudge=0.36)
    # R3 development pipeline
    _link(ax, JJ, PR, "+", C_PIPE, nudge=0.32)
    _link(ax, PR, SS, "+", C_PIPE, nudge=-0.34)
    _link(ax, SS, QQ, "+", C_PIPE, rad=-0.34, lab_t=0.5, nudge=-0.36)
    _link(ax, QQ, PR, "+", C_PIPE, nudge=0.32)

    _loop_label(ax, (4.95, 8.85), "B1", C_DISP)
    _loop_label(ax, (3.95, 3.60), "B2", C_SCALE)
    _loop_label(ax, (3.30, 0.95), "R4", C_SCALE)
    _loop_label(ax, (10.30, 5.55), "R1", C_REIN)
    _loop_label(ax, (13.65, 9.45), "R2", C_LEARN)
    _loop_label(ax, (13.05, 2.10), "R3", C_PIPE)

    handles = [
        Line2D([], [], color=C_DISP, lw=1.7,
               label="B1  entry-port displacement (balancing)"),
        Line2D([], [], color=C_SCALE, lw=1.7,
               label="B2 productivity–headcount / R4 scale"),
        Line2D([], [], color=C_REIN, lw=1.7,
               label="R1  task reinstatement (reinforcing)"),
        Line2D([], [], color=C_LEARN, lw=1.7,
               label="R2  organisational learning engine (reinforcing)"),
        Line2D([], [], color=C_PIPE, lw=1.7,
               label="R3  development pipeline (reinforcing)"),
    ]
    ax.legend(handles=handles, loc="lower center", ncol=3, frameon=False,
              bbox_to_anchor=(0.5, -0.055), handlelength=2.0,
              columnspacing=1.6, fontsize=7.0)
    return _save(fig, "figure1_cld.png")


# ===========================================================================
# Figure 2 - stock and flow diagram
# ===========================================================================
def _stock(ax, xy, label, w=2.9, h=1.00, fc="#EAF2F8"):
    x, y = xy
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=fc, ec=GREY,
                           lw=1.1, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=7.4, zorder=4,
            linespacing=1.25)
    return dict(x=x, y=y, w=w, h=h)


def _cloud(ax, xy, r=0.32):
    for dx, dy, rr in ((0, 0, r), (-r * 0.8, -r * 0.25, r * 0.7),
                       (r * 0.8, -r * 0.25, r * 0.7)):
        ax.add_patch(Ellipse((xy[0] + dx, xy[1] + dy), rr * 2, rr * 1.5,
                             fc="white", ec=GREY, lw=0.8, zorder=3))


def _valve(ax, xy, s=0.20):
    ax.plot([xy[0] - s, xy[0] + s, xy[0] - s, xy[0] + s, xy[0] - s],
            [xy[1] - s, xy[1] + s, xy[1] + s, xy[1] - s, xy[1] - s],
            color=GREY, lw=0.9, zorder=5)
    ax.add_patch(Ellipse(xy, 0.0, 0.0))


def _pipe(ax, p, q, color=GREY):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=13,
                                 lw=2.4, color=color, shrinkA=0, shrinkB=0,
                                 zorder=2))


def _info(ax, p, q, rad=0.25, color="#7F8C8D"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=7.5,
                                 lw=0.85, color=color,
                                 linestyle=(0, (3.2, 2.0)),
                                 shrinkA=3, shrinkB=3, zorder=1,
                                 connectionstyle="arc3,rad=%.2f" % rad))


def figure2():
    fig, ax = plt.subplots(figsize=(W, W * 0.60))
    ax.set_xlim(0, 16.6)
    ax.set_ylim(0.1, 9.5)
    ax.axis("off")

    _stock(ax, (5.4, 7.6), "$J$\nearly-career\nstaff", w=3.2, h=1.30,
           fc="#FEF9E7")
    _stock(ax, (11.7, 7.6), "$S$\nexperienced\nstaff", w=3.2, h=1.30,
           fc="#F4ECF7")
    _stock(ax, (5.4, 2.4), "$K$\ncollaboration\nroutines", w=3.2, h=1.30,
           fc="#E8F6F3")
    _stock(ax, (11.7, 2.4), "$A$\nGenAI\ncapability", w=3.2, h=1.30,
           fc="#EAF2F8")

    def hflow(x0, x1, y, lab, color, up=True, fs=7.0):
        _pipe(ax, (x0, y), (x1, y), color)
        xv = (x0 + x1) / 2
        _valve(ax, (xv, y))
        ax.text(xv, y + (0.78 if up else -0.86), lab, ha="center",
                va="center", fontsize=fs, color=color, linespacing=1.25)

    def vflow(x, y0, y1, lab, color, side=1, fs=7.0):
        _pipe(ax, (x, y0), (x, y1), color)
        yv = (y0 + y1) / 2
        _valve(ax, (x, yv))
        ax.text(x + 0.48 * side, yv, lab, ha="left" if side > 0 else "right",
                va="center", fontsize=fs, color=color, linespacing=1.25)

    _cloud(ax, (1.15, 7.6))
    hflow(1.55, 3.80, 7.6, "hiring  $h$", C_REIN)
    hflow(7.00, 10.10, 7.6, "promotion\n$c=\\psi\\,x\\,J/\\tau_{dev}$", C_PIPE)
    hflow(13.30, 15.35, 7.6, "separations\n$\\delta_S S$", C_DISP)
    _cloud(ax, (15.75, 7.6))
    vflow(5.4, 6.95, 5.55, "separations $\\delta_J J$", C_DISP, side=1)
    _cloud(ax, (5.4, 5.20))

    _cloud(ax, (1.15, 2.4))
    hflow(1.55, 3.80, 2.4, "learning by collaborating\n"
          "$\\ell = 2\\lambda\\, u\\,\\sqrt{J S}\\,/\\,N_{ref}$", C_LEARN)
    hflow(7.00, 8.55, 2.4, "obsolescence\n$\\delta_K K$", C_DISP, up=False)
    
    _cloud(ax, (8.95, 2.4))
    hflow(15.35, 13.30, 2.4, "adoption\n$\\nu\\Lambda_A (F-A)$", C_LEARN)
    _cloud(ax, (15.75, 2.4))
    ax.text(15.75, 1.55, "external\nfrontier $F(t)$", ha="center", va="center",
            fontsize=6.9, color=GREY, linespacing=1.25)
    vflow(11.7, 1.75, 0.95, "$\\delta_A A$", C_DISP, side=1)
    _cloud(ax, (11.7, 0.60))

    _info(ax, (10.55, 3.05), (6.75, 7.00), rad=0.20)
    ax.text(7.60, 5.05, "$\\alpha,\\ u,\\ \\pi_J,\\ \\pi_S$", fontsize=7.2,
            color="#7F8C8D", ha="center",
            bbox=dict(fc="white", ec="none", pad=0.6))
    _info(ax, (3.95, 3.05), (3.95, 6.95), rad=0.22)
    ax.text(2.95, 5.05, "$\\Lambda,\\ \\rho,\\ x$", fontsize=7.2,
            color="#7F8C8D", ha="center",
            bbox=dict(fc="white", ec="none", pad=0.6))
    _info(ax, (10.30, 6.95), (8.62, 7.30), rad=-0.55)
    ax.text(9.50, 6.20, "mentoring\nadequacy $q$", fontsize=7.0,
            color="#7F8C8D", ha="center", linespacing=1.25,
            bbox=dict(fc="white", ec="none", pad=0.6))
    return _save(fig, "figure2_sfd.png")


# ===========================================================================
# Figure 3 - baseline behaviour
# ===========================================================================
def figure3(r0, r1):
    t = r1["t"]
    fig, axes = plt.subplots(2, 3, figsize=(W, W * 0.60))
    (a, b, c), (d, e, f) = axes

    a.plot(t, r1["A"], color=C_REIN, label="$A$ capability")
    a.plot(t, r1["u"], color=C_SCALE, ls="--", label="$u$ utilisation")
    a.plot(t, r1["Lam"], color=C_LEARN, ls="-.", label="$\\Lambda$ absorptive capacity")
    a.plot(t, r1["K"] / 2.0, color=C_PIPE, ls=":", label="$K/2$ routines")
    a.set_ylabel("index"); a.set_ylim(0, 1.06); a.legend(loc="lower right", fontsize=6.6)
    _panel_tag(a, "(a)")

    b.plot(t, r1["alpha"], color=C_DISP, label="$\\alpha$ automated entry tasks")
    b.plot(t, r1["rho"], color=C_REIN, ls="--", label="$\\rho$ reinstated core tasks")
    b.plot(t, r1["iJ"] / r1["iJ"][0], color=GREY, ls=":",
           label="$i_J / i_J(0)$ entry-port intensity")
    b.set_ylabel("share"); b.set_ylim(0, 1.55)
    b.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    b.legend(loc="upper right", fontsize=6.6)
    _panel_tag(b, "(b)")

    c.plot(t, r1["J"], color=C_REIN, label="$J$ with GenAI")
    c.plot(t, r0["J"], color=C_REIN, ls=":", label="$J$ counterfactual")
    c.plot(t, r1["S"], color=C_PIPE, label="$S$ with GenAI")
    c.plot(t, r0["S"], color=C_PIPE, ls=":", label="$S$ counterfactual")
    c.set_ylabel("persons"); c.set_ylim(200, 1160); c.legend(loc="upper left", fontsize=6.6)
    _panel_tag(c, "(c)")

    d.axhline(0, color="black", lw=0.6)
    d.plot(t, 100 * (r1["J"] / r0["J"] - 1), color=C_REIN, label="early-career $J$")
    d.plot(t, 100 * (r1["S"] / r0["S"] - 1), color=C_PIPE, ls="--",
           label="experienced $S$")
    d.plot(t, 100 * (r1["h"] / r0["h"] - 1), color=C_DISP, ls="-.",
           label="entry hiring $h$")
    d.set_ylabel("% deviation from counterfactual")
    d.set_ylim(-64, 14); d.legend(loc="lower right", fontsize=6.6); _panel_tag(d, "(d)")

    e.plot(t, r1["Phi"], color=C_DISP, label="$\\Phi$ output fulfilment")
    e.plot(t, r1["x"], color=C_LEARN, ls="--", label="$x$ experiential quality")
    e.plot(t, r1["Om"], color=C_PIPE, ls="-.", label="$\\Omega$ external availability")
    e.set_ylabel("ratio"); e.set_ylim(0.70, 1.04)
    e.legend(loc="lower right", fontsize=6.6)
    _panel_tag(e, "(e)")

    f.axhline(0, color="black", lw=0.6)
    f.plot(t, 100 * (r1["Y"] / r0["Y"] - 1), color=C_SCALE, label="output $Y$")
    f.plot(t, 100 * (r1["C"] / r0["C"] - 1), color=C_DISP, ls="--",
           label="unit cost $C$")
    f.set_ylabel("% deviation from counterfactual")
    f.set_ylim(-26, 22); f.legend(loc="upper left", fontsize=6.6); _panel_tag(f, "(f)")

    for ax in axes.ravel():
        ax.set_xlabel("years after the generative-AI shock")
        ax.set_xlim(0, t[-1])
        ax.grid(alpha=0.25, lw=0.5)
    fig.tight_layout(w_pad=1.6, h_pad=1.7)
    return _save(fig, "figure3_baseline.png")


# ===========================================================================
# Figure 4 - entry-port elasticity decomposition
# ===========================================================================
def figure4(r1, runs):
    t = r1["t"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, W * 0.36))

    a.axhline(0, color="black", lw=0.6)
    a.plot(t, r1["reinstatement"], color=C_REIN,
           label="reinstatement contribution")
    a.plot(t, -r1["displacement"], color=C_DISP, ls="--",
           label="displacement contribution")
    a.plot(t, -r1["productivity"], color=C_SCALE, ls="-.",
           label="headcount-saving contribution")
    a.plot(t, r1["E"], color="black", lw=1.8,
           label="net elasticity $\\mathcal{E}$")
    a.set_ylabel("contribution to $\\partial \\ln D_J / \\partial \\ln A$")
    a.set_ylim(-0.60, 0.13)
    a.legend(loc="lower left", fontsize=6.6); _panel_tag(a, "(a)")

    b.axhline(0, color="black", lw=0.6)
    styles = {"S0": ("-", "black"), "S1": ("--", C_DISP), "S2": ("-.", C_LEARN),
              "S3": (":", C_REIN), "S6": ("-", C_SCALE)}
    names = {"S0": "S0 baseline", "S1": "S1 automation-first",
             "S2": "S2 learning system", "S3": "S3 work redesign",
             "S6": "S6 joint package"}
    for k, (ls, col) in styles.items():
        b.plot(t, runs[k]["E"], ls=ls, color=col, label=names[k],
               lw=1.7 if k == "S6" else 1.3)
    b.set_ylabel("net entry-port elasticity $\\mathcal{E}$")
    b.set_ylim(-0.84, 0.08)
    b.legend(loc="lower left", fontsize=6.6); _panel_tag(b, "(b)")

    for ax in (a, b):
        ax.set_xlabel("years after the generative-AI shock")
        ax.set_xlim(0, t[-1]); ax.grid(alpha=0.25, lw=0.5)
    fig.tight_layout(w_pad=2.0)
    return _save(fig, "figure4_elasticity.png")


# ===========================================================================
# Figure 5 - regime maps
# ===========================================================================
def figure5(grid):
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, W * 0.40))
    lv = np.linspace(-70, 25, 20)

    def draw(ax, xs, ys, Z, xlabel, ylabel, marker):
        cf = ax.contourf(xs, ys, Z, levels=lv, cmap="RdYlBu", extend="both")
        cs = ax.contour(xs, ys, Z, levels=[0], colors="black", linewidths=1.6)
        ax.clabel(cs, fmt={0: "$\\Delta J=0$"}, fontsize=6.8)
        ax.contour(xs, ys, Z, levels=[-40, -20], colors="black",
                   linewidths=0.5, linestyles=":")
        ax.plot(*marker, marker="o", ms=5.5, mfc="white", mec="black", mew=1.1)
        ax.annotate("baseline", marker, textcoords="offset points",
                    xytext=(7, -9), fontsize=6.8)
        ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
        return cf

    cf = draw(a, grid["rhos"], grid["alphas"], grid["G1"],
              "reinstatement ceiling  $\\rho_{max}$",
              "automation ceiling  $\\alpha_{max}$",
              (X.BASE.rho_max, X.BASE.alpha_max))
    _panel_tag(a, "(a)")
    draw(b, grid["rhos"], grid["lams"], grid["G2"],
         "reinstatement ceiling  $\\rho_{max}$",
         "learning investment rate  $\\lambda$",
         (X.BASE.rho_max, X.BASE.lam))
    _panel_tag(b, "(b)")

    cb = fig.colorbar(cf, ax=(a, b), fraction=0.035, pad=0.02)
    cb.set_label("$\\Delta J$ at year 25 (% vs. counterfactual)", fontsize=7.4)
    cb.ax.tick_params(labelsize=7.0)
    return _save(fig, "figure5_regimes.png")


# ===========================================================================
# Figure 6 - policy experiments
# ===========================================================================
def figure6(r0, runs, pol):
    fig = plt.figure(figsize=(W, W * 0.42))
    a = fig.add_axes([0.065, 0.155, 0.40, 0.80])
    b = fig.add_axes([0.575, 0.155, 0.405, 0.80])

    t = runs["S0"]["t"]
    order = ["S1", "S0", "S5", "S4", "S2", "S3", "S6"]
    cols = {"S0": "black", "S1": C_DISP, "S2": C_LEARN, "S3": C_REIN,
            "S4": C_PIPE, "S5": "#7F8C8D", "S6": C_SCALE}
    lss = {"S0": "-", "S1": "--", "S2": "-.", "S3": ":", "S4": (0, (4, 1.4, 1, 1.4)),
           "S5": (0, (1.6, 1.6)), "S6": "-"}
    label = {r[0]: r[1] for r in pol}
    a.axhline(0, color="black", lw=0.6)
    for k in order:
        a.plot(t, 100 * (runs[k]["J"] / r0["J"] - 1), ls=lss[k], color=cols[k],
               lw=2.0 if k in ("S0", "S6") else 1.25,
               label="%s  %s" % (k, label[k]))
    for k in order:
        yv = 100 * (runs[k]["J"][-1] / r0["J"][-1] - 1)
        a.annotate(k, (t[-1], yv), xytext=(4, -2.5), textcoords="offset points",
                   fontsize=6.9, color=cols[k], fontweight="bold", va="center")
    a.set_xlabel("years after the generative-AI shock")
    a.set_ylabel("early-career employment,\n% deviation from counterfactual")
    a.set_xlim(0, t[-1] * 1.075); a.grid(alpha=0.25, lw=0.5)
    _panel_tag(a, "(a)", dx=-0.145)

    codes = [r[0] for r in pol]
    dJ = np.array([r[3] for r in pol], float)
    dS = np.array([r[5] for r in pol], float)
    dY = np.array([r[7] for r in pol], float)
    phi = np.array([r[9] for r in pol], float)
    idx = np.arange(len(codes))
    w = 0.26
    b.axhline(0, color="black", lw=0.6)
    b.bar(idx - w, dJ, w, color=C_REIN, label="$\\Delta J$")
    b.bar(idx, dS, w, color=C_PIPE, label="$\\Delta S$")
    b.bar(idx + w, dY, w, color=C_SCALE, label="$\\Delta Y$")
    b.set_xticks(idx); b.set_xticklabels(codes)
    b.set_ylabel("% deviation from counterfactual at year 25")
    b.grid(axis="y", alpha=0.25, lw=0.5)
    b.legend(loc="upper left", ncol=3, frameon=False)
    b2 = b.twinx()
    b2.plot(idx, phi, marker="D", ms=4.2, color="black", lw=1.1, ls="--",
            label="$\\Phi$ (right axis)")
    b2.set_ylabel("output fulfilment ratio $\\Phi$", fontsize=7.6)
    b2.set_ylim(0.60, 1.05); b2.tick_params(labelsize=7.0)
    b2.legend(loc="lower right", frameon=False)
    _panel_tag(b, "(b)", dx=-0.135)
    return _save(fig, "figure6_policies.png")


# ===========================================================================
# Figure 7 - global sensitivity
# ===========================================================================
def figure7(srows):
    raw = np.load(os.path.join(X.OUT, "sensitivity_raw.npz"))
    fig = plt.figure(figsize=(W, W * 0.42))
    a = fig.add_axes([0.365, 0.14, 0.335, 0.82])
    b = fig.add_axes([0.795, 0.14, 0.190, 0.82])

    sym = {"alpha_max": "$\\alpha_{max}$", "rho_max": "$\\rho_{max}$",
           "lambda": "$\\lambda$", "delta_K": "$\\delta_K$",
           "beta_J": "$\\beta_J$", "beta_S": "$\\beta_S$", "eta": "$\\eta$",
           "zeta_0": "$\\zeta_0$", "tau_dev": "$\\tau_{dev}$", "q_0": "$q_0$",
           "nu": "$\\nu$", "epsilon": "$\\varepsilon$",
           "delta_S": "$\\delta_S$", "chi_S": "$\\chi_S$", "omega": "$\\omega$"}

    def pretty(lab):
        head, _, tail = lab.rpartition(", ")
        return "%s, %s" % (head, sym.get(tail, tail)) if head else lab

    rows = srows[::-1]
    labs = [pretty(r[0]) for r in rows]
    vals = np.array([r[2] for r in rows], float)
    cols = [C_REIN if v > 0 else C_DISP for v in vals]
    y = np.arange(len(vals))
    a.barh(y, vals, color=cols, height=0.66)
    a.set_yticks(y); a.set_yticklabels(labs, fontsize=6.6)
    a.axvline(0, color="black", lw=0.7)
    a.set_xlabel("partial rank correlation coefficient with $\\Delta J$ (year 25)")
    a.set_xlim(-1.05, 1.05); a.grid(axis="x", alpha=0.25, lw=0.5)
    _panel_tag(a, "(a)", dx=-0.90)

    yJ = raw["yJ"]
    b.hist(yJ, bins=28, color="#5D6D7E", ec="white", lw=0.4,
           orientation="horizontal")
    b.axhline(np.median(yJ), color=C_DISP, lw=1.4, ls="--")
    b.set_ylabel("$\\Delta J$ at year 25 (%)")
    b.set_xlabel("runs")
    b.grid(alpha=0.25, lw=0.5)
    b.text(0.96, 0.03, "median %.1f%%\n5–95%%: %.0f to %.0f%%"
           % (np.median(yJ), np.percentile(yJ, 5), np.percentile(yJ, 95)),
           transform=b.transAxes, ha="right", va="bottom", fontsize=6.6)
    _panel_tag(b, "(b)", dx=-0.52)
    return _save(fig, "figure7_sensitivity.png")


# ===========================================================================
if __name__ == "__main__":
    r0, r1, brows = X.baseline()
    pol, syn, runs, r0p = X.policies()
    grid = np.load(os.path.join(X.OUT, "regime_grid.npz"))
    srows = [l.rstrip("\n").split("\t") for l in
             open(os.path.join(X.OUT, "table_sensitivity.tsv"), encoding="utf-8")][1:]
    srows = [[r[0], float(r[1]), float(r[2]), float(r[3]), float(r[4])]
             for r in srows]

    figure1()
    figure2()
    figure3(r0, r1)
    figure4(r1, runs)
    figure5(grid)
    figure6(r0p, runs, pol)
    figure7(srows)
