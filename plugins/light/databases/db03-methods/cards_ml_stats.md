# db03 方法卡 — 机器学习 / 统计学习

> schema: `method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`
> maturity: 经典 | 主流 | 新兴 | 过时 | 不推荐
> representative_papers 的 标题/年份/被引/DOI 均来自 OpenAlex `curl` 实测（2026-06 取数，&mailto 礼貌池）。被引数随时间增长，记录为取数当时快照。受版权全文不收录，仅元数据/链接。

```yaml
- method_name: "线性回归 / 逻辑回归 (Linear / Logistic Regression)"
  task_type: "回归(线性) / 二分类·多分类(逻辑)"
  input_data: "结构化数值/类别特征(需编码)"
  output_result: "连续值(线性) / 类别概率(逻辑)"
  core_assumption: "目标与特征线性可加；逻辑回归假设 log-odds 线性；误差独立同分布"
  advantages: "可解释(系数=效应)、训练快、概率输出校准好、统计推断成熟(置信区间/p值)、强基线"
  limitations: "仅线性边界、需手工交互/非线性项、对共线性与离群点敏感、高维需正则"
  common_baselines: "常数/均值预测、朴素贝叶斯"
  evaluation_metrics: "回归 RMSE/MAE/R²；分类 Acc/F1/AUC/LogLoss/校准曲线"
  suitable_datasets: "UCI 表格、医学/计量经济数据、低维可解释场景"
  implementation_repo: "scikit-learn (LinearRegression/LogisticRegression)、statsmodels、glmnet(R)"
  representative_papers:
    - "Logistic regression and artificial neural network classification models: a methodology review (2002, 被引 2175, DOI 10.1016/s1532-0464(03)00034-0)"
    - "A review of goodness of fit statistics for use in the development of logistic regression models (1982, 被引 1961, DOI 10.1093/oxfordjournals.aje.a113284)"
  possible_innovation_points: "L1/L2/弹性网正则与稀疏选择、广义可加模型(GAM)非线性化、与深度特征拼接做可解释 head、因果/工具变量扩展、概率校准; domain_scope=通用ML统计"
  maturity: "经典"
```

