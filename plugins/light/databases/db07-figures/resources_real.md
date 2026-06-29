# db07 补充 — 科研图表真实资源库（resources_real.md）

> 服务 m09(图表规划) 与 m11(绘图)。两部分：**(1) 真实资源清单**（带可核查链接 + 用途），**(2) figure_card 扩充卡片**（重点写"支撑哪个 claim + 用什么工具 + 放论文哪里"）。
> 配色铁律（全 db07 统一，见 README 与 a07）：**色盲友好**（viridis / ColorBrewer 安全色板 / Set2）、**全文统一调色板**、**黑白可辨**（线型+标记双重编码）、**矢量优先**（PDF/SVG，位图 ≥300 dpi）。
> 核实方式：工具论文的标题/年份/DOI 来自 **OpenAlex API 真实 curl 结果**（2026-06-06）；官网/Gallery URL 经 **WebSearch 核实可达**。查不到的标 `待核查`。
> **被引数是薄缓存快照**(last_checked=2026-06-06、会增长、仅作可信度背书非权威值)：DOI 已在表内,需最新值按 DOI 查 OpenAlex `works/doi:{DOI}` 即得,本表不保证长期准确。

---

## 第一部分 · 真实资源清单（核实链接 + 用途）

### A. 通用绘图库与 Gallery（出版级统计图首选）

| 资源 | 真实链接 | 用途 / 适用场景 | 核实信息 |
|---|---|---|---|
| **Matplotlib Gallery** | https://matplotlib.org/stable/gallery/index.html | Python 出版级静态图基石；折线/柱状/箱线/误差棒/混淆矩阵/子图组合，导出 PDF/SVG 矢量 | 引擎论文 Hunter, *Matplotlib: A 2D Graphics Environment* (2007), DOI 10.1109/mcse.2007.55，被引 **39283**（OpenAlex） |
| **Seaborn Example Gallery** | https://seaborn.pydata.org/examples/index.html | 统计图高层封装；分组柱+误差、分布/小提琴、相关热力、回归带置信区间；内置色盲友好 palette | Waskom, *seaborn: statistical data visualization* (JOSS 2021), DOI 10.21105/joss.03021，被引 **78** |
| **Plotly (Python)** | https://plotly.com/python/ ；库总览 https://plotly.com/graphing-libraries/ ；源码 https://github.com/plotly/plotly.py | 交互式图（HTML/网页/附录补充材料）；3D、悬浮提示、可缩放；适合在线 SI 与汇报，论文正文仍导静态 | 官网 + GitHub 经 WebSearch 核实 |
| **Python Graph Gallery** | https://www.python-graph-gallery.com/ | 按图型检索 + 完整可复制代码（matplotlib/seaborn/plotly）；快速找"某种图怎么画" | 经 WebSearch 核实可达 |
| **ggplot2 (R) 官网** | https://ggplot2.tidyverse.org/ | 图形语法（Grammar of Graphics）；分面 facet、主题统一、出版排版精致 | Wickham, *ggplot2: Elegant Graphics for Data Analysis* (2009), DOI 10.1007/978-0-387-98141-3，被引 **20555** |
| **R Graph Gallery** | https://r-graph-gallery.com/ | R/ggplot2 按图型检索 + 代码；含 ridgeline、相关网络等 | 经 WebSearch 核实可达 |
| **Altair Example Gallery** | https://altair-viz.github.io/gallery/index.html | 声明式（Vega-Lite）交互统计图，适合探索性分析与网页 SI | VanderPlas, *Altair: Interactive Statistical Visualizations for Python* (JOSS 2018), DOI 10.21105/joss.01057，被引 **238** |
| **Datawrapper** | https://www.datawrapper.de/ | 无代码做出版/媒体级图表与地图；新闻图风格，适合科普稿、报告、答辩图 | 经 WebSearch 核实可达 |
| **Observable** | https://observablehq.com/ | 基于 D3/Observable Plot 的在线交互可视化笔记本；定制化交互 SI | 经 WebSearch 核实可达 |

### B. 科研专用样式 / 配色 / 色板

