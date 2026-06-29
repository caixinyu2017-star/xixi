---
project_name: dairygoat-detect-track
created: 2026-06-06
---

# 项目卡：奶山羊多目标行为识别系统

> 来源：Task2 端到端试飞跑通 Light 全链路后沉淀。每次重要进展立即更新（联动 a02/a07）。

```yaml
project_name: 奶山羊多目标行为识别系统 (dairy-goat behavior recognition)
goal: 用羊场监控视频自动识别奶山羊采食/反刍/站立/躺卧/爬跨(发情)/跛行等行为，做健康与发情预警 → 成果形态：论文(应用型CV) + 可落地系统
current_stage: 实验实现（检测+跟踪已出代码骨架，下游行为识别/时空融合停在方案层）
confirmed_idea: |
  主推(m03 Idea B)：YOLOv11/RT-DETR检测 + OC-SORT/ByteTrack无re-id运动跟踪 + PoseC3D骨架⊕SlowFast双流时空融合，做ID-anchored个体级行为识别，可算个体反刍时长。
  备选(Idea A)：把发情/跛行从闭集分类重定义为个体级异常早预警(VideoMAE自监督 + lead-time指标)。
  ⚠️ m04 审定结论：当前三模块串联新颖性不足(GSCW-YOLO 2024已占坑)，创新点须落在"级联误差传播处理"+"奶山羊场景专属适配"，否则审稿人难买账。
data_status: |
  无奶山羊"姿态+个体ID+多场景+行为"综合公开基准(db04核查确认)。真实可用：CherryChèvre(检测,CC许可,DOI:10.57745/4C03OG,唯一明确可下载)、GoatABRD(行为含跛行,GitHub无LICENSE待核)、DiaryGoatMVT(多任务,无论文)。许可/DOI 为快照,权威源见 db04 cards_animal_livestock.md,用前重核、冲突信在线。
  结论：必须自建行为视频标注；起步可用CherryChèvre做检测预训练 + AP-10K/APT-36K做姿态迁移。
method_status: |
  检测：YOLOv11(imgsz=1280小目标/俯拍OBB) / RT-DETR。跟踪：ByteTrack(低分框二次关联)+OC-SORT(观测回溯)，弃通用re-id(白羊外观同质化)。
  行为：SlowFast双流 + PoseC3D(抗群养遮挡) + VideoMAE自监督(缓解长尾稀有类)。
  稀疏事件：ActionFormer/BMN时序动作检测(发情爬跨秒级事件)。跛行评分：CORAL/CORN序数回归 + QWK指标。
  夜间：Zero-DCE低光增强 + RGB-IR多模态融合(CFT/ProbEn)。
experiment_status: 方案级(m05给出E1-E11实验矩阵：主实验/消融/SOTA对比GSCW-YOLO/泛化/鲁棒/敏感性)。尚无真实实验数据。
paper_status: 方法章节开头与结构骨架已起草(m07)；其余未写。目标 pipeline 形式化 F=F_fuse∘F_act∘F_track∘F_det。
ppt_status: 未开始
code_status: 检测+跟踪代码骨架(train.yaml/bytetrack_goat.yaml/infer_track.py,pytest 2项通过)；下游行为识别训练脚本未落地(实现完成度~25%)
risk_list: |
  R1[高] 无公开行为基准，自建标注成本与周期是最大风险 → 用CherryChèvre+迁移学习起步，分阶段标注。
  R2[高] 创新性不足(近同工作已占坑) → 创新点锁定级联误差传播+奶山羊专属适配。
  R3[中] 级联误差累积(检测→跟踪→行为四级) → 上端到端/联合优化或置信度传播。
  R4[中] 夜间红外场景 → 补RGB-IR融合，不能只白天。
  R5[低] GoatABRD/DiaryGoatMVT许可未声明，不能直接做可再分发的公开基线。
next_actions: |
  1) 落地行为识别训练脚本(tracks.jsonl→行为片段聚合→TSM/VideoMAE训练)，把实现从25%推进。
  2) 锁定创新点表述并回写 confirmed_idea。
  3) 启动自建数据标注协议(双视角/17-20关键点对齐AP-10K/RFID做ID金标准)。
  4) 投稿定位：首选 Computers and Electronics in Agriculture(venues.csv第140行)，会议看 CV4Animals。
decision_log: 见 decision_log.md
version_history: 见 version_history.md
```
