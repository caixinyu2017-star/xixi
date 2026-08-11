# -*- coding: utf-8 -*-
"""后半部机制图（D 型，10 幅：fig9_1、fig10_1、fig10_2、fig10_4、fig11_1、
fig11_2、fig12_1、fig13_1、fig13_2、fig14_1）。graphviz + matplotlib 手绘。
图名与图注不写入图内（由 Word 排版程序添加）；实线＝直接作用，虚线＝反馈。
除 fig11_1（因果回路图，Vensim 风格允许弧线）外，连线一律直线或正交折线。"""
import json
import math
import os
import subprocess

import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, FancyArrowPatch, Ellipse,
                                Polygon, Rectangle, Arc)

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
    """学术风格：正交/折线连线，不用曲线；避免交叠。"""
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


def loopmark(ax, x, y, lab, c, ccw=True, rx=2.4, ry=2.0):
    """CLD 回路徽标：R/B 字样 + 环形旋转箭头（Arc 精确控制外扩范围，防压线）。"""
    th1, th2 = -55, 205  # 留 100° 缺口放旋转箭头
    ax.add_patch(Arc((x, y), 2 * rx, 2 * ry, theta1=th1, theta2=th2,
                     color=c, lw=1.2, zorder=3))
    the = math.radians(th2 if ccw else th1)
    px, py = x + rx * math.cos(the), y + ry * math.sin(the)
    tx, ty = -rx * math.sin(the), ry * math.cos(the)
    L = math.hypot(tx, ty)
    tx, ty = tx / L, ty / L
    if not ccw:
        tx, ty = -tx, -ty
    hl, hw = 0.95, 0.55
    nx, ny = -ty, tx
    ax.add_patch(Polygon([(px + tx * hl, py + ty * hl),
                          (px + nx * hw, py + ny * hw),
                          (px - nx * hw, py - ny * hw)],
                         closed=True, fc=c, ec=c, zorder=3))
    txt(ax, x, y, lab, fs=8, c=c, bold=True, z=4)


def delaymark(ax, p1, p2, c='#444444', t=0.5, ln=2.2, gap=1.1):
    """在直线边上画 ∥ 延迟标记（两道垂直于边的短线）。"""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    mx, my = p1[0] + t * dx, p1[1] + t * dy
    for s in (-gap / 2, gap / 2):
        cx0, cy0 = mx + s * ux, my + s * uy
        ax.plot([cx0 - ln / 2 * nx, cx0 + ln / 2 * nx],
                [cy0 - ln / 2 * ny, cy0 + ln / 2 * ny], color=c, lw=1.4, zorder=3)


def cloud(ax, x, y, lab='源'):
    e = Ellipse((x, y), 9, 6, fc='white', ec=PAL['gray'], lw=1.1, ls='--', zorder=2)
    ax.add_patch(e)
    txt(ax, x, y, lab, fs=7, c=PAL['gray'])


def valve(ax, x, y, col):
    ax.add_patch(Polygon([(x - 1.8, y + 2), (x, y), (x - 1.8, y - 2)], closed=True,
                         fc=col, ec=col, zorder=3))
    ax.add_patch(Polygon([(x + 1.8, y + 2), (x, y), (x + 1.8, y - 2)], closed=True,
                         fc=col, ec=col, zorder=3))


# --------------------------------------------------- 图9.1 三方博弈关系（matplotlib）
def fig9_1():
    g = R['game']['params']
    th = R['game']['threshold']
    fig, ax = canvas(8.6, 6.6, 100, 80)
    bx(ax, 29, 62, 42, 15,
       '高　校　U\n策略：深度融合转型（x）／传统模式（1－x）\n参数：转型成本 c_U＝%g·融合收益 R_U＝%g' % (g['cU'], g['RU']),
       fc=C['ltblue'], ec=PAL['blue'], fs=8.3, lw=1.6)
    bx(ax, 2, 6, 40, 15,
       '企　业　E\n策略：深度参与（y）／浅层合作（1－y）\n参数：参与成本 c_E＝%g·人才红利 R_E＝%g～%g' % (g['cE'], g['RE_base'], g['RE_hi']),
       fc=C['ltteal'], ec=PAL['teal'], fs=8.3, lw=1.6)
    bx(ax, 58, 6, 40, 15,
       '政　府　G\n策略：强激励（z）／常规支持（1－z）\n参数：激励成本 c_G＝%g·补贴 s＝%g\n错配损失 L＝%g' % (g['cG'], g['s'], g['L']),
       fc=C['ltgold'], ec=PAL['gold'], fs=8.3, lw=1.6)
    # U—E（左侧两条平行直线）
    arr(ax, (30, 61.5), (12, 21.5), c=PAL['blue'], lw=1.4)
    txt(ax, 16.7, 43.3, '定制化人才输送\n（人才红利 R_E 之源）', fs=7.0, c=PAL['blue'], rot=66)
    arr(ax, (20, 21.5), (37, 61.5), c=PAL['teal'], lw=1.4)
    txt(ax, 25.0, 41.5, '项目·导师·实训投入\n（分担成本·实现 R_U）', fs=7.0, c=PAL['teal'], rot=67)
    # U—G（右侧两条平行直线）
    arr(ax, (70, 61.5), (88, 21.5), c=PAL['blue'], lw=1.4)
    txt(ax, 83.3, 43.3, '培养成效与错配缓解\n（降低社会损失 L）', fs=7.0, c=PAL['blue'], rot=-66)
    arr(ax, (80, 21.5), (63, 61.5), c=PAL['gold'], lw=1.4)
    txt(ax, 75.0, 41.5, '专项补贴 s·绩效拨款\n（对冲转型成本 c_U）', fs=7.0, c=PAL['gold'], rot=-67)
    # E—G（底部两条水平直线）
    arr(ax, (42.5, 15.5), (57.5, 15.5), c=PAL['teal'], lw=1.4)
    txt(ax, 49.7, 18.9, '深度参与提升治理绩效', fs=6.7, c=PAL['teal'])
    arr(ax, (57.5, 10.5), (42.5, 10.5), c=PAL['gold'], lw=1.4)
    txt(ax, 50, 6.4, '税费激励与补贴\n分担参与成本 c_E', fs=7.0, c=PAL['gold'])
    # 中心：复制动态系统
    bx(ax, 33, 33, 34, 14,
       '复制动态系统\ndx/dt·dy/dt·dz/dt（三维演化）\n跃迁阈值：R_E＞%.2f → 深度融合均衡' % th['RE_crit'],
       fc=C['ltred'], ec=PAL['red'], fs=7.8, lw=1.4, ls='dashed', bold=True)
    for p1, p2 in [((44, 61.5), (46, 47.8)), ((30, 21.7), (38, 32.2)),
                   ((70, 21.7), (62, 32.2))]:
        arr(ax, p1, p2, c=PAL['red'], lw=1.0, ls='--', ms=10)
    txt(ax, 50, 29.4, '三方策略互动（虚线）共同决定演化均衡', fs=6.8, c=PAL['red'])
    save(fig, f'{FIG}/fig9_1.png')
    print('ok fig9_1')


