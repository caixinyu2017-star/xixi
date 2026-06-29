# light-citation 参考工具研究笔记

> 研究方法说明：核心数据/真实性 API（Crossref、DOI 内容协商、OpenAlex、Unpaywall、OpenCitations）
> 已用 curl/urllib **实测固化**，HTTP 码标注于下（测试 DOI `10.1038/s41597-023-02555-8`，由
> `scripts/verify_refs.py`、`scripts/doi_to_any.py` 自测覆盖）。其余工具型条目（Zotero/JabRef/Better
> BibTeX 等）结合官方文档整理，链接经搜索确认可达；少数无法核实之处已标注。
> 最后实测日期：2026-06-06。

---

## Anthropic Citations API（"Citation Management" 能力对应）

【是什么】Anthropic 官方提供的"引用接地"能力，不是独立 skill，而是 Messages API 的一个特性：
把文档作为内容块传入并 `citations.enabled=true`，模型回答时会自动返回引用了原文哪一段的
结构化引用，杜绝凭空捏造。可类比"引用真实性自检"的工程化实现。

【可复用方法】
- 在 `messages` 请求里把来源放进 `document` 类型内容块（支持 plain text、PDF、自定义
  content、search results）。设置该块 `"citations": {"enabled": true}`。
- 回答的 `content` 会带 `citations` 数组，每条含被引原文 `cited_text` 与定位：
  纯文本用 `char_location`（start/end 字符偏移），PDF 用 `page_location`（页码），
  自定义内容用 `content_block_location`（块索引）。
- 借鉴点：审查引用时，要求"每条引用都能指回原文具体位置"——可作为引用真实性核查的硬标准。

【链接】https://docs.anthropic.com/en/docs/build-with-claude/citations ；
公告 https://www.anthropic.com/news/introducing-citations-api

【已知坑】只接地"传进去的文档"，不校验外部真实性；模型仍可能漏引或选错段落，需人工复核。

---

## Crossref REST API

【是什么】Crossref 注册的 DOI 元数据库（>1.5 亿条），引用真实性/元数据核验的首选权威源。免费、免注册。

【✅ 已验证 2026-06-06】
- `GET /works/{doi}` → **HTTP 200**（`https://api.crossref.org/works/10.1038/s41597-023-02555-8?mailto=...`），返回 `message.title/author/issued/DOI/is-referenced-by-count`。
- `GET /works?query.bibliographic=...&rows=1&mailto=...` → **HTTP 200**。
- 不存在的 DOI（如 `10.9999/...`）→ **HTTP 404**（`verify_refs.py` 据此标 severity=high）。
- 由 `scripts/verify_refs.py` 自测覆盖。

【可复用方法/真实端点/参数】
- Base：`https://api.crossref.org`
- 主端点：`/works`（按 DOI 取单条：`/works/{doi}`）；其他：`/members`、`/journals`、`/funders`、`/types`。
- 查询参数：
  - `query=`（全字段自由文本）、`query.bibliographic=`（书目式整句，最适合"标题+作者+年"模糊匹配）、
    `query.author=`、`query.title=`、`query.container-title=`（期刊名）。
  - `filter=`：如 `from-pub-date:2023-01-01`、`type:journal-article`、`has-full-text:true`，逗号分隔可叠加。
  - `select=`：只取需要的字段（如 `DOI,title,author,issued,container-title`），减小响应。
  - `rows=`（每页，最大 1000）、`offset=`（仅前 10000 条内有效）。
  - 深翻页用 `cursor=*`，响应里取 `message.next-cursor` 带入下一次请求，可遍历全集。
- **Polite pool（强烈建议）**：在 `User-Agent` 或 query 里带 `mailto=you@example.com`，进入礼貌池，
  限速更稳。响应头 `X-Rate-Limit-Limit` 与 `X-Rate-Limit-Interval` 给出当前配额（典型 ~50 req/s）。
- 返回核心字段：`DOI, title, author(given/family), issued.date-parts, container-title, volume, issue, page, ISSN, type, is-referenced-by-count(被引数), reference(参考文献列表)`。

【链接】文档 https://www.crossref.org/documentation/retrieve-metadata/rest-api/ ；
仓库 https://github.com/CrossRef/rest-api-doc

【已知坑】`offset` 超过 10000 会失效，必须改用 cursor；title 字段是数组；机构作者无 given/family；预印本/会议覆盖不全。

