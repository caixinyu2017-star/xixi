# light-research-ethics 参考工具研究笔记

逐个研究的科研伦理/合规/扫描工具与规范。每条含【是什么】【可复用方法/真实端点/参数】【链接】【已知坑/局限】。
研究日期：2026-06。带 ⚠️ 的为部分未能完整核实，已如实标注。

---

## COPE Guidelines（Committee on Publication Ethics）

【是什么】出版伦理领域权威组织，提供 Core Practices（核心实践）与一套 Flowcharts（决策流程图），是期刊编辑处理学术不端的事实标准。

【可复用方法】
- Core Practices 十大类，可直接用作审查维度清单：Allegations of misconduct（不端指控）、Authorship & contributorship（署名）、Complaints & appeals（投诉申诉）、Conflicts of interest（利益冲突）、Data & reproducibility（数据与可复现）、Ethical oversight（伦理监督）、Intellectual property（知识产权）、Journal management、Peer review processes、Post-publication discussions & corrections（更正/撤稿）。
- Flowcharts 是"遇到 X 情形怎么一步步处理"的决策树，覆盖：抄袭（已发表/投稿中）、图片重复或操纵、数据造假/伪造、署名争议、利益冲突未披露、同行评审操纵（systematic manipulation of peer review）、机构被期刊联系时如何调查等。审查产出时可对照对应 flowchart 给"下一步该找谁/怎么处理"。

【链接】
- Core practices: https://publicationethics.org/core-practices/
- 全套 flowcharts（英文）: https://publicationethics.org/resources/flowcharts/complete-set-english
- Elsevier PERK（把 COPE 类决策树落地为编辑工具包）: https://www.elsevier.com/editor/perk

【已知坑】publicationethics.org 对自动抓取返回 403，需人工浏览。Flowcharts 面向"编辑视角"，作者自审时要转换语境。

---

## ICMJE Recommendations（国际医学期刊编辑委员会）

【是什么】"Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals"，最权威的署名与投稿伦理标准，被大量期刊采纳（不限医学）。

【可复用方法 — 署名四条标准，必须同时满足全部四条】
1. 对研究构思/设计，或数据获取/分析/解释有 substantial contribution；
2. 起草或对重要智力内容做 critical review；
3. 对最终发表版本 final approval；
4. 同意对工作整体 accountable（保证准确性/完整性问题被恰当调查解决）。
仅满足部分 → 列入致谢（acknowledgement），不得署名。

【不构成署名的活动】仅获取资助、仅一般性监督/行政支持、仅写作/语言/校对协助。
【AI 政策】LLM/聊天机器人不得列为作者（无法对准确性/完整性负责）；须在投稿时披露 AI 使用——写作辅助写入致谢，数据/分析/作图用途写入方法部分；作者对 AI 产出负全责并须检查抄袭与偏差。
【通讯作者】负责全程沟通，发表后须可回应质疑。

【链接】https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html

【已知坑】四条标准对"只提供数据/只做实验"的人偏严，学界有争议；非医学领域可作参考但需结合学科惯例。

---

## CRediT taxonomy（贡献者角色分类）

【是什么】ANSI/NISO Z39.104-2022 标准，14 个标准化贡献角色，用结构化词表替代笼统署名。CC-BY 4.0 许可，可自由复用。

【可复用方法 — 14 个角色，逐人勾选并可标 lead/equal/supporting】
Conceptualization、Data curation、Formal analysis、Funding acquisition、Investigation、Methodology、Project administration、Resources、Software、Supervision、Validation、Visualization、Writing – original draft、Writing – review & editing。
用法：为每位作者生成贡献声明（如"张三：Conceptualization, Methodology, Writing – original draft"）。出版商常在 JATS XML 文章元数据中编码 CRediT 角色（页面本身未详述具体 schema ⚠️）。

【链接】https://credit.niso.org/

【已知坑】不解决署名顺序与"谁是第一/通讯作者"，需与 ICMJE 四条标准配合判断"够不够署名"。

---

## ORI Research Misconduct（美国研究诚信办公室 / 42 CFR Part 93）

【是什么】美国联邦层面对"研究不端"的统一定义（2000 年通过，2001 生效），即 FFP。

