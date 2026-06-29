# 图表清单 manifest（figure-drawing 阶段产出）

> 目标期刊栏宽:IEEE 单栏 = 3.5 in。所有图 PDF(矢量)+PNG(300dpi)双格式,实测宽度 3.50in。

| 图号 | 文件 | 章节 | 栏宽 | caption |
|------|------|------|------|---------|
| F1 | fig1_ece_by_condition | IV-B 主效应 | 单栏 | Expected Calibration Error (ECE) across resampling and post-hoc calibration conditions, averaged over 5 datasets × 2 models × 10 seeds. Error bars: SEM. Resampling (red/orange) raises ECE; post-hoc calibration (green) reduces it below baseline. |
| F2 | fig2_reliability | IV-C 修复 | 单栏 | Reliability diagram on credit-g (HistGBDT). SMOTE without calibration (red) deviates from the diagonal; isotonic recalibration (green) restores agreement between predicted probability and observed frequency. |
| F3 | fig3_ece_vs_ir | IV-D IR分层 | 单栏 | ECE inflation relative to baseline versus dataset imbalance ratio (log scale). Undersampling (purple) degrades calibration sharply as imbalance grows; SMOTE (red) stays mild. |

| 表号 | 章节 | 内容 |
|------|------|------|
| T1 | III 数据 | 5 个数据集:n / 特征数 / IR / 少数类占比 |
| T2 | IV-A 主结果 | 各条件 ECE/Brier/AUC/PR-AUC/F1 + Wilcoxon p + Cliff's δ |

## 正文引用 citekey 约定（与 drafting/citation/typesetting 同源）
公式:author+year+title首词小写。例:chawla2002smote、breiman2001random、chen2016xgboost、saito2015precision。
