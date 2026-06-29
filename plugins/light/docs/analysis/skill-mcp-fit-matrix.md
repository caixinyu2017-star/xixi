# 技能 × MCP 适配表

> 2026-06-13 ｜ 5 个推荐 MCP（[[light-mcp-recommended-set]]）逐技能落点判断。**该接的接、不该接明说不接，不硬塞凑数。**
> 方法：Explore agent 实读 28 技能 SKILL.md 职责 + 实测核对"已接"。MCP 能力见 mcp-revamp-log.md。
> 重要纠正：competition 正文的 "Canva" 是 **Lean Canvas 精益画布**，非 Canva MCP——原 grep 基线误判，competition 实际未接 Canva。

## MCP 能力速记
| MCP | 用途 | 不适用 |
|---|---|---|
| Figma | 读设计稿→前端 UI 出码 | 非前端的一切 |
| Canva | 路演 PPT/海报/品牌物料(生成+导出) | 数据图、论文图 |
| Draw.io | diagram-as-code 框架/系统/流程/架构/ER 图(XML 可版本控制) | 统计数据图、3D |
| Blender | 3D 科学可视化(分子/结构/天文)、路演 3D 渲染 | 2D 数据图、论文数据图须谨慎 |
| MATLAB | 跑本地 MATLAB 信号/控制/数值/Simulink | 非数值/Python 生态 |

## 适配矩阵（✅已接 / ➕可接未接(本轮补) / —不该接 / 空=无关）

| 技能 | Figma | Canva | Draw.io | Blender | MATLAB |
|---|---|---|---|---|---|
| tool-selection | ➕ | ✅ | ➕ | ➕ | ✅ |
| figure-planning | | | ✅ | ✅ | ➕ |
| figure-drawing | | | ➕ | ✅ | ✅ |
| frontend-design | ✅ | — | — | — | — |
| slides | — | ✅ | ➕ | ✅ | — |
| competition | | ➕ | ➕ | ➕弱 | |
| system-design | | | ➕ | | |
| ip-application | | | ➕ | — | |
| backend-coding | | | | | ➕弱 |
| 其余 19 技能 | 无 MCP 落点（见下） | | | | |

> 无 MCP 落点（纯方法论/审计/规划/分析，生产委托下游）：citation、consistency、data-engineering、file-reading、idea-critique、idea-generation、literature-search、memory-pm、orchestrator、paper-drafting、paper-polishing、project-structure、research-ethics、research-plan、result-analysis、review-rebuttal、self-review、typesetting、venue-matching。
> 边界说明：research-plan/result-analysis 只规划/分析、出图出仿真委托 figure-drawing/backend-coding，MCP 落点在下游；consistency 是审计器不生产物料；data-engineering 栈是 pandas/DuckDB 非数值计算。

## 本轮要补的"可接未接"（➕）
- **T1 tool-selection**：前端项加 Figma MCP、绘图项加 Draw.io MCP、新增 3D→Blender MCP，进 MCP 发现清单（元路由中枢，收益最大）
- **T2 system-design**：架构/分层/数据流/ER 图用 Draw.io MCP（最强落点，职责明确要"写进软著/论文"，比现有 Mermaid 表达力强可版本控制）
- **T3 ip-application**：专利附图(流程/结构/框图)用 Draw.io MCP 出黑白线条 diagram-as-code（符合专利附图要求、便于按代理人改）
- **T4 figure-drawing**：框架图工具组补 Draw.io MCP（与 figure-planning 已列 drawio 对齐）
- **T5 slides**：流程/架构/路线图用 Draw.io MCP 出图嵌入（守文本落原生框、数据图走 m11 红线）
- **T6 competition**：路演 PPT/海报用 Canva MCP、技术路线/架构图用 Draw.io MCP（数据图仍 m11；Blender 仅产品/装置类弱落点）
- **T7 figure-planning**：信号/控制/数值仿真类图的"建议工具"补 MATLAB（执行端已支持，规划端补齐闭环）

## 执行进度
- ✅ T1 tool-selection — 绘图项加 Draw.io、新增 3D→Blender 行、前端项加 Figma；MCP 发现节加 5 推荐 MCP 路由指引（能力/费用单一真相源指向 README 表不复写，口径同 OpenAlex key）
- ✅ T2 system-design — ER 图节补 Draw.io MCP（复杂架构/分层/数据流/ER 图，可版本控制写软著论文，比 Mermaid 强）
- ✅ T3 ip-application — 专利附图节补 Draw.io MCP（黑白线条流程/框图，diagram-as-code 便于按代理人改稿，仍核标记线/术语）
- ✅ T4 figure-drawing — 框架图工具组补 Draw.io（要可编辑矢量源+版本控制的系统/架构图，与 m09 对齐）
- ✅ T5 slides — 实现工具加 Draw.io 流程/架构/路线图嵌入（守文本落原生框、数据图走 m11 红线）
- ✅ T6 competition — 路演 deck 加 Canva MCP、技术路线/架构图加 Draw.io MCP（数据图仍 m11）
- ✅ T7 figure-planning — 工具速查加信号/控制/仿真类图的 MATLAB（执行端已支持，规划端补齐闭环）
- ✅ 四 CI 全绿 + 记忆更新

---

## 结论
逐技能 MCP 适配做完：9 技能有落点，已接 7 处 + 本轮补 7 处「可接未接」（T1-T7，集中在 Draw.io 的 diagram-as-code 用途）；19 技能明确无 MCP 落点不硬塞。**纠正了 competition 的 Canva 误判**（实为 Lean Canvas 精益画布）。所有补充都指向 README 推荐 MCP 表作单一真相源、不复写费用，守"不该接明说不接"。四 CI 全绿。
