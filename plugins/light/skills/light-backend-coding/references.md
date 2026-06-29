# light-backend-coding 参考工具研究笔记

本文件为 `light-backend-coding` 技能的硬信息支撑。每个工具记录【是什么】【可复用方法/真实端点/参数】【链接】【已知坑/局限】。研究日期 2026-06。

> **可运行骨架**：同目录 `assets/project-scaffold/` 是按本笔记搭的最小可跑项目（`pyproject.toml` + `.pre-commit-config.yaml` + `.github/workflows/ci.yml` + 示例模块/测试）。2026-06 本机实跑 `python -m pytest` → 4 passed、`ruff check .` → All checks passed。
>
> **版本实测（2026-06，PyPI / GitHub API curl 核验，HTTP 200）**：ruff `0.15.16`、ruff-pre-commit tag `v0.15.16`、pre-commit-hooks tag `v6.0.0`、pytest `9.0.3`、uv `0.11.19`、`actions/checkout@v6`、`actions/setup-python@v6`、`actions/cache@v4` 均存在。骨架内 rev/版本据此锁定。

---

## systematic-debugging（系统化调试，obra/superpowers）

【是什么】一套"先定位根因再动手"的四阶段调试框架。核心铁律："ALWAYS find root cause before attempting fixes. Symptom fixes are failure." Phase 1 完成前禁止任何修复。

【可复用方法】
- **Phase 1 根因调查**（五步，缺一不可）：1) 逐字读错误信息/栈/行号；2) 稳定复现，复现不了就采集更多数据而非猜；3) 查最近改动（git diff、新依赖、配置/环境差异）；4) 多组件系统在每个组件边界加诊断埋点，一次跑下来定位是哪层断的；5) 反向追踪数据流，从坏值回溯到源头，在源头修而非症状处修。
- **Phase 2 模式分析**：在同一代码库找可工作的相似实现，完整读（不跳读），列出 working 与 broken 的每一处差异。
- **Phase 3 假设验证**：提单一具体假设"我认为 X 是根因因为 Y"，做最小改动一次只验一个变量；失败就换新假设，不要叠补丁。
- **Phase 4 实施**：先写失败测试 → 单一针对根因的修复 → 验证测试通过且无回归。
- **架构升级信号**：连修 3 次仍失败、每次修复牵出新耦合/新症状/需大重构 → 停手，这是结构问题不是 bug，回去和人讨论根本设计。
- 报告称系统化方法首次命中约 95% vs 乱试 40%，耗时 15-30 分钟 vs 2-3 小时。

【链接】https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md

【已知坑】时间压力下最容易跳过 Phase 1；警惕"先试试这个""问题很简单"这类合理化借口。

---

## test-driven-development（TDD，obra/superpowers）

【是什么】Red-Green-Refactor 循环。铁律："NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST."

【可复用方法】
- **RED**：写一个最小、单一行为、命名清晰的失败测试，尽量用真实代码而非 mock。**必须运行并亲眼看它失败**，确认是因功能缺失而失败（不是拼写错）。若立刻通过，说明在测已有行为，要修测试。
- **GREEN**：写让测试通过的最简实现，不加额外功能。再跑，确认新测试过且其他测试仍绿。新测试挂就修代码不修测试。
- **REFACTOR**：仅在绿灯后清理（去重、改名、抽函数），全程保持绿灯，本阶段不加新行为。
- 每个新函数/方法都要有一个"被看着失败过"的测试；bug 修复总是先写复现该 bug 的失败测试。
- 卡住时：先写断言、简化接口、mock 太多就用依赖注入、setup 复杂就抽 helper。
- 事后补的测试本质不同——回答"它做了什么"而非"它应该做什么"，偏向验证记得的边界而非发现新边界。

【链接】https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md

【已知坑】红旗信号：代码先于测试写、测试首跑就过、合理化例外、把先写的代码"留作参考"（应删掉重来）。

---

## requesting-code-review（请求代码审查，obra/superpowers）

【是什么】把变更交付给（子代理）审查者的标准流程。

