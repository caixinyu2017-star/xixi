# light-result-analysis 参考工具笔记

说明：以下逐工具笔记基于官方文档/仓库检索（WebSearch）与已验证知识整理。本环境 WebFetch 被网络策略拦截，无法逐页抓取全文，故 API 细节以官方文档检索片段 + 稳定版公认接口为准；凡版本敏感处已标注。请以各库当前版本文档为准再落地。

## EDA workflows（探索性数据分析流程）
- 【是什么】Tukey 提出的探索性分析范式：先看数据形状再建模。落到实验结果分析就是"分布→关系→异常→分组对比"的固定动作序列。
- 【可复用方法】标准顺序：① 形状与缺失（df.shape / df.info() / df.isna().mean()）；② 单变量分布（直方图 + 箱线图，看偏度/长尾/多峰）；③ 双变量关系（散点 + 相关矩阵 df.corr(numeric_only=True)，注意 Pearson 只测线性，非线性用 Spearman）；④ 分组对比（groupby + 聚合 + 误差棒）；⑤ 异常值（IQR 法 Q1-1.5IQR / Q3+1.5IQR，或 z-score>3）；⑥ 数据泄漏体检（特征与标签相关过高、时间穿越）。对结果数据：先 EDA 再下结论，避免被均值掩盖的双峰/长尾误导。
- 【链接】https://en.wikipedia.org/wiki/Exploratory_data_analysis
- 【坑】均值/相关系数对长尾和离群极敏感；务必配合分布图，不要只报点估计。

## Statistical Analysis workflows（统计分析流程）
- 【是什么】把"看起来更好"升级为"统计上显著更好"的判定流程。
- 【可复用方法】① 明确假设（H0/H1）与配对性；② 选检验：两组独立连续→Welch t 检验（不假设等方差）、配对→paired t、非正态→Mann-Whitney U / Wilcoxon、多组→ANOVA + Tukey HSD、比例→two-proportion z-test、分类列联→卡方；③ 多重比较校正（Bonferroni 或 Benjamini-Hochberg FDR，statsmodels.stats.multitest.multipletests）；④ 同时报效应量（Cohen's d / Cliff's delta）与置信区间，别只报 p 值；⑤ 多随机种子（≥5）跑均值±标准差，区分"方法增益"与"种子噪声"。
- 【链接】https://www.statsmodels.org/stable/stats.html
- 【坑】p<0.05 不等于效应大；样本极大时微小差异也显著。务必 p 值 + 效应量 + 区间三件套。

## Matplotlib
- 【是什么】Python 绘图底座，所有出版级图表的最终可控层。
- 【可复用方法/真实 API】坚持面向对象接口 `fig, ax = plt.subplots(...)` 而非 pyplot 状态机；多子图布局用 `plt.subplots(2,2, layout="constrained")`（constrained_layout 自动防重叠，优于 tight_layout，见 3.8+ 文档）；出版导出 `fig.savefig("f.pdf", dpi=300, bbox_inches="tight")`，矢量优先 PDF/SVG；全局样式 `plt.rcParams.update({"font.size":11,"figure.dpi":150})` 或 `plt.style.use(...)`。
- 【链接】https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html
- 【坑】中文需设字体（rcParams["font.sans-serif"]）并 `axes.unicode_minus=False`；论文图用矢量格式避免位图模糊。

## Seaborn
- 【是什么】基于 matplotlib 的统计可视化高层封装，自动聚合 + 置信区间。
- 【可复用方法】区分两类函数：图形级（figure-level）`relplot/displot/catplot/lmplot` 自带分面（col=/row=/hue=）并返回 FacetGrid；轴级（axes-level）`scatterplot/histplot/boxplot/barplot/heatmap` 接受 ax= 可嵌入子图。`barplot/lineplot` 默认画 95% 置信区间误差棒（errorbar=("ci",95) 或 "se"/"sd"）。相关矩阵热图：`sns.heatmap(df.corr(), annot=True, cmap="vlag", center=0)`。
- 【链接】https://seaborn.pydata.org/tutorial/function_overview.html
- 【坑】figure-level 函数返回 FacetGrid 不能直接塞进已有 ax，想组合子图须用 axes-level 函数。

## Scientific Visualization skill（科研可视化技能）
- 【是什么】Claude Code 生态中的"科研出版级绘图"技能模板，封装配色/字体/布局规范，目标产出可直接进论文的图。
- 【可复用方法/评审维度】① 配色对色盲友好：用 viridis/cividis 等感知均匀且色盲安全 colormap，避免 jet/rainbow；分类色用 colorblind 调色板。② 字体≥论文正文字号、线宽够粗、矢量导出。③ 一图一信息，去除 chartjunk（多余网格/边框）。④ 误差棒/置信区间必标，注明 n 与统计含义。⑤ 坐标轴含单位、避免误导性截断 y 轴。
- 【链接】https://www.aitmpl.com/component/skills/scientific/scientific-visualization ；色盲友好理念参考 https://pmc.ncbi.nlm.nih.gov/articles/PMC8567791/
- 【坑】不同来源同名技能实现各异；把它当"检查清单"用，落地仍靠 matplotlib/seaborn。

