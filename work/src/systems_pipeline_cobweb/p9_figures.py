# -*- coding: utf-8 -*-
"""Paper 9 figures. Every plotted value is read from p9_results.json, so the figures
and the text cannot disagree."""
import json
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'p9_results.json')))

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.6,
                     'axes.linewidth': 0.8, 'axes.edgecolor': '#3a3a3a'})
INK, MUT, GRID = '#111111', '#5a5a5a', '#d8d8d8'
BLUE, RED, GREEN, ORANGE, PURPLE = '#2c6fbb', '#c0392b', '#1e8449', '#d68910', '#6c3483'
TEAL, CRIM = '#00695c', '#c2185b'
DPI = 320
T0 = 10


def style(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, color=GRID, lw=0.5, alpha=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=7.6, length=3, color='#7a7a7a')


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ======================================================= Figure 1: the structure
def fig1():
    W_IN, H_IN = 7.3, 4.3
    XR, YR = 100.0, 59.0
    fig, ax = plt.subplots(figsize=(W_IN, H_IN))
    ax.set_xlim(0, XR); ax.set_ylim(4, YR); ax.axis('off')
    ux, uy = XR / W_IN, YR / H_IN
    FS = 7.3

    N = {
        'tech': (13, 50, 'Technology shock\nto entry-level\ndemand'),
        'mkt':  (39, 50, 'Entry-level market\nin the exposed field\nwage, job finding'),
        'sig':  (67, 50, 'Observed return\nto the field'),
        'bel':  (86, 37, 'Forecast of the\nreturn D years\nahead'),
        'ch':   (67, 24, 'Field choice of\nthis year’s entrants'),
        'pipe': (39, 24, 'Pipeline:\nD cohorts enrolled\nbut not graduated'),
        'stk':  (13, 33, 'Entry-tier stock\nof the field'),
    }
    face = {'tech': ('#fdecec', RED), 'mkt': ('#e6eefa', BLUE),
            'sig': ('#e6eefa', BLUE), 'bel': ('#fdf2e2', ORANGE),
            'ch': ('#f2ecf7', PURPLE), 'pipe': ('#e7f5ec', GREEN),
            'stk': ('#e7f5ec', TEAL)}

    def half(key):
        _, _, t = N[key]
        lines = t.split('\n')
        w_in = max(len(s) for s in lines) * FS * 0.545 / 72.0
        h_in = len(lines) * FS * 1.32 / 72.0
        return w_in * ux / 2 + 1.4, h_in * uy / 2 + 1.3

    def clip(key, dx, dy):
        x, y, _ = N[key]
        hw, hh = half(key)
        sx = abs(dx) / hw if dx else 0.0
        sy = abs(dy) / hh if dy else 0.0
        s = max(sx, sy, 1e-9)
        return x + dx / s, y + dy / s

    for key in N:
        x, y, t = N[key]
        fc, ec = face[key]
        ax.text(x, y, t, ha='center', va='center', fontsize=FS, color=INK, zorder=6,
                linespacing=1.3,
                bbox=dict(boxstyle='round,pad=0.34', fc=fc, ec=ec, lw=1.15))

    def edge(a, b, col, rad=0.0, ls='-', lw=1.25, lab=None, st=0.5):
        x1, y1, _ = N[a]; x2, y2, _ = N[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        cx, cy = mx + rad * dy, my - rad * dx
        p1 = clip(a, cx - x1, cy - y1)
        p2 = clip(b, cx - x2, cy - y2)
        ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=10,
                                     lw=lw, color=col, linestyle=ls,
                                     connectionstyle=f'arc3,rad={rad}',
                                     shrinkA=0, shrinkB=0, zorder=3))
        if lab:
            cx2 = (p1[0] + p2[0]) / 2 + rad * (p2[1] - p1[1])
            cy2 = (p1[1] + p2[1]) / 2 - rad * (p2[0] - p1[0])
            w0, w1, w2 = (1 - st) ** 2, 2 * st * (1 - st), st ** 2
            ax.text(w0 * p1[0] + w1 * cx2 + w2 * p2[0],
                    w0 * p1[1] + w1 * cy2 + w2 * p2[1], lab,
                    fontsize=6.3, color=col, ha='center', va='center', zorder=7,
                    bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none'))

    edge('tech', 'mkt', RED, lw=1.5)
    edge('mkt', 'sig', BLUE)
    edge('sig', 'bel', ORANGE)
    edge('bel', 'ch', PURPLE)
    edge('ch', 'pipe', PURPLE)
    edge('pipe', 'stk', GREEN, lab='D-year delay', st=0.5)
    edge('stk', 'mkt', TEAL, lab='congestion', st=0.55)

    ax.text(50, 8.5, 'B', fontsize=9.5, color=TEAL, ha='center', va='center',
            fontweight='bold',
            bbox=dict(boxstyle='circle,pad=0.30', fc='white', ec=TEAL, lw=1.2))
    ax.text(56.5, 8.5, 'the balancing loop the delay makes slow', fontsize=6.6,
            color=TEAL, ha='left', va='center')
    save(fig, 'p9_fig1.png')


# ============================================ Figure 2: calibration and the shock
def fig2():
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.0))
    cal = R['calibration']
    keys = ['share', 'u_other', 'premium', 'supply_elast']
    lab = ['share of cohort\nin the field', 'unemployment,\nother fields',
           'early-career\nwage premium', 'elasticity to\nrelative wage']
    ax = axes[0]
    y = np.arange(len(keys))[::-1]
    tgt = [cal['targets'][k] for k in keys]
    mod = [cal['moments'][k] for k in keys]
    ax.barh(y + 0.18, tgt, height=0.34, color=BLUE, alpha=0.85, label='target')
    ax.barh(y - 0.18, mod, height=0.34, color=GREEN, alpha=0.85, label='model')
    ax.set_yticks(y); ax.set_yticklabels(lab, fontsize=7.0)
    ax.set_title('Targeted moments', fontsize=8.4, pad=4)
    ax.legend(fontsize=6.9, frameon=False, loc='lower right')
    ax.set_xlabel('value', fontsize=7.4)
    style(ax)

    ax = axes[1]
    pa = R['paths']
    t = np.arange(len(pa['u0'])) - T0
    ax.plot(t, 100 * np.array(pa['u0']), color=RED, lw=1.7, label='exposed field')
    ax.plot(t, 100 * np.array(pa['u1']), color=BLUE, lw=1.4, ls='--',
            label='other fields')
    ax.axvline(0, color=MUT, lw=0.9, ls=':')
    ax.axhline(100 * R['shock']['target_peak_unemployment'], color=GREEN, lw=1.0,
               ls='-.', label='observed 7.0%')
    ax.set_xlim(-6, 40)
    ax.set_xlabel('years since the shock', fontsize=7.4)
    ax.set_ylabel('new-graduate unemployment (%)', fontsize=7.4)
    ax.set_title('The shock, sized to the data', fontsize=8.4, pad=4)
    ax.legend(fontsize=6.8, frameon=False, loc='upper right')
    style(ax)
    fig.tight_layout(pad=0.5, w_pad=1.5)
    save(fig, 'p9_fig2.png')


