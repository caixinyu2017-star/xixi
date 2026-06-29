# light-paper-drafting 参考工具研究笔记

本文件记录对论文初稿撰写相关工具/项目/框架的逐个调研。每个条目含【是什么】【可复用方法】【链接】【已知坑/局限】。研究时间：2026-06。

未能核实的工具单列在文末，绝不编造。

---

## 1. Scientific Writing skill (K-Dense claude-scientific-writer)

【是什么】一个开源的"深度研究 + 写作"工具，可作为 Claude Code 插件 / PyPI 包(`pip install scientific-writer`) / CLI 使用。生成可发表级别的科学论文、报告、海报、基金申请书、文献综述。MIT 许可。

【可复用方法】
- **先研究后写作**：写每段前先做文献检索（实时 lookup），确保每个 claim 有可核查来源，再落笔。这正对应本技能"审稿人读到这里会信吗"的原则。
- **数据驱动的 prompt 模式**：用户 prompt 中显式带上数据文件名 + 关键数字 + 显著性（如 `87% efficiency (p<0.001)`）+ 与文献基线对比，模型据此组织结果段。可借鉴为草稿阶段的"结果占位语法"。
- **19+ 子技能拆分**：`research-lookup`(实时文献)、`peer-review`(系统评审)、`citation-management`(BibTeX)、`scientific-schematics`(示意图)、`scientific-slides`、`latex-posters`、`hypothesis-generation` 等。说明论文流水线应按职能拆成可独立调用的模块。
- **ScholarEval 8 维评分**：peer-review 子技能用 8 维量化打分给反馈（见条目 9）。
- **文档转换**：用 MarkItDown 把 PDF/DOCX/PPTX/XLSX 转 Markdown 喂给模型（见条目 5）。
- **输出目录约定**：`writing_outputs/<timestamp>_<topic>/`，data/ 下图片自动归 figures/，便于版本管理。

【链接】https://github.com/K-Dense-AI/claude-scientific-writer ; https://pypi.org/project/scientific-writer/

【已知坑/局限】实时检索依赖 Perplexity Sonar Pro（经 OpenRouter，需 `OPENROUTER_API_KEY`）；图像生成依赖 Nano Banana Pro。核心写作需 `ANTHROPIC_API_KEY`。Python 限 3.10–3.12。免费版能力弱于其商业 k-dense.ai 平台。

---

## 2. Research-Paper-Writing-Skills / Academic Research Skills (ARS, Imbad0202/yian0625)

【是什么】Claude Code 的完整学术研究技能套件，覆盖 research → write → review → revise → finalize 全流程。强调 human-in-the-loop（"AI 是副驾不是主驾"）。CC BY-NC 4.0。当前 v3.5+。

【可复用方法 — 这是本技能最值得借鉴的来源】
- **10 阶段流水线 + 双类检查点**：1 RESEARCH → 2 WRITE → 2.5 INTEGRITY(诚信门) → 3 REVIEW → (修订辅导) → 4 REVISE → 3' RE-REVIEW → 4' RE-REVISE → 4.5 FINAL INTEGRITY → 5 FINALIZE → 6 PROCESS SUMMARY。每阶段结束都要用户确认。
- **2.5 / 4.5 诚信门的 7 类 AI 失败模式检查表**（源自 Lu et al. 2026 *Nature* "The AI Scientist"，见条目 6）——草稿自检必备清单：
  - M1 实现 bug 通过了 AI 自审
  - M2 幻觉引用（编造的参考文献）
  - M3 幻觉实验结果
  - M4 走捷径（shortcut reliance）
  - M5 把实现 bug 包装成"新洞察"
  - M6 方法学造假（methodology fabrication）
  - M7 早期阶段的框架锁死（frame-lock）
