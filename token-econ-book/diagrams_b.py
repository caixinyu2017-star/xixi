# -*- coding: utf-8 -*-
"""后半部机制图（D 型，9 幅：fig8_1、fig9_1、fig10_1、fig10_2、fig11_1、
fig12_1、fig13_1、fig13_3、fig14_1）。matplotlib 手绘（FancyBboxPatch/FancyArrowPatch）。

约束：图名与图注不写入图内（由 Word 排版添加）；连线一律直线或正交折线（rad=0）；
无图标／emoji；浅色填充＋深色描边；含下标变量走 mathtext。
数值一律取自 data/results.json，不得手写。
"""
import json
import os

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon

from matplotlib import font_manager as _fm

from figstyle import save, PAL, CJK  # noqa: F401

# figstyle 只注册了 Regular 字面；机制图大量使用粗体强调，补注册同族 Bold 字面，
# 使 fontweight='bold' 对中文生效（不改动 figstyle 的字族与 rcParams）。
_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
if os.path.exists(_BOLD):
    try:
        _fm.fontManager.addfont(_BOLD)
    except Exception:  # pragma: no cover
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))

C = dict(blue='#1F4E79', ltblue='#DCE6F1', orange='#C55A11', ltorange='#FCE4D6',
         teal='#2E8B8B', ltteal='#D6EAEA', gold='#BF9000', ltgold='#FFF2CC',
         green='#548235', ltgreen='#E2EFDA', red='#A02020', ltred='#F8D7D7',
         gray='#7F7F7F', ltgray='#EDEDED', purple='#674EA7', ltpurple='#E6E0F0')

# ---- 数学符号（与 DESIGN.md 符号约定一致；含下标一律 mathtext） ----
TT = r'$\tilde{T}$'            # 标准词元
TG = r'$\tilde{T}^{g}$'        # 绿色词元
TE = r'$\tilde{T}^{e}$'        # 有效标准词元
PT = r'$\tilde{p}$'            # 标准词元价格
ETA = r'$\eta$'
THETA = r'$\theta$'
IOTA = r'$\iota$'
CO2 = r'$\mathrm{CO_2}$'
CO2E = r'$\mathrm{CO_2}e$'
ETAF = r'$\eta=P^{w_P}R^{w_R}S^{w_S}$'
RFS = r'$R_F$'
AT = r'$\alpha_T$'


# ============================ 通用绘图辅助 ============================
def canvas(win, hin, W=100, H=70):
    fig, ax = plt.subplots(figsize=(win, hin))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis('off')
    ax.grid(False)
    ax.set_position([0, 0, 1, 1])
    return fig, ax


def bx(ax, x, y, w, h, text, fc=C['ltblue'], ec=PAL['blue'], fs=8, lw=1.1,
       ls='solid', tc='#1a1a1a', bold=False, pad=0.3, z=2):
    """圆角方框＋居中文字。(x, y) 为左下角。"""
    p = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad={pad}', fc=fc, ec=ec,
                       lw=lw, linestyle=ls, zorder=z)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs,
            color=tc, zorder=z + 2, fontweight='bold' if bold else 'normal',
            linespacing=1.45)


def rc(ax, x, y, w, h, fc='white', ec=PAL['gray'], lw=1.0, ls='solid', z=1):
    """直角矩形（矩阵单元格、分组框）。"""
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, linestyle=ls, zorder=z))


def arr(ax, p1, p2, c=PAL['gray'], lw=1.3, ls='solid', ms=12, z=3, style='-|>'):
    """直线箭头（rad=0，绝不用曲线）。"""
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms, color=c, lw=lw,
                        linestyle=ls, connectionstyle='arc3,rad=0.0',
                        shrinkA=0.0, shrinkB=0.0, zorder=z)
    ax.add_patch(a)


def orth(ax, pts, c=PAL['gray'], lw=1.3, ls='solid', ms=12, z=3, both=False):
    """正交折线：前 n-1 段用直线，最后一段带箭头；both=True 时首段反向也带箭头。"""
    for i in range(len(pts) - 2):
        ax.plot([pts[i][0], pts[i + 1][0]], [pts[i][1], pts[i + 1][1]],
                color=c, lw=lw, linestyle=ls, zorder=z, solid_capstyle='butt')
    arr(ax, pts[-2], pts[-1], c=c, lw=lw, ls=ls, ms=ms, z=z)
    if both:
        arr(ax, pts[1], pts[0], c=c, lw=lw, ls=ls, ms=ms, z=z)


def txt(ax, x, y, s, fs=7, c='#333333', ha='center', va='center', bold=False,
        rot=0, z=5, bg=None):
    kw = {}
    if bg:
        kw['bbox'] = dict(boxstyle='round,pad=0.25', fc=bg, ec='none')
    ax.text(x, y, s, fontsize=fs, color=c, ha=ha, va=va, rotation=rot,
            fontweight='bold' if bold else 'normal', linespacing=1.4, zorder=z, **kw)


def group(ax, x, y, w, h, label=None, c=PAL['gray'], fs=8, lw=1.0, lx=None):
    """虚线分组框＋左上角标签。"""
    rc(ax, x, y, w, h, fc='none', ec=c, lw=lw, ls=(0, (4, 3)), z=1)
    if label:
        txt(ax, lx if lx is not None else x + w / 2, y + h + 1.9, label,
            fs=fs, c=c, bold=True)


