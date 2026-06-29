# db07 扩展卡 — 高级科研图表模式

> schema: `figure_type, paper_source, research_field, purpose, data_required, layout, color_scheme, annotation_style, caption_style, possible_code_tool, replication_notes, where_to_place_in_paper`
> 核验日期：2026-06-10。PRISMA/CONSORT 官网脚本 HTTP 200；PRISMA 2020、CONSORT 2010、UMAP、qqman、limma、Bland-Altman 等代表论文由 OpenAlex 查询核验。下列卡片重点写“图支撑哪个 claim”，不是只学样式。

```yaml
- figure_type: PRISMA 2020 文献筛选流程图
  paper_source: "PRISMA 2020 statement | 2021 | doi:10.1136/bmj.n71 | 官网 https://www.prisma-statement.org/"
  research_field: 系统综述 / 文献调研
  purpose: 支撑“检索与筛选过程透明、可复现、无任意删文献”的 claim
  data_required: 数据库检索数、去重数、标题摘要排除数、全文排除理由、最终纳入数
  layout: 从 Identification → Screening → Included 的纵向流程框，左右列标数据库/其他来源
  color_scheme: 黑白/浅灰为主，少量蓝色强调最终纳入；打印友好
  annotation_style: 每个框写 n=；全文排除需列理由和数量；箭头清晰
  caption_style: 说明检索日期、数据库、去重规则、排除依据
  possible_code_tool: Mermaid / Graphviz / python 脚本生成 SVG / 官方 PRISMA 模板重绘
  replication_notes: 数字必须能勾稽；用 light-literature-search/scripts/prisma_flow.py 检查算术
  where_to_place_in_paper: 方法-文献检索流程；系统综述正文或附录

- figure_type: CONSORT 随机对照试验流程图
  paper_source: "CONSORT 2010 Statement | 2010 | doi:10.1186/1741-7015-8-18 | 官网 https://www.consort-statement.org/"
  research_field: 临床试验 / 干预研究
  purpose: 支撑“试验纳入、随机分组、随访与分析人群透明”的 claim
  data_required: assessed/enrolled/randomized/allocation/follow-up/analysis 各阶段人数与排除理由
  layout: 顶部 assessed，分流到 allocation 两组，再到 follow-up 与 analysis
  color_scheme: 黑白为主，组别用轻微色块区分，确保灰度可辨
  annotation_style: 每个框写人数与排除理由；两组对称排版
  caption_style: 说明分析原则(ITT/per-protocol)与随访截止
  possible_code_tool: diagrams.net / Graphviz / CONSORT 官方模板重绘
  replication_notes: 不得隐瞒失访/排除；人数前后必须能加总
  where_to_place_in_paper: 方法-研究对象/流程

- figure_type: Kaplan-Meier 生存曲线(含风险表)
  paper_source: "Kaplan-Meier 生存分析经典方法；Cox/KM 代表作已在 db03 biomedical 方法卡核验"
  research_field: 生物医学 / 生存分析
  purpose: 支撑“不同组别事件发生时间分布存在差异”的 claim
  data_required: 随访时间、事件/删失指示、组别；可选协变量分层
  layout: 主图为阶梯生存曲线，底部 aligned risk table，右上角 log-rank p 值与 HR
  color_scheme: 色盲友好组别色；删失点用短竖线；黑白用线型区分
  annotation_style: 标注中位生存时间、置信区间、删失点、风险表人数
  caption_style: 说明起点/终点、删失定义、log-rank/Cox 设置
  possible_code_tool: R survival/survminer 或 Python lifelines + matplotlib
  replication_notes: 必须显示 risk table；PH 假设不满足时不要只报 Cox HR
  where_to_place_in_paper: 结果-主要终点/预后分析

- figure_type: Forest plot 森林图(效应量与置信区间)
  paper_source: 系统综述/meta-analysis 标准图；可与 PRISMA/ROB 工具配套
  research_field: 医学统计 / meta-analysis / 亚组分析
  purpose: 支撑“多个研究/亚组的效应方向与不确定性”的 claim
  data_required: 每项研究或亚组的效应量、95%CI、权重、总体合并效应
  layout: 左表列研究名/样本量，右侧横向 CI 线，底部菱形总体效应
  color_scheme: 黑白为主，整体效应用强调色；打印友好
  annotation_style: 垂直无效线，CI 横线，权重方块大小，异质性 I² 标注
  caption_style: 说明模型(fixed/random)、效应量类型、异质性统计
  possible_code_tool: R meta/metafor/forestplot 或 Python matplotlib 自绘
  replication_notes: 效应方向必须统一；权重和 CI 需可复算；亚组不应过度解读
  where_to_place_in_paper: 结果-meta-analysis / 亚组分析

- figure_type: Bland-Altman 一致性图
  paper_source: "Bland-Altman agreement analysis; OpenAlex 核验相关方法文献 doi:10.11613/bm.2015.015"
  research_field: 医学测量 / 方法学比较 / 传感器校准
  purpose: 支撑“两个测量方法是否可互换/一致”的 claim，而不是只看相关性
  data_required: 同一样本的两种方法测量值，差值与均值
  layout: x=两方法均值，y=差值；中心 bias 线，±1.96SD limits of agreement
  color_scheme: 单色散点 + 红/蓝水平参考线；灰度可辨
  annotation_style: 标注 mean bias、LoA 数值、异常点；可加回归线检查比例偏差
  caption_style: 说明单位、样本量、是否有重复测量、LoA 解释
  possible_code_tool: matplotlib / statsmodels / R blandr
  replication_notes: 遵 R4(相关≠一致性,方法学比较用 Bland-Altman 不能只给 R²/散点); 领域特异——重复测量需用扩展方法
  where_to_place_in_paper: 方法比较/设备验证结果

- figure_type: 校准曲线 / reliability diagram
  paper_source: "临床预测校准教程 OpenAlex 核验 doi:10.1093/jamia/ocz228"
  research_field: 机器学习 / 临床预测 / 风险模型
  purpose: 支撑“模型概率输出可信/或需校准”的 claim
  data_required: 预测概率、真实标签、分箱或平滑校准估计；可选 Brier/ECE
  layout: x=预测概率，y=观察频率；45°理想线；底部可加预测概率直方图
  color_scheme: 本模型强调色，理想线灰色虚线，baseline 中性
  annotation_style: 标注 Brier/ECE、校准斜率/截距；样本少的 bin 用透明度提示
  caption_style: 说明分箱数/平滑方法/测试集/是否外部验证
  possible_code_tool: sklearn.calibration + matplotlib / R rms
  replication_notes: 分类 AUC 高不代表校准好；小样本分箱会不稳定
  where_to_place_in_paper: 结果-模型可靠性/临床可用性

- figure_type: Volcano plot 火山图
  paper_source: "limma RNA-seq/microarray differential expression | 2015 | doi:10.1093/nar/gkv007；volcano plot 方法文献 doi:10.1142/s0219720012310038"
  research_field: 组学 / 差异表达
  purpose: 支撑“显著且效应量大的基因/特征被识别”的 claim
  data_required: 每个基因/特征的 log2 fold change、p 值或 FDR、显著阈值
  layout: x=log2FC，y=-log10(FDR/p)，左右两侧高亮上/下调
  color_scheme: 非显著灰色，上调红/橙，下调蓝；色盲场景加形状/标签
  annotation_style: 阈值线、top genes 标签、FDR 与 fold-change 门槛
  caption_style: 说明统计检验、校正方法、阈值、样本组别
  possible_code_tool: R ggplot2/EnhancedVolcano 或 Python matplotlib/seaborn
  replication_notes: 必须用多重校正 FDR；不要只挑好看的基因标签
  where_to_place_in_paper: 结果-组学差异分析

- figure_type: Manhattan + QQ plot (GWAS)
  paper_source: "qqman: GWAS Q-Q and Manhattan plots | 2018 | doi:10.21105/joss.00731"
  research_field: 遗传学 / GWAS
  purpose: 支撑“显著位点分布与全基因组假阳性控制”的 claim
  data_required: SNP/variant 的染色体、位置、p 值；可选 LD/clumping 结果
  layout: Manhattan 主图按染色体交替上色；QQ plot 检查 p 值膨胀
  color_scheme: 染色体交替深浅色；显著阈值红线；suggestive 阈值虚线
  annotation_style: 标注 lead SNP/基因名，写 genome-wide significance 线
  caption_style: 说明样本量、协变量、主成分校正、λGC/LD score 结果
  possible_code_tool: R qqman / Python matplotlib
  replication_notes: 群体分层必须校正；QQ plot 不能省；阈值 5e-8 需说明
  where_to_place_in_paper: 结果-GWAS 主发现

- figure_type: UMAP/t-SNE 嵌入可视化
  paper_source: "UMAP: Uniform Manifold Approximation and Projection | 2018 | doi:10.21105/joss.00861"
  research_field: 单细胞 / NLP embedding / 表征学习
  purpose: 支撑“表示空间有聚类/分离/连续轨迹”的探索性 claim
  data_required: 高维特征/embedding、标签或连续变量、样本批次信息
  layout: 2D scatter，颜色=类别/连续值；可分面显示批次/方法前后
  color_scheme: 类别用 ColorBrewer/Okabe-Ito，连续用 viridis；点透明防遮挡
  annotation_style: 标注簇名/轨迹箭头/批次效应；图例清晰
  caption_style: 说明预处理、距离度量、参数(n_neighbors/perplexity)、随机种子
  possible_code_tool: umap-learn / scikit-learn TSNE / scanpy / matplotlib
  replication_notes: UMAP/t-SNE 不能当定量证明；参数敏感，需报告设置并配定量指标
  where_to_place_in_paper: 结果-表征可视化/探索分析
```
