# db03 方法卡 — 行为识别 / 时空特征融合（cards_action_spatiotemporal.md）

> 每张卡注明 maturity（经典|主流|新兴|过时|不推荐），避免提出落后方案。受版权全文不收录，仅元数据与开源链接。
> representative_papers 的标题/年份/被引/DOI 来自 OpenAlex 真实 curl 结果（https://api.openalex.org，mailto 礼貌池），查询日期 **2026-06-06**；被引数随时间变动。
> 同一论文 OpenAlex 常有「会议正式版」与「arXiv 预印本」两条记录，被引分散；本卡优先取被引更高的正式版，必要时标注。
> 排名/成熟度判断为人工标注。查不到的字段写「待核查」。

字段 schema 同 db03：`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`

## 奶山羊行为识别（采食/反刍/站立/躺卧/爬跨/跛行/发情）适配说明

- **任务特点**：行为细粒度（采食 vs 反刍口部动作相近）、类间相似（站立 vs 躺卧静态姿态、爬跨 vs 正常接触）、长尾分布（发情/跛行/爬跨为罕见类，采食/站立为高频类）、需长时序建模（反刍是周期性咀嚼、跛行是步态周期、发情爬跨是短时事件，时间跨度从数秒到数分钟不等）。
- **方法适配结论**（详见各卡 possible_innovation_points）：
  - 长时序周期行为（反刍/跛行）→ SlowFast 双路径、TSN 稀疏长程采样、Transformer 时序聚合（TimeSformer/ViViT 的分解注意力）。
  - 细粒度+类间相似 → Something-Something v2 上强（强时序建模）的 TSM/MViTv2/VideoMAE 优于仅靠外观的 I3D。
  - 数据稀缺/标注贵 → VideoMAE/VideoMAE V2 自监督预训练，少样本下游微调。
  - 多目标群养遮挡 → 骨架/姿态路线（PoseC3D 用 2D 姿态热图，对光照/毛色鲁棒；ST-GCN/2s-AGCN）规避外观噪声。
  - 长尾 → 类重加权/重采样/解耦表征+分类器（BBN、Deep Long-Tailed Learning 综述思路），与上述骨干正交叠加。
- **数据现实（诚实声明）**：奶山羊行为识别**无公开标准视频基准数据集**。curl OpenAlex 检索到的真实相关工作多为自建私有数据集，例如 "Automatic behavior recognition of group-housed goats using deep learning"（2020, cited:85, doi:10.1016/j.compag.2020.105706）与 "A Real-Time Lightweight Behavior Recognition Model for Multiple Dairy Goats"（2024, cited:10, doi:10.3390/ani14243667）。**发情爬跨、跛行步态的山羊专用公开视频集未检索到**（OpenAlex "goat estrus mounting video"、"sheep lameness computer vision gait" 返回的均为加速度计/PLF 综述类，非视频识别基准）。本卡 suitable_datasets 中的 Kinetics/SSv2/NTU 等均为**人体**通用基准，仅用于预训练与方法选型参考，迁移到奶山羊须自建标注数据，不可声称存在山羊基准。

## 方法卡

```yaml
- method_name: 双流网络(Two-Stream CNN)
  task_type: 视频动作识别
  input_data: 空间流=单帧RGB；时间流=堆叠光流(optical flow)场
  output_result: 动作类别概率(两流分别预测后融合)
  core_assumption: 外观信息与运动信息可解耦——空间流CNN学外观/场景，时间流CNN从预计算光流学短时运动；两流分数后期融合互补
  advantages: 显式建模运动、在小数据(UCF101/HMDB51)上效果好、概念清晰、是后续融合研究的奠基
  limitations: 光流预计算昂贵不端到端、仅捕获短时运动、两流分离冗余、长时序建模弱
  common_baselines: 单帧CNN、iDT(改进密集轨迹手工特征)
  evaluation_metrics: Top-1 Acc、Clip/Video Acc
  suitable_datasets: UCF101、HMDB51
  implementation_repo: mmaction2(OpenMMLab)、feichtenhofer/twostreamfusion
  representative_papers:
    - "Two-Stream Convolutional Networks for Action Recognition in Videos | 2014 | cited:5369 | doi:10.48550/arxiv.1406.2199 | checked:2026-06-06"
    - "Convolutional Two-Stream Network Fusion for Video Action Recognition | 2016 | cited:2761 | doi:10.1109/cvpr.2016.213 | checked:2026-06-06"
  possible_innovation_points: 奶山羊场景光流可凸显反刍口部周期运动与爬跨快速位移，但群养遮挡下光流噪声大；适合作对比基线而非首选；可用RAFT等学习式光流替代TV-L1降本; domain_scope=cv-行为识别
  maturity: 经典(奠基性，现已被3D卷积/Transformer超越，多作历史基线)
```

```yaml
- method_name: C3D(3D卷积网络)
  task_type: 视频动作识别、时空特征提取
  input_data: 短视频片段(16帧RGB体素 L×H×W×C)
  output_result: 时空特征 / 动作类别
  core_assumption: 用3×3×3的3D卷积核同时在空间和时间维滑动，直接从原始视频体素学时空特征，无需光流
  advantages: 端到端、统一时空建模、特征通用(C3D fc6特征曾广泛迁移)、推理直接
  limitations: 参数量大易过拟合、时间感受野短(16帧)、算力高、精度被I3D/R(2+1)D超越
  common_baselines: 双流CNN、iDT、LRCN(CNN+LSTM)
  evaluation_metrics: Top-1 Acc、UCF101/Sports-1M 准确率
  suitable_datasets: Sports-1M、UCF101、HMDB51
  implementation_repo: facebook/C3D(原Caffe)、mmaction2
  representative_papers:
    - "Learning Spatiotemporal Features with 3D Convolutional Networks (C3D) | 2015 | cited:9663 | doi:10.1109/iccv.2015.510 | checked:2026-06-06"
  possible_innovation_points: 奶山羊短时事件(爬跨)用短片段3D卷积可行，但反刍/跛行长周期需更长时序，C3D感受野不足；作轻量基线或边缘部署候选; domain_scope=cv-行为识别
  maturity: 经典/趋于过时(开创3D卷积，现已被I3D/X3D等高效3D网络取代)
```

