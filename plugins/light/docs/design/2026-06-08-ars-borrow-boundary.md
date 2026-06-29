# 向 ARS 学习的取舍：学诚实工程，不照搬其拒绝边界

**日期**：2026-06-08
**影响范围**：m03 idea-generation、m04 idea-critique、Light 全局定位

## 背景

ARS（Academic Research Skills for Claude Code，作者 Wu C.-I.，CC BY-NC 4.0）是一个成熟的学术研究 copilot 框架，4 个技能覆盖"研究→论文→审稿→管道"。我们调研它，想看能学到什么。

调研中发现两件事：

1. Light 过去其实已经从 ARS 借鉴过一部分——`light-paper-drafting` 的 7 类 AI 失败模式（M1–M7，含 frame-lock）与 ARS 的 7-mode checklist 同源（都追溯到 The AI Scientist 的失败模式分析）；`light-idea-critique` 的 calibration.py（FNR/FPR 自校准）明确借鉴了 ARS 的 reviewer calibration 模式。
2. ARS 有一条**鲜明的拒绝边界**：它把"idea/hypothesis 生成"主动列为拒绝机制（其 POSITIONING.md "Rejected mechanisms"），理由是"替学者提研究问题，会让学者沦为 AI 输出的审稿人，而非作者"。

第 2 点与 Light 直接冲突——Light 有 m03 idea-generation ⇄ m04 idea-critique 这个核心闭环。

## 决策

- **学 ARS 的诚实工程机制**：失败模式可见化、审稿人自我校准、引用忠实核验、人在环检查点、边界写成文档（即本目录）。这些与定位无关，纯属把"AI 可能错在哪"做成机制，照学。
- **不照搬 ARS 拒绝 idea-generation 的边界**。Light 保留 m03，但**用 m04 严审来约束它**：idea 由 AI 提出后，必须过 idea-critique 的对抗式打分，不过关就打回 m03；最终选择权始终在用户。
- 不照搬 ARS 对"实验自动执行""paper→PPT 自动生成"的全面拒绝——Light 的 a03、m16 在用户主导下执行这些，但同样受 self-review、research-ethics 常驻闸门约束。

## 理由

ARS 的拒绝边界源自它"纯 copilot、绝不替学者做研究状态转移"的定位，这个定位本身是自洽且值得尊重的。但 Light 的定位不同：Light 面向更宽的场景（含竞赛、数模、本科生科研训练），在这些场景里"帮你想几个方向再一起挑"是真实且正当的需求。

关键区别不在于"AI 能不能提 idea"，而在于**谁掌握最终决策权、有没有对抗式审查兜底**。Light 的答案是：AI 可以提，但必须经 m04 严审 + 用户拍板，AI 永远不替用户"选定"研究问题。这样既保留能力，又避免 ARS 担心的"学者沦为审稿人"——因为用户在 m04 之后仍是拍板者，不是被动接收者。

照搬 ARS 的拒绝边界 = 砍掉 Light 的核心闭环，得不偿失且没有必要。

## 复核问题

下次再遇到"要不要从某个克制型系统借鉴它的拒绝边界"时，先问：

> **这条边界是对方"定位"的产物，还是普适的诚实底线？**

- 如果是**普适诚实底线**（不造假、不幻觉引用、不夸大、不隐瞒 AI 使用）→ 照学，Light 也该守。
- 如果是**对方特定定位的产物**（如"绝不替学者提 idea"）→ 对照 Light 自己的定位判断，不盲从。判据：谁掌握最终决策权？只要决策权在用户、且有对抗式审查兜底，该能力就可以保留。
