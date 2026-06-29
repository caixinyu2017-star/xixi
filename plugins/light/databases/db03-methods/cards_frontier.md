# db03 方法卡 — 前沿 / 新兴方法（_new_frontier.md）

> 续作入口：本文件补充 cards_dl.md 之外的前沿/新兴方法卡，共 25 张，覆盖自监督、对比学习、元学习、持续学习、NAS/AutoML、蒸馏/剪枝/量化、LLM/指令微调/RLHF/Agent/MoE/状态空间、多模态大模型、因果推断、可解释 AI、神经渲染、图 Transformer、扩散策略、世界模型。RAG canonical 卡已迁移至 `cards_nlp_speech.md`。
> 字段 schema 同 db03：`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`
> `maturity`: 经典 | 主流 | 新兴 | 过时 | 不推荐
>
> **核查口径（务必遵守）**：representative_papers 的 标题/年份/被引/DOI 均来自 OpenAlex API 真实 curl（`https://api.openalex.org/works`，mailto 礼貌池），查询日期 **2026-06-06**，被引数为当日快照、随时间增长。implementation_repo 为真实公开仓库，已用 GitHub API 核 HTTP 状态。maturity / possible_innovation_points 为人工领域判断。
> **付费墙诚实声明**：Clarivate JCR 影响因子、Scimago SJR 等付费指标本卡一律不出现（免费源不可得）；本库不涉及期刊指标，仅用 OpenAlex 被引作为可核查热度替代。查不到/记录异常的写「待核查」并说明，绝不臆造。

## 方法卡

```yaml
- method_name: 自监督表示学习 — 动量对比(MoCo)
  task_type: 无标注视觉表示学习(下游分类/检测/分割迁移)
  input_data: 无标注图像 + 两路数据增广视图
  output_result: 可迁移的视觉特征编码器(backbone)
  core_assumption: 把对比学习看作字典查询；用动量更新的键编码器维护一个大且一致的负样本队列，使正样本(同图两视图)相近、与队列中负样本相远
  advantages: 解耦 batch 大小与负样本数(队列)、无需超大 batch、迁移到检测/分割超过有监督预训练、实现成熟
  limitations: 需调动量系数/队列长度、增广策略敏感、纯实例判别对细粒度语义弱、v3 改用 ViT 后算力上升
  common_baselines: 有监督 ImageNet 预训练、SimCLR、BYOL、SwAV
  evaluation_metrics: 线性探测 Top-1 Acc、下游检测 mAP / 分割 mIoU、k-NN 评估
  suitable_datasets: ImageNet-1k(预训练)、COCO/VOC(下游)、医学/遥感无标注图像
  implementation_repo: facebookresearch/moco (GitHub API 200)
  representative_papers:
    - "Momentum Contrast for Unsupervised Visual Representation Learning (MoCo) | 2019 | cited:1010 | doi:10.48550/arXiv.1911.05722 [被引为 OpenAlex arXiv 记录数值，原文聚合后更高，待核查] | checked:2026-06-06"
  possible_innovation_points: 领域自监督预训练(医学/遥感/工业缺陷)、与掩码建模融合(对比+重构)、视频/多模态队列、小数据高效自监督; domain_scope=前沿ML
  maturity: 主流(自监督视觉的经典强基线，常作下游迁移起点)

- method_name: 自监督表示学习 — 无负样本自蒸馏(BYOL)
  task_type: 无标注视觉表示学习
  input_data: 无标注图像 + 两路增广视图
  output_result: 可迁移视觉编码器
  core_assumption: 不需要负样本；在线网络预测目标网络(动量更新)的表示，配合预测头与停梯度防止表示坍塌
  advantages: 无需负样本/大队列、对 batch 大小更鲁棒、表示质量高、避免负样本采样偏差
  limitations: 坍塌机理依赖 BN/预测头等工程细节、理论解释仍在讨论、对增广仍敏感
  common_baselines: SimCLR、MoCo、SimSiam、SwAV
  evaluation_metrics: 线性探测 Top-1 Acc、半监督微调、下游迁移
  suitable_datasets: ImageNet-1k、下游视觉任务
  implementation_repo: lucidrains/byol-pytorch (GitHub API 200)；官方 deepmind 实现
  representative_papers:
    - "Bootstrap your own latent: A new approach to self-supervised Learning (BYOL) | 2020 | cited:3445 | doi:10.48550/arXiv.2006.07733 | checked:2026-06-06"
  possible_innovation_points: 坍塌的理论刻画、跨模态 BYOL、轻量自蒸馏、与掩码自编码结合、领域迁移; domain_scope=前沿ML
  maturity: 主流(自监督无负样本路线的代表)

- method_name: 自监督表示学习 — 掩码图像建模(MAE)
  task_type: 视觉自监督预训练(ViT backbone)
  input_data: 无标注图像，随机掩码大比例(约75%) patch
  output_result: 预训练 ViT 编码器(下游微调)
  core_assumption: 图像高度冗余，掩码大部分 patch 后用非对称编码-解码重构像素，迫使模型学语义结构；编码器只看可见 patch 故高效
  advantages: 训练高效(只编码可见 patch)、可扩展到大模型、微调下游强、概念简单
  limitations: 线性探测弱于对比方法、重构像素非语义目标、主要适配 ViT、需较大数据/算力发挥
  common_baselines: 有监督 ViT、对比自监督(MoCo v3/DINO)、BEiT
  evaluation_metrics: 微调 Top-1 Acc、下游检测/分割、线性探测
  suitable_datasets: ImageNet-1k/21k、下游视觉任务
  implementation_repo: facebookresearch/mae (GitHub API 200)
  representative_papers:
    - "Masked Autoencoders Are Scalable Vision Learners (MAE) | 2021 | cited:195 | doi:10.48550/arXiv.2111.06377 [被引为 OpenAlex arXiv 记录数值；该论文存在多条拆分/合并记录，原文真实被引远高于此，待核查] | checked:2026-06-06"
  possible_innovation_points: 多模态掩码建模(音视频/点云)、掩码+对比联合目标、领域 MAE(医学/遥感)、高效解码与目标设计; domain_scope=前沿ML
  maturity: 主流(掩码视觉建模主线方法之一)

- method_name: 对比学习通用框架(InfoNCE / CPC)
  task_type: 自监督/表示学习的通用对比目标(图像/语音/文本/序列)
  input_data: 成对或多视图样本(锚-正-负)
  output_result: 判别性表示编码器
  core_assumption: 通过 InfoNCE 损失最大化正样本对的互信息下界，使表示能从负样本中区分正样本(预测编码)
  advantages: 通用、理论与互信息相连、可跨模态、构成 SimCLR/MoCo/CLIP 等方法的损失核心
  limitations: 依赖负样本质量与数量、增广/采样策略敏感、互信息下界与表示质量非严格对应
  common_baselines: 自编码、生成式预训练、三元组损失
  evaluation_metrics: 线性探测、下游迁移、检索 Recall@K
  suitable_datasets: ImageNet、LibriSpeech(语音)、各序列数据
  implementation_repo: facebookresearch/moco、google-research/simclr(GitHub API 000=网络瞬时，仓库公开存在)
  representative_papers:
    - "Representation Learning with Contrastive Predictive Coding (CPC, InfoNCE) | 2018 | cited:4526 | doi:10.48550/arXiv.1807.03748 | checked:2026-06-06"
  possible_innovation_points: 难负样本挖掘、去偏对比、跨模态对比对齐、监督对比(SupCon)、与生成式目标融合; domain_scope=前沿ML
  maturity: 主流(对比学习的理论与损失基石)
```

