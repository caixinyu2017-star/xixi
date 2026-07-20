# -*- coding: utf-8 -*-
"""Figure 1 — study/analysis pipeline diagram (matplotlib, journal-clean)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({'font.size': 8.0, 'font.family': 'DejaVu Sans'})

INK = '#0b0b0b'; MUT = '#52514e'
BLUE = '#2a78d6'; LBLUE = '#e3eefb'
GRAY = '#f0efe9'; EDGE = '#b9b7ae'
GREEN = '#eaf6f0'; GEDGE = '#1baf7a'
VIOL = '#eceafd'; VEDGE = '#4a3aa7'

fig, ax = plt.subplots(figsize=(7.1, 5.1))
ax.set_xlim(0, 100); ax.set_ylim(0, 106); ax.axis('off')

def box(x, y, w, h, title_lines, lines, fc=GRAY, ec=EDGE, tc=INK, title_fs=8.0, fs=7.1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.6,rounding_size=1.6',
                                fc=fc, ec=ec, lw=1.1))
    if isinstance(title_lines, str):
        title_lines = [title_lines]
    cy = y + h - 2.8
    for tl in title_lines:
        ax.text(x + w / 2, cy, tl, ha='center', va='center', fontsize=title_fs,
                fontweight='bold', color=tc)
        cy -= 3.9
    for ln in lines:
        ax.text(x + w / 2, cy, ln, ha='center', va='center', fontsize=fs, color=MUT)
        cy -= 3.9

def arrow(x1, y1, x2, y2, color=MUT):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                                 mutation_scale=11, lw=1.2, color=color,
                                 shrinkA=1, shrinkB=1))

# Row 1 — survey
box(27, 95, 46, 10, 'Cross-sectional online survey',
    ['N = 947 young adults (18–29), Zhejiang, China'], fc=LBLUE, ec=BLUE)

# Row 2 — two data streams
box(4, 77, 44, 13.5, 'Open-ended career narratives',
    ['3 prompts: situation and difficulties; feelings;', 'future and support needs (Mdn 155 characters)'],
    fc=GREEN, ec=GEDGE)
box(54, 77, 42, 13.5, 'Validated closed-ended scales',
    ['CDS · CAAS-SF · GAD-7 · PHQ-8', 'perceived employability · SWLS'], fc=LBLUE, ec=BLUE)
arrow(43, 95, 30, 91.2)
arrow(57, 95, 71, 91.2)

# de-identification bar
box(4, 68, 44, 6.2, 'De-identification and preprocessing', [], fc='#ffffff', ec=EDGE)
arrow(26, 77, 26, 74.9)

# Row 3 — three AI/coding branches
box(2, 42, 31, 20.5, 'LLM zero-shot ratings',
    ['GPT-4o + Qwen2.5-72B,', '3 runs each, temperature 0;', 'distress, anxiety, and', 'career confidence (1–10)'],
    fc=VIOL, ec=VEDGE)
box(35.5, 42, 31, 20.5, 'Semantic clustering',
    ['BGE-M3 embeddings →', 'UMAP → k-means', '(k = 6 by silhouette) →', 'researcher-refined themes'],
    fc=VIOL, ec=VEDGE)
box(69, 42, 29, 20.5, 'Human expert coding',
    ['n = 200 stratified subsample,', '2 trained raters;', 'distress rubric and', 'theme validation'],
    fc=VIOL, ec=VEDGE)
arrow(15, 68, 15, 63.2)
arrow(32, 68, 49, 63.2)
arrow(46, 68, 81, 63.2)

# Row 4 — validation band with four mini-panels
ax.add_patch(FancyBboxPatch((2, 10.5), 96, 25, boxstyle='round,pad=0.6,rounding_size=1.6',
                            fc='#fbfbf9', ec=EDGE, lw=1.0, ls=(0, (4, 2))))
box(4.5, 12.5, 21.5, 17.5, 'Reliability', 
    ['run-level and', 'between-model ICCs;', 'human-rater ICCs'], fc=GRAY, ec=EDGE)
box(28.5, 12.5, 21.5, 17.5, ['Convergent and', 'discriminant', 'validity'],
    ['multitrait correlation', 'pattern (BH-FDR)'], fc=GRAY, ec=EDGE, title_fs=7.6, fs=6.9)
box(52.5, 12.5, 21.5, 17.5, 'Incremental validity',
    ['hierarchical ΔR²;', 'ROC/AUC comparison', '(DeLong test)'], fc=GRAY, ec=EDGE)
box(76.5, 12.5, 19, 17.5, 'Theme profiles',
    ['prevalence; χ² by', 'status; ANOVA on', 'adjustment outcomes'], fc=GRAY, ec=EDGE, fs=6.9)
arrow(17.5, 42, 17.5, 36.2)
arrow(51, 42, 51, 36.2)
arrow(83.5, 42, 83.5, 36.2)

ax.text(50, 5.0, 'Closed-ended scale scores serve as validation criteria; inferential tests are '
                 'two-tailed with Benjamini–Hochberg false-discovery-rate control where applicable.',
        ha='center', fontsize=6.8, color=MUT, style='italic')

fig.savefig('p3_fig1.png', dpi=300, bbox_inches='tight')
print('p3_fig1.png written')
