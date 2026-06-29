# 文献追踪 diff 报告 · 2026-06-12（首轮基线 + 增量演示）

> 由 m01 `search_normalize.py --from-date ... --known-dois ...` 真实跑出（OpenAlex=200 / Crossref=200）。
> 本报告同时是 R11.4「真实增量追踪跑通」的留痕。

## 跑了什么

1. **基线**：`"dairy goat behavior recognition"` per-page 12，双源合并 **24 条**（含 DOI），存入 `known_dois.txt` 作为"已读库快照"。
2. **增量**：同 query 加 `--from-date 2023-01-01 --known-dois known_dois.txt`，双源合并 24 条，diff 出 `new=24`（与 ≤2022 基线零重叠）。

机制层结论：**`--from-date` 过滤生效**——基线年份跨 1970–2020，增量结果仅 2023–2024，`year<2023` 条目数 = 0；增量去重 diff 正确把已读 DOI 全部剔除。增量追踪的管线打通。

## 关键发现（诚实标注，比"找到 N 篇新文献"更重要）

**宽 query + 纯被引排序的原始增量输出几乎全是领域外高被引噪声，不能直接入库。**

24 条"新增"里，真正与奶山羊行为识别相关的 ≈ 0–1 条（最沾边的是一篇山羊肠道微生物组论文 `10.1186/s40104-023-00856-x`，但属微生物而非行为识别）；其余是 YOLOv7、DETR、DreamBooth、Visual Instruction Tuning、Job Demands–Resources Theory 等通用 CV/无关高引文——它们因被引量极高被 `cited_by` 排序顶上来。

这正复现了 m01 SKILL 与 examples 里的检索教训：**宽检索式必须配标题/摘要相关度筛选，原始命中是候选不是结论**。所以本轮**没有**把任何条目自动追加进 `known_dois.txt`——按协议，新条目须人工按相关度筛过才入库，演示阶段不污染已读库。

## 下一步（真正做这个项目追踪时）

1. 收窄检索式：`goat` + (`estrus` OR `rumination` OR `lameness` OR `tracking` OR `accelerometer`)，或限定精准畜牧刊（Computers and Electronics in Agriculture、Animals、Biosystems Engineering）。
2. 跑中文源（《农业工程学报》《畜牧兽医学报》按 ISSN 检 OpenAlex source）——本轮未跑，待补。
3. 人工筛相关 → 确认条目 DOI 追加 `known_dois.txt` → 更新 `saved_search.yaml` 的 `last_run_date` → 下月以新日期增量重跑。

## 局限

- 本轮用宽 query 是为**演示增量机制**，非该项目的正式文献追踪；正式追踪须先收窄（见上）。
- 被引数来自 OpenAlex 口径，不跨库直比。
- 中文文献本轮未覆盖。
