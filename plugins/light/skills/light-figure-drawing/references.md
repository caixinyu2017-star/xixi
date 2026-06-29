# light-figure-drawing 参考工具笔记

逐工具研究笔记，聚焦**可核查、可复用**的硬信息。所有链接均为官方文档/仓库。
本环境 WebFetch 被网络策略拦截，无法抓正文，下列细节以官方文档检索结果 + 既有可核查知识交叉确认；个别处标注置信度。

## Matplotlib

【是什么】Python 最底层、最可控的绘图库。一切 seaborn/pandas.plot 都建立在它之上。投稿图的"最后一公里"基本靠它。

【可复用方法/真实 API】
- 导出：`fig.savefig("f.pdf", dpi=600, bbox_inches="tight", pad_inches=0.02, transparent=True)`。矢量格式直接传 `.pdf/.svg/.eps`（dpi 对矢量无意义，只影响内嵌位图）；位图用 `.png` + `dpi=300/600`。
- 字体可编辑（投 AI/Illustrator 二次编辑必备）：`rcParams["pdf.fonttype"]=42`、`rcParams["ps.fonttype"]=42`（TrueType，不转曲线，文字仍可选中编辑）。
- 全局规范一次设好：`rcParams` 里 `font.family`、`font.size`、`axes.linewidth`、`lines.linewidth`、`savefig.dpi`、`figure.figsize`。可用 `plt.style.use("seaborn-v0_8-paper")` 或自定义 `.mplstyle` 文件统一全论文。
- 组图：`fig, axes = plt.subplots(2,2, figsize=(7,5), constrained_layout=True)`；不规则布局用 `GridSpec`（`fig.add_gridspec` + `subplotspec`），跨格用切片 `gs[0, :]`。`constrained_layout=True` 比 `tight_layout()` 更适合共享色标/图例。
- 物理尺寸控制：figsize 单位是英寸，按目标栏宽设（单栏≈3.5in，双栏≈7.2in），避免投稿后被缩放导致字号失真。
- 色盲友好 colormap：`viridis/cividis/magma`（感知均匀），分类用 `tab10`。
- **色觉模拟自检（Okabe-Ito 默认之上的复核手段）**：默认色环已是 Okabe-Ito 色盲安全，但配色定稿前仍建议**渲染模拟复核一遍**——跑 `python scripts/color_palettes.py`（或 `preview_palette()`）出原色/灰度/三种色盲对照图，有 `colorspacious` 走精确算法、缺则线性近似降级；无本地环境时用 Coblis 在线模拟器（color-blindness.com/coblis-color-blindness-simulator/）上传图核对。重点看相邻类别在 deuteranopia/protanopia 下是否仍可区分。

【链接】
- savefig: https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html
- 文字可编辑 PDF (fonttype 42): https://matplotlib.org/stable/users/explain/text/fonts.html
- constrained_layout: https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html

【已知坑】默认 `font.family` 不含 Times/Arial 需自行注册字体否则回退；`bbox_inches="tight"` 会改变最终物理尺寸（与精确栏宽要求冲突，二选一）；EPS 不支持透明，需透明背景用 PDF/SVG。

### SciencePlots vs 自有 mplstyle（对照与选用）
SciencePlots（garrettj403）是流行的 matplotlib 期刊风格包；本 skill 的 `assets/` 自带 `nature.mplstyle`/`science.mplstyle`/`publication.mplstyle` 三套。两者解决同一问题（统一论文图风格），但取舍不同：

| 维度 | SciencePlots | 本 skill 自有 mplstyle |
|---|---|---|
| 安装 | `pip install SciencePlots`，`import scienceplots` 注册 | 无需安装，`plt.style.use("assets/nature.mplstyle")` 直接用 |
| 风格 | `science`(核心)+`ieee`/`nature`+修饰 `scatter`/`notebook`/`grid`/`high-vis`+Paul Tol 色环+`no-latex`+`cjk-*` | nature/science/publication 三套，对齐 `figure_export.py` 的 `JOURNAL_SPECS` |
| **LaTeX 依赖** | **默认需本机装 LaTeX**，没装要显式加 `no-latex`（高频踩坑） | 不依赖 LaTeX，开箱即用 |
| 物理栏宽 | 风格不锁 figsize，栏宽要自己设 | `figure_export.py` 的 `save_for_journal` 按刊锁死物理 mm+最小字号 |
| 组合 | `plt.style.use(['science','ieee','grid'])` 可叠加 | 单文件，需叠加自行合并 rcParams |

