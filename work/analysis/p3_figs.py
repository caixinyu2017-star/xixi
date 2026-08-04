# -*- coding: utf-8 -*-
"""论文3 概念图：理论映射框架图 / 蝴蝶结风险机制图 / 分类分级矩阵示意图 / 全过程闭环路径图 / 数字化赋能架构图"""
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from diagram import *      # noqa
from style import C, save
import matplotlib.patches as mp

OUT = "/home/user/xixi/work/figures/"
NAVY, GRAY, ORANGE, BRICK = C["navy"], C["gray"], C["clay"], C["brick"]
F1, F2, F3 = "#EAF0F7", "#FBF1E7", "#F2F4F7"

# ---------------- c1 理论映射框架 ----------------
fig, ax = canvas(8.4, 4.4)
left = ["目标精准化\n分类识别管理对象", "过程标准化\n事前事中事后全覆盖",
        "责任明确化\n谁主管谁负责、谁作业谁负责", "评价科学化\n数据驱动持续改进"]
right = ["分类分级管控机制\nLEC 风险 × 能力评分二维定级", "全过程闭环监管\n准入—合同—作业票—验收—评价",
         "合同与经济杠杆\n安全费用、履约保证金、违章计分", "绩效评价与激励\n红黑名单与优质优价挂钩"]
ax.text(23, 92, "精细化管理要义", ha="center", fontsize=9.5, fontweight="bold", color=NAVY)
ax.text(76, 92, "相关方安全监管机制", ha="center", fontsize=9.5, fontweight="bold", color=NAVY)
ax.plot([50, 50], [4, 88], color=GRAY, lw=0.9, ls=(0, (4, 3)))
for i, (l, r) in enumerate(zip(left, right)):
    y = 68 - i * 19
    a = box(ax, 2, y, 42, 15, l, fc=F1, fs=8)
    b = box(ax, 56, y, 42, 15, r, fc=F2, fs=8)
    arrow(ax, a, b, color=NAVY, lw=1.2)
save(fig, OUT + "p3_c1_mapping.png")

# ---------------- c2 蝴蝶结风险机制图 ----------------
fig, ax = canvas(9.2, 4.6)
hz = box(ax, 41, 42, 18, 18, "相关方作业\n失控事件", fc=NAVY, tc="white", fs=9, bold=True)
causes = ["人员资质不符\n（特种作业无证）", "动火/受限空间\n作业未办票", "临时用电与\n高处作业违章"]
cons = ["人员伤害", "火灾爆炸", "业务中断与\n声誉损失"]
cn, sn = [], []
for i, t in enumerate(causes):
    cn.append(box(ax, 2, 74 - i * 30, 20, 17, t, fc=F3, fs=7.8))
for i, t in enumerate(cons):
    sn.append(box(ax, 78, 74 - i * 30, 20, 17, t, fc=F2, fs=7.8))
ax.plot([32, 32], [8, 90], color=C["sage"], lw=1.4, ls=(0, (5, 3)))
ax.text(32, 94, "预防屏障\n准入/交底/作业票/旁站", ha="center", fontsize=7.8, color=C["sage"])
ax.plot([68, 68], [8, 90], color=ORANGE, lw=1.4, ls=(0, (5, 3)))
ax.text(68, 94, "缓解屏障\n应急处置/演练/保险", ha="center", fontsize=7.8, color=ORANGE)
for n in cn:
    arrow(ax, n, hz, color=GRAY, lw=1.1)
for n in sn:
    arrow(ax, hz, n, color=BRICK, lw=1.1)
ax.text(50, 2, "屏障失效是事故链条的关键节点；精细化管理的落点是把每道屏障变成可查验的具体动作",
        ha="center", fontsize=8, color=NAVY)
save(fig, OUT + "p3_c2_bowtie.png")

# ---------------- c3 分类分级矩阵 ----------------
fig, ax = canvas(6.6, 6.0, ylim=(0, 118))
cells = [["A1", "A2", "B1"],    # 高风险：能力弱→强
         ["A2", "B1", "B2"],    # 中风险
         ["B2", "C1", "C2"]]    # 低风险
shade = {"A1": "#B0512A", "A2": "#C9622E", "B1": "#E0A33E", "B2": "#EFD9B4",
         "C1": "#DCE3EC", "C2": "#F0F3F7"}
tcol = {"A1": "white", "A2": "white"}
x0, y0, s_ = 26, 24, 20
for i in range(3):
    for j in range(3):
        lab = cells[i][j]
        ax.add_patch(mp.Rectangle((x0 + j * s_, y0 + (2 - i) * s_), s_, s_,
                                  facecolor=shade[lab], edgecolor=C["ink"], lw=0.9))
        ax.text(x0 + j * s_ + s_ / 2, y0 + (2 - i) * s_ + s_ / 2, lab, ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=tcol.get(lab, C["ink"]))
