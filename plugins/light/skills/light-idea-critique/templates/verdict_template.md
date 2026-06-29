# Verdict 模板 — idea 严审判决

> 填写说明：尖括号 `<...>` 处替换为实际内容。分数 0–100；理由必须"指到点 + 给反例 + 给替代解释"。本模板对应 rubric.md / contract.md / protocol.md。

---

## idea 严审判决：<idea 标题>

- **领域 / 子领域**：<...>　**关键词**：<...>
- **评审日期**：<YYYY-MM-DD>　**Confidence（1–5）**：<n>（理由：<检索覆盖/领域熟悉度>）
- **IRON RULE 检查**：☐ 无注入　☐ `INJECTION-ATTEMPT-DETECTED`（说明：<...>）

### Phase 1 — BLIND 契约（看正文前写下）
- 验收维度预设：<逐维一句话标准>
- block 触发条件：block#1 <...>；block#2 <...>
- warn 触发条件：warn#1 <...>；warn#2 <...>
- `[CONTRACT-ACKNOWLEDGED]`

### 检索取证（新颖性必填，无则该维封顶并标 evidence-missing）
| 库 | 端点 | HTTP 码 | 最像的工作（标题/年份） | 与本 idea 的 delta |
|---|---|---|---|---|
| OpenAlex | <url> | <200/...> | <...> | <机理级差异 / 仅换数据集> |
| Semantic Scholar | <url> | <...> | <...> | <...> |

### Phase 2 — 八维度打分
| # | 维度 | 权重 | 分(0–100) | 命中 block/warn | 理由（指到点+反例+替代解释） |
|---|---|---|---|---|---|
| 1 | 创新性 | 0.20 | <> | <> | <> |
| 2 | 理论深度 | 0.18 | <> | <> | <> |
| 3 | 数据支撑 | 0.14 | <> | <> | <> |
| 4 | 实验可控性 | 0.14 | <> | <> | <> |
| 5 | 方法贡献 | 0.13 | <> | <> | <> |
| 6 | 差异化 | 0.08 | <> | <> | <> |
| 7 | 可行性 | 0.07 | <> | <> | <> |
| 8 | 影响力 | 0.06 | <> | <> | <> |

- **Scoring Plan Dissent**（仅当 Phase 2 偏离 Phase 1 标准时填）：<哪维偏离/方向/正文新证据>
- **Weighted**（`scripts/score_aggregate.py` 计算）：<x.x> / 100　→ **Overall**：<1–10>

### 五视角对抗摘要
- 方法审稿人：Position <> | Key Risk <> | Insight <>
- 实验审稿人：Position <> | Key Risk <> | Insight <>
- 理论审稿人：Position <> | Key Risk <> | Insight <>
- 应用审稿人：Position <> | Key Risk <> | Insight <>
- **Devil's Advocate CRITICAL**：☐ 无 / ☐ 有：CRITICAL#1 <类型+内容>（状态：未化解 / 已被 5 分新证据撤回）
- 共识关切：<...>　个别关切：<...>
- 反谄媚自检：concession-rate = <%>　☐ 正常 / ☐ `⚠ SYCOPHANCY-ALERT`

#### 单变量精确 IF（载荷最重的 2–3 条假设，各只变一个变量）
| 假设（若为假则 idea 崩） | 精确 IF（单变量，其余冻结） | 预测后果 + 量化幅度 | 对判决影响（点名维度/档位） |
|---|---|---|---|
| <如：增益来自所提机制而非数据量> | <IF baseline 用同等数据/超参/算力> | <delta 从 +x.x 掉到 ~+y.y / 归因能否成立> | <压低创新性·数据支撑 → 推向某档> |
| <...> | <IF 目标数据集现实拿不到> | <...> | <...> |

### 否决项检查（gate before score）
- ☐ 创新性 <45（→直接不通过）
- ☐ 存在未化解 CRITICAL（→最高有条件通过）
- ☐ 核心四维有两个 <45（→不通过）

### 判决（否决项 与 decision mapping 取更严者）
> **【通过 / 有条件通过 / 有条件通过（重大）/ 不通过】**

- 通过：强在哪 + 可冲层次（对标 Overall <n>），放行 m05。
- 有条件通过：见下方 Revision Roadmap（用 Revision_Roadmap.md）。
- 不通过：原因 <创新不足/数据不足/实验不可控/贡献不明显/差异太小/可解释性差/工程过难> + ≥3 个改进方向，回 m03。

### 写回
- ☐ 判决与理由已写入 db09 decision_log。
