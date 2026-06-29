# light-memory-pm — 深度分析与同类对标

> 源：[`skills/light-memory-pm/SKILL.md`](../../../skills/light-memory-pm/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：科研项目的"状态中枢"与跨会话记忆纪律层：用 db09 项目库做权威长期记忆、用衔接卡+启动提示词做主动会话交接，把 m01–m17 全链路产物登记在一处并随时恢复。

## 核心运行逻辑
核心是"两层记忆模型"：会话级状态(短期、可随压缩丢弃)与项目级状态(长期、按项目 namespace 持久化到 db09)严格分离，关键事实即使能被自动抽取也必须显式写入,因为 db09 才是权威来源(借鉴 LangGraph checkpointer/Store 与 mem0 作用域设计)。每个项目落盘为 db09 一个独立目录,以 project_card.md 的 14 字段为总览,decision_log/terminology/version_history 分别承载决策时间线、术语统一、版本记录。整套机制是"纪律驱动"而非"工具驱动"——靠"触发→写入对照表"和"更新纪律(硬性)"强制 agent 在每次进展后立即回写,而非依赖任何自动同步脚本。会话开始优先读 next_actions 恢复"上次做到哪",会话收尾主动产出衔接卡+中文启动提示词让下一个对话零成本接续,衔接链是文件链(parent_session)而非聊天记忆链。跨项目可复用的过程教训上浮到顶层 lessons.md,立项/选方法前先检索复用。

## 关键步骤
- 1. 会话开始：定位 db09/projects/<slug>/project_card.md，优先读 next_actions 确认上次进度，跳过 archived 非空的归档项目，立项/选方法前先 Grep lessons.md 检索同类历史教训
- 2. 进展发生：按'触发→写入对照表'立即回写——idea 定稿改 confirmed_idea+追加 decision_log；实验跑完改 experiment_status+next_actions；出新版改 *_status+追加 version_history 并打 git tag
- 3. 五步写入示例：①读现状 ②改项目卡(带具体指标) ③追加决策日志(只追加不改写) ④记版本+git tag ⑤涉长期偏好则写 Light 记忆文件+MEMORY.md 索引行，相对日期一律转绝对日期
- 4. 跨项目教训回写(节制)：仅当决策产生可复用过程教训(踩坑/被否/复现失败/显著省时)才同时回写 lessons.md，日常项目内决策不强制
- 5. 会话交接(四类触发 T1 上下文水位/T2 任务完成/T3 阶段切换/T4 用户索要)：落盘衔接卡 .light/handoff/S<NN>-<slug>.md + 打印填好值的中文启动提示词，自传播条款要求每个接手会话收尾再造下一张卡
- 6. 项目完结：加 archived 字段(不挪目录)+回写终版 1-3 条 lessons，归档不删除，可删 archived 行复活

## 自带资产
- SKILL.md — 主纪律文件：两层记忆模型、四文件格式硬性定义、触发→写入对照表、会话开始/交接协议
- references.md — 13 个外部工具研究笔记(Git/DVC/MLflow/W&B/Zotero/Notion/Obsidian/Logseq/GitHub Issues/LangGraph/mem0/Open Notebook/Screenpipe 等)的端点/坑/可借鉴点，含项目归档协议全文；明确标注【未能核实】项，未编造端点
- references/session_handoff.md — 会话衔接协议执行细则：四类触发判据表、落盘规则、自包含原则、自传播条款、与 orchestrator 被动恢复的边界
- references/hermes_session_lineage_recovery.md — Hermes 单客户端的多会话/压缩主链恢复细则(查 state.db 的 parent_session_id/archived/cwd)
- templates/handoff_card.md — 衔接卡模板：session_no/parent_session/project 等 frontmatter + 当前阶段/已完成/下一步/阻塞/必读文件/禁止 六节
- templates/handoff_prompt.md — 中文启动提示词模板：含对话命名建议、必读文件顺序、刷新现实指令、自传播收尾要求
- (外部依赖)databases/db09-projects/ — README + project_card_template.md + lessons.md + 实例 projects/dairygoat-detect-track/，是本技能的实际落盘后端

## 优点
- 两层记忆模型有明确理论锚点(LangGraph Store/mem0 作用域)且落地为可操作规则：'自动抽取会漏记，db09 是权威来源'这一判断直击 LLM 记忆系统的真实失效点，比单纯依赖向量记忆更可靠
- '触发→写入对照表'把抽象的'记得更新'转成可机械执行的 if-then 规则(idea定稿→改X+追加Y)，并配五步写入示例和真实实例 dairygoat-detect-track，可复现性强、不留模糊地带
- 主动交接协议设计完整且自洽：四类触发+两件套产出+自传播条款，且诚实区分了'主动留种'与 orchestrator'被动恢复'的边界，避免概念打架；衔接链做成文件链(parent_session)而非记忆链，是真正抗压缩的设计
- decision_log'只追加不改写'、相对日期转绝对日期、archived 加字段不挪目录——这些细节体现了对'历史可追溯'和'不破坏既有相对路径'的工程审慎
- references.md 的研究诚实度高：网络被拦时明确标注【未能核实】、不编造端点、区分'是什么/可复用方法/已知坑'，并给出可借鉴点如何映射回本技能字段，是高质量的二手知识沉淀
- 职责边界划得清：方法选型事实归 db03、个人偏好归 feedback 记忆、跨项目教训归 lessons.md，三者不混，避免了记忆库语义污染

## 缺点 / 可被质疑处
- 纯纪律驱动，零自动化执行：整个技能没有 scripts/ 目录,所有'硬性'纪律(立即更新、序号递增、日期转绝对、git tag 对齐)全靠 agent 自觉。一旦上下文压缩或 agent 走神,'每次完成立即更新'必然漏执行——而这恰恰是它声称要解决的问题。references 提到 check_databases 校验但那个脚本不在本技能内,本技能自身无任何 schema 校验/lint 工具
- SKILL.md 与 db09 README 对'项目目录有几个文件'说法不一致:SKILL §存哪只列 4 文件并称实例'四文件齐全',但 README 和实例实际有 palette.json、literature/、reviews/、submissions/ 共 7+ 项,且实例缺 version_history 的真实历史(只记当前态)。新 agent 照 SKILL 建库会漏建配套文件
- 并发/冲突完全未处理:decision_log 只追加可防丢,但 project_card.md 是整体覆盖写。两个并行会话(正是本技能鼓励的多会话衔接场景)同时改项目卡会互相覆盖,无锁、无 last-modified 检查、无合并策略。handoff 卡的 <NN> 递增也依赖'先扫描已有最大序号',并发下会撞号
- references.md 的 13 个工具全是'可借鉴'(inspiration),无一真正集成:没有 Zotero/Notion/GitHub 的实际 adapter 或调用封装,'管理工具映射'在执行层只是建议 agent 手敲 git tag/gh CLI。声称的'文献→Zotero、进展→README+CHANGELOG'对 agent 而言仍是裸命令,价值停留在文档
- 两套记忆系统(Light 记忆文件 user/feedback/project/reference + MEMORY.md 索引 vs db09)边界虽有描述但认知负荷高:feedback 槽的'跨项目过程教训'要落到 db09 lessons.md、但 feedback 文件本身又存偏好,project 记忆文件与 db09 project_card 职责高度重叠却要双写。何时写哪个、是否重复,规则散落在多处,易错
- 可扩展性瓶颈未解:db09'只进不出',归档协议靠加 archived 字段+会话开始扫描跳过来防膨胀,但项目到几十上百个时,'会话开始扫描所有 project_card 找活跃项目'本身就是 O(n) 全表扫,无索引文件(如顶层 active projects 清单),恢复成本随项目数线性增长
- Hermes 恢复细则直接写死在通用记忆技能里:hermes_session_lineage_recovery.md 是单客户端(查 state.db)的实现细节,放在本应客户端无关的记忆技能 references 下,耦合了具体宿主,换客户端即失效且无抽象层

## 可优化点（供后续逐技能优化）
- 补一个 scripts/check_project_card.py:校验 14 必填字段齐全、日期为绝对格式、current_stage 在枚举内、decision_log/version_history 行格式合规、handoff 卡 parent_session 链可达,把'硬性纪律'从口头约束变成可运行的 lint(并在会话收尾自动跑一次)
- 加一个顶层 projects/_index.md 或 active.yaml:登记每个项目的 slug/current_stage/next_actions 首条/archived 状态,会话开始只读这一份索引即可定位,把 O(n) 全表扫降为读单文件,顺带解决项目膨胀后的恢复延迟
- 统一并修正文件清单:SKILL §存哪改为列全 7 项(标注必建/可选),与 db09 README 对齐;删除或修正'四文件齐全'表述,避免新建库时漏建 terminology/palette/submissions
- 给 project_card 写入加轻量乐观锁:frontmatter 增 last_modified 字段,改写前先读、写后比对,或改为'分字段追加式 patch 文件'而非整体覆盖,缓解并行会话互相覆盖;handoff <NN> 改为带 session 短哈希后缀防撞号
- 把 references.md 中高频工具(至少 git tag/gh issue/gh milestone)沉淀成 scripts/ 下的薄封装或可复制命令片段模板,让'管理工具映射'真正可执行而非纯建议;version_history 行与 git tag 之间做一个对账脚本(列出有 tag 无记录/有记录无 tag)
- 把 Hermes 细则抽象成 references/clients/ 子目录下的'每客户端恢复适配'格式,主协议只定义通用接口(找父会话/找归档/找 cwd),客户端实现下沉,降低宿主耦合
- 给两套记忆系统画一张唯一真相源(SSOT)决策表:每类信息(偏好/项目背景/进展/教训/方法事实)只指定一个权威落点+是否需索引双写,放在 SKILL 显眼处,消除 project 记忆文件与 db09 project_card 的职责重叠

## 与其他 Light 技能/知识库的衔接
本技能是 Light 全链路的状态中枢，衔接面最广。后端依赖 databases/db09-projects/(README+template+lessons+实例)作为实际落盘库,二者强耦合(README 多处写明'执行者是 a02')。上游接收 m01–m17 所有技能的产物登记:literature/ 收 light-literature-search(m01)、reviews/ 收 light-review-rebuttal(m14)、confirmed_idea 链 light-idea-generation/critique(m03/m04)、experiment_status 链 light-research-plan(m05)、各 *_status 链 paper-drafting/slides/figure-drawing/backend-coding。横向与 light-consistency(a07)共享 terminology.md 和 palette.json 做术语/配色 SSOT(db09_glossary/method_lock/metric_registry 在 consistency 技能侧)。与 light-orchestrator 互补:本技能管'主动留种(事前)'，orchestrator §0 管'被动断点恢复(事后六探针)'，§5 管阶段交接,三者通过 CONVENTIONS.md §9 统一纪律。palette.json 上游锚定 db05 design_tokens(a05 frontend-design)与 db06 themes.py(slides)。归档与 check_databases schema 校验(14 必填字段)联动但校验脚本不在本技能内。

---

## GitHub 同类前沿技能对标

light-memory-pm 的独特定位是"科研项目的跨会话状态中枢 + 记忆纪律层":它不是一个存储引擎,而是一套强约束的纪律协议——两层记忆模型(会话级 vs 项目级 namespace)、project_card 14 字段总览、decision_log/terminology/version_history 三件套、衔接卡+中文启动提示词的文件链交接、以及把 m01–m17 科研全链路产物登记在 db09 一处。GitHub 上的同类前沿项目几乎全部走"工具驱动"路线,可分三类:(1) 通用 agent 记忆引擎(mem0/Letta/cognee/langmem),强在自动抽取、向量/图检索、规模化召回,但缺科研项目语义和产物台账;(2) 编码 agent 的 Memory Bank 范式(cline memory bank/cursor-memory-bank/memory-bank-mcp/basic-memory/memsearch),最接近 Light 的"markdown 文件即记忆+会话间续接",但面向通用软件开发而非论文/实验/投稿链路;(3) 任务编排型(claude-task-master/deer-flow),强在任务拆解执行,弱在长期项目记忆纪律。Light 的差异点在于"纪律驱动而非自动同步"和"科研领域特化的字段/产物模型",这恰是通用工具最薄弱处;反过来 Light 缺的是语义检索、向量召回和工程化落地(目前是纯人工写盘约定,无自动 consolidation)。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | 面向 AI Agent 的通用记忆层,提供作用域(user/session/agent)分层记忆、自动事实抽取与向量检索召回,被大量 agent 框架集成。light-memory-pm 的两层记忆模型(会话级/项目级 namespace)正是借鉴其作用域设计。 | 58.5k | 2026-06-12 (最新 release) | 强:自动事实抽取+向量检索,规模化召回,生态成熟,工程化程度高。弱:无科研项目语义模型(没有 project_card/decision_log/version_history),不解决论文投稿全链路产物登记与会话衔接卡问题,是引擎而非纪律协议。 |
| [letta-ai/letta (原 MemGPT)](https://github.com/letta-ai/letta) | 构建有状态 agent 的平台,核心是 OS 式分层记忆(core/archival/recall memory)与自编辑记忆,让 agent 跨会话学习与自我改进。 | 23.3k | 2026-05-14 (v0.16.8) | 强:自动记忆分页/编辑,服务化部署,通用性强。弱:重框架、需运行时,不是轻量 markdown 约定;无科研领域特化,不产出可人读的中文启动提示词与衔接卡,科研产物台账需自建。 |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) | 开源 AI 记忆平台,用知识图谱+向量混合检索为 agent 提供跨会话长期记忆,强调实体关系建模。 | 17.8k | 2026-05-30 (v1.1.2) | 强:知识图谱建模能力强,跨文档实体关联检索远超纯文件链。弱:需 ETL/图数据库基建,门槛高;面向通用记忆而非科研项目状态中枢,缺投稿/版本/术语统一这类领域字段。 |
| [langchain-ai/langmem](https://github.com/langchain-ai/langmem) | LangChain 出品的 agent 长期记忆 SDK,配合 LangGraph 的 checkpointer/Store 让 agent 从交互中学习适配。light-memory-pm 的'关键事实必须显式写入权威源'借鉴了 LangGraph checkpointer/Store 思路。 | 1.5k | unknown | 强:与 LangGraph 原生集成,有 checkpointer/Store 标准化持久化抽象。弱:偏 SDK 原语,需自己组装记忆策略;无开箱的项目台账/衔接卡/科研流程,定位是库而非完整纪律层。 |
| [cline/cline (Memory Bank)](https://github.com/cline/cline/blob/main/docs/prompting/custom%20instructions%20library/cline-memory-bank.md) | Cline 的 Memory Bank 范式:用一组结构化 markdown(projectbrief/productContext/activeContext/progress 等)在会话间保存项目上下文,新会话先读 memory bank 恢复状态。与 light-memory-pm 的'会话开始读 next_actions 恢复进度'高度同构。 | unknown (文档页未显示;主仓库 star 较高但未核到具体值) | unknown | 强:生态庞大、范式被广泛采用,通用软件开发场景成熟。弱:面向编码而非科研,无 decision_log/terminology/version_history 三件套,无跨项目 lessons 上浮,无中文启动提示词;靠用户自觉更新,纪律强制弱于 Light 的'触发→写入对照表'。 |
| [eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master) | 可嵌入 Cursor/Windsurf/Roo 等的 AI 任务管理系统,把 PRD 拆成结构化任务并跟踪依赖与进度,是任务编排型的代表。 | 27.4k | 2026-03-31 (task-master-ai@0.43.1) | 强:任务拆解/依赖管理/进度跟踪非常成熟,工程化好。弱:重'任务'轻'记忆',无长期项目记忆纪律与会话衔接,不做术语统一/决策时间线/版本记录,科研产物登记需另建。 |
| [basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory) | 本地优先的 AI 记忆 MCP,把对话沉淀为本地 markdown 知识库(Obsidian 兼容),让 agent 跨会话'记住项目,不用反复解释'。理念与 Light 文件即记忆最接近。 | 3.2k | 2026-06-11 (v0.22.0) | 强:本地 markdown+双向链接+MCP,自动从对话沉淀知识,工具化落地好。弱:通用笔记式记忆,无科研项目 14 字段总览/投稿状态/衔接卡协议,缺'更新纪律(硬性)'这种强制回写机制。 |
| [vanzan01/cursor-memory-bank](https://github.com/vanzan01/cursor-memory-bank) | 文档驱动的开发框架,用 Cursor 自定义模式(VAN/PLAN/CREATIVE/IMPLEMENT)配合可视流程图提供持久记忆并引导结构化开发流程。与 Light 的'纪律驱动+阶段流程'思路相近。 | 3k | 2025-12-05 (0.8-Beta) | 强:模式化流程+可视流程图,把记忆嵌入开发阶段,纪律性较强。弱:绑定 Cursor、面向编码;无科研全链路(idea→实验→论文→投稿)模型,无跨项目 lessons 复用与中文启动提示词。 |
| [zilliztech/memsearch](https://github.com/zilliztech/memsearch) | 面向 Claude Code/Codex 等的统一持久记忆层,底层用 Markdown + Milvus 向量库,兼顾人读文件与语义检索。 | 2k | 2026-06-12 (v0.4.7) | 强:markdown 可读性 + Milvus 向量语义检索,正好补齐 Light 缺的'检索召回'能力。弱:通用记忆层,无科研项目状态字段与产物台账,不做决策/版本/术语的领域化结构,无会话交接协议。 |
| [alioshr/memory-bank-mcp](https://github.com/alioshr/memory-bank-mcp) | 受 Cline Memory Bank 启发的 MCP 服务器,把 memory bank 集中化为远程多项目管理,支持跨项目隔离的记忆文件读写。其'多项目隔离'与 Light 的 db09 项目 namespace 思路一致。 | 911 | unknown | 强:把 memory bank 服务化、支持多项目集中管理与隔离,可远程访问。弱:仍是通用编码记忆,无科研语义模型、无衔接卡/启动提示词、无 lessons 上浮,纯存储无纪律强制。 |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Claude Skills 的精选清单与生态索引,收录大量面向 Claude Code 的技能/资源,是观察同类 agent skill 前沿的入口。 | 13.4k | 2026-02 (badge);最新条目约 2025-11-13 | 强:生态全景、发现性好,可定位最新同类技能。弱:本身是清单非功能实现,不提供记忆/项目管理能力;可作为 Light 对标与吸收新范式的情报源。 |

### Light 该技能可借鉴的点
- 引入语义/向量检索补齐纯文件链的召回短板:可借鉴 memsearch(Markdown+Milvus)与 cognee(知识图谱),在保留 db09 人读 markdown 权威源的同时,对 decision_log/lessons/terminology 建轻量向量索引,让'立项前检索复用'从全文 grep 升级为语义查找。
- 借鉴 LangGraph checkpointer/Store 与 mem0 的标准化持久化抽象,把'触发→写入对照表'从纯约定固化为可被 hook 半自动触发的写盘动作(每次进展后自动追加 decision_log 草稿,人工确认入库),降低纪律靠自觉的失败率。
- 参考 Letta/mem0 的自动事实抽取,在会话收尾生成衔接卡时自动从对话里抽取候选'关键事实/决策',提示用户确认是否写入项目级状态,减少漏记。
- 学习 cursor-memory-bank 的可视化流程图(VAN/PLAN/IMPLEMENT 模式),给 m01–m17 全链路加一张项目状态可视图,让 next_actions 与产物台账的关系一目了然。
- 对标 basic-memory 的 Obsidian 兼容双向链接,让 project_card/decision_log/version_history 之间、以及跨项目 lessons 之间用可点击链接互联,提升长期项目的可导航性。
- 借鉴 memory-bank-mcp 的多项目集中管理思路,考虑把 db09 的项目 namespace 暴露为一个轻量 MCP/CLI,实现跨项目记忆的统一检索与隔离访问,而不仅是目录约定。