```yaml
- method_name: I3D(Inflated 3D ConvNet / 双流I3D)
  task_type: 视频动作识别
  input_data: RGB片段(+可选光流流)，64帧
  output_result: 动作类别概率
  core_assumption: 将2D ImageNet预训练网络(Inception)的卷积核沿时间维"膨胀"为3D并复制权重，从而继承2D预训练优势；配合Kinetics大规模预训练
  advantages: 利用2D预训练加Kinetics大数据显著提升、双流(RGB+flow)进一步增益、长期作迁移骨干与强基线
  limitations: 仍依赖光流取最佳精度、算力较高、长时序建模有限
  common_baselines: C3D、双流CNN、TSN
  evaluation_metrics: Top-1/Top-5 Acc(Kinetics)、UCF101/HMDB51 Acc
  suitable_datasets: Kinetics-400、UCF101、HMDB51、Charades
  implementation_repo: deepmind/kinetics-i3d、mmaction2
  representative_papers:
    - "Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset (I3D) | 2017 | cited:432 | doi:10.1109/cvpr.2017.502 [被引为OpenAlex该CVPR条目数值，原文真实被引远高于此，存在记录分散，待核查] | checked:2026-06-06"
  possible_innovation_points: 奶山羊上可用Kinetics预训练I3D做迁移基线；RGB-only分支避免群养光流噪声；细粒度采食/反刍区分能力一般，宜与强时序模型对比; domain_scope=cv-行为识别
  maturity: 经典/主流基线(膨胀+大规模预训练范式影响深远，仍常作对比)
```

```yaml
- method_name: P3D(Pseudo-3D 残差网络)
  task_type: 视频动作识别、时空特征提取
  input_data: 视频RGB片段
  output_result: 时空特征 / 动作类别
  core_assumption: 将3D卷积分解为1×3×3空间卷积 + 3×1×1时间卷积的伪3D块，按串/并/混合三种残差结构组合，降低3D卷积参数与算力
  advantages: 比C3D参数少、可加深、复用2D预训练、精度优于C3D
  limitations: 分解仍非最优(R(2+1)D进一步优化)、长时序有限、已被后续工作超越
  common_baselines: C3D、双流CNN、ResNet-2D
  evaluation_metrics: Top-1 Acc、Sports-1M/UCF101 Acc
  suitable_datasets: Sports-1M、UCF101、Kinetics
  implementation_repo: ZhaofanQiu/pseudo-3d-residual-networks、mmaction2
  representative_papers:
    - "Learning Spatio-Temporal Representation with Pseudo-3D Residual Networks (P3D) | 2017 | cited:1812 | doi:10.1109/iccv.2017.590 | checked:2026-06-06"
  possible_innovation_points: 时空分解思想可用于奶山羊轻量边缘部署；与R(2+1)D同属分解路线，建议直接用更成熟的R(2+1)D; domain_scope=cv-行为识别
  maturity: 经典/趋于过时(分解卷积先驱，实用上被R(2+1)D取代)
```

```yaml
- method_name: R(2+1)D(时空分解卷积)
  task_type: 视频动作识别
  input_data: 视频RGB片段
  output_result: 动作类别概率
  core_assumption: 将3D卷积显式分解为(2+1)D——先2D空间卷积再1D时间卷积，中间增加非线性，增大表达能力且更易优化；系统对比2D/3D/混合卷积
  advantages: 同算力下精度优于C3D/P3D、优化更稳、纯RGB即可达双流水平、工程实现简单
  limitations: 时间窗仍有限、长时序建模弱、被Transformer与SlowFast在大基准超越
  common_baselines: C3D、P3D、I3D、双流CNN
  evaluation_metrics: Top-1 Acc(Kinetics/UCF101/HMDB51)、Clip Acc
  suitable_datasets: Kinetics-400、UCF101、HMDB51、Sports-1M
  implementation_repo: facebookresearch/VMZ、torchvision.models.video(r2plus1d_18)、mmaction2
  representative_papers:
    - "A Closer Look at Spatiotemporal Convolutions for Action Recognition (R(2+1)D) | 2018 | cited:3513 | doi:10.1109/cvpr.2018.00675 | checked:2026-06-06"
  possible_innovation_points: 奶山羊上可作强而轻的3D基线(torchvision现成权重)；时空解耦便于分析采食(空间为主)与反刍(时间为主)的贡献；长周期跛行仍需多片段聚合; domain_scope=cv-行为识别
  maturity: 主流基线(分解3D的成熟代表，torchvision内置，常用对比)
```

```yaml
- method_name: TSN(时序段网络)
  task_type: 视频动作识别(尤擅长长时序/裁剪级)
  input_data: 整段视频稀疏分段后每段抽1帧/短片段(RGB及可选光流)
  output_result: 段级预测的共识(consensus)聚合为视频级类别
  core_assumption: 长视频中稀疏采样若干段即可覆盖全局时序，段间共享网络、段级预测做共识融合，避免密集采样冗余且建模长程结构
  advantages: 长时序建模、训练高效、对trimmed视频强、易与多种骨干结合、工程经典
  limitations: 共识(平均)忽略段间时序顺序、细粒度时序关系弱、依赖光流取最佳
  common_baselines: 双流CNN、C3D、iDT
  evaluation_metrics: Top-1 Acc(UCF101/HMDB51/Kinetics)、mAP(ActivityNet)
  suitable_datasets: UCF101、HMDB51、Kinetics-400、ActivityNet
  implementation_repo: yjxiong/temporal-segment-networks、mmaction2(TSN为默认范式之一)
  representative_papers:
    - "Temporal Segment Networks: Towards Good Practices for Deep Action Recognition | 2016 | cited:3920 | doi:10.1007/978-3-319-46484-8_2 | checked:2026-06-06"
    - "Temporal Segment Networks for Action Recognition in Videos | 2018 | cited:894 | doi:10.1109/tpami.2018.2868668 | checked:2026-06-06"
  possible_innovation_points: 奶山羊反刍/跛行为长周期行为，TSN稀疏长程采样天然契合——可覆盖数分钟反刍周期；缺点是平均共识丢顺序，可换TSM/Transformer聚合替代平均；强烈推荐作长行为基线; domain_scope=cv-行为识别
  maturity: 经典/主流(长时序采样范式影响深远，仍是常用基线与工程方案)
```