# --------------------------------------------------- 图10.1 培育机制总体架构（matplotlib，核心图）
def fig10_1():
    m = R['ahp']['mech']
    fig, ax = canvas(11.0, 8.0, 120, 88)
    # 顶部：三原则
    ax.add_patch(Rectangle((8, 70), 104, 15, fc='none', ec=PAL['orange'],
                           lw=1.1, ls='--', zorder=1))
    txt(ax, 60, 82.6, '机制设计三原则（源于第5—9章实证结论）', fs=8.8, c=PAL['orange'], bold=True)
    prins = [(12, '需求牵引\n以岗位能力需求锚定培养目标与课程内容'),
             (45, '能力本位\n以五层能力模型组织培养过程与评价'),
             (78, '激励相容\n以利益结构设计保障企业深度参与（R_E＞1.81）')]
    for x0, t in prins:
        bx(ax, x0, 71.5, 30, 8, t, fc=C['ltorange'], ec=PAL['orange'], fs=7.0, pad=0.35)
    for xa in (27, 60, 93):
        arr(ax, (xa, 71.1), (xa, 66.6), c=PAL['orange'], lw=1.3)
    # 中部：五大子机制
    ax.add_patch(Rectangle((4, 38), 112, 28, fc='none', ec=PAL['blue'],
                           lw=1.1, ls='--', zorder=1))
    txt(ax, 60, 63.4, '五大子机制（括号内为 AHP 组合权重，CR＝%.3f＜0.1）' % m['CR'],
        fs=8.8, c=PAL['blue'], bold=True)
    mechs = [('需求传导机制\n（%.3f）\n岗位能力图谱发布\n培养方案动态调整' % m['transmit'], C['ltblue'], PAL['blue']),
             ('协同培养机制\n（%.3f）\n项目制课程与实训\n双导师联合培养' % m['cotrain'], C['ltteal'], PAL['teal']),
             ('师资共建机制\n（%.3f）\n产业教师特设岗位\n教师企业实践轮训' % m['faculty'], C['ltgreen'], PAL['green']),
             ('评价反馈机制\n（%.3f）\n就业匹配质量监测\nCTD 触发课程修订' % m['feedback'], C['ltpurple'], PAL['purple']),
             ('利益分配机制\n（%.3f）\n成本分担与收益共享\n知识产权权益安排' % m['benefit'], C['ltgold'], PAL['gold'])]
    x0, cw, gap = 4.6, 20.6, 2.0
    for i, (t, fc, ec) in enumerate(mechs):
        bx(ax, x0 + i * (cw + gap), 40.5, cw, 19, t, fc=fc, ec=ec, fs=6.7, pad=0.35)
    # 底部：供需两侧接口
    bx(ax, 6, 8, 50, 20, '供给侧接口——高　校\n培养方案与课程模块实施\n实训体系与学分认定\n毕业生能力供给',
       fc=C['ltblue'], ec=PAL['blue'], fs=7.6, lw=1.5, pad=0.4)
    bx(ax, 64, 8, 50, 20, '需求侧接口——企　业\n岗位能力需求与用人标准\n真实项目·企业导师·实训资源\n用人反馈与质量评价',
       fc=C['ltteal'], ec=PAL['teal'], fs=7.6, lw=1.5, pad=0.4)
    arr(ax, (31, 28.8), (31, 37.4), c=PAL['blue'], lw=1.6, style='<|-|>', ms=13)
    txt(ax, 21.5, 33, '标准·课程下行\n能力供给上行', fs=6.4, c=PAL['blue'])
    arr(ax, (89, 28.8), (89, 37.4), c=PAL['teal'], lw=1.6, style='<|-|>', ms=13)
    txt(ax, 99.0, 33, '需求·资源上行\n人才·反馈下行', fs=6.4, c=PAL['teal'])
    arr(ax, (56.8, 18), (63.2, 18), c=PAL['gold'], lw=1.6, style='<|-|>', ms=13)
    txt(ax, 60, 23.2, '供需\n对接', fs=6.6, c=PAL['gold'], bold=True)
    save(fig, f'{FIG}/fig10_1.png')
    print('ok fig10_1')


