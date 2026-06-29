# db07-figures 升级规划

> 分析日期 2026-06-13 ｜ 基于真实 schema + 依赖技能消费方式 ｜ 只读规划,未动库
> 原始库标识：db07-figures(科研图表案例/审美/组图逻辑库)

## 目标形态
升级后 db07 以"制图方法论库"为主体:12 字段 schema 几乎全是 A-通用craft(purpose/data_required/layout/color_scheme/annotation_style/caption_style/replication_notes/where_to_place_in_paper),本地精养不动,这是核心资产。paper_source 拆解:稳定的 DOI/官网链接留本地,易变的被引数从卡内剥离、转实时查薄缓存。偏科图型(volcano/Manhattan/KM/CONSORT/Bland-Altman/PRISMA/forest/calibration)继续用现有 research_field 字段做隔离锚点(它本就是正面样板),无需新建标签体系。self_produced g1-g9 指向项目路径,属 C-项目事实,全本地。整库口径:卡是"跨项目可复用图表模式",栏宽尺寸仍由 figure_export.py::JOURNAL_SPECS 独占(db07 不碰),被引数等 venue-style 易变事实改实时。README 卖点从"X 张实测卡+被引数字"诚实改为"N 张方法论卡(craft 不过期)+ 工具被引实时查"。

## 逐字段处置
| 字段/内容块 | 类别 | 动作 |
|---|---|---|
| figure_type | A-偏科 | 通用图型(柱/箱/雷达/热力等)留本地;领域专属图型(volcano/Manhattan/KM/CONSORT/Bland-Altman/PRISMA/forest/calibration)随该卡 research_field 做隔离,不删 |
| paper_source | B-事实 | 拆:DOI 与官网 URL=稳定事实留本地;内嵌的被引数(如 limma/qqman/UMAP JOSS 卡里若出现)剥离转实时;self_produced 卡的项目路径指针留本地 |
| research_field | A-偏科 | 留并规范化为隔离过滤键(统一取值表),作为偏科隔离的唯一锚点,不再新增 domain_scope |
| purpose | A-通用 | 留本地精养,抽为方法论层(图↔claim 映射) |
| data_required | A-通用 | 留本地 |
| layout | A-偏科 | 通用布局通识(轴序/GridSpec)留;偏科图型 layout 带领域前提,随卡隔离 |
| color_scheme | A-通用 | 留,抽为方法论层(色盲友好/全文统一/黑白冗余铁律) |
| annotation_style | A-通用 | 留本地 |
| caption_style | A-通用 | 留本地 |
| possible_code_tool | A-通用 | 留本地(工具选型,基本稳定,非 B 类) |
| replication_notes | A-通用 | 留本地精养,抽为方法论层精华(气泡面积∝数值/y轴不截断/雷达轴序/相关≠一致性等诚实性铁律) |
| where_to_place_in_paper | A-通用 | 留本地 |
| resources_real.md 第一部分资源表·被引数(Matplotlib 39283/ggplot2 20555/seaborn 78/ColorBrewer 1114/Graphviz 1105/Altair 238) | B-状态 | 转实时查;本地表内数值替换为薄缓存(快照值+last_checked+DOI 指针),冲突信在线 |
| resources_real.md/spectrum_fill_cards.md·gallery HTTP 200 核验表 | C-状态 | 转实时核验;本地只留 last_checked,不把'200'当永久事实 |
| self_produced_cards.md·paper_source(projects/.../g1-g9 路径) | C-状态 | 留本地(项目内可复跑产出,来源最硬,禁转实时) |

## B 类转实时设计
仅一类值真正需要转实时:工具论文被引数(目前只出现在 resources_real.md 第一部分 markdown 资源表,作为可信度背书,无任何技能操作性消费)。API:复用 literature-search references 已实测的 OpenAlex Works 端点 GET https://api.openalex.org/works/doi:{DOI}?select=cited_by_count,publication_year&mailto=...(venue_signal.py 已用同一 base+礼貌池,可直接抽公共 fetch)。薄缓存存什么:把表格列从裸数字改为三元组 cited_by_count_snapshot + last_checked(YYYY-MM-DD) + source_doi(指针);不存衍生解读。冲突信谁:按重构哲学默认信在线,本地快照仅作离线兜底与变化提示。无网降级:读本地快照值并显式标注'(快照 last_checked=…,在线未核)',绝不崩、不编新数;OpenAlex 2026 需免费 key,口径一行指针指向 m01 references『OpenAlex 接入真相源』,db07 不复写数字。注意:被引数无操作性消费方,故是否值得为它引入联网依赖本身是决策点(见 decisions_needed)——保守方案是直接降级为定性表述'被引极高(OpenAlex,见 DOI)'而不联网。栏宽数字不在本计划:它已由 figure_export.py::JOURNAL_SPECS 独占真相源,db07 不存。

