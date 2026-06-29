# db09 — 用户个人项目知识库

为每个科研项目建立**独立**知识库，长期陪伴项目从选题到成果转化。这是 a02(记忆PM)、a07(一致性) 的状态中枢，所有技能的产出都在此登记。

## 这个库是什么(诚实卖点)

db09 是**项目状态中枢 + B-fact 回指在线源**。与其他 8 库不同,**本库卡数/字段不缩水**(~82% 是项目状态 C 类,在线源不知道"你上周决定弃用 re-id",这正是它存在的唯一理由,必须本地)——重构只是把卡内少量对外部事实的引用(venue 计量/数据集许可/DOI)的**引用方式变严**:不再隐含"db09 自带权威计量",改为带时间戳的快照线索 + 回指真相源。这与其他库"卡数缩水"性质不同。

- **状态层(C 类,本地精养,核心)**:project_card 14 字段、decision_log、version_history、terminology、saved_search、known_dois、watch_report——项目专属、在线不可得,不动 schema、不转实时。
- **方法论层(A 通用,本地)**:lessons.md 跨项目过程教训,归档时去偏科化回写。
- **B-fact 引用三件套(对外部事实的引用)**:见下纪律节。

## project_card schema
`project_name, goal, current_stage, confirmed_idea, data_status, method_status, experiment_status, paper_status, ppt_status, code_status, risk_list, next_actions, decision_log, version_history`

## B-fact 引用三件套纪律（硬性）
db09 卡内凡引用 **venue 计量 / 数据集许可/DOI / 外部数值** 等他库权威事实,**不当自带权威**,必须写成三件套:**快照值(可带 ≈) + `[snapshot YYYY-MM-DD, src=dbNN:文件#定位, 用前重核, 冲突信在线]`**。`palette.json` 是既成样板(每 token 带 source 回指 db05/db06 + last_checked + 顶层 `$aligned_with`)。
- **存值但标快照**:允许本地留数值(无网时有线索),但带 last_checked,绝不假装是当前值。
- **超期重核(a02 读卡时)**:计量值(h_index/被引)>90 天、许可类 >365 天给"需重核"提示,投稿/用前以在线/官方源为准。
- **冲突信在线**:重核后不一致就地更新快照值 + last_checked。
- 现存三处:decision_log venue 计量(回指 db01:venues.csv)、project_card/terminology 数据集许可DOI(回指 db04)、palette hex(回指 db05 DTCG)。

- `current_stage`: 资料调研 | idea 构思 | 方案确认 | 数据准备 | 实验实现 | 结果分析 | 论文写作 | 图表制作 | 投稿准备 | 答辩展示 | 成果转化
- `archived`（可选，归档专用）：项目完结后加 `archived: YYYY-MM-DD`（可再加 `archive_reason:`）。属**可选**字段，不在上述 14 必填字段内，check_databases 校验只认 14 必填、对额外字段兼容。归档协议见下「项目归档」节，执行者是 a02(light-memory-pm)。

## 顶层目录结构
```
db09-projects/
├── README.md              本说明
├── project_card_template.md
├── lessons.md             跨项目过程/方法论教训库（与 projects/ 平级，见下）
└── projects/<project_name>/   每个项目一个独立目录（结构见下）
```

## lessons.md — 跨项目过程教训库
全局单文件，追加式。收"做法层面的有效/失败经验"（踩坑、被拒、复现失败、流程省时），**不收**方法选型事实（→ db03 方法卡）与个人偏好（→ Light feedback 记忆）。格式：`- [YYYY-MM-DD] 阶段/场景 — 做法 — 结果(有效|失败) — 适用条件 — 来源项目slug`。写入纪律与检索时机见 a02 SKILL.md。