| 资源 | 真实链接 | 用途 / 适用场景 | 核实信息 |
|---|---|---|---|
| **SciencePlots** | https://github.com/garrettj403/SciencePlots | matplotlib 样式包，一行 `plt.style.use(['science'])` 套用 IEEE/Nature 风格（衬线字、紧凑边距、矢量友好） | 软件存档 *SciencePlots* (Zenodo, v1.0.8 2021), DOI 10.5281/zenodo.4893230（v1.0.6 2020: 10.5281/zenodo.4106650） |
| **ColorBrewer 2.0** | https://colorbrewer2.org/ | 经科学验证的离散/顺序/发散色板；明确标注 **colorblind-safe / print-safe**，分类与连续值首选 | Harrower & Brewer, *ColorBrewer.org: An Online Tool for Selecting Colour Schemes for Maps* (2003), DOI 10.1179/000870403235002042，被引 **1114** |
| **viridis 色图** | matplotlib 内置（`cmap='viridis'`）；R 包 https://CRAN.R-project.org/package=viridis | 感知均匀 + 色盲友好的顺序色图；热力图/连续标量默认首选，黑白打印仍单调可辨 | matplotlib 内置随引擎分发；R 包经 WebSearch 核实于 CRAN |

### C. 框架图 / 流程图 / 示意图（diagram & schematic）

| 资源 | 真实链接 | 用途 / 适用场景 | 核实信息 |
|---|---|---|---|
| **Graphviz** | https://graphviz.org/ | DOT 脚本自动布局有向/无向图；技术路线、依赖图、状态机；可重现、可版本控制 | Gansner & North, *An open graph visualization system and its applications to software engineering* (2000), DOI 10.1002/1097-024x...，被引 **1105** |
| **Mermaid** | https://mermaid.js.org/ ；在线 https://mermaid.live/ | 文本即图（Markdown 友好）；流程图/时序图/甘特/类图；适合方法流程、实验 pipeline 快速出图 | 官网经 WebSearch 核实可达 |
| **draw.io / diagrams.net** | https://www.drawio.com/ ；在线 https://app.diagrams.net/ | 拖拽式框架图/系统图/流程图，导出 SVG/PDF；模型框架图主力（无需写代码） | 经 WebSearch 核实可达 |
| **Inkscape** | https://inkscape.org/ | 开源矢量编辑器；精修框架图、拼合子图、对齐字号、导出 PDF/SVG，期刊矢量要求达标 | 经 WebSearch 核实可达 |
| **TikZ / PGFPlots** | PGFPlots 文档 https://ctan.org/pkg/pgfplots ；TikZ 示例 https://texample.net/tikz/examples/ | LaTeX 原生矢量绘图；框架图与函数图与正文字体/公式完全一致，投稿质感最高（学习曲线陡） | CTAN/texample 经 WebSearch 核实可达 |

### D. 领域插画 / 商业绘图 / 数据分析软件

| 资源 | 真实链接 | 用途 / 适用场景 | 核实信息 |
|---|---|---|---|
| **BioRender** | https://www.biorender.com/ | 生物/医学专业插画素材库（细胞、分子、实验流程）；Graphical Abstract、机理示意图主力（部分功能付费） | 官网经 WebSearch 核实可达 |
| **Origin (OriginLab)** | https://www.originlab.com/ | 实验/理工科商业绘图与分析；多 Y 轴、峰拟合、误差棒、出版模板；物理化学材料领域常见（商业付费） | 官网经 WebSearch 核实可达 |

### 选型速查（按产出场景）

- **论文正文统计图**（主结果/消融/敏感性/ROC/PR）→ matplotlib + SciencePlots，配 ColorBrewer/viridis，导 PDF。
- **混淆矩阵/相关热力** → seaborn `heatmap` + viridis（顺序）或发散色板（带符号值）。
- **模型框架图** → draw.io 起稿 → Inkscape 精修 → 矢量导出；追求极致一致用 TikZ。
- **流程 / 技术路线 / pipeline** → Mermaid（快、可版本控制）或 Graphviz（自动布局）。
- **生物医学机理 / Graphical Abstract** → BioRender。
- **交互 / 网页 SI** → Plotly / Altair / Observable。
- **无代码报告与答辩图** → Datawrapper。

> 色盲友好与全文统一：任选一个安全色板（如 ColorBrewer `Set2`/`Dark2` 分类、`viridis` 连续），由 a07 跨全图维护同一套 hex；本方法固定用同一"强调色"，baseline 用中性灰系；务必同时用线型+标记做黑白冗余编码。

