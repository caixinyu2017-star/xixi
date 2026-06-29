# db03 方法卡 — 生物医学（cards_biomedical.md）

> 每张卡注明 maturity（经典|主流|新兴|过时|不推荐），避免提出落后方案。受版权全文不收录，仅元数据与开源链接。
> representative_papers 的标题/年份/被引/DOI 来自 OpenAlex 真实 curl 结果（https://api.openalex.org，mailto 礼貌池），查询日期 **2026-06-09**；被引数随时间变动。
> 排名/成熟度判断为人工标注。查不到的字段写「待核查」。

字段 schema 同 db03：`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`

## 方法卡

```yaml
- method_name: Cox 比例风险模型 / Kaplan-Meier 生存分析
  task_type: 生存分析(time-to-event,删失数据的风险/生存概率建模)
  input_data: 个体协变量 + 随访时间 + 事件/删失指示(right-censored)
  output_result: 风险比(HR)及置信区间、基线风险、生存曲线 S(t)
  core_assumption: Cox 假设各协变量的风险比不随时间变化(比例风险 PH);KM 为非参数,无分布假设
  advantages: 半参数无需指定基线分布;天然处理右删失;HR 临床可解释;KM 直观展示分组生存差异
  limitations: PH 假设易被违反(需 Schoenfeld 残差检验);难捕捉时变效应/非线性;高维需正则化(Lasso-Cox);竞争风险需 Fine-Gray
  common_baselines: Kaplan-Meier + log-rank、参数模型(Weibull/AFT)、随机生存森林、DeepSurv
  evaluation_metrics: C-index(Harrell/Uno)、time-dependent AUC、Brier score、校准曲线
  suitable_datasets: TCGA(生存终点)、MIMIC-IV、UK Biobank、SEER
  implementation_repo: R survival/survminer、Python lifelines、scikit-survival
  representative_papers:
    - "Regression Models and Life-Tables | 1972 | cited:39192 | doi:10.1111/j.2517-6161.1972.tb00899.x | checked:2026-06-09"
    - "Nonparametric Estimation from Incomplete Observations (Kaplan-Meier) | 1958 | cited:39006 | doi:10.1080/01621459.1958.10501452 | checked:2026-06-09"
  possible_innovation_points: 深度生存(DeepSurv/DeepHit)与可解释性结合、时变协变量建模、竞争风险下的多终点联合、多组学+影像融合预后; domain_scope=生物医学
  maturity: 经典  # 1958/1972 奠基,至今临床预后/流行病学标准方法,统计严谨且强制要求,不会过时

- method_name: U-Net / nnU-Net 医学影像分割
  task_type: 医学图像语义分割(器官/病灶,2D/3D)
  input_data: CT/MRI/超声/病理等影像(常为体素 volume)
  output_result: 逐像素/体素分割掩膜(可多类)
  core_assumption: 编码器-解码器 + 跳跃连接可同时保留全局语义与局部细节;nnU-Net 假设可由数据指纹自动推断最优配置
  advantages: 小样本表现强(医学数据稀缺友好);跳跃连接保边界;nnU-Net 自动配置预处理/网络/训练,免手调即达多任务 SOTA
  limitations: 纯 CNN 感受野有限(长程依赖弱);3D 显存开销大;对域偏移(扫描仪/协议差异)敏感;标注成本高
  common_baselines: FCN、V-Net、Attention U-Net、TransUNet、Swin-UNet、SAM/MedSAM
  evaluation_metrics: Dice(DSC)、IoU、Hausdorff 距离(HD95)、ASSD、敏感度/特异度
  suitable_datasets: Medical Segmentation Decathlon、BraTS、KiTS、ACDC
  implementation_repo: MIC-DKFZ/nnUNet、官方 U-Net、MONAI
  representative_papers:
    - "U-Net: Convolutional Networks for Biomedical Image Segmentation | 2015 | cited:88543 | doi:10.1007/978-3-319-24574-4_28 | checked:2026-06-09"
    - "nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation | 2020 | cited:8409 | doi:10.1038/s41592-020-01008-z | checked:2026-06-09"
  possible_innovation_points: Transformer/Mamba 混合架构、基础模型(SAM)零样本/少样本适配、半监督与领域泛化、不确定性估计辅助临床; domain_scope=生物医学
  maturity: 主流  # U-Net 经典骨干,nnU-Net 仍是分割竞赛强基线/事实标准,2020 后持续被超越但难被取代

- method_name: GWAS 全基因组关联分析
  task_type: 基因型-表型关联检验(变异位点与性状/疾病的统计关联)
  input_data: 个体 SNP 基因型(芯片/测序)+ 表型 + 协变量(年龄/性别/主成分)
  output_result: 各 SNP 的效应量(beta/OR)与 p 值(曼哈顿图、QQ 图、显著位点)
  core_assumption: 常见变异-常见病假设;线性/逻辑回归下加性遗传效应;群体分层可由 PCA/混合模型校正
  advantages: 无假设全基因组扫描;成熟显著性阈值(5e-8);可做多基因风险评分(PRS)与孟德尔随机化下游
  limitations: 需极大样本;群体分层与亲缘关系导致假阳性;连锁不平衡使因果位点难定位;缺失遗传率;跨族裔迁移差
  common_baselines: 线性/逻辑回归(PLINK)、混合线性模型(BOLT-LMM/GCTA)、SAIGE(罕见病/不平衡)
  evaluation_metrics: 全基因组显著性 p<5e-8、基因组膨胀因子 λ_GC、LD score 回归、PRS 的 AUC/R²
  suitable_datasets: UK Biobank、1000 Genomes(参考/imputation)、FinnGen
  implementation_repo: PLINK 1.9/2.0、BOLT-LMM、SAIGE、REGENIE
  representative_papers:
    - "PLINK: A Tool Set for Whole-Genome Association and Population-Based Linkage Analyses | 2007 | cited:36013 | doi:10.1086/519795 | checked:2026-06-09"
    - "10 Years of GWAS Discovery: Biology, Function, and Translation | 2017 | cited:4048 | doi:10.1016/j.ajhg.2017.06.005 | checked:2026-06-09"
  possible_innovation_points: 跨族裔/多祖先 PRS 可迁移性、罕见变异负荷检验、功能注释整合的精细定位、与多组学/EHR 的联合分析; domain_scope=生物医学
  maturity: 主流  # 群体遗传学标准范式,工具链(PLINK/REGENIE)持续迭代,生物库时代仍是核心

- method_name: 临床预测模型(逻辑回归风险评分,TRIPOD 规范)
  task_type: 临床二分类风险预测/诊断概率估计(可解释评分)
  input_data: 结构化临床变量(人口学/生命体征/实验室/合并症)
  output_result: 事件发生概率、风险评分/列线图(nomogram)
  core_assumption: 对数几率与预测变量近似线性;变量间无严重共线性;事件数/变量数(EPV)充足
  advantages: 高度可解释、系数即 OR、易转列线图/床旁评分;数据需求小;监管/临床接受度高;TRIPOD 提供透明报告标准
  limitations: 难捕捉非线性与高阶交互;特征工程依赖专家;易过拟合(需内/外部验证);类别不平衡需校准
  common_baselines: 既有评分(APACHE/SOFA/Framingham)、随机森林、XGBoost、GAM
  evaluation_metrics: AUROC(区分度)、校准曲线/Brier/Hosmer-Lemeshow、决策曲线分析(DCA)、净重分类指数(NRI)
  suitable_datasets: MIMIC-IV、eICU、UK Biobank、Framingham 队列
  implementation_repo: R rms/glmnet、Python statsmodels/scikit-learn、列线图 R regplot
  representative_papers:
    - "Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis (TRIPOD): the TRIPOD statement | 2015 | cited:3983 | doi:10.1136/bmj.g7594 | checked:2026-06-09"
    - "General Cardiovascular Risk Profile for Use in Primary Care (Framingham) | 2008 | cited:7437 | doi:10.1161/circulationaha.107.699579 | checked:2026-06-09"
  possible_innovation_points: 可解释 ML 与逻辑回归对比的临床效用(DCA)、外部多中心验证与公平性、动态/时序风险更新、TRIPOD+AI 报告规范落地; domain_scope=生物医学
  maturity: 经典  # 逻辑回归风险评分是临床预测金标准范式,TRIPOD(及 2024 TRIPOD+AI)强化其规范地位

- method_name: AlphaFold 蛋白质结构预测
  task_type: 从氨基酸序列预测蛋白三维结构
  input_data: 蛋白序列 + 多序列比对(MSA)+ 模板(可选)
  output_result: 原子级三维坐标 + 每残基置信度(pLDDT)+ PAE 矩阵
  core_assumption: 进化共变信息(MSA)编码残基空间邻近关系;端到端几何注意力(Evoformer+结构模块)可直接回归坐标
  advantages: 多数单体达实验级精度;pLDDT 提供可信度;覆盖近全人类蛋白组(AlphaFold DB);加速结构生物学/药物发现
  limitations: 依赖深 MSA(孤儿蛋白/快速进化差);静态单构象(难捕捉动态/变构/无序区);点突变效应、配体结合预测有限(AF3 部分改善);算力高
  common_baselines: 同源建模(Modeller)、RoseTTAFold、I-TASSER、ESMFold(单序列)
  evaluation_metrics: GDT-TS、TM-score、lDDT、RMSD(对实验结构,CASP 评测)
  suitable_datasets: PDB、CASP 评测集、UniProt/AlphaFold DB
  implementation_repo: deepmind/alphafold、ColabFold、OpenFold
  representative_papers:
    - "Highly accurate protein structure prediction with AlphaFold | 2021 | cited:44717 | doi:10.1038/s41586-021-03819-2 | checked:2026-06-09"
    - "Accurate structure prediction of biomolecular interactions with AlphaFold 3 | 2024 | cited:13376 | doi:10.1038/s41586-024-07487-w | checked:2026-06-09"
  possible_innovation_points: 蛋白动态/多构象与无序区、蛋白-配体/核酸复合物(AF3 方向)、突变效应与稳定性预测、与冷冻电镜/实验数据联合精修; domain_scope=生物医学
  maturity: 主流  # 2021 起结构预测范式革命,AF3(2024)扩展到复合物,领域绝对主流且快速演进

- method_name: CheXNet 类 医学影像分类(胸片多标签)
  task_type: 医学图像分类/多标签疾病检测(常配弱监督定位)
  input_data: 胸部 X 光片(单/多视角),弱标注(报告/NLP 抽取标签)
  output_result: 各病理类别概率;Grad-CAM 热力图定位
  core_assumption: 自然图像预训练 CNN/Transformer 可迁移到放射影像;影像级标签足以学习病理表征
  advantages: 迁移学习小成本达放射科医师级表现(特定任务);可弱监督热力图定位;部署相对轻量
  limitations: 标签由 NLP 从报告抽取,噪声/不确定标签多;数据集偏移与捷径学习(导联/标记物);单中心泛化差;多标签共现混淆
  common_baselines: DenseNet-121(CheXNet 原型)、ResNet、ViT/Swin、CLIP 类视觉-语言预训练
  evaluation_metrics: 每类 AUROC、宏/微平均 AUROC、F1、与放射科医师对比的敏感度/特异度
  suitable_datasets: ChestX-ray14、CheXpert、MIMIC-CXR、PadChest
  implementation_repo: TorchXRayVision、官方/复现 CheXNet、MONAI
  representative_papers:
    - "CheXNet: Radiologist-Level Pneumonia Detection on Chest X-Rays with Deep Learning | 2017 | cited:1455 | doi:10.48550/arxiv.1711.05225 | checked:2026-06-09"
    - "CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison | 2019 | cited:2539 | doi:10.1609/aaai.v33i01.3301590 | checked:2026-06-09"
  possible_innovation_points: 视觉-语言基础模型(报告+影像)、不确定标签的鲁棒学习、跨机构域泛化与公平性、罕见病理长尾、可信定位与临床验证; domain_scope=生物医学
  maturity: 主流  # CheXNet(2017)为奠基范式,当前实践已转向 ViT/视觉-语言基础模型,任务范式仍主流
```
