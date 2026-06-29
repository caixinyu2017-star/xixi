# db05 — 前端设计真实资源库（resources_real）

> 实测可达、链接真实的前端设计资源清单 + 可落地 design_card。学版式逻辑、用开源组件，**不抄袭**（CONVENTIONS §5）。
> 链接均经 WebSearch 核实存在（核实日期 2026-06-06）。许可信息标注于每条；商用前请以各项目官方 LICENSE/服务条款为准（许可会变更，标 *待核查* 者务必自查）。

---

## Part 1 — 真实可用资源清单

> **许可列是薄缓存快照,非认证事实**(last_checked=2026-06-06)。license/版本会随版本与服务条款变更——
> npm 系工具(见文末「npm 薄缓存映射」)用 `scripts/style_signal.py --npm <包名>` 实时查 registry.npmjs.org,冲突信在线;
> 画廊/SaaS/Figma/Pro 定价层**无 license API**,只存指针指向官方 LICENSE/pricing 页,标 *待核查*、投产前人工核。无网时用快照并标 stale。

### A. 组件库 / UI Kit（可直接写代码）

| 资源 | 链接 | 是什么 | 许可 | 适合的科研/项目场景 |
|---|---|---|---|---|
| shadcn/ui | https://ui.shadcn.com/ | 复制粘贴式 React 组件集合（基于 Radix + Tailwind），非 npm 黑盒，代码进自己仓库可改 | MIT（开源免费，可商用） | 学术主页、管理系统、数据平台——需要高度定制又不想从零写组件 |
| shadcn Blocks | https://ui.shadcn.com/blocks/sidebar | 官方现成区块（侧栏、仪表盘布局等） | MIT | 管理后台/科研数据平台快速搭骨架 |
| Radix UI Primitives | https://www.radix-ui.com/primitives | 无样式、可访问性(a11y)达标的底层组件原语（Dialog/Popover/Tabs 等） | MIT | 任何需要无障碍合规的项目；shadcn 的底座 |
| Material UI (MUI) | https://mui.com/material-ui/ | 实现 Material Design 的成熟 React 组件库，生态完整 | MIT（核心免费；MUI X 高级组件部分商用收费 *待核查具体组件*） | 管理系统、企业级后台、需要大量现成表格/表单的科研工具 |
| Ant Design (antd) | https://ant.design | 企业级 React 组件库，中后台首选，中文文档完善 | MIT（开源可商用） | 科研数据管理系统、软著作品、中后台大屏配套表单 |
| Tremor | https://tremor.so/ | 面向仪表盘/图表的 Tailwind 组件（KPI 卡、图表、表格） | Apache-2.0（npm 包开源可商用；Tremor Blocks 模板另有授权 *待核查*） | 数据分析仪表盘、科研指标看板 |
| Aceternity UI | https://ui.aceternity.com/ | 炫酷动效 React/Next + Tailwind + Framer Motion 组件（背景特效、卡片动画） | 免费组件开源；Aceternity UI **Pro** 模板为付费商用授权（见 https://pro.aceternity.com/licence） | 产品落地页、答辩展示页、需要视觉冲击的项目主页 |
| Magic UI | https://magicui.design | 面向设计工程师的动画组件库，与 shadcn 风格兼容，可复制粘贴 | MIT（开源免费，仓库 https://github.com/magicuidesign/magicui）；Magic UI **Pro** 付费 | 落地页 hero 区、营销/答辩页动效 |

### B. 设计系统配套工具（配色 / 主题）

| 资源 | 链接 | 是什么 | 许可 | 适合场景 |
|---|---|---|---|---|
| tweakcn | https://github.com/jnsahaj/tweakcn | shadcn/ui 可视化主题编辑器（无代码调 token，导出 CSS 变量） | 开源（见仓库 LICENSE *待核查具体协议*） | 快速为科研系统/主页定制一套 shadcn 主题 token |
| Realtime Colors | https://realtimecolors.com/ | 实时预览整套配色落在真实网页上的效果 + 调色板生成器 | 免费工具；开源仓库 https://github.com/juxtopposed/realtimecolors | 定主色/中性/强调色，看真实排版对比度 |
| Coolors | https://coolors.co/ | 极快的配色方案生成器，可锁色、导出 | 免费（含付费 Pro 高级功能）；商用配色本身无版权限制 | 任何项目起步定调色板 |
| Color Palette (Tremor) | https://npm.tremor.so/docs/layout/color-palette | Tremor 内置图表配色规范文档 | Apache-2.0 | 图表系列色统一 |

