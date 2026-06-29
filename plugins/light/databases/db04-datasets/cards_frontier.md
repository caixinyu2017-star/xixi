# db04 — 前沿数据集卡：大模型 / 多模态 / 科学 / 领域（_new_frontier）

> 20 张 dataset_card，schema 见 db04 README：dataset_name, domain, task, data_type, size, format, license, download_url, paper_url, citation, leaderboard_url, known_issues, bias_risk, privacy_risk, preprocessing_steps, recommended_splits。
> **可核查字段来源**：paper_url / DOI / 被引数来自 OpenAlex 实时 curl（2026-06-06 快照，被引随时间增长）；license / 官方下载页经 WebSearch 定位后标注，不确定者写「待核查」。
> **license 必填**，并明确：商用？再分发？隐私？需授权？— 隐私授权风险务必写明（联动 a10）。
> ⚠ 免费源不可得（付费墙）的 JCR IF / Scimago SJR 一律不写；数据集本身无 IF 概念，此处不涉及。

---

## 一、大模型预训练语料（LLM Pretraining Corpora）

```yaml
- dataset_name: "LAION-5B"
  domain: "多模态 / 视觉-语言预训练"
  task: "图文对比预训练 (CLIP/扩散模型训练语料)"
  data_type: "图像-文本对 (URL + caption + CLIP 相似度等元数据)"
  size: "~5.85B 图文对 (laion2B-en + laion2B-multi + laion1B-nolang)"
  format: "Parquet 元数据 (URL/alt-text/相似度/水印/NSFW 分数); 不含图像本体, 需自行按 URL 下载"
  license: "元数据 CC-BY 4.0(可商用/再分发); 图像本体为原始网页版权, LAION 仅分发 URL 索引。⚠ 商用?元数据可/图像受原始版权; 再分发?元数据可/图像否; 需授权?图像受逐链接版权约束。⚠ 原始 LAION-5B 因被指含 CSAM 于 2023-12 下架, 2024 以 Re-LAION-5B(已移除疑似非法链接)重新发布 → 应使用 Re-LAION-5B, 旧版勿用"
  download_url: "https://laion.ai/blog/laion-5b/ (现行: https://laion.ai/blog/relaion-5b/)"
  paper_url: "https://openalex.org/W4306820534"  # LAION-5B: An open large-scale dataset... (NeurIPS 2022 D&B), DOI:10.48550/arXiv.2210.08402
  citation: "Schuhmann et al., 2022, NeurIPS Datasets & Benchmarks. OpenAlex 被引 1,036 (2026-06-06); last_checked=2026-06-06; oa_id=W4306820534"
  leaderboard_url: "无官方榜(作训练语料, 下游评测见 CLIP/扩散模型 benchmark)"
  known_issues: "大量链接失效(link rot)、alt-text 噪声大、CLIP 过滤引入偏差、NSFW 标注不完美、含重复; domain_scope=多模态CV"
  bias_risk: "网络爬取强烈英语/西方中心偏差、刻板印象、版权与有害内容"
  privacy_risk: "⚠ 高 — 含可识别人物、私人照片、医疗影像泄露案例; 原版曾含 CSAM 链接已下架; 涉肖像权/GDPR 争议"
  preprocessing_steps: "按 URL 下载图像 / CLIP 相似度阈值过滤(常用 >0.28) / 去重 / NSFW 与水印过滤"
  recommended_splits: "无标准 train/test(全量预训练); 评测用下游零样本任务"
```

```yaml
- dataset_name: "Common Crawl"
  domain: "大模型预训练 / NLP"
  task: "大规模网页语料 (LLM 预训练原料、信息抽取)"
  data_type: "网页爬取原始数据 (HTML/纯文本/元数据)"
  size: "每月新增数 PB; 历史累计数百亿网页, 单月常 ~3-4B 页"
  format: "WARC(原始响应) / WET(纯文本) / WAT(元数据), 存于 AWS S3"
  license: "数据按 Common Crawl Terms of Use 提供, 底层网页版权归各原网站(CC 不持版权)。⚠ 商用?ToU 允许使用但底层内容版权/隐私需自行合规; 再分发?派生语料常见但须遵守 ToU 与原始版权; 需授权?否(公开 S3) → 待核查(底层网页版权/PII/被爬站点合规)"
  download_url: "https://commoncrawl.org/get-started"
  paper_url: "无专属数据集论文(基础设施项目); 常通过下游语料(C4/RedPajama 等)引用 → 待核查"
  citation: "Common Crawl Foundation. 无标准学术引用, 通常引用官网或派生语料论文; last_checked=待核; src=community"
  leaderboard_url: "无(原料语料, 无榜)"
  known_issues: "含大量重复/低质/样板/spam, 编码错误, 语言混杂; 需重度清洗去重才可用; domain_scope=通用NLP"
  bias_risk: "高 — 网页分布偏英语/西方/高流量站点; 放大社会偏见与有害内容"
  privacy_risk: "⚠ 高 — 大量未脱敏 PII、版权全文、个人主页等; 未经同意爬取, 涉 GDPR/个保法"
  preprocessing_steps: "WET 提取 / 语言识别 / MinHash 或 SimHash 去重 / 质量与毒性过滤 / PII 清洗"
  recommended_splits: "无标准 split(预训练全量); 按月度 crawl 或派生子集划分"
```

