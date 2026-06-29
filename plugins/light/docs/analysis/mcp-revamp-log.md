# MCP 推荐配置改造台账（Figma/Canva/MATLAB/Draw.io/Blender）

> 起始 2026-06-13 ｜ 范围（已拍板）：**README 推荐 MCP 表 + 技能引用 + references 全做**；MATLAB **按实测改正**过时说法；删 BioRender；Draw.io/Blender 按真实能力合理融入（非顶替 BioRender 图位）。
> 诚实底线：star/项目名/能力/费用全用**实测值**（5 个并行检索代理已查，2026-06-14 GitHub API）；查不到标 unknown；Blender "MCP 驱动科研可视化"**实践尚少**，文案写"设想方向"不写成既成事实；论文图禁 AI 生成底线不受影响（Draw.io 是 diagram-as-code、Blender 是程序化建模，均非 AI 生图）。

---

## 实测事实底盘（写进 references/README 的依据）

### Figma — 官方 MCP，能读能写，免费档可用
- 官方 Figma MCP server：**Remote server 所有 plan 含免费账号可用**（纠正原 README"仅 Dev Mode 付费"）；Desktop/local 版需付费 Dev/Full seat。能读（frame→代码、design context、Code Connect）+ 写（创建/改 canvas 原生内容，写功能 beta 期免费）。docs: developers.figma.com/docs/figma-mcp-server/
- 热门 GitHub：GLips/Figma-Context-MCP(Framelink) **~15.1k★** MIT；grab/cursor-talk-to-figma-mcp **~6.8k★**。
- 科研用法：读设计稿→实现前端（实验平台/标注工具/项目主页）。**学术 figure 用法 unknown，不当 figure 路径**（与论文图禁 AI 底线一致）。

### Canva — 官方 MCP，能创建/编辑，核心免费
- 官方两个 MCP：①Canva（设计）MCP `mcp.canva.com/mcp`（2025-06，能生成/编辑/检索/导出 PDF/PNG/PPTX，核心功能任意账户可用；缩放→Pro；autofill/brand template→Enterprise）②Dev MCP（写 Canva app 代码，非设计）。docs: canva.dev/docs/mcp/
- 热门 GitHub：社区项目 star 都很低（canva-gemini-extension 33★ 等），官方远程 server 已够用。
- 科研/路演用法：答辩/路演 PPT（生成→导出 PPTX）、海报、品牌模板批量填充（限 Enterprise）。

### MATLAB — 官方开源 MCP 跑本地 MATLAB，不需 Production Server（⚠ 改正过时说法）
- **MATLAB MCP Core Server**（matlab/matlab-mcp-core-server，**~965★**，2025-11 开源，Go）：跑**本地普通 MATLAB**（R2021a+），**不需要 Production Server 商业许可**。能力：detect_toolboxes/check_code/evaluate_code/run_file/run_test。
- 另有 MCP Framework for MATLAB Production Server（~25★）——**这条才**需 Production Server（商业部署）。
- ⚠ 费用诚实点：Core Server 不需商业许可，但**本地 MATLAB 本身需购买**；学生版/家庭版能否用于 MCP 自动化**官方未明写**，标"需自查 MathWorks 许可协议"。
- 社区：WilliamCloudQi(54★)/Tsuchijo(38★)/sohumsuthar/simulink-mcp(16★) 等，调本地 MATLAB engine，不需商业许可（但受 MATLAB 自身 license 约束）。
- 科研用法：信号处理/控制/数值计算/Simulink 仿真/结果复现。

### Draw.io — 官方 MCP + diagram-as-code，开源免费
- 官方 **jgraph/drawio-mcp ~4.4k★** Apache-2.0（4 种集成：App Server/Tool Server `@drawio/mcp`/Claude Code Skill+CLI/Project Instructions，含 10000+ 形状索引）；社区 lgazo/drawio-mcp-server **~1.3k★**（v2.1.1 2026-06-02，npm+PyPI）。
- 程序化：CLI `drawio --export --format png/svg/pdf`（⚠ 26.0→26.2 flag 不兼容 issue#2057，脚本锁版本；无头需 xvfb-run）；.drawio 即 mxGraph XML 可脚本拼装。
- 科研用法：框架图/系统架构/算法流程/技术路线，diagram-as-code 纳 Git 可 diff 可批量改。

