# 参考工具研究笔记 — light-review-rebuttal

逐工具核查（2026-06）。每条都标注【是什么】【可复用方法/真实端点/参数】【链接】【已知坑/局限】。
未能核实者如实标注，未编造端点。

---

## 1. academic-paper-reviewer（imbad0202/academic-research-skills，"Review/Revise" 技能）

【是什么】最贴近本技能的开源项目：模拟完整国际期刊同行评审流程的多智能体技能（v1.10）。
3 阶段流水线 + 7 个 agent：先识别领域并动态配置 5 位审稿人身份，再并行评审，最后综合出录用决定与返修路线图。

【可复用方法】
- **5 位审稿人画像**（非重叠视角，可直接照搬到模式一）：
  1. EIC（主编）— 期刊契合度、原创性、整体质量、对读者群的相关性；不深入方法细节。
  2. R1 方法学 — 研究设计、抽样、统计有效性、效应量、可复现性、数据透明。
  3. R2 领域 — 文献覆盖、理论框架、领域贡献定位。
  4. R3 跨视角 — 跨学科连接、实践影响、挑战根本假设。
  5. **Devil's Advocate（魔鬼代言人）— 不打分，只攻击**：找最脆弱点、最大逻辑缺口、最强反论。是投稿前的"压力测试"。
- **7 维通用评审框架 + 权重**（方法学权重最高）：原创性 15%、方法学严谨性 25%、证据充分性 20%、论证连贯性 15%、写作质量 10%、文献整合 10%、意义与影响 5%。每维 1–5 分含明确行为锚点（5 出色 / 4 强 / 3 合格 / 2 弱 / 1 不可接受）。
- **按论文类型追加维度**：实证（假设可检验性、变量操作定义、内/外部效度、统计报告完整性 effect size+CI+假设检验、结论保守性）；理论（概念界定、前提→推理→结论链、反论处理、可检验命题）；综述/元分析（PRISMA 合规、纳入排除标准、偏倚风险评估、异质性处理、发表偏倚）；案例研究（案例选择理由、三角验证、厚描述、可迁移性、研究者反身性）。
- **三透镜思维框架**（产出高质量评审的认知方法）：
  - 透镜1 内部效度"证据支持论点吗"——找中心论点→证据→论证链(warrant)→未考虑的替代解释→**抽掉哪一条证据论证就崩**(linchpin 单点依赖)。
  - 透镜2 外部效度"研究之外还成立吗"——目标总体→样本代表性→可复制条件→换情境/文化/时间是否成立→作者没提的边界条件。启发：多数作者高估普适性。
  - 透镜3 贡献"so what"——之前知道什么→之后知道什么→delta 是否有意义(非仅统计显著)→谁受益→开启什么新问题。启发：一句话说不清 delta，要么贡献弱要么没讲清。
- **审稿人常见陷阱表**（自查）：方法学隧道视野（先看贡献再看方法）；新颖性偏见（复现也有价值）；专长投射（按论文所选方法本身评，别强求你偏好的方法）；正面-严苛摇摆（先写分再写评语）；只见树木（永远先说唯一最重要的问题）。
- **5 条校准问题**（评审写完后自查）：①若原样发表会误导读者吗？(是→Major/Reject) ②作者一个返修周期能解决吗？(否→Reject) ③我对它比对自己的工作更苛刻吗？④至少找到一个真实优点了吗？⑤即便拒稿，我的评审能帮作者改进吗？
- **编辑决定明确阈值**（综合后判定）：Accept = 各维均分≥4.0 且无维度<3.0 且≥3/4 审稿人推荐 Accept/Minor；Minor = 均分≥3.5 且无维度<2.5，2–4 周可解决，不动核心论点/方法；Major = 有潜力但需大改后重审；Reject。另有 0–100 加权映射：≥80 Accept / 65–79 Minor / 50–64 Major / <50 Reject。
- **re-review（验证性复审）模式**：输入"返修路线图 + 修改稿 + response letter"，逐条判定 `FULLY_ADDRESSED / PARTIALLY_ADDRESSED / NOT_ADDRESSED / MADE_WORSE`。Priority 1 必须全部 FULLY_ADDRESSED 才能 Accept。**可溯源规则**：对每条 P1，复审者须①读作者声称②跳到声称的修改位置③独立核实声称与实际改动一致；若作者声称为空或含糊（"已按建议修改"）则标 `🔍 Cannot verify`。
- **承诺账本(commitment ledger)**：把每条审稿意见解析出的"承诺"逐条核验 `fulfilled / partial / not-fulfilled / explicitly-rejected-with-rationale`，证据类型决定核验位置（new_section/figure/table/citation 在修改稿核验；acknowledgment_only 在 response letter 核验；prose_edit 核验具体句子）。非 fulfilled 必须带 rationale，否则报 `COMMITMENT_GAP`。
- **revision_response_template（R→A→C 格式）**：Reviewer Comment → Author Response → Changes Made。规则：每条都回不许跳过；不同意须给理由不能只写"disagree"；改动用 tracked changes/颜色标注；提供改前改后页码交叉引用。**生成标红稿的工具**：LaTeX 项目用 latexdiff（`latexdiff old.tex new.tex` 或 `latexdiff-vc --git -r <旧tag>`，多文件加 `--flatten`，中文/公式炸点降级 `--math-markup=0`，详见 light-typesetting `light-typesetting/references.md`「latexdiff」节）；Word 项目用修订模式（OOXML `<w:ins>`/`<w:del>`）。结构：稿件信息 → 变更摘要(300–500 字，列 Major/结构/新增) → 逐 reviewer 分段（先 "Strengths Acknowledged" 致谢，再 R1-W1/W2… 逐条）。
- **calibration（校准）模式**（独到）：用 5–20 篇已知录用结果的金标准论文，测本审稿人自身的假阴率 FNR/假阳率 FPR/平衡准确率，作为置信披露附到后续评审。要点：金标准集须同时含 ≥1 accept 和 ≥1 reject，n<10 时结果仅供参考；误差画像是领域特定的。

