# -*- coding: utf-8 -*-
"""Publication figures for the YSTS paper (600 dpi PNG)."""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Arc
from matplotlib.lines import Line2D

import model as M

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.abspath(os.path.join(HERE, "..", "figs"))
os.makedirs(FIGS, exist_ok=True)
D = json.load(open(os.path.join(HERE, "stats.json")))
P = dict(D["params"])
Y0 = np.array(D["calibration"]["y0_2015"])

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Liberation Serif", "DejaVu Serif"],
    "font.size": 8.5, "axes.labelsize": 8.5, "axes.titlesize": 9,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
    "axes.linewidth": 0.7, "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "lines.linewidth": 1.3, "savefig.dpi": 600, "figure.dpi": 150,
    "axes.spines.top": False, "axes.spines.right": False,
    "mathtext.fontset": "dejavuserif",
})

NAVY, TEAL, ORANGE, GREY, RED = "#1F3864", "#2E8B92", "#D2691E", "#6E6E6E", "#B03A2E"
GREEN = "#4E7B3A"


def save(fig, name):
    path = os.path.join(FIGS, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  wrote", name)


# ------------------------------------------------------------------ Figure 1
def box(ax, xy, w, h, text, fc="white", ec=NAVY, fs=7.6, lw=0.9, bold=False):
    x, y = xy
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.012,rounding_size=0.05",
                                fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4,
            fontweight="bold" if bold else "normal", color="#12203F")
    return (x, y, w, h)


def anchor(a, b):
    """Point on the border of box a facing box b."""
    ax_, ay, aw, ah = a
    bx, by = b[0], b[1]
    dx, dy = bx - ax_, by - ay
    if dx == 0 and dy == 0:
        return ax_, ay
    sx = aw / 2 / abs(dx) if dx else np.inf
    sy = ah / 2 / abs(dy) if dy else np.inf
    s = min(sx, sy)
    return ax_ + dx * s, ay + dy * s


def link(ax, a, b, sign, color=GREY, rad=0.0, lw=0.9, soff=0.0, fs=8, ls="-"):
    """Draw a signed causal link.  The polarity sign is placed at the exact
    midpoint of the quadratic Bezier used by matplotlib's arc3 connector."""
    p0, p1 = anchor(a, b), anchor(b, a)
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle="-|>", mutation_scale=8,
                                 lw=lw, color=color, zorder=2, linestyle=ls,
                                 shrinkA=1.5, shrinkB=2.5))
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    sx, sy = mx + rad * dy / 2.0, my - rad * dx / 2.0
    n = np.hypot(dx, dy) or 1.0
    sx += soff * (-dy / n); sy += soff * (dx / n)
    ax.text(sx, sy, sign, color=color, fontsize=fs, ha="center", va="center",
            zorder=6, fontweight="bold",
            bbox=dict(fc="white", ec="none", pad=0.5))


def loop_marker(ax, xy, label, color, r=0.055):
    ax.add_patch(Arc(xy, 2 * r, 2 * r, angle=0, theta1=35, theta2=330,
                     color=color, lw=1.0, zorder=4))
    ax.annotate("", xy=(xy[0] + r * np.cos(np.deg2rad(35)),
                        xy[1] + r * np.sin(np.deg2rad(35))),
                xytext=(xy[0] + r * np.cos(np.deg2rad(55)),
                        xy[1] + r * np.sin(np.deg2rad(55))),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.0,
                                mutation_scale=7), zorder=4)
    ax.text(xy[0], xy[1], label, ha="center", va="center", fontsize=7.2,
            color=color, fontweight="bold", zorder=6,
            bbox=dict(fc="white", ec="none", pad=0.8))


