---
name: gpt-image-2
description: 用环境中已配置的 gpt-image-2 模型生成科研与工程用的概念类图像。凡是用户要「示意图、机制图、机理图、路径图、技术路线图、研究框架图、概念图、流程示意、架构示意、模型结构图、原理图、Graphical Abstract、封面图、配图」时一律使用本技能；也覆盖英文说法 schematic / schematic diagram / mechanism diagram / pathway diagram / technical roadmap / conceptual framework / architecture illustration / graphical abstract，以及「画一张图说明…」「帮我出个示意图」「做个技术路线图」「生成一张配图」这类口语请求。工作流是：先写中文图释 → 转成英文提示词 → 调 scripts/gpt_image2.py 生成 PNG → 看图质检（文字乱码/箭头方向/元素缺失）→ 必要时重生成。注意边界：需要绑定真实数据的统计图表（折线、柱状、散点、热图、森林图、回归系数图、Table 1）不属于本技能，交给 nature-figure 用 Python/R 画；需要事后逐个形状编辑的 Visio 工程图交给 auto-visio-helper / visio-image-rebuilder。
version: 1.0.0
---

<!-- ENCODING-GUARD: 本文件为 UTF-8。Windows PowerShell 5.1 下请用 `Get-Content -Encoding UTF8` 读取；若中文乱码，先按 UTF-8 重读再行动。 -->

# gpt-image-2 概念图生成

## 这个技能负责什么

把「一段说明性的想法」变成一张能放进论文、标书、汇报里的**概念类图像**，用环境里配置好的
`gpt-image-2` 模型生成。它管的是**没有数据坐标轴的图**：结构、关系、流程、机制、时间线。

| 用户说 | 本技能接管 |
|---|---|
| 示意图 / 原理图 / 概念图 / schematic | ✅ |
| 机制图 / 机理图 / mechanism diagram | ✅ |
| 路径图 / 通路图 / pathway diagram | ✅ |
| 技术路线图 / 研究技术路线 / roadmap | ✅ |
| 研究框架图 / 理论框架图 / conceptual framework | ✅ |
| 系统架构示意 / 模型结构示意 | ✅ |
| Graphical Abstract / 期刊封面图 / 论文配图 | ✅ |
| 折线图、柱状图、散点图、热图、森林图、系数图 | ❌ → `nature-figure`（Python/R，绑真实数据） |
| Table 1 / 回归表 / 描述统计表 | ❌ → `nature-skills` 路由 |
| 要在 Visio 里逐个形状改的工程图 | ❌ → `auto-visio-helper` / `visio-image-rebuilder` |

**边界判据**：图里有没有必须与真实数值对齐的坐标轴或刻度？有 → 不是本技能。

---

## 强制工作流

不要一上来就拼提示词丢给模型。按下面四步走，每步都有产出物。

### 第 1 步 — 写中文图释（Figure Brief），并与用户确认

在调任何脚本之前，先用中文写清楚这五项，展示给用户：

1. **图的类型**：示意 / 机制 / 路径 / 技术路线 / 框架（决定构图与画幅）
2. **要素清单**：图里出现的每个方块、节点、图标，逐条列出，写清各自的中文标签
3. **关系与方向**：谁指向谁，箭头是单向还是双向，是否有反馈回路、分支、并行泳道
4. **布局**：左→右流程 / 上→下分层 / 中心辐射 / 环形闭环 / 时间轴
5. **画幅与用途**：论文正文单栏、双栏跨页、PPT 16:9、标书 A4——决定 `--size`

> 要素超过 12 个、或存在三层以上嵌套时，先提醒用户：生成式模型在密集图上容易丢元素或写错标签，
> 建议拆成 2 张，或改走 `auto-visio-helper` 出可编辑矢量图。让用户决定，不要自作主张换方案。

### 第 2 步 — 把图释翻成英文提示词

按 `references/diagram-recipes.md` 里对应图型的模板写。硬性要求：

- **提示词整体用英文**。模型对英文指令的服从度明显更高。
- **图内标签默认用英文**。中文字形常被画成乱码。用户坚持要中文标签时，照办，
  但必须在第 4 步逐字核对字形，并提前告知返工概率较高。
- 每个标签在提示词里**用引号原样写出**，例如 `a box labeled "Policy Shock"`，
  不要只描述"一个政策冲击的方块"。
