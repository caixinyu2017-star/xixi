# db03 方法卡 — 时序动作检测(TAL) + 序数回归（cards_temporal_action.md）

> 每张卡注明 maturity（经典|主流|新兴|过时|不推荐），避免提出落后方案。受版权全文不收录，仅元数据与开源链接。
> representative_papers 的标题/年份/被引/DOI 来自 OpenAlex 真实 curl 结果（https://api.openalex.org，mailto 礼貌池），查询日期 **2026-06-06**；被引数随时间变动。
> 同一论文 OpenAlex 常有「会议正式版」与「arXiv 预印本」两条记录，被引分散；本卡优先取被引更高的正式版，并在必要时标注。
> 排名/成熟度判断为人工标注。查不到的字段写「待核查」。

字段 schema 同 db03：`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`

## 为什么补这一类（动因）

现有 db03 行为卡（cards_action_spatiotemporal.md）全是 **trimmed-clip 分类**——输入已剪好的短片段、输出单一动作类别，假设"片段里有且只有一个动作"。但奶山羊真实监控是**未剪辑长视频**：
- **发情爬跨**：秒级瞬时稀疏事件，一天可能只出现几次、每次数秒，淹没在数小时正常行为里 → 需要在长视频里**定位起止时刻**，分类模型无法回答"何时发生"。
- **跛行**：分钟级周期步态异常，需在连续行走片段里**圈出异常步态区间**，且严重程度是**有序分级**（locomotion score 1–5）。
- 两类都**长尾稀疏**，正常行为占绝对多数。

→ 第一部分 **时序动作检测/定位(TAL)** 解决"长视频里事件的起止定位"；第二部分 **序数回归** 解决"跛行评分 1–5 这种有序多级标签的损失与评测"（普通分类把 1 和 5 的错分代价等同于 1 和 2，不合理）。

## 奶山羊 TAL + 序数评分 适配总览

- **数据现实（诚实声明）**：TAL 的公开基准 **THUMOS14 / ActivityNet-1.3 / EPIC-Kitchens-100** 全部是**人体/第一视角**动作，无任何奶山羊时序定位基准。curl OpenAlex 检索"goat estrus mounting video temporal"、"sheep lameness gait video localization"均未返回视频时序定位基准（多为加速度计/PLF 综述）。**奶山羊发情爬跨起止、跛行步态区间的时序标注须自建**，公开集仅用于预训练与方法选型，不可声称存在山羊 TAL 基准。
- **跛行评分金标准**：兽医常用 Sprecher (1997) 5 级 locomotion scoring（牛），山羊可类比自建；标注本身有序、相邻级易混 → 适合序数回归 + QWK 评测，而非普通 Accuracy/F1。
- **方法选型结论**（详见各卡 possible_innovation_points）：
  - 秒级瞬时事件（爬跨）→ ActionFormer/TriDet 多尺度特征金字塔对短时实例敏感；BMN/BSN 的密集 proposal 召回适合稀疏正样本。
  - 分钟级周期步态（跛行区间）→ 长时序建模强的 ActionMamba/Video-Mamba 线性复杂度利于长视频；TadTR 端到端 set prediction 减少 NMS 超参。
  - 长尾稀疏 → 提高 proposal 召回 + focal/类重加权；TAL 头与跛行严重度的**序数回归头**多任务联合（先定位区间，再对区间打 1–5 分）。
  - 评分头损失 → CORAL/CORN 保证 rank 单调一致，评测用 QWK + 序数 MAE，而非 plain Accuracy。

---

## 一、时序动作检测 / 定位（TAL）方法卡

