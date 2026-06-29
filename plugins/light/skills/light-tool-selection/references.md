# light-tool-selection 参考工具笔记

逐工具研究笔记，支撑 SKILL.md 的"工具发现"与"环境/协同"判断。所有信息来自官方文档/仓库，研究日期 2026-06。

## find-skills（技能发现）
- 【是什么】Vercel Labs 开源的 skill，当用户问"怎么做 X / 有没有做 X 的工具"时触发，去开放 agent-skill 生态里检索并安装合适的 skill。
- 【可复用工作流】1) 判断领域与任务、估计是否已有 skill；2) 看 skills.sh 排行榜（按总安装量排序的实战款，顶部如 vercel-labs/agent-skills 的 React/Next.js/web 设计、anthropics/skills 的 frontend-design/文档处理，均 100K+ 安装）；3) `npx skills find [关键词]` 搜索；4) 校验质量（安装量/GitHub star/来源信誉的数值阈值权威版见 references/decision_matrix.md 第 7 节，本处不复写数字）；5) 给用户列出 名称/用途/安装量/来源/安装命令/链接；6) 同意后 `npx skills add <owner/repo@skill> -g -y`。没有命中就坦白没有，转为直接用通用能力帮忙，并建议 `npx skills init <name>` 自建。
- 【链接】https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md
- 【已知坑】依赖 skills.sh 生态与安装量信号；冷门领域可能无可用 skill，别硬塞。

## skill-creator（技能创作）
- 【是什么】Anthropic 官方 skill，覆盖 skill 全生命周期：起草→测试→评估→迭代→优化触发率。
- 【可复用方法】目录结构：`skill-name/SKILL.md`（必需，YAML frontmatter 仅 name/description + Markdown 正文）+ 可选 `scripts/`（确定性任务的可执行代码）、`references/`（按需载入上下文的文档）、`assets/`（输出用模板/图标）。三级渐进披露：① metadata(name+description，约 100 词，常驻)；② SKILL.md 正文（触发时载入，建议 <500 行）；③ bundled resources（按需载入，无大小限制）。description 写法：Claude 倾向"欠触发"，描述要略"push"——枚举所有适用场景而非只写主用例；测试 query 要具体真实（含文件路径、口语、错别字、长短不一），别写"format this data"这种抽象句。正文用祈使句、解释"为什么"而非堆 MUST、从反馈泛化而非过拟合测试样例、>300 行的 reference 文件加目录、多框架时按领域拆分 reference 让 Claude 只读相关那份。
- 【评估/迭代闭环（核查得到的硬流程）】官方推荐的测试循环：① 起草 skill；② 写 2-3 条**贴近真实**的测试 prompt 并与用户确认；③ 同时跑 with-skill 与 baseline(without-skill) 两组（并行）；④ 跑的同时起草量化断言(assertions)；⑤ 评分、汇总成 benchmark、起 viewer；⑥ 用户在浏览器看输出+benchmark；⑦ 读反馈、改 skill、重复。测试样例存 `evals/evals.json`（字段 `skill_name` + `evals[{id,prompt,expected_output,files}]`）；工作区按 `iteration-N/eval-K/{with_skill,without_skill}/outputs` + `benchmark.json/md` 组织。改进哲学：从反馈泛化别过拟合样例；删不顶用的指令保持精简；读 transcript 而非只看输出找浪费的步骤；跨样例重复的活抽进 `scripts/`；改完用"新眼睛"复审再落地。停止条件：用户满意 / 反馈为空 / 无实质进展。
- 【链接】https://anthropics-skills.mintlify.app/reference/skill-creator ；规范 https://github.com/anthropics/skills ；官方实现 https://github.com/anthropics/claude-plugins-official/blob/main/plugins/skill-creator/skills/skill-creator/SKILL.md
- 【已知坑】SKILL.md 正文过长会吃满上下文；frontmatter 只认 name/description，其余靠目录约定。

## Autoskill（运行时动态生技能）
- 【是什么】dataanswer 开源（Python 3.11+，MIT，集成 LangChain）的 agent 插件，让 agent 运行时用 LLM 把自然语言任务描述生成可执行 Python skill 代码，并注册/版本化/持久化。
- 【可复用方法】reflection engine 分析执行报错并自动修复代码；用 sentence-transformers 做 skill 指纹（embedding 比对）去重；多级环境隔离执行；代码质量自动检测修复；懒加载 + 可选依赖控资源。
- 【链接】https://github.com/dataanswer/autoskill
- 【已知坑】生成代码质量依赖 LLM；运行时执行自生成代码需隔离，安全边界要自己把控。与 skill-creator 的"人写、可评审"路线相反——本工具偏自动化、适合原型/批量，慎用于生产。

