# Customize 上传包

把技能装进 claude.ai 的 **Customize → Skills**，让它在**所有会话**（包括不在本仓库里的会话、
网页端、手机端）都能自动触发。

本仓库的技能有两条生效路径，互不冲突，可以都用：

| 路径 | 生效范围 | 怎么做 |
|---|---|---|
| **仓库软链** | 只在 `xixi` 仓库内的会话 | 已配置好，见 `.claude/skills/`，无需操作 |
| **Customize 上传** | 账号下所有会话 | 用本目录的 zip 手动上传一次 |
| （可选）插件安装 | 装了插件的机器 | `/plugin install <name>@xixi-research-skills` |

## 生成 zip

```bash
bash customize/build.sh
```

产物在 `customize/dist/`：

- `gpt-image-2.zip` — 概念图生成（示意图 / 机制图 / 路径图 / 技术路线图 / 研究框架图）
- `nature-skills.zip` — 数据分析与实证分析总入口（8 步流水线）

两个包都是自包含的：不依赖仓库里的其他路径，也不依赖同插件下的兄弟技能
（兄弟技能在时会自动路由过去，不在时按内置规范自己完成）。

## 上传步骤

1. 打开 <https://claude.ai>
2. 左下角头像 → **Customize**（或 Settings → Capabilities → Skills）
3. **Skills** → **Upload skill**
4. 选 `customize/dist/gpt-image-2.zip`，确认技能名与描述无误
5. 重复第 3–4 步上传 `customize/dist/nature-skills.zip`
6. 确认两个技能都是**启用**状态

> 容器内无法代为上传——Customize 是网页端账号级设置，需要你手动点一次。
> 上传后新开的会话才会加载，已经在跑的会话不会热更新。

## 上传后的效果

| 你说 | 自动走 |
|---|---|
| 「帮我画个机制图」「做张技术路线图」「出个研究框架示意图」 | `gpt-image-2` |
| 「分析下这份数据」「跑个 DID」「做稳健性检验」「把结果写成文字」 | `nature-skills` |

分界线：**图里有没有必须与真实数值对齐的坐标轴？**
有 → 数据类图，走 `nature-skills` → `nature-figure` 用 Python/R 画；
没有 → 概念类图，走 `gpt-image-2`。

## gpt-image-2 的前置配置

技能本身不带密钥，运行时从环境变量读：

| 配置项 | 环境变量（按优先级） | 默认值 |
|---|---|---|
| API Key | `GPT_IMAGE_API_KEY` → `CHEDANKJ_API_KEY` → `OPENAI_API_KEY` | 无，必须配 |
| Base URL | `GPT_IMAGE_BASE_URL` → `CHEDANKJ_BASE_URL` → `OPENAI_BASE_URL` | `https://api.chedankj.com/v1` |
| 模型名 | `GPT_IMAGE_MODEL` | `gpt-image-2` |

在 Claude Code 环境设置的 **Environment variables** 里配 `CHEDANKJ_API_KEY` 即可。
另外要确认环境的**出网策略放行 `api.chedankj.com`**，否则自检会报
`Tunnel connection failed: 403 Forbidden`。

自检（不产生生成费用）：

```bash
python3 plugins/gpt-image-2/skills/gpt-image-2/scripts/gpt_image2.py --check
```

## 更新技能

改完 `SKILL.md` 或 references 后重新 `bash customize/build.sh`，
再去 Customize 里删掉旧技能、上传新 zip。zip 是构建产物，改内容请改源目录，不要直接改 zip。
