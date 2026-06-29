# 更新日志 / Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 与 [语义化版本](https://semver.org/lang/zh-CN/)。
All notable changes are documented here.

## [Unreleased]

### Removed
- **移除 PPT 生图流水线**(`light-slides` 原 `imggen-enhanced` 模式):删除 `imagegen.py`、`assemble_from_spec.py`、`deck_spec.yaml` 及五阶段流水线文档;`light-slides` 回归 **python-pptx 程序化单一路线**(无 mode 切换)。配套清理:推荐配置改为 MCP(Canva/Figma/MATLAB/BioRender)+ 环境(Git/Python/R/LaTeX),删生图 API key 段;db06 移除 imggen 实跑沉淀卡。脚本 51 → 49,模板 40 → 39,知识卡 318 → 317,显式 mode 10 → 8。论文图禁用 AI 生成的诚实底线(m11 figure_integrity)保留不变。

### Changed
- **推荐配置重构**:Harness(Claude Code/Codex)+ 模型(Opus 4.8/GPT 5.5,备 DeepSeek V4 Pro)+ 环境(Git/Python/R,排版补 LaTeX)+ 推荐 MCP(Canva/Figma 免费、MATLAB/BioRender 标注付费门槛)。
- **推荐 MCP 表重订(实测校正 + 扩 3D/绘图)**:据 2026-06 联网实测调整为 **Figma · Canva · Draw.io · Blender · MATLAB** 五项,各标官方/社区 MCP、能力、费用、热门项目 star(实测值)。变更点——①**移除 BioRender**:其官方 connector/MCP 仅查询不能作图,不作为出图路径(需图标库时仍可手工用,降为说明);②**MATLAB 费用校正**:MathWorks 2025-11 开源 MATLAB MCP Core Server,跑本地 MATLAB 即可、**不需 Production Server 商业许可**(原表述已过时),但本地 MATLAB 本身付费、学生/家庭版能否用于 MCP 须自查许可;③**Figma 校正**:Remote server 免费账号可用、能读能写(原仅写 Dev Mode 付费);④**新增 Draw.io**(开源,官方 jgraph/drawio-mcp,diagram-as-code,配 m09)、**Blender**(开源,社区 ahujasid/官方 Lab MCP,3D 科学可视化/路演渲染,配 m09/m16)。论文数据图禁 AI 生成底线不变;Draw.io/Blender 均非 AI 生图,3D 渲染作论文图须数据真实可复现。

## [3.0.0] - 2026-06-12

第三期:P0 清零、中文链路闭环、会话衔接协议、PPT 生图流水线、数据库上量、行为评测与保鲜自动化、安全合规增量。Third-phase release.

### Added
- **会话衔接协议**(全局新机制):上下文将尽时主动产出自包含衔接卡(`.light/handoff/`)+ 中文新对话启动提示词,新对话读最新卡即可无缝续跑,可沿衔接链回溯任意上级对话。落地于 CONVENTIONS §9 + `light-memory-pm` 两件套模板 + `light-orchestrator` 收编 + 路由触发 + README FAQ。
- **PPT 生图流水线**(`light-slides` 的 `imggen-enhanced` 模式):`deck_spec.yaml` 契约 → 三后端统一生图(OpenAI gpt-image / Gemini Nano Banana / 火山方舟 Seedream,无 key 不静默假成功)→ 真数据图叠加 → 重组为可编辑 pptx;新增脚本 `imagegen.py`、`assemble_from_spec.py`,模板 `deck_spec.yaml`,离线 selftest 绿。生图严禁进论文图链路(期刊禁令)。
- **行为评测体系** `evals/`:44 个黄金任务(Tier1 24 + Tier2 20)+ Tier1 基线分(48/48,诱导编造红线 8/8 守住)+ 弱模型(Haiku 4.5)降级记录;与 CI 结构校验分工(CI 验结构、evals 验行为)。
- **保鲜自动化** `.github/workflows/freshness.yml`:每月 1 日定时 + 手动 `workflow_dispatch`,数据卡超期自动开"保鲜清单"issue(warn-only,永不阻断 CI)。
- **新脚本**:`plan_lint.py`(实验矩阵四要素检查)、`venue_signal.py`(投稿信号)、`er_diagram.py`(表结构转 Mermaid)、`rebuttal_budget.py`(rebuttal 字数/页数预算)、`search_normalize.py` 增 `--from-date`/`--known-dois`(定期追踪增量)。脚本数 45 → 51。
- **数据库上量**:db05/db06/db07 真实卡补到 18/16/31(均 ≥15);db01 期刊会议扩至 308 卡(ai_policy 字段 186 卡有值,六大出版社官方页实查);db02 写作样本 +8 篇(2024-2026 顶会顶刊);合计 318 张可溯源知识卡。
- **跨库共享色板** `palette.json` 机制(R9.7):项目级视觉 SSOT,figure-drawing/slides/frontend/consistency 四技能接线,dairygoat 真实实例落地。
- **安全合规**:外部内容防注入纪律四处落地(CONVENTIONS §4 真相源 + a01/m01/a10 指针,标记统一 `INJECTION-ATTEMPT-DETECTED`);`light-research-ethics` 涉动物伦理块(GB/T 35892-2018 实查);`light-research-plan` 预注册一节;a02/db09 项目归档协议。
- **CI 门禁扩建**:校验器 7 → 8 个脚本 + 多个新 gate 点(路由 28/28 必覆盖、README 结构同步、模板防漂移、db09 schema、体量红线、离线性、产物残留、安装可达性);新增 windows-latest 安装看护 job(`check_install_windows.ps1`,防 junction 穿透删源)。
- **门面**:推荐配置节、竞品对照矩阵(实查留痕)、技能链路图 `assets/pipeline.svg`、社交预览图 `assets/social-preview.png`、会话衔接卖点、Star History、知识卡贡献 issue 模板。
- 仓库专业化(承前期):`.github/`(issue/PR 模板、CI、FUNDING)、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`SECURITY.md`、`CITATION.cff`、本 `CHANGELOG.md`。

