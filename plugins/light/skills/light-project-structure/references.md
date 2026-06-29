# references — light-project-structure 工具与方法笔记

逐个核查过的参考工具/项目/API 的硬信息。研究日期 2026-06-06。
每条含【是什么】【可复用方法/真实端点/参数】【链接】【已知坑/局限】。

---

## repo-intake-and-plan（AI 论文复现技能套件）

【是什么】lllllllama 的 `ai-paper-reproduction-skill` 套件中的首个技能。对一个陌生仓库（尤其是文档散乱的学术 ML repo）做自动化首遍体检，产出"最安全的复现路径"计划。

【可复用方法】
- 工作流三步：①读 README 抽取高层信息；②扫描 setup 脚本与文档化命令，定位安装/运行方式；③把工作流分类为 inference / training / evaluation 三类管线。
- 保守分类（classification errs on the side of caution）：宁可标注为更安全的路径，不冒进。
- 输出"喂给 orchestrator"：plan 本身不做执行决策，只给编排器决策依据。
- 借鉴点：整理已有项目时，先 README→setup 脚本→命令清单，再按"推理/训练/评估"给已有 src 分门别类。

【链接】https://claudemarketplaces.com/skills/lllllllama/ai-paper-reproduction-skill/repo-intake-and-plan
安装：`npx skills add https://github.com/lllllllama/ai-paper-reproduction-skill --skill repo-intake-and-plan`

【已知坑】只做"读+计划"，不执行、不搭环境、不挑目标；面向 ML 复现场景，对非研究仓库针对性弱。

---

## env-and-assets-bootstrap（AI 论文复现技能套件）

【是什么】同套件第二个技能，负责"选定论文→真正跑代码"之间的环境搭建阶段。

【可复用方法】
- 产出保守的 conda 环境创建命令（conservative conda commands）。
- 映射资产位置：明确 checkpoint 与 dataset 应当落在哪个目录。
- 提前识别缺失依赖、提前暴露资产来源问题（如缺 CUDA toolkit），避免浪费数小时训练后才发现。
- 对自己解决不了的问题"诚实声明无法自动解决"，不假装搞定。
- 借鉴点：本技能 bootstrap 阶段应同时产出"环境创建命令 + data/models 资产目录布局 + 依赖缺口清单"，并对无法自动解决的项如实标注。

【链接】https://claudemarketplaces.com/skills/lllllllama/ai-paper-reproduction-skill/env-and-assets-bootstrap

【已知坑】只管执行前的搭建，本身不跑模型；以 conda 为主。

---

## minimal-run-and-audit（AI 论文复现技能套件）

【是什么】同套件第三个技能，负责"跑一次 + 记录发生了什么"的执行与归档阶段。

【可复用方法】
- 五步：执行预先确定的命令（smoke test 或文档化的推理命令）→ 捕获输出 → 判定 success/failure → 把标准化文件写进 `repro_outputs/` 目录 → 改动文件时生成 `PATCHES.md` 记录补丁。
- 完整产出清单（核对自 SKILL.md）：`repro_outputs/` 标准化文件 + `SCIENTIFIC_CHANGELOG.md`（记录科学含义被改动处及证据状态）+ `COMPARABILITY_REPORT.md`（与 README/论文/baseline 的可比性）+ `PATCHES.md`（仅当 repo 文件被改时）；并明确区分 verified / partial / blocked 三态。
- 范围克制：只记录"发生了什么"，不分析正确性、不做深度验证；核心要求是"保住科学含义、最小化语义改动、记录假设/阻塞/证据"。
- 借鉴点：复现/审计实验时固定一个 `repro_outputs/` 归档目录，每次跑都落"verified/partial/blocked 三态标记 + 输出 + PATCHES.md（改了哪些文件）+ 假设与阻塞清单"，保证可追溯。

【链接】https://claudemarketplaces.com/skills/lllllllama/ai-paper-reproduction-skill/minimal-run-and-audit

【已知坑】不帮你选目标、不搭环境；只做"跑了就记"。

---

## handoff skill（claude-handoff 插件）

【是什么】willseltzer 的 claude-handoff 插件（MIT）。生成结构化 `HANDOFF.md`，让任意 AI agent 接续上一会话——跨工具、跨上下文窗口续作。