```yaml
- dataset_name: "The Pile"
  domain: "大模型预训练 / NLP"
  task: "多样化英文文本 LLM 预训练语料"
  data_type: "22 个子数据集混合文本(学术/代码/对话/书籍/网页等)"
  size: "~825 GiB(未压缩); 含 Pile-CC, PubMed, arXiv, GitHub, Books3, OpenWebText2 等 22 源"
  format: "JSONL(zstd 压缩), 每条含 text 与 meta(子集来源)"
  license: "⚠ 整体无统一开放许可; 各子集许可不一。Books3 子集含盗版图书, 因版权诉讼/丹麦反盗版通知已移除, 官方原始打包不再可下载。商用?否(含受版权与受限子集); 再分发?受限(Books3 等已撤); 需授权?部分子集需 → 应使用移除侵权子集的版本, 勿用含 Books3 的旧包"
  download_url: "https://pile.eleuther.ai/ (原打包已失效, 见 https://huggingface.co/datasets/EleutherAI/pile 说明)"
  paper_url: "https://openalex.org/W3118781290"  # The Pile: An 800GB Dataset of Diverse Text for Language Modeling, arXiv:2101.00027 (DOI:10.48550/arxiv.2101.00027)
  citation: "Gao et al., 2020. OpenAlex 被引 485 (2026-06-06); last_checked=2026-06-06; oa_id=W3118781290"
  leaderboard_url: "无(预训练语料)"
  known_issues: "子集去重不彻底、含基准泄漏风险、Books3 等子集已因版权下架、质量参差; domain_scope=通用NLP"
  bias_risk: "偏学术/技术/英语文本; 含网络爬取偏见与刻板印象"
  privacy_risk: "⚠ 高 — 含书籍全文/邮件/代码等可能含 PII 与受版权内容"
  preprocessing_steps: "按子集权重采样 / 去重 / 过滤受限子集 / 分词"
  recommended_splits: "官方提供 train/val/test 划分"
```

```yaml
- dataset_name: "RedPajama (RedPajama-Data v1 / v2)"
  domain: "大模型预训练 / NLP"
  task: "开源复现 LLaMA 训练语料 (LLM 预训练)"
  data_type: "多源混合文本 (CommonCrawl/C4/GitHub/Wikipedia/Books/arXiv/StackExchange)"
  size: "v1 ~1.2T tokens (复现 LLaMA 配比); v2 ~30T tokens (含质量信号注释), 5 语言"
  format: "JSONL; v2 附带质量打分信号(quality signals)便于过滤"
  license: "各子集沿用原始许可(Apache-2.0 代码/CC 等), 整体为各来源许可的集合; Together 以开放方式发布。⚠ 商用?需逐子集核实(底层 CommonCrawl/Books 等受原始版权); 再分发?多数子集允许但须遵守原许可; 需授权?部分子集需 → 待核查(逐子集许可与底层版权)"
  download_url: "https://huggingface.co/datasets/togethercomputer/RedPajama-Data-1T (v2: RedPajama-Data-V2)"
  paper_url: "https://openalex.org/W4404573785"  # RedPajama: an Open Dataset for Training Large Language Models, arXiv:2411.12372 (DOI:10.48550/arxiv.2411.12372)
  citation: "Weber et al., 2024, NeurIPS D&B. OpenAlex 被引 18 (2026-06-06); last_checked=2026-06-06; oa_id=W4404573785"
  leaderboard_url: "无(预训练语料)"
  known_issues: "沿袭 CommonCrawl 噪声、去重与质量过滤依赖使用者、v2 体量巨大存储/IO 压力大; domain_scope=通用NLP"
  bias_risk: "高 — 继承网页/代码语料的英语与西方偏差、社会偏见"
  privacy_risk: "⚠ 高 — 含网页/代码可能携带 PII 与受版权内容"
  preprocessing_steps: "按质量信号阈值过滤 / 去重 / 子集配比采样 / 分词"
  recommended_splits: "无标准 split(全量预训练)"
```

```yaml
- dataset_name: "C4 (Colossal Clean Crawled Corpus)"
  domain: "大模型预训练 / NLP"
  task: "清洗后网页语料 (T5/LLM 预训练)"
  data_type: "经启发式清洗的英文网页文本(另有 multilingual mC4)"
  size: "en 子集 ~750 GB / ~3.65 亿文档; mC4 覆盖 100+ 语言"
  format: "TFDS / JSON(Hugging Face allenai/c4)"
  license: "C4 派生数据标注 ODC-BY 1.0(开放数据署名, 可商用+再分发须署名); 底层基于 Common Crawl, 须同时遵守 CC ToU。⚠ 商用?ODC-BY 允许需署名; 再分发?允许; 需授权?否 → 底层网页版权/PII 仍待核查"
  download_url: "https://huggingface.co/datasets/allenai/c4"
  paper_url: "https://openalex.org/W2981852735"  # Exploring the Limits of Transfer Learning (T5/C4), arXiv:1910.10683, JMLR 2020
  citation: "Raffel et al., 2020, JMLR. OpenAlex 被引 3,692 (2026-06-06); last_checked=2026-06-06; oa_id=W2981852735"
  leaderboard_url: "无(预训练语料)"
  known_issues: "启发式过滤误伤(Dodge 2021 指出过滤少数群体方言/特定网站)、含基准泄漏、去重不彻底; domain_scope=通用NLP"
  bias_risk: "高 — 过滤规则引入偏差、英语/西方中心、放大刻板印象"
  privacy_risk: "⚠ 高 — 含可能未脱敏 PII 与版权内容(源自爬取)"
  preprocessing_steps: "语言识别 / 去重 / badwords 与样板过滤 / 句末标点启发式清洗"
  recommended_splits: "官方提供 train/validation"
```

