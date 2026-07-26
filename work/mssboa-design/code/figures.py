"""Regenerate every result figure of the manuscript from the new runs.

    Figure 2   convex-lens imaging behind Eq. (11)              (draw_figs.py)
    Figure 4   Friedman ranks over the N_min grid
    Figure 5   Friedman ranks over the p_m grid
    Figure 6   Friedman ranks of the ablation
    Figure 7   per-function ranking heat maps, one panel per dimension
    Figure 8   convergence curves on representative functions
    Figure 9   Friedman ranks of the comparison across dimensions
    Figure 10  Nemenyi critical-difference diagrams
    Figure 11  Wilcoxon rank-sum summary
    Figure 12  colour-harmony palettes and the best-fitting template
    Figure 13  colour-harmony convergence and score distribution
    Figure 14  layout ranking heat map
    Figure 15  representative layouts
"""
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt                                  # noqa: E402
import numpy as np                                               # noqa: E402
from matplotlib.patches import Rectangle, Wedge                  # noqa: E402
from scipy import stats                                          # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, '..', 'figs')
RES = os.path.join(HERE, '..', 'results')
os.makedirs(FIGS, exist_ok=True)

import tables as TB                                              # noqa: E402
from bench import CEC2017_IDS                                    # noqa: E402
from run_all import MAIN_ORDER, COLOR_K, SCALE_ALGOS             # noqa: E402
from design_problems import (LAYOUT_PROBLEMS, hsv_to_rgb,        # noqa: E402
                             HARMONIC_TEMPLATES, best_template)
from algos_mssboa import FACTORIAL                               # noqa: E402

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                     'axes.linewidth': 0.8, 'savefig.dpi': 300})
PAL = ['#c0392b', '#2b6ca3', '#1e8449', '#8e44ad', '#e67e22', '#16a085',
       '#7f8c8d', '#d35400', '#2c3e50', '#c2185b', '#00838f']


def _save(fig, name):
    fig.savefig(os.path.join(FIGS, name), bbox_inches='tight')
    plt.close(fig)
    print('  wrote', name)


# ------------------------------------------------------- Figures 4, 5 and 6
def _rank_plot(rows, xlabel, title, out, best_label=None):
    header = rows[0][1:]
    dims = [r for r in rows[1:] if r[0].startswith('D')]
    avg = next((r for r in rows[1:] if r[0] == 'Average'), None)
    if avg is None:
        return
    xs = np.arange(len(header))
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for i, r in enumerate(dims):
        ax.plot(xs, [float(v) for v in r[1:]], marker='os^D'[i % 4], ms=5,
                lw=1.3, color=PAL[i % len(PAL)], label=r[0], alpha=0.9)
    a = np.array([float(v) for v in avg[1:]])
    ax.plot(xs, a, marker='*', ms=13, lw=2.3, color='#e67e22', label='Average',
            zorder=5)
    j = int(np.argmin(a))
    ax.scatter([xs[j]], [a[j]], s=200, facecolor='none', edgecolor='#e67e22',
               lw=1.9, zorder=6)
    ax.annotate(f'best: {best_label or header[j]}\n(mean rank {a[j]:.3f})',
                xy=(xs[j], a[j]), xytext=(xs[j], a[j] + max(2.2, 0.25 * a.max())),
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='#b9531a',
                bbox=dict(fc='#fdf3e7', ec='#e67e22', lw=1.3,
                          boxstyle='round,pad=0.4'),
                arrowprops=dict(arrowstyle='-|>', color='#e67e22', lw=1.7,
                                shrinkA=6, shrinkB=8))
    ax.set_xticks(xs)
    ax.set_xticklabels(header, fontsize=9)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel('Friedman mean rank', fontsize=10)
    ax.set_title(title, fontsize=10.5, pad=8)
    ax.grid(alpha=0.28, ls=':')
    ax.set_ylim(0, a.max() + max(3.2, 0.45 * a.max()))
    ax.legend(fontsize=8, ncol=len(dims) + 1, loc='upper center',
              bbox_to_anchor=(0.5, 1.005), framealpha=0.95)
    _save(fig, out)


def fig4_fig5():
    t2, t3 = TB.t2_nmin(), TB.t3_pm()
    if t2:
        _rank_plot(t2[0], r'LOBL subpopulation size $N_{\min}$',
                   r'Friedman rankings of MSSBOA with different $N_{\min}$ ($\alpha=0.05$)',
                   'fig04_nmin.png', t2[1]['best'])
    if t3:
        _rank_plot(t3[0], r'ACGM mutation probability $p_m$',
                   r'Friedman rankings of MSSBOA with different $p_m$ ($\alpha=0.05$)',
                   'fig05_pm.png', t3[1]['best'])