---

## DOI.org 内容协商（Content Negotiation）

【是什么】对任意 DOI 发 HTTP 请求并通过 `Accept` 头协商，直接拿到 BibTeX / CSL JSON / RIS 等格式，
无需先查 API 再转换。Crossref 与 DataCite 已统一支持。是"一条命令把 DOI 变成 .bib"的最快路径。

【✅ 已验证 2026-06-06，测试 DOI 10.1038/s41597-023-02555-8，均 HTTP 200】
- `Accept: application/x-bibtex` → **200**（BibTeX）
- `Accept: application/vnd.citationstyles.csl+json` → **200**（CSL JSON）
- `Accept: application/x-research-info-systems` → **200**（RIS）
- `Accept: text/x-bibliography; style=apa` → **200**（已排版书目文本）
- 由 `scripts/doi_to_any.py` 自测覆盖（bibtex + csljson + 本地 GB/T 7714 排版）。

【可复用方法/真实端点/参数】
- 对 `https://doi.org/{doi}` 发请求，设 `Accept`：
  - BibTeX：`Accept: application/x-bibtex`
  - CSL JSON：`Accept: application/vnd.citationstyles.csl+json`
  - RIS：`Accept: application/x-research-info-systems`
  - DataCite XML：`Accept: application/vnd.datacite.datacite+xml`
- 进阶：`Accept: text/x-bibliography; style=apa; locale=en-US` 可直接返回**已排版的参考文献文本**
  （style 取 CSL 样式名，如 apa、ieee、chicago-author-date）。
- 示例：`curl -LH "Accept: application/x-bibtex" https://doi.org/10.1145/3292500.3330701`

【链接】https://crossref.org/documentation/retrieve-metadata/content-negotiation/ ；
DataCite https://datacite.readme.io/docs/what-is-the-best-way-to-make-a-content-negotiation-request-for-any-doi

【已知坑】`text/x-bibliography` 排版质量取决于 CSL 样式与元数据完整度；少数注册机构格式支持不全；务必跟随 30x 重定向（curl 加 `-L`）。

---

## Semantic Scholar Academic Graph API

【是什么】Allen AI 的学术图谱 API（~2 亿论文），强在**引用/被引关系**、tldr 摘要、影响力筛选，适合补"对比工作/SOTA baseline"。

【可复用方法/真实端点/参数】
- Base：`https://api.semanticscholar.org/graph/v1`
- 端点：
  - 相关性搜索 `/paper/search?query=...`（按相关度返回，带分页 `offset`/`limit`，limit≤100）。
  - 大批量检索 `/paper/search/bulk`（最多 1000 条/页，用返回的 `token` 翻页，支持 `year`、`fieldsOfStudy` 等过滤）。
  - 单篇 `/paper/{paper_id}`；批量 `POST /paper/batch`（body 传 ids 列表）。
  - 引用 `/paper/{id}/citations`、参考文献 `/paper/{id}/references`。
  - ID 形式多样：DOI:、ARXIV:、CorpusId: 等前缀。
- `fields=` 控制返回字段：`title,abstract,year,authors,citationCount,influentialCitationCount,externalIds,tldr,openAccessPdf,referenceCount`。
- 认证/限速：无 key 时为全体匿名用户**共享** 1000 req/s 池（高峰常 429，不保证）；申请免费 `x-api-key` 后走专属配额（introductory 约 1 RPS 起，更稳定可预期）。

【链接】教程 https://www.semanticscholar.org/product/api/tutorial ；API 文档 https://api.semanticscholar.org/api-docs/

【已知坑】共享池经常 429，生产务必申请 key；`abstract`/`tldr` 可能为 null；非英文与冷门会议覆盖弱于 Crossref。

---

## OpenAlex

【是什么】开放学术图谱（接替已关停的 Microsoft Academic Graph），覆盖 works/authors/sources/institutions/concepts/topics 全实体，适合大规模检索与计量。**2026 起接入需免费 API key**，key/限流/计费的唯一口径见 m01（light-literature-search）references「OpenAlex 接入真相源」节。

