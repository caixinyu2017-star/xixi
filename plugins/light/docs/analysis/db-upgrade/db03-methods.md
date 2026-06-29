# db03-methods 升级规划

> 分析日期 2026-06-13 ｜ 基于真实 schema + 依赖技能消费方式 ｜ 只读规划,未动库

## 目标形态
分三层。①方法论层(本地精养)：core_assumption/advantages/limitations/common_baselines/evaluation_metrics 这 5 个跨学科字段不动，是库的真正资产，m05 直接取。②薄缓存+实时层：representative_papers 的 cited 数、implementation_repo 的存活状态转实时查(复用 m01/venue_signal 的 OpenAlex+GitHub 模式)，本地只留 "DOI/repo 指针 + 快照值 + last_checked"，冲突信在线、无网降级到快照并标 stale。③隔离层：每卡/每文件打 domain_scope + maturity_scope 标签，把 82 张奶山羊 CV 卡和其 maturity 时间线圈成可过滤的偏科区，非该方向用户默认看不到。README 卖点从 "176 张实拉被引方法卡" 诚实改为 "176 张方法卡(方法论本地精养 + 被引/仓库状态实时核)"。

## 逐字段处置
| 字段/内容块 | 类别 | 动作 |
|---|---|---|
| method_name | A-通用 | 留本地。主键，去重锚点(method_cards.md canonical 索引已做)。 |
| task_type | A-通用 | 留本地。 |
| input_data / output_result | A-通用 | 留本地。方法的 IO 契约，跨学科稳定。 |
| core_assumption | A-通用 | 留本地精养。最高价值方法论资产，抽方法论层。 |
| advantages / limitations | A-通用 | 留本地。少量含 CV 时间线判断的(如'被3DGS替代')需迁入 maturity_scope 限定，不在 limitations 里硬写时效。 |
| common_baselines | A-通用 | 留本地。m05 直接取作对比设置,跨学科。 |
| evaluation_metrics | A-通用 | 留本地。m05 直接取，方法学通用。 |
| suitable_datasets | A-偏科(部分) | 留本地但只存数据集名(指针)。具体规模/许可转引 db04 dataset_card,不在本库复刻。奶山羊'无公开基准'的诚实声明保留,打 domain_scope。 |
| implementation_repo | B-事实 | 转实时查仓库存活(GitHub API)。本地留 org/repo 指针 + 上次状态 + last_checked;frontier 已有的'GitHub API 200/301/404'注释正是薄缓存雏形,推广全库。 |
| representative_papers (cited:N) | B-事实 | cited 数转实时(OpenAlex by DOI)。本地保留 标题+年份+DOI 指针 + cited 快照值 + 查询日期(已有);'待核查'标注保留。 |
| representative_papers (标题/年份/DOI) | A-事实-稳定 | 留本地。DOI 是实时查的主键,不变。 |
| possible_innovation_points | A-偏科 | 拆分:奶山羊专用建议(82卡)打 domain_scope 隔离;其中可泛化的'方法选型逻辑'(如长周期→稀疏采样/长尾→重采样)抽到方法论层,对任意学科成立。 |
| maturity | C-状态(偏科) | 留本地但加 maturity_scope 字段限定判断域(如 scope=CV-2026)。'过时/被替代'类判断标明只在某领域时间线成立,避免误用到其他学科。 |
| 各文件头部'适配说明'/'选型矩阵'块 | A-偏科 | 整块属奶山羊 CV,打文件级 domain_scope=cv-livestock。其中跨域选型方法论抽到方法论层。 |

## B 类转实时设计
查哪个 API:①cited 数用 OpenAlex Works,GET https://api.openalex.org/works/doi:{DOI}?select=id,cited_by_count,publication_year&mailto=（DOI 是现成主键，246 条多数有 DOI）;②仓库存活用 GitHub API,GET https://api.github.com/repos/{org}/{repo} 看 HTTP 200/301(迁移)/404(失效)——frontier 文件已实测过这套(facebookresearch/llama→301、facebookresearch/maml→404)。落地脚本:在 db03 或 m01 scripts 下建 method_signal.py，结构照搬 venue_signal.py(urllib 直连、graceful degrade、--selftest mock)。薄缓存存什么:每条 representative_paper 存 {title, year, doi, cited_snapshot, cited_checked_date};每个 repo 存 {org/repo, last_status, status_checked_date}。冲突信谁:默认信在线，实时值覆盖快照并回写 checked_date;若在线值与快照差异>50% 提示可能是 OpenAlex 记录合并/拆分(库里已知 arXiv vs 正式版分散问题),标注供人工核。无网降级:返回快照值 + status="stale" + 上次 checked_date,绝不崩、不编新数(照 venue_signal 的 unavailable 约定)。OpenAlex 2026 起需免费 key,key/限流唯一口径指向 m01 references「OpenAlex 接入真相源」,本脚本不复写数字、只加 mailto。待核实:GitHub API 未鉴权限 60 req/min,176 卡全量刷需分批或带 token,标"待核实是否需 token"。

