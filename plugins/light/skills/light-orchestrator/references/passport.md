# 产物台账（Passport）

一份贯穿整个 pipeline 的记录，回答三个问题：**做到哪了、每步产出了什么、过了哪些关**。中断后据此续跑。写入 a02 memory-pm 的项目记忆。

## 为什么需要

跨阶段任务常被打断（换天、等实验、等审稿）。没有台账，重启时只能靠翻聊天记录猜进度，容易重做或跳步。台账让"做到哪了"有单一真相源。

## 字段

每个已完成阶段记一条：

```yaml
project: <项目名/slug>
pipeline: A   # 走的哪条链
created: 2026-06-08T09:00   # 首次启动时间，固定不变
updated: 2026-06-08T14:30   # 台账最后更新时间，续跑时判断新旧（记到分钟）
current_stage: 8  # 当前到第几阶段
stages:
  - stage: 1
    skill: m01
    input: "用户提供的信用卡欺诈数据集 + 研究目标"
    output: "文献清单 12 篇，方向=校准+不平衡，gap=缺少树模型系统对照"
    artifacts: [docs/lit-review.md]
    gate: {type: confirm, result: PASS, notes: "来源均可核"}
  - stage: 4
    round: 2   # m03⇄m04 回环的第几轮，首轮可省略
    revision_rounds: 1   # 本阶段已用整体返修轮次（上限 2），续跑从此读、不重置
    skill: m04
    input: "m03 第 2 轮提出的 idea"
    output: "idea 八维 72 分，新颖性存疑"
    gate: {type: decision, choice: "微调放行（缩小到树模型）", by: user}
  - stage: 8
    skill: m07
    input: "m05 方案 + a03 实验结果 + m06 分析"
    output: "初稿 6 节"
    revision_rounds: 1   # 诚信门返修 1 轮后过，配额还剩 1 轮
    gate: {type: confirm, result: FAIL→PASS, notes: "首轮 2 处幻觉引用(M2)，已删/替换后过"}
    gaps: ["讨论节 1 处 [RESULT GAP] 待补敏感性分析"]
known_limitations:
  - "E5 先验校正为负结果，如实写入，未强行修正"
```

字段说明：
- `input`：本阶段从上游接收了什么——续跑和回溯时靠它还原阶段间交接。
- `round`：m03⇄m04 这类回环阶段记第几轮；线性阶段省略。
- `revision_rounds`：本阶段在确认点已用的**整体返修轮次**（一轮 = 把该阶段所有 Critical 项一起修一遍再复检）。上限 2（见 `checkpoints.md`）。**这是跨会话续跑的配额真相源**：断点恢复后从台账读这个数继续计，不重置归零，否则换一次会话就能把返修配额刷新、绕过"2 轮后转已知局限"的诚实约束。首轮过关可省略（视为 0）。
- `created`：首次启动 pipeline 的时间，建后不改。
- `updated`：每次写台账都刷新（记到分钟），续跑时一眼看出进度多旧、项目跨了多久。

## 用工具读写，别手填（schema 校验）

台账由 `scripts/passport.py` 维护，把"手填 YAML"变成"工具调用 + schema 校验"，堵三类机械错误：必填字段缺失、stage 序号乱序/重复、gate.result 枚举非法。脚本只校验**结构**，不判断 input/output 文字是否属实——内容真实性仍靠 a08/a10 闸门与人工。

四个子命令（脚本不强依赖 PyYAML：解析时 try-import，缺了就退回内置最小 YAML 解析器；写出始终用内置 emitter，输出稳定确定）：

```bash
# 启动 pipeline：新建台账（已存在则报错，避免覆盖续跑现场）
python scripts/passport.py init --project <slug> --pipeline A --out .light/passport.yaml
# 每过一阶段：追加一条（写入前自动 validate，FAIL 不落盘）
python scripts/passport.py append-stage --file .light/passport.yaml \
    --stage 8 --skill m07 --input "..." --output "初稿6节" \
    --revision-rounds 1 --gate-type confirm --gate-result FAIL->PASS \
    --gate-notes "2处幻觉引用已删" --gaps "[RESULT GAP] 待补敏感性分析"
# 续跑：读当前阶段摘要（含 revision_rounds 已用配额）
python scripts/passport.py get-current-stage --file .light/passport.yaml
# 任意时刻：全量 schema 校验，FAIL 返回非零
python scripts/passport.py validate --file .light/passport.yaml
```

校验规则：顶层必填 `project/pipeline/created/updated/current_stage`；每阶段必填 `stage/skill/input/output`；`stage` 序号必须整数且升序无重复；`gate.type ∈ {confirm, decision}`，confirm 的 `result ∈ {PASS, FAIL, WARN, FAIL->PASS}`，decision 须有 `choice`；`revision_rounds` 为非负整数，超过 2 轮上限给 WARN（提示应转 known_limitations）。一条 `examples/passport-evolution.yaml` 给出从数据集到诚信门返修的端到端演进快照。

## 存哪 / 叫什么（续跑的前提）

台账存为项目记忆里的固定文件：**`.light/passport.yaml`**（项目根目录下）。这是 orchestrator 和 a02 memory-pm 约定的单一位置。

- 启动 pipeline 时：先查 `.light/passport.yaml` 是否存在——存在则是续跑（读 current_stage 接着走），不存在则新建。
- 每过一阶段：更新该文件并刷新 `updated`。
- a02 memory-pm 负责把它纳入项目长期记忆、跨会话恢复；orchestrator 只负责按上述路径读写内容。

## 维护规则

- 每过一个阶段就追加一条，**当场写**，别攒到最后补。
- 决策点记录用户**选了什么**（choice + by:user），不只记"已确认"。
- 确认点记录闸门结果；FAIL→PASS 要记原因（什么不达标、怎么修的）。
- GAP 和 known_limitations 必须如实留痕——这是诚实底线，不是可选项。
- 确认点返修后更新该阶段 `revision_rounds`；续跑时**从台账读已用轮次接着计，不重置**——配额刷新等于绕过 2 轮上限的诚实约束。
- 续跑时：读台账 → 定位 current_stage → 从下一阶段继续，已过阶段不重跑（除非用户要求）。

## 与 memory-pm 的关系

台账是 pipeline 维度的进度记录，memory-pm 是项目维度的长期记忆。台账写入 memory-pm 作为项目卡的一部分；memory-pm 负责持久化和跨会话恢复。编排器只管在 pipeline 运行时维护台账内容。
