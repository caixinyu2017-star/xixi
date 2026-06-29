# db04 — 动物/家畜 行为识别与姿态/检测 数据集卡（cards_animal_livestock）

> 每条记录含 license 与 商用/再分发/隐私 限制（联动 a10）。受版权/受限数据仅存元数据与链接。
> 论文 paper_url / citation 来自 OpenAlex 实时 curl（2026-06-06，`&mailto=` 无 key）；license / 官方下载页经 WebSearch + GitHub API 核实，不确定者标「待核查」。
> 被引数为查询当日 OpenAlex `cited_by_count` 快照，会随时间增长。
> 付费墙指标（JCR 精确 IF / Scimago SJR）免费源不可得，本卡用被引/期刊层级做可核查替代。

---

## 一、通用动物（行为 / 姿态 / 检测 / 分类）

```yaml
- dataset_name: Animal Kingdom
  domain: 通用动物 / 视频行为理解
  task: 视频动作识别(140 行为类) / 姿态估计(23 关键点) / 视频定位 / 细粒度物种
  data_type: 野生动物视频 + 帧图像(RGB)
  size: ~50 小时视频, 30k 视频片段(动作识别); 33k 帧(姿态), 850 物种, 6 大纲(哺乳/鸟/爬行/两栖/鱼/无脊椎)
  format: 视频 + 帧图 + COCO 式关键点 JSON + 动作标签
  license: 研究用途, 需在官方/GitHub 申请并同意条款; 商用?否(研究授权); 再分发?否; 需授权?是(申请) → 待核查(无单一开源许可文本)
  download_url: https://github.com/sutdcv/Animal-Kingdom
  paper_url: https://openalex.org/W4224285690  # CVPR 2022, DOI:10.1109/CVPR52688.2022.01844
  citation: Ng et al., 2022, CVPR. OpenAlex 被引 105 (2026-06-06); last_checked=2026-06-06; oa_id=W4224285690
  leaderboard_url: https://paperswithcode.com/dataset/animal-kingdom
  known_issues: 长尾类别极不均衡、罕见行为样本稀少、视频来源多样导致分辨率/帧率不一; domain_scope=动物视觉
  bias_risk: 物种/地域采集偏差(依赖可获取的纪录片/网络视频)、常见物种过采样
  privacy_risk: 低(野生动物为主, 偶含拍摄者)
  preprocessing_steps: 抽帧 / 时序裁剪 / 关键点归一化 / 长尾重采样或类别加权
  recommended_splits: 官方 train/val/test(动作与姿态各自划分)
```

```yaml
- dataset_name: AP-10K
  domain: 通用动物 / 2D 姿态估计
  task: 野外动物 2D 关键点姿态估计(17 关键点)
  data_type: 自然图像(RGB)
  size: ~10k 标注图, 23 科 54 种哺乳动物
  format: COCO 式关键点 JSON
  license: Creative Commons Attribution 4.0 International (CC BY 4.0, 经 GitHub API 核实); 商用?是(署名); 再分发?是(署名); 需授权?否
  download_url: https://github.com/AlexTheBad/AP-10K
  paper_url: https://openalex.org/W3196756430  # NeurIPS 2021 D&B Track, arXiv:2108.12617
  citation: Yu et al., 2021, NeurIPS Datasets & Benchmarks. OpenAlex 被引 35 (2026-06-06); last_checked=2026-06-06; oa_id=W3196756430
  leaderboard_url: https://paperswithcode.com/sota/animal-pose-estimation-on-ap-10k
  known_issues: 部分物种样本少、遮挡/截断关键点标注难、跨物种关键点定义统一性受限; domain_scope=动物视觉
  bias_risk: 物种分布不均(哺乳动物为主)、姿态/视角偏差
  privacy_risk: 低
  preprocessing_steps: 检测框裁剪 / 关键点热图生成 / 标准 top-down 姿态增强
  recommended_splits: 官方 train/val/test, 支持跨物种泛化评测
```