【可复用方法】
- 命令：`/handoff:create`（完整）/ `/handoff:quick`（最简）生成 HANDOFF.md；`/handoff:resume` 在新会话续作（会先检查 repo 是否漂移）。非 Claude agent 直接读 HANDOFF.md。
- HANDOFF.md 必含字段：Goal / Completed-NotYetDone（勾选清单）/ **Failed Approaches（强制，最有价值）** / Key Decisions（表格化，含理由）/ Current State（含真实报错）/ Code Context（贴签名而非泛描述）/ Resume Instructions（编号步骤）/ Setup Required（env var、测试数据、前置）/ Warnings（坑与约束）。
- 关键准则：失败的尝试必须写；贴代码签名而非含糊描述；测试步骤带预期结果（如具体状态码/响应体）；报错带行号。
- 借鉴点：项目整理结束时产出的"文件归位说明"可借用此结构，尤其"Key Decisions 表格 + Failed Approaches"两节。

【链接】https://github.com/willseltzer/claude-handoff
安装：`/plugin marketplace add willseltzer/claude-handoff` 然后 `/plugin install handoff`

【已知坑】为编码会话续作设计；HANDOFF.md 需要人/agent 主动维护，过期会误导。

---

## to-issues（mattpocock/skills，engineering 分类）

【是什么】Matt Pocock 的 `to-issues` 技能（注意：仓库内实际命名为 `to-issues`，路径 `skills/engineering/to-issues`，非 "prd-to-issues"）：把任意 plan/spec/PRD 拆成可独立认领的 GitHub issues。上游有配套 `to-prd` 技能，把当前对话上下文转成 PRD 并作为 issue 提交，再喂给 `to-issues`。

【可复用方法】
- 核心方法：垂直切片（vertical slices）拆解——官方描述原文 "Break any plan, spec, or PRD into independently-grabbable GitHub issues using vertical slices"。每个 issue 是一条贯穿所有集成层（前端/后端/DB）的端到端完整路径，而非横向按技术层切（"先建表""再做 UI"）。
- 每个 issue 特征：可独立认领（independently-grabbable），可单独实现合并不阻塞其他切片。
- 借鉴点：把项目整理动作转成任务列表时，按"可独立完成 + 带验收标准 + 标依赖顺序"组织，而不是一锅烩。
- 安装：`npx skills add https://github.com/mattpocock/skills --skill to-issues`

【链接】https://github.com/mattpocock/skills （SKILL.md：`skills/engineering/to-issues/SKILL.md`）

【已知坑】面向软件交付 PRD，纯文档/数据整理类任务的"垂直切片"语义需自行映射；acceptance criteria / 依赖排序的细节在 SKILL.md 内，README 仅给一行摘要。

---

## writing-plans（obra/superpowers）

【是什么】superpowers 技能库中的实现计划编写技能。在设计获批后激活，产出"小到一口能吃下"的任务计划。

【可复用方法】
- 任务粒度：每个任务估时 2–5 分钟。
- 每个任务必含：精确文件路径 + 完整代码 + 验证步骤。
- 写作目标读者设定为"热心但无判断力、无项目上下文、抗拒测试的初级工程师"也能照做——逼出绝对明确、无歧义的步骤。
- 原则：TDD、YAGNI、DRY。
- 整体工作流顺序：brainstorming（苏格拉底式精炼，存设计文档）→ using-git-worktrees → writing-plans → executing-plans/subagent-driven-development → TDD → requesting-code-review → finishing-a-development-branch。
- 借鉴点：整理项目时先出"精确路径 + 具体动作 + 验证步骤"的计划再执行；命名/归位决策写到可被无上下文者照做的程度。

【链接】https://github.com/obra/superpowers

【已知坑】README 中并无 repo-intake / to-issues 技能（那些来自别的仓库，勿混淆）；超细粒度计划对小任务可能过重。

---

## Cookiecutter Data Science (CCDS)

【是什么】DrivenData 维护的数据科学项目脚手架，"逻辑化、合理标准化但灵活"的目录结构标准。需 Python 3.9+。

