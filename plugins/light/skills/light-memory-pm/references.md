# light-memory-pm 参考工具笔记

研究于 2026-06。WebFetch 在本环境被网络策略全面拦截，以下基于 WebSearch 返回的官方文档/仓库标题与摘要核实；标注【未能核实】处表示无法确认具体细节，未编造端点。

## Open Notebook (lfnovo/open-notebook)
- 【是什么】开源 NotebookLM 替代实现，强调比 Google 版更灵活、更可配置；支持把多来源资料做成笔记并生成播客音频。
- 【可复用方法】核心数据模型是 notebooks → sources（导入的资料）→ notes（人/AI 笔记）三层；提供 transformations（对 source 跑可定制的处理/摘要 prompt）、context 配置（按 source 选择"不放/只摘要/全文"喂给模型，控制上下文成本）、search（跨库检索）、podcast 生成。后端存储用 SurrealDB，模型层用 Esperanto 抽象层对接多家 LLM/TTS provider。可借鉴的设计：用"context 等级（none/summary/full）"显式控制每条资料进入模型上下文的粒度——直接对应本技能"该记什么/不记什么"的取舍。
- 【链接】https://github.com/lfnovo/open-notebook ，Wiki https://github.com/lfnovo/open-notebook/wiki
- 【已知坑】播客质量高度依赖正确配置（XDA 评测明确指出"要配置对才好用"）；自托管需自带 SurrealDB 与各 provider API key。

## Obsidian
- 【是什么】本地优先的 Markdown 知识库，纯文件夹+`.md` 文件，强调双链笔记网络。
- 【可复用方法】用 `[[wikilink]]` 建双链、反向链接(backlinks)自动生成；YAML frontmatter 作 properties（如 `tags:`、自定义字段）。Dataview 社区插件提供对 Markdown 的"数据索引+查询语言"，可写 `dataview` 代码块按 frontmatter 字段查询/汇总笔记（如列出所有 `status: in-progress` 的项目卡）。新版有 Bases（表格化视图）。可借鉴：用 frontmatter 字段承载 project_card 的结构化字段，再用 Dataview 聚合成项目看板。
- 【链接】https://obsidian.md ，Dataview https://github.com/blacksmithgu/obsidian-dataview ，元数据文档 https://blacksmithgu.github.io/obsidian-dataview/annotation/metadata-pages/
- 【已知坑】YAML frontmatter 里的 wikilink 历史上支持不完善（社区长贴讨论）；Dataview 是第三方插件，查询语言非标准 Markdown，迁移到别的工具会失效。

## Zotero
- 【是什么】开源文献管理器，带 Web API v3 与本地条目库。
- 【可复用方法】Web API 基址 `https://api.zotero.org`，按 `/users/<id>/items` 或 `/groups/<id>/items` 取条目，集合用 `/collections`。版本通过 `Zotero-API-Version: 3` 头或 URL 指定；写操作需 API key（`Zotero-API-Key` 头或 `key=` 参数）。支持 `format=bibtex/csljson` 等多种导出格式，配合 Better BibTeX 插件可做引文键管理与自动导出 `.bib`。可借鉴：把"投稿/引用过的文献"用集合分组，按 itemKey + dateModified 做增量同步。
- 【链接】https://api.zotero.org ，官方 API 文档 https://www.zotero.org/support/dev/web_api/v3/start
- 【已知坑】写 API 用 `If-Unmodified-Since-Version` 做乐观锁，版本不匹配会 412；有速率限制（响应带 Backoff / Retry-After 头，须遵守退避）。具体每秒配额【未能核实确切数值】。

