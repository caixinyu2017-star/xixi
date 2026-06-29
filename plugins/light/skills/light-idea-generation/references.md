# light-idea-generation 参考工具笔记

逐个研究的参考工具/项目/API 的硬信息。研究日期 2026-06。每条尽量给真实端点、参数、工作流步骤、评审维度与已知坑；查不到的如实标注"未能核实"。

---

## ResearchAgent (Baek et al., 2024, 论文)

**【是什么】** 微软/KAIST 提出的迭代式研究 idea 生成框架。从一篇核心论文出发，自动产出 Problem → Method → Experiment 三段式研究构想，再用多个 ReviewingAgent 反复打分修订。arXiv 2404.07738，ICLR 拒/讨论稿。

**【可复用方法】**
- **三阶段顺序生成**：先定义"问题"，再提"方法"，最后设计"实验"，每段用独立模板，模板里写明显式 desiderata（清晰/新颖/有效）。比一次性吐一个 idea 更结构化。
- **文献图 + 实体知识库双重增强**：(1) 对核心论文 l₀ 取引文子图邻居 {l₁…lₙ}，用引用边 + TF-IDF/SBERT 余弦相似度选相关文献；(2) 用实体抽取（如 BLINK）建共现矩阵 K_ij = #{同时出现实体 e_i,e_j 的论文数}，从子图实体并集里按联合似然挑"扩展概念实体"注入 prompt，制造跨域联想。本技能的 method-transfer / combination 角度可借此思路：先抽取项目领域核心实体，再找高共现的邻域实体作为迁移来源。
- **ReviewingAgent 五维评审**：多个人类偏好对齐的 LLM 评审，标准从真实人类判断中提炼。五个维度：**Clarity（清晰度）、Relevance（相关性）、Originality（原创性）、Feasibility（可行性）、Significance（重要性）**。评审反馈聚合后回灌给生成 agent 驱动多轮修订。→ 这 5 维可直接做 idea 自检清单。

**【链接】** https://arxiv.org/abs/2404.07738 ｜ https://www.microsoft.com/en-us/research/publication/researchagent-iterative-research-idea-generation-over-scientific-literature-with-large-language-models/

**【已知坑/局限】** 论文级评测显示"新颖但未必有效/可落地"；评审标准是 LLM 模拟人类，存在偏置。HTML 全文页是壳，正文细节需读 PDF。

---

## The AI Scientist v1 (Sakana AI, 2024)

**【是什么】** 首个端到端自动科研系统：idea 生成 → 新颖性检索 → 跑实验 → 写论文 → 自动评审。arXiv 2408.06292。其后续工作据称登 Nature（Lu et al.；**卷页 Nature 651:914-919 为待核条目，引用前须核验真实出处，勿当既成事实**）。基于固定"模板"（NanoGPT / 2D Diffusion / Grokking）在某领域内迭代。

**【可复用方法/真实端点】**
- **idea 三维自评分**：`generate_ideas.py` 让 LLM 对每个候选 idea 输出 JSON，含字段 `Name / Title / Experiment / Interestingness / Feasibility / Novelty`，后三者均为 **1–10 打分**，prompt 明确要求"打分谨慎、贴近现实"。→ 本技能可借用 Interestingness+Feasibility+Novelty 这套轻量三维快评。
- **迭代生成 + 反思**：先看已生成的 `prev_ideas`，再"想下一个有影响力且有创意的方向"，避免重复。
- **新颖性检索真实端点**：`search_for_papers(query, result_limit=10, engine="semanticscholar")`
  - Semantic Scholar：`GET https://api.semanticscholar.org/graph/v1/paper/search`，header `X-API-KEY`（可选），参数 `query`、`limit`、`fields`；返回后 `time.sleep(1.0)` 限流。
  - 无 S2 key 时改用 OpenAlex（`engine="openalex"`，`pip install pyalex`，设 `OPENALEX_MAIL_ADDRESS`）。
- **自动评审**：`perform_review()` 复刻 NeurIPS/ICLR 审稿，返回 dict：`review["Overall"]`（1–10）、`review["Decision"]`（Accept/Reject）、`review["Weaknesses"]`（列表）。可设 `num_reflections=5`、`num_reviews_ensemble=5`（多次集成）、`temperature=0.1`。

