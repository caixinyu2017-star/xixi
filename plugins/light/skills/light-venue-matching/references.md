# 投稿定位与 venue 匹配 — 参考工具研究笔记

> 逐工具核查笔记，供 SKILL.md 调用。每个工具列【是什么】【可复用方法/端点/参数】【链接】【已知坑/局限】。
> 研究日期 2026-06；指标随年度更新，引用具体数值前务必 last_checked。

---

## OpenAlex Sources API

【是什么】免费开放的学术图谱，Sources 实体即"期刊/会议/repository/出版商系列"，CC0 授权，可全量下载或 REST 查询。是程序化拉取 venue 元数据（ISSN、OA、h-index、APC、学科）的首选。

【可复用方法/真实端点/参数】
- Base URL：`https://api.openalex.org/sources`
- 单条：`/sources/S{id}`、`/sources/issn:1234-5678`（支持按 ISSN 直查）。
- 过滤 `?filter=`（逗号分隔 AND）：`issn`、`is_oa`、`is_in_doaj`、`type`(journal/conference/repository)、`country_code`、`apc_usd`、`works_count`、`cited_by_count`、`summary_stats.h_index`、`summary_stats.i10_index`、`summary_stats.2yr_mean_citedness`(≈影响因子代理)、`topics.id`、`concepts.id`、`host_organization`。
- 搜索：`?search=` 按名称模糊匹配；排序 `?sort=cited_by_count:desc`。
- 分面统计：`?group_by=` 得到分桶计数（如按 country_code 统计某方向期刊分布）。
- 分页：游标 `?cursor=*`（首页），用返回的 `meta.next_cursor` 翻页；`per_page` 最大 200。深翻只能用 cursor，不能用 page。
- 认证/限流/计费：OpenAlex 2026 起**需免费 API key**；礼貌池仍可加 `?mailto=you@example.com` 更稳。key 申请、限流、计费、退避的唯一口径见 **m01（light-literature-search）references「OpenAlex 接入真相源」节**，本技能不复写数字。
- 典型组合：`?filter=topics.id:T10883,is_oa:true&sort=summary_stats.2yr_mean_citedness:desc&per_page=50&mailto=...` → 按方向取 OA 期刊并按引用强度排序。

【链接】https://api.openalex.org/sources ｜ 文档 https://docs.openalex.org/api-entities/sources （现重定向至 https://developers.openalex.org/）

【已知坑/局限】`2yr_mean_citedness` 只是影响因子的近似，不等于 JCR IF；会议常被合并/缺失；topics 体系 2024 改版，老的 concepts 字段逐步弃用；不含中文核心/CCF/分区等本土评价，需另接。

---

## OpenAlex Authors API（录用可能性 rubric 的"作者相对实力"信号源）

【是什么】OpenAlex 的 Authors 实体，REST，给每位作者 `works_count`、`cited_by_count`、`summary_stats.h_index`、`summary_stats.2yr_mean_citedness`、`summary_stats.i10_index`、ORCID 等。是 rubric 中"作者 h-index 相对该刊典型作者"这一可核查信号的数据来源（OpenAlex 2026 起需免费 key，接入口径见 m01 真相源节；加 `mailto` 进礼貌池）。

【可复用方法/真实端点/参数】
- 按名检索：`GET https://api.openalex.org/authors?search=<姓名>&mailto=<email>`（返回 `results[].summary_stats.h_index`）。
- 过滤+排序：`GET https://api.openalex.org/authors?filter=display_name.search:<name>&sort=cited_by_count:desc&per_page=1&mailto=<email>`。
- 单条：`/authors/A{id}` 或 `/authors/orcid:0000-0000-0000-0000`（ORCID 直查，排重名最稳）。
- venue 侧对照：作者 h-index 与该 venue 的 `summary_stats.h_index`（OpenAlex Sources `/sources/issn:<ISSN>`，或 db01 已存值）比较——作者接近/超过该刊量级=信号"高"。

【实测核查（2026-06，curl + mailto）】
- `GET /authors?search=Kaiming He&mailto=...` → HTTP 200，返回 `summary_stats.h_index`（示例命中 A5100700361，h_index=85，works_count=163）。
- `GET /authors?filter=display_name.search:hinton&sort=cited_by_count:desc&per_page=1&mailto=...` → HTTP 200。
- `GET /sources/issn:0162-8828&mailto=...`（IEEE TPAMI）→ 返回 `"h_index":549`，可作"该刊典型量级"对照。

