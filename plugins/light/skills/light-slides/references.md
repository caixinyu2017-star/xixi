# light-slides 参考工具研究笔记

逐工具核查笔记。每项含【是什么】【可复用方法/真实端点/参数】【链接】【已知坑/局限】。
研究日期 2026-06；端点与参数以官方文档为准，使用前请复核版本。

## PPTX skill (Anthropic)

【是什么】Anthropic 官方 Agent Skill，凡涉及 .pptx（读/写/改/合并/拆分/模板）都触发。两条主路径：从模板编辑、从零创建。

【可复用方法/真实流程】
- 读内容：`python -m markitdown presentation.pptx`（文本提取）；缩略图总览 `python scripts/thumbnail.py xx.pptx`；拆 XML `python scripts/office/unpack.py xx.pptx unpacked/`。
- 模板编辑 7 步：thumbnail+markitdown 分析 → 规划版式映射(强制多样化版式) → unpack → 结构改动(改 `ppt/presentation.xml` 的 `<p:sldIdLst>` 删/复制/重排，复制用 `add_slide.py` 别手抄) → 逐 `slideN.xml` 改文字(可并行子代理) → `clean.py` 清孤儿 → `pack.py … --original` 回封校验。
- 从零创建：用 PptxGenJS（见下）。
- 转图做视觉 QA：`python scripts/office/soffice.py --headless --convert-to pdf out.pptx` 然后 `pdftoppm -jpeg -r 150 out.pdf slide`。
- 设计准则（直接可抄）：一个主色占 60–70% 视觉权重 + 1–2 辅色 + 1 个尖锐强调色；深色用于封面/结论、浅色用于内容(三明治结构)；锁定一个重复视觉母题(圆角图框/色环图标/单边粗边)。每页必须有视觉元素，禁止纯文字页。正文左对齐、只标题居中。标题 36–44pt、节标题 20–24pt、正文 14–16pt、注释 10–12pt。页边距≥0.5"，块间距统一 0.3" 或 0.5"。
- 明确禁忌：标题下不要加装饰下划线(AI 味标志)；不要每页同一版式；不要正文居中；不默认蓝色；文本框设 `margin:0` 才能与形状对齐。
- QA 强制：先假设有错当 bug 猎。内容 QA 用 markitdown + grep 残留占位符 `grep -iE "xxxx|lorem|ipsum"`；视觉 QA 必须用子代理(新鲜眼睛)逐图找重叠/溢出/低对比/对齐/边距问题；改完重渲染受影响页，循环到整轮无新问题才收。

【链接】https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md ；editing.md / pptxgenjs.md 同目录。

【已知坑/局限】专有许可(Proprietary)，只能学方法不能直接照搬其脚本进商用。依赖 markitdown、Pillow、pptxgenjs、LibreOffice、Poppler。

## Scientific / Academic Slides skill（academic-pptx）

【是什么】社区 Claude Skill（Gabberflast/academic-pptx-skill），专管学术汇报的**内容与结构**，技术实现仍交给 Anthropic PPTX skill。两层协作：内容层(本 skill) + 技术层(pptx skill)，建议都读。

【可复用方法/评审维度】
- 第一步定模式：默认"结构化论证"(会议/答辩/基金)，优先级 论证结构 > 数据 > 版式 > 美学；面向大众科普才切"视觉/叙事"模式。
- **Action title（行动式标题）**：每页标题是陈述结论的完整句子，不是话题标签。例：不写"Results"，写"三个队列中处理效应均显著"。
- **Ghost deck test（幽灵 deck 测试）**：只读所有标题连起来，应能讲完整个论证；不行就先改大纲再做页。
- 叙事骨架三选一：SCR(情境-冲突-解决) / 漏斗+答案(背景→缺口→方法→发现→意义) / 答案先行(给时间紧的评委)。
- 一份报告只讲一个论点，其余进附录；每页只一个职责、一个 exhibit(图/表/式/图示)。
- Exhibit 纪律：图放左、解读 bullet 放右(左→右阅读)；在图上直接标注关键发现(箭头/高亮区/"↑23%"标注/焦点序列变色)；结果优先用图不用表；从论文重画图(放大轴标≥16pt)别直接贴 PDF 图。
- 正文≤~40 词/页。
- 学术配色：白底；单一无衬线字体；最多三色(主 navy `1F4E79` + 辅 `2E75B6` + 强调)；无装饰图标/渐变/标题下划线。
- 学术 QA 清单：每页有 action title □ ghost deck 通过 □ 每结果页一图且有"so what"标注 □ 借用图/数据有页内引用 □ 末尾有 References 页 □ 以 Conclusions 收尾(不是"Thank You"/空白) □ 末页留联系方式/二维码 □ 正文≥20pt □ 无空装饰元素 □ >15 页有分节导航。

