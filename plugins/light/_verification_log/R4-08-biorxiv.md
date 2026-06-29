# R4.8 bioRxiv/medRxiv 预印本源 — API 实测留痕

- 研究日期：2026-06-11
- 执行：Claude Opus 4.8（Claude Code）
- 任务：light-literature-search 补 bioRxiv 源（API 实测），预印本可信度分级与 db01 联动。

## 实测端点（均 HTTP 200，本机 urllib 直连，2026-06-11）

Base：`https://api.biorxiv.org`（medRxiv 同 API，server 段换 `medrxiv`）

| 端点 | 用途 | 实测结果 |
|---|---|---|
| `/details/biorxiv/{from}/{to}/{cursor}` | 按日期区间拉预印本元数据 | HTTP 200，total=220（2024-01-01~02），每页 30 条 |
| `/details/biorxiv/{doi}` | 按 DOI 取单篇 | HTTP 200，返回 version/category 等 |
| `/pubs/biorxiv/{from}/{to}/{cursor}` | 预印本→正式发表映射 | HTTP 200，total=267（2023-01-01~05） |
| `/details/medrxiv/{from}/{to}/{cursor}` | medRxiv 同结构 | HTTP 200，total=24 |

### 关键字段
- `/details/` collection[]：`doi`、`title`、`authors`、`date`、`version`、`category`、`published`
  （`published=NA` 表示尚未在期刊正式发表）。
- `/pubs/` collection[]：`preprint_doi` → `published_doi` + `published_journal`
  （实测样例：某 bioRxiv 预印本 → `10.1371/journal.pbio.3001961` / PLOS Biology）。
  **这是可信度升级的硬信号**：预印本若 pubs 端点查到 published_doi，说明已通过同行评审正式发表，应改引正式版。

## 可信度分级（写入 references + 与 db01 联动）
1. 预印本**未发表**（published=NA 且 pubs 无映射）：未经同行评审，引用须显式标注，结论作"线索"非定论。
2. 预印本**已发表**（pubs 有 published_doi）：换引正式发表版 DOI（与 light-citation verify_refs 的 preprint warning 一致）。
3. 版本号 version>1：注意引用的是哪一版，结论可能随版本变。

与 db01 联动：预印本平台（bioRxiv/medRxiv/arXiv）不是传统 venue，db01 不单列；在文献表"可信度"列按上述分级标注，预印本风险口径与 light-citation verify_refs.py 的 `type=preprint` warning 同源。

## 四源并查口径
生医/系统综述方向：OpenAlex（覆盖广）+ Europe PMC（免 key、直接给 abstract+开放标记）+ PubMed（MeSH+Clinical Queries 独有）+ bioRxiv/medRxiv（预印本最前沿，但需可信度分级）。bioRxiv 补"最新未发表"盲区，PubMed 补"受控词规范检索"，四源互补。
