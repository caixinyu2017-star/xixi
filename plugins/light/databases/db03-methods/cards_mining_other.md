# db03 方法卡 — 数据挖掘 / 图 / 时序 / 推荐 / 优化

> 续作扩充卡集，schema 与 [method_cards.md](method_cards.md) 一致。`maturity`: 经典|主流|新兴|过时|不推荐。
> 受版权全文不收录，仅元数据与开源链接。representative_papers 的标题/年份/被引/DOI 均来自 OpenAlex 真实 curl 结果（2026-06 取数，含 &mailto 礼貌池）；被引数随时间增长，标注为取数时刻快照。
> 分区/CCF/影响因子等本卡未涉及（方法卡不绑定单一刊物）；如需会议等级见 db04。

## 关联规则挖掘

```yaml
- method_name: Apriori
  task_type: 频繁项集挖掘 / 关联规则
  input_data: 事务数据库(购物篮/事件序列)
  output_result: 频繁项集 + 关联规则(support/confidence/lift)
  core_assumption: 反单调性(Apriori 性质)——非频繁项集的超集必非频繁
  advantages: 原理简单可解释、规则直观、工业落地早(购物篮分析)
  limitations: 多次扫描数据库、候选集爆炸、大数据/低支持度阈值下极慢
  common_baselines: 暴力枚举、Eclat
  evaluation_metrics: support / confidence / lift / 规则数 / 运行时间
  suitable_datasets: UCI Retail、Online Retail、Instacart 购物篮
  implementation_repo: mlxtend (frequent_patterns)、Spark MLlib FPGrowth(对照)
  representative_papers: >
    Fast Algorithms for Mining Association Rules in Large Databases
    (Agrawal & Srikant, 1994, OpenAlex 被引≈9385);
    Fast algorithms for mining association rules (1998, 被引≈10755)
  possible_innovation_points: 与图/序列模式结合、增量/流式挖掘、隐私保护关联规则、稀有但高价值规则的兴趣度度量; domain_scope=数据挖掘
  maturity: 经典

- method_name: FP-Growth
  task_type: 频繁项集挖掘
  input_data: 事务数据库
  output_result: 频繁项集(经 FP-tree 压缩)
  core_assumption: 用前缀树(FP-tree)压缩事务，分治递归避免候选生成
  advantages: 无候选生成、只需两次扫库、典型快于 Apriori 一个量级、可分布式(Spark)
  limitations: FP-tree 内存占用大、稠密/长事务下树膨胀、实现较复杂
  common_baselines: Apriori、Eclat
  evaluation_metrics: 运行时间 / 内存 / support / 规则质量
  suitable_datasets: 同 Apriori，规模更大场景
  implementation_repo: mlxtend、Spark MLlib FPGrowth
  representative_papers: >
    Mining frequent patterns without candidate generation
    (Han, Pei & Yin, 2000, DOI 10.1145/335191.335372, OpenAlex 被引≈6348);
    期刊扩展版 FP-tree Approach (2003, DOI 10.1023/b:dami.0000005258.31418.83)
  possible_innovation_points: 流式/增量 FP、GPU 并行、与序列/图模式融合、高效近似挖掘; domain_scope=数据挖掘
  maturity: 经典
```

## 时间序列预测