**何时用哪个**：
- 直接 `pip install scienceplots` 用——快速出图、要 IEEE/高可视色环/scatter 等现成变体、且本机有 LaTeX（或加 `no-latex`）；风格多、社区活跃。
- 用自有 mplstyle——需要**精确栏宽+最小字号锁定**（走 `figure_export.py` 的导出校验链路 `check_figure_size`/`check_scaled_fonts`）、无 LaTeX 环境、或要与本 skill 的诚实性 lint/db07 模式衔接。
- 一行安装+引用：`pip install SciencePlots`；`import matplotlib.pyplot as plt; import scienceplots; plt.style.use(['science','nature'])`（无 LaTeX 改 `['science','nature','no-latex']`）。两者可混用：用 SciencePlots 出风格、仍用 `figure_export.py` 做栏宽/字号终检。

【链接】SciencePlots Gallery https://github.com/garrettj403/SciencePlots/wiki/Gallery ；Using the Styles https://github.com/garrettj403/SciencePlots/wiki/Using-the-Styles ；PyPI https://pypi.org/project/SciencePlots/

### tueplots：venue 字号/尺寸换算更全（可对照补 JOURNAL_SPECS）
tueplots（pnkraemer，~743★）按**具体会议/期刊**（NeurIPS/ICML/ICLR/JMLR/AISTATS/CVPR 等）精确设 figure size + 字号 + 字体，区分单/双/半栏，且**字号随栏宽联动**（窄栏自动用更小但仍达下限的字号）。本 skill 的 `JOURNAL_SPECS` 目前锁物理宽度+min_font_pt 下限，但不做"字号随栏宽自适应"。
- **何时直接用 tueplots**：投 ML 顶会（NeurIPS/ICML/ICLR…）且想要其 venue 预设字号/尺寸——`from tueplots import bundles; plt.rcParams.update(bundles.neurips2024())`，比手设省心，条目比 JOURNAL_SPECS 全。
- **可借鉴补强**：JOURNAL_SPECS 可对照 tueplots 增补更多 ML 会议条目，并考虑给 `save_for_journal` 加"窄栏建议字号"提示（非强制，仅在 column 偏窄时提示正文字号下调到下限附近）。当前仍以 min_font_pt 硬下限为准。
- 可混用：tueplots 出 venue rcParams、本 skill `figure_export.py` 做栏宽/dpi/格式/字体落空终检。

【链接】tueplots https://github.com/pnkraemer/tueplots



## Seaborn

【是什么】基于 matplotlib 的统计可视化高层封装，强在分类/分布/回归图和"一行出图 + 默认好看"。

【可复用方法/真实 API】
- 全局风格：`sns.set_theme(style=..., context=..., palette=...)`。`style` ∈ {darkgrid, whitegrid, white, dark, ticks}；投稿常用 `white`/`ticks` + `sns.despine()` 去顶/右边框。
- `context` ∈ {paper, notebook, talk, poster} 控制字号/线宽整体缩放——投稿选 `paper`，做 slides/海报选 `talk`/`poster`，一行切换不用逐个调字号。
- 调色板：`sns.color_palette("colorblind")`（8 色色盲安全）、`"viridis"`、`sns.color_palette("Set2")`；连续用 `sns.color_palette("rocket", as_cmap=True)`。
- **figure-level vs axes-level**（关键区分）：figure-level（`relplot/displot/catplot/lmplot`）自己管理整张 Figure，支持 `col=/row=` 分面、返回 `FacetGrid`，用 `g.savefig()` 存；axes-level（`scatterplot/boxplot/histplot/heatmap`）画在传入的 `ax=` 上，可与 matplotlib 自由拼图。组图想手动控制布局就用 axes-level + 自己的 subplots。

【链接】
- 主题/审美: https://seaborn.pydata.org/tutorial/aesthetics.html
- 调色板: https://seaborn.pydata.org/tutorial/color_palettes.html
- figure-level vs axes-level: https://seaborn.pydata.org/tutorial/function_overview.html

【已知坑】figure-level 函数不接受 `ax=`，硬塞进现成 subplots 会报错；`set_theme` 是全局副作用，会影响同进程后续所有 matplotlib 图。

