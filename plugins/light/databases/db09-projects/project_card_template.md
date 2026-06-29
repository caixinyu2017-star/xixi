# 项目卡模板（project_card）

> 复制到 `projects/<project_name>/project_card.md`。每次重要进展立即更新（联动 a02）。相对日期转绝对日期。

```yaml
project_name:
goal:                  # 一句话目标 + 成果形态(论文/竞赛/专利/系统)
current_stage:         # 资料调研|idea构思|方案确认|数据准备|实验实现|结果分析|论文写作|图表制作|投稿准备|答辩展示|成果转化
confirmed_idea:        # m04 通过的 idea(一句话) + 创新点
data_status:           # 数据来源/规模/质量结论(链 m02)
method_status:         # 选定方法/baseline(链 db03)
experiment_status:     # 已跑/待跑实验(链 m05 实验矩阵)
paper_status:          # 各章节进度 + 当前版本
ppt_status:            # PPT 版本与场景
code_status:           # 代码进度 + 仓库/分支
risk_list:             # 风险点 + 应对
next_actions:          # 下一步(会话开始先读这里)
decision_log:          # 见 decision_log.md
version_history:       # 见 version_history.md
# archived: YYYY-MM-DD # 可选,仅项目完结(录用/结题/用户声明)后加;a02 会话开始扫描跳过已归档项目,见 db09 README「项目归档」
```

## 配套文件
- `terminology.md` — 方法名/数据集名/指标名/创新点标准措辞(供 a07 跨材料统一)。
- `decision_log.md` — 决策时间线：`[日期] 决策 — 理由 — 来源(m03/m04/m14...)`。
- `version_history.md` — `[日期] 材料(论文/PPT/图/代码) vN — 变更摘要`。
- `palette.json` — 跨材料共享色板(视觉 SSOT 实例，可选)；论文图(m11)/PPT(m16)/前端(a05)共读，a07 据此核配色一致。schema 与模板见 db09 README「palette.json」节，字段与 db05 `design_tokens.template.json` 对齐。
- `submissions/` — 投稿记录：venue / 投稿日期 / 状态 / 审稿意见 / 结果。

## palette.json 模板（跨材料共享色板，可选）
> 复制到 `projects/<project_name>/palette.json`。`source` 须指向 db05/db06 真实卡并经核验，`hex` 不凭记忆填。schema 说明见 db09 README。
```json
{
  "$description": "项目级共享色板(视觉 SSOT 实例)。论文图/PPT/前端/海报同取一份，a07 据此核配色一致。",
  "$project": "<project_name>",
  "$aligned_with": "databases/db05-frontend-styles/design_tokens.template.json",
  "tokens": [
    { "name": "primary",   "hex": "#RRGGBB", "usage": "主色",       "source": "db06:light-slides/assets/themes.py::<THEME>.COLORS.primary", "last_checked": "YYYY-MM-DD" },
    { "name": "accent",    "hex": "#RRGGBB", "usage": "强调色",     "source": "db06:.../themes.py::<THEME>.COLORS.accent",                "last_checked": "YYYY-MM-DD" },
    { "name": "success",   "hex": "#RRGGBB", "usage": "语义色-成功", "source": "db05:design_tokens.template.json::color.semantic.success", "last_checked": "YYYY-MM-DD" }
  ]
}
```

## 术语表模板（terminology.md）
```
| 类别 | 标准叫法 | 缩写 | 英文 | 备注 |
|------|----------|------|------|------|
| 方法 |          |      |      |      |
| 数据集 |        |      |      |      |
| 指标 |          |      |      | 定义+单位 |
| 创新点1 | (标准措辞，论文/PPT/软著一字对齐) |
| 创新点2 |  |
| 创新点3 |  |
```
