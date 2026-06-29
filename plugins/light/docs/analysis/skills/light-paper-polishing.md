# light-paper-polishing — 深度分析与同类对标

> 源：[`skills/light-paper-polishing/SKILL.md`](../../../skills/light-paper-polishing/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：以"深层论证优先于表层语言"为核心的审稿人视角论文分模块润色技能，配三个可直跑的离线/在线检测脚本，把"挑刺"落成结构化发现并喂给下游模拟审稿。

## 核心运行逻辑
核心设计是"两层 + 四步"。两层：表层(语言/术语/句式/可读性)和深层(逻辑/论证/结构/创新点呈现)，明确"深层优先——审稿人拒稿很少因为语法"。四步流水线 distill(抓核心贡献)→critique(审稿人五问列弱点)→polish(语言层四查逐模块改)→audit(一致性/术语/格式/引用终检)。方法论有真实出处：审稿五问(soundness/novelty/clarity/reproducibility/related-work)综合 Elsevier + NeurIPS 式评审；语言四查借 Grammarly 四分法但弱化 engagement;引言四段式与"贡献三处一致"取自彭思达写作笔记;深层改法落成 Claim-Evidence-Boundary 三件套 + Hedging 校准阶梯。三个脚本把方法变成可运行工具，输出同构结构化发现(findings schema)，作为 m14 模拟审稿的预审输入。整套贯穿强烈的诚实纪律：真实 HTTP 码不预填、端点不可达自动降级且标注、脚本只报命中不杜撰文献数据。

## 关键步骤
- 1. distill:先抓论文核心贡献,确认每段服务于哪个论点(结构/故事线层)
- 2. critique:审稿人五问逐项过每个论断,标出裸论断/最易被质疑处;跑 mechanical_check.py 定位 overclaim/ai_tone
- 3. polish:语言层四查(correctness/clarity/delivery/consistency)逐模块改;跑 polish.py 调 LanguageTool 做语法核对;每处按四栏输出(原句→问题诊断→修改后→为什么更好)
- 4. audit:合并两份 findings 按(line,col)复核一致性/术语/标点/缩写/引用,作为预投稿合规门槛
- 5. 贯穿:style_fingerprint.py 用作者过往文稿校准文风,避免改成统一'标准学术腔';交付前过 a08 自检,版本记入 db09

## 自带资产
- SKILL.md:主入口,定义两层四步方法论、审稿五问、语言四查、三个单句示范(soundness/clarity/novelty)、脚本说明与衔接图
- references/argument_review.md:深层论证审查规范——CEB三件套、四类高频失败修法表、Hedging校准阶梯、章节责任分工(Results不堆机制/Methods可复现/Discussion才hedging)、AI使用披露模板
- references.md:9个参考工具的真实核查笔记(LanguageTool/DeepL/Writefull/Paperpal/Grammarly等),含实测curl的真实端点参数与HTTP码、能力边界、已知坑
- references/findings_schema.md:两脚本输出的字段契约(_meta+findings),category取值表、severity人工分级表、与四步流水线对接说明、诚实性约束
- scripts/mechanical_check.py:纯stdlib离线脚本,扫overclaim/ai_tone/hedge_stacking/claim_strength/passive/punctuation六类,任何环境可跑
- scripts/polish.py:封装LanguageTool匿名云端点,自动分块+offset映射回原文绝对line/col,端点失败自动降级本地正则
- scripts/style_fingerprint.py:文风指纹提取与校准,从过往文稿量句长/被动比/第一人称/连接词偏好,标出待润色稿偏离最大的维度
- examples/full_pipeline_walkthrough.md:一段引言走完四步流水线的端到端before/after范例,含四栏逐条改

## 优点
- 深层优先的定位准确且少见——多数润色工具只做语法,这个技能把'裸论断/相关写成因果/主张强度不匹配证据'这些真正决定录用的问题落成可操作的CEB三件套和Hedging阶梯,直击审稿人痛点
- 诚实纪律贯穿到代码级:polish.py 的 _meta.http_codes 记录运行时真实HTTP码、端点失败标注 local-fallback 不伪造云端结果、references.md 对无法核实者明确标【未能核实】并带2026-06-06实测curl结果,可信度远高于一般技能
- 方法论有真实出处而非凭空编造:审稿五问对标Elsevier+NeurIPS、语言四查借Grammarly并按学术稿调权重、引言四段式与贡献三处一致引彭思达,references.md逐条给了链接与可复用方法
- 脚本有自检样例,python <script> 永远跑得通,且两脚本输出同构schema可直接合并;mechanical_check纯stdlib无依赖、polish有离线降级,在受限环境也能用
- style_fingerprint 的反同质化思路有亮点:针对'通用润色把所有人改成同一种学术腔'这一真实弊病,用统计指纹校准回作者声音,且明确'脚本不自动改写,改成什么样仍是作者判断',分寸把握好
- 三个单句示范+一个整段walkthrough覆盖soundness/clarity/novelty,四栏格式(原句→诊断→修改后→为什么更好)固定可复制,教学性强、可直接套用
- 衔接设计具体:findings作为m14预审输入并给出category→severity映射、引用问题转m10且citekey同源、文风存入a02跨项目复用,不是空泛的'与其他技能配合'

## 缺点 / 可被质疑处
- schema与代码已漂移:mechanical_check.py 第166行实际输出 claim_strength 类别,但 findings_schema.md §3 类别表只列了6类(overclaim/ai_tone/hedge_stacking/passive_overuse/passive_voice/punctuation)不含 claim_strength,§4 severity表和SKILL §66的m14映射也都没覆盖它——这个类别下游孤立,而SKILL恰恰强调'改字段名两处同步',自己先违反了
- 整个脚本工具链是英文中心的,但技能服务对象多为中文研究者:OVERCLAIM/AI_TONE/HEDGES/被动正则全是英文,style_fingerprint 的 words() 正则把连续中文当成一个超长'词',中文稿的句长/词频/被动指纹基本失效;中文润色无脚本支撑,与description承诺的'润色'范围不匹配
- 完全没有 LaTeX/.tex 处理:论文通常是.tex源码,直接拿mechanical_check扫会把\cite、\ref、宏命令、$...$数学环境当prose,数学里的标点/significant等会触发海量误报;SKILL大谈\cite citekey却没给脚本任何strip-latex能力,实际工程落地缺一环
- polish.py 的降级是'全或无'且无限流处理:任一chunk非200就break并丢弃已收集的全部LanguageTool findings、整篇退回本地正则;而免费端点限流是20请求/分钟+75KB/分钟,长论文多chunk极易在第二三块触发429,导致前面的真实结果全丢、无retry/backoff/sleep节流
- overclaim/语言检测无上下文豁免:'significant'在统计语境(statistically significant)是合法的,SKILL自己也写了'significantly(非统计语境)'要区分,但脚本是无条件黑名单匹配,必然误报;对直接引语、专有名词(如方法名含novel)、代码块也无白名单
- 句子切分过于naive:SENT_SPLIT用 (?<=[.!?])\s+,遇到 et al.、e.g.、Fig. 1、i.e. 会错误断句,直接污染 hedge_stacking、passive ratio、fingerprint 句长统计;check_hedge_stack 还用 text.find(sent) 定位,句子重复时会定位到错误offset
- polish本地fallback与mechanical_check有重复检测:两者都查double space和space-before-punctuation,fallback模式下合并findings会产生重复条目,schema的'按(line,col)合并'未提去重,且polish用 rule 键、mechanical用 category 键,合并展示需额外适配

## 可优化点（供后续逐技能优化）
- 补一个 strip_latex 预处理函数(去\command、$...$、注释、environments,保留纯prose并维护行号映射),让两脚本能直接吃.tex而不爆误报;这是当前最影响实际可用性的缺口
- 把 claim_strength 补进 findings_schema.md §3类别表和§4 severity表(建议归 major,与overclaim同档),并在SKILL §66的m14映射里加上对应Soundness意见,消除已存在的契约漂移
- polish.py 改为'每chunk独立保留'而非全或无:某chunk非200时只对该chunk降级本地规则、其余chunk保留LanguageTool结果;chunk间加sleep(基于75KB/20req限流计算间隔)、对429做指数退避重试,避免长论文结果全丢
- 给overclaim/claim_strength加上下文豁免:'significant'后跟'difference/level/p<'或前有'statistically'时跳过;支持一个项目级白名单(方法名、专有名词)避免把NovelNet这类命名当overclaim
- 升级句子切分:加缩写保护表(et al./e.g./i.e./Fig./Eq./vs./cf.)和小数点保护,或在有依赖环境优先用更稳的切分;hedge_stacking 改用迭代offset而非text.find,修掉重复句定位错误
- 为中文稿提供最小支撑:中文版overclaim/AI腔/夸大词表(显著/极大提升/前所未有/完美解决等)、用jieba或正则近似分词让fingerprint句长词频对中文有效,或在脚本里明确声明'仅英文'并在SKILL标注边界
- 在merge时做去重(同(line,col,category)只留一条,LanguageTool优先),并统一findings键名(rule/category合并为一个type字段+source区分),减少下游m14/审计的适配负担
- examples只有引言一段,可补Methods(可复现性改写)、Results(去机制解释)、Discussion(hedging校准)各一个walkthrough,覆盖章节责任分工那一节的全部场景

## 与其他 Light 技能/知识库的衔接
SKILL显式衔接:与 m07(paper-drafting)交替循环、重大重构与声明模板回 m07;改完跑 m14(review-rebuttal)模拟审稿验证,findings JSON 作为预审输入,category→severity 映射写进 m14;引用/缺引用问题转 m10(citation),正文\\cite占位用 authorYearWord 公式且与 m10 pin 的 .bib 键同源;术语对齐与版本记录用 db09(consistency,SKILL中a07/db09指代略有混用)；摘要/引言/结论按 db02 高水平套路重写；文风指纹可存入 a02(memory-pm)的用户写作偏好跨项目复用；交付前过 a08(self-review)自检闸门。整体处于 m07↔m08↔m10↔m14 的写作-润色-引用-审稿闭环中。注意:SKILL里同时出现 a07 和 db09 指代一致性/术语,编号体系存在小幅不统一,需与 light-consistency 实际编号核对。

---

## GitHub 同类前沿技能对标

Light 的 light-paper-polishing 在 GitHub 同类生态里处于一个少有人占的中间地带：它既不是纯语法/文风 linter（proselint、write-good、sciwrite），也不是端到端"自动审稿打分机"（SakanaAI/AI-Scientist、AgentReview、CycleResearcher/DeepReviewer）。它的差异化在于把"审稿人视角的深层论证诊断"和"逐句可执行润色"拼成 distill→critique→polish→audit 四步流水线，并落成同构 findings schema 喂给下游模拟审稿(m14)，形成可串联的科研流水线。绝大多数同类项目只覆盖其中一段：要么给一个整体 review 分数和大段意见但不落到逐句改写，要么做表层 lint 但没有 soundness/novelty 的深层维度。Light 真正稀缺的是"诚实纪律"工程化——真实 HTTP 码不预填、端点不可达自动降级标注、脚本只报命中不杜撰文献，这在追求"全自动生成 review"的热门项目里几乎是反向取舍。劣势同样明显：Light 是单作者中文技能包、零外部 star、方法论靠引述而非论文验证，而 sciwrite/AI-Scientist/proselint 有社区规模、论文背书或大规模实证数据支撑。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [labarba/sciwrite](https://github.com/labarba/sciwrite) | Claude/Codex Agent Skill，基于 Stanford Kristin Sainani《Writing in the Sciences》方法论做手稿写作审查，强调去名词化、削冗余、句子主语-动词靠近等可读性原则，附 SKILL.md。是与 light-paper-polishing 形态最接近的'写作审查 agent skill'。 | 693 | 2026-04-05 | 强：单一权威方法论(Sainani 课程)贯彻彻底、有社区认可、英文生态可见度高、定位极清晰。弱：只覆盖表层写作可读性，没有 soundness/novelty 的审稿五问深层维度，没有可跑检测脚本输出结构化 findings，不串联下游模拟审稿，方法单一不分两层四步。 |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Claude Code 的学术研究技能套件，覆盖 research→write→review→revise→finalize 全流程，是 GitHub 上最热的'科研全流程 agent skills'集合。与 Light 整包定位重叠，其 review/revise 环节直接对标 paper-polishing。 | 30710 | 2026-06-13 | 强：star 量级碾压、流程完整、英文社区活跃、更新频繁。弱：review/revise 偏通用化，缺 Light 的两层(表层/深层)切分与审稿五问打分维度，没有 LanguageTool 降级+本地 fallback 的诚实工程、没有 overclaim/AI 腔/claim_strength 机检脚本、不做个人文风指纹校准。 |
| [K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) | 通用型科学写作 agent，基于 Claude 做论文起草与改写，含写作与文献处理能力，主打'general purpose scientific writer'。 | 1936 | 2026-06-10 | 强：起草+写作一体、工程完成度高、更新活跃、面向通用场景。弱：偏'生成/写'而非'审稿人视角挑刺改'，没有逐句'问题→原因→修改方案→修改后'四栏诊断，没有可复现的离线检测脚本与结构化发现 schema，缺少 hedging 校准/裸论断标注这类深层论证工具。 |
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 全自动科研系统，内含 NeurIPS 式 LLM 自动审稿模块，对生成论文打 soundness/presentation/contribution 分并给 strengths/weaknesses/decision。是'审稿五问'思路的著名工程化实现。 | 13956 | 2025-12-19 | 强：审稿维度有 NeurIPS 指南背书、规模大名气高、自动出整体评分与决策。弱：产出的是'审稿意见+分数'而非'逐句润色改写文本'，不帮作者改稿；偏批量评测而非交互润色；没有表层语言四查与文风指纹；其自动评分的可信度本身受过学界质疑(arXiv 2502.14297)。 |
| [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | AI-Scientist 第二代，agentic tree search 驱动的 workshop 级自动科研，含改进的自动 review/反馈环节用于迭代论文质量。 | 6561 | 2025-12-19 | 强：迭代式 review-改进闭环、工程前沿、agentic 架构先进。弱：同 v1，目标是自动产研究而非给人改稿；review 服务于自我迭代不输出可读的逐句修改建议；无表层语言检测脚本、无诚实降级机制、无个人声音保持。 |
| [Ahren09/AgentReview](https://github.com/Ahren09/AgentReview) | EMNLP 2024 Oral 官方实现，用多 LLM agent(reviewer/AC/author)模拟学术同行评审全过程，研究评审动态与偏差。 | 118 | 2026-05-10 | 强：多角色对抗式评审有论文背书、模拟真实评审社会过程、研究性强。弱：是评审过程的'仿真/研究'而非给作者的润色工具，不产出修改后文本；与 Light 的 critique 步类似但没有 polish/audit 与可跑表层脚本;偏学术实验代码而非可直接用的稿件改进流水线。 |
| [Weixin-Liang/LLM-scientific-feedback](https://github.com/Weixin-Liang/LLM-scientific-feedback) | Stanford 大规模实证研究，用 GPT-4 对论文给结构化反馈并与人类 review 对比，附可跑的论文反馈生成流程。 | 533 | 2024-01-11 | 强：有大规模实证数据支撑'LLM 反馈有效性'、方法可信、Stanford 出品。弱：产出整体性反馈意见而非逐句润色；已近两年未更新；无表层语言四查、无 overclaim/文风脚本、不串联流水线;反馈粒度粗于 Light 的四栏修改。 |
| [zhu-minjun/Researcher](https://github.com/zhu-minjun/Researcher) | CycleResearcher/DeepReviewer 项目仓库，训练专用 LLM 做'人类式深度思考'的批判性论文评审与自动研究-评审循环(DeepReview-13K 数据集)。 | 393 | 2026-03-05 | 强：专训模型+13K 评审数据集、深度思考链式评审、有 ACL 论文背书。弱：重在产出高质量 review 文本与训练资源，不做作者侧逐句改写与语言层润色;无离线降级脚本、无文风指纹;落地为模型/数据而非即用 agent skill。 |
| [amperser/proselint](https://github.com/amperser/proselint) | 成熟的英文散文 linter，按一组可解释规则(冗词、套话、夸张、误用)给出命中位置与建议，纯本地可跑、可集成编辑器。 | 4539 | 2026-06-07 | 强：规则库成熟、纯离线稳定、生态集成广、社区规模大,与 Light 的 mechanical_check.py 同类且更完备。弱：只做通用表层文风,无学术 soundness/novelty 深层维度、不懂审稿五问、不输出修改后整句方案、不保持作者声音、不接论文场景的引用/claim 校准。 |
| [ChicagoHAI/OpenAIReview](https://github.com/ChicagoHAI/OpenAIReview) | 用 AI 评审论文草稿以帮助改进的工具，面向作者侧的 draft 反馈，定位'AI reviewing paper drafts for improvement'。 | 148 | 2026-06-06 | 强：明确面向作者改稿、目标与 Light 的 critique 一致、近期活跃。弱：偏整体 review 反馈,缺 Light 的两层四步结构与逐句四栏改写;无表层语言检测脚本与结构化 findings schema;无诚实降级/文风指纹这类工程细节。 |

### Light 该技能可借鉴的点
- 把 sciwrite 那种'单一权威方法论彻底贯彻'的做法借过来：当前 Light 引述了 Elsevier/NeurIPS/Grammarly/彭思达多源，可考虑给每条规则标注更明确的出处锚点，提升可信度与可教学性。
- 借鉴 proselint 的规则库工程化：把 mechanical_check.py 的黑名单/规则做成可配置、可解释、带规则 ID 的规则集(类似 proselint 的 checks 注册表)，便于扩展、关闭单条规则和编辑器集成。
- 学习 Weixin-Liang/LLM-scientific-feedback 与 zhu-minjun/Researcher 的实证/数据支撑思路：给'审稿五问能否预测拒稿'之类核心假设找一点公开数据或案例验证，弱化纯方法论引述。
- 参考 AI-Scientist 的 NeurIPS 式结构化评分维度，把 critique 步的输出再结构化为可量化分档(soundness/novelty/clarity/repro/related-work 各自打分),增强与 m14 findings schema 的对接刚性。
- 借 AgentReview 的多角色对抗思路，在 critique 步可选启用'多审稿人视角'(严格派/领域派/方法派)交叉挑刺,覆盖单一视角易漏的质疑点。
- 面向英文社区可见度:沿用 sciwrite/academic-research-skills 的 SKILL.md + 英文 README 暴露方式做一份对外版本,Light 目前为中文私包,零 star 不利于被同行发现与复用。
- 参考 OpenAIReview / claude-scientific-writer 的'作者侧 draft 反馈即跑'体验,把四步流水线包成更傻瓜的一键入口(给定 paper.txt 直接产出四栏报告+findings JSON),降低使用门槛。