# ================================================== Figure 3: the transition path
def fig3():
    pa = R['paths']
    tr = R['transition']
    s = np.array(pa['s']); t = np.arange(len(s)) - T0
    s0 = tr['pre_shock_share']
    fig, axes = plt.subplots(1, 3, figsize=(7.3, 2.9))

    ax = axes[0]
    ax.plot(t, 100 * (s / s0 - 1.0), color=PURPLE, lw=1.8)
    ax.axhline(tr['long_run_change_pct'], color=GREEN, lw=1.1, ls='--',
               label='long run')
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=MUT, lw=0.9, ls=':')
    k = tr['years_to_trough']
    ax.plot([k], [tr['trough_change_pct']], 'o', color=RED, ms=5, zorder=5)
    ax.annotate('trough %.1f%%' % tr['trough_change_pct'],
                xy=(k, tr['trough_change_pct']),
                xytext=(k + 6, tr['trough_change_pct'] - 1.0),
                fontsize=6.8, color=RED)
    ax.set_xlim(-6, 50)
    ax.set_xlabel('years since the shock', fontsize=7.4)
    ax.set_ylabel('entering share, % change', fontsize=7.4)
    ax.set_title('Enrolment overshoots', fontsize=8.4, pad=4)
    ax.legend(fontsize=6.8, frameon=False, loc='lower right')
    style(ax)

    ax = axes[1]
    ax.plot(t, np.array(pa['prem']), color=ORANGE, lw=1.7)
    ax.axvline(0, color=MUT, lw=0.9, ls=':')
    ax.set_xlim(-6, 50)
    ax.set_xlabel('years since the shock', fontsize=7.4)
    ax.set_ylabel('early-career wage premium', fontsize=7.4)
    ax.set_title('The price signal', fontsize=8.4, pad=4)
    style(ax)

    ax = axes[2]
    ax.plot(t, np.array(pa['n_extrap']), color=CRIM, lw=1.7)
    ax.axvline(0, color=MUT, lw=0.9, ls=':')
    ax.set_ylim(0, 1.02)
    ax.set_xlim(-6, 50)
    ax.set_xlabel('years since the shock', fontsize=7.4)
    ax.set_ylabel('weight on extrapolation', fontsize=7.4)
    ax.set_title('Which rule entrants use', fontsize=8.4, pad=4)
    style(ax)
    fig.tight_layout(pad=0.5, w_pad=1.5)
    save(fig, 'p9_fig3.png')