【链接】
- 仓库：https://github.com/imbad0202/academic-research-skills
- SKILL.md：https://raw.githubusercontent.com/imbad0202/academic-research-skills/main/academic-paper-reviewer/SKILL.md
- 评审框架：https://raw.githubusercontent.com/imbad0202/academic-research-skills/main/academic-paper-reviewer/references/review_criteria_framework.md
- 三透镜：https://raw.githubusercontent.com/imbad0202/academic-research-skills/main/academic-paper-reviewer/references/review_quality_thinking.md
- 编辑决定标准：.../references/editorial_decision_standards.md ；re-review：.../references/re_review_mode_protocol.md ；返修模板：.../templates/revision_response_template.md ；校准：.../references/calibration_mode_protocol.md

【已知坑/局限】单 LLM 审稿人绝对分仅"序数可解释"不"基数可解释"（85 分不保证录用）；FPR 偏高（易过度拒稿，见下 ScholarPeer/Lu 数据）。多 agent 跑全流程 token 开销大。

---

## 2. OpenReview API v2 + openreview-py（抓真实公开审稿/rebuttal 的数据源）

【是什么】ICLR/NeurIPS/COLM 等顶会的公开评审平台。其 REST API 可直接拉取某会议全部投稿的审稿意见、作者 rebuttal、reviewer-author 讨论、meta-review、最终决定——是"模式一对标真实审稿风格""学习成功 rebuttal 话术"的一手语料来源。

