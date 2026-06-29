# light-project-structure — 深度分析与同类对标

> 源：[`skills/light-project-structure/SKILL.md`](../../../skills/light-project-structure/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：科研项目目录骨架的规范化技能:用"数据流即 DAG"的方法论组织 17+ 目录,并附一个可一键生成全树+模板+pyproject 的 scaffold.py,服务于论文/软著/专利/复现全链路。

## 核心运行逻辑
核心方法论是"把整个项目当成一张有向无环图(DAG)":raw 数据不可变作可信源头,所有下游产物(processed/models/results/figures)都能由"上游数据+代码+params"重算因而不入 Git 只入 DVC,notebooks 拆 exploratory(草稿)与 reports(可重跑)且定稿逻辑下沉到 src。目录结构刻意与知识库 db09 的 project_card 各 status 字段一一对应(code_status↔src/、data_status↔data/),从而让 a02 能跟踪进度。落地手段是 scaffold.py 一条命令建树+拷 6 模板+始终写 pyproject(默认 uv 后端、--poetry 备选),数据分层与 notebook 命名沿用 Cookiecutter Data Science。references.md 是该技能的"事实底座",14 个工具/技能逐条核实(带日期/端点/已知坑),保证 SKILL 里出现的每条命令可核查。

## 关键步骤
- 1. 盘点已有项目:借 repo-intake-and-plan 思路,先读 README→扫 setup 脚本与文档化命令→把工作流归类为推理/训练/评估,据此给散落文件归位(注:此路径无脚本,纯人工)
- 2. 新建项目:首选 python scripts/scaffold.py <dir> [--dvc --poetry --force],建 23 个目录(data 四分层+notebooks 探索/报告分流+.light 台账)+拷 6 模板+写 src 包+pyproject
- 3. 重命名规范化:小写+连字符/下划线、实验带编号(exp_004_ablation)、结果文件名映射实验编号
- 4. 补 README/CHANGELOG/PROJECT_PLAN(填 {{占位符}})
- 5. 版本与依赖:git 管文本+DVC 管大文件;依赖默认 uv(uv init/add/sync),备选 Poetry
- 6. 质量门:Ruff+pre-commit+EditorConfig+.gitignore 四件套(配置已在模板),任务运行器 Makefile 或 Taskfile 二选一
- 7. 产出'文件归位说明':借 handoff 结构(Key Decisions 表+失败尝试+警告),复现场景固定 repro_outputs/ 落 verified/partial/blocked 三态

## 自带资产
- scripts/scaffold.py — 一键脚手架,建目录树+拷模板+写 pyproject(uv/poetry 两后端)+可选 dvc.yaml;含 --selftest 离线自测两路径,有非空目录守卫与 Windows UTF-8 编码修复
- templates/PROJECT_STRUCTURE.md — 完整目录骨架说明+命名规范+db09 字段对应表(但 scaffold 不拷贝它)
- templates/README.template.md — 科研 README 模板(状态表/数据表/快速复现/引用 bibtex)
- templates/PROJECT_PLAN.template.md — 实现计划模板,含强制 No-Placeholders 规则+2-5 分钟任务粒度+垂直切片+失败尝试表
- templates/CHANGELOG.template.md — Keep a Changelog + SemVer 模板
- templates/python-research.gitignore — GitHub 官方 Python.gitignore + 科研补充条目
- templates/editorconfig.template — 跨编辑器统一缩进/换行(root=true)
- templates/pre-commit-config.template.yaml — rev 钉死 tag 的 pre-commit-hooks + ruff-pre-commit
- references.md — 14 个工具/技能逐条核实笔记(CCDS/DVC/Poetry/Ruff/pre-commit/EditorConfig/Taskfile/.gitignore + 6 个借鉴技能),含真实端点与已知坑

## 优点
- 方法论有真正的内核而非堆目录:'数据流即 DAG'三铁律(raw 不可变/下游可重算故不入库/notebooks 拆探索与报告)是可推导、可执行的设计原则,直接决定了哪些进 Git 哪些进 DVC
- scaffold.py 工程质量扎实:有 --selftest 覆盖 uv+poetry 两后端并校验 tomllib 可解析、有非空目录守卫(返回码 2)、有 Windows GBK 乱码修复、空目录放 .gitkeep,不是玩具脚本
- references.md 罕见的严谨:14 条全部标注核查日期(2026-06-06)、给真实命令/配置键/官方链接/已知坑,还诚实记录了自我纠错(prd-to-issues→to-issues)和未能逐行核实的项(两个 SKILL.md raw 被拦)
- 深度嵌入 Light 生态:目录与 db09 project_card 字段一一映射、质量门口径声明与 a03 对齐为单一真相源、为 m07/m15/m16 预留目录,不是孤立技能
- 模板有实操含金量:PROJECT_PLAN 的 No-Placeholders 强制规则、CHANGELOG 的 Keep-a-Changelog 规范、pre-commit 的 rev 钉死 tag,都是经过审稿能站住的工程惯例
- 对 CCDS 做了显式取舍说明(figures/ vs reports/figures/、src/ vs 顶层模块包),而非盲抄上游

## 缺点 / 可被质疑处
- uv/Poetry 默认后端在文档与模板间自相矛盾:SKILL.md 与 scaffold.py 默认 uv,但 README.template.md 写'推荐用 Poetry'且安装命令是 poetry install、PROJECT_PLAN.template.md 全用 poetry run pytest、PROJECT_STRUCTURE.md 第 41 行标 'Poetry/Ruff'。scaffold 出 uv 版 pyproject,生成的 README 却教用户 poetry——开箱即错
- PROJECT_STRUCTURE.md 是模板却从不被 scaffold 拷进项目:TEMPLATE_MAP 只有 6 项不含它,而生成的 README 第 35 行写'详见同目录 PROJECT_STRUCTURE.md'——这是个落地即悬空的引用;且 SKILL.md 第 69 行把它算进'6 份模板'实则列了 7 个文件名,自身计数混乱
- environment.yml 全程画饼:SKILL 骨架、PROJECT_STRUCTURE、README 都提到 conda environment.yml,scaffold.py 从不生成它,conda 路径在所有产物里都是断头路
- .light/passport.yaml 这个被反复称为'跨阶段续跑真相源/orchestrator 维护'的核心台账文件,scaffold 只建 .light/ 空目录放 .gitkeep,从不生成 passport.yaml 本体——最关键的编排文件缺位
- 技能自称范围含'整理已有项目结构',但只有新建项目有脚本;盘点/分类/归位全靠 prose 借 repo-intake-and-plan 思路,零工具支撑,实际是半残
- --dvc 用 dvc init --no-scm,与 SKILL/references 反复强调的'git init→dvc init、.dvc/config 要 commit、git+DVC 互补'流程冲突:--no-scm 是给非 git 项目用的,生成的 DVC 元数据不会与 git 正确集成;dvc.yaml 占位 cmd 指向不存在的 {module}.dataset,dvc repro 开箱必失败(注释虽有说明但易踩)
- 质量门讲了 Makefile/Taskfile 二选一,却不提供任一模板;LICENSE 在 README 有'许可'节、CCDS 也生成 LICENSE,但 scaffold 不产出 LICENSE/CITATION.cff——对要发论文/软著的科研项目是明显缺口

## 可优化点（供后续逐技能优化）
- 统一依赖后端口径:既然默认 uv,就把 README.template.md/PROJECT_PLAN.template.md/PROJECT_STRUCTURE.md 里的 poetry install、poetry run、'推荐 Poetry'全部改为 uv sync/uv run,或让 scaffold 按 --poetry/--uv 渲染模板里的安装段(模板参数化),消除开箱矛盾
- 把 PROJECT_STRUCTURE.md 加进 TEMPLATE_MAP 拷进项目(或拷到 docs/),修掉 README 的悬空引用;同时把 SKILL.md 第 68-69 行'6 份模板'的计数与实际落地清单对齐
- 让 scaffold 真正生成 .light/passport.yaml 初始骨架(产物台账初始字段)和一份首张 handoff 卡模板,而不是只留空目录;passport schema 应与编排器约定对齐
- --dvc 改为:若检测到/能 git init 就先 git init 再 dvc init(不带 --no-scm),并把 .dvc/config、dvc.yaml 一并 git add 提示;dvc.yaml 占位同时生成一个最小可跑的 src/<module>/dataset.py 桩,使 dvc repro 开箱不报错
- 补 environment.yml 生成开关(--conda)或从文档中彻底删除 conda 承诺,二者择一,别留断头路
- 新增 --license 选项生成 LICENSE(MIT/BSD-3)与可选 CITATION.cff;科研项目引用与合规是刚需
- 为'整理已有项目'补一个 intake 脚本(扫目录→按 推理/训练/评估 给文件打标→输出归位建议 + 文件归位说明草稿),把 prose 承诺变成工具,补齐技能另一半范围
- 提供 Makefile 与 Taskfile 两个任务运行器模板并由 scaffold 按 flag 二选一落地,兑现 SKILL 里的'二选一'承诺

## 与其他 Light 技能/知识库的衔接
["a03 backend-coding:声明为代码侧质量门(Ruff/pre-commit/uv)的单一真相源,本技能口径与之对齐,uv 默认后端也'与 a03 推荐一致'", "db09 project_card:目录结构与 project_card 各 status 字段一一映射(code_status↔src/、data_status↔data/、paper_status↔paper/、exp_status↔experiments/),是结构设计的硬约束来源", "a02:依赖上述 db09 映射来跟踪项目进度", "m05/a04:本技能为其提供落地的项目结构", "m15(软著专利)/m07(论文)/m16(PPT):本技能预留 software-copyright/、patent/、paper/、ppt/ 对应目录给它们", "方法论借鉴(非 Light 内部,均来自 references.md 外部技能):repo-intake-and-plan(盘点已有项目)、handoff(文件归位说明结构)、to-issues(垂直切片拆任务)、writing-plans(2-5 分钟粒度计划)、minimal-run-and-audit(repro_outputs 三态归档)", "工具依赖:CCDS(数据分层与 notebook 命名来源)、DVC、uv/Poetry、Ruff、pre-commit、EditorConfig、Makefile/Taskfile"]

---

## GitHub 同类前沿技能对标

x

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [drivendataorg/cookiecutter-data-science](https://github.com/drivendataorg/cookiecutter-data-science) | ccds | 9901 | 2026-04-09 | std |
| [CodeCutTech/data-science-template](https://github.com/CodeCutTech/data-science-template) | dstp | 813 | 2026-06-12 | dvc |
| [showyourwork/showyourwork](https://github.com/showyourwork/showyourwork) | pdag | 652 | 2026-06-11 | dag |
| [mkrapp/cookiecutter-reproducible-science](https://github.com/mkrapp/cookiecutter-reproducible-science) | rsci | 195 | 2025-12-26 | cls |
| [snakemake-workflows/snakemake-workflow-template](https://github.com/snakemake-workflows/snakemake-workflow-template) | smk | 136 | 2026-06-03 | eng |
| [CLAIRE-Labo/python-ml-research-template](https://github.com/CLAIRE-Labo/python-ml-research-template) | mltp | 118 | 2025-06-06 | dkr |
| [gchure/reproducible_research](https://github.com/gchure/reproducible_research) | prsl | 116 | 2026-06-12 | aln |
| [lachlandeer/snakemake-econ-r](https://github.com/lachlandeer/snakemake-econ-r) | ecnr | 64 | 2026-05-07 | rnv |
| [timtroendle/cookiecutter-reproducible-research](https://github.com/timtroendle/cookiecutter-reproducible-research) | smkp | 37 | 2026-03-10 | pdc |
| [aidanscannell/reproducible-research-project-template](https://github.com/aidanscannell/reproducible-research-project-template) | mlpp | 12 | 2023-05-18 | mno |
