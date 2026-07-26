"""Figures produced for the revision.

fig_lens         New Figure 2: convex-lens imaging geometry behind Eq. (11),
                 plus the behaviour of the dynamic scaling factor k(t).
fig_param_nmin   Redrawn Figure 4 (Reviewer 3, comment 4: the "best" label was
                 illegible under the marker; it is now placed above the point
                 in a larger, boxed font).
fig_param_pm     Redrawn Figure 5, same treatment.
"""
import csv
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt                                   # noqa: E402
import numpy as np                                                # noqa: E402
from matplotlib.patches import Ellipse, FancyArrowPatch           # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, '..', 'figs')
RES = os.path.join(HERE, '..', 'results')
SRC = os.path.join(RES, 'from_manuscript')
os.makedirs(FIGS, exist_ok=True)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                     'axes.linewidth': 0.9, 'savefig.dpi': 300})


# --------------------------------------------------------------- Figure 2
def fig_lens():
    fig = plt.figure(figsize=(12.6, 4.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.5, 1.0, 1.0], wspace=0.42)

    # ---------------- (a) lens imaging geometry ----------------
    ax = fig.add_subplot(gs[0, 0])
    lb, ub = 0.0, 10.0
    o = (lb + ub) / 2.0
    x = 8.6
    h = 2.0
    k = 1.6
    xs = o + (o - x) / k
    hs = h / k

    ax.axhline(0, color='0.25', lw=1.2, zorder=1)
    ax.plot([lb, lb], [-0.25, 0.25], color='0.25', lw=1.2)
    ax.plot([ub, ub], [-0.25, 0.25], color='0.25', lw=1.2)
    ax.text(lb, 0.30, r'$lb_j$', ha='center', fontsize=11)
    ax.text(ub, 0.30, r'$ub_j$', ha='center', fontsize=11)

    # the lens sits on the optical axis at the midpoint of the interval
    ax.add_patch(Ellipse((o, 0), 0.62, 5.6, facecolor='#cfe3f5',
                         edgecolor='#2b6ca3', lw=1.4, alpha=0.85, zorder=2))
    ax.plot([o, o], [-3.0, 3.0], color='#2b6ca3', lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.text(o, 3.15, 'convex lens', ha='center', color='#2b6ca3', fontsize=10)
    ax.text(o, 0.30, r'$o_j$', ha='center', fontsize=11)

    # object (current individual) and image (refracted solution)
    ax.add_patch(FancyArrowPatch((x, 0), (x, h), arrowstyle='-|>',
                                 mutation_scale=14, color='#c0392b', lw=2.2, zorder=3))
    ax.text(x + 0.30, h * 0.55, r'$h$', color='#c0392b', fontsize=12)
    ax.text(x + 0.05, -0.55, r'$x_j$', ha='center', color='#c0392b', fontsize=11)
    ax.add_patch(FancyArrowPatch((xs, 0), (xs, -hs), arrowstyle='-|>',
                                 mutation_scale=14, color='#1e8449', lw=2.2, zorder=3))
    ax.text(xs - 0.62, -hs * 0.55, r'$h^{*}$', color='#1e8449', fontsize=12)
    ax.text(xs, 0.30, r'$x_j^{*}$', ha='center', color='#1e8449', fontsize=11)

    # the two similar triangles
    ax.plot([x, o, xs], [h, 0, -hs], color='#7f8c8d', lw=1.1, ls=':', zorder=2)
    ax.plot([x, x, o], [0, h, 0], color='#c0392b', lw=0.9, alpha=0.55, zorder=2)
    ax.plot([xs, xs, o], [0, -hs, 0], color='#1e8449', lw=0.9, alpha=0.55, zorder=2)

    ax.annotate('', xy=(o, 2.55), xytext=(x, 2.55),
                arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=1.0))
    ax.text((o + x) / 2, 2.72, r'$x_j-o_j$', ha='center', color='#c0392b', fontsize=10)
    ax.annotate('', xy=(xs, -2.0), xytext=(o, -2.0),
                arrowprops=dict(arrowstyle='<->', color='#1e8449', lw=1.0))
    ax.text((o + xs) / 2, -2.45, r'$o_j-x_j^{*}$', ha='center',
            color='#1e8449', fontsize=10)

    ax.text(0.5, -0.045,
            r'$\dfrac{h}{h^{*}}=\dfrac{x_j-o_j}{o_j-x_j^{*}}=k'
            r'\;\Longrightarrow\;x_j^{*}=\dfrac{lb_j+ub_j}{2}'
            r'+\dfrac{lb_j+ub_j}{2k}-\dfrac{x_j}{k}$',
            transform=ax.transAxes, fontsize=11.5, va='top', ha='center',
            bbox=dict(fc='white', ec='0.55', lw=0.9, boxstyle='round,pad=0.4'))
    ax.set_xlim(-1.0, 11.2)
    ax.set_ylim(-3.2, 3.7)
    ax.axis('off')
    ax.set_title('(a) convex-lens imaging behind Eq. (11)', fontsize=11, pad=10)

    # ---------------- (b) the k schedule ----------------
    ax = fig.add_subplot(gs[0, 1])
    tt = np.linspace(0, 1, 400)
    for nu, mu, lab, c in ((0.5, 10, r'$\nu=1/2,\ \mu=10$ (adopted)', '#c0392b'),
                           (1.0, 10, r'$\nu=1,\ \mu=10$', '#2b6ca3'),
                           (0.5, 5, r'$\nu=1/2,\ \mu=5$', '#1e8449'),
                           (0.5, 20, r'$\nu=1/2,\ \mu=20$', '#8e44ad')):
        ax.semilogy(tt, (1 + tt ** nu) ** mu, lw=2.0 if mu == 10 and nu == 0.5 else 1.3,
                    color=c, label=lab)
    ax.axhline(1, color='0.5', lw=0.8, ls='--')
    ax.text(0.97, 1.25, r'$k=1$: classical OBL', fontsize=8.5, color='0.35',
            ha='right', va='bottom')
    ax.set_xlabel(r'$t/T$')
    ax.set_ylabel(r'$k(t)$')
    # panels (b) and (c) draw the same four settings, so they share one legend
    # placed below them; a legend inside either panel covers its own curves
    handles, labels = ax.get_legend_handles_labels()
    ax.set_title(r'(b) scaling factor $k(t)=(1+(t/T)^{\nu})^{\mu}$',
                 fontsize=10.5, pad=10)
    ax.grid(alpha=0.25, which='both')

    # ---------------- (c) the induced refraction radius ----------------
    ax = fig.add_subplot(gs[0, 2])
    for nu, mu, lab, c in ((0.5, 10, r'$\nu=1/2,\ \mu=10$ (adopted)', '#c0392b'),
                           (1.0, 10, r'$\nu=1,\ \mu=10$', '#2b6ca3'),
                           (0.5, 5, r'$\nu=1/2,\ \mu=5$', '#1e8449'),
                           (0.5, 20, r'$\nu=1/2,\ \mu=20$', '#8e44ad')):
        ax.plot(tt, 1.0 / (1 + tt ** nu) ** mu,
                lw=2.0 if mu == 10 and nu == 0.5 else 1.3, color=c, label=lab)
    ax.set_xlabel(r'$t/T$')
    ax.set_ylabel(r'$|x^{*}_j-o_j|\,/\,|x_j-o_j|=1/k$')
    ax.set_title('(c) refraction radius about $o_j$', fontsize=10.5, pad=10)
    ax.grid(alpha=0.25)
    ax.set_ylim(-0.03, 1.03)
    # every curve decays towards zero, so the free space is the upper right;
    # both labels go there rather than on top of the slowest-decaying curve
    ax.annotate('wide reversal\n(exploration)', xy=(0.02, 0.95), xytext=(0.30, 0.86),
                fontsize=8.5, color='0.3', va='center',
                arrowprops=dict(arrowstyle='->', color='0.5', lw=0.9))
    ax.annotate('image collapses onto $o_j$\n(fine, local probing)',
                xy=(0.80, 0.03), xytext=(0.52, 0.52), fontsize=8.5, color='0.3',
                ha='center', va='center',
                arrowprops=dict(arrowstyle='->', color='0.5', lw=0.9,
                                connectionstyle='arc3,rad=-0.15'))

    fig.legend(handles, labels, loc='upper center', ncol=4, fontsize=9,
               bbox_to_anchor=(0.70, 0.045), frameon=True, framealpha=1.0,
               title='exponent pair of the lens schedule', title_fontsize=9)
    fig.subplots_adjust(bottom=0.20)
    fig.savefig(os.path.join(FIGS, 'fig02_lens_imaging.png'), bbox_inches='tight')
    plt.close(fig)
    print('wrote fig02_lens_imaging.png')


