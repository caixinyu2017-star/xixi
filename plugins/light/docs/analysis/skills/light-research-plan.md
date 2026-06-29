# light-research-plan — 深度分析与同类对标

> 源：[`skills/light-research-plan/SKILL.md`](../../../skills/light-research-plan/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：把已通过 idea 审查(m04)的研究构想,落成一份可证伪、可复现、可验收的研究方案 + 实验矩阵 + 复现清单,并把派生数据/代码/分析任务派回各专职技能。

## 核心运行逻辑
核心思路是"假设驱动 + 可验收 + 可复现"三位一体。它强制每个实验条目按 EXP-Bench 四要素(研究问题/设计/实现/结论判定)写全,把最易跑偏的"设计"和"结论判定"作为重点核查项,用 plan_lint.py 离线校验实验矩阵每行四要素齐全(假设是 H#、数据集+baseline、指标、完成判定)。统计上以功效分析(TTestIndPower)反推种子/样本数,纠正"3~5 个种子就够"的误区(中效应需每组64次)。可复现性落到具体工具栈(Hydra/DVC/Snakemake/MLflow·W&B/CCDS/sklearn Pipeline 防泄漏)而非只喊口号。它定位为"上游研究设计文档",刻意把任务级 to-do、代码落地、目录脚手架、画图、数据构建派给 a03/a06/m09/m02,自己只承载研究设计与判定标准,通过 m-code/db-code 形成 pipeline 衔接。

## 关键步骤
- 1. 前置门控:仅对 m04 已放行 idea 执行,开工先确认数据(m02)与方法(db03)就绪
- 2. 按 10 项写实方案:研究目标&可证伪假设H1/H2 → 技术路线 → 数据 → 模型/方法 → 实验设计 → 可视化 → 时间甘特 → 风险+planB → 算力成本预算 → 预期成果
- 3. 放行后第一环节算账:逐实验估 GPU时数×卡数×单价,汇总对照预算上限,扫参×多种子超支则砍范围
- 4. 实验设计按 EXP-Bench 四要素展开主/消融/对比/敏感性/泛化/鲁棒性/显著性各类实验,先做功效分析定种子数
- 5. 可复现规划硬性落地:环境锁版本、CCDS 目录脚手架、Hydra 配置、DVC 数据版本、Snakemake 流水线、MLflow/W&B 日志、固定种子/划分
- 6. 验证性研究可做预注册(OSF/AsPredicted)锁定假设/主指标/分析计划,防 HARKing/p-hacking
- 7. 执行纪律:先计划后执行分phase、关键代码 TDD、系统化排错、完成前过 checklist
- 8. 填完实验矩阵跑 plan_lint.py 自查四要素齐全性
- 9. 产出 PROJECT_PLAN.md + experiment_matrix.md + 复现清单,派生评测集需求回 m02,代码交 a03,目录交 a06,里程碑登记 a02/db09
- 10. 复现已有论文走专门五步协议:定可验收复现目标→资产盘点→偏差预算→复现日志→失败三分归因

## 自带资产
- scripts/plan_lint.py — 离线只读校验实验矩阵 Markdown 表每行四要素(假设/变量/指标/停止条件)齐全,带列名别名容错、占位符识别、--selftest 三路径自测,退出码可接 CI
- templates/research-plan.md — PROJECT_PLAN 主模板,9 节+m04 must-fix 承接表,每节强制配'成功标准'和'验证方式'两个字段,刻意声明不重复 a06 任务清单
- templates/experiment_matrix.md — 实验矩阵模板,含主表(7类实验示例行)、派生数据规格表(交 m02)、算力成本预算表(三块联动)
- templates/reproducibility-checklist.md — 复现清单,按 环境/目录/配置/数据版本/流水线/日志/固定项 分组的勾选表
- references.md — 14 节逐工具核查笔记:Academic Research Skills、EXP-Bench、obra/superpowers 五工程纪律、DVC、MLflow、W&B、Hydra、Snakemake、CCDS、sklearn Pipeline、PyMC、Statsmodels、功效分析实跑算例、预注册、算力预算、复现论文协议;每条带真实端点/参数/已知坑

## 优点
- EXP-Bench 四要素 + plan_lint.py 把'实验设计写没写全'从主观判断变成可机器校验的硬约束,且脚本带别名容错和 selftest,工程上靠谱,真正能在 CI 里拦住空泛实验条目
- 统计功效分析是真正的亮点:用 statsmodels 实跑核验了 d=0.5→每组64、3~5种子对中效应 power 仅0.108 等具体数字(并留痕到 _verification_log),直击科研界'5个种子万岁'的普遍误区,远超一般模板的'报均值±标准差'套话
- 可复现规划落到真实命令/API级别(dvc stage add 完整参数、Hydra defaults列表、Snakemake rule字段、sklearn Pipeline 防泄漏要点),不是工具名堆砌,可直接照抄落地
- 边界划分克制且清晰:明确声明自己是'上游研究设计文档',把任务清单/脚手架/画图/数据构建/代码派给 a06/m09/m02/a03,模板里甚至显式标注'勿在此重复',有效防止技能间内容重叠膨胀
- 把'复现已有论文'纳为一等公民研究方案,五步协议(可验收复现目标→偏差预算→复现日志→失败三分归因)非常实战,尤其'不说复现这篇论文这种无法验收的目标'和失败归因的伦理边界(指向原文问题须走 research-ethics)考虑周到
- 防 p-hacking/HARKing 的预注册节给出 OSF/AsPredicted 真实流程 + 预注册字段↔实验矩阵字段映射表,并诚实区分验证性/探索性,是审稿人真正在意的点

## 缺点 / 可被质疑处
- plan_lint.py 校验偏'形式齐全'而非'语义正确':它只检查完成判定列非空,但 EXP-Bench 强调最易跑偏的恰是'结论判定与假设是否真对齐'。一行写 H1 对应假设、完成判定填'p<0.05'但指标与 H1 根本无关,脚本照样判为通过——四要素最难的语义一致性它管不到,有'绿了但错了'的风险(讽刺的是 references 自己引用了 TDD 的同名告诫)
- SKILL.md 正文与模板存在种子数口径的潜在矛盾:正文写'≥5个随机种子;算力受限≥3且须在m06显式标注',而功效分析又证明中效应需每组64次。模板默认给{{0,1,2,3,4}}5个种子,实际会诱导用户用一个对中小效应严重欠功效(power 0.108)的设置交差,'先做功效分析'的告诫容易被默认值淹没
- 工具栈全套(Hydra+DVC+Snakemake+MLflow/W&B+CCDS)对绝大多数本科生/小课题是重型过度工程,SKILL 未给'轻量档 vs 完整档'的分级裁剪指引。一个跑单数据集小模型的学生被要求配 DVC远端+Snakemake DAG+MLflow server,落地成本与收益严重不匹配,可能导致整套被弃用
- Snakemake references 自己注明'Windows 上 shell 兼容性一般,建议 WSL/Linux',而本技能运行环境是 Windows 11——把 Snakemake 列为推荐流水线工具,对实际用户存在可执行性落差,缺少 Windows 友好替代(如纯 Python/Make/Invoke)的并列建议
- 算力预算严重依赖云价单价,references 也承认'WebFetch 受限、未逐页核',且这是 2026-06 的快照价。模板要求'记来源+日期'是对的,但技能本身没有任何取价机制或参考价区间,用户仍需自行查价,预算环节落地度低于其它环节
- 大量 m-code/db-code(m02/m04/m06/m09/a03/a06/a02/db03/db04/db08/db09)散落正文,对不熟悉 Light 体系编号的人可读性差;尤其 db03(方法就绪)、db08、db09 在本技能内无任何展开说明,衔接全靠外部 CONVENTIONS,单独看本技能会有断点

## 可优化点（供后续逐技能优化）
- 给 plan_lint.py 增加'语义一致性'弱校验层:例如检查完成判定列里是否出现了该行指标列的关键词、是否含可量化阈值(数字/不等号/p值),对'完成判定只有定性词无门槛'给 warning;并新增对'同一假设是否至少有一个主实验+一个消融'的覆盖度检查,把校验从'每行齐全'升级到'假设-实验覆盖矩阵'
- 统一种子数口径并把功效分析做成可执行脚本:新增 power_check.py,输入预期效应量/种子数输出实际 power 与建议最小重复数,并在 experiment_matrix 模板默认行改为'{{种子数:由 power_check.py 反推}}'而非写死5个,让功效分析成为强制前置而非脚注
- 在 SKILL 增加'规划档位'分级(轻量/标准/完整):轻量档对应单机小课题只需 requirements锁版本+固定种子+目录约定+一个跑批脚本;完整档才上 DVC/Snakemake/MLflow,按项目规模给裁剪决策树,避免重型工具劝退小用户
- 针对 Windows 运行环境,给流水线工具补 Windows 友好并列项(如 invoke/纯Python driver/make for Windows),并在 Snakemake 条目标注'本机为 Windows,建议 WSL2 或改用 X',消除 references 已自承的可执行性落差
- 把 m-code/db-code 在 SKILL 末尾补一张'本技能涉及的衔接技能速查表'(编号→技能名→交什么),尤其展开 db03/db08/db09 指代,使本技能脱离 CONVENTIONS 也能自解释
- 算力预算补一个'参考价区间'内置表(按 GPU 型号给云价量级区间 + 取价日期 + 必须现查的提醒),或提供取价 checklist,降低预算环节对外部查价的硬依赖,即使过期也给用户一个起算锚点
- 为复现论文协议补一个独立的复现日志模板(templates/reproduction-log.md),把五步协议中的'逐次记录{改了什么/得到的数/与目标差/下一步假设}'落成可填表,目前该协议只有正文描述无配套工件

## 与其他 Light 技能/知识库的衔接
上游:严格依赖 m04(light-idea-critique)放行,并承接其 Revision Roadmap 的 must-fix(模板第0节有专门承接表);开工前依赖 m02(数据就绪)与 db03(方法就绪)。下游与横向:产出 PROJECT_PLAN.md/experiment_matrix.md 交 a03(light-backend-coding)落地代码与调试(复现论文的代码/日志也走 a03);目录脚手架交 a06(light-project-structure,模板显式让其生成而本技能不重复);框架图/可视化交 m09(figure-planning,正文还提 m11);里程碑与决策登记 a02(memory-pm)并写 db09 decision_log;实验跑完交 m06(light-result-analysis,功效/显著性口径与 m06 significance_test.py 的 BH-FDR 对齐)。关键回边:实验矩阵中鲁棒性/泛化/敏感性所需派生评测集作为派生数据规格回 m02 构建并回填 db04;算力预算口径与 db08(ip-application 经费预算)一致;失败归因指向原文问题时走 research-ethics。方法论上借鉴 EXP-Bench 与 obra/superpowers 五项工程纪律。

---

## GitHub 同类前沿技能对标

同类生态分两大阵营,而 light-research-plan 不属于其中任何一个的主流形态。第一阵营是"全自动 AI 科学家"(SakanaAI AI-Scientist、HKUDS AI-Researcher、InternAgent、Agent Laboratory、MLR-Copilot、Curie),它们追求 idea→实验→跑代码→写论文的端到端闭环,实验设计只是被一笔带过的中间环节,几乎都把"设计严谨性/可验收判定"让位于"能跑通+刷指标"。第二阵营是"技能市场"(K-Dense scientific-agent-skills、AI-research-SKILLs),把实验设计、统计功效、可复现拆成各自独立的原子技能,覆盖广但彼此孤立,没有"先过 idea 审查、再产出可证伪方案、再派发下游任务"的串接编排。light-research-plan 的独特点正在于:它不抢着跑实验,而是把自己钉死在"上游研究设计文档"这一格,用 EXP-Bench 四要素 + plan_lint.py 离线强校验、用 TTestIndPower 反推样本数纠正种子误区、用明确工具栈落地可复现,并通过编号 pipeline 把代码/画图/数据派回专职技能。也就是说,主流项目要么全自动黑箱、要么松散技能堆叠,而 Light 这个技能填的是"严谨的、可审计的、人在环中的研究方案设计"这块被普遍轻视的空白。它最接近的"精神同类"其实是 EXP-Bench 的四要素评测范式和各家零散的 Rigor Reviewer,但没有任何一个开源项目把这套校验做成可直接产出方案文档的技能。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 面向 Claude/Cursor/Codex 的现成 Agent Skills 合集,含 Experimental Design(随机化/区组/析因 DOE,pyDOE3)、Statistical Power(t检验/ANOVA/比例的样本量与功效)、Hypothesis Generation、Arbor(假设树精修+留出测试门防过拟合)等技能。与 light 同为 Agent Skills 形态,功能领域高度重叠。 | 28.1k | v2.52.0,2026-06-12 | 强:技能数量多(140+)、统计/DOE 工具更专业(pyDOE3、statsmodels、PyMC),领域覆盖生化医药广;有专门的 Statistical Power 技能正面对标 light 的功效分析。弱:各技能彼此孤立,没有'idea 审查→可证伪方案→派发下游'的编排串接;没有 plan_lint 式的离线四要素强校验把'设计'和'结论判定'作为重点核查项;定位是工具箱而非'上游研究设计文档'。 |
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 首个端到端全自动科学发现系统:从 idea 生成、跑实验、写论文到自动评审一条龙,内置 NanoGPT/2D Diffusion/Grokking 模板,支持多家 LLM 与 Semantic Scholar/OpenAlex 文献检索。 | 14k | unknown(无 release,页面未暴露最近 commit 日期) | 强:全自动闭环、影响力大、生态成熟、能真正跑实验出论文。弱:实验设计是被一笔带过的中间步骤,缺乏可证伪/可验收的强约束;不做功效分析反推样本量;以'刷通指标'为导向而非'方案可审计';黑箱程度高、需 Docker 沙箱跑 LLM 生成代码,与 light'人在环中产出设计文档'的定位正相反。 |
| [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | AI-Scientist 升级版,去掉人工模板、用渐进式 agentic 树搜索(BFTS,experiment manager agent 引导)做实验探索,自动生成假设、跑实验、写稿,曾产出通过同行评审的 workshop 论文。 | 6.6k | unknown(无 release,页面未暴露最近 commit 日期) | 强:树搜索式实验探索更通用、num_seeds/num_workers 等并行探索参数化、开放式探索能力强。弱:实验设计交给树搜索自动展开,缺人可读的'四要素齐全'方案文档与离线校验;不强制可证伪假设与完成判定;复现靠脚本而非 Hydra/DVC/MLflow 工具栈规范;同样是自动跑代码黑箱路线。 |
| [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | 端到端自主研究工作流,三阶段(文献综述→实验→报告写作),含 plan-formulation 实验计划制定步骤,集成 arXiv/HF/Python/LaTeX,有 Co-Pilot 人参与模式和 AgentRxiv 共享框架。 | 5.7k | unknown(无 release,页面未暴露最近 commit 日期) | 强:有显式 plan-formulation 阶段、Co-Pilot 人在环模式、AgentRxiv 让 agent 间复用研究。弱:实验计划是流程内一环、非可独立审计的方案文档;无四要素离线校验、无功效分析、无可复现工具栈强约束;不做'派发下游专职技能'的模块化分工。 |
| [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher) | 自主科研系统(NeurIPS 2025 Spotlight),支持 Level1(详细 idea)/Level2(仅给参考论文自动生 idea)两级输入,走 设计→实现→验证→精修 循环,附 CV/NLP/DM/IR 四领域含新颖性/实验完备性等维度的基准。 | 5.5k | unknown(最新 news 2025-09,页面未暴露 commit 日期) | 强:有明确 Design→Validation→Refinement 循环并强调实验完备性,自带多维评测基准。弱:设计阶段偏'概念开发+实现策略'而非可证伪假设+完成判定的强结构;无 plan_lint 式逐行四要素校验;无功效分析反推样本;全自动跑实验,人审计空间小。 |
| [zechenzhangAGI/AI-research-SKILLs](https://github.com/zechenzhangAGI/AI-research-SKILLs) | Orchestra Research 维护的 AI 研究/工程技能库('idea 到 paper'),含 Autoresearch 全生命周期编排、Ideation(头脑风暴/创意思维)、ARA Rigor Reviewer(对可证伪性/方法严谨性打分)、NeMo Evaluator 容器化可复现评测等。 | 9.6k | v1.6.0 约 2026-04;最新 tag v1.4.0,2026-03-16 | 强:同为 Agent Skills 形态、技能多(98+)、有 ARA Rigor Reviewer 直接对标'可证伪/严谨性'审查、有 Autoresearch 编排。弱:无独立的实验设计技能、无统计功效技能、无专门可复现技能;偏工程与编排,缺 light 的四要素强校验和样本量反推这类硬约束工具。 |
| [InternScience/InternAgent](https://github.com/InternScience/InternAgent) | InternAgent-1.5 长周期自主科学发现统一框架,覆盖物理/生物/地球/生命科学的算法发现与干湿实验,支持从 idea 或已有 idea 文件起跑,带持久记忆(避开失败方向)和 Deep Research 子任务分解模块。 | 1.3k | unknown(最新 news 2026-05-07,页面未暴露 commit 日期) | 强:长周期、跨学科(含干湿实验)、持久记忆复用经验、Deep Research 分解能力。弱:面向自动发现而非产出可审计设计文档;无四要素离线校验、无功效分析;复现靠框架而非显式工具栈规范;人审计/可证伪约束弱。 |
| [drivendataorg/cookiecutter-data-science](https://github.com/drivendataorg/cookiecutter-data-science) | 数据科学项目标准化目录脚手架(data/notebooks/src 等),V2 带 ccds 命令行,业界事实标准的可复现项目结构模板。 | 9.9k | v2.3.0,2025-07-24 | 强:可复现项目结构的事实标准、社区极成熟、被广泛采用。弱:只做目录脚手架,完全不涉及假设/实验矩阵/结论判定/功效分析;是 light 在'目录脚手架'环节会派给 m02/m09 之类下游的工具,而非研究设计同类——可作为 light 可复现清单里推荐的落地模板之一。 |
| [du-nlp-lab/MLR-Copilot](https://github.com/du-nlp-lab/MLR-Copilot) | 基于 LLM agent 的自主 ML 研究框架,IdeaAgent 从论文生成研究假设与实验计划,ExperimentAgent 用检索到的原型代码实现并运行实验,支持人反馈与迭代调试。 | 69 | unknown(页面未暴露最近 commit 日期) | 强:明确区分'假设+实验设计'(IdeaAgent)与'实现执行'(ExperimentAgent),与 light'设计与落地分离'理念相近;支持人反馈。弱:实验计划无四要素强结构与离线校验;无功效分析;无可复现工具栈规范;偏跑通而非可验收;社区很小。 |
| [Just-Curieous/Curie](https://github.com/Just-Curieous/Curie) | 号称首个面向'严谨'自动科学实验的 AI-agent 框架,覆盖 假设→实现→执行→结果分析→反思 全程,内置验证模块强调方法规范、可靠性与可复现性,自动产出实验报告/结果 notebook/可复现脚本。提出 EXP-Bench(四要素:研究问题/设计/实现/结论判定),正是 light 实验条目结构的来源范式。 | 363 | unknown(最新 news 2025-06,页面未暴露 commit 日期) | 强:同样把'严谨性/可复现'作为卖点、内置 verification 模块、且是 EXP-Bench 四要素范式的提出方(light 直接借用其结构)。弱:仍是自动跑实验出报告的执行框架,而非人可审计的上游设计文档;无 plan_lint 式逐行四要素离线门禁;无功效分析反推样本;star 较小。 |
| [Just-Curieous/EXP-Bench](https://github.com/Just-Curieous/EXP-Bench) | 评测 AI agent 完成科研实验任务的基准/评测 harness,为每个 task+LLM+Agent 起干净 Docker 容器,跑生成+评判两阶段,支持 OpenHands/Iterative Agent 与多家 LLM。其论文定义了实验四要素结构。 | 6 | unknown(work in progress,页面未暴露 commit 日期) | 强:四要素(研究问题/设计/实现/结论判定)评测范式正是 light 实验矩阵的理论基础,直接相关。弱:是评测基准而非生产方案的技能/工具;不产出研究方案;仓库极早期(6 star、6 commit、明示频繁变动)。可作为 light 引用四要素出处与对齐评测口径的参考。 |

### Light 该技能可借鉴的点
- 借鉴 K-Dense 的 Statistical Power 技能形态,把现有 TTestIndPower 功效分析扩成可复用脚本/子技能,覆盖 ANOVA、比例、相关、回归等多场景,并补充 simulation-based 功效估计(纯闭式公式在复杂设计下会失真)。
- 引入 DOE 工具(如 pyDOE3)支撑析因/分数析因/区组/交叉设计,让实验矩阵不止枚举,而能按正交设计自动生成条目,减少'拍脑袋列实验'的遗漏。
- 参考 AI-research-SKILLs 的 ARA Rigor Reviewer 与 Curie 的 verification 模块,把 plan_lint.py 从'四要素齐全'的格式校验升级为'严谨性评分'(可证伪性、是否有 ablation、是否防数据泄漏、判定阈值是否预注册),输出可审计评分卡。
- 吸收 InternAgent 的持久记忆思路,在派发下游(a03/a06/m09/m02)时记录已失败/已验证的设计方向,避免续作里重复踩坑。
- 把 cookiecutter-data-science(ccds)作为可复现清单里推荐的具体落地模板直接引用,并补 version pinning(release tag/commit SHA)规范,让'可复现'从工具点名变成可执行脚手架。
- 学 SakanaAI-v2 与 AI-Scientist 的 ideation 输出结构,把'已过 m04 idea 审查'的产物固化成带 novelty 检查(Semantic Scholar/OpenAlex)的结构化 JSON,使方案与上游 idea 之间的衔接可机读、可校验。
- 对齐 EXP-Bench 公开的四要素评测口径与数据集,让 light 产出的实验条目能被该基准式标准直接打分,增强方案'可被第三方验收'的客观性。
- 借鉴 MLR-Copilot 显式分离 IdeaAgent/ExperimentAgent 的做法,在文档里更清晰地标注每个实验条目的'设计责任'与'实现责任'边界,强化派发下游技能时的接口契约。