### Changed
- **OpenAlex 限流口径统一**:`light-literature-search` 设单一真相源,其余技能改放指针(消除"同一事实两套说法");OpenAlex 文档域名同步迁 `developers.openalex.org`。
- **契约统一**:`light-orchestrator` 跨阶段契约双向化(声明方与消费方互指),实验矩阵模板文件名统一为下划线 `experiment_matrix.md`。
- **常驻技能瘦身 -15%**:11 个常驻技能 SKILL.md 总行数 901 → 763 行(细节下沉 references/examples,未删任何能力)。
- **依赖管理默认 uv**(scaffold pyproject 始终落地,`--poetry` 切备选);`vaex` 全仓库标已淘汰(迁 DuckDB/polars streaming,a09 单一口径);种子数统一"≥5,算力受限 ≥3 须显式标注"。
- 重写中英双语 README,按"17 手动 / 11 常驻"同步技能总览;`light-orchestrator` 纳入常驻计数,技能数 28。

### Fixed
- 11 个 P0 问题清零(均经 file:line 二次交叉验证):
  1. OpenAlex 限流口径分裂 → 单一真相源 + 指针。
  2. MDPI/中文刊栏宽死锁 → 指认 `light-figure-planning` 出版商图宽表为来源,付费墙未实测值标 `verified=False`。
  3. Science 栏宽 120/121 不一致 → 统一 120mm(订正 `science.mplstyle` 写死的 figsize)。
  4. orchestrator 契约单向挂载 → 双向化。
  5. 安装后断链 → 4 文档随装链接 + `check_installation_assets.py` 校验,装后相对引用可达。
  6. Hermes 安装目标歧义 → 确认对外只支持 Claude Code 与 Codex 两端。
  7. MCM 赛时 AI 规定口径 → 按官方 2025 试行版(自 2025-09-01)统一写入 `light-competition`。
  8. CI 模板版本陈旧 → `light-system-design`/`light-tool-selection` 升 v6 并指向 `light-backend-coding` 真相源。
  9. `light-idea-critique` 示例诚实标注不统一 → 统一标注。
  10. `light-competition` selftest 产物污染当前目录 → 改临时目录。
  11. README 卸载指引数据风险 → 补 Windows `rmdir` 防 junction 穿透删源警示。

## [1.0.0] - 2026-06

### Added
- 28 个技能,覆盖科研全流程:文献调研 → 数据 → 创新 → 方案 → 实验 → 分析 → 写作润色 → 图表 → 排版 → 投稿 → 返修 → 软著专利 → PPT → 竞赛。
  - **17 个手动技能**(`/` 可调用):literature-search、data-engineering、idea-generation、idea-critique、research-plan、result-analysis、paper-drafting、paper-polishing、figure-planning、figure-drawing、citation、typesetting、venue-matching、review-rebuttal、ip-application、slides、competition。
  - **11 个常驻技能**(后台自动):file-reading、memory-pm、orchestrator、backend-coding、system-design、frontend-design、project-structure、consistency、self-review、tool-selection、research-ethics。
- 9 个共享知识库(`databases/db01–db09`):期刊会议、模板、方法、数据集、设计系统、幻灯主题、科研图表、知识产权与竞赛、项目状态。
- `code_assets/`:经对抗验证的统计与指标代码(κ/QWK、Welch t/BH-FDR/Wilson、MOTA/IDF1、CORAL 序数损失、长尾重采样),与 `scipy`/`sklearn` 逐位对齐。
- 双端安装脚本 `install.ps1` / `install.sh`(Claude Code 与 Codex)。
- 全局规约 `CONVENTIONS.md` 与技能路由 `ROUTER.md`。

[Unreleased]: https://github.com/Light0305/Light-skills/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/Light0305/Light-skills/releases/tag/v3.0.0
[1.0.0]: https://github.com/Light0305/Light-skills/releases/tag/v1.0.0