## Plotly

【是什么】交互式可视化库（HTML/JS 渲染），强在 hover/缩放/3D/dashboard。投稿需要静态高分图时走 Kaleido 导出。

【可复用方法/真实 API】
- 静态导出：`fig.write_image("f.pdf", scale=3)` 或 `.png/.svg/.eps`。**依赖 `kaleido` 包**（`pip install -U kaleido`），新版 plotly 默认引擎已是 Kaleido（旧 orca 已弃用）。
- `scale` 参数放大像素密度（位图等效提高 dpi）；矢量直接出 `.pdf/.svg`。可在 `write_image` 里传 `width=/height=` 锁定像素尺寸。
- 布局/字体统一：`fig.update_layout(font=dict(family="Arial", size=12), template="simple_white")`；内置 template 有 `plotly_white/simple_white/none` 等，投稿用 `simple_white`。
- 子图：`from plotly.subplots import make_subplots; make_subplots(rows=, cols=, shared_xaxes=True)`。

【链接】
- 静态导出: https://plotly.com/python/static-image-export/
- Kaleido: https://github.com/plotly/Kaleido

【已知坑】Kaleido 安装/Chromium 依赖在受限环境常失败（导出报错的头号原因）；交互特性导出成静态后全部丢失；默认主题背景偏"网页风"，不改 template 不像期刊图。

## Altair

【是什么】基于 Vega-Lite 的声明式可视化库（grammar of graphics 的 JSON 实现）。强在用"编码通道"声明式描述图，代码简洁、可复现性强。

【可复用方法/真实 API】
- 保存：`chart.save("f.png")` / `.svg` / `.pdf` / `.html` / `.json`。PNG/SVG/PDF 导出**依赖 `vl-convert-python`**（`pip install vl-convert-python`，纯 Rust，无需 node/Chromium，已取代旧 `altair_saver`）。
- 提分辨率：`chart.save("f.png", scale_factor=3.0)`（PNG 放大像素）；矢量首选 `.svg`/`.pdf`。
- 语法核心：`alt.Chart(df).mark_point().encode(x="a:Q", y="b:Q", color="c:N")`，类型后缀 `:Q`(定量)/`:N`(名义)/`:O`(有序)/`:T`(时间)。组图用 `chart1 | chart2`（水平）、`chart1 & chart2`（垂直）、`alt.concat(...)`。
- 数据上限：默认 5000 行限制，超出 `alt.data_transformers.enable("vegafusion")` 或 disable_max_rows。

【链接】
- 保存图表: https://altair-viz.github.io/user_guide/saving_charts.html
- vl-convert: https://pypi.org/project/vl-convert-python/

【已知坑】无 vl-convert 时只能存 HTML/JSON；5000 行默认上限是新手常踩；声明式范式自定义细节（如非常规注释）不如 matplotlib 灵活。

## ggplot2 (R)

【是什么】R 的图形语法标杆库（tidyverse 一员），`ggplot(data) + aes() + geom_*()` 分层叠加。统计图表达力与一致性极强。

【可复用方法/真实 API】
- 导出：`ggsave("f.pdf", plot=p, width=7, height=5, units="in", dpi=600, device=cairo_pdf)`。`units` ∈ in/cm/mm，按栏宽精确设尺寸；`device=cairo_pdf` 解决字体嵌入/中文问题。
- 投稿主题：`theme_classic()`（仅左下轴线，最干净）、`theme_bw()`、`theme_minimal()`；细调用 `theme(text=element_text(family="Arial", size=10), legend.position="top")`。
- 色盲友好：`scale_color_viridis_c()`(连续)/`scale_color_viridis_d()`(离散)/`scale_fill_brewer(palette="Set2")`。
- 分面（强项）：`facet_wrap(~var)` / `facet_grid(row~col)` 一行做规整组图，共享坐标轴自动对齐。
- 组合多图：`patchwork` 包 `p1 + p2 / p3` 拼版并自动对齐；`plot_annotation(tag_levels="a")` 自动加 (a)(b)(c)。

【链接】
- 官网: https://ggplot2.tidyverse.org/
- 入门 vignette: https://ggplot2.tidyverse.org/articles/ggplot2.html
- patchwork: https://patchwork.data-imaginist.com/