## Skills CLI（npx skills）
- 【是什么】管理开放 agent skill 的命令行（find-skills 背后的工具）。
- 【可复用命令】`npx skills find [query]` 搜索；`npx skills add <owner/repo@skill> -g -y` 安装（-g 全局、-y 免确认）；`npx skills check` 查更新；`npx skills update` 更新；`npx skills init` 新建自定义 skill。排行榜在 skills.sh。
- 【链接】https://github.com/vercel-labs/skills
- 【已知坑】安装第三方 skill 等于引入他人指令/脚本，先看来源与安装量。

## GitHub Agent Skills 生态（anthropics/skills + awesome 列表）
- 【是什么】官方与社区的 skill 仓库集合。anthropics/skills 含 `skills/`（实现）、`spec/`（规范）、`template/`（起手模板）、`.claude-plugin/`（插件市场配置）。
- 【可复用方法】官方分四类：Creative & Design、Development & Technical、Enterprise & Communication、Document Skills。文档类 skill：`docx`/`pdf`/`pptx`/`xlsx`（source-available，生产文档能力即来源于此，恰好对应 Light 的排版/文档处理需求）；以 `document-skills` 与 `example-skills` 两个 plugin bundle 安装。社区聚合：VoltAgent/awesome-claude-skills（700+ skill，兼容 Codex/Cursor/Gemini CLI 等）、kodustech、junminhong 等 awesome 列表。
- 【链接】https://github.com/anthropics/skills ；https://github.com/VoltAgent/awesome-claude-skills
- 【已知坑】文档类 skill 非完全开源（source-available）；社区 skill 质量参差，用 find-skills 的质量信号筛。

## agent-browser（Vercel Labs，CDP 浏览器自动化）
- 【是什么】给 AI agent 用的浏览器自动化 CLI：导航、填表、点击、截图、抽数据、测 web app；还支持 Electron 桌面应用（VS Code/Slack/Discord/Figma/Notion/Spotify）和云浏览器。
- 【可复用方法】直接走 Chrome/Chromium 的 CDP（Chrome DevTools Protocol），不依赖 Playwright/Puppeteer；原生 Rust CLI（非 Node wrapper）。抓 accessibility-tree 快照，用紧凑 `@eN` 元素引用做稳定定位。SKILL.md 是发现 stub，真正用法由 CLI 动态发：`agent-browser skills get core`（工作流/常见模式/排错）、`--full`（全命令参考+模板）、`agent-browser skills list`；专门 skill：electron/slack/dogfood(探索测试)/vercel-sandbox/agentcore(AWS Bedrock 云浏览器)。安装 `npm i -g agent-browser && agent-browser install`。带会话、认证 vault、状态持久化、录像、4848 端口可观测面板。
- 【链接】https://github.com/vercel-labs/agent-browser/blob/main/skills/agent-browser/SKILL.md
- 【已知坑】仅 Chromium/CDP；面板与会话流量内部代理，agent 要留在面板 origin。

## browser-use（Python，LLM 驱动浏览器）
- 【是什么】开源 Python 库（MIT，Python ≥3.11），基于 Playwright，把网页变成 AI agent 可操作的对象，按自然语言任务自动执行。
- 【可复用方法】核心两对象：`Agent(task=..., llm=..., browser=...)` + `await agent.run()`；`Browser()` 包会话，`use_cloud=True` 走云端 stealth 浏览器。LLM provider：`ChatBrowserUse`（自家优化模型，推荐）、`ChatGoogle`、`ChatAnthropic`、Ollama 本地。自定义工具用 `@tools.action(description=...)`（`Tools` 装饰器）。CLI 在命令间保活浏览器：`browser-use open/state/click N/type/screenshot/close`。装：`uv init && uv add browser-use && uv sync`，缺 Chromium 跑 `uvx browser-use install`；起手模板 `uvx browser-use init --template default`（另有 advanced/tools 模板）。LLM 模型示例 `ChatAnthropic(model='claude-sonnet-4-6')`、`ChatGoogle(model='gemini-3-flash-preview')`。
- 【链接】https://github.com/browser-use/browser-use
- 【已知坑】Chrome 吃内存、多 agent 并行难管；CAPTCHA 需更好指纹/代理（官方导向云服务）；登录态要复用真实 Chrome profile；准确率强依赖所用 LLM。