## SHAP
- 【是什么】基于 Shapley 值的模型可解释性库，把单条/全局预测拆成每个特征的贡献。
- 【可复用方法/真实 API】统一入口 `explainer = shap.Explainer(model, X_background)`；专用更快：树模型 `shap.TreeExplainer`、线性 `shap.LinearExplainer`、神经网络 `shap.DeepExplainer/GradientExplainer`、模型无关兜底 `shap.KernelExplainer`（慢，需背景集采样）。算 `sv = explainer(X)`。绘图：`shap.summary_plot`/`shap.plots.beeswarm`（全局特征重要性+方向）、`shap.plots.bar`（平均绝对贡献排序）、`shap.plots.waterfall`（单样本分解）、`shap.plots.force`（力图）、`shap.plots.scatter`（依赖图，看交互）。
- 【链接】https://shap.readthedocs.io/en/stable/api.html
- 【坑】KernelExplainer 计算昂贵，背景集要采样（shap.sample / kmeans）；SHAP 反映模型而非真实因果，别当因果证据；特征强相关时贡献分配会被稀释。

## Statsmodels
- 【是什么】统计建模与假设检验库，提供带 p 值/置信区间/诊断的"统计学家级"输出，补 sklearn 不给推断的短板。
- 【可复用方法/真实 API】回归 `sm.OLS(y,X).fit()` 或公式接口 `smf.ols("y~x1+x2", data).fit()`，`.summary()` 给系数/标准误/p/R²/AIC；分类 `smf.logit(...)`；混合效应 `smf.mixedlm`；广义线性 `sm.GLM(family=...)`。方差分析 `statsmodels.stats.anova.anova_lm(model, typ=2)`。检验工具箱（statsmodels.stats）：`weightstats.ttest_ind`、`proportion.proportions_ztest`、`multitest.multipletests(pvals, method="fdr_bh")`（多重比较校正）、`diagnostic.het_breuschpagan`（异方差）、`stattools.durbin_watson`（残差自相关）、`diagnostic.acorr_ljungbox`。
- 【链接】https://www.statsmodels.org/stable/api.html ；ANOVA：https://www.statsmodels.org/stable/generated/statsmodels.stats.anova.anova_lm.html
- 【坑】OLS 默认不含截距，需 `sm.add_constant(X)`；公式接口（smf）才会自动加截距与处理分类变量。

## NetworkX
- 【是什么】纯 Python 图/网络分析库，做关系结构、引用网络、特征相关图、消融依赖图等。
- 【可复用方法/真实 API】建图 `G=nx.Graph()/DiGraph()`，`add_edges_from([...])`。中心性：`nx.degree_centrality`、`nx.betweenness_centrality`（桥接节点）、`nx.closeness_centrality`、`nx.eigenvector_centrality`、`nx.pagerank`（有向影响力）。社区发现：`nx.community.louvain_communities`、`greedy_modularity_communities`、`girvan_newman`。结构：`nx.connected_components`、`nx.shortest_path`、`nx.density`、`nx.clustering`。绘图 `nx.draw_networkx`（布局 spring_layout/kamada_kawai）。
- 【链接】https://networkx.org/documentation/stable/reference/algorithms/community.html
- 【坑】betweenness 在大图上是 O(VE)，超过几千节点要用 k 采样近似（k= 参数）；可视化大图意义有限，优先用中心性指标量化。

## Plotly
- 【是什么】交互式可视化库，输出可缩放/悬停/筛选的 HTML 图，适合附录、补充材料、内部 review。
- 【可复用方法/真实 API】快速接口 plotly.express：`px.scatter/line/bar/histogram/box/imshow`，参数 color=/size=/facet_col=/hover_data= 一行成图。精细控制用 graph_objects：`go.Figure(data=[go.Scatter(...)])`。导出交互 HTML `fig.write_html("f.html")`；导出静态图 `fig.write_image("f.png")`（需装 kaleido）；`fig.update_layout(...)` 调标题/坐标轴/图例。
- 【链接】https://plotly.com/python/ ；导出 HTML 参考 https://stackoverflow.com/questions/67290534/save-interactive-plotly-plot-in-html-or-another-way
- 【坑】论文正文要静态矢量图（用 matplotlib），Plotly 更适合交互探索与网页；write_image 需额外装 kaleido 引擎。