# =============================================================== 图8.1
def fig8_1():
    """词元市场的多边平台结构：四角布局＋交叉网络外部性＋平台三项职能。"""
    fig, ax = canvas(11.0, 8.2, 124, 92)

    # ---- 中心：平台 ----
    bx(ax, 42, 32, 40, 28, '', fc='#F4F8FC', ec=PAL['blue'], lw=1.9)
    txt(ax, 62, 57.0, '平　台', fs=11, c=PAL['blue'], bold=True)
    txt(ax, 62, 52.6, '城市词元运营中心／模型服务平台', fs=7.4, c=PAL['blue'])
    txt(ax, 62, 48.6, '三项职能', fs=6.6, c=PAL['gray'])
    chips = [('撮合匹配\n任务—模型\n最优配对', C['ltblue'], PAL['blue']),
             ('计量结算\n用量与效值\n双口径记账', C['ltteal'], PAL['teal']),
             ('质量认证\n效值系数 ' + ETA + '\n公示与核验', C['ltgold'], PAL['gold'])]
    for i, (t, fc, ec) in enumerate(chips):
        bx(ax, 43.2 + i * 13.0, 34, 11.6, 12.4, t, fc=fc, ec=ec, fs=5.9, lw=1.0, pad=0.22)

    # ---- 四角主体 ----
    bx(ax, 2, 39, 28, 15, '算　力　方\n智算中心·云服务商\n供给：算力（PFLOPS·h）',
       fc=C['ltteal'], ec=PAL['teal'], fs=7.6, lw=1.5, pad=0.35)
    bx(ax, 47, 74, 30, 13, '模　型　方\n模型开发者·开源社区\n供给：模型能力 → ' + ETA,
       fc=C['ltorange'], ec=PAL['orange'], fs=7.6, lw=1.5, pad=0.35)
    bx(ax, 94, 39, 28, 15, '应　用　方\n企业用户·开发者\n需求：场景效用 $S$',
       fc=C['ltpurple'], ec=PAL['purple'], fs=7.6, lw=1.5, pad=0.35)
    bx(ax, 32, 4, 60, 13,
       '政　府　与　监　管\n标准制定 · 补贴核定与政策抵扣 · 价格监测 · 安全审计',
       fc=C['ltgray'], ec=PAL['gray'], fs=7.8, lw=1.5, pad=0.35)

    # ---- 算力方 ↔ 平台 ----
    arr(ax, (30.5, 49), (41.4, 49), c=PAL['teal'], lw=1.4)
    txt(ax, 36, 51.4, '算力池化', fs=6.4, c=PAL['teal'])
    arr(ax, (41.4, 42), (30.5, 42), c=PAL['blue'], lw=1.4)
    txt(ax, 36, 39.6, '产能订单', fs=6.4, c=PAL['blue'])
    # ---- 平台 ↔ 应用方 ----
    arr(ax, (82.6, 49), (93.5, 49), c=PAL['blue'], lw=1.4)
    txt(ax, 88, 53.9, '标准词元服务', fs=6.4, c=PAL['blue'])
    txt(ax, 88, 51.4, '按 ' + PT + ' 计价', fs=6.4, c=PAL['blue'])
    arr(ax, (93.5, 42), (82.6, 42), c=PAL['purple'], lw=1.4)
    txt(ax, 88, 39.6, '用量与反馈', fs=6.4, c=PAL['purple'])
    # ---- 模型方 ↔ 平台 ----
    arr(ax, (57, 73.5), (57, 60.6), c=PAL['orange'], lw=1.4)
    txt(ax, 48.6, 67.2, '模型接入\n效值认证', fs=6.4, c=PAL['orange'])
    arr(ax, (67, 60.6), (67, 73.5), c=PAL['blue'], lw=1.4)
    txt(ax, 75.6, 67.2, '流量分发\n调用分成', fs=6.4, c=PAL['blue'])
    # ---- 政府 ↔ 平台 ----
    arr(ax, (54, 17.5), (54, 31.4), c=PAL['gray'], lw=1.4, ls=(0, (5, 3)))
    txt(ax, 44.0, 21.4, '统一标准\n补贴与抵扣', fs=6.4, c=PAL['gray'])
    arr(ax, (70, 31.4), (70, 17.5), c=PAL['gray'], lw=1.4, ls=(0, (5, 3)))
    txt(ax, 80.2, 21.4, '计量数据\n碳足迹凭证', fs=6.4, c=PAL['gray'])

    # ---- 交叉网络外部性（外圈正交折线，双向） ----
    orth(ax, [(16, 54.6), (16, 80), (46.5, 80)], c=PAL['red'], lw=1.3,
         ls=(0, (5, 3)), both=True, ms=11)
    txt(ax, 26.5, 72.0, '交叉网络外部性 ①\n算力规模 ↔ 模型迭代速度', fs=6.6, c=PAL['red'])
    orth(ax, [(108, 54.6), (108, 80), (77.5, 80)], c=PAL['red'], lw=1.3,
         ls=(0, (5, 3)), both=True, ms=11)
    txt(ax, 97.5, 72.0, '交叉网络外部性 ②\n模型丰富度 ↔ 应用规模', fs=6.6, c=PAL['red'])
    # ---- 应用方 ↔ 算力方（需求规模摊薄算力成本） ----
    orth(ax, [(100, 38.6), (100, 26), (9, 26), (9, 38.6)], c=PAL['red'],
         lw=1.3, ls=(0, (5, 3)), both=True, ms=11)
    txt(ax, 22, 32, '交叉网络外部性 ③\n应用用量规模 ↔ 单位算力成本', fs=6.6, c=PAL['red'])

    save(fig, f'{FIG}/fig8_1.png')
    print('ok fig8_1')