## 偏科隔离设计
两个新标签。①domain_scope(卡级,枚举:general / cv-livestock / cv-general / nlp-speech / biomedical / stats-econ / physical-sci / frontier-ml)——82 张奶山羊卡及 detection_tracking/action_spatiotemporal/temporal_action/nighttime_multimodal 四文件整体标 cv-livestock;ml_stats/stats_econ/biomedical/physical_sciences 等标对应通用域。②maturity_scope(卡级,限定 maturity 判断成立的领域时间线,如 'CV-2026'、'NLP-2026')——把'过时/被替代'锁死在其域内。怎么过滤:m03/m04/m05 调用前按项目方向传 domain_scope 白名单(如非 CV 项目排除 cv-livestock);奶山羊项目则 domain_scope IN (general, cv-livestock, cv-general)。文件级可在每个 cards_*.md 头部 YAML 注 domain_scope，卡级覆盖文件级。通用层(general)对所有方向可见。README 增"按方向过滤"说明。

## A-通用判断 → 方法论层
把 A-通用判断沉淀为跨学科方法论资产，新建 db03-methods/methodology.md(或 method_cards.md 扩展为方法论索引)。内容:①从 core_assumption/advantages/limitations 提炼的"方法族选型原则"(如:长周期行为→稀疏长程采样/时序聚合;数据稀缺→自监督预训练;长尾→重采样/重加权解耦,与骨干正交;边缘实时→蒸馏/量化/轻量分解)——现散在 action_spatiotemporal 的"跨切面策略"和各卡 innovation_points,抽出后对任意学科的方法选型都成立。②common_baselines/evaluation_metrics 沉淀为"按 task_type 的标准对比设置查找表",m05 直接调。组织:按 task_type(分类/检测/时序/生成/因果/表示学习)分组，每组给"主流骨干族 + 标准 baseline + 标准指标 + 选型决策树",与领域卡解耦,领域卡只引方法论条目 id。

## schema 改动
CONVENTIONS §3 方法卡 schema 当前 14 字段。建议新增 2 个隔离字段:domain_scope、maturity_scope(都是卡级标签,不破坏现有字段)。representative_papers/implementation_repo 不改字段名,改的是"值的语义"——从'权威事实'降级为'快照值+指针+last_checked'(在字段值内以 cited:N(checked:2026-06-06) 形式承载,无需加列,类似 §3 里 venues.csv 用 risk_note catch-all 追加 ai_policy 的做法,避免动 CI 列校验)。若要更结构化可在卡内 representative_papers 子项加 checked 后缀。决策点:domain_scope/maturity_scope 是否进 §3 统一 schema(影响其他库是否也加)。

## 影响的技能及改法
- **light-research-plan (m05)**：它直接从 common_baselines/evaluation_metrics/suitable_datasets 取对比设置——这些留本地不变,引用方式不动;但 suitable_datasets 改为'取名后转 db04 查规模/许可',SKILL 已说'数据集来自db04'，对齐即可。新增:取卡前按项目 domain_scope 过滤。
- **light-idea-generation (m03)**：已用 maturity 过滤'过时/做烂'方向——改为读 maturity+maturity_scope，避免把 CV 时间线误用到非 CV idea;novelty 检索它本就实时调 m01 脚本(不信本地 cited)，无需改。possible_innovation_points 引用改为分层:通用选型逻辑取方法论层,奶山羊专用建议仅 CV 项目取。
- **light-idea-critique (m04)**：用 maturity 判'已过时'——同样改读 maturity_scope 限定域;它本就实时查 OpenAlex/S2 做撞车复核，不依赖本地 cited，被引实时化对它透明。
- **light-literature-search (m01)**：它是 db03 的生产者(写入 method_card)。新增卡时须填 domain_scope/maturity_scope,representative_papers 写快照值+查询日期(本就在做)。可把新建的 method_signal.py 放 m01 scripts 复用其 OpenAlex 直连模式。