### Blender — 官方+社区 MCP，3D 全能；⚠ MCP 驱动科研可视化实践尚少
- 热门：ahujasid/blender-mcp **~22.7k★** MIT（自然语言建模/改材质/查场景/跑任意 bpy Python/Poly Haven/Hyper3D 生成）；**Blender 基金会官方 Lab MCP**（Anthropic 2026-04 赞助，star unknown 在 Gitea，需 Blender 4.2+，偏场景分析/技术美术）。
- 能力：创建/改 3D 对象/材质/灯光相机/执行任意 bpy；需本地装 Blender 跑。安全：execute_code 跑任意 Python，操作前先存盘。
- 科研用法（⚠ 区分）：**确有实践但多是直接用插件非 MCP**——Molecular Nodes（分子/PDB）、SciBlend（科研数据可视化）、AstroBlend（天文）、TheorChem2Blender（计算化学，有论文）。**"用 MCP 让 AI 驱动这些"目前是设想/早期探索，无成熟案例**——文案写"设想方向"。
- 论文图底线：Blender 是程序化建模渲染（非 AI 生图），但 3D 渲染图作为论文图需谨慎（数据真实性/可复现），路演展示用更稳妥。

---

## 执行进度（⬜待办 / 🔧完成）

- ✅ M-readme README.md + README.en.md 推荐 MCP 表：5 个（Figma/Canva/Draw.io/Blender/MATLAB），删 BioRender，MATLAB 改正（Core Server 不需商业许可、本地 MATLAB 需购买），费用按实测，加论文图禁 AI/3D 渲染谨慎说明
- ✅ M-figplan figure-planning：SKILL 删 BioRender 主路径（图表清单/工具速查），Draw.io 强化（官方 MCP+diagram-as-code+CLI 锁版本）、加 Blender 3D 科学可视化（标实践尚少/插件成熟/论文图谨慎）；BioRender 降为"需图标库时手工、其 MCP 仅查询不作图"
- ✅ M-frontend frontend-design：灵感来源节加"Figma MCP（读设计稿→前端实现）"——免费档可用/能读写/GLips 15.1k★，明确只用于前端界面不生成论文 figure
- ✅ M-slides slides：实现工具节加"3D 渲染配图（路演/展示用）"Blender 选项，严守三条硬边界（只作装饰展示配图、不作数据图、不进论文图链路），科研 3D 可视化指向 m09
- ✅ M-toolsel tool-selection：核对后**无需实质改动**——其 MCP 节是方法论层（发现/探测/安全评估通用纪律），不复写 README 的具体 MCP 费用表，符合 CONVENTIONS 单点沉淀原则；line16 MATLAB 仅作工具能力描述不涉 MCP 费用
- ✅ M-ref figure-planning references：drawio 节加官方/社区 MCP（实测 star+issue#2057 锁版本）；新增 Blender 节（ahujasid 22.7k★/官方 Lab MCP/Molecular Nodes/SciBlend，诚实标 MCP 驱动科研可视化实践尚少）；BioRender 并入 Blender 节末诚实说明
- ✅ M-consistency CHANGELOG（[Unreleased] 新增 Changed 条目记 MCP 表重订，保旧条目原貌不篡改）+ CONTRIBUTING（MCP 费用核对项更新为新五项口径 + star 实测/unknown 纪律）
- ✅ M-figdraw（核查补漏）figure-drawing(m11)：SKILL line23 BioRender 加"MCP 仅查询不作图、只手工用"+ 补 Blender 3D 选项；references BioRender 专节加同口径说明，指向 m09 Blender 节
- ✅ 四 CI 全绿（assets/links/entry/databases）；全仓 BioRender 残留核查：仅剩"手工用/MCP 仅查询"的诚实说明，无"可程序化/MCP 出图"误导表述
- ✅ 记忆更新

---

## 本轮 MCP 改造结论
README 推荐 MCP 表从 4 项（Canva/Figma/MATLAB/BioRender）重订为 5 项 **Figma · Canva · Draw.io · Blender · MATLAB**，全部基于 2026-06 联网实测（5 个并行检索代理）。
**实测校正（诚实底线）**：①MATLAB——官方 Core Server 2025-11 开源、跑本地 MATLAB 即可、**不需 Production Server 商业许可**（原"个人无法免费"说法已过时），但本地 MATLAB 付费、学生/家庭版用于 MCP 须自查许可；②Figma——Remote server 免费账号可用、能读能写（原仅写 Dev Mode 付费）；③删 BioRender——其 MCP 仅查询不能作图，降为"需图标库时手工用"。
**扩能力**：新增 Draw.io（开源，官方 jgraph/drawio-mcp 4.4k★，diagram-as-code，配 m09）、Blender（开源，社区 ahujasid 22.7k★/官方 Lab MCP，3D 科学可视化/路演渲染，配 m09/m16）。
**底线贯穿**：star/能力/费用全用实测值，查不到标 unknown；Blender"MCP 驱动科研可视化"诚实标"实践尚少、成熟路子是直接用 Molecular Nodes/SciBlend 插件"；论文数据图禁 AI 生成底线不受影响，3D 渲染作论文图须数据真实可复现。
**触达技能**：README×2 + figure-planning(SKILL+ref) + figure-drawing(SKILL+ref) + frontend-design + slides + CHANGELOG + CONTRIBUTING；tool-selection 核对后无需改（方法论层不复写费用表）。