# =============================================================== 图9.1
def fig9_1():
    """算力—词元转化与配置分析框架：转化链条＋四项损失作用点＋调度层反馈。"""
    e = R['eff']
    th = e['theta_wan_ste_per_pflops_h']
    ls_ = e['losses']
    fig, ax = canvas(12.2, 7.6, 136, 84)

    # ---- 主链条 ----
    yb, hh = 35, 14
    bx(ax, 2, yb, 20, hh, '算 力 投 入\n$C$（PFLOPS·h）\n装机规模 × 可用率',
       fc=C['ltteal'], ec=PAL['teal'], fs=6.6, lw=1.5, pad=0.32)
    bx(ax, 27, yb, 26, hh,
       '转 化 函 数 ' + THETA + '\n单位算力的有效标准词元产出\n分档位 %.1f — %.1f 万枚／(PFLOPS·h)'
       % (th['reason'], th['light']),
       fc=C['ltblue'], ec=PAL['blue'], fs=6.4, lw=1.5, pad=0.32)
    bx(ax, 58, yb, 20, hh, '物 理 词 元 $T$\n分词器计费口径\n不区分模型与任务',
       fc=C['ltgray'], ec=PAL['gray'], fs=6.6, lw=1.5, pad=0.32)
    bx(ax, 83, yb, 23, hh, '效 值 折 算 ' + ETA + '\n' + TT + r'$=\eta T$' + '\n' + ETAF,
       fc=C['ltorange'], ec=PAL['orange'], fs=6.6, lw=1.5, pad=0.32)
    bx(ax, 111, yb, 23, hh, '有效标准词元 ' + TE + '\n可比 · 可加 · 可入账\n配置与核算的共同尺度',
       fc=C['ltgreen'], ec=PAL['green'], fs=6.6, lw=1.5, pad=0.32)
    for x1, x2 in [(22.4, 26.5), (53.4, 57.5), (78.4, 82.5), (106.4, 110.5)]:
        arr(ax, (x1, 42), (x2, 42), c=PAL['gray'], lw=1.6, ms=13)

    # ---- 四项损失（作用点以直线箭头指向链条相应位置） ----
    losses = [
        (4, '① 空 转 损 失　−%d pp\n负载波动 · 预留冗余闲置\n作用点：有效算力供给' % round(ls_['idle'] * 100),
         (16, 25.6), (33, 34.5), PAL['red']),
        (32, '② 批 次 损 失　−%d pp\n批大小与并发配置欠优\n作用点：转化函数 ' % round(ls_['batch'] * 100) + THETA,
         (44, 25.6), (45, 34.5), PAL['red']),
        (60, '③ 匹 配 损 失　−%d pp\n高效值模型承接低价值任务\n作用点：任务—模型匹配' % round(ls_['match'] * 100),
         (72, 25.6), (68, 34.5), PAL['red']),
        (88, '④ 效 值 损 失　−%d pp\n产出词元效值低于可达上界\n作用点：效值折算 ' % round(ls_['value'] * 100) + ETA,
         (100, 25.6), (94, 34.5), PAL['red'])]
    for x0, t, p1, p2, col in losses:
        bx(ax, x0, 13, 24, 12, t, fc=C['ltred'], ec=PAL['red'], fs=6.2, lw=1.2, pad=0.3)
        arr(ax, p1, p2, c=col, lw=1.3, ms=11)

    # ---- 上方调度层（虚线反馈作用于转化函数与效值折算） ----
    bx(ax, 28, 64, 80, 16,
       '统 一 调 度 层 ：任 务 — 模 型 最 优 匹 配\n'
       r'任务集 $\mathcal{J}$ × 模型集 $\mathcal{M}$ → 匹配矩阵 $\mathbf{X}$' + '\n'
       '目标：单位算力的有效标准词元产出最大化\n'
       '效果：有效效值利用率 %d%% → %d%%（理论上界 %d%%）'
       % (round(e['effective_util'] * 100), round(e['sched']['matched_util'] * 100),
          round(e['sched']['upper_bound'] * 100)),
       fc='#F4F8FC', ec=PAL['blue'], fs=7.0, lw=1.6, pad=0.35)
    arr(ax, (45, 63.5), (45, 49.6), c=PAL['blue'], lw=1.3, ls=(0, (5, 3)), ms=11)
    txt(ax, 55.5, 57.0, '调度决定批次\n与匹配损失', fs=6.2, c=PAL['blue'])
    arr(ax, (95, 63.5), (95, 49.6), c=PAL['blue'], lw=1.3, ls=(0, (5, 3)), ms=11)
    txt(ax, 105.5, 57.0, '匹配提升产出\n词元的平均效值', fs=6.2, c=PAL['blue'])

    # ---- 底部小结条 ----
    bx(ax, 6, 1, 124, 8.4,
       '名义算力利用率 %d%%　−　空转 %d ＋ 批次 %d ＋ 匹配 %d ＋ 效值 %d ＝ %d 个百分点　→　有效效值利用率 %d%%'
       % (round(e['nominal_util'] * 100), round(ls_['idle'] * 100), round(ls_['batch'] * 100),
          round(ls_['match'] * 100), round(ls_['value'] * 100),
          round((ls_['idle'] + ls_['batch'] + ls_['match'] + ls_['value']) * 100),
          round(e['effective_util'] * 100)),
       fc=C['ltgold'], ec=PAL['gold'], fs=7.4, lw=1.4, bold=True, pad=0.32)

    save(fig, f'{FIG}/fig9_1.png')
    print('ok fig9_1')


