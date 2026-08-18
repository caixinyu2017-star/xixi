# -*- coding: utf-8 -*-
"""《标准词元与智能经济》前半部机制图（D 型，8 幅）。

fig1_1 研究技术路线／fig1_2 全书结构／fig2_2 理论基础与研究框架逻辑／fig3_1 词元属性谱系／
fig5_1 标准词元效值折算体系框架／fig6_1 价值创造的劳动凝结结构／
fig6_2 价值实现与增值循环／fig7_1 词元价格三层结构。

铁律：图内不写图名、图注与资料来源；标签全中文（数学符号走 mathtext）；
只用直线与正交折线（rad=0）；浅色填充＋深色描边；无图标与剪贴画。
"""
import os
import re

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

from matplotlib.font_manager import fontManager, FontEntry

from figstyle import save, PAL, CJK  # noqa: F401

# 注册中文粗体字面（figstyle 仅注册常规字面），使小标题的加粗真正生效
fontManager.ttflist.append(FontEntry(
    fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', name=CJK,
    style='normal', variant='normal', weight=700, stretch='normal', size='scalable'))

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figs')
os.makedirs(FIG, exist_ok=True)

C = dict(blue='#1F4E79', ltblue='#DCE6F1', orange='#C55A11', ltorange='#FCE4D6',
         teal='#2E8B8B', ltteal='#D9EBEB', gold='#BF9000', ltgold='#FFF2CC',
         green='#548235', ltgreen='#E4EFDC', red='#A02020', ltred='#F7DDDD',
         gray='#7F7F7F', ltgray='#EFEFEF', purple='#674EA7', ltpurple='#E7E2F2',
         ink='#1A1A1A', sub='#333333')

_SC = [0.1]      # 每个数据单位对应的英寸数（canvas 设定，x、y 各向同性）
_WARN = []


# ============================ 通用辅助 ============================
def canvas(W, H, win):
    """建立等比画布：W×H 数据单位，图宽 win 英寸（1 单位＝win/W 英寸，x、y 同尺度）。"""
    fig, ax = plt.subplots(figsize=(win, win * H / float(W)))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis('off')
    ax.grid(False)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    _SC[0] = win / float(W)
    return fig, ax


def _cw(s):
    """粗估一行文本的字符宽度（以 1 个汉字为 1 单位）。"""
    s = re.sub(r'\\[a-zA-Z]+', 'M', s)
    for ch in '${}^_\\ ':
        s = s.replace(ch, '' if ch != ' ' else ' ')
    w = 0.0
    for ch in s:
        w += 1.0 if ord(ch) > 0x2E7F else 0.58
    return w


def _need(text, fs):
    """返回文本所需的（宽, 高），单位为数据单位。"""
    lines = text.split('\n')
    wmax = max(_cw(ln) for ln in lines)
    return wmax * fs / 72.0 / _SC[0], len(lines) * fs * 1.42 / 72.0 / _SC[0]


def _check(tag, text, fs, w, h, mw=1.4, mh=0.9):
    nw, nh = _need(text, fs)
    if nw > w - mw:
        _WARN.append('宽溢出 %-10s 需%.1f 有%.1f ｜%s' % (tag, nw, w, text.split('\n')[0]))
    if nh > h - mh:
        _WARN.append('高溢出 %-10s 需%.1f 有%.1f ｜%s' % (tag, nh, h, text.split('\n')[0]))


def bx(ax, x, y, w, h, text, fc=C['ltblue'], ec=None, fs=8.0, lw=1.1, ls='solid',
       tc=C['ink'], bold=False, pad=0.4, rot=0, z=2, tag=''):
    """圆角方框＋居中文本。"""
    ec = ec or C['blue']
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=%.2f' % pad,
                                fc=fc, ec=ec, lw=lw, linestyle=ls, zorder=z))
    ax.text(x + w / 2., y + h / 2., text, ha='center', va='center', fontsize=fs,
            color=tc, rotation=rot, zorder=z + 2, linespacing=1.42,
            fontweight='bold' if bold else 'normal')
    _check(tag or text[:6], text, fs, w if rot == 0 else h, h if rot == 0 else w)


def bx2(ax, x, y, w, h, title, sub, fc=C['ltblue'], ec=None, fs=8.0, fs2=6.5,
        lw=1.1, ls='solid', pad=0.4, z=2, tc=None, sc=C['sub'], tag=''):
    """圆角方框＋首行小标题（加粗）＋下方说明文字。"""
    ec = ec or C['blue']
    tc = tc or ec
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=%.2f' % pad,
                                fc=fc, ec=ec, lw=lw, linestyle=ls, zorder=z))
    th = fs * 1.42 / 72.0 / _SC[0]
    nh = len(sub.split('\n')) * fs2 * 1.42 / 72.0 / _SC[0] if sub else 0.0
    gapv = 0.35 * th if sub else 0.0
    tot = th + gapv + nh
    top = y + h / 2. + tot / 2.
    ax.text(x + w / 2., top - th / 2., title, ha='center', va='center', fontsize=fs,
            color=tc, fontweight='bold', zorder=z + 2, linespacing=1.42)
    if sub:
        ax.text(x + w / 2., top - th - gapv - nh / 2., sub, ha='center', va='center',
                fontsize=fs2, color=sc, zorder=z + 2, linespacing=1.42)
    _check(tag or title, title, fs, w, h, mh=-1e6)
    if sub:
        _check(tag or title, sub, fs2, w, h, mh=-1e6)
    if tot > h - 0.8:
        _WARN.append('高溢出 %-10s 需%.1f 有%.1f ｜%s' % (tag or title, tot, h, title))