【✅ 已验证 2026-06-06；接入口径以 m01 真相源为准】
- `GET /works/https://doi.org/{doi}?mailto=...` → **HTTP 200**，返回 `id/doi/title/publication_year/cited_by_count/authorships`。
- `GET /works?filter=title.search:goat detection&per_page=1&mailto=...` → **HTTP 200**。
- 不存在的 DOI → **HTTP 404**。由 `scripts/verify_refs.py` 自测覆盖（与 Crossref 交叉核对标题/年份）。
- 注：上述 6-06 实测为匿名（仅 mailto）放行，属 key 强制过渡期现象；现行政策需免费 key，生产代码按"需 key"实现（口径见 m01 真相源节）。

【可复用方法/真实端点/参数】
- Base：`https://api.openalex.org`，实体端点 `/works`、`/authors`、`/sources`、`/institutions`、`/concepts`、`/topics`。
- 单条可直接用 DOI/OpenAlex ID：`/works/https://doi.org/10.xxxx` 或 `/works/W2741809807`。
- 查询：
  - `filter=`：强类型过滤，逗号 AND，竖线 OR。如 `filter=publication_year:2024,authorships.author.id:Axxx`、
    `filter=title.search:graph neural network`、`filter=cited_by_count:>100`、`filter=is_oa:true`。
  - `search=` 全文相关性检索；`select=` 限定返回字段；`sort=cited_by_count:desc`。
  - `group_by=` 做聚合统计（如按年、按机构计数），是做引用计量分析的利器。
- 分页：`per_page`（≤200）+ `page`（仅前 10000 条）；超过用游标 `cursor=*`，从响应 `meta.next_cursor` 续取。
- **Polite pool / 接入**：query 带 `mailto=you@example.com` 进入更快的池；OpenAlex 2026 起需免费 `api_key`。限流/计费具体口径见 m01 references「OpenAlex 接入真相源」节，本处不复写数字。
- 摘要以 `abstract_inverted_index`（倒排词位）存储，需自行重建为正文。
- 核心字段：`id, doi, title, publication_year, authorships, primary_location.source, cited_by_count, referenced_works, related_works, open_access`。

【链接】文档 https://docs.openalex.org/ ；端点 https://api.openalex.org/works

【已知坑】摘要是倒排索引非纯文本；机构/作者消歧偶有错配；`page` 模式同样限 10000，深翻必须 cursor。

---

## Unpaywall API

【是什么】按 DOI 查论文是否有**合法开放获取（OA）全文**及其链接，用于给参考文献补可访问的免费 PDF、判断来源开放性。覆盖 ~3000 万+ OA 记录。

【✅ 已验证 2026-06-06】
- `GET /v2/{doi}?email=<真实邮箱>` → **HTTP 200**，返回 `is_oa/oa_status/best_oa_location`。
- ⚠️ 实测坑：email 用 `example.com` 等占位域名 → **HTTP 422**（"Please use your own email address"）。必须用真实邮箱。

【可复用方法/真实端点/参数】
- Base：`https://api.unpaywall.org/v2`
- 端点：`/{doi}?email=you@example.com`（email 必填，否则 422）；批量搜索 `/search?query=...&email=...`。
- 关键返回字段：`is_oa`（是否 OA）、`oa_status`（gold/green/hybrid/bronze/closed）、
  `best_oa_location`（含 `url_for_pdf`、`host_type`、`version`）、`oa_locations`（全部 OA 位置）、
  `journal_is_oa`、`title`、`year`、`genre`。
- 限速：约 10 万次/天；超大规模用官方数据快照（data dump）而非逐条 API。

【链接】文档 https://unpaywall.org/products/api ；端点 https://api.unpaywall.org/v2

【已知坑】email 参数强制；只认 Crossref DOI（无 DOI 文献查不到）；`best_oa_location` 可能为 null（即闭源）；`version` 区分 publishedVersion / acceptedVersion，引用时注意是否为正式版。

【被 m01 消费】light-literature-search(m01) 的「单篇深读协议」用本节做"检索到→合法拿全文"的衔接：只取 OA 版本深读，闭源回退元数据+摘要级精读并声明（改本节端点须顾及 m01 深读节的指针）。

---

## OpenCitations API

【是什么】开放的**引用关系**数据库（DOI→DOI 引用对），独立于商业数据库，适合交叉验证被引/施引关系、做引文网络。CC0 开放。

