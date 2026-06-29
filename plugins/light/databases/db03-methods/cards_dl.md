# db03 方法卡 — 深度学习 / CV / NLP（cards_dl.md）

> 每张卡注明 maturity（经典|主流|新兴|过时|不推荐），避免提出落后方案。受版权全文不收录，仅元数据与开源链接。
> representative_papers 的标题/年份/被引/DOI 来自 OpenAlex 真实 curl 结果（https://api.openalex.org，mailto 礼貌池），查询日期 **2026-06-06**；被引数随时间变动。
> 排名/成熟度判断为人工标注。查不到的字段写「待核查」。

字段 schema 同 db03：`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`

## 方法卡

```yaml
- method_name: 卷积神经网络 / 残差与高效网络(CNN：ResNet / EfficientNet)
  task_type: 图像分类、特征提取骨干网络(backbone)
  input_data: 图像张量(H×W×C)
  output_result: 类别概率 / 特征图
  core_assumption: 局部卷积+权重共享捕获平移不变的层级视觉特征；残差连接缓解深层退化；复合缩放(深度/宽度/分辨率)平衡精度与算力
  advantages: 归纳偏置强、小数据友好、推理高效、迁移学习成熟、部署生态完善
  limitations: 感受野有限、长程/全局依赖弱于 Transformer、超大规模数据下精度上限低于 ViT
  common_baselines: VGG、Inception、ViT(大数据下)
  evaluation_metrics: Top-1/Top-5 Acc、Params、FLOPs、吞吐量
  suitable_datasets: ImageNet、CIFAR-10/100、下游各类视觉数据集
  implementation_repo: torchvision.models、rwightman/pytorch-image-models(timm)、官方 tensorflow/tpu(EfficientNet)
  representative_papers:
    - "Deep Residual Learning for Image Recognition (ResNet) | 2016 | cited:221133 | doi:10.1109/cvpr.2016.90 | checked:2026-06-06"
    - "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks | 2019 | cited:5013 | doi:10.48550/arXiv.1905.11946 | checked:2026-06-06"
  possible_innovation_points: 与注意力混合(ConvNeXt/CoAtNet 思路)、轻量化与 NAS、自监督预训练 backbone、边缘部署量化; domain_scope=通用深度学习
  maturity: 经典(ResNet 仍是强基线/常用 backbone；EfficientNet 主流但分类 SOTA 已转向 ViT 系)
```

```yaml
- method_name: 循环神经网络与门控变体(RNN / LSTM / GRU)
  task_type: 序列建模(时序预测、早期机器翻译、语音、文本)
  input_data: 变长序列(token/特征向量序列)
  output_result: 序列表示 / 逐步预测 / 序列到序列输出
  core_assumption: 隐状态沿时间递归传递历史信息；门控机制(输入/遗忘/输出门)缓解长程梯度消失
  advantages: 天然处理变长序列、参数量小、流式/在线推理友好、低资源场景仍实用
  limitations: 难并行(时间步串行)、超长依赖仍弱、长序列训练慢；多数任务已被 Transformer 超越
  common_baselines: 普通 RNN、HMM、TCN、Transformer
  evaluation_metrics: 困惑度(PPL)、BLEU、RMSE/MAE(时序)、Acc/F1
  suitable_datasets: Penn Treebank、WikiText、时序数据(M4/electricity)、语音(LibriSpeech)
  implementation_repo: torch.nn.LSTM / torch.nn.GRU、tensorflow.keras.layers.LSTM
  representative_papers:
    - "Long Short-Term Memory (LSTM) | 1997 | cited:97420 | doi:10.1162/neco.1997.9.8.1735 | checked:2026-06-06"
    - "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation (GRU) | 2014 | cited:24334 | doi:10.3115/v1/d14-1179 | checked:2026-06-06"
  possible_innovation_points: 与注意力/状态空间模型(Mamba/S4)结合、轻量时序预测、边缘流式推理; domain_scope=通用深度学习
  maturity: 经典(LSTM/GRU 在轻量时序/低资源仍用；NLP 主线已过时被 Transformer 取代)

- method_name: Transformer / 自注意力
  task_type: 序列建模(NLP/CV/语音/多模态)，通用骨干
  input_data: token / patch 序列 + 位置编码
  output_result: 上下文表示 / 自回归或并行预测
  core_assumption: 多头自注意力对全序列两两交互，捕获长程依赖，无递归即可并行
  advantages: 高度并行、长程依赖强、可扩展(scaling law)、迁移与多模态统一
  limitations: 注意力计算/显存随序列长度平方增长、数据与算力需求大、位置编码外推有限
  common_baselines: RNN/LSTM、CNN
  evaluation_metrics: 任务相关(PPL/BLEU/Acc/F1/mAP)
  suitable_datasets: 大规模语料、图像、语音、多模态对齐数据
  implementation_repo: huggingface/transformers、官方 tensorflow/tensor2tensor
  representative_papers:
    - "Attention Is All You Need | 原始为 2017 NeurIPS(Vaswani et al.) | OpenAlex 返回记录 publication_year=2025、cited:6557、doi:10.65215/2q58a426 [待核查：该 OpenAlex 记录为异常/合并条目，年份与被引明显失真，原文真实被引远高于此] | checked:2026-06-06"
  possible_innovation_points: 高效/稀疏注意力、长上下文、线性注意力与状态空间替代、领域与多模态适配; domain_scope=通用深度学习
  maturity: 主流(当代深度学习核心架构)
```