def arr(ax, p1, p2, c=C['gray'], lw=1.2, ls='solid', ms=11, z=1, style='-|>'):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms, color=c,
                                 lw=lw, linestyle=ls, connectionstyle='arc3,rad=0',
                                 shrinkA=0, shrinkB=0, zorder=z))


def poly(ax, pts, c=C['gray'], lw=1.2, ls='solid', ms=11, z=1, arrow=True):
    """正交折线（末段带箭头）。"""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    if arrow:
        ax.plot(xs[:-1], ys[:-1], color=c, lw=lw, ls=ls, zorder=z, solid_capstyle='round')
        arr(ax, pts[-2], pts[-1], c=c, lw=lw, ls=ls, ms=ms, z=z)
    else:
        ax.plot(xs, ys, color=c, lw=lw, ls=ls, zorder=z, solid_capstyle='round')


def txt(ax, x, y, s, fs=7.0, c=C['sub'], ha='center', va='center', bold=False, rot=0,
        z=5, bg=None):
    kw = {}
    if bg:
        kw['bbox'] = dict(boxstyle='round,pad=0.2', fc='white', ec=bg, lw=0.7)
    ax.text(x, y, s, fontsize=fs, color=c, ha=ha, va=va, rotation=rot, zorder=z,
            linespacing=1.4, fontweight='bold' if bold else 'normal', **kw)


def frame(ax, x0, y0, x1, y1, ec=C['gray'], lw=0.9, ls=(0, (5, 3)), z=0, fc='none'):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec=ec, lw=lw,
                           linestyle=ls, zorder=z))


def done(fig, name):
    save(fig, os.path.join(FIG, name + '.png'))
    print('ok', name)


# ==================================================== 图1.1 研究技术路线
def fig1_1():
    fig, ax = canvas(100, 100, 10.0)
    L, R0 = 18.0, 95.0                    # 主体栏左右边界
    # ---- 主线：标准词元贯穿（左侧纵栏）
    bx(ax, 2.0, 7.0, 11.5, 65.0,
       '标准词元 $\\tilde{T}=\\eta T$：贯穿计量—定价—配置的统一主线\n'
       '价值尺度·定价基准·配置信号·增长核算变量',
       fc=C['ltorange'], ec=C['orange'], fs=8.6, lw=1.5, rot=90, tc=C['orange'],
       bold=True, tag='主线')
    # ---- A 现实问题
    bx(ax, 3.0, 90.5, 92.0, 8.0,
       '现实问题：物理词元不等值\n'
       '同名 1 枚词元，各档位模型的算力消耗、任务达成度与场景价值相差数倍乃至十倍以上，不可比、不可加',
       fc=C['ltred'], ec=C['red'], fs=9.0, lw=1.4, tag='现实问题')
    # ---- B 四项后果
    bs = [('定价无公允基准', '同类服务报价跨度达 12.6 倍'),
          ('补贴无核定依据', '按物理词元量核定技改补贴失真'),
          ('统计无可加口径', '跨模型词元量不可直接加总'),
          ('出海无互认凭证', '缺乏效值与碳足迹互认标尺')]
    bw, bg = 17.75, 2.0
    bxs = [L + i * (bw + bg) for i in range(4)]
    for i, (t, s) in enumerate(bs):
        bx2(ax, bxs[i], 79.0, bw, 6.4, t, s, fc=C['ltred'], ec=C['red'],
            fs=7.8, fs2=6.2, tag='后果%d' % (i + 1))
        arr(ax, (bxs[i] + bw / 2, 90.1), (bxs[i] + bw / 2, 86.0), c=C['red'], lw=1.1)
    # ---- C 三个科学问题
    cw_, cg = 24.33, 2.0
    cxs = [L + i * (cw_ + cg) for i in range(3)]
    cq = [('科学问题一　计量',
           '词元的经济价值由什么决定？\n异质词元如何折算为可比、\n可加的标准计量单位？'),
          ('科学问题二　定价',
           '标准词元的价格如何形成\n与演化？词元市场呈现\n何种结构与均衡？'),
          ('科学问题三　配置与增长',
           '词元如何在算力、模型与场景\n之间有效配置？其增长贡献\n如何测度？')]
    for i, (t, s) in enumerate(cq):
        bx2(ax, cxs[i], 60.0, cw_, 11.6, t, s, fc=C['ltgold'], ec=C['gold'],
            fs=8.2, fs2=7.0, tag='问题%d' % (i + 1))
    # B→C 汇流母线
    ax.plot([bxs[0] + bw / 2, bxs[3] + bw / 2], [75.5, 75.5], color=C['gray'], lw=1.0, zorder=1)
    for i in range(4):
        ax.plot([bxs[i] + bw / 2] * 2, [78.6, 75.5], color=C['gray'], lw=1.0, zorder=1)
    for i in range(3):
        arr(ax, (cxs[i] + cw_ / 2, 75.5), (cxs[i] + cw_ / 2, 72.1), c=C['gray'], lw=1.1)
    # ---- D 三大模块
    dm = [('计量模块（第3、5、6章）',
           '技术与经济属性谱系\n三维效值 $P$／$R$／$S$ 与公理化折算\n价值创造、实现与增值'),
          ('定价模块（第7、8章）',
           '三层价格结构与价格地板\n价格指数 TPI／STPI 编制\n需求弹性与市场均衡'),
          ('配置与增长模块（第9—12章）',
           '转化效率 $\\theta$ 与四项损失分解\n任务—模型匹配与统一调度\n绿色词元与增长核算')]
    for i, (t, s) in enumerate(dm):
        bx2(ax, cxs[i], 42.0, cw_, 12.4, t, s, fc=C['ltblue'], ec=C['blue'],
            fs=8.2, fs2=7.0, lw=1.3, tag='模块%d' % (i + 1))
        arr(ax, (cxs[i] + cw_ / 2, 59.6), (cxs[i] + cw_ / 2, 55.0), c=C['gold'], lw=1.2)
        arr(ax, (cxs[i] + cw_ / 2, 41.6), (cxs[i] + cw_ / 2, 37.0), c=C['blue'], lw=1.2)
    # ---- E 实践与治理
    em = [('城市词元运营中心（第10章）', '五类主体的资产禀赋—职能匹配\n「五个统一」与三方演化博弈'),
          ('绿色词元与可信溯源（第11章）', '能耗核算·碳强度 $\\iota$ 与阈值\n绿电协同与出海碳合规'),
          ('区域实践与多案例（第13章）', '五城模式跨案例比较\n与定量结论三角验证')]
    for i, (t, s) in enumerate(em):
        bx2(ax, cxs[i], 25.0, cw_, 11.0, t, s, fc=C['ltteal'], ec=C['teal'],
            fs=8.0, fs2=6.8, tag='实践%d' % (i + 1))
        arr(ax, (cxs[i] + cw_ / 2, 24.6), (cxs[i] + cw_ / 2, 20.0), c=C['teal'], lw=1.2)
    # ---- F 政策转化
    fm = [('政策转化·计量侧', '标准词元计量国家标准\n与统计口径建设'),
          ('政策转化·定价侧', '价格指数发布与\n市场价格监测'),
          ('政策转化·配置侧', '调度效率考核·绿色认证\n与国际互认')]
    for i, (t, s) in enumerate(fm):
        bx2(ax, cxs[i], 8.5, cw_, 10.8, t, s, fc=C['ltgreen'], ec=C['green'],
            fs=8.0, fs2=6.8, lw=1.3, tag='政策%d' % (i + 1))
    txt(ax, (cxs[0] + cxs[2] + cw_) / 2., 5.4, '结论、政策建议与研究展望（第14章）',
        fs=7.8, c=C['green'], bold=True)
    # ---- 主线→各层（虚线短箭头）
    for yy in (65.8, 48.2, 30.5, 13.9):
        arr(ax, (14.2, yy), (17.4, yy), c=C['orange'], lw=1.1, ls=(0, (4, 2.5)), ms=10)
    # ---- 评估反馈回路（右侧正交折线）
    poly(ax, [(R0 + 0.4, 13.9), (98.3, 13.9), (98.3, 48.2), (R0 + 0.4, 48.2)],
         c=C['red'], lw=1.1, ls=(0, (5, 3)), ms=11)
    txt(ax, 96.6, 31.0, '实践检验与政策评估反馈：口径修订与参数再标定',
        fs=6.2, c=C['red'], rot=90)
    done(fig, 'fig1_1')


