# light-slides — 深度分析与同类对标

> 源：[`skills/light-slides/SKILL.md`](../../../skills/light-slides/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：以 python-pptx 程序化出可编辑 PPTX 为首选路线、自带 10 主题色板 + 9 套版式片段 + 端到端 demo + 无 soffice 也能跑的视觉/内容 QA 的科研汇报幻灯片技能，强学术叙事方法论(行动式标题/幽灵 deck)并对 AI 生图划三条硬红线。

## 核心运行逻辑
SKILL.md 把"出 PPT"拆成先定三件事(场景受众/叙事骨架/视觉风格)再程序化落页:视觉风格从 db06 选主题、能取 db09 项目 palette.json 则强制复用以保证与论文图(m11)/前端(a05)同色。实现以 python-pptx 为唯一自带可运行路线(其余 PptxGenJS/Marp/reveal/Beamer/海报/Paper2Slides 仅在 references.md 做选型笔记),数据图一律走 m11/m06 真数据、严禁生成式模型画数据图或论文图、文本一律落原生文本框三条红线贯穿。学术专项把 action title 与 ghost deck test 固化进 build_deck.py 的代码与自检。QA 设计为"默认有 bug",thumbnail.py 在无 LibreOffice 时用 PIL 读 python-pptx 几何画版式示意图,to_pdf.py 缺引擎时明确报 unavailable 不假装成功——整体偏环境健壮、诚实降级。

## 关键步骤
- 1. 先定三件事:场景与受众(答辩/路演/汇报)→叙事骨架三选一(SCR/漏斗+答案/答案先行)→每页一个核心信息列大纲
- 2. 选视觉风格:从 db06 取主题(get_theme),有 db09 palette.json 则必用其取色,定色板+字体配对
- 3. 用 patterns.md 片段或 examples/build_deck.py 程序化出页:fill_bg 铺底+accent 色块代下划线+margin=0 对齐+行动式标题
- 4. 逐页配 speaker notes(1-2句+时长+必讲/可略),控制总页数匹配时长
- 5. 内容 QA:markitdown 查缺漏 + grep 抓 lorem/ipsum/xxxx 残留占位符
- 6. 视觉 QA:thumbnail.py 出缩略图网格逐页扫,有 soffice 则 to_pdf.py 转 PDF 高保真校验,改完只重渲受影响页
- 7. 交付前过 a08(light-self-review)闸门,风格与版本登记 db06/db09

## 自带资产
- SKILL.md:主流程与路线/边界/排版尺度/学术专项/QA/衔接的总纲
- assets/themes.py:db06 十大主题的 COLORS(8字段)/FONTS 常量+get_theme/list_themes,dataviz 带 Okabe-Ito 色盲友好序列,带 __main__ 自检
- patterns.md:9 套可直接跑的 python-pptx 版式片段(封面/目录/过渡/内容/结果左图右解读/对比高亮表/时间线/结论/References)+fill_bg/add_text/rect 共用函数+讲稿导出片段
- examples/build_deck.py:端到端生成 5 页学术 pptx(封面/内容/结果/对比/References)每页配 notes,内置 ghost_deck_test,无外部数据可跑
- scripts/thumbnail.py:pptx→缩略图网格视觉 QA,soffice 像素渲染优先、无则 PIL 几何版式示意回退,带 --selftest
- scripts/to_pdf.py:pptx→pdf 的 soffice 无头封装,缺引擎明确报 unavailable+安装指引,带 --check/--selftest
- references.md:14 类工具(Anthropic PPTX/academic-pptx/两支 paper2slides/LaTeX海报/python-pptx/PptxGenJS/Marp/reveal/Beamer/Canva/Gamma/Beautiful.ai/Slidesgo/飞书)的真实端点/参数/坑逐条研究笔记

## 优点
- 自带资产真能跑且带自检:themes.py/thumbnail.py/to_pdf.py 都有 __main__ 或 --selftest,build_deck 无外部数据即可端到端出 pptx,不是只讲方法的空壳
- 环境健壮+诚实降级是亮点:thumbnail 无 LibreOffice 时用 PIL 读几何画版式示意图照样能抓重叠/空页,to_pdf 缺引擎明确报 unavailable 并给安装指引,绝不静默假成功——比多数依赖 soffice 的方案可用性强
- 10 主题色板用统一 8 字段 schema(bg/surface/primary/secondary/accent/text/muted/line),便于 patterns/build_deck 机械复用;dataviz 额外给 Okabe-Ito 色盲友好序列,有可访问性意识
- 学术方法论落到代码:action title 与 ghost deck test 不只是口号,ghost_deck_test() 真抽每页标题连读;patterns 把'结果页左图右so-what''对比页高亮本方法列''以Conclusions收尾不写ThankYou'都给了片段
- 对科研诚信的红线清晰且互引:数据图走 m11/m06 真数据、严禁 AI 画数据图/论文图、文本不烤进图片三条,且与 m11 figure_integrity 双向指认 Nature/Science/Elsevier 禁令,适配顶刊语境
- 真实 python-pptx 工程细节到位:margin=0 才能与形状对齐、用 accent 色块替代 AI 味下划线、fill_bg 用全幅矩形 insert(2) 沉底层绕过无原生页背景、shadow.inherit=False 去默认阴影,这些都是踩过坑才有的写法

## 缺点 / 可被质疑处
- CJK 字体很可能不生效(核心隐患):add_text 只设 r.font.name,python-pptx 仅写 latin typeface,不设 run 的 <a:ea> 东亚字体属性;themes 里 Source Han/微软雅黑 等中文字体对中文字符大概率不被应用,渲染机回退到默认黑体——对一个中文优先的技能这是正确性 bug,且 SKILL 只提'建议嵌入字体'却无任何设 ea 或嵌字体的代码
- 原生图表不套主题色,破坏'审美统一'承诺:results_slide 用 python-pptx chart 但只设 has_title/has_legend,完全没把 series 改成 t['COLORS'] 或 Okabe-Ito 序列,图表沿用 Office 默认蓝橙灰,与封面/版式的主题色和 db09 palette SSOT 直接矛盾;patterns 仅提了 vary_by_categories 单序列高亮,没有把'图表配色=主题色'做成 helper
- demo 与技能自定规则自相矛盾:SKILL 反复强调'以 Conclusions 收尾而非 Thank You',但 build_deck 的 5 页恰恰止于 References、根本没有 Conclusions 页;patterns 有 9 套版式而 demo 只演了 5 套(缺目录/过渡/时间线/结论),最该示范的收尾页缺席
- pillow 回退的文字溢出检测被夸大:render_slides_pillow 把文字按 maxc=(right-left)//7 字符硬截断且单行不换行,框内文字超长会被裁掉而非画出,所以'足以抓溢出'对文字溢出其实抓不到(只能看色块重叠);无 soffice 时真正的文字溢出/压行 QA 形同虚设
- references.md 大半不可在环境内执行:Canva 需 Enterprise、Gamma 按 credit 付费、两支 paper2slides 需各自 conda/API key 且无任何 bundled wrapper/glue,'从论文一键转稿'是纯概念描述,用户照着仍要从零搭;研究笔记价值高但与'自带可运行资产'落差大
- 缺关键链路的版式与脚本:patterns 通篇没有 add_picture 导入 m11 成品图+页内引用+caption 的片段(结果页强调复用论文图却只给了原生 chart);没有从 CSV/真数据出图的 helper(与'走真数据'的红线脱节);没有按 notes 时长标记汇总估算总时长的脚本(SKILL 强调页数匹配时长却无工具);无 requirements.txt/版本钉死,图片/形状无 altText(可访问性)

## 可优化点（供后续逐技能优化）
- 加 CJK 字体 helper:用 lxml 给每个 run 的 rPr 写 <a:ea typeface> 和 <a:cs>,把 themes 的中文字体真正应用到中文字符;并补一段'交付前嵌入字体'的说明或退而求其次锁定随 Office 分发的微软雅黑,消除回退风险
- 做 style_chart(chart, theme) helper:按 t['COLORS']['series']/Okabe-Ito 给每个 series.format.fill 上色、统一坐标轴/字号/网格线,接进 results 片段与 build_deck,让图表配色与主题和 db09 palette 一致
- 修 demo 一致性:给 build_deck 补 conclusions_slide 并以它收尾(对齐 SKILL 规则),再补 toc/transition/timeline 三个 builder 把 9 套版式全演一遍,可加 --pages 选择子集
- 补两个缺失链路片段:①add_picture 导入 m11 成品图 + 页内 [k] 引用 + 适配投影(轴标≥16pt)的结果页变体;②from_csv 读真数据出 chart 的 helper,落实'真数据出图'红线
- 强化 pillow 回退的溢出检测:用 ImageFont.getlength 测量+按框宽换行实际绘制,文字超出框高时画红框告警,把'抓溢出'从口号变成真能力;或在无 soffice 时显式提示'文字溢出需 soffice 复核'
- 补工程化收尾:加 requirements.txt 钉死 python-pptx/Pillow(+可选 PyMuPDF);加 pacing.py 解析每页 notes 里 30s/1min 标记汇总总时长并对比目标分钟数告警;给 add_picture/add_table 设 altText,加一个对比度自检 helper
- 给 references.md 的闭源/需付费/需独立环境工具加可执行性分级标注(可调API vs 仅借工作流思路),并为 paper2slides 至少提供一个薄 wrapper 或明确'本环境不集成,仅参考'的边界,缩小与自带资产的落差

## 与其他 Light 技能/知识库的衔接
内容来自 m07(论文正文)/m06(结果),图表来自 m11(light-figure-drawing,且与其 references/figure_integrity.md 的 AI 生图政策双向互引划红线),竞赛路演来自 m17;视觉风格与 a05(前端)/m11 协调、由 a07 统一术语与指标;文件解析借 a01;工具选型走 a09(含 anthropics/skills 的 pptxgenjs.md JS 路线,本 skill 不带 JS 资产);风格与版本登记 db06(十大主题注册表)/db09(projects/<name>/palette.json 视觉 SSOT,与论文图/前端共享同一取色源);交付前过 a08(light-self-review)自检闸门。

---

## GitHub 同类前沿技能对标

> 补跑日期 2026-06-13（原 workflow 结果仅 1 项且 summary 异常，单独补检索）。star/更新时间经 GitHub API 实测。

Light 的 light-slides 在这条赛道里属于"程序化、可编辑、学术叙事强约束"的小众精品路线，而 GitHub 上的热门同类大致分四派：(1) **渲染框架派**(reveal.js/slidev/marp)——代码即幻灯片，生态成熟、star 极高，但产出是 HTML/网页而非原生可编辑 .pptx，且不含学术叙事方法论；(2) **底层库派**(python-pptx/PptxGenJS)——Light 本身就站在 python-pptx 之上，它们只提供 API 不提供主题/版式/QA/叙事；(3) **AI 生成派**(presenton/PPTAgent/slide-deck-ai)——一句话端到端出片，主打"快"和"通用美观"，但内容真实性弱、容易把文字烤进图、模板审美趋同；(4) **论文转片派**(HKUDS/Paper2Slides、OpenDCAI/Paper2Any、Auto-Slides、paper2slides)——专攻 paper→deck，与 Light 场景最贴近。Light 的差异化在于它不是"生成器"而是"方法论+可复现脚手架"：强制 action title、ghost deck 幽灵测试、数据图走真实数据、文本一律原生文本框、不依赖 LibreOffice 的视觉/内容 QA——这些正是 AI 生成派和论文转片派普遍欠缺的工程化与学术严谨性。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 官方 Agent Skills 仓库，含 pptx skill(读/生成/编辑 PPTX) | 150005 | 2026-06-13 | 强：官方背书、生态规范、海量集成。弱：pptx skill 是通用能力，无学术叙事方法论、无 10 主题/9 版式、无"真实数据图+原生文本框"硬约束 |
| [icip-cas/PPTAgent](https://github.com/icip-cas/PPTAgent) | 多智能体反思式 PPT 生成框架(含 PPTEval 评测) | 4640 | 2026-06-08 | 强：学术化自动评测 PPTEval、agentic 自我反思、含 MCP。弱：依赖参考模板做编辑式生成，可控/可复现不如纯脚本，易受 LLM 内容失真影响 |
| [presenton/presenton](https://github.com/presenton/presenton) | 开源 AI 演示生成器+API(对标 Gamma)，可自托管 | 8140 | 2026-06-12 | 强：端到端产品化、API 化、出片快。弱：面向通用商务美观而非学术严谨，数据图真实性无保障，叙事方法论缺失 |
| [gitbrent/PptxGenJS](https://github.com/gitbrent/PptxGenJS) | 用 JS/TS 程序化生成 .pptx | 5596 | 2026-06-12 | 强：JS 生态、浏览器端可跑、原生可编辑 pptx。弱：与 python-pptx 同为底层库，无主题/版式/QA/叙事，语言不同于 Light 的 Python 路线 |
| [slidevjs/slidev](https://github.com/slidevjs/slidev) | 面向开发者的 Markdown→网页幻灯片框架 | 47143 | 2026-06-03 | 强：开发者体验极佳、动效/代码高亮强。弱：产出网页非原生可编辑 pptx，答辩/投稿常需 pptx；无学术叙事强约束 |
| [hakimel/reveal.js](https://github.com/hakimel/reveal.js) | 经典 HTML 演示框架 | 71681 | 2026-05-21 | 强：最成熟稳定、star 最高、插件丰富。弱：HTML 非 pptx，纯展示框架不含内容生成/叙事/QA |
| [marp-team/marp](https://github.com/marp-team/marp) | Markdown 演示生态(CLI 可导出 PDF/PPTX/HTML) | 11954 | 2026-05-01 | 强：Markdown 极简、可导出 pptx、CLI 化。弱：导出 pptx 多为图片式不可深编，主题定制弱，无学术叙事与数据真实性约束 |
| [HKUDS/Paper2Slides](https://github.com/HKUDS/Paper2Slides) | 一键把论文转成演示(agentic) | 3722 | 2026-06-13 | 强：专攻 paper→deck、热度高、迭代快、场景最贴。弱：LLM 端到端易内容失真/文字进图，可控与可复现弱于脚本化 |
| [scanny/python-pptx](https://github.com/scanny/python-pptx) | Python 创建/编辑 OOXML PowerPoint | 3415 | 2026-06-11 | 强：Light 的底层依赖、原生可编辑、最权威。弱：纯库，无主题/版式/叙事/QA/demo——Light 正是在其之上补这一层 |
| [OpenDCAI/Paper2Any](https://github.com/OpenDCAI/Paper2Any) | 把论文/文本/主题转成可编辑图表、路线图与幻灯片(LangGraph) | 2599 | 2026-06-13 | 强：强调"editable pptx"、还能出科研图与路线图、活跃。弱：仍是 LLM 生成，图文真实性靠模型，无 ghost deck 类方法论 |
| [Westlake-AGI-Lab/Auto-Slides](https://github.com/Westlake-AGI-Lab/Auto-Slides) | ICME 2026 交互式多智能体科研演示生成系统 | 514 | 2026-06-12 | 强：顶会背书、交互式定制、专注 research presentation。弱：体量小、依赖 LLM 管线，工程化 QA 与可复现脚手架不如 Light 显式 |
| [barun-saha/slide-deck-ai](https://github.com/barun-saha/slide-deck-ai) | 与 AI 协同共创 PPTX(多模型，Streamlit) | 360 | 2026-06-06 | 强：多模型广、有 UI、可对话迭代。弱：通用场景、内容真实性弱、无学术叙事与真实数据图约束 |
| [takashiishida/paper2slides](https://github.com/takashiishida/paper2slides) | 用 LLM 把任意 arXiv 论文转成幻灯片 | 88 | 2026-06-06 | 强：轻量、聚焦 arXiv、prompt 清晰。弱：体量小、Beamer/LLM 路线，内容真实性与可控性弱于 Light 脚本化 |

### Light 该技能可借鉴的点
- 借鉴 PPTAgent 的 **PPTEval 自动评测思路**：把视觉/内容 QA 升级为可打分维度(内容/设计/连贯性)，让"幽灵测试"从人工检查变成可量化、可回归的指标
- 借鉴 presenton/Paper2Any 的 **API/批处理化**：暴露稳定的生成 API 或 CLI，支持"一份配置→整套 deck"的批量与 CI 集成，同时保持原生可编辑 pptx 输出
- 借鉴 paper2slides 系列的 **论文自动抽取前端**：在保持"真实数据图+原生文本框"硬约束下，加一个可选的 arXiv/PDF 结构化抽取层，把章节/图表/公式喂给版式片段，降低人工填充成本
- 借鉴 slidev/reveal.js 的 **主题/版式生态化**：把 10 主题 + 9 版式做成可插拔、可社区扩展的主题包格式，而非内置固定集合
- 反向坚守差异化护城河：前沿项目几乎都吃了"LLM 把文字烤进图、内容失真、模板审美趋同"的亏——Light 的 action title 强约束、数据图走真实数据、文本原生化、离线 QA 正是它们缺的，应作为卖点显式文档化
- 可考虑做 **anthropics/skills 风格的 skill 封装**，蹭官方 skills 生态分发渠道，同时保留方法论内核
