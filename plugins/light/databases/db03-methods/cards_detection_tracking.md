# db03 方法卡 — 目标检测 + 多目标跟踪（cards_detection_tracking.md）

> 每张卡注明 maturity（经典|主流|新兴|过时|不推荐），避免提出落后方案。受版权全文不收录，仅元数据与开源链接。
> representative_papers 的标题/年份/被引/DOI 来自 OpenAlex 真实 curl 结果（https://api.openalex.org，mailto 礼貌池），查询日期 **2026-06-06**；被引数随时间变动。
> 同一论文常有会议正式版与 arXiv 预印本两条 OpenAlex 记录，被引数不同，已分别标注；优先取正式版。
> 排名/成熟度判断为人工标注。查不到的字段写「待核查」。
> **付费墙说明**：本卡不涉及期刊 IF/SJR；如需期刊指标见 db01/db02，免费源不可得处用 OpenAlex summary_stats 替代。

字段 schema 同 db03：`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`

## 奶山羊 / 家畜场景适配总览（贯穿各卡 limitations / innovation_points）

针对【奶山羊 / 家畜栏舍】实拍特点，给出方法选型导向（结论性，细节见各卡）：
- **栏舍遮挡重、密集个体**：偏好强关联跟踪器（ByteTrack / OC-SORT / BoT-SORT）+ 高 recall 检测器；低置信框二次关联（ByteTrack 思想）对遮挡羊只尤其有效。
- **个体外观高度相似（re-id 难）**：纯外观 re-id（DeepSORT / FairMOT / StrongSORT）在同品种白色奶山羊上 embedding 区分度低，易 ID switch；建议以运动/位置线索为主（OC-SORT 的 observation-centric 思想、ByteTrack 的 IoU 关联），re-id 作弱辅助或改用部位/花纹/耳标特征。
- **俯拍视角（top-down）**：目标尺度变化小但形变与朝向多样，anchor-free（FCOS / CenterNet / YOLOX）与旋转框/关键点扩展更友好；COCO 预训练的水平框范式需重训。
- **夜间红外 / 低光**：RGB 预训练权重域差大，需红外微调或多模态；Transformer 检测器（DINO/RT-DETR）数据需求大，红外小数据下 YOLO 系迁移更稳。
- **实时 + 边缘部署（场端盒子）**：YOLOv8/v11、RT-DETR、ByteTrack 这类高 FPS、易导出 ONNX/TensorRT 的组合最实际；两阶段（Faster/Cascade R-CNN）与重型 DETR 一般不上边缘。
- **无奶山羊专用公开检测/MOT 数据集**：据查证，COCO/MOT17/MOT20/DanceTrack 均为通用/行人/舞者域，**不含奶山羊**；动物领域多为 AP-10K（姿态）、Animal Kingdom 等，奶山羊专用检测+跟踪基准稀缺，需自建并标注（如实说明，不编造）。

## 方法卡

### 一、目标检测（Object Detection）

```yaml
- method_name: Faster R-CNN（两阶段，RPN）
  task_type: 目标检测（two-stage anchor-based）
  input_data: 单张 RGB 图像
  output_result: 类别 + 边界框（bbox），含 RPN 候选框再分类回归
  core_assumption: 用 Region Proposal Network 在共享特征图上生成候选框，二阶段精修，proposal+RoI 对齐能换取高定位精度
  advantages: 精度高、定位准、对小目标较友好（高分辨率特征+RoIAlign）、生态成熟、强基线
  limitations: 两阶段慢、难做边缘实时、anchor 超参敏感、NMS 后处理
  common_baselines: Fast R-CNN、SSD、YOLO 系、RetinaNet
  evaluation_metrics: mAP@[.5:.95]、AP50、AP_small/medium/large、FPS
  suitable_datasets: COCO、PASCAL VOC、自建奶山羊检测集（需自标，无现成）
  implementation_repo: open-mmlab/mmdetection、facebookresearch/detectron2、torchvision.models.detection
  representative_papers:
    - "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | 2016(TPAMI) | cited:53939 | doi:10.1109/tpami.2016.2577031 | checked:2026-06-06"
    - "Faster R-CNN (arXiv 预印本) | 2015 | cited:18238 | doi:10.48550/arxiv.1506.01497 | checked:2026-06-06"
  possible_innovation_points: 奶山羊俯拍密集场景作高精度离线标注/伪标签生成器（非实时）；小目标羊羔用 FPN+高分辨 RoIAlign；红外域微调 backbone; domain_scope=cv-检测跟踪
  maturity: 经典（仍是强基线与精度上界参考，实时部署已被单阶段/DETR 取代）
```

```yaml
- method_name: SSD（Single Shot MultiBox Detector）
  task_type: 目标检测（one-stage anchor-based）
  input_data: 单张 RGB 图像（固定输入如 300/512）
  output_result: 类别 + bbox（多尺度特征图直接预测）
  core_assumption: 在多个尺度特征图上设置默认框(default box)一次前向直接回归分类，去掉 proposal 阶段换速度
  advantages: 速度快、结构简单、多尺度检测、易部署
  limitations: 小目标弱（浅层语义不足）、default box 设计依赖经验、精度低于现代检测器
  common_baselines: YOLOv1/v2、Faster R-CNN、RetinaNet
  evaluation_metrics: mAP、AP50、FPS
  suitable_datasets: COCO、PASCAL VOC
  implementation_repo: open-mmlab/mmdetection、weiliu89/caffe(ssd 原始)、torchvision(ssd300_vgg16)
  representative_papers:
    - "SSD: Single Shot MultiBox Detector | 2016(ECCV) | cited:20846 | doi:10.1007/978-3-319-46448-0_2 | checked:2026-06-06"
  possible_innovation_points: 历史基线，奶山羊场景不推荐新用；可作教学/对比项; domain_scope=cv-检测跟踪
  maturity: 过时（被 YOLO 现代版与 anchor-free 取代，仅作对比基线）
```

