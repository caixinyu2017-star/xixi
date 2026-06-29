# light-ip-application 参考工具研究笔记

> 本文件为逐工具的可核查硬信息记录，供 SKILL.md 调用。所有端点/语法以官方文档为准；标注"未能核实"的项不得在产出中当作事实使用。
> 研究日期：2026-06。

---

## Google Patents

【是什么】Google 的免费专利检索界面（patents.google.com），覆盖全球 100+ 专利局、含全文 OCR 与机器翻译、引用关系、非专利文献（NPL）。无官方对外检索 REST API（Google Patents 与 Google Scholar 都没有官方公开 API）。

【可复用方法/真实端点/参数】
- 网页高级检索 URL 参数式：`https://patents.google.com/?q=...&before=priority:20200101&after=...&country=CN,US&inventor=...&assignee=...&language=ENGLISH`。
- 检索语法：支持词组（引号）、CPC 分类码（如 `G06N3/08`）、`country=`、`before:/after:` 配合 `priority`/`filing`/`publication` 日期类型。
- 程序化获取唯一官方途径是 **BigQuery 公开数据集** `patents-public-data.patents.publications`（Google Patents Public Datasets）。可用 SQL 跑大规模检索/分析，核心字段：`publication_number`、`application_number`、`title_localized`、`abstract_localized`、`claims_localized`(均为带语言变体的嵌套结构)、`cpc`、`ipc`、`assignee_harmonized`、`inventor_harmonized`、`priority_date`、`filing_date`、`publication_date`、`citation` 等。官方示例仓库含 patent landscaping（从种子集找相关专利）、claim 文本抽取、claim breadth ML 估计等 notebook（仓库 2026-04 起已归档只读）。
- 第三方封装（非官方、收费）：SerpApi 的 Google Patents API（`engine=google_patents`）。仅在用户已有 key 且接受合规风险时使用。

【链接】
- https://patents.google.com/
- https://github.com/google/patents-public-data
- https://cloud.google.com/blog/topics/public-datasets/google-patents-public-datasets-connecting-public-paid-and-private-patent-data/
- https://serpapi.com/google-patents-api （第三方）

【已知坑/局限】机器翻译/OCR 可能有误，法律状态非权威（以各局官方为准）；无官方检索 API，爬取网页违反 ToS；BigQuery 需 GCP 账号且按查询量计费；不能作为 FTO（自由实施）法律结论来源。

---

## WIPO PATENTSCOPE

【是什么】WIPO 的全球专利检索系统，核心覆盖 PCT 国际申请（公开当日可见）+ 70 余个国家/地区库；强项是 **CLIR 跨语言检索**（一个语种查词自动扩展到多语种同义词）与化学结构检索。

【可复用方法/真实端点/参数】
- 高级检索使用字段码 + 布尔/邻近运算符。常用字段码：`EN_TI`(英文标题)、`EN_AB`(英文摘要)、`EN_DE`(说明书)、`EN_CL`(权利要求)、`FP`(首页/前页全文)、`IC`(IPC 分类)、`PA`(申请人)、`IN`(发明人)、`DP`(公开日)、`AD`(申请日)、`PN`(公开号)。
- 运算符：`AND OR NOT`、邻近 `NEAR`/`P`(同段)/`S`(同句)，可带距离如 `NEAR5`；截词 `*`(多字符)、`?`(单字符)。
- CLIR：在"跨语言扩展"里输入一个语种关键词，系统给出多语种同义词供勾选，适合中国申请人查外文在先技术。
- 有 SOAP/REST 形式的 PCT 数据 web service，但访问需申请；网页高级检索是最稳的免登录入口。

【链接】
- https://patentscope.wipo.int/search/en/search.jsf
- https://www.wipo.int/en/web/patents/patent-information

【已知坑/局限】各国库收录时滞与字段完整度不一；机器翻译辅助仅供理解；REST/SOAP 数据服务的字段与配额未能逐项核实（以 WIPO 官方 API 文档为准）。

