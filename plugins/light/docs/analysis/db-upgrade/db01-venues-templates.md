# db01-venues-templates 升级规划

> 分析日期 2026-06-13 ｜ 基于真实 schema + 依赖技能消费方式 ｜ 只读规划,未动库
> 原始库标识：db01-venues-templates (期刊会议与投稿模板,308行×19列单CSV,非卡文件)

## 目标形态
升级后 db01 是一个"薄事实缓存 + 厚方法论"的混合库,仍是单 venues.csv(19 列 CSV schema 不破 CI 列校验),但每行的 B 类易变值(IF/分区/被引/h_index/周期/APC/链接)被重新定性为"快照",必须随 last_checked_date 一起读、冲突时信在线。新增一个隐式锚点层:把散落在 indexing/risk_note 里的 ISSN 与 OpenAlex source id 规整为稳定查询键(写进 indexing 列固定位置或 risk_note 的 `oa_id=`/`issn=` 子串),让 venue_signal.py 能对全库实时复查而不只对单候选。A-通用判断(reference_style 映射逻辑、ai_policy 出版社政策口径、采集核验方法论)从"数据行"上抽出来沉淀进 README/references 作为跨学科资产。A-偏科判断(ccf_level 仅中国 CS、cas_quartile 仅中国语境)用 risk_note 内 `domain_scope=` 子串打标隔离,非该方向用户可过滤。README 卖点诚实改写:不再宣称"308 条权威 IF 库",而是"308 条 venue 锚点 + 实时复查管线 + reference_style/ai_policy 方法论"。

## 逐字段处置
| 字段/内容块 | 类别 | 动作 |
|---|---|---|
| source | C-状态 | 留本地。记录该行采集来源(openalex+websearch),是溯源元数据,本地权威。 |
| venue_name | B-事实(但极稳定) | 留本地作主键。venue 改名罕见,不进实时复查。 |
| venue_type | A-通用 | 留本地。journal/conference 二分稳定。 |
| publisher | B-事实(稳定) | 留本地;45 行'待核查(OpenAlex无host_organization)'转实时:venue_signal 查 OpenAlex Sources host_organization 兜底补。 |
| subject_area | A-偏科边界/B混合 | 留本地作过滤维度。261 个 distinct 值过碎,需归一到受控词表(否则 venue-matching 按方向筛会漏)。这是方法论层要做的事。 |
| level | A-偏科 | 留本地但打 domain_scope 标签。混合了 SCI(国际通用)/CCF(中国CS)/北大核心-CSSCI-CSCD(中国语境),不同体系不可混读。 |
| indexing | B-事实 | 留本地薄缓存 + 规整为 ISSN 锚点位。当前 ISSN 散落此列与 risk_note,只 251/308 行有,补全 ISSN 是实时复查前置。 |
| impact_factor | B-事实(高易变) | 转实时为主、薄缓存为辅。178 行已是真 JCR/LetPub 值(带 journalid+JCR2024+日期)→保留为快照值;122 行 OpenAlex 2yr 代理→标注口径非 JCR,实时用 venue_signal 复查;46 会议 N/A 保持。 |
| jcr_quartile | B-事实(高易变) | 薄缓存快照。87 行真 Q* 值保留+last_checked;110 行待核标注付费源;实时层 OpenAlex 无此字段,只能标'需 JCR/LetPub 付费源',不编。 |
| cas_quartile | A-偏科+B-事实 | 薄缓存 + domain_scope=中国语境标签。134 行真值(含'区')保留;仅对投中国体系用户有意义,打标隔离。 |
| ccf_level | A-偏科(强) | 留本地 + domain_scope=中国CS 标签。198 行 N/A(非CS venue 本就不该有),56A/28B/6C 真值保留;明确'仅中国计算机方向适用',非CS用户过滤掉。 |
| review_cycle | B-事实(中易变) | 薄缓存。128 行含待核;venue_signal 信号3 已从本卡读,保留本地值+last_checked,投前重核。 |
| apc_fee | B-事实(中易变) | 薄缓存 + 实时兜底。167 行待核;venue_signal 信号5 已用 OpenAlex apc_usd 兜底,本地存快照,冲突信在线。 |
| template_url | B-事实(链接易腐) | 薄缓存 + 失链检测。179 行 http;链接会腐,加轻量 last_checked,m12 取用前可校验 200。reference_style 映射逻辑抽方法论。 |
| submission_url | B-事实(链接易腐) | 薄缓存 + 失链检测。202 行 http,同上。 |
| reference_style | A-通用(方法论核心资产) | 留本地精养 + 抽映射逻辑为方法论。这是全库最高价值的跨学科 A 类:publisher→引用风格映射(Elsevier→elsarticle、IEEE→IEEEtran、Springer→LNCS、GB/T7714→中文)稳定且 m10/m12 直接消费。 |
| representative_papers | B-事实(易变) | 转实时。25 行空/占位;107 行(prior round)空;venue-matching 信号2 方向匹配用它,改为按 OpenAlex source.id 实时拉该刊被引前列 works,本地只留 2-3 篇快照。 |
| risk_note | 混合 catch-all | 拆解。内含 4 类异质内容:ai_policy=(A-通用方法论,抽出)、OpenAlex source id(B-锚点,规整为查询键)、掠夺预警(C-状态,留本地)、各种待核标注(降级为 last_checked 缺口)。 |
| last_checked_date | C-状态(管线核心) | 留本地并升级为'每字段块时效'语义。当前是行级单日期;薄缓存模型下它是判断'快照是否过期、要不要触发实时复查'的开关,check_freshness.py 已消费。 |