【链接】https://api.openalex.org/authors ｜ 文档 https://docs.openalex.org/api-entities/authors

【已知坑/局限】**重名严重**：常见中文姓名拼音会聚多人或拆分一人，h-index 不能盲信——优先用 ORCID 或机构排歧，无法确认时按 CONVENTIONS 标"待核查"，不强行认定；OpenAlex 作者消歧本身有误差；h-index 受职业生涯长度影响，年轻作者偏低属正常，rubric 里只作"相对该刊"的一项信号、非唯一依据。

---

## Scimago Journal Rank (SJR) / SCImago Journal & Country Rank

【是什么】基于 Scopus 数据的免费期刊声望指标与排名门户。SJR 是核心指标，另给 H-index、Citations per Doc、按学科的四分位 Q1–Q4。门户数据可免费检索并按年度/学科导出 Excel。

【可复用方法/真实端点/参数】
- SJR 计算：类 PageRank 的特征向量声望算法——被引按"施引期刊的声望"加权（非所有引用等值），统计窗口为前 3 年发文的当年加权被引/文献数；迭代收敛后归一化为规模无关的 SJR 值。区别于"所有引用等权"的 JIF。
- 分区：在每个 Scopus 学科类目内按 SJR 排序，前 25% = Q1，依次 Q2/Q3/Q4。一刊跨多类目可有多个分区，取最高常被用来"包装"，评估时要看主类目。
- 数据获取：portal 的 journalrank.php 支持按 subject area / category / country / year 筛选并下载 CSV/Excel；无官方 REST API，但有第三方封装（如 R 包 `sjrdata` 把全量数据打包）。
- 取舍：SJR 用 Scopus（覆盖比 WoS 广，含更多会议与非英文刊），适合做免费、跨库的声望参考；与 Eigenfactor（用 WoS）思路相同但数据源不同。

【链接】门户 https://www.scimagojr.com/ ｜ 排名下载 https://www.scimagojr.com/journalrank.php ｜ 方法学 https://www.scimagojr.com/methodology.php ｜ R 封装 https://github.com/ikashnitsky/sjrdata

【已知坑/局限】分区年度更新、与中科院分区/JCR 分区口径完全不同，三者别混；SJR 高不代表 IF 高；门户网页禁爬（直接 fetch 易 403），优先下载官方 Excel 或用第三方数据包。

---

## Clarivate JCR (Journal Citation Reports) — JIF / 分区

【是什么】科睿唯安基于 Web of Science Core Collection 的年度期刊报告，产出 Journal Impact Factor(JIF)、JIF 四分位、JIF 百分位、JCI 等。是 SCI/SSCI "影响因子"与"几区(JCR分区)"的官方源。需订阅访问完整 JCR。

【可复用方法/真实端点/参数】
- JIF 计算：当年对前 2 年所发"可引用文献"(article+review)的被引总数 / 前 2 年可引用文献数。另有 5 年 JIF。
- 2023 起 JIF 只显示 1 位小数（制造更多并列，弱化排名微差，鼓励看多指标）。
- 2024 JCR 重大变化：把原先分版(SCIE/SSCI)分别排名的 9 个跨版类目合并为单一统一排名，且 ESCI 期刊正式纳入各类目 JIF 排名，覆盖全部 229 个科学+社科类目。
- JIF 分区：在类目内按 JIF 排序分 Q1–Q4（这是"JCR 分区/汤森路透分区"，与中科院分区不同）。
- JCI(Journal Citation Indicator)：领域归一化指标，可跨学科比较；2025 起 25 个艺术人文类目不设 JIF 排名，只用 JCI。

【链接】JCR 变化说明 https://clarivate.com/academia-government/blog/2024-journal-citation-reports-changes-in-journal-impact-factor-category-rankings-to-enhance-transparency-and-inclusivity/ ｜ 2024 发布 https://ir.clarivate.com/news-events/press-releases/news-details/2024/Clarivate-Reveals-Worlds-Leading-and-Trusted-Journals-with-the-2024-Journal-Citation-Reports/default.aspx

