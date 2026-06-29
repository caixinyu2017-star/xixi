# db05-frontend-styles 升级规划

> 分析日期 2026-06-13 ｜ 基于真实 schema + 依赖技能消费方式 ｜ 只读规划,未动库
> 原始库标识：db05-frontend-styles (Light 前端/可视化设计规范与 token 库)

## 目标形态
升级后 db05 是一个"视觉范式 + token SSOT"库:18 张设计卡(genre 4 / 官方设计系统 8 / 科研场景 6)保留 9 个学科中立的范式字段(style_tag/layout_type/color_palette 逻辑/font_style/component_pattern/interaction_pattern/animation_type/project_type/suitable_project_scene),这些是 A-通用方法论的实例化锚点,本地精养。design_tokens.template.json 作为 DTCG 视觉 SSOT 模板不动(它是模板/A 类,不是 B 事实)。resources_real.md Part1 的 26 条工具的"是什么/适用场景"范式描述留库;但其 license/version/定价/链接这些 B 事实从"卡里写死"降级为薄缓存(快照值 + last_checked + source_pointer),由新增 style_signal.py 对 npm 系工具实时查 registry.npmjs.org、对画廊/SaaS 做 HTTP 存活探测,冲突默认信在线。agri-tech/medical 等带研究方向前提的偏科卡打 domain_scope 标签隔离,通用层用户可过滤。glass/neumorphism 的可访问性判断这类跨学科方法论上抽到 a05 reference,db05 卡只留范式 + 指针。

## 逐字段处置
| 字段/内容块 | 类别 | 动作 |
|---|---|---|
| project_type (卡主键,CI 唯一性键) | A-通用 | 留本地。它是卡身份与去重键,check_databases.py 按它判唯一,不动。 |
| style_tag | A-通用 | 留本地。视觉风格谱系(玻璃拟态/极简/卡片式)学科中立,是范式核心。 |
| layout_type | A-通用 | 留本地精养。版式逻辑(栅格/分栏/hero 分段)是跨学科方法论实例。 |
| color_palette | A-通用(含偏科信号) | 留本地。色板逻辑通用;但 agri-tech 绿色系/medical 蓝白是偏科信号,给所在卡打 domain_scope,不改字段本身。具体 hex 与 design_tokens.template.json 对齐。 |
| font_style / component_pattern / interaction_pattern / animation_type | A-通用 | 留本地。字体层次/组件模式/交互/动效都是学科中立范式。 |
| screenshot_reference | B-事实(链接易失效) | 转薄缓存。值留本地但加 last_checked,纳入 style_signal.py 的 HTTP 存活探测;沿用 check_freshness.py warn-only 月度复查,失效标 stale 不阻断。 |
| implementation_notes(方法论部分:WCAG 对比/性能/glass 可读性风险/neumorphism a11y 硬伤) | A-通用 | 抽方法论层。把可访问性/性能判断上抽到 a05 references/visual-a11y-rules.md,db05 卡内只留一句范式提示 + 指针,避免方法论散落在 18 张卡里各写一遍。 |
| implementation_notes(事实部分:具名库 license/版本,如 'ECharts Apache-2.0'/'Magic UI MIT'/'MUI X 收费') | B-事实 | 转实时查。从散文里剥离为结构化薄缓存条目(库名→license/version/source_pointer),由 style_signal.py 查;卡内散文不再断言 license,改为'见 tool_signal 薄缓存/实时核验'。 |
| suitable_project_scene | A-通用(含偏科信号) | 留本地;若为 domain_scope 候选载体(决策点 1B),把 'domain_scope=agri-tech' 等以子串塞此字段或 implementation_notes catch-all。 |
| resources_real.md Part1『许可』列(26 行) | B-事实 | 转实时/薄缓存。npm 系(shadcn/radix/mui/antd/echarts/d3/recharts/tremor/tailwind 等)走 registry.npmjs.org 的 .license 实时查;非 npm(画廊/Figma/Coolors)只留 source_pointer 指向官方 LICENSE,标 待核查。 |
| resources_real.md Part1『链接』列 | B-事实 | 转薄缓存。值留 + last_checked + HTTP 存活探测(复用 venue_signal 式 GET),失效 warn-only。 |
| Part1 Pro/定价层(Aceternity Pro/Magic UI Pro/MUI X/Coolors Pro) | B-事实(无 API) | 留薄缓存 + 强制 待核查 标。定价无开放 API,style_signal.py 不能查值,只存 source_pointer 指向官方 pricing/licence 页 + last_checked,引用时提示人工核。 |
| design_tokens.template.json(color/typography/dimension/radius/shadow) | A-通用(模板) | 留本地不动。它是 DTCG 视觉 SSOT 种子模板,属方法论/模板层不是 B 事实,真实项目副本落 db09;a07 维护。不转实时。 |
| design_cards.md(0 实体卡,仅模板+canonical 索引) | A-通用(模板) | 留本地不动,仅更新索引指向重构后的薄缓存位置。 |

