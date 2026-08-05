#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 7 步：论文级配图。配色沿用稿件蓝色系，黑白打印下靠明度与填充图案冗余编码。"""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'results.json'), encoding='utf-8'))
OUT = os.path.join(HERE, 'figs')
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    'font.sans-serif': ['WenQuanYi Zen Hei'],
    'axes.unicode_minus': False,
    'font.size': 10.5,
    'axes.labelsize': 11,
    'axes.titlesize': 11.5,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.edgecolor': '#333333',
    'axes.linewidth': 0.9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.facecolor': 'white',
})

DEEP = '#1B4C9C'
MID = '#2B6CD4'
LIGHT = '#9DC2F0'
PALE = '#D6E6FA'
GREY = '#8A93A0'


def despine(ax, keep=('left', 'bottom')):
    for s in ('top', 'right', 'left', 'bottom'):
        ax.spines[s].set_visible(s in keep)


# ============================================================ 图 A 治理提效
def fig_efficiency():
    eff = R['efficiency']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.0),
                                   gridspec_kw={'width_ratios': [1.35, 1]})

    labels = [e['环节'] for e in eff]
    y = range(len(labels))
    before = [e['before_min'] for e in eff]
    after = [e['after_min'] for e in eff]

    h = 0.34
    ax1.barh([i + h / 2 for i in y], before, height=h, color=GREY,
             edgecolor='#5A6270', linewidth=0.6, label='数字化前（人工）')
    ax1.barh([i - h / 2 for i in y], after, height=h, color=MID,
             edgecolor=DEEP, linewidth=0.6, hatch='///', label='数字化后')
    for i, (b, a) in enumerate(zip(before, after)):
        ax1.text(b * 1.06, i + h / 2, f'{b:,} 分钟', va='center', fontsize=8.5, color='#333333')
        ax1.text(a * 1.30, i - h / 2, f'{a} 分钟', va='center', fontsize=8.5, color=DEEP)
    ax1.set_xscale('log')
    ax1.set_xlim(10, 6000)
    ax1.set_yticks(list(y))
    ax1.set_yticklabels(labels)
    ax1.set_xlabel('单次业务处理时耗（分钟，对数刻度）')
    ax1.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f'{int(v):,}'))
    ax1.legend(frameon=False, fontsize=8.5, loc='lower right')
    ax1.grid(axis='x', color='#E3E7EC', linewidth=0.6)
    ax1.set_axisbelow(True)
    despine(ax1)
    ax1.set_title('（a）时耗对比', loc='left', color=DEEP)

    comp = [e['压缩率'] * 100 for e in eff]
    bars = ax2.bar(range(len(labels)), comp, width=0.46, color=DEEP,
                   edgecolor=DEEP, linewidth=0.6)
    for i, (bar, e) in enumerate(zip(bars, eff)):
        ax2.text(bar.get_x() + bar.get_width() / 2, e['压缩率'] * 100 + 2.2,
                 f'{e["压缩率"]*100:.1f}%\n（提升 {e["提升倍数"]:.0f} 倍）',
                 ha='center', va='bottom', fontsize=8.5, color=DEEP, linespacing=1.35)
    avg = R['efficiency_avg_compression'] * 100
    ax2.axhline(avg, color=LIGHT, linestyle='--', linewidth=1.1, zorder=0)
    ax2.text(0.5, avg - 9.5, f'两环节均值 {avg:.1f}%', ha='center',
             fontsize=8.5, color=GREY)
    ax2.set_xticks(range(len(labels)))
    ax2.set_xticklabels(['特征提炼', '风险研判'])
    ax2.set_ylim(0, 132)
    ax2.set_yticks([0, 25, 50, 75, 100])
    ax2.set_ylabel('时耗压缩率（%）')
    ax2.grid(axis='y', color='#E3E7EC', linewidth=0.6)
    ax2.set_axisbelow(True)
    despine(ax2)
    ax2.set_title('（b）压缩幅度', loc='left', color=DEEP)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'A_efficiency.png'))
    plt.close(fig)
    print('A_efficiency.png')


