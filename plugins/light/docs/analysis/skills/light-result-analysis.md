# light-result-analysis — 深度分析与同类对标

> 源：[`skills/light-result-analysis/SKILL.md`](../../../skills/light-result-analysis/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：实验跑完后的"结果深度分析"技能:把"看起来更好"升级为"统计上显著更好",并配套 5 个自测通过的即用 Python 脚本(自动选检验/效应量/FDR、出版图、泄漏体检、SHAP)+ 四段式报告模板,衔接 m05 补实验与 m07/m09 写作绘图。

## 核心运行逻辑
SKILL.md 用"描述→解释→诊断→洞察→行动"五层递进框架组织分析思路,核心方法论是"p 值 + 效应量(Cohen's d) + 置信区间 + BH-FDR 校正"四件套,并强调三个常被忽视的统计点:配对设计识别(同种子/折用配对 t/Wilcoxon,功效更高)、切片分析(防聚合指标掩盖子群失败)、泄漏/过拟合体检。脚本层把这套方法论落地为可执行工具:significance_test.py 是经 scipy/statsmodels 对齐自测的统计原语库,analyze_results.py 按 Shapiro 正态性与组数自动派发检验(Welch/Mann-Whitney/ANOVA+Tukey/Kruskal),make_figs.py 出 dpi300 矢量出版图,leakage_overfit_check.py 纯 numpy 查泄漏,explain_shap.py 产 SHAP 三图。设计上贯彻"复用 code_assets 已验证统计""可选依赖优雅降级(deepchecks/shap 缺失不崩)""每脚本带合成自测"三原则。references.md 是 13 个工具的逐工具笔记(API+坑),作为不可执行的查阅层。

## 关键步骤
- 1. 1. EDA 体检:分布/缺失/相关/异常值,先看形状再下结论(references 给出 ydata-profiling/deepchecks 用法,但无对应脚本,需手工)
- 2. 2. 跑 analyze_results.py:输入结果 CSV,自动出每组 EDA 摘要(n/均值±std/95%CI/正态性)+ 自动选 omnibus 检验 + 每对 Cohen's d + BH-FDR,落 summary.json/md;方法共享种子时加 --paired-by 启用配对检验
- 3. 3. 跑 leakage_overfit_check.py:train/val/test gap + 特征-标签高相关泄漏 + 重复行 + 近常量列,落 leakage_report.json(verdict CLEAN/FLAGS RAISED)
- 4. 4. 跑 explain_shap.py:对模型出 beeswarm/bar/waterfall 三图(可解释性证据)
- 5. 5. 跑 make_figs.py:出方法对比柱状图(带CI)/箱线+散点/学习曲线/热图四类出版级图
- 6. 6. 按 result_analysis_report_template.md 填四段式报告(现象→原因→证据→对论文的意义)+ 亮点/异常/待补实验/推荐图表清单
- 7. 7. 衔接交付:亮点→m07,异常/不足→回 m05/m03,结论→db09,推荐图→m09/m11

## 自带资产
- scripts/significance_test.py — p+Cohen's d(Hedges校正)+mean-diff CI+bootstrap CI+BH-FDR 函数库,__main__ 逐函数对齐 scipy/statsmodels 打印 ALL PASS,复用 code_assets/stats_tests.py(welch_t/benjamini_hochberg/wilson_ci)
- scripts/analyze_results.py — 结果表 CSV 一键分析,按正态性+组数自动选检验,支持 --paired-by 配对检验(d_z + bootstrap 差值CI),输出 summary.json/md
- scripts/make_figs.py — OO matplotlib 出版模板,constrained_layout+viridis色盲友好+误差棒+dpi300矢量,builder: grouped_bar_ci/box_strip/line_with_band/heatmap+save_all
- scripts/leakage_overfit_check.py — 纯 numpy/pandas 的泛化gap+特征泄漏+重复行+近常量列体检,deepchecks 缺失自动降级
- scripts/explain_shap.py — SHAP 出图,TreeExplainer→Explainer→KernelExplainer 三级派发,封装 SHAP 存图坑,shap 缺失优雅降级 exit 0
- examples/worked_example.py — 端到端串联五脚本+生成填好的 example_report.md,全部写入 example_out/
- assets/result_analysis_report_template.md — 四段式报告模板,含元信息/描述层/关键发现/亮点/异常/待补实验/推荐图表/诚实标注八节
- references.md — 13 个工具(EDA/统计/matplotlib/seaborn/SHAP/statsmodels/networkx/plotly/altair/deepchecks/Evidently/ydata-profiling/Jupyter)逐工具笔记+配对设计识别+切片分析协议两节深度方法

## 优点
- 统计严谨度高且可落地:不只喊口号,significance_test.py 真的把 Cohen's d 的 Hedges 校正、Welch df、bootstrap CI 都对齐 scipy 做了数值自测(diff<1e-9),这是大多数同类技能缺失的'正确性锚点'
- 抓住了两个论文里最高频的统计误用并给了工具:配对 vs 独立检验识别(--paired-by 自动按共享列对齐,用 d_z 而非独立 d)和切片分析(防 85% 整体掩盖 50% 子群),references 对这两点的解释到位且符合审稿人关注点
- 工程鲁棒性好:可选依赖(deepchecks/shap)缺失时优雅降级而非崩溃,explain_shap 还专门封装了 SHAP 在 Agg 后端 show=False→gcf→save 的存图坑,每个脚本都有合成自测和无参 demo,可直接验证
- 脚本间复用清晰、不重复造轮子:analyze_results 复用 significance_test,后者复用 code_assets/stats_tests,explain_shap 复用 make_figs 的 save_all 和 house style,体现单一真相源思想
- 诚实标注文化贯穿始终:报告模板第 7 节强制区分'已验证/推测/不能过度声称',SKILL 反复强调'SHAP 非因果''p<0.05≠效应大''小 n 切片禁强结论',符合科研诚信
- 交接契约明确:产出对应到 CONVENTIONS §6.1 的阶段工件,亮点→m07、异常→m05、图→m09/m11、结论→db09,在多技能编排里定位清楚

## 缺点 / 可被质疑处
- 核心交接工件名实不符:SKILL.md 和 CONVENTIONS §6.1 都把 claim_evidence_table.md 列为交 m07/m09 的标准工件,但技能里既无该文件的生成脚本也无模板,assets 下只有 result_analysis_report_template.md,worked_example 产出的也叫 example_report.md——这个被反复强调的'标准工件'实际无人产出
- 自动选检验的正态性判定在推荐样本量下统计失效:SKILL 推荐 ≥5(算力受限≥3)种子,而 _normal() 用 Shapiro 在 n=5~8 时检出非正态的功效极低,几乎总判'正态'→默认走 Welch/ANOVA,恰恰在最需要稳健检验时失灵;且 n<3 直接 return True 更是无依据假定正态
- ANOVA 路径缺方差齐性检验:k≥3 正态时直接 f_oneway(经典 ANOVA 假设等方差)+Tukey,但 2 组时却用不假设等方差的 Welch,逻辑不自洽;references 列了 het_breuschpagan 却未在脚本里对多组做 Levene/Welch-ANOVA,异方差下 ANOVA 会失真
- 多重比较校正范围不完整:BH-FDR 只在'每 metric 内跨配对'校正,跨 metric(acc/f1/auroc 同时报)不校正,多指标多方法时家族错误率仍膨胀;omnibus 与 pairwise 的检验选择各自独立判正态,可能出现 Kruskal 显著但配对却走 Welch 的不一致
- 切片分析与公平性'只说不做':references 用大篇幅写了切片协议、SKILL 必查清单列了切片/公平性,但 analyze_results.py 只有 --paired-by 没有 --slice-by,公平性维度无任何脚本支撑,落地全靠人工 groupby,与配对设计已脚本化形成明显落差
- references 列的工具大半无脚本兜底:ydata-profiling/deepchecks 全套/Evidently 漂移/networkx 中心性/plotly/altair/Jupyter Book 都只在 references 有 API 笔记,且作者自述本环境 WebFetch 被拦截、API 以'检索片段+公认接口'为准、版本敏感处需用户自核——即这些 API 细节未经实际运行验证,与脚本层'自测跑通'的可信度不在一个量级

## 可优化点（供后续逐技能优化）
- 补 claim_evidence_table.md 的模板与生成器:在 analyze_results.py 增 --emit-claim-table,把每个显著比较(claim)自动连到证据字段(检验/p/q/d/CI/n)落盘成 CONVENTIONS §6.1 要求的表,消除名实不符;或至少在 assets 下加该模板
- 把切片分析脚本化:给 analyze_results.py 加 --slice-by <col>,对每个切片复算同一套 EDA+检验+效应量+FDR 并带 n,自动标注小 n 切片(如 n<某阈值)为'样本不足待核查',输出切片×方法热图数据,兑现 references 的切片协议
- 修正多组检验的稳健性:k≥3 正态时加 Levene 方差齐性检验,不齐则自动切 Welch-ANOVA(scipy 1.6+ 或 pingouin);Kruskal 后用真正的 Dunn 检验(scikit-posthocs)而非笼统'pairwise Mann-Whitney 注释';并对小样本默认提示 Shapiro 功效不足、建议直接用非参或预设检验
- 扩展 FDR 校正范围并让 omnibus/pairwise 检验选择一致:提供跨 metric 的统一校正选项;pairwise 的配对/独立、正态/非正态选择应继承 omnibus 的判定,避免同一分析内检验家族混用
- 给 leakage_overfit_check 的阈值加 CLI 参数:GAP_OVERFIT/GAP_SHIFT/LEAK_CORR/NEAR_CONST 现全硬编码 0.05/0.05/0.95/0.999,而合理 gap 阈值强依赖任务,应可 --gap-overfit 等覆盖,并在报告里说明阈值仅为启发式
- 加 requirements.txt/环境清单与依赖真实性核验:技能依赖 scipy(Shapiro/Mann-Whitney 硬需求)、可选 statsmodels/shap/deepchecks 却无任何 manifest;同时把 references 中版本敏感的 Evidently/deepchecks API 在装好库后实跑一遍核对签名,降低'未验证 API'风险
- explain_shap 自测对 shap 缺失场景仅 exit 0 通过,应在 CI 里区分'真验证过 SHAP 路径'与'仅跳过',避免'全部自测跑通'被误读为 SHAP 功能已验证

## 与其他 Light 技能/知识库的衔接
["上游 m05(light-research-plan):种子数口径(≥5/受限≥3)与本技能必查清单同口径;待补实验清单回流 m05 补设计。", "上游 m03(light-idea-*):异常/不足回流提新 idea。", "下游 m07(light-paper-drafting):亮点清单+claim↔证据表作为写作支撑(经 claim_evidence_table.md,当前缺生成器)。", "下游 m09(light-figure-planning)/m11(light-figure-drawing):推荐图表清单交规划与绘制;make_figs 的 house style 与 light-figure-drawing 应保持一致(references 引用了 scientific-visualization 评审维度)。", "横向 a10(疑为 light-research-ethics 公平性):切片分析的敏感属性维度与公平性必查项关联,但本技能未脚本化。", "底层 code_assets/stats_tests.py:significance_test 复用 welch_t/benjamini_hochberg/wilson_ci(其中 wilson_ci 被导入但本技能未实际使用;cohens_d/mean_diff_ci/bootstrap_ci 为本技能新增、不在 code_assets)。", "规范 CONVENTIONS.md §4(已验证/推测标注)、§6.1(阶段工件契约);结论写入 databases 的 db09。"]

---

## GitHub 同类前沿技能对标

Light 的 result-analysis 是一个"方法论 + 即用脚本 + 工具笔记"三层一体的 agent skill,定位在"实验跑完到论文成稿"之间的统计分析环节,把 p 值/效应量/置信区间/BH-FDR 四件套、配对设计识别、切片分析、泄漏体检、SHAP 解释打包成一条可执行流水线,并强调优雅降级与合成自测。GitHub 上的同类生态分成两类:一类是单点能力的成熟 Python 库(shap、deepchecks、pingouin、deep-significance、tea-tasting),它们在各自领域比 Light 的脚本更深更经过实战检验,但都只覆盖 Light 的一个子模块,且不是为 LLM agent 编排设计的;另一类是 agent skill 集合(K-Dense scientific-agent-skills、claude-scholar、claude-code-templates),它们在"被 agent 调用"这点上同构,但要么偏生物化学领域、要么把统计分析作为众多技能之一带过,缺少 Light 这种"五层框架 + 自动选检验 + 泄漏/SHAP 一条龙"的深度统计专精。综合看,Light 的差异化在于"统计严谨方法论 + 自动派发检验 + 端到端落地脚本"被收敛进单个面向 agent 的技能;它的弱点是底层统计原语的成熟度和社区验证远不及那些专业库,本质上是站在这些库肩膀上的编排层。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [shap/shap](https://github.com/shap/shap) | 博弈论 Shapley 值的统一模型解释库,几乎是 SHAP 解释的事实标准,支持树模型/深度模型/核方法多种 explainer 与全套可视化(beeswarm、waterfall、force、dependence) | 25522 | 2026-06-12 | 强:explain_shap.py 实际就是对它的封装,shap 本身的算法深度、explainer 覆盖面、可视化丰富度远超 Light 的三图脚本。弱:它只是纯解释库,不含统计显著性检验、检验自动派发、报告模板,也不是面向 agent 的技能,Light 把它收敛进端到端分析流水线并做了缺失降级处理 |
| [deepchecks/deepchecks](https://github.com/deepchecks/deepchecks) | ML 数据与模型的持续验证框架,内置 train-test 泄漏、数据漂移、单特征预测力、标签泄漏等成套检查,以 Suite/Check/Condition 三级结构组织 | 4023 | 2025-12-28 | 强:泄漏检测的检查项远比 leakage_overfit_check.py 系统、分类清晰且经工业验证。弱:体量重、需较多依赖,不做显著性检验与效应量,也无 agent 技能封装;Light 的泄漏脚本是纯 numpy 轻量实现,可在无 deepchecks 时降级运行 |
| [raphaelvallat/pingouin](https://github.com/raphaelvallat/pingouin) | 基于 Pandas 的统计库,t 检验/ANOVA/非参数检验/相关/效应量/功效分析一应俱全,每个检验输出含效应量、置信区间、贝叶斯因子、功效的整洁表格 | 1918 | 2026-04-05 | 强:统计方法覆盖面与输出完整度(一次给齐效应量/CI/功效/贝叶斯因子)成熟度高于 significance_test.py。弱:仅是库,需用户自己决定用哪个检验、自己做 FDR 编排和报告;Light 的 analyze_results.py 在它之上加了'按正态性与组数自动派发检验 + FDR + 报告'的决策层 |
| [Kaleidophon/deep-significance](https://github.com/Kaleidophon/deep-significance) | 面向深度学习的显著性检验包,核心是 ASO(Almost Stochastic Order)检验,处理多随机种子、非正态、小样本的模型比较,并含多重比较校正 | 339 | 2024-07-01 | 强:ASO 检验针对深度学习场景比传统 t/U 检验更稳健,这正是 Light 自动派发逻辑里缺的一环。弱:专注单一方法、近两年未更新,不含切片分析/泄漏/SHAP/报告;Light 覆盖更广但深度学习专项检验不如它 |
| [e10v/tea-tasting](https://github.com/e10v/tea-tasting) | A/B 实验统计分析 Python 包,支持 Student t/Z 检验、Bootstrap、CUPED 方差削减、多指标与多重比较的统一分析接口 | 328 | 2026-06-12 | 强:A/B 场景的方差削减(CUPED)与多指标编排比 Light 成熟,活跃更新。弱:聚焦在线实验/A-B 域,不覆盖 ML 模型比较、SHAP、泄漏;Light 的切片/多指标分析可借鉴其 CUPED 提升功效 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/k-dense-ai/scientific-agent-skills) | 号称第一的科研 agent skills 库,140+ 技能 + 100+ 科学数据库,覆盖生物/化学/医学/药物发现,兼容 Cursor/Claude Code/Codex 等并遵循开放 Agent Skills 标准 | 28080 | 2026-06-12 | 强:规模、跨平台兼容、社区影响力(自称 16 万科学家使用)远超单个 Light 技能,与 Light 同为 agent skill 形态。弱:偏湿实验/生化领域,统计结果分析不是其专精,缺少 Light 这种'四件套 + 自动选检验 + 泄漏/SHAP'的深度统计技能 |
| [Galaxy-Dawn/claude-scholar](https://github.com/galaxy-dawn/claude-scholar) | 半自动科研助手,覆盖选题/编码/实验/写作/发表全流程,内含 results-analysis 技能,支持 Claude Code/Codex/Kimi/OpenCode 多 CLI | 4297 | 2026-06-05 | 强:全流程覆盖与多 CLI 支持,定位与 Light 科研技能包高度同构,也有专门的 results-analysis 技能可直接对标。弱:其结果分析技能的统计深度(自动派发/FDR/泄漏体检/SHAP 即用脚本)需逐项比对,通常不如 Light 把方法论落地为 5 个自测脚本那样细;是 Light 最直接的同类竞品 |
| [kdis-lab/StaTDS](https://github.com/kdis-lab/StaTDS) | 算法结果统计检验与比较库,提供参数/非参数检验、多算法多数据集比较的事后检验与校正,并能生成 LaTeX/PDF 报告 | 18 | 2026-03-30 | 强:多算法跨数据集比较的事后检验(Nemenyi 等)与自动报告生成,正对应 Light 的多组比较 + 报告需求,且持续更新。弱:star 少、纯库无 agent 封装、不含泄漏/SHAP;Light 的报告模板可借鉴其 LaTeX 输出 |
| [Brritany/MLstatkit](https://github.com/Brritany/MLstatkit) | 把成熟统计方法集成进 ML 工作流的 Python 库,含 Delong 检验比较 AUROC、Bootstrap 置信区间、最优阈值等 | 30 | 2025-09-19 | 强:Delong 检验比较两条 ROC 的 AUC 差异是 significance_test.py 缺的实用原语,医疗/分类评估场景常用。弱:覆盖窄、无检验自动派发与报告;Light 可吸收其 Delong/Bootstrap CI 原语 |
| [hendersontrent/correctipy](https://github.com/hendersontrent/correctipy) | 计算相关样本(如交叉验证折间)下校正后检验统计量的 Python 包,实现 Nadeau-Bengio 等修正以避免低估方差 | 11 | 2023-01-12 | 强:专门解决 CV 折间相关性导致的假阳性问题,补足 Light 配对设计识别里对'相关样本方差校正'的处理。弱:单一功能、2023 年后未更新、star 少;Light 可在配对/折交叉场景引入其校正逻辑 |
| [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) | Claude Code 配置与监控的 CLI 工具,聚合官方/社区/K-Dense 科学技能等大量 agent 组件供一键安装 | 28000 | 2025-11-15 | 强:作为技能分发/安装平台与监控工具,生态聚合与影响力大,Light 若要扩散可作为发布渠道。弱:本身不是统计分析技能,页面未把统计分析单列为类别;与 Light 是'平台 vs 单技能'关系而非功能直接竞争 |

### Light 该技能可借鉴的点
- deep-significance 的 ASO(Almost Stochastic Order)检验:针对深度学习多随机种子、非正态、样本量小的场景,比标准 t/Mann-Whitney 更稳健,Light 的 analyze_results.py 自动派发逻辑里可以增加 ASO 作为深度学习场景的可选检验
- correctipy / Nadeau-Bengio 校正:同一数据集上交叉验证产生的折间结果是相关样本,普通配对 t 检验会低估方差、高估显著性,Light 强调了配对设计识别,但可进一步引入这种针对 CV 相关性的方差校正检验
- deepchecks 的结构化 Suite/Check/Condition 三级抽象与 train-test 泄漏专项检查(数据漂移、单特征预测力、日期泄漏、索引泄漏),Light 的 leakage_overfit_check.py 可借鉴其分类化的泄漏检查清单而非只做通用检测
- pingouin 的输出范式:每个检验直接返回带效应量、置信区间、贝叶斯因子、检验功效的 DataFrame 一行,Light 的报告模板可对齐这种'一次检验全要素输出'的表格化呈现
- tea-tasting 的 CUPED 方差削减与多重比较场景下的统一分析接口,Light 在切片/多指标分析时可引入方差削减提升功效
- K-Dense scientific-agent-skills 与 claude-scholar 的跨 agent 兼容(Cursor/Codex/Claude Code/开放 Agent Skills 标准)与数据库配套模式,Light 若要扩大使用面可考虑遵循开放 Agent Skills 标准做跨平台适配