```yaml
- method_name: "ActionFormer"
  task_type: "时序动作检测/定位(单阶段, anchor-free, 长视频未剪辑)"
  input_data: "长视频预提取的片段特征序列(I3D/SlowFast/VideoMAE 等逐片段特征)"
  output_result: "每个时间步的动作类别 + 到动作起/止边界的距离回归(即起止时刻 + 类别 + 置信度)"
  core_assumption: "在多尺度时序特征金字塔上做局部自注意力, 把 TAL 当作\"每个时刻直接回归边界\"的密集预测, 无需预设 anchor 或两阶段 proposal"
  advantages: "单阶段端到端、anchor-free、Transformer 多尺度对不同时长动作鲁棒、在 THUMOS14/ActivityNet/EPIC 上长期 SOTA、实现简洁是当前最常用 TAL 基线"
  limitations: "依赖冻结的预提取特征(特征质量决定上限)、对极短瞬时事件的边界仍受特征时间分辨率限制、超长视频自注意力开销随长度增长"
  common_baselines: "BMN、G-TAD、TadTR、A2Net、TriDet"
  evaluation_metrics: "mAP@tIoU(0.3:0.7 平均, ActivityNet 用 0.5:0.95)、Average-mAP"
  suitable_datasets: "THUMOS14、ActivityNet-1.3、EPIC-Kitchens-100(均为人体/第一视角, 奶山羊须自建时序标注)"
  implementation_repo: "happyharrycn/actionformer_release(官方)、mmaction2(OpenMMLab, 含 TAL 配置)"
  representative_papers:
    - "ActionFormer: Localizing Moments of Actions with Transformers | 2022 | cited:重(OpenAlex relevance≈2112, 该ECCV/LNCS条目) | doi:10.1007/978-3-031-19772-7_29 | checked:2026-06-06"
  possible_innovation_points: "首选 TAL 基线。奶山羊监控长视频先用 VideoMAE/SlowFast 抽片段特征再喂 ActionFormer 定位发情爬跨(秒级)与跛行行走段; 多尺度金字塔利于同时覆盖秒级爬跨与分钟级跛行; 可在回归头并联跛行 1-5 序数评分头做\"定位+评分\"多任务; 长尾稀疏下加 focal loss 提爬跨召回; domain_scope=cv-时序动作"
  maturity: "主流(当前 TAL 最常用强基线/SOTA 起点)"
```

```yaml
- method_name: "BMN(Boundary-Matching Network)"
  task_type: "时序动作 proposal 生成(两阶段 TAL 的第一阶段)"
  input_data: "长视频片段特征序列(常用 TSN 双流特征)"
  output_result: "边界概率序列 + 边界匹配置信度图(BM map, 枚举所有 起点×时长 组合的 proposal 置信度)"
  core_assumption: "用\"边界匹配机制\"把每个候选 proposal 的起点与终点配对, 在一张二维 BM 置信图上端到端、密集、并行地评估所有 (start, duration) 组合的置信度"
  advantages: "端到端生成高质量稠密 proposal、召回率高、BM 置信图可并行计算、长期作 ActivityNet proposal 阶段标配、与下游分类器解耦灵活"
  limitations: "两阶段(需额外分类头给 proposal 打类别)、BM 图随时序长度二次增长、对超长视频内存吃紧、边界精度受特征分辨率限制"
  common_baselines: "BSN、TURN、CTAP、G-TAD"
  evaluation_metrics: "AR@AN(平均召回@提案数)、AUC(proposal)、配下游分类后 mAP@tIoU"
  suitable_datasets: "ActivityNet-1.3、THUMOS14(人体, 奶山羊须自建)"
  implementation_repo: "JJBOY/BMN-Boundary-Matching-Network、mmaction2(含 BMN 配置)"
  representative_papers:
    - "BMN: Boundary-Matching Network for Temporal Action Proposal Generation | 2019 | cited:623 | doi:10.1109/iccv.2019.00399 | checked:2026-06-06"
  possible_innovation_points: "奶山羊发情爬跨正样本极稀疏, BMN 高召回密集 proposal 利于\"宁可多召回再筛\"; 可作 ActionFormer 之外的两阶段对照; BM 置信图思路可改造为对周期性跛行步态的区间枚举; 提案阶段加类不可知设计降低长尾偏置; domain_scope=cv-时序动作"
  maturity: "主流/经典(proposal 生成奠基, 仍是常用召回基线)"
```

