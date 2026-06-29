# R4.2 AI 生成图像政策 — 出版商实查留痕

- 研究日期：2026-06-11
- 执行：Claude Opus 4.8（Claude Code）
- 任务：figure_integrity.md 新增「AI 生成图像政策」节，≥3 家出版商原文链接实查。

## 1. Elsevier（完整原文实查 ✓ WebFetch 成功）

来源：https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-writing-for-elsevier

原文关键句（WebFetch 取得）：
> "Elsevier does not permit the use of generative AI or AI-assisted tools to
> create or alter images in submitted manuscripts."

- 覆盖范围：增强/遮盖/移动/移除/引入图像内的特征均禁止。亮度/对比度/色彩平衡调整
  仅在「不消除原图信息」时允许。
- **唯一例外**：AI 成像本身是研究设计/方法的一部分——须在 methods 节可复现描述
  （模型/工具名、版本、扩展号、厂商），并可能被要求提交调整前原图供编辑审查。
- 文本：AI 辅助写作须披露，正文末尾 references 前加
  "Declaration of Generative AI and AI-assisted technologies in the writing process"
  （拼写/语法检查豁免）。

## 2. Nature / Springer Nature（政策立场多源核实 ✓；原文页登录墙 ⚠️）

一手来源（WebSearch 命中，确认存在）：
- 社论 "Why Nature will not allow the use of generative AI in images and video"
  （2023-06-07）：https://www.nature.com/articles/d41586-023-01546-4
- 编辑政策页：https://www.nature.com/nature-portfolio/editorial-policies/ai

政策立场（WebSearch 摘要 + 多源一致）：
- Nature **不发表**生成式 AI 制作的图像、视频、插图（general rule），
  理由：integrity / consent / privacy / IP 保护。
- 区分：文本可在披露前提下有限使用（LLM 不得列为作者）；图像/视频则整体不允许。
- ⚠️ **GAP**：原文页 `nature.com/.../editorial-policies/ai` 与社论页均 303 重定向到
  `idp.nature.com` 登录授权，WebFetch 无法取得逐字引文。立场经 Nature 官方社论标题、
  Ars Technica（2023-06-12）、Artnet（2023-06-14）多源一致核实，确切措辞待登录核验。

## 3. Science / AAAS（政策立场多源核实 ✓；原文页 403 ⚠️）

一手来源（WebSearch 命中，确认存在）：
- "ChatGPT is fun, but not an author"（Science 社论, 2023-01, Thorp）:
  https://www.science.org/doi/10.1126/science.adg7879
- "Change to policy on the use of generative AI and large language models"
  （AAAS, 2023-11-16）:
  https://www.science.org/content/blog-post/change-policy-use-generative-ai-and-large-language-models

政策立场（WebSearch 摘要 + 多源一致）：
- 2023-01 初版：文本/图/表/图形均不得为 AI 产物，AI 不得署名。
- 2023-11 修订：放松 AI 辅助**文本**（须披露），但**图像/图表限制仍更严**——
  AI 生成图像/图形/视频一般仍禁止，除非获编辑明确许可。
- ⚠️ **GAP**：science.org 政策页返回 HTTP 403，WebFetch 无法取得逐字引文。
  立场经 AAAS 官方页标题、Times Higher Education（2023-11-16）多源一致核实。

## 4. 共性结论（写入 figure_integrity.md）

三家头部出版商口径一致：**生成式 AI 直接生成/篡改论文图像（figure/插图/显微图等）
一律禁止**；唯一普遍例外是「AI 本身是研究对象/方法」（须在 methods 可复现披露）；
AI 辅助**文本**则普遍可在披露前提下使用。→ 故 Light 的 R6 PPT 生图流水线
**严禁进入论文图链路**，仅服务 PPT/路演/前端灵感。

## 5. 诚实声明
Elsevier 为逐字原文实查；Nature/Science 为政策立场多源核实、原文确切引文因登录墙/403
未取得（标 GAP）。三家政策页 URL 均已确认存在且为官方域名，引用前建议复查最新版本
（出版商政策持续更新）。