# =============================================================== 图10.1
def fig10_1():
    """五类词元运营主体的资产禀赋与职能匹配矩阵。"""
    fig, ax = canvas(12.6, 7.8, 136, 86)

    assets = ['网络与云资源\n骨干网 · 云平台 · 边缘节点',
              '土地·电力·机房\n用地 · 变电容量 · 机架',
              '数据与场景\n行业语料 · 应用场景',
              '制度与政策工具\n标准 · 补贴 · 监管权限']
    subjects = [
        ('基础电信运营商', ['强', '中', '中', '弱'],
         '统一 API 入口与网络接入\n出海通道与跨境合规服务'),
        ('城 投 集 团', ['弱', '强', '弱', '中'],
         '存量机房与电力资产再打包\n算力批发与产能池化'),
        ('数 据 集 团', ['中', '中', '强', '中'],
         '场景数据供给与语料治理\n行业模型适配与效值提升'),
        ('数据交易所', ['弱', '弱', '强', '中'],
         '交易组织与确权登记\n计量凭证发放与结算清分'),
        ('政 策 制 定 者', ['弱', '中', '中', '强'],
         '标准词元计量标准与补贴核定\n价格监测与安全审计')]
    tone = {'强': ('#8FAADC', True), '中': ('#C9D9EC', False), '弱': ('#EDF2F8', False)}

    x_lab, w_lab = 2, 24
    x0, cw, cg = 28, 19, 2.0
    x_fun, w_fun = 112, 22
    rowh, rowg = 11.0, 1.6
    tops = [72 - i * (rowh + rowg) for i in range(5)]

    # 表头
    rc(ax, x_lab, 74, w_lab, 9, fc=C['ltgray'], ec=PAL['gray'], lw=1.1, z=2)
    txt(ax, x_lab + w_lab / 2, 78.5, '运营主体　＼　资产禀赋', fs=7.2, c='#1a1a1a', bold=True)
    for j, a in enumerate(assets):
        rc(ax, x0 + j * (cw + cg), 74, cw, 9, fc=C['ltblue'], ec=PAL['blue'], lw=1.1, z=2)
        txt(ax, x0 + j * (cw + cg) + cw / 2, 78.5, a, fs=6.2, c=PAL['blue'], bold=True)
    rc(ax, x_fun, 74, w_fun, 9, fc=C['ltgold'], ec=PAL['gold'], lw=1.1, z=2)
    txt(ax, x_fun + w_fun / 2, 78.5, '比较优势职能', fs=7.2, c=PAL['gold'], bold=True)

    # 矩阵主体
    for i, (nm, lv, fun) in enumerate(subjects):
        yy = tops[i] - rowh
        rc(ax, x_lab, yy, w_lab, rowh, fc=C['ltgray'], ec=PAL['gray'], lw=1.0, z=2)
        txt(ax, x_lab + w_lab / 2, yy + rowh / 2, nm, fs=7.4, c='#1a1a1a', bold=True)
        for j, s in enumerate(lv):
            fc, bold = tone[s]
            xx = x0 + j * (cw + cg)
            rc(ax, xx, yy, cw, rowh, fc=fc, ec=PAL['blue'], lw=1.0, z=2)
            txt(ax, xx + cw / 2, yy + rowh / 2, s, fs=9.0, c='#12314D', bold=bold)
        rc(ax, x_fun, yy, w_fun, rowh, fc='#FDF8E8', ec=PAL['gold'], lw=1.0, z=2)
        txt(ax, x_fun + w_fun / 2, yy + rowh / 2, fun, fs=6.0, c='#1a1a1a')

    # 匹配强度图示
    txt(ax, 28, 5.4, '匹配强度', fs=7.0, c='#333333', ha='left', bold=True)
    for k, s in enumerate(['强', '中', '弱']):
        xx = 40 + k * 22
        rc(ax, xx, 2.6, 6, 5.6, fc=tone[s][0], ec=PAL['blue'], lw=1.0, z=2)
        lab = {'强': '强：核心禀赋', '中': '中：部分具备', '弱': '弱：需外部协同'}[s]
        txt(ax, xx + 7.2, 5.4, lab, fs=6.6, c='#333333', ha='left')

    save(fig, f'{FIG}/fig10_1.png')
    print('ok fig10_1')


# =============================================================== 图10.2
def fig10_2():
    """“五个统一”的机制设计与交易费用节约，汇入平台价值闭环。"""
    it = R['ahp']['items']
    g = R['game']
    fig, ax = canvas(12.4, 8.0, 136, 88)

    mods = [('统 一 API 入 口\n（组合权重 %.3f）' % it['entry'],
             '搜寻与匹配费用\n多模型比选 · 接口适配的重复投入'),
            ('统 一 计 量\n（组合权重 %.3f）' % it['metering'],
             '计量与验证费用\n口径不一 · 用量与效值反复核对'),
            ('统 一 结 算\n（组合权重 %.3f）' % it['settlement'],
             '支付与对账费用\n多方开票 · 跨主体对账与清分'),
            ('统一政策抵扣\n（组合权重 %.3f）' % it['subsidy'],
             '政策申报费用\n补贴申报 · 材料核验与合规举证'),
            ('统一安全审计\n（组合权重 %.3f）' % it['audit'],
             '合规与审计费用\n数据出境 · 安全评估的重复审计')]
    tops = [80 - i * 15.5 for i in range(5)]

    txt(ax, 18, 83.4, '“五个统一”机制设计', fs=8.4, c=PAL['blue'], bold=True)
    txt(ax, 63, 83.4, '所节约的交易费用类型', fs=8.4, c=PAL['teal'], bold=True)
    txt(ax, 110, 83.4, '平台价值闭环', fs=8.4, c=PAL['orange'], bold=True)

    for i, (m, ct) in enumerate(mods):
        yy = tops[i] - 11.5
        cy0 = yy + 5.75
        bx(ax, 2, yy, 32, 11.5, m, fc=C['ltblue'], ec=PAL['blue'], fs=7.0, lw=1.3, pad=0.3)
        bx(ax, 44, yy, 38, 11.5, ct, fc=C['ltteal'], ec=PAL['teal'], fs=6.6, lw=1.3, pad=0.3)
        arr(ax, (34.5, cy0), (43.4, cy0), c=PAL['gray'], lw=1.3, ms=11)
        # 汇入右侧收集干线
        arr(ax, (82.5, cy0), (88, cy0), c=PAL['teal'], lw=1.1, ms=9)
    ax.plot([88, 88], [12.75, 74.25], color=PAL['teal'], lw=1.4, zorder=3)
    orth(ax, [(88, 74.25), (110, 74.25), (110, 66.6)], c=PAL['teal'], lw=1.4, ms=12)

    # 右侧价值闭环链
    chain = [('交易费用总节约\n' + r'$\tau$' + '＝%.2f' % g['params']['tau_save'], C['ltgold'], PAL['gold']),
             ('企业采纳净收益上升\n' + RFS + ' 越过临界值 %.2f' % g['threshold']['RF_crit'],
              C['ltorange'], PAL['orange']),
             ('用量规模扩大\n平台规模经济显现', C['ltorange'], PAL['orange']),
             ('单位成本与价格下行\n采纳门槛进一步降低', C['ltorange'], PAL['orange'])]
    cy = [57, 42, 27, 12]
    for k, (t, fc, ec) in enumerate(chain):
        bx(ax, 94, cy[k], 32, 9, t, fc=fc, ec=ec, fs=6.4, lw=1.3, pad=0.28)
        if k < 3:
            arr(ax, (110, cy[k] - 0.4), (110, cy[k + 1] + 9.4), c=PAL['orange'], lw=1.3, ms=11)
    # 正反馈闭环
    orth(ax, [(126.4, 16.5), (131, 16.5), (131, 61.5), (126.4, 61.5)],
         c=PAL['red'], lw=1.3, ls=(0, (5, 3)), ms=11)
    txt(ax, 133.4, 39, '正反馈闭环', fs=6.4, c=PAL['red'], rot=90)

    save(fig, f'{FIG}/fig10_2.png')
    print('ok fig10_2')


