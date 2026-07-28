# -*- coding: utf-8 -*-
"""Figures 1 and 2 in the conventional system-dynamics (Vensim) idiom.

Conventions followed: auxiliary and rate variables are plain text with no
enclosing box; stocks are rectangles; material flows are double-line pipes with
a bow-tie valve and cloud boundaries; information links are thin curved arrows;
causal polarities are marked at the arrowhead.  Every label carries a white halo
so that no link is ever occluded by text.
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrowPatch, Rectangle
from matplotlib.patheffects import withStroke

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.abspath(os.path.join(HERE, "..", "figs"))
os.makedirs(FIGS, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Liberation Serif", "DejaVu Serif"],
    "savefig.dpi": 600, "figure.dpi": 150, "mathtext.fontset": "dejavuserif",
})

BLUE = "#1B2FA8"        # Vensim information-link blue
INK = "#101010"         # stocks, flows, valves
CLOUD = "#7A7A7A"
HALO = [withStroke(linewidth=2.6, foreground="white")]


# ----------------------------------------------------------------- primitives
class Canvas:
    """Places labels first, measures them, then draws links between the boxes."""

    def __init__(self, w, h):
        self.fig, self.ax = plt.subplots(figsize=(w, h))
        self.ax.set_xlim(0, 1); self.ax.set_ylim(0, 1); self.ax.axis("off")
        self.boxes = {}

    def label(self, key, x, y, text, fs=7.6, stock=False, color=INK, weight="normal"):
        t = self.ax.text(x, y, text, ha="center", va="center", fontsize=fs,
                         color=color, zorder=6, fontweight=weight,
                         path_effects=None if stock else HALO)
        self.boxes[key] = dict(x=x, y=y, text=t, stock=stock)
        return key

    def measure(self, padx=0.012, pady=0.010):
        self.fig.canvas.draw()
        inv = self.ax.transData.inverted()
        for k, b in self.boxes.items():
            bb = b["text"].get_window_extent(self.fig.canvas.get_renderer())
            (x0, y0), (x1, y1) = inv.transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
            b["w"] = (x1 - x0) + 2 * padx
            b["h"] = (y1 - y0) + 2 * pady
            if b["stock"]:
                self.ax.add_patch(Rectangle((b["x"] - b["w"] / 2, b["y"] - b["h"] / 2),
                                            b["w"], b["h"], fc="white", ec=INK,
                                            lw=1.1, zorder=5))
                b["text"].set_zorder(6)

    def anchor(self, a, toward, pad=1.0):
        b = self.boxes[a]
        dx, dy = toward[0] - b["x"], toward[1] - b["y"]
        if dx == 0 and dy == 0:
            return b["x"], b["y"]
        sx = (b["w"] / 2 * pad) / abs(dx) if dx else np.inf
        sy = (b["h"] / 2 * pad) / abs(dy) if dy else np.inf
        s = min(sx, sy)
        return b["x"] + dx * s, b["y"] + dy * s

    def link(self, a, b, sign="", rad=0.0, color=BLUE, lw=0.85, fs=7.4,
             sfrac=0.80, soff=0.020):
        """Thin curved information link with the polarity marked at the head."""
        A, B = self.boxes[a], self.boxes[b]
        p0 = self.anchor(a, (B["x"], B["y"]))
        p1 = self.anchor(b, (A["x"], A["y"]))
        self.ax.add_patch(FancyArrowPatch(
            p0, p1, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
            mutation_scale=7.5, lw=lw, color=color, zorder=3,
            shrinkA=1.0, shrinkB=1.6))
        if not sign:
            return
        # quadratic Bezier of matplotlib's arc3 connector
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        cx = (p0[0] + p1[0]) / 2 + rad * dy
        cy = (p0[1] + p1[1]) / 2 - rad * dx
        t = sfrac
        bx = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * cx + t ** 2 * p1[0]
        by = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * cy + t ** 2 * p1[1]
        tx = 2 * (1 - t) * (cx - p0[0]) + 2 * t * (p1[0] - cx)
        ty = 2 * (1 - t) * (cy - p0[1]) + 2 * t * (p1[1] - cy)
        n = np.hypot(tx, ty) or 1.0
        self.ax.text(bx - ty / n * soff, by + tx / n * soff, sign, color=color,
                     fontsize=fs, ha="center", va="center", zorder=7,
                     fontweight="bold", path_effects=HALO)

    def loop(self, x, y, tag, color, r=0.030, cw=True):
        self.ax.add_patch(Arc((x, y), 2 * r, 2 * r, theta1=200, theta2=110,
                              color=color, lw=0.9, zorder=4))
        a0 = np.deg2rad(110 if cw else 200)
        d = 1 if cw else -1
        self.ax.annotate("", xy=(x + r * np.cos(a0 + d * 0.02),
                                 y + r * np.sin(a0 + d * 0.02)),
                         xytext=(x + r * np.cos(a0 + d * 0.30),
                                 y + r * np.sin(a0 + d * 0.30)),
                         arrowprops=dict(arrowstyle="-|>", color=color, lw=0.9,
                                         mutation_scale=6), zorder=4)
        self.ax.text(x, y, tag, ha="center", va="center", fontsize=6.8,
                     color=color, fontweight="bold", zorder=7,
                     path_effects=HALO)

    def save(self, name):
        p = os.path.join(FIGS, name)
        self.fig.savefig(p, bbox_inches="tight", facecolor="white")
        plt.close(self.fig)
        print("  wrote", name)


# ------------------------------------------------------------------- Figure 1
R_COL, B_COL = "#B03A2E", "#1F6F4A"


def fig1():
    c = Canvas(7.3, 5.0)
    c.label("psi", 0.15, 0.955, "Digital\ntransformation $\\Psi$")
    c.label("th", 0.57, 0.955, "Employer skill\nthreshold $\\theta$")
    c.label("U", 0.865, 0.855, "Mismatched\nemployment $U$", stock=True)
    c.label("x", 0.600, 0.800, "Skill–threshold\ngap $x$")
    c.label("h", 0.865, 0.645, "Hiring rate $h$")
    c.label("H", 0.600, 0.640, "Employability\ncapital $H$", stock=True)
    c.label("S", 0.355, 0.540, "Open\nsearchers $S$", stock=True)
    c.label("Q", 0.090, 0.640, "Exam\nqueue $Q$", stock=True)
    c.label("pe", 0.090, 0.430, "Exam success\nrate $\\pi_e$")
    c.label("V", 0.355, 0.360, "Market\ntightness $V/S$")
    c.label("q", 0.640, 0.345, "Offer quality $q$")
    c.label("A", 0.880, 0.450, "Aspiration $A$", stock=True)
    c.measure()

    c.link("psi", "th", "+")
    c.link("U", "th", "+", rad=0.14)
    c.link("th", "x", "−")
    c.link("H", "x", "+")
    c.link("x", "h", "+", rad=0.10)
    c.link("h", "U", "−", rad=0.14)
    c.link("h", "S", "−", rad=0.15)
    c.link("S", "h", "+", rad=0.15)
    c.link("S", "H", "−", rad=-0.24, sfrac=0.55, soff=0.024)
    c.link("S", "Q", "+", rad=0.20, sfrac=0.88, soff=0.024)
    c.link("Q", "S", "+", rad=0.20, sfrac=0.22, soff=0.024)
    c.link("Q", "H", "−", rad=-0.32, sfrac=0.42, soff=0.024)
    c.link("Q", "pe", "−")
    c.link("pe", "Q", "+", rad=-0.55, sfrac=0.46, soff=0.036)
    c.link("S", "V", "−")
    c.link("V", "q", "+")
    c.link("q", "h", "+", rad=0.18)
    c.link("q", "A", "+")
    c.link("A", "h", "−")

    c.loop(0.740, 0.845, "R3", R_COL)
    c.loop(0.745, 0.760, "R1", R_COL)
    c.loop(0.250, 0.760, "R2", R_COL)
    c.loop(0.520, 0.470, "R4", R_COL)
    c.loop(0.712, 0.548, "B1", B_COL, cw=False)
    c.loop(0.782, 0.352, "B2", B_COL, cw=False)
    c.loop(0.014, 0.498, "B3", B_COL, cw=False)

    ax = c.ax
    ax.plot([0.01, 0.99], [0.215, 0.215], color="#BBBBBB", lw=0.7)
    ax.text(0.015, 0.172, "Reinforcing loops", fontsize=7.4, fontweight="bold",
            color=R_COL)
    ax.text(0.545, 0.172, "Balancing loops", fontsize=7.4, fontweight="bold",
            color=B_COL)
    left = [("R1", "skill decay while searching"),
            ("R2", "queue–skill erosion"),
            ("R3", "threshold escalation"),
            ("R4", "thin-market offer quality")]
    right = [("B1", "matching"),
             ("B2", "aspiration adjustment"),
             ("B3", "exam-queue congestion")]
    for i, (k, t) in enumerate(left):
        ax.text(0.020, 0.128 - i * 0.036, k, fontsize=7.0, color=R_COL,
                fontweight="bold", va="center")
        ax.text(0.062, 0.128 - i * 0.036, t, fontsize=6.9, color="#333333",
                va="center")
    for i, (k, t) in enumerate(right):
        ax.text(0.550, 0.128 - i * 0.036, k, fontsize=7.0, color=B_COL,
                fontweight="bold", va="center")
        ax.text(0.592, 0.128 - i * 0.036, t, fontsize=6.9, color="#333333",
                va="center")
    c.save("fig1_cld.png")


# ------------------------------------------------------------------- Figure 2
def cloud(ax, x, y, s=0.019):
    for dx, dy, r in [(-s, -0.10 * s, 0.78 * s), (-0.35 * s, 0.44 * s, 0.72 * s),
                      (0.35 * s, 0.50 * s, 0.80 * s), (s, -0.05 * s, 0.74 * s),
                      (0.0, -0.32 * s, 0.72 * s)]:
        ax.add_patch(plt.Circle((x + dx, y + dy), r, fc="white", ec=CLOUD,
                                lw=0.8, zorder=2))


def pipe(ax, pts, label, side=1, off=0.040, fs=6.5, vfrac=0.5, dxy=(0.0, 0.0),
         ha="center"):
    """Double-line material flow with an hourglass valve at fraction vfrac."""
    pts = np.asarray(pts, float)
    seg = np.diff(pts, axis=0)
    L = np.hypot(seg[:, 0], seg[:, 1])
    cum = np.concatenate([[0.0], np.cumsum(L)])
    w = 0.0050

    def rail(sgn):
        out = []
        for i in range(len(pts)):
            if i == 0:
                d = seg[0] / L[0]
            elif i == len(pts) - 1:
                d = seg[-1] / L[-1]
            else:
                d = seg[i - 1] / L[i - 1] + seg[i] / L[i]
                d = d / (np.hypot(*d) or 1.0)
            out.append([pts[i][0] - sgn * d[1] * w, pts[i][1] + sgn * d[0] * w])
        return np.array(out)

    for sgn in (1, -1):
        r = rail(sgn)
        ax.plot(r[:, 0], r[:, 1], color=INK, lw=0.85, zorder=3,
                solid_joinstyle="miter")

    u = seg[-1] / L[-1]
    n = np.array([-u[1], u[0]])
    tip = pts[-1]
    base = tip - u * 0.016
    ax.add_patch(plt.Polygon([tip, base + n * 0.010, base - n * 0.010],
                             closed=True, fc=INK, ec=INK, lw=0.4, zorder=4))

    d = vfrac * cum[-1]
    i = min(max(int(np.searchsorted(cum, d, side="right") - 1), 0), len(seg) - 1)
    u = seg[i] / L[i]
    v = pts[i] + u * (d - cum[i])
    n = np.array([-u[1], u[0]])
    a, b = 0.0105, 0.0135
    for s_ in (1, -1):
        ax.add_patch(plt.Polygon([v + s_ * u * a + n * b, v + s_ * u * a - n * b, v],
                                 closed=True, fc="white", ec=INK, lw=0.9, zorder=5))
    ax.plot([v[0] + n[0] * 0.022], [v[1] + n[1] * 0.022], marker="o", ms=2.4,
            mfc="white", mec=INK, mew=0.8, zorder=5)
    ax.text(v[0] + n[0] * off * side + dxy[0], v[1] + n[1] * off * side + dxy[1],
            label, fontsize=fs, ha=ha, va="center", color="#1A1A1A", zorder=7,
            path_effects=HALO)
    return v


def fig2():
    c = Canvas(7.3, 4.6)
    ax = c.ax
    c.label("S", 0.320, 0.680, "$S$\nopen searchers", stock=True, fs=7.6)
    c.label("M", 0.620, 0.860, "$M$\nmatched", stock=True, fs=7.6)
    c.label("U", 0.620, 0.500, "$U$\nmismatched", stock=True, fs=7.6)
    c.label("Q", 0.085, 0.680, "$Q$\nexam queue", stock=True, fs=7.6)
    c.label("H", 0.240, 0.150, "$H$\nemployability\ncapital", stock=True, fs=7.2)
    c.label("A", 0.665, 0.150, "$A$\naspiration", stock=True, fs=7.2)
    c.label("hh", 0.420, 0.352, "hiring rate $h$", fs=7.0)
    c.label("x", 0.215, 0.262, "skill–threshold gap\n$x=H-\\theta$", fs=6.9)
    c.label("th", 0.530, 0.262, "employer\nthreshold $\\theta$", fs=6.9)
    c.label("psi", 0.815, 0.262, "digital\ntransformation $\\Psi$", fs=6.9)
    c.label("xi", 0.060, 0.430, "exam seats $\\Xi$", fs=6.9)
    c.measure()

    cloud(ax, 0.168, 0.912); cloud(ax, 0.085, 0.520)
    cloud(ax, 0.905, 0.860); cloud(ax, 0.905, 0.500)
    cloud(ax, 0.075, 0.150); cloud(ax, 0.500, 0.150)

    pipe(ax, [(0.183, 0.896), (0.278, 0.730)], "$\\Phi(t)$ cohort", side=-1,
         off=0.054)
    v_hs = pipe(ax, [(0.376, 0.706), (0.556, 0.826)], "$h\\sigma$", side=1, off=0.030)
    v_hu = pipe(ax, [(0.376, 0.654), (0.556, 0.534)], "$h(1-\\sigma)$", side=1,
                off=0.036, vfrac=0.30)
    pipe(ax, [(0.688, 0.860), (0.884, 0.860)], "$\\omega M$", side=1, off=0.032)
    pipe(ax, [(0.688, 0.500), (0.884, 0.500)], "$\\omega U$", side=-1, off=0.032)
    pipe(ax, [(0.580, 0.902), (0.455, 0.960), (0.338, 0.734)], "$\\delta_M M$",
         side=1, off=0.034, vfrac=0.40)
    pipe(ax, [(0.572, 0.468), (0.470, 0.430), (0.344, 0.630)], "$\\delta_U U$",
         side=1, off=0.034, vfrac=0.40)
    pipe(ax, [(0.266, 0.706), (0.145, 0.706)], "$f_{SQ}$", side=1, off=0.030)
    pipe(ax, [(0.145, 0.654), (0.266, 0.654)], "$f_{QS}$", side=-1, off=0.030)
    pipe(ax, [(0.070, 0.634), (0.070, 0.542)], "$\\omega Q$", side=-1, off=0.030,
         vfrac=0.45)
    v_qm = pipe(ax, [(0.112, 0.634), (0.112, 0.565), (0.730, 0.565),
                     (0.730, 0.782), (0.664, 0.814)], "$f_{QM}$", side=-1,
                off=0.030, vfrac=0.22)
    pipe(ax, [(0.097, 0.150), (0.170, 0.150)], "renewal, decay,\ntraining",
         side=-1, off=0.086, fs=6.2)
    pipe(ax, [(0.522, 0.150), (0.598, 0.150)], "adjustment\ntowards $A^{*}$",
         side=-1, off=0.086, fs=6.2)

    c.link("psi", "th", "")
    c.link("th", "x", "")
    c.link("H", "x", "")
    c.link("x", "hh", "", rad=-0.14)
    c.link("A", "hh", "", rad=0.20)
    for v, rad in [(v_hs, -0.20), (v_hu, -0.14)]:
        ax.add_patch(FancyArrowPatch(
            c.anchor("hh", tuple(v)), tuple(v + np.array([0.0, -0.024])),
            connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>", mutation_scale=7,
            lw=0.85, color=BLUE, zorder=6))
    ax.add_patch(FancyArrowPatch(
        c.anchor("xi", tuple(v_qm)), tuple(v_qm + np.array([-0.006, -0.020])),
        connectionstyle="arc3,rad=-0.24", arrowstyle="-|>", mutation_scale=7,
        lw=0.85, color=BLUE, zorder=6))

    ax.text(0.990, 0.020, "rectangles: stocks    double lines with valves: flows    "
                          "thin blue arrows: information links",
            fontsize=6.1, color="#777777", ha="right")
    c.save("fig2_stockflow.png")


if __name__ == "__main__":
    fig1()
    fig2()