```yaml
- dataset_name: APT-36K
  domain: 通用动物 / 姿态估计 + 多目标跟踪
  task: 视频动物 2D 姿态估计 + 姿态跟踪(15 关键点)
  data_type: 动物视频 + 帧(RGB)
  size: 36k 帧, 2.4k 视频片段, 30 物种
  format: 帧图 + 关键点 JSON + track ID
  license: 仓库未声明 LICENSE(GitHub API 返回 None) → 待核查(默认版权归作者, 商用/再分发不明)
  download_url: https://github.com/pandorgan/APT-36K
  paper_url: https://openalex.org/W4282941653  # NeurIPS 2022, arXiv:2206.05683
  citation: Yang et al., 2022, NeurIPS Datasets & Benchmarks. OpenAlex 被引 21 (2026-06-06); last_checked=2026-06-06; oa_id=W4282941653
  leaderboard_url: https://paperswithcode.com/dataset/apt-36k
  known_issues: 跟踪 ID 切换/遮挡丢失、物种样本不均、视频质量差异; domain_scope=动物视觉
  bias_risk: 物种/场景采集偏差
  privacy_risk: 低
  preprocessing_steps: 抽帧 / 关联 track / top-down 裁剪 / 时序平滑
  recommended_splits: 官方划分; 扩展版 APTv2 见 ViTAE-Transformer/APTv2
```

```yaml
- dataset_name: Animal-Pose (Cross-Domain Animal Pose)
  domain: 通用动物 / 2D 姿态估计
  task: 跨域动物 2D 关键点姿态估计(20 关键点)
  data_type: 自然图像(RGB), 5 类家畜/宠物(狗/猫/牛/马/羊)
  size: ~6k 实例(4k+ 图), 含从 VOC 扩展的标注
  format: 关键点 JSON(类 COCO)
  license: 仓库未声明 LICENSE(GitHub API 返回 None); 图像部分源自 PASCAL VOC(研究用途) → 待核查(无开源许可, 图像受 VOC 条款)
  download_url: https://github.com/noahcao/animal-pose-dataset
  paper_url: https://openalex.org/W2983454547  # ICCV 2019, DOI:10.1109/ICCV.2019.00959
  citation: Cao et al., 2019, ICCV. OpenAlex 被引 175 (2026-06-06); last_checked=2026-06-06; oa_id=W2983454547
  leaderboard_url: https://paperswithcode.com/dataset/animal-pose
  known_issues: 类别少(5 类)、关键点定义与人体姿态迁移有 gap、规模偏小; domain_scope=动物视觉
  bias_risk: 物种集中于常见家畜/宠物
  privacy_risk: 低
  preprocessing_steps: 检测框裁剪 / 关键点热图 / 域适应增强
  recommended_splits: 论文设定的 train/test, 常用于跨域(人→动物)迁移评测
```

```yaml
- dataset_name: MammalNet
  domain: 通用哺乳动物 / 视频识别 + 行为理解
  task: 物种识别(173 类) / 组合动作识别(12 行为) / 行为检测
  data_type: 视频(RGB)
  size: ~18k 视频, ~539 小时, 173 哺乳动物类别, 12 通用行为
  format: 视频 + 物种/行为标签 + 时序标注
  license: 代码仓库 MIT License(GitHub API 核实); 视频数据来自公开来源, 使用前须核实逐源条款 → 数据 待核查(逐源版权)
  download_url: https://mammal-net.github.io/
  paper_url: https://openalex.org/W4386065426  # CVPR 2023, DOI:10.1109/CVPR52729.2023.01254
  citation: Chen et al., 2023, CVPR. OpenAlex 被引 36 (2026-06-06); last_checked=2026-06-06; oa_id=W4386065426
  leaderboard_url: https://paperswithcode.com/dataset/mammalnet
  known_issues: 长尾物种分布、行为粒度粗(通用 12 类)、视频来源异构; domain_scope=动物视觉
  bias_risk: 物种采集偏差、网络视频来源偏差
  privacy_risk: 低
  preprocessing_steps: 抽帧 / 时序采样 / 物种-行为联合标签处理
  recommended_splits: 官方 train/val/test
```

