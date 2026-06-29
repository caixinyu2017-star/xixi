# light-file-reading 参考工具笔记

逐工具核查笔记，供深度读文件时查阅。每条含【是什么】【可复用方法/真实端点/参数】【链接】【已知坑/局限】。
研究日期 2026-06。

---

## Anthropic PDF skill

【是什么】Anthropic 官方文档技能之一，处理 .pdf 的读取、合并/拆分、表单、创建、OCR。

【可复用方法】按任务选库（决策表）：
- 合并/拆分/旋转/加密 → **pypdf**
- 抽文本 → **pdfplumber**（保留版面）
- 抽表格 → **pdfplumber**（`extract_tables` → pandas DataFrame）
- 生成新 PDF → **reportlab**（Platypus：`SimpleDocTemplate` + `story` 列表）
- 扫描件 OCR → **pytesseract + pdf2image**（`convert_from_path` 转图再识别）
- 填表单 → pdf-lib 或 pypdf（详见其 FORMS.md）
- 命令行 → `pdftotext -layout`、`qpdf --empty --pages a.pdf b.pdf -- out.pdf`、`pdfimages -j`

【已知坑】reportlab 中绝不要用 Unicode 上下标字符（₀₁₂ ⁰¹²），会渲染成黑块；改用 Paragraph 内的 `<sub>`/`<super>` XML 标签。

【链接】https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md

---

## Anthropic DOCX skill

【是什么】官方 Word 技能，覆盖读取、创建、改 XML、修订(tracked changes)、批注。

【可复用方法】按任务分流：
- 读/分析 → `pandoc`（或解 ZIP 看裸 XML）
- 新建 → **docx-js**（npm `docx`），不是 python-docx
- 编辑既有 → 解包→直接改 XML→重打包（三步流）
- .doc→.docx、转图 → LibreOffice `soffice`
- 接受修订 → `scripts/accept_changes.py`

三步编辑流：
1. `python scripts/office/unpack.py document.docx unpacked/`（解包、美化、合并相邻 run、智能引号转 XML 实体）
2. 用 Edit 工具直接改 `unpacked/word/document.xml`，不要写 Python 脚本
3. `python scripts/office/pack.py unpacked/ out.docx --original document.docx`（校验+自动修复）

修订标记：插入用 `<w:ins w:author="Claude" w:date=...><w:r><w:t>...</w:t></w:r></w:ins>`；删除用 `<w:del>` 内放 `<w:delText>`（不是 `<w:t>`）。最小化改动只标真正变化的词。删整段要把段落标记也标删（`<w:pPr><w:rPr>` 内加 `<w:del/>`），否则接受后留空段。批注的 `<w:commentRangeStart/End>` 必须是 `<w:r>` 的兄弟节点，不能塞进 run 里。

【创建规则(docx-js)】显式设页面尺寸（默认 A4，美国文档用 US Letter 12240×15840 DXA）；绝不用 `\n`（用独立 Paragraph）；表格列宽要双份（table 的 `columnWidths` + 每个 cell 的 `width`，都用 DXA 不用百分比）；底纹用 `ShadingType.CLEAR`；横向页传纵向尺寸（库内部会交换）。

【链接】https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md

---

## Anthropic PPTX skill

【是什么】官方 PowerPoint 技能，读/编辑/从零创建幻灯片。

【可复用方法】
- 读/分析 → `python -m markitdown presentation.pptx`
- 编辑既有/套模板 → 解包→改 XML→重打包（用 `scripts/office/unpack.py`）
- 从零创建 → **pptxgenjs**（npm，JavaScript），注意不用 python-pptx
- 视觉概览 → `scripts/thumbnail.py`（缩略图网格，Pillow）
- 转图 QA → `soffice.py --headless --convert-to pdf` 再 `pdftoppm -jpeg -r 150 out.pdf slide`