## Get Available Resources（= MCP resources/list）
- 【是什么】对应 MCP 的资源发现机制：server 把文件/DB schema/应用数据等以 URI 标识的"资源"暴露给 client，供 LLM 取用上下文。资源是 application-driven（宿主决定如何纳入上下文），与 model-controlled 的 tools 不同。
- 【可复用方法】`resources/list`（支持 cursor 分页）发现资源；`resources/read`（传 uri）读内容（text 或 base64 blob）；`resources/templates/list` 列参数化模板（RFC6570 URI template，如 `file:///{path}`）；可 `resources/subscribe` 订阅变更，server 发 `notifications/resources/updated`。资源字段：uri/name/title/description/mimeType/size；annotations（audience=user/assistant、priority 0-1、lastModified）帮 client 过滤与排序。标准 URI scheme：https://、file://、git:// + 自定义。错误：未找到 -32002、内部 -32603。
- 【链接】https://modelcontextprotocol.io/specification/2025-06-18/server/resources
- 【已知坑】tool 返回的 resource_link 不保证出现在 resources/list；敏感资源要做访问控制。

## Modal（Python serverless 云算力）
- 【是什么】Python 的 serverless AI 基础设施：把代码跑进云端容器、自动扩缩、按秒计费、无空闲成本。适合 LLM 推理、大规模并行批处理、GPU 训练/微调、代码沙箱、文档解析/转写/抓取。
- 【可复用方法】`app = modal.App("name")`；`@app.function(gpu="h100", image=...)` 标记远程函数；`modal.Image.debian_slim().uv_pip_install(...)` 代码内定义容器环境（无需 Dockerfile/YAML）；原语：Volumes(持久存储)、Secrets(密钥)、Sandboxes(跑 AI 生成代码的隔离环境)、Cron/Scheduling(定时)、Dicts/Queues(跨函数共享结构)。流程：`pip install modal` → `modal setup` 认证 → `modal run file.py`(本地触发云容器)；持久服务用 `modal deploy`。Python 为主，JS/TS/Go 可调用 Function/Sandbox/管理资源。跨云池化容量动态优化 GPU 可用性与成本。
- 【链接】https://modal.com/docs/guide
- 【已知坑】纯 Python 生态、按秒计费需留意成本；环境全在代码里定义，迁出 Modal 需另写容器化。

## OpenAPI Specification（HTTP API 契约）
- 【是什么】描述 HTTP API 的语言无关标准（JSON/YAML），是 provider 与 consumer 之间的机器可读契约（当前 3.1.x）。
- 【可复用方法】顶层：`openapi`(版本，必需)、`info`(title/version，必需)、`servers`(base URL，可变量替换)、`paths`(核心：路径→各 HTTP 方法的 Operation，含 parameters[path/query/header/cookie]、requestBody、responses[按状态码]、security、operationId)、`components`(可复用 schemas/parameters/responses/securitySchemes 等)、`security`(全局)、`webhooks`(3.1)。工具链：Swagger Codegen 生成 server stub/client SDK、Swagger UI 渲染交互文档、Swagger Editor、契约测试、mock server。对 agent：把"读散文文档"变确定性——选对 operationId、按 schema 填参、套对 auth(header/query/cookie)、按 response schema 解析。
- 【链接】https://swagger.io/specification/
- 【已知坑】文档与实现可能漂移，需契约测试守护；3.0 与 3.1（对齐 JSON Schema）有差异，注意 codegen 版本支持。

## MCP Server 生态（modelcontextprotocol/servers + registry）
- 【是什么】MCP 参考 server 集 + 社区注册中心。统一协议让 client 发现并调用外部 tool/resource/prompt。
- 【可复用方法】官方参考 server：Everything(演示 prompts/resources/tools)、Fetch(取网页转 LLM 友好格式)、Filesystem(带访问控制的文件操作)、Git(读/搜/改 Git 仓库)、Memory(知识图谱持久记忆)、Sequential Thinking(反思式分步推理)、Time(时区转换)。运行：TS server 用 `npx -y @modelcontextprotocol/server-memory`，Python server 用 `uvx mcp-server-git`(推荐)；client 用 JSON 配 command+args（Windows 的 npx 项要 `cmd /c` 包裹）。发现更多 server 去 registry.modelcontextprotocol.io。Tool 发现走 `tools/list`(分页)、调用 `tools/call`，结果可 text/image/audio/resource_link/embedded/structuredContent，错误分协议错误(JSON-RPC)与执行错误(isError:true)。
- 【链接】https://github.com/modelcontextprotocol/servers ；https://github.com/modelcontextprotocol/registry
- 【已知坑】参考 server 是教学用、非生产级；引入第三方 server 等于授权外部代码访问文件/网络，要评估安全。