# --------------------------------------------------- 图10.2 AHP 层次结构（graphviz）
def fig10_2():
    cr = R['ahp']['criteria']
    m = R['ahp']['mech']
    ex = R['ahp']['experts']
    d = f'''
  rankdir=TB; nodesep=0.25; ranksep=0.8; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.16,0.09"];
  edge [color="{C['gray']}", arrowsize=0.7];
  A [label="目标层 A：产教融合培育机制构建\\n（五大子机制权重配置）", fillcolor="{C['ltred']}", color="{C['red']}", fontsize=13.5];
  C1 [label="准则层 C1\\n需求适配性\\n（权重 {cr['demand']:.3f}）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  C2 [label="准则层 C2\\n价值创造性\\n（权重 {cr['value']:.3f}）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  C3 [label="准则层 C3\\n可持续性\\n（权重 {cr['sustain']:.3f}）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  P1 [label="需求传导机制\\n（{m['transmit']:.3f}）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  P2 [label="协同培养机制\\n（{m['cotrain']:.3f}）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  P3 [label="师资共建机制\\n（{m['faculty']:.3f}）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  P4 [label="评价反馈机制\\n（{m['feedback']:.3f}）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  P5 [label="利益分配机制\\n（{m['benefit']:.3f}）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  NOTE [label="德尔菲法两轮征询：{ex['n']} 位专家，Kendall W＝{ex['kendall_w']:.2f}\\n一致性检验：准则层 CR＝{cr['CR']:.3f}，方案层 CR＝{m['CR']:.3f}，均＜0.1", shape=note, style="filled", fillcolor="{C['ltgray']}", color="{C['gray']}", fontsize=11];
  {{rank=same; C1; C2; C3;}} C1 -> C2 -> C3 [style=invis];
  {{rank=same; P1; P2; P3; P4; P5;}} P1 -> P2 -> P3 -> P4 -> P5 [style=invis];
  A -> C1; A -> C2; A -> C3;
  C1 -> P1; C1 -> P2; C1 -> P3; C1 -> P4; C1 -> P5;
  C2 -> P1; C2 -> P2; C2 -> P3; C2 -> P4; C2 -> P5;
  C3 -> P1; C3 -> P2; C3 -> P3; C3 -> P4; C3 -> P5;
  P3 -> NOTE [style=invis];
'''
    render(d, 'fig10_2')


# --------------------------------------------------- 图10.4 国际模式比较（matplotlib）
def fig10_4():
    fig, ax = canvas(10.0, 6.6, 112, 74)
    cols = [('德　国\n双元制', '企业与职业院校双主体\n工学交替·学徒制培养\n\n《联邦职业教育法》\n提供法定制度保障\n\n行业协会主导职业\n标准与考核认证',
             C['ltblue'], PAL['blue']),
            ('美　国\nCO-OP 合作教育', '工作—学习学期交替\n嵌入真实产业项目\n\n带薪实习·企业深度\n参与培养与考核\n\n校企协议与学分认定\n制度化衔接',
             C['ltteal'], PAL['teal']),
            ('新加坡\nSkillsFuture', '政府主导全民技能\n账户与学习补贴\n\n技能框架对接产业\n需求·动态发布标准\n\n企业共训与税补激励\n终身学习导向',
             C['ltgold'], PAL['gold']),
            ('中　国\n现代产业学院', '校企共建二级学院\n实体·理事会共治\n\n产业真实场景与项目\n牵引课程与实训\n\n多元投入·资源共享\n面向区域产业布局',
             C['ltgreen'], PAL['green'])]
    x0, cw, gap = 3, 24, 3.4
    for i, (hd, body, fc, ec) in enumerate(cols):
        xx = x0 + i * (cw + gap)
        bx(ax, xx, 58, cw, 9, hd, fc=ec, ec=ec, fs=8.5, tc='white', bold=True, pad=0.35)
        bx(ax, xx, 24, cw, 31, body, fc=fc, ec=ec, fs=6.6, pad=0.35)
        arr(ax, (xx + cw / 2, 57.7), (xx + cw / 2, 55.6), c=ec, lw=1.2, ms=9)
        arr(ax, (xx + cw / 2, 23.6), (xx + cw / 2, 18.8), c=ec, lw=1.3)
    bx(ax, 8, 6, 96, 12, '共性提炼\n需求牵引的培养标准　·　企业深度参与的制度化保障　·　激励相容的成本分担与收益共享',
       fc=C['ltred'], ec=PAL['red'], fs=8.2, lw=1.5, bold=True, pad=0.4)
    save(fig, f'{FIG}/fig10_4.png')
    print('ok fig10_4')