【可复用方法 — 定义与认定要件】
- Fabrication（伪造）：编造数据或结果并记录/报告。
- Falsification（篡改）：操纵材料/设备/过程，或更改/遗漏数据使研究记录失真。
- Plagiarism（抄袭）：挪用他人想法/过程/结果/文字而未恰当署源。
- 认定需同时满足三要件：① significant departure 显著偏离学界惯例；② 故意/明知/轻率（intentionally, knowingly, or recklessly）；③ preponderance of evidence 优势证据。
- 明确排除：honest error（诚实错误）与 differences of opinion（学术分歧）。
- 注意：联邦定义已删去旧的"other serious deviations"宽泛条款（因过于模糊）。审查措辞应紧扣 FFP，不把诚实失误等同不端。

【链接】研究综述（FFP 定义与各机构落地差异）: https://pmc.ncbi.nlm.nih.gov/articles/PMC4269469/

【已知坑】这是美国标准；中国/欧盟科研不端口径不完全一致，跨境项目需对应本地规定。

---

## Retraction Watch（撤稿数据库，已并入 Crossref）

【是什么】最大的撤稿追踪数据库，2023 起完全开放，并接入 Crossref。可用于核查参考文献是否已被撤稿。

【可复用方法 — 真实端点/数据】
- 免费 CSV（每个工作日更新，含撤稿原因）: https://gitlab.com/crossref/retraction-watch-data
- 查所有撤稿（Crossref REST API filter）：`https://api.crossref.org/v1/works?filter=update-type:retraction`
- 查单篇 DOI：`https://api.crossref.org/v1/works/<DOI>`
- 返回 `update-to[]` 每项含字段：`DOI`、`type`（如 retraction）、`source`（publisher 或 retraction-watch）、`label`（如 "Retraction"）、`record-id`（指回 CSV 行获取撤稿原因）、`updated`（日期）。
- 实用流程：拿到参考文献 DOI 列表 → 批量查 Crossref → 命中 update-type:retraction 即标红警示。

【链接】
- Crossref 公告: https://www.crossref.org/blog/retraction-watch-retractions-now-in-the-crossref-api
- 用户指南: https://retractionwatch.com/retraction-watch-database-user-guide/

【已知坑】同一撤稿可能来自 publisher 与 retraction-watch 多个 source 重复出现；API 不含撤稿原因，需用 record-id 回查 CSV。引用其元数据发表时 Crossref 要求注明出处。

---

## Turnitin / 相似度检查

【是什么】主流文本相似度（"原创性"）与 AI 写作检测服务，比对期刊、网页与历史学生作业库。

【可复用方法 / 解读要点】
- Similarity Report 给相似百分比并高亮匹配来源。关键原则：**文本匹配≠抄袭**，匹配高也可能是正常引用；匹配为零也不证明无不端。
- 封面/标题、带引号的引文、参考文献列表通常会被高亮，属正常匹配，可在设置中排除（exclude quotes / bibliography / small matches）。真正风险信号是"大段未加引号且未高亮"的文本。
- 审查复用：把"相似度分数"当线索而非判决，逐条看匹配来源与上下文。
- AI 写作检测（**厂商自报数字**，源自 Turnitin 官方博客/发布说明，非独立第三方评测；链接已核实可达）：
  - **文档级误报率 <1%**（人写文档被误判为 AI 的比例）。
  - **句子级误报率约 4%**，明显更高。
  - 因此 Turnitin 设了安全阈值：**整篇 AI 占比低于 20% 时不出 AI 指标/不标红**，专为降低低分文档的误指控。
  - 官方一再强调：AI 分数是"对话起点"而非定罪依据，不应作为学术不端裁定的唯一证据，须人工复核 + 与作者沟通。
- 实务提醒：上述数字是**厂商自报、利益相关方**，且主要源自 2023 年发布说明；模型已多次更新，引用前回查 Turnitin Guides 最新页。公开研究与多校反映 AI 检测器对非母语英语写作误报偏高，独立评测的误报率常高于厂商自报值——对外引用时务必注明"厂商自报"性质，勿当客观基准。

【链接】
- 句子级误报率官方说明: https://www.turnitin.com/blog/understanding-the-false-positive-rate-for-sentences-of-our-ai-writing-detection-capability
- 文档级误报与安全阈值说明: https://www.turnitin.com/blog/understanding-false-positives-within-our-ai-writing-detection-capabilities
- AI 检测模型指南（最新行为以此为准）: https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model
- 相似度报告解读（UWA 图书馆指南）: https://guides.library.uwa.edu.au/textmatching

