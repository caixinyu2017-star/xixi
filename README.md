# xixi — 科研 Skills 集合 / Research Skills Marketplace

本仓库把 **12 套 Claude Code Skill 包**（6 套科研类 + 3 套科研绘图/演示 + 3 套 PPT 制作）打包成一个本地
**plugin marketplace（插件市场）**，安装后即可在 Claude Code 中按需启用。每套包都保留了
作者原始的目录结构与相对路径引用，因此知识库、脚本、模板、`_shared`/`shared`/`databases`/`catalog`
等内部资源都能正确加载。

This repo bundles **twelve skill packages** (six academic-research packs, three scientific-figure /
web-slides packs, and three PPT-production packs) into a single local **Claude Code plugin marketplace**.
Each package keeps its original directory layout and relative-path references intact, so its knowledge
bases, scripts, templates and shared folders all resolve correctly once installed.

---

## 📦 包含的技能包 / The skill packages

| 技能包 / Package | 市场内可安装插件 / Installable plugins | 说明 / What it does |
| --- | --- | --- |
| **light** | `light` (28 skills) | 全流程科研技能包：文献检索、数据工程、创意生成/批判、系统与图表设计、实验分析、论文写作/润色、引用、排版、审稿返修、专利软著、PPT 与竞赛材料。内置 9 个可溯源知识库与可运行脚本。 |
| **academic-research-skills** | `academic-research-skills` (4 skills, +35 modes) | 生产级学术研究流水线：research → write → review → revise → finalize，含 deep-research、引用核验闸门与多智能体集成。 |
| **nature-skills** | `nature-skills` (12 skills) | Nature 风格科研技能：学术检索、引用、数据、图表、论文转专利、论文转 PPT、润色、阅读/翻译、审稿回复、同行评审、科研写作，外加 OpenClaw 医学模块。 |
| **econ-top-journal-writing** | `econ-top-journal-writing` (5 skills) | 经济学顶刊写作流程：总入口路由、英文经济学写作、中文顶刊写作、中英文表图设计、多智能体写作控制器。 |
| **writing-ai-paper** | `writing-ai-paper` (1 skill) | 《Writing AI Conference Papers》新手手册（hzwer & DingXiaoH 著）封装成可调用 skill，用于 AI/ML 顶会论文的选题、框架、引言、可读性与审稿应对。 |
| **auto-empirical-research-skills (AERS)** | `aer-skills` (9→14 skills), `empirical-analysis-python`, `empirical-analysis-stata`, `empirical-analysis-r` | Stanford REAP × CoPaper.AI 的实证研究技能栈。**4 个开箱即用插件**：顶刊经济学 AER/AEJ 全流程写作（选题、DiD/IV/RDD/SCM/Bartik 因果识别、稳健性、AER 表格、openICPSR 存档、R&R 回复）+ 显式 **8 步计量流水线**（清洗→变量→Table 1→诊断→估计 OLS/IV/DID/RDD/PSM/SCM/DML/Causal Forest→稳健性→机制/异质性/中介→出版级表图）的 Python / Stata / R 三套实现。此外仓库内附带**可浏览的 73 套第三方技能 catalog（约 1,150 个 SKILL.md）** 与一个 router `SKILL.md`。 |
| **cyber-ppt** | `cyber-ppt` (1 skill) | CyberPPT：把 DOCX/PDF/TXT/XLSX、研究报告或原始数据转成高密度、可编辑、咨询风格 PPTX。三阶段流水线（MBB 证据分析 + SCR 论证 → 8 种固定视觉风格样张 + 逐页 ImageGen 蓝图 → 混合还原 PPTX），内置渲染质检门、11k+ SVG 图标库与 PPTX 验证脚本。 |
| **dashiai-ppt** | `dashiai-ppt` (1 skill) | DashiAI PPT：基于预置视觉主题组合页面，把自然语言需求整理成 JSON 计划后调用内置本地生成器（React + pptxgenjs），输出可离线打开、可在浏览器编辑的 HTML 演示，支持导出 PPTX / PDF。 |
| **ppt-master** | `ppt-master` (1 skill) | 把 PDF/DOCX/URL/Markdown 转成原生可编辑 PPTX（真实 DrawingML 形状/文本框/图表/动画），AI 多角色 SVG 生成流水线；内置大型图标/模板/参考图库。**首次使用前需在 `skills/ppt-master/` 下 `pip install -r requirements.txt`。** |
| **auto-visio-helper** | `auto-visio-helper` (1 skill) | Auto Visio Helper：把方法描述、论文截图或手绘草图转成可编辑的 Microsoft Visio `.vsdx` 图。先产出可审阅的 JSON 绘图 spec，再经本地 Visio COM 自动化渲染，保持形状/连线/文本/图层可编辑；附参考文档、demo、可复用 Visio 模板与 PNG/PDF/SVG 预览导出。 |
| **visio-image-rebuilder** | `visio-image-rebuilder` (1 skill) | Visio 图重建 Skill：从参考图片或已有 `.vsdx` 重建/改版可编辑的 Visio 图，并可导出 `.vsdx`/PNG/SVG/PDF/PPTX；用原生形状/文本/连线复刻多面板科学图而非整图嵌入，含面板坐标校准与中文技术标流程图默认模式（宋体 12pt、固定样式/页面框、只输出主 `.vsdx` 的批量出图）；附重建指南、Visio PowerShell/COM 自动化脚手架与 CJK Unicode 转义指引。 |
| **frontend-slides** | `frontend-slides` (1 skill) | Frontend Slides：零依赖、动画丰富的 HTML 演示文稿生成器，可从零搭建或将 PPT/PPTX 转成网页，含安全预设、bold 模板库、固定 16:9 舞台与反 “AI slop” 设计理念。 |

