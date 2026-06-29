# db04 — CV / NLP 数据集卡（cards_cv_nlp）

> 每条记录 license 与 商用/再分发/隐私 限制（联动 a10）。受版权数据仅存元数据与链接。
> 论文 paper_url / citation 来自 OpenAlex 实时 curl（2026-06-06）；license/官方下载页经 WebSearch 核实，许可不确定者标「待核查」。
> 被引数为查询当日 OpenAlex `cited_by_count` 快照，会随时间增长。

---

## 一、计算机视觉 (CV)

```yaml
- dataset_name: "ImageNet (ILSVRC)"
  domain: "计算机视觉"
  task: "图像分类 / 目标定位"
  data_type: "自然图像 (RGB)"
  size: "~14M 标注图(全库); ILSVRC-2012 子集 ~1.28M 训练 / 50k 验证 / 100k 测试, 1000 类"
  format: "JPEG + XML/synset 标注"
  license: "仅限非商业研究, 需注册并同意 terms of access; 不可再分发原图(只授权访问)。商用?否; 再分发?否(受限); 需授权?是(注册)"
  download_url: "https://image-net.org/download.php"
  paper_url: "https://openalex.org/W2117539524"  # ImageNet Large Scale Visual Recognition Challenge (IJCV 2015), DOI:10.1007/s11263-015-0816-y
  citation: "Russakovsky et al., 2015, IJCV. OpenAlex 被引 40,129 (2026-06-06); last_checked=2026-06-06; oa_id=W2117539524"
  leaderboard_url: "https://paperswithcode.com/sota/image-classification-on-imagenet"
  known_issues: "标签噪声(约5-6%)、类别粒度不均、多目标图只给单标签、val/test 标签泄漏争议; domain_scope=通用CV"
  bias_risk: "地域/文化偏差(西方中心)、部分 person 子树含冒犯性/刻板印象类别(已部分下线)"
  privacy_risk: "含可识别人物图像, 未经被摄者同意, 隐私与肖像权争议"
  preprocessing_steps: "resize 短边256 / center 或 random crop 224 / 通道均值方差归一化(ImageNet mean-std)"
  recommended_splits: "ILSVRC-2012 官方 train/val; 测试集标签不公开(需提交)"
```

```yaml
- dataset_name: "MS COCO (Common Objects in Context)"
  domain: "计算机视觉"
  task: "目标检测 / 实例分割 / 关键点 / 图像描述(captioning)"
  data_type: "自然图像 (RGB) + 多类型标注"
  size: "~330k 图(>200k 标注), 80 物体类(检测), 91 stuff 类(分割), ~1.5M 实例, 5 caption/图"
  format: "JPEG + COCO JSON 标注"
  license: "标注为 CC BY 4.0(可商用/再分发需署名); 图像来自 Flickr, 版权归原作者, 仅按 Flickr 条款使用。商用?标注可/图像受限; 再分发?标注可/图像否; 需授权?图像受原始版权约束。建议核实逐图授权 → 待核查(逐图版权)"
  download_url: "https://cocodataset.org/#download"
  paper_url: "https://openalex.org/W1861492603"  # Microsoft COCO: Common Objects in Context (ECCV 2014), DOI:10.1007/978-3-319-10602-1_48
  citation: "Lin et al., 2014, ECCV. OpenAlex 被引 42,032 (2026-06-06); last_checked=2026-06-06; oa_id=W1861492603"
  leaderboard_url: "https://paperswithcode.com/sota/object-detection-on-coco"
  known_issues: "小目标标注难、部分实例漏标、stuff/thing 边界模糊、caption 多样性有限; domain_scope=通用CV"
  bias_risk: "日常生活场景偏差、地域/场景分布不均、person 类占比高"
  privacy_risk: "含可识别人物(Flickr 图), 肖像/隐私风险"
  preprocessing_steps: "按 COCO API 解析 JSON / resize+padding / 检测多尺度增强"
  recommended_splits: "train2017(118k) / val2017(5k) / test-dev(需提交评测)"
```

