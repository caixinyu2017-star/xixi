# 深层论证审查

语法谁都会查，真正决定论文成败的是论证。这份规范把"深层优先"落成可操作的四个审查环，配合审稿人五问一起用。区别于通用语法检查（那是表层）。

## 1. Claim–Evidence–Boundary（每个科学陈述三件套）

论文里每一句"我们发现/证明/表明……"的科学陈述，都要同时具备三件：

- **Claim 主张**：你声称什么。
- **Evidence 证据**：哪个实验/数据/引用/推导支撑它（指得出来，不是"显然"）。
- **Boundary 边界**：在什么条件/范围内成立，不确定性多大。

逐句过，修复这四类高频失败：

| 失败类型 | 症状 | 修法 |
|----------|------|------|
| 有主张无证据 | "X 显著提升性能"但没指向数据 | 补证据指向，或降为假设语气 |
| 有数据无观点 | 堆了一段数字却没说明它意味着什么 | 加一句"这说明……" |
| 有推论无边界 | 把单数据集结论写成普遍规律 | 加适用范围限定（"在 X 设定下"）|
| 相关被写成因果 | "A 提高导致 B 下降"但只有相关性 | 改为"A 与 B 负相关"，或补因果论证 |

最后一类（相关→因果）最致命，审稿人必抓。

## 2. Hedging 校准阶梯（主张强度匹配证据强度）

主张的语气强度，要和证据强度对齐。从强到弱：

```
demonstrate / prove(慎用) → show / indicate → suggest / point to → may reflect / could be
   铁证(理论证明/大样本重复)        强证据         中等证据            初步/单次/小样本
```

审查动作：
- 证据弱却用强词（"prove" "conclusively" "definitively"）→ 降级。
- 证据强却过度对冲（什么都 "may possibly suggest"）→ 适度上调，别把确定的结果写得心虚。
- 过度宣称黑名单 → 安全替换（`mechanical_check.py` 已扫 overclaim 词）：
  - `prove → show` / `unprecedented → to our knowledge the first` / `best/superior → among the strongest / outperforms on X` / `significantly(非统计语境) → substantially`。

## 3. 章节责任分工（各章节只说该说的话）

润色时按章节定位检查"这句话放对地方了吗"：

- **Results**：只陈述观察到的事实（过去时 + 定量）。**不在这里堆机制解释**——"because/due to 某机制"属于 Discussion。
- **Methods**：必须能复现。拒绝含糊话："under standard conditions"、"routine procedures"、"data were analyzed statistically"（哪个检验？）——都要具体到可复现。
- **Discussion**：解释、推测、含义、局限的家。Hedging 主要在这里。也是承认 boundary 的地方。
- **Intro/Discussion 沙漏结构**：Intro 由宽到窄收到本研究；Discussion 由具体发现展开到更宽含义 + 限制。

## 4. AI 使用披露（合规，别漏）

用了 AI 辅助写作/润色，投稿前要按目标期刊政策披露。要点：
- **AI 不能列为作者**（无法对内容负责）——主流出版商（Nature/Springer、ICMJE 等）的硬规则。
- **作者对全部内容负全责**，包括 AI 生成部分的准确性。
- **不得用 AI 编造**引用、数据、机制。

两版可粘贴模板（具体措辞以目标期刊最新政策为准，详版在 m07 paper-drafting 的声明模板）：

- **Methods/方法版**：「During the preparation of this work the author(s) used [工具名] to [润色语言/改善可读性]. After using this tool, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.」
- **致谢版**：「The author(s) acknowledge the use of [工具名] for language editing. All scientific content and conclusions are the author(s)' own.」

完整声明（含数据/代码可用性等）回 m07 `references/mandatory_inclusions.md`。

## 与审稿人五问的关系
审稿人五问（soundness/novelty/clarity/reproducibility/related-work）是"审什么维度"；本文四环是"怎么改"。soundness ↔ CEB + Hedging；reproducibility ↔ 章节分工的 Methods 部分；合规 ↔ AI 披露。两者配套用。