**【链接】** https://github.com/SakanaAI/AI-Scientist ｜ https://arxiv.org/abs/2408.06292 ｜ https://sakana.ai/ai-scientist/

**【已知坑/局限】** README 自己警告会执行 LLM 写的代码，需容器化隔离、限制网络。Semantic Scholar 易撞限流；模板内创新，跨领域泛化弱。

---

## The AI Scientist v2 (Sakana AI, 2025)

**【是什么】** v1 升级版，去掉人写模板，靠"实验管理 agent + 渐进式 agentic 树搜索"泛化到多 ML 领域。arXiv 2504.08066；号称首篇全 AI 写、过 workshop 盲审的论文。

**【可复用方法】**
- **ideation 与实验解耦**：先跑 `perform_ideation_temp_free.py` 单独做 ideation。输入是一份 Markdown 主题描述文件，含 `Title / Keywords / TL;DR / Abstract` 四节来界定范围；关键参数 `--max-num-generations`（生成几个 idea）、`--num-reflections`（每个 idea 精修几轮）。输出一个 JSON，含 hypotheses + proposed experiments + related work analysis 的结构化 idea 列表。→ 本技能可照搬"主题描述四件套（Title/Keywords/TL;DR/Abstract）"作为 idea 立项卡。
- **生成时实时查 Semantic Scholar 做新颖性核验**（ideation 与写作两阶段都用 S2_API_KEY）。
- **best-first tree search (BFTS)**：`bfts_config.yaml` 配 `num_workers`（并行探索路径数）、`steps`（最多展开节点数）、`num_drafts`（Stage 1 独立树/根节点数）。idea 阶段成本一般几美元；实验阶段用 Claude 3.5 Sonnet 约 \$15–\$20/次。
- **多根并行 = 多样性**：`num_drafts` 即"独立长几棵树"，对应本技能"从多个角度各自发散再收敛"。

**【链接】** https://github.com/sakanaai/ai-scientist-v2 ｜ https://arxiv.org/abs/2504.08066

**【已知坑/局限】** 成功率依赖底座模型与 idea 复杂度；弱模型常跑不出 PDF。仍依赖 S2 限流。

---

## AI-Researcher (HKUDS, NeurIPS 2025)

**【是什么】** 港大数据智能实验室的全自动科研 agent：文献综述 → idea 生成 → 算法设计与实现 → 验证与迭代调优 → 结果分析 → 论文撰写。生产版见 novix.science。

**【可复用方法】** 最值得借鉴的是它的**两级输入抽象**：
- **Level 1 详细 idea 描述**：用户已有明确想法，系统按显式需求做实现策略。
- **Level 2 参考文献驱动 ideation**：用户只丢几篇参考论文（"帮我基于这些论文想个创新点并实现"），系统分析参考文献自己生成新概念。
→ 对应本技能：当用户已有方向时走 Level 1（细化+可行性）；当用户只有"这个方向/数据能做什么"时走 Level 2（从文献+数据反推 idea）。仓库根目录 `research_agent/`、`paper_agent/` 两个模块分别管研究与写作。

**【链接】** https://github.com/HKUDS/AI-Researcher

**【已知坑/局限】** 强调"全自动"，但全自动流水线继承一切幻觉/捷径风险（见 ARS 条目的 7 失败模式）；README 偏宣传，工作流细节需读代码。

---

## MAGenIdeas / 迭代规划检索 (Chen et al., ISSI 2025)

**【是什么】** "组合创新 + 多智能体迭代检索"提升 LLM 研究 idea 的新颖性与多样性。对应：原始方法 arXiv 2410.14255（Iterative Planning and Search）。**其扩展版（曾记 arXiv 2604.20548 / Scientometrics）编号与出处为待核条目，未核实前勿当既成事实引用。** 代码仓 `ChenShuai00/MAGenIdeas`，基于 AgentScope，数据用 ACL 2024 long papers。

