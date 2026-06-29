# db04 数据集卡 — 表格 / 图 / 时序 / 多模态 / 领域

> 配套主卡：[dataset_cards.md](dataset_cards.md)。schema 见 [README.md](README.md)。
> 每条 license 必填，隐私/再分发/商用/授权限制务必写明（联动 a10）。
> 可核查字段（论文标题、年份、被引、DOI、ISSN）来自 OpenAlex `api.openalex.org` 真实 curl（核实日期 2026-06-06）。
> 排名/license/access 条款附来源 URL；查不到写「待核查」。

---

## 一、表格数据集

```yaml
- dataset_name: "UCI Adult (Census Income)"
  domain: "表格 / 社会经济"
  task: "收入二分类 (>50K vs <=50K)"
  data_type: "结构化 (14 特征, 含类别+数值)"
  size: "48842 实例 (train 32561 / test 16281)"
  format: "CSV (data + names)"
  license: "公开, CC BY 4.0 (UCI ML Repository 统一条款); 可商用; 可再分发"
  download_url: "https://archive.ics.uci.edu/dataset/2/adult"
  paper_url: "https://doi.org/10.24432/C5XW20"   # UCI DOI (Becker & Kohavi, 1996)
  citation: "Becker, B. & Kohavi, R. (1996). Adult. UCI ML Repository.; last_checked=待核; doi=10.24432/C5XW20"
  leaderboard_url: "待核查 (无统一官方榜; 多见于公平性论文对比)"
  known_issues: "1994 普查抽样, 时效性差; 类别不均衡 (~24% 正类); 含缺失值 (?); domain_scope=经济"
  bias_risk: "高 — 含 sex/race/native-country 敏感属性, 公平性研究标准反例"
  privacy_risk: "低 — 普查衍生且已脱敏, 无直接标识符"
  preprocessing_steps: "处理缺失值; 类别特征 one-hot/编码; 数值标准化"
  recommended_splits: "官方 train/test (adult.data / adult.test)"

- dataset_name: "Iris"
  domain: "表格 / 植物分类学"
  task: "三分类 (鸢尾花种类)"
  data_type: "结构化 (4 数值特征)"
  size: "150 实例 (每类 50)"
  format: "CSV"
  license: "公开, CC BY 4.0 (UCI ML Repository); 可商用; 可再分发"
  download_url: "https://archive.ics.uci.edu/dataset/53/iris"
  paper_url: "https://doi.org/10.1111/j.1469-1809.1936.tb02137.x"
  citation: "Fisher, R.A. (1936). The use of multiple measurements in taxonomic problems. Annals of Eugenics, 7(2):179-188. [OpenAlex 被引 14705]; last_checked=待核; doi=10.1111/j.1469-1809.1936.tb02137.x"
  leaderboard_url: "无 (教学基准, 已饱和)"
  known_issues: "极小且线性可分性强, 仅适合教学/快速验证; 2 类部分重叠; domain_scope=通用表格"
  bias_risk: "无"
  privacy_risk: "无"
  preprocessing_steps: "通常无需; 可标准化"
  recommended_splits: "无官方划分, 常用分层 K 折交叉验证"

- dataset_name: "Wine (UCI)"
  domain: "表格 / 化学分析"
  task: "三分类 (意大利同区三种栽培葡萄酒)"
  data_type: "结构化 (13 数值特征, 化学成分)"
  size: "178 实例 (类别 59/71/48)"
  format: "CSV"
  license: "公开, CC BY 4.0 (UCI ML Repository); 可商用; 可再分发"
  download_url: "https://archive.ics.uci.edu/dataset/109/wine"
  paper_url: "待核查 (UCI 引 Forina et al., PARVUS 程序包; 无规范期刊 DOI)"
  citation: "Forina, M. et al. (1988). PARVUS - An Extendable Package for Data Exploration, Classification and Correlation. [OpenAlex 该书条目被引 132]; last_checked=待核; src=community"
  leaderboard_url: "无"
  known_issues: "极小样本; 特征尺度差异大 (需归一化); domain_scope=化学-材料"
  bias_risk: "无"
  privacy_risk: "无"
  preprocessing_steps: "数值标准化 (尺度差异显著)"
  recommended_splits: "无官方划分, 常用 K 折交叉验证"

- dataset_name: "Titanic (Kaggle)"
  domain: "表格 / 社会"
  task: "生存二分类"
  data_type: "结构化 (混合: 数值+类别+文本姓名/票号)"
  size: "891 train / 418 test (经典 Kaggle 版)"
  format: "CSV"
  license: "待核查 — Kaggle \"Titanic - Machine Learning from Disaster\" 入门竞赛数据, 平台条款下供竞赛/学习使用; 商用与再分发需查竞赛 Rules; 底层乘客名单为历史公开记录"
  download_url: "https://www.kaggle.com/c/titanic/data"
  paper_url: "无 (Kaggle 入门竞赛, 无规范论文)"
  citation: "Kaggle. Titanic - Machine Learning from Disaster.; last_checked=待核; src=community"
  leaderboard_url: "https://www.kaggle.com/c/titanic/leaderboard"
  known_issues: "含缺失值 (Age/Cabin 大量缺失); test 标签不公开, 需提交评测; domain_scope=通用表格"
  bias_risk: "含 sex/class(社会阶层) 与生存强相关, 可作公平性讨论"
  privacy_risk: "历史人物真实姓名, 但属公开历史记录, 风险低"
  preprocessing_steps: "缺失值填补; 类别编码; 特征工程 (称谓/家庭规模)"
  recommended_splits: "官方 train/test (test 标签需在线评测)"

- dataset_name: "HIGGS"
  domain: "表格 / 高能物理"
  task: "二分类 (信号 vs 背景过程)"
  data_type: "结构化 (28 数值特征: 21 运动学 + 7 高阶)"
  size: "11,000,000 实例"
  format: "CSV (单文件, 最后 500k 作测试)"
  license: "公开, CC BY 4.0 (UCI ML Repository); 可商用; 可再分发"
  download_url: "https://archive.ics.uci.edu/dataset/280/higgs"
  paper_url: "https://doi.org/10.1038/ncomms5308"
  citation: "Baldi, P., Sadowski, P., Whiteson, D. (2014). Searching for exotic particles in high-energy physics with deep learning. Nature Communications 5:4308. [OpenAlex 被引 1177]; last_checked=待核; doi=10.1038/ncomms5308"
  leaderboard_url: "无统一官方榜 (论文报 AUC 基准)"
  known_issues: "模拟 (Monte Carlo) 数据非真实探测; 规模大, IO/内存敏感; domain_scope=物理科学"
  bias_risk: "无 (物理模拟)"
  privacy_risk: "无"
  preprocessing_steps: "标准化; 可分别使用低阶/高阶特征做消融"
  recommended_splits: "论文约定: 最后 500,000 行作测试集"
```

