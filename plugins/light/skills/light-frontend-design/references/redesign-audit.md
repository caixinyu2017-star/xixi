# Redesign 审计协议

改造已有项目时用，避免「推倒重来」破坏可用功能，也避免「只换皮」掩盖结构问题。
顺序固定：先判定 → 先审计 → 守住该守的 → 拉动可改的 → 决策改造 vs 重做。

## 第 0 步：detect — preserve vs overhaul

先读现有代码（别凭截图臆断），判断这是哪种任务：

- **PRESERVE 改造**：功能/信息架构/品牌基本对，问题在视觉陈旧或细节。→ 保留骨架，只动表层。
- **OVERHAUL 重做**：信息架构混乱、品牌过时、技术栈阻碍迭代，局部修无意义。→ 重建结构。

判定信号：用户原话（「现代化一下」=preserve；「重新设计」=overhaul）+ 代码健康度（组件可复用度、token 化程度、可访问性债务）。拿不准时默认 PRESERVE，向用户确认再升级。

## 第 1 步：audit — 沿 4 轴体检现有页

逐轴打分（差/中/好）并记录具体证据：

1. **Layout（结构构图）**：栅格是否一致、布局家族是否单调（全是 image+text split？）、留白节奏。
2. **Spacing（节奏/呼吸）**：间距是否成体系（4/8 基数）、密度是否匹配场景、是否拥挤或空洞。
3. **Hierarchy（视觉权重/阅读顺序）**：标题层级是否清晰、CTA 是否突出、眼动路径是否可控。
4. **Styling（色/字/表面处理）**：调色板是否怯懦（均匀分布无强调）、字体是否系统字/禁用字、阴影圆角是否一致。

## 第 2 步：preservation rules — 守住不能动的

- 已验证可用的**信息架构与导航结构**（用户已习惯的路径）。
- **真实品牌资产**：logo、品牌主色、注册字体（按 Core Asset Protocol 收集，写入 brand-spec.md）。
- 通过测试的**交互逻辑/表单流程/数据契约**。
- 现有**可访问性达标点**（别在美化时打碎键盘可达/对比度）。

## 第 3 步：modernisation levers — 可放心拉动的

- 调色板：怯懦均匀 → 「主色 + 锐利强调色」。
- 字体：系统字/Inter/禁用字 → display+body 配对池（见 fonts-and-colors.md）。
- 布局家族多样化：8 sections 至少 4 个 layout family（见 audit_checklist R3）。
- 间距重做成 4/8 体系；表面处理统一（圆角/阴影 token 化）。
- 错峰揭示动效（一次编排良好的载入 > 散落微交互），加 prefers-reduced-motion。
- 清除 AI-tell（见 ai_tell_lint.py：scroll cue / 编号 eyebrow / 版本页脚 / em-dash）。

## 第 4 步：改造 vs 重做决策树

```
现有信息架构合理？
├─ 否 → 组件复用度低 / token 化差？
│        ├─ 是 → OVERHAUL（重建结构 + 设计系统）
│        └─ 否 → 先重排 IA，再 PRESERVE 表层
└─ 是 → 视觉问题集中在 Styling/Spacing（轴 3-4）？
         ├─ 是 → PRESERVE：只拉 modernisation levers，骨架不动
         └─ 否（Layout/Hierarchy 也烂）→ 部分 OVERHAUL：
                  保 IA 与品牌，重做布局家族 + 层级
```

## 交付前

跑 `scripts/audit_checklist.py`（结构可数项）+ `scripts/ai_tell_lint.py`（AI-tell），二者全过再交付。
被守住的 preservation rules 逐条对照确认没被误伤。