## Altair
- 【是什么】基于 Vega-Lite 的声明式可视化库，"图形语法"风格：声明数据+编码+标记，少写循环。
- 【可复用方法/真实 API】`alt.Chart(df).mark_point().encode(x="a:Q", y="b:Q", color="cat:N")`。类型后缀关键：Q 定量、N 名义、O 有序、T 时间。组合：`chart1 | chart2`（横排）、`chart1 & chart2`（竖排）、`+`（叠加图层）。交互 `.interactive()`、选择器 `alt.selection_point()` 做联动筛选。导出 `chart.save("f.html"/"f.png"/"f.svg")`。
- 【链接】https://altair-viz.github.io/user_guide/encodings/
- 【坑】默认对行数有上限（早期 5000 行需 alt.data_transformers.enable("default", max_rows=...)）；编码类型后缀写错会静默出错图。

## Deepchecks
- 【是什么】ML 数据与模型的"测试套件"库，一键跑数据完整性、训练/测试分布漂移、模型评估等成套检查。
- 【可复用方法/真实 API（版本敏感）】tabular 用法：`from deepchecks.tabular import Dataset`，`ds = Dataset(df, label="y", cat_features=[...])`；套件 `from deepchecks.tabular.suites import data_integrity, train_test_validation, model_evaluation`，运行 `data_integrity().run(ds)` 或 `train_test_validation().run(train_ds, test_ds)`、`model_evaluation().run(train_ds, test_ds, model)`，结果对象可 `.show()`（notebook）或 `.save_as_html()`。检查含：重复/缺失/单值列、特征-标签泄漏、train-test 漂移、类别不平衡等。另有 deepchecks.nlp / deepchecks.vision。
- 【链接】https://docs.deepchecks.com/stable/ ；仓库 https://github.com/deepchecks/deepchecks
- 【坑】具体套件名与 API 随版本变动（本环境未能抓取官方页全文核实当前签名），落地前请对照所装版本文档；大数据集跑全套较慢，可选子集检查。

## Evidently AI
- 【是什么】数据漂移与模型性能监控库，生成漂移/质量/性能可视化报告，也支持测试断言与线上监控。
- 【可复用方法/真实 API（版本敏感，API 经历大改）】经典版（约 0.4.x）：`from evidently.report import Report`、`from evidently.metric_preset import DataDriftPreset, DataQualityPreset, ClassificationPreset, RegressionPreset`；`r = Report(metrics=[DataDriftPreset()]); r.run(reference_data=ref, current_data=cur); r.save_html("r.html")`。测试断言用 `TestSuite` + `evidently.test_preset`。新版（0.6+）API 重构为 `Report`/`Dataset` 新接口与 DataSummaryPreset 等，导入路径变化较大。
- 【链接】https://docs.evidentlyai.com/ ；迁移说明 https://docs.evidentlyai.com/faq/migration
- 【坑】新旧版本导入路径与预设名不兼容，务必先 `import evidently; evidently.__version__` 确认版本再选 API；漂移检测对数值/类别列用不同统计检验，默认阈值未必合适需调。

## ydata-profiling（原 pandas-profiling）
- 【是什么】一行代码生成完整 EDA 报告（分布、缺失、相关、交互、警告）的画像库。
- 【可复用方法/真实 API】`from ydata_profiling import ProfileReport`；`ProfileReport(df, title="...").to_file("report.html")`，notebook 内 `.to_notebook_iframe()`。大数据集用 `minimal=True`（关掉昂贵的相关/交互计算）；时序数据 `tsmode=True` + sortby=；可传 config 调 `correlations`/`missing_diagrams`/`samples`。报告自带 Alerts（高相关、高缺失、零方差、高基数）直接当数据体检清单。
- 【链接】https://docs.profiling.ydata.ai/ ；仓库 https://github.com/ydataai/ydata-profiling ；大数据 https://docs.profiling.ydata.ai/latest/features/big_data/
- 【坑】列多/行多时默认全相关矩阵极慢且占内存，务必 minimal=True 或限制列；报告是体检不是结论，仍需人判读。

## Jupyter Notebook
- 【是什么】交互式代码+输出+叙述一体的笔记本，结果分析的"留痕"载体。
- 【可复用方法】分析流程固定分区：数据加载→清洗→EDA→统计检验→可视化→结论，每个发现旁配文字解读（现象→原因→证据）。固定随机种子保证可复现；用 `%matplotlib inline`；导出 `jupyter nbconvert --to html/pdf notebook.ipynb` 出报告。配合 papermill 可参数化批量执行。
- 【链接】https://jupyter.org/ ；nbconvert https://nbconvert.readthedocs.io/
- 【坑】乱序执行导致状态污染——交付前务必 Restart & Run All 验证从头跑通；大输出/图片会让 .ipynb 膨胀，提交前可清输出。

