# db03 方法卡 — 夜间红外/热成像检测 + RGB-IR 多模态融合 + 级联误差传播/端到端联合（cards_nighttime_multimodal.md）

> 每张卡注明 maturity（经典|主流|新兴|过时|不推荐），避免提出落后方案。受版权全文不收录，仅元数据与开源链接。
> representative_papers 的标题/年份/被引/DOI 来自 OpenAlex 真实 curl 结果（https://api.openalex.org，mailto 礼貌池），查询日期 **2026-06-06**；被引数随时间变动。
> 同一论文常有会议正式版与 arXiv 预印本两条 OpenAlex 记录，被引数不同，已分别标注；优先取正式版。
> 排名/成熟度判断为人工标注。查不到的字段写「待核查」。
> 本文件为 db03 既有「检测+跟踪 / 行为识别」卡的补充：补齐**夜间红外检测、RGB-IR 多模态融合、检测→跟踪→行为级联误差传播**三类落地方法（审计确认的空白）。

字段 schema 同 db03：`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`

## 奶山羊夜间/多模态/级联场景适配总览（贯穿各卡 limitations / innovation_points）

针对【奶山羊栏舍 24h 健康/发情/跛行预警】的实拍特点，给出方法选型导向（结论性，细节见各卡）：
- **夜间是刚需，非可选**：发情多在夜间表现（爬跨、活动量骤增），产羔与跛行夜间同样需监测。纯 RGB 夜间近黑，依赖**红外补光相机（NIR）或热成像（LWIR）**。现有 db03 检测卡仅在 limitations 提「需红外微调」，本文件补落地路径。
- **白色奶山羊昼夜外观差异大**：白羊在 NIR/IR 下与栏舍背景对比、纹理、反光均与日间 RGB 差异显著，COCO/日间预训练权重域差大，**低光增强（Zero-DCE/EnlightenGAN）→ 检测** 与 **日间→夜间域适应** 是两条互补路线。
- **热成像（LWIR）无纹理、个体相似**：热图只有温度轮廓，奶山羊个体 re-id 几乎不可行；热成像更适合**做检测+粗定位**，re-id/行为细节需 RGB 或运动线索补充 → 天然指向 **RGB-IR 多模态融合**。
- **多模态可缓解单模态失效**：白天 RGB 主导、夜间 IR 主导、逆光/灯下混合，**illumination-aware 加权 / 概率融合（ProbEn）** 比固定融合更鲁棒；但需 RGB-IR **像素级配准**（栏舍双目/同轴需标定）。
- **级联误差是预警可靠性的命门**：检测→跟踪→行为四级流水线，前级一个漏检/ID switch 会被后级放大为错误发情/跛行告警；置信度传播、不确定性建模、端到端联合训练是缓解方向，目前**无奶山羊专用方法**，需自研。
- **无奶山羊专用夜间/红外/多模态公开数据集**：据查证 KAIST/FLIR/LLVIP 等均为行人/交通域，**不含奶山羊**；红外小目标集（SIRST/NUDT-SIRST）为遥感天空背景。奶山羊夜间红外+行为基准需自建标注（如实说明，不编造）。

## 方法卡

### 一、夜间 / 红外 / 热成像目标检测

```yaml
- method_name: "热红外目标检测（Thermal/LWIR Object Detection，以 YOLO 系迁移为代表）"
  task_type: "单模态热成像目标检测（one-stage 迁移微调）"
  input_data: "单通道/伪彩热成像图（LWIR 8-14μm），夜间无外部光照亦可成像"
  output_result: "类别 + bbox（基于温度轮廓而非可见光纹理）"
  core_assumption: "恒温动物/行人与背景存在稳定温差，热辐射轮廓在全黑/逆光/雾天仍可分辨；可见光检测器结构可迁移，只需在热域重训/微调"
  advantages: "全黑环境可用、不受可见光照变化影响、对烟雾/弱遮挡鲁棒、与 RGB 检测器同构易复用"
  limitations: "无颜色/纹理→个体 re-id 极难；热串扰（群羊聚集体温叠加）致粘连；玻璃/水反射干扰；日间高温环境对比下降；标注数据稀缺"
  common_baselines: "在 RGB 上预训练的 YOLOv8/v11、Faster R-CNN、RetinaNet 直接热域微调；可见光基线对照"
  evaluation_metrics: "mAP@[.5:.95]（热域，记 mAP-IR）、AP50、Miss Rate、FPS"
  suitable_datasets: "FLIR ADAS、KAIST(热通道)、LLVIP、自建奶山羊栏舍热成像集（需自标，无现成）"
  implementation_repo: "ultralytics/ultralytics、open-mmlab/mmdetection、相关 FLIR-YOLO 复现仓库"
  representative_papers:
    - "Thermal Object Detection in Difficult Weather Conditions Using YOLO | 2020(IEEE Access) | cited:297 | doi:10.1109/access.2020.3007481 | checked:2026-06-06"
    - "A Thermal Infrared Pedestrian-Detection Method for Edge Computing Devices | 2022(Sensors) | cited:7 | doi:10.3390/s22176710 | checked:2026-06-06"
    - "Robust pedestrian detection in thermal infrared imagery using the wavelet transform | 2010 | cited:83 | doi:10.1016/j.infrared.2010.03.005 | checked:2026-06-06"
  possible_innovation_points: "奶山羊栏舍 LWIR 夜间检测基线；体温异常（发热/产羔）与热成像检测联动作健康预警；热串扰粘连分割（群羊聚卧）的奶山羊专用后处理; domain_scope=cv-夜间多模态"
  maturity: "主流（热域检测工程成熟，但奶山羊场景为空白，需自建数据）"
```