```yaml
- method_name: ARIMA / SARIMA (Box-Jenkins)
  task_type: 单变量时序预测
  input_data: 平稳化后的单序列(可季节差分)
  output_result: 点预测 + 置信区间
  core_assumption: 序列(经差分后)平稳，未来由历史线性自回归+移动平均刻画
  advantages: 统计基础扎实、可解释(AR/I/MA 阶数)、小样本可用、给出置信区间
  limitations: 仅线性、需平稳化与定阶、不擅长多变量/非线性/长程、多序列扩展差
  common_baselines: 朴素/季节朴素、指数平滑(ETS)、Theta
  evaluation_metrics: MAE / RMSE / MAPE / sMAPE / MASE
  suitable_datasets: M3/M4 竞赛、电力负荷、零售销量
  implementation_repo: statsmodels、pmdarima(auto_arima)
  representative_papers: >
    Box & Jenkins, Time Series Analysis: Forecasting and Control(经典专著,
    OpenAlex 收录多版本如 2013 DOI 10.1057/9781137291264_6)
  possible_innovation_points: 自动定阶+深度残差混合、与外生变量(ARIMAX)结合、分层预测; domain_scope=数据挖掘
  maturity: 经典

- method_name: Prophet
  task_type: 业务单变量时序预测(带季节/节假日)
  input_data: 含时间戳的序列 + 节假日/事件回归项
  output_result: 趋势+季节+节假日分解的预测 + 不确定性区间
  core_assumption: 时序可加性分解为趋势(分段线性/logistic)+周期(傅里叶)+节假日+噪声
  advantages: 易用、对缺失/异常稳健、可解释分解、分析师可手调、自动季节性
  limitations: 本质曲线拟合非真正动态模型、多变量/高频/长程弱、对快速变化反应慢
  common_baselines: ARIMA、ETS、朴素季节
  evaluation_metrics: MAE / RMSE / MAPE / 覆盖率(区间)
  suitable_datasets: 业务日/周销量、网站流量、容量规划
  implementation_repo: facebook/prophet (Python/R)
  representative_papers: >
    Forecasting at Scale (Taylor & Letham, 2017,
    DOI 10.1080/00031305.2017.1380080, OpenAlex 被引≈2256)
  possible_innovation_points: 与深度/梯度提升残差融合、多序列层级协调、外生变量自动选择; domain_scope=数据挖掘
  maturity: 主流

- method_name: LSTM(时序预测)
  task_type: 单/多变量时序预测、序列回归
  input_data: 滑窗序列张量(样本×时间步×特征)
  output_result: 多步/单步预测
  core_assumption: 门控记忆单元可学习长程时间依赖
  advantages: 建模非线性与长程依赖、支持多变量、可端到端
  limitations: 需较多数据、训练慢、长序列仍受限、解释性差、常被 Transformer/简单线性超越
  common_baselines: ARIMA、GRU、TCN、DLinear
  evaluation_metrics: MAE / RMSE / MAPE / MASE
  suitable_datasets: 电力(ETT)、交通(PEMS)、气象、金融
  implementation_repo: PyTorch、Keras、GluonTS、Darts
  representative_papers: >
    Long Short-Term Memory (Hochreiter & Schmidhuber, 1997,
    DOI 10.1162/neco.1997.9.8.1735, OpenAlex 被引≈97420)
  possible_innovation_points: 注意力增强、与分解结合、概率预测、迁移/少样本时序; domain_scope=数据挖掘
  maturity: 主流(在长序列预测中部分被 Transformer/线性模型替代)

- method_name: Transformer(时序预测, 如 Informer)
  task_type: 长序列时序预测(LSTF)
  input_data: 长滑窗多变量序列
  output_result: 长程多步预测
  core_assumption: 自注意力捕获长程依赖；稀疏注意力降低 O(L^2) 复杂度
  advantages: 长程依赖、并行、长输出一次性预测(生成式解码)
  limitations: 算力/显存大、调参敏感；DLinear 等简单基线质疑其必要性
  common_baselines: LSTM、TCN、DLinear、Autoformer/FEDformer
  evaluation_metrics: MAE / MSE / RMSE
  suitable_datasets: ETT、Electricity、Weather、Traffic
  implementation_repo: zhouhaoyi/Informer2020、thuml/Time-Series-Library
  representative_papers: >
    Informer: Beyond Efficient Transformer for Long Sequence Time-Series
    Forecasting (Zhou et al., AAAI 2021, DOI 10.1609/aaai.v35i12.17325,
    被引≈5981); 反方观点 Are Transformers Effective for Time Series
    Forecasting? (DLinear, AAAI 2023, DOI 10.1609/aaai.v37i9.26317, 被引≈2556)
  possible_innovation_points: 频域/分解注意力、线性复杂度、与简单基线公平对比、基础模型(TimesFM/通用时序大模型); domain_scope=数据挖掘
  maturity: 新兴/主流
```