```yaml
- method_name: "BSN(Boundary-Sensitive Network)"
  task_type: "时序动作 proposal 生成"
  input_data: "长视频片段特征序列(TSN 双流特征)"
  output_result: "起点/终点/动作性三条概率序列 → 局部组合候选 proposal → proposal-level 置信度评估"
  core_assumption: "\"局部到全局\"——先用边界敏感分支逐时刻预测起点、终点、actionness 概率, 在高概率处局部组合成 proposal, 再对每个 proposal 评估置信度"
  advantages: "边界灵活精确(不受固定 anchor 限制)、proposal 质量高、是 BMN 的前身奠基工作、模块清晰"
  limitations: "多阶段流水线(边界生成+组合+评估分离)、非完全端到端、组合步骤启发式、被 BMN/端到端方法在效率与精度上超越"
  common_baselines: "TURN、TAG、CTAP"
  evaluation_metrics: "AR@AN、AUC(proposal)、配分类后 mAP@tIoU"
  suitable_datasets: "ActivityNet-1.3、THUMOS14(人体, 奶山羊须自建)"
  implementation_repo: "wzmsltw/BSN-boundary-sensitive-network、mmaction2"
  representative_papers:
    - "BSN: Boundary Sensitive Network for Temporal Action Proposal Generation | 2018 | cited:757 | doi:10.1007/978-3-030-01225-0_1 | checked:2026-06-06"
  possible_innovation_points: "边界敏感分支适合定位爬跨这种边界明确的瞬时事件起止; 作历史基线与消融对照价值大于直接部署; actionness 序列可迁移为\"是否处于异常步态\"的逐帧打分; domain_scope=cv-时序动作"
  maturity: "经典(proposal 生成开创性工作, 现多作基线, 实际部署优先 BMN/ActionFormer)"
```

```yaml
- method_name: "G-TAD(Sub-Graph Localization)"
  task_type: "时序动作检测/定位(图卷积建模时序上下文)"
  input_data: "长视频片段特征序列(节点=时序片段)"
  output_result: "sub-graph 形式的动作 proposal + 类别/边界"
  core_assumption: "把视频片段建成图, 用图卷积聚合多层级时序上下文与语义关系, 将动作检测转化为图中的子图定位问题"
  advantages: "显式建模片段间长程语义关系、上下文聚合强、在 ActivityNet/THUMOS 上一度领先、为 TAL 引入图视角"
  limitations: "图构建与 GCN 增加复杂度、依赖预提取特征、被后续 Transformer 单阶段方法在精度/简洁性上超越、超长视频图规模大"
  common_baselines: "BMN、BSN、P-GCN、TadTR"
  evaluation_metrics: "mAP@tIoU、AR@AN"
  suitable_datasets: "ActivityNet-1.3、THUMOS14(人体, 奶山羊须自建)"
  implementation_repo: "frostinassiky/gtad(官方)、mmaction2(部分支持)"
  representative_papers:
    - "G-TAD: Sub-Graph Localization for Temporal Action Detection | 2020 | cited:466 | doi:10.1109/cvpr42600.2020.01017 | checked:2026-06-06"
  possible_innovation_points: "图视角可建模奶山羊跛行步态周期内\"支撑相-摆动相\"片段间关系, 或群养多目标的时序-空间联合图; 但实现重, 优先级低于 ActionFormer; 适合做\"时序上下文是否有用\"的方法对照; domain_scope=cv-时序动作"
  maturity: "主流→趋稳(图卷积 TAL 代表作, 现多作对比基线)"
```

```yaml
- method_name: "TadTR(End-to-End Temporal Action Detection Transformer)"
  task_type: "时序动作检测/定位(端到端, DETR 式 set prediction)"
  input_data: "长视频片段特征序列"
  output_result: "一组动作 query 直接预测 (起止时刻, 类别), 无需 NMS 后处理"
  core_assumption: "借鉴 DETR, 用可学习 action query 与时序可变形注意力, 把 TAL 当作集合预测(set prediction)端到端求解, 二分匹配监督"
  advantages: "真正端到端、免 anchor 免 NMS、超参少、时序可变形注意力聚焦关键片段、推理简洁"
  limitations: "query 数量上限制约密集/超多实例场景、训练收敛较慢(DETR 通病)、对预提取特征仍敏感、极稀疏长尾下匹配不稳定"
  common_baselines: "BMN、G-TAD、A2Net、ActionFormer"
  evaluation_metrics: "mAP@tIoU、Average-mAP"
  suitable_datasets: "THUMOS14、ActivityNet-1.3、HACS(人体, 奶山羊须自建)"
  implementation_repo: "xlliu7/TadTR(官方)"
  representative_papers:
    - "End-to-End Temporal Action Detection With Transformer (TadTR) | 2022 | cited:260 | doi:10.1109/tip.2022.3195321 | checked:2026-06-06"
  possible_innovation_points: "免 NMS 对奶山羊稀疏事件友好(无需调 NMS 阈值); action query 可显式对应\"爬跨\"\"跛行段\"等少数语义槽; query 数与长尾匹配是难点, 可改进匹配代价加入序数评分项实现\"定位即评分\"; domain_scope=cv-时序动作"
  maturity: "主流(端到端 DETR 式 TAL 代表, 简化流水线)"
```

