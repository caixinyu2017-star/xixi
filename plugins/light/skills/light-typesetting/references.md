# light-typesetting 参考工具笔记

逐工具核查笔记。每条尽量给真实命令/选项/字段与可点链接。无法核实者如实标注。

## Venue Templates（期刊/会议官方模板）
【是什么】出版方为每个 venue 提供的官方排版骨架（LaTeX `.cls` 或 Word `.docx`），规定版式、字号、页边距、参考文献样式与匿名规则。不是单一软件，而是分发在各出版方 author kit、CTAN、Overleaf gallery 上的一类资产。
【可复用方法】
- 取模板优先级：venue 官网 author kit > Overleaf 官方模板页 > CTAN 包。永远不要手搓版式去"模仿"官方样式。
- Overleaf gallery 按标签检索：`overleaf.com/gallery/tagged/conference-paper`、`/tagged/acm`、`/tagged/academic-journal`，可直接 "Open as Template" 拿到可编译工程。
- 模板里通常自带 `bare_*.tex`（IEEE）或 `sample-*.tex`（ACM）骨架文件，从骨架改而不是从空文件起。
- 关键校验项：单/双栏、页数上限、字号、参考文献 `.bst`/CSL、是否要求匿名（双盲）。
【链接】
- Overleaf gallery: https://www.overleaf.com/gallery/tagged/conference-paper
- CTAN: https://ctan.org/
【已知坑】会议每年模板可能更新（如 NDSS 提供 `bare_conf_LAST-X2026.tex` 年度版本）；务必用当届指定版本，旧版会被 desk-reject。

## PACSOMATIC
【是什么】**未能核实。** 以该名称做 WebSearch 未找到任何对应的排版工具、库或项目；最接近的命中是无关的个人站点 `pacomatic1.github.io`。疑似名称有误或为私有/小众工具。
【建议】若用户提到此名，先向用户确认全称/来源链接，再决定是否采用；不要假定其功能。
【链接】无可靠来源。

## Overleaf
【是什么】基于云的协作式 LaTeX 编辑器，自带完整 TeX Live、实时协同、模板库、版本历史。
【可复用方法】
- 编译引擎在 Menu 里切换：pdfLaTeX / XeLaTeX / LuaLaTeX；中文工程选 XeLaTeX 或 LuaLaTeX 配 `ctex`。
- 后台用 latexmk 驱动多轮编译（含 bibtex/biber）。可在工程放 `latexmkrc` 自定义。
- 同步方式：付费版支持 Git（`git clone https://git.overleaf.com/<project-id>`）与 GitHub 双向同步；免费可用 "Download as zip" 导出可编译源工程。
- "Open as Template" 直接克隆 venue 官方模板。
【链接】https://www.overleaf.com/learn
【已知坑】免费版有单次编译超时；大工程或大量 TikZ 易超时，可关闭草稿包或本地编译。Git/GitHub 同步是付费功能。

## LaTeX
【是什么】基于 TeX 的文档排版系统，学术论文事实标准。
【可复用方法（论文常用包）】
- 数学：`amsmath`、`amssymb`、`mathtools`；定理 `amsthm`。
- 图表：`graphicx`（`\includegraphics`）、`booktabs`（三线表 `\toprule/\midrule/\bottomrule`）、`subcaption`（子图）。
- 算法：`algorithm2e` 或 `algorithmic`/`algpseudocode`(algorithmicx)。
- 交叉引用：`\label`/`\ref`，配 `cleveref` 用 `\cref`（自动带 "Fig./Eq." 前缀，注意 `\usepackage{cleveref}` 要最后加载）。
- 中文：`ctex` 宏包/文档类，配合 XeLaTeX/LuaLaTeX。
- 参考文献：传统 `bibtex` + `.bst`，或现代 `biblatex` + `biber`（后者排序/本地化更强）。
【链接】https://en.wikipedia.org/wiki/LaTeX ；包文档查 https://ctan.org/pkg/<name>
【已知坑】`cleveref` 与 `hyperref` 加载顺序敏感（hyperref 先、cleveref 后）；biblatex 与 bibtex 工作流不可混用。

