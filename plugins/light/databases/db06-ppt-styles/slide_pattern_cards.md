# db06 扩展卡 — 高级 PPT 页型与叙事模式

> schema: `scenario, theme_style, page_type, layout_structure, color_palette, font_pairing, visual_hierarchy, chart_style, icon_style, transition_style, speaker_notes_style, reuse_template_notes`
> 核验日期：2026-06-10（前 8 卡）/ 2026-06-12（开题、课程教学 2 卡）。Marp、reveal.js、python-pptx、PptxGenJS 官方文档均脚本 HTTP 200 可达；本文件总结可复用”页型/叙事模式”，不复制任何商用模板素材。
> **来源诚信说明**：「开题报告答辩」「课程教学」两卡的调色板/字体配对取自 db06 自家已验证的 `light-slides/assets/themes.py`（academic / light_elegant 主题，selftest 绿），版式逻辑参照公开来源（HTTP 200 核验 2026-06-12）。

```yaml
- scenario: 学术论文答辩 — action-title 结果页
  theme_style: 学术风/浅色/结论先行
  page_type: 结果页 / 图表页
  layout_structure: 顶部行动式标题(一句结论) + 左侧大图(60%) + 右侧 3 条 so-what 解读 + 底部数据来源
  color_palette: 白底 + 单一学校/项目主色 + 本方法强调色 + baseline 灰
  font_pairing: 思源黑体标题 + 思源黑体正文; 英文 Helvetica/Arial; 数字可用等宽
  visual_hierarchy: 行动式标题最大，其次图中高亮，最后解释 bullet；正文不超过 40 词
  chart_style: 复用论文图但放大轴标与图例，关键序列加粗/变色，直接在图上标注发现
  icon_style: 基本不用图标，最多用箭头/圈注
  transition_style: 图先出现，结论 bullet 逐条淡入
  speaker_notes_style: "先读标题结论→指图中高亮→解释为什么重要，每页 35-50 秒"
  reuse_template_notes: 适合所有主结果页；可由 python-pptx 批量生成，确保图文一致

- scenario: 学术报告 — 方法 pipeline 页
  theme_style: 学术/科技克制
  page_type: 方法概览 / 技术路线
  layout_structure: 左到右 4-6 个阶段块 + 上方输入/下方输出 + 创新模块描边高亮
  color_palette: 白底或浅灰底 + 低饱和阶段色 + 单一强调色
  font_pairing: 无衬线标题 + 无衬线正文; 模块名 16-18pt
  visual_hierarchy: 主流程箭头 > 创新模块 > 输入输出细节
  chart_style: Mermaid/Graphviz/draw.io 导出的矢量流程图，字号投影可读
  icon_style: 线性图标或纯文字块，统一线宽
  transition_style: 按流程阶段依次出现，不做复杂飞入
  speaker_notes_style: 每阶段一句“输入-处理-输出”，最后一句点明创新模块
  reuse_template_notes: 与论文 m09/m11 的模型框架图同源，避免 PPT 另画一套导致不一致

- scenario: 文献综述 / 相关工作矩阵页
  theme_style: 学术/信息密度中等
  page_type: 文献矩阵 / gap 定位
  layout_structure: 二维矩阵：行=代表工作，列=任务/数据/方法/局限；最后一列高亮 gap
  color_palette: 白底 + 浅灰表格线 + gap 强调色
  font_pairing: 无衬线; 表格正文 12-14pt，关键词加粗
  visual_hierarchy: gap 列最突出，其余列保持中性
  chart_style: 表格 + 轻量色块，不用花哨图标
  icon_style: 勾/叉/短横可用，但需图例说明
  transition_style: 先显示矩阵，再高亮 gap 列
  speaker_notes_style: 不逐格读；讲“已有工作覆盖了什么、缺什么、我们补什么”
  reuse_template_notes: 由 m01 文献表自动生成；适合开题、答辩、论文引言前半段

- scenario: 数据分析汇报 — dashboard summary 页
  theme_style: 数据分析风/浅色高级
  page_type: 概览页 / KPI 总览
  layout_structure: 上方 3-5 个 KPI 卡 + 中间主图 + 右侧异常/风险列表
  color_palette: 中性浅底 + 色盲安全数据色 + 风险橙/红
  font_pairing: 无衬线 + 等宽数字; KPI 数字 32pt+
  visual_hierarchy: KPI 数字 > 主图 > 风险列表 > 注释
  chart_style: 同一页最多 1 张主图 + 1 个小 sparkline；避免图表堆满
  icon_style: 简洁状态图标，颜色不是唯一编码
  transition_style: KPI 数字出现后主图淡入
  speaker_notes_style: "一句总览结论 + 解释最大异常 + 下一步动作"
  reuse_template_notes: 可用 python-pptx 从 m06 summary.json 生成；适合周报/结题汇报

- scenario: 竞赛路演 — 痛点到方案强钩子页
  theme_style: 竞赛路演/高对比/故事化
  page_type: 痛点页 / 方案页
  layout_structure: 左侧大痛点数字/一句话，右侧真实场景图或抽象示意，下方三步方案
  color_palette: 深色或白底高对比 + 品牌强调色 + 危险/机会色
  font_pairing: 粗黑标题 + 无衬线正文; 核心数字超大
  visual_hierarchy: 痛点数字/结论 > 方案三步 > 说明脚注
  chart_style: 单指标大数字 + 简化流程，不放复杂统计图
  icon_style: 彩色填充图标可用，但全 deck 保持同一套
  transition_style: 痛点先出现，方案后出现，形成反差
  speaker_notes_style: 20 秒内讲清“为什么现在必须解决”
  reuse_template_notes: 市场/用户数据必须可核查；未经来源的数据不进页

- scenario: 创业/成果转化 — 商业模式与财务假设页
  theme_style: 商务/路演/可信
  page_type: 商业模式 / 财务预测 / 假设登记
  layout_structure: 左侧商业模式画布，右侧 3 年关键假设与收入/成本小表
  color_palette: 白底 + 品牌主色 + 中性灰 + 现金流转正强调色
  font_pairing: 无衬线; 表格正文 11-13pt，关键数字 24pt+
  visual_hierarchy: 假设来源 > 收入/成本逻辑 > 预测结果
  chart_style: 瀑布图/堆叠条/简化损益表；必须标假设来源
  icon_style: 线性业务图标，避免卡通化
  transition_style: 不花哨；逐步显示收入、成本、盈亏平衡
  speaker_notes_style: 明确每个数字来自哪里，无法核实就说“待验证假设”
  reuse_template_notes: 与 db08 budget_template / case_skeletons 联动；严禁臆造市场规模

- scenario: A0 学术海报 / 展板
  theme_style: 学术海报/高可读/远距离
  page_type: 单页海报
  layout_structure: 三栏网格：背景/方法/结果/结论；顶部标题横幅，右下角二维码/联系
  color_palette: 白底 + 学校主色 + 结果强调色；大面积低饱和背景
  font_pairing: 标题无衬线 72pt+，正文 28-36pt，图注 22pt+
  visual_hierarchy: 标题 > 结论框 > 主图 > 方法细节
  chart_style: 图大字少，所有论文图重导出高分辨率/矢量
  icon_style: 少量统一线性图标
  transition_style: 无
  speaker_notes_style: 海报讲解词按 1 分钟/3 分钟两个版本准备
  reuse_template_notes: PPTX 设 A0 尺寸或用 beamerposter；图片至少 150-300 DPI，嵌入字体

- scenario: 投稿返修 / rebuttal 汇报页
  theme_style: 学术/审稿响应/克制
  page_type: 问题-回应矩阵 / 修改证据页
  layout_structure: 左列 reviewer concern，右列 response/action/evidence，底部标论文页码/图表编号
  color_palette: 白底 + 中性灰 + 已解决绿色 + 需补实验橙色
  font_pairing: 无衬线; 引文/审稿意见用浅灰框
  visual_hierarchy: 审稿人问题 > 我们的动作 > 证据位置
  chart_style: 小表/勾选矩阵；必要时嵌入新增结果小图
  icon_style: 状态 lozenge，不用表情符号
  transition_style: 一条意见一条意见出现
  speaker_notes_style: 用 R-A-C 结构：Response、Action、Citation/Change location
  reuse_template_notes: 与 m14 response letter 同源，确保页码/图号/修改内容一致

- scenario: 开题报告答辩
  theme_style: 学术风/浅色高级(academic 主题)
  page_type: 封面/选题背景/研究现状与gap/研究问题与目标/技术路线/创新点/计划进度/预期成果/参考文献
  layout_structure: 顶部细标题条 + 左文右图; 研究现状用文献矩阵, 技术路线用横向 pipeline, 进度用甘特图
  color_palette: 白底 #FFFFFF + 学校主色(取 academic 主题 primary #1F4E79) + 辅蓝 #2E75B6 + 深灰字 #333333 + 强调红 #C00000(仅创新点/gap)
  font_pairing: 思源宋体标题 + 思源黑体正文(academic 主题 FONTS); 英文 Times New Roman; 公式 LaTeX
  visual_hierarchy: 研究问题/创新点最突出 > 技术路线图 > 研究现状 > 计划细节; 一页一观点
  chart_style: 文献 gap 矩阵 + 技术路线框图 + 甘特/里程碑时间线; 开题阶段多为示意, 数据图占比低
  icon_style: 统一线性图标(同一线宽), 阶段块用克制色块
  transition_style: 淡入, 克制无花哨
  speaker_notes_style: "每页 1-2 句; 重点讲清'为什么做(gap)→做什么(问题/目标)→怎么做(路线)→做到什么程度(预期)'; 开题控时 10-15 min"
  reuse_template_notes: 区别于毕业答辩——开题重'问题与计划'而非'结果'; 技术路线图与 m05 研究计划/m09 框架图同源, 勿另画一套; 推荐 Beamer(academic)或 Marp 出稿。版式参考 Beamer 主题矩阵 https://mpetroff.net/files/beamer-theme-matrix/

- scenario: 课程教学 / 授课讲义
  theme_style: 浅色高级/莫兰迪(light_elegant 主题)/低认知负荷
  page_type: 章节封面/学习目标/概念讲解/示例演示/课堂活动或提问/小结/作业与延伸阅读
  layout_structure: 单点聚焦, 一屏一概念; 概念页左图(示意)右文(要点≤5), 示例页用分步高亮, 小结页回扣学习目标
  color_palette: 米白底 #FAF8F5 + 莫兰迪主色 #7C6F64(取 light_elegant 主题) + 辅 #A39788 + 强调 #B5651D(仅关键术语/重点) + 深灰字 #3A352F
  font_pairing: 思源黑体标题+正文(light_elegant 主题 FONTS); 正文字号偏大(投影后排可读), 代码用 Consolas
  visual_hierarchy: 学习目标/关键术语 > 示意图 > 讲解要点 > 补充; 认知负荷低, 单页信息量克制
  chart_style: 概念示意图/类比图为主, 数据图少而精; 善用前后对比、流程分解、标注引导注意力
  icon_style: 双色线性图标, 统一圆角; 用图标区分'定义/示例/注意/练习'
  transition_style: 淡入/轻推; 分步揭示(逐条出现)降低一次性信息量, 配合讲解节奏
  speaker_notes_style: "每页讲解锚点 + 预设课堂提问/易错点; 按一节课 45 min 配 15-25 页, 留活动与答疑时间"
  reuse_template_notes: 与答辩/汇报不同——教学重'循序渐进与认知负荷', 多用分步揭示与示例; 章节封面/目标页/小结页可模板化复用。版式逻辑参考 CMU 教学设计 https://www.cmu.edu/teaching/designteach/teach/instructionalstrategies/lectures.html

```
