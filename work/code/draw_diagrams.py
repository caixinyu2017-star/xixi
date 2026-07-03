"""Static diagram figures: classification chart, strategy sketches, flowcharts."""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

FIGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figs')
os.makedirs(FIGS, exist_ok=True)

plt.rcParams.update({'font.family': 'serif', 'font.size': 9})

CAT_COLORS = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3']


def box(ax, x, y, w, h, text, fc='#EAEFF7', ec='#33507A', fs=8, style='round,pad=0.02', bold=False):
    p = FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=1.0,
                       mutation_scale=1.0)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs,
            fontweight='bold' if bold else 'normal', wrap=True)
    return p


def arrow(ax, x1, y1, x2, y2, style='-|>', lw=1.0, color='#33507A'):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=10,
                        lw=lw, color=color)
    ax.add_patch(a)


def classification_figure(path):
    cats = [
        ('Evolution-based', ['GA', 'DE', 'ES', 'CMA-ES', 'LSHADE']),
        ('Swarm-based', ['PSO', 'ACO', 'GWO', 'WOA', 'HHO', 'SSA', 'DBO', 'COA', 'SBOA', 'BKA']),
        ('Physics-based', ['SA', 'MVO', 'EO', 'RIME', 'SAO', 'KOA']),
        ('Mathematics-based', ['SCA', 'AOA', 'QIO', 'ETO']),
        ('Human-based', ['TLBO', 'PO', 'SNS', 'EDO']),
    ]
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.4)
    ax.axis('off')
    box(ax, 3.4, 4.6, 3.2, 0.6, 'Metaheuristic Algorithms', fc='#33507A', ec='#33507A', fs=10, bold=True)
    for t in ax.texts[-1:]:
        t.set_color('white')
    w = 1.8
    gap = (10 - 5 * w) / 6
    for i, (name, algs) in enumerate(cats):
        x = gap + i * (w + gap)
        box(ax, x, 3.3, w, 0.6, name, fc=CAT_COLORS[i], ec=CAT_COLORS[i], fs=8.2, bold=True)
        ax.texts[-1].set_color('white')
        arrow(ax, 5.0, 4.6, x + w / 2, 3.95)
        for j, a in enumerate(algs):
            y = 2.85 - j * 0.31
            ax.text(x + w / 2, y, a, ha='center', va='center', fontsize=7.4)
        # bracket line
        ax.plot([x + w / 2, x + w / 2], [3.3, 3.05], color=CAT_COLORS[i], lw=1)
    fig.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)


