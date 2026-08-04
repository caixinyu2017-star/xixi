# -*- coding: utf-8 -*-
"""论文4 概念图：外部性治理机制图 / 角色边界图 / 多中心协同结构图 / 助推式吸烟点设计示意图 / PDCA评估闭环路径图"""
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from diagram import *      # noqa
from style import C, save
import matplotlib.patches as mp

OUT = "/home/user/xixi/work/figures/"
TEAL, SAND, BRICK, GRAY = C["teal"], "#D9C08C", C["brick"], C["gray"]
F1, F2, F3 = "#E6F0F0", "#F7F1E3", "#F4F6F7"

# ---------------- c1 外部性治理机制图 ----------------
fig, ax = canvas(9.0, 4.4)
a = box(ax, 3, 42, 22, 18, "无序吸烟行为", fc=F1, fs=9, bold=True)
b = box(ax, 38, 42, 24, 18, "负外部性\n二手烟暴露·烟蒂散落", fc=F1, fs=8.5, bold=True)
c = box(ax, 75, 42, 22, 18, "公共环境\n品质损失", fc=F1, fs=9, bold=True)
arrow(ax, a, b, color=TEAL, lw=1.5, text="产生", fs=8, toff=(0, 3))
arrow(ax, b, c, color=TEAL, lw=1.5, text="导致", fs=8, toff=(0, 3))
m1 = box(ax, 18, 74, 30, 16, "设施供给与科学选址\n（降低规范吸烟的行为成本）", fc=F2, fs=7.8)
m2 = box(ax, 18, 20, 30, 16, "助推式环境设计\n（提示、距离、可见性）", fc=F2, fs=7.8)
inhibit(ax, m1, (31.5, 60.8), color=BRICK, ls=(0, (3, 2)))
inhibit(ax, m2, (31.5, 41.2), color=BRICK, ls=(0, (3, 2)))
# 社会规范反馈：绕行折线，避免与调节变量框交叠
ax.plot([86, 86, 14, 14], [42, 8, 8, 38], color=GRAY, lw=1.1, ls=(0, (4, 3)), zorder=1)
arrow(ax, (14, 20), (14, 41), color=GRAY, ls=(0, (4, 3)), lw=1.1, shrink=0)
ax.text(58, 5, "社会规范反馈：他人守规行为提高个体守规概率", ha="center", fontsize=7.8, color=GRAY,
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
ax.text(50, 96, "两条调节路径均作用于“行为—外部性”这条边，而非作用于结点本身",
        ha="center", fontsize=8.2, color=C["ink"])
save(fig, OUT + "p4_c1_externality.png")

# ---------------- c2 角色边界图 ----------------
fig, ax = canvas(8.4, 4.6)
dashed_region(ax, 2, 6, 78, 86, None, ec=C["ink"], lw=1.1)
ax.text(41, 95, "控烟优先前提下的行业参与边界", ha="center", fontsize=9.5,
        fontweight="bold", color=C["ink"])
ax.plot([4, 78], [50, 50], color=C["ink"], lw=1.0, ls=(0, (5, 3)))
ax.text(7, 84, "可为", fontsize=9.5, fontweight="bold", color=TEAL)
ax.text(7, 43, "不可为", fontsize=9.5, fontweight="bold", color=BRICK)
ok = ["设施出资但不冠名\n不出现品牌标识", "烟蒂清理与\n保洁支持", "无品牌元素的\n文明提示物料"]
no = ["品牌标识、广告\n与促销赞助", "设于未成年人\n聚集场所周边", "主导或影响\n控烟政策制定"]
for j, t in enumerate(ok):
    box(ax, 6 + j * 24, 60, 22, 18, t, fc=F1, fs=7.8)
for j, t in enumerate(no):
    box(ax, 6 + j * 24, 16, 22, 18, t, fc="#F7E9E8", fs=7.8, ec=BRICK)
band(ax, 84, 6, 14, 86, "", fc=F2)
ax.text(91, 49, "政\n府\n与\n场\n所\n方\n主\n导", ha="center", va="center", fontsize=9,
        fontweight="bold", color=C["clay"], linespacing=1.5)
for y in [69, 49]:
    arrow(ax, (84, y), (80, y), color=C["clay"], lw=1.0, head=6)
ax.text(41, 1.5, "边界清晰是行业参与公共治理的正当性前提，也是规避《烟草控制框架公约》第 5.3 条与第 13 条风险的必要条件",
        ha="center", fontsize=7.8, color=C["ink"])
save(fig, OUT + "p4_c2_boundary.png")

# ---------------- c3 多中心协同治理结构 ----------------
fig, ax = canvas(6.8, 5.4)
hub = hexagon(ax, 50, 50, 15, "协同议事平台\n（联席会议·信息共享）", fc=TEAL, tc="white", fs=8.5)
roles = [("政府部门", "规划引领·标准制定·监督管理", 20, 82),
         ("场所管理单位", "日常管理·设施维护·秩序引导", 80, 82),
         ("烟草商业企业", "有限支持·理念宣传·环境改善", 20, 18),
         ("社会组织与公众", "志愿服务·社会监督·自律共建", 80, 18)]
ns = []
for name, sub, x, y in roles:
    n = box(ax, x - 18, y - 10, 36, 20, f"{name}\n{sub}", fc=F1, fs=8)
    ns.append(n)
    dblarrow(ax, hub, n, color=C["ink"], lw=1.1)
for i, j in [(0, 1), (1, 3), (3, 2), (2, 0)]:
    arrow(ax, ns[i], ns[j], color=C["sage"], ls=(0, (4, 3)), lw=1.0, rad=0.0, pad=1.0)
ax.text(50, 3, "协同不等于主体叠加：需明确职责分工、成本分担与信息共享的具体规则",
        ha="center", fontsize=8.2, color=C["ink"])
save(fig, OUT + "p4_c3_polycentric.png")

# ---------------- c4 助推式吸烟点设计示意图 ----------------
fig, ax = canvas(9.4, 4.8, xlim=(-6, 112))
# 主体：吸烟点平面示意
ax.add_patch(mp.FancyBboxPatch((36, 36), 26, 26, boxstyle="round,pad=1.5",
                               facecolor=F1, edgecolor=C["ink"], lw=1.3))
ax.text(49, 56, "指定吸烟点", ha="center", fontsize=9.5, fontweight="bold", color=C["ink"])
ax.add_patch(mp.Rectangle((41, 40), 7, 7, facecolor=SAND, edgecolor=C["ink"], lw=0.9))
ax.text(44.5, 43.5, "烟蒂\n收集", ha="center", va="center", fontsize=7, color=C["ink"])
ax.add_patch(mp.Rectangle((52, 40), 7, 7, facecolor="#EDEDED", edgecolor=C["ink"], lw=0.9))
ax.text(55.5, 43.5, "地面\n导引", ha="center", va="center", fontsize=7, color=C["ink"])
ax.plot([36, 62], [50, 50], color=GRAY, lw=0.7, ls=(0, (2, 2)))
callouts = [("① 高识别度标识\n视距 15 m 内可辨", 8, 84, (40, 62)),
            ("② 烟蒂收集装置\n距站立位不超过 2 步", 8, 20, (44.5, 40)),
            ("③ 下风向布置\n与人流通道错开", 90, 84, (58, 62)),
            ("④ 与出入口、\n等候区间隔≥ 8 m", 90, 20, (58, 40)),
            ("⑤ 顶部半开敞\n保证自然通风", 90, 52, (62, 52))]
for t, x, y, tgt in callouts:
    n = box(ax, x - 16, y - 8, 32, 16, t, fc=F2 if x < 50 else F3, fs=7.6)
    ax.plot([n[0] + (16 if x < 50 else -16), tgt[0]], [n[1], tgt[1]],
            color=GRAY, lw=0.8, ls="-", zorder=0)
ax.text(49, 6, "五项要素均可量化验收；助推的要义是降低规范行为的实施成本，而非增加禁止性标语",
        ha="center", fontsize=8, color=C["ink"])
save(fig, OUT + "p4_c4_nudge.png")

# ---------------- c5 PDCA 评估闭环 ----------------
fig, ax = canvas(7.6, 5.0)
quad = [("P 计划\n选址优化与\n标准制定", 30, 74, "覆盖率最大化模型"),
        ("D 实施\n设施部署与\n助推设计", 70, 74, "场所协议与分工"),
        ("C 检查\n暴露与烟蒂\n监测", 70, 30, "双重差分评估"),
        ("A 改进\n标准修订与\n经验推广", 30, 30, "指南更新")]
ns = []
for t, x, y, sub in quad:
    n = box(ax, x - 16, y - 12, 32, 24, t, fc=F1, fs=8.5, bold=True)
    ns.append(n)
    box(ax, x - 16, y - 24, 32, 9, sub, fc=F2, fs=7.5)
for i in range(4):
    arrow(ax, ns[i], ns[(i + 1) % 4], color=TEAL, lw=1.3, rad=-0.15)
ax.text(50, 6, "闭环的关键在“C”：没有暴露与落地率的实测数据，前三步无法证伪，也无法迭代",
        ha="center", fontsize=8.2, color=C["ink"])
save(fig, OUT + "p4_c5_pdca.png")
print("[done] p4 concept figures")