【✅ 已验证 2026-06-06，两套 host 均可】
- `https://opencitations.net/index/api/v2/citation-count/doi:{doi}` → **HTTP 200**（返回 `[{"count":"5"}]`）。
- `https://api.opencitations.net/index/v2/citation-count/doi:{doi}` → **HTTP 200**（等价镜像 host）。
- `.../index/api/v2/references/doi:{doi}` → **HTTP 200**。

【可复用方法/真实端点/参数】
- Base：`https://api.opencitations.net`，主推 v2 索引：`https://api.opencitations.net/index/v2`。
- 标识符用 OMID 或带前缀的 DOI，如 `doi:10.1186/1756-8722-6-59`。
- 核心端点：
  - `/citations/{id}`：列出施引该文的所有引用。
  - `/references/{id}`：列出该文引用的所有文献。
  - `/citation-count/{id}`、`/reference-count/{id}`：计数。
  - 元数据走 OpenCitations Meta：`https://api.opencitations.net/meta/api/v1`。
- 认证：可选 `authorization` token（注册免费）提升限额；返回 JSON，字段含 `citing`、`cited`、`creation`、`timespan`、`oci`。

【链接】v2 索引 https://opencitations.net/index/api/v2 ；Meta https://opencitations.net/meta/api/v1 ；
论文 https://arxiv.org/abs/1904.06052

【已知坑】只覆盖**开放 DOI-DOI** 引用，绝对被引数低于 Scopus/WoS，不能当完整计数用；冷门/无 DOI 文献缺失；适合做"是否存在引用关系"的验证而非排名。

---

## Zotero（桌面 + Web API v3）

【是什么】开源参考文献管理器。本地库 + 云同步 + 浏览器 Connector 一键抓取，是个人/团队文献库的事实标准。

【可复用方法/真实端点/参数】
- Web API base：`https://api.zotero.org`，版本头 `Zotero-API-Version: 3`，鉴权 `Zotero-API-Key`。
- 路径：`/users/{userID}/items`、`/groups/{groupID}/items`、`.../collections`、`.../items/{itemKey}`。
- `format=` 取不同格式：`json`（默认，Zotero item JSON）、`bibtex`、`csljson`、`ris`、`atom`。
- 取**已排版引用/书目**：`include=citation,bib` 配 `style=`（CSL 名，如 `ieee`、`apa`）与 `locale=`。
- 分页 `start`/`limit`（默认 25，≤100），用响应头 `Total-Results` 与 `Link: rel="next"` 续取。
- 写操作带版本控制（`If-Unmodified-Since-Version`）防冲突。

【链接】https://www.zotero.org/support/dev/web_api/v3/start ；端点 https://api.zotero.org

【已知坑】写操作有版本并发校验，需处理 412；条目类型字段映射须按 itemTypes 端点；本地实时操作建议用下面的本地连接器/插件而非云 API。

---

## pyzotero

【是什么】Zotero Web API v3 的 Python 封装，把上面所有 REST 调用变成方法调用。

【可复用方法/真实端点/参数】
- 安装 `pip install pyzotero`；实例化 `from pyzotero import zotero; zot = zotero.Zotero(library_id, library_type, api_key)`，
  `library_type` 取 `'user'` 或 `'group'`。
- 读：`zot.items()`、`zot.top()`、`zot.collections()`、`zot.collection_items(key)`、`zot.item(key)`、
  `zot.everything(zot.items())`（自动翻完所有页）。
- 取格式：`zot.items(format='bibtex')`、`zot.items(content='csljson')`、
  或 `zot.items(content='bib', style='ieee')` 拿排版书目。
- 写：`zot.create_items([...])`、`zot.update_item(item)`、`zot.add_tags(item, 'tag')`、`zot.attachment_simple([...])`。
- 检索参数透传：`zot.items(q='keyword', itemType='journalArticle', limit=100, sort='date')`。

【链接】https://pyzotero.readthedocs.io/ ；仓库 https://github.com/urschrei/pyzotero

【已知坑】受同一限速；大库务必用 `everything()` 或手动 `follow()` 翻页；写操作同样要处理版本冲突。

---

## Better BibTeX（Zotero 插件）

【是什么】Zotero 的 BibTeX/BibLaTeX 神级导出插件，解决"引用键(citekey)稳定、可控、不重复"与"自动同步 .bib"两大痛点。LaTeX 工作流必备。

