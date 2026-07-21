# -*- coding: utf-8 -*-
"""机制图/框架图（D 型，共 20 幅）。graphviz + matplotlib 手绘，中文出版级。
图名不写入图内（由 Word 排版）；实线=直接作用，虚线=反馈。"""
import json
import os
import subprocess

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Polygon, Rectangle

from figstyle import save, PAL, CJK  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))

FN = 'Noto Sans CJK SC'
C = dict(blue='#1F4E79', ltblue='#DCE6F1', orange='#C55A11', ltorange='#FCE4D6',
         teal='#2E8B8B', ltteal='#D6EAEA', gold='#BF9000', ltgold='#FFF2CC',
         green='#548235', ltgreen='#E2EFDA', red='#A02020', ltred='#F8D7D7',
         gray='#7F7F7F', ltgray='#EDEDED', purple='#674EA7', ltpurple='#E6E0F0')


# ============================ graphviz 通用 ============================
def render(dot, name, engine='dot', dpi=300):
    dot = f'digraph G {{\n  graph [fontname="{FN}", dpi={dpi}];\n' \
          f'  node [fontname="{FN}"];\n  edge [fontname="{FN}"];\n' + dot + '\n}\n'
    p = os.path.join(FIG, name + '.dot')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(dot)
    subprocess.run([engine, '-Tpng', p, '-o', os.path.join(FIG, name + '.png')], check=True)
    os.remove(p)
    print('ok', name)


# ============================ matplotlib 通用 ============================
def canvas(win, hin, W=100, H=70):
    fig, ax = plt.subplots(figsize=(win, hin))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis('off')
    ax.grid(False)
    return fig, ax


def bx(ax, x, y, w, h, text, fc='#DCE6F1', ec=PAL['blue'], fs=8, lw=1.1,
       ls='solid', tc='#1a1a1a', bold=False, pad=0.5):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad={pad}', fc=fc, ec=ec,
                       lw=lw, linestyle=ls, zorder=2)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs, color=tc,
            zorder=4, fontweight='bold' if bold else 'normal', linespacing=1.4)


def arr(ax, p1, p2, c=PAL['gray'], lw=1.3, ls='solid', rad=0.0, ms=12, z=1, style='-|>'):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms, color=c, lw=lw,
                        linestyle=ls, connectionstyle=f'arc3,rad={rad}',
                        shrinkA=1.5, shrinkB=1.5, zorder=z)
    ax.add_patch(a)


def txt(ax, x, y, s, fs=7, c='#333333', ha='center', va='center', bold=False, rot=0, z=4):
    ax.text(x, y, s, fontsize=fs, color=c, ha=ha, va=va, rotation=rot,
            fontweight='bold' if bold else 'normal', linespacing=1.35, zorder=z)


# --------------------------------------------------- 图1.1 研究技术路线（graphviz）
def fig1_1():
    d = f'''
  rankdir=TB; nodesep=0.28; ranksep=0.42; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.14,0.08"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  P [label="现实问题：“双碳”目标与碳排放双控转型、欧盟 CBAM 生效背景下，\\n如何构建国际认可的中国绿色低碳标准体系？", fillcolor="{C['ltorange']}", color="{C['orange']}", fontsize=13.5];
  subgraph cluster_q {{ label="三个科学问题"; style=dashed; color="{C['red']}"; fontcolor="{C['red']}"; fontsize=12;
    Q1 [label="问题一（厘清机制）\\n多元主体如何驱动\\n标准体系形成与演化？", fillcolor="{C['ltred']}", color="{C['red']}"];
    Q2 [label="问题二（设计体系）\\n如何设计“双碳”导向的\\n完善标准体系？", fillcolor="{C['ltred']}", color="{C['red']}"];
    Q3 [label="问题三（评估效果）\\n如何评估贡献度与适配性\\n并反馈优化体系？", fillcolor="{C['ltred']}", color="{C['red']}"]; }}
  subgraph cluster_m1 {{ label="模块一：动态演化机理（第3—7章）"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12;
    M11 [label="典型事实：国际演进与\\n中国时空特征（第3—4章）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    M12 [label="状态空间模型：A/B 矩阵\\n卡尔曼滤波（第5章）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    M13 [label="技术—制度 LV 协同演进\\nα、β 互馈（第6章）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    M14 [label="政府—企业—国际组织\\n演化博弈（第7章）", fillcolor="{C['ltblue']}", color="{C['blue']}"]; }}
  subgraph cluster_m2 {{ label="模块二：体系构建（第8—10章）"; style=dashed; color="{C['teal']}"; fontcolor="{C['teal']}"; fontsize=12;
    M21 [label="SSDMI 供需动态\\n错配识别（第8章）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    M22 [label="总体架构：五大功能模块\\n×四层级（第9章）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    M23 [label="SD 协同效应与动态\\n更新机制（第10章）", fillcolor="{C['ltteal']}", color="{C['teal']}"]; }}
  subgraph cluster_m3 {{ label="模块三：适配性评估（第11—13章）"; style=dashed; color="{C['gold']}"; fontcolor="{C['gold']}"; fontsize=12;
    M31 [label="SFA-PEL 政策适配性\\n评估（第11章）", fillcolor="{C['ltgold']}", color="{C['gold']}"];
    M32 [label="ISGI-CIAI 国际适配性\\n评估（第12章）", fillcolor="{C['ltgold']}", color="{C['gold']}"];
    M33 [label="中外比较与典型行业\\n案例（第13章）", fillcolor="{C['ltgold']}", color="{C['gold']}"]; }}
  CC [label="研究结论与政策建议：供给侧补短板·执行侧强激励·国际侧提话语权（第14章）", fillcolor="{C['ltgreen']}", color="{C['green']}", fontsize=13];
  {{rank=same; Q1; Q2; Q3;}} Q1 -> Q2 -> Q3 [style=invis];
  {{rank=same; M11; M12; M13; M14;}} M11 -> M12 -> M13 -> M14 [style=invis];
  {{rank=same; M21; M22; M23;}} M21 -> M22 -> M23 [style=invis];
  {{rank=same; M31; M32; M33;}} M31 -> M32 -> M33 [style=invis];
  P -> Q1; P -> Q2; P -> Q3;
  Q1 -> M11 [lhead=cluster_m1];
  Q2 -> M22 [lhead=cluster_m2];
  Q3 -> M31 [lhead=cluster_m3];
  M12 -> M23 [label="Â 矩阵→溢出矩阵 Φ", style=dashed, constraint=false];
  M14 -> M22 [label="演化规律→三项构建原则", ltail=cluster_m1, lhead=cluster_m2];
  M23 -> M31 [label="体系方案→评估对象", ltail=cluster_m2, lhead=cluster_m3];
  M31 -> M21 [label="评估结果反馈优化体系", style=dashed, color="{C['red']}", fontcolor="{C['red']}", ltail=cluster_m3, lhead=cluster_m2, constraint=false];
  M33 -> CC [ltail=cluster_m3];
'''
    render(d, 'fig1_1')


# --------------------------------------------------- 图1.2 全书结构（graphviz 树形）
def fig1_2():
    ch = {1: '导论', 2: '理论基础与文献综述', 3: '国际绿色低碳标准化的演进历程与全球格局',
          4: '中国绿色低碳标准体系的演进历程与时空特征', 5: '标准体系动态演化的状态空间模型',
          6: '技术—制度协同演进模型', 7: '标准制定的多主体演化博弈模型',
          8: '标准供需动态错配的识别与测算', 9: '“双碳”目标下标准体系的总体架构',
          10: '标准体系的协同效应与动态更新机制', 11: '政策适配性评估：执行效率与效能损耗',
          12: '国际适配性评估：标准差距与贸易影响', 13: '中外标准体系比较与典型行业案例',
          14: '研究结论、政策建议与研究展望'}
    parts = [('P1', '第一篇  总论\\n（第1—2章）', [1, 2], 'blue'),
             ('P2', '第二篇  动态演化机理\\n（第3—7章）', [3, 4, 5, 6, 7], 'teal'),
             ('P3', '第三篇  体系构建\\n（第8—10章）', [8, 9, 10], 'gold'),
             ('P4', '第四篇  适配性评估与结论\\n（第11—14章）', [11, 12, 13, 14], 'green')]
    lines = ['  rankdir=LR; nodesep=0.12; ranksep=0.65;',
             '  node [shape=box, style="rounded,filled", fontsize=12, margin="0.14,0.07"];',
             f'  edge [color="{C["gray"]}", arrowsize=0.7];',
             f'  ROOT [label="《“双碳”目标下中国绿色低碳\\n标准体系研究》\\n动态演化·体系构建·适配性评估", fillcolor="{C["ltorange"]}", color="{C["orange"]}", fontsize=13.5];']
    for pid, plab, chs, col in parts:
        lines.append(f'  {pid} [label="{plab}", fillcolor="{C["lt" + col]}", color="{C[col]}", fontsize=12.5];')
        lines.append(f'  ROOT -> {pid};')
        for k in chs:
            lines.append(f'  C{k} [label="第{k}章  {ch[k]}", fillcolor="{C["ltgray"]}", color="{C[col]}", fontsize=11];')
            lines.append(f'  {pid} -> C{k};')
    render('\n'.join(lines), 'fig1_2')


