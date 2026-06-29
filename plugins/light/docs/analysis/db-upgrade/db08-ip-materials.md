# db08-ip-materials 升级规划

> 分析日期 2026-06-13 ｜ 基于真实 schema + 依赖技能消费方式 ｜ 只读规划,未动库
> 原始库标识：db08-ip-materials（软著专利竞赛材料骨架：material_cards.md 模板+canonical索引、material_extended_cards.md 8张实体卡、resources_real.md 检索入口/软著/专利/竞赛真实资源、budget_template.md 预算模板、case_skeletons.md 高分结构骨架、README.md）

## 目标形态
db08 与 db01 本质不同：它不是"按实体存数值事实"的事实表，而是"存写作方法论+行政程序+结构骨架"的方法论库，A-通用占比天然极高（你给的62%偏低，按真实卡看更高）。升级后形态：material_cards/extended_cards 的 10 字段全部确认为 A-通用方法论资产，留本地精养，不动 schema 主体；真正的 B 类只集中在 resources_real.md（检索平台API现状、官方URL、加急费用、页数口径）与 case_skeletons 的评分权重，这些**绝大多数没有可查 API**，因此"转实时"在 db08 = 转"官方源指针 + last_checked + 提交前强制核查"的指针模型，而非 db01/venue_signal.py 那种"查 API 缓存数值"模型。唯一真有 API 的专利检索已由 light-ip-application/patent_search.py 实时化，resources_real §1 应降级为指针、把端点真相源唯一指向 references.md。偏科极薄（~3%，仅 budget §3 材料化学示例），用轻量 illustrative_only 标记隔离即可，不必引入重型 domain_scope 字段。

## 逐字段处置
| 字段/内容块 | 类别 | 动作 |
|---|---|---|
| material_card 10字段(material_type/required_sections/official_requirement/writing_style/common_mistakes/checklist/sample_structure/legal_risk/reuse_scope/final_review_needed) | A-通用 | 留本地精养。这是跨学科行政程序+写作方法论(软著登记/专利撰写/申报书),不偏科、不易变,是库的核心资产。schema 主体不动。 |
| resources_real §1 专利检索表的 API 列(Google Patents无API/EPO OPS OAuth/PatentsView需key/Lens token/CNIPA无API) | B-事实 | 转指针。这些端点/认证/限流的单一真相源应是 light-ip-application/references.md(已 curl 实测),resources_real §1 删去重复的 API 细节列,改为'平台名+官方URL+一句话适用+指针指向 references.md',消除双源维护。 |
| resources_real §1/§2/§4 的官方入口 URL + curl HTTP 状态/探测日期 | B-事实 | 转薄指针。保留 URL 作 source_pointer,把'探测日期 2026-06-06'结构化为 last_checked + verify_method,冲突时默认信在线、提交前重探。 |
| 软著源代码'前后各30页/每页≥50行/页眉含软件名版本'(resources_real §2 + extended_cards 软著源码卡 + SKILL.md line16) | A-偏科→实为A-通用行政规则 | 留本地(全学科任何软件通用),但归类为'行政规则 volatility:low',加 last_checked + source_pointer 指向 CPCC 当期《登记指南》。当前在 3 处重复(SKILL/resources_real/extended_cards),收敛为单一真相源(建议 resources_real §2),另两处指针引用。 |
| 软著/专利加急费用、官费、审查周期(约30工作日) | B-状态 | 保持'待核查不缓存数值'(当前已是),补 source_pointer 指向 CPCC/CNIPA 收费公告。不存快照数值,合规更稳。 |
| resources_real §4 竞赛官方URL + 报名/平台入口(大创全国平台逐年变) | B-事实 | 官方主站URL留作指针+last_checked;'当年报名入口'标 volatility:high + 待核查,不缓存逐年链接。 |
| case_skeletons 各赛事评分权重/分值百分比 | B-状态 | 保持'【权重待核查】+不臆造分值'(当前正确),补 source_pointer 指向当届《评审规则》压缩包。维度名称(创新性/可行性等公开口径)是 A-通用,留本地。 |
| budget_template §2 科研经费科目体系(材料费/测试化验费/差旅/劳务...) | A-通用 | 抽为方法论层,标 universal。科目口径是财政/基金通行分类,跨学科通用,留本地。 |
| budget_template §3 已填示例(材料化学:催化剂/XRD/SEM/XPS送测,示意金额) | A-偏科 | 打 illustrative_only + domain_example:材料化学 标记隔离,显著声明'演示填法、非领域锁定、金额非真实封顶额',让非材料方向用户知道照搬科目而非照搬领域。 |
| budget §1比例上限/封顶额(劳务费占比/总额) | B-状态 | 保持'待核查本校口径',加 source_pointer 指向本校《经费管理办法》,不缓存比例数值。 |
| 数模硬规则(MCM 25页上限/99小时/CUMCM摘要权重/AI说明) | A-偏科(竞赛型,非研究方向) | 留本地。已核到官方 contest instructions,带 last_checked,是稳定硬规则非易变事实。注意这是'竞赛类型差异'非'研究领域偏科',属库的合法核心轴,不需 domain_scope 过滤。 |