【可复用方法/真实端点/参数】（2026-06 curl 逐条实测，HTTP 码见文末实测记录）
- **Base URL（API v2，2024 起默认）**：`https://api2.openreview.net`；2024 前的老会议走 legacy v1 `https://api.openreview.net`，两者 JSON 结构不同，先确认会议年份再选版本。
- **核心端点 `GET /notes`**（一切提交物——论文、审稿、rebuttal、meta-review 都是一条 Note）。
- **⚠️ 实测关键坑——审稿 invitation 是 per-submission，不是 venue 级**：
  - ❌ `?invitation=ICLR.cc/2024/Conference/-/Official_Review` → 实测 **HTTP 200 但 `{"notes":[]}`**（venue 级 review invitation 根本不存在，照抄必拿空结果）。legacy v1 同 URL 实测 `{"notes":[],"count":0}`，同样空。
  - ✅ 真实审稿 invitation 形如 `ICLR.cc/2024/Conference/Submission9504/-/Official_Review`（多一段 `Submission<编号>`）——实测对 forum `cXs5md5wAq`(#9504) 返回 **4 条** Official_Review，含 `summary/soundness/presentation/contribution/strengths/weaknesses/questions/rating/confidence`。rebuttal/讨论是 `.../Submission9504/-/Official_Comment`、meta 是 `.../Submission9504/-/Meta_Review`、决定是 `.../Submission9504/-/Decision`（均实测存在）。
  - ✅ 只有 **投稿本身** 是 venue 级：`?invitation=ICLR.cc/2024/Conference/-/Submission` 实测返回全部投稿（每条带 `id`/`number`/`forum`）。NeurIPS 2024 同样：venue 级 Submission 可用，venue 级 Official_Review 返回空。
- **取审稿的两条实测可用路径**：
  1. **批量（推荐）**：拉投稿时带 `details=directReplies`，每篇投稿的 `details.directReplies` 直接挂着它的 Official_Review/Official_Comment/Meta_Review/Decision——实测对单篇投稿返回 7 条 directReplies（含 4× Official_Review、1× Official_Comment、1× Meta_Review、1× Decision）。一次调用即可遍历全 venue 审稿：
     `GET /notes?invitation=ICLR.cc/2024/Conference/-/Submission&details=directReplies&limit=1000&offset=0`
  2. **单篇**：拿到 `forum`(=投稿 id) 后按论文取整条讨论树 `GET /notes?forum=<forum_id>&details=directReplies`（实测对 `cXs5md5wAq` 返回 13 条 Note，覆盖 Submission/Official_Review×4/Official_Comment×6/Meta_Review/Decision/Revision），或精确取 `GET /notes?invitation=<venueid>/Submission<number>/-/Official_Review`。
- **invitation 因会议而异，别硬编码——先查 venue group 拿真实段名**：`GET /groups?id=ICLR.cc/2024/Conference`（实测 HTTP 200），读 `content.submission_name.value`(实测 `Submission`)、`content.review_name.value`(实测 `Official_Review`)、`meta_review_name.value`(实测 `Meta_Review`)、`decision_name.value`(实测 `Decision`)，拼成 `<venueid>/Submission<n>/-/<review_name>`。（注：`/venues` 端点实测返回的是一条无关占位记录，**不能**用来枚举会议；用 group 端点。）
- **认证**：公开评审多数无需登录即可读；需要时 `openreview.api.OpenReviewClient(baseurl=..., username=..., password=...)`，内部 POST `/login` 拿 token 走 Bearer。
- **分页**：`offset`（默认 0）+ `limit`（单页上限通常 1000）。Python 客户端 `client.get_all_notes(invitation=...)` 自动翻页（其内部已按 per-submission 展开审稿），`get_notes(...)` 取单页。
- **审稿 Note 的内容字段**（v2 放在 `note.content[field].value`）：实测 ICLR 2024 一条 Official_Review 的 keys = `summary / soundness / presentation / contribution / strengths / weaknesses / questions / flag_for_ethics_review / rating / confidence / code_of_conduct`（rating 形如 `"3: reject, not good enough"`，confidence 形如 `"4: ..."`）——与 NeurIPS/ICLR 官方评审表对齐（见 tool 6）。
- 典型用法：批量拉投稿+directReplies → 过滤 Official_Review 统计 weakness 高频措辞和打分分布，校准"模式一"；同一 forum 的 Official_Comment 抽几组高质量 rebuttal 作话术模板。

【链接】
- 文档：https://docs.openreview.net/getting-started/using-the-api ；Notes 概念：https://docs.openreview.net/getting-started/using-the-api/objects-in-openreview/introduction-to-notes
- Python 库：https://pypi.org/project/openreview-py/ ；脚本示例：https://github.com/openreview/openreview-scripts
- 站点：https://openreview.net

【已知坑/局限】v1/v2 字段名与结构不一致，跨年份脚本要分别处理；不同会议的 invitation 命名和 content 字段不完全统一（rating 量纲、是否有 soundness 三项都因会而异），用前先抓一条样本看真实 key；只读公开数据，勿抓取/再分发受限内容。**最大坑已在上文标注：审稿用 per-submission invitation，venue 级 `.../Conference/-/Official_Review` 永远空。**

【实测记录（2026-06，Bash curl 直连 api2.openreview.net，无 key）】
- `GET /notes?invitation=ICLR.cc/2024/Conference/-/Official_Review` → HTTP 200，body `{"notes":[],"fromCache":true}`（**坏端点，空**）。
- legacy `GET https://api.openreview.net/notes?invitation=ICLR.cc/2024/Conference/-/Official_Review` → `{"notes":[],"count":0}`（同样空）。
- `GET /notes?invitation=ICLR.cc/2024/Conference/-/Submission&limit=1` → HTTP 200，返回投稿（`id=cXs5md5wAq`, `number=9504`, 带 `forum`）。
- `GET /notes?invitation=ICLR.cc/2024/Conference/Submission9504/-/Official_Review` → HTTP 200，`count=4`，content keys = summary/soundness/presentation/contribution/strengths/weaknesses/questions/flag_for_ethics_review/rating/confidence/code_of_conduct。
- `GET /notes?forum=cXs5md5wAq&details=directReplies` → 13 条 Note：7×Edit、1×Post_Submission、1×Submission、1×Decision、1×Meta_Review、6×Official_Comment、4×Official_Review、1×Rebuttal_Revision、1×Revision。
- `GET /notes?invitation=ICLR.cc/2024/Conference/-/Submission&details=directReplies&limit=1` → 投稿的 `details.directReplies` 含 4×Official_Review、1×Official_Comment、1×Meta_Review、1×Decision。
- `GET /groups?id=ICLR.cc/2024/Conference` → HTTP 200，`content.submission_name=Submission`、`review_name=Official_Review`、`meta_review_name=Meta_Review`、`decision_name=Decision`、`reviewers_name=Reviewers`。
- NeurIPS 2024 验证同一模式：venue 级 `NeurIPS.cc/2024/Conference/-/Submission` 可用，venue 级 `.../-/Official_Review` 返回 `{"notes":[]}`；group `review_name=Official_Review`。
- `GET /venues` → HTTP 200 但仅返回一条无关占位（`{"invitation":"Venue/-/Conference/Occurrence","year":"2012"}`），**不可用于枚举会议**；改用 `/groups?id=<venueid>`。

---

## 3. PRISM：评估 LLM 审稿质量的多维基准（arXiv 2605.26730）

【是什么】专门衡量"LLM 当审稿人写得好不好"的基准，把评审拆成 4 条可溯源的结构化评估管线。它定义了"好审稿"的客观维度，可直接当本技能模式一的自检 rubric，也解释了 LLM 审稿的系统性偏差。

【可复用方法 — 四维 + 失败模式】
- **维度1 分析深度 DoA**：把评审拆成论证单元(ADU)，分 Claim(论断) vs Premise(论据)；论据按 grounding 打分——0 空泛/套话、1 直接指向稿件具体处、2 引用更广文献。最终分 = 论据比例与 grounding 的调和平均。启示：**每个 weakness 都要带论据，且最好指到具体页/表/式或外部文献**，否则就是"深度的假象"(illusion of depth)。
- **维度2 新颖性评估**：novelty 判断必须能被可检索的前作支持或反驳（PRISM 用 Semantic Scholar 检索核验，[-2,+2] 打分）。启示：**说"不新颖"必须举出具体先行工作，不能空断**；这正是 LLM 最易"幻觉新颖性"的地方。
- **维度3 缺陷识别与优先级**：既看缺陷召回（关键 vs 次要），也看排序——用 NDCG 式 nCPS 衡量是否把致命方法学问题排在错别字之前。Critical=需补实验/改证明；Minor=编辑性可修。启示：**永远先抛唯一最重要的问题，别让格式问题稀释火力**。
- **维度4 多维建设性**：把评审拆成原子评论(ARC)，每条按 可执行性/具体性/有依据/给方案/语气 五项 0–2 打分。
- **已证实的 LLM 审稿通病（写模式一时要主动规避）**：①"表层陷阱"——过度纠结排版格式（某系统 24% 精力花在 formatting）；②论据比例低、只下论断不给证据；③新颖性幻觉；④次要缺陷的幻觉率高（某系统 18.5%）；⑤建设性/给解决方案弱于人类。结论：LLM 审稿是人类审稿的"定向补充"，单维度强但都有盲区。

【链接】https://huggingface.co/papers/2605.26730 （PRISM: A Multi-Dimensional Benchmark for Evaluating LLM Peer Reviewers）；语料覆盖 ICLR 2024–2026、ICML 2025、NeurIPS 2025。

【已知坑/局限】基准本身，不是即用工具；各维度需检索增强(Semantic Scholar)才能跑"新颖性核验"。提醒：本技能写模拟评审时应自查这 5 个通病。

---

## 4. grill-me / grill-with-docs（mattpocock skills）——"被拷问"式压力测试

【是什么】两个广传的 Claude 技能。grill-me 是通用生产力技能：对一个计划/设计/想法"逐问拷问直到与 AI 达成共识"；grill-with-docs 是其工程版，针对代码库一个 bounded context 做问答并产出 `context.md` 与 ADR。对本技能的价值：把"投稿前自我拷问 / rebuttal 预演"做成结构化逼问流程。

【可复用方法/提示策略】
- 核心提示原型："interview me relentlessly about every aspect of this plan until we reach a shared understanding"——**沿决策树逐分支提问，一次只解一个依赖**，而非泛泛而谈。
- 关键加速技巧：**每个问题 AI 先给出自己的推荐答案**，用户只需说"yes/调整"，把抽取式访谈变协作式。可直接用于"rebuttal 预演"：对每个审稿人可能追问，先替作者拟一个推荐回应。
- 若问题能靠读代码/读论文自己回答，就去查而不是问用户（移植：能从正文/实验里查到的，先查再问）。
- grill-with-docs 的 ADR 触发三条件可借用为"何时值得在 response letter 里专门解释一个设计决定"：**难以逆转 + 无背景会让人意外 + 是真实权衡的结果**。
- 一次 session 约 45 分钟、走完决策树即止——提示拷问要有终止条件（达成共识），不是无限追问。

【链接】https://github.com/mattpocock/skills （grill-me/SKILL.md、grill-with-docs）；作者说明 https://www.aihero.dev/my-grill-me-skill-has-gone-viral ；grill-with-docs 演进自已废弃的 ubiquitous-language，借鉴 DDD 的 bounded context。

【已知坑/局限】grill-me 是开放式访谈，无评分维度，需配 rubric（见 tool 1/3/6）才能用于正式评审；GitHub 原文在本环境被网络策略拦截，工作流细节取自作者博客与官方说明页，未能逐字核对 SKILL.md。

---

## 5. IJCAI/NeurIPS 类会议 rebuttal 规则 + Zenke Lab 期刊 response 模板

【是什么】两类一手返修规范：会议 rebuttal（强约束、限页、限时）与期刊 response letter（逐点、可附新结果）。本技能模式二必须区分这两种语境。

【可复用方法 — 会议 rebuttal（IJCAI 2025 FAQ，规则代表性强）】
- **rebuttal 的定位**：回答审稿人的"急迫问题"、指出会导致拒稿的事实性错误、申诉不道德评审——**不是与审稿人开启对话**。
- **该回才回**：只在(1)审稿人提了需澄清/与相关工作关系的急迫问题，(2)发现致命事实错误，(3)不道德评审(走机密通道，仅 AC/SAC/PC 可见) 时回应；别只为"不喜欢某句评语"而回。
- **硬约束**：通常**限 1 页**、用官方模板；**不得加新实验/新结果、不得给代码链接或上传新材料**（均算超出原稿）；可以放澄清性图/例（属于"解释稿件已有内容"）。
- **风格**：less is more，越短越crisp越能说服；四审全 reject 的论文基本翻不了案，不必硬写。
- **盲点**：勿情绪化、勿塞审稿人没要的新结果、勿超长。

【可复用方法 — 期刊 response letter（Zenke Lab LaTeX 模板）】
- **point-by-point 结构**：按审稿人分节(`\reviewersection` → Reviewer 1/2…)，每点自动编号 **P[审稿人].[点]**（P1.1、P2.1），支持 `\label/\ref` **跨点交叉引用**（在回 R2 时引用对 R1 的回应）。
- **视觉区分**：审稿意见用衬线体+粗体标签 `Reviewer Point P1.1`；作者回复用**无衬线体** + 粗体 `Reply:`，一眼区分"谁说的/怎么答的"。
- **推荐结构**：开头总致谢段 → 每审稿人一节(逐点 point/reply) → 节内 `Minor` 子节归并错别字等小问题（用 `\shortpoint/\shortreply` 一行式）。
- 用 `xr` + `\externaldocument{manuscript}` 引入正文的式号/节号，回复里精确指位。

【链接】IJCAI 2025 Rebuttal FAQ https://2025.ijcai.org/rebuttal-faq/ ；Zenke Lab 模板 https://zenkelab.org/resources/latex-rebuttal-response-to-reviewers-template/ （CC BY-SA 3.0）。

【已知坑/局限】会议 vs 期刊规则相反：会议常禁新实验、期刊鼓励补实验；务必按目标 venue 的具体征稿/返修说明再定策略，FAQ 仅代表一类会议。

---

## 6. NeurIPS/ICLR 官方评审表维度（模式一打分的权威锚点）

【是什么】顶会官方审稿表字段，是模拟评审"多维 + 打分"应直接对齐的金标准（本仓库 light-idea-critique/references.md 已逐字记录 NeurIPS 2024 表，本技能复用其字段）。

【可复用方法 — 真实字段】
- 文字维度：**Summary**（复述论文与贡献，作者应认可）/ **Strengths & Weaknesses** / **Questions**（作者回应能改变判断的问题）/ **Limitations**（含负面社会影响）/ **Ethical Concerns**。
- Strengths&Weaknesses 四子维：**Originality / Quality / Clarity / Significance**。
- 三个 1–4 分项：**Soundness / Presentation / Contribution**（4 excellent…1 poor）。
- **Overall 1–10**：10 award；9 very strong accept；8 strong accept；7 accept；6 weak accept；5 borderline accept；4 borderline reject；3 reject；2 strong reject；1 very strong reject。
- **Confidence 1–5**：5 核对过数学/绝对确定；3 较自信但可能没看懂某些部分；1 educated guess/非本领域。
- 用法：模拟审稿人给分时一并给 confidence，并对应到 OpenReview 抓到的真实分布做校准。

【链接】NeurIPS 评审表（公开评审可在 OpenReview 各年会议 reviewer guide 查），本仓库已记录于 ../light-idea-critique/references.md。

【已知坑/局限】不同会议量纲不同（ICLR rating 也是 1–10，但子维设置随年份变）；用前以 OpenReview 实抓的某条 review 为准。

---

## 7. Scholar Evaluation（ScholarEval 框架，本轮新核实）

【是什么】基于 ScholarEval（Moussa et al. 2025, arXiv:2510.16234）的检索增强论文/科研评估技能，评 soundness（方法相对已有文献的经验有效性）与 contribution。适用实证/理论/综述论文、研究提案、学位论文、会议摘要。可直接当模式一的"通用维度 rubric"。

【可复用方法 — 8 维 + 5 级 rubric + 6 步流程】
- **8 评估维度**：①问题界定与研究问题(清晰/意义/可行/新颖/范围) ②文献综述(全面/批判性综合而非罗列/识别 gap/时效/语境化) ③方法与设计(契合问题/严谨/可复现/透明/伦理/承认局限) ④数据与来源(质量/样本代表性/程序/可信度) ⑤分析与解释(方法契合/严谨/逻辑自洽/替代解释/结果与论断对齐) ⑥结果与发现(呈现清晰/统计或质性严谨/可视化/解释准确/启示) ⑦学术写作(组织/学术语气/语法/逻辑流/可读性) ⑧引用与参考(完整/来源质量/准确/视角平衡/规范)。
- **5 级评分**：5 出色(顶刊可发) / 4 强(小改) / 3 合格(有明显改进项) / 2 需改进(需大改) / 1 差(根本性问题)。可跨维加权平均。
- **6 步流程**：①界定范围(work 类型 + 评估深度：comprehensive/targeted/comparative) ②逐维评估 ③逐维打分(每维给 2–3 优点 + 2–3 改进点 + critical issues + 可选 1–5 分) ④综合(总体判断 + 3–5 主优点 + 3–5 关键弱点 + 按影响排序的建议 + 可发表度) ⑤可执行反馈(具体到章节/可操作/按影响排序/平衡/有据) ⑥按语境校准(早稿看结构、终稿全面查；期刊高严谨、会议看新颖+清晰、学生作品重发展性；STEM 重可复现+统计、社科重混合方法、人文重论证)。
- **反偏好原则**：评判依据 rubric 而非个人偏好；每个判断都从文本举证；弱点框成改进机会；非所有维度适用所有 work 类型(理论论文无"数据收集")。

【链接】ScholarEval 论文 https://arxiv.org/abs/2510.16234 ；技能 https://playbooks.com/skills/microck/ordinary-claude-skills/scholar-evaluation

【已知坑/局限】绝对分仅序数可解释；检索增强是核验 soundness/novelty 的前提，无检索时新颖性判断不可靠。

---

## 8. Scientific Critical Thinking（GRADE + Cochrane ROB，本轮新核实）

【是什么】把 GRADE（证据质量分级）与 Cochrane Risk of Bias 引入论文批判的技能，系统评证据强度与研究可信度。给模式一/魔鬼代言人提供"方法学攻击清单"。

【可复用方法 — 五块批判框架】
- **方法学(四种效度)**：内部效度(因果可信？查随机化/混杂控制/选择偏倚/失访)、外部效度(可推广？)、构念效度(测量真测到目标？)、统计结论效度(功效/假设/检验选择是否合理)。再加 控制/盲法充分性、测量质量(工具验证/信度/标准化)。
- **偏倚扫描(五类)**：认知偏倚(确认偏倚/HARKing/发表偏倚/挑樱桃)、选择偏倚(抽样/志愿者/失访/幸存者)、测量偏倚(观察者/回忆/社会赞许/工具)、分析偏倚(p-hacking/结局切换/选择性报告/亚组捕捞)、混杂(未测变量)。
- **统计 8 点清单**：样本量/功效(应有先验分析)、检验适当性+假设满足、多重比较校正、p 值解释(避免"显著=重要")、效应量+CI、缺失数据机制与处理、模型拟合/过拟合、常见陷阱(回归均值/Simpson 悖论)。
- **GRADE 应用**：从研究设计起步；**降级**因素=偏倚风险/不一致/间接性/不精确/发表偏倚；**升级**因素=大效应量/剂量-反应/混杂只会削弱效应。独立复现+多方法+多团队收敛=加强结论。
- **逻辑谬误 6 族**：因果(post hoc/相关当因果/反向因果)、归纳(草率概化/轶事/生态谬误)、权威来源(诉诸权威/人身攻击/起源谬误)、统计(基率忽视/德州神枪手/检察官谬误)、结构(假二分/移动球门/窃取论点)、科学特有(伽利略策略/诉诸无知/不可证伪)。标谬误时须命名+解释缺陷+指出"何种证据才能有效推断"。
- **逐条断言评估 6 步**：①辨断言类型(因果/关联/描述)及强度 ②证据直接/间接、是否够支撑该强度 ③数据与结论的逻辑连接 ④置信度与证据成比例 ⑤是否过度概化 ⑥红旗扫描(相关研究用因果语言/无视反证)。
- **核心原则**：永远区分"数据(观察到什么)"与"解释(意味什么)"；批评严苛度匹配对主结论的实际影响；不论结论是否合预期都用同一标准。

【链接】技能 https://playbooks.com/skills/kjgarza/marketplace-claude/scientific-critical-thinking ；GRADE handbook https://gdt.gradepro.org/app/handbook/handbook.html ；Cochrane RoB 2 https://methods.cochrane.org/risk-bias-2

【已知坑/局限】GRADE/ROB 源自临床/系统综述语境，迁移到 CS/工程论文时部分条目(剂量-反应)不适用；需按学科裁剪。

---

## 9. critique / audit 类技能（obra superpowers + 安全审计，本轮新核实）

【是什么】两类工程评审技能，其"严重度分级 + 闭环处置"机制可直接移植到论文评审与返修核验。

【可复用方法】
- **obra `requesting-code-review`（critique 范式）**：派独立子代理只看"描述+需求+diff 范围"而非对话历史，保证评审聚焦。
  - **三级严重度 + 处置规则**：Critical(立即修，先于一切)、Important(进入下一任务前修)、Minor(记下，不阻塞)。映射到论文：Critical=需补实验/改证明、Important=返修周期内必改、Minor=编辑性。
  - 评审者输出固定三段：**Strengths / Issues(按严重度分类) / Assessment(整体就绪判断)**。
  - 行为铁律：不因"看起来简单"就跳过评审；不忽略 Critical；带未修 Important 不得推进；**不同意反馈必须给技术理由/给出代码或测试证明，不能沉默忽略**——对应 response letter"不同意须带证据反驳，不能只写 disagree"。
  - 触发时机："review early, review often"——每完成一个单元就评审。移植：投稿前、每轮返修后都跑一次模拟评审。
- **安全审计技能（audit 范式，wrsmith108/claude-skill-security-auditor）**：可复用的"审计流水线 + 可溯源处置"骨架——发现 → 执行工具(结构化 JSON 输出而非抓文本) → 解析分类(严重度 + 直接/间接依赖) → 过滤(对照 risk-accepted 例外表) → 报告(摘要表+逐条+整改命令) → 退出码契约(0 干净/1 违规/2 工具错)。
  - **可过期的例外机制**：风险接受项带 `expires` 日期 + `approvedBy`，到期自动重新浮现——移植为"明确拒绝某条审稿意见"时须登记理由且可被复审重新审视（对应承诺账本的 `explicitly-rejected-with-rationale`）。

【链接】obra requesting-code-review https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md ；superpowers https://github.com/obra/superpowers ；安全审计 https://github.com/wrsmith108/claude-skill-security-auditor

【已知坑/局限】这些是工程语境技能，"diff/CVE/退出码"不直接对应论文；取其严重度分级与闭环处置的方法论，别照搬术语。

---

## 10. Academic Research Skills 的返修/反驳内部协议（本轮深挖，补充 tool 1）

【是什么】imbad0202/academic-research-skills（即 tool 1）的 Review→Re-review→Revise 阶段，含若干可直接移植的抗谄媚/可溯源机制。

【可复用方法】
- **Devil's Advocate 让步阈值协议**：DA 对每条 rebuttal 先打 1–5 分再回应；只有 ≥4（"用证据直击核心攻击"）才允许让步，≤3 则保持立场、重述原攻击；**禁止连续让步**、跟踪让步率；每个 checkpoint 后跑 frame-lock 检测。攻击强度不因用户反复施压而软化——"用户的坚持不算有效证据"。移植：写魔鬼代言人/模拟审稿时，对作者的辩解设"证据门槛"，避免被说服得太轻易。
- **Sprint Contract 两段式硬门**：评审者先 paper-blind 预提交打分计划(Phase 1)，再 paper-visible 打分(Phase 2)，阻止事后合理化。移植：模拟评审先定 rubric 与各维预期，再读论文打分，防止"看了结论倒推评语"。
- **R&R 可溯源矩阵**：re-review 输出加 "Author's Claim" + "Verified?" 两列，独立核验作者是否真的处理了每点。
- **承诺账本(Rebuttal Commitment Ledger)**：跟踪作者承诺改 vs 实际改了什么（灵感 Kong et al. 2026）。
- **分数轨迹协议**：跨返修轮跟踪每维 rubric 分差；delta < -3 触发强制 checkpoint（防越改越糟）。
- **7 模式 AI 失败清单(2.5/4.5 阶段阻断)**：实现 bug / 幻觉结果 / 走捷径 / bug 当洞见重框 / 方法学造假 / frame-lock / 引用幻觉。**引用幻觉 5 型**：TF 完全捏造 / PAC 部分准确 / IH 内插幻觉 / PH 似真幻觉 / SH 统计幻觉。
- **三索引三角核验引用**：Semantic Scholar(Tier 0，Levenshtein≥0.70 标题匹配) + OpenAlex(交叉索引) + Crossref(DOI 解析) + arXiv(无 key 存在性查)，按几个索引失配给出置信层级 k=0…3。移植：rebuttal 里新引的文献先过三索引核验，避免引用幻觉。

【链接】仓库 https://github.com/imbad0202/academic-research-skills （README 详述各阶段 schema/版本协议）

【已知坑/局限】协议繁多、token 开销大；多为该项目特定 schema，移植时取机制不取版本号。

---

## 11. 未能核实（本环境网络策略拦截，未取得可靠一手文本，不作事实引用）

本环境中 arxiv.org、neurips.cc、openreview.net、lobehub.com、mcpmarket.com、aiweekly.co 等域名被网络策略屏蔽，无法逐字读取以下目标的一手正文，故只列搜索所见、不臆造其内部协议：

- **verification-before-completion**（多仓库收录，如 oskar-dragon/superpowers、withzombies/hyperpowers、rileyhilliard/claude-essentials）：托管页本次 429/被拦，未能逐字读取清单。通用主旨可由搜索结果确认——**任务声称完成前必须用证据验证**（跑构建/测试、对比实际输出与声称，而非"读代码就说 done"），核心反模式是"过早宣称成功(false success claims)"。已折入 SKILL.md re-review 闭环：response letter 里每条"已修改"声称都要能跳到具体改动核验。
- **Peer Review skill / paper-reviewing / reviewer-2-simulator**：确认存在多个同类技能（curryfromuestc/academic-paper、jeandiable/academic-research、reviewer-2-simulator 等），但托管页本次 429/被拦，未能逐字提炼其内部 rubric。其评审维度共识（originality/soundness/significance/clarity，决定分 accept/minor/major/reject）已被 tool 1/6/7 的已核实材料完整覆盖，本技能以那些为准。
- **ICLR/NeurIPS 公开评审逐篇正文**：proceedings.neurips.cc 与 openreview 评审页本次被拦，未能逐字摘录单篇 review；但 OpenReview API（tool 2）取数方式与 NeurIPS 评审表字段（tool 6）已分别核实，足以指导实抓。

诚实声明：本轮真正读到一手/可靠转述并提炼的工具为 tool 1–10（tool 1 为既有笔记；tool 2–6 为前轮核实；tool 7–10 为本轮新增核实：Scholar Evaluation/ScholarEval、Scientific Critical Thinking、critique+audit 技能、Academic Research Skills 返修内部协议、grill-me 九大误用）。tool 11 所列为本环境未能逐字核实项，按要求如实标注，未编造端点或协议。