# --------------------------------------------------- 图2.1 理论基础与研究框架（graphviz）
def fig2_1():
    d = f'''
  rankdir=TB; nodesep=0.45; ranksep=0.85; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  subgraph cluster_t {{ label="理论基础"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12.5;
    T1 [label="标准化经济学\\n网络外部性·锁定效应\\n标准竞争与兼容选择", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    T2 [label="演化经济学\\n路径依赖·技术—制度共生演化\\n适应性治理", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    T3 [label="制度经济学与全球治理\\n布鲁塞尔效应·规则性权力\\n制度竞争与规则输出", fillcolor="{C['ltpurple']}", color="{C['purple']}"]; }}
  subgraph cluster_f {{ label="“三位一体”研究框架"; style=dashed; color="{C['orange']}"; fontcolor="{C['orange']}"; fontsize=12.5;
    F1 [label="动态演化机理\\n（认识规律）\\n第3—7章", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    F2 [label="体系构建\\n（设计体系）\\n第8—10章", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    F3 [label="适配性评估\\n（评价效果）\\n第11—13章", fillcolor="{C['ltorange']}", color="{C['orange']}"]; }}
  G [label="研究目标：构建国际认可、支撑“双碳”目标的中国绿色低碳标准体系", fillcolor="{C['ltgreen']}", color="{C['green']}", fontsize=13];
  {{rank=same; T1; T2; T3;}} T1 -> T2 -> T3 [style=invis];
  {{rank=same; F1; F2; F3;}}
  T1 -> F1 [label="标准竞争·锁定\\n→演化动力"];
  T1 -> F2;
  T2 -> F1 [label="共生演化\\n→互馈机制"];
  T2 -> F2 [label="适应性治理\\n→动态适应"];
  T3 -> F2;
  T3 -> F3 [label="国际规则\\n→适配标尺"];
  F1 -> F2 [label="规律→设计", color="{C['orange']}", penwidth=1.5, fontcolor="{C['orange']}"];
  F2 -> F3 [label="体系→评估", color="{C['orange']}", penwidth=1.5, fontcolor="{C['orange']}"];
  F3 -> F2 [label="反馈优化", style=dashed, color="{C['red']}", fontcolor="{C['red']}"];
  F1 -> G; F2 -> G; F3 -> G;
'''
    render(d, 'fig2_1')


# --------------------------------------------------- 图3.1 国际演进时间轴（matplotlib）
def fig3_1():
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    ax.set_xlim(1995.2, 2027.6)
    ax.set_ylim(-3.4, 3.9)
    ax.axis('off')
    ax.grid(False)
    stages = [(1996.0, 2004.5, C['ltblue'], PAL['blue'], '技术规范确立期\n（1997—2004）'),
              (2004.5, 2020.5, C['ltteal'], PAL['teal'], '制度化规制期\n（2005—2020）'),
              (2020.5, 2027.2, C['ltorange'], PAL['orange'], '战略工具化期\n（2021—  ）')]
    ax.annotate('', xy=(2027.5, 0), xytext=(1995.4, 0),
                arrowprops=dict(arrowstyle='-|>', color='#444444', lw=1.2), zorder=1)
    for x0, x1, fc, ec, lab in stages:
        ax.add_patch(Rectangle((x0, -0.42), x1 - x0, 0.84, fc=fc, ec=ec, lw=1.0, zorder=2))
        ax.text((x0 + x1) / 2, 0, lab, ha='center', va='center', fontsize=8,
                color=ec, fontweight='bold', linespacing=1.3, zorder=3)
    ax.text(2027.4, -0.75, '年份', fontsize=8, ha='right', color='#444444')
    events = [(1997, '《京都议定书》\n首个量化减排国际框架', 1),
              (2001, 'GHG Protocol 发布\n企业温室气体核算范式', -1),
              (2005, 'EU ETS 启动\n碳定价制度化开端', 1),
              (2015, '《巴黎协定》与 TCFD\n全球目标与气候信息披露', -1),
              (2021, '欧盟 CBAM 立法案\n标准成为贸易规则工具', 1),
              (2023, 'ISSB 准则·CBAM 过渡期\n可持续披露全球基线', -1)]
    cols = [PAL['blue'], PAL['blue'], PAL['teal'], PAL['teal'], PAL['orange'], PAL['orange']]
    hs = [1.55, -1.55, 2.6, -2.6, 1.55, -1.55]
    for (yr, lab, sgn), cc, h in zip(events, cols, hs):
        ax.plot([yr, yr], [0.45 * sgn, h - 0.45 * sgn], color=cc, lw=1.0, zorder=2)
        ax.plot([yr], [0.45 * sgn], marker='o', ms=4.5, color=cc, zorder=4)
        ax.text(yr, h, f'{yr}年\n{lab}', ha='center', va='center', fontsize=7,
                color='#1a1a1a', linespacing=1.35, zorder=3,
                bbox=dict(boxstyle='round,pad=0.32', fc='white', ec=cc, lw=0.9))
    save(fig, f'{FIG}/fig3_1.png')


# --------------------------------------------------- 图3.3 三足鼎立格局（matplotlib）
def fig3_3():
    fig, ax = canvas(8.0, 6.2, 100, 78)
    bx(ax, 32, 62, 36, 13, '欧　盟：领先—控制型\nEU ETS·CBAM·新电池法规\n以规则输出控制市场（布鲁塞尔效应）',
       fc=C['ltblue'], ec=PAL['blue'], fs=8.5, lw=1.4, bold=False)
    bx(ax, 1, 6, 34, 13, '美　国：领先—争夺型\nIRA·《清洁竞争法案》（CCA）\n以产业补贴与技术优势争夺主导权',
       fc=C['ltteal'], ec=PAL['teal'], fs=8.5, lw=1.4)
    bx(ax, 65, 6, 34, 13, '发展中国家：跟随—突破型\n规则接受者·合规成本高企\n谋求差异化突破与集体发声',
       fc=C['ltgold'], ec=PAL['gold'], fs=8.5, lw=1.4)
    bx(ax, 32, 30, 36, 14, '中　国\n全球最大碳排放国与制造业中心\n从“跟随”走向“并跑”、争取“领跑”',
       fc=C['ltred'], ec=PAL['red'], fs=9, lw=1.6, bold=True)
    # 三方博弈（灰色双向）
    arr(ax, (34, 63), (16, 20.5), c=PAL['gray'], lw=1.2, style='<|-|>', rad=0.08)
    txt(ax, 18.5, 44, '规则主导权竞争\n（碳定价 vs 产业补贴）', fs=7, c=PAL['gray'], rot=52)
    arr(ax, (66, 63), (84, 20.5), c=PAL['gray'], lw=1.2, style='<|-|>', rad=-0.08)
    txt(ax, 82.5, 44, 'CBAM 单边规制传导\nvs 合规压力与诉求', fs=7, c=PAL['gray'], rot=-52)
    arr(ax, (36.5, 12.5), (63.5, 12.5), c=PAL['gray'], lw=1.2, style='<|-|>')
    txt(ax, 50, 9.3, '产业链竞争与合作', fs=7, c=PAL['gray'])
    # 中国的突破方向（红色实线）
    arr(ax, (50, 45), (50, 61), c=PAL['red'], lw=1.6)
    txt(ax, 38.5, 53.4, '对接互认：ISO 14064/14067\nCBAM 核算规则衔接', fs=7, c=PAL['red'],
        ha='center')
    arr(ax, (33, 33), (21, 20.5), c=PAL['red'], lw=1.6)
    txt(ax, 20, 28.5, '技术与市场竞合\n新能源产业优势', fs=7, c=PAL['red'])
    arr(ax, (67, 33), (79, 20.5), c=PAL['red'], lw=1.6)
    txt(ax, 80.5, 28.5, '“一带一路”绿色标准合作\n引领集体突破', fs=7, c=PAL['red'])
    txt(ax, 50, 24.5, '突破方向：实线（红）＝中国主动作为；灰双向箭头＝三方战略互动',
        fs=6.5, c='#666666')
    save(fig, f'{FIG}/fig3_3.png')