```yaml
- method_name: RetinaNet（Focal Loss）
  task_type: 目标检测（one-stage anchor-based）
  input_data: 单张 RGB 图像
  output_result: 类别 + bbox（FPN 多尺度 + 密集预测）
  core_assumption: 单阶段精度低的根因是前景/背景极端类别不均衡，Focal Loss 降低易分负样本权重即可让单阶段达到两阶段精度
  advantages: 单阶段下精度高、FPN 多尺度强、Focal Loss 已成通用组件
  limitations: anchor 设计与正负样本匹配仍需调、速度不及最新 YOLO、密集遮挡下重叠框难
  common_baselines: SSD、Faster R-CNN、FCOS、YOLO 系
  evaluation_metrics: mAP@[.5:.95]、AP50、FPS
  suitable_datasets: COCO、PASCAL VOC
  implementation_repo: open-mmlab/mmdetection、facebookresearch/detectron2、torchvision(retinanet)
  representative_papers:
    - "Focal Loss for Dense Object Detection | 2017(ICCV) | cited:25515 | doi:10.1109/iccv.2017.324 | checked:2026-06-06"
    - "Focal Loss for Dense Object Detection | 2018(TPAMI 扩展) | cited:9532 | doi:10.1109/tpami.2018.2858826 | checked:2026-06-06"
  possible_innovation_points: Focal Loss 直接迁移到奶山羊密集栏舍缓解类别/难例不均衡；红外小目标羊羔加权; domain_scope=cv-检测跟踪
  maturity: 主流偏经典（Focal Loss 仍广用；RetinaNet 本体作强基线，已非首选 SOTA）
```

```yaml
- method_name: YOLOv3
  task_type: 目标检测（one-stage anchor-based）
  input_data: 单张 RGB 图像
  output_result: 类别 + bbox（三尺度预测）
  core_assumption: Darknet-53 + 多尺度预测 + 维度聚类 anchor，单网络一次前向兼顾速度与精度
  advantages: 速度快、工程成熟、易部署、小目标较前代改善（多尺度）
  limitations: 精度低于现代版、anchor 依赖、密集遮挡弱
  common_baselines: SSD、RetinaNet、YOLOv2
  evaluation_metrics: mAP、AP50、FPS
  suitable_datasets: COCO、PASCAL VOC
  implementation_repo: AlexeyAB/darknet、ultralytics(早期)、open-mmlab/mmdetection(yolov3)
  representative_papers:
    - "YOLOv3: An Incremental Improvement | 2018(arXiv 技术报告) | cited:5887 | doi:10.48550/arxiv.1804.02767 | checked:2026-06-06"
  possible_innovation_points: 历史基线，奶山羊新项目建议直接用 v8/v11；保留作轻量对比; domain_scope=cv-检测跟踪
  maturity: 过时（被 v5/v8/v11 取代，仅基线/教学）
```

```yaml
- method_name: YOLOv5（Ultralytics）
  task_type: 目标检测（one-stage anchor-based）
  input_data: 单张 RGB 图像
  output_result: 类别 + bbox（n/s/m/l/x 多尺寸）
  core_assumption: 工程化集大成——Mosaic 增广、auto-anchor、CSP backbone + PANet，PyTorch 实现易训练易导出
  advantages: 训练/部署极成熟、文档与社区强、ONNX/TensorRT 导出顺、速度精度平衡好、边缘友好
  limitations: 无正式论文（仅代码与 Zenodo release）、anchor-based、学术引用规范性弱
  common_baselines: YOLOv3/v4、YOLOX、PP-YOLO
  evaluation_metrics: mAP@[.5:.95]、AP50、FPS、参数量
  suitable_datasets: COCO、自建奶山羊集（迁移学习友好）
  implementation_repo: ultralytics/yolov5
  representative_papers:
    - "ultralytics/yolov5: v5.0 - YOLOv5-P6 1280 models 等 (Zenodo 软件发布记录) | 2021 | cited:390 | doi:10.5281/zenodo.4679653 | checked:2026-06-06"
    - "ultralytics/yolov5: v3.1 (Zenodo 软件发布) | 2020 | cited:507 | doi:10.5281/zenodo.4154370 | checked:2026-06-06"
  possible_innovation_points: 奶山羊小数据迁移训练首选之一；P6 大输入利于俯拍小目标；红外微调；与 ByteTrack 串联做计数/行为; domain_scope=cv-检测跟踪
  maturity: 主流（工业部署广泛；学术上 v8/v11 更新，但 v5 仍稳）
```