## TeX Live
【是什么】跨平台的完整 TeX 发行版，含 `tlmgr` 包管理器。
【可复用方法】
- 装包：`tlmgr install <pkg>`；更新自身后再更新全部：`tlmgr update --self` 然后 `tlmgr update --all`。
- 查包/找文件归属：`tlmgr search --global --file <name.sty>`。
- 安装方案（scheme）：`scheme-full`（全量，省去缺包烦恼）vs `scheme-basic`/`scheme-small`（轻量，按需补包）。
- 无 root 时可装到 `~/texmf`，或用 TinyTeX。
【链接】https://tug.org/texlive/ ；tlmgr 手册 https://manpages.ubuntu.com/manpages/questing/man1/tlmgr.1.html
【已知坑】发行版有年度版本（texlive 2024/2025…），`tlmgr` 不能跨年度大版本升级，跨年需重装；CTAN 镜像校验失败时换镜像。

## latexmk
【是什么】Perl 写的 LaTeX 自动化构建工具，自动判定需要跑几轮、何时跑 bibtex/biber 直到引用/目录收敛。
【可复用方法（核心选项）】
- `latexmk -pdf file.tex`：用 pdflatex 出 PDF。`-pdfxe`/`-xelatex` 用 XeLaTeX；`-pdflua`/`-lualatex` 用 LuaLaTeX。
- `-pvc`：持续预览，监视源文件改动自动重编。
- `-interaction=nonstopmode`：报错不停顿，适合自动化/CI。
- `-bibtex` 强制、`-bibtex-` 禁止跑 bibtex。
- `-shell-escape`：开启 `\write18`（minted、部分 TikZ 外部化需要）。
- 清理：`-c` 删中间文件（保留 PDF），`-C` 连 PDF 一起删。
- `-f` 出错继续，`-g` 强制重跑，`-outdir=DIR` 指定输出目录。
- 配置文件 `latexmkrc`/`.latexmkrc`：设 `$pdf_mode=1`（pdflatex）/`4`（lualatex）/`5`（xelatex）、`$pdflatex`、`$bibtex_use`、`@default_files`。
【链接】https://mg.readthedocs.io/latexmk.html ；手册 https://man.archlinux.org/man/latexmk.1
【已知坑】中文/特殊字体务必用 `-xelatex`/`-lualatex`，否则字体报错；minted 需配合 `-shell-escape`；biber 工程要确保 `.bcf` 触发 biber 而非 bibtex。

## latexdiff（返修标红 / tracked changes）
【是什么】对比 LaTeX 源的新旧两版，生成"标红 diff"——新增文字加下划线、删除文字加删除线，编译出可视化修订稿。返修（m14 light-review-rebuttal）要给审稿人"改前改后"对照时的标准工具。
【可复用方法（核心命令）】
- 基本：`latexdiff old.tex new.tex > diff.tex`，再 `latexmk -pdf diff.tex`（中文用 `-xelatex`）得标红 PDF。
- 多文件项目：先 `--flatten` 展开 `\input`/`\include` 再 diff：`latexdiff --flatten old_main.tex new_main.tex > diff.tex`。
- 与 git 配合（最省事）：`latexdiff-vc --git -r <旧tag/commit> main.tex` 自动取旧版对比当前；或 `latexdiff-vc -r REV1 -r REV2 main.tex` 比两个修订。
- 中文/复杂公式炸点（高频）：中文宏包（ctex/xeCJK）或复杂公式环境下，逐符号标记常破坏编译——降级 `--math-markup=0`（公式整体当一块不逐符号标）、加 `--encoding=utf8`；仍炸可试 `--type=CFONT` 或对公式段用 `%DIF` 手动豁免。
【链接】CTAN https://ctan.org/pkg/latexdiff ；手册 https://mirrors.ctan.org/support/latexdiff/doc/latexdiff-man.pdf
【已知坑/局限】**latexdiff 是 Perl 脚本，依赖 Perl 模块 `Algorithm::Diff`**——本机 MiKTeX 自带 latexdiff 但缺该模块，`latexdiff --version` 即报 `Can't locate Algorithm/Diff.pm`，**本机未跑通输出（2026-06-11 实测，标 GAP）**；TeX Live 通常自带完整 Perl 依赖，MiKTeX 需 `cpan Algorithm::Diff` 或装 Strawberry Perl。命令流程为公开文档整理，使用前确认本机 Perl 环境。复杂宏包/自定义命令可能使标记编译失败，先小范围试。
【与 m14 返修互引】light-review-rebuttal 要求"正文改动用 tracked changes/颜色标注、给改前改后页码"，LaTeX 项目即用 latexdiff 生成该标红稿（见 light-review-rebuttal `light-review-rebuttal/references.md` 的 revision_response_template）；Word 流程的 tracked changes 见本文件「Word 学术排版」节。

