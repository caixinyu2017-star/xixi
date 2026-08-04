# gpt-image-2

用环境中已配置的 **gpt-image-2** 模型生成科研与工程用的**概念类图像**：示意图、机制图、路径图、
技术路线图、研究框架图、Graphical Abstract。

## 这个插件解决什么

科研写作里有两类完全不同的"画图"需求，经常被混在一起：

| 类型 | 特征 | 正确工具 |
|---|---|---|
| **概念类图** | 没有坐标轴，画的是结构、关系、流程、机制 | **本插件**（生成式模型） |
| **数据类图** | 有坐标轴，每个点必须对应真实数值 | `nature-figure`（Python/R 绘制） |

本插件只做前者，并在 SKILL.md 里把边界写死，避免生成式模型去画带真实数据的统计图
——那是学术不端风险。

## 安装

```text
/plugin marketplace add caixinyu2017-star/xixi
/plugin install gpt-image-2@xixi-research-skills
```

装完重启 Claude Code。之后凡是聊到"示意图 / 机制图 / 路径图 / 技术路线图 / 研究框架图 /
配图 / schematic / mechanism diagram / pathway diagram / technical roadmap"，技能会自动触发；
也可以用 `/gpt-image-2` 显式调用。

在 `xixi` 仓库内，`.claude/skills/gpt-image-2` 已软链到本技能，无需安装即可直接生效。

## 配置

| 配置项 | 环境变量（按优先级） | 默认值 |
|---|---|---|
| API Key | `GPT_IMAGE_API_KEY` → `CHEDANKJ_API_KEY` → `OPENAI_API_KEY` | 无，必须配 |
| Base URL | `GPT_IMAGE_BASE_URL` → `CHEDANKJ_BASE_URL` → `OPENAI_BASE_URL` | `https://chedankj.com/v1` |
| 模型名 | `GPT_IMAGE_MODEL` | `gpt-image-2` |

也支持在当前目录 / skill 目录 / 仓库根 / `~/.gpt-image-2/` 放 `.env`（进程环境变量优先）。

先自检，不产生生成费用：

```bash
python3 skills/gpt-image-2/scripts/gpt_image2.py --check
```

> 已实测可用：自检返回 200，模型列表里有 `gpt-image-2`，端到端出图正常。
> 两个坑：**域名不要写成 `api.chedankj.com`**（不通），**User-Agent 不能是 `Python-urllib/*`**
> （网关 WAF 返 403，脚本已固定发 `gpt-image-2-skill/1.0`）。

## CLI

零第三方依赖，只用 Python 标准库（自动读取环境代理与 CA 证书）。

```bash
S=skills/gpt-image-2/scripts/gpt_image2.py

# 配置与连通性自检
python3 $S --check

# 单图
python3 $S "flat vector mechanism diagram ..." -o figures/fig1.png --size 1536x1024

# 出 3 张备选
python3 $S "..." -o figures/ -n 3

# 批量：{"items":[{"filename":"f1.png","prompt":"...","size":"16:9"}, ...]}
python3 $S --manifest figures/prompts.json -o figures/

# 参考图改画（走 /images/edits）
python3 $S "redraw as a clean journal schematic" --image sketch.png -o figures/v2.png

# 只打印请求体，不调用
python3 $S "..." --dry-run
```

画幅：`1024x1024` / `1536x1024` / `1024x1536` / `auto`，也接受 `1:1` `3:2` `16:9` `2:3` `9:16` 别名。

## 工作流

技能强制走四步，不允许直接甩提示词给模型：

1. **中文图释** — 图型、要素清单、关系与方向、布局、画幅用途，先给用户确认
2. **英文提示词** — 按 `references/diagram-recipes.md` 的图型模板写，标签用引号原样写出
3. **生成** — 调 CLI 出 PNG
4. **看图质检** — 用 Read 实际看图，逐项核对文字乱码、箭头方向、要素缺失、多余装饰

两轮改不好就停，改走 `auto-visio-helper`（可编辑 Visio）或 `nature-figure`（Python/R）。

## 目录

```
plugins/gpt-image-2/
├── .claude-plugin/plugin.json
├── README.md
└── skills/gpt-image-2/
    ├── SKILL.md
    ├── references/
    │   ├── diagram-recipes.md   # 5 类图型提示词配方 + 学术配色 + 失败模式对照表
    │   └── troubleshooting.md   # 退出码、代理白名单、API 错误码、响应兼容
    └── scripts/
        └── gpt_image2.py        # OpenAI 兼容 CLI，零第三方依赖
```

## License

MIT