# ==================================================== 图1.2 全书结构与章节安排
def fig1_2():
    fig, ax = canvas(100, 96, 11.0)
    ch = {1: '导论', 2: '理论基础与文献述评',
          3: '词元的技术属性与经济属性',
          4: '词元经济的发展格局与典型事实',
          5: '标准词元：效值折算体系的构建',
          6: '词元的价值创造、实现与增值',
          7: '词元定价机制：三层结构与价格指数',
          8: '词元市场的结构、竞争与均衡',
          9: '算力—词元转化效率与配置优化',
          10: '城市词元运营中心的组织模式与机制设计',
          11: '绿色词元：能耗、碳足迹与可信溯源',
          12: '词元经济的增长贡献测度',
          13: '区域实践与多案例研究',
          14: '结论、政策建议与研究展望'}
    parts = [('第一篇　总起', '第1—2章', [1, 2], 'blue'),
             ('第二篇　属性与事实', '第3—4章', [3, 4], 'teal'),
             ('第三篇　计量与价值', '第5—6章', [5, 6], 'gold'),
             ('第四篇　定价与市场', '第7—8章', [7, 8], 'purple'),
             ('第五篇　配置、增长与实践', '第9—14章', [9, 10, 11, 12, 13, 14], 'green')]
    top, hh, pitch = 94.0, 5.0, 6.6
    cy = {k: top - (k - 1) * pitch for k in ch}           # 各章方框上沿
    x_ch, w_ch = 60.0, 37.0
    x_pt, w_pt = 28.0, 24.0
    # 根节点
    bx(ax, 2.0, cy[14] - hh, 18.0, (cy[1] + hh) - (cy[14] - hh) - hh,
       '《标准词元与智能经济》\n\n词元的价值计量、\n定价机制与配置效率研究\n\n'
       '全书 14 章·五篇\n计量·定价·配置三线贯通',
       fc=C['ltorange'], ec=C['orange'], fs=8.6, lw=1.5, tc=C['orange'], tag='书名')
    ymid = (cy[1] + cy[14] - hh) / 2.
    pcs = []
    for name, rng, chs, col in parts:
        y1, y0 = cy[chs[0]], cy[chs[-1]] - hh
        bx(ax, x_pt, y0, w_pt, y1 - y0, name + '\n（' + rng + '）',
           fc=C['lt' + col], ec=C[col], fs=8.6, lw=1.3, tc=C[col], bold=True, tag=name)
        pcs.append((y0 + y1) / 2.)
        ys = [cy[k] - hh / 2. for k in chs]
        ax.plot([56.0, 56.0], [min(ys), max(ys)], color=C[col], lw=1.0, zorder=1)
        ax.plot([x_pt + w_pt + 0.4, 56.0], [(y0 + y1) / 2.] * 2, color=C[col], lw=1.0, zorder=1)
        for k in chs:
            yc = cy[k] - hh / 2.
            bx(ax, x_ch, cy[k] - hh, w_ch, hh, '第%d章　%s' % (k, ch[k]),
               fc=C['ltgray'], ec=C[col], fs=8.4, lw=1.0, pad=0.3, tag='第%d章' % k)
            arr(ax, (56.0, yc), (x_ch - 0.4, yc), c=C[col], lw=1.0, ms=10)
    ax.plot([24.0, 24.0], [min(pcs), max(pcs)], color=C['orange'], lw=1.1, zorder=1)
    ax.plot([20.4, 24.0], [ymid, ymid], color=C['orange'], lw=1.1, zorder=1)
    for yc in pcs:
        arr(ax, (24.0, yc), (x_pt - 0.4, yc), c=C['orange'], lw=1.1, ms=10)
    done(fig, 'fig1_2')


