# light-figure-drawing — 深度分析与同类对标

> 源：[`skills/light-figure-drawing/SKILL.md`](../../../skills/light-figure-drawing/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：从顶刊投稿视角把规划好的图实际画出来的"执行层"绘图技能:多工具选型指南 + 自带 matplotlib 投稿级样式/导出/配色/诚实性 lint 四件套,核心卖点是按刊锁死物理栏宽与字号。

## 核心运行逻辑
技能定位是 Light 体系里 m09(规划)下游的"执行画图"环节:读规划卡的叙事层(图绑哪个 claim、组图角色)与规格层(source_card/target_journal/column),照卡产出可复现代码+矢量/位图+figure manifest。设计上把"栏宽数字的唯一真相源"收敛到 figure_export.py 的 JOURNAL_SPECS 字典,SKILL.md 里的人读表只是镜像,杜绝臆测栏宽。四个自带脚本各司其职:mplstyle 套样式、figure_export 按 mm 锁尺寸并导出+校验、color_palettes 做 Okabe-Ito 色盲安全配色与 CVD 模拟、figure_integrity_lint 静态扫绘图代码提示误导风险。强调矢量优先、文字可编辑(fonttype42)、色盲安全、诚实性(误差棒类型/截断轴/双轴/rainbow),并设了 AI 生成图像投稿红线与 PPT 链路的严格隔离。所有脚本无外部数据、Agg 后端、自带 selftest/demo,可独立跑通。

## 关键步骤
- 1. 读规划卡:上层确认 claim 与组图角色,下层读 source_card(必填,指向 db07 实体卡)/target_journal/column
- 2. 选工具:统计图走 matplotlib/seaborn(首选可复现),框架图走 Graphviz/TikZ,精细曲线走 Origin/MATLAB,示意图走 BioRender,最终精修进 Illustrator/Inkscape
- 3. 套样式:plt.style.use publication.mplstyle 作底,按刊叠加 nature/science.mplstyle(Okabe-Ito 色环+无衬线+矢量可编辑)
- 4. 配色:优先用 db09 项目 palette.json,否则 color_palettes 的 Okabe-Ito;preview_palette 出原色/灰度/三色盲对照复核
- 5. 导出:save_for_journal(fig, base, journal, column) 按 mm 锁物理尺寸+最小字号,bbox_inches=None 兑现精确栏宽
- 6. 导出后必检:check_figure_size(实测落盘文件宽度) + check_scaled_fonts(缩放后有效字号);涉误差棒/截断轴/双轴/rainbow 再跑 figure_integrity_lint
- 7. 产出 figure manifest(figure_id↔文件↔caption↔检查结果)交 m07,风格说明写 db09 version_history,新增可复用模式才回写 db07

## 自带资产
- assets/publication.mplstyle:通用投稿级底样式(无衬线/去chart junk/Okabe-Ito色环/fonttype42)
- assets/nature.mplstyle:Nature 风格(默认 figsize 89mm 单栏,字号5-8pt)
- assets/science.mplstyle:Science 风格(默认 120mm 双栏,刻度朝内)
- scripts/figure_export.py:核心导出器,含 JOURNAL_SPECS(7刊)、save_for_journal按mm锁尺寸、check_figure_size(支持measured读回落盘文件实测宽度)、check_scaled_fonts(缩放后有效字号盲点)
- scripts/color_palettes.py:Okabe-Ito 8色常量、sequential/diverging/discrete cmap、to_grayscale、simulate_cvd(colorspacious精确/线性近似降级)、preview_palette
- scripts/figure_integrity_lint.py:静态正则扫绘图代码,7类误导风险(截断轴/双轴/无误差棒bar/误差棒无类型/rainbow/3D),含selftest
- references.md:14种工具(matplotlib/seaborn/plotly/altair/ggplot2/R base/MATLAB/Origin/TikZ/Graphviz/Mermaid/Inkscape/Illustrator/PPT/BioRender)逐条真实API+已知坑,含SciencePlots对照与专利附图规范
- references/figure_integrity.md:图表诚实性硬规范+三家头部出版商AI生成图像红线表
- examples/:matplotlib多面板(GridSpec+标号+误差棒+显著性)、seaborn统计对比、Graphviz框架图(.dot+渲染脚本,无dot降级matplotlib),均可跑通

## 优点
- 栏宽单一真相源设计扎实:JOURNAL_SPECS 字典 + SKILL.md 镜像表 + custom 逃生通道 + 反复强调禁止臆测栏宽,从机制上堵住投稿图物理尺寸作废的高频坑
- check_figure_size 的 measured 模式真正读回落盘 PNG/PDF/SVG 的物理宽度复核(PIL读dpi/pypdf读MediaBox/解析svg width),能抓出 bbox_inches=tight 静默改栏宽的盲点,demo 里有对应回归断言,不是纸面承诺
- 诚实性是真正的差异化:既有规范文档(误差棒类型/截断轴/双轴/小样本bar反模式/image integrity)又有可跑的 lint 脚本,还把 2026 AI 生成图像投稿红线和 PPT 链路隔离写成硬约束,这是多数绘图工具忽略的审稿命门
- verified 标记诚实:7刊里只有 nature/science/plos 标 verified=True 并附 HTTP200/多源核实日期,其余明确标未实测+付费墙原因,note 里留了来源,符合科研可核查精神
- 脚本工程质量高:全部无外部数据、Agg 后端、自带 selftest/demo 断言关键不变量,colorspacious 缺失时 CVD 降级线性近似且 cvd_backend() 可查,Graphviz 无 dot 时降级 matplotlib,鲁棒性好
- references.md 不堆砌:每个工具按是什么/真实API/链接/已知坑结构化,SciencePlots vs 自有 mplstyle 给了选用矩阵,专利附图按 CNIPA 规范单列,体现真实领域经验
- 与 Light 生态衔接定义清晰:受 m09 驱动、交 m07 的 figure manifest 用 yaml 示例锁死 figure_id↔文件↔caption↔检查结果,db07/db09/db01 各自职责边界写得明确

## 缺点 / 可被质疑处
- check_scaled_fonts 与 save_for_journal 逻辑上互斥近乎空转:save_for_journal 已把画布设成精确栏宽(scale=1),之后跑 check_scaled_fonts 必然报 scale>=0.999 无风险。它只在'先大画布作图再缩到栏宽'的工作流才有意义,但 SKILL.md 推荐的恰是前者,导致 SKILL.md '导出后必检 check_scaled_fonts' 这条指令在标准流程下是无效操作,文档没点破这个前提
- figure_integrity_lint 是纯正则扫描,假阴性偏多:1) ERRTYPE 正则含 \bstd\b,任何 numpy .std() 调用(如自带 example_matplotlib 里 resid.std())都会被当成'已声明误差类型'从而压掉 ERRBAR_NO_TYPE 警告;2) BAR 正则 \.(bar|barh)\( 匹配不到 seaborn 的 .barplot(,sns.barplot 完全漏检;3) SETYLIM 抓不到 set_ylim(bottom=5) 关键字形式;4) SMALL_N 依赖代码里literal写 n=,真实绘图代码极少这么写
- lint 仅覆盖 matplotlib,但技能本身大力推荐 seaborn/plotly/altair/ggplot2/MATLAB,这些工具产的代码诚实性完全不被检查,诚实性保障实际只落在 matplotlib 一条链路
- 字体一致性是承诺但无校验:mplstyle 把 font.sans-serif 设 Arial/Helvetica 优先,但这两个字体在 Linux/CI 常不存在,matplotlib 会静默回退 DejaVu Sans——'字体与正文一致'的核心诉求可能悄悄落空,而导出/校验链路里没有任何'实际渲染字体≠期望字体'的告警(已知坑只在 references 提了一句)
- 校验维度不全:JOURNAL_SPECS 含 min_dpi 各档和 preferred_formats,但 check 系列只查宽度+字号,不查高度上限(PLOS 高<=2625px、整页高有限)、不查文件体积(PLOS<10MB)、不查实际导出 dpi 是否达 min_dpi、不查格式是否在 preferred_formats 内——这些规格录进了字典却没被任何函数消费
- MDPI 的 single_mm=170 语义可疑:170mm 是 MDPI 单列版式的正文整宽,把 column='single' 映射到 170mm 容易让人误以为是窄单栏,与其他刊 single≈85mm 的直觉冲突,且 mdpi 只有 single/full 两键都=170,column 参数形同虚设
- 7刊里 4 刊(cell/ieee/elsevier/mdpi)verified=False,中文刊全靠 custom 手传——覆盖面对非英文/非头部刊仍薄,且 custom 通道不强制最小字号,等于绕过了字号校验这道关
- CMYK 与 TIFF 是多家硬要求(印刷 CMYK、PLOS 仅收 TIFF/EPS),但 matplotlib 出不了 CMYK、TIFF 依赖 Pillow,脚本对 Pillow 缺失/CMYK 转换没有 guard 或自动化钩子,只能口头甩给 Illustrator

