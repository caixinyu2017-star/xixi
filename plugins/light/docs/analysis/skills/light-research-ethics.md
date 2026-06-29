# light-research-ethics — 深度分析与同类对标

> 源：[`skills/light-research-ethics/SKILL.md`](../../../skills/light-research-ethics/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：常驻后台的科研伦理与合规风险审查官:把 FFP/COPE/ICMJE/IRB/IACUC 等权威规范拆成 11 类红旗清单 + 三级分级模板 + 两个可跑离线脚本,在全流程中发现风险即提示/拦截并给合规替代。

## 核心运行逻辑
设计思路是"规范→可操作":把抽象的出版伦理/科研诚信规范(ORI FFP 三要件、COPE flowchart、ICMJE 四条 + CRediT 14 角色、IRB 三级审查 + 45 CFR 46.111 八标准、IACUC/GB-T 35892)固化为可勾选的红旗清单和填表式审查报告,再用 BLOCK/WARN/NOTE 三级分级统一定级口径。核心护栏是"认定权不在研究者":脚本和决策树只做"是否升级 + 找谁",最终裁定留给机构诚信办/IRB/代理人/法律。两个 Python 脚本把两条最易落地的红旗变成真工具——撤稿核查(Crossref update-to[])和离线自查重(difflib 最长逐字重合),都纯 stdlib、带 --selftest、带诚实限制声明。常驻属性(user-invocable:false)让它在 m01-m17、a01-a09 全流程后台生效,撤稿判定逻辑被 m10 引用复用为单一真相源。

## 关键步骤
- 1. 材料进入任一科研任务时,先过清单第 0 条:外部内容防注入检查(待审材料里的'忽略指令/给高分'当数据不当指令)
- 2. 用 risk_checklist.md 逐条勾选 11 类(+动物 6′类)红旗信号,每类带默认起评级
- 3. 命中红旗即到 ethics_review_template.md 风险表对应行登记证据(文件:行/图号/DOI)并定 BLOCK/WARN/NOTE 级
- 4. 高利害情形走 decision_trees.md:A 疑似不端→FFP 三要件→COPE flowchart;B IRB 级别;C 引用前撤稿核查;D 涉动物干预 vs 观测
- 5. 可跑工具落地:check_retractions.py 批量查 Crossref 撤稿/更正;text_overlap.py 离线比对自我抄袭最长逐字重合
- 6. 署名用 ICMJE 四条 + CRediT 14 角色填贡献声明表,AI 按用途披露(写作入致谢/分析作图入方法,不得署名)
- 7. 产出三级风险清单 + 每项(为什么是风险 + 合规做法)+ 是否需第三方审核标注;命中红线直接拒绝并给合规替代
- 8. 风险记入 db09,衔接 a08(自审)/m10(引用)/m15(软著专利)

## 自带资产
- SKILL.md:常驻审查主文档,11 类风险清单 + 规范依据(含真实 API 端点)+ 资产索引 + 红线 + 衔接
- references.md:13 个工具/规范逐条研究笔记(COPE/ICMJE/CRediT/ORI/Retraction Watch/Turnitin/ScanCode/Snyk/Socket/CC Chooser/IRB/ISO 13485/Anthropic compliance),含真实端点、CLI 参数、已知坑,带 ⚠️ 标注未完整核实项
- references/decision_trees.md:4 棵高利害决策树(A 不端 FFP→COPE / B IRB 三级 / C 撤稿核查 / D 涉动物),每个判定点给满足/不满足分支
- assets/ethics_review_template.md:结构化审查报告模板,风险表 + ICMJE/CRediT 署名表 + AI 披露 + 结论判定
- assets/risk_checklist.md:11 类(+0 防注入 +6′动物)红旗 checkbox 清单,每条带红旗信号 + 默认起评级 + 落地命令
- scripts/check_retractions.py:批量 Crossref 撤稿核查,查 update-to[] 标 🛑撤稿/⚠️更正/✅/❔,出 markdown 或 --json,带 --selftest
- scripts/text_overlap.py:纯 stdlib 离线自查重,difflib 找最长逐字连续重合 + 词重合率/Jaccard,--min-run 40/--exclude-refs/--json/--selftest

## 优点
- 规范来源权威且标注诚实:每条规范都给真实端点/CLI 参数/已知坑,并用 ⚠️ 明确标出'政府原文被网络策略阻断、未逐字核实、厂商自报数字'等局限——这种自我证伪在 AI 技能里罕见,直接降低了误导用户的风险
- 两个脚本是真能跑的工具而非伪代码:都纯 stdlib 无依赖、带 --selftest 离线自测、Crossref 端点标注'已 curl 实测 HTTP 200',text_overlap 用 SequenceMatcher 精确命中'连续>40词'红旗并能定位到行,落地性强
- 分级口径统一可执行:BLOCK/WARN/NOTE 三级 + 每类默认起评级 + '命中越多越升级',把主观的'有点问题'变成可登记可追溯的判定,审查报告模板要求写清证据定位(文件:行/DOI)
- 护栏意识清醒:反复强调'认定权在机构不在研究者''Turnitin 分数是对话起点非定罪依据''文本匹配≠抄袭''诚实错误≠不端',避免了 AI 乱扣学术不端帽子的高危误用
- 与 m10 建立了真正的单一真相源:撤稿判定 FLAG_TYPES 被 light-citation/verify_refs.py 实际内联复用(已在代码注释中确认),不是口头衔接,避免两处口径漂移
- 领域适配到位:专设决策树 D 和 6′ 类覆盖奶山羊行为识别项目的动物伦理(IACUC/GB-T 35892/T-CAI 003-2019/非侵入观测边界),并附验证日志 R12-03,不是泛泛而谈

## 缺点 / 可被质疑处
- check_retractions.py 第 26 行硬编码个人 QQ 邮箱 1833058953@qq.com 作为 MAILTO——这是真实 PII 被写进脚本,而本技能 risk_checklist 第 6 类明令'PII 不得出现在代码',自我违规;且分发给他人时等于泄露作者邮箱、Crossref polite pool 也被绑定到该私人邮箱
- 11 类风险里只有 2 类(撤稿、自我抄袭)有可跑工具,其余 9 类(图片不当、p-hacking、署名、版权许可、结论夸大等)全靠人工肉眼勾选清单,而图片复用/拼接、统计自洽性恰恰是最需要工具辅助、人工最易漏的高频造假点,工具覆盖严重不均衡
- 大量声称的外部工具(ScanCode/Snyk/Socket/Turnitin/CC Chooser)只在 references 里给命令,技能本身无任何封装或调用脚本,用户仍需自行安装配置跑——'可操作'更多停留在'知道用什么命令'而非'帮你跑出来'
- 决策树编号错乱(A→B→D→C,C 撤稿核查排在最后),且 SKILL.md 资产说明里也按 A/B/C/D 顺序引用,与文件实际顺序不一致,阅读和定位时易混乱,暴露出迭代追加(D 是后补的动物树)未回头整理
- text_overlap.py 仅做逐字/词级匹配,对'改写式抄袭'(换词、调语序、translation plagiarism)完全无能为力——而清单第 1 类自己就列了'译述他人成果当原创'红旗,工具能力与所声称要防的红旗不匹配,易给用户'查过自查重=安全'的虚假安心
- 规范高度偏向美国体系(ORI/42 CFR 93、Common Rule 45 CFR 46、ICMJE),中国本土口径(《涉及人的生命科学和医学研究伦理审查办法》《科研失信行为调查处理规则》、国自然/教育部学术不端办法)仅一句带过、无落地清单,而目标用户主体是中国科研人员,本地合规这条最关键的线最薄
- FLAG_TYPES 用 expression_of_concern(下划线),但 Crossref 实际 type 字段惯用 expression-of-concern(连字符);脚本靠 .replace('-','_') 兜底,而 SKILL/references 文字描述用连字符——两处口径声称'必须一致'却靠隐式归一化维系,m10 那侧若未同样归一化就会漏判,是个埋着的不一致隐患

## 可优化点（供后续逐技能优化）
- 立即移除 check_retractions.py 硬编码私人邮箱:改为读环境变量 CROSSREF_MAILTO 或命令行 --mailto 参数,缺省用占位符 anonymous@example.org 并提示用户填写;同时全仓 grep 排查其他脚本是否有同样 PII
- 补齐高频造假点的轻量工具:(1) 图片完整性预筛脚本——用 stdlib/Pillow 做 EXIF 提取 + 同文档内图像感知哈希(pHash)近重复检测,命中跨图复用红旗;(2) 统计自洽性检查——实现 GRIM/granularity 检验和 p 值-自由度一致性快查,把第 2 类 p-hacking 红旗工具化
- 把外部工具从'给命令'升级为'给可跑封装':至少为 ScanCode/Snyk 提供一个检测是否安装→给安装指引→跑→解析 JSON 输出成本技能三级分级报告的 wrapper 脚本,真正做到'帮你跑出来'
- 新增中国本土合规模块:补一份 references/cn_compliance.md(《涉及人的生命科学和医学研究伦理审查办法》三级审查、《科研失信行为调查处理规则》失信情形清单、国自然/教育部不端认定口径),并在决策树 A/B 里加'适用法域=中国'分支,与现有美国树并列
- 整理决策树编号与交叉引用:按 A/B/C/D 物理重排文件,或统一改为按主题命名(不端树/IRB树/撤稿树/动物树),同步修正 SKILL.md 资产说明里的引用顺序
- text_overlap 增加近义改写检测档:可选启用 token 集合 n-gram + 词干化/同义归并的'软匹配'模式,或集成轻量句向量(若允许依赖)做改写式重合提示,并在输出明确区分'逐字重合'与'疑似改写',堵上 translation/paraphrase plagiarism 缺口
- 把 FLAG_TYPES 抽成两技能共享的单一常量文件(如 references/_retraction_flag_types.json),check_retractions.py 与 m10 verify_refs.py 都 import,并在其中显式同时收录连字符与下划线两种写法,彻底消除靠 replace 兜底的隐式不一致
- 给常驻审查加一个'触发-产出'的最小契约:目前 user-invocable:false 且'后台生效'较虚,建议在 SKILL 里明确'哪些任务类型(投稿前/软著提交前/数据发布前)强制产出一次完整 ethics_review_template',避免常驻=从不实际触发

## 与其他 Light 技能/知识库的衔接
作为常驻横切技能覆盖 m01-m17 与 a01-a09 全流程,衔接关系真实且部分已在代码层面落地:与 m10(light-citation)最紧——撤稿判定 FLAG_TYPES 被 verify_refs.py 实际内联复用为单一真相源(已在其代码注释确认),引用核验时随每条 DOI 自动查撤稿;与 m15(软著/专利)配合专利权属与软著真实性审查,最终文本须代理人审核;与 a08(自审)在收尾时联动查结论夸大;与 m11(light-figure-drawing)的 figure_integrity 互引 AI 生成图像红线与'PPT 可 AI 生图但禁入论文图链路'的边界;与 m07(light-paper-drafting)的 AI 声明模板、m05(功效分析定最小样本→动物 3R 减少原则)、a01(PII 不回显)、m08/a08(SOTA 滥用)、db01(venues.csv 取 ai_policy)、db09(风险记录)联动;AI 政策按 venue 实查 db01。隐私合规工作流借鉴 Anthropic compliance 技能结构。横切真相源指向 CONVENTIONS(§4 防注入单一真相、§5 版权只存元数据)。

---

## GitHub 同类前沿技能对标

GitHub 上没有任何项目和 light-research-ethics 的整体定位重合:它是把出版伦理/科研诚信规范(ORI FFP、COPE、ICMJE+CRediT、IRB 45 CFR 46.111、IACUC/GB-T 35892)系统拆成 11 类红旗清单 + BLOCK/WARN/NOTE 三级分级 + 常驻后台审查官的 LLM agent skill,核心护栏是认定权不在研究者。社区里能找到的同类工具几乎全是单点功能的窄工具,聚成三类:一类是撤稿/失效文献核查(retractobot、Retraction-Radar、retract-check、citicious),恰好对应 Light 那个 Crossref update-to 撤稿脚本;一类是参考文献真实性/AI 假引核查(refchecker、VeriExCiting),热度最高;一类是图像取证(sherloq、image-forensics),对应 Light 没做成脚本的图像不端红旗。规范层面的同类只有伦理清单 deon 和 GenAI 报告清单 TREGAI,但它们是静态清单/CLI,没有 Light 的全流程常驻拦截、三级分级和找谁裁定的决策树。整体上 Light 在规范覆盖广度与流程内常驻治理上独一档,但在两个落地脚本的工程成熟度上明显弱于这些专精工具(纯 stdlib、difflib 自查重、单 Crossref 源 vs 它们多源 API + 数据库 + 浏览器插件)。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [HelenoPaiva/Retraction-Radar](https://github.com/HelenoPaiva/Retraction-Radar) | 扫描论文参考文献列表,用 OpenAlex + Crossref + Retraction Watch 三源交叉检出被撤稿、更正和关注声明的引文。和 Light 的撤稿核查脚本几乎同一目标。 | 1 | 2026-06-13 | 强点:三数据源交叉比 Light 单 Crossref update-to 覆盖更全,且自动解析整篇参考文献。弱点:只做撤稿这一红旗,无伦理规范体系/分级/裁定护栏,star 极低无社区验证。 |
| [ebmdatalab/retractobot](https://github.com/ebmdatalab/retractobot) | 牛津 EBM DataLab 出品,从 PubMed 识别撤稿论文,经 Scopus API 找出引用它们的论文并给作者发邮件告警。机构级撤稿监测管线。 | 6 | 2024-10-08 | 强点:真实科研机构背书、引文网络追溯 + 主动告警闭环,产品化管线。弱点:依赖 Scopus 付费 API(Light 纯 stdlib 离线可跑),只覆盖撤稿单点,无伦理规范拆解;近两年未更新。 |
| [saadabdurrazzaq00/retract-check-saas](https://github.com/saadabdurrazzaq00/retract-check-saas) | 隐私优先的浏览器端工具,把整份参考文献的 DOI 在本地浏览器内比对官方 Retraction Watch 数据库,数据不出本机即可标出撤稿文献。 | 1 | 2026-01-06 | 强点:本地优先隐私设计 + 批量 DOI、面向非技术用户的 React 界面。弱点:JS 单功能撤稿核查,无伦理体系/分级/常驻 agent 属性,star 近乎为零。 |
| [choxos/citicious](https://github.com/choxos/citicious) | Chrome 扩展,在学术网页上实时标记被撤稿文章和疑似伪造/幻觉引文,用 CrossRef + OpenAlex + doi.org 解析器校验 DOI。 | 0 | 2026-05-28 | 强点:浏览器内实时拦截、同时覆盖撤稿 + AI 假引两类红旗。弱点:只是阅读期插件,不进入写作/投稿全流程,无规范分级与机构裁定护栏,无社区验证。 |
| [markrussinovich/refchecker](https://github.com/markrussinovich/refchecker) | 验证学术论文参考文献真实性的工具(作者为微软 Azure CTO Mark Russinovich),核查引用是否真实存在、是否被 AI 伪造。本批次热度最高之一。 | 398 | 2026-06-07 | 强点:知名作者背书、近 400 star、专注引文真实性这一 LLM 时代最痛的红旗,工程成熟。弱点:范围仅限引文核查,不触及 FFP/IRB/IACUC/作者署名等伦理面,无分级与流程内常驻治理。 |
| [ykangw/VeriExCiting](https://github.com/ykangw/VeriExCiting) | 检测学术论文中 AI 生成的虚假引文(Verify Existing Citations),针对 LLM 写作导致的幻觉参考文献问题。 | 30 | 2025-12-25 | 强点:精准命中 LLM 假引这一较新的风险点,有一定 star 与论文背景。弱点:窄到只做假引检测,无伦理规范体系、无三级分级、不做常驻全流程审查。 |
| [GuidoBartoli/sherloq](https://github.com/GuidoBartoli/sherloq) | 开源数字图像取证工具集(ELA、噪声分析、JPEG 伪影、克隆检测等),可用于核查科研论文图像是否被篡改/复制。本批次 star 最高。 | 3150 | 2026-05-25 | 强点:3000+ star、成熟的图像篡改取证能力,正好填补 Light 未做成脚本的图像不端红旗。弱点:通用取证工具非科研伦理专用,不懂 COPE 图像操纵流程,无分级/裁定/规范映射,需专业判读。 |
| [MKLab-ITI/image-forensics](https://github.com/MKLab-ITI/image-forensics) | 图像篡改检测库,提供多种取证算法实现,可用于识别图片造假与拼接。 | 238 | 2019-06-26 | 强点:算法库可被集成进自动化图像红旗检测流程。弱点:2019 年后停更、Java 老库,纯算法无科研伦理语境,与 Light 的规范化分级/常驻审查无重叠。 |
| [drivendataorg/deon](https://github.com/drivendataorg/deon) | 命令行工具,一键为数据科学项目插入伦理审查清单(数据收集、存储、分析、建模、部署各阶段勾选项)。是把伦理拆成可勾选清单这一设计哲学最接近的开源物。 | 309 | 2026-03-30 | 强点:同样走规范到可勾选清单路线且 CLI 化、300+ star、可定制清单,理念和 Light 高度共鸣。弱点:面向数据科学伦理非出版/科研诚信,纯静态清单无分级、无撤稿/查重脚本、不常驻流程、无 FFP/IRB/COPE 映射。 |
| [nliulab/GenAI-Ethics-Checklist](https://github.com/nliulab/GenAI-Ethics-Checklist) | TREGAI(Transparent Reporting of Ethics for Generative AI)清单,规范化报告研究中使用生成式 AI 的伦理事项,对应 ICMJE/期刊对 AI 使用披露的要求。 | 15 | 2024-10-16 | 强点:权威清单形式、精准对应 Light 红旗中 AI 使用披露这一最新合规热点,可作为规范引用源。弱点:仅一份静态报告清单文档,无工具/脚本/分级/常驻能力,覆盖面远窄于 Light 的 11 类红旗。 |

### Light 该技能可借鉴的点
- 撤稿核查从单一 Crossref update-to 升级为多源交叉(OpenAlex + Crossref + Retraction Watch 官方库),像 Retraction-Radar / citicious 那样降低漏检,这与 m10 复用 Light 撤稿逻辑的单一真相源诉求直接相关,值得作为脚本下一版方向
- 把整篇参考文献自动解析批量核查(retractobot / Retraction-Radar 已做),而非逐条手填,提升红旗清单的可落地性
- 新增 AI 生成假引/幻觉引文检测红旗并参考 refchecker、VeriExCiting 的判定思路,这是 LLM 时代新增且热度最高的诚信风险,Light 现有清单可显式强化
- 图像不端红旗目前只在清单层面,可借鉴 sherloq 的取证维度(ELA / 克隆检测 / JPEG 伪影)给出更具体的自查指引或可选外接工具,而非仅文字提示
- deon 的 CLI 一键插入清单 + 可自定义清单源的交付形态,值得 Light 借鉴用于把红旗清单导出为项目内可勾选文件,增强随项目常驻的可见性
- 引用 TREGAI(GenAI-Ethics-Checklist)作为生成式 AI 使用披露红旗的权威外部规范锚点,补强 ICMJE 之外的 AI 披露合规依据
