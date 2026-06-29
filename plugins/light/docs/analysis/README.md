# Light 28 技能横向分析总览

> 分析日期 2026-06-13 ｜ 方法：每技能用 Explore agent 读真实 SKILL.md + references/scripts 做深度逻辑与优缺点分析，再逐技能联网检索 GitHub 同类前沿技能（主查 GitHub，star/更新时间经 API 实测）。逐技能详档见 [`docs/analysis/skills/`](skills/)。
>
> 本轮统计：28 技能合计 **178 条优点 · 202 条缺点 · 214 条可优化点**；GitHub 同类对标合计 **约 290 个真实项目**（含 3 个因 workflow socket 断连后单独补检索的技能：figure-planning / venue-matching / slides）。

---

## 一、Light 在 GitHub 生态中的整体定位

把 28 技能的同类检索结果横向拼起来，Light 的竞争格局清晰分成三档：

**1. 有强势同类、Light 靠"科研严谨 + 中文链路 + 可复现脚手架"差异化的技能**
- 通用 agent skill 合集：`anthropics/skills`(15万★)、`obra/superpowers`、`K-Dense-AI/scientific-agent-skills`(2.8万★)、`VoltAgent/awesome-agent-skills` —— 它们覆盖广、生态大，但**无固定科研主线闭环、无自有可溯源知识库、无诚实红线写进正文**。Light 的 backend-coding / self-review / orchestrator / tool-selection 直接对标 superpowers 这类"工程纪律"技能，差异在科研垂直化。
- 自动科研框架：`SakanaAI/AI-Scientist`(1.4万★)、`HKUDS/AI-Researcher`、`AgentLaboratory` —— 强在"端到端自动生成"，但 reviewer 是产物评分器而非 idea 阶段硬闸门，易内容失真。Light 的 idea-critique / review-rebuttal 是"协议化严审闸门"，不是生成引擎。

**2. 有成熟垂直工具、Light 靠"整合进主线 + 中文 + 诚实"补位的技能**
- 文献检索：`K-Dense`、`gpt-researcher`(2.7万★)、`local-deep-researcher` —— 自主性强但学术源口径松散、易臆造引用。
- 文档解析：`microsoft/markitdown`(高★) —— Light file-reading 实质是 markitdown 等工具的"理解层"封装。
- 记忆：`mem0ai/mem0`(高★) —— 通用记忆框架，Light memory-pm 是科研项目专用 + 跨会话衔接协议。
- 润色/一致性：`languagetool-org/languagetool` —— Light polish/consistency 在其上加学术语域与跨材料一致。
- 排版：ARIS `paper-compile`、cookiecutter-data-science、full-stack-fastapi-template —— 各自垂直成熟，Light 的优势是串进主线。

**3. GitHub 上几乎空白、Light 是差异化先发的技能**
- `figure-planning`：按 claim 规划全文图表 + 双向卡 + 幽灵 deck 完整性检查——补检索确认**该精确赛道 GitHub 空白**，同类要么是执行层(出图)要么是数据驱动图型推荐(Draco/Voyager)。
- `venue-matching`：把论文实力+作者背景+预算映射成冲/稳/保分层 + 录用可能性定性分级(拒用 LetPub 百分比)——同类多是纯主题匹配的"期刊推荐器"，决策层空白。
- `consistency` / `self-review` / `research-ethics` 作为**常驻横切技能**：通用生态有零散工具，但"写进规约、全任务后台生效"的形态少见。

> 一句话：Light 的护城河**不在单点技能强度**（很多单点都有更强的垂直对手），而在**科研主线闭环 + 9 个可溯源知识库 + 诚实红线写进正文 + 中英双语 + 跨会话衔接**的组合，以及 figure-planning / venue-matching 等决策规划层的先发。

---

## 二、跨技能的共性优点（28 技能反复出现的强项）