## 可优化点（供后续逐技能优化）
- 把 figure_integrity_lint 从正则升级为 AST 解析(ast 模块走 matplotlib,正则兜底其他库):精确识别 set_ylim 的位置/关键字参数、区分 .std() 数据计算与误差类型声明(只在 errorbar/fill_between 的 caption/邻近注释里找 SD/SEM/CI)、补 sns.barplot/sns.boxplot 检测,并新增 seaborn/plotly 的专用规则
- 在 figure_export 导出阶段加字体落空告警:导出前用 matplotlib.font_manager 检查 font.sans-serif 首选项是否真实可用,回退到 DejaVu 时打印 WARNING 并写进 info dict,让'字体与正文一致'可验证
- 让 check 系列消费已录入但闲置的规格:新增高度上限校验、导出后实测 dpi 校验(measured 模式下 PNG 读 dpi、按像素反推)、文件体积校验(PLOS<10MB)、格式是否在 preferred_formats 内的检查,把 JOURNAL_SPECS 的字段用满
- 澄清并重构 check_scaled_fonts 的适用场景:要么在 SKILL.md 明确它只服务'大画布工作流'、save_for_journal 流程下跳过,要么提供一个显式的 draw_large_then_scale 模式让两者不矛盾;当前'导出后必检'的措辞要修正
- 修正 MDPI 的 column 语义:补 MDPI 真实的窄栏/整栏数据(或注明 MDPI 为单列版式、single 即正文整宽 170mm 并在 note 写清),避免 single 被误读
- 补齐 cell/ieee/elsevier/mdpi 的实测(投稿前逐家官网核栏宽/dpi/格式),把 verified 翻成 True 并附核实日期;给 custom 通道加可选 min_font_pt 参数,使中文刊也能走字号校验而非裸奔
- 给 TIFF/CMYK 加落地支持:save_publication_figure 对 TIFF 格式先检测 Pillow 可用性、缺失时清晰报错;提供一个可选的 Pillow 后处理钩子把 RGB PDF/PNG 转 CMYK TIFF(或至少在 info 里标注'印刷需手动 CMYK 转换'),减少甩给 Illustrator 的断点
- examples 增加反例与负向用例:补一个'故意违规'示例(截断轴/无误差棒 bar/rainbow)让 lint 命中,既当 lint 的端到端测试,也当用户对照教材

