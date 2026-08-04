# -*- coding: utf-8 -*-
"""Publication figures.  Every figure is drawn from an estimation output file
produced by estimate.py.  All legends are placed BELOW the plotting area so that
no legend can overlap the data."""
from __future__ import annotations

import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'out')
TAB = os.path.join(HERE, '..', 'tables')
FIG = os.path.join(HERE, '..', 'figures')
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 8.5, 'axes.labelsize': 8.5,
    'axes.titlesize': 9, 'xtick.labelsize': 8, 'ytick.labelsize': 8,
    'legend.fontsize': 8, 'axes.linewidth': 0.8, 'lines.linewidth': 1.4,
    'xtick.major.width': 0.8, 'ytick.major.width': 0.8,
    'axes.spines.top': False, 'axes.spines.right': False,
    'figure.dpi': 400, 'savefig.dpi': 400, 'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.03,
})

# Okabe-Ito, colour-blind safe; markers and line styles give redundant encoding
C = {'blue': '#0072B2', 'orange': '#E69F00', 'green': '#009E73', 'red': '#D55E00',
     'purple': '#CC79A7', 'sky': '#56B4E9', 'grey': '#5A5A5A'}


def legend_below(fig, handles, labels, ncol=3, pad=0.10, labelspacing=0.5):
    """Place a single legend beneath the whole figure, clear of the x-axis label.

    `pad` is the vertical gap, in figure-height units, between the bottom of the
    axes area and the top of the legend."""
    fig.tight_layout()
    fig.legend(handles, labels, loc='upper center',
               bbox_to_anchor=(0.5, -pad), bbox_transform=fig.transFigure,
               ncol=ncol, frameon=False, handlelength=1.8, columnspacing=1.6,
               labelspacing=labelspacing, borderaxespad=0.0, borderpad=0.0)


# ==================================================================================
def fig3_event():
    d = pd.read_csv(os.path.join(RAW, 'event_study.csv')).sort_values('rel')
    pt = pd.read_csv(os.path.join(RAW, 'pretrend_test.csv'), index_col=0).iloc[:, 0]
    fig, ax = plt.subplots(figsize=(5.1, 3.0))
    ax.axhline(0, color='k', lw=0.8)
    ax.axvline(-0.5, color=C['grey'], lw=1.0, ls='--')
    ax.errorbar(d.rel, d.coef, yerr=[d.coef - d.lo, d.hi - d.coef], fmt='o',
                color=C['blue'], ecolor=C['blue'], elinewidth=1.0, capsize=2.5,
                markersize=4.2, markerfacecolor='white', markeredgewidth=1.2,
                label='Point estimate with 95% confidence interval')
    base = d[d.rel == -1]
    ax.plot(base.rel, base.coef, 'o', color=C['red'], markersize=5.2, zorder=5,
            label='Reference year (2021), normalised to zero')
    ax.set_xlabel('Years relative to the generative-AI shock (2022 = 0)')
    ax.set_ylabel('Effect on the youth employment share')
    ax.set_xticks(range(-6, 3))
    ax.text(0.02, 0.06, f'Joint test of pre-shock leads: $\\chi^2$ = {pt["chi2"]:.2f}, '
                        f'$p$ = {pt["p"]:.3f}',
            transform=ax.transAxes, fontsize=7.6)
    h = [Line2D([0], [0], color=C['blue'], marker='o', markerfacecolor='white',
                markeredgewidth=1.2, markersize=4.2),
         Line2D([0], [0], color=C['red'], marker='o', ls='none', markersize=5.2),
         Line2D([0], [0], color=C['grey'], ls='--')]
    lab = ['Point estimate with 95% confidence interval',
           'Reference year (2021), normalised to zero',
           'Timing of the generative-AI shock']
    legend_below(fig, h, lab, ncol=1, pad=0.005, labelspacing=0.28)
    fig.savefig(os.path.join(FIG, 'fig3_event_study.png'))
    plt.close(fig)
    print('fig3_event_study.png')


# ==================================================================================
def fig4_psm():
    d = pd.read_csv(os.path.join(RAW, 'psm_balance.csv'))
    d = d.iloc[::-1]
    y = np.arange(len(d))
    fig, ax = plt.subplots(figsize=(5.1, 3.4))
    ax.axvline(0, color='k', lw=0.8)
    for s in (-10, 10):
        ax.axvline(s, color=C['grey'], lw=0.7, ls=':')
    ax.scatter(d['%bias (unmatched)'], y, marker='o', s=26, facecolors='none',
               edgecolors=C['red'], linewidths=1.1)
    ax.scatter(d['%bias (matched)'], y, marker='D', s=22, color=C['blue'])
    ax.set_yticks(y); ax.set_yticklabels(d.Variable)
    ax.set_xlabel('Standardised percentage bias across the treated and control groups')
    ax.grid(axis='x', ls=':', lw=0.5, alpha=0.6); ax.set_axisbelow(True)
    h = [Line2D([0], [0], marker='o', ls='none', markerfacecolor='none',
                markeredgecolor=C['red'], markersize=5.4),
         Line2D([0], [0], marker='D', ls='none', color=C['blue'], markersize=4.6),
         Line2D([0], [0], color=C['grey'], ls=':')]
    legend_below(fig, h, ['Before matching', 'After matching',
                          'Conventional 10% threshold'], ncol=3, pad=0.01, labelspacing=0.28)
    fig.savefig(os.path.join(FIG, 'fig4_psm_balance.png'))
    plt.close(fig)
    print('fig4_psm_balance.png')