def fig6_ablation():
    t5 = TB.t5_ablation()
    if not t5:
        return
    rows, m = t5
    algos = m['algos']
    dims = [r for r in rows if r[0].startswith('CEC') or (r[1] or '').isdigit()]
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    xs = np.arange(len(algos))
    w = 0.8 / max(1, len(dims))
    for i, r in enumerate(dims):
        vals = [float(v) for v in r[2:2 + len(algos)]]
        ax.bar(xs + i * w - 0.4 + w / 2, vals, w, label=f'D = {r[1]}',
               color=PAL[i % len(PAL)], alpha=0.88, edgecolor='white', lw=0.6)
    ax.set_xticks(xs)
    ax.set_xticklabels(algos, rotation=12, fontsize=9)
    ax.set_ylabel('Friedman mean rank', fontsize=10)
    ax.set_title(r'Friedman rankings of MSSBOA with different strategies ($\alpha=0.05$)',
                 fontsize=10.5, pad=8)
    ax.grid(axis='y', alpha=0.28, ls=':')
    ax.legend(fontsize=8, ncol=len(dims))
    _save(fig, 'fig06_ablation.png')


# --------------------------------------------------------------- Figure 7
def fig7_heatmaps():
    d = TB.load('main')
    if d is None:
        return
    probs = [f'F{f}' for f in CEC2017_IDS]
    dims = [dm for dm in (10, 30, 50, 100) if TB.usable(d, MAIN_ORDER, probs, dm)]
    if not dims:
        return
    fig, axes = plt.subplots(1, len(dims), figsize=(4.6 * len(dims), 6.4),
                             squeeze=False)
    for ax, dm in zip(axes[0], dims):
        n = TB.usable(d, MAIN_ORDER, probs, dm)
        M = np.zeros((len(probs), len(MAIN_ORDER)))
        for i, p in enumerate(probs):
            M[i] = stats.rankdata([np.mean(d[(a, p, dm)][:n]) for a in MAIN_ORDER])
        im = ax.imshow(M, cmap='RdYlGn_r', aspect='auto', vmin=1,
                       vmax=len(MAIN_ORDER))
        ax.set_xticks(range(len(MAIN_ORDER)))
        ax.set_xticklabels(MAIN_ORDER, rotation=90, fontsize=7.5)
        ax.set_yticks(range(len(probs)))
        ax.set_yticklabels(probs, fontsize=6.5)
        ax.set_title(f'({chr(97 + dims.index(dm))}) {dm}D', fontsize=10)
        for i in range(len(probs)):
            for j in range(len(MAIN_ORDER)):
                ax.text(j, i, int(M[i, j]), ha='center', va='center',
                        fontsize=5.2, color='black')
    fig.colorbar(im, ax=axes[0].tolist(), fraction=0.02, pad=0.02,
                 label='rank (1 = best)')
    _save(fig, 'fig07_heatmaps.png')