【设计规则】标题 36–44pt 粗、节标题 20–24pt、正文 14–16pt、注释 10–12pt；最少 0.5" 边距；深色背景用于标题/结论页、浅色用于正文（"三明治"结构）。禁忌：别每页同版式、别纯文字页（总加视觉元素）、别在标题下加强调线（AI 痕迹）、别默认蓝色、正文左对齐只标题居中。

【QA 流程(强制)】假设首次渲染必有问题。内容 QA 用 markitdown 抽文本 grep 检查残留占位符(lorem/ipsum/xxxx)；视觉 QA 用 subagent 新视角看渲染图，查重叠/溢出/低对比/间距不匀；改完重验受影响页（修复常引入新问题），循环到一整轮无问题。"未完成至少一轮 fix-and-verify 前不要宣布成功。"

【链接】https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md

---

## Anthropic XLSX skill

【是什么】官方 Excel 技能，读/写/算公式。

【可复用方法】选库：pandas 做数据分析/批量/导出；openpyxl 做复杂格式/公式/Excel 特性。
- 读：`pd.read_excel('f.xlsx', sheet_name=None)` 读全部 sheet 成 dict；`df.info()/describe()`。
- 写：`openpyxl.Workbook()`，`sheet['B2']='=SUM(A1:A10)'`，Font/PatternFill/Alignment 设格式。
- 改：`load_workbook`，`insert_rows/delete_cols/create_sheet`。

【核心铁律】
1. **公式优先于硬编码**：用 `sheet['B10']='=SUM(B2:B9)'`，绝不在 Python 算好写死值。
2. **写完必须重算**：openpyxl 只存公式字符串不计算，保存后跑 `python scripts/recalc.py out.xlsx 30`，返回 JSON 含 total_errors/total_formulas，有错就改了再算。

【已知坑】`data_only=True` 保存会永久销毁公式（只读取缓存值时用）；openpyxl 1-based 索引（row=1,col=1=A1）；DataFrame 第5行=Excel 第6行（表头偏移）；跨表引用用 `Sheet1!A1`；财务模型远右列常在 50+ 列，注意列映射（col 64=BL）。财务配色约定：蓝=硬编码输入、黑=公式、绿=跨表链接、红=外部文件链接、黄底=关键假设。

【链接】https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md

---

## MarkItDown (microsoft/markitdown)

【是什么】微软开源 Python 工具，把各类文件/Office 文档转成 Markdown，专为喂 LLM 的文本分析管道设计。支持 PDF/PPTX/DOCX/XLSX(XLS)/图片(EXIF+OCR)/音频(转写)/HTML/CSV/JSON/XML/ZIP/YouTube URL/EPub/Outlook 邮件。

【可复用方法】
- 安装：`pip install 'markitdown[all]'` 或选装 `markitdown[pdf,docx,pptx]`。需 Python 3.10+。
- CLI：`markitdown file.pdf -o out.md`，或 `cat file.pdf | markitdown`。
- Python：`from markitdown import MarkItDown; md=MarkItDown(enable_plugins=False); md.convert("x.xlsx").text_content`。方法由窄到宽：`convert_stream`/`convert_local`/`convert_response`/`convert`。
- LLM 图像描述(PPTX/图片)：`MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o", llm_prompt=...)`。
- Azure Document Intelligence：`MarkItDown(docintel_endpoint=...)`（CLI `-d -e <endpoint>`）。
- 插件 `markitdown-ocr`：给 PDF/DOCX/PPTX/XLSX 加 LLM Vision OCR。

【已知坑】输出供文本分析、非高保真人读用；视频仅 Azure Content Understanding 支持；Azure 功能产生计费 API 调用；以当前进程权限做 I/O，不可信环境要净化输入。

【链接】https://github.com/microsoft/markitdown

---

## LiteParse (run-llama/liteparse)

【是什么】LlamaIndex 团队开源的快速、轻量、**无模型**文档解析器。Rust 核心 + Python/Node/WASM 绑定，PDFium 抽文本，纯本地无云依赖。

