# light-backend-coding — 深度分析与同类对标

> 源：[`skills/light-backend-coding/SKILL.md`](../../../skills/light-backend-coding/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：科研/后端代码编写与审查技能:把 obra/superpowers 的 TDD-调试-代码审查方法论本地化到数据/模型场景,并配一套版本实测、pytest 实跑通过的可复制 Python 项目骨架。

## 核心运行逻辑
核心是"方法论 + 可运行资产"双层结构。SKILL.md 正文给决策要点(代码质量五标准、uv/Poetry 双依赖路线、ruff/mypy/pytest/pre-commit/SonarQube/GitHub Actions 质量门、调试与审查四法、安全与产出契约),深用细节下沉到 references/ 七个专题文件,避免正文膨胀。方法论几乎全部对标 obra/superpowers 与 mattpocock 的五个开源 skill(systematic-debugging、TDD、requesting/receiving-code-review、improve-codebase-architecture、subagent-driven-development、finishing-a-development-branch),并为科研场景做"本地加强"(数值/shape/NaN、随机种子、数据泄漏、设备精度热点)。references.md 是硬信息层,每个工具记【是什么/真实端点参数/链接/已知坑】,版本号经 2026-06 PyPI+GitHub API curl HTTP 200 核验。assets/project-scaffold 是按 references 搭的最小可跑项目,本机 pytest 4 passed、ruff All checks passed,复制改名即用。技能定位为 Light 科研流水线里 a03 阶段的代码执行者,与 m05 方案、m02 流水线、db03 方法卡、m06 分析、a06 结构整理衔接。

## 关键步骤
- 1. 写代码前:读现有代码匹配项目风格/约定/依赖,明确输入输出/边界/复现要求(种子/版本)
- 2. 选依赖路线:uv(推荐)或 Poetry,始终提交 lock 文件,CI 用 uv sync/poetry install 还原确定性环境
- 3. TDD 循环:写最小失败测试并亲眼看它失败(确认功能缺失而非拼写错)→ 最简实现转绿 → 绿灯后才重构;无失败测试不写生产代码
- 4. 起步可直接复制 assets/project-scaffold(pyproject+pre-commit+CI+示例模块/测试+审查清单+调试脚本)
- 5. 质量门:ruff check + ruff format --check(两个命令)、mypy 按项目性质选档(科研 basic/库 strict)、pytest --cov、pre-commit、必要时 SonarQube Quality Gate
- 6. 遇 bug 走系统化调试四阶段:Phase 1 根因调查五步(逐字读错误→稳定复现→查最近改动→边界埋点定位坏在哪层→反向追数据流到源头),连修 3 次失败停手质疑架构
- 7. 代码审查:按 Critical/Important/Minor 分级,每条建议过五查+YAGNI,回应技术化不表演性赞同
- 8. 收尾:合并前必过全测试,合并→重跑测试→移 worktree→删分支,丢弃工作需显式确认
- 9. 产出:可运行代码+测试+依赖环境说明+README+运行命令;作 a03 时产出 run_manifest.md 交 m06

## 自带资产
- SKILL.md — 主入口,代码质量标准/工程实践/调试审查四法/衔接的决策要点
- references.md — 12 个工具的硬信息研究笔记(systematic-debugging/TDD/code-review×2/improve-architecture/subagent-dev/finishing-branch/GitHub Actions/Ruff/pre-commit/pytest/SonarQube/uv/Poetry),含真实端点参数和已知坑,版本经 curl 核验
- references/debug_protocol.md — 系统化调试四阶段+科研场景根因热点+边界埋点模板+合理化借口反驳表
- references/tdd_redflags.md — TDD 红旗清单+合理化借口反驳表+科研代码特有红旗+完成前验证清单
- references/code_examples.md — 最小够用vs过度工程、源头校验vs症状补丁的 Python 对照例 + 四法摘要
- references/asset_manifest_governance.md — 资产清单防漂移校验器设计(精确键/AST入口检测/分阶段收紧)
- references/skill_selftest_ci.md — 技能脚本 --selftest 与 CI 实际执行门规范
- references/light_skill_pack_maintenance.md — 维护 Light 技能包的断点恢复/质量门/入口防漂移/安装脚本防漂移
- assets/project-scaffold/pyproject.toml — uv+hatchling+ruff+mypy(双档注释)+pytest 完整配置
- assets/project-scaffold/.github/workflows/ci.yml — checkout@v6→setup-python@v6→uv sync→ruff→pytest 多版本矩阵
- assets/project-scaffold/.pre-commit-config.yaml — ruff+基础钩子,rev 锁 tag
- assets/project-scaffold/src/example/stats.py + tests/test_stats.py + conftest.py — 单一职责+源头校验+parametrize+异常断言示例,本机实跑 4 passed
- assets/project-scaffold/CODE_REVIEW_CHECKLIST.md — 分级审查清单,科研代码加强
- assets/project-scaffold/scripts/boundary_trace.py — 数据流边界打点装饰器,含合成 NaN 自测可直接 python 跑
- assets/project-scaffold/scripts/debug_instrument.sh — 多组件边界证据采集 bash 模板

## 优点
- 方法论不空谈:TDD/调试/审查都对标具体开源 skill 并给出可执行铁律(无失败测试不写生产代码、连修3次停手质疑架构、合并前必过测试),配合合理化借口反驳表,直接对抗 agent 在压力下偷懒走捷径的倾向
- 硬信息可信度高:references.md 的工具版本号经 2026-06 PyPI/GitHub API curl HTTP 200 核验,骨架本机 pytest 4 passed/ruff 通过,不是凭记忆写的版本号,降低 agent 编造过时配置的风险
- 科研场景本地加强是真增量:数值/shape/dtype/NaN-Inf、随机种子全链路固定、数据泄漏(划分前标准化)、设备/精度(CPU过GPU挂)、Windows GBK 编码这些热点是参考库未覆盖且科研代码高频踩的坑
- 骨架质量过硬:pyproject 注释解释了 hatchling packages 为何必须显式声明、mypy 双档切换、per-file-ignores 等真实工程细节;conftest 还诚实标注了 sys.path hack 装包后应删除、uv 路径未实测只测了 pip
- boundary_trace.py 设计巧妙:不依赖 numpy/torch 具体库用 getattr 取 shape/dtype、math 检 NaN/Inf,合成自测构造 0/0 演示 NaN 源头定位,真正可跑且教学意义强
- 正文/references/assets 三层分工清晰,正文保留指针不膨胀,衔接段把本技能精确嵌入 Light 流水线(m05/m02/db03/m06/a06/db09)并明确边界(指向原文问题移交 research-ethics)

## 缺点 / 可被质疑处
- 科研代码的'复现'被反复强调却没有可运行的种子固定资产:debug_protocol 列了 python random/numpy/torch/PYTHONHASHSEED/worker_init_fn/cudnn deterministic 六处,但骨架里没有一个 set_seed() 工具函数或 reproducibility fixture,agent 仍要每次手写,容易漏(尤其 PYTHONHASHSEED 必须在进程启动前设、DataLoader worker_init_fn 易忘)
- 骨架示例与科研内容脱节:stats.py 只是 mean() 空序列校验,test 只测算术平均,完全没演示技能反复强调的科研契约(loss单步下降、forward输出范围、save/load往返一致、assert_allclose、固定种子两次前向一致)。tdd_redflags 第三节讲得很好,但没有任何对应的可跑测试样例
- run_manifest.md 是 SKILL.md 明确承诺的 a03 标准交接工件(交 m06),但技能目录里没有它的模板或字段定义,只在 CONVENTIONS §6.1 提了命名,agent 要凭空造结构,跨技能交接一致性无保障
- 安全门是清单式而非可执行:SKILL/审查清单反复说不硬编码密钥/参数化查询/无鉴权要标注,但骨架 CI 里没有任何 secret 扫描或 bandit/pip-audit 步骤;light_skill_pack_maintenance 里那套 added-line 静态扫描(secret/shell=True/eval/pickle/SQL拼接)只用于维护 Light 仓库本身,没下放成给用户项目的可复用 gist
- ci.yml 与 README/SKILL 存在轻微不一致:ci.yml 触发分支是 branches:[main],而 SKILL 工程实践说'功能分支不直接推 main';且 ci.yml 没有 mypy 步骤(README 质量门和 pyproject 都配了 mypy,SKILL 也说 CI 加一步 mypy src),CI 实际没跑类型检查,自相矛盾
- SonarQube 这一节偏重:对绝大多数科研/单人项目 SonarQube+Quality Gate 是过重工具,正文用'必要时'带过但 references 给了完整篇幅,可能诱导 agent 在小项目里上重型平台,与'避免过度工程/YAGNI'的核心主张相左
- Poetry 路线只在 references 和 SKILL 文字里,骨架是纯 uv,Poetry 用户复制骨架后得自己改造 pyproject(build-system/group.dev),双路线承诺与单一资产之间有落差
- references.md 顶部声明 uv 0.11.19,但 conftest 注释承认'本环境无 uv,uv sync 路径未实测'——即推荐路线(uv sync)实际未在本机跑通,只测了 pip 退路,与'pytest 实跑通过'的宣传有口径差

## 可优化点（供后续逐技能优化）
- 在 scaffold 加 src/example/reproducibility.py:提供 set_global_seed(seed) 一次性固定 random/numpy/torch/PYTHONHASHSEED/cudnn,并提供 seed_everything fixture 和 dataloader worker_init_fn 模板,配 test 验证固定种子下两次调用结果一致——把反复强调的复现要求变成可复制资产
- 把 tdd_redflags 第三节的科研契约落成可跑测试样例文件(如 tests/test_model_contracts.py):演示 loss 单步下降、forward 输出范围、save/load 往返、assert_allclose、种子固定两次前向一致,让 agent 有 copy 模板而非只有文字指引
- 新增 run_manifest.md 模板(在技能目录或 templates/):固定字段=运行命令/环境(python+lock hash)/产物路径/关键指标/种子,与 m06 对齐,消除跨技能交接的结构随意性
- 把 light_skill_pack_maintenance 里的 added-line 静态扫描(secret/shell=True/eval/pickle/SQL拼接)抽成一个面向用户项目的可复用脚本 scripts/security_scan.py 并接入 scaffold CI,把'安全'从清单变成可执行 gate;同时在 ci.yml 加 pip-audit 或 bandit 步骤
- 修正 ci.yml 一致性:补 mypy src 步骤(与 README/pyproject 对齐),并把触发分支改为更通用的 on.pull_request + push 不限定 main 或明确注释'main 仅指 CI 触发,开发用功能分支',消除与 git 纪律的表面矛盾
- 给 Poetry 用户一个并行骨架变体或在 README 加'转 Poetry 的最小 diff'段(build-system 换 poetry-core、依赖搬到 group.dev、CI 换 poetry install),兑现双路线承诺
- 在本机或 CI 真跑通 uv sync 路径并更新 conftest/references 的实测声明,消除'推荐路线未实测、只测 pip 退路'的口径差;或诚实把 uv 标为'推荐但本环境未实跑',避免过度承诺
- 给 SonarQube 加明确适用边界(团队/长期维护/合规项目才上),并在正文 YAGNI 处呼应,防止 agent 在单人科研项目里上重型平台

## 与其他 Light 技能/知识库的衔接
["上游:实现 m05(方案/复现协议放行)与 m02(流水线);复用 db03 方法卡的 implementation_repo(HuggingFace/sklearn/xgboost/lightgbm/diffusers)而非造轮子","下游:产出供 m06 分析(标准工件 run_manifest.md);代码版本登记 db09;结构整理交 a06;系统级设计交 a04","论文复现专线:m05'复现已有论文协议'放行的任务由本技能落地,按其偏差预算与复现日志格式;复现失败三分归因中'实现差异'本技能继续逼近,'原文问题'移交 research-ethics 不在代码里轻率断言原文错","横向方法同源:复现日志'逐次只改一个变量'与本技能 systematic-debugging 的假设-验证同源","安全衔接:网络暴露接口无鉴权必须主动标注(security_awareness);敏感值不回显(a10)","元规则衔接:references.md 自任命为 GitHub Actions 版本真相源,a04/a06/tool-selection 的 action 版本以本节为准不各自复写;maintenance/manifest/selftest 三个 references 服务于 Light 技能包自身的 CI 治理(check_skills/check_skill_assets/run_skill_selftests 等 gate)而非用户项目"]

---

## GitHub 同类前沿技能对标

这一类对标对象分三档:(1)方法论框架——obra/superpowers 和 mattpocock/skills 是当下绝对头部(20万+/12万+ star),它们正是 light-backend-coding 方法论层显式对标的源头,提供 TDD、systematic-debugging、code-review、finishing-a-branch 等通用软件工程 skill,但都不针对科研/数据/模型场景,也不附带版本核验过的可跑骨架。(2)聚合目录——anthropics/claude-plugins-official、hesreallyhim/awesome-claude-code、VoltAgent/awesome-claude-code-subagents、karanb192/awesome-claude-skills 是索引型,覆盖面广但每个条目都浅,不是可直接执行的单一深度技能。(3)可跑资产——osprey-oss/cookiecutter-uv、drivendataorg/cookiecutter-data-science、manikosto/claude-code-python-stack 提供 uv/ruff/mypy/pytest 工程骨架或 Python 栈技能集,工程成熟度高于 Light 的 scaffold,但它们是纯模板或纯栈,缺少"审稿人视角的方法论 + 科研数值/shape/NaN/随机种子/数据泄漏加强"这条主线。Light 这个技能的差异化定位正是把"头部方法论 + 工程化骨架"两者缝合,并专门为科研 a03 执行阶段做本地加强和流水线衔接——这个交集目前在 GitHub 上几乎没有正面对手,但它的每一半都各自被远比它成熟、远比它热门的项目占据。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | Claude Code 的 agentic skills 框架 + 软件开发方法论,提供 TDD、systematic-debugging、code-reviewer、finishing-a-development-branch、subagent-driven-development 等成体系的 skill,是当前 agent skill 方法论的事实标准。 | 226112 | 2026-06-12 (pushed_at) | 强:方法论权威性、社区规模、持续高频更新,正是 Light 方法论层的对标源头。弱:完全面向通用软件工程,无科研/数据/模型场景的数值/shape/NaN/随机种子/数据泄漏加强,也不附带版本核验过的可跑 Python 骨架,不做科研流水线阶段衔接。 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Matt Pocock 直接从自己 .claude 目录开源的 'Skills for Real Engineers',包含 TDD、code-review、improve-codebase-architecture 等工程实践 skill,brief 中点名对标的五个 skill 来源之一。 | 127033 | 2026-06-13 | 强:实战工程师视角、极高人气、TypeScript/通用工程打磨深。弱:同样无科研场景本地加强、无可复现实验骨架、无 uv/Poetry 双路线与版本实测端点信息,不与论文/方案/分析阶段衔接。 |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Anthropic 官方维护的高质量 Claude Code 插件/skill 目录,含 skills、mcp 主题,是官方背书的能力分发入口。 | 30009 | 2026-06-13 | 强:官方权威、质量门槛、分发渠道。弱:是目录而非单一深度技能,不提供科研代码方法论细节,也没有针对数据/模型的可跑资产与 references 硬信息层。 |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 100+ 专业化 Claude Code subagent 合集,覆盖后端、测试、DevOps 等大量开发用例,含可直接复用的 agent 定义。 | 21681 | 2026-06-13 | 强:subagent 数量与覆盖面大、活跃。弱:偏 agent 角色定义罗列,深度有限,无版本核验的可跑骨架、无科研数值陷阱加强,也不是单一可执行的代码编写+审查技能。 |
| [drivendataorg/cookiecutter-data-science](https://github.com/drivendataorg/cookiecutter-data-science) | 数据科学界经典项目结构模板,规范 data/src/models/notebooks 等目录,主打可复现、可共享的数据科学工程结构。 | 9901 | 2026-06-12 | 强:数据科学项目结构事实标准、生态成熟、被广泛采用。弱:纯结构模板,无 AI agent 方法论、无 TDD/调试/审查决策要点,不内置 ruff/mypy/pytest 质量门实测,需要使用者自己补方法论。 |
| [osprey-oss/cookiecutter-uv](https://github.com/osprey-oss/cookiecutter-uv) | 现代 Python 项目模板(原 fpgmaas/cookiecutter-uv),内置 uv 依赖管理、ruff、mypy/ty、deptry、pytest+codecov、pre-commit、GitHub Actions、tox-uv、Docker、devcontainer。 | 1305 | 2026-06-08 | 强:工程化质量门覆盖比 Light scaffold 更全(deptry/tox/docker/devcontainer/PyPI 发布),社区验证充分。弱:纯工程模板,无科研场景加强、无 agent 方法论,不解决数值/shape/数据泄漏等研究代码特有问题。 |
| [karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills) | 50+ 经核验的 Claude Skills 精选目录,覆盖 TDD、debugging、git workflow、文档处理等,带 tdd/debugging 等主题标签,社区驱动。 | 375 | 2026-06-11 (updated_at; pushed_at 为 2025-10-21) | 强:索引清晰、主题标注到位、便于发现 TDD/调试类 skill。弱:索引型而非深度技能,本身不含可跑代码或方法论正文;pushed_at 显示内容自 2025-10 后基本未再扩充。 |
| [manikosto/claude-code-python-stack](https://github.com/manikosto/claude-code-python-stack) | 面向 Claude Code 的完整 Python 工具集:20 skills + 11 agents + 11 commands,覆盖 FastAPI、Django、SQLAlchemy、pytest、Allure、PostgreSQL、Redis、ClickHouse、Docker。 | 39 | 2026-06-12 (updated_at; pushed_at 2026-03-25) | 强:Python 后端工程栈技能数量多、覆盖 Web/DB/容器,定位最接近'Python 后端 skill 集'。弱:偏 Web 后端而非科研/模型,无数值/随机种子/数据泄漏加强,无版本核验的端点 references,star 与活跃度低。 |
| [shadowrootdev/awesome-agent-skills-mcp](https://github.com/shadowrootdev/awesome-agent-skills-mcp) | 以 MCP server 形式分发 100+ 来自 Anthropic、Vercel、Trail of Bits、Hugging Face 等的 agent skill,兼容 Claude、Copilot 及任意 MCP client。 | 23 | 2026-04-13 (pushed_at) | 强:以 MCP 协议跨客户端分发 skill 的思路新颖,聚合来源权威。弱:是 skill 分发管道而非单一深度技能,不针对科研代码,无可跑骨架与方法论正文,规模小、更新近两月停滞。 |
| [dawiddutoit/custom-claude](https://github.com/dawiddutoit/custom-claude) | 个人维护的 Claude Code skills/agents/plugins 合集,带 testing、quality-assurance、architecture、devops 等主题,结构上与 Light 这种'多技能包'最像。 | 1 | 2026-03-27 | 强:同为个人多技能包形态,含 testing/QA/architecture 主题,组织思路可参考。弱:几乎无人关注(1 star),无科研定位、无版本实测、无可复现骨架与流水线衔接,成熟度远低于 Light。 |
| [architsinghh/code-review-agent](https://github.com/architsinghh/code-review-agent) | 一个用 7 个链式工具自动化端到端 GitHub PR 代码审查的 MCP server,串联静态分析、覆盖率、模式匹配与 GitHub API。 | 0 | 2026-03-19 | 强:把'代码审查'做成可自动执行的 MCP 工具链,审查环节工程化程度高,可参考其静态分析+覆盖率串联思路。弱:只覆盖 PR review 单环节,不写代码、不做 TDD/调试、无科研加强,几乎无人使用(0 star)、近三月未更新。 |

### Light 该技能可借鉴的点
- 从 osprey-oss/cookiecutter-uv 借鉴把质量门做厚:在现有 ruff/mypy/pytest/pre-commit 基础上补 deptry(依赖健康)、tox-uv(多 Python 版本兼容)、devcontainer 与 Docker 化,让 scaffold 的工程完备度对齐主流模板。
- 从 architsinghh/code-review-agent 借鉴把'审查四法'落成可执行链路:静态分析→覆盖率→模式匹配→GitHub API 串联,可考虑把 Light 的代码审查方法论包成一个可调用的检查脚本/子流程,而不仅是文本决策要点。
- 从 obra/superpowers 与 mattpocock/skills 借鉴 subagent-driven-development 的拆解粒度和'finishing-a-development-branch'的收尾仪式感,把方法论 skill 进一步原子化,便于被 Light 编排器按阶段精确调用。
- 从 drivendataorg/cookiecutter-data-science 借鉴科研/数据项目专用目录约定(data/external|interim|processed、notebooks 命名规范),强化 scaffold 在'数据科学项目结构'这一 Light 已有但可更标准化的维度。
- 从 shadowrootdev/awesome-agent-skills-mcp 借鉴 MCP 分发思路:考虑让 light-backend-coding 的能力以 MCP/插件形式对外暴露,提升跨客户端复用与被发现度。
- 从 karanb192 与 VoltAgent 这类高 star 目录借鉴 README 的主题标签与可发现性运营(topics、清晰分类、对标声明),Light 在仓库层面可补充标准化的 skill 元数据以便外部检索引用。
