# db02 · 2024–2026 顶会顶刊写作样本（LLM/扩散时代）

> 补齐现有 16 篇 2012–2021 经典样本的时代缺口。每篇为**真实获奖/高被引论文**的结构拆解，
> 标题/年份/venue/被引/DOI 全部 OpenAlex API 实拉（2026-06-12 快照，被引会增长属正常），
> **只存结构笔记 + reviewer_potential_questions，不存全文**（版权纪律）。摘要仅做结构归纳，不录原文长段。
> 字段 schema 同 [README](README.md)：title_pattern / abstract_structure / intro(problem-gap-contribution) /
> related_work_taxonomy / method_narrative / experiment_design / figure_table_logic / limitation /
> contribution_sentence / reviewer_potential_questions / venue / source_url。

## 来源与方法（可复现）
- 顶会获奖名单：NeurIPS 2024 官方 blog（blog.neurips.cc/2024/12/10）、CVPR 2024 官方 Awards 页（cvpr.thecvf.com/Conferences/2024/News/Awards），实查 2026-06-12。
- 每篇按标题回查 OpenAlex `works`，取 DOI/被引/年份；CVPR 系均有权威 IEEE DOI（10.1109/cvpr52733.2024.*），非预印本镜像。
- 选篇覆盖提示词要求：CVPR/NeurIPS 最佳论文 + Nature 子刊 2 篇 + 用户域（农业 CV）1 篇。

---

## R01 · Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction (VAR)
- **venue**：NeurIPS 2024（**Best Paper Award**） · **被引**：34（2026-06-12 快照） · **DOI**：10.52202/079017-2694 · 作者 5 人 · domain_scope=cv-视觉
- **title_pattern**：`方法名缩写(VAR): 大类任务 via 核心机制` —— 用"次尺度预测(next-scale prediction)"一短语点破与 GPT 式 next-token 的类比与差异，标题自带记忆点。
- **abstract_structure（归纳，非原文）**：① 自回归生图长期落后于扩散模型(立靶) → ② 病因诊断：传统按 raster/patch 顺序预测不符合图像多尺度结构 → ③ 主张：改为"由粗到细、逐尺度"预测 → ④ 结果：首次让 GPT 式自回归在 ImageNet 上**超过扩散基线**且推理更快、具 scaling law → ⑤ 意义：为视觉生成接入 LLM 范式打开口子。
- **intro(problem-gap-contribution)**：重要性=统一视觉与语言的生成范式；gap=已有视觉自回归顺序不当、慢且弱；contribution=次尺度自回归定义 + 幂律 scaling 证据 + zero-shot 泛化。
- **related_work_taxonomy**：按生成范式分族——扩散模型 / 掩码预测 / 传统栅格自回归，逐族点"与本文逐尺度的差异"。
- **method_narrative**：直觉(人看图由整体到细节) → 形式化(多尺度 token map 的条件分解) → 框架图(多尺度 VQ + Transformer) → 训练目标 → 推理复杂度优势。
- **experiment_design**：ImageNet 256/512 条件生成，FID/IS 对比扩散与旧自回归；scaling 曲线(参数 vs 损失幂律)；zero-shot 编辑/外推消融。
- **figure_table_logic**：首图必是"逐尺度预测"示意(讲清核心机制)；scaling law 折线是说服力支点；FID 表压过 DiT/扩散基线。
- **limitation**：分辨率与 codebook 受限、超大图与文本到图泛化仍待验证（获奖论文也明示边界）。
- **contribution_sentence 套路**：`We show, for the first time, that GPT-style autoregressive models can surpass diffusion ... by predicting at the next scale rather than the next token`——"first time + 可量化超越 + 一句话机制"。
- **reviewer_potential_questions**：①与扩散模型在公平算力下的对比是否充分？②scaling law 是否在更大模型/数据上仍成立？③次尺度顺序对 VQ codebook 质量的依赖有多强？④推理加速是否以牺牲多样性为代价(覆盖率/召回指标)？
- **source_url**：https://blog.neurips.cc/2024/12/10/announcing-the-neurips-2024-best-paper-awards/

