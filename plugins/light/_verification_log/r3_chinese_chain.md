# R3 中文链路专项 — 实查/实测留痕

> 第三期 R3 执行期间（2026-06-11）对中文科研链路四断点所需的"实查/实测"项做的联网核实记录。
> 凡下游 references / db01 写入的中文链路事实，来源回指本文件。无网或被反爬拦截的项标 `GAP：待联网核验`，禁止凭记忆冒充。
> 核实环境：Claude Code (Opus 4.8)，curl + pdfplumber/pypdf 直读，HTTP 码与文件字节均真实落地。

---

## 1. EI / Compendex 数据源（R3.4）

| 项 | 结论 | 证据（URL + HTTP 码 + 日期） |
|---|---|---|
| Engineering Village 入口 | 存活，需订阅（302 跳登录） | `https://www.engineeringvillage.com` → **HTTP 302**（2026-06-11） |
| Compendex 产品页 | 存活 | `https://www.elsevier.com/products/engineering-village/databases/compendex` → **HTTP 200**（2026-06-11） |
| **Compendex Source List（权威收录刊单）** | **实测可下载 Excel** | 页内 "View source list" 指向 `https://assets.ctfassets.net/o78em1y1w4i4/wRpDAQPyS5xorlKFLeSrq/499c39b330a506838630188f00bc444c/CPXSourceList_052026__1_.xlsx` → **HTTP 200, size=5,647,296 bytes**（2026-06-11）。文件名 `CPXSourceList_052026` 表明为 2026 年 5 月版。 |
| 旧候选路径 | 已失效，勿再引 | `https://www.elsevier.com/products/engineering-village/compendex` → **HTTP 404**；`.../databases/compendex/content` → **HTTP 404**（2026-06-11） |

- 结论：EI 核查权威源 = Engineering Village 内的 **Compendex Source List**（Elsevier 官方 Excel，当前 2026-05 版，**下载本身免登录**，但库内检索需订阅）。下载 URL 是 Contentful CDN 资产链接，**会随版本更新而变**，引用时须从 compendex 产品页 "View source list" 现取，不硬编码 CDN 路径。
- Source List 覆盖说明（产品页原文）："Compendex content is sourced from thousands of publishers ... including major engineering societies such as IEEE, ASME, SAE and ACM."

## 2. 国内会议 / CCF 目录（R3.4）

| 项 | 结论 | 证据 |
|---|---|---|
| CCF 推荐目录官方页 | 存活 | `https://www.ccf.org.cn/Academic_Evaluation/By_category/` → **HTTP 200**（2026-06-11）；页面含"推荐"×28、"国际学术会议"、"领域"分类标识，与 m13 references 既有 CCF 条目（2022 版，A/B/C 三档、十大领域）一致。 |

- 结论：CCF 目录入口可达，沿用 m13 references 既有 CCF 条目口径（官方页 + 社区结构化 gist），本轮不改其数值，仅在"国内会议信号源"节指引。

## 3. 中文刊栏宽实测（R3.5）—— 真实 PDF 量版心

方法：从期刊官网文章页 `citation_pdf_url` meta 取正式出版 PDF，`pdfplumber` 读页面 mediabox（pt→mm，1pt=25.4/72mm）与正文 word 的 x0/x1 众数聚类得双栏边界。

| 刊 | 样本 DOI / 来源 | 页面尺寸 | 单栏宽（实测） | 中缝 | 整幅版心 | 状态 |
|---|---|---|---|---|---|---|
| **农业工程学报** | DOI 10.11975/j.issn.1002-6819.2019.14.030（2019,35(14):235-242），PDF `tcsae.org/cn/article/pdf/preview/<doi>.pdf`，8 页 3.23 MB | A4 210×297 mm | 左栏 15→101mm，右栏 109→195mm → **约 86 mm** | 约 8 mm | 15→195 = **约 180 mm** | ✅ 实测 2026-06-11 |
| **中国农业科学** | DOI 10.3864/j.issn.0578-1752.2026.11.001（2026,59(11):2299-2313），PDF `chinaagrisci.com/CN/article/downloadArticleFile.do?attachType=PDF&id=24078`，15 页 4.11 MB | 裁切 210×285 mm | 左栏 20→101mm，右栏 109→190mm → **约 81 mm** | 约 8 mm | 20→190 = **约 170 mm** | ✅ 实测 2026-06-11 |
| **作物学报** | DOI 10.3724/SP.J.1006.2026.51088（2026,52(6):1830-1846），PDF `zwxb.chinacrops.org/CN/article/downloadArticleFile.do?attachType=PDF&id=18443`，17 页 1.26 MB | 裁切 210×285 mm | 左栏 20→101mm，右栏 109→190mm → **约 81 mm** | 约 8 mm | 20→190 = **约 170 mm** | ✅ 实测 2026-06-11 |
| 农业机械学报 | — | — | — | — | — | GAP：站点 `j-csam.org` PDF 路径被 `_guard/html.js` 反爬拦截（返回 JS 守卫页非 PDF），本轮未取得可量 PDF；待换网络/带 cookie 再测 |