```yaml
- method_name: 元学习 — 模型无关元学习(MAML)
  task_type: 少样本学习(few-shot 分类/回归/RL 快速适应)
  input_data: 多任务分布上的小样本支持集/查询集
  output_result: 一组对新任务"易微调"的初始化参数
  core_assumption: 存在一组初始参数，使其在任意新任务上经少量梯度步即可快速适应；通过二阶梯度优化"适应后性能"
  advantages: 模型无关(适配任意可微模型与任务)、少样本快速适应、思想通用
  limitations: 二阶梯度算力/显存高(常用一阶近似 FOMAML)、对任务分布敏感、训练不稳定、深网难扩展
  common_baselines: 预训练+微调、Prototypical/Matching Net、Reptile、迁移学习
  evaluation_metrics: N-way K-shot 准确率、适应步数、回归 MSE
  suitable_datasets: Omniglot、miniImageNet、Meta-Dataset、少样本 RL 任务
  implementation_repo: cbfinn/maml (GitHub API 200)；learn2learn 库
  representative_papers:
    - "Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks (MAML) | 2017 | cited:5791 | doi:10.48550/arXiv.1703.03400 | checked:2026-06-06"
  possible_innovation_points: 与大模型 in-context learning 对比/融合、领域少样本(医学/工业)、一阶高效近似、元学习做超参/损失/数据增广搜索; domain_scope=前沿ML
  maturity: 主流(少样本元学习经典方法；近年部分场景被大模型 ICL 替代)

- method_name: 持续/增量学习(克服灾难性遗忘，EWC 等)
  task_type: 任务/类别序列上的持续学习，避免遗忘旧知识
  input_data: 按时间到达的任务序列(旧数据不可或受限访问)
  output_result: 在新旧任务上均保持性能的单一模型
  core_assumption: 用 Fisher 信息衡量参数对旧任务的重要性，对重要参数施加二次惩罚(EWC)以保护旧知识，同时学习新任务
  advantages: 缓解灾难性遗忘、无需存全部旧数据(正则化类)、贴近真实数据流场景
  limitations: 长任务序列下仍累积遗忘、任务边界/身份常需已知、正则与回放各有局限、可塑性-稳定性权衡难
  common_baselines: 微调(下界)、联合训练(上界)、经验回放(Replay)、LwF、iCaRL
  evaluation_metrics: 平均准确率、遗忘率(BWT)、前向迁移(FWT)
  suitable_datasets: Split-MNIST/CIFAR、Permuted-MNIST、CORe50、CLEAR
  implementation_repo: GMvandeVen/continual-learning、ContinualAI/avalanche
  representative_papers:
    - "Overcoming catastrophic forgetting in neural networks (EWC) | 2017 | cited:7078 | doi:10.1073/pnas.1611835114 | checked:2026-06-06"
  possible_innovation_points: 大模型/LoRA 的持续学习、无样本回放(生成式回放)、预训练表示下的持续学习、参数隔离与扩展、在线/流式持续学习; domain_scope=前沿ML
  maturity: 主流(持续学习的经典正则化代表，仍是常用强基线)

- method_name: 神经架构搜索 — 可微分搜索(DARTS)
  task_type: 自动搜索神经网络结构(分类/分割等)
  input_data: 搜索空间(候选算子) + 训练数据
  output_result: 搜索得到的网络结构(cell)及其权重
  core_assumption: 将离散架构选择松弛为连续可微的算子权重(softmax 混合)，用梯度下降联合优化架构与权重，再离散化
  advantages: 比强化学习/进化搜索快几个数量级(GPU 天级)、端到端可微、可复用搜索 cell
  limitations: 显存占用大(需载入全部候选)、易坍塌到 skip-connect、搜索-评估鸿沟、稳定性/复现性差
  common_baselines: 随机搜索、强化学习 NAS(NASNet)、进化 NAS(AmoebaNet)、ENAS
  evaluation_metrics: 搜索得网络的 Top-1 Acc、搜索代价(GPU-days)、参数量/FLOPs
  suitable_datasets: CIFAR-10(搜索)、ImageNet(迁移)、NAS-Bench-201
  implementation_repo: quark0/darts (GitHub API 200)
  representative_papers:
    - "DARTS: Differentiable Architecture Search | 2018 | cited:1402 | doi:10.48550/arXiv.1806.09055 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
  possible_innovation_points: 缓解坍塌(DARTS+/Fair DARTS/PC-DARTS)、零样本/免训练 NAS、硬件感知搜索、为 Transformer/大模型搜结构、与 AutoML 流水线集成; domain_scope=前沿ML
  maturity: 新兴主流(NAS 主流路线之一；纯分类 SOTA 多靠人工设计+缩放，NAS 在受限/硬件感知场景价值高)

- method_name: 自动化机器学习(AutoML / auto-sklearn)
  task_type: 自动完成模型选择、超参优化与特征/管道构建
  input_data: 表格/结构化数据 + 任务定义(分类/回归)
  output_result: 自动构建并集成的机器学习管道
  core_assumption: 模型+超参+预处理构成可搜索的联合空间(CASH 问题)，可用贝叶斯优化+元学习热启动+集成自动求解
  advantages: 降低建模门槛、自动化调参省人力、元学习热启动快、自动集成稳健
  limitations: 大搜索空间计算开销大、深度/非结构化数据上不及专门设计、可解释性弱、易过拟合验证集
  common_baselines: 人工调参、网格/随机搜索、单一 GBDT(XGBoost/LightGBM)、TPOT/H2O
  evaluation_metrics: 任务指标(Acc/AUC/RMSE)、达标所需时间/算力、跨数据集稳健性
  suitable_datasets: OpenML-CC18、AutoML Benchmark、各类表格数据
  implementation_repo: automl/auto-sklearn (GitHub API 200)
  representative_papers:
    - "Efficient and robust automated machine learning (auto-sklearn) | 2015 | cited:1259 | doi:待核查(OpenAlex 该 NeurIPS 2015 记录 DOI 字段为 null) | checked:2026-06-06"
  possible_innovation_points: LLM 驱动的 AutoML(自动写管道/解释)、面向深度学习/大模型的 AutoML、绿色/低碳搜索、自动特征工程、可解释 AutoML; domain_scope=前沿ML
  maturity: 主流(表格数据自动建模常用；深度/大模型场景仍在发展)

- method_name: 知识蒸馏(Knowledge Distillation)
  task_type: 模型压缩与能力迁移(大教师→小学生)
  input_data: 教师模型输出(软标签/中间特征) + 训练数据
  output_result: 性能接近教师的小型/高效学生模型
  core_assumption: 教师的软概率分布含类间相似性"暗知识"，用带温度的 KL 散度让学生匹配软标签，比硬标签学到更多
  advantages: 显著压缩模型/加速推理、可跨架构、可结合剪枝量化、广泛用于部署与大模型小型化
  limitations: 依赖强教师、师生容量差距过大时收益降、温度/权重需调、特征蒸馏需对齐设计
  common_baselines: 直接训练小模型、剪枝、量化、教师集成
  evaluation_metrics: 学生精度 vs 教师、压缩比/加速比、参数量/FLOPs
  suitable_datasets: ImageNet、CIFAR、GLUE(BERT 蒸馏)、各下游任务
  implementation_repo: huggingface/transformers(DistilBERT)、各蒸馏库
  representative_papers:
    - "Distilling the Knowledge in a Neural Network | 2015 | cited:13952 | doi:10.48550/arXiv.1503.02531 | checked:2026-06-06"
  possible_innovation_points: LLM 蒸馏(白盒/黑盒、推理链蒸馏)、数据无关蒸馏、自蒸馏、跨模态蒸馏、与量化联合压缩; domain_scope=前沿ML
  maturity: 主流(模型压缩与大模型小型化的核心手段)
```

