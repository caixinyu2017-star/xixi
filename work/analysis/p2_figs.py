# -*- coding: utf-8 -*-
"""论文2 概念图：研究框架图 / 多层委托代理衰减机制图 / 四维穿透机制图 / 三阶段实施路径图 / 数据中台架构图"""
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from diagram import *      # noqa
from style import C, save

OUT = "/home/user/xixi/work/figures/"
INK, SAGE, CLAY, GRAY = C["ink"], C["sage"], C["clay"], C["gray"]
F1, F2, F3 = "#EEF2EE", "#F7F0E6", "#F2F4F7"

# ---------------- c1 研究框架图 ----------------
fig, ax = canvas(9.4, 5.0, xlim=(0, 116))
tiers = [
    ("理论视角", ["多层委托代理", "协同治理", "穿透式监管"], F1, 78, 92),
    ("问题诊断", ["层级监督衰减", "数据孤岛与烟囱", "责任传导虚化"], F2, 57, 82),
    ("四维穿透", ["制度穿透 · 数据穿透", "流程穿透 · 责任穿透", "队伍穿透（保障）"], F1, 36, 74),
    ("效能验证", ["监督效能指数", "监督成本—收益均衡", "分批推行准实验"], F3, 15, 62),
]
prev = None
for name, subs, fc, y, w in tiers:
    x = (100 - w) / 2
    band(ax, x, y, w, 16, name, fc=fc, fs=9.5)
    for j, s in enumerate(subs):
        box(ax, x + 16 + j * ((w - 18) / 3), y + 3, (w - 20) / 3, 10, wrap(s, 8), fc="white", fs=7.5)
    if prev is not None:
        arrow(ax, (50, prev), (50, y + 16), color=INK, lw=1.3)
    prev = y
arrow(ax, (88, 22), (88, 62), color=CLAY, ls=(0, (4, 3)), lw=1.1, rad=-0.45)
ax.text(104, 42, "证据反馈\n以效能数据\n回调路径设计", ha="center", va="center",
        fontsize=7.6, color=CLAY, linespacing=1.5)
save(fig, OUT + "p2_c1_framework.png")

# ---------------- c2 多层委托代理与监督衰减机制 ----------------
fig, ax = canvas(8.6, 4.8)
levels = ["国家局", "省级局", "市级局", "县级局（末梢）"]
ys = [78, 58, 38, 15]
ns = []
for t, y in zip(levels, ys):
    ns.append(box(ax, 20, y, 34, 15, t, fc=F1 if t != "县级局（末梢）" else F2, fs=9, bold=True))
for i in range(3):
    arrow(ax, ns[i], ns[i + 1], color=INK, lw=1.2, text="授权委托", fs=7.4, toff=(9, 0))
arrow(ax, (18, 20), (18, 84), color=GRAY, ls=(0, (4, 3)), lw=1.0, rad=0.0,
      text="信息上报\n（选择性过滤）", fs=7.4, toff=(-9, 0))
# 衰减楔形
import matplotlib.patches as mp
ax.add_patch(mp.Polygon([(60, 93), (68, 93), (65.5, 15), (62.5, 15)], closed=True,
                        facecolor="#DCE4DC", edgecolor=C["ink"], lw=0.8))
ax.text(64, 96.5, "监督强度", ha="center", fontsize=8.5, color=INK)
for y, lab in zip(ys, ["100%", "≈70%", "≈49%", "≈34%"]):
    ax.text(70, y + 7.5, lab, ha="left", va="center", fontsize=8, color=CLAY)
    ax.plot([59, 69], [y + 7.5, y + 7.5], color=GRAY, lw=0.6, ls=(0, (2, 2)))
e1 = box(ax, 79, 66, 19, 13, "信息不对称", fc=F2, fs=8)
e2 = box(ax, 79, 44, 19, 13, "管办合一\n双重角色", fc=F2, fs=8)
e3 = box(ax, 79, 22, 19, 13, "熟人社会\n人情约束", fc=F2, fs=8)
for e, yy in [(e1, 68), (e2, 48), (e3, 26)]:
    inhibit(ax, e, (68, yy), color=C["brick"], ls=(0, (3, 2)))
ax.text(50, 5, "监督效力沿层级逐级折损（衰减因子 δ）；穿透式监督的实质是新增一条不随层级衰减的直达通道",
        ha="center", fontsize=8.2, color=INK)
save(fig, OUT + "p2_c2_agency.png")