# =============================================================== 图11.1
def fig11_1():
    """词元能耗—碳足迹核算框架＋可信溯源链路。"""
    gr = R['green']
    ca = gr['carbon']
    fig, ax = canvas(12.6, 7.7, 138, 84)

    # ---- 上排：核算链条 ----
    steps = [('① 算 力 功 耗\nIT 设备功率 $P$（kW）\n分档位耗电 %.1f — %.1f\nkWh／百万 ' %
              (gr['energy_kwh_per_m_ste']['light'], gr['energy_kwh_per_m_ste']['reason']) + TT,
              C['ltteal'], PAL['teal']),
             ('② PUE 修 正\n数据中心用电量 $E$\n$E=P\\times PUE\\times t$',
              C['ltblue'], PAL['blue']),
             ('③ 排 放 因 子\n电网 %.2f／绿电 %.2f\nkg' % (ca['grid_factor'], ca['green_factor'])
              + CO2 + '／kWh\n绿电占比 %d%%（2026）' % round(gr['mix']['2026'] * 100),
              C['ltgold'], PAL['gold']),
             ('④ 碳 排 放 量\n$C_{e}=E\\times f$\n（kg' + CO2E + '）',
              C['ltorange'], PAL['orange']),
             ('⑤ 碳 强 度 ' + IOTA + '\n' + IOTA + r'$=C_{e}/\tilde{T}$' +
              '\n现状均值 %d g' % ca['iota_avg'] + CO2E + '／千' + TT,
              C['ltred'], PAL['red'])]
    xs = [1.5, 29.5, 57.5, 85.5, 113.5]
    for k, (t, fc, ec) in enumerate(steps):
        bx(ax, xs[k], 66, 23, 15, t, fc=fc, ec=ec, fs=6.2, lw=1.5, pad=0.32)
    for k in range(4):
        arr(ax, (xs[k] + 23.4, 73.5), (xs[k + 1] - 0.4, 73.5), c=PAL['gray'], lw=1.5, ms=12)

    # ---- 阈值判定（菱形） ----
    arr(ax, (125, 65.6), (125, 57.4), c=PAL['red'], lw=1.5, ms=12)
    ax.add_patch(Polygon([(113, 49), (125, 57), (137, 49), (125, 41)], closed=True,
                         fc=C['ltred'], ec=PAL['red'], lw=1.5, zorder=2))
    txt(ax, 125, 49, '绿色词元阈值\n' + IOTA + r'$\leq$' + '%d ？' % gr['threshold_iota'],
        fs=6.6, c=PAL['red'], bold=True)

    # ---- 否：减排路径，虚线反馈至排放因子 ----
    bx(ax, 57, 42, 24, 14, '未达阈值：减排路径\n绿电直供 · 算电协同\nPUE 优化 · 错峰调度',
       fc=C['ltgray'], ec=PAL['gray'], fs=6.2, lw=1.3, pad=0.3)
    arr(ax, (112.6, 49), (81.6, 49), c=PAL['gray'], lw=1.3, ms=11)
    txt(ax, 97, 51.4, '否', fs=7.2, c=PAL['gray'], bold=True)
    arr(ax, (69, 56.6), (69, 65.6), c=PAL['green'], lw=1.3, ls=(0, (5, 3)), ms=11)
    txt(ax, 71.5, 61.0, '提高绿电占比\n→ 排放因子下降', fs=6.2, c=PAL['green'], ha='left')

    # ---- 是：绿色词元 → 碳足迹凭证 ----
    arr(ax, (125, 40.6), (125, 36.6), c=PAL['green'], lw=1.5, ms=12)
    txt(ax, 128.4, 38.6, '是', fs=7.2, c=PAL['green'], bold=True)
    bx(ax, 113, 22, 24, 14, '绿 色 词 元 ' + TG + '\n' + IOTA + '＝%d g' % ca['iota_green']
       + CO2E + '／千' + TT + '\n支付意愿溢价 %.1f%%' % (gr['premium']['coef'] * 100),
       fc=C['ltgreen'], ec=PAL['green'], fs=6.2, lw=1.5, pad=0.3)
    arr(ax, (125, 21.6), (125, 18.6), c=PAL['green'], lw=1.5, ms=12)
    bx(ax, 95, 4, 42, 14, '碳 足 迹 凭 证\n随标准词元签发 · 可核验 · 可互认\n支撑出海碳合规与绿色采购',
       fc=C['ltgold'], ec=PAL['gold'], fs=6.6, lw=1.6, pad=0.32)

    # ---- 可信溯源链路 ----
    group(ax, 1, 2, 90, 36, '可 信 溯 源 链 路 ：全 过 程 可 追 溯', c=PAL['purple'], fs=7.8, lx=46)
    tr = [('数 据 传 输\n加密通道 · 数据出境合规', 4),
          ('模 型 调 用\n调用日志 · 用量与效值留痕', 33),
          ('业 务 落 地\n结果归档 · 价值与责任可溯', 62)]
    for t, xx in tr:
        bx(ax, xx, 20, 26, 12, t, fc=C['ltpurple'], ec=PAL['purple'], fs=6.4, lw=1.3, pad=0.3)
    arr(ax, (30.4, 26), (32.6, 26), c=PAL['purple'], lw=1.3, ms=10)
    arr(ax, (59.4, 26), (61.6, 26), c=PAL['purple'], lw=1.3, ms=10)
    bx(ax, 4, 6, 84, 8, '存证层：时间戳 · 内容哈希 · 主体标识 —— 与碳足迹凭证一一对应',
       fc='#F5F2FA', ec=PAL['purple'], fs=6.8, lw=1.3, pad=0.3)
    for xx in (17, 46, 75):
        arr(ax, (xx, 19.6), (xx, 14.6), c=PAL['purple'], lw=1.2, ms=10)
    arr(ax, (88.5, 10), (94.4, 10), c=PAL['gold'], lw=1.4, ms=11)
    txt(ax, 91.4, 12.6, '绑定', fs=6.2, c=PAL['gold'])

    save(fig, f'{FIG}/fig11_1.png')
    print('ok fig11_1')