```yaml
- method_name: YOLOv8（Ultralytics）
  task_type: 目标检测 / 分割 / 姿态 / 跟踪一体（anchor-free）
  input_data: 单张 RGB 图像（或视频流）
  output_result: 类别 + bbox（可选 mask/关键点）
  core_assumption: anchor-free + decoupled head + 任务统一框架，工程化进一步提升精度速度比
  advantages: anchor-free 省调参、检测/分割/姿态/MOT 一体、API 极易用、导出与边缘部署成熟、内置跟踪(ByteTrack/BoT-SORT)
  limitations: 仍为非正式论文体系、Transformer 类全局建模弱、密集重叠仍靠 NMS
  common_baselines: YOLOv5、YOLOX、YOLOv7、RT-DETR
  evaluation_metrics: mAP@[.5:.95]、AP50、FPS、mask AP、pose mAP
  suitable_datasets: COCO、自建奶山羊集
  implementation_repo: ultralytics/ultralytics
  representative_papers:
    - "YOLOv8: A Novel Object Detection Algorithm with Enhanced Performance and Robustness | 2024 | cited:1506 | doi:10.1109/adics58448.2024.10533619 [注：第三方评测/应用论文，非官方原始发布；官方仅代码] | checked:2026-06-06"
    - "UAV-YOLOv8: Small-Object-Detection Model Based on Improved YOLOv8 for UAV | 2023 | cited:841 | doi:10.3390/s23167190 [小目标改进代表作] | checked:2026-06-06"
  possible_innovation_points: 奶山羊场景一体化首选——检测+姿态(跛行/发情行为)+内置跟踪计数；俯拍小目标用小目标头改进(参考 UAV-YOLOv8)；红外微调; domain_scope=cv-检测跟踪
  maturity: 主流（当前工业与农牧 CV 落地最常用之一）
```

```yaml
- method_name: YOLOv11（Ultralytics, 2024）
  task_type: 目标检测 / 分割 / 姿态 / 跟踪一体（anchor-free）
  input_data: 单张 RGB 图像（或视频流）
  output_result: 类别 + bbox（可选 mask/关键点/OBB 旋转框）
  core_assumption: 在 v8 基础上改进 backbone/neck（C3k2、C2PSA 注意力），同精度下更少参数、更快
  advantages: 精度/速度/参数三优、含 OBB 旋转框（利于俯拍）、生态延续 v8、边缘友好
  limitations: 发布新、长期稳定性待验、仍无正式同行评审原始论文
  common_baselines: YOLOv8、YOLOv10、RT-DETR
  evaluation_metrics: mAP@[.5:.95]、AP50、FPS、参数量
  suitable_datasets: COCO、DOTA(OBB)、自建奶山羊集
  implementation_repo: ultralytics/ultralytics
  representative_papers:
    - "Research on object detection and recognition in remote sensing images based on YOLOv11 | 2025 | cited:141 | doi:10.1038/s41598-025-96314-x [应用代表作，非官方原始] | checked:2026-06-06"
    - "MAS-YOLOv11: Improved Underwater Object Detection Based on YOLOv11 | 2025 | cited:24 | doi:10.3390/s25113433 | checked:2026-06-06"
  possible_innovation_points: 奶山羊俯拍可用 OBB 旋转框贴合羊只朝向；轻量版上场端盒子；与跟踪串联做夜间红外计数; domain_scope=cv-检测跟踪
  maturity: 新兴主流（2024 最新稳定版，快速普及中）
```

```yaml
- method_name: YOLOX
  task_type: 目标检测（one-stage anchor-free）
  input_data: 单张 RGB 图像
  output_result: 类别 + bbox（decoupled head）
  core_assumption: 将 YOLO 转为 anchor-free + decoupled head + SimOTA 动态标签分配，去 anchor 提升精度
  advantages: anchor-free 省调参、SimOTA 标签分配优、精度速度平衡好、是 ByteTrack 默认检测器
  limitations: 社区活跃度不及 ultralytics、新版本迭代慢
  common_baselines: YOLOv5、YOLOv4、FCOS
  evaluation_metrics: mAP@[.5:.95]、AP50、FPS
  suitable_datasets: COCO、自建奶山羊集
  implementation_repo: Megvii-BaseDetection/YOLOX
  representative_papers:
    - "YOLOX: Exceeding YOLO Series in 2021 | 2021(arXiv) | cited:3016 | doi:10.48550/arxiv.2107.08430 | checked:2026-06-06"
  possible_innovation_points: 作 ByteTrack 检测前端用于奶山羊跟踪；SimOTA 缓解密集羊只标签分配；红外微调; domain_scope=cv-检测跟踪
  maturity: 主流（ByteTrack 生态常用检测器；通用检测被 v8/v11 部分替代）
```