## Docker（容器化与可复现环境）
- 【是什么】把应用与依赖打包进可移植镜像、跑成隔离容器，保证"我机器能跑=你机器能跑"。Light 中用于后端部署、复现实验环境。
- 【可复用方法】Dockerfile 关键指令：`FROM`(基础镜像，务必钉版本 tag 而非 latest)、`WORKDIR`、`COPY`、`RUN`(装依赖，合并减少层)、`EXPOSE`、`CMD`(默认命令)/`ENTRYPOINT`(固定入口)。镜像按层缓存——把不常变的依赖安装放前面、源码 COPY 放后面以复用缓存。`.dockerignore` 排除无关文件。`docker build -t name .` / `docker run` / 数据用 `-v` volume 挂载。多阶段构建(multi-stage)：构建阶段产物拷进精简运行镜像，减小体积。多服务用 docker compose（compose.yaml 声明 services/networks/volumes）。
- 【链接】https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/ （注：研究时该域名在本环境被网络策略拦截，内容据 Docker 既有官方知识整理；端点/概念稳定，使用前以官方文档为准）
- 【已知坑】用 latest 破坏可复现；镜像层顺序不当导致缓存失效、构建慢；容器内写数据不持久需 volume。

## GitHub Actions（仓库事件触发的 CI/CD 自动化）
- 【是什么】GitHub 内建的事件驱动自动化平台：仓库发生事件(push/PR/定时/手动)时，在云端 runner 上跑 workflow。与 Snakemake/Make 互补——后者管本地数据依赖编排，前者管"何时由什么事件触发、跑在哪个环境"。科研常用：push 即跑测试、cron 定时抓 arXiv/数据/重算、自动构建 LaTeX PDF 与图、发布 release、matrix 多环境复现。
- 【可复用方法】workflow 是 YAML，放 `.github/workflows/*.yml`(一仓可多份)。核心字段：
  - `name`：workflow 名。
  - `on`：触发条件——`push`/`pull_request`(可按 branches/paths 过滤)、`schedule`(cron 定时，如 `- cron: '0 6 * * *'` 每日 06:00 UTC)、`workflow_dispatch`(手动/带输入参数触发)、`release`/`issues` 等。
  - `jobs`：并行的作业，每个含 `runs-on`(如 ubuntu-latest)与有序 `steps`。
  - `steps`：每步要么 `uses`(调现成 action)要么 `run`(跑 shell)。常用 action(checkout/setup-python 版本真相源见 light-backend-coding a03 references「版本实测」段，2026-06 为 v6)：`actions/checkout@v6`(拉代码)、`actions/setup-python@v6`(装 Python)、`astral-sh/setup-uv@v5`(装 uv，配 `uv sync` 复现)、`actions/cache@v4`(缓存依赖/~/.cache 提速)、`actions/upload-artifact@v4` / `download-artifact`(传产物如 PDF/图/数据)。
  - `strategy.matrix`：多版本/多环境笛卡尔积复现，如 `matrix: {python-version: ['3.10','3.11','3.12'], os: [ubuntu-latest, macos-latest]}`，配 `runs-on: ${{ matrix.os }}`。
  - `secrets`：敏感值经 `${{ secrets.NAME }}` 注入(仓库/环境级配置，绝不写进 YAML)。
  - `permissions`：收窄 `GITHUB_TOKEN` 权限(如发 release/写 pages 才给 `contents: write`)，最小权限原则。
- 【科研典型场景】① test-on-push：`on: [push, pull_request]` + setup-uv + `uv run pytest`。② 定时抓数：`on: schedule` cron + 脚本抓 arXiv/数据 + commit 回仓或 upload-artifact。③ 自动出论文：checkout + 装 TinyTeX/TeX Live + `latexmk -pdf` + upload-artifact 上传 PDF。④ 发布：打 tag 触发 `on: release` 或 `softprops/action-gh-release` 传产物。⑤ matrix 复现：跨 Python/OS 跑同一套实验验证可复现。
- 【链接】https://docs.github.com/actions ；action 市场 https://github.com/marketplace?type=actions ；setup-uv https://github.com/astral-sh/setup-uv
- 【已知坑】schedule cron 用 UTC 且高峰可能延迟数分钟、仓库 60 天无活动会停跑定时任务；私有仓有分钟配额、注意成本；不要把 secret 写进日志/YAML；第三方 action 钉到 commit SHA 或可信版本 tag(防供应链投毒)；GITHUB_TOKEN 默认权限按仓库设置，能收窄就收窄。