```yaml
- method_name: 网络剪枝(Pruning)
  task_type: 模型压缩(去除冗余权重/通道)
  input_data: 已训练模型 + 训练数据(微调用)
  output_result: 稀疏或更窄的高效模型
  core_assumption: 训练好的网络存在大量冗余连接，按重要性(幅值等)剪除并微调可在小精度损失下显著减小模型(连接学习假设)
  advantages: 减小模型/算力、结构化剪枝可直接加速、与蒸馏量化叠加、思路简单有效
  limitations: 非结构化稀疏需专用硬件/库才提速、剪枝比例与微调需调、迭代剪枝耗时、可能损精度
  common_baselines: 原始稠密模型、量化、蒸馏、低秩分解
  evaluation_metrics: 稀疏度/压缩比、精度保持、实际加速比、FLOPs
  suitable_datasets: ImageNet、CIFAR、各部署任务
  implementation_repo: PyTorch torch.nn.utils.prune；microsoft/nni(剪枝模块)
  representative_papers:
    - "Learning both Weights and Connections for Efficient Neural Networks | 2015 | cited:668 | doi:10.48550/arXiv.1506.02626 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
  possible_innovation_points: 彩票假设(lottery ticket)子网、结构化/硬件感知剪枝、大模型(LLM)剪枝(SparseGPT/Wanda 思路)、训练时稀疏、剪枝+量化+蒸馏联合; domain_scope=前沿ML
  maturity: 主流(模型压缩经典手段；LLM 剪枝为新兴热点)

- method_name: 模型量化(Quantization, 含 LLM.int8)
  task_type: 模型压缩与推理加速(低比特表示权重/激活)
  input_data: 已训练模型(+ 校准数据 / 微调数据)
  output_result: 低比特(int8/int4 等)高效模型
  core_assumption: 浮点权重/激活可用低比特定点近似而精度损失可控；对大模型用混合精度分解处理离群激活(LLM.int8)保持性能
  advantages: 大幅降显存/带宽、加速推理、int8 近无损、是端侧与大模型部署关键技术
  limitations: 激活离群值致精度下降、低比特(<=4bit)需精细方法、需硬件支持、训练后量化(PTQ)与量化感知训练(QAT)权衡
  common_baselines: FP16/BF16、剪枝、蒸馏、PTQ vs QAT
  evaluation_metrics: 精度/困惑度保持、比特宽、显存占用、加速比
  suitable_datasets: ImageNet、LLM 评测(WikiText/MMLU)、部署基准
  implementation_repo: TimDettmers/bitsandbytes、huggingface/transformers(量化集成)
  representative_papers:
    - "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale | 2022 | cited:113 | doi:10.48550/arXiv.2208.07339 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
  possible_innovation_points: 4bit/低比特 LLM(GPTQ/AWQ 思路)、量化感知训练大模型、KV-cache 量化、与 LoRA 结合(QLoRA)、激活量化新方案; domain_scope=前沿ML
  maturity: 主流(大模型/端侧部署的核心压缩技术)

- method_name: 大语言模型(LLM：GPT / LLaMA 系)
  task_type: 通用语言理解与生成、对话、推理、代码、few-shot/zero-shot
  input_data: 海量无标注文本(预训练) + 提示/指令
  output_result: 自回归生成的 token 序列(文本/代码)
  core_assumption: 解码器 Transformer 上做大规模自回归预训练，随参数/数据/算力扩展(scaling law)涌现 in-context learning 与推理能力
  advantages: 通用强、少样本/零样本、统一多任务、可作 Agent/RAG 基座、开源(LLaMA)生态繁荣
  limitations: 训练/推理算力极高、幻觉与事实性、上下文长度与时效限制、对齐与安全风险、评测困难
  common_baselines: BERT 类编码器、T5、早期 GPT-2/3、RNN seq2seq
  evaluation_metrics: MMLU、困惑度、HELM、人类偏好/Arena、代码 pass@k
  suitable_datasets: Common Crawl/RedPajama、The Pile、指令与评测基准
  implementation_repo: meta-llama/llama (facebookresearch/llama 已 301 迁移)、huggingface/transformers
  representative_papers:
    - "LLaMA: Open and Efficient Foundation Language Models | 2023 | cited:3894 | doi:10.48550/arXiv.2302.13971 | checked:2026-06-06"
  possible_innovation_points: 长上下文/高效注意力、推理增强(CoT/工具)、领域/多语言适配、小模型高效化、数据质量与合成、安全对齐; domain_scope=前沿ML
  maturity: 主流(当代 NLP 与通用 AI 主线)

- method_name: 指令微调(Instruction Tuning, FLAN)
  task_type: 让预训练 LLM 遵循自然语言指令、提升零样本泛化
  input_data: 多任务、模板化的指令-响应数据集
  output_result: 能遵循未见任务指令的指令模型
  core_assumption: 把大量任务统一为"指令→输出"格式做多任务微调，可让模型泛化到未见过的新指令(指令泛化)
  advantages: 显著提升零样本/未见任务表现、数据相对易构造、是对齐与可用性的第一步、与 RLHF 互补
  limitations: 依赖指令数据多样性与质量、可能学到表层模式、对复杂偏好对齐不足(需 RLHF/DPO)、易过拟合模板
  common_baselines: 纯预训练模型、单任务微调、in-context few-shot
  evaluation_metrics: 未见任务零样本指标、MMLU/BBH、人类评测
  suitable_datasets: FLAN collection、Super-NaturalInstructions、Alpaca/Dolly
  implementation_repo: google-research/FLAN、huggingface/transformers
  representative_papers:
    - "Finetuned Language Models Are Zero-Shot Learners (FLAN) | 2021 | cited:69 | doi:10.48550/arXiv.2109.01652 [被引为 OpenAlex arXiv 记录数值，原文真实被引远高于此，待核查] | checked:2026-06-06"
  possible_innovation_points: 合成指令数据(self-instruct)、指令数据配比/质量筛选、多模态指令微调、推理链指令、领域指令微调; domain_scope=前沿ML
  maturity: 主流(对齐流程的标准第一阶段)

- method_name: 人类反馈强化学习(RLHF / InstructGPT)
  task_type: 将 LLM 行为对齐到人类偏好(有用/无害/诚实)
  input_data: 人类偏好比较数据 + SFT 模型
  output_result: 与人类偏好对齐的策略模型
  core_assumption: 用人类偏好训练奖励模型，再用 PPO 等 RL 以奖励模型为信号优化 LLM 策略，可对齐难以用监督标签表达的偏好
  advantages: 显著提升有用性/安全性与对话质量、可优化非可微目标、ChatGPT 类产品关键技术
  limitations: 流程复杂(SFT→RM→RL)、PPO 不稳定/调参难、奖励黑客(reward hacking)、标注成本高、易过度对齐
  common_baselines: 纯 SFT、DPO(直接偏好优化)、RLAIF、best-of-n 采样
  evaluation_metrics: 人类偏好胜率、有用/无害评测、Arena Elo、奖励模型准确率
  suitable_datasets: 人类偏好对比集(HH-RLHF)、指令数据
  implementation_repo: huggingface/trl、CarperAI/trlx
  representative_papers:
    - "Training language models to follow instructions with human feedback (InstructGPT) | 2022 | cited:4284 | doi:10.48550/arXiv.2203.02155 | checked:2026-06-06"
    - "Direct Preference Optimization: Your Language Model is Secretly a Reward Model (DPO) | 2023 | cited:275 | doi:10.48550/arXiv.2305.18290 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
  possible_innovation_points: 免 RL 对齐(DPO/IPO/KTO)、AI 反馈(RLAIF/Constitutional)、过程奖励(PRM)、多目标对齐、奖励黑客缓解; domain_scope=前沿ML
  maturity: 主流(LLM 对齐主流；DPO 等简化路线快速兴起)
```

