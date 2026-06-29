# 端到端 worked example：奶山羊行为监测（dairy goat behavior monitoring）

本例用本目录脚本真实跑通，记录 PICO → 各库 query → 命中 → 去重 → 筛选留痕。
配套产物：`goat_littable.md`（文献表）、`goat_search.json`（原始合并记录）。

## 1. PICO
- P（对象）：舍饲奶山羊（dairy goat）
- I（方法）：传感器/视频自动行为识别（accelerometer / computer vision）
- C（对比）：人工观察 / 传统阈值法
- O（结果）：行为分类准确率、可监测的行为种类（采食/反刍/活动）

## 2. 各库实际 query 字符串（可直接复制）
- OpenAlex：
  `https://api.openalex.org/works?search=dairy goat behavior monitoring&sort=cited_by_count:desc&per-page=8&mailto=...`
- Crossref：
  `https://api.crossref.org/works?query.bibliographic=dairy goat behavior monitoring&sort=is-referenced-by-count&order=desc&rows=8&mailto=...`
- 中文（按核心刊 ISSN，例：中国农业科学）：
  `https://api.openalex.org/works?filter=primary_location.source.id:S4306529288&search=山羊 行为&sort=cited_by_count:desc`

实跑命令：
```
python scripts/search_normalize.py "dairy goat behavior monitoring" --per-page 8 \
    --json-out examples/goat_search.json --md-out examples/goat_littable.md
```
本次运行：`[HTTP] OpenAlex=200 Crossref=200`，raw=16 → merged=16。

## 3. 命中 → 去重留痕（PRISMA 思想）
| 库 | 检索式 | 命中 | 去重后 | 标题/摘要筛后 | 纳入 |
|----|--------|------|-------|-------------|------|
| OpenAlex | search=dairy goat behavior monitoring, sort=cited_by | 8 | — | （见下） | — |
| Crossref | query.bibliographic=同上, sort=is-referenced-by | 8 | — | — | — |
| 合并 | DOI 优先归并 | 16 | 16 | 主题相关约 3–5 | 入方法卡 |

去重：本次两库 top 命中 DOI 不重叠（OpenAlex 按其相关度+被引、Crossref 按被引），
故 merged 仍 16；真实项目里跨库重叠通常出现在主题更窄的检索。

## 4. 关键教训（诚实记录，写进 SKILL.md 注意事项）
对**宽口径 search + 纯 cited_by 排序**，会把领域外的超高被引论文顶上来
（本次 top 命中如 "theory of planned behavior"、"G*Power" 等通用高被引文，
明显跑题）。正确做法：
1. 收窄检索（加 `filter=primary_topic.id:` 或更具体短语、限定 `from_publication_date`）；
2. 排序后**必做标题/摘要相关度筛选**，不可直接采信被引序；
3. 中文成果走 ISSN 范围检索补齐（英文库对小众畜牧主题覆盖偏弱）。

## 5. 筛选后纳入（示例，需按摘要二次确认）
真正相关的应是 `Computers and Electronics in Agriculture` / `Animals` /
`Sensors` 等农业工程刊里的行为识别工作；用收窄 query 复跑：
```
python scripts/search_normalize.py "goat accelerometer behaviour classification" --per-page 10
```

## 6. 引用核验
入表后对每条 DOI 跑：
```
python scripts/verify_citations.py 10.1038/s41597-023-02555-8 --title "CherryChevre" --year 2023
```
实测该 DOI HTTP=200，权威标题
`CherryChèvre: A fine-grained dataset for goat detection in natural environments`
（Scientific Data, 2023）——是一个真实可用的山羊检测数据集，可直接入资源清单。
