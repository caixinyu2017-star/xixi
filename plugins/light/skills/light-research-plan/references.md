# light-research-plan 参考资料（逐工具核查笔记）

本文件记录制定研究方案/实验执行规划时可直接复用的硬信息。每个工具含【是什么】【可复用方法/真实端点/参数】【链接】【已知坑/局限】。
信息核查日期：2026-06-06（功效分析/算力预算/论文复现协议三节为 R5 增补，研究日期 2026-06-11，功效数值经 statsmodels 实跑核验）。标注"未能核实"的条目表示未找到可靠公开来源，禁止据此编造。

---

## Academic Research Skills

【是什么】一套面向 Claude Code 的开源学术研究技能集，把科研工作流拆成 research → write → review → revise → finalize 五段流水线，每段是一个独立 skill。定位与 Light 包高度相似，可借鉴其分段衔接思路。

【可复用方法】
- 流水线分段：调研(research)→写作(write)→评审(review)→修订(revise)→定稿(finalize)。每段产出作为下段输入，强调"先评审再推进"。
- 卖点之一是抑制引用幻觉（号称针对"hallucinated citations"做了约束），方案里凡引用 baseline/数据集出处时应强制要求可点链接 + 可核查。
- 借鉴点：把"评审"作为独立显式阶段插在写作与定稿之间，而非隐式混在写作里。

【链接】
- 仓库：https://github.com/imbad0202/academic-research-skills
- 介绍：https://pyshine.com/Academic-Research-Skills-Claude-Code/

【已知坑/局限】社区项目，非官方；技能质量依赖底层模型；引用核查仍需人工复核，不能全信"已修复幻觉"的宣称。

---

## Experiment Agent（EXP-Bench / "Can AI Conduct AI Research Experiments?"）

【是什么】论文 EXP-Bench（arXiv 2505.24785）提出的"实验智能体"评测框架，把"完整跑一个 AI 研究实验"形式化为可评测任务，从顶会论文+开源代码反推出端到端实验任务。对制定实验规划极有参考价值：它定义了一个实验任务必须包含的要素。

【可复用方法 — 实验任务的四要素拆解】每个实验任务被拆成：
1. **Research question（研究问题/假设）** —— 对应方案里的可证伪假设 H1/H2。
2. **Experiment design（实验设计）** —— 自变量、因变量、控制变量、数据集、baseline、评价指标、消融点。
3. **Implementation（实现）** —— 可执行代码 + 运行配置（这是把设计落到代码的环节）。
4. **Conclusion / analysis（结论）** —— 用实验结果回答研究问题，需与原始假设对齐。
评测分别打分这四块，提示"设计"与"结论"最易出错（agent 常实现得出来但分析跑偏）。规划时把这四块作为每个实验条目的最小完整单元。