【可复用方法/真实端点/参数】
- **Citation key 公式**：在 设置→Better BibTeX→Citation Keys 用模板生成，如
  `auth.lower + year + shorttitle(3,3)`（典型 `zhang2024deep`）。冲突自动加后缀 a/b/c。
- **Pin key**：右键条目可"钉住"citekey，避免元数据变动后键名漂移（保证正文 \cite 不失效）。
- **Auto-export**：把某 collection 导出为 .bib 并勾选自动更新，库一改 .bib 自动重写，论文仓库始终最新。
- **本地集成接口**：Zotero 暴露 JSON-RPC 在 `http://127.0.0.1:23119/better-bibtex/`，可脚本化拉取条目、
  按 citekey 取 entry、触发导出——适合做 CI 里"校验正文每个 \cite 都在库中"。
- 导出格式：Better BibTeX / Better BibLaTeX / Better CSL JSON，可配字段保留与大小写保护。

【链接】https://retorque.re/zotero-better-bibtex/ ；citekey 文档 https://retorque.re/zotero-better-bibtex/citing/ ；
auto-export https://retorque.re/zotero-better-bibtex/exporting/auto/ ；仓库 https://github.com/retorquere/zotero-better-bibtex

【已知坑】未 pin 的 key 会随元数据变化；标题大小写保护（`{}`）与期刊样式可能冲突；JSON-RPC 仅本机、需 Zotero 开着。

---

## JabRef

【是什么】开源、跨平台、**以 .bib 为原生格式**的文献管理器，特别适合纯 LaTeX/BibTeX 工作流（不依赖 Zotero 生态）。

【可复用方法/真实端点/参数】
- 在线抓取（fetcher）：按 DOI、ISBN、arXiv、PubMed/Medline、Google Scholar 等直接拉元数据生成条目。
- **citation key 生成器**：可配 key 模式（如 `[auth][year]`），批量统一/重生成键名。
- **整洁度/完整性检查（Integrity check）**：检测缺失必填字段、重复条目、非法字符、未转义特殊符号、
  期刊缩写不一致——可作为投稿前 .bib 体检清单。
- Cleanup 操作：规范化页码范围、月份、大小写、从 PDF 提取元数据、批量加/改字段。
- 群组（groups）按关键词/作者自动归类；支持 BibTeX 与 BibLaTeX 两种模式。

【链接】https://docs.jabref.org/ ；社区 https://discourse.jabref.org/ ；仓库 https://github.com/JabRef/jabref

【已知坑】PDF 元数据抽取质量不稳（社区反复反馈）；改 citation key 时注意正文 \cite 同步；与 Zotero 生态需经 .bib/RIS 互导。

---

## CSL JSON（Citation Style Language JSON）

【是什么】CSL 引擎（citeproc-js / Pandoc / Zotero）使用的**中性元数据交换格式**。一份 CSL JSON + 一个 .csl 样式
即可渲染成任意期刊格式（APA/IEEE/GB-T 7714…），是"一处存储、多处排版"的中枢。

【可复用方法/真实端点/参数】
- 一条记录是一个 JSON 对象，关键字段：
  - `id`（引用键）、`type`（`article-journal`/`paper-conference`/`book`/`chapter`/`thesis` 等，决定排版模板）。
  - `title`、`container-title`（期刊/会议名）、`author`（数组，每项 `{family, given}` 或 `{literal}`）。
  - `issued`（日期，`{"date-parts": [[2024, 5, 1]]}`）、`volume`、`issue`、`page`、`DOI`、`URL`、`ISSN`、`publisher`。
- 与 BibTeX 字段映射要点：BibTeX `journal`→`container-title`，`year/month`→`issued.date-parts`，`booktitle`→会议 `container-title`。
- 排版：Pandoc `--citeproc --csl=ieee.csl --bibliography=refs.json`；DOI 内容协商可直接吐 CSL JSON（见上）。

【链接】规范 https://docs.citationstyles.org/en/stable/specification.html ；
字段 schema https://github.com/citation-style-language/schema ；样式库 https://github.com/citation-style-language/styles

【已知坑】`type` 选错会套错模板（如把会议论文标成 article-journal）；机构作者用 `literal` 而非 family/given；
date-parts 是嵌套数组易写错；中文姓名需注意 family/given 拆分。

---

## GB/T 7714（中文国标引用样式，基于 CSL）