---

## 二、多模态：图文 / 视频 / 音频 (Multimodal)

```yaml
- dataset_name: "LAION-COCO"
  domain: "多模态 / 图文生成"
  task: "合成式 caption 图文对 (生成模型/captioning 预训练)"
  data_type: "图像 URL + 机器生成的 COCO 风格 caption"
  size: "~600M 图文对 (取自 LAION-2B-en, 用 BLIP/CLIP 生成并排序 caption)"
  format: "Parquet 元数据(URL + 合成 caption + 模型分数); 不含图像本体"
  license: "元数据沿 LAION 以 CC-BY 4.0 发布(可商用/再分发); 图像本体为原网页版权。⚠ 商用?元数据可/图像受原始版权; 再分发?元数据可/图像否; 需授权?图像受逐链接版权约束。⚠ 关联 LAION-5B 安全事件, 应使用经清理的现行版本"
  download_url: "https://laion.ai/blog/laion-coco/"
  paper_url: "无专属同行评审论文(LAION 博客发布的派生数据集); 方法关联 BLIP/CLIP → 待核查"
  citation: "LAION e.V., 2022 (博客技术发布). 无标准学术引用 → 待核查; last_checked=待核; src=community"
  leaderboard_url: "无(训练语料)"
  known_issues: "caption 为机器生成含幻觉/泛化模板、link rot、继承 LAION 噪声与过滤偏差; domain_scope=多模态CV"
  bias_risk: "高 — 继承 LAION-2B 英语/西方偏差; 合成 caption 放大字幕模型自身偏见"
  privacy_risk: "⚠ 高 — 图像源自网络爬取, 含可识别人物; 关联 LAION 安全/CSAM 历史问题"
  preprocessing_steps: "按 URL 下载图像 / 选取 top caption / 相似度过滤 / 去重"
  recommended_splits: "无标准 split(预训练全量)"
```

```yaml
- dataset_name: "WebVid (WebVid-2M / WebVid-10M)"
  domain: "多模态 / 视频-语言"
  task: "视频-文本检索 / 视频 caption / 文生视频预训练"
  data_type: "短视频 + alt-text 描述 (网络爬取的带字幕素材视频)"
  size: "WebVid-2M ~250 万视频-文本对; WebVid-10M ~1040 万对"
  format: "视频 URL + 文本描述(CSV 元数据); 视频本体需按 URL 获取"
  license: "⚠ 视频来自素材库(Shutterstock 等), 含水印, 仅供研究用途; 非商业, 不可再分发原视频。⚠ 因来源版权该数据集后被官方下架(takedown)。商用?否; 再分发?否; 需授权?是(受素材库版权约束) → 现行多用替代集(如 Panda-70M), 旧链接已失效"
  download_url: "https://github.com/m-bain/webvid (原下载已受限/下架)"
  paper_url: "https://openalex.org/W3204588463"  # Frozen in Time: A Joint Video and Image Encoder for End-to-End Retrieval (ICCV 2021)
  citation: "Bain et al., 2021, ICCV. OpenAlex 被引 749 (2026-06-06); last_checked=2026-06-06; oa_id=W3204588463"
  leaderboard_url: "https://paperswithcode.com/sota/video-retrieval-on-msr-vtt"
  known_issues: "视频含 Shutterstock 水印影响下游、alt-text 与视频弱对齐、来源版权致下架、link rot; domain_scope=多模态CV"
  bias_risk: "素材视频偏商业/广告题材、英语描述、场景分布偏差"
  privacy_risk: "中-高 — 含可识别人物的素材视频; 受版权与肖像约束"
  preprocessing_steps: "抽帧 / 文本清洗 / 去水印或裁剪 / 时序采样"
  recommended_splits: "训练用 WebVid-2M/10M; 评测常迁移到 MSR-VTT/DiDeMo"
```

```yaml
- dataset_name: "AudioCaps"
  domain: "多模态 / 音频-语言"
  task: "音频字幕生成 (audio captioning) / 文本-音频检索 / 文生音频"
  data_type: "音频片段(取自 AudioSet, 10s YouTube 片段) + 人工众包英文描述"
  size: "~46k 训练 / ~0.5k 验证 / ~1k 测试 音频-描述对(每测试样本多参考)"
  format: "caption CSV(含 YouTube id + 时间戳 + 文本); 音频需按 AudioSet/YouTube 获取"
  license: "⚠ 标注(caption)以 MIT 许可发布; 音频本体源自 AudioSet/YouTube, 受 YouTube 条款与原视频版权约束。商用?标注 MIT 可/音频受 YouTube 条款; 再分发?标注可/音频否; 需授权?音频受原平台约束 → 待核查(音频版权与可用性, link rot)"
  download_url: "https://audiocaps.github.io/"  # https://github.com/cdjkim/audiocaps
  paper_url: "https://openalex.org/W2945761034"  # AudioCaps: Generating Captions for Audios in The Wild (NAACL 2019, DOI:10.18653/v1/n19-1011)
  citation: "Kim et al., 2019, NAACL-HLT. OpenAlex 被引 82 (2026-06-06; 经典工作实际被引更高); last_checked=待核; oa_id=W2945761034"
  leaderboard_url: "https://paperswithcode.com/sota/audio-captioning-on-audiocaps"
  known_issues: "依赖 YouTube 源音频(link rot 致部分不可得)、众包描述主观/多样、与 AudioSet 标签弱一致; domain_scope=多模态CV"
  bias_risk: "继承 AudioSet 的 YouTube 内容分布偏差、英语描述、声音类别长尾"
  privacy_risk: "中 — 音频可能含可识别人声/环境信息; 受 YouTube 平台条款"
  preprocessing_steps: "按 YouTube id 下载并切 10s / 重采样(常 16/32 kHz) / log-mel 特征 / 文本规范化"
  recommended_splits: "官方 train/val/test"
```