```yaml
- dataset_name: iWildCam 2021 Competition Dataset
  domain: 通用野生动物 / 相机陷阱
  task: 物种分类 / 计数 / 跨地点域泛化
  data_type: 相机陷阱图像(RGB, 含日夜/红外)
  size: ~20 万+ 训练图, 数百物种类别(年度赛题, 含 iNat 辅助数据)
  format: JPEG + COCO-Camera-Traps JSON
  license: 多数据归 CC BY 4.0 / 数据集层级公开赛(LILA BC 平台多为 CDLA/CC); 商用?多数允许(逐子集核实); 再分发?是; 需授权?否 → 待核查(逐子集许可)
  download_url: https://github.com/visipedia/iwildcam_comp
  paper_url: https://openalex.org/W3017567979  # The iWildCam 2021 Competition Dataset, arXiv:2105.03494
  citation: Beery et al., 2021, arXiv/CVPR FGVC Workshop. OpenAlex 被引 18 (2026-06-06); last_checked=2026-06-06; oa_id=W3017567979
  leaderboard_url: https://www.kaggle.com/c/iwildcam2021-fgvc8
  known_issues: 极端类别不均、空图(无动物)比例高、夜间/遮挡/运动模糊、跨地点分布偏移; domain_scope=动物视觉
  bias_risk: 地点/物种采集偏差大(域泛化为核心挑战)
  privacy_risk: 低(偶含人类闯入帧, 通常需过滤)
  preprocessing_steps: MegaDetector 预筛动物框 / 空图过滤 / 按地点分域 / 类别加权
  recommended_splits: 官方按地点划分 train/test(测试地点不重叠, 评测域泛化)
```

```yaml
- dataset_name: Animals-10 (Kaggle)
  domain: 通用动物 / 图像分类
  task: 10 类动物图像分类(狗/猫/马/蜘蛛/蝴蝶/鸡/羊/牛/松鼠/象)
  data_type: 自然图像(RGB), 源自 Google Images
  size: ~26k 图, 10 类
  format: 按类别分目录的 JPEG
  license: Kaggle 页标注 GPL-2.0(数据集发布者声明); 图像源自 Google Images, 原始版权归各作者 → 待核查(逐图版权, 教学/研究常用)
  download_url: https://www.kaggle.com/datasets/alessiocorrado99/animals10
  paper_url: 无官方发布论文(Kaggle 社区数据集, 由 Alessio Corrado 发布)
  citation: 无规范学术引用; 相关使用见 OpenAlex W3128016812 (迁移学习动物图像分类, DOI:10.1145/3443467.3443849, 被引 6); last_checked=待核; src=community
  leaderboard_url: https://www.kaggle.com/datasets/alessiocorrado99/animals10/code
  known_issues: 网络爬取标签噪声、类间样本不均、含少量错标/水印图、分辨率不一; domain_scope=动物视觉
  bias_risk: 搜索引擎来源偏差、类别代表性有限
  privacy_risk: 低-中(网络图像偶含人物/水印)
  preprocessing_steps: 去重/清洗水印 / resize / 标准分类增强
  recommended_splits: 无官方划分, 自行 train/val/test(建议分层抽样)
```


---

## 二、家畜专用（奶牛 / 猪 / 羊 个体识别·行为·检测）