```yaml
- method_name: LLM 智能体(LLM Agent：ReAct / 工具调用)
  task_type: 多步推理 + 工具使用 + 与环境交互的自主任务执行
  input_data: 任务目标 + 可用工具/API + 环境观测
  output_result: 推理-行动轨迹与最终结果(调用工具、检索、执行)
  core_assumption: 让 LLM 交替产生"推理(thought)"与"行动(action)"，用工具/环境反馈(observation)指导下一步，把推理与行动协同(ReAct)以完成复杂任务
  advantages: 突破单次生成局限、可调用外部工具/实时信息、可解释轨迹、组合复杂任务、可与 RAG/记忆结合
  limitations: 易陷错误循环/级联误差、规划长程弱、工具调用可靠性与成本、评测与可复现难、安全/越权风险
  common_baselines: 直接提示、思维链(CoT)、思维树(ToT)、纯 RAG
  evaluation_metrics: 任务成功率、步数/成本、工具调用准确率、AgentBench/WebArena
  suitable_datasets: ALFWorld、WebShop、HotpotQA(工具问答)、AgentBench
  implementation_repo: langchain-ai/langchain、Significant-Gravitas/AutoGPT、microsoft/autogen
  representative_papers:
    - "Toolformer: Language Models Can Teach Themselves to Use Tools | 2023 | cited:388 | doi:10.48550/arXiv.2302.04761 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
    - "Tree of Thoughts: Deliberate Problem Solving with Large Language Models | 2023 | cited:564 | doi:10.48550/arXiv.2305.10601 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
    - "[ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al. 2022, arXiv:2210.03629) — OpenAlex 该 arXiv DOI 解析到无关条目、按标题精确检索 count=0，免费源无法定位真实记录，标题/被引待核查]"
  possible_innovation_points: 多智能体协作、长程规划与反思(Reflexion)、记忆机制、工具学习与可靠性、Agent 评测基准、具身/GUI Agent; domain_scope=前沿ML
  maturity: 新兴(快速发展、热度极高；可靠性与评测仍不成熟，落地谨慎)

- method_name: 混合专家(Mixture-of-Experts, MoE)
  task_type: 超大模型高效扩展(语言/多模态)
  input_data: token 序列(路由到子专家)
  output_result: 由稀疏激活专家计算的表示/预测
  core_assumption: 用门控网络为每个 token 只激活少数专家(稀疏激活)，使总参数量大增而单 token 计算量近恒定，实现"参数扩展而算力可控"
  advantages: 参数规模可达万亿而推理算力可控、同算力下质量更高、专家可特化、是前沿大模型主流扩展路线
  limitations: 训练不稳定/负载不均、需辅助负载均衡损失、显存与通信开销大、专家利用率与路由坍塌、部署复杂
  common_baselines: 同算力稠密模型、同参数量稠密模型
  evaluation_metrics: 困惑度/下游指标 vs 算力、专家负载均衡、激活参数占比
  suitable_datasets: 大规模语料、多任务/多语言数据
  implementation_repo: google/flaxformer、microsoft/tutel、华为/Mixtral 类开源实现
  representative_papers:
    - "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer | 2017 | cited:268 | doi:10.48550/arXiv.1701.06538 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
    - "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity | 2021 | cited:361 | doi:10.48550/arXiv.2101.03961 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
  possible_innovation_points: 路由稳定性与负载均衡、细粒度/共享专家、MoE+LoRA、专家剪枝/合并部署、多模态 MoE、推理时专家卸载; domain_scope=前沿ML
  maturity: 主流(前沿大模型扩展主线之一)

- method_name: 状态空间模型(State Space Models / Mamba)
  task_type: 长序列建模(语言/基因组/音频/时序)，Transformer 的线性复杂度替代
  input_data: 长 token / 信号序列
  output_result: 序列表示 / 自回归预测
  core_assumption: 用结构化状态空间(SSM)以选择性(输入相关)参数压缩历史，实现序列长度上线性复杂度与硬件高效扫描，兼顾长程依赖与速度
  advantages: 复杂度随长度线性、长序列推理快/省显存、长程依赖强、可作 Transformer 替代或混合
  limitations: 生态/工具不如 Transformer 成熟、上下文检索(copy/in-context)能力曾弱、需定制 CUDA 核、超大规模验证仍在进行
  common_baselines: Transformer/注意力、线性注意力、S4、RNN/LSTM
  evaluation_metrics: 困惑度、长程任务(LRA)、吞吐/显存、下游指标
  suitable_datasets: The Pile、Long Range Arena、基因组、长音频/时序
  implementation_repo: state-spaces/mamba、state-spaces/s4
  representative_papers:
    - "Mamba: Linear-Time Sequence Modeling with Selective State Spaces | 2023 | cited:996 | doi:10.48550/arXiv.2312.00752 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
  possible_innovation_points: SSM+注意力混合架构、多模态/视觉 Mamba、长上下文检索增强、领域长序列(基因/时序)、硬件高效实现; domain_scope=前沿ML
  maturity: 新兴(高热度长序列前沿；与 Transformer 长期竞合，混合架构看好)

- method_name: 多模态大模型(CLIP / Flamingo / LLaVA)
  task_type: 图文理解/对话、零样本分类与检索、视觉问答、图像描述
  input_data: 图文对(CLIP)；图像/视频 + 文本指令(Flamingo/LLaVA)
  output_result: 跨模态对齐表示(CLIP)；以图为条件的文本生成(VQA/对话)
  core_assumption: CLIP 用大规模图文对比对齐双塔表示；Flamingo/LLaVA 用视觉编码器+投影把图像特征接入冻结/微调的 LLM，做视觉指令跟随
  advantages: CLIP 零样本强、开放词表；LLaVA/Flamingo 视觉对话与推理强、数据高效(对齐+指令微调)、可复用强 LLM
  limitations: 细粒度/计数/空间关系弱、视觉幻觉、依赖图文数据质量与规模、高分辨率/文档理解需专门设计
  common_baselines: 纯视觉模型、CLIP 线性探测、BLIP/BLIP-2、专用 VQA 模型
  evaluation_metrics: 零样本/检索 Recall、VQAv2、MMBench/MMMU、图像描述 CIDEr、幻觉评测(POPE)
  suitable_datasets: WIT/LAION(CLIP)、视觉指令数据(LLaVA-Instruct)、VQAv2、COCO Captions
  implementation_repo: openai/CLIP、mlfoundations/open_clip、haotian-liu/LLaVA
  representative_papers:
    - "Flamingo: a Visual Language Model for Few-Shot Learning | 2022 | cited:1240 | doi:10.48550/arXiv.2204.14198 | checked:2026-06-06"
    - "Visual Instruction Tuning (LLaVA) | 2023 | cited:679 | doi:10.48550/arXiv.2304.08485 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
  possible_innovation_points: 高分辨率/文档/图表理解、视频与 3D 多模态、幻觉抑制、统一生成+理解、领域多模态(医学影像报告)、任意模态; domain_scope=前沿ML
  maturity: 主流(CLIP 为基础模型；视觉指令多模态为当前热点主流)
```

