# 术语表 (terminology.md) — 奶山羊行为识别项目

供 a07 跨材料(论文/PPT/软著/图表)统一措辞。任何材料引用以下名称须一字对齐。

| 类别 | 标准叫法 | 缩写 | 英文 | 备注 |
|------|----------|------|------|------|
| 方法 | 目标检测 | — | object detection | YOLOv11 / RT-DETR |
| 方法 | 多目标跟踪 | MOT | multi-object tracking | ByteTrack + OC-SORT，无 re-id |
| 方法 | 行为识别 | — | action recognition | SlowFast + PoseC3D |
| 方法 | 时空特征融合 | — | spatiotemporal fusion | 双流(RGB+骨架) |
| 方法 | 时序动作检测 | TAL | temporal action localization | ActionFormer/BMN，定位发情爬跨事件 |
| 方法 | 序数回归 | — | ordinal regression | CORAL/CORN，跛行评分 |
| 方法 | 自监督预训练 | — | self-supervised pretraining | VideoMAE |
| 数据集 | CherryChèvre | — | CherryChèvre | 山羊检测，CC许可，DOI:10.57745/4C03OG（许可/DOI 快照，权威源 db04 cards_animal_livestock.md 用前重核） |
| 数据集 | GoatABRD | — | GoatABRD | 山羊行为含跛行，许可待核 |
| 数据集 | 自建奶山羊行为集 | — | (self-built) | 双视角/17-20关键点/RFID-ID金标准 |
| 指标 | 检测均值平均精度 | mAP | mean Average Precision | IoU=0.5:0.95 |
| 指标 | 跟踪综合精度 | HOTA | Higher Order Tracking Accuracy | 优先于MOTA，用TrackEval计算 |
| 指标 | 多目标跟踪精度 | MOTA | — | 含ID切换惩罚 |
| 指标 | 身份F1 | IDF1 | — | ID一致性 |
| 指标 | 二次加权Kappa | QWK | Quadratic Weighted Kappa | 跛行有序评分专用 |
| 创新点1 | 级联误差传播抑制：检测→跟踪→行为四级流水线的不确定性传播建模 | | |
| 创新点2 | 奶山羊场景专属适配：弃通用re-id(白羊外观同质化)，运动驱动跟踪 + 群养遮挡下骨架行为识别 | | |
| 创新点3 | 个体级稀疏事件预警：发情爬跨(秒级)与跛行(分钟级步态)的时序定位 + 序数评分 | | |
