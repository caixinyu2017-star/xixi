# db08 — 软著 / 专利 / 申报 真实资源与模板库（resources_real.md）

> 服务 m15(软著专利)、m17(竞赛申报)。本文件只收录**可核实的官方入口**与**结构性要点**。
> ⚠ 合规底线（联动 a10 / CONVENTIONS）：
> - 软著、专利、申报材料**不得虚构、夸大或编造数据**；软件/技术方案须真实存在。
> - **专利权利要求书与说明书最终文本必须由专业专利代理师（机构）或法律人员审核**（`final_review_needed: true`），本库仅提供结构与写作要点，不替代代理。
> - 加急时效、具体官费/代理费随政策与机构浮动，凡未当场核实者一律标【待核查】，不臆造数值。
> - 核实方式：下列 URL 已用 `curl` 探测可达性（标注 HTTP 状态）或经 WebSearch 命中官方页；探测日期 2026-06-06。

---

## 1. 真实专利检索入口

> **端点/认证/限流的单一真相源 = [light-ip-application/references.md](../../skills/light-ip-application/references.md)（已 curl 实测 OPS OAuth/Lens/PatentsView 细节）；程序化在先技术检索走 [patent_search.py](../../skills/light-ip-application/scripts/patent_search.py)（已实时化）。** 本表只留平台指针 + 适用 + 核实状态(last_checked=2026-06-06),不重复维护 API 细节(消除双源)。

| 平台 | 入口 URL(source_pointer) | 适用 | 有无 API | 核实状态(last_checked 2026-06-06) |
|---|---|---|---|---|
| Google Patents | https://patents.google.com | 全球专利+非专利文献,跨语种,免费初检 | 无公开 REST(批量走 BigQuery 公开数据集) | curl 000(地区网络),WebSearch 确认有效 |
| CNIPA 公布公告 | http://epub.cnipa.gov.cn | 中国专利公布/公告原始文本 | 无开放 API | 主站 cnipa.gov.cn HTTP 200 |
| CNIPA 检索及分析系统 | https://pss-system.cnipa.gov.cn | 官方权威检索(需登录),法律状态/同族/引证 | 无开放 API | 主站可达,子系统需登录【待核查】 |
| EPO Espacenet | https://worldwide.espacenet.com | 1.4亿+全球文献,同族(INPADOC)/法律状态/CPC | **有(OPS,OAuth2,详见 references.md)** | curl 403(反爬,站点真实) |
| WIPO PATENTSCOPE | https://patentscope.wipo.int | PCT 国际申请,多语种(CLIR) | 有限 Web service【细节待核查】 | curl HTTP 200 |
| USPTO Patent Public Search | https://ppubs.uspto.gov/pubwebapp/ | 美国专利与公开申请官方检索 | 页面本身无开放 API | curl 000(地区网络),WebSearch 确认 |
| USPTO PatentsView | https://search.patentsview.org | 美国专利结构化数据/引证分析 | **有(PatentSearch API,需 X-Api-Key;旧 legacy 2025-02 停用,详见 references.md)** | WebSearch 命中官方 |
| The Lens | https://www.lens.org | 专利+学术联合检索 | 有(token,收费/机构;免费额度待核查,详见 references.md) | curl HTTP 200 |

要点：免费初检用 Google Patents + CNIPA 公布公告；同族/法律状态用 Espacenet(OPS 最全);批量结构化分析用 PatentsView(美国)或 OPS(全球);PCT 用 PATENTSCOPE。检索是新颖性/创造性自评前置,**不替代代理师专业检索与可专利性判断**。

---

## 2. 软件著作权申请真实要点

**登记机构**：中国版权保护中心（CPCC）。官网 http://www.ccopyright.com.cn （curl 实测 301→ **https://www.ccopyright.com.cn HTTP 可达**）。计算机软件著作权登记是其法定职能之一；线上入口为「中国版权保护中心 / 软件著作权登记」业务系统（需注册实名账号）。

**办理流程（典型线上）**：
1. 注册账号、实名认证（个人/单位）。
2. 在线填报软件基本信息（全称+简称+版本号），生成申请表。
3. 上传材料（源代码鉴别材料、文档鉴别材料、申请表、权属/身份证明）。
4. 形式审查 → 补正（如有）→ 受理 → 发放《计算机软件著作权登记证书》。
5. 普通办理法定审查周期较长，**加急办理需另付加急费、按工作日分档**——具体费用与时效【待核查：以 CPCC 当期收费/服务公告为准,source_pointer: ccopyright.com.cn 收费公告;不缓存数值】。