def fig1_cld():
    fig, ax = plt.subplots(figsize=(7.3, 4.9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    W, H_ = 0.150, 0.074
    c1, c2, c3, c4 = 0.115, 0.362, 0.608, 0.862
    r1, r2, r3, r4 = 0.905, 0.700, 0.495, 0.290

    Psi = box(ax, (c2, r1), W, H_, "Digital\ntransformation $\\Psi$", fc="#E8EEF7")
    th = box(ax, (c3, r1), W, H_, "Employer skill\nthreshold $\\theta$")
    U = box(ax, (c2, r2), W, H_, "Mismatched\nemployment $U$")
    x = box(ax, (c3, r2), W, H_, "Skill–threshold\ngap $x=H-\\theta$")
    h = box(ax, (c4, r2), W, H_, "Hiring rate $h$")
    Qb = box(ax, (c1, r3), W, H_, "Exam queue $Q$", fc="#FBF3E6")
    Sb = box(ax, (c2, r3), W, H_, "Open searchers $S$", fc="#FBF3E6")
    Hb = box(ax, (c3, r3), W, H_, "Employability\ncapital $H$")
    pe = box(ax, (c1, r4), W, H_, "Exam success\nrate $\\pi_e$")
    tg = box(ax, (c2, r4), W, H_, "Market tightness\n$V/S$")
    qb = box(ax, (c3, r4), W, H_, "Offer quality $q$")
    Ab = box(ax, (c4, r4), W, H_, "Aspiration $A$")

    link(ax, Psi, th, "+", NAVY)
    link(ax, U, th, "+", RED, rad=-0.18)
    link(ax, th, x, "−", RED)
    link(ax, Hb, x, "+", TEAL)
    link(ax, x, h, "+", NAVY)
    link(ax, h, U, "−", RED, rad=0.45)
    link(ax, h, Sb, "−", GREY, rad=0.18)
    link(ax, Sb, h, "+", GREY, rad=0.18)
    link(ax, Sb, Hb, "−", TEAL)
    link(ax, Sb, Qb, "+", ORANGE, rad=0.32)
    link(ax, Qb, Sb, "+", ORANGE, rad=0.32)
    link(ax, Qb, Hb, "−", ORANGE, rad=-0.34)
    link(ax, Qb, pe, "−", GREEN)
    link(ax, pe, Qb, "+", GREEN, rad=-0.50)
    link(ax, Sb, tg, "−", GREEN)
    link(ax, tg, qb, "+", GREEN)
    link(ax, qb, h, "+", GREEN, rad=0.14)
    link(ax, qb, Ab, "+", NAVY)
    link(ax, Ab, h, "−", NAVY)

    loop_marker(ax, (0.762, 0.832), "R3", RED)
    loop_marker(ax, (0.498, 0.600), "R1", TEAL)
    loop_marker(ax, (0.238, 0.610), "R2", ORANGE)
    loop_marker(ax, (0.492, 0.392), "R4", GREEN, r=0.043)
    loop_marker(ax, (0.648, 0.572), "B1", GREY)
    loop_marker(ax, (0.778, 0.428), "B2", NAVY)
    loop_marker(ax, (0.192, 0.392), "B3", GREEN, r=0.043)

    left = [("R1", "skill decay while searching", TEAL),
            ("R2", "queue–skill erosion", ORANGE),
            ("R3", "threshold escalation", RED),
            ("R4", "thin-market offer quality", GREEN)]
    right = [("B1", "matching", GREY),
             ("B2", "aspiration adjustment", NAVY),
             ("B3", "exam-queue congestion", GREEN)]
    ax.text(0.020, 0.190, "Reinforcing loops", fontsize=7.2, fontweight="bold",
            color="#222222")
    ax.text(0.520, 0.190, "Balancing loops", fontsize=7.2, fontweight="bold",
            color="#222222")
    for i, (k, txt, c) in enumerate(left):
        ax.text(0.020, 0.145 - i * 0.042, k, fontsize=7.0, color=c,
                fontweight="bold", va="center")
        ax.text(0.062, 0.145 - i * 0.042, txt, fontsize=6.9, color="#333333",
                va="center")
    for i, (k, txt, c) in enumerate(right):
        ax.text(0.520, 0.145 - i * 0.042, k, fontsize=7.0, color=c,
                fontweight="bold", va="center")
        ax.text(0.562, 0.145 - i * 0.042, txt, fontsize=6.9, color="#333333",
                va="center")
    ax.plot([0.015, 0.985], [0.222, 0.222], color="#CCCCCC", lw=0.7)
    save(fig, "fig1_cld.png")


# ------------------------------------------------------------------ Figure 2
def fig2_stockflow():
    fig, ax = plt.subplots(figsize=(7.3, 4.05))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    def stock(x, y, label, sub, w=0.112, hh=0.110, fc="#E8EEF7"):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - hh / 2), w, hh,
                                    boxstyle="square,pad=0.003", fc=fc,
                                    ec=NAVY, lw=1.2, zorder=3))
        ax.text(x, y + 0.018, label, ha="center", va="center", fontsize=10,
                fontweight="bold", color="#12203F", zorder=4)
        ax.text(x, y - 0.030, sub, ha="center", va="center", fontsize=6.0,
                color="#444444", zorder=4)
        return (x, y, w, hh)

    def cloud(x, y, s=0.021):
        for dx, dy, r in [(-s, 0, s * 0.75), (0, s * 0.30, s * 0.90),
                          (s, 0, s * 0.75), (0, -s * 0.18, s * 0.82)]:
            ax.add_patch(plt.Circle((x + dx, y + dy), r, fc="white", ec=GREY,
                                    lw=0.8, zorder=1))

    def pipe(p0, p1, name, lab_side=1, lab_off=0.052, fs=6.4, color=NAVY,
             lab_dx=0.0):
        ax.annotate("", xy=p1, xytext=p0,
                    arrowprops=dict(arrowstyle="-|>", lw=2.6, color=color,
                                    mutation_scale=12, shrinkA=0, shrinkB=0),
                    zorder=2)
        vx, vy = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        n = np.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        px, py = -uy, ux
        a, b = 0.017, 0.024
        ax.add_patch(plt.Polygon([[vx - ux * a + px * b, vy - uy * a + py * b],
                                  [vx - ux * a - px * b, vy - uy * a - py * b],
                                  [vx + ux * a + px * b, vy + uy * a + py * b],
                                  [vx + ux * a - px * b, vy + uy * a - py * b]],
                                 closed=True, fc="white", ec=color, lw=1.0,
                                 zorder=4))
        ax.plot([vx + px * 0.034 * lab_side], [vy + py * 0.034 * lab_side],
                marker="o", ms=2.8, mfc="white", mec=color, mew=0.9, zorder=4)
        ax.text(vx + px * lab_off * lab_side + lab_dx,
                vy + py * lab_off * lab_side, name,
                ha="center", va="center", fontsize=fs, color="#333333", zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.6))

    yT, yM, yB = 0.795, 0.470, 0.135
    cloud(0.030, yT)
    S = stock(0.168, yT, "$S$", "open searchers", fc="#FBF3E6")
    Mst = stock(0.430, yT, "$M$", "matched")
    cloud(0.578, yT)
    Ust = stock(0.430, yM, "$U$", "mismatched")
    cloud(0.578, yM)
    Q = stock(0.168, yB, "$Q$", "exam queue", fc="#FBF3E6")

    pipe((0.052, yT), (0.111, yT), "$\Phi(t)$ cohort")
    pipe((0.225, yT), (0.373, yT), "$h\sigma$ good matches")
    pipe((0.487, yT), (0.556, yT), "$(\delta_M{+}\omega)M$", lab_off=0.066,
         lab_dx=0.030)
    pipe((0.487, yM), (0.556, yM), "$(\delta_U{+}\omega)U$", lab_side=-1,
         lab_off=0.066, lab_dx=0.030)
    pipe((0.216, 0.752), (0.378, 0.516), "$h(1{-}\sigma)$", lab_side=-1,
         lab_off=0.040)
    pipe((0.168, 0.738), (0.168, 0.192), "$f_{SQ}$", lab_side=1, lab_off=0.040)

    ax.annotate("", xy=(0.126, 0.740), xytext=(0.126, 0.190),
                arrowprops=dict(arrowstyle="-|>", lw=1.7, color=TEAL,
                                mutation_scale=10,
                                connectionstyle="arc3,rad=0.34"), zorder=2)
    ax.text(0.020, 0.465, "$f_{QS}$\ndiscouraged\nreturn", fontsize=6.3,
            color=TEAL, ha="center", va="center")
    ax.annotate("", xy=(0.408, 0.740), xytext=(0.226, 0.150),
                arrowprops=dict(arrowstyle="-|>", lw=1.7, color=ORANGE,
                                mutation_scale=10,
                                connectionstyle="arc3,rad=-0.28"), zorder=2)
    ax.text(0.395, 0.215, "$f_{QM}=\mathrm{smin}(\Xi,Q)$\nsuccessful exam takers",
            fontsize=6.3, color=ORANGE, ha="center")

    ax.annotate("", xy=(0.190, 0.856), xytext=(0.412, 0.856),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color=GREY,
                                mutation_scale=9,
                                connectionstyle="arc3,rad=0.30"), zorder=2)
    ax.text(0.301, 0.962, "$\delta_M M$ separations", fontsize=6.3, color=GREY,
            ha="center")
    ax.annotate("", xy=(0.148, 0.740), xytext=(0.374, 0.440),
                arrowprops=dict(arrowstyle="-|>", lw=1.3, color=GREY,
                                mutation_scale=9,
                                connectionstyle="arc3,rad=-0.34"), zorder=2)
    ax.text(0.238, 0.395, "$\delta_U U$ churn", fontsize=6.3, color=GREY,
            ha="center")

    ax.add_patch(FancyBboxPatch((0.645, 0.775), 0.345, 0.200,
                                boxstyle="round,pad=0.006,rounding_size=0.02",
                                fc="#FDF6EC", ec=ORANGE, lw=1.0, zorder=3))
    ax.text(0.817, 0.945, "$H$ — employability capital of searchers",
            ha="center", fontsize=7.0, color="#7A3E12", zorder=4)
    ax.text(0.817, 0.862, r"$\dot H=\dfrac{\Phi(h_{new}-H)-f_{QS}(1-\chi)H}{S}$"
                          "\n"
                          r"$\qquad\;-\delta_H H+\tau(h_{max}-H)$",
            ha="center", va="center", fontsize=6.6, color="#222222", zorder=4)

    ax.add_patch(FancyBboxPatch((0.645, 0.585), 0.345, 0.160,
                                boxstyle="round,pad=0.006,rounding_size=0.02",
                                fc="#EDF5F5", ec=TEAL, lw=1.0, zorder=3))
    ax.text(0.817, 0.715, "$A$ — aspiration threshold", ha="center", fontsize=7.0,
            color="#1C5F63", zorder=4)
    ax.text(0.817, 0.645,
            r"$\dot A=\lambda\left[\zeta A_{anch}+(1-\zeta)qp_s-A\right]$",
            ha="center", fontsize=6.6, color="#222222", zorder=4)

    ax.add_patch(FancyBboxPatch((0.645, 0.075), 0.345, 0.460,
                                boxstyle="round,pad=0.006,rounding_size=0.02",
                                fc="#F5F5F5", ec="#AAAAAA", lw=0.8, zorder=3))
    ax.text(0.817, 0.498, "Rate equations", ha="center", fontsize=7.0,
            color="#333333", zorder=4, fontweight="bold")
    ax.text(0.817, 0.300,
            r"$h=\mathrm{smin}\!\left(\mu S^{\alpha}V^{1-\alpha}p_sp_a,\;"
            r"S/d_{min}\right)$" "\n\n"
            r"$p_s=\Lambda(\beta_s x),\quad p_a=\Lambda(\beta_a(q-A))$" "\n\n"
            r"$\sigma=\Lambda(\sigma_0+\beta_{\sigma}x)$" "\n\n"
            r"$f_{SQ}=\nu S\,\Lambda\!\left(\beta_c\dfrac{W_Q-W_S}{W_Q+W_S}\right)$"
            "\n\n"
            r"$f_{QS}=\nu_r Q\left[1-\Lambda(\cdot)\right]$",
            ha="center", va="center", fontsize=6.5, color="#222222", zorder=4)
    save(fig, "fig2_stockflow.png")


