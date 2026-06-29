# 向 nature-skills 学习：图表诚实性与深层论证审查

**日期**：2026-06-08
**影响范围**：light-figure-drawing、light-paper-polishing

## 背景

调研 `Yuan1z0825/nature-skills`（约 1.8 万星的第三方科研技能包，对标 Nature 风格，绘图血统来自顶刊出图脚本 `ChenLiu-1996/figures4papers`）及真正的官方权威 Nature Research Figure Guide。目的是给 Light 的图表与润色技能找改进点。

盘点发现两个明确缺口与调研结论吻合：
- figure-drawing 的图表诚实性只做了一半（有误差棒/显著性，但缺 y 轴截断、双轴误导、误差棒类型等硬规范）。
- paper-polishing "深层优先"但深层论证完全无工具支撑（只有表层语法和词级黑名单）。

## 决策

- **图表**：补"图表诚实性硬规范"（`references/figure_integrity.md`）+ 静态 lint 脚本（`figure_integrity_lint.py`，扫 y 轴截断/双轴/bar 无误差棒/rainbow 色图/3D 等）。
- **润色**：把深层论证落成可操作的四环（`references/argument_review.md`）——Claim–Evidence–Boundary、Hedging 校准阶梯、章节责任分工、AI 披露；并给 `mechanical_check.py` 加 `claim_strength` 检测，对强主张词给出降级建议。
- **只学公开规范与思路，不抄 nature-skills 文本**：色盲色板、栏宽字号、CEB、Hedging 阶梯这些是行业标准/官方规范/学术常识，不是某仓库的版权表达；用 Light 自己的实现和措辞重写。

## 理由

这两项都符合 Light "脚本管机械可验证、人管判断"的一贯分工：图表诚实性的常见误导模式（截断轴、双轴、裸 bar）可静态扫描提示；强主张词可词表检测并给降级建议。但都明确标注"只提示不阻断，最终判断交作者"——因为 ylim 非 0、用 prove 都可能在特定语境完全合理，脚本不能越界替作者下结论。

未照搬 nature-skills 的全部机制（如它的 12 步润色工作流、语义配色系统）——Light 已有自己的四步润色流水线和 Okabe-Ito 配色体系，重复造会割裂现有结构。只补真正缺的、且能融入现有结构的点。这是 [ars-borrow-boundary](2026-06-08-ars-borrow-boundary.md) 复核原则的再次应用：补普适的诚实底线，不照搬对方的特定结构。

## 复核问题

下次再从某个高人气技能包借鉴时，先问：

> **这个点是"普适的学术规范/诚实底线"，还是"对方的特定结构选择"？**

普适规范（图表不误导、主张配证据、AI 要披露）→ 学，用自己的实现重写。
特定结构（对方的 N 步工作流、配色命名体系）→ 除非 Light 缺对应能力，否则不照搬，避免割裂现有结构。