# --------------------------------------------------------------- Figure 8
def fig8_convergence(dim=30, funcs=(1, 5, 10, 15, 21, 27)):
    path = os.path.join(RES, 'curves_main.npz')
    if not os.path.exists(path):
        return
    z = np.load(path)
    avail = [f for f in funcs if any(k.endswith(f'|F{f}|{dim}') for k in z.files)]
    if not avail:
        return
    ncol = 3
    nrow = int(np.ceil(len(avail) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.4 * ncol, 3.2 * nrow),
                             squeeze=False)
    for k, f in enumerate(avail):
        ax = axes[k // ncol][k % ncol]
        for i, a in enumerate(MAIN_ORDER):
            key = f'{a}|F{f}|{dim}'
            if key not in z.files:
                continue
            c = np.maximum(z[key] - 100 * f, 1e-12)
            ax.semilogy(np.linspace(0, 1, len(c)) * 1000 * dim, c,
                        lw=2.0 if a == 'MSSBOA' else 1.0,
                        color=PAL[i % len(PAL)], label=a,
                        alpha=1.0 if a == 'MSSBOA' else 0.75)
        ax.set_title(f'F{f} ({dim}D)', fontsize=10)
        ax.set_xlabel('function evaluations', fontsize=8.5)
        ax.set_ylabel('error', fontsize=8.5)
        ax.grid(alpha=0.25, which='both', ls=':')
    for k in range(len(avail), nrow * ncol):
        axes[k // ncol][k % ncol].axis('off')
    axes[0][0].legend(fontsize=7, ncol=2, loc='upper right')
    _save(fig, 'fig08_convergence.png')


# --------------------------------------------------------------- Figure 9
def fig9_friedman():
    t6 = TB.t6_friedman()
    if not t6:
        return
    rows, m = t6
    dims = m['dims']
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    xs = np.arange(len(MAIN_ORDER))
    w = 0.8 / len(dims)
    for i, dm in enumerate(dims):
        ax.bar(xs + i * w - 0.4 + w / 2, [m['rank'][dm][a] for a in MAIN_ORDER],
               w, label=f'{dm}D', color=PAL[i % len(PAL)], alpha=0.88,
               edgecolor='white', lw=0.5)
    ax.plot(xs, [m['avg'][a] for a in MAIN_ORDER], 'k*--', ms=10, lw=1.2,
            label='Average')
    ax.set_xticks(xs)
    ax.set_xticklabels(MAIN_ORDER, rotation=25, ha='right', fontsize=9)
    ax.set_ylabel('Friedman mean rank', fontsize=10)
    ax.set_title(r'Friedman rankings across dimensions ($\alpha=0.05$)',
                 fontsize=10.5, pad=8)
    ax.grid(axis='y', alpha=0.28, ls=':')
    ax.legend(fontsize=8, ncol=len(dims) + 1)
    _save(fig, 'fig09_friedman.png')


# -------------------------------------------------------------- Figure 10
def fig10_nemenyi():
    t6 = TB.t6_friedman()
    if not t6:
        return
    _, m = t6
    dims = m['dims']
    k, N = len(MAIN_ORDER), len(CEC2017_IDS)
    q_alpha = {2: 1.960, 3: 2.343, 4: 2.569, 5: 2.728, 6: 2.850, 7: 2.949,
               8: 3.031, 9: 3.102, 10: 3.164, 11: 3.219, 12: 3.268}.get(k, 3.219)
    cd = q_alpha * np.sqrt(k * (k + 1) / (6.0 * N))
    fig, axes = plt.subplots(len(dims), 1, figsize=(8.0, 2.3 * len(dims)),
                             squeeze=False)
    for ax, dm in zip(axes[:, 0], dims):
        r = np.array([m['rank'][dm][a] for a in MAIN_ORDER])
        order = np.argsort(r)
        ax.set_xlim(0.5, k + 0.5)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.plot([0.8, k + 0.2], [0.75, 0.75], 'k-', lw=1.1)
        for x in range(1, k + 1):
            ax.plot([x, x], [0.72, 0.78], 'k-', lw=0.9)
            ax.text(x, 0.83, str(x), ha='center', fontsize=7.5)
        for rank_i, i in enumerate(order):
            y = 0.60 - 0.045 * (rank_i % 6)
            ax.plot([r[i], r[i]], [0.72, y], color=PAL[i % len(PAL)], lw=1.0)
            side = -1 if rank_i < k / 2 else 1
            ax.plot([r[i], r[i] + side * 0.35], [y, y],
                    color=PAL[i % len(PAL)], lw=1.0)
            ax.text(r[i] + side * 0.4, y, MAIN_ORDER[i], fontsize=7.5,
                    ha='left' if side > 0 else 'right', va='center')
        # cliques of statistically indistinguishable algorithms
        y = 0.68
        used = []
        for a in range(k):
            b = a
            while b + 1 < k and r[order[b + 1]] - r[order[a]] < cd:
                b += 1
            if b > a and not any(a >= s and b <= e for s, e in used):
                ax.plot([r[order[a]], r[order[b]]], [y, y], 'k-', lw=2.4,
                        solid_capstyle='butt')
                used.append((a, b))
                y -= 0.035
        ax.text(0.8, 0.93, f'{dm}D   CD = {cd:.3f}', fontsize=9,
                fontweight='bold')
    _save(fig, 'fig10_nemenyi.png')


# -------------------------------------------------------------- Figure 11
def fig11_wilcoxon():
    t7 = TB.t7_wilcoxon()
    if not t7:
        return
    rows, m = t7
    comp = [r[0] for r in rows[1:]]
    tot = np.array([[int(x) for x in r[-1].split('/')] for r in rows[1:]])
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    ys = np.arange(len(comp))
    ax.barh(ys, tot[:, 0], color='#1e8449', label='MSSBOA better (+)')
    ax.barh(ys, tot[:, 1], left=tot[:, 0], color='#bdc3c7', label='no difference (=)')
    ax.barh(ys, tot[:, 2], left=tot[:, 0] + tot[:, 1], color='#c0392b',
            label='MSSBOA worse (−)')
    for i in range(len(comp)):
        ax.text(m['cases'] + 1, i, f'{tot[i,0]}/{tot[i,1]}/{tot[i,2]}',
                va='center', fontsize=8)
    ax.set_yticks(ys)
    ax.set_yticklabels(comp, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel(f'number of the {m["cases"]} algorithm-function cases',
                  fontsize=10)
    ax.set_xlim(0, m['cases'] * 1.16)
    ax.set_title(r'Wilcoxon rank-sum outcome of MSSBOA against each algorithm ($\alpha=0.05$)',
                 fontsize=10.5, pad=8)
    ax.legend(fontsize=8, loc='lower right')
    _save(fig, 'fig11_wilcoxon.png')


# --------------------------------------------------- Figures 12 and 13
def fig12_palettes(best_json='design_best.json'):
    import json
    path = os.path.join(RES, best_json)
    if not os.path.exists(path):
        return
    best = json.load(open(path))
    key7 = [k for k in best if k.startswith('color|') and k.endswith('|7')]
    if not key7:
        return
    algos = [k.split('|')[1] for k in key7]
    order = [a for a in MAIN_ORDER if a in algos]
    fig = plt.figure(figsize=(11.5, 4.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.5], wspace=0.22)

    # (a) hue wheel with the best-fitting template of the MSSBOA palette
    ax = fig.add_subplot(gs[0, 0])
    rec = best.get('color|MSSBOA|7') or best[key7[0]]
    pal = np.array(rec['palette'])
    tname, alpha = rec['template'], rec['alpha']
    for h in range(0, 360, 2):
        ax.add_patch(Wedge((0, 0), 1.0, h, h + 2, width=0.22,
                           facecolor=hsv_to_rgb(h, 0.85, 0.95), lw=0))
    for off, width in HARMONIC_TEMPLATES[tname]:
        c = (off + alpha) % 360
        ax.add_patch(Wedge((0, 0), 0.74, c - width / 2, c + width / 2,
                           width=0.74, facecolor='0.25', alpha=0.22, lw=0))
        ax.add_patch(Wedge((0, 0), 0.74, c - width / 2, c + width / 2,
                           width=0.74, facecolor='none', edgecolor='0.25',
                           lw=1.2, ls='--'))
    for h, s, v in pal:
        th = np.deg2rad(h % 360)
        ax.plot([0.86 * np.cos(th)], [0.86 * np.sin(th)], 'o', ms=11,
                color=hsv_to_rgb(h, s, v), mec='k', mew=0.8, zorder=5)
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'(a) MSSBOA palette on the hue wheel\n'
                 f'best-fitting template: {tname}-type, α = {alpha:.0f}°',
                 fontsize=10)

    # (b) the palettes of every algorithm
    ax = fig.add_subplot(gs[0, 1])
    for i, a in enumerate(order):
        rec = best[f'color|{a}|7']
        pal = np.array(rec['palette'])
        for j, (h, s, v) in enumerate(pal):
            ax.add_patch(Rectangle((j, len(order) - 1 - i), 1, 0.82,
                                   facecolor=hsv_to_rgb(h, s, v), lw=0.4,
                                   edgecolor='white'))
        ax.text(-0.25, len(order) - 1 - i + 0.41, a, ha='right', va='center',
                fontsize=8.5)
        ax.text(len(pal) + 0.2, len(order) - 1 - i + 0.41,
                f'{rec["score"] * 100:.2f}%', ha='left', va='center', fontsize=8.5)
    ax.set_xlim(-2.6, 9.4)
    ax.set_ylim(-0.2, len(order))
    ax.axis('off')
    ax.set_title('(b) optimized seven-colour palettes and harmony scores',
                 fontsize=10)
    _save(fig, 'fig12_palettes.png')


def fig13_color():
    d = TB.load('design_color')
    path = os.path.join(RES, 'curves_design_color.npz')
    if d is None:
        return
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.0))
    if os.path.exists(path):
        z = np.load(path)
        for i, a in enumerate(MAIN_ORDER):
            k = f'{a}|K7|0'
            if k in z.files:
                c = -z[k]
                axes[0].plot(np.linspace(0, 1, len(c)) * 20000, c * 100,
                             lw=2.0 if a == 'MSSBOA' else 1.0,
                             color=PAL[i % len(PAL)], label=a,
                             alpha=1.0 if a == 'MSSBOA' else 0.75)
        axes[0].set_xlabel('function evaluations')
        axes[0].set_ylabel('harmony score (%)')
        axes[0].legend(fontsize=7, ncol=2, loc='lower right')
        axes[0].grid(alpha=0.25, ls=':')
    axes[0].set_title('(a) convergence, K = 7', fontsize=10)
    n = TB.usable(d, MAIN_ORDER, ['K7'], 0)
    data = [np.array(d[(a, 'K7', 0)][:n]) * 100 for a in MAIN_ORDER]
    bp = axes[1].boxplot(data, labels=MAIN_ORDER, patch_artist=True, widths=0.6)
    for patch, c in zip(bp['boxes'], PAL):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
    axes[1].set_ylabel('harmony score (%)')
    axes[1].tick_params(axis='x', rotation=35, labelsize=8)
    axes[1].grid(axis='y', alpha=0.25, ls=':')
    axes[1].set_title(f'(b) distribution over {n} runs, K = 7', fontsize=10)
    _save(fig, 'fig13_color.png')