# ==================================================== 图2.2 理论基础与研究框架逻辑
def fig2_2():
    fig, ax = canvas(100, 63, 10.5)
    # 左列四支理论：自上而下与中部模块顺序对应，连线互不交叉
    ths = [('价值理论', '劳动价值论·效用价值论\n信息产品价值论', 'blue', 46.0),
           ('当量折算传统', '标准煤·标准箱\n二氧化碳当量', 'teal', 33.0),
           ('平台定价与增长核算', '双边平台与价格结构\n索洛残差·资本服务测度', 'gold', 20.0),
           ('通用目的技术理论', '迂回渗透·配套投资\n索洛生产率悖论', 'purple', 7.0)]
    for t, s, col, yy in ths:
        bx2(ax, 1.5, yy, 25.0, 11.0, t, s, fc=C['lt' + col], ec=C[col],
            fs=8.0, fs2=6.6, tag=t)
    frame(ax, 33.0, 8.0, 67.5, 61.0, ec=C['orange'], lw=1.2)
    txt(ax, 50.25, 58.6, '标准词元「三位一体」研究框架', fs=9.2, c=C['orange'], bold=True)
    mods = [('计量　第5—6章', '三维效值与公理化折算\n价值创造、实现与增值', 44.0),
            ('定价　第7—8章', '三层价格结构与价格指数\n需求弹性与市场均衡', 29.0),
            ('配置　第9—12章', '转化效率与统一调度\n绿色词元与增长核算', 14.0)]
    for t, s, yy in mods:
        bx2(ax, 35.0, yy, 30.5, 11.0, t, s, fc=C['ltorange'], ec=C['orange'],
            fs=8.2, fs2=6.6, lw=1.2, tag=t)
    arr(ax, (50.25, 43.6), (50.25, 40.4), c=C['orange'], lw=1.3)
    txt(ax, 60.5, 42.0, '统一尺度', fs=6.4, c=C['orange'])
    arr(ax, (50.25, 28.6), (50.25, 25.4), c=C['orange'], lw=1.3)
    txt(ax, 60.5, 27.0, '价格信号', fs=6.4, c=C['orange'])
    # 理论→框架（正交折线，路径互不相交）
    links = [(0, 51.5, 49.5, 30.0), (1, 38.5, 46.0, 31.5),
             (2, 25.5, 32.0, 30.0), (2, 23.0, 18.5, 32.5), (3, 12.5, 14.5, 31.0)]
    for i, y1, y2, xk in links:
        col = C[ths[i][2]]
        poly(ax, [(26.9, y1), (xk, y1), (xk, y2), (34.6, y2)], c=col, lw=1.1, ms=10)
    outs = [('核算变量与统计口径', '标准词元流量 $\\tilde{T}$ 进入生产函数\n增长贡献分解（第12章）', 44.0),
            ('词元价格指数', 'TPI 与 STPI 编制\n背离测度与监测（第7章）', 29.0),
            ('配置信号与调度优化', '转化效率 $\\theta$·任务—模型匹配\n效率改进上界（第9章）', 14.0)]
    for t, s, yy in outs:
        bx2(ax, 74.0, yy, 24.5, 11.0, t, s, fc=C['ltgreen'], ec=C['green'],
            fs=8.0, fs2=6.4, tag=t)
        arr(ax, (65.9, yy + 5.5), (73.6, yy + 5.5), c=C['green'], lw=1.2)
    poly(ax, [(86.0, 13.6), (86.0, 4.5), (50.25, 4.5), (50.25, 8.0)],
         c=C['red'], lw=1.0, ls=(0, (5, 3)), ms=10)
    txt(ax, 68.5, 2.9, '实证反馈：权重再标定与口径修订', fs=6.4, c=C['red'])
    done(fig, 'fig2_2')


