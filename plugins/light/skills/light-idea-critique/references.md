# light-idea-critique 参考工具研究笔记

本文件记录为升级"idea 严审"技能而实际查证过的工具/项目/API。每条含【是什么】【可复用方法】【链接】【已知坑/局限】。
凡标注"未能核实"者，表示未找到可靠公开信息，不应作为事实引用。

研究日期：2026-06-06。

---

## 1. NeurIPS / ICLR 公开评审表（评审维度与评分制的金标准）

【是什么】顶会官方审稿表，是本技能"多维评审"的权威锚点，应直接对齐而非自创维度。

【可复用方法 — NeurIPS 2024 评审表真实字段】
- 文字维度（逐条写）：Summary（复述论文与贡献，作者应认可这份摘要）/ Strengths & Weaknesses / Questions（作者回应能改变你判断的问题）/ Limitations（含负面社会影响）/ Ethical Concerns。
- Strengths & Weaknesses 拆 4 个子维度：**Originality（新颖性/与前作区分）、Quality（技术可靠性/论据完整）、Clarity（写作与可复现）、Significance（重要性与可被后续工作建立）**。
- 三个 1–4 分项：**Soundness / Presentation / Contribution**（4 excellent, 3 good, 2 fair, 1 poor）。
- **Overall 1–10**：10 award quality；9 very strong accept；8 strong accept；7 accept（technically solid, high impact）；6 weak accept；5 borderline accept；4 borderline reject；3 reject（technical flaws/weak eval）；2 strong reject；1 very strong reject（trivial）。
- **Confidence 1–5**：5 绝对确定/核对过数学；4 自信但非绝对；3 较自信但可能没看懂某些部分；2 愿意辩护但很可能没看懂；1 educated guess/非本领域。

【可复用方法 — 公开 review 的行文结构】NeurIPS proceedings 的 Review.html 显示真实审稿固定结构：`Summary and Contributions` → `Strengths` → `Weaknesses`（最长、最具体，常逐点 + 反例 + 替代解释）→ `Clarity` → `Relation to Prior Work` → 评分 → rebuttal 后 `UPDATE/Post-rebuttal` 是否改分。可借鉴：弱点要"指到节、给反例、提替代假设"，而非泛泛而谈。

【链接】
- NeurIPS 2024 Reviewer Guidelines: https://neurips.cc/Conferences/2024/ReviewerGuidelines
- 公开 review 样例: https://proceedings.neurips.cc/paper_files/paper/2020/file/0cbc5671ae26f67871cb914d81ef8fc1-Review.html
- OpenReview 上 ICLR 全量公开 review（见第 8 条 API）

【已知坑】Overall 与 Soundness 量纲不同（10 分 vs 4 分），混用会失真；Confidence 低时不应给极端分。ICLR 历年评分项有差异（早年用 1–10 rating + confidence，近年加 soundness/presentation/contribution），引用时注明年份。

---

## 2. OpenReview API（拉取顶会真实 review，做"对照锚定"与新颖性核查）

【是什么】ICLR/部分 NeurIPS/ARR 的公开评审平台，可程序化获取每篇投稿的全部 review、rebuttal、meta-review、decision。用于把"我这个 idea 像不像已发表/被拒的工作""真实审稿人会怎么挑刺"落到实证。

【可复用方法 — 真实端点/客户端】
- 两套 API：**API 2（默认/当前）base URL `https://api2.openreview.net`**；legacy **API 1 base URL `https://api.openreview.net`**（多用于 2024 前的会议）。两者 JSON 格式不同，注意区分。
- Python 客户端：`pip install openreview-py`，`openreview.api.OpenReviewClient(baseurl='https://api2.openreview.net', username=..., password=...)`（v1 用 `openreview.Client`）。
- 拉全量 note（投稿/review/rebuttal 都是 note）：`client.get_all_notes(invitation=f'{venue_id}/-/{submission_name}')`，按 `content={'venueid': venue_id}` 过滤；加 `details='replies'` 一并取回每篇投稿下的 review/comment 回复树。
- REST 直查：GET `/notes` 端点，参数含 `invitation`、`content.*`、`offset`、`limit`、`sort`；登录拿 token 后放 Authorization 头。
- 典型 invitation 形如 `ICLR.cc/2024/Conference/-/Submission`，review 的 invitation 形如 `.../-/Official_Review`。