【可复用方法】
- 安装 `pip install liteparse`，提供 `lit` CLI 与 Python 库(PyO3)。
- 主格式 PDF；Office(.docx/.pptx/.xlsx/.odt/.rtf/.csv 经 LibreOffice)、图片(经 ImageMagick)先转 PDF。
- 输出：带 bounding box 的结构化 JSON、保留版面的纯文本、页面 PNG 截图（供 LLM 视觉处理）。**不输出 Markdown**——它做带坐标的空间文本抽取，不做语义结构化。
- OCR：内置 Tesseract（零配置）；可经 `--ocr-server-url` 接 EasyOCR/PaddleOCR 的 HTTP OCR 服务（POST `/ocr`，参数 file+language，返回 text/bbox/confidence）；`--no-ocr` 完全关闭。

【已知坑】复杂文档（密集表格、多栏、图表、手写、扫描件）官方建议改用其云产品 LlamaParse；Office/图片支持依赖外部 LibreOffice/ImageMagick。

【链接】https://github.com/run-llama/liteparse/ ; 文档 https://developers.llamaindex.ai/liteparse/getting_started/

---

## Open Notebook (lfnovo/open-notebook)

【是什么】自托管、隐私优先的 NotebookLM 开源替代。组织知识、与资料对话、生成播客，数据与模型选择全自控。MIT。

【可复用方法/架构】
- 摄取源：PDF/视频/音频/网页/Office 文档；全文+向量检索。
- 笔记：手写或 AI 生成洞见；按 notebook 项目化组织。
- 播客：多说话人(1–4，自定义 Episode Profiles)，强于 NotebookLM 的 2 人限制。
- Chat：基于资料的上下文对话，每 notebook 多会话，可细粒度控制喂给 AI 的内容。
- Transformations：自定义动作做摘要/抽洞见。
- 18+ 模型提供商经 Esperanto 库（OpenAI/Anthropic/Google/Ollama/Mistral 等）。
- 栈：FastAPI(REST API) + Next.js/React + SurrealDB v2(文档存储+向量) + LangChain。
- 部署：Docker Compose（SurrealDB:8000 + 应用前端:8502/API:5055），可配 Ollama 全本地，支持 MCP（Claude Desktop/VS Code）。API key 用用户密钥静态加密。

【已知坑】引用功能基础但在改进中。

【链接】https://github.com/lfnovo/open-notebook

---

## Paperzilla (paperzilla.ai)

【是什么】持续科研监控系统：聚合论文/数据集/软件仓库/专利，按你的研究主题做相关性过滤，输出结构化 feed 给人和 AI agent。解决每日 10000+ 新论文的信息过载。

【可复用方法】
- 源聚合：arXiv/bioRxiv/medRxiv/ChemRxiv/ChinaXiv，并接收转发的 Google Scholar/期刊/newsletter 提醒。
- 相关性引擎：对主题排序，带随时间改进的反馈回路。
- 多格式输出：应用内 feed、邮件摘要(日/周)、RSS/Atom、**MCP server**、CLI、API。
- 源锚定设计：每条结果回链原始记录，"AI 摘要助分诊，原记录仍是事实依据"。
- AI agent 用例：经 MCP/CLI/API 消费特定主题的研究流，让 agent 从聚焦上下文而非开放网起步。

【已知坑】商业服务，核查仅基于官网描述，具体 API 端点/限流未公开核实。

【链接】https://paperzilla.ai/

---

## Pandoc

【是什么】通用文档转换器(Haskell)。reader 解析源→抽象语法树(AST)→writer 生成目标。研究相关格式：docx/latex/markdown/bibtex/biblatex/html/odt/epub 进；docx/latex/pdf/html/markdown/jats/typst/beamer/pptx 出。