```yaml
- method_name: TSM(时序位移模块)
  task_type: 高效视频动作识别(在线/边缘友好)
  input_data: 视频帧序列(2D骨干，TSN式采样)
  output_result: 动作类别概率
  core_assumption: 在2D CNN通道维沿时间方向移位(shift)一部分通道，使相邻帧信息交换，从而以零额外FLOPs获得时序建模能力，达到接近3D卷积的效果
  advantages: 计算量≈2D网络、可在线推理(单向shift)、精度接近3D、极适合实时与边缘
  limitations: 时序建模隐式有限、长程依赖弱、对极细粒度时序不如显式3D/注意力
  common_baselines: TSN、I3D、R(2+1)D
  evaluation_metrics: Top-1 Acc(Kinetics/SSv2)、FLOPs、延迟/吞吐
  suitable_datasets: Kinetics-400、Something-Something v1/v2、Jester
  implementation_repo: mit-han-lab/temporal-shift-module、mmaction2
  representative_papers:
    - "TSM: Temporal Shift Module for Efficient Video Understanding | 2019 | cited:1961 | doi:10.1109/iccv.2019.00718 | checked:2026-06-06"
  possible_innovation_points: 奶山羊牧场边缘设备(摄像头端)实时多目标行为识别首选——低算力且在SSv2类强时序任务上强，契合细粒度采食/反刍；可作实时部署主力模型; domain_scope=cv-行为识别
  maturity: 主流(高效视频识别代表，工业实时部署常用)
```

```yaml
- method_name: SlowFast Networks
  task_type: 视频动作识别、时空动作检测
  input_data: 同一视频的双路径——Slow路径低帧率(语义/外观)、Fast路径高帧率轻通道(运动)
  output_result: 动作类别 / 时空动作框
  core_assumption: 视频的空间语义变化慢、运动变化快，应分别用低帧率高容量与高帧率低容量两路径处理，并通过侧向连接(lateral connection)融合
  advantages: 显式分离慢/快语义与运动、纯RGB无需光流、精度高、可扩展到检测、对时间分辨率敏感行为强
  limitations: 双路径增加复杂度、推理成本较高、超长时序仍需额外建模
  common_baselines: I3D、R(2+1)D、Non-local
  evaluation_metrics: Top-1/Top-5 Acc(Kinetics)、mAP(AVA时空检测)
  suitable_datasets: Kinetics-400/600、AVA、Charades、Something-Something
  implementation_repo: facebookresearch/SlowFast(官方PySlowFast)、mmaction2
  representative_papers:
    - "SlowFast Networks for Video Recognition | 2019 | cited:3592 | doi:10.1109/iccv.2019.00630 | checked:2026-06-06"
  possible_innovation_points: 奶山羊行为快慢混合(采食/站立慢语义 + 爬跨/跛步快运动)极契合双路径思想——Fast路径捕反刍咀嚼节律与跛行步态周期；强烈推荐作主力骨干，可在Fast路径加入步态周期先验; domain_scope=cv-行为识别
  maturity: 主流(强时空骨干，AVA等检测基准长期SOTA梯队)
```

```yaml
- method_name: X3D(高效视频网络渐进扩展)
  task_type: 高效视频动作识别
  input_data: 视频RGB片段
  output_result: 动作类别概率
  core_assumption: 从一个微型2D图像分类网络出发，沿时间/帧率/空间分辨率/宽度/深度/瓶颈宽度等多个轴逐步渐进扩展(借鉴EfficientNet复合缩放),只保留增益高的扩展
  advantages: 极高精度/算力比、模型族(XS/S/M/L)灵活、参数小、适合受限算力
  limitations: 架构搜索/扩展过程繁琐、超长时序仍有限、纯卷积全局建模弱于Transformer
  common_baselines: SlowFast、I3D、R(2+1)D
  evaluation_metrics: Top-1 Acc vs FLOPs/Params(效率前沿)、Kinetics Acc
  suitable_datasets: Kinetics-400、Charades、AVA
  implementation_repo: facebookresearch/SlowFast(含X3D)、mmaction2
  representative_papers:
    - "X3D: Expanding Architectures for Efficient Video Recognition | 2020 | cited:40 | doi:10.1109/cvpr42600.2020.00028 [OpenAlex该CVPR条目被引偏低/记录分散，原文真实被引远高于此，待核查] | checked:2026-06-06"
  possible_innovation_points: 奶山羊边缘/嵌入式部署高性价比骨干，可按算力预算选X3D-XS/S；与SlowFast同源，便于从云端SlowFast蒸馏到端侧X3D; domain_scope=cv-行为识别
  maturity: 主流(高效视频网络代表，资源受限场景常用)
```

