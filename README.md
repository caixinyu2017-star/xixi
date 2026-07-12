# xixi — 科研 Skills 集合 / Research Skills Marketplace

本仓库把 **8 套科研与绘图类 Claude Code Skill 包** 打包成一个本地 **plugin marketplace（插件市场）**，
安装后即可在 Claude Code 中按需启用。每套包都保留了作者原始的目录结构与相对路径引用，
因此知识库、脚本、模板、`_shared`/`shared`/`databases` 等内部资源都能正确加载。

This repo bundles **eight academic-research and scientific-figure skill packages** into a single local
**Claude Code plugin marketplace**. Each package keeps its original directory layout and relative-path
references intact, so its knowledge bases, scripts, templates and shared folders all resolve correctly
once installed.

---

## 📦 包含的 8 个插件 / The 8 plugins

| 插件 / Plugin | 技能数 / Skills | 说明 / What it does |
| --- | --- | --- |
| **light** | 28 | 全流程科研技能包：文献检索、数据工程、创意生成/批判、系统与图表设计、实验分析、论文写作/润色、引用、排版、审稿返修、专利软著、PPT 与竞赛材料。内置 9 个可溯源知识库与可运行脚本。 |
| **academic-research-skills** | 4 (+35 modes) | 生产级学术研究流水线：research → write → review → revise → finalize，含 deep-research、引用核验闸门与多智能体集成。 |
| **nature-skills** | 12 | Nature 风格科研技能：学术检索、引用、数据、图表、论文转专利、论文转 PPT、润色、阅读/翻译、审稿回复、同行评审、科研写作，外加 OpenClaw 医学模块。 |
| **econ-top-journal-writing** | 5 | 经济学顶刊写作流程：总入口路由、英文经济学写作、中文顶刊写作、中英文表图设计、多智能体写作控制器。 |
| **writing-ai-paper** | 1 | 《Writing AI Conference Papers》新手手册（hzwer & DingXiaoH 著）封装成可调用 skill，用于 AI/ML 顶会论文的选题、框架、引言、可读性与审稿应对。 |
| **auto-visio-helper** | 1 | Auto Visio Helper：把方法描述、论文截图或手绘草图转成可编辑的 Microsoft Visio `.vsdx` 图。先产出可审阅的 JSON 绘图 spec，再经本地 Visio COM 自动化渲染，保持形状/连线/文本/图层可编辑；附参考文档、demo、可复用 Visio 模板与 PNG/PDF/SVG 预览导出。 |
| **visio-image-rebuilder** | 1 | Visio 图重建 Skill：从参考图片或已有 `.vsdx` 重建/改版可编辑的 Visio 图，并可导出 `.vsdx`/PNG/SVG/PDF/PPTX；用原生形状/文本/连线复刻多面板科学图而非整图嵌入，含面板坐标校准与中文技术标流程图默认模式（宋体 12pt、固定样式/页面框、只输出主 `.vsdx` 的批量出图）；附重建指南、Visio PowerShell/COM 自动化脚手架与 CJK Unicode 转义指引。 |
| **frontend-slides** | 1 | Frontend Slides：零依赖、动画丰富的 HTML 演示文稿生成器，可从零搭建或将 PPT/PPTX 转成网页，含安全预设、bold 模板库、固定 16:9 舞台与反 “AI slop” 设计理念。 |

合计 **53 个 skill**。

---

## 🚀 安装与部署 / Install & deploy