```yaml
- dataset_name: Cows2021
  domain: 家畜(奶牛) / 个体识别
  task: Holstein-Friesian 奶牛个体身份识别(视频, 自监督/度量学习)
  data_type: 顶视(俯拍)视频 + 帧(RGB)
  size: ~10k+ 标注图(裁剪个体), 182 头牛; 含定位框与个体 ID
  format: 帧图 + 个体 ID 标签 + 检测框
  license: data.bris 平台, 非商业研究用途, 需同意条款(Non-Commercial Government Licence 类) → 待核查(具体许可以 data.bris 页面为准); 商用?否; 再分发?否; 需授权?是
  download_url: https://data.bris.ac.uk/data/dataset/4vnrca7qw1642qlwxjadp87h7
  paper_url: https://openalex.org/W3176867605  # arXiv:2105.01938
  citation: Gao et al., 2021, BMVC/arXiv. OpenAlex 被引 18 (2026-06-06); last_checked=2026-06-06; oa_id=W3176867605
  leaderboard_url: https://paperswithcode.com/dataset/cows2021
  known_issues: 单一牧场采集、毛色花纹相似个体易混、光照/泥污影响、ID 随时间(换毛)漂移; domain_scope=精准畜牧
  bias_risk: 单场景/单品种(Holstein-Friesian 黑白花)偏差
  privacy_risk: 低(动物); 含牧场位置等元数据需注意
  preprocessing_steps: 个体检测裁剪 / 自监督预训练 / 度量学习 embedding
  recommended_splits: 论文设定(已知/未知个体, 评测开放集再识别)
```

```yaml
- dataset_name: OpenCows2020
  domain: 家畜(奶牛) / 个体识别 + 检测
  task: 奶牛检测 + Holstein-Friesian 个体识别(开放基准)
  data_type: 俯拍/侧拍图像(RGB)
  size: ~4.7k 图(检测) + 个体识别子集(46 头), 含 train/test 划分
  format: 检测框 + 个体 ID 标签
  license: data.bris, 非商业研究用途, 需同意条款 → 待核查(以 data.bris 页面为准); 商用?否; 再分发?否; 需授权?是
  download_url: https://data.bris.ac.uk/data/dataset/10m32xl88x2b61zlkkgz3fml17
  paper_url: https://openalex.org/W3035522863  # Computers and Electronics in Agriculture 2021, DOI:10.1016/j.compag.2021.106133
  citation: Andrew et al., 2021, Comput. Electron. Agric. OpenAlex 被引 162 (2026-06-06); last_checked=2026-06-06; oa_id=W3035522863
  leaderboard_url: https://paperswithcode.com/dataset/opencows2020
  known_issues: 个体数有限、跨牧场泛化差、花纹相似混淆; domain_scope=精准畜牧
  bias_risk: 单品种/有限牧场偏差
  privacy_risk: 低(动物)
  preprocessing_steps: 检测器训练 / 个体裁剪 / 开放集识别评测
  recommended_splits: 官方 train/test(含已知/未知个体协议)
```

```yaml
- dataset_name: AerialCattle2017
  domain: 家畜(奶牛) / 航拍检测与识别
  task: 无人机航拍牛只检测 / 个体识别(Friesian)
  data_type: 无人机(UAV)俯拍 RGB 图像
  size: ~46 头牛, 数千裁剪个体图块(单次航拍区域)
  format: 图像 + 检测框 + 个体 ID
  license: data.bris, 非商业研究用途, 需同意条款 → 待核查(以 data.bris 页面为准); 商用?否; 再分发?否; 需授权?是
  download_url: https://data.bris.ac.uk/data/dataset/3owflku95bxsx24643cybxu3qh
  paper_url: https://openalex.org/W2764259953  # ICCVW 2017, DOI:10.1109/ICCVW.2017.336
  citation: Andrew et al., 2017, ICCV Workshops. OpenAlex 被引 139 (2026-06-06); last_checked=2026-06-06; oa_id=W2764259953
  leaderboard_url: https://paperswithcode.com/dataset/aerialcattle2017
  known_issues: 单次航拍/单牧场、尺度小、背景单一(草地)、泛化受限; domain_scope=精准畜牧
  bias_risk: 单场景/单品种、航拍高度固定
  privacy_risk: 低(动物); 航拍含地块信息
  preprocessing_steps: 航拍图切块 / 牛只检测 / 个体识别
  recommended_splits: 论文设定; 常与 Cows2021/OpenCows 联合做再识别研究
```