```yaml
- method_name: TimeSformer(时空分解自注意力)
  task_type: 视频动作识别
  input_data: 视频帧切patch序列(时空token) + 位置编码
  output_result: 动作类别概率
  core_assumption: 将ViT扩展到视频，提出"分离时空注意力"(divided space-time attention)——先在时间维做注意力再在空间维，避免联合时空注意力的平方爆炸，纯Transformer无卷积
  advantages: 全局长程时空建模、无卷积归纳偏置、可处理较长片段、分离注意力高效
  limitations: 需大规模预训练、数据/算力需求大、小数据易过拟合、纯注意力局部细节弱
  common_baselines: I3D、SlowFast、R(2+1)D
  evaluation_metrics: Top-1 Acc(Kinetics-400/600、SSv2)
  suitable_datasets: Kinetics-400/600、Something-Something v2、HowTo100M
  implementation_repo: facebookresearch/TimeSformer、mmaction2
  representative_papers:
    - "Is Space-Time Attention All You Need for Video Understanding? (TimeSformer) | 2021 | cited:1357 | doi:10.48550/arxiv.2102.05095 | checked:2026-06-06"
  possible_innovation_points: 奶山羊长周期行为(反刍/跛行)可用时间维注意力跨帧聚合；分离注意力降本利于长片段；缺点是需先在大数据预训练，建议配合VideoMAE自监督预训练后微调; domain_scope=cv-行为识别
  maturity: 主流/新兴(视频Transformer开篇之作，仍活跃)
```

```yaml
- method_name: ViViT(Video Vision Transformer)
  task_type: 视频动作识别
  input_data: 视频时空管(tubelet)嵌入为token序列 + 位置编码
  output_result: 动作类别概率
  core_assumption: 系统化探索视频Transformer的token化(均匀帧采样 vs tubelet)与因式分解(分解编码器/分解自注意力/分解点积),用因式分解降低时空注意力复杂度
  advantages: 多种因式分解灵活权衡精度/算力、tubelet嵌入捕局部时空、大数据下高精度
  limitations: 算力/数据需求大、小数据需强正则或预训练、长视频token爆炸
  common_baselines: TimeSformer、SlowFast、I3D
  evaluation_metrics: Top-1 Acc(Kinetics-400/600、SSv2、Moments in Time)
  suitable_datasets: Kinetics-400/600、Something-Something v2、Moments in Time、Epic-Kitchens
  implementation_repo: google-research/scenic(ViViT)、mmaction2
  representative_papers:
    - "ViViT: A Video Vision Transformer | 2021 | cited:79 | doi:10.1109/iccv48922.2021.00676 [OpenAlex该ICCV条目被引偏低/记录分散，原文真实被引远高，待核查] | checked:2026-06-06"
  possible_innovation_points: 奶山羊tubelet嵌入可捕局部口部/腿部时空模式利于细粒度采食/反刍/跛行；分解编码器降本利于长片段；同样依赖大规模预训练; domain_scope=cv-行为识别
  maturity: 主流/新兴(视频Transformer代表，与TimeSformer并列)
```

```yaml
- method_name: VideoMAE(视频掩码自编码自监督预训练)
  task_type: 视频自监督预训练 → 下游动作识别微调
  input_data: 无标注视频(预训练，超高比例随机管状掩码) + 下游标注视频
  output_result: 预训练时空表示 / 下游动作类别
  core_assumption: 视频时序冗余高，可用极高掩码率(90%+)的管状(tube)掩码做掩码自编码，迫使模型从极少可见patch重建，学到强时空表示且数据高效
  advantages: 数据高效(小数据集也能从头预训练)、不需大规模标注、下游SOTA、对Transformer骨干通用
  limitations: 预训练仍需算力、对极长视频需采样、重建目标与判别任务有gap
  common_baselines: 有监督ViT/视频Transformer、对比学习(如ρMoCo)
  evaluation_metrics: 下游Top-1 Acc(Kinetics-400、SSv2、UCF101、HMDB51)
  suitable_datasets: Kinetics-400、Something-Something v2、UCF101、HMDB51、AVA
  implementation_repo: MCG-NJU/VideoMAE、huggingface/transformers(VideoMAE)、mmaction2
  representative_papers:
    - "VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training | 2022 | cited:435 | doi:10.48550/arxiv.2203.12602 | checked:2026-06-06"
  possible_innovation_points: 奶山羊标注稀缺场景的关键技术——用牧场大量无标注监控视频自监督预训练，再用少量发情/跛行标注微调，直接缓解长尾稀有类样本不足；强烈推荐; domain_scope=cv-行为识别
  maturity: 主流/新兴(视频自监督主流范式，数据稀缺场景首选)
```

```yaml
- method_name: VideoMAE V2(双掩码可扩展视频MAE)
  task_type: 大规模视频自监督预训练 → 下游识别/检测
  input_data: 百万级无标注视频(预训练) + 下游标注
  output_result: 大模型时空表示 / 下游任务输出
  core_assumption: 在VideoMAE基础上引入"双掩码"(decoder也掩码)降低预训练算力，使十亿参数级视频Transformer的可扩展自监督预训练可行，并配合渐进训练与多数据集
  advantages: 可扩展到十亿参数、预训练效率高、多任务(分类/检测/时序定位)全面SOTA、迁移强
  limitations: 仍需大规模数据与算力、大模型部署成本高、对小机构门槛高
  common_baselines: VideoMAE、有监督大视频Transformer、UMT
  evaluation_metrics: 下游Top-1 Acc(Kinetics)、mAP(AVA)、时序动作检测指标
  suitable_datasets: Kinetics-400/600/700、Something-Something v2、AVA、自建大规模无标注集
  implementation_repo: OpenGVLab/VideoMAEv2、mmaction2
  representative_papers:
    - "VideoMAE V2: Scaling Video Masked Autoencoders with Dual Masking | 2023 | cited:410 | doi:10.1109/cvpr52729.2023.01398 | checked:2026-06-06"
  possible_innovation_points: 奶山羊可用预训练好的VideoMAE V2权重做强特征提取/少样本微调，避免自行大规模预训练；双掩码思想也可用于自建羊场视频高效预训练; domain_scope=cv-行为识别
  maturity: 新兴(可扩展视频自监督前沿，2023后强基线)
```

