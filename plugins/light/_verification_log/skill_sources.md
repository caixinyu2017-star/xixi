# 技能内部实现重核（curl 直读 GitHub 源码）

研究日期 2026-06-06。本轮用 Bash `curl` 直连 GitHub API + raw 重核此前「未能核实（GitHub/网页被拦）」的 skill 内部实现。
凡标注【真实源码】者均来自本轮 curl 实际返回；标注【证伪/不存在】者为按名查找后确认不存在。

## 核查方法
- 列目录：`https://api.github.com/repos/<org>/<repo>/contents/<path>`
- 读源码：`https://raw.githubusercontent.com/<org>/<repo>/<branch>/<path>/SKILL.md`
- 全树：`https://api.github.com/repos/<org>/<repo>/git/trees/main?recursive=1`

## 关键校正（重要事实更新）
1. **K-Dense 仓库已改名**：`K-Dense-AI/claude-scientific-skills` → **`K-Dense-AI/scientific-agent-skills`**（GitHub API 301 重定向确认，default_branch=main）。旧链接仍能跳转，但 raw 必须用新名。
2. **superpowers 无 `critique`/`audit` 同名 skill**：全树 recursive 搜索 critique/audit 仅命中 code-review 相关文件，**无独立 critique/audit 技能**。此前推断正确。
3. **K-Dense 无 `find-skills` 技能**：按名 contents 查询返回 `Not Found`。同仓有 `autoskill` / `get-available-resources` 等近似功能，但无 `find-skills`。

---

## A. obra/superpowers（核心开发流铁律）

### A1. verification-before-completion 【真实源码】
回填到：**light-self-review、light-idea-critique**
- 链接：https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md
- 目录仅含 `SKILL.md`（无脚本，纯方法论）。
- **核心铁律（The Iron Law）**：`NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE` — 本条消息里没跑过验证命令，就不能声称通过。
- **Gate Function（闸门 5 步）**：1) IDENTIFY 哪条命令能证明此声明 → 2) RUN 跑完整命令（fresh, complete）→ 3) READ 完整输出+退出码+失败计数 → 4) VERIFY 输出是否确证 → 5) ONLY THEN 才下结论。跳任一步 = 撒谎而非验证。
- **Common Failures 对照表（声明 / 需要 / 不充分）**：Tests pass→需测试输出 0 failures，不够：上次运行、"应该过"；Build succeeds→需 exit 0，不够：linter 过、日志看着对；Bug fixed→需复测原症状通过，不够：改了代码就假定修好；Regression test→需 red-green 循环验证，不够：跑过一次；Agent completed→需 VCS diff 显示改动，不够：agent 自报成功；Requirements met→需逐行 checklist，不够：测试通过。
- **Red Flags（看到即停）**：用 "should/probably/seems to"；验证前就说 "Great!/Perfect!/Done!"；未验证就 commit/push/PR；信 agent 自报；只做了部分验证；"就这一次"。
- **TDD Red-Green 规范**：Write → Run(pass) → Revert fix → Run(MUST FAIL) → Restore → Run(pass)。

### A2. requesting-code-review 【真实源码】
回填到：**light-self-review（请评审一侧）**
- 链接：https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md
- 目录含 `SKILL.md` + `code-reviewer.md`（评审 subagent 模板）。
- **核心**："Review early, review often"。派一个 code-reviewer **subagent**，只给精心裁剪的上下文（**绝不给整段会话历史**），让评审聚焦产物而非你的思考过程，同时保住主 agent 的 context。
- **何时请评审**：强制——subagent-driven 每个 task 后、完成大特性后、合入 main 前；可选——卡住时（换视角）、重构前（基线）、修完复杂 bug 后。
- **操作**：1) 取 SHA：`BASE_SHA=$(git rev-parse HEAD~1)`、`HEAD_SHA=$(git rev-parse HEAD)`；2) 用 Task 工具 general-purpose 类型，填 `code-reviewer.md` 模板（占位 `{DESCRIPTION}/{PLAN_OR_REQUIREMENTS}/{BASE_SHA}/{HEAD_SHA}`）；3) 按反馈处理：Critical 立即修、Important 继续前修、Minor 记录待办。