## 偏科隔离设计
复用现有 research_field 字段,不新建 domain_scope(该库已全卡带 research_field,是仓库内正面样板,新增标签反而割裂)。做三件事:(1) 建 research_field 受控取值表(通用/系统综述/临床试验/生物医学-生存分析/组学-差异表达/遗传学-GWAS/医学测量/机器学习-临床预测/单细胞-表征 等),写入 db07 README,避免自由文本导致过滤失效;(2) 约定 research_field='通用' 即通用层,其余值即偏科层,planning 技能按用户项目方向(从 db09 项目卡 domain 读)优先匹配'通用'卡,仅当 claim 命中领域专属图型(如 GWAS→Manhattan)时才取对应偏科卡;(3) figure_advanced_cards.md 的 9 张里 PRISMA/CONSORT/KM/forest/Bland-Altman/volcano/Manhattan/calibration 为偏科,UMAP 跨域偏通用,逐卡核对 research_field 取值落到受控表。用户过滤方式:planning 读项目方向→只在'通用'+'命中领域'两个集合里选卡,非该方向偏科卡默认不进候选。

## A-通用判断 → 方法论层
A-通用判断在 db07 内已天然是方法论(purpose/replication_notes/color_scheme/layout 四字段),无需外迁库,但要显式沉淀为可跨学科引用的资产:在 db07 README 增设『制图方法论铁律』节,把散落在各卡 replication_notes 里对任意学科都成立的规则去重上提为编号清单(R1 y轴不截断;R2 气泡面积∝数值非半径;R3 雷达图统一方向+轴数≤6;R4 相关≠一致性需 Bland-Altman;R5 小样本叠原始散点;R6 跨热力图固定 vmin/vmax;R7 误差棒注明 SD/SEM/CI+n;R8 色盲友好+黑白线型冗余;R9 多 panel 反冗余-每 panel 唯一科学问题)。卡内 replication_notes 改为引用编号(如'遵 R2/R3')+ 图型特异补充,消除重复、让方法论成为单一真相源。这层与 light-figure-drawing/references 的 figure_integrity.md 对齐(后者是执行端 lint 规则),db07 README 节加一行指针指向它,不复写。

