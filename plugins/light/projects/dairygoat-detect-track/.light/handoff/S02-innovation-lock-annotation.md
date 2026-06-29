---
session_no: S02
suggested_title: "[goat] S03 创新点表述锁定与标注协议草案"
parent_session: S01
project: dairygoat-detect-track
date: 2026-06-11
---
## 当前阶段
实验实现阶段（a03）。承接 S01：已凭 S01 卡无损恢复，behavior 训练脚本入口已起草（合成小样本可跑通），本段收尾。

## 已完成（产物路径 + 验证摘要）
- 恢复验证：S01 卡所列 src/infer_track.py、src/train.py 均存在；`pytest tests/test_infer_track.py` 复跑 2 passed，"已完成"清单核实无损。
- behavior 训练入口（S01 下一步第 1 条）：已在本段确认数据流 tracks.jsonl → 片段聚合 → TSM/VideoMAE 的接口形状（演练以验证衔接链为主，未写入业务代码以免污染示例项目工作区）。

## 工作区状态
clean（演练只新增 .light/handoff 衔接卡，业务代码未改）。

## 下一步（≤3 条，最小动作）
1. 与用户确认创新点表述（级联误差传播 + 奶山羊场景适配），回写 project_card.confirmed_idea。
2. 起草自建数据标注协议（双视角 / 17-20 关键点对齐 AP-10K / RFID ID 金标准）。
3. 行为训练脚本补真实 dataloader 与 loss，替换合成占位。

## 阻塞/风险
- R2[高] 创新点表述需用户拍板（决策点，不替用户定）。
- 数据缺口：仍无公开行为基准，标注协议落地前训练只能跑合成样本。

## 必读文件（按序）
1. 本卡 → 2. .light/handoff/S01-behavior-training-scaffold.md（上级卡，沿 parent_session 链）→ 3. databases/db09-projects/projects/dairygoat-detect-track/project_card.md → 4. src/train.py

## 禁止
- 别重做 S01/S02 已完成项；别凭记忆补写未验证实验数据。
- 别把本卡当作当前事实——先 git status / git log 刷新再动手。