## 与其他 Light 技能/知识库的衔接
上游受 m09(light-figure-planning)驱动,读其规划卡的双层字段(叙事层 claim/组图角色 + 规格层 source_card/target_journal/column);需要数据时回 m06/m02 取。下游交 m07(light-paper-drafting)的 figure manifest(yaml 绑 figure_id↔文件↔caption↔检查结果)、交 m12 排版插入;跨图风格一致性由 a07 维护。知识库依赖:db07-figures(图表模式实体卡,source_card 必指向 resources_real.md 或 figure_advanced_cards.md,figure_cards.md 仅模板索引不可执行)、db09-projects(项目 palette.json 作视觉 SSOT 必用、version_history.md 落风格说明)、db01(中文刊等表外栏宽来源)、db07 调色板登记。横向:受 m15(light-ip-application)委托按专利附图规范绘黑白线条图;与 m16(PPT/前端)严格隔离——AI 生成图像严禁进论文图链路,m16 要放数据图须从本技能成品重画。工具决策同 a09。

---

## GitHub 同类前沿技能对标

GitHub 上同类项目大致分三层:一是纯样式/工具库(SciencePlots、tueplots、pub-ready-plots、proplot、pypubfigs、SSCI-Plots、figrecipe),它们把"投稿级样式 + 按刊/会议物理栏宽字号"做成可 import 的 Python 包,功能密度高、被社区长期打磨;二是 agent skill 生态(davila7、K-Dense、Galaxy-Dawn/pubfig),把绘图能力封装成 LLM 可调用的技能;三是单点工具(okabe-ito-py 配色)。Light 的 light-figure-drawing 在功能层面与第一层高度重叠(JOURNAL_SPECS 锁 mm 栏宽 ≈ tueplots,Okabe-Ito 色盲安全 ≈ pypubfigs,mplstyle 套样式 ≈ SciencePlots),但它的独特定位在第二、三层都罕见:它不是库而是"规划→执行"工作流中的一环(读 m09 规划卡的 claim/组图角色再产图),且自带 figure_integrity_lint 这种"诚实性静态扫描"(误差棒类型/截断轴/双轴/rainbow 误导)和 AI 生图投稿红线——这两点在所有检索到的同类项目里几乎没有对应物。换句话说,别人强在"画得专业、配置全",Light 强在"为什么画这张、画得诚不诚实、能不能复现交付",是面向 agent + 投稿合规的工作流编排,而非一个更好的 matplotlib 封装。劣势是底层绘图功能广度、社区验证和样式精细度远不及 SciencePlots/tueplots/proplot 这些万星级或专门库。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [garrettj403/SciencePlots](https://github.com/garrettj403/SciencePlots) | 最知名的科研投稿级 matplotlib 样式库,提供 science/ieee/nature 等可叠加 .mplstyle 风格,一行 plt.style.use 即得期刊级外观 | 8971 | 2026-02-25 | 强:社区验证充分(近9k星)、风格覆盖广、可叠加组合成熟。弱:只管'外观样式',不锁物理 mm 栏宽/不做色盲安全强约束/无诚实性 lint/无 agent 工作流,Light 在'按刊锁尺寸+诚实性+复现交付'上更系统 |
| [pnkraemer/tueplots](https://github.com/pnkraemer/tueplots) | 按具体会议/期刊(NeurIPS、ICML、JMLR 等)精确设置 figure size、字号、字体的轻量配置库,主打最小开销修好论文图尺寸 | 743 | 2026-03-24 | 强:venue 尺寸/字号换算极精细且区分单双栏,正是 Light JOURNAL_SPECS 想做的事,条目更全。弱:纯尺寸字号配置,无配色/无诚实性检查/无 agent 编排,Light 的'唯一真相源字典+lint+规划联动'范围更大 |
| [wiseodd/pub-ready-plots](https://github.com/wiseodd/pub-ready-plots) | opinionated 的投稿绘图库,为 ICML/NeurIPS/ICLR/AISTATS 及期刊提供正确尺寸与上下文管理器式样式 | 74 | 2026-05-10 | 强:开箱即用 context manager、ML 顶会尺寸预设到位。弱:聚焦尺寸样式,无色盲安全模拟/无 integrity lint/无 AI 生图红线,Light 的诚实性与合规边界是其没有的 |
| [proplot-dev/proplot](https://github.com/proplot-dev/proplot) | 简洁的 matplotlib 封装,擅长组图布局、共享色条/图例、漂亮的默认配色与字体,面向 publication-quality 图形 | 1154 | 2025-02-27 | 强:组图/共享色条图例的 API 设计成熟、出图美观。弱:近一年多未大更新且与新版 matplotlib 兼容性受关注;不针对具体期刊锁 mm 栏宽,无诚实性/合规层,Light 更贴投稿规范 |
| [JLSteenwyk/pypubfigs](https://github.com/JLSteenwyk/pypubfigs) | 为 seaborn/matplotlib 提供投稿质量主题 + 色盲友好调色板的小型库 | 5 | 2026-02-24 | 强:命名色盲友好 palette 开箱即用。弱:体量小、只做主题与配色,无尺寸锁定/无 lint/无工作流,Light 的 color_palettes 已含 Okabe-Ito+CVD 模拟且嵌入更大体系 |
| [davila7/claude-code-templates (scientific-visualization skill)](https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/scientific/scientific-visualization/assets/color_palettes.py) | 大型 Claude Code 配置/技能模板仓库,内含 scientific-visualization 技能,自带 color_palettes.py 等绘图资产,是与 Light 同形态的 agent skill | 28016 | 2026-06-12 | 强:仓库星标极高、技能生态完整、分发渠道成熟,且同样走'技能+配色脚本'路线。弱:其可视化技能偏通用,未见按刊锁 mm 栏宽/诚实性 lint/AI 生图红线这类投稿合规深度,Light 在科研投稿垂直度更高 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 号称#1 的科研 agent skills 库,140+ 技能 + 100+ 科学数据库,覆盖生化医药,兼容 Cursor/Claude/Codex 等开放 Agent Skills 标准 | 28080 | 2026-06-12 | 强:规模与影响力大(2.8w星、宣称16万科学家使用)、多宿主兼容、数据库联动,生态与 Light 体系最可对标。弱:广度优先,绘图为众多技能之一,未见专门的投稿级栏宽锁定/figure 诚实性 lint,Light 在'画图执行+合规'单点更深 |
| [Galaxy-Dawn/pubfig](https://github.com/Galaxy-Dawn/pubfig) | 面向论文的投稿风格科研绘图工具,提供常见图族、干净导出与 panel-first 的 Figma 组图装配 | 57 | 2026-04-23 | 强:显式支持'面板优先 + Figma 组图装配'的外部组版链路,补足 Light 偏弱的组版环节。弱:无明确按刊 mm 锁定/无色盲安全强约束/无诚实性 lint,Light 的规格唯一真相源与 integrity 检查更严 |
| [O0000-code/SSCI-Plots](https://github.com/O0000-code/SSCI-Plots) | 面向 SSCI/SCI 期刊投稿的 publication-ready matplotlib 样式集 | 2 | 2026-05-17 | 强:明确针对中文社科/SCI 投稿场景,定位贴近国内用户。弱:体量极小、主要是样式表,无尺寸锁定逻辑/无配色科学性/无 lint/无 agent 集成,Light 功能完整度高出很多 |
| [ywatanabe1989/figrecipe](https://github.com/ywatanabe1989/figrecipe) | 可复现的 matplotlib wrapper,主打 mm 精度布局,理念上与 Light'照卡复现产图'最接近 | 0 | 2026-06-12 | 强:与 Light 思路最像(mm 精度 + 可复现),在'复现'这一维度落到代码层值得跟踪。弱:刚起步无社区验证、无色盲安全/诚实性 lint/无 venue 字典与 agent 工作流,Light 体系更完整成熟 |

### Light 该技能可借鉴的点
- tueplots(743★)把'按会议/期刊精确换算 figure size + 字号'做成结构化配置(NeurIPS/ICML/JMLR 等),且区分单双栏、半栏、字号随栏宽自适应——Light 的 JOURNAL_SPECS 可对照补全更多具体 venue 条目和'字号随栏宽联动'逻辑,而不仅锁物理宽度
- SciencePlots(8971★)用可叠加的 .mplstyle 分层组合(science + ieee + nature + grid + 各种子风格)证明了'风格正交可组合'的价值,Light 的单一 mplstyle 可拆成可叠加层,提升复用与按刊切换效率
- proplot(1154★)在'子图/组图布局、共享色条、统一图例'上的 API 设计成熟,Light 处理组图(panel a/b/c 角色)时可借鉴其布局与跨子图一致性管理
- Galaxy-Dawn/pubfig 明确把'panel-first Figma 组图装配'写进定位——Light 目前对 PPT 链路做严格隔离,但可考虑为'矢量面板→外部组版工具(Figma/AI)'设计同样清晰的导出边界与素材命名规范
- pypubfigs 把'色盲友好调色板 + 主题'打包成开箱即用的命名 palette,Light 的 color_palettes.py 可补充更多场景化命名色板(定性/顺序/发散)与一键预览对照表
- K-Dense scientific-agent-skills(28080★,140 技能 + 跨 Cursor/Claude/Codex 兼容)证明科研 agent skill 走'开放标准 + 多宿主兼容 + 数据库联动'路线能规模化,Light 体系若想外部分发可参考其技能打包与互操作约定
- figrecipe 主打'mm 精度布局 + 可复现 matplotlib wrapper',与 Light 思路最像,值得跟踪它如何把'可复现'落到代码层(随机种子/数据快照/manifest)以强化 Light 的 figure manifest 设计