【链接】https://github.com/Gabberflast/academic-pptx-skill （SKILL.md / content_guidelines.md / slide_patterns.md）

【已知坑/局限】专有许可。只是内容指南，不含渲染代码；技术实现依赖 PPTX skill 全套依赖。

## paper-slides / Paper2Slides（HKUDS）

【是什么】HKUDS/Paper2Slides，开源(MIT)，一条命令把论文/报告/文档转成幻灯片或海报。RAG 驱动、保持来源可溯。

【可复用方法/pipeline】
- 4 阶段流水线 + checkpoint 断点续跑：RAG(解析+建检索索引→`checkpoint_rag.json`) → Analysis(抽结构/图/表/层级→`checkpoint_summary.json`) → Planning(生成版式与组织蓝图→`checkpoint_plan.json`) → Creation(渲染成品)。
- 关键 CLI：`python -m paper2slides --input paper.pdf --output slides --style academic --length medium --fast --parallel 2`。
- 参数借鉴：`--output slides|poster`；`--length short|medium|long`；`--density sparse|medium|dense`(海报)；`--style academic|doraemon|自然语言自定义`；`--fast` 跳过 RAG 直接喂 LLM(短文档/快速预览)；`--from-stage rag|summary|plan|generate` 强制从某阶段重跑(只换风格用 `--from-stage plan`，重渲图用 `generate`)。
- 可借鉴思路：源链接可溯(content 与原文对应，防信息漂移)；自定义风格用一段自然语言描述(色调/角色/氛围)而非选模板。

【链接】https://github.com/HKUDS/Paper2Slides ；示例 https://arxiv.org/abs/2512.02556

【已知坑/局限】需 Python 3.12 + conda + API keys(.env)；normal 模式 RAG 索引慢(长文/多图才值)；本身是独立工具，集成时主要借其"RAG→分析→规划→渲染 + 断点"分阶段思路。
【图像生成实测教训(可直接抄进 prompt 策略)】用逐张单图调用而非多图一次出(多图原生输出会"故事化"、风格不一致)；prompt 里给细粒度元素样式 grounding 差，给版式/布局指令更有效；简单 prompt 反而比堆细节的复杂 prompt 出图更好。

## paper2slides（takashiishida，Beamer 路线，与 HKUDS 不同的另一支）

【是什么】takashiishida/paper2slides，把 arXiv 论文(LaTeX 源)用 LLM 转成 **Beamer** 幻灯片 PDF。核心理念：把任务当"摘要练习"——长 LaTeX 论文压成简洁 Beamer LaTeX，全程不出 LaTeX 生态。与 HKUDS 的"图像渲染"路线互补：这条更适合公式/引用密集的硬核论文。

【可复用方法/6 步 pipeline】① 按 arXiv ID 下载 LaTeX 源；② flatten——找主 `.tex`、把所有 `\input` 合并成 `FLATTENED.tex`(用 arxiv-to-prompt)，剥注释与附录；③ 拼 prompt——flattened + `ADDITIONAL.tex`(宏包/`\newcommand`) + 造稿指令，YAML 管理(`prompts/config.yaml`)；④ LLM(GPT-4.1)生成 Beamer，再跑一遍自检/修订 pass；⑤ 可选 `chktex` lint 把告警喂回 LLM 继续修；⑥ `pdflatex` 编译，可选 `pdfcrop` 裁边。Streamlit 提供交互式编辑 UI。

【链接】https://github.com/takashiishida/paper2slides ；https://github.com/takashiishida/arxiv-to-prompt

【已知坑/局限】图只靠 caption 推断(无视觉模型)，复杂图表表现差；首轮生成常有问题、靠自检+lint 循环救；内容发往 OpenAI 有隐私/IP 风险；需本地 `pdflatex`；高度定制/非常规的论文易编译报错；分享前须遵守每篇论文各自许可。

## LaTeX Posters（beamerposter / tikzposter / a0poster）

【是什么】用 LaTeX 出印刷级科研海报，矢量文本任意缩放清晰。