【可复用方法/真实命令】
- 安装与使用：`pipx install cookiecutter-data-science`（推荐），然后跑 `ccds` 交互生成项目。
- 生成的目录结构（v2）：
  - `data/raw/`（原始不可变数据）`data/interim/`（中间转换）`data/processed/`（建模用最终数据集）`data/external/`（第三方源）
  - `<module_name>/`（源码包）下：`config.py`、`dataset.py`（下载/生成数据）、`features.py`（特征）、`modeling/train.py`、`modeling/predict.py`、`plots.py`
  - `models/`（序列化模型/预测）`notebooks/`（命名约定：编号+缩写+描述，如 `1.0-jqp-initial-exploration`）
  - `references/`（数据字典/手册）`reports/` 与 `reports/figures/`（生成的图）`docs/`（MkDocs）
  - `Makefile`（如 `make data` / `make train`）`pyproject.toml`、`requirements.txt`、`setup.cfg`（flake8）、`LICENSE`、`README.md`
- 可选集成（生成时选择）：依赖管理 virtualenv/conda/pipenv/uv/pixi/poetry；依赖文件 requirements.txt/pyproject.toml/environment.yml/Pipfile/pixi.toml；lint ruff 或 flake8+black+isort；数据存储 none/S3/GCS/Azure；测试 none/pytest/unittest；文档 mkdocs/none；license MIT/BSD-3/none。
- 借鉴点：本技能 data/ 四分层（raw/interim/processed/external）、figures 放 reports/figures、notebooks 编号命名约定均源自 CCDS，可直接对齐。

【链接】https://cookiecutter-data-science.drivendata.org/ ；仓库 https://github.com/drivendataorg/cookiecutter-data-science

【已知坑】CCDS 把 figures 放在 `reports/figures/`、源码放顶层模块包，与本技能的 `figures/`、`src/` 命名略有差异，对齐时需注明取舍。

---

## DVC (Data Version Control)

【是什么】数据/模型版本控制工具，与 Git 互补：Git 管文本元数据，DVC 管大文件本体。

【可复用方法/真实命令】
- `git init` 后 `dvc init`：生成 `.dvc/config`、`.dvc/.gitignore` 等（这些要 commit）。
- `dvc add data/data.xml`：把数据移入缓存，生成 `data/data.xml.dvc`（含 md5 哈希+路径的小文本文件），并自动把原文件加进 `.gitignore`。提交：`git add data/data.xml.dvc .gitignore && git commit`。
- 远端：`dvc remote add -d storage s3://mybucket/dvcstore`（支持 S3/GCS/Azure/SSH/本地目录）；`dvc push` 上传缓存，`dvc pull`（通常在 `git pull`/`clone` 后）下载。
- 管线：`dvc.yaml` 声明多阶段管线（stage 字段：`cmd` 必填、`deps`、`params`（从 params.yaml 取字段名）、`outs`（可带子字段 `cache`/`remote`/`persist`/`push`/`desc`）、`metrics`、`plots`，另有 `wdir`/`frozen`/`always_changed`/`meta`/`desc`）；`dvc.lock` 记录各依赖与产物的精确哈希（md5/etag/checksum）+ 完整 param 键值。`dvc repro` 只重跑依赖/参数变了的阶段（带 run-cache 跳过未变阶段）；`frozen: true` 的阶段在 repro 时被跳过。
- 实验：`dvc exp run` / `exp show`（表格）/ `exp diff` / `exp apply` / `exp branch`（提升为 git 分支）/ `exp push|pull`。
- 版本回切：`git checkout HEAD~1 data/data.xml.dvc && dvc checkout`。
- 入 Git 的：`*.dvc`、`dvc.yaml`、`dvc.lock`、`.dvc/config`；进 .gitignore 的：大数据文件、模型二进制、数据目录（DVC 自动写）。

【链接】https://dvc.org/doc/start （现重定向 https://doc.dvc.org/start）

【已知坑】"DVC 本身不是版本控制系统"——它操纵 .dvc 文件，真正的版本由 Git 提交的 .dvc 内容定义；忘记 `dvc push` 会导致他人 `dvc pull` 拿不到数据。

---

## Poetry