```yaml
- method_name: 预训练语言模型(BERT 系 / GPT 系)
  task_type: NLP 理解(BERT：分类/NER/QA) 与生成(GPT：文本生成/对话/few-shot)
  input_data: 大规模无标注文本(预训练) + 下游任务文本
  output_result: BERT 输出双向上下文表示；GPT 自回归生成 token 序列
  core_assumption: 大规模自监督预训练学通用语言表示；BERT 用掩码语言建模(双向)，GPT 用自回归(单向)；规模扩大涌现 few-shot/in-context 能力
  advantages: 强迁移、少样本/零样本能力(GPT)、统一多任务、生态成熟
  limitations: 预训练算力极高、存在幻觉/偏见、上下文长度与时效受限、BERT 不擅长生成、GPT 推理成本高
  common_baselines: word2vec/GloVe、ELMo、RNN seq2seq
  evaluation_metrics: GLUE/SuperGLUE、SQuAD F1/EM、MMLU、困惑度、人类评测
  suitable_datasets: Wikipedia+BookCorpus、Common Crawl、GLUE、SQuAD
  implementation_repo: huggingface/transformers、google-research/bert、openai(API)
  representative_papers:
    - "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | 2019 | cited:32329 | doi:10.18653/v1/n19-1423 | checked:2026-06-06"
    - "Language Models are Few-Shot Learners (GPT-3) | 2020 | cited:3029 | doi:10.48550/arXiv.2005.14165 [被引：OpenAlex 该 arXiv 记录数值，原文真实被引应更高，待核查] | checked:2026-06-06"
  possible_innovation_points: 高效微调(LoRA/PEFT)、检索增强(RAG)、长上下文、领域/多语言适配、对齐(RLHF/DPO); domain_scope=通用深度学习
  maturity: 主流(BERT 类编码器在理解任务仍常用；GPT 类解码器为当前大模型主线)

- method_name: 视觉 Transformer(ViT)
  task_type: 图像分类、视觉骨干网络
  input_data: 图像切分为固定大小 patch 序列 + 位置编码
  output_result: 类别概率 / 视觉特征表示
  core_assumption: 图像可视作 patch 序列，纯 Transformer 在足够大数据上可超越 CNN，弱归纳偏置由数据规模补偿
  advantages: 全局建模强、可扩展、大数据/大模型下精度高、与多模态统一
  limitations: 小数据上不如 CNN(需大规模预训练或强增广)、计算量大、对分辨率变化敏感
  common_baselines: ResNet、EfficientNet
  evaluation_metrics: Top-1/Top-5 Acc、Params、FLOPs
  suitable_datasets: ImageNet-1k/21k、JFT-300M、下游视觉任务
  implementation_repo: google-research/vision_transformer、timm
  representative_papers:
    - "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (ViT) | 2020 | cited:21562 | doi:10.48550/arXiv.2010.11929 | checked:2026-06-06"
  possible_innovation_points: 数据高效训练(DeiT)、层级结构(Swin)、自监督(MAE/DINO)、与卷积混合、轻量化; domain_scope=通用深度学习
  maturity: 主流(大规模视觉与多模态主流 backbone)
```

