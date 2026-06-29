# R9 批3 — palette.json 跨库色板核验记录

- 日期：2026-06-12
- 范围：R9.7 共享色板机制落地 + R9.8 采集→核验→入库管线成文衔接 freshness
- 执行：Opus 4.8（Claude Code）

## 1. dairygoat palette.json 色值溯源核验（铁律：hex/source 须真实可追溯）

dairygoat 是农业/CV/畜牧检测项目 → 取色自 db06 `light-slides/assets/themes.py` 的 **AGRICULTURE** 主题
（该主题 `scenario` 原文含「智慧农业、农学、生态、畜牧检测项目」，themes.py 已 selftest 绿），
语义色取自 db05 `design_tokens.template.json`（DTCG 视觉 SSOT，色值锚点真相源）。

程序化逐 token 比对 hex 与所引源文件实际值（脚本见本轮对话），**12/12 全部精确匹配**：

| token | hex | source | 匹配 |
|---|---|---|---|
| primary | #4E7D2C | db06 themes.py AGRICULTURE.COLORS.primary | ✅ |
| secondary | #8AB661 | …secondary | ✅ |
| accent | #E08A1E | …accent | ✅ |
| text | #2E3A22 | …text | ✅ |
| bg | #FBFDF7 | …bg | ✅ |
| surface | #EAF3DE | …surface | ✅ |
| muted | #7A8769 | …muted | ✅ |
| line | #D2E0BF | …line | ✅ |
| success | #16A34A | db05 design_tokens.template.json color.semantic.success | ✅ |
| warning | #D97706 | …warning | ✅ |
| danger | #DC2626 | …danger | ✅ |
| info | #0EA5E9 | …info | ✅ |

`last_checked` 全部落 2026-06-12（本轮实查日期）。无凭记忆填色。

## 2. 四处接线 grep 可见（R9.7 验收）

- m11 `light-figure-drawing/SKILL.md`「审美与规范·配色」：项目有 palette.json 则必用其取色。
- m16 `light-slides/SKILL.md`「先定三件事·视觉风格」：项目有 palette.json 则必用其取色。
- a05 `light-frontend-design/SKILL.md`「设计语言」：项目有 palette.json 则必用，前端不另立色板。
- a07 `light-consistency/SKILL.md`：维护要点 + 五维⑤视觉，把"跨材料配色一致"改为**对照 palette.json 逐项核**。

schema 写入 db09 README + project_card_template.md（含 JSON 模板），字段与 db05 DTCG 模板对齐。

## 3. R9.8 采集→核验→入库管线成文 + freshness 衔接

- db01 README 已有完整管线（批2 落地）；本批为 db05/db06/db07 README 各补**同口径**5 步管线
  （采集→核验铁律→入库→check_databases 校验→落 `核验日期 YYYY-MM-DD` 供 freshness 月度统计）。
- **修复一处真实衔接断点**：`check_freshness.py` 的 PROSE_DATE_RE 原只认 `核实日期/研究日期/核查日期`，
  而 db05/06/07 卡文件实际用 `核验日期` → 6 个卡文件被静默漏统计。已补 `核验日期` 同义词到正则 + selftest 断言。
  修复后 freshness 统计 db05 2→3、db06 1→2、db07 1→3 张卡（合计 313→318）。warn-only，不阻断 CI。

## 4. 门禁结果

8 校验器全绿（check_skills/entry_docs/skill_links/skill_assets/installation_assets/databases/freshness）
+ 51 selftest 全 PASS、无产物残留；git diff --check 无空白错误。
（installation_assets 2 条 warning 为 Windows 主机跳过 install.sh 本地校验的既有提示，非失败。）
