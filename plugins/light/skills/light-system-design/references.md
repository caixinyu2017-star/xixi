# 后端系统设计 · 工具参考笔记

逐工具核查笔记，配合 SKILL.md 使用。所有要点来自官方文档/仓库，链接可点。研究日期 2026-06；版本/端点随上游演进，落地前以所装版本官方文档为准，标「未能完整核实」者不臆造。

## Supabase RLS（行级安全）

【是什么】Postgres 原生行级安全 + Supabase 的 auth 辅助函数，做多租户/按用户隔离数据。开启后用 publishable key 访问时，没有 policy 的表一律不可见。

【可复用方法 / 真实语法】
- 开启：`alter table t enable row level security;`，强制连表 owner 也走策略：`alter table t force row level security;`
- 策略骨架：
  ```sql
  create policy "name" on t
    for [select|insert|update|delete]
    to [anon|authenticated|service_role]
    using ( <可见性条件> )      -- 控制哪些已有行可读/可改/可删
    with check ( <写入约束> );  -- 控制新行/改后行是否合法（insert/update）
  ```
- 辅助函数：`auth.uid()` 取当前用户 id；`auth.jwt()` 取 JWT。授权信息用 `raw_app_meta_data`（用户改不了），别用 `raw_user_meta_data`（用户可改）。
- **区分内置与自定义**：`auth.uid()`/`auth.jwt()` 是 Supabase **内置**函数；`auth.tenant_id()` 之类**不是内置**，必须自行定义（从 `auth.jwt()->'app_metadata'` 取，或用会话变量 `current_setting('app.tenant_id', true)`）。多租户模板 `templates/rls_policy.sql` 顶部给了两种可移植实现。
- 三个内置角色：`anon`（未登录）、`authenticated`（已登录）、`service_role`（服务端、绕过 RLS）。
- 性能五条（官方 benchmark 显著）：
  1. 把函数包进 select 触发 initPlan 缓存：`using ((select auth.uid()) = user_id)`（179ms→9ms）。
  2. 给 policy 引用的列建索引（171ms→<0.1ms）。
  3. 永远写 `to` 子句，避免对无关角色求值。
  4. 客户端仍显式带 `.eq('user_id', ...)` 过滤，帮优化器选更好计划。
  5. 避免在 policy 里 join，改成子查询 `IN`/`ANY`（9000ms→20ms）；复杂跨表查询用 `security definer` 函数（放在非暴露 schema）。

【链接】
- https://www.supabase.com/docs/guides/database/postgres/row-level-security
- https://supabase.com/blog/postgres-best-practices-for-ai-agents

【已知坑】未授权时 `auth.uid()` 返回 null，需 `auth.uid() is not null and auth.uid()=user_id`；security definer 函数绝不能放在暴露 schema。

## supabase-postgres-best-practices（Postgres 通用最佳实践）

【是什么】Supabase 沉淀的 Postgres 实操规则，按 Critical→Low 排序。

【可复用方法】
- 安全：多租户表一律开 RLS + 显式 policy；别只靠应用层 WHERE，"一个 bug 或绕过就全量泄露"。
- 索引：**外键必须建索引**（最常见漏建）；生产建索引用 `CREATE INDEX CONCURRENTLY` 避免锁表；别为写性能加无收益索引。
- 查询：警惕 ORM 隐藏的全表扫描；上线前用 `EXPLAIN ANALYZE` 验证计划。
- 迁移：生产不跑锁表迁移；改类型仍可能锁表，加默认值列在现代 PG 已不锁。
- 连接：必须用连接池，"连接池耗尽"是高频故障。
- 数据类型：刻意选型，别无脑 `text`/超大 numeric；按访问模式做规范化。
- 分页：大数据集用游标/keyset 分页，别用大 OFFSET。

【链接】https://supabase.com/blog/postgres-best-practices-for-ai-agents

【已知坑】机器可读规则面向 agent，落地仍需结合具体 schema 判断取舍。

