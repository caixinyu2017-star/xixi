# -*- coding: utf-8 -*-
"""论文1 概念图：技术路线图 / 三层架构图 / 多模态融合机制图 / 程序合规校验路径图 / 算法治理机制图"""
import sys
sys.path.insert(0, "/home/user/xixi/work/analysis")
from diagram import *          # noqa
from style import C, save

OUT = "/home/user/xixi/work/figures/"
NAVY, STEEL, AMBER, GRAY, BRICK = C["navy"], C["steel"], C["amber"], C["gray"], C["brick"]
FILL1, FILL2, FILL3 = "#EAF0F7", "#F7F0E2", "#F2F4F7"

# ---------------- 图 c1 技术路线图 ----------------
fig, ax = canvas(9.0, 4.6)
stages = [
    ("一 问题诊断", ["抽检覆盖率不足15%", "证据调取平均40分钟", "程序瑕疵难以校验", "视频数据价值沉睡"], FILL2),
    ("二 系统设计", ["数据层：接入与治理", "模型层：推理与适配", "应用层：三端服务", "安全与隐私护栏"], FILL1),
    ("三 领域适配", ["关键帧自适应采样", "LoRA 领域微调", "程序规则引擎", "代价敏感阈值"], FILL1),
    ("四 验证与治理", ["消融与配对显著性检验", "人机协同筛查策略", "人在回路复核与申诉", "投入产出与推广"], FILL3),
]
x0, w, gap = 3.0, 21.5, 2.0
for i, (h, subs, fc) in enumerate(stages):
    x = x0 + i * (w + gap)
    box(ax, x, 68, w, 11, h, fc=NAVY, tc="white", fs=9.5, bold=True)
    for j, s in enumerate(subs):
        box(ax, x, 55 - j * 12.5, w, 10.5, wrap(s, 11), fc=fc, fs=7.8)
arrow(ax, (x0 + w, 85.5), (x0 + 3 * (w + gap), 85.5), color=NAVY, lw=1.8, head=9)
ax.text(50, 89.5, "研究推进主线", ha="center", fontsize=8.5, color=NAVY)
arrow(ax, (x0 + 3 * (w + gap) + w / 2, 3.5), (x0 + 2 * (w + gap) + w / 2, 3.5),
      color=BRICK, ls=(0, (4, 3)), lw=1.2, text="迭代反馈：按验证结果回调采样率、微调数据与阈值", fs=7.5, toff=(0, 2.6))
save(fig, OUT + "p1_c1_roadmap.png")

# ---------------- 图 c2 三层架构 ----------------
fig, ax = canvas(8.4, 5.4)
layers = [
    ("应用层", ["法制监督端", "执法办案端", "管理决策端", "对外服务接口"], FILL1, 68),
    ("模型层", ["Qwen Omni 推理引擎", "LoRA 领域适配器", "程序合规规则引擎", "模型服务网关"], FILL2, 40),
    ("数据层", ["执法记录仪视频接入", "案件与人员结构化数据", "特征与向量存储", "冷热分级存储"], FILL3, 12),
]
for name, mods, fc, y in layers:
    band(ax, 3, y, 78, 22, name, fc=fc, fs=10)
    for j, m in enumerate(mods):
        box(ax, 14.5 + j * 16.6, y + 5, 15.6, 12, wrap(m, 7), fc="white", fs=7.5)
for y0, y1 in [(40 + 22, 68), (12 + 22, 40)]:
    dblarrow(ax, (42, y0), (42, y1), color=NAVY, lw=1.2)
band(ax, 84, 12, 13, 78, "", fc="#FBF3E8")
ax.text(90.5, 51, "安\n全\n与\n隐\n私\n治\n理", ha="center", va="center", fontsize=9,
        fontweight="bold", color=C["clay"], linespacing=1.5)
for y in [23, 51, 79]:
    arrow(ax, (84, y), (81, y), color=C["clay"], lw=1.0, head=6)
save(fig, OUT + "p1_c2_architecture.png")

# ---------------- 图 c3 多模态融合与时序对齐机制 ----------------
fig, ax = canvas(9.0, 4.6)
ins = [("视频帧序列", 74), ("现场音频流", 50), ("文书与规范文本", 26)]
encs = [("SigLIP2\n视觉编码器", 74), ("AuT\n音频编码器", 50), ("文本\nTokenizer", 26)]
for (t, y), (e, _) in zip(ins, encs):
    box(ax, 2, y - 6, 15, 12, wrap(t, 6), fc=FILL3, fs=8)
    box(ax, 21, y - 6, 15, 12, e, fc=FILL1, fs=7.8)
    arrow(ax, (17, y), (21, y), color=GRAY)
cx = box(ax, 41, 38, 17, 32, "统一\nToken\n序列", fc=NAVY, tc="white", fs=9.5, bold=True)
for _, y in ins:
    arrow(ax, (36, y), (41, 54 if y > 50 else (54 if y == 50 else 46)), color=STEEL, rad=0.12)
