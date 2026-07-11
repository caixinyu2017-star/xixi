# -*- coding: utf-8 -*-
"""Generate Figure 1 (conceptual framework) and Figure 2 (PSM balance)."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

SCRATCH = os.path.dirname(os.path.abspath(__file__))
plt.rcParams['font.family'] = 'DejaVu Sans'

# ---------------------------------------------------------------- Figure 1
fig, ax = plt.subplots(figsize=(9.0, 5.0), dpi=200)
ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis('off')

def box(x, y, w, h, text, fc='#f2f2f2', fs=9.5, bold=False):
    p = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.6,rounding_size=1.6',
                       linewidth=1.1, edgecolor='#333333', facecolor=fc)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs,
            weight='bold' if bold else 'normal', linespacing=1.4)

def arrow(x1, y1, x2, y2, style='-|>', dashed=False, lw=1.4):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=16, linewidth=lw, color='#333333',
                        linestyle='--' if dashed else '-')
    ax.add_patch(a)

# X box
box(2, 26, 22, 12, 'Industrial intelligent\ntransformation\n(robot penetration, II)', fc='#dce6f1', bold=True)
# Mediators
box(38, 40, 24, 10, 'Skill restructuring\n(firm skill structure, SKILL)', fc='#f2f2f2')
box(38, 12, 24, 10, 'Expansion effect\n(labor productivity, lnPROD)', fc='#f2f2f2')
# Y box
box(76, 26, 22, 13, 'Youth employment (YEMP)\nYouth career\ndevelopment (YCAR)', fc='#dce6f1', bold=True)
# Moderators
box(30, 0.5, 40, 7.5,
    'Multi-level employment governance\nTRAIN (firm)  ·  PES (regional)  ·  POLICY (policy pilots)',
    fc='#e9f2e4', fs=9)

# arrows X -> mediators -> Y
arrow(24, 34.5, 37.5, 44)     # X -> skill
arrow(24, 29.5, 37.5, 18)     # X -> productivity
arrow(62.5, 44.5, 75.5, 34.5) # skill -> Y
arrow(62.5, 17.5, 75.5, 29.5) # prod -> Y
# direct X -> Y (H1)
arrow(24, 32, 75.5, 32.4)
ax.text(50, 33.6, 'H1a / H1b', ha='center', fontsize=9, style='italic')
ax.text(30.5, 42.5, 'H2a', ha='center', fontsize=9, style='italic')
ax.text(30.5, 21.0, 'H2b', ha='center', fontsize=9, style='italic')
# moderation arrow (routed right of the mediator boxes)
arrow(69.5, 8.6, 69.5, 30.8, dashed=True)
ax.text(71.2, 13.6, 'H3a–H3c', ha='left', fontsize=9, style='italic')

plt.tight_layout(pad=0.4)
plt.savefig(os.path.join(SCRATCH, 'fig_framework.png'), bbox_inches='tight',
            facecolor='white')
plt.close()

# ---------------------------------------------------------------- Figure 2
covs = ['Age', 'Size', 'Lev', 'RoA', 'Cash', 'Growth', 'Top10', 'Board',
        'Separation', 'SOE', 'lngdp']
pre = [18.4, 27.6, 14.2, 12.8, 8.9, 11.7, 9.4, 7.2, 6.1, 16.8, 13.5]
post = [2.1, 3.4, 1.8, 2.6, 1.2, 2.3, 1.5, 0.9, 1.1, 2.8, 1.9]

fig, ax = plt.subplots(figsize=(9.0, 4.9), dpi=200)
y = range(len(covs))
ax.scatter(pre, y, marker='o', s=52, facecolors='none', edgecolors='#1f4e79',
           linewidths=1.6, label='Pre-match')
ax.scatter(post, y, marker='x', s=52, c='#c0504d', linewidths=2.0, label='Post-match')
ax.axvline(0, color='#444444', linewidth=1.0)
ax.axvline(10, color='#888888', linewidth=0.9, linestyle='--')
ax.set_yticks(list(y)); ax.set_yticklabels(covs, fontsize=9.5)
ax.invert_yaxis()
ax.set_xlabel('Standardized mean difference (%)', fontsize=10)
ax.legend(frameon=False, fontsize=9.5, loc='lower right')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', labelsize=9.5)
plt.tight_layout(pad=0.5)
plt.savefig(os.path.join(SCRATCH, 'fig_psm.png'), bbox_inches='tight',
            facecolor='white')
plt.close()
print('figures written')