## B 类转实时设计
分两条路,都复用 venue_signal.py 的成熟模式(urllib GET + 逐项 status=unavailable 优雅降级 + mock fetcher selftest)。
(1) npm 系工具(license + version):查 https://registry.npmjs.org/<pkg> —— 该 JSON 顶层有 .license(SPDX)、.dist-tags.latest、.versions[latest].license。此端点已被 design-systems-map.md 用 curl 实测 HTTP 200,可靠。可查:shadcn、@radix-ui/react-*、@mui/material、antd、@tremor/react、echarts、d3、recharts、tailwindcss,以及设计系统的 @fluentui/react-components、@carbon/react、@shopify/polaris、@primer/react、@uswds/uswds、govuk-frontend、@atlaskit/*。
(2) 画廊/SaaS/Figma/定价层(无 license API):只做 HTTP 存活探测(GET 取状态码,沿用 venue_signal http_fetch 写法)+ 存 source_pointer 指向官方 LICENSE/pricing 页;定价值不抓,标 待核查。
薄缓存存什么:每条 = {tool, npm_pkg(可空), cached_license, cached_version, source_pointer(registry URL 或 LICENSE 页), last_checked, flag(ok/待核查/stale)}。建议落 tool_signal.json(机器可核)或原地表格加列(决策点 2)。
冲突信谁:按用户已定规则——在线查到且与缓存不一致时,信在线,并回写薄缓存 + 刷新 last_checked。
无网降级:查不到/无网时不崩,返回 cached_license + 标 stale + 打印 last_checked + 提示'投产前以官方 LICENSE 为准',绝不编值(与 venue_signal 的 unavailable+reason 一致)。注:本环境 WebFetch 全域被拦,但 urllib/curl 到 registry.npmjs.org 与 OpenAlex 已证可行,脚本走 urllib;Awwwards/Mobbin/定价标 '待核实 API 能力',不编造。

## 偏科隔离设计
偏科占比小(~9%),集中在科研场景卡里带研究方向前提的两类:agri-tech(智慧农业/绿色系)、medical(医疗/蓝白)。设计:引入 domain_scope 取值集 {general, agri-tech, medical, gov, commerce, devtool, mobile};绝大多数 genre 卡(玻璃拟态/极简/杂志编辑)与官方设计系统卡(按商业生态而非研究方向)标 general;只给真·研究方向偏科的 agri-tech 平台卡、medical 卡打专门标。过滤方式:a05 在'先定设计方向'步按项目学科读 domain_scope,非该方向用户默认只看 general + 本方向卡,跳过他方向偏科卡(如做农业项目不被 medical 蓝白卡干扰)。通用层(general)与偏科层物理上仍在同文件,靠 domain_scope 子串/字段逻辑隔离,不拆库。载体二选一见决策点 1。

## A-通用判断 → 方法论层
把跨学科成立的视觉判断从 18 张卡的 implementation_notes 里上抽,集中到 a05(light-frontend-design)新建 references/visual-a11y-rules.md:收录(a)WCAG 2.1 AA 阈值(正文 4.5:1/大字 3:1/UI 组件 3:1,已散见 SKILL)、(b)玻璃拟态可读性风险(模糊层下正文须足够对比、避免长段落、blur 吃 GPU 移动端控层数)、(c)新拟物 a11y 硬伤(边界靠阴影非对比,低视力/强光不可辨,只配装饰性轻交互)、(d)4/8pt 栅格与字体层次原则、(e)触控目标 iOS≥44/Android≥48。db05 卡内对应位置改成一句范式提示 + 指针'a11y 判据见 a05 visual-a11y-rules.md',方法论一处维护、对任意学科成立。design_tokens.template.json 已是方法论/模板层,保持。