```yaml
- dataset_name: Pig Behavior (Two-Stream CNN 视频行为)
  domain: 家畜(猪) / 视频行为识别
  task: 猪只行为识别(进食/饮水/活动等, 双流卷积网络)
  data_type: 监控视频(RGB) + 光流
  size: 论文级数据(单/多栏舍视频片段); 公开下载需按论文数据声明核实
  format: 视频片段 + 行为标签
  license: 论文未提供标准开源数据集; 数据多为「按合理请求提供」 → 待核查(无公开下载链接, 联系作者)
  download_url: 无公开统一下载页(见论文 Data Availability, 通常 on request)
  paper_url: https://openalex.org/W3005865003  # Sensors 2020, DOI:10.3390/s20041085
  citation: Zhang et al., 2020, Sensors. OpenAlex 被引 64 (2026-06-06); last_checked=2026-06-06; oa_id=W3005865003
  leaderboard_url: 无
  known_issues: 数据非公开下载、栏舍场景单一、夜间/遮挡难、行为类别有限; domain_scope=精准畜牧
  bias_risk: 单养殖场/单品种偏差
  privacy_risk: 低(动物); 养殖场商业信息需脱敏
  preprocessing_steps: 抽帧+光流计算 / 双流输入 / 时序采样
  recommended_splits: 论文自定; 公开复现受限于数据可得性
```

```yaml
- dataset_name: Pig Movement & Aggression (Deep Learning)
  domain: 家畜(猪) / 行为检测(攻击/运动)
  task: 猪只运动与攻击行为检测
  data_type: 栏舍监控视频(RGB)
  size: 论文级标注视频(攻击/正常片段); 公开性需按数据声明核实
  format: 视频 + 行为/事件标签
  license: 期刊为开放获取(MDPI Animals, 文章 CC BY 4.0); 数据集本体公开性待核实 → 待核查(数据多为 on request)
  download_url: 见论文 Data Availability(https://www.mdpi.com/journal/animals 文章页)
  paper_url: https://openalex.org/W4387264759  # Animals 2023, DOI:10.3390/ani13193074
  citation: 2023, Animals (MDPI). OpenAlex 被引 34 (2026-06-06); last_checked=2026-06-06; oa_id=W4387264759
  leaderboard_url: 无
  known_issues: 攻击事件稀疏(类别极不均)、遮挡/重叠猪只、标注主观; domain_scope=精准畜牧
  bias_risk: 单场景偏差、事件定义主观
  privacy_risk: 低(动物)
  preprocessing_steps: 事件片段切分 / 不均衡处理 / 时空特征提取
  recommended_splits: 论文自定(事件级划分)
```

```yaml
- dataset_name: Sheep Facial Expression (Pain / Transfer Learning)
  domain: 家畜(绵羊) / 面部表情·疼痛评估
  task: 绵羊面部表情分类(疼痛/正常, SPFES 量表自动化)
  data_type: 绵羊面部图像(RGB)
  size: 论文级面部图集(基于 Sheep Pain Facial Expression Scale 标注); 公开性需核实
  format: 面部裁剪图 + 表情/疼痛等级标签
  license: 期刊为 Elsevier(Computers and Electronics in Agriculture); 数据集本体公开性待核实 → 待核查(数据多为 on request)
  download_url: 见论文(https://doi.org/10.1016/j.compag.2020.105528 Data Availability)
  paper_url: https://openalex.org/W3033615074  # Comput. Electron. Agric. 2020, DOI:10.1016/j.compag.2020.105528
  citation: Noor et al., 2020, Comput. Electron. Agric. OpenAlex 被引 83 (2026-06-06); last_checked=2026-06-06; oa_id=W3033615074
  leaderboard_url: 无
  known_issues: 疼痛标注主观(需兽医)、品种/姿态差异、面部检测前置难; domain_scope=精准畜牧
  bias_risk: 品种/个体偏差、标注者主观
  privacy_risk: 低(动物)
  preprocessing_steps: 面部检测对齐 / 迁移学习微调 / 等级不均处理
  recommended_splits: 论文自定
```

