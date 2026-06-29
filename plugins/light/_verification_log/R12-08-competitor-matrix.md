# R12.8 竞品对照矩阵 — 实查留痕（当时版本）

- 对照日期：**2026-06-12**（竞品在持续演进，本表只陈述此日实查事实，不贬低）。
- 方法：GitHub MCP 直接拉仓库目录树数主干技能数；README 经 WebFetch/raw 读取定位定位/能力；技能数=`skills/` 下子目录计数（排除模板 `_*.md`）。
- 纪律：每个"无"都是"此日该仓库 README/目录未见"，非"永远没有"；竞品后续可能补上。

## 实查记录

### 1. anthropics/skills（官方套件）
- commit 抓取点 `57546260929473d4e0d1c1bb75297be2fdfa1949`（2026-06-12 拉取）。
- `skills/` 下 **17 个技能**：algorithmic-art, brand-guidelines, canvas-design, claude-api, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing, xlsx。
- 定位：通用文档/制品工具（Office 文件读写、前端制品、技能脚手架），**非科研工作流**。无科研主线衔接、无知识库、无中文、无诚实/防编造机制、无会话衔接、无行为评测（README 与目录未见）。
- 来源：https://github.com/anthropics/skills （README + skills/ 目录树）。

### 2. K-Dense-AI/scientific-agent-skills（头部科研套件，最强对照）
- commit `dab7aa672944a77f20cda3f2a672a6f1582adab6`（2026-06-12 拉取）。
- `skills/` 下 **146 个技能**（远超审计估的"6-8"——审计当时口径偏旧/指别的小仓）：多为单一科研 Python 库/数据库的封装（adaptyv/aeon/anndata/astropy/biopython/deepchem/cobrapy/diffdock/esm…），覆盖生信/化学信息/药物发现/临床/ML/材料/地理空间/实验室自动化/科学传播。
- README 自述：统一接入 **100+ 数据库**（PubChem/ChEMBL/UniProt/ClinicalTrials.gov 等）+ 70+ Python 包；**支持连续多步研究流水线**（一条 prompt 链里查库→分析→出报告）；多 agent 兼容（Cursor/Claude Code/Codex/Antigravity）。仓库级 MIT，单技能各自许可。
- README **未见**：中文支持、会话衔接机制、诚实/防编造护栏、行为评测。仓库有超大 `SECURITY.md`（508KB，疑为自动扫描产物）。
- 来源：https://github.com/K-Dense-AI/scientific-agent-skills （README raw + skills/ 目录树，146 计数程序化数得）。

### 3. ScienceIntelligence/ResearchSkills（学科知识型，带中文）
- commit `ada6c05b4e15eef0d1010c8d4d38f9db01963330`（2026-06-12 拉取）。
- `skills/` 按**学科**组织 **8 个领域**：clinical-medicine, computer-science, economics, management, mathematics, physics, quantitative-biology, statistics；另有记忆模板（episodic/procedural/semantic）。
- 有 `readme.md` + **`readme_zh.md`（中文）**、`CLAUDE.md`、`.context/`；定位为按学科组织的研究知识/记忆型技能，**非端到端论文工作流**（无投稿定位/排版/软著专利/竞赛/PPT 生图等成果工程链路）。诚实机制/行为评测 README 未见。
- 来源：https://github.com/ScienceIntelligence/ResearchSkills （readme + skills/ 目录树）。

## 关键诚实修正（写入 R10 须知）
- 审计旧结论"最接近的仅 6-8 技能"**已过时**：K-Dense 现 146 技能、anthropics 17。Light 的差异化**不在技能数**（数量上不占优），而在**形态**：科研主线闭环 + 自有知识库 + 写进规约的诚实底线 + 中文链路 + 会话衔接 + 行为评测这套组合，竞品各有其一二，未见同时具备。
- K-Dense 是"库封装广度"路线（146 个工具各包一库），Light 是"工作流纵深 + 中文 + 诚实"路线，两者不是同形态竞品，对照时按"形态差异"陈述，不比纯数量。
- ScienceIntelligence 也有中文 + 记忆，故"中文链路"格对它不能写"无"，只能写"有中文 README，但无端到端成果工程链路"——逐格按实查写，别一刀切。