【已知坑】闭源、需机构订阅；句子级误报率（~4%）远高于文档级，单句标红不可靠；不要把相似度百分比当作"抄袭率"对外宣称；AI 检测对非母语写作误报偏高。

### 离线自查重（本技能落地 · scripts/text_overlap.py）

【范围】Turnitin 本体闭源、需订阅、比对其私有期刊/网页/历史学生库——无法复刻。但"本地自查重"（自我抄袭 / 重复发表 / 与某特定源文本比对）可做且原 references 缺失，故补此脚本。纯 Python 标准库（difflib），无第三方依赖。

【方法】文本归一化（小写 + 去标点 `\w+` + 折叠空白）→ 词级处理 → `difflib.SequenceMatcher.get_matching_blocks` 找"最长逐字连续重合片段"（比纯 n-gram 更精确命中"连续 >N 词逐字相同"红旗），同时算整体重合比例（词重合率 / Jaccard）。输出最长逐字重合（词数 + 原文 + 两份文件行定位）、重合比例、超阈片段计数。参数：`--min-run`（默认 40 词，对应 risk_checklist 红旗，命中标 🛑）、`--exclude-refs`（丢弃 References/参考文献 标题之后内容避免书目误报）、`--json`、`--selftest`（离线自测）。

【局限（守诚实原则，引用时必带）】
- 本地只比对**用户提供的文本**，不含 Turnitin 的期刊/网页/学生库。
- 仅用于**自我抄袭与重复文本筛查**，不得对外宣称"抄袭率 / 相似度 %"。
- 清结果只代表"在所给语料内未见重合"，**不是**保证无抄袭。

---

## ScanCode Toolkit（开源许可/版权扫描）

【是什么】AboutCode 维护的开源代码扫描器，检测许可证、版权、依赖与包元数据，是同类 SCA 工具的参考实现。

【可复用方法 — 真实 CLI】
- 核心命令 `scancode`，关键选项：`--license`（许可检测）、`--copyright`（版权）、`--package`（包清单/依赖）、`-i`/输入路径。
- 输出格式：`--json-pp out.json`、`--spdx-tv out.spdx`、`--csv`、HTML、CycloneDX（SBOM）；支持 Jinja 自定义模板。
- 典型用法：`scancode --license --copyright --package /path/to/code --json-pp output.json`
- 许可检测引擎用全文 diff 比对（非正则/概率/编辑距离），准确度高；提供 License Clarity Score 评估"许可声明是否清晰"。
- ScanCode.io 是配套服务端/CI 应用，支持脚本化扫描 pipeline，适合嵌入 CI/CD 做持续合规。

【链接】
- 仓库: https://github.com/aboutcode-org/scancode-toolkit
- 文档: https://scancode-toolkit.readthedocs.io/
- ScanCode.io: https://scancodeio.readthedocs.io/

【已知坑】偶有误报（如把某些文件误判为 proprietary-license）；侧重许可/版权/SBOM，漏洞检测能力弱（漏洞应配合 Snyk 等）。

---

## Snyk（依赖漏洞/SCA 扫描）

【是什么】商业化为主的安全平台，扫描开源依赖漏洞、代码（SAST）、容器、IaC，并支持许可策略检查。

【可复用方法 — CLI 命令】
- `snyk test`：本地扫描依赖已知漏洞并报告，**不**上传平台。
- `snyk monitor`：上传依赖快照到平台做持续监控，新漏洞披露时告警。
- `snyk code test`：源码静态分析（SAST）。
- `snyk container test`：扫描镜像内 OS 包与应用依赖漏洞。
- `snyk iac test`：扫描 Terraform/CloudFormation/K8s 等配置错误。
- 认证：`snyk auth`（浏览器登录）或 CI 中设置环境变量 `SNYK_TOKEN`。
- 常用选项：`--severity-threshold=<low|medium|high|critical>`、`--json`、`--sarif`、`--all-projects`（monorepo）、`--org=<id>`、`--project-name`。
- 除漏洞外可做开源许可策略扫描（标记不合规许可）。

【链接】
- CLI 文档: https://docs.snyk.io/snyk-cli
- 仓库: https://github.com/snyk/cli

【已知坑】官方 docs URL 结构变动频繁（部分页面 404，以 docs.snyk.io 现行为准）；免费额度有限，深度功能需付费；偏漏洞，许可/版权清单不如 ScanCode 细。

---

## Socket.dev（供应链恶意包检测）