```yaml
- dataset_name: "MSR-VTT (Microsoft Research Video to Text)"
  domain: "多模态 / 视频-语言"
  task: "视频 caption / 视频-文本检索 / 视频问答"
  data_type: "网络视频片段 + 人工英文描述"
  size: "10,000 视频片段(20 类), 每片段 20 条描述, 共 ~20 万句描述"
  format: "视频文件 + JSON 标注(句子/类别)"
  license: "⚠ 微软研究发布, 仅供学术/非商业研究; 视频源自网络(YouTube 等), 受原始版权。商用?否; 再分发?受限; 需授权?是(研究用途同意) → 待核查(底层视频版权)"
  download_url: "https://www.microsoft.com/en-us/research/publication/msr-vtt-a-large-video-description-dataset-for-bridging-video-and-language/ (镜像见各复现仓库)"
  paper_url: "https://openalex.org/W2425121537"  # MSR-VTT: A Large Video Description Dataset for Bridging Video and Language (CVPR 2016, DOI:10.1109/cvpr.2016.571)
  citation: "Xu et al., 2016, CVPR. OpenAlex 被引 1,737 (2026-06-06); last_checked=2026-06-06; oa_id=W2425121537"
  leaderboard_url: "https://paperswithcode.com/sota/video-retrieval-on-msr-vtt"
  known_issues: "不同论文用不同 train/test split(1k-A/1k-B 等)致结果不可直接比较、描述重复度高、规模偏小、link rot; domain_scope=多模态CV"
  bias_risk: "YouTube 内容/类别分布偏差、英语描述"
  privacy_risk: "中 — 含可识别人物的网络视频"
  preprocessing_steps: "抽帧/特征(如 CLIP/S3D) / 文本分词 / 统一 split 设置"
  recommended_splits: "官方 6513/497/2990; 检索常用 1k-A 测试 split(注明设置)"
```

---

## 三、3D / 自动驾驶 (3D & Autonomous Driving)

```yaml
- dataset_name: "ScanNet (v2)"
  domain: "3D 计算机视觉 / 室内场景理解"
  task: "3D 语义/实例分割 / 3D 物体检测 / 重建 / 视图合成"
  data_type: "RGB-D 视频 + 重建网格 + 相机位姿 + 3D/2D 语义标注"
  size: "1513 个扫描(v2 含 ~2.5M RGB-D 帧), 707 个独立空间; 20 类评测(ScanNet200 扩展 200 类)"
  format: ".sens(RGB-D 流) + .ply 网格 + 标注(JSON/聚合)"
  license: "⚠ 自定义 ScanNet Terms of Use, 仅限非商业学术研究; 需签署协议并提交申请。商用?否; 再分发?否; 需授权?是(填表签约获取下载脚本)"
  download_url: "http://www.scan-net.org/ (需提交 ToU 申请获取 download script)"
  paper_url: "https://openalex.org/W2594519801"  # ScanNet: Richly-Annotated 3D Reconstructions of Indoor Scenes (CVPR 2017, DOI:10.1109/cvpr.2017.261)
  citation: "Dai et al., 2017, CVPR. OpenAlex 被引 3,990 (2026-06-06); last_checked=2026-06-06; oa_id=W2594519801"
  leaderboard_url: "http://kaldir.vc.in.tum.de/scannet_benchmark/"
  known_issues: "重建网格有噪声/空洞、标注粒度不一、长尾类、消费级深度传感器误差; domain_scope=通用CV"
  bias_risk: "室内场景(住宅/办公为主)偏差、地域偏差、家具类别长尾"
  privacy_risk: "中-高 — 扫描私人住宅/办公空间, 可能含可识别个人物品与人物"
  preprocessing_steps: "体素化或点采样 / 帧采样 / 标签映射到 20 或 200 类 / 坐标对齐"
  recommended_splits: "官方 train/val/test(test 标注隐藏, 需提交)"
```