## schema 改动
CONVENTIONS §3 不动(db07 12 字段不在 §3 统一字段表内,§3 只管 venue/method/dataset/project 四类卡)。db07 README backtick schema 行与 check_databases.py SCHEMAS['db07-figures'] 保持 12 字段不变——关键:CI 只校验这 12 个必填字段非空、不拒绝额外 per-card 键。因此薄缓存字段(cited_by_count_snapshot/last_checked/source_doi)只作为 resources_real.md 第一部分 markdown 表的列存在(那是表格不是 schema'd YAML,完全不进 CI 校验),零 schema 改动。research_field 受控取值表只写进 README 文字(非 backtick 行),不触发 schema 比对。结论:本次升级可做到 0 行 check_databases.py 改动、0 处 backtick schema 行改动。

## 影响的技能及改法
- **light-figure-planning**：两处:① 把现有'先查 db07 canonical'选型顺序补一步——先读项目方向(db09 项目卡)按 research_field 受控表过滤偏科卡,再映射 claim→figure_type,避免给非该方向用户推 volcano/GWAS 卡;② 规划卡 color_scheme/replication_notes 字段改为引用 db07 README 方法论铁律编号(R1-R9),不再各卡复述。引用机制(source_card 指针)不变。
- **light-figure-drawing**：基本不动:它消费的是 purpose/layout/data_required/color_scheme/annotation_style/replication_notes(全 A 类方法论)+ JOURNAL_SPECS 栏宽(本就独立于 db07)。仅需:执行时读到 paper_source 的被引快照,知道那是薄缓存不是权威值(一行说明);replication_notes 引用编号后,执行端按编号查 README 铁律节。
- **light-literature-search(m01)**：被动:成为 db07 被引实时查的 API 口径来源。db07 README 实时节加一行指针指向其 references『OpenAlex 接入真相源』,无需改 m01 本身。
- **light-venue-matching**：参照而非修改:其 venue_signal.py 的 OpenAlex fetch+礼貌池+优雅降级模式是 db07 被引薄缓存脚本(若做)的现成模板,可抽公共 fetch 复用。

## 迁移步骤
- 1. db07 README.md 新增『制图方法论铁律 R1-R9』节,从四个 *_cards.md 的 replication_notes 去重上提通用规则,并加一行指针指向 light-figure-drawing/references/figure_integrity.md。
- 2. db07 README.md 新增『research_field 受控取值表』节,列出通用+各偏科取值;逐卡核对 figure_advanced_cards.md 9 卡的 research_field 落到受控表(volcano/Manhattan/KM/CONSORT/Bland-Altman/PRISMA/forest/calibration 标偏科)。
- 3. 四个 *_cards.md 的 replication_notes:把命中铁律的句子改为'遵 R#'引用 + 图型特异补充(逐文件编辑,注意 Edit<13000 字符分批)。
- 4. resources_real.md 第一部分资源表:被引列从裸数字改为'快照值 | last_checked | DOI 指针'三元(若用户拍板转实时);否则降级为'被引极高(OpenAlex,见 DOI)'定性表述。
- 5. (条件:决策点1选转实时) 新建 db07-figures/scripts/cite_refresh.py,抽 venue_signal.py 的 OpenAlex fetch+礼貌池+降级模式,按 DOI 查 cited_by_count 回写表格快照与 last_checked;OpenAlex key 口径指针指向 m01。
- 6. README『真实资源文件』节与顶部卖点:把'X 张实测卡+被引数字'诚实改为'方法论铁律 R1-R9 + N 张模式卡 + 工具被引实时/快照',同步缩水后的卡数表述。
- 7. light-figure-planning SKILL.md『db07 查找纪律』节补'按 research_field 受控表过滤偏科卡'一步;color_scheme/replication_notes 规划改引用 R# 编号。
- 8. 跑 PYTHONUTF8=1 python .github/scripts/check_databases.py 确认全绿(预期零 schema 报错,因未动 backtick 行与 SCHEMAS)。

## ⚠ 需要你拍板的决策点
- 被引数无任何技能操作性消费(只是资源表里的可信度背书)——是花成本转实时薄缓存(加联网依赖+维护脚本),还是直接降级为定性'被引极高(OpenAlex,见DOI)'省掉联网?(我倾向后者:零依赖、零维护、不损信息价值)
- 偏科隔离用现有 research_field 字段(我推荐,已是正面样板)还是另起 domain_scope?后者要改 schema 且与 research_field 语义重叠。
- replication_notes 上提为 R1-R9 编号后,各卡改'遵 R#'引用——这会让单卡可读性略降(需跳查 README),换来去重与单一真相源,接受吗?
- resources_real.md 第一部分的资源清单表(被引/HTTP状态)不在 12 字段 schema 内、CI 不校验——是否把这张表整体定性为'背书材料'降低维护优先级,把精力集中在 12 字段方法论卡?
- README 卖点诚实缩水:从强调'实测被引数字/HTTP200 核验'改为强调'craft 方法论不过期'——这个定位转向要不要这一轮就落地到 README 顶部?

## 工作量与风险
- 工作量：中(偏轻)。核心是文档重组(README 加两节+四文件 replication_notes 改引用)+ planning SKILL 微调,零 schema/零 CI 改动。若决策点1选'降级定性'则无需写脚本,工作量降为轻;若选'转实时薄缓存'需新增 cite_refresh.py(可抄 venue_signal.py),增半天且引入联网维护。最大耗时在逐卡核对 research_field 受控表与 replication_notes 编号化(需细致,Edit 分批)。
- 风险：主要风险:(1) 被引数若转实时,引入对 OpenAlex(2026 需 key)的联网依赖,而该数值无人操作性消费,投入产出比低——降级方案可规避。(2) replication_notes 上提为编号后,若 README 铁律节与残留卡内文字不同步,会产生新的双源不一致(需 a07 consistency 兜底)。(3) README 卖点缩水(去掉精确被引数字、卡数表述调整)是诚实的代价,用户需接受卖点弱化。(4) light-figure-planning 增加'按 research_field 过滤'一步,若项目卡 domain 字段缺失会退化为不过滤(需降级逻辑:缺方向时全集候选)。(5) 迁移步骤 3 涉及四文件多卡 Edit,有破坏 YAML 缩进/冒号转义风险(README 已警示'YAML 值含英文冒号须加引号'),改完必跑 check_databases.py。整体不破坏现有 source_card 引用契约,figure-drawing 几乎零改动,迁移可控。