---

## 第二部分 · figure_card 扩充卡片（db07 schema）

> schema：`figure_type, paper_source, research_field, purpose, data_required, layout, color_scheme, annotation_style, caption_style, possible_code_tool, replication_notes, where_to_place_in_paper`
> 本文件是 db07 通用图表卡的 canonical 实体位置，覆盖主结果、消融、框架图、可解释性与常见性能/错误分析图；`figure_cards.md` 仅保留模板与索引。

```yaml
- figure_type: 参数敏感性折线图(多曲线)
  paper_source: 仅元数据/链接
  research_field: 通用
  purpose: 支撑"方法对关键超参鲁棒/存在稳定最优区间"的 claim
  data_required: 单一超参扫描下指标均值(多种子)+误差带
  layout: x=超参取值(可对数轴), y=指标; 多数据集多条曲线
  color_scheme: 统一调色板, 每数据集一色; 色盲友好 + 线型区分
  annotation_style: 阴影误差带, 标出选定取值的竖虚线
  caption_style: 说明扫描范围/固定其余超参/重复次数
  possible_code_tool: matplotlib/seaborn
  replication_notes: 遵 R1(y 轴不截断造假); 图型特异——仅扫一个超参其余固定
  where_to_place_in_paper: 实验-分析(敏感性)

- figure_type: ROC 曲线(含 AUC)
  paper_source: 仅元数据/链接
  research_field: 分类/检测/医学诊断
  purpose: 支撑"判别能力优于 baseline"的 claim, 阈值无关
  data_required: 各方法的 fpr/tpr 序列 + AUC
  layout: x=FPR, y=TPR; 对角随机线参考; 图例标 AUC
  color_scheme: 本方法强调色, baseline 中性; 色盲友好+线型
  annotation_style: 图例内标 AUC 数值; 多折时画均值+std 带
  caption_style: 说明数据集/正负样本比/交叉验证设置
  possible_code_tool: scikit-learn + matplotlib
  replication_notes: 类别不均衡时务必同时给 PR 曲线
  where_to_place_in_paper: 实验-分类性能

- figure_type: PR 曲线(Precision-Recall)
  paper_source: 仅元数据/链接
  research_field: 不均衡分类/信息检索/检测
  purpose: 支撑"正类少时仍优"的 claim(比 ROC 更敏感)
  data_required: 各方法 precision/recall 序列 + AP/AUPRC
  layout: x=Recall, y=Precision; 标注随机基线=正例比例
  color_scheme: 与 ROC 同一套配色, 保持全文一致
  annotation_style: 图例标 AP; 标出工作点
  caption_style: 注明正例占比与基线含义
  possible_code_tool: scikit-learn + matplotlib
  replication_notes: 与 ROC 成对出现更有说服力
  where_to_place_in_paper: 实验-分类性能(与 ROC 并排)

- figure_type: 混淆矩阵热力图
  paper_source: 仅元数据/链接
  research_field: 多分类
  purpose: 支撑"错误集中在某些易混类"的细粒度分析 claim
  data_required: NxN 计数或行归一化比例
  layout: 方阵热力, 行=真实, 列=预测; 对角即正确
  color_scheme: 顺序色图(viridis/Blues)+色标; 单调
  annotation_style: 格内标数值/百分比; 高亮主对角
  caption_style: 说明归一化方式与类别顺序
  possible_code_tool: seaborn heatmap / sklearn ConfusionMatrixDisplay
  replication_notes: 类多时行归一化更可读; 字号防重叠
  where_to_place_in_paper: 实验-错误分析

- figure_type: 技术路线 / pipeline 流程图
  paper_source: 仅元数据/链接
  research_field: 通用
  purpose: 支撑"整体方法各阶段如何衔接"的概览, 帮审稿人建立全局认知
  data_required: 无(示意)
  layout: 左→右或上→下分阶段块, 箭头标数据/控制流
  color_scheme: 阶段分色但克制, 与论文主色一致
  annotation_style: 阶段名 + 输入输出标注; 关键模块加粗
  caption_style: 一句话概述流程, 指引后文对应章节
  possible_code_tool: Mermaid / Graphviz / draw.io
  replication_notes: 文本式(Mermaid)便于改版; 矢量导出
  where_to_place_in_paper: 引言或方法章节开头

- figure_type: 定性效果拼图(qualitative grid)
  paper_source: 仅元数据/链接
  research_field: CV/生成/分割/检测
  purpose: 支撑"输出在视觉/语义上更优"的定性 claim
  data_required: 同样本下 输入/GT/baseline/本方法 的成对结果
  layout: 网格 GridSpec, 行=样本, 列=方法; 列标题对齐
  color_scheme: 图像保真, 叠加掩膜用半透明统一色
  annotation_style: 局部放大框/箭头指出差异; 失败案例诚实保留
  caption_style: 说明样本来源, 标注列含义
  possible_code_tool: matplotlib GridSpec / PIL 拼图 / PPT 精排
  replication_notes: 不挑樱桃; 同一裁剪尺度; 高分辨率避免压缩失真
  where_to_place_in_paper: 实验-定性结果

- figure_type: 跨数据集主结果对比(分组柱+误差棒)
  paper_source: 仅元数据/链接
  research_field: 通用
  purpose: 支撑"本方法在多数据集普遍领先"的核心 claim
  data_required: 各方法×各数据集 多种子均值+标准差
  layout: 分组柱, x=数据集, 同组内并列各方法, y=指标
  color_scheme: 本方法固定强调色, baseline 中性灰阶; 色盲友好
  annotation_style: 误差棒 + 显著性星标 + 数值标签
  caption_style: 自洽; 指标定义/重复次数/是否统计检验
  possible_code_tool: matplotlib/seaborn (+ SciencePlots 样式)
  replication_notes: 遵 R1(y 轴从合理基线起不误导)/R7(多种子算 std 并注明误差棒类型+n)
  where_to_place_in_paper: 实验-主结果(开篇大图)
```