【链接】
- Using the API: https://docs.openreview.net/getting-started/using-the-api
- 取全部 notes 指南: https://docs.openreview.net/how-to-guides/data-retrieval-and-modification/how-to-get-all-notes-for-submissions-reviews-rebuttals-etc
- Python 客户端文档: https://openreview-py.readthedocs.io/en/latest/api.html

【已知坑】venue_id 与 invitation 命名每年/每会都不同，要先查该会的 group；`get_notes` 默认分页（offset/limit），大批量要循环翻页或直接用 `get_all_notes`；只有已 release 的评审才可匿名拉取，bidding/未公开会议拿不到。

---

## 3. Semantic Scholar Academic Graph API（"最像的 3 篇"对照检索）

【是什么】学术图谱检索 API，本技能"给出最像的 3 篇做对照""相对最接近的工作 delta 多大"必须靠它/同类（OpenAlex/arXiv）落地，而非凭记忆断言新颖性。

【可复用方法 — 真实端点】
- base：`https://api.semanticscholar.org`
- 相关性检索：GET `https://api.semanticscholar.org/graph/v1/paper/search`，参数 `query`(必填)、`fields`(逗号分隔，如 `title,abstract,year,citationCount,authors`)、`limit`、`offset`。
- 批量检索（多数场景推荐，更省资源）：GET `https://api.semanticscholar.org/graph/v1/paper/search/bulk`，支持 `query`（含 `+ - * ~` 与短语操作符）、`fields`、`sort`(paperId/publicationDate/citationCount)、`year`(如 `2023-`)、`minCitationCount`、`venue`、`fieldsOfStudy`、`openAccessPdf`；**分页用返回的 `token` 续传，无 offset/limit**。
- 认证：请求头 `x-api-key: <key>`。

【链接】
- API 文档: https://api.semanticscholar.org/api-docs/graph
- 教程: https://www.semanticscholar.org/product/api/tutorial

【已知坑】无 key 时与所有匿名用户共享限流，极易 429；有 key 也仅 ~1 req/s（across all endpoints），需排队/退避。relevance search 比 bulk 更吃资源，常规用 bulk。新颖性判断不能只靠一个库，建议与 OpenAlex/arXiv 交叉验证（覆盖与字段不同）。

---

## 4. ResearchAgent + ReviewingAgents（多审稿 agent 迭代精修 idea 的范式）

【是什么】Microsoft Research / 论文（NAACL 2025）提出的系统：从一篇核心论文出发，沿学术图谱与跨论文挖掘的"实体知识库"扩展，自动产出问题/方法/实验，再由**多个 LLM ReviewingAgents** 给 review 并迭代修订。本技能"对抗式多视角自检 + 回到 m03 循环"的直接理论来源。

【可复用方法】
- 评审 agent 的评判标准不是拍脑袋，而是**从真实人类评审中用 LLM prompting 反推/对齐（human-preference-aligned criteria）**——对应本技能应把维度锚到 NeurIPS/ICLR 表（第 1 条）。
- 工作流：生成 idea → 多审稿 agent 各自挑刺 → 汇总反馈 → 修订 → 再评，循环。论文用的评判信号是 idea 的 **novelty / clarity / validity** 三性 + 人评。
- 可借鉴：审稿 agent 之间要"非重叠视角"，并用迭代 revision 而非一次性否决。

【链接】
- arXiv: https://arxiv.org/abs/2404.07738
- MSR 页面: https://www.microsoft.com/en-us/research/publication/researchagent-iterative-research-idea-generation-over-scientific-literature-with-large-language-models/

【已知坑】LLM 评审存在"对齐到平均人评"的回归效应，倾向打安全的中间分；novelty 判断依赖检索覆盖面，库不全则高估新颖性。

---

## 5. The AI Scientist（Sakana）自动评审器（近人类水平的 LLM reviewer）

【是什么】端到端自动科研 pipeline（idea→实验→写作→评审），其中**自动评审器**按顶会标准给 review/打分并反哺下一轮 ideation。idea 生成后先做"novelty 评估"再实现，与本技能"先严审再放行 m05"同构。