```yaml
- dataset_name: "PASCAL VOC (2007/2012)"
  domain: "计算机视觉"
  task: "目标检测 / 语义分割 / 图像分类"
  data_type: "自然图像 (RGB)"
  size: "VOC2012 ~11.5k 图(检测/分类), 20 类; 分割子集 ~2.9k 标注图"
  format: "JPEG + Pascal VOC XML / 分割 PNG"
  license: "图像来自 flickr, 数据集\"仅供研究/教育, 非商业\"使用; 官方未给标准开源许可。商用?否; 再分发?受限; 需授权?注册下载。 → 待核查(无标准许可文本)"
  download_url: "http://host.robots.ox.ac.uk/pascal/VOC/"
  paper_url: "https://openalex.org/W2031489346"  # The PASCAL VOC Challenge (IJCV 2010), DOI:10.1007/s11263-009-0275-4
  citation: "Everingham et al., 2010, IJCV. OpenAlex 被引 19,471 (2026-06-06); last_checked=2026-06-06; oa_id=W2031489346"
  leaderboard_url: "https://paperswithcode.com/sota/object-detection-on-pascal-voc-2012"
  known_issues: "规模小(已被 COCO 取代)、类别少、难样本标注主观、VOC07 用 11-point AP, VOC12 用插值 AP 不一致; domain_scope=通用CV"
  bias_risk: "类别/场景偏差、欧洲 Flickr 来源偏差"
  privacy_risk: "含人物图像, 隐私风险中等"
  preprocessing_steps: "解析 VOC XML / 标准检测增强 / 分割掩码读取(忽略 255 边界)"
  recommended_splits: "VOC07 train/val/test(test 公开); VOC12 train/val(test 需提交)"
```

```yaml
- dataset_name: "CIFAR-10 / CIFAR-100"
  domain: "计算机视觉"
  task: "图像分类"
  data_type: "彩色图像 32x32 (RGB)"
  size: "各 60k 图(50k 训练 / 10k 测试); CIFAR-10 = 10 类, CIFAR-100 = 100 类(20 超类)"
  format: "Python pickle / 二进制, 各库内置"
  license: "公开供研究使用(Tiny Images 子集), 通常视为自由学术使用; 无显式商用许可声明。商用?未明确; 再分发?常见镜像存在; 需授权?否。 → 待核查(商用条款)"
  download_url: "https://www.cs.toronto.edu/~kriz/cifar.html"
  paper_url: "https://openalex.org/W3118608800"  # Learning Multiple Layers of Features from Tiny Images (2009 tech report)
  citation: "Krizhevsky, 2009, Tech Report, Univ. Toronto. OpenAlex 被引 25,499 (2026-06-06); last_checked=2026-06-06; oa_id=W3118608800"
  leaderboard_url: "https://paperswithcode.com/sota/image-classification-on-cifar-10"
  known_issues: "分辨率低、测试集与训练集存在近重复样本、CIFAR-100 部分细类易混; 来源 Tiny Images 母集因含冒犯内容已被撤下; domain_scope=通用CV"
  bias_risk: "类别/来源偏差; 母数据集 Tiny Images 含问题标签"
  privacy_risk: "低(物体/动物为主), 但源自网络爬取图像"
  preprocessing_steps: "per-channel 归一化 / random crop(pad 4) / 水平翻转"
  recommended_splits: "官方 50k/10k; 常从训练集划 5k 做 val"
```