【可复用方法】
- **请求前**：1) 提交工作入 git；2) 确定提交范围 base SHA 与 head SHA；3) 备好计划/规格。
- **提供给审查者**：变更摘要 `{DESCRIPTION}`、需求/计划 `{PLAN_OR_REQUIREMENTS}`、`{BASE_SHA}`、`{HEAD_SHA}`。只给精心构造的评审上下文，**不给会话历史**，让审查者聚焦交付物本身。
- **何时必审**：子代理开发每个任务后、完成大功能后、合并 main 前。可选：卡住时、重构前建基线、修完复杂 bug 后。
- **审查严重度分级**：Critical（立即修）/ Important（进入下个任务前修）/ Minor（记录待后）；输出还包括观察到的优点与整体就绪评估。
- **处理反馈**：先修 Critical+Important；审查者错时用代码/测试佐证地"技术性反推"；模糊处请求澄清。

【链接】https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md

【已知坑】别因"改动简单"跳过审查；别带着未解决的 Important 往下走。

---

## receiving-code-review（接收代码审查，obra/superpowers）

【是什么】接到审查意见后的处理流程。

【可复用方法】
- **六步分诊**：Read（先全收不反应）→ Understand（用自己话复述需求，不清就问）→ Verify（对照真实代码核实建议）→ Evaluate（判断对本项目是否技术成立）→ Respond（技术性确认或有理反推）→ Implement（逐条做、每条测）。
- **实施顺序**：Blocking（安全洞/功能坏）→ 简单修复（拼写、import）→ 复杂修复（重构、逻辑）。动手前先把不清楚的全部澄清。
- **回应规范**：技术化、动作导向；**禁止**"你说得太对了"式表演性赞同与道谢。用"Fixed. [简述改了什么]"或具体澄清问题。
- **评估外部反馈的五查**：对本库技术正确吗？会破坏现有功能吗？当前实现为何这么写？跨所有支持平台/版本可行吗？审查者有完整上下文吗？再加 YAGNI 检查：动手前 grep 实际用法，无人用就质疑该不该存在。
- 反推错了就如实更正"You were right - 我查了 X 确实 Y"，不长篇道歉。

【链接】https://github.com/obra/superpowers/blob/main/skills/receiving-code-review/SKILL.md

【已知坑】部分理解就动手会做错；澄清必须在实现前完成。

---

## improve-codebase-architecture（改进代码库架构，mattpocock/skills）

【是什么】把"浅模块"（接口几乎和实现一样复杂）改造成"深模块"（小接口藏大实现）的架构改进法，目标是可测性与 AI 可导航性。

【可复用方法】
- **关注的摩擦信号**：浅模块（低杠杆）；局部性破坏（为可测性抽出纯函数，但真 bug 藏在如何被调用里）；耦合跨缝泄漏；理解一个概念要在很多小模块间跳转；难测代码。
- **删除测试（Deletion Test）诊断**：设想整个删掉该模块——若复杂度消失，它是穿透层（浅，可吸收）；若复杂度在 N 个调用方重现，它在挣钱（深，提供真杠杆）。
- **重构策略**：合并穿透层；在缝处加深（接口藏更多实现）；建真缝（一个 adapter 是假设的缝，两个 adapter 才确认是真缝）；把知识集中到一处。
- **三阶段**：探索（先读领域上下文与既有架构决策 ADR，再有机走读记摩擦）→ 呈现候选（带 before/after 图，按 Strong/Worth exploring/Speculative 评级，每项列涉及文件、问题、方案、在局部性与杠杆上的收益）→ 拷问循环（和开发者走设计树：约束、依赖、模块形状、缝后是什么、哪些测试存活；决策落为 ADR）。
- 准则："接口即测试面"——测契约不测内部细节；既有 ADR 仅在摩擦真实可证时才挑战。

【链接】https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md

【已知坑】用有机探索而非死规则；过度抽小函数反而破坏局部性。

---

## subagent-driven-development（子代理驱动开发，obra/superpowers）

【是什么】把实现计划里每个任务派给一个全新、隔离的子代理，协调者绝不传整段会话上下文，只构造该子代理所需信息；每个任务做完走两阶段审查再前进。

【可复用方法】
- **准备**：一次读完计划文件抽出所有任务全文与上下文 → 建 TodoWrite → 记下共享上下文。
- **每任务循环**：1) 派实现子代理（给完整任务文本+相关上下文+全新上下文窗口）；2) 处理它开工前的提问；3) 实现（写代码+测试+自审+提交），回报四态之一：DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED；4) **规格符合性审查**（Stage 1，子代理查实现是否精确匹配规格，不多不少，有问题回修再审直至通过）；5) **代码质量审查**（Stage 2，仅在 Stage 1 通过后，查结构/命名/模式，同样回修循环）；6) 标 TodoWrite 完成下一任务。
- **全部任务后**：派最终审查子代理整体评估，再 finish development branch。
- **铁规**：审查不可乱序（规格必先于质量）；发现问题不可跳过复审循环；不可并行派多个实现子代理；不停下问用户是否继续——执行计划全部任务；按角色选最弱够用的模型（简单任务用便宜模型，架构/审查用强模型）。