【是什么】中国国标参考文献格式（GB/T 7714-2015），有顺序编码制与著者-出版年制两版，社区维护成 .csl 样式，
Zotero/Pandoc 直接可用。中文期刊投稿必备。

【可复用方法/真实端点/参数】
- 在 CSL 官方 styles 库搜 `china-national-standard-gb-t-7714`，区分 `-numeric`（顺序编码，最常用）与 `-author-date`（著者-出版年）。
- Zotero：从样式库一键安装该 .csl，导出/复制书目即按国标排版；Pandoc：`--csl=china-national-standard-gb-t-7714-2015-numeric.csl`。
- 关键差异点（核查时看）：作者≤3 全列、>3 取前 3 加"等/et al."；文献类型标识码 `[J]/[C]/[M]/[D]/[EB/OL]`；中英文混排标点与全角处理。

【链接】CSL 样式库（搜 gb-t-7714）https://github.com/citation-style-language/styles ；
样式检索 https://www.zotero.org/styles?q=gb

【已知坑】不同年份/不同高校变体众多，需按目标期刊确认具体 .csl；文献类型标识码、电子资源 `[EB/OL]` 与访问日期最易错；中文姓名大小写不可被英文样式规则误改。

---

## 中文文献核验兜底（无 DOI 的 CNKI/万方文献整条旁路）

> `doi_to_any.py` / `verify_refs.py` 均以 DOI 为入口。**知网（CNKI）、万方收录的大量中文文献无 DOI**，整条核验在 DOI 链路里缺失。本节是无 DOI 中文文献的**核验执行方**：把 m07（light-paper-drafting）`references/integrity_gate.md` 第 4 节「无 DOI 中文文献核对协议」比对出的题录，固化成字段齐全、可排版的规范 .bib 条目。
> **双向声明（避免单向挂载）**：m07 是写作时的**拦截方**（落笔即比对、核不到标"待核查"）；本节是**核验执行方**（题录→.bib 字段齐全性核对）。两方比对的字段集一致：m07 的题录三字段（题名 / 作者+单位 / 刊名+年卷期页），就是下面 .bib 必须齐全的字段。

### 1. CNKI 题录手工 → .bib 字段映射与逐条核对 checklist

知网导出格式（GB/T 7714 文本、EndNote、NoteExpress、Refworks 等）转 .bib 时的字段映射与齐全性核对：

| 知网题录字段 | BibTeX 字段 | 核对要点（最易错） |
|---|---|---|
| 题名 | `title` | 逐字一致，含副标题与全角标点；中文标题用 `{}` 包裹防英文样式误改大小写 |
| 作者（全部） | `author`，多作者用 ` and ` 分隔 | **不要在 .bib 里就截断成"等"**——`author` 存全部作者，"≥3 取前 3 加等"是**排版样式（gbt7714 .bst/.csl）自动做的事**，源数据存全。中文姓名整体作为一个 `{姓名}` 单元，勿被拆成 family/given |
| 刊名（全称） | `journal` | 用**全称**（如"农业工程学报"非"农业工程"）；缩写交样式处理 |
| 年 | `year` | 出版年（非网络首发年，除非引网络首发版） |
| 卷 | `volume` | 中文刊"卷"常等于年份序号，按题录页填 |
| 期 | `number` | 期号 |
| 起止页 | `pages` | 用**半角连接符区间** `235--242`（BibTeX 双连字符），样式渲染成"235-242" |
| 文献类型 | `@article`/`@inproceedings`/`@phdthesis`/`@book`/`@misc` + 见下类型标识 | entry type 选错→`[J]/[C]/[D]` 标识错 |
| 语言（关键） | `langid = {chinese}` | **必填**：缺 langid，gbt7714 样式下"等/et al."与 `[C]/[J]` 类型标识会出错（与 `doi_to_any.py` 对 CJK 自动注入 langid 同口径）。`langid` 按作者/标题是否含 CJK 判定 |

逐条核对 checklist（每条中文 .bib 条目过一遍）：