```yaml
- method_name: "A2Net(Anchor-based + Anchor-free 联合)"
  task_type: "时序动作检测/定位"
  input_data: "长视频片段特征序列"
  output_result: "anchor-based 分支(预设时长 anchor 回归) + anchor-free 分支(逐时刻预测到边界距离)联合输出动作起止+类别"
  core_assumption: "anchor-based 与 anchor-free 两类机制互补——前者对常见时长稳健, 后者对任意/极端时长灵活, 联合训练取长补短"
  advantages: "兼顾固定与任意时长动作、对时长分布多样的数据集鲁棒、揭示两类机制互补性、单阶段"
  limitations: "双分支增加设计与调参、依赖预提取特征、整体精度被 ActionFormer/TriDet 超越、anchor 设计仍需先验"
  common_baselines: "BMN、G-TAD、GTAN、BSN"
  evaluation_metrics: "mAP@tIoU(THUMOS14 0.3:0.7)"
  suitable_datasets: "THUMOS14、ActivityNet-1.3(人体, 奶山羊须自建)"
  implementation_repo: "VividLe/A2Net(官方)"
  representative_papers:
    - "Revisiting Anchor Mechanisms for Temporal Action Localization (A2Net) | 2020 | cited:205 | doi:10.1109/tip.2020.3016486 | checked:2026-06-06"
  possible_innovation_points: "奶山羊事件时长差异极大(爬跨秒级 vs 跛行分钟级), anchor-free 分支专攻短瞬时爬跨、anchor-based 分支稳态覆盖周期跛行段, 天然契合双时长场景; 可作\"是否需双机制\"的消融对照; domain_scope=cv-时序动作"
  maturity: "主流→趋稳(anchor-free/based 互补思想代表作)"
```

```yaml
- method_name: "TriDet(Relative Boundary Modeling)"
  task_type: "时序动作检测/定位(单阶段)"
  input_data: "长视频片段特征序列"
  output_result: "动作起止时刻 + 类别(用相对边界 + Trident-head 建模边界)"
  core_assumption: "直接回归绝对边界对模糊/渐变边界不稳, 改用\"相对边界建模\"(Trident-head 估计边界相对当前时刻的分布)并用 SGP 层替代自注意力建模时序"
  advantages: "边界建模更鲁棒(对模糊边界友好)、SGP 层高效(规避自注意力开销)、在 THUMOS14/ActivityNet/EPIC 上超越 ActionFormer、精度-效率平衡好"
  limitations: "仍依赖预提取特征、相对边界头实现稍复杂、对极稀疏样本召回仍受限"
  common_baselines: "ActionFormer、BMN、G-TAD、TadTR"
  evaluation_metrics: "mAP@tIoU、Average-mAP"
  suitable_datasets: "THUMOS14、ActivityNet-1.3、EPIC-Kitchens-100、HACS(人体, 奶山羊须自建)"
  implementation_repo: "dingfengshi/TriDet(官方)、mmaction2(部分)"
  representative_papers:
    - "TriDet: Temporal Action Detection with Relative Boundary Modeling | 2023 | cited:180 | doi:10.1109/cvpr52729.2023.01808 | checked:2026-06-06"
  possible_innovation_points: "跛行步态起止边界本就模糊(逐渐变跛), TriDet 相对边界建模天然适配这种渐变边界; SGP 高效层利于边缘部署长视频; 推荐与 ActionFormer 并列作主力候选与互相对照; domain_scope=cv-时序动作"
  maturity: "新兴/主流(2023 SOTA 级, 边界建模新思路)"
```

