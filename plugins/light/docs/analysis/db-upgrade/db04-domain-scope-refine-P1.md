# db04 domain_scope 精化建议(P1 备用,2026-06-13 workflow 产出)

> 库重构时决定:机械 domain_scope 值已够过滤,精化为 P1 锦上添花。本表存 agent 对 100 张卡的精化建议,以后做 P1 可批量回填。

| 数据集 | 机械值 | 精化建议 |
|---|---|---|
| Animal Kingdom | 动物视觉 | 通用CV-野生动物视频行为/姿态 |
| AP-10K | 动物视觉 | 通用CV-动物2D姿态估计 |
| APT-36K | 动物视觉 | 通用CV-动物姿态估计+多目标跟踪 |
| Animal-Pose (Cross-Domain Animal Pose) | 动物视觉 | 通用CV-动物2D姿态估计(家畜/宠物近缘) |
| MammalNet | 动物视觉 | 通用CV-哺乳动物视频识别/行为 |
| iWildCam 2021 Competition Dataset | 动物视觉 | 通用CV-相机陷阱野生动物分类/域泛化 |
| Animals-10 (Kaggle) | 动物视觉 | 通用CV-图像分类(教学/baseline) |
| Cows2021 | 精准畜牧 | 精准畜牧-奶牛个体识别(再识别) |
| OpenCows2020 | 精准畜牧 | 精准畜牧-奶牛检测+个体识别 |
| AerialCattle2017 | 精准畜牧 | 精准畜牧-奶牛航拍(UAV)检测与识别 |
| Pig Behavior (Two-Stream CNN 视频行为) | 精准畜牧 | 精准畜牧-猪视频行为识别 |
| Pig Movement & Aggression (Deep Learning | 精准畜牧 | 精准畜牧-猪行为检测(攻击/运动) |
| Sheep Facial Expression (Pain / Transfer | 精准畜牧 | 精准畜牧-绵羊面部疼痛/表情评估 |
| Sheep Face Recognition (Bilinear Feature | 精准畜牧 | 精准畜牧-绵羊个体识别(人脸式) |
| Sheep videos from drone (Zenodo) | 精准畜牧 | 精准畜牧-绵羊航拍(UAV)检测计数 |
| GoatABRD (Goat Abnormal Behavior Recogni | 精准畜牧-奶山羊 | 精准畜牧-奶山羊行为识别(异常+常见) |
| CherryChèvre | 精准畜牧-奶山羊 | 精准畜牧-奶山羊/山羊自然环境检测 |
| DiaryGoatMVT (Dairy Goat Multiple Visual | 精准畜牧-奶山羊 | 精准畜牧-奶山羊多视觉任务(检测/分类) |
| 【现状评估卡】奶山羊专用公开数据集 — 稀缺但非空白 | 精准畜牧-奶山羊 | 精准畜牧-奶山羊(元说明卡,非数据集) |
| MIMIC-IV | 生物医学 | 临床医学-ICU/EHR |
| eICU Collaborative Research Database | 生物医学 | 临床医学-ICU/EHR(多中心) |
| UK Biobank | 生物医学 | 生物医学-人群队列/多组学 |
| TCGA / Pan-Cancer Atlas | 通用 | 生物医学-肿瘤组学/多组学 |
| MIMIC-CXR / CheXpert | 生物医学 | 生物医学-医学影像-胸部X光 |
| ADNI (Alzheimer's Disease Neuroimaging I | 多模态CV | 生物医学-神经影像-阿尔茨海默病 |
| HAM10000 / ISIC Archive | 通用 | 生物医学-皮肤病学-皮肤镜图像 |
| ImageNet (ILSVRC) | 通用CV | 通用CV-图像分类 |
| MS COCO (Common Objects in Context) | 通用CV | 通用CV-目标检测分割 |
| PASCAL VOC (2007/2012) | 通用CV | 通用CV-目标检测分割 |
| CIFAR-10 / CIFAR-100 | 通用CV | 通用CV-图像分类 |
| MNIST | 通用CV | 通用CV-教学/快速验证基准 |
| ADE20K | 通用CV | 通用CV-语义分割/场景解析 |
| Cityscapes | 自动驾驶-特定地域 | 自动驾驶-城市街景-特定地域(德语区) |
| CelebA (CelebFaces Attributes) | 通用CV | 计算机视觉-人脸属性/生成 |
| Open Images (V4–V7) | 通用CV | 通用CV-检测/分割/视觉关系 |
| GLUE | 通用NLP | 通用NLP-英文自然语言理解(NLU) |
| SuperGLUE | 通用NLP | 通用NLP-英文自然语言理解(NLU) |
| SQuAD (1.1 / 2.0) | 通用NLP | 通用NLP-抽取式阅读理解/问答 |
| WikiText (WikiText-2 / WikiText-103) | 通用NLP | 通用NLP-语言建模(困惑度) |
| Common Crawl / C4 (Colossal Clean Crawle | 通用NLP | 通用NLP-大规模预训练语料 |
| IMDB (Large Movie Review Dataset) | 通用NLP | 通用NLP-情感分类 |
| SNLI / MultiNLI (MNLI) | 通用NLP | 通用NLP-自然语言推理(NLI) |
| LAION-5B | 多模态CV | 通用多模态-图文(视觉语言预训练) |
| Common Crawl | 通用NLP | 通用NLP-网页爬取语料 |
| The Pile | 通用NLP | 通用NLP-多源混合英文语料 |
| RedPajama (RedPajama-Data v1 / v2) | 通用NLP | 通用NLP-LLaMA复现预训练语料 |
| C4 (Colossal Clean Crawled Corpus) | 通用NLP | 通用NLP-清洗后网页语料 |
| LAION-COCO | 多模态CV | 通用多模态-图文(合成caption预训练) |
| WebVid (WebVid-2M / WebVid-10M) | 多模态CV | 通用多模态-视频语言 |
| AudioCaps | 多模态CV | 通用多模态-音频语言(误标修正:原机械值多模态CV不准,实为音频-语言) |
| MSR-VTT (Microsoft Research Video to Tex | 多模态CV | 通用多模态-视频语言 |
| ScanNet (v2) | 通用CV | 3D视觉-室内场景理解(误标修正:原机械值通用CV过宽,实为RGB-D室内3D) |
| KITTI | 自动驾驶-特定地域 | 自动驾驶-特定地域(德国卡尔斯鲁厄单城) |
| nuScenes | 自动驾驶-特定地域 | 自动驾驶-特定地域(波士顿/新加坡两城) |
| Waymo Open Dataset (Perception) | 自动驾驶-特定地域 | 自动驾驶-特定地域(美国若干城市) |
| OGB-LSC (Open Graph Benchmark — Large-Sc | 通用 | 图机器学习-大规模图/分子(误标修正:原机械值通用过宽,无法过滤) |
| ZINC (含 ZINC15 / ZINC20 与 ZINC-250k 子集) | 化学-材料 | 药物化学-分子(类药可购小分子) |
| MoleculeNet | 化学-材料 | 分子机器学习-性质预测基准 |
| PhysioNet (PhysioBank / 含 MIT-BIH, MIMIC | 生物医学 | 生物医学-生理信号(ECG/EEG/血流动力学) |
| CheXpert | 生物医学 | 生物医学-胸片X光影像 |
| ISIC (HAM10000 / ISIC Archive 皮肤镜) | 生物医学 | 生物医学-皮肤镜影像(皮损/黑色素瘤) |
| DeepWeeds | 通用 | 精准农业-杂草识别(澳洲牧场,误标修正:原机械值通用无法过滤) |
| MMLU (Massive Multitask Language Underst | 通用NLP | LLM评测-英文知识与推理 |
| XTREME / XTREME-R | 通用NLP | 多语言NLP-跨语言理解 |
| LibriSpeech | 语音 | 语音识别-英语朗读有声书 |
| Common Voice | 语音 | 多语言语音-众包朗读 |
| VoxCeleb | 语音 | 说话人识别-名人YouTube视频 |
| FLEURS | 语音 | 多语言语音-朗读(ASR/语音翻译/语种识别) |
| VoxPopuli / AISHELL-1 | 语音 | 多语言语音-欧洲议会演讲+中文普通话朗读 |
| Materials Project | 化学-材料 | 材料科学-无机晶体/DFT计算数据库 |
| QM9 | 化学-材料 | 化学-小分子量子化学 |
| OQMD (Open Quantum Materials Database) | 化学-材料 | 材料科学-无机晶体/DFT形成能 |
| Open Catalyst 2020 (OC20) | 通用 | 催化-表面吸附/原子模拟 |
| JARVIS-DFT | 化学-材料 | 材料科学-多性质DFT数据库 |
| WeatherBench / ERA5-derived benchmark | 通用 | 气象-地球系统/数据驱动天气预报 |
| Human Connectome Project (HCP) | 通用 | 生物医学-神经影像/脑科学 |
| FRED-MD / FRED-QD | 经济 | 经济学-宏观时间序列(美国为主) |
| Penn World Table (PWT) | 经济 | 经济学-跨国宏观/增长(国家-年份面板) |
| World Bank World Development Indicators  | 经济 | 经济学-发展/国际比较(国家-年份面板) |
| Fama-French 因子库 | 金融-特定市场 | 金融-资产定价/因子模型(美股为主) |
| CRSP / Compustat / WRDS 金融数据库 | 金融-特定市场 | 金融-公司财务/股票市场(美股上市公司为主,商业订阅) |
| OECD Data / Product Market Regulation /  | 通用 | 经济学-跨国政策/制度指标 |
| UCI Adult (Census Income) | 经济 | 通用表格-公平性基准(美国1994普查) |
| Iris | 通用表格 | 通用表格-教学基准 |
| Wine (UCI) | 化学-材料 | 通用表格-教学基准(化学特征) |
| Titanic (Kaggle) | 通用表格 | 通用表格-入门竞赛基准 |
| HIGGS | 物理科学 | 通用表格-大规模二分类(高能物理模拟) |
| OGB (Open Graph Benchmark) — ogbn-arxiv | 图学习 | 图学习-节点分类(引文网络) |
| Cora / CiteSeer / PubMed (Planetoid) | 图学习 | 图学习-半监督节点分类(引文网络,小规模) |
| Reddit (GraphSAGE) | 图学习 | 图学习-归纳式节点分类(社交网络) |
| ETT (Electricity Transformer Temperature | 时序 | 时序预测-电力(变压器温度,LSTF基准) |
| M4 Competition | 时序 | 时序预测-通用单变量竞赛基准 |
| Traffic (PeMS, LSTNet 版) | 时序 | 时序预测-交通(道路占用率) |
| Electricity (ElectricityLoadDiagrams, LS | 时序 | 时序预测-电力(客户用电量) |
| Flickr30k | 多模态CV | 多模态-视觉语言(图像描述/检索,英文) |
| VQA (v2.0) | 多模态CV | 多模态-视觉问答 |
| AudioSet | 多模态CV | 多模态-音频事件分类(机械误标CV，实为音频) |
| MIMIC-III | 生物医学 | 生物医学-ICU重症监护EHR(credentialed授权) |
| PlantVillage | 通用 | 精准农业-植物叶片病害分类(机械误标通用) |
| Sentinel-2 / BigEarthNet (遥感) | 通用 | 遥感-多光谱卫星影像(土地覆盖,机械误标通用) |