# --------------------------------------------------- 图11.1 因果回路图（matplotlib，唯一允许弧线）
def fig11_1():
    fig, ax = canvas(9.2, 6.3, 100, 68)
    nodes = {
        'DEM': (10, 62, '产业人才需求'),
        'GAP': (9, 46, '人才需求缺口'),
        'SUP': (9, 26, '毕业生有效供给'),
        'ENR': (14, 10, '招生与培养规模'),
        'LOAD': (38, 5, '师资负荷'),
        'F': (33, 55, '产教融合强度'),
        'FIT': (61, 61, '课程—岗位适配'),
        'DIV': (76, 47, '企业人才红利'),
        'Q': (58, 29, '培养质量'),
        'REP': (36, 20, '院校声誉'),
        'STU': (65, 13, '优质生源')}

    def edge(k1, k2, sign, rad=0.12, col=None, lab=None, labp=None, sp=None,
             shA=16, shB=26):
        x1, y1, _ = nodes[k1]
        x2, y2, _ = nodes[k2]
        col = col or (PAL['blue'] if sign == '+' else PAL['red'])
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=13,
                            color=col, lw=1.5, connectionstyle=f'arc3,rad={rad}',
                            shrinkA=shA, shrinkB=shB, zorder=1)
        ax.add_patch(a)
        txt(ax, sp[0], sp[1], '＋' if sign == '+' else '－', fs=10.5, c=col, bold=True)
        if lab:
            txt(ax, labp[0], labp[1], lab, fs=6.5, c=col)

    # 外生驱动与缺口
    edge('DEM', 'GAP', '+', rad=0.0, sp=(12.2, 51.8))
    edge('GAP', 'F', '+', rad=0.10, lab='缺口牵引政策与\n企业激励', labp=(14.8, 55.5),
         sp=(25.5, 52.5), shB=30)
    # R1 需求牵引增强回路：F→FIT→DIV→F（顺时针）
    edge('F', 'FIT', '+', rad=0.12, lab='能力图谱传导', labp=(44, 62.6), sp=(51.5, 60.7), shB=30)
    edge('FIT', 'DIV', '+', rad=0.12, lab='适配人才增加红利', labp=(80, 58.0), sp=(78.5, 53.8), shB=24)
    edge('DIV', 'F', '+', rad=-0.12, lab='红利驱动企业加大参与投入', labp=(57, 45.3), sp=(40.5, 50.3), shB=28)
    # F→Q
    edge('F', 'Q', '+', rad=-0.06, lab='双师与实训\n提升质量', labp=(37.5, 41.5), sp=(51.5, 35.5), shB=22)
    # R2 质量声誉增强回路：Q→REP→STU→Q
    edge('Q', 'REP', '+', rad=0.10, lab='就业口碑', labp=(48.5, 28.5), sp=(41.5, 24.6), shB=22)
    edge('REP', 'STU', '+', rad=0.14, lab='声誉吸引生源', labp=(50, 11.6), sp=(59.5, 11.2), shB=24)
    edge('STU', 'Q', '+', rad=0.14, lab='生源支撑质量', labp=(70.5, 22.5), sp=(63, 23.5), shB=20)
    # B1 师资约束平衡回路：REP→ENR→LOAD→Q（－）→REP
    edge('REP', 'ENR', '+', rad=0.10, lab='声誉扩大招生', labp=(23.5, 12.7), sp=(19, 15.6), shB=30)
    edge('ENR', 'LOAD', '+', rad=0.10, lab='规模推高负荷', labp=(24, 3.6), sp=(31.5, 5.6), shB=20)
    edge('LOAD', 'Q', '-', rad=0.10, lab='生师比恶化\n制约质量', labp=(50.5, 6.8), sp=(55, 22.0), shB=22)
    # 培养延迟与供给闭环
    edge('ENR', 'SUP', '+', rad=0.0, sp=(8.0, 19.5), shB=22)
    delaymark(ax, (14, 10), (9, 26), c='#444444', t=0.52)
    txt(ax, 19.5, 18.5, '培养延迟 τ\n（约3.5年）', fs=6.5, c='#444444')
    edge('SUP', 'GAP', '-', rad=0.0, sp=(6.0, 36.5), shB=22)
    # 节点文字（白底盖住箭头端部）
    for k, (x, y, lab) in nodes.items():
        ax.text(x, y, lab, fontsize=8.5, color='#1a1a1a', fontweight='bold',
                ha='center', va='center', linespacing=1.3, zorder=5,
                bbox=dict(boxstyle='round,pad=0.32', fc='white', ec='none', alpha=0.92))
    # 回路徽标（旋转箭头）与回路名（置于回路内空白处，避开弧线）
    loopmark(ax, 56, 53.2, 'R1', PAL['blue'], ccw=False)
    txt(ax, 62.5, 51.6, '需求牵引\n增强回路', fs=6.6, c=PAL['blue'], z=5)
    loopmark(ax, 58.5, 17.5, 'R2', PAL['teal'], ccw=True)
    txt(ax, 78, 17, '质量声誉增强回路', fs=6.6, c=PAL['teal'], z=5)
    loopmark(ax, 30.5, 11.5, 'B1', PAL['red'], ccw=True)
    txt(ax, 31, 15.2, '师资约束平衡回路', fs=6.2, c=PAL['red'], z=5)
    txt(ax, 50, 0.8, '＋＝同向变动　－＝反向变动　R＝增强回路　B＝平衡回路　∥＝延迟',
        fs=6.6, c='#666666')
    save(fig, f'{FIG}/fig11_1.png')
    print('ok fig11_1')