# ==================================================================================
def fig5_marginal():
    d = pd.read_csv(os.path.join(RAW, 'marginal_effects.csv'))
    s = pd.read_csv(os.path.join(RAW, 'moderation_summary.csv'), index_col=0).iloc[:, 0]
    panel = pd.read_csv(os.path.join('..', 'data', 'panel.csv'), usecols=['OLC'])
    fig, ax = plt.subplots(figsize=(5.1, 3.0))
    ax.axhline(0, color='k', lw=0.8)
    ax.plot(d.OLC, d.me, color=C['blue'], lw=1.6)
    ax.fill_between(d.OLC, d.lo, d.hi, color=C['blue'], alpha=0.18, linewidth=0)
    cross = float(s['crossing_sd'])
    drawn = -2.5 < cross < 2.5
    if drawn:
        ax.axvline(cross, color=C['red'], ls='--', lw=1.1)
        ax.annotate(f'zero crossing at {cross:.2f} SD', xy=(cross, 0),
                    xytext=(cross + 0.12, ax.get_ylim()[1] * 0.55), fontsize=7.4,
                    color=C['red'])
    ax2 = ax.twinx()
    ax2.hist(panel.OLC, bins=45, color=C['grey'], alpha=0.16, linewidth=0)
    ax2.set_yticks([]); ax2.spines['right'].set_visible(False)
    ax.set_zorder(ax2.get_zorder() + 1); ax.patch.set_visible(False)
    ax.set_xlabel('Organisational learning capacity (standard deviations from the mean)')
    ax.set_ylabel('Marginal effect of treatment\non the youth employment share')
    ax.set_xlim(-2.5, 2.5)
    h = [Line2D([0], [0], color=C['blue'], lw=1.6),
         Patch(facecolor=C['blue'], alpha=0.18),
         Patch(facecolor=C['grey'], alpha=0.16)]
    lab = ['Marginal effect', '95% confidence band',
           'Sample distribution of the moderator']
    if drawn:
        h.insert(2, Line2D([0], [0], color=C['red'], ls='--'))
        lab.insert(2, 'Zero crossing')
    legend_below(fig, h, lab, ncol=3 if not drawn else 2, pad=0.01, labelspacing=0.28)
    fig.savefig(os.path.join(FIG, 'fig5_marginal_effect.png'))
    plt.close(fig)
    print('fig5_marginal_effect.png')


# ==================================================================================
def fig6_heterogeneity():
    d = pd.read_csv(os.path.join(RAW, 'heterogeneity.csv'))
    d = d.iloc[::-1].reset_index(drop=True)
    y = np.arange(len(d))
    lo = d.coef - 1.96 * d.se
    hi = d.coef + 1.96 * d.se
    fig, ax = plt.subplots(figsize=(5.1, 3.2))
    ax.axvline(0, color='k', lw=0.8)
    for i in range(len(d)):
        ax.plot([lo[i], hi[i]], [y[i], y[i]], color=C['blue'], lw=1.2)
    ax.scatter(d.coef, y, marker='s', s=26, color=C['blue'], zorder=4)
    for i in range(len(d)):
        ax.text(hi[i] + 0.006, y[i], f'n = {int(d.n[i]):,}', va='center', fontsize=6.8,
                color=C['grey'])
    ax.set_yticks(y); ax.set_yticklabels(d.group)
    ax.set_xlabel('Estimated effect of treatment on the youth employment share')
    ax.grid(axis='x', ls=':', lw=0.5, alpha=0.6); ax.set_axisbelow(True)
    ax.set_xlim(min(lo) - 0.03, max(hi) + 0.055)
    h = [Line2D([0], [0], marker='s', color=C['blue'], markersize=4.8),
         Line2D([0], [0], color=C['blue'], lw=1.2)]
    legend_below(fig, h, ['Subsample point estimate', '95% confidence interval'],
                 ncol=2, pad=0.01, labelspacing=0.28)
    fig.savefig(os.path.join(FIG, 'fig6_heterogeneity.png'))
    plt.close(fig)
    print('fig6_heterogeneity.png')


# ==================================================================================
def fig7_placebo():
    d = pd.read_csv(os.path.join(RAW, 'placebo.csv'))
    s = pd.read_csv(os.path.join(RAW, 'placebo_summary.csv'), index_col=0).iloc[:, 0]
    fig, ax = plt.subplots(figsize=(5.1, 3.0))
    ax.hist(d.coef, bins=48, color=C['sky'], edgecolor='white', linewidth=0.3)
    ax.axvline(0, color=C['grey'], lw=0.9, ls=':')
    ax.axvline(float(s['actual']), color=C['red'], lw=1.6)
    ax.annotate(f"actual estimate\n{float(s['actual']):.4f}",
                xy=(float(s['actual']), ax.get_ylim()[1] * 0.72),
                xytext=(float(s['actual']) + 0.018, ax.get_ylim()[1] * 0.72),
                fontsize=7.4, color=C['red'], va='center',
                arrowprops=dict(arrowstyle='->', color=C['red'], lw=0.9))
    ax.set_xlabel('Estimated coefficient under randomly reassigned entry-task exposure')
    ax.set_ylabel('Number of placebo draws')
    h = [Patch(facecolor=C['sky']), Line2D([0], [0], color=C['red'], lw=1.6),
         Line2D([0], [0], color=C['grey'], ls=':')]
    legend_below(fig, h, ['Placebo distribution', 'Actual estimate', 'Zero'],
                 ncol=3, pad=0.01, labelspacing=0.28)
    fig.savefig(os.path.join(FIG, 'fig7_placebo.png'))
    plt.close(fig)
    print('fig7_placebo.png')


if __name__ == '__main__':
    import sys
    jobs = {'3': fig3_event, '4': fig4_psm, '5': fig5_marginal,
            '6': fig6_heterogeneity, '7': fig7_placebo}
    for k in (sys.argv[1:] or list(jobs)):
        jobs[k]()