## Jupyter Book
- 【是什么】把多个 notebook/markdown 编译成带导航、交叉引用、可执行的在线书/报告站点（基于 Sphinx + MyST）。
- 【可复用方法】项目结构核心两文件：`_config.yml`（标题/作者/执行设置 execute）与 `_toc.yml`（章节目录树）。源用 MyST Markdown（支持 directive、引用、公式）。构建 `jupyter-book build mybook/` 产出 `_build/html`；可导出 PDF。适合把多组实验结果汇编成结构化分析报告/补充材料站点。注：项目已演进到 MyST/Jupyter Book 2 体系。
- 【链接】https://jupyterbook.org/
- 【坑】execute 设置不当会在 build 时重跑全部 notebook（慢/可能失败），CI 中常设 `execute: cache` 或 off；MyST 语法与普通 Markdown 有差异。

## 配对设计识别（paired vs independent，最常见的统计误用）
- 【是什么】当多个方法在**同一组单元**（同一批随机种子、同一组 CV 折、同一批测试样本）上评测时，方法间的逐单元差值是**配对**的。此时正确检验是**配对 t 检验**（差值近正态）或 **Wilcoxon 符号秩检验**（非正态），而非把两组当独立样本做 Welch t / Mann-Whitney。
- 【为什么重要】配对检验扣除了单元间方差（如"种子 7 天生偏高"对两方法同时抬高，被差值抵消），**功效严格高于**独立检验——同样数据更容易检出真实差异；反之误当独立会低估显著性、甚至把真实提升判为不显著。这是论文结果分析里最常见的统计误用之一。
- 【如何识别】结果表里有没有跨方法共享的列（`seed`/`fold`/`sample_id`）？若每个方法都在同一组该列值上各跑一次 → 配对设计。`analyze_results.py --paired-by seed` 即按此列对齐做配对检验（仅用两方法都有的共享单元，重复行先平均；共享单元 <2 则跳过并记原因）。
- 【配套量】配对效应量用 **Cohen's d_z = mean(diff)/sd(diff)**（注意 d_z 比独立 d 大，不可与独立 d 直接比较）；差值的 95% CI 用对差值序列做**百分位 bootstrap**（复用 significance_test.py 的 `bootstrap_ci`，不另造）。多对比较照样过 BH-FDR。
- 【坑】配对要求单元真正对齐——种子相同但数据划分/初始化不同则非真配对；样本级配对要确保是同一批测试样本的逐样本指标，而非两个不同测试集的聚合值；Wilcoxon 要求差值不全为 0（全 0 时按 p=1 处理）。

## 切片分析协议（slice / subgroup analysis：聚合指标的盲区）
- 【是什么】整体指标（总 acc、总 mAP）会掩盖**子群体上的系统性失败**：模型可能整体 85%，却在某个类别/某段数据/某个难度桶上只有 50%。切片分析 = 按有意义的维度把测试集切成子群，逐子群复算指标，找被平均数掩盖的坑。
- 【可复用方法（协议）】
  1. **选切片维度**：类别标签、数据来源/域、样本难度（如目标尺寸、文本长度）、敏感属性（性别/地区，关联公平性）、时间段（查时间漂移）。维度从研究问题与数据元信息来，不是穷举所有列。
  2. **逐切片复算指标 + 样本量 n**：每个子群必须带 n——小样本切片的指标方差大，**禁止对 n 很小的切片下强结论**（标"样本不足待核查"）。
  3. **对照整体基线找异常切片**：哪些切片显著低于整体？哪些方法在某切片反超/反负？用切片 × 方法的热图或分组柱看交互。
  4. **多切片比较要校正**：切了很多片就是多重比较，对"某切片显著差"的判断过 BH-FDR，避免切片越多越容易"碰巧显著"。
  5. **诚实归因**：切片差异是真实弱点，还是该切片本身标注噪声大/任务更难？需结合错例分析判断，别把数据问题当模型问题。
- 【与现有工具衔接】切片就是按维度列 `groupby` 后对每个子群跑 `analyze_results.py` 的同一套（EDA + 自动选检验 + 效应量 + FDR）；公平性维度的切片差异关联 a10 与必查清单的"公平性"项；时间段切片异常关联 Evidently 漂移检测。
- 【坑】切片维度若与标签强相关会制造伪发现；切片粒度太细导致每片 n 过小，结论不稳；只报"最差切片"不报其 n 是误导。报告每个切片结论都要带 n 与不确定性。


