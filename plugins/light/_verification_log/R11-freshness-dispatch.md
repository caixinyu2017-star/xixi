# R11.3 数据卡保鲜月度自动化 · 实测留痕

- 日期：2026-06-12
- 工作流：`.github/workflows/freshness.yml`（schedule 每月1日 + workflow_dispatch 手动入口）
- 跑的脚本：`.github/scripts/check_freshness.py`（R8.6 产物，warn-only，当前基线 318 卡）

## workflow_dispatch 手动触发实测（成功）

### 现场结构性约束（先记，属偏差日志级别）
GitHub 硬规则：**workflow_dispatch 只能触发"默认分支上已存在的工作流文件"**。本仓库 R1-R11 以叠加 PR 形式维护、尚未并入 master（master 落后约 46 提交，连 check_freshness.py 都未合并）。直接在 `r11-evals-automation` 分支 dispatch 报：

```
gh workflow run freshness.yml --ref r11-evals-automation
→ HTTP 404: workflow freshness.yml not found on the default branch
```

处理（经用户授权，可逆方案）：临时把仓库默认分支切到 `r11-evals-automation` → 实测 → **立即切回 master**。全程默认分支变更前后均记录并复原，未改动 master 任何内容。

### 实测记录（两次 dispatch，覆盖两条 issue 逻辑）

为同时验证"开单"和"更单"两条路径，dispatch 时用 `today=2026-12-01`（未来日）人为制造超期，`threshold_days=90`。注意这是**演练用的人为基准日**——真实基准日 2026-06-12 下全部 318 卡均在阈值内、`stale_count=0`、不会开单（本地已双路径验证：今天→0 张超期，2026-12-01→318 张超期）。

| # | run 链接 | event | 结论 | 效果 |
|---|---|---|---|---|
| 1 | https://github.com/Light0305/Light-skills/actions/runs/27399467099 | workflow_dispatch | success | **新建** issue #7「数据卡保鲜清单 (2026-06)」 |
| 2 | https://github.com/Light0305/Light-skills/actions/runs/27399541184 | workflow_dispatch | success | **追加评论**到 #7（不重复开单，验证去重逻辑） |

run #1 步骤结论：checkout/Python/跑新鲜度检查/开-更 issue 均 success，"无超期仅记录"步骤正确 skipped。

issue #7 自动生成正文（节选，证明内容真实由脚本输出回填）：
```
> 由 `.github/workflows/freshness.yml` 自动生成于 2026-06-12T06:44Z（UTC）。
以下数据卡超过新鲜度阈值未复查……
数据卡新鲜度（基准日 2026-12-01，阈值 90 天，warn-only）
  db01-venues-templates: 308 张卡, 308 超期
      ! CVPR — 2026-06-01（183 天）……
```

### 收尾
- issue #7 系演练产物（人为未来基准日），实测后已加说明评论并 **关闭**（reason: not planned）。当前无遗留开放保鲜 issue。
- 仓库默认分支已复原为 `master`（`gh repo view --json defaultBranchRef` 确认 = master）。

## 结论
R11.3 验收项「workflow_dispatch 手动触发一次成功并真实生成/更新 issue」**达成**：两次真实 run 均 success，分别验证了开单与更单两条路径，留 run 链接如上。

合并入 master 后（R10 收官），此工作流的 schedule（每月1日）与 workflow_dispatch 即在默认分支长期可用；README 维护节律指向手动入口（应对 GitHub 60 天不活跃自动停 schedule、fork 默认禁用两条限制，工作流注释已写明）。
