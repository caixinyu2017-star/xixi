# light-data-engineering 参考工具笔记

逐工具核查笔记。每条含【是什么】【可复用方法/真实端点/参数】【链接】【已知坑/局限】。
凡是核查受限的，明确标注「未能完整核实」，不臆造端点。

## EDA workflows（探索性数据分析流程）
- 【是什么】Tukey 提出的探索性数据分析，目标是先“看懂数据”再建模：理解结构、发现异常、形成假设。社区已收敛出一套可复用的分步框架。
- 【可复用方法】标准 7 步：①结构概览（shape/dtypes/head/describe/info）②缺失分析（缺失率矩阵、缺失模式，missingno 的 matrix/bar/heatmap/dendrogram）③单变量（数值直方图+箱线图看分布与偏度；类别用频次/条形）④双变量（数值-数值散点+相关；类别-数值分组箱线；类别-类别交叉表/卡方）⑤多变量（相关热力图、配对图 pairplot、分组着色、PCA 降维可视化）⑥目标关系（特征 vs 目标的分组统计，初判预测力与泄漏）⑦质量与异常小结（重复、基数、常量列、ID 列、潜在泄漏列）。
- 【链接】https://r-statistics.co/Exploratory-Data-Analysis-in-R.html ；https://kindatechnical.com/statistical-inference/exploratory-data-analysis-workflow.html
- 【已知坑】EDA 结论只是假设而非证据，别用同一份数据既探索又下统计结论（会过拟合/数据窥探）；相关不等于因果；大数据下先抽样再画图避免渲染卡死。

## Statistical Analysis workflows（统计分析流程）
- 【是什么】把 EDA 发现的假设上升为可检验结论的流程：选检验、查前提、算效应量、控多重比较。
- 【可复用方法】决策路径：①先定问题类型（比较组间均值/比例、相关、关联）②查前提——正态性（Shapiro-Wilk，n 大时直方图/QQ 图更可靠，因 Shapiro 在大样本过于敏感）、方差齐性（Levene）③选检验：两组数值正态→独立样本 t 检验（方差不齐用 Welch t）；非正态→Mann-Whitney U；配对→配对 t/Wilcoxon；多组→ANOVA/Kruskal-Wallis；类别关联→卡方/Fisher 精确④必报效应量（Cohen's d、Cliff's delta、Cramér's V、相关 r/ρ）和置信区间，别只报 p 值⑤多重比较校正：Bonferroni（保守）或 Benjamini-Hochberg FDR（推荐，控假发现率）。
- 【链接】https://en.wikipedia.org/wiki/Statistical_hypothesis_test ；https://statisticsbyjim.com/hypothesis-testing/ ；多重检验校正常见误区：https://sequenceanddestroy.substack.com/p/issue-76-what-llms-get-wrong-about
- 【已知坑】p<0.05 不等于“重要”（大样本下微小差异也显著，故必看效应量）；做了多个检验不校正会假阳性暴增；先看数据再挑假设/检验（HARKing、p-hacking）使结论失真。

## Pandas
- 【是什么】Python 表格数据事实标准库，单机内存内分析。
- 【可复用方法】读入即定 dtype（`pd.read_csv(..., dtype=..., parse_dates=...)`）省内存且避免类型踩雷；`df.info(memory_usage='deep')` 看真实内存；类别列转 `category`、整型用 `Int8/Int16` 等可大幅省内存；`df.isna().mean()` 一行得缺失率；`df.duplicated()`/`drop_duplicates`；`df.describe(include='all')`；分组 `groupby().agg({...})`；缺失插补 `fillna`，类型转 `astype`，时间用 `pd.to_datetime`。
- 【链接】https://realpython.com/polars-vs-pandas/
- 【已知坑】单机内存上限是硬约束（经验上数据超过内存的 ~1/3 就吃力）；`object` dtype 极慢极占内存；链式赋值 `SettingWithCopyWarning`；默认行操作 apply 慢，优先向量化。

