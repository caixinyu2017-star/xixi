# xixi — 科研 Skills 集合 / Research Skills Marketplace

本仓库把 **9 套科研/演示类 Claude Code Skill 包** 打包成一个本地 **plugin marketplace（插件市场）**，
安装后即可在 Claude Code 中按需启用。每套包都保留了作者原始的目录结构与相对路径引用，
因此知识库、脚本、模板、`_shared`/`shared`/`databases` 等内部资源都能正确加载。

This repo bundles **nine academic-research and presentation/diagramming skill packages** into a single
local **Claude Code plugin marketplace**. Each package keeps its original directory layout and
relative-path references intact, so its knowledge bases, scripts, templates and shared folders all
resolve correctly once installed.

---

## 📦 包含的 9 个插件 / The 9 plugins

| 插件 / Plugin | 技能数 / Skills | 说明 / What it does |
| --- | --- | --- |
| **light** | 28 | 全流程科研技能包：文献检索、数据工程、创意生成/批判、系统与图表设计、实验分析、论文写作/润色、引用、排版、审稿返修、专利软著、PPT 与竞赛材料。内置 9 个可溯源知识库与可运行脚本。 |
| **academic-research-skills** | 4 (+35 modes) | 生产级学术研究流水线：research → write → review → revise → finalize，含 deep-research、引用核验闸门与多智能体集成。 |
| **nature-skills** | 12 | Nature 风格科研技能：学术检索、引用、数据、图表、论文转专利、论文转 PPT、润色、阅读/翻译、审稿回复、同行评审、科研写作，外加 OpenClaw 医学模块。 |
| **econ-top-journal-writing** | 5 | 经济学顶刊写作流程：总入口路由、英文经济学写作、中文顶刊写作、中英文表图设计、多智能体写作控制器。 |
| **writing-ai-paper** | 1 | 《Writing AI Conference Papers》新手手册（hzwer & DingXiaoH 著）封装成可调用 skill，用于 AI/ML 顶会论文的选题、框架、引言、可读性与审稿应对。 |
| **auto-visio-helper** | 1 | 把方法描述、论文截图或手绘草图先转成可核对的 JSON 绘图 spec，再通过本地 Visio COM 自动化渲染成可编辑 `.vsdx` 科研配图。**需 Windows + 已激活的本地 Microsoft Visio。** |
| **visio-image-rebuilder** | 1 | 面向论文配图，用参考图片/已有 `.vsdx` 重建或改版可编辑 Visio 图形（原生形状而非整图内嵌），支持多面板结构复刻与配色/字体统一。**需 Windows + 已激活的本地 Microsoft Visio。** |
| **frontend-slides** | 1 | 生成零依赖、动效丰富的单文件 HTML 演示文稿，支持从零创作或将 PPT/PPTX 转成网页版；内置 bold 模板包与"反 AI 陈词滥调"设计理念。 |
| **ppt-master** | 1 | 把 PDF/DOCX/URL/Markdown 转成原生可编辑 PPTX（真实 DrawingML 形状/文本框/图表/动画），AI 多角色 SVG 生成流水线；内置大型图标/模板/参考图库。**首次使用前需在 `skills/ppt-master/` 下 `pip install -r requirements.txt`。** |

合计 **54 个 skill**。

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
/plugin install ppt-master@xixi-research-skills
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
│   └── marketplace.json          # 列出全部 9 个插件 / lists all 9 plugins
├── plugins/
│   ├── light/                    # 28 skills (+ databases/, code_assets/)
│   ├── academic-research-skills/ # 4 skills (+ shared/, agents/, hooks/, modes)
│   ├── nature-skills/            # 12 skills (+ skills/_shared/)
│   ├── econ-top-journal-writing/ # 5 skills
│   ├── writing-ai-paper/         # 1 skill (handbook wrapped as a skill)
│   ├── auto-visio-helper/        # 1 skill (spec-first Visio diagram generation, Windows-only)
│   ├── visio-image-rebuilder/    # 1 skill (rebuild paper figures as native Visio shapes, Windows-only)
│   ├── frontend-slides/          # 1 skill (zero-dependency HTML decks + PPT→web)
│   └── ppt-master/               # 1 skill (doc→native PPTX pipeline, large icon/template library)
└── README.md
```

每个插件目录都含有 `.claude-plugin/plugin.json` 与 `skills/`。其中 `light` 与
`academic-research-skills` 由作者自带插件清单；`nature-skills`、`econ-top-journal-writing`
的清单在本次部署中按其结构补全；`writing-ai-paper`、`auto-visio-helper`、
`visio-image-rebuilder` 由原手册/skill 文档封装为可调用 skill；
`frontend-slides`、`ppt-master` 的插件清单由原仓库自带，直接照原样收录。

---

## 📝 来源与许可 / Sources & licenses

各插件保留了原始 `LICENSE`/`NOTICE`：

- **light** — MIT（Light，https://github.com/Light0305/Light-skills）
- **academic-research-skills** — CC-BY-NC-4.0（Cheng-I Wu，https://github.com/Imbad0202/academic-research-skills）
- **nature-skills** — Apache-2.0（袁一哲 / nature-skills community）
- **econ-top-journal-writing** — 分层许可，见插件内 `LICENSE`
- **writing-ai-paper** — 见 https://github.com/hzwer/WritingAIPaper（hzwer、DingXiaoH）
- **auto-visio-helper** — MIT（0Antique，https://github.com/0Antique/Auto-Visio-Helper）
- **visio-image-rebuilder** — 许可未在源仓库注明，见 https://github.com/pengjunchi0/codex-visio-paper-figure-skill
- **frontend-slides** — MIT（Zara Zhang，https://github.com/zarazhangrui/frontend-slides）
- **ppt-master** — MIT（Hugo He，https://github.com/hugohe3/ppt-master）

请在使用时遵循各自许可（尤其 academic-research-skills 为非商业 CC-BY-NC-4.0）。