```yaml
- dataset_name: "MNIST"
  domain: "计算机视觉"
  task: "手写数字分类"
  data_type: "灰度图像 28x28"
  size: "70k (60k 训练 / 10k 测试), 10 类"
  format: "IDX 二进制 / 各框架内置"
  license: "原始 NIST 数据为美国政府公共领域衍生; 常按自由使用对待, 官方页未附标准许可。商用?一般可; 再分发?可; 需授权?否。 → 待核查(无显式许可文本)"
  download_url: "http://yann.lecun.com/exdb/mnist/"  # 原站时有失效, 镜像见各框架 datasets
  paper_url: "https://openalex.org/W2112796928"  # Gradient-based learning applied to document recognition (Proc. IEEE 1998), DOI:10.1109/5.726791
  citation: "LeCun et al., 1998, Proc. IEEE. OpenAlex 被引 57,987 (2026-06-06); last_checked=2026-06-06; oa_id=W2112796928"
  leaderboard_url: "https://paperswithcode.com/sota/image-classification-on-mnist"
  known_issues: "过于简单已饱和(>99.7%)、仅适合教学/快速验证、官方原始下载链接不稳定; domain_scope=通用CV"
  bias_risk: "低(美国人口普查/高中生书写者), 字体风格偏差"
  privacy_risk: "无(匿名手写数字)"
  preprocessing_steps: "归一化到 [0,1] 或标准化(mean 0.1307, std 0.3081)"
  recommended_splits: "官方 60k/10k"
```

```yaml
- dataset_name: "ADE20K"
  domain: "计算机视觉"
  task: "语义分割 / 场景解析 / 实例分割"
  data_type: "自然图像 (RGB) + 像素级标注"
  size: "~20k 训练 / 2k 验证 / 3k 测试; >3000 物体+部件类(SceneParse150 用 150 类子集)"
  format: "JPEG + 分割 PNG / 标注 mat"
  license: "BSD 3-Clause(MIT CSAIL 发布); 学术研究使用, 注册下载。商用?需核实(BSD 通常允许, 但站点限研究用途存在张力); 再分发?BSD 允许保留声明; 需授权?注册。 → 待核查(研究限定 vs BSD 商用条款冲突)"
  download_url: "https://groups.csail.mit.edu/vision/datasets/ADE20K/"  # 及 http://sceneparsing.csail.mit.edu/
  paper_url: "https://openalex.org/W2737258237"  # Scene Parsing through ADE20K Dataset (CVPR 2017), DOI:10.1109/cvpr.2017.544
  citation: "Zhou et al., 2017, CVPR. OpenAlex 被引 3,154 (2026-06-06); last_checked=2026-06-06; oa_id=W2737258237"
  leaderboard_url: "https://paperswithcode.com/sota/semantic-segmentation-on-ade20k"
  known_issues: "长尾类别极不均衡、标注粒度差异大、部件标注稀疏、全类评测困难(常用 150 类); domain_scope=通用CV"
  bias_risk: "场景类型偏室内/城市、类别长尾"
  privacy_risk: "含可识别人物与场所, 隐私风险中等"
  preprocessing_steps: "resize/crop(常 512x512) / 类别映射到 150 / 忽略 0 背景标签"
  recommended_splits: "官方 train/val; SceneParse150 标准设置"
```

```yaml
- dataset_name: "Cityscapes"
  domain: "计算机视觉 (自动驾驶)"
  task: "城市街景语义/实例/全景分割"
  data_type: "车载立体相机图像 (2048x1024 RGB)"
  size: "5k 精标注(2975/500/1525) + 20k 粗标注; 19 评测类(30 标注类), 50 城市"
  format: "PNG + 分割标注 PNG/JSON polygon"
  license: "自定义协议, 仅限非商业/学术研究, 需注册同意; 禁止商用与再分发。商用?否; 再分发?否; 需授权?是(注册并同意条款)"
  download_url: "https://www.cityscapes-dataset.com/downloads/"
  paper_url: "https://openalex.org/W2340897893"  # The Cityscapes Dataset for Semantic Urban Scene Understanding (CVPR 2016), DOI:10.1109/cvpr.2016.350
  citation: "Cordts et al., 2016, CVPR. OpenAlex 被引 11,884 (2026-06-06); last_checked=2026-06-06; oa_id=W2340897893"
  leaderboard_url: "https://www.cityscapes-dataset.com/benchmarks/"
  known_issues: "仅德国及周边城市、天气/光照偏好晴天、粗标注噪声、夜间/恶劣天气样本少; domain_scope=自动驾驶-特定地域"
  bias_risk: "地域(德语区)/气候/季节偏差, 泛化到其他城市受限"
  privacy_risk: "含行人/车牌等可识别信息(官方做了部分模糊处理)"
  preprocessing_steps: "标签 ID 映射到 train ID(19 类) / random crop / 多尺度增强"
  recommended_splits: "官方 train(2975)/val(500)/test(1525, 需提交)"
```

