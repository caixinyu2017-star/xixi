# xixi — 科研 Skills 集合 / Research Skills Marketplace

本仓库把 **6 套 Claude Code Skill 包**（5 套科研 + 1 套专业作图）打包成一个本地
**plugin marketplace（插件市场）**，安装后即可在 Claude Code 中按需启用。
每套包都保留了作者原始的目录结构与相对路径引用，
因此知识库、脚本、模板、`_shared`/`shared`/`databases` 等内部资源都能正确加载。

This repo bundles **six skill packages** (five academic-research packs plus one professional
diagramming pack) into a single local **Claude Code plugin marketplace**. Each package keeps its
original directory layout and relative-path references intact, so its knowledge bases, scripts,
templates and shared folders all resolve correctly once installed.

---

## 📦 包含的 6 个插件 / The 6 plugins

| 插件 / Plugin | 技能数 / Skills | 说明 / What it does |
| --- | --- | --- |
| **light** | 28 | 全流程科研技能包：文献检索、数据工程、创意生成/批判、系统与图表设计、实验分析、论文写作/润色、引用、排版、审稿返修、专利软著、PPT 与竞赛材料。内置 9 个可溯源知识库与可运行脚本。 |
| **academic-research-skills** | 4 (+35 modes) | 生产级学术研究流水线：research → write → review → revise → finalize，含 deep-research、引用核验闸门与多智能体集成。 |
| **nature-skills** | 12 | Nature 风格科研技能：学术检索、引用、数据、图表、论文转专利、论文转 PPT、润色、阅读/翻译、审稿回复、同行评审、科研写作，外加 OpenClaw 医学模块。 |
| **econ-top-journal-writing** | 5 | 经济学顶刊写作流程：总入口路由、英文经济学写作、中文顶刊写作、中英文表图设计、多智能体写作控制器。 |
| **writing-ai-paper** | 1 | 《Writing AI Conference Papers》新手手册（hzwer & DingXiaoH 著）封装成可调用 skill，用于 AI/ML 顶会论文的选题、框架、引言、可读性与审稿应对。 |
| **diagram-skills** | 4 | 专业作图：`baoyu-diagram` 输出精美、可编辑、自包含的 SVG——技术路线图/时间线、路径图/流程图、框架图/架构图、时序图、结构图、思维导图、状态机、数据流图；`academic-diagram-style` 叠加**科研/期刊风格**（白底、色盲友好 Okabe-Ito 配色、期刊排版），论文场景默认生效；`image2-diagram` 调用 OpenAI GPT Image 2 生成位图（需 `OPENAI_API_KEY`）；`frontend-design` 为 Anthropic 官方审美校准 skill。 |

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
/plugin install diagram-skills@xixi-research-skills
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
│   └── marketplace.json          # 列出全部 6 个插件 / lists all 6 plugins
├── plugins/
│   ├── light/                    # 28 skills (+ databases/, code_assets/)
│   ├── academic-research-skills/ # 4 skills (+ shared/, agents/, hooks/, modes)
│   ├── nature-skills/            # 12 skills (+ skills/_shared/)
│   ├── econ-top-journal-writing/ # 5 skills
│   ├── writing-ai-paper/         # 1 skill (handbook wrapped as a skill)
│   └── diagram-skills/           # 4 skills (baoyu-diagram, academic-diagram-style,
│                                 #           image2-diagram, frontend-design)
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
- **diagram-skills** — `baoyu-diagram`：MIT（Jim Liu，https://github.com/JimLiu/baoyu-skills ）；
  `frontend-design`：Apache-2.0（Anthropic，https://github.com/anthropics/skills ）。详见插件内 `NOTICE.md`。

请在使用时遵循各自许可（尤其 academic-research-skills 为非商业 CC-BY-NC-4.0）。

---

## 🎨 作图说明 / About diagramming (and "image 2")

装好 `diagram-skills` 并重启 Claude Code 后，说"**画个技术路线图 / 画一个架构图 / 画流程图**"
就会自动触发 `baoyu-diagram`，输出单个自包含、可直接编辑的 `.svg` 文件。SVG 可在浏览器打开，
也可导入 draw.io / Inkscape / Figma 继续编辑，或用插件自带的 `scripts/main.ts`
（需 `bun` + npm 包 `sharp`）转成 PNG。

**科研风格 / Academic style**：论文、报告、基金申报等学术场景（或说"科研风格/期刊风格"）会自动
叠加 `academic-diagram-style`——白底、细线、色盲友好的 Okabe-Ito 配色、期刊排版、系统字体
（不依赖网络字体），SVG 可经 `rsvg-convert -f pdf` / Inkscape 转为 LaTeX 用的 PDF，
或直接插入 Word/PPT。`baoyu-diagram` 默认的深色科技风只在明确要求时使用。

After installing `diagram-skills` and restarting Claude Code, asking for a roadmap / architecture
diagram / flowchart auto-triggers `baoyu-diagram` (self-contained, editable `.svg`). In academic
contexts `academic-diagram-style` overlays a publication-grade look: white background, thin strokes,
colorblind-safe Okabe-Ito palette, journal typography, system fonts only.

### 用 GPT Image 2 作图 / Drawing with GPT Image 2

`image2-diagram` skill 封装了 OpenAI Images API（`gpt-image-2`，即"image 2"）。
说"**用 image 2 画……**"或需要**封面图/宣传图/海报**等一次性位图时触发。启用前需两步配置：

1. **配置 API key（绝不要写进仓库）/ Set the key (never commit it):**
   - Claude Code 网页版/远程：在环境设置的 **Environment variables** 里添加
     `OPENAI_API_KEY`（见 https://code.claude.com/docs/en/claude-code-on-the-web ）。
   - 本地：`export OPENAI_API_KEY=...` 写入 shell 配置，或在 `~/.claude/settings.json`
     的 `"env"` 里添加。
2. **放行域名（仅远程环境需要）/ Allow the domain (remote envs only):**
   在环境设置的网络策略（network access）中允许 `api.openai.com`，否则请求会被代理以 403 拒绝。

也可以手动调用脚本 / Manual invocation:

```bash
python3 plugins/diagram-skills/skills/image2-diagram/scripts/generate.py \
  --prompt "..." --out figure.png --size 1536x1024 --quality high
```

**选型建议 / Which to use:** 对带大量文字标注、需要反复修改的技术路线图/框架图，图像生成模型
输出的是不可编辑的位图——改一个标签要整图重生成且布局会漂移，小字号标注仍不可靠，连线关系可能
被"脑补"错；SVG 文字 100% 准确、逐元素可编辑、可进版本库。所以日常技术图用
`baoyu-diagram`（+ 科研风格），GPT Image 2 留给内容定稿后的一次性宣传图/封面图/概念示意图。

Image-gen models output flat rasters: labels aren't element-editable, small text is still
unreliable, and regenerating shifts the layout. Use structured SVG for label-heavy, frequently
edited technical diagrams; use GPT Image 2 for one-off, content-frozen visuals.

其他可选的图像生成 MCP 方案 / Alternative image-gen MCP servers:

- https://github.com/shinpr/mcp-image — Gemini 图像模型，可选接入 GPT Image（需 `GEMINI_API_KEY`）
- https://github.com/ArcadeAI/blueprint-mcp — 基于 Nano Banana Pro 的架构图生成（需 Gemini API key）