# --------------------------------------------------- 图4.1 四层级金字塔（matplotlib）
def fig4_1():
    cum = R['std_counts']['cum']
    n = {k: cum[k]['2025'] for k in ('gb', 'hb', 'db', 'tb')}
    fig, ax = canvas(7.6, 5.6, 100, 74)
    top_y, base_y, top_hw, base_hw, cx = 66, 10, 8, 40, 50

    def hw(y):
        return top_hw + (base_hw - top_hw) * (top_y - y) / (top_y - base_y)

    layers = [('国家标准', n['gb'], '兜底保障：基础通用·强制底线', C['ltblue'], PAL['blue']),
              ('行业标准', n['hb'], '专业细化：行业技术特色', C['ltteal'], PAL['teal']),
              ('地方标准', n['db'], '先行先试：区域禀赋适配', C['ltgold'], PAL['gold']),
              ('团体标准', n['tb'], '创新引领：快速响应市场', C['ltgreen'], PAL['green'])]
    ys = [66, 52, 38, 24, 10]
    for (nm, cnt, role, fc, ec), y1, y0 in zip(layers, ys[:-1], ys[1:]):
        poly = Polygon([(cx - hw(y1), y1), (cx + hw(y1), y1),
                        (cx + hw(y0), y0), (cx - hw(y0), y0)],
                       closed=True, fc=fc, ec=ec, lw=1.4, zorder=2)
        ax.add_patch(poly)
        ym = (y1 + y0) / 2
        txt(ax, cx, ym + 2.2, nm, fs=9.5, bold=True, c='#1a1a1a')
        txt(ax, cx, ym - 2.6, f'{cnt} 项', fs=8.5, c=ec, bold=True)
        ax.plot([cx + hw(ym) + 1, cx + base_hw + 4], [ym, ym], color=ec, lw=0.8, ls=':')
        txt(ax, cx + base_hw + 5.5, ym, role, fs=7.5, c=ec, ha='left')
    arr(ax, (4.5, 14), (4.5, 62), c=PAL['gray'], lw=1.6, ms=13)
    txt(ax, 2.2, 38, '权威性·约束力增强', fs=7.5, c=PAL['gray'], rot=90)
    arr(ax, (10.5, 62), (10.5, 14), c=PAL['gray'], lw=1.6, ms=13)
    txt(ax, 13.0, 38, '灵活性·创新性增强', fs=7.5, c=PAL['gray'], rot=270)
    txt(ax, 50, 3.5, '注：数量为截至 2025 年累计有效标准数（标准文本数据库）', fs=7, c='#666666')
    save(fig, f'{FIG}/fig4_1.png')


# --------------------------------------------------- 图5.1 状态空间模型逻辑（graphviz）
def fig5_1():
    d = f'''
  rankdir=TB; nodesep=0.35; ranksep=0.5; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.16,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  U [label="驱动向量 u_t = (u^ETS, u^DC, u^CBAM, u^Tech)ᵀ\\n碳市场政策·“双碳”政策·国际规制·绿色技术", fillcolor="{C['ltorange']}", color="{C['orange']}"];
  S [label="状态向量 S_t = (S_1t, …, S_5t)ᵀ\\n五类标准综合指数：碳排放核算/碳足迹认证/\\n绿色产品/碳吸收/绿色金融", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  EQ [label="状态方程　dS_t/dt = A·S_t + B·u_t + ε_t", fillcolor="{C['ltteal']}", color="{C['teal']}", fontsize=13.5];
  AN [label="A：5×5 标准间交互矩阵\\n对角元＝自我调整速度\\n非对角元＝互补（+）/替代（－）", fillcolor="{C['ltgray']}", color="{C['gray']}", fontsize=11];
  BN [label="B：5×4 驱动传导矩阵\\n三重驱动力→五类标准\\n的传导强度", fillcolor="{C['ltgray']}", color="{C['gray']}", fontsize=11];
  OBS [label="观测数据：标准文本数据库（1993—2025）\\n量化编码（技术严格程度×覆盖完整性，n=165）", fillcolor="{C['ltgold']}", color="{C['gold']}"];
  KF [label="卡尔曼滤波（预测—更新递推）＋极大似然估计", fillcolor="{C['ltpurple']}", color="{C['purple']}", fontsize=13];
  EST [label="参数估计结果 Â、B̂\\n识别标准间互补/替代关系·三重驱动力时变贡献", fillcolor="{C['ltgreen']}", color="{C['green']}"];
  SIM [label="情景模拟（2026—2035）\\n基准延续/政策强化/供给停滞三情景", fillcolor="{C['ltgreen']}", color="{C['green']}"];
  PHI [label="输出：溢出矩阵 Φ\\n（第10章系统动力学模型）", style="rounded,filled,dashed", fillcolor="white", color="{C['red']}", fontcolor="{C['red']}"];
  {{rank=same; U; S;}} U -> S [style=invis];
  {{rank=same; AN; EQ; BN; OBS;}} AN -> EQ -> BN -> OBS [style=invis];
  {{rank=same; SIM; PHI;}} SIM -> PHI [style=invis];
  U -> EQ; S -> EQ;
  AN -> EQ [style=dotted, dir=none]; BN -> EQ [style=dotted, dir=none];
  EQ -> KF; OBS -> KF;
  KF -> EST; EST -> SIM;
  EST -> PHI [style=dashed, color="{C['red']}"];
'''
    render(d, 'fig5_1')


# --------------------------------------------------- 图6.1 技术—制度互馈（matplotlib）
def fig6_1():
    lv = R['lv']
    a0, a1 = lv['pre']['alpha'], lv['post']['alpha']
    b0, b1 = lv['pre']['beta'], lv['post']['beta']
    g0, g1 = lv['pre']['gamma'], lv['post']['gamma']
    w0, w1 = lv['omega']['p2004_2019'], lv['omega']['p2020_2025']
    fig, ax = canvas(8.0, 5.6, 100, 68)
    # 外部驱动（顶部）
    bx(ax, 32, 58, 36, 8, '外部驱动：“双碳”目标·政策推力·市场调节力',
       fc='white', ec=PAL['gray'], fs=8.5, ls='dashed')
    arr(ax, (40, 57.6), (30, 47.6), c=PAL['gray'], lw=1.1)
    arr(ax, (60, 57.6), (70, 47.6), c=PAL['gray'], lw=1.1)
    # 两大系统
    bx(ax, 8, 30, 33, 17, '技术系统 T_t\n绿色低碳技术水平\nLogistic 增长：速率 r_T·容量 K_T',
       fc=C['ltblue'], ec=PAL['blue'], fs=8.6, lw=1.6, bold=False)
    bx(ax, 59, 30, 33, 17, '制度系统 I_t\n标准体系完善度\n速率 r_I·容量 K_I·调整成本 C_I',
       fc=C['ltteal'], ec=PAL['teal'], fs=8.6, lw=1.6)
    # 自增长回路
    arr(ax, (12, 47.6), (24, 47.6), c=PAL['blue'], lw=1.1, rad=-1.7, ms=9)
    txt(ax, 18, 54.4, 'r_T·T(1－T/K_T)', fs=7.5, c=PAL['blue'])
    arr(ax, (76, 47.6), (88, 47.6), c=PAL['teal'], lw=1.1, rad=-1.7, ms=9)
    txt(ax, 82, 54.4, 'r_I·I(1－I/K_I)', fs=7.5, c=PAL['teal'])
    # 互馈双箭头
    arr(ax, (41.5, 42), (58.5, 42), c=PAL['orange'], lw=1.9, rad=-0.25, ms=15)
    txt(ax, 50, 49.5, 'α：技术进步催生标准需求\nα：%.3f → %.3f（“双碳”后）' % (a0, a1),
        fs=7.8, c=PAL['orange'], bold=True)
    arr(ax, (58.5, 34), (41.5, 34), c=PAL['green'], lw=1.9, rad=-0.25, ms=15)
    txt(ax, 50, 27.0, 'β：标准引导技术研发方向\nβ：%.3f → %.3f' % (b0, b1),
        fs=7.8, c=PAL['green'], bold=True)
    txt(ax, 76.5, 26.8, '制度调整阻尼 γ：%.2f → %.2f' % (g0, g1), fs=7.2, c=PAL['teal'])
    # 综合状态
    bx(ax, 31, 6, 38, 11, '标准体系综合状态\nS_t = T_t^ω · I_t^(1－ω)　（ω：%.2f → %.2f）' % (w0, w1),
       fc=C['ltgold'], ec=PAL['gold'], fs=9, lw=1.6, bold=True)
    arr(ax, (24, 29.5), (38, 17.6), c=PAL['blue'], lw=1.4)
    txt(ax, 26.5, 20.5, '技术贡献 ω', fs=7.2, c=PAL['blue'], rot=40)
    arr(ax, (76, 29.5), (62, 17.6), c=PAL['teal'], lw=1.4)
    txt(ax, 74, 20.5, '制度贡献 1－ω', fs=7.2, c=PAL['teal'], rot=-40)
    # 状态反馈（虚线，沿左侧回到外部驱动）
    ax.plot([30.6, 3, 3], [11.5, 11.5, 62], color=PAL['red'], lw=1.1, ls='--', zorder=1)
    arr(ax, (3, 62), (31.6, 62), c=PAL['red'], lw=1.1, ls='--', ms=11)
    txt(ax, 5.2, 36, '状态反馈：绩效评估\n调节政策与市场力度', fs=7, c=PAL['red'], rot=90)
    save(fig, f'{FIG}/fig6_1.png')