```yaml
- dataset_name: "CelebA (CelebFaces Attributes)"
  domain: "计算机视觉 (人脸)"
  task: "人脸属性识别 / 人脸检测对齐 / 生成模型基准"
  data_type: "名人人脸图像 (RGB)"
  size: "~202,599 图, 10,177 身份, 40 属性标注, 5 landmark"
  format: "JPEG + 属性 txt / landmark txt; 另有 CelebA-HQ 30k 高清"
  license: "仅限非商业研究使用; 图像版权归原属(网络收集), 不可商用。商用?否; 再分发?受限; 需授权?同意非商业条款"
  download_url: "https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html"
  paper_url: "https://openalex.org/W1834627138"  # Deep Learning Face Attributes in the Wild (ICCV 2015), DOI:10.1109/iccv.2015.425
  citation: "Liu et al., 2015, ICCV. OpenAlex 被引 7,667 (2026-06-06); last_checked=2026-06-06; oa_id=W1834627138"
  leaderboard_url: "https://paperswithcode.com/dataset/celeba"
  known_issues: "名人偏差(妆容/灯光/角度非自然分布)、属性标注主观且二值化、身份标签噪声; domain_scope=通用CV"
  bias_risk: "严重人口学偏差(肤色/年龄/性别分布不均), 公平性研究常用反例"
  privacy_risk: "高 — 真实可识别人脸, 未经被摄者同意, 肖像/生物特征隐私风险"
  preprocessing_steps: "人脸对齐裁剪(178x218 或 align&crop 128) / 归一化"
  recommended_splits: "官方 train/val/test 按身份不重叠划分(162770/19867/19962)"
```

```yaml
- dataset_name: "Open Images (V4–V7)"
  domain: "计算机视觉"
  task: "图像分类 / 目标检测 / 视觉关系 / 实例分割 / 局部叙述"
  data_type: "自然图像 (RGB)"
  size: "~9M 图; V4: 600 检测类 ~15.4M 框; 另有分割掩码/关系标注"
  format: "JPEG(Flickr URL) + CSV/标注; 标注 CC BY 4.0"
  license: "标注 CC BY 4.0(可商用/再分发需署名); 图像为 Flickr CC-BY 2.0, 版权归原作者。商用?标注可+图像按各自 CC; 再分发?标注可/图像按 CC; 需授权?否(遵守署名)"
  download_url: "https://storage.googleapis.com/openimages/web/download.html"
  paper_url: "https://openalex.org/W4288083516"  # The Open Images Dataset V4 (IJCV 2020), DOI:10.1007/s11263-020-01316-z
  citation: "Kuznetsova et al., 2020, IJCV. OpenAlex 被引 1,607 (2026-06-06); last_checked=2026-06-06; oa_id=W4288083516"
  leaderboard_url: "https://paperswithcode.com/sota/object-detection-on-open-images-v6"
  known_issues: "标注不完全(部分类别只验证存在的框, 漏标多)、机器+人工混合标注质量不一、类别层级复杂; domain_scope=通用CV"
  bias_risk: "网络爬取分布偏差、类别长尾、地域偏差"
  privacy_risk: "含可识别人物(Flickr 图), 隐私/肖像风险"
  preprocessing_steps: "按 image-id 下载 / 解析层级标签 / 处理 group-of 框与负标签"
  recommended_splits: "官方 train/validation/test"
```

---

## 二、自然语言处理 (NLP)