# ------------------------------------------------------------------ Figure 3
def fig3_baseline():
    ts, ys = M.rk4(Y0, P, 0.0, 25.0, 1 / 24)
    s = M.series(ts, ys, P)
    yrs = 2015 + ts
    att = D["moving_attractor"]
    ay = [e["year"] for e in att]; an = [e["NER"] for e in att]

    fig, axes = plt.subplots(2, 2, figsize=(7.3, 4.9))
    a = axes[0, 0]
    a.plot(yrs, s["NER"], color=NAVY, label="Realised $\\mathrm{NER}(t)$")
    a.plot(ay, an, color=RED, ls="--", label="Moving attractor $\\mathrm{NER}^{*}(t)$")
    a.fill_between(ay, an, np.interp(ay, yrs, s["NER"]), color=RED, alpha=0.10)
    for x, y, lab in [(2015, 0.115, None), (2025, 0.180, None)]:
        a.plot([x], [y], "o", ms=4.5, mfc="white", mec=NAVY, mew=1.1, zorder=5)
    a.plot([], [], "o", ms=4.5, mfc="white", mec=NAVY, mew=1.1,
           label="Observed benchmark")
    a.set_ylabel("Youth non-employment rate")
    a.set_title("(a) Realised state versus its moving attractor", loc="left")
    a.legend(frameon=False, loc="upper left")
    a.axvline(2025, color=GREY, lw=0.6, ls=":")

    a = axes[0, 1]
    a.plot(yrs, s["SEflow"], color=ORANGE, label="Slow-employment share of entrants")
    a.plot(yrs, s["MM"], color=TEAL, label="Vertical mismatch share")
    a.plot([2025], [0.191], "o", ms=4.5, mfc="white", mec=ORANGE, mew=1.1, zorder=5)
    a.plot([2025], [0.240], "o", ms=4.5, mfc="white", mec=TEAL, mew=1.1, zorder=5)
    a.set_title("(b) Delayed entry and mismatch", loc="left")
    a.legend(frameon=False, loc="upper left")
    a.axvline(2025, color=GREY, lw=0.6, ls=":")

    a = axes[1, 0]
    a.plot(yrs, s["THETA"], color=RED, label="Employer skill threshold $\\theta$")
    a.plot(yrs, ys[:, 4], color=TEAL, label="Employability capital $H$")
    a.plot(yrs, ys[:, 5], color=NAVY, ls="-.", label="Aspiration $A$")
    a.fill_between(yrs, ys[:, 4], s["THETA"], where=s["THETA"] > ys[:, 4],
                   color=RED, alpha=0.10)
    a.set_ylabel("Index")
    a.set_xlabel("Year")
    a.set_title("(c) The skill–threshold gap closes and reverses", loc="left")
    a.legend(frameon=False, loc="lower left")
    cross = yrs[np.argmax(s["GAP"] < 0)]
    a.axvline(cross, color=GREY, lw=0.6, ls=":")
    a.annotate("$x=0$ in %d" % round(cross), (cross, 0.70), fontsize=6.8,
               color=GREY, ha="right")

    a = axes[1, 1]
    a.plot(yrs, s["RATIO"], color=ORANGE, label="Queue-to-seat ratio (left)")
    a.plot([2015, 2025], [63, 96], "o", ms=4.5, mfc="white", mec=ORANGE, mew=1.1,
           ls="none", zorder=5, label="Observed exam competition ratio")
    a.set_yscale("log"); a.set_ylabel("Applicants per post (log)")
    a.set_xlabel("Year")
    a2 = a.twinx()
    a2.plot(yrs, s["TIGHT"], color=GREEN, ls="--")
    a2.set_ylabel("Vacancy-to-seeker ratio", color=GREEN)
    a2.tick_params(axis="y", colors=GREEN); a2.spines["top"].set_visible(False)
    a.set_title("(d) Queue congestion rises while the market stays tight", loc="left")
    a.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    save(fig, "fig3_baseline.png")


