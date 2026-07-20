# -*- coding: utf-8 -*-
"""机制图 / 理论分析图（不依赖外部数据的11幅）。输出至 ../figs/fig_X_Y.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figstyle import *

FIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figs')
os.makedirs(FIG, exist_ok=True)

# ---------- 图1.2 研究技术路线图 ----------
def fig_1_2():
    fig, ax = diagram_ax(8.8, 6.4)
    box(ax, 50, 95, 74, 6.5, '现实问题：供强需弱、价格低位运行与“内卷式”竞争蔓延', fc=BOX_FC2, ec=BOX_EC2, bold=True, fs=10.5)
    box(ax, 50, 84.5, 74, 6.5, '政策命题：纵深推进全国统一大市场建设，深入整治“内卷式”竞争', fc=BOX_FC4, ec=BOX_EC4, bold=True, fs=10.5)
    arrow(ax, 50, 91.5, 50, 88)
    box(ax, 50, 73, 60, 6.5, '理论构建：“内卷式竞争陷阱”与“统一市场红利”\n“市场分割—内卷竞争—统一红利”三环框架（第三章）', fs=9.5)
    arrow(ax, 50, 81, 50, 76.6)
    box(ax, 50, 61.5, 60, 6.5, '数理模型：补贴竞争→过度进入→一体化选择与创新效应\n可检验命题H1—H5（第四章）', fs=9.5)
    arrow(ax, 50, 69.6, 50, 65.2)
    box(ax, 22, 48, 34, 7.5, '典型化事实\n宏观与行业证据（第五章）', fc=BOX_FC3, ec=BOX_EC3, fs=9.5)
    box(ax, 61, 48, 30, 7.5, '指数测度\n分割指数与内卷指数\n（第六、七章）', fc=BOX_FC3, ec=BOX_EC3, fs=9.5)
    box(ax, 88.5, 48, 19, 7.5, '案例研究\n（第十章）', fc=BOX_FC3, ec=BOX_EC3, fs=9.5)
    arrow(ax, 40, 58, 24, 52.2); arrow(ax, 52, 58, 60, 52.2); arrow(ax, 66, 58, 86, 52.2)
    box(ax, 35, 35, 44, 7.5, '机制检验：分割如何催生“内卷”\n面板回归+机制+异质性（第八章）', fs=9.5)
    box(ax, 76.5, 35, 33, 7.5, '效应评估：统一的“红利”\n公平竞争审查强度DID（第九章）', fs=9.5)
    arrow(ax, 26, 44, 32, 39.2); arrow(ax, 62, 44, 70, 39.2); arrow(ax, 88, 44, 82, 39.2)
    box(ax, 50, 22, 68, 7, '国际镜鉴：美国州际市场、欧盟单一市场、日本“过当竞争”治理（第十章）', fc=BOX_GREY, ec=BOX_GEC, fs=9.5)
    arrow(ax, 40, 31.2, 45, 26); arrow(ax, 72, 31.2, 62, 26)
    box(ax, 50, 9.5, 76, 8, '政策路径：“十五五”纵深推进全国统一大市场建设与\n“内卷式”竞争综合整治的制度设计（第十一章）', fc=BOX_FC4, ec=BOX_EC4, bold=True, fs=10)
    arrow(ax, 50, 18.4, 50, 14.4)
    save(fig, f'{FIG}/fig_1_2.png')

# ---------- 图2.1 政策演进时间轴 ----------
def fig_2_1():
    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    ax.set_xlim(2012.0, 2027.6); ax.set_ylim(-5.2, 5.6)
    ax.axis('off'); ax.grid(False)
    ax.axhline(0, color='#555555', lw=1.6, zorder=1)
    # (锚点年份, 文本, 侧别, 文本层级1/2/3, 文本横向偏移)
    events = [
        (2013.0, '党的十八届三中全会：使市场\n在资源配置中起决定性作用', 1, 1, 0.6),
        (2015.0, '《关于清理规范税收\n等优惠政策的通知》', -1, 1, 0),
        (2016.5, '公平竞争审查制度\n建立（国发34号）', 1, 1, 0),
        (2018.9, '市场准入负面清单\n全面实施（151项）', -1, 1, 0),
        (2020.3, '《要素市场化配置\n体制机制的意见》', 1, 1, 0),
        (2021.1, '《建设高标准市场\n体系行动方案》', -1, 1, 0),
        (2022.3, '《加快建设全国统一\n大市场的意见》', 1, 2, 0),
        (2023.3, '市场准入负面清单\n压减至117项', -1, 1, 0),
        (2024.6, '《公平竞争审查条例》施行；\n二十届三中全会再部署', 1, 1, -0.55),
        (2025.05, '《全国统一大市场\n建设指引（试行）》', -1, 2, -0.35),
        (2025.5, '中央财经委六次会议：\n“五统一、一开放”', 1, 2, 0.35),
        (2025.95, '中央经济工作会议：制定条例、\n深入整治“内卷式”竞争', -1, 1, 1.05),
        (2026.2, '“十五五”规划纲要\n第十七章专章部署', 1, 1, 0.95),
    ]
    lev = {1: 1.35, 2: 3.1}
    for x, txt, side, level, dx in events:
        ytxt = lev[level] * side
        color = DARK if side > 0 else C2
        ax.plot([x, x], [0, ytxt*0.82], color=color, lw=1.0, zorder=2)
        if abs(dx) > 0.01:
            ax.plot([x, x+dx], [ytxt*0.82, ytxt*0.9], color=color, lw=0.8, zorder=2, ls=':')
        ax.plot(x, 0, 'o', ms=5.5, color=color, mfc='white', mew=1.4, zorder=3)
        ax.text(x+dx, ytxt*0.95 + 0.28*side, txt, ha='center',
                va='bottom' if side > 0 else 'top', fontsize=8.0, linespacing=1.4, color='#222222')
    for yr in range(2013, 2028, 2):
        ax.text(yr, -0.52, str(yr), ha='center', fontsize=8, color='#888888', va='top')
        ax.plot(yr, 0, '|', ms=7, color='#555555')
    save(fig, f'{FIG}/fig_2_1.png')

# ---------- 图3.1 三环传导框架 ----------
def fig_3_1():
    fig, ax = diagram_ax(9.0, 6.2)
    # 第一环：市场分割
    box(ax, 16, 88, 26, 7, '第一环：市场分割', fc=BOX_FC2, ec=BOX_EC2, bold=True, fs=11)
    box(ax, 16, 74, 27, 16.5, '显性壁垒：地方保护、\n准入差异、执法不一\n隐性壁垒：标准不一、\n信用分割、数据孤岛\n激励根源：晋升锦标赛\n＋土地财政＋属地税收', fs=8.8)
    # 第二环：内卷竞争
    box(ax, 50, 88, 28, 7, '第二环：“内卷式”竞争', fc=BOX_FC2, ec=BOX_EC2, bold=True, fs=11)
    box(ax, 50, 74, 28, 16.5, '同质化过度进入\n产能持续过剩\n价格向成本线以下收敛\n利润与创新回报侵蚀\n落后产能退出失灵', fs=9.2)
    # 第三环：统一红利
    box(ax, 84, 88, 26, 7, '第三环：统一市场红利', fc=BOX_FC3, ec=BOX_EC3, bold=True, fs=11)
    box(ax, 84, 74, 27, 16.5, '规模经济效应\n选择效应（优胜劣汰）\n创新激励效应\n预期与秩序效应', fs=9.2)
    arrow(ax, 30, 88, 35, 88, lw=1.8)
    label(ax, 32.6, 92.5, '催生', fs=9.5)
    arrow(ax, 65, 88, 70, 88, lw=1.8, color=BOX_EC3)
    label(ax, 67.4, 92.5, '破解', fs=9.5, color=BOX_EC3)
    # 中部机制带
    box(ax, 52, 56, 82, 8, '传导机制：市场规模碎片化 → 最小有效规模不可达 → 补贴维持的低效进入\n→ 需求收缩放大价格内卷 → 出清受阻形成“陷阱”',
        fc=BOX_GREY, ec=BOX_GEC, fs=9.2)
    arrow(ax, 18, 65, 32, 60.5, connectionstyle='arc3,rad=-0.12')
    arrow(ax, 50, 65.4, 50, 60.8)
    # 陷阱回路
    box(ax, 28, 41, 44, 8, '“内卷式竞争陷阱”自我强化回路：\n利润↓→创新↓→同质化↑→价格战↑→利润↓', fc=BOX_FC2, ec=BOX_EC2, fs=9.2)
    arrow(ax, 40, 51.8, 34, 45.6)
    arrow(ax, 5.5, 43, 5.5, 68, connectionstyle='arc3,rad=-0.2', ls='--', color=BOX_EC2)
    label(ax, 5.5, 34.5, '反哺地方保护动机', fs=8.5, color=BOX_EC2)
    # 统一大市场治理
    box(ax, 76, 41, 40, 8, '统一大市场建设：基础制度统一＋公平竞争刚性约束\n＋设施联通＋要素市场化＋监管执法统一', fc=BOX_FC4, ec=BOX_EC4, fs=9.0)
    arrow(ax, 68, 45.6, 62, 51.4, color=BOX_EC4)
    label(ax, 61.5, 47.5, '拆解', fs=9, color=BOX_EC4)
    arrow(ax, 90, 45.6, 90, 64.8, color=BOX_EC3, lw=1.8)
    label(ax, 95.5, 55, '释放\n红利', fs=9, color=BOX_EC3)
    # 底部结果
    box(ax, 50, 26, 88, 7, '竞争范式跃迁：从“价格内卷、存量互耗”转向“质量竞争、创新竞争、增量共创”', fc=BOX_FC3, ec=BOX_EC3, bold=True, fs=10)
    arrow(ax, 50, 37, 50, 30)
    box(ax, 50, 12.5, 88, 7.5, '宏观绩效：物价合理回升、企业利润修复、全要素生产率提升、\n国内大循环内生动力与可靠性增强', fc=BOX_FC, ec=BOX_EC, fs=9.5)
    arrow(ax, 50, 22.5, 50, 16.8)
    save(fig, f'{FIG}/fig_3_1.png')

# ---------- 图3.2 四重扭曲 ----------
def fig_3_2():
    fig, ax = diagram_ax(8.8, 5.6)
    box(ax, 50, 91, 56, 7, '“内卷式竞争陷阱”的形成机理：四重扭曲', fc=BOX_FC2, ec=BOX_EC2, bold=True, fs=11.5)
    specs = [
        (15, '扭曲一\n地方激励扭曲', 'GDP与税收锦标赛\n招商引资补贴竞赛\n重复建设与产业同构', '过度进入'),
        (38.3, '扭曲二\n要素价格扭曲', '低价供地、财政贴息\n电价优惠、隐性担保\n成本外部化', '成本失真'),
        (61.7, '扭曲三\n退出机制失灵', '破产制度不健全\n地方保护“僵尸企业”\n稳就业稳税源考量', '出清受阻'),
        (85, '扭曲四\n需求约束收紧', '居民消费率偏低\n外需波动加大\n供强需弱失衡', '内卷放大'),
    ]
    for x, t1, t2, t3 in specs:
        box(ax, x, 74, 26, 8.5, t1, fc=BOX_FC, ec=BOX_EC, bold=True, fs=9.8)
        box(ax, x, 57, 26, 15, t2, fs=8.8)
        arrow(ax, x, 69.5, x, 65)
        box(ax, x, 42.5, 20, 6, t3, fc=BOX_GREY, ec=BOX_GEC, fs=9.2)
        arrow(ax, x, 49.3, x, 46)
        arrow(ax, 50, 87.2, x, 78.6)
        arrow(ax, x, 39.3, 50 + (x-50)*0.25, 30.8)
    box(ax, 50, 25.5, 74, 8, '合成结果：同质化产能过剩 ＋ 价格向成本以下收敛 ＋ 创新回报侵蚀',
        fc=BOX_FC2, ec=BOX_EC2, bold=True, fs=10.2)
    box(ax, 50, 10.5, 62, 7.5, '“内卷式竞争陷阱”：自我强化的低水平竞争均衡', fc='#f9e3dd', ec=NEG, bold=True, fs=10.5)
    arrow(ax, 50, 21.2, 50, 14.8)
    save(fig, f'{FIG}/fig_3_2.png')

# ---------- 图3.3 统一红利四大效应 ----------
def fig_3_3():
    fig, ax = diagram_ax(8.8, 5.4)
    box(ax, 15, 50, 22, 24, '全国统一\n大市场建设\n\n（分割成本τ\n系统性下降）', fc=BOX_FC4, ec=BOX_EC4, bold=True, fs=10.5)
    specs = [
        (78, '规模经济效应', '有效市场规模扩大→分摊固定成本→\n单位成本下降→最小有效规模可达', BOX_FC3, BOX_EC3),
        (59, '选择效应', '生存生产率门槛上移→低效产能出清→\n资源向高效率企业再配置', BOX_FC3, BOX_EC3),
        (40, '创新激励效应', '创新回报随市场规模放大→研发强度上升→\n竞争从价格维度转向质量与技术维度', BOX_FC3, BOX_EC3),
        (21, '预期与秩序效应', '规则统一稳定预期→抑制策略性压价与\n囚徒困境式扩产→竞争秩序修复', BOX_FC3, BOX_EC3),
    ]
    for y, t1, t2, fc, ec in specs:
        box(ax, 46, y, 24, 8, t1, fc=fc, ec=ec, bold=True, fs=10)
        box(ax, 79.5, y, 37, 9.5, t2, fs=8.8)
        arrow(ax, 26.5, 50 + (y-50)*0.35, 33.5, y, connectionstyle='arc3,rad=%.2f' % (0.12 if y<50 else -0.12))
        arrow(ax, 58.2, y, 60.5, y)
    box(ax, 55, 6.5, 78, 6.5, '“统一市场红利”＝规模效应＋选择效应＋创新效应＋预期效应−转型调整成本',
        fc=BOX_FC, ec=BOX_EC, bold=True, fs=10)
    save(fig, f'{FIG}/fig_3_3.png')

# ---------- 图4.1 补贴竞争反应函数 ----------
def fig_4_1():
    fig, ax = new_fig(6.4, 4.6)
    s = np.linspace(0, 10, 200)
    # 反应函数 s_i = a + b s_j (b>0 战略互补)
    a, b = 2.8, 0.45
    r1 = a + b*s
    r2 = (s - a) / b
    ax.plot(s, r1, color=C1, lw=2, label='地区1反应函数 $R_1(s_2)$')
    ax.plot(s, r2, color=C2, lw=2, ls='--', label='地区2反应函数 $R_2(s_1)$')
    se = a / (1 - b)
    ax.plot([se], [se], 'o', ms=8, color=DARK, zorder=5)
    ax.annotate('纳什均衡 $E$\n$(s^*,s^*)$', (se, se), xytext=(se+0.7, se-1.6), fontsize=9.5,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax.plot([0], [0], 's', ms=8, color=C3, zorder=5)
    ax.annotate('合作最优 $O$\n$(0,0)$', (0, 0), xytext=(0.55, 1.15), fontsize=9.5,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax.plot([0, se], [0, se], ls=':', color=GRAY, lw=1.2)
    ax.set_xlim(-0.3, 10); ax.set_ylim(-0.3, 10)
    ax.set_xlabel('地区1补贴 $s_1$'); ax.set_ylabel('地区2补贴 $s_2$')
    ax.legend(loc='upper left')
    save(fig, f'{FIG}/fig_4_1.png')

# ---------- 图4.2 进入均衡与平均成本 ----------
def fig_4_2():
    fig, ax = new_fig(6.6, 4.6)
    n = np.linspace(2, 30, 300)
    S_unified, S_seg = 100.0, 100.0/6   # 统一市场 vs 六分割子市场
    F = 1.6
    ac_u = 1 + F*n/S_unified            # 单位平均成本（规模摊薄的倒数形式，示意）
    ac_s = 1 + F*n/(S_seg*6)*2.2        # 分割下重复固定成本，成本曲线上移
    ax.plot(n, ac_u, color=C1, lw=2, label='统一市场：平均成本 $AC^U(n)$')
    ax.plot(n, ac_s, color=C2, lw=2, ls='--', label='分割市场：平均成本 $AC^S(n)$')
    p_line = 1.42
    ax.axhline(p_line, color=GRAY, lw=1.2, ls=':')
    ax.text(30.2, p_line, '价格 $p$', va='center', fontsize=9.5, color='#555555')
    nU = (p_line-1)*S_unified/F
    nS = (p_line-1)*S_unified/(F*2.2)
    ax.plot([nU],[p_line],'o',ms=7,color=C1,zorder=5)
    ax.plot([nS],[p_line],'s',ms=7,color=C2,zorder=5)
    ax.annotate('统一市场零利润点\n$n^U$（企业更少、规模更大）', (nU, p_line), xytext=(nU-9.5, p_line+0.24), fontsize=9,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax.annotate('分割市场零利润点\n$n^S$（企业更多、规模更小）', (nS, p_line), xytext=(nS+1.2, p_line+0.3), fontsize=9,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax.axvspan(nS, nU, color='#f9e3dd', alpha=0.5, zorder=0)
    ax.text((nS+nU)/2, 1.06, '过度进入区间', ha='center', fontsize=9, color=NEG)
    ax.set_xlim(2, 30); ax.set_ylim(1.0, 1.95)
    ax.set_xlabel('企业数量 $n$'); ax.set_ylabel('价格与平均成本')
    ax.legend(loc='upper left')
    save(fig, f'{FIG}/fig_4_2.png')

# ---------- 图4.3 生产率门槛与选择效应 ----------
def fig_4_3():
    fig, ax = new_fig(6.6, 4.4)
    phi = np.linspace(0.5, 5, 400)
    k = 3.2
    dens = k * phi**(-k-1) / (0.5**(-k))
    dens = dens / dens.max()
    ax.plot(phi, dens, color=GRAY, lw=1.6, label='企业生产率分布 $g(\\varphi)$')
    ph1, ph2 = 1.15, 1.75
    ax.axvline(ph1, color=C2, lw=2, ls='--')
    ax.axvline(ph2, color=C1, lw=2)
    ax.fill_between(phi, 0, dens, where=(phi>=ph1)&(phi<=ph2), color='#fdf1e6', zorder=0)
    ax.text(ph1, 1.03, '分割市场门槛 $\\varphi^*_S$', color=C2, fontsize=9.5, ha='center')
    ax.text(ph2+0.02, 0.92, '统一市场门槛 $\\varphi^*_U$', color=C1, fontsize=9.5, ha='left')
    ax.annotate('低效企业退出区间\n（选择效应）', ((ph1+ph2)/2, 0.30), xytext=(2.6, 0.55), fontsize=9.5,
                arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
    ax.set_xlabel('生产率 $\\varphi$'); ax.set_ylabel('密度（标准化）')
    ax.set_xlim(0.5, 5); ax.set_ylim(0, 1.1)
    ax.legend(loc='upper right')
    save(fig, f'{FIG}/fig_4_3.png')

# ---------- 图4.4 统一红利福利分解 ----------
def fig_4_4():
    fig, ax = new_fig(6.8, 4.2)
    labels = ['规模经济\n效应', '选择效应\n（再配置）', '创新激励\n效应', '预期秩序\n效应', '转型调整\n成本', '统一市场\n红利（净）']
    vals = [1.0, 1.3, 0.9, 0.5, -0.7, 3.0]
    starts = [0]
    for v in vals[:-1]:
        starts.append(starts[-1] + v)
    starts[-1] = 0
    colors = [C3, C3, C3, C3, NEG, DARK]
    for i, (lab, v) in enumerate(zip(labels, vals)):
        bottom = starts[i] if i < len(vals)-1 else 0
        ax.bar(i, v, bottom=bottom, color=colors[i], width=0.62,
               edgecolor='white', linewidth=1.5, alpha=0.92 if i<5 else 1.0)
        ytext = bottom + v + 0.09 if v > 0 else bottom + v - 0.16
        ax.text(i, ytext, f'{v:+.1f}', ha='center', fontsize=9.5, color='#333333')
    for i in range(len(vals)-2):
        ax.plot([i+0.31, i+1-0.31], [starts[i]+vals[i]]*2, color='#aaaaaa', lw=0.9, ls=':')
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel('福利变化（标准化单位）')
    zero_line(ax)
    ax.set_ylim(-1.2, 4.2)
    save(fig, f'{FIG}/fig_4_4.png')

# ---------- 图6.1 实证设计框架 ----------
def fig_6_1():
    fig, ax = diagram_ax(8.8, 5.2)
    box(ax, 50, 93, 60, 6.5, '实证总体设计：三步递进、证据三角互证', fc=BOX_FC, ec=BOX_EC, bold=True, fs=11)
    box(ax, 18, 76, 30, 13, '第一步：测度\n市场分割指数（相对价格法）\n“内卷式竞争”强度指数（熵权法）\n统一大市场发展指数（四维）', fs=8.8)
    box(ax, 50, 76, 28, 13, '第二步：机制检验\n分割→内卷（H1—H3）\n面板FE＋中介机制＋IV\n异质性：行业/区域/时期', fs=8.8)
    box(ax, 82, 76, 30, 13, '第三步：效应评估\n统一→红利（H4—H5）\n公平竞争审查强度DID\n事件研究＋安慰剂', fs=8.8)
    arrow(ax, 33.5, 76, 35.5, 76); arrow(ax, 64.5, 76, 66.5, 76)
    box(ax, 18, 55, 30, 9, '数据：31省份面板\n2012—2024年\n8大类商品价格分省数据', fc=BOX_GREY, ec=BOX_GEC, fs=8.8)
    box(ax, 50, 55, 28, 9, '数据：省级工业指标\n上市公司补贴数据\n产业结构相似系数', fc=BOX_GREY, ec=BOX_GEC, fs=8.8)
    box(ax, 82, 55, 30, 9, '数据：公平竞争审查\n清理文件强度\nTFP与创新指标', fc=BOX_GREY, ec=BOX_GEC, fs=8.8)
    for x in (18, 50, 82):
        arrow(ax, x, 68.8, x, 60.3)
    box(ax, 50, 37, 74, 8, '稳健性体系：替换指标、剔除直辖市、滞后解释变量、\n工具变量（地形起伏度、历史驿道密度）、安慰剂检验', fs=9.2)
    for x in (18, 50, 82):
        arrow(ax, x, 50, 50 + (x-50)*0.35, 41.4)
    box(ax, 50, 20, 66, 8, '结论整合：命题H1—H5的证据链闭合\n→ 支撑第十一章政策路径设计', fc=BOX_FC4, ec=BOX_EC4, bold=True, fs=10)
    arrow(ax, 50, 32.8, 50, 24.4)
    save(fig, f'{FIG}/fig_6_1.png')

# ---------- 图11.1 政策路径框架 ----------
def fig_11_1():
    fig, ax = diagram_ax(9.0, 6.0)
    box(ax, 50, 94, 82, 6.5, '“十五五”时期纵深推进全国统一大市场建设的政策路径：一个目标、两个支柱、五大工程、一项重构',
        fc=BOX_FC4, ec=BOX_EC4, bold=True, fs=9.8)
    box(ax, 50, 84, 56, 6, '目标：基本建成高效规范、公平竞争、充分开放的全国统一大市场', fc=BOX_FC, ec=BOX_EC, fs=9.5, bold=True)
    arrow(ax, 50, 90.6, 50, 87.2)
    box(ax, 27, 73.5, 40, 6.5, '支柱一：统一大市场制度建设（治本）', fc=BOX_FC3, ec=BOX_EC3, bold=True, fs=9.8)
    box(ax, 76, 73.5, 40, 6.5, '支柱二：“内卷式”竞争综合整治（治标）', fc=BOX_FC2, ec=BOX_EC2, bold=True, fs=9.8)
    arrow(ax, 38, 81, 30, 77); arrow(ax, 62, 81, 72, 77)
    left = [
        '工程1　基础制度统一：产权保护、市场准入\n“全国一张清单”、信用体系、简易退出与破产',
        '工程2　公平竞争刚性化：审查全覆盖、\n招商引资“鼓励和禁止事项清单”、通报问责',
        '工程3　设施与要素贯通：物流降本、\n数据市场、要素市场化配置改革扩围',
    ]
    for i, t in enumerate(left):
        box(ax, 27, 62 - i*11.5, 42, 9, t, fs=8.6)
        arrow(ax, 27, 70.2 - i*11.5 if i==0 else 66.8 - (i-1)*11.5, 27, 66.6 - i*11.5, lw=1.1)
    right = [
        '工程4　治卷工具箱：产能调控、标准引领、\n价格执法、质量监管、反垄断反不正当竞争',
        '工程5　需求侧协同：城乡居民增收计划、\n服务消费扩容、投资于人',
    ]
    for i, t in enumerate(right):
        box(ax, 76, 62 - i*11.5, 42, 9, t, fs=8.6)
        arrow(ax, 76, 70.2 if i==0 else 66.8, 76, 66.6 - i*11.5, lw=1.1)
    box(ax, 76, 39, 42, 9, '一项重构　地方政府激励重构：消费地税收分享、\n经营主体活动发生地统计、差异化考核', fc=BOX_FC, ec=BOX_EC, fs=8.6)
    box(ax, 50, 24, 80, 7.5, '实施保障：条例落地＋央地协同＋节奏把握（防止“运动式反内卷”与行政化干预复归）',
        fc=BOX_GREY, ec=BOX_GEC, fs=9.2)
    arrow(ax, 27, 45.8, 40, 28.2); arrow(ax, 76, 34.4, 62, 28.2)
    box(ax, 50, 11, 72, 7, '预期成效：价格秩序修复→企业利润与创新回报回升→\n全要素生产率提升→国内大循环畅通', fc=BOX_FC3, ec=BOX_EC3, bold=True, fs=9.5)
    arrow(ax, 50, 20.2, 50, 14.6)
    save(fig, f'{FIG}/fig_11_1.png')

if __name__ == '__main__':
    for fn in [fig_1_2, fig_2_1, fig_3_1, fig_3_2, fig_3_3, fig_4_1, fig_4_2, fig_4_3, fig_4_4, fig_6_1, fig_11_1]:
        fn(); print('done', fn.__name__)
