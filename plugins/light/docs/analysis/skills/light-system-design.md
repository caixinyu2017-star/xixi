# light-system-design — 深度分析与同类对标

> 源：[`skills/light-system-design/SKILL.md`](../../../skills/light-system-design/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：面向科研/软著/竞赛场景的后端系统与数据库设计技能,把架构、ER、表结构、OpenAPI、权限安全、部署的工程决策固化成"可落地+可写文档"的设计产物,主打 Postgres/FastAPI 技术栈与经核查的工具笔记。

## 核心运行逻辑
SKILL.md 作为决策主线(架构分层→DB设计→接口→安全运维→产出),把每个环节的关键工程取舍写成带"刻意选型"导向的清单(索引按查询模式选、外键必建索引、游标分页优于OFFSET、生产 migrate deploy 不 reset 等)。真正的能力沉淀在 references.md:14 个工具的逐条核查笔记,每条含"是什么/真实语法/链接/已知坑",并标注研究日期 2026-06 与版本,带官方 benchmark 数字(RLS 179ms→9ms)。配 1 个离线脚本(YAML/JSON schema→Mermaid ER)和 4 个起手模板(schema.sql/openapi.yaml/rls_policy.sql/ci.yml),设计上要求产物既能交 a03 实现又能喂 m15 软著功能说明。整体偏 Postgres/Supabase + Python(FastAPI/SQLAlchemy/Alembic)栈。

## 关键步骤
- 1. 系统架构:分层(接口/业务/数据)+职责边界+数据流转;技术选型按 a09,框架起手式查 references(FastAPI/DRF/Spring Boot);向量检索 pgvector vs 专用库选型;OpenTelemetry 可观测
- 2. 数据库设计:用 scripts/er_diagram.py 产 Mermaid ER;表结构按范式/反范式刻意选型;索引按查询模式(B-Tree/GIN/BRIN/GiST/Hash)且外键必建索引;迁移 Alembic/Prisma 人工审;ORM 防 N+1
- 3. 接口设计:RESTful/OpenAPI 3.x,资源命名+状态码+版本化(/v1);schema 放 components 用 $ref 复用;错误码体系+游标分页;从 openapi.yaml 模板起手
- 4. 安全与运维:认证(JWT)+授权(RBAC)最小权限;多租户用 RLS(rls_policy.sql)而非只靠应用层 WHERE;Redis cache-aside;分级日志/统一异常;Docker 多阶段+K8s 三探针+Nginx 反代+CI(ci.yml);无鉴权暴露服务主动告警
- 5. 产出:架构图+ER+DDL+OpenAPI+权限安全部署说明,设计文档喂 m15 软著
- 6. 衔接:设计→a03 实现→a06 规整→与论文/软著一致(a07)→版本入 db09

## 自带资产
- scripts/er_diagram.py — 把 YAML/JSON 表结构定义离线转 Mermaid erDiagram 文本;无 PyYAML 自动回退 JSON;含 6 种基数映射、PK/FK/UK 标记、_sanitize 清洗、带断言的 _selftest(覆盖 JSON/YAML/错误输入路径)
- references.md — 14 个工具的逐条核查笔记(Supabase RLS、PG 索引、FastAPI、Prisma、SQLAlchemy、DRF、Spring Boot、Redis、Docker、K8s、OpenAPI、Alembic、Nginx、GitHub Actions、pgvector+HNSW、OpenTelemetry),每条带真实语法/官方链接/已知坑
- templates/schema.sql — PG 建表骨架,演示 identity vs uuid 主键、审计列、CHECK 约束、外键必建索引、CONCURRENTLY 注释
- templates/openapi.yaml — OpenAPI 3.1 最小骨架,游标分页、$ref 复用、bearerAuth、统一 Error 响应体
- templates/rls_policy.sql — 多租户 RLS 骨架,按操作分 policy、initPlan 缓存写法、引用列建索引、security definer 注意
- templates/ci.yml — GitHub Actions 轻量 CI,最小权限 contents:read、lint/test/alembic check 三步,pin checkout@v6/setup-python@v6

## 优点
- references.md 质量真实可信:不是标题堆砌,而是带真实语法、官方文档链接、可量化的官方 benchmark(RLS 五条性能 179ms→9ms、join→子查询 9000ms→20ms)和'已知坑',且标注研究日期与版本、明确写'落地前以所装版本为准/未能完整核实者不臆造',诚实可核查
- er_diagram.py 工程化扎实:纯离线无硬依赖、PyYAML 缺失优雅回退 JSON、输入名做 _sanitize、错误输入抛 ValueError 而非崩、自带覆盖 JSON/YAML/错误三条路径的 selftest,可直接 --selftest 验证
- 模板不是空壳:schema.sql 把'外键必建索引/identity vs uuid/CONCURRENTLY 不能在事务内'等真坑写进注释,rls_policy.sql 把 references 的性能五条直接落进可跑 SQL,模板与 references 双向呼应
- 强安全意识贯穿:RLS 优于应用层 WHERE、最小权限、密钥不入库、fork PR 拿不到 secrets、Secret 只是 base64 需配 RBAC、网络暴露无鉴权主动告警,符合 security_awareness
- 科研定位精准而非通用企业模板:专门给了 pgvector+HNSW(科研 RAG/语义检索)选型对照和 OpenTelemetry(看清一次推理耗时花在哪)两节,且明确 CI 是'科研可复现绿勾'而非全套 DevOps
- 选型给判据而非结论:索引六型给场景对照表、向量库给'何时该上 Milvus'的量级阈值、Redis 八种淘汰策略逐一说明适用并警告'勿凭印象加不存在的值',引导刻意选型

## 缺点 / 可被质疑处
- rls_policy.sql 与 references 自相矛盾且依赖未定义函数:模板通篇用 auth.tenant_id(),但 references 的 Supabase RLS 节只讲 auth.uid(),auth.tenant_id() 在任何地方都没定义、也非 Supabase 内置,非 Supabase 用户根本没有 auth schema。模板既不可移植也没说明这个函数怎么来,直接跑会报错
- schema.sql 与 rls_policy.sql 不能组合成单一真相源:schema.sql 的 app_user 没有任何 auth/JWT 集成,rls_policy 却假设有 auth.tenant_id();且 er_diagram.py 只吃手写 YAML,无法从 schema.sql 或 SQLAlchemy 模型反推 ER——表结构存在两份独立来源,改一处另一处不同步
- 产出声明'架构图'但只提供 ER 脚本:架构图/数据流转图/模块划分图全靠手画,没有 flowchart/C4 之类的架构图生成脚本,而架构图恰是软著和论文系统描述最需要的
- 栈覆盖偏窄:深度绑定 Postgres+Python,无 SQLite(科研原型最常用)、无 MongoDB/时序库选型;接口侧虽提 DRF/Spring Boot 但只有 FastAPI 风味的 openapi.yaml,没有非 Python 栈的具体骨架文件;无 Node/Express、Go 等
- 缺端到端 example:无 examples/ 目录,没有一个从需求→ER→DDL→API→部署的完整科研系统走查;SKILL 反复声称'喂 m15 软著功能说明'但没给任何'设计→软著功能说明'的映射模板或样例,衔接承诺无落地凭证
- 部署段(SKILL.md 第41行)信息密度过高、可执行性差:Docker+K8s+Nginx+CI 全挤进一个超长 bullet,像压缩的检查清单而非可操作指引;且 references 重墨写 Docker/K8s,templates 里却没有 Dockerfile 和 k8s manifest 模板,重知识轻可复制产物
- 版本/规范有细节漂移:references OpenAPI 节示例用 3.0.4,openapi.yaml 模板却是 3.1.0,二者 nullable/JSON Schema 语义不同却未说明差异;er_diagram.py 对关系里出现但未定义的实体静默渲染空块,会掩盖实体名拼写错误

## 可优化点（供后续逐技能优化）
- 修 rls_policy.sql:要么补一段定义 auth.tenant_id()(或改用可移植的 current_setting('app.tenant_id', true) 会话变量方案),并明确标注'此函数来自 Supabase / 需自行实现',让非 Supabase 用户能跑通;同时让它与 schema.sql 的列名严格对齐
- 给 er_diagram.py 加 DDL/ORM 入口:支持解析 schema.sql 或 SQLAlchemy/Django 模型生成 ER,消除'手写 YAML 与 DDL 两份真相源'的不同步;并对'关系引用了 entities 里没有的实体'报警而非静默建空块
- 补一个架构/数据流图生成脚本:用 Mermaid flowchart 或 C4 文本,从分层/模块定义产架构图与数据流转图,补齐 SKILL 已声明但缺失的'架构图'产出
- 新增 examples/:放一个完整科研系统走查(可复用 dairygoat 行为识别这类真实项目)从需求→ER→DDL→OpenAPI→RLS→部署,并附一份'设计文档→m15 软著功能说明'的映射样例,兑现衔接承诺
- 把部署段拆成可操作清单或补 Dockerfile/k8s-deployment.yaml/nginx.conf 模板:references 已有充足知识,落成可改字段的模板即可,降低从知识到产物的落差
- 补轻量栈选型:加 SQLite(单文件/原型/嵌入式)、MongoDB(文档/非结构化)的适用判据,标明何时科研项目根本不需要 Postgres+K8s 这套重组合,避免过度工程
- 统一 OpenAPI 版本:references 与 openapi.yaml 都用同一版本(建议统一到 3.1.0),并在 references 加一节 3.1 vs 3.0 的关键差异(nullable 写法、与 JSON Schema 对齐),避免照搬出错
- 补一个 JWT 认证流(签发→校验→刷新)的最小骨架与限流具体配置,这两块 SKILL 反复提及却无可复制产物

## 与其他 Light 技能/知识库的衔接
技术选型上游依赖 a09(light-tool-selection);设计产物下游交 a03(light-backend-coding)实现,且 ci.yml/references 显式把 GitHub Actions 的 action 版本真相源 deferred 给 a03 的 references「版本实测」段,二者强耦合;实现后交 a06(light-project-structure)规整目录;设计文档喂 m15(light-ip-application)软著功能说明、并与论文系统描述(m07/light-paper-drafting)保持一致;一致性由 a07(light-consistency)守、版本记录入 db09(light-memory-pm)。注意衔接多为单向声明,目前缺少把设计产物真正转成软著/论文章节的桥接模板。

---

## GitHub 同类前沿技能对标

GitHub 上同类项目几乎都落在两个极端:一端是"工具/编辑器/代码生成器"(chartdb、drawdb、dbml、fastapi-forge、scafoldr、stackrender),把 schema→ER 或 schema→后端代码做成可运行的产品,交互强、可视化好,但它们生成的是"东西"不是"工程决策依据";另一端是 awesome-claude-skills 这类技能聚合清单和 postgres-mcp 这类运行期 agent 工具,前者只索引不沉淀决策,后者强在让 agent 实时连库做性能诊断而非离线设计文档。light-system-design 的独特定位在于它既不是产品也不是清单,而是"把架构/DB/接口/安全/部署的刻意选型写成带核查笔记(日期+版本+官方 benchmark)的可落地设计技能",并显式服务于下游 a03 实现与 m15 软著文档这条科研/软著链路——这种"决策固化 + 经核查工具笔记 + 产出可喂给后续技能"的组合在主流开源里基本没有对应物。它的弱点是没有可视化交互、没有运行期连库能力、模板数量和生态曝光远不及成熟工具。它的强点是工程取舍的显式化、可核查性,以及面向中文科研/软著/竞赛场景的产物导向。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [crystaldba/postgres-mcp](https://github.com/crystaldba/postgres-mcp) | Postgres MCP Pro:给 AI agent 提供 Postgres 读写访问、索引调优建议、EXPLAIN 分析与健康检查的 MCP server,运行期连真实库做性能诊断 | 2893 | 2026-01-22 | 强:运行期连库、真实 EXPLAIN/索引调优、被广泛集成的 MCP 标准接口,工程性能权威性强。弱:它是运行期诊断工具不产出设计文档,不覆盖 ER/OpenAPI/RLS 模板/部署决策的离线设计链路,也不面向软著产物。Light 的索引/RLS 笔记可借鉴它的 benchmark 思路反过来引用它做权威来源 |
| [holistics/dbml](https://github.com/holistics/dbml) | DBML 数据库标记语言:用文本定义和文档化数据库结构,配套 CLI 可在 DBML/SQL 间互转并生成文档 | 3623 | 2026-06-12 | 强:schema-as-code 标准成熟、生态广(dbdiagram.io 背后语言)、双向转换。弱:只管 schema 表达与文档,不含架构分层/接口/安全/部署决策,也无核查笔记。Light 的离线 schema→Mermaid 脚本可借鉴 DBML 做中间表达层以提升互操作 |
| [chartdb/chartdb](https://github.com/chartdb/chartdb) | 开源数据库图编辑器,一条查询导入即可可视化与设计 DB 的 ER 图 | 22380 | 2026-06-04 | 强:可视化交互体验、从现有库一键反向出图、星数高生态活跃。弱:纯 ER 可视化工具,无工程选型决策、无接口/安全/部署、无文档化产物。Light 可借鉴其反向工程(连库导出 ER)能力补足只能正向生成的短板 |
| [drawdb-io/drawdb](https://github.com/drawdb-io/drawdb) | 免费在线数据库图编辑器 + SQL 生成器,画 ER 即可导出建表 SQL | 37359 | 2026-06-11 | 强:零门槛可视化、ER→SQL 导出、星数极高。弱:同为画图工具,不涉及架构/接口/安全/部署的工程取舍,无核查笔记与软著产物。Light 可借鉴其 ER→SQL 的双向同步与导出格式多样性 |
| [mslaursen/fastapi-forge](https://github.com/mslaursen/fastapi-forge) | 基于 UI 的 FastAPI 项目生成工具,定义数据模型后生成 FastAPI+SQLAlchemy+Postgres 工程脚手架 | 168 | 2026-01-24 | 强:技术栈高度重合(FastAPI/SQLAlchemy/Postgres),直接产出可运行后端代码。弱:是代码生成器而非设计决策技能,不解释为什么这样选,也无 RLS/部署/接口契约的工程笔记。Light 的设计产物可作为它的上游输入,二者互补 |
| [scafoldr/scafoldr](https://github.com/scafoldr/scafoldr) | 开源的 v0/Lovable 替代,从需求/schema 生成后端应用代码 | 65 | 2026-02-02 | 强:端到端生成可运行应用、对标商业 AI 建站工具。弱:偏全自动黑盒生成,工程决策不透明、无核查笔记、无软著/科研产物导向。Light 的'刻意选型清单'恰好是它缺的可解释层 |
| [stackrender/stackrender](https://github.com/stackrender/stackrender) | 新一代数据库 schema 设计与生成工具,可视化设计并生成多方言 schema | 242 | 2026-06-10 | 强:较新、可视化 schema 设计 + 多数据库方言生成。弱:聚焦 schema 层,不含接口/安全/部署/架构决策,无核查笔记。Light 可借鉴其多方言输出思路扩展模板 |
| [ahmedkhaleel2004/gitdiagram](https://github.com/ahmedkhaleel2004/gitdiagram) | 把任意 GitHub 仓库 URL 转成交互式系统架构图(hub→diagram) | 15681 | 2026-06-12 | 强:从真实代码逆向出架构图、交互可视化、星数高。弱:只做架构可视化、不做正向工程决策与 DB/接口/安全设计,无文档产物。Light 可借鉴其 LLM 生成 Mermaid/架构图的提示工程做正向架构图输出 |
| [tiangolo/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | 官方全栈模板:FastAPI+SQLModel+PostgreSQL+Docker+GitHub Actions+自动 HTTPS | 43644 | 2026-06-11 | 强:权威官方模板、技术栈高度重合、CI/部署/HTTPS 一应俱全、星数极高。弱:是静态起手模板而非设计决策技能,不解释选型也无 ER/RLS/接口契约的取舍笔记。Light 的 4 个起手模板(schema/openapi/rls/ci)可直接借鉴其 CI 与 Docker 部署最佳实践 |
| [VoltAgent/awesome-claude-skills](https://github.com/VoltAgent/awesome-claude-skills) | 1000+ agent skills 的精选聚合清单,兼容 Claude Code/Codex/Gemini CLI/Cursor 等 | 25158 | 2026-06-12 | 强:生态曝光极高、是 skill 收录与发现的主入口。弱:只是索引清单,不沉淀任何工程决策或可核查内容,无后端/DB 专门深度。Light 这类技能若想被发现可争取被它收录;反过来 Light 的'核查笔记+产物链路'深度是清单类项目无法提供的 |

### Light 该技能可借鉴的点
- 可视化与逆向能力是最大短板:chartdb/drawdb/gitdiagram 都支持'从现有库或代码反向出图',Light 目前只能正向 schema→Mermaid,可考虑加一条连库/读现有 SQL 反向生成 ER 的路径
- 引入 DBML 作为中间表达层:holistics/dbml 是 dbdiagram 背后的事实标准,Light 的 schema→Mermaid 脚本若同时支持 DBML 输入输出,能直接接入成熟生态并提升互操作
- 把 postgres-mcp 当成运行期校验闭环:设计阶段写的'索引按查询模式选、外键必建索引'等决策,可建议用户用 postgres-mcp 的 EXPLAIN/索引调优在真实库上回测,让离线决策有运行期证据
- 借鉴官方 full-stack-fastapi-template 的 CI/Docker/HTTPS 实践充实 ci.yml 与部署模板,尤其是迁移、健康检查、密钥管理这些 Light 部署清单可对齐的细节
- 争取被 VoltAgent/awesome-claude-skills、karanb192/awesome-claude-skills 等聚合清单收录以提升发现度——这是同类技能获取曝光的主要渠道
- 多数据库方言输出:stackrender 支持多方言 schema 生成,Light 模板目前偏 Postgres/Supabase 单栈,可在保持 Postgres 主线的同时为 schema.sql 增加方言适配说明
