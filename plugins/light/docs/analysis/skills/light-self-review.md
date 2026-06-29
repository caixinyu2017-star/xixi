# light-self-review — 深度分析与同类对标

> 源：[`skills/light-self-review/SKILL.md`](../../../skills/light-self-review/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：所有 Light 技能的输出闸门:交付前用「证据闸门+借口拦截+三态判定」对产出做自我审查与迭代,先修后交,常驻但非用户直接调用。

## 核心运行逻辑
核心是把「自我审查」从含糊感受改造成可判定的工程流程,三根支柱:①证据闸门(借 verification-before-completion)——不下「完成/通过/修好」结论除非当轮有新鲜证据(当场重跑、读完整输出、查 exit code、数失败);②三态判定(✓/✖/!)+严重级(Critical/Important/Minor),与 Deepchecks condition、Cisco HIGH/MED/LOW 同构,把每项检查落到明确判定;③分级执行档——重产出跑全量 11 项清单,轻任务只跑「证据/事实/夸大」最小三项,解决「轻任务全跑则慢、整体跳过则失守」的真实矛盾。设计上大量「借」外部成熟技能(superpowers 四件套)而非自造,并用 excuse_intercept 表针对 LLM 临交付前最爱编借口跳验证这一心理弱点做拦截。开场即上强度(grill 规则)首句列三个最致命弱点,对抗自我放水。

## 关键步骤
- 1. 先判档:按产出量级显式判定命中哪条判据(≥1完整章节/含定量结论/对外交付/改代码/涉引用合规→全量档;其余→最小三项)
- 2. 过证据闸门:IDENTIFY 想清什么命令能证明→RUN 当场重跑不引用旧结果→READ 读完整输出查 exit code 数失败→VERIFY 确认输出真支撑结论→ONLY THEN 才下结论
- 3. 交付前扫借口拦截表:命中 26 条任一(改动小/应该能过/上次跑过/先交了等)即回证据闸门重跑,不自我放行
- 4. 跑自检清单:全量档逐项判通用 11 项(逻辑/事实/格式/表达/创新/引用/夸大/审美/重复/结构/可执行)三态,对照 self_check_contrasts 反例
- 5. 按产出类型补充检查:代码走红-绿/TDD+依赖安全;论文走同行评审维度+科学批判性思维+核心撞车终检;数据走统计/漂移;skill/MCP 走 prompt injection/数据外泄/含糊触发自查
- 6. 不通过项附严重级,致命问题排在格式问题前,先修后再验证拿新鲜证据
- 7. 失败循环熔断:同一问题修≥2次诊断根因、≥3次停手质疑架构
- 8. 接收外部反馈走暂停→核验→判定→行动,禁表演式同意、不清楚就停、范围纪律+YAGNI
- 9. 默认静默自检直接交付修正结果;无法自解的重大问题如实告知不隐瞒

## 自带资产
- SKILL.md — 主入口:工作方式、证据闸门、分级执行档、通用11项清单、按产出类型补充、失败循环、接收反馈、衔接
- references.md — 逐工具真实研究笔记(superpowers四件套/Deepchecks/Evidently/Snyk/Socket/Cisco两扫描器/Peer Review/科学批判性思维/Scholar Eval),带链接与已知坑,诚实标注未核实项
- references/excuse_intercept.md — 26条自我借口→真相拦截表,分A跳过验证/B缩小证据/C科研夸大/D反馈失败循环/E完成度审美五类
- references/walkthrough.md — 2个端到端走查示例(代码命中#5/#10、论文段落命中#14),演示草稿→拦截→重跑→✖判定→修→重验证→交付完整一轮
- references/receiving_feedback.md — 禁表演式同意措辞表、暂停核验判定行动四步、不清楚就停、反驳带证据、范围纪律+YAGNI、问题三级
- references/self_check_contrasts.md — 通用11项每项配一组最小✓/✖反例对照,把抽象检查变成可判别形态
- assets/self_review_checklist.md — 可勾选交付前清单(证据闸门+11项+借口自查+按类型补充+接收反馈+失败循环+收尾)

## 优点
- 证据闸门设计扎实且可操作:五步明确、强调当轮新鲜证据不许引用旧结果,并把抽象的『通过』量化为可核对的形态(测试=0失败输出、构建=exit 0、bug修复=原症状被测且通过、回归=红-绿循环)
- 分级执行档解决真实痛点:对轻改动只跑证据/事实/夸大三项,既不让全量11项拖慢轻任务,又避免整体跳过失守;判据『命中任一即全量』可显式判定,拿不准用重档的兜底合理
- excuse_intercept 表心理学上精准:针对 LLM 临交付前最爱编借口(should/probably、先交了再说、子代理说做完了)逐条给拦截动作,这是把『为什么会失守』而非只是『要做什么』讲清楚,实战价值高
- references.md 的诚实姿态稀有可贵:明确标注 audit/critique 技能官方无同名实现、Snyk 文档抓取403未逐条核验、厂商自述数据未独立验证、研究日期,不把社区实现冒充权威——这正是技能本身倡导的诚实
- 三态判定+严重级与真实工具同构(Deepchecks condition/Cisco分级/code-review三级),不是凭空发明,迁移成本低且有据可循
- self_check_contrasts 把每项抽象检查配最小✓/✖反例,杜绝『感觉还行』式自评;核心撞车终检(定稿前用核心结论再检索2库找最像那篇)是输出端兜底,呼应顶刊最怕的『假装首创』
- grill 规则(首句直列三个最致命弱点、禁缓冲句)对抗自我放水,严重级排序坚持致命问题排在格式问题前,避免陷入只挑表述的表面陷阱

## 缺点 / 可被质疑处
- 『常驻所有任务收尾』缺真实触发机制:user-invocable:false 意味着不靠用户调用,但全靠模型自觉记得在收尾时跑;除括号里提一句 light-orchestrator/checkpoints 外,无任何 hook/契约保证它真的被触发,『所有技能的输出闸门』是愿景而非强制
- 零可执行脚本:references.md 详列了 snyk/sfw/skill-scanner/deepchecks/evidently 的真实命令,但 scripts/ 目录不存在,一个反复强调『证据来自当场跑命令』的技能却不自带任何可跑的检查脚本,验证负担全压在模型手工重建命令+人工判断上,有自我矛盾之嫌
- 证据闸门对代码强、对文稿弱且不自知:exit code/失败数对论文不适用,『结论被结果支撑』本身又是 LLM 判断,而技能引用的1998实验恰恰证明评审者注意不到结论不被支撑——它引了这个坑却没给越过坑的机制,只停留在『要小心』
- 11项通用清单轴线重叠未去重:逻辑/事实重叠、创新/夸大/引用相关、结构/重复重叠,清单是平铺的(严重级排序只在处理阶段提),顶刊审稿人会指出它混淆了正确性轴与表面轴
- 大量跨技能引用(m04/m06/m10/m14/a03/a07/a10、light-orchestrator、light-backend-coding、CONVENTIONS §4)是裸标签,本技能内无法确认这些技能/章节是否存在、确切提供什么,链接缺失会静默断裂
- 分级判档本身是自判断,轻档可能变成新借口面(『这是轻任务』跳过全量);excuse_intercept 泛泛警告过自我放行,但分级机制恰恰新开了一个可被滥用的口子,未针对性堵
- 上下文成本:一个号称『每次收尾必跑』的常驻技能,SKILL.md 密集+6个引用文件,若每次全载开销大,却无『哪些常驻在上下文、哪些懒加载』的最小足迹指引;grill规则首句列三弱点若不按档收口,对琐碎改动也输出会很吵
- 无假阳性校准指引:引用的 skill-scanner 自承『无发现≠无威胁』且有误报,但本技能没给『判定某标记为非问题』时该如何带理由放行,既可能过度标记导致每次交付分析瘫痪,也可能随手忽略

## 可优化点（供后续逐技能优化）
- 补一个可执行检查脚本(scripts/run_checks.py 或薄封装):至少自动跑 build/test/lint 并输出 exit code+失败计数作为证据闸门的真实产物,产出是 skill/MCP 时封装 skill-scanner/snyk 命令,让『我跑过了』变成可附的工件而非叙述
- 明确触发契约:既然 user-invocable:false+常驻,写清到底由谁在何处调用(绑定 light-orchestrator 阶段间检查点,或定义『每个技能最后一步必调本技能』的契约),把现在的括号附注升级为可执行约定
- 为文稿类补证据闸门的外部替代:要求每条主张逐句引出结果中支撑它的原句(带行/表号定位),把『结论被结果支撑』从劝诫变成可核对动作,绕开 exit code 不适用的问题
- 按档收口 grill 规则与全量11项:轻档显式关闭『首句三弱点』开场以免琐碎改动噪声;在 SKILL.md 用一句话把 grill 规则限定到重产出档
- 把11项重组为正交轴并给死板优先序(正确性→表面),消除逻辑/事实、创新/夸大/引用、结构/重复的重叠,平铺清单改成分层
- 针对分级判档新开的借口面,在 excuse_intercept 增一条『这是轻任务所以不用全量』→真相(判据命中任一即全量,拿不准用重档),堵住自判档放水
- 加假阳校准条:任何标记为非问题的项要求一行带证据的放行理由,既防过度标记瘫痪也防随手忽略
- 解决悬空引用:确认 CONVENTIONS §4 与 m/a 系列技能的真实位置,加一个 manifest 或缺失降级守则,链接技能缺失时优雅退化而非静默断裂

## 与其他 Light 技能/知识库的衔接
作为所有 Light 技能的输出闸门(收尾时生效)。大量『借』obra/superpowers 四件套:verification-before-completion(证据闸门)、systematic-debugging(失败循环/根因,全文在 light-backend-coding/references/debug_protocol.md)、test-driven-development(红-绿/TDD)、receiving-code-review(接收反馈)。横向联动:a07(审美一致性)、a10(合规/伦理版权隐私)、m04(创新/审稿视角,与核心撞车终检同源)、m06(统计)、m10(引用)、m14(论文格式/审稿)、a03(代码安全)。被 light-orchestrator/references/checkpoints.md 按执行档在阶段间调用。引用 CONVENTIONS §4(反臆造规范,位置本技能内未确认)。工具侧依赖 Deepchecks/Evidently(数据漂移三态)、Snyk/Socket/Cisco MCP/Skill Scanner(代码与技能安全自查),但均以文字描述形式『借』,无封装。

---

## GitHub 同类前沿技能对标

Light 的 self-review 是一个「Agent 端、prose 形态、常驻输出闸门」——它不是跑代码的库,而是用提示词把「自我审查」改造成可判定流程(证据闸门+三态判定+借口拦截+分级执行),嵌在交付前自动触发。GitHub 上的同类生态分两层:一层是 Agent Skill / 方法论(obra/superpowers 的 verification-before-completion 正是 Light 明确「借」的母体,还有 reflexion/self-refine/CRITIC 这些学术自反思范式的工程化),它们与 Light 形态最接近但多为「单次反思循环」,缺 Light 的严重级分档与 excuse_intercept 这种针对 LLM 临交付编借口的心理拦截。另一层是 LLM 评测/护栏库(deepeval、deepchecks、guardrails、promptfoo),它们把「pass/fail condition、HIGH/MED/LOW」做成了可编程断言,正是 Light 三态判定的同构来源,但它们是外挂式 CI 工具,不在 agent 交付链路里常驻、也不做「先修后交」的迭代。Light 的独特定位是把这两层的思想压进一个轻量、零依赖、随每次交付自动跑的提示词闸门,并用分级执行档解决「轻任务全跑太慢/整体跳过失守」的真实矛盾——这一点在检索到的项目里几乎没有对应物。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md) | Claude Code 的 agentic 技能框架与开发方法论,内含 verification-before-completion 技能——交付前必须有新鲜证据(重跑/读完整输出/查 exit code)才能下结论,正是 Light self-review 证据闸门直接借用的母体。 | 226114 | 2026-06-12 | 强:生态庞大、被广泛采用,verification 技能是行业事实标准,Light 直接站在它肩上。弱:它是通用「完成前验证」单技能,没有三态判定+严重级分档、没有 excuse_intercept 借口拦截表、没有重/轻任务分级执行档,也不针对科研产出(夸大/引用/创新)定制。 |
| [anthropics/skills](https://github.com/anthropics/skills) | Anthropic 官方 Agent Skills 仓库,含 skill-creator 等,定义了 SKILL.md 规范与最佳实践,是所有同类技能(含 Light)的格式标准来源。 | 149996 | 2026-06-09 | 强:官方权威、规范定义者、含测试与评估技能的方法论。弱:不提供专门的「自我审查闸门」技能,更不涉及证据闸门/借口拦截这类对抗 LLM 自我放水的机制;Light 在其规范之上做了垂直深化。 |
| [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/reflexion) | 手工打造的 Claude Code 质量提升技能集,含 reflexion 插件(把学术 Reflexion 自反思范式工程化为可挂载的 agent 插件),跨 OpenCode/Cursor/Gemini CLI 通用。 | 1100 | 2026-06-13 | 强:同样是 agent 端、提示词形态、专注结果质量,reflexion 插件即「行动后反思」与 Light 理念高度同源,活跃维护。弱:reflexion 偏「失败后回顾改进」的循环,缺 Light 的可判定三态+严重级+证据闸门的硬约束,也无分级执行档与科研场景定制。 |
| [noahshinn/reflexion](https://github.com/noahshinn/reflexion) | NeurIPS 2023 Reflexion 官方实现:agent 对任务反馈做语言化自我反思并存入情节记忆,提升后续尝试表现,是「自我反思」范式的奠基开源实现。 | 3180 | 2025-01-14 | 强:学术奠基、被大量引用,提供了「自我反思能提升表现」的理论与实证基础。弱:是研究代码/任务 benchmark 实现而非可即插的交付闸门,跨任务记忆而非单次交付前硬验证;Light 把它的思想落成了可判定、可拦截借口的工程清单。 |
| [microsoft/ProphetNet (CRITIC)](https://github.com/microsoft/ProphetNet/tree/master/CRITIC) | CRITIC 框架:LLM 借助外部工具(搜索/代码解释器/计算器)验证并修正自身输出,模拟人类用外部资源校验而非只靠内部知识。 | 748 | 2024-07-25 | 强:核心主张「不靠内部直觉、要用外部证据验证」与 Light 证据闸门思想完全同构,且强调工具实证。弱:研究实现、已较少更新,聚焦事实纠错单点,没有三态/严重级/分级执行的交付流程,也非常驻 agent 技能。 |
| [Thomaszhou22/self-refine-skill](https://github.com/Thomaszhou22/self-refine-skill) | 把 Self-Refine 论文做成的 agent 技能:GENERATE→CRITIQUE→REFINE→CHECK 系统化自反思,零 API 成本,兼容 Claude Code/Cursor/Copilot/Codex 等。 | 3 | 2026-05-21 | 强:形态最像 Light——同为提示词技能、含 CHECK 闸门、跨平台、先批评后精修(先修后交)。弱:star 极少、影响力小,CRITIQUE 偏通用文本质量,无证据闸门(新鲜证据强制)、无 excuse_intercept、无严重级与重/轻分级,科研维度缺位。 |
| [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills) | Claude Code 插件套件,覆盖完整交付生命周期:多模型 AI 评审、代码审计、quality gates(质量闸门)、文档生成等,含 hash 校验编辑等 MCP。 | 488 | 2026-06-10 | 强:明确含「quality gates」与多模型交叉评审,工程化程度高、有 MCP 加持,质量闸门定位与 Light 相近。弱:面向软件交付管线而非科研产出,闸门偏 CI/代码维度,无针对 LLM 自我放水的借口拦截心理设计,也无轻任务最小三项的分级。 |
| [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | LLM 评测框架,把输出质量做成可断言的 metric/测试用例(类 pytest),支持 pass/fail 判定与 CI 集成,广泛用于 LLM 应用回归。 | 16130 | 2026-06-10 | 强:成熟、活跃、生态大,pass/fail 断言把「判定」彻底工程化,远比 prose 清单可量化可回归。弱:是离线/CI 评测库,不在 agent 交付链路常驻,不做「自己发现问题→当场修→再交」的闭环;Light 是 in-the-loop 自审而非外挂打分。 |
| [deepchecks/deepchecks](https://github.com/deepchecks/deepchecks) | 数据与模型持续验证库,核心是 Check+Condition(每个检查带明确 pass/fail/warn 条件),从研究到生产做整体校验。 | 4023 | 2025-12-28 | 强:Condition 的 pass/conditionally-pass/fail 正是 Light 三态判定(✓/!/✖)明确引用的同构来源,标准化程度高。弱:面向 ML 数据/模型而非 agent 文本交付,需写代码、跑离线套件,不是随交付自动触发的轻量提示词闸门。 |
| [guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails) | 为 LLM 输出加「护栏」:用可组合的 validator 在输出层做结构/质量/安全校验,失败可重询或修正(类输出闸门)。 | 6999 | 2026-06-13 | 强:输出层闸门+失败重试的理念与 Light「先修后交」相通,validator 可编程、可拦截不合格输出,活跃。弱:是程序化中间件、面向 API 集成而非 agent 自我审查的提示词,关注 schema/安全合规多于科研论证质量与夸大/引用维度。 |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | 提示词/agent/RAG 测试与红队工具,声明式配置做断言、对比多模型、可接 CI/CD,被 OpenAI、Anthropic 使用。 | 22156 | 2026-06-13 | 强:工业级、活跃、断言+红队覆盖广,把「输出是否达标」做成可重复回归。弱:开发期测试工具而非交付时常驻自审,需配置与外部跑;Light 是 agent 内省式、零配置、每次交付即跑的轻量闸门,定位互补而非重叠。 |

### Light 该技能可借鉴的点
- 把 prose 检查项进一步「可编程化」:像 deepeval/deepchecks 那样为关键检查项写出可机读的 pass/fail condition 表达式(哪怕只是结构化清单),让三态判定从「LLM 自评」逐步可回归、可被外部断言复核,降低自我放水空间。
- 引入 deepchecks 的 conditionally-pass(警告但不阻断)语义边界定义:明确「! 警示态」何时降级为可放行、何时升级为阻断,给三态之间画出更硬的判定线。
- 借鉴 self-refine-skill 的显式 GENERATE→CRITIQUE→REFINE→CHECK 命名循环,把 Light 的「先修后交」迭代步骤显性编号,便于 agent 自我追踪迭代轮次与收敛判据(避免无限自我修补)。
- 参考 promptfoo/guardrails 的失败重询+重试上限机制,为 self-review 增加「最多 N 轮自修后仍 ✖ 则上报用户而非硬交付」的熔断规则,防止在 Critical 项上反复打补丁(契合系统提示的 failure-loop 识别)。
- 借 CRITIC 的工具实证主张,把证据闸门里『新鲜证据』的来源清单显式化(重跑命令/读完整输出/查 exit code/外部检索),并要求附上证据出处,而非仅声明『已验证』。
- 参考 reflexion 的情节记忆:把每次被拦下的失败模式(尤其 excuse_intercept 命中的借口)写入 MEMORY,形成项目级『常犯借口/常漏检查』累积库,让分级执行档随项目自适应加项。
- 对标 levnikolaevich 的多模型交叉评审,在重产出档可选『换一个视角/模型再审一遍』,降低单模型自审的同源盲区。