# --------------------------------------------------- 图7.1 三方博弈关系（matplotlib）
def fig7_1():
    fig, ax = canvas(8.2, 6.4, 100, 80)
    bx(ax, 29, 62, 42, 15, '政　府　G\n策略：强制推行（x）／激励引导（1－x）\n参数：执法成本 c_G·补贴 s·声誉收益 R_G',
       fc=C['ltblue'], ec=PAL['blue'], fs=8.5, lw=1.6, bold=False)
    bx(ax, 2, 6, 40, 15, '企　业　E\n策略：积极响应（y）／被动观望（1－y）\n参数：遵从成本 c_E·竞争力提升 ΔM·处罚 F',
       fc=C['ltteal'], ec=PAL['teal'], fs=8.5, lw=1.6)
    bx(ax, 58, 6, 40, 15, '国际组织　O\n策略：接纳衔接（z）／排斥壁垒（1－z）\n参数：互认收益 R_O·排斥损失 L_O',
       fc=C['ltgold'], ec=PAL['gold'], fs=8.5, lw=1.6)
    # G—E
    arr(ax, (33, 61.5), (18, 21.5), c=PAL['blue'], lw=1.4, rad=0.12)
    txt(ax, 15.5, 44, '政策工具：补贴 s\n处罚 F·标准约束', fs=7.2, c=PAL['blue'], rot=65)
    arr(ax, (25, 21.5), (40, 61.5), c=PAL['teal'], lw=1.4, rad=0.12)
    txt(ax, 26.3, 41, '响应程度影响\n声誉收益 R_G', fs=7.0, c=PAL['teal'], rot=70)
    # E—O
    arr(ax, (43, 15.5), (57, 15.5), c=PAL['teal'], lw=1.4, rad=0.35)
    txt(ax, 50, 24.5, '达标产品出口·申请认证互认', fs=7.2, c=PAL['teal'])
    arr(ax, (57, 10.5), (43, 10.5), c=PAL['gold'], lw=1.4, rad=0.35)
    txt(ax, 50, 2.6, '碳关税减免 ΔT·市场准入·竞争力提升 ΔM', fs=7.2, c=PAL['gold'])
    # G—O
    arr(ax, (67, 61.5), (82, 21.5), c=PAL['blue'], lw=1.4, rad=-0.12)
    txt(ax, 85, 44, '标准互认谈判\n国际标准化参与', fs=7.2, c=PAL['blue'], rot=-65)
    arr(ax, (75, 21.5), (60, 61.5), c=PAL['gold'], lw=1.4, rad=-0.12)
    txt(ax, 73.7, 41, '规则约束\n衔接要求传导', fs=7.0, c=PAL['gold'], rot=-70)
    # 中心：复制动态系统
    bx(ax, 31, 33, 38, 14, '复制动态系统（dx/dt, dy/dt, dz/dt）\n均衡跃迁：“被动跟跑”→“主动领跑”\n关键条件：ΔT＋ΔM＞2.0（阈值）',
       fc=C['ltred'], ec=PAL['red'], fs=8, lw=1.4, ls='dashed', bold=True)
    for p1, p2 in [((41, 61.5), (44, 47.6)), ((30, 21.5), (37, 32.4)), ((70, 21.5), (63, 32.4))]:
        arr(ax, p1, p2, c=PAL['red'], lw=1.0, ls='--', ms=10)
    txt(ax, 50, 29.5, '三方策略互动（虚线）共同决定演化均衡', fs=6.8, c=PAL['red'])
    save(fig, f'{FIG}/fig7_1.png')


# --------------------------------------------------- 图8.1 SSDMI 测算框架（graphviz）
def fig8_1():
    reg = R['ssdmi']['reg']
    d = f'''
  rankdir=TB; nodesep=0.3; ranksep=0.45; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  subgraph cluster_d {{ label="需求侧：真实标准需求内生建模"; style=dashed; color="{C['orange']}"; fontcolor="{C['orange']}"; fontsize=12;
    CI [label="碳排放系数 CI\\n（β=%.3f***）", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    GT [label="绿色转型进程 GT\\n（β=%.3f***）", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    PC [label="减排约束强度 PC\\n（β=%.3f**）", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    CB [label="CBAM 国际压力\\n（β=%.3f***）", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    D [label="行业真实标准需求 D_kt = f(CI, GT, PC, CBAM)\\n面板回归（R²=%.2f，N=%d）", fillcolor="{C['orange']}", fontcolor="white", color="{C['orange']}", fontsize=13];
  }}
  subgraph cluster_s {{ label="供给侧：有效标准供给量化"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12;
    DB [label="标准文本数据库\\n四层级×五大功能模块", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    RR [label="行业有效标准供给 R_kt\\n（覆盖度×严格度加权）", fillcolor="{C['blue']}", fontcolor="white", color="{C['blue']}", fontsize=13];
  }}
  MIS [label="供需错配指数　SSDMI_kt = (D_kt － R_kt) / D_kt\\n＞0 短缺性错配；＜0 冗余性错配", fillcolor="{C['ltteal']}", color="{C['teal']}", fontsize=13.5];
  W [label="碳排放权重 w_kt 加权 → 综合错配指数\\n八大高碳行业（2015—2025）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  OUT [label="结构性短板识别：碳吸收端·市场机制类标准缺口最大", fillcolor="{C['ltgold']}", color="{C['gold']}", fontsize=13];
  FB [label="反馈：指导第9章体系架构\\n横向补短板设计", style="rounded,filled,dashed", fillcolor="white", color="{C['red']}", fontcolor="{C['red']}"];
  {{rank=same; CI; GT; PC; CB; DB;}} CI -> GT -> PC -> CB [style=invis];
  CI -> D; GT -> D; PC -> D; CB -> D;
  DB -> RR;
  D -> MIS; RR -> MIS;
  MIS -> W; W -> OUT;
  OUT -> FB [style=dashed, color="{C['red']}"];
''' % (reg['CI']['coef'], reg['GT']['coef'], reg['PC']['coef'], reg['CBAM']['coef'],
       reg['R2'], reg['N'])
    render(d, 'fig8_1')


