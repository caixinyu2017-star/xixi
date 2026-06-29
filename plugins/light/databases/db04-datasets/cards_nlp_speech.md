# db04 数据集卡 — NLP / 语音 / 多语言评测

> schema: `dataset_name, domain, task, data_type, size, format, license, download_url, paper_url, citation, leaderboard_url, known_issues, bias_risk, privacy_risk, preprocessing_steps, recommended_splits`
> 可核查字段来自 OpenAlex 真实查询（2026-06-10）。本文件补充 NLP/语音专题卡，部分通用数据集可能与 `cards_cv_nlp.md` 或 `cards_frontier.md` 有轻微重叠。

```yaml
- dataset_name: MMLU (Massive Multitask Language Understanding)
  domain: NLP / 大模型评测 / 知识与推理
  task: 多学科多选题评测、few-shot/zero-shot LLM 能力测试
  data_type: 英文多选题，57 个学科，从高中到专业考试
  size: 约 15,908 道题（dev/validation/test/auxiliary_train）
  format: CSV/JSON（社区镜像多见）
  license: 原始仓库/数据使用条款需核实；题目来源含考试/教材，商用与再分发需谨慎
  download_url: https://github.com/hendrycks/test ; Hugging Face datasets/mmlu
  paper_url: https://doi.org/10.48550/arxiv.2009.03300
  citation: "Measuring Massive Multitask Language Understanding | 2020 | cited:278 | doi:10.48550/arxiv.2009.03300; last_checked=待核; doi=10.48550/arxiv.2009.03300"
  leaderboard_url: HELM / Open LLM Leaderboard / Papers with Code（不同实现不完全一致）
  known_issues: 数据污染风险高；题目版权/来源复杂；只评英文选择题，不能代表真实科研能力; domain_scope=通用NLP
  bias_risk: 中 — 学科/语言/文化偏英语教育体系
  privacy_risk: 低
  preprocessing_steps: 固定 prompt 模板；严格区分 dev/val/test；报告 few-shot 数与答案解析是否使用；检查训练污染
  recommended_splits: 官方 dev/validation/test；禁止用 test 调 prompt

- dataset_name: XTREME / XTREME-R
  domain: NLP / 多语言理解
  task: 跨语言迁移、句子分类、序列标注、问答、检索等多任务评测
  data_type: 多语言文本 benchmark 集合
  size: 40+ 语言、多任务（具体随 XTREME/XTREME-R 版本）
  format: Hugging Face datasets / TSV/JSON
  license: 各子数据集 license 不一；使用前逐项核查
  download_url: https://github.com/google-research/xtreme ; Hugging Face xtreme
  paper_url: https://doi.org/10.48550/arxiv.2003.11080
  citation: "XTREME: A Massively Multilingual Multi-task Benchmark for Evaluating Cross-lingual Generalization | 2020 | cited:301 | doi:10.48550/arxiv.2003.11080; last_checked=待核; doi=10.48550/arxiv.2003.11080"
  leaderboard_url: XTREME official / Papers with Code
  known_issues: 子任务 license/质量差异；训练语言与测试语言不平衡；多语言 tokenization 影响大; domain_scope=通用NLP
  bias_risk: 中高 — 高资源语言表现不代表低资源语言，文化/标注偏差明显
  privacy_risk: 低到中（取决于子数据集）
  preprocessing_steps: 明确子任务；统一 tokenizer；报告 zero-shot/translate-train/translate-test 设置；逐子数据集核 license
  recommended_splits: 官方 split；按语言分组报告，而非只报平均

- dataset_name: LibriSpeech
  domain: 语音识别 / 英语朗读语音
  task: ASR、语音自监督预训练、说话人/噪声鲁棒评测
  data_type: 16kHz 英语有声书语音 + 转写文本
  size: 约 1000 小时（train-clean-100/360、train-other-500 等）
  format: FLAC + TXT transcriptions
  license: CC BY 4.0（基于 LibriVox 公共有声书；使用前核对具体发布条款）
  download_url: https://www.openslr.org/12
  paper_url: https://doi.org/10.1109/icassp.2015.7178964
  citation: "Librispeech: An ASR corpus based on public domain audio books | 2015 | cited:5976 | doi:10.1109/icassp.2015.7178964; last_checked=待核; doi=10.1109/icassp.2015.7178964"
  leaderboard_url: Papers with Code LibriSpeech ASR
  known_issues: 朗读体、干净语音偏多，不代表真实会议/电话/噪声场景；训练/测试说话人需保持不重叠; domain_scope=语音
  bias_risk: 中 — 英语朗读、有声书人群与文本体裁偏差
  privacy_risk: 低 — 公共有声书语音
  preprocessing_steps: 使用官方 split；统一采样率；规范化文本；记录是否使用 LM/外部数据
  recommended_splits: 官方 train/dev/test clean/other splits

- dataset_name: Common Voice
  domain: 多语言语音 / 众包语音
  task: 多语言 ASR、低资源语音、自监督预训练、口音鲁棒性
  data_type: 众包朗读语音 + 文本 + 元数据（年龄/性别/口音可选）
  size: 多语言、数万小时量级（版本持续更新）
  format: MP3/TSV；Hugging Face datasets
  license: CC0（Common Voice 数据通常为 public domain dedication；仍需核对版本）
  download_url: https://commonvoice.mozilla.org/
  paper_url: https://doi.org/10.48550/arxiv.1912.06670
  citation: "Common Voice: A Massively-Multilingual Speech Corpus | 2019 | cited:209 | doi:10.48550/arxiv.1912.06670; last_checked=待核; doi=10.48550/arxiv.1912.06670"
  leaderboard_url: 无统一官方榜；常见于 Hugging Face/ASR benchmark
  known_issues: 众包质量差异；各语言样本量极不均衡；文本提示与真实口语差异大；元数据自报不完整; domain_scope=语音
  bias_risk: 高 — 语言/地区/性别/口音覆盖不均
  privacy_risk: 中 — 公开人声音频，虽授权开放但仍有声纹隐私风险
  preprocessing_steps: 固定版本与语言；质量过滤；说话人去重；按 speaker split；文本规范化
  recommended_splits: 官方 train/dev/test；低资源实验按语言单独报告

- dataset_name: VoxCeleb
  domain: 说话人识别 / 语音表征
  task: speaker identification / verification、说话人嵌入、跨域鲁棒性
  data_type: YouTube 采访/视频中截取的人声片段 + speaker ID
  size: VoxCeleb1/2 合计百万级 utterances、数千说话人
  format: WAV/音频片段 + metadata
  license: 研究用途；原始音视频来源 YouTube，商用/再分发与肖像/声音权需谨慎核实
  download_url: https://www.robots.ox.ac.uk/~vgg/data/voxceleb/
  paper_url: https://doi.org/10.21437/interspeech.2017-950
  citation: "VoxCeleb: A Large-Scale Speaker Identification Dataset | 2017 | cited:2126 | doi:10.21437/interspeech.2017-950; last_checked=待核; doi=10.21437/interspeech.2017-950"
  leaderboard_url: Papers with Code speaker verification on VoxCeleb
  known_issues: 背景噪声/视频抽取错误；名人/公开视频偏差；声纹属于敏感生物特征; domain_scope=语音
  bias_risk: 高 — 名人/语言/性别/地区分布不均
  privacy_risk: 高 — 声纹可识别个人，研究使用需合规，不建议任意再分发派生可识别音频
  preprocessing_steps: 使用官方 verification pairs；VAD/裁剪；说话人级 split；记录增强与外部数据
  recommended_splits: 官方 VoxCeleb1-O/E/H 和 VoxCeleb2 train/test 设置

- dataset_name: FLEURS
  domain: 多语言语音识别 / 语音翻译 / 语言识别
  task: 102 语言 ASR、speech translation、language identification、few-shot 语音评测
  data_type: 多语言朗读语音 + 转写/翻译文本
  size: 约 12 小时/语言量级，102 语言（具体按发布版本）
  format: 音频 + TSV/JSON；TensorFlow Datasets/Hugging Face 可加载
  license: CC BY 4.0（需核对具体版本与文本来源）
  download_url: https://github.com/google-research/google-research/tree/master/fleurs
  paper_url: https://doi.org/10.1109/slt54892.2023.10023141
  citation: "FLEURS: FEW-Shot Learning Evaluation of Universal Representations of Speech | 2023 | cited:167 | doi:10.1109/slt54892.2023.10023141; last_checked=待核; doi=10.1109/slt54892.2023.10023141"
  leaderboard_url: 无统一官方榜；常用于 Whisper/USM 多语评测
  known_issues: 朗读体；每语种规模小；不同语言录音质量与文本难度不一; domain_scope=语音
  bias_risk: 中高 — 语言资源与说话人覆盖仍不均
  privacy_risk: 中 — 公开语音，需按许可使用
  preprocessing_steps: 固定语言列表；按官方 split；统一文本规范化；按语言分别报告 WER/CER
  recommended_splits: 官方 train/dev/test；多语平均需同时报 macro 与 per-language

- dataset_name: VoxPopuli / AISHELL-1
  domain: 多语言/中文语音识别
  task: 多语言 ASR、中文普通话 ASR、半监督/自监督语音学习
  data_type: VoxPopuli 为欧洲议会多语言语音；AISHELL-1 为中文普通话朗读语音
  size: VoxPopuli 数万小时量级；AISHELL-1 约 178 小时中文语音
  format: 音频 + 转写文本
  license: VoxPopuli 研究使用（源自欧洲议会公开资料，需核对许可）；AISHELL-1 通常为研究许可，商用需核实
  download_url: https://github.com/facebookresearch/voxpopuli ; https://www.openslr.org/33/
  paper_url: https://doi.org/10.18653/v1/2021.acl-long.80 ; https://doi.org/10.1109/icsda.2017.8384449
  citation: |
    VoxPopuli: A Large-Scale Multilingual Speech Corpus for Representation Learning, Semi-Supervised Learning and Interpretation | 2021 | cited:318 | doi:10.18653/v1/2021.acl-long.80
    AISHELL-1: An open-source Mandarin speech corpus and a speech recognition baseline | 2017 | cited:792 | doi:10.1109/icsda.2017.8384449
    [last_checked=待核; 锚点已内联 doi:/cited:,被引实时查见 dataset_signal.py]
  leaderboard_url: Papers with Code / ESPnet recipes（非统一官方榜）
  known_issues: VoxPopuli 是议会演讲域；AISHELL-1 为朗读普通话，真实电话/会议/方言泛化有限; domain_scope=语音
  bias_risk: 中 — 场景、语言、说话人分布偏差
  privacy_risk: 中 — 公开语音数据仍涉及声纹隐私与许可约束
  preprocessing_steps: 官方 split；采样率统一；文本规范化；说话人不重叠；按语言/中文方言场景单独评估
  recommended_splits: 官方 split；跨域测试建议用 Common Voice/真实会议数据作外部验证
```