> 前置：已安装 [Claude Code](https://claude.ai/code)。

### 方式 A — 作为插件市场安装（推荐）/ As a plugin marketplace (recommended)

在 Claude Code 中运行：

```text
# 1) 添加本仓库为插件市场（本地路径，或克隆后的目录）
/plugin marketplace add /home/user/xixi
#   或从 GitHub： /plugin marketplace add caixinyu2017-star/xixi

# 2) 安装需要的插件（市场名为 xixi-research-skills）
/plugin install light@xixi-research-skills
/plugin install academic-research-skills@xixi-research-skills
/plugin install nature-skills@xixi-research-skills
/plugin install econ-top-journal-writing@xixi-research-skills
/plugin install writing-ai-paper@xixi-research-skills
/plugin install auto-visio-helper@xixi-research-skills
/plugin install visio-image-rebuilder@xixi-research-skills
/plugin install frontend-slides@xixi-research-skills
```

也可以直接运行 `/plugin` 打开交互式菜单，浏览并勾选要安装的插件。
安装后**重启 Claude Code**，技能即可被自动触发（也可用 `/<skill-name>` 显式调用）。

You can also just run `/plugin` to open the interactive menu, then browse and toggle the plugins you
want. Restart Claude Code after installing; skills then auto-trigger (or invoke explicitly with
`/<skill-name>`).

### 方式 B — 各包自带的安装方式 / Each package's own installer

部分包附带独立安装脚本（例如 `plugins/light/install.sh` 会把 28 个 skill 软链到
`~/.claude/skills/`）。这些脚本仍然可用，但与方式 A 二选一即可，避免重复安装。

Some packages ship their own installer (e.g. `plugins/light/install.sh` symlinks its 28 skills into
`~/.claude/skills/`). Those still work, but use either method A or B — not both — to avoid duplicates.

---

## 🗂 目录结构 / Layout

```text
xixi/
├── .claude-plugin/
│   └── marketplace.json          # 列出全部 8 个插件 / lists all 8 plugins
├── plugins/
│   ├── light/                    # 28 skills (+ databases/, code_assets/)
│   ├── academic-research-skills/ # 4 skills (+ shared/, agents/, hooks/, modes)
│   ├── nature-skills/            # 12 skills (+ skills/_shared/)
│   ├── econ-top-journal-writing/ # 5 skills
│   ├── writing-ai-paper/         # 1 skill (handbook wrapped as a skill)
│   ├── auto-visio-helper/        # 1 skill (+ references/, demo/, assets/, scripts/)
│   ├── visio-image-rebuilder/    # 1 skill (+ references/, scripts/ incl. multi-format export)
│   └── frontend-slides/          # 1 skill (+ bold-template-pack/, scripts/)
└── README.md
```

每个插件目录都含有 `.claude-plugin/plugin.json` 与 `skills/`。其中 `light` 与
`academic-research-skills` 由作者自带插件清单；`nature-skills`、`econ-top-journal-writing`
的清单在本次部署中按其结构补全；`writing-ai-paper` 由原手册文档封装为可调用 skill。
`frontend-slides` 沿用作者自带的 plugin 结构；`auto-visio-helper` 与 `visio-image-rebuilder`
原为 Codex skill（含 `agents/openai.yaml`），本次将其目录整体封装进 `skills/` 并补全 plugin 清单，
`agents/`、`references/`、`scripts/`、`assets/`、`demo/` 等相对引用保持不变。

---

## 📝 来源与许可 / Sources & licenses

各插件保留了原始 `LICENSE`/`NOTICE`：

- **light** — MIT（Light，https://github.com/Light0305/Light-skills）
- **academic-research-skills** — CC-BY-NC-4.0（Cheng-I Wu，https://github.com/Imbad0202/academic-research-skills）
- **nature-skills** — Apache-2.0（袁一哲 / nature-skills community）
- **econ-top-journal-writing** — 分层许可，见插件内 `LICENSE`
- **writing-ai-paper** — 见 https://github.com/hzwer/WritingAIPaper（hzwer、DingXiaoH）
- **auto-visio-helper** — MIT（Auto-Visio-Helper，https://github.com/0Antique/Auto-Visio-Helper）
- **visio-image-rebuilder** — 见插件 `skills/visio-image-rebuilder/README.md`（Visio 图重建 / Codex 科研论文绘图 Skill）
- **frontend-slides** — MIT（zarazhangrui / Zara Zhang，https://github.com/zarazhangrui/frontend-slides），见插件内 `LICENSE`

请在使用时遵循各自许可（尤其 academic-research-skills 为非商业 CC-BY-NC-4.0）。

> ℹ️ `auto-visio-helper` 与 `visio-image-rebuilder` 依赖 Windows 上的 Microsoft Visio（COM/PowerShell
> 自动化）来渲染/导出 `.vsdx`；spec 规划、参考分析等步骤在任意平台可用。