# =============================================================== 图12.1
def fig12_1():
    """增长核算框架对照：传统核算 vs 本书核算，中间大箭头标注引入词元流量。"""
    pf = R['growth']['prodfn']
    tb = R['growth']['tfp_bias']
    dc = R['growth']['decomp']['2026']
    fig, ax = canvas(12.2, 8.2, 132, 88)

    # ================= 左栏：传统核算 =================
    rc(ax, 2, 2, 52, 78, fc='none', ec=PAL['gray'], lw=1.1, ls=(0, (4, 3)), z=1)
    txt(ax, 28, 82.4, '传 统 增 长 核 算', fs=9.6, c=PAL['gray'], bold=True)
    bx(ax, 6, 62, 18, 8, '资　本\n$K$', fc=C['ltgray'], ec=PAL['gray'], fs=7.2, lw=1.2, pad=0.28)
    bx(ax, 32, 62, 18, 8, '劳　动\n$L$', fc=C['ltgray'], ec=PAL['gray'], fs=7.2, lw=1.2, pad=0.28)
    bx(ax, 15, 46, 26, 8, '产　出　$Y$', fc=C['ltgray'], ec=PAL['gray'], fs=8.0, lw=1.4, pad=0.28)
    arr(ax, (15, 61.6), (22, 54.5), c=PAL['gray'], lw=1.3, ms=11)
    arr(ax, (41, 61.6), (34, 54.5), c=PAL['gray'], lw=1.3, ms=11)
    arr(ax, (28, 45.6), (28, 40.6), c=PAL['gray'], lw=1.5, ms=12)
    txt(ax, 30.0, 43.0, '扣除 $K$、$L$ 贡献', fs=6.2, c=PAL['gray'], ha='left')
    bx(ax, 6, 14, 44, 26, '', fc='#F2ECEC', ec=PAL['red'], lw=2.0)
    txt(ax, 28, 34.0, '索 洛 残 差　TFP', fs=10.0, c=PAL['red'], bold=True)
    txt(ax, 28, 27.5, '%.2f%%／年' % tb['without_token'], fs=12.0, c=PAL['red'], bold=True)
    txt(ax, 28, 20.0, '含 AI 贡献，无法分离\n（技术进步 · 效率改善 · AI 应用混同）',
        fs=7.2, c='#1a1a1a')
    bx(ax, 6, 4, 44, 8, 'AI 的增长贡献沉入残差\n不可观测 · 不可归因 · 不可考核',
       fc=C['ltred'], ec=PAL['red'], fs=6.8, lw=1.2, pad=0.28)

    # ================= 中间：引入词元流量 =================
    ax.add_patch(Polygon([(56, 38), (67, 38), (67, 33), (75, 42), (67, 51), (67, 46), (56, 46)],
                         closed=True, fc=C['ltgold'], ec=PAL['gold'], lw=1.6, zorder=2))
    txt(ax, 65.5, 57.5, '引入可观测的\n标准词元流量 ' + TT, fs=7.6, c=PAL['gold'], bold=True)
    txt(ax, 65.5, 27.0, '残差\n%.2f%% → %.2f%%\n（高估 %.2f pp）'
        % (tb['without_token'], tb['with_token'], tb['overstate']), fs=7.0, c=PAL['gold'])

    # ================= 右栏：本书核算 =================
    rc(ax, 76, 2, 54, 78, fc='none', ec=PAL['blue'], lw=1.1, ls=(0, (4, 3)), z=1)
    txt(ax, 103, 82.4, '本 书 增 长 核 算 框 架', fs=9.6, c=PAL['blue'], bold=True)
    ins = [('资本\n$K$\n' + r'$\alpha_K$' + '＝%.3f' % pf['lnK']['coef'], 78, C['ltgray'], PAL['gray']),
           ('劳动\n$L$\n' + r'$\alpha_L$' + '＝%.3f' % pf['lnL']['coef'], 91, C['ltgray'], PAL['gray']),
           ('数据\n$D$\n' + r'$\alpha_D$' + '＝%.3f' % pf['lnD']['coef'], 104, C['ltteal'], PAL['teal']),
           ('标准词元\n' + TT + '\n' + AT + '＝%.3f' % pf['lnT']['coef'], 117, C['ltblue'], PAL['blue'])]
    for t, xx, fc, ec in ins:
        bx(ax, xx, 60, 11, 10, t, fc=fc, ec=ec, fs=5.8, lw=1.3, pad=0.26)
    bx(ax, 88, 46, 30, 8, '产　出　$Y$', fc=C['ltgreen'], ec=PAL['green'], fs=8.0, lw=1.4, pad=0.28)
    for xx, tx in [(83.5, 94), (96.5, 100), (109.5, 106), (122.5, 112)]:
        arr(ax, (xx, 59.6), (tx, 54.5), c=PAL['gray'], lw=1.2, ms=10)
    arr(ax, (103, 45.6), (103, 42.6), c=PAL['green'], lw=1.5, ms=12)
    bx(ax, 92, 32, 22, 10, '残差 TFP\n%.2f%%／年' % tb['with_token'],
       fc='#F2ECEC', ec=PAL['red'], fs=7.8, lw=1.8, bold=True, pad=0.28)
    bx(ax, 78, 6, 50, 20,
       'AI 贡献已显性分离\n'
       '标准词元流量弹性 ' + AT + '＝%.3f（$t$＝%.2f，1%% 水平显著）\n' % (pf['lnT']['coef'], pf['lnT']['t']) +
       '2026 年直接贡献 %.2f 个百分点，占产出增长 %.1f%%\n' % (dc['cT'], dc['share_T'] * 100) +
       '残差高估 %.2f 个百分点被纠正' % tb['overstate'],
       fc=C['ltblue'], ec=PAL['blue'], fs=7.0, lw=1.4, pad=0.32)

    save(fig, f'{FIG}/fig12_1.png')
    print('ok fig12_1')


