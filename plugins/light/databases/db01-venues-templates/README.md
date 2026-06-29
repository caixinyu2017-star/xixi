# db01 — 期刊会议与模板资源库

覆盖中英文期刊、会议与投稿模板的知识库，供 m13(投稿匹配)、m12(排版)、m10(引用格式)、m01(调研) 使用。

> **定位（库重构 2026-06-13）**：这是一个**薄缓存 + 方法论层**的混合库，不是"权威 IF 静态库"。
> - **薄缓存层**：venues.csv 的事实字段（IF/被引/APC/分区/链接）是**快照**，每行带 `last_checked_date` + `oa_id=`/`issn=` 锚点，投前用 `venue_signal.py` 实时复查 OpenAlex，**冲突默认信在线**。
> - **方法论层**：跨学科通用、几乎不过时的资产（`reference_style`→LaTeX cls/bst 映射、subject_area 受控词归一、采集核验管线、risk_note 子串口径）沉淀在 **[references.md](references.md)**。
> - **诚实边界**：① 46 个会议 **100% 是 CS 方向**，其他学科会议待扩；② `impact_factor` 分两类口径（`if_kind=jcr` 真 JCR 仅 5 行 / `if_kind=proxy` OpenAlex 代理值 245 行），**代理值禁当 JCR 真值引用**；③ `cas_quartile`/`ccf_level` 是**偏科字段**（仅中国语境/中国 CS 适用），用 `domain_scope=` 子串隔离，非该方向用户应过滤。

## 字段 schema（统一）
`source, venue_name, venue_type, publisher, subject_area, level, indexing, impact_factor, jcr_quartile, cas_quartile, ccf_level, review_cycle, apc_fee, template_url, submission_url, reference_style, representative_papers, risk_note, last_checked_date`

- `venue_type`: journal | conference
- `level`: 中文(北大核心/CSCD/CSSCI/科技核心) | SCI | EI | CCF-A/B/C | 其他
- `indexing`: SCI/SSCI/EI/Scopus/CCF/北大核心 等
- `reference_style`: IEEE | ACM | APA | GB/T 7714 | Springer LNCS | Elsevier 等

## 数据来源（建库 & 更新去哪找）
OpenAlex Venues、Crossref、Semantic Scholar、arXiv、DOAJ、Web of Science/JCR、Scopus Sources、Scimago(SJR)、CCF 推荐目录、北大核心目录、CSCD/CSSCI 目录、各出版社官网(IEEE/ACM/Springer/Elsevier/Wiley/Nature/Science)、各会议官网、Overleaf 模板库、各社官方 LaTeX 模板页。

## 合规
受版权论文/模板**只存元数据、链接、摘要、笔记、引用关系**，不收集违规全文。优先公开资源、官方模板、arXiv、预印本、作者主页公开版。

## 更新方式
可执行流程（落地"定期更新"承诺，避免空头）：每月跑一次 `python .github/scripts/check_freshness.py`，按它列出的超期清单逐条复查更新——这是 warn-only 检查，不影响 CI，只产出待办清单。超期行可喂给 `venue_signal.py --batch venues.csv` 批量实时复查 OpenAlex，产"在线值 vs 本地快照"diff 清单。
- 每月：跑 check_freshness 取超期清单 + `venue_signal.py --batch` 复查 + 更新元数据。
- 每季度：更新分区、版面费、模板链接、预警信息。
- 每次选投稿目标前：对候选 venue 重新核查一次并更新 `last_checked_date`。

## 维护说明
- 新增条目追加到 [venues.csv](venues.csv)（表头即上述字段）。
- 预警/掠夺性期刊在 `risk_note` 明确标注，并联动 m13/a10。
- 模板缺失时在 `template_url` 标注 "需补"。

## 采集→核验→入库管线（实际作业流程，照此复现可扩库）
1. **采集**：OpenAlex Sources API 按方向 `search=` 或 `filter=country_code/type` 拉候选；记 ISSN/display_name/works_count/summary_stats(h_index、2yr_mean_citedness)/host/type。
2. **双源核验（铁律）**：按精确 ISSN 回查 OpenAlex（不盲取 search 第一条），比对年份/被引/works_count/host 合理性；剔除 works_count<50 的碎片记录与重名/同 ISSN 重复；代表作取该刊被引前列 works（真实 cited_by）。
3. **入库**：按 19 列 schema 生成行，含英文逗号/引号的字段必须加引号（拿不准就交给程序按 CSV 规范转义，勿手填裸逗号）。`impact_factor` 列写值并在 risk_note 标 `if_kind=`：真 JCR（带 LetPub journalid）标 `if_kind=jcr`；OpenAlex 2yr 均被引代理或付费墙不可得标 `if_kind=proxy`（**非 JCR IF**）；会议无 IF 标 `if_kind=na`。落 `oa_id=`/`issn=`/`domain_scope=` 锚点子串（口径见 references.md §1，migrate_db01_v2.py 可幂等回填）。
4. **校验**：`PYTHONUTF8=1 python .github/scripts/check_databases.py`（CSV 不进 YAML schema 校验，但须自检列数=19、物理行数=逻辑行数即无多行字段被压平）。
5. **落日期**：`last_checked_date` 列填 `YYYY-MM(-DD)`，供 [check_freshness.py](../../.github/scripts/check_freshness.py) 月度统计。

> 改 venues.csv 三条血泪铁律（R4/R8）：①含多行字段时禁用 csv 模块全量重写（会压平多行）——本库当前无多行字段，重写安全，但改前务必先验"物理行数==逻辑行数"；②无引号字段禁含英文逗号（会拆列），用中文分号/顿号或加引号；③`last_checked_date` 必须是日期格式。

## ai_policy 字段口径
`risk_note` 内的 `ai_policy=` 子串记录该 venue 的生成式 AI 投稿政策（CONVENTIONS §3 定义）。**出版社级政策**（Elsevier/IEEE/Wiley/Springer/Nature/ACM 等同社旗下期刊共用）按出版社官方政策页实查后批量标注，带官方页出处 + 核验日期；会议（CVPR/NeurIPS/ICML/ICLR 等）按各自 CFP/Author Guidelines 单独实查。三类常见口径：期刊=AI 辅助写作须披露+AI 不得署名+原始数据图禁用 AI；ML 会议=LLM 允许+作者全责+不得署名；Nature/Springer 额外=生成式 AI 图像原则禁止。论文图严禁生成式 AI（真相源 m11 figure_integrity「AI 生成图像政策」节）。

种子数据见 [venues.csv](venues.csv)。