```yaml
- method_name: "Zero-DCE（Zero-Reference Deep Curve Estimation 低光增强）"
  task_type: "低光照图像增强（无参考自监督），作检测前置预处理"
  input_data: "低光/夜间 RGB 图（无需配对正常光参考）"
  output_result: "增强后亮度/对比提升的 RGB 图（再喂下游检测器）"
  core_assumption: "低光增强可建模为逐像素估计一组高阶曲线(LE-curve)并迭代映射，用一组无参考损失（曝光/色彩恒常/光照平滑/空间一致）即可训练，无需配对数据"
  advantages: "零参考（无需配对数据，契合栏舍难采正常光夜景）、极轻量快、即插即用作检测前处理、无监督"
  limitations: "极暗/近全黑（无红外补光）信息已丢失无法恢复；可能放大噪声；增强目标是「人眼好看」非「检测最优」，不一定提升 mAP；对 NIR 单通道需适配"
  common_baselines: "EnlightenGAN、RetinexNet、LIME、直方图均衡、不增强直接检测"
  evaluation_metrics: "下游检测 mAP/Miss Rate（端到端）、PSNR/SSIM/NIQE（增强质量，无参考用 NIQE）"
  suitable_datasets: "SICE、LOL、自建奶山羊夜间低光集；下游用奶山羊检测集评估"
  implementation_repo: "Li-Chongyi/Zero-DCE、Li-Chongyi/Zero-DCE_extension（Zero-DCE++）"
  representative_papers:
    - "Zero-Reference Deep Curve Estimation for Low-Light Image Enhancement | 2020(CVPR) | cited:2142 | doi:10.1109/cvpr42600.2020.00185 | checked:2026-06-06"
    - "Learning to Enhance Low-Light Image via Zero-Reference Deep Curve Estimation | 2021(TPAMI 扩展) | cited:666 | doi:10.1109/tpami.2021.3063604 | checked:2026-06-06"
    - "Zero-Reference Deep Curve Estimation (arXiv 预印本) | 2020 | cited:141 | doi:10.48550/arxiv.2001.06826 | checked:2026-06-06"
  possible_innovation_points: "奶山羊夜间微光（弱补光）场景作检测前处理；以「下游检测/行为 mAP」而非视觉质量为增强训练目标（task-driven enhancement）；白羊高反光区域的曲线约束; domain_scope=cv-夜间多模态"
  maturity: "主流（轻量低光增强代表作，奶山羊夜间需验证增强是否真提升检测）"
```

```yaml
- method_name: "EnlightenGAN（无配对低光增强 GAN）"
  task_type: "低光照图像增强（无配对对抗学习），检测前置"
  input_data: "低光 RGB 图（无需配对正常光，仅需非配对的低光/正常光两域样本）"
  output_result: "增强 RGB 图"
  core_assumption: "用全局-局部双判别器 + 自正则化（输入注意力 + 自特征保持损失）即可在无配对下学习低光→正常光映射，避免对齐数据需求"
  advantages: "无需配对数据、增强真实感强、可处理空间非均匀光照（局部判别器）、适合现场难采配对的栏舍"
  limitations: "GAN 训练不稳、可能引入伪纹理/伪影（对医学/计量级判读风险高）、增强不保证利于检测、推理比 Zero-DCE 重"
  common_baselines: "Zero-DCE、RetinexNet、CycleGAN、LIME"
  evaluation_metrics: "NIQE/无参考质量、下游 mAP/Miss Rate、用户研究"
  suitable_datasets: "自采非配对低光/正常光集、LOL、自建奶山羊夜景"
  implementation_repo: "VITA-Group/EnlightenGAN"
  representative_papers:
    - "EnlightenGAN: Deep Light Enhancement Without Paired Supervision | 2021(TIP) | cited:2384 | doi:10.1109/tip.2021.3051462 | checked:2026-06-06"
    - "EnlightenGAN (arXiv 预印本) | 2019 | cited:205 | doi:10.48550/arxiv.1906.06972 | checked:2026-06-06"
  possible_innovation_points: "栏舍非均匀灯光（局部灯下/阴影）下作增强；与 Zero-DCE 对比择优；需警惕 GAN 伪影对发情/跛行细节判读的误导（计量场景慎用）; domain_scope=cv-夜间多模态"
  maturity: "主流偏经典（无配对增强里程碑，新场景多被更轻的 Zero-DCE 系替代）"
```