**源代码提交规则（鉴别材料）** — `rule_type:行政规则 volatility:low last_checked:2026-06-06 source_pointer:CPCC《软件著作权登记申请指南》`。**本节是 60 页规则的单一真相源**(SKILL/extended_cards/copyright_source_prep.py 指针引用此处,不各写一遍):
- 提交**源程序前、后各连续 30 页，共 60 页**；不足 60 页者全部提交。
- **每页不少于 50 行**（最后一页除外），打印代码，**页眉含软件名称及版本号、页码连续**。
- 代码须**连续、真实、可与软件功能对应**；不得含与本软件无关的代码、不得插入大段空行充数、不得含密钥/口令等敏感信息。
- 说明：上述为业内长期通行的 CPCC 鉴别材料规则,变动极慢(全学科任何软件通用);**最新页数/行数口径以 CPCC 官网当期《软件著作权登记申请指南》为准【提交前核查】**。来源参考：[Wikipedia: Software copyright in China](https://en.wikipedia.org/wiki/Software_copyright_in_China) + CPCC 官网指南。

**材料清单（checklist）**：
- □ 软件全称 + 简称 + 版本号（三者一致、与代码页眉一致）
- □ 源代码鉴别材料：前后各 30 页 / 共 60 页，每页≥50 行，带页眉页码
- □ 文档鉴别材料：操作说明书或设计说明书（前后各 30 页规则同上），**配关键界面截图**，截图与功能描述一致
- □ 软件著作权登记申请表（系统生成）
- □ 权属证明：单位营业执照 / 个人身份证明；合作或委托开发需权属约定
- □ 开发完成日期、首次发表日期（如已发表）
- □ 功能模块说明完整，与源代码、截图三者对应

**常见错误**：代码页不连续、版本号前后不一致、页眉缺失、含敏感信息、功能说明与代码/截图不符、用自动生成代码或第三方代码充页。

**法律风险**：软件须真实存在；登记采形式审查，**材料不实不产生确权效力且可能被撤销**。`final_review_needed: false`（建议自查，高校可咨询科技处/知识产权办）。

---

## 3. 专利权利要求书 / 说明书结构模板要点

> ⚠ **本节为结构与写作要点，非可直接提交文本。发明/实用新型的权利要求书与说明书最终稿务必经专利代理师审核（`final_review_needed: true`）。**

**说明书结构（发明/实用新型，CNIPA 规范顺序）**：
1. 技术领域 — 一句话界定所属技术领域。
2. 背景技术 — 客观介绍现有技术及其缺陷（即"要解决的问题"由来），可引用对比文献，**不得贬损、不得编造**。
3. 发明内容 — ① 要解决的技术问题；② 技术方案（与权利要求对应）；③ 有益效果（可量化更佳，需真实）。
4. 附图说明 — 逐图说明。
5. 具体实施方式 — **至少一个完整实施例**，充分公开到本领域技术人员可实现的程度；可含多个实施例/优选方案。

**权利要求书结构要点**：
- **独立权利要求**：前序部分（共有技术特征）+ 特征部分（区别技术特征），界定**最大且稳妥的保护范围**。
- **从属权利要求**：引用在先权利要求，**逐层附加技术特征**，作为回退保护层级。
- 每项权利要求须**得到说明书支持**、清楚、简要；术语前后一致；避免功能性限定过宽或保护范围过窄。
- 一份申请通常 1 个独立权利要求 + 若干从属权利要求（主题单一/单一性要求）。

**常见驳回 / 缺陷理由**：
- **新颖性不足**（已被现有技术公开）— 检索不充分所致。
- **创造性不足**（相对现有技术无突出实质性特点/显著进步）— 最常见实质驳回。
- **缺乏实用性**。
- **公开不充分**（说明书无法使本领域技术人员实现）。
- **权利要求得不到说明书支持 / 不清楚 / 不简要**。
- **缺乏单一性**（一案含多个不具备相同/相应特定技术特征的发明）。
- **客体不适格**（如智力活动规则、单纯算法/科学发现，需结合技术手段、技术问题、技术效果"三要素"撰写软件类专利）。
- 修改超范围（超出原始申请文件记载的内容）。

---

## 4. 竞赛 / 项目申报真实资源

| 赛事 | 官方入口 | 说明 | 核实状态 |
|---|---|---|---|
| 中国国际大学生创新大赛（原"互联网+"） | https://cy.ncss.cn （英文 https://cy.ncss.cn/en/ ） | 教育部主办，全国大学生创新创业最高规格赛事；报名、赛道、评审在此平台 | curl **HTTP 200 实测可达**；WebSearch 命中官方 |
| "挑战杯"全国大学生系列科技学术竞赛 | https://www.tiaozhanbei.net | 含"挑战杯"课外学术科技作品竞赛 与 "挑战杯"中国大学生创业计划竞赛（两年各一届，交替） | curl **HTTP 200 实测可达** |
| 大学生创新创业训练计划（国创计划 / 大创） | 全国大学生创新创业训练计划平台（教育部，依托各高校教务处/创新创业学院组织申报） | 国家级/省级/校级三级；**报名入口通常由本校教务系统下发，全国统一平台入口随年度变动【待核查当年官方链接,volatility:high 不缓存逐年值】** | 平台入口未当场 curl 确认，标【待核查】 |
| 全国大学生数学建模竞赛（CUMCM） | http://www.mcm.edu.cn （中国工业与应用数学学会 CSIAM 主办） | 国内最大数模赛事，9 月开赛 | 入口经 WebSearch/常识确认，未当场 curl【建议核查当年通知】 |
| 美国大学生数学建模竞赛 MCM/ICM（美赛） | https://www.comap.com/contests/mcm-icm （主办方 COMAP；竞赛站 https://www.contest.comap.org ） | 国际数模赛，2 月开赛，COMAP 组织 | WebSearch 命中官方 comap.com |

申报书通用要点（实体细分卡见 [material_extended_cards.md](material_extended_cards.md)，预算与结构骨架见 [budget_template.md](budget_template.md) / [case_skeletons.md](case_skeletons.md)）：
- 必备模块：项目摘要 / 背景意义 / 研究内容 / 技术路线 / 创新点 / 可行性 / 研究基础 / 预期成果 / 进度 / 经费预算 / 团队分工。
- **创业类的市场规模、财务、用户数等数据必须可核查来源，禁止臆造**；学术类创新点应可量化、与技术路线一一对应。
- 模板以**各校/各赛事当年官方通知**为准，本库不缓存受版权的官方模板原文，仅总结结构。

---

## 来源（WebSearch / curl 核实）

- [China International College Students' Innovation Competition 2025](https://cy.ncss.cn/en/)
- [挑战杯 tiaozhanbei.net](https://www.tiaozhanbei.net/)（curl HTTP 200）
- [CNIPA 国家知识产权局](https://www.cnipa.gov.cn/)（curl HTTP 200）
- [中国版权保护中心 ccopyright.com.cn](https://www.ccopyright.com.cn/)（curl 301→可达）
- [PatentsView API Purpose](https://patentsview.org/apis/purpose) / [Support for Legacy API to End in February 2025](https://patentsview.org/data-in-action/support-legacy-api-end-february-2025-switch-patentsearch-api-now) / [Patents Endpoint](https://patentsview.org/apis/api-endpoints/patents)
- [USPTO Patent Public Search](https://www.uspto.gov/patents/search/patent-public-search) / [PatentsView (USPTO)](https://www.uspto.gov/ip-policy/economic-research/patentsview)
- [The Lens](https://www.lens.org/) / [Lens Patent Search & Analysis](https://about.lens.org/patent-search-analysis/)
- [EPO Web services (OPS)](https://www.epo.org/en/searching-for-patents/data/web-services)
- [WIPO PATENTSCOPE (WIPO Open Source Patent Analytics Manual)](https://wipo-analytics.github.io/manual/patentscope-1.html)
- [COMAP MCM/ICM](https://www.comap.com/contests/mcm-icm)
- [Software copyright in China — Wikipedia](https://en.wikipedia.org/wiki/Software_copyright_in_China)

> 标【待核查】项：软著加急具体费用与时效、CPCC 当期源代码页数/行数最新口径、大创全国统一平台当年入口、PATENTSCOPE/Lens API 免费额度与端点细节、CUMCM 当年报名链接。使用前请以对应官方当期公告为准。