```yaml
- method_name: 目标检测(YOLO / Faster R-CNN / DETR)
  task_type: 目标检测(定位 + 分类)
  input_data: 图像
  output_result: 目标边界框 + 类别 + 置信度
  core_assumption: YOLO 单阶段网格直接回归框(实时)；Faster R-CNN 两阶段(RPN 生成候选+精修，重精度)；DETR 用 Transformer + 集合预测端到端去除 NMS/anchor
  advantages: YOLO 快、易部署；Faster R-CNN 精度高、生态成熟；DETR 端到端、无需手工 anchor/NMS
  limitations: YOLO 小目标/密集场景弱；Faster R-CNN 慢、组件多；DETR 收敛慢、小目标弱(早期版本)
  common_baselines: SSD、RetinaNet、Cascade R-CNN
  evaluation_metrics: mAP(COCO AP@[.5:.95])、AP50、FPS、Params
  suitable_datasets: COCO、PASCAL VOC、Objects365
  implementation_repo: ultralytics(YOLO)、facebookresearch/detectron2(Faster R-CNN/Mask R-CNN)、facebookresearch/detr(DETR)
  representative_papers:
    - "You Only Look Once: Unified, Real-Time Object Detection (YOLO) | 2016 | cited:3255 | doi:10.1109/cvpr.2016.91 [被引为 OpenAlex 该条记录数值，原始论文真实被引更高，待核查] | checked:2026-06-06"
    - "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | 2016 | cited:53939 | doi:10.1109/tpami.2016.2577031 | checked:2026-06-06"
    - "End-to-End Object Detection with Transformers (DETR) | 2020 | cited:831 | doi:10.1007/978-3-030-58452-8_13 [OpenAlex 该条被引偏低，原文真实被引更高，待核查] | checked:2026-06-06"
  possible_innovation_points: 实时+高精度平衡、开放词表检测、DETR 加速收敛(Deformable/DINO)、小目标与遥感、多模态检测; domain_scope=通用深度学习
  maturity: 主流(YOLO 工业部署首选；Faster R-CNN 经典强基线；DETR 系为新兴主流研究方向)

- method_name: 图像分割(U-Net / Mask R-CNN / SAM)
  task_type: 语义分割 / 实例分割 / 可提示通用分割
  input_data: 图像(SAM 额外接受点/框/文本提示)
  output_result: 像素级掩码(U-Net 语义；Mask R-CNN 实例框+掩码；SAM 可提示掩码)
  core_assumption: U-Net 编码-解码+跳连保留细节(医学/小数据强)；Mask R-CNN 在检测上加掩码分支；SAM 用大规模数据预训练做零样本可提示分割
  advantages: U-Net 小数据高效、结构简洁；Mask R-CNN 实例分割成熟；SAM 零样本泛化强、可交互
  limitations: U-Net 仅语义、类别固定；Mask R-CNN 依赖检测质量、慢；SAM 不输出类别语义、算力大
  common_baselines: FCN、DeepLab、Mask2Former
  evaluation_metrics: mIoU、Dice、AP(mask)、边界 F1
  suitable_datasets: Cityscapes、ADE20K、COCO、医学(ISIC/BraTS)、SA-1B
  implementation_repo: milesial/Pytorch-UNet、detectron2(Mask R-CNN)、facebookresearch/segment-anything(SAM)
  representative_papers:
    - "U-Net: Convolutional Networks for Biomedical Image Segmentation | 2015 | cited:88486 | doi:10.1007/978-3-319-24574-4_28 | checked:2026-06-06"
    - "Mask R-CNN | 2017 | cited:28690 | doi:10.1109/iccv.2017.322 | checked:2026-06-06"
    - "Segment Anything (SAM) | 2023 | cited:8946 | doi:10.1109/iccv51070.2023.00371 | checked:2026-06-06"
  possible_innovation_points: 医学/遥感领域适配、提示分割与文本结合、轻量 SAM(MobileSAM)、半监督/弱监督分割; domain_scope=通用深度学习
  maturity: U-Net 经典(医学主流强基线)；Mask R-CNN 主流；SAM 新兴主流(通用分割基础模型)
```

