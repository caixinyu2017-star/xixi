# light-literature-search — 深度分析与同类对标

> 源：[`skills/light-literature-search/SKILL.md`](../../../skills/light-literature-search/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：多源学术检索→去重归并→可信度判级→PRISMA留痕→引用核验的科研资料调研技能，以"免费无key API + 诚实不臆造"为底色，产出可直接喂给写综述/提idea的结构化文献工件。

## 核心运行逻辑
核心是把"调研一个方向"工程化为可复现管线：多源并行检索(OpenAlex/Crossref为可运行主力，PubMed/Europe PMC/arXiv/bioRxiv/S2等为文档级指引)→按DOI跨源去重归并→还原OpenAlex倒排摘要→按被引(标来源库口径)排序→用"年龄×年均被引"经验阈值判奠基/里程碑/SOTA角色→PRISMA计数勾稽留痕→DOI内容协商核验幻觉引用。贯穿全程的设计纪律是"诚实第一":无网络回退合成样本并打[OFFLINE]、打印真实HTTP码、被引数不跨库直接比、不臆造DOI、免费源不可得就如实标注。中文检索绕开无API的知网/万方,改用OpenAlex/Crossref按ISSN命中中文期刊作低门槛主力。所有重资料(端点/限流/坑)沉到references.md,SKILL.md做策略层。

## 关键步骤
- 1. 输入澄清:方向/核心问题/中英关键词/目标venue/时间范围/语言/深度(速览/中等/穷尽)
- 2. 多源+多角度检索:按概念/方法/作者/时间/引用关系分别扫,给每库可直接复制的query字符串
- 3. 运行 search_normalize.py 拉 OpenAlex+Crossref,还原摘要,跨源DOI去重,按被引排序出文献表(JSON+MD)
- 4. 滚雪球 snowball.py:从种子做前向被引+后向参考(OpenAlex或S2),标边类型与isInfluential
- 5. 筛选整理:相关度阈值剔跑题→分类(子方向/方法族)→可信度分层→重要性判级
- 6. 系统综述走 PRISMA:screen两轮(题摘筛+全文筛)+extract逐篇抽,prisma_flow.py 勾稽核对各阶段计数自洽
- 7. 引用核验:verify_citations.py 回Crossref/doi.org比对标题/年/首作者,标VERIFIED/MISMATCH/DOI_NOT_FOUND(疑似幻觉)
- 8. 落盘 docs/literature_review.md(文献表+研究脉络+方法卡+优缺点对比+可复用资源+gap),交m03/m07等
- 9. 长期项目按定期追踪协议(--from-date + --known-dois)周期增量重跑盯新文献

## 自带资产
- scripts/search_normalize.py — urllib直连OpenAlex+Crossref,还原倒排摘要,DOI跨源去重归并,被引排序,支持--from-date/--known-dois增量追踪,带[OFFLINE]回退与selftest
- scripts/verify_citations.py — DOI内容协商(doi.org→Crossref回退)核验,比对标题相似度/年份/首作者,四类verdict标幻觉引用
- scripts/snowball.py — 引用滚雪球,OpenAlex(referenced_works批量回填+cites:过滤)或S2(references/citations),支持两跳,标isInfluential
- scripts/prisma_flow.py — PRISMA2020计数勾稽核对(前阶段−排除=后阶段),抓算术错误,出流程图结构化数据,含反例自测
- scripts/cn_journal_probe.py — 读ISSN清单批量探OpenAlex source体量(id/works_count/cited_by)
- assets/cn_core_issn.csv — 11个北大核心/CSCD真实ISSN种子(计算机/电子/自动化/农业等,声称逐条curl核实)
- assets/litreview_template.md — 综述填空骨架(含PRISMA检索元信息表+脉络+方法族+判级+gap)
- assets/method_card.md — 方法卡模板,字段对齐db03,带[已验证]/[文献]/[推测]证据等级标注
- examples/worked_example_dairy_goat.md — 奶山羊端到端PICO→query→命中→去重→筛选→核验留痕实例(含'宽query出垃圾'的诚实教训)
- examples/goat_search.json + goat_littable.md — worked example的真实输出产物
- references.md — ~490行参考研究笔记:逐一核实的API端点/参数/限流/坑,含OpenAlex接入真相源(key/计费唯一口径)、中文检索、screen/extract协议、单篇深读卡、定期追踪协议、灰色文献路径

## 优点
- 诚实纪律是真落到代码的,不是口号:每个脚本都有[OFFLINE]合成样本回退+selftest+打印真实HTTP码,被引数处处标来源库(OpenAlex/Crossref/S2口径不同不可直接比),verify_citations把幻觉引用做成可执行检测——这正面回应了综述类任务最大的审稿风险
- references.md把易变信息(端点/限流/计费)单点沉淀,尤其OpenAlex 2026需key+$1/天计费设为'全仓库唯一口径',并保留口径冲突存档(旧'无需key'已废弃),版本治理意识强
- PRISMA勾稽脚本切中真实痛点:审稿人必查的'各阶段数字加减是否自洽',脚本机械核对并带反例检测,且明确划清'只核计数不替你做筛选判断'的边界
- 跨源DOI去重+倒排摘要还原+无DOI回退(规范化标题+年)实现正确且自洽,snowball与search_normalize复用同一_norm_doi/_norm_title,工程一致
- 中文检索处理务实诚实:不假装有知网API,改走OpenAlex/Crossref按ISSN命中,并明确标注'OpenAlex把中文标题存英译、按source.id比language:zh可靠'这个真实坑,GB/T 7714著录到位
- 概念分层清晰且防重复:综述extract(横向可比表)vs单篇深读卡(纵向钻深)vs定期追踪(增量diff)三类协议各司其职,worked example甚至诚实记录'宽query+纯被引排序会顶出跑题高被引文'的失败教训
- 衔接设计明确:gap喂m03、PRISMA数据喂m09绘图、文献表交m10做引用核查、预印本可信度口径与light-citation统一,工件命名挂CONVENTIONS

## 缺点 / 可被质疑处
- 文档承诺与可运行能力严重不对称:description宣称覆盖论文/专利/标准/政策/数据集/开源/竞赛方案/行业报告/技术博客/官方文档10+类源,但有脚本支撑的只有OpenAlex+Crossref期刊文章;PubMed/Europe PMC/arXiv/bioRxiv/S2全文检索、Exa/Parallel/browser-use全停在references文字层,agent每次得手搓urllib,'多源并行'在代码里只有2源
- OpenAlex接入存在内部矛盾:references斩钉截铁说'2026起需免费key、生产代码一律按需key实现',但search_normalize/snowball/cn_journal_probe三个脚本都没有--api-key参数、只带mailto,一旦匿名通道关闭脚本即失效——这是技能自己定的铁律自己没遵守
- MAILTO硬编码为伪造的'light-skill@example.com'进礼貌池,既不合礼貌池本意也可能被限流;且用户无法从命令行覆盖
- 无任何代码级相关度过滤,worked example自己承认宽query+纯cited_by排序会把'theory of planned behavior''G*Power'等跑题高被引文顶上来,而script输出就是这个被引序,质量净化完全甩给人工/agent二次筛,开箱产出对宽主题基本不可用
- references力推的SPECTER2语义去重(768维余弦补关键词盲区)只有文字描述,没有任何脚本实现;dedup仍是difflib字符串匹配,'换标题的同一工作'抓不到
- search_normalize/snowball无游标分页,search_normalize每源只取per_page条,穷尽式扫库(声称支持的深度档)实际做不到;snowball两跳只对top-3做扩展是写死的任意值
- verify_citations的标题相似度阈值0.6硬编码、只能验有DOI条目,arXiv-only/中文无DOI条目落NO_DOI需人工,且无法识别'真DOI挂错论文'之外的语义造假;首作者只比姓氏易误判
- 中文链路只能拿到英译标题+常缺卷期页码,cn_journal_probe只探刊'体量'不取论文,要原始中文题录仍需人工回知网/出版商,实际中文产能比宣传弱
- references.md约490行,末尾还有一段'已知坑/局限'孤立悬挂在灰色文献节之后(疑似K-Dense skills节的注脚错位),全量加载有上下文膨胀与结构瑕疵风险

## 可优化点（供后续逐技能优化）
- 给所有联网脚本加 --api-key 参数与 OPENALEX_API_KEY/CROSSREF_MAILTO 环境变量读取,把MAILTO从伪造邮箱改为运行时必填/可覆盖,兑现references自己定的'按需key实现'铁律
- 把references里已详尽文档化的源补成可运行脚本:至少加 arxiv_fetch.py、pubmed_eutils.py、europepmc_search.py、biorxiv_fetch.py,统一输出与search_normalize同schema,让'多源并行'名实相符
- 给search_normalize加最小相关度过滤:支持 --topic-id(OpenAlex primary_topic.id)/--require-terms(标题摘要必含词)/--exclude-terms,或对结果跑标题×query的TF-IDF/嵌入打分截断,直接解决worked example暴露的跑题问题
- 落地SPECTER2语义去重为 semantic_dedup.py:对DOI/标题去重后的结果批量取embedding算余弦(用相对差不用绝对阈值),既补关键词盲区也可直接被m03多样性检查复用(references已声明双向消费)
- search_normalize/snowball加cursor分页支持(--max-results),让'穷尽'深度档真正可用;snowball两跳的top-N扩展数改为可配参数
- verify_citations扩展:阈值可配、支持arXiv id核验(打export.arxiv.org)、对NO_DOI条目调用Crossref query.bibliographic反查候选DOI给人工确认,降低纯人工占比
- cn_journal_probe升级为可按ISSN直接拉刊内题录(filter=primary_location.source.id),并在缺原始中文标题时输出'需回出版商核对'标记,把中文链路从'探体量'推进到'真取数'
- references.md做瘦身与分文件(按源拆 references/*.md 懒加载),修复末尾孤立的'已知坑'错位段,降低全量加载的上下文成本
- 补一个端到端编排脚本或checklist把5个脚本串起来(检索→去重→滚雪球→PRISMA→核验→落盘literature_review.md),减少agent每次手工拼装的出错面

## 与其他 Light 技能/知识库的衔接
下游:gap与SPECTER2多样性数据喂 light-idea-generation(m03)、供 light-idea-critique(m04)审、related work喂 light-paper-drafting(m07)、PRISMA结构化数据喂 light-figure-drawing/planning(m09)绘流程图、返修对线喂 light-review-rebuttal(m14)。强耦合 light-citation(m10):文献表入库后交其做引用核查规避幻觉,预印本可信度分级与其verify_refs.py/Unpaywall(只取OA全文)口径统一。数据落盘 db01/db03(method_card字段对齐)/db04 与项目库 db09 的 literature/ 子目录(saved_search.yaml+known_dois.txt)。受 CONVENTIONS 约束(§3字段/§4注入安全单一真相源/§5版权不下全文/§6.1工件命名)。常驻技能 light-research-ethics(合规)、light-consistency(术语一致)、light-self-review(收尾自查)后台叠加。与 light-data-engineering(判数据是否足以支撑研究)、light-orchestrator(pipeline首阶段调用)存在自然衔接但SKILL未显式声明。

---

## GitHub 同类前沿技能对标

Light 这个技能的同类生态可分三层：(1) 学术检索 MCP/技能(paper-search-mcp、Academix、afrise、mcp-scholarly、K-Dense)——和 Light 同样做多源聚合，但绝大多数只到"搜得到+下PDF+导BibTeX"，几乎没人做跨源DOI去重归并、年龄×被引判级、PRISMA计数勾稽、DOI核验幻觉引用这一整套"调研工程化+诚实留痕"管线；(2) PRISMA系统综述工具(prisma-review-tool、LocalCitationNetwork)——在留痕/引用网络上比Light垂直深入，但绑定特定流程或前端、不是通用调研技能；(3) 通用深度研究agent(gpt-researcher、local-deep-researcher、PaSa、AI-Researcher)——star高、agent自主性强、产出长报告，但以"web/全文检索+LLM综合"为主，学术源口径松散、不强调被引来源不可跨库比、不做PRISMA勾稽、易产生臆造引用。Light 的差异化在于把"免费无key API为主力 + 诚实不臆造(打HTTP码/OFFLINE回退/被引标来源/不造DOI) + 中文期刊按ISSN绕开无API库 + 结构化可复现工件"捏成一条链路，定位偏"严谨可复现的科研调研脚手架"而非"一键出报告"。它的弱点是无独立UI/服务、自主检索智能(query改写、迭代反思)弱于深度研究agent、覆盖源数量少于paper-search-mcp。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | 面向科研的 Agent Skills 大合集(遵循开放 Agent Skills 标准，支持 Claude Code/Cursor/Codex 等)，含 Literature Review、Paper Lookup(PubMed/PMC/bioRxiv/arXiv/OpenAlex/Crossref)、Paperzilla 等子技能，是与 Light 最直接对标的'技能形态'同类。 | 28100 | 2026-06-12 (v2.52.0) | 强:技能数量庞大、社区活跃、覆盖基因组/药物/临床等多域、跨多agent生态。弱:literature-review更偏'能查能整理'的通用模板，未见Light这种跨源DOI去重归并+年龄×被引判级阈值表+PRISMA计数勾稽+DOI核验幻觉引用的成体系'诚实可复现'管线;中文期刊按ISSN检索的本地化几乎没有。 |
| [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) | LLM 自主研究 agent，对 web 与本地资料做深度检索并生成带引用的长篇研究报告，planner+execution 双agent聚合多源。 | 27700 | 2026-05-28 (v3.5.0) | 强:自主性高、query规划与多源聚合成熟、一键出长报告、生态/集成丰富。弱:以web深检索为主、学术源口径松散，不强调被引数跨库不可比、无PRISMA勾稽、无DOI内容协商核验,易产生臆造/不可追溯引用;非'科研调研工件'而是'报告生成'。 |
| [langchain-ai/local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher) | 全本地深度研究助手(Ollama/LMStudio 任意本地LLM)，自动生成检索式→搜集摘要→反思补缺→多轮迭代→输出带来源的 markdown 报告。 | 9200 | 2025-08-06 (README 最近记载) | 强:本地隐私友好、迭代反思式检索循环(query自我改写+gap补检)正是Light偏弱处、零API成本。弱:面向通用web而非学术库，无DOI去重/被引判级/PRISMA/引用核验,产出是报告非结构化文献工件。 |
| [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher) | 全自动科研发现系统(NeurIPS 2025 Spotlight)，从文献综述→idea生成→算法实现→验证→结果分析→论文撰写全链路自动化，文献调研只是其一环。 | 5500 | unknown (最新动态 2025-09) | 强:野心覆盖整条科研流水线、学术影响力大、综述环节嵌在闭环里。弱:文献检索子模块非其重点、不强调免费源/诚实留痕/中文/PRISMA;重而难复现,与Light'轻量可运行脚本+诚实纪律'定位相反。 |
| [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) | MCP 服务器(也可作 Claude Code skill+CLI)，从 20+ 学术源搜索/下载论文并抽取全文，free-first 策略(arXiv/PubMed/bioRxiv/medRxiv/S2/Crossref/OpenAlex/Europe PMC/CORE/DOAJ/Zenodo 等)。 | 1800 | unknown (43 commits，页面无日期) | 强:覆盖源数量明显多于Light、能下PDF+抽全文、免费优先理念一致、MCP即插即用。弱:止于'搜+下+抽'，无跨源DOI去重归并、无被引判级、无PRISMA勾稽、无幻觉引用核验、无中文期刊ISSN策略,缺Light的'整理与可信度判级'层。 |
| [bytedance/pasa](https://github.com/bytedance/pasa) | 字节跳动的 LLM 论文搜索 agent，Crawler+Selector 双agent经强化学习训练(AutoScholarQuery 数据集)，自主调搜索工具、读论文、选参考文献回答复杂学术查询。 | 1600 | unknown (8 commits，页面无日期) | 强:RL训练的自主检索决策、面向复杂学术query的召回质量、有论文背书。弱:研究原型而非可复用技能/管线，无去重判级/PRISMA/引用核验/中文/诚实留痕的工程纪律,落地与可复现性弱于Light。 |
| [adityak74/mcp-scholarly](https://github.com/adityak74/mcp-scholarly) | 查找学术论文的 MCP 服务器，目前单一工具 search-arxiv 按关键词检索 arXiv(README 称后续会加更多源)。 | 180 | unknown (24 commits，无 release/日期) | 强:轻量、MCP标准、易接入。弱:目前仅 arXiv 单源，远窄于Light的多源并行;无任何去重/判级/PRISMA/核验/中文能力。 |
| [afrise/academic-search-mcp-server](https://github.com/afrise/academic-search-mcp-server) | 面向 Claude Desktop 的学术检索 MCP，暴露 search_papers/fetch_paper_details(按DOI或S2 ID)/search_by_topic(可按年份过滤)，数据来自 Semantic Scholar 与 Crossref。 | 117 | unknown (14 commits，页面无日期) | 强:接口干净、含按DOI取详情、可年份过滤、MCP即用。弱:仅2源、无去重归并/被引判级/PRISMA/引用核验/中文;Light的Crossref'DOI真相源'用法它只用作普通检索。 |
| [LocalCitationNetwork/LocalCitationNetwork.github.io](https://github.com/LocalCitationNetwork/LocalCitationNetwork.github.io) | 面向科研文献综述的 Web 应用，用 OpenAlex/Semantic Scholar/Crossref 元数据围绕种子文献构建并可视化本地引用网络，给出 Top Cited/Top Citing 帮助发现遗漏文献(支持 Zotero Cita)。 | 140 | unknown (52 commits，页面无日期) | 强:引用网络可视化+前后向滚雪球做得比Light的snowball脚本直观、可发现遗漏关键文献、面向系统综述补检。弱:是web前端工具非agent技能、不出结构化文献表/方法卡、无被引判级阈值/PRISMA计数勾稽/DOI幻觉核验/中文期刊策略。 |
| [RainerSeventeen/paper-tracker](https://github.com/RainerSeventeen/paper-tracker) | 关键词驱动的论文追踪工具，支持 arXiv/OpenAlex/PubMed，LLM 做摘要翻译/总结，SQLite 去重存储，多格式输出(JSON/Markdown/HTML)。 | 54 | 2026-05-07 (v0.2.0) | 强:'定期增量追踪新文献'做成了独立持久化工具(SQLite去重+多格式导出+LLM翻译)，正对应Light的'文献定期追踪协议'但更产品化;OpenAlex/arXiv/PubMed与Light主力源重合。弱:仅去重去到标题级、无被引判级/PRISMA/DOI核验/中文期刊ISSN/可信度分层,定位是追踪而非深度调研。 |

### Light 该技能可借鉴的点
- 借鉴 RainerSeventeen/paper-tracker：把'文献定期追踪协议'从脚本参数升级为带 SQLite 持久化的增量追踪 + 多格式(JSON/MD/HTML)导出 + 可选 LLM 摘要翻译，让定期重跑更产品化、状态可留存。
- 借鉴 local-deep-researcher / PaSa：补强自主检索智能——加入'生成检索式→看命中→反思盲区→自动改写query再检'的迭代循环，缓解 Light 目前 query 构造偏静态、依赖用户给词的弱点(可作为可选 agent 模式，仍保留诚实留痕)。
- 借鉴 LocalCitationNetwork：把 snowball.py 的滚雪球结果做成引用网络可视化(节点=文献、边=引用，标 Top Cited/Top Citing)，更直观地暴露遗漏的奠基/枢纽文献，喂给综述写作。
- 借鉴 paper-search-mcp 的源覆盖广度：在保持 free-first 与诚实标注的前提下，把 references.md 里'文档级指引'的源(CORE/DOAJ/Zenodo/HAL/OpenAIRE 等)挑可运行的逐步升级为真实可跑脚本，扩展召回面。
- 借鉴 paper-search-mcp / K-Dense 的形态：把现有 Python 脚本封装成 MCP server 或标准 Agent Skill 入口，降低在 Claude Code/Cursor/Codex 等不同 agent 上的接入门槛，提升复用与分发。
- 借鉴 prisma-review-tool：为 prisma_flow.py 配一个轻量 PRISMA 流程图渲染(直接出图而非只出结构化数据)，并对接 AI 辅助标题/摘要初筛(带人工复核位)，让系统综述链路更完整。