---

## R02 · Generative Image Dynamics
- **venue**：CVPR 2024（**Best Paper Award**） · **被引**：41（2026-06-12 快照） · **DOI**：10.1109/cvpr52733.2024.02279 · 作者 4 人(Li, Tucker, Snavely, Holynski) · domain_scope=cv-视觉
- **title_pattern**：`Generative + 领域名词(Image Dynamics)` —— 两词极简、强画面感，不堆方法缩写，靠概念新颖度取胜（顶会 Best Paper 常见自信式命名）。
- **abstract_structure（归纳）**：① 真实世界含无数微小往复运动(树摇/烛火/呼吸) → ② 缺：从单图建模这种"自然振荡动态"的生成先验 → ③ 方法：在频域(谱体积)上学习每像素的运动基 → ④ 结果：单张静图→可循环播放的真实动画，且支持交互式拖拽响应 → ⑤ 意义：图像空间动态先验，可迁移到多种下游交互。
- **intro(problem-gap-contribution)**：重要性=让静态照片"活"起来的通用动态先验；gap=已有视频生成难保长时一致与物理合理的往复运动；contribution=频域运动表示 + 从单图预测谱体积 + 交互式动态渲染。
- **related_work_taxonomy**：按动态来源分——视频扩散/外插 / 物理仿真驱动 / 基于光流的动画，点出本文"频域运动基"的独到。
- **method_narrative**：直觉(自然振荡=少数低频模态叠加) → 形式化(傅里叶域运动谱体积) → 扩散模型预测谱系数 → 反变换得运动场 → 基于运动的图像渲染。
- **experiment_design**：真实场景视频集上对比运动质量与长时循环稳定性；交互响应 demo；与视频扩散基线的一致性/伪影对比；消融频域 vs 时域。
- **figure_table_logic**：核心是"单图→运动谱→循环动画"流程图 + 大量定性帧序列(动态论文定性 > 定量)；用户交互拖拽图证明可控性。
- **limitation**：仅擅长小幅往复运动，大位移/拓扑变化(行走、流体喷溅)不适用；依赖训练分布。
- **contribution_sentence 套路**：`We present an approach to modeling ... image-space scene dynamics ... from a single image`——"单输入×强能力"对比凸显贡献。
- **reviewer_potential_questions**：①频域假设对非周期/大幅运动失效时如何界定适用边界？②长时播放的漂移与闪烁如何量化？③与最新视频扩散模型(如 SVD)正面比较是否公平？④交互延迟与分辨率的工程可用性？
- **source_url**：https://cvpr.thecvf.com/Conferences/2024/News/Awards

---

