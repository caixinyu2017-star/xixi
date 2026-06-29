# db04 数据集卡 — 理工跨学科 / 科学计算 / 材料天气脑科学

> schema: `dataset_name, domain, task, data_type, size, format, license, download_url, paper_url, citation, leaderboard_url, known_issues, bias_risk, privacy_risk, preprocessing_steps, recommended_splits`
> 可核查字段来自 OpenAlex 真实查询（2026-06-10）；许可/下载条款按官方页面常识记录，不确定处写「待核查」。本文件是专题归档，少量数据集可能与 `cards_frontier.md` 重叠。

```yaml
- dataset_name: Materials Project
  domain: 材料科学 / 第一性原理数据库
  task: 晶体结构性质预测、形成能/带隙/稳定性、高通量筛选
  data_type: 晶体结构 + DFT 计算性质
  size: 约 15 万+ inorganic compounds（随版本更新）
  format: API / JSON / pymatgen Structure / CSV 导出
  license: Materials Project API 条款；研究可用，批量下载/再分发/商用需遵守官方 Terms
  download_url: "https://materialsproject.org/ ; API: https://api.materialsproject.org/"
  paper_url: https://doi.org/10.1063/1.4812323
  citation: "Commentary: The Materials Project: A materials genome approach to accelerating materials innovation | 2013 | cited:12560 | doi:10.1063/1.4812323; last_checked=待核; doi=10.1063/1.4812323"
  leaderboard_url: https://matbench.materialsproject.org/  # 相关 Matbench 任务
  known_issues: DFT-PBE 系统误差；数据库版本持续变动，必须记录 API 版本/查询日期；部分性质缺失; domain_scope=化学-材料
  bias_risk: 中 — 偏无机晶体与可计算稳定结构，对实验失败/非晶/缺陷覆盖不足
  privacy_risk: 无
  preprocessing_steps: 固定材料 ID 与版本；去重 polymorph；按 composition/structure 防泄漏划分；标准化目标单位
  recommended_splits: Matbench 官方 split 或 composition-disjoint / time-split

- dataset_name: QM9
  domain: 量子化学 / 小分子
  task: 分子性质预测、量子化学回归、分子图表示学习
  data_type: 134k 小有机分子结构 + DFT 计算性质
  size: 133,885 molecules（常用清洗版）
  format: SDF / XYZ / CSV / PyG/DGL/DeepChem 内置
  license: Scientific Data 数据集开放使用；具体再分发按原始条款核实
  download_url: https://figshare.com/articles/dataset/Quantum_chemistry_structures_and_properties_of_134_kilo_molecules/978904
  paper_url: https://doi.org/10.1038/sdata.2014.22
  citation: "Quantum chemistry structures and properties of 134 kilo molecules | 2014 | cited:2007 | doi:10.1038/sdata.2014.22; last_checked=待核; doi=10.1038/sdata.2014.22"
  leaderboard_url: https://paperswithcode.com/dataset/qm9
  known_issues: 小分子、元素范围窄(CHONF)；任务已高度饱和；随机划分会高估泛化; domain_scope=化学-材料
  bias_risk: 中 — 只覆盖小有机分子化学空间
  privacy_risk: 无
  preprocessing_steps: 统一单位；去除异常分子；3D 坐标/原子特征标准化；保留 scaffold split
  recommended_splits: scaffold split 或官方/常用 110k/10k/10k split；报告 split 种子

- dataset_name: OQMD (Open Quantum Materials Database)
  domain: 材料科学 / DFT 形成能
  task: 形成能预测、相稳定性、晶体结构性质建模
  data_type: 无机晶体结构 + DFT 计算形成能/稳定性
  size: 百万级 DFT 计算条目（随版本更新）
  format: Web/API/SQL dump（具体按官方发布）
  license: OQMD 使用条款；学术研究可用，批量再分发/商用需核实
  download_url: https://oqmd.org/
  paper_url: https://doi.org/10.1038/npjcompumats.2015.10
  citation: "The Open Quantum Materials Database (OQMD): assessing the accuracy of DFT formation energies | 2015 | cited:2331 | doi:10.1038/npjcompumats.2015.10; last_checked=待核; doi=10.1038/npjcompumats.2015.10"
  leaderboard_url: 待核查（常用于 Matbench/材料性质预测对比）
  known_issues: DFT 参数/版本差异；重复结构与衍生结构多；形成能标签非实验真值; domain_scope=化学-材料
  bias_risk: 中 — 偏可枚举无机晶体与 DFT 可收敛体系
  privacy_risk: 无
  preprocessing_steps: 记录版本；去重 composition/structure；单位统一；按元素组合或时间切分
  recommended_splits: composition-disjoint split / scaffold-like chemical split / 时间版本 split

- dataset_name: Open Catalyst 2020 (OC20)
  domain: 催化 / 表面吸附 / 原子模拟
  task: 吸附体系能量与力预测、结构弛豫、催化材料筛选
  data_type: DFT 弛豫轨迹、原子结构、能量、力
  size: 约 1.2M relaxations / 2.5M structures（OC20 量级）
  format: LMDB / ASE Atoms / PyTorch Geometric
  license: CC BY 4.0（Open Catalyst Project 数据常用条款，使用前核对具体版本）
  download_url: https://opencatalystproject.org/
  paper_url: https://doi.org/10.1021/acscatal.0c04525
  citation: "Open Catalyst 2020 (OC20) Dataset and Community Challenges | 2021 | cited:704 | doi:10.1021/acscatal.0c04525; last_checked=待核; doi=10.1021/acscatal.0c04525"
  leaderboard_url: https://opencatalystproject.org/challenge.html
  known_issues: 数据极大、训练成本高；任务 split 复杂(ID/OOD adsorbate/catalyst/both)；DFT 标签仍有近似误差; domain_scope=通用
  bias_risk: 中 — 任务分布由特定表面/吸附物组合定义
  privacy_risk: 无
  preprocessing_steps: 用官方 split；邻域半径图构建；能量/力单位一致；记录是否使用 IS2RE/S2EF/IS2RS 任务
  recommended_splits: 官方 ID / OOD Ads / OOD Cat / OOD Both

- dataset_name: JARVIS-DFT
  domain: 材料科学 / 多性质 DFT 数据库
  task: 材料性质预测、2D材料/光电/弹性/声子等多任务建模
  data_type: 晶体结构 + DFT 计算性质 + 多领域派生数据
  size: 数万级 DFT 材料条目（随 JARVIS 版本更新）
  format: JSON / jarvis-tools / API
  license: NIST/JARVIS 开放数据条款；使用前核对引用与再分发要求
  download_url: https://jarvis.nist.gov/
  paper_url: https://doi.org/10.1038/s41524-020-00440-1
  citation: "The joint automated repository for various integrated simulations (JARVIS) for data-driven materials design | 2020 | cited:479 | doi:10.1038/s41524-020-00440-1; last_checked=待核; doi=10.1038/s41524-020-00440-1"
  leaderboard_url: https://pages.nist.gov/jarvis_leaderboard/
  known_issues: 任务多且版本变动；不同性质缺失率不同；需明确使用的子任务与版本; domain_scope=化学-材料
  bias_risk: 中 — 偏计算可得材料，实验合成失败样本不足
  privacy_risk: 无
  preprocessing_steps: 固定 JARVIS version；按任务过滤缺失；统一单位；避免同构/同组成泄漏
  recommended_splits: 官方 leaderboard split 或 composition-disjoint split

- dataset_name: WeatherBench / ERA5-derived benchmark
  domain: 气象 / 地球系统科学
  task: 数据驱动天气预报、再分析场外推、时空预测
  data_type: ERA5 再分析格点场，多变量、多气压层时间序列
  size: TB 级（变量/分辨率/时间范围决定）
  format: NetCDF / Zarr / xarray
  license: ERA5/Copernicus 数据开放但需遵守 ECMWF/C3S 使用条款与署名要求
  download_url: "https://github.com/pangeo-data/WeatherBench ; ERA5: https://cds.climate.copernicus.eu/"
  paper_url: https://doi.org/10.1029/2020ms002203
  citation: |
    WeatherBench: A Benchmark Data Set for Data‐Driven Weather Forecasting | 2020 | cited:432 | doi:10.1029/2020ms002203
    ERA5: The ERA5 global reanalysis | 2020 | cited:30033 | doi:10.1002/qj.3803
    [last_checked=待核; 锚点已内联 doi:/cited:,被引实时查见 dataset_signal.py]
  leaderboard_url: https://sites.research.google/weatherbench/
  known_issues: 数据量大；变量/层/分辨率选择会影响可比性；物理守恒和极端事件评估需额外指标; domain_scope=通用
  bias_risk: 中 — 再分析系统误差与观测稀疏地区偏差
  privacy_risk: 无
  preprocessing_steps: 选定变量/层/lead time；时间切分；归一化按 train 统计；记录再网格化/分辨率
  recommended_splits: WeatherBench 官方 train/validation/test 时间切分

- dataset_name: Human Connectome Project (HCP)
  domain: 脑科学 / 神经影像
  task: 连接组分析、脑网络建模、fMRI/DTI 表征学习
  data_type: MRI/fMRI/dMRI/行为量表等多模态人脑数据
  size: 约 1200 名健康成年人（HCP Young Adult 主队列）
  format: NIfTI/CIFTI/BIDS-like 派生格式，ConnectomeDB 下载
  license: HCP Data Use Terms；需注册，同意隐私/再识别限制；部分 restricted data 需额外申请
  download_url: https://www.humanconnectome.org/study/hcp-young-adult
  paper_url: https://doi.org/10.1016/j.neuroimage.2013.05.041
  citation: "The WU-Minn Human Connectome Project: An overview | 2013 | cited:6205 | doi:10.1016/j.neuroimage.2013.05.041; last_checked=待核; doi=10.1016/j.neuroimage.2013.05.041"
  leaderboard_url: 无统一 leaderboard；常作为神经影像方法 benchmark
  known_issues: 数据预处理复杂；家系/亲缘结构可能造成泄漏；restricted variables 不可随意公开; domain_scope=通用
  bias_risk: 中 — 健康青年样本，年龄/疾病泛化有限
  privacy_risk: 高 — 人体影像与行为数据，需遵守 DUA，禁止再识别
  preprocessing_steps: 使用官方 minimal preprocessing；被试级划分；去除 restricted 字段；记录 parcellation/平滑/滤波
  recommended_splits: subject-level split；家系相关研究需 family-aware split
```