【已知坑】默认灰底网格（`theme_gray`）不像期刊图，必换主题；字体嵌入 PDF 需 cairo 设备否则投稿系统可能报字体未嵌入；离散色标超过 ~8 类需手动指定调色板。

## R base graphics

【是什么】R 自带的底层绘图系统（grDevices + graphics 包），不依赖 ggplot2。胜在零依赖、出图快、与统计输出（如 `plot.lm`、`hist`、`boxplot`）无缝。

【可复用方法/真实 API】
- 设备模型："打开设备 → 画 → 关闭"：`pdf("f.pdf", width=7, height=5)` 或 `png("f.png", width=7, height=5, units="in", res=600)`；画完 `dev.off()` 才落盘。位图设备用 `type="cairo"` 抗锯齿更好。
- 多图布局：`par(mfrow=c(2,2))` 规则网格；`layout(matrix(...))` 做不等大小布局；`par(mar=c(b,l,t,r))` 调边距（单位行高）。
- 全局参数 `par()`：`cex`(整体缩放)、`lwd`(线宽)、`pch`(点型)、`family`(字体)、`las`(刻度方向)。

【链接】
- grDevices/Devices: https://stat.ethz.ch/R-manual/R-devel/library/grDevices/html/Devices.html
- par: https://stat.ethz.ch/R-manual/R-devel/library/graphics/html/par.html

【已知坑】忘记 `dev.off()` 文件损坏/为空是最常见错误；`par(mfrow)` 状态会污染后续绘图需 reset；与 ggplot 对象不能混用同一 par 布局（grid 系统不同）。

## MATLAB / Octave

【是什么】MATLAB：商业数值计算环境，绘图引擎成熟、矢量导出质量高。Octave：开源近似兼容替代，绘图能力较弱、导出选项少。

【可复用方法/真实 API（MATLAB）】
- **首选导出 `exportgraphics`**（R2020a+）：`exportgraphics(ax, "f.pdf", "ContentType","vector")` 出真矢量；位图 `exportgraphics(ax,"f.png","Resolution",600)`。比旧 `print`/`saveas` 裁白边更干净。
- `ContentType` ∈ `"vector"`/`"image"`/`"auto"`；可传 figure、axes 或 tiledlayout 句柄（传 layout 句柄可整组导出）。
- 组图用 `tiledlayout(2,2)` + `nexttile`（R2019b+，取代 `subplot`，间距更紧凑，支持 `TileSpacing="compact"`、`Padding="compact"`）。
- 尺寸：设 `fig.Units="inches"; fig.Position=[0 0 3.5 2.6]` 锁物理尺寸。

【链接】
- exportgraphics: https://www.mathworks.com/help/matlab/ref/exportgraphics.html
- 保存特定尺寸/分辨率: https://www.mathworks.com/help/matlab/creating_plots/save-figure-at-specific-size-and-resolution.html

【已知坑】Octave 不支持 `exportgraphics`/`tiledlayout`（需用 `print -dpdf`/`subplot`），脚本跨平台前要确认版本；MATLAB 旧 `saveas` 出的 EPS/PDF 常有多余白边，应换 exportgraphics。

## OriginLab (Origin)

【是什么】Windows 平台老牌科研绘图/分析软件，模板丰富、对期刊尺寸/分辨率支持细致，理工科论文常见。

【可复用方法/真实 API】
- 导出对话框（Export Graphs）支持 EPS/PDF/TIFF/EMF/AI 等；关键是**按出版商要求精确设尺寸与分辨率**：在 Export 设置里指定 Width/Height + DPI（位图常 TIFF 600 dpi；线条图可更高）。
- 矢量：可导出 PDF/EPS，或 `Export as AI`（直接给 Illustrator 二次编辑）。
- 可脚本化：LabTalk `Image.Export` 对象批量导出；模板（.otp）固化样式实现一致风格批量出图。

【链接】
- 导出图到图像文件: https://www.originlab.com/doc/Origin-Help/ExpGraph-to-Image
- FAQ-441 精确尺寸与分辨率: https://www.originlab.com/doc/Quick-Help/Set-ExpGraph-Size-Resolution
- 导出为 AI: http://cloud.originlab.com/doc/en/Quick-Help/Export-Graphs-as-AI