## Polars
- 【是什么】Rust 写的高性能 DataFrame，多线程 + 查询优化 + 惰性执行，常比 pandas 快数倍到十几倍。
- 【可复用方法】两套 API：即时 `pl.read_csv` 和惰性 `pl.scan_csv`（返回 LazyFrame，不立即读数据）。惰性管线 `pl.scan_csv(...).filter(...).group_by(...).agg(...).collect()`，`collect()` 才触发执行，期间做谓词下推、投影下推等优化；超大数据用 `collect(streaming=True)` 分块流式跑，内存可控。表达式 API：`pl.col("x").filter(...).sum()`，链式且并行。
- 【链接】https://docs.pola.rs/api/python/stable/reference/api/polars.scan_csv.html ；https://docs.pola.rs/user-guide/lazy/execution/
- 【已知坑】API 与 pandas 不兼容（无索引概念、语法不同），迁移有成本；生态/第三方集成不如 pandas 广；惰性模式下报错点延后到 collect，调试需注意。

## Dask
- 【是什么】并行/分布式计算框架，`dask.dataframe` 提供 pandas 兼容 API，把大数据切成多个 pandas 分区，可单机多核或集群跑。
- 【可复用方法】`dd.read_csv("*.csv")` 读多文件，操作 lazy，`.compute()` 触发；适合“数据比内存大但代码想保持 pandas 写法”的场景；`.persist()` 把中间结果留在内存；用 dashboard 看任务图与瓶颈。也有 `dask.array`（大 numpy）、`dask.bag`、`dask.delayed`（自定义并行）。
- 【链接】https://medium.com/data-science/beyond-pandas-spark-dask-vaex-and-other-big-data-technologies-battling-head-to-head-a453a1f8cc13 ；https://www.kdnuggets.com/2021/03/pandas-big-data-better-options.html
- 【已知坑】分区大小要调（太多小分区调度开销大）；不是所有 pandas 操作都支持/高效（涉及全局 shuffle 的 sort、某些 groupby 较贵）；小数据上 Dask 反而比 pandas 慢（调度开销）。

## DuckDB（超内存分析首选）
- 【是什么】嵌入式分析型数据库（OLAP 版 SQLite），单文件零服务，直接对 parquet/csv/pandas/polars 跑 SQL，out-of-core 执行超内存时自动 spill 到磁盘。
- 【可复用方法】`import duckdb; duckdb.sql("SELECT col, count(*) FROM 'data/*.parquet' GROUP BY col")` 直查文件无需先导入；`duckdb.sql("...").df()` / `.pl()` 出 pandas/polars；`SET memory_limit='8GB'; SET temp_directory='/tmp'` 控内存与 spill；与 Polars 互通（`pl.read_database` 或直接查 `pl.scan_*` 的 Arrow）。适合“单机、超大、做统计/聚合/连接”的体检与特征工程。
- 【链接】https://duckdb.org/docs/ ；https://duckdb.org/2021/06/25/querying-parquet.html
- 【已知坑】OLAP 取向，逐行 OLTP 更新不是强项；极宽表全列扫描仍吃内存（按需 `SELECT` 列）；版本间存储格式偶有不兼容，长期落盘优先 parquet 而非 `.duckdb`。

## Vaex（已淘汰，仅存档）
> ⚠ Vaex 2023 后基本停止维护，**不再推荐新项目使用**；超内存场景迁 DuckDB（SQL）或 polars streaming（DataFrame 写法）。引擎选型以 a09 tool-selection `decision_matrix.md` 为单一口径。以下为历史方法存档。
- 【是什么】面向单机超大表（亿~十亿行）的 DataFrame 库，核心是内存映射 + 惰性表达式，几乎零内存开销地扫数据。
- 【可复用方法（历史）】把 CSV 先转 HDF5/Arrow（`df.export_hdf5`），之后 `vaex.open` 内存映射瞬间打开；虚拟列（virtual columns）——新列只存表达式不占内存，按需计算；惰性表达式 + 流式聚合一遍扫盘出结果。
- 【链接】https://vaex.io/blog/dask-vs-vaex-a-qualitative-comparison
- 【已知坑】项目活跃度近年下降、维护停滞（淘汰主因）；强项是单机大数据的聚合/扫描，不是分布式也不是复杂 join/ETL；同等场景 DuckDB / polars streaming 更活跃、生态更广。