```yaml
- method_name: MViT / MViTv2(多尺度视觉Transformer)
  task_type: 视频动作识别、图像分类、目标检测
  input_data: 视频/图像token序列(多尺度层级)
  output_result: 类别 / 检测框
  core_assumption: 将多尺度特征层级(由细到粗、通道由少到多)引入Transformer,用池化注意力(pooling attention)降低分辨率与算力；MViTv2加分解相对位置编码与残差池化连接
  advantages: 层级多尺度兼顾细节与语义、池化注意力高效、视频/图像/检测统一、强精度算力比
  limitations: 结构较复杂、训练调参敏感、超长时序仍需采样
  common_baselines: SlowFast、TimeSformer、ViViT、Swin
  evaluation_metrics: Top-1 Acc(Kinetics、SSv2)、mAP(检测)
  suitable_datasets: Kinetics-400/600、Something-Something v2、ImageNet、COCO(检测)
  implementation_repo: facebookresearch/SlowFast(含MViT)、facebookresearch/mvit、mmaction2
  representative_papers:
    - "Multiscale Vision Transformers (MViT) | 2021 | cited:56 | doi:10.48550/arxiv.2104.11227 [arXiv条目，会议正式版被引更高，待核查] | checked:2026-06-06"
    - "MViTv2: Improved Multiscale Vision Transformers for Classification and Detection | 2022 | cited:717 | doi:10.1109/cvpr52688.2022.00476 | checked:2026-06-06"
  possible_innovation_points: 奶山羊细粒度行为受益于多尺度——粗尺度看整体姿态(站立/躺卧)、细尺度看口部/腿部(采食/反刍/跛行)；池化注意力利于高分辨率监控帧；推荐作Transformer路线主力; domain_scope=cv-行为识别
  maturity: 主流/新兴(多尺度视频Transformer强骨干，检测+识别通用)
```

```yaml
- method_name: Video Swin Transformer
  task_type: 视频动作识别、时空建模骨干
  input_data: 视频3D token + 3D移位窗口
  output_result: 动作类别 / 时空特征
  core_assumption: 将Swin的局部移位窗口注意力扩展到3D时空——在不重叠的3D窗口内算自注意力，跨层移位窗口实现跨窗连接,用局部归纳偏置兼顾效率与精度
  advantages: 局部窗口注意力线性复杂度、层级结构、归纳偏置强(小数据更友好)、精度高、可迁移图像Swin预训练
  limitations: 窗口限制全局长程交互、3D窗口设计需调、长视频仍需采样
  common_baselines: SlowFast、MViT、TimeSformer、ViViT
  evaluation_metrics: Top-1 Acc(Kinetics-400/600、SSv2)
  suitable_datasets: Kinetics-400/600、Something-Something v2
  implementation_repo: SwinTransformer/Video-Swin-Transformer、mmaction2
  representative_papers:
    - "Video Swin Transformer | 2022 | cited:1886 | doi:10.1109/cvpr52688.2022.00320 | checked:2026-06-06"
  possible_innovation_points: 奶山羊场景Swin局部窗口+层级归纳偏置在中小自建数据上比纯ViT更稳；3D窗口可设计对齐口部/腿部局部区域；推荐数据量中等时优先于TimeSformer/ViViT; domain_scope=cv-行为识别
  maturity: 主流(层级视频Transformer强骨干，工程常用)
```

```yaml
- method_name: UniFormer(卷积-注意力统一时空骨干)
  task_type: 视频动作识别、时空表示学习
  input_data: 视频RGB片段
  output_result: 动作类别 / 时空特征
  core_assumption: 浅层用卷积式局部聚合(降低浅层注意力的计算冗余与局部建模不足)、深层用全局自注意力,在统一Transformer框架内结合卷积的局部高效与注意力的全局长程
  advantages: 兼顾局部冗余抑制与全局依赖、算力/精度平衡好、浅层高效深层强、可扩展V2(用图像ViT武装)
  limitations: 结构设计较精细、调参成本、生态不如Swin/MViT普及
  common_baselines: SlowFast、MViT、Video Swin、TimeSformer
  evaluation_metrics: Top-1 Acc(Kinetics、SSv2)、FLOPs/精度比
  suitable_datasets: Kinetics-400/600、Something-Something v1/v2
  implementation_repo: Sense-X/UniFormer、OpenGVLab/UniFormerV2、mmaction2
  representative_papers:
    - "UniFormer: Unified Transformer for Efficient Spatiotemporal Representation Learning | 2022 | cited:108 | doi:10.48550/arxiv.2201.04676 | checked:2026-06-06"
    - "UniFormerV2: Spatiotemporal Learning by Arming Image ViTs with Video UniFormer | 2022 | cited:58 | doi:10.48550/arxiv.2211.09552 | checked:2026-06-06"
  possible_innovation_points: 奶山羊上浅层卷积捕局部口部/步态纹理、深层注意力建模反刍/跛行长程节律——天然契合细粒度+长时序双需求；推荐作高效兼顾型骨干; domain_scope=cv-行为识别
  maturity: 新兴(卷积+注意力混合时空骨干，效率精度俱佳)
```

```yaml
- method_name: ST-GCN(时空图卷积网络)
  task_type: 基于骨架的动作识别
  input_data: 人体/动物关节坐标序列(图：关节为节点，骨骼+时间为边)
  output_result: 动作类别概率
  core_assumption: 将骨架序列建模为时空图——空间维按人体物理连接构图、时间维连接相邻帧同一关节，用图卷积在该时空图上学习,自动学关节关系
  advantages: 不依赖外观/光照、抗背景干扰、紧凑高效、对遮挡相对鲁棒、骨架方法奠基
  limitations: 依赖姿态估计质量、固定图结构限制远端关节关系、丢失外观/物体交互信息
  common_baselines: 手工骨架特征、LSTM(骨架)、CNN(骨架伪图)
  evaluation_metrics: Top-1 Acc(NTU RGB+D X-Sub/X-View、Kinetics-Skeleton)
  suitable_datasets: NTU RGB+D(60/120)、Kinetics-Skeleton
  implementation_repo: yysijie/st-gcn、open-mmlab/mmaction2(skeleton)、pyskl
  representative_papers:
    - "Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition (ST-GCN) | 2018 | cited:4800 | doi:10.1609/aaai.v32i1.12328 | checked:2026-06-06"
  possible_innovation_points: 奶山羊群养遮挡/毛色/光照变化大，骨架路线规避外观噪声有优势——需先有山羊关键点检测(可迁移AnimalPose/自标注)；可自定义羊体骨架拓扑(四足+头颈)建图；跛行=步态关节角周期，骨架尤其适配; domain_scope=cv-行为识别
  maturity: 经典(骨架动作识别奠基，仍是常用基线，图结构思想被后续继承)
```

