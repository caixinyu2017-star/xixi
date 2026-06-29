# 结构化润色发现 Schema（findings schema）

> 目的：让 `polish.py`（LanguageTool）与 `mechanical_check.py`（离线规则）输出
> **同构**的结构化发现，便于合并、排序、去重、回填到原文，并喂给下游
> （m07 重构 / m14 模拟审稿 / db09 版本记录）。所有脚本以此为契约。

## 1. 顶层结构

```json
{
  "_meta": { ... },
  "findings": [ { finding }, { finding }, ... ]
}
```

### `_meta` 字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `endpoint` | string | 仅 polish.py：实际请求的 URL（便于核查） |
| `http_codes` | int[] | 仅 polish.py：每个 chunk 实测 HTTP 码（如 `[200]`） |
| `mode` | string | `languagetool` / `local-fallback`（polish）；mechanical 省略 |
| `n_chunks` | int | 分块数（polish） |
| `n_findings` | int | 发现总数 |
| `by_category` | obj | 仅 mechanical：各类别计数 |

## 2. 单条 finding 字段（统一契约）

| 字段 | 类型 | 必填 | 说明 |
|------|------|:--:|------|
| `line` | int | YES | 在**原始全文**中的行号（1 起） |
| `col` | int | YES | 列号（1 起）；分块后已映射回绝对位置 |
| `rule` / `category` | string | YES | 规则 ID（polish，如 `EN_A_VS_AN`）或类别（mechanical） |
| `issue` | string | YES | 问题的人类可读说明 |
| `suggestion` | string\|null | YES | 修改建议；无确定建议时为 `null` |
| `context` | string | YES | 命中片段前后约 25 字符，定位用 |
| `source` | string | polish | `languagetool` / `local`（mechanical 用 `category` 区分） |

> 约定：`line/col/issue/suggestion/context` 五字段两脚本**必然都有**，
> 因此可直接 `findings = polish.findings + mechanical.findings` 后按
> `(line, col)` 排序合并展示。

## 3. mechanical_check 的 category 取值
- `overclaim` — 无证据夸大词（significant/novel/outperforms…）；统计语境的 significant 已豁免不报
- `claim_strength` — 强主张词（prove/conclusively/guarantees/always…）给降级替换建议（Hedging 校准阶梯，见 argument_review.md §2）
- `ai_tone` — AI 腔/填充语（in conclusion/it is worth noting…）
- `hedge_stacking` — 一句内堆叠 >=2 个 hedge
- `passive_overuse` — 段落被动句占比超阈值（默认 0.4）
- `passive_voice` — 单条被动构造（细粒度，上限 50 条）
- `punctuation` — em-dash 间距 / 全角标点 / 多空格 / 标点前空格

## 4. 严重度建议（人工分级，非脚本输出）
脚本只报"事实命中"，不替作者判定 severity。落到审稿语境时按下表归并：

| severity | 对应类别 | 处理 |
|----------|----------|------|
| major | overclaim（裸论断）、claim_strength（强主张超证据）、passive_overuse、soundness 类 | 必改，可能影响录用 |
| minor | ai_tone、hedge_stacking、punctuation、单条 grammar | 表述层，统一清理 |

## 5. 与四步流水线（distill->critique->polish->audit）对接
- **critique** 阶段：跑 `mechanical_check.py` 先扫 overclaim / ai_tone，定位"裸论断"。
- **polish** 阶段：跑 `polish.py`（LanguageTool）做语法/风格逐条核对。
- **audit** 阶段：合并两份 findings，按 `(line,col)` 复核一致性/标点/术语。
- 每条最终修改仍按 SKILL.md 四栏输出：**原句 -> 问题诊断 -> 修改后 -> 为什么更好**。

## 6. 诚实性约束
- `polish.py` 的 `_meta.http_codes` 记录**运行时真实** HTTP 码，不预填。
- 端点不可达时 `mode` 自动转 `local-fallback`，不静默伪造 LanguageTool 结果。
- 脚本只报命中，不杜撰文献/数据；建议替换文本来自 LanguageTool `replacements`
  或离线正则，均可溯源。