## TinyTeX
【是什么】基于 TeX Live 的精简发行版，主打"够用 + 缺包自动装"，由 R 的 `tinytex` 包维护，亦可独立安装。
【可复用方法】
- R 内安装：`tinytex::install_tinytex()`；编译：`tinytex::latexmk("file.tex")`，编译时**自动探测并安装缺失的 LaTeX 包**（最省心的特性）。
- 装包：`tinytex::tlmgr_install("<pkg>")`；底层仍是 `tlmgr`。
- 命令行也有 `tlmgr`/`pdflatex`/`xelatex` 包装器；安装目录 `~/.TinyTeX`（或 `~/Library/TinyTeX`）。
- 适合 CI / 容器 / 个人机：初装小（几百 MB），按需膨胀。
【链接】https://yihui.org/tinytex/ ；https://github.com/rstudio/tinytex
【已知坑】超大依赖（如完整 CJK、某些字体包）首次自动装会变慢；需联网；R 工作流外用要确认 PATH 已含 TinyTeX bin。

## Pandoc
【是什么】通用文档转换器，markdown/docx/tex/html 等互转，论文场景常用于 md↔docx↔tex 与统一参考文献渲染。
【可复用方法】
- md→docx 套样式：`pandoc in.md -o out.docx --reference-doc=ref.docx`（`ref.docx` 提供标题/正文/题注样式，先 `pandoc -o ref.docx --print-default-data-file reference.docx` 改后复用）。
- md→PDF：`pandoc in.md -o out.pdf --pdf-engine=xelatex`（中文用 xelatex/lualatex）。
- 参考文献：`--citeproc --bibliography=refs.bib --csl=style.csl`，CSL 决定输出样式（如 GB/T 7714 可用对应 CSL）；引用语法 `[@key]`。
- md→tex：`-t latex`；可配 `--template=custom.tex` 与 YAML metadata 头注入标题/作者。
- 提取 docx 内容做转换前清洗，配合下游 LaTeX。
【链接】手册 https://pandoc.org/MANUAL.html ；引用 https://pandoc.org/MANUAL.html#citations
【已知坑】复杂 LaTeX 宏/TikZ 转 docx 会丢失；`--citeproc` 用 CSL（非 .bst），与 LaTeX 的 bibtex/.bst 是两套体系；公式转 docx 走 OMML，复杂公式可能走样。

## DOCX skill（anthropics/skills 的 docx）
【是什么】Anthropic 官方文档技能之一，让模型创建/编辑 Word 文档。
【可复用工作流】
- 新建：从 markdown 经 Pandoc 生成 `.docx`，或用 JS 库 docx (docx-js) 以代码构造段落/表格/样式。
- 编辑既有文件：`.docx` 本质是 zip，解包后直接改 `word/document.xml`（及 `styles.xml`），保留原结构再重新打包，避免整篇重排丢格式。
- 修订/红线（tracked changes）：在 OOXML 里用 `<w:ins>`/`<w:del>` 标记插入/删除，配作者与时间戳。
- 用样式（Styles）控制层级，而非手动字号字体。
【链接】https://github.com/anthropics/skills/tree/main/skills/docx
【已知坑】手改 XML 易破坏文档完整性，改后需校验能正常打开；样式名称需与模板一致才能"套上"。（注：具体实现细节以仓库 SKILL.md 为准，本环境无法抓取页面正文。）

## PDF skill（anthropics/skills 的 pdf）
【是什么】Anthropic 官方文档技能之一，处理 PDF 读取/生成/表单/拆合并。
【可复用工作流】
- 文本/表格抽取：`pdfplumber`（`page.extract_text()` / `extract_tables()`）。
- 页操作：`pypdf` 做 merge/split/rotate、读写元数据、加密。
- 表单填写：`pypdf` 读取 AcroForm 字段并写值。
- 从零生成：`reportlab` 画版面，或先出 HTML/LaTeX 再转 PDF。
【链接】https://github.com/anthropics/skills/tree/main/skills/pdf
【已知坑】扫描件无文本层需 OCR；复杂版式抽取易错行错列；本环境无法抓取页面正文，库分工以仓库 SKILL.md 为准。