for j, t in enumerate(["能力弱\n(<60 分)", "能力中\n(60~80 分)", "能力强\n(≥80 分)"]):
    ax.text(x0 + j * s_ + s_ / 2, y0 - 5.5, t, ha="center", va="center", fontsize=8, color=C["ink"])
for i, t in enumerate(["高风险\nD>160", "中风险\n70<D≤160", "低风险\nD≤70"]):
    ax.text(x0 - 3, y0 + (2 - i) * s_ + s_ / 2, t, ha="right", va="center", fontsize=8, color=C["ink"])
ax.text(x0 + 1.5 * s_, 11, "相关方安全管理能力评分", ha="center", fontsize=9, fontweight="bold", color=NAVY)
ax.text(5, y0 + 1.5 * s_, "作\n业\n风\n险\n等\n级", ha="center", va="center", fontsize=9,
        fontweight="bold", color=NAVY, linespacing=1.4)
leg = ["A 级：专人旁站、全过程监督，月度检查≥2 次，作业逐项审批",
       "B 级：重点抽查、作业前审批，月度检查 1 次",
       "C 级：常态管理、季度检查，以资料核验为主"]
for k, t in enumerate(leg):
    ax.add_patch(mp.Rectangle((6, 114 - k * 6.0), 3.4, 3.4,
                              facecolor=["#B0512A", "#E0A33E", "#DCE3EC"][k], edgecolor=C["ink"], lw=0.7))
    ax.text(11.5, 115.7 - k * 6.0, t, va="center", fontsize=8, color=C["ink"])
ax.text(50, 2, "风险越高、能力越弱，监管强度越高——监管资源按二维定级差异化投放",
        ha="center", fontsize=8, color=NAVY)
save(fig, OUT + "p3_c3_matrix.png")

# ---------------- c4 全过程闭环监管路径 ----------------
fig, ax = canvas(8.6, 4.8)
nodes = ["① 准入审核\n资质·体系·业绩", "② 合同与安全协议\n责任界面·经济条款",
         "③ 作业前交底\n风险告知·电子作业票", "④ 作业中监督\n旁站·抽查·变更管理",
         "⑤ 验收与绩效评价\n量化打分·结果归档", "⑥ 分析改进\n隐患归因·制度迭代"]
pos = loop_positions(50, 50, 33, 30, 6, start_deg=105, clockwise=True)
ns = [box(ax, x - 13, y - 8.5, 26, 17, t, fc=F1, fs=7.6) for (x, y), t in zip(pos, nodes)]
for i in range(6):
    arrow(ax, ns[i], ns[(i + 1) % 6], color=NAVY, lw=1.2, rad=-0.12)
circle(ax, 50, 50, 11, "闭环\n管控", fc=F2, fs=9.5, bold=True)
for n in ns:
    ax.plot([n[0], 50 + (n[0] - 50) * 0.32], [n[1], 50 + (n[1] - 50) * 0.32],
            color=GRAY, lw=0.6, ls=(0, (2, 2)), zorder=0)
ax.text(50, 3, "评价结果回流至准入环节，形成“准入—监管—评价—改进”的经济与准入双重约束",
        ha="center", fontsize=8, color=NAVY)
save(fig, OUT + "p3_c4_closedloop.png")

# ---------------- c5 数字化赋能架构 ----------------
fig, ax = canvas(8.4, 4.8)
rows = [("决策支持层", ["风险热力图", "分级排名看板", "监管资源配置", "隐患归因分析"], F1, 74),
        ("监管应用层", ["电子作业票", "隐患随手拍", "视频行为预警", "培训与考试"], F1, 53),
        ("主数据层", ["资质档案", "人员与证书", "违章计分台账", "评价结果库"], "#E9EEF4", 32),
        ("感知层", ["人员定位标签", "现场摄像头", "气体检测仪", "移动终端"], F3, 11)]
for name, mods, fc, y in rows:
    band(ax, 12, y, 86, 18, "", fc=fc)
    ax.text(14.5, y + 9, name, fontsize=8.8, fontweight="bold", color=NAVY, va="center")
    for j, m in enumerate(mods):
        box(ax, 35 + j * 15.8, y + 3.5, 14.6, 11, wrap(m, 5), fc="white", fs=7.4)
for y in [29, 50, 71]:
    arrow(ax, (26, y), (26, y + 3), color=NAVY, lw=1.4, head=8)
ax.text(55, 4, "数字化不替代人工，而是把“看不见的履责过程”变成可留痕、可比对、可考核的数据",
        ha="center", fontsize=8, color=NAVY)
save(fig, OUT + "p3_c5_digital.png")
print("[done] p3 concept figures")