## 异常检测

```yaml
- method_name: Isolation Forest
  task_type: 无监督异常检测
  input_data: 数值/混合特征表格
  output_result: 异常分数(路径长度) / 异常标签
  core_assumption: 异常点更易被随机切分孤立，平均路径更短
  advantages: 线性时间、低内存、无需密度/距离假设、高维较稳健、少调参
  limitations: 轴平行切分对局部/相关异常弱、分数阈值需定、对类别特征需编码
  common_baselines: One-Class SVM、LOF、Elliptic Envelope
  evaluation_metrics: ROC-AUC / PR-AUC / F1 / Precision@k
  suitable_datasets: KDD99/NSL-KDD、信用卡欺诈、ODDS 基准
  implementation_repo: scikit-learn IsolationForest、PyOD
  representative_papers: >
    Isolation Forest (Liu, Ting & Zhou, ICDM 2008,
    DOI 10.1109/icdm.2008.17, OpenAlex 被引≈5528);
    Extended Isolation Forest (2019, DOI 10.1109/tkde.2019.2947676);
    Deep Isolation Forest (2023, DOI 10.1109/tkde.2023.3270293)
  possible_innovation_points: 非轴平行切分、深度表示+孤立、流式/概念漂移、可解释异常归因; domain_scope=数据挖掘
  maturity: 主流

- method_name: LOF (Local Outlier Factor)
  task_type: 无监督异常检测(局部密度)
  input_data: 数值特征(需定义距离)
  output_result: 局部离群因子(>1 越异常)
  core_assumption: 异常点的局部密度显著低于其近邻
  advantages: 检测局部/簇内密度异常、给出连续程度分、原理直观
  limitations: O(n^2) 近邻计算、对 k 与距离敏感、维度灾难、不适合超大数据
  common_baselines: kNN 距离、Isolation Forest、One-Class SVM
  evaluation_metrics: ROC-AUC / PR-AUC / Precision@k
  suitable_datasets: ODDS、网络入侵、传感器异常
  implementation_repo: scikit-learn LocalOutlierFactor、PyOD
  representative_papers: >
    LOF: Identifying Density-Based Local Outliers (Breunig et al.,
    SIGMOD 2000, DOI 10.1145/342009.335388, OpenAlex 被引≈3836)
  possible_innovation_points: 近似/索引加速、流式 LOF、子空间局部异常、与深度嵌入结合; domain_scope=数据挖掘
  maturity: 经典

- method_name: AutoEncoder(重构式异常检测)
  task_type: 无监督/半监督异常检测
  input_data: 高维向量/图像/时序(以正常样本为主训练)
  output_result: 重构误差作为异常分数
  core_assumption: 模型仅学到正常数据流形，异常样本重构误差大
  advantages: 处理高维非线性、可端到端、变体多(VAE/去噪/卷积/LSTM-AE)
  limitations: 需足量"干净"正常数据、阈值难定、可能过度泛化重构出异常、训练成本
  common_baselines: PCA 重构、Isolation Forest、One-Class SVM、DAGMM
  evaluation_metrics: ROC-AUC / PR-AUC / F1 / 重构误差分布
  suitable_datasets: MNIST/CIFAR(图像异常)、SWaT/SMD(时序)、网络流量
  implementation_repo: PyOD、PyTorch 自建、DAGMM 实现
  representative_papers: >
    Deep Autoencoding Gaussian Mixture Model for Unsupervised Anomaly
    Detection (Zong et al., ICLR 2018, OpenAlex 被引≈1091)
  possible_innovation_points: 记忆模块抑制泛化、对抗/扩散重构、时序-图联合、置信度校准阈值; domain_scope=数据挖掘
  maturity: 主流
```

## 推荐系统