```yaml
- method_name: "随机森林 (Random Forest)"
  task_type: "表格分类/回归、特征重要性"
  input_data: "结构化特征(无需缩放/可含缺失)"
  output_result: "类别/数值 + 特征重要性(MDI/置换)"
  core_assumption: "bootstrap + 特征随机子采样建多棵去相关树，集成降方差"
  advantages: "稳健少调参、抗过拟合、可并行、内置 OOB 误差与重要性、小中数据友好"
  limitations: "大规模高维稀疏弱于 GBDT/深度、模型大、外推差、MDI 重要性对高基数特征有偏"
  common_baselines: "单决策树(CART)、逻辑回归、Bagging"
  evaluation_metrics: "Acc/F1/AUC、RMSE/MAE、OOB error"
  suitable_datasets: "UCI 表格、生信/遥感、中小样本结构化数据"
  implementation_repo: "scikit-learn (RandomForestClassifier/Regressor)、ranger(R)、randomForest(R)"
  representative_papers:
    - "Random Forests (Breiman, 2001, 被引 125032, DOI 10.1023/a:1010933404324)"
    - "Classification and Regression by randomForest (Liaw & Wiener, 2007, 被引 18407, 无 DOI)"
    - "Bias in random forest variable importance measures (2007, 被引 3595, DOI 10.1186/1471-2105-8-25)"
  possible_innovation_points: "无偏/条件特征重要性、与深度表征融合、概率校准、分位数回归森林做不确定性、面向漂移的在线森林、可解释规则提取; domain_scope=通用ML统计"
  maturity: "经典"

- method_name: "梯度提升决策树 (GBDT: XGBoost / LightGBM / CatBoost)"
  task_type: "表格分类/回归/排序(LTR)"
  input_data: "结构化特征(可含缺失；CatBoost 原生类别)"
  output_result: "类别概率/数值/排序分"
  core_assumption: "前向分步加法模型，按损失负梯度(残差)逐步拟合弱学习器"
  advantages: "表格任务常 SOTA、精度高、内置正则/缺失处理、特征重要性、竞赛常胜、工程成熟(GPU/分布式)"
  limitations: "超参多(学习率/深度/采样/正则)、对噪声与标签错误敏感、串行训练慢于 RF、外推差、需早停防过拟合"
  common_baselines: "随机森林、线性/逻辑回归、单树"
  evaluation_metrics: "AUC/F1/LogLoss、RMSE/MAE、NDCG/MAP(排序)"
  suitable_datasets: "Kaggle 表格赛、风控/广告 CTR、点击排序"
  implementation_repo: "xgboost(dmlc/xgboost)、LightGBM(microsoft/LightGBM)、catboost(catboost/catboost)、sklearn HistGradientBoosting"
  representative_papers:
    - "XGBoost: A Scalable Tree Boosting System (Chen & Guestrin, 2016, 被引 47898, DOI 10.1145/2939672.2939785)"
    - "Greedy function approximation: A gradient boosting machine (Friedman, 2001, 被引 28682, DOI 10.1214/aos/1013203451)"
    - "LightGBM: A Highly Efficient Gradient Boosting Decision Tree (Ke et al., 2017, 被引 9487, 无 DOI)"
    - "CatBoost: unbiased boosting with categorical features (Prokhorenkova et al., 2017, 被引 1125, DOI 10.48550/arxiv.1706.09516)"
  possible_innovation_points: "自动调参/NAS for boosting、不确定性输出(NGBoost 思路)、深度与 GBDT 融合(DeepGBM)、单调约束与可解释、对抗噪声鲁棒损失、GPU/联邦/差分隐私训练; domain_scope=通用ML统计"
  maturity: "主流"

- method_name: "支持向量机 (SVM / SVR)"
  task_type: "中小样本分类/回归、核方法"
  input_data: "数值特征(需标准化)，可经核函数升维"
  output_result: "类别(间隔决策) / 数值(SVR) / 决策分(需 Platt 校准成概率)"
  core_assumption: "最大化分类间隔；核技巧将非线性映射到高维线性可分"
  advantages: "高维小样本表现好、核函数灵活、有全局最优(凸优化)、泛化理论扎实(VC/间隔)"
  limitations: "大规模(n>1e5)训练慢(O(n²~n³))、核与 C/γ 调参敏感、概率非原生、多分类需 OvO/OvR"
  common_baselines: "逻辑回归、KNN、随机森林"
  evaluation_metrics: "Acc/F1/AUC、RMSE/MAE(SVR)"
  suitable_datasets: "文本/生信高维小样本、UCI 中小数据"
  implementation_repo: "scikit-learn (SVC/SVR, 基于 LIBSVM/LIBLINEAR)、LIBSVM、ThunderSVM(GPU)"
  representative_papers:
    - "Support-vector networks (Cortes & Vapnik, 1995, 被引 40372, DOI 10.1007/bf00994018)"
    - "LIBSVM: A library for support vector machines (Chang & Lin, 2011, 被引 41320, DOI 10.1145/1961189.1961199)"
  possible_innovation_points: "大规模近似核(随机特征/Nyström)、深度核学习、多核学习自动选核、不平衡代价敏感 SVM、与现代表征(预训练嵌入)级联做轻量分类头; domain_scope=通用ML统计"
  maturity: "主流"
```