```yaml
- method_name: DETR（DEtection TRansformer）
  task_type: 目标检测（端到端 set prediction，无 anchor/NMS）
  input_data: 单张 RGB 图像
  output_result: 固定数量 object query 的类别 + bbox（二分匹配监督）
  core_assumption: 检测=集合预测问题，用 Transformer encoder-decoder + 匈牙利匹配，去掉 anchor 与 NMS
  advantages: 端到端无 NMS、全局建模、概念简洁、密集场景免重叠框后处理
  limitations: 收敛极慢(500 epoch)、小目标弱、训练算力大、query 数固定
  common_baselines: Faster R-CNN、RetinaNet
  evaluation_metrics: mAP@[.5:.95]、AP50、AP_small、收敛 epoch
  suitable_datasets: COCO
  implementation_repo: facebookresearch/detr、open-mmlab/mmdetection
  representative_papers:
    - "End-to-End Object Detection with Transformers | 2020(ECCV) | cited:831 | doi:10.1007/978-3-030-58452-8_13 [注：DETR 原论文影响力远高，OpenAlex 该 ECCV 记录被引偏低，另有 arXiv/会议合并条目分散计数，待核查合并] | checked:2026-06-06"
  possible_innovation_points: 无 NMS 特性利于奶山羊密集遮挡(免重叠框抑制误删)；但小目标弱+收敛慢，红外小数据慎用; domain_scope=cv-检测跟踪
  maturity: 经典/奠基（开创 DETR 范式；本体已被 Deformable/DINO/RT-DETR 全面超越，少直接用）
```

```yaml
- method_name: Deformable DETR
  task_type: 目标检测（端到端，DETR 改进）
  input_data: 单张 RGB 图像
  output_result: object query 的类别 + bbox
  core_assumption: 用可变形注意力(deformable attention)只关注少量关键采样点，解决 DETR 收敛慢与小目标弱
  advantages: 收敛快10×、小目标显著改善、多尺度特征、保留端到端无 NMS
  limitations: 实现复杂、仍重于 YOLO、部署算子(deformable)对边缘不友好
  common_baselines: DETR、Faster R-CNN
  evaluation_metrics: mAP@[.5:.95]、AP_small、收敛 epoch
  suitable_datasets: COCO
  implementation_repo: fundamentalvision/Deformable-DETR、open-mmlab/mmdetection
  representative_papers:
    - "Deformable DETR: Deformable Transformers for End-to-End Object Detection | 2020(arXiv/ICLR2021) | cited:1868 | doi:10.48550/arxiv.2010.04159 | checked:2026-06-06"
  possible_innovation_points: 多尺度可变形注意力利于俯拍奶山羊尺度差异；小目标羊羔较 DETR 友好；deformable 算子部署需评估; domain_scope=cv-检测跟踪
  maturity: 主流（DETR 系实用化关键节点，后续 DINO/RT-DETR 的基础）
```

```yaml
- method_name: RT-DETR（Real-Time DETR）
  task_type: 目标检测（实时端到端，无 NMS）
  input_data: 单张 RGB 图像（或视频流）
  output_result: object query 的类别 + bbox
  core_assumption: 高效混合 encoder + 不确定性最小 query 选择，使 DETR 系首次在实时区间超越同级 YOLO 且无需 NMS
  advantages: 实时且无 NMS、精度超同级 YOLO、密集场景免 NMS 调参、已并入 ultralytics 易用
  limitations: 训练显存大于 YOLO、小数据迁移不如 YOLO 稳、边缘部署算子支持仍弱于纯卷积
  common_baselines: YOLOv8、YOLOX、DINO、Deformable DETR
  evaluation_metrics: mAP@[.5:.95]、AP50、FPS（T4/TensorRT）
  suitable_datasets: COCO、自建奶山羊集
  implementation_repo: lyuwenyu/RT-DETR（PaddlePaddle/PyTorch）、ultralytics(rtdetr)
  representative_papers:
    - "DETRs Beat YOLOs on Real-time Object Detection | 2024(CVPR) | cited:3234 | doi:10.1109/cvpr52733.2024.01605 | checked:2026-06-06"
    - "DETRs Beat YOLOs on Real-time Object Detection | 2023(arXiv) | cited:231 | doi:10.48550/arxiv.2304.08069 | checked:2026-06-06"
  possible_innovation_points: 奶山羊密集栏舍免 NMS 实时检测，缓解遮挡羊只被 NMS 误删；与 ByteTrack 串联；红外需较大数据微调; domain_scope=cv-检测跟踪
  maturity: 新兴主流（实时 DETR 代表，2024 起快速落地）
```

```yaml
- method_name: DINO（DETR with Improved DeNoising Anchor Boxes）
  task_type: 目标检测（端到端，DETR 系 SOTA）
  input_data: 单张 RGB 图像
  output_result: object query 的类别 + bbox
  core_assumption: 对比去噪训练(contrastive denoising) + 混合 query 选择 + look-forward-twice，稳定并加速 DETR 收敛、冲 SOTA
  advantages: COCO 高精度(曾 SOTA)、收敛比早期 DETR 快、anchor box 去噪稳定训练
  limitations: 训练算力大、推理重、边缘部署难、小数据迁移不友好
  common_baselines: Deformable DETR、DN-DETR、DAB-DETR
  evaluation_metrics: mAP@[.5:.95]、AP_small、收敛 epoch
  suitable_datasets: COCO、Objects365(预训练)
  implementation_repo: IDEA-Research/DINO、open-mmlab/mmdetection
  representative_papers:
    - "DINO: DETR with Improved DeNoising Anchor Boxes for End-to-End Object Detection | 2022(arXiv/ICLR2023) | cited:758 | doi:10.48550/arxiv.2203.03605 | checked:2026-06-06"
    - "Mask DINO: Towards A Unified Transformer-based Framework for Detection and Segmentation | 2023(CVPR) | cited:476 | doi:10.1109/cvpr52729.2023.00297 | checked:2026-06-06"
  possible_innovation_points: 追求奶山羊检测精度上界/离线标注时可用；去噪训练利于密集小目标；实时与边缘场景不优先; domain_scope=cv-检测跟踪
  maturity: 主流（DETR 系高精度代表；实时需求转向 RT-DETR）
```