## scikit-learn（数据划分/预处理相关）
- 【是什么】Python 机器学习库，本技能主要用其数据划分与预处理防泄漏能力。
- 【可复用方法】划分：`train_test_split(X, y, test_size=, stratify=y, random_state=)`（分类务必 stratify 保持类比例）；交叉验证选择——`StratifiedKFold`（分类）、`KFold`（一般）、`TimeSeriesSplit`（时序，只用过去预测未来，防穿越）、`GroupKFold`/`StratifiedGroupKFold`（同一实体/患者/用户不跨集，防分组泄漏）。防泄漏关键：所有 fit 类预处理（StandardScaler、SimpleImputer、OneHotEncoder、特征选择）必须放进 `Pipeline`/`ColumnTransformer`，在交叉验证里只对训练折 fit，绝不能先在全量数据上 fit_transform 再划分。
- 【链接】https://scikit-learn.org/1.5/modules/cross_validation.html ；https://scikit-learn.org/1.5/modules/generated/sklearn.model_selection.train_test_split.html
- 【已知坑】最常见泄漏=在划分前对全量数据做缩放/插补/特征选择；时序数据用随机划分=未来信息泄漏；分组数据（重复个体）用普通 KFold 会高估性能。

## Great Expectations (GX)
- 【是什么】数据质量校验框架：把“对数据的期望”写成可执行、可版本化、能出文档的断言（Expectation），用于流水线质量门禁。
- 【可复用方法】GX 1.x 核心对象链：`context = gx.get_context()` → 在 context 上加 Data Source / Data Asset / Batch Definition → 建 Expectation Suite（一组 Expectation）→ Validation Definition（绑定 batch 与 suite）→ Checkpoint（运行校验并触发动作）。常用 Expectation：`ExpectColumnValuesToNotBeNull`、`ExpectColumnValuesToBeBetween`、`ExpectColumnValuesToBeInSet`、`ExpectColumnValuesToBeUnique`、`ExpectColumnValuesToMatchRegex`、`ExpectTableRowCountToBeBetween`。能自动生成 Data Docs（HTML 校验报告）。注意 1.0 相比 0.x 大改 API（旧的 `great_expectations init`/`v3` batch_request 写法多已弃用）。
- 【链接】https://docs.greatexpectations.io/docs/core/introduction/ （文档站当前网络受限未能逐页核实，对象名依据 GX 1.x 公开资料）
- 【已知坑】0.x↔1.x API 断层大，照旧教程会报错，务必看版本；适合“规则明确的结构化数据门禁”，对自由文本/图像无能为力；期望套件需人工维护，否则随数据漂移失效。

## Frictionless Data
- 【是什么】开放数据打包与校验标准 + Python 框架（frictionless-py）：用 Data Package（datapackage.json）描述数据集，用 Table Schema 描述表字段类型/约束，做到自描述、可校验、可移植。
- 【可复用方法】CLI：`frictionless describe data.csv`（自动推断 schema 生成 descriptor）、`frictionless validate data.csv`（校验并报告 cell/row/header 级错误）、`frictionless extract`。Python：`from frictionless import describe, validate, Package, Resource`，`validate("datapackage.json")` 返回 report（含 valid 布尔与错误清单）。Table Schema 字段含 `name/type/format/constraints(required/unique/minimum/maximum/enum/pattern)`、`primaryKey`、`foreignKeys`。
- 【链接】https://framework.frictionlessdata.io/ ；https://framework.frictionlessdata.io/docs/guides/validating-data.html ；https://github.com/frictionlessdata/frictionless-py ；规范 https://specs.frictionlessdata.io
- 【已知坑】面向表格/结构化数据，复杂嵌套或非表格数据不适用；价值在“发布/交换标准化元数据”，不做统计画像；v4 与早期 datapackage 库 API 有差异，认准 frictionless-py 当前版本。