【已知坑/局限】完整 JCR 要订阅；"JCR 分区"≠"中科院分区"≠"SJR 分区"，写报告必须标明是哪套；IF 受综述/自引影响大，单看 IF 会误判。

---

## Web of Science Master Journal List (MJL)

【是什么】科睿唯安免费检索入口，查一本刊是否被 WoS 收录、收在哪个索引（SCIE/SSCI/AHCI/ESCI）。覆盖 21,000+ 期刊，每月数十万用户访问。是判定"是否 SCI/SSCI 收录"的权威核查点。

【可复用方法/真实端点/参数】
- 免费搜索，可按 collection、category、country、language、出版频率、open access、期刊指标过滤；可限定只看 Core Collection。
- 四大索引含义：SCIE=科学引文索引扩展，SSCI=社会科学引文索引，AHCI=艺术人文引文索引，ESCI=新兴来源引文索引（被收录但门槛/影响较低，是观察区）。
- 期刊 profile 页给：WoS 收录信息、最新 JIF、平均投稿到发表时长（若有）、OA 信息、同行评议信息。
- Manuscript Matcher：内置 AI + Core Collection 数据的稿件匹配工具，输入题目/摘要给候选刊。

【链接】https://mjl.clarivate.com/ ｜ 改版说明 https://clarivate.com/news/web-of-science-group-relaunches-master-journal-list-of-21k-journals/

【已知坑/局限】免费版只告诉"收没收录/收在哪个索引"，IF/分位等要 JCR 订阅；ESCI 收录 ≠ 有影响因子（部分作者误以为 ESCI=SCI）；收录状态会动态调整（被剔除/On Hold），投前要现查。

---

## Scopus Sources / CiteScore

【是什么】Elsevier Scopus 的期刊层级，核心指标 CiteScore。覆盖比 WoS 广（含更多会议、非英文、新刊）。CiteScore 值对所有人免费可查（不像 JIF 需订阅）。

【可复用方法/真实端点/参数】
- CiteScore 计算（2020 起新口径）：当年及前 3 年共 4 年窗口内被引总数 / 同 4 年发文数；分母计入 article、review、conference paper、book chapter、data paper（比 JIF 分母宽）。例：Nature 2021 = 338,611 引 / 4,823 文 = 70.2。
- CiteScore Tracker：每月更新的次年预测值，正式年值约每年 5 月底发布（比 JCR 的 IF 早约一个月）。
- 分位：在学科类目内给绝对排名+百分位，据此分 Q1–Q4。
- 数据：Scopus Source List(含 CiteScore、ASJC 学科码、是否 OA、是否被剔除)可从 Elsevier 免费下载 Excel；程序化访问需 Scopus/Elsevier API key（机构订阅）。

【链接】https://www.scopus.com/sources ｜ Scopus 内容 https://www.elsevier.com/products/scopus/content ｜ CiteScore 说明 https://en.wikipedia.org/wiki/CiteScore

【已知坑/局限】CiteScore 分母比 IF 宽，数值与 IF 不可直接比；覆盖广也意味着鱼龙混杂，需配预警名单；完整指标/被剔除记录看官方 source list。

---

## DOAJ (Directory of Open Access Journals)

【是什么】社区策展的合规开放获取期刊白名单，22,000+ 刊。是判定"正规 OA 期刊 vs 掠夺性 OA"的关键反查点：被 DOAJ 收录是正面信号。提供免费公共 REST API 与 CC0 元数据。

【可复用方法/真实端点/参数】
- Base URL：`https://doaj.org/api/v3/`
- 检索端点：`GET /api/v3/search/journals/{search_query}`、`GET /api/v3/search/articles/{search_query}`；单条 `GET /api/v3/journals/{journal_id}`、`/articles/{article_id}`。
- 查询语法：Elasticsearch query string，可按字段，如 `search/journals/issn:1234-5678`、`bibjson.title:...`。
- 参数：`page`、`pageSize`(默认/上限较小，分页拉取)、`sort=field:direction`(如 `bibjson.title:desc`)。
- 认证：检索/读取公开免授权；创建/更新 application 等写操作需 `api_key`（账号 Dashboard 生成），属"非公开"端点。
- 批量：`/bulk/articles`、`/bulk/applications` 需认证；全量元数据有 CC0 公开 data dump 可下载。
- 收录门槛(可作合规清单)：真同行评议、即时开放无 embargo、有独立网站与 OA 声明、年发文≥5、已运营≥1年或已发≥10 篇 OA。
- DOAJ Seal：满足一组更高最佳实践(如长期保存、持久标识符 DOI、自存档政策、CC 许可、元数据提供等)的标识，是更强的质量信号。

