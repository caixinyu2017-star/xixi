# -*- coding: utf-8 -*-
"""学术概念图绘制工具箱（扁平矢量风格：白底、细等宽描边、克制配色、无阴影无渐变）。

用于示意图 / 机制图 / 路径图 / 技术路线图 / 框架图。所有标签为中文，字形由
Noto Sans CJK SC 提供，不存在生成式模型的乱码与伪字母问题。
"""
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from style import plt, C, save          # noqa
import matplotlib.patches as mp
from matplotlib.path import Path
import numpy as np

LW = 1.0
EDGE = C["ink"]


def canvas(w=8.0, h=5.0, xlim=(0, 100), ylim=(0, 100)):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("auto")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    return fig, ax


class Node(tuple):
    """行为等同于 (cx, cy) 的二元组，另外携带外接矩形，供 arrow() 自动求边界交点。"""
    def __new__(cls, cx, cy, x=None, y=None, w=None, h=None):
        o = super().__new__(cls, (cx, cy))
        o.cx, o.cy, o.x, o.y, o.w, o.h = cx, cy, x, y, w, h
        return o

    def edge(self, tx, ty, pad=0.6):
        """从中心朝 (tx,ty) 方向，返回矩形边界上的点。"""
        if self.w is None:
            return (self.cx, self.cy)
        dx, dy = tx - self.cx, ty - self.cy
        if dx == 0 and dy == 0:
            return (self.cx, self.cy)
        hw, hh = self.w / 2 + pad, self.h / 2 + pad
        sx = hw / abs(dx) if dx else float("inf")
        sy = hh / abs(dy) if dy else float("inf")
        t = min(sx, sy)
        return (self.cx + dx * t, self.cy + dy * t)


def box(ax, x, y, w, h, text, fc="white", ec=EDGE, tc=None, fs=8.5, r=1.6,
        lw=LW, bold=False, ls="-", align="center", pad=0.0, zorder=2):
    """圆角矩形 + 居中文本。(x,y) 为左下角。"""
    p = mp.FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                          boxstyle=f"round,pad={r}", linewidth=lw,
                          edgecolor=ec, facecolor=fc, linestyle=ls, zorder=zorder)
    ax.add_patch(p)
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
                color=tc or EDGE, fontweight="bold" if bold else "normal",
                linespacing=1.35, zorder=zorder + 1)
    return Node(x + w / 2, y + h / 2, x, y, w, h)


def band(ax, x, y, w, h, text, fc="#F4F6F9", ec=EDGE, fs=9, lw=LW, bold=True,
         label_side="left", tc=None, zorder=1):
    """宽横带（分层架构的层）。标题贴左侧竖排区。"""
    p = mp.FancyBboxPatch((x + 1.2, y + 1.2), w - 2.4, h - 2.4,
                          boxstyle="round,pad=1.2", linewidth=lw,
                          edgecolor=ec, facecolor=fc, zorder=zorder)
    ax.add_patch(p)
    if text:
        if label_side == "left":
            ax.text(x + 3.0, y + h / 2, text, ha="left", va="center", fontsize=fs,
                    fontweight="bold" if bold else "normal", color=tc or EDGE, zorder=zorder + 1)
        else:
            ax.text(x + w / 2, y + h - 4.0, text, ha="center", va="center", fontsize=fs,
                    fontweight="bold" if bold else "normal", color=tc or EDGE, zorder=zorder + 1)
    return p