# --------------------------------------------------- 图11.2 存量—流量结构图（matplotlib）
def fig11_2():
    tau = R['sd']['delay_tau']
    ctd = R['sd']['ctd_star']
    fig, ax = canvas(9.2, 6.3, 104, 70)
    yM = 50
    # 主链：源→HI→在培存量→HO→就业存量→AT→汇
    cloud(ax, 6, yM, '源')
    cloud(ax, 98, yM, '汇')
    ax.add_patch(Rectangle((26, yM - 6.5), 18, 13, fc=C['ltblue'], ec=PAL['blue'],
                           lw=1.8, zorder=2))
    txt(ax, 35, yM, '在培人才存量\nHS_t', fs=8.5, bold=True)
    ax.add_patch(Rectangle((60, yM - 6.5), 18, 13, fc=C['ltteal'], ec=PAL['teal'],
                           lw=1.8, zorder=2))
    txt(ax, 69, yM, '就业人才存量\nES_t', fs=8.5, bold=True)
    ax.plot([10.5, 25.8], [yM, yM], color=PAL['blue'], lw=2.2, zorder=1)
    arr(ax, (23, yM), (25.8, yM), c=PAL['blue'], lw=2.2, ms=14)
    valve(ax, 17, yM, PAL['blue'])
    txt(ax, 14.5, yM + 5.8, '招生流入 HI_t', fs=7.6, c=PAL['blue'], bold=True)
    ax.plot([44.2, 59.8], [yM, yM], color=PAL['teal'], lw=2.2, zorder=1)
    arr(ax, (57, yM), (59.8, yM), c=PAL['teal'], lw=2.2, ms=14)
    valve(ax, 52, yM, PAL['teal'])
    txt(ax, 52, yM + 6.0, '毕业流出 HO_t\n（培养延迟 τ＝%g 年）' % tau, fs=7.6,
        c=PAL['teal'], bold=True)
    ax.plot([78.2, 93.5], [yM, yM], color=PAL['gray'], lw=2.0, zorder=1)
    arr(ax, (91, yM), (93.5, yM), c=PAL['gray'], lw=2.0, ms=13)
    valve(ax, 85, yM, PAL['gray'])
    txt(ax, 89, yM + 6.2, '离职与流失 AT_t', fs=7.2, c=PAL['gray'])
    # 顶部：产业需求与缺口
    bx(ax, 56, 62, 32, 7, '产业人才需求 D_t（第6章三情景预测）',
       fc=C['ltorange'], ec=PAL['orange'], fs=7.8, pad=0.35)
    e = Ellipse((78, 33), 28, 9.5, fc=C['ltgold'], ec=PAL['gold'], lw=1.5, zorder=2)
    ax.add_patch(e)
    txt(ax, 78, 33, '人才需求缺口\nGAP_t＝D_t－ES_t', fs=7.6, bold=True)
    # D_t → GAP（信息线，跨主链处断线避让）
    ax.plot([80, 80], [61.6, 51.0], color=PAL['orange'], lw=1.3, zorder=1)
    ax.plot([80, 80], [48.9, 43.4], color=PAL['orange'], lw=1.3, zorder=1)
    arr(ax, (80, 43.4), (79.2, 38.6), c=PAL['orange'], lw=1.3)
    txt(ax, 82.5, 45.0, '＋', fs=10, c=PAL['orange'], bold=True)
    arr(ax, (72, 43.2), (76, 38.3), c=PAL['teal'], lw=1.3)
    txt(ax, 72.2, 40.6, '－', fs=10, c=PAL['teal'], bold=True)
    # GAP → 招生（虚线信息反馈，正交折线）
    ax.plot([64, 17, 17], [33, 33, 45.8], color=PAL['red'], lw=1.3, ls='--', zorder=1)
    arr(ax, (17, 44), (17, 47.6), c=PAL['red'], lw=1.3, ls='--', ms=11)
    txt(ax, 39, 35.8, '缺口驱动扩招（＋）', fs=7.0, c=PAL['red'])
    # 底部：CTD 阈值触发课程修订
    bx(ax, 4, 22, 20, 8, 'AI 技术前沿\nTL_t', fc=C['ltgreen'], ec=PAL['green'], fs=7.6, pad=0.35)
    bx(ax, 30, 22, 20, 8, '课程技术水平\nCL_t', fc=C['ltblue'], ec=PAL['blue'], fs=7.6, pad=0.35)
    e2 = Ellipse((27, 11), 32, 8.5, fc=C['ltgold'], ec=PAL['gold'], lw=1.4, zorder=2)
    ax.add_patch(e2)
    txt(ax, 27, 11, '课程滞后度\nCTD_t＝(TL_t－CL_t)/TL_t', fs=7.2, bold=True)
    arr(ax, (13, 21.6), (20, 15.0), c=PAL['green'], lw=1.3)
    txt(ax, 13.5, 17.5, '＋', fs=10, c=PAL['green'], bold=True)
    arr(ax, (39, 21.6), (33, 15.2), c=PAL['blue'], lw=1.3)
    txt(ax, 39.5, 17.5, '－', fs=10, c=PAL['blue'], bold=True)
    ax.add_patch(Polygon([(48, 11), (58, 5.5), (68, 11), (58, 16.5)], closed=True,
                         fc=C['ltred'], ec=PAL['red'], lw=1.4, zorder=2))
    txt(ax, 58, 11, '触发判断\nCTD_t＞CTD*？\n（CTD*＝%.2f）' % ctd, fs=6.4, c=PAL['red'], bold=True)
    arr(ax, (43.2, 11), (47.6, 11), c=PAL['gold'], lw=1.3)
    bx(ax, 72, 7, 24, 8, '课程修订\n（新增模块·更新内容）', fc=C['ltpurple'],
       ec=PAL['purple'], fs=7.2, pad=0.35)
    arr(ax, (68.3, 11), (71.6, 11), c=PAL['red'], lw=1.3)
    txt(ax, 70, 13.6, '是', fs=6.8, c=PAL['red'], bold=True)
    # GAP → 课程修订（虚线信息反馈）
    ax.plot([84, 84], [28.2, 15.6], color=PAL['red'], lw=1.3, ls='--', zorder=1)
    arr(ax, (84, 17), (84, 15.6), c=PAL['red'], lw=1.3, ls='--', ms=11)
    txt(ax, 92.2, 22.5, '缺口结构信息\n→修订方向', fs=6.6, c=PAL['red'])
    # 课程修订 → 课程技术水平（虚线，正交折线）
    ax.plot([76, 76, 51], [15.4, 18.8, 18.8], color=PAL['purple'], lw=1.3, ls='--', zorder=1)
    arr(ax, (51, 18.8), (44, 22.6), c=PAL['purple'], lw=1.3, ls='--', ms=11)
    txt(ax, 62, 20.9, '修订后课程水平提升（＋）', fs=6.6, c=PAL['purple'])
    # 图例（符号说明）
    txt(ax, 52, 1.2, '矩形＝存量　蝶形阀＝流量　虚线云朵＝系统边界源汇　实线＝人才流　虚线＝信息反馈',
        fs=6.6, c='#666666')
    save(fig, f'{FIG}/fig11_2.png')
    print('ok fig11_2')