---

## 二、图 / 网络数据集

```yaml
- dataset_name: "OGB (Open Graph Benchmark) — ogbn-arxiv"
  domain: "图 / 引文网络"
  task: "节点分类 (论文学科 40 类); 时序划分"
  data_type: "有向引文图 (节点 169,343, 边 1,166,243; 节点特征 128 维词向量)"
  size: "~170k 节点 / ~1.17M 边 (ogbn-arxiv); OGB 含多规模数据集 (含 ogbn-papers100M 等)"
  format: "OGB Python 包加载 (NumPy/PyG/DGL)"
  license: "ogbn-arxiv 基于 MAG, 标注 ODC-BY 1.0; OGB 各数据集 license 不一 (见官网); 多数可商用/再分发但需核对单个数据集"
  download_url: "https://ogb.stanford.edu"
  paper_url: "https://doi.org/10.48550/arxiv.2005.00687"
  citation: "Hu, W. et al. (2020). Open Graph Benchmark: Datasets for Machine Learning on Graphs. NeurIPS. [OpenAlex arXiv 版被引 491]; last_checked=待核; doi=10.48550/arxiv.2005.00687"
  leaderboard_url: "https://ogb.stanford.edu/docs/leader_nodeprop/"
  known_issues: "不同子数据集划分/指标不同; ogbn-papers100M 规模极大需分布式; domain_scope=图学习"
  bias_risk: "学科分布不均衡"
  privacy_risk: "低 (公开论文元数据); 含作者机构信息"
  preprocessing_steps: "用官方 Evaluator; arxiv 按发表年份时序划分"
  recommended_splits: "官方提供 (arxiv 按时间; 其它按 scaffold/随机等)"

- dataset_name: "Cora / CiteSeer / PubMed (Planetoid)"
  domain: "图 / 引文网络"
  task: "半监督节点分类"
  data_type: "无向引文图 + 词袋节点特征"
  size: "Cora 2708节点/7类; CiteSeer 3327/6; PubMed 19717/3"
  format: "Planetoid (.cites/.content) 或 PyG/DGL 内置"
  license: "待核查 — 学术公开, 广泛免费用于研究; 无统一明确商用 license, 商用前核实"
  download_url: "https://linqs.org/datasets/"   # LINQS 组发布
  paper_url: "https://doi.org/10.1609/aimag.v29i3.2157"
  citation: "Sen, P. et al. (2008). Collective Classification in Network Data. AI Magazine 29(3). [OpenAlex 被引 3279]; 标准划分见 Yang et al. 2016 (Planetoid); last_checked=待核; doi=10.1609/aimag.v29i3.2157"
  leaderboard_url: "https://paperswithcode.com/sota/node-classification-on-cora"
  known_issues: "规模小易过拟合; 多种划分共存导致结果不可比; 已接近饱和; domain_scope=图学习"
  bias_risk: "低"
  privacy_risk: "低 (公开论文元数据)"
  preprocessing_steps: "行归一化特征; 取最大连通分量(部分工作)"
  recommended_splits: "Planetoid (Yang 2016) 公开划分 / 或 60-20-20 随机"

- dataset_name: "Reddit (GraphSAGE)"
  domain: "图 / 社交网络"
  task: "归纳式节点分类 (帖子所属社区 subreddit)"
  data_type: "大规模无向图 (节点 ~232,965, 边 ~11.6M; 节点特征 602 维)"
  size: "~233k 节点 / ~11.6M 边 / 50 类"
  format: "PyG/DGL 内置 或 GraphSAGE 原始文件"
  license: "待核查 — 源自 Reddit 公开帖 (2014/09); 数据集供研究, 商用/再分发受 Reddit 内容条款约束, 需核实"
  download_url: "https://snap.stanford.edu/graphsage/"
  paper_url: "https://doi.org/10.48550/arxiv.1706.02216"
  citation: "Hamilton, W., Ying, R., Leskovec, J. (2017). Inductive Representation Learning on Large Graphs. NeurIPS. [OpenAlex 被引 4544]; last_checked=待核; doi=10.48550/arxiv.1706.02216"
  leaderboard_url: "https://paperswithcode.com/sota/node-classification-on-reddit"
  known_issues: "规模大需邻居采样; 不同框架预处理版本节点/边数略有差异; domain_scope=图学习"
  bias_risk: "社区/话题分布不均"
  privacy_risk: "中 — 源自用户生成内容, 虽为社区级标签, 仍涉用户帖文"
  preprocessing_steps: "邻居采样; 特征标准化"
  recommended_splits: "按时间归纳划分 (train/val/test 帖)"
```

