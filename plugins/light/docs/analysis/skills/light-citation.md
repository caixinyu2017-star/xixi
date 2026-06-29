# light-citation — 深度分析与同类对标

> 源：[`skills/light-citation/SKILL.md`](../../../skills/light-citation/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：科研论文引用的全链路管家:从引用规划、真实性/关联度/撤稿/被引关系核验,到 DOI 一键多格式生成与投稿前体检,三个零依赖 Python 脚本把"杜绝虚假引用"落成可运行机读流程。

## 核心运行逻辑
核心设计是"分层核验 + 诚实留白":把引用错误拆成三个独立层次——文献是否真实存在(verify_refs.py 查 Crossref+OpenAlex 双源)、A 引 B 的被引关系是否成立(verify_citation_edge.py 查 OpenCitations+S2)、被引文献是否真支撑正文那句话(locator_audit.md 人工三态审计)——并反复强调"key/DOI 对得上 ≠ 论点被支撑"。第二条主线是"开放性 vs 权威性"严格分离:脚本只从 OpenAlex 同源带出 OA 字段当线索,绝不据 oa_status=closed 扣分,权威性/掠夺性判定明确交人工。格式生成走 DOI 内容协商最短路径(Accept 头直取 BibTeX/CSL JSON/RIS),CSL JSON 作多格式中枢,并针对中文国标 GB/T 7714 做了 langid 注入、文献类型标识码、作者截断等专门处理。所有脚本免外部依赖(纯 urllib)、自带离线 __main__ 自测、端点都标了 2026-06-06 实测 HTTP 码。撤稿检测与中文核验则刻意复用/对接 a10、m07 的同源口径,避免多技能各说一套。

## 关键步骤
- 1. 1. 引用规划:列出每个 claim/方法/数据集/对比工作,匹配经典+最新+SOTA+背景四类来源,检查覆盖盲区
- 2. 2. 搜索/抽取候选 DOI(Crossref query.bibliographic 或 OpenAlex title.search,或从 .bib/.tex 直接抽 DOI)
- 3. 3. 去重:合并同一工作的多版本/多 DOI,预印本优先换正式版
- 4. 4. 跑 verify_refs.py 出机读报告:真实性(查不到=high severity)、撤稿(update-to[]+标题前缀)、中外占比、自引率、缺近2年标志、预印本数、OA 开放性字段
- 5. 5. 对正文声称的第三方引用关系逐条跑 verify_citation_edge.py 取三态结论(confirmed/not_in_open_index/unknown)
- 6. 6. 核心论点引用过 locator_audit.md 人工三态审计(supports/partial/unsupported),核对原文是否真支撑
- 7. 7. 跑 doi_to_any.py 生成 BibTeX/CSL JSON/GB-T 7714,按 authorYearWord 公式 pin citekey,中文条目注入 langid
- 8. 8. 抽正文 \cite{} 键与 .bib 键对账(补缺/删冗)
- 9. 9. 逐项过 citation_checklist.md 投稿前体检,产出补引/删引/换源/改格式修改清单 + 标准工件 citation_audit.md / refs.bib

## 自带资产
- scripts/verify_refs.py — 批量 DOI 经 Crossref+OpenAlex 双源核验,产机读 JSON;含真实性/标题年份一致性/撤稿/自引/中外占比/被引时效/OA开放性字段,带离线 mock 自测
- scripts/verify_citation_edge.py — 实证'A引用了B',OpenCitations 双向 + Semantic Scholar 兜底,严格三态输出(绝不输出裸 edge_exists:false),带自测
- scripts/doi_to_any.py — DOI 内容协商一键转 BibTeX/CSL JSON/GB-T7714,按 CJK 自动注入 langid,本地实现 GB/T 7714 顺序编码制排版,带自测
- references/locator_audit.md — 引用关联度审计方法论:三态判定表 + 审计动作清单 + 高危优先级,治'引了真文献但不支撑该句'
- assets/citation_checklist.md — 投稿前五大类(真实性/关联度/覆盖/数量/格式)勾选清单 + 中外占比建议表 + 按文献年龄的被引阈值分档表
- references.md — 14 个工具的真实端点/参数/已知坑研究笔记(Crossref/DOI协商/OpenAlex/S2/Unpaywall/OpenCitations/Zotero/Better BibTeX/JabRef/CSL JSON/GB-T7714/中文兜底/BibTeX-Biber/EndNote),核心 API 标实测 HTTP 码

## 优点
- 分层核验模型立得住:把'真实存在/被引关系/论点支撑'三层严格拆开,并反复强调'DOI 对得上≠论点被支撑',精准命中审稿人最在意、自动工具最查不出的关联度问题,这是绝大多数引用工具的盲区
- 诚实工程化做得扎实:三个脚本都坚持'只报 API 真实返回',查不到标 high severity、被引关系用三态而非布尔、明确区分'未覆盖≠未引用',不替任一方圆场;脚本零外部依赖(纯 urllib)+离线自测,可移植性和可信度都高
- '开放性 vs 权威性'分离是专业判断:明确 oa_status=closed 不等于低质(顶刊多闭源),脚本只给线索不下权威性结论,避免了常见的'闭源即低质'误判
- 中文国标支持有真功夫:不只提 GB/T 7714,还落到 langid 注入、文献类型标识码 [J]/[C]/[D]、作者>3 截断'等'交样式而非源数据处理、无 DOI 中文文献核验兜底,并给了三条实查留痕,对中文投稿场景远超通用工具
- 跨技能口径对齐意识强:撤稿检测显式复用 a10 check_retractions.py 的 FLAG_TYPES,中文核验与 m07 integrity_gate 第4节做双向声明、三字段口径一致,降低了多技能拼装时的逻辑分裂
- 工具研究笔记质量高:references.md 对每个 API 标了真实端点/参数/限速/已知坑(如 Unpaywall 占位邮箱 422、Crossref offset>10000 失效、OpenAlex 倒排摘要),是能直接照着写代码的真知识而非链接堆砌

## 缺点 / 可被质疑处
- 脏数据/边界鲁棒性不足:GB/T 7714 排版假定 CSL author 有规整 family/given,但中文 DOI 内容协商常返回 literal 或把整名塞进 family,_fmt_authors_gbt 的西文缩写逻辑(取首字母加点)会把中文名误处理;csljson_to_gbt7714 对缺 container/page/卷期的会议与电子资源 [EB/OL] 几乎没覆盖,而清单却要求查访问日期,生成与核对标准不对齐
- 撤稿检测召回率实际很低且文档自己承认:仅靠 Crossref update-to[] + 标题 RETRACTED 前缀,SKILL 明说'经典撤稿常不暴露 update-to',等于主路径漏报多;但 workflow 又把 retracted_count==0 当硬门槛,容易给用户'已查干净'的虚假安全感,真正兜底(Retraction Watch)却没脚本化
- 存在死引用与未验证留痕:references.md 第357行指向 _verification_log/r3_chinese_chain.md,该文件在技能内不存在;三条中文实查留痕直接硬编码在 references.md 里,既无脚本可复现也无法更新,时效性存疑
- verify_refs 的几个判定过于粗糙:is_cn 靠标题含汉字或作者串含'China'判断,会漏掉英文标题的中国团队、误判含 China 地名的外国文献;自引仅按姓氏子串匹配,'Li/Wang'这类高频姓会大面积误报;标题一致度用字符级 Jaccard,中英混排或短标题阈值 0.6 噪声大
- verify_citation_edge 的 S2 兜底脆弱:references 端点 limit=1000 但不翻页,引用数>1000 的综述会漏判 B;且无 key 时 S2 共享池高频 429,极易落到 unknown,文档虽诚实标注但实战可用性受限
- 邮箱硬编码与隐私:三个脚本把 light.research@gmail.com 写死进 UA/mailto,用户跑出去的请求都署这个名,既不符合 polite pool 本意(应是调用者邮箱),OpenAlex 2026 需 key 的政策脚本也完全没接入(只在文档里说'按需 key 实现'但代码没做)
- 规划与覆盖度核验仍高度依赖人工且无工具支撑:'经典/最新/SOTA 是否引全'这类最影响论文质量的判断,清单里基本是'人工'或泛泛的 OpenAlex 高被引扫描,没有可运行脚本把'实验表里比较过的方法 vs 已引文献'做差集,落地性弱于真实性核验那条线

## 可优化点（供后续逐技能优化）
- 给 doi_to_any 增加 CJK 作者特判:_has_cjk(name) 为真时整名作单元、不做西文缩写;补全 GB/T 7714 的 @online/[EB/OL] 访问日期、会议地点出版者、专利/标准字段,使生成口径与 citation_checklist E 节核对项一一对应;并对 literal/缺字段做显式占位而非静默丢字段
- 撤稿检测接真兜底:把 a10 check_retractions.py 作为可选第二跳(或直接调用其三态),并在 retracted_count 摘要里把'已用信号'与'未覆盖经典撤稿'分开报,避免 0 被误读为'保证干净';可考虑接 Retraction Watch / Crossref 的 retraction 索引
- 清掉死引用:补建 _verification_log/r3_chinese_chain.md 或删去 references.md 对它的指针;把三条硬编码中文实查留痕改为脚本可重跑的样例(给一个 cn_demo dois 列表 + 期望字段),让留痕可复现可更新
- 把 self-author/机构判断从子串升级:支持 ORCID 或'姓+名首字母'组合匹配降低高频姓误报;is_cn 改用 OpenAlex 的 authorships.institutions.country_code + language 字段,而非标题汉字/China 子串启发式
- 脚本接入 OpenAlex 免费 key 与可配置 mailto:把硬编码邮箱改为 --mailto 参数或环境变量,默认不署具体私人邮箱;按 m01'OpenAlex 接入真相源'实现 api_key 读取,兑现文档承诺;S2 references 加 token 翻页与 --s2-key 选项,避免大综述漏判和 429
- 补一个覆盖度差集脚本:输入实验对比表里的方法名/DOI 与当前 .bib,输出'比较过但未引'清单;再用 OpenAlex group_by 年份+cited_by_count 给经典/近2年候选,把现在纯人工的 C 节覆盖度自检部分自动化
- 补 citekey 对账脚本:SKILL workflow 第5步'抽 \cite{} ↔ .bib 键对账'目前无脚本,可加一个从 .tex/.md 抽 \cite 键、与 .bib 键求双向差集并按 authorYearWord 公式校验的小工具,与 m07/m08 占位公式同源

## 与其他 Light 技能/知识库的衔接
SKILL.md 显式声明与 m07(light-paper-drafting)/m08/m12(typesetting?) 协同:撤稿检测复用 a10(light-research-ethics)的 check_retractions.py FLAG_TYPES 同源口径(已确认该脚本存在);无 DOI 中文文献核验与 m07 integrity_gate.md 第4节做'拦截方 vs 执行方'双向声明、三字段口径一致(已确认 integrity_gate.md 存在);OpenAlex 接入(key/限流)统一指向 m01(light-literature-search)references 的'OpenAlex 接入真相源',缺关键文献回 m01 补检;格式随 m13(venue-matching)选定 venue 调整、引用样式查 db01 的 reference_style 字段;引用库登记 db09;虚假/掠夺性来源风险上报 a10;标准工件 citation_audit.md + refs.bib 交付 m12,命名遵 CONVENTIONS §6.1(CONVENTIONS.md 存在)。整体在 Light 体系里定位清晰、衔接点具体,是引用诚信链路的执行枢纽。

---

## GitHub 同类前沿技能对标

GitHub 上同类项目可分三类:一是引用真实性核验工具(refchecker、hallucinator、PHY041、AlterLab),普遍只解决'文献是否存在+元数据匹配'这一层,且多数依赖 LLM/PDF 抽取/多 API key,做得最重最热的是微软 CTO 的 refchecker(398 星);二是格式转换库(citation.js、Bibtex-to-GBT7714、doi2bibtex),专精 DOI/BibTeX/CSL 互转但完全不碰核验;三是检索/撤稿单点工具(pasa、re-cite)。light-citation 的独到之处在于把'引用错误'显式拆成三个正交层次——文献是否真实(双源)、A 引 B 被引边是否成立(OpenCitations+S2)、被引是否真支撑正文那句话(人工三态审计)——这种'被引边独立核验+支撑性留白'的分层在同类里几乎没人做全;同时它坚持纯 urllib 零依赖、自带离线自测、端点标实测 HTTP 码,并内建中文 GB/T 7714 细节(langid 注入、文献类型标识码、作者截断),在'轻量可机读+开放性与权威性严格分离+诚实留白'这条路线上独树一帜。代价是数据源广度、PDF 抽取、GUI/桌面交付和社区声量都不及 refchecker 这类重型项目。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [markrussinovich/refchecker (PyPI: academic-refchecker)](https://github.com/markrussinovich/refchecker) | 学术论文引用校验工具,从 PDF/.bib 抽取参考文献,跨 Crossref/OpenAlex/Semantic Scholar/arXiv 核验是否真实存在、元数据是否匹配,带 LLM 抽取、Web UI、CLI、Docker、桌面应用和幻觉检测。由 Mark Russinovich(微软 CTO)维护,生态最成熟。 | 398 | 2026-06-07 | 强:数据源覆盖更广(含 arXiv)、有 PDF 抽取+GUI+桌面端+Docker 多种交付、LLM 辅助抽取、社区声量大。弱:依赖重(LLM/GROBID/多 API key),非零依赖;偏向'文献是否存在/元数据匹配',缺 Light 的'A 引 B 被引边核验'独立层和'被引是否真支撑论点'人工三态审计;无中文 GB/T 7714 专门处理。 |
| [gianlucasb/hallucinator](https://github.com/gianlucasb/hallucinator) | 检测学术 PDF 论文里潜在幻觉/伪造参考文献的工具,面向 AI 生成内容的虚假引用排查。 | 224 | 2026-06-04 | 强:专注 PDF 输入的幻觉检测,star 高、迭代活跃,直接面向'AI 编造引用'痛点。弱:只解决'真实性'一层,没有被引关系核验、撤稿对接、DOI 多格式生成、投稿前体检的全链路;无中文国标支持;设计粒度不如 Light 的三层分离清晰。 |
| [PHY041/claude-skill-citation-checker](https://github.com/PHY041/claude-skill-citation-checker) | Claude Code 技能,核验 .bib 文件对 Crossref/Semantic Scholar/OpenAlex 三源,无需 API key,专门抓三类问题:完全编造、嵌合引用(真标题配错作者)、可疑 DOI/过泛标题。 | 21 | 2026-03-22 | 强:同为 Claude 技能、同样三源零 key,'嵌合引用'概念很精炼,定位最接近 Light 的核验脚本。弱:只做真实性+元数据这一层,无被引边/撤稿/支撑性审计/DOI 生成/投稿体检;无中文处理;只有 2 次提交,成熟度低。 |
| [haiyichen001/reference-workbench-skill](https://github.com/haiyichen001/reference-workbench-skill) | Agent Skill(兼容 Claude Code/Codex/Gemini CLI/Cursor 等 20+ 编辑器),核验学术引用并写文献综述+自动生成参考书目,检查论文是否存在、元数据准确性、被引论点是否真被支撑。 | 3 | 2026-05-14 | 强:跨 20+ 编辑器的 Agent Skills 标准兼容性好,且明确含'引用论点是否被支撑'这一层(与 Light 的 locator_audit 同思路),还带综述写作。弱:star 低、较新;核验链路不如 Light 在被引边、撤稿、DOI 多格式、投稿前体检上分层清晰;无中文国标。 |
| [AlterLab-IEU/AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) | 学术技能套件,含 alterlab-citation-verifier(确定性引用存在性闸门,跨 Crossref/OpenAlex/S2/arXiv 校验、解析 DOI/arXiv、匹配标题作者、标记撤稿)、Citation Graph(无 key 的 ResearchRabbit 类比,基于 OpenAlex 出共引图)、Citation Management、PyZotero。 | 27 | 2026-06-12 | 强:技能套件覆盖面广,引用核验+撤稿+引用图+Zotero 一条龙,撤稿对接 Retraction Watch,且确定性闸门思路与 Light 一致;迭代很活跃。弱:'存在性闸门'仍以真实性为主,缺 Light'被引边是否成立'与'是否支撑该句'的独立分层与三态留白哲学;无中文 GB/T 7714。 |
| [larsgw/citation.js (citation-js/citation-js)](https://github.com/citation-js/citation-js) | 格式转换核心库:BibTeX/Wikidata JSON/DOI/RIS 等互转,以 CSL-JSON 为中枢输出 APA/Vancouver/BibTeX 等多格式。 | 238 | 2026-06-06 | 强:格式转换生态极成熟,CSL-JSON 为中枢的设计与 Light DOI 生成思路一致,支持的格式和 CSL 样式远多于 Light。弱:纯格式转换库,完全不做真实性/被引/撤稿/支撑性核验;JS 生态、非 Python 零依赖脚本;中文国标需额外 CSL 样式而非内建处理。 |
| [54dbd/Bibtex-to-GBT7714-2015](https://github.com/54dbd/Bibtex-to-GBT7714-2015) | 把 BibTeX 文件转成中国国标 GB/T 7714-2015 格式的工具。 | 43 | 2026-01-27 | 强:专攻中文国标 GB/T 7714,在国标格式细节上更专、更纯粹。弱:单一格式转换工具,无核验/撤稿/被引/投稿体检;不处理 langid 注入、文献类型标识码、作者截断等 Light 已内建的国标细节是否全覆盖未知;非技能形态。 |
| [timothygebhard/doi2bibtex](https://github.com/timothygebhard/doi2bibtex) | 把 DOI 和 arXiv 标识解析成格式化 BibTeX 条目的命令行工具。 | 23 | 2024-08-20 | 强:DOI→BibTeX 这一窄场景做得干净,支持 arXiv id。弱:只覆盖 Light DOI 生成功能的一小段,无 CSL JSON/RIS 多格式中枢、无核验/撤稿/体检;两年未更新;无中文支持。 |
| [bytedance/pasa](https://github.com/bytedance/pasa) | 字节跳动的 LLM 论文搜索 agent,自主调用搜索、读论文、选相关参考文献,服务复杂学术检索。 | 1591 | 2025-05-27 | 强:论文检索/相关性发现能力强,star 高,可做引用规划阶段的'找文献'。弱:定位是检索 agent 而非引用核验,不做真实性/被引边/撤稿/格式/投稿体检;与 Light'杜绝虚假引用'的机读核验目标只在引用规划环节部分重叠。 |
| [recite/re-cite.org](https://github.com/recite/re-cite.org) | 高亮论文中引用了撤稿文章的 Web 应用代码。 | 11 | 2021-12-24 | 强:专注撤稿引用高亮,概念与 Light 撤稿检测同源。弱:只做撤稿一项,无其他核验层;2021 年后未更新基本停摆;Web 应用形态,不是可嵌入技能/脚本。 |

### Light 该技能可借鉴的点
- 借鉴 refchecker 的 PDF/正文自动抽取参考文献能力,补上 Light 目前依赖结构化输入的短板,让核验链路能直接吃论文原文
- 引入 PHY041 的'嵌合引用(Chimeric Citation,真标题配错作者)'这一命名清晰的错误类型,作为真实性核验里的显式检查项
- 参考 refchecker/citation.js 把更多 CSL 样式纳入,用现成 CSL 样式库扩充输出格式,而非只手写少数几种
- 对接 AlterLab 的 Citation Graph / ResearchRabbit 类比思路,在被引边核验之外提供共引/引用网络的可视化或线索,辅助引用规划
- 学习 refchecker 的多渠道交付(CLI/Web UI/Docker)经验,至少提供一个零配置的批量 CLI 入口降低使用门槛
- 借鉴 AlterLab'确定性闸门(deterministic gate)'的措辞与 CI 集成定位,把 Light 的核验脚本包装成投稿流水线里可阻断的质量门