【可复用方法】
- pipeline 顺序值得照搬到科研流：brainstorm ideas → **evaluate novelty** → 实现 → 跑实验 → 写报告 → **automated review** → 用 review 反馈改进下一代。
- 评审器对齐"top ML conference standards"（即 NeurIPS 式 rubric），输出可作为是否超过"接收阈值"的判据；论文报告其评审达"near-human accuracy"，最好成果被自家评审判为约"Weak Accept"。
- 可借鉴：把"创新性筛查"作为独立前置闸门，不通过就不进实现阶段——正是本技能的强制衔接逻辑。

【链接】
- arXiv: https://arxiv.org/abs/2408.06292
- 项目页: https://sakana.ai/ai-scientist/
- 代码: https://github.com/SakanaAI/AI-Scientist ; v2: https://github.com/SakanaAI/AI-Scientist-v2

【已知坑】作者明示风险：自动评审若线上滥用会拉低评审质量并引入偏见；AI 生成的论文/评审应显式标注。评审"近人类"不等于可靠，对边缘分尤其不稳。具体 prompting 细节（few-shot/self-reflection/ensembling 的确切配置与 F1）未在摘要核实到，需查全文，此处不下断言（未能核实具体数值）。

---

## 6. CycleResearcher / CycleReviewer（开源模型模拟评审，ICLR 2025）

【是什么】开源后训练 LLM 跑完整"科研+评审"闭环：CycleResearcher 做研究，CycleReviewer 模拟同行评审并以 RL 给迭代反馈；配套数据集 Review-5k / Research-14k。

【可复用方法】
- 证据点：CycleReviewer 预测论文分数的 MAE 比单个人类审稿人低 26.89%——说明"结构化 LLM 评审做相对排序/打分"是可行的辅助，但定位是 assist，不是替代。
- 可借鉴：用"模拟评审分数"做 idea/草稿的相对体检与迭代目标值。

【链接】arXiv: https://arxiv.org/abs/2411.00816

【已知坑】生成论文的模拟评分（5.36）仍低于已接收论文（5.69），说明"过自家评审"≠"过真实会议"；分数是相对信号，别当绝对真理。

---

## 7. academic-paper-reviewer（imbad0202，5 角色多视角评审 skill）★最直接可借鉴

【是什么】一个成熟的 Claude skill：自动识别论文领域，动态配置 **5 名审稿人（Editor-in-Chief + 3 名 peer reviewer + Devil's Advocate）**，从"方法 / 领域 / 跨学科 / 核心论点挑战"四个**互不重叠**视角评审，产出结构化 Editorial Decision + Revision Roadmap。

【可复用方法 — 角色分工与"先盲后明"协议】
- 模式：full / re-review（核查修订是否回应了意见）/ quick / methodology-focus / guided（苏格拉底式带教）/ calibration（先测自身 FNR/FPR 再信其打分）。
- **Devil's Advocate 协议**（值得照搬）：它**不打分，只挑刺**——专找最脆弱点、最大逻辑缺口、最强反论。它判定的 CRITICAL 四类：
  1. Foundation Collapse：核心假设可证伪或无据。
  2. Logic Chain Break：即便证据有效，主结论也不从证据推出（例：只有相关性却宣称因果，未控混杂 A/B/C）。
  3. Evidence Gaps：核心论点仅靠 N<50 的单实验室 2 项研究。
  4. Stronger Counter-Narrative：替代解释更简洁且更契合数据。
- **Sprint Contract 协议**：Phase 1 在"看正文之前"先用自己的话复述每个验收维度并预先承诺 failure_conditions；Phase 2 才看正文写 Review Body 与 Decision，按 failure_conditions 的 severity 取最高者定档。可借鉴：先立标准再看内容，避免被论文叙事带跑。

【链接】https://github.com/imbad0202/academic-research-skills （目录 `academic-paper-reviewer/`，含各 agent 的 md 与 references）

【已知坑】5 个 persona 易输出冗长、彼此重复；calibration 需额外一轮才知其误报率；"动态领域识别"对小众交叉领域可能配错专家。

---

## 8. peer-review / scientific-critical-thinking / scholar-evaluation（K-Dense 科研 skill 三件套）

【是什么】三个分工明确的评估 skill，可作本技能不同子任务的方法论模板：
- **peer-review**：写正式审稿意见，按 checklist 评 methodology/statistics/design/reproducibility/ethics，并核对报告规范 **CONSORT / STROBE / PRISMA**。
- **scientific-critical-thinking**：评"证据质量"，用 **GRADE** 与 **Cochrane Risk of Bias** 框架识别 bias / confounding、判断设计能否支撑因果主张（performance/detection/selection bias）。
- **scholar-evaluation**：用 **ScholarEval** 框架做"量化打分"，维度含 problem formulation / methodology / analysis / writing，每维 5 点量表给分 + 可执行反馈。