---

## 三、时序数据集

```yaml
- dataset_name: "ETT (Electricity Transformer Temperature)"
  domain: "时序 / 电力"
  task: "长序列多变量预测 (LSTF)"
  data_type: "多变量时序 (7 变量: 油温 OT + 6 负荷特征)"
  size: "ETTh1/h2 (小时级 ~17,420 步, 2年); ETTm1/m2 (15分钟级 ~69,680 步)"
  format: "CSV"
  license: "CC BY 4.0 (官方仓库 zhouhaoyi/ETDataset 声明); 可商用; 可再分发(署名)"
  download_url: "https://github.com/zhouhaoyi/ETDataset"
  paper_url: "https://doi.org/10.1609/aaai.v35i12.17325"
  citation: "Zhou, H. et al. (2021). Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting. AAAI (Best Paper). [OpenAlex AAAI 版被引 5981]; last_checked=待核; doi=10.1609/aaai.v35i12.17325"
  leaderboard_url: "https://paperswithcode.com/sota/time-series-forecasting-on-etth1-336"
  known_issues: "不同论文预测长度/通道设置不一致, 比较需对齐设置; domain_scope=时序"
  bias_risk: "无"
  privacy_risk: "低 (设备/区域脱敏)"
  preprocessing_steps: "标准化 (零均值单位方差); 滑窗切分"
  recommended_splits: "论文常用 train/val/test ≈ 12/4/4 月 (ETTh) 时序顺序划分"

- dataset_name: "M4 Competition"
  domain: "时序 / 通用预测竞赛"
  task: "单变量点预测 + 预测区间"
  data_type: "单变量时序 (混合频率)"
  size: "100,000 条序列 (Yearly/Quarterly/Monthly/Weekly/Daily/Hourly)"
  format: "CSV"
  license: "待核查 — 学术公开 (M4 官方 GitHub 提供); 供研究/竞赛, 商用前核实"
  download_url: "https://github.com/Mcompetitions/M4-methods"
  paper_url: "https://doi.org/10.1016/j.ijforecast.2018.06.001"
  citation: "Makridakis, S., Spiliotis, E., Assimakopoulos, V. (2018/2020). The M4 Competition: Results, findings, conclusion and way forward. Int. J. Forecasting 34(4). [OpenAlex 被引 573]; last_checked=待核; doi=10.1016/j.ijforecast.2018.06.001"
  leaderboard_url: "待核查 (竞赛已结束, 结果见论文/官方仓库)"
  known_issues: "各频率序列长度/特性差异大; 评测指标特定 (sMAPE/MASE/OWA); domain_scope=时序"
  bias_risk: "来源以经济/金融/人口等为主, 领域偏置"
  privacy_risk: "低 (匿名化序列)"
  preprocessing_steps: "按频率分组; 去趋势/季节性(可选)"
  recommended_splits: "官方固定 train + 各频率指定预测步长 (held-out)"

- dataset_name: "Traffic (PeMS, LSTNet 版)"
  domain: "时序 / 交通"
  task: "多变量长序列预测"
  data_type: "多变量时序 (862 个传感器道路占用率, 小时级)"
  size: "862 变量 × ~17,544 步 (2015-2016, 48 个月)"
  format: "CSV/TXT"
  license: "待核查 — 源自 California PeMS 公开数据; LSTNet 整理版供研究; 商用/再分发核实 PeMS 与仓库条款"
  download_url: "https://github.com/laiguokun/multivariate-time-series-data"
  paper_url: "https://doi.org/10.1145/3209978.3210006"
  citation: "Lai, G. et al. (2018). Modeling Long- and Short-Term Temporal Patterns with Deep Neural Networks (LSTNet). SIGIR. [OpenAlex 被引 2043]; last_checked=待核; doi=10.1145/3209978.3210006"
  leaderboard_url: "https://paperswithcode.com/sota/time-series-forecasting-on-traffic-336"
  known_issues: "占用率 [0,1] 截断; 强日/周周期; 不同处理版本变量数略异; domain_scope=时序"
  bias_risk: "地域单一 (加州旧金山湾区)"
  privacy_risk: "低 (聚合道路传感器, 无个体)"
  preprocessing_steps: "归一化; 滑窗; 周期特征"
  recommended_splits: "时序顺序 6:2:2 (论文设置)"

- dataset_name: "Electricity (ElectricityLoadDiagrams, LSTNet 版)"
  domain: "时序 / 电力"
  task: "多变量长序列预测"
  data_type: "多变量时序 (321 客户用电量, 小时级)"
  size: "321 变量 × ~26,304 步 (2012-2014)"
  format: "CSV/TXT"
  license: "公开 — 原始 UCI ElectricityLoadDiagrams2011-2014 为 CC BY 4.0; LSTNet 整理版同源, 可商用/再分发(署名)"
  download_url: "https://github.com/laiguokun/multivariate-time-series-data"
  paper_url: "https://doi.org/10.1145/3209978.3210006"
  citation: "原始 Trindade, A. UCI ElectricityLoadDiagrams2011-2014; 基准用法见 Lai et al. (2018) LSTNet, SIGIR. [OpenAlex 被引 2043]; last_checked=待核; doi=10.1145/3209978.3210006"
  leaderboard_url: "https://paperswithcode.com/sota/time-series-forecasting-on-electricity-336"
  known_issues: "原始 15 分钟级 (370 客户), 基准版重采样为小时级 321 客户, 版本需对齐; domain_scope=时序"
  bias_risk: "葡萄牙单一地区客户"
  privacy_risk: "中 — 客户级用电曲线, 已编号匿名但仍属个体消费模式"
  preprocessing_steps: "重采样小时级; 归一化; 滑窗"
  recommended_splits: "时序顺序 6:2:2 (论文设置)"
```

