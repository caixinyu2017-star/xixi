# R4.15 SPECTER2 语义嵌入 — S2 API 实测留痕

- 研究日期：2026-06-11
- 执行：Claude Opus 4.8（Claude Code）
- 任务：light-literature-search 补"语义去重/相似检索"节（S2 embedding 端点实测）；
  light-idea-generation 候选 idea 防伪多样性引用（双向）。

## 实测端点（HTTP 200，本机 urllib 直连，2026-06-11）

- 单篇：`GET /graph/v1/paper/DOI:{doi}?fields=embedding.specter_v2`
  → 返回 `embedding.model=specter_v2`、`embedding.vector`=**768 维** float。
  实测 CherryChèvre 数据集论文：768 维向量取得。
- 批量：`POST /graph/v1/paper/batch?fields=title,embedding.specter_v2`，body `{"ids":[...]}`
  → 一次取多篇向量。id 支持 `DOI:`/`ARXIV:`/`CorpusId:` 等。

## 余弦相似度实测（三篇经典论文）

ids = BERT(ARXIV:1810.04805)、GPT-3(ARXIV:2005.14165)、ResNet(ARXIV:1512.03385)

| 对 | 余弦相似度 |
|---|---|
| BERT vs GPT-3（都是 NLP 语言模型） | **0.9308** |
| BERT vs ResNet（NLP vs CV） | 0.8971 |
| GPT-3 vs ResNet（NLP vs CV） | 0.8558 |

→ 语义排序符合直觉：同主题（BERT/GPT-3）相似度最高，跨主题（语言模型 vs 视觉）最低。

## 关键诚实细节（写入节）
1. **SPECTER2 余弦值整体偏高**（实测 0.85~0.93），**不能用绝对阈值**判同异，要看**相对差**
   （同一批候选内排序、或相对同主题 baseline 的偏移）。
2. **部分论文无 embedding**：实测某 compag DOI 在 batch 返回里无 embedding 字段
   （S2 未收录或未生成 SPECTER2 向量）——降级回标题/摘要文本相似度，不假装有向量。
3. **限流**：匿名共享池高峰常 429，批量/稳定用须申请免费 `x-api-key`（与 SKILL 既有口径一致）。

## 双向联动（堵单向挂载）
- light-literature-search：用 SPECTER2 做跨库**语义去重**（标题不同但语义重复的同一工作）与
  **相似检索**（找与种子论文语义最近的工作，补关键词检索盲区）。
- light-idea-generation：候选 idea 两两算 SPECTER2 相似度，**过高视为同一 idea 的变体**
  （防"换皮凑数"伪多样性）。需在 idea-generation 侧写消费声明（双向）。