box(ax, 41, 22, 17, 10, "TMRoPE\n绝对时间轴", fc=FILL2, fs=7.8)
arrow(ax, (49.5, 32), (49.5, 38), color=AMBER, ls=(0, (3, 2)), lw=1.2)
box(ax, 63, 38, 16, 20, "Thinker\nMoE\n跨模态推理", fc=FILL1, fs=8.5, bold=True)
arrow(ax, (58, 48), (63, 48), color=NAVY, lw=1.4)
box(ax, 84, 56, 14, 14, "程序合规\n判定", fc=FILL2, fs=8)
box(ax, 84, 30, 14, 14, "证据链\n时间线", fc=FILL2, fs=8)
arrow(ax, (79, 52), (84, 63), color=NAVY, rad=-0.1)
arrow(ax, (79, 44), (84, 37), color=NAVY, rad=0.1)
ax.text(50, 15, "四类模态在同一语义空间内相互注意，而非特征层拼接；时序由绝对时间轴统一对齐",
        ha="center", fontsize=7.8, color=GRAY)
save(fig, OUT + "p1_c3_mechanism.png")

# ---------------- 图 c4 执法程序合规校验路径 ----------------
fig, ax = canvas(9.6, 4.2)
steps = ["进入\n经营场所", "出示\n执法证件", "表明身份\n说明来意", "告知\n当事人权利",
         "现场检查", "提取\n证据材料", "文书送达\n与结束"]
x0, w, gap = 1.5, 12.2, 1.6
centers = []
for i, s in enumerate(steps):
    x = x0 + i * (w + gap)
    c = box(ax, x, 34, w, 18, s, fc=FILL1, fs=8)
    centers.append(c)
    if i:
        arrow(ax, (x - gap - 0.2, 43), (x + 0.2, 43), color=NAVY, lw=1.3, shrink=0.5)
    diamond(ax, c[0], 68, 11, 13, "校验", fc=FILL2, fs=7.5)
    arrow(ax, (c[0], 52), (c[0], 61.5), color=GRAY, ls=(0, (3, 2)), lw=0.9, head=5)
    arrow(ax, (c[0] + 2.2, 74.5), (c[0] + 2.2, 84), color=GRAY, ls=(0, (3, 2)), lw=0.9, head=5)
    box(ax, c[0] - w / 2, 84, w, 9, ["主体", "主体", "言语", "程序", "程序", "证据", "文书"][i],
        fc="white", fs=7.5, ec=GRAY)
band(ax, 1.5, 16, 96, 12, "", fc="#FBF3E8")
ax.text(49.5, 22, "时序约束：环节缺失或顺序错位即触发程序瑕疵告警（依托 TMRoPE 绝对时间戳）",
        ha="center", va="center", fontsize=8, color=C["clay"])
for c in centers:
    ax.plot([c[0], c[0]], [28, 34], color=C["clay"], lw=0.8, ls=(0, (2, 2)))
ax.text(49.5, 96, "四维检测口径", ha="center", fontsize=8.5, color=GRAY)
save(fig, OUT + "p1_c4_procedure.png")

# ---------------- 图 c5 数据合规与人在回路治理机制 ----------------
fig, ax = canvas(9.0, 4.6)
ys = 58
xs = [3, 22.5, 42, 61.5, 81]
lbl = ["执法记录仪\n视频采集", "去标识化与\n最小必要处理", "本地化\n私有模型推理",
       "风险提示\n（线索而非结论）", "人工复核\n与认定"]
ns = [box(ax, x, ys, 16, 17, t, fc=FILL1, fs=8) for x, t in zip(xs, lbl)]
for i in range(4):
    arrow(ax, ns[i], ns[i + 1], color=NAVY, lw=1.3)
dashed_region(ax, 0.5, 50, 78, 34, None, ec=C["clay"])
ax.text(39.5, 87.5, "个人信息保护边界：原始音视频不出省局政务云，不向公网大模型传输",
        ha="center", fontsize=8, color=C["clay"])
ap = box(ax, 61.5, 26, 16, 14, "异议申诉\n与纠错", fc=FILL2, fs=8)
tr = box(ax, 30, 26, 20, 14, "标注与训练\n反馈闭环", fc=FILL2, fs=8)
arrow(ax, ns[4], ap, color=GRAY, lw=1.1, ls=(0, (3, 2)))
arrow(ax, ap, tr, color=GRAY, lw=1.1, ls=(0, (3, 2)))
arrow(ax, tr, ns[2], color=GRAY, lw=1.1, ls=(0, (3, 2)), rad=-0.15)
box(ax, 81, 26, 16, 14, "程序瑕疵\n整改与培训", fc=FILL3, fs=8)
arrow(ax, ns[4], (89, 40), color=NAVY, lw=1.1)
ax.text(50, 12, "算法输出仅作为线索提示，最终认定权保留于法制审核人员；\n"
                "结论用于整改与培训改进，不直接作为追责依据，申诉结果反哺模型迭代",
        ha="center", fontsize=8.2, color=EDGE, linespacing=1.5)
save(fig, OUT + "p1_c5_governance.png")
print("[done] p1 concept figures")