```yaml
- method_name: 生成对抗网络(GAN)
  task_type: 图像/数据生成、图像翻译、超分、数据增广
  input_data: 随机噪声(条件 GAN 加标签/图像)
  output_result: 生成样本
  core_assumption: 生成器与判别器极小极大对抗博弈，达到纳什均衡时生成分布逼近真实分布
  advantages: 采样快(单次前向)、生成清晰、图像翻译/超分等任务成熟
  limitations: 训练不稳定、模式崩塌、难评估收敛；高保真生成多已被扩散模型超越
  common_baselines: VAE、扩散模型
  evaluation_metrics: FID、IS、Precision/Recall、LPIPS
  suitable_datasets: CelebA、LSUN、ImageNet、FFHQ
  implementation_repo: NVlabs/stylegan3、eriklindernoren/PyTorch-GAN
  representative_papers:
    - "Generative Adversarial Networks (Goodfellow et al.，2014 NeurIPS；CACM 2020 重印) | 2020 | cited:13506 | doi:10.1145/3422622 | checked:2026-06-06"
  possible_innovation_points: 与扩散互补(对抗+去噪)、少样本生成、稳定训练、领域特定生成、作为快速采样器; domain_scope=通用深度学习
  maturity: 经典/部分过时(StyleGAN 类在特定人脸/快速生成仍用；通用高保真生成已被扩散取代，新研究不建议作为主方法)

- method_name: 变分自编码器(VAE)
  task_type: 生成、表示学习、异常检测、隐空间建模
  input_data: 数据样本(图像/序列等)
  output_result: 重构样本 + 连续隐变量分布
  core_assumption: 数据由低维隐变量经概率解码生成，用变分下界(ELBO)近似后验，重参数化使其可微
  advantages: 训练稳定、隐空间连续可插值、有概率解释、易与下游结合
  limitations: 生成偏模糊(相比 GAN/扩散)、后验坍塌、ELBO 与真实似然有差距
  common_baselines: 自编码器(AE)、GAN、扩散模型
  evaluation_metrics: ELBO/负对数似然、FID、重构误差
  suitable_datasets: MNIST、CelebA、分子(化学生成)
  implementation_repo: AntixK/PyTorch-VAE、pytorch 官方示例
  representative_papers:
    - "Auto-Encoding Variational Bayes (VAE) | 2013 | cited:15627 | doi:10.48550/arXiv.1312.6114 | checked:2026-06-06"
  possible_innovation_points: 离散隐变量(VQ-VAE)作扩散/自回归先验、解耦表示、科学数据(分子/基因)生成; domain_scope=通用深度学习
  maturity: 经典(纯生成弱于扩散；但 VQ-VAE 作为隐空间/tokenizer 在 latent diffusion、多模态中仍主流)

- method_name: 扩散模型(DDPM / Latent Diffusion)
  task_type: 高保真生成(图像/音频/视频/3D/分子)、条件生成(文生图)
  input_data: 高斯噪声 + 条件(文本/类别/图像)
  output_result: 生成样本
  core_assumption: 前向逐步加噪破坏数据、学习逆向去噪过程恢复数据；Latent Diffusion 在 VAE 压缩的隐空间扩散以降算力
  advantages: 生成质量与多样性 SOTA、训练稳定、可控条件生成、生态(Stable Diffusion)繁荣
  limitations: 采样需多步迭代(慢)、训练与推理算力大、对采样器/调度敏感
  common_baselines: GAN、VAE、自回归生成
  evaluation_metrics: FID、IS、CLIP-score、人类偏好
  suitable_datasets: ImageNet、LAION、CelebA-HQ
  implementation_repo: huggingface/diffusers、CompVis/stable-diffusion、CompVis/latent-diffusion
  representative_papers:
    - "Denoising Diffusion Probabilistic Models (DDPM) | 2020 | cited:5623 | doi:10.48550/arXiv.2006.11239 | checked:2026-06-06"
    - "High-Resolution Image Synthesis with Latent Diffusion Models (Stable Diffusion) | 2022 | cited:13494 | doi:10.1109/cvpr52688.2022.01042 | checked:2026-06-06"
  possible_innovation_points: 少步/一致性采样加速(蒸馏/Consistency)、可控生成与编辑、视频/3D/科学扩散、与 Transformer(DiT)结合; domain_scope=通用深度学习
  maturity: 主流(当前生成式视觉/多模态的主导方法)
```