---

## 四、多模态数据集

```yaml
- dataset_name: "Flickr30k"
  domain: "多模态 / 视觉-语言"
  task: "图像描述 (caption) / 图文检索 (Flickr30k Entities 加短语-区域 grounding)"
  data_type: "图像 + 文本 (每图 5 条英文描述)"
  size: "31,783 图 / ~158k 描述"
  format: "JPEG + 文本标注"
  license: "待核查 — 图片源自 Flickr 用户, 多为 CC 许可; 数据集供研究用途, 商用/再分发受原图各自许可约束, 需逐一核实"
  download_url: "http://shannon.cs.illinois.edu/DenotationGraph/"  # 及 Flickr30k Entities
  paper_url: "https://doi.org/10.1162/tacl_a_00166"
  citation: "Young, P. et al. (2014). From image descriptions to visual denotations. TACL 2. [OpenAlex 被引 2442]; Entities: Plummer et al. (2015) ICCV; last_checked=待核; doi=10.1162/tacl_a_00166"
  leaderboard_url: "https://paperswithcode.com/sota/image-retrieval-on-flickr30k"
  known_issues: "描述风格/长度不均; 标注主观性; domain_scope=多模态CV"
  bias_risk: "来源人群/场景偏置 (Flickr 用户群体)"
  privacy_risk: "中 — 含真实人物照片 (来自社交平台)"
  preprocessing_steps: "resize; 文本分词/小写; 构建词表"
  recommended_splits: "Karpathy split (1000 val / 1000 test / 其余 train) 常用"

- dataset_name: "VQA (v2.0)"
  domain: "多模态 / 视觉问答"
  task: "看图回答自然语言问题 (开放/计数/是否)"
  data_type: "图像 (COCO) + 问题文本 + 答案"
  size: "VQA v2.0: ~204k 图, ~1.1M 问题, ~11M 答案"
  format: "JSON (问答) + COCO 图像"
  license: "注释 CC BY 4.0 (VQA 官方); COCO 图像 CC BY 4.0; 可商用/再分发(署名)"
  download_url: "https://visualqa.org/download.html"
  paper_url: "https://doi.org/10.1109/iccv.2015.279"
  citation: "Antol, S. et al. (2015). VQA: Visual Question Answering. ICCV. [OpenAlex 被引 4274]; v2.0: Goyal et al. (2017) CVPR; last_checked=待核; doi=10.1109/iccv.2015.279"
  leaderboard_url: "https://eval.ai/web/challenges/challenge-page/830/leaderboard"
  known_issues: "v1.0 语言先验偏置严重 (v2.0 平衡问答对缓解); 答案开放评分需特定指标; domain_scope=多模态CV"
  bias_risk: "高 — 语言先验/常识偏置; 标注者文化偏差"
  privacy_risk: "中 — 基于 COCO 含人物场景"
  preprocessing_steps: "图像特征提取; 问题分词; 答案归一化 top-k"
  recommended_splits: "官方 train/val/test-dev/test-std (test 需在线提交)"

- dataset_name: "AudioSet"
  domain: "多模态 / 音频事件"
  task: "多标签音频事件分类"
  data_type: "音频 (10 秒 YouTube 片段) + 标签 (632 类本体)"
  size: "~2,084,320 片段, 总计 ~5800 小时"
  format: "标签 CSV + 128 维 VGGish 嵌入特征 (TFRecord); 原始音频需自取 YouTube"
  license: "标注/本体 CC BY 4.0 (Google); 原始音频版权属各 YouTube 上传者, 不随数据集分发; 商用/再分发音频受 YouTube 条款约束"
  download_url: "https://research.google.com/audioset/"
  paper_url: "https://doi.org/10.1109/icassp.2017.7952261"
  citation: "Gemmeke, J.F. et al. (2017). Audio Set: An ontology and human-labeled dataset for audio events. ICASSP. [OpenAlex 被引 2955]; last_checked=待核; doi=10.1109/icassp.2017.7952261"
  leaderboard_url: "https://paperswithcode.com/sota/audio-classification-on-audioset"
  known_issues: "视频可能下架致数据漂移; 标签弱标注 (片段级, 含噪); 类别极不均衡; domain_scope=多模态CV"
  bias_risk: "YouTube 内容来源偏置"
  privacy_risk: "中 — 源自含人声/人物的网络视频"
  preprocessing_steps: "用官方 VGGish 嵌入 或 自行下载音频重采样 16kHz; 对数梅尔谱"
  recommended_splits: "官方 balanced_train / unbalanced_train / eval"
```

