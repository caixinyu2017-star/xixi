# light-figure-planning — 深度分析与同类对标

> 源：[`skills/light-figure-planning/SKILL.md`](../../../skills/light-figure-planning/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：论文图表的"规划层"技能:把每条 claim 映射成必做/可做/可删的图表,填成双层规划卡,交 light-figure-drawing(m11)照卡执行——只决策不画图。

## 核心运行逻辑
核心命题是"图表服务论点,不是装饰":每张图先回答"它支撑哪条 claim、删掉论文会不会缺一块"。规划流程为 列claim→匹配最有说服力的呈现形式→标优先级(必做/可做/可删)→定排版位置(正文/附录/组图)。产出是一张张"规划卡",上层锁叙事(绑哪条 claim、讲什么故事、放哪节、组图里回答哪个唯一科学问题),下层锁规格(figure_type、配色、栏宽键、无障碍)。设计上刻意把"栏宽/字号/格式"的真相源外包给 light-figure-drawing 的 figure_export.py JOURNAL_SPECS,自己只引用键名,避免臆测物理尺寸导致整图作废。组图反冗余检验(遮住任一 panel 应造成无法补回的信息缺口)是其最有方法论价值的原创检查点。

## 关键步骤
- 1. 通读论文/大纲 + m06 结果,列出全部 claim
- 2. 给每个 claim 匹配最有说服力的图表类型(概念/数据/定量/定性/表 五大类清单)
- 3. 标优先级:必做(核心贡献)/可做(增强)/可删(冗余或弱)
- 4. 定排版:进正文还是附录、组图如何组(overview→deviation→relationship 信息递进)
- 5. 查 db07 canonical 图表模式库,命中已有 figure_type 则复用,确无匹配才规划新增可复用卡
- 6. 为每张图/表填 figure_plan_card(双层:叙事层+规格层),写明 source_card、target_journal、column
- 7. 过审稿人视角自检(13 点投稿前核查 + 5 维示意图评分≥8.5 + 组图反冗余)
- 8. 规划卡交 m11 绘制,项目级图号/caption/导出路径登记到 db09 manifest

## 自带资产
- SKILL.md — 规划方法论主体:流程、图表类型清单、工具选型速查、出版级硬规格(配色/字体/8家出版商栏宽)、db07查找纪律、规划卡字段定义、审稿人自检清单
- references.md — 14+工具的逐一核查笔记(matplotlib/seaborn/plotly/ggplot2/Altair/Graphviz/Mermaid/TikZ/draw.io/BioRender/Inkscape/Illustrator + 3个社区科研技能),含真实API参数与已知坑;另含'出版商图宽硬规格核查表'并诚实标注哪些经curl实测、哪些付费墙未实测
- templates/figure_plan_card.md — 双层规划卡模板:上层叙事(绑claim/讲什么故事/放哪节/优先级/组图唯一科学问题)+下层规格(db07基础字段+项目执行辅助字段)+无障碍自检清单+交接说明

## 优点
- 定位锋利:'图服务claim、删掉会不会缺一块'这条贯穿始终的判据,直接对标审稿人对 display item 必要性的拷问,避免凑图
- 组图反冗余检验是真正的原创方法论(遮住任一panel应造成不可补回的信息缺口,并列出3类冗余陷阱+替换思路),比泛泛说'组图要一致'有可操作性
- 规格层不臆测:明确把栏宽/字号真相源指向 figure_export.py 的 JOURNAL_SPECS 键,custom_width_mm 逃生通道处理中文刊,工程上很克制
- references.md 的诚实声明罕见且专业:逐条标注 Nature 经 curl 实测 HTTP200、其余出版商付费墙403未实测,并指出原始社区笔记的 Science 175/Cell 178 是错值已更正——可追溯、不糊弄
- 双层规划卡设计清晰地切开了'叙事决策'与'执行规格',且明确哪些字段可沉淀回 db07、哪些只进项目 manifest,与生态其他模块边界划得干净
- 工具选型给到 claim→图型→工具的映射,且区分了代码拼版(GridSpec,可复现)与手工矢量拼版(Inkscape/Illustrator,异源面板自由对齐)的判定条件,不是简单罗列工具

## 缺点 / 可被质疑处
- 零脚本资产:整个技能只有 prose+1模板+references,没有任何可执行校验。规划卡 target_journal/column 是否为 JOURNAL_SPECS 实有键、custom 是否补了 custom_width_mm,全靠人肉遵守,m11 打回成本高
- 栏宽/字号数据三处重复(SKILL正文、references表格、并依赖figure_export.py),违反自己声明的'唯一真相源',一旦 figure_export.py 改值,SKILL 的硬编码数字会静默过期——已现端倪:SKILL说Nature字号最小5pt,references却写通用6-7pt,内部不自洽
- 表(Table)规划被严重边缘化:类型清单里只占一行,却共用图导向的规划卡(color_scheme/layout/GridSpec 等字段对表毫无意义),T# 表缺少列结构、加粗规则、统计标注、跨页处理等表专属字段
- 缺少 examples/:全是原则,没有一张填好的真实规划卡样例(如一张主结果对比图、一张框架图、一张消融表),新手无法照着学 claim→figure 的实际映射粒度
- 未处理 display item 预算:顶刊普遍限制正文图表数量(常6-8件),技能从不要求统计总数对照投稿venue上限,也没有'砍到预算内'的取舍流程
- 强依赖外部代号生态(m02/m06/m07/m08/m11/a07/db01/db07/db09)却无任何图例或术语表,脱离 Light 全家桶几乎无法独立使用;5维示意图评分(≥8.5)直接搬自社区 AI 生图技能,套到所有示意图规划上存在场景错配
- 规划与执行边界仍偏糊:references.md 实质是一本绘图工具手册(含Inkscape CLI语法、kaleido安装、mpl rcParams),这些执行细节更应属于 light-figure-drawing,放在'规划'技能里造成两技能职责重叠

## 可优化点（供后续逐技能优化）
- 新增 scripts/validate_plan_card.py:解析规划卡,校验 target_journal/column 是否命中 figure_export.py 的 JOURNAL_SPECS 键、custom 必须带 custom_width_mm、figure_id 是否唯一且与 m07 占位对齐、source_card 必填——把 m11 的打回前移到规划阶段
- 去重栏宽数据:SKILL/references 的栏宽表改为只放'指针+最后同步日期',或加一个 sync 脚本从 figure_export.py 反向生成快照,杜绝三处漂移;同时修掉 5pt vs 6-7pt 的字号内部矛盾
- 新增 examples/ 放3张填满的真实规划卡(定量主结果对比图、概念框架图、消融表)+一份小型项目的'claim→图表清单'全景,展示必做/可做/可删的实际判定粒度
- 拆出 table_plan_card.md 变体:去掉 color_scheme/layout,加入列/行结构、表头分组、加粗与显著性标注规则、数值对齐与有效位数、跨页/横排处理
- 在流程加'display item 预算'步骤:统计 F#+T# 总数对照目标 venue 上限,超出时强制走取舍(合并/降级到附录/删冗余),并在自检清单加一条数量核查
- 文件顶部加一个代号图例表(m02/m06/m07/m08/m11/a07/db01/db07/db09 各是什么),提升脱离全家桶时的可读性;并把'5维评分'限定为AI生图类示意图专用,代码矢量图改用其专属QA项
- 把 references.md 里纯执行细节(Inkscape CLI、kaleido安装、mpl rcParams 等)瘦身或迁移到 light-figure-drawing,本技能 references 只保留'选型决策'所需信息,强化规划/执行边界

## 与其他 Light 技能/知识库的衔接
上游:m06(light-result-analysis)供结果与claim、m02(light-data-engineering)供数据、m07/m08(paper-drafting/polishing)供论文占位 [图位F1]/[表位T1] 并保图文一致。下游核心:m11(light-figure-drawing)照规划卡执行,且其 scripts/figure_export.py 的 JOURNAL_SPECS 是本技能栏宽/字号/格式的唯一真相源,执行端据 target_journal/column 直接 save_for_journal,并跑 check_figure_size/check_scaled_fonts。知识库:db01 供目标刊与实测栏宽、db07-figures 供可复用 figure_card 模式库(resources_real.md/figure_advanced_cards.md)、db09-projects 登记项目级图号/caption/导出路径/version_history。常驻协同:a07(light-consistency)维护全文图表风格统一。

---

## GitHub 同类前沿技能对标

> 补跑日期 2026-06-13（原 workflow socket 断连失败后单独补检索）。star/更新时间经 GitHub API 实测。

GitHub 上和 light-figure-planning 真正同类的"规划层"工具非常稀少——绝大多数热门项目落在两端：要么是**执行层**(把数据/方法文本直接画成图，如 academic-figures-mcp、ScholarPlot、SciFigureAI、paper-banana、ml-visuals)，要么是**资源清单层**(awesome-* 列表)。中间这条"为每个 claim 规划配哪些图、放哪一节、什么优先级、做完整性检查"的链路，目前只有 HKUSTDial/Supervisor-Skills 的 figure-designer 和经典可视化推荐引擎 Draco/Voyager 沾边，但角度都不同：figure-designer 以**单张图**为单位给设计范式，不是以 **claim/全文论证**为单位；Draco/Voyager 是数据驱动推荐图型，不懂论文叙事与章节角色。也就是说，light-figure-planning 主张的"图表服务于论证、按 claim 双向装配、幽灵 deck 式完整性检查"这一定位，在 GitHub 上几乎没有正面竞品——这是它的差异化空间。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [HKUSTDial/Supervisor-Skills (figure-designer)](https://github.com/HKUSTDial/Supervisor-Skills) | 博导经验型 AI 科研技能集；figure-designer 针对论文三类核心图(动机图/方法总览图/结果图)推荐设计范式、布局、标注、工具并做 QC 审计 | 2460 | 2026-04-29 | 最接近。强：成熟、范式库具体、有 venue 适配、QC 规则细。弱：以**单张图**为单位，不是以**全文 claim**为单位做覆盖规划；无双向规划卡、无 deck 式全局完整性检查 |
| [cmudig/draco2](https://github.com/cmudig/draco2) | 基于约束求解的可视化推荐引擎，给定数据字段+任务推荐/排序图型编码 | 112 | 2026-06-09 | 强：形式化、可学习权重、可程序化调用。弱：纯数据驱动，不懂论文叙事、章节角色、claim 优先级 |
| [vega/voyager](https://github.com/vega/voyager) | 数据探索式可视化推荐工具，枚举并推荐图表 | 1491 | 2023-03-02(停更) | 同 Draco：EDA 选图型导向，无论文/论证/规划维度。可作"图型推荐"子环节灵感 |
| [u9401066/academic-figures-mcp](https://github.com/u9401066/academic-figures-mcp) | MCP server，把论文转成发表级医学/科学图 | 0 | 2026-05-05 | 纯执行层(出图)。与 Light 互补——正是 light-figure-drawing 那一侧的角色 |
| [peizhou/ScholarPlot](https://github.com/peizhou/ScholarPlot) | AI 生成 Nature/Science/Cell 级图表，一键出图 | 1 | 2025-12-10 | 执行层，主打成图质量；无规划/章节/claim 维度 |
| [SciFigureAi/SciFigureAI](https://github.com/SciFigureAi/SciFigureAI) | 从文本/摘要/草图生成科学示意图草稿 | 0 | 2026-06-03 | 执行层(示意图生成)；不做规划与完整性审计 |
| [javidmardanov/paper-banana-skill](https://github.com/javidmardanov/paper-banana-skill) | agentic skill，从方法文本生成发表级示意图 | 2 | 2026-03-13 | 执行层 skill，同生态。弱：只把方法段落变 diagram，不做全文图表规划 |
| [tofunori/mcp-image-scientific](https://github.com/tofunori/mcp-image-scientific) | MCP，出发表级科学图(图/表/地图)并带 QA 校验，Gemini 驱动 | 0 | 2026-02-27 | 执行层+QA；QA 校验思路可借鉴，但无 claim 级规划 |
| [sai-tv/academic-figures](https://github.com/sai-tv/academic-figures) | Claude skill，快速原型化学术图 | 4 | 2026-02-26 | 同生态 skill，执行/原型导向；无规划层 |
| [dair-ai/ml-visuals](https://github.com/dair-ai/ml-visuals) | 可复用 ML 论文图模板与素材库(Google Slides) | 17262 | 2023-02-13(停更) | 资源层(模板素材)，非工具非规划；Light 可引用为"图型范式参考库" |
| [nehSgnaiL/awesome-scientific-figure](https://github.com/nehSgnaiL/awesome-scientific-figure) | 论文优秀科学图的精选清单 | 35 | 2026-04-28 | 资源清单层；可做 Light 规划时的范例图库 |
| [khuangaf/Awesome-Chart-Understanding](https://github.com/khuangaf/Awesome-Chart-Understanding) | 图表理解论文综述清单 | 240 | 2025-12-17 | 偏"机器读图"研究，与规划弱相关；了解"什么样的图易被自动理解"对规划有参考 |

> 没有找到任何项目其核心定位就是"按 claim 规划全文图表清单+双向卡+完整性审计"——**这一精确赛道在 GitHub 上目前是空白**，Light 在这一点上是差异化而非跟随。

### Light 该技能可借鉴的点
- 借鉴 figure-designer 的"范式库"具象化：内置一套"图型范式速查表"，让规划产出从"建议放一张方法图"升级到"建议放方法总览图，推荐 X 范式 + Y 布局骨架"
- 吸收 Draco 的形式化推荐思路：在"根据 claim/数据推荐图型"这一步引入"数据字段→候选图型→按任务排序"的轻量规则，让图型推荐可解释可复现(甚至绘图阶段直接调 draco2)
- 把 QA 校验前移到规划卡：在规划卡里就预置成图必须满足的约束(矢量/字号/色盲安全/坐标轴诚实/caption 自洽)作为交付给 drawing 的硬性 spec，而非画完再审
- 明确"规划层↔执行层"接口契约：把规划卡设计成可直接喂给 academic-figures-mcp/paper-banana/ScholarPlot 这类执行端的结构化输入，坐稳 agent 生态里"上游规划器"的位置
- 引用现成范例图库降低规划成本：ml-visuals(17k★模板)、awesome-scientific-figure 可作规划时的"参考样例池"，规划某图时挂一个高质量范例链接
- 保住并强打差异化：把"每张图回答哪个不可替代的科学问题"做成可量化的覆盖率/冗余度检查报告，加深护城河
