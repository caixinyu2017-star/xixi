# db03 — 研究方法与技术路线知识库

按领域建立 method_card，帮 m03(提 idea)、m04(审 idea)、m05(方案)、m01(调研) 快速判断该用什么方法、什么过时、什么可做创新基础、什么适合做对比。

## 这个库是什么(诚实卖点)

**不是** "175 张实拉被引的方法权威库",而是**方法论本地精养 + 被引/仓库状态实时核**的分层资产:

- **方法论层(本地精养,护城河)**:每张卡的 `core_assumption / advantages / limitations / common_baselines / evaluation_metrics` 是跨学科稳定的方法学判断——"这方法假设什么、强在哪、什么场景会崩、标准 baseline 和指标是什么"。这部分几乎不过时,是库的真正价值,m05 直接取作方案对比设置。
- **薄缓存层(易变事实,实时核)**:`representative_papers` 的被引数、`implementation_repo` 的仓库存活状态是会变的事实。本地只存**快照值 + DOI/repo 指针 + last_checked 日期**(239 处被引已带 checked 标注),真实数由 [`scripts/method_signal.py`](scripts/method_signal.py) 实时查 OpenAlex/GitHub;冲突默认信在线,无网降级到快照并标 stale,绝不把过期值当权威。
- **偏科隔离层(可过滤)**:175 张卡 = **通用方法卡 93 张 + CV 偏科卡 82 张**。CV 卡(检测跟踪 25 / 行为识别 25 / 夜间多模态 18 / 时序动作 14)里的**方法本身是通用 CV 方法**(Faster R-CNN、YOLO、DETR、SlowFast、VideoMAE、ST-GCN、ByteTrack 等,方法学不偏科),只是 `suitable_datasets / possible_innovation_points` 附带了奶山羊/家畜场景的适配注解。靠卡级 `domain_scope=` 标签隔离,非该方向用户调用时按白名单过滤即可不受干扰。

## method_card schema
`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`

- `maturity`: 经典 | 主流 | 新兴 | 过时 | 不推荐
- `domain_scope=`(catch-all 子串,追加在 `possible_innovation_points` 等字段值内,不占正式列):标卡的适用方向。通用方向(`通用ML统计 / 通用深度学习 / 数据挖掘 / 统计经济金融 / 生物医学 / 物理科学 / NLP语音 / 前沿ML`)对所有用户可见;CV 偏科(`cv-检测跟踪 / cv-行为识别 / cv-夜间多模态 / cv-时序动作`)非 CV 项目可过滤排除。

## 数据来源
Papers With Code、Hugging Face Models/Papers、GitHub Trending、Awesome 系列、OpenReview、arXiv、Semantic Scholar、领域综述、各会议 tutorial、官方 benchmark leaderboard。被引/仓库状态等易变事实以本地快照 + 实时核为准(见下)。

## 更新方式
每个方法标注成熟度(经典/主流/新兴/过时/不推荐)，避免 Light 提出已落后的方案。新兴方法定期升降级。`maturity` 的"过时/被替代"判断多带领域时间线前提(如 CV-2026),跨领域引用时不要直接套用。

## 使用方式
- m03 提 idea 前：查目标任务的主流/新兴方法 + possible_innovation_points;按项目方向用 `domain_scope=` 过滤(非 CV 项目排除 cv-* 卡)。
- m04 审 idea：用 maturity 判断是否"做烂了"或"已过时";撞车/被引复核走实时检索,不依赖本地快照值。
- m05 方案：从 common_baselines / evaluation_metrics 直接取对比设置(本地精养、稳定);suitable_datasets 取名后转 db04 查规模/许可。

## 被引/仓库状态实时核
易变事实不当权威值存。[`scripts/method_signal.py`](scripts/method_signal.py)(照 db01 venue_signal 模式)实时查:①`representative_papers` 被引数 → OpenAlex Works by-DOI;②`implementation_repo` 存活 → GitHub repos API(200/301 迁移/404 失效)。本地每条只存 `快照值 + 指针 + (checked:日期)`(已回填 239 处)。冲突默认信在线并回写日期;无网返回快照 + 标 stale,不崩、不编新数。OpenAlex key/限流唯一口径见 m01 references「OpenAlex 接入真相源」,本脚本只加 mailto 不复写数字。脚本自检:`PYTHONUTF8=1 python scripts/method_signal.py --selftest`。