【链接】API 文档 https://doaj.org/api/docs ｜ swagger https://doaj.org/api/v3/swagger.json ｜ 关于 https://doaj.org/about/

【已知坑/局限】DOAJ 只管 OA 期刊，订阅刊不在内（不在 DOAJ ≠ 掠夺性）；收录是动态的，被移除是危险信号；API pageSize 有上限，大批量用 data dump。

---

## CCF 推荐国际学术会议和期刊目录

【是什么】中国计算机学会发布的计算机领域会议/期刊分级目录（现行 2022 版），分 A/B/C 三档（A 最高，顶级；B 优秀；C 良好/有价值），是国内计算机方向毕业、考核、求职最常用的"档位"基准。

【可复用方法/真实端点/参数】
- 三档语义：A=本领域顶尖（如 OSDI/SIGCOMM/CCS/SIGMOD/STOC/SIGGRAPH/NeurIPS·AAAI 级、TOCS/TON 等顶刊）；B=知名/优秀；C=入门级正规会刊。给学生建议时优先用 CCF 档而非 IF。
- 十个领域分类（id:中文 / English）：
  0 计算机体系结构/并行与分布计算/存储系统；1 计算机网络；2 网络与信息安全；3 软件工程/系统软件/程序设计语言；4 数据库/数据挖掘/内容检索；5 计算机科学理论；6 计算机图形学与多媒体；7 人工智能；8 人机交互与普适计算；9 交叉/综合/新兴。
- 每条记录含 abbr(缩写)、name(全称)、publisher、type(Journal/Conference)、rank(A/B/C)、领域 id——可直接做成结构化表按方向+目标档筛候选。
- 可复用结构化数据源（社区整理，需核对官方）：见下方 gist。

【链接】官方 https://www.ccf.org.cn/Academic_Evaluation/By_category/ ｜ 结构化 2022 版数据 https://gist.github.com/anyzelman/57d1b8c5ada9399698dbb8dcbfa0484d

【已知坑/局限】仅限计算机领域，跨学科不适用；只分 A/B/C 不给录用率/周期，需配 LetPub/官网补；榜单约数年更新，引用前确认是最新版；部分会议改名/合并需核对。

---

## 北大核心（中文核心期刊要目总览）

【是什么】北京大学图书馆主持的《中文核心期刊要目总览》，遴选各学科"核心区"中文期刊，约每 4 年一版（现行第 10 版，2023 年版）。是国内中文期刊"核心"认定最广用的一套。

【可复用方法/真实端点/参数】
- 评价方法：多指标定量综合+学科专家定性。常用指标包括被摘量、被摘率、被引量、他引量、影响因子、被国内外重要数据库收录、基金论文比、Web 下载量、获奖情况等，按学科分别加权排序取核心区。
- 用法：按学科找"是否北大核心"，作为中文期刊的硬门槛（很多单位毕业/评职要求中文核心起步）。
- 与其他中文体系并列核对：北大核心、CSSCI(南大核心)、CSCD、科技核心(统计源)四套口径不同，一刊可能只命中其中几套，报告要分别列。

【链接】北京大学期刊网 https://ccj.pku.edu.cn/

【已知坑/局限】无公开 API，需查官方名录/图书馆数据库；版本之间进出变动大，必须标明版本年份；只覆盖中文刊。

---

## CSCD / CSSCI（中国科学引文数据库 / 中文社会科学引文索引）

【是什么】两套中文来源期刊体系：CSCD 由中科院文献情报中心建（理工医，分核心库 C 与扩展库 E）；CSSCI（南大核心）由南京大学建（人文社科，含来源期刊与扩展版、集刊）。是理工/社科方向中文期刊的权威认定。

【可复用方法/真实端点/参数】
- CSCD：核心库(C)门槛高于扩展库(E)；常与 SCI 类比，理工方向中文投稿优先看 CSCD-C。
- CSSCI：南大每 2 年遴选来源期刊；社科方向"C 刊"通常即指 CSSCI 来源期刊，扩展版次之，集刊单列。给社科作者定位时，CSSCI ＞ 北大核心 ＞ 普通刊 是常见硬梯度。
- 用法：按学科类别核查命中哪套哪库，连同北大核心一起作为中文档位标注。