## Git（版本与发布管理）
- 【是什么】分布式版本控制；本技能用于代码/文本/论文稿的版本中枢。
- 【可复用方法】用带注释标签 `git tag -a v1.2.0 -m "..."` 标记里程碑版本（注释标签存 tagger/日期/消息，可被 `git describe` 用，轻量标签不行）；遵循 SemVer（MAJOR.MINOR.PATCH）。配合 Conventional Commits（`feat:`/`fix:`/`docs:` 等前缀）可由 conventional-changelog 自动生成 CHANGELOG/release notes。CHANGELOG 遵循 Keep a Changelog 格式（Added/Changed/Fixed/Removed 分组 + 日期）。可借鉴：论文/PPT 也用 tag 标投稿版本（如 `submit-icml2026`），把 version_history 与 git tag 对齐。
- 【链接】Tagging https://git-scm.com/book/en/v2/Git-Basics-Tagging ，SemVer https://semver.org ，Keep a Changelog https://keepachangelog.com ，Conventional Commits https://www.conventionalcommits.org
- 【已知坑】标签默认不随 `git push` 推送，需 `git push --tags` 或 `git push origin <tag>`；二进制大文件（数据/图表）不该进 Git，交给 DVC。

## GitHub Issues（任务/里程碑跟踪）
- 【是什么】GitHub 的工单系统，可作阶段任务清单与里程碑跟踪。
- 【可复用方法】REST API `apiVersion: 2022-11-28`：`POST /repos/{owner}/{repo}/issues`（建 issue，可带 `labels`/`milestone`/`assignees`），`/repos/{owner}/{repo}/milestones` 管理里程碑（带 due_on、open/closed 状态、完成度统计）。Issue 正文里 `- [ ]` / `- [x]` task list 自动渲染成可勾选清单并统计进度。CLI：`gh issue create --title --body --label --milestone`。可借鉴：每个项目阶段=一个 milestone，阶段内任务=带 checkbox 的 issue，risk_list 用 `risk` label 标注。
- 【链接】Issues API https://docs.github.com/rest/issues/issues?apiVersion=2022-11-28 ，Milestones https://docs.github.com/en/rest/issues/milestones ，gh CLI https://cli.github.com/manual/gh_issue_create
- 【已知坑】task list 嵌套/跨 issue 依赖能力有限；私有仓 API 受 token scope 限制；REST 有主限流（认证后约 5000 req/h）。

## DVC（数据/实验版本）
- 【是什么】Git 之上的数据与 ML 流水线版本控制。
- 【可复用方法】`dvc add data/`→生成 `.dvc` 指针文件（存 md5），大文件进 cache 不进 Git；`dvc remote add -d storage s3://...`（支持 S3/GCS/Azure/SSH 等）+ `dvc push/pull` 同步数据。流水线写在 `dvc.yaml`，每个 stage 有 `cmd`/`deps`/`params`/`outs`/`metrics`/`plots`；`dvc repro` 按依赖图重跑变更的 stage。参数从 `params.yaml` 读，`dvc params diff`、`dvc metrics show/diff`、`dvc plots` 对比实验。`dvc exp run` 跑实验、`dvc exp show` 列表对比。可借鉴：data_status / experiment_status 字段直接挂 `.dvc`/`dvc.yaml` 的 commit 与 metrics。
- 【链接】https://dvc.org/doc/start ，命令参考 https://dvc.org/doc/command-reference ，pipelines/metrics https://dvc.org/doc/start/data-pipelines/metrics-parameters-plots
- 【已知坑】须与 Git 配合提交 `.dvc`/`dvc.lock`，否则版本错位；remote 存储要单独配置与鉴权；改大文件用 `dvc add` 重新追踪。