```yaml
- method_name: Cascade R-CNN
  task_type: 目标检测（two-stage，多级精修）
  input_data: 单张 RGB 图像
  output_result: 类别 + 高质量 bbox
  core_assumption: 用递增 IoU 阈值训练级联检测头，逐级提升 proposal 质量，解决单一阈值下高 IoU 样本不足
  advantages: 高 IoU 定位精度最佳之一、对精确定位任务强、可叠加各 backbone
  limitations: 三级头更慢更重、训练成本高、不适合实时/边缘
  common_baselines: Faster R-CNN、RetinaNet
  evaluation_metrics: mAP@[.5:.95]（尤其高 IoU AP75+）、AP50
  suitable_datasets: COCO、PASCAL VOC
  implementation_repo: open-mmlab/mmdetection、facebookresearch/detectron2
  representative_papers:
    - "Cascade R-CNN: Delving Into High Quality Object Detection | 2018(CVPR) | cited:6750 | doi:10.1109/cvpr.2018.00644 | checked:2026-06-06"
    - "Cascade R-CNN (arXiv) | 2017 | cited:397 | doi:10.48550/arxiv.1712.00726 | checked:2026-06-06"
  possible_innovation_points: 奶山羊高精度离线标注/精确定位（如乳房/蹄部测量）可用；实时计数不推荐; domain_scope=cv-检测跟踪
  maturity: 主流偏经典（高精度强基线；实时场景非首选）
```

```yaml
- method_name: CenterNet（Objects as Points）
  task_type: 目标检测（anchor-free，关键点式）
  input_data: 单张 RGB 图像
  output_result: 目标中心点热力图 + 尺寸/偏移回归 → bbox（可扩展 3D/姿态）
  core_assumption: 把目标表示为中心点，用关键点热力图回归，去 anchor 去 NMS（峰值即检测）
  advantages: 简洁、无 NMS、易扩展(3D/姿态/跟踪)、速度快
  limitations: 中心重叠目标冲突、密集遮挡下中心点粘连、精度略逊现代检测器
  common_baselines: YOLOv3、RetinaNet、CornerNet
  evaluation_metrics: mAP@[.5:.95]、AP50、FPS
  suitable_datasets: COCO、PASCAL VOC
  implementation_repo: xingyizhou/CenterNet、open-mmlab/mmdetection
  representative_papers:
    - "Objects as Points | 2019(arXiv) | cited:739 | doi: (OpenAlex 无 DOI，arXiv:1904.07850，待核查 DOI) | checked:2026-06-06"
  possible_innovation_points: 中心点范式利于奶山羊计数与中心轨迹跟踪(CenterTrack)；密集遮挡羊只中心粘连需改进; domain_scope=cv-检测跟踪
  maturity: 主流偏经典（anchor-free 奠基之一；通用检测被 YOLO/DETR 系超越）
```

```yaml
- method_name: FCOS（Fully Convolutional One-Stage）
  task_type: 目标检测（anchor-free，逐像素回归）
  input_data: 单张 RGB 图像
  output_result: 类别 + bbox（逐像素回归到四边距离 + center-ness）
  core_assumption: 无需 anchor，逐特征点直接回归到边界四距，center-ness 抑制低质量远心点预测
  advantages: 全卷积简洁、去 anchor 省调参、FPN 多尺度、强基线、易扩展
  limitations: 密集重叠目标的点归属歧义、仍需 NMS、精度被 DETR 系/最新 YOLO 超越
  common_baselines: RetinaNet、CenterNet、YOLO 系
  evaluation_metrics: mAP@[.5:.95]、AP50、FPS
  suitable_datasets: COCO、PASCAL VOC
  implementation_repo: tianzhi0549/FCOS、open-mmlab/mmdetection、facebookresearch/detectron2
  representative_papers:
    - "FCOS: Fully Convolutional One-Stage Object Detection | 2019(ICCV) | cited:6063 | doi:10.1109/iccv.2019.00972 | checked:2026-06-06"
    - "FCOS (arXiv) | 2019 | cited:802 | doi:10.48550/arxiv.1904.01355 | checked:2026-06-06"
  possible_innovation_points: anchor-free 利于俯拍奶山羊多朝向；center-ness 思想可缓解栏栅边缘误检；作 anchor-free 对比基线; domain_scope=cv-检测跟踪
  maturity: 主流偏经典（anchor-free 经典强基线；非当前 SOTA）
```

### 二、多目标跟踪（Multi-Object Tracking, MOT）

```yaml
- method_name: SORT（Simple Online and Realtime Tracking）
  task_type: 多目标跟踪（MOT，tracking-by-detection，纯运动）
  input_data: 逐帧检测框序列
  output_result: 带 ID 的轨迹
  core_assumption: 卡尔曼滤波预测 + 匈牙利算法做 IoU 关联，仅靠运动即可实时跟踪
  advantages: 极快、极简、易实现、实时基线
  limitations: 无外观特征、遮挡后 ID switch 多、检测漏检即断轨
  common_baselines: IoU Tracker
  evaluation_metrics: MOTA、IDF1、ID switches、HOTA、FPS
  suitable_datasets: MOT15/16/17、MOT20
  implementation_repo: abewley/sort
  representative_papers:
    - "Simple online and realtime tracking | 2016(ICIP) | cited:3873 | doi:10.1109/icip.2016.7533003 | checked:2026-06-06"
  possible_innovation_points: 奶山羊外观相似 re-id 难时，纯运动 SORT 反而稳；但栏舍遮挡重→ID switch 多，建议升级到 OC-SORT/ByteTrack; domain_scope=cv-检测跟踪
  maturity: 经典（实时基线常青；现代多用其改进版）
```