```yaml
- method_name: "K 近邻 (KNN)"
  task_type: "分类/回归、相似检索基线"
  input_data: "数值特征(需标准化)，依赖距离度量"
  output_result: "邻居投票类别 / 邻居均值"
  core_assumption: "相似样本标签相似(局部平滑)，无显式训练(惰性学习)"
  advantages: "无训练、实现简单、天然多分类与非线性边界、可作强检索基线"
  limitations: "预测慢(需全量距离)、维度灾难、对尺度/噪声/不平衡敏感、需选 k 与度量、存储全量数据"
  common_baselines: "逻辑回归、SVM、决策树"
  evaluation_metrics: "Acc/F1/AUC、RMSE/MAE"
  suitable_datasets: "低维结构化、嵌入向量检索、UCI 小数据"
  implementation_repo: "scikit-learn (KNeighbors*)、FAISS/ScaNN/HNSWlib(大规模近邻)"
  representative_papers:
    - "Nearest neighbor pattern classification (Cover & Hart, 1967, 被引 16013, DOI 10.1109/tit.1967.1053964)"
  possible_innovation_points: "度量学习(Metric Learning)、近似最近邻加速(HNSW/IVF-PQ)、与深度嵌入结合做检索增强、自适应 k、面向不平衡的加权投票; domain_scope=通用ML统计"
  maturity: "经典"

- method_name: "朴素贝叶斯 (Naive Bayes)"
  task_type: "文本/类别特征分类、概率基线"
  input_data: "词频/TF-IDF、离散或高斯连续特征"
  output_result: "后验类别概率"
  core_assumption: "给定类别下特征条件独立；贝叶斯定理求后验"
  advantages: "极快、小样本可用、高维文本表现好、天然概率与增量更新、几乎无需调参"
  limitations: "条件独立假设强(概率常过自信)、特征相关时精度下降、连续特征需分布假设、零频需平滑"
  common_baselines: "逻辑回归、SVM(文本)"
  evaluation_metrics: "Acc/F1/AUC、LogLoss"
  suitable_datasets: "20Newsgroups、垃圾邮件/情感文本、Reuters"
  implementation_repo: "scikit-learn (MultinomialNB/GaussianNB/BernoulliNB/ComplementNB)"
  representative_papers:
    - "A comparison of event models for naive Bayes text classification (McCallum & Nigam, 1998, 被引 3226, 无 DOI)"
    - "Bayesian Network Classifiers (Friedman et al., 1997, 被引 4733, DOI 10.1023/a:1007465528199)"
  possible_innovation_points: "半朴素/TAN 放松独立、概率校准、与神经文本编码器融合、流式/概念漂移更新、贝叶斯网扩展依赖建模; domain_scope=通用ML统计"
  maturity: "经典"

- method_name: "聚类 (KMeans / DBSCAN / 层次聚类)"
  task_type: "无监督聚类、结构发现"
  input_data: "数值特征(KMeans 需标准化)、距离/密度"
  output_result: "簇标签 / 树状图(层次) / 噪声点(DBSCAN)"
  core_assumption: "KMeans 球形等方差簇(最小化簇内平方和)；DBSCAN 高密度连通区为簇；层次按距离逐步合并/分裂"
  advantages: "KMeans 快可扩展；DBSCAN 任意形状+识别噪声+无需指定簇数；层次给多粒度树状结构且无需预设 k"
  limitations: "KMeans 需指定 k、对初始化/离群敏感、仅凸簇；DBSCAN 对 eps/minPts 与变密度敏感；层次 O(n²~n³) 不易扩展"
  common_baselines: "随机划分、GMM、谱聚类"
  evaluation_metrics: "轮廓系数、CH/DB 指数、ARI/NMI(有标签时)、簇内平方和"
  suitable_datasets: "客户分群、空间数据(DBSCAN)、基因表达(层次)、UCI"
  implementation_repo: "scikit-learn (KMeans/DBSCAN/AgglomerativeClustering)、scipy.cluster.hierarchy、HDBSCAN(scikit-learn-contrib)"
  representative_papers:
    - "A density-based algorithm for discovering clusters in large spatial databases with noise (DBSCAN, Ester et al., 1996, 被引 19137, 无 DOI)"
    - "k-means++: the advantages of careful seeding (Arthur & Vassilvitskii, 2007, 被引 6302, DOI 10.5555/1283383.1283494)"
    - "Ward's Hierarchical Clustering Method (Murtagh & Legendre, 2011, 被引 1317, DOI 10.48550/arxiv.1111.6285)"
  possible_innovation_points: "深度聚类(联合表征学习)、自动选簇数、变密度 DBSCAN(HDBSCAN)、可扩展层次聚类、半监督/约束聚类、簇稳定性评估; domain_scope=通用ML统计"
  maturity: "经典"
```