# ------------------------------------------------------------------ Figure 4
def fig4_structure():
    fig, axes = plt.subplots(1, 3, figsize=(7.3, 2.55))

    a = axes[0]
    for pname, c, lab in [("kappa", RED, "$\\kappa$ threshold sensitivity"),
                          ("Pi", NAVY, "$\\Pi$ value of a public post")]:
        b = D["bifurcation"][pname]
        g = np.array(b["grid"]); f = np.array(b["ner_fwd"]); r = np.array(b["ner_bwd"])
        gn = (g - g.min()) / (g.max() - g.min())
        a.plot(gn, f, color=c, label=lab)
        a.plot(gn, r, color=c, ls=":", lw=1.0)
        a.plot([(b["base_value"] - g.min()) / (g.max() - g.min())],
               [np.interp(b["base_value"], g, f)], "o", ms=4.5, mfc="white",
               mec=c, mew=1.1, zorder=5)
    a.set_xlabel("Control parameter (normalised range)")
    a.set_ylabel("Equilibrium $\\mathrm{NER}^{*}$")
    a.set_title("(a) Continuation: no fold", loc="left")
    a.legend(frameon=False, loc="upper left")

    a = axes[1]
    sh = D["shock"]
    t = 2015 + np.array(sh["t"]); dev = np.array(sh["dev"])
    a.plot(t, dev, color=NAVY)
    a.axhline(0, color=GREY, lw=0.6)
    a.axvspan(sh["start"], sh["start"] + sh["shock_years"], color=ORANGE, alpha=0.16)
    a.axhline(sh["peak_excess_NER"] / 2, color=RED, lw=0.7, ls="--")
    a.annotate("half-life\n%.1f yr" % sh["half_life_years"],
               (sh["start"] + sh["shock_years"] + sh["half_life_years"],
                sh["peak_excess_NER"] / 2), fontsize=6.8, color=RED,
               ha="left", va="bottom")
    a.set_xlabel("Year"); a.set_ylabel("Excess NER over baseline")
    a.set_title("(b) A three-year demand shock decays", loc="left")
    a.set_xlim(2020, 2055)

    a = axes[2]
    ev = np.array(D["moving_attractor"][-1]["eig_real"])
    tau = -1.0 / ev
    a.barh(range(len(tau)), tau, color=[RED if abs(x - tau.max()) < 1e-9 else NAVY
                                        for x in tau], height=0.6)
    a.set_yticks(range(len(tau)))
    a.set_yticklabels(["$\\lambda_%d$" % (i + 1) for i in range(len(tau))])
    a.set_xlabel("Relaxation time $-1/\\mathrm{Re}\\,\\lambda_i$ (years)")
    a.set_title("(c) Spectrum of adjustment times", loc="left")
    a.invert_yaxis()
    for i, v in enumerate(tau):
        a.text(v + 0.12, i, "%.2f" % v, va="center", fontsize=6.6)
    a.set_xlim(0, tau.max() * 1.30)
    fig.tight_layout()
    save(fig, "fig4_structure.png")


