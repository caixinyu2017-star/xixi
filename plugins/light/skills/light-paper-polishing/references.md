# light-paper-polishing 参考工具研究笔记

> 研究方法说明：本环境 WebFetch 被全面拦截，以下信息来自 WebSearch 返回的标题/摘要、已验证存在的官方 URL，以及对公开 API 文档的核查。凡无法可靠核实者均标注【未能核实】，不编造端点或功能。

---

## 1. Scientific Writing skill / Peer Review skill（学术写作与同行评审类 Claude skill）
【是什么】社区里以 SKILL.md 形式分发的两类技能：写作侧（把研究素材组织成符合学术规范的章节）和评审侧（以审稿人视角对稿件挑错）。它们不是单一官方产品，而是 academic-research-skills 这类合集中的子技能。

【可复用方法】
- 写作侧核心约束：clarity（一句一义）、concision（删冗余）、主动语态优先、避免名词化堆叠（nominalization）、术语前后一致、段落用主题句开头（topic sentence）。
- 评审侧给的是结构化审稿报告，业界通用骨架：Summary（复述贡献）→ Strengths → Weaknesses → Major comments（影响录用的硬伤）→ Minor comments（表述/笔误）→ 打分维度。这套骨架可直接做润色前的"自审清单"。
- 评分维度（综合 Elsevier reviewer 指南与 NeurIPS 式评审）：soundness（方法是否成立）、novelty/significance（贡献与差异）、clarity（可读性）、reproducibility（可复现）、related work（引用是否充分）。

【链接】
- https://www.elsevier.com/reviewer/what-is-peer-review
- https://researcheracademy.elsevier.com/navigating-peer-review
- https://en.wikipedia.org/wiki/Scholarly_peer_review

【已知坑】"Scientific Writing skill" 不是某个唯一权威实现，不同合集定义不同；引用其能力时应说"对标这类技能的工作流"，而非具体某产品端点。

---

## 2. Research-Paper-Writing-Skills（Master-cai，GitHub）
【是什么】面向 ML/CV/NLP 论文写作的 skill 包，作者注明"curated and adapted from Prof. Peng Sida's open notes"（浙大彭思达的写作公开笔记），适配 Codex / Claude Code / Gemini 三种 agent。

【可复用方法】彭思达写作方法论里最值得折进润色技能的几条：
- 先定"故事线（story line）"再写句子：每章、每段先确定"这段要让审稿人相信什么"，再填内容。润色时反向检查每段是否服务于一个明确论点。
- 引言的"四段式"：背景痛点 → 现有方法的不足（动机）→ 我们的洞察/做法 → 贡献列表。润色引言时逐段对位。
- 贡献（contribution）写法：动词开头、可度量、与 abstract/conclusion 三处措辞一致。
- 句子层面强调"don't make reviewer think"：消除指代不清、被动堆叠、长从句。

【链接】https://github.com/Master-cai/Research-Paper-Writing-Skills

【已知坑】GitHub 在本环境无法抓正文，上述细节来自仓库描述与彭思达公开写作笔记的通行内容；具体文件结构未逐字核实。

---

## 3. academic-paper-skills（lishix520，GitHub）
【是什么】"Systematic framework for planning and writing academic papers using Claude Code"，含两个角色技能：**strategist（规划）** 与 **composer（写作）**，并设有 quality checkpoints（质量检查点）。

【可复用方法】
- 双角色拆分：先 strategist 定结构/论证骨架与目标贡献，再 composer 落字。润色阶段对应"先校结构(strategist 视角)，再抠语言(composer 视角)"——与本技能"深层优先于表层"一致。
- quality checkpoints：在关键节点设硬性门槛（如"贡献是否三处一致""每个论断是否有证据"）才放行下一步。可借为润色的 gate 清单。

【链接】https://github.com/lishix520/academic-paper-skills

【已知坑】仓库正文未能抓取；checkpoint 的具体条目以描述为准，未逐条核实。

相关同类（搜索中确认存在，可参考）：
- yian0625/Paper_writing_skill —— 明确流水线 research → write → review → revise → finalize。https://github.com/yian0625/Paper_writing_skill
- bahayonghang/academic-writing-skills —— 定位"后期排版精修、格式校验与深度润色，拒绝从零代写"，与本润色技能定位高度重合，强调"提升既有文本质量"。https://github.com/bahayonghang/academic-writing-skills

---

## 4. polish / critique / audit / distill / impeccable（一组动作型 skill 名）
【是什么】这些是 Claude Code skill 生态里常见的"动作命名"风格。核查后区分如下：
- **polish**：语言层精修（流畅度、词汇、句式），不改动论点。
- **critique**：批判性审读，列出弱点与可质疑处（审稿人视角）。
- **audit**：合规/一致性核查（如 Beamer skill 里有 "TikZ audit"，指系统性逐项检查）。
- **distill**：压缩提炼（把长内容压成摘要/要点，对应摘要精炼）。
- **impeccable**：核查发现 "impeccable" 是一个**前端 UI** skill（unique frontend UI），**与论文润色无关**，不应混入写作语境。

