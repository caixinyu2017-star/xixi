# light-review-rebuttal — 深度分析与同类对标

> 源：[`skills/light-review-rebuttal/SKILL.md`](../../../skills/light-review-rebuttal/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：投稿前模拟严苛审稿 + 收到真实意见后逐条返修的双模技能,以顶会官方评审表为锚点,内置抗谄媚让步门槛、提交前自我复审闭环,并能用 OpenReview 真实语料校准刻薄度。

## 核心运行逻辑
技能分两模式:模式一(投稿前模拟审稿)按论文类型择一套 rubric(NeurIPS 官方表/GRADE+Cochrane/ScholarEval 8 维,强调不叠加),扮 3-4 位非重叠视角审稿人出具对齐 NeurIPS 字段的评审,核心机制是 Sprint Contract 两段式(先 paper-blind 定 rubric 再 paper-visible 打分)防倒推、魔鬼代言人对每条辩解先打 1-5 分再回应防谄媚、以及主动规避 PRISM 五大 LLM 审稿通病。模式二(真实返修)区分会议 rebuttal(限页禁新实验)与期刊 response letter(逐点鼓励补实验)两种相反语境,用 concession 1-5 评分决定让步姿态(只有≥4 才实质让步、禁连续让步),并强制建立承诺账本和提交前 re-review 闭环核实每条声称是否真落地。设计思路是把"会被说服/会幻觉/会和稀泥"的 LLM 评审行为用证据门槛和可溯源核验约束成结构化决策。

## 关键步骤
- 1. 模式一-定 rubric:按论文类型择一套打分体系(不叠加),攻击方法学时统一过 GRADE/Cochrane 偏倚子清单
- 2. 模式一-两段式打分:先 paper-blind 定各维预期(防倒推),再 paper-visible 由 3-4 位审稿人画像(主编/方法学R1/文献R2/魔鬼代言人)按 NeurIPS 字段出具 Summary/Strengths/Weaknesses/Questions/打分
- 3. 模式一-自查:规避 PRISM 五通病,可选用 fetch_openreview.py 抓真实语料校准刻薄度与打分分布
- 4. 模式二-解析:逐条拆审稿意见识别真实关注点+分类,建立承诺账本登记每条承诺
- 5. 模式二-策略:对每条质疑打 concession 1-5 分决定接受/补实验/反驳/折中,禁连续让步,多审共同质疑=最高优先级
- 6. 模式二-写 letter:用 response_letter_template.md 按 R→A→C 格式逐点回应(会议/期刊选对应区块),新引文献过三索引核验
- 7. 模式二-改论文:同步改正文交 m07/m08,颜色标注修改
- 8. 模式二-自我复审:用 rereview_checklist.md 对每条 Priority-1 独立核实 FULLY/PARTIALLY/NOT/WORSE/🔍,过承诺账本与分数轨迹,最终放行门
- 9. 落盘:逐条意见↔回应↔改动产出 response_matrix.md 交 m12

## 自带资产
- SKILL.md — 双模主流程,内含 rubric 选择表、审稿人画像、concession 让步策略、会议vs期刊语境区分、OpenReview API 取数坑位详解、消费 m08 findings 的字段映射
- references.md — 11 节逐工具核查笔记(2026-06),覆盖 academic-paper-reviewer/OpenReview API 实测/PRISM/grill-me/会议rebuttal规则/NeurIPS评审表/ScholarEval/GRADE+Cochrane/critique-audit/返修内部协议,每条标【是什么/可复用方法/链接/已知坑】并诚实标注未能核实项
- scripts/fetch_openreview.py — 纯标准库抓 OpenReview 公开评审语料,走 directReplies 规避 venue 级审稿 invitation 永远空的坑,统计 rating 分布+weakness 高频词,带 --selftest 离线自检
- scripts/rebuttal_budget.py — 纯标准库会议 rebuttal 字数/页数预算检查,中英混排分别计词+markdown 去噪+PASS/WARN/FAIL 退出码,带 venue 预设与 --selftest
- templates/response_letter_template.md — 会议+期刊双模 response letter 模板,期刊段含变更摘要+R→A→C 逐点+Minor 归并,会议段含限页禁新实验铁律+General Response
- templates/rereview_checklist.md — 提交前自我复审清单,Priority-1/2/3 三表+承诺账本+分数轨迹+最终放行门

## 优点
- 语境区分精准且少见:明确点出会议 rebuttal(禁新实验/限页)与期刊 response letter(鼓励补实验)规则相反,并在 SKILL、模板、checklist、budget 脚本四处一致贯彻,避免了同类技能最常犯的'一套话术套所有 venue'错误
- 抗谄媚机制有真实约束力而非口号:concession 1-5 评分+'只有≥4 才实质让步'+'禁连续让步'+'用户反复施压不算有效证据',把 LLM 易被说服的倾向转成有证据门槛的决策;模式一对称地用 Sprint Contract 两段式防'看结论倒推评语'
- 提交前 re-review 闭环是真正的质量护栏:承诺账本(fulfilled/partial/not/explicitly-rejected-with-rationale)+独立核实声称位置+'已按建议修改'式空声称直接标🔍打回,直击 false success claims 这一核心反模式
- 两个脚本都是纯标准库、带离线 selftest、可直接跑,fetch_openreview 还把 OpenReview 'venue 级审稿 invitation 永远空、必须走 per-submission directReplies'这个 2026-06 实测坑写进代码并规避,工程上靠谱
- references.md 的诚实度高:tool 11 明确列出本环境网络拦截、未能逐字核实的目标,不编造端点;每条都带【已知坑】,可追溯到一手链接
- 与外部知识对齐扎实:rubric 锚定 NeurIPS/ICLR 官方表字段、PRISM 五通病、GRADE+Cochrane,不是凭空设计的打分维度
- 强调 rubric 不叠加(三套各有适用面,混用既冗余又自相矛盾),这是对'维度越多越严谨'的常见误区的正确纠偏

## 缺点 / 可被质疑处
- SKILL.md 信息密度过高、可执行性打折:模式一把 rubric 选择、4 个审稿人画像、NeurIPS 字段、GRADE 偏倚清单、PRISM 通病、Sprint Contract 全压在一屏内,执行时缺一个'最小可跑流程'。新手 agent 很可能只挑表面字段填,跳过两段式 paper-blind 这一最难也最关键的步骤——而该步骤无任何脚本/模板强制,纯靠自觉,极易被省略
- response_matrix.md 被指定为标准交接工件(产出节、衔接 m12),但全技能没有它的模板或字段 schema,只有 response_letter 和 rereview_checklist 两个模板;'逐条意见↔回应↔改动'三元组到底落成什么列、与 rereview_checklist 的 Priority 表是否重复,未定义
- rebuttal_budget.py 的 venue 预设几乎是空壳:iclr/neurips/cvpr 三个真实会议的 max_words 全是 0(回退 INFO 估页),只有 generic-1page 真有 650 词硬上限。也就是说对用户最常投的三个会,脚本实际只输出'未设上限'估页,WARN/FAIL 判定形同虚设,与 SKILL 里'FAIL 即超限、提交前必跑'的强承诺不符
- 三索引引用核验(Semantic Scholar/OpenAlex/Crossref)在 SKILL 和模板里被反复要求,但本技能没有实现脚本——它依赖 light-citation 的能力却未显式声明这一硬依赖,agent 可能既不会真去核验、也不知道该调哪个技能
- concession 评分与 re-review 判定主观性强且无校准:1-5 让步分、FULLY/PARTIALLY 判定全靠 LLM 自评,references 里 academic-paper-reviewer 提到的 calibration 模式(用金标准集测自身 FNR/FPR)在本技能完全没落地,'禁连续让步'也无任何机制核查(不像字数有脚本),实战中容易自我宽纵
- 魔鬼代言人'不打分只攻击'与模式一'3-4 位审稿人'的人数/组合关系略含糊:到底是 3 位打分+1 位 DA,还是 DA 算在 3-4 内,SKILL 与 references(5 画像)表述不完全一致,执行时审稿人配置可能漂移
- fetch_openreview.py 的 weakness 高频词分析过于初级:仅 lower-case 正则分词+一个手写小 stopword 表,产出的 top terms 对'校准刻薄度'帮助有限(method/results 这类词已在停用表但仍会出现大量无信息高频词),离'校准打分分布'的承诺有差距;且只抽第 1 条 rebuttal 前 300 字作样本,代表性弱

## 可优化点（供后续逐技能优化）
- 补 response_matrix.md 模板与字段 schema(意见ID/原文/分类/concession分/回应/改动位置/re-review判定/承诺状态),并明确它与 rereview_checklist 的关系(前者是交接全量台账,后者是放行门),避免两个工件字段打架;落盘命名对齐 CONVENTIONS §6.1
- 给模式一加一个'最小流程卡片'或编号步骤(1 选 rubric→2 paper-blind 写预期→3 paper-visible 打分→4 PRISM 自查),把现在散在段落里的 Sprint Contract 两段式提成不可跳过的显式 step,最好配一个轻量 blind-then-score 的 checklist 模板强制留痕
- 把 rebuttal_budget.py 的 iclr/neurips/cvpr 预设填上当年真实可核查的字符/页限(或显式改成 char 模式),至少给 ICLR 的 ~5000 字符/条这类已知框一个真判定;或在脚本里加 --max-chars 模式,让 SKILL 里'必跑+FAIL 拦截'的承诺真正成立
- 显式声明对 light-citation 的硬依赖:在三索引核验处写明'调 light-citation 的核验能力',或在本技能 scripts 下提供一个最小引用存在性核验脚本(arXiv/Crossref 无 key 查),避免核验沦为口头要求
- 落地一个轻量 calibration:提供 5-20 篇 OpenReview 已知决定的金标准小样本流程,让模式一跑完后自测'我的录用倾向 vs 真实 decision'的吻合度,把抽象的'刻薄度校准'变成可量化的自检;同时给'禁连续让步'加一个让步率统计的小脚本或 checklist 计数项
- 升级 fetch_openreview.py 的语料分析:rating 分布按 venue 给均值/中位数/accept 阈占比,weakness 词改用 bigram 或按官方子维(soundness/clarity 等)聚类,rebuttal 样本随机抽多条并按是否改判分层,真正支撑'校准打分分布与话术'
- 统一审稿人画像口径:在 SKILL 里固定写明'3 位打分审稿人(主编/方法学/文献)+1 位魔鬼代言人(不打分)',并与 references tool 1 的 5 画像差异给一句话说明(R3 跨视角可选),消除人数漂移
- 为模式一产出补一个评审报告模板(对齐 NeurIPS 字段),目前模式二有两个模板而模式一'模拟评审报告'无模板,产出格式全靠即兴

## 与其他 Light 技能/知识库的衔接
SKILL 显式声明的衔接:消费 m08(light-paper-polishing)的 polish.py/mechanical_check.py 结构化 findings(按 overclaim/ai_tone/passive 等 category 映射进 Weaknesses 子维,只读不回写),并引用其 findings_schema.md;模拟前可取 db02 的审稿人提问清单(patterns_library §11)作攻击维度起点。下游:模拟结果回 m07(paper-drafting)/m08(paper-polishing)/m09 改稿,真实返修联动 m05/m06(补实验)/m10/m12,全过程记入 db09(审稿意见与修改历史),标红稿生成依赖 light-typesetting 的 latexdiff。隐性未声明依赖:三索引引用核验实际依赖 light-citation 的能力但未在 SKILL 中点名,是衔接链上的缺口。rubric 字段复用 light-idea-critique/references.md 已记录的 NeurIPS 2024 评审表。

---

## GitHub 同类前沿技能对标

GitHub 上的同类项目主要分三类。一是自动审稿引擎(SakanaAI/AI-Scientist 的 perform_review、ecnu-sea/SEA、maxidl/openreviewer、Ahren09/AgentReview),偏研究系统或微调模型,产出一份机器评审或模拟多 agent 评审,但几乎不做投稿前自审加真实返修的双模闭环,也不内置抗谄媚让步门槛。二是新兴 agent skill(Imbad0202/academic-research-skills、ChanMeng666、Boom5426、wukeping99-svg),与 Light 形态最接近,走 Claude Code/Cursor 技能路线、多视角评审,但多为单向审稿或反馈,rubric 锚定和提交前 re-review 闭环弱。三是专门的 rebuttal 技能(Iayce/omnirebuttal、xiongqi123123/awesome-rebuttal),已具备按 venue 路由、证据门槛、禁造假等机制,与 Light 模式二高度重合且做得相当扎实。Light 的差异化在于把模拟审稿(模式一)加真实返修(模式二)合一,且独有 Sprint Contract 两段式防倒推、魔鬼代言人先打分后回应防谄媚、concession 1-5 让步门槛、PRISM 五大通病规避这套结构化抗偏差机制,这是其他项目普遍缺失的。纯做会议或期刊 rebuttal,Light 覆盖与 omnirebuttal 接近;但论模拟审稿严苛度校准加双模一体加反谄媚证据门槛,Light 设计更系统。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Claude Code 学术研究全流程技能套件(调研到写作到审稿到 pipeline 编排),含 Academic Paper Reviewer 子技能,主打 7-agent 多视角同行评审加 0-100 质量 rubric。形态与 Light 最像。 | 30710 | 2026-06-13 | 强:star 量极高、活跃、全流程一体、多 agent 评审。弱:偏单向审稿加写作,没有真实返修/response letter 的相反语境处理,缺 concession 让步门槛、提交前承诺账本 re-review 闭环和 Sprint Contract 两段式防倒推。 |
| [xiongqi123123/awesome-rebuttal](https://github.com/xiongqi123123/awesome-rebuttal) | 面向 AI 编程助手(Codex/Claude Code/Cursor)的项目级 rebuttal 技能包:在论文工作区存 rebuttal 记忆、分析审稿关切、规划补充实验、起草回复,带安全闸拦截无证据声称、伪造结果、匿名泄露。 | 220 | 2026-05-29 | 强:rebuttal 领域 star 最高,记忆持久化加反造假安全闸做得实,与 Light 模式二理念一致。弱:专注真实返修,不含投稿前模拟严苛审稿模式一,无 NeurIPS rubric 锚定与魔鬼代言人评分机制。 |
| [Iayce/omnirebuttal](https://github.com/Iayce/omnirebuttal) | 统一 agent skill,按 venue 格式自动路由 rebuttal(CV 单页 PDF、OpenReview 线程、ICML 字数限制、期刊逐点信、ARR/TMLR 滚动修订),9 步流程含 venue 调研、分诊、策略、补实验规划、起草、压缩、引用核验、QA。 | 3 | 2026-06-01 | 强:venue 路由精细度高(区分会议字数/页限与期刊逐点),引用核验加 QA 与 Light 思路一致。弱:star 极低、新生项目,仅做返修(无模拟审稿模式),无 concession 1-5 让步评分与禁连续让步这类抗谄媚约束。 |
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 全自动科研系统(产生 idea 到跑实验到写论文),内置 perform_review LLM 评审功能,输出总分、Accept/Reject、弱点列表,支持基于 ICLR 数据的批量评审分析。 | 13956 | 2025-12-19 | 强:影响力大、评审锚定真实会议标准、有批量校准数据。弱:评审只是科研流水线一环,产出单份机器评审,不做返修、不做多视角对抗、无抗谄媚让步门槛与提交前复审闭环。 |
| [Ahren09/AgentReview](https://github.com/Ahren09/AgentReview) | EMNLP 2024 论文官方实现,首个 LLM-agent 同行评审模拟:五阶段流水线含 reviewer、author、area chair 三类 agent,可配置性格特质以研究审稿偏见(报告 37.1% 决策偏差)。 | 118 | 2026-05-10 | 强:多 agent 角色加 area chair 链路完整,系统研究了审稿偏见,可作 Light 多视角非重叠审稿人的理论参照。弱:研究框架而非可复用技能,产出模拟评审用于研究分析,不面向作者投稿前自审或返修,无 rubric 不叠加与反谄媚机制。 |
| [ecnu-sea/SEA](https://github.com/ecnu-sea/SEA) | 自动论文评审框架,三模块 Standardization、Evaluation、Analysis,生成对作者有信息量、一致性高的评审反馈以帮助改稿。 | 89 | 2026-01-18 | 强:强调评审一致性(对应 Light 的刻薄度校准目标),有标准化对齐步骤。弱:学术模型或框架,单向产评审,无双模、无 venue 区分、无让步门槛与承诺账本。 |
| [maxidl/openreviewer](https://github.com/maxidl/openreviewer) | 开源同行评审生成系统,核心是 Llama-OpenReviewer-8B(在专家评审上微调),能读 PDF、按会议评审模板产出贴近人类标准的严苛评审。 | 11 | 2025-06-21 | 强:专用微调模型对齐真实会议模板,严苛度由数据驱动(与 Light 用 OpenReview 语料校准刻薄度同源思路)。弱:是模型或推理工具而非 agent 技能,只生成评审,不返修、无对抗多视角、无防谄媚结构。 |
| [ChanMeng666/academic-paper-review-skill](https://github.com/ChanMeng666/academic-paper-review-skill) | 可复用 Claude Code 技能,从两个视角(编辑视角加技术/领域视角)评审稿件,输出 Markdown/Typst/PDF,含 CeTZ 图表库与 Mermaid 模板,可产出叙述式审稿信或分级 audit 报告。 | 0 | 2026-06-07 | 强:技能形态与 Light 一致,多格式排版输出(含 PDF)是亮点。弱:0 star 新项目,只两视角且单向审稿,无真实返修模式、无 rubric 不叠加约束、无 concession 让步门槛与提交前复审。 |
| [Boom5426/Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills) | 面向高水平论文(Nature 级)写作与评审的 agent 技能集合,提供论文打磨加审稿视角辅助。 | 300 | 2026-05-08 | 强:有一定关注度、定位高端期刊。弱:偏写作打磨,审稿或返修结构化程度低,无 NeurIPS rubric 锚定、无双模与抗谄媚让步门槛。 |
| [wukeping99-svg/AI-research-feedback](https://github.com/wukeping99-svg/AI-research-feedback) | 面向科研反馈的 agent 技能或工具,模拟审稿意见给作者改进建议(AI research feedback)。 | 368 | 2026-04-16 | 强:有关注度,聚焦给作者可行动反馈贴近实战。弱:偏单向反馈,缺真实 rebuttal/response letter 的相反语境处理,无 concession 评分、承诺账本与提交前 re-review 闭环。 |
| [guruvamsi-policharla/paper-review-skill](https://github.com/guruvamsi-policharla/paper-review-skill) | Claude Code 论文评审技能,把稿件转成一份可信的同行评审意见。 | 15 | 2026-02-04 | 强:轻量、技能形态一致、易上手。弱:单一审稿功能,无多视角对抗、无返修模式、无防谄媚与 rubric 锚定机制,深度远低于 Light。 |

### Light 该技能可借鉴的点
- 多格式或可排版输出:借鉴 ChanMeng666 的 Markdown/Typst/PDF 加 CeTZ/Mermaid 模板,让评审信与 response letter 能一键导出投稿可用格式。
- venue 路由再细化:omnirebuttal 把 CV 单页 PDF、OpenReview 线程、ICML 字数限制、ARR/TMLR 滚动修订分别建模,Light 的会议 vs 期刊二分可拆得更细(字数、页数、线程格式自动适配)。
- 偏见的量化校准:AgentReview 报告了具体偏见决策偏差(37.1%)、openreviewer 用专家语料微调,Light 可在刻薄度校准中引入可量化的偏差基线与一致性指标,而非仅定性。
- 批量真实语料评测:AI-Scientist 的 iclr_analysis 批量评审分析,可启发 Light 用 OpenReview 真实评审做严苛度自检回归测试,验证模拟审稿是否过松或过严。
- 反造假安全闸工程化:awesome-rebuttal 把拦截无证据声称、伪造结果、匿名泄露做成显式安全 gate,Light 的承诺账本可升级为强制阻断式校验而非仅清单核对。
- 记忆持久化:awesome-rebuttal 在论文工作区存 rebuttal 记忆,Light 可与 light-memory-pm 联动,把多轮 rebuttal 或审稿历史结构化沉淀,支持跨轮次一致性。
