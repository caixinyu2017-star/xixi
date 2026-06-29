# db05 扩展卡 — 风格谱系（玻璃拟态 / 新拟物 / 编辑器极简 / 杂志编辑）

> schema: `project_type, style_tag, layout_type, color_palette, font_style, component_pattern, interaction_pattern, animation_type, screenshot_reference, implementation_notes, suitable_project_scene`
> 核验日期：2026-06-12。下列卡补齐 db05 风格谱系中尚缺的四种视觉范式；每张卡标真实来源链接（curl HTTP 状态见文末核验表）。**只学版式/配色/token 逻辑，不复制受版权素材**（CONVENTIONS §5）。
> 与既有卡的关系：本文件是"按视觉风格"切分（玻璃拟态/新拟物/编辑器极简/杂志编辑）；`design_system_cards.md` 是"按官方设计系统"切分（Carbon/Fluent/Polaris…）；`resources_real.md` Part 2 是"按科研项目场景"切分（大屏/主页/管理系统…）。三者 project_type 互不重复。

```yaml
- project_type: 玻璃拟态数据仪表盘
  style_tag: 玻璃拟态/glassmorphism/半透明层叠
  layout_type: 深色或图像背景 + 多层半透明卡片网格 + 顶部概览条
  color_palette: 背景渐变(深蓝紫 #1E1B4B→#312E81) / 卡面半透明白 rgba(255,255,255,0.08) / 边框高光 rgba(255,255,255,0.18) / 强调青 #22D3EE / 文字 #F1F5F9
  font_style: 无衬线(Inter/思源黑体); 数字稍大, 字重中等避免在模糊层上发虚
  component_pattern: 毛玻璃 KPI 卡 + 半透明侧栏 + 浮层图表卡 + 玻璃按钮/标签
  interaction_pattern: 悬停加深模糊/提升层级 + 卡片轻微视差 + 平滑展开
  animation_type: backdrop-filter 过渡 + 卡片浮起阴影渐变(克制)
  screenshot_reference: https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter （backdrop-filter 规范与示例，技术真相源）
  implementation_notes: CSS `backdrop-filter:blur(12px)` + 半透明背景 + 1px 高光边框; 必须有足够对比的背景图/渐变才出效果; **可读性风险**——正文务必加足够对比度(WCAG AA), 模糊层下避免长段落; 性能上 blur 较吃 GPU, 移动端控制层数
  suitable_project_scene: 监控大屏的现代化皮肤、产品落地页 hero 区、答辩演示的视觉点缀层(非数据密集正文)

- project_type: 新拟物控制面板
  style_tag: 新拟物/neumorphism/软 UI
  layout_type: 单一浅底大面板 + 同色凸起/凹陷控件 + 低密度留白
  color_palette: 同色系底 #E0E5EC / 亮阴影 #FFFFFF / 暗阴影 #A3B1C6 / 单一强调色(克制, 如 #5B7FFF) / 文字 #4A5568
  font_style: 圆润无衬线(Nunito/思源黑体 Medium); 字重偏轻, 配合柔和质感
  component_pattern: 凸起按钮/开关 + 凹陷输入框 + 软卡片 + 圆形图标按钮
  interaction_pattern: 按下时凸→凹切换(inset 阴影) + 悬停微抬起
  animation_type: box-shadow 内外切换过渡; 无强动效
  screenshot_reference: https://neumorphism.io/ （新拟物双向阴影 CSS 生成器，社区事实源）
  implementation_notes: 核心是一对方向相反的 box-shadow(亮+暗)制造"从背景挤出/压入"错觉; 底色与控件必须同色; **可访问性硬伤**——边界靠阴影而非对比, 低视力/强光下几乎不可辨, 故只适合装饰性/轻交互, 关键操作仍需明确对比的控件; 不要整站铺满
  suitable_project_scene: 音乐/IoT 控制类小程序原型、单一功能 App 的播放/调节面板、设计风格 demo; 不用于表单密集的科研管理系统

- project_type: 极简开发者 SaaS(Linear/Vercel 系)
  style_tag: 编辑器极简/developer-minimal/高密度克制
  layout_type: 窄边距 + 命令面板优先 + 左侧极简导航 + 内容区大量留白 + 细分隔线
  color_palette: 近黑底 #0B0B0F 或纯白 #FFFFFF 双主题 / 中性灰阶 #18181B~#A1A1AA / 单一品牌强调(电蓝/品红) / 极细边框 #27272A
  font_style: 几何无衬线(Inter/Geist Sans)标题与正文; 代码用 Geist Mono/JetBrains Mono; 字号层级少而精
  component_pattern: 命令面板(⌘K) + 键盘可达列表 + 内联状态 lozenge + 极简卡片 + Toast
  interaction_pattern: 键盘优先(快捷键/⌘K 搜一切) + 即时反馈 + 乐观更新 + 细腻 hover 态
  animation_type: 极快微动效(150-200ms ease) + 内容淡入; 拒绝花哨
  screenshot_reference: https://linear.app/method （Linear 产品方法与设计语言）; https://vercel.com/geist/introduction （Vercel Geist 设计系统）
  implementation_notes: 学其"少即是多"——克制的中性色 + 单一强调 + 极细边框 + 大留白 + 键盘可达; Next.js + Tailwind + shadcn/ui 易复刻; 命令面板可用 cmdk 库; 暗色为一等公民, 双主题 token 化
  suitable_project_scene: 算法库/工具的产品官网、开发者文档站、科研 SaaS 工具、开源项目主页(技术受众)

- project_type: 杂志编辑式长文/数据叙事
  style_tag: 杂志编辑风/editorial/强排版
  layout_type: 非对称多栏网格 + 大标题压字距 + 图文穿插 + 引文/边注 + 滚动叙事(scrollytelling)
  color_palette: 米白纸感底 #FBFAF7 / 浓墨正文 #1A1A1A / 一个克制点缀色(朱红/靛蓝) / 分隔细线 #D9D6CE
  font_style: 强衬线标题(Playfair/思源宋体)大字号 + 高可读无衬线/衬线正文; 强烈字号对比与字距控制是灵魂
  component_pattern: 通栏大图 + 首字下沉 + 拉引文(pull quote) + 边注/脚注 + 内嵌数据图与图注
  interaction_pattern: 滚动触发图表/段落出现(scrollytelling) + 锚点目录 + 图片渐入
  animation_type: 滚动驱动的渐入/数据图分步揭示(克制, 服务阅读而非炫技)
  screenshot_reference: https://pudding.cool/ （The Pudding 数据叙事范本）; https://www.typewolf.com/ （排版/字体配对参考）
  implementation_notes: 核心是**排版层次**而非组件——字号对比、行长(45-75 字符)、节奏留白; 数据叙事可用 scrollama + D3/Observable Plot; 衬线中文用思源宋体, 注意网页字重渲染; 适合"把研究讲成故事"
  suitable_project_scene: 科研成果科普长文、项目故事页、年度报告 web 版、数据新闻式答辩补充页
```

---

### 核验表（2026-06-12，curl HTTP 状态）

| 来源 | 状态 | 用途 |
|---|---|---|
| https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter | 200 | 玻璃拟态技术真相源 |
| https://neumorphism.io/ | 200 | 新拟物阴影生成器 |
| https://linear.app/method | 200 | 编辑器极简设计语言 |
| https://vercel.com/geist/introduction | 200 | Geist 设计系统 |
| https://pudding.cool/ | 200 | 数据叙事范本 |
| https://www.typewolf.com/ | 200 | 排版/字体配对 |

> 说明：链接经 Bash `curl` 取 HTTP 状态码核实于 2026-06-12 真实可达；本环境未抓取正文，卡内 token/手法为前端通识与各来源公开设计语言的提炼，落地前以来源站当时内容为准。许可——MDN(CC-BY-SA)、Linear/Vercel/The Pudding/Typewolf 为各自版权站点，**仅学版式与 token 逻辑，不复制素材**。
