# -*- coding: utf-8 -*-
"""论文5 概念图：技术路线图 / 模型结构机制图 / 循环论证与外部效度设计示意图 / 价值分层示意图 / 应用路径图"""
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from diagram import *      # noqa
from style import C, save
import numpy as np
import matplotlib.patches as mp

OUT = "/home/user/xixi/work/figures/"
NAVY, STEEL, BRICK, GRAY = C["navy"], C["steel"], C["brick"], C["gray"]
F1, F2, F3 = "#EAF0F7", "#F7E9E8", "#F2F4F7"

# ---------------- c1 技术路线图 ----------------
fig, ax = canvas(9.4, 4.2)
cols = [("一 数据获取", ["DII 2010—2024", "去重与失效剔除", "99 分位缩尾"]),
        ("二 标签构造", ["四维价值指标", "熵权法赋权", "自然间断点分级"]),
        ("三 模型构建", ["随机森林基模型", "Kappa 距离聚类", "DBSCAN 剪枝重构"]),
        ("四 效度检验", ["剔标签特征消融", "嵌套交叉验证", "5×2cv 配对检验"]),
        ("五 专卖应用", ["技术壁垒预警", "自由实施(FTO)排查", "非法制品特征溯源"])]
x0, w, gap = 2.0, 18.4, 1.4
for i, (h, subs) in enumerate(cols):
    x = x0 + i * (w + gap)
    box(ax, x, 70, w, 11, h, fc=NAVY, tc="white", fs=9, bold=True)
    for j, sname in enumerate(subs):
        box(ax, x, 56 - j * 13, w, 11, wrap(sname, 9), fc=F1 if i < 3 else F3, fs=7.6)
arrow(ax, (x0 + w, 88), (x0 + 4 * (w + gap), 88), color=NAVY, lw=1.8, head=9)
ax.text(50, 92.5, "研究推进主线", ha="center", fontsize=8.5, color=NAVY)
arrow(ax, (x0 + 3 * (w + gap) + w / 2, 5), (x0 + 1 * (w + gap) + w / 2, 5),
      color=BRICK, ls=(0, (4, 3)), lw=1.2,
      text="效度不足则回到标签构造：更换价值代理变量、剔除与标签同源的特征", fs=7.5, toff=(0, 3.2))
save(fig, OUT + "p5_c1_roadmap.png")