【可复用方法】
- beamerposter：`\documentclass[final]{beamer}` + `\usepackage[orientation=portrait,size=a0,scale=1.4]{beamerposter}`；沿用 beamer 的 `columns`/`block` 排版；options：`orientation=landscape|portrait`、`size=a0..a4|custom`、`scale=数字`(字号缩放)。
- tikzposter：独立文档类 `\documentclass{tikzposter}`，用 `\block{标题}{正文}` 摆内容，theme 更现代。
- a0poster：最轻量的大幅面类。
- 尺寸/DPI：A0 = 841×1189mm(33.1×46.8in)；照片元素 150 DPI 够(观看距离 1–2m)，矢量文字/图无所谓 DPI；200–250 DPI 折中，300 DPI 文件巨大。

【链接】https://www.overleaf.com/learn/latex/Posters ；https://ctan.org/pkg/beamerposter ；https://github.com/deselaers/latex-beamerposter ；https://ctan.org/pkg/a0poster

【已知坑/局限】学习曲线陡；图文混排微调繁琐；适合公式/参考文献多的硬核学术海报，不适合强视觉营销海报。

## PPTX Posters

【是什么】用 PowerPoint/python-pptx/PptxGenJS 做单页超大画布海报(设置幻灯片尺寸=A0)，比 LaTeX 易上手、好协作改图。

【可复用方法】
- python-pptx 设大画布：`prs.slide_width=Inches(33.1)`、`prs.slide_height=Inches(46.8)`(A0 竖版)，全部用一页 + 文本框/图片/形状自由摆放。
- 走 PPTX skill 全套(thumbnail/markitdown/soffice 转 PDF 校验)；导出印刷 PDF 注意嵌入字体、图片≥150–300 DPI。
- 取舍：易改、模板多、非技术同事能协作；公式排版与跨机字体一致性弱于 LaTeX。

【链接】https://python-pptx.readthedocs.io/ ；尺寸参考同上 A0。

【已知坑/局限】无原生 A0 模板需手动设尺寸；字体未嵌入会在打印店错位；大图易让文件膨胀。

## python-pptx

【是什么】Python 库，程序化读写 .pptx（无需安装 PowerPoint）。

【可复用方法/核心 API】
- 骨架：`from pptx import Presentation`；`prs=Presentation()`(或传模板路径)；`slide=prs.slides.add_slide(prs.slide_layouts[idx])`；`prs.save("out.pptx")`。
- 版式索引惯例：0 标题页、1 标题+内容、5 仅标题、6 空白(随模板而变，先枚举确认)。
- 占位符：`slide.placeholders[idx]`；`slide.shapes.title.text="..."`；正文 `tf=placeholder.text_frame; tf.text=...; p=tf.add_paragraph(); p.text=...; p.level=1`。
- 自由元素：`slide.shapes.add_textbox(left,top,width,height)`、`add_picture(path,left,top,width,height)`、`add_table(rows,cols,...)`、`add_chart(...)`。
- 尺寸单位：`from pptx.util import Inches, Pt, Emu`；颜色 `from pptx.dml.color import RGBColor`；`RGBColor(0x1F,0x4E,0x79)`。
- 字号 `run.font.size=Pt(24)`、`run.font.bold=True`、`run.font.color.rgb=RGBColor(...)`。

【链接】https://python-pptx.readthedocs.io/en/latest/user/quickstart.html ；占位符 https://python-pptx.readthedocs.io/en/latest/user/placeholders-using.html ；shapes API https://python-pptx.readthedocs.io/en/latest/api/shapes.html

【已知坑/局限】不支持渐变填充等高级效果；不能直接渲染/导出 PDF(靠 LibreOffice)；对已有模板的母版/主题改动有限；图表类型与样式不如 PptxGenJS 丰富。最佳场景：数据驱动批量出页、表格密集。

## PptxGenJS

【是什么】Node/浏览器 JS 库，简洁 API 生成 .pptx；Anthropic PPTX skill「从零创建」就用它。