## B 类转实时设计
分两条，关键是承认 db08 的 B 类大多无 API。(1) 专利检索(唯一真有 API 的 B 类)：复用已实现的 light-ip-application/scripts/patent_search.py——它已封装 OpenAlex /works(NPL在先技术,2026需免费key,per_page≤200) 并为 The Lens(POST api.lens.org/patent/search, Bearer token)、EPO OPS(ops.epo.org/3.2/rest-services, OAuth2 client_credentials, CQL, X-Throttling-Control 红绿灯节流)、USPTO ODP(data.uspto.gov/api/v1, X-Api-Key, 旧 api.patentsview.org 已301停用)构造请求体。端点真相源唯一锁定在 references.md，resources_real §1 仅留指针。薄缓存：在 resources_real 每个 API 行存 {api_status快照, last_checked, verify_method(curl状态/WebSearch), source_pointer(开发者门户URL), realtime_queryable:yes-via-patent_search.py}，不缓存检索结果本身(结果实时查)。冲突信在线：references.md 端点与本地快照冲突时信 references.md 当次实测。(2) 无 API 的 B 类(加急费用/评分权重/页数口径/竞赛报名链接)：不建数值缓存(这是与 db01 venue_signal.py 的根本差异)，只存 {snapshot:'待核查'或最近一次口径文字, last_checked, source_pointer(官方公告URL), volatility}。无网降级：写软著/专利/申报材料常在受限网环境，实时核查不可强制——降级策略=用本地快照口径(如'60页/50行''约30工作日')+在产出顶部打显著【提交前以XX官方当期公告核查】警示，patent_search.py 联网失败时按其既有 status='unavailable'+reason 优雅降级、不编数。

## 偏科隔离设计
偏科极薄(~3%)，不引入重型 domain_scope schema 字段(会给 95%+ 纯方法论卡加无意义噪声)。改用两级轻量标记：(1) budget_template §3 材料化学示例加行内标记 illustrative_only:true + domain_example:材料化学 + 一句声明，用户按方向过滤时只需忽略示例数字、照搬科目体系(科目是 universal)。(2) 区分两种'偏科'：研究领域偏科(仅预算示例,需隔离)vs 竞赛类型差异(数模/互联网+/挑战杯/大创——这是库的合法核心轴,是 material_type 维度,不是偏科,不过滤)。过滤入口：material_cards canonical 索引表已按 material_type 组织，用户天然按'我要做软著/专利/哪个赛事'选卡，无需额外方向过滤层。若未来补入领域特化示例(如医学专利实施例),再统一加 domain_scope 字段并回填,现在不做。

## A-通用判断 → 方法论层
db08 本身就是方法论库，A-通用判断已沉淀在 material_cards 的 10 字段里，无需外迁——升级动作是"确认+提纯"而非"抽取"。需提纯的是把嵌入卡内的易变事实指针化后，让卡只剩纯方法论：权利要求'独立项求最大稳妥范围/从属项逐层回退/方法+装置+介质组合布局'、说明书'充分公开到本领域技术人员可实现'、软著'源代码连续真实可对应功能'、申报书'创新点与现有方案差异化可量化、技术路线拆可验证小步'、TAM-SAM-SOM'自下而上+假设登记表+交叉校验'、预算'每项单价×数量与研究活动匹配'——这些对任意学科成立，确认为 db08 的方法论资产留本地精养。组织方式不变(material_card schema + canonical 索引)，仅在卡内补 source_pointer 字段把官方口径外链化。

## schema 改动
不动 CONVENTIONS §3 统一字段(那是 venue/method/dataset/project schema，db08 的 material_card 是独立 schema 不在其中)。material_card schema 增 2 个可选字段：source_pointer(官方口径外链，用于把卡内引用的行政口径外链化)、last_checked(卡内引用的官方口径核查日)。不加 domain_scope(偏科太薄)。resources_real.md 引入结构化资源条目字段：{resource_name, official_url, api_status, last_checked, verify_method, source_pointer, volatility, realtime_queryable}。budget_template §3 加行内标记 illustrative_only + domain_example。

## 影响的技能及改法
- **light-ip-application**：(1) API 真相源唯一化：SKILL.md §查新检索表 + references.md 已是端点真相源，确认 resources_real §1 降级为指针后，SKILL/db08 不再各存一份端点。(2) 软著'60页/50行'规则当前在 SKILL.md line16、references.md、db08 三处重复——收敛为 db08 resources_real §2 单一真相源 + last_checked，SKILL 指针引用。(3) patent_search.py 已实时化在先技术检索，确认 db08 resources_real §1 标 realtime_queryable 指向它，不重复维护端点。
- **light-competition**：(1) 消费 db08 budget_template/case_skeletons/material_cards 不变；确认评分权重'待核查不缓存数值'政策与 case_skeletons 一致。(2) market_charts.py 的 TAM/SAM/SOM 已与 budget §4 财务预测共用同一套数(a07 一致性)，确认薄指针不破坏这一联动。(3) budget §3 材料化学示例加 illustrative_only 后，light-competition 引用时需说明'示例仅演示填法'，避免跨学科用户照搬金额。