## ydata-profiling（原 pandas-profiling）
- 【是什么】一行生成完整 EDA HTML 报告：概览、每列分布、缺失、相关、交互、重复、告警。
- 【可复用方法】`from ydata_profiling import ProfileReport`；`profile = ProfileReport(df, title="...")`；输出 `profile.to_file("report.html")` 或 notebook 内 `profile.to_notebook_iframe()`。大数据用 `ProfileReport(df, minimal=True)` 关掉昂贵的相关/交互计算；时序数据 `tsmode=True` 并指定 `sortby`；对比两份数据集（如 train vs test、清洗前后）用 `report_a.compare(report_b)`。报告里的 “Alerts/Warnings” 直接给出高相关、高基数、常量、缺失、零值、唯一等质量信号。
- 【链接】https://github.com/ydataai/ydata-profiling （文档站本次未能逐页抓取，方法名依据库公开 API）
- 【已知坑】列多/行多时默认模式极慢且占内存，务必先抽样或开 minimal；相关矩阵在高维下计算昂贵；报告是“描述性体检”，不替代针对性统计检验与建模验证。

## Deepchecks
- 【是什么】面向表格/CV/NLP 的数据与模型校验库，把检查打包成 Suite，一次性跑出带通过/失败状态的交互报告。
- 【可复用方法】表格三大内置套件：`data_integrity()`（单数据集完整性：重复、混合类型、字符串不一致、特征-标签相关性/泄漏、异常值、冲突标签）、`train_test_validation()`（train/test 漂移、新类别、泄漏如 train-test 样本重叠、分布偏移）、`model_evaluation()`（性能、过拟合、弱分段）；`full_suite()` 全跑。用法：`from deepchecks.tabular import Dataset`，`ds = Dataset(df, label="target", cat_features=[...])`，`from deepchecks.tabular.suites import data_integrity`，`result = data_integrity().run(ds)`，notebook 直接展示或 `result.save_as_html()`。
- 【链接】https://docs.deepchecks.com/stable/user-guide/general/when_should_you_use.html ；https://docs.deepchecks.com/0.13/user-guide/tabular/auto_quickstarts/plot_quick_train_test_validation.html
- 【已知坑】需正确声明 `label` 与 `cat_features` 否则部分检查不准；某些检查要传入训练好的模型；检查项多，报告需人读取舍而非全盘当结论。

## Evidently AI
- 【是什么】数据与 ML 监控库：生成数据漂移、数据质量、模型性能报告与测试，可做生产环境持续监控。
- 【可复用方法】新版 API：`from evidently import Dataset, DataDefinition, Report`，`from evidently.presets import DataDriftPreset, DataSummaryPreset`；先 `Dataset.from_pandas(df, data_definition=DataDefinition(...))` 包装 current 与 reference 两份数据，再 `report = Report(metrics=[DataDriftPreset()])`，`snapshot = report.run(current_data=cur, reference_data=ref)`，输出 `snapshot.save_html(...)` / `.json()` / `.dict()`。漂移检测对数值/类别/文本按列选统计检验（KS、PSI、卡方、Wasserstein 等）并给 drift share。可接 Evidently 服务做监控面板。
- 【链接】https://docs.evidentlyai.com/docs/library/report ；https://docs.evidentlyai.com/docs/library/data_definition ；https://docs.evidentlyai.com/quickstart_ml
- 【已知坑】API 近一年大改（旧 `evidently.report`/`metric_preset` 写法变化大，照旧教程会失败，认版本）；漂移“被检测到”不等于“有害”，需结合业务判断；参考集选择不当会误报。

