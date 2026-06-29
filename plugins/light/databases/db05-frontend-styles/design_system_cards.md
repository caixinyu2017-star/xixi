# db05 扩展卡 — 官方设计系统与科研项目落地模式

> schema: `project_type, style_tag, layout_type, color_palette, font_style, component_pattern, interaction_pattern, animation_type, screenshot_reference, implementation_notes, suitable_project_scene`
> 核验日期：2026-06-10。下列官方站点均以脚本 HTTP 200 核验可达：Carbon、Fluent 2、Polaris、Atlassian Design System、Primer、USWDS、GOV.UK Design System、Material Design 3。只学习设计系统的结构、token、组件模式，不复制受版权素材。

```yaml
- project_type: 科研数据平台 / 企业级分析后台
  style_tag: Carbon/enterprise-data/中性高密度
  layout_type: 左侧产品导航 + 顶栏 + 数据表/图表工作区 + 右侧详情抽屉
  color_palette: "Carbon Blue #0F62FE / Gray 100 #161616 / Gray 10 #F4F4F4 / support colors"
  font_style: IBM Plex Sans / IBM Plex Mono; 数字与代码用等宽
  component_pattern: DataTable + Tile + Tabs + OverflowMenu + Modal + Notification
  interaction_pattern: 筛选、排序、批量操作、详情抽屉、可访问键盘导航
  animation_type: 极克制; 状态反馈优先于装饰动效
  screenshot_reference: https://carbondesignsystem.com/
  implementation_notes: 适合高信息密度科研平台; token 体系完整; 用 Carbon 思路约束 spacing/type/color，React 可直接用 Carbon Components 或仿其布局逻辑
  suitable_project_scene: 实验管理系统、模型评测平台、数据资产目录、软著后台作品

- project_type: Office/Teams 风格协作系统
  style_tag: Fluent-2/productivity/collaboration
  layout_type: 顶栏命令区 + 左侧 rail 导航 + 卡片/列表混排 + 命令面板
  color_palette: "Fluent neutral + brand accent; light/dark 双主题"
  font_style: Segoe UI / 系统无衬线; 中文用微软雅黑/思源黑体替代
  component_pattern: CommandBar + Persona + Dialog + Toast + Tree + List
  interaction_pattern: 命令优先、上下文菜单、协作状态、通知反馈
  animation_type: 轻量 motion; 只用于状态转移和注意力引导
  screenshot_reference: https://fluent2.microsoft.design/
  implementation_notes: 适合“科研协作/项目管理/文档系统”，把复杂功能做成命令与面板，不做营销页式炫技
  suitable_project_scene: 课题组协作系统、项目进度看板、文献/任务管理系统

- project_type: 电商/成果转化/项目商店
  style_tag: Polaris/commerce/trustworthy
  layout_type: 顶部资源导航 + 页面标题区 + 卡片化表单/设置页 + 订单/商品表格
  color_palette: "Shopify green accent / neutral surface / semantic success-warning-critical"
  font_style: Inter/System sans; 表单标签清晰、正文高可读
  component_pattern: ResourceList + IndexTable + Banner + Card + Form + ChoiceList
  interaction_pattern: 分步配置、批量操作、保存状态、风险提示 banner
  animation_type: 极少; 重点在明确的表单状态和错误提示
  screenshot_reference: https://polaris.shopify.com/
  implementation_notes: 适合把科研成果包装成可演示 SaaS/服务平台；学习其“信任感+可操作”而非复制 Shopify 视觉
  suitable_project_scene: 科研成果转化平台、设备/服务管理后台、竞赛商业化原型

- project_type: 协作/项目管理/知识库系统
  style_tag: Atlassian/productivity/team-workflow
  layout_type: 侧边项目导航 + issue/list/board 多视图 + 内联编辑 + activity feed
  color_palette: "Atlassian blue #0052CC 体系 / neutral background / status colors"
  font_style: Atlassian-style sans; 高密度但层级清晰
  component_pattern: Lozenge status + Breadcrumb + InlineEdit + EmptyState + Flag + Modal
  interaction_pattern: 快速创建、状态流转、拖拽看板、评论/历史记录
  animation_type: 功能性微动效; 拖拽/状态切换要有明确反馈
  screenshot_reference: https://atlassian.design/
  implementation_notes: 适合“项目进度/实验任务/缺陷跟踪”类系统，状态标签和操作历史要成为一等元素
  suitable_project_scene: 科研项目 PM、实验任务看板、论文返修问题跟踪

- project_type: 开发者工具 / 开源项目门户
  style_tag: Primer/developer/github-like
  layout_type: 顶部 repo 导航 + README 主栏 + 右侧 metadata + tabbed content
  color_palette: "GitHub neutral / blue accent / success-warning-danger semantics"
  font_style: System sans + monospace for code; Markdown 排版优先
  component_pattern: Label + Button + ActionList + Markdown body + Octicon icon + Timeline
  interaction_pattern: issue/PR 式状态流、代码块复制、标签筛选、版本/commit 链接
  animation_type: 几乎无装饰; 交互反馈即时
  screenshot_reference: https://primer.style/
  implementation_notes: 适合技术型作品展示，强调 README 可信度、版本、issue/PR 语义；可与 GitHub Pages/Next.js 结合
  suitable_project_scene: 开源算法库主页、Light 示例项目页、开发者文档站

- project_type: 政务/公共服务/高可信表单系统
  style_tag: USWDS/government/accessibility-first
  layout_type: 顶部官方横幅 + 明确步骤表单 + 内容页分区 + 辅助说明
  color_palette: "USWDS blue / red / gold status; high-contrast neutral"
  font_style: Source Sans / Public Sans 风格; 正文大、行距足
  component_pattern: Step indicator + Alert + Form group + Summary box + Identifier
  interaction_pattern: 表单校验、分步保存、错误集中提示、键盘/读屏可达
  animation_type: 无装饰动效; 可访问性优先
  screenshot_reference: https://designsystem.digital.gov/
  implementation_notes: 用于严肃申报/填报系统时，学习其“明确、可信、少干扰”；WCAG 与错误提示是核心
  suitable_project_scene: 大创/竞赛申报填报系统、伦理审批/数据申请系统

- project_type: 政策/指南/说明文档服务
  style_tag: GOV.UK/content-first/plain-language
  layout_type: 单列内容页 + 明确标题 + inset text/warning + step-by-step guide
  color_palette: "Black/white high contrast + GOV.UK blue accent + warning yellow"
  font_style: 大字号无衬线; 短句、强段落层级
  component_pattern: Back link + Breadcrumb + Details + Inset text + Warning text + Phase banner
  interaction_pattern: 内容折叠、步骤导航、表单错误提示
  animation_type: 基本无; 内容理解优先
  screenshot_reference: https://design-system.service.gov.uk/
  implementation_notes: 适合把复杂科研流程写成“人能一步步照做”的系统；文案比装饰更重要
  suitable_project_scene: 技术文档站、实验复现指南、项目材料提交流程页

- project_type: 移动端/跨平台应用原型
  style_tag: Material-Design-3/mobile/adaptive
  layout_type: top app bar + navigation bar/rail + cards + FAB + responsive pane
  color_palette: "Material dynamic color / primary-secondary-tertiary / surface variants"
  font_style: Roboto/System sans; 中文用思源黑体或系统字体，保持移动端可读
  component_pattern: Material Card + NavigationBar + FAB + Dialog + Snackbar + BottomSheet
  interaction_pattern: 手势、底部导航、状态保存、响应式 navigation rail
  animation_type: Material motion; 页面切换和 shared element 需服务理解
  screenshot_reference: https://m3.material.io/
  implementation_notes: 适合移动端演示和跨端产品原型；注意 48dp 触控目标、暗色模式、动态色别过度炫技
  suitable_project_scene: 移动科研工具、采集 App 原型、项目答辩中的移动端演示
```