【已知坑】仅 Windows、商业授权；GUI 重度依赖，自动化需 LabTalk/Origin C 学习成本；版本间模板兼容性需注意。

## TikZ / PGFPlots (LaTeX)

【是什么】LaTeX 内的矢量绘图（TikZ）与数据绘图（PGFPlots）系统。最大优势：**字体/字号与正文完全一致**，公式排版原生，输出纯矢量。框架图、示意图、坐标图皆可。

【可复用方法/真实 API】
- PGFPlots 骨架：`\begin{tikzpicture}\begin{axis}[xlabel=,ylabel=,legend pos=north west] \addplot table {data.dat}; \addplot coordinates {(1,2)(2,3)}; \end{axis}\end{tikzpicture}`。
- 全局样式：导言区 `\pgfplotsset{compat=1.18, every axis/.append style={...}}` 统一所有图样式。
- `\addplot` 数据源：`table`(读文件/列)、`coordinates`(内联)、`expression`(函数)、`+[red,mark=*]` 设线型标记。
- 独立编译加速：`external` 库 `\usetikzlibrary{external}\tikzexternalize` 把每张图缓存为单独 PDF，避免每次全文重编译。

【链接】
- 完整在线手册: https://tikz.dev/
- \addplot 参考: https://tikz.dev/pgfplots/reference-addplot
- axis 环境: https://tikz.dev/pgfplots/reference-axis

【已知坑】编译慢（大数据集尤甚，需 external 或先抽样）；学习曲线陡；超大数据点直接内联会拖垮编译，应外置 .dat 或预降采样。

## Graphviz

【是什么】用 DOT 文本语言描述图，自动布局。适合流程图、依赖图、状态机、树——**结构由你写，位置自动算**。

【可复用方法/真实 API】
- DOT：`digraph G { rankdir=LR; node[shape=box,style=rounded]; A->B->C; A->C[style=dashed]; }`（`graph` 无向用 `--`，`digraph` 有向用 `->`）。
- 布局引擎（选错布局丑一半）：`dot`(分层/有向，最常用)、`neato`(弹簧模型/无向)、`fdp`(大型无向力导)、`circo`(环形)、`twopi`(放射)。命令行 `dot -Tpdf in.dot -o out.pdf` 或 `-Tsvg/-Tpng`。
- 关键属性：图级 `rankdir/ranksep/nodesep`；节点 `shape/style/fillcolor/fontname`；边 `label/style/arrowhead`；`rank=same` 强制同层对齐。
- Python 封装：`graphviz` 包 `Digraph()` 编程式生成。

【链接】
- 文档总览: https://graphviz.org/documentation/
- 布局引擎 dot: https://graphviz.org/docs/layouts/dot/
- 图属性: https://graphviz.org/docs/graph/
- Python 包: https://graphviz.readthedocs.io/en/stable/manual.html

【已知坑】自动布局不可像素级精控，追求特定排布要靠 `rank`/不可见边 hack；中文字体需显式 `fontname`；复杂图易交叉，需调 engine 而非硬调坐标。

## Mermaid

【是什么】Markdown 风格文本生成图（flowchart/sequence/class/state/gantt/ER 等）。GitHub/Notion/Typora 原生渲染，写文档随手出图最方便。

【可复用方法/真实 API】
- Flowchart：`graph TD`(上下) 或 `graph LR`(左右)；节点 `A[方框] B(圆角) C{菱形判断} D((圆))`；边 `A --> B`、`A -->|标签| B`、`A -.-> B`(虚线)。
- Sequence：`sequenceDiagram` + `Alice->>Bob: msg`、`activate/deactivate`、`alt/loop` 块。
- 渲染/导出：Mermaid Live Editor 在线导出 SVG/PNG；CLI `@mermaid-js/mermaid-cli` 的 `mmdc -i in.mmd -o out.svg/pdf/png` 批量出图。

【链接】
- 仓库: https://github.com/mermaid-js/mermaid
- Flowchart 语法: https://mermaid.js.org/syntax/flowchart.html
- Sequence 语法: https://mermaid.js.org/syntax/sequenceDiagram.html

【已知坑】样式/排版精控弱（不适合最终投稿级框架图，更适合文档/初稿）；复杂图自动布局拥挤；导出矢量后常仍需 Illustrator 精修。

## Inkscape