## MLflow（实验跟踪 + 模型注册）
- 【是什么】开源 ML 生命周期平台：Tracking / Models / Model Registry / Projects。
- 【可复用方法】Tracking Python API：`mlflow.start_run()`（上下文管理器，可嵌套 run）、`mlflow.log_param/log_params`、`mlflow.log_metric/log_metrics`（metric 可带 step 画曲线）、`mlflow.log_artifact(s)`、`mlflow.set_tag`。`mlflow.<flavor>.autolog()` 自动记录（sklearn/pytorch/xgboost 等）。`mlflow.<flavor>.log_model()` 存模型。Model Registry 管理已注册模型的版本与别名/阶段（旧版 Staging/Production/Archived stage，新版推荐用 alias）。后端有 tracking server + backend store（DB）+ artifact store。可借鉴：method_status/experiment_status 用 run_id 串联，目标期刊指标对应 logged metrics。
- 【链接】https://mlflow.org/docs/latest/ ，Tracking API（历史版） https://mlflow.org/docs/2.9.0/tracking/tracking-api.html ，Model Registry https://mlflow.org/docs/latest/ml/model-registry/
- 【已知坑】stage 体系已被 alias 取代（迁移注意）；自托管要单独跑 tracking server 和 artifact 存储；大量 metric 高频 log 会拖慢。

## Weights & Biases (wandb)
- 【是什么】云端实验跟踪/可视化/Artifacts/Sweeps 平台。
- 【可复用方法】`wandb.init(project=, config=, resume=)` 开 run；`wandb.config` 存超参；`wandb.log({"loss": x}, step=)` 记指标并实时画图；`wandb.log_artifact()` / `run.use_artifact()` 做数据/模型版本与血缘。Sweeps：写 sweep YAML（method=grid/random/bayes + metric + parameters）→ `wandb.sweep()` 建、`wandb.agent()` 跑超参搜索。Public API（`wandb.Api()` → `api.run("entity/project/run_id")`）可程序化拉历史指标。可借鉴：experiment_status 记 run URL + sweep best run。
- 【链接】https://docs.wandb.ai ，创建实验 https://docs.wandb.ai/guides/track/create-an-experiment/ ，Artifacts https://docs.wandb.ai/tutorials/artifacts/ ，Sweeps https://docs.wandb.ai/guides/sweeps/
- 【已知坑】默认上云（敏感数据需自托管/离线 `WANDB_MODE=offline`）；免费版团队/存储有额度；网络差时 log 会阻塞。

## Autoskill / AutoSkill（自动技能获取，研究方向）
- 【是什么】指 LLM agent 自动创建/复用"技能"的研究与工具族。GitHub 上有 ECNU-ICALK/AutoSkill 等仓库；2026 年多篇论文围绕 skill creation + memory + management + evaluation。
- 【可复用方法】共性 pipeline：从过往任务经验中归纳可复用流程→存入 skill/经验库（procedural memory）→新任务检索并复用→用结果评估并更新技能。代表作 MUSE（Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation）给出"创建/记忆/管理/评估"四环。可借鉴：把本技能的 decision_log 与 next_actions 升级成"可复检索的经验条目"，完成任务后回写"哪种做法有效"。
- 【链接】ECNU-ICALK/AutoSkill https://github.com/ECNU-ICALK/AutoSkill ，MUSE 论文 https://huggingface.co/papers/2605.27366
- 【已知坑】具体某个名叫"Autoskill"的产品身份不唯一（npm autoskills、多个同名 repo、学术 AutoSkill），引用时须指明是哪一个；学术实现多为原型。【未能核实】是否存在单一权威"Autoskill"工具。

## Screenpipe (mediar-ai/screenpipe)
- 【是什么】开源、本地优先的 24/7 屏幕+音频录制工具，对标 Microsoft Recall / Rewind，给 AI 提供"看过/听过"的记忆，Rust 编写。
- 【可复用方法】事件驱动捕获→OCR/语音转写→存入本地 SQLite。本地 REST API 默认 `http://localhost:3030`，`/search` 端点按内容检索（区分 OCR 与 audio 内容类型，可按时间/应用窗口过滤），结果 JSON。"pipes"是插件式 AI agent，跑在屏幕数据上。还提供 MCP server 接入 Claude/Cursor/Codex。可借鉴：作为"被动记忆"补充——会话外的工作上下文也能检索，区别于本技能的"主动结构化登记"。
- 【链接】https://docs.screenpi.pe ，API 参考 https://docs.screenpi.pe/cli-reference ，架构 https://docs.screenpi.pe/architecture ，MCP https://docs.screenpi.pe/mcp-server
- 【已知坑】持续录制占磁盘/CPU，隐私敏感（全本地可缓解）；`/search` 具体查询参数名（如 q/content_type/app_name/limit）我在搜索摘要中见到提及但【未能逐字核实参数全集】，调用前应查 localhost:3030 自带文档。