【可复用方法】
- 基础：`pandoc in.docx -o out.md`；`-s/--standalone` 出完整文档。
- 修订：`pandoc --track-changes=accept|reject|all in.docx -o out.md`；`all` 把增删/批注包成 insertion/deletion/comment span（保留作者+时间，可脚本化按审阅者接受）。**仅 docx reader 有效。**
- 抽媒体：`pandoc --extract-media=./media in.docx -o out.md`（导出内嵌图并改引用）。
- 引文：`pandoc --citeproc --bibliography=refs.bib --csl=apa.csl paper.md -o paper.pdf`；不给 CSL 默认 chicago-author-date；书目支持 BibTeX/BibLaTeX/CSL JSON/CSL YAML；LaTeX 原生用 `--natbib`/`--biblatex`。
- 样式模板：`pandoc --reference-doc=custom.docx paper.md -o out.docx`（只用样式，内容被丢弃）；生成模板 `pandoc -o ref.docx --print-default-data-file reference.docx`。
- PDF：默认 pdflatex，Unicode/自定义字体用 `--pdf-engine=xelatex`。
- defaults 文件：把常用选项写进 YAML，`pandoc --defaults cfg.yaml paper.md` 复现。

【已知坑】转换天然有损（AST 比源表达力弱，复杂表格/精确格式不保）；仅 UTF-8；PDF 需外部 LaTeX 引擎(TeX Live)，缺包报错隐晦——可输出中间 `.tex` 调试；`-V foo=false` 是字符串(真值)，`-M foo=false` 才是布尔假；`--citeproc` 时自动关掉 writer 原生引文语法避免重复渲染。

【链接】https://pandoc.org/MANUAL.html

---

## Apache Tika

【是什么】内容分析工具包(Java)，从 1000+ 文件类型检测并抽取文本与元数据，统一接口。两大接口：Parser(抽内容+元数据)、Detector(识别类型)。最新稳定 3.3.1(2026-05)，需 Java 11+。

【可复用方法】
- tika-app(CLI)：独立 JAR，单次或批量处理。
- tika-server(REST)：JAX-RS 服务，端点：
  - `/tika` 抽文本(也支持 JSON handler)
  - `/meta` 元数据
  - `/rmeta` 递归元数据(处理内嵌文档)
  - `/unpack` 抽内嵌资源/附件
  - `/language` 语言检测
- 输出：纯文本或 XHTML、键值元数据(content-type/author/创建日期/页数)、MIME 类型、语言码。
- 适合搜索引擎索引、内容分析、翻译预处理。

【已知坑】抽取质量随格式而异(parser 成熟度不同)；大文档吃资源(历史 OOM 致 503，1.20 修复)；OCR(Tesseract)、ffmpeg/exiftool 需另装；内嵌文档(ZIP/MSG/PDF+XFA)处理复杂；深度学习特性(图像描述)需额外大依赖且已不再打包。

【链接】https://tika.apache.org/

---

## unstructured.io (unstructured)

【是什么】开源 Python 库，把原始非结构化文档切成有类型的 element：`Title`/`NarrativeText`/`Table`/`ListItem`。20+ 格式(PDF/DOCX/PPTX/XLSX/HTML/MD/EML/MSG/EPUB/图片/代码)。专为 RAG 预处理。

【可复用方法】
- 入口：`from unstructured.partition.auto import partition; elements = partition(filename="x.pdf")`，libmagic 自动识别类型并路由。可 `include_page_breaks=True`、`content_type=...`。
- `partition_pdf` 四策略：
  - `fast`：pdfminer 抽文本，多数有文本层 PDF 首选。
  - `hi_res`：detectron2_onnx 做版面分析，对元素分类敏感时用；可 `extract_image_block_types=["Image","Table"]`。
  - `ocr_only`：Tesseract OCR，多栏无文本层文档用。
  - `auto`(默认)：按文档特征选(需表格→hi_res，有文本→fast，否则 ocr_only)。