## schema 改动
CONVENTIONS §3 的统一字段表未列 db05 卡 schema(db05 schema 只在 README + check_databases.py SCHEMAS 里),所以 §3 本身不必动。两个候选:(A)新增 domain_scope 为 db05 第 12 个 schema 字段——需同步改 check_databases.py SCHEMAS、README schema 行、三个卡文件(genre/design_system/resources_real),且过校验;CONVENTIONS §3 可顺带登记 db05 schema 以备引用。(B)零 schema 改动,domain_scope 以 'domain_scope=agri-tech' 子串塞 suitable_project_scene/implementation_notes catch-all(仿 db01 ai_policy 进 risk_note 末列的先例)。薄缓存若落 tool_signal.json 是新增数据形态文件,不影响现有 11 字段校验(Part1 是表格非 YAML 卡,本就不走 schema 校验)。新增字段建议:cached_license/cached_version/source_pointer/last_checked/flag(仅在薄缓存条目内,不进卡 schema)。

## 影响的技能及改法
- **light-frontend-design (a05)**：三处改引用:①'沉淀进 db05'与'设计系统登记 db05'保留,但新增一条规则——引用某库 license/版本时不信卡内散文,跑 scripts/style_signal.py 实时查(把 a05 已对 npm 版本做的 curl 习惯推广到 license),与 venue-matching 用 venue_signal 实时查同构;②新建 references/visual-a11y-rules.md 承接从 db05 上抽的可访问性方法论;③'先定设计方向'步按项目学科读 domain_scope 过滤偏科卡。新增'信在线'规则:license/定价冲突默认信官方在线源,无网时用薄缓存快照值并标 stale。
- **light-consistency (a07)**：基本不动。a07 维护 design_tokens.template.json(模板/A 类,不转实时),extract-design-system 流程不变;仅需知晓 agri/medical 色板卡可能带 domain_scope 标,抽取写回 SSOT 时不受影响。
- **check_databases.py / check_freshness.py (CI)**：若 domain_scope 走新增字段(决策 1A),改 check_databases.py SCHEMAS['db05-frontend-styles'] 加第 12 字段 + README schema 行同步;若走 catch-all 子串(决策 1B)则 CI 零改动。freshness 已支持 last_checked_date/核验日期,薄缓存沿用,无需改。

## 迁移步骤
- 1. 在 resources_real.md Part1 26 行中,把『许可』『链接』两列的易变值与范式描述分离:范式(是什么/适用场景)留表;license/version/链接迁入薄缓存载体(决策 2:原地加 last_checked+source_pointer+flag 列,或抽 tool_signal.json)。Pro/定价层一律标 待核查 + source_pointer。
- 2. 新建 Light/databases/db05-frontend-styles/scripts/style_signal.py,照 venue_signal.py 结构:http_fetch(urllib GET)+ 对 npm 系工具查 registry.npmjs.org/<pkg> 取 .license/.dist-tags.latest,对画廊/SaaS 做 HTTP 存活探测,逐条 status=ok/unavailable 优雅降级 + mock fetcher selftest(--selftest 离线过)。
- 3. 在三个卡文件的 implementation_notes 里,把具名库 license 断言改为指向薄缓存/实时查;把 WCAG/glass/neumorphism 可访问性判断替换为指针,指向 a05 新建 references/visual-a11y-rules.md。
- 4. 新建 Light/skills/light-frontend-design/references/visual-a11y-rules.md,收纳从 db05 上抽的方法论(WCAG 阈值/glass 可读性/neumorphism a11y 硬伤/4-8pt 栅格/触控目标),并在 a05 SKILL.md 相应处加指针。
- 5. 给 agri-tech 平台卡(resources_real Part2『智慧农业监测平台』)、medical 类卡打 domain_scope(载体见决策 1);其余卡标 general。a05 SKILL.md『先定设计方向』步加按 domain_scope 过滤的说明。
- 6. 若选决策 1A:改 check_databases.py SCHEMAS['db05-frontend-styles'] 加 domain_scope、README schema 行同步,跑 PYTHONUTF8=1 python Light/.github/scripts/check_databases.py 全绿。
- 7. 更新 README:诚实同步卖点——18 设计卡范式留库,26 工具条的 license/版本/定价/链接转实时核验+薄缓存(不再当认证事实),并说明 domain_scope 过滤用法与 style_signal.py 用法。
- 8. 跑 check_freshness.py 与 run_skill_selftests.py 确认薄缓存日期与 style_signal selftest 纳入月度复查与 CI。