## OpenML
- 【是什么】开放机器学习平台：数据集、任务（task）、流程（flow）、运行（run）全部可编程获取与复现，便于找基准数据集与对比方法。
- 【可复用方法】轻量取数走 sklearn：`from sklearn.datasets import fetch_openml`，`fetch_openml(name="adult", version=, as_frame=True, return_X_y=)` 或 `fetch_openml(data_id=1590)`。完整能力走 openml-python：`import openml`，`openml.datasets.get_dataset(id)` 取数据集对象，`.get_data(target=..., dataset_format="dataframe")` 得 X/y；`openml.datasets.list_datasets(output_format="dataframe")` 检索；`openml.tasks.get_task(id)` 取标准化任务（含划分），`openml.runs.run_model_on_task(clf, task)` 跑并可上传复现。每个数据集有稳定 ID 与版本。
- 【链接】https://openml.github.io/openml-python/main/api.html ；https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_openml.html
- 【已知坑】社区上传数据质量参差，需自行体检；同名数据集有多版本，务必锁 version/data_id 保证可复现；大数据集下载可能慢，注意缓存目录。

## Hugging Face Datasets
- 【是什么】数据集库 + Hub：统一加载/处理大规模数据集，基于 Arrow 做零拷贝内存映射，支持流式。
- 【可复用方法】`from datasets import load_dataset`；`load_dataset("squad", split="train")`；本地文件 `load_dataset("csv"/"json"/"parquet", data_files=...)`；多配置 `load_dataset(name, config_name)`；超大数据 `streaming=True` 返回 IterableDataset 边下边用、不落全量到磁盘。处理用 `.map(fn, batched=True)`、`.filter`、`.train_test_split(test_size=)`、`.cast_column`。发布 `dataset.push_to_hub("user/name")`，并写 Dataset Card（README.md + YAML 元数据：license、language、task_categories、size_categories 等）。
- 【链接】https://huggingface.co/docs/datasets/loading ；https://huggingface.co/docs/hub/datasets-cards
- 【已知坑】首次下载与 Arrow 缓存占磁盘大，注意 `HF_HOME`/cache 清理；streaming 下不能随机索引、长度未知；上传需注意数据许可与隐私（Dataset Card 必须如实写 license 与已知偏差）。

## Kaggle Datasets
- 【是什么】Kaggle 的数据集托管与 API/CLI，便于检索与拉取公开数据集、发布自有数据集。
- 【可复用方法】认证：在账户页生成 API token 得 `kaggle.json`，放 `~/.kaggle/kaggle.json`（权限 600）或设环境变量 `KAGGLE_USERNAME`/`KAGGLE_KEY`。CLI：`kaggle datasets list -s <关键词>` 搜索；`kaggle datasets download -d <owner>/<dataset> [-f file] [--unzip]` 下载；竞赛数据 `kaggle competitions download -c <comp>`。发布：建 `dataset-metadata.json` 后 `kaggle datasets create -p <dir>`，更新版本 `kaggle datasets version -p <dir> -m "msg"`。
- 【链接】https://www.kaggle.com/docs/api ；https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md
- 【已知坑】需接受数据集/竞赛规则页条款后才能下载，否则 403；`kaggle.json` 是密钥不可入库；下载有速率与配额限制；许可各数据集不同，二次使用/发表前务必核对 license。

## 数据增强（按模态分工，附跨 split 泄漏红线）
> **红线：增强只在训练折内做，绝不跨 split 泄漏。** 先划分再增强；验证/测试集保持原始分布不增强（否则评测失真、指标虚高）。增强变换的随机性要固定种子；过采样/SMOTE 类必须只在训练折拟合（放进 Pipeline，参见 scikit-learn 节防泄漏铁律）。

### 图像 — albumentations
- 【是什么】高性能图像增强库（OpenCV 后端，比 torchvision transform 快），支持 bbox/mask/keypoint 随图同步变换，检测/分割任务首选。
- 【可复用方法】`import albumentations as A`；`A.Compose([A.RandomResizedCrop(h,w), A.HorizontalFlip(p=0.5), A.RandomBrightnessContrast(p=0.2), A.Normalize()], bbox_params=A.BboxParams(format="yolo", label_fields=["cls"]))`；调用 `aug(image=img, bboxes=bb, cls=labels)` 返回同步变换后的字典。几何变换会自动同步标注框/掩膜。
- 【链接】https://albumentations.ai/docs/ ；https://github.com/albumentations-team/albumentations
- 【已知坑】bbox_params 的 format 要与标注格式严格对应（coco/pascal_voc/yolo），错配静默产出错框；过强的颜色/遮挡增强会破坏小目标；mask 任务用 `additional_targets` 同步多掩膜。

