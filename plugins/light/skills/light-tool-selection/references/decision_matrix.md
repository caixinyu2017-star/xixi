# 任务 → 工具决策矩阵（带数值阈值）

按需载入。给定一个任务，先量化关键维度（数据规模/输出去向/复现要求/规模），再查表选工具。阈值是经验起点，不是硬性物理边界——临界值附近优先实测。研究日期 2026-06。

## 1. 数据处理：按数据体量选库

| 数据规模 | 内存关系 | 首选 | 备选/理由 |
|---|---|---|---|
| < 100 MB | 远小于内存 | pandas | 生态最全，无需优化 |
| 100 MB – 2 GB | 适配单机内存 | pandas（够用）/ polars（要快） | polars 多核+惰性，2-30x 提速 |
| 2 GB – 50 GB | 接近/超单机内存 | polars (lazy/streaming) / DuckDB | 流式扫描，SQL 直查 parquet |
| 50 GB – 数 TB | 远超单机内存 | DuckDB / polars streaming / dask | DuckDB out-of-core SQL 直查 parquet；polars `streaming=True` 流式；dask 并行 pandas API。（vaex 2023 后停维护，已淘汰，勿新用） |
| > TB 或需集群 | 分布式 | Spark (PySpark) | 集群编排；单机别上 Spark（开销大于收益） |

- 经验法则：**pandas 工作集 ≈ 文件大小的 3-10 倍**（中间副本）。500 MB CSV 可能吃 2-5 GB 内存。
- 文件格式：列存分析用 **Parquet**（压缩+按列读，比 CSV 小 5-10x、快数倍）；交换/可读用 CSV；嵌套用 JSON/JSONL。
- 别为 200 MB 数据上 dask/Spark——调度开销 + 调试难度远超收益。

## 2. 统计与建模：按目标选

| 目标 | 工具 | 阈值/说明 |
|---|---|---|
| 要 p 值/置信区间/假设检验 | statsmodels、scipy.stats、R | 推断统计；样本 n<30 注意正态性假设 |
| 预测精度优先（经典 ML） | scikit-learn | 表格数据 <100 万行单机 OK；GBDT 用 xgboost/lightgbm |
| 深度学习 | PyTorch | 参数量大/GPU 训练 → 上云（见第 6 节） |
| 高级统计绘图/混合模型 | R (lme4/ggplot2) | Python 生态薄弱处 R 更专业 |
| 复用 Light 已验证实现 | code_assets/stats_tests.py、agreement.py | 不重建，直接 import |

## 3. 绘图：按输出去向选格式与工具

| 输出去向 | 格式 | 工具 |
|---|---|---|
| 期刊/会议投稿 | 矢量 PDF/EPS/SVG，300+ dpi | matplotlib(savefig pdf)、Origin、TikZ |
| 网页/演示 | PNG（≥150 dpi）/交互 HTML | matplotlib png、plotly、ECharts |
| 统计快图 | PNG | seaborn |
| 框架/流程图 | 矢量 | TikZ、Graphviz、Mermaid、draw.io |
| 论文级精修 | 矢量 | Illustrator/Inkscape 手工调 |

- 投稿图务必矢量：放大不糊、期刊排版友好。位图最低 300 dpi（线条图 600 dpi）。
- 交互探索用 plotly；最终静态投稿仍回 matplotlib（可控、可复现）。

## 4. 一次性 vs 可复现：决定手工还是脚本

| 重复次数 | 方式 |
|---|---|
| 1 次且永不重来 | 手工/交互即可 |
| ≥ 2 次或需交付他人复现 | 写脚本，参数化输入 |
| 多步骤跨工具流水线 | Snakemake/Makefile 编排，固定数据流转格式 |

- 判据：**“别人能否照脚本复现同一结果”**。投稿/审稿/竞赛一律走可复现。

### 自动化触发条件 → 方案

| 触发条件 | 方案 | 理由 |
|---|---|---|
| 一次性本地运行 | 直接脚本/命令 | 无需编排，跑完即弃 |
| 多步骤、步骤间有数据依赖 | Snakemake/Make | 按文件依赖增量重算，本地编排 |
| 仓库事件/定时/协作复现 | GitHub Actions | `.github/workflows/*.yml`：push 即测、cron 定时抓数/重算、自动构建 PDF/图、发 release、matrix 多环境 |

- GitHub Actions 与 Snakemake 互补不替代：Actions 管"何时由什么事件触发、跑在哪个环境"，Snakemake 管"步骤间数据依赖怎么算"。CI 里常套一层 Actions 触发 → 内部调 Snakemake/脚本。

## 5. Python 环境：按依赖性质选

| 场景 | 工具 | 关键命令 |
|---|---|---|
| 纯 Python/PyPI | uv | `uv init` → `uv add` → `uv lock` → `uv sync` → `uv run`（比 pip 快 10-100x） |
| 编译科学库/CUDA/HDF5/跨语言 | conda (mamba/miniforge) | `conda env create -f environment.yml`；提速用 mamba |
| 既有 Poetry 项目 | Poetry | `poetry install`（按 poetry.lock） |
| 服务可移植复现 | Docker | 钉 FROM 版本，依赖层在前源码在后 |

- 铁律：**同一环境不混 pip + conda**（依赖求解冲突）。三者都靠锁文件保复现。
- uv 装不了的（预编译 CUDA、MKL、GDAL 等系统级二进制）才退到 conda。

## 6. 云算力：何时离开本机

| 触发条件 | 方案 |
|---|---|
| 本机无 GPU 且需训练/推理 | Modal（`@app.function(gpu="h100")`，按秒计费无空闲成本） |
| 大规模并行批处理 | Modal（map/spawn）/ 集群 |
| 跑 AI 生成的不可信代码 | Modal Sandboxes（隔离执行） |
| 本机足够（小模型/CPU 任务） | 留在本地，别上云徒增复杂度 |

## 7. 扩能力：发现已有 skill / MCP / 自建

决策序（详见 assets/skill_discovery_report.md）：

1. 先查现成 skill（skills.sh 排行榜 → `npx skills find`）。质量阈值见下。
2. 接外部数据/工具 → 找 MCP server（registry.modelcontextprotocol.io）。
3. 都没有 → skill-creator 自建（人写可评审）；批量原型可看 Autoskill（自动生成需隔离）。

### skill/MCP 质量数值阈值

| 信号 | 放心用 | 谨慎 | 存疑/避免 |
|---|---|---|---|
| 安装量 | ≥ 1K | 100 – 1K | < 100 |
| GitHub stars | ≥ 100 | 一般 | < 100 需额外审查 |
| 来源 | anthropics / vercel-labs / microsoft 官方 | 知名社区 | 无名作者 + 低星 |

- 任何第三方 skill/MCP = 授权外部指令与代码，先评估来源与安全再装。

## 8. HTTP API 调用

| 有无契约 | 做法 |
|---|---|
| 有 OpenAPI(3.1.x) 描述 | 按 `paths→operationId` + 参数 schema + `securitySchemes` 确定性调用，按 response schema 解析 |
| 无描述 | 先嗅探/抓包确认端点与字段，curl 实测记录 HTTP code，再封装 |

- 写进参考的任何端点必须 curl 实测并记录 HTTP code（CONVENTIONS 诚实底线）。

## 速用：四问定工具

1. **数据多大？** → 第 1 节选库。
2. **结果给谁/去哪？** → 第 3 节选格式。
3. **要不要复现？** → 第 4 节决定脚本化与版本管理。
4. **本机够不够？** → 第 5/6 节决定环境与是否上云。