# ------------------------------------------------- Figures 4 and 5 redrawn
def _read_rank_table(path):
    with open(path, newline='') as fh:
        rows = list(csv.reader(fh))
    header = rows[0][1:]
    data = {r[0]: [float(v) for v in r[1:]] for r in rows[1:]}
    return header, data


def _free_spot(xs, series, ylim, box=(0.30, 0.20)):
    """Where to put a callout box so that it does not cover any curve.

    The candidate centres are scanned on a coarse grid in data coordinates and
    scored by the distance from the box to the nearest plotted point, measured
    after normalizing both axes to [0, 1] so that the two scales are
    comparable.  The best-scoring candidate is returned.  Placing the box by a
    fixed offset from the marked point, as before, put it on top of the curves
    whenever the marked point happened to sit in a crowded part of the plot.
    """
    y0, y1 = ylim
    span_x = max(xs) - min(xs) or 1.0
    pts = [((x - min(xs)) / span_x, (y - y0) / (y1 - y0))
           for s in series for x, y in zip(xs, s)]
    bw, bh = box
    best, best_score = None, -1.0
    for cx in np.linspace(0.12, 0.88, 25):
        for cy in np.linspace(0.12, 0.88, 25):
            # distance from the point to the box, zero when inside it
            d = min(max(abs(px - cx) - bw / 2, 0.0, abs(py - cy) - bh / 2)
                    for px, py in pts)
            if d > best_score:
                best, best_score = (cx, cy), d
    return (min(xs) + best[0] * span_x, y0 + best[1] * (y1 - y0))