【可复用方法】路由原则很清晰且可照搬：**判证据质量→critical-thinking；要量化分→scholar-evaluation；写正式 review→peer-review**。本技能"逐条 1–5 打分 + 理由"对应 scholar-evaluation 的 5 点量表；"数据/实验可控性"对应 critical-thinking 的混杂/选择偏倚清单；"是否够发表"对应 peer-review 的报告规范核对。

【链接】
- 三件套（agent-studio 镜像）：https://github.com/oimiragieo/agent-studio （路径 `.claude/skills/scientific-skills/skills/{peer-review, scientific-critical-thinking, scholar-evaluation}`）
- scientific-critical-thinking 介绍页：https://www.claudepluginhub.com/skills/ckorhonen-claude-skills/scientific-critical-thinking

【已知坑】CONSORT/STROBE/PRISMA 偏生医/临床，纯方法或理论 ML idea 未必适用，要按领域取舍；GRADE/Cochrane 同理偏循证医学。ScholarEval 的分数需配理由，否则只是数字。

---

## 9. Consciousness Council（多原型对抗式议事，强制"会冲突"的视角）

【是什么】多视角"心智议会" skill：不给一个声音，而是召集 4–6 个**思维原型**让其观点**真正相撞**，再综合成可执行结论。本技能"方法/实验/理论/应用四视角独立挑刺"的升级蓝本。

【可复用方法 — 12 原型与选人启发式】
- 原型各有"提问/盲点"：Architect（结构优先/会过度工程）、Contrarian（反过来想/为反而反）、Empiricist（数据优先/忽略不可测）、Ethicist、Futurist、Pragmatist、Historian（先例/打上一场仗）、Empath、Outsider（跨域天真提问）、Strategist（二三阶博弈）、Minimalist（能删什么）、Creator（还没试过什么）。
- **选人启发式**：技术架构类→Architect+Minimalist+Empiricist+Outsider；策略竞争类→Strategist+Historian+Futurist+Contrarian+Pragmatist。核心原则：**选会产生"建设性冲突"的成员，一致没价值，张力才有价值**。
- 三阶段：Summon（选人）→ Deliberation（每人输出 Position / Reasoning / Key Risk They See / Surprising Insight）→ Synthesis。

【链接】https://github.com/k-dense-ai/scientific-agent-skills （路径 `skills/consciousness-council/`）；上游 https://github.com/ashrafkahoush-ux/claude-consciousness-skills

【已知坑】纯角色扮演会流于表演；必须让视角真冲突且各自给"别人会漏掉的风险"，否则退化成换皮的同一意见。原型选错（全是互相同意的）就失去价值。

---

## 10. What-If Oracle（反事实/可能性空间压力测试）

【是什么】结构化"What-If"情景分析 skill：不给单一预测，而是 4–6 条分支（best / likely / worst / wild card / contrarian / second-order）映射可能性空间。可给本技能加"如果这个 idea 的关键假设不成立会怎样"的压力测试维度。

【可复用方法】
- 核心 `0·IF·1`：0=未发生的潜在态，1=当前现实，IF=触发变化的条件；**分析质量取决于 IF 的精确度**——"如果出问题"→垃圾结论；"如果主供应商 Q3 涨价 30%"→可执行。
- Frame 阶段把问题拆成：Variable（变什么，一次一个变量）/ Magnitude（变多少，量化）/ Timeframe / Context。
- 用于 idea：把"创新点不成立/数据拿不到/baseline 也能达到同效果"作为精确 IF，逐分支推二阶后果。

【链接】https://github.com/k-dense-ai/scientific-agent-skills （路径 `skills/what-if-oracle/`）

【已知坑】一次只能干净地变一个变量，多变量耦合会混乱；分支概率多为主观估计，别当真实概率；其 DOI/"数字意识理论"思辨成分较重，方法论可用、理论叙事谨慎引用。

---

## 11. grill-me / grill-with-docs（mattpocock，逐题逼问式压力测试）

【是什么】两个广为流传的 skill：不写文档，而是**像审稿人一样把一个 plan/design 往死里盘问**，沿决策树一支一支走到双方达成共识。