```yaml
- method_name: "TemporalMaxer"
  task_type: "时序动作检测/定位(极简单阶段)"
  input_data: "长视频片段特征序列"
  output_result: "动作起止时刻 + 类别"
  core_assumption: "强大的预提取特征已含足够时序语义, 仅用最大池化(max pooling)做时序上下文聚合即可, 无需复杂自注意力/图/卷积时序模块"
  advantages: "极其轻量(仅 max pooling)、参数与算力远低于 Transformer 类、却在 THUMOS14/MUSES/EPIC 上达到甚至超过复杂模型、训练快、易部署"
  limitations: "强依赖上游特征质量(特征弱则上限低)、max pooling 丢失细粒度时序结构、对需精细时序推理的任务可能不足"
  common_baselines: "ActionFormer、TriDet、BMN、G-TAD"
  evaluation_metrics: "mAP@tIoU、Average-mAP"
  suitable_datasets: "THUMOS14、MUSES、EPIC-Kitchens-100、ActivityNet(人体, 奶山羊须自建)"
  implementation_repo: "TuanTNG/TemporalMaxer(官方)"
  representative_papers:
    - "TemporalMaxer: Maximize Temporal Context with only Max Pooling for Temporal Action Localization | 2023 | cited:22 | doi:10.48550/arxiv.2303.09055 | checked:2026-06-06"
  possible_innovation_points: "奶山羊农场算力受限/边缘盒子部署的首选轻量基线; 验证\"在好特征(VideoMAE 微调)上简单聚合是否够用\"的高性价比方案; 若 max pooling 丢失跛行周期细节, 可作为\"复杂时序模块是否必要\"的下界对照; domain_scope=cv-时序动作"
  maturity: "新兴(2023, 极简高效路线代表)"
```

```yaml
- method_name: "ActionMamba / Video Mamba Suite(状态空间模型时序定位)"
  task_type: "时序动作检测/定位 + 视频理解(状态空间 SSM 骨干)"
  input_data: "长视频片段特征序列(可超长)"
  output_result: "动作起止时刻 + 类别(用 Mamba/S6 选择性状态空间替代 Transformer 时序建模)"
  core_assumption: "选择性状态空间模型(Mamba/S6)以线性复杂度建模长序列, 在 TAL 时序维上替代二次复杂度的自注意力, 兼顾长程依赖与效率"
  advantages: "线性复杂度(对超长视频友好)、长程时序依赖建模强、Video Mamba Suite 系统验证 SSM 在多视频任务(含 TAL)的通用性、ActionMamba 在 TAL 上达 SOTA 级"
  limitations: "新兴方法生态/预训练权重不如 Transformer 成熟、SSM 训练稳定性与超参经验少、硬件 kernel 依赖、长期泛化待更多验证"
  common_baselines: "ActionFormer、TriDet、TadTR"
  evaluation_metrics: "mAP@tIoU、Average-mAP"
  suitable_datasets: "THUMOS14、ActivityNet-1.3、EPIC-Kitchens-100、FineAction(人体, 奶山羊须自建)"
  implementation_repo: "OpenGVLab/video-mamba-suite(官方, 含 ActionMamba TAL 分支)"
  representative_papers:
    - "Video Mamba Suite: State Space Model as a Versatile Alternative for Video Understanding | 2024 | cited:19 | doi:10.48550/arxiv.2403.09626 | checked:2026-06-06"
    - "Enhancing Temporal Action Localization: Advanced S6 Modeling with Recurrent Mechanism | 2024 | cited:1 | doi:10.48550/arxiv.2407.13078 | checked:2026-06-06"
  possible_innovation_points: "奶山羊监控常是数小时连续长视频, Mamba 线性复杂度直接利好\"全天候不切片定位\"; 跛行是分钟级长周期步态, SSM 长程依赖适配周期建模; 作为前沿点可探索\"SSM 时序骨干 + 序数评分头\"的奶山羊定制结构, 创新性高; domain_scope=cv-时序动作"
  maturity: "新兴(2024 前沿, 生态成长中, 适合做创新基础)"
```

---

## 二、序数回归 / 有序标签损失 + 评测指标方法卡