### A3. receiving-code-review 【真实源码】
回填到：**light-self-review、light-review-rebuttal（收评审/收审稿意见一侧）**
- 链接：https://github.com/obra/superpowers/blob/main/skills/receiving-code-review/SKILL.md
- **核心原则**："Verify before implementing. Ask before assuming. 技术正确性高于社交舒适。"
- **Response Pattern（6 步）**：READ（读完不立即反应）→ UNDERSTAND（用自己的话复述需求或发问）→ VERIFY（对照代码库实际）→ EVALUATE（对**本**代码库技术上是否成立）→ RESPOND（技术性确认或有理有据的反驳）→ IMPLEMENT（一次一项，逐项测试）。
- **Forbidden Responses**：禁止 "You're absolutely right!"（显式违反 CLAUDE.md）、"Great point!"、未验证就 "Let me implement that now"。改为：复述技术需求 / 问清楚 / 有理由就技术性反驳 / 直接动手（行动胜于表态）。
- 反馈不清时：STOP，先别动任何代码，先问清。

### A4. brainstorming 【真实源码】
回填到：**light-idea-generation、light-idea-critique、light-research-plan**
- 链接：https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md
- 目录：`SKILL.md` + `scripts/` + `spec-document-reviewer-prompt.md` + `visual-companion.md`。
- **HARD-GATE**：在拿出 design 并获用户批准前，不得调用任何实现类 skill、不写代码、不脚手架。适用于**每个**项目，无论看起来多简单。
- **9 步 Checklist（须为每项建 task 按序完成）**：1) 探查项目上下文（文件/文档/近期 commit）；2) 视觉伴侣（若涉视觉，单独成条消息）；3) 一次一个澄清问题（优先选择题）；4) 提 2-3 个方案+权衡+推荐；5) 分节呈现 design，每节获批；6) 写 design doc 存 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` 并 commit；7) Spec 自审（查占位符/矛盾/歧义/范围）；8) 用户审 spec；9) 转 writing-plans skill。
- **终态唯一**：批准后只调 writing-plans，**不**调 frontend-design/mcp-builder 等实现 skill。
- 大项目须先分解为子项目，每个子项目各走 spec→plan→implementation。

<!-- KDENSE_PLACEHOLDER -->

---

## B. K-Dense-AI/scientific-agent-skills（原 claude-scientific-skills，已改名）
仓库根：https://github.com/K-Dense-AI/scientific-agent-skills （branch main，130+ 技能）

### B1. research-lookup 【真实源码】
回填到：**light-literature-search、light-idea-generation**
- raw：https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/research-lookup/SKILL.md
- license MIT，version 1.0，author K-Dense Inc.，`allowed-tools: Read Write Edit Bash`。
- **智能后端路由**（自动按 query 类型选最优后端）：
  · **parallel-cli search**（主/默认后端）：快、省，academic 源优先，用 `--include-domains` 锁学术源；
  · **Parallel Chat API（core 模型）**：复杂多源深研，60s-5min，仅必要时用；
  · **Perplexity sonar-pro-search（经 OpenRouter）**：仅学术论文检索（含 papers/DOI/journal/peer-reviewed 等关键词时）。
- **隐私提示（描述中明示）**：query 文本会传给 api.parallel.ai（PARALLEL_API_KEY），学术检索还会传 openrouter.ai（OPENROUTER_API_KEY）。
- 文档建议配 scientific-schematics 出版级配图：`python scripts/generate_schematic.py "描述" -o figures/output.png`。

### B2. paper-lookup 【真实源码】
回填到：**light-literature-search、light-citation**
- raw：https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/paper-lookup/SKILL.md
- version 1.0，author K-Dense Inc.。**经 REST API 查 10 个学术库**：PubMed、PMC（全文）、bioRxiv、medRxiv、arXiv、OpenAlex、Crossref、Semantic Scholar、CORE、Unpaywall。
- **5 步工作流**：1) 理解 query（DOI/主题/作者/OA/全文）→ 2) 选库（按用例表）→ 3) **先读 `references/` 里对应库的端点参考文件再调** → 4) 调 API → 5) 返回**原始 JSON**（arXiv 为 XML）+ 已查库与端点清单（无结果须明说，不得省略）。
- **按用例选库（节选真实表）**：生医主题→PubMed；生医全文→PMC；生物预印→bioRxiv；医学预印→medRxiv；理/数/CS 预印→arXiv；全领域→OpenAlex；按 DOI→Crossref；OA PDF→Unpaywall；引文图→Semantic Scholar；作者著作→Semantic Scholar；全领域全文→CORE；期刊/资助方元数据→Crossref；PMID/PMCID/DOI 互转→PMC ID Converter。
- 跨库：「某文全部信息」= Crossref+Semantic Scholar+Unpaywall；「全面文献检索」= PubMed+OpenAlex+Semantic Scholar。

### B3. bgpt-paper-search 【真实源码】
回填到：**light-literature-search**
- raw：https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/bgpt-paper-search/SKILL.md
- license MIT，**version 1.1**，author BGPT，website https://bgpt.pro/mcp ，github https://github.com/connerlambden/bgpt-mcp 。
- **是什么**：远程 **MCP 服务器**，检索从全文研究抽取的结构化实验数据库。不同于只返回题录/摘要的传统库，BGPT 每篇返回 **25+ 字段**：methods、定量 results、sample sizes、quality scores、conclusions。
- **依赖**：需在 agent host 配好 BGPT MCP（`npx mcp-remote https://bgpt.pro/mcp/sse` 或 `npx bgpt-mcp`），联网 bgpt.pro，付费用量需 BGPT API key。skill 本身只指示调用 `search_papers` MCP 工具，**不自带 MCP 访问能力**。
- 适用：要 sample size/effect size/方法学对比/质量评分/证据表（meta 分析、临床指南）等摘要里没有的全文结构化数据。