```yaml
- method_name: DeepSORT
  task_type: 多目标跟踪（MOT，运动 + 外观 re-id）
  input_data: 逐帧检测框 + re-id 外观特征
  output_result: 带 ID 的轨迹
  core_assumption: 在 SORT 上加 CNN 外观 embedding 做级联匹配，外观+运动联合降低遮挡后 ID switch
  advantages: 遮挡后重识别优于 SORT、ID 更稳、生态成熟
  limitations: 依赖独立 re-id 模型(额外算力)、外观相似目标 re-id 失效、低质检测框拖累
  common_baselines: SORT、IoU Tracker
  evaluation_metrics: MOTA、IDF1、ID switches、HOTA、FPS
  suitable_datasets: MOT15/16/17、MOT20
  implementation_repo: nwojke/deep_sort、levan92/deep_sort_realtime
  representative_papers:
    - "Simple online and realtime tracking with a deep association metric | 2017(ICIP) | cited:4634 | doi:10.1109/icip.2017.8296962 | checked:2026-06-06"
    - "DeepSORT (arXiv) | 2017 | cited:119 | doi:10.48550/arxiv.1703.07402 | checked:2026-06-06"
  possible_innovation_points: 奶山羊同品种白色外观高度相似，通用 re-id embedding 区分度低→易误关联；建议改用花纹/耳标/部位特征训练专用 re-id，或弱化外观权重; domain_scope=cv-检测跟踪
  maturity: 经典/主流（行业广用基线；外观相似家畜场景需谨慎）
```

```yaml
- method_name: ByteTrack
  task_type: 多目标跟踪（MOT，tracking-by-detection，强关联）
  input_data: 逐帧检测框（含低分框）
  output_result: 带 ID 的轨迹
  core_assumption: 不丢弃低置信检测框——先高分框关联，再用低分框与未匹配轨迹二次关联，遮挡目标常呈低分框
  advantages: 不需 re-id 即高 IDF1/MOTA、遮挡鲁棒、极快、实现简单、可叠加任意检测器
  limitations: 仍依赖检测质量、纯运动在长时遮挡/相机运动下漂移、无外观难处理交叉
  common_baselines: SORT、DeepSORT、FairMOT
  evaluation_metrics: MOTA、IDF1、HOTA、ID switches、FPS
  suitable_datasets: MOT17、MOT20、DanceTrack
  implementation_repo: ifzhang/ByteTrack（官方）、ultralytics 内置
  representative_papers:
    - "ByteTrack: Multi-object Tracking by Associating Every Detection Box | 2022(ECCV) | cited:2018 | doi:10.1007/978-3-031-20047-2_1 | checked:2026-06-06"
    - "ByteTrack (arXiv) | 2021 | cited:105 | doi:10.48550/arxiv.2110.06864 | checked:2026-06-06"
  possible_innovation_points: 奶山羊场景强烈推荐——低分框二次关联恰好救回栏舍遮挡羊只；无需 re-id 规避外观相似难题；与 YOLOv8/v11 串联做计数; domain_scope=cv-检测跟踪
  maturity: 主流（当前 MOT 事实标准强基线，落地极广）
```

```yaml
- method_name: BoT-SORT
  task_type: 多目标跟踪（MOT，运动 + 相机补偿 + 可选 re-id）
  input_data: 逐帧检测框（可选 re-id 特征）
  output_result: 带 ID 的轨迹
  core_assumption: 在 ByteTrack 思路上加相机运动补偿(CMC) + 改进卡尔曼状态 + 融合 re-id，提升移动相机与遮挡下精度
  advantages: 相机运动补偿强、IDF1 高、re-id 可选融合、ultralytics 内置
  limitations: CMC 增加开销、re-id 在相似目标上仍弱、参数较多
  common_baselines: ByteTrack、StrongSORT、OC-SORT
  evaluation_metrics: MOTA、IDF1、HOTA、ID switches、FPS
  suitable_datasets: MOT17、MOT20、DanceTrack
  implementation_repo: NirAharon/BoT-SORT（官方）、ultralytics 内置
  representative_papers:
    - "BoT-SORT: Robust Associations Multi-Pedestrian Tracking | 2022(arXiv) | cited:309 | doi:10.48550/arxiv.2206.14651 | checked:2026-06-06"
  possible_innovation_points: 奶山羊俯拍若用云台/移动相机，CMC 补偿很有用；建议关闭/弱化 re-id（外观相似）只用运动+CMC；栏舍固定相机时退化为 ByteTrack 即可; domain_scope=cv-检测跟踪
  maturity: 主流（ByteTrack 强化版，ultralytics 默认跟踪器之一）
```