```yaml
- method_name: "RetinexNet / Deep Retinex（基于 Retinex 分解的低光增强）"
  task_type: "低光照图像增强（反射-光照分解）"
  input_data: "低光 RGB 图（RetinexNet 训练用配对 LOL 数据）"
  output_result: "分解出反射图 + 光照图，调整光照后重组增强图"
  core_assumption: "图像 = 反射(reflectance) × 光照(illumination)，分别用 Decom-Net 分解、Enhance-Net 调光照即可还原正常光"
  advantages: "物理可解释（Retinex 理论）、分解便于单独调光照、对色彩恒常性好"
  limitations: "依赖配对训练数据（LOL）、分解不准会放噪、边界光晕、对极暗效果有限"
  common_baselines: "Zero-DCE、EnlightenGAN、LIME、传统 Retinex"
  evaluation_metrics: "PSNR/SSIM、下游检测 mAP、NIQE"
  suitable_datasets: "LOL、自建奶山羊夜景"
  implementation_repo: "weichen582/RetinexNet（官方）、低光增强综合库"
  representative_papers:
    - "Deep Retinex Decomposition for Low-Light Enhancement | 2018(BMVC, arXiv) | cited:238 | doi:10.48550/arxiv.1808.04560 | checked:2026-06-06"
    - "Low-light image enhancement via deep Retinex decomposition and bilateral learning | 2021 | cited:27 | doi:10.1016/j.image.2021.116466 | checked:2026-06-06"
  possible_innovation_points: "分解出的光照图可作栏舍灯光不均的度量；反射图（去光照）或更利于跨昼夜个体外观一致性；与检测联合微调; domain_scope=cv-夜间多模态"
  maturity: "主流偏经典（Retinex 系强基线；需配对数据是栏舍落地短板）"
```

```yaml
- method_name: "红外小目标检测（Infrared Small Target Detection，ACM / DNANet 系）"
  task_type: "单帧红外小弱目标检测/分割（无纹理、低信噪、点状目标）"
  input_data: "单通道红外图（目标仅几像素~几十像素，背景杂波强）"
  output_result: "小目标位置/分割 mask（多为分割式检测）"
  core_assumption: "小目标缺乏形状/纹理线索，需靠局部对比度与上下文调制；网络应保留浅层细节同时建模背景杂波（如非对称上下文调制、密集嵌套注意力）"
  advantages: "专攻极小/低对比目标、对远距离/小尺度敏感、分割式定位精"
  limitations: "面向遥感/天空均匀背景，栏舍复杂地面背景适配差；目标定义为「点状」，奶山羊近距非小目标；易受热杂波误检"
  common_baselines: "传统 Top-Hat / 局部对比度(LCM) / IPI 低秩、ACM、ALCNet、DNANet"
  evaluation_metrics: "IoU、nIoU、Pd（检测概率）、Fa（虚警率）、ROC"
  suitable_datasets: "NUAA-SIRST、NUDT-SIRST、IRSTD-1k（均遥感/天空域，无奶山羊）"
  implementation_repo: "YimianDai/open-acm（ACM）、YeRen123455/Infrared-Small-Target-Detection（DNANet）"
  representative_papers:
    - "Asymmetric Contextual Modulation for Infrared Small Target Detection | 2021(WACV) | cited:720 | doi:10.1109/wacv48630.2021.00099 | checked:2026-06-06"
    - "Dense Nested Attention Network for Infrared Small Target Detection | 2022(TIP) | cited:854 | doi:10.1109/tip.2022.3199107 | checked:2026-06-06"
    - "YOLOSR-IST: small target detection in infrared remote sensing images based on super-resolution and YOLO | 2023 | cited:157 | doi:10.1016/j.sigpro.2023.108962 | checked:2026-06-06"
  possible_innovation_points: "远距/广角栏舍俯拍中**远端羊只成小目标**时借鉴局部对比度模块；新生羊羔/远处个体的小尺度增强；一般近距奶山羊不属此范式（如实标注边界）; domain_scope=cv-夜间多模态"
  maturity: "新兴（红外小目标专门方向活跃；但与奶山羊近距场景错配，仅远端小目标可借鉴）"
```

```yaml
- method_name: "日间→夜间域适应检测（Day-to-Night Domain Adaptation）"
  task_type: "无监督/零样本域适应目标检测（跨光照域）"
  input_data: "有标注日间 RGB（源域）+ 无/少标注夜间或热成像（目标域）"
  output_result: "在夜间/热域可用的检测器（无需大量夜间标注）"
  core_assumption: "日间与夜间共享目标语义，差异主要在低层风格/光照；通过风格迁移(GAN)、特征对齐(对抗/统计)或零样本提示，可把日间标注知识迁到夜间，免去夜间重标"
  advantages: "省夜间标注成本、利用现有日间数据、零样本变体无需目标域图像"
  limitations: "风格迁移可能改变目标几何/引入伪影、域差过大（RGB→LWIR 跨模态）效果有限、对齐不当反伤性能、评测需真实夜间标注"
  common_baselines: "源域直推(no adaptation)、CycleGAN 风格迁移+检测、对抗特征对齐(DA-Faster)、teacher-student 自训练"
  evaluation_metrics: "目标域 mAP/Miss Rate、域差下降量、与全监督上界差距"
  suitable_datasets: "BDD100K(day/night)、KAIST、Cityscapes→Nighttime、自建奶山羊昼夜集"
  implementation_repo: "论文官方仓库（Boosting Day-Night DA）、open-mmlab 域适应检测扩展"
  representative_papers:
    - "Boosting Object Detection with Zero-Shot Day-Night Domain Adaptation | 2024(CVPR) | cited:51 | doi:10.1109/cvpr52733.2024.01204 | checked:2026-06-06"
    - "GAN-Based Day-to-Night Image Style Transfer for Nighttime Vehicle Detection | 2020(T-ITS) | cited:162 | doi:10.1109/tits.2019.2961679 | checked:2026-06-06"
    - "Unsupervised thermal-to-visible domain adaptation method for pedestrian detection | 2021 | cited:27 | doi:10.1016/j.patrec.2021.11.024 | checked:2026-06-06"
  possible_innovation_points: "用大量日间奶山羊标注迁到夜间 NIR/IR，免夜间重标；白羊昼夜外观差异作域差建模对象；昼夜个体外观一致性约束辅助跨时段 re-id; domain_scope=cv-夜间多模态"
  maturity: "新兴（域适应检测活跃；RGB→热成像跨模态域适应仍偏研究期）"
```