---

## EPO Espacenet / Open Patent Services (OPS) API

【是什么】欧洲专利局的官方机器接口 OPS，提供著录项、说明书全文、法律状态（INPADOC）、同族（patent family）、引用、图像等。配套人机界面是 Espacenet（worldwide.espacenet.com）。需在 EPO Developer Portal 注册应用拿到 Consumer Key/Secret。

【可复用方法/真实端点/参数】
- Base：`https://ops.epo.org/3.2/rest-services`（版本号会演进，以门户为准）。
- 认证：OAuth2 client_credentials。先 POST `https://ops.epo.org/3.2/auth/accesstoken`（Basic Auth 带 base64(consumer_key:secret)，body `grant_type=client_credentials`）换取 `access_token`（有效约 20 分钟），后续请求 `Authorization: Bearer <token>`。
- 关键服务：
  - 检索：`/published-data/search`（CQL 查询，参数 `q=`，可加 `Range: X-Y` 头取第 X–Y 条，每页上限 100）。
  - 著录/全文/同族：`/published-data/publication/{format}/{number}/biblio`（或 `/fulltext`、`/claims`、`/description`）。
  - 同族：`/family/publication/docdb/{number}`。
  - 法律状态：INPADOC legal 服务。
  - 图像：`/published-data/images`。
- CQL 字段：`ti=`(标题)、`ab=`(摘要)、`ta=`(标题或摘要)、`txt=`(全文)、`pa=`(申请人)、`in=`(发明人)、`cpc=`/`ipc=`、`pn=`(公开号)、`pd=`(公开日，支持 `within "20200101 20201231"`)。

【限流/配额】OPS 实行**红绿灯式节流**：每个响应带 `X-Throttling-Control` 头，给出系统总体状态（idle/busy/overloaded）以及 5 类服务各自的颜色档（green/yellow/black）：`images`(图像)、`inpadoc`(同族/法律状态)、`other`(号码/法律/register)、`retrieval`(著录/全文取用)、`search`(检索)。节流基于**1 分钟滚动窗口**，客户端应按头里的颜色自适应降速；overloaded/black 时请求被拒（403）。另有按注册用户的**每周数据量配额**（GB 级，超限触发 `RegisteredQuotaPerWeekExceeded`）与**每小时请求数上限**（超限触发 `IndividualQuotaPerHourExceeded`）。具体 GB 阈值以登录后门户为准。

【链接】
- https://developers.epo.org/
- https://worldwide.espacenet.com/
- https://www.epo.org/en/searching-for-patents/data/web-services
- https://github.com/sujith3g/epo-ops （第三方封装可参考调用模式）

【已知坑/局限】token 短时过期需缓存复用；分页用 `Range` 头而非 offset 参数；号码格式区分 docdb/epodoc/original，传错查不到；法律状态仅供参考非权威。

---

## CNIPA 专利检索（国家知识产权局）

【是什么】中国国家知识产权局官方"专利检索及分析"系统，权威的中国专利数据（发明/实用新型/外观）来源，含法律状态、同族、运营信息。是中国申请前查新与同族核对的首选。

【可复用方法/真实端点/参数】
- 入口：`https://pss-system.cponline.cnipa.gov.cn`（需注册登录；常规检索免费）。
- 检索方式：常规检索（关键词/申请号/公开号）、高级检索（字段表达式）、命令行检索。
- 常用字段：申请号、公开（公告）号、名称(TI)、摘要(AB)、权利要求、说明书、申请人、发明人、IPC 分类号、申请日、公开日。
- 法律状态字段对查新很关键：可筛"有权/无权/审中/驳回/撤回"等，避免引用已失效或未授权文献。

【链接】
- https://pss-system.cponline.cnipa.gov.cn
- https://english.cnipa.gov.cn/