【链接】CSSCI/南大核心(中国社会科学研究评价中心) https://cssrac.nju.edu.cn/ ｜ CSCD(中国科学文献服务系统) http://sciencechina.cn/ ｜ CSSCI 概览 https://en.wikipedia.org/wiki/Chinese_Social_Sciences_Citation_Index

【已知坑/局限】均需机构订阅库核查、无开放 API；遴选周期短、进出频繁，务必标版本；CSCD(理工) 与 CSSCI(社科) 学科不重叠，别张冠李戴。

---

## 中科院分区（SCI 期刊分区表，附：与上面三套指标的关系）

【是什么】中科院文献情报中心基于 WoS/JCR 数据做的国产 SCI/SSCI 分区，国内认可度极高。分"基础版"和现主推"升级版"，按大类(13)与小类学科双重分区，1 区门槛远高于 JCR 分区（金字塔式：1 区约前 5%）。另发布 Top 期刊与《国际期刊预警名单》。

【可复用方法/真实端点/参数】
- 升级版用"期刊超越指数"等替代单纯 IF 排序，1/2/3/4 区按比例划分（1 区约前 5%，呈金字塔，故"中科院 1 区"远难于"JCR Q1"）。
- 大类(如"计算机科学")给总体分区，小类给细分方向分区，二者可不同——评估要看作者关心的口径。
- Top 期刊：1 区刊 + 部分综述/2 区高影响刊的特别标注。
- 预警名单：每年发布，按风险高/中/低标注问题刊（异常自引、超高发文/快审、国人发文占比畸高、商业模式可疑等），命中=强烈劝退信号，直接联动预警筛查。

【链接】期刊分区表官网 https://www.fenqubiao.com/

【已知坑/局限】需订阅/机构访问看完整表；"中科院分区"≠"JCR 分区"，数值口径差异巨大，必须显式标注是哪套；分区每年更新且偶有大改（如升级版上线导致刊降区）；预警名单年度变动，投前现查最新版。

---

## Elsevier JournalFinder

【是什么】Elsevier 官方免费稿件-期刊匹配工具，基于论文题目+摘要用 NLP/向量匹配，推荐 Elsevier 旗下相关期刊并附投稿决策指标。

【可复用方法/真实端点/参数】
- 输入：粘贴 paper title + abstract（可选研究领域），不需投稿即可用。
- 输出每刊：CiteScore、Impact Factor、接受率(acceptance rate)、首次决定时长(time to first decision)、生产/出版周期、OA 选项与 APC、是否支持开放获取。
- 可复用的"决策维度"：把"首次决定时长 + 接受率 + APC + OA"四项作为周期/费用/概率评估的标准字段抓取。

【链接】https://journalfinder.elsevier.com/ ｜ 说明 https://researcheracademy.elsevier.com/publication-process/finding-right-journal

【已知坑/局限】只覆盖 Elsevier 自家期刊，结论有出版商偏向，不能当全市场推荐；指标随刊更新；匹配靠文本相似度，跨学科/新方向易偏。

---

## Springer Nature Journal Suggester

【是什么】Springer Nature 官方免费匹配工具，输入摘要/稿件文本做语义匹配，推荐 SN 旗下期刊（含大量 OA 刊）。

【可复用方法/真实端点/参数】
- 输入：粘贴 manuscript text / abstract（可加学科）。
- 输出每刊：影响因子、首次决定中位时长、是否 OA / 混合 OA、APC 金额、接受率(若有)、是否符合某些 OA 资助协议(transformative agreement)。
- 可复用点：对预算敏感的作者，用它快速比对同方向 SN 刊的 APC 与 OA 资助减免可能。

【链接】https://journalsuggester.springer.com/

【已知坑/局限】同样只限 Springer Nature 自家刊，有出版商偏向；侧重 OA、APC 普遍偏高，给低预算/本科生时要提醒费用。

---

## IEEE Publication Recommender

【是什么】IEEE 官方免费工具，输入关键词或题目/摘要，推荐匹配的 IEEE 期刊与会议并并排比较指标。计算机/电子/通信方向定位主力。