**【可复用方法】**
- **有目的地规划"该去检索什么外部知识"**：不是一次检索完，而是迭代地规划下一步检索目标，逐步把更广更深的知识喂给 idea 生成。带规划检索后唯一新颖 idea 数是不带时的 **3.4 倍**。
- **组合创新理论 + 跨域知识重组**：故意把不同领域知识拼接以激发突破 → 强化本技能 method-transfer / combination 角度。
- **专家 + 批评家多角色多轮讨论**：功能特化 agent（expert、critic）多轮交互做创意迭代优化。
- **Swiss Tournament 评选**：用瑞士轮两两比拼对大量候选 idea 排序选 top（在 170 篇种子论文上，top-rated idea 数是 SOTA 的 ≥2.5 倍）。→ 本技能产出多个 idea 时可借瑞士轮/两两 PK 做排序而非单独打分。

**【链接】** https://arxiv.org/abs/2410.14255 ｜ https://github.com/ChenShuai00/MAGenIdeas （2604.20548 链接为待核，暂不列）

**【已知坑/局限】** 评测显示生成 idea 质量"介于被接收与被拒论文之间"，离顶会接收还有差距；实验仅在 NLP 域验证。

---

## Scientific Brainstorming skill (K-Dense-AI)

**【是什么】** Claude 科研技能包里的开放式 ideation 技能，定位"早期、还没有具体观测时"的创意发散；与 hypothesis-generation（从数据出发提可检验假设）互补。

**【可复用方法】** 一套四阶段对话工作流，每阶段有现成话术：
1. **Phase 1 理解语境**：开放式提问挖背景与隐含假设（"哪个假设值得被质疑？""有没有不符合现有模型的反常发现？"）。
2. **Phase 2 发散探索**（重数量与多样、不评判），6 个结构化技法直接可抄：① 跨域类比（把别领域概念映射过来）② 假设反转（反过来会怎样 / 资源无限会怎样）③ 尺度切换（分子↔种群、毫秒↔千年）④ 约束增删（能测任何东西 / 只能用 1800 年代技术）⑤ 跨学科融合 ⑥ 技术外推（CRISPR/AI/量子来了能做什么）。
3. **Phase 3 连接**：找想法间共同线索、互补与意外联系。
4. **Phase 4 批判评估**：转向建设性筛选最有潜力的想法。
→ 这 6 个发散技法可直接补进本技能的"生成策略"。

**【链接】** https://github.com/K-Dense-AI/scientific-agent-skills （skills/scientific-brainstorming）

**【已知坑/局限】** 偏对话引导、无量化排序；产物需另接评审/可行性过滤。

---

## Hypothesis Generation skill (K-Dense-AI)

**【是什么】** 从观测/初步数据出发，按科学方法走"形成可检验假设 → 提机制 → 设计实验 → 给可证伪预测"，并探讨竞争性解释。与开放式 brainstorming 分工明确。

**【可复用方法】**
- idea 必须落到**可检验 + 可证伪的预测**，且并列列出**竞争性解释**而非只押一个机制 → 对应本技能"凭什么更强（机理假设）"与"风险"。
- 强制可视化：每份假设报告至少 1–2 张图（竞争解释框架图、机制通路图、实验设计流程图、预测决策树），用 scientific-schematics 技能生成。→ 与本包 m07/m08 绘图衔接。

**【链接】** https://github.com/K-Dense-AI/scientific-agent-skills （skills/hypothesis-generation）

**【已知坑/局限】** 需要有观测/数据作输入，不适合纯空想阶段（那应走 brainstorming）。

---

## brainstorm-diverge-converge skill (lyndonkl)

**【是什么】** 通用"发散-聚类-收敛"三段法，不限科研，适合产品/策略/研究问题。

**【可复用方法】** 五步可勾选 checklist：① 收集需求（题目/目标/约束）② Diverge：不评判地生成大量想法（示例直接生成 ~30 个）③ Cluster：归 5–6 个主题簇 ④ Converge：按"影响 × 工作量"等标准打分，选 Top 3（示例给 8.5/10 这种量化分）⑤ 记录并验证。→ 给本技能"先发散后收敛"补了一个可量化的收敛漏斗（影响-成本二维打分 + Top-N）。

**【链接】** https://github.com/lyndonkl/claude （skills/brainstorm-diverge-converge）

**【已知坑/局限】** 通用法、不含领域文献检索；新颖性靠人判断。

---

## Academic Research Skills (ARS, Imbad0202)