【已知坑/局限】无公开 REST API（程序化访问需走授权数据服务/第三方商业库如 incoPat、PatentHub）；登录与验证码限制自动化；最近申请有公开时滞（发明自申请日 18 个月公开）。

---

## The Lens API（lens.org）

【是什么】Cambia/QUT 运营的开放创新情报平台，单一接口聚合专利（>1.6 亿）+ 学术文献（>2.7 亿）+ 二者关联（专利引学术、PatCite）。适合做"专利—论文"双向关联分析。API 需注册并申请 token（学术用途可免费授权）。

【可复用方法/真实端点/参数】
- 专利检索：`POST https://api.lens.org/patent/search`
- 学术检索：`POST https://api.lens.org/scholarly/search`
- 认证：HTTP 头 `Authorization: Bearer <token>`（或 `?token=` 查询参数）；`Content-Type: application/json`。
- 请求体（Elasticsearch 风格 DSL）：
  ```json
  {
    "query": {"match": {"title": "neural network"}},
    "size": 50,
    "from": 0,
    "sort": [{"date_published": "desc"}],
    "include": ["lens_id","biblio","abstract"]
  }
  ```
  也支持 `{"query_string":{"query":"title:(...) AND class_cpc.symbol:G06N*"}}`。
- 分页：浅分页用 `size`+`from`；深分页/全量导出用 `scroll`（首次传 `"scroll":"1m"`，响应返回 `scroll_id`，后续请求带 `{"scroll_id":"...","scroll":"1m"}`；`scroll_id` 过期会返回 404）。
- 返回字段（patent）：`lens_id`、`biblio`(标题/摘要/分类/申请人/日期)、`claims`、`description`、`legal_status`、`families`、`cited_by`/`references`。

【限流/配额】按订阅计划分级限流。响应头给出实时用量，可据此自适应：`x-rate-limit-remaining-request-per-minute`、`x-rate-limit-remaining-request-per-month`、`x-rate-limit-remaining-record-per-month`、`x-rate-limit-retry-after-seconds`/`-millis`、`x-rate-limit-reset-date`。超限返回 **429 Too Many Requests**。具体每分钟/每月数值随计划变化，以账户 dashboard 为准。

【链接】
- https://docs.api.lens.org/getting-started.html
- https://docs.api.lens.org/request-patent.html
- https://docs.api.lens.org/request-scholar.html
- https://www.lens.org/

【已知坑/局限】免费/学术 token 有配额，批量导出走 scroll 而非大 size；DSL 与 ES 语法贴近但字段名需查文档；商用需付费授权。

---

## USPTO Patent Public Search (PPUBS) / PatentSearch API（原 PatentsView）

【是什么】
- **PPUBS**：USPTO 官方人机检索系统（2022 起替代 PatFT/AppFT 等四套旧系统），免费、含美国授权专利与公开申请全文。
- **PatentSearch API（原 PatentsView）**：USPTO 资助的官方开放数据 API，结构化字段（专利、申请人、发明人、引用、CPC 等），适合程序化抓取与统计分析。

【⚠️ 重大变更（curl 实测 2026-06-06）】PatentsView 已完成向 USPTO Open Data Portal（ODP）的迁移：
- 旧 legacy `https://api.patentsview.org/patents/query` → **HTTP 301**，重定向到 `https://data.uspto.gov/support/transition-guide/patentsview`（已停服，2025-02 起）。
- 过渡端点 `https://search.patentsview.org/api/v1/` → 本机 **DNS 无法解析（Could not resolve host，curl HTTP 000；本机 DoH 亦被网络策略拦截）**，故**未能实测其在线状态**；官方迁移指南已宣布该域属过渡安排，能否程序化访问以 ODP 为准。
- `https://patentsview.org/apis/*` → **HTTP 301**，同样指向 data.uspto.gov 迁移指南。
- 迁移目的地 ODP：`https://data.uspto.gov/` → **HTTP 200**（站点在线）；其 API 形如 `https://data.uspto.gov/api/v1/patent/applications/search` → **HTTP 200**；另有 `https://api.uspto.gov/api/v1/patent/applications/search` → **HTTP 401**（端点存在，需 key/鉴权）。
- 结论：PatentsView 风格旧端点（api./search.patentsview.org）均已不可用，**程序化访问统一走 data.uspto.gov 的 ODP API**，调用前到 ODP 注册 key 并核对当前在用的 base URL 与各端点路径（ODP 页面 JS 渲染，逐字端点清单需人工核对，本次未抓全）。