```yaml
- method_name: "CORAL(COnsistent RAnk Logits, 秩一致序数回归)"
  task_type: "序数回归(有序多级标签预测, 如评分 1-5)"
  input_data: "特征(图像/视频/向量)+ 有序类别标签 k∈{1..K}"
  output_result: "K-1 个二分类输出 P(y>1)...P(y>K-1), 阈值求和得序数预测等级"
  core_assumption: "把 K 级序数标签转成 K-1 个\"是否大于第 k 级\"的二分类任务; 通过共享权重+独立偏置, 强制各二分类阈值单调一致(rank-consistent), 保证 P(y>k) 随 k 单调不增"
  advantages: "显式保证秩单调一致(不会出现 P(y>2)>P(y>1) 的矛盾)、考虑标签有序性、实现简单可接在任意骨干后、年龄估计等任务上优于普通分类/回归"
  limitations: "共享权重的单调约束限制表达力(各阈值不能独立学复杂决策面)、对极不平衡序数分布仍需配重采样、假设类间序数等距性较弱时优势有限"
  common_baselines: "普通多分类(softmax+CE)、标准回归(MSE)、OR-CNN(Niu 2016)"
  evaluation_metrics: "MAE(序数)、QWK、Accuracy、RMSE"
  suitable_datasets: "MORPH-2/AFAD/CACD(年龄估计, 人脸)、任意有序评分任务(奶山羊跛行评分须自建)"
  implementation_repo: "Raschka-research-group/coral-cnn(官方)、coral-pytorch(库)"
  representative_papers:
    - "Rank consistent ordinal regression for neural networks with application to age estimation (CORAL) | 2020 | cited:288 | doi:10.1016/j.patrec.2020.11.008 | checked:2026-06-06"
  possible_innovation_points: "奶山羊跛行 locomotion score 1-5 有序且相邻级易混, CORAL 接在 TAL 定位出的步态区间特征后做评分头, 保证\"评分单调不矛盾\"; 比普通 5 分类更契合\"错判相邻级代价小、跨级代价大\"; 长尾(多数为 1-2 级正常)下需配重加权; domain_scope=cv-时序动作"
  maturity: "主流(深度序数回归常用强基线, 秩一致经典实现)"
```

```yaml
- method_name: "CORN(Conditional Ordinal Regression for Neural networks)"
  task_type: "序数回归(有序多级标签预测)"
  input_data: "特征 + 有序类别标签 k∈{1..K}"
  output_result: "K-1 个条件概率 P(y>k | y>k-1), 链式相乘得各等级概率与序数预测"
  core_assumption: "CORAL 用共享权重保证秩一致但限制表达力; CORN 改用\"条件概率链式分解\"(基于条件训练子集), 无需共享权重即可保证秩一致, 放松约束、提升灵活性"
  advantages: "保留秩一致性的同时不强制共享权重(表达力强于 CORAL)、条件概率分解理论清晰、年龄/序数任务上常优于 CORAL、可接任意骨干"
  limitations: "条件子集训练使各 rank 的有效样本递减(高 rank 数据更少, 长尾更敏感)、实现略复杂于 CORAL、对极少样本等级估计不稳"
  common_baselines: "CORAL、OR-CNN、普通分类/回归"
  evaluation_metrics: "MAE(序数)、QWK、Accuracy、RMSE"
  suitable_datasets: "MORPH-2/AFAD/CACD(年龄估计)、有序评分任务(奶山羊跛行评分须自建)"
  implementation_repo: "Raschka-research-group/corn-ordinal-neuralnet(官方)、coral-pytorch(库, 含 CORN)"
  representative_papers:
    - "Deep neural networks for rank-consistent ordinal regression based on conditional probabilities (CORN) | 2023 | cited:72 | doi:10.1007/s10044-023-01181-9 | checked:2026-06-06"
    - "(预印本) Deep Neural Networks for Rank-Consistent Ordinal Regression Based On Conditional Probabilities | 2021 | cited:6 | doi:10.48550/arxiv.2111.08851 | checked:2026-06-06"
  possible_innovation_points: "跛行评分头优先候选(表达力优于 CORAL); 但条件子集训练加剧高分级(重度跛行)样本稀缺问题, 需结合重采样/过采样或与 CORAL 对照取稳; 可探索 CORN 头 + Mamba/ActionFormer 时序特征的联合\"定位+评分\"端到端结构; domain_scope=cv-时序动作"
  maturity: "主流/新兴(CORAL 的改进版, 秩一致序数回归当前推荐之一)"
```

