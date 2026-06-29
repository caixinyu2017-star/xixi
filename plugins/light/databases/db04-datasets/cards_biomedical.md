# db04 数据集卡 — 生物医学 / 临床 / 组学

> schema: `dataset_name, domain, task, data_type, size, format, license, download_url, paper_url, citation, leaderboard_url, known_issues, bias_risk, privacy_risk, preprocessing_steps, recommended_splits`
> 可核查字段来自 OpenAlex 真实查询（2026-06-10）；医学数据集访问限制/隐私风险必须如实写。本文件是专题归档，少量数据集可能与 `cards_frontier.md` 重叠。

```yaml
- dataset_name: MIMIC-IV
  domain: 临床医学 / ICU / EHR
  task: ICU 预后预测、死亡率/再入院/败血症/用药/时间序列建模
  data_type: 去标识化电子病历、ICU chart events、实验室、用药、诊断/操作编码
  size: 数十万住院/ICU 记录（随版本更新）
  format: CSV/Parquet（PhysioNet 下载后自处理）
  license: PhysioNet credentialed access；需 CITI/数据使用协议；禁止再识别/再分发原始数据
  download_url: https://physionet.org/content/mimiciv/
  paper_url: https://doi.org/10.1038/s41597-022-01899-x
  citation: "MIMIC-IV, a freely accessible electronic health record dataset | 2023 | cited:2694 | doi:10.1038/s41597-022-01899-x; last_checked=待核; doi=10.1038/s41597-022-01899-x"
  leaderboard_url: 无统一官方榜；常见任务有 mortality/LOS/sepsis benchmark
  known_issues: 单中心(BIDMC)；时间戳偏移；编码体系复杂；缺失非随机；版本间 schema 变化; domain_scope=生物医学
  bias_risk: 高 — ICU 人群、地区/医院选择偏差、种族/保险等社会因素影响
  privacy_risk: 高 — 去标识化医疗数据，必须遵守 DUA/HIPAA 风险控制
  preprocessing_steps: 只用合法下载；固定版本；按 patient-level split；处理时间窗/缺失/单位；避免未来信息泄漏
  recommended_splits: patient-level train/val/test；时间外推 split 可做泛化测试

- dataset_name: eICU Collaborative Research Database
  domain: 临床医学 / 多中心 ICU / EHR
  task: ICU 预后、跨医院泛化、迁移学习、多中心验证
  data_type: 去标识化 ICU EHR、护理记录、实验室、治疗、APACHE 等
  size: 20 万+ ICU stays、300+ hospitals（量级）
  format: CSV（PhysioNet）
  license: PhysioNet credentialed access；需培训/DUA；禁止再识别和未授权再分发
  download_url: https://physionet.org/content/eicu-crd/
  paper_url: https://doi.org/10.1038/sdata.2018.178
  citation: "The eICU Collaborative Research Database, a freely available multi-center database for critical care research | 2018 | cited:1822 | doi:10.1038/sdata.2018.178; last_checked=待核; doi=10.1038/sdata.2018.178"
  leaderboard_url: 无统一官方榜
  known_issues: 多中心数据字段不一致；医院级差异大；部分变量抽取规则复杂；缺失机制强; domain_scope=生物医学
  bias_risk: 高 — 医院类型/地区/纳入机制差异，模型可能学到中心偏差
  privacy_risk: 高 — 医疗隐私数据，需 credentialed access
  preprocessing_steps: patient/hospital-level split；统一变量单位；处理医院 ID 泄漏；跨中心外部验证
  recommended_splits: hospital-disjoint 或 patient-level split；与 MIMIC-IV 互作外部验证

- dataset_name: UK Biobank
  domain: 生物医学 / 人群队列 / 多组学
  task: 流行病学、GWAS、影像遗传、疾病风险预测、多模态健康建模
  data_type: 表型、问卷、基因型、影像、体检、生化、随访结局
  size: 50 万参与者量级
  format: 申请获批后按字段下载；BGEN/PLINK/CSV/影像等多格式
  license: 需正式项目申请与 Data Access Agreement；不可公开再分发个人级数据
  download_url: https://www.ukbiobank.ac.uk/
  paper_url: https://doi.org/10.1371/journal.pmed.1001779
  citation: "UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age | 2015 | cited:13217 | doi:10.1371/journal.pmed.1001779; last_checked=待核; doi=10.1371/journal.pmed.1001779"
  leaderboard_url: 无统一 leaderboard
  known_issues: 健康志愿者偏倚；祖源/年龄范围限制；字段多、缺失与随访时间复杂; domain_scope=生物医学
  bias_risk: 高 — 英国中老年志愿者样本，不代表全人群；祖源不均衡影响 PRS 泛化
  privacy_risk: 高 — 个人级健康/遗传数据，受严格 DUA 控制
  preprocessing_steps: 项目审批；祖源/亲缘过滤；字段缺失处理；按参与者 split；结局时间窗定义
  recommended_splits: participant-level split；跨祖源/时间外部验证；严格避免亲缘泄漏

- dataset_name: TCGA / Pan-Cancer Atlas
  domain: 肿瘤组学 / 多组学
  task: 癌种分类、生存分析、突变/表达关联、预后模型、多组学融合
  data_type: 基因表达、突变、拷贝数、甲基化、临床结局、部分病理影像
  size: 1 万+肿瘤样本、30+ 癌种（按项目版本）
  format: GDC portal/API、MAF、HTSeq counts、clinical TSV、BAM 受控访问
  license: GDC/NIH 数据使用条款；开放层可下载，受控层需 dbGaP 授权
  download_url: https://portal.gdc.cancer.gov/
  paper_url: https://doi.org/10.1038/ng.2764
  citation: "The Cancer Genome Atlas Pan-Cancer analysis project | 2013 | cited:9467 | doi:10.1038/ng.2764; last_checked=待核; doi=10.1038/ng.2764"
  leaderboard_url: 无统一 leaderboard；常用于 pan-cancer benchmark
  known_issues: 批次效应、癌种/平台差异、样本量不均衡、临床结局缺失与删失; domain_scope=通用
  bias_risk: 中高 — 癌种/中心/族裔分布不均；肿瘤样本非一般人群
  privacy_risk: 中高 — 开放数据已去标识，受控原始测序需授权
  preprocessing_steps: 批次校正；基因过滤/标准化；样本 ID 对齐；patient-level split；生存结局删失处理
  recommended_splits: patient-level stratified split；癌种留一外推；时间/中心外部验证（若字段可用）

- dataset_name: MIMIC-CXR / CheXpert
  domain: 医学影像 / 胸部 X 光
  task: 多标签胸片疾病分类、报告生成、视觉-语言预训练、弱监督定位
  data_type: 胸部 X 光图像 + 放射报告/不确定标签
  size: MIMIC-CXR 37 万+ 图像；CheXpert 22 万+ 图像（量级）
  format: DICOM/JPG + CSV labels/reports
  license: MIMIC-CXR 需 PhysioNet credentialed access；CheXpert 按 Stanford 数据使用条款申请/下载；禁止未授权再分发
  download_url: https://physionet.org/content/mimic-cxr/ ; https://stanfordmlgroup.github.io/competitions/chexpert/
  paper_url: https://doi.org/10.1038/s41597-019-0322-0 ; https://doi.org/10.1609/aaai.v33i01.3301590
  citation: |
    MIMIC-CXR, a de-identified publicly available database of chest radiographs with free-text reports | 2019 | cited:1601 | doi:10.1038/s41597-019-0322-0
    CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison | 2019 | cited:2539 | doi:10.1609/aaai.v33i01.3301590
    [last_checked=待核; 锚点已内联 doi:/cited:,被引实时查见 dataset_signal.py]
  leaderboard_url: CheXpert competition/leaderboard（官方页面）；MIMIC-CXR 无统一榜
  known_issues: 标签由报告 NLP 抽取，存在 uncertain/no mention 噪声；便携机/标记物/医院域偏移；患者多图相关; domain_scope=生物医学
  bias_risk: 高 — 医院/设备/人群偏差，弱标签可能反映报告习惯
  privacy_risk: 高 — 医疗影像去标识数据，需遵守 DUA
  preprocessing_steps: patient-level split；视图过滤；uncertain label 策略固定；图像归一化；报告文本去 PHI 检查
  recommended_splits: 官方 CheXpert train/val/test；MIMIC-CXR patient-level split，与 CheXpert 互作外部验证

- dataset_name: ADNI (Alzheimer's Disease Neuroimaging Initiative)
  domain: 神经影像 / 阿尔茨海默病 / 多模态纵向队列
  task: AD/MCI 诊断、疾病进展预测、影像-生物标志物融合、纵向建模
  data_type: MRI/PET、认知量表、CSF/血液生物标志物、遗传与临床随访
  size: 数千名受试者、纵向多时间点（随 ADNI 阶段更新）
  format: DICOM/NIfTI、CSV 临床表、影像派生特征
  license: 需 ADNI 数据使用申请；不可未授权再分发；遵守隐私与署名规则
  download_url: https://adni.loni.usc.edu/
  paper_url: https://doi.org/10.1016/j.jalz.2010.03.007
  citation: "The Alzheimer's Disease Neuroimaging Initiative: Progress report and future plans | 2010 | cited:603 | doi:10.1016/j.jalz.2010.03.007; last_checked=待核; doi=10.1016/j.jalz.2010.03.007"
  leaderboard_url: TADPOLE challenge（历史挑战）/ 待核查当前官方榜
  known_issues: 队列选择偏倚；扫描协议/中心差异；纵向缺失；MCI 转化标签定义复杂; domain_scope=多模态CV
  bias_risk: 高 — 年龄/教育/族裔/中心偏差影响泛化
  privacy_risk: 高 — 人体影像与临床数据，需 DUA
  preprocessing_steps: subject-level split；按时间预测避免未来泄漏；影像配准/分割流程固定；缺失机制记录
  recommended_splits: subject-level split；外部验证可用 AIBL/OASIS（需另核许可）

- dataset_name: HAM10000 / ISIC Archive
  domain: 皮肤病学 / 皮肤镜图像
  task: 皮肤病灶分类、黑色素瘤检测、领域泛化与公平性评估
  data_type: 皮肤镜 RGB 图像 + 诊断标签 + 元数据(年龄/性别/部位等)
  size: HAM10000 10,015 张图像；ISIC Archive 更大且持续更新
  format: JPG/PNG + CSV metadata
  license: HAM10000 Scientific Data 开放数据；ISIC 各集合许可不一，商用/再分发需逐集合核实
  download_url: "https://www.isic-archive.com/ ; HAM10000: https://doi.org/10.1038/sdata.2018.161"
  paper_url: https://doi.org/10.1038/sdata.2018.161
  citation: "The HAM10000 dataset, a large collection of multi-source dermatoscopic images of common pigmented skin lesions | 2018 | cited:3144 | doi:10.1038/sdata.2018.161; last_checked=待核; doi=10.1038/sdata.2018.161"
  leaderboard_url: ISIC Challenge leaderboards
  known_issues: 类别极不平衡；同一 lesion 多图可能泄漏；肤色/设备/中心偏差；标签质量混合; domain_scope=通用
  bias_risk: 高 — 肤色/地区/采集设备偏差会影响临床公平性
  privacy_risk: 中 — 去标识皮肤图像和有限元数据，仍需遵守许可
  preprocessing_steps: lesion-level split；去重；颜色/尺寸标准化；类别重采样需报告；按肤色/中心做分组评估
  recommended_splits: 官方 ISIC challenge split 或 lesion-disjoint stratified split
```