## PostgreSQL 索引类型

【是什么】PG 六种索引，按查询模式选型。

【可复用方法 / 选型表】
| 场景 | 索引 | 说明 |
|------|------|------|
| 通用等值/范围/排序 | **B-Tree**(默认) | `< <= = >= >`、`BETWEEN/IN/IS NULL`；支持 `col LIKE 'foo%'` 前缀匹配（C locale） |
| 仅等值，无范围 | **Hash** | 只 `=`；UUID/token 精确查 |
| 几何/全文/范围类型/最近邻 | **GiST** | `@> <@ && <->`；`ORDER BY location <-> point LIMIT 10` |
| 四叉树/基数树类数据 | **SP-GiST** | 电话前缀、IP 段、点空间分区 |
| 数组/JSONB/全文/trigram | **GIN** | `@> <@ &&`；`tags @> ARRAY['x']`、pg_trgm |
| 超大表+物理有序列 | **BRIN** | 时序/日志按时间追加写入，索引极小（存块区间 min/max） |

【链接】https://www.postgresql.org/docs/18/indexes-types.html

【已知坑】GIN 写入慢、体积大；BRIN 只在物理顺序与列值相关时有效（如 append-only 时间戳）。

## FastAPI

【是什么】Python 异步 Web 框架，类型驱动校验 + 自动 OpenAPI 文档。

【可复用方法】
- 路由：`@app.get("/items/{item_id}")`，路径/查询参数由类型注解自动校验。
- 请求/响应模型用 Pydantic `BaseModel`；用 `response_model=ItemOut` 控制输出 schema（隐藏内部字段）。
- 依赖注入 `Depends(...)`；`yield` 依赖可做 DB session 的 setup/teardown；支持全局/路由级依赖。
- 状态码：`status_code=status.HTTP_201_CREATED`。
- 安全：`OAuth2PasswordBearer(tokenUrl="token")` + `Depends` 取 token，配 JWT。
- 自动文档：Swagger UI 在 `/docs`，机器可读规范在 `/openapi.json`。
- 安装运行：`pip install "fastapi[standard]"`，开发 `fastapi dev`（自动重载，127.0.0.1:8000）。

【链接】https://fastapi.tiangolo.com/tutorial/

【已知坑】同步 `def` 端点在线程池跑，CPU 密集会阻塞；`response_model` 与返回类型不一致会触发校验/序列化错误。

## Prisma（ORM + Migrate）

【是什么】Node/TS 的 schema-first ORM，`schema.prisma` 单一数据源。

【可复用方法】
- **`migrate dev`** 仅开发用：用 shadow DB 检测 drift、生成并应用迁移、生成 Client，冲突会提示 reset。
- **`migrate deploy`** 用于生产/CI：只应用待执行迁移，不检测 drift、不 reset、不用 shadow DB。
- `--create-only` 生成迁移但不执行，便于手改 SQL（重命名、触发器、存储过程）。
- `migrate reset` 仅开发：drop+重建+全迁移+seed。
- 生产命令用 advisory lock（10s 超时）防并发；5.3.0+ 可用 `PRISMA_SCHEMA_DISABLE_ADVISORY_LOCK` 关闭。

【链接】https://www.prisma.io/docs/orm/prisma-migrate/workflows/development-and-production

【已知坑】**生产绝不能跑 `migrate dev`**（会 reset）；`migrate deploy` 对"历史里缺失的已应用迁移"不告警，需自查。

## SQLAlchemy 2.0

【是什么】Python 事实标准 ORM/Core，2.0 用类型注解声明模型。

【可复用方法】
- 模型：继承 `DeclarativeBase`，`Mapped[int] = mapped_column(primary_key=True)`；`Optional[]` 决定 nullable。
- 关系：`relationship(back_populates=...)`，双向都写 back_populates；`cascade="all, delete-orphan"`。
- 查询：`select(User).where(...).join(...)`，多个 `.where()` 自动 AND；`session.scalars(stmt)` 返回 ORM 对象。
- Session 用 context manager：`with Session(engine) as s: ...; s.commit()`；`get/add_all/delete/flush`。
- 引擎 `create_engine(url)` 自带连接池。
- **防 N+1**：默认 lazy load 逐行 SELECT；用 `selectinload`（二次 IN 查询）或 `joinedload`（JOIN）预加载。