# --------------------------------------------------- 图12.1 效能评估框架（graphviz）
def fig12_1():
    ev = R['eval12']
    mq = ev['mq']
    rg = ev['reg']
    d = f'''
  rankdir=TB; nodesep=0.3; ranksep=0.5; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  subgraph cluster_io {{ label="院校投入产出表（院校—年份面板，N＝{rg['N']}）"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12;
    I1 [label="投入：生均经费 K", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    I2 [label="投入：师资规模 L", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    I3 [label="投入：产教融合投入 F\\n（企业参与度·双师比例·实训强度）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    O1 [label="产出：毕业生能力增值\\n（五层能力测评）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    O2 [label="产出：就业结果\\n（去向·起薪·留存）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  }}
  DEA [label="DEA 效率测度\\n（BCC 模型，均值 {ev['dea']['mean']:.2f}）", fillcolor="{C['ltgold']}", color="{C['gold']}"];
  SFA [label="SFA 效率测度\\n（随机前沿，与 DEA 相关 {ev['sfa_corr']:.2f}）", fillcolor="{C['ltgold']}", color="{C['gold']}"];
  MQ [label="就业匹配质量指数 MQ＝{mq['index']:.2f}\\n专业对口率 {mq['match_rate']:.2f}·薪酬溢价 {mq['salary_prem']:.2f}·留存率 {mq['retention']:.2f}", fillcolor="{C['ltgreen']}", color="{C['green']}"];
  TE [label="培养效率 TE（双方法互证）", fillcolor="{C['ltorange']}", color="{C['orange']}", fontsize=13];
  REG [label="回归诊断：产教融合强度 F 的效能效应\\nF→TE：{ev['reg']['F_on_te']['coef']:.3f}***　F→MQ：{ev['reg']['F_on_mq']['coef']:.3f}***\\n（控制院校类型·区域·年份固定效应）", fillcolor="{C['ltpurple']}", color="{C['purple']}", fontsize=13];
  FB [label="机制反馈：定位低效环节\\n调整五大子机制配置（第10章）·对照案例证据（第13章）", style="rounded,filled,dashed", fillcolor="white", color="{C['red']}", fontcolor="{C['red']}"];
  {{rank=same; I1; I2; I3; O1; O2;}} I1 -> I2 -> I3 -> O1 -> O2 [style=invis];
  {{rank=same; DEA; SFA; MQ;}} DEA -> SFA -> MQ [style=invis];
  I2 -> DEA; I3 -> SFA; O1 -> SFA; O2 -> MQ;
  DEA -> TE; SFA -> TE;
  TE -> REG; MQ -> REG;
  REG -> FB;
  FB -> I3 [style=dashed, color="{C['red']}", fontcolor="{C['red']}", label="反馈闭环", constraint=false];
'''
    render(d, 'fig12_1', splines='polyline')