## 迁移步骤
- 1. 在 CONVENTIONS §3 方法卡 schema 追加 domain_scope、maturity_scope 两字段定义(决策通过后)。
- 2. 给 12 个 cards_*.md 每个文件头加文件级 domain_scope;其中 detection_tracking/action_spatiotemporal/temporal_action/nighttime_multimodal 标 cv-livestock,逐卡复核 82 张奶山羊卡确认。
- 3. 给所有带'过时/被替代'判断的 maturity(NeRF/SSD/C3D/P3D/LSTM 等)补 maturity_scope=CV-2026 等限定。
- 4. 新建 db03-methods/methodology.md:抽 action_spatiotemporal'跨切面策略'+各卡通用 innovation_points 为按 task_type 的选型决策树与标准 baseline/指标表;领域卡 innovation_points 拆为'通用逻辑(引 methodology id)+奶山羊专用(留本地打 domain_scope)'。
- 5. 建 scripts/method_signal.py:照 venue_signal.py,OpenAlex by-DOI 查 cited + GitHub repos 查存活,薄缓存回写,--selftest 离线 mock,降级 unavailable。
- 6. 把 246 条 representative_papers 的 cited 值统一改为带 (checked:日期) 后缀;implementation_repo 推广 frontier 的状态注到全库(脚本批量探一次回填快照)。
- 7. README 重写卖点:诚实标'方法论本地精养 + 被引/仓库状态实时核',卡数构成说明(通用层 X 张/CV偏科 82 张)。
- 8. m05/m03/m04 SKILL 引用节加'按 domain_scope 过滤 + maturity 读 scope'一句;m01 SKILL 产出节加'新卡必填 domain_scope/maturity_scope/快照日期'。

## ⚠ 需要你拍板的决策点
- domain_scope/maturity_scope 是否进 CONVENTIONS §3 统一 schema(只动 db03 局部，还是作为全库知识库的偏科隔离通用机制,影响 db01/db04 是否跟进)?
- 薄缓存到底存不存数值:存 cited 快照值便于无网降级但会过期失真,还是只存 DOI 指针、每次必联网查(更诚实但无网即不可用)?——倾向'存快照值+checked_date+stale 标记'。
- representative_papers 的 cited 转实时是否强制联网:m03/m04 本就实时检索不依赖本地 cited,这些 cited 数主要给人看/给 m01 文献表用,值得为它专门建 method_signal.py 周期刷,还是降级为'仅在 m01 维护时手动核、平时标 last_checked 让用户自判'?
- 82 张奶山羊卡是否物理拆分到独立子目录(db03-methods/cv-livestock/)做硬隔离,还是仅靠 domain_scope 软标签(改动小但混在通用卡里)?
- methodology.md 抽象层是新建独立文件,还是扩展现有 method_cards.md(它现在是模板+canonical 索引、0 实体卡)?

## 工作量与风险
- 工作量：中偏重。标签回填 176 卡 + 拆分 82 卡 innovation_points + 抽方法论层属人工密集(中);method_signal.py 脚本可照搬 venue_signal.py(轻);246 条 cited 批量加 checked 后缀可脚本化(轻)。总体一人 2-3 天，主要耗时在逐卡 domain_scope 复核与 innovation_points 拆分。
- 风险：①README 卖点缩水:'176 张实拉被引方法卡'改为分层表述后，对外卖点感知变弱，需诚实同步(用户已知)。②联网依赖加重:cited/repo 实时化后无网时这两字段降级，若 m01 文献表强依赖会受影响;靠 stale 标记缓解。③迁移破坏现有引用:m05 直接取 baselines/metrics 不受影响(留本地),但若误把 suitable_datasets 也实时化会断 m05;须保证只动 cited/repo。④maturity_scope 加得不彻底会留'过时'判断越域误用的隐患。⑤GitHub API 限流(60/min 未鉴权)批量刷 176 卡可能被限,需分批/加 token,标待核实。⑥domain_scope 枚举若与 db04 不一致会割裂,建议两库共用同一套域枚举。