- **写作阶段产出物**：Paper Configuration Record、Outline、Argument Map(论证图)、Draft、Bilingual Abstract、Figures+Captions、Citation List。"先论证图后落笔"很值得吸收。
- **反泄漏协议(anti-leakage)**：没有来源支撑的内容必须标 `[MATERIAL GAP]`，不许凭空填充——对应本技能的 TODO 标记。
- **Material Passport（材料护照）**：记录每个数据/结果的出处与验证状态，贯穿全流程。
- **声称验证(claim verification)抽样**：评审前抽查 30%（至少 10 条）claim，终审查 100%。
- **多视角评审团**：EIC(主编) + R1 方法学 + R2 领域 + R3 跨学科 + Devil's Advocate，0–100 量化 rubric。Devil's Advocate 让步阈值：反驳打分 1–5，只有 ≥4 才让步（anti-sycophancy）。
- **score trajectory tracking**：修订后逐维度追踪分数，回退的维度会被标记，防止"改了 A 坏了 B"。
- **支持结构**：IMRaD / 主题综述 / 理论分析 / 案例研究 / 政策简报 / 会议论文。引用格式：APA7/Chicago/MLA/IEEE/Vancouver。
- **disclosure 模式**：按 venue(ICLR/NeurIPS/Nature/Science/ACL/EMNLP) 生成 AI 使用声明。

【链接】https://github.com/yian0625/Paper_writing_skill ; https://github.com/Imbad0202/academic-research-skills ; ARCHITECTURE.md 内含全 stage×skill×gate 矩阵。

【已知坑/局限】token 成本较高（15k 词论文约 $4–6）；data_access_level/repro_lock 是声明式标注，非运行时强制；LLM 输出非字节可复现，repro_lock 只是事后文档。

---

## 3. academic-paper-skills (lishix520, strategist + composer)

【是什么】面向哲学/跨学科论文的双技能框架：`strategist`(规划) + `composer`(写作)，带质量检查点。偏人文社科。

【可复用方法】
- **两技能分工**：Strategist 三阶段（平台分析→理论框架+gap 分析→大纲优化）；Composer 三阶段（基础+章节规划→系统写作带质检→润色+投稿准备）。
- **证据驱动的 gap 识别**：每个研究 gap 必须由 3–5 篇引用支撑。
- **平台风格学习**：分析 8–10 篇样本论文提取写作规范（句长、结构、术语）。
- **7 维 35 分审稿模拟系统** + 3 个验证门 + 2 个 Python 校验脚本(`evaluate_samples.py`、`gap_analysis.py`)。
- 支持 PhilArchive / arXiv / PhilSci-Archive / PsyArXiv 等预印本平台。

【链接】https://github.com/lishix520/academic-paper-skills

【已知坑/局限】定位人文社科，实验型 STEM 论文适配度有限；脚本需 Python 3.8+。

---

## 4. academic-writing-skills (bahayonghang) — 后期精修类

【是什么】专注论文"后期"：排版精修、格式校验、文献搜索验证、语法、de-AI 润色、实验叙事审查。明确"拒绝从零代写"，只提升既有文本。Claude Code/Codex。

【可复用方法】
- 子技能按格式拆：`latex-paper-en`、`latex-thesis-zh`(GB/T 7714)、`typst-paper`、`paper-audit`(reviewer 式诊断不改源)、`cover-letter`、`bib-search-citation`。
- **provenance 字段 ≠ 证明**：citation key/DOI/arXiv ID/URL 只是溯源字段，不等于该文真支撑了你的论点——核查时要点开看。
- **bib 搜索脚本**支持字段查询语法：`"mamba forecasting author:Cheng year>=2024 has:code"`，可同时输出 LaTeX + Typst 引用片段。
- 安全原则：不发明实验/引用/政策/无支撑声称。

【链接】https://github.com/bahayonghang/academic-writing-skills

【已知坑/局限】不做从零写作；在线核查为可选；推荐用强模型(Opus/GPT-5.5/Gemini 3 Pro)。

---

## 5. MarkItDown (microsoft)