```yaml
- method_name: 因果推断(DoWhy / 双重机器学习)
  task_type: 观测数据下估计因果效应(处理效应/反事实/政策评估)
  input_data: 观测数据(处理/结果/协变量) + 因果图假设
  output_result: 因果效应估计(ATE/CATE)及稳健性检验
  core_assumption: 在可识别性假设(无未观测混杂/可忽略性等)下，因果效应可由"建模→识别→估计→反驳"四步框架估计；DML 用机器学习去偏估计高维混杂下的效应
  advantages: 显式区分相关与因果、DoWhy 提供统一识别+反驳流程、DML 高维混杂稳健且有统计保证、支持反事实/政策分析
  limitations: 依赖不可检验的因果假设(混杂/外生性)、对图设定敏感、隐藏混杂致偏、需领域知识构图
  common_baselines: 朴素相关/回归、倾向得分匹配、IPW、断点回归、工具变量
  evaluation_metrics: 效应估计偏差/置信区间、反驳检验通过性、合成数据真值对比
  suitable_datasets: IHDP、Lalonde/Jobs、ACIC 因果基准、各观测研究数据
  implementation_repo: py-why/dowhy (GitHub API 200)、py-why/econml
  representative_papers:
    - "Double/debiased machine learning for treatment and structural parameters | 2017 | cited:2416 | doi:10.1111/ectj.12097 | checked:2026-06-06"
    - "DoWhy: An End-to-End Library for Causal Inference | 2020 | cited:15 | doi:10.48550/arXiv.2011.04216 [被引为 OpenAlex arXiv 记录数值，原文/库真实影响更高，待核查] | checked:2026-06-06"
    - "Causality (Pearl，因果推断奠基) | 2009 | cited:11077 | doi:10.1017/cbo9780511803161 | checked:2026-06-06"
  possible_innovation_points: LLM 辅助因果发现/构图、高维 CATE 个体效应、因果表示学习、与可解释 AI 结合、领域因果(医疗/经济政策); domain_scope=前沿ML
  maturity: 主流(因果推断标准工具链；与机器学习结合为活跃前沿)

- method_name: 可解释 AI(LIME / SHAP)
  task_type: 黑盒模型的事后解释(特征归因)
  input_data: 训练好的模型 + 待解释样本
  output_result: 特征对预测的贡献/重要性(局部或全局)
  core_assumption: LIME 在样本邻域用可解释线性模型局部逼近黑盒；SHAP 基于合作博弈 Shapley 值为每个特征分配公平且满足一致性的贡献
  advantages: 模型无关、提供可理解归因、SHAP 有公理化基础(局部精确/一致性)、广泛用于风控/医疗/合规
  limitations: LIME 邻域/采样不稳定、SHAP 精确计算指数级(需近似如 KernelSHAP/TreeSHAP)、相关特征归因有歧义、解释非因果
  common_baselines: 特征重要性(置换/基尼)、注意力可视化、梯度类(Grad-CAM/IG)
  evaluation_metrics: 忠实度(faithfulness)、稳定性、删除/插入曲线、人类可理解性
  suitable_datasets: 表格(信贷/医疗)、图像、文本各类任务
  implementation_repo: marcotcr/lime (GitHub API 200)、shap/shap (GitHub API 200)
  representative_papers:
    - "\"Why Should I Trust You?\": Explaining the Predictions of Any Classifier (LIME) | 2016 | cited:15043 | doi:10.1145/2939672.2939778"
    - "A Unified Approach to Interpreting Model Predictions (SHAP) | 2017 | cited:7622 | doi:10.48550/arXiv.1705.07874 | checked:2026-06-06"
  possible_innovation_points: LLM/大模型可解释、解释的因果化与稳定性、概念级解释(TCAV)、可解释性评测基准、解释驱动的调试与对齐; domain_scope=前沿ML
  maturity: 主流(事后可解释的事实标准工具)

- method_name: 神经辐射场(NeRF)
  task_type: 新视角合成、3D 场景隐式重建
  input_data: 多视角带位姿图像
  output_result: 连续体积场(颜色+密度)，可渲染任意新视角
  core_assumption: 用 MLP 把空间坐标+视角方向映射到颜色与密度，经可微体渲染沿光线积分合成图像，用多视角图监督即可隐式重建场景
  advantages: 照片级新视角、连续隐式表示紧凑、可微端到端、推动 3D 视觉重建范式革新
  limitations: 训练/渲染慢(原版)、需精确相机位姿、静态场景为主、大场景/动态/反射难、编辑性差
  common_baselines: 多视图立体(MVS)、光场、点云/网格重建、3D Gaussian Splatting
  evaluation_metrics: PSNR、SSIM、LPIPS、渲染速度
  suitable_datasets: NeRF Synthetic(Blender)、LLFF、Tanks and Temples、Mip-NeRF 360
  implementation_repo: bmild/nerf (GitHub API 200)、nerfstudio-project/nerfstudio
  representative_papers:
    - "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis | 2020 | cited:4719 | doi:10.1007/978-3-030-58452-8_24 | checked:2026-06-06"
  possible_innovation_points: 加速(Instant-NGP/哈希编码)、动态/可变形 NeRF、少视角/无位姿、大规模城市场景、与扩散/生成结合做 3D 生成、可编辑 NeRF; domain_scope=前沿ML
  maturity: 主流→部分被 3DGS 替代(实时渲染场景下 3D Gaussian Splatting 兴起；NeRF 仍是隐式重建重要基线)

- method_name: 3D 高斯泼溅(3D Gaussian Splatting)
  task_type: 实时新视角合成、显式 3D 场景表示
  input_data: 多视角带位姿图像(常用 SfM 点云初始化)
  output_result: 一组 3D 各向异性高斯(位置/协方差/颜色/不透明度)，可实时光栅化渲染
  core_assumption: 用大量可微 3D 高斯显式表示场景，通过快速可微光栅化(泼溅)渲染，质量媲美 NeRF 而渲染达实时
  advantages: 实时高帧率渲染、训练快、质量高、显式表示易编辑/操作、迅速成为新视角合成主流
  limitations: 存储/显存占用大、稀疏视角/反射弱、需较好初始化、动态与大场景仍在发展、走样/伪影
  common_baselines: NeRF 及其加速变体(Instant-NGP/Mip-NeRF)、MVS
  evaluation_metrics: PSNR、SSIM、LPIPS、FPS、显存/存储
  suitable_datasets: Mip-NeRF 360、Tanks and Temples、Deep Blending
  implementation_repo: graphdeco-inria/gaussian-splatting (GitHub API 200)
  representative_papers:
    - "3D Gaussian Splatting for Real-Time Radiance Field Rendering | 2023 | cited:4354 | doi:10.1145/3592433 | checked:2026-06-06"
  possible_innovation_points: 动态/4D 高斯、大场景与压缩、稀疏视角重建、与扩散结合做 3D/4D 生成、SLAM/自动驾驶应用、抗走样; domain_scope=前沿ML
  maturity: 新兴主流(2023 后迅速成为实时新视角合成主导方法)

- method_name: 图 Transformer(Graph Transformer / Graphormer)
  task_type: 图表示学习(尤以图级任务/分子性质预测)
  input_data: 图(节点/边特征 + 结构编码)
  output_result: 节点/图级表示与预测
  core_assumption: 将自注意力用于全图节点对，并以中心性/空间(最短路)/边编码注入图结构偏置，克服消息传递 GNN 的过平滑与长程依赖局限
  advantages: 全局感受野、缓解过平滑/长程依赖、分子等图级任务 SOTA、可统一序列与图建模
  limitations: 注意力随节点数平方、需精心设计结构编码、超大图可扩展性差、小图/稀疏标签优势有限
  common_baselines: GCN/GAT/GraphSAGE、GIN、消息传递 GNN
  evaluation_metrics: 图回归 MAE(分子)、节点/图分类 Acc/ROC、OGB 排行
  suitable_datasets: OGB(ogbg-molpcba/PCQM4M)、ZINC、分子/材料图数据
  implementation_repo: microsoft/Graphormer (GitHub API 200)
  representative_papers:
    - "Do Transformers Really Perform Bad for Graph Representation? (Graphormer) | 2021 | cited:128 | doi:10.48550/arXiv.2106.05234 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
  possible_innovation_points: 线性/稀疏图注意力扩展大图、更优结构/位置编码、与消息传递混合、3D 几何图 Transformer(分子构象)、与 LLM 结合的图推理; domain_scope=前沿ML
  maturity: 新兴主流(图级/分子任务的强方法；大图可扩展性为开放问题)

- method_name: 扩散策略(Diffusion Policy)
  task_type: 机器人视觉运动控制 / 模仿学习(动作序列生成)
  input_data: 观测(图像/状态)历史 + 专家示范
  output_result: 以观测为条件的动作序列(去噪生成)
  core_assumption: 把策略建模为条件去噪扩散过程，生成多步动作序列，可表达多模态动作分布并稳定建模复杂、连续高维动作
  advantages: 天然建模多模态动作、训练稳定、长动作序列连贯、在操作类任务显著超越传统行为克隆
  limitations: 推理需多步去噪(慢，需加速)、需较多示范数据、实时性与算力、对分布外状态泛化有限
  common_baselines: 行为克隆(BC)、隐式策略(IBC)、LSTM/Transformer 策略、CVAE 策略
  evaluation_metrics: 任务成功率、多任务平均得分、动作多模态覆盖
  suitable_datasets: Robomimic、Push-T、真实机器人操作示范、RLBench
  implementation_repo: real-stanford/diffusion_policy (GitHub API 200)
  representative_papers:
    - "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion | 2023 | cited:405 | doi:10.15607/RSS.2023.XIX.026 | checked:2026-06-06"
  possible_innovation_points: 少步/一致性采样加速实时控制、与 VLA(视觉-语言-动作)大模型结合、3D 场景条件、离线 RL + 扩散、跨本体泛化; domain_scope=前沿ML
  maturity: 新兴(机器人操作/具身智能高热度前沿方向)

- method_name: 世界模型(World Models / Dreamer)
  task_type: 基于模型的强化学习、想象中规划与控制
  input_data: 环境交互轨迹(观测/动作/奖励)
  output_result: 学到的潜在动力学模型 + 在其"想象"中训练的策略
  core_assumption: 学习环境的隐空间动力学模型(预测下一隐状态/奖励)，在压缩的潜在空间里"做梦"(rollout)训练策略，大幅提升样本效率
  advantages: 样本效率高(少量真实交互)、可在想象中规划、适合昂贵/危险真实交互、Dreamer 系跨任务通用
  limitations: 模型误差累积/想象偏差、长程预测难、复杂高维环境建模挑战、训练复杂、奖励稀疏仍难
  common_baselines: 无模型 RL(PPO/SAC/DQN)、MuZero、PlaNet
  evaluation_metrics: 样本效率、累积回报、跨任务通用性、想象预测误差
  suitable_datasets: DeepMind Control Suite、Atari(ALE)、Crafter、Minecraft(DreamerV3)
  implementation_repo: danijar/dreamer (GitHub API 200)、danijar/dreamerv3
  representative_papers:
    - "World Models (Ha & Schmidhuber) | 2018 | cited:180 | doi:10.48550/arXiv.1803.10122 [被引为 OpenAlex arXiv 记录数值，原文真实被引更高，待核查] | checked:2026-06-06"
    - "Dream to Control: Learning Behaviors by Latent Imagination (Dreamer) | 2019 | cited:137 | doi:10.48550/arXiv.1912.01603 [被引为 OpenAlex arXiv 记录数值，待核查] | checked:2026-06-06"
  possible_innovation_points: 通用世界模型(跨域 DreamerV3)、视频生成式世界模型(决策+生成融合)、与大模型结合的可控世界模型、具身/自动驾驶世界模型、长程规划; domain_scope=前沿ML
  maturity: 新兴(基于模型 RL 与生成式世界模型为高热度前沿)
```

