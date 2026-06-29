# light-orchestrator — 深度分析与同类对标

> 源：[`skills/light-orchestrator/SKILL.md`](../../../skills/light-orchestrator/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：科研全流程的"调度+把关+断点续跑"指挥层——自己不干活,只负责裁链路、卡检查点、记台账(passport)、做阶段交接,让跨技能大任务可中断可恢复。

## 核心运行逻辑
把"声明式的技能组合链路"变成可执行流程:接到跨≥3阶段的大任务或"继续/刚断了"信号时启动,按 CONVENTIONS §6 科研主线裁出一条 pipeline,逐阶段调用 m01-m17/a03 等技能。它本身不写作不画图不分析,只做四件事:规划阶段计划表、在阶段间设两类检查点(决策点🧑交用户拍板、确认点✓机器闸门先验)、把每阶段产物+闸门结果+用户决策写入 .light/passport.yaml 台账、在阶段切换/暂停时按 a02 协议留衔接卡+启动提示词。断点恢复时用"六探针"(git/todo/passport/transcript/脏文件/恢复摘要)拼出当前事实状态再续跑,严禁凭聊天记忆猜进度或重跑已完成阶段。设计上刻意"不接管研究判断"——借鉴调度形态但所有研究决策都退回用户。

## 关键步骤
- 1. 判别任务类型:跨阶段大任务→pipeline;继续/刚断了→断点恢复;单一动作→直接路由单技能(宁可少编排)
- 2. 若断点恢复:先跑六探针(工作区版本/任务单/passport台账/对话交接/脏文件/恢复摘要)拼出当前事实,不可用探针标 unavailable 不硬阻断
- 3. 若新 pipeline:从 CONVENTIONS §6 主线裁链路(链路A数据到论文12步/链路B投稿返修/链路C成果转化),产出阶段计划表先给用户确认
- 4. 逐阶段执行:调用对应技能→产物落盘(命名以 CONVENTIONS §6.1 为单一真相源)→过该阶段检查点→才进下一阶段
- 5. 检查点把关:决策点停下让用户选分支;确认点跑 a08/a07/a10 闸门出 PASS/FAIL 报告,Critical 默认阻断,最多2轮整体返修,仍不达标转'已知局限'如实记录
- 6. 每过一阶段当场把 input/output/artifacts/gate/gaps 追加进 .light/passport.yaml 并刷新 updated
- 7. 阶段切换默认触发 T3 会话衔接:落衔接卡到 .light/handoff/ + 打印启动提示词,不等上下文耗尽

## 自带资产
- SKILL.md — 主文件:何时启动/不启动的判据、0断点恢复协议、1-5五大职责(规划/契约/检查点/台账/交接)、边界与自检清单
- references/pipelines.md — 三条具体链路(A数据到论文/B投稿返修/C成果转化)定义、∥可并行段标注、裁剪原则、阶段工件契约镜像表
- references/checkpoints.md — 两类检查点机制详解、各阶段闸门对照表(含Critical阻断条件)、2轮返修细则、六探针全文
- references/passport.md — 台账 YAML 字段规范、完整示例、存储位置约定(.light/passport.yaml)、维护规则、与 memory-pm 的分工

## 优点
- 职责边界极克制且自洽:明确'不亲自干活、不替用户做研究决策',把 idea选择/venue/结论都设为决策点,避免了编排器越权下结论这一常见失控模式,且该边界有 docs/design 设计决策记录背书
- 断点恢复协议是真亮点:六探针强制以 git/passport/db09/CI/todo 客观证据重建状态,显式禁止'凭聊天记忆说应该到X了',并区分'已完成未提交/已提交未推送/等CI/CI失败'四态,工程上可落地
- 诚信闸门不可绕过且有反作弊设计:确认点要求证据必须'新鲜'(当轮命令输出/diff/CI/selftest),写作第8步和引用第11步设强诚信门默认阻断,2轮修不好转'已知局限'而非假装修好——直接对抗 LLM 谄媚和幻觉
- 台账(passport)设计具体可执行:YAML schema 含 round 字段记 m03⇄m04 回环轮次、created/updated 双时间戳判新旧、FAIL→PASS 要记修复原因,且明确是 a07 consistency 回扫的权威产物清单,形成数据闭环
- 单一真相源纪律严格:工件命名反复指向 CONVENTIONS §6.1、self-review 力度指向 light-self-review 分级档、交接格式收编进 a02 两件套,明确'本技能不再自带摘要格式避免口径分裂',防止文档漂移
- 裁剪与分级原则务实:'宁可少编排不可为编排而编排''有数据不等于知道gap调研不能跳',并标注了∥可并行段(图表与引用、PPT与排版),不是死板全跑

## 缺点 / 可被质疑处
- pipelines.md 的'阶段工件契约镜像表'与 CONVENTIONS §6.1 实际内容并非镜像而是超集:镜像表多出 evidence table、split/manifest、draft.md、GAP台账、m12排版日志、m14 response_matrix 等 §6.1 没有的工件。SKILL 声称'与§6.1不一致以后者为准',但读者无法判断这些多出项是'§6.1遗漏待补'还是'镜像表越权新增',真要改名时到底改哪张表存在歧义,反而违背了单一真相源初衷
- 零脚本零模板:整个技能没有任何可执行资产。passport.yaml 的读写、六探针的执行、衔接卡递增编号(S<NN>)、台账 schema 校验全靠 LLM 手工按文字描述执行,没有 init_passport.py / validate_passport.py / resume_probe.sh 之类工具,一致性和可靠性完全依赖模型自觉,长任务里极易漂移或字段填错
- '2轮整体返修'的轮次计数缺乏持久化锚点:规则说'同一阶段最多2轮',但跨会话中断后(换天续跑),新会话如何知道某阶段已经修过几轮?passport 的 gate 字段示例只记最终 FAIL→PASS,没有 round_of_revision 计数字段,断点恢复后可能重置返修配额或无限返修
- 检查点闸门与各技能的耦合是'声明式假设'而非验证:表中写'数据评估→a10+a08+check_access_level.py''写作→m07 integrity_gate''引用→m10 verify_citation_edge',但 orchestrator 无法确认这些下游闸门真的存在且会按预期返回 PASS/FAIL。若某技能没实现对应 gate,编排器会静默地'确认通过'一个根本没跑的闸门
- 断点恢复的 transcript 探针实践性存疑:协议要求'缓存路径/会话标题/项目slug与当前仓库或db09项目名明确匹配'才检索,但没给出任何具体的 transcript 存储位置、命名规则或检索命令示例,这个探针在真实环境里大概率永远落到 unavailable,等于形同虚设
- 对'并行段'只有概念标注没有执行机制:链路A标了第10/11步∥可并行、链路C标了PPT与排版∥,但单会话单线程的 LLM 实际无法真并行,文档也没说清串行环境下并行标注除了'不必空等'还有什么操作含义,容易让人误以为有调度能力

## 可优化点（供后续逐技能优化）
- 补一个 scripts/passport.py:提供 init/append-stage/get-current-stage/validate 四个子命令,把台账读写从'LLM手填YAML'变成工具调用,顺带做 schema 校验(必填字段、stage 序号连续、gate result 枚举合法),消除手填漂移
- 在 passport schema 增加 revision_rounds 计数字段(per-stage),并在 checkpoints.md 明确'断点恢复后从 passport 读已用轮次而非重置',堵上跨会话返修配额被刷新的漏洞
- 把 pipelines.md 的'镜像表'从超集改成真正的逐字镜像,或反过来:把镜像表多出的中间工件(evidence table/split manifest/GAP台账/排版日志/response_matrix)正式提案补进 CONVENTIONS §6.1,使两表内容完全一致;无法合并的执行视角细节(上游输入/下游)用脚注挂在 §6.1 同名行下,而非另起一张内容不同的表
- 给确认点加'闸门存在性预检':执行某阶段确认点前,先验证下游技能确实声明了对应 gate(可读该技能 SKILL.md 的产出/闸门节),缺失则报'该阶段闸门未实现'并降级为人工确认,而不是静默判 PASS
- 为断点恢复六探针配一个 scripts/resume_probe.sh(git status/log/branch/remote/gh run list 一次性打包输出),并在 checkpoints.md 给出 transcript 探针的具体落地示例(常见 Claude/Codex 缓存路径模式 + 关键词检索命令),让 transcript 探针从'纸面'变可操作
- 在 SKILL 增加一个最小化的端到端 example(examples/):走一遍'用户给数据集→裁链路A→第4步idea决策点→第8步诚信门FAIL一轮修复→留衔接卡'的完整 passport.yaml 演进快照,让模型有可模仿的执行轨迹而非只有规则
- 澄清并行段语义:在 pipelines.md 注明'∥仅表示无数据依赖、可由不同会话/不同人分线推进或任意先后串行,单会话按标注顺序串行执行即可',去掉对'并行调度能力'的暗示

## 与其他 Light 技能/知识库的衔接
作为 Light 技能体系的总调度层,几乎与所有技能衔接。上游真相源:强依赖顶层 CONVENTIONS.md——§6 科研主线(裁链路依据)、§6.1 工件契约(命名单一真相源,已验证存在且有双向声明机制)、§9 会话衔接(T1-T4触发)。横向调度:按阶段调用 m01-m17 全部主线技能 + a03 backend-coding(实验)。常驻闸门落点:确认点显式调用 a08 self-review(且力度按其分级执行档,口径在 light-self-review)、a07 consistency(passport 的 artifacts 路径并集正是 a07 变更广播的权威回扫清单,形成数据闭环)、a10 research-ethics;数据阶段还调 light-data-engineering 的 check_access_level.py(已验证存在)。交接格式:完全收编进 a02 memory-pm 的两件套,直接复用其 templates/handoff_card.md 与 handoff_prompt.md(均已验证存在),并把台账纳入 a02 项目记忆/db09 项目卡。无 passport 的轻项目则退回 db09 version_history.md。设计边界记录挂在仓库 docs/design/(未随安装分发)。本身 user-invocable:false,由 ROUTER 按"继续/刚断了 vs 继续写/继续润色"区分触发。

---

## GitHub 同类前沿技能对标

light-orchestrator 的独特定位是"只调度不干活"的纯指挥层 + 科研场景专用 + 以 passport.yaml 台账和"六探针"做断点续跑。GitHub 上的同类项目几乎都偏向另外两个方向之一:要么是"重执行框架"(claude-flow/BMAD/wshobson agents——既调度也派子 agent 真干活,面向软件开发),要么是"重基建"(tidebase/spec-workflow-mcp——提供 checkpoint/状态持久化的底层引擎,但不含科研链路裁剪逻辑)。真正同时具备"声明式链路裁剪 + 人类决策点回退 + 文件化可恢复台账"三件套、且刻意不接管研究判断的开源技能,目前几乎找不到对等物——这是 Light 的差异化空白点。科研域的同类(paper-writer-skill、deep-research-skill)是"单条流水线执行者",而非跨技能调度层,二者更多是被编排对象而非竞品。Light 最该补的短板是:这些热门项目普遍有可视化看板/MCP 状态面板、子 agent 实际派活能力、以及社区分发(marketplace)机制,而 Light 目前是纯文本约定。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | Claude Code 的 agentic skills 框架 + 软件开发方法论,把技能组织成可复用的工作流体系,是目前最火的 agent skills 集合之一。 | 226114 | 2026-06-12 | 强:生态体量与方法论成熟度碾压,技能编排/复用机制完善,社区分发强。弱:面向通用软件开发而非科研主线,没有 passport 式文件台账+六探针断点续跑,也没有'决策点回退用户'这种刻意不接管判断的把关设计。 |
| [github/spec-kit](https://github.com/github/spec-kit) | GitHub 官方的规范驱动开发(Spec-Driven Development)工具包,把需求→设计→任务→实现拆成阶段化流程,支持多种 AI agent。 | 111782 | 2026-06-11 | 强:官方背书+超高人气,阶段化 spec 流程标准化,跨 agent 通用。弱:本质是软件开发的 spec 流水线,没有科研链路裁剪,没有运行时检查点/断点恢复台账,阶段交接靠文档而非可执行的 passport 状态机。 |
| [ruvnet/claude-flow](https://github.com/ruvnet/claude-flow) | Claude 的 agent 编排/meta-harness 平台,部署多 agent swarm、协调自主工作流,带自适应记忆、swarm 智能、RAG、原生 Claude Code 集成。(仓库已改名 ruflo,原链接重定向可达) | 59182 | 2026-06-12 | 强:真正的多 agent 并行编排+持久记忆+swarm,执行力远超 Light。弱:它'既调度又派活'且面向通用/开发任务,重而复杂;Light 的轻量'只调度+把研究判断退回用户'的克制设计反而更适合科研可控场景,claude-flow 缺少显式人类决策闸门。 |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | Breakthrough Method for Agile AI-Driven Development:用 PM/架构师/开发等角色 agent 做多阶段敏捷规划与执行的编排框架,近期引入 spec kernel distiller 等 skill。 | 49033 | 2026-06-12 | 强:多阶段规划+角色分工成熟,planning 形态与 Light 的'阶段计划表'最接近,社区活跃。弱:面向软件交付而非科研主线,阶段产物没有 passport.yaml 式机器可读台账,也没有'六探针重建事实状态'的断点续跑机制,恢复仍偏靠上下文。 |
| [wshobson/agents](https://github.com/wshobson/agents) | 面向 Claude Code/Codex/Cursor 等的多 agent 编排插件市场,提供大量专职 agent 与自动化编排模式。 | 36675 | 2026-06-12 | 强:agent 数量与跨工具覆盖广,marketplace 分发机制是 Light 没有的。弱:是'agent 仓库+编排'而非带检查点/台账的续跑指挥层,缺少科研链路裁剪和决策点/确认点两类闸门的把关语义。 |
| [Pimzino/spec-workflow-mcp](https://github.com/Pimzino/spec-workflow-mcp) | 提供结构化 spec 驱动开发流程的 MCP server,带实时 Web 看板和 VSCode 插件,可监控/管理项目阶段进度。 | 4226 | 2026-05-05 | 强:有实时可视化看板+IDE 集成,阶段进度可视,这正是 Light 纯文本约定缺的。弱:软件开发域,无科研链路;它管'spec 进度'但不做跨技能 pipeline 裁剪,也没有 Light 那种用户决策回退+机器确认点的双闸门和断点探针。 |
| [SkyworkAI/DeepResearchAgent](https://github.com/SkyworkAI/DeepResearchAgent) | 分层多 agent 系统:顶层 planning agent 协调多个专职下层 agent,做深度研究与通用任务的自动分解与执行。 | 3453 | 2026-05-04 | 强:顶层规划+任务分解的'调度层'形态与 Light 神似,且面向研究任务,执行力强。弱:它是全自动分解执行(agent 自己拍板),恰恰相反于 Light'所有研究决策退回用户'的设计;无文件化 passport 台账与可中断可恢复的人机交接协议。 |
| [cexll/myclaude](https://github.com/cexll/myclaude) | 跨 Claude Code/Codex/Gemini/OpenCode 的多 agent 编排工作流配置集。 | 2689 | 2026-05-04 | 强:跨多个 CLI 工具的编排配置,通用性好。弱:偏开发工作流模板,无科研主线裁剪、无 passport 台账与六探针断点续跑、无显式人类决策闸门。 |
| [199-biotechnologies/claude-deep-research-skill](https://github.com/199-biotechnologies/claude-deep-research-skill) | Claude Code 的企业级深度研究技能,8 阶段研究流水线 + 来源可信度评分 + 自动校验。 | 766 | 2026-04-11 | 强:科研域,且阶段化流水线+来源校验做得扎实,是 Light 检查点'确认点✓'可借鉴的范本。弱:它是'单条流水线执行者'而非跨技能调度层,流程写死 8 阶段不做动态裁剪,且不含断点恢复台账与人类决策点回退——更像被 Light 编排的对象。 |
| [BlueprintLabIO/tidebase](https://github.com/BlueprintLabIO/tidebase) | AI agent 的开源 checkpoint 层:checkpoint/replay、持久队列、cron、取消、human-approval gate、live state,跑在自己的 Postgres 上。 | 1 | 2026-06-12 | 强:这是与 Light 'passport 台账+断点续跑+人类闸门'机制最对位的项目,且把 checkpoint/replay/approval gate 做成了真正的持久化引擎(数据库级),比 Light 的文件 yaml 更工业级。弱:极早期(star 个位数),是底层基建无科研语义、无链路裁剪;Light 是开箱即用的科研技能而非基建库。 |
| [kgraph57/paper-writer-skill](https://github.com/kgraph57/paper-writer-skill) | Claude Code 的全流程学术论文写作技能(IMRAD 结构、文献管理、质量检查清单)。 | 29 | 2026-06-10 | 强:科研域同行,质量检查清单与 Light 的'确认点'闸门思路一致。弱:单技能写作流水线,不做跨技能调度/裁链路,无台账与断点续跑——属于 Light 会去编排的下游技能而非竞品。 |

### Light 该技能可借鉴的点
- 可视化状态面板:spec-workflow-mcp 用实时 Web 看板+VSCode 插件展示阶段进度,Light 的 passport.yaml 可加一个只读 dashboard 或 MCP 端点,让用户一眼看到检查点/闸门状态,而不只读文本台账。
- 持久化 checkpoint 引擎化:tidebase 把 checkpoint/replay/human-approval gate 做成数据库级持久层。Light 的'六探针重建事实状态'可借鉴其 replay/idempotency 思路,把断点恢复从启发式探测升级为可确定性重放。
- 来源可信度评分+自动校验闸门:199-biotechnologies/claude-deep-research-skill 的 8 阶段流水线带 source credibility scoring,可作为 Light'确认点✓机器闸门'的具体校验项模板(尤其填卡/引用核验场景)。
- 角色化阶段规划:BMAD-METHOD 用明确角色 agent 承载每个阶段,Light 的'阶段计划表'可借鉴其角色-产物-验收的结构化模板,让阶段交接卡更标准。
- 声明式链路+人类闸门并存:claude-flow/DeepResearchAgent 都偏全自动,Light'决策退回用户'是差异优势,但可借鉴它们的链路声明 DSL 形式,让 pipeline 裁剪规则更显式可配置而非埋在 CONVENTIONS 文本里。
- 社区分发机制:wshobson/agents 与 superpowers 的 marketplace/打包分发,提示 Light 可考虑把 orchestrator 与被编排技能做成可安装包,降低被复用门槛。