## 迁移步骤
- 1. resources_real.md §1：删除专利检索表的'API'细节列，改为'平台/官方URL/适用/last_checked/verify_method/realtime_queryable'，在表后加一句'API端点/认证/限流以 light-ip-application/references.md 为单一真相源；程序化检索走 patent_search.py'。
- 2. resources_real.md §2：把软著'前后30页/每页≥50行/页眉含软件名版本'标 rule_type:行政规则 volatility:low + last_checked:2026-06-06 + source_pointer:CPCC当期《软件著作权登记申请指南》；加急费用/30工作日保持【待核查】并补 source_pointer。
- 3. 收敛 60页规则重复：确认 resources_real §2 为单一真相源，material_extended_cards 软著源码卡 official_requirement 与 light-ip-application SKILL.md line16 改为指针引用(不再各写一遍页数)。
- 4. resources_real.md §4：每赛事拆为 official_url(指针)+last_checked+'当年报名入口 volatility:high 待核查'，大创全国平台链接明确不缓存逐年值。
- 5. budget_template.md §3：示例表头加 illustrative_only:true + domain_example:材料化学，强化现有'演示性示例'声明为结构化标记；§2 科目体系标 universal。
- 6. case_skeletons.md：各赛事【权重待核查】处补 source_pointer 指向当届《评审规则》压缩包，确认不存任何分值快照。
- 7. material_cards.md 卡片模板 + material_extended_cards.md：在 10 字段后增可选字段 source_pointer(官方口径外链)、last_checked(卡内引用的官方口径如60页规则的核查日)；不加 domain_scope(偏科太薄)。
- 8. README.md 诚实同步：说明卡数不缩水(均方法论资产)，但 resources_real 的 API/费用/权重明确为'官方源指针+待核查'非数值缓存；声明 db08 与 db01 模型差异(无数值薄缓存,因 B 类多无 API)；指明专利端点真相源在 references.md。

## ⚠ 需要你拍板的决策点
- 【核心】db08 的 B 类(加急费/评分权重/页数口径/竞赛链接)绝大多数无可查 API，'转实时'实际是'官方源指针+提交前强制核查'的指针模型，而非 db01/venue_signal.py 式'查API缓存数值'模型。是否确认采用指针模型、不为 db08 建数值薄缓存？(这决定整个升级的形态)
- 软著'60页/50行/页眉'规则归 A-通用方法论(留本地+last_checked)还是 B-易变事实(指针化)？建议归 A(全学科通用、变动极慢的行政规则),但需你拍板，因它是 A/B 边界模糊的典型。
- 专利检索 API 真相源唯一化：是否接受删除 resources_real §1 的重复端点信息、只留指针指向 references.md+patent_search.py？(消除双源但 resources_real 阅读时需跳转)
- 是否引入统一 domain_scope 字段进 material_card schema？建议不引入(偏科仅~3%,只 budget 材料化学示例),改用轻量 illustrative_only 标记；若你预期未来大量补领域特化示例则现在就加。
- 评分权重/加急费用：保持当前'待核查+不缓存数值'(合规最稳)，还是要存'最近一次快照值+last_checked'供无网时参考？建议保持不缓存。
- 无网降级是否可接受'用本地快照口径+显著【提交前核查】警示'？(软著/专利写作常在受限网环境,实时核查不能强制)

## 工作量与风险
- 工作量：轻-中。db08 主体(material_cards 方法论)几乎不动，工作量集中在 resources_real.md 重构(§1 降级指针、§2/§4 结构化 last_checked)与三处 60 页规则去重，约 1-2 个文件编辑会话。风险低因不涉及代码逻辑改动、patent_search.py 已实时化无需新写。
- 风险：(1) README 诚实同步后需向用户说明'卖点'其实不缩水(db08 是方法论库非事实表)，避免误以为降级——这是表述风险非实质损失。(2) resources_real §1 删端点改指针后，单独读 resources_real 的用户需跳转 references.md，牺牲单文件自包含性换取去重；若用户偏好 resources_real 自包含则保留摘要+'详见references.md'两全。(3) 60 页规则去重若收敛点选错(改了 resources_real 但 SKILL/extended_cards 仍硬写)会再次分叉，迁移步骤3必须三处同步。(4) 指针模型依赖'提交前核查'纪律，无网环境下用户可能直接采信本地快照口径——靠显著警示+合规底线(a10)兜底，但无法技术强制。(5) 不引入 domain_scope 的代价：未来若补大量领域特化实施例需回头加字段并回填,现在省的成本届时要还。