```yaml
- dataset_name: "KITTI"
  domain: "自动驾驶 / 3D 视觉"
  task: "立体/光流 / 视觉里程计 / 2D-3D 目标检测 / 跟踪 / 道路分割"
  data_type: "车载相机(立体)+ Velodyne 64 线激光雷达 + GPS/IMU"
  size: "原始 ~6 小时驾驶; 检测基准 7481 训练 / 7518 测试帧, 3 主类(Car/Pedestrian/Cyclist)"
  format: "PNG 图像 + .bin 点云 + 标定/标注 txt"
  license: "CC BY-NC-SA 3.0(署名-非商业-相同方式共享)。商用?否(NC); 再分发?可(须 BY-NC-SA 同条款); 需授权?否(公开下载)"
  download_url: "https://www.cvlibs.net/datasets/kitti/"
  paper_url: "https://openalex.org/W2150066425"  # Are we ready for autonomous driving? The KITTI vision benchmark suite (CVPR 2012, DOI:10.1109/cvpr.2012.6248074)
  citation: "Geiger et al., 2012, CVPR. OpenAlex 被引 14,348 (2026-06-06); last_checked=2026-06-06; oa_id=W2150066425"
  leaderboard_url: "https://www.cvlibs.net/datasets/kitti/eval_object.php"
  known_issues: "仅德国卡尔斯鲁厄单城晴天白天、规模小、3D 框仅前视相机视野内标注、已较饱和; domain_scope=自动驾驶-特定地域"
  bias_risk: "地域(德国)/天气(晴天)/时间(白天)严重偏差, 泛化受限"
  privacy_risk: "中 — 街景含行人/车牌等可识别信息"
  preprocessing_steps: "点云裁剪到相机视野 / 体素化或 BEV 投影 / 图像-点云标定对齐 / 难度分级(easy/mod/hard)"
  recommended_splits: "官方 train/test; 检测常用 Chen 等的 train/val 3712/3769 拆分(注明)"
```

```yaml
- dataset_name: "nuScenes"
  domain: "自动驾驶 / 多模态 3D"
  task: "3D 目标检测 / 跟踪 / 预测 / BEV 分割 / 全景分割(nuScenes-lidarseg)"
  data_type: "6 相机环视 + 1 旋转激光雷达 + 5 毫米波雷达 + GPS/IMU, 同步标定"
  size: "1000 个 20s 场景(波士顿/新加坡), ~140 万相机图 / 39 万激光帧, 23 类, 140 万 3D 框"
  format: "图像/点云 + JSON 标注(nuScenes devkit schema)"
  license: "⚠ 非商业, 自定义 nuScenes Terms of Use(类 CC BY-NC-SA); 商用需联系 Motional 单独商业授权。商用?否(免费版); 再分发?受限(须同条款); 需授权?是(注册同意 ToU) → 商用须单独签约, 待核查具体条款"
  download_url: "https://www.nuscenes.org/nuscenes (需注册账号同意 ToU)"
  paper_url: "https://openalex.org/W2925148167"  # nuScenes: A Multimodal Dataset for Autonomous Driving (CVPR 2020, DOI:10.1109/cvpr42600.2020.01164)
  citation: "Caesar et al., 2020, CVPR. OpenAlex 被引 379 (2026-06-06; arXiv 1903.11027 另有计数); last_checked=待核; oa_id=W2925148167"
  leaderboard_url: "https://www.nuscenes.org/object-detection"
  known_issues: "仅两城、激光线数较低(32 线)、类别长尾、标注频率 2Hz(需插值)、夜雨样本有限; domain_scope=自动驾驶-特定地域"
  bias_risk: "地域(波士顿/新加坡)/交通规则(左右行)偏差、类别长尾"
  privacy_risk: "⚠ 中-高 — 街景含行人/人脸/车牌; 官方已做部分模糊但需复核"
  preprocessing_steps: "多帧点云聚合 / 传感器标定融合 / 关键帧采样(2Hz) / NDS/mAP 评测协议"
  recommended_splits: "官方 train(700)/val(150)/test(150)场景"
```

```yaml
- dataset_name: "Waymo Open Dataset (Perception)"
  domain: "自动驾驶 / 多模态 3D"
  task: "2D/3D 目标检测 / 跟踪 / 运动预测 / 域适应"
  data_type: "5 相机 + 5 激光雷达(中长距)环视, 高频同步标定, 多城市多天气"
  size: "1150 段 20s 场景(Perception v1), ~20 万帧, ~1200 万 3D 框 + 1000 万 2D 框"
  format: "TFRecord(protobuf frame) + 标注"
  license: "⚠ Waymo Dataset License Agreement, 仅限非商业研究; 禁止商用与未授权再分发。商用?否; 再分发?否; 需授权?是(注册同意 license) → 商用须单独联系 Waymo"
  download_url: "https://waymo.com/open/ (需注册同意 license)"
  paper_url: "https://openalex.org/W3035172746"  # Scalability in Perception for Autonomous Driving: Waymo Open Dataset (CVPR 2020, DOI:10.1109/cvpr42600.2020.00252)
  citation: "Sun et al., 2020, CVPR. OpenAlex 被引 2,998 (2026-06-06); last_checked=2026-06-06; oa_id=W3035172746"
  leaderboard_url: "https://waymo.com/open/challenges/"
  known_issues: "体量大(TB 级)处理成本高、仅美国若干城市、标注/坐标系与 KITTI/nuScenes 不一致需转换; domain_scope=自动驾驶-特定地域"
  bias_risk: "地域(美国)偏差、Waymo 传感器配置特定、类别长尾"
  privacy_risk: "⚠ 中-高 — 街景含行人/人脸/车牌; 官方做了脱敏处理但需复核"
  preprocessing_steps: "解析 protobuf / 多激光融合 / 坐标系转换 / 关键帧采样 / 官方 metrics 评测"
  recommended_splits: "官方 train/val/test(test 需提交评测服务器)"
```

---

## 四、科学：图 / 分子 / 量子化学 (Scientific: Graphs & Molecules)

