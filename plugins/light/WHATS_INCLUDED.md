# 脚本与模板清单

本仓库各技能内置的可运行脚本与可套用模板，按技能归类。脚本以纯 Python/常见科学计算库为主，均应至少可 `py_compile`、带真实 `__main__` 入口，并覆盖显式离线 `--selftest`。

> 本清单由 `.github/scripts/check_skill_assets.py` 防漂移：新增/删除 `skills/light-*/scripts/*.py` 后必须同步本表，否则 CI 失败；`.github/scripts/run_skill_selftests.py` 会实际执行全部脚本的 `--selftest`。

## 可运行脚本

| 技能 | 脚本 | 作用 |
|------|------|------|
| citation | `scripts/citekey_audit.py` | \cite 键↔.bib 键双向对账：缺失键(编译??)/冗余键/重复定义/authorYearWord 命名校验，支持 LaTeX 与 pandoc 语法 |
| citation | `scripts/doi_to_any.py` | DOI 转 BibTeX / CSL-JSON / GB/T 7714，中文条目自动注入 `langid` |
| citation | `scripts/verify_citation_edge.py` | 核验“A 是否引用 B”，返回 confirmed / not_in_open_index / unknown 三态(OpenCitations / Semantic Scholar) |
| citation | `scripts/verify_refs.py` | 批量 DOI 真实性、元数据一致性与开放获取状态核验，产 JSON 报告 |
| competition | `scripts/market_charts.py` | 市场分析 JSON 渲染为 TAM/SAM/SOM、竞品定位矩阵、五力分级、风险热图 |
| competition | `scripts/roadmap_gen.py` | 里程碑 JSON 渲染技术路线图 / 甘特图，支撑申报书与路演路线页 |
| competition | `scripts/scorecard.py` | 评委视角自审评分卡：逐维度自评 JSON 按赛事维度加权求总分 + 薄弱项 + 对照 anti_patterns 红旗，权重为经验相对参考非官方分值 |
| consistency | `scripts/consistency_audit.py` | 读取 db09 术语/方法/指标事实源，跨论文/PPT/文档检测术语、指标名、指标值与覆盖缺口 |
| data-engineering | `scripts/check_access_level.py` | 数据访问分级守门：阻断 raw 数据流向 paper/figure/public-repo 等公开产物 |
| data-engineering | `scripts/croissant_export.py` | 数据卡字段 → Croissant JSON-LD（MLCommons 机器可读标准），便于发布 HF/Kaggle/OpenML 被自动索引（最小骨架，标注须官方库校验） |
| data-engineering | `scripts/data_doctor.py` | CSV → Markdown 数据体检报告：形状、类型、缺失、重复、异常值、强相关、泄漏提示、inf/混合类型/类不均衡/偏态/稀有类 |
| data-engineering | `scripts/data_feasibility.py` | 数据先行四问 → data_feasibility.md（交 m03/m04）：四问各 ok/warn/insufficient + 依据，insufficient 退出码 1 当"不进 m03"闸门 |
| data-engineering | `scripts/derive_eval_set.py` | m05 派生数据回边的可执行实现：据规格生成加噪/缺失/跨域/扫参评测集 + 对齐 db04 的 dataset_card 字段（只动特征不碰标签、固定种子） |
| data-engineering | `scripts/drift_check.py` | 两数据集分布漂移检验：数值列 KS+PSI、类别列卡方+PSI，纯 numpy(p 渐近近似)，以 PSI 效应量为主 |
| data-engineering | `scripts/emit_artifacts.py` | m02 标准工件落位守门：核 quality_report/data_card/data_feasibility 落 §6.1 标准名，打印 passport 登记命令 |
| data-engineering | `scripts/quality_gate.py` | 按 YAML 规则校验 CSV，输出 PASS/FAIL 数据质量门报告，退出码可接 CI |
| data-engineering | `scripts/safe_split.py` | 构建防泄漏 split + Pipeline/ColumnTransformer，支持 clf/reg/timeseries/group 任务 |
| data-engineering | `scripts/sample_size_check.py` | 数据规模充足性经验预警：分类每类最小样本/回归样本特征比(EPV)/检测每类实例数，把"四问"之规模变可计算（标注非 power analysis） |
| figure-drawing | `scripts/color_palettes.py` | 投稿级配色工具：Okabe-Ito、连续/离散色图、灰度与色盲模拟预览 |
| figure-drawing | `scripts/figure_export.py` | 按目标期刊栏宽精确导出矢量+位图，校验物理尺寸与缩放后字号 |
| figure-drawing | `scripts/figure_integrity_lint.py` | 图表诚实性静态扫描：y 轴截断、双 y 轴、bar 无误差棒、jet/rainbow、3D 扭曲等 |
| figure-planning | `scripts/recommend_chart.py` | 图型启发式推荐：数据字段+分析任务→候选图型排序+理由（Cleveland-McGill 感知精度先验），喂规划卡再校验 |
| figure-planning | `scripts/validate_plan_card.py` | 规划卡契约校验：target_journal/column 命中 figure_export JOURNAL_SPECS、figure_id 唯一、source_card 必填，把 m11 打回前移到规划阶段 |
| file-reading | `scripts/docx_read.py` | DOCX 结构读取：段落、表格、标题层级与基本元数据归一化 |
| file-reading | `scripts/pdf_ops.py` | PDF 读取与结构操作：文本/页级信息抽取、合并拆分等轻量操作 |
| file-reading | `scripts/xlsx_read.py` | XLSX 工作簿读取与数据画像：sheet、表头、行列、缺失与样例预览 |
| frontend-design | `scripts/ai_tell_lint.py` | 机械检测“AI 生成感”前端文案/界面痕迹，提示模板腔、空泛词和常见坏味道 |
| frontend-design | `scripts/audit_checklist.py` | 前端布局质量可计算检查：对齐、间距、层级、密度、可读性等清单化输出 |
| frontend-design | `scripts/contrast_lint.py` | WCAG 2.1 对比度门禁：解析 token/CSS 变量 hex 两两组合算相对亮度对比度，按正文4.5:1/大字3:1/UI3:1 判 PASS/FAIL，纯 stdlib |
| memory-pm | `scripts/check_project_card.py` | db09 项目卡细粒度校验（补 check_databases 未覆盖项）：绝对日期格式、current_stage 枚举、decision_log/version_history 行格式、handoff parent_session 链可达 |
| memory-pm | `scripts/version_tag_reconcile.py` | version_history 各版本 vN 与 git tag 两段对账，列出"有tag无记录/有记录无tag"，落地 SKILL 反复强调的 tag 对齐纪律 |
| orchestrator | `scripts/passport.py` | .light/passport.yaml 台账工具：init/append-stage/get-current-stage/validate 四子命令+schema校验+返修轮次计数，把手填 YAML 变工具调用，PyYAML 缺失降级内置解析 |
| idea-critique | `scripts/calibration.py` | idea 审查 calibration 模式：用已知结局样本估计 FNR/FPR，校准严格度 |
| idea-critique | `scripts/novelty_audit.py` | 新颖性检索证否四阶段留痕(抽论断→检索证据→撞车对比→判定)+一致性勾稽：抓"声称新但证据有 same 撞车"等自相矛盾，喂回否决项 |
| idea-critique | `scripts/score_aggregate.py` | idea 八维评分加权聚合、否决项处理与 verdict 映射 |
| idea-critique | `scripts/sycophancy_guard.py` | 反谄媚协议的可计算检查，约束 idea 评审不要迎合式放行 |
| idea-generation | `scripts/card_gate.py` | 立项卡交接门禁：校验 (m04复核) 字段非空、最近邻≥3带留痕、新颖性归档三档、撞车自评选档，残卡拒绝交 m04 |
| idea-generation | `scripts/candidate_dedup.py` | 候选 idea 去重/伪多样性检测：文本相似度(零依赖)或 SPECTER2 余弦(可选)，批内 mean+1σ 自动标疑似变体对，把含糊阈值算法化 |
| idea-generation | `scripts/rank_ideas.py` | 候选 idea 排序(m03 triage)：影响×工作量性价比确定性排序+先做/缓做/砍建议，收敛三套评分为唯一裁定 |
| ip-application | `scripts/copyright_source_prep.py` | 软件著作权源代码材料整理：过滤/抽样/编号，避免提交敏感或无关代码 |
| ip-application | `scripts/patent_search.py` | 在先技术检索辅助，支持引用图一跳扩展 `--snowball` |
| literature-search | `scripts/arxiv_search.py` | 预印本检索（arXiv Atom + 可选 bioRxiv/medRxiv），标注 preprint 与是否已转正式发表 |
| literature-search | `scripts/biomedical_search.py` | 生医文献检索（Europe PMC + PubMed E-utilities），支持 MeSH 检索式透传、跨源 DOI 去重 |
| literature-search | `scripts/cn_journal_probe.py` | 读取 ISSN 清单批量探测 OpenAlex source 体量，用于中文期刊/来源可见性初筛 |
| literature-search | `scripts/cross_domain_search.py` | 跨领域正交双轴检索（应用轴×方法轴分别检索分别排序），方法轴强时效抓 SOTA，输出迁移提示喂 idea-generation，治窄领域近三年文稀但创新靠跨领域嫁接前沿方法 |
| literature-search | `scripts/pipeline.py` | 端到端编排：串检索→相关度过滤→滚雪球→引用核验→(PRISMA 勾稽)→出 literature_review 骨架，复用 5 脚本不重复实现 |
| literature-search | `scripts/prisma_flow.py` | 系统综述 PRISMA 2020 流程留痕：核对筛选计数勾稽并产结构化流程数据 |
| literature-search | `scripts/search_normalize.py` | 多源文献检索与规范化，首轮即带后向引用边(OpenAlex / Crossref)；`--from-date`+`--known-dois` 做定期追踪增量重跑与新增去重 |
| literature-search | `scripts/snowball.py` | 按一篇文献的前向被引与后向参考做“引用滚雪球”，扩展相关文献 |
| literature-search | `scripts/tracker.py` | 文献定期追踪 SQLite 持久化：检索结果 upsert 去重、记 first/last_seen 与 new/seen/read 状态、被引快照随轮次更新、增量列新增、多格式导出 |
| literature-search | `scripts/verify_citations.py` | DOI 引用核验与幻觉引用标记，辅助文献真实性检查 |
| paper-drafting | `scripts/draft_lint.py` | 论文草稿诚信门机检：claim 无源、结果/引用 GAP、夸大词与占位符风险 |
| paper-polishing | `scripts/mechanical_check.py` | 离线学术文稿机械检查：弱词、夸大、被动堆叠、占位符、句式坏味道 |
| paper-polishing | `scripts/polish.py` | LanguageTool 云端/本地降级的语法风格检查，输出结构化发现与 HTTP 元数据 |
| paper-polishing | `scripts/style_fingerprint.py` | 从用户过往文稿提取文风指纹，润色时校准作者声音而非通用模板 |
| project-structure | `scripts/scaffold.py` | 一条命令生成规范科研项目骨架，含 data/src/docs/experiments/figures/paper 等目录 |
| research-plan | `scripts/plan_lint.py` | 实验矩阵四要素齐全性检查：假设/变量/指标/停止条件，缺一即提示，离线只读可接 CI；另含语义弱校验(完成判定可量化/判定指标对齐/假设-消融覆盖度) |
| research-plan | `scripts/power_check.py` | 统计功效反推：输入效应量+重复数→实际 power+达标最小重复数，纠"≥5 种子"对中效应欠功效误区(d=0.5 需 64/组)，statsmodels 优先缺失降级正态近似 |
| system-design | `scripts/er_diagram.py` | 表结构定义(YAML/JSON) → Mermaid erDiagram 文本，支持 PK/FK/UK 与关系基数，纯离线 |
| research-ethics | `scripts/check_retractions.py` | 批量撤稿/更正检查，通过 Crossref 等公开元数据标记 retraction risk |
| research-ethics | `scripts/text_overlap.py` | 离线自查重，定位与给定语料最长逐字重合片段，辅助学术规范审查 |
| research-ethics | `scripts/stat_consistency.py` | 统计自洽快查：GRIM/granularity 检验（均值粒度不可能）+ p值-自由度一致性（t/df、F/df1/df2），纯 stdlib 抓 p-hacking/造假信号 |
| result-analysis | `scripts/analyze_results.py` | 一条命令分析结果表：指标汇总、分组比较、排序与异常模式初筛 |
| result-analysis | `scripts/explain_shap.py` | 生成 SHAP 可解释性三图（beeswarm / bar / waterfall），无 shap 库时降级 |
| result-analysis | `scripts/leakage_overfit_check.py` | train/val/test gap 与数据泄漏风险筛查，提示过拟合和异常高分模式 |
| result-analysis | `scripts/make_figs.py` | 结果分析阶段的 matplotlib 出图模板，快速生成论文级统计图初稿 |
| result-analysis | `scripts/significance_test.py` | 显著性检验工具：p 值、效应量、置信区间、BH-FDR 多重校正 |
| review-rebuttal | `scripts/fetch_openreview.py` | 抓取 OpenReview 公开评审语料，校准模拟审稿与 rebuttal 话术 |
| review-rebuttal | `scripts/rebuttal_budget.py` | 会议 rebuttal 字数/页数预算检查，纯 stdlib 离线，中英混排分别计词、超限返回码 1 |
| slides | `scripts/pacing.py` | 答辩/路演时长估算：读 PPTX notes 时长标记累加估总时长、对照限时给 OK/超时+分配失衡页，无标记按字数×语速兜底 |
| slides | `scripts/pptx_eval.py` | PPT 可量化质量评测：内容密度/设计一致/连贯性三维扣分制，对照 SKILL 硬尺度逐页给分+扣分理由，把视觉 QA 从肉眼查升级为可回归指标 |
| slides | `scripts/thumbnail.py` | 把 PPTX/PDF 渲染成缩略图网格，快速做整套 deck 视觉 QA |
| slides | `scripts/to_pdf.py` | PPTX 转 PDF，优先 LibreOffice `soffice` 无头转换，用于后续视觉审查 |
| tool-selection | `scripts/detect_stack.py` | 读取项目清单文件识别技术栈，给出工具/技能选型建议 |
| typesetting | `scripts/precheck_log.py` | 扫描 LaTeX `.log`，汇总编译错误、警告、undefined citation/reference 等问题 |
| typesetting | `scripts/submission_check.py` | 投稿前合规/匿名雷区扫描：双盲身份泄漏(\author/致谢/可识别链接)、PDF 元数据 /Author、页数上限、残留 TODO，拦 desk-reject |
| venue-matching | `scripts/venue_signal.py` | 投稿 venue 五信号对照：发文量趋势/自引率粗查/审稿周期/作者匹配度/APC 分区，OpenAlex + db01 卡，失败优雅降级 |