```yaml
- method_name: 2s-AGCN(双流自适应图卷积网络)
  task_type: 基于骨架的动作识别
  input_data: 关节流(joint) + 骨骼流(bone，关节差分)骨架序列
  output_result: 动作类别概率(双流融合)
  core_assumption: ST-GCN固定图不最优——用自适应图(数据驱动学习邻接矩阵+可学习残差图)替代固定拓扑,并用关节+骨骼二阶信息双流互补
  advantages: 自适应拓扑突破物理连接限制、双流(关节+骨骼)显著增益、精度大幅超ST-GCN
  limitations: 双流训练成本翻倍、仍依赖姿态质量、图学习增加参数
  common_baselines: ST-GCN、HCN、LSTM骨架
  evaluation_metrics: Top-1 Acc(NTU RGB+D X-Sub/X-View)
  suitable_datasets: NTU RGB+D(60/120)、Kinetics-Skeleton
  implementation_repo: lshiwjx/2s-AGCN、pyskl、mmaction2
  representative_papers:
    - "Two-Stream Adaptive Graph Convolutional Networks for Skeleton-Based Action Recognition (2s-AGCN) | 2019 | cited:1973 | doi:10.1109/cvpr.2019.01230 | checked:2026-06-06"
  possible_innovation_points: 奶山羊体态关节关系未必符合人为拓扑，自适应图可数据驱动学羊体关节关联(如发情时头-尾-后肢联动)；骨骼流对爬跨/跛行的肢段相对运动敏感；推荐作骨架路线主力; domain_scope=cv-行为识别
  maturity: 主流(自适应图骨架识别代表，强基线)
```

```yaml
- method_name: MS-G3D(多尺度统一时空图卷积)
  task_type: 基于骨架的动作识别
  input_data: 骨架关节序列
  output_result: 动作类别概率
  core_assumption: 解耦多尺度图卷积(去除不同距离邻居的有偏加权,实现真正多尺度聚合)并用统一时空图卷积算子(G3D)直接跨时空建模,打通空间多跳与时间依赖
  advantages: 真多尺度聚合远近关节、时空联合算子捕跨帧关节关系、NTU上强SOTA
  limitations: 计算量较大、依赖姿态质量、结构复杂
  common_baselines: ST-GCN、2s-AGCN、DGNN
  evaluation_metrics: Top-1 Acc(NTU RGB+D 60/120 X-Sub/X-View)
  suitable_datasets: NTU RGB+D(60/120)、Kinetics-Skeleton
  implementation_repo: kenziyuliu/MS-G3D、pyskl
  representative_papers:
    - "Disentangling and Unifying Graph Convolutions for Skeleton-Based Action Recognition (MS-G3D) | 2020 | cited:1157 | doi:10.1109/cvpr42600.2020.00022 | checked:2026-06-06"
  possible_innovation_points: 奶山羊多尺度图可同时聚合近端(膝-蹄)与远端(头-尾)关节,利于发情(全身姿态)与跛行(局部步态)兼顾；时空联合算子捕反刍周期；骨架路线进阶选项; domain_scope=cv-行为识别
  maturity: 主流(多尺度骨架GCN代表，强基线)
```

```yaml
- method_name: PoseC3D(基于2D姿态热图的3D-CNN骨架识别)
  task_type: 基于骨架的动作识别
  input_data: 2D姿态估计输出的关节热图体(heatmap volume，时间×关节热图)
  output_result: 动作类别概率
  core_assumption: 不用GCN处理坐标，而把2D姿态估计的关节热图沿时间堆叠成3D体,用3D-CNN处理,避免坐标对姿态噪声敏感且更鲁棒、易与RGB融合
  advantages: 对姿态估计误差鲁棒(用热图而非坐标)、抗扰动、易与RGB双流融合、多人场景好、SOTA
  limitations: 热图体内存占用大、依赖2D姿态质量、相比GCN计算更重
  common_baselines: ST-GCN、2s-AGCN、MS-G3D
  evaluation_metrics: Top-1 Acc(NTU RGB+D、FineGYM、Kinetics)
  suitable_datasets: NTU RGB+D(60/120)、FineGYM、Kinetics-400、UCF101、HMDB51
  implementation_repo: open-mmlab/pyskl、mmaction2(PoseC3D)
  representative_papers:
    - "Revisiting Skeleton-based Action Recognition (PoseC3D) | 2022 | cited:757 | doi:10.1109/cvpr52688.2022.00298 | checked:2026-06-06"
  possible_innovation_points: 奶山羊2D关键点检测噪声大(毛发/遮挡)，PoseC3D用热图比坐标GCN更鲁棒；可与RGB双流融合兼得外观(采食物体)与姿态(跛行步态)；细粒度FineGYM上强，契合细粒度行为；强烈推荐骨架+RGB融合方案; domain_scope=cv-行为识别
  maturity: 主流/新兴(姿态热图3D-CNN，骨架识别新范式，鲁棒性优)
```

## 时空融合机制卡（融合策略，可与上述骨干组合）