**可直接安装的插件共 15 个**（`light` / `academic-research-skills` / `nature-skills` /
`econ-top-journal-writing` / `writing-ai-paper` / `aer-skills` /
`empirical-analysis-python` / `empirical-analysis-stata` / `empirical-analysis-r` /
`cyber-ppt` / `dashiai-ppt` / `ppt-master` / `auto-visio-helper` / `visio-image-rebuilder` / `frontend-slides`）；
AERS 另附约 **1,150 个可浏览/可复制的 catalog skill**（见下）。

**15 directly installable plugins** in total; AERS additionally ships a browsable ~1,150-skill catalog.

---

## 🚀 安装与部署 / Install & deploy

> 前置：已安装 [Claude Code](https://claude.ai/code)（`/plugin` 需要 v2.1+）。

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
/plugin install cyber-ppt@xixi-research-skills
/plugin install dashiai-ppt@xixi-research-skills
/plugin install ppt-master@xixi-research-skills

# —— AERS 的 4 个开箱即用插件 / the 4 first-party AERS plugins ——
/plugin install aer-skills@xixi-research-skills
/plugin install empirical-analysis-python@xixi-research-skills
/plugin install empirical-analysis-stata@xixi-research-skills
/plugin install empirical-analysis-r@xixi-research-skills
```

也可以直接运行 `/plugin` 打开交互式菜单，浏览并勾选要安装的插件。
安装后**重启 Claude Code**，技能即可被自动触发（也可用 `/<skill-name>` 显式调用）。

You can also just run `/plugin` to open the interactive menu, then browse and toggle the plugins you
want. Restart Claude Code after installing; skills then auto-trigger (or invoke explicitly with
`/<skill-name>`).

### 方式 B — 使用 AERS 的 73 套 catalog 技能 / Use any skill in the AERS catalog

AERS 的 catalog（`plugins/auto-empirical-research-skills/skills/00…69`）里每个含 `SKILL.md`
的文件夹都是一个可用技能，未在市场里注册的那些可用「复制到 skills 目录」的方式启用：

```bash
# 项目级（仅当前项目可见）/ project-scoped
mkdir -p .claude/skills
cp -R plugins/auto-empirical-research-skills/skills/00.1-Full-empirical-analysis-skill_Python \
      .claude/skills/empirical-python

# 全局（所有项目可见）/ global
cp -R plugins/auto-empirical-research-skills/skills/00.1-Full-empirical-analysis-skill_Python \
      ~/.claude/skills/empirical-python
```

整仓库还带一个根 router `plugins/auto-empirical-research-skills/SKILL.md`：把 AERS 目录作为
「单个技能」导入时，它会作为轻量目录路由器，按需选择并加载正确的子技能，而不是一次性载入全部
1,150 个 skill。

### 方式 C — 各包自带的安装方式 / Each package's own installer

部分包附带独立安装脚本（例如 `plugins/light/install.sh` 会把 28 个 skill 软链到
`~/.claude/skills/`）。这些脚本仍然可用，但与方式 A 二选一即可，避免重复安装。

---

## 🧪 Windows 一键安装 Claude Science

想在 Windows 上使用 Anthropic 的科研工作台 **Claude Science**（在浏览器中打开）？
参见 [claude-science-windows/](claude-science-windows/)：下载其中的
`ClaudeScience-Install.bat` 双击运行，即可自动完成 WSL2 + Ubuntu 24.04 + Claude Science
的安装，并在桌面生成一键启动器。

Want Anthropic's **Claude Science** research workbench on Windows (opened in your browser)?
See [claude-science-windows/](claude-science-windows/) — download `ClaudeScience-Install.bat`
and double-click it; it installs WSL2 + Ubuntu 24.04 + Claude Science automatically and drops a
launcher on your desktop.

---

## 🗂 目录结构 / Layout

```text
xixi/
├── .claude/
│   └── skills/
│       ├── cyber-ppt   -> ../../plugins/cyber-ppt/skills/cyber-ppt      # 项目级技能，本仓库会话自动加载
│       └── dashiai-ppt -> ../../plugins/dashiai-ppt/skills/dashiai-ppt  # 项目级技能，本仓库会话自动加载
├── .claude-plugin/
│   └── marketplace.json          # 列出全部 15 个可安装插件 / lists all 15 installable plugins
├── claude-science-windows/       # Windows 一键安装 Claude Science / one-click installer
├── plugins/
│   ├── light/                    # 28 skills (+ databases/, code_assets/)
│   ├── academic-research-skills/ # 4 skills (+ shared/, agents/, hooks/, modes)
│   ├── nature-skills/            # 12 skills (+ skills/_shared/)
│   ├── econ-top-journal-writing/ # 5 skills
│   ├── writing-ai-paper/         # 1 skill (handbook wrapped as a skill)
│   ├── auto-visio-helper/        # 1 skill (+ references/, demo/, assets/, scripts/)
│   ├── visio-image-rebuilder/    # 1 skill (+ references/, scripts/ incl. multi-format export)
│   ├── frontend-slides/          # 1 skill (+ bold-template-pack/, scripts/)
│   ├── cyber-ppt/                # 1 skill (+ references/, scripts/, assets/icons 11k+ SVG)
│   ├── dashiai-ppt/              # 1 skill (+ project/ 本地 HTML→PPTX/PDF 生成器)
│   ├── ppt-master/               # 1 skill (doc→native PPTX pipeline, large icon/template library)
│   └── auto-empirical-research-skills/   # AERS — Stanford REAP × CoPaper.AI
│       ├── .claude-plugin/marketplace.json   # AERS 自带市场清单（4 first-party plugins）
│       ├── SKILL.md              # 根 router / catalog-router skill
│       ├── catalog/              # skills.json 等机读索引 / machine-readable indexes
│       ├── docs/                 # 安装、分类法、golden workflows 等文档
│       ├── plugins/              # empirical-analysis-{python,stata,r}（已注册）
│       └── skills/               # 73 套 catalog（00…69），含 50-brycewang-aer-skills（已注册）
└── README.md
```

> 说明：`cyber-ppt` 与 `dashiai-ppt` 同时通过 `.claude/skills/` 符号链接注册为**项目级技能**——在本仓库
> 目录中启动的 Claude Code 会话无需安装插件即可自动发现并按需触发它们（Windows 下如符号链接不可用，
> 请改用方式 A 安装插件）。
>
> Note: `cyber-ppt` and `dashiai-ppt` are also registered as **project-level skills** via symlinks under
> `.claude/skills/`, so Claude Code sessions started inside this repo auto-discover and auto-trigger them
> without installing the plugins (on Windows, if symlinks are unavailable, use method A instead).

每个插件目录都含有 `.claude-plugin/plugin.json` 与 `skills/`。其中 `light` 与
`academic-research-skills` 由作者自带插件清单；`nature-skills`、`econ-top-journal-writing`
的清单在本次部署中按其结构补全；`writing-ai-paper` 由原手册文档封装为可调用 skill。
`frontend-slides` 沿用作者自带的 plugin 结构；`auto-visio-helper` 与 `visio-image-rebuilder`
原为 Codex skill（含 `agents/openai.yaml`），本次将其目录整体封装进 `skills/` 并补全 plugin 清单，
`agents/`、`references/`、`scripts/`、`assets/`、`demo/` 等相对引用保持不变。
AERS 作为完整技能包整体 vendored 进来，保留其 `SKILL.md` 路由器、`catalog/`、`docs/` 与
73 套子技能；市场里注册的是它自己声明的 4 个开箱即用插件。（vendoring 时已剔除与技能运行无关的
`images/`、`demo-notebooks/`、`benchmark/`、`eval-harness/`、`tests/` 等体积负担；
`skills/69-Paper-WorkFlow` 的 submodule 已就地展开为普通文件。）

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
- **cyber-ppt** — MIT（CyberPPT contributors）
- **dashiai-ppt** — AGPL-3.0（大师的AI小灶，https://github.com/chuspeeism/dashiAI-ppt-skill）
- **ppt-master** — MIT（Hugo He，https://github.com/hugohe3/ppt-master）
- **auto-empirical-research-skills (AERS)** — Stanford REAP × CoPaper.AI（Bryce Wang，https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills）；
  `aer-skills` 为 MIT，`empirical-analysis-{python,stata,r}` 为 CC-BY-SA-4.0；catalog 内 73 套第三方技能各自保留其原始许可，请逐个查阅子目录的 `LICENSE`。

请在使用时遵循各自许可（尤其 academic-research-skills 为非商业 CC-BY-NC-4.0；AERS catalog 内含多种许可）。

> ℹ️ `auto-visio-helper` 与 `visio-image-rebuilder` 依赖 Windows 上的 Microsoft Visio（COM/PowerShell
> 自动化）来渲染/导出 `.vsdx`；spec 规划、参考分析等步骤在任意平台可用。