# ---------------- c3 四维穿透机制图 ----------------
fig, ax = canvas(6.6, 5.6, ylim=(-6, 100))
hub = circle(ax, 50, 50, 15, "穿透式\n大监督", fc=INK, tc="white", fs=10, bold=True)
dims = [("制度穿透", "统一标准与权责清单", 50, 86, F1),
        ("数据穿透", "一次采集、多方复用", 86, 50, F1),
        ("流程穿透", "业务链嵌入监督卡点", 50, 14, F1),
        ("责任穿透", "刚性问责与闭环整改", 14, 50, F1)]
pts = []
for name, sub, x, y, fc in dims:
    n = box(ax, x - 17, y - 9, 34, 18, f"{name}\n{sub}", fc=fc, fs=8.5)
    pts.append(n)
    dblarrow(ax, hub, n, color=INK, lw=1.2)
for i in range(4):
    a, b = pts[i], pts[(i + 1) % 4]
    arrow(ax, a, b, color=SAGE, ls=(0, (4, 3)), lw=1.0, rad=0.32, pad=1.2)
ax.text(50, -2.5, "四维互为条件：制度定标准、数据供证据、流程设卡点、责任保落地",
        ha="center", fontsize=8.2, color=INK)
save(fig, OUT + "p2_c3_fourdim.png")

# ---------------- c4 三阶段实施路径图 ----------------
fig, ax = canvas(9.2, 4.2)
arrow(ax, (4, 50), (96, 50), color=INK, lw=2.0, head=9)
ms = [(20, "第一阶段  0—6 个月", "制度穿透先行", ["监督权责清单", "高风险领域标准", "指标口径统一"],
       ["2 个县级局试点", "基线数据采集"]),
      (50, "第二阶段  6—18 个月", "数据与流程穿透", ["监督数据中台", "风险预警模型", "业务卡点嵌入"],
       ["市级全域推行", "监督减负核算"]),
      (80, "第三阶段  18—36 个月", "责任穿透与固化", ["刚性问责机制", "效能指数考核", "长效制度固化"],
       ["全域评估", "经验复制推广"])]
for x, ph, sub, ups, dns in ms:
    circle(ax, x, 50, 3.2, "", fc=CLAY, ec=INK)
    box(ax, x - 15, 62, 30, 30, ph + "\n" + sub + "\n\n" + "\n".join("· " + u for u in ups),
        fc=F1, fs=8)
    box(ax, x - 15, 16, 30, 22, "\n".join("· " + d for d in dns), fc=F2, fs=8)
    ax.plot([x, x], [53.2, 62], color=INK, lw=0.9)
    ax.plot([x, x], [38, 46.8], color=INK, lw=0.9)
ax.text(4, 55, "建设任务", fontsize=8.2, color=GRAY)
ax.text(4, 41, "落地范围", fontsize=8.2, color=GRAY)
ax.text(50, 6, "阶段优先级由蒙特卡洛边际贡献仿真确定：制度与数据维度先行，责任维度收口",
        ha="center", fontsize=8.2, color=INK)
save(fig, OUT + "p2_c4_rollout.png")

# ---------------- c5 数据中台架构图 ----------------
fig, ax = canvas(8.6, 5.2)
rows = [("监督应用", ["风险预警", "线索派发", "整改督办", "效能评价"], F1, 76),
        ("分析模型", ["围标串标识别", "费用异常识别", "审批越权识别", "关联交易画像"], F1, 58),
        ("统一监督数据中台", ["数据汇聚", "口径校核", "血缘追溯", "权限管控"], "#E4EAE4", 40),
        ("数据标准与安全分级", ["分类分级", "脱敏与授权", "可用不可见", "审计留痕"], F2, 22),
        ("业务系统", ["烟叶生产", "卷烟营销", "物资采购", "财务资金", "专卖执法"], F3, 4)]
for name, mods, fc, y in rows:
    band(ax, 14, y, 84, 15, "", fc=fc)
    ax.text(16.5, y + 7.5, name, fontsize=8.8, fontweight="bold", color=INK, va="center")
    n = len(mods)
    for j, m in enumerate(mods):
        box(ax, 38 + j * (58 / n), y + 3, 58 / n - 1.5, 9, wrap(m, 5), fc="white", fs=7.3)
for y in [4 + 15, 22 + 15, 40 + 15, 58 + 15]:
    arrow(ax, (30, y), (30, y + 3), color=INK, lw=1.3, head=8)
band(ax, 1, 4, 11, 87, "", fc="#F7F0E6")
ax.text(6.5, 47, "一\n次\n采\n集\n多\n方\n复\n用", ha="center", va="center", fontsize=9,
        fontweight="bold", color=CLAY, linespacing=1.5)
save(fig, OUT + "p2_c5_platform.png")
print("[done] p2 concept figures")