## B 类转实时设计
复用 light-venue-matching/scripts/venue_signal.py(已实测 OpenAlex Sources/Authors/Works,免 key 走 mailto 礼貌池,2026 起需免费 key 口径见 m01 references)。查的端点:①IF/被引/h_index/发文趋势/APC → `GET api.openalex.org/sources/issn:<ISSN>`(select=summary_stats,counts_by_year,apc_usd,host_organization),已在 oa_source_by_issn() 实现;②representative_papers → `GET api.openalex.org/works?filter=primary_location.source.id:<S...>&sort=cited_by_count:desc`,signal_self_citation 已用此模式;③publisher 兜底 → 同 source 响应 host_organization。**待核实 API 能力**:OpenAlex 不提供 JCR IF/JCR分区/CAS分区(这是付费 Clarivate/中科院数据),实时层只能给 OpenAlex 2yr_mean_citedness 代理值,真 JCR/CAS 必须保留本地快照+标 LetPub/付费源出处,不可声称实时。薄缓存每行存:快照数值(如 IF=18.6) + last_checked_date + 来源指针(risk_note 内 journalid=3411 或 oa_id=S4363607701)。冲突时默认信在线(CONVENTIONS §1 投前重核),但 JCR/CAS 这类 OpenAlex 查不到的字段,本地快照即最优解、不被覆盖。无网降级:venue_signal 各信号已独立 status=unavailable+reason 不崩,降级直接用本地快照值并明示'离线快照,last_checked=X,投前需联网重核'。前置阻塞:ISSN 只 251/308 行有、且非独立列(散在 indexing/risk_note),190 行有 oa_id;必须先把 ISSN/oa_id 规整为稳定查询键(写进固定子串位)实时复查才能覆盖全库。

## 偏科隔离设计
偏科字段:ccf_level(仅中国CS)、cas_quartile(中国语境分区)、level 中的北大核心/CSSCI/CSCD/CCF中文T1 部分。隔离做法:在 risk_note catch-all 内追加 `domain_scope=` 子串(沿用 ai_policy= 同模式,不加列、不破 19 列 CI 校验),取值如 `domain_scope=中国CS`(CCF系)、`domain_scope=中国语境`(CAS/北大核心系)、`domain_scope=通用`(SCI/国际)。venue-matching 按方向筛候选时:非计算机用户自动过滤掉 domain_scope=中国CS 的 CCF 档位展示;投国际刊用户隐藏 CAS/CSSCI 档。过滤实现轻量:消费方读 risk_note 子串判断,无需 schema 改动。46 会议 100% 是 CS 这一事实在 README 显式声明'本库会议覆盖偏 CS,其他学科会议待扩',避免误导非CS用户以为库内有其方向会议。

