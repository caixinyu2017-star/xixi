# db02-paper-writing 升级规划

> 分析日期 2026-06-13 ｜ 基于真实 schema + 依赖技能消费方式 ｜ 只读规划,未动库
> 原始库标识：db02-paper-writing

## 目标形态
升级后 db02 分三层、各司一职。① 方法论层(A-通用,本地精养):patterns_library.md + writing_cards.md 领域无关套路 + samples_real「跨样本归纳 A/B/C/D 表」合并为唯一的"领域无关写作方法论"主体,是三个写作技能的真正消费对象。② 样本层(偏科,打标签隔离):24 张真实论文卡保留,但每卡加 domain_scope/research_field 标签,AI 文化专属的"竞赛排名最硬/开源 social proof/beat baseline"背书规则从通用层剥离、降级为 cs.AI/cs.CV 方向专属规则,非该方向用户可过滤。③ 事实层(B-易变,薄缓存+实时):每卡的被引数/venue 待核查项不再当正文断言,收进卡尾"volatile 块"——只存 source_pointer(DOI/OpenAlex id 这种稳定锚)+ cited_by_snapshot + last_checked_date,真实数值用时实时查 OpenAlex,冲突默认信在线。README 卖点同步诚实缩水:从"16 篇被引实拉"改述为"N 张结构样本卡 + 实时可核的元数据指针"。

## 逐字段处置
| 字段/内容块 | 类别 | 动作 |
|---|---|---|
| patterns_library.md 全文(摘要五段/IMRaD/hedging/措辞红线/审稿人五问/§11 提问清单) | A-通用 | 抽为方法论层主体。原样保留并设为三技能的规范消费入口;仅把内嵌的两条指南被引(Whitesides 124/PLOS 79)纳入事实层薄缓存处理(见 realtime)。 |
| writing_cards.md「高频可迁移套路(领域无关)」+ 卡片模板 yaml | A-通用 | 留本地,与 patterns_library 合并去重(标题套路/实验节序/审稿追问/措辞红线已与 patterns_library §1/§6/§11/§12 重复),保留 yaml 模板并在其中加 domain_scope/source_pointer 新字段。 |
| samples_real.md「跨样本归纳 A 标题速查表 / B 摘要五段×类型 / C 贡献句式 / D 背书清单」 | A-通用(D 块偏科) | A/B/C 三表抽到方法论层(这是最有价值的领域无关沉淀);D『可信度背书清单』中『竞赛排名最硬/开源 social proof/业界采用』打 domain_scope=cs.* 标签隔离,『理论保证/真实部署/第三方基准』保留为通用。 |
| 每卡 title_pattern / abstract_structure / contribution_sentence 套路 / limitation_expression | A-通用 | 留本地。模式抽象本身领域中立,是样本卡的核心训练价值,精养保留。 |
| 每卡 related_work_taxonomy / experiment_design / figure_table_logic / method_narrative | A-偏科 | 打领域标签隔离。这些含 FID/IS/mAP/PSNR/scaling law 折线/ablation/3DGS 等强 CV-ML 烙印的实例,加 domain_scope,通用层只抽出其领域中立骨架(如 method_narrative 的『直觉→形式化→框架图→模块→复杂度』)。 |
| 每卡 reviewer_potential_questions | A-偏科(部分通用) | 双层处理:patterns_library §11 的通用清单留通用层供 m14;samples_recent 各卡的具体追问(IAA/scaling law/FID 公平比较)随卡打 domain_scope。 |
| 24 卡的被引数(samples_real 16 + samples_recent 8) | B-事实(易变) | 转实时查。从正文断言降级为卡尾 volatile 块:cited_by_snapshot=<值> + last_checked_date + source_pointer;用时查 OpenAlex,冲突信在线。 |
| venue『待核查』项(VGG/Adam/BatchNorm/word2vec/scikit-learn 的 ICLR/ICML/JMLR) | B-事实 | 转实时/打标签隔离。OpenAlex source 指向 arXiv 镜像,正式 venue 经 Crossref/DOI 前缀核实后填 verified_venue,未核实保留『待核查』标记不当定论。 |
| 每卡 DOI / OpenAlex id | B-事实(稳定) | 留本地作 source_pointer。DOI/OpenAlex id 是不变锚点,正是薄缓存的『来源指针』,实时刷新被引时按它回查。 |
| 获奖身份(NeurIPS/CVPR Best Paper)+ 作者/年份 | B-事实(稳定) | 留本地,source_url 锚定官方公告页。一旦公布即不变,无需实时,但标 last_checked_date。 |
| samples_real.md 各卡『摘要原文(倒排还原)』全段 | B-事实 + 合规风险 | 建议删/降级为结构笔记。与 samples_recent『只存结构笔记不录原文』的版权纪律冲突,需用户拍板是否统一降级(见 decisions)。 |
| impact_factor / 分区 / 录用率(README/卡内标注『OpenAlex 不提供、待核查』) | B-事实 | 不本地存值,转指针:指向 db01 venues.csv 同名字段(jcr_quartile/cas_quartile/impact_factor),由 venue_signal.py 路径取,db02 不重复维护。 |