```yaml
- method_name: "序数回归综述与方法体系(Ordinal Regression Survey)"
  task_type: "序数回归方法学梳理(理论框架/方法分类/评测)"
  input_data: "有序类别标签数据(评分/等级/分级)"
  output_result: "序数回归三大范式梳理——naive 化简法、序数二分解法(如 OR-CNN/CORAL/CORN)、阈值模型(如有序 logit/probit、SVOR)"
  core_assumption: "序数标签介于名义分类与数值回归之间——有序但类间距离未知; 直接分类丢序、直接回归假等距, 均不最优; 应有专门方法显式利用\"有序但非等距\"结构"
  advantages: "系统厘清方法谱系与适用边界、提供统一评测协议(MAE/MZE/QWK)、是选型与写 related work 的权威依据、含传统与早期深度方法对比"
  limitations: "综述本身非可运行方法(需落到具体模型)、2015 版未覆盖近年深度序数(CORN/序数化分布学习)、传统方法在高维视频特征上需替换为深度骨干"
  common_baselines: "SVOR(支持向量序数回归)、有序逻辑回归(proportional odds)、高斯过程序数回归"
  evaluation_metrics: "MAE、MZE(平均零一误差)、QWK、Spearman/Kendall 相关"
  suitable_datasets: "UCI 序数基准、问卷/分级评分数据(奶山羊跛行评分须自建)"
  implementation_repo: "ayrna/orca(MATLAB 序数回归算法集)、statsmodels(有序 logit, Python)"
  representative_papers:
    - "Ordinal Regression Methods: Survey and Experimental Study | 2015 | cited:459 | doi:10.1109/tkde.2015.2457911 | checked:2026-06-06"
    - "Deep Ordinal Regression Network for Monocular Depth Estimation (DORN, 序数化深度回归代表应用) | 2018 | cited:1907 | doi:10.1109/cvpr.2018.00214 | checked:2026-06-06"
  possible_innovation_points: "为奶山羊跛行评分提供方法选型地图——明确\"5 级评分该用序数法而非分类/回归\"的依据; DORN 把连续深度离散成有序区间用序数回归的思路, 可类比把\"跛行严重度连续谱\"离散为有序级别建模; 写 idea/方案的理论支撑卡; domain_scope=cv-时序动作"
  maturity: "经典(综述权威, 方法体系参考基石)"
```

```yaml
- method_name: "QWK(Quadratic Weighted Kappa, 二次加权 Kappa) — 评测指标"
  task_type: "序数分类/评分一致性评测指标(非模型)"
  input_data: "预测等级序列 + 真值等级序列(K 级有序), 构建 K×K 混淆矩阵"
  output_result: "标量 κ∈(-∞,1]; 1=完全一致, 0=等同随机, 负值=比随机还差"
  core_assumption: "错分代价应随\"预测级与真值级的距离平方\"增长(权重 w_ij=(i-j)^2/(K-1)^2); 并扣除按边缘分布期望的随机一致, 衡量\"超出随机的有序一致程度\""
  advantages: "专为有序标签设计(惩罚跨级大错 >> 相邻小错)、对类别不平衡比 Accuracy 稳健、扣除随机基线、医学评分/糖网分级/作文评分等竞赛标准指标、可解释性好"
  limitations: "对边缘分布敏感(极不平衡时 κ 可能虚高或悖论, 见 Warrens 研究)、单指标掩盖具体错分结构、阈值化连续输出方式影响结果、非可直接优化的损失(需代理)"
  common_baselines: "Accuracy、Macro-F1、Cohen's Kappa(线性加权)、Spearman"
  evaluation_metrics: "自身即指标; 常与 MAE/混淆矩阵并报"
  suitable_datasets: "任意有序评分任务(糖网分级 APTOS、作文评分 ASAP; 奶山羊跛行评分须自建)"
  implementation_repo: "scikit-learn(cohen_kappa_score(weights='quadratic'))、ml-metrics"
  representative_papers:
    - "Weighted kappa: Nominal scale agreement provision for scaled disagreement or partial credit (Cohen 加权 Kappa 原始定义) | 1968 | cited:8510 | doi:10.1037/h0026256 | checked:2026-06-06"
    - "Some Paradoxical Results for the Quadratically Weighted Kappa | 2012 | cited:52 | doi:10.1007/s11336-012-9258-4 | checked:2026-06-06"
  possible_innovation_points: "奶山羊跛行评分应以 QWK 为主指标——把\"1 级误判为 5 级\"重罚、把\"2 误判为 3\"轻罚, 符合兽医诊断实际代价; 正常级(1-2)占多数的长尾下比 Accuracy 可信; 报告时须同时给混淆矩阵防止边缘分布悖论误读; domain_scope=cv-时序动作"
  maturity: "经典(有序评分评测金标准指标)"
```

