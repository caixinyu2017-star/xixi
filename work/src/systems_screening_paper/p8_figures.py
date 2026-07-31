# -*- coding: utf-8 -*-
"""Paper 8 figures. Every plotted value is read from p8_results.json so the
figures and the text cannot disagree."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'p8_results.json')))

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.6,
                     'axes.linewidth': 0.8, 'axes.edgecolor': '#3a3a3a'})
INK, MUT, GRID = '#111111', '#5a5a5a', '#d8d8d8'
BLUE, RED, GREEN, ORANGE, PURPLE = '#2c6fbb', '#c0392b', '#1e8449', '#d68910', '#6c3483'
TEAL, CRIM = '#00695c', '#c2185b'
DPI = 320

PARAMS = R['m2_mixed']['names']
LAB = {
    'ai': 'Disclosed AI assistance',
    'proc': 'Process-evidence portfolio',
    'ai_proc': 'Disclosure × process evidence',
    'test70': 'Verified assessment, 70th pct',
    'test90': 'Verified assessment, 90th pct',
    'inst': 'Elite institution',
    'refer': 'Employee referral',
    'intern': 'Relevant internship',
    'wage': 'Expected salary (+1000 CNY)',
    'optout': 'Neither candidate',
}


def style(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, color=GRID, lw=0.5, alpha=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=7.6, length=3, color='#7a7a7a')


# =============================================== Figure 1: conceptual framework
def fig1():
    W_IN, H_IN = 7.4, 4.7
    XR, YR = 100.0, 64.0
    fig, ax = plt.subplots(figsize=(W_IN, H_IN))
    ax.set_xlim(0, XR); ax.set_ylim(0, YR); ax.axis('off')
    ux, uy = XR / W_IN, YR / H_IN
    FS = 7.4

    N = {
        'ai':   (12, 55, 'Generative AI\nwrites the\napplication'),
        'cost': (12, 36, 'Cost of producing\na polished\napplication → 0'),
        'sig':  (37, 45, 'Written signal\nstops separating\ncandidates'),
        'r1':   (68, 57, 'R1  Retreat to\nascriptive signals\n(institution, referral)'),
        'r2':   (68, 40, 'R2  Triage on\nvolume\n(AI screening score)'),
        'r3':   (68, 26, 'R3  Restore a\ncostly signal\n(verified test, process)'),
        'acc':  (92, 48, 'Narrower\naccess for\nnon-elite youth'),
        'fit':  (92, 26, 'Access on\ndemonstrated\ncapability'),
    }

    def half(key):
        _, _, t = N[key]
        lines = t.split('\n')
        w_in = max(len(s) for s in lines) * FS * 0.545 / 72.0
        h_in = len(lines) * FS * 1.32 / 72.0
        return w_in * ux / 2 + 1.3, h_in * uy / 2 + 1.2

    def clip(key, dx, dy):
        x, y, _ = N[key]
        hw, hh = half(key)
        sx = abs(dx) / hw if dx else 0.0
        sy = abs(dy) / hh if dy else 0.0
        s = max(sx, sy, 1e-9)
        return x + dx / s, y + dy / s

    face = {'ai': ('#e6eefa', BLUE), 'cost': ('#e6eefa', BLUE),
            'sig': ('#fdecec', RED), 'r1': ('#fdf2e2', ORANGE),
            'r2': ('#f2ecf7', PURPLE), 'r3': ('#e7f5ec', GREEN),
            'acc': ('#fdecec', CRIM), 'fit': ('#e7f5ec', TEAL)}
    for key in N:
        x, y, t = N[key]
        fc, ec = face[key]
        ax.text(x, y, t, ha='center', va='center', fontsize=FS, color=INK,
                zorder=6, linespacing=1.3,
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
                    fontsize=6.4, color=col, ha='center', va='center', zorder=7,
                    bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none'))

    edge('ai', 'cost', BLUE, lw=1.5)
    edge('cost', 'sig', RED, lw=1.5)
    edge('ai', 'sig', RED, lw=1.5)
    edge('sig', 'r1', ORANGE)
    edge('sig', 'r2', PURPLE)
    edge('sig', 'r3', GREEN)
    edge('r1', 'acc', CRIM)
    edge('r2', 'acc', CRIM)
    edge('r3', 'fit', TEAL)
    # the disclosure trap: penalising disclosure feeds back into concealment
    edge('acc', 'sig', CRIM, rad=0.55, ls=(0, (5, 2.4)), lw=1.2,
         lab='concealment feedback', st=0.5)

    # the explanatory notes live in the caption, not in the artwork
    ax.set_ylim(19, YR)
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    fig.savefig(os.path.join(HERE, 'p8_fig1.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ================================================= Figure 2: example choice task
def fig2():
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    ax.set_xlim(0, 100); ax.set_ylim(0, 52); ax.axis('off')
    rows = [
        ('Application states AI assistance was used', 'Yes', 'No'),
        ('Process-evidence portfolio (drafts, revisions,\nreasoning notes)',
         'Yes', 'No'),
        ('Verified proctored assessment', '90th percentile', 'Not taken'),
        ('Institution', 'Non-elite', 'Elite'),
        ('Employee referral', 'No', 'Yes'),
        ('Relevant internship (6 months)', 'Yes', 'No'),
        ('Expected monthly salary', '10,000 CNY', '12,000 CNY'),
    ]
    x0, xa, xb = 4, 55, 79
    ax.text(x0, 47.5, 'Attribute', fontsize=7.6, fontweight='bold')
    ax.text(xa, 47.5, 'Candidate A', fontsize=7.6, fontweight='bold', ha='center')
    ax.text(xb, 47.5, 'Candidate B', fontsize=7.6, fontweight='bold', ha='center')
    ax.plot([2, 96], [45.6, 45.6], color=INK, lw=1.0)
    y = 42.0
    for i, (a, b, c) in enumerate(rows):
        nl = a.count('\n') + 1
        ax.text(x0, y, a, fontsize=7.0, va='top')
        ax.text(xa, y, b, fontsize=7.0, ha='center', va='top')
        ax.text(xb, y, c, fontsize=7.0, ha='center', va='top')
        y -= 3.1 * nl + 1.5
        if i < len(rows) - 1:
            ax.plot([2, 96], [y + 1.4, y + 1.4], color='#dddddd', lw=0.6)
    ax.plot([2, 96], [y + 1.2, y + 1.2], color=INK, lw=1.0)
    ax.text(x0, y - 2.4, 'Which candidate would you shortlist?   '
                         '☐ Candidate A     ☐ Candidate B     '
                         '☐ Neither of these two', fontsize=7.2)
    d = R['design']
    ax.text(x0, y - 7.2,
            'Each respondent completed %d such tasks drawn from a D-efficient '
            'design (D-error %.3f); %s choice sets in total.'
            % (d['n_tasks'], d['d_error'], f"{d['n_choice_sets']:,}"),
            fontsize=6.6, color=MUT)
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    fig.savefig(os.path.join(HERE, 'p8_fig2.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ============================================ Figure 3: mixed logit part-worths
def fig3():
    m = R['m2_mixed']
    keys = ['test90', 'test70', 'inst', 'refer', 'intern', 'proc', 'ai_proc',
            'ai', 'wage']
    idx = [m['names'].index(k) for k in keys]
    mu = np.array([m['mean'][i] for i in idx])
    se = np.array([m['mean_se'][i] for i in idx])
    sd = np.array([m['sd'][i] for i in idx])
    sdse = np.array([m['sd_se'][i] for i in idx])

    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.6),
                             gridspec_kw={'width_ratios': [1.35, 1.0]})
    ax = axes[0]
    y = np.arange(len(keys))[::-1]
    cols = [GREEN if v > 0 else RED for v in mu]
    ax.errorbar(mu, y, xerr=1.96 * se, fmt='o', ms=5, capsize=3,
                elinewidth=1.1, ecolor=INK, mfc='white', mec=INK, zorder=4)
    for yy, v, c in zip(y, mu, cols):
        ax.plot([0, v], [yy, yy], color=c, lw=3.0, alpha=0.55, zorder=2,
                solid_capstyle='butt')
    ax.axvline(0, color=INK, lw=0.9)
    ax.set_yticks(y)
    ax.set_yticklabels([LAB[k] for k in keys], fontsize=7.2)
    ax.set_xlabel('mean part-worth utility (95% CI)', fontsize=7.4)
    ax.set_title('What employers weight', fontsize=8.4, pad=4)
    style(ax)

    ax = axes[1]
    ax.errorbar(sd, y, xerr=1.96 * sdse, fmt='s', ms=4.4, capsize=3,
                elinewidth=1.1, ecolor=PURPLE, mfc='white', mec=PURPLE)
    ax.axvline(0, color=INK, lw=0.9)
    ax.set_yticks(y); ax.set_yticklabels([])
    ax.set_xlabel('standard deviation of the part-worth', fontsize=7.4)
    ax.set_title('How much employers differ', fontsize=8.4, pad=4)
    style(ax)
    fig.tight_layout(pad=0.5, w_pad=1.2)
    fig.savefig(os.path.join(HERE, 'p8_fig3.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# =================================== Figure 4: the disclosure penalty and repair
def fig4():
    t = R['tradeoffs']
    a = t['disclosure_penalty_no_evidence']
    b = t['disclosure_penalty_with_evidence']
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.2),
                             gridspec_kw={'width_ratios': [1.0, 1.15]})

    ax = axes[0]
    xs = [0, 1]
    vals = [a['utility'], b['utility']]
    errs = [1.96 * a['se'], 1.96 * b['se']]
    cols = [RED, GREEN]
    ax.bar(xs, vals, yerr=errs, color=cols, alpha=0.85, width=0.55,
           capsize=4, error_kw=dict(elinewidth=1.1, ecolor=INK))
    ax.axhline(0, color=INK, lw=0.9)
    ax.set_xticks(xs)
    ax.set_xticklabels(['without process\nevidence', 'with process\nevidence'],
                       fontsize=7.4)
    ax.set_ylabel('utility effect of disclosing AI assistance', fontsize=7.4)
    ax.set_title('The disclosure penalty and its repair', fontsize=8.4, pad=4)
    # labels sit clear of the whisker so the shorter bar's value cannot ride up
    # into the panel title
    for x, v, e in zip(xs, vals, errs):
        ax.text(x, v - e - 0.05, f'{v:+.3f}', ha='center', va='top',
                fontsize=7.0)
    ax.set_ylim(min(v - e for v, e in zip(vals, errs)) - 0.22, 0.03)
    style(ax)

    ax = axes[1]
    by = t['by_attribute']
    keys = ['test90', 'test70', 'inst', 'refer', 'intern', 'proc', 'ai']
    vals = [by[k]['estimate'] for k in keys]
    ses = [by[k]['se'] for k in keys]
    y = np.arange(len(keys))[::-1]
    cols = [GREEN if v > 0 else RED for v in vals]
    ax.barh(y, vals, xerr=[1.96 * s for s in ses], color=cols, alpha=0.85,
            height=0.6, capsize=3, error_kw=dict(elinewidth=1.0, ecolor=INK))
    ax.axvline(0, color=INK, lw=0.9)
    ax.set_yticks(y); ax.set_yticklabels([LAB[k] for k in keys], fontsize=7.2)
    ax.set_xlabel('equivalent monthly salary, thousand CNY (95% CI)',
                  fontsize=7.4)
    ax.set_title('What each signal is worth', fontsize=8.4, pad=4)
    style(ax)
    fig.tight_layout(pad=0.5, w_pad=1.4)
    fig.savefig(os.path.join(HERE, 'p8_fig4.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ==================================== Figure 5: latent classes and model choice
def fig5():
    sel = R['lc_selection']
    lc = R['m3_latent_class']
    C = lc['n_classes']
    names = ['C%d' % (i + 1) for i in range(C)]
    fig = plt.figure(figsize=(7.3, 4.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[0.9, 1.45], wspace=0.46)

    ax = fig.add_subplot(gs[0, 0])
    ks = [s['n_classes'] for s in sel]
    ax.plot(ks, [s['bic'] for s in sel], 'o-', color=BLUE, lw=1.8, ms=5,
            label='BIC')
    ax.plot(ks, [s['caic'] for s in sel], 's--', color=PURPLE, lw=1.3, ms=4,
            label='CAIC')
    kb = C
    ax.axvline(kb, color=GREEN, lw=1.0, ls=':')
    bic_min = min(s['bic'] for s in sel)
    ax.annotate('selected', xy=(kb, bic_min), xytext=(kb + 0.18, bic_min),
                fontsize=6.8, color=GREEN, va='center')
    ax.set_xticks(ks)
    ax.set_xlabel('number of latent classes', fontsize=7.4)
    ax.set_ylabel('information criterion', fontsize=7.4)
    ax.set_title('Selecting the number of regimes', fontsize=8.4, pad=4)
    # headroom above the highest series point so the legend never sits on a curve
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.30 * (hi - lo))
    ax.legend(fontsize=6.8, frameon=False, loc='upper left')
    style(ax)

    # horizontal bars: attribute names get the full panel width, so the seven
    # labels cannot collide with one another
    ax = fig.add_subplot(gs[0, 1])
    keys = ['test90', 'test70', 'proc', 'ai', 'inst', 'refer', 'intern']
    ii = [lc['names'].index(k) for k in keys]
    h = 0.8 / C
    cols = [GREEN, ORANGE, PURPLE, BLUE, CRIM][:C]
    ys = np.arange(len(keys))[::-1]
    for c in range(C):
        v = [lc['b'][c][i] for i in ii]
        ax.barh(ys - (c - (C - 1) / 2) * h, v, height=h, color=cols[c],
                alpha=0.88, label='%s (%.0f%%)' % (names[c], 100 * lc['share'][c]))
    ax.axvline(0, color=INK, lw=0.9)
    ax.set_yticks(ys)
    short = {'test90': 'Assessment,\n90th pct', 'test70': 'Assessment,\n70th pct',
             'proc': 'Process\nevidence', 'ai': 'Disclosed\nAI use',
             'inst': 'Elite\ninstitution', 'refer': 'Employee\nreferral',
             'intern': 'Relevant\ninternship'}
    ax.set_yticklabels([short[k] for k in keys], fontsize=7.0)
    ax.set_xlabel('part-worth utility', fontsize=7.4)
    ax.set_title('Three screening regimes', fontsize=8.4, pad=4)
    lo, hi = ax.get_xlim()
    ax.set_xlim(lo, hi + 0.42 * (hi - lo))
    ax.legend(fontsize=6.8, frameon=False, loc='lower right')
    style(ax)
    fig.savefig(os.path.join(HERE, 'p8_fig5.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# =========================== Figure 6: who ends up in which regime (membership)
def fig6():
    mm = R['m4_membership']
    lc = R['m3_latent_class']
    C = lc['n_classes']
    ref = mm['reference_class']
    B = np.array(mm['b'])                    # (C-1, q)
    full = np.zeros((C, B.shape[1]))
    r = 0
    for c in range(C):
        if c == ref:
            continue
        full[c] = B[r]; r += 1

    names = ['C%d' % (i + 1) for i in range(C)]
    cols = [GREEN, ORANGE, PURPLE, BLUE, CRIM][:C]
    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.1))
    grid = np.linspace(-2, 2, 120)
    for ax, j, lab in ((axes[0], 2, 'Perceived share of applications\nthat are '
                                    'AI-assisted (standardised)'),
                       (axes[1], 3, 'Growth in application volume\n(standardised)')):
        Z = np.zeros((len(grid), B.shape[1]))
        Z[:, 0] = 1.0
        Z[:, j] = grid
        v = Z @ full.T
        v = v - v.max(axis=1, keepdims=True)
        p = np.exp(v); p /= p.sum(axis=1, keepdims=True)
        for c in range(C):
            ax.plot(grid, p[:, c], color=cols[c], lw=2.0, label=names[c])
        ax.set_ylim(0, 1)
        ax.set_xlabel(lab, fontsize=7.2)
        ax.set_ylabel('predicted class probability', fontsize=7.4)
        style(ax)
    axes[0].set_title('Signal degradation drives the retreat', fontsize=8.4, pad=4)
    axes[1].set_title('Volume drives triage', fontsize=8.4, pad=4)
    axes[0].legend(fontsize=6.8, frameon=False, ncol=C, loc='upper center')
    fig.tight_layout(pad=0.5, w_pad=1.6)
    fig.savefig(os.path.join(HERE, 'p8_fig6.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ================================= Figure 7: the randomised architecture result
def fig7():
    pb = R['partB']
    arms = pb['arms']
    cols = [PURPLE, ORANGE, GREEN]
    panels = [('nonelite_share', 'share of the shortlist from\nnon-elite institutions',
               'Access', 1.0),
              ('assessment_pct', 'mean verified-assessment\npercentile of the shortlist',
               'Measured quality', 1.0),
              ('seconds_per_applicant', 'seconds spent per applicant',
               'Screening cost', 1.0)]
    fig, axes = plt.subplots(1, 3, figsize=(7.3, 2.9))
    for ax, (key, ylab, title, sc) in zip(axes, panels):
        d = pb[key]
        m = np.array(d['means']) * sc
        se = np.array(d['sds']) / np.sqrt(np.array(d['n'])) * sc
        xs = np.arange(3)
        ax.bar(xs, m, yerr=1.96 * se, color=cols, alpha=0.88, width=0.6,
               capsize=4, error_kw=dict(elinewidth=1.1, ecolor=INK))
        ax.set_xticks(xs)
        ax.set_xticklabels(['AI-score\nfirst', 'Credential\nfirst',
                            'Evidence\nfirst'], fontsize=7.0)
        ax.set_ylabel(ylab, fontsize=7.2)
        ax.set_title(title, fontsize=8.2, pad=4)
        lo = min(m - 1.96 * se); hi = max(m + 1.96 * se)
        pad = (hi - lo) * 0.35
        ax.set_ylim(max(0, lo - pad), hi + pad)
        ax.text(0.5, 0.965, 'F(2, %d) = %.2f, p %s' % (
            sum(d['n']) - 3, d['F'],
            '< 0.001' if d['p'] < 0.001 else '= %.3f' % d['p']),
            transform=ax.transAxes, ha='center', va='top', fontsize=6.6,
            color=MUT)
        style(ax)
    fig.tight_layout(pad=0.5, w_pad=1.5)
    fig.savefig(os.path.join(HERE, 'p8_fig7.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7()
    print('figures written:', [f'p8_fig{i}.png' for i in range(1, 8)])