# =============================================================== 图13.1
def fig13_1():
    """多案例分析框架：五城×五维矩阵 → 跨案例比较 → 三角验证。"""
    cs = R['cases']['cities']
    order = ['jx', 'sz', 'wz', 'gz', 'sh']
    fig, ax = canvas(11.4, 9.2, 124, 100)

    dims = ['接入便利', '计量透明', '成本可控', '合规可信', '生态丰度']
    x0, cw, cg = 25, 18, 1.5
    x_lab, w_lab = 2, 20

    # 案例列表头
    for j, k in enumerate(order):
        xx = x0 + j * (cw + cg)
        bx(ax, xx, 88, cw, 9, cs[k]['name'] + '\n' + cs[k]['subject'] + '主导',
           fc=C['ltblue'], ec=PAL['blue'], fs=6.6, lw=1.3, pad=0.26)
    txt(ax, x_lab + w_lab / 2, 92.5, '能力维度', fs=7.4, c='#1a1a1a', bold=True)

    # 矩阵
    for i, d in enumerate(dims):
        yy = 78 - i * 8.5
        rc(ax, x_lab, yy, w_lab, 7.5, fc=C['ltgray'], ec=PAL['gray'], lw=1.0, z=2)
        txt(ax, x_lab + w_lab / 2, yy + 3.75, d, fs=7.0, c='#1a1a1a', bold=True)
        for j in range(5):
            xx = x0 + j * (cw + cg)
            rc(ax, xx, yy, cw, 7.5, fc='white', ec=PAL['blue'], lw=0.9, z=2)
            txt(ax, xx + cw / 2, yy + 3.75, '$e_{%d%d}$' % (i + 1, j + 1),
                fs=8.0, c='#555555')
    txt(ax, 62, 40.6,
        '$e_{ij}$：案例 $j$ 在能力维度 $i$ 上的证据编码（深度访谈 · 政策文件 · 实地观察三源互证）',
        fs=6.6, c='#666666')

    arr(ax, (62, 38.6), (62, 34.6), c=PAL['gray'], lw=1.5, ms=12)
    bx(ax, 14, 26, 96, 8, '跨 案 例 比 较：模式求同（复制逻辑）　·　差异归因（资产禀赋条件与机制组合）',
       fc=C['ltgold'], ec=PAL['gold'], fs=7.6, lw=1.4, pad=0.3)
    arr(ax, (62, 25.6), (62, 21.6), c=PAL['gold'], lw=1.5, ms=12)

    bx(ax, 44, 5, 36, 16, '三 角 验 证\n案例证据 × 定量结论 × 理论预期\n检验结论的收敛性与稳健性',
       fc=C['ltred'], ec=PAL['red'], fs=7.4, lw=1.6, bold=True, pad=0.32)
    bx(ax, 2, 5, 36, 16,
       '定 量 结 论\n效值离散度收敛（第5章）\nTPI／STPI 背离（第7章）\n四项损失与调度改进（第9章）\n词元流量增长贡献（第12章）',
       fc=C['ltgray'], ec=PAL['gray'], fs=6.2, lw=1.2, pad=0.3)
    bx(ax, 86, 5, 36, 16,
       '理 论 预 期\n统一计量降低交易费用\n统一入口提升接入便利\n三层结构解释成本分化\n绿色凭证支撑合规溢价',
       fc=C['ltgray'], ec=PAL['gray'], fs=6.2, lw=1.2, pad=0.3)
    arr(ax, (38.5, 13), (43.4, 13), c=PAL['gray'], lw=1.4, ms=11)
    arr(ax, (85.5, 13), (80.6, 13), c=PAL['gray'], lw=1.4, ms=11)

    save(fig, f'{FIG}/fig13_1.png')
    print('ok fig13_1')


# =============================================================== 图13.3
def fig13_3():
    """扎根理论编码结构：访谈 → 开放编码 → 主轴编码 → 核心范畴 → 改进路径。"""
    iv = R['cases']['interviews']
    cd = R['cases']['coding']
    ct = R['cases']['categories']
    cn = R['cases']['category_cn']
    n = iv['platform'] + iv['enterprise'] + iv['govt'] + iv['vendor']
    fig, ax = canvas(11.4, 8.6, 124, 94)

    bx(ax, 8, 82, 108, 9,
       '访谈样本：深度访谈 %d 份　　平台方 %d · 企业方 %d · 政府方 %d · 服务商 %d'
       % (n, iv['platform'], iv['enterprise'], iv['govt'], iv['vendor']),
       fc=C['ltgray'], ec=PAL['gray'], fs=7.6, lw=1.3, pad=0.3)
    arr(ax, (62, 81.6), (62, 77.6), c=PAL['gray'], lw=1.5, ms=12)

    bx(ax, 16, 68, 92, 9, '开 放 编 码：逐句概念化　→　%d 个初始概念' % cd['open'],
       fc=C['ltblue'], ec=PAL['blue'], fs=7.8, lw=1.4, pad=0.3)
    arr(ax, (62, 67.6), (62, 63.6), c=PAL['blue'], lw=1.5, ms=12)

    bx(ax, 24, 54, 76, 9, '主 轴 编 码：归并聚类　→　%d 个副范畴' % cd['axial'],
       fc=C['ltteal'], ec=PAL['teal'], fs=7.8, lw=1.4, pad=0.3)
    bx(ax, 101.5, 54, 21, 9, '理论饱和检验\n后续访谈未再\n涌现新的范畴',
       fc='white', ec=PAL['gray'], fs=6.0, lw=1.0, ls=(0, (4, 3)), pad=0.26)
    ax.plot([100.4, 101.1], [58.5, 58.5], color=PAL['gray'], lw=1.0,
            linestyle=(0, (2, 2)), zorder=3)

    # 核心编码：四大主范畴（括号内为参考点频次）
    cats = [('① ' + cn['metering'], ct['metering'], '用量口径不一\n效值不可核验'),
            ('② ' + cn['cost'], ct['cost'], '价格波动频繁\n年度预算不可控'),
            ('③ ' + cn['capability'], ct['capability'], '提示工程与系统\n集成能力不足'),
            ('④ ' + cn['trust'], ct['trust'], '数据出境 · 审计\n与责任界定模糊')]
    paths = ['统一计量与用量可视\n效值系数公示核验',
             '标准词元价格指数\n阶梯报价与预算包',
             '场景模板与集成\n服务包 · 陪跑培训',
             '统一安全审计与\n可信溯源凭证']
    xs = [7.5, 35.5, 63.5, 91.5]
    cxs = [x + 12.5 for x in xs]

    ax.plot([62, 62], [53.6, 51], color=PAL['teal'], lw=1.5, zorder=3)
    ax.plot([cxs[0], cxs[-1]], [51, 51], color=PAL['teal'], lw=1.5, zorder=3)
    for k, (nm, freq, det) in enumerate(cats):
        arr(ax, (cxs[k], 51), (cxs[k], 48.6), c=PAL['teal'], lw=1.5, ms=11)
        bx(ax, xs[k], 34, 25, 14, '核心范畴 ' + nm + '\n（参考点 %d）\n' % freq + det,
           fc=C['ltred'], ec=PAL['red'], fs=6.4, lw=1.4, pad=0.3)
        arr(ax, (cxs[k], 33.6), (cxs[k], 28.6), c=PAL['red'], lw=1.4, ms=11)
        bx(ax, xs[k], 18, 25, 10, paths[k], fc=C['ltgreen'], ec=PAL['green'],
           fs=6.4, lw=1.3, pad=0.28)
        ax.plot([cxs[k], cxs[k]], [17.6, 14], color=PAL['green'], lw=1.4, zorder=3)
    txt(ax, 62, 30.9, '改 进 路 径', fs=7.0, c=PAL['green'], bold=True)

    ax.plot([cxs[0], cxs[-1]], [14, 14], color=PAL['green'], lw=1.4, zorder=3)
    arr(ax, (62, 14), (62, 11.6), c=PAL['green'], lw=1.5, ms=12)
    bx(ax, 16, 2, 92, 9.5,
       '改进路径汇总：降低企业采纳门槛，提升深度采纳净收益 ' + RFS + '\n'
       '（对接第10章“五个统一”机制设计与三方演化博弈的激励相容条件）',
       fc=C['ltgold'], ec=PAL['gold'], fs=7.0, lw=1.4, pad=0.3)

    save(fig, f'{FIG}/fig13_3.png')
    print('ok fig13_3')