```yaml
- dataset_name: "GLUE"
  domain: "NLP"
  task: "自然语言理解多任务基准(9 任务: CoLA/SST-2/MRPC/STS-B/QQP/MNLI/QNLI/RTE/WNLI)"
  data_type: "英文文本(句/句对)"
  size: "各子任务规模不一(数百到 ~40 万对)"
  format: "TSV / 在线评测"
  license: "基准聚合器为研究用途; 各子任务原始许可不一(如 MRPC 受微软研究协议, QQP 受 Quora 条款)。商用?整体不保证; 再分发?各子任务受限; 需授权?部分子任务需。 → 待核查(逐子任务许可)"
  download_url: "https://gluebenchmark.com/tasks"
  paper_url: "https://openalex.org/W2923014074"  # GLUE (EMNLP 2018 BlackboxNLP), DOI:10.18653/v1/w18-5446
  citation: "Wang et al., 2018, ICLR/EMNLP-Workshop. OpenAlex 被引 3,941 (2026-06-06); last_checked=2026-06-06; oa_id=W2923014074"
  leaderboard_url: "https://gluebenchmark.com/leaderboard"
  known_issues: "多任务已饱和(超人类基线), 部分任务(WNLI)训练集有陷阱、被 SuperGLUE 接棒; domain_scope=通用NLP"
  bias_risk: "子任务含标注 artifact(假设偏置)、来源分布偏差"
  privacy_risk: "低-中(部分来自 Quora/新闻/影评公开文本)"
  preprocessing_steps: "分词/截断到 max_len / 句对拼接 [CLS]A[SEP]B[SEP]"
  recommended_splits: "各任务官方 train/dev/test(test 在线提交)"
```

```yaml
- dataset_name: "SuperGLUE"
  domain: "NLP"
  task: "更难的 NLU 多任务基准(8 任务: BoolQ/CB/COPA/MultiRC/ReCoRD/RTE/WiC/WSC)"
  data_type: "英文文本(含推理/共指/阅读理解)"
  size: "各子任务数百到数万样本"
  format: "JSONL / 在线评测"
  license: "聚合基准研究用途; 各子任务许可不一(多为 CC BY 或研究许可)。商用?不保证; 再分发?各子任务受限; 需授权?部分需。 → 待核查(逐子任务许可)"
  download_url: "https://super.gluebenchmark.com/tasks"
  paper_url: "https://openalex.org/W2943552823"  # SuperGLUE (NeurIPS 2019), arXiv:1905.00537
  citation: "Wang et al., 2019, NeurIPS. OpenAlex 被引 991 (2026-06-06); last_checked=2026-06-06; oa_id=W2943552823"
  leaderboard_url: "https://super.gluebenchmark.com/leaderboard"
  known_issues: "同样已被大模型刷至接近饱和、部分任务样本量小方差大、WSC 共指难; domain_scope=通用NLP"
  bias_risk: "标注 artifact、来源分布偏差"
  privacy_risk: "低(公开来源文本)"
  preprocessing_steps: "任务特定格式化(问句+段落/选项拼接) / 分词截断"
  recommended_splits: "各任务官方 train/val/test(test 在线提交)"
```

```yaml
- dataset_name: "SQuAD (1.1 / 2.0)"
  domain: "NLP"
  task: "抽取式阅读理解 / 问答"
  data_type: "英文文本(维基段落 + 问答对)"
  size: "SQuAD1.1 ~10.7 万问答(536 篇维基); SQuAD2.0 增加 ~5 万不可回答问题"
  format: "JSON"
  license: "CC BY-SA 4.0(署名+相同方式共享); 可商用/再分发需遵守 SA 条款(基于维基百科文本)"
  download_url: "https://rajpurkar.github.io/SQuAD-explorer/"
  paper_url: "https://openalex.org/W2963748441"  # SQuAD: 100,000+ Questions (EMNLP 2016), DOI:10.18653/v1/d16-1264
  citation: "Rajpurkar et al., 2016, EMNLP. OpenAlex 被引 6,308 (2026-06-06); 2.0 见 Rajpurkar et al., 2018, ACL (DOI:10.18653/v1/p18-2124, 被引 2,155); last_checked=2026-06-06; oa_id=W2963748441"
  leaderboard_url: "https://rajpurkar.github.io/SQuAD-explorer/"
  known_issues: "答案为段落内连续 span(限制题型)、众包问题与文本词汇重叠高(浅层匹配可解)、已基本饱和; domain_scope=通用NLP"
  bias_risk: "维基百科主题/写作风格偏差、众包标注模式偏差"
  privacy_risk: "低(维基公开文本)"
  preprocessing_steps: "段落+问题拼接 / 答案 span 字符→token 对齐 / 滑窗处理长文档"
  recommended_splits: "官方 train/dev; test 隐藏(需提交至排行榜)"
```