```yaml
- method_name: OC-SORT（Observation-Centric SORT）
  task_type: 多目标跟踪（MOT，纯运动，强化卡尔曼）
  input_data: 逐帧检测框
  output_result: 带 ID 的轨迹
  core_assumption: SORT 在遮挡/非线性运动下卡尔曼误差累积——以观测为中心(observation-centric)做虚拟轨迹回溯与动量修正，减少漂移
  advantages: 无需 re-id、非线性运动/遮挡鲁棒、对检测漏检容忍强、快
  limitations: 仍纯运动、密集交叉时无外观难分辨、依赖检测
  common_baselines: SORT、ByteTrack、DeepSORT
  evaluation_metrics: MOTA、IDF1、HOTA、ID switches、FPS
  suitable_datasets: MOT17、MOT20、DanceTrack（非线性运动强项）
  implementation_repo: noahcao/OC_SORT、ultralytics(可选)
  representative_papers:
    - "Observation-Centric SORT: Rethinking SORT for Robust Multi-Object Tracking | 2023(CVPR) | cited:830 | doi:10.1109/cvpr52729.2023.00934 | checked:2026-06-06"
    - "OC-SORT (arXiv) | 2022 | cited:33 | doi:10.48550/arxiv.2203.14360 | checked:2026-06-06"
  possible_innovation_points: 奶山羊跳跃/转身等非线性运动 + 遮挡后重现，OC-SORT 的观测回溯很契合；无 re-id 依赖恰避开外观相似难题，强烈推荐与 ByteTrack 并列候选; domain_scope=cv-检测跟踪
  maturity: 主流（DanceTrack 等遮挡/非线性基准强；家畜场景潜力大）
```

```yaml
- method_name: StrongSORT
  task_type: 多目标跟踪（MOT，DeepSORT 升级，运动 + 强 re-id）
  input_data: 逐帧检测框 + 强 re-id 特征
  output_result: 带 ID 的轨迹（可后接 AFLink/GSI 插值）
  core_assumption: 升级 DeepSORT 各组件（更强 re-id、EMA 特征、NSA 卡尔曼、AFLink 关联、GSI 插值）使经典范式重回高位
  advantages: IDF1 高、外观关联强、AFLink/GSI 补全断轨、模块化
  limitations: re-id 计算重、外观相似目标仍受限、流程较多
  common_baselines: DeepSORT、ByteTrack、FairMOT
  evaluation_metrics: MOTA、IDF1、HOTA、ID switches
  suitable_datasets: MOT17、MOT20
  implementation_repo: dyhBUPT/StrongSORT、mikel-brostrom/boxmot
  representative_papers:
    - "StrongSORT: Make DeepSORT Great Again | 2023(TMM) | cited:991 | doi:10.1109/tmm.2023.3240881 | checked:2026-06-06"
    - "StrongSORT (arXiv) | 2022 | cited:20 | doi:10.48550/arxiv.2202.13514 | checked:2026-06-06"
  possible_innovation_points: GSI 插值可补奶山羊遮挡断轨；但强 re-id 在相似白羊上增益有限，建议保留 GSI/AFLink、改用专用 re-id；计算重不利边缘; domain_scope=cv-检测跟踪
  maturity: 主流（高精度离线 MOT 选择；实时/边缘逊于 ByteTrack）
```

```yaml
- method_name: FairMOT
  task_type: 多目标跟踪（MOT，one-shot 联合检测 + re-id）
  input_data: 单帧图像（检测与 re-id 同一网络输出）
  output_result: 检测框 + re-id 特征 + 轨迹
  core_assumption: 检测与 re-id 不应共用 anchor-based 头(偏向检测)，用 anchor-free + 平衡的双分支公平学两任务于一个网络
  advantages: 检测+re-id 一体省算力、anchor-free、实时、re-id 质量较 JDE 公平
  limitations: 联合训练调参难、re-id 仍受外观相似限制、精度被 ByteTrack 系超越
  common_baselines: JDE、DeepSORT、SORT
  evaluation_metrics: MOTA、IDF1、HOTA、ID switches、FPS
  suitable_datasets: MOT15/16/17、MOT20
  implementation_repo: ifzhang/FairMOT
  representative_papers:
    - "FairMOT: On the Fairness of Detection and Re-identification in Multiple Object Tracking | 2021(IJCV) | cited:1475 | doi:10.1007/s11263-021-01513-4 | checked:2026-06-06"
  possible_innovation_points: one-shot 省算力适合边缘奶山羊跟踪；但其卖点 re-id 在相似白羊上优势缩水→可借其框架改用部位/花纹分支；夜间红外需重训; domain_scope=cv-检测跟踪
  maturity: 主流偏经典（one-shot MOT 代表；纯指标上 ByteTrack 系更优）
```