【链接】
- 论文：https://arxiv.org/abs/2505.24785 ；HTML：https://arxiv.org/html/2505.24785
- 专题：https://api.emergentmind.com/topics/exp-bench
- 同类对照基准（可用于设计参考）：MLE-bench、PaperBench(https://openai.com/index/paperbench/)、MLR/MLGym。

【已知坑/局限】是评测基准而非现成可装的 agent 工具；当前 SOTA agent 在端到端实验上得分仍远低于人类专家，说明"设计+分析"环节不能完全托管给自动化，需人工把关。

---

## 工程纪律技能（obra/superpowers 体系：writing-plans / executing-plans / test-driven-development / systematic-debugging / verification-before-completion）

这五个是 obra/superpowers 这套 Claude Code 技能框架里的核心"工程纪律"技能，把编码 agent 拉回"研究→计划→实现→验证"的工程流程。它们彼此配套，对实验执行规划的"如何稳健落地+验证"部分直接复用。仓库：https://github.com/obra/superpowers ；介绍：https://www.knightli.com/en/2026/05/15/obra-superpowers-agentic-skills-framework/

### writing-plans
【是什么】先研究代码库/资料、再写分阶段(phased)实现计划的技能。
【可复用方法】
- 写计划前**先调研**（读现有代码、依赖、约束），不凭空规划。
- 计划按 **phase 分段**，每个 phase 有明确的**成功标准(success criteria)**和可验证的产出。
- 计划写成可被另一个执行者(或 agent)independently 照做的文档——粒度细到"做什么、改哪、怎么验证"。
【借鉴到方案】实验矩阵里每个实验条目都配"完成判定标准"，而不是只列名字。

### executing-plans
【是什么】严格按既定计划逐 phase 执行、每步做完即核对的技能。
【可复用方法】一次只推进一个 phase；完成后对照 success criteria 勾验，再进入下一个；偏离计划要显式记录（对应 decision_log）。

### test-driven-development（TDD）
【是什么】RED → GREEN → REFACTOR 循环：先写会失败的测试，再写最小实现使其通过，最后重构。
【可复用方法】
- **先写测试，看它失败(RED)**，确认测试真的在测东西；再写实现让它变绿(GREEN)；再重构(REFACTOR)。
- 关键纪律：不要先写实现再补测试；警惕"测试全绿但代码是错的"（测试没断言到位）。
【借鉴到方案】科研代码的关键函数（数据处理、指标计算、统计检验）应配单元测试，指标实现要有"已知输入→已知输出"的金标准用例。

### systematic-debugging
【是什么】结构化排错，强调先定位根因再改，禁止盲目试错打补丁。
【可复用方法（阶段化）】
1. **复现**：稳定复现 bug，记录精确触发条件。
2. **读错误信息**：完整读 stack trace / 报错，别跳过。
3. **隔离/定位根因**：二分缩小范围，形成关于根因的**假设**。
4. **验证假设**：用最小实验确认假设成立。
5. **修复并验证**：改完要回到复现步骤确认真的修好，且没引入回归。
核心戒律：同一思路失败两次就停下找根因，换打法，而不是连续打补丁（与 Light 主 prompt 的 failure-loop 规则一致）。

### verification-before-completion
【是什么】声称"做完"之前必须先验证的技能——build/测试/核对成功标准全过了才算完成。
【可复用方法】完成前过一遍 checklist：build 通过、相关测试通过、产出与 success criteria 逐条对上、临时文件清理。对应方案里的"复现清单 checklist"。

【已知坑/局限】均为社区/个人维护的 skill，非 Anthropic 官方；存在大量 fork（claudepluginhub、lobehub 上同名多版本），具体措辞略有出入；核心方法论一致，引用时以 obra/superpowers 主仓为准。

---

## DVC（Data Version Control）

【是什么】基于 Git 的数据/模型版本控制 + 可复现流水线工具。大文件不进 Git，只在 Git 里存 `.dvc` 指针，实体推到远端存储。

【可复用方法/真实命令】
- 初始化：`dvc init`（在 git repo 内）。
- 跟踪数据：`dvc add data/raw.csv` → 生成 `data/raw.csv.dvc`（含 md5），把 `.dvc` 文件提交进 git。
- 远端：`dvc remote add -d myremote s3://bucket/path`（支持 s3/gs/azure/ssh/本地）；`dvc push` 上传实体、`dvc pull` 拉取。
- 流水线：`dvc.yaml` 定义 stages，每个 stage 有 `cmd`（命令）、`deps`（依赖文件/代码）、`params`（引用 `params.yaml` 的超参）、`outs`（产物）、`metrics`、`plots`。
  - 加 stage：`dvc stage add -n train -d train.py -d data/ -p lr,epochs -o model.pkl -M metrics.json python train.py`
  - 运行/复现：`dvc repro`（只重跑依赖变化的 stage，靠 `dvc.lock` 记录的哈希判断）。
- 实验：`dvc exp run`（跑一次实验并记录）、`dvc exp show`（表格对比超参×指标）、`dvc exp diff`、`dvc metrics diff`、`dvc params diff`、`dvc plots diff`。
- 关键文件：`dvc.yaml`(人写的流水线定义) + `dvc.lock`(自动生成，锁定每个 stage 的输入输出哈希，保证可复现) + `params.yaml`(超参)。

【链接】
- Get Started：https://dvc.org/doc/start
- 流水线/指标/参数：https://dvc.org/doc/start/data-pipelines/metrics-parameters-plots
- exp run：https://dvc.org/doc/command-reference/exp/run
- 与 Hydra 组合：https://dvc.org/doc/user-guide/experiment-management/hydra-composition

【已知坑/局限】`dvc.lock`/`.dvc` 必须连同代码一起提交，否则别人 `dvc pull` 不到对应版本；大文件首次 add 慢；远端存储凭证需另配；与 Git LFS 二选一别混用。

---

## MLflow

【是什么】开源实验追踪 + 模型管理平台。四大组件：Tracking（记录参数/指标/产物）、Models、Model Registry、Projects。

【可复用方法/真实 API（Python）】
- `mlflow.set_tracking_uri("http://...")` 或本地 `file:./mlruns`；`mlflow.set_experiment("exp-name")`。
- `with mlflow.start_run(run_name=...):` 包裹一次实验；run 归属于 experiment。
- 记录：`mlflow.log_param("lr",0.01)` / `log_params(dict)`；`mlflow.log_metric("acc",0.9, step=epoch)`（支持 step，画曲线）/ `log_metrics(dict)`；`mlflow.set_tag(...)`；`mlflow.log_artifact(path)` / `log_artifacts(dir)`（存图/模型/配置）。
- 自动记录：`mlflow.autolog()` 或框架专用 `mlflow.sklearn.autolog()` / `mlflow.pytorch.autolog()`，自动抓参数、指标、模型。
- 模型注册：`mlflow.<flavor>.log_model(...)` + Model Registry 管理版本/阶段(Staging/Production)。
- 查看：`mlflow ui`（默认 http://localhost:5000）。

【链接】
- Tracking API：https://mlflow.org/docs/latest/tracking/tracking-api.html
- autolog：https://mlflow.org/docs/latest/tracking/autolog.html

【已知坑/局限】默认 backend 是本地文件，团队协作需起 tracking server + 数据库后端(SQLAlchemy)；`log_metric` 高频调用有开销；artifact 存储要单独配（本地/S3）；run 忘了 `start_run` 会落到默认实验里乱掉。

---

## Weights & Biases（W&B / wandb）

【是什么】云端实验追踪、可视化、超参搜索(Sweeps)、Artifacts 版本管理平台。

【可复用方法/真实 API（Python）】
- `wandb.init(project="...", config={...})` 启动一次 run，`config` 存超参（可被 sweep 覆盖）。
- `wandb.log({"loss":x, "acc":y}, step=i)` 记录指标，自动画交互曲线；`wandb.log({"img": wandb.Image(...)})` 记图。
- `wandb.config` 读写超参；`wandb.watch(model)` 跟踪梯度/权重。
- Artifacts：`wandb.log_artifact(...)` / `use_artifact(...)` 做数据/模型版本与血缘。
- **Sweeps（超参搜索）**：写 sweep 配置（YAML/dict），字段：`method`（`grid`/`random`/`bayes`）、`metric`（`{name, goal: minimize/maximize}`）、`parameters`（每个超参的取值/分布）。流程：`sweep_id = wandb.sweep(config, project=...)` → `wandb.agent(sweep_id, function=train, count=N)`，agent 反复拉超参组合跑 train。
- Public API：`wandb.Api()` 程序化拉取历史 run 数据做汇总分析。

【链接】
- Sweeps 指南：https://docs.wandb.ai/guides/sweeps
- Artifacts：https://docs.wandb.ai/guides/artifacts/
- Public API：https://docs.wandb.ai/ref/python/public-api/

【已知坑/局限】默认上传到 W&B 云（涉及数据外发，敏感数据需 self-hosted/离线 `WANDB_MODE=offline`）；免费版团队/存储有限额；`bayes` sweep 不保证全局最优；忘了 `wandb.finish()` 在 notebook 里会串 run。

---

## Hydra

【是什么】Facebook(Meta) 开源的分层配置框架，用组合方式管理复杂实验配置，命令行可覆盖任意字段，原生支持 multirun 扫参。

【可复用方法/真实用法】
- 入口：`@hydra.main(version_base=None, config_path="conf", config_name="config")` 装饰 `main(cfg: DictConfig)`，配置以 OmegaConf 的 `DictConfig` 传入，`cfg.optimizer.lr` 点号访问。
- **config groups + Defaults List**：`conf/` 下按目录分组（如 `conf/model/`, `conf/dataset/`），`config.yaml` 顶部用 `defaults:` 列表组合，例：`defaults: [_self_, model: resnet, dataset: cifar]`。
- **命令行覆盖**：`python train.py optimizer.lr=0.1 model=resnet50`；加键用 `+key=val`，强制改用 `++key=val`，删用 `~key`。
- **multirun 扫参**：`python train.py -m optimizer.lr=0.01,0.1,1 model=a,b` → 笛卡尔积逐一跑；range/glob 等扩展语法见 override grammar；可换 sweeper 插件（Optuna/Ax/Nevergrad）做智能搜索。
- 每次 run 自动建带时间戳的输出目录，保存最终合成配置 → 天然可复现。

【链接】
- 入门：https://hydra.cc/docs/intro/
- Defaults List：https://hydra.cc/docs/advanced/defaults_list/
- Multi-run：https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/
- Override 语法：https://hydra.cc/docs/advanced/override_grammar/basic/

【已知坑/局限】`_self_` 在 defaults 列表中的位置决定覆盖优先级，放错会被组默认覆盖；改了工作目录(默认 chdir 到 output 目录)易踩相对路径坑（新版可关）；复杂插值/结构化配置学习曲线陡。

---

## Snakemake

【是什么】受 GNU Make 启发的工作流引擎（Python 语法），用 rule 描述"输入→命令→输出"，自动推 DAG、增量重跑、并行调度，科研流水线常用。

【可复用方法/真实语法】
- `Snakefile` 里写 `rule`：含 `input:`、`output:`、`params:`、`threads:`、`resources:`、`log:`、以及 `shell: "..."` 或 `run:`(Python) 或 `script: "x.py"`。
- **wildcards（通配）**：output 里写 `"results/{sample}.txt"`，Snakemake 反推 `{sample}` 并对每个样本展开规则；`input` 用同名 wildcard 关联上游。
- `rule all:` 列最终目标(`input:` 指向想要的终产物)，Snakemake 反向推导需要跑哪些 rule。
- 运行：`snakemake --cores 8`（增量：只重跑输入/代码变化的 rule）；`snakemake --dag | dot -Tpng` 画 DAG。
- **可复现**：`conda:` 指定每个 rule 的环境 yaml（`--use-conda`）；`container:` 指定容器镜像；`configfile:` 读 `config.yaml` 参数。

【链接】
- 写 Snakefile：https://snakemake.readthedocs.io/en/stable/snakefiles/writing_snakefiles.html
- Rules：https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html
- 教程：https://snakemake.readthedocs.io/en/latest/tutorial/tutorial.html

【已知坑/局限】所有产物路径由 rule 唯一确定，命名规划不好会很乱；动态依赖/聚合需 `checkpoint` 机制，较绕；Windows 上 shell 命令兼容性一般，建议 WSL/Linux。

---

## Cookiecutter Data Science（CCDS, drivendata）

【是什么】数据科学项目的标准目录脚手架模板，一条命令生成统一、可复现的工程结构。新版命令行工具是 `ccds`。

【可复用方法/真实结构（典型布局）】
```
├── data/
│   ├── raw/        # 原始只读数据，绝不修改
│   ├── interim/    # 中间转换结果
│   ├── processed/  # 最终建模用数据
│   └── external/   # 第三方来源
├── models/         # 训练好的模型/序列化对象
├── notebooks/      # 探索性 notebook（命名带序号+作者）
├── references/     # 数据字典、说明手册
├── reports/figures/# 生成的图表
├── src/ (或包名)   # 源码：data/ features/ models/ visualization/
├── requirements.txt / environment.yml
├── Makefile        # make data / make train 等命令
└── README.md
```
核心理念（"opinions"）：原始数据不可变、分析可从原始数据完整重建、notebook 不放可复用逻辑（逻辑下沉到 src）、用相对路径+配置不写死绝对路径。
- 安装/用：`pip install cookiecutter-data-science` 后 `ccds`（旧版 `cookiecutter -c v1 ...`）。

【链接】
- 主页：https://cookiecutter-data-science.drivendata.org/
- 设计理念：https://cookiecutter-data-science.drivendata.org/opinions/
- 用法：https://cookiecutter-data-science.drivendata.org/using-the-template/
- 仓库：https://github.com/drivendataorg/cookiecutter-data-science

【已知坑/局限】v1(cookiecutter) 与 v2(ccds) 目录略有差异，引用时注明版本；模板是约定而非强制，团队需自觉遵守；纯模板，不含 CI/版本控制逻辑，需自行配 DVC/git。

---

## scikit-learn Pipelines

【是什么】sklearn 把预处理 + 估计器串成单一对象的机制，杜绝训练/测试间的数据泄漏，并让整条流程可一起调参/交叉验证。

【可复用方法/真实 API】
- `Pipeline([("scaler", StandardScaler()), ("clf", SVC())])` 或简写 `make_pipeline(StandardScaler(), SVC())`；`.fit(X,y)` 时各步顺序 `fit_transform`，最后一步 `fit`。
- **`ColumnTransformer`**：对不同列走不同预处理（数值列标准化、类别列 OneHot），是表格数据防泄漏的关键。
- **防泄漏要点**：所有基于训练集统计量的步骤（标准化、填补、编码）必须放进 Pipeline，再交给交叉验证，使每折只在该折训练集上 fit。
- 调参：`GridSearchCV(pipe, param_grid={"clf__C":[1,10]}, cv=5, scoring=...)`——参数名用 `步骤名__参数名` 双下划线；`RandomizedSearchCV` 做随机搜索。
- 评估：`cross_val_score(pipe, X, y, cv=5)`；多指标用 `cross_validate(..., scoring=["accuracy","f1"])`。

【链接】
- Pipeline/组合：https://scikit-learn.org/stable/modules/compose.html
- 交叉验证：https://scikit-learn.org/stable/modules/cross_validation.html
- GridSearchCV：https://scikit-learn.org/stable/modules/grid_search.html
- cross_validate：https://scikit-learn.org/1.5/modules/generated/sklearn.model_selection.cross_validate.html

【已知坑/局限】最常见错误是在 Pipeline 外先对全量数据做 scaling/imputation → 泄漏；`__` 参数名写错 GridSearch 静默不报；自定义步骤需实现 `fit/transform` 接口。

---

## PyMC

【是什么】Python 概率编程库，写贝叶斯模型并用 MCMC(NUTS)/变分推断采样后验，配 ArviZ 做诊断。适合需要不确定性量化、小样本、层级模型的研究。

【可复用方法/真实 API】
- `with pm.Model() as model:` 上下文里声明先验（如 `mu = pm.Normal("mu", 0, 1)`）和似然（`pm.Normal("y", mu, sigma, observed=data)`）。
- 采样：`idata = pm.sample(draws=1000, tune=1000, chains=4, target_accept=0.9)`（默认 NUTS），返回 ArviZ `InferenceData`。
- 后验预测：`pm.sample_posterior_predictive(idata)`；先验预测 `pm.sample_prior_predictive()`。
- 诊断（用 ArviZ）：`az.summary(idata)` 看 `r_hat`(应≈1.0)、`ess_bulk/ess_tail`(有效样本量)；`az.plot_trace`、`az.plot_posterior`。
- 模型比较：`az.compare({...}, ic="loo")`（LOO/WAIC）。

【链接】
- 概览：https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html
- pm.sample：https://www.pymc.io/projects/docs/en/stable/api/generated/pymc.sample.html
- 模型比较：https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/model_comparison.html

【已知坑/局限】采样出现 `divergences` 警告说明后验几何难采，需调 `target_accept` 或重参数化（non-centered）；`r_hat>1.01` 表示未收敛不能用；大数据/复杂模型采样慢；PyMC3 与 PyMC(v4+) API 有别，引用注明版本。

---

## Statsmodels

【是什么】Python 统计建模库，偏统计推断（系数、标准误、p 值、置信区间、假设检验），与 sklearn 偏预测形成互补。做显著性检验/回归诊断的首选。

【可复用方法/真实 API】
- 两套接口：数组接口 `import statsmodels.api as sm`（需自己 `sm.add_constant(X)` 加截距）；公式接口 `import statsmodels.formula.api as smf`，R 风格公式 `smf.ols("y ~ x1 + x2 + C(group)", data=df)`。
- 拟合+报告：`res = sm.OLS(y, X).fit()`；`res.summary()` 给系数、std err、t、`P>|t|`、`[0.025 0.975]` 置信区间、R²、F 统计量、AIC/BIC。
- 取值：`res.params`、`res.pvalues`、`res.conf_int()`、`res.rsquared`。
- 假设检验：`res.t_test(...)`、`res.f_test(...)`、`res.wald_test(...)`；其它模型 `Logit`、`GLM`、`Poisson`、混合效应 `MixedLM`、时间序列 `SARIMAX`。
- 回归诊断：残差正态性、异方差（`het_breuschpagan`）、多重共线性（VIF：`variance_inflation_factor`）。
- 配对/独立检验也可用 scipy.stats（t-test、Wilcoxon），与方案里"统计显著性"对应。

【链接】
- OLS：https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html
- 公式接口：https://www.statsmodels.org/stable/example_formulas.html
- 回归诊断：https://www.statsmodels.org/stable/examples/notebooks/generated/regression_diagnostics.html

【已知坑/局限】数组接口默认**不含截距**，忘了 `add_constant` 结果全错；面向推断不做自动正则化；大规模数据不如 sklearn 高效；p 值解读需满足模型假设（线性、独立、同方差、正态残差），违背时结论无效。

---

## 统计功效与样本量 / 种子数规划（statsmodels TTestIndPower）

【是什么】做实验设计时，先用**功效分析(power analysis)**反推"要检测出某大小的差异，每组最少需要多少样本/多少随机种子"，避免事后发现"种子太少根本检不出差异"。四个量 effect_size / power / alpha / n 知三求一。

【可复用方法 / 真实 API】
```python
from statsmodels.stats.power import TTestIndPower
analysis = TTestIndPower()
# 正向：给定效应量 d、功效 0.8、显著性 0.05，求每组最小样本量
n = analysis.solve_power(effect_size=0.5, power=0.8, alpha=0.05, alternative='two-sided')
# 反查：给定每组样本量，求能达到的实际功效
p = analysis.solve_power(effect_size=0.5, nobs1=5, alpha=0.05, alternative='two-sided')
```
- `effect_size` 用 Cohen's d（两组均值差 / 合并标准差）；经验档 **0.2 小 / 0.5 中 / 0.8 大**；有预实验时用 `(mean1-mean2)/pooled_sd` 实算更准。
- `power` 惯例取 0.8（容忍 20% 漏检），`alpha` 取 0.05；`alternative` 单/双侧按假设选。

【科研常景算例（数值经 statsmodels 0.14.5 实跑核验，留痕见 `../../_verification_log/R5-04-power-analysis.md`）】

| 场景 | Cohen's d | power=0.8, α=0.05 双侧 → 每组最小 n |
|---|---|---|
| 检测微小提升（小效应） | 0.3 | 175.38 → 取 **176** |
| 检测典型 mAP/准确率差异（中效应） | 0.5 | 63.77 → 取 **64** |
| 检测显著差异（大效应） | 0.8 | 25.52 → 取 **26** |

反查"3~5 个种子够不够"：d=0.5、每组 n=5 → power **仅 0.108**（严重欠功效）；要 d=0.5 达 power 0.8 需每组 **64** 次重复；d=0.8、n=30 → power **0.861**（达标）。

【借鉴到方案】"≥3~5 个随机种子"只够检测**大效应**；对方法间细微差异（中小效应）必须先做功效分析定种子/样本数，别等跑完才发现检不出。把"目标效应量 + 反推的最小种子/样本数 + 实际功效"写进实验矩阵，作为统计显著性实验行的设计依据。验证性研究时这两个数同时是预注册的"样本量依据 + 分析计划"字段（见下「预注册」节）。

【已知坑/局限】功效分析对效应量假设极敏感（d 估小一点 n 翻几倍）；t 检验功效公式假设近似正态/等方差，重尾或极不均衡时偏乐观；多重比较要对 alpha 做校正（如 BH-FDR，见 m06 significance_test.py）后再算功效；这是**计划阶段**的样本量规划，不能替代结果阶段的实际检验。

---

## 预注册（preregistration，可选，验证性研究）

【何时值得】研究是**验证性**（confirmatory，事先有明确可证伪假设、要做假设检验）时，预注册把假设/指标/分析计划在看数据**前**时间戳锁定，防 HARKing 与 p-hacking（联动 a10 风险清单第2条）。纯**探索性**（exploratory，找模式、生成假设）不必预注册，但论文里须**如实区分**哪些是预注册的验证性分析、哪些是事后探索，别把探索结果包装成验证（审稿人必查）。

【最小流程（OSF / AsPredicted，2026-06 实查）】
1. 选平台：OSF Registrations（多模板、可详写、可设禁止期 embargo）或 AsPredicted（短问卷式、固定几问、最轻）。
2. 选模板：按研究类型选（COS 模板指南），常用 OSF Prereg；填完生成**只读时间戳版本**，不可再改（要改只能加注新版）。
3. 拿到注册链接/DOI，写进 PROJECT_PLAN.md 与论文方法节；数据采集后严格按计划做主分析，偏离须在论文显式声明并标为探索性。

【预注册字段 ↔ 实验矩阵字段映射】（后两行复用 R5.4 功效分析产出，不重复算）

| 预注册字段 | 对应实验矩阵/方案字段 | 来源 |
|---|---|---|
| 假设（可证伪 H1/H2） | 实验条目的"对应假设" | m03/m04 立项 |
| 主要结局指标（primary outcome，**事先**指定，防多指标择优） | 评价指标 + "主指标"标记 | m05 实验矩阵 |
| 样本量/重复数依据 | 目标效应量 + 反推最小种子/样本数 | **R5.4 功效分析**（上节，statsmodels 实跑：d=0.5→每组64） |
| 分析计划（检验方法、校正、剔除准则） | 统计显著性实验行的检验与多重比较校正 | **R5.4 + m06**（BH-FDR 见 significance_test.py） |

【链接】OSF Registrations https://help.osf.io/article/330-welcome-to-registrations ；AsPredicted https://aspredicted.org/ ；COS 模板指南 https://www.cos.io/blog/choosing-preregistration-template-guide-for-researchers 。

【已知坑/局限】预注册≠论文被接收，也不锁死你只能做注册内分析（可加探索性分析，只要标清）；登记平台全文未逐页核（WebFetch 受限），落地前以 OSF/AsPredicted 现行表单为准；中国本土无强制预注册要求，属可选最佳实践。

---

## 算力 / 成本预算（承接 m04 rubric 维度7）

【是什么】idea 经 m04 放行后，第一个落地环节必须**算账**——把"算力可行性"从口头估计变成 GPU 时数 × 单价的金额表。m04 critique 维度7(算力与成本) 在立项卡里只给了量级粗估，m05 在此细化为可执行预算。

【可复用方法 / 预算估算骨架】
- **单次训练成本** = 单次训练 GPU 时数 × 卡数 × 单价/卡时。
- **总预算** = Σ(主实验 + 消融 + 敏感性扫参 + 多种子重复) × 单次成本 + 调试/失败重跑冗余(经验加 30~50%)。
- 扫参/多种子是预算放大器：功效分析定的 64 种子 × 网格点数会让成本指数膨胀，规划时与功效需求联动取舍。
- 云价随厂商/区域/竞价实例波动大，**取数时记来源 + 日期**（对齐 db08 预算口径），禁凭记忆写单价；自有集群按电费 + 折旧粗算机会成本。

【借鉴到方案】实验矩阵模板已加"算力/成本预算"字段（见 templates/experiment_matrix.md）：逐实验行估 GPU 时数 → 汇总成本表 → 对照预算上限，超支则砍扫参范围或降种子数（并记录功效损失）。预算与 db08(知产/申报材料) 的经费预算口径一致。

---

## 复现已有论文协议（paper2code 并入：复现也是一种研究方案）

【是什么】复现一篇已发表论文的结果，本身就是一种合法的研究方案（验证、教学、作为自己工作的 baseline）。它和"从 0 设计实验"共享同一套可复现规划，但多了"对标原文"的特殊环节。按 I-1 裁决，paper2code 能力并入本技能，以下五步走。

【五步协议】
1. **定复现目标**：明确复现的是**哪张表 / 哪张图的哪个数**（如"Table 2 第 3 行 ImageNet top-1 76.5%"），不说"复现这篇论文"这种无法验收的目标。一次锚定一个可量化数字。
2. **资产盘点**：列原文的代码（官方 repo？第三方？无代码？）、权重（是否放出）、数据（公开可下？需申请？预处理脚本是否提供）、配置（超参/种子/环境是否完整披露）。三类资产可得性决定复现难度与归因空间。
3. **偏差预算**：**事先**定"差多少算复现成功"——如"top-1 在原文 ±0.5% 内算成功"。阈值依指标方差与原文是否给多种子定；不预设阈值，复现完就会陷入"算不算复现成功"的扯皮。
4. **复现日志格式**：逐次尝试记 {日期 / 改了什么 / 得到的数 / 与目标的差 / 下一步假设}，与 systematic-debugging 的"假设-验证"一致；每次只改一个变量，便于归因。
5. **复现失败的诚实归因（三分）**：达不到偏差预算时，把原因诚实归到三类，禁止笼统说"没复现出来"：
   - **实现差异**：我方代码/超参/环境与原文不同（最常见，可继续逼近）。
   - **数据差异**：数据版本/预处理/划分不同（核对原文数据来源与处理）。
   - **原文问题**：原文未充分披露、结果不可复现、甚至存疑（需多方交叉，证据充分才下此结论，关联 research-ethics）。

【衔接】复现产出的代码与日志走 a03(light-backend-coding) 落地与调试协议；偏差预算与"完成前验证"checklist 对齐；复现作为自己工作的 baseline 时，结果回 m06 分析。复现失败若指向"原文问题"，走 research-ethics 的核查流程，勿轻率公开指控。

