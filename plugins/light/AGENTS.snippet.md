<!-- LIGHT-SKILLS-START -->
## Light 科研技能包（路由说明）

当用户的请求涉及科研全流程时，调用 `~/.agents/skills/<skill-name>/SKILL.md` 下对应技能的 SKILL.md，按其指令执行。Light 安装器会把 28 个 `light-*` 技能逐个链接到 `~/.agents/skills/`，并把 `databases/` 与 `code_assets/` 作为同级共享资源链接过去。

### 科研主线（按阶段）
- 资料调研 → `light-literature-search`
- 数据评估/处理 → `light-data-engineering`
- 提创新点 → `light-idea-generation`；审创新点 → `light-idea-critique`（二者构成循环）
- 方案/技术路线 → `light-research-plan`
- 实验代码 → `light-backend-coding`；结果分析 → `light-result-analysis`
- 论文写作 → `light-paper-drafting`；润色 → `light-paper-polishing`
- 图表规划 → `light-figure-planning`；绘图/图表审查 → `light-figure-drawing`
- 引用整理 → `light-citation`；排版 → `light-typesetting`
- 投稿定位 → `light-venue-matching`；正式模拟审稿/返修/rebuttal → `light-review-rebuttal`

### 并行/按需
- 软著专利 → `light-ip-application`；PPT/deck QA → `light-slides`；竞赛申报 → `light-competition`
- 读文件/PDF/Word/PPT/Excel/图片/代码/压缩包 → `light-file-reading`
- 项目记忆与状态 → `light-memory-pm`
- 跨 ≥3 阶段 pipeline、断点恢复、接手 Claude/Hermes 上下文 → `light-orchestrator`
- 系统设计 → `light-system-design`；前端/可视化 → `light-frontend-design`；项目结构 → `light-project-structure`

### 全程常驻（每次输出前自检）
- 术语/指标/创新点跨材料一致 → `light-consistency`
- 输出前自审（逻辑/事实/格式/夸大/审美）→ `light-self-review`
- 选工具/选方法 → `light-tool-selection`
- 学术伦理与合规底线 → `light-research-ethics`

### 易混边界
- “继续 / 刚断了 / 接手 Claude”且语义指向断点恢复 → `light-memory-pm` + `light-orchestrator`，先读 git/todo/CI/最近提交再继续。
- “继续写 / 继续润色当前段落” → 单技能 `light-paper-drafting` / `light-paper-polishing`，不要启动 orchestrator。
- 图表规划归 `light-figure-planning`；实际绘图、配色、图表诚实性检查归 `light-figure-drawing`；整套 PPT/deck 视觉 QA 归 `light-slides`。
- paper-drafting 的草稿失败模式自检归 `light-paper-drafting`；正式模拟审稿与 rebuttal 归 `light-review-rebuttal`。

核心纪律：不臆造文献/数据/DOI/端点；区分「已验证」与「推测」；凡写入的 API 端点须实测；受版权材料只存元数据/链接/笔记。
<!-- LIGHT-SKILLS-END -->
