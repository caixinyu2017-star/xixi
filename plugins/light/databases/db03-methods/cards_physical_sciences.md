# db03 方法卡 — 理工跨学科 / 物理化学材料

> 每张卡注明 maturity（经典|主流|新兴|过时|不推荐），避免提出落后方案。受版权全文不收录，仅元数据与开源链接。
> representative_papers 的标题/年份/被引/DOI 来自 OpenAlex 真实查询（https://api.openalex.org，mailto 礼貌池），查询日期 **2026-06-10**；被引数随时间变动。
> 查不到可信记录的字段写「待核查」，不编造。

字段 schema 同 db03：`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`

## 方法卡

```yaml
- method_name: 分子/材料图神经网络性质预测 (MPNN / SchNet / CGCNN)
  task_type: 分子与晶体材料性质预测(能量、形成能、带隙、HOMO-LUMO、溶解度、力等回归/分类)
  input_data: 分子图(原子节点、化学键边)或晶体周期图(原子坐标+晶格+邻接/半径图)
  output_result: 分子/材料级性质、逐原子力/电荷、结构嵌入表示
  core_assumption: 化学/材料性质主要由局部原子环境与相互作用决定；图消息传递可保持排列不变性并聚合邻域信息
  advantages: 端到端利用结构信息；比手工描述符更灵活；可跨分子/晶体任务迁移；适合高通量筛选
  limitations: 对训练分布外元素/结构泛化弱；3D等变性若未显式建模会损失几何归纳偏置；数据质量依赖 DFT/实验标签；不确定性需额外建模
  common_baselines: Morgan fingerprint + RF/XGBoost、Coulomb Matrix、SOAP、MEGNet、DimeNet、PaiNN、NequIP/Allegro
  evaluation_metrics: MAE/RMSE、R²、Spearman、分类 AUC/F1、OOD split 性能、校准/不确定性覆盖率
  suitable_datasets: QM9、Materials Project、OQMD、MoleculeNet、Open Catalyst OC20/OC22
  implementation_repo: PyTorch Geometric、DGL-LifeSci、DeepChem、CGCNN、MatGL、SchNetPack
  representative_papers:
    - "Neural Message Passing for Quantum Chemistry | 2017 | cited:3008 | doi:10.48550/arxiv.1704.01212 | checked:2026-06-10"
    - "SchNet – A deep learning architecture for molecules and materials | 2018 | cited:2176 | doi:10.1063/1.5019779 | checked:2026-06-10"
    - "Crystal Graph Convolutional Neural Networks for an Accurate and Interpretable Prediction of Material Properties | 2018 | cited:2623 | doi:10.1103/physrevlett.120.145301 | checked:2026-06-10"
  possible_innovation_points: 等变几何网络、多保真/主动学习、跨材料体系迁移、物理约束损失、预测不确定性驱动的实验/DFT 采样; domain_scope=物理科学
  maturity: 主流  # 2017–2018 后成为材料/分子 ML 主流基线，仍快速迭代到等变网络与基础模型

- method_name: "密度泛函理论 (DFT: Kohn-Sham / PBE)"
  task_type: 从第一性原理计算电子结构、能量、力、带隙、吸附能与材料稳定性
  input_data: 原子种类、晶体/分子结构、赝势/基组、交换关联泛函、k 点与收敛参数
  output_result: 总能、电子密度、能带/DOS、力、应力、形成能/吸附能等
  core_assumption: 多电子体系基态由电子密度唯一决定；Kohn-Sham 将相互作用体系映射为非相互作用参考体系；PBE 等 GGA 近似交换关联能
  advantages: 物理基础扎实；无需经验势即可给出材料/分子性质；是材料数据库和机器学习势的主要标签来源
  limitations: 计算成本高；泛函近似导致带隙/强关联/范德华/激发态误差；结果对收敛参数与赝势敏感
  common_baselines: LDA、GGA-PBE、PBEsol、SCAN、HSE06、DFT+U、GW/CCSD(T)小体系高精度参考
  evaluation_metrics: 能量/力误差、晶格常数误差、形成能 MAE、带隙误差、实验一致性、收敛残差
  suitable_datasets: Materials Project、OQMD、AFLOW、JARVIS-DFT、NOMAD
  implementation_repo: VASP、Quantum ESPRESSO、ABINIT、GPAW、CP2K、ASE/pymatgen 工作流
  representative_papers:
    - "Self-Consistent Equations Including Exchange and Correlation Effects | 1965 | cited:63031 | doi:10.1103/physrev.140.a1133 | checked:2026-06-10"
    - "Generalized Gradient Approximation Made Simple | 1996 | cited:210436 | doi:10.1103/physrevlett.77.3865 | checked:2026-06-10"
  possible_innovation_points: DFT+ML surrogate、主动学习减少昂贵计算、泛函误差校正、多保真融合、自动高通量工作流与可复现实验记录; domain_scope=物理科学
  maturity: 经典  # 第一性原理材料模拟的核心范式，机器学习方法多数仍以 DFT 标签为基础

- method_name: "机器学习原子间势 (MLIP: DeePMD / NequIP)"
  task_type: 以接近第一性原理精度进行大规模分子动力学/材料动力学模拟
  input_data: 原子类型、坐标、邻域图；训练标签为 DFT 能量/力/应力
  output_result: 原子势能面、能量、力、应力；可驱动 MD 轨迹
  core_assumption: 总能可由局部原子环境分解/组合；网络需满足平移/旋转/置换对称性；等变网络可更高效学习几何力场
  advantages: 比 DFT 快几个数量级；比传统经验势更准确/可迁移；可扩展到百万原子或长时间尺度
  limitations: 训练集覆盖不足会导致不稳定外推；主动学习/不确定性监控必需；跨相/反应路径泛化难；训练与验证成本高
  common_baselines: EAM/MEAM、ReaxFF、GAP/SOAP、MTP、SNAP、传统 DFT-MD
  evaluation_metrics: 能量/力 RMSE、应力误差、结构/相变/扩散系数复现、能量守恒、OOD 稳定性
  suitable_datasets: Materials Project 派生轨迹、OC20/OC22、自建 DFT-MD、JARVIS、NOMAD
  implementation_repo: DeePMD-kit、NequIP、Allegro、MACE、ASE/LAMMPS 接口
  representative_papers:
    - "Deep Potential Molecular Dynamics: A Scalable Model with the Accuracy of Quantum Mechanics | 2018 | cited:2191 | doi:10.1103/physrevlett.120.143001 | checked:2026-06-10"
    - "E(3)-equivariant graph neural networks for data-efficient and accurate interatomic potentials | 2022 | cited:1642 | doi:10.1038/s41467-022-29939-5 | checked:2026-06-10"
  possible_innovation_points: 主动学习闭环、反应/相变 OOD 检测、长程电荷/磁性物理约束、基础势模型微调、多保真势能面; domain_scope=物理科学
  maturity: 主流  # DeePMD/NequIP/MACE 已成为计算材料与化学模拟的主流 MLIP 路线

- method_name: EEG 深度解码网络 (EEGNet / Deep ConvNet)
  task_type: 脑机接口/神经工程中的 EEG 运动想象、事件相关电位、睡眠/情绪等分类
  input_data: 多通道 EEG 时间序列(通道 × 时间)，可带滤波、分段、伪迹去除
  output_result: 类别概率、时频/空间滤波特征、可视化的通道/频段贡献
  core_assumption: EEG 判别信息分布在空间通道、频段与时间模式中；轻量卷积可学习类似 FBCSP 的时空滤波器
  advantages: 参数少、小数据可训练；端到端学习时空特征；跨范式相对通用；便于嵌入实时 BCI
  limitations: 个体差异大、跨被试泛化弱；伪迹/电极噪声敏感；数据量小容易过拟合；解释性需配合频段/拓扑图
  common_baselines: CSP/FBCSP + LDA/SVM、Riemannian geometry、Shallow ConvNet、Transformer/TCN EEG 模型
  evaluation_metrics: Accuracy、balanced accuracy、F1、AUC、信息传输率(ITR)、跨被试/跨会话泛化
  suitable_datasets: BCI Competition IV、PhysioNet EEG Motor Movement/Imagery、TUH EEG、Sleep-EDF
  implementation_repo: braindecode、MOABB、EEGNet Keras/PyTorch 复现、MNE-Python
  representative_papers:
    - "EEGNet: a compact convolutional neural network for EEG-based brain–computer interfaces | 2018 | cited:4204 | doi:10.1088/1741-2552/aace8c | checked:2026-06-10"
    - "Deep learning with convolutional neural networks for EEG decoding and visualization | 2017 | cited:3452 | doi:10.1002/hbm.23730 | checked:2026-06-10"
  possible_innovation_points: 跨被试自适应/域泛化、少样本校准、Riemannian+深度融合、可解释频段约束、在线漂移检测; domain_scope=物理科学
  maturity: 主流  # EEGNet 是 BCI 深度学习强基线，传统 CSP/Riemannian 仍需作为对照

- method_name: AI 中期天气预报 (Pangu-Weather / GraphCast)
  task_type: 全球中期天气预报、再分析场外推、多变量时空预测
  input_data: ERA5 等再分析格点场(气压层/地表变量、多时间步)，可带地理网格/球面图结构
  output_result: 未来多步气象变量场(温度、风、位势高度、降水等)与极端天气轨迹
  core_assumption: 大气演化可从历史再分析场中学习统计动力学；3D 神经网络/图网络可捕捉垂直层和球面邻接关系
  advantages: 推理远快于传统数值天气模式；中期预报精度在多指标上接近/超过 ECMWF HRES；适合快速集合预报
  limitations: 依赖 ERA5 训练分布；物理守恒与极端外推仍需谨慎；降水/小尺度过程较难；业务部署需不确定性与资料同化
  common_baselines: ECMWF HRES/IFS、FourCastNet、ClimaX、传统 NWP、Persistence/Climatology
  evaluation_metrics: RMSE、ACC(anomaly correlation)、CRPS、极端事件命中率、热带气旋轨迹误差
  suitable_datasets: ERA5、WeatherBench、ECMWF 业务分析/预报资料
  implementation_repo: Huawei Pangu-Weather、DeepMind GraphCast、WeatherBench、NVIDIA Modulus/FourCastNet
  representative_papers:
    - "Accurate medium-range global weather forecasting with 3D neural networks | 2023 | cited:1386 | doi:10.1038/s41586-023-06185-3 | checked:2026-06-10"
    - "Learning skillful medium-range global weather forecasting | 2023 | cited:1120 | doi:10.1126/science.adi2336 | checked:2026-06-10"
  possible_innovation_points: 物理约束/守恒校正、不确定性集合预报、区域高分辨率下尺度、极端事件专门损失、与传统 NWP 混合; domain_scope=物理科学
  maturity: 新兴  # 2023 后快速爆发，效果强但业务可信度/物理一致性仍在验证

- method_name: 晶体结构预测 (CALYPSO / USPEX)
  task_type: 给定化学组成/压力条件预测稳定晶体结构、相图与候选新材料
  input_data: 元素组成、原子数、压力/温度约束、对称性/空间群约束、DFT 能量评估
  output_result: 候选晶体结构、形成焓/能量排序、相稳定性与可能新相
  core_assumption: 全局优化可在巨大结构空间中搜索低能构型；粒子群/进化算法通过选择-变异/群体更新逼近全局最优
  advantages: 不依赖已知结构模板；能发现高压/新奇化合物结构；与 DFT 联用可直接给物理可验证候选
  limitations: DFT 调用昂贵；复杂大体系搜索空间爆炸；易受参数/初始群体影响；动力学可合成性不等于热力学稳定性
  common_baselines: 随机结构搜索、AIRSS、遗传算法、已知原型替换、机器学习势辅助搜索
  evaluation_metrics: 最低能/焓、重复发现率、与实验结构 RMSD/空间群一致性、相图稳定性、计算预算
  suitable_datasets: Materials Project、OQMD、ICSD/Crystallography Open Database、自建 DFT 结构库
  implementation_repo: CALYPSO、USPEX、AIRSS、pymatgen/ASE 高通量结构工作流
  representative_papers:
    - "Crystal structure prediction using ab initio evolutionary techniques: Principles and applications | 2006 | cited:2511 | doi:10.1063/1.2210932 | checked:2026-06-10"
    - "CALYPSO: A method for crystal structure prediction | 2012 | cited:2822 | doi:10.1016/j.cpc.2012.05.008 | checked:2026-06-10"
  possible_innovation_points: MLIP 加速结构搜索、主动学习选择 DFT 评估、合成可达性约束、生成模型提出候选、压力/成分多目标优化; domain_scope=物理科学
  maturity: 主流  # 新材料发现与高压物理中成熟路线，但仍计算昂贵，ML 加速空间大
```