```yaml
- method_name: 协同过滤(基于物品 ItemCF)
  task_type: Top-N 推荐 / 评分预测
  input_data: 用户-物品交互(评分/点击)矩阵
  output_result: 物品相似度 + 个性化推荐列表
  core_assumption: 用户会喜欢与其历史交互物品相似的物品(行为相似)
  advantages: 实现简单可解释、物品相似度可离线预计算、工业部署久经验证
  limitations: 冷启动、稀疏性、长尾覆盖差、相似度计算随规模膨胀、无内容/上下文
  common_baselines: UserCF、流行度、矩阵分解
  evaluation_metrics: Recall@K / NDCG@K / HitRate / MAP / 覆盖率
  suitable_datasets: MovieLens、Amazon Reviews、Netflix
  implementation_repo: implicit、Surprise、Spark MLlib
  representative_papers: >
    Item-based collaborative filtering recommendation algorithms
    (Sarwar et al., WWW 2001, DOI 10.1145/371920.372071, OpenAlex 被引≈9005)
  possible_innovation_points: 与图/序列融合、相似度可学习、冷启动内容补全、去偏(流行度偏差); domain_scope=数据挖掘
  maturity: 经典

- method_name: 矩阵分解(MF / SVD / ALS)
  task_type: 评分预测 / 隐式反馈推荐
  input_data: 用户-物品交互矩阵
  output_result: 用户/物品隐向量 + 预测评分/排序
  core_assumption: 交互矩阵低秩，可由用户与物品隐因子内积近似
  advantages: 缓解稀疏、隐因子泛化好、可加偏置/正则/隐式反馈(BPR/ALS)、可扩展
  limitations: 冷启动、仅线性内积、难融合上下文/内容、需重训应对新数据
  common_baselines: ItemCF、流行度、FM
  evaluation_metrics: RMSE(评分) / Recall@K / NDCG@K / AUC
  suitable_datasets: MovieLens、Netflix Prize、Amazon
  implementation_repo: implicit(ALS)、LightFM、Surprise
  representative_papers: >
    Matrix Factorization Techniques for Recommender Systems
    (Koren, Bell & Volinsky, IEEE Computer 2009,
    DOI 10.1109/mc.2009.263, OpenAlex 被引≈11640)
  possible_innovation_points: 神经矩阵分解、贝叶斯/概率 MF、加边信息(图正则)、去偏与公平; domain_scope=数据挖掘
  maturity: 经典

- method_name: DeepFM
  task_type: CTR 预估 / 排序
  input_data: 高维稀疏类别特征(one-hot/ID) + 数值特征
  output_result: 点击/转化概率
  core_assumption: 同时建模低阶(FM 二阶交叉)与高阶(DNN)特征交互，共享嵌入
  advantages: 无需手工特征工程、端到端、低高阶交互兼顾、工业 CTR 常用
  limitations: 仅隐式交互、对超大规模特征需工程优化、可解释性有限、易过拟合
  common_baselines: LR、FM、Wide&Deep、xDeepFM、DCN
  evaluation_metrics: AUC / LogLoss / GAUC
  suitable_datasets: Criteo、Avazu、MovieLens(CTR 化)
  implementation_repo: shenweichen/DeepCTR、FuxiCTR
  representative_papers: >
    DeepFM: A Factorization-Machine based Neural Network for CTR Prediction
    (Guo et al., IJCAI 2017, DOI 10.24963/ijcai.2017/239, OpenAlex 被引≈2234)
  possible_innovation_points: 显式高阶交叉(DCN-V2)、特征重要性自适应(FiBiNET/AutoInt)、多任务/多场景共享; domain_scope=数据挖掘
  maturity: 主流

- method_name: 双塔模型(Two-Tower / DSSM 式召回)
  task_type: 大规模召回 / 向量检索推荐
  input_data: 用户侧特征塔 + 物品侧特征塔
  output_result: 用户/物品共享空间嵌入 + 内积相似度
  core_assumption: 用户与物品可映射到同一向量空间，相关性≈内积，物品向量可离线索引
  advantages: 物品嵌入离线建库、在线 ANN 毫秒级召回、可扩展到亿级、支持多特征
  limitations: 用户物品塔晚交互(信息瓶颈)、采样偏差需校正、负样本策略关键
  common_baselines: ItemCF、MF、YouTube DNN
  evaluation_metrics: Recall@K / 召回命中率 / HitRate / 线上 CTR
  suitable_datasets: 工业日志(MovieLens/Amazon 可模拟)、点击流
  implementation_repo: TensorFlow Recommenders、faiss(ANN)
  representative_papers: >
    Sampling-bias-corrected neural modeling for large corpus item
    recommendations (Yi et al., RecSys 2019, DOI 10.1145/3298689.3346996,
    OpenAlex 被引≈209); 相关 Deep Neural Networks for YouTube Recommendations
    (2016, DOI 10.1145/2959100.2959190, 被引≈3351)
  possible_innovation_points: 细粒度晚交互(ColBERT 式)、对比学习负采样、多兴趣用户塔、对齐召回-精排; domain_scope=数据挖掘
  maturity: 主流
```

