# Phase3 重核：Phase1 标"未能核实"的 API 字段

> 探测方式：本机 Bash `curl` 直连 + 官方文档源（GitHub raw / 文档站）实测。
> 探测日期：2026-06-06。所有 HTTP 码与返回结构均为真实抓取；DNS 受限或付费墙不可得者如实标注。
> 诚实声明：可核查字段全部来自真实 curl；拿不到的不臆造。

---

## 1. PatentsView 新版 PatentSearch API（search.patentsview.org）

回填到：`light-ip-application`、`light-literature-search`（专利检索）、`light-tool-selection`

**本机直连结果（受限）**
- `curl https://search.patentsview.org/...` → `HTTP 000`，`curl: (6) Could not resolve host`。
  本机 DNS 无法解析 `search.patentsview.org`（DoH 1.1.1.1 / dns.google 也被网络策略拦截）。**无法实测其在线行为**。
- 旧域 `https://api.patentsview.org/patents/query?...` → `HTTP 301`，`Location: https://data.uspto.gov/support/transition-guide/patentsview`。**旧版 API 已迁移/下线**。

**官方文档实测（GitHub raw 可直连，权威源）**
源：`https://raw.githubusercontent.com/PatentsView/PatentSearch-API/main/docs/docs/Search%20API/SearchAPIReference.md`（仓库 `PatentsView/PatentSearch-API`，default branch=main，HTTP 200）

确认字段（逐字摘自官方文档）：
- **需要 API Key（是）**：`The PatentSearch API uses API Keys to authenticate requests` / `All API requests must include the header X-Api-Key: {your_key}`。
- **请求头**：`X-Api-Key: {your_key}`（非 query 参数）。
- **限流**：`Each API Key is allowed **45 requests/minute**. If you exceed this limit, your API requests will fail.`
- **超限返回**：`429 Too many requests`，并通过 `Retry-After` 响应头给出等待秒数。
- **错误诊断头**：400 看 `X-Status-Reason` / `X-Status-Reason-Code`；403 检查 `X-Api-Key` 是否正确。
- **Base URL / 端点**：`https://search.patentsview.org/api/v1/patent/?q={...}`；Swagger：`https://search.patentsview.org/swagger-ui/`。
- **请求结构**：4 部分 = API Key + Endpoint + Method(GET/POST) + Parameters；`q` 参数必填。
- **申请 Key（重要变化）**：`We have temporarily suspended new API Key grants.` —— **官方已临时暂停新 Key 发放**；每用户限 1 个 Key，Key 当前不过期。

> 结论：search.patentsview.org **确实需要 `X-Api-Key` 头**，限流 **45 请求/分钟**，旧 api.patentsview.org 已 301 迁移。本机无法解析该域名，故"在线 HTTP 行为"未实测，字段依据官方文档源核实。

---

## 2. The Lens API（api.lens.org）

回填到：`light-ip-application`、`light-literature-search`

**本机直连实测**
- `GET https://api.lens.org/scholarly/search`（无 token）→ `HTTP 401`。
- `POST https://api.lens.org/scholarly/search` + `{"query":"test"}`（无 token）→ `HTTP 401`，返回体：
  `{"reference":"...","message":"Missing/Incorrect Authorization Header","code":401}`。

**官方文档实测**（`https://docs.api.lens.org/getting-started.html`，HTTP 200，可直连）
- **认证（必需 token）**：`Lens uses token-based API authentication`，需先 `request access` 获批，再在 profile 创建 Access Token。
  - POST 请求：请求头 `Authorization: Bearer your-access-token`。
  - GET 请求：query 参数 `?token=your-access-token`。
- **端点**：
  - 学术：`POST/GET https://api.lens.org/scholarly/search`、`GET https://api.lens.org/scholarly/{lens_id}`、`GET https://api.lens.org/schema/scholarly`。
  - 专利：`POST/GET https://api.lens.org/patent/search`、`GET https://api.lens.org/patent/{lens_id}`、`GET https://api.lens.org/schema/patent`。
