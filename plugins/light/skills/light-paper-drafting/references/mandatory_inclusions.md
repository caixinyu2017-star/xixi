# Mandatory Inclusions（必备声明）+ AI 使用声明模板

提交前的"声明位"收口清单。多数 venue 缺这些会被退稿或编辑部退回补充。
具体措辞与是否强制因 venue 而异，**投稿前以目标 venue 当年作者须知为准**；下列为通用骨架模板。

---

## 1. 必备声明清单（逐项勾，N/A 也要显式写明）

| 声明 | [ ] | 何时必填 | 一句话要点 |
|---|---|---|---|
| **Data Availability** | [ ] | 几乎所有期刊 | 数据在哪/怎么获取；不可公开则说明原因与受限获取途径 |
| **Code Availability** | [ ] | 计算类研究 | 代码仓库链接或"可应请求提供"；双盲下用匿名仓库 |
| **Ethics Statement** | [ ] | 涉人/动物/敏感数据 | IRB/伦理委员会批准号；动物实验遵 ARRIVE |
| **Informed Consent** | [ ] | 涉人受试者/个案 | 已获知情同意；个案另需发表同意 |
| **CRediT Contributions** | [ ] | 多数期刊 | 按 CRediT 14 角色分工（见下） |
| **Conflicts of Interest (COI)** | [ ] | 所有 | 利益冲突；无则写 "The authors declare no competing interests." |
| **Funding** | [ ] | 所有 | 资助方与项目号；无则 "This research received no specific grant..." |
| **AI Use Disclosure** | [ ] | 越来越多 venue 强制 | 见第 3 节按 venue 模板 |

---

## 2. CRediT 14 角色（贡献声明用）

Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Resources, Data Curation, Writing – Original Draft, Writing – Review & Editing, Visualization, Supervision, Project administration, Funding acquisition.

模板：
> **CRediT:** A.B.: Conceptualization, Methodology, Writing – Original Draft. C.D.: Software, Validation. E.F.: Supervision, Funding acquisition.

---

## 3. AI 使用声明模板（按 venue 取用）

> 通用原则：声明用了哪个工具、用在哪个环节（措辞润色 / 代码 / 文献检索 / 生成内容）、作者对全部内容负责。AI **不得**列为作者。
>
> **先查目标 venue 政策**：取稿模板前先查 db01 该 venue 的 `risk_note` 里 `ai_policy=` 子串（R4 已实查头部 venue），按其口径定声明范围——期刊普遍**禁止 AI 生成图像**（图像若涉 AI 须落 methods 可复现披露，见 light-figure-drawing `light-figure-drawing/references/figure_integrity.md`）、文本须披露；会议（NeurIPS/ICLR/CVPR 等）普遍允许 LLM 但要求作者对全文负责、AI 不得署名、未验证的 LLM 生成引用会被拒/撤稿。venue 无 ai_policy 值时回查其官网最新作者须知。

**通用 / 多数期刊（Elsevier/Springer 风格）**
> During the preparation of this work the author(s) used [TOOL] in order to [improve language and readability / assist with code]. After using this tool, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication.

**Nature / Science 系**
> Generative AI tools were used for [language editing only]. No AI tool is listed as an author. All scientific content, analysis, and conclusions are the authors' own, and the authors take full responsibility.

**ACL / EMNLP（ACL Policy）**
> We disclose the use of [TOOL] for [writing assistance / coding assistance / research ideation]. Use was limited to [scope]; all claims, experiments, and citations were verified by the authors.

**ICLR / NeurIPS**
> LLMs were used for [editing / coding assistance]. The authors verified all content; any LLM use central to the methodology is described in the main text. No LLM is credited as an author.

**未使用 AI 时（若 venue 要求显式声明）**
> The authors declare that no generative AI tools were used in the preparation of this manuscript.

---

## 4. 收口判据
- 每条声明非填即标 N/A 并说明；不得留空。
- AI 声明的 scope 必须与实际一致（对接 self_review_checklist 的 M6 方法学造假：别声明没做的，也别瞒做了的）。
- 涉人/动物研究无伦理声明 → 视为不可提交。
- `scripts/draft_lint.py` 可机检关键声明小节是否存在。