【是什么】轻量 Python 工具，把各种文件转成对 LLM 友好的 Markdown（保留标题/列表/表格/链接结构）。由 AutoGen 团队出品。`pip install 'markitdown[all]'`。

【可复用方法 — 草稿阶段读资料/转材料用】
- 支持：PDF、PPTX、DOCX、XLSX/XLS、图片(EXIF+OCR)、音频(转写)、HTML、CSV/JSON/XML、ZIP(遍历)、EPUB、YouTube URL。
- CLI：`markitdown paper.pdf -o paper.md`，也支持管道 `cat x.pdf | markitdown`。
- Python：
  ```python
  from markitdown import MarkItDown
  md = MarkItDown()
  print(md.convert("paper.pdf").text_content)
  ```
- 按需装依赖：`markitdown[pdf,docx,pptx]`，省体积。
- **OCR/图像理解**：`markitdown-ocr` 插件用 LLM Vision 抽图中文字（传 `llm_client`/`llm_model`，如 OpenAI gpt-4o）；无 client 时静默跳过。
- **高质量云端**：Azure Content Understanding（`cu_endpoint`）支持音视频、结构化字段抽取(YAML front matter)、扫描件版面分析；`--use-cu`。
- 安全：以当前进程权限做 I/O，处理不可信输入时用最窄的 `convert_stream()`/`convert_local()`。

【链接】https://github.com/microsoft/markitdown ; https://pypi.org/project/markitdown/

【已知坑/局限】面向"文本分析消费"而非高保真人读转换；复杂表格/扫描 PDF 本地转换质量一般（需 Azure Doc Intelligence/CU）；需 Python ≥3.10。

---

## 6. AI-Researcher Writer Agent / The AI Scientist (Sakana, Lu et al.)

【是什么】首个端到端全自动科学发现框架：生成 idea → 写代码 → 跑实验 → 可视化 → 写整篇论文 → 跑模拟评审。每篇成本 <$15。其升级版论文 2026 年登上 *Nature*（ICLR 2025 workshop 盲审分 6.33 > 平均 4.87）。

【可复用方法】
- **模拟评审器(automated reviewer)**：基于 NeurIPS 审稿指南构建，对论文打分接近人类水平；可作为草稿"自评分"的范式。
- **paper write-up 流程**：先有实验结果与图，再按模板逐节填充，最后整体评审。
- **7 类失败模式**（其 Limitations 节，已被 ARS 提炼为诚信门清单，见条目 2 的 M1–M7）：实现 bug、幻觉结果、走捷径、bug 当洞察、方法造假、frame-lock、引用幻觉。写草稿时把这 7 条当"红线自查表"。

【链接】https://arxiv.org/abs/2408.06292 ; 代码 https://github.com/SakanaAI/AI-Scientist （Nature DOI s41586-026-10265-5 为**待核条目**，引用前须核验真实出处与卷页，勿当既成事实）

【已知坑/局限】全自动有上述失败模式，本技能采人在环路；模拟评审与真实审稿仍有差距。

### 关联：HKUDS/AI-Researcher（另一同名项目）
端到端自主研究：文献综述→idea 生成→算法设计实现→验证精化→结果分析→manuscript 生成。两级输入：L1 详细 idea 描述；L2 给参考论文让其自己想 idea。NeurIPS 2025 Spotlight。
链接：https://github.com/HKUDS/AI-Researcher

---

## 7. Paper Writing Agent / PaperOrchestra (Google, Song et al. 2026)

【是什么】多智能体自动论文写作框架，把无结构的 pre-writing 材料转成可投稿的 LaTeX 稿，含文献综述合成与生成的图（plots + 概念图）。提出 PaperWritingBench（200 篇顶会论文逆向出的原始材料基准）。

【可复用方法】
- **不与特定实验管线硬耦合**：接受"非约束的预写材料"，比旧式自动写作器灵活。
- **文献综述质量**是胜负手：人评中文献综述质量胜率领先基线 50%–68%，整体稿件 14%–38%。提示草稿阶段要重投入综述合成。
- ARS v3.3 从它借鉴：Semantic Scholar API 验证、anti-leakage 协议、VLM 图表验证、score trajectory tracking。

