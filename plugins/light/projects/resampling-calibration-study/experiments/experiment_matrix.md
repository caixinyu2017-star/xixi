# 实验矩阵（research-plan / experiment-matrix）

> 承接 04_research_plan.md。每个实验行可独立跑、可复现。派生数据需求列交 data-engineering。

## 主实验矩阵

| 实验ID | 假设 | 模型 | 数据处理 | 后处理校准 | 数据集 | 指标 | 种子 |
|--------|------|------|----------|-----------|--------|------|------|
| E0 | baseline | RF, HistGBDT | 无 | 无 | 全部 | ECE,Brier,AUC,PR-AUC,F1 | 10 |
| E1-smote | H1 | RF, HistGBDT | SMOTE(ρ=1.0) | 无 | 全部 | 同上 | 10 |
| E1-ros | H1 | RF, HistGBDT | 随机过采样(ρ=1.0) | 无 | 全部 | 同上 | 10 |
| E1-rus | H1 | RF, HistGBDT | 随机欠采样 | 无 | 全部 | 同上 | 10 |
| E2-cw | must-fix#2 | RF, HistGBDT | 仅 class_weight | 无 | 全部 | 同上 | 10 |
| E3-platt | H2 | RF, HistGBDT | SMOTE | Platt(sigmoid) | 全部 | 同上 | 10 |
| E3-iso | H2 | RF, HistGBDT | SMOTE | isotonic | 全部 | 同上 | 10 |
| E4-rho | H3 | HistGBDT | SMOTE ρ∈{.25,.5,.75,1} | 无 | 高IR子集 | ECE,AUC | 10 |

## 派生数据规格（交 data-engineering 构建）
| 需求 | 基础数据集 | 变换 | 参数 | 划分 |
|------|-----------|------|------|------|
| 采样比变体 | 高IR数据集 | SMOTE 过采样 | ρ∈{.25,.5,.75,1.0} | 仅对训练折,校准/测试折不动 |
| 欠采样变体 | 全部 | 随机欠采样 | 多数类降到 IR=1 | 同上 |

## 防泄漏纪律（must-fix#3 配套）
- 重采样**只在训练折内**做,绝不碰验证/测试折。
- 校准用独立 holdout 或 CalibratedClassifierCV(cv=prefit + 独立校准集)。
- 分层 K 折保持原始类分布于测试折。

## 统计（must-fix#4）
- 跨数据集×种子配对 Wilcoxon;Cliff's delta;Holm 多重比较校正。
- AUC 损失:配对检验 + 效应量,声明"不损判别力"前给证据。

## 成功标准
- H1 成立:E1 vs E0 的 ECE 配对检验 p<0.05 且效应量非可忽略。
- H2 成立:E3 vs E1 的 ECE 显著下降,且 E3 vs E0 的 AUC 无显著差异。
- 即使 H 不成立也如实报告(零结果也是结果)。
