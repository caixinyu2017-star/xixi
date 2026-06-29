# db02 写作样本卡（seed）

> 用法：抽取结构与论证策略迁移到当前论文，**不照抄原文**。来源链接仅作元数据，受版权全文不收录。

## 卡片模板
```yaml
- venue:
  title_pattern:            # 标题套路
  abstract_structure:       # 摘要分句逻辑(归纳,不录原文)
  intro_problem_gap_contribution:
  related_work_taxonomy:
  method_narrative:
  experiment_design:
  figure_table_logic:
  limitation_expression:
  contribution_sentence:
  reviewer_potential_questions:
  source_url:
  # —— 偏科隔离 + 薄缓存(db02 重构新增, catch-all 子串, 不占正式列) ——
  domain_scope:             # 方向标签(cv-视觉/通用ML统计/统计经济金融/生物医学/NLP语音/cs.* 等);非该方向取卡时过滤
  source_pointer:           # doi + openalex_id, 实时刷新被引的稳定锚
  cited_snapshot:           # 被引快照值(社会证明、非权威事实, 会增长)
  last_checked:             # 快照采集日期 YYYY-MM-DD; 用时以 scripts/paper_signal.py 实时查为准、冲突信在线
```

> 被引数定位为「快照、会增长的 social proof」,非权威值;`scripts/paper_signal.py --doi <DOI>` 实时核。
> **不录摘要原文**(版权纪律): abstract_structure 只写人工归纳的分句逻辑,引用零星英文短句仅作模式示例。
> 背书规则按方向用: cs.AI/CV 的竞赛排名/SOTA/开源 social proof 不套用到统计/医学/农业等方向。

## 高频可迁移套路（领域无关）

### 标题套路
- "方法名: 一句话能力描述"（如 "X-Net: Efficient ... for ..."）
- "动词开头的问题陈述"（如 "Learning to ... via ..."）
- 避免空泛词("A Study on")；体现新意与任务。

### 实验章节标准顺序
1. Experimental Setup（数据集 / baselines / 指标 / 实现细节 / 算力）
2. Main Results（主表 + 一段解读）
3. Ablation Study（逐组件，证明贡献来源）
4. Analysis（敏感性 / 收敛 / 复杂度）
5. Qualitative Results（可视化 / case study）
6. Limitations

### 审稿人高频追问（预演用，喂 m14）
- 创新点和最接近的工作 X 到底差在哪？
- 对比是否公平（同数据/同算力/同设置）？
- 提升是否统计显著（多种子+检验）？
- 消融能否证明提升来自所声称的组件？
- 在更大规模/真实场景能否泛化？
- 计算开销代价如何？

### 措辞红线（写作/润色共用）
慎用 novel / significantly / state-of-the-art / first，每个都要有证据支撑，否则审稿人反感。

## 待补充
按用户领域逐步加入 3–5 篇代表作的结构化卡片（从 OpenReview/arXiv 公开版抽取结构）。
