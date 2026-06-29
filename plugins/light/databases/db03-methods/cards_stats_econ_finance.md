# db03 方法卡 — 统计 / 经济金融 / 因果推断

> 每张卡注明 maturity（经典|主流|新兴|过时|不推荐），避免提出落后方案。受版权全文不收录，仅元数据与开源链接。
> representative_papers 的标题/年份/被引/DOI 来自 OpenAlex 真实查询（https://api.openalex.org，mailto 礼貌池），查询日期 **2026-06-10**；被引数随时间变动。
> 查不到可信记录的字段写「待核查」，不编造。

字段 schema 同 db03：`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`

## 方法卡

```yaml
- method_name: 双重差分与多期双重差分 (DiD / staggered DiD)
  task_type: 政策评估、准实验因果推断、处理组/对照组在政策前后的平均处理效应估计
  input_data: 面板数据或重复截面数据；处理组/对照组标识、政策实施时间、结果变量、协变量
  output_result: 平均处理效应(ATT/ATE)、事件研究动态效应、置信区间与平行趋势检验
  core_assumption: 若无政策冲击，处理组与对照组结果趋势应平行；多期错位处理需避免传统 TWFE 权重污染
  advantages: 政策研究中直观、可解释；能控制时间不变个体差异和共同时间冲击；事件研究可展示动态路径
  limitations: 平行趋势不可完全验证；异质处理效应下传统 TWFE 可能有负权重/污染；政策预期效应与溢出会破坏识别
  common_baselines: 前后对比、横截面 OLS、固定效应模型、合成控制、倾向得分匹配+DiD
  evaluation_metrics: 平行趋势图、placebo test、预处理系数联合检验、聚类稳健标准误、敏感性分析
  suitable_datasets: World Bank WDI、OECD、Penn World Table、上市公司面板、城市/地区政策面板
  implementation_repo: R did/fixest、Stata csdid/reghdfe、Python linearmodels/statsmodels
  representative_papers:
    - "Difference-in-Differences with multiple time periods | 2020 | cited:1413 | doi:10.1016/j.jeconom.2020.12.001 | checked:2026-06-10"
    - "Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California’s Tobacco Control Program | 2010 | cited:5388 | doi:10.1198/jasa.2009.ap08746 | checked:2026-06-10"
  possible_innovation_points: 异质处理效应估计、空间溢出 DiD、机器学习构造对照组、政策强度连续处理、多源数据融合的动态效应; domain_scope=统计经济金融
  maturity: 主流  # 政策评估核心工具；多期 DiD 新规范已逐渐取代简单 TWFE

- method_name: 工具变量与局部平均处理效应 (IV / LATE)
  task_type: 内生性校正、因果效应识别、自然实验中的外生变异利用
  input_data: 结果变量、内生解释变量、工具变量、协变量；常见为横截面/面板/实验鼓励设计数据
  output_result: 2SLS/IV 估计量、LATE、第一阶段强度、过识别检验
  core_assumption: 工具变量相关性(relevance)、排除限制(exclusion)、独立性、单调性(LATE)
  advantages: 可处理遗漏变量、反向因果和测量误差；自然实验解释力强；LATE 明确效应人群
  limitations: 工具变量难找且排除限制常被质疑；弱工具导致偏误和大方差；LATE 只代表 complier，外推有限
  common_baselines: OLS、固定效应、控制函数、RDD、DiD、匹配方法
  evaluation_metrics: 第一阶段 F 统计量、弱工具检验、Sargan/Hansen 过识别检验、稳健性/安慰剂检验
  suitable_datasets: 劳动经济、教育政策、医疗政策、金融冲击、自然实验数据
  implementation_repo: R ivreg/AER、Stata ivreg2、Python linearmodels.iv
  representative_papers:
    - "Identification of Causal Effects Using Instrumental Variables | 1996 | cited:4203 | doi:10.1080/01621459.1996.10476902 | checked:2026-06-10"
    - "Double/debiased machine learning for treatment and structural parameters | 2017 | cited:2420 | doi:10.1111/ectj.12097 | checked:2026-06-10"
  possible_innovation_points: 高维控制下的 DML-IV、弱工具稳健推断、空间/网络工具变量、机器学习发现候选工具后的人工识别审查; domain_scope=统计经济金融
  maturity: 经典  # 计量经济学核心识别工具，DML 扩展让高维控制场景更可用

- method_name: 断点回归设计 (Regression Discontinuity Design, RDD)
  task_type: 阈值规则下的局部因果效应估计(考试分数、年龄、收入线、政策资格线等)
  input_data: running variable、阈值、处理指示、结果变量、阈值附近样本
  output_result: 阈值处局部平均处理效应、带宽敏感性、McCrary 密度检验与协变量平衡检验
  core_assumption: 个体无法精确操纵阈值附近的 running variable；潜在结果在阈值处连续
  advantages: 识别直观、接近局部随机实验；图形展示有说服力；无需全局模型正确
  limitations: 只估计阈值附近局部效应；带宽/多项式阶数敏感；操纵阈值或排序变量测量误差会破坏识别
  common_baselines: OLS 控制函数、DiD、IV、匹配、局部线性回归
  evaluation_metrics: 带宽敏感性、左右密度连续性、协变量跳跃检验、donut RDD、局部线性/二次稳健性
  suitable_datasets: 教育录取线、社保/医保资格线、最低工资/税收门槛、金融监管阈值
  implementation_repo: R rdrobust/rdd、Stata rdrobust、Python rdd/linearmodels 自实现
  representative_papers:
    - "Regression Discontinuity Designs in Economics | 2010 | cited:65 | doi:10.1257/jel.48.2.281 | checked:2026-06-10"
    - "The central role of the propensity score in observational studies for causal effects | 1983 | cited:30848 | doi:10.1093/biomet/70.1.41 | checked:2026-06-10"
  possible_innovation_points: 多阈值/空间 RDD、fuzzy RDD 与 IV 结合、机器学习辅助带宽/异质效应、阈值操纵鲁棒诊断; domain_scope=统计经济金融
  maturity: 主流  # 准实验研究常用设计；需要严格图示和稳健性检查

- method_name: 倾向得分与匹配/加权 (Propensity Score Matching / IPW)
  task_type: 观察性研究中处理组/对照组平衡、平均处理效应估计
  input_data: 处理指示、结果变量、处理前协变量；可为医疗、社会科学、营销、金融样本
  output_result: 倾向得分、匹配样本/权重、ATE/ATT、协变量平衡诊断
  core_assumption: 条件可交换性(无未观测混杂)与重叠性(positivity)；倾向得分能平衡可观测协变量
  advantages: 直观解释“可比样本”；平衡诊断明确；可与 DiD、Doubly Robust、TMLE 结合
  limitations: 不能解决未观测混杂；PS 模型错设会偏；极端权重导致高方差；匹配会丢样本
  common_baselines: 协变量调整 OLS、IPW、AIPW/DR、DML、工具变量
  evaluation_metrics: 标准化均差(SMD)、Love plot、有效样本量、重叠图、敏感性分析
  suitable_datasets: MIMIC-IV/临床观察数据、社会调查、政策项目评估、用户增长/营销数据
  implementation_repo: R MatchIt/WeightIt/cobalt、Python causalinference/EconML/DoWhy
  representative_papers:
    - "The central role of the propensity score in observational studies for causal effects | 1983 | cited:30848 | doi:10.1093/biomet/70.1.41 | checked:2026-06-10"
    - "Machine learning in the estimation of causal effects: targeted minimum loss-based estimation and double/debiased machine learning | 2019 | cited:79 | doi:10.1093/biostatistics/kxz042 | checked:2026-06-10"
  possible_innovation_points: ML 倾向得分、双重稳健估计、重叠性自动诊断、临床研究报告规范化、未观测混杂敏感性可视化; domain_scope=统计经济金融
  maturity: 经典  # 观察性研究标准工具，但必须强调“只能平衡可观测协变量”

- method_name: 金融波动与时序模型 (GARCH / VAR)
  task_type: 金融收益波动建模、宏观多变量动态关系、冲击响应与风险预测
  input_data: 金融收益率/价格序列、宏观时间序列、利率/汇率/通胀等多变量序列
  output_result: 条件方差/波动率、VaR/ES 风险指标、脉冲响应、方差分解、Granger 关系
  core_assumption: GARCH 假设条件异方差随过去残差/方差演化；VAR 假设变量间线性动态滞后关系
  advantages: 解释性强、金融/宏观标准工具；可做风险管理、政策冲击分析；与机器学习预测形成强基线
  limitations: 线性/参数假设强；结构突变与高维变量难处理；Granger 不等于因果；波动极端尾部需重尾/非线性扩展
  common_baselines: ARIMA、EWMA、随机波动率模型、LSTM/Transformer、Bayesian VAR、DCC-GARCH
  evaluation_metrics: AIC/BIC、残差诊断、波动预测 QLIKE/MSE、VaR 回测(Kupiec/Christoffersen)、预测 RMSE/MAE
  suitable_datasets: FRED-MD、Fama-French 因子、WRDS/CRSP、Yahoo Finance、Wind/CSMAR(授权)
  implementation_repo: R rugarch/vars、Python arch/statsmodels、MATLAB Econometrics Toolbox
  representative_papers:
    - "Generalized autoregressive conditional heteroskedasticity | 1986 | cited:22242 | doi:10.1016/0304-4076(86)90063-1 | checked:2026-06-10"
    - "Macroeconomics and Reality | 1980 | cited:12679 | doi:10.2307/1912017 | checked:2026-06-10"
  possible_innovation_points: GARCH+深度混合、宏观高维因子+VAR、结构突变检测、尾部风险/极端事件建模、可解释 ML 与传统时序对照; domain_scope=统计经济金融
  maturity: 经典  # 金融/宏观时序标准基线，任何新模型都应与之比较

- method_name: 分位数回归与异质效应建模 (Quantile Regression / Causal Forest)
  task_type: 条件分布建模、尾部/中位数效应估计、个体化/异质处理效应识别
  input_data: 结构化协变量、结果变量、处理变量(可选)、面板/横截面数据
  output_result: 不同分位点的条件效应、CATE/异质效应、分组政策建议
  core_assumption: 分位数回归直接建模条件分位数；因果森林通过局部随机森林估计条件处理效应并依赖识别假设
  advantages: 不只看均值；能发现尾部风险和群体差异；适合收入分布、金融风险、医疗个体化效果
  limitations: 分位点多重检验与交叉问题；CATE 易过拟合且解释需谨慎；因果结论仍依赖可交换/实验设计
  common_baselines: OLS/均值回归、GAM、随机森林、DML、分组回归、GBDT 分位数损失
  evaluation_metrics: pinball loss、覆盖率、CATE calibration、policy value、分组稳健性、置信区间覆盖
  suitable_datasets: 收入/工资分布、信用风险、医疗治疗效果、市场营销 uplift 数据
  implementation_repo: R quantreg/grf、Python statsmodels QuantReg、EconML/causalml、LightGBM quantile objective
  representative_papers:
    - "Regression Quantiles | 1978 | cited:12772 | doi:10.2307/1913643 | checked:2026-06-10"
    - "Generalized random forests | 2019 | cited:16 | doi:10.1214/18-aos1709 | checked:2026-06-10"
  possible_innovation_points: 公平性下的分布效应、尾部风险个体化预警、CATE 与机制解释结合、稳健分位数因果推断; domain_scope=统计经济金融
  maturity: 主流  # 分位数回归经典，因果森林是异质效应主流现代工具
```