## 图分析

```yaml
- method_name: 链接预测(经典指标 + GNN)
  task_type: 图中缺失/未来边预测
  input_data: 图(节点+已知边，可含属性)
  output_result: 节点对成边概率/排序
  core_assumption: 结构邻近(共同邻居/路径)或可学习表示蕴含连边倾向
  advantages: 经典指标(CN/AA/RA/Katz)无需训练、可解释；GNN(SEAL)可学子图结构，精度高
  limitations: 经典指标表达力弱；GNN 计算重、负采样与评测易乐观、稀疏图困难
  common_baselines: Common Neighbors、Adamic-Adar、Katz、node2vec、GAE
  evaluation_metrics: AUC / AP / Hits@K / MRR
  suitable_datasets: ogbl-collab/ddi/citation2、Cora/Citeseer、社交网络
  implementation_repo: PyG(SEAL/GAE)、DGL、networkx(经典指标)
  representative_papers: >
    The link-prediction problem for social networks (Liben-Nowell &
    Kleinberg, 2003/2007, DOI 10.1002/asi.20591, OpenAlex 被引≈3022);
    Link Prediction Based on Graph Neural Networks (SEAL, Zhang & Chen,
    NeurIPS 2018, arXiv DOI 10.48550/arxiv.1802.09691)
  possible_innovation_points: 子图/路径感知 GNN、时序动态链接预测、异质图链接、可扩展负采样与无偏评测; domain_scope=数据挖掘
  maturity: 主流

- method_name: 社区发现(Louvain / Leiden)
  task_type: 图聚类 / 社区检测
  input_data: (加权)图
  output_result: 节点社区划分(层级)
  core_assumption: 好的社区划分使模块度(modularity)最大化
  advantages: 近线性、可处理百万级图、层级结构、无需预设社区数、应用广
  limitations: 模块度分辨率极限(吞并小社区)、Louvain 可能产生不连通社区(Leiden 修复)、非确定性
  common_baselines: 谱聚类、Infomap、标签传播、Leiden
  evaluation_metrics: Modularity / NMI / ARI / 电导
  suitable_datasets: SNAP 社交网络、引文网、生物网络
  implementation_repo: python-louvain、leidenalg、networkx、igraph
  representative_papers: >
    Fast unfolding of communities in large networks (Blondel et al., 2008,
    DOI 10.1088/1742-5468/2008/10/p10008, OpenAlex 被引≈21129);
    From Louvain to Leiden (Traag et al., 2019,
    DOI 10.1038/s41598-019-41695-z, 被引≈5121)
  possible_innovation_points: 属性/多层图社区、动态社区演化、GNN+模块度联合、重叠社区; domain_scope=数据挖掘
  maturity: 经典(Leiden 为推荐升级版)

- method_name: 知识图谱嵌入 TransE
  task_type: 知识图谱补全 / 链接预测
  input_data: 三元组(头实体, 关系, 尾实体)
  output_result: 实体/关系低维向量 + 三元组打分
  core_assumption: 关系是实体间的平移，h + r ≈ t
  advantages: 参数少、训练快、可扩展、几何直观、强基线
  limitations: 难表达 1-N/N-1/N-N 与对称/自反关系、表达力受限
  common_baselines: TransH/TransR、DistMult、ComplEx、RotatE
  evaluation_metrics: MRR / MR / Hits@1/3/10
  suitable_datasets: FB15k-237、WN18RR、YAGO3-10
  implementation_repo: OpenKE、PyKEEN、DGL-KE
  representative_papers: >
    Translating Embeddings for Modeling Multi-relational Data
    (Bordes et al., NeurIPS 2013; OpenAlex 收录版被引≈5199);
    后续 TransH (Wang et al., AAAI 2014, DOI 10.1609/aaai.v28i1.8870)
  possible_innovation_points: 复杂关系建模(旋转/双曲)、时序 KG 嵌入、规则+嵌入融合、与 LLM 联合补全; domain_scope=数据挖掘
  maturity: 经典(基线常用，研究主线已转向 RotatE/复数及 GNN 类)
```

