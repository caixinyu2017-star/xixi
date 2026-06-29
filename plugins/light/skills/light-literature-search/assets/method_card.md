# 方法卡（method_card.md）

> 6 件套之一。字段对齐 CONVENTIONS §3 / db03 method_card。一篇代表方法填一张。

| 字段 | 内容 |
|------|------|
| method_name | （方法/模型名 + 出处论文简称） |
| task_type | （分类 / 检测 / 分割 / 回归 / 生成 / 跟踪 / 排序 …） |
| input_data | （模态、维度、采样率、典型规模） |
| output_result | （预测目标、输出格式） |
| core_assumption | （方法成立的核心假设/前提） |
| advantages | （相对 baseline 的明确优点，最好有数字） |
| limitations | （已知失效场景、计算/数据代价、复现难点） |
| common_baselines | （论文里对比的基线，便于横向对照） |
| evaluation_metrics | （主指标 + 口径，如 mAP@0.5 / F1 / QWK / MOTA） |
| suitable_datasets | （适配数据集 + license） |
| implementation_repo | （官方/复现仓库链接，注明 star / 最近更新 / license） |
| representative_papers | （DOI / arXiv id，须可核查） |
| possible_innovation_points | （可挖的改进方向 → 喂给 m03） |
| maturity | （成熟度：原型 / 已被复现 / 工业落地） |

## 证据等级标注（每条结论后标）
- [已验证]：本环境 curl/跑代码核实过（注明 HTTP 码或脚本）。
- [文献]：来自论文原文，给 DOI。
- [推测]：尚未核实，需进一步查证。

## 被引/重要性（接 SKILL.md 量化表）
- 论文年龄：______ 年；被引（来源库 ______）：______
- 年均被引：______；判级：奠基 / 里程碑 / SOTA / 一般。