- 元素结构：每个有 `.text` 和 `.metadata`；表格的 `metadata.text_as_html` 给 HTML 表示；PDF/图片可带页码。
- 下游：partition 产出的 element 喂给 chunking(如 `by_title`)做 RAG 检索分块。

【已知坑】hi_res 对多栏文档排序困难；OCR 仅在无文本层时启用；版权保护 PDF 不能用 fast 会退回 hi_res；partition_doc/ppt 需外部 libreoffice；EPUB/RST/RTF/Org 需 pandoc。

【链接】https://docs.unstructured.io/open-source/core-functionality/partitioning

---

## 视频工具链（ffmpeg 抽帧 + Whisper 转写）

【是什么】视频无现成"读懂"库，标准做法是拆成两路降维：画面→抽帧→当图片读；语音→抽音轨→转写成文本。ffmpeg 管音视频解复用/抽帧，faster-whisper / openai-whisper 管语音转文字。

【可复用方法】
- 抽帧（固定间隔）：`ffmpeg -i in.mp4 -vf "fps=1/5" frames/%04d.jpg`（每 5 秒一帧，调 `1/N`）。
- 抽帧（场景切变，适合 PPT 录屏/翻页）：`ffmpeg -i in.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr frames/%04d.jpg`，阈值 0.3 可调（越小越敏感）。
- 抽音轨（转写前置）：`ffmpeg -i in.mp4 -vn -ac 1 -ar 16000 audio.wav`（单声道 16kHz，Whisper 友好）。
- 转写（faster-whisper，推荐，快且省显存）：`pip install faster-whisper` 后 CLI `whisper-faster audio.wav --model base --language zh --output_format srt`；或 Python `from faster_whisper import WhisperModel; model=WhisperModel("base"); segments,_=model.transcribe("audio.wav", language="zh")` 拿带时间戳的段。
- 转写（openai-whisper，官方实现）：`pip install -U openai-whisper` 后 `whisper audio.wav --model base --output_format srt`。模型档 tiny/base/small/medium/large-v3，越大越准越慢。
- 取视频元信息/时长：`ffprobe -v quiet -print_format json -show_format -show_streams in.mp4`。

【已知坑】ffmpeg、whisper 均需**另装**（ffmpeg 走系统包管理器/官网二进制；whisper 走 pip，openai-whisper 还需 ffmpeg 在 PATH）；large 模型显存吃紧，长音频先按 ffprobe 时长分段或先抽帧定位关键时段再精转写，别整段硬转；中文务必显式 `--language zh`（自动检测对中英混杂易误判）；抽帧 fps 太高会产生海量图片，按需求先粗后细。

---

## pdfplumber (jsvine/pdfplumber)

【是什么】基于 pdfminer.six 的 Python 库，抽取字符/线/矩形/曲线的细节，含高层文本/表格抽取与可视化调试。最适合机器生成 PDF(非扫描件)。MIT。

【可复用方法】
- 打开：`with pdfplumber.open("f.pdf") as pdf: page = pdf.pages[0]`（支持 password/laparams）。
- 对象：`page.chars/lines/rects/curves/images/annots/hyperlinks`，每个是带坐标(x0/x1/top/bottom)的 dict，带 fontname/size 等。
- 空间过滤：`page.crop((x0,top,x1,bottom))`、`within_bbox`、`outside_bbox`、`filter(fn)`——定位页面特定区域。
- 文本：`extract_text(layout=True)` 保版面、`extract_words(...)` 返回词框、`extract_text_lines`、`search(pattern)`、`dedupe_chars`；调 `x_tolerance/y_tolerance/use_text_flow`。
- 表格：`extract_tables`/`extract_table`/`find_tables`，策略 `lines`/`lines_strict`/`text`/`explicit`；调 `snap_tolerance/join_tolerance/intersection_tolerance`。
- 可视化调试：`im=page.to_image(resolution=150); im.draw_rects(page.rects); im.debug_tablefinder(...); im.save("d.png")`——迭代表格设置利器，Jupyter 自动渲染。