【链接】https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md

【已知坑】传错/传多上下文会污染子代理隔离性；并行实现会引入冲突。

---

## finishing-a-development-branch（收尾开发分支，obra/superpowers）

【是什么】功能分支完工后的标准收尾流程。

【可复用方法】
- **合并前先跑测试**，测试不过就停："Cannot proceed with merge/PR until tests pass."
- **环境探测**：判断是普通 repo / 命名分支 worktree / 游离 HEAD，决定可用选项与清理方式。
- **基线分支识别**：用 merge-base 找分叉点（通常 main/master）或与开发者确认。
- **给出四个选项**：1) 本地合并（checkout base → pull → merge → 在合并结果上重跑测试）；2) push 并建 PR（带 tracking 推送，用 CLI 建 PR 附摘要与测试计划）；3) 保持原样；4) 丢弃（需手打 "discard" 确认）。
- **合并顺序关键**：先合并 → 在结果上验测试 → 再移除 worktree → 再删分支。顺序反了 `git branch -d` 会因 worktree 仍引用分支而失败。移除后跑 `git worktree prune` 自愈。
- **安全检查**：测试失败不合并；无明确确认不删工作；不删外部工具建的 worktree；无明确请求不 force-push。

【链接】https://github.com/obra/superpowers/blob/main/skills/finishing-a-development-branch/SKILL.md

【已知坑】选项 2/3 必须保留 worktree（PR 迭代要用）；清理只对选项 1/4 跑。

---

## GitHub Actions（CI）

【是什么】GitHub 原生 CI/CD，工作流 YAML 放在 `.github/workflows/*.yml`。

【可复用方法】
- 结构：`name`、`on`（push/pull_request 等触发）、`jobs`、`runs-on`（如 ubuntu-latest）、`steps`（`run` 跑命令 / `uses` 用 action）。
- **【GitHub Actions 版本真相源】**关键 action（截至 2026-06 均为 v6，经本 references 顶部「版本实测」GitHub API curl HTTP 200 核验）：`actions/checkout@v6`（拉代码）、`actions/setup-python@v6`（装指定 Python，`with: python-version: '3.13'` + `cache: "pip"`/`pipenv`/`poetry` 缓存依赖；缓存默认关闭，须显式开）。a04（system-design）模板/references 与 a06、tool-selection 等处的 action 版本均以本节为准，不各自复写版本号。
- `strategy.matrix.python-version: ["3.11","3.12","3.13"]` 并行多版本测试。
- 最小 Python CI：checkout → setup-python(cache) → 装依赖 → `ruff check .` → `pytest`。
- 缓存 pre-commit：`actions/cache@v4` path `~/.cache/pre-commit`，key 含 Python 版本 + `hashFiles('.pre-commit-config.yaml')`。

【链接】https://docs.github.com/en/actions/writing-workflows/quickstart

【已知坑】secrets 用 `${{ secrets.X }}` 注入，勿硬编码；matrix 会成倍消耗运行时长。

---

## Ruff（极快的 Python linter + formatter，Astral）

【是什么】Rust 写的 Python linter+formatter，一个工具替代 flake8/isort/black/pyupgrade 等。

【可复用方法】
- 配置文件：`pyproject.toml` 下 `[tool.ruff]`，或 `ruff.toml`/`.ruff.toml`（后者无 `tool.ruff` 前缀）。优先级 `.ruff.toml` > `ruff.toml` > `pyproject.toml`，不跨文件合并，用 `extend` 继承父配置。
- 默认规则：仅 Pyflakes(`F`) + 部分 pycodestyle，即 `select = ["E4","E7","E9","F"]`；默认**不**开 `W` 与 McCabe `C901`。
- 选规则：`[tool.ruff.lint]` 下 `select`（全量设定）/ `extend-select`（叠加，如加 `B` bugbear）/ `ignore`（如 `E501` 行长）。
- `[tool.ruff]`：`line-length = 88`、`indent-width = 4`、`target-version = "py310"`（不写则从 `requires-python` 推断）。
- `[tool.ruff.format]`：`quote-style="double"`、`indent-style="space"`、`skip-magic-trailing-comma=false`。
- 命令：`ruff check path/`（`--fix` 自动修，`--diff` 看变更）；`ruff format path/`（`--check` 干跑）。
- `[tool.ruff.lint.per-file-ignores]`：如 `"__init__.py" = ["E402"]`、`"**/{tests,docs}/*" = ["E402"]`。