## R03 · BioCLIP: A Vision Foundation Model for the Tree of Life
- **venue**：CVPR 2024（**Best Student Paper**） · **被引**：100（2026-06-12 快照） · **DOI**：10.1109/cvpr52733.2024.01836 · 作者 12 人 · domain_scope=cv-视觉
- **用户域强相关**：动植物/物种细粒度识别的视觉基础模型——精准畜牧/农业 CV/生物多样性监测可直接迁移其"大规模物种图像 + 分类层级标签"范式。
- **title_pattern**：`方法名(BioCLIP): A 定位(Vision Foundation Model) for 宏大领域(the Tree of Life)` —— "Tree of Life" 把生物分类全域诗意化，定位"基础模型"立刻拔高格局。
- **abstract_structure（归纳）**：① 生物学影像爆炸式增长、亟需跨物种通用视觉表征 → ② 缺：覆盖整个生命之树、含分类层级语义的基础模型与数据 → ③ 方法：构建大规模带分类阶元(界门纲目科属种)标签的图像库 + CLIP 式对比预训练 → ④ 结果：在大量细粒度物种任务上 zero/few-shot 显著超通用 CLIP → ⑤ 意义：生物学通用视觉基座，促进生态/保护/农业应用。
- **intro(problem-gap-contribution)**：重要性=自动化物种识别支撑生态与农业；gap=通用视觉模型不懂分类层级、细粒度差；contribution=TreeOfLife-10M 数据集 + 层级文本标签的对比学习 + 广谱物种基准的 SOTA。
- **related_work_taxonomy**：按表征来源分——通用 CLIP/视觉基础模型 / 细粒度识别专用网络 / 生物领域专用分类器，点出本文"层级语义 + 规模"的双重独到。
- **method_narrative**：直觉(分类阶元本身是强语义监督) → 数据构建(多源物种图像 + 标准化学名/俗名/阶元文本) → CLIP 对比目标(图像↔层级文本) → 推理(zero-shot 用类名文本)。
- **experiment_design**：跨多个物种数据集(鸟/虫/植物/动物)zero-shot 与 few-shot；对比 CLIP/OpenCLIP；消融"层级文本 vs 仅种名"证明阶元监督价值。
- **figure_table_logic**：核心图=数据规模与覆盖的"生命之树"可视化 + 层级文本构造示意；大表横扫多基准；t-SNE 展示层级聚类结构。
- **limitation**：长尾稀有物种与地域偏差、标签噪声；非自然图(显微/遥感)迁移待验证。
- **contribution_sentence 套路**：`We ... develop BioCLIP, ... demonstrating strong generalization across the tree of life`——"建数据 + 建模型 + 广谱泛化"三连。
- **reviewer_potential_questions**：①TreeOfLife-10M 的标签来源与质量控制如何？长尾分布偏差？②层级文本相比纯类名的增益是否经严格消融？③与领域专用细粒度模型在同等数据下孰优？④数据版权与生物采集伦理是否合规？
- **source_url**：https://cvpr.thecvf.com/Conferences/2024/News/Awards

---

## R04 · Mip-Splatting: Alias-free 3D Gaussian Splatting
- **venue**：CVPR 2024（**Best Student Paper**） · **被引**：379（2026-06-12 快照，3DGS 热点高被引） · **DOI**：10.1109/cvpr52733.2024.01839 · 作者 5 人 · domain_scope=cv-视觉
- **title_pattern**：`致敬经典(Mip-，借 mipmap)+方法名(Splatting): 解决的痛点(Alias-free) 大类(3D Gaussian Splatting)` —— 用图形学经典词"Mip"一秒传达"抗锯齿/多尺度"，命名即卖点。
- **abstract_structure（归纳）**：① 3DGS 渲染快但变焦/变分辨率时强烈走样 → ② 病因：高斯核缺多尺度频率约束 → ③ 方法：3D 平滑滤波(限频)+ 2D Mip 滤波(替代膨胀)→ ④ 结果：任意缩放下抗锯齿、跨分辨率泛化、几乎不增开销 → ⑤ 意义：让 3DGS 在真实多尺度观测下稳健可用。
- **intro(problem-gap-contribution)**：重要性=3DGS 是实时新视角合成主力；gap=采样率变化导致走样、out-of-distribution 缩放崩坏；contribution=频域分析定位病因 + 两个滤波器 + 即插即用几乎零成本。
- **related_work_taxonomy**：按新视角合成范式分——NeRF 系 / 点基与 splatting / 抗锯齿专门方法(mip-NeRF 等)，承上启下点出本文把 mip 思想搬进 3DGS。
- **method_narrative**：直觉(采样定理→限频抗锯齿) → 频域分析高斯走样来源 → 3D 平滑滤波 + 2D Mip 滤波公式 → 与原 3DGS 管线无缝集成。
- **experiment_design**：多分辨率/多缩放测试集；对比原 3DGS、mip-NeRF 系；PSNR/SSIM/LPIPS + 速度；单/多尺度训练-测试交叉协议(证明 OOD 泛化)。
- **figure_table_logic**：核心是"放大后锯齿 vs 无锯齿"对比放大图(一眼见效)；交叉分辨率协议表是说服力核心；消融两个滤波器各自贡献。
- **limitation**：极端缩放与稀疏视角下仍有残余伪影；滤波带宽需按场景设定。
- **contribution_sentence 套路**：`We introduce ... to address the aliasing ... achieving alias-free renderings at arbitrary scales`——"点病因 + 给方法 + 任意尺度"闭环。
- **reviewer_potential_questions**：①频域分析的假设(高斯近似)在真实场景多稳健？②两滤波器引入的额外计算/显存到底多少？③与并发抗锯齿 3DGS 工作的区别与公平比较？④训练/测试分辨率严重失配时上限在哪？
- **source_url**：https://cvpr.thecvf.com/Conferences/2024/News/Awards