```yaml
- dataset_name: "OGB-LSC (Open Graph Benchmark — Large-Scale Challenge)"
  domain: "图机器学习 / 科学"
  task: "节点分类(MAG240M) / 链接预测(WikiKG90Mv2) / 图回归(PCQM4Mv2 分子 HOMO-LUMO gap)"
  data_type: "超大规模图 — 学术异质图 / 知识图谱 / 分子图(SMILES+量子标签)"
  size: "MAG240M ~2.4 亿节点; WikiKG90Mv2 ~9100 万实体; PCQM4Mv2 ~360 万分子"
  format: "预处理 numpy/图张量 + OGB-LSC Python 加载器"
  license: "各子集许可不一 — PCQM4Mv2 基于 PubChemQC(CC BY 4.0); MAG240M 基于 Microsoft Academic Graph(ODC-BY); WikiKG 基于 Wikidata(CC0)。商用?多数子集允许(需署名/遵守各许可); 再分发?允许(遵守原许可); 需授权?否 → 逐子集核实"
  download_url: "https://ogb.stanford.edu/docs/lsc/"
  paper_url: "https://openalex.org/W3136399186"  # OGB-LSC: A Large-Scale Challenge for Machine Learning on Graphs (NeurIPS 2021 D&B, arXiv:2103.09430)
  citation: "Hu et al., 2021, NeurIPS D&B. OpenAlex 被引 121 (2026-06-06); last_checked=2026-06-06; oa_id=W3136399186"
  leaderboard_url: "https://ogb.stanford.edu/docs/lsc/leaderboards/"
  known_issues: "规模巨大需分布式/采样训练、内存与 IO 瓶颈、标签分布不均、3D 构象仅训练集提供(PCQM4Mv2 测试无 3D); domain_scope=通用"
  bias_risk: "学术/知识图来源偏差、分子化学空间覆盖偏差"
  privacy_risk: "低(学术图含作者名属公开元数据; 分子无个人隐私)"
  preprocessing_steps: "邻居采样(GraphSAGE/NeighborLoader) / 特征标准化 / SMILES→图 / 子图划分"
  recommended_splits: "官方按 scaffold/时间/随机的标准 split(各子集不同), test 需提交"
```

```yaml
- dataset_name: "ZINC (含 ZINC15 / ZINC20 与 ZINC-250k 子集)"
  domain: "药物化学 / 分子机器学习"
  task: "虚拟筛选 / 分子性质预测 / 分子生成(ZINC-250k 常用作生成基准)"
  data_type: "商用可购小分子(2D/3D 结构 + SMILES + 理化性质)"
  size: "ZINC20 ~10 亿+ 化合物(可购); 常用 ZINC-250k(约 25 万)做生成/GNN 基准"
  format: "SMILES / SDF / mol2; 提供按性质过滤的子集下载"
  license: "ZINC 数据库免费供学术与商业研究使用, 官方声明 free to use; 来源供应商目录数据。商用?一般允许(官方称 free to use, 建议引用); 再分发?派生子集常见; 需授权?否(注册可选) → 商用前建议复核当前 ZINC 使用条款"
  download_url: "https://zinc.docking.org/ (ZINC20: https://zinc20.docking.org/)"
  paper_url: "https://openalex.org/W2176516200"  # ZINC — A Free Database of Commercially Available Compounds for Virtual Screening (J. Chem. Inf. Model. 2005, DOI:10.1021/ci049714+)
  citation: "Irwin & Shoichet, 2005, JCIM. OpenAlex 被引 4,064 (2026-06-06; ZINC15/20 另有后续论文); last_checked=待核; oa_id=W2176516200"
  leaderboard_url: "https://paperswithcode.com/sota/molecular-graph-generation-on-zinc"
  known_issues: "化学空间偏类药小分子、3D 构象为计算生成、不同版本与子集规模差异大、可购状态随时间变化; domain_scope=化学-材料"
  bias_risk: "偏类药/可购化学空间, 对天然产物/大分子覆盖不足"
  privacy_risk: "无(分子结构数据, 不含个人信息)"
  preprocessing_steps: "SMILES 规范化(RDKit) / 去盐去立体歧义 / 性质过滤 / 图或指纹编码"
  recommended_splits: "生成任务常用 ZINC-250k 随机划分; 筛选任务按靶点/性质自定义"
```


```yaml
- dataset_name: "MoleculeNet"
  domain: "分子机器学习 / 药物与材料"
  task: "分子性质预测基准(分类: BBBP/Tox21/ToxCast/SIDER/ClinTox/HIV/BACE; 回归: ESOL/FreeSolv/Lipophilicity/QM7/QM8/QM9)"
  data_type: "分子(SMILES) + 物理化学/生物活性/量子标签, 多任务"
  size: "各子集差异大(数百到 ~44 万分子, 如 PCBA); 共 17 个数据集"
  format: "CSV(SMILES + 标签); 集成于 DeepChem"
  license: "⚠ 聚合多来源, 整体随 DeepChem 以 MIT 发布加载器; 各子数据集原始许可不一(多为公开数据库)。商用?加载器 MIT 可/各子集需逐一核实; 再分发?多数允许; 需授权?否 → 逐子集许可待核查"
  download_url: "https://moleculenet.org/ (DeepChem: https://deepchem.io/)"
  paper_url: "https://openalex.org/W2594183968"  # MoleculeNet: A Benchmark for Molecular Machine Learning (Chem. Sci. 2018, DOI:10.1039/c7sc02664a)
  citation: "Wu et al., 2018, Chemical Science. OpenAlex 被引 2,923 (2026-06-06); last_checked=2026-06-06; oa_id=W2594183968"
  leaderboard_url: "https://paperswithcode.com/dataset/moleculenet"
  known_issues: "小数据集方差大、标签噪声与缺失、类别极不均衡(如 Tox21)、scaffold split 与随机 split 结果差异显著; domain_scope=化学-材料"
  bias_risk: "各子集化学/靶点空间偏差、活性数据正负样本失衡"
  privacy_risk: "无(分子数据)"
  preprocessing_steps: "SMILES 规范化(RDKit) / 缺失标签掩码 / 指纹或图编码 / scaffold 划分"
  recommended_splits: "官方推荐 scaffold split(分类/回归各指定); 报告需注明 split 类型"
```