# ============================================================ 图 B 人才规模
def fig_headcount():
    hc = R['headcount']
    pts = hc['points']
    labels = [f'{p["阶段"]}\n（{p["年份提示"]}）' for p in pts]
    vals = [p['人数'] for p in pts]
    rd = [v * hc['rd_share'] for v in vals]

    fig, ax = plt.subplots(figsize=(5.6, 3.1))
    x = range(len(vals))
    ax.bar(x, vals, width=0.5, color=PALE, edgecolor=DEEP, linewidth=0.8,
           label='员工总数')
    ax.bar(x, rd, width=0.5, color=MID, edgecolor=DEEP, linewidth=0.8,
           hatch='///', label='研发技术人员（按 60% 下界估算）')
    for i, (v, r) in enumerate(zip(vals, rd)):
        ax.text(i, v + 3.5, f'{v} 人', ha='center', fontsize=9.5, color=DEEP)
        ax.text(i, r / 2, f'≈{r:.0f}', ha='center', va='center',
                fontsize=8.5, color='white')
    # 阶段增幅标注
    for i, g in enumerate([hc['growth_p1'], hc['growth_p2']]):
        ytop = 148
        ax.annotate('', xy=(i + 1 - 0.18, ytop), xytext=(i + 0.18, ytop),
                    arrowprops=dict(arrowstyle='->', color=GREY, lw=1.0))
        ax.text(i + 0.5, ytop + 2.5, f'+{g*100:.0f}%', ha='center',
                fontsize=8.5, color=GREY)
    ax.set_ylim(0, 168)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel('人数')
    ax.legend(frameon=False, fontsize=8.5, loc='upper left', bbox_to_anchor=(0.0, 0.86))
    ax.grid(axis='y', color='#E3E7EC', linewidth=0.6)
    ax.set_axisbelow(True)
    despine(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'B_headcount.png'))
    plt.close(fig)
    print('B_headcount.png')


# ============================================================ 图 C 资质进阶
def fig_qualification():
    q = R['qualification']
    years = [x['年份'] for x in q]
    cum = [x['累计'] for x in q]
    new = [x['当期新增'] for x in q]

    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.bar(years, new, width=0.42, color=PALE, edgecolor=DEEP, linewidth=0.8,
           label='当期新增资质数')
    ax.plot(years, cum, marker='o', markersize=6, color=DEEP, linewidth=1.8,
            markerfacecolor='white', markeredgewidth=1.6, label='累计资质数')
    for xx, c in zip(years, cum):
        ax.text(xx, c + 0.42, f'{c}', ha='center', fontsize=9.5, color=DEEP)
    for xx, x0 in zip(years, q):
        ax.text(xx, -1.55, x0['阶段'], ha='center', fontsize=8.5, color=DEEP)
        ax.text(xx, -2.45, x0['能力维度'], ha='center', fontsize=8, color=GREY)
    ax.set_ylim(-2.9, 11.2)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years])
    ax.set_ylabel('资质数量（项）')
    ax.set_yticks([0, 2, 4, 6, 8, 10])
    ax.legend(frameon=False, fontsize=8.5, loc='upper left', bbox_to_anchor=(0.0, 0.86))
    ax.grid(axis='y', color='#E3E7EC', linewidth=0.6)
    ax.set_axisbelow(True)
    despine(ax)
    ax.spines['bottom'].set_position(('data', 0))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'C_qualification.png'))
    plt.close(fig)
    print('C_qualification.png')


# ============================================================ 图 D 产品结构
def fig_structure():
    s = R['solutions']
    order = ['民生服务', '产业赋能', '治理效能']
    counts = [s['by_attribute'].get(k, 0) for k in order]
    total = sum(counts)
    colors = [DEEP, MID, LIGHT]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0),
                                   gridspec_kw={'width_ratios': [1, 1.25]})

    wedges, _ = ax1.pie(counts, colors=colors, startangle=90,
                        wedgeprops=dict(width=0.42, edgecolor='white', linewidth=1.6))
    ax1.text(0, 0.08, f'{total}', ha='center', va='center', fontsize=17,
             color=DEEP, weight='bold')
    ax1.text(0, -0.24, '个垂直领域', ha='center', va='center', fontsize=9, color=GREY)
    ax1.legend(wedges, [f'{k}  {v} 个（{v/total:.0%}）' for k, v in zip(order, counts)],
               frameon=False, fontsize=8.5, loc='center left', bbox_to_anchor=(-0.18, -0.14))
    ax1.set_title('（a）垂直领域价值属性构成', loc='left', color=DEEP)

    doms = list(reversed(s['domains']))
    domains = [d['领域'] for d in doms]
    attrs = [d['属性'] for d in doms]
    cmap = dict(zip(order, colors))
    hatches = {'民生服务': '', '产业赋能': '///', '治理效能': '...'}
    yy = range(len(domains))
    ax2.barh(list(yy), [1] * len(domains),
             color=[cmap[a] for a in attrs], edgecolor='white', linewidth=1.2,
             hatch='')
    for i, (d, a) in enumerate(zip(domains, attrs)):
        ax2.text(0.035, i, d, va='center', fontsize=9.5,
                 color='white' if a != '治理效能' else DEEP)
        ax2.text(0.97, i, a, va='center', ha='right', fontsize=8.5,
                 color='white' if a != '治理效能' else DEEP)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.62, len(domains) - 0.38)
    ax2.set_xticks([])
    ax2.set_yticks([])
    despine(ax2, keep=())
    ax2.set_title('（b）六大垂直解决方案领域', loc='left', color=DEEP)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'D_structure.png'))
    plt.close(fig)
    print('D_structure.png')


fig_efficiency()
fig_headcount()
fig_qualification()
fig_structure()
print('全部图已输出至', OUT)
