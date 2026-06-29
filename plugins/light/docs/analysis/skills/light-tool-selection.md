# light-tool-selection — 深度分析与同类对标

> 源：[`skills/light-tool-selection/SKILL.md`](../../../skills/light-tool-selection/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：常驻型"用什么做"的元决策技能:给定科研任务,按数据规模/输出去向/复现要求/算力四维匹配最高效稳定专业的工具栈,并提供项目技术栈自动检测脚本与 skill/MCP 扩能力发现流程。

## 核心运行逻辑
核心是一条"不为用工具而用工具"的元原则,落到一张"任务→推荐工具"映射表 + 一份带数值阈值的决策矩阵(decision_matrix.md)。设计上把"选型知识"分三层渐进披露:SKILL.md 正文给映射与决策要点,references.md 给逐工具真实端点/命令/坑,decision_matrix.md 给量化阈值,按需载入。唯一的自动化环节是 detect_stack.py:读 package.json/pyproject/requirements/environment.yml/Pipfile 的依赖,精确匹配约 70 条内置规则给选型建议,命中才给、未命中标 no-signal 不臆造,并据锁文件给环境/复现建议。扩能力遵循"先查现成 skill→再找 MCP server→最后 skill-creator 自建"的安全决策序,配三份呈现模板。整体偏被动知识库+一个轻量检测器,本身不执行选型,而是给其他技能与编排器提供判断依据。

## 关键步骤
- 1. 进入任务/项目时先问四问:数据多大、结果给谁、要不要复现、本机够不够
- 2. 已有项目则跑 detect_stack.py 扫描清单文件,识别依赖与锁文件,按类别输出命中规则的选型建议,no-signal 项不臆造
- 3. 查 decision_matrix.md 按数值阈值(数据<100MB pandas / 2-50GB polars / >TB Spark;投稿矢量 vs 演示 png 等)定具体工具
- 4. 需要新能力时按序:skills.sh 排行榜+npx skills find 查现成 skill(安装量≥1K/star≥100 质量阈值)→registry 找 MCP server(先 tools/list 探测)→skill-creator 自建
- 5. 用对应 assets 模板(stack/skill/mcp 三份)向用户汇报候选与质量信号,征得同意后再安装
- 6. 多工具协同时规划数据在工具间的流转格式(CSV/JSON/Parquet),减少手工搬运

## 自带资产
- scripts/detect_stack.py — 读项目清单识别技术栈、按 RULES 表给选型建议,带 --self-test 离线自检与 --json 输出
- references/decision_matrix.md — 8 节带数值阈值的决策矩阵(数据规模/统计建模/绘图格式/复现/环境/云算力/扩能力质量阈值/HTTP API)+四问速用
- references.md — 16 个工具的逐项研究笔记(是什么/可复用方法/链接/已知坑),含 uv/conda/Poetry/Docker/GitHub Actions/Modal/MCP/OpenAPI/agent-browser/browser-use 等
- assets/stack_detection_report.md — 检测脚本结果的汇报模板,含边界声明
- assets/skill_discovery_report.md — 发现 skill 的呈现模板(单候选/多候选对比表/未命中兜底/质量阈值速查)
- assets/mcp_discovery_report.md — 发现 MCP server 的呈现模板,含接入前 tools/list 探测清单与官方参考 server 表
- scripts/__pycache__/detect_stack.cpython-311.pyc — 编译缓存(不应随技能打包,属冗余)

## 优点
- 决策有量化锚点:decision_matrix.md 给出真实数值阈值(数据体量分档、dpi、安装量/star),而非空泛的'视情况而定',可直接照用
- 诚实底线扎实:检测脚本'命中才给、未命中标 no-signal'不臆造;所有版本/安装量信息带 last_checked 2026-06;阈值明确标注为'经验起点,临界值实测'
- detect_stack.py 工程质量高:纯标准库+优雅降级(无 PyYAML 时正则解析 yml、无 tomllib 时跳过并提示),覆盖 6 种清单+9 种锁文件+GitHub Actions 探测,自带 self_test 断言可离线验证
- references.md 是真做过功课的研究笔记,每个工具都有'已知坑'(如 vaex 已停维护、Anaconda 商业授权、cron UTC 延迟、第三方 action 钉 SHA 防供应链投毒),不是堆砌官网摘要
- 安全意识贯穿:反复强调'装第三方 skill/MCP=授权外部代码先评估来源',符合科研工具引入的合规要求
- 三份呈现模板把抽象的'发现→汇报→征得同意'流程标准化,降低 agent 自由发挥导致的不一致

## 缺点 / 可被质疑处
- 注释与实现不符(潜在 bug):detect_stack.py 第25行称'小写子串'匹配,实际 suggest() 是精确相等,torchvision/opencv-python/scikit-image/lightgbm/xgboost 等常见科研库都不会命中,静默掉进 no-signal,误导用户以为'无建议'
- 断链引用:decision_matrix.md 第85行指向不存在的 skill_discovery.md(真实文件名 assets/skill_discovery_report.md),按需载入会失败
- 检测能力与技能宣称范围严重不匹配:SKILL.md 声称覆盖 R/MATLAB/LaTeX/Word/Excel/Origin,但 detect_stack.py 只解析 Python/JS 清单,无法识别 R(DESCRIPTION/renv.lock)、MATLAB(.m/项目)、LaTeX 项目,科研最常用的几类工具检测不到
- 最关键的决策维度无法自动化:pandas/polars/dask 选型取决于数据体量,但脚本只能看依赖、看不到数据规模;'四问'里最核心的'数据多大'完全靠人工,检测器价值受限
- 三处文档大量重复(Python 环境选型在 SKILL.md/decision_matrix.md/references.md 各写一遍、质量阈值写三遍),维护时极易产生版本漂移,改一处忘改两处
- 跨技能引用编码不统一且无对照表:SKILL.md 用 a06/a02/a03,decision_matrix.md 用 light-backend-coding/code_assets,读者无法对应到具体技能;'常驻'如何真正生效也无机制说明,纯靠编排器自觉
- 自相矛盾的资产缺失:references.md 用整段详述 skill-creator 的 evals/evals.json 评估闭环,但本技能自己未附任何 eval 用例,无法量化验证选型建议质量;RULES 表无任何测试覆盖率说明,70 条规则的取舍依据不透明

## 可优化点（供后续逐技能优化）
- 修正 detect_stack.py 匹配逻辑:要么把 suggest() 改为真正的子串/前缀匹配(torch* 系列归 torch),要么把注释改为'精确匹配'并补全常见别名(opencv-python/scikit-image/xgboost/lightgbm/gradio/streamlit/langchain/openai/anthropic 等),同时在 self_test 里加这些断言
- 修复 decision_matrix.md→skill_discovery.md 的断链,统一指向 assets/skill_discovery_report.md;并全目录做一次内部引用校验
- 扩展检测器到科研真实栈:加 R(DESCRIPTION/renv.lock/.Rproj)、MATLAB(.m 扫描/Project)、LaTeX(.tex/latexmkrc)、Jupyter(.ipynb)识别,使检测能力覆盖 SKILL.md 宣称的工具面
- 给检测器加'数据规模感知':可选扫描项目 data/ 目录下文件大小,据 decision_matrix 第1节自动提示 pandas/polars/dask 分档,补上最关键却缺失的自动化维度
- 去重收敛:把 Python 环境选型、质量阈值等重复内容收到单一权威位置(如只留 decision_matrix.md),SKILL.md 改为指针引用,消除三处漂移风险
- 建立技能编码对照:在 SKILL.md 或 CONVENTIONS 增加 a02/a03/a06 ↔ light-* 名称映射表,让跨技能衔接可追溯
- 补一份 evals/evals.json:用几条真实 prompt(如'5GB CSV 该用什么''投稿图要什么格式''这个 conda 项目环境怎么搭')做 with/without 对比,既自证质量又示范 skill-creator 闭环
- 把 __pycache__ 加入忽略、从技能包移除,保持 bundle 干净;并给检测器输出加版本/日期戳便于追踪规则表更新

## 与其他 Light 技能/知识库的衔接
作为"用什么做"的元判断技能,自述与 a06(项目结构/目录)、a02(版本工具)、a03(代码栈 light-backend-coding)协同,decision_matrix.md 还引用 light-backend-coding 的 references 版本实测段(setup-python v6 等)与 code_assets/stats_tests.py、agreement.py(主张复用已验证实现不重建)。实际上它为几乎所有 Light 技能前置供给工具选型:数据处理(light-data-engineering)、绘图(light-figure-drawing/planning)、排版(light-typesetting)、PPT(light-slides)、前后端(light-frontend-design/light-system-design)。声明 user-invocable: false 且"常驻、后台生效",定位为编排层调用的支撑技能而非用户直接触发,但文件内未说明常驻的具体触发机制,依赖 light-orchestrator/light-memory-pm 在 pipeline 中主动挂载。

---

## GitHub 同类前沿技能对标

light-tool-selection 是一个"元决策"知识库技能:它本身不执行选型,而是用四维(数据规模/输出去向/复现要求/算力)把科研任务映射到工具栈,并配一个约70条规则的轻量栈检测脚本(detect_stack.py)和"先skill→再MCP→最后自建"的扩能力发现序。GitHub 上几乎没有与它"科研场景+工具栈映射表+三层渐进披露+诚实no-signal检测"完全同构的项目。最接近的是两类:一类是工程化的"工具/模型路由器"(RouteLLM、tool-selector-cascade、mcp-mcp、metamcp、claude-skills-mcp),用嵌入/重排/分类器在运行时动态选工具或模型,自动化和规模远超 Light,但全部面向通用 agent 而非科研选型,且不给"为什么用这个工具"的人读决策矩阵;另一类是 skills/agents 大全(VoltAgent、travisvn、obra/superpowers、awesome-claude-agents),靠数量与社区覆盖取胜,其中 awesome-claude-agents 内置"技术栈自动检测→路由到专家子agent",与 detect_stack.py 思路最像。整体看,Light 的差异化在于"科研垂直+带数值阈值的人读决策表+命中才给不臆造"的克制定位,弱点在于无运行时自动执行、规则为手工内置、无语义检索因而召回受限。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM) | 面向模型选型的路由框架:训练/评估路由器,在强弱模型间按查询难度分流,在不牺牲质量前提下省成本,是'自动选哪个模型'的学术级实现。 | 5014 | 2026-06-12 | 强:有可训练路由器、基准与量化评估,真正运行时自动决策。弱:只解决选哪个LLM,不覆盖科研工具栈(绘图/统计/复现/算力)选型,无人读决策表,不做项目依赖检测。 |
| [metatool-ai/metamcp](https://github.com/metatool-ai/metamcp) | MCP 聚合器/编排器/中间件/网关,一处管理所有 MCP server,可对工具分组、过滤、命名空间与按需暴露,缓解工具过多导致的上下文膨胀。 | 2409 | 2026-06-12 | 强:工程成熟、可自托管,真正落地'扩能力发现'里 MCP 接入与治理。弱:是基础设施层,不给'该不该用某工具'的判断逻辑,与 Light 互补而非同质,且无科研语境。 |
| [wojtyniak/mcp-mcp](https://github.com/wojtyniak/mcp-mcp) | Meta-MCP server,充当 MCP 的工具发现与按需供给服务:agent 描述需求,它去发现并临时挂载合适的 MCP 工具,正是 Light'先找MCP server'那步的自动化版。 | 22 | 2026-06-11 | 强:把'找MCP'从人工查变成运行时自动发现+供给。弱:star 少、早期阶段,只管 MCP 不管原生工具/库选型,无科研四维矩阵,无依赖检测。 |
| [K-Dense-AI/claude-skills-mcp](https://github.com/K-Dense-AI/claude-skills-mcp) | 用向量检索对 Claude Agent Skills 做搜索与召回的 MCP server,让 agent 在大量技能里语义匹配出该用哪个,对应 Light'先查现成skill'那步。 | 392 | 2026-06-10 | 强:语义检索召回比 Light 手工规则更可扩展,技能多时优势明显。弱:只做'选技能'检索,不给科研工具栈映射与阈值决策,不解释取舍,无栈检测。 |
| [bernard777/tool-selector-cascade](https://github.com/bernard777/tool-selector-cascade) | 级联式工具选择器:用'语义嵌入→交叉编码重排→微型LLM'三级渐进过滤,约450ms 内从1000+工具选出最佳匹配,跨 OpenAI/Anthropic/Gemini。 | 0 | 2026-03-12 | 强:三级渐进过滤与 Light 三层渐进披露神似,且运行时自动执行、可处理超大工具集。弱:0 star、很新,通用 function-calling 取向,无科研选型知识,无人读决策矩阵与复现建议。 |
| [vijaythecoder/awesome-claude-agents](https://github.com/vijaythecoder/awesome-claude-agents) | 编排式子 agent 开发团队:内置'技术栈自动检测→路由到对应框架专家 agent',按检测到的项目栈(Laravel/React/Django 等)动态组队。 | 4309 | 2026-06-12 | 强:其'检测栈→路由'思路与 detect_stack.py 最接近,且真正驱动子 agent 执行。弱:面向通用 Web/应用开发而非科研,检测后派 agent 干活而非输出'工具选型决策表',无算力/复现/投稿维度。 |
| [obra/superpowers](https://github.com/obra/superpowers) | 一套 agentic 技能框架与软件开发方法论,提供大量可组合技能与技能编排约定,是当前最热门的 Claude 技能框架之一。 | 226114(API 返回值,数量级偏异常,仅供参考) | 2026-06-13 | 强:生态与社区体量大,技能组织/披露范式成熟,可借鉴其编排约定。弱:偏软件开发方法论,无'科研任务→工具栈'垂直映射,无量化决策矩阵与依赖检测脚本。 |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 1000+ agent 技能精选大全,跨 Claude Code/Codex/Gemini CLI/Cursor,按领域分类索引,可视作'有哪些工具/技能可选'的目录层。 | 25158 | 2026-06-13 | 强:覆盖面与更新频率极高,是发现候选工具/技能的优质来源。弱:是清单不是决策器,不告诉你'这个科研任务该用哪个',无阈值、无检测、无取舍逻辑。 |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | 面向 Claude Code 的 Claude Skills 精选清单与资源集合,收录官方与社区技能、模板与工作流。 | 13418 | 2026-06-13 | 强:热度高、社区活跃,适合做'先查现成skill'的检索入口。弱:同为静态清单,无元决策能力,不做工具栈匹配与项目检测,是上游目录而非同类决策器。 |
| [levnikolaevich/claude-code-skills](https://github.com/levnikolaevich/claude-code-skills) | 覆盖完整交付生命周期的 Claude Code 插件套件+内置 MCP server(研究、规划、审计、性能优化、代码知识图谱等),含按阶段路由的工作流。 | 488 | 2026-06-10 | 强:把技能按交付阶段编排并捆绑 MCP,工程完整度高,可借鉴其'阶段→技能'映射。弱:面向软件交付而非科研选型,无四维工具矩阵、无诚实 no-signal 检测脚本。 |

### Light 该技能可借鉴的点
- 给 detect_stack.py 加可选语义检索层(参考 claude-skills-mcp / tool-selector-cascade):手工70条规则未命中时,用嵌入对工具库做软匹配召回候选,仍保留'命中才给、其余 no-signal'的诚实输出,提升召回又不臆造。
- 把'扩能力发现序'从纯文档升级为可调用入口:对接 mcp-mcp / metamcp 这类 Meta-MCP,让'先查skill→再找MCP'从人工查变成运行时可发现可挂载,Light 仍只负责'该不该用'的决策。
- 借鉴 awesome-claude-agents 的'检测栈→路由到专家'闭环:detect_stack.py 当前只给建议,可加可选钩子把检测结果直接喂给 light-orchestrator 触发对应技能,缩短'检测—决策—执行'链路。
- 引入 RouteLLM 式'难度/成本分级'到算力维度:在 decision_matrix.md 里对模型/算力档位给出类似'轻任务走小模型、重任务才上大模型'的量化分流规则,而非仅按数据规模给阈值。
- 用 VoltAgent/travisvn 这类清单作为 references.md 的外部刷新源,定期核对内置规则里工具端点/命令是否过时,缓解'手工内置规则会陈旧'的弱点。
- 对标 superpowers/levnikolaevich 的技能编排约定,把三层渐进披露(SKILL/references/decision_matrix)做成更标准化、可被其他技能机器读取的元数据结构,便于被编排器和外部技能复用。