# ==================================================== 图3.1 词元的技术属性与经济属性谱系
def fig3_1():
    fig, ax = canvas(100, 60, 11.0)
    tech = [('分词与编码', '分词器切分·词表映射\n同一文本的词元数因模型而异'),
            ('推理生成', '逐词元自回归前向计算\n算力消耗随参数规模上升'),
            ('多模态扩展', '文本·图像·语音·视频\n统一词元化后可比性更弱'),
            ('上下文与缓存', '长上下文·前缀缓存复用\n改变单位词元的实际成本')]
    tw, tg = 22.0, 3.6
    tx0 = (100 - 4 * tw - 3 * tg) / 2.
    for i, (t, s) in enumerate(tech):
        xx = tx0 + i * (tw + tg)
        bx2(ax, xx, 47.0, tw, 11.0, t, s, fc=C['ltblue'], ec=C['blue'],
            fs=8.2, fs2=6.3, tag=t)
        if i < 3:
            arr(ax, (xx + tw + 0.5, 52.5), (xx + tw + tg - 0.5, 52.5), c=C['blue'], lw=1.1, ms=10)
        arr(ax, (xx + tw / 2., 46.6), (xx + tw / 2., 44.8), c=C['blue'], lw=1.0, ms=9)
    bx(ax, tx0, 39.0, 100 - 2 * tx0, 5.4,
       '技术过程决定词元的算力消耗、信息含量、可复制性与可排他程度',
       fc=C['ltgray'], ec=C['gray'], fs=8.4, lw=1.1, tc=C['ink'], tag='传导带')
    attrs = [('价值尺度', '可计量·可定价\n可交易的最小单元'),
             ('稀缺性', '受算力、能源与\n时延约束'),
             ('部分排他性', '经接口与许可\n实现排他'),
             ('规模经济', '训练固定成本高\n推理边际成本低'),
             ('范围经济', '同一模型服务\n多任务多场景'),
             ('场景依赖性', '同量词元的价值\n随场景差异'),
             ('非竞争性', '可无损复制\n重复使用'),
             ('网络外部性', '用户与生态\n互促增强')]
    groups = [(0, 3, '计量职能', '充当价值尺度与统计口径\n（第5—6章）', 'gold'),
              (3, 6, '配置职能', '引导算力—模型—场景匹配\n（第7—9章）', 'teal'),
              (6, 8, '增长职能', '作为可观测的增长核算变量\n（第12章）', 'purple')]
    aw, ag, gg = 10.1, 1.3, 4.0
    xs, cur = [], 2.2
    for a, b, _t, _s, _c in groups:
        for j in range(a, b):
            xs.append(cur)
            cur += aw + (ag if j < b - 1 else 0)
        cur += gg
    for i, (t, s) in enumerate(attrs):
        col = [g[4] for g in groups if g[0] <= i < g[1]][0]
        bx2(ax, xs[i], 22.0, aw, 10.0, t, s, fc=C['lt' + col], ec=C[col],
            fs=7.2, fs2=5.8, pad=0.3, tag=t)
    for a, b, t, s, col in groups:
        gx0, gx1 = xs[a] - 1.3, xs[b - 1] + aw + 1.3
        frame(ax, gx0, 20.3, gx1, 34.5, ec=C[col], lw=0.9)
        gc = (gx0 + gx1) / 2.
        arr(ax, (gc, 38.6), (gc, 34.9), c=C[col], lw=1.1, ms=10)
        bx2(ax, gx0, 6.0, gx1 - gx0, 9.5, t, s, fc=C['lt' + col], ec=C[col],
            fs=8.6, fs2=6.8, lw=1.3, tag=t)
        arr(ax, (gc, 19.9), (gc, 15.9), c=C[col], lw=1.2)
    done(fig, 'fig3_1')