---

## R05 · Rich Human Feedback for Text-to-Image Generation
- **venue**：CVPR 2024（**Best Paper Award**） · **被引**：49（2026-06-12 快照） · **DOI**：10.1109/cvpr52733.2024.01835 · 作者 18 人 · domain_scope=cv-视觉
- **title_pattern**：`Rich + 数据类型(Human Feedback) for 任务(Text-to-Image Generation)` —— 用 "Rich" 一词点出对粗粒度评分的升级(细粒度标注)，标题即贡献定位。
- **abstract_structure（归纳）**：① T2I 生成质量评估多停在单一总体评分 → ② 缺：细粒度、可定位的人类反馈(哪块不真实、哪词没画出) → ③ 方法：收集带区域标注+词级标注的丰富反馈数据集，训练预测模型 → ④ 结果：可预测细粒度问题并反哺改进生成 → ⑤ 意义：把"人类反馈"从标量升级为结构化信号，推动对齐。
- **intro(problem-gap-contribution)**：重要性=生成模型对齐依赖高质量反馈；gap=现有反馈太粗、不可定位；contribution=RichHF 数据集(区域+词级标注) + 多模态预测模型 + 反馈指导生成改善的验证。
- **related_work_taxonomy**：按反馈粒度分——标量偏好(RLHF 式) / 图文对齐打分 / 本文细粒度可定位反馈，凸显粒度升级。
- **method_narrative**：直觉(人能指出"哪里错") → 标注协议(不真实区域 mask + 缺失/多余词标注 + 多维评分) → 多模态模型联合预测 → 用预测信号筛选/微调改善生成。
- **experiment_design**：标注一致性分析；预测模型在区域/词级任务的准确度；下游用其改善生成的对比；跨模型泛化。
- **figure_table_logic**：核心图=一张"标注示例"(热区+划词)直观传达"rich"；预测 vs 人工的对齐表；改善前后定性对比。
- **limitation**：标注成本高、主观性与文化偏差；反馈模型自身误差会传递到下游。
- **contribution_sentence 套路**：`We collect rich human feedback ... and show that ... can be used to improve image generation`——"建细粒度数据 + 证可反哺"。
- **reviewer_potential_questions**：①细粒度标注的标注者间一致性(IAA)多高？协议如何控偏？②预测模型误差对下游改善的影响有多大？③相比标量 RLHF 的额外收益是否值回标注成本？④跨生成模型/跨语言的泛化证据？
- **source_url**：https://cvpr.thecvf.com/Conferences/2024/News/Awards

---

