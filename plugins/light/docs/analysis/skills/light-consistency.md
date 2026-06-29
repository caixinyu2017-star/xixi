# light-consistency — 深度分析与同类对标

> 源：[`skills/light-consistency/SKILL.md`](../../../skills/light-consistency/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：常驻后台的"跨材料一致性维护"技能:以 db09 项目术语/指标/方法为单一事实源,用一个 Python 审计器对论文/PPT/软著等多份材料做术语替换、指标换名、指标数值冲突、覆盖缺口四类文本级检测并定位到行,视觉与逻辑线索维度则走人工对照。

## 核心运行逻辑
设计核心是"先定义后生产 + 单一事实源(SSOT)":所有材料从 db09 派生,禁止下游各写各的。事实源有两种同构形态——人读的 terminology.md(每个项目必有,只够做覆盖缺口检测)和机读增强的三份 YAML(glossary/method_lock/metric_registry,多了 forbidden/confusable/权威数值列,才能支撑替换与数值冲突检测)。consistency_audit.py 读取这套事实源,逐行扫描材料:用词边界/子串匹配命中 forbidden 写法报 SUBSTITUTION,命中 confusable 且同行有数字报 METRIC_NAME,把指标名片段挖空后按"就近左侧"把数字配给最近的指标名与方法名、与权威值比对报 METRIC_VALUE,某术语只在部分材料出现报 COVERAGE_GAP。报告统一"现状→问题→建议"三段式、定位到 材料:行号、末尾做条数自检,ERROR 返回退出码 1 可接 CI。视觉一致性诚实声明为人工/半人工流程(截图取色有偏差),靠 design_language_extract 模板的⚠签字栏把关。

## 关键步骤
- 1. 常驻后台:每生成/修改一份材料即比对 db09 SSOT,发现偏差纠正或提示
- 2. 审计四步法 inventory→tag→gap→fix:盘点关键主张→打标(一致/冲突/缺失)→量化覆盖率→给修正后文本
- 3. 脚本加载 db09(自适应:目录有三份 yaml 走 schema 模式,否则找 terminology.md 走 Markdown 模式)
- 4. 对一组材料跑四类检测,位置感知配对数字避免 F1/mAP 串位,去重+按 ERROR/WARN 排序
- 5. 渲染定位报告+条数自检,可选导出 JSON;视觉维度对照 palette.json 或 db05 design_tokens 人工逐项核
- 6. 变更广播:定义一改即对 passport.yaml(或 version_history.md)列出的全部已产出材料回扫

## 自带资产
- scripts/consistency_audit.py:四类检测审计器,含 db09 双形态加载、位置感知数值配对、内置合成自测、JSON 导出、CI 退出码
- assets/db09_glossary.yaml:受控术语 schema 模板,字段含 canonical/aliases/forbidden/case_lock/zh/en,带 DCA-Net 等示例
- assets/db09_metric_registry.yaml:指标登记表模板,含 confusable/unit/decimals/higher_is_better/records 权威数值表,4 个指标示例
- assets/db09_method_lock.yaml:方法名锁定清单,带 role(main/module/baseline)/abbr/full/first_use_rule,4 条示例
- assets/design_language_extract.template.md:视觉设计语言抽取模板,采样清单+原子属性抽取表+⚠人工签字核对栏,明确声明非自动可信
- examples/worked_example.md:论文 vs PPT 指标名/数值冲突的端到端实例(复现命令→定位表→统一→修正后文本→回归)
- examples/materials_paper.txt + materials_ppt.txt:配套可运行材料,实测 8 条发现全部命中
- references.md:13 个参考工具的逐条核查笔记(distill/polish/audit/critique/content-strategy/Mermaid/Style Dictionary/Prettier/EditorConfig/DTCG 等),诚实标注【未能核实】项

## 优点
- SSOT 设计扎实且诚实分层:明确区分人读 terminology.md 与机读 YAML,并直说 Markdown 形态只支撑覆盖缺口检测,不夸大
- 数值配对工程上有真功夫:把指标名片段挖空再取数字(避免 mAP@0.5 的 0.5 被误读)、按'就近且优先左侧'把数字归给指标名和方法名,处理了一行并列多指标多方法的串位问题
- 可验证、可复现、可入 CI:内置无参合成自测(断言四类全触发)、material:行号定位、报告末尾条数自检、ERROR→退出码 1,实测 examples 命中 8 条与文档表格一致
- 通篇诚实声明局限:视觉维度明说是人工/半人工、截图取色有偏差、⚠项须签字、脚本不核视觉 token,不把不可靠能力包装成自动
- 缺失文件容错:db09 三件套缺任一份返回空表而非崩溃,db09 来源自适应识别目录/md
- schema 用稳定 id 解耦措辞与标识,为'变更广播回扫'提供了可追溯锚点

## 缺点 / 可被质疑处
- 最大缺口:description 与 SKILL 反复承诺的'创新点 3 条标准措辞跨论文/PPT/软著/竞赛一字对齐',脚本里完全没有对应检测器,也无 contributions schema——这是头号宣称能力却零实现,只能靠人工
- METRIC_VALUE 的 30% 容差是致命设计:abs(num-auth)/auth>0.30 即当无关数字跳过,于是 87.6 被误抄成 60.0 这类粗错、以及 0.876(分数) vs 87.6(百分比) 的单位不一致,反而被静默丢弃——恰恰漏掉最严重的数值不一致,与'数值冲突'这个卖点矛盾
- 数值检测召回严重依赖'方法名+指标名+数值同处一物理行':真实论文/PPT 的表格是逐行罗列(方法名在表头、指标值在数据行),跨行就配不上,实战中大量真实数值冲突检测不到
- 默认轻量路径几乎是空跑:SKILL 说三份 YAML'需严格校验时再生成',而每个项目必有的 terminology.md 只支撑 COVERAGE_GAP——意味着多数项目默认只有 1/4 检测能力可用,SUBSTITUTION/METRIC_VALUE 形同虚设
- COVERAGE_GAP 在真实场景必然刷屏:PPT 天然比论文短,paper 里每个未出现在 ppt 的术语都报 WARN,且无'哪些是贡献级必须全覆盖'的标记,example 只有 4 个术语显得干净,真实材料会被噪声淹没
- 代码与规则瑕疵:audit_metric_value 末尾有重复的死代码 return;method_lock 里 forbidden 的'本文方法(...)'被 startswith 硬编码跳过、规则实际失效;METRIC_NAME 把'准确率/Accuracy'当 F1 的 confusable,会把真实并列报告准确率与 F1 的论文误报为换名

## 可优化点（供后续逐技能优化）
- 新增创新点/贡献检测器:在 db09 存 3 条 canonical 贡献句,跨材料用 token 重叠或语义相似度做漂移检测,标出'同一贡献在 PPT/软著的提法偏离',直接补齐头号宣称缺口
- 重做数值比对:加单位归一化(% 与分数互转再比),把'偏差>30%'从静默跳过改为单列 GROSS_MISMATCH/疑似单位错 告警,而非丢弃;容差按 decimals 参数化并可配
- 数值配对引入跨行上下文:在段落/表格内维护'当前方法名上下文',数据行缺方法名时继承最近表头方法,显著提升真实表格的召回
- COVERAGE_GAP 分级降噪:schema 加 must_cover/贡献级 标记,只对必须全覆盖项报 WARN,普通术语降为 INFO 或默认抑制
- 给轻量路径补能力:提供 terminology.md→YAML 脚手架生成器,自动从标准叫法派生常见大小写/连字符变体填入 forbidden,让默认路径不止覆盖缺口检测
- 清理实现债:删除重复 return;把'本文方法'占位改为 schema 显式 placeholder:true 字段而非字符串前缀 hack;METRIC_NAME 区分'已登记的不同真实指标'与'真同义误用'以压低误报
- 落地视觉自动核:为 palette.json/design_tokens 写一个取值同源比对器(四方色值是否引用同一锚点),把视觉维度从纯人工部分自动化

## 与其他 Light 技能/知识库的衔接
上游事实源依赖 db09:terminology.md/palette.json/version_history.md 由 light-memory-pm(a02)维护,本技能只读;机读 YAML 扩写后存回 databases/db09-projects/projects/<项目>/。变更广播的'已产出材料'权威清单来自 orchestrator 的 .light/passport.yaml 各阶段 artifacts,无 passport 的轻项目退回 db09 version_history.md。视觉链路接 db05 design_tokens.template.json(DTCG SSOT)、db06 PPT 母版、db07 论文图,四方同取一份色值。服务对象为 m07/m08/m09/m11/m15/m16/m17/a05。方法论上借鉴 content-strategy(先定义后生产)、audit(inventory→tag→gap→fix)、critique(分维度+证据三段式)、full-output-enforcement(逐条列全+条数自检)、distill/polish(被标记为最易制造不一致的上游改写动作,需把受控词表当禁改清单传入并改完回扫)、extract-design-system(视觉抽取)。

---

## GitHub 同类前沿技能对标

GitHub 上的同类工具几乎全是"无状态 prose/术语 linter"(Vale、textlint、proselint、alex、LanguageTool、retext),它们的事实源是规则文件或词表,逐文件检查"写法对不对",但没有"单一事实源派生多份材料"的概念,更不做指标数值冲突与跨材料覆盖缺口检测。light-consistency 最独特的地方有两点:一是把 db09 的 terminology/glossary/method_lock/metric_registry 当作 SSOT,材料从它派生而非各写各的;二是 METRIC_VALUE 检测(把权威指标值与论文/PPT/软著正文里的数字逐行比对找冲突)和 COVERAGE_GAP(某术语只在部分材料出现)这两类是科研写作特有、通用 linter 基本不覆盖的维度。最接近的对标是 jeremylongshore 的 content-consistency-validator(同为 agent skill、同样跨网站/仓库/本地多源、同样输出带行号的分级报告),但它靠 LLM+grep/diff 临时比对、无机读事实源、不做数值权威值校验,可复现性和 CI 退出码不如 Light 的 Python 审计器。Light 的弱点是只服务中文科研材料场景、生态封闭、无成熟规则市场,而 Vale/textlint 有庞大的可复用规则包和 CI Action 生态。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [jeremylongshore/claude-code-plugins-plus-skills (content-consistency-validator)](https://github.com/jeremylongshore/claude-code-plugins-plus-skills/blob/main/plugins/productivity/000-jeremy-content-consistency-validator/skills/000-jeremy-content-consistency-validator/SKILL.md) | Claude Code agent skill,跨网站/GitHub 仓库/本地 docs 多源校验消息一致性(版本号、功能声明、产品名、术语、联系方式),输出只读差异报告,按 Critical/Warning/Info 分级并给文件路径+行号,设有 website>GitHub>local 信任优先级。 | 2366 (整个 plugins 仓库) | 2026-06-13 | 功能定位最接近 Light:同为 agent skill、跨多份材料、带行号分级报告、有信任源优先级。强点:开箱即用、覆盖 URL/版本/联系方式等通用元素、MIT 协议生态活跃。弱点:靠 LLM 临时 grep/diff 比对而非机读 SSOT,无 glossary/forbidden/confusable 结构化词表,不做指标权威数值冲突校验,无 CI 退出码,可复现性弱;且面向产品文档而非中文科研材料。 |
| [errata-ai/vale](https://github.com/errata-ai/vale) | markup-aware 的 prose linter,用 YAML 规则定义 substitution/existence/occurrence 等检查,支持术语强制替换、禁用词、风格规则,有大量可复用 style 包(Microsoft/Google/写作风格)和 GitHub Action。 | 5452 | 2026-06-12 | 强点:工业级成熟、规则生态庞大、CI 集成完善、速度快、substitution 规则与 Light 的 SUBSTITUTION 检测思路高度一致。弱点:无 SSOT 派生模型(规则即事实,但不跨材料对照),不理解'指标数值'语义、不做 METRIC_VALUE 冲突与 COVERAGE_GAP,不针对中文科研论文/PPT/软著三材料联动场景。 |
| [textlint/textlint](https://github.com/textlint/textlint) | 可插拔的自然语言 linter,通过 rule/preset 插件做术语统一、禁用表达、风格检查,支持 Markdown/纯文本/AST,有日英等多语言术语规则生态。 | 3135 | 2026-06-11 | 强点:插件机制灵活、可写自定义术语规则、社区规则多、可接 CI。弱点:仍是单文件无状态检查,无跨材料覆盖缺口概念,不做指标权威值比对,需自己写插件才能逼近 Light 的语义检测,中文科研词表生态薄弱。 |
| [amperser/proselint](https://github.com/amperser/proselint) | Python 写的英文文风 linter,内置数十类规则(冗余、误用、不一致拼写等),命令行输出问题位置,可作为写作质量基线工具。 | 4539 | 2026-06-07 | 强点:Python 实现(与 Light 审计器同栈)、规则成体系、可脚本化。弱点:纯英文、规则写死无项目级 SSOT、不可定制术语表为主、完全不涉及指标数值/跨材料一致性,定位是通用文风而非科研事实一致。 |
| [get-alex/alex](https://github.com/get-alex/alex) | 检测文本中不敏感/不包容措辞的 linter(基于 retext),面向用词一致性与替换建议。 | 5094 | 2024-11-27 | 强点:零配置、用词替换提示清晰、star 高。弱点:仅做敏感词维度,既无项目术语 SSOT 也无数值/覆盖检测,与 Light 的科研一致性目标差距大,近一年多未更新。 |
| [languagetool-org/languagetool](https://github.com/languagetool-org/languagetool) | 25+ 语言的语法与风格检查器,支持自定义规则与术语词表,可本地部署做大规模文本质量检查。 | 14575 | 2026-06-12 | 强点:多语言(含中文部分支持)、规模大、可自建术语规则、API 化。弱点:面向语法/风格而非'跨材料事实源一致',无 SSOT 派生、无指标数值冲突、无覆盖缺口,重量级且需服务部署,不贴科研三材料联动。 |
| [retextjs/retext](https://github.com/retextjs/retext) | 基于 unified 的自然语言处理框架,通过插件做拼写、可读性、用词一致等检查,是 alex 等工具的底座。 | 2433 | 2025-02-04 | 强点:可组合插件、AST 级精确定位、生态成熟。弱点:需自行拼装插件,默认不含术语 SSOT/指标校验,定位是 NLP 基础设施而非成品科研一致性方案。 |
| [crate-ci/typos](https://github.com/crate-ci/typos) | 面向源码与文档的低误报拼写纠正器,支持自定义词表/扩展词典,极快、易接 CI 与 pre-commit。 | 3992 | 2026-06-04 | 强点:速度极快、CI/pre-commit 集成好、自定义词表机制可借鉴。弱点:只做拼写,不理解术语规范/指标/跨材料,维度远窄于 Light。 |
| [redocly/redocly-cli](https://github.com/redocly/redocly-cli) | API 文档/OpenAPI 的 lint 与治理工具,可对规范做规则化校验、强制命名与一致性,支持自定义规则集。 | 1466 | 2026-06-12 | 强点:把'规范即事实源'做成强校验、规则化治理思路与 Light 的 SSOT 接近、CI 友好。弱点:仅限 API/OpenAPI 领域,不处理自然语言科研材料、无指标数值与覆盖缺口检测。 |
| [FSoft-AI4Code/DocChecker](https://github.com/FSoft-AI4Code/DocChecker) | 研究型工具,用预训练语言模型检测代码与注释/文档之间的语义不一致,并可生成修正。 | 16 | 2024-01-23 | 强点:专攻'内容与事实源语义不一致'这一核心命题、方向与 Light 的一致性检测理念最契合、是学术化方法。弱点:仅限 code-comment 场景、模型化不可解释/难定位到行、无术语词表与指标校验、star 极低且久未更新,不能直接用于科研材料。 |

### Light 该技能可借鉴的点
- 借鉴 Vale 的 styles 规则包机制:把 db09 的 glossary/method_lock 做成可分发、可版本化的规则包,让多个科研项目复用同一套术语规则,而不必每个项目从零写 YAML。
- 学 Vale/textlint/typos 提供官方 GitHub Action 与 pre-commit hook 模板,让 consistency_audit.py 的 ERROR 退出码真正接进 CI/提交钩子,而非仅手动跑。
- 参考 textlint/retext 的可插拔规则架构,把四类检测器(SUBSTITUTION/METRIC_NAME/METRIC_VALUE/COVERAGE_GAP)解耦成可单独开关、可扩展的插件,方便后续加'图表标题一致''参考文献编号一致'等新维度。
- 借鉴 DocChecker 的语义级思路:在纯文本子串匹配之外,可选叠加一个轻量语义层(embedding/LLM)来捕捉'同义不同形'的术语漂移,弥补 forbidden/confusable 词表必须穷举的局限,但保留可解释的行号定位。
- 学 jeremylongshore 把信任源优先级和报告格式标准化的做法,在视觉一致性这种人工维度上,用结构化模板+签字栏强约束流程,减少'诚实声明为人工'带来的执行随意性。
- 参考 LanguageTool 的多语言规则组织,为中英文混排科研材料补充中英对照术语校验(如指标英文缩写与中文名必须配对出现),覆盖国内投稿常见的中英不一致问题。
