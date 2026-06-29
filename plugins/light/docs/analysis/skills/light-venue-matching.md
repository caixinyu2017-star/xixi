# light-venue-matching — 深度分析与同类对标

> 源：[`skills/light-venue-matching/SKILL.md`](../../../skills/light-venue-matching/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：把"论文实力 + 作者背景 + 预算/时间目标"映射到中外期刊/会议的分层投稿方案,核心卖点是"反编造录用率"——用可核查信号做高/中/低定性分级,而非抓 LetPub 录用比例编百分比。

## 核心运行逻辑
先盘点作者实力七要素(创新/实验/语言/背景/deadline/预算/目标),再用 db01 期刊库按 subject_area 筛候选、不足时用 OpenAlex Sources 程序化扩候选,对每个候选填一张"统一对比字段表"(三套指标 + 三套分区 + 周期 + APC/OA + 收录核查)。最关键的设计是一条贯穿全文的铁律:除非 venue 官网/正式报告公开接收率并能附链接,否则绝不输出录用概率百分比,LetPub 的"录用比例"被显式禁止当概率引用。录用可能性改走"五个可核查信号(作者相对实力/方向匹配/方法规模/官方接收率档位/创新性自评)逐项打高中低 + 标来源"的 rubric,每条分级必须跟"因为…(引哪个信号+来源)"。最后产出冲刺/稳妥/保底三档推荐,叠加白名单(DOAJ/WoS/Scopus 收录)+黑名单(中科院预警名单+假会议三红线)的预警双向筛查。脚本 venue_signal.py 把五信号里能程序化的部分(发文量趋势/外向自引粗估/作者主题重叠/APC+分区)封装成统一口径 JSON,每信号独立降级、取数失败标 unavailable 不编数。

## 关键步骤
- 1. 输入盘点:论文质量(创新/实验/理论)、方向、语言、作者背景(本科/硕博/有无强导师)、deadline、预算(能否付APC)、目标(毕业/评奖/求职/纯发表)
- 2. 候选生成:db01 按 subject_area 筛 → 不足时 OpenAlex Sources REST(topics.id/is_oa/apc/h_index 过滤+cursor翻页)扩候选 → 计算机方向直接对 CCF 目录按领域+目标档取候选
- 3. 统一字段抓取:每候选填影响指标(IF+JCR分区/CiteScore+分位/SJR/中科院分区)、档位(CCF/北大核心/CSSCI/CSCD)、周期、APC/OA/DOAJ、收录核查(WoS MJL/Scopus/EI Compendex Source List)
- 4. 可选跑 scripts/venue_signal.py:输入 ISSN+作者+db01卡,输出五信号对照 JSON,统一口径填表
- 5. 录用可能性评估:五信号逐项打高/中/低并标来源,按汇总规则(多数高且无致命短板=高;有1致命短板=中;方向/方法/作者实力明显不达标=低)给总评
- 6. 预警筛查:白名单(DOAJ Seal/WoS/Scopus索引)正面信号 + 黑名单(中科院预警名单/异常自引/超快审稿/国人占比畸高/假会议三红线),命中标红劝退联动 a10
- 7. 分层推荐:冲刺/稳妥/保底各1-3个,附理由+定性分级+周期+费用+风险
- 8. 产出:对比表(templates骨架)+ 投稿策略(先投哪、被拒转投顺序)+ 风险提示
- 9. 衔接:选定后 m12 套模板、m10 调引用格式,投稿决策入 db09,被拒转投回本技能重排

## 自带资产
- SKILL.md — 主流程 + 录用可能性 rubric(五信号+汇总规则)+ 反编造百分比铁律 + 工具各司其职口径表
- references.md — 14 个数据源的逐工具核查笔记(OpenAlex Sources/Authors、SJR、JCR、WoS MJL、Scopus、DOAJ、CCF、北大核心、CSCD/CSSCI、中科院分区、Elsevier/Springer/IEEE 匹配器、LetPub、EI Compendex 路径、国内会议信号源),每条带【是什么/端点参数/链接/已知坑】,部分含 2026-06 curl 实测留痕
- scripts/venue_signal.py — 五信号对照查询脚本,封装 OpenAlex Sources/Authors,含外向自引粗估、作者主题 Jaccard 重叠、发文量趋势、APC+分区,带离线 mock selftest 与逐信号优雅降级
- templates/venue_compare_table.md — 交付物骨架:横向对比矩阵 + 逐 venue 详情卡 + 录用可能性分级填空,顶部写明四条铁律

## 优点
- 反学术诚信风险的设计是真亮点且落到实处:不是口号,而是 SKILL/references/template/脚本四处一致地禁止把 LetPub 录用比例当概率、强制'待核查—无官方公开数据'、强制每个指标带来源+年份,这正是审稿人和评估者最容易被忽悠的地方
- 三套分区(JCR/SJR/中科院)+三类指标(引用热度/声望加权/国内档位)口径不混用的纪律贯穿全文,且明确'中科院1区≈前5%远难于JCR Q1'这种容易踩坑的差异,体现真实领域know-how
- references.md 的工具笔记质量高:不仅给端点参数,还给已知坑(OpenAlex 2yr_mean_citedness≠IF、ESCI≠SCI、出版商匹配器有偏向、CDN链接会变要现取),并有 2026-06 curl 实测 HTTP 状态码留痕,可信度高于泛泛罗列
- 脚本工程质量扎实:每信号独立 try/except 降级、取数失败标 unavailable+reason 不编数、离线 mock selftest 覆盖五信号全路径+三条降级路径,作者重名强制输出 disambiguation_caveat,与 SKILL rubric 严格对齐
- 对'学生/本科生/弱导师'群体的针对性强:强调用'档位'(CCF/中科院分区)而非裸 IF,提醒 Springer/掠夺刊 APC 偏高、本科生预算敏感,假会议三红线对国内低年级学生很实用
- 预警筛查白名单+黑名单双向,且把'国人发文占比畸高/超快审稿/年发文激增'这些中文学术圈特有的掠夺信号纳入,本土化到位

## 缺点 / 可被质疑处
- 对 db01 期刊库的依赖是最大隐性短板:全流程(候选筛选、审稿周期、APC、分区、代表作、五信号信号3/5)都建立在 db01 venues.csv 已存在且字段齐全的假设上,但技能本身不交付 db01,也未说明 db01 不存在/为空时的冷启动路径,新用户极可能卡在第一步
- 脚本的'外向自引粗估'方法学上偏弱且易误导:它统计的是'本刊论文引用本刊的比例'(outgoing),而预警关心的是'期刊自引率'通常指 incoming(被引中来自本刊的比例),二者不是一回事;虽然代码 method 字段诚实标注了,但用 >25% 这个本为 incoming 设的阈值去 flag outgoing 比例,阈值缺乏依据,可能产生误报
- 五信号 rubric 里有两项(官方接收率、创新性自评)在多数真实情况下要么'待核查'要么'主观',真正可客观核查的只剩作者实力/方向匹配/方法规模三项,而其中'方法规模匹配'高度依赖人对 representative_papers 的主观判读;rubric 看似严谨,实际可操作的客观信号偏少,容易退化成三项里两项靠人拍脑袋
- 作者相对实力信号严重受 OpenAlex 重名问题制约:中文拼音姓名聚合/拆分误差大,脚本只取 search 首个命中,虽标了 caveat 但对'弱导师本科生'这一目标用户,h-index 对比往往直接 unavailable 或失真,该信号实际贡献度可能很低
- 覆盖学科明显偏理工/计算机:CCF、EI Compendex、中科院分区、IEEE Recommender 都很细,但人文社科只有 CSSCI 一节、艺术人文(AHCI/只用JCI)几乎未展开,真正给社科作者定位时工具链和档位梯度的指导薄弱
- 缺少对'同一篇论文跨方向投稿'和'转投顺序'的具体算法:SKILL 说'被拒后转投顺序'但没给排序逻辑(按周期?按命中率?按 scope 距离?),策略建议这块停留在原则层面,不如对比表那样可执行
- 脚本与 SKILL 的'五信号'命名一致但内容并不完全对应:脚本信号3/4/5 与 rubric 的信号1/2/3/4/5 编号不同(脚本是发文量/自引/周期/作者匹配/APC,rubric 是作者实力/方向/方法/接收率/创新),容易让用户误以为跑完脚本=完成了 rubric 五信号评估,实际脚本只覆盖了 rubric 的部分且口径不同

## 可优化点（供后续逐技能优化）
- 补一份 db01 冷启动指南或最小 venues.csv 种子模板:列出必填字段(venue_name/issn/subject_area/review_cycle/apc_fee/cas_quartile/jcr_quartile/representative_papers/last_checked_date),并在 SKILL 开头加'若无 db01 则先用 OpenAlex+本节字段现建临时卡'的分支,消除冷启动卡点
- 脚本自引信号要么改为抓真正的 incoming 期刊自引率(用 OpenAlex group_by 施引来源或直接读 source 的自引统计),要么把 >25% 阈值明确改为'仅作 outgoing 粗筛、不等同期刊自引率',并下调/标注阈值来源,避免按错口径误报掠夺
- 统一脚本与 rubric 的'五信号'编号与命名,或在脚本输出里显式标注'本脚本覆盖 rubric 的哪几项、哪几项仍需人工',防止用户把跑脚本误当完成评估
- 把'转投顺序'做成可执行规则:例如按(方向匹配度↓ → 接收信号↓ → 周期↑ → APC↑)的字典序给出 fallback 链,或给一个被拒原因→下一档建议的映射表,让策略建议和对比表一样可落地
- 补强社科/人文工具链:为 CSSCI/AHCI/JCI 路径增加和理工对等的'档位梯度 + 收录核查 + 周期来源'小节,并说明社科会议/集刊的特殊性,平衡学科覆盖
- 给五信号 rubric 增加一个'最低可评估信号数'门槛(如可核查信号<2 项时,总评只能给'数据不足,不下定性结论'),防止 rubric 在数据稀疏时退化成靠主观项硬凑结论
- venue_signal.py 增加可选的速率限制/重试退避(自引信号会发多个批量请求),并把 MAILTO 占位改为从环境变量或参数读取,避免真实调用时都用 example.com 占位邮箱

## 与其他 Light 技能/知识库的衔接
["上游 db01(期刊会议库):候选来源与审稿周期/APC/分区/代表作的主数据源,本技能强依赖但不交付;m01(light-literature-search)的 references「OpenAlex 接入真相源」节是 OpenAlex key/限流/计费的唯一口径,本技能和脚本都不复写、直接指向", "下游 m12(light-typesetting)套对应模板、m10(light-citation)按 venue 调引用格式(reference_style 字段在对比表里就为此预留);投稿决策与记录入 db09(投稿记录库),被拒转投时回流本技能重排", "横向 a10(light-research-ethics):预警筛查命中掠夺刊/假会议时标红劝退并联动 a10 做合规处理;CONVENTIONS §1(投前数据重核)和 §3(对比表字段/铁律)是本技能模板和铁律的上位约定", "在 light-orchestrator 的论文 pipeline 中处于'成稿→投稿'的定位环节,典型上游是 paper-drafting/polishing/review-rebuttal 产出的成熟稿件,定位结果再驱动 typesetting+citation 的终稿排版"]

---

## GitHub 同类前沿技能对标

> 补跑日期 2026-06-13（原 workflow socket 断连失败后单独补检索）。star/更新时间经 GitHub API 实测。

GitHub 上与 light-venue-matching 同类的开源项目可分四类：(1) 学术界经典的"投稿期刊推荐器"(JANE、journal_targeter、preprint-similarity-search)，基于摘要/参考文献做文本相似度或 ML 匹配，数据权威但只解决"哪本期刊主题相近"，几乎不碰录用可能性分级、预算/时间分层和掠夺性预警；(2) 掠夺性期刊检查器(check-bib-for-predatory)，只做单点风险核验，正好是 Light 的一个子环节；(3) 2026 新兴 AI agent skill(journal-recommender、submission-nav)，形态最接近 Light，但多偏英文/医学场景，且部分把 JCR/CAS 分区或"录用比例"直接当结论；(4) 会议/CFP 评估(PRAGATI、openreview_finder、cfp-session-eval-council)，补足"会议"维度。真正像 Light 那样"把论文实力+作者背景+预算/时间映射成冲刺/稳妥/保底分层、用可核查信号给录用可能性定性分级、且拒绝把 LetPub 录用比例当官方统计"的开源项目几乎没有——Light 在"投稿策略决策层"是差异化的，且该细分方向 star 普遍偏低（尚未被充分占据）。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [Agents365-ai/asta-skill](https://github.com/Agents365-ai/asta-skill) | 指令包式 agent skill，封装 Ai2 Asta(Semantic Scholar) MCP 做学术检索 | 147 | 2026-05-25 | 强：同为 skill 形态、人气最高、有真实学术数据后端。弱：核心是文献检索而非投稿决策，不做 venue 分层/录用分级 |
| [zero565656/journal-recommender](https://github.com/zero565656/journal-recommender) | Agent Skill：期刊推荐、选刊、CAS/JCR 分区、Aims&Scope 匹配、发表风险检查 | 28 | 2026-05-27 | 最接近 Light。弱：依赖 JCR/CAS 分区结论，未见"录用可能性定性分级+拒用录用比例"协议，无统一对比字段框架 |
| [greenelab/preprint-similarity-search](https://github.com/greenelab/preprint-similarity-search) | Web app，用 ML 按预印本全文内容推荐期刊 | 22 | 2023-05-23 | 强：真实 ML 模型+可视化、可复现。弱：纯主题相似度，无作者/预算/时间维度，无分层、无掠夺性预警 |
| [danmackinlay/openreview_finder](https://github.com/danmackinlay/openreview_finder) | 对 OpenReview 上的会议/期刊做语义检索 | 9 | 2026-05 | 强：覆盖会议、语义搜索。弱：只检索不评估，无录用可能性、无 APC/索引统一字段 |
| [bhaskatripathi/Journalfinder](https://github.com/bhaskatripathi/Journalfinder) | 按论文给出最匹配期刊的查找器 | 9 | 2023-04-10 | 强：轻量直接。弱：基本是主题匹配脚本，无策略分层、无风险预警、久未更新 |
| [ShuvraneelMitra/PRAGATI](https://github.com/ShuvraneelMitra/PRAGATI) | Agentic 工作流：为论文推荐研究会议，或判定"不可发表" | 8 | 2025-05-08 | 强：agentic、含可发表性门槛、面向会议。弱：不做期刊、无预算/索引/APC 维度，无掠夺性核验 |
| [mi-erasmusmc/JANE](https://github.com/mi-erasmusmc/JANE) | 经典 Journal/Author Name Estimator，按文本估计目标期刊/作者 | 6 | 2026-03-20 | 强：生物医学权威老牌、被广泛引用。弱：只做主题相似匹配，无录用分级/分层/预算维度 |
| [CfKu/check-bib-for-predatory](https://github.com/CfKu/check-bib-for-predatory) | 检查 BibTeX 参考文献中是否含掠夺性出版商/期刊 | 6 | 2025-02-15 | 强：掠夺性核验专一、可当数据源/子模块。弱：仅风险检查一环，不做选刊与投稿规划 |
| [Townsend-Lab-Yale/journal_targeter](https://github.com/Townsend-Lab-Yale/journal_targeter) | Web app：基于标题/摘要/参考文献计算期刊"适配度指标" | 1 | 2026-05-04 | 强：有同行评审背景、显式 suitability metrics。弱：仍是匹配度量，无录用分级、无分层与作者背景维度 |
| [qwerty239qwe/submission-nav](https://github.com/qwerty239qwe/submission-nav) | AI agent skill：从 PDF/DOCX 草稿出发选刊、查投稿规则、规划修改 | 0 | 2026-05-21 | 形态最像 Light(skill+从草稿入手+查 submission rules)。弱：star 极低，未见录用分级与掠夺性预警硬协议 |
| [ponchotitlan/cfp-session-eval-council](https://github.com/ponchotitlan/cfp-session-eval-council) | 多 agent council 评估并打磨会议 CFP 投稿 | 2 | 2026-03-26 | 强：多 agent 对抗式评估值得借鉴。弱：面向 CFP 内容打磨而非 venue 选择与录用评估 |

### Light 该技能可借鉴的点
- 接入真实检索后端做事实锚定(OpenAlex/DOAJ/Semantic Scholar/OpenReview)，在"找候选刊"环节增加可选检索数据源接口，降低 LLM 编造期刊风险(asta-skill/openreview_finder/JANE 的做法)
- 吸收成熟的主题适配度量(journal_targeter 的 suitability metrics、preprint-similarity-search 的全文相似度)，给冲稳保分层补一个可解释的相似度信号
- 把掠夺性检查做成可调用子模块(借 check-bib-for-predatory 按出版商/ISSN 比对的实现)，并明确数据来源与时效
- 引入多 agent 对抗式评估(PRAGATI 可发表性门槛、cfp council 多视角)，给录用可能性分级加乐观/严格双视角交叉，增强稳健性
- 强化会议维度(多数期刊工具忽略会议)：保持会议(CFP/截稿/录用率信号/CCF 等级)与期刊同等的统一对比字段，做实差异化优势
- 打通"投稿草稿→自动填充论文实力字段"链路(借 submission-nav 从 PDF/DOCX 抽取)，减少用户手填