# ==================================================== Figure 4: belief regimes
def fig4():
    reg = R['belief_regimes']
    order = ['anchored', 'mixed', 'baseline', 'imitative']
    lab = ['anchored\nonly', 'fixed\nmixture', 'baseline\n(switching)',
           'strong\nimitation']
    fig, axes = plt.subplots(1, 3, figsize=(7.3, 2.9))

    for ax, key, ttl, col, unit in [
            (axes[0], 'trough_change_pct', 'Depth of the overshoot', RED, '%'),
            (axes[1], 'amplification', 'Amplification', PURPLE, '×'),
            (axes[2], 'discounted_loss_pct', 'Output forgone', ORANGE, '%')]:
        v = [reg[k][key] for k in order]
        x = np.arange(len(order))
        ax.bar(x, v, color=col, alpha=0.85, width=0.62)
        ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=6.8)
        ax.set_title(ttl, fontsize=8.4, pad=4)
        lo, hi = min(0, min(v)), max(0, max(v))
        pad = 0.22 * (hi - lo if hi > lo else 1.0)
        ax.set_ylim(lo - pad, hi + pad)
        for xi, vi in zip(x, v):
            ax.text(xi, vi + (0.04 * (hi - lo) if vi >= 0 else -0.04 * (hi - lo)),
                    ('%.2f' % vi) + unit, ha='center',
                    va='bottom' if vi >= 0 else 'top', fontsize=6.7)
        style(ax)
    fig.tight_layout(pad=0.5, w_pad=1.4)
    save(fig, 'p9_fig4.png')


# ================================================= Figure 5: stability frontier
def fig5():
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.0))
    stb = R['stability']

    ax = axes[0]
    ax.plot(stb['psi_grid'], stb['modulus'], color=BLUE, lw=1.8)
    ax.axhline(1.0, color=RED, lw=1.1, ls='--')
    ax.axvline(stb['psi_baseline'], color=GREEN, lw=1.0, ls=':')
    if stb['psi_critical'] is not None:
        ax.plot([stb['psi_critical']], [1.0], 'o', color=RED, ms=5, zorder=5)
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.30 * (hi - lo))
    ax.text(stb['psi_baseline'], hi + 0.06 * (hi - lo), ' calibrated',
            fontsize=6.8, color=GREEN, ha='left', va='bottom')
    if stb['psi_critical'] is not None:
        ax.text(stb['psi_critical'], hi + 0.18 * (hi - lo),
                'loses stability at ψ = %.0f' % stb['psi_critical'],
                fontsize=6.8, color=RED, ha='center', va='bottom')
    ax.set_xlabel('intensity of choice over forecasting rules, ψ', fontsize=7.4)
    ax.set_ylabel('modulus of the dominant mode', fontsize=7.4)
    ax.set_title('Imitation destabilises', fontsize=8.4, pad=4)
    style(ax)

    ax = axes[1]
    fr = R['frontier']
    sigmas = sorted({d['sigma'] for d in fr})
    cols = [GREEN, BLUE, ORANGE, PURPLE, CRIM]
    for i, sg in enumerate(sigmas):
        pts = sorted([d for d in fr if d['sigma'] == sg],
                     key=lambda d: d['supply_elast'])
        ax.plot([d['supply_elast'] for d in pts],
                [abs(d['loop_gain']) for d in pts], 'o-', ms=3.4, lw=1.4,
                color=cols[i % len(cols)], label='σ = %.1f' % sg)
    ax.axhline(1.0, color=RED, lw=1.1, ls='--')
    ax.set_xlabel('elasticity of field choice to the relative wage', fontsize=7.4)
    ax.set_ylabel('absolute loop gain', fontsize=7.4)
    ax.set_title('Where the loop gain reaches one', fontsize=8.4, pad=4)
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.28 * (hi - lo))
    ax.legend(fontsize=6.7, frameon=False, ncol=2, loc='upper left')
    style(ax)
    fig.tight_layout(pad=0.5, w_pad=1.5)
    save(fig, 'p9_fig5.png')