【可复用方法】把四个写作相关动作组成润色流水线：distill（先抓核心贡献）→ critique（找弱点）→ polish（改语言）→ audit（终检一致性/格式/术语）。

【链接】
- impeccable（前端，非写作）：https://apidog.com/blog/impeccable-claude-code-skill/
- audit 风格参考（Beamer skill 的 TikZ audit / 质量评分）：https://github.com/Noi1r/beamer-skill

【已知坑】这些名字非统一标准，不同作者实现各异；"impeccable"易被望文生义当成"完美润色"，实为前端技能，已纠正。各 skill 正文未抓取。

---

## 5. Writefull（学术写作 AI，被 Digital Science/Hindawi 采用）
【是什么】面向学术英语的写作助手，核心卖点是其语言模型"基于大量已发表期刊论文训练"，因此给出的是"期刊里真实这么写"的建议，而非通用语法。提供 Word/Overleaf 插件与网页版。

【可复用方法/功能】
- **Language feedback**：检查语法、词选、学术措辞，建议偏向已发表论文的惯用表达。
- **Academizer**：把口语/非正式句改写成学术语体（独立工具页 x.writefull.com/academizer）。
- **Title Generator / Abstract Generator**：基于正文自动生成标题与摘要草稿。
- **Paraphraser**：学术语境改写。
- **Sentence Palette / 短语库**：给出某语义功能（如"指出局限""引出对比"）下期刊常用句式。
- **Overleaf 两个命令**（博客确认）：在 Overleaf 内直接调语言检查与改写。
- **GenAI detector**：检测文本是否疑似 AI 生成。

【链接】
- https://www.writefull.com/faqs
- https://x.writefull.com/academizer/
- https://blog.writefull.com/title-generator-and-paraphraser-added-to-witefull-for-word/
- https://www.digital-science.com/news/ai-based-academic-language-platform-writefull-piloted-by-open-access-publisher-hindawi-limited/

【已知坑】无公开通用 API 给第三方调用（主要走插件）；建议本质是"向已发表语料看齐"，对前沿/新术语可能保守。

---

## 6. Paperpal（Cactus/Editage 旗下学术写作工具）
【是什么】面向研究者投稿的写作助手，提供 Word 插件、网页版、浏览器版，强调"实时学术语言建议 + 投稿前检查"。

【可复用方法/功能】
- 实时语言建议：语法、拼写、学术语气（academic tone）、简洁性，针对非母语作者优化。
- **Submission Readiness / 预投稿检查**：技术合规类核查（如字数、参考文献格式、图表引用、伦理与利益冲突声明是否齐全），对标期刊投稿要求。
- 改写/扩写/缩写与同义替换。
- 抄袭检测、AI 检测（部分版本）。

【链接】https://paperpal.com/

【已知坑】官网在本环境无法抓取，功能清单据搜索摘要与同类产品（LetPub Verity 等预投稿检查工具）通行项归纳；具体检查项数目未逐条核实。无开放 API。

---

## 7. Grammarly（通用写作助手）
【是什么】通用英语写作助手（非学术专精），覆盖语法/拼写/标点，并提供风格与语气分析。

【可复用方法/功能】Grammarly 把建议分为四大维度，这套维度直接可借为语言层 checklist：
- **Correctness**：语法、拼写、标点错误。
- **Clarity**：是否简洁、是否有冗长/含混表达（rewrite for conciseness）。
- **Engagement**：用词是否单调（词汇多样性）。
- **Delivery / Tone**：语气是否得体（tone detector），对学术稿应偏正式、克制。
另有可读性评分、字数/字符统计、抄袭检测、AI 写作辅助。

【链接】
- https://www.grammarly.com/features
- https://en.wikipedia.org/wiki/Grammarly

【已知坑】非学术专精——对术语、引用规范、学术语体不如 Writefull/Paperpal；面向第三方的实时编辑 SDK（Grammarly Text Editor SDK）已于 2024 年起停止/弃用方向，不应假设有稳定公开 API。学术润色时其"engagement/华丽用词"建议需谨慎采纳。

---

## 8. LanguageTool（开源语法风格检查，可自托管）
【是什么】开源（Java）语法、拼写、风格检查器，支持 30+ 语言，提供云 API 与可自托管 server。是唯一在本组里有**清晰公开 REST API**的工具。

【可复用方法/真实端点/参数】
- 公开/云端点：`POST https://api.languagetool.org/v2/check`（高级版为 `https://api.languagetoolplus.com/v2/check`）。
- 关键参数：
  - `text`（待检查文本，或用 `data` 传带标注的 JSON）
  - `language`（如 `en-US`、`auto` 自动识别）
  - `motherTongue`（母语，用于检测易混错误，如 `zh-CN`）
  - `enabledRules` / `disabledRules`（逗号分隔规则 ID）
  - `enabledOnly`（仅跑 enabledRules）
  - `level`：`default` 或 `picky`（picky 开启更严格的风格规则，适合论文精修）