- **限流（官方 Rate Limiting 段，逐字）**：超限返回 `429 - Too Many Requests`。限流信息通过响应头给出：
  - `x-rate-limit-remaining-request-per-minute`（每分钟剩余请求数）
  - `x-rate-limit-retry-after-seconds` / `x-rate-limit-retry-after-millis`（下次可请求等待时长）
  - `x-rate-limit-reset-date`（重置时间）
  - `x-rate-limit-remaining-request-per-month`（到重置日剩余月度调用数）
  - `x-rate-limit-remaining-record-per-month`（剩余可取记录数）
  - 具体数值取决于个人 access plan（文档未给统一固定数字，按订阅计划而定）。

> 结论：The Lens 需申请并通过审批才能拿 token，**非匿名可用**；限流为"每分钟+每月"双层，数值随计划而定，靠响应头自适应。

---

## 3. WIPO PATENTSCOPE

回填到：`light-ip-application`、`light-literature-search`

**本机直连实测**
- `https://patentscope.wipo.int/search/en/search.jsf` → `HTTP 302`（重定向到会话页，JSF 应用，非 REST API）。
- `https://patentscope.wipo.int/search/en/result.jsf` → `HTTP 302`。
- `https://www.wipo.int/patentscope/en/data/products.html` → `HTTP 302`。

> 结论：PATENTSCOPE 网页检索是 JSF 会话式界面，**无面向公众的免费开放 REST 检索 API**（curl 仅得 302 会话跳转）。WIPO 的批量数据以"产品/下载"形式提供（如  download/FTP 数据集），需另行申请，**无公开免费即时查询 API**。标注：**无公开免费即时检索接口**；如需机读数据走 WIPO 官方数据产品下载渠道。

---

## 4. Zotero Web API（api.zotero.org，v3）

回填到：`light-citation`、`light-memory-pm`、`light-tool-selection`

**本机直连实测**
- `GET https://api.zotero.org/groups/1/items?limit=1` → `HTTP 200`，返回 `[]`；响应头 `Zotero-API-Version: 3`。**公共/公开库匿名可读**。

**官方文档实测**（`https://www.zotero.org/support/dev/web_api/v3/basics`，HTTP 200）
- **版本**：当前默认且推荐 v3；生产应通过 `Zotero-API-Version: 3` 头或 `v=3` 参数显式指定。
- **认证**：私有库用 API Key（`Authorization: Bearer` 或 key 参数）；当前 OAuth 1.0a。
- **限流（官方 Rate Limiting 段，逐字要点）**：客户端需处理两类：
  - **Backoff**：服务器过载时响应可含 `Backoff: <seconds>` 头（任何响应包括成功响应都可能带），收到后应完成必要请求后暂停指定秒数。
  - **429 Too Many Requests**：请求过多或并发过高时返回，可能带 `Retry-After: <seconds>` 头；收到后至少等待该秒数，否则可能被更严格限流或临时封禁。无 Retry-After 时应做指数退避。
  - **并发上限建议**：`make no more than 4 concurrent requests`（不超过 4 个并发请求）。
  - `Retry-After` 也可能随 `503 Service Unavailable`（维护时）一并返回。
  - 官方**未公布固定每分钟数字**，采用动态 Backoff/429 机制。
- 其他限制：单次 item 请求最多 50 个 key；`format=bib` 最多 150 items。

> 结论：Zotero 公开库匿名可读（实测 200）；限流为**动态 Backoff + 429/Retry-After**机制而非固定 RPM，建议并发 ≤4。

---

## 5. Mendeley / Elsevier 现行端点

回填到：`light-citation`、`light-literature-search`、`light-tool-selection`

**本机直连实测**
- Mendeley：`GET https://api.mendeley.com/documents`（无 token）→ `HTTP 401`，响应头 `WWW-Authenticate: Bearer realm="mendeley" error="invalid_token"`。**端点存活，需 OAuth2 Bearer token**。
- Elsevier Scopus：`GET https://api.elsevier.com/content/search/scopus?query=test`（无 key）→ `HTTP 401`，响应头：
  - `X-ELS-Status: AUTHENTICATION_ERROR - Invalid API Key`
  - `X-ELS-ReqId` / `X-ELS-TransId` / `X-ELS-ResourceVersion: default`
  - `tdm-policy: https://www.elsevier.com/tdm/tdmrep-policy.json`
  **端点存活，需 `X-ELS-APIKey`（Elsevier API Key），并通常需机构 token / IP 授权**。