## MarkItDown（microsoft/markitdown）
【是什么】微软开源 Python 工具，把各类文件转成 Markdown，主打喂给 LLM/RAG。
【可复用方法】
- 安装 `pip install markitdown`（可带 extras）。
- 用法：`from markitdown import MarkItDown; md = MarkItDown(); print(md.convert("file.pdf").text_content)`。
- 支持 PDF、Word、PowerPoint、Excel、图片（可接 LLM 生成图注）、HTML、音频转写等。
- 提供 MCP server，可作为工具接入 agent。
【链接】https://github.com/microsoft/markitdown
【已知坑】保留的是"内容结构"而非精确版式，不适合做"还原排版"，适合做内容提取/转写；复杂表格与多栏 PDF 可能错乱。

## IEEEtran（IEEE 论文文档类）
【是什么】IEEE 期刊/会议官方 LaTeX 文档类。
【可复用方法】
- `\documentclass[conference]{IEEEtran}`（会议双栏）；期刊用默认/`journal`；`technote`、`peerreview`，计算机学会用 `compsoc` 选项。
- 作者块：`\author{\IEEEauthorblockN{Name}\IEEEauthorblockA{Affiliation\\email}}`。
- 关键词：`\begin{IEEEkeywords}...\end{IEEEkeywords}`；首字下沉 `\IEEEPARstart{T}{he}`。
- 参考文献：`\bibliographystyle{IEEEtran}` + `IEEEtran.bst`。
- 骨架文件：`bare_conf.tex`、`bare_jrnl.tex`、`bare_conf_compsoc.tex` 等。
【链接】README https://tug.org/docs/latex/ieeetran/README ；CTAN https://ctan.org/pkg/ieeetran
【已知坑】双栏下宽图用 `figure*`/`table*` 跨栏并多放在页顶；作者多行对齐需用 `\IEEEauthorblockN` 内换行或 `\and`；匿名投稿手动去作者信息。

## acmart（ACM 论文文档类）
【是什么】ACM 期刊与会议统一文档类。
【可复用方法】
- `\documentclass[sigconf]{acmart}`（会议双栏）；其它格式 `manuscript`（审稿单栏行距大）、`acmsmall`/`acmlarge`/`acmtog`（期刊）、`sigplan`、`sigchi`。
- 匿名审稿：`\documentclass[sigconf,review,anonymous]{acmart}`。
- 版权：`\setcopyright{...}`、`\acmConference[短名]{全名}{日期}{地点}`、`\acmDOI`、`\acmISBN`。
- 分类：CCS concepts `\begin{CCSXML}...\end{CCSXML}` + `\ccsdesc[500]{...}`（从 https://dl.acm.org/ccs 生成）；`\keywords{...}`。
【链接】CTAN https://ctan.org/pkg/acmart ；CCS https://dl.acm.org/ccs
【已知坑】缺版权信息会出红色提示框；`review` 加行号、`anonymous` 自动隐藏作者；最终版需填 venue 提供的 rights/DOI 信息。

## Springer LNCS（llncs.cls）
【是什么】Springer Lecture Notes in Computer Science 会议论文集文档类。
【可复用方法】
- `\documentclass{llncs}`；作者：`\author{Name\inst{1}}`，机构 `\institute{Org\\\email{a@b.c}}`。
- 页眉短名：`\titlerunning{}`、`\authorrunning{}`（作者多时必填，否则页眉溢出）。
- 摘要+关键词：`\begin{abstract}...\keywords{...}\end{abstract}`。
- 参考文献：`\bibliographystyle{splncs04}`（Springer 当前推荐 bst）。
【链接】CTAN https://ctan.org/pkg/llncs ；说明文档 llncsdoc。
【已知坑】Springer 要求用 `splncs04` 而非自选样式；不要随意改页边距/字号，会被退回；作者机构编号用 `\inst{}` 对应。