# --------------------------------------------------- 图9.1 总体架构（matplotlib，核心图）
def fig9_1():
    ahp = R['ahp']['module']
    fig, ax = canvas(11.2, 7.4, 122, 82)
    # 顶部：目标
    bx(ax, 24, 74, 72, 7, '“双碳”目标（2030 碳达峰·2060 碳中和）→ 构建国际认可的中国绿色低碳标准体系',
       fc=C['ltred'], ec=PAL['red'], fs=9.5, lw=1.6, bold=True, pad=0.4)
    arr(ax, (60, 73.6), (60, 69.2), c=PAL['red'], lw=1.6)
    # 五大功能模块（列）
    mods = [('碳排放核算', ahp['acct'], C['ltblue'], PAL['blue']),
            ('碳足迹认证', ahp['fp'], C['ltteal'], PAL['teal']),
            ('绿色产品', ahp['prod'], C['ltgold'], PAL['gold']),
            ('碳吸收', ahp['sink'], C['ltgreen'], PAL['green']),
            ('绿色金融', ahp['fin'], C['ltpurple'], PAL['purple'])]
    cells = {
        '国家': ['核算通则与\nMRV 制度', '产品碳足迹\n量化通则', '绿色产品\n评价通则', '碳汇计量\n监测通则', '绿色金融\n术语与目录'],
        '行业': ['重点行业核算细则\n（钢铁·水泥等）', '重点产品\n种类规则 PCR', '行业绿色设计\n与能效标准', '林业·海洋\n碳汇方法学', '环境信息\n披露规范'],
        '地方': ['区域温室\n气体清单', '试点城市\n认证规范', '绿色采购与\n消费目录', '生态产品\n价值核算', '绿色金融改革\n试验区标准'],
        '团体': ['数字化碳监测\n在线核算', '碳标签与\n快速认证', '先进值引领\n（“领跑者”）', 'CCUS·负排放\n技术标准', '转型金融与\n碳金融产品']}
    rows = [('国家标准', '基础通用·兜底', 55.5, 66.5), ('行业标准', '行业细化·深化', 43.5, 54.5),
            ('地方标准', '先行先试·适配', 31.5, 42.5), ('团体标准', '市场创新·引领', 19.5, 30.5)]
    x0, cw, gap = 35, 11.6, 0.9
    # 列头
    for i, (nm, w, fc, ec) in enumerate(mods):
        xx = x0 + i * (cw + gap)
        bx(ax, xx, 67.5, cw, 5.6, f'{nm}\n（权重 {w:.3f}）', fc=ec, ec=ec, fs=7.5,
           tc='white', bold=True, pad=0.3)
    # 行头与单元格
    for (rnm, rrole, y0, y1) in rows:
        bx(ax, 24.5, y0, 9.2, y1 - y0, f'{rnm}\n{rrole}', fc=C['ltgray'], ec=PAL['gray'],
           fs=6.8, bold=True, pad=0.3)
        key = rnm[:2]
        for i, (nm, w, fc, ec) in enumerate(mods):
            xx = x0 + i * (cw + gap)
            bx(ax, xx, y0, cw, y1 - y0, cells[key][i], fc=fc, ec=ec, fs=6.2, lw=0.9, pad=0.3)
    # 左侧：三项构建原则
    bx(ax, 1.5, 62, 20, 6, '三项体系构建原则', fc=PAL['orange'], ec=PAL['orange'], fs=8.5,
       tc='white', bold=True, pad=0.35)
    prins = [('协同互补', '源于标准间互补/替代关系\n（第5章状态空间模型）', 51),
             ('动态适应', '源于技术—制度互馈机制\n（第6章 LV 协同演进）', 38),
             ('多元协调', '源于多主体激励相容要求\n（第7章演化博弈）', 25)]
    for nm, src, yy in prins:
        bx(ax, 1.5, yy, 20, 10, f'{nm}\n{src}', fc=C['ltorange'], ec=PAL['orange'],
           fs=6.6, pad=0.35)
        arr(ax, (22.2, yy + 5), (24.2, yy + 5), c=PAL['orange'], lw=1.2, ls='--', ms=10)
    txt(ax, 11.5, 21.5, '（虚线＝原则指导）', fs=6.2, c=PAL['orange'])
    # 右侧：国际衔接接口
    bx(ax, 100.5, 62, 20, 6, '国际衔接接口', fc=PAL['teal'], ec=PAL['teal'], fs=8.5,
       tc='white', bold=True, pad=0.35)
    intf = [('ISO 14064/14067\n方法学对标', 53), ('CBAM 核算规则\n与缺省值衔接', 43),
            ('第三方核查与\n认证结果互认', 33), ('MRV 数据质量\n国际对标', 23)]
    for lab, yy in intf:
        bx(ax, 100.5, yy, 20, 8, lab, fc=C['ltteal'], ec=PAL['teal'], fs=6.8, pad=0.35)
    arr(ax, (97.5, 44), (100.2, 44), c=PAL['teal'], lw=1.6, style='<|-|>')
    txt(ax, 98.8, 47.5, '衔接\n互认', fs=6.5, c=PAL['teal'])
    # 底部：反馈优化
    bx(ax, 24.5, 9, 71.5, 7,
       '动态反馈优化：SSDMI 错配识别（第8章）·SFA-PEL 政策适配（第11章）·ISGI-CIAI 国际适配（第12章）→ 补短板·调权重·促衔接',
       fc='white', ec=PAL['red'], fs=7.5, ls='dashed', pad=0.4)
    arr(ax, (60, 16.4), (60, 19.1), c=PAL['red'], lw=1.4, ls='--')
    txt(ax, 60, 4.8, '注：矩阵单元格为各层级×各模块建设重点；模块权重为 AHP 测算结果（CR=%.3f＜0.1）' % ahp['CR'],
        fs=6.8, c='#666666')
    save(fig, f'{FIG}/fig9_1.png')


# --------------------------------------------------- 图9.2 AHP 层次结构（graphviz）
def fig9_2():
    cr = R['ahp']['criteria']
    mo = R['ahp']['module']
    ex = R['ahp']['experts']
    d = f'''
  rankdir=TB; nodesep=0.25; ranksep=0.75; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.16,0.09"];
  edge [color="{C['gray']}", arrowsize=0.7];
  A [label="目标层 A：绿色低碳标准体系\\n五大功能模块建设优先序", fillcolor="{C['ltred']}", color="{C['red']}", fontsize=13.5];
  C1 [label="准则层 C1\\n碳减排贡献度\\n（权重 {cr['carbon']:.3f}）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  C2 [label="准则层 C2\\n产业转型促进度\\n（权重 {cr['industry']:.3f}）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  C3 [label="准则层 C3\\n国际衔接兼容度\\n（权重 {cr['intl']:.3f}）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  P1 [label="碳排放核算\\n（{mo['acct']:.3f}）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  P2 [label="碳足迹认证\\n（{mo['fp']:.3f}）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  P3 [label="碳吸收\\n（{mo['sink']:.3f}）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  P4 [label="绿色产品\\n（{mo['prod']:.3f}）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  P5 [label="绿色金融\\n（{mo['fin']:.3f}）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  NOTE [label="德尔菲法两轮征询：{ex['n']} 位专家，Kendall W={ex['kendall_w']:.2f}\\n判断矩阵一致性：准则层 CR={cr['CR']:.3f}，方案层 CR={mo['CR']:.3f}，均＜0.1", shape=note, style="filled", fillcolor="{C['ltgray']}", color="{C['gray']}", fontsize=11];
  {{rank=same; C1; C2; C3;}} C1 -> C2 -> C3 [style=invis];
  {{rank=same; P1; P2; P3; P4; P5;}} P1 -> P2 -> P3 -> P4 -> P5 [style=invis];
  A -> C1; A -> C2; A -> C3;
  C1 -> P1; C1 -> P2; C1 -> P3; C1 -> P4; C1 -> P5;
  C2 -> P1; C2 -> P2; C2 -> P3; C2 -> P4; C2 -> P5;
  C3 -> P1; C3 -> P2; C3 -> P3; C3 -> P4; C3 -> P5;
  P3 -> NOTE [style=invis];
'''
    render(d, 'fig9_2')


# --------------------------------------------------- 图9.4 四层级分工衔接（matplotlib）
def fig9_4():
    fig, ax = canvas(8.0, 6.0, 100, 74)
    layers = [('国家标准——兜底保障', '基础通用·强制底线·全国统一实施', 57, C['ltblue'], PAL['blue']),
              ('行业标准——专业细化', '行业技术特点·支撑主管部门监管', 41, C['ltteal'], PAL['teal']),
              ('地方标准——先行先试', '结合区域禀赋·为国标积累经验', 25, C['ltgold'], PAL['gold']),
              ('团体标准——创新引领', '快速响应市场·先进值高于国标', 9, C['ltgreen'], PAL['green'])]
    for nm, sub, y, fc, ec in layers:
        bx(ax, 25, y, 50, 11, f'{nm}\n{sub}', fc=fc, ec=ec, fs=9, lw=1.5, bold=False)
    mech = [('引用衔接·分工不交叉不重复', 54.2), ('严于上位标准·区域差异适配', 38.2),
            ('试点协同·竞争互补', 22.2)]
    for lab, y in mech:
        arr(ax, (38, y + 2), (38, y - 1.6), c=PAL['gray'], lw=1.1, ms=10)
        arr(ax, (62, y - 1.6), (62, y + 2), c=PAL['gray'], lw=1.1, ms=10)
        txt(ax, 50, y + 0.2, lab, fs=6.8, c='#555555',
            bold=False)
    # 左：约束传导（下行，实线）
    arr(ax, (17, 64), (17, 12), c=PAL['blue'], lw=2.6, ms=17)
    txt(ax, 12.5, 38, '纵向约束传导：统一术语·方法·底线\n（自上而下，实线＝直接作用）',
        fs=7.5, c=PAL['blue'], rot=90)
    # 右：经验上升（上行，虚线反馈）
    arr(ax, (83, 12), (83, 64), c=PAL['red'], lw=2.2, ms=17, ls='--')
    txt(ax, 88.5, 38, '经验上升与采信转化：地方先行经验上升为国标\n成熟团标转化为行标/国标（虚线＝反馈）',
        fs=7.5, c=PAL['red'], rot=270)
    txt(ax, 50, 3, '四层级“各有分工、纵向贯通、上下互动”的衔接逻辑', fs=8, c='#444444', bold=True)
    save(fig, f'{FIG}/fig9_4.png')