【是什么】专注开源供应链攻击防护，靠"深度包行为分析"在恶意包执行前拦截，而非仅比对 CVE 数据库。

【可复用方法】
- Socket Firewall Free（`sfw`）：在安装命令前加前缀，如 `sfw uv pip install flask` / `sfw npm install <pkg>`。原理是起一个临时 HTTP 代理拦截子进程的 registry 流量，安装前向 Socket API 查安全性，阻断恶意的顶层与传递依赖。
- 行为信号（可直接当"可疑包"审查维度）：install scripts（安装期执行代码）、network access（异常外联）、filesystem 操作（读写敏感路径）、shell access（spawn 子进程/执行命令）、obfuscation（混淆/编码代码）、typosquatting（仿名包）。
- 两层判定：AI 扫描出嫌疑先告警，经人工复核确认恶意后才网络拦截（降低误报）。
- 支持生态：免费版覆盖 JS/TS（npm/yarn/pnpm）、Python（pip/uv）、Rust（cargo）；企业版扩展更多生态、自定义 registry、阻断未扫描包、allow list。也有 GitHub App 做 PR 级检查。

【链接】
- 官网: https://socket.dev
- 文档: https://docs.socket.dev

【已知坑】网络层拦截不查本地缓存命中（建议先清缓存）；免费版采集匿名遥测（机器 ID、被阻断包、GitHub org 名）；Firewall Free 用 PolyForm Shield 许可（非标准 OSI 开源）。

---

## Creative Commons License Chooser（CC 许可选择器）

【是什么】官方向导式工具，按问题帮创作者选 CC 许可并生成署名标记。不存储输入信息。

【可复用方法 — 4 个决策问题 → 许可】
1. 要求署名？2. 允许商业使用？3. 允许改编/二次创作？4. 改编是否须同条款共享（ShareAlike）？
- 6 种 CC 4.0 许可 + CC0：CC BY、CC BY-SA、CC BY-NC、CC BY-NC-SA、CC BY-ND、CC BY-NC-ND；CC0（放弃全部权利，进入公共领域）。
- 要素含义：BY=署名、NC=仅非商业、SA=相同方式共享、ND=禁止改编。
- 输出三种标记格式：HTML（网页）、Rich Text（文档）、Plain Text（印刷/演示的版权页或片尾），可填标题/作者/链接/年份自动生成署名。

【关键提醒（审查时引用）】CC 许可一经授予**不可撤销**；CC **不建议**用于软件/硬件（应用自由软件许可）；已属公共领域的作品用 Public Domain Mark 而非 CC。

【链接】https://creativecommons.org/chooser/

【已知坑】NC（非商业）定义在边界场景常有歧义；选 SA 会传染下游改编作品的许可条款，需提醒使用者。

---

## IRB ethics checklist（机构伦理审查 / Common Rule 45 CFR 46）

【是什么】涉人体研究的伦理审查框架。美国以 Common Rule（45 CFR 46）为核心，对应中国的伦理委员会审查。

【可复用方法 — 三级审查 + 批准标准】
- 三级审查：Exempt（豁免，最低风险的特定类别）、Expedited（快速，不超过最小风险且属特定类别，由主席或指定委员单独审）、Full Board（全体委员会，涉大于最小风险或脆弱人群）。
- 45 CFR 46.111 批准标准（审查清单）：① 风险最小化；② 风险/受益比合理；③ 受试者选择公平（equitable selection）；④ 征求知情同意；⑤ 知情同意有记录/文档；⑥ 必要时有数据安全监测；⑦ 隐私与保密保护；⑧ 对脆弱人群有额外保障。
- 知情同意要素（46.116）：研究目的/时长/程序、风险、受益、替代方案、保密安排、补偿、联系方式、自愿参与且可随时退出；2018 修订版还要求开头放"key information"摘要让受试者先抓住要点。上述 46.111 八项与 46.116 要素已由多家法律解读源交叉核实；⚠️ ecfr.gov / cornell / hhs.gov 政府原文页在本环境被网络策略阻断，未能逐字抓取，引用具体条文措辞时应回查官方原文。

【链接（供回查）】
- 45 CFR 46.111: https://www.ecfr.gov/current/title-45/section-46.111
- 45 CFR 46.116（知情同意）: https://www.ecfr.gov/current/title-45/section-46.116
- OHRP 培训（IRB 审查）: https://www.hhs.gov/ohrp/education-and-outreach/online-education/human-research-protection-training/

