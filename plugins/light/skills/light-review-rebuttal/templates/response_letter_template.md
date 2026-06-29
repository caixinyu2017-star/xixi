# Response Letter / Rebuttal 模板（会议 + 期刊双模）

> 用法：**先定语境**。会议 rebuttal 与期刊 response letter 规则相反——会议常限 1 页/限字、
> 多数禁新实验/禁新材料、定位是"答急迫问题+指事实错误"而非开启对话；期刊鼓励逐点补实验、附新结果。
> 选对应区块，删掉另一个。所有 `<...>` 占位符替换后删除尖括号。
> 编号约定：每点 `P<审稿人>.<序号>`（P1.1、P2.3），支持跨点交叉引用（回 R2 时引对 R1 的回应）。
> R→A→C 三段：Reviewer Comment → Author Response → Changes Made（标页/行/图表号）。

---

# ========== 模式 A：期刊 RESPONSE LETTER（逐点，鼓励补实验） ==========

## Manuscript Information
- **Manuscript ID**: <MS-ID>
- **Title**: <论文标题>
- **Authors**: <作者列表>
- **Journal / Section**: <期刊 / 栏目>
- **Decision**: <Major Revision / Minor Revision>
- **Submission date of revision**: <YYYY-MM-DD>

## Summary of Changes（变更摘要，300–500 字）
We thank the Editor and all reviewers for their constructive feedback. The manuscript
has been substantially revised. The principal changes are:

- **Major**: <列致核心论点/方法的大改，如新增实验、重做分析>
- **Structural**: <章节重组、图表增删>
- **New content**: <新增小节/图/表，给编号>

All changes are marked in <颜色/tracked changes> in the revised manuscript. Page and
line references below refer to the **revised** version unless noted as "(orig.)".

---

## Reviewer 1

**Strengths Acknowledged.** We are grateful that the reviewer found <复述审稿人认可的优点>.

### P1.1 — <一句话标题，最重要的问题排第一>
> **Reviewer Comment (P1.1):** <逐字引用审稿意见>

**Author Response.** <感谢 + 直接回应；同意则说明如何处理，不同意则带证据反驳，
绝不只写 "we disagree">。

**Changes Made.** <具体改了什么 + 位置：p.X, lines Y–Z / Fig. N / Table M>。
若新增实验：<结果一句话 + 指向图表>。

### P1.2 — <次要问题标题>
> **Reviewer Comment (P1.2):** <引用>

**Author Response.** <回应>

**Changes Made.** <改动 + 位置>

#### Minor (P1.m1–P1.m3) — 编辑性问题合并
- **P1.m1** > <typo/措辞> — Fixed, p.X line Y.
- **P1.m2** > <格式> — Fixed, p.X.
- **P1.m3** > <引用补全> — Added ref [N], p.X.（新引文献先过三索引核验避免引用幻觉）

---

## Reviewer 2

**Strengths Acknowledged.** <致谢>

### P2.1 — <标题>
> **Reviewer Comment (P2.1):** <引用>

**Author Response.** <回应。若与 R1 共同质疑，标注 "This concern was also raised by
Reviewer 1 (P1.1); we addressed it by ..." 并交叉引用，体现多审稿人共识=最高优先级>。

**Changes Made.** <改动 + 位置>

#### Minor (P2.m1–) 
- **P2.m1** > <小问题> — Fixed, p.X.

---

## Reviewer 3
（按需复制 Reviewer 2 区块）

---

## Closing
We believe the revised manuscript addresses all concerns and is substantially stronger.
We thank the reviewers again for their time and expertise.

<br>

# ========== 模式 B：会议 REBUTTAL（限 1 页，禁新实验，less is more） ==========

> **铁律**：(1) 通常限 1 页/限字，用官方模板；(2) 多数会议禁加新实验/新结果、禁给代码链接/
> 上传新材料（算超出原稿）——只能放澄清性图/例（解释稿件已有内容）；(3) 定位=答急迫问题、
> 指会致拒稿的事实错误、申诉不道德评审（走机密通道），**不是开启对话**；(4) 越短越 crisp
> 越能说服；四审全 reject 基本翻不了案，不必硬写。

## Manuscript Information
- **Paper ID**: <编号> · **Title**: <标题> · **Venue**: <ICLR/NeurIPS/IJCAI ...>

## General Response（可选，仅当多审稿人共同质疑同一点时用）
We thank all reviewers. Two concerns were shared across reviews; we clarify them here
to avoid repetition:
- **(C1)** <共同质疑 1 + 一句话澄清，指向稿件已有的 §X / Fig.Y（不引入新结果）>
- **(C2)** <共同质疑 2 + 澄清>

## To Reviewer <R1 的匿名 ID>（Rating: <x>, Confidence: <y>）
- **[Q1]** > <审稿人急迫问题/事实质疑，精简引用>
  <回应：直接、聚焦；事实错误则明确指出"This is a factual misunderstanding: as stated
  in §X / Eq.(n), ..."；澄清则指向稿件已有内容，不承诺超纲新实验>。
- **[Q2]** > <问题>
  <回应>

## To Reviewer <R2 的 ID>（Rating: <x>, Confidence: <y>）
- **[Q1]** > <问题>
  <回应。若该点已在 General Response 答过，写 "Please see (C1) above." 省字>。

> 提交前自查（会议）：是否超 1 页？是否塞了审稿人没要的新结果/新实验/代码链接？
> 是否情绪化？能删的礼貌套话删了吗？每条回应是否指到稿件具体 §/式/图？