## ⚠ 需要你拍板的决策点
- 决策 1(domain_scope 载体):(A)新增第 12 个 schema 字段 domain_scope——过滤最干净,但要改 check_databases.py SCHEMAS + README + 三卡文件并过 CI;还是(B)以 'domain_scope=agri-tech' 子串塞 suitable_project_scene/implementation_notes catch-all——零 CI 改动、仿 db01 ai_policy 先例,但过滤靠字符串匹配较脆。
- 决策 2(薄缓存形态):(A)resources_real.md Part1 表格原地加 last_checked/source_pointer/flag 列——人读友好、改动小;还是(B)抽成 tool_signal.json + style_signal.py——可机器自动核验/回写,但 db05 多一种数据形态、README 卖点表述更复杂。
- 决策 3(license 实时查范围):仅 npm-published 工具(约 16 个)走 registry.npmjs.org 自动查 license+version,非 npm 的画廊/Figma/定价(约 10 个)只存 source_pointer + HTTP 存活、不抓值;还是要求全部只留指针手工核(更保守但放弃 npm 可自动化的红利)。
- 决策 4(无网/查不到时的降级):用户已定'冲突信在线';需补定无网时——是用薄缓存快照值 + 标 stale 继续(不阻断交付),还是硬阻断标'待核实'要求联网后再断言 license?建议前者(配 last_checked 提示),与 venue_signal unavailable 降级一致。
- 决策 5(方法论抽离粒度):glass/neumorphism 的可访问性判断是全量上抽到 a05 visual-a11y-rules.md(db05 卡只留指针),还是因 db05 本就是范式库而保留在卡内 implementation_notes、只把纯 WCAG 阈值上抽?边界需用户拍。
- 决策 6(screenshot_reference 存活探测):纳入 style_signal.py 主动 HTTP 探测(多一类网络调用),还是仅靠现有 check_freshness.py warn-only 月度复查就够?

## 工作量与风险
- 工作量：中。脚本 1 个(style_signal.py,可大量复用 venue_signal.py 结构与 selftest 范式)+ 三卡文件 implementation_notes 改写 + Part1 薄缓存化 + a05 新建 1 个 reference + README 诚实重写;若选 domain_scope 走新字段还要动 CI 一处。风险主要在'诚实同步卖点'与'无网降级'两个口径,技术实现不重,端点(registry.npmjs.org)已被仓库实测可用。
- 风险：(1)卖点缩水需诚实:README 现宣称『18 设计卡 + 26 工具条』,重构后 26 工具条的 license/版本/定价不再是认证事实而是薄缓存+实时,README 必须明说,否则与实际能力不符(踩 CONVENTIONS §4 诚实)。(2)联网依赖加重:license/版本从'读卡即得'变成'要跑脚本/联网',无网时只能给 stale 快照——需降级路径兜底(决策 4)。(3)registry.npmjs.org 的 .license 字段对个别包可能缺失或非标准 SPDX(如 shadcn 是 CLI 非组件库、Pro 定价根本无 API),会出现查不到——必须优雅降级标 待核查,不可编。(4)迁移破坏现有引用:a05 多处'沉淀进 db05/登记 db05'与 a07 的 design_tokens.template.json 引用必须保持路径不变;新增 domain_scope 走字段(决策 1A)会动 CI 校验,改错会红。(5)方法论上抽若过度,db05 卡变得过空、失去'范式库'自包含价值——抽离粒度要克制(决策 5)。(6)本环境 WebFetch 被拦,style_signal.py 必须走 urllib(已证可行),不能依赖 WebFetch,否则脚本在本环境跑不通。