## 项目归档（防膨胀，执行者 a02）
db09 只进不出会越攒越多、拖慢会话开始扫描。完结项目**归档不删除**（历史/lessons 仍可复用）。
- **完结判据**（满足其一）：论文录用/发表、竞赛或项目验收结题、用户显式声明收尾。
- **归档动作**（加字段，不挪目录——最轻且不破坏相对路径/本 README 链接）：① project_card.md 字段块加 `archived: YYYY-MM-DD`（可选，不计入 14 必填，schema 校验兼容）；② 把该项目 1-3 条可跨项目复用的过程教训回写 `lessons.md`（出库前最后一次沉淀）；③ 目录原地保留。
- **会话开始行为**：a02 罗列/恢复项目时**跳过** `archived` 非空者，除非用户点名；删掉 `archived` 行即"复活"回活跃集。
- 协议细则见 a02 `references.md`「项目归档协议」节。

## 每个项目目录结构
```
projects/<project_name>/
├── project_card.md       项目卡(上述字段)
├── terminology.md        术语/指标/创新点统一定义表(供 a07)
├── decision_log.md       重大决策时间线(含 idea 取舍、方案变更)
├── version_history.md    论文/PPT/图表/代码各版本记录
├── palette.json          跨材料共享色板(视觉 SSOT 实例，可选；论文图/PPT/前端共读，见下)
├── literature/           m01 调研产出
├── reviews/              m14 审稿意见与 response
└── submissions/          投稿记录(venue/日期/状态/结果)
```

## palette.json — 跨材料共享色板（视觉 SSOT 实例）
解决"slides 与 figure 风格统一只能靠 a07 人工把关"：项目级一份 `palette.json`，论文图(m11/db07)、PPT(m16/db06)、前端(a05/db05)三方共读——**有则必用**，谁都不另起一套色板；a07 的"跨材料配色一致"检查改为对照本文件。

它是 db05 `design_tokens.template.json`（DTCG 视觉 SSOT，色值锚点真相源，a05/a07 维护）在本项目的**落地副本/扁平视图**，字段与之对齐，色值最终以 db05 DTCG 模板为准。改色只改这一份并触发 a07 变更广播回扫下游。

schema（每个 token 一项）：

| 字段 | 含义 |
|---|---|
| `name` | token 名（primary/secondary/accent/text/bg/surface/muted/line/success/warning/danger/info…，对齐 themes.py 8 字段色板 + DTCG 语义色） |
| `hex` | `#RRGGBB` 色值 |
| `usage` | 用途：主色 / 辅色 / 强调 / 语义色（成功/警告/危险/信息）/ 背景 / 文字 / 分隔线 等 |
| `source` | 取色出处，**须真实可追溯**：指向 db05 卡或 db06 卡 id（如 `db06:light-slides/assets/themes.py::AGRICULTURE.COLORS.primary`、`db05:design_tokens.template.json::color.semantic.success`） |
| `last_checked` | 核验日期 `YYYY-MM-DD` |

顶层带 `$description`/`$project`/`$aligned_with`（指回 db05 DTCG 模板路径）。**铁律**：`hex`/`source` 不凭记忆填，每个 token 的 source 指向 db05/db06 真实卡并经核验。实例见 `projects/dairygoat-detect-track/palette.json`（取色自 db06 themes.py 农业风主题 + db05 DTCG 语义色，selftest 绿）。

## 管理工具映射
- 代码/文本版本 → Git
- 数据/实验 → DVC / MLflow / W&B
- 文献 → Zotero
- 项目知识 → Obsidian / Notion / Markdown / Logseq
- 进展 → README + CHANGELOG

## 更新纪律（硬性，联动 a02）
每次完成：资料搜索 / idea 修改 / 实验运行 / 论文修改 / PPT 修改 / 投稿返修——**立即**更新对应 status + decision_log + version_history，避免上下文丢失。

## 与跨会话记忆的关系
项目级状态存这里(db09)；跨会话的用户偏好/项目背景/参考资源额外写入 Light 记忆文件并在 MEMORY.md 加索引(见 a02)。会话开始先读 project_card 恢复 `current_stage` 与 `next_actions`。

模板见 [project_card_template.md](project_card_template.md)。