```yaml
- method_name: "降维与可视化 (PCA / t-SNE / UMAP)"
  task_type: "线性降维(PCA)、非线性流形可视化(t-SNE/UMAP)"
  input_data: "高维数值特征/嵌入向量"
  output_result: "低维坐标(2~50 维)、主成分/嵌入"
  core_assumption: "PCA 数据主要方差在低维线性子空间；t-SNE/UMAP 保持局部邻域结构于低维流形"
  advantages: "PCA 快·可解释·可逆·去相关；t-SNE 簇可视化效果好；UMAP 比 t-SNE 快·保全局结构更好·支持新样本投影"
  limitations: "PCA 仅线性、对尺度敏感；t-SNE 慢·不保全局距离·超参(perplexity)敏感·不可解释轴·随机性；UMAP 超参(n_neighbors/min_dist)影响结构、距离不可直接定量解读"
  common_baselines: "随机投影、MDS、Isomap、自编码器"
  evaluation_metrics: "解释方差比(PCA)、邻域保持/trustworthiness、下游任务精度、KL 散度(t-SNE)"
  suitable_datasets: "单细胞 RNA-seq、MNIST/嵌入可视化、高维特征探索"
  implementation_repo: "scikit-learn (PCA/TSNE)、umap-learn(lmcinnes/umap)、openTSNE、Multicore-TSNE"
  representative_papers:
    - "Principal component analysis: a review and recent developments (Jolliffe & Cadima, 2016, 被引 9351, DOI 10.1098/rsta.2015.0202)"
    - "Visualizing Data using t-SNE (van der Maaten & Hinton, 2008, 被引 35730, 无 DOI)"
    - "UMAP: Uniform Manifold Approximation and Projection (McInnes et al., 2018, 被引 9493, DOI 10.21105/joss.00861)"
  possible_innovation_points: "监督/参数化 UMAP、稳定性与可重复性度量、densMAP 保密度、与对比学习表征结合、大规模 GPU 加速、可解释的非线性降维; domain_scope=通用ML统计"
  maturity: "PCA 经典；t-SNE 主流；UMAP 主流(新兴升级)"

- method_name: "高斯过程 (Gaussian Process, GP)"
  task_type: "回归(GPR)/分类(GPC)、贝叶斯优化代理、不确定性建模"
  input_data: "中小样本数值特征"
  output_result: "预测均值 + 校准的预测方差(不确定性)"
  core_assumption: "函数服从高斯过程先验，由核(协方差)函数刻画平滑性；后验仍为高斯"
  advantages: "原生不确定性量化、小样本强、核编码先验灵活、超参可由边际似然优化、贝叶斯优化首选代理模型"
  limitations: "标准 GP 训练 O(n³)·存储 O(n²) 难扩展、核选择敏感、高维与大数据需稀疏/近似、分类需近似推断"
  common_baselines: "核岭回归、随机森林、贝叶斯线性回归"
  evaluation_metrics: "RMSE/MAE、NLPD/负对数似然、覆盖率/校准、贝叶斯优化收敛曲线"
  suitable_datasets: "计算机实验/代理建模、时空回归、超参优化、材料/实验设计"
  implementation_repo: "GPyTorch(cornellius-gp)、GPflow、scikit-learn (GaussianProcessRegressor)、BoTorch(贝叶斯优化)"
  representative_papers:
    - "Gaussian Processes for Machine Learning (Rasmussen & Williams, MIT Press; OpenAlex 记录 被引 19637, DOI 10.7551/mitpress/3206.001.0001;书名字段在 OpenAlex 为空，标题以原书为准[待核查 OpenAlex 标题缺失])"
  possible_innovation_points: "稀疏变分 GP(SVGP)扩展大数据、深度核学习、多任务/多保真 GP、可扩展精确 GP(GPyTorch KeOps)、与神经网络融合的不确定性建模、批量贝叶斯优化; domain_scope=通用ML统计"
  maturity: "主流"

- method_name: "隐马尔可夫模型 (Hidden Markov Model, HMM)"
  task_type: "序列标注/分割、时序建模、生物序列分析"
  input_data: "离散/连续观测序列"
  output_result: "隐状态序列(Viterbi)、序列似然、状态后验"
  core_assumption: "一阶马尔可夫隐状态链 + 观测仅依赖当前隐状态(输出独立)"
  advantages: "概率可解释、训练(Baum-Welch/EM)与解码(Viterbi)算法成熟高效、小数据可用、生成式可处理缺失"
  limitations: "马尔可夫与输出独立假设强、长程依赖弱、状态数需预设、已被 RNN/CRF/Transformer 在多数序列任务超越"
  common_baselines: "CRF、RNN/LSTM、n-gram"
  evaluation_metrics: "序列对数似然、标注 F1/Acc、困惑度"
  suitable_datasets: "语音/音素、基因序列(profile HMM)、词性标注、金融状态切换"
  implementation_repo: "hmmlearn、pomegranate、HMMER(生物序列)"
  representative_papers:
    - "A tutorial on hidden Markov models and selected applications in speech recognition (Rabiner, 1989, 被引 22755, DOI 10.1109/5.18626)"
    - "Accelerated Profile HMM Searches (Eddy, 2011, 被引 7426, DOI 10.1371/journal.pcbi.1002195)"
  possible_innovation_points: "神经-HMM 混合(可微 HMM)、半马尔可夫/分层状态、贝叶斯非参(HDP-HMM)自动定状态数、与深度发射模型结合、可解释状态切换分析; domain_scope=通用ML统计"
  maturity: "经典(多数任务过时，特定领域如生信仍主流)"
```

