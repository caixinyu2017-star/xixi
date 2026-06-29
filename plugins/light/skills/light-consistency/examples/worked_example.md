# 端到端实例：论文 vs PPT 指标名/数值冲突 → 定位 → 统一 → 修正

本例演示 light-consistency 的完整闭环，配套可运行材料在 `examples/materials_paper.txt`、
`examples/materials_ppt.txt`，单一事实源用 `assets/db09_*.yaml`。

## 0. 复现命令

```bash
cd d:/skill/Light/skills/light-consistency
python scripts/consistency_audit.py \
    --db09 assets \
    --materials examples/materials_paper.txt examples/materials_ppt.txt
```

（无数据时直接 `python scripts/consistency_audit.py` 跑内置合成自测。）

## 1. 背景（冲突是怎么产生的）

论文初稿里方法叫 `DCA-Net`，主指标用 `F1=87.6%`、`mAP@0.5=74.2%`。
做 PPT 时同义改写 + 手抄数字，引入四类典型不一致：

- 方法名被写成 `DCANet`（少了连字符）和口语化的 `我们的网络`。
- 把 `F1` 说成 `准确率`（语义不同的易混名）。
- `F1` 数值从 87.6% 抄成 85.2%（手误）。
- `mAP@0.5` 只在论文出现，PPT 整页缺席（覆盖缺口）。

## 2. 定位（inventory → tag，脚本自动产出）

运行审计后，报告把每条冲突定位到 `材料:行号`，并按 ERROR/WARN 分级：

| # | 类型 | 位置 | 问题 |
|---|------|------|------|
| 1 | SUBSTITUTION | materials_ppt.txt:3 | `DCANet` 应为 `DCA-Net` |
| 2 | SUBSTITUTION | materials_ppt.txt:5 | `我们的网络` 应为 `DCA-Net` |
| 3 | METRIC_NAME  | materials_ppt.txt:5 | `准确率` 被当 `F1` 用 |
| 4 | METRIC_VALUE | materials_ppt.txt:4 | `F1=85.2%` 与权威 `87.6%` 不符 |
| 5 | COVERAGE_GAP | materials_ppt.txt  | `mAP@0.5` 在 PPT 缺席 |

## 3. 统一（gap → fix，对照 db09 单一事实源）

裁决一律以 db09 为准（`db09_metric_registry.yaml` 中 DCA-Net 的 F1=87.6、mAP@0.5=74.2；
`db09_method_lock.yaml` 锁定方法名 `DCA-Net`）：

- 方法名统一 `DCA-Net`；正式名出现后不再用"我们的网络"。
- 指标名统一 `F1`（PPT 误用的"准确率"实为 F1，改名）。
- 数值统一为权威 `87.6%`。
- PPT 增补 `mAP@0.5=74.2%`，与论文表对齐。

## 4. 修正后文本（PPT 对应页）

```text
DCA-Net 在 CrowdScene-2k 上的 F1 达到 87.6%，mAP@0.5 为 74.2%，
相比基线 YOLOv8（F1 82.3%）有明显提升。
```

## 5. 回归校验

把 `materials_ppt.txt` 按上文改好后重跑同一命令，报告应显示
`发现总数：0`、`完整性自检 ... 通过`，即冲突清零。变更同时回写 db09 的
`last_checked_date`，触发对其余材料的广播回扫。