```yaml
- method_name: 双流融合(光流+RGB，Two-Stream Fusion)
  task_type: 时空特征融合策略
  input_data: 空间流(RGB外观) + 时间流(光流运动)
  output_result: 融合后的时空预测
  core_assumption: 外观与运动信息互补，可在不同阶段融合——后期融合(分数平均)、早/中期融合(特征级在某卷积层空间对齐后融合),融合位置与方式影响精度
  advantages: 显式注入运动先验、互补性强、小数据有效、可即插
  limitations: 光流预计算昂贵/不端到端、融合位置需调、运动仅短时
  common_baselines: 单流、后期分数平均
  evaluation_metrics: Top-1 Acc(UCF101/HMDB51/Kinetics)
  suitable_datasets: UCF101、HMDB51、Kinetics-400
  implementation_repo: feichtenhofer/twostreamfusion、mmaction2
  representative_papers:
    - "Convolutional Two-Stream Network Fusion for Video Action Recognition | 2016 | cited:2761 | doi:10.1109/cvpr.2016.213 | checked:2026-06-06"
    - "Two-Stream Convolutional Networks for Action Recognition in Videos | 2014 | cited:5369 | doi:10.48550/arxiv.1406.2199 | checked:2026-06-06"
  possible_innovation_points: 奶山羊可用RGB+光流双流凸显反刍咀嚼与爬跨快速运动；群养遮挡下光流噪声大，建议用学习式光流(RAFT)或改用骨架+RGB融合(PoseC3D)替代光流; domain_scope=cv-行为识别
  maturity: 经典(融合奠基策略，现代多用隐式时序替代显式光流)
```

```yaml
- method_name: 3D卷积时空融合(3D Convolution Fusion)
  task_type: 时空特征融合策略
  input_data: 视频体素(时间×空间)
  output_result: 联合时空特征
  core_assumption: 用3D卷积核在时间与空间维同时卷积,在单一算子内隐式融合外观与短时运动,无需显式光流
  advantages: 端到端、隐式融合运动、统一时空、无需光流预计算
  limitations: 参数/算力大、时间感受野受核尺寸限、长时序需堆叠或扩张
  common_baselines: 2D卷积+时序池化、双流光流
  evaluation_metrics: Top-1 Acc(Kinetics/UCF101)
  suitable_datasets: Kinetics-400、Sports-1M、UCF101
  implementation_repo: facebookresearch/SlowFast、torchvision.models.video、mmaction2
  representative_papers:
    - "Learning Spatiotemporal Features with 3D Convolutional Networks (C3D) | 2015 | cited:9663 | doi:10.1109/iccv.2015.510 | checked:2026-06-06"
    - "A Closer Look at Spatiotemporal Convolutions for Action Recognition (R(2+1)D) | 2018 | cited:3513 | doi:10.1109/cvpr.2018.00675 | checked:2026-06-06"
  possible_innovation_points: 奶山羊短时事件(爬跨)用3D卷积隐式融合即可；长周期反刍/跛行需配合扩张时间卷积或多片段聚合扩大时间感受野; domain_scope=cv-行为识别
  maturity: 主流(隐式时空融合主力，分解3D降本)
```

```yaml
- method_name: 时序注意力 / Non-local(Temporal & Non-local Attention)
  task_type: 时空特征融合策略(长程依赖建模)
  input_data: 时空特征图序列
  output_result: 经全局/时序注意力重加权的时空特征
  core_assumption: 卷积感受野局部，难捕长程时空依赖；Non-local操作让每个位置直接与所有时空位置交互(自注意力的非局部均值形式),显式建模长程关系；时序注意力则在帧/段维加权聚合
  advantages: 捕长程时空依赖、即插即用模块、可叠加到3D-CNN、提升远距离关节/帧关系建模
  limitations: 全局注意力算力随时空尺寸平方、显存高、需放在合适层
  common_baselines: 纯3D卷积、局部注意力
  evaluation_metrics: Top-1 Acc(Kinetics)、mAP(检测)
  suitable_datasets: Kinetics-400、Charades、AVA
  implementation_repo: facebookresearch/video-nonlocal-net、mmaction2
  representative_papers:
    - "Non-local Neural Networks | 2018 | cited:11173 | doi:10.1109/cvpr.2018.00813 | checked:2026-06-06"
  possible_innovation_points: 奶山羊反刍/跛行的长周期节律需长程时序关系，Non-local/时序注意力可跨帧聚合咀嚼-吞咽或步态周期；可设计行为感知的时序注意力突出关键帧(如爬跨瞬间); domain_scope=cv-行为识别
  maturity: 主流(长程依赖建模标准模块，广泛叠加)
```

```yaml
- method_name: LSTM/GRU时序建模(CNN+RNN, LRCN)
  task_type: 时空融合策略(逐帧特征的时序聚合)
  input_data: 逐帧CNN特征序列
  output_result: 序列级动作类别 / 视频描述
  core_assumption: 用CNN逐帧提空间特征，再用LSTM/GRU沿时间递归聚合,显式建模帧间时序动态(CNN管空间、RNN管时间)
  advantages: 处理变长序列、显式时序建模、可用于识别+描述、流式在线推理、轻量
  limitations: 串行难并行、长程依赖仍弱、多数任务已被3D-CNN/Transformer超越、空间与时序解耦不如联合
  common_baselines: 单帧CNN、时序池化、3D-CNN
  evaluation_metrics: Top-1 Acc、序列标注指标、视频描述BLEU/METEOR
  suitable_datasets: UCF101、HMDB51、ActivityNet、视频描述数据集
  implementation_repo: 各框架CNN+torch.nn.LSTM组合、mmaction2(部分recurrent头)
  representative_papers:
    - "Long-term recurrent convolutional networks for visual recognition and description (LRCN) | 2015 | cited:5268 | doi:10.1109/cvpr.2015.7298878 | checked:2026-06-06"
  possible_innovation_points: 奶山羊轻量边缘+流式场景可用CNN特征+GRU在线判别反刍/采食状态；长周期跛行可用双向LSTM；现代更推荐TSM/Transformer聚合，LSTM作轻量备选; domain_scope=cv-行为识别
  maturity: 经典/趋于过时(CNN+RNN范式，识别主线已被3D/注意力取代，轻量流式仍用)
```