【链接】（arXiv 2604.05018 / PaperOrchestra 为**待核条目**：编号与出处未经核验，引用前须 curl 实测记 HTTP 码确认存在，核不到不得当既成事实写入）

【已知坑/局限】基准与评测仍偏 AI 会议论文；自动生成图的正确性需 VLM 复核。

---

## 8. Paperzilla

【是什么】持续更新的"研究论文 feed"服务：监控论文源 + 接收转发的 alert + 按你的研究主题做相关性过滤排序。面向研究者/团队/AI agent。免费层。

【可复用方法】
- 直接监控源：arXiv、bioRxiv、medRxiv、ChemRxiv、ChinaXiv（可按需加源）。
- 可转发 Google Scholar 等 alert 邮件作为输入，做相关性过滤（比 Scholar alert 更聚焦）。
- 输出渠道：站内 feed、日/周邮件摘要、RSS/Atom、**MCP server**、**CLI**。AI agent 可经 MCP/CLI 消费相关性过滤后的研究上下文——可作为"写作时补最新文献"的数据源。

【链接】https://paperzilla.ai/ ; docs https://docs.paperzilla.ai/

【已知坑/局限】公开文档较薄；具体 API/端点未在公开页明示（MCP/CLI 接入细节需登录查），故端点未核实，不臆造。

---

## 9. ScholarEval / scholar-evaluation（8 维评审框架）

【是什么】LLM 论文评审框架，给草稿/手稿做量化评分反馈。被 K-Dense scientific-writer 的 peer-review 子技能采用（"8-dimension scoring"）。学界另有 CNPE(Comparison-Native Paper Evaluation, ACL 2026 Findings) 指出"绝对打分易拟合 venue 特定规则"，主张改用成对比较排序。

【可复用方法 — 模块自检维度清单】综合公开版本的 8 个评审维度通常含：
1. Novelty / Originality（创新性）
2. Significance / Impact（意义与影响）
3. Soundness / Methodology（方法严谨性）
4. Clarity（清晰度/写作质量）
5. Reproducibility（可复现性）
6. Evidence / Experimental support（实验/证据支撑）
7. Related work / Positioning（与已有工作的定位）
8. Ethics / Limitations（伦理与局限诚实度）
每维给分并指出具体可改处，对应本技能"模拟审稿"自检。

【链接】各 scholar-evaluation 技能聚合 https://lobehub.com/skills/oimiragieo-agent-studio-scholar-evaluation （CNPE arXiv 2603.17588 / "ACL 2026 Findings" 为**待核条目**，编号与会议出处未核验，勿当既成事实引用）

【已知坑/局限】绝对打分跨 venue 漂移大（CNPE 指出），用作相对自检比绝对分更可靠；维度命名各实现略有差异。

---

## 10. Open Notebook (lfnovo)

【是什么】开源、隐私优先、100% 本地可跑的 NotebookLM 替代品。组织多模态资料(PDF/视频/音频/网页)，全文+向量检索，与资料对话，生成播客。MIT。支持 18+ 模型提供商(OpenAI/Anthropic/Ollama/LM Studio…)。

【可复用方法】
- 写作前的"资料库 + RAG"层：把参考文献入库，做向量检索 + 与上下文对话，为引言/相关工作提供有出处的素材。
- 多语言 UI（含简繁中文）；可全本地，适合敏感/未发表数据。

【链接】https://github.com/lfnovo/open-notebook ; https://www.open-notebook.ai

【已知坑/局限】本质是知识管理/检索工具，不产出论文级结构化稿件；需自建模型 key/本地模型。

---

## 11. writing-plans skill (obra/superpowers)

【是什么】写"实现计划文档"的 Claude 技能（面向多步任务，落地前先写计划）。其方法论可迁移到论文写作的"先大纲后落笔"。