def flowchart(path, title_algo, init_label, strategy_lines, phase_lines, extra_lines):
    """Generic vertical flowchart."""
    fig, ax = plt.subplots(figsize=(6.4, 9.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 22)
    ax.axis('off')
    y = 21.0
    items = [('start', 'Start'), *strategy_lines]
    def diamond(ax, cx, cy, w, h, text, fs=7.5):
        xs = [cx - w / 2, cx, cx + w / 2, cx, cx - w / 2]
        ys = [cy, cy + h / 2, cy, cy - h / 2, cy]
        ax.plot(xs, ys, color='#33507A', lw=1.0)
        ax.fill(xs, ys, color='#FDF3E3')
        ax.text(cx, cy, text, ha='center', va='center', fontsize=fs)
    # This generic helper is bypassed; specific charts are drawn in dedicated funcs.
    plt.close(fig)


def flowchart_mssboa(path):
    fig, ax = plt.subplots(figsize=(7.2, 10.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 26)
    ax.axis('off')
    cx = 6
    def stадия(y, w, h, text, fc='#EAEFF7'):
        box(ax, cx - w / 2, y, w, h, text, fc=fc, fs=8)
        return y
    def diam(cy, w, h, text):
        xs = [cx - w / 2, cx, cx + w / 2, cx]
        ys = [cy, cy + h / 2, cy, cy - h / 2]
        ax.fill(xs + [xs[0]], ys + [ys[0]], color='#FDF3E3', ec='#B8860B', lw=1.0)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=7.6)
    box(ax, cx - 1.1, 24.9, 2.2, 0.8, 'Start', fc='#D5E8D4', fs=9)
    arrow(ax, cx, 24.9, cx, 24.35)
    box(ax, cx - 3.6, 23.5, 7.2, 0.8, 'Initialize population with good point set strategy (GPS)', fc='#FFE6CC', fs=8)
    arrow(ax, cx, 23.5, cx, 22.95)
    box(ax, cx - 3.2, 22.1, 6.4, 0.8, 'Evaluate fitness and determine $X_{best}$')
    arrow(ax, cx, 22.1, cx, 21.55)
    diam(20.85, 4.6, 1.4, 'FEs < MaxFEs ?')
    ax.text(cx + 0.25, 19.75, 'Yes', fontsize=8)
    arrow(ax, cx, 20.15, cx, 19.65)
    diam(18.85, 5.2, 1.5, 'Hunting stage by t')
    arrow(ax, cx - 2.6, 18.85, 1.9, 17.8)
    arrow(ax, cx, 18.1, cx, 17.8)
    arrow(ax, cx + 2.6, 18.85, 10.1, 17.8)
    box(ax, 0.3, 16.4, 3.2, 1.4, 'Stage 1:\nelite-guided golden\nsine search (EGS)', fc='#FFE6CC', fs=7.4)
    box(ax, 4.4, 16.4, 3.2, 1.4, 'Stage 2:\nBrownian motion\naround $X_{best}$', fs=7.4)
    box(ax, 8.5, 16.4, 3.2, 1.4, 'Stage 3:\nLevy flight\nattacking', fs=7.4)
    for xx in (1.9, 6.0, 10.1):
        arrow(ax, xx, 16.4, cx, 15.6)
    box(ax, cx - 3.4, 14.8, 6.8, 0.8, 'Greedy selection and update $X_{best}$')
    arrow(ax, cx, 14.8, cx, 14.25)
    diam(13.55, 4.4, 1.3, 'rand < 0.5 ?')
    arrow(ax, cx - 2.2, 13.55, 2.4, 12.5)
    arrow(ax, cx + 2.2, 13.55, 9.6, 12.5)
    box(ax, 0.8, 11.2, 3.2, 1.3, 'Escape:\ncamouflage move', fs=7.4)
    box(ax, 8.0, 11.2, 3.2, 1.3, 'Escape:\nfly or run away', fs=7.4)
    arrow(ax, 2.4, 11.2, cx, 10.4)
    arrow(ax, 9.6, 11.2, cx, 10.4)
    box(ax, cx - 3.4, 9.6, 6.8, 0.8, 'Greedy selection and update $X_{best}$')
    arrow(ax, cx, 9.6, cx, 9.05)
    box(ax, cx - 4.3, 7.7, 8.6, 1.3, 'Elite refinement mechanism (ERM): t-distribution perturbation or\nquadratic interpolation on $X_{best}$; greedy replacement of the worst', fc='#FFE6CC', fs=8)
    arrow(ax, cx, 7.7, cx, 7.15)
    box(ax, cx - 2.4, 6.3, 4.8, 0.8, 'FEs accounting and recording')
    # loop back
    arrow(ax, cx, 6.3, cx, 5.9)
    ax.plot([cx, 11.6, 11.6, cx + 2.3], [5.9, 5.9, 20.85, 20.85], color='#33507A', lw=1.0)
    arrow(ax, cx + 2.35, 20.85, cx + 2.3, 20.85)
    # exit
    ax.text(cx - 0.5, 19.95, '', fontsize=8)
    ax.plot([cx - 2.3, 0.6, 0.6], [20.85, 20.85, 3.9], color='#33507A', lw=1.0)
    ax.text(cx - 3.2, 21.0, 'No', fontsize=8)
    arrow(ax, 0.6, 3.9, cx - 1.3, 3.9)
    box(ax, cx - 1.3, 3.5, 4.4, 0.8, 'Output the best solution $X_{best}$', fc='#D5E8D4', fs=8)
    fig.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)