- [ ] entry type 与文献实体一致（期刊 `@article` / 会议 `@inproceedings` / 学位论文 `@phdthesis` / 专著 `@book` / 标准 `@misc`+type / 电子资源 `@online`/`@misc`）。
- [ ] `title` 逐字比对检索结果页，含全角标点；外层 `{}` 防大小写被改。
- [ ] `author` 存**全部**作者并用 ` and ` 分隔；中文姓名整体一个单元；不在源数据里截断"等"。
- [ ] `journal` 用刊名全称。
- [ ] `year/volume/number/pages` 与题录一致；`pages` 用 `--`。
- [ ] `langid = {chinese}` 已注入（中文条目缺它必错）。
- [ ] 与 m07 留痕台账对账：该条已有 `[核对日期] … 三字段一致` 记录（核不到的不进 .bib，留"待核查"）。

### 2. GB/T 7714-2015 中文条目核对速查表（≤15 行）

按 GB/T 7714-2015《信息与文献 参考文献著录规则》文后参考文献核对，写报告时逐项查：

| 项 | 规则 | 易错 |
|---|---|---|
| 文献类型标识码 | 期刊 `[J]`、会议论文集 `[C]`、学位论文 `[D]`、专著 `[M]`、标准 `[S]`、专利 `[P]`、报告 `[R]`、电子资源 `[EB/OL]` | entry type / langid 缺失致标识不出或出错 |
| 载体/电子资源标识 | 联机网络 `[文献类型/OL]`，如期刊网络版 `[J/OL]`、电子公告 `[EB/OL]` | 纸版误标 `/OL` 或反之 |
| 作者人数 | **≤3 人全列**；**>3 人取前 3 加"等"**（英文文献 "et al."） | 在源 .bib 里就截断（应存全，交样式截）；"等"前是否漏空格按样式 |
| 作者姓名 | 中文姓名全角、姓在前；不缩写名 | 被英文样式拆成 family/given 或缩写 |
| 题名后无类型缺失 | 题名后紧跟 `[文献类型标识]` | 漏标识码 |
| 出版年/卷期页 | 期刊：年, 卷(期): 起页-止页 | 卷期缺失、页码连接符用全角或单连字符 |
| 页码连接符 | 用半角连接号 | .bib 里 `--`，渲染后单连字符 |
| 电子资源引用日期 | `[EB/OL]` 须含 `[引用日期]` 与访问 URL | 漏引用日期或漏 URL |
| 顺序编码 vs 著者-出版年 | 两版制式不同（`-numeric` / `-author-date`），按目标刊选 .csl/.bst | 两制混用 |

> 速查依据：GB/T 7714-2015 标准条文 + CSL 社区 `china-national-standard-gb-t-7714-2015-numeric` 样式实现 + `zepinglee/gbt7714` 包文档（见上「GB/T 7714」与「GB/T 7714 BibTeX 样式」两节）。标准全文以国标原文为准；本表是核对速查，非标准替代。

### 3. 三条真实中文文献核对留痕（实查，2026-06-11）

从期刊官网实查、走题录三字段比对（题名 / 作者+单位 / 刊名+年卷期页，三者都对上才算同一篇）：

```
- [2026-06-11] 天然微藻水热炭理化特性及热解动力学研究 — 农业工程学报官网 http://www.tcsae.org/cn/article/doi/10.11975/j.issn.1002-6819.2019.14.030 — 三字段一致(刘慧慧,曲磊,陈应泉,等; 农业工程学报; 2019,35(14):235-242)
- [2026-06-11] 春小麦耐低氮种质资源的筛选与综合评价 — 中国农业科学官网 https://www.chinaagrisci.com/CN/10.3864/j.issn.0578-1752.2026.11.001 — 三字段一致(高亚峰,杨嘉宁,孙雪迪,等; 中国农业科学; 2026,59(11):2299-2313)
- [2026-06-11] 一次灌溉下耕作方式和氮肥用量对旱地小麦产量和品质的影响 — 作物学报官网 https://zwxb.chinacrops.org/CN/10.3724/SP.J.1006.2026.51088 — 三字段一致(胡川,赵凯男,黄修利,等; 作物学报; 2026,52(6):1830-1846)
```

对应第一条的规范 .bib（演示字段齐全 + langid + 类型标识）：

```bibtex
@article{liu2019weizao,
  title   = {{天然微藻水热炭理化特性及热解动力学研究}},
  author  = {刘慧慧 and 曲磊 and 陈应泉 and 张文楠 and 杨海平 and 王贤华 and 陈汉平},
  journal = {农业工程学报},
  year    = {2019},
  volume  = {35},
  number  = {14},
  pages   = {235--242},
  langid  = {chinese}
}
```