```yaml
- dataset_name: Sheep Face Recognition (Bilinear Feature Fusion)
  domain: 家畜(绵羊) / 个体识别(人脸式)
  task: 绵羊面部个体识别
  data_type: 绵羊面部图像(RGB)
  size: 论文级面部数据集(多个体); 公开性需核实
  format: 面部图 + 个体 ID
  license: 期刊为 MDPI Animals(文章 CC BY 4.0); 数据集本体公开性待核实 → 待核查(数据多为 on request)
  download_url: 见论文(https://doi.org/10.3390/ani13121957 Data Availability)
  paper_url: https://openalex.org/W4380372343  # Animals 2023, DOI:10.3390/ani13121957
  citation: 2023, Animals (MDPI). OpenAlex 被引 32 (2026-06-06); last_checked=2026-06-06; oa_id=W4380372343
  leaderboard_url: 无
  known_issues: 同品种个体相似度高、姿态/光照敏感、需精确面部检测; domain_scope=精准畜牧
  bias_risk: 单品种/单场景偏差
  privacy_risk: 低(动物)
  preprocessing_steps: 面部检测对齐 / 双线性特征融合 / 度量学习
  recommended_splits: 论文自定(开放集/闭集识别)
```

```yaml
- dataset_name: Sheep videos from drone (Zenodo)
  domain: 家畜(绵羊) / 航拍检测计数
  task: 低空无人机绵羊检测 / 计数
  data_type: 无人机(UAV)低空视频(RGB)
  size: 多段低空航拍绵羊视频(Zenodo 公开记录)
  format: 视频文件(可抽帧标注)
  license: Zenodo 记录, 通常 CC(以记录页声明为准) → 待核查(逐记录许可); 多为开放下载
  download_url: https://doi.org/10.5281/zenodo.10400302
  paper_url: https://openalex.org/W4393664673  # Zenodo dataset record, DOI:10.5281/zenodo.10400302
  citation: 2023, Zenodo dataset. OpenAlex 被引 1 (2026-06-06); last_checked=2026-06-06; oa_id=W4393664673
  leaderboard_url: 无
  known_issues: 无现成框/ID 标注(原始视频)、羊群密集重叠、尺度小; domain_scope=精准畜牧
  bias_risk: 单场景/单次飞行偏差
  privacy_risk: 低(动物); 航拍地块信息
  preprocessing_steps: 抽帧 / 自行标注检测框 / 密集小目标检测
  recommended_splits: 无官方划分, 自定
```

---

## 三、奶山羊（dairy goat）专项 — 诚实核查结果

> 【关键诚实说明】本节专门检索 "dairy goat behavior / detection dataset"（OpenAlex + WebSearch + GitHub API，2026-06-06）。
> 与任务预期"很可能不存在公开数据集"不同，实际**检索到数张真实公开/半公开的山羊(含奶山羊)数据集**，如实建卡如下；
> 同时附「现状评估 + 自建数据集建议」。下列每张卡的论文/链接均经真实 curl/WebSearch 核实，**未编造任何数据集名称或链接**。

```yaml
- dataset_name: GoatABRD (Goat Abnormal Behavior Recognition Dataset)
  domain: 奶山羊 / 行为识别(异常+常见)
  task: 山羊行为识别 — 4 异常(跛行 limping / 攻击 attacking / 死亡 death / 啃咬 gnawing) + 6 常见(站/卧/吃/饮/抓挠/梳理)
  data_type: 栏舍监控视频/图像(RGB)
  size: 10 类行为标注数据集(规模以仓库 README 为准)
  format: 图像/帧 + 行为标签(检测/分类)
  license: GitHub 仓库未声明 LICENSE(GitHub API 返回 None) → 待核查(默认版权归作者, 使用前建议联系); 公开可见但许可不明
  download_url: https://github.com/sunianbei/GoatABRD-Dataset
  paper_url: https://openalex.org/W4405572779  # A Real-Time Lightweight Behavior Recognition Model for Multiple Dairy Goats (GSCW-YOLO), Animals 2024, DOI:10.3390/ani14243667
  citation: 2024, Animals (MDPI). OpenAlex 被引 10 (2026-06-06); 预印本 W4403010363 (Research Square, DOI:10.21203/rs.3.rs-4994192/v1); last_checked=2026-06-06; oa_id=W4405572779
  leaderboard_url: 无
  known_issues: 异常行为(死亡/攻击)样本极稀疏、单场景采集、许可未明; domain_scope=精准畜牧-奶山羊
  bias_risk: 单牧场/单品种偏差、异常类别极不均衡
  privacy_risk: 低(动物); 养殖场信息
  preprocessing_steps: 抽帧 / 行为时序切分 / 异常类过采样或加权 / YOLO 式检测标注
  recommended_splits: 以仓库/论文为准(自定 train/val/test)
```