# ------------------------------------------------------------------ Figure 5
def fig5_sensitivity():
    fig = plt.figure(figsize=(7.3, 4.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.35, 1.0], hspace=0.55, wspace=0.30)

    a = fig.add_subplot(gs[0, :])
    rows = D["sobol"]["NER"]["rows"]
    lab = [r["label"] for r in rows]
    y = np.arange(len(rows))
    s1 = [r["S1"] for r in rows]; stt = [r["ST"] for r in rows]
    e1 = np.array([[r["S1"] - r["S1_lo"] for r in rows],
                   [r["S1_hi"] - r["S1"] for r in rows]])
    et = np.array([[r["ST"] - r["ST_lo"] for r in rows],
                   [r["ST_hi"] - r["ST"] for r in rows]])
    a.barh(y - 0.19, stt, height=0.36, color=NAVY, label="Total-order $S_{Ti}$",
           xerr=et, error_kw=dict(lw=0.7, ecolor="#444444", capsize=1.6))
    a.barh(y + 0.19, s1, height=0.36, color=TEAL, label="First-order $S_i$",
           xerr=e1, error_kw=dict(lw=0.7, ecolor="#444444", capsize=1.6))
    a.set_yticks(y); a.set_yticklabels(lab, fontsize=7.0)
    a.invert_yaxis(); a.set_xlabel("Share of output variance")
    a.set_title("(a) Sobol decomposition of the 2040 non-employment rate "
                "(bootstrap 95% CI)", loc="left")
    a.legend(frameon=False, loc="lower right")

    a = fig.add_subplot(gs[1, 0])
    df = __import__("pandas").read_csv(os.path.join(HERE, "..", "data",
                                                    "policy_draws.csv"))
    mc = D["montecarlo"]["NER"]
    xs = np.linspace(0.05, 0.85, 400)
    from scipy.stats import gaussian_kde
    base = df[df.policy == "Baseline"]["NER_T"].values
    a.hist(base, bins=32, density=True, color="#D9E2F0", edgecolor="white", lw=0.4)
    a.plot(xs, gaussian_kde(base)(xs), color=NAVY)
    a.axvline(mc["q"][0], color=GREY, ls=":"); a.axvline(mc["q"][-1], color=GREY, ls=":")
    a.axvline(0.36, color=RED, ls="--", lw=1.0)
    a.annotate("trap\nthreshold", (0.365, a.get_ylim()[1] * 0.72), fontsize=6.6,
               color=RED)
    a.set_xlabel("$\\mathrm{NER}$ in 2040"); a.set_ylabel("Density")
    a.set_title("(b) Monte Carlo distribution", loc="left")

    a = fig.add_subplot(gs[1, 1])
    lg = D["logit"]["rows"][:7][::-1]
    y = np.arange(len(lg))
    coef = [r["coef"] for r in lg]
    err = [r["se"] * 1.96 for r in lg]
    a.barh(y, coef, color=[RED if c > 0 else TEAL for c in coef], height=0.6,
           xerr=err, error_kw=dict(lw=0.7, ecolor="#333333", capsize=1.6))
    a.set_yticks(y); a.set_yticklabels([r["param"] for r in lg], fontsize=7.0)
    a.axvline(0, color=GREY, lw=0.7)
    a.set_xlabel("Standardised logit coefficient")
    a.set_title("(c) Trap-risk meta-model (AUC = %.3f)" % D["logit"]["auc"],
                loc="left")
    save(fig, "fig5_sensitivity.png")


