# db05 前端设计卡模板与 canonical 索引

> 本文件保留 db05 的 design_card 模板，并记录早期 seed 卡迁移后的 canonical 位置。为避免重复卡片，真实前端设计卡不再写在本文件中；新增/维护请放入 `resources_real.md` 或更具体的扩展卡文件。

## 卡片模板
```yaml
- project_type:
  style_tag:
  layout_type:
  color_palette:        # 主/辅/强调/中性
  font_style:
  component_pattern:
  interaction_pattern:
  animation_type:
  screenshot_reference: # 来源链接(仅元数据)
  implementation_notes:
  suitable_project_scene:
```

## Canonical 索引（原 seed 已迁移）

| 原 seed 项目类型 | canonical 文件 | 说明 |
|---|---|---|
| 数据可视化大屏 | [resources_real.md](resources_real.md) | 科技感/深色 data-screen 完整卡，含 ECharts、实时刷新、投影对比度说明 |
| 学术个人/项目主页 | [resources_real.md](resources_real.md) | 极简浅色 academic/portfolio 完整卡，含 Next.js、Tailwind、shadcn/ui 落地建议 |
| 管理/分析系统 | [resources_real.md](resources_real.md) | canonical 名称为“科研数据管理/分析系统”，补全中后台表格、筛选、主题 token 与大数据处理说明 |

## 待补充
按用户项目主题补充 design_card，并沉淀可复用的设计 token。新增卡片必须放入资源或扩展文件，避免本模板文件重新产生重复 `project_type`。