【链接】https://docs.sqlalchemy.org/en/20/orm/quickstart.html

【已知坑】遍历关系集合默认触发 N+1，必须显式 eager load；`joinedload` 对一对多会放大行数，集合优先用 `selectinload`。

## Django REST Framework (DRF)

【是什么】Django 之上的 REST 框架，serializer + viewset + router 三件套。

【可复用方法】
- Serializer：`ModelSerializer` / `HyperlinkedModelSerializer`，`Meta` 指定 model 与 fields。
- ViewSet：`ModelViewSet` 自带 list/create/retrieve/update/destroy；需要细控时降级到 generic views（`ListCreateAPIView` 等）。
- Router：`DefaultRouter().register(r"users", UserViewSet)` 自动生成 URL。
- 权限：`IsAuthenticated`/`AllowAny`/`IsAdminUser`/`IsAuthenticatedOrReadOnly`；自定义重写 `has_permission`/`has_object_permission`。
- 认证：`SessionAuthentication`、`TokenAuthentication`（`rest_framework.authtoken`）、JWT（`djangorestframework-simplejwt`）。
- 分页：settings 里设 `DEFAULT_PAGINATION_CLASS`（`PageNumberPagination`/`LimitOffsetPagination`/`CursorPagination`）+ `PAGE_SIZE`。
- 限流：`AnonRateThrottle`/`UserRateThrottle` + `DEFAULT_THROTTLE_RATES`（如 `"100/day"`）。

【链接】https://www.django-rest-framework.org/tutorial/quickstart/

【已知坑】ViewSet 默认 queryset 易触发 N+1，用 `select_related`/`prefetch_related`；分页大数据集优先 `CursorPagination`。

## Spring Boot（REST）

【是什么】Java 主流后端框架，注解驱动 + 自动配置 + 分层架构。

【可复用方法】
- `@SpringBootApplication` = `@Configuration`+`@EnableAutoConfiguration`+`@ComponentScan`。
- `@RestController`(= `@Controller`+`@ResponseBody`) + `@GetMapping`/`@PostMapping`（派生自 `@RequestMapping`）；`@RequestParam(defaultValue=...)`。
- 分层：`@RestController`(接口层) → `@Service`(业务层) → `@Repository`/Spring Data JPA `JpaRepository<T,ID>`(数据层)；构造器注入依赖。
- 实体 `@Entity`；Jackson 自动 JSON 序列化（web starter 自带）。
- 配置：`application.properties` / `application.yml`，多环境用 profiles（`application-prod.yml`）。
- 构建运行：`./mvnw clean package` / `./gradlew build` 出可执行 jar，`java -jar` 启动。

【链接】
- https://spring.io/guides/gs/rest-service
- https://spring.io/guides/gs/accessing-data-jpa

【已知坑】组件需在主类所在包及子包内才被 `@ComponentScan` 扫到；JPA 默认 lazy fetch 在 session 外访问会 LazyInitializationException。

## Redis（缓存）

【是什么】内存数据结构存储，常用作缓存层/会话/排行榜/pub-sub。