# ------------------------------------------------------------------ Figure 6
def fig6_policy():
    fig, axes = plt.subplots(1, 3, figsize=(7.3, 2.75))
    cols = {"P1 Skill upgrading": TEAL, "P2 Matching efficiency": GREEN,
            "P3 Expectation guidance": NAVY, "P4 Vacancy creation": ORANGE,
            "P5 Threshold moderation": RED}

    a = axes[0]
    for k, pts in D["frontier"].items():
        e = [p[0] for p in pts]; v = [p[1] for p in pts]
        a.plot(e, v, color=cols[k], label=k.split(" ", 1)[0] + " " + k.split(" ", 1)[1])
    a.set_xlabel("Policy effort (prior SD units)")
    a.set_ylabel("$\\mathrm{NER}$ in 2040")
    a.set_title("(a) Effort–response curves", loc="left")
    a.legend(frameon=False, fontsize=6.2, loc="upper right")

    a = axes[1]
    rows = D["policies"]["rows"]
    y = np.arange(len(rows))
    d = [r["dNER"] for r in rows]
    err = np.array([[r["dNER"] - r["dNER_lo"] for r in rows],
                    [r["dNER_hi"] - r["dNER"] for r in rows]])
    a.barh(y, d, color=[cols[r["policy"]] for r in rows], height=0.6,
           xerr=err, error_kw=dict(lw=0.7, ecolor="#333333", capsize=1.8))
    a.set_yticks(y); a.set_yticklabels([r["policy"].split(" ", 1)[0] for r in rows])
    a.invert_yaxis(); a.axvline(0, color=GREY, lw=0.7)
    a.set_xlabel("$\\Delta\\mathrm{NER}$ at one unit of effort")
    a.set_title("(b) Equal-effort comparison (95% band)", loc="left")

    a = axes[2]
    seq = D["sequencing"]["rows"]
    pairs = sorted({r["pair"] for r in seq})
    short = {p: (p.split(" / ")[0].split(" ", 1)[0], p.split(" / ")[1].split(" ", 1)[0])
             for p in pairs}
    lblmap = {"A-first": "front-load 1st instrument",
              "B-first": "front-load 2nd instrument",
              "simultaneous": "both throughout"}
    w = 0.26
    for j, order in enumerate(["A-first", "simultaneous", "B-first"]):
        vals = [next(r["NER_mean"] for r in seq if r["pair"] == p
                     and r["order"] == order) for p in pairs]
        a.bar(np.arange(len(pairs)) + (j - 1) * w, vals, width=w,
              color=[NAVY, GREY, ORANGE][j], label=lblmap[order])
    a.set_xticks(range(len(pairs)))
    a.set_xticklabels(["%s + %s" % short[p] for p in pairs], fontsize=6.8)
    for i, p in enumerate(pairs):
        for j, txt in enumerate(["%s first" % short[p][0], "together",
                                 "%s first" % short[p][1]]):
            a.text(i + (j - 1) * w, 0.185, txt, rotation=90, fontsize=5.6,
                   ha="center", va="bottom", color="white")
    a.set_ylabel("Mean $\\mathrm{NER}$, 2025–2040")
    a.set_ylim(0.18, 0.27)
    a.set_title("(c) Sequencing at equal cumulative effort", loc="left")
    a.legend(frameon=False, fontsize=6.2)
    fig.tight_layout()
    save(fig, "fig6_policy.png")


