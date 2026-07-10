# -*- coding: utf-8 -*-
"""机制图/示意图/框架图（graphviz 矢量图，中文）。章节编号命名。"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)
FN = 'WenQuanYi Zen Hei'
C = dict(blue='#1F4E79', ltblue='#DCE6F1', orange='#C55A11', ltorange='#FCE4D6',
         teal='#2E8B8B', ltteal='#D6EAEA', gold='#BF9000', ltgold='#FFF2CC',
         green='#548235', ltgreen='#E2EFDA', red='#A02020', ltred='#F8D7D7',
         gray='#7F7F7F', ltgray='#EDEDED', purple='#674EA7', ltpurple='#E6E0F0')


def render(dot, name, dpi=300):
    dot = f'digraph G {{\n  graph [fontname="{FN}", dpi={dpi}];\n' \
          f'  node [fontname="{FN}"];\n  edge [fontname="{FN}"];\n' + dot + '\n}\n'
    p = os.path.join(FIG, name + '.dot')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(dot)
    subprocess.run(['dot', '-Tpng', p, '-o', os.path.join(FIG, name + '.png')], check=True)
    os.remove(p)
    print('ok', name)


# --------------------------------------------------- 图1.1 研究技术路线
def roadmap():
    d = f'''
  rankdir=TB; nodesep=0.35; ranksep=0.45;
  node [shape=box, style="rounded,filled", fillcolor="{C['ltblue']}", color="{C['blue']}", fontsize=13, margin="0.14,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8];
  P [label="现实问题：地方保护与市场分割制约要素高效配置", fillcolor="{C['ltorange']}", color="{C['orange']}"];
  Q [label="核心问题：全国统一大市场建设如何影响要素配置效率？"];
  subgraph cluster_t {{ label="理论层（顶天）"; color="{C['blue']}"; fontcolor="{C['blue']}"; style=dashed;
    T1 [label="新概念：要素市场行政性分割\\n制度性配置楔子"];
    T2 [label="空间一般均衡模型\\n数理推导与命题"]; }}
  subgraph cluster_m {{ label="测度与实证层"; color="{C['teal']}"; fontcolor="{C['teal']}"; style=dashed;
    M1 [label="NUMI 六维测度体系\\n（省级2006—2023）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    M2 [label="要素错配与效率损失估计", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    M3 [label="基准回归·机制·异质性\\nIV·多期DID", fillcolor="{C['ltteal']}", color="{C['teal']}"]; }}
  subgraph cluster_p {{ label="政策层（立地）"; color="{C['green']}"; fontcolor="{C['green']}"; style=dashed;
    R1 [label="破除地方保护·要素市场化改革\\n统一制度·公平竞争", fillcolor="{C['ltgreen']}", color="{C['green']}"]; }}
  P->Q->T1->T2->M1->M2->M3->R1;
  T2->M3 [style=dotted, constraint=false, label="检验"];
'''
    render(d, 'fig1_1')


# --------------------------------------------------- 图2.1 理论分析框架
def framework():
    d = f'''
  rankdir=LR; nodesep=0.4; ranksep=0.7;
  node [shape=box, style="rounded,filled", fontsize=13, margin="0.16,0.1"];
  edge [color="{C['gray']}", arrowsize=0.85, fontsize=11, fontcolor="{C['gray']}"];
  A [label="全国统一大市场建设\\n（NUMI↑）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  W [label="制度性配置楔子\\nτ 及其离散度↓", fillcolor="{C['ltgold']}", color="{C['gold']}"];
  subgraph cluster_ch {{ label="传导机制"; style=dashed; color="{C['teal']}"; fontcolor="{C['teal']}";
    C1 [label="要素流动效应", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    C2 [label="竞争淘汰效应", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    C3 [label="创新激励效应", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    C4 [label="规模与专业化效应", fillcolor="{C['ltteal']}", color="{C['teal']}"]; }}
  E [label="要素配置效率↑\\nTFP↑", fillcolor="{C['ltgreen']}", color="{C['green']}"];
  O [label="高质量发展\\n区域协调·共同富裕", fillcolor="{C['ltorange']}", color="{C['orange']}"];
  A->W [label="降壁垒"];
  W->C1; W->C2; W->C3; W->C4;
  C1->E; C2->E; C3->E; C4->E;
  E->O;
  A->C1 [style=dotted, constraint=false];
'''
    render(d, 'fig2_1')


# --------------------------------------------------- 图3.5 市场分割制度成因
def seg_causes():
    d = f'''
  rankdir=TB; nodesep=0.3; ranksep=0.5;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.14,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8];
  ROOT [label="国内市场分割与地方保护", fillcolor="{C['ltred']}", color="{C['red']}", fontsize=14];
  F1 [label="财政分权与\\n地方政府竞争", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  F2 [label="以GDP为核心的\\n官员晋升激励", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  F3 [label="要素市场行政管制\\n（户籍·用地·金融）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  F4 [label="行政性垄断与\\n地方性法规壁垒", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  M1 [label="重复建设·产业同构"];
  M2 [label="地方保护·市场准入歧视"];
  M3 [label="要素跨区流动受阻"];
  OUT [label="要素错配·效率损失·全国大循环受阻", fillcolor="{C['ltorange']}", color="{C['orange']}", fontsize=13];
  ROOT->F1; ROOT->F2; ROOT->F3; ROOT->F4;
  F1->M1; F2->M2; F3->M3; F4->M2;
  M1->OUT; M2->OUT; M3->OUT;
'''
    render(d, 'fig3_5')


# --------------------------------------------------- 图4.1 理论机制传导
def theory_mech():
    d = f'''
  rankdir=TB; nodesep=0.45; ranksep=0.5;
  node [shape=box, style="rounded,filled", fontsize=13, margin="0.16,0.1"];
  edge [color="{C['blue']}", arrowsize=0.85, penwidth=1.3];
  UM [label="统一大市场建设：降低商品与要素流动壁垒\\nτ^G↓，τ^F↓", fillcolor="{C['ltblue']}", color="{C['blue']}", fontsize=13.5];
  subgraph cluster_1 {{ label="要素再配置"; style=dashed; color="{C['teal']}"; fontcolor="{C['teal']}";
    R1 [label="劳动·资本·土地·数据\\n由低效率部门流向高效率部门", fillcolor="{C['ltteal']}", color="{C['teal']}"]; }}
  subgraph cluster_2 {{ label="市场竞争"; style=dashed; color="{C['gold']}"; fontcolor="{C['gold']}";
    R2 [label="进入退出加剧·优胜劣汰\\n加成率离散度下降", fillcolor="{C['ltgold']}", color="{C['gold']}"]; }}
  subgraph cluster_3 {{ label="创新与专业化"; style=dashed; color="{C['purple']}"; fontcolor="{C['purple']}";
    R3 [label="市场规模扩大→分工深化\\n研发要素集聚·知识溢出", fillcolor="{C['ltpurple']}", color="{C['purple']}"]; }}
  WEDGE [label="边际收益离散度↓\\nVar(lnτ)↓", fillcolor="{C['ltorange']}", color="{C['orange']}", fontsize=13];
  TFP [label="全要素生产率与配置效率提升\\nln TFP = ln A − ½·Var(lnτ)·Θ", shape=box, style="rounded,filled", fillcolor="{C['ltgreen']}", color="{C['green']}", fontsize=13.5];
  UM->R1; UM->R2; UM->R3;
  R1->WEDGE; R2->WEDGE; R3->TFP;
  WEDGE->TFP;
'''
    render(d, 'fig4_1')


# --------------------------------------------------- 图5.1 NUMI 指标体系
def numi_tree():
    d = f'''
  rankdir=LR; nodesep=0.16; ranksep=0.6;
  node [shape=box, style="rounded,filled", fontsize=12, margin="0.13,0.07"];
  edge [color="{C['gray']}", arrowsize=0.7];
  ROOT [label="全国统一大市场\\n建设指数 NUMI", fillcolor="{C['ltblue']}", color="{C['blue']}", fontsize=13.5];
  D1 [label="商品市场一体化", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  D2 [label="劳动力市场一体化", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  D3 [label="资本市场一体化", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  D4 [label="土地市场一体化", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  D5 [label="技术与数据市场一体化", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  D6 [label="市场制度环境一体化", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  node [fillcolor="{C['ltgray']}", color="{C['gray']}", fontsize=10.5];
  I1 [label="相对价格方差(逆向)·省际贸易强度"];
  I2 [label="跨省流动人口占比·工资收敛·户籍开放度"];
  I3 [label="信贷可得性收敛·资本回报离散度(逆向)"];
  I4 [label="建设用地市场化率·地价收敛度"];
  I5 [label="技术合同跨省成交·数据平台接入·专利转移"];
  I6 [label="公平竞争审查·市场监管统一·营商环境"];
  ROOT->D1->I1; ROOT->D2->I2; ROOT->D3->I3;
  ROOT->D4->I4; ROOT->D5->I5; ROOT->D6->I6;
'''
    render(d, 'fig5_1')


# --------------------------------------------------- 图4.2 空间一般均衡模型结构
def sge_model():
    d = f'''
  rankdir=TB; nodesep=0.4; ranksep=0.5;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  H [label="地区代表性家庭\\nCES 偏好·要素供给", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  F [label="地区—部门企业\\n生产函数 Y=A·K^α L^β N^γ", fillcolor="{C['ltgreen']}", color="{C['green']}"];
  GM [label="商品市场：冰山成本 τ^G", fillcolor="{C['ltgold']}", color="{C['gold']}"];
  FM [label="要素市场：流动壁垒 τ^F\\n（楔子 τ^K, τ^L）", fillcolor="{C['ltorange']}", color="{C['orange']}"];
  EQ [label="空间一般均衡\\n价格·工资·租金·配置", fillcolor="{C['ltteal']}", color="{C['teal']}", fontsize=13];
  AGG [label="总量TFP与福利\\nlnTFP = f(−Var(lnτ))", fillcolor="{C['ltpurple']}", color="{C['purple']}", fontsize=13];
  H->EQ [label="需求·要素供给"];
  F->EQ [label="供给·要素需求"];
  GM->EQ; FM->EQ;
  EQ->AGG;
  FM->AGG [style=dotted, label="错配", constraint=false];
'''
    render(d, 'fig4_2')


# --------------------------------------------------- 图10.1 改革政策体系框架
def policy_frame():
    d = f'''
  rankdir=TB; nodesep=0.3; ranksep=0.45;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8];
  G [label="加快建设全国统一大市场·提升要素配置效率", fillcolor="{C['ltblue']}", color="{C['blue']}", fontsize=14];
  P1 [label="立柱破壁：破除地方保护\\n清理地方性壁垒·规范招商引资", fillcolor="{C['ltred']}", color="{C['red']}"];
  P2 [label="要素市场化改革：户籍·土地\\n资本·技术·数据市场改革", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  P3 [label="统一制度规则：产权·准入\\n公平竞争审查·统一监管", fillcolor="{C['ltgold']}", color="{C['gold']}"];
  P4 [label="设施联通：交通物流\\n数据基础设施·信用体系", fillcolor="{C['ltgreen']}", color="{C['green']}"];
  P5 [label="激励相容：改革政绩考核\\n横向利益补偿机制", fillcolor="{C['ltpurple']}", color="{C['purple']}"];
  O [label="要素配置效率提升·全国统一大市场·中国式现代化", fillcolor="{C['ltorange']}", color="{C['orange']}", fontsize=13.5];
  G->P1; G->P2; G->P3; G->P4; G->P5;
  P1->O; P2->O; P3->O; P4->O; P5->O;
'''
    render(d, 'fig10_1')


if __name__ == '__main__':
    roadmap(); framework(); seg_causes(); theory_mech(); numi_tree(); sge_model(); policy_frame()
    print('diagrams done')