## 优化 / 联邦学习

```yaml
- method_name: 多目标优化 NSGA-II
  task_type: 多目标进化优化(求 Pareto 前沿)
  input_data: 决策变量空间 + 多个(冲突)目标函数 + 约束
  output_result: 非支配解集(Pareto 近似前沿)
  core_assumption: 通过非支配排序+拥挤度保持多样性，精英保留逼近 Pareto 前沿
  advantages: 无需目标可微、保前沿多样性、精英保留收敛好、工程应用极广、强基线
  limitations: 目标数>3(多目标→超多目标)退化、评估开销大、收敛慢、需调种群/代数
  common_baselines: SPEA2、加权和、ε-约束、MOEA/D、NSGA-III
  evaluation_metrics: Hypervolume / IGD / GD / Spread / 收敛性
  suitable_datasets: ZDT/DTLZ/WFG 测试集、工程设计基准
  implementation_repo: pymoo、DEAP、Platypus、jMetal
  representative_papers: >
    A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II
    (Deb et al., IEEE TEVC 2002, DOI 10.1109/4235.996017, OpenAlex 被引≈47464)
  possible_innovation_points: 超多目标(NSGA-III/参考点)、代理模型加速(贝叶斯/Kriging)、与梯度/学习混合、约束处理; domain_scope=数据挖掘
  maturity: 经典

- method_name: 联邦学习(FedAvg)
  task_type: 分布式隐私保护协同训练
  input_data: 多客户端本地私有数据(不出本地)
  output_result: 全局共享模型
  core_assumption: 客户端本地多轮更新后聚合参数，可近似集中训练而无需汇集原始数据
  advantages: 数据不出域(隐私/合规)、通信高效(本地多步)、利用分散数据、跨机构协作
  limitations: 非独立同分布(Non-IID)掉点、系统异构掉队者、通信瓶颈、易受投毒/推断攻击、需加密增强
  common_baselines: 集中训练(上界)、本地单独训练、FedProx、SCAFFOLD
  evaluation_metrics: 全局精度 / 通信轮数 / 收敛速度 / 公平性 / 隐私预算(ε)
  suitable_datasets: FEMNIST、Shakespeare、LEAF 基准、CIFAR Non-IID 划分
  implementation_repo: TensorFlow Federated、Flower、FedML、PySyft
  representative_papers: >
    Communication-Efficient Learning of Deep Networks from Decentralized
    Data (FedAvg, McMahan et al., AISTATS 2017;
    arXiv DOI 10.48550/arxiv.1602.05629, OpenAlex 被引≈5178)
  possible_innovation_points: Non-IID 鲁棒聚合、个性化联邦、差分隐私/安全聚合、通信压缩、抗投毒; domain_scope=数据挖掘
  maturity: 新兴/主流
```

## 待补充
按用户领域扩充更多方法卡，定期复核 maturity 与 representative_papers 被引快照。