---

## 五、领域数据集（医疗 / 农业 / 遥感）

```yaml
- dataset_name: "MIMIC-III  ⚠ 需 credentialed access"
  domain: "领域 / 医疗 (重症监护 EHR)"
  task: "死亡率预测/住院时长/表型/临床NLP 等多任务"
  data_type: "去标识结构化 EHR + 临床文本 (生命体征/化验/用药/护理记录/出院小结)"
  size: "~40,000 患者, ~60,000 次 ICU 住院 (Beth Israel, 2001-2012)"
  format: "关系表 CSV (可导入 PostgreSQL)"
  license: |
    ⚠ 严格受限 — PhysioNet Credentialed Health Data License 1.5.0;
    获取需: (1) PhysioNet 注册并通过身份认证; (2) 完成 CITI "Data or Specimens Only Research" 培训; (3) 签署 DUA。
    禁止再分发/禁止尝试重标识患者; 商用受限需另行授权; 不得上传至无授权第三方/公有大模型
  download_url: "https://physionet.org/content/mimiciii/"   # 需登录+授权
  paper_url: "https://doi.org/10.1038/sdata.2016.35"
  citation: "Johnson, A.E.W. et al. (2016). MIMIC-III, a freely accessible critical care database. Scientific Data 3:160035. [OpenAlex 被引 8091]; last_checked=待核; doi=10.1038/sdata.2016.35"
  leaderboard_url: "待核查 (benchmark 见 Harutyunyan et al. 2019 等, 无单一官方榜)"
  known_issues: "单中心; 编码体系 (ICD-9) 时效; 文本含拼写/缩写噪声; 时间戳已偏移; domain_scope=生物医学"
  bias_risk: "高 — 单一医院人群, 种族/社会经济分布偏置, 用于公平性须谨慎"
  privacy_risk: "极高 — 真实患者健康数据 (已去标识但受 HIPAA/DUA 约束); 严禁重标识/外泄"
  preprocessing_steps: "建库 (PostgreSQL); 用官方/社区 pipeline (如 MIMIC-Extract); 文本去标识符已做但需复核"
  recommended_splits: "无官方统一划分; 按 benchmark 任务自定义 (患者级划分防泄漏)"

- dataset_name: "PlantVillage"
  domain: "领域 / 农业 (植物病害)"
  task: "叶片病害图像分类"
  data_type: "图像 (受控背景叶片照)"
  size: "~54,000 图, 14 作物 / 38 类 (健康+病害)"
  format: "JPEG (彩色; 另有灰度/分割版本)"
  license: "待核查 — 常引为开放研究使用 (spMohanty/PlantVillage-Dataset 仓库); 部分镜像标注 CC0; 商用前以官方仓库 LICENSE 为准"
  download_url: "https://github.com/spMohanty/PlantVillage-Dataset"
  paper_url: "https://doi.org/10.3389/fpls.2016.01419"
  citation: "Mohanty, S.P., Hughes, D.P., Salathé, M. (2016). Using Deep Learning for Image-Based Plant Disease Detection. Frontiers in Plant Science 7:1419. [OpenAlex 被引 4508]; 数据原始: Hughes & Salathé (2015) arXiv:1511.08060; last_checked=待核; doi=10.3389/fpls.2016.01419"
  leaderboard_url: "https://paperswithcode.com/sota/image-classification-on-plantvillage"
  known_issues: "实验室受控背景, 田间泛化差; 类别不均衡; 数据泄漏风险(同叶多图); domain_scope=通用"
  bias_risk: "受控拍摄, 与真实田间分布差异大"
  privacy_risk: "无 (植物图像)"
  preprocessing_steps: "resize; 增强; 注意按叶片/来源分组划分防泄漏"
  recommended_splits: "无统一官方划分; 论文用 train/test 多种比例 (建议来源分组)"

- dataset_name: "Sentinel-2 / BigEarthNet (遥感)"
  domain: "领域 / 遥感 (多光谱卫星影像)"
  task: "多标签土地覆盖分类 / 检索 (BigEarthNet); 原始影像支持广泛遥感任务"
  data_type: "多光谱影像 (Sentinel-2 13 波段, 10/20/60m 分辨率)"
  size: "原始 Sentinel-2: 全球持续观测; BigEarthNet-S2: 590,326 图块 (120×120 像素), 多标签 (CORINE)"
  format: "Sentinel-2 SAFE/JP2 (原始); BigEarthNet GeoTIFF + JSON 标签"
  license: |
    Sentinel-2 影像: Copernicus 开放数据条款 (免费, 可商用/再分发, 需署名 "Contains modified Copernicus Sentinel data");
    BigEarthNet: CDLA-Permissive-1.0 (可商用/再分发); CORINE 标签遵循 Copernicus 条款
  download_url: "https://dataspace.copernicus.eu  (原始); https://bigearth.net  (BigEarthNet)"
  paper_url: "https://doi.org/10.1109/igarss.2019.8900532"   # BigEarthNet
  citation: "Sumbul, G. et al. (2019). BigEarthNet: A Large-Scale Benchmark Archive for Remote Sensing Image Understanding. IGARSS. [OpenAlex 被引 527]; Sentinel-2 任务: Drusch, M. et al. (2012). Sentinel-2: ESA's Optical High-Resolution Mission for GMES Operational Services. Remote Sensing of Environment 120. [OpenAlex 被引 4413]; last_checked=待核; doi=10.1109/igarss.2019.8900532"
  leaderboard_url: "https://paperswithcode.com/sota/multi-label-classification-on-bigearthnet"
  known_issues: "云/雪遮挡; 部分图块标签含噪 (含云者建议剔除, 见 BigEarthNet 推荐); 大气校正级别 (L1C/L2A) 需统一; domain_scope=通用"
  bias_risk: "地理覆盖偏置 (BigEarthNet 限 10 个欧洲国家)"
  privacy_risk: "低 (中分辨率, 不可识别个体); 注意敏感设施使用合规"
  preprocessing_steps: "波段重采样对齐 10m; 大气校正 (L2A); 归一化; 剔除云/雪图块"
  recommended_splits: "BigEarthNet 官方 train/val/test 划分"
```

