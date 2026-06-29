# light-paper-drafting — 深度分析与同类对标

> 源：[`skills/light-paper-drafting/SKILL.md`](../../../skills/light-paper-drafting/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：以"如何让审稿人相信这篇值得发表"为总纲、把反幻觉协议从口号落成可执行配额的论文初稿撰写技能,支持五档操作模式与六类结构模板。

## 核心运行逻辑
核心是"先研究后落笔 + brief 驱动":每个 claim 落笔前要有可核查来源,无来源即标 [MATERIAL GAP]/[RESULT GAP],绝不凭空填充(anti-leakage)。围绕"贡献清单(pillar)→大纲+论证图(论点→证据→反驳)→逐节初稿"的 ARS 流水线组织。诚信是第一性约束,通过两道量化门(初稿≥30% 抽样、终稿 100% 全查)+ 8 维质量自检 + 7 类 AI 失败模式红线(源自 The AI Scientist)落地,并用 draft_lint.py 做机检兜底(人判优先)。设计上明确区分"五种操作模式",避免每次都走全流程。还专设"论文差点意思时如何诚实讲好故事"一节,把重新定位贡献/负结果变卖点与"绝不谎报增量、绝不藏失败"两条铁律绑定。

## 关键步骤
- 1. 选操作档位:full / outline-only / abstract-only / section-redraft / self-review(见 operational_modes.md)
- 2. 写作前确认创新点(m03/m04)、结果亮点(m06)、目标 venue 风格(db01/db02)
- 3. Paper Configuration:定结构类型与目标 venue
- 4. 写 3 条左右贡献清单作为全文 pillar
- 5. 画大纲 + 论证图(论点→证据→反驳→回应)再落笔
- 6. 选 templates/ 六类骨架之一,认领 guideline_map 对应报告规范
- 7. 逐节初稿,未核内容一律标 GAP,正文引用用 \cite{authorYearWord} 机读 citekey
- 8. 每节写完过 8 维 + 7 模式自检(self_review_checklist),命中'触发改写'列即返工
- 9. 填 mandatory_inclusions 必备声明位
- 10. 过诚信门:初稿门抽样→终稿门 100% claim/引用核查(含无 DOI 中文文献三字段比对)
- 11. 机检 draft_lint.py 查残留 GAP/缺声明/无显著性 SOTA 句,交付下游(m08/m09/m10/m11/m12/m14)

## 自带资产
- SKILL.md — 总纲、五模式导航、分模块要点、诚实讲故事、citekey 公式
- references/operational_modes.md — 五档模式的触发/输入/步骤/产出/诚信门档位
- references/integrity_gate.md — claim 抽样配额表 + DOI/Crossref/arXiv/OpenAlex 核查动作 + 无 DOI 中文文献三字段比对协议(含真实留痕示例)
- references/self_review_checklist.md — 8 维质量 + 7 类 AI 失败模式,每项'看什么/什么触发改写'两栏
- references/guideline_map.md — 研究类型→CONSORT/STROBE/PRISMA/STARD/TRIPOD/ARRIVE/CARE/SRQR 报告规范映射
- references/mandatory_inclusions.md — Data/Code/Ethics/CRediT/COI/Funding + 按 venue 的 AI 使用声明模板
- references.md — 15 个相关工具/框架逐个调研笔记(含已知坑)+ 未能核实工具单列
- scripts/draft_lint.py — 正则机检器:残留 GAP / 缺失声明 / 无显著性 SOTA 句 / 抽取待核 DOI+arXiv,带 --selftest
- templates/01_imrad.md — IMRaD 实证骨架(节序+字数上限+图表位+声明位)
- templates/02_review_survey.md — 综述/系统综述骨架(含 PRISMA 图位)
- templates/03_theory.md — 理论/定理方法骨架(假设/定理/证明附录)
- templates/04_case_study.md — 案例研究骨架(CARE/SRQR)
- templates/05_policy_brief.md — 政策简报骨架(结论前置)
- templates/06_conference.md — CS/ML 会议短篇骨架(双盲/页数/teaser 图)
- examples/worked_example.md — CVPR 长尾分类端到端范例,Introduction'前(踩满幻觉红线)/后(合规标 GAP)'对照

## 优点
- 反幻觉不是口号而是可执行机制:GAP 标记 + 抽样配额(30%/100%)+ 高危类永远全查 + 机检脚本四重落地,worked_example 用真实'前/后'对照演示了 M2/M3 如何被拦截
- 无 DOI 中文文献核对协议罕见且接地气:题录三字段(题名/作者单位/刊名年卷期)比对、明确 CNKI 直连不通与维普 403 反爬、改走人工浏览器比对,并与 m10 citation 双向声明职责划分,口径一致
- 五档操作模式设计务实:outline-only/abstract-only/section-redraft 让用户按最小够用工作量调用,不必每次走全流程,降低 token 成本
- 六类结构模板覆盖面广且实用:每个含节序、每节字数上限、[图位/表位]、必备声明位,且按 venue 标注双盲/页数/PRISMA 图等差异
- references.md 调研诚实硬核:15 个工具逐个给【是什么/可复用方法/链接/已知坑】,且专列'未能核实工具'(PACSOMATIC)拒绝编造,与技能本身反幻觉立场自洽
- '论文差点意思时诚实讲好故事'一节有水平:区分'重新定位贡献'与'夸大',把负结果设节变卖点,并用两条铁律(不谎报增量、不藏失败)兜底,直面真实科研场景
- 与 Light 生态衔接缜密:citekey 公式 authorYearWord 与 m10 pin 的键同源,声明、图表、排版、润色、审稿、版本各有明确下游对接点

## 缺点 / 可被质疑处
- draft_lint.py 的高危句检查是逐行的:HYPE_PAT 与 SIG_PAT 必须在同一行命中才算通过,SOTA 主张与 p 值分处相邻句/相邻行时会误报,而连排成一个长段落的草稿(很常见)则整段失配,缺句子/段落级切分
- lint 未跳过 markdown 围栏代码块:GAP 的 TODO、DOI/arXiv 抽取会把代码块或引用示例里的内容当真命中,产生假阳性;REQUIRED_SECTIONS 用关键词全文子串匹配('ethics'出现在正文散句即算通过),并非校验真有该 section 标题
- 诚信门最核心的 Material Passport / claim 台账没有模板文件:integrity_gate 反复要求'登记到 claim 台账''写进 Material Passport',但 templates/ 里只有结构骨架,没有台账脚手架,最 load-bearing 的产物反而无落地表格
- claim 抽样 30%/100% 与台账登记全靠 LLM 自律,无任何枚举/强制工具——references.md 自己点出 ARS 的 data_access_level 是'声明式标注非运行时强制',但本技能对自己的 claim 台账存在同样弱点却未承认
- 报告规范偏临床医学(CONSORT/STROBE/PRISMA/STARD/ARRIVE/CARE),而范例与主要受众是 CS/ML;guideline_map 对 ML 只给了 TRIPOD+AI,缺 NeurIPS reproducibility checklist、datasheets、model cards 等该领域真正会用的报告件
- 中文写作支持名实不符:技能描述与中文文献协议都面向中文用户,但模板字数全用英文'词'(150–250 词)计,中文论文按'字'计,字/词口径未澄清;references 提到 ARS 有 Bilingual Abstract、SKILL 也说'可选双语',但无双语摘要模板或方法
- references.md 出现多条未经技能自身诚信门核验的未来日期文献(Nature s41586-026-10265-5、arXiv 2604.05018、CNPE arXiv 2603.17588 标 ACL 2026),以确定语气写入却无 HTTP 码留痕——这与技能强调的 M2 幻觉引用红线和'curl 实测记码'要求自相矛盾
- self-review 依赖的 Devil's Advocate'反驳打分≥4 才让步'阈值在 worked_example/SKILL 被引用,但 1–5 评分 rubric 本身不在本技能资产内(来自外部 ARS),脱离 ARS 单独用时不可操作

## 可优化点（供后续逐技能优化）
- 新增 templates/claim_passport.md(或 material_passport.md)脚手架:列 claim-ID / 类型①②③④ / 来源指针(日志·表格·DOI) / 核查状态(已验证·待核·GAP) / HTTP 码·核查日期,把 integrity_gate 反复引用却无实体的台账补齐
- 重写 draft_lint.py 的句/段切分:HYPE×SIG 改为同句(或同段窗口)共现判定而非同行;解析时跳过 ``` 围栏代码块与引用块;REQUIRED_SECTIONS 改为校验行首 markdown 标题(^#+\s*…)而非全文子串;可加 --claims 模式抽取候选事实句以播种 claim 台账
- 在 guideline_map 增补 CS/ML 行:NeurIPS/ICLR reproducibility checklist、Model Cards、Datasheets for Datasets,匹配范例与主要受众,避免该领域用户只能借医学规范
- 为'相关工作综述合成'补一个微流程/模板:技能自己说综述是胜负手(references 引 50–68% 胜率)却最缺脚手架——给出 taxonomy 轴选取 + 每类'delta 句'骨架 + 强 baseline 锁定清单
- 澄清中文写作的字/词口径并给双语摘要模板:模板字数标注改为'字/词'双预算或给换算说明,新增 bilingual abstract 写法与结构
- 对 references.md 自身执行技能的诚信门:对 Nature s41586-026、arXiv 2604.05018、CNPE 2603.17588 等逐条 curl 实测并记 HTTP 码,核不到的改标'待核查',做到自洽
- 把 Devil's Advocate 的 1–5 评分 rubric 直接写进 self_review_checklist(M7 行),使≥4 让步阈值脱离外部 ARS 也可独立执行
- draft_lint.py 增加机读输出(JSON/退出码摘要),便于 m-orchestrator 在阶段间自动判定过门与否

## 与其他 Light 技能/知识库的衔接
上游输入:m03/m04(创新点)、m05(实验设计)、m06(结果与亮点)、db01/db02(venue 风格与结构套路,取目标年份当年模板)。下游对接:图表交 m09/m11、引用交 m10(citekey authorYearWord 与 m10 pin 的键同源,且无 DOI 中文文献核验由本技能拦截、m10 兜底执行,双向声明)、排版交 m12、润色交 m08、模拟审稿交 m14、投稿定位交 m13(如实报增量)。横向:术语与 db09 术语表对齐(a07),交付前过 a08(light-self-review)自检闸门,版本入 db09。失败模式与诚信门方法论显式取自 references.md 调研的 ARS、The AI Scientist、ScholarEval、MarkItDown 等外部工作。

---

## GitHub 同类前沿技能对标

GitHub 上的同类项目大体分两类:一类是"端到端自动写论文"的多 agent 流水线(AI-Scientist、AI-Researcher、Idea2Paper、paper-orchestra、opendraft、open-paper-machine、PaperKit),目标是无人值守生成完整稿件;另一类是"诚信/检索基础设施"(paper-qa 做带引用的高精度 RAG、STORM 做带引用的报告生成、hallucinator 做参考文献造假检测)。light-paper-drafting 与这两类都不同:它是一个面向 Claude Code/Codex 的人机协作"技能"而非自动管线,把审稿人视角、反幻觉协议落成可量化配额(30% 抽检/100% 全查两道门)、7 类 AI 失败模式红线和五档操作模式,核心卖点是"诚信第一性 + 不凭空填充(标 MATERIAL/RESULT GAP)+ 诚实讲好故事"。直接可比的只有 Master-cai/Research-Paper-Writing-Skills(同为 Claude Code 写作技能包),但后者偏写作经验萃取、缺把反幻觉做成机检兜底与量化门;其余项目要么追求全自动产出(与 Light"先研究后落笔、人判优先"理念相反),要么只解决引用核验单点而无完整初稿撰写流程。Light 的独特性在于把"防造假"从口号变成可执行规约,这是绝大多数热门项目的明显缺口。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | 面向 Codex/Claude Code/Gemini 的 ML/CV/NLP 论文写作技能包,改编自彭思达老师的公开写作笔记,提供成稿规范与写作经验。与 Light 形态最接近(同为 agent skill)。 | 3749 | 2026-04-23 | 强:同生态、星数高、写作经验沉淀厚、中文社区认可度高。弱:偏'怎么把话写好'的经验法则,缺 Light 的量化反幻觉双门(30%/100%)、draft_lint.py 机检兜底、7 类 AI 失败模式红线与 MATERIAL/RESULT GAP 留白机制;无显式五档操作模式与论证图(论点-证据-反驳)流水线。 |
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 端到端全自动科研框架:从想法生成、实验、写作到自动审稿,论文中总结的 AI 写作失败模式正是 Light 红线条目的来源。 | 13956 | 2025-12-19 | 强:完整自动闭环、影响力大、有自动评审环节。弱:追求全自动产出,易产生幻觉与夸大增量;无人在环把关,与 Light'人判优先、不凭空填充、绝不谎报增量'的诚信约束方向相反;它是 Light 的'反面教材来源'而非协作写作工具。 |
| [Future-House/paper-qa](https://github.com/Future-House/paper-qa) | 面向科学文献的高精度带引用 RAG,每个回答都附可核查来源,主打超人级文献综合与低幻觉。 | 8690 | 2026-06-11 | 强:引用接地工程化成熟、检索精度高、活跃维护,正好补 Light'每个 claim 要有可核查来源'的检索后端。弱:是问答/综述检索库,不产出按六类结构模板组织的论文初稿,也无操作模式/质量自检/讲故事环节;定位是基础设施而非写作技能。 |
| [stanford-oval/storm](https://github.com/stanford-oval/storm) | LLM 知识策展系统,先做多视角提问检索再生成带引用的长篇报告(Wikipedia 式),含 Co-STORM 协作模式。 | 28358 | 2025-09-30 | 强:星数极高、'先研究后写'的 pipeline 理念与 Light 一致、引用接地、有大纲生成。弱:产出是百科式报告非学术论文,无审稿人视角、无反幻觉量化门、无负结果/重定位贡献的讲故事策略;面向通用主题而非投稿级稿件。 |
| [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher) | NeurIPS2025 的自主科研创新系统,覆盖想法到论文的自动化研究流程,有生产版本。 | 5453 | 2025-10-16 | 强:学术背书强、自动化程度高、覆盖研究全周期。弱:全自动取向,弱化人类核验与诚信约束;无 Light 的可执行反幻觉配额、GAP 留白与五档模式;偏研究执行而非可投稿初稿的诚实撰写。 |
| [AgentAlphaAGI/Idea2Paper](https://github.com/AgentAlphaAGI/Idea2Paper) | 从想法到论文的自动生成 agent 演示项目。 | 1349 | 2026-03-24 | 强:轻量、想法到稿件链路直观、有一定关注度。弱:Demo 性质,缺引用核验、反幻觉门、质量自检与结构模板体系;无人在环把关,易凭空生成,与 Light 诚信优先理念冲突。 |
| [google-research/paper-orchestra](https://github.com/google-research/paper-orchestra) | Google Research 的多 agent 自动论文写作框架。 | 57 | 2026-05-17 | 强:大厂出品、多 agent 编排架构清晰。弱:面向自动化编排,无显式反幻觉量化门/机检兜底,无操作模式分层与'诚实讲好故事'章节;研究框架而非协作写作技能,星数尚低。 |
| [federicodeponte/opendraft](https://github.com/federicodeponte/opendraft) | 开源 AI 学位论文写作器,19 个专门 agent,声称从 5 亿+篇文献核验引用,导出 PDF/Word/LaTeX。 | 135 | 2026-06-01 | 强:多 agent 分工细、内置引用核验、强调 verified citations(与 Light 反幻觉同向)、产出格式丰富。弱:仍是全自动 20k 字快速出稿取向,缺人判优先、抽检/全查量化门与 GAP 留白;无审稿人视角与五档模式,质量把关靠引用核验单点。 |
| [gianlucasb/hallucinator](https://github.com/gianlucasb/hallucinator) | 检测学术 PDF 中潜在幻觉/伪造参考文献的工具。 | 224 | 2026-06-04 | 强:专精参考文献造假检测,正好对应 Light 的 anti-leakage/终稿全查思路,可作核验后端。弱:只做引文事后检测单点,不撰写初稿、无写作流程/操作模式/结构模板;是检查器而非写作技能。 |
| [peternicholls/PaperKit](https://github.com/peternicholls/PaperKit) | 用于检索、抽取引用、起草并产出 LaTeX 学术论文的 agent 框架。 | 4 | 2026-03-25 | 强:覆盖检索-引用-起草-LaTeX 全链路、引用抽取与 Light'可核查来源'契合。弱:星数很低、社区验证不足;无反幻觉量化门、质量自检八维、AI 失败模式红线与讲故事策略;偏工程脚手架而非诚信规约驱动的写作技能。 |

### Light 该技能可借鉴的点
- 接入成熟的引用接地后端:可借鉴 Future-House/paper-qa 的高精度带引用 RAG 与 stanford-oval/storm 的'多视角提问-检索-成文'管线,把 Light'每个 claim 要有可核查来源'的检索环节工程化,减少人工找源成本。
- 强化引文事后核验:gianlucasb/hallucinator 专做参考文献造假检测,其思路可融入 Light 终稿 100% 全查门,作为 draft_lint.py 之外的伪造引用机检兜底。
- 多 agent 角色分工:opendraft(19 agent)、paper-orchestra、PaperKit 的专门化 agent 编排,可启发 Light 把五档操作模式拆成可调度的子角色(检索员/论证图构建/逐节起草/红线审查),而不牺牲人判优先。
- 成稿写作经验萃取:Master-cai/Research-Paper-Writing-Skills 沉淀了大量'怎么把话写好'的具体写作法则,Light 的八维质量自检可吸收其句段级写作规范,补足从'诚信合格'到'文笔过审'的最后一公里。
- 自动审稿环节:SakanaAI/AI-Scientist 的自动 reviewer 可逆向用于 Light——在终稿门后增设'模拟审稿人'自检,把'让审稿人相信值得发表'的总纲变成可运行的对抗性检查。
- 引用规模与格式产出:opendraft 的 5 亿+文献核验与 PDF/Word/LaTeX 多格式导出,提示 Light 可补充终稿格式化与大规模文献覆盖能力。