【可复用方法/真实端点/参数】
- PPUBS 检索语法（fielded search）：
  - 字段码后缀格式：`词.字段.`，如 `nanowire.ti.`(标题)、`graphene.ab.`(摘要)、`.pn.`(专利号)、`.in.`(发明人)、`.cpcl.`(CPC)。
  - 布尔：`AND OR NOT XOR`；邻近：`ADJ`(相邻,可 `ADJ3`)、`NEAR`、`WITH`(同句)、`SAME`(同段)；截词：`$`(任意长度)、`?`(0或1字符)、`!`(1字符)。
  - 日期：`@pd>=20200101`(公开日)、`@ad`(申请日) 等。字段索引清单见 USPTO Searchable indexes 页。
- PatentSearch API（旧 `search.patentsview.org` 本机无法解析、未能实测；**现统一以 data.uspto.gov 的 ODP API 为准**，下列查询 DSL 为 PatentsView 沿用风格，端点路径以 ODP 文档为准）：
  - 资源类型如 patent / assignee / inventor / cpc_class / us_patent_citation 等。
  - 认证：申请 API key（ODP 注册），放 `X-Api-Key` 请求头。实测 `https://api.uspto.gov/api/v1/...` 无 key → 401。
  - 查询三参数：`q`(查询，JSON)、`f`(返回字段数组)、`o`(选项如分页 size/after)、`s`(排序)。
  - 查询运算符：`_and _or _not`、`_gt _gte _lt _lte`、`_begins`、`_contains`、文本 `_text_any _text_all _text_phrase`。
  - 示例：`q={"_and":[{"_gte":{"patent_date":"2020-01-01"}},{"_text_phrase":{"patent_abstract":"neural network"}}]}`。
  - 分页：`o={"size":1000,"after":"<last_id>"}` 游标式（单页上限 1000，总量可深翻）。

【限流/配额】PatentSearch API 官方文档载明约每分钟 45 次请求；迁移到 ODP 后以 data.uspto.gov 的 swagger/文档为准（若有调整以官方为准）。PPUBS 为交互界面无公开 API 配额。

【链接】
- https://ppubs.uspto.gov/pubwebapp/
- https://www.uspto.gov/patents/search/patent-public-search/searchable-indexes
- https://data.uspto.gov/（USPTO Open Data Portal，PatentsView 迁移目的地）
- https://data.uspto.gov/support/transition-guide/patentsview
- https://www.uspto.gov/subscription-center/2026/patentsview-migrating-uspto-open-data-portal-march-20

【已知坑/局限】仅覆盖美国数据；**端点迁移已完成：旧 `api.patentsview.org` 301 弃用、过渡域 `search.patentsview.org` 本机无法解析（受网络策略限制，未能实测其在线状态），程序化访问统一走 data.uspto.gov 的 ODP API**，编码前必须到 data.uspto.gov 注册 key 并核对最新 base URL 与端点路径；PPUBS 语法与 PatentSearch 查询 DSL 完全不同别混用。

---

## OpenAlex

【是什么】开放学术知识图谱（替代已停服的 Microsoft Academic Graph），覆盖 works/authors/sources/institutions/concepts/topics/publishers/funders 等实体。用于专利场景的"非专利文献(NPL)在先技术"与作者机构关联检索。**接入口径（是否需 key、限流、计费）以 m01（light-literature-search）references「OpenAlex 接入真相源」节为全仓库唯一真相源**，本技能不复写数字。