> 结论：
> - **Mendeley** 现行 API base `https://api.mendeley.com`，OAuth2 Bearer 认证（`Authorization: Bearer`）。匿名 401。
> - **Elsevier**（Scopus/ScienceDirect）现行 API base `https://api.elsevier.com`，需 API Key（`X-ELS-APIKey` 头），多数全文/检索端点还需机构订阅 + InstToken/IP 授权。匿名 401。
> - 二者均**非匿名可用**，需注册凭证；本机已实测端点存活与认证方式。

---

## 6. LanguageTool（api.languagetool.org/v2/check）真实限流

回填到：`light-paper-polishing`、`light-citation`、`light-tool-selection`

**本机直连实测**
- `POST https://api.languagetool.org/v2/check` + `text=This are a test.` + `language=en-US` → `HTTP 200`。**公共匿名可用**，返回完整 JSON：
  - `software.name=LanguageTool`，`software.version=6.9-SNAPSHOT`，`premium:true`（带 `premiumHint`）。
  - `language.detectedLanguage`（含 confidence、source=ngram）。
  - `matches[]`：每条含 `message`、`shortMessage`、`replacements[]`、`offset`、`length`、`context`、`sentence`、`rule` 等。
  - 示例命中："This are" → 建议改 "These"。
- 响应头：`access-control-allow-origin: *`（无显式 rate-limit 头返回）。

**官方文档实测**（`https://dev.languagetool.org/public-http-api`，HTTP 200，逐字）
- 公共端点限流：
  - **20 requests per IP per minute**（峰值，不可持续打满，否则会被封）。
  - **75 KB text per IP per minute**。
  - 仅接受 **POST**（不要用 GET）。
  - 不要发自动化批量请求；大量使用应自建实例或购买 Plus 计划。
  - 免费服务，无性能/可用性保证，限制随时可能变更。
  - 不要使用首页 HTML 里发现的其它内部端点，官方公共端点即 `api.languagetool.org/v2`。

> 结论：LanguageTool 公共 API **匿名可用**（实测 200），真实限流 **20 req/IP/min 且 75KB 文本/IP/min**，仅 POST。原 Phase1"未核实"现已坐实。

---

## 7. DeepL 参数（/v2/translate）

回填到：`light-paper-polishing`、`light-citation`、`light-tool-selection`

**本机直连实测**
- `POST https://api-free.deepl.com/v2/translate` + `text=Hello&target_lang=DE`（无 key）→ `HTTP 403`，返回体：
  `{"message":"Missing Authorization header, expected 'Authorization: DeepL-Auth-Key <API key>'..."}`。**端点存活，需鉴权**。

**官方文档实测**（`https://developers.deepl.com/docs/getting-started/auth` & `/api-reference/translate`，HTTP 200）
- **双端点（关键）**：
  - Free API → `https://api-free.deepl.com`
  - Pro API → `https://api.deepl.com`
  - Free key 以后缀 `:fx` 标识（如 `...e42a0:fx`），用错 base 会失败。
- **认证**：请求头 `Authorization: DeepL-Auth-Key [yourAuthKey]`。
- **请求头限制**：所有请求 header 大小上限 16 KiB。
- **/v2/translate 参数**（文档确认）：`text`（必填，可多次）、`target_lang`（必填）、`source_lang`、`formality`、`tag_handling`、`split_sentences`、`preserve_formatting`、`glossary_id` 等。

> 结论：DeepL 现行 base 区分 Free(`api-free.deepl.com`)/Pro(`api.deepl.com`)，鉴权头 `Authorization: DeepL-Auth-Key`，核心参数 `text`+`target_lang` 必填。匿名 403，需 key。

---

## 8. Semantic Scholar 限流（探 429）

回填到：`light-literature-search`、`light-citation`、`light-venue-matching`、`light-tool-selection`

**本机直连实测**
- `GET https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/nature12373?fields=title,year`（无 key）→ `HTTP 200`，返回真实 JSON：
  `{"paperId":"a5de30adc5c22bc86e8cfabe7fbd07c052d196a8","title":"Nanometer scale thermometry in a living cell","year":2013}`。
- **压测探 429**：连续 8 次顺序请求 → 全部 200；20 路并发请求 → 全部 200。**本次未触发 429**（共享池在该时段未限到本机）。

