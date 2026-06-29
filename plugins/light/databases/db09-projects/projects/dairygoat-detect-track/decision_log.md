# 决策日志 (decision_log.md) — 奶山羊行为识别项目

格式：`[日期] 决策 — 理由 — 来源`

- [2026-06-06] 跟踪弃用通用 re-id，改用运动/位置驱动(ByteTrack 低分框二次关联 + OC-SORT 观测回溯) — 奶山羊多为白羊、外观高度同质化，通用外观 re-id embedding 不可分；Cows2021/OpenCows2020 的 known_issues 也证实"花纹相似个体易混" — 来源 m04/m08 + db03 检测跟踪卡 + db04 数据集卡
- [2026-06-06] 检测器选 YOLOv11(imgsz=1280)/RT-DETR，俯拍考虑 OBB 旋转框 — 栏舍俯拍视角 + 个体偏小 + 边缘实时需求 — 来源 m05 + db03 检测卡
- [2026-06-06] 行为识别用 SlowFast 双流 + PoseC3D + VideoMAE 自监督 — PoseC3D 热图抗群养遮挡、VideoMAE 自监督缓解稀有类长尾、SlowFast 双路径配跛行步态周期 — 来源 m03/m05 + db03 行为时空卡
- [2026-06-06] 创新点锁定"级联误差传播抑制 + 奶山羊场景专属适配"，不以三模块串联为卖点 — m04 审定：YOLOv11+ByteTrack+SlowFast 纯串联新颖性≈0，GSCW-YOLO(2024,Animals)等近同工作已占坑，必须有方法层 delta — 来源 m04
- [2026-06-06] 数据起步策略：CherryChèvre(CC许可,可下载)做检测预训练 + AP-10K/APT-36K 做姿态迁移 + 自建行为标注 — 无奶山羊"姿态+ID+多场景+行为"综合公开基准；GoatABRD/DiaryGoatMVT 许可未声明不能做可再分发基线 `[许可/DOI 见 db04:cards_animal_livestock.md, 用前重核, 冲突信在线]` — 来源 m02 + db04 cards_animal_livestock.md
- [2026-06-06] 稀疏事件预警改用时序动作检测(ActionFormer/BMN)而非 trimmed-clip 分类；跛行评分用序数回归(CORAL/CORN)+QWK — 发情爬跨是秒级瞬时事件、跛行运动评分是有序多级标签，普通分类不适配 — 来源 Task2 审计 + db03 cards_temporal_action.md
- [2026-06-06] 补夜间 RGB-IR 多模态融合(Zero-DCE + CFT/ProbEn) — 昼夜健康/发情预警必涉夜间，不能只做白天 — 来源 Task2 审计 + db03 cards_nighttime_multimodal.md
- [2026-06-06] 投稿首选 Computers and Electronics in Agriculture(venues.csv 第140行)，会议关注 CV4Animals — 应用型家畜 CV 工作主场；该刊本方向 h_index≈220、2yr均被引≈9.19 `[snapshot 2026-06-06, src=db01:venues.csv#L140, 投前用 venue_signal.py --issn 重核, 冲突信在线]` — 来源 m01/m13 + db01 venues.csv