# ==================================================== Figure 6: the instruments
def fig6():
    ins = R['instruments']
    order = ['noisier_wage_signal', 'baseline', 'pipeline_published_half',
             'pipeline_published_full']
    lab = ['noisier wage\nsignal (ω=0.6)', 'baseline', 'pipeline\npublished (half)',
           'pipeline\npublished (full)']
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.0))

    ax = axes[0]
    v = [ins[k]['amplification'] for k in order]
    x = np.arange(len(order))
    cols = [RED, MUT, GREEN, TEAL]
    ax.bar(x, v, color=cols, alpha=0.88, width=0.62)
    ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=6.7)
    ax.set_ylabel('amplification of the overshoot', fontsize=7.4)
    ax.set_title('What dampens the swing', fontsize=8.4, pad=4)
    hi = max(v)
    ax.set_ylim(0, hi * 1.22)
    for xi, vi in zip(x, v):
        ax.text(xi, vi + 0.03 * hi, '%.2f×' % vi, ha='center', va='bottom',
                fontsize=6.8)
    style(ax)

    ax = axes[1]
    v = [ins[k]['discounted_loss_pct'] for k in order]
    ax.bar(x, v, color=cols, alpha=0.88, width=0.62)
    ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=6.7)
    ax.set_ylabel('output forgone, % of the post-shock level', fontsize=7.4)
    ax.set_title('What it is worth', fontsize=8.4, pad=4)
    hi = max(v)
    ax.set_ylim(0, hi * 1.22)
    for xi, vi in zip(x, v):
        ax.text(xi, vi + 0.03 * hi, '%.3f%%' % vi, ha='center', va='bottom',
                fontsize=6.8)
    style(ax)
    fig.tight_layout(pad=0.5, w_pad=1.5)
    save(fig, 'p9_fig6.png')


# ================================================== Figure 7: global sensitivity
def fig7():
    se = R['sensitivity']
    d = se['draws']
    fig, axes = plt.subplots(1, 3, figsize=(7.3, 2.8))

    for ax, key, ttl, col, xlab in [
            (axes[0], 'amplification', 'Amplification', PURPLE,
             'trough ÷ long-run change'),
            (axes[1], 'loss', 'Output forgone', ORANGE, '% of post-shock output'),
            (axes[2], 'modulus', 'Dominant modulus', BLUE, 'modulus')]:
        v = np.array(d[key])
        ax.hist(v, bins=22, color=col, alpha=0.82, edgecolor='white', linewidth=0.4)
        ax.axvline(float(np.mean(v)), color=INK, lw=1.2, ls='--')
        if key == 'modulus':
            ax.axvline(1.0, color=RED, lw=1.1, ls='-')
        ax.set_xlabel(xlab, fontsize=7.3)
        ax.set_ylabel('draws', fontsize=7.3)
        ax.set_title(ttl, fontsize=8.4, pad=4)
        lo, hi = ax.get_ylim()
        ax.set_ylim(lo, hi * 1.26)
        ax.text(0.03, 0.94, 'mean %.2f\n5–95%%  %.2f–%.2f'
                % (np.mean(v), np.percentile(v, 5), np.percentile(v, 95)),
                transform=ax.transAxes, fontsize=6.5, va='top', color=MUT)
        style(ax)
    fig.tight_layout(pad=0.5, w_pad=1.4)
    save(fig, 'p9_fig7.png')


if __name__ == '__main__':
    for fn in (fig1, fig2, fig3, fig4, fig5, fig6, fig7):
        fn()
    print('figures written:',
          sorted(f for f in os.listdir(HERE) if f.startswith('p9_fig')))