```yaml
- dataset_name: "WikiText (WikiText-2 / WikiText-103)"
  domain: "NLP"
  task: "语言建模(困惑度评测)"
  data_type: "英文长文本(维基百科 Good/Featured 文章)"
  size: "WikiText-2 ~2M tokens; WikiText-103 ~1.03 亿 tokens, 词表 ~26.7 万"
  format: "纯文本(保留标点/大小写/换行)"
  license: "CC BY-SA 3.0(基于维基百科); 可商用/再分发需遵守 SA 署名"
  download_url: "https://blog.salesforceairesearch.com/the-wikitext-long-term-dependency-language-modeling-dataset/"  # 或各框架 datasets
  paper_url: "https://openalex.org/W2525332836"  # Pointer Sentinel Mixture Models (ICLR 2017), arXiv:1609.07843
  citation: "Merity et al., 2016/2017, ICLR. OpenAlex 被引 484 (2026-06-06); last_checked=2026-06-06; oa_id=W2525332836"
  leaderboard_url: "https://paperswithcode.com/sota/language-modelling-on-wikitext-103"
  known_issues: "仅维基文本(领域单一)、PPL 受词表/tokenization 影响不可跨设置直接比较、长尾词 <unk> 处理差异; domain_scope=通用NLP"
  bias_risk: "维基主题/编者偏差、英文为主"
  privacy_risk: "低(维基公开文本)"
  preprocessing_steps: "词级 tokenization / 构建词表(频次截断) / 连续拼接成长序列做 BPTT"
  recommended_splits: "官方 train/valid/test"
```

```yaml
- dataset_name: "Common Crawl / C4 (Colossal Clean Crawled Corpus)"
  domain: "NLP"
  task: "大规模语言模型预训练语料"
  data_type: "网页爬取文本"
  size: "Common Crawl 每月数百 TB; C4(en) 清洗后 ~750GB / ~3.65 亿文档"
  format: "WARC/WET(CC); C4 为 TFDS/JSON"
  license: "Common Crawl 数据按其 ToU(基于网页, 版权归原网站); C4 衍生数据标注为 ODC-BY 1.0(开放数据署名)。商用?C4 ODC-BY 允许商用需署名+遵守 CC ToU; 再分发?ODC-BY 允许; 但底层网页版权与隐私存在不确定 → 待核查(底层网页内容版权/隐私)"
  download_url: "https://commoncrawl.org/get-started"  # C4: https://huggingface.co/datasets/allenai/c4
  paper_url: "https://openalex.org/W2981852735"  # Exploring the Limits of Transfer Learning (T5/C4), arXiv:1910.10683, JMLR 2020
  citation: "Raffel et al., 2020, JMLR (T5). OpenAlex 被引 8,337 (含各版本, 2026-06-06); last_checked=待核; oa_id=W2981852735"
  leaderboard_url: "无统一榜(作为预训练语料使用)"
  known_issues: "启发式清洗丢弃大量内容、含重复/低质/模板文本、毒性与偏见内容、去重不彻底、可能含基准测试泄漏; domain_scope=通用NLP"
  bias_risk: "高 — 网页分布偏差(英语/西方/男性视角)、放大社会偏见与刻板印象、文档化研究(Dodge et al. 2021)指出过滤误伤少数群体方言"
  privacy_risk: "高 — 可能含个人信息/PII、版权内容, 未经同意爬取"
  preprocessing_steps: "语言识别 / 去重(MinHash) / 质量与毒性过滤 / 去 PII(部分管线)"
  recommended_splits: "预训练无标准 split; C4 提供 train/validation"
```

