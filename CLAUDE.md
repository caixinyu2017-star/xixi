# xixi-research-skills — 仓库约定

本仓库是一个 Claude Code 插件市场（marketplace 名：`xixi-research-skills`）。
下面的路由规则对**本仓库内的所有会话**生效。

## 技能路由规则（强制）

### 1. 概念类图 → `gpt-image-2`

用户提到下列任一需求时，**直接调用 `gpt-image-2` 技能**，不要自己写 SVG、不要用 matplotlib
凑一张、也不要只给文字描述：

> 示意图、机制图、机理图、路径图、通路图、技术路线图、研究技术路线、研究框架图、理论框架图、
> 概念图、原理图、流程示意、架构示意、模型结构图、Graphical Abstract、期刊封面图、论文配图，
> 以及 schematic / mechanism diagram / pathway diagram / technical roadmap /
> conceptual framework / graphical abstract。

技能会用环境中配置好的 **gpt-image-2** 模型出图，并强制走
「中文图释 → 英文提示词 → 生成 → 看图质检」四步。

### 2. 数据分析与实证分析 → `nature-skills`

用户提到下列任一需求时，**直接调用 `nature-skills` 技能**作为总入口：

> 数据分析、实证分析、计量分析、统计分析、跑数据、分析这份数据、描述统计、Table 1、
> 相关性分析、回归、DID、双重差分、工具变量 / IV、断点回归 / RDD、倾向得分匹配 / PSM、
> 合成控制、面板固定效应、中介效应、机制检验、异质性分析、稳健性检验、显著性、
> 出结果表、结果解读、把结果写成文字，以及 data analysis / empirical analysis /
> econometric analysis / regression / robustness / heterogeneity / results section。

该技能负责 8 步流水线（数据审计 → 描述统计 → 识别策略 → 估计 → 稳健性 → 机制与异质性 →
表图产出 → 结果文字），并按需路由到 `nature-figure`、`nature-data`、`nature-writing`、
`nature-polishing`、`nature-citation`，重型计量下沉到 `empirical-analysis-python/stata/r`。

### 3. 两者的分界线

**图里有没有必须与真实数值对齐的坐标轴或刻度？**

- **有** → 数据类图 → 走 `nature-skills` → 由 `nature-figure` 用 Python/R 绘制。
  **绝不允许**用生成式图像模型画带真实数据的统计图（折线、柱状、散点、热图、森林图、
  系数图），那会画错数值，是学术不端风险。
- **没有** → 概念类图 → 走 `gpt-image-2`。

需要事后逐个形状编辑的 Visio 工程图，两者都不走，交给 `auto-visio-helper` /
`visio-image-rebuilder`。

## 技能如何在本仓库生效

`.claude/skills/` 下用软链把插件内的技能挂进项目，无需 `/plugin install` 即可直接触发：

```
.claude/skills/gpt-image-2    -> ../../plugins/gpt-image-2/skills/gpt-image-2
.claude/skills/nature-skills  -> ../../plugins/nature-skills/skills/nature-skills
.claude/skills/cyber-ppt      -> ../../plugins/cyber-ppt/skills/cyber-ppt
.claude/skills/dashiai-ppt    -> ../../plugins/dashiai-ppt/skills/dashiai-ppt
```

新增技能要在本仓库自动生效，照此加软链；跨仓库/网页端生效则把技能目录打包上传到
claude.ai 的 **Customize → Skills**（打包脚本见 `customize/build.sh`）。

## gpt-image-2 环境配置

| 配置项 | 环境变量（按优先级） | 默认值 |
|---|---|---|
| API Key | `GPT_IMAGE_API_KEY` → `CHEDANKJ_API_KEY` → `OPENAI_API_KEY` | 无，必须配 |
| Base URL | `GPT_IMAGE_BASE_URL` → `CHEDANKJ_BASE_URL` → `OPENAI_BASE_URL` | `https://chedankj.com/v1` |
| 模型名 | `GPT_IMAGE_MODEL` | `gpt-image-2` |

自检（不产生生成费用）：

```bash
python3 plugins/gpt-image-2/skills/gpt-image-2/scripts/gpt_image2.py --check
```

已实测可用（自检 200、模型列表含 `gpt-image-2`、端到端出图正常）。两个坑：

- 域名是 `chedankj.com`，**不要加 `api.` 前缀**——`api.chedankj.com` 不通。
- 网关前置 WAF 拒绝 `Python-urllib/*` 这类 User-Agent（返 403），脚本已固定发
  `gpt-image-2-skill/1.0`；手写 curl 复现时也要带上 UA 头。

## 仓库结构约定

- 每个插件放在 `plugins/<name>/`，含 `.claude-plugin/plugin.json` 与 `skills/<skill>/SKILL.md`
- 新增插件必须同步登记到 `.claude-plugin/marketplace.json` 并更新根 `README.md`
- 插件目录保持完整，不要拆散 `skills/_shared/` 这类共享层