1. **诚实红线真正落到代码与协议，不是口号**：几乎每个带脚本的技能都有 `--selftest` + `[OFFLINE]` 合成回退 + 打印真实 HTTP 码；literature-search 的幻觉引用检测、idea-critique 的反谄媚 concession-rate、research-ethics 的撤稿核查都是**可执行**的诚实机制。这是相对所有 GitHub 同类最稳的差异点。
2. **references.md 把易变信息单点沉淀**：端点/限流/计费/坑写在 references，SKILL.md 做策略层，版本治理意识强（如 OpenAlex 2026 计费设"全仓库唯一口径"）。
3. **behavioral anchor 式评分而非空泛形容词**：idea-critique 八维、self-review、review-rebuttal 的评分都写"打到这档要看到什么证据形态"，可据此反查。
4. **工件契约化交接**：CONVENTIONS §6.1 的阶段工件命名让技能间不靠聊天总结交接，orchestrator 可调度。
5. **对抗式自检内建**：idea-critique 的 Devil's Advocate、self-review 的独立挑刺、review-rebuttal 的模拟审稿，把"自己挑自己毛病"做成流程。
6. **中文链路务实**：不假装有知网 API，改走 OpenAlex/Crossref 按 ISSN 命中中文期刊，GB/T 7714 著录到位。

---

## 三、跨技能的共性缺点（反复出现的系统性问题，按优先级）

这是后续逐技能优化最该先啃的——多个技能犯同一类问题，说明是**设计层的系统性短板**，不是个别疏漏：

1. **文档承诺 > 可运行能力（覆盖面虚胖）**：最普遍的问题。literature-search 宣称 10+ 类源但有脚本的只有 OpenAlex+Crossref 2 源；多个技能的 references 把"可借鉴工具"写得很全，但落地脚本只覆盖一小部分。审稿人/资深用户一眼能看出"宣称的多源/多功能在代码里不存在"。
2. **联网依赖无离线降级闭环**：idea-critique 的检索闸门、literature-search、citation、venue-matching 都重度依赖网络，但多数没写"无网时核心闸门怎么办"——只说"封顶/标 unavailable"，没说封顶后还能不能放行，核心机制可能架空。
3. **关键阈值/权重硬编码且无依据**：idea-critique 的通过线 Weighted≥80、八维权重、verify_citations 的相似度 0.6 都是写死的魔数，缺敏感性分析或标注集反推依据，易被质疑"为什么是这个数"。
4. **API key / 礼貌池等工程细节不达标**：literature-search 的 MAILTO 硬编码成伪造邮箱、脚本无 `--api-key` 参数，与 references 自定的"按需 key"铁律自相矛盾，一旦匿名通道关闭即失效。
5. **单模型扮演多视角 = 伪多样性**：idea-critique 五视角、review-rebuttal 多审稿人都靠同一模型角色扮演，references 自认多样性弱于真·多模型，但无结构化约束逼出真冲突。
6. **领域适配单一（ML 口味重）**：idea-critique、figure-drawing、result-analysis 的 anchor 明显偏机器学习(backbone/消融/baseline)，对理论、数学、systems、HCI、定性、人文社科类研究不适配，但都宣称"通用"。
7. **批量/多对象工作流缺失**：idea-critique 消费多卡 idea_candidates 却只逐卡评、不排序；多个技能面对"一批对象"时没有批量比较模式。
8. **常驻技能的"自动生效"难验证**：consistency/self-review/tool-selection 等常驻技能靠模型自觉触发，没有可机检的"确实生效了"证据。

---

## 四、优化优先级建议（带着做后续逐技能优化时的顺序）

按"影响面 × 可信度损伤 × 修复成本"排，建议分三批：

**P0（先修，影响诚实可信与名实相符）**
- 补齐"文档承诺 vs 可运行能力"的差距：要么把 references 里宣称的源/功能补成可运行脚本（如 literature-search 补 arxiv/pubmed/europepmc fetch），要么把 SKILL/README 的措辞降到与代码一致。这直接关系产品诚实底线。
- 修 API key / MAILTO：给联网脚本加 `--api-key`/环境变量读取，MAILTO 改运行时必填，兑现自定铁律。
- 给所有联网闸门写离线降级协议：明确无网时的状态机（能否放行、要不要二次检索）。

