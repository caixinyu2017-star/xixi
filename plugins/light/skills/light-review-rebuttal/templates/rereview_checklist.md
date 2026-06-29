# Re-review 自我复审清单（提交前必做）

> 用途：提交返修稿/rebuttal **之前**，自己当一次刻薄的复审者，独立核实"每条声称的修改
> 是否真的落地"。核心反模式 = false success claims（"已按建议修改"式空声称）。
> 判定四态：**FULLY / PARTIALLY / NOT_ADDRESSED / MADE_WORSE**。
> 可溯源规则：对每条意见①读作者声称②跳到声称的修改位置③独立核实声称与实际改动一致；
> 作者声称为空或含糊即标 🔍 **Cannot verify**，打回重写。

## 优先级定义
- **Priority 1**：多审稿人共同质疑 / 致拒稿的方法学或事实问题 / Critical(需补实验或改证明)。
  **全部必须 FULLY，否则不提交。**
- **Priority 2**：单审稿人重要质疑 / 返修周期内应解决 / Important。
- **Priority 3**：编辑性、措辞、格式、补引用 / Minor。

---

## Priority 1 复审表

| ID | 审稿意见(摘要) | 作者声称(Author's Claim) | 声称的修改位置 | 独立核实结果 | 判定 |
|----|----------------|--------------------------|----------------|--------------|------|
| P1.1 | <意见> | <作者说改了什么> | p.X / Fig.N / §M | <你跳过去看到的实际改动> | FULLY / PARTIALLY / NOT / WORSE / 🔍 |
| P1.2 |  |  |  |  |  |
| P2.1 |  |  |  |  |  |

判定规则：声称为空/含糊("已按建议修改"无定位) → 🔍 Cannot verify → 打回。
任一 Priority-1 非 FULLY → 不提交，回去补。

## Priority 2 复审表

| ID | 审稿意见(摘要) | 作者声称 | 位置 | 核实结果 | 判定 |
|----|----------------|----------|------|----------|------|
| P_.. |  |  |  |  |  |

## Priority 3 复审表（编辑性，批量核）

| ID | 问题 | 是否已改 | 位置 |
|----|------|----------|------|
| P_.m1 |  | ✅/❌ | p.X |

---

## Commitment Ledger（承诺账本）

> 把每条意见解析出的"承诺"逐条登记并核验。证据类型决定核验位置：
> new_section/figure/table/citation → 在**修改稿**核验；acknowledgment_only → 在
> **response letter**核验；prose_edit → 核验具体句子。
> 状态四选一：**fulfilled / partial / not-fulfilled / explicitly-rejected-with-rationale**。
> 非 fulfilled 项必须带 rationale，否则报 **COMMITMENT_GAP**。
> explicitly-rejected 项须登记理由且可被复审重新审视（带"重审日期"，类比可过期例外）。

| Ledger ID | 承诺内容 | 证据类型 | 核验位置 | 状态 | Rationale(非 fulfilled 必填) | 重审日期 |
|-----------|----------|----------|----------|------|------------------------------|----------|
| L1 | <承诺补 X 实验> | figure | Fig.N | fulfilled |  | — |
| L2 | <承诺加文献综述> | new_section | §2.3 | partial | <还差 Y，下轮补> | — |
| L3 | <拒绝改方法> | — | — | explicitly-rejected | <带证据的理由> | <YYYY-MM-DD> |

## 分数轨迹（防越改越糟，跨轮跟踪）

| 维度 | 上轮分 | 本轮自评 | Δ | 触发 checkpoint(Δ<-3?) |
|------|--------|----------|---|------------------------|
| Soundness |  |  |  |  |
| Clarity |  |  |  |  |
| Contribution |  |  |  |  |

## 最终放行门
- [ ] 所有 Priority-1 = FULLY，无 🔍
- [ ] 承诺账本无 COMMITMENT_GAP（非 fulfilled 均带 rationale）
- [ ] 无分数 Δ<-3 未解释
- [ ] （会议）未超页/未塞超纲新材料；（期刊）每条"已修改"声称都能跳到具体改动
- [ ] 每条审稿意见都回了，无遗漏
