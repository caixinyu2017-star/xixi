# xixi — 科研 Skills 集合 / Research Skills Marketplace

本仓库把 **5 套科研类 Claude Code Skill 包** 打包成一个本地 **plugin marketplace（插件市场）**，
安装后即可在 Claude Code 中按需启用。每套包都保留了作者原始的目录结构与相对路径引用，
因此知识库、脚本、模板、`_shared`/`shared`/`databases` 等内部资源都能正确加载。

This repo bundles **five academic-research skill packages** into a single local **Claude Code plugin
marketplace**. Each package keeps its original directory layout and relative-path references intact, so
its knowledge bases, scripts, templates and shared folders all resolve correctly once installed.

---

## 📦 包含的 5 个插件 / The 5 plugins

| 插件 / Plugin | 技能数 / Skills | 说明 / What it does |
| --- | --- | --- |
| **light** | 28 | 全流程科研技能包：文献检索、数据工程、创意生成/批判、系统与图表设计、实验分析、论文写作/润色、引用、排版、审稿返修、专利软著、PPT 与竞赛材料。内置 9 个可溯源知识库与可运行脚本。 |
| **academic-research-skills** | 4 (+35 modes) | 生产级学术研究流水线：research → write → review → revise → finalize，含 deep-research、引用核验闸门与多智能体集成。 |
| **nature-skills** | 12 | Nature 风格科研技能：学术检索、引用、数据、图表、论文转专利、论文转 PPT、润色、阅读/翻译、审稿回复、同行评审、科研写作，外加 OpenClaw 医学模块。 |
| **econ-top-journal-writing** | 5 | 经济学顶刊写作流程：总入口路由、英文经济学写作、中文顶刊写作、中英文表图设计、多智能体写作控制器。 |
| **writing-ai-paper** | 1 | 《Writing AI Conference Papers》新手手册（hzwer & DingXiaoH 著）封装成可调用 skill，用于 AI/ML 顶会论文的选题、框架、引言、可读性与审稿应对。 |

合计 **50 个 skill**。

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

## 🔌 可选：MCP 服务器 / Optional: MCP servers

除技能外，本仓库还附带即插即用的 MCP 服务器配置，供上述科研技能调用外部工具。

Beyond skills, the repo ships ready-to-use MCP server configs that the research skills above can call.

| 服务器 / Server | 用途 / What it does | 安装 / Install |
| --- | --- | --- |
| **markitdown** | 把 PDF / Word / PPT / Excel / 图片 / HTML 等转换为 Markdown，便于文献阅读、数据抽取与写作。/ Convert PDF, Word, PPT, Excel, images, HTML and more to Markdown for reading, extraction and writing. | `bash mcp/markitdown/install.sh` — 详见 [`mcp/markitdown/`](./mcp/markitdown/) |

安装后**重启 Claude Code**，即可让 Claude 直接读取并转换文档（例如 `convert file:///path/to/paper.pdf`）。

Restart Claude Code after installing, and Claude can read/convert documents directly
(e.g. `convert file:///path/to/paper.pdf`).

---

## 🗂 目录结构 / Layout

```text
xixi/
├── .claude-plugin/
│   └── marketplace.json          # 列出全部 5 个插件 / lists all 5 plugins
├── claude-science-windows/       # Windows 一键安装 Claude Science / one-click installer
├── plugins/
│   ├── light/                    # 28 skills (+ databases/, code_assets/)
│   ├── academic-research-skills/ # 4 skills (+ shared/, agents/, hooks/, modes)
│   ├── nature-skills/            # 12 skills (+ skills/_shared/)
│   ├── econ-top-journal-writing/ # 5 skills
│   └── writing-ai-paper/         # 1 skill (handbook wrapped as a skill)
├── mcp/
│   └── markitdown/               # MarkItDown MCP server (文档→Markdown / doc→Markdown)
└── README.md
```

每个插件目录都含有 `.claude-plugin/plugin.json` 与 `skills/`。其中 `light` 与
`academic-research-skills` 由作者自带插件清单；`nature-skills`、`econ-top-journal-writing`
的清单在本次部署中按其结构补全；`writing-ai-paper` 由原手册文档封装为可调用 skill。

---

## 📝 来源与许可 / Sources & licenses

各插件保留了原始 `LICENSE`/`NOTICE`：

- **light** — MIT（Light，https://github.com/Light0305/Light-skills）
- **academic-research-skills** — CC-BY-NC-4.0（Cheng-I Wu，https://github.com/Imbad0202/academic-research-skills）
- **nature-skills** — Apache-2.0（袁一哲 / nature-skills community）
- **econ-top-journal-writing** — 分层许可，见插件内 `LICENSE`
- **writing-ai-paper** — 见 https://github.com/hzwer/WritingAIPaper（hzwer、DingXiaoH）

请在使用时遵循各自许可（尤其 academic-research-skills 为非商业 CC-BY-NC-4.0）。