## B 类转实时设计
查哪个 API:OpenAlex Works 端点(literature-search references 已实测 /works 与 cited_by_count 字段存在)。按稳定锚回查单篇——DOI 优先 `GET https://api.openalex.org/works/doi:{DOI}?select=cited_by_count,publication_year,primary_location&mailto=...`,无 DOI 用 `GET /works/{OpenAlexID}?select=...`。复用 venue_signal.py 的 http_fetch/_add_mailto/优雅降级范式;但注意 venue_signal.py 只覆盖 Sources/Authors,无 Works 被引刷新——需在该脚本加一个 `--work-doi/--work-id` 子模式,或新建 scripts/paper_signal.py(更内聚)。薄缓存存什么:每卡 volatile 块存 {cited_by_snapshot:<采集值>, last_checked_date:<YYYY-MM-DD>, source_pointer:{doi, openalex_id}}——存数值是为离线可读,但定位为『快照、会增长』而非事实。冲突信谁:按用户已定哲学,本地快照与在线不一致时默认信在线,并就地刷新 snapshot+last_checked。无网降级:展示 cached snapshot 并强制带『as-of <last_checked_date>,被引会增长』标签(沿用现卡已有措辞),绝不把快照当现值。OpenAlex 接入 key/限流口径不在此复写,只放一行指针指向 m01 references『OpenAlex 接入真相源』。venue 待核查项用 Crossref `GET https://api.crossref.org/journals/{ISSN}` 或按 DOI 前缀(10.1109/cvpr.* 等)交叉核实,免 key。

## 偏科隔离设计
给样本层每张卡加两个标签:research_field(粗方向,取值 cs.CV/cs.AI/cs.LG/cs.CL/stat.ML/eess.IV-medical/agri-CV/stat-methodology 等,对齐 arXiv 类目便于机读)与 domain_scope(该卡背书规则的适用边界,如 'AI/CV/系统类会议-竞赛与开源背书有效')。现状偏科证据:24 卡中 ResNet/AlexNet/VGG/ImageNet/Faster R-CNN/GoogLeNet/BatchNorm/VAR/Mip-Splatting/BioCLIP/RichHF/GenImageDynamics 等 20+ 为 cs.CV/cs.AI;Lasso(stat)/NSGA-II(优化)/YOLO survey(agri)/cancer imaging(medical)/ChemCrow(LLM-agent) 是少数非纯 CV。过滤方式:卡片用 YAML front-matter 写标签,三技能在取卡时按当前论文 research_field 过滤——非 cs.* 方向论文取卡时,自动跳过 domain_scope 限定为 AI 的背书规则(竞赛排名/SOTA/开源 social proof),改用通用层的中立背书(理论保证/第三方基准/真实部署)。通用层(patterns_library + A/B/C 表)不打 domain_scope,对任意学科开放。README 增『按方向取卡』使用说明,并诚实标注当前样本 CV/AI 偏置,邀请按用户域补样本(已有 agri/medical/stat 种子)。