## elsarticle（Elsevier 论文文档类）
【是什么】Elsevier 期刊投稿用 LaTeX 文档类。
【可复用方法】
- 投稿（双倍行距审稿）：`\documentclass[preprint,review,12pt]{elsarticle}`；终排版式 `[final,5p,times,twocolumn]`，版式选项 `1p`(单栏)/`3p`/`5p`。
- 前置信息放 `\begin{frontmatter}...\end{frontmatter}`，含 `\title`、`\author[label]{}`、`\affiliation[label]{organization=...}`、`\cortext`（通讯作者）、`\begin{abstract}`、`\begin{keyword}`。
- 参考文献：`elsarticle-num`（数字）/`elsarticle-num-names`/`elsarticle-harv`（作者年）。
【链接】CTAN https://ctan.org/pkg/elsarticle ；模板 https://www.overleaf.com/latex/templates/elsevier-article-elsarticle-template/vdzfjgjbckgz
【已知坑】不同期刊指定不同参考文献模型，投前查 guide for authors；`review` 选项才出行号与宽行距，便于审稿批注。

## GB/T 7714 BibTeX 样式（zepinglee/gbt7714）
【是什么】实现中国国标 GB/T 7714-2015 文后参考文献格式的 BibTeX/biblatex 方案，CTAN 包名 `gbt7714`。
【可复用方法】
- BibTeX 路线：`\usepackage{gbt7714}` 提供 `\citet`/`\citep`；`\bibliographystyle{gbt7714-numerical}`（顺序编码）或 `gbt7714-author-year`（著者-出版年）。
- 条目需带 `language`/`langid` 区分中英文（影响 "等" vs "et al."、句点等）；电子/网络资源、arXiv、标准等类型需正确的 entry type 与字段（issue #89/#134 讨论 arXiv DOI、`[C]/[J]` 文献类型标识）。
- 现代 biblatex 路线另有 `biblatex-gb7714-2015`（配 biber）。
【链接】仓库 https://github.com/zepinglee/gbt7714-bibtex-style ；CTAN https://ctan.org/pkg/gbt7714
【已知坑】中英文混排时 `langid` 缺失会导致文献类型标识/缩写错误；InProceedings 不显示 `[C]` 等是字段/版本问题（见 issue #32）；biblatex 版与 bibtex 版不可混用。

## Word 学术排版（研究日期 2026-06-11）
【是什么】国内学位论文与多数中文期刊投稿走 Word 路线（官方多只发 `.docx` 模板，不提供 `.cls`）。本节把 Word 侧排版做成可执行清单，密度对齐上面的 LaTeX 路线；两条路线各管各的，不互相重复。
【核心 checklist（按此顺序做，做一项划一项）】
1. **先套官方模板再写正文**：从学校研究生院/期刊 author kit 下 `.docx`，"另存为"成自己的文件，正文写进模板的样式里，绝不在空白文档手搓版式。
2. **一切层级用"样式"，不手动调字号**：标题 1/2/3、正文、图题、表题、参考文献都套样式面板里的命名样式；要改全局外观就改样式定义（右键样式→修改），不要逐段手刷。
3. **多级列表绑定标题样式**：用"定义新的多级列表"把级别 1-3 链接到"标题 1/2/3"，章节号才会自动连号（1 → 1.1 → 1.1.1），手敲序号必乱。
4. **图表用题注 + 交叉引用**：插入→题注（`图`/`表` 标签，可设"包含章节号"），正文引用处用"交叉引用"指向题注，不要手打"图 3"。这样增删图后编号能自动更新。
5. **公式**：用内置公式编辑器（Alt+=）或 MathType；编号靠右用制表位或单行三列表格，编号本身可用题注+交叉引用维护。
6. **域要手动刷新**：目录、图表目录、交叉引用、页码都是"域"，改完内容要 `Ctrl+A` 全选后按 `F9` 更新；打印/导出前务必刷一遍。
7. **分节符控版式**：封面/摘要/正文页码格式不同时用"分节符（下一页）"分开，再到"页眉页脚"取消"链接到前一节"，分别设页码（罗马数字 vs 阿拉伯数字）。
8. **自动目录**：引用→目录→自动目录，依赖标题样式正确套用；改了标题后回到目录"更新整个目录"。
9. **参考文献插件**：Zotero / EndNote 的 Word 插件按 GB/T 7714 CSL/输出样式插入并自动编号；定稿前点"移除域代码"前先备份（去域后不可再自动更新）。
10. **交稿前过"文档检查器"**：文件→信息→检查文档，清掉批注/修订/隐藏文字/个人信息（双盲送审尤其要清作者属性）。
【常见错误对照表（现象 → 原因 → 修法）】

