# light-idea-generation — 深度分析与同类对标

> 源：[`skills/light-idea-generation/SKILL.md`](../../../skills/light-idea-generation/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：科研 idea 生成器：把"方向/数据/文献"按两级抽象收敛成可被 m04 逐字段复核的分层 idea 候选卡,核心卖点是"核心撞车一票否决"防自以为新。

## 核心运行逻辑
技能本质是一套"发散—收敛—新颖性核验—强制送审"的纯流程编排,自身不带可执行代码,检索能力全部委托给 m01(light-literature-search)的已验证脚本以避免手拼 API 和引用幻觉。设计主线借鉴 AI-Researcher 两级输入抽象(已有 idea 走细化 / 只有方向走文献+数据反推),用 idea_card 立项卡把模糊想法收敛成字段与 m04 rubric 八维度严格对齐的单元,实现"自报不被采信、下游逐项独立复查"的契约式交接。最硬的一环是带血泪教训(Dal Pozzolo 2015 撞车案例)的"核心撞车四问",要求以对抗心态专门去找最像的那一篇,并把检索留痕写进卡里供 m04 重查。references.md 把 14 个外部工具/论文(ResearchAgent、AI Scientist v1/v2、MAGenIdeas、若干 Claude 科研技能)的真实端点、参数、评审维度与已知坑逐条记录,作为方法出处的真相源。

## 关键步骤
- 1. 前置门槛:确认 m01 文献 gap 清楚 + m02 数据足够,否则回退不做空想
- 2. 判定输入级别:Level1(已有 idea→细化/差异化/可行性) 或 Level2(只有方向/数据→从文献+数据反推,每候选填立项卡)
- 3. 发散:从 7 个角度(gap/迁移/数据/重定义/组合/理论/效率)独立生成,不够时补 6 个结构化激发技法 + 实体共现跨域重组
- 4. 收敛:db03 方法成熟度过滤→两两PK/瑞士轮排序→影响×工作量二维漏斗选 Top-N
- 5. 新颖性核验:调 m01 的 search_normalize.py + snowball.py 检索对标工作,SPECTER2 余弦防伪多样性
- 6. 核心撞车检查(最高优先级一票否决):回答四问并写检索留痕到立项卡
- 7. 逐 idea 填齐必说清字段(一句话/动机/创新点/机理假设+竞争性解释/可证伪目标/数据可行性/成果形态/投稿层次/精确IF风险)
- 8. 提交前自检:ResearchAgent 五维 + AI Scientist 三维 + 7 失败模式反向自检
- 9. 产出 3–6 个分层 idea 汇成 idea_candidates.md,强制送 m04 严审,通过写入 db09 decision_log 并进 m05

## 自带资产
- SKILL.md:主流程文档,定义前置条件/两级输入/发散收敛策略/撞车四问/必说清字段/自检/强制衔接
- references.md:14 条外部工具笔记(ResearchAgent、AI Scientist v1/v2、AI-Researcher、MAGenIdeas、Scientific Brainstorming、Hypothesis Generation、diverge-converge、ARS 7失败模式、What-If Oracle、Consciousness Council、Critical Thinking、ScholarEval、OpenAlex API),每条带真实端点/参数/评审维度/已知坑
- templates/idea_card.md:单条 idea 立项卡,字段与 m04 rubric 八维度对齐,标注 (m04复核) 一票否决/封顶锚点,内含最近邻≥3篇检索留痕表与填写自检

## 优点
- 核心撞车四问是真正的差异化亮点:以真实血泪案例(做完整套实验才发现 Dal Pozzolo 2015 撞车)立规,要求带'假设已有人做过去揪出来'的对抗心态、至少 2 库交叉、找最像的那篇逐句比对,直击 LLM 提 idea 最致命的'自以为新'
- 检索零自研、统一委托 m01 已验证脚本并显式禁止手拼 API URL,既避免限流/分页/编码坑,又与文献真相源保持单一口径,从机制上压制引用幻觉
- idea_card 字段与下游 m04 rubric 八维度逐项对齐、标注复核锚点,形成'自报不被采信'的契约式交接,而非松散的自然语言传递
- references.md 信息密度高且诚实:每个外部方法都给真实端点/参数(如 perform_ideation_temp_free.py 的 --max-num-generations、OpenAlex group_by 趋势分析)并附'已知坑/局限',方法可追溯到出处而非空谈
- 发散有方法论支撑(7角度+6技法+实体共现重组)、收敛有量化手段(瑞士轮/两两PK + 影响×工作量漏斗),并用 SPECTER2 余弦相对差防'换皮凑数'的伪多样性,系统性地对抗单一思路死磕
- 强制循环闭环设计:必送 m04、被毙带方向回炉再生成、通过写 db09 decision_log,把 idea 生成嵌入可追溯的项目主线而非一次性产出

## 缺点 / 可被质疑处
- 自身零可执行脚本:SPECTER2 余弦防伪多样性、瑞士轮排序、影响×工作量打分、立项卡空字段门禁全是文字描述,靠模型每次手工执行→结果不可复现、难一致,与隔壁强调'调已验证脚本'的原则自相矛盾
- 三套评分体系并存且无统一聚合规则:五维(1–5)、三维(1–10)、影响×工作量二维快评同时存在,但没说清谁决定最终 Top-N 排序、如何加权融合,操作者会困惑该信哪个分
- SPECTER2 阈值指引含糊到无法落地:只给'实测 0.85~0.93'和'显著高于其余对的视为变体',既无具体 cutoff 也无算法(如 mean+1σ),用户无法把'显著高于'变成可执行判定
- 完全没有 examples/:一个教 idea 生成的技能却没有任何填好的 idea_card 或 idea_candidates.md 样例,新用户不知道合格输出长什么样、撞车检索留痕该写到多细,降低了可复制性
- references.md 自身踩了它警告的引用幻觉坑:引用了未来日期/未核实文献(Nature 2026 651:914-919、arXiv 2604.20548、Scientometrics 2026)却当既成事实陈述,未标注'预印本/未核实',违背技能自己倡导的诚实归档
- 重度跨技能/库耦合且无降级路径:大量硬引用 db03/db04/db08/db09、m01/m02/m04/m05/m13、CONVENTIONS §6.1,一旦命名漂移就静默失效;且若 m01 脚本或 OpenAlex key 不可用,没有任何 fallback 检索方案
- 发散数量与收敛漏斗脱节:借来的 diverge-converge 示例说生成~30 个,主流程却只说产出 3–6 个,中间'先发散到多少个再过滤'没有明确数量指引,漏斗入口悬空

## 可优化点（供后续逐技能优化）
- 新增 scripts/:(1) 候选去重脚本——调 S2 specter_v2 embedding 输出两两余弦矩阵并按 mean+1σ 自动标出疑似变体对;(2) 瑞士轮/两两PK 排序脚本——吃 idea_candidates.md 输出排名;(3) 立项卡门禁脚本——校验所有 (m04复核) 字段非空、最近邻≥3 且带留痕,否则拒绝交接
- 新增 examples/:至少 1 张填满的 idea_card.md + 1 份含 3–6 个分层 idea 的 idea_candidates.md,完整展示撞车四问的阴性证据/最像3篇/量化 delta 写法,作为输出黄金样例
- 统一三套评分:明确各自分工与决策规则(如三维做快速 triage 入场、影响×工作量做漏斗收敛、五维做交 m04 前终检),并写出 Top-N 的唯一裁定依据,消除评分系统冗余
- 把模糊阈值算法化:给 SPECTER2 一个具体判定流程(批内 mean+1σ 标记 / 或绝对 cutoff),并写明 embedding 缺失时降级到标题摘要文本相似度的具体做法
- 对 references.md 中未来日期文献明确加'未核实/预印本'标注,身体力行技能自己的诚实归档原则,避免被 m04 或审稿人反将一军
- 补 m01 不可用时的降级检索路径(如直连 OpenAlex/S2 的最小只读查询),保证撞车检查在依赖缺失时仍能跑、不致整条流程卡死
- 明确发散→收敛的数量漏斗(如原始生成≥15 条→聚类去重→收敛到 3–6 条),把漏斗入口数量补上,让'先发散后收敛'可操作

## 与其他 Light 技能/知识库的衔接
上游强依赖 m01(light-literature-search):检索脚本 search_normalize.py/snowball.py、OpenAlex 接入真相源、SPECTER2 语义嵌入节全部复用其口径;m02(light-data-engineering):数据充分性前置门槛与自建标注回退。下游强制衔接 m04(light-idea-critique):立项卡字段与其 rubric 八维度逐项对齐、必送严审、被毙回炉形成循环;通过后进 m05(light-research-plan)细化算力预算、m13(light-venue-matching)定投稿层次。项目库:db03(方法成熟度过滤)、db04(数据集卡对齐数据可行性)、db08(成本粗算)、db09(decision_log 落档);交接工件命名遵循 CONVENTIONS §6.1。绘图侧可接 m07/m08(竞争解释/机制通路/实验设计图)。常驻技能 light-consistency/light-research-ethics/light-self-review 在其产出上后台生效。

---

## GitHub 同类前沿技能对标

Light 的 light-idea-generation 在定位上属于"纯流程编排型 agent skill":自身不带可执行代码,把检索委托给已验证的 m01 脚本,把评审契约式交给 m04,核心资产是"两级抽象收敛 + idea_card 字段对齐 + 核心撞车一票否决 + 强制送审"这套工程纪律。GitHub 上的同类项目分两大阵营,定位都和它有明显错位。第一类是重量级可执行研究框架(AI-Scientist v1/v2、HKUDS/AI-Researcher、AgentLaboratory、deep-research),它们把 ideation 当作端到端自动发现流水线的一个内部环节,代码量大、能真跑实验出论文,但 idea 阶段往往是黑盒,没有 Light 那种"字段级可复核 + 撞车留痕"的交接契约,novelty 检查多为打分而非一票否决。第二类是学术原型与方法实现(NoviScl/AI-Researcher、ResearchAgent、SciMuse、hypothesis-generation、Nova),它们在"新颖性/有趣度量化、知识图谱反推、迭代规划"等单点上比 Light 更有理论深度和实证评估,但都是研究代码、不是可复用的 agent skill,缺工程编排和防幻觉留痕。真正与 Light 形态最接近的是 markdown-only 技能仓(ARIS / wanshuiyin、lingzhi227/agent-research-skills):同样无框架、靠 Claude Code 跑、含 idea-discovery/novelty-check 流程,但它们偏"睡眠中自动刷 idea"的吞吐导向,缺 Light 强调的"自报不被采信、下游逐项独立复查 + 八维 rubric 对齐"的严谨契约。整体看,Light 的差异化护城河是"防自以为新的对抗式撞车四问 + 契约式交接",这是上述项目普遍弱化的一环;而 Light 的短板是没有量化新颖性指标、没有真跑实验闭环、没有规模化吞吐机制。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 端到端全自动科研框架,从 idea 生成、实验、写论文到自动评审全流程;ideation 阶段含基于已有 idea 库去重的新颖性检查(用 Semantic Scholar 查相似工作)。 | 13956 | 2025-12-19 (pushed) | 强:能真跑实验闭环出完整论文,工程成熟度和影响力远超 Light;ideation 自带 Semantic Scholar 新颖性查重。弱:idea 环节是大流水线里的子步骤,无 Light 那种字段级可复核卡片与契约式送审,新颖性是打分制而非'核心撞车一票否决'。 |
| [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | AI Scientist 第二代,用 agentic tree search 做 workshop 级自动科研,去掉对人写模板的依赖,迭代探索假设空间。 | 6561 | 2025-12-19 (pushed) | 强:树搜索式假设探索比 Light 的两级抽象收敛更自动、更能跑出可投稿成果。弱:同样是重代码框架,ideation 黑盒化,无可被逐字段复核的立项卡,也无 Light 的撞车留痕供下游重查。 |
| [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher) | NeurIPS2025 论文配套,LLM 驱动的全自主科学创新 agent,支持从想法到实现的自动化,有生产版 novix.science。 | 5453 | 2025-10-16 (pushed) | 强:覆盖从 idea 到代码实现的完整自主流程,有产品化落地与论文背书。弱:面向自动产出而非人机契约交接,无 Light 的 idea_card 八维 rubric 对齐与对抗式撞车四问这类防自欺机制。 |
| [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | 端到端自主研究工作流,把人给的研究 idea 落地为文献综述、实验、报告;强调辅助人类研究者实现想法。 | 5681 | 2025-08-20 (pushed) | 强:实现阶段(跑实验、写报告)是 Light 完全不碰的部分,补全了下游闭环。弱:它假定 idea 已给定,ideation/新颖性把关薄弱,正是 Light 主攻且更严谨的环节。 |
| [dzhng/deep-research](https://github.com/dzhng/deep-research) | 极简实现的深度研究 agent:结合搜索引擎+网页抓取+LLM 做迭代式深挖,自动细化研究方向并递归深入。 | 19108 | 2026-04-11 (pushed) | 强:star 最高、TypeScript 实现可直接部署,迭代深挖与方向细化机制成熟。弱:产物是研究报告而非可立项的科研 idea,无新颖性撞车把关,无字段化送审,定位偏'调研'而非'选题'。 |
| [wanshuiyin/Auto-claude-code-research-in-sleep (ARIS)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 纯 Markdown、无框架的自主 ML 研究技能集,含 idea-discovery / idea-creator / novelty-check / research-pipeline 等技能,跨 Claude Code/Codex 等任意 LLM agent 运行,主打'睡眠中自动做研究'。 | 11992 | 2026-06-11 (pushed) | 强:与 Light 形态最像(markdown-only、无锁定、含独立 novelty-check 技能),且有吞吐自动化与跨模型 review 循环,人气极高。弱:偏自动刷量,缺 Light 的契约式逐字段复核与'对抗式找最像那一篇'的撞车纪律,新颖性检查较轻。 |
| [lingzhi227/agent-research-skills](https://github.com/lingzhi227/agent-research-skills) | 面向 Claude Code 的研究类技能集,含 deep-research 技能做系统化学术文献综述。 | 126 | 2026-02-27 (pushed) | 强:同为 Claude Code 技能形态,文献综述编排清晰,体量轻。弱:聚焦综述而非 idea 收敛与立项,无 idea_card、无新颖性一票否决,也无与下游评审技能的字段对齐契约。 |
| [NoviScl/AI-Researcher](https://github.com/NoviScl/AI-Researcher) | 斯坦福'LLM 能否产出比人更新颖的研究 idea'大规模实验配套代码,含 idea 生成与新颖性/可行性人评流程。 | 390 | 2025-08-07 (pushed) | 强:对'新颖性'有严谨的大规模人类评估与统计方法论,是 Light 撞车理念的学术源头之一。弱:是研究实验代码而非可复用技能,无工程化编排、无卡片契约,不能即插即用。 |
| [JinheonBaek/ResearchAgent](https://github.com/JinheonBaek/ResearchAgent) | NAACL2025 论文官方代码:基于科学文献的迭代式研究 idea 生成,用实体知识图谱与多评审 agent 迭代打磨 idea。 | 41 | 2025-08-24 (pushed) | 强:迭代 idea+多评审 agent 反馈循环有方法论深度,是 Light references 里列的真实出处。弱:研究原型、依赖特定数据与图谱,无 Light 的契约式送审与撞车留痕,落地复用门槛高。 |
| [ChicagoHAI/hypothesis-generation](https://github.com/ChicagoHAI/hypothesis-generation) | HypoGeniC / HypoRefine 官方库:数据驱动地用 LLM 为开放域研究生成并迭代精炼假设。 | 118 | 2025-11-12 (pushed) | 强:从数据反推假设的算法化机制成熟,有可复现的精炼迭代与基准。弱:聚焦'数据→假设'单点,无文献撞车把关、无立项卡与送审契约,定位是方法库非选题编排。 |
| [artificial-scientist-lab/SciMuse](https://github.com/artificial-scientist-lab/SciMuse) | 用知识图谱+LLM 生成'有趣'的科研 idea,并用 100 位课题组长的真实评分做有趣度评估。 | 37 | 2025-02-03 (pushed) | 强:把'有趣/有价值'做成可量化、有专家实证的指标,这是 Light 缺的维度。弱:研究代码、依赖大规模知识图谱,无新颖性撞车一票否决,也非可复用 agent skill。 |
| [hflyzju/Nova](https://github.com/hflyzju/Nova) | Nova 论文(迭代规划与搜索提升 LLM 生成 idea 的新颖性与多样性)的非官方实现。 | 7 | 2025-09-23 (pushed) | 强:专门针对'新颖性与多样性'做迭代规划检索,理念与 Light 防撞车高度同源。弱:star 极低、为个人复现代码,无工程编排、无卡片契约与下游评审对接,成熟度低。 |

### Light 该技能可借鉴的点
- 引入可量化的新颖性/有趣度指标:借鉴 SciMuse(100 位课题组长评分)与 NoviScl/AI-Researcher 的统计化人评,把'核心撞车四问'的二元一票否决补上一个连续打分维度,降低边界 case 误杀。
- 借鉴 ResearchAgent 的'实体/知识图谱 + 多评审 agent 迭代'机制,让 idea_card 在送 m04 前先经一轮内部多角色对抗精炼,而不仅靠单次两级抽象收敛。
- 参考 AI-Scientist 的 Semantic Scholar 自动查重做法,把 m01 的撞车检索从'人工对抗式找最像一篇'升级为可脚本化的相似论文召回+留痕,提升撞车四问的召回率。
- 学习 HypoGeniC/HypoRefine 的'数据驱动假设精炼'循环,为 Light'只有数据/方向'的反推路径补一套显式的假设迭代精炼子流程。
- 借鉴 ARIS 的跨模型 review 循环与'睡眠中批量产出'机制,在保持契约严谨的前提下增加一个可选的批量候选生成模式,提升吞吐。
- 参考 Nova 的迭代规划-搜索框架,显式优化候选 idea 之间的'多样性',避免收敛阶段产出高度同质的候选卡。
- 学习 AI-Scientist-v2 的 agentic tree search,把两级抽象收敛升级为可回溯的搜索树,让被撞车否决的分支能自动回退到上一抽象层重新发散,而非整条作废。