## A-通用判断 → 方法论层
A-通用判断沉淀到一个领域中立的方法论主体:以 patterns_library.md 为骨架,把 samples_real『跨样本归纳 A/B/C 表』(标题模板速查 / 摘要五段×论文类型 / 高复用贡献句式)与 writing_cards 领域无关套路并入,去重(三处现有重复:标题套路、实验节序、审稿追问、措辞红线)。组织为对任意学科成立的『写作骨架库』:每条规则标明是否领域中立,凡带学科前提的(竞赛/开源/SOTA 背书、CV 专属图表逻辑)一律下沉到样本层并打 domain_scope,不混入方法论主体。这样 m07/m08/m14 默认消费方法论层即可拿到跨学科可用的判断力,样本层按需按方向调取。方法论层内嵌的两条写作指南被引(Whitesides/PLOS/Peyton Jones)按 B 类薄缓存处理但因数值稳定、查询成本低,实时刷新优先级最低。

## schema 改动
CONVENTIONS §3 现无 db02 writing_card schema(只有 venue/method/dataset/project 四类),db02 schema 目前是 README/writing_cards 局部声明。建议:writing_card schema 新增 research_field、domain_scope、source_pointer(doi+openalex_id)、volatile{cited_by_snapshot,last_checked_date} 四块;last_checked_date 复用 db01 同名字段语义(CONVENTIONS §3 已有)。是否把 domain_scope/research_field 提升为 CONVENTIONS §3 跨库统一字段待决(见 decisions)。被引数从『卡内正文断言』改为『volatile 块快照』不算新增字段、是定位降级。venue 字段拆为 verified_venue(已核实)+ venue_note(待核查标记)两子项,避免把待核查当定论。

## 影响的技能及改法
- **light-paper-drafting**：SKILL §写作前 line 26/30『从 db02 抽取结构套路』:明确区分两类消费——结构套路(title_pattern/节序/摘要五段)取自方法论层,领域中立直接用;但取『可信度背书』时必须按目标 venue 的 research_field 过滤样本卡,非 cs.* 方向禁用竞赛排名/SOTA/开源 social proof 背书(防止给农业/医学/统计论文写歪)。新增一行:若引用任何卡内被引数/venue 作为论据,必须经 OpenAlex 实时刷新,不得信 snapshot。
- **light-paper-polishing**：SKILL line 42『摘要/引言/结论按 db02 高水平套路重写』:套路源指向方法论层(领域中立),无需改逻辑;仅加注该套路已剥离 AI 文化背书,润色非 CS 稿时不照搬『beat baseline/SOTA』式表达。影响最小。
- **light-review-rebuttal**：SKILL line 42『取 db02 审稿人提问清单(patterns_library §11)』:§11 通用清单仍直接用;补一行——若按论文方向取 samples 卡的 per-card reviewer_potential_questions,需先按 research_field 过滤,CV 专属追问(FID 公平性/scaling law/IAA)不套用到其他学科。该技能已用 OpenReview API 实时取审稿语料,不依赖 db02 的 B-facts,事实层改动对其无影响。