```yaml
- dataset_name: "IMDB (Large Movie Review Dataset)"
  domain: "NLP"
  task: "情感二分类(影评 正/负)"
  data_type: "英文影评文本"
  size: "50k 标注(25k 训练 / 25k 测试) + 50k 无标注"
  format: "纯文本(每条一文件) / 各库内置"
  license: "学术研究使用(Stanford AI Lab 发布), 未附标准开源许可; 评论文本版权属 IMDb/原作者。商用?未明确; 再分发?常见镜像; 需授权?否。 → 待核查(无显式许可文本)"
  download_url: "https://ai.stanford.edu/~amaas/data/sentiment/"
  paper_url: "https://openalex.org/W2113459411"  # Learning Word Vectors for Sentiment Analysis (ACL 2011)
  citation: "Maas et al., 2011, ACL. OpenAlex 被引 3,298 (2026-06-06); last_checked=2026-06-06; oa_id=W2113459411"
  leaderboard_url: "https://paperswithcode.com/sota/sentiment-analysis-on-imdb"
  known_issues: "二分类去除中性(评分 5-6)分布偏极端、已饱和(>96%)、评论长度差异大; domain_scope=通用NLP"
  bias_risk: "影评领域偏差、极性人工筛选偏差"
  privacy_risk: "低(公开影评), 但含用户撰写内容"
  preprocessing_steps: "HTML 清洗 / 分词截断 / 词表或子词编码"
  recommended_splits: "官方 25k/25k; 常从训练集划 val"
```

```yaml
- dataset_name: "SNLI / MultiNLI (MNLI)"
  domain: "NLP"
  task: "自然语言推理(蕴含/中立/矛盾 三分类)"
  data_type: "英文句对(前提-假设)"
  size: "SNLI ~57 万对(基于 Flickr30k caption); MNLI ~43 万对(10 个体裁, 跨领域)"
  format: "JSONL / TSV"
  license: "SNLI = CC BY-SA 4.0; MNLI = 多数样本 OANC 等公开来源, 整体研究使用(部分子来源许可不一)。商用?SNLI 可(SA)/MNLI 部分受限; 再分发?SNLI 可/MNLI 受限; 需授权?否。 → MNLI 逐来源许可待核查"
  download_url: "https://nlp.stanford.edu/projects/snli/"  # MNLI: https://cims.nyu.edu/~sbowman/multinli/
  paper_url: "https://openalex.org/W1840435438"  # SNLI: A large annotated corpus for NLI (EMNLP 2015), DOI:10.18653/v1/d15-1075
  citation: "Bowman et al., 2015, EMNLP, 被引 3,440; MNLI = Williams et al., 2018, NAACL (https://openalex.org/W2607892599, DOI:10.18653/v1/n18-1101, 被引 325) (2026-06-06); last_checked=2026-06-06; oa_id=W1840435438"
  leaderboard_url: "无单一官方榜; SNLI/MNLI 常作为 NLI 基准出现在 GLUE/XTREME/模型论文中, 使用前到 Papers with Code 或原项目页复核"
  known_issues: "著名 annotation artifacts(仅看假设即可猜标签, Gururangan 2018)、众包标注偏置、SNLI 单一图像描述领域; domain_scope=通用NLP"
  bias_risk: "假设偏置、性别/社会刻板印象出现在众包文本、SNLI 领域窄"
  privacy_risk: "低(SNLI 基于公开 caption, MNLI 公开语料)"
  preprocessing_steps: "句对拼接 / 去除 gold_label='-'(无共识)样本 / 分词截断"
  recommended_splits: "SNLI train/dev/test; MNLI train + matched/mismatched dev/test"
```