**【是什么】** Claude Code 的学术全流程技能套件（research → write → review → revise → finalize），`/plugin install academic-research-skills`，入口 `/ars-plan` 用苏格拉底式对话搭论文结构。明确"AI 是副驾不是主驾，human-in-the-loop"。

**【可复用方法 — 最该抄的是 7 失败模式清单】** ARS 引 Lu et al. (2026, Nature) 列出全自动 AI 科研流水线的 7 类失败模式，做成 Stage 2.5 / 4.5 的**阻断式 integrity gate**：① 实现 bug ② 幻觉结果 ③ 走捷径(shortcut) ④ 把 bug 当洞见(bug-as-insight) ⑤ 方法论造假 ⑥ frame-lock（锁死在一个框架出不来）⑦ 引用幻觉。→ 本技能生成 idea 时可拿这 7 条做反向自检，尤其"frame-lock"对应别在单一思路上死磕、"引用幻觉"对应别编不存在的对标工作。还提供 Style Calibration（学用户文风）、reviewer 可测自身 FNR/FPR 的 calibration 模式。

**【链接】** https://github.com/imbad0202/academic-research-skills

**【已知坑/局限】** CC BY-NC 4.0 非商用；强调它不替你写论文，定位辅助。

---

## What-If Oracle skill (AHK Strategies)

**【是什么】** 结构化"What-If"情景分析技能：不给单一预测，而是映射整个**可能性空间**——多分支时间线（best / likely / worst / wild card / contrarian / second-order 等 4–6 个分支），每支有自己的逻辑、概率、后果。

**【可复用方法】**
- **0·IF·1 原则**：0=未发生的潜在态，1=当前现实，IF=把 0 变 1 的条件/决策。分析质量取决于 **IF 的精确度**——"万一出岔子"太空泛，"Q3 主供应商涨价 30%"才可行动。→ 提 idea 风险/赌注时，把模糊风险改写成精确条件句。
- **多分支 + 概率 + 二阶后果**：对一个 idea 同时想最好/最可能/最坏/黑天鹅/反共识/二阶效应，而非只想成功路径。

**【链接】** https://github.com/ashrafkahoush-ux/claude-consciousness-skills （what-if-oracle；CC BY-NC-SA 4.0）

**【已知坑/局限】** 其理论基础（"What-If Paradigm/数字意识"，Zenodo 自发表 DOI）非主流同行评审，当方法论模板用、别当科学结论。

---

## Consciousness Council skill (AHK Strategies)

**【是什么】** 多视角"心智议会"审议技能：召集 4–6 个思维原型针对一个决策/难题辩论再综合，强调"刻意选会真正冲突的视角，共识廉价、张力有价值"。

**【可复用方法】** 12 原型表里几个对 idea 评审直接有用：**The Architect**（系统结构优先，盲点=过度工程化简单问题）、**The Contrarian**（反转/魔鬼代言，盲点=为反而反）等。三阶段：① 召集会冲突的成员 ② 各自发言 ③ 综合成可行洞见。→ 本技能可让"对标派/可行性派/新颖性派/工程派"几个角色对每个候选 idea 互怼，再综合，弥补单一视角天花板（与 MAGenIdeas 多 agent 讨论同源思想）。

**【链接】** https://github.com/itshussainsprojects/Claude-Council-Skill ｜ https://github.com/ashrafkahoush-ux/claude-consciousness-skills （consciousness-council；MIT）

**【已知坑/局限】** 是结构化的"认知多样性"模拟，不是真专家；archetype 选择主观。

---

## Scientific Critical Thinking skill (K-Dense-AI)

**【是什么】** 评估科学主张与证据质量的技能：方法学、实验设计、统计有效性、偏倚与混杂，并套用 **GRADE** 和 **Cochrane Risk of Bias** 框架。定位"判断证据质量、找缺陷"，与正式 peer-review 写作分工。

**【可复用方法】** idea 立项前做"反向尽调"：用 GRADE/Cochrane ROB 的视角问——这个 idea 想验证的效应，现有证据等级如何？有没有混杂/选择偏倚会让结果不可信？→ 对应本技能"凭什么更强"要立得住、"风险"要点出实验可被质疑处。

**【链接】** https://github.com/K-Dense-AI/scientific-agent-skills （skills/scientific-critical-thinking）