【可复用方法】
- **计划文档头部模板**：Goal(一句话) + Architecture(2–3 句) + Tech Stack。论文版可对应：核心论点 + 结构思路 + 目标 venue。
- **bite-sized 任务粒度**：每步 2–5 分钟一个动作（写失败测试→跑→实现→跑→commit）。论文版：每节拆成"列要点→写一段→自检→标 TODO"。
- **先映射文件结构再定任务**：每个文件单一职责，一起变的放一起。论文版：先定每节承担的论证职责再动笔。
- 计划存 `docs/.../plans/YYYY-MM-DD-<name>.md`，步骤用 `- [ ]` 复选框便于追踪。

【链接】https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md

【已知坑/局限】原生面向软件实现，迁移到论文需把"测试/commit"换成"自检/版本快照"。

---

## 12. distill skill / Distill.pub 写作规范

【是什么】Distill 是致力于让 ML 研究"清晰且动态"的期刊与 web 框架，强调交互式可解释文章。其作者指南给出科学传播的硬规范。

【可复用方法】
- **数字内联引用 + hover 详情**：引用密集时用编号 `[1]` 内联、悬停显示详情提升可读性；正文讨论时仍点名作者姓氏（对作者友好）。
- **BibTeX 为引用唯一来源**：`<script type="text/bibliography">` 或外部 `bibliography.bib`；强烈建议填 `url` 字段以便给引用加链接。脚注用 `<dt-fn>`，编号自动。
- **公式用 MathJax/KaTeX**。
- 交互式文章原则（Communicating with Interactive Articles）：减少认知负荷、连接多种表征（文字↔图）、用动画/交互让读者主动探索。草稿阶段虽不做交互，但"图文表征对齐、降低读者负担"的取向可吸收。
- 透明/可复现/清晰/易记是其核心价值取向。

【链接】https://distill.pub/guide/ ; https://distill.pub/2020/communicating-with-interactive-articles/

【已知坑/局限】Distill 已停刊(2021)，框架仍可用；面向 web 交互文，传统 PDF 论文只能借鉴其传播理念，不能照搬组件。

---

## 13. content-strategy skill

【是什么】把内容当"系统/产品"而非单篇来运营的 Claude 技能/persona（topic cluster、编辑日历、分发）。本为营销内容，但其"结构胜过才华"理念可迁移。

【可复用方法】
- **brief 先行**："平庸写手 + 好 brief > 好写手 + 无方向"。论文版：每节先写明确 brief（要论证什么、用哪些证据、对标哪篇）再写。
- **cluster 思维**：先定主线(pillar)再展开子节，内部互链。论文版：贡献清单(pillar) → 各节服务于它。
- **每段都要有"为什么存在"**：内容无理由不写。论文版：每段自问"删了论证还成立吗"。
- /content:brief 产出含：大纲、目标字数、内部链接、要超越的对标内容——可借为节级写作 brief 模板。

【链接】https://github.com/alirezarezvani/claude-skills/blob/main/agents/personas/content-strategist.md ; https://coldiq.com/skills/content-strategy

【已知坑/局限】源自 SEO/营销，KPI(流量/转化)不适用学术；只取其"结构化、brief 驱动、每单元须有理由"方法论。

---

## 14. Venue Templates / Overleaf Templates

【是什么】各 venue 的官方 LaTeX 模板与 Overleaf 模板库，决定论文结构套路与排版约束。

【可复用方法 — 草稿阶段对齐结构】
- **IEEE**：官方会议/期刊模板（`IEEEtran` 类），见 ieee.org/conferences/publishing/templates；Overleaf `ieee-official` 标签库。
- **NeurIPS**：`neurips_2024.sty`（每年更新年号），正文页数上限+附录规则；neurips.cc StyleFiles 与 Overleaf NeurIPS 模板。
- **ACL/EMNLP**：`acl.sty`(ACL Rolling Review)。
- **Nature/Science**：投稿初期常用 Word/特定结构(无严格 LaTeX 类)，结构=摘要+正文(限字)+方法+扩展数据。
- Overleaf 按标签浏览：`conference-paper` / `academic-journal` / `ieee-official`。
- 草稿阶段从模板抽**结构套路**（节序、字数/页数上限、图表规范）而非照抄内容；正式排版交给 typesetting(m12)。