【已知坑】各机构对"豁免/快速"的本地落地不一；中国伦理审查（如《涉及人的生命科学和医学研究伦理审查办法》）口径与美国不同，跨境项目须按当地走。

---

## ISO 13485（医疗器械质量管理体系）

【是什么】ISO 13485:2016，面向医疗器械设计/生产/安装/服务的 QMS 标准。仅在科研产出涉及医疗器械软硬件时相关。

【可复用方法 — 关键条款（Clauses 4–8）】
- 风险导向：风险管理贯穿设计、生产、上市后全过程。
- 设计开发控制：结构化、可文档化的开发过程（计划、输入、输出、评审、验证、确认、转移、变更控制）。
- 文档与记录控制：质量手册、受控程序、医疗器械文档、作为符合性客观证据的记录。
- CAPA：纠正措施针对已发生不符合的根因，预防措施针对潜在问题。
- 管理职责：质量方针、资源、角色、管理评审。
- 与 ISO 9001（10 章，通用）相比为 8 章、更规定性；FDA 的 QMSR 终规（2024 年 2 月发布，**2026 年 2 月 2 日正式生效**）已将 ISO 13485:2016 incorporate by reference，取代/改写 21 CFR 820，两者趋同（已核实，多家律所确认生效）。是 MDSAP、CE 标记的基础。

【链接】https://simplerqms.com/iso-13485-quality-management-system/ ；标准本体需向 ISO/认证机构购买。

【已知坑】标准全文需付费购买；认证需第三方审核（两阶段审核 + 每三年复审）；仅在医疗器械语境下适用，普通科研项目不必套用。

---

## Regulatory Compliance skill（参考 Anthropic compliance 技能）

【是什么】Anthropic knowledge-work 插件里的 compliance 技能，面向法务/隐私团队的合规工作流助手。**不提供法律意见**，产出供合格法律人员复核。

【可复用方法 — 可借鉴的工作流结构】
- 覆盖法规：GDPR、CCPA/CPRA、UK GDPR 为主；监控 LGPD（巴西）、POPIA（南非）、PIPEDA（加拿大）、PDPA（新加坡）、澳隐私法、PIPL（中国）；引用 SOC 2、ISO 27001、NIST。（注：未含 HIPAA。）
- 三大工作流可借鉴到本技能的隐私/合规审查：
  1. DPA 审查：按 GDPR Art.28 清单核对（主体/期限、处理者义务、子处理者控制、72h 内泄露通知、审计权、跨境传输机制 SCC/BCR/充分性认定），并标记常见问题（如"无通知的概括性子处理者授权""泄露通知 >72h"）。
  2. 数据主体请求（DSR）处理：识别请求类型 → 判定适用法规/管辖 → 比例化验证身份 → 登记截止期 → 检查豁免 → 在法定期限内响应（GDPR 30 天 / CCPA 45 天）→ 记录结果。
  3. 法规监控：跟踪指南/执法/立法/传输机制变化，触发条件满足时升级给高级法律顾问。
- 设计要点：分层清单 + 决策树 + 截止期护栏 + 缺口识别 + 升级建议，最终判断留给法律专业人员。

【链接】https://playbooks.com/skills/anthropics/knowledge-work-plugins/compliance

【已知坑】明确"非法律意见"；不覆盖 HIPAA 等行业专门法；用于本技能时要把"隐私法务视角"映射到"科研数据合规"语境。

---

## 研究小结

本轮逐工具复核（2026-06），13 个参考对象全部研究：
完整核实 12 个：COPE、ICMJE、CRediT、ORI、Retraction Watch（Crossref API + CSV）、Turnitin、ScanCode、Snyk、Socket.dev、Creative Commons Chooser、ISO 13485（含 FDA QMSR 2026-02 生效）、Anthropic compliance 技能。
- 本轮新核实：Turnitin AI 检测官方误报数字（文档级 <1%、句子级 ~4%、20% 阈值安全机制）；FDA QMSR 终规已于 2026-02-02 正式生效。
仍部分受限 1 项：
- IRB / 45 CFR 46 政府原文页（ecfr.gov/hhs.gov）在本环境被网络策略阻断，46.111/46.116 内容已用多家法律解读源交叉核实，但逐字条文须回查官方原文。
- 旁注：api.crossref.org / scancode-toolkit.readthedocs.io / aboutcode.org 等域名在本环境对直接抓取受限，相关端点/CLI 选项已通过搜索结果与既往核实交叉确认。