---

## 五、医疗影像与生理信号 (Medical — 隐私/授权高风险)

```yaml
- dataset_name: "PhysioNet (PhysioBank / 含 MIT-BIH, MIMIC 等)"
  domain: "医疗 / 生理信号"
  task: "心电(ECG)/脑电/血流动力学等生理信号分析 / 临床预测(随挑战赛而异)"
  data_type: "多导生理信号(ECG/EEG/ABP 等)波形 + 注释 + 临床元数据"
  size: "平台聚合数百个数据库(如 MIT-BIH Arrhythmia 48 段 30min 双导 ECG); 总量随库而异"
  format: "WFDB(.dat/.hea/.atr 波形+注释); 各库格式略异"
  license: "⚠ 逐数据库不同: 部分 ODC-BY / CC BY, 受限库需通过 PhysioNet Credentialed 访问并签 DUA(尤其含临床数据者, 如 MIMIC)。商用?多数研究用途/部分受限; 再分发?受限库禁止; 需授权?受限库需认证+培训(CITI)+签 DUA → 逐库核实"
  download_url: "https://physionet.org/"
  paper_url: "https://openalex.org/W2162800060"  # PhysioBank, PhysioToolkit, and PhysioNet (Circulation 2000, DOI:10.1161/01.cir.101.23.e215)
  citation: "Goldberger et al., 2000, Circulation. OpenAlex 被引 14,433 (2026-06-06); last_checked=2026-06-06; oa_id=W2162800060"
  leaderboard_url: "https://physionet.org/about/challenge/ (各年 Challenge)"
  known_issues: "各库采样率/导联/标注标准不一、信号含基线漂移与工频/运动伪迹、标注者间差异、类别不均衡; domain_scope=生物医学"
  bias_risk: "单中心/特定人群偏差、设备与采集协议偏差、罕见病样本少"
  privacy_risk: "⚠ 高 — 真实患者生理数据; 受限库属受保护健康信息(PHI), 须 HIPAA/伦理合规与 DUA, 禁止重标识"
  preprocessing_steps: "WFDB 读取 / 滤波去伪迹(带通/陷波) / 重采样 / 分段与标准化 / 类别重采样"
  recommended_splits: "按数据库/挑战赛官方划分(常按患者不重叠), 务必避免患者跨集泄漏"
```

```yaml
- dataset_name: "CheXpert"
  domain: "医疗影像 / 胸片"
  task: "胸部 X 光多标签分类(14 类观察, 含不确定标签)"
  data_type: "正/侧位胸部 X 光片 + 报告抽取的弱标签"
  size: "224,316 张胸片, 65,240 名患者(Stanford Hospital 2002–2017)"
  format: "JPG/DICOM 派生 + CSV 标签(含 -1 不确定标注)"
  license: "⚠ Stanford CheXpert 自定义研究使用协议, 仅限非商业研究; 需在 Stanford AIMI 注册申请并同意条款。商用?否; 再分发?否; 需授权?是(注册+同意 Research Use Agreement)"
  download_url: "https://stanfordmlgroup.github.io/competitions/chexpert/ (Stanford AIMI 注册)"
  paper_url: "https://openalex.org/W2963466845"  # CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison (AAAI 2019, DOI:10.1609/aaai.v33i01.3301590)
  citation: "Irvin et al., 2019, AAAI. OpenAlex 被引 2,538 (2026-06-06); last_checked=2026-06-06; oa_id=W2963466845"
  leaderboard_url: "https://stanfordmlgroup.github.io/competitions/chexpert/"
  known_issues: "标签由 NLP 从报告自动抽取(噪声)、不确定标签(-1)处理策略影响大、类别不均衡、隐藏测试集; domain_scope=生物医学"
  bias_risk: "单中心(Stanford)人群/设备偏差、人口学分布不均、公平性研究关注点"
  privacy_risk: "⚠ 高 — 真实患者医学影像(PHI); 虽经去标识, 仍受研究协议约束, 禁止重标识与商用"
  preprocessing_steps: "去识别核验 / resize/归一化(ImageNet 统计或自适应) / 不确定标签策略(U-Ones/U-Zeros) / 类别加权"
  recommended_splits: "官方 train + 小型专家标注 validation; test 隐藏(竞赛提交)"
```