```yaml
- method_name: "MAE-ordinal / MZE(序数平均绝对误差与平均零一误差) — 评测指标"
  task_type: "序数回归/评分评测指标(非模型)"
  input_data: "预测等级 + 真值等级(以整数序号表示有序级别)"
  output_result: "MAE=平均 |预测级序号-真值级序号|; MZE=平均误分率(1-Accuracy)"
  core_assumption: "序数级别可用整数序号近似(等距假设), 则预测偏离真值的\"级差绝对值\"是直接、可解释的误差; MZE 衡量是否分对、MAE 衡量分错时错多远, 二者互补"
  advantages: "直观可解释(MAE=0.4 即\"平均差不到半级\")、对有序结构敏感(优于纯 Accuracy)、计算简单、与 QWK 互补(QWK 看一致性、MAE 看平均偏离幅度)、序数回归综述标准报告项"
  limitations: "隐含\"级间等距\"假设(若 1→2 与 4→5 严重度跨度不同则失真)、MAE 对类不平衡敏感(被多数类主导)、不像 QWK 扣随机基线、单独看易误导, 须组合报告"
  common_baselines: "Accuracy、QWK、RMSE、Spearman 相关"
  evaluation_metrics: "自身即指标; 序数任务通常 MAE + QWK + Accuracy 三者并报"
  suitable_datasets: "任意有序评分任务(年龄估计、跛行评分; 奶山羊须自建)"
  implementation_repo: "scikit-learn(mean_absolute_error 配整数标签)、ayrna/orca(含 MAE/MZE/AMAE)"
  representative_papers:
    - "Ordinal Regression Methods: Survey and Experimental Study (定义并系统使用 MAE/MZE/AMAE 评测) | 2015 | cited:459 | doi:10.1109/tkde.2015.2457911 | checked:2026-06-06"
  possible_innovation_points: "奶山羊跛行评分用 MAE 报\"平均评分偏差\"对兽医直观(差半级 vs 差两级一目了然); 但 1-5 级严重度未必等距(轻跛到中跛 vs 重跛到卧地跨度不同), 建议报 AMAE(各类 MAE 宏平均)抵消长尾, 并与 QWK 联合; 提醒勿单用 MAE 下结论; domain_scope=cv-时序动作"
  maturity: "经典(序数评测标准辅助指标, 须与 QWK 组合使用)"
```

---

## 维护备注

- 本文件 14 张卡：TAL 9 张（ActionFormer/BMN/BSN/G-TAD/TadTR/A2Net/TriDet/TemporalMaxer/ActionMamba）+ 序数回归 5 张（CORAL/CORN/序数回归综述/QWK/MAE-ordinal）。
- 所有 representative_papers 的标题/年份/被引/DOI 均由 `curl https://api.openalex.org/works?search=...&mailto=light@example.com` 实拉（2026-06-06）。同一论文存在会议版与 arXiv 预印本双记录、被引分散的，已就近标注；查不到独立 DOI 的（如部分预印本/分散记录）写明情况。
- ActionFormer 的 OpenAlex 该 LNCS/ECCV 条目未直接返回 cited_by_count（relevance_score≈2112，被引高但记录分散），已诚实标注「重/relevance≈2112」而非臆造具体被引数。
- 与 cards_action_spatiotemporal.md（trimmed-clip 分类）互补：那边做"是什么行为"，这边做"何时发生 + 多严重"。奶山羊典型流水线：长视频 → 特征提取(VideoMAE/SlowFast) → TAL 定位(ActionFormer/TriDet/ActionMamba) → 区间送序数评分头(CORAL/CORN) → QWK/MAE 评测。