### B4. scientific-brainstorming 【真实源码】
回填到：**light-idea-generation**
- raw：.../skills/scientific-brainstorming/SKILL.md ｜ MIT，v1.0，K-Dense Inc.。
- **定位**：开放式科研创意。早期（**尚无具体观测/数据**）阶段用；做创意伙伴生成假设、探跨学科联系、挑战假设、发展方法、找研究空白。描述明确分工：要从数据形成可检验假设走 hypothesis-generation。

### B5. hypothesis-generation 【真实源码】
回填到：**light-idea-generation、light-research-plan**
- raw：.../skills/hypothesis-generation/SKILL.md ｜ MIT，v1.0，`allowed-tools: Read Write Edit Bash`。
- **定位**：有观测/数据后，按科学方法系统形成**可检验假设**：从观测出发→提机制→设计实验→给可证伪预测，并探竞争性解释。分工：开放空想走 scientific-brainstorming；数据集上 LLM 自动化假设检验走 hypogenic。

### B6. scientific-critical-thinking 【真实源码】
回填到：**light-idea-critique、light-self-review**
- raw：.../skills/scientific-critical-thinking/SKILL.md ｜ MIT，**v1.1**。
- **定位**：评估科学主张与证据质量——方法学、实验设计、统计有效性、偏倚、混杂、证据质量，**用 GRADE 与 Cochrane Risk of Bias（ROB）框架**。分工：写正式 peer review 走 peer-review。
- compatibility：分析本身不需联网；可选配图经 scientific-schematics 需 OPENROUTER_API_KEY。

### B7. scholar-evaluation 【真实源码】
回填到：**light-self-review、light-idea-critique**
- raw：.../skills/scholar-evaluation/SKILL.md ｜ MIT，v1.0；含 `references/evaluation_framework.md`（完整 rubric）。
- **定位**：用 **ScholarEval 框架**系统评估学术工作，跨多质量维度（problem formulation、methodology、analysis、writing）做**量化评分 + 可执行反馈**；可评论文/提案/文献综述/学术写作，并判断对目标 venue 的发表就绪度。定位为「量化评分」，与 peer-review（定性评审）互补。