## 仓库级资产校验

| 位置 | 文件 | 作用 |
|------|------|------|
| `.github/scripts/check_skills.py` | 技能 frontmatter 校验 | 检查 28 个 Light 技能的 `name` / `description` 与手动/常驻数量 |
| `.github/scripts/check_databases.py` | 数据库 YAML/schema/link 校验 | 检查 db03–db08 schema、重复卡片、YAML 解析与 README 本地链接 |
| `.github/scripts/check_skill_assets.py` | 脚本资产清单校验 | 检查 50 个技能脚本均登记到本文件、可编译、带真实 `__main__` 且覆盖显式 `--selftest` |
| `.github/scripts/check_entry_docs.py` | 入口文档一致性校验 | 检查 README/ROUTER/MODE_REGISTRY/ROUTER_EXAMPLES 的技能数量、mode 数量、路由样例与范围边界 |
| `.github/scripts/check_installation_assets.py` | 安装与客户端集成校验 | 检查 install.sh/install.ps1、Codex 路由片段、插件 JSON、安装文档与 CI 触发路径不漂移 |
| `.github/scripts/check_skill_links.py` | 技能内部链接校验 | 检查 28 个技能的 SKILL.md、references.md、references/*.md、templates/*.md、examples/*.md 中指向 references/templates/examples/assets/scripts 的本地链接；验证 SKILL.md 反引号资产路径与可选 linked_files |
| `.github/scripts/run_skill_selftests.py` | 技能脚本自测执行器 | 按 stdlib/science/documents 分层发现脚本并实际运行 `python <script> --selftest`，失败或超时即 CI 失败 |

## 可套用模板与数据文件

> 本表对 `skills/*/templates/*` 全量 1:1 登记，由 `.github/scripts/check_skill_assets.py` 防漂移（缺登记/多登记/路径失效均报错）。表末若干非 templates/ 行（脚本配套 / assets / 数据库文件）为高亮指引，不进 templates 校验。

| 位置 | 文件 | 作用 |
|------|------|------|
| data-engineering | `templates/annotation_guide.md` | 标注规范骨架：标签定义/边界判定/IAA 复核流程 |
| file-reading | `templates/understanding-note.md` | 五面理解结构化模板（元信息/结构逻辑/关键内容/格式要求/视觉风格/可复用）+文件→下游技能动作映射，读完产出标准笔记 |
| idea-generation | `templates/idea_card.md` | idea 卡：问题/创新点/可行性/风险/对照工作 |
| idea-critique | `templates/verdict_template.md` | idea 严审裁决书：创新度/可行性/风险逐维评级 |
| idea-critique | `templates/Revision_Roadmap.md` | 严审后修订路线图：按问题优先级排改进项 |
| research-plan | `templates/research-plan.md` | 研究方案填空骨架，每节带成功标准/验证方式 |
| research-plan | `templates/experiment_matrix.md` | 实验矩阵：实验ID × 假设 × 数据集 × baseline × 指标 × 种子，含派生数据规格 |
| research-plan | `templates/reproducibility-checklist.md` | 可复现性勾选清单（环境/目录/配置/版本/流水线） |
| research-plan | `templates/reproduction-log.md` | 复现已有论文的逐次日志表：改了什么/得到的数/与目标差/下一步假设 + 失败三分归因 |
| paper-drafting | `templates/claim_passport.md` | claim 台账：每个论断挂类型/来源指针/核查状态(已验证/待核/GAP)/HTTP码，诚信门抽样全查的 load-bearing 工件 |
| paper-drafting | `templates/01_imrad.md` | IMRaD 实证论文章节骨架 |
| paper-drafting | `templates/02_review_survey.md` | 综述/survey 论文章节骨架 |
| paper-drafting | `templates/03_theory.md` | 理论/方法型论文章节骨架 |
| paper-drafting | `templates/04_case_study.md` | 案例研究论文章节骨架 |
| paper-drafting | `templates/05_policy_brief.md` | 政策简报/对策建议骨架 |
| paper-drafting | `templates/06_conference.md` | 会议短文（含 rebuttal 预算意识）骨架 |
| figure-planning | `templates/figure_plan_card.md` | 图表规划卡：图号/类型/数据/目标章节/栏宽 |
| figure-planning | `templates/table_plan_card.md` | 表格专用规划卡：行列结构/表头分组/对齐/有效位数/最优标注/booktabs三线表/跨页横排 |
| citation 上游 | — | （引用样式无模板文件，见脚本表 verify_refs.py） |
| venue-matching | `templates/venue_compare_table.md` | 投稿候选刊对比表：冲稳保分档与匹配信号 |
| review-rebuttal | `templates/response_matrix.md` | 回应矩阵全量台账：每条意见→分类/concession分/回应/改动位置/re-review判定/承诺状态，逐条闭环 |
| review-rebuttal | `templates/response_letter_template.md` | 审稿意见逐条回复信骨架 |
| review-rebuttal | `templates/rereview_checklist.md` | 复审自查清单：逐条意见闭环核对 |
| ip-application | `templates/disclosure_template.md` | 专利交底书骨架：技术问题/方案/有益效果 |
| ip-application | `templates/claims_template.md` | 权利要求书骨架：独权/从权层级 |
| ip-application | `templates/specification_template.md` | 专利说明书骨架：背景/内容/实施例/附图说明 |
| ip-application | `templates/copyright_checklist.md` | 软著申报材料勾选清单 |
| competition | `templates/application_draft.md` | 申报书可填模板：核心页八段 + 十二段骨架（大创/挑战杯大挑/科研训练），对齐 db08 case_skeletons §4 |
| competition | `templates/business_plan.md` | 商业计划书可填模板：Lean Canvas 九格 + 十一段骨架（创新大赛/小挑），TAM/SAM/SOM 喂 market_charts |
| competition | `templates/defense_qa.md` | 答辩 QA 预演模板：六类高频追问 + 软肋诚实预案 + 备份附录清单 + 时间分配自检 |
| competition | `templates/abstract.md` | 项目摘要模板：数模摘要"模型名+关键结论数字"占位 + 申报/路演摘要，承接核心页 |
| typesetting | `templates/ieee_bare_conf.tex` | IEEE 会议双栏 LaTeX 骨架（Tectonic 实编译验证） |
| typesetting | `templates/acm_sigconf.tex` | ACM sigconf LaTeX 骨架 |
| typesetting | `templates/springer_llncs.tex` | Springer LLNCS LaTeX 骨架 |
| typesetting | `templates/elsevier_elsarticle.tex` | Elsevier elsarticle LaTeX 骨架 |
| typesetting | `templates/ctex_chinese.tex` | 中文 XeLaTeX(ctex) 骨架，自动装中文字体 |
| memory-pm | `templates/handoff_card.md` | 跨会话衔接卡：状态/已产出/下一步/恢复探针 |
| memory-pm | `templates/handoff_prompt.md` | 新对话启动提示词骨架，与衔接卡配套 |
| system-design | `templates/schema.sql` | 关系库建表 DDL 骨架 |
| system-design | `templates/rls_policy.sql` | 行级安全(RLS)策略骨架 |
| system-design | `templates/openapi.yaml` | OpenAPI 接口契约骨架 |
| system-design | `templates/ci.yml` | GitHub Actions 轻量 CI 骨架（lint + test + 迁移校验） |
| project-structure | `templates/README.template.md` | 项目 README 骨架 |
| project-structure | `templates/PROJECT_PLAN.template.md` | 项目计划骨架 |
| project-structure | `templates/PROJECT_STRUCTURE.md` | 标准可复现目录结构说明 |
| project-structure | `templates/CHANGELOG.template.md` | 变更日志骨架（Keep a Changelog 风格） |
| project-structure | `templates/pre-commit-config.template.yaml` | pre-commit 质量门配置，scaffold 自动生成 |
| project-structure | `templates/editorconfig.template` | 跨编辑器风格统一 .editorconfig |
| project-structure | `templates/python-research.gitignore` | 科研 Python 项目 .gitignore（显式不忽略 .light/） |
| competition | `scripts/market_charts.py` 配套 | 市场图所需 JSON 字段与 db08 预算共用同一套 TAM/SAM/SOM |
| consistency | `assets/design_language_extract.template.md` | 从现有图/PPT/前端反推设计语言的抽取模板 |
| db05 | `design_tokens.template.json` | DTCG 格式视觉 token，论文图/PPT/前端/海报共用的取值锚点 |
| db09 | `lessons.md` | 跨项目方法论经验库，新项目立项时检索复用 |

## 技能间衔接约定

- 正文引用占位统一用 `\cite{authorYearWord}` / `author+year+标题首词` 公式，从草稿(drafting)到引用(citation)到排版(typesetting)同源。
- 图表交付带 manifest：图号 F#/T# + `source_card` + 矢量/位图路径 + caption + 章节 + 目标期刊/栏宽 + 导出/字号 checks，供论文初稿与排版直接引用。
- 实验阶段所需的派生评测集（加噪/缺失/跨域）回 data-engineering 构建。
- 各产出技能交付前过 self-review 自检闸门。