### 补充卡片（覆盖消融 / 框架 / 可解释性，字段写满）

```yaml
- figure_type: 消融实验图(分组柱/累加折线)
  paper_source: 仅元数据/链接
  research_field: 通用
  purpose: 支撑"每个创新组件都有独立贡献"的 claim
  data_required: 逐组件移除/叠加后的指标(多种子)
  layout: 分组柱(各变体) 或 自底向上累加折线
  color_scheme: 统一调色板, full model 用强调色高亮
  annotation_style: 变体标签清晰; 标注相对增量(Δ)
  caption_style: 列明各变体含义与移除内容
  possible_code_tool: matplotlib/seaborn
  replication_notes: 控制变量, 一次只改一处; 与主结果同指标
  where_to_place_in_paper: 实验-消融

- figure_type: 模型框架图(architecture)
  paper_source: 仅元数据/链接
  research_field: 通用
  purpose: 一图讲清方法整体结构与数据流, 支撑方法可理解性
  data_required: 无(示意)
  layout: 左输入→中间模块→右输出, 箭头标数据流与维度
  color_scheme: 模块分色但克制, 与论文主色一致
  annotation_style: 模块名 + 关键张量维度; 创新模块加粗/描边
  caption_style: 概述结构, 指引后文小节
  possible_code_tool: draw.io / Inkscape / TikZ
  replication_notes: 矢量导出; 单栏缩放后字号仍可读
  where_to_place_in_paper: 方法章节开头

- figure_type: 可解释性热力图(注意力/SHAP/Grad-CAM)
  paper_source: 仅元数据/链接
  research_field: 通用(CV/NLP/表格)
  purpose: 提供机理证据, 支撑"为什么有效/关注了正确区域"的 claim
  data_required: 注意力权重 / SHAP 值 / 梯度显著图
  layout: 原始输入 + 半透明叠加热力; 多样本成行
  color_scheme: 顺序色图(viridis)或发散图(带符号贡献)+ 色标
  annotation_style: 色标含义清晰; 标出关键高响应区
  caption_style: 说明解释方法与归一化方式
  possible_code_tool: SHAP / Captum / matplotlib
  replication_notes: 解释方法需注明版本与设置; 不挑樱桃样本
  where_to_place_in_paper: 结果分析/讨论
```


## 待补充

按用户具体领域(CV/NLP/时序/生医/材料)补充专用图卡与统一调色板 hex；与 db05/db06 的主色联动由 a07 维护，确保论文-PPT-前端三处配色一致。