【已知坑】无 OCR(扫描件不行)；不能生成/修改 PDF；OCR 文档表格抽取弱；比 pymupdf 慢(基于 pdfminer.six)。

【链接】https://github.com/jsvine/pdfplumber

---

## pypdf

【是什么】纯 Python PDF 库，读文本/元数据/书签、合并拆分旋转加密、表单。读内嵌文本(非 OCR)。

【可复用方法】
- 读：`from pypdf import PdfReader; reader=PdfReader("f.pdf"); reader.pages[0].extract_text()`。
- 版面模式：`extract_text(extraction_mode="layout")` 定宽对齐；`layout_mode_space_vertically=False` 去多余竖白。
- 朝向过滤：`extract_text(0)` 只正立、`extract_text((0,90))` 含左旋。
- Visitor：`extract_text(visitor_text=fn)`，fn 收(text,cm,tm,font_dict,font_size)，`tm[5]` 是 y 坐标可按区域过滤。
- 写：`PdfWriter` 的 `add_page/merge/append/encrypt(userpw,ownerpw)/add_metadata`；`PageObject` 的 `rotate/scale/merge_page`(水印)。
- 表单：`reader.get_fields()`、`writer.update_page_form_field_values(...)`。

【已知坑】非 OCR(纯图扫描件不行)；解析内容流吃内存(300MB 未压缩流见过要 10GB RAM，用 `len(page.get_contents().get_data())` 防 OOM)；空白/换行重建靠启发式；无语义层(无 header/table 结构信息)。表格/结构化抽取配 pdfplumber。

【链接】https://pypdf.readthedocs.io/en/stable/user/extract-text.html

---

## python-docx

【是什么】创建/修改 .docx 的 Python 库(v1.2.0, python-openxml)。文本/标题/run、表格、图片、样式、节/页眉页脚/分页。

【可复用方法】
- `from docx import Document; document=Document()`。
- 文本：`add_heading('T',0)`、`add_paragraph('x')`、`p.add_run('bold').bold=True`。
- 图片：`add_picture('img.png', width=Inches(1.25))`。
- 表格：`add_table()`，`table.rows[i].cells` 访问。
- 读：遍历 `doc.paragraphs`→`paragraph.runs`→`run.text/bold/italic`；`doc.tables`。
- 样式：内置 'List Bullet'/'Intense Quote' 等；Section 设页面/页眉页脚。

【已知坑】**不支持修订(tracked changes)、不能渲染成 PDF/图、复杂格式无完整往返保真**。仅覆盖 OOXML 段落/表格/图片模型，非全部 Word 特性。需修订时改用 Anthropic DOCX skill 的裸 XML `<w:ins>/<w:del>` 路线或 pandoc。

【链接】https://python-docx.readthedocs.io/en/latest/

---

## openpyxl

【是什么】读写 Excel 2010 xlsx/xlsm/xltx/xltm 的 Python 库(v3.1.3, MIT)。

【可复用方法】
- 加载：`load_workbook(filename, data_only=False, read_only=False, keep_vba=False)`；`data_only=True` 返回缓存值(需 Excel 之前算过并保存)。
- 单元格：`ws['A1']`、`ws.cell(row,col)`、`iter_rows`、`ws.values`。
- 样式：Font/PatternFill/Border/Alignment/NamedStyle。
- 大文件用 `read_only`/`write_only` 模式省内存。
- 支持图表、合并单元格、列宽、条件格式(有约束)。

【已知坑】**无公式求值引擎**(公式只存字符串不计算)——配 Anthropic XLSX skill 的 `recalc.py`(用 LibreOffice 重算)或读取 `data_only` 缓存值；默认不防 quadratic blowup / billion laughs XML 攻击，装 `defusedxml` 缓解；大文件吃内存。

【链接】https://openpyxl.readthedocs.io/en/stable/