【可复用方法】
- Cache-aside（旁路缓存）：读→查缓存命中即返回→未命中读 DB→写回 Redis 带 TTL→返回；写时更新 DB 后失效或更新缓存。
- 内存上限：`maxmemory 100mb`（运行时 `CONFIG SET maxmemory`）。
- 淘汰策略 `maxmemory-policy`：
  - 合法值仅 8 个：`noeviction`/`allkeys-lru`/`allkeys-lfu`/`allkeys-random`/`volatile-lru`/`volatile-lfu`/`volatile-random`/`volatile-ttl`。`allkeys-lru` 最佳默认（热点访问呈幂律）；`allkeys-lfu` 频率比近因更重要时；`allkeys-random` 访问均匀；`volatile-ttl` 优先淘汰快过期的；`volatile-*` 在无 TTL 键时退化成 `noeviction`。
  - 注：不存在按"最后修改时间"淘汰的策略（如 lrm），只有上述 LRU/LFU 的近似实现；勿凭印象添加不存在的值。
  - 持久化/复制实例留内存余量给 AOF/复制缓冲（查 `INFO memory` 的 `mem_not_counted_for_evict`）。
- 近似 LRU：采样而非全量，`maxmemory-samples 5`（调到 10 更准、略耗 CPU）；LFU 调 `lfu-log-factor`/`lfu-decay-time`。
- 监控：命中率 `keyspace_hits/(hits+misses)`；`evicted_keys` 高说明策略不对。

【链接】
- https://redis.io/docs/latest/develop/use-cases/cache-aside/
- https://redis.io/docs/latest/develop/reference/eviction/

【已知坑】`volatile-*` 策略若没键带 TTL 等于不淘汰会写报错；缓存与 DB 一致性需靠失效策略，注意缓存穿透/雪崩（空值缓存 + TTL 加随机抖动）。

## Docker（镜像最佳实践）

【是什么】容器镜像构建，目标小、快、安全、可复现。

【可复用方法】
- **多阶段构建**：build 阶段带编译工具，最终阶段只拷产物，镜像小、攻击面小。
- **层缓存**：先 COPY 依赖清单（package.json/requirements.txt/go.mod）再装依赖，最后才 COPY 源码——源码改动不破坏依赖层缓存。临时文件用 `RUN --mount=type=bind` 而非 COPY。
- `.dockerignore` 排除 .git/node_modules/测试/文档。
- **非 root 运行**：`groupadd -r app && useradd -r -g app app; USER app`。
- 小基础镜像（slim/alpine/distroless）；优先官方/认证发行镜像。
- 钉版本：base 镜像钉 digest（`FROM alpine:3.21@sha256:...`），apt 包钉版本。
- 合并 RUN 减层：`apt-get update && apt-get install -y --no-install-recommends ... && rm -rf /var/lib/apt/lists/*`。
- `HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/health || exit 1`。
- `ENTRYPOINT` 放主命令、`CMD` 放默认参数；`WORKDIR` 用绝对路径；优先 `COPY` 而非 `ADD`。
- 仅 build 阶段需要的文件用 `RUN --mount=type=bind,source=requirements.txt,target=/tmp/req.txt pip install -r /tmp/req.txt`，不进最终镜像；多命令也可用 heredoc `RUN <<EOF ... EOF`。
- ENTRYPOINT 用 helper 脚本时以 `exec "$@"` 收尾，让主进程成 PID 1 正确收信号；管道命令前加 `set -o pipefail &&` 捕获上游失败。
- `ADD` 仅在拉远程产物且带校验时用：`ADD --checksum=sha256:... https://... /file`。

【链接】https://docs.docker.com/build/building/best-practices/

【已知坑】tag 可变（publisher 可改指向），生产钉 digest；`apt-get update` 必须和 install 同一 RUN 否则吃旧缓存。

## Kubernetes

【是什么】容器编排，声明式管理 Pod/Deployment/Service 等。