【链接】https://docs.astral.sh/ruff/configuration/ ， linter 规则 https://docs.astral.sh/ruff/linter/

【已知坑】`# noqa` 可被 `--ignore-noqa` 忽略；linter 与 formatter 是两个独立命令，CI 里都要跑。

---

## pre-commit（多语言 git 钩子框架）

【是什么】管理 git pre-commit 钩子的框架，提交时自动跑 lint/format/检查。

【可复用方法】
- 安装：`pip install pre-commit` → `pre-commit install`（在 `.git/hooks/pre-commit` 装脚本）。
- 配置 `.pre-commit-config.yaml`（项目根）：顶层 `repos` 列表 + 可选 `default_language_version`/`fail_fast`/`files`/`exclude`/`minimum_pre_commit_version`。每个 repo 含 `repo`(URL 或 `local`/`meta`) + `rev`(不可变 tag/SHA 锁版本) + `hooks`(每项 `id` 必填，可选 `args`/`files`/`types`/`stages`/`additional_dependencies`)。
- 接 Ruff：`repo: https://github.com/astral-sh/ruff-pre-commit`，`rev: vX.Y.Z`，hooks `id: ruff`(`args: [--fix]`) + `id: ruff-format`。
- 运行：`pre-commit run`（已暂存文件）/ `pre-commit run --all-files`（全库，CI 常用）/ `pre-commit run <hook_id>` / `--from-ref origin/HEAD --to-ref HEAD`（只查 diff）。
- 升级：`pre-commit autoupdate`（更新 rev 到各 repo 最新 tag，`--freeze` 存完整 SHA）。
- CI：跑 `pre-commit run --all-files`；缓存 `~/.cache/pre-commit`（`PRE_COMMIT_HOME`/`XDG_CACHE_HOME` 覆盖）；有官方 action 与 pre-commit.ci。

【链接】https://pre-commit.com/ ， 仓库 https://github.com/pre-commit/pre-commit

【已知坑】`rev` 务必锁版本（用 tag/SHA），不要用浮动分支；钩子环境隔离，额外依赖走 `additional_dependencies`。

---

## pytest（Python 测试框架）

【是什么】Python 主流测试框架，自动发现 + 纯 `assert` 内省。

【可复用方法】
- 发现：文件 `test_*.py`/`*_test.py`，函数/方法 `test_*` 自动收集。
- 断言：直接 `assert x == y`，pytest 重写 assert 给详细失败信息，无需特殊断言方法。
- **fixture**：`@pytest.fixture` 装饰，测试以参数声明依赖注入；scope 有 `function`(默认)/`class`/`module`/`session`。
- **参数化**：`@pytest.mark.parametrize("input,expected", [(1,2),(3,4)])` 一个测试多组输入。
- **conftest.py**：放共享 fixture/hook，同目录及子目录自动可用，无需 import。
- 运行：`pytest`、`-v`(详)、`-x`(首失败即停)、`-k "表达式"`(按名筛)、`-m marker`(按标记)、`pytest path/test_file.py`。
- 标记：`@pytest.mark.slow` 等自定义标记需在 `pyproject.toml`/`pytest.ini` 注册避免警告。
- 覆盖率：装 `pytest-cov`，`pytest --cov=my_package --cov-report=term-missing` 看未覆盖行；`--cov-report=xml` 出 `coverage.xml` 供 SonarQube。

【链接】https://docs.pytest.org/en/stable/how-to/index.html

【已知坑】fixture scope 选错会泄漏状态；未注册的自定义 marker 触发警告。

---

## SonarQube（静态分析与质量门）

【是什么】静态分析平台，查 bug、安全漏洞、code smell、重复率，跟踪覆盖率，用 Quality Gate 卡阈值。

【适用边界】SonarQube 是重型基建（服务器/SonarCloud 账号、token、scanner、Quality Gate 维护），不是默认起手项。**值得上**：多人团队、长期维护的代码库、有合规/审计要求（需可追溯的质量与安全门）。**别急着上**：单人脚本、一次性实验、短命原型——本地 `ruff` + `mypy` + `pytest --cov` 已覆盖绝大部分价值，加 SonarQube 是徒增维护面（呼应 SKILL 的 YAGNI：必要时才上）。