# --------------------------------------------------- 图10.1 因果回路图（matplotlib）
def fig10_1():
    fig, ax = canvas(8.6, 5.8, 100, 64)
    nodes = {
        'SI': (13, 32, '标准制定投入'),
        'A': (29, 51, '碳排放核算\n标准存量'),
        'B': (53, 57, '碳足迹认证\n标准存量'),
        'CN': (78, 50, '绿色产品·碳吸收\n绿色金融标准存量'),
        'E': (87, 25, '标准体系\n综合效能'),
        'T': (60, 8, '绿色技术创新'),
        'L': (15, 12, '存量维护与\n修订负荷')}

    def edge(k1, k2, sign, rad=0.12, col=None, lab=None, labp=None, sp=None,
             shA=16, shB=30):
        x1, y1, _ = nodes[k1]
        x2, y2, _ = nodes[k2]
        col = col or (PAL['blue'] if sign == '+' else PAL['red'])
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=13,
                            color=col, lw=1.5, connectionstyle=f'arc3,rad={rad}',
                            shrinkA=shA, shrinkB=shB, zorder=1)
        ax.add_patch(a)
        txt(ax, sp[0], sp[1], '＋' if sign == '+' else '－', fs=10.5, c=col, bold=True)
        if lab:
            txt(ax, labp[0], labp[1], lab, fs=6.6, c=col)

    # R1：SI→A→B→CN→E→SI（标准链增强回路）
    edge('SI', 'A', '+', rad=0.15, lab='新订标准', labp=(14.5, 43.5), sp=(24.5, 45.5), shB=26)
    edge('A', 'B', '+', rad=0.15, lab='核算奠定认证基础', labp=(38, 60.0), sp=(44.5, 58.5), shB=34)
    edge('B', 'CN', '+', rad=0.15, lab='认证支撑产品评价', labp=(68, 60.0), sp=(70, 55.8), shB=48)
    edge('CN', 'E', '+', rad=0.15, lab='覆盖完整性提升', labp=(93.5, 38.5), sp=(90.5, 31.5), shB=24)
    edge('E', 'SI', '+', rad=-0.15, lab='效能显现→政策与市场加大投入', labp=(50, 32.8), sp=(24, 35.5), shB=38)
    # R2：E→T→SI（技术—标准互促回路）
    edge('E', 'T', '+', rad=0.12, lab='效能引导创新', labp=(80, 13.0), sp=(69.5, 10.2), shB=38)
    edge('T', 'SI', '+', rad=0.14, lab='技术进步催生新标准需求', labp=(45, 12.6), sp=(20.5, 26.5), shB=32)
    # B1：SI→L→SI（资源约束平衡回路）
    edge('SI', 'L', '+', rad=0.28, lab='存量累积\n（延迟）', labp=(3.5, 22), sp=(9.0, 16.0), shB=26)
    edge('L', 'SI', '-', rad=0.28, lab='挤占制定资源', labp=(27.5, 19), sp=(19.5, 28.5), shB=26)
    # 节点文字（白底盖住箭头端部）
    for k, (x, y, lab) in nodes.items():
        ax.text(x, y, lab, fontsize=8.5, color='#1a1a1a', fontweight='bold',
                ha='center', va='center', linespacing=1.3, zorder=5,
                bbox=dict(boxstyle='round,pad=0.32', fc='white', ec='none', alpha=0.92))
    # 回路标注
    for xx, yy, rl, rn, cc in [(53, 42, 'R1', '标准链增强回路', PAL['blue']),
                               (57, 22, 'R2', '技术—标准互促回路', PAL['teal']),
                               (15, 25, 'B1', '资源约束平衡回路', PAL['red'])]:
        cir = Ellipse((xx, yy + 0.4), 5.6, 4.6, fc='white', ec=cc, lw=1.3, zorder=3)
        ax.add_patch(cir)
        txt(ax, xx, yy + 0.4, rl, fs=9, c=cc, bold=True)
        txt(ax, xx, yy - 3.8, rn, fs=6.8, c=cc, z=5)
    txt(ax, 50, 1.2, '注：＋＝同向变动，－＝反向变动；R＝增强回路，B＝平衡回路；（延迟）＝存量累积滞后效应',
        fs=7, c='#666666')
    save(fig, f'{FIG}/fig10_1.png')


# --------------------------------------------------- 图10.2 存量—流量结构（matplotlib）
def fig10_2():
    fig, ax = canvas(8.6, 5.8, 100, 66)

    def cloud(x, y, lab):
        e = Ellipse((x, y), 9, 6, fc='white', ec=PAL['gray'], lw=1.1, ls='--', zorder=2)
        ax.add_patch(e)
        txt(ax, x, y, lab, fs=7, c=PAL['gray'])

    def valve(x, y, col):
        ax.add_patch(Polygon([(x - 1.8, y + 2), (x, y), (x - 1.8, y - 2)], closed=True,
                             fc=col, ec=col, zorder=3))
        ax.add_patch(Polygon([(x + 1.8, y + 2), (x, y), (x + 1.8, y - 2)], closed=True,
                             fc=col, ec=col, zorder=3))

    yF = 40
    cloud(8, yF, '源')
    cloud(92, yF, '汇')
    # 存量
    ax.add_patch(Rectangle((40, yF - 6.5), 22, 13, fc=C['ltblue'], ec=PAL['blue'], lw=1.8, zorder=2))
    txt(ax, 51, yF, '标准存量 SS_kt\n（第 k 功能模块）', fs=9, bold=True)
    # 流入/流出
    ax.plot([12.5, 39.8], [yF, yF], color=PAL['blue'], lw=2.2, zorder=1)
    arr(ax, (36, yF), (39.8, yF), c=PAL['blue'], lw=2.2, ms=15)
    valve(25, yF, PAL['blue'])
    txt(ax, 22, yF - 6.2, '标准新增流量 SI_kt\n（新订·修订）', fs=7.8, c=PAL['blue'], bold=True)
    ax.plot([62.2, 87.5], [yF, yF], color=PAL['gray'], lw=2.2, zorder=1)
    arr(ax, (84, yF), (87.5, yF), c=PAL['gray'], lw=2.2, ms=15)
    valve(75, yF, PAL['gray'])
    txt(ax, 75, yF + 5.6, '标准淘汰流量 SO_kt\n（废止·整合）', fs=7.8, c=PAL['gray'], bold=True)
    # 溢出与政策驱动
    bx(ax, 2, 55, 22, 8, '其他模块标准存量\nSS_jt（j≠k）', fc=C['ltteal'], ec=PAL['teal'], fs=7.5)
    arr(ax, (14, 54.6), (23.5, yF + 2.6), c=PAL['teal'], lw=1.5, rad=-0.08)
    txt(ax, 8.5, 47.5, '协同溢出 φ_kj\n（源于第5章Â矩阵）', fs=6.8, c=PAL['teal'])
    bx(ax, 34, 55, 28, 8, '政策驱动 u_t\n（“双碳”政策·碳市场·CBAM）', fc=C['ltorange'], ec=PAL['orange'], fs=7.5)
    arr(ax, (40, 54.6), (27, yF + 2.8), c=PAL['orange'], lw=1.5, rad=0.1)
    txt(ax, 36, 49.2, '政策推力', fs=7.0, c=PAL['orange'])
    # 技术—政策偏离度机制
    bx(ax, 12, 17, 22, 8, '技术前沿水平 TL_kt', fc=C['ltgreen'], ec=PAL['green'], fs=8)
    bx(ax, 44, 17, 22, 8, '标准技术水平 SL_kt', fc=C['ltblue'], ec=PAL['blue'], fs=8)
    arr(ax, (53, yF - 6.9), (55, 25.4), c=PAL['blue'], lw=1.3)
    txt(ax, 63.5, 31.0, '存量→标准\n技术水平', fs=6.8, c=PAL['blue'])
    e = Ellipse((33, 6.5), 34, 9, fc=C['ltgold'], ec=PAL['gold'], lw=1.4, zorder=2)
    ax.add_patch(e)
    txt(ax, 33, 6.5, '技术—政策偏离度\nTPD_kt = (TL_kt － SL_kt) / TL_kt', fs=7.8, bold=True)
    arr(ax, (21, 16.6), (26, 10.6), c=PAL['green'], lw=1.3)
    txt(ax, 19.5, 13, '＋', fs=10, c=PAL['green'], bold=True)
    arr(ax, (54, 16.6), (44, 10.2), c=PAL['blue'], lw=1.3)
    txt(ax, 52.5, 12.6, '－', fs=10, c=PAL['blue'], bold=True)
    # 触发判断
    ax.add_patch(Polygon([(76, 12.5), (86.5, 7), (97, 12.5), (86.5, 18)], closed=True,
                         fc=C['ltred'], ec=PAL['red'], lw=1.4, zorder=2))
    txt(ax, 86.5, 12.5, '触发判断\nTPD_kt＞TPD*？\n（TPD*=%.2f）' % R['sd']['tpd_star'], fs=7, c=PAL['red'], bold=True)
    arr(ax, (50.5, 6.5), (75.4, 11), c=PAL['gold'], lw=1.3)
    # 反馈虚线：修订与淘汰
    arr(ax, (84, 18.6), (26.5, yF - 2.8), c=PAL['red'], lw=1.4, ls='--', rad=-0.22)
    txt(ax, 41, 27.8, '是→触发新订/修订（虚线反馈）', fs=7.2, c=PAL['red'])
    arr(ax, (91, 18.6), (76.5, yF - 2.6), c=PAL['red'], lw=1.4, ls='--', rad=0.2)
    txt(ax, 91.5, 27.5, '是→触发\n废止淘汰', fs=7.2, c=PAL['red'])
    txt(ax, 50, 0.8, '注：矩形＝存量；蝶形阀＝流量；虚线椭圆＝系统边界外源/汇；虚线箭头＝动态更新反馈',
        fs=7, c='#666666')
    save(fig, f'{FIG}/fig10_2.png')


