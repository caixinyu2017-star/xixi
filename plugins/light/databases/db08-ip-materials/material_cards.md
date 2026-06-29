# db08 材料卡模板与 canonical 索引

> 本文件保留 db08 的 material_card 模板，并记录早期 seed 卡迁移后的 canonical 位置。为避免重复卡片，真实软著、专利与申报材料卡不再写在本文件中；新增/维护请放入 `material_extended_cards.md` 或更具体的配套资产文件。

## 卡片模板
```yaml
- material_type:
  required_sections:
  official_requirement:
  writing_style:
  common_mistakes:
  checklist:
  sample_structure:
  legal_risk:
  reuse_scope:
  final_review_needed:
  # —— 可选(db08 重构新增,不进必填 schema,CI 不强校验) ——
  source_pointer:           # 卡内引用的官方口径外链(如 CPCC 指南/CNIPA 公告/当届评审规则),把易变行政口径外链化
  last_checked:             # 卡内引用的官方口径核查日 YYYY-MM-DD;费用/页数/权重等以官方当期公告为准、提交前重核
```

> db08 是方法论库:10 字段是跨学科行政程序+写作方法论(留本地精养)。卡内引用的官方口径(软著页数/加急费/评分权重/竞赛链接)**绝大多数无 API**,走指针模型:存口径文字/【待核查】+ source_pointer 指向官方源 + last_checked,**不缓存数值假权威值**,提交前以官方当期公告强制核查。

## Canonical 索引（原 seed 已迁移）

| 原 seed 材料类型 | canonical 文件 | 说明 |
|---|---|---|
| 软件著作权申请 | [resources_real.md](resources_real.md) + [material_extended_cards.md](material_extended_cards.md) | 软著总体流程与 CPCC/源代码 60 页规则见 `resources_real.md`；实体细分卡见“软著操作说明书”“软著源代码鉴别材料” |
| 发明专利 | [resources_real.md](resources_real.md) + [material_extended_cards.md](material_extended_cards.md) | 专利说明书/权利要求结构与风险见 `resources_real.md`；实体细分卡见“技术交底书”“权利要求书草案”“专利附图与图号说明”“在先技术检索报告” |
| 竞赛/项目申报书(大创/挑战杯/互联网+) | [material_extended_cards.md](material_extended_cards.md) + [budget_template.md](budget_template.md) + [case_skeletons.md](case_skeletons.md) | 挑战杯/创新大赛实体卡见 `material_extended_cards.md`；预算和高分结构分别见 `budget_template.md`、`case_skeletons.md` |

## 配套资产
- [budget_template.md](budget_template.md) — 经费预算表模板：科研经费支出预算表（大创/大挑）+ 已填示例 + 创业财务预测表（互联网+创业组，含假设登记表）+ 自审清单。
- [case_skeletons.md](case_skeletons.md) — 各赛事高分材料结构骨架 + 评审维度 + 高分特征/常见出局点（互联网+、挑战杯大挑、大创、数模）。

## 待补充
后续可按用户具体参赛类型补充更细的官方模板差异（以当届官方压缩包为准，不缓存受版权原文）。新增卡片必须放入扩展或配套文件，避免本模板文件重新产生重复 `material_type`。