### C. 数据可视化库（大屏 / 图表）

| 资源 | 链接 | 是什么 | 许可 | 适合场景 |
|---|---|---|---|---|
| Apache ECharts | https://echarts.apache.org/en/feature.html | 功能最全的 JS 图表库，地图/热力/3D/大数据量渲染强 | Apache-2.0（可商用） | 数据大屏、智慧农业监控、竞赛答辩可视化 |
| D3.js | https://d3js.org/what-is-d3 | 底层数据驱动 SVG/Canvas 库，完全自定义可视化 | ISC（可商用，仓库 https://github.com/d3/d3） | 论文图表、定制化/创新型可视化 |
| Recharts | https://recharts.org/ | 基于 React + D3 的声明式图表组件，上手快 | MIT | React 管理系统里的常规图表（折线/柱/饼） |

### D. 设计灵感画廊（看版式，不抄袭）

| 资源 | 链接 | 是什么 | 使用方式 | 适合场景 |
|---|---|---|---|---|
| Awwwards | https://www.awwwards.com/ | 全球获奖网站集，高水准动效/版式 | 仅看版式逻辑与交互，不复制素材 | 落地页、答辩页、项目主页找灵感 |
| Mobbin | https://mobbin.com/ （社媒 https://dribbble.com/mobbindesign 可核实存在） | 海量真实 App/Web UI 截图库，按流程归档 | 看移动端/Web 交互流程 | 移动端 App 演示、产品流程设计 |
| Dribbble | https://dribbble.com/ | 设计师作品社区，UI 概念稿丰富 | 看视觉风格，注意多为概念稿非可落地 | 视觉风格探索、配色参考 |
| Behance | https://www.behance.net/ | Adobe 旗下作品集平台，完整项目案例 | 看完整设计流程与品牌系统 | 品牌/视觉系统、作品集参考 |
| Land-book | https://land-book.com/ （ProductHunt 收录 https://www.producthunt.com/products/land-book） | 精选落地页画廊 | 看落地页结构 | 项目/产品落地页版式 |
| Godly | https://godly.website/ | 精选前沿/实验性网页设计 | 看趋势性视觉 | 前沿风格答辩页、创意主页 |
| Lapa Ninja | https://www.lapa.ninja/ | 落地页设计库 + UI 元素拆解 | 看落地页与组件拆分 | 落地页、营销页 |

### E. 模板 / 设计资源

| 资源 | 链接 | 是什么 | 许可 | 适合场景 |
|---|---|---|---|---|
| Tailwind CSS | https://tailwindcss.com/ | 原子化 CSS 框架，几乎所有上面组件库的样式底座 | MIT | 一切项目的样式层 |
| Vercel Templates (Next.js) | https://vercel.com/templates/next.js | 官方 Next.js 项目模板，一键部署 | 各模板许可不同（多为 MIT/开源 *逐个待核查*） | 学术主页、SaaS 演示、快速起项目 |
| Vercel Templates (Tailwind) | https://vercel.com/templates/tailwind | Tailwind 主题/模板集合 | 同上，逐模板查 | 落地页、博客、作品集 |
| Figma Community | https://www.figma.com/community | 海量免费/付费 Figma 设计文件、UI Kit、图标 | 逐文件看作者授权（CC/免费/付费混杂 *使用前必查*） | 设计稿、组件库 Figma 源文件、交付给前端 |

> 合规提醒：灵感画廊（D 类）只用于**学习版式与交互逻辑**，禁止下载/复制他人素材直接用于自己作品（CONVENTIONS §5）。组件/库（A/C/E 类）以各仓库 LICENSE 为准，商用前确认。

### npm 薄缓存映射（style_signal.py 实时查的输入清单，license 为 2026-06-06 快照）

