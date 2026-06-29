# db07 图表卡模板与 canonical 索引

> 本文件保留 db07 的 figure_card 模板，并记录早期 seed 卡迁移后的 canonical 位置。为避免重复卡片，真实图表卡不再写在本文件中；新增/维护请放入 `resources_real.md`、`figure_advanced_cards.md` 或更具体的扩展卡文件。

## 卡片模板
```yaml
- figure_type:
  figure_id:           # F# 图 / T# 表 (如 F1/T1), 与 m07 模板 [图位 F1]/[表位 T1] 对齐；模板辅助字段，真实 db07 schema 以 README 为准
  paper_source:        # 仅元数据/链接
  research_field:
  purpose:             # 支撑哪个 claim
  data_required:
  layout:
  color_scheme:
  annotation_style:
  caption_style:
  possible_code_tool:
  replication_notes:
  where_to_place_in_paper:
  target_journal:      # JOURNAL_SPECS 键: nature/science/cell/plos/ieee/elsevier；规划/执行辅助字段
  column:              # single/double/full/onehalf (须为该刊实有的键)；规划/执行辅助字段
```

## Canonical 索引（原 seed 已迁移）

| 原 seed 图表类型 | canonical 文件 | 说明 |
|---|---|---|
| 主结果对比柱状图(带误差棒) | [resources_real.md](resources_real.md) | canonical 名称为“跨数据集主结果对比(分组柱+误差棒)”，补全多数据集、多种子、显著性与 SciencePlots/matplotlib 落地说明 |
| 消融分组柱状/折线 | [resources_real.md](resources_real.md) | canonical 名称为“消融实验图(分组柱/累加折线)”，强调控制变量、一次只改一处、与主结果同指标 |
| 模型框架图 | [resources_real.md](resources_real.md) | canonical 名称为“模型框架图(architecture)”，补全矢量导出、创新模块描边与单栏缩放可读性要求 |
| 可解释性热力图(注意力/SHAP) | [resources_real.md](resources_real.md) | canonical 名称为“可解释性热力图(注意力/SHAP/Grad-CAM)”，补充 Grad-CAM、归一化、样本选择与不挑樱桃约束 |

## 待补充
按用户领域补充 figure_card，沉淀统一调色板与组图模板。新增卡片必须放入资源或扩展文件，避免本模板文件重新产生重复 `figure_type`。