## R06 · Foundation model for cancer imaging biomarkers
- **venue**：Nature Machine Intelligence 2024（Nature 子刊） · **被引**：168（2026-06-12 快照） · **DOI**：10.1038/s42256-024-00807-9 · domain_scope=生物医学
- **医学影像 AI 范本**：医疗影像基础模型写作范式，可迁移到任何"小标注医学影像 + 自监督预训练"的论文。
- **title_pattern**：`Foundation model for 领域(cancer imaging biomarkers)` —— Nature 子刊偏好"能力定位"式极简标题，不带方法缩写。
- **abstract_structure（Nature 体，背景更长）**：① 影像生物标志物对肿瘤诊疗价值大 → ② 缺：标注稀缺限制深度模型、任务专用模型迁移差 → ③ 方法：大规模 CT 影像自监督预训练基础模型 → ④ 结果：少样本下多项生物标志物任务超专用模型、跨数据集稳健、标注效率高 → ⑤ 意义：可复用的肿瘤影像基座，降低落地门槛。
- **intro(problem-gap-contribution)**：重要性=影像生物标志物指导临床决策；gap=标注昂贵、模型碎片化；contribution=肿瘤影像自监督基础模型 + 少样本广谱评测 + 稳健性与可复现证据。
- **related_work_taxonomy**：按学习范式分——任务专用监督模型 / 迁移学习 / 自监督基础模型，点出本文规模与领域专属。
- **method_narrative**：直觉(无标注影像蕴含可迁移表征) → 自监督预训练(对比/重建) → 下游少样本微调协议 → 跨中心外部验证。
- **experiment_design**：多任务(分期/预后/分子标志)少样本对比专用模型；跨机构外部验证防过拟合；标注效率曲线；消融预训练规模。
- **figure_table_logic**：核心图=预训练→下游迁移示意 + 少样本性能曲线(横扫专用模型)；外部验证表是临床可信度核心；显著图/可解释性增信。
- **limitation**：模态/癌种覆盖有限、单中心偏差、临床前瞻验证缺失(医学论文必诚实声明)。
- **contribution_sentence 套路**：`We present a foundation model ... that ... with limited annotations ... generalizes across ...`——"基座 + 省标注 + 泛化"三点。
- **reviewer_potential_questions**：①预训练数据的中心/设备/人群分布偏差如何控？②少样本增益是否在前瞻数据上仍成立？③与最新通用医学基础模型的公平比较？④临床可用性(假阴性代价、可解释性)是否充分论证？
- **source_url**：https://doi.org/10.1038/s42256-024-00807-9

---

## R07 · Agricultural object detection with You Only Look Once (YOLO): A survey
- **venue**：Computers and Electronics in Agriculture 2024（农业工程旗舰刊，用户域核心） · **被引**：327（2026-06-12 快照） · **DOI**：10.1016/j.compag.2024.109090 · domain_scope=cv-农业
- **用户域 + 综述写作双范本**：精准农业/畜牧 CV 的检测综述，既是用户域最贴的写作样本，也是"综述类论文如何组织"的范式。
- **title_pattern**：`领域(Agricultural) 任务(object detection) with 方法(YOLO): A survey` —— 综述标题直白挂"任务×方法×survey"，利于检索与定位。
- **abstract_structure（综述体）**：① 农业场景目标检测需求激增(病虫害/果实/牲畜/杂草) → ② YOLO 因实时性成农业首选但应用零散缺系统梳理 → ③ 本文：按农业子任务系统综述 YOLO 各版本应用、数据集与改进 → ④ 发现：归纳常见改进策略与性能权衡、指出数据与部署缺口 → ⑤ 展望：边缘部署/小目标/域适应等方向。
- **intro(problem-gap-contribution)**：重要性=实时检测支撑智慧农业落地；gap=YOLO 农业应用碎片化、缺横向对比与选型指南；contribution=任务分类法 + 版本/改进谱系 + 数据集与指标汇总 + 开放问题清单。
- **related_work_taxonomy（综述即以此为骨架）**：按农业子任务分族——果实/作物检测 / 病虫害 / 杂草 / 牲畜与精准畜牧 / 农机视觉，每族梳理代表工作与数据集。
- **method_narrative（综述无方法，改为"组织逻辑"）**：YOLO 版本演进脉络(v1→最新) → 农业常见改进(轻量化/注意力/小目标/数据增强) → 部署形态(边缘/无人机/手机)。
- **experiment_design（综述=对比表）**：横向汇总各工作的数据集/mAP/速度/硬件；指出可比性缺失(数据集不统一)这一领域痛点。
- **figure_table_logic**：核心是"农业子任务 × YOLO 版本"的大覆盖表 + 任务分类树图；性能-速度散点示意权衡；典型失败案例图。
- **limitation**：综述受检索范围与时效限制；农业数据集不统一致跨研究对比受限(诚实声明)。
- **contribution_sentence 套路**：`This survey systematically reviews ... identifies ... and outlines open challenges`——综述三段式"系统梳理 + 归纳 + 开放问题"。
- **reviewer_potential_questions**：①综述检索协议(库/关键词/纳排标准)是否 PRISMA 式可复现？②是否覆盖最新 YOLO 版本与 transformer 检测器对比？③对农业数据集不统一问题是否给出可操作建议？④精准畜牧等子域覆盖是否充分？
- **source_url**：https://doi.org/10.1016/j.compag.2024.109090

