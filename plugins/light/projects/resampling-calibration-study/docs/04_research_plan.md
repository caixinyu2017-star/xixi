# 研究方案（research-plan 阶段产出）

> 承接 idea-critique「有条件通过」判决,4 条 must-fix 全部落到本方案。
> 标题(暂):重采样对树集成概率校准的破坏与事后修复——多数据集实证研究

## 0. m04 must-fix 承接
| must-fix | 落到方案何处 | 如何验证整改 |
|----------|-------------|-------------|
| 1. 覆盖宽 IR 跨度 | §2 数据集选 IR∈[~2, ~30] | 数据表列出每个 IR |
| 2. 设 class_weight 对照分离两种解释 | §4 实验组 E2 | 单独一组只调权重不重采样 |
| 3. 校准多指标(ECE+Brier+可靠性曲线) | §3 指标 | 三指标全报 |
| 4. AUC 损失配对检验 | §5 统计 | Wilcoxon 配对 + 效应量 |

## 1. 假设（可证伪）
- **H1**:相对不处理,重采样(SMOTE/随机过采样/随机欠采样)显著抬高树集成的校准误差 ECE(Wilcoxon 配对 p<0.05,跨数据集)。
- **H2**:事后校准(Platt/isotonic)能把重采样模型的 ECE 拉回到接近 baseline,且 AUC 损失无统计显著性(配对检验 p>0.05 或效应量可忽略)。
- **H3**(探索):校准破坏程度随过采样比 ρ 单调上升。

## 2. 数据集（UCI/OpenML 真实公开,宽 IR）
拟选(最终以 data-engineering 体检为准):credit-g、Pima diabetes、成人收入(adult)子集、breast-cancer-wisconsin、以及一个高 IR 集(如 OpenML 信用卡欺诈子采样)。覆盖 IR ~1.3 到 ~30。

## 3. 评估指标
- **校准**:ECE(分箱)、Brier score、可靠性曲线。
- **判别力**:ROC-AUC、PR-AUC。
- **少数类**:F1(作对照,说明"光看 F1 看不出校准坏")。

## 4. 实验设计（矩阵见 experiment-matrix.md）
- 模型:RandomForest、HistGradientBoosting(sklearn 自带,CPU 快)。
- 处理:E0 原始 / E1 SMOTE / E1b 随机过采样 / E1c 随机欠采样 / **E2 仅 class_weight(对照)** / +事后 Platt / +事后 isotonic。
- 采样比扫描 ρ ∈ {0.25,0.5,0.75,1.0}(H3)。

## 5. 统计与可复现
- ≥10 个随机种子,报均值±std。
- 配对 Wilcoxon 检验 + Cliff's delta 效应量;多重比较 Holm 校正。
- 固定种子、分层 K 折、防泄漏(校准集与训练集分离,用 CalibratedClassifierCV 的 cv 机制或独立 holdout)。
- 派生数据需求 → 回 data-engineering 构建采样比变体。

## 衔接
派生/重采样数据需求回 m02(data-engineering)。方案交实现与跑实验。