【可复用方法】
- **Deployment**：`replicas`、`selector.matchLabels`(创建后不可改)、`strategy.rollingUpdate.maxUnavailable/maxSurge`、`revisionHistoryLimit`；只有改 `.spec.template` 才触发滚动，scale 不触发。
- **Service**：`ClusterIP`(默认内部)/`NodePort`(30000-32767)/`LoadBalancer`(云 LB)/`ExternalName`(CNAME)；`port`→`targetPort`。
- **探针**：`livenessProbe`(失败重启)/`readinessProbe`(失败摘除流量)/`startupProbe`(慢启动期间禁用前两者)；支持 httpGet/tcpSocket/exec/grpc。
- **资源**：`requests`(调度保障下限)/`limits`(超内存 OOM kill、超 CPU 节流)。
- **配置**：`ConfigMap`(非敏感)、`Secret`(base64，Opaque/tls/dockerconfigjson)，经 env 或 volume 注入。
- **Ingress**：`ingressClassName`、host/path 路由、`tls.secretName`；需 Ingress Controller。
- **HPA**(autoscaling/v2)：`scaleTargetRef` + `minReplicas/maxReplicas` + CPU `averageUtilization: 70`；需 metrics-server。
- 运维：`kubectl rollout status/history/undo --to-revision`、`kubectl scale`、`rollout pause/resume`。
- **健康判定**：`progressDeadlineSeconds`（默认 600，超时报 `ProgressDeadlineExceeded`）；`minReadySeconds`（新 Pod 须无崩溃就绪满 N 秒才算 available）；`revisionHistoryLimit` 默认 10。

【链接】https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

【已知坑】Secret 只是 base64 非加密，需配 RBAC/加密 at rest；漏配 readinessProbe 会把流量打到没就绪的 Pod；limits 设太低会被频繁 OOM/节流。

## OpenAPI / Swagger（3.x）

【是什么】API 契约规范，YAML/JSON 描述端点，可生成文档/客户端/Mock。

【可复用方法 / 顶层结构】
- `openapi`(必填,如 `3.1.0`；模板 `templates/openapi.yaml` 即用此版本)、`info`(title/version 必填, description 选填)、`servers`(完整 base URL，替代 2.0 的 host/basePath/schemes)。
- `paths`：每路径下 get/post/... 含 `summary`/`parameters`(path/query/header/cookie)/`requestBody`/`responses`(至少一个状态码+description+content schema)。
- `components`：复用 `schemas`/`securitySchemes`/`parameters`/`responses` 等，用 `$ref: '#/components/schemas/User'` 引用保持 DRY。
- `securitySchemes` 支持 apiKey/oauth2/http bearer/openIdConnect/basic；`security` 可全局或按操作应用。
- 关键字大小写敏感；YAML/JSON 等价可互换。

【3.1 vs 3.0 关键差异（写模板/选版本必看）】
- **nullable 关键字**：3.0 用 `type: string, nullable: true`；**3.1 移除了 `nullable`**，改用 JSON Schema 的类型数组 `type: [string, "null"]`。版本声明写 3.1.x 却仍写 `nullable: true` 是常见 bug（被忽略或报错）。
- **JSON Schema 对齐**：3.1 的 Schema Object 与 JSON Schema 2020-12 完全兼容（`examples` 用数组、`$ref` 旁可并列其他关键字、支持 `const`/`if-then-else` 等）；3.0 是 JSON Schema 的子集。
- **顶层版本号**：选好一个版本贯穿全文档与工具链，别 3.1 与 3.0 语法混用。本笔记与模板统一用 `3.1.0`。

【链接】https://swagger.io/docs/specification/v3_0/basic-structure/

【已知坑】FastAPI/DRF/Spring 可自动产出 OpenAPI，手写时易漏 error 响应码与示例；版本化建议放在 `servers` URL（/v1）或路径前缀。

## Alembic（SQLAlchemy 迁移）

【是什么】SQLAlchemy 官方迁移工具，支持 autogenerate diff。

【可复用方法】
- `alembic init` 生成 `alembic.ini`、`versions/`、`env.py`。
- 在 `env.py` 设 `target_metadata = Base.metadata`（多个用 list，表 key 须唯一），否则 autogenerate 出空 diff。
- 生成：`alembic revision --autogenerate -m "msg"`，比对 DB 与 metadata 产出 `upgrade()`/`downgrade()`（含 `revision`/`down_revision`，用 `op.*`）。
- 应用：`alembic upgrade head`；回退：`alembic downgrade -1`。
- CI 校验：`alembic check`(1.9.0+) 若有未生成的变更则报错。
- autogenerate **能测**：增删表/列、nullable 变更、基本索引/唯一约束/外键变更；默认比类型(1.12.0+ `compare_type`)。
- **检不出**：表/列重命名(报成 drop+add，需手改)、匿名约束、部分 CHECK/EXCLUDE/PK、Sequence。