- 显式写死风格三件套：`flat vector infographic`、`clean white background`、
  `thin uniform stroke weight`。
- 显式写死排除项：`no photorealism, no 3D bevel, no drop shadows, no lens flare,
  no stock-photo people, no watermark, no signature, no decorative clutter`。

### 第 3 步 — 生成

```bash
python3 <SKILL_DIR>/scripts/gpt_image2.py "<英文提示词>" \
  -o figures/mechanism.png --size 1536x1024 --quality high
```

首次使用或报错时，先自检（不产生生成费用）：

```bash
python3 <SKILL_DIR>/scripts/gpt_image2.py --check
```

一次要出多张（比如技术路线图的 3 个备选构图）时走批量清单：

```bash
python3 <SKILL_DIR>/scripts/gpt_image2.py --manifest figures/prompts.json -o figures/
```

有草图或参考图要改画时：

```bash
python3 <SKILL_DIR>/scripts/gpt_image2.py "<英文提示词>" --image sketch.png -o figures/v2.png
```

常用参数：

| 参数 | 说明 |
|---|---|
| `--size` | `1536x1024`（横，默认，适合路线图/流程图）、`1024x1024`（方，机制图）、`1024x1536`（竖，分层框架图）；也接受 `16:9` `3:2` `1:1` `9:16` 别名 |
| `--quality` | `high`（默认）/ `medium` / `low` |
| `--background` | `transparent` 用于要叠进 PPT 的元素（需 png/webp） |
| `-n` | 一次出几张备选，挑图时用 `-n 2` 或 `-n 3` |
| `--dry-run` | 只打印请求体，不调用，用于排查参数 |

### 第 4 步 — 看图质检（不可跳过）

生成完必须用 Read 工具把 PNG **实际看一遍**，逐项核对，把结论写给用户：

- [ ] 图内每个文字标签拼写正确、无乱码、无重复叠字、无 AI 常见的伪字母
- [ ] 箭头方向与图释一致，没有该单向却画成双向、或指反
- [ ] 图释里列的要素**一个不少**地出现了
- [ ] 没有凭空多出来的元素、装饰、水印、签名
- [ ] 画幅、留白、可读性适合声明的用途（论文栏宽下最小字号是否还认得出）

任何一项不过：改提示词重生成（针对性地强化出问题的那句），或用 `--image` 带上这一版做定向修正。
**连续两轮仍不达标就停下**，向用户说明失败模式，并给出替代路径（`auto-visio-helper` 出可编辑矢量图，
或人工在 PPT/Illustrator 里拼）。不要无限重试。

---

## 环境配置

脚本零第三方依赖，只用 Python 标准库，自动读取环境代理与 CA 证书。

| 配置项 | 环境变量（按优先级） | 默认值 |
|---|---|---|
| API Key | `GPT_IMAGE_API_KEY` → `CHEDANKJ_API_KEY` → `OPENAI_API_KEY` | 无，必须配 |
| Base URL | `GPT_IMAGE_BASE_URL` → `CHEDANKJ_BASE_URL` → `OPENAI_BASE_URL` | `https://api.chedankj.com/v1` |
| 模型名 | `GPT_IMAGE_MODEL` | `gpt-image-2` |

也可以在当前目录、skill 目录、仓库根或 `~/.gpt-image-2/` 放 `.env` 文件写同名键；
进程环境变量优先于 `.env`。

**出网白名单**：Claude Code 远程环境的出网策略若未放行 `api.chedankj.com`，
`--check` 会报 `Tunnel connection failed: 403 Forbidden`。这是环境侧白名单问题，
**不要尝试绕过**——把该域名加进环境设置的允许列表，或改配一个已放行的网关。

排错细节见 `references/troubleshooting.md`。

---

## 硬性规则

- 生成前必须有第 1 步的中文图释，且要素清单是逐条列出的，不能只写一句"画个机制图"。
- 生成后必须真的看图，不能凭返回码就说"已生成，效果良好"。
- 不要把带真实数据的统计图交给本技能画——生成式模型会把数值画错，这是学术不端风险。
  用户明确要求"随便画个示意的柱状图，数据不用真"时可以做，但必须在交付说明里写明
  **该图为示意，坐标与数值不代表真实数据**。
- 用户提供的参考图若是他人已发表的图，只做风格参考与结构重组，不做像素级复刻。