### 文本 — nlpaug
- 【是什么】文本数据增强库，覆盖字符/词/句级：同义词替换、词嵌入近邻替换、上下文词（BERT MLM）插入/替换、回译（back-translation）。
- 【可复用方法】`import nlpaug.augmenter.word as naw`；同义词 `naw.SynonymAug(aug_src="wordnet")`、上下文 `naw.ContextualWordEmbsAug(model_path="bert-base-uncased", action="substitute")`、回译 `naw.BackTranslationAug(from_model_name=..., to_model_name=...)`；`aug.augment(text, n=3)` 出多条。
- 【链接】https://github.com/makcedward/nlpaug ；https://nlpaug.readthedocs.io/
- 【已知坑】同义词替换可能改变语义/情感标签（情感分类任务慎用，会翻转标签）；上下文/回译依赖下载大模型，离线环境失败；回译质量受中间语种影响；中文需对应中文模型与分词。

### 时序 — tsaug
- 【是什么】时间序列专用增强库，变换设计保持时序结构：抖动、缩放、时间扭曲（TimeWarp）、幅度扭曲、加噪、Drift、Pool、Quantize、Reverse、Crop。
- 【可复用方法】`import tsaug`；`my_aug = (tsaug.TimeWarp() * 5 + tsaug.Drift(max_drift=0.1) @ 0.5 + tsaug.AddNoise(scale=0.01))`；`X_aug = my_aug.augment(X)`（X 形状 (N, T) 或 (N, T, C)），`*` 重复、`@p` 以概率施加、`+` 串联。
- 【链接】https://tsaug.readthedocs.io/ ；https://github.com/arundo/tsaug
- 【已知坑】TimeWarp/Drift 会破坏严格周期性，预测任务慎用；多变量序列要保通道间同步变换；增强后若改变了与未来标签的因果关系会引入泄漏；分类任务确认变换不改类别语义。

## cleanlab（置信学习找标签错误）
- 【是什么】基于置信学习（confident learning）的标签质量库，用模型的交叉验证预测概率反推哪些样本**可能标错**，给出按"标错可能性"排序的样本清单。补"质量评估有标注质量指标却无检测手段"的缺口。
- 【可复用方法】关键输入是**out-of-sample 预测概率**（交叉验证得到，避免用训练样本自身预测）：`from sklearn.model_selection import cross_val_predict; pred_probs = cross_val_predict(clf, X, y, cv=5, method="predict_proba")`；找错 `from cleanlab.filter import find_label_issues; issues = find_label_issues(labels=y, pred_probs=pred_probs, return_indices_ranked_by="self_confidence")`；高层接口 `from cleanlab.classification import CleanLearning; CleanLearning(clf).fit(X, y)` 自动剔噪再训。多标注者一致性/众包真值估计用 `cleanlab.multiannotator`。
- 【链接】https://docs.cleanlab.ai/ ；https://github.com/cleanlab/cleanlab
- 【已知坑】pred_probs 必须 out-of-sample（用训练集自身概率会严重低估错误，违背置信学习前提）；模型太弱则"找出的错"多是模型自身偏差而非真标错，需人工复核 top-K 而非全盘删除；找出后的处置（重标/删除/降权）是数据决策，删样本要记录并评估对分布的影响。cleanlab 找候选 → 人工裁定，二者配合，不可全自动删。
- 【与一致性指标衔接】cleanlab 解决"单一标注与模型预测不一致"的标签错误检测；多标注者之间的一致性（IAA）用 `code_assets/agreement.py`（Cohen's κ / 加权 κ / Fleiss' κ / ICC(2,1)，已对齐 sklearn）。两者互补：IAA 评标注流程整体可靠度，cleanlab 定位具体可疑样本。