```yaml
- method_name: 对比学习(SimCLR / CLIP)
  task_type: 自监督表示学习(SimCLR)、多模态对齐与零样本分类(CLIP)
  input_data: SimCLR 用无标注图像+数据增广对；CLIP 用大规模图文对
  output_result: 通用视觉/多模态表示，可零样本迁移
  core_assumption: 拉近正样本(同图增广 / 匹配图文对)、推远负样本，使表示对语义不变；大规模图文对比可学到开放词表对齐
  advantages: 无需人工标签、表示迁移强、CLIP 零样本分类与检索强、跨模态统一
  limitations: SimCLR 依赖大 batch/强增广/算力；CLIP 依赖海量图文数据、细粒度与计数弱、有数据偏见
  common_baselines: 有监督预训练、自编码、MoCo、BYOL
  evaluation_metrics: 线性探测 Acc、零样本 Acc、检索 Recall@K
  suitable_datasets: ImageNet(SimCLR)、WIT/LAION(CLIP)
  implementation_repo: google-research/simclr、openai/CLIP、mlfoundations/open_clip
  representative_papers:
    - "A Simple Framework for Contrastive Learning of Visual Representations (SimCLR) | 2020 | cited:7333 | doi:10.48550/arXiv.2002.05709 | checked:2026-06-06"
    - "Learning Transferable Visual Models From Natural Language Supervision (CLIP) | 2021 | cited:5296 | doi:10.48550/arXiv.2103.00020 | checked:2026-06-06"
  possible_innovation_points: 无负样本对比(BYOL/SimSiam)、多模态扩展(音频/视频)、细粒度对齐、领域 CLIP(医学/遥感)、作为生成模型条件编码器; domain_scope=通用深度学习
  maturity: 主流(SimCLR 为自监督经典强基线；CLIP 为多模态与开放词表任务的基础模型)

- method_name: 图神经网络(GCN / GAT / GraphSAGE)
  task_type: 节点分类、链接预测、图分类(社交/分子/推荐/知识图谱)
  input_data: 图(节点特征 + 邻接结构)
  output_result: 节点/边/图级表示与预测
  core_assumption: 消息传递——节点聚合邻居信息更新表示；GCN 用归一化邻接谱卷积，GAT 用注意力加权邻居，GraphSAGE 用采样+聚合支持归纳与大图
  advantages: 显式利用结构、半监督有效、GraphSAGE 可归纳推广到新节点、GAT 自适应邻居权重
  limitations: 过平滑(层深退化)、大图可扩展性、异配图弱、长程依赖难
  common_baselines: DeepWalk/node2vec、MLP(仅特征)、标签传播
  evaluation_metrics: 节点分类 Acc/F1、链接预测 AUC、图分类 Acc、ROC
  suitable_datasets: Cora/Citeseer/PubMed、OGB、PPI、分子(QM9/ZINC)
  implementation_repo: pyg-team/pytorch_geometric(PyG)、dmlc/dgl
  representative_papers:
    - "Semi-Supervised Classification with Graph Convolutional Networks (GCN) | 2016 | cited:8068 | doi:10.48550/arXiv.1609.02907 | checked:2026-06-06"
    - "Graph Attention Networks (GAT) | 2017 | cited:8340 | doi:待核查(OpenAlex 该记录 doi 为 null) | checked:2026-06-06"
    - "Inductive Representation Learning on Large Graphs (GraphSAGE) | 2017 | cited:4544 | doi:10.48550/arXiv.1706.02216 | checked:2026-06-06"
  possible_innovation_points: 缓解过平滑/深层 GNN、可扩展采样、Graph Transformer、异配图、与 LLM 结合的图推理; domain_scope=通用深度学习
  maturity: 主流(图结构任务标准方法；GCN/GAT/GraphSAGE 为三大经典基线)
```