### 二、RGB-IR / 多光谱多模态融合检测

```yaml
- method_name: "多光谱行人检测基准与 Halfway Fusion（KAIST 系奠基工作）"
  task_type: "RGB-热成像双模态目标检测（特征级融合基线）"
  input_data: "配准的 RGB + 热成像(LWIR) 图像对（同视角对齐）"
  output_result: "类别 + bbox（融合两模态特征后预测）"
  core_assumption: "白天 RGB 信息丰、夜间热成像更可靠，两模态互补；在网络中段(halfway)拼接两路特征比早/晚融合更优，统一检测器即可学到互补性"
  advantages: "昼夜全天候鲁棒、奠定 KAIST 基准与融合范式、特征级融合实现简单、强基线"
  limitations: "需像素级配准（错配致性能崩）、固定融合不随光照自适应、模态不平衡（某模态噪声大时拖累）、KAIST 标注有噪"
  common_baselines: "RGB-only、Thermal-only、早融合(input concat)、晚融合(决策)、Halfway Fusion"
  evaluation_metrics: "Miss Rate (MR, log-average, KAIST 标准)、MR-FPPI 曲线、mAP、分昼/夜/全天评测"
  suitable_datasets: "KAIST Multispectral、CVC-14、FLIR Aligned、LLVIP（均行人/交通，无奶山羊）"
  implementation_repo: "SoonminHwang/rgbt-ped-detection（KAIST 官方）、多光谱检测复现仓库"
  representative_papers:
    - "Multispectral pedestrian detection: Benchmark dataset and baseline | 2015(CVPR) | cited:1121 | doi:10.1109/cvpr.2015.7298706 | checked:2026-06-06"
    - "Fusion of multispectral data through illumination-aware deep neural networks for pedestrian detection | 2018 | cited:325 | doi:10.1016/j.inffus.2018.11.017 | checked:2026-06-06"
  possible_innovation_points: "栏舍 RGB+热成像双相机昼夜全天检测奶山羊；Miss Rate 作奶山羊夜间漏检的核心指标（漏检=漏报发情/跛行）；配准方案适配栏舍固定机位; domain_scope=cv-夜间多模态"
  maturity: "经典（多光谱检测奠基，融合范式仍是后续工作起点）"
```

```yaml
- method_name: "Illumination-aware Faster R-CNN（光照感知自适应融合）"
  task_type: "RGB-热成像双模态检测（光照门控加权融合）"
  input_data: "配准 RGB + 热成像图像对"
  output_result: "类别 + bbox，融合权重随场景光照动态调整"
  core_assumption: "两模态可靠性随光照变化（白天信 RGB、夜间信热），用一个光照估计子网络预测白天/夜晚置信度，据此对两路检测结果/特征加权，比固定融合更鲁棒"
  advantages: "显式建模昼夜可靠性差异、对光照突变鲁棒、可解释（输出光照权重）、即插于双流检测器"
  limitations: "光照子网需额外标注/监督、权重在黄昏/灯下混合光易误估、仍需配准、计算量翻倍"
  common_baselines: "Halfway Fusion、RGB-only、Thermal-only、固定平均融合"
  evaluation_metrics: "Miss Rate（分昼/夜/全天）、MR-FPPI、mAP"
  suitable_datasets: "KAIST、CVC-14、自建奶山羊昼夜双模态集"
  implementation_repo: "论文复现仓库（IATDNN / IAF R-CNN）、open-mmlab 多模态扩展"
  representative_papers:
    - "Illumination-aware faster R-CNN for robust multispectral pedestrian detection | 2018(Pattern Recognition) | cited:475 | doi:10.1016/j.patcog.2018.08.005 | checked:2026-06-06"
    - "Illumination-aware Faster R-CNN (arXiv 预印本) | 2018 | cited:20 | doi:10.48550/arxiv.1803.05347 | checked:2026-06-06"
    - "Cross-modality interactive attention network for multispectral pedestrian detection | 2018(Information Fusion) | cited:284 | doi:10.1016/j.inffus.2018.09.015 | checked:2026-06-06"
  possible_innovation_points: "栏舍灯光开关/昼夜切换的光照门控；黄昏/夜灯混合光下的奶山羊检测可靠性；光照权重可作数据质量指标驱动主动采样; domain_scope=cv-夜间多模态"
  maturity: "主流（光照自适应融合是多光谱检测主流路线之一）"
```