# --------------------------------------------------- 图11.1 SFA-PEL 框架（graphviz）
def fig11_1():
    sfa = R['sfa']
    pel = sfa['pel']
    d = f'''
  rankdir=TB; nodesep=0.3; ranksep=0.42; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  subgraph cluster_x {{ label="投入变量（30省×2010—2025，N=480）"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12;
    X1 [label="标准供给量 X1\\n（弹性 0.312***）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    X2 [label="监管经费 X2\\n（弹性 0.187***）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    X3 [label="执法人员 X3\\n（弹性 0.094**）", fillcolor="{C['ltblue']}", color="{C['blue']}"]; }}
  subgraph cluster_z {{ label="无效率决定因素（效率均值方程）"; style=dashed; color="{C['purple']}"; fontcolor="{C['purple']}"; fontsize=12;
    Z1 [label="标准完整性 SCI\\n（－0.428***）", fillcolor="{C['ltpurple']}", color="{C['purple']}"];
    Z2 [label="激励强度 INC\\n（－0.365***）", fillcolor="{C['ltpurple']}", color="{C['purple']}"];
    Z3 [label="协调效率 CDE\\n（－0.291***）", fillcolor="{C['ltpurple']}", color="{C['purple']}"]; }}
  F [label="随机前沿模型（Battese-Coelli, 1995）\\nlnY_it = f(lnX_it; β) + v_it － u_it　（γ={sfa['gamma']:.2f}，LR={sfa['lr_stat']:.1f}）", fillcolor="{C['ltteal']}", color="{C['teal']}", fontsize=13];
  U [label="无效率项 u_it", fillcolor="{C['ltpurple']}", color="{C['purple']}"];
  TE [label="标准执行效率　TE_it = exp(－u_it)", fillcolor="{C['ltgold']}", color="{C['gold']}", fontsize=13.5];
  PEL [label="政策有效性损失　PEL_it = 1 － TE_it", fillcolor="{C['ltorange']}", color="{C['orange']}", fontsize=13.5];
  subgraph cluster_dec {{ label="PEL 三源分解（Oaxaca-Blinder）"; style=dashed; color="{C['red']}"; fontcolor="{C['red']}"; fontsize=12;
    D1 [label="供给不足损失\\n{pel['supply']*100:.1f}%", fillcolor="{C['ltred']}", color="{C['red']}"];
    D2 [label="激励不完善损失\\n{pel['incentive']*100:.1f}%", fillcolor="{C['ltred']}", color="{C['red']}"];
    D3 [label="协调失灵损失\\n{pel['coordinate']*100:.1f}%", fillcolor="{C['ltred']}", color="{C['red']}"]; }}
  FB [label="政策优化反馈：补供给·强激励·促协调\\n（衔接第9—10章体系优化与第14章政策建议）", style="rounded,filled,dashed", fillcolor="white", color="{C['red']}", fontcolor="{C['red']}", fontsize=12];
  {{rank=same; X1; X2; X3;}} X1 -> X2 -> X3 [style=invis];
  {{rank=same; Z1; Z2; Z3;}} Z1 -> Z2 -> Z3 [style=invis];
  {{rank=same; D1; D2; D3;}} D1 -> D2 -> D3 [style=invis];
  X1 -> F; X2 -> F; X3 -> F;
  Z1 -> U; Z2 -> U; Z3 -> U;
  U -> F; F -> TE; TE -> PEL;
  PEL -> D1; PEL -> D2; PEL -> D3;
  D2 -> FB [style=dashed, color="{C['red']}", ltail=cluster_dec];
'''
    render(d, 'fig11_1')


# --------------------------------------------------- 图12.1 ISGI-CIAI 框架（graphviz）
def fig12_1():
    d = f'''
  rankdir=TB; nodesep=0.24; ranksep=0.42; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12, margin="0.13,0.08"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  subgraph cluster_dim {{ label="八维度中外标准比较（专家逐维评分，对标 ISO/IEC 与 CBAM 规范）"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12;
    K1 [label="核算边界", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    K2 [label="排放因子", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    K3 [label="生命周期范围", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    K4 [label="第三方核查", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    K5 [label="数据质量", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    K6 [label="行业覆盖", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    K7 [label="更新频率", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    K8 [label="市场衔接", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    {{rank=same; K1; K2; K3; K4; K5; K6; K7; K8;}}
    K1 -> K2 -> K3 -> K4 -> K5 -> K6 -> K7 -> K8 [style=invis];
  }}
  ISGI [label="分维国际标准差距指数\\nISGI_k = (S_k^int － S_k^CN) / S_k^int，k=1,…,8", fillcolor="{C['ltteal']}", color="{C['teal']}", fontsize=13];
  CIAI [label="综合国际适配性指数\\nCIAI = 1 － Σ π_k·ISGI_k（π_k 为维度权重）\\n行业测算：钢铁/铝/水泥/化肥/化工/氢能", fillcolor="{C['ltgold']}", color="{C['gold']}", fontsize=13];
  TH [label="适配调节系数 θ_j\\n（决定中国碳价被欧盟认可的折算比例）", fillcolor="{C['ltorange']}", color="{C['orange']}"];
  IO [label="动态投入产出模型\\n碳关税　τ_j = (P^EU － θ_j·P^CN)·e_j·ρ_j·X_j", fillcolor="{C['ltorange']}", color="{C['orange']}", fontsize=13];
  OUT [label="CBAM 情景模拟（2026—2030）\\n碳关税负担·高碳行业产出损失·出口竞争力影响", fillcolor="{C['ltred']}", color="{C['red']}", fontsize=13];
  FB [label="适配改进路径：对标改造·互认谈判·数据质量提升\\n（反馈第9章国际衔接接口设计）", style="rounded,filled,dashed", fillcolor="white", color="{C['red']}", fontcolor="{C['red']}"];
  K2 -> ISGI [ltail=cluster_dim]; K7 -> ISGI [ltail=cluster_dim];
  ISGI -> CIAI [label="π_k 加权集成"];
  CIAI -> TH; TH -> IO; IO -> OUT;
  OUT -> FB [style=dashed, color="{C['red']}"];
'''
    render(d, 'fig12_1')