## 数据来源与核查说明

- 本文件共 **25 张方法卡**。representative_papers 的 标题/年份/被引/DOI 全部来自 **OpenAlex API 真实 curl**（`https://api.openalex.org/works`，加 `&mailto` 进礼貌池），查询日期 **2026-06-06**；被引数为当日快照，随时间增长。
- implementation_repo 均用 **GitHub API**（`https://api.github.com/repos/<org>/<repo>`）核过 HTTP 状态：返回 200 的已标注；`facebookresearch/llama` 返回 301（仓库迁移至 `meta-llama/llama`），`facebookresearch/maml` 返回 404（官方实现为 `cbfinn/maml`），均已在卡内更正。`google-research/simclr` 单次取到 000 为网络瞬时失败，仓库为公开已知仓库。
- **付费墙诚实声明**：Clarivate JCR 影响因子、Scimago SJR 等付费指标本卡不涉及、不出现（免费源不可得，付费墙）。本库用 OpenAlex 被引作为可核查的热度替代，绝不臆造期刊指标。
- **标注「待核查」的情况（如实说明，未臆造）**：
  - 多数 arXiv 论文（MoCo/MAE/DARTS/剪枝/量化/FLAN/DPO/MoE/Mamba/LLaVA/Graphormer/World Models/Dreamer 等）：所给被引为 OpenAlex 对应 arXiv 记录的数值；这些高影响论文常存在 arXiv 版与会议/期刊版多条拆分或合并记录，原文聚合后真实被引通常更高，故标「待核查」。
  - **MAE**：OpenAlex 中按标题检索时排序受同名/合并记录干扰，已用 arXiv DOI(2111.06377) 精确定位原文记录，但其被引数(195)明显低于该论文真实影响，判为拆分记录，标「待核查」。

  - **ReAct**（Yao et al. 2022, arXiv:2210.03629）：用该 arXiv DOI 经 OpenAlex 解析到无关条目（"Distributing Accountability..."），按标题 `title.search` 精确检索返回 count=0，免费源无法定位其真实记录，标题/被引/DOI 整体标「待核查」；该 LLM Agent 卡改以可核实的 Toolformer、Tree of Thoughts 作为代表作支撑。
  - **auto-sklearn**（NeurIPS 2015）：OpenAlex 记录 DOI 字段为 null（会议论文无传统 DOI），DOI 标「待核查」。
- maturity（经典/主流/新兴/过时/不推荐）与 possible_innovation_points 为人工领域判断，非 API 字段。
- 受版权，全文不收录，仅元数据与公开开源链接。

> 维护建议：新兴卡（LLM Agent、Mamba、3DGS、扩散策略、世界模型、图 Transformer）热度高、迭代快，建议每季度复查被引与成熟度并做升降级；待核查的被引项可在 OpenAlex 记录合并后回填准确聚合值。


