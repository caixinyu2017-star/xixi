# light-ip-application — 深度分析与同类对标

> 源：[`skills/light-ip-application/SKILL.md`](../../../skills/light-ip-application/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：面向中国软著与专利申请的"草稿+检索"辅助技能:出技术交底书/权利要求/说明书草案、整理软著源码材料、做非专利文献(NPL)在先技术检索,并反复声明须代理人审核。

## 核心运行逻辑
技能分两条主线:软著走"形式登记"思路(命名→功能说明→操作手册→源码前30+后30页整理→材料清单→流程),专利走"实质审查"思路(可专利性初判→查新检索→技术交底→权利要求两部分撰写法→充分公开的说明书→附图)。设计上把"可核查硬信息"(API端点/字段码/限流/CPCC规则/撰写规范)全部沉到 references.md 作真相源,SKILL.md 只给选用指引和流程,避免正文复写易过期数字。两个脚本各自带 --selftest 离线自测,强调 curl 实测过端点状态。全程以 CONVENTIONS 式"诚实声明"贯穿:不内置伪造 key、不臆造返回、所有 FTO/新颖性法律结论一律外推给代理师,材料不得虚构(联动 a10)。

## 关键步骤
- 1. 软著: 软件命名(全称+简称+版本)→功能说明→操作说明书(配截图)→copyright_source_prep.py 整理源码(50行/页、≤60页全交否则前30+后30、页眉、脱敏)→套 copyright_checklist.md 核对材料→在线登记系统填报→受理审查(约30工作日)→下证
- 2. 专利: 可专利性初判(发明/实用新型/外观)→patent_search.py 查新(OpenAlex NPL + 专利库请求模板)→disclosure_template.md 技术交底→claims_template.md 权利要求(方法+装置+介质组合)→specification_template.md 说明书(技术领域→背景→发明内容→附图说明→实施例)→附图交 m11 绘制→标注需代理人审核
- 3. 检索: 按数据范围选系统(CNIPA权威中国/Google Patents全球/PATENTSCOPE跨语言/EPO OPS机读/The Lens专利↔论文/USPTO ODP/OpenAlex NPL),硬端点参数查 references.md,带 key 自行发起
- 4. 交付前过 a08 自检闸门,材料入 db09,权属/检索风险上报 a10

## 自带资产
- scripts/patent_search.py — 在先技术检索:实发 OpenAlex /works 做 NPL 检索+一跳引用图扩展(snowball 后向/前向),并为 The Lens/EPO OPS/USPTO ODP 构造带鉴权的请求体(不发起),按被引数排序去重
- scripts/copyright_source_prep.py — 软著源码材料整理:遍历源码目录、正则脱敏(邮箱/手机/密钥行)、按50行/页分页、实现≤60页全交否则前30+后30页选取、加全称+版本页眉、尾页沿用真实总页号
- references.md — 9 节逐工具研究笔记(Google Patents/PATENTSCOPE/EPO OPS/CNIPA/The Lens/USPTO/OpenAlex/CPCC软著/权利要求规范/说明书规范),含真实端点、字段码、限流机制、2026-06 curl 实测状态与已知坑
- templates/disclosure_template.md — 技术交底书模板,含可专利性初判、查新证据留档(含 snowball checkbox)、必要技术特征清单、实施例
- templates/claims_template.md — 权利要求书草案,方法+装置+介质+电子设备组合布局,带从属权引用规则与提交前自检清单
- templates/specification_template.md — 说明书草案,按 CNIPA 审查指南顺序,含伪代码块占位与四项写作自检
- templates/copyright_checklist.md — 软著材料清单核对表(关键信息/提交材料/文档要点/截图建议/流程周期)

## 优点
- 真相源分层做得扎实:易过期的端点/限流/字段码集中在 references.md,标注 curl 实测日期(2026-06)与 HTTP 返回码(401/301/000),并把 OpenAlex 接入口径单点委托给 m01,避免全仓库数字漂移
- 诚实边界感强且一致:脚本不内置伪造 key、不臆造返回,反复声明 FTO/新颖性/无效结论须代理师定,材料不得虚构(联动 a10),符合科研/法律辅助工具应有的谨慎
- 两个脚本都可离线 --selftest,自测覆盖了真实边界条件(per_page=201→400 上限钳制、>60页前30+后30选取、尾页真实页号、merge_dedup 的 seed 优先级、脱敏命中)
- 专利撰写知识准确且体系化:两部分撰写法、从属权引用方向(不引更大编号)、单一性、充分公开、中国不允许超范围修改/事后补实施例——这些是真考点,模板自检清单可直接当 checklist 用
- 软著源码整理把 CPCC 的具体形式规则(50行/页、≤60全交否则前30+后30、页眉、脱敏)代码化,尾页沿用真实总页号这个细节正确,体现对登记实务的理解
- 检索覆盖面广且分场景给选用指引(权威中国走 CNIPA、跨语言走 PATENTSCOPE、专利↔论文走 The Lens),引用图 snowball 一跳扩展有助于补全在先技术链路并留档

## 缺点 / 可被质疑处
- 唯一可程序化的实数据源存在功能风险:脚本自己声明 OpenAlex 2026 起需免费 key,但 patent_search.py 只透传 mailto、不透传 api_key(明列为'已知缺口待 R5 补')。一旦匿名灰度关闭,该技能唯一能真正跑通的检索就会 401/限流失败,而其余专利库全是'构造请求'不发起
- 对主力用户(中国个人/中小企业申请人)的实际查新能力薄弱:最权威的 CNIPA 无公开 API、纯手工;EPO/Lens/USPTO 全需自带凭证且实测 401。绝大多数无 key 用户实际只能拿到 OpenAlex 的论文型 NPL,拿不到任何专利在先技术——与'查新检索'的承诺有落差
- claims_template.md 独权 1 骨架在法理上有瑕疵:写成'一种…方法,其特征在于,包括以下步骤 S1/S2/S3',把全部必要特征(含共有特征)都塞进'其特征在于'之后,既非纯两部分法也非纯单部分法,是个错误混合体;模板括注虽提了两种写法但给出的实际骨架会误导用户,代理人会直接打回
- SKILL 承诺生成'操作说明书/功能说明书',但 templates 里只有 copyright_checklist 核对表,没有这两份文档的实际模板;软著'文档'部分(用户手册/设计说明书)同样要前30+后30页处理,但 copyright_source_prep.py 只处理源码、不支持文档分页,承诺与资产之间有缺口
- 外观设计与实用新型支持几乎为零:SKILL/交底书只给一个 checkbox,但外观需要六面视图+简要说明、实用新型必须有附图且仅限产品形状构造——这些差异化材料要求完全没有模板或脚本支撑
- copyright_source_prep.py 脱敏是行级正则,自己声明'不保证完备':抓不到多行字符串里的密钥、base64/PEM 私钥、IP、中文姓名、版权头作者名,易给用户'已脱敏'的错觉;且 desensitize 作用于所有代码行而非仅注释(与 SKILL'去除注释中信息'表述不符),可能误改合法的 token= 配置常量
- 页数统计口径粗糙:脚本把自插入的 '//// FILE:' 标记行和空行都计入 50行/页,会虚增页数、与 CPCC 对实际提交 PDF 的页数认定不一致,可能导致前30+后30选取偏移
- snowball 前向引文只取一页(per_page=per_seed)、无 cursor 深翻,高被引种子的 cited_by 会静默截断到 200;后向是分批的、前向不是,行为不对称且未提示截断

## 可优化点（供后续逐技能优化）
- 给 patent_search.py 补 --api-key 参数并透传 OpenAlex ?api_key=,从环境变量(OPENALEX_API_KEY)读取,无 key 时打印明确告警'匿名请求不保证可用'——这是当前最高优先级的功能修复(脚本自己标的 R5 缺口)
- 为无凭证的中国申请人补一条可落地的查新路径:在 references/SKILL 里给出 CNIPA pss-system 与 Google Patents 网页高级检索的 URL 参数构造模板(country=CN、CPC、before:priority 等),让脚本能生成'人工点开即用'的检索链接清单,弥补无 API 的空白
- 修正 claims_template.md 独权 1 骨架:拆成两个正确范式——(A)单部分法'一种…方法,包括:S1…S3'(不带其特征在于);(B)两部分法'一种…方法,(共有特征),其特征在于:(区别特征)';去掉现在的错误混合写法
- 补 templates/manual_template.md(操作说明书/功能说明书文档模板:用途+功能模块+运行环境+技术特点+安装配置+逐功能操作步骤+截图占位),并让 copyright_source_prep.py 增加 --mode doc 支持对文档同样做前30+后30分页
- 增加外观设计与实用新型的专用模板/checklist(外观:六面视图清单+简要说明+设计要点;实用新型:必须附图、仅产品形状构造的权利要求范式),补齐 SKILL 已声明的三种专利类型
- 强化脱敏:把 desensitize 限定到注释/字符串区域,补 PEM/SSH 私钥块、base64 长串、IPv4、常见证书头的检测,并在输出末尾打印'命中并替换 N 处,但正则不保证完备,请人工复核'的统计与免责;统计页数时排除 '//// FILE:' 标记行与纯空行或给出两种口径
- snowball 前向引文改用 cursor 深翻或显式提示'已截断至前 200 条';让后向/前向行为对称,并在交底书查新证据节自动写入检索日期与命中数
- 补充申请成本/周期信息:软著加急档位区间、专利(发明实审周期、实用新型/外观周期)、官费量级,放 references 供用户预期管理(标注以官方公告为准、未逐字核实)

## 与其他 Light 技能/知识库的衔接
["m01(light-literature-search): OpenAlex 接入口径(是否需 key/限流/计费)的全仓库唯一真相源,本技能不复写数字,patent_search.py 的 NPL 检索直接依赖其口径", "m11(light-figure-drawing): 专利附图走黑白矢量线条链路,图号编排/标记线不交叉/术语对应等规范见 m11 references「专利附图规范」节,附图交其绘制,不套论文数据图样式", "m05/a03/a04/m07: 专利的技术问题/有益效果与论文 Introduction/Results 高度同源,软著功能说明可复用论文(m07)方法与结果段,技术内容由这些技能供给", "a10: 材料真实性、不得虚构夸大、权属与检索风险的上报闸门", "a08(light-self-review): 交付前自检闸门;a07: 与论文/系统保持一致;db08/db09: 模板与审查重点库、材料归档库"]

---

## GitHub 同类前沿技能对标

Light 的 light-ip-application 在这批同类项目里属于少数"软著 + 专利双线 + 检索辅助 + 诚实声明"一体化的技能,且把可核查硬信息(API端点/字段码/限流/CPCC/撰写规范)沉到 references.md 做真相源、脚本带 --selftest 离线自测,这种"工程化抗过期 + 可复现"设计在同类里几乎没人做。GitHub 上同类生态明显分三派:一派是中文软著/专利交底书生成 skill(patent-disclosure-skill、repo2patent、cn-patent-drafter、paper2patent、SoftwareCopyright-Skill、miaozhu),与 Light 功能最贴近,但多为单线(要么只软著要么只专利)、且很少把"诚实声明/法律外推代理师"做成贯穿协议;一派是多 Agent 全自动撰写流水线(PatentWriterAgent、PatentDrafter),侧重端到端生成而非检索真相源管理;一派是纯检索/数据层(uspto-opendata-python、yorkeccak/patents、LLM4DPCG),专做专利数据库 API/语义检索/claim 微调,可作为 Light 检索脚本的上游数据源。Light 的独特优势是双线覆盖 + 工程化抗过期 + 强合规自律;短板是缺少 PNG 附图自动渲染、缺多源检索路由(Lens/Espacenet/FPO)、缺成品 .docx/PDF 一键导出与真实端到端 demo,这些在 repo2patent、patent-disclosure-skill、paper2patent 里更成熟。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill) | 中文专利技术交底书生成 Claude/Cursor agent skill:扫项目文档与代码→专利点挖掘合并→以 CNIPA 公布公告站为主做查新(异常降级 WebSearch)→脱敏撰写→mermaid 系统/流程图渲染 PNG→输出 .docx,带无写自检与修订对话日志。 | 2600 | unknown(页面仅显示 9 commits,无明确日期) | 强:同类里最热门,附图自动渲染 PNG + .docx 成品 + 时间戳交付命名 + 降级检索链,工程成熟度高于 Light。弱:只做专利交底书一条线,不覆盖软著与权利要求/说明书两部分撰写法;不像 Light 把硬信息沉 references.md 抗过期,也没有 --selftest 离线自测与软著线。 |
| [rohitg00/awesome-claude-code-toolkit (patent-analyst)](https://github.com/rohitg00/awesome-claude-code-toolkit/blob/main/agents/research-analysis/patent-analyst.md) | 超大型 Claude Code 工具集(135 agents/35 skills/42 commands)中的 patent-analyst 子 agent,定位专利检索、在先技术、IP 全景分析。 | 2000(母仓库) | Mar 2026(母仓库 badge) | 强:生态规模与曝光极大,patent-analyst 偏检索分析方向。弱:patent-analyst 只是一个单文件 prompt agent,无双线流程、无软著、无脚本/自测、无 references 真相源,深度与可复现性远不如 Light 专项技能。 |
| [ninehills/PatentWriterAgent](https://github.com/ninehills/PatentWriterAgent) | 基于 Claude Code 的多 Agent 专利提案撰写 demo:输入解析→专利检索(SerpAPI/Exa)→大纲→权利要求→说明书→并行生成图与摘要→Markdown 合并成完整草稿。 | 550 | unknown(仅 2 commits,无 release 日期) | 强:端到端多 Agent 全自动流水线,一条命令出完整草稿,自动化程度高。弱:是 demo 性质(仅 2 commits),只做专利不做软著,依赖商业检索 key,缺合规/诚实声明协议与离线自测;Light 更强调可核查、抗过期与法律外推。 |
| [7toCR/paper2patent](https://github.com/7toCR/paper2patent) | 论文转专利中文智能模板库 + agent skill:把论文贡献改写为中国专利五要件(摘要/摘要附图/权利要求/说明书/附图),含 Flash/Pro 两套 prompt、清单与黑白线图绘制规范,带 figure/docx/pdf 导出脚本。 | 234 | 2026年4月(模板版本注明) | 强:论文→专利场景专精,附图规范 + docx/pdf 导出脚本齐全,强调忠于原文不添加歪曲。弱:输入限定论文、不做软著、不做独立在先技术检索;Light 覆盖面更广(软著+专利+NPL 检索)且有硬信息真相源与脚本自测。 |
| [ip-tools/uspto-opendata-python](https://github.com/ip-tools/uspto-opendata-python) | 访问 USPTO Open Data API(PEDS/PBD)的 Python 客户端库,用于程序化检索美国专利著录与文档数据。 | 108 | unknown(105 commits,无明确日期;README 提及兼容 Py2.7/3.6,较老) | 强:成熟的专利数据 API 客户端,可作为检索数据源底座。弱:纯数据访问库,无撰写/交底/软著能力,且偏美国 USPTO;Light 是面向中国软著/专利的撰写+检索辅助技能,定位互补而非竞争,可借其做检索上游。 |
| [duhbbx/miaozhu](https://github.com/duhbbx/miaozhu) | AI 自动生成软件著作权申请材料的 Web 工具(FastAPI+Vue):填基本信息→AI 产出操作手册、源码清单、数据库设计文档→导出 Word/PDF,兼容任意 OpenAI 兼容 API。 | 97 | unknown(仅 3 commits,无 release) | 强:软著专精、有完整前后端 Web UI 与一键 Word/PDF 导出,产品化体验好。弱:只做软著不做专利,源码材料更偏 AI 生成而非只取真实源码,缺 Light 的反伪造/诚实声明与专利线;Light 在合规与双线上更全。 |
| [bb-boy/repo2patent](https://github.com/bb-boy/repo2patent) | GitHub 项目→专利交底书可审计流水线 agent skill:读仓库提取证据→生成检索词→多源专利检索(Google/Lens/Espacenet/CNIPA/FPO)→相关性重排→claims-first 新颖性对比矩阵→输出 .docx,严格模式禁伪造在先技术。 | 62 | unknown(25 commits,无明确日期) | 强:多源检索路由 + 相关性重排 + 新颖性对比矩阵 + 质量门/失败退出码,检索工程化与禁伪造理念与 Light 高度一致甚至更细。弱:只做专利交底不做软著、不做权利要求两部分撰写完整法;Light 双线 + references 真相源 + --selftest 是其没有的。 |
| [yorkeccak/patents](https://github.com/yorkeccak/patents) | 对话式专利检索助手 Next.js Web 应用,自然语言搜 USPTO+EPO,支持 prior art/FTO/竞争情报/引用分析,含附图查看与本地 LLM(Ollama)。 | 12 | unknown(57 commits,页脚 2026) | 强:自然语言检索体验好,覆盖 FTO/在先技术/引用分析,有 Web UI。弱:纯检索分析、不做撰写与软著、依赖 Valyu 商业 API;Light 是撰写+检索辅助技能而非检索 Web 应用,且明确把 FTO/新颖性法律结论外推代理师,合规更克制。 |
| [handsomeZR-netizen/cn-patent-drafter](https://github.com/handsomeZR-netizen/cn-patent-drafter) | 对齐 CNIPA 2025-2026 规范的中国发明专利撰写 Claude Code skill:加载合规清单→定位章节文件→grep 源码取技术事实→套 LaTeX 模板→自检约50项→编译出 PDF。 | 9 | unknown(仅 1 commit,版权 2026) | 强:CNIPA 2026 规范同步 + ~50 项合规自检 + 权利要求依赖管理 + 段落编号连续 + LaTeX/PDF 产出,撰写规范化程度高。弱:明确不做软著/实用新型/外观/OA/检索,单一发明专利撰写;Light 覆盖更广且自带检索与软著线、脚本自测。 |
| [scylj1/LLM4DPCG](https://github.com/scylj1/LLM4DPCG) | 科研代码库:微调 Llama-3 从专利说明书生成权利要求,含数据准备、(多任务)微调、推理与评测,支撑论文《Can LLMs Generate High-quality Patent Claims?》。 | 9 | unknown(仅 2 commits,无 release) | 强:聚焦说明书→权利要求生成的模型微调与评测,有学术基准支撑。弱:研究原型而非可用 agent skill,无软著/检索/交底/合规流程;与 Light 不在同一层,可作为权利要求自动生成的技术参考。 |
| [maojoey/SoftwareCopyright-Skill](https://github.com/maojoey/SoftwareCopyright-Skill) | Codex/Claude skill:读本地真实项目自动生成中国软著全套材料(申请表字段、操作手册、源码前30+后30页整理),只取真实源码禁 AI 编造,导出 docx/txt。 | 0(为 Fokkyp/SoftwareCopyright-Skill 的 fork) | unknown(4 commits,无 release) | 强:软著材料专精,只取真实源码、禁编造与 Light 反伪造理念一致,前30/后30页规则与材料清单处理到位。弱:只做软著不做专利与检索,无 references 真相源与离线自测;Light 双线 + 检索 + 工程化抗过期更完整。该项目名义为 fork,原作者 Fokkyp 仓库为源头。 |

### Light 该技能可借鉴的点
- 附图自动渲染:借鉴 patent-disclosure-skill / repo2patent / paper2patent,用 mermaid→PNG 把系统图、流程图、专利附图(黑白线图)程序化生成,补上 Light 当前缺的成品附图能力(且符合 Light 论文数据图必须程序化的边界)。
- 成品一键导出:学 miaozhu / cn-patent-drafter,给软著材料和专利文本加 .docx(宋体)与 LaTeX/PDF 一键导出,让草稿真正落到可提交格式。
- 多源检索路由 + 相关性重排:借鉴 repo2patent 的 Google/Lens/Espacenet/CNIPA/FPO 多源路由、相关性重排与 claims-first 新颖性对比矩阵,强化 Light 的 NPL/在先技术检索,并保持其禁伪造、可溯源硬约束。
- CNIPA 规范化自检清单:学 cn-patent-drafter 的 ~50 项合规清单 + 权利要求依赖检测 + 段落编号连续校验,把 Light 的 references.md 撰写规范升级成可机检的 checklist。
- 端到端 demo 与失败退出码:借鉴 repo2patent 的质量门/失败退出码与 PatentWriterAgent 的全流程串联,给 Light 配一个真实可跑的最小端到端 demo,降低用户上手门槛、佐证可复现性。
- 权利要求自动生成参考:关注 LLM4DPCG 的说明书→权利要求评测思路,为 Light 的权利要求两部分撰写法增加质量自评维度(不引入模型微调,但可借其评测指标做自检)。