【是什么】开源矢量编辑器（SVG 原生）。在科研流程里常作"后处理站"：把 matplotlib/Origin 出的 SVG 拼版、改字体、统一线宽、转格式。

【可复用方法/真实 API（1.x CLI）】
- 转格式：`inkscape in.svg --export-type=pdf`（自动同名）；指定名 `--export-filename=out.pdf`；位图 `--export-type=png --export-dpi=600`。
- 区域/对象：`--export-area-drawing`(裁到内容)、`--export-area-page`、`--export-id=<obj>` 只导某对象。
- 批处理/复杂操作：`--actions="..."` 串联命令（1.x 取代了 0.92 的 `--export-pdf` 等老 flag）。可 `--shell` 进交互批处理。

【链接】
- Wikipedia（含 CLI 概览）: https://en.wikipedia.org/wiki/Inkscape
- man page: https://man.archlinux.org/man/inkscape.1.en
- 官网: https://inkscape.org/

【已知坑】**0.92 与 1.x 命令行 flag 不兼容**（老教程的 `--export-pdf` 在 1.x 失效，要用 `--export-type`），写脚本前先 `inkscape --version`；批量 `--actions` 后接附加问号参数曾有挂起 bug。

## Adobe Illustrator

【是什么】行业标准矢量编辑器。科研里用于：拼最终大图、画精美示意图、统一全文风格、出版商要求的 CMYK/EPS。

【可复用方法/工作流】
- 通用论文图工作流（多份高校指南一致）：各子图存**矢量 SVG/PDF/EPS** → 置入 Illustrator → 用**图层(Layers)**管理子图、用**画板(Artboards)**按目标尺寸建版 → 对齐(Align 面板)、统一字体字号线宽 → 加 (a)(b)(c) 标号 → 导出。
- 导出：`File > Export` / `Save As`，投稿按要求选 PDF(矢量)、EPS、或 TIFF(位图)；色彩模式按期刊选 RGB/CMYK（印刷常 CMYK）。
- 脚本化：JSX 脚本（如 MultiExporter.jsx）批量按图层/画板导出多格式。
- 关键原则：保持矢量到最后；文字保持可编辑（除非要求转曲）；线宽用绝对值（pt）不随缩放变。

【链接】
- 导出 artwork 官方: https://helpx.adobe.com/illustrator/using/exporting-artwork.html
- 出版图工作流指南: https://cloud.wikis.utexas.edu/wiki/spaces/khlab/pages/53544722/A+basic+workflow+for+putting+together+a+figure+for+publication
- 科研图指南仓库: https://github.com/nrokh/ScientificFigures

【已知坑】商业订阅；位图置入后放大失真（务必矢量源）；CMYK 与屏幕 RGB 颜色有偏差，投印刷前要校色；EPS 渐变/透明易出问题，新流程倾向 PDF。

## PowerPoint figure assembly (含 python-pptx)

【是什么】用 PPT 拼科研组图/做 graphical abstract/海报——门槛低、所见即所得。`python-pptx` 可编程生成，适合批量/模板化。

【可复用方法/真实 API（python-pptx）】
- 骨架：`from pptx import Presentation; from pptx.util import Inches, Pt; prs=Presentation(); slide=prs.slides.add_slide(prs.slide_layouts[6])`（layout 6 = 全空白，最适合自由拼图）。
- 插图：`slide.shapes.add_picture("f.png", Inches(1), Inches(1), width=Inches(3))`（只给 width 等比缩放）。
- 文本/标号：`slide.shapes.add_textbox(...).text_frame` 加 (a)(b)(c)；`add_shape` 加箭头/方框。
- 精确版面：所有位置/尺寸用 `Inches()`/`Pt()` 显式给，保证对齐；设 `prs.slide_width/height` 定画布。
- 导出高清图：PPT 本身导图分辨率低，置入**矢量或 600dpi 位图源**，最终走 PDF 或在外部转图。

【链接】
- python-pptx 文档: https://python-pptx.readthedocs.io/
- add_picture API: https://python-pptx.readthedocs.io/en/latest/api/shapes.html

【已知坑】PPT 直接"另存为图片"分辨率偏低、字体跨机器替换错乱；位图拉伸失真；适合拼版/初稿与 graphical abstract，最终投稿级精度仍建议 Illustrator/矢量流程。

## BioRender