# --------------------------------------------------- 图13.1 多案例分析框架（matplotlib）
def fig13_1():
    fig, ax = canvas(9.8, 7.8, 112, 94)
    cases = [('华为智能基座\n（企业生态主导型）', PAL['blue']),
             ('腾讯犀牛鸟\n（项目牵引型）', PAL['teal']),
             ('百度松果\n（平台课程型）', PAL['purple']),
             ('示范性软件学院\n（院校建制型）', PAL['green'])]
    x0, cw, gap = 24, 20.4, 1.3
    for j, (nm, ec) in enumerate(cases):
        bx(ax, x0 + j * (cw + gap), 81, cw, 9, nm, fc=ec, ec=ec, fs=7.2, tc='white',
           bold=True, pad=0.3)
    mechs = ['需求传导', '协同培养', '师资共建', '评价反馈', '利益分配']
    y0, rh, rgap = 72, 6.4, 1.1
    for i, mn in enumerate(mechs):
        yy = y0 - i * (rh + rgap)
        bx(ax, 2, yy, 20, rh, f'{mn}维度', fc=C['ltgray'], ec=PAL['gray'], fs=7.4,
           bold=True, pad=0.3)
        for j, (nm, ec) in enumerate(cases):
            bx(ax, x0 + j * (cw + gap), yy, cw, rh, f'$e_{{{i+1}{j+1}}}$',
               fc='white', ec=ec, fs=8.5, lw=0.9, tc='#555555', pad=0.3)
    txt(ax, 57, 39.2, '$e_{ij}$：案例 $j$ 在机制维度 $i$ 上的证据编码（访谈、内部档案、实地观察三源互证）',
        fs=6.8, c='#666666')
    arr(ax, (57, 37.2), (57, 33.4), c=PAL['gray'], lw=1.5)
    bx(ax, 16, 25, 82, 8, '跨案例比较：模式求同（复制逻辑）·差异归因（情境条件与机制组合）',
       fc=C['ltgold'], ec=PAL['gold'], fs=8.2, pad=0.4)
    arr(ax, (57, 24.6), (57, 19.4), c=PAL['gold'], lw=1.5)
    bx(ax, 37, 5, 40, 13, '三角验证\n案例证据×定量结果×理论预期\n检验结论收敛性与稳健性',
       fc=C['ltred'], ec=PAL['red'], fs=7.4, lw=1.5, bold=True, pad=0.4)
    bx(ax, 2, 5, 28, 13, '理论预期\n演化博弈均衡（第9章）\n系统动力学机理（第11章）',
       fc=C['ltgray'], ec=PAL['gray'], fs=6.6, pad=0.35)
    bx(ax, 84, 5, 26, 13, '定量结果\n培养效率 TE（第7·12章）\n匹配质量 MQ（第12章）',
       fc=C['ltgray'], ec=PAL['gray'], fs=6.6, pad=0.35)
    arr(ax, (31.0, 11.5), (36.0, 11.5), c=PAL['gray'], lw=1.4)
    arr(ax, (83.0, 11.5), (78.0, 11.5), c=PAL['gray'], lw=1.4)
    save(fig, f'{FIG}/fig13_1.png')
    print('ok fig13_1')


# --------------------------------------------------- 图13.2 扎根理论编码结构（graphviz）
def fig13_2():
    cs = R['cases']
    iv = cs['interviews']
    cd = cs['coding']
    ct = cs['categories']
    ntot = iv['mgr'] + iv['teacher'] + iv['mentor'] + iv['grad']
    d = f'''
  rankdir=LR; nodesep=0.28; ranksep=0.55; compound=true; newrank=true;
  node [shape=box, style="rounded,filled", fontsize=12, margin="0.14,0.08"];
  edge [color="{C['gray']}", arrowsize=0.75, fontsize=10.5, fontcolor="{C['gray']}"];
  SRC [label="深度访谈 {ntot} 份\\n企业管理者 {iv['mgr']}·高校教师 {iv['teacher']}\\n企业导师 {iv['mentor']}·毕业生 {iv['grad']}", fillcolor="{C['ltgray']}", color="{C['gray']}"];
  OPEN [label="开放式编码\\n逐句概念化\\n{cd['open']} 个初始概念", fillcolor="{C['ltblue']}", color="{C['blue']}"];
  AX [label="主轴编码\\n归并聚类\\n{cd['axial']} 个范畴", fillcolor="{C['ltteal']}", color="{C['teal']}"];
  subgraph cluster_core {{ label="选择性编码：{cd['core']} 大核心障碍范畴（括号内为参考点频次）"; style=dashed; color="{C['red']}"; fontcolor="{C['red']}"; fontsize=12;
    G1 [label="利益机制障碍（{ct['benefit']}）\\n成本分担失衡·收益难共享", fillcolor="{C['ltred']}", color="{C['red']}"];
    G2 [label="师资结构障碍（{ct['faculty']}）\\n双师短缺·企业导师激励不足", fillcolor="{C['ltred']}", color="{C['red']}"];
    G3 [label="课程滞后障碍（{ct['curriculum']}）\\n内容更新滞后于技术迭代", fillcolor="{C['ltred']}", color="{C['red']}"];
    G4 [label="评价体系障碍（{ct['evaluation']}）\\n重学术轻实践·评价主体单一", fillcolor="{C['ltred']}", color="{C['red']}"]; }}
  subgraph cluster_path {{ label="培育机制提升路径"; style=dashed; color="{C['green']}"; fontcolor="{C['green']}"; fontsize=12;
    P1 [label="① 利益分配制度化", fillcolor="{C['ltgreen']}", color="{C['green']}"];
    P2 [label="② 双师队伍共建", fillcolor="{C['ltgreen']}", color="{C['green']}"];
    P3 [label="③ 课程动态更新", fillcolor="{C['ltgreen']}", color="{C['green']}"];
    P4 [label="④ 多元评价重构", fillcolor="{C['ltgreen']}", color="{C['green']}"]; }}
  OUT [label="激励相容的培育机制\\n优化方案\\n（反馈第10章机制设计）", fillcolor="{C['ltgold']}", color="{C['gold']}", fontsize=12.5];
  SAT [label="理论饱和检验：后续访谈\\n未再涌现新的范畴与关系", shape=note, style=filled, fillcolor="{C['ltgray']}", color="{C['gray']}", fontsize=10.5];
  {{rank=same; G1; G2; G3; G4;}}
  {{rank=same; P1; P2; P3; P4;}}
  SRC -> OPEN -> AX;
  AX -> G1; AX -> G2; AX -> G3; AX -> G4;
  G1 -> P1; G2 -> P2; G3 -> P3; G4 -> P4;
  P1 -> OUT; P2 -> OUT; P3 -> OUT; P4 -> OUT;
  AX -> SAT [style=dotted, dir=none];
'''
    render(d, 'fig13_2', splines='polyline')


