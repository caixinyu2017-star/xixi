# light-data-engineering — 深度分析与同类对标

> 源：[`skills/light-data-engineering/SKILL.md`](../../../skills/light-data-engineering/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：科研流程中的"数据先行"关口技能:从数据体检、质量画像、防泄漏处理划分到自建数据集与隐私分级,在 idea 之前回答"数据够不够",并产出可复现流水线与数据卡。

## 核心运行逻辑
SKILL.md 把数据工作定位为科研 pipeline 的上游关口,核心原则是"数据先行四问"(是否足以支撑/质量是否可靠/规模是否足够/特征是否有挖掘价值),结论喂给 m03(idea-generation)/m04(idea-critique);同时设了一条从 m05(research-plan)回来的"回边",据实验矩阵的派生数据规格产出加噪/缺失/跨域/扫参评测集。方法论主体是按场景选引擎(pandas/Polars/DuckDB/Dask)、多工具质量画像(ydata-profiling/Deepchecks/GX/Frictionless)、EDA 七步+统计检验决策树、清洗-缺失-异常-特征-增强-划分处理链,贯穿一条"防数据泄漏铁律"(先划分再增强只增训练折、所有 fit 类预处理进 Pipeline 只在训练折 fit、按数据性质选 CV)。技能不重造轮子:统计检验/一致性/重采样统一复用仓库根 code_assets,自身只补四个纯 Python 零依赖脚本作为可运行闸门。设计上诚实克制:启发式标记只当假设不当结论,LLM 预标注不当真值,访问分级只按声明判定真实脱敏仍交 a10。

## 关键步骤
- 1. 数据体检:概览(形状/类型/真实内存/缺失率)→按数据规模选引擎→多工具质量画像→给出可直接用/需清洗/不足以支撑/需补采的明确结论
- 2. EDA 七步(结构→缺失→单变量→双变量→多变量→目标关系→质量小结)+统计检验决策(查前提→选检验→报效应量与置信区间→多重校正),警惕 p-hacking/HARKing
- 3. 处理流程:清洗→按机制(MCAR/MAR/MNAR)处理缺失→异常值(区分错误vs真实极端)→特征工程→数据增强(先划分再增强只增训练折)→防泄漏划分(分层/TimeSeriesSplit/GroupKFold)
- 4. 找现成数据集(OpenML/HF/Kaggle,锁版本保复现);自建则规划采集/标注规范/格式/datasheet/隐私合规/发布,标注走 LLM 预标注+人工审核闭环,IAA 复用 agreement.py,标错检测用 cleanlab
- 5. 产出四件套:数据质量报告(含四问)、可复现流水线(交 a03)、划分方案、dataset_card;数据按 access_level 分级守门,登记 db04/db09,隐私上报 a10

## 自带资产
- scripts/data_doctor.py — CSV→Markdown 数据体检报告,检测全空/常量列、重复行、高基数、IQR异常、强相关、目标泄漏提示,按HIGH/MED/LOW排序,带合成自测断言
- scripts/safe_split.py — 按task(clf/reg/timeseries/group)建Pipeline+ColumnTransformer并自动选CV,核心卖点是泄漏断言:证明预处理每折单独refit(折内mean≠全量mean)
- scripts/quality_gate.py — 纯pandas+PyYAML的CSV质量门禁,支持dataset/columns规则(dtype/required/non_null/unique/min/max/enum/regex),退出码0/1可直接做CI闸门
- scripts/check_access_level.py — 数据访问分级守门,三态pass/blocked/unknown,raw数据流向paper/figure/public-repo被阻断,可当pipeline闸门
- examples/rules.example.yaml — quality_gate的YAML规则示例,带逐行注释说明各约束
- templates/annotation_guide.md — 标注规范模板:类目定义/边界案例判定/LLM辅助+人工审核闭环/质检抽样率/IAA门槛(κ分级)
- assets/data_card_template.md — datasheet模板,10节字段对齐db04,含质量评估/偏差隐私风险/访问分级/推荐划分/溯源核实
- references.md — 19个工具逐条核查笔记(是什么/可复用方法+真实端点/链接/已知坑),含版本断层与停维护警示(GX1.x、Evidently、Vaex淘汰)

## 优点
- 防数据泄漏是真正的主线且贯彻到位:SKILL正文、references的sklearn节、数据增强红线、safe_split的可执行泄漏断言四处呼应,这是审稿人最常打回的硬伤,技能把它做成了可验证的工件而非口号
- 脚本工程质量高且诚实:四个脚本全部纯Python零网络依赖、全带--selftest用合成数据+断言验证检测器真的触发(如dup_rows==10、income在outliers、score与score_copy强相关),safe_split甚至用'折内mean≠全量mean'反证无泄漏,可信度远高于只给代码片段
- references.md不是API罗列而是带'已知坑'的核查笔记,且诚实标注版本断层(GX 0.x↔1.x、Evidently近年大改、Vaex 2023停维护已淘汰)和'文档站网络受限未能逐页核实',符合不臆造端点的要求
- 诚实克制的设计哲学一以贯之:启发式标记当假设不当结论、LLM预标注不可当真值必须人工闭环、cleanlab找候选人工裁定不全自动删、check_access_level只按声明判定真实脱敏仍交a10——避免给用户虚假的安全感
- 不重造轮子的边界清晰:统计检验/效应量/多重校正复用code_assets/stats_tests.py,IAA复用agreement.py,长尾复用longtail_resample.py,引擎选型以a09 decision_matrix.md为单一口径,降低维护重复与不一致风险(已核实这些sibling文件真实存在)
- 在科研pipeline中的位置设计巧妙:既是idea前的上游关口(四问喂m03/m04),又承接m05实验阶段的派生数据回边,把'数据工程'从一次性前处理升级为贯穿研究全程的双向节点

## 缺点 / 可被质疑处
- SKILL正文宣称的能力广度与自带可运行脚本严重不匹配:正文覆盖图像/文本/时序/表格全模态增强、多引擎大数据、漂移监控、置信学习等,但脚本只覆盖表格小数据(data_doctor/quality_gate/safe_split全是pd.read_csv单机内存),非表格模态和大数据场景完全无工件支撑,只能靠references口述+外部库,落地能力有断层
- data_doctor的泄漏检测过于薄弱且易误导:leakage_hint仅在target是数值且|corr|≥0.98时触发,对分类目标、类别特征、以及最常见的'划分前全量fit'这类时序/泄漏完全无能为力;高基数阈值card_thresh=0.5、相关0.9等魔数无依据也不随行数自适应,小表上会频繁误报
- safe_split存在真实可用性缺口:run_cv对timeseries任务仍调用cv.split(X,y)但TimeSeriesSplit要求数据已按时间排序,脚本既不排序也不校验时间列,用户给乱序数据会静默得到错误(穿越)结果;且StratifiedGroupKFold的触发用'y.nunique()<=20'硬判分类/回归,对20类以上分类会误退化为GroupKFold丢失分层
- quality_gate的datetime/int类型判定有副作用风险:int判定对float列做np.mod检查会把含NaN或超大浮点的列误判;datetime用pd.to_datetime(errors='raise')对大表逐值解析很慢且对混合格式行为不可控;regex用pat.search(非fullmatch)对email等'整串匹配'语义偏松,示例正则也确实只是loose check但未在正文强调局限
- 统计检验决策树、EDA七步、增强红线等核心方法只停留在SKILL与references的文字描述,无对应脚本或worked example,而同仓库其他技能(light-result-analysis、light-figure-drawing)都配了examples/worked_example,本技能examples目录只有一个rules.yaml,缺少端到端走查样例,用户难以照搬
- 对'数据规模是否足够'这一四问之一缺乏可操作判据:SKILL反复强调规模充足性却没给样本量估算、功效分析(power analysis)、或最小样本/类的任何工具或经验阈值,而stats_tests.py是否含power analysis未在本技能引用,这使'四问'里最量化的一问反而最空泛
- 访问分级模型偏简化:SINK_EXPOSURE把paper与figure都设为2、public-repo与public-release都设为3,但论文附录原始数据表与一张聚合图的暴露风险并不相同;且raw→只能internal-analysis(0)意味着raw连'给导师看的internal-report(1)'都被blocked,可能过严产生大量误阻断

## 可优化点（供后续逐技能优化）
- 补齐模态-工件鸿沟:为非表格场景至少各加一个带--selftest的最小脚本或worked example——如image_aug_check.py(验证bbox/mask随albumentations同步变换、断言验证折不被增强)、text_aug_label_guard.py(回译/同义词替换后标签语义未翻转的抽检),让正文宣称的全模态能力有可运行落点
- 强化data_doctor泄漏检测:增加分类目标的泄漏检测(用单特征对target的AUC/互信息≥阈值)、ID-like列检测(unique_ratio≈1且非数值)、以及'高基数类别特征对小样本'的过拟合风险提示;魔数阈值改为随n_rows自适应或可配置并在报告里说明依据
- 修复safe_split时序正确性:新增--time-col参数,timeseries任务强制按时间列排序并校验单调性,不提供时显式报错而非静默;StratifiedGroupKFold的分类判定改用task显式声明或检测y是否整数/低基数而非硬编码20;同时输出每折的train/val索引范围供人工核查穿越
- 给quality_gate加更稳健的类型校验与性能护栏:int判定先排除全NaN列、datetime解析加format参数与抽样预检、regex区分search/fullmatch由规则指定;对大表加--sample抽样校验选项;并支持规则级severity(error/warn)让部分检查不一票否决
- 补一份examples/worked_example:用一个真实风格的小数据集(如复用dairygoat项目数据)端到端走一遍体检→质量门禁→防泄漏划分→数据卡填写,展示四问如何下结论、quality_report.md与data_card.md长什么样,与其他Light技能的worked_example体例对齐
- 把'规模是否足够'变可操作:引用或补充power analysis工具(检查stats_tests.py是否已有,无则补),给出分类每类最小样本、回归样本/特征比、检测任务每类实例数等经验阈值清单,让data_doctor或一个新脚本能对'规模四问'给出量化预警
- 细化访问分级模型:拆分paper正文表格与figure的暴露度,raw放行到internal-report(导师内部),增加'aggregated/k-anon'中间级,并在check_access_level输出里附带建议的脱敏动作(对齐data_card的redaction_actions字段),让守门结果直接可执行
- 在SKILL显著位置标注每个外部库的版本敏感度与最小验证命令:GX/Evidently/Polars等API易变,可在references每条加一行'本笔记核对于X版本',并提示用户运行前先验证环境,降低照搬过期API报错的概率

## 与其他 Light 技能/知识库的衔接
上游产出"数据先行四问"结论喂给 m03(light-idea-generation)与 m04(light-idea-critique),决定 idea 是否有数据基础;承接 m05(light-research-plan)实验矩阵的派生数据规格回边,产出 ROB/GEN/SEN 评测集回填 db04。可复现流水线交 a03(light-backend-coding)落地实现。引擎选型以 a09(light-tool-selection)的 decision_matrix.md 为单一口径,不自行裁定。隐私/许可/脱敏复核上报 a10(light-research-ethics)。强复用仓库根 code_assets:统计检验用 stats_tests.py、标注一致性用 agreement.py、长尾重采样用 longtail_resample.py(均已核实存在)。数据集登记 db04(数据集卡)与项目库 db09;data_card_template 字段显式对齐 db04。标准工件命名(quality_report.md/data_card.md)遵循 CONVENTIONS §6.1。与 light-consistency(术语/指标一致性)、light-self-review(收尾自查)作为常驻技能在后台协同。

---

## GitHub 同类前沿技能对标

GitHub 上的同类项目分两类:一类是 Light 直接调用/封装的成熟工具库(ydata-profiling、Great Expectations、deepchecks、pandera、cleanlab、evidently、frictionless、Croissant),它们各自把'画像/校验/漂移/标注检测/数据卡'某一环做到工业级,但都是单点能力,不提供方法论决策、不串科研 pipeline、不管隐私分级;另一类是 LLM 数据分析 agent(DeepAnalyze、DataMind、Auto-Analyst),走端到端自动化、交互体验前沿,但偏通用 BI 而非科研上游,且普遍缺少 Light 那套'诚实克制'纪律(启发式只当假设、LLM 标注不当真值、防泄漏铁律)与可复现产出。Light 的差异化在于它不是工具也不是黑盒 agent,而是把这些工具按场景编排成'数据先行四问→喂 idea-generation、回边接实验矩阵派生数据'的科研关口方法论,自身只补四个零依赖闸门脚本,定位是流程编排与判断框架而非重造轮子。</comparison_summary>
<light_can_learn">[
    "数据卡可对齐 mlcommons/croissant 的机器可读标准格式(data_card_template.md 增产一份 croissant JSON-LD),便于直接发布到 HF/Kaggle/OpenML 并被自动索引,而不止人读 Markdown。",
    "quality_gate.py 可借鉴 pandera 的 schema-as-code 表达力(类型+统计+假设检验内联),在保持零依赖的同时提供可选的 pandera 后端,增强校验表达能力。",
    "data_doctor.py 报告偏纯文本,可借鉴 ydata-profiling 的 r1.compare(r2) 思路,补一个清洗前后/train-test 画像对比模式,直观暴露分布偏移。",
    "可参考 DeepAnalyze/Auto-Analyst 的 agentic 端到端编排,把现有四个闸门脚本串成一条可自动巡检的 pipeline(体检→门禁→划分→访问分级)一键跑,降低人工串联成本。",
    "考虑把技能投放到 VoltAgent/awesome-agent-skills 等清单仓库提升曝光,同时反向调研其中数据类技能的高频用法补齐自身覆盖。",
    "evidently/deepchecks 都提供漂移/泄漏的现成可视化报告,Light 的防泄漏铁律目前靠 safe_split.py 断言验证,可补一个把 train-test 泄漏检测结果可视化输出的环节,让'铁律'可被审阅而非只在脚本里断言。"
  ]</light_can_learn>