```yaml
- method_name: "CFT（Cross-Modality Fusion Transformer，多光谱检测）"
  task_type: "RGB-热成像双模态检测（Transformer 跨模态注意力融合）"
  input_data: "配准 RGB + 热成像图像对"
  output_result: "类别 + bbox（跨模态自注意力融合后的预测）"
  core_assumption: "卷积局部融合难捕获跨模态长程互补关系；用 Transformer 自注意力在 RGB 与热成像 token 间同时做模态内与模态间注意力，可学到更充分的互补特征"
  advantages: "跨模态长程依赖建模强、注意力自适应权衡两模态、在 KAIST/FLIR 显著超卷积融合、可插入 YOLO 类骨干"
  limitations: "Transformer 数据/算力需求大（栏舍小数据易过拟合）、仍需配准、注意力可解释性有限、边缘部署偏重"
  common_baselines: "Halfway Fusion、IAF R-CNN、CIAN、ICAFusion"
  evaluation_metrics: "Miss Rate（KAIST）、mAP（FLIR/多光谱）、MR-FPPI"
  suitable_datasets: "KAIST、FLIR Aligned、VEDAI、LLVIP"
  implementation_repo: "DocF/multispectral-object-detection（CFT 官方）"
  representative_papers:
    - "Cross-Modality Fusion Transformer for Multispectral Object Detection | 2022(SSRN/正式版) | cited:167 | doi:10.2139/ssrn.4227745 | checked:2026-06-06"
    - "Cross-Modality Fusion Transformer for Multispectral Object Detection (arXiv) | 2021 | cited:14 | doi:10.48550/arxiv.2111.00273 | checked:2026-06-06"
    - "ICAFusion: Iterative cross-attention guided feature fusion for multispectral object detection | 2023(Pattern Recognition) | cited:353 | doi:10.1016/j.patcog.2023.109913 | checked:2026-06-06"
  possible_innovation_points: "跨模态注意力做奶山羊 RGB-热成像融合；小数据下用预训练+轻量化适配；注意力图可定位「哪模态在该羊只起主导」辅助可靠性评估; domain_scope=cv-夜间多模态"
  maturity: "新兴（Transformer 跨模态融合当前热点，需解决小数据/部署）"
```

```yaml
- method_name: "ProbEn（Probabilistic Ensembling 概率融合，决策级）"
  task_type: "多模态检测的决策级概率融合（后融合）"
  input_data: "各单模态检测器（RGB 检测器 + 热成像检测器）的独立输出（框 + 类别后验）"
  output_result: "融合后的类别后验与框（贝叶斯式合并多模态检测结果）"
  core_assumption: "在条件独立假设下，多模态检测结果可用贝叶斯规则做概率级融合（后验相乘/几何平均 + 框融合），无需联合训练即可超过特征级融合，且对缺失模态天然鲁棒"
  advantages: "无需重训/无需配准到像素级（决策级）、可融合异构/异步模态、缺模态可降级运行、简单且强、对模态不平衡鲁棒"
  limitations: "条件独立假设不总成立、依赖单模态检测器质量、需校准的概率输出（未校准则融合偏差）、框对齐仍需空间一致"
  common_baselines: "特征级融合(Halfway/CFT)、score averaging、NMS 合并、单模态"
  evaluation_metrics: "Miss Rate、mAP、缺模态鲁棒性测试、概率校准(ECE)"
  suitable_datasets: "KAIST、FLIR、自建奶山羊多模态集"
  implementation_repo: "Jamie725/Multimodal-Object-Detection-via-Probabilistic-Ensembling"
  representative_papers:
    - "Multimodal Object Detection via Probabilistic Ensembling | 2022(ECCV) | cited:187 | doi:10.1007/978-3-031-20077-9_9 | checked:2026-06-06"
    - "Multimodal Object Detection via Probabilistic Ensembling (arXiv) | 2021 | cited:5 | doi:10.48550/arxiv.2104.02904 | checked:2026-06-06"
  possible_innovation_points: "栏舍 RGB/热成像两路独立检测器概率融合，**夜间热成像失效或 RGB 失效时自动降级**；概率校准后的后验可直接传入级联下游缓解误差累积（与第三类卡呼应）; domain_scope=cv-夜间多模态"
  maturity: "新兴（决策级概率融合简单强，缺模态鲁棒，契合栏舍多模态降级需求）"
```

```yaml
- method_name: "不确定性引导跨模态融合（Uncertainty-Guided Cross-Modal Learning）"
  task_type: "RGB-热成像双模态检测（按不确定性加权融合）"
  input_data: "配准 RGB + 热成像图像对"
  output_result: "类别 + bbox，各模态贡献按其预测不确定性自适应加权"
  core_assumption: "模态可靠性应由其**预测不确定性**而非仅光照决定；估计每模态的不确定性并据此加权（高不确定性模态降权），可同时缓解模态不平衡与标注噪声"
  advantages: "比纯光照门控更细粒度（逐样本/逐区域）、对标注噪声与模态退化鲁棒、不确定性可外传给下游级联"
  limitations: "不确定性估计本身难校准、训练复杂、需配准、计算开销"
  common_baselines: "IAF R-CNN、CFT、ProbEn、固定融合"
  evaluation_metrics: "Miss Rate、mAP、不确定性校准(ECE)、模态退化鲁棒性"
  suitable_datasets: "KAIST、CVC-14、FLIR、自建奶山羊集"
  implementation_repo: "论文官方仓库（Uncertainty-Guided Cross-Modal，部分待核查）"
  representative_papers:
    - "Uncertainty-Guided Cross-Modal Learning for Robust Multispectral Pedestrian Detection | 2021(TCSVT) | cited:121 | doi:10.1109/tcsvt.2021.3076466 | checked:2026-06-06"
    - "Robust Multispectral Pedestrian Detection via Uncertainty-Aware Cross-Modal Learning | 2021(ACCV) | cited:7 | doi:10.1007/978-3-030-67832-6_32 | checked:2026-06-06"
    - "Improving Multispectral Pedestrian Detection by Addressing Modality Imbalance Problems | 2020(ECCV) | cited:263 | doi:10.1007/978-3-030-58523-5_46 | checked:2026-06-06"
  possible_innovation_points: "把模态不确定性作为级联误差传播的「显式信号」传给跟踪/行为模块；奶山羊夜间某模态退化时自动降权；不确定性高的检测触发人工复核（主动学习闭环）; domain_scope=cv-夜间多模态"
  maturity: "新兴（不确定性引导融合是缓解级联误差的关键桥梁，研究活跃）"
```