```yaml
- method_name: 深度强化学习(DQN / PPO)
  task_type: 序贯决策(游戏、机器人控制、对齐 RLHF、运筹优化)
  input_data: 环境状态/观测 + 奖励信号
  output_result: 策略(动作选择) / 价值估计
  core_assumption: DQN 用神经网络逼近 Q 值+经验回放+目标网络稳定离线值学习(离散动作)；PPO 用裁剪目标限制策略更新幅度，稳定策略梯度(连续/离散均可)
  advantages: DQN 样本可复用、离散控制经典；PPO 稳定、易调、适用广、RLHF 主力
  limitations: 样本效率低、训练不稳定/对超参敏感、奖励设计难、仿真到现实(sim2real)差距
  common_baselines: DQN 系(Double/Dueling DQN)、A2C/A3C、SAC、TRPO
  evaluation_metrics: 累积回报/平均回报、样本效率、成功率、收敛稳定性
  suitable_datasets: Atari(ALE)、MuJoCo、OpenAI Gym/Gymnasium、Procgen
  implementation_repo: DLR-RM/stable-baselines3、ray-project/ray(RLlib)、openai/baselines
  representative_papers:
    - "Human-level control through deep reinforcement learning (DQN) | 2015 | cited:29824 | doi:10.1038/nature14236 | checked:2026-06-06"
    - "Proximal Policy Optimization Algorithms (PPO, Schulman et al. 2017, arXiv:1707.06347) | 待核查：OpenAlex 对应记录标题字段为空、被引约 1798 且条目异常，无法确认为原文，原文真实被引远高于此"
  possible_innovation_points: 离线 RL、样本高效探索、RLHF/RLAIF 对齐、世界模型、多智能体、与 LLM 结合的决策; domain_scope=通用深度学习
  maturity: 主流(DQN 为离散控制经典基线；PPO 为当前策略优化与 RLHF 的事实标准)

- method_name: 大模型参数高效微调(LoRA / PEFT)
  task_type: 预训练大模型在下游任务/领域的高效适配
  input_data: 预训练模型权重 + 下游任务数据
  output_result: 少量可训练适配参数(冻结主干)，得到适配后模型
  core_assumption: 微调时权重更新具低秩结构，故在冻结原权重旁注入低秩矩阵(A·B)只训练增量；PEFT 泛指仅训练小部分参数(LoRA/Adapter/Prefix/Prompt tuning)
  advantages: 显存与存储大幅降低、训练快、多任务可切换适配器、几乎不损精度、可合并回主干
  limitations: 极端领域漂移时不如全量微调、秩/层选择需调、推理需加载适配器(未合并时)
  common_baselines: 全参数微调(full fine-tuning)、Adapter、Prefix/Prompt tuning、BitFit
  evaluation_metrics: 下游任务指标(Acc/F1/Rouge/MMLU)、可训练参数量占比、显存/时间
  suitable_datasets: 指令微调集(Alpaca/Dolly)、领域语料、各下游基准
  implementation_repo: huggingface/peft、microsoft/LoRA
  representative_papers:
    - "LoRA: Low-Rank Adaptation of Large Language Models | 2021 | cited:2445 | doi:10.48550/arXiv.2106.09685 [被引为 OpenAlex arXiv 记录数值，实际更高，待核查] | checked:2026-06-06"
  possible_innovation_points: 量化结合(QLoRA)、动态秩/自适应分配、多适配器组合与路由(MoE-LoRA)、跨模态 PEFT、推理期高效切换; domain_scope=通用深度学习
  maturity: 主流(大模型微调的事实标准；LoRA/QLoRA 应用极广)
```

## 数据来源与核查说明

- representative_papers 的 标题/年份/被引/DOI 来自 OpenAlex API 真实 curl 查询（`https://api.openalex.org/works`，加 `&mailto` 进礼貌池），查询日期 2026-06-06。被引数为查询时快照，会随时间增长。
- 标注「待核查」的情况：
  - Transformer《Attention Is All You Need》：OpenAlex 返回的主记录为异常/合并条目（publication_year=2025、cited≈6557、非常规 DOI），与原文（2017 NeurIPS, Vaswani et al.）真实情况不符，原文真实被引远高于该数值。
  - PPO《Proximal Policy Optimization Algorithms》(Schulman et al. 2017, arXiv:1707.06347)：OpenAlex 中对应记录标题字段为空、被引约 1798 且条目状态异常，无法确认即原文，原文真实被引远高于此。
  - GPT-3 / YOLO / DETR / LoRA：所给被引为 OpenAlex 对应（多为 arXiv 版或某一拆分记录）的数值，原始论文聚合后真实被引更高。
  - GAT《Graph Attention Networks》：OpenAlex 该记录 DOI 字段为 null（原文为 ICLR 2018，无传统 DOI），DOI 标为待核查。
- maturity（经典/主流/新兴/过时/不推荐）与 possible_innovation_points 为人工领域判断，非 API 字段。
- implementation_repo 为公开知名仓库（GitHub / 官方库），受版权全文不收录，仅元数据与开源链接。

