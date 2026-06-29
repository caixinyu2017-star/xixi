# 发现技能（skill）呈现模板

当通过 skills.sh 排行榜或 `npx skills find <query>` 找到候选 skill 时，用此模板向用户汇报，再征得同意后安装。不要凭搜索结果直接装——先核对质量信号。

## 单个候选

```
找到一个可能合适的 skill：

  名称：<owner/repo@skill-name>
  用途：<一句话说明它做什么>
  安装量：<N>（来源：skills.sh 排行榜 / npx skills find）
  来源：<owner>（官方 anthropics/vercel-labs/microsoft？社区？）
  GitHub stars：<N>
  质量判断：<放心用 / 谨慎 / 存疑> —— 依据 安装量≥1K & star≥100 阈值
  链接：https://skills.sh/<owner>/<repo>/<skill-name>

安装命令（确认后执行）：
  npx skills add <owner/repo@skill-name> -g -y
  （-g 全局安装，-y 免确认）

要我装吗？
```

## 多个候选（对比表）

```
针对「<用户需求>」找到 N 个候选 skill：

| 名称 | 用途 | 安装量 | 来源 | star | 质量 |
|------|------|--------|------|------|------|
| owner/repo@a | ... | 185K | vercel-labs(官方) | 2.1K | 放心 |
| owner/repo@b | ... | 800  | 社区              | 120  | 谨慎 |
| owner/repo@c | ... | 40   | 无名              | 12   | 存疑 |

推荐 a（官方源 + 高安装量）。安装：
  npx skills add owner/repo@a -g -y

要装 a，还是看其它？
```

## 未找到时（坦白 + 兜底）

```
搜了「<query>」相关的 skill，没有命中合适的（或都低于质量阈值）。

我可以直接用通用能力帮你完成这个任务。要继续吗？

如果这是常做的事，也可以自建 skill：
  npx skills init my-<name>
（再按 skill-creator 路线补 SKILL.md / scripts / references / assets）
```

## 质量阈值速查（核对后再推荐）

- 安装量：≥1K 放心 / 100-1K 谨慎 / <100 存疑
- GitHub star：≥100 较可信 / <100 需额外审查
- 来源：anthropics / vercel-labs / microsoft 官方最可信
- 任何第三方 skill = 引入外部指令与脚本，安装即授权，先评估安全。

## 验证过的入口（2026-06 实测）

- skills.sh 排行榜：`https://skills.sh/` → 308 重定向到 `https://www.skills.sh/`（最终 200）。
- Skills CLI 包：npm `skills`，最新版 1.5.10（`https://registry.npmjs.org/skills` → 200）。
- 命令：`npx skills find` / `add` / `check` / `update` / `init`。