**P1（提质量，影响判决可靠性）**
- 硬编码阈值改为标注集反推或显式声明为可调超参 + 给依据（idea-critique 通过线、权重敏感性分析）。
- 领域 profile 切换：给 idea-critique / figure-drawing / result-analysis 加 ML / 理论 / 生医 / HCI-定性 等领域档，替换证据形态 anchor。
- 结构化多样性：把多视角从"自律"升级为可机检（各视角引不同前作、锚不同维度、去重检查）。

**P2（补能力，影响完整性与体验）**
- 批量/排序工作流：idea-critique 摄入全部候选卡统一打分排序输出 top-k。
- 接真实检索后端做事实锚定（venue-matching 接 OpenAlex/DOAJ、figure-planning 规划卡可喂给执行层 MCP）。
- 借鉴同类的工程化亮点：PPTAgent 的 PPTEval 可量化 QA、OpenNovelty 的检索证否 pipeline、Draco 的形式化图型推荐。

> 详细每技能的 `improvement_ideas` 见各自详档，本表只提炼跨技能共性优先级。

---

## 五、28 技能详档索引

> 每份含：核心逻辑 / 关键步骤 / 自带资产 / 优点 / 缺点 / 可优化点 / 衔接 / GitHub 同类对标表。

### 手动技能（按科研主线）
- [light-literature-search](skills/light-literature-search.md) — 多源检索去重判级 PRISMA 留痕
- [light-data-engineering](skills/light-data-engineering.md) — 数据体检/防泄漏划分/质量门
- [light-idea-generation](skills/light-idea-generation.md) ⇄ [light-idea-critique](skills/light-idea-critique.md) — 提 idea / 严审闸门
- [light-research-plan](skills/light-research-plan.md) — 技术路线与实验矩阵
- [light-result-analysis](skills/light-result-analysis.md) — 显著性检验/效应量/出图
- [light-paper-drafting](skills/light-paper-drafting.md) ⇄ [light-paper-polishing](skills/light-paper-polishing.md) — 成稿 / 润色
- [light-figure-planning](skills/light-figure-planning.md) ⇄ [light-figure-drawing](skills/light-figure-drawing.md) — 图表规划 / 出版级绘图
- [light-citation](skills/light-citation.md) · [light-typesetting](skills/light-typesetting.md) — 引用核验 / LaTeX·Word 排版
- [light-venue-matching](skills/light-venue-matching.md) · [light-review-rebuttal](skills/light-review-rebuttal.md) — 投稿定位 / 审稿返修
- [light-ip-application](skills/light-ip-application.md) · [light-slides](skills/light-slides.md) · [light-competition](skills/light-competition.md) — 软著专利 / PPT / 竞赛

### 常驻技能（后台自动）
- [light-file-reading](skills/light-file-reading.md) · [light-memory-pm](skills/light-memory-pm.md) · [light-orchestrator](skills/light-orchestrator.md)
- [light-backend-coding](skills/light-backend-coding.md) · [light-system-design](skills/light-system-design.md) · [light-frontend-design](skills/light-frontend-design.md)
- [light-project-structure](skills/light-project-structure.md) · [light-consistency](skills/light-consistency.md) · [light-self-review](skills/light-self-review.md)
- [light-tool-selection](skills/light-tool-selection.md) · [light-research-ethics](skills/light-research-ethics.md)

---

## 六、下一步

用户将带着这批分析**逐技能优化**。每份详档的「可优化点」是该技能优化的直接输入；本总览第四节的 P0/P1/P2 是跨技能的优化顺序建议。建议从 P0（诚实名实相符）开始，因为它最伤产品核心卖点。

> **数据库专题分析**见 [`databases.md`](databases.md)：9 个库按"A-通用判断/B-易变事实/C-项目状态"归类，回答"本地库会不会过时/偏科/该不该砍"——结论是 db01/db04 主体转实时，db02/05/06/07/08 主体留为方法论资产，db03 拆开处置，db09 必须本地。与逐技能优化交叉，建议**先定库架构再优化依赖库的技能**。
