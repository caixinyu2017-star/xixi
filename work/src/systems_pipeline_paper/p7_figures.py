# -*- coding: utf-8 -*-
"""Paper 7 figures. Every plotted value is read from p7_model.json /
p7_traj.json / p7_survey.json so that figures and text cannot disagree."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, 'p7_model.json')))
T = json.load(open(os.path.join(HERE, 'p7_traj.json')))
SV = json.load(open(os.path.join(HERE, 'p7_survey.json')))

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.6,
                     'axes.linewidth': 0.8, 'axes.edgecolor': '#3a3a3a'})
INK, MUT, GRID = '#111111', '#5a5a5a', '#d8d8d8'
BLUE, RED, GREEN, ORANGE, PURPLE = '#2c6fbb', '#c0392b', '#1e8449', '#d68910', '#6c3483'
DPI = 320

# channel / loop palette used in Figure 1
C1C, C2C, C3C = '#1f6fb2', '#7b3fa0', '#d68910'
R1C, R2C, R3C, B1C = '#1e8449', '#c0392b', '#c2185b', '#00695c'
SPINE = '#4d4d4d'


def style(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, color=GRID, lw=0.5, alpha=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=7.8, length=3, color='#7a7a7a')


# ===================================================== Figure 1: causal loops
def fig1():
    W_IN, H_IN = 7.4, 6.0
    XR, YR = 100.0, 86.0
    fig, ax = plt.subplots(figsize=(W_IN, H_IN))
    ax.set_xlim(0, XR); ax.set_ylim(0, YR); ax.axis('off')
    ux = XR / W_IN          # data units per inch, x
    uy = YR / H_IN          # data units per inch, y
    FS = 7.5

    # ------------------------------------------------------------- geometry
    N = {
        'A':    (11, 68, 'Generative-AI\nautomation of\nentry tasks'),
        'H':    (35, 68, 'Entry-level\nhiring'),
        'J':    (56, 68, 'Junior\nstock'),
        'rho':  (76, 68, 'Flow to\nproficiency'),
        'S':    (92, 56, 'Senior\n(proficient)\nstock'),
        'tau':  (76, 53, 'Time to\nproficiency'),
        'Le':   (33, 53, 'Learning\ncontent of\nentry work'),
        'V':    (11, 44, 'Verification\nload'),
        'm':    (56, 39, 'Mentoring\nper junior'),
        'P':    (11, 26, 'Entrant\npool'),
        'Kp':   (33, 26, 'Skill capital\nper entrant'),
        'pres': (76, 26, 'Delivery\npressure'),
        'W':    (92, 26, 'Perceived\nsenior scarcity'),
    }

    def half(key):
        """half-width / half-height of a node box, in data units"""
        _, _, t = N[key]
        lines = t.split('\n')
        w_in = max(len(s) for s in lines) * FS * 0.545 / 72.0
        h_in = len(lines) * FS * 1.32 / 72.0
        return w_in * ux / 2 + 1.25, h_in * uy / 2 + 1.15

    def clip(key, dx, dy):
        """exit point of direction (dx,dy) on the box boundary of `key`"""
        x, y, _ = N[key]
        hw, hh = half(key)
        sx = abs(dx) / hw if dx else 0.0
        sy = abs(dy) / hh if dy else 0.0
        s = max(sx, sy, 1e-9)
        return x + dx / s, y + dy / s

    for key in N:
        x, y, t = N[key]
        fc, ec, lw = '#f6f7f9', '#98a2ad', 0.8
        if key == 'A':
            fc, ec, lw = '#e6eefa', C1C, 1.3
        elif key == 'S':
            fc, ec, lw = '#e7f5ec', R1C, 1.3
        elif key == 'P':
            fc, ec, lw = '#fdecec', R3C, 1.3
        ax.text(x, y, t, ha='center', va='center', fontsize=FS, color=INK,
                zorder=6, linespacing=1.28,
                bbox=dict(boxstyle='round,pad=0.32', fc=fc, ec=ec, lw=lw))

    def edge(a, b, sign, col=SPINE, rad=0.0, ls='-', lw=1.05, tag=None, st=0.5):
        x1, y1, _ = N[a]; x2, y2, _ = N[b]
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        dx, dy = x2 - x1, y2 - y1
        cx, cy = mx + rad * dy, my - rad * dx          # matplotlib arc3 control pt
        p1 = clip(a, cx - x1, cy - y1)                 # tangent at t=0 is C-P0
        p2 = clip(b, cx - x2, cy - y2)                 # tangent at t=1 is C-P2
        ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=9.5,
                                     lw=lw, color=col, linestyle=ls,
                                     connectionstyle=f'arc3,rad={rad}',
                                     shrinkA=0, shrinkB=0, zorder=3))
        # point at parameter st on the quadratic Bezier through p1, C', p2
        cx2 = (p1[0] + p2[0]) / 2.0 + rad * (p2[1] - p1[1])
        cy2 = (p1[1] + p2[1]) / 2.0 - rad * (p2[0] - p1[0])
        w0, w1, w2 = (1 - st) ** 2, 2 * st * (1 - st), st ** 2
        sxp = w0 * p1[0] + w1 * cx2 + w2 * p2[0]
        syp = w0 * p1[1] + w1 * cy2 + w2 * p2[1]
        txt = sign if tag is None else f'{tag}  {sign}'
        ax.text(sxp, syp, txt, fontsize=8.6 if tag is None else 7.2, color=col,
                ha='center', va='center', zorder=7, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.16', fc='white', ec='none'))

    # exogenous channels of the automation shock
    edge('A', 'H',  '−', C1C, lw=1.7, tag='C1')
    edge('A', 'Le', '−', C2C, lw=1.7, tag='C2')
    edge('A', 'V',  '+',      C3C, lw=1.7, tag='C3')
    edge('Le', 'tau', '−', C2C, lw=1.3, st=0.28)
    edge('V', 'pres', '+',      C3C, lw=1.3)
    # shared pipeline spine
    edge('H', 'J', '+')
    edge('J', 'rho', '+')
    edge('rho', 'S', '+')
    edge('tau', 'rho', '−')
    edge('m', 'tau', '−')
    # R1 mentoring-budget dilution
    edge('S', 'm', '+', R1C, rad=-0.12, lw=1.3, tag='R1')
    # R2 delivery-pressure crowd-out
    edge('S', 'pres', '−', R2C, lw=1.3, tag='R2')
    edge('pres', 'm', '−', R2C, lw=1.3)
    # R3 entrant-pool scarring
    edge('rho', 'H', '+', R3C, rad=0.42, lw=1.3)
    edge('H', 'P', '−', R3C, rad=0.22, lw=1.3)
    edge('P', 'Kp', '−', R3C, lw=1.3, tag='R3')
    edge('Kp', 'tau', '−', R3C, rad=-0.35, lw=1.3)
    # B1 delayed scarcity correction
    edge('S', 'W', '−', B1C, lw=1.3, tag='B1')
    edge('W', 'H', '+', B1C, rad=0.20, lw=1.3, ls=(0, (5, 2.4)), st=0.72)

    # ------------------------------------------------------------- legend
    ax.text(3, 15.0, 'Exogenous channels of the automation shock',
            fontsize=7.0, fontweight='bold', color=INK, ha='left')
    for i, (c, s) in enumerate((
            (C1C, 'C1  substitution of AI for entry-level labour  (φ)'),
            (C2C, 'C2  displacement of learning-bearing practice, net of\n'
                  '        AI-as-tutor support  (θ, λ)'),
            (C3C, 'C3  verification load on senior time  (ν)'))):
        ax.text(3, 11.4 - 3.6 * i, s, fontsize=6.4, color=c, ha='left',
                va='top', linespacing=1.35)
    ax.text(52, 15.0, 'Endogenous feedback loops', fontsize=7.0,
            fontweight='bold', color=INK, ha='left')
    for i, (c, s) in enumerate((
            (R1C, 'R1  mentoring-budget dilution  (reinforcing)'),
            (R2C, 'R2  delivery-pressure crowd-out  (reinforcing)'),
            (R3C, 'R3  entrant-pool scarring  (reinforcing)'),
            (B1C, 'B1  delayed scarcity correction  (balancing; dashed = long delay)'))):
        ax.text(52, 11.4 - 2.6 * i, s, fontsize=6.4, color=c, ha='left', va='top')

    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    fig.savefig(os.path.join(HERE, 'p7_fig1.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ================================================ Figure 2: stock-flow map
def fig2():
    fig, ax = plt.subplots(figsize=(7.4, 4.7))
    ax.set_xlim(0, 100); ax.set_ylim(0, 64); ax.axis('off')

    def stock(x, y, w, h, label, sub, fc):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle='square,pad=0', fc=fc, ec=INK,
                                    lw=1.1, zorder=4))
        ax.text(x, y + 1.9, label, ha='center', va='center', fontsize=8.4,
                fontweight='bold', zorder=5)
        ax.text(x, y - 2.6, sub, ha='center', va='center', fontsize=6.3,
                color=MUT, zorder=5)

    def valve(x, y):
        ax.add_patch(Circle((x, y), 2.0, fc='white', ec='#4a6fa5', lw=1.2, zorder=6))
        ax.plot([x - 0.95, x + 0.95], [y + 0.6, y + 0.6], color='#4a6fa5',
                lw=1.0, zorder=7)
        ax.plot([x - 0.95, x + 0.95], [y - 0.6, y - 0.6], color='#4a6fa5',
                lw=1.0, zorder=7)

    def pipe(x1, x2, y, lw=2.4, col='#4a6fa5'):
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='-|>,head_width=0.30,head_length=0.55',
                                    lw=lw, color=col, shrinkA=0, shrinkB=0))

    Y = 45
    stock(25, Y, 21, 10.5, 'Entrant pool  P', 'skill capital Q,  K = Q/P', '#fdecec')
    stock(56, Y, 17, 10.5, 'Juniors  J', 'entry-level staff', '#eaf2fb')
    stock(85, Y, 17, 10.5, 'Seniors  S', 'proficient staff', '#e8f6ee')

    pipe(4.5, 14.0, Y)
    ax.text(6.0, Y + 7.5, 'graduate\ninflow  G', ha='left', va='center',
            fontsize=6.8, linespacing=1.4)
    pipe(35.5, 47.5, Y); valve(41.5, Y)
    ax.text(41.5, Y + 8.2, 'hiring  H', ha='center', fontsize=7.0)
    pipe(64.5, 76.5, Y); valve(70.5, Y)
    ax.text(70.5, Y + 8.2, 'promotion  ρ = J/τ', ha='center', fontsize=7.0)
    pipe(93.5, 99.0, Y)
    ax.text(96.0, Y + 7.5, 'exit\nS/τS', ha='center', va='center',
            fontsize=6.8, linespacing=1.4)

    ax.annotate('', xy=(56, 33.5), xytext=(56, 39.5),
                arrowprops=dict(arrowstyle='-|>,head_width=0.28,head_length=0.52',
                                lw=1.8, color='#8a8a8a'))
    ax.text(59.0, 32.5, 'junior exit  J/τJ', fontsize=6.6, color=MUT,
            ha='left', va='center')
    ax.annotate('', xy=(25, 33.5), xytext=(25, 39.5),
                arrowprops=dict(arrowstyle='-|>,head_width=0.28,head_length=0.52',
                                lw=1.8, color='#8a8a8a'))
    ax.text(23.0, 35.5, 'discouragement  P/τP', fontsize=6.6, color=MUT,
            ha='right', va='center')
    ax.annotate('', xy=(30.0, 38.5), xytext=(53.0, 32.6),
                arrowprops=dict(arrowstyle='-|>,head_width=0.26,head_length=0.5',
                                lw=1.3, color='#8a8a8a',
                                connectionstyle='arc3,rad=0.30',
                                linestyle=(0, (4, 2.2))))
    ax.text(42.5, 29.2, 'returning share  b', fontsize=6.4, color=MUT, ha='center')

    ax.add_patch(FancyBboxPatch((2.5, 4.0), 43.5, 18.0,
                                boxstyle='round,pad=0.6,rounding_size=1.3',
                                fc='#fbfbfc', ec='#b9bec6', lw=0.9))
    ax.text(24.2, 19.3, 'Automation of the entry task bundle', ha='center',
            fontsize=7.3, fontweight='bold')
    ax.text(24.2, 14.2, 'dA/dt = c A (1 − A/Aₘₐₓ)',
            ha='center', fontsize=7.6)
    ax.text(24.2, 8.4, 'desired juniors\nJ* = j₀ D (1 − φA)(1 + w W)',
            ha='center', fontsize=6.9, color=MUT, linespacing=1.5)

    ax.add_patch(FancyBboxPatch((54.0, 4.0), 43.5, 18.0,
                                boxstyle='round,pad=0.6,rounding_size=1.3',
                                fc='#fbfbfc', ec='#b9bec6', lw=0.9))
    ax.text(75.7, 19.3, 'Senior time allocation (strict priority)', ha='center',
            fontsize=7.3, fontweight='bold')
    ax.text(75.7, 15.3,
            'complex work  C/πS   →   verification  ν A R\n'
            '→   residual routine work   →   mentoring  m J',
            ha='center', fontsize=6.8, linespacing=1.5)
    ax.text(75.7, 8.0,
            'mentoring is the residual claimant on the non-delivery\n'
            'budget (1 − u*)S;   τ = τ₀ / (Lm · Le · Lk)',
            ha='center', fontsize=6.5, color=MUT, linespacing=1.5)

    ax.annotate('', xy=(85, 22.8), xytext=(85, 39.5),
                arrowprops=dict(arrowstyle='-|>,head_width=0.24,head_length=0.48',
                                lw=1.1, color='#b6b6b6'))
    ax.annotate('', xy=(62.5, 39.5), xytext=(62.5, 22.8),
                arrowprops=dict(arrowstyle='-|>,head_width=0.24,head_length=0.48',
                                lw=1.1, color='#b6b6b6'))
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    fig.savefig(os.path.join(HERE, 'p7_fig2.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ============================================= Figure 3: reference behaviour
def fig3():
    t = np.array(T['t'])
    fig, axes = plt.subplots(2, 2, figsize=(7.3, 5.0))
    panels = [
        (axes[0, 0], 'S', 'Senior (proficient) stock', 'thousand persons', GREEN),
        (axes[0, 1], 'hire', 'Entry-level hiring', 'thousand persons per year', BLUE),
        (axes[1, 0], 'Y', 'Productive capacity of the system',
         'thousand task units per year', ORANGE),
        (axes[1, 1], 'tau', 'Time to proficiency', 'years', RED),
    ]
    for ax, key, title, ylab, col in panels:
        cf = np.array(T[f'cf_{key}']); bs = np.array(T[f'base_{key}'])
        ax.plot(t, cf, color='#7a7a7a', lw=1.5, ls='--',
                label='No-automation counterfactual')
        ax.plot(t, bs, color=col, lw=2.0, label='Automation baseline')
        ax.fill_between(t, cf, bs, color=col, alpha=0.10)
        ax.set_title(title, fontsize=8.4, pad=4)
        ax.set_ylabel(ylab, fontsize=7.2)
        ax.set_xlabel('year', fontsize=7.2)
        ax.set_xlim(0, t[-1])
        style(ax)
    cr = M['key_results'].get('output_crossover_year')
    if cr:
        axes[1, 0].axvline(cr, color=INK, lw=0.9, ls=':')
        axes[1, 0].annotate(f'capacity crossover\nyear {cr:.1f}',
                            xy=(cr, np.array(T['base_Y'])[-1]),
                            xytext=(cr + 1.2, min(T['base_Y']) * 1.0),
                            fontsize=6.4, color=INK,
                            arrowprops=dict(arrowstyle='-', lw=0.7, color=INK))
    axes[0, 0].legend(fontsize=6.8, frameon=False, loc='lower left')
    ax2 = axes[0, 1].twinx()
    ax2.plot(t, np.array(T['base_A']), color='#9aa5b1', lw=1.1, ls='-.')
    ax2.set_ylabel('automation depth A', fontsize=6.6, color='#7a7a7a')
    ax2.tick_params(labelsize=6.6, colors='#7a7a7a')
    ax2.spines['top'].set_visible(False)
    fig.tight_layout(pad=0.6, w_pad=1.8, h_pad=1.4)
    fig.savefig(os.path.join(HERE, 'p7_fig3.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ================================================== Figure 4: tipping analysis
def fig4():
    sw = M['sweep']
    A = np.array([r['A_max'] for r in sw])
    S = np.array([r['S_rel'] for r in sw])
    Y = np.array([r['Y_rel'] for r in sw])
    mr = np.array([r['ment_ratio'] for r in sw])
    q = np.array([r['q30'] for r in sw])
    tp = M['tipping']

    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.0))
    ax = axes[0]
    ax.plot(A, S, color=GREEN, lw=2.0, label='Senior stock')
    ax.plot(A, Y, color=ORANGE, lw=2.0, label='Productive capacity')
    ax.axhline(0, color=INK, lw=0.8)
    for key, lab, col in (('A_training_collapse', 'training\ncrowd-out', RED),
                          ('A_verification_binds', 'verification\nbottleneck', PURPLE)):
        v = tp.get(key)
        if v:
            ax.axvline(v, color=col, lw=1.0, ls='--')
            y0 = ax.get_ylim()[0]
            side = -1 if key == 'A_training_collapse' else 1
            ax.text(v + 0.012 * side, y0 * 0.98, f'{lab}\nA = {v:.2f}',
                    fontsize=6.2, color=col, va='bottom',
                    ha='right' if side < 0 else 'left')
    ax.set_xlabel('asymptotic automation depth of the entry task bundle  A$_{max}$',
                  fontsize=7.4)
    ax.set_ylabel('deviation at year 30 (%)', fontsize=7.4)
    ax.set_title('Response of the system to automation depth', fontsize=8.4, pad=4)
    ax.legend(fontsize=6.8, frameon=False, loc='lower left')
    style(ax)

    ax = axes[1]
    ax.plot(A, mr, color=RED, lw=2.0, label='Mentoring per junior (ratio to reference)')
    ax.plot(A, q, color=PURPLE, lw=2.0, label='Verifiable share of AI output')
    ax.set_ylim(-0.03, 1.08)
    ax.set_xlabel('asymptotic automation depth  A$_{max}$', fontsize=7.4)
    ax.set_ylabel('ratio at year 30', fontsize=7.4)
    ax.set_title('Two successive regime shifts', fontsize=8.4, pad=4)
    ax.legend(fontsize=6.6, frameon=False, loc='lower left')
    style(ax)
    fig.tight_layout(pad=0.5, w_pad=2.0)
    fig.savefig(os.path.join(HERE, 'p7_fig4.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ==================================================== Figure 5: policy design
def fig5():
    t = np.array(T['t'])
    pol = M['policies']
    rob = M['policy_robustness']
    tags = ['P1', 'P2', 'P3', 'P4', 'P5']
    cols = {'P1': BLUE, 'P2': ORANGE, 'P3': GREEN, 'P4': PURPLE, 'P5': INK}

    fig = plt.figure(figsize=(7.3, 5.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.92], hspace=0.52, wspace=0.34)

    ax = fig.add_subplot(gs[0, :])
    ax.plot(t, np.array(T['cf_S']), color='#7a7a7a', lw=1.4, ls='--',
            label='No-automation counterfactual')
    ax.plot(t, np.array(T['base_S']), color=RED, lw=2.1, label='Automation baseline')
    for tg in tags:
        ax.plot(t, np.array(T[f'{tg}_S']), color=cols[tg], lw=1.5,
                label=f"{tg}  {pol[tg]['name']}")
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo - (hi - lo) * 0.14, hi)
    ax.axvline(M['policy_start_year'], color='#b0b0b0', lw=0.9, ls=':')
    ax.text(M['policy_start_year'] - 0.5, lo + (hi - lo) * 0.42,
            'policies begin', fontsize=6.4, color=MUT, va='center',
            ha='center', rotation=90)
    ax.set_xlabel('year', fontsize=7.4)
    ax.set_ylabel('senior stock (thousand persons)', fontsize=7.4)
    ax.set_title('Policy trajectories for the stock of proficient professionals',
                 fontsize=8.6, pad=4)
    ax.set_xlim(0, t[-1])
    ax.legend(fontsize=6.5, frameon=False, ncol=2, loc='lower left',
              bbox_to_anchor=(0.10, -0.015), handlelength=1.8, columnspacing=1.4)
    style(ax)

    ax = fig.add_subplot(gs[1, 0])
    y = np.arange(len(tags))
    means = [rob[tg]['mean'] for tg in tags]
    lo_e = [rob[tg]['mean'] - rob[tg]['p05'] for tg in tags]
    hi_e = [rob[tg]['p95'] - rob[tg]['mean'] for tg in tags]
    ax.barh(y, means, color=[cols[tg] for tg in tags], alpha=0.85, height=0.6)
    ax.errorbar(means, y, xerr=[lo_e, hi_e], fmt='none', ecolor=INK,
                elinewidth=0.9, capsize=2.6)
    xmax = max(m + h for m, h in zip(means, hi_e))
    for i, tg in enumerate(tags):
        ax.text(means[i] + hi_e[i] + xmax * 0.035, y[i], f"{means[i]:+.1f}%",
                va='center', ha='left', fontsize=6.6)
    ax.set_xlim(min(0, min(m - l for m, l in zip(means, lo_e))) - xmax * 0.05,
                xmax * 1.30)
    ax.set_yticks(y); ax.set_yticklabels(tags, fontsize=7.4)
    ax.invert_yaxis()
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_xlabel('senior stock at year 30 vs. baseline (%)\nmean and 5th–95th '
                  'percentile over {:d} parameterisations'.format(rob['P1']['n']),
                  fontsize=6.8)
    ax.set_title('Robustness of each lever', fontsize=8.2, pad=4)
    style(ax)

    ax = fig.add_subplot(gs[1, 1])
    conv = [pol[tg]['conversion'] for tg in ['P0'] + tags]
    lab = ['P0'] + tags
    xs = np.arange(len(lab))
    bars = ax.bar(xs, conv, color=['#8a8a8a'] + [cols[tg] for tg in tags],
                  alpha=0.85, width=0.62)
    ccf = M['key_results']['conversion_cf']
    ax.axhline(ccf, color=GREEN, lw=1.0, ls='--')
    ax.text(-0.48, ccf + 0.010, 'counterfactual', fontsize=6.2,
            color=GREEN, ha='left', va='bottom')
    for b, v in zip(bars, conv):
        ax.text(b.get_x() + b.get_width() / 2, v - 0.018, f'{v:.3f}',
                ha='center', va='top', fontsize=6.4, color='white',
                fontweight='bold')
    ax.set_xticks(xs); ax.set_xticklabels(lab, fontsize=7.4)
    ax.set_ylabel('promotions per entry hire', fontsize=7.2)
    ax.set_ylim(0, max(max(conv), ccf) * 1.16)
    ax.set_title('Conversion efficiency of the pipeline', fontsize=8.2, pad=4)
    style(ax)
    fig.savefig(os.path.join(HERE, 'p7_fig5.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ============================================= Figure 6: sensitivity analysis
def fig6():
    sen = M['sensitivity']
    pr = sen['prcc_senior']
    lbl = {'phi': 'φ  AI–junior substitutability',
           'A_max': 'A$_{max}$  automation depth',
           'theta': 'θ  practice displacement',
           'lam': 'λ  AI-as-tutor effect',
           'tau0': 'τ₀  reference proficiency time',
           'g': 'g  demand growth',
           'c_diff': 'c  diffusion speed',
           'w_sens': 'w  scarcity response',
           'tauS': 'τₛ  senior exit time',
           'mstar': 'm*  reference mentoring',
           'sigma': 'σ  complex-work share',
           'ustar': 'u*  utilisation norm',
           'nu': 'ν  verification load',
           'a_ment': 'a  mentoring elasticity',
           'delta': 'δ  pool skill decay'}
    items = sorted(pr.items(), key=lambda kv: abs(kv[1]['prcc']), reverse=True)
    keys = [k for k, _ in items]
    vals = [v['prcc'] for _, v in items]
    sig = [v['p'] < 0.05 for _, v in items]

    fig, axes = plt.subplots(1, 2, figsize=(7.3, 3.5),
                             gridspec_kw={'width_ratios': [1.22, 1.0]})
    ax = axes[0]
    y = np.arange(len(keys))
    bars = ax.barh(y, vals, color=[(GREEN if v > 0 else RED) for v in vals],
                   height=0.66)
    for b, s_ in zip(bars, sig):
        b.set_alpha(0.92 if s_ else 0.30)
    ax.set_yticks(y)
    ax.set_yticklabels([lbl.get(k, k) for k in keys], fontsize=6.9)
    ax.invert_yaxis()
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_xlabel('partial rank correlation coefficient (PRCC)', fontsize=7.2)
    ax.set_title('Global sensitivity (%d Latin-hypercube runs)' % sen['n_runs'],
                 fontsize=8.3, pad=4)
    style(ax)

    ax = axes[1]
    sg, og = sen['senior_gap'], sen['output_gap']
    for i, (d, col) in enumerate(((sg, GREEN), (og, ORANGE))):
        ax.barh(i, d['p95'] - d['p05'], left=d['p05'], height=0.30, color=col,
                alpha=0.28)
        ax.plot([d['p05'], d['p95']], [i, i], color=col, lw=1.4)
        ax.plot([d['p50']], [i], 'o', color=col, ms=6)
        ax.text(d['p50'], i + 0.26, f"median {d['p50']:.1f}%", ha='center',
                fontsize=6.7, color=col)
        ax.text((d['p05'] + d['p95']) / 2, i - 0.24,
                f"P5 {d['p05']:.1f}%    P95 {d['p95']:.1f}%", ha='center',
                fontsize=6.1, color=MUT)
        ax.text((d['p05'] + d['p95']) / 2, i - 0.46,
                f"{100 * d['share_negative']:.1f}% of runs negative",
                fontsize=6.3, color=col, ha='center')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Senior\nstock', 'Productive\ncapacity'], fontsize=7.2)
    ax.set_ylim(-0.75, 1.55)
    ax.axvline(0, color=INK, lw=0.9)
    ax.set_xlabel('deviation from the no-automation\ncounterfactual at year 30 (%)',
                  fontsize=7.2)
    ax.set_title('Distribution of outcomes', fontsize=8.3, pad=4)
    style(ax)
    fig.tight_layout(pad=0.5, w_pad=2.4)
    fig.savefig(os.path.join(HERE, 'p7_fig6.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


# ================================ Figure 7: Study 1 marginal learning effect
def fig7():
    d = SV['model_D']
    nl = SV['net_learning_effect']
    b_ata = d['b'][2]; b_int = d['b'][3]
    sal = np.linspace(0.05, 0.95, 120)
    eff = b_ata + b_int * sal
    se_a, se_i = d['se'][2], d['se'][3]
    approx_se = np.sqrt(se_a ** 2 + (sal ** 2) * se_i ** 2
                        - 2 * sal * 0.80 * se_a * se_i)
    fig, ax = plt.subplots(figsize=(4.9, 3.2))
    ax.plot(sal, eff, color=BLUE, lw=2.0)
    ax.fill_between(sal, eff - 1.96 * approx_se, eff + 1.96 * approx_se,
                    color=BLUE, alpha=0.15)
    ax.axhline(0, color=INK, lw=0.9)
    for key, pos, tg in (('at_p25', nl['sal_p25'], 'P25'),
                         ('at_p75', nl['sal_p75'], 'P75'),
                         ('at_p95', nl['sal_p95'], 'P95')):
        e = nl[key]['estimate']
        ax.errorbar([pos], [e], yerr=[1.96 * nl[key]['se']], fmt='o', ms=4.6,
                    color=RED, ecolor=RED, elinewidth=1.0, capsize=2.6, zorder=5)
        ax.text(pos, e + 1.96 * nl[key]['se'] + 0.022, tg, ha='center',
                fontsize=6.5, color=RED)
    nz = nl['neutralising_SAL']
    if 0 < nz < 1:
        ax.axvline(nz, color=GREEN, lw=1.0, ls='--')
        ax.text(nz - 0.02, ax.get_ylim()[1] * 0.86,
                f'neutralising level\nSAL = {nz:.2f}', fontsize=6.4, color=GREEN,
                ha='right')
    ax.set_xlabel('structured AI-assisted learning practice (SAL)', fontsize=7.6)
    ax.set_ylabel('marginal effect of automation depth\non ln(time to independence)',
                  fontsize=7.2)
    ax.set_title('The learning penalty of automation depends on how AI is used',
                 fontsize=8.3, pad=5)
    style(ax)
    fig.tight_layout(pad=0.4)
    fig.savefig(os.path.join(HERE, 'p7_fig7.png'), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6(); fig7()
    print('figures written:', [f'p7_fig{i}.png' for i in range(1, 8)])