---

## 核实说明

- 论文标题/年份/被引/DOI 均来自 OpenAlex (`api.openalex.org`) 真实 curl，核实日期 2026-06-06。
- UCI 系列 (Adult/Iris/Wine/HIGGS/Electricity 原始) 现统一 CC BY 4.0（UCI ML Repository 站点条款）。
- license/access 经 WebSearch 辅助核对的来源：
  · MIMIC-III credentialed access / CITI / DUA — PhysioNet 内容页与 CITI Program (about.citiprogram.org)。
  · ETT — 官方仓库 [zhouhaoyi/ETDataset](https://github.com/zhouhaoyi/ETDataset)。
  · PlantVillage — 官方仓库 [spMohanty/PlantVillage-Dataset](https://github.com/spMohanty/PlantVillage-Dataset)。
  · AudioSet / VQA — Google AudioSet 站点、VQA 官网（注释 CC BY 4.0）。
  · Sentinel-2 — Copernicus 开放数据条款；BigEarthNet — [bigearth.net](https://bigearth.net)。
- 标「待核查」字段：license 不明确或无规范官方榜的项（Titanic/Cora 系列/Reddit/M4/Flickr30k/PlantVillage license），使用前须复核。
- ⚠ 高敏感：MIMIC-III（受 DUA 与 HIPAA 约束，严禁重标识/外泄/上传无授权第三方）。