【是什么】Python 依赖管理与打包工具，靠 `pyproject.toml` + `poetry.lock` 实现可复现安装。

【可复用方法/真实命令】
- `poetry init`（在已有目录交互生成 pyproject.toml）/ `poetry new`（脚手架新项目）。
- `poetry add pendulum`：自动选版本约束并安装，写入 pyproject.toml + 更新 poetry.lock。
- `poetry install`：无 lock 时解析依赖并生成 lock；有 lock 时按 lock 精确版本装，保证全员一致。`--no-root` 跳过安装本项目。
- `poetry update`：拉取约束内最新版并重生成 lock（≈删 lock 再 install）。
- `poetry run python x.py` / `poetry run pytest`：在虚拟环境内执行。
- `poetry build` / `poetry publish`：打包发布（仅 package mode）。
- 配置：`[project]`（PEP 621：name/version/requires-python/dependencies）+ `[build-system]`（poetry-core）+ `[tool.poetry]`（Poetry 专属：packages/include/exclude/source）。`package-mode = false` 进入非打包模式（只管依赖，name/version 可选）。
- 依赖分组：`[tool.poetry.group.dev.dependencies]` 等把 dev/test/docs 与生产依赖分开。
- 锁定原理：首次 install 解析全部传递依赖→下载兼容版本→把每个包精确版本写进 poetry.lock；"universal locking" 保证在 requires-python 跨版本都可装。
- 提交建议：应用开发者应提交 poetry.lock（CI/生产/团队一致）；库开发者权衡。lock 与 pyproject.toml 不同步时 Poetry 会告警。
- 虚拟环境默认在 `{cache-dir}/virtualenvs`，可设 `virtualenvs.in-project` 放项目内。

【链接】https://python-poetry.org/docs/basic-usage/

【已知坑】Poetry 2.x 用 PEP 621 的 `[project]` 表，旧教程的 `[tool.poetry.dependencies]` 写法已变；与 conda 混用时需先激活 conda 环境再跑 poetry。

---

## Ruff

【是什么】Astral 用 Rust 写的极快 Python linter + formatter，单二进制替代 flake8 + black + isort。

【可复用方法/真实配置】
- 命令：`ruff check`（lint，`--fix` 自动修，`--select`/`--ignore` 覆盖规则，`--output-format` json/github/sarif）；`ruff format`（`--check` 干跑、`--diff`、`--line-length`）。
- 配置位置：`pyproject.toml` 的 `[tool.ruff]`，或 `ruff.toml`/`.ruff.toml`（无前缀）。同目录优先级 `.ruff.toml` > `ruff.toml` > `pyproject.toml`。
- 顶层：`line-length = 88`（同 black）、`indent-width = 4`、`target-version = "py310"`（可由 requires-python 推断）。
- `[tool.ruff.lint]`：`select = ["E4","E7","E9","F"]`、`ignore = ["E501"]`、`fixable = ["ALL"]`、`unfixable`。
- 规则集：E=pycodestyle 错误、F=Pyflakes（未用 import/未定义名）、B=bugbear、I=isort、W=pycodestyle 警告（默认不开）、Q=quotes、C901=McCabe 复杂度（默认不开）。
- `[tool.ruff.lint.per-file-ignores]`：如 `"__init__.py" = ["E402"]`、`"**/{tests,docs,tools}/*" = ["E402"]`。
- `[tool.ruff.format]`：`quote-style = "double"`、`indent-style = "space"`、`docstring-code-format`。
- 配置发现是分层的，不跨层合并，用 `extend` 继承父配置；CLI flag/`--config "k=v"` 优先级最高。

【链接】https://docs.astral.sh/ruff/configuration/

【已知坑】与 flake8 不同，Ruff 默认不开 W 警告和 C901 复杂度，需显式 select；配置不跨层 merge，多目录项目易踩。

---

## pre-commit

【是什么】多语言 git hook 管理框架，提交前自动跑 linter/formatter，不需要 root。