【认证现状（以 m01 真相源为准；下为历史 curl 实测存档）】现行政策：OpenAlex 2026 起**需免费 API key**（官网 2026-06-11 核实，额度/限流见 m01 真相源节）。生产代码一律按"需 key"实现，到 https://openalex.org/settings/api 免费申请。
- 历史存档：本技能 2026-06-06 curl 实测曾记到——无 key 无 mailto `GET /works?per_page=2` → HTTP 200；带 mailto 仍有效；传伪造 key → 401。合理解释：key 强制处于灰度/过渡期，匿名当时仍被放行但额度受限、不保证。**以官网现行口径为准，不要据此实测认定匿名长期可用。**

【可复用方法/真实端点/参数】
- Base：`https://api.openalex.org`，实体端点 `/works`、`/authors`、`/sources`、`/institutions`、`/concepts`、`/topics`。
- 认证：**2026 起需免费 API key**（口径见 m01 真相源节），放 `?api_key=YOUR_KEY`；建议同时带 `?mailto=you@example.com` 进入 polite pool。免费注册见 https://openalex.org/settings/api 。
- 单条：`/works/W2741809807` 或用外部 ID `/works/doi:10.7717/peerj.4375`。
- 过滤：`?filter=` 逗号分隔即 AND，如 `?filter=publication_year:2020,title.search:graphene,authorships.institutions.country_code:CN`；行内运算符如 `cited_by_count:>100`；全文/标题搜索用 `?search=`。
- 分页：浅页 `per_page`（1–200，**上限 200**，默认 25）+ `page`；深分页/全量用游标 `cursor=*`（响应 `meta.next_cursor` 续传）。`page`+`per_page` 方式最多翻到第 10,000 条，更深必须用 `cursor`。
  - 实测（2026-06-06）：`?per_page=200` → HTTP 200 正常返回；`?per_page=201` → **HTTP 400**，错误体 `{"error":"Pagination error.","message":"per-page parameter must be between 1 and 200."}`，由 API 自身确认上限即 200。
- 聚合统计：`?group_by=publication_year`（或任意可分组字段）直接出计数分布。
- 字段裁剪：`?select=id,title,publication_year,doi,cited_by_count`。

【限流/配额】见 m01 references「OpenAlex 接入真相源」节（全仓库唯一存具体口径处：现行为需免费 key + 按量额度）。本技能不复写数字。

【链接】
- https://developers.openalex.org/（新文档站）
- https://developers.openalex.org/guides/authentication
- https://api.openalex.org/works

【已知坑/局限】免费匿名即可用，带 `mailto` 进 polite pool 更稳；`api_key` 可选，传错 key 反而 401。`per_page` 上限 **200**（API 错误信息明确"between 1 and 200"），`page` 方式最多到第 10,000 条，更深翻必须用 `cursor`；机构/概念消歧偶有噪声；非专利数据库，仅作 NPL 与文献关联补充。

---

## 中国版权保护中心 — 软件著作权（软著）申请流程

【是什么】中国版权保护中心（CPCC, ccopyright.com）是计算机软件著作权登记的官方机构。软著不审查代码质量/新颖性，仅做形式登记，确认权属与完成时间，是常见的资质/项目交付与申报材料。

【可复用方法/复用要点】
- 申请途径：线上"中国版权保护中心"软件著作权登记系统在线填报 + 电子/纸质材料。
- 核心材料清单：
  1. 软件著作权登记申请表（系统生成）。
  2. **源程序**：通常提交前 30 页 + 后 30 页，连续，每页约 50 行（不足 60 页则全部提交）；页眉含软件全称及版本号；去除注释中的个人/敏感信息。
  3. **文档**：用户操作手册或设计说明书，前 30 页 + 后 30 页规则同上；含界面截图、功能模块说明。
  4. 权属/身份证明：企业营业执照或个人身份证；合作/委托/职务开发需相应权属证明。