| 工具 | npm 包名 | license 快照 | flag |
|---|---|---|---|
| shadcn/ui | shadcn | MIT | ok（CLI 工具，组件代码进自己仓库） |
| Radix UI | @radix-ui/react-dialog（系列同协议） | MIT | ok |
| Material UI | @mui/material | MIT | ok（MUI X 高级组件部分收费，*待核查* 具体组件） |
| Ant Design | antd | MIT | ok |
| Tremor | @tremor/react | Apache-2.0 | ok（Blocks 模板另有授权 *待核查*） |
| Magic UI | magicui（仓库 magicuidesign/magicui） | MIT | ok（Pro 付费层无 API *待核查*） |
| Apache ECharts | echarts | Apache-2.0 | ok |
| D3.js | d3 | ISC | ok |
| Recharts | recharts | MIT | ok |
| Tailwind CSS | tailwindcss | MIT | ok |

> 用法：`python scripts/style_signal.py --npm echarts --cached-license Apache-2.0`（查在线 license+最新版本、与快照对比、冲突信在线）。
> 不在表内的（Aceternity/tweakcn/Realtime Colors/Coolors/画廊/Figma/Vercel 模板）无统一 npm 包或无 license API，走 `--url` 存活探测 + 官方 LICENSE 页人工核，定价层恒标 *待核查*。

---

## Part 2 — 可落地 design_card（db05 schema）

> schema：`project_type, style_tag, layout_type, color_palette, font_style, component_pattern, interaction_pattern, animation_type, screenshot_reference, implementation_notes, suitable_project_scene`