【可复用方法/核心 API】
- 骨架：`const pptxgen=require("pptxgenjs"); let pres=new pptxgen(); pres.layout='LAYOUT_16x9'; let s=pres.addSlide(); s.addText("Hi",{x,y,w,h,fontSize,color}); pres.writeFile({fileName:"x.pptx"})`。坐标单位=英寸。
- 版式尺寸：`LAYOUT_16x9`=10×5.625"、`LAYOUT_WIDE`=13.3×7.5"、`LAYOUT_4x3`=10×7.5"。
- 文本：富文本用数组 `[{text,options}]`；多行/列表项必须 `breakLine:true`；项目符号用 `bullet:true`(别打 Unicode `•`，会双重符号)；编号 `bullet:{type:"number"}`；与形状对齐设 `margin:0`；字间距用 `charSpacing`(非 letterSpacing)。
- 形状：`addShape(pres.shapes.RECTANGLE,{x,y,w,h,fill:{color},line:{...}})`；圆角用 `ROUNDED_RECTANGLE`+`rectRadius`；阴影 `shadow:{type:"outer",color,blur,offset(≥0!),angle,opacity}`(offset 负值会损坏文件)；透明用 `fill:{transparency:50}`，**不要**在 color 里编码透明。
- 图片：`addImage({path|data|url,x,y,w,h, sizing:{type:'contain'|'cover'|'crop'}, rounding, altText})`；base64 最快。算宽保比：`w = maxH*(origW/origH)`。
- 表格 `addTable(rows,{colW,border,fill})` 支持 `colspan/rowspan`；图表 `addChart(pres.charts.BAR|LINE|PIE,[{name,labels,values}],{...})`。
- 图标：react-icons → SVG → sharp 转 PNG(size≥256) → base64 贴入。

【链接】https://gitbrent.github.io/PptxGenJS/ ；charts https://gitbrent.github.io/PptxGenJS/docs/api-charts.html ；https://github.com/anthropics/skills/blob/main/skills/pptx/pptxgenjs.md

【已知坑/局限】无原生渐变(用渐变图当背景)；shadow offset 必须非负、color 必须 6 位 hex 无 `#`；不能直接转 PDF/图(靠 LibreOffice)。相对 python-pptx：JS 生态、形状/图标/视觉效果更顺手，数据分析链路弱于 Python。

## Marp

【是什么】Markdown 转幻灯片(HTML/PDF/PPTX/图片)；marp-core 引擎 + marp-cli 命令行。

【可复用方法】
- 全局指令(front-matter 或 HTML 注释)：`theme`(default/gaia/uncover)、`paginate:true`、`headingDivider:2`(按标题级自动分页)、`style:|`(注入 CSS)、`lang`。
- 局部指令(当页起生效)：`backgroundColor`、`color`、`backgroundImage`；加 `_` 前缀(如 `_backgroundColor`)只作用当前页(spot)。
- 分页：默认用 `---` 水平分隔；或 `headingDivider` 按标题自动切。
- 演讲备注：用 HTML 注释 `<!-- 备注 -->`。
- 导出 CLI：`npx @marp-team/marp-cli@latest deck.md --pdf`(或 `--pptx`/`-o out.html`)；`--pptx --pptx-editable` 尝试导出**可编辑文本**而非纯图(默认 `--pptx` 是把每页栅格化成图嵌入，不可在 PPT 里改字)，但可能复现不全样式；`--pdf-notes` 把备注写进 PDF；`--pdf-outlines` 生成书签；`-w` watch、`-s` server 目录预览。Node v18+。

【链接】https://github.com/marp-team/marpit/blob/main/docs/directives.md ；https://github.com/marp-team/marp-cli/blob/main/README.md ；https://marpit.marp.app/

【已知坑/局限】PDF/PPTX 转换走无头浏览器(需 Chrome/Chromium，沙箱里要配)；PPTX 是把每页当图片嵌入(不可在 PPT 里再编辑文字)；复杂自由排版不如 PPTX/HTML，强项是版本可控、文本化、Git 友好。

## reveal.js

【是什么】HTML 演示框架，浏览器里跑；支持 Markdown、Auto-Animate、PDF 导出、演讲者视图、LaTeX 数学、代码高亮。

【可复用方法】
- 初始化：`Reveal.initialize({ controls,progress,slideNumber,hash,transition,plugins:[Markdown,Notes,Highlight,Math] })`；返回 promise；`Reveal.destroy()` 反初始化。
- 结构：`.reveal>.slides>section`；嵌套 `section` = 纵向幻灯片(垂直堆叠)。
- Markdown：`<section data-markdown>` + `<textarea data-template>`；外部文件 `data-markdown="x.md"` 配 `data-separator`(横向，默认 `^\r?\n---\r?\n$`)、`data-separator-vertical`、`data-separator-notes`(默认 `notes?:`)。
- Fragment(分步出现)：`class="fragment"`，可加 `data-fragment-index` 控顺序；Markdown 里用 `<!-- .element: class="fragment" -->`。
- 演讲备注：Notes 插件 + 按 `S` 开演讲者视图(当前页/下一页/备注/计时)。
- PDF 导出：URL 加 `?print-pdf` 后浏览器打印；或用 decktape。