【链接】https://alembic.sqlalchemy.org/en/latest/autogenerate.html

【已知坑】autogenerate"不保证完美"，每次必须人工审；用 `include_object`/`include_name` 防止误删不在 metadata 里的表。

## Nginx（反向代理）

【是什么】高性能 Web 服务器/反向代理/负载均衡/TLS 终止。

【可复用方法】
- 反代：`location /path/ { proxy_pass http://localhost:8000; }`；地址带 URI 会替换匹配段。
- 透传客户端信息（关键）：
  ```nginx
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  ```
- 负载均衡：`upstream backend { server a:8080; server b:8080; }` + `proxy_pass http://backend;`。
- TLS：`listen 443 ssl; ssl_certificate ...; ssl_certificate_key ...;`。
- 静态文件：`location /static/ { root /var/www; expires 30d; }`。
- gzip：`gzip on; gzip_types application/json text/css application/javascript;`。
- 限流：`limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;` + `limit_req zone=api burst=20 nodelay;`。
- `worker_processes auto;` 匹配核数；缓冲 `proxy_buffering`(默认开，低延迟流式可关)。
- 其他协议：`fastcgi_pass`(PHP-FPM)、`uwsgi_pass`(Python uWSGI)。

【链接】https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/

【已知坑】默认只改 Host/Connection 头，不透传真实 IP 需手动 set_header；改配置后 `nginx -t` 校验再 `nginx -s reload`。

## GitHub Actions（CI）

【是什么】GitHub 内置的工作流引擎，每次 push/PR 自动跑 lint/test/迁移校验。面向科研：把"代码能跑、迁移没漏生成"固化成可复现的绿勾，而非搭企业级发布流水线。

【可复用方法 / 真实结构】
- 文件放 `.github/workflows/*.yml`，三件套：
  - `on`：触发事件——`push`（推送）、`pull_request`（PR，含 fork）、`workflow_dispatch`（Actions 页手动触发）。
  - `jobs.<id>.runs-on`：跑在哪个 runner，如 `ubuntu-latest`。
  - `steps`：依次执行，`uses:` 调 action、`run:` 跑命令。
- 关键 action（版本真相源见 light-backend-coding a03 references.md「版本实测」段，2026-06 均为 v6）：`actions/checkout@v6` 拉代码；`actions/setup-python@v6`（或 `setup-node`）装运行时，配 `cache: pip`/`npm` 复用依赖缓存提速。
- 闭合 SKILL 迁移铁律的最小 job 骨架：
  ```yaml
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v6
        - uses: actions/setup-python@v6
          with: { python-version: "3.12", cache: pip }
        - run: pip install -r requirements.txt
        - run: ruff check .        # lint
        - run: pytest -q           # test
        - run: alembic check       # 迁移有没漏生成（Prisma 换 migrate deploy 对临时库）
  ```
- 最小权限：顶层 `permissions: { contents: read }` 把默认 token 收成只读，需要写（如发 release）才按 job 放宽。
- secrets：`${{ secrets.NAME }}` 读仓库/环境密钥，绝不硬编码；**fork 发起的 `pull_request` 默认拿不到 secrets**（防恶意 PR 偷密钥），需密钥的集成测试要么跳过要么用 `pull_request_target`（谨慎）。

【链接】
- https://docs.github.com/actions/writing-workflows/workflow-syntax-for-github-actions
- https://docs.github.com/actions/security-guides/security-hardening-for-github-actions