```yaml
- project_type: 数据可视化大屏
  style_tag: 科技感/深色/data-screen
  layout_type: 16:9 三栏栅格 + 中央主视图(地图/主图)
  color_palette: 深蓝底 #0A1A2F / 青强调 #2EE6D6 / 橙警示 #FF8A3D / 浅灰文字 #C9D4E0
  font_style: 无衬线; 指标数字用等宽字体(DIN/Roboto Mono), 大号 KPI
  component_pattern: KPI 指标卡 + 实时折线 + 地图热力 + 排行榜 + 滚动列表
  interaction_pattern: 自动轮播 + 悬停明细 tooltip + 定时刷新
  animation_type: 数字滚动(countup) + 渐入 + 光晕脉冲
  screenshot_reference: https://echarts.apache.org/examples/  (地图/热力示例)
  implementation_notes: ECharts 主力 + CSS Grid 布局; 投影/大屏注意对比度与字号; 数据用 WebSocket/轮询。库 license/版本见 Part1 表薄缓存,投产前以 style_signal.py 实时核为准
  suitable_project_scene: 智慧农业监控、竞赛答辩大屏、科研数据中台

- project_type: 学术个人/项目主页
  style_tag: 极简/浅色/minimalist
  layout_type: 单列居中 + 充足留白 + 顶部导航锚点
  color_palette: 白底 #FFFFFF / 深灰文字 #1A1A1A / 单一强调色(如学术蓝 #2563EB)
  font_style: 衬线标题(Lora/Source Serif) + 无衬线正文(Inter); 强字号层次
  component_pattern: 论文列表卡 + 发表时间线 + 顶部导航 + 联系方式区
  interaction_pattern: 平滑滚动 + 锚点高亮 + 论文展开摘要
  animation_type: 克制(fade-in on scroll)
  screenshot_reference: https://vercel.com/templates/next.js  (academic/portfolio 模板)
  implementation_notes: Next.js + Tailwind + shadcn/ui 卡片; 可一键部署 Vercel; tweakcn 调主题色。库 license 见 Part1 薄缓存、实时核为准
  suitable_project_scene: 论文/项目展示、个人作品集、课题组主页

- project_type: 科研数据管理/分析系统
  style_tag: 卡片式/中后台/card
  layout_type: 左侧导航栏 + 顶栏 + 内容区卡片网格
  color_palette: 浅灰底 #F5F7FA / 品牌主色 #1677FF / 状态色(成功#52C41A 警告#FAAD14 危险#FF4D4F)
  font_style: 无衬线(Inter/思源黑体); 表格密排, 中性字重
  component_pattern: 侧导航 + 数据表(可筛选/排序/分页) + 筛选器 + 图表卡 + 模态框/抽屉
  interaction_pattern: 筛选/排序/分页 + 表单即时校验反馈 + 批量操作确认
  animation_type: 克制(抽屉滑入/loading 骨架屏)
  screenshot_reference: https://ui.shadcn.com/blocks/sidebar  (官方侧栏布局区块)
  implementation_notes: Ant Design 或 shadcn/ui + Recharts/ECharts; 主题 token 化; 表格用虚拟滚动应对大数据。库 license 见 Part1 薄缓存、实时核为准
  suitable_project_scene: 科研数据平台、实验管理系统、软著系统类作品

- project_type: 智慧农业监测平台
  style_tag: 农业智慧化/绿色系/agri-tech
  layout_type: 顶栏 + 地图主视图(地块/物联网点位) + 右侧数据面板
  color_palette: 自然绿主色 #2E7D32 / 浅绿辅 #A5D6A7 / 土棕中性 #8D6E63 / 数据强调橙 #FB8C00
  font_style: 无衬线(圆润字体增亲和力); 数据区等宽数字
  component_pattern: 地图/卫星图 + 传感器实时卡(温湿度/土壤) + 趋势折线 + 告警列表 + 设备状态
  interaction_pattern: 地块点击下钻 + 时间轴回放 + 阈值告警高亮
  animation_type: 数据渐变过渡 + 告警闪烁(克制)
  screenshot_reference: https://echarts.apache.org/examples/  (geo/effectScatter 地图点位)
  implementation_notes: ECharts(地图+折线) + Tailwind 绿色调色板(Realtime Colors 验证对比度); 注意户外强光下可读性, 提供深色备选主题
  suitable_project_scene: 智慧农业课题、物联网监测、农业 IoT 答辩演示 · domain_scope=agri-tech

- project_type: 移动端 App 演示页
  style_tag: 移动端/mobile/拇指可达
  layout_type: 单列竖屏 + 顶部状态区 + 底部 Tab 导航
  color_palette: 浅底 #FAFAFA / 品牌主色 + 强调色; 高对比可达 WCAG AA
  font_style: 无衬线大字号(可点击区 ≥44px); 层次靠字号+字重
  component_pattern: 底部 Tab 栏 + 卡片流 + 下拉刷新 + 悬浮操作按钮(FAB) + 表单
  interaction_pattern: 手势滑动 + 下拉刷新 + 触底加载 + 触觉反馈
  animation_type: 页面切换过渡 + 微交互(按钮按压/点赞)
  screenshot_reference: https://dribbble.com/mobbindesign  (Mobbin 真实 App UI 流程, 仅学习版式)
  implementation_notes: Tailwind + shadcn/ui(响应式) 或 MUI; 移动栅格 4/8pt; 触控目标 ≥44px; 参考 Mobbin 真实流程, 不照搬素材
  suitable_project_scene: App 原型演示、移动端产品答辩、小程序设计参考

- project_type: 产品/项目落地页(答辩用)
  style_tag: 科技感+动效/landing
  layout_type: 全宽分段(hero + 特性 + 数据 + CTA)纵向滚动
  color_palette: 深色 hero #0B0F1A / 渐变强调(紫青 #7C3AED→#2EE6D6) / 浅区交替
  font_style: 大号无衬线标题(粗字重) + 常规正文; 强对比
  component_pattern: 全屏 hero + 特性卡网格 + 数据指标条 + 时间线 + CTA 按钮
  interaction_pattern: 滚动触发动画(scroll-reveal) + 悬停高亮 + 视差
  animation_type: Framer Motion 进场动画 + 背景粒子/光效
  screenshot_reference: https://ui.aceternity.com/components  (动效组件参考)
  implementation_notes: Next.js + Tailwind + Aceternity UI(免费组件)/Magic UI 动效; Pro 模板商用需购授权(定价无 API,见官方 pricing 页人工核); 动效克制避免喧宾夺主。库 license 见 Part1 薄缓存、实时核为准
  suitable_project_scene: 课题成果落地页、竞赛答辩首页、开源项目主页
```

## 待补充
按用户具体项目主题继续补充风格卡，沉淀可复用的设计 token（色/字/间距/圆角），由 a07 跨材料统一。

---

### 核实说明
- 全部链接经 WebSearch 核实于 2026-06-06 真实存在（搜索仅返回标题+URL，URL 已核对）。
- 许可信息：MIT/Apache-2.0/ISC 等开源协议来自各项目官方仓库的常识性事实；标 *待核查* 者为可能随版本/服务条款变更或需逐文件确认的项（如 Figma Community 单文件授权、Vercel 单模板授权、MUI X 高级组件、各 Pro 付费层），商用前以官方 LICENSE/服务条款为准。
- 本环境 WebFetch 全域被拦截，未抓取正文；链接有效性以 WebSearch 返回的 URL 为依据。