</invoke>


| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [ydataai/ydata-profiling](https://github.com/ydataai/ydata-profiling) | 一行代码出整体 EDA/质量画像 HTML 报告(原 pandas-profiling),含相关性、缺失、告警、train/test 对比。 | 13598 | 2026-04-22 | 强:开箱即用的可视化 EDA 报告深度远超 Light 的 data_doctor.py 纯文本报告;社区成熟。弱:只是单工具,不给方法论决策(何时用哪种检验、防泄漏铁律、四问结论)、不衔接科研 pipeline、不管数据集构建与隐私分级。Light 正是把它当画像工具之一调用。 |
| [great-expectations/great_expectations](https://github.com/great-expectations/great_expectations) | 声明式数据质量门禁框架:Expectation Suite + Checkpoint + Data Docs,做可复现的数据验证。 | 11555 | 2026-06-13 | 强:工业级、可扩展、Data Docs 自动文档、生态广。弱:重、上手成本高(1.x/0.x API 断层),纯质量门禁,不涉 EDA 方法论/划分防泄漏/数据集卡/科研定位。Light 的 quality_gate.py 是其零依赖轻量替身,可做 CI 但能力远不及。 |
| [cleanlab/cleanlab](https://github.com/cleanlab/cleanlab) | 置信学习定位标注错误/数据问题样本,自动给出可疑样本排序清单,支持图像/文本/表格。 | 11511 | 2026-01-13 | 强:标注质量检测的事实标准,算法严谨、覆盖多模态。弱:只解决'找错标'一个点。Light 直接在 SKILL 里引用 cleanlab 做标注质检,并强调 pred_probs 必须 out-of-sample、top-K 人工裁定不全自动删——是对它的正确用法封装而非竞争。 |
| [evidentlyai/evidently](https://github.com/evidentlyai/evidently) | 数据/模型漂移与质量监控,按列选 KS/PSI/卡方/Wasserstein 出报告,面向生产监控。 | 7595 | 2026-05-02 | 强:漂移监控专业、生产级、报告丰富。弱:偏生产 MLOps 监控,非科研上游'数据够不够'判断;近年 API 大改。Light 把它列为漂移监控工具并提醒'检出漂移≠有害需结合业务',定位互补。 |
| [unionai-oss/pandera](https://github.com/unionai-oss/pandera) | 轻量、表达力强的 DataFrame 统计校验库,schema 即代码,支持 pandas/Polars/PySpark。 | 4377 | 2026-06-12 | 强:比 GX 轻、与代码贴合、类型/统计校验优雅,多后端。弱:同样只是校验库,无 EDA/划分/数据集构建/科研衔接。可作 Light quality_gate 的更强替代后端,Light 当前选了零依赖纯 pandas+YAML 走极简。 |
| [deepchecks/deepchecks](https://github.com/deepchecks/deepchecks) | 数据与模型的结构化校验套件:data_integrity、train_test_validation(漂移/新类别/train-test 泄漏)。 | 4023 | 2025-12-28 | 强:成套泄漏/完整性检查现成可跑、报告完善。弱:库本身不教方法、不管数据集卡与隐私、不串科研流程。Light 在 SKILL 直接引用其 data_integrity/train_test_validation 套件,理念高度一致(都强调 train-test 泄漏检测)。 |
| [ruc-datalab/DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze) | 面向自主数据科学的 agentic LLM,端到端自动完成数据分析与报告生成。 | 4220 | 2026-04-13 | 强:真·自主 agent,能端到端跑分析、有模型训练成果。弱:黑盒自动化,缺 Light 那套'诚实克制'纪律(启发式只当假设、LLM 标注不当真值、防泄漏铁律)与科研定位/隐私分级闸门。前沿但可复现性与严谨约束不如 Light 的人工把关流程。 |
| [FireBird-Technologies/Auto-Analyst](https://github.com/FireBird-Technologies/Auto-Analyst) | 开源 AI 数据分析多智能体系统,自然语言驱动 EDA、可视化与建模。 | 698 | 2026-04-15 | 强:对话式自动分析、多 agent 协作、产品化 UI。弱:面向通用 BI 分析而非科研上游关口,无防泄漏铁律/数据集卡/隐私分级/与 idea-generation 的衔接。交互体验强,科研严谨度与可控产出弱于 Light。 |
| [mlcommons/croissant](https://github.com/mlcommons/croissant) | ML 数据集的标准化元数据格式(datasheet/data card),已被 HF/Kaggle/OpenML 采用。 | 856 | 2026-06-01 | 强:跨平台标准、机器可读、生态背书(MLCommons)。弱:只是元数据 schema,不做体检/清洗/划分/检测。Light 的 data_card_template.md 是同类'数据卡'但偏科研人读+对齐内部 db04,可借鉴 Croissant 走机器可读标准格式以便发布到 HF/Kaggle。 |
| [frictionlessdata/frictionless-py](https://github.com/frictionlessdata/frictionless-py) | 数据描述/校验框架:推断 Table Schema、validate 出 cell/row 级错误,标准化数据交换。 | 823 | 2026-06-11 | 强:标准化元数据+校验一体、Data Package 规范成熟。弱:聚焦表格交换校验,无 EDA 方法论/防泄漏/增强/数据集构建全链。Light 把它列为'标准化交换/发布元数据'工具,定位互补。 |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 汇集 200+ 官方与社区 Agent Skills(兼容 Claude Code/Codex/Cursor 等)的清单仓库。 | 25158 | 2026-06-12 | 强:同为'agent skill'生态的聚合入口、曝光高。弱:是清单不是技能本身;其中数据类技能多为通用清洗/分析,鲜有 Light 这种'科研数据先行关口+防泄漏铁律+四问+回边到实验矩阵'的成体系科研技能。是 Light 可投放/对标曝光的渠道。 |