【已知坑 / 进阶（科研一般不展开）】第三方 action 钉 commit SHA 而非 tag（防供应链投毒，官方 `actions/*` 用版本 tag 可接受）；多版本测试用 `strategy.matrix`；build-push 镜像到仓库 / 部署 K8s、`environments` 配审批与回滚、OIDC 免密换云凭证（不存长期 secret）——这些属发布/部署链，按需再加，别让 CI 一上来就背全套 DevOps。

## pgvector + HNSW（向量检索选型，科研 RAG / 语义检索常用）

【是什么】pgvector 是 PostgreSQL 的向量扩展，让"已有 Postgres"直接存 embedding 做相似检索，省去单独引入向量数据库。科研系统里做语义检索、RAG、近重复去重时，数据量不大（百万级以内）优先 pgvector——一套库管关系数据 + 向量，运维与事务一致性都简单。

【可复用方法 / 真实语法】
- 建扩展与列：`CREATE EXTENSION vector;` → 列 `embedding vector(768)`（维度写死，与模型输出对齐）。
- 距离算子：`<->` L2、`<=>` 余弦距离、`<#>` 负内积；查询 `ORDER BY embedding <=> $1 LIMIT 10`。
- **HNSW 索引（首选，查询快、召回高）**：`CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);` 算子类要与查询距离一致（cosine→`vector_cosine_ops`）。建参 `m`（每节点连接数，默认 16）/`ef_construction`（建图候选数，默认 64，调高更准更慢建）；查询期 `SET hnsw.ef_search = 40;` 调召回/延迟。
- **IVFFlat 替代**：`USING ivfflat (...) WITH (lists=N)`，建索引快、占内存小，但召回通常不如 HNSW，且必须在有代表性数据后再建（lists≈行数/1000）。

【链接】https://github.com/pgvector/pgvector

【选型对照 / 已知坑】HNSW 召回好、查询快但**建索引慢、占内存大**；IVFFlat 反之且需先有数据才能建。何时该上专用向量库（Milvus/Qdrant/Weaviate）：向量量级到千万~亿、需分布式水平扩展、需要高 QPS 或丰富的过滤+混合检索时——pgvector 在亿级与高并发下吃力。HNSW 索引不支持精确，`ef_search` 太小会漏召回；维度过高（>2000）pgvector 有上限，需降维。

## OpenTelemetry（可观测，科研 AI 服务的 trace/metric/log 统一）

【是什么】厂商中立的可观测性标准 + SDK，统一采集三类信号：**traces**（一次请求跨服务的调用链）、**metrics**（计数/直方图等数值）、**logs**。科研 AI 系统里用于看清"一次推理请求耗时花在哪、哪步报错、GPU/队列指标"，避免 print 调试。

【可复用方法 / 真实用法（Python）】
- 自动埋点最省力：`pip install opentelemetry-distro opentelemetry-exporter-otlp` → `opentelemetry-bootstrap -a install`（按已装库装对应 instrumentation，如 FastAPI/requests/SQLAlchemy）→ `opentelemetry-instrument python app.py` 零改代码出 trace。
- 手动埋点：`from opentelemetry import trace; tracer = trace.get_tracer(__name__)`；`with tracer.start_as_current_span("inference"): ...` 包住关键段，`span.set_attribute("model.name", m)`。
- 导出：OTLP 协议（`OTEL_EXPORTER_OTLP_ENDPOINT`）发到 Collector，再转 Jaeger/Tempo（trace）、Prometheus（metric）、Loki（log）等后端；`OTEL_SERVICE_NAME` 标服务名。
- 关联：trace_id 注入日志即可把 log 与调用链对齐，定位"哪次请求的哪一步"。

【链接】https://opentelemetry.io/docs/languages/python/

【已知坑】采样率默认全采，高 QPS 下开销大，生产按比例采样（`OTEL_TRACES_SAMPLER`）；instrumentation 包与被测库版本要匹配，不匹配静默不出 span；metrics/logs 的 SDK 比 traces 成熟度略低，认版本；别把敏感数据（密钥/PII）写进 span attribute（会进可观测后端）。