# ---------------- c2 模型结构机制图 ----------------
fig, ax = canvas(9.2, 4.4)
box(ax, 2, 40, 15, 22, "自助采样\nBootstrap", fc=F1, fs=8.5)
# 全体决策树
rng = np.random.default_rng(7)
ax.text(30, 76, "全体基分类器", ha="center", fontsize=8.5, color=NAVY)
for k in range(18):
    cx = 22 + (k % 6) * 3.4
    cy = 68 - (k // 6) * 9
    ax.add_patch(mp.Polygon([(cx, cy), (cx - 1.5, cy - 4.2), (cx + 1.5, cy - 4.2)],
                            closed=True, facecolor=F1, edgecolor=NAVY, lw=0.7))
dashed_region(ax, 19.5, 34, 22.5, 44, None, ec=GRAY)
arrow(ax, (17, 51), (19.5, 51), color=NAVY, lw=1.2)
# 聚类分组
ax.text(58, 76, "Kappa 距离 DBSCAN 聚类分组", ha="center", fontsize=8.5, color=NAVY)
grp_x = [48, 58, 68]
for g, gx in enumerate(grp_x):
    dashed_region(ax, gx - 5, 44, 10, 26, None, ec=STEEL)
    ax.text(gx, 71, f"簇 {g+1}", ha="center", fontsize=7.5, color=STEEL)
    for k in range(4):
        cx = gx - 3 + (k % 2) * 6
        cy = 64 - (k // 2) * 9
        best = (k == 0)
        ax.add_patch(mp.Polygon([(cx, cy), (cx - 1.6, cy - 4.4), (cx + 1.6, cy - 4.4)],
                                closed=True, facecolor="#E0A33E" if best else F1,
                                edgecolor=NAVY, lw=0.8))
arrow(ax, (42, 51), (43, 51), color=NAVY, lw=1.2)
box(ax, 46, 26, 24, 10, "噪声点直接剔除", fc=F2, fs=7.8, ec=BRICK)
arrow(ax, (58, 44), (58, 36), color=BRICK, ls=(0, (3, 2)), lw=1.0)
# 剪枝后子森林
ax.text(84, 76, "剪枝后子森林", ha="center", fontsize=8.5, color=NAVY)
for k in range(3):
    cx = 79 + k * 5
    ax.add_patch(mp.Polygon([(cx, 66), (cx - 1.8, 60), (cx + 1.8, 60)], closed=True,
                            facecolor="#E0A33E", edgecolor=NAVY, lw=0.9))
arrow(ax, (74, 51), (77, 51), color=NAVY, lw=1.2)
box(ax, 76, 38, 20, 12, "多数投票输出\n价值等级", fc=F1, fs=8)
ax.text(50, 14, "每簇仅保留验证集表现最优的一棵树，降低同质化分类器的重复投票权重；"
                "剪枝比例与增益需以 5×2cv 配对检验确认",
        ha="center", fontsize=8, color=C["ink"])
save(fig, OUT + "p5_c2_model.png")

# ---------------- c3 循环论证与外部效度设计 ----------------
fig, ax = canvas(9.2, 4.4)
ax.plot([50, 50], [4, 92], color=C["ink"], lw=1.0)
ax.text(25, 94, "问题：标签与特征同源导致的循环论证", ha="center", fontsize=9.2,
        fontweight="bold", color=BRICK)
ax.text(76, 94, "修补：外部效度检验设计", ha="center", fontsize=9.2, fontweight="bold", color=C["teal"])
l1 = box(ax, 4, 62, 24, 15, "四项价值指标\n引用数·权项数·发明人数·同族数", fc=F2, fs=7.6)
l2 = box(ax, 26, 30, 24, 15, "熵权法综合得分\n→ 价值等级标签", fc=F2, fs=7.6)
l3 = box(ax, 2, 30, 22, 15, "模型特征集\n（含上述四项）", fc=F2, fs=7.6)
arrow(ax, l1, l2, color=BRICK, lw=1.2, rad=-0.2)
arrow(ax, l2, l3, color=BRICK, lw=1.2)
arrow(ax, l3, l1, color=BRICK, lw=1.2, rad=-0.2)
ax.text(38, 56, "同义\n反复", ha="center", va="center", fontsize=8.5, color=BRICK,
        fontweight="bold", bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=BRICK, lw=0.8))
ax.text(25, 16, "模型只是在重新拟合自己定义的规则，\n无法证明其识别的是“价值”而非“规则”",
        ha="center", fontsize=8, color=C["ink"])
r = ["① 剔除同源特征后重训\n观察准确率跌幅",
     "② 引入独立价值代理\n维持年限·转让许可·质押·无效宣告",
     "③ 专家标注留出集\n计算 Kappa 一致性"]
for j, t in enumerate(r):
    box(ax, 54, 66 - j * 22, 44, 17, t, fc="#E6F0F0", fs=8)
    if j:
        arrow(ax, (76, 66 - (j - 1) * 22), (76, 66 - j * 22 + 17), color=C["teal"], lw=1.1, shrink=0)
ax.text(76, 8, "三项检验通过后，准确率才具有可解释的实践含义",
        ha="center", fontsize=8, color=C["ink"])
save(fig, OUT + "p5_c3_circularity.png")

# ---------------- c4 价值分层示意图 ----------------
fig, ax = canvas(9.4, 4.6, xlim=(0, 118))
tiers = [("极高价值尖端集群", "n=77，100%", 78, 46, "#B0512A", "white"),
         ("高价值核心集群", "n=83，95.2%", 60, 56, "#C9622E", "white"),
         ("中价值过渡集群", "n=136，27.2%", 42, 66, "#E0A33E", C["ink"]),
         ("基础外围集群", "n=4658，2.1%", 24, 76, "#EFD9B4", C["ink"])]
for name, sub, y, w, fc, tc in tiers:
    ax.add_patch(mp.Polygon([(50 - w / 2, y), (50 + w / 2, y),
                             (50 + w / 2 - 5, y + 14), (50 - w / 2 + 5, y + 14)],
                            closed=True, facecolor=fc, edgecolor=C["ink"], lw=0.9))
    ax.text(50, y + 7, f"{name}（{sub}）", ha="center", va="center", fontsize=8.0, color=tc)
tracks = ["烟具外观结构、连接装配等浅表改良", "烟草提取工艺、烟气组分调控",
          "电阻式加热元件（核心硬件）", "烟草发烟基质配方（前沿材料）"]
for (name, sub, y, w, fc, tc), t in zip(tiers, tracks[::-1]):
    ax.plot([50 + w / 2, 87], [y + 7, y + 7], color=GRAY, lw=0.7, ls=(0, (2, 2)))
    ax.text(88, y + 7, wrap(t, 11), va="center", fontsize=7.4, color=C["ink"])
arrow(ax, (6, 24), (6, 90), color=NAVY, lw=1.4)
ax.text(2.5, 57, "价\n值\n密\n度", ha="center", va="center", fontsize=8.5, color=NAVY, linespacing=1.4)
ax.text(50, 12, "价值分层与技术赛道高度耦合：越靠近产业链上游材料与核心元件，价值密度越高",
        ha="center", fontsize=8, color=C["ink"])
save(fig, OUT + "p5_c4_layering.png")

# ---------------- c5 专卖管理应用路径图 ----------------
fig, ax = canvas(9.0, 4.2)
src = box(ax, 2, 40, 20, 20, "高价值专利\n识别模型", fc=NAVY, tc="white", fs=9, bold=True)
j = circle(ax, 30, 50, 2.4, "", fc=C["ink"])
arrow(ax, src, (27.6, 50), color=NAVY, lw=1.4)
paths = [("通路 Ⅰ", "海外核心专利壁垒预警", "锁定竞品高价值专利族，\n预判技术封锁点", 78),
         ("通路 Ⅱ", "自由实施（FTO）排查", "为工业企业新品出海\n提供侵权风险清单", 50),
         ("通路 Ⅲ", "非法制品技术特征溯源", "以专利技术特征比对\n辅助涉案物品认定", 22)]
ends = []
for tag, name, sub, y in paths:
    ax.text(36, y + 11, tag, fontsize=7.8, color=STEEL)
    n = box(ax, 36, y - 8, 32, 17, f"{name}\n{sub}", fc=F1, fs=8)
    ends.append(n)
    arrow(ax, (32.4, 50), n, color=STEEL, lw=1.2)
out = box(ax, 76, 36, 22, 28, "专卖管理\n决策支持", fc="#E0A33E", fs=9.5, bold=True)
for n in ends:
    arrow(ax, n, out, color=NAVY, lw=1.2)
ax.text(50, 6, "研究成果的落点应回到专卖管理职能：壁垒预警、侵权排查与涉案物品认定，"
                "而非县级局无法执行的研发立项建议",
        ha="center", fontsize=8, color=C["ink"])
save(fig, OUT + "p5_c5_application.png")
print("[done] p5 concept figures")
