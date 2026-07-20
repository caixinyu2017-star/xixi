# -*- coding: utf-8 -*-
"""Figure 1 — CONSORT participant flow diagram."""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p4_stats.json')))
F = S['flow']; R = S['retention']

plt.rcParams.update({'font.size': 7.8, 'font.family': 'DejaVu Sans'})
INK = '#0b0b0b'; MUT = '#52514e'; EDGE = '#b9b7ae'
BLUE = '#2a78d6'; LBLUE = '#e3eefb'; GRAY = '#f0efe9'

fig, ax = plt.subplots(figsize=(7.0, 6.6))
ax.set_xlim(0, 100); ax.set_ylim(0, 134); ax.axis('off')

def box(x, y, w, lines, fc=GRAY, ec=EDGE, fs=7.6):
    h = 4.1 * len(lines) + 2.6
    ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle='round,pad=0.5,rounding_size=1.2',
                                fc=fc, ec=ec, lw=1.1))
    cy = y - 3.2
    for i, ln in enumerate(lines):
        ax.text(x + w / 2, cy, ln, ha='center', va='center', fontsize=fs,
                fontweight='bold' if i == 0 else 'normal',
                color=INK if i == 0 else MUT)
        cy -= 4.1
    return y - h            # bottom

def arr(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=10,
                                 lw=1.1, color=MUT, shrinkA=1, shrinkB=1))

CX, CW = 14, 40             # center column (upper part)
b1 = box(CX, 133, CW, [f"Assessed for eligibility (n = {F['screened']})"], fc=LBLUE, ec=BLUE)
b2 = box(CX, b1 - 6, CW, [f"Completed baseline (n = {F['baseline']})"], fc=LBLUE, ec=BLUE)
b3 = box(CX, b2 - 6, CW, [f"Randomized (n = {F['randomized']})"], fc=LBLUE, ec=BLUE)
arr(CX + CW / 2, b1, CX + CW / 2, b1 - 6)
arr(CX + CW / 2, b2, CX + CW / 2, b2 - 6)

mid1 = b1 - 3
box(58, mid1 + 7.5, 40, ['Excluded (n = 203)',
                         f"ineligible {F['ineligible']}; declined {F['declined']};",
                         f"elevated risk, referred {F['excluded_risk']}"])
arr(CX + CW / 2, mid1, 58, mid1)
mid2 = b2 - 3
box(58, mid2 + 4.5, 40, [f"Not randomized (n = {F['not_randomized']})",
                         'incomplete baseline or unreachable'])
arr(CX + CW / 2, mid2, 58, mid2)

# allocation columns
LX, RX, W2 = 3, 53, 44
top_alloc = b3 - 5
a1 = box(LX, top_alloc, W2, [f"CareerMate arm (n = {F['n_int']})",
                             '4-week LLM career-companion program',
                             'plus digital career resources'], fc=LBLUE, ec=BLUE)
a2 = box(RX, top_alloc, W2, [f"Waitlist control (n = {F['n_ctl']})",
                             'Digital career-resources handbook;',
                             'chatbot offered after week 8'], fc=LBLUE, ec=BLUE)
arr(CX + 12, b3, LX + W2 / 2, top_alloc)
arr(CX + 28, b3, RX + W2 / 2, top_alloc)

li1 = F['n_int'] - R['t1_int']; lc1 = F['n_ctl'] - R['t1_ctl']
p1 = box(LX, a1 - 5, W2, [f"Week-4 assessment (n = {R['t1_int']})",
                          f"Lost to follow-up (n = {li1}):",
                          'time constraints, unreachable'])
p2 = box(RX, a2 - 5, W2, [f"Week-4 assessment (n = {R['t1_ctl']})",
                          f"Lost to follow-up (n = {lc1}):",
                          'time constraints, unreachable'])
arr(LX + W2 / 2, a1, LX + W2 / 2, a1 - 5)
arr(RX + W2 / 2, a2, RX + W2 / 2, a2 - 5)

li2 = R['t1_int'] - R['t2_int']; lc2 = R['t1_ctl'] - R['t2_ctl']
f1 = box(LX, p1 - 5, W2, [f"Week-8 follow-up (n = {R['t2_int']})",
                          f"Additional loss (n = {li2}):",
                          'started employment, unreachable'])
f2 = box(RX, p2 - 5, W2, [f"Week-8 follow-up (n = {R['t2_ctl']})",
                          f"Additional loss (n = {lc2}):",
                          'started employment, unreachable'])
arr(LX + W2 / 2, p1, LX + W2 / 2, p1 - 5)
arr(RX + W2 / 2, p2, RX + W2 / 2, p2 - 5)

n1 = box(LX, f1 - 5, W2, [f"Analyzed, intention-to-treat (n = {F['n_int']})",
                          'Linear mixed models,',
                          'all available observations'], fc='#eceafd', ec='#4a3aa7')
n2 = box(RX, f2 - 5, W2, [f"Analyzed, intention-to-treat (n = {F['n_ctl']})",
                          'Linear mixed models,',
                          'all available observations'], fc='#eceafd', ec='#4a3aa7')
arr(LX + W2 / 2, f1, LX + W2 / 2, f1 - 5)
arr(RX + W2 / 2, f2, RX + W2 / 2, f2 - 5)

fig.savefig('p4_fig1.png', dpi=300, bbox_inches='tight')
print('p4_fig1.png written, bottom at', min(n1, n2))