【可复用方法/真实配置】
- 安装：`pip install pre-commit`；`pre-commit install`（写 `.git/hooks/pre-commit`，每次提交自动触发）；`pre-commit run --all-files`（首次加 hook 时全量跑）。
- `.pre-commit-config.yaml` 结构：顶层 `repos` 列表，每项含 `repo`（git URL，或哨兵 `local`/`meta`）、`rev`（tag/SHA，应不可变）、`hooks`（每个含 `id`，可加 `args`/`files`/`exclude`/`types`/`stages`/`additional_dependencies` 等）。其他顶层键：`default_language_version`/`default_stages`/`fail_fast`/`files`/`exclude`/`minimum_pre_commit_version`。
- 常用通用 hook（来自 pre-commit/pre-commit-hooks）：`trailing-whitespace`、`end-of-file-fixer`、`check-yaml`。
- 集成 Ruff（repo `astral-sh/ruff-pre-commit`）：
  ```yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  ```
  Ruff 作为预编译二进制随 hook 系统自动装，无需本地 Rust。
- `pre-commit autoupdate`：把各 repo 的 `rev` 更到最新 tag；`--freeze` 存解析出的 commit hash（带 `# frozen: vX.Y.Z` 注释）；`--repo REPO` 只更某仓库。

【链接】https://pre-commit.com/ ；hooks 仓库 https://github.com/pre-commit/pre-commit-hooks

【已知坑】`rev` 应固定到不可变 tag/SHA 保证可复现；首次接入老项目跑 `--all-files` 可能一次性改动大量文件。

---

## EditorConfig

【是什么】跨编辑器/IDE 统一代码风格的配置系统，由 `.editorconfig` 文件 + 编辑器插件两部分组成。INI 风格（兼容 Python configparser），UTF-8 编码。

【可复用方法/真实配置】
- `root = true`：放文件顶部（section 外），告诉编辑器停止向父目录继续搜 .editorconfig。
- section 用文件 glob：`*`（除路径分隔符外任意串）、`**`（含 `/`）、`?`、`[name]`/`[!name]`、`{s1,s2}`、`{num1..num2}`。大小写敏感，只用正斜杠。
- 关键属性：`indent_style`（tab/space）、`indent_size`、`tab_width`、`end_of_line`（lf/cr/crlf）、`charset`（utf-8 等）、`trim_trailing_whitespace`、`insert_final_newline`。属性/值大小写不敏感；设 `unset` 取消某属性。
- 典型：
  ```ini
  root = true
  [*]
  charset = utf-8
  end_of_line = lf
  insert_final_newline = true
  trim_trailing_whitespace = true
  indent_style = space
  indent_size = 4
  [*.{yml,yaml,json}]
  indent_size = 2
  [Makefile]
  indent_style = tab
  ```
- 优先级：从打开文件目录向上搜直到 root 或文件系统根；自上而下读，离源文件更近（更晚读）的规则胜出。

【链接】https://editorconfig.org/

【已知坑】Makefile 必须用 tab，要单列 section 覆盖；部分编辑器需装插件才生效。

---

## Makefile / Taskfile（任务运行器取舍）

【是什么】两种"项目任务运行器"。Makefile 是经典 DSL（tab 敏感）；Taskfile（Task，Go 写的单二进制）用 YAML 定义任务，跨平台。

【可复用方法/真实配置】
- Taskfile.yml 结构：顶层 `version: '3'`；`tasks:` 下每个任务含 `desc`、`cmds`（顺序执行的命令列表）、`deps`（并行先跑的依赖）、`vars`（静态或 `sh:` 动态取 shell 输出）。
- up-to-date 检查：声明 `sources:` 与 `generates:`，用 checksum（默认，内容哈希）或 timestamp 判定是否跳过；也可用 `status:`（命令全返回 0 即视为最新）。
- Task CLI：`task`（默认任务）、`task build`、`task -l`（列任务）、`task -w`（watch 重跑）、`task --dry`、`task -f`（强制）、`task -p`（并行）；`task deploy ENV=prod` 传变量；`task yarn -- install` 经 `{{.CLI_ARGS}}` 转发。
- Make vs Task：Make 是自定义 DSL、tab 敏感、依赖系统已装 make、跨 OS shell 有差异、靠文件 mtime 判定、`make -j` 并行；Task 是 YAML 可读、Go 单二进制无依赖、内置 watch、checksum 缓存、`deps` 自动并行、`includes:` 带命名空间、`internal: true` 隐藏任务、原生 `for` 循环与 `platforms:` 平台过滤。
- 借鉴点：CCDS 默认给 Makefile（`make data`/`make train`）。本技能可二选一：团队已用 make 就给 Makefile；要跨平台（含 Windows）一致、可读性优先就给 Taskfile。

