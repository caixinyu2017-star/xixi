# -*- coding: utf-8 -*-
"""前半部机制图（D 型，9 幅）：fig1_1 fig1_2 fig2_2 fig4_2 fig4_4 fig5_1 fig6_1 fig7_1 fig8_1。
graphviz（正交/折线直连）+ matplotlib 手绘（直线，rad=0），中文出版级。
铁律：图内不写图名/图注/资料来源；全部中文标签；直线或正交折线；浅色填充+深色描边。"""
import json
import os
import subprocess

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

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
def render(dot, name, engine='dot', dpi=300, splines='ortho'):
    """学术风格：正交直线连线（splines=ortho/polyline），不用曲线；避免交叠。"""
    dot = f'digraph G {{\n  graph [fontname="{FN}", dpi={dpi}, splines={splines}];\n' \
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
  rankdir=TB; nodesep=0.3; ranksep=0.48; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.14,0.08"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  P [label="现实问题：人工智能开发应用领域需求爆发、青年科技人才供需结构性错配背景下，\\n如何构建供需适配的产教融合培育机制？", fillcolor="{C['ltorange']}", color="{C['orange']}", fontsize=13.5];
  subgraph cluster_q {{ label="三个科学问题"; style=dashed; color="{C['red']}"; fontcolor="{C['red']}"; fontsize=12;
    Q1 [label="问题一（刻画需求）\\n能力需求结构是什么？\\n规模与结构如何演化？", fillcolor="{C['ltred']}", color="{C['red']}"];
    Q2 [label="问题二（解构供给）\\n培养体系如何生产能力？\\n产教融合投入如何起作用？", fillcolor="{C['ltred']}", color="{C['red']}"];
    Q3 [label="问题三（匹配机制）\\n错配如何测度？如何设计\\n激励相容的培育机制？", fillcolor="{C['ltred']}", color="{C['red']}"]; }}
  subgraph cluster_d {{ label="需方模块（第3、5—6章）"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12;
    D1 [label="产业发展与人才需求格局\\n典型事实（第3章）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    D2 [label="岗位能力需求识别：五层能力\\n权重与 JD 指数（第5章）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    D3 [label="需求规模动态预测：弹性模型\\n＋GM(1,1)三情景（第6章）", fillcolor="{C['ltblue']}", color="{C['blue']}"]; }}
  subgraph cluster_s {{ label="供方模块（第4、7章）"; style=dashed; color="{C['teal']}"; fontcolor="{C['teal']}"; fontsize=12;
    S1 [label="供给体系与产教融合\\n制度演进（第4章）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    S2 [label="教育生产函数与培养效率\\nK·L·F→Q→TE（第7章）", fillcolor="{C['ltteal']}", color="{C['teal']}"]; }}
  subgraph cluster_m {{ label="匹配模块（第8—9章）"; style=dashed; color="{C['gold']}"; fontcolor="{C['gold']}"; fontsize=12;
    M1 [label="技能错配测度 SMI\\n与匹配效率（第8章）", fillcolor="{C['ltgold']}", color="{C['gold']}"];
    M2 [label="高校—企业—政府三方\\n演化博弈（第9章）", fillcolor="{C['ltgold']}", color="{C['gold']}"]; }}
  MECH [label="培育机制总体设计（第10章）：需求牵引·能力本位·激励相容三项原则\\n×五大子机制（需求传导／协同培养／师资共建／评价反馈／利益分配）", fillcolor="{C['ltred']}", color="{C['red']}", fontsize=13];
  SIM [label="机制运行：系统动力学仿真\\n与动态调整（第11章）", fillcolor="{C['ltpurple']}", color="{C['purple']}"];
  subgraph cluster_e {{ label="机制验证（第12—13章）"; style=dashed; color="{C['green']}"; fontcolor="{C['green']}"; fontsize=12;
    EV [label="效能评估：培养效率与\\n就业匹配质量（第12章）", fillcolor="{C['ltgreen']}", color="{C['green']}"];
    CASE [label="典型案例与质性研究\\n三角验证（第13章）", fillcolor="{C['ltgreen']}", color="{C['green']}"]; }}
  CC [label="研究结论与政策建议：需求侧·供给侧·匹配侧协同发力（第14章）", fillcolor="{C['ltgreen']}", color="{C['green']}", fontsize=13];
  {{rank=same; Q1; Q2; Q3;}} Q1 -> Q2 -> Q3 [style=invis];
  {{rank=same; D1; S1;}} {{rank=same; D2; S2;}} {{rank=same; EV; CASE;}}
  EV -> CASE [style=invis];
  P -> Q1; P -> Q2; P -> Q3;
  Q1 -> D1 [lhead=cluster_d];
  Q2 -> S1 [lhead=cluster_s];
  Q3 -> M1 [lhead=cluster_m];
  D1 -> D2; D2 -> D3;
  S1 -> S2;
  D3 -> M1 [ltail=cluster_d, lhead=cluster_m, label="需方结构与规模"];
  S2 -> M1 [ltail=cluster_s, lhead=cluster_m, label="供方能力供给"];
  M1 -> M2 [label="错配格局→博弈情境"];
  M2 -> MECH [ltail=cluster_m, label="激励相容条件"];
  MECH -> SIM;
  SIM -> EV [lhead=cluster_e];
  CASE -> CC [ltail=cluster_e];
  EV -> MECH [style=dashed, color="{C['red']}", fontcolor="{C['red']}",
              label="效能评估反馈机制优化", constraint=false];
'''
    render(d, 'fig1_1', splines='polyline')


# --------------------------------------------------- 图1.2 全书结构（graphviz 树形）
def fig1_2():
    ch = {1: '导论', 2: '理论基础与文献综述',
          3: '人工智能产业发展与青年科技人才需求格局',
          4: '青年科技人才供给体系与产教融合的制度演进',
          5: '需方模型：岗位能力需求结构的识别与测度',
          6: '需方模型：人才需求规模的动态预测',
          7: '供方模型：教育生产函数与产教融合培养效率',
          8: '供需匹配模型：技能错配测度与匹配效率',
          9: '供需匹配模型：高校—企业—政府三方演化博弈',
          10: '产教融合培育机制的总体设计',
          11: '培育机制运行的系统动力学仿真与动态调整',
          12: '培育机制效能评估：培养效率与就业匹配质量',
          13: '典型案例与质性研究',
          14: '研究结论、政策建议与研究展望'}
    parts = [('P1', '第一篇  总起\\n（第1—2章）', [1, 2], 'blue'),
             ('P2', '第二篇  需方研究\\n（第3、5—6章）', [3, 5, 6], 'teal'),
             ('P3', '第三篇  供方研究\\n（第4、7章）', [4, 7], 'gold'),
             ('P4', '第四篇  匹配与机制设计\\n（第8—11章）', [8, 9, 10, 11], 'purple'),
             ('P5', '第五篇  评估与结论\\n（第12—14章）', [12, 13, 14], 'green')]
    lines = ['  rankdir=LR; nodesep=0.12; ranksep=0.65;',
             '  node [shape=box, style="rounded,filled", fontsize=12, margin="0.14,0.07"];',
             f'  edge [color="{C["gray"]}", arrowsize=0.7];',
             f'  ROOT [label="《面向人工智能开发应用领域需求的\\n青年科技人才产教融合培育机制研究》\\n需求刻画·供给解构·匹配机制·效能评估", '
             f'fillcolor="{C["ltorange"]}", color="{C["orange"]}", fontsize=13.5];']
    for pid, plab, chs, col in parts:
        lines.append(f'  {pid} [label="{plab}", fillcolor="{C["lt" + col]}", color="{C[col]}", fontsize=12.5];')
        lines.append(f'  ROOT -> {pid};')
        for k in chs:
            lines.append(f'  C{k} [label="第{k}章  {ch[k]}", fillcolor="{C["ltgray"]}", color="{C[col]}", fontsize=11];')
            lines.append(f'  {pid} -> C{k};')
    render('\n'.join(lines), 'fig1_2')


# --------------------------------------------------- 图2.2 理论基础与研究框架（graphviz）
def fig2_2():
    d = f'''
  rankdir=TB; nodesep=0.4; ranksep=0.85; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  subgraph cluster_t {{ label="理论基础"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12.5;
    T1 [label="人力资本理论\\nSchultz·Becker·Mincer\\n能力投资与收益", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    T2 [label="搜寻匹配理论\\nDMP·匹配函数\\n摩擦、错配与空缺", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    T3 [label="三螺旋理论\\nEtzkowitz—Leydesdorff\\n校—企—政协同", fillcolor="{C['ltpurple']}", color="{C['purple']}"];
    T4 [label="技能形成理论\\nBusemeyer 等\\n集体技能形成体制", fillcolor="{C['ltgold']}", color="{C['gold']}"]; }}
  subgraph cluster_f {{ label="“三位一体”研究框架"; style=dashed; color="{C['orange']}"; fontcolor="{C['orange']}"; fontsize=12.5;
    F1 [label="需求刻画\\n（认识需方）\\n第3、5—6章", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    F2 [label="供给解构\\n（认识供方）\\n第4、7章", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    F3 [label="匹配测度与机制设计\\n（打通供需）\\n第8—11章", fillcolor="{C['ltorange']}", color="{C['orange']}"]; }}
  G [label="研究目标：构建供需适配、激励相容的青年科技人才产教融合培育机制\\n（效能评估与案例验证：第12—13章）", fillcolor="{C['ltgreen']}", color="{C['green']}", fontsize=13];
  {{rank=same; T1; T2; T3; T4;}} T1 -> T2 -> T3 -> T4 [style=invis];
  {{rank=same; F1; F2; F3;}}
  T1 -> F1 [label="人力资本溢价\\n→需求信号"];
  T1 -> F2 [label="教育投资\\n→能力生产"];
  T2 -> F3 [label="匹配函数·贝弗里奇曲线\\n→错配与匹配效率"];
  T3 -> F3 [label="三方协同\\n→演化博弈"];
  T4 -> F2 [label="技能形成体制\\n→培养模式"];
  T4 -> F3 [label="利益协调\\n→成本分担"];
  F1 -> F2 [label="需求基准→供给对标", color="{C['orange']}", penwidth=1.5, fontcolor="{C['orange']}"];
  F2 -> F3 [label="供需两侧向量对接", color="{C['orange']}", penwidth=1.5, fontcolor="{C['orange']}"];
  F1 -> G; F2 -> G; F3 -> G;
  G -> F3 [style=dashed, color="{C['red']}", fontcolor="{C['red']}", label="评估反馈优化", constraint=false];
'''
    render(d, 'fig2_2', splines='polyline')


# --------------------------------------------------- 图4.2 产教融合政策演进时间轴（matplotlib）
def fig4_2():
    fig, ax = plt.subplots(figsize=(9.0, 4.4))
    ax.set_xlim(2011.9, 2026.6)
    ax.set_ylim(-4.7, 4.7)
    ax.axis('off')
    ax.grid(False)
    stages = [(2012.5, 2016.5, C['ltblue'], PAL['blue'], '探索期\n（2013—2016）'),
              (2016.5, 2020.5, C['ltteal'], PAL['teal'], '制度化期\n（2017—2020）'),
              (2020.5, 2025.9, C['ltorange'], PAL['orange'], '深化期\n（2021—2025）')]
    ax.annotate('', xy=(2026.5, 0), xytext=(2012.1, 0),
                arrowprops=dict(arrowstyle='-|>', color='#444444', lw=1.2), zorder=1)
    for x0, x1, fc, ec, lab in stages:
        ax.add_patch(Rectangle((x0, -0.5), x1 - x0, 1.0, fc=fc, ec=ec, lw=1.0, zorder=2))
        ax.text((x0 + x1) / 2, 0, lab, ha='center', va='center', fontsize=8,
                color=ec, fontweight='bold', linespacing=1.3, zorder=3)
    ax.text(2026.5, -0.85, '年份', fontsize=7.5, ha='right', color='#444444')
    events = [  # (年份, 文本, 竖直高度[含正负号], 颜色)
        (2013, '应用型转型试点启动\n应用技术大学联盟成立', 1.75, PAL['blue']),
        (2015, '《关于引导部分地方普通本科\n高校向应用型转变的指导意见》', -1.75, PAL['blue']),
        (2017, '《关于深化产教融合的若干意见》\n（国办发〔2017〕95号）', 3.2, PAL['teal']),
        (2019, '《国家职业教育改革实施方案》\n《国家产教融合建设试点实施方案》', -3.2, PAL['teal']),
        (2020, '《现代产业学院建设指南》\n《特色化示范性软件学院建设指南》', 1.75, PAL['teal']),
        (2021, '“101计划”启动\n首批产教融合试点城市公布', -1.75, PAL['orange']),
        (2022, '新修订《职业教育法》施行\n产教融合写入法律', 3.2, PAL['orange']),
        (2023, '《普通高等教育学科专业设置\n调整优化改革方案》', -3.2, PAL['orange']),
        (2024, '九部门《加快数字人才培育\n支撑数字经济发展行动方案》', 1.75, PAL['orange'])]
    for yr, lab, h, cc in events:
        sgn = 1 if h > 0 else -1
        ax.plot([yr, yr], [0.55 * sgn, h - 0.52 * sgn], color=cc, lw=1.0, zorder=2)
        ax.plot([yr], [0.55 * sgn], marker='o', ms=4.5, color=cc, zorder=4)
        ax.text(yr, h, f'{yr}年\n{lab}', ha='center', va='center', fontsize=6.8,
                color='#1a1a1a', linespacing=1.32, zorder=3,
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=cc, lw=0.9))
    save(fig, f'{FIG}/fig4_2.png')
    print('ok fig4_2')


# --------------------------------------------------- 图4.4 校企合作形态谱系（matplotlib）
def fig4_4():
    fig, ax = canvas(10.0, 3.5, 100, 35)
    forms = [('讲座与实习', '企业讲座·认知实习\n信息交换界面', '#EFF4FA'),
             ('共建课程与教材', '产业案例进课堂\n协同育人项目', '#DCE6F1'),
             ('现代产业学院', '共建二级学院\n项目制·双导师制', '#C9D9EC'),
             ('联合实验室', '校企联合研发\n实训与攻关平台', '#AFC7E2'),
             ('订单式培养', '定向招生·定向就业\n成本分担·入职衔接', '#97B3D7')]
    w, h, y0, gap = 17.0, 12.0, 14.0, 3.1
    x0 = (100 - 5 * w - 4 * gap) / 2
    for i, (nm, sub, fc) in enumerate(forms):
        xx = x0 + i * (w + gap)
        p = FancyBboxPatch((xx, y0), w, h, boxstyle='round,pad=0.5', fc=fc,
                           ec=PAL['blue'], lw=1.0 + 0.15 * i, zorder=2)
        ax.add_patch(p)
        txt(ax, xx + w / 2, y0 + h - 2.6, nm, fs=8.2, bold=True, c='#12233D')
        txt(ax, xx + w / 2, y0 + 3.6, sub, fs=6.6, c='#333333')
        if i < 4:
            arr(ax, (xx + w + 0.6, y0 + h / 2), (xx + w + gap - 0.6, y0 + h / 2),
                c=PAL['gray'], lw=1.3, ms=11)
    # 底部：合作深度递增箭头（水平直线）
    arr(ax, (x0 + 1, 6.2), (100 - x0 - 1, 6.2), c=PAL['blue'], lw=2.2, ms=16)
    txt(ax, 50, 3.0, '合作深度递增：资源投入加大·制度化程度提高·校企利益绑定加深',
        fs=7.6, c=PAL['blue'], bold=True)
    txt(ax, x0 + 3.5, 8.6, '浅层合作', fs=7, c=PAL['gray'])
    txt(ax, 100 - x0 - 3.5, 8.6, '深度融合', fs=7, c=PAL['gray'])
    # 顶部：合作界面类型（与形态一一对应）
    faces = ['信息互通', '课程嵌入', '组织共建', '研发共创', '雇佣绑定']
    for i, fl in enumerate(faces):
        xx = x0 + i * (w + gap) + w / 2
        txt(ax, xx, y0 + h + 3.6, fl, fs=7, c=PAL['gray'])
        ax.plot([xx, xx], [y0 + h + 1.0, y0 + h + 2.3], color=PAL['gray'],
                lw=0.8, ls=':', zorder=1)
    save(fig, f'{FIG}/fig4_4.png')
    print('ok fig4_4')


# --------------------------------------------------- 图5.1 岗位能力需求识别框架（graphviz）
def fig5_1():
    ds = R['ability']['dict_stats']
    ov = R['ability']['overall']
    d = f'''
  rankdir=TB; nodesep=0.3; ranksep=0.5; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  SRC [label="招聘大数据语料：{ds['corpus_wan']}万条 JD 文本\\n五大岗位族（算法／模型工程／数据／产品应用／治理安全），2018—2025年", fillcolor="{C['ltorange']}", color="{C['orange']}", fontsize=13];
  TM [label="文本挖掘\\n分词与短语抽取·TF-IDF\\n能力词共现网络", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  DICT [label="能力词典构建\\n{ds['vocab']} 个词条·五层归类\\n双人标注一致性 κ={ds['kappa']}", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  MAP [label="能力条目识别与词频—权重估计\\nJD 文本→五层能力模型映射", fillcolor="{C['ltteal']}", color="{C['teal']}", fontsize=13];
  subgraph cluster_w {{ label="五层能力需求权重 w_k（总体，行和=1）"; style=dashed; color="{C['gold']}"; fontcolor="{C['gold']}"; fontsize=12;
    W1 [label="基础理论层\\n{ov['base']:.2f}", fillcolor="{C['ltgold']}", color="{C['gold']}", fontsize=11.5];
    W2 [label="技术方法层\\n{ov['tech']:.2f}", fillcolor="{C['ltgold']}", color="{C['gold']}", fontsize=11.5];
    W3 [label="工程实践层\\n{ov['eng']:.2f}", fillcolor="{C['ltgold']}", color="{C['gold']}", fontsize=11.5];
    W4 [label="创新应用层\\n{ov['innov']:.2f}", fillcolor="{C['ltgold']}", color="{C['gold']}", fontsize=11.5];
    W5 [label="伦理治理层\\n{ov['ethic']:.2f}", fillcolor="{C['ltgold']}", color="{C['gold']}", fontsize=11.5]; }}
  MTX [label="分岗位族权重矩阵（5岗位族×5能力层）\\n刻画岗位间能力需求结构差异", fillcolor="{C['ltgold']}", color="{C['gold']}"];
  JDX [label="岗位需求指数 JD_jt\\n分岗位族需求热度（2018年=100）", fillcolor="{C['ltpurple']}", color="{C['purple']}"];
  D [label="需方能力需求向量 D_t（能力维度×岗位族）", fillcolor="{C['ltgreen']}", color="{C['green']}", fontsize=13.5];
  FB [label="输入第6章需求预测·第8章错配测度\\n第10章需求传导机制", style="rounded,filled,dashed", fillcolor="white", color="{C['red']}", fontcolor="{C['red']}"];
  {{rank=same; TM; DICT;}} TM -> DICT [style=invis];
  {{rank=same; W1; W2; W3; W4; W5;}} W1 -> W2 -> W3 -> W4 -> W5 [style=invis];
  {{rank=same; MTX; JDX;}} MTX -> JDX [style=invis];
  SRC -> TM; SRC -> DICT;
  SRC -> JDX [label="岗位需求量统计"];
  TM -> MAP; DICT -> MAP;
  MAP -> W3 [lhead=cluster_w];
  W3 -> MTX [ltail=cluster_w, label="分岗位族分解"];
  MTX -> D; JDX -> D [label="需求热度加权"];
  D -> FB [style=dashed, color="{C['red']}"];
'''
    render(d, 'fig5_1')


# --------------------------------------------------- 图6.1 需求预测框架（graphviz）
def fig6_1():
    fc = R['forecast']
    eta, gm, sc, bj = fc['eta'], fc['gm'], fc['scenario'], fc['by_job_2030']
    d = f'''
  rankdir=TB; nodesep=0.32; ranksep=0.5; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  Y [label="产业规模序列 Y_t\\n中国AI核心产业规模（亿元）", fillcolor="{C['ltgray']}", color="{C['gray']}"];
  H [label="人才需求历史序列 D_t\\n招聘大数据口径（第5章）", fillcolor="{C['ltgray']}", color="{C['gray']}"];
  subgraph cluster_a {{ label="通道一：产业弹性模型"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12;
    A1 [label="对数需求方程\\nlnD_t = c + η·lnY_t", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    A2 [label="弹性估计 η={eta['coef']}***\\n（t={eta['t']:.1f}，R²={eta['R2']}，N={eta['N']}）", fillcolor="{C['ltblue']}", color="{C['blue']}"]; }}
  subgraph cluster_b {{ label="通道二：GM(1,1) 灰色预测"; style=dashed; color="{C['teal']}"; fontcolor="{C['teal']}"; fontsize=12;
    B1 [label="累加生成（AGO）\\n白化方程 dx/dt＋a·x＝b", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    B2 [label="参数 a={gm['a']}，b={gm['b']}\\n精度检验 C={gm['C']}，P={gm['P']}（良好）", fillcolor="{C['ltteal']}", color="{C['teal']}"]; }}
  X [label="双通道交叉验证与组合预测", fillcolor="{C['ltpurple']}", color="{C['purple']}", fontsize=13];
  SCEN [label="情景修正：产业增速×政策强度\\n基准／加速／放缓三情景", fillcolor="{C['ltorange']}", color="{C['orange']}", fontsize=13];
  OUT [label="青年AI人才需求预测（2026—2035年，万人）\\n基期2025年 {sc['base']['2025']:.0f} → 2030年基准 {sc['base']['2030']:.0f}\\n2035年：基准 {sc['base']['2035']:.0f}／加速 {sc['fast']['2035']:.0f}／放缓 {sc['slow']['2035']:.0f}", fillcolor="{C['ltgreen']}", color="{C['green']}", fontsize=13];
  JOB [label="分岗位族分解（2030年基准，万人）\\n算法 {bj['algo']}·模型工程 {bj['meng']}·数据 {bj['data']}·产品应用 {bj['prod']}·治理安全 {bj['gov']}", fillcolor="{C['ltgold']}", color="{C['gold']}"];
  FB [label="输出：第8章供需比较基准\\n第11章系统动力学需求输入", style="rounded,filled,dashed", fillcolor="white", color="{C['red']}", fontcolor="{C['red']}"];
  {{rank=same; Y; H;}} Y -> H [style=invis];
  {{rank=same; A1; B1;}} {{rank=same; A2; B2;}} {{rank=same; JOB; FB;}}
  Y -> A1; H -> A1; H -> B1;
  A1 -> A2; B1 -> B2;
  A2 -> X; B2 -> X;
  X -> SCEN; SCEN -> OUT;
  OUT -> JOB;
  OUT -> FB [style=dashed, color="{C['red']}"];
'''
    render(d, 'fig6_1')


# --------------------------------------------------- 图7.1 教育生产函数逻辑（matplotlib）
def fig7_1():
    pf = R['prodfn']
    ols, sfa = pf['ols'], pf['sfa']
    te = sfa['te']
    fig, ax = canvas(8.8, 5.8, 100, 66)
    # 产教融合投入 F 的三要素（左列）
    subs = [('企业参与度 ENG', 26), ('双师双能比例 DTR', 17), ('实训基地强度 PRA', 8)]
    for nm, yy in subs:
        bx(ax, 2, yy, 16, 6, nm, fc=C['ltteal'], ec=PAL['teal'], fs=7.3)
    # 三投入（中左列）
    bx(ax, 24, 47, 21, 10, '物质资本投入 K\n生均经费·实验设备', fc=C['ltblue'], ec=PAL['blue'], fs=8)
    bx(ax, 24, 33, 21, 10, '师资投入 L\n专任教师规模与结构', fc=C['ltblue'], ec=PAL['blue'], fs=8)
    bx(ax, 24, 14, 21, 15, '产教融合投入 F\n综合指数\n（熵权法合成三要素）', fc=C['ltteal'], ec=PAL['teal'], fs=8, lw=1.5)
    arr(ax, (18, 29), (24, 25.5), c=PAL['teal'], lw=1.2)
    arr(ax, (18, 20), (24, 21.5), c=PAL['teal'], lw=1.2)
    arr(ax, (18, 11), (24, 17.5), c=PAL['teal'], lw=1.2)
    # 生产函数（中心）
    bx(ax, 52, 31, 28, 15,
       '教育生产函数（院校面板估计）\nlnQ = lnA + α·lnK + β·lnL + γ·lnF\nR²=%.2f，N=%d' % (ols['R2'], ols['N']),
       fc=C['ltorange'], ec=PAL['orange'], fs=8, lw=1.6, bold=False)
    arr(ax, (45, 52), (52, 42), c=PAL['blue'], lw=1.4)
    txt(ax, 49.5, 49.8, 'α=%.3f***' % ols['lnK']['coef'], fs=7, c=PAL['blue'])
    arr(ax, (45, 38), (52, 38.5), c=PAL['blue'], lw=1.4)
    txt(ax, 48.5, 40.6, 'β=%.3f***' % ols['lnL']['coef'], fs=7, c=PAL['blue'])
    arr(ax, (45, 21.5), (52, 35), c=PAL['teal'], lw=1.6)
    txt(ax, 51, 25.8, 'γ=%.3f***' % ols['lnF']['coef'], fs=7, c=PAL['teal'])
    # 能力产出 Q（右上）
    bx(ax, 84, 33, 14.5, 11, '能力产出 Q\n毕业生五层能力\n结构向量', fc=C['ltgold'], ec=PAL['gold'], fs=7.5, lw=1.4)
    arr(ax, (80, 38.5), (84, 38.5), c=PAL['orange'], lw=1.6)
    # SFA 与效率（下行）
    bx(ax, 52, 7, 28, 14,
       '随机前沿分析（SFA）：v_it − u_it\nγ=%.2f，LR=%.1f\n无效率决定：ENG %.3f***\nDTR %.3f***·PRA %.3f***'
       % (sfa['gamma'], sfa['lr'], sfa['ineff']['ENG']['coef'],
          sfa['ineff']['DTR']['coef'], sfa['ineff']['PRA']['coef']),
       fc=C['ltpurple'], ec=PAL['purple'], fs=7, lw=1.4)
    arr(ax, (66, 31), (66, 21.6), c=PAL['purple'], lw=1.4)
    txt(ax, 71.5, 26.3, '前沿偏离分解', fs=7, c=PAL['purple'])
    # 三要素→无效率（正交折线，沿底部）
    ax.plot([10, 10, 62], [7.7, 3.2, 3.2], color=PAL['teal'], lw=1.2, ls='--', zorder=1)
    arr(ax, (62, 3.2), (62, 6.6), c=PAL['teal'], lw=1.2, ls='--', ms=10)
    txt(ax, 36, 5.0, '产教融合三要素显著降低培养无效率', fs=7, c=PAL['teal'])
    # 培养效率 TE（右下）
    bx(ax, 84, 9, 14.5, 11, '培养效率\nTE=exp(−u_it)\n均值 %.2f' % te['mean'],
       fc=C['ltgreen'], ec=PAL['green'], fs=7.5, lw=1.5)
    arr(ax, (80, 14.5), (84, 14.5), c=PAL['purple'], lw=1.6)
    txt(ax, 91.2, 5.4, '部属高校 %.2f·地方本科 %.2f\n高职高专 %.2f'
        % (te['by_type']['部属高校'], te['by_type']['地方本科'], te['by_type']['高职高专']),
        fs=6.4, c='#666666')
    save(fig, f'{FIG}/fig7_1.png')
    print('ok fig7_1')


# --------------------------------------------------- 图8.1 SMI 测度框架（graphviz）
def fig8_1():
    smi = R['smi']
    comp = smi['composite']
    d = f'''
  rankdir=TB; nodesep=0.35; ranksep=0.5; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  subgraph cluster_d {{ label="需求侧入口（第5章）"; style=dashed; color="{C['orange']}"; fontcolor="{C['orange']}"; fontsize=12;
    DW [label="五层能力需求权重 w_k\\n招聘大数据文本挖掘", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    DJ [label="岗位需求指数 JD_jt\\n分岗位族需求热度", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    DD [label="需方能力需求向量 D_kt", fillcolor="{C['orange']}", fontcolor="white", color="{C['orange']}", fontsize=13]; }}
  subgraph cluster_s {{ label="供给侧入口（第7章）"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12;
    SQ [label="教育生产函数能力产出\\n毕业生能力结构测评", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    SS [label="供方能力供给向量 Q_kt", fillcolor="{C['blue']}", fontcolor="white", color="{C['blue']}", fontsize=13]; }}
  MIS [label="技能错配指数　SMI_kt = (D_kt − Q_kt) / D_kt\\n＞0 短缺性错配；＜0 过剩性错配", fillcolor="{C['ltteal']}", color="{C['teal']}", fontsize=13.5];
  VER [label="纵向层次错配\\n学历／能力层级偏离\\n（学历高配与能力欠配并存）", fillcolor="{C['ltgold']}", color="{C['gold']}"];
  HOR [label="横向结构错配\\n能力维度×岗位族偏离\\n（工程实践层缺口最大 {smi['dim_2025']['eng']:.2f}）", fillcolor="{C['ltgold']}", color="{C['gold']}"];
  AGG [label="加权合成　SMI_t = Σ_k w_kt·SMI_kt（权重＝需求占比）\\n{list(comp)[0]}年 {comp['2018']:.2f} → {list(comp)[-1]}年 {comp['2025']:.2f}", fillcolor="{C['ltpurple']}", color="{C['purple']}", fontsize=13];
  OUT [label="错配格局：总量收敛、结构分化\\n模型工程（{smi['by_job_2025']['meng']:.2f}）与治理安全（{smi['by_job_2025']['gov']:.2f}）岗位族错配最深", fillcolor="{C['ltgreen']}", color="{C['green']}", fontsize=13];
  FB [label="反馈：第10章需求传导机制\\n与课程模块设计", style="rounded,filled,dashed", fillcolor="white", color="{C['red']}", fontcolor="{C['red']}"];
  {{rank=same; DW; DJ; SQ;}} DW -> DJ -> SQ [style=invis];
  {{rank=same; DD; SS;}} {{rank=same; VER; HOR;}}
  DW -> DD; DJ -> DD; SQ -> SS;
  DD -> MIS; SS -> MIS;
  MIS -> VER; MIS -> HOR;
  VER -> AGG; HOR -> AGG;
  AGG -> OUT;
  OUT -> FB [style=dashed, color="{C['red']}"];
'''
    render(d, 'fig8_1')


ALL = [fig1_1, fig1_2, fig2_2, fig4_2, fig4_4, fig5_1, fig6_1, fig7_1, fig8_1]

if __name__ == '__main__':
    for f in ALL:
        f()
    print('diagrams_a done:', len(ALL))