## LangGraph memory / checkpointer
- 【是什么】LangGraph 的状态持久化机制：短期记忆=checkpointer，长期记忆=Store。
- 【可复用方法】Checkpointer（`InMemorySaver`/`MemorySaver`、`SqliteSaver`、`PostgresSaver`/`AsyncPostgresSaver`）在每步保存图状态快照；调用时传 `config={"configurable": {"thread_id": ...}}`，同 thread_id 续接对话、可时间旅行/回放。长期记忆用 `BaseStore`（如 `InMemoryStore`/Postgres store），按 `namespace`(tuple) + key 做 `put`/`get`/`search`，跨 thread 共享，支持语义检索与 TTL。可借鉴：thread_id≈一次会话、Store namespace≈项目，正好映射"会话级 vs 项目级"两层记忆——本技能 db09 即长期 Store 角色。
- 【链接】memory 概念 https://docs.langchain.com/oss/python/langchain/long-term-memory ，TTL https://docs.langchain.com/langsmith/configure-ttl
- 【已知坑】checkpointer 数据随对话增长，生产要选持久后端并清理；语义检索需配 embeddings；状态 schema 变更要兼容旧 checkpoint。

## mem0
- 【是什么】AI agent 记忆层，自动从对话抽取并存储"记忆"，支持检索增强。
- 【可复用方法】Python：`from mem0 import Memory; m = Memory()`；`m.add(messages, user_id=/agent_id=/run_id=, metadata=)` 抽取并存事实（`infer=False` 可存原文不抽取）；`m.search(query, user_id=)` 语义检索相关记忆；`m.get_all(user_id=)`、`update`、`delete`。按 user_id / agent_id / run_id（会话）三种作用域隔离记忆。架构=向量库 + 可选 graph memory（实体关系，配 Neo4j）+ LLM 抽取层。有托管平台与自托管(OSS)，OpenMemory/MCP 提供本地 MCP 服务。可借鉴：user_id 作用域≈用户偏好记忆，run_id≈会话记忆，与本技能 user/feedback/project 文件分层一致。
- 【链接】https://docs.mem0.ai ，API 参考 https://docs.mem0.ai/templates/api_reference_template ，OpenMemory https://openmemory.cavira.app/
- 【已知坑】LLM 抽取会漏/错记，关键事实仍需显式写入（呼应本技能"立即更新纪律"）；graph memory 需额外部署；托管版数据上云。

## Notion
- 【是什么】块结构工作区，可作项目知识库/看板，开放 API。
- 【可复用方法】API 基址 `https://api.notion.com/v1/`，必须带 `Notion-Version` 头（如 `2022-06-28`）和 Bearer integration token。核心：`/pages`（建/读页面，属性按 database schema）、`/databases/{id}/query`（带 filter/sorts/分页 `start_cursor`+`has_more`）、`/blocks/{id}/children`（读写块内容）。新版引入 data_source 概念（一个 database 可多 data source）。限流约 3 请求/秒（均值），超限返回 429 + Retry-After。可借鉴：project_card 字段映射成 Notion database 属性，阶段任务做看板视图。
- 【链接】https://developers.notion.com/ ，内部集成 https://developers.notion.com/guides/get-started/internal-connections
- 【已知坑】3 req/s 限流写批量需退避；集成要显式被分享到对应页面/库才有权限；block 模型嵌套深时分页繁琐。