【链接】https://taskfile.dev/usage/ ；GNU Make https://www.gnu.org/software/make/manual/

【已知坑】Makefile 的 tab 敏感与跨 OS shell 差异是常见坑（Windows 上尤甚）；Task 需额外安装二进制，团队需统一。

---

## .gitignore 最佳实践（GitHub Python 模板）

【是什么】GitHub 官方 `Python.gitignore` 模板，社区共识的 Python 项目忽略清单。

【可复用方法/真实条目】
- 字节码：`__pycache__/`、`*.py[codz]`、`*$py.class`
- 打包/分发：`build/`、`dist/`、`*.egg-info/`、`*.egg`、`.eggs/`、`wheels/`、`sdist/`、`var/`、`.installed.cfg`、`MANIFEST`
- 虚拟环境：`.env`、`.venv`、`env/`、`venv/`、`ENV/`、`env.bak/`、`venv.bak/`
- 测试/覆盖率：`htmlcov/`、`.tox/`、`.nox/`、`.coverage`、`.coverage.*`、`coverage.xml`、`.pytest_cache/`、`.hypothesis/`
- Jupyter/IPython：`.ipynb_checkpoints`、`profile_default/`、`ipython_config.py`
- 类型检查缓存：`.mypy_cache/`、`.dmypy.json`、`.pyre/`、`.pytype/`
- 工具缓存：`.ruff_cache/`；Sphinx：`docs/_build/`
- IDE（默认注释，按需开）：`# .idea/`、`# .vscode/`
- 锁文件（模板里默认注释，按项目类型决定是否提交）：pipenv/uv/poetry/pdm/pixi 的 lock。应用项目通常提交 lock，故不要忽略。
- 科研补充建议：`data/` 大文件交给 DVC（DVC 会自动写 .gitignore），不要直接 git 跟踪；`models/*.ckpt`、`*.pth`、`logs/`、`wandb/`、`mlruns/` 视情况忽略。

【链接】https://github.com/github/gitignore/blob/main/Python.gitignore

【已知坑】lock 文件该不该忽略取决于项目类型（应用提交、库权衡），别盲目 ignore；DVC 管理的数据目录交给 DVC 自动写忽略，别和 .gitignore 手写规则冲突。

---

## 研究覆盖说明

本批 14 个参考全部于 2026-06-06 重新对照官方文档/仓库逐条核实，无编造端点。
6 个技能/工作流（repo-intake-and-plan、env-and-assets-bootstrap、minimal-run-and-audit、handoff、to-issues、writing-plans）+ 8 个工具/规范（CCDS、DVC、Poetry、Ruff、pre-commit、EditorConfig、Makefile/Taskfile、.gitignore）。

核实中纠正/补强：
- mattpocock 技能实际命名为 `to-issues`（路径 `skills/engineering/to-issues`），原"prd-to-issues"为误记；上游配套 `to-prd`。
- minimal-run-and-audit 产出经 SKILL.md 核实，除 `repro_outputs/` 与 `PATCHES.md` 外，还含 `SCIENTIFIC_CHANGELOG.md`、`COMPARABILITY_REPORT.md`，并区分 verified/partial/blocked 三态。
- DVC stage 字段（cmd/deps/params/outs/metrics/plots + frozen 等）、CCDS 目录与可选集成、Ruff/Poetry/pre-commit/EditorConfig/Taskfile/.gitignore 全部逐键比对官方文档一致。
- 唯一未能直接抓取的是 ai-paper-reproduction-skill 仓库内 repo-intake-and-plan / env-and-assets-bootstrap 两个 SKILL.md 原文（github raw 在本环境间歇性被拦），其要点依据 README 入口表 + claudemarketplaces 技能页 + 同套件 minimal-run-and-audit SKILL.md 交叉印证，工作流描述可信但未达"逐行原文"级。