```yaml
- method_name: Transformer时序聚合(Temporal Transformer Aggregation)
  task_type: 时空融合策略(帧/段级特征的注意力聚合)
  input_data: 逐帧/逐段特征token序列 + 时间位置编码
  output_result: 全局聚合的视频级表示与类别
  core_assumption: 用自注意力替代RNN/平均做时序聚合,对所有帧/段两两交互并行建模长程时序顺序与依赖,常作骨干后的时序聚合头或端到端视频Transformer的时间分支
  advantages: 并行、长程时序、可建模顺序与关键帧、易与图像/视频骨干拼接、可扩展
  limitations: token数多时算力大、需位置编码与足够数据、短视频上可能过参数化
  common_baselines: 平均池化、LSTM/GRU聚合、TSN共识
  evaluation_metrics: Top-1 Acc(Kinetics/SSv2)、时序定位mAP
  suitable_datasets: Kinetics-400/600、Something-Something v2、ActivityNet
  implementation_repo: mmaction2、facebookresearch/TimeSformer(分解时间注意力)
  representative_papers:
    - "Is Space-Time Attention All You Need for Video Understanding? (TimeSformer，分离时序注意力) | 2021 | cited:1357 | doi:10.48550/arxiv.2102.05095 | checked:2026-06-06"
    - "Non-local Neural Networks (自注意力时空聚合先驱) | 2018 | cited:11173 | doi:10.1109/cvpr.2018.00813 | checked:2026-06-06"
  possible_innovation_points: 奶山羊长周期行为用Transformer跨段聚合最契合——可对反刍周期、跛行步态序列做顺序敏感聚合；结合时间位置编码注入周期先验；推荐作骨干(SlowFast/TSM)后的时序聚合头; domain_scope=cv-行为识别
  maturity: 主流/新兴(当代时序聚合主流，取代RNN与平均共识)
```

## 关联数据集（suitable_datasets 引用，均为人体/通用基准，OpenAlex 实拉）

| 数据集 | 用途 | 代表论文(OpenAlex 实拉，2026-06-06) |
|---|---|---|
| Kinetics-400 | 大规模动作识别/预训练 | "The Kinetics Human Action Video Dataset \| 2017 \| cited:2894 \| doi:10.48550/arxiv.1705.06950" |
| Something-Something v2 | 强时序/细粒度动作(类间相似) | "The 'Something Something' Video Database for Learning and Evaluating Visual Common Sense \| 2017 \| cited:1435 \| doi:10.1109/iccv.2017.622" |
| UCF101 / HMDB51 | 经典中小规模动作识别基线 | (UCF101/HMDB51 为社区标准基准，原始报告非期刊DOI，按惯例引用其官方页) |
| NTU RGB+D (60/120) | 骨架动作识别主基准 | "NTU RGB+D: A Large Scale Dataset for 3D Human Activity Analysis \| 2016 \| cited:2931 \| doi:10.1109/cvpr.2016.115" |
| AVA | 时空动作检测 | (AVA，见 SlowFast/AVA-Kinetics 相关条目) |

- 下载/许可：Kinetics(DeepMind，CC BY 4.0 标注，视频按YouTube条款)、SSv2(Qualcomm/20BN，研究许可需注册)、NTU RGB+D(南洋理工，申请协议)、UCF101/HMDB51(学术免费)。具体以各官方页为准；本卡不复制全文，仅引用元数据。

## 奶山羊行为识别方法选型矩阵（综合上述卡的人工建议）

| 目标行为 | 关键特性 | 推荐方法(优先级) | 理由 |
|---|---|---|---|
| 采食 / 反刍 | 细粒度口部周期动作、类间相似 | TSM、MViTv2、SlowFast(Fast路径)、VideoMAE微调 | SSv2类强时序任务表现好，捕咀嚼节律 |
| 站立 / 躺卧 | 静态姿态、长时段 | TSN稀疏采样、骨架(PoseC3D/2s-AGCN) | 姿态主导，长程采样足够，骨架抗外观噪声 |
| 爬跨 / 发情 | 短时事件、多目标交互、罕见(长尾) | SlowFast、骨架(2s-AGCN自适应图)、VideoMAE自监督缓解样本少 | 快运动+个体交互，自适应图学关节联动 |
| 跛行 | 步态周期、细粒度腿部、长时序 | PoseC3D/骨架(步态关节角)、SlowFast Fast路径、Transformer时序聚合 | 步态=关节周期，骨架最直接，长程聚合捕周期 |
| 群养遮挡通用 | 遮挡、毛色/光照变化 | PoseC3D(热图鲁棒)、骨架路线、RGB+骨架双流融合 | 规避外观噪声，热图比坐标稳 |

- **跨切面策略**：(1) 数据稀缺→VideoMAE/VideoMAE V2 自监督预训练；(2) 长尾(发情/跛行/爬跨稀有)→重采样/重加权/解耦表征(BBN、Deep Long-Tailed Learning 综述思路，与骨干正交)；(3) 长时序→TSN采样 + Transformer/Non-local时序聚合；(4) 边缘实时→TSM/X3D。
- **长尾参考(OpenAlex 实拉)**："Deep Long-Tailed Learning: A Survey \| 2023 \| cited:573 \| doi:10.1109/tpami.2023.3268118"；"BBN: Bilateral-Branch Network With Cumulative Learning for Long-Tailed Visual Recognition \| 2020 \| cited:870 \| doi:10.1109/cvpr42600.2020.00974"。
- **山羊领域真实工作(OpenAlex 实拉)**："Automatic behavior recognition of group-housed goats using deep learning \| 2020 \| cited:85 \| doi:10.1016/j.compag.2020.105706"；"A Real-Time Lightweight Behavior Recognition Model for Multiple Dairy Goats \| 2024 \| cited:10 \| doi:10.3390/ani14243667"。二者均自建私有数据集，**无公开山羊行为视频基准**；发情爬跨/跛行步态的山羊专用公开视频集未检索到，迁移须自建标注。