```yaml
- dataset_name: CherryChèvre
  domain: 奶山羊/山羊 / 自然环境检测
  task: 自然放牧环境下细粒度山羊检测(bounding box)
  data_type: 自然环境(户外牧场)RGB 图像
  size: 数千张标注图(细粒度个体框, YOLO 格式版本可下载)
  format: 图像 + YOLO/COCO 检测标注
  license: Recherche Data Gouv(法国国家科研数据平台)公开数据集, DOI 直链可下载; 多为 etalab/CC 开放许可 → 待核查(以记录页许可字段为准); 通常允许研究使用
  download_url: https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi:10.57745/4C03OG
  paper_url: https://openalex.org/W4387529049  # Scientific Data 2023, DOI:10.1038/s41597-023-02555-8
  citation: 2023, Scientific Data (Nature). OpenAlex 被引 8 (2026-06-06); last_checked=2026-06-06; oa_id=W4387529049
  leaderboard_url: 无
  known_issues: 仅检测(无行为/姿态)、单地区采集、自然光照/遮挡变化大; domain_scope=精准畜牧-奶山羊
  bias_risk: 单牧场/地域偏差
  privacy_risk: 低(动物)
  preprocessing_steps: YOLO 格式直接训练 / 自然场景检测增强 / 多尺度
  recommended_splits: 数据集自带划分(以记录页为准)
```

```yaml
- dataset_name: DiaryGoatMVT (Dairy Goat Multiple Visual Tasks)
  domain: 奶山羊 / 多视觉任务(检测/分类等)
  task: 奶山羊多视觉任务数据集(repo 描述 Multiple Visual Tasks)
  data_type: 奶山羊图像/视频(RGB)
  size: 以仓库 README 为准(多任务标注)
  format: 图像 + 多任务标注
  license: GitHub 仓库未声明 LICENSE(GitHub API 返回 None) → 待核查(默认版权归作者, 建议联系作者); 公开可见但许可不明
  download_url: https://github.com/tiana-tang/DiaryGoatMVT
  paper_url: 暂未在 OpenAlex 检索到对应已发表论文(2026-06-06); 视为社区/课题组发布的数据仓库
  citation: 无规范学术引用(仓库, 引用前请核实是否有配套论文); last_checked=待核; src=community
  leaderboard_url: 无
  known_issues: 缺配套论文/规模文档、许可未明、维护状态需核实; domain_scope=精准畜牧-奶山羊
  bias_risk: 单课题组/单场景偏差
  privacy_risk: 低(动物)
  preprocessing_steps: 按任务解析标注 / 标准检测或分类流程
  recommended_splits: 以仓库为准
```

