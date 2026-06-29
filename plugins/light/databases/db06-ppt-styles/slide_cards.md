# db06 PPT 设计卡模板与 canonical 索引

> 本文件保留 db06 的 slide_card 模板，并记录早期 seed 卡迁移后的 canonical 位置。为避免重复卡片，真实 PPT 场景卡不再写在本文件中；新增/维护请放入 `resources_real.md` 或更具体的页型/叙事扩展卡文件。

## 卡片模板
```yaml
- scenario:
  theme_style:
  page_type:
  layout_structure:
  color_palette:
  font_pairing:
  visual_hierarchy:
  chart_style:
  icon_style:
  transition_style:
  speaker_notes_style:
  reuse_template_notes:
```

## Canonical 索引（原 seed 已迁移）

| 原 seed 场景 | canonical 文件 | 说明 |
|---|---|---|
| 学术答辩 | [resources_real.md](resources_real.md) | canonical 名称为“学术答辩（硕博/毕业设计）”，补全页面序列、控时、Beamer/Marp 建议 |
| 互联网+/挑战杯路演 | [resources_real.md](resources_real.md) | canonical 名称为“竞赛路演（互联网+/挑战杯/创业大赛）”，补全痛点→方案→价值的路演叙事 |
| 数据分析汇报 | [resources_real.md](resources_real.md) | 数据分析风完整卡；高级 dashboard summary 页型另见 [slide_pattern_cards.md](slide_pattern_cards.md) |

## 待补充
按用户具体场景补充 slide_card，并沉淀可复用页面版式。新增卡片必须放入资源或扩展文件，避免本模板文件重新产生重复 `scenario`。