def flowchart_msbka(path):
    fig, ax = plt.subplots(figsize=(7.2, 10.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 25)
    ax.axis('off')
    cx = 6
    def diam(cy, w, h, text):
        xs = [cx - w / 2, cx, cx + w / 2, cx]
        ys = [cy, cy + h / 2, cy, cy - h / 2]
        ax.fill(xs + [xs[0]], ys + [ys[0]], color='#FDF3E3', ec='#B8860B', lw=1.0)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=7.6)
    box(ax, cx - 1.1, 23.9, 2.2, 0.8, 'Start', fc='#D5E8D4', fs=9)
    arrow(ax, cx, 23.9, cx, 23.35)
    box(ax, cx - 3.8, 22.5, 7.6, 0.8, 'Initialize population with tent chaotic mapping (TCM)', fc='#FFE6CC', fs=8)
    arrow(ax, cx, 22.5, cx, 21.95)
    box(ax, cx - 3.2, 21.1, 6.4, 0.8, 'Evaluate fitness and determine the leader $L$')
    arrow(ax, cx, 21.1, cx, 20.55)
    diam(19.85, 4.6, 1.4, 'FEs < MaxFEs ?')
    ax.text(cx + 0.25, 18.75, 'Yes', fontsize=8)
    arrow(ax, cx, 19.15, cx, 18.65)
    box(ax, cx - 4.0, 17.6, 8.0, 1.0, 'Attacking behavior: hovering / diving update with $n$', fs=8)
    arrow(ax, cx, 17.6, cx, 17.05)
    box(ax, cx - 3.4, 16.2, 6.8, 0.8, 'Greedy selection')
    arrow(ax, cx, 16.2, cx, 15.65)
    box(ax, cx - 4.6, 14.3, 9.2, 1.3, 'Migration behavior with fitness-distance balance (FDB)\ncompanion selection and Cauchy mutation', fc='#FFE6CC', fs=8)
    arrow(ax, cx, 14.3, cx, 13.75)
    box(ax, cx - 3.4, 12.9, 6.8, 0.8, 'Greedy selection and update the leader $L$')
    arrow(ax, cx, 12.9, cx, 12.35)
    box(ax, cx - 4.6, 10.9, 9.2, 1.4, 'Adaptive Cauchy-Gaussian hybrid mutation (CGM) on the\nleader; greedy replacement of the worst individual', fc='#FFE6CC', fs=8)
    arrow(ax, cx, 10.9, cx, 10.35)
    box(ax, cx - 2.4, 9.5, 4.8, 0.8, 'FEs accounting and recording')
    arrow(ax, cx, 9.5, cx, 9.1)
    ax.plot([cx, 11.6, 11.6, cx + 2.3], [9.1, 9.1, 19.85, 19.85], color='#33507A', lw=1.0)
    arrow(ax, cx + 2.35, 19.85, cx + 2.3, 19.85)
    ax.plot([cx - 2.3, 0.6, 0.6], [19.85, 19.85, 6.9], color='#33507A', lw=1.0)
    ax.text(cx - 3.2, 20.0, 'No', fontsize=8)
    arrow(ax, 0.6, 6.9, cx - 1.7, 6.9)
    box(ax, cx - 1.7, 6.5, 4.6, 0.8, 'Output the best solution', fc='#D5E8D4', fs=8)
    fig.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)


def sketch_egs(path):
    """Sketch of elite-guided golden sine search (paper A, Figure 2)."""
    rng = np.random.default_rng(3)
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))
    ax = axes[0]
    pts = rng.normal(0, 1.6, (24, 2)) + np.array([4.5, 4.5])
    ax.scatter(pts[:, 0], pts[:, 1], s=18, c='#9EB6D4', label='Ordinary individuals')
    el = np.array([[3.2, 5.6], [4.0, 5.9], [3.4, 6.3]])
    ax.scatter(el[:, 0], el[:, 1], s=55, c='#C44E52', marker='*', label='Elite pool')
    cm = el.mean(axis=0)
    ax.scatter(*cm, s=60, c='#DD8452', marker='P', label='Elite centroid')
    xi = np.array([6.8, 2.6])
    ax.scatter(*xi, s=40, c='#55A868', marker='s', label='$X_i$')
    for e in list(el) + [cm]:
        arrow(ax, xi[0], xi[1], (xi[0] + e[0]) / 2, (xi[1] + e[1]) / 2, lw=0.8, color='#888888')
    tgt = xi + 0.62 * (cm - xi)
    arrow(ax, xi[0], xi[1], tgt[0], tgt[1], lw=1.6, color='#C44E52')
    ax.set_title('(a) Elite guidance', fontsize=9)
    ax.set_xlim(0, 9); ax.set_ylim(0, 9)
    ax.set_xticks([]); ax.set_yticks([])
    ax.legend(fontsize=7, loc='lower left', frameon=False)
    ax2 = axes[1]
    t = np.linspace(0, 4 * np.pi, 300)
    r = np.exp(-0.12 * t)
    ax2.plot(4.5 + 3.5 * r * np.sin(t), 4.5 + 3.5 * r * np.cos(t), color='#4C72B0', lw=1.2)
    ax2.scatter([4.5], [4.5], s=70, c='#C44E52', marker='*', label='Elite target')
    ax2.set_title('(b) Golden sine contraction path', fontsize=9)
    ax2.set_xlim(0, 9); ax2.set_ylim(0, 9)
    ax2.set_xticks([]); ax2.set_yticks([])
    ax2.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)