```yaml
- method_name: JDE（Joint Detection and Embedding）
  task_type: 多目标跟踪（MOT，one-shot 联合检测 + embedding）
  input_data: 单帧图像
  output_result: 检测框 + 外观 embedding + 轨迹
  core_assumption: 在单个网络里同时输出检测与 re-id embedding(共享计算)，实现近实时 MOT
  advantages: 检测+embedding 共享计算、近实时、是 one-shot MOT 开创工作之一
  limitations: 检测与 re-id 任务竞争(anchor-based 偏检测)致 re-id 欠佳、ID switch 多于 FairMOT
  common_baselines: SORT、DeepSORT
  evaluation_metrics: MOTA、IDF1、ID switches、FPS
  suitable_datasets: MOT15/16/17
  implementation_repo: Zhongdao/Towards-Realtime-MOT
  representative_papers:
    - "Towards Real-Time Multi-Object Tracking | 2020(ECCV) | cited:1065 | doi:10.1007/978-3-030-58621-8_7 | checked:2026-06-06"
    - "Towards Real-Time Multi-Object Tracking (arXiv) | 2019 | cited:32 | doi:10.48550/arxiv.1909.12605 | checked:2026-06-06"
  possible_innovation_points: 历史 one-shot 基线；奶山羊新项目建议直接用 FairMOT 后继或 ByteTrack，JDE 作对比; domain_scope=cv-检测跟踪
  maturity: 过时偏经典（被 FairMOT 等改进取代，作 one-shot 起点参考）
```

```yaml
- method_name: MOTR
  task_type: 多目标跟踪（MOT，端到端 Transformer，tracking-by-query）
  input_data: 视频帧序列
  output_result: 跨帧传播的 track query → 轨迹（无显式关联/NMS）
  core_assumption: 用可跨帧传播的 track query 表示每条轨迹，端到端联合检测与关联，免手工匹配与 re-id
  advantages: 真端到端、无手工关联/NMS、隐式时序建模、新生/消失目标统一处理
  limitations: 训练难且贵、检测主导易压制关联学习、密集场景与长视频显存大、精度/速度不及 ByteTrack
  common_baselines: TransTrack、FairMOT、ByteTrack
  evaluation_metrics: MOTA、IDF1、HOTA、ID switches
  suitable_datasets: MOT17、DanceTrack、BDD100K
  implementation_repo: megvii-research/MOTR
  representative_papers:
    - "MOTR: End-to-End Multiple-Object Tracking with Transformer | 2022(ECCV) | cited:578 | doi:10.1007/978-3-031-19812-0_38 | checked:2026-06-06"
    - "MOTR (arXiv) | 2021 | cited:16 | doi:10.48550/arxiv.2105.03247 | checked:2026-06-06"
  possible_innovation_points: 端到端 query 传播理论上利于奶山羊密集遮挡(免关联启发式)；但训练贵、边缘难、小数据不友好，目前研究性强于落地; domain_scope=cv-检测跟踪
  maturity: 新兴（端到端 MOT 研究主线；工程落地不及 tracking-by-detection）
```

```yaml
- method_name: TransTrack
  task_type: 多目标跟踪（MOT，Transformer，query-based）
  input_data: 视频帧序列
  output_result: detection query + track query 联合 → 轨迹
  core_assumption: 用两组 query（检测新目标 + 传播已有轨迹）在 Transformer 内联合，简化关联流程
  advantages: query 范式简洁、检测与传播统一、端到端雏形
  limitations: 精度被 MOTR/ByteTrack 超越、训练贵、密集长时遮挡仍弱
  common_baselines: FairMOT、CenterTrack
  evaluation_metrics: MOTA、IDF1、HOTA、ID switches
  suitable_datasets: MOT17、MOT20
  implementation_repo: PeizeSun/TransTrack
  representative_papers:
    - "TransTrack: Multiple Object Tracking with Transformer | 2020(arXiv) | cited:359 | doi:10.48550/arxiv.2012.15460 | checked:2026-06-06"
  possible_innovation_points: Transformer MOT 早期代表，奶山羊场景作研究对比；落地建议优先 ByteTrack/OC-SORT; domain_scope=cv-检测跟踪
  maturity: 新兴偏过时（开创 query-based MOT，已被 MOTR 等超越，作里程碑参考）
```

## 奶山羊场景推荐组合（结论速查）

| 需求 | 检测器 | 跟踪器 | 理由 |
|---|---|---|---|
| 边缘实时计数/盘点 | YOLOv8/v11 | ByteTrack | 高 FPS、易导出、低分框救遮挡羊、无需 re-id |
| 密集栏舍遮挡重 | RT-DETR 或 YOLOv11 | OC-SORT / ByteTrack | 免 NMS/低分框关联 + 观测回溯抗漂移 |
| 移动/云台相机俯拍 | YOLOv11(OBB) | BoT-SORT | 旋转框贴朝向 + 相机运动补偿 |
| 高精度离线标注 | Cascade R-CNN / DINO | StrongSORT(GSI 插值) | 精度上界 + 断轨补全 |
| 夜间红外 | YOLOv8 红外微调 | ByteTrack | 小数据迁移稳；运动关联不依赖 RGB 外观 |

**re-id 警示**：同品种白色奶山羊外观高度相似，DeepSORT/FairMOT/StrongSORT/JDE 的外观 embedding 区分度低，易 ID switch。优先选**运动/位置驱动**的 ByteTrack / OC-SORT；若必须 re-id，建议训练**部位/花纹/耳标**专用特征而非通用行人 re-id。

**数据集诚实声明**：经查证，COCO（通用 80 类）、MOT17/MOT20（行人）、DanceTrack（舞者）**均不含奶山羊**，无法直接评测家畜跟踪。动物领域现有公开集偏姿态(AP-10K、Animal Kingdom)而非奶山羊检测+MOT 基准。**奶山羊专用检测+跟踪数据集目前稀缺/未见权威公开**，落地需自建采集与标注（含俯拍、夜间红外、遮挡场景），本卡不编造不存在的数据集。

