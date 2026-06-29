# db06 — PPT 设计真实资源库（resources_real）

> 服务 m16(PPT 制作)。**学版式逻辑、配色、视觉层次，最终原创化重绘**(CONVENTIONS §5)。
> 商用/付费模板只学结构与审美，**不直接复制元素用于交付**；免费/开源资源按其许可使用并保留署名。
> 链接核实方式：Bash `curl` 取 HTTP 状态 + GitHub/PyPI API 取许可与星标 + WebSearch 取官方页面（附 URL）。核实日期 2026-06-06。
> ⚠ 许可条款会变动，正式商用前请到对应官网 License/FAQ 页面二次确认；本表"许可"列为速查，非法律意见。
>
> **星标/许可/HTTP 状态是薄缓存快照**(last_checked=2026-06-06,非长期有效)：开源仓星标/许可由 [scripts/resource_signal.py](scripts/resource_signal.py) 实时查 GitHub/PyPI API,冲突信在线、无网回退快照标 stale。许可为合规红线(metropolis=CC-BY-SA-4.0 必须可追溯),以官方 LICENSE 为准。下表快照值(2026-06-06)：Marp(MIT, 11.9k★)、reveal.js(MIT, 71.6k★)、PptxGenJS(MIT, 5.5k★)、mtheme(CC-BY-SA-4.0, 6.8k★)、moloch(CC-BY-SA-4.0, 238★)、python-pptx(MIT, PyPI)；Canva/SlidesMania/Envato curl 403(反爬非失效)、Gamma curl 000(已 WebSearch 核实 https://gamma.app/ 存在),其余模板站 200。

---

## 第一部分 · 真实资源清单（带链接 + 用途 + 许可）

### A. 在线模板站（设计成稿型，学版式为主）

| 资源 | 链接 | 用途 | 许可速查（学版式 / 商用注意） |
|---|---|---|---|
| Canva | https://www.canva.com/presentations/ | 在线拖拽设计，海量演示模板、图标、图库 | 免费版可商用导出；部分 Pro 元素需订阅。模板版式可学，**勿原样套用 Pro 素材交付**。链接核实：curl 返回 403（反爬），浏览器可正常访问 |
| Slidesgo | https://slidesgo.com/ | Google Slides / PPT 免费+付费模板，主题丰富 | 免费模板需**署名 Slidesgo/Freepik**；Premium 订阅免署名。商用看具体授权。FAQ: https://slidesgo.com/faqs ，定价: https://slidesgo.com/pricing |
| SlidesCarnival | https://www.slidescarnival.com/ | 免费 Google Slides / PPT 模板，风格统一 | 多为免费可商用，部分要求署名；以站内每模板说明为准 |
| SlidesMania | https://slidesmania.com/ | 免费 PPT / Google Slides / Canva 模板 | 站方说明个人+商用可免费用、无需署名，但不可转售模板本身；以官方"Can I use these templates"页为准 https://slidesmania.com/questions-powerpoint-google-slides/can-i-use-these-templates （curl 403 反爬，浏览器可访问）|
| SlideModel | https://slidemodel.com/ | 商务图表、信息图、版式素材库（付费为主） | 订阅制商用；学其图表/信息图版式逻辑，元素需自绘 |
| Envato Elements | https://elements.envato.com/presentation-templates | 订阅制海量 PPT/Keynote 模板 | 订阅期内商用授权；退订后需保留授权记录。学版式 |

### B. AI / 在线生成型（出稿快，需原创化打磨）

| 资源 | 链接 | 用途 | 许可速查 |
|---|---|---|---|
| Gamma | https://gamma.app/ | AI 一键生成演示/网页，自动排版 | 免费额度 + 订阅；导出内容归用户。生成稿需**人工校验事实与去模板感** |
| Beautiful.ai | https://www.beautiful.ai/ | AI 智能排版，自适应布局规则 | 订阅制，团队商用。学其"智能版式"约束 |
| Pitch | https://pitch.com/ | 协作式演示，模板+品牌套件 | 免费版 + 付费协作；商用看计划。路演/销售 deck 版式参考 |

### C. 代码 / 开源型（可版本管理，最适合学术与原创化交付）

| 资源 | 链接 | 用途 | 许可速查 |
|---|---|---|---|
| Marp | https://marp.app/ ，源码 https://github.com/marp-team/marp | Markdown 写 PPT，导出 PPTX/PDF/HTML | 开源 MIT（GitHub API 实测，11.9k★）。适合纯文本可控、版本化的学术 slide |
| reveal.js | https://revealjs.com/ ，源码 https://github.com/hakimel/reveal.js | HTML 演示框架，浏览器放映，支持 Markdown | MIT（GitHub API 实测，71.6k★）。强交互/网页型演示，可深度自定义 CSS |
| Beamer + metropolis 主题 | 源码 https://github.com/matze/mtheme （moloch 续作 https://github.com/jolars/moloch） | LaTeX 学术演示，现代极简主题，公式排版强 | 主题代码 **CC-BY-SA-4.0**（README 实测：修改并再分发须保留版权头并以相同协议授权；**不影响你用该主题做出的演示稿**）；moloch 续作同为 CC-BY-SA-4.0。学术答辩/组会首选，内容完全原创可控。GitHub API：mtheme 6.8k★、moloch 238★ |
| python-pptx | 文档 https://python-pptx.readthedocs.io/ ，PyPI https://pypi.org/project/python-pptx/ | Python 程序化生成/批改 PPTX | MIT（PyPI API 实测）。批量出图表页、数据驱动汇报 |
| PptxGenJS | https://gitbrent.github.io/PptxGenJS/ ，源码 https://github.com/gitbrent/PptxGenJS | JS/Node/浏览器端生成 PPTX | MIT（GitHub API 实测，5.5k★）。Web 应用内导出演示 |

### D. 国内模板站（中文场景，注意商用授权）

| 资源 | 链接 | 用途 | 许可速查 |
|---|---|---|---|
| OfficePLUS | https://www.officeplus.cn/ | 微软官方中文模板站，PPT/简历/图示 | 微软官方平台；部分会员模板。商用以站内授权说明为准。curl 200 |
| iSlide | https://www.islide.cc/ | PPT 插件：图示库、主题库、一键设计、补间动画 | 插件免费 + 资源会员制。**学其设计规范（统一字号/配色/对齐）很有价值**。curl 200 |
| 优品PPT (ypppt) | https://www.ypppt.com/ | 免费中文 PPT 模板、图表、字体 | 标注"免费下载"，但**商用须自行核实字体/图片二次授权**，下载页常注明仅学习交流。curl 200 |

> 补充：Behance / Dribbble 的 Presentation 作品、Pinterest PPT board 适合**找灵感与版式参考**，作品受原作者版权保护，**只学不抄**。

---

## 第二部分 · slide_card（db06 字段，场景化版式卡）

> 字段：`scenario, theme_style, page_type, layout_structure, color_palette, font_pairing, visual_hierarchy, chart_style, icon_style, transition_style, speaker_notes_style, reuse_template_notes`
> 以下卡片描述**版式逻辑**，落地时按本场景重绘，不复用任何受版权素材。

```yaml
- scenario: 学术答辩（硕博/毕业设计）
  theme_style: 学术风/浅色高级
  page_type: 封面/目录/研究背景/方法/实验/结果/结论/致谢/QA
  layout_structure: 顶部细标题条 + 左文右图; 方法页用流程框图横向铺开
  color_palette: 白底 + 学校主色(单一) + 深灰文字(#333); 强调色仅一种
  font_pairing: 思源宋体/思源黑体标题 + 思源黑体正文; 英文 Times/Helvetica
  visual_hierarchy: 页标题 > 小标题 > 要点 > 出处; 一页一观点
  chart_style: 复用论文图并放大字号/加粗坐标; 关键结果高亮一处
  icon_style: 统一线性图标(同一线宽)
  transition_style: 淡入, 克制无花哨
  speaker_notes_style: 每页 1-2 句讲稿 + 累计时长标注(总 8-12 min ≈ 10-15 页)
  reuse_template_notes: 推荐 Beamer+metropolis 或 Marp 出稿, 版本可控; 封面/过渡可复用, 内容页按论文章节定制

- scenario: 竞赛路演（互联网+/挑战杯/创业大赛）
  theme_style: 竞赛路演风/科技感(可深色)
  page_type: 封面/痛点/方案/技术壁垒/演示/市场/商业模式/团队/规划/融资
  layout_structure: 全屏大字标题 + 视觉冲击主图 + 单一核心数据高亮
  color_palette: 品牌主色 + 高对比强调色; 深色背景配霓虹/渐变(克制)
  font_pairing: 粗黑体标题 + 无衬线正文; 关键数字超大号(数据先行)
  visual_hierarchy: 核心卖点/数据最大, 弱化细节为脚注
  chart_style: 信息图/增长曲线/对比图, 一页一个论点图
  icon_style: 填充式彩色图标, 与品牌色一致
  transition_style: 动感但不过度(推入/缩放), 全场统一一种
  speaker_notes_style: 按路演节奏分段(钩子→痛点→方案→价值→Ask), 控时 5-7 min
  reuse_template_notes: 强叙事钩子; 参考 Pitch/Canva 路演版式学结构, 元素自绘

- scenario: 项目结题/工作汇报
  theme_style: 浅色高级风/莫兰迪
  page_type: 封面/目录/目标/进展/成果/数据/问题与对策/下一步
  layout_structure: 左侧导航条 + 右侧内容; 成果页用卡片网格
  color_palette: 米白/浅灰底 + 莫兰迪低饱和主色 + 深灰字
  font_pairing: 无衬线统一(思源黑体/微软雅黑), 标题加粗区分层级
  visual_hierarchy: 结论先行 > 支撑数据 > 过程细节
  chart_style: 进度甘特/里程碑时间线 + KPI 卡片
  icon_style: 双色线性图标, 统一圆角
  transition_style: 淡入/轻推
  speaker_notes_style: 每页结论句 + 数据出处; 汇报 10-15 min
  reuse_template_notes: 卡片/时间线可模板化; 参考 OfficePLUS/iSlide 图示库学规范

- scenario: 数据分析汇报
  theme_style: 数据分析风/浅色
  page_type: 封面/概览/方法/分析/洞察/结论/附录
  layout_structure: 图表主导(占 60%+) + 右侧/上方关键结论批注
  color_palette: 中性底 + 一组协调数据色(色盲友好, 4-6 色上限)
  font_pairing: 无衬线统一; 数字用等宽字体对齐
  visual_hierarchy: 图 > 结论批注 > 轴/图例细节
  chart_style: 全套统一调色板, 突出关键序列, 去除冗余网格线(data-ink 原则)
  icon_style: 极简线性, 少用图标避免干扰图表
  transition_style: 淡入, 同类图表用一致出现方式
  speaker_notes_style: 每张图"看什么+得出什么"两句话
  reuse_template_notes: 推荐 python-pptx 批量生成图表页; 图表风格与论文/前端统一(a07)

- scenario: 技术分享/组会汇报
  theme_style: 极简风/科技风
  page_type: 封面/动机/相关工作/核心思路/实验/讨论/QA
  layout_structure: 大留白 + 单点聚焦; 代码/公式页用等宽块居中
  color_palette: 白底或深底二选一 + 一两个强调色
  font_pairing: 无衬线标题 + 正文; 代码用 JetBrains Mono/Consolas
  visual_hierarchy: 一屏一概念, 标题点题 > 图示 > 要点
  chart_style: 示意图/架构图为主, 折线对比为辅
  icon_style: 线性极简, 必要时仅用箭头/框
  transition_style: 无转场或纯淡入(技术场合重内容)
  speaker_notes_style: 口语化讲解锚点 + 易被问处预备 QA
  reuse_template_notes: 推荐 reveal.js/Marp, Markdown 写作可版本管理, 公式用 KaTeX/LaTeX

- scenario: 产品/方案发布
  theme_style: 科技风(深色)/极简
  page_type: 封面/愿景/痛点/产品/功能演示/对比/定价/路线图/CTA
  layout_structure: 全屏主视觉 + 功能页左图右文交替; 对比页用表格/双栏
  color_palette: 深底 + 品牌渐变强调 + 留白; 截图带设备外框
  font_pairing: 现代无衬线(粗细对比强); 标语大号
  visual_hierarchy: 主视觉/标语最大, 功能点分块呈现
  chart_style: 功能对比矩阵 + 简洁增长/采用曲线
  icon_style: 统一填充/描边风格, 与品牌一致
  transition_style: 缩放/推入, 主视觉可加轻微动效
  speaker_notes_style: 演讲式, 每页一个记忆点; 结尾明确 CTA
  reuse_template_notes: 参考 Beautiful.ai/Pitch 发布会版式; 主视觉与功能模块原创设计
```

---

## 合规与原创化清单（交付前自检）

- [ ] 商用/付费模板的具体元素（图标、插画、图库照片）**未原样出现在交付稿**，仅借鉴了版式与配色逻辑。
- [ ] 免费模板若要求署名（如 Slidesgo 免费档）已保留署名，或已确认无需署名。
- [ ] 字体已确认商用授权（思源系/Noto 为 SIL OFL 可商用；中文商用字体需逐一核实）。
- [ ] 图库照片来源合法（自摄/CC0/已购授权），AI 生成稿事实已人工核验。
- [ ] 配色、版式、图标线型在全 deck 内统一，已"去模板感"重绘为原创视觉。
- [ ] 与论文/前端图表风格保持一致(a07)，术语/数据/创新点跨材料一致。

> 待核查：各站"免费可商用"细则随政策变动，正式商用前以官网当时的 License/FAQ 为准。