## A-通用判断 → 方法论层
三块 A-通用判断抽到 README + 新增 references.md(库级,当前库无 references.md):①reference_style 映射逻辑——publisher→引用风格→LaTeX cls/bst 的对应表(Elsevier→elsarticle-num、IEEE→IEEEtran、Springer→splncs04、ACM→acmart、GB/T7714→gbt7714-numerical),这是 m10/m12 直接复用的跨学科资产,与具体 venue 无关;②ai_policy 出版社政策口径——出版社级(Elsevier/IEEE/Wiley/Springer/Nature/ACM)政策按官方页批量标、会议按 CFP 单标的方法论(README 已有雏形,固化为可复现规则);③采集→双源核验→入库管线(README §采集管线已是优秀方法论,保留并强化'IF 必标口径:JCR 真值 vs OpenAlex 2yr 代理'的区分纪律)。subject_area 受控词归一表(261→约30个受控方向)也属方法论层,供 venue-matching 按方向稳定筛选。

## schema 改动
不动 19 列 CSV schema(CI 按列校验,加列会破 check_databases.py)。所有新字段沿用 CONVENTIONS §3 既定的'risk_note catch-all 子串'模式:新增 `domain_scope=`、`issn=`、`oa_id=` 三类子串(与既有 `ai_policy=` 同机制)。impact_factor 列不改结构但强制口径标注。last_checked_date 语义从'行级最后核查'升级为'快照时效开关'(check_freshness 已消费,无需改列)。新增库级文件 references.md(reference_style 映射表 + subject_area 受控词表),不属 CSV schema。

## 影响的技能及改法
- **light-venue-matching**：已最接近目标态:SKILL §1 已写'用 db01 按方向筛,不足时 OpenAlex 实时扩候选',venue_signal.py 信号3/5 已从 db01 卡读 review_cycle/apc/分区、信号1/2/4 已实时查 OpenAlex。改动:①把'db01 已存或 OpenAlex 查'的 h_index 推广到全 B 字段实时复查;②脚本 _load_card_from_csv 当前按 ISSN 模糊 blob 匹配,依赖 ISSN 在文本里——ISSN 规整为固定子串后改为精确取;③SKILL 显式声明'db01 的 IF/分区是薄缓存快照,投前 venue_signal 实时复查,冲突信在线';④按 domain_scope 子串过滤偏科档位。
- **light-typesetting**：SKILL §开工前已'确认 db01: template_url, reference_style, 单双栏'。改动:①template_url 标注为'易腐链接,取用前校验200,失链回 venue 官网 author kit';②reference_style 映射逻辑指向 db01 新 references.md 的 publisher→cls/bst 表,而非逐行读卡。
- **light-citation**：SKILL §衔接已'引用样式查 db01 reference_style 字段'。改动:把 reference_style→CSL/bst 的对应也指向 db01 references.md 方法论表,保持与 typesetting 同源,避免两技能各读各的。
- **light-literature-search**：SKILL §衔接'结果写入 db01'、已有 cn_journal_probe.py 按 ISSN 探 OpenAlex source。改动:①新增 venue 行时强制写 ISSN/oa_id 锚点(供 db01 实时复查),与 cn_core_issn.csv 锚点格式对齐;②采集管线方法论已与 db01 README 重叠,统一指向 db01 README §采集管线避免双份。