```yaml
- method_name: "可见光-热成像配准（RGB-Thermal Registration / Alignment）"
  task_type: "多模态图像配准（融合检测的前置必需步骤）"
  input_data: "非对齐的 RGB 与热成像图像对（不同相机内外参、分辨率、视场）"
  output_result: "像素级/区域级对齐的 RGB-热成像对（或对齐变换矩阵）"
  core_assumption: "两模态成像几何可由单应/仿射或可学习配准场关联；跨模态相似性（梯度/互信息/边缘）或深度特征可驱动对齐，使融合检测能逐像素对应"
  advantages: "是特征级融合的前提（CFT/Halfway 均假设已配准）、标定式（同轴/双目）一次标定长期有效、提升融合上限"
  limitations: "跨模态外观差异大致配准难、动态视差（近距运动目标）残差、热-可见无共同纹理时基于内容的配准失败、CVC-14/部分数据天然弱配准"
  common_baselines: "棋盘格标定单应、互信息配准、CrossRAFT/可学习跨模态配准、AlignFusion"
  evaluation_metrics: "配准误差(像素 RMSE)、配准后下游 mAP/Miss Rate 提升、对错配的鲁棒性"
  suitable_datasets: "KAIST(对齐)、CVC-14(弱对齐)、LLVIP、自建奶山羊双相机集"
  implementation_repo: "标定用 OpenCV；可学习配准见多光谱检测仓库的 align 模块（部分待核查）"
  representative_papers:
    - "Improving Multispectral Pedestrian Detection by Addressing Modality Imbalance Problems | 2020(ECCV) | cited:263 | doi:10.1007/978-3-030-58523-5_46 | checked:2026-06-06"
    - "Cross-modality interactive attention network for multispectral pedestrian detection | 2018(Information Fusion) | cited:284 | doi:10.1016/j.inffus.2018.09.015 | checked:2026-06-06"
  possible_innovation_points: "栏舍固定机位 RGB+热成像同轴/双目一次标定方案；对运动奶山羊近距视差的弱配准鲁棒融合（用 ProbEn 决策级规避像素配准）；配准残差作融合可靠性指标; domain_scope=cv-夜间多模态"
  maturity: "主流（配准是多模态落地的工程瓶颈；决策级融合可部分绕过）"
```

### 三、级联误差传播 / 端到端联合（检测→跟踪→行为）

```yaml
- method_name: "JDE / FairMOT（联合检测与 re-id 嵌入，one-shot MOT）"
  task_type: "联合检测+跟踪（一个网络同时输出检测框与 re-id 嵌入）"
  input_data: "视频帧序列（RGB）"
  output_result: "每帧检测框 + 关联用 re-id 嵌入 → 跨帧轨迹"
  core_assumption: "检测与 re-id 可共享骨干一次前向输出（避免检测→裁剪→re-id 两阶段的误差与延迟）；FairMOT 指出二者应「公平」对待（anchor-free + 低维嵌入 + 同分辨率特征）以免检测主导损害 re-id"
  advantages: "一阶段省去级联裁剪步骤（减一处误差源）、实时、检测与关联端到端协同、FairMOT 显著降 ID switch"
  limitations: "检测与 re-id 仍存任务冲突、同品种白羊外观相似致 re-id 嵌入区分度低、密集遮挡 ID switch、本质仍「先检测后关联」非完全端到端"
  common_baselines: "SORT、DeepSORT、Tracktor、ByteTrack（见 db03 检测跟踪卡）"
  evaluation_metrics: "MOTA、IDF1、ID switch、HOTA、FPS"
  suitable_datasets: "MOT16/17/20、自建奶山羊 MOT（无现成）"
  implementation_repo: "Zhongdao/Towards-Realtime-MOT（JDE）、ifzhang/FairMOT"
  representative_papers:
    - "FairMOT: On the Fairness of Detection and Re-identification in Multiple Object Tracking | 2021(IJCV) | cited:1475 | doi:10.1007/s11263-021-01513-4 | checked:2026-06-06"
  possible_innovation_points: "联合范式减少检测→跟踪级联误差；白羊 re-id 弱→以运动/位置为主、re-id 为辅；夜间红外下嵌入退化的降权策略（与本文件第二类不确定性卡结合）; domain_scope=cv-夜间多模态"
  maturity: "主流（one-shot MOT 代表；奶山羊 re-id 难是核心适配挑战，db03 跟踪卡已侧重，此处只强调「联合」减级联思想）"
```