# ==================================================== 图5.1 标准词元效值折算体系框架
def fig5_1():
    fig, ax = canvas(100, 88, 10.0)
    bx(ax, 22.0, 79.5, 56.0, 8.0,
       '物理词元 $T$\n各档位分词器切分并计费的原始词元计数，不区分模型与任务——不可比、不可加',
       fc=C['ltgray'], ec=C['gray'], fs=8.6, lw=1.3, tag='物理词元')
    arr(ax, (50.0, 79.1), (50.0, 76.4), c=C['gray'], lw=1.3)
    # 三维效值
    frame(ax, 5.0, 60.0, 95.0, 76.0, ec=C['teal'], lw=1.1)
    txt(ax, 50.0, 74.0, '三维效值测度（均相对基准档「中型通用级」，基准档各维 ≡ 1）',
        fs=8.0, c=C['teal'], bold=True)
    dims = [('$P$　算力强度', '生成单枚词元所耗\n浮点运算量之比'),
            ('$R$　推理质量', '单枚词元承载的有效信息量\n与任务达成度之比'),
            ('$S$　场景效用', '所替代人类认知劳动的\n价值密度之比')]
    for i, (t, s) in enumerate(dims):
        xx = 8.0 + i * 28.5
        bx2(ax, xx, 61.5, 26.0, 9.0, t, s, fc=C['ltteal'], ec=C['teal'],
            fs=8.4, fs2=6.6, tag='维度%d' % (i + 1))
        ax.plot([xx + 13.0] * 2, [61.1, 57.5], color=C['teal'], lw=1.1, zorder=1)
    ax.plot([21.0, 78.0], [57.5, 57.5], color=C['teal'], lw=1.1, zorder=1)
    arr(ax, (50.0, 57.5), (50.0, 55.1), c=C['teal'], lw=1.2)
    # 四条公理
    frame(ax, 1.0, 29.5, 23.5, 56.5, ec=C['gold'], lw=1.0)
    txt(ax, 12.25, 54.4, '四条公理约束', fs=8.0, c=C['gold'], bold=True)
    ax_items = [('公理一　基准归一', '$\\eta(1,1,1)=1$'),
                ('公理二　严格单调', '对 $P$、$R$、$S$ 的偏导恒为正'),
                ('公理三　可加性', '同口径标准词元可直接加总'),
                ('公理四　链式一致', '$\\eta(P_1P_2,R_1R_2,S_1S_2)=\\eta_1\\eta_2$')]
    for i, (t, s) in enumerate(ax_items):
        bx2(ax, 2.2, 48.0 - i * 5.6, 20.1, 4.6, t, s, fc=C['ltgold'], ec=C['gold'],
            fs=6.6, fs2=5.4, pad=0.25, tag='公理%d' % (i + 1))
    arr(ax, (23.9, 45.5), (26.6, 45.5), c=C['gold'], lw=1.2)
    # 幂积折算函数
    bx(ax, 27.0, 37.5, 66.0, 17.0, '', fc=C['ltorange'], ec=C['orange'], lw=1.6, tag='折算函数')
    txt(ax, 60.0, 51.6, '幂积折算函数（命题5.1：连续、严格单调、基准归一与链式一致，'
                        '则折算函数必为幂积形式）', fs=7.6, c=C['ink'])
    txt(ax, 60.0, 46.6, '$\\eta = P^{\\,w_P}\; R^{\\,w_R}\; S^{\\,w_S}$', fs=13.5, c=C['orange'])
    txt(ax, 60.0, 42.0, '权重标定　$w_P$＝0.4383　　$w_R$＝0.2964　　$w_S$＝0.2653（三者和为 1）',
        fs=7.8, c=C['ink'])
    txt(ax, 60.0, 39.3, '基准任务集拟合优度 0.9996；CES 交叉验证替代参数 0.0794，统计上无法拒绝退化为幂积形式',
        fs=7.0, c=C['sub'])
    arr(ax, (50.0, 37.1), (50.0, 33.1), c=C['orange'], lw=1.3)
    # 标准词元
    bx(ax, 26.0, 21.5, 48.0, 11.0,
       '标准词元　$\\tilde{T} = \\eta\\, T$\n'
       '基准档「中型通用级」1 枚物理词元 ≡ 1 标准词元\n'
       '标准词元价格　$\\tilde{p} = p\\,/\\,\\eta$',
       fc=C['ltgreen'], ec=C['green'], fs=8.6, lw=1.7, tag='标准词元')
    bx(ax, 14.0, 15.5, 72.0, 4.5,
       '六档位效值系数 $\\eta$：轻量蒸馏级 0.38｜中型通用级 1.00｜开源旗舰级 1.96｜'
       '旗舰闭源级 2.94｜推理增强级 4.28｜多模态级 2.62',
       fc=C['ltgray'], ec=C['gray'], fs=6.4, lw=0.9, pad=0.3, tag='效值系数')
    # 三个输出接口
    outs = [('定价基准（第7章）', '三层价格结构与价格地板\n价格指数 TPI／STPI'),
            ('配置信号（第9章）', '转化效率 $\\theta$＝有效标准词元／算力\n任务—模型最优匹配'),
            ('核算变量（第12章）', '标准词元流量进入生产函数\n产出弹性 $\\alpha_T$ 的识别')]
    ax.plot([50.0, 50.0], [15.1, 13.5], color=C['blue'], lw=1.1, zorder=1)
    ax.plot([18.0, 82.0], [13.5, 13.5], color=C['blue'], lw=1.1, zorder=1)
    for i, (t, s) in enumerate(outs):
        xx = 4.0 + i * 32.0
        bx2(ax, xx, 2.5, 28.0, 9.5, t, s, fc=C['ltblue'], ec=C['blue'],
            fs=8.0, fs2=6.4, lw=1.2, tag='接口%d' % (i + 1))
        arr(ax, (xx + 14.0, 13.5), (xx + 14.0, 12.4), c=C['blue'], lw=1.1, ms=10)
    poly(ax, [(96.4, 7.2), (98.4, 7.2), (98.4, 68.0), (95.4, 68.0)],
         c=C['red'], lw=1.0, ls=(0, (5, 3)), ms=10)
    txt(ax, 96.9, 38.0, '接口反馈：基准任务集与权重再标定', fs=6.2, c=C['red'], rot=90)
    done(fig, 'fig5_1')