def _rank_figure(path, out, xlabel, title, skip_first=True):
    header, data = _read_rank_table(path)
    cols = header[1:] if skip_first else header      # drop the SBOA reference
    dims = [d for d in data if d.lower() != 'average']
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    colors = ['#2b6ca3', '#c0392b', '#1e8449', '#8e44ad']
    marks = ['o', 's', '^', 'D']
    xs = np.arange(len(cols))
    for i, d in enumerate(dims):
        y = data[d][1:] if skip_first else data[d]
        ax.plot(xs, y, marker=marks[i % 4], ms=5.5, lw=1.5,
                color=colors[i % 4], label=d, alpha=0.9)
    avg = np.array(data['Average'][1:] if skip_first else data['Average'])
    ax.plot(xs, avg, marker='*', ms=13, lw=2.4, color='#e67e22', label='Average',
            zorder=5)

    ax.set_xticks(xs)
    ax.set_xticklabels(cols, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel('Friedman mean rank', fontsize=11)
    ax.set_title(title, fontsize=11.5, pad=26)
    ax.grid(alpha=0.28, ls=':')
    ymax = max(max(v[1:]) for v in data.values())
    ax.set_ylim(0.0, ymax * 1.12)
    # the legend sits above the axes, outside the data region entirely: inside
    # it covered the top of the curves at the ends of the grid
    ax.legend(fontsize=9, ncol=5, loc='lower center', frameon=True,
              bbox_to_anchor=(0.5, 1.005), framealpha=1.0, borderaxespad=0.0)

    # -- the "best" annotation, placed where the data leaves room --
    j = int(np.argmin(avg))
    ax.scatter([xs[j]], [avg[j]], s=210, facecolor='none', edgecolor='#e67e22',
               lw=2.0, zorder=6)
    series = [data[d][1:] if skip_first else data[d] for d in dims] + [list(avg)]
    ax.annotate(f'best: {cols[j]}\n(mean rank {avg[j]:.3f})',
                xy=(xs[j], avg[j]),
                xytext=_free_spot(xs, series, ax.get_ylim()),
                ha='center', va='center', fontsize=12.5, fontweight='bold',
                color='#b9531a', zorder=7,
                bbox=dict(fc='#fdf3e7', ec='#e67e22', lw=1.4,
                          boxstyle='round,pad=0.45'),
                arrowprops=dict(arrowstyle='-|>', color='#e67e22', lw=1.8,
                                shrinkA=10, shrinkB=10))
    fig.savefig(os.path.join(FIGS, out), bbox_inches='tight')
    plt.close(fig)
    print('wrote', out)


def fig_params():
    _rank_figure(os.path.join(SRC, 'T17_Table_2.csv'),
                 'fig04_nmin_ranking.png',
                 r'LOBL subpopulation size $N_{\min}$',
                 r'Friedman rankings of MSSBOA with different $N_{\min}$ ($\alpha=0.05$)')
    _rank_figure(os.path.join(SRC, 'T18_Table_3.csv'),
                 'fig05_pm_ranking.png',
                 r'ACGM mutation probability $p_m$',
                 r'Friedman rankings of MSSBOA with different $p_m$ ($\alpha=0.05$)')


if __name__ == '__main__':
    which = sys.argv[1:] or ['lens', 'params']
    if 'lens' in which:
        fig_lens()
    if 'params' in which:
        fig_params()