## Logseq
- 【是什么】隐私优先、开源、本地优先的大纲式(outliner)知识库，支持 Markdown 与 org-mode。
- 【可复用方法】一切皆 block，`[[page]]` 与 `((block-ref))` 双链；journals（每日页）天然做研究日志/进展流水；内置 query（基于 Datalog 风格的图数据库）按属性/标签/任务状态聚合，TODO/DOING/DONE 任务关键字 + `LOGBOOK` 计时。可借鉴：用 journals 当 decision_log 时间线、用 page 当项目卡、用 query 自动汇总未完成 next_actions。
- 【链接】https://logseq.com ，概述 https://en.wikipedia.org/wiki/Logseq
- 【已知坑】outliner 心智模型与普通 Markdown 不同，迁移有成本；查询语言相对小众；大图加载/同步偶有性能与冲突问题。

## Jupyter Book
- 【是什么】把 Markdown/MyST + Jupyter notebook 编译成可发布的书/静态网站与 PDF（executablebooks，现 jupyter-book 组织）。
- 【可复用方法】项目根放 `_config.yml`（站点配置：标题、执行设置、Sphinx/扩展）与 `_toc.yml`（目录结构，format=jb-book/section 等）；内容用 MyST Markdown（支持 cross-reference、admonition、引用 `{cite}` + BibTeX、可执行代码块）。`jupyter-book build .` 生成 `_build/html`。Jupyter Book 2.x 转向以 MyST 引擎为核心。可借鉴：把论文/实验报告做成可执行、带引用、可发布网页的"活文档"，paper_status 之外多一条复现产物。
- 【链接】https://jupyterbook.org ，cookiecutter 模板 https://github.com/executablebooks/cookiecutter-jupyter-book
- 【已知坑】1.x 基于 Sphinx、2.x 基于 MyST 引擎，配置不完全兼容（注意版本）；notebook 执行依赖环境，CI 里要装齐 kernel 与依赖。

---

## 项目归档协议（防 db09 膨胀，与 a07 一致性配合）

db09 只进不出，项目越攒越多会拖慢会话开始时的扫描、稀释"当前在做什么"。完结的项目应**归档**而非删除（历史与 lessons 仍有复用价值）。

【完结判据（满足其一即可归档）】
- 论文/成果**已录用或正式发表**；或竞赛/项目**已验收结题**；或**用户显式声明**"这个项目收了/不做了"。

【归档动作（选"加字段"不"挪目录"——最轻且不破坏既有相对路径与 db09 README 链接）】
1. 在 `project_card.md` 的 yaml 字段块加一行 `archived: YYYY-MM-DD`（绝对日期；可选字段，仅归档项目才有，不影响 CONVENTIONS §3 的 14 必填字段，check_databases 兼容）。可再加 `archive_reason:` 一句（录用/结题/用户声明）。
2. **终版 lessons 回写**：归档时把该项目最值得跨项目复用的 1-3 条过程教训补进 db09 顶层 `lessons.md`（格式见 db09 README），来源 slug 即本项目——这是项目"出库"前的最后一次知识沉淀。
3. 目录原地不动：`projects/<slug>/` 保留全部文件，相对路径/链接不变。

【会话开始时的行为（a02 SKILL「会话开始时」据此）】
- 扫描/罗列项目时**跳过** `archived:` 非空的项目，只在活跃项目里恢复 `current_stage`/`next_actions`；除非用户**点名**该归档项目（"看下之前那个 X 项目"），才读取。
- 归档项目可"复活"：用户要继续做，删掉 `archived` 行即回到活跃集。

【与既有机制的边界】归档只改 project_card 一行 + lessons 回写，**不动** R8.4 的 db09 schema 校验（14 必填字段照常全在）、不动 palette.json/terminology 等配套文件；与 a07 变更广播无关（归档不是材料变更）。