> 这三条恰有 DOI（中文刊近年也注册 DOI），但**核对走题录三字段而非 DOI 端点**，演示无 DOI 时同样动作。`author` 存全部 7 位作者，"前 3 加等"由 `gbt7714-numerical` 样式渲染时自动完成，源数据不截断。

---

## BibTeX 与 Biber/BibLaTeX

【是什么】LaTeX 的两套参考文献后端。传统 `bibtex`（配 natbib）vs 现代 `biber`（配 `biblatex` 宏包）。

【可复用方法/取舍】
- 经典：`\usepackage{natbib}` + `bibtex` 编译，.bst 控制样式，编译链 `pdflatex→bibtex→pdflatex×2`。
- 现代：`\usepackage[backend=biber, style=ieee]{biblatex}` + `\addbibresource{refs.bib}`，编译链 `pdflatex→biber→pdflatex×2`。
- Biber/biblatex 优势：原生 **UTF-8**（中文/变音字符不再乱码）、复杂排序/分组、`@online`等更多条目类型、样式用 LaTeX 写（无需 .bst）。
- 取舍：很多顶会模板（IEEEtran、ACM、Springer LNCS）仍硬性要求传统 bibtex + 指定 .bst，**投稿前先看模板要求再决定后端**，不要擅自换。

【链接】biblatex/biber 宏包 https://ctan.org/pkg/biblatex ；biber https://ctan.org/pkg/biber ；
对比讨论 https://tex.stackexchange.com/questions/25701/bibtex-vs-biber-and-biblatex-vs-natbib

【已知坑】两者命令/字段不完全兼容（biblatex 的 `date`、`journaltitle` vs bibtex 的 `year`、`journal`）；
换后端要清 `.aux/.bbl/.bcf` 重编；模板锁死后端时强行替换会被拒稿。

---

## EndNote / Mendeley（商业参考管理器）

【是什么】两大商业/半商业管理器。EndNote（Clarivate，付费，机构常用，深度对接 Web of Science）；
Mendeley（Elsevier，免费，对接 Scopus）。常出现在协作者已有的库里，需互导。

【可复用方法/取舍】
- 交换格式：两者都支持导出 **RIS**（`TY  - JOUR` 行式）与 BibTeX；EndNote 还有 XML（`.xml`/`.enl`）。
  跨工具迁移走 RIS 最稳，能保留大部分字段。
- 都提供 "Cite While You Write" Word 插件做正文插引与即时改样式。
- 取舍：与 Zotero/JabRef 协作时，统一以 .bib 或 RIS 为中转；EndNote XML 字段最全但只 EndNote 系认。
- **API 现状**【部分未能核实】：Mendeley 曾有公开开发者 REST API，近年 Elsevier 多次调整且功能收缩；
  EndNote 无开放公共 REST API（以桌面/Word 插件为主）。具体现存端点请以官方为准，本笔记不臆造端点。

【链接】EndNote https://support.clarivate.com/Endnote/ ；Mendeley https://www.mendeley.com/

【已知坑】RIS 字段映射各家略有差异（尤其会议论文、类型标签）；导入后务必抽查作者/年份/页码；
EndNote XML 与开源工具兼容性差；不要假设 Mendeley API 仍提供历史端点，迁移前先验证。

---

## 速查：审查/生成任务该用哪个

| 需求 | 首选 | 备选 |
|---|---|---|
| 验证 DOI/标题/作者/年份真实 | Crossref `/works` | OpenAlex、Semantic Scholar |
| DOI→.bib / →CSL JSON / →排版文本 | DOI 内容协商 | Crossref、Zotero API |
| 找对比工作/SOTA、看被引影响力 | Semantic Scholar | OpenAlex（group_by 计量） |
| 验证"A 是否引用了 B" | OpenCitations | Semantic Scholar citations |
| 补开放获取免费 PDF / 判来源开放性 | Unpaywall | OpenAlex `is_oa` |
| 管理个人/团队文献库 | Zotero(+pyzotero) | JabRef（纯 .bib） |
| 稳定 citekey + 自动同步 .bib | Better BibTeX | JabRef key 生成器 |
| 多格式一处存多处排版 | CSL JSON + .csl | — |
| 中文国标格式 | GB/T 7714 .csl | — |
| LaTeX 后端选择 | 看模板要求选 biber 或 bibtex | — |