# --------------------------------------------------- 图13.1 比较制度分析框架（matplotlib）
def fig13_1():
    fig, ax = canvas(9.2, 6.2, 112, 76)
    hdrs = [('中国体系', 26, C['ltred'], PAL['red']),
            ('欧盟体系', 55, C['ltblue'], PAL['blue']),
            ('ISO 国际体系', 84, C['ltteal'], PAL['teal'])]
    cw = 27
    for nm, x, fc, ec in hdrs:
        bx(ax, x, 64, cw, 7, nm, fc=ec, ec=ec, fs=9.5, tc='white', bold=True, pad=0.35)
    dims = [('体系架构', 52, ['政府主导·四层级\n（国标/行标/地标/团标）', '法规嵌入式\n指令＋条例＋协调标准（EN）', '国际共识型\nTC 技术委员会主导']),
            ('覆盖范围', 40, ['生产端密集\n碳核算·碳吸收端薄弱', '全生命周期覆盖\n产品—组织—金融贯通', '方法学通用框架\nISO 14060 族·14067 等']),
            ('技术严格程度', 28, ['中等·部分指标宽松\n更新周期较长', '严格·动态收紧\nCBAM 缺省值从严设定', '基准性要求\n提供全球最低共识']),
            ('制度机制', 16, ['行政推动\n强制与推荐双轨并行', '法律强制＋市场机制\nETS·CBAM 联动执行', '自愿采用\n采标与互认的基础平台'])]
    for nm, y, cells in dims:
        bx(ax, 2, y, 21, 10, nm, fc=C['ltgray'], ec=PAL['gray'], fs=8.5, bold=True, pad=0.35)
        for (hn, x, fc, ec), cell in zip(hdrs, cells):
            bx(ax, x, y, cw, 10, cell, fc=fc, ec=ec, fs=7, lw=0.9, pad=0.35)
    for _, x, fc, ec in hdrs:
        arr(ax, (x + cw / 2, 63.6), (x + cw / 2, 62.6), c=ec, lw=1.2, ms=9)
    bx(ax, 23, 3, 66, 8, '四维度逐项比较 → 识别中外制度差异与国际适配障碍\n（衔接扎根理论访谈编码，见图13.2）',
       fc=C['ltgold'], ec=PAL['gold'], fs=8, pad=0.4)
    arr(ax, (56, 15.6), (56, 11.6), c=PAL['gold'], lw=1.5)
    save(fig, f'{FIG}/fig13_1.png')


# --------------------------------------------------- 图13.2 扎根理论编码结构（graphviz）
def fig13_2():
    cs = R['cases']
    iv = cs['interviews']
    cd = cs['coding']
    ct = cs['categories']
    ntot = iv['steel'] + iv['alu'] + iv['fert']
    d = f'''
  rankdir=LR; nodesep=0.28; ranksep=0.55; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12, margin="0.14,0.08"];
  edge [color="{C['gray']}", arrowsize=0.75, fontsize=10.5, fontcolor="{C['gray']}"];
  SRC [label="访谈资料\\n钢铁 {iv['steel']} 人·铝 {iv['alu']} 人·化肥 {iv['fert']} 人\\n（共 {ntot} 位，NVivo 14）", fillcolor="{C['ltgray']}", color="{C['gray']}"];
  OPEN [label="开放式编码\\n逐句概念化\\n{cd['open_codes']} 个初始概念", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  AX [label="主轴编码\\n归并聚类\\n{cd['axial']} 个副范畴", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  subgraph cluster_core {{ label="选择性编码：{cd['core']} 大核心范畴（括号内为参考点频次）"; style=dashed; color="{C['red']}"; fontcolor="{C['red']}"; fontsize=12;
    G1 [label="数据基础障碍（{ct['data']}）\\n计量体系不全·因子库缺失", fillcolor="{C['ltred']}", color="{C['red']}"];
    G2 [label="制度衔接障碍（{ct['inst']}）\\n规则不互认·核查体系差异", fillcolor="{C['ltred']}", color="{C['red']}"];
    G3 [label="认知—能力障碍（{ct['cap']}）\\n人才与核算能力不足", fillcolor="{C['ltred']}", color="{C['red']}"];
    G4 [label="话语权障碍（{ct['voice']}）\\n国际标准参与度低", fillcolor="{C['ltred']}", color="{C['red']}"]; }}
  subgraph cluster_path {{ label="国际适配提升路径模型"; style=dashed; color="{C['green']}"; fontcolor="{C['green']}"; fontsize=12;
    P1 [label="① 数据基础夯实", fillcolor="{C['ltgreen']}", color="{C['green']}"];
    P2 [label="② 核算能力提升", fillcolor="{C['ltgreen']}", color="{C['green']}"];
    P3 [label="③ 认证互认突破", fillcolor="{C['ltgreen']}", color="{C['green']}"];
    P4 [label="④ 话语权提升", fillcolor="{C['ltgreen']}", color="{C['green']}"]; }}
  SAT [label="理论饱和度检验：预留 6 份\\n访谈复检，未出现新范畴", shape=note, style=filled, fillcolor="{C['ltgray']}", color="{C['gray']}", fontsize=10.5];
  {{rank=same; G1; G3; G2; G4;}}
  {{rank=same; P1; P2; P3; P4;}}
  SRC -> OPEN -> AX;
  AX -> G1; AX -> G3; AX -> G2; AX -> G4;
  G1 -> P1; G3 -> P2; G2 -> P3; G4 -> P4;
  G3 -> P3 [style=invis, weight=40]; G2 -> P2 [style=invis, weight=40];
  P1 -> P2 [color="{C['green']}", penwidth=1.6];
  P2 -> P3 [color="{C['green']}", penwidth=1.6];
  P3 -> P4 [color="{C['green']}", penwidth=1.6];
  P4 -> P1 [style=dashed, color="{C['red']}", fontcolor="{C['red']}", label="话语权反哺\n数据规则制定", constraint=false];
  AX -> SAT [style=dotted, dir=none];
'''
    render(d, 'fig13_2')


# --------------------------------------------------- 图14.1 政策体系框架（graphviz）
def fig14_1():
    d = f'''
  rankdir=TB; nodesep=0.26; ranksep=0.5; compound=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  BASE [label="研究结论支撑：演化机理（第5—7章）·体系构建（第8—10章）·适配评估（第11—13章）", fillcolor="{C['ltgray']}", color="{C['gray']}", fontsize=12];
  GOAL [label="总体目标：“十五五”时期建成支撑“双碳”、国际认可的绿色低碳标准体系", fillcolor="{C['ltred']}", color="{C['red']}", fontsize=14];
  subgraph cluster_s {{ label="支柱一：供给侧·补短板"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12.5;
    S1 [label="加快碳吸收·负排放标准供给\\n（碳汇计量·CCUS，错配缺口 0.58）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    S2 [label="碳核算·碳足迹标准全覆盖\\n对标 ISO 14064/14067", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    S3 [label="培育高质量团体标准\\n畅通采信转化通道", fillcolor="{C['ltblue']}", color="{C['blue']}"]; }}
  subgraph cluster_e {{ label="支柱二：执行侧·强激励"; style=dashed; color="{C['teal']}"; fontcolor="{C['teal']}"; fontsize=12.5;
    E1 [label="激励相容机制：补贴·绿色采购\\n金融支持与标准实施联动", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    E2 [label="央地协同与跨部门协调\\n降低协调失灵损失（27.2%）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    E3 [label="标准动态更新机制\\n触发阈值 TPD*=0.30", fillcolor="{C['ltteal']}", color="{C['teal']}"]; }}
  subgraph cluster_i {{ label="支柱三：国际侧·提话语权"; style=dashed; color="{C['gold']}"; fontcolor="{C['gold']}"; fontsize=12.5;
    I1 [label="深度参与 ISO/IEC 治理\\n牵头优势领域国际提案", fillcolor="{C['ltgold']}", color="{C['gold']}"];
    I2 [label="CBAM 核算规则对接\\n数据互认与 θ 提升", fillcolor="{C['ltgold']}", color="{C['gold']}"];
    I3 [label="“一带一路”绿色标准\\n软联通与集体发声", fillcolor="{C['ltgold']}", color="{C['gold']}"]; }}
  OUT [label="预期政策效果：供需错配收敛·执行效率 TE 提升·国际适配性 CIAI 提升·碳关税负担下降", fillcolor="{C['ltgreen']}", color="{C['green']}", fontsize=13];
  S1 -> S2 -> S3 [style=invis];
  E1 -> E2 -> E3 [style=invis];
  I1 -> I2 -> I3 [style=invis];
  BASE -> GOAL;
  GOAL -> S1 [lhead=cluster_s]; GOAL -> E1 [lhead=cluster_e]; GOAL -> I1 [lhead=cluster_i];
  S3 -> OUT [ltail=cluster_s]; E3 -> OUT [ltail=cluster_e]; I3 -> OUT [ltail=cluster_i];
  OUT -> GOAL [style=dashed, color="{C['red']}", fontcolor="{C['red']}", label="评估—反馈—迭代", constraint=false];
'''
    render(d, 'fig14_1')


ALL = [fig1_1, fig1_2, fig2_1, fig3_1, fig3_3, fig4_1, fig5_1, fig6_1, fig7_1,
       fig8_1, fig9_1, fig9_2, fig9_4, fig10_1, fig10_2, fig11_1, fig12_1,
       fig13_1, fig13_2, fig14_1]

if __name__ == '__main__':
    for f in ALL:
        f()
    print('diagrams done:', len(ALL))