```yaml
- dataset_name: "ISIC (HAM10000 / ISIC Archive 皮肤镜)"
  domain: "医疗影像 / 皮肤病"
  task: "皮肤镜图像皮损分类 / 黑色素瘤检测 / 病灶分割(ISIC Challenge)"
  data_type: "皮肤镜(dermoscopy)图像 + 诊断标签(部分组织病理确诊)"
  size: "HAM10000 = 10,015 张, 7 类诊断; ISIC Archive 累计数十万张(逐年挑战赛扩充)"
  format: "JPEG + CSV/JSON 元数据(诊断/部位/年龄/性别)"
  license: "HAM10000 经 ISIC 以 CC BY-NC 4.0 发布(署名-非商业); ISIC Archive 多数 CC-BY-NC, 部分逐图许可不同。商用?否(NC 为主); 再分发?可(须 BY-NC 同条款); 需授权?否(公开下载, 但须遵守 NC) → 逐图许可待核查"
  download_url: "https://challenge.isic-archive.com/data/"  # HAM10000: https://doi.org/10.7910/DVN/DBW86T
  paper_url: "https://openalex.org/W2794825826"  # The HAM10000 dataset (Sci. Data 2018, DOI:10.1038/sdata.2018.161)
  citation: "Tschandl et al., 2018, Scientific Data. OpenAlex 被引 3,138 (2026-06-06); last_checked=2026-06-06; oa_id=W2794825826"
  leaderboard_url: "https://challenge.isic-archive.com/leaderboards/"
  known_issues: "类别极不均衡(nv 占多数)、部分标签非组织病理确诊、多源设备/标尺差异、近重复图像、毛发/气泡伪迹; domain_scope=生物医学"
  bias_risk: "⚠ 肤色偏差显著(偏浅肤色, 深肤色样本稀少), 对深肤色泛化与公平性差; 部位/年龄分布偏差"
  privacy_risk: "⚠ 中-高 — 真实患者皮损图像(医疗数据); 已去标识, 仍受 NC 与伦理约束, 部分含可定位身体部位"
  preprocessing_steps: "去识别核验 / 去毛发(DullRazor) / 颜色归一化 / resize / 类别重采样或加权"
  recommended_splits: "各年 ISIC Challenge 官方 train/val/test; HAM10000 常用分层随机划分(注明)"
```

---

## 六、农业 / 领域应用 (Agriculture & Domain)


```yaml
- dataset_name: "DeepWeeds"
  domain: "农业 / 杂草识别"
  task: "多类杂草物种图像分类(田间原位拍摄)"
  data_type: "澳大利亚牧场原位杂草 RGB 图像"
  size: "17,509 张图, 8 类目标杂草 + 1 负类(non-weed), 多地点采集"
  format: "JPEG + CSV 标签"
  license: "CC BY 4.0(可商用/再分发须署名)。商用?是(BY); 再分发?是(须署名); 需授权?否"
  download_url: "https://github.com/AlexOlsen/DeepWeeds (数据见 https://doi.org/10.6084/m9.figshare.7570577)"
  paper_url: "https://openalex.org/W2962953743"  # DeepWeeds: A Multiclass Weed Species Image Dataset for Deep Learning (Sci. Rep. 2019, DOI:10.1038/s41598-018-38343-3)
  citation: "Olsen et al., 2019, Scientific Reports. OpenAlex 被引 487 (2026-06-06); last_checked=2026-06-06; oa_id=W2962953743"
  leaderboard_url: "https://paperswithcode.com/dataset/deepweeds"
  known_issues: "类别不均衡(negative 类占比大)、田间光照/距离/遮挡变化大、仅澳洲特定牧场物种、背景复杂; domain_scope=通用"
  bias_risk: "地域(澳大利亚)与物种偏差, 难迁移到其他地区杂草; 采集地点偏差"
  privacy_risk: "无(田间植物图像)"
  preprocessing_steps: "resize/归一化 / 田间增强(裁剪/亮度/模糊) / 类别加权或重采样"
  recommended_splits: "论文用 5 折交叉验证; 也可分层 train/val/test(注明)"
```

---

## 维护说明

- 本卡片为 db04 前沿扩展集（大模型语料 / 多模态 / 3D 驾驶 / 科学分子 / 医疗 / 农业），共 20 张，与 [cards_cv_nlp.md](cards_cv_nlp.md)、[cards_tabular_other.md](cards_tabular_other.md)、[cards_physical_sciences.md](cards_physical_sciences.md)、[cards_nlp_speech.md](cards_nlp_speech.md) 互补；QM9/LibriSpeech/Common Voice/PlantVillage 已迁移到对应领域 canonical 文件。
- paper_url / DOI / 被引数均来自 OpenAlex `cited_by_count` 实时 curl 快照（2026-06-06），仅作量级参考，随时间增长。无专属同行评审论文者（Common Crawl / LAION-COCO）已标「待核查」，不臆造引用。
- ⚠ **免费源不可得（付费墙）**：Clarivate JCR 精确 IF、Scimago SJR 一律未写；数据集本身无 IF 概念，故不涉及。
- ⚠ **高隐私/授权风险**（务必合规后使用，联动 a10）：
  - LAION-5B / LAION-COCO：原版含 CSAM 已下架，须用 Re-LAION；图像含可识别人物。
  - The Pile：含 Books3 盗版子集（已撤），勿用旧包。
  - Common Crawl / C4 / RedPajama：含未脱敏 PII 与版权内容。
  - WebVid / MSR-VTT / AudioCaps：底层视频/音频受 Shutterstock / YouTube 版权，WebVid 已下架。
  - ScanNet / nuScenes / Waymo / KITTI：街景或私人空间含人脸/车牌；前三者非商业授权，商用须单独签约。
  - PhysioNet（受限库）/ CheXpert / ISIC：真实患者数据（PHI），须 DUA / 伦理审查 / 去标识，禁止重标识与商用（CheXpert 非商业、ISIC 多为 CC BY-NC）。
- 标「待核查」字段（逐子集/逐图/逐链接许可、底层网页版权）使用前务必到官方页核实，商用/再分发前做合规检查。