# -------------------------------------------------------------- Figure 14
def fig14_layout_heatmap():
    t10 = TB.t10_layout()
    if not t10:
        return
    rows, m = t10
    probs = [r[0] for r in rows[1:-1]]
    M = np.zeros((len(probs), len(MAIN_ORDER)))
    for i, r in enumerate(rows[1:-1]):
        vals = [float(v) for v in r[1:]]
        M[i] = stats.rankdata([-v for v in vals])
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    im = ax.imshow(M, cmap='RdYlGn_r', aspect='auto', vmin=1, vmax=len(MAIN_ORDER))
    ax.set_xticks(range(len(MAIN_ORDER)))
    ax.set_xticklabels(MAIN_ORDER, rotation=35, ha='right', fontsize=8.5)
    ax.set_yticks(range(len(probs)))
    ax.set_yticklabels(probs, fontsize=9)
    for i in range(len(probs)):
        for j in range(len(MAIN_ORDER)):
            ax.text(j, i, int(M[i, j]), ha='center', va='center', fontsize=7.5)
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, label='rank (1 = best)')
    ax.set_title('Ranking of the algorithms on the graphic-layout problems',
                 fontsize=10.5, pad=8)
    _save(fig, 'fig14_layout_heatmap.png')


# -------------------------------------------------------------- Figure 15
def fig15_layouts(codes=('DL01', 'DL04', 'DL06')):
    import json
    path = os.path.join(RES, 'design_best.json')
    if not os.path.exists(path):
        return
    best = json.load(open(path))
    pairs = [(a, c) for a in ('MSSBOA', 'SBOA') for c in codes]
    if not all(f'layout|{a}|{c}' in best for a, c in pairs):
        return
    fig, axes = plt.subplots(2, len(codes), figsize=(3.4 * len(codes), 6.8))
    for r, algo in enumerate(('MSSBOA', 'SBOA')):
        for c, code in enumerate(codes):
            ax = axes[r][c]
            rec = best[f'layout|{algo}|{code}']
            sizes = LAYOUT_PROBLEMS[code][1]
            xy = np.array(rec['x']).reshape(-1, 2)
            ax.add_patch(Rectangle((0, 0), 1, 1, fc='#fbfbfb', ec='0.4', lw=1.1))
            for i, (cx, cy) in enumerate(xy):
                w, h = sizes[i]
                ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h,
                                       fc=PAL[i % len(PAL)], alpha=0.62,
                                       ec='0.2', lw=0.9))
            ax.set_xlim(-0.06, 1.06)
            ax.set_ylim(-0.06, 1.06)
            ax.set_aspect('equal')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(f'{algo} — {code} ({LAYOUT_PROBLEMS[code][0]})\n'
                         f'score {rec["score"] * 100:.2f}', fontsize=9)
    _save(fig, 'fig15_layouts.png')


ALL = [fig4_fig5, fig6_ablation, fig7_heatmaps, fig8_convergence,
       fig9_friedman, fig10_nemenyi, fig11_wilcoxon, fig12_palettes,
       fig13_color, fig14_layout_heatmap, fig15_layouts]


if __name__ == '__main__':
    for fn in ALL:
        try:
            fn()
        except Exception as exc:
            print(f'  ! {fn.__name__}: {type(exc).__name__}: {exc}')