【可复用方法/真实端点/参数】
- 输入：关键词，或上传/粘贴文章题目与摘要（有 50MB 文件上限）。
- 输出每个 publication：Impact Factor、Eigenfactor Score(按施引刊声望加权的五年被引网络指标)、Article Influence(篇均影响)、投稿到发表周期(submission-to-publication，周)、OA 选项、出版频率；期刊与会议都覆盖。
- 可复用点：IEEE 会议多、周期是关键，抓"submission-to-publication 周数"做时间规划；与 CCF 档位交叉验证（IEEE 会议对照 CCF A/B/C）。

【链接】https://publication-recommender.ieee.org/ ｜ 介绍 https://ieeetv.ieee.org/ieee-products/introducing-the-publication-recommender-tool

【已知坑/局限】只覆盖 IEEE 出版物，有出版商偏向；明确声明使用该工具不等于投稿、不保证录用；纯文本匹配，需人工核对方向真匹配。

---

## LetPub（SCI 期刊查询数据库）

【是什么】国内常用的 SCI 期刊综合查询站，把多源指标聚合成中文友好的单刊画像，是给中国作者定位时最省事的"一站查"。

【可复用方法/真实端点/参数】
- 单刊字段（可作抓取清单）：期刊名/缩写、ISSN/E-ISSN、最新影响因子 + JCR 分区、5 年平均 IF、中科院分区(大类/小类)、自引率、研究方向、审稿周期/时间、录用比例、年发文量与国人发文占比、是否 OA、版面费(APC)、官网与投稿系统链接，并标注是否在预警名单。
- 可复用点：一处同时拿到 IF/JCR 分区/中科院分区/审稿周期/录用率/国人占比/APC，正好覆盖本技能的对比表全部列；"国人发文占比畸高"是预警交叉信号。

【链接】期刊检索 https://www.letpub.com.cn/index.php?page=journalapp ｜ 单刊示例 https://www.letpub.com.cn/index.php?journalid=11049&page=journalapp&view=detail

【已知坑/局限】聚合数据有滞后/偶错，关键数值(IF、分区、预警)须回官方源(JCR/中科院/期刊官网)二次核实；无开放 API，网页禁爬；**"录用比例/审稿周期"多为社区投稿经验估计，非官方统计——本技能明确禁止把 LetPub 的"录用比例"当作录用概率数字写进报告**（详见 SKILL.md「录用可能性评估 rubric」），录用可能性一律走可核查信号的定性分级(高/中/低)，仅在官网/正式报告公开接收率时才给具体数字并附链接。

---

## EI 核查路径（Compendex Source List，研究日期 2026-06-11）

【是什么】EI（工程索引）现由 Elsevier 的 Engineering Village 平台承载，核心库即 **Compendex**。判定"某刊/某会是否被 EI 收录"的权威依据是 Engineering Village 官方发布的 **Compendex Source List**（收录刊单 Excel），而非任何第三方"EI 源刊查询"站。

【可复用方法/真实路径/实查留痕（2026-06-11，curl）】
- Engineering Village 入口 `https://www.engineeringvillage.com` → **HTTP 302**（跳登录，库内检索需机构订阅）。
- Compendex 产品页 `https://www.elsevier.com/products/engineering-village/databases/compendex` → **HTTP 200**；页内 "View source list" 链接指向官方收录刊单 Excel。
- 实测：该 "View source list" 当前指向 Contentful CDN 资产 `https://assets.ctfassets.net/.../CPXSourceList_052026__1_.xlsx` → **HTTP 200，约 5.6 MB**（文件名 `CPXSourceList_052026` = 2026 年 5 月版）。**此 CDN 链接会随版本更新而变，务必每次从产品页 "View source list" 现取，不要硬编码 CDN 路径。**
- 间接核查法（无订阅时）：① 下载 Compendex Source List Excel，按刊名/ISSN 在表内查是否在列；② 看出版方/会议官网是否声明 "Indexed by Ei Compendex"，再回 source list 复核；③ 会议论文集多经 IEEE Xplore/ACM DL/Springer 出版后被 EI 收录，可结合出版方确认。Source List 产品页说明其内容来自数千家出版方，含 IEEE、ASME、SAE、ACM 等主要工程学会。