```yaml
- dataset_name: 【现状评估卡】奶山羊专用公开数据集 — 稀缺但非空白
  domain: 奶山羊 / 元说明(非数据集)
  task: 说明奶山羊数据现状 + 可迁移近缘数据 + 自建建议
  data_type: 不适用(说明卡)
  size: 不适用
  format: 不适用
  license: 不适用
  download_url: 不适用
  paper_url: 参考综述 https://openalex.org/W4399830201  # Public Computer Vision Datasets for Precision Livestock Farming: A Systematic Survey, arXiv:2406.10628 (2024, 被引 3)
  citation: 见上述精准畜牧 CV 数据集系统综述(可核查现有家畜 CV 数据集全景); last_checked=待核; src=community
  leaderboard_url: 不适用
  known_issues: 说明卡而非单一数据集；结论依赖 2026-06-06 前的公开检索快照，使用前应复核新发布数据集与许可证; domain_scope=精准畜牧-奶山羊
  bias_risk: 说明卡本身无采样偏差；其总结的公开奶山羊数据多为单场景/小规模/许可不明，存在领域覆盖偏差
  现状结论: |
    截至 2026-06-06 真实核查:
    1) 奶山羊"专用"公开数据集确实**稀缺**, 但**非完全空白** —
       本节 GoatABRD(行为)、CherryChèvre(检测)、DiaryGoatMVT(多任务) 为真实可访问资源;
       其中仅 CherryChèvre 有 DOI 支撑且明确直链下载, GoatABRD/DiaryGoatMVT 许可未声明、需联系作者。
    2) 缺口: 暂未找到大规模、有标准开源许可、覆盖"奶山羊姿态关键点 + 多场景 + 个体ID"的综合公开基准。
    3) 行为识别近作(GSCW-YOLO 2024 / YOLO11+ELSlowFast-LSTM 2025)多自建私有数据, 公开性有限。
  可迁移近缘数据: |
    - 检测/计数: CherryChèvre(同为山羊, 最直接) > Sheep videos from drone(绵羊航拍) > AerialCattle2017。
    - 姿态: AP-10K / APT-36K(含偶蹄目/羊近缘物种关键点) + Animal-Pose(含 sheep 类) 做迁移预训练。
    - 行为: MammalNet / Animal Kingdom 通用行为预训练 + GoatABRD 微调。
    - 面部/个体ID: Sheep Face Recognition / goat face recognition(W4211164812, DOI:10.1016/j.compag.2022.106730, 被引92) 做方法迁移。
  自建数据集建议: |
    采集方案: 多牧场/多季节/昼夜(含红外)覆盖域差异; 顶视(俯拍, 利于个体不重叠)+ 侧视(利于行为/步态)双视角;
              固定监控 + 移动/航拍补充; 同步耳标/RFID 作个体 ID ground truth。
    标注体系: (a)检测框(羊只/头部); (b)2D 姿态关键点(建议 17-20 点, 对齐 AP-10K 便于迁移);
              (c)个体 ID(再识别); (d)行为类(站/卧/反刍/采食/饮水/走动/争斗/跛行 等, 异常单列);
              (e)时序事件标注(发情/产前/疾病前兆等可选)。
    规模建议: 起步 ≥ 5k-10k 标注帧 + ≥ 50 个体做 ID; 行为按类 ≥ 数百段, 异常类专门补采;
              划分按"牧场/时间"留出做域泛化测试(勿随机泄漏)。
    合规: 养殖场授权 + 位置/商业信息脱敏; 发布建议 CC BY 4.0 或 CDLA, 附 datasheet(动机/采集/标注/局限)。
  privacy_risk: 自建需注意养殖场商业信息与人员入镜脱敏
  preprocessing_steps: 不适用(建议见上)
  recommended_splits: 自建务必按牧场/时间分域划分以评测泛化
```

---

## 汇总

- 总卡数: **19** 张(含 1 张奶山羊现状评估说明卡)。
- 通用动物(7): Animal Kingdom / AP-10K / APT-36K / Animal-Pose / MammalNet / iWildCam 2021 / Animals-10。
- 家畜专用(8): Cows2021 / OpenCows2020 / AerialCattle2017 / Pig 双流行为 / Pig 运动攻击 / Sheep 面部表情 / Sheep 面部识别 / Sheep 航拍。
- 奶山羊专项(4, 含说明卡): GoatABRD / CherryChèvre / DiaryGoatMVT / 现状评估卡。
- license 明确: AP-10K(CC BY 4.0)、MammalNet 代码(MIT); data.bris 系列为非商业研究(待核查具体条款); 多数家畜/羊数据为论文 on-request 或仓库未声明许可 → 已逐条标「待核查」。
- 诚实声明: 所有 paper_url/被引/DOI 来自真实 OpenAlex curl; 下载页/license 经 WebSearch+GitHub API 核实; 奶山羊数据**未编造** —— 找到的真实资源如实建卡, 缺口与许可不明处明确标注。