**官方文档实测**（`https://www.semanticscholar.org/product/api`，HTTP 200，逐字）
- **多数端点匿名可用**，但 `rate-limited to 1000 requests per second shared among all unauthenticated users`（**所有匿名用户共享 1000 req/s**），高峰期可能进一步节流。
- 部分端点需 API Key；持 key 用户限流更高，**但 introductory API key 限流为 1 RPS（所有端点）**。
- 超限返回 **`429 Too Many Requests`**（tutorial 页确认），应放慢请求。

> 结论：S2 匿名可用（实测 200）；官方限流＝**全体匿名共享 1000 req/s**，超限 429。本机压测未触发 429（共享池当时空闲），属预期——匿名额度是全局共享而非每 IP 固定，无法稳定复现 429，符合官方描述。

---

## 9. 确无公开免费接口者（如实标注）

回填到：`light-citation`、`light-venue-matching`、`light-tool-selection`

- **EndNote**：无公开 REST API。EndNote（Clarivate）为桌面/同步产品，**无面向开发者的公开免费 REST 接口**。集成走文件格式（.enw / RIS / BibTeX）或 EndNote Click，**不存在可 curl 的查询端点**。标注：**无公开免费接口**。
- **JCR（Journal Citation Reports，精确 Impact Factor）**：付费墙。Clarivate JCR 需机构订阅，**无免费 API**；本环境 curl 付费源 301/403。
  - 替代（可核查、禁编造 IF）：用 **OpenAlex `summary_stats.2yr_mean_citedness`**（≈2年期被引均值，IF 的可核查近似）与 **`h_index`**。例：`curl "https://api.openalex.org/sources/S<id>?mailto=light@example.com"` 读 `summary_stats`。
  - 国内可查渠道：LetPub / easyScholar（本环境可直连），用于分区/影响因子参考，但**精确 Clarivate IF 仍标"免费源不可得（付费墙）"**。
- **Scimago SJR**：付费/受限源，curl 不可稳定获取。同样以 OpenAlex `2yr_mean_citedness` / `h_index` 作可核查替代，**禁造 SJR 数值**。

---

## 附：本机环境对各域可达性速查（实测 HTTP 码，2026-06-06）

| 服务 | 实测端点 | HTTP | 匿名可用 | 备注 |
|---|---|---|---|---|
| Semantic Scholar | graph/v1/paper | 200 | 是 | 共享 1000 req/s，超限 429 |
| LanguageTool | /v2/check | 200 | 是 | 20 req/IP/min + 75KB/min，仅 POST |
| Zotero | groups/1/items | 200 | 公开库是 | Backoff/429，并发≤4 |
| The Lens | scholarly/search | 401 | 否 | 需审批 token，Bearer |
| Mendeley | /documents | 401 | 否 | OAuth2 Bearer |
| Elsevier Scopus | content/search/scopus | 401 | 否 | X-ELS-APIKey + 机构授权 |
| DeepL Free | api-free.deepl.com/v2/translate | 403 | 否 | DeepL-Auth-Key 头 |
| PatentsView 旧 | api.patentsview.org/patents/query | 301 | — | 已迁移 data.uspto.gov |
| PatentsView 新 | search.patentsview.org | 000(DNS) | 否 | 需 X-Api-Key，45/min（文档源核实，新Key暂停发放） |
| WIPO PATENTSCOPE | search.jsf | 302 | — | 无公开免费 REST API |
| EndNote | — | — | — | 无公开免费接口 |
| JCR / SJR | — | 301/403 | — | 付费墙，免费源不可得；用 OpenAlex 替代 |

**数据来源链接**
- PatentsView 官方文档源：https://github.com/PatentsView/PatentSearch-API （docs/docs/Search API/SearchAPIReference.md，main 分支）
- 旧 API 迁移：https://data.uspto.gov/support/transition-guide/patentsview
- The Lens：https://docs.api.lens.org/getting-started.html
- Zotero：https://www.zotero.org/support/dev/web_api/v3/basics
- LanguageTool：https://dev.languagetool.org/public-http-api
- DeepL：https://developers.deepl.com/docs/getting-started/auth
- Semantic Scholar：https://www.semanticscholar.org/product/api
- OpenAlex（IF/SJR 替代）：https://api.openalex.org/sources/{id}

