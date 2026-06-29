# Pipeline 链路定义

每条 pipeline 是一串阶段。每阶段 = 调用技能 + 输入 + 产出 + 检查点。检查点类型见 [checkpoints.md](checkpoints.md)。链路按需裁剪——不是每个任务都跑全程。

## 链路 A：从数据/想法到一篇论文（最常用）

| # | 阶段 | 技能 | 产出 | 阶段末检查点 |
|---|------|------|------|--------------|
| 1 | 调研 | m01 literature-search | 文献清单 + 方向与 gap | ✓ 确认：来源可核 |
| 2 | 数据评估 | m02 data-engineering | 数据卡 + 防泄漏划分 | ✓ 确认：无泄漏、划分合理 |
| 3 | 提 idea | m03 idea-generation | 候选 idea | 🧑 决策：选哪个方向 |
| 4 | 审 idea | m04 idea-critique | 八维打分 + 判决 | 🧑 决策：不过关→回 3；放行→进 5 |
| 5 | 方案 | m05 research-plan | 实验矩阵 + 可复现方案 | ✓ 确认：方案可执行 |
| 6 | 实验 | a03 backend-coding | 代码 + 原始结果 | ✓ 确认：无数据泄漏、结果可复现 |
| 7 | 结果分析 | m06 result-analysis | 显著性检验 + 洞察 | ✓ 确认：统计正确、不过度解读 |
| 8 | 写作 | m07 paper-drafting | 初稿 + GAP 台账 | ✓ 确认：**诚信门**（claim/引用核查）|
| 9 | 润色 | m08 paper-polishing | 润色稿 | ✓ 确认：表达 + 论证 |
| 10 ∥ | 图表 | m09 → m11 | 出版级图 | ✓ 确认：图文一致 |
| 11 ∥ | 引用 | m10 citation | 核验过的引文 | ✓ 确认：**每条引用真支撑该句** |
| 12 | 排版 | m12 typesetting | 编译通过的 PDF | ✓ 确认：编译零错误 |

第 8、11 步是**强诚信闸门**，不达标默认阻断。

**∥ 可并行段**：第 10（图表 m09→m11）与第 11（引用 m10）互不依赖——图表消费 m06 结果、引用消费正文 claim，无交叉输入，可同时推进，到第 12 排版前汇合（排版要同时吃图和引文）。两者各自的诚信闸门独立判定。串行环境按 10→11 顺序即可，不必空等。

## 链路 B：投稿与返修

| # | 阶段 | 技能 | 产出 | 检查点 |
|---|------|------|------|--------|
| 1 | 投稿定位 | m13 venue-matching | venue 候选 + 录用分级 | 🧑 决策：投哪个 |
| 2 | 模拟审稿 | m14 review-rebuttal 模式一 | 预审报告 | ✓ 确认：先改硬伤再投 |
| 3 | （投出，等结果）| — | — | 🧑 决策：收到意见后启动返修 |
| 4 | 返修 | m14 review-rebuttal 模式二 | response letter + 改稿 | ✓ 确认：逐条回应、不回避 |

## 链路 C：成果转化（按需并行，通常不卡重检查点）

- 软著/专利：m15 ip-application（🧑 决策：专利文本须代理人审核）
- 答辩/路演 PPT：m16 slides
- 竞赛申报：m17 competition（✓ 确认：AI 使用声明合规）

**∥ 可并行段**：论文定稿后，PPT（m16）与排版出 PDF（m12 链路 A 第 12 步）互不依赖——PPT 取结论与图、排版编译正文，可同时做（一人/一会话推 PPT，另一线程推排版）；三类成果转化（m15/m16/m17）本身也彼此独立，按用户需要并行或择一。

## 裁剪原则

- 用户已有数据 → 阶段 2 仍要做（数据卡/划分），但**调研（阶段 1）不能跳**：有数据不等于知道领域 gap，投稿仍需先看相关工作。只有用户明确"已做完调研、只差实验/写作"时才跳 1。
- 用户已有初稿要润色投稿 → 直接走 8→9→链路 B。
- 用户只要某一段 → 不启动 pipeline，单技能闭环。
- 缺哪个阶段的输入，就在该阶段前停下问用户，别凭空补。

## 阶段工件契约（CONVENTIONS §6.1 的执行视角镜像）

> 工件命名的单一真相源是 **CONVENTIONS §6.1**；下表为执行视角镜像，与 §6.1 不一致以后者为准。项目已有约定时以项目约定为准，但必须在 passport 记录路径。

| 阶段 | 上游输入 | 标准产物 / handoff artifact | 下游 |
|---|---|---|---|
| m01 调研 | 研究问题、关键词、目标领域 | `docs/literature_review.md` + evidence table（文献、claim、来源链接、可信度） | m03/m04/m07/m10 |
| m02 数据工程 | 数据文件/来源/任务定义 | `data_card.md` + `quality_report.md` + split/manifest | m05/a03/m06 |
| m03 idea 生成 | 调研 gap、数据约束、用户偏好 | `idea_candidates.md`（候选、机制、风险、验证方式） | m04 |
| m04 idea 审查 | 候选 idea | `critique_verdict.md` / scorecard / 是否回 m03 | m05 |
| m05 研究方案 | 放行 idea、数据卡、方法卡 | `PROJECT_PLAN.md` + `experiments/experiment_matrix.md` | a03/m06 |
| a03 实验代码 | 方案、数据、指标 | 可运行代码 + test/log + `run_manifest.md` | m06 |
| m06 结果分析 | 原始结果、实验矩阵 | `claim_evidence_table.md` + 统计检验报告 + 图表建议 | m07/m09 |
| m07/m08 写作润色 | claim/evidence、图表、引用 | `draft.md` / 修订稿 + GAP 台账 | m09/m10/m12 |
| m09/m11 图表 | claim/evidence、规划卡、source_card | `projects/<project_name>/figures/manifest.md` + 图文件 + checks | m07/m12 |
| m10 引用 | 草稿 citekey、候选文献 | `refs.bib` + `citation_audit.md`（真实性 + locator） | m12 |
| m12 排版 | 稿件、图、bib、模板 | 编译日志 + final PDF/DOCX | m13/m14/提交 |
| m14 返修 | 审稿意见、稿件、实验/图表 | `response_matrix.md` + response letter + 改稿 | m12/提交 |
| m15 软著专利 | 技术内容（m05/a03/m07） | `ip/disclosure_draft.md` + `ip/claims_draft.md` + `ip/specification_draft.md`（软著 `ip/copyright_package/`） | a08/提交 |
| m16 路演 PPT | 论文/项目内容、图表（m11） | `slides/`（源+导出）+ `slide_outline.md` | a08/现场 |
| m17 竞赛申报 | 技术内容、市场数据、图表 | `competition/`（申报书/BP/路演纲/答辩QA/预算表按需）+ `material_checklist.md` | a07/a08/m16/提交 |