- 认证：免费匿名可用但有速率/字数限制；高级版用 `username` + `apiKey` 参数。
- 返回 JSON：`matches[]`，每条含 `message`（问题说明）、`shortMessage`、`replacements[]`（建议替换）、`offset` + `length`（定位）、`rule`（含 `id`、`category`、`issueType`）、`context`。
- 自托管：官方 docker / 社区镜像（loglux/languagetool-docker、meyayl/docker-languagetool），起一个本地 `server.py`/jar 即可离线批量检查，隐私友好。

【链接】
- https://languagetool.org/api
- https://api.languagetoolplus.com
- https://dev.languagetool.org/java-api.html
- https://github.com/loglux/languagetool-docker
- https://pylanguagetool.lw1.at/api_docs/

【实测（2026-06-06 本环境 curl）】`POST https://api.languagetool.org/v2/check`，匿名（无 key）`-d language=en-US --data-urlencode text=...` → **HTTP 200**，返回合法 JSON，`matches[]` 含 `message`/`replacements`/`offset`/`rule.id`（如 PLURAL_VERB_AFTER_THIS、EN_A_VS_AN），并带 `premiumHint`（提示部分规则仅 Premium 可见）。结论：本组里唯一可直接匿名跑通的工具，定为首选。

【已知坑】免费匿名端点有限流（官方文档实测 2026-06：每 IP 每分钟 20 请求 + 75 KB 文本，仅 POST，超限 HTTP 429）；规则偏通用语法，深层学术论证它管不了；长稿需分段并尊重限流。

---

## 9. DeepL Write（改写/润色 API）
【是什么】DeepL 的写作改写产品，提供 grammar/style 改写，并可指定写作风格与语气；有对应的 "improve text" API（写作改写端点）。

【可复用方法/真实端点/参数】
- 端点：`POST https://api.deepl.com/v2/write/rewrite`（免费版 host 为 `api-free.deepl.com`）。
- 认证：HTTP 头 `Authorization: DeepL-Auth-Key <key>`。
- 核心参数：
  - `text[]`（待改写文本，可数组）
  - `target_lang`（如 `EN-US`、`DE`）
  - `writing_style`（写作风格，文档列出含 `academic`、`simple`、`business`、`casual`、`default`/`prefer_*` 变体）
  - `tone`（语气，如 `confident`、`diplomatic`、`enthusiastic`、`friendly`、`default`；**注意 writing_style 与 tone 通常二选一，不可同时指定非默认值**）
- 返回：`improvements[]`，含改写后的 `text` 与检测到的源语言。

【链接】
- https://developers.deepl.com/docs/api-reference/improve-text
- https://www.deepl.com/en/docs-api/
- 风格与语气说明：https://support.deepl.com/hc/en-us/articles/9710730337820

【实测（2026-06-06 本环境 curl，用占位 key `DeepL-Auth-Key test`）】
- `POST https://api-free.deepl.com/v2/write/rewrite` → **HTTP 404**
- `POST https://api.deepl.com/v2/write/rewrite` → **HTTP 404**
- `POST https://api-free.deepl.com/v2/translate` → **HTTP 403**
- `POST https://api.deepl.com/v2/translate` → **HTTP 403**
说明：`/v2/write/rewrite` 在两个 host 上都返回 404（路径不可匿名命中，疑似改写产品走独立鉴权/路径，或对无效 key 直接拒绝路由）；`/v2/translate` 返回 403（端点存在但需有效 `Authorization: DeepL-Auth-Key`）。**结论：DeepL 在本环境无法匿名验证或运行**，写作改写功能需付费/有效 key，参数（`text[]`/`target_lang`/`writing_style`/`tone`）来自公开文档结构，未能在本环境实跑确认响应体。故 SKILL.md 中 DeepL 仅作"有 key 时的整句改写参考"，首选改用可匿名跑通的 LanguageTool。

【已知坑】本环境无法抓 developers.deepl.com 正文，参数名据 DeepL 公开 API 文档结构与搜索摘要给出；`writing_style="academic"` 适合论文，但 DeepL 改写偏整句重述，可能动到术语与作者声音，**改写后必须人工核对术语与事实**。免费版有月度字符配额。

---

## 综合：折进 light-paper-polishing 的要点
1. 评审维度统一为：soundness / novelty / clarity / reproducibility / related-work（来自 Elsevier + NeurIPS 式评审），作为深层润色 checklist。
2. 语言层维度借 Grammarly 四分法（correctness / clarity / engagement / delivery），但学术稿弱化 engagement、强化 formality。
3. 流水线借动作型 skill：distill → critique → polish → audit。
4. 引言用彭思达"四段式"、贡献三处一致（abstract/intro/conclusion）。
5. 工具落地：纯语法首选**可匿名跑通**的 LanguageTool 云端点（`/v2/check`, `level=picky`，本环境实测 200）批量过，隐私场景转自托管；整句改写可参考 DeepL `writing_style=academic`，但**需付费/有效 key**（本环境实测 rewrite 404、translate 403，无法匿名跑），且偏整句重述，务必人工复核术语与事实；学术措辞向 Writefull"已发表语料"思路看齐。