## 迁移步骤
- 1. 在 writing_cards.md 的卡片 yaml 模板加四字段:research_field、domain_scope、source_pointer(doi/openalex_id)、volatile{cited_by_snapshot,last_checked_date};作为新卡 schema 真相源。
- 2. README.md schema 行(line 6)同步加上述字段;数据来源段(line 41-42)诚实改写:把『被引实拉/16 篇』改述为『结构样本卡 + 实时可核元数据指针,被引为快照需实时刷新』,并标注当前样本 CV/AI 偏置与按方向取卡说明。
- 3. samples_real.md:16 卡逐卡把『被引数：NNN(快照)』『DOI』『OpenAlex』三行重组为卡尾 volatile 块(snapshot+last_checked+source_pointer);venue 待核查项保留标记并补 verified_venue(经 Crossref/DOI 前缀核实的填,未核实留待核查)。
- 4. samples_real.md『跨样本归纳 A/B/C 表』剪切到方法论层(并入 patterns_library 或新建 methodology 段),『D 背书清单』拆分:通用项留、AI 项打 domain_scope=cs.*。
- 5. samples_real.md『摘要原文(倒排还原)』:按用户决策(见 decisions)统一降级为结构笔记或保留——若降级,16 段原文删除,补『结构归纳』,与 samples_recent 版权纪律对齐。
- 6. samples_recent_2024_2026.md:8 卡同样把被引/DOI 收进 volatile 块,加 research_field/domain_scope(cancer→medical、YOLO→agri-CV、ChemCrow→cs.AI-agent、其余 cs.CV)。
- 7. patterns_library.md:并入 A/B/C 表后去重(标题套路/实验节序/§11 追问与 writing_cards 重复段);两条指南被引标 last_checked_date。
- 8. 在 light-venue-matching/scripts/venue_signal.py 增 `--work-doi/--work-id` 子模式刷新单篇 cited_by_count(或新建 scripts/paper_signal.py),复用 http_fetch/降级范式;写离线 selftest。
- 9. 三技能 SKILL.md 按 affected_skills 改引用措辞(drafting line 26/30、polishing line 42、rebuttal line 42)。
- 10. 若 domain_scope/last_checked_date 决定进统一 schema,则更新 CONVENTIONS §3 增 db02 writing_card 条目并标注 last_checked_date 与 db01 同源语义。

## ⚠ 需要你拍板的决策点
- 薄缓存要不要存被引『数值』:db02 是训练库、被引仅作 social proof 非下游载荷,可选(A)存 snapshot 数值+as-of标签(离线可读) 还是(B)只存 source_pointer+定性标签(seminal/high-cited)、数值一律实时查不落地。建议 A,但需拍板。
- samples_real.md 16 段『摘要原文』是否统一降级为结构笔记:samples_recent 已守『不录原文』版权纪律,samples_real 存全摘要原文构成不一致与潜在版权暴露。降级更稳但损失部分还原细节,需用户定。
- domain_scope/research_field 进 CONVENTIONS §3 统一 schema 还是 db02-local:进则跨库一致(将来 db01/db09 复用),不进则改动最小。同时定 research_field 取值表(建议对齐 arXiv 类目)。
- 转实时是否强制联网:写作技能常离线消费样本卡。定降级策略——无网时是否允许直接用 cached snapshot(带 as-of 标签)继续,还是必须提示『未刷新』。建议允许,因被引非载荷数据。
- 被引刷新归谁执行:扩展 venue_signal.py 加 Works 子模式 vs 新建 paper_signal.py vs drafting 内联调 OpenAlex。建议新建轻量 paper_signal.py(内聚、不污染 venue 五信号逻辑)。
- 偏科是只隔离还是承诺补非 AI 样本:24 卡 20+ 为 CV/AI。仅打标签隔离 vs 同时立任务补 stat/med/agri/社科代表样本以平衡训练分布,影响工作量。

## 工作量与风险
- 工作量：中。三个 md 文件逐卡改造(24 卡加标签+volatile 块,机械但量大)+ 方法论层合并去重(需判断,中等)+ 一个轻量实时脚本(~150 行,复用 venue_signal 范式,轻)+ 三技能引用微调(轻)。最大不确定性在 samples_real 摘要原文去留与是否补非 AI 样本两个决策——前者影响合规、后者直接放大工作量。无破坏性数据库操作,全部为文本重构,可逐文件提交、可回滚。
- 风险：README 卖点缩水:从『16 篇被引实拉/22 万被引』式硬数字营销改为『结构样本+实时指针』,卡数表面价值下降,需诚实同步(背景已认可)。联网依赖加重:被引/venue 实时化后,无网或 OpenAlex 需 key/限流时降级为快照,若降级标签不醒目易被误当现值。迁移破坏现有引用:三技能对 db02 的引用是『结构套路』而非 B-facts,故破坏面小——但若 patterns_library 与 samples_real A/B/C 表合并后章节锚点变动,rebuttal『patterns_library §11』这类 section 引用需同步改,否则指空。偏科隔离若只打标签不补样本,训练分布仍 CV 偏置,非 CS 用户取到的通用层偏薄。samples_real 摘要原文若保留则版权风险悬而未决、若删则损失已投入的还原工作。