| # | 现象 | 原因 | 修法 |
|---|------|------|------|
| 1 | 改一处字号，全文没跟着变 | 手动刷字号而非改样式 | 改"正文"样式定义，让段落都引用样式 |
| 2 | 章节号 1.1.1 串乱/不连号 | 多级列表没绑定标题样式 | 重新"定义新多级列表"链接到标题 1/2/3 |
| 3 | 删了一张图，后面图号没更新 | 编号是手打的死数字 | 用题注+交叉引用，删后 F9 更新 |
| 4 | 目录页码与正文对不上 | 改完没更新域 | 目录右键→更新整个目录 |
| 5 | 正文和摘要页码连号无法分开 | 没插分节符就改页码 | 插"分节符(下一页)"，断开"链接到前一节" |
| 6 | 中英文字体混乱（宋体里夹了 Calibri） | 只设了中文字体没设西文字体 | 字体对话框分别设中文/西文字体 |
| 7 | 行距忽大忽小 | 段落"如果定义了文档网格则对齐"勾着 | 取消该勾选，统一行距值 |
| 8 | 三线表变成全框线表 | 用了默认表格样式 | 套"无边框"后只加上/中/下三条线，或用三线表样式 |
| 9 | 图片乱跑/压字 | 环绕方式是"浮于文字上方" | 改"嵌入型"，图单独成段居中 |
| 10 | 公式行被压扁/行距异常 | 公式按"显示"插在正文行内 | 公式单独成段，用"显示公式"模式 |
| 11 | 粘贴外部文字带来一堆杂样式 | 直接 Ctrl+V 带格式 | 用"只保留文本"粘贴，再套样式 |
| 12 | 参考文献编号与正文引用对不上 | 手敲序号或域损坏 | 用 Zotero/EndNote 重新刷新域 |
| 13 | 标题出现在页面最后一行（孤行） | 没设"与下段同页" | 标题样式段落设置勾"与下段同页/段中不分页" |
| 14 | 目录里混进了不该有的标题 | 把正文误套了标题样式 | 把该段改回"正文"样式 |
| 15 | 页眉出现多余横线删不掉 | 横线是段落下边框 | 页眉段落→边框→无 |
| 16 | 交叉引用显示"错误!未找到引用源" | 被引目标被删/域失效 | 重新插入交叉引用，F9 更新 |
| 17 | 导出 PDF 后图变模糊 | 压缩了图片分辨率 | 文件→选项→高级，取消"丢弃编辑数据/降分辨率" |
| 18 | 中文标点占位过宽/挤压 | 用了半角标点或字体替换 | 统一全角中文标点，检查字体 |
| 19 | 同级标题字号/缩进不一致 | 个别段落被手改过 | 选中→"清除格式"后重套对应样式 |
| 20 | 修订模式下别人看到我的批注 | 没清修订/批注就交稿 | 接受/拒绝所有修订，删批注，过文档检查器 |
| 21 | 公式编号没法自动连号 | 编号是手打的 | 公式用题注(标签"公式")+交叉引用 |
| 22 | 图表目录是空的 | 没用题注，或没插图表目录域 | 用题注后引用→插入图表目录 |
【中文学位论文模板指针】
- LaTeX 路线（若学校允许）：清华 `thuthesis`（CTAN https://ctan.org/pkg/thuthesis ）、中科大 `ustcthesis`、北大 `pkuthss`，均为社区维护、对应各校格式规范。
- Word 路线（多数情况）：**以本校研究生院官网发布的官方 `.docx` 模板为唯一准绳**，不要从网上第三方"通用论文模板"改——各校页边距/字号/参考文献格式差异大且每年可能微调；下载后核对发布日期与适用届别。
【已知坑】Word 文档"看起来对"不等于"结构对"——评审/查重/送审系统按样式与域解析，手刷出来的外观在导出或换机后易崩；定稿前务必：全选 F9 更新域 → 文档检查器清隐私 → 另存一份"去域代码"的终稿副本备份。