# ==================================================== 图6.1 价值创造的劳动凝结结构
def fig6_1():
    fig, ax = canvas(100, 62, 10.0)
    frame(ax, 1.5, 32.5, 28.0, 59.5, ec=C['orange'], lw=1.1)
    txt(ax, 14.75, 57.2, '活劳动投入', fs=8.6, c=C['orange'], bold=True)
    live = [('数据劳动', '语料采集·清洗·标注'),
            ('算法劳动', '架构设计·训练·对齐'),
            ('知识工程劳动', '提示工程·工作流编排·评测')]
    for i, (t, s) in enumerate(live):
        bx2(ax, 3.2, 48.4 - i * 7.4, 23.1, 6.2, t, s, fc=C['ltorange'], ec=C['orange'],
            fs=7.4, fs2=6.0, pad=0.3, tag=t)
    frame(ax, 1.5, 2.5, 28.0, 29.5, ec=C['blue'], lw=1.1)
    txt(ax, 14.75, 27.2, '物化劳动投入', fs=8.6, c=C['blue'], bold=True)
    dead = [('算力设施', '芯片·服务器·数据中心折旧'),
            ('模型资产', '预训练参数与工具链摊销'),
            ('能源投入', '电力消耗与冷却')]
    for i, (t, s) in enumerate(dead):
        bx2(ax, 3.2, 18.4 - i * 7.4, 23.1, 6.2, t, s, fc=C['ltblue'], ec=C['blue'],
            fs=7.4, fs2=6.0, pad=0.3, tag=t)
    frame(ax, 33.5, 8.0, 68.5, 55.0, ec=C['teal'], lw=1.2, fc='#F6FAFA', z=0)
    txt(ax, 51.0, 52.3, '词元生成过程', fs=9.0, c=C['teal'], bold=True)
    steps = [('预训练与对齐', '社会必要劳动凝结为模型资产', 38.5),
             ('推理生成', '物化劳动转移价值＋活劳动新创价值\n随每枚词元一并让渡', 25.0),
             ('效值形成', '单枚词元的 $P$、$R$、$S$ 由此确定', 11.5)]
    for t, s, yy in steps:
        bx2(ax, 36.0, yy, 30.0, 9.5, t, s, fc=C['ltteal'], ec=C['teal'],
            fs=8.0, fs2=6.3, tag=t)
    arr(ax, (51.0, 38.1), (51.0, 35.0), c=C['teal'], lw=1.2)
    arr(ax, (51.0, 24.6), (51.0, 21.4), c=C['teal'], lw=1.2)
    arr(ax, (28.4, 43.0), (33.1, 43.0), c=C['orange'], lw=1.3)
    arr(ax, (28.4, 26.0), (33.1, 26.0), c=C['blue'], lw=1.3)
    bx(ax, 74.0, 30.0, 24.5, 14.0,
       '标准词元当量\n$\\tilde{T} = \\eta\\, T$\n以基准档为 1 单位的\n可比、可加计量',
       fc=C['ltgreen'], ec=C['green'], fs=8.2, lw=1.5, tag='当量')
    bx(ax, 74.0, 10.0, 24.5, 16.0,
       '单位标准词元的价值构成\n\n物化劳动转移价值\n（算力折旧·模型摊销·电力）\n＋\n活劳动新创价值\n（数据·算法·知识工程）',
       fc=C['ltgold'], ec=C['gold'], fs=6.8, lw=1.2, tag='价值构成')
    poly(ax, [(66.4, 16.25), (70.5, 16.25), (70.5, 37.0), (73.6, 37.0)],
         c=C['teal'], lw=1.3, ms=11)
    arr(ax, (86.25, 29.6), (86.25, 26.4), c=C['green'], lw=1.2)
    done(fig, 'fig6_1')


# ==================================================== 图6.2 价值实现与增值循环
def fig6_2():
    fig, ax = canvas(100, 80, 10.0)
    nodes = [('生产', '预训练与模型构建\n算力与数据凝结为模型资产', 4.0, 44.0, 24.0, 14.0, 'blue'),
             ('推理', '按需生成词元\n物化劳动转移与新创价值让渡', 38.0, 44.0, 24.0, 14.0, 'teal'),
             ('应用', '词元嵌入业务流程\n在场景中转化为使用价值', 70.0, 44.0, 24.0, 14.0, 'gold'),
             ('反馈', '真实交互与评测数据回流\n沉淀为高质量语料', 70.0, 22.0, 24.0, 14.0, 'purple'),
             ('优化', '模型迭代与调度改进\n效值系数与转化效率提升', 4.0, 22.0, 24.0, 14.0, 'green')]
    for t, s, x, y, w, h, col in nodes:
        bx2(ax, x, y, w, h, t, s, fc=C['lt' + col], ec=C[col], fs=9.2, fs2=6.5,
            lw=1.4, tag=t)
    arr(ax, (28.5, 51.0), (37.5, 51.0), c=C['gray'], lw=1.4, ms=13)
    arr(ax, (62.5, 51.0), (69.5, 51.0), c=C['gray'], lw=1.4, ms=13)
    arr(ax, (82.0, 43.5), (82.0, 36.5), c=C['gray'], lw=1.4, ms=13)
    arr(ax, (69.5, 29.0), (28.5, 29.0), c=C['gray'], lw=1.4, ms=13)
    arr(ax, (16.0, 36.5), (16.0, 43.5), c=C['gray'], lw=1.4, ms=13)
    txt(ax, 33.0, 53.2, '模型能力\n转为词元', fs=6.4, c=C['gray'])
    txt(ax, 66.0, 53.2, '词元进入\n业务流程', fs=6.4, c=C['gray'])
    txt(ax, 84.0, 40.0, '使用效果\n可观测', fs=6.4, c=C['gray'], ha='left')
    txt(ax, 49.0, 31.2, '数据与评测回流', fs=6.4, c=C['gray'])
    txt(ax, 14.0, 40.0, '能力再生产', fs=6.4, c=C['gray'], ha='right')
    txt(ax, 50.0, 40.0,
        '每轮循环：效值系数 $\\eta$ 上升　转化效率 $\\theta$ 上升　单位标准词元成本下降',
        fs=7.2, c=C['red'])
    bx2(ax, 36.0, 64.0, 28.0, 12.0, '规模复用', '一次训练、多次推理\n单位词元边际成本趋零',
        fc=C['ltred'], ec=C['red'], fs=8.2, fs2=6.4, lw=1.2, tag='规模复用')
    bx2(ax, 68.0, 64.0, 28.0, 12.0, '网络协同', '用户与场景增多提升\n匹配效率与生态价值',
        fc=C['ltred'], ec=C['red'], fs=8.2, fs2=6.4, lw=1.2, tag='网络协同')
    bx2(ax, 36.0, 4.0, 28.0, 12.0, '持续学习', '反馈数据回流提升推理质量 $R$\n进而提升效值系数 $\\eta$',
        fc=C['ltred'], ec=C['red'], fs=8.2, fs2=6.4, lw=1.2, tag='持续学习')
    arr(ax, (50.0, 63.6), (50.0, 58.5), c=C['red'], lw=1.1, ls=(0, (4, 2.5)), ms=10)
    arr(ax, (82.0, 63.6), (82.0, 58.5), c=C['red'], lw=1.1, ls=(0, (4, 2.5)), ms=10)
    arr(ax, (50.0, 16.4), (50.0, 28.4), c=C['red'], lw=1.1, ls=(0, (4, 2.5)), ms=10)
    txt(ax, 4.0, 74.0, '增值来源（外挂于循环）', fs=7.6, c=C['red'], ha='left', bold=True)
    done(fig, 'fig6_2')