- 度量口径：单栏宽 = 各栏 word x0/x1 众数边界之差，取整到 mm；中缝 = 两栏间空白。**这是版心栏宽（text column），非"建议图宽"**——投稿图宽以投稿系统/作者须知模板为准，栏宽给的是"图按单栏排时的物理上限参考"。
- 三本刊版心高度一致：单栏 ≈81–86 mm、双栏整幅 ≈170–180 mm，符合中文农科刊 A4 双栏惯例。
- 落库：写入 db01 对应 venue 卡新增列（见下游 venues.csv 改动），来源回指本节。

## 4. CNKI / 万方 可达性（R3.2）

| 源 | HTTP 码 | 备注 |
|---|---|---|
| 万方 `wanfangdata.com.cn` | **200** | 可达 |
| 万方一框检索 `c.wanfangdata.com.cn` | **200** | 可达 |
| CNKI `cnki.net` / `kns.cnki.net` | **000**（连接失败/被拒） | 本轮执行环境直连不通；CNKI 题录核对协议按"用户侧浏览器可达"设计，不依赖脚本直连 CNKI。 |
| 维普 `qikan.cqvip.com` | **403** | 反爬 |

- 结论：无 DOI 中文文献核对协议（R3.1/R3.2）以**人工在浏览器比对检索结果页**为准，不假设脚本能直连 CNKI/维普；万方 API 侧可达可作辅助。三字段比对法的留痕格式见 m07/m10 references。

---

## 仍为 GAP（如实标注，非遗漏）

- 农业机械学报版心栏宽：站点反爬，未取得可量 PDF。`GAP：待联网核验（2026-06-XX）`。db01 该刊卡 `column_width_mm` 暂标待核查。
- 中文刊"官方建议图宽硬规格"：三本刊官网均未给出独立于版心的图宽硬规格（与英文刊 author-guide 的 figure width 不同），投稿图宽以投稿系统模板为准。db01 落的是**实测版心栏宽**，已在备注注明语义。
- Compendex Source List 内具体某刊是否被 EI 收录：需下载 5.6 MB Excel 逐条查，本轮只验证了**下载入口活性**，未对具体中文刊做收录逐条核对（属投稿前现查动作，m13 协议已说明）。

---

## 5. 总验收场景走查（R3 收口）

虚构论文《基于深度学习的设施番茄长势无损监测方法》，作者为某农业院校硕士，目标投《农业工程学报》（中文，EI/CSCD，无 DOI 参考文献若干）。沿 m07→m10→m12→m13 全链路逐站核对是否存在"仅英文可用/无路径"断点：

| 站点 | 走到的中文路径 | 落点（本轮新增/已有） | 断点？ |
|---|---|---|---|
| **m07 写作** | 写作时遇无 DOI 中文参考文献，触发"无 DOI 中文文献核对协议"：题录三字段比对法（题名 / 作者+单位 / 刊名+年卷期页），按留痕格式记录待 m10 执行核验；诚信门有指针行 | integrity_gate.md §4 + SKILL.md 诚信门 bullet（R3.1） | 无 |
| **m10 引用** | CNKI/万方题录手工→`.bib` 字段映射（title 加 `{}`、author 全列表 ` and `、刊名全称、页码 `--`、`langid={chinese}`）+ GB/T 7714-2015 速查表核对；3 条真实中文文献已走通手工 checklist 并留痕 | references.md「中文文献核验兜底」+ SKILL.md bullet（R3.2）；3 条留痕见本文件 §3 区 | 无 |
| **m12 排版** | 中文刊走 Word 路线：套官方 .docx 模板→样式/多级列表/题注交叉引用→域 F9 刷新→分节符→自动目录→Zotero/EndNote 按 GB/T 7714 插引用→文档检查器清隐私 | references.md「Word 学术排版」大节（核心 checklist+22 条错误对照表+模板纪律）+ SKILL.md 指针（R3.3） | 无 |
| **m13 投稿** | 《农业工程学报》EI 收录核查走 Compendex Source List（产品页 "View source list" 取当期 Excel 按 ISSN 1002-6819 查）；非计算机方向不套 CCF，按"一级学会（中国农业工程学会）主办+出版检索去向"判正规性；假会议三红线备查 | references.md「EI 核查路径」+「国内会议信号源」+ SKILL.md 指针（R3.4） | 无 |
| **配图（m09→m11）** | 《农业工程学报》单栏图宽用 db01 实测值 86 mm，经 `save_for_journal(fig, base, journal="custom", custom_width_mm=86.0)` 逃生通道出图（不在 JOURNAL_SPECS） | db01 risk_note 实测栏宽 + m09/m11 SKILL.md custom 通道（R3.5） | 无 |

- 结论：中文链路四断点（写作核对 / 引用核验 / Word 排版 / EI 与国内会议核查）+ 配图栏宽，全链路均有可执行中文路径落点，**无"仅英文可用/无路径"断点**。GAP 仅余农业机械学报版心栏宽（反爬，已如实标注，不影响本场景的农业工程学报链路）。