```yaml
- method_name: "TrackFormer / MOTR（端到端 Transformer 联合检测跟踪）"
  task_type: "端到端多目标跟踪（track query 自回归，无显式关联步骤）"
  input_data: "视频帧序列"
  output_result: "轨迹（track query 跨帧传递，直接输出带身份的检测）"
  core_assumption: "把跟踪建模为 track query 在帧间的自回归传播——检测 query 发现新目标、track query 延续已有目标，关联由注意力隐式完成，**无需手工 NMS/匈牙利关联**，真正端到端"
  advantages: "检测与关联在一个 set-prediction 框架内联合优化（消除显式关联级误差源）、长时序时空注意力、无需运动模型/re-id 模块"
  limitations: "数据/算力需求大、训练慢难收敛、密集场景 query 冲突、长视频 query 漂移、边缘部署重、小数据（栏舍）易过拟合"
  common_baselines: "FairMOT、ByteTrack、CenterTrack、Tracktor"
  evaluation_metrics: "MOTA、IDF1、HOTA、ID switch"
  suitable_datasets: "MOT17/20、DanceTrack、BDD100K MOT"
  implementation_repo: "timmeinhardt/trackformer、megvii-research/MOTR"
  representative_papers:
    - "TrackFormer: Multi-Object Tracking with Transformers | 2022(CVPR) | cited:941 | doi:10.1109/cvpr52688.2022.00864 | checked:2026-06-06"
    - "Looking Beyond Two Frames: End-to-End Multi-Object Tracking Using Spatial and Temporal Transformers | 2022(TPAMI) | cited:64 | doi:10.1109/tpami.2022.3213073 | checked:2026-06-06"
  possible_innovation_points: "端到端消除检测→跟踪关联级误差，利于下游行为稳定；track query 可延伸携带行为状态做检测-跟踪-行为三级联合（创新空白）；栏舍小数据需大规模预训练+适配; domain_scope=cv-夜间多模态"
  maturity: "新兴（端到端 MOT 前沿；落地需解决数据与部署，奶山羊场景空白）"
```

```yaml
- method_name: "TransVOD（端到端视频目标检测，时空 Transformer）"
  task_type: "端到端视频目标检测（跨帧时空聚合，无后处理串联）"
  input_data: "视频帧序列（多帧联合输入）"
  output_result: "每帧检测（利用相邻帧时空信息增强当前帧，缓解单帧漏检/模糊）"
  core_assumption: "单帧检测在运动模糊/遮挡/失焦帧上不稳；用时空 Transformer 跨帧聚合特征与 query，可让难帧借助邻帧线索，端到端无需逐帧 NMS+后链接"
  advantages: "利用时序冗余降低单帧漏检（级联第一级误差源）、端到端、对运动模糊/短遮挡鲁棒"
  limitations: "多帧输入显存/算力大、实时性弱于单帧、长程时序受限、栏舍小数据训练难"
  common_baselines: "单帧检测器逐帧、FGFA、SELSA、MEGA(特征聚合 VOD)"
  evaluation_metrics: "mAP（ImageNet VID）、按运动速度分组 mAP(slow/medium/fast)"
  suitable_datasets: "ImageNet VID、自建奶山羊视频检测集"
  implementation_repo: "SJTU-LuHe/TransVOD"
  representative_papers:
    - "TransVOD: End-to-End Video Object Detection With Spatial-Temporal Transformers | 2022(TPAMI) | cited:181 | doi:10.1109/tpami.2022.3223955 | checked:2026-06-06"
    - "End-to-End Video Object Detection with Spatial-Temporal Transformers | 2021(ACM MM) | cited:102 | doi:10.1145/3474085.3475285 | checked:2026-06-06"
  possible_innovation_points: "用时序聚合稳住夜间红外单帧难检的奶山羊（运动模糊/低对比），从源头减少级联误差；夜间低帧率/补光闪烁下的时序鲁棒聚合; domain_scope=cv-夜间多模态"
  maturity: "新兴（端到端 VOD 把时序前置到检测，利于级联稳健性）"
```

```yaml
- method_name: "ACT / 端到端时空行为检测（Action Tubelet + Tubelet Transformer）"
  task_type: "端到端时空动作检测（同时定位人/物并识别行为，tube 级）"
  input_data: "视频片段（连续帧）"
  output_result: "行为管(action tube)：随时间的框序列 + 行为类别（检测与行为一体输出）"
  core_assumption: "行为检测不应「先检测人再分类行为」串联，而应在 tubelet（短时框序列）上联合回归框与行为，时序上下文同时服务定位与分类，减少级联误差"
  advantages: "检测与行为联合（合并两级，减误差累积）、tubelet 利用短时运动、时空一致性强"
  limitations: "tube 标注昂贵、长行为需链接 tubelet、密集多目标 tube 冲突、计算重"
  common_baselines: "逐帧检测+行为分类(串联)、SlowFast+ROI、I3D+检测（见 db03 行为卡）"
  evaluation_metrics: "frame-mAP、video-mAP（@不同 tube IoU 阈值）"
  suitable_datasets: "UCF101-24、JHMDB、AVA（均人类行为，无奶山羊）"
  implementation_repo: "vkalogeiton/caffe-act（ACT 原始）、后续 PyTorch tubelet transformer 复现"
  representative_papers:
    - "Action Tubelet Detector for Spatio-Temporal Action Localization | 2017(ICCV) | cited:341 | doi:10.1109/iccv.2017.472 | checked:2026-06-06"
    - "An Efficient Spatio-Temporal Pyramid Transformer for Action Detection | 2022(ECCV) | cited:31 | doi:10.1007/978-3-031-19830-4_21 | checked:2026-06-06"
    - "STD-TR: End-to-End Spatio-Temporal Action Detection with Transformers | 2021(CAC) | cited:7 | doi:10.1109/cac53003.2021.9727692 | checked:2026-06-06"
  possible_innovation_points: "把奶山羊检测+发情/跛行行为合到 tube 级联合学习，绕过「检测→跟踪→行为」逐级误差；爬跨/采食 tube 的时空联合定位；夜间红外 tube 检测; domain_scope=cv-夜间多模态"
  maturity: "新兴（端到端时空行为检测；奶山羊细粒度行为为空白，是合并级联的直接路径）"
```