def arrow(ax, p0, p1, color=EDGE, lw=1.1, ls="-", rad=0.0, head=7, text=None,
          fs=7.5, tpos=0.5, toff=(0, 2.2), shrink=2.0, zorder=3, tcolor=None, pad=0.6):
    if isinstance(p0, Node) and p0.w is not None:
        p0 = p0.edge(p1[0], p1[1], pad)
    if isinstance(p1, Node) and p1.w is not None:
        p1 = p1.edge(p0[0], p0[1], pad)
    a = mp.FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                           arrowstyle=f"-|>,head_width={head/24:.3f},head_length={head/16:.3f}",
                           mutation_scale=14, linewidth=lw, linestyle=ls,
                           color=color, shrinkA=shrink, shrinkB=shrink, zorder=zorder)
    ax.add_patch(a)
    if text:
        mx = p0[0] + (p1[0] - p0[0]) * tpos + toff[0]
        my = p0[1] + (p1[1] - p0[1]) * tpos + toff[1]
        ax.text(mx, my, text, ha="center", va="center", fontsize=fs,
                color=tcolor or color, zorder=zorder + 1,
                bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none"))
    return a


def dblarrow(ax, p0, p1, **kw):
    kw.setdefault("lw", 1.0)
    pad = kw.pop("pad", 0.6)
    if isinstance(p0, Node) and p0.w is not None:
        p0 = p0.edge(p1[0], p1[1], pad)
    if isinstance(p1, Node) and p1.w is not None:
        p1 = p1.edge(p0[0], p0[1], pad)
    a = mp.FancyArrowPatch(p0, p1, arrowstyle="<|-|>", mutation_scale=12,
                           linewidth=kw.get("lw", 1.0), color=kw.get("color", EDGE),
                           linestyle=kw.get("ls", "-"), shrinkA=2, shrinkB=2, zorder=3)
    ax.add_patch(a)
    return a


def inhibit(ax, p0, p1, color=C["brick"], lw=1.1, ls="-", pad=0.6):
    """抑制关系：平头线（⊣）。"""
    if isinstance(p0, Node) and p0.w is not None:
        p0 = p0.edge(p1[0], p1[1], pad)
    if isinstance(p1, Node) and p1.w is not None:
        p1 = p1.edge(p0[0], p0[1], pad)
    a = mp.FancyArrowPatch(p0, p1, arrowstyle="-[,widthB=0.35,lengthB=0.12",
                           mutation_scale=14, linewidth=lw, color=color,
                           linestyle=ls, shrinkA=2, shrinkB=2, zorder=3)
    ax.add_patch(a)


def diamond(ax, cx, cy, w, h, text, fc="white", ec=EDGE, fs=7.5, lw=LW):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(mp.Polygon(pts, closed=True, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=EDGE, zorder=3)
    return Node(cx, cy, cx - w / 2, cy - h / 2, w, h)


def circle(ax, cx, cy, r, text, fc="white", ec=EDGE, fs=8.5, lw=LW, bold=False, tc=None):
    ax.add_patch(mp.Circle((cx, cy), r, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2))
    if text:
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=tc or EDGE,
                fontweight="bold" if bold else "normal", linespacing=1.3, zorder=3)
    return Node(cx, cy, cx - r, cy - r, 2 * r, 2 * r)


def hexagon(ax, cx, cy, r, text, fc="white", ec=EDGE, fs=8.5, lw=LW, bold=True, tc=None):
    th = np.linspace(0, 2 * np.pi, 7)[:-1] + np.pi / 6
    pts = np.c_[cx + r * np.cos(th), cy + r * 0.92 * np.sin(th)]
    ax.add_patch(mp.Polygon(pts, closed=True, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=tc or EDGE,
            fontweight="bold" if bold else "normal", linespacing=1.3, zorder=3)
    return Node(cx, cy, cx - r, cy - r * 0.92, 2 * r, 1.84 * r)


def dashed_region(ax, x, y, w, h, text=None, ec=C["gray"], fs=8, tc=None, r=2.0,
                  tpos="top", fc="none", lw=0.9):
    p = mp.FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                          boxstyle=f"round,pad={r}", linewidth=lw, linestyle=(0, (4, 3)),
                          edgecolor=ec, facecolor=fc, zorder=0)
    ax.add_patch(p)
    if text:
        yy = y + h - 2.6 if tpos == "top" else y + 2.6
        ax.text(x + w / 2, yy, text, ha="center", va="center", fontsize=fs,
                color=tc or ec, zorder=1,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
    return p


def title(ax, text, x=50, y=97, fs=10):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, fontweight="bold", color=EDGE)


def wrap(s, n):
    """按字宽折行；连续的拉丁字母/数字视为不可拆分的整词，避免出现 "Qwen O / mni" 这类断词。"""
    import re
    toks = re.findall(r"[A-Za-z0-9][A-Za-z0-9\.\-\+/%]*|\s+|.", s)
    out, cur, w = [], "", 0
    for t in toks:
        if t.isspace():
            if cur:
                cur += " "; w += 0.5
            continue
        tw = len(t) * 0.55 if re.match(r"^[A-Za-z0-9]", t) else 1.0
        if w + tw > n and cur:
            out.append(cur.rstrip()); cur, w = "", 0
        cur += t; w += tw
    if cur:
        out.append(cur.rstrip())
    return "\n".join(out)


def loop_positions(cx, cy, rx, ry, n, start_deg=90, clockwise=True):
    """返回环形布局上 n 个节点中心坐标。"""
    sgn = -1 if clockwise else 1
    ang = [np.deg2rad(start_deg + sgn * 360 * i / n) for i in range(n)]
    return [(cx + rx * np.cos(a), cy + ry * np.sin(a)) for a in ang]
