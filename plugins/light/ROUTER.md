# Light 技能路由表（ROUTER）

根据用户任务自动选择技能。当用户用 `/` 显式调用某技能时，直接执行该技能。否则按下表匹配意图。典型输入的回归样例见 [ROUTER_EXAMPLES.md](ROUTER_EXAMPLES.md)，用于防止路由边界漂移。

## 任务 → 技能

| 用户意图关键词 | 调用技能 |
|---|---|
| 找文献 / 调研 / 综述 / 这个方向有哪些工作 | m01 literature-search |
| 数据清洗 / 数据质量 / 建数据集 / 数据够不够 | m02 data-engineering |
| 想 idea / 创新点 / 这个能做什么 / 提方案 | m03 idea-generation |
| 这个 idea 行不行 / 够不够创新 / 帮我挑刺 | m04 idea-critique |
| 做研究方案 / 实验设计 / 技术路线 / 怎么做实验 | m05 research-plan |
| 分析结果 / 这些数据说明什么 / 实验跑完了 | m06 result-analysis |
| 写论文 / 写引言 / 写方法 / 写摘要 | m07 paper-drafting |
| 润色 / 改语言 / 这段不通顺 / 增强论证 | m08 paper-polishing |
| 论文该画什么图 / 图表规划 | m09 figure-planning |
| 引用 / 参考文献 / bibtex / 引文格式 | m10 citation |
| 画图 / 出图 / 配色 / 组图 | m11 figure-drawing |
| 排版 / latex / word 模板 / 导出 pdf | m12 typesetting |
| 投哪个期刊 / 会议 / 期刊匹配 / 录用概率 | m13 venue-matching |
| 模拟审稿 / 返修 / response letter / 回复审稿人 | m14 review-rebuttal |
| 软著 / 专利 / 权利要求 | m15 ip-application |
| 做 PPT / 答辩 / 路演幻灯片 | m16 slides |
| 大创 / 挑战杯 / 互联网+ / 申报书 / 商业计划书 | m17 competition |
| 读这个文件 / 这个 PDF/PPT/Excel 讲了啥 | a01 file-reading |
| 记住 / 项目进展 / 我们做到哪了 | a02 memory-pm |
| 继续 / 刚断了 / 接手 Claude / 恢复上下文 / 上次做到哪（断点恢复/跨轮续接） | a02 memory-pm + light-orchestrator |
| 给我衔接提示词 / 开新对话继续 / 这个对话快满了（主动交接，留衔接卡+启动提示词） | a02 memory-pm + light-orchestrator |
| 写代码 / 实验代码 / 复现 | a03 backend-coding |
| 系统设计 / 数据库 / 接口 / ER 图 | a04 system-design |
| 前端 / 界面 / 大屏 / 可视化平台 | a05 frontend-design |
| 整理项目 / 文件夹结构 | a06 project-structure |

## 常驻技能（无需显式调用，默认嵌入每个任务）

- a07 consistency、a08 self-review、a09 tool-selection、a10 research-ethics 在**所有**任务中后台生效。
- a01 file-reading、a02 memory-pm 在涉及文件/长期项目时自动触发。
- **light-orchestrator** 在跨多阶段的大任务（"从X做到Y""全流程"）时启动，规划 pipeline、逐阶段调用下列技能、在阶段间卡强制检查点。用户说"继续/刚断了/接手/恢复上下文"且语义指向断点恢复/跨轮续接时，也优先启动它做断点恢复：先读 git 状态、todo、passport/db09、最近提交/CI，再继续执行；若只是续写当前段落/文本，按写作或润色单技能路由。单一阶段的轻任务不启动它，直接按下表路由。

## 组合调用（常见链路）

> 下列链路的**可执行版**（带阶段产出与检查点）见 light-orchestrator/references/pipelines.md。ROUTER 这里只给概览。

- 新项目启动：a02 → m01 → m02 → m03 ⇄ m04 → m05 → a03(实验实现)
- 写论文：a03(实验) → m06 → m07 ⇄ m08 → m09 → m11 → m10 → m12
- 投稿：m13 → m12 → （投出）→ m14
- 成果转化：m15（软著/专利）、m16（PPT）、m17（竞赛）