```yaml
- method_name: "集成学习 (Ensemble: Bagging / Boosting / Stacking / Voting)"
  task_type: "分类/回归(提升任意基学习器)"
  input_data: "任意(取决于基学习器)"
  output_result: "多模型聚合的类别/数值/概率"
  core_assumption: "多个弱/不完美模型的合理聚合优于单模型(Bagging 降方差、Boosting 降偏差、Stacking 学习元组合)"
  advantages: "通用涨点、降方差/偏差、鲁棒、Stacking 可融合异质模型、竞赛 SOTA 常用"
  limitations: "计算/存储成本高、可解释性下降、Boosting 对噪声敏感、Stacking 易过拟合需交叉验证、调参与流程复杂"
  common_baselines: "单一基学习器、简单平均"
  evaluation_metrics: "Acc/F1/AUC、RMSE/MAE、与单模型增益对比"
  suitable_datasets: "Kaggle 表格/CV 赛、风控、任意监督任务"
  implementation_repo: "scikit-learn (Bagging/AdaBoost/Voting/StackingClassifier)、xgboost/lightgbm(Boosting)、mlxtend"
  representative_papers:
    - "Bagging predictors (Breiman, 1996, 被引 16356, DOI 10.1007/bf00058655)"
    - "A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting (AdaBoost, Freund & Schapire, 1997, 被引 20251, DOI 10.1006/jcss.1997.1504)"
    - "Issues in Stacked Generalization (Ting & Witten, 1999, 被引 550, DOI 10.1613/jair.594)"
  possible_innovation_points: "异质深度+树模型 Stacking、动态/自适应集成选择、不确定性感知加权、知识蒸馏压缩集成、自动化集成搜索(AutoML)、面向漂移的在线集成; domain_scope=通用ML统计"
  maturity: "经典(方法论)/主流(实践)"

- method_name: "贝叶斯方法 (Bayesian Inference: MCMC / 变分推断 / 贝叶斯神经网络)"
  task_type: "概率建模、参数后验估计、不确定性量化、分层建模"
  input_data: "观测数据 + 先验"
  output_result: "参数/预测的后验分布、可信区间、模型证据"
  core_assumption: "参数为随机变量，由先验与似然经贝叶斯定理得后验；预测对后验积分(边缘化)"
  advantages: "原生不确定性、自然融合先验/领域知识、分层建模处理嵌套数据、小样本稳健、模型比较(证据/WAIC)"
  limitations: "计算昂贵(MCMC 慢/VI 近似有偏)、先验选择主观、收敛诊断难、高维与大数据扩展受限、BNN 仍不及确定性网精度"
  common_baselines: "最大似然/MAP 点估计、自助法、频率派区间"
  evaluation_metrics: "后验预测检验、WAIC/LOO-CV、ELBO(VI)、收敛诊断(R̂/ESS)、校准/覆盖率"
  suitable_datasets: "分层/纵向数据、小样本科研数据、A/B 测试、流行病学"
  implementation_repo: "PyMC、Stan(cmdstanpy)、NumPyro/Pyro、TensorFlow Probability"
  representative_papers:
    - "Variational Inference: A Review for Statisticians (Blei et al., 2017, 被引 3697, DOI 10.1080/01621459.2017.1285773)"
  possible_innovation_points: "可扩展 VI(随机/分摊推断)、归一化流增强后验近似、贝叶斯深度学习不确定性校准、模拟基推断(SBI)、先验敏感性自动分析、概率编程加速(GPU/JIT); domain_scope=通用ML统计"
  maturity: "经典(统计)/主流(概率编程)/新兴(贝叶斯深度学习)"
```

## 取数与诚实说明
- 所有 representative_papers 的 标题/年份/被引/DOI 来自 OpenAlex API 实测 `curl`（`api.openalex.org/works`，&mailto 礼貌池，2026-06 取数快照）；被引数随时间增长。
- 部分经典论文 OpenAlex 无 DOI（如 DBSCAN KDD'96、t-SNE JMLR、McCallum&Nigam NB、Liaw&Wiener randomForest），已如实标注"无 DOI"。
- Gaussian Processes for Machine Learning 一书在 OpenAlex 的 title 字段为空（DOI 10.7551/mitpress/3206.001.0001，被引 19637），书名以原书为准，标记 [待核查 OpenAlex 标题缺失]。
- maturity / 是否过时 为依据方法学共识的判断，非 API 数值。implementation_repo 为业界真实主流开源库（scikit-learn / xgboost / LightGBM / catboost / GPyTorch / PyMC 等）。