【已知坑/局限】
- **严禁引用过期的第三方"EI 源刊目录"站**（大量 `ei*.com`/个人整理表已多年不更新或为营销站），收录状态只认 Engineering Village 官方 source list 的当期版本。
- 收录是动态的，刊/会可能被移除；投稿前须现查最新版 source list，并标 last_checked。
- 本轮只验证了 source list **下载入口活性**，未对具体中文刊做逐条收录核对——逐条查是投稿前动作（下载 5.6 MB Excel 按 ISSN 检索）。

【链接】产品页 https://www.elsevier.com/products/engineering-village/databases/compendex ｜ 平台 https://www.engineeringvillage.com （收录刊单从产品页 "View source list" 现取）

---

## 国内会议信号源（CCF 目录 / 一级学会官网 / 假会议识别，研究日期 2026-06-11）

【是什么】国内（含中文）学术会议没有像 SCI/EI 那样的单一权威库，正规性要靠多信号交叉判断：CCF 推荐目录（限计算机）、主办方是否为一级学会、出版与检索去向。

【可复用方法/真实路径/实查留痕（2026-06-11）】
- **CCF 推荐目录**（计算机方向首选档位）：`https://www.ccf.org.cn/Academic_Evaluation/By_category/` → **HTTP 200**；分 A/B/C 三档、十大领域，详见上文 "CCF 推荐国际学术会议和期刊目录"节。计算机方向的国内/国际会议先对 CCF 档；非计算机方向 CCF 不适用。
- **一级学会官网**：正规国内会议多由全国性一级学会（及其专委会）主办，如中国计算机学会(ccf.org.cn)、中国电子学会、中国自动化学会、中国人工智能学会等。核查办法：到学会官网"学术活动/会议通知"栏目核对该会是否在官方议程内，主办/承办单位是否与会议征稿启事一致。
- **出版与检索去向**：正规会议会明确说明论文集出版方（IEEE/ACM/Springer LNCS/EI 会议集等）与检索去向，且可在出版方平台或 Compendex Source List（见上节）复核；只承诺"录用即 EI/SCI 检索"却拿不出出版方信息的，视为危险信号。

【假会议识别三红线（命中任一即高度警惕）】
1. **"交钱包录、几天给录用"**：承诺极短周期录用、无实质同行评议、强调缴费即出版。
2. **检索承诺无出处**：声称"100% EI/Scopus 检索"却不给出版方与刊号/会议集信息，或所列检索源查无实据（回 source list / 出版方官网查不到）。
3. **主办方身份含糊或冒名**：主办单位查无此学会、盗用知名学会/高校名义、官网域名与正规学会无关、同一壳子每年换名批量办会、广撒约稿邮件。

【已知坑/局限】
- CCF 目录只覆盖计算机领域，其他学科无对应统一目录，更依赖"一级学会主办 + 出版检索去向"两项判断。
- 学会官网信息更新有滞后，承办信息以学会官方通知为准，不轻信第三方会议聚合站/约稿邮件。
- "EI/Scopus 检索"是投稿后、出版后的结果，征稿阶段的检索承诺只能作参考、不能当保证，须按上文 EI 核查路径回官方源复核。

【链接】CCF 目录 https://www.ccf.org.cn/Academic_Evaluation/By_category/ ｜ 各一级学会官网（按方向查），出版检索去向回出版方平台 + Compendex Source List 复核。

---

## 交叉使用要点（写报告必记）

- 三套分区不可混：JCR 分区(科睿唯安) / SJR 分区(Scopus) / 中科院分区(国产，1 区门槛最高) 口径完全不同，每次标注来源+年份。
- 三类指标各有用途：IF/CiteScore 看引用热度，SJR/Eigenfactor 看声望加权，CCF/中科院分区/北大核心/CSSCI 看国内认可档位。给学生定位优先用"档位"而非裸 IF。
- 出版商自家匹配工具(Elsevier/Springer/IEEE)有偏向，只能作候选发现，全市场判断要靠 OpenAlex/Scopus/WoS + 本土榜单。
- 预警/掠夺核查走"白名单(DOAJ收录、被正规库索引) + 黑名单(中科院预警名单)"双向，命中黑名单或异常(超快审稿、国人占比畸高、高 APC、虚假指标)即标红劝退。
- 所有数值有时效，引用前 last_checked，以 db01 + 官方源为准。