```yaml
- method_name: "检测不确定性建模（MC-Dropout / Deep Ensembles / 概率检测）"
  task_type: "目标检测的不确定性量化（为级联误差传播提供置信信号）"
  input_data: "检测器输入（单帧/多模态），输出附不确定性"
  output_result: "检测框 + 类别 + **校准的不确定性**（认知不确定性 epistemic + 偶然不确定性 aleatoric）"
  core_assumption: "标准检测的 softmax 置信度未校准、不反映真实可靠性；通过 MC-Dropout（多次随机前向）、深度集成或显式概率输出，可估计可信的不确定性，供下游决策与融合使用"
  advantages: "给级联下游提供「该检测有多可信」、支持选择性预测/人工复核、改善多模态融合权重、识别分布外样本"
  limitations: "MC-Dropout/集成推理成本数倍、不确定性需校准否则误导、定位不确定性建模仍不成熟、增加系统复杂度"
  common_baselines: "原始 softmax 置信、温度缩放校准、MC-Dropout、Deep Ensembles、概率检测(高斯/证据)"
  evaluation_metrics: "ECE(期望校准误差)、PAvPU、mAP、不确定性-误差相关性、OOD 检测 AUROC"
  suitable_datasets: "COCO/KITTI(概率检测评测)、自建奶山羊集做校准评估"
  implementation_repo: "概率检测综述配套代码、yaringal/DropoutUncertaintyExps（MC-Dropout 原理）"
  representative_papers:
    - "A Review and Comparative Study on Probabilistic Object Detection in Autonomous Driving | 2021(T-ITS) | cited:303 | doi:10.1109/tits.2021.3096854 | checked:2026-06-06"
    - "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning | 2015(arXiv/ICML) | cited:4159 | doi:10.48550/arxiv.1506.02142 | checked:2026-06-06"
  possible_innovation_points: "**缓解级联误差的核心工具**——检测不确定性高时降低其对发情/跛行告警的权重、触发复核；夜间红外检测不确定性普遍升高，可据此自动切换多模态/人工; domain_scope=cv-夜间多模态"
  maturity: "主流（不确定性量化方法成熟；用于级联误差缓解的系统化应用是空白）"
```

```yaml
- method_name: "流水线不确定性/误差传播建模（Uncertainty Propagation across Pipeline）"
  task_type: "多级感知流水线（检测→跟踪→行为）的误差累积分析与缓解（系统级方法论）"
  input_data: "各级模块的输出 + 不确定性（检测置信、跟踪关联不确定性、行为分类后验）"
  output_result: "末级决策（发情/跛行告警）+ 端到端不确定性，含各级误差贡献归因"
  core_assumption: "级联系统末级可靠性由各级误差**联合**决定，前级错误（漏检/ID switch）会沿流水线传播并被后级放大；显式传播每级不确定性（而非只传 hard 决策）并在末级联合推断，可抑制累积误差"
  advantages: "直面「检测→跟踪→行为四级误差累积」这一审计确认空白、提供端到端可靠性度量、支持薄弱环节归因、可指导联合优化或人工兜底"
  limitations: "该方向在动物行为/畜牧领域**几乎无现成方法**（多源自自动驾驶感知-决策链）、跨级不确定性建模与校准难、需各级均输出校准概率、端到端联合训练数据稀缺"
  common_baselines: "hard-decision 级联（各级只传 top-1，无不确定性传播）、独立优化各级、端到端联合训练"
  evaluation_metrics: "末级告警 Precision/Recall/F1、误报率(发情/跛行)、各级误差贡献分解、端到端校准(ECE)、与单级误差的相关分析"
  suitable_datasets: "无专用集；需自建奶山羊「检测+跟踪+行为」全链路标注序列（如实说明）"
  implementation_repo: "待核查（畜牧领域无现成端到端流水线误差传播仓库；可借鉴自动驾驶感知不确定性传播实现）"
  representative_papers:
    - "A review of Link-level uncertainty in the perception-decision-control pipeline of connected and autonomous vehicles | 2025 | cited:1 | doi:10.1177/09544070251390424 | checked:2026-06-06"
    - "A Review and Comparative Study on Probabilistic Object Detection in Autonomous Driving | 2021(T-ITS) | cited:303 | doi:10.1109/tits.2021.3096854 | checked:2026-06-06"
  possible_innovation_points: "**本文件核心创新点**——为奶山羊「检测→跟踪→行为」四级流水线建立不确定性传播框架：前级 soft 信息（不确定性/多假设）下传而非 hard 决策；夜间红外/单模态退化时的端到端可靠性评估；告警阈值随累积不确定性自适应，降低误报发情/跛行；薄弱级归因指导数据补采; domain_scope=cv-夜间多模态"
  maturity: "新兴（畜牧行为分析中为空白方向，方法论需自驾感知链迁移+自建数据，创新空间大）"
```