# ------------------------------------------------------------------ Figure 7
def fig7_archetypes():
    import analysis as A
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 2.6))
    cols = [NAVY, TEAL, ORANGE]
    a = axes[0]
    for (name, over), c in zip(A.ARCHETYPES.items(), cols):
        p = dict(P, **over)
        y0, ok = A.eq_at(p, M.GUESS_LOW, 0.0)
        ts, ys = M.rk4(y0 if ok else Y0, p, 0.0, 25.0, 1 / 24)
        s = M.series(ts, ys, p)
        a.plot(2015 + ts, s["NER"], color=c, label=name.split(" (")[0])
    a.set_xlabel("Year"); a.set_ylabel("Youth non-employment rate")
    a.set_title("(a) Prefecture-level city archetypes", loc="left")
    a.legend(frameon=False, fontsize=6.4, loc="upper left")

    a = axes[1]
    rows = D["archetypes"]
    y = np.arange(len(rows))
    a.barh(y - 0.19, [r["NER_2040"] for r in rows], height=0.36, color="#B9C4D8",
           label="No new policy")
    a.barh(y + 0.19, [r["NER_2040_best"] for r in rows], height=0.36, color=RED,
           label="Best single instrument")
    a.set_yticks(y)
    a.set_yticklabels([r["archetype"].split(".")[0] for r in rows])
    a.invert_yaxis(); a.set_xlabel("$\\mathrm{NER}$ in 2040")
    a.set_title("(b) Policy responsiveness by archetype", loc="left")
    a.legend(frameon=False, fontsize=6.6, loc="lower right")
    for i, r in enumerate(rows):
        a.text(r["NER_2040"] + 0.008, i - 0.19, "%.3f" % r["NER_2040"],
               va="center", fontsize=6.4)
        a.text(r["NER_2040_best"] + 0.008, i + 0.19, "%.3f" % r["NER_2040_best"],
               va="center", fontsize=6.4)
    a.set_xlim(0, 0.72)
    fig.tight_layout()
    save(fig, "fig7_archetypes.png")


if __name__ == "__main__":
    fig1_cld()
    fig2_stockflow()
    fig3_baseline()
    fig4_structure()
    fig5_sensitivity()
    fig6_policy()
    fig7_archetypes()
    print("all figures written to", FIGS)