# --------------------------------------------------- 图14.1 政策体系框架（graphviz）
def fig14_1():
    gap35 = R['sd']['scenario']['strong']['gap']['2035']
    d = f'''
  rankdir=TB; nodesep=0.26; ranksep=0.5; compound=true;
  node [shape=box, style="rounded,filled", fontsize=12.5, margin="0.15,0.09"];
  edge [color="{C['gray']}", arrowsize=0.8, fontsize=10.5, fontcolor="{C['gray']}"];
  GOAL [label="“十五五”目标：建成供需适配、激励相容的 AI 青年科技人才产教融合培育体系\\n人才缺口由扩大转向收敛（强化情景下 2035 年降至 {gap35:.0f} 万人）", fillcolor="{C['ltred']}", color="{C['red']}", fontsize=13.5];
  subgraph cluster_d {{ label="需求侧支柱：精准释放与传导需求"; style=dashed; color="{C['orange']}"; fontcolor="{C['orange']}"; fontsize=12.5;
    D1 [label="岗位能力标准体系：能力图谱\\n定期发布·衔接职业标准", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    D2 [label="企业参与激励：税费抵扣与补贴联动\\n（提高人才红利 R_E·降低参与成本 c_E）", fillcolor="{C['ltorange']}", color="{C['orange']}"];
    D3 [label="重点领域人才需求预测\\n与目录发布制度", fillcolor="{C['ltorange']}", color="{C['orange']}"]; }}
  subgraph cluster_s {{ label="供给侧支柱：提升培养能力"; style=dashed; color="{C['blue']}"; fontcolor="{C['blue']}"; fontsize=12.5;
    S1 [label="专业与课程动态调整\\n（CTD＞0.25 触发修订制度化）", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    S2 [label="双师队伍建设：产业教师特设岗位\\n教师企业实践轮训", fillcolor="{C['ltblue']}", color="{C['blue']}"];
    S3 [label="现代产业学院扩面提质\\n高职—本科—硕博分层培养", fillcolor="{C['ltblue']}", color="{C['blue']}"]; }}
  subgraph cluster_m {{ label="匹配侧支柱：畅通供需对接"; style=dashed; color="{C['teal']}"; fontcolor="{C['teal']}"; fontsize=12.5;
    M1 [label="产教融合信息平台：供需对接\\n实习实训学分互认", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    M2 [label="就业匹配质量监测\\n（MQ 指标纳入培养质量评估）", fillcolor="{C['ltteal']}", color="{C['teal']}"];
    M3 [label="青年人才流动通道：实习—就业\\n联动·区域协同引才", fillcolor="{C['ltteal']}", color="{C['teal']}"]; }}
  BASE [label="数据底座：人才供需监测平台·岗位能力图谱数据库·培养质量追踪调查（支撑三支柱动态校准）", fillcolor="{C['ltgray']}", color="{C['gray']}", fontsize=12.5];
  D1 -> D2 -> D3 [style=invis];
  S1 -> S2 -> S3 [style=invis];
  M1 -> M2 -> M3 [style=invis];
  GOAL -> D1 [lhead=cluster_d]; GOAL -> S1 [lhead=cluster_s]; GOAL -> M1 [lhead=cluster_m];
  D3 -> BASE [ltail=cluster_d, dir=back, style=dashed, color="{C['gray']}"];
  S3 -> BASE [ltail=cluster_s, dir=back, style=dashed, color="{C['gray']}", label="数据支撑与动态校准", fontcolor="{C['gray']}"];
  M3 -> BASE [ltail=cluster_m, dir=back, style=dashed, color="{C['gray']}"];
'''
    render(d, 'fig14_1', splines='polyline')


ALL = [fig9_1, fig10_1, fig10_2, fig10_4, fig11_1, fig11_2, fig12_1,
       fig13_1, fig13_2, fig14_1]

if __name__ == '__main__':
    for f in ALL:
        f()
    print('diagrams_b done:', len(ALL))