```yaml
- dataset_name: "CoNLL-2003 (NER)"
  domain: "NLP"
  task: "命名实体识别(PER/LOC/ORG/MISC 四类)"
  data_type: "英文/德文新闻文本(英文为 Reuters RCV1)"
  size: "英文 ~22.1 万 token(train 14.0k 句 / testa / testb)"
  format: "列式(token POS chunk NER 标签), IOB/BIO"
  license: "标注脚本/任务说明公开研究用; 底层 Reuters RCV1 语料需向 NIST/Reuters 单独申请协议。商用?否(底层语料受限); 再分发?否(底层文本不可分发); 需授权?是(RCV1 协议)。 → 待核查(RCV1 授权)"
  download_url: "https://www.clips.uantwerpen.be/conll2003/ner/"  # 文本需自行获取 RCV1
  paper_url: "https://openalex.org/W2952732525"  # Introduction to the CoNLL-2003 Shared Task (CoNLL 2003), arXiv:cs/0306050
  citation: "Tjong Kim Sang & De Meulder, 2003, CoNLL. OpenAlex 被引 40 (该 arXiv 记录, 实际经典被引远高于此; 2026-06-06); last_checked=待核; oa_id=W2952732525"
  leaderboard_url: "https://paperswithcode.com/sota/named-entity-recognition-ner-on-conll-2003"
  known_issues: "实体类型少(4 类)、新闻领域窄、标注一致性问题、已接近饱和、底层文本获取门槛高; domain_scope=通用NLP"
  bias_risk: "新闻(Reuters 1996-1997)时代/领域偏差、实体分布偏机构地名"
  privacy_risk: "中(新闻含真实人名/机构名)"
  preprocessing_steps: "转 BIO/BIOES 标注 / 句子级切分 / 子词对齐(标签对齐到首子词)"
  recommended_splits: "官方 train/testa(dev)/testb(test)"
```

```yaml
- dataset_name: "WMT (Workshop/Conference on Machine Translation, 如 WMT14/16/19)"
  domain: "NLP"
  task: "机器翻译(多语言对, 如 En-De / En-Fr)"
  data_type: "平行/单语语料(新闻评论、Europarl、Common Crawl、ParaCrawl 等)"
  size: "因年份/语言对而异(WMT14 En-De ~450 万句对常用设置)"
  format: "纯文本(对齐句对) / SGM"
  license: "聚合多来源, 逐子语料许可不一(Europarl 公开、News Commentary CC、Common Crawl 受其 ToU、部分子集限研究用)。商用?各子集不一; 再分发?受限; 需授权?部分需。 → 待核查(逐子语料许可)"
  download_url: "https://www.statmt.org/wmt14/translation-task.html"  # 各年份对应 wmtXX 页面
  paper_url: "https://openalex.org/W2257408573"  # Findings of the 2014 Workshop on Statistical Machine Translation (WMT 2014), DOI:10.3115/v1/w14-3302
  citation: "Bojar et al., 2014, WMT(ACL Workshop). OpenAlex 被引 537 (2026-06-06); last_checked=2026-06-06; oa_id=W2257408573"
  leaderboard_url: "https://paperswithcode.com/sota/machine-translation-on-wmt2014-english-german"
  known_issues: "不同论文使用的训练集/预处理/BPE 不一致导致 BLEU 不可直接比较、测试集年份各异、子语料质量参差、需统一 tokenization 与 detok 才公平; domain_scope=通用NLP"
  bias_risk: "新闻/议会领域偏差、高资源语言对偏好、爬取语料噪声与对齐错误"
  privacy_risk: "中(新闻/网页含真实人名与个人信息)"
  preprocessing_steps: "tokenization(Moses) / 联合 BPE 或 SentencePiece / 长度过滤与对齐清洗 / sacreBLEU 标准评测"
  recommended_splits: "按年份: 训练(混合语料) / dev(如 newstest 前一年) / test(对应年份 newstest)"
```

---

## 维护说明

- 本卡片为 db04 的 CV/NLP 扩展集, 与 [dataset_cards.md](dataset_cards.md) 种子卡互补(ImageNet/MNIST/GLUE 此处给出更完整版本)。
- 被引(citation)数据均来自 OpenAlex `cited_by_count` 实时 curl 快照(2026-06-06), 仅作量级参考, 随时间增长。
- 标「待核查」字段使用前务必到官方页确认许可, 商用/再分发前联动 a10 合规检查。
- 高隐私风险数据(CelebA / Common Crawl-C4 / Cityscapes)用于含人物/PII 场景时, 须评估肖像权与数据保护合规(GDPR/个保法)。
```