def sketch_fdb(path):
    """Sketch of FDB companion selection + CGM mutation (paper B, Figure 2)."""
    rng = np.random.default_rng(7)
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))
    ax = axes[0]
    pts = rng.uniform(1, 8, (26, 2))
    fit = ((pts - np.array([3.4, 5.2])) ** 2).sum(axis=1)
    best = pts[fit.argmin()]
    dist = np.linalg.norm(pts - best, axis=1)
    score = (1 - (fit - fit.min()) / fit.ptp()) + dist / dist.max()
    sc = ax.scatter(pts[:, 0], pts[:, 1], c=score, cmap='viridis', s=26)
    ax.scatter(*best, s=90, c='#C44E52', marker='*', label='Leader')
    top = pts[np.argsort(score)[-3:]]
    ax.scatter(top[:, 0], top[:, 1], s=70, facecolors='none', edgecolors='#C44E52',
               lw=1.4, label='High FDB score')
    plt.colorbar(sc, ax=ax, shrink=0.85, label='FDB score')
    ax.set_title('(a) Fitness-distance balance selection', fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
    ax.legend(fontsize=7, frameon=False, loc='lower right')
    ax2 = axes[1]
    x = np.linspace(-5, 5, 400)
    cauchy = 1 / (np.pi * (1 + x ** 2))
    gauss = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
    ax2.plot(x, cauchy, label='Cauchy: early stage', color='#DD8452', lw=1.4)
    ax2.plot(x, gauss, label='Gaussian: later stage', color='#4C72B0', lw=1.4)
    ax2.fill_between(x, cauchy, alpha=0.15, color='#DD8452')
    ax2.fill_between(x, gauss, alpha=0.15, color='#4C72B0')
    ax2.set_title('(b) Adaptive Cauchy-Gaussian mutation', fontsize=9)
    ax2.set_xlabel('Perturbation size'); ax2.set_ylabel('Probability density')
    ax2.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)


def gps_vs_random(path):
    """GPS initialization vs random (paper A, part of strategy section)."""
    from algos_sboa import _good_point_set
    rng = np.random.default_rng(11)
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.6))
    Xr = rng.random((100, 2))
    Xg = _good_point_set(100, 2, np.zeros(2), np.ones(2))
    for ax, X, name in ((axes[0], Xr, '(a) Random initialization'),
                        (axes[1], Xg, '(b) Good point set initialization')):
        ax.scatter(X[:, 0], X[:, 1], s=14, c='#4C72B0')
        ax.set_title(name, fontsize=9)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xlabel('$x_1$'); ax.set_ylabel('$x_2$')
        ax.grid(lw=0.3, alpha=0.5)
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)


def tent_vs_random(path):
    """Tent chaotic initialization vs random (paper B)."""
    from algos_bka import _tent_init
    rng = np.random.default_rng(13)
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.6))
    Xr = rng.random((100, 2))
    Xt = _tent_init(100, 2, np.zeros(2), np.ones(2), np.random.default_rng(5))
    for ax, X, name in ((axes[0], Xr, '(a) Random initialization'),
                        (axes[1], Xt, '(b) Tent chaotic initialization')):
        ax.scatter(X[:, 0], X[:, 1], s=14, c='#55A868')
        ax.set_title(name, fontsize=9)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xlabel('$x_1$'); ax.set_ylabel('$x_2$')
        ax.grid(lw=0.3, alpha=0.5)
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight', dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    classification_figure(f'{FIGS}/classification.png')
    flowchart_mssboa(f'{FIGS}/flow_mssboa.png')
    flowchart_msbka(f'{FIGS}/flow_msbka.png')
    sketch_egs(f'{FIGS}/sketch_egs.png')
    sketch_fdb(f'{FIGS}/sketch_fdb.png')
    gps_vs_random(f'{FIGS}/gps_vs_random.png')
    tent_vs_random(f'{FIGS}/tent_vs_random.png')
    print('diagrams done')