### B8. peer-review 【真实源码】
回填到：**light-review-rebuttal、light-self-review**
- raw：.../skills/peer-review/SKILL.md ｜ MIT，v1.0，`allowed-tools: Read Write Edit Bash`；目录含 `SKILL.md`+`references/`+`scripts/`。
- 标题「Scientific Critical Evaluation and Peer Review」。**定位**：基于 checklist 的结构化稿件/基金评审——方法学、统计、设计、可复现性、伦理、报告规范，给建设性反馈。**报告规范合规检查含 CONSORT/STROBE/PRISMA**。分工：评证据质量走 scientific-critical-thinking；量化评分走 scholar-evaluation。

---

## C. anthropics/skills（官方）
仓库根：https://github.com/anthropics/skills ｜ skills/ 下 17 个官方 skill（algorithmic-art, brand-guidelines, canvas-design, claude-api, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing, xlsx）。

### C1. frontend-design 【真实源码】
回填到：**light-typesetting / 任何前端产出类技能**
- raw：https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md
- **定位**：造有辨识度、production-grade 的前端界面，**刻意规避「AI slop」通用审美**。
- **Design Thinking（编码前）**：先定 Purpose / Tone（取一种极端：brutally minimal、maximalist chaos、retro-futuristic、editorial、brutalist 等）/ Constraints / Differentiation（让人记住的那一点）。
- **审美指南**：Typography——避开 Arial/Inter 等通用字体，display 字体配 refined body 字体；Color——CSS 变量、主色+利落 accent；Motion——HTML 优先纯 CSS、React 用 Motion 库，重点是一次编排好的 staggered page-load；Spatial——非对称/重叠/对角/破格。
- **明确禁令**：不得用通用 AI 审美——overused 字体（Inter/Roboto/Arial/system）、陈词色（尤其白底紫渐变）、可预测布局；且**不得**在多次生成间收敛到同一选择（点名 Space Grotesk 为反例）。

### C2. skill-creator 【真实源码】
回填到：**autoskill / 元技能创作**
- raw：https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md
- **定位**：创建/修改/优化 skill，并**测量 skill 性能**（跑 eval、benchmark 含方差分析、优化 description 以提升触发准确率）。
- **创建流程**：定目标 → 写草稿 → 写几个 test prompt 用 claude-with-access-to-the-skill 跑 → 定性+定量评估（后台跑时起草定量 eval，用 `eval-viewer/generate_review.py` 生成 review 给用户看）→ 按反馈重写。

---

## D. 证伪/不存在（按名查找后确认）

- **superpowers `critique` skill**：【不存在】全树 recursive 搜索无 critique 独立技能。其职能由 requesting-code-review + receiving-code-review + verification-before-completion + brainstorming 分担。→ 修正 light-self-review / light-idea-critique 中相关表述（此前推断与本轮一致）。
- **superpowers `audit` skill**：【不存在】无同名技能；仅 code-review 相关文件。安全审计需借社区实现（如 wrsmith108/claude-skill-security-auditor）或通用审计模式，不可冠以 superpowers/anthropic 官方名。
- **K-Dense `find-skills` skill**：【不存在】contents 查询返回 Not Found。同仓近似功能为 `autoskill`、`get-available-resources`、`hugging-science`，但**无 find-skills**。→ 修正 light-memory-pm / 技能索引类引用，勿引用不存在的 find-skills。
- **仓库改名**：所有引用 `K-Dense-AI/claude-scientific-skills` 的 raw 链接须改为 `K-Dense-AI/scientific-agent-skills`（旧名 GitHub 仍 301 跳转，但 raw.githubusercontent.com 旧名可能取不到）。涉及 light-idea-generation、light-idea-critique、light-literature-search 等多处 references.md。

## 回填动作清单
1. light-self-review：补 A1/A2/A3 真实步骤；audit 段保留「无官方同名」诚实声明。
2. light-idea-critique：补 A1、A4、B6、B7；critique「无单一来源」声明保留。
3. light-idea-generation：补 A4、B1、B4、B5；改 K-Dense 链接为新仓名。
4. light-literature-search：补 B1/B2/B3 真实端点与工作流；改链接。
5. light-citation：补 B2 十库清单。
6. light-review-rebuttal：补 A3、B8（含 CONSORT/STROBE/PRISMA）。
7. light-research-plan：补 A4、B5。
8. 全局：批量替换旧仓名 `claude-scientific-skills` → `scientific-agent-skills`。


