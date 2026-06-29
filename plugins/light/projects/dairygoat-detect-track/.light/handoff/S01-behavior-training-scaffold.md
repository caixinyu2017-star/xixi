---
session_no: S01
suggested_title: "[goat] S02 行为识别训练脚本落地"
parent_session: none
project: dairygoat-detect-track
date: 2026-06-11
---
## 当前阶段
实验实现阶段（a03 backend-coding）。检测+跟踪代码骨架已就绪，本段任务是把下游行为识别训练脚本从 ~25% 推进到可跑通。

## 已完成（产物路径 + 验证摘要）
- src/infer_track.py、src/train.py — 检测+跟踪推理/训练骨架，`pytest tests/test_infer_track.py` 2 项通过。
- configs/goat_det.yaml、configs/bytetrack_goat.yaml、configs/train.yaml — 检测/跟踪/训练配置，已被骨架读取。
- databases/db09-projects/projects/dairygoat-detect-track/project_card.md — 项目卡 14 字段最新；experiment_status=方案级(E1-E11 矩阵)，code_status≈25%。

## 工作区状态
clean（本段尚未改动业务代码；本卡为会话衔接协议 R2 演练首卡）。

## 下一步（≤3 条，最小动作）
1. 落地行为识别训练脚本：tracks.jsonl → 行为片段聚合 → TSM/VideoMAE 训练入口（先跑通合成小样本）。
2. 锁定创新点表述（级联误差传播 + 奶山羊场景适配），回写 project_card 的 confirmed_idea。
3. 启动自建数据标注协议草案（双视角 / 17-20 关键点对齐 AP-10K / RFID 做 ID 金标准）。

## 阻塞/风险
- R1[高] 无公开行为基准，自建标注成本是最大风险 → 起步用 CherryChèvre + 迁移学习。
- R2[高] 创新性不足（GSCW-YOLO 2024 已占坑）→ 创新点须锁定级联误差传播 + 场景适配，否则审稿人难买账（需用户在第 2 步拍板表述）。

## 必读文件（按序）
1. 本卡 → 2. .light/passport.yaml（本演练项目暂无，缺则跳过）→ 3. databases/db09-projects/projects/dairygoat-detect-track/project_card.md → 4. src/infer_track.py

## 禁止
- 别重做"已完成"清单里的检测/跟踪骨架；别凭记忆补写未验证的实验数据（experiment_status 仍是方案级，无真实跑数）。
- 别把本卡当作当前事实——接手后先用 git status / git log 刷新现实再动手。