---

## R08 · Augmenting large language models with chemistry tools (ChemCrow)
- **venue**：Nature Machine Intelligence 2024（Nature 子刊） · **被引**：568（2026-06-12 快照，LLM-agent 高被引） · **DOI**：10.1038/s42256-024-00832-8 · domain_scope=NLP语音
- **LLM 智能体写作范本**：LLM + 工具调用(agent) 范式的顶刊写法，迁移到任何"LLM 接专业工具解决领域任务"的论文。
- **title_pattern**：`动词(Augmenting) 对象(large language models) with 手段(chemistry tools)` —— 动词开头点出"增强"动作，直白传达"LLM+工具"主张。
- **abstract_structure（归纳）**：① LLM 擅长语言但在化学等专业任务上不可靠(幻觉/不会算) → ② 缺：让 LLM 可靠完成化学合成规划/性质预测等专业任务的途径 → ③ 方法：把 LLM 与一组专家化学工具(检索/计算/合成规划)用 agent 框架编排 → ④ 结果：在多类化学任务上显著优于纯 LLM、能自主完成合成规划 → ⑤ 意义：专家工具增强是 LLM 落地专业领域的可行范式。
- **intro(problem-gap-contribution)**：重要性=LLM 落地科学需可靠专业能力；gap=纯 LLM 幻觉且不会精确计算；contribution=化学工具集 + LLM agent 编排 + 多任务评测 + 安全考量。
- **related_work_taxonomy**：按增强方式分——纯提示/微调 / 检索增强(RAG) / 工具调用 agent，点出本文工具编排的系统性。
- **method_narrative**：直觉(让 LLM 会"用工具"而非"背知识") → agent 框架(思考-调用-观察循环) → 化学工具集成 → 任务编排与安全护栏。
- **experiment_design**：多类化学任务(合成路线/性质/反应)对比纯 LLM 与基线；专家人工评估(LLM 自评不可信，须人评)；案例研究展示自主规划。
- **figure_table_logic**：核心图=agent 工具调用流程示意 + 任务覆盖表；人工评估对比柱状(纯 LLM vs 工具增强)；典型成功/失败案例。
- **limitation**：工具覆盖与质量决定上限、安全滥用风险、评估依赖专家主观判断(明确声明)。
- **contribution_sentence 套路**：`We introduce ... an LLM ... augmented with ... tools, ... outperforming ... and autonomously ...`——"工具增强 + 超基线 + 自主完成"。
- **reviewer_potential_questions**：①专家人工评估的评分者一致性与盲评设计如何？②工具失败时 agent 的鲁棒性与错误传播？③与最新 LLM-agent 框架的公平比较？④双重用途/安全滥用(危险合成)的防护是否充分？
- **source_url**：https://doi.org/10.1038/s42256-024-00832-8

---

## 字段诚实性声明
- **已 OpenAlex 实拉核验**（2026-06-12 快照）：8 篇的标题、发表年、venue、被引数、DOI、作者数。CVPR 四篇均有权威 IEEE DOI（10.1109/cvpr52733.2024.*），NeurIPS VAR 为会议 proceedings DOI，两篇 Nature 子刊与农业刊为正式期刊 DOI。
- **被引为快照值会增长**：2024 论文被引仍在快速积累，数值偏小属正常，非质量判断。
- **摘要只做结构归纳不录原文**：所有 abstract_structure/method_narrative 均为结构笔记（版权纪律），需原文请访问 source_url。
- **获奖身份来源**：NeurIPS 2024 官方 blog 与 CVPR 2024 官方 Awards 页（见各卡 source_url），实查 2026-06-12。