【链接】https://www.ieee.org/conferences/publishing/templates ; https://www.overleaf.com/gallery/tagged/ieee-official ; https://neurips.cc 与 Overleaf NeurIPS 模板 ; https://www.overleaf.com/gallery/tagged/conference-paper

【已知坑/局限】模板年号/规则逐年变，投稿前务必取目标年份当年版本；页数/匿名(双盲)规则因 venue 而异。

---

## 15. 期刊句式方法论（按语义功能采集，只记结构不搬句）

【是什么】学术写作有稳定的"语步（move）+ 句式骨架"。母语写作者靠读够多论文形成肌肉记忆，非母语/新手则常卡在"知道要说什么、不知道用什么句式说"。Writefull Sentence Palette、Academic Phrasebank（曼大）走的就是"按写作功能给句式骨架"的思路。本节给**采集与使用方法论**，不内置成品句库（句库会过时、且有抄袭风险）。

【按语义功能归类（采集时的分类轴）】
采集目标期刊真实句式时，按**写作功能**而非主题归档，常用功能桶：
- **背景引入**：领域重要性、研究脉络起手（"Recent advances in X have… / X has emerged as…" 类骨架）。
- **缺口陈述**：指出前人不足、引出本文动机（"However, … remains underexplored / little attention has been paid to…"）。
- **方法宣告**：声明本文做法（"We propose / In this work, we…"）。
- **结果陈述与让步**：报告发现并诚实让步（"… outperforms … by X%, although …"）——让步句式是非母语写作弱项，重点采。
- **局限承认**：discussion 里坦陈边界（"One limitation is… / These findings should be interpreted with caution because…"）。
- 其他：图表指引、对比转折、因果归因、未来工作。

【采集方法（可操作）】
1. 选 3-5 篇**目标期刊近年高质量论文**（同子领域、同文章类型）。
2. 逐篇按上面功能桶**标注句式骨架**——抽出"功能词 + 句法结构"，把领域名词挖空成占位符（如 `[方法] achieves [指标] on [数据集], outperforming [baseline] by [幅度]`）。
3. 同一功能下汇集多个骨架，比较其语气强度（强主张 vs 保守），按目标刊调性选用。

【双红线（硬约束）】
- **只记结构，不整句搬运**：采集的是"挖空占位符的句法骨架"，不是原句。整句或长片段照搬=抄袭（即便改几个词，连续 ≥ 一定词数的雷同仍会被 Turnitin 类工具命中，见 light-research-ethics「离线自查重」>40 词红旗）。
- **版权**：他人论文受版权，句库供**学习句法**用，不得成段复制其表达。生成正文时用自己的话填占位符，写完过 m08/a08 自审 + light-citation 查重。

【链接】Academic Phrasebank（曼彻斯特大学，公开）https://www.phrasebank.manchester.ac.uk/ ；Writefull Sentence Palette（产品页）https://www.writefull.com/

【已知坑/局限】句式骨架有领域/期刊调性差异（CS 直接、生医保守），跨领域套用会水土不服；保守与强主张的边界按目标刊与审稿文化定；句库只解决"怎么说"，不解决"说得对不对"（内容真实性仍归 a10/自审）。

---

## 未能核实的工具

- **PACSOMATIC**：多次检索(含 "PACS-O-MATIC" 变体)未找到可靠的公开文档/仓库/论文。检索结果均为通用"研究论文结构/大纲"教学页，与一个名为 PACSOMATIC 的具体工具无法对应。**故不收录其功能/端点，避免编造。** 若指的是某内部/小众工具，需用户提供链接再补。