**【已知坑/局限】** GRADE/Cochrane 源于医学循证，迁到 CS/工程类 idea 时只能借其"分级 + 找偏倚"思路，不能照搬条目。

---

## Scholar Evaluation skill (K-Dense-AI, ScholarEval 框架)

**【是什么】** 用 ScholarEval 框架对学术工作做结构化打分评估，覆盖问题形成、方法、分析、写作等维度，给量化分 + 可执行反馈。也用来评"投稿就绪度 / 对标目标会议"。

**【可复用方法 — 8 维评估清单可直接做 idea 评分卡】**
1. 问题形成与研究问题（清晰/意义/范围可行/新颖贡献潜力）
2. 文献综述（覆盖面/批判性综合而非罗列/找到 gap/时效性）
3. 方法与研究设计（与问题匹配/严谨/可复现/伦理/局限）
4. 数据与来源（质量/样本量代表性/采集流程/可信度）
5. 分析与解释（方法恰当/严谨/逻辑自洽/考虑替代解释/结论-结果一致）
6. 结果与发现（呈现清晰/统计严谨/可视化/解读准确）
7. 学术写作与表达
8. 引用与参考（完整/质量/准确/视角平衡）
每维给：2–3 条优点 + 2–3 条改进 + 关键问题，并可用 5 分制量化。→ 本技能产出 idea 时，至少用第 1/2/3/5 维自评，再交 m04 严审。

**【链接】** https://github.com/K-Dense-AI/scientific-agent-skills （skills/scholar-evaluation；references/evaluation_framework.md 有完整 rubric）

**【已知坑/局限】** 面向"已成型的学术工作"，对一句话 idea 用时取前几维即可，别全套套。

---

## OpenAlex concept / topic graph (API)

**【是什么】** 开放学术知识图谱（替代 Scopus/Web of Science），约 2.4 亿 works，CC0。每篇 work 自带 `concepts`（旧，分级 0–5，带 score）与 `topics`/`primary_topic`（新分类体系，score）。可用其概念/主题图做选题定位、趋势与空白分析。

**【可复用方法 / 真实端点 / 参数】**
- **Base**：`https://api.openalex.org`。主要实体：`/works`、`/concepts`、`/topics`、`/authors`、`/sources`。
- **检索**：`/works?search=...`（全文/标题摘要）或 `/works?filter=title.search:graph%20neural%20network`。过滤可叠加逗号，如 `filter=title.search:diffusion model,from_publication_date:2023-01-01`。
- **趋势/空白分析用 group_by**：`/works?filter=...&group_by=primary_topic.id` 直接返回各主题计数（实测对 "diffusion model" 2023+ 返回 GAN/图像合成 2669 篇等聚合），可快速看一个方向被哪些子主题占满、哪里稀疏。也支持 `group_by=publication_year` 看时间趋势。
- **按概念/主题取代表作**：`/works?filter=concepts.id:C41008148`（C 开头是 concept id）。`/concepts?search=neural network` 查概念 id 与 `works_count`、`level`。
- **省流量**：`&select=id,display_name,cited_by_count` 只取需要字段；返回里有 `cited_by_count`、`fwci`、`referenced_works`、`related_works`、`abstract_inverted_index` 等可用于找高影响/相关/对标工作。
- **分页**：超过 page*per-page=10000 必须用游标——首次 `&cursor=*`，之后用响应 `meta.next_cursor` 续传；`per-page` 最大 200。
- **认证/限流/计费**：OpenAlex 2026 起**需免费 API key**，响应带成本字段；具体 key 申请、限流、计费、退避口径以 **m01（light-literature-search）references「OpenAlex 接入真相源」节为唯一真相源**，本技能不复写数字（改接入策略只改那一处）。仍建议带 `&mailto=you@example.com`（礼貌池）。

**【链接】** https://api.openalex.org ｜ https://developers.openalex.org ｜ 接入口径见 m01 references「OpenAlex 接入真相源」节

**【已知坑/局限】** `concepts` 字段官方逐步让位给 `topics`，新项目优先用 `topics`/`primary_topic`。计费模型 2026 改为按量额度（口径见 m01 真相源节），跑大批量前先看响应成本字段估算每日预算。