# =============================================================== 图14.1
def fig14_1():
    """政策体系框架：目标横条 → 计量／定价／配置三支柱 → 标准与统计基础设施横条。"""
    gr = R['green']
    e = R['eff']
    fig, ax = canvas(11.6, 8.8, 126, 96)

    bx(ax, 3, 84, 120, 10,
       '“十五五”时期词元经济治理目标\n'
       '以标准词元 ' + TT + ' 为价值锚点，建成可计量、可定价、可配置、可核证的智能经济计量与治理体系',
       fc=C['ltred'], ec=PAL['red'], fs=8.4, lw=1.7, bold=True, pad=0.35)

    pillars = [
        ('计 量 侧\n统一计量口径', C['ltblue'], PAL['blue'],
         ['制定标准词元计量国家标准\n明确效值系数 ' + ETA + ' 的测算与公示规则',
          '建立基准任务集与效值认证\n第三方核验 · 定期复评与追溯',
          '用量与效值双口径统计\n纳入数字经济统计调查制度',
          '推动跨模型可比与跨境互认\n对接国际当量折算规则']),
        ('定 价 侧\n公允价格形成', C['ltteal'], PAL['teal'],
         ['编制并发布词元价格指数\nTPI 与 STPI 双轨定期发布',
          '三层价格结构的信息披露\n成本底价 · 效值溢价 · 场景租金',
          '分级服务与普惠定价\n普惠包 · 按需套餐 · 专属定制',
          '治理效值虚标与信息不对称\n防范低效值词元的逆向选择']),
        ('配 置 侧\n效率与绿色', C['ltgreen'], PAL['green'],
         ['建设统一调度平台\n任务—模型匹配与产能池化',
          '补贴由建算力转向用词元\n技改补贴与政策抵扣相挂钩',
          '有效利用率纳入考核\n现状 %d%% → 目标 %d%%（上界 %d%%）'
          % (round(e['effective_util'] * 100), round(e['sched']['matched_util'] * 100),
             round(e['sched']['upper_bound'] * 100)),
          '绿色词元认证与碳足迹凭证\n碳强度阈值 %.1f g' % gr['threshold_iota'] + CO2E + '／千' + TT])]
    px = [3, 44, 85]
    for k, (hd, fc, ec, pts) in enumerate(pillars):
        x = px[k]
        rc(ax, x, 24, 38, 57, fc='none', ec=ec, lw=1.1, ls=(0, (4, 3)), z=1)
        bx(ax, x + 1, 72, 36, 8, hd, fc=ec, ec=ec, fs=8.0, tc='white', bold=True, pad=0.3)
        arr(ax, (x + 19, 83.6), (x + 19, 80.6), c=PAL['red'], lw=1.5, ms=12)
        for i, t in enumerate(pts):
            bx(ax, x + 2, 60 - i * 11, 34, 9, t, fc=fc, ec=ec, fs=6.4, lw=1.1, pad=0.26)
        arr(ax, (x + 19, 23.6), (x + 19, 20.6), c=ec, lw=1.4, ls=(0, (5, 3)),
            ms=11, style='<|-|>')

    bx(ax, 3, 6, 120, 14, '', fc='#FBFAF4', ec=PAL['gold'], lw=1.7)
    txt(ax, 63, 17.3, '标 准 与 统 计 基 础 设 施（支撑三侧政策的实施、监测与动态校准）',
        fs=8.0, c=PAL['gold'], bold=True)
    base = ['标准词元计量\n国家标准与检测方法',
            '词元价格指数\n定期发布与监测平台',
            '调度效率与\n有效利用率考核体系',
            '绿色词元认证\n与国际互认机制']
    for i, t in enumerate(base):
        bx(ax, 4.5 + i * 30, 7.5, 27, 7.4, t, fc=C['ltgold'], ec=PAL['gold'],
           fs=6.2, lw=1.1, pad=0.26)

    save(fig, f'{FIG}/fig14_1.png')
    print('ok fig14_1')


ALL = [fig8_1, fig9_1, fig10_1, fig10_2, fig11_1, fig12_1, fig13_1, fig13_3, fig14_1]

if __name__ == '__main__':
    for f in ALL:
        f()
    print('diagrams_b done:', len(ALL))