【可复用方法】
- 配置 `sonar-project.properties`（项目根）：`sonar.projectKey`(唯一标识)、`sonar.organization`(SonarCloud 必填)、`sonar.sources`(源目录如 `src` 或 `.`)、`sonar.tests`(测试目录)、`sonar.host.url`(如 https://sonarcloud.io)、`sonar.token`(认证 token)。
- Python 覆盖率：`sonar.python.coverage.reportPaths=coverage.xml`（先 `coverage xml` 或 `pytest --cov-report=xml` 生成）。
- 运行：项目根执行 `sonar-scanner`，读 properties 分析后上报服务器。
- **Quality Gate**：一组阈值条件（如新代码无新 bug、覆盖率 > X%、无新安全热点），不过则分析标记为未达标，可在 CI 阻断合并/部署。
- GitHub Action：`SonarSource/sonarqube-scan-action`，env 注入 `SONAR_TOKEN`、`SONAR_HOST_URL`。

【链接】https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/analysis-parameters/ ， scanner 文档 https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/scanners/sonarscanner/

【已知坑】官方 docs 多个旧 URL 已 404/重定向；属性名以本笔记为准（`sonar.python.coverage.reportPaths` 针对 Python）。token 走 secrets，勿提交。

---

## uv（极快 Python 包与项目管理器，Astral）

【是什么】Rust 写的 Python 包/项目管理器，号称替代 pip、pip-tools、pipx、poetry、pyenv、twine、virtualenv，比 pip 快 10-100x。

【可复用方法】
- 项目：`uv init`(脚手架)、`uv add <pkg>`(加依赖，自动建 venv+解析+装)、`uv remove`、`uv lock`(生成/更新锁文件)、`uv sync`(按锁文件精确安装)、`uv run <cmd>`(项目环境内运行)。
- 文件：`pyproject.toml`(元数据/依赖) + `uv.lock`(通用可复现锁文件)。
- venv：`uv venv`（`--python 3.12.0` 指定版本）。
- pip 兼容：`uv pip compile`(锁，`--universal` 跨平台)、`uv pip sync`、`uv pip install`(drop-in 替代)。
- Python 版本：`uv python install 3.10 3.11 3.12`、`uv python pin 3.11`(写 `.python-version`)。
- 工具：`uvx <tool>`(= `uv tool run`，临时环境跑 CLI)、`uv tool install <pkg>`(全局装)。
- 脚本：`uv add --script file <pkg>` 写内联依赖元数据，`uv run script.py` 隔离环境跑。

【链接】https://docs.astral.sh/uv/

【已知坑】生态较新；`uv.lock` 是 uv 专有格式（非 requirements.txt），CI 用 `uv sync` 复现。

---

## Poetry（Python 依赖管理与打包）

【是什么】Python 依赖管理 + 打包工具，含锁文件做可复现安装、可构建分发。需 Python 3.10+。

【可复用方法】
- 命令：`poetry new`(脚手架)、`poetry init`(交互建 pyproject)、`poetry add`(加依赖并装)、`poetry install`(按锁文件装)、`poetry update`(更新到允许的最新并刷新锁)、`poetry lock`(只解析锁不装)、`poetry run`(虚拟环境内执行)、`poetry build`、`poetry publish`。
- 文件：`pyproject.toml`(清单) + `poetry.lock`(锁定精确版本)。Poetry 2.0 起依赖推荐放 PEP 621 的 `[project.dependencies]`（旧版用 `[tool.poetry.dependencies]`）。
- 依赖分组：`[tool.poetry.group.*]`（如 dev 组）。
- 版本约束：PEP 440，支持 `^`(caret)、`~`(tilde)、`*`、精确、不等，例 `requests = "^2.13.0"`。
- venv：默认每项目自动建隔离 venv，`poetry env` 子命令管理。
- 安装 Poetry 本身：`pipx install poetry` 或官方 installer；CI 里固定版本如 `pipx install poetry==2.0.0`。

【链接】https://python-poetry.org/docs/ ， 命令 https://python-poetry.org/docs/cli/

【已知坑】`^` caret 约束可能拉入意外的次版本更新；Poetry 应装在独立 venv 隔离；2.0 前后依赖声明位置不同需注意。
