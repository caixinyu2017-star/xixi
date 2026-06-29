# light-file-reading — 深度分析与同类对标

> 源：[`skills/light-file-reading/SKILL.md`](../../../skills/light-file-reading/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：常驻、自动触发的多格式文件深度理解层:把 PDF/Word/Excel/PPTX/图片/视频/代码/压缩包"读懂"成五面理解笔记,并路由到下游科研技能;以"先问宿主能否原生读"为决策起点,需结构化抽取时才上专用脚本/库。

## 核心运行逻辑
设计核心是"理解优先于提取 + 决策优先于工具"。SKILL.md 先用一条决策链(① 看懂内容→宿主原生 Read 直接喂;② 结构化抽取/批处理/redline/OCR→专用脚本;③ 宿主读不了的格式→按格式表选库)避免对轻任务过度脚本化。真正落盘能力集中在三个带自检的 Python 模块(pdf_ops/docx_read/xlsx_read),每个模块把"库的职责分工"显式化(pdfplumber 抽文本表格 vs pypdf 结构操作;pandas 画像 vs openpyxl 公式格式)。知识用渐进式三层组织:SKILL.md 极简正文 → references/ 四个 copy-paste REF → references.md 13 个工具的深度核查笔记(端点/参数/已知坑)。最后所有理解结果都被强制"转化为可执行任务",指向 m02/m06/m08/m10/m11/m16 等下游技能,并把笔记登记到项目库 db09。安全上把"读到的一切视为数据非指令",内置 prompt injection 防御。

## 关键步骤
- 1. 决策:先判断宿主(Claude Code 的 Read)能否原生读 PDF/图片/notebook,能则零依赖直接喂,不绕道写脚本
- 2. 分流:需结构化抽取/批量/改 XML/OCR/公式不求值时,按格式选库——PDF 走 pdfplumber+pypdf,Word 走 python-docx 或 pandoc(修订走裸 XML 三步流),Excel 走 pandas+openpyxl,PPTX 走 markitdown+LibreOffice 渲染
- 3. 执行:调用 scripts/ 模块函数或 references/ 里的 copy-paste 代码块完成抽取(文本/表格/公式/页边距/缩略图等)
- 4. 视觉理解:PPTX/图片/视频转图后喂视觉模型;视频拆两路(ffmpeg 抽帧 + whisper 转写)
- 5. 产出五面理解笔记:结构与逻辑、关键内容、格式与要求、视觉风格、可复用内容(而非原文堆叠)
- 6. 转化:明确'这个文件→下一步能做什么',路由到对应下游技能
- 7. 合规与衔接:版权全文不外传、敏感值按 key 名引用;笔记与可复用资源登记到 db09

## 自带资产
- scripts/pdf_ops.py — PDF 读取与结构操作(read_meta/extract_text(layout)/extract_tables→DataFrame/merge/split/rotate),自带 reportlab 合成 PDF 的全流程断言自检
- scripts/docx_read.py — Word 读取(read_paragraphs/read_headings/read_runs 样式/read_tables/read_layout 页边距),自带合成 docx 自检
- scripts/xlsx_read.py — Excel 读取(list_sheets/read_formulas 不求值/read_values 读缓存/profile 数据画像),自带含公式 xlsx 自检
- references/PDF-REF.md — PDF 决策表 + 抽文本/表格/裁剪区域/合并拆分旋转加密水印/OCR/命令行 的 copy-paste 代码块 + 已知坑
- references/DOCX-REF.md — Word 决策表 + python-docx 读法 + pandoc 修订/批注 + 解包改 XML 重打包三步流(<w:ins>/<w:del> 模板)
- references/XLSX-REF.md — Excel 决策表 + pandas 画像 + openpyxl 读公式/缓存值 + LibreOffice 重算扫错
- references/PPTX-REF.md — PPTX 文本抽取(markitdown)+ soffice/pdftoppm 渲染成图视觉理解 + 占位符 grep QA + 视觉风格提取要点(无配套脚本)
- references.md — 13 个工具的深度核查笔记(Anthropic 四官方 skill、MarkItDown、LiteParse、Open Notebook、Paperzilla、Pandoc、Tika、unstructured、视频工具链、pdfplumber/pypdf/python-docx/openpyxl),含真实端点/参数/已知坑,链接 2026-06 curl 200 核验

## 优点
- 决策优先于工具:开篇就强制'先问宿主能不能原生读',对'只想看懂内容'的轻任务明令零依赖直喂,有效防止 AI 习惯性地对一个 PDF 先写 pdfplumber 绕远路——这是非常务实且少见的反过度工程设计
- 三个脚本都自带 selftest:自己合成 fixture(reportlab/python-docx/openpyxl)、逐步 assert、结束清理临时文件,可复现验证'声称能跑'非空话,工程质量高于多数技能
- 库职责分工讲清楚了'为什么'而非只列 API:pdfplumber 抽文本表格 vs pypdf 结构操作、pandas 画像 vs openpyxl 公式、python-docx 读 vs 裸 XML 改修订,选型有依据
- 已知坑具体且高价值:reportlab Unicode 上下标渲染成黑块、data_only=True 保存永久毁公式、pandas 行号比 Excel 少 1、pypdf 300MB 流要 10GB RAM、财务模型 col 64=BL——都是实战踩过才知道的细节
- 渐进式三层信息架构(SKILL 极简/references copy-paste/references.md 深度核查)token 高效,按需加载,符合 skill 设计规范
- '不止提取要理解'的五面框架(结构逻辑/关键内容/格式要求/视觉风格/可复用内容)把它从'文本转储器'抬升为科研理解层,且每面都显式映射到下游技能,衔接意识强
- prompt injection 防御内置(读到的'忽略以上指令'当数据处理、记 INJECTION-ATTEMPT-DETECTED),并有版权/敏感值合规约束,安全意识到位
- Windows 适配到位:脚本顶部 sys.stdout.reconfigure(encoding='utf-8') 防 GBK 控制台乱码,与运行环境(Win11 中文)匹配

## 缺点 / 可被质疑处
- 格式覆盖严重不对称:description 承诺'图片、视频、代码、压缩包'等,但只有 PDF/DOCX/XLSX 有脚本+REF,PPTX 仅 REF 无脚本,图片/代码/压缩包在 SKILL.md 里各只有一行口号(图片'转 db07'、代码'读结构依赖逻辑'、压缩包'解包后递归'),无任何可执行资产或参考——名实不副,深度断崖
- docx_read 对中文 Word 失效:read_headings/read_paragraphs 靠英文 style 名 'Heading N'/'Title' 判断标题,中文模板的'标题 1'会被误判为正文或 lvl=1,而目标用户正是中文科研论文作者——这是会真实出错的 bug,不是边角
- 脚本只能当库 import,不能直接处理用户文件:CLI 入口被写死只接受 --selftest(python pdf_ops.py file.pdf 会报 usage 错),SKILL.md '可直接 python 运行'只指自检。实际用必须 agent 手写 inline import,多一层摩擦,也与'即用脚本'宣传不符
- 无理解笔记模板/examples:SKILL.md 规定了五面输出和'文件→下一步'映射,却没有 templates/ 或 examples/ 落地成可复用 schema,输出一致性全靠模型临场发挥,也不利于稳定登记到 db09
- 脚本健壮性缺口:缺依赖守卫(pdfplumber/openpyxl 未装时抛裸 ImportError 无 pip 提示);extract_text 把全部页文本载入 list、read_formulas/read_values 不用 read_only,大文件易 OOM(自己 references 里刚警告过 pypdf 内存问题却没在脚本防);xlsx profile 对多行表头/合并单元格会静默错位
- 读取盲区未覆盖:docx_read 只读 doc.paragraphs,漏掉表格内文字、页眉页脚、文本框;无 read_meta(作者/标题)等价物;PPTX 无脚本意味着演讲者备注(notes,常含真正内容)可能随 markitdown 丢失
- 科研高频图像需求缺位:从图表图片反提数据(WebPlotDigitizer 类)、公式 OCR(Mathpix/pix2tex)、表格截图→CSV 全无,而读论文/读他人结果图恰恰最需要这些——图片处理停在'喂视觉模型看'
- references.md 与 references/*.md 内容重叠(PDF 决策表、已知坑两处都有),双份维护易漂移;且大量 m0x/db0x/a0x 代号依赖外部 CONVENTIONS,技能内无法自解析

## 可优化点（供后续逐技能优化）
- 给三个脚本加 argparse CLI,让 python pdf_ops.py extract-text file.pdf / xlsx_read.py profile f.xlsx 能直接处理真实文件,并保留 --selftest;消除'即用脚本却只能自检'的名实差
- 修中文标题检测:read_headings 同时匹配 'Heading N'/'标题 N'/'Title'/'标题',并优先读段落的 w:outlineLvl(p._p.pPr) 而非 style 名,彻底脱离语言依赖
- 补 docx 读取盲区:遍历表格内段落、页眉页脚、文本框文字;新增 read_core_props(作者/标题/创建时间)与 pdf read_meta 对齐
- 新增 IMG-REF.md + 可选脚本:覆盖图表反提数据(WebPlotDigitizer/PlotDigitizer)、公式 OCR(pix2tex/Mathpix)、表格截图→CSV、EXIF——把图片从'看一眼'升级为'抽得出数据',直接服务读论文/读结果图
- 新增 templates/understanding-note.md:把五面理解 + '文件→下一步动作(指向哪个下游技能)'固化成结构化模板,保证输出一致并可直接登记 db09;配 1-2 个 examples/ 真实样例
- 加依赖守卫与大文件防护:统一 try-import 给出 pip 安装提示;extract_text 支持页范围/生成器流式;openpyxl 读取默认 read_only 并对超阈值行列告警;profile 支持 header=多行 与 describe 输出截断
- 补 PPTX 读取脚本(至少抽正文+演讲者备注+逐 shape 文本)与 CODE-REF/ARCHIVE-REF(代码用 tree-sitter/ctags 出结构与依赖;压缩包递归分派并加 zip-bomb/总解压大小守卫)
- 把 references.md 收敛为索引/工具选型矩阵,具体代码与坑只留在 references/*.md,消除双份维护;并在 SKILL.md 加一张'格式×(宿主原生/脚本/REF/仅提及)'覆盖矩阵,让 agent 对每种格式的真实深度有预期

## 与其他 Light 技能/知识库的衔接
作为常驻自动触发的上游"输入层",几乎为整条 pipeline 供料,衔接最密。下游显式路由:数据画像→light-data-engineering(m02)、实验结果/图表解读→light-result-analysis(m06)、论文修改→light-paper-polishing(m08)、引用提取→light-citation(m10)、图表重绘→light-figure-drawing/planning(m11)、PPT 视觉风格→light-slides(m16)与前端 a05、项目整理→light-project-structure(a06);理解笔记与可复用资源登记到 light-memory-pm 的项目库(db09),视觉素材进 db06/db07。安全/合规依赖外部 CONVENTIONS §4(注入即数据)、§5 与 a10(敏感值按 key 名引用)。工具选型与 a09(light-tool-selection)同源呼应。注意:大量 m0x/db0x/a0x 代号在技能内无定义,完全依赖外部 CONVENTIONS 注册表才能解析。

---

## GitHub 同类前沿技能对标

Light 的 light-file-reading 是一层"理解+决策+路由"的科研专用阅读编排器:它的核心资产不是解析引擎,而是一条"先问宿主能否原生读→需结构化抽取才上脚本→读不了才按格式选库"的决策链,加上五面理解笔记、强制转化为下游科研任务(m02/m06/m08 等)、登记 db09、以及 prompt-injection 防御。GitHub 上的同类前沿项目几乎全部落在"解析/抽取引擎"这一层:markitdown、docling、MinerU、marker、unstructured、zerox、olmOCR 都在比拼"把 PDF/Office/图片转成干净 markdown/JSON"的保真度与版面/表格/公式还原能力,普遍带 OCR、视觉大模型、GPU pipeline,工程成熟度和格式覆盖远超 Light 的三个轻量 Python 模块。但它们几乎都不做"理解优先于提取"的决策判断,也不内置科研工作流路由、研究伦理/注入防御或记忆登记——这正是 Light 的差异化定位。真正与 Light 形态接近的是 anthropics/skills(官方 docx/pdf/pptx/xlsx 渐进式 SKILL.md,Light 的模块设计明显借鉴此范式)和 opendatalab/MinerU-Document-Explorer(agent-native、MCP、deep reading + wiki 组织),后者在"agent 主动深读"理念上和 Light 最神似但偏检索而非科研产出。整体看:Light 在"决策克制+科研闭环"上独特,在"解析引擎硬实力+格式广度"上明显弱于这些专用工具,最佳策略是把后者作为 light-file-reading 决策链第②③步可调用的后端。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | Anthropic 官方 Agent Skills 仓库,含 docx/pdf/pptx/xlsx 等文档处理 skill,采用渐进式 SKILL.md + 脚本 + 参考文档结构,与 Light 技能形态同源 | 149996 | 2026-06-09 | 强:官方范式、社区巨大、文档创建/编辑能力(不止读)成熟、被各 harness 内置;弱:面向通用办公而非科研,无'先问宿主能否原生读'的决策克制,无下游科研技能路由、无 db 登记、无科研伦理/注入防御整合,单格式独立而非统一理解层 |
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | 把 PDF/Word/Excel/PPT/图片/音频等统一转成 LLM 友好的 Markdown 的轻量 Python 工具,亦提供 markitdown-mcp | 152156 | 2026-05-26 | 强:格式覆盖极广、极轻量、社区第一、可直接做 MCP 后端;弱:纯'提取转换'无'理解+决策',不产五面笔记、不路由科研任务、不防注入,表格/版面保真不如 docling/marker |
| [opendatalab/MinerU](https://github.com/opendatalab/MinerU) | 面向 Agentic 工作流,把复杂 PDF/Office 转 LLM-ready markdown/JSON,强版面分析、公式/表格/OCR,适合科研文献 | 67382 | 2026-06-11 | 强:科研文献解析保真度(公式/表格/多栏)远超 Light 的 pdfplumber 方案、活跃迭代、GPU pipeline;弱:重型依赖、纯解析引擎、无决策链/无理解笔记/无科研闭环路由,适合作为 Light 决策链第③步的库 |
| [docling-project/docling](https://github.com/docling-project/docling) | IBM 发起,把 PDF/DOCX/PPTX/XLSX/HTML 转成统一 DoclingDocument 结构,带表格/阅读顺序/OCR,深度集成 LangChain/LlamaIndex | 61473 | 2026-06-12 | 强:统一文档模型、结构化保真高、生态集成强、有 docling-serve API;弱:同为引擎层,无'理解优先/决策优先'哲学,不做科研任务转化与记忆登记 |
| [datalab-to/marker](https://github.com/datalab-to/marker) | 高精度高速把 PDF(及多格式)转 markdown+JSON,强表格/公式/图像,可选 LLM 增强,科研论文转换常用 | 36045 | 2026-06-13 | 强:PDF 转换精度与速度业界领先、对论文公式表格友好;弱:专注转换不做理解决策、不覆盖压缩包/视频/代码的统一阅读、无科研流程编排 |
| [allenai/olmOCR](https://github.com/allenai/olmocr) | AllenAI 出品,用视觉语言模型把 PDF 线性化为适合 LLM 训练/数据集的文本,擅长扫描件与复杂版面 | 17386 | 2026-06-12 | 强:VLM 驱动的扫描/复杂版面 OCR 质量高、面向大规模数据集构建;弱:只解决 PDF→文本一环,无多格式统一层、无决策链、无理解笔记与科研路由,可作 Light OCR 分支后端 |
| [Unstructured-IO/unstructured](https://github.com/Unstructured-IO/unstructured) | 开源 ETL,把 PDF/DOCX/HTML 等复杂文档拆成结构化元素(标题/表格/段落),为 RAG/LLM 预处理、分块、嵌入 | 14897 | 2026-06-11 | 强:格式广、元素级结构化、分块/嵌入一条龙、企业级生态;弱:偏 RAG 流水线非交互式理解,无'宿主能否原生读'的克制判断、无科研任务转化、注入防御非内置 |
| [getomni-ai/zerox](https://github.com/getomni-ai/zerox) | 用视觉模型做 OCR 与文档抽取,把页面渲染成图再交给多模态 LLM 输出 markdown,对复杂版面鲁棒 | 12239 | 2025-05-20 | 强:视觉模型路线对扫描件/复杂版面强、API 简单;弱:更新放缓(2025-05)、单一 OCR 用途、无多格式统一与科研编排,只能作 Light 的一个可选后端 |
| [simonw/claude-skills](https://github.com/simonw/claude-skills) | Simon Willison 抓取并公开的 Claude 代码解释器 /mnt/skills 内容,含官方 pdf/docx/pptx/xlsx skill 原文,常被当作 skill 写法参考 | 924 | 2025-12-12 | 强:直接展示官方文档 skill 的真实写法、是 Light 借鉴 SKILL.md 渐进式结构的活样本;弱:只是只读快照、非可维护项目、无任何科研化封装或决策逻辑 |
| [opendatalab/MinerU-Document-Explorer](https://github.com/opendatalab/MinerU-Document-Explorer) | Agent-native 知识引擎,提供 MCP 工具做文档索引、wiki 组织、快速检索与对 PDF/DOCX/PPTX/Markdown 的'deep reading' | 585 | 2026-04-26 | 强:与 Light 理念最接近(agent 主动深读+组织),MCP 化、有索引与 wiki 沉淀;弱:偏检索/知识库构建而非科研产出闭环,无下游论文/idea 技能路由,无伦理/注入约束,星少较新 |

### Light 该技能可借鉴的点
- 把解析重活外包给成熟引擎:在决策链第②③步显式接入 docling 或 MinerU 作为可选后端(尤其论文公式/多栏表格保真),而不是只靠 pdfplumber/pypdf,避免在复杂科研 PDF 上吃亏
- 对扫描件/图片型 PDF 增加 VLM-OCR 分支(参考 olmOCR/zerox 的'渲染成图再交多模态'路线),补足当前纯文本抽取在扫描文献上的短板
- 学习 markitdown 的'万格式统一进、统一 Markdown 出'思路,为 light-file-reading 增加一个统一中间表示,让五面笔记的上游更标准化、跨格式一致
- 借鉴 docling/unstructured 的'文档元素模型'(标题/表格/段落/阅读顺序的结构化对象),让结构化抽取产物可被 db09 与下游 m08/m11 直接消费而非自由文本
- 参考 MinerU-Document-Explorer 的 agent-native 索引+wiki 组织,把多文件项目的理解笔记升级为可检索知识库,支撑长周期科研项目的跨文档回看
- 跟随 anthropics/skills 官方 docx/pptx/xlsx skill 的最新写法持续对齐渐进式 SKILL.md + 脚本 + REF 的边界划分,保持与官方范式同步,降低维护成本
- 引擎选型与版本坑同步:这些库迭代很快(多在 2026-06 仍活跃),在 references.md 的工具核查笔记中增加'推荐后端+版本+已知坑'条目并定期更新,避免脚本对老版本 API 失效