## Conda（语言无关的包+环境管理）
- 【是什么】跨平台命令行工具，管理"环境+包"，含非 Python 二进制/编译库，语言无关。
- 【可复用方法】`conda create --name env`、`conda activate env`、`conda install pkg`、`conda env export`(→ environment.yml 复现)、`conda env create -f environment.yml`、`conda info --envs`。channel 是包来源，社区首选 conda-forge（`conda install conda-forge::numpy` 或 .condarc 设默认）。**何时优先 conda**：编译科学库(NumPy/SciPy/OpenCV 预编译二进制)、CUDA/GPU 栈(能协调 CUDA toolkit 版本，pip 做不到)、系统级非 Python 依赖(HDF5/FFTW/MKL)、跨语言(R/Julia/C++ 同环境)。提速用 **mamba**(C++ 重写、drop-in)，**miniforge** 最小安装器(默认 conda-forge + 自带 mamba，规避 Anaconda 商业 license 顾虑)。
- 【链接】https://docs.conda.io/projects/conda/en/stable/user-guide/getting-started.html
- 【已知坑】大环境求解慢(用 mamba)；与 pip 混用易冲突；Anaconda 默认 channel 有商业授权限制(转 conda-forge/miniforge)。

## uv（Astral，Rust 写的极速 Python 包/项目管理）
- 【是什么】Rust 实现、号称比 pip 快 10-100x 的统一工具，替代 pip/pip-tools/pipx/poetry/pyenv/twine/virtualenv。
- 【可复用方法】`uv init`(建项目)、`uv add`(加依赖，`--script` 支持单文件脚本)、`uv lock`(写 uv.lock 通用锁文件，跨平台可复现)、`uv sync`(按锁文件确定性安装)、`uv run`(项目环境内执行)、`uv venv`(建虚拟环境，可指定 Python 版本)、`uv pip compile/sync`(pip-tools 兼容)、`uv python install 3.10 3.11 3.12` + `uv python pin`(替代 pyenv)、`uvx`(临时环境跑工具 = uv tool run)。全局缓存去重省盘；无需预装 Python(独立安装器)。
- 【链接】https://docs.astral.sh/uv/
- 【已知坑】较新、生态比 Poetry 年轻；纯 Python/PyPI 范畴，编译科学栈/CUDA 仍可能需 conda。

## Poetry（Python 依赖管理与打包）
- 【是什么】Python 3.10+ 的依赖管理+打包一体工具，自带锁文件与每项目自动 virtualenv。
- 【可复用方法】`poetry new`/`poetry init`(建/初始化 pyproject.toml)、`poetry add`、`poetry install`(按 poetry.lock 装)、`poetry lock`、`poetry run`(virtualenv 内执行)、`poetry build` + `poetry publish`(发 PyPI)。2.0+ 依赖可写 PEP 621 `[project.dependencies]`；poetry.lock 钉全部传递依赖。dependency groups 分 main/dev/自定义组，可选装子集。
- 【链接】https://python-poetry.org/docs/
- 【已知坑】Python 实现的 SAT resolver 比 uv 慢；仅 Python/PyPI 范畴；与 conda 的科学二进制栈不互通。

## 横向选型小结
- 装 Python 环境：纯 Python 项目优先 **uv**(快、统一)；需编译科学库/CUDA/跨语言用 **conda(mamba/miniforge)**；已有 Poetry 项目延续 **Poetry**。
- 扩能力：先 **find-skills / Skills CLI** 查现成 skill，再看 **MCP server 生态**接外部数据/工具；自建 skill 用 **skill-creator**(可评审、人写)，原型批量可看 **Autoskill**(自动生成，需隔离)。
- 跑网页任务：偏 CLI/CDP 稳定选 **agent-browser**；偏 Python 集成选 **browser-use**。
- 接 HTTP API：有 **OpenAPI** 描述就按 operationId+schema 确定性调用。
- 上云算力：Python serverless/GPU 用 **Modal**；要可移植可复现的服务环境用 **Docker**。