- 关键登记信息：软件全称+简称+版本号、开发完成日期、首次发表日期（未发表可填）、开发方式（独立/合作/委托/职务）、权利取得方式。
- 周期：受理后官方法定审查期约 30 个工作日（可付费加急缩短，具体档位以中心公告为准，未逐字核实）。下证为《计算机软件著作权登记证书》。

【链接】
- https://www.ccopyright.com/
- https://register.ccopyright.com/ （登记系统入口，以官网为准）

【已知坑/局限】源代码与文档须真实对应、不得拼凑/虚构；软件名一旦登记不便更改；软著不保护思想/算法本身（如需保护技术方案应走专利）；加急费用与时效以官方为准。

---

## 专利权利要求书 撰写规范

【是什么】权利要求书界定专利保护范围，是侵权判定的法律基准（《专利法》及实施细则、审查指南为依据）。

【可复用方法/撰写要点】
- 总原则：权利要求应**以说明书为依据**，清楚、简要地限定保护范围；用说明书支持的技术特征表述。
- 独立权利要求：
  - 须记载解决技术问题的**全部必要技术特征**，构成最大保护范围。
  - 推荐"两部分撰写法"：**前序部分**（主题名称 + 与现有技术共有的特征）+ **特征部分**（用"其特征在于"引出区别于现有技术的技术特征）。
- 从属权利要求：用"根据权利要求 N 所述的……，其特征在于……"引用在先权利要求，附加技术特征作进一步限定（逐层缩小、增加稳定性）。引用多项时用"或"且不得反向引用编号更大的项。
- 撰写禁忌：不用功能性/结果性含糊措辞（除非说明书充分支持）；避免"约""左右"等不清楚用语；不出现说明书未公开的特征（缺乏支持）；保持术语前后一致。
- 单一性：一份申请的多项独立权利要求须属于**一个总的发明构思**（共享相同或相应的特定技术特征）。
- 类型：产品权利要求（结构/组成特征）与方法权利要求（步骤/条件特征）分开撰写，软件类常用"一种……方法"+"一种……装置/系统"+"计算机可读存储介质"组合布局。

【链接】
- 《专利审查指南》（CNIPA 官方）：https://www.cnipa.gov.cn/
- 法规检索：https://english.cnipa.gov.cn/

【已知坑/局限】保护范围与稳定性需权衡（写太宽易被现有技术无效，太窄易规避）；最终文本须由专利代理师审核，本技能仅出草案。

---

## 专利说明书 撰写

【是什么】说明书须**充分公开**发明，使所属领域技术人员无需创造性劳动即可实现（"充分公开"是法定要件，公开不足将导致无法授权或被无效）。

【可复用方法/标准结构】按审查指南规定顺序：
1. **技术领域**：发明所属及直接应用的技术领域（不写背景）。
2. **背景技术**：现有技术现状 + 引用对比文件 + 客观指出其缺陷/待解决问题（不贬损）。
3. **发明内容**：
   - 要解决的技术问题（针对背景缺陷）。
   - 技术方案（与权利要求对应，但更完整地描述）。
   - 有益效果（相对现有技术的优点，最好可量化/有机理说明，支撑创造性）。
4. **附图说明**：逐图说明 + 附图标记清单。
5. **具体实施方式**：≥1 个**实施例**，详述如何实现技术方案、参数取值、流程步骤；软件类给算法流程/模块交互/伪代码级描述，使方案可重现。
- 写作要点：术语与权利要求/附图标记一致；每个权利要求特征都能在说明书找到支持与解释；公开程度匹配保护范围。

【链接】
- 《专利审查指南》：https://www.cnipa.gov.cn/
- 可借鉴范例库：https://patents.google.com/ 、https://pss-system.cponline.cnipa.gov.cn

【已知坑/局限】公开不充分或"事后补充实施例"不被接受（中国不允许超范围修改）；有益效果若无依据易被质疑；最终须代理师审核定稿。