【可复用方法 — 盘问纪律】
- **一次只问一个问题，问完等回答再继续**（grill-me 原文："Ask the questions one at a time"）；每个问题**自带你推荐的答案**，而不是空抛问题。
- 能从代码/材料里查到答案的，就去查，不要问。
- grill-with-docs 额外四招（可移植到 idea 审）：
  1. **Challenge against the glossary**：用词与既有定义冲突立刻点破（"你术语表里 cancellation 指 X，你现在像在说 Y，到底哪个？"）。
  2. **Sharpen fuzzy language**：模糊/重载词逼其给精确规范术语。
  3. **Discuss concrete scenarios**：用具体边界场景压力测试概念间关系。
  4. **Cross-reference with code**：声称的行为与代码/数据对不上就当场指出矛盾。

【链接】
- grill-me: https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md
- grill-with-docs: https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md

【已知坑】逐题逼问适合"交互式打磨"，本技能多为一次性出审稿意见，借鉴其"自带推荐答案 + 用具体场景而非泛问"的纪律即可；连环追问过长会拖垮节奏。

---

## 12. verification-before-completion（obra/superpowers，"先验证再下结论"铁律）

【是什么】一条防止"未验证就宣称完成"的 skill。本技能的纪律基石：**判决与打分必须有证据，不能凭感觉说"应该挺新的/数据应该够"**。

【可复用方法 — Gate Function】
- 铁律：`NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE`——这条消息里没跑过验证命令，就不能宣称通过。
- 闸门 5 步：IDENTIFY（什么证据能证明此断言）→ RUN（真的去跑/查）→ READ（读全输出）→ VERIFY（输出是否支持断言）→ ONLY THEN 才下断言。
- 红旗词：用了 "should / probably / seems to"，或在验证前就说 "Great/Perfect/Done"。
- 映射到 idea 审：宣称"新颖"前必须真检索（第 2、3 条 API）；宣称"数据够"前要核数据规模/标注；宣称"实验可控"前要能写出干净对照与消融。

【链接】https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md

【已知坑】科研新颖性无法 100% 证否（检索覆盖有限），可达到的是"已尽力检索且列出最像的工作"，应如实标注 confidence 而非假装确定。

---

## 13. 多 LLM 评审 + 去标识 meta-review pipeline（poldrack/ai-peer-review）

【是什么】一个真实的"多模型评审 + 元评审"工程实现，可作"多视角不是同一模型自演"的落地方案。

【可复用方法 — 具体流程与提示词】
1. 摄入 PDF，分发给多个 LLM（仓库示例用 o1、o3-mini、Claude Sonnet 3.7、Gemini 2.5 Pro、DeepSeek R1、Llama 4 Maverick），统一提示：扮演领域专家审稿人，先复述研究与结果，再逐点剖析所有缺陷。
2. **去标识**：把每份 review 的模型来源抹掉，再喂给元评审模型，避免来源偏见。
3. 元评审提示：总结各审稿的**共识点**与**仅个别提出的关切**，并按"有用性/抓到关键问题的能力"给 review 排序。
4. 各 review 与 meta-review/评分存成 JSON。

【链接】https://github.com/poldrack/ai-peer-review （见 `CLAUDE.md`、`putiken/` 真实样例）

【已知坑】单 agent 模拟多视角时，仍是同一模型的相关性输出（伪多样性）；本技能在单模型内运行，可用"先盲承诺标准 + 互不重叠视角 + 去标识汇总"近似，但要承认其多样性弱于真·多模型。

---

## 关于其余命名项的核实说明

- "critique skill / audit skill"：未找到单一权威同名 skill；可对照的实物是 obra/superpowers 的 `brainstorming`（idea→design，一次一问、强制产出可评审的 design）与 qdhenry/Claude-Command-Suite 的 `security-audit`/`architecture-review` 等命令（结构化审计模板）。链接：https://github.com/obra/superpowers 、https://github.com/qdhenry/Claude-Command-Suite 。其"逐项 checklist + 给证据 + 给修复方向"的范式可借鉴，但"critique/audit"作为确切技能名**未能核实为单一来源**。
- "Scholar Evaluation"：即第 8 条的 scholar-evaluation（ScholarEval 框架），已核实。
- "Peer Review skill / Scientific Critical Thinking"：即第 8 条三件套，已核实。


