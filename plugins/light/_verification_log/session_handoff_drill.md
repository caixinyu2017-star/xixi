# 会话衔接协议 A/B 双会话演练记录（R2.5）

- 演练日期：2026-06-11
- 执行模型：Claude Opus 4.8（Claude Code 内，第三期 R2）
- 演练项目：`projects/dairygoat-detect-track/`（已有检测+跟踪代码骨架的真实示例项目）
- 协议位置：CONVENTIONS §9 / a02 `light-memory-pm`（`templates/handoff_card.md`、`templates/handoff_prompt.md`、`references/session_handoff.md`）/ light-orchestrator §5
- 目的：真实走一遍"A 造卡并打印启动提示词 → B 只凭提示词恢复 → B 比对状态无损并续下一步 → B 自传播造 S02 卡 → 验证沿 parent_session 链可回读 A 卡"。

## 演练设置

示例项目演练前无 `.light/` 目录（轻量项目，靠 db09 项目卡承载状态）。本演练按协议在项目根新建 `.light/handoff/`，落两张衔接卡，验证主动交接与衔接链。两张卡刻意保留为仓库内的工作示例（衔接卡纳入版本控制，见 a06 gitignore 模板注释）。

## A 会话（S01）：主动交接两件套

T2（任务收尾）触发。A 完成检测+跟踪骨架后，按协议交付两件套：

1. **衔接卡落盘**：`projects/dairygoat-detect-track/.light/handoff/S01-behavior-training-scaffold.md`
   - 字段齐全：当前阶段 / 已完成（带 pytest 验证摘要）/ 工作区状态 / 下一步 3 条 / 阻塞风险 / 必读文件按序 / 禁止。
   - `parent_session: none`（首卡），`suggested_title: "[goat] S02 行为识别训练脚本落地"`。

2. **启动提示词打印**（A 打印给用户的实际内容，按 `handoff_prompt.md` 填值）：

```
【请把本对话命名为：[goat] S02 行为识别训练脚本落地】
你在 d:\skill\Light\projects\dairygoat-detect-track 工作，接续上一个会话（S01）。
先按顺序读：
1. .light/handoff/S01-behavior-training-scaffold.md（衔接卡，含已完成/下一步/禁止事项）
2. .light/passport.yaml（本演练项目暂无则跳过）与 databases/db09-projects/projects/dairygoat-detect-track/project_card.md
读完先用 git status / git log -3 刷新现实，再开始执行衔接卡"下一步"第 1 条。
本段目标：把行为识别训练脚本从 ~25% 推进到合成小样本可跑通。完成判据：tracks.jsonl→片段聚合→TSM/VideoMAE 训练入口能在合成样本上跑通且有最小测试。
收尾要求：更新衔接卡（新建 S02 卡）并打印下一段启动提示词——本协议自传播，不许断链。
```

## B 会话（S02）：只凭提示词恢复 + 比对无损 + 自传播

B 模拟"只拿到 A 的启动提示词、无 A 的对话记忆"的新对话，按提示词执行恢复探针：

| 恢复探针 | 命令/动作 | 结果 |
|---|---|---|
| 读衔接卡 | 读 S01 卡 | 拿到当前阶段/已完成/下一步，自包含，无需翻历史对话 |
| 卡 ≠ 事实，刷新 git | `git log --oneline -3` / `git status --short` | 现实与卡一致（工作区为 R2 文档改动，业务代码未动）|
| 校验"已完成"声明 | `pytest tests/test_infer_track.py -q` | **2 passed** — S01 卡"pytest 2 项通过"声明核实无损 |
| 校验产物路径 | `ls src/infer_track.py src/train.py` | 均存在，与卡一致 |

**比对结论：状态无损恢复。** B 不需要 A 的任何聊天上下文，仅凭 S01 卡 + 一次 git/pytest 刷新即可续上"下一步"第 1 条（行为训练脚本入口）。

**自传播**：B 收尾按协议新建 `S02-innovation-lock-annotation.md`，`parent_session: S01`，并准备打印 S03 启动提示词——协议不断链。

## 衔接链演练（B 沿 parent_session 回读 A）

```
$ grep parent_session .light/handoff/S02-innovation-lock-annotation.md
parent_session: S01
$ grep "session_no\|parent_session" .light/handoff/S01-behavior-training-scaffold.md
session_no: S01
parent_session: none
```

链路：S02 → (parent_session) → S01 → (parent_session) → none。从 B 会话出发，只读 S02 的 `parent_session` 字段即可定位并读回 A 的 S01 卡，验证"无缝衔接到上级任意一个对话"——衔接链是文件链，不依赖聊天记忆。

## R2.5 验收逐条核对

- [x] A 造卡并打印提示词 → B 只凭提示词恢复 → B 比对状态无损并能续"下一步"第 1 条（pytest 2 passed 实证）。
- [x] 衔接链演练：B 造 S02 卡，验证从 B 沿 parent_session 读回 A 的 S01 卡。
- [x] `grep -rn "handoff" skills/light-orchestrator/` 无两套格式并存（§5 已收编为 a02 两件套单一口径，旧自带 `## Handoff` 摘要块已删）。
- [x] ROUTER_EXAMPLES 新增 3 个主动交接正例（route_examples 44→47），check_skills/check_entry_docs/check_skill_links 全绿。
- [x] 安装视角：新增模板/参考随 a02 技能目录走（`templates/`、`references/`），无仓库级引用断链。

## 已知局限（如实声明）

- 无项目目录的轻对话只能打印启动提示词、不落衔接卡（无 `.light/` 可安放），状态靠提示词单件传递。
- 客户端无改名 API，对话命名只能请用户手动按提示词第一行设置。
