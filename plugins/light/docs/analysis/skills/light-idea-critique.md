# light-idea-critique — 深度分析与同类对标

> 源：[`skills/light-idea-critique/SKILL.md`](../../../skills/light-idea-critique/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：以顶会审稿人标准对 m03 产出的科研 idea 做"先盲后明 + 八维加权 + 五视角对抗 + 反谄媚 + 检索证否"的硬闸门式严审,只评不改,带 Roadmap 回 m03 循环,过线才放行 m05。

## 核心运行逻辑
核心是"gate before score"(否决项优先于加权分):先用 BLIND 物理隔离阶段在没看正文前钉死验收标准与 block/warn 条件(输出 [CONTRACT-ACKNOWLEDGED]),再开正文按八维 behavioral anchor 打 0–100、加权求 Weighted(0–100)并映射 NeurIPS 式 Overall(1–10);创新性<45 或核心四维两项<45 或存在未化解 CRITICAL 时,无论加权多高都被压顶到不通过/有条件通过。把"证据先于结论"落地为强制检索(OpenAlex/S2/arXiv 至少两库交叉、记 HTTP 码+最像3篇+量化 delta),无检索则创新性维度封顶并标 evidence-missing。对抗性靠五视角(方法/实验/理论/应用四打分视角 + 只挑刺的 Devil's Advocate)+ 单变量精确 IF 归因证否 + 反谄媚 1–5 评分制(让步必挂证据、禁连续让步、concession-rate>50% 报警)。待审 idea 被当作 data 而非指令(IRON RULE),技能对 idea READ-ONLY,改进只写进 Roadmap 交还 m03,形成"评审→再 ideation"闭环。

## 关键步骤
- 1. Step 0 路由 + IRON RULE 注入扫描(命中记 INJECTION-ATTEMPT-DETECTED 并照常严审)
- 2. Step 1 Phase 1 BLIND:仅给标题/领域/关键词,写八维验收标准+block+warn,输出 [CONTRACT-ACKNOWLEDGED] 才能进 Phase 2
- 3. Step 2 检索取证:至少两库交叉验证;必做核心撞车复核(对抗心态独立复查 m03 自报,判定撞车等级,自报不符记 NOVELTY-OVERCLAIM,强制拒稿理由预演)
- 4. Step 3 Phase 2 OPEN:拿全文按 rubric 逐维 0–100,偏离 Phase 1 标准须先出 Scoring Plan Dissent
- 5. Step 4 五视角对抗:四视角锚不同维度独立挑刺 + Devil's Advocate 找四类 CRITICAL + 单变量精确 IF 归因证否
- 6. Step 5 反谄媚反驳:每条反驳 1–5 评分,首句直给三个最致命弱点(grill),sycophancy_guard.py 算 concession-rate
- 7. Step 6 聚合判决:score_aggregate.py 算 Weighted/Overall,否决项与 decision mapping 取更严者,落盘 critique_verdict.md
- 8. Step 7 强制衔接:不通过/有条件通过带 Roadmap 回 m03 循环,无 block 且 Weighted≥80 才放行 m05,写入 db09 decision_log
- 9. 可选 calibration mode:喂已知结局 idea 跑 calibration.py 算 FNR/FPR 调严格度

## 自带资产
- SKILL.md — 立场/消费声明/IRON RULE/资产地图/Step 0–7 + calibration 主流程
- references/rubric.md — 八维 5 分段 behavioral anchor + 权重表(合计1.00) + 加权公式 + Weighted→Overall 映射 + decision mapping 表(打分必读)
- references/contract.md — A 先盲后明物理隔离协议 + B 反谄媚 1–5 评分制/禁连续让步/concession-rate 报警(执行序必读)
- references/protocol.md — IRON RULE + 五视角对抗格式 + 单变量精确 IF 四步纪律 + 7 条 anti-patterns 表
- references.md — 13 条工具/API 真实研究笔记(NeurIPS 表、OpenReview/S2/OpenAlex 端点与坑、可借鉴的 12 个 skill,标注未能核实项)
- templates/verdict_template.md — 判决填写模板(含检索表/八维表/五视角/单变量IF表/否决项 checklist)
- templates/Revision_Roadmap.md — 必做项/选做项/未化解CRITICAL/回m03指令 的可验收修订表
- examples/worked_example_dermoscopy.md — 皮肤镜 idea 走完整流程范例(明确标注哪些数字是实测、哪些是示意)
- scripts/score_aggregate.py — 八维加权+否决项 gate+判决映射,纯标准库+自测
- scripts/sycophancy_guard.py — 反驳 1–5 归一化(无证据让步强制降3)+concession-rate+连续让步检查,纯标准库+自测
- scripts/calibration.py — 喂已知结局算混淆矩阵/FNR/FPR/precision,有条件通过保守计为不通过,纯标准库+自测

## 优点
- gate-before-score 设计真正可靠:用否决项压顶加权均值,防止'创新性致命但其余维度凑高分'的 idea 被平均分洗白——这是顶会审稿真实逻辑(一个 fatal flaw 即拒),score_aggregate.py 里用 rank 字典取更严者落地得很干净
- 先盲后明做成物理信息隔离 + [CONTRACT-ACKNOWLEDGED] 闸门 + Scoring Plan Dissent 强制说明偏离,是有牙齿的反锚定机制,不是口头承诺;直击'被作者精彩叙事带跑改写验收线'这一真实失效
- 八维 anchor 写的是'打到这档要看到什么证据形态'(可命名机理级差异/干净对照+消融/数据集名+规模+标注)而非空泛形容词,可直接据此打分和反查,远胜常见的'创新性:1-5分'式空表
- Step 2 核心撞车复核是有动机的硬闸门:用真实事故(Dal Pozzolo 2015 已发表导致秒拒)论证为何必须带'假设已有人做过去揪出来'的对抗心态独立复查,而非采信 m03 自报,并强制拒稿理由预演
- references.md 的认识论诚实度罕见:给真实端点/参数/限流坑,明确标注'未能核实'项,并主动承认单模型模拟多视角=伪多样性(#13)、LLM 评审有回归到平均人评的倾向(#4)——不掩盖自身根本局限
- 三个脚本都纯标准库、带 __main__ 自测、把加权/concession 等易算错的算术外置,降低模型手算出错;READ-ONLY + 把 idea 正文与检索返回都当 data 的 IRON RULE 安全姿态正确且优先级最高

## 缺点 / 可被质疑处
- 单模型扮演五视角的伪多样性是根本软肋,且只靠 prompt 自律缓解:protocol 让'≥3 视角指向同一关切就重抽',但'重抽'由同一模型自判,无任何可机检的张力判据;references.md #13 已自认'多样性弱于真·多模型',技能却未提供结构化约束(如强制各视角引不同 rubric 维度+不同前作)来真正逼出冲突
- 整套 gate 重度依赖检索能力,但运行环境未必有网络:worked example 自承只有 HTTP 码与 meta.count 是实测,'最像3篇'全是示意;一旦离线,创新性被封顶到 evidence-missing,而 SKILL 没有离线降级工作流(只说封顶,没说封顶后还能不能'通过'、要不要二次人工检索),核心闸门可能架空
- 通过线 Weighted≥80(≈Overall 8 strong accept)与技能自引证据自相矛盾:references.md #6 明示真实被接收论文 CycleReviewer 仅评 5.69/10、生成论文 5.36,要求每个 idea 达 strong-accept 级才放行 m05 大概率过严、FNR 高;阈值是硬编码而非由 calibration.py 在标注集上反推,缺乏依据
- 八维权重(0.20/0.18/0.14...)被包装成'锚定 NeurIPS'但 NeurIPS 评审表并不给数值权重,这些权重实为自创且无敏感性分析支撑;审稿人会直接质疑'为何 soundness 0.18 而非 0.20',权重微扰下判决稳健性未验证
- rubric 的数据/实验 anchor 明显 ML 口味(backbone/对照/消融/baseline 超参对齐),对纯理论、数学、systems、HCI、定性研究类 idea 不适配;references.md #8 自己指出 CONSORT/GRADE 偏生医,但 rubric 并未提供领域 profile 切换,'通用严审'的宣称与单一锚定冲突
- calibration.py 把'有条件通过'保守计为负例(未放行),但真实闭环里有条件通过是回 m03 迭代而非拒稿——这把'需修订'与'被拒'混为一谈,会高估 FNR 并误导严格度调参;concession-rate>50% 阈值在小 N 下脆弱(worked example 恰好 1/2=50% 不报警),连续让步 flag 在自主 agent 里只标'需人工复核'形同虚设;消费 idea_candidates.md(多卡)却全程只评单卡,缺批量比较/排序工作流

## 可优化点（供后续逐技能优化）
- 把通过线从硬编码 80 改为由 calibration.py 在一批标注 idea(真实接收/被拒)上反推的经验阈值,或下调到与所引 weak-accept 现实(~65–70/Overall 6)对齐并写明依据,消除与 references.md #6 的内部矛盾
- 新增结构化多样性强制:要求四视角各声明'主锚维度互不相同 + 各引一篇不同前作 + 各给一个别视角会漏的风险',提供可机检的去重/张力检查清单,把伪多样性从'自律'升级为'可验证',弥补单模型软肋
- 补离线/降级检索协议:明确列出哪些库不可达、强制标注检索覆盖度,并规定 evidence-missing 状态下最高只能'有条件通过'+要求二次检索后才可改判'通过',让核心闸门在无网时不被架空
- 给 rubric 加领域 profile(ML / 理论 / systems / 生医 / HCI-定性),按领域替换数据/实验维度的 anchor 与证据形态(理论 idea 用可证伪假设+证明草图替代消融/对照),并据领域微调权重
- calibration.py 改三分类(通过/需修订/拒)分别统计,使 FNR/FPR 反映真实回 m03 循环而非把修订当拒稿;修小 N 脆弱性:N<4 时用绝对让步计数门限,连续让步在自主模式下改为自动降级到≤3 而非'需人工复核'
- 增加批量比较/排序模式:摄入 idea_candidates.md 全部立项卡统一打分并排序,输出 top-k 放行而非逐卡孤立判决,匹配 m03 多卡产出的真实形态
- 给权重做敏感性分析并写进 rubric(±0.02 微扰下判决档位是否翻转),要么给权重一个可引用出处,要么显式声明为可调超参并说明默认值理由
- 加输出长度/压缩纪律:五视角+DA+单变量IF+反驳栈叠加易产出冗长重复(references.md #7 已警告 5 persona 冗长),要求汇总阶段对共识关切去重、每视角限字数
- 对齐文档小瑕疵:score_aggregate.py 自测 assert 用 51.2 而实算/worked example 为 51.0,统一为 51.0 避免给后续维护者造成'脚本算错'的误判

## 与其他 Light 技能/知识库的衔接
上游强耦合 m03(light-idea-generation):消费其 idea_card.md / 多卡汇成的 idea_candidates.md,按卡字段(新颖性档位、最近邻≥3篇、数据可行性、算力成本)逐项独立复核而非采信,核心撞车四问做对抗式复查。下游 gatekeeping m05(research-plan):仅'通过'的 idea 放行,判决落盘为 critique_verdict.md 作为交接工件(命名见 CONVENTIONS §6.1)。横向:数据偏倚/许可联动 m02 与 db04;判决与理由写入 db09 的 decision_log。闭环:不通过/有条件通过带 Revision_Roadmap.md 回 m03 重新生成,循环到无 block、无未化解 CRITICAL、Weighted≥80。方法论上整体仿 ResearchAgent/AI Scientist 的'评审反馈→再 ideation',视角/契约/盘问分别借鉴 Consciousness Council、academic-paper-reviewer、grill-me、what-if-oracle、verification-before-completion 等(references.md 第7/9/10/11/12 条)。

---

## GitHub 同类前沿技能对标

GitHub 上同类工作主要分两脉:一是重型"全自动科研"框架(SakanaAI/AI-Scientist v1/v2、HKUDS/AI-Researcher、AgentLaboratory、CycleResearcher),它们都内置 automated reviewer,但 reviewer 是给"已产出论文"做 NeurIPS 式评分或当训练奖励信号,目的是推进生成、而非作为拦在 idea 阶段的硬闸门。二是轻量 Claude Code agent skill(HKUSTDial/Supervisor-Skills 的 idea-evaluator、ngtiendong/Academic-Research-Agent-Skill)以及专做新颖性核验的 OpenNovelty,它们最接近 Light 的"评 idea + novelty gate + 证据接地"定位。但几乎没有任何一个同时具备 Light 的四件套:BLIND 先盲后明物理隔离 + contract-acknowledged 锁验收、八维 behavioral-anchor 加权并映射 NeurIPS Overall 的否决项优先(gate before score)、强制多库交叉检索证否(HTTP 码+最像3篇+量化 delta)、以及反谄媚 1-5 让步配额与 concession-rate 报警。Light 的差异化在于"防自欺/防谄媚的审稿纪律"和"只评不改、回 m03 的闭环 Roadmap",而非生成能力或模型规模——它是协议化的严审闸门,不是科研生成引擎。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [HKUSTDial/Supervisor-Skills (idea-evaluator skill)](https://github.com/HKUSTDial/Supervisor-Skills/blob/main/plugins/phd-research/skills/idea-evaluator/SKILL.md) | 博导经验炼成的 Claude Code 科研技能包,其中 idea-evaluator 子技能以顶会审稿人/导师标准评 idea,出 Strong Accept / Accept with Revisions / Reject and Pivot 三档判决,5 轴(Higher/Faster/Stronger/Cheaper/Broader)1-10 打分 + fatal-flaws 审计 + 范式跃迁探测 + 可行性检查 + integrity gate(每个分必须引证据,禁 gut feeling)。 | 2458 | 2026-04-29 | 最接近的同类。强:同为 Markdown agent skill、判决三档、整合在覆盖 idea→投稿全流程的高 star 技能包里、社区可见度高。弱:无 BLIND 先盲后明物理隔离、无 contract-acknowledged 锁验收、无八维加权→Overall(1-10) 映射、无强制 OpenAlex/S2/arXiv 两库交叉检索证否、无反谄媚 1-5 让步配额与 concession-rate 报警、无 Devil's Advocate 独立视角、无 read-only data 隔离与回 m03 Roadmap 闭环。Light 在严苛度和防自欺机制上更深。 |
| [ngtiendong/Academic-Research-Agent-Skill](https://github.com/ngtiendong/Academic-Research-Agent-Skill) | 面向 CS/AI/数学硕博的人类引导式科研 agent 技能:文献接地、novelty gates(创新性闸门)、数学形式化、实验规划、reviewer simulation(审稿人模拟)、claim verification(论断核验)。 | 16 | 2026-05-24 | 功能定位高度重合(novelty gate + reviewer 模拟 + claim 核验都对应 Light 的闸门/对抗/检索证否)。强:覆盖更广(还含数学形式化、实验规划)、明确 human-guided。弱:star 低、无 Light 的八维加权数值化打分体系、无反谄媚量化协议、无先盲后明隔离、检索证否的硬量化(HTTP 码+3篇+delta)未见。 |
| [january-blue/OpenNovelty](https://github.com/january-blue/OpenNovelty) | LLM 驱动的论文新颖性评估流水线:四阶段(抽取论断→检索相关工作→深度对比分析→生成 novelty 报告),强调 transparent / evidence-grounded / verifiable,降低人工评审的主观性与覆盖盲区。 | 134 | 2026-05-12 | 与 Light 的'检索证否+量化 delta'内核最契合。强:检索接地与证据可验证做成了专门 pipeline,创新性比对更系统、可复现。弱:只评 novelty 单维,不像 Light 八维加权+否决项 gate+五视角对抗;是独立 Python 工具非可插拔 skill;不评 idea(评成稿论文),无反谄媚与盲审隔离。Light 可借鉴其 evidence-grounded 检索流程的工程化。 |
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 端到端全自动科研框架(Nature 发表):自动生成 idea、写代码跑实验、写论文,并内置 LLM automated reviewer 用 NeurIPS 式打分对产出论文评审。 | 13956 | 2025-12-19 | 该领域旗舰。强:全自动闭环、NeurIPS 评分 reviewer 有学术背书、生态巨大。弱:reviewer 是流水线里的产物评分器,非 Light 那种硬闸门式严审 idea;无先盲后明、无反谄媚配额、无 read-only/data 隔离;评论文非评 idea;是重型 Python 框架而非轻量可路由 skill。 |
| [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | AI Scientist 第二代:Agentic Tree Search 驱动的 workshop 级自动科研发现,改进了 idea 探索与实验代理树搜索。 | 6561 | 2025-12-19 | 强:idea 探索用树搜索更强、规模大。弱:同 v1,reviewer 仍是产物评分而非 idea 硬 gate;无 Light 的反谄媚/盲审/检索证否量化协议;非 skill 形态。 |
| [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher) | NeurIPS2025 自主科研创新 agent,从想法到实现的生产级全自动框架(配套 novix.science)。 | 5453 | 2025-10-16 | 强:自主创新 + 生产级落地、学术背书。弱:重在'生成与实现'而非'严审 idea 把关';无先盲后明、八维加权、反谄媚、Devil's Advocate;非轻量 skill。 |
| [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | 端到端自主科研工作流,辅助人类研究者落地研究 idea(文献综述→实验→报告),含评审/反思环节。 | 5681 | 2025-08-20 | 强:全流程协作框架、human-in-the-loop。弱:评审是流程内反思,非独立硬闸门;无 Light 的数值化八维 gate、反谄媚量化、检索证否硬指标;偏执行非把关。 |
| [zhu-minjun/Researcher (CycleResearcher/CycleReviewer)](https://github.com/zhu-minjun/Researcher) | ICLR2025 工作:CycleReviewer(自动评审模型,作奖励信号)与 CycleResearcher 训练成环,用自动评审迭代提升自动科研质量;放出 12B/72B 评审模型。 | 393 | 2026-03-05 | 强:把'评审当奖励'做成可训练模型、有数据/权重、量化评审能力强、ICLR 背书。弱:是训练好的评审 LLM 而非可解释 prompt 协议;无先盲后明、反谄媚配额、五视角与显式否决项 gate;评论文非把关 idea 回循环。Light 可借鉴其 reviewer-as-reward 的闭环思想。 |
| [deep-diver/paper-reviewer](https://github.com/deep-diver/paper-reviewer) | 从 arXiv 论文自动生成综合 review 并转成博客,驱动 HuggingFace Daily Papers 网站。 | 839 | 2025-02-20 | 强:实战驱动真实站点、review 生成成熟。弱:做的是描述性 review 生成,非严苛打分把关;无评分 gate、反谄媚、盲审、检索证否;评成稿非 idea。 |
| [bytedance/pasa](https://github.com/bytedance/pasa) | 字节 PaSa 论文搜索 agent:自主决策调用搜索工具、读论文、选参考文献,完成复杂学术查询。 | 1591 | 2025-05-27 | 仅对应 Light 的'强制检索证否'子环节。强:学术检索/相关工作召回能力强、可复现。弱:只做检索不做评审打分,无 gate/对抗/反谄媚/判决;可作为 Light 检索证否环节的能力补强参考。 |
| [The-Swarm-Corporation/AI-CoScientist](https://github.com/The-Swarm-Corporation/AI-CoScientist) | 对 Google 'Towards an AI co-scientist' 论文的极简可靠实现(基于 Swarms 框架),多 agent 生成与辩论式精炼科研假设。 | 111 | 2025-10-27 | 强:多 agent 辩论式精炼假设,与 Light 的五视角对抗思路相近、轻量。弱:偏生成/协作非严审把关;无数值八维 gate、反谄媚配额、先盲后明、检索证否硬指标。 |

### Light 该技能可借鉴的点
- 借鉴 OpenNovelty 把'检索证否'工程化为固定四阶段 pipeline(抽论断→检索相关工作→深度对比→novelty 报告),让 Light 的强制检索更可复现、覆盖更系统,而不止于'至少两库交叉'的约束描述
- 借鉴 CycleResearcher 的 reviewer-as-reward 闭环思想:Light 的 Roadmap 回 m03 已是闭环雏形,可把审稿评分显式作为下一轮 ideation 的优化奖励信号,量化迭代收敛
- 借鉴 HKUSTDial idea-evaluator 的 lifecycle/capability matching 与 paradigm-shift probe,在八维之外补一个'与作者实际资源/数据/周期是否匹配'的可行性视角,避免只评学术新颖性
- 借鉴 The-Swarm-Corporation/AI-CoScientist 与多 agent 辩论框架,把五视角对抗从单模型角色扮演升级为真正独立的多 agent 辩论,降低单模型自我一致性偏差
- 借鉴 bytedance/pasa 的自主检索 agent 能力,增强 Light 检索证否环节的相关工作召回率与参考文献精选,减少 evidence-missing 误判
- 参考 ngtiendong 技能把 novelty gate / reviewer simulation / claim verification 模块化的做法,以及 AI-Scientist 公开的 NeurIPS 式 reviewer prompt,校准 Light 八维 anchor 与 Overall 映射,使分数与真实会议口径更可比