## 迁移步骤
- 1. 锚点规整(最高优先,实时复查前置):写一次性脚本扫 venues.csv,把散在 indexing/risk_note 的 ISSN 与 OpenAlex source id 抽出,统一回写为 risk_note 内 `issn=xxxx-xxxx; oa_id=S...` 固定子串。补齐缺 ISSN 的 57 行(用 venue_name 反查 OpenAlex)。遵守 README R4/R8 铁律:改前验物理行数==逻辑行数,含逗号字段加引号。
- 2. 字段口径标注:对 122 行 OpenAlex 2yr 代理 IF,确认 impact_factor 列已注明'(OpenAlex 2yr均被引,非JCR)';178 行真 JCR/LetPub 值保留并确认带 journalid/JCR2024/日期出处。
- 3. domain_scope 打标:批量为 ccf_level≠N/A 行追加 risk_note `domain_scope=中国CS`,cas_quartile 含'区'但无CCF的行追加 `domain_scope=中国语境`,纯 SCI 国际刊 `domain_scope=通用`。
- 4. 抽方法论:新建 databases/db01-venues-templates/references.md,落 reference_style→cls/bst 映射表 + subject_area 受控词归一表(261→约30)。README §reference_style 与 ai_policy 已有内容指过去。
- 5. venue_signal.py 改造:_load_card_from_csv 改为按规整后的 `issn=`/`oa_id=` 子串精确匹配;新增一个 batch 模式可对全库逐行实时复查(非只单候选),输出 IF/被引/h_index 在线值 vs 本地快照的 diff 清单。
- 6. check_freshness.py 对接:确认它读 last_checked_date 产超期清单(README 已述);把超期行喂给步骤5的 batch 复查。
- 7. 改 4 个消费技能 SKILL 的 db01 引用措辞(见 affected_skills),指向新 references.md 方法论表 + 声明薄缓存语义。
- 8. README 诚实改写:卖点从'权威IF库'改为'venue锚点+实时复查管线+reference_style/ai_policy方法论';明示会议偏CS、IF分两类口径、cas/ccf是偏科字段。
- 9. 校验:PYTHONUTF8=1 python .github/scripts/check_databases.py 确认列数=19、物理行数==逻辑行数;venue_signal.py --selftest 通过。

## ⚠ 需要你拍板的决策点
- ISSN/oa_id 锚点存哪:塞进 risk_note 子串(零 schema 改动、不破 19 列 CI,但 risk_note 越发臃肿)vs 占用 indexing 列固定前缀(语义更干净但要改采集规范)。我倾向 risk_note 子串沿用 ai_policy= 同模式——是否同意?
- 178 行已有真 JCR/LetPub IF 要不要保留:这些是付费源人工核出的高价值数据,OpenAlex 实时查不到。我主张保留为权威快照、不被在线代理值覆盖(即'信在线'规则对 JCR/CAS 字段例外)。请确认这条例外。
- 实时复查是否强制联网:venue-matching 投前是否硬性要求跑 venue_signal 联网复查(无网则明确标'离线快照')?还是允许纯本地快照出结论?这决定降级策略的严格度。
- subject_area 261→受控词归一表的粒度:归到约30个大方向(好筛但粗)还是保留二级细分(准但碎)?影响 venue-matching 按方向筛的召回。
- domain_scope 取值集合:用'中国CS/中国语境/通用'三档,还是更细(分 CCF/北大核心/CSSCI/CSCD)?三档够过滤但损失信息。
- README 卖点缩水的诚实度:是否明确写出'46会议全是CS、IF分真JCR(178)与OpenAlex代理(122)两类、cas/ccf仅中国语境适用'这些会显得库不够全的事实?

## 工作量与风险
- 工作量：中。锚点规整(步骤1)是最重的一次性脚本活+57行缺ISSN手工补,约半天;domain_scope/口径批量标注脚本可做,约2小时;venue_signal.py 加 batch 模式约2小时;4个技能SKILL措辞微调+README重写约2小时;references.md 方法论表抽取约2小时。风险点集中在步骤1改CSV(R4/R8铁律,改前必验物理行数==逻辑行数)。
- 风险：①改 venues.csv 触发 README R4/R8 血泪铁律:含英文逗号字段必须加引号、禁用 csv 模块全量重写压平多行(当前无多行字段但 risk_note 含大量逗号),锚点回写脚本若处理不当会拆列——必须用 csv 标准库读写+改前后验物理行数==逻辑行数。②卖点缩水:README 从'308条IF库'诚实改为'锚点+实时管线'后,对外观感上数据量价值下降,需用户接受这种诚实。③联网依赖加重:representative_papers/IF 转实时后,无网时 venue-matching 输出质量下降,降级快照需明示时效。④178行真JCR值若误被'信在线'规则覆盖成 OpenAlex 代理值是数据降级事故,必须设字段级例外。⑤4个技能改引用措辞若不同步,会出现 typesetting/citation 各读各的 reference_style 口径不一(light-consistency 关注点)。⑥OpenAlex 2026 起需免费 key,batch 全库复查 308 行的限流/退避口径必须遵 m01 references,不可硬刷。
