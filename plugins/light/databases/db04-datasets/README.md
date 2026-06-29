# db04 — 数据集、Benchmark 与开源项目资源库

为各领域数据集/benchmark/开源项目建立 dataset_card，供 m02(数据)、m05(方案)、m03(idea) 使用。

> **定位（库重构 2026-06-13）**：~100 张卡是**薄缓存 + 方法论层 + 偏科隔离**的混合库，不是"全精养静态卡"。
> - **事实锚点层**：dataset_name/domain/task/data_type/size/format 等本地精养，稳定。
> - **薄缓存层**：citation 被引/license/download_url 是**快照**，卡内 citation 字段尾部带 `last_checked=` + 锚点（`oa_id=W...` 可 OpenAlex 实时查被引 / `doi=...` 可 Crossref 查 / `src=community` 无实时源）；用 `scripts/dataset_signal.py` 实时校验，**冲突默认信在线**（license 例外：变更须人工确认，合规高危）。
> - **偏科隔离层**：known_issues 尾部带 `domain_scope=` 子串（如 通用CV/精准畜牧-奶山羊/自动驾驶-特定地域），非该方向用户应过滤；bias_risk 的"通用警示"(PII/标签噪声)不随方向折叠、"偏科判断"(西方中心/单城)才折叠。
> - **方法论层**：preprocessing_steps/recommended_splits 的通用防泄漏原则上移至 m02 命名锚点（`SPLIT-01` time-forward / `SPLIT-02` 按组分域 / `LEAK-01` 训练折内 fit），卡内只留 dataset-specific 实参 + 指针。
> - **诚实边界**：卡严重集中在 CV/多模态/动物视觉（约 76/100），材料化学/社科等方向覆盖薄（各 6-7 卡），换方向用户按 `domain_scope=` 过滤后可用卡更少——扩库时按方向补。

## dataset_card schema
`dataset_name, domain, task, data_type, size, format, license, download_url, paper_url, citation, leaderboard_url, known_issues, bias_risk, privacy_risk, preprocessing_steps, recommended_splits`

> 16 字段固定（CI 校验）。锚点/口径/偏科标记不加列，以 `key=value` 子串塞进 citation/known_issues 字段（同 db01 哲学）。`migrate_db04.py` 幂等回填，`scripts/dataset_signal.py --selftest` 离线自测。

## 数据来源
Hugging Face Datasets、Kaggle、OpenML、UCI ML Repository、Papers With Code Datasets、Google Dataset Search、Zenodo、Figshare、DataHub、Open Graph Benchmark、各领域官方数据集站、GitHub 论文复现仓库。

## ⚠ 许可协议（必记，联动 a10）
每条必须记录 `license`，并明确：
- 是否允许商用？
- 是否允许再分发？
- 是否涉及个人隐私(privacy_risk)？
- 是否需要申请授权？
不确定许可的数据集标红，使用前核实。

## 使用方式
- m02：从 known_issues / bias_risk / preprocessing_steps 预判数据坑。
- m05：从 recommended_splits / leaderboard_url 取标准设置与 SOTA。
- m03：从 data_type 判断创新机会。

## 维护说明
卡片归档。记录引用方式(citation)便于 m10 引用。每张卡的 license 必填、论文引用由 OpenAlex 实拉。

## 卡片文件
- [cards_cv_nlp.md](cards_cv_nlp.md) — CV/NLP 数据集（ImageNet/COCO/GLUE/SQuAD 等，含真实 paper_url/被引/license）
- [cards_tabular_other.md](cards_tabular_other.md) — 表格/图/时序/多模态/领域（UCI/OGB/MIMIC-III/遥感等，授权风险已标注）
- [cards_frontier.md](cards_frontier.md) — 前沿数据集（LAION-5B/The Pile/C4/nuScenes/CheXpert/DeepWeeds 等，按大模型/多模态/3D驾驶/科学分子/医疗/农业 六类，20 卡；QM9/LibriSpeech/Common Voice/PlantVillage canonical 见领域文件）
- [cards_animal_livestock.md](cards_animal_livestock.md) — 动物/家畜行为·姿态·检测（AP-10K/Animal Kingdom/Cows2021/CherryChèvre 等 19 卡；含奶山羊专用数据集现状评估与自建建议，缺口如实标注）
- [dataset_cards.md](dataset_cards.md) — 卡片模板 + canonical 索引（0 张实体卡，避免重复 dataset_name）
- [cards_physical_sciences.md](cards_physical_sciences.md) — 理工跨学科/科学计算数据集（Materials Project、QM9、OQMD、OC20、JARVIS、WeatherBench/ERA5、HCP 等 7 卡）
- [cards_biomedical.md](cards_biomedical.md) — 生物医学/临床/组学数据集（MIMIC-IV、eICU、UK Biobank、TCGA、MIMIC-CXR/CheXpert、ADNI、HAM10000/ISIC 等 7 卡）
- [cards_stats_econ_finance.md](cards_stats_econ_finance.md) — 统计/经济金融/社会科学数据集（FRED-MD/QD、PWT、WDI、Fama-French、CRSP/Compustat/WRDS、OECD 等 6 卡）
- [cards_nlp_speech.md](cards_nlp_speech.md) — NLP/语音/多语言评测数据集（MMLU、XTREME、LibriSpeech、Common Voice、VoxCeleb、FLEURS、VoxPopuli/AISHELL 等 7 卡）