## 维护说明
方法卡按领域归档。每张卡注明代表论文与开源实现链接(受版权全文不收录,仅元数据/链接)。代表作的被引数为 OpenAlex 实拉快照、带 last_checked,可随时实时复核;不保证每次读取都是最新值,以 method_signal.py 实时查为准。新增卡须填 domain_scope 与代表作快照日期。

## 卡片文件(共 175 张:通用 93 + CV 偏科 82)

代表作的被引数均为 OpenAlex 快照值(带 checked 日期),以 method_signal.py 实时核为准,下列各文件不再逐一标注。

**通用方法卡(93 张,domain_scope 通用,所有方向可见):**
- [cards_ml_stats.md](cards_ml_stats.md) — 机器学习/统计学习（随机森林/GBDT/SVM/聚类/降维等，12 卡，`domain_scope=通用ML统计`）
- [cards_dl.md](cards_dl.md) — 深度学习/CV/NLP（ResNet/Transformer/Diffusion/GNN/RL/LoRA 等，14 卡，`domain_scope=通用深度学习`）
- [cards_mining_other.md](cards_mining_other.md) — 数据挖掘/图/时序/推荐/优化（18 卡，`domain_scope=数据挖掘`）
- [cards_frontier.md](cards_frontier.md) — 前沿/新兴方法（自监督/MAE/LLM Agent/Mamba/多模态大模型/NeRF/3DGS 等，25 卡，`domain_scope=前沿ML`；RAG canonical 见 cards_nlp_speech.md）
- [cards_biomedical.md](cards_biomedical.md) — 生物医学方法（Cox/KM、U-Net/nnU-Net、GWAS、临床预测、AlphaFold、CheXNet 等，6 卡，`domain_scope=生物医学`）
- [cards_physical_sciences.md](cards_physical_sciences.md) — 理工跨学科/物理化学材料（MPNN/SchNet/CGCNN、DFT、MLIP、EEGNet、Pangu/GraphCast、CALYPSO/USPEX 等，6 卡，`domain_scope=物理科学`）
- [cards_stats_econ_finance.md](cards_stats_econ_finance.md) — 统计/经济金融/因果推断（DiD、IV/LATE、RDD、PSM/IPW、GARCH/VAR、分位数回归/因果森林等，6 卡，`domain_scope=统计经济金融`）
- [cards_nlp_speech.md](cards_nlp_speech.md) — NLP/语音（Seq2Seq/Transformer、T5/GPT-3、RAG、CTC/Conformer、wav2vec2/HuBERT、Whisper 等，6 卡，`domain_scope=NLP语音`）

**CV 偏科卡(82 张,方法本身通用、附奶山羊适配注解,非 CV 项目可按 domain_scope 过滤):**
- [cards_detection_tracking.md](cards_detection_tracking.md) — 目标检测 + 多目标跟踪（Faster R-CNN/YOLO 系/DETR 系/SORT/ByteTrack/OC-SORT 等，25 卡，`domain_scope=cv-检测跟踪`，含奶山羊/家畜场景适配注解）
- [cards_action_spatiotemporal.md](cards_action_spatiotemporal.md) — 行为识别 + 时空特征融合（Two-Stream/I3D/SlowFast/TimeSformer/VideoMAE/ST-GCN/PoseC3D 等，25 卡，`domain_scope=cv-行为识别`，含奶山羊行为细粒度/长时序适配注解）
- [cards_nighttime_multimodal.md](cards_nighttime_multimodal.md) — 夜间红外/热成像检测 + RGB-IR 多模态融合 + 级联误差/端到端联合（Zero-DCE/CFT/ProbEn 等，18 卡，`domain_scope=cv-夜间多模态`，含昼夜预警与四级流水线误差传播适配注解）
- [cards_temporal_action.md](cards_temporal_action.md) — 时序动作检测(TAL) + 序数回归（ActionFormer/BMN/TriDet/CORAL/CORN/QWK 等，14 卡，`domain_scope=cv-时序动作`，适配发情爬跨瞬时事件定位与跛行有序评分）

**索引(不计入卡数):**
- [method_cards.md](method_cards.md) — 卡片模板 + canonical 索引（0 张实体卡，避免重复 method_name）