【是什么】面向生命科学的在线科研插图工具，内置数万个经专家绘制的图标（细胞/蛋白/器官/实验装置），强在快速做机制图、实验流程图、graphical abstract。**仅手工网页使用——其官方 connector/MCP 只支持查询、不能作图，故不作为程序化/MCP 出图路径**（不在推荐 MCP 表内）。3D 结构/分子可视化改用 Blender（开源程序化，见 m09 figure-planning references「Blender」节）。

【可复用方法/工作流】
- 拖拽式画布：从图标库检索元素 → 拼装 → 连箭头/加文字 → 套模板。核心价值是**省去自己画生物结构**且风格统一专业。
- 导出：付费可导出高分辨率 PNG/PDF/（部分）矢量用于投稿；提供面向期刊发表的导出与授权说明。
- 适用：机制示意、实验设计图、综述配图、graphical abstract——不适合定量数据图（那是 matplotlib/Origin 的活）。

【链接】
- 功能页: https://biorender.com/features
- 期刊发表须知: https://help.biorender.com/hc/en-gb/articles/28577290921117-Publishing-BioRender-figures-in-a-journal-What-you-need-to-know

【已知坑】免费版有水印且高分辨率/矢量导出受限，**投稿前务必确认导出授权与分辨率**；图标版权归 BioRender，须按其条款署名/授权；只擅长示意图、不做数据可视化。

## 专利附图规范（服务 m15 light-ip-application；中国 CNIPA 制图要求）

【是什么】专利说明书附图与论文插图规则不同：以**黑白线条图**为原则、有严格的图号与标记规范、不追求美观而追求"清楚、可对应权利要求与说明书"。m15 的附图需求按本节执行，绘制工具仍用本技能的矢量链路（TikZ/Graphviz/Inkscape/matplotlib 黑白线条）。

【可复用规范（CNIPA《专利审查指南》制图要求）】
- **图号编排**：附图按出现顺序编"图1、图2…"（多图用"图1a/图1b"或"图1、图2"），与说明书「附图说明」逐图文字一一对应；说明书正文引用处与图号一致。一个发明的所有附图连续编号，不分章节重起。
- **附图标记（附图标记线/指引线）**：部件用阿拉伯数字标记，同一部件在各图中标记必须**前后一致**；指引线（引出线）从标记指向部件、**不得交叉**、不穿过其他标记；标记数字字号清晰（通常不小于正文），不写在阴影/线条密集处。说明书末尾或附图说明列**标记清单**（如"1—电机；2—传动轴；…"），每个出现的标记都要在说明书中解释。
- **黑白线条为原则**：附图用**黑色线条**绘制，原则上**不得着色、不用照片**；不得用工程蓝图/铅笔草图。剖面用均匀剖面线（影线），同一部件剖面线方向/间距一致；灰度阴影/底纹**受限**（易在公开印刷中糊成一团），能用线条表达就不用灰阶。确需照片（如金相图、电泳图）须说明理由并保证清晰可复制。
- **流程图 / 框图规范**：方法类发明常用流程图（步骤框 + 箭头，对应权利要求的方法步骤）、系统类用模块框图（模块框 + 连线，对应装置权利要求的部件）。框内文字简洁、步骤/模块与权利要求术语一致；箭头方向表数据/控制流向。流程图步骤宜与权利要求步骤可对应（便于"以说明书为依据"审查）。
- **图幅与清晰度**：线条均匀清晰、便于缩印后仍可辨（公开文本会缩小印刷）；不加图框装饰、不加与技术方案无关的文字标题（图号除外）。

【绘制工具落地】框图/流程图用 Graphviz 或 TikZ（黑白、矢量）；结构示意用 Inkscape/TikZ 画线条图；matplotlib 出线条图时关闭颜色、用 `linestyle`+标记区分而非配色。导出矢量 PDF/EPS，文字可编辑，便于代理人修改标记。

【链接 / 已知坑】规范以 CNIPA《专利审查指南》现行版与受理局具体要求为准（本节为通用要点，未逐条核对最新版次，落地前核对当年指南）；不同国家/地区（USPTO/EPO）附图规则有差异（如 USPTO 对线宽、edge shading 另有规定），涉外申请按目标局要求另核；**最终附图须由专利代理师审核**，标记与权利要求/说明书的对应关系是审查重点，错标/漏标会发补正。