# ==================================================== 图7.1 词元价格的三层结构
def fig7_1():
    fig, ax = canvas(100, 62, 10.0)
    bands = [('成本底价层（价格地板）', '算力折旧＋电费＋运维\n零边际成本产品的刚性下限', 8.0, 'blue'),
             ('效值溢价层（质量梯度）', '效值系数 $\\eta$ 越高，单枚词元可索取的溢价越大\n质量梯度定价：档位越高，单位词元定价阶梯上移', 23.0, 'teal'),
             ('场景租金层（纵向差异）', '应用所创造价值中可被服务方占有的份额 $\\rho$\n价值密度越高、可替代性越弱，租金越厚', 38.0, 'gold')]
    rights = [('决定因素：算力价格·电价与 PUE·运维与折旧年限',
               '随硬件迭代与能效改善缓慢下移，构成价格竞争的底线'),
              ('决定因素：三维效值 $P$、$R$、$S$ 的合成',
               '六档位效值系数 $\\eta$ 跨度 0.38—4.28，决定质量梯度'),
              ('决定因素：场景价值密度·可占有份额·议价能力',
               '八类场景价值密度跨度 1.9—11.3，决定纵向价差')]
    for i, ((t, s, yy, col), (rt, rs)) in enumerate(zip(bands, rights)):
        bx2(ax, 17.0, yy, 50.0, 11.5, t, s, fc=C['lt' + col], ec=C[col],
            fs=9.0, fs2=6.8, lw=1.4, pad=0.15, tag=t)
        bx2(ax, 70.5, yy, 28.0, 11.5, rt, rs, fc='#FFFFFF', ec=C[col],
            fs=6.6, fs2=6.0, lw=1.0, pad=0.25, tag='因素%d' % (i + 1))
        arr(ax, (67.4, yy + 5.75), (70.2, yy + 5.75), c=C[col], lw=1.0, ms=9)
        if i < 2:
            arr(ax, (42.0, yy + 11.7), (42.0, yy + 14.3), c=C['gray'], lw=1.3, ms=12)
            txt(ax, 46.5, yy + 13.0, '叠加', fs=6.4, c=C['gray'])
    ax.plot([13.0, 13.0], [8.0, 49.5], color=C['red'], lw=1.4, zorder=1)
    ax.plot([13.0, 15.5], [8.0, 8.0], color=C['red'], lw=1.4, zorder=1)
    arr(ax, (13.0, 44.0), (13.0, 50.5), c=C['red'], lw=1.4, ms=13)
    txt(ax, 9.6, 28.5, '市场价 $p$：自下而上三层累积', fs=8.4, c=C['red'], rot=90, bold=True)
    txt(ax, 5.0, 28.5, '标准词元价格 $\\tilde{p}=p\\,/\\,\\eta$', fs=7.4, c=C['red'], rot=90)
    bx(ax, 17.0, 53.5, 81.5, 4.6,
       '结构性含义：成本底价层持续下行使通用词元价格走低，效值溢价层与场景租金层扩张使高效值词元溢价扩大',
       fc=C['ltgray'], ec=C['gray'], fs=7.4, lw=1.0, pad=0.25, tag='含义')
    bx(ax, 17.0, 1.0, 81.5, 4.6,
       '中型通用级示例（元／百万词元）：成本底价 0.52 ＋ 效值溢价 0.34 ＋ 场景租金 0.44 ＝ 市场价 1.30',
       fc=C['ltgreen'], ec=C['green'], fs=7.4, lw=1.0, pad=0.25, tag='示例')
    done(fig, 'fig7_1')


ALL = [fig1_1, fig1_2, fig2_2, fig3_1, fig5_1, fig6_1, fig6_2, fig7_1]

if __name__ == '__main__':
    for f in ALL:
        f()
    if _WARN:
        print('--- 版式告警 %d 条 ---' % len(_WARN))
        for w in _WARN:
            print('  ', w)
    else:
        print('版式自检通过：无文字溢出告警')
    print('diagrams_a done:', len(ALL))