【链接】https://revealjs.com/ ；初始化 https://revealjs.com/initialization/ ；Markdown https://revealjs.com/markdown/ ；https://github.com/hakimel/reveal.js

【已知坑/局限】本质是网页(交互/动画/嵌视频强)，但导出 PDF/分发不如 PPTX 通用；外部 Markdown 需本地服务器(file:// 取不到)；离线分发要带 dist 资源。

## Beamer（LaTeX，学术）

【是什么】LaTeX 演示文档类，编译出多页 PDF，公式/参考文献/代码排版强，学术会议标配。

【可复用方法/核心语法】
- `\documentclass[11pt]{beamer}`(字号 8–20pt)；主题 `\usetheme{Madrid}` 然后 `\usecolortheme{beaver}`(颜色须在 usetheme 之后)；常见主题 Madrid/CambridgeUS/Boadilla/Berlin/Copenhagen。
- 页：`\begin{frame}\frametitle{...}...\end{frame}`；标题页 `\frame{\titlepage}`(配 `\title[短]{全}`、`\subtitle`、`\author[]{\inst{1}}`、`\institute`、`\date`、`\logo`)。
- 双栏：`\begin{columns}\column{0.5\textwidth}...\column{0.5\textwidth}...\end{columns}`。
- 高亮框：`block`(普通)、`alertblock`(红)、`examples`(绿)；行内 `\alert{词}`。
- 逐步显示(overlay)：item 上 `\item<1->`、`\item<2->`、`\item<3>`；或 `\pause` 分段；一个 frame 的 overlay 会编译成多页 PDF。
- 目录：`\tableofcontents`；分节自动插目录用 `\AtBeginSection[]{...\tableofcontents[currentsection]...}`。

【链接】https://www.overleaf.com/learn/latex/Beamer ；overlay https://latex-beamer.com/tutorials/overlays/

【已知坑/局限】视觉自定义繁琐、迭代慢；不擅长强设计感商务/路演；图文精细摆位不如 PPT；适合公式密集、需 BibTeX 引用的硬核学术答辩/报告。

## Canva（Connect API）

【是什么】在线设计平台 + Connect API，可程序化用品牌模板批量出图/演示。

【可复用方法/真实端点】
- Base URL：`https://api.canva.com/rest/v1`；认证 OAuth 2.0 授权码流，`Authorization: Bearer {TOKEN}`，支持 refresh token。
- 取模板字段集：`GET /brand-templates/{TEMPLATE-ID}/dataset` → 返回各字段名 + `type`(`text`/`image`)。
- 自动填充(异步)：`POST /autofills`，body `{brand_template_id, data:{FIELD:{type:"text",text:"..."}|{type:"image",asset_id:"..."}}}`；省略字段用模板默认。
- 轮询：`GET /autofills/{JOB-ID}` 直到 `status:"success"`，结果含 `design.url`(编辑链接) 与 `thumbnail.url`。
- 所需 scope：`design:content/meta`、`brandtemplate:meta/content`、`asset`。

【链接】https://www.canva.dev/docs/connect/autofill-guide/ ；https://canva.dev/docs/connect/api-reference/autofills/

【已知坑/局限】品牌模板 + Autofill API **要求开发者与用户都属 Canva Enterprise 组织**；图片字段只接受已上传 asset_id(不收外链/视频)；文档未公布具体限流数值。

## Gamma（Generations API）

【是什么】AI 文档/演示生成器，prompt→成品 deck，卡片式(card)编辑；有公开 Generations API。

【可复用方法/真实端点】
- Base URL：`https://public-api.gamma.app`；认证头 `X-API-KEY`(非 Bearer)，需 Pro/Ultra/Teams/Business 套餐。
- 生成(异步)：`POST /v1.0/generations`，仅 `inputText` 必填(≤~40 万字符/100k token)；可选 `format`(presentation/document/webpage/social)、`textMode`(generate/condense/preserve)、`numCards`(默认 10，Pro/Teams/Business 1–60、Ultra 1–75)、`cardSplit`(auto / inputTextBreaks 按 `\n---\n` 分页)、`themeId`(来自 `GET /v1.0/themes`)、`exportAs`(pdf/pptx/png 每次一种)、`additionalInstructions`(≤5000)、嵌套 `imageOptions{source,model,style}`、`textOptions{amount,tone,audience,language}`。
- 返回 `{generationId}`；轮询 `GET /v1.0/generations/{id}` 每 5s，到 `completed`；结果含 `gammaUrl`、`exportUrl`(签名链接约 1 周失效)、`credits.remaining`。
- 限流响应头 `x-ratelimit-remaining`/`-burst`/`-daily`。
- 其它端点：`POST /v1.0/generations/from-template`(改写已有 gamma，需 prompt+gammaId)、`GET /v1.0/themes`、`GET /v1.0/folders`(均游标分页)、`POST /v1.0/gammas/{id}/archive`、`DELETE /v1.0/gammas/{id}`(需 workspace admin)。

【链接】https://developers.gamma.app/ ；https://gamma.app/

【已知坑/局限】按 credit 计费(1–3 credit/卡，AI 图最高 125 credit/张)；导出 URL 会过期；细排版控制弱(适合快速初稿，再人工精修)。可借鉴工作流：topic→outline→card→theme→export 的分步式生成。

## Beautiful.ai

【是什么】在线演示工具，核心是 **Smart Slides**——基于规则(非 AI)的自适应版式；另有 DesignerBot 等 AI 生成内容功能。

【可复用方法/可借鉴理念】
- 规则驱动版式：加 bullet 自动调间距、插图自动再平衡、删内容周边元素自动重分布；300+ 智能版式持续强制对齐/间距/字号。
- 折成 light-slides 可用的设计约束：①约束式间距(min/max 随内容重算) ②内容感知重流 ③自动对齐到网格 ④按内容角色定字号/字重的层级规则 ⑤把"版式"定义成元素间关系而非绝对坐标(类似 Flexbox/Auto Layout)。

【链接】https://www.beautiful.ai/

【已知坑/局限】未核实其公开 API；闭源 SaaS，只能借鉴"约束/规则求解最佳版式"的设计哲学，无法直接调用。

## Slidesgo

【是什么】免费 Google Slides / PowerPoint 模板库 + AI 演示生成器，可下 PPTX 在 PowerPoint/Google Slides/Figma 编辑。

【可复用方法/可借鉴】
- AI 工具：AI Presentation Maker、PDF→PPT 转换、Lesson Plan/Quiz 等教育向生成器。
- 模板分类轴(选风格时可借)：按行业(商务/科技/法律/医学/营销…)、按风格(极简/简约/美学/专业/复古)、按颜色筛；教育中心按内容类型(论文答辩/课程/工作坊)、学科、学段组织。
- 用法：找版式灵感 + 下 PPTX 当起点，再原创化。

【链接】https://slidesgo.com/ ；AI https://slidesgo.com/ai/presentation-maker

【已知坑/局限】免费层每月限 3 个、高级模板需 Premium；免费模板的署名/许可条款见其 Terms(本次未逐条核实，商用前须确认授权)；本质是模板源，不是可调 API。

## 飞书 / Lark（国内协作场景）

【是什么】飞书云文档平台，国内团队协作高频。**注意区分**：官方开放平台云文档体系（实查 open.feishu.cn）只开放**文档 Docx / 电子表格 / 多维表格 / 知识库**等资源类型的服务端 API，**不含独立的"演示文稿/Slides"开放资源类型**——截至 2026-06 实查，无官方 OpenAPI 可程序化创建/编辑飞书演示文稿。

【可复用方法/适用场景】
- **内容协同**：用飞书文档/多维表格协作写 PPT 大纲与数据表（`tenant_access_token`/`user_access_token` 可程序化读写文档/表格），定稿后导出，再用本 skill 自带 python-pptx 资产渲染成品 PPT。飞书适合"协作写内容"，不适合"程序化出 PPT"。
- **lark-slides**：WebSearch 命中的 `larksuite/cli` 仓库 skills 目录下有 `lark-slides`（含 SKILL.md / xml-schema-quick-ref.md），是 **Lark CLI 的社区工具 skill，非飞书开放平台官方 OpenAPI**，借鉴其 XML schema 思路可，勿当官方 API 引用。

【链接】云文档概述 https://open.feishu.cn/document/server-docs/docs/docs-overview?lang=zh-CN ；lark-slides（社区，非官方 API）https://github.com/larksuite/cli/tree/main/skills/lark-slides

【已知坑/局限】演示文稿无官方开放 API（实查口径，引用前复查最新版本，飞书 API 持续扩展）；程序化出 PPT 仍走 python-pptx/PptxGenJS/Marp；飞书文档导出的格式保真度有限，复杂版式需在成品端重排。
