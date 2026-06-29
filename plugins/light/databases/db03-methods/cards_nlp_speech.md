# db03 方法卡 — NLP / 语音

> 每张卡注明 maturity（经典|主流|新兴|过时|不推荐），避免提出落后方案。受版权全文不收录，仅元数据与开源链接。
> representative_papers 的标题/年份/被引/DOI 来自 OpenAlex 真实查询（https://api.openalex.org，mailto 礼貌池），查询日期 **2026-06-10**；被引数随时间变动。
> OpenAlex 对部分经典 arXiv/NLP 条目检索会错配；本文件只采纳标题/年份合理的命中，未稳定核到 DOI 的写「doi:待核查」。

字段 schema 同 db03：`method_name, task_type, input_data, output_result, core_assumption, advantages, limitations, common_baselines, evaluation_metrics, suitable_datasets, implementation_repo, representative_papers, possible_innovation_points, maturity`

## 方法卡

```yaml
- method_name: 序列到序列与注意力机制 (Seq2Seq Attention / Transformer)
  task_type: 机器翻译、摘要、问答、序列标注到生成、通用 encoder-decoder 建模
  input_data: token 序列、位置编码、源/目标文本对；可扩展到语音/视觉 token
  output_result: 目标序列概率分布、对齐/注意力权重、生成文本
  core_assumption: 序列元素之间的依赖可由注意力动态加权建模；Transformer 用自注意力替代循环结构以并行捕捉长程依赖
  advantages: 长程依赖强、并行训练快、成为大模型基础架构；attention 对齐可辅助解释
  limitations: 自注意力 O(n²) 成本高；长上下文需稀疏/线性注意力或检索；生成易幻觉，需事实核验
  common_baselines: RNN/LSTM Seq2Seq、CNN Seq2Seq、Transformer、T5/BART、检索增强模型
  evaluation_metrics: BLEU、ROUGE、chrF、BERTScore、exact match/F1、人评事实性
  suitable_datasets: WMT、CNN/DailyMail、XSum、SQuAD、GLUE/SuperGLUE
  implementation_repo: Hugging Face Transformers、fairseq、OpenNMT、MarianNMT
  representative_papers:
    - "Neural Machine Translation by Jointly Learning to Align and Translate | 2014 | cited:14620 | doi:10.48550/arxiv.1409.0473 | checked:2026-06-10"
    - "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer | 2019 | cited:8337 | doi:10.48550/arxiv.1910.10683 | checked:2026-06-10"
  possible_innovation_points: 长上下文高效注意力、事实一致性约束、检索增强与引用定位、多语言迁移、轻量蒸馏部署; domain_scope=NLP语音
  maturity: 经典  # 注意力/Transformer 已是 NLP 基础范式，新工作需与强预训练模型比较

- method_name: 文本到文本预训练与指令式生成 (T5 / GPT-3 式 few-shot)
  task_type: 多任务 NLP 统一建模、prompt/few-shot 学习、文本生成与推理
  input_data: 自然语言指令或任务前缀 + 文本上下文；大规模无监督/弱监督语料
  output_result: 任务答案、生成文本、分类标签文本化输出、few-shot 预测
  core_assumption: 足够大规模的语言模型可把多任务统一为文本条件生成；上下文示例可诱导临时任务行为
  advantages: 任务接口统一、少样本能力强、迁移范围广；适合快速原型和低标注场景
  limitations: 幻觉与不可控输出；成本高；对 prompt 敏感；事实/引用必须外部校验；闭源模型复现性受限
  common_baselines: BERT/RoBERTa fine-tuning、T5/BART、GPT-3/LLM few-shot、LoRA/PEFT 微调、RAG
  evaluation_metrics: 任务指标(Acc/F1/EM/ROUGE/BLEU)、校准、事实性、人类偏好、成本/延迟
  suitable_datasets: GLUE、SuperGLUE、MMLU、BIG-bench、SQuAD、CNN/DailyMail
  implementation_repo: Hugging Face Transformers/PEFT、OpenAI API、vLLM、llama.cpp、T5X
  representative_papers:
    - "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer | 2019 | cited:8337 | doi:10.48550/arxiv.1910.10683 | checked:2026-06-10"
    - "Language Models are Few-Shot Learners | 2020 | cited:3029 | doi:10.48550/arxiv.2005.14165 | checked:2026-06-10"
  possible_innovation_points: 领域指令数据构建、轻量微调与 RAG 结合、事实性/引用约束、中文/低资源评测、成本-质量折中; domain_scope=NLP语音
  maturity: 主流  # LLM 时代核心范式，但科研场景必须配事实核验与复现说明

- method_name: 检索增强生成 (RAG)
  task_type: 知识密集型问答、文档问答、科研资料助手、可追溯生成
  input_data: 用户问题、检索语料库、向量/关键词索引、top-k 文档片段
  output_result: 带依据的答案、引用片段、检索命中文档、生成过程证据链
  core_assumption: 参数知识不足或过时的问题可通过外部检索补足；生成模型应基于检索证据而非凭空回答
  advantages: 降低幻觉、知识可更新、可给来源；适合本地资料库/论文库/项目文档问答
  limitations: 检索召回差会直接导致错误；chunking/重排/引用定位复杂；生成仍可能不忠实；评测比普通 QA 更难
  common_baselines: closed-book LLM、BM25-only QA、dense retrieval + reader、FiD、long-context 直接读
  evaluation_metrics: retrieval recall@k、MRR/NDCG、answer F1/EM、faithfulness、citation precision/recall、RAGAS 指标
  suitable_datasets: Natural Questions、MS MARCO、HotpotQA、FEVER、企业/科研内部文档库
  implementation_repo: LlamaIndex、LangChain、Haystack、FAISS、Milvus、Qdrant、RAGAS
  representative_papers:
    - "Retrieval-Augmented Generation for Large Language Models: A Survey | 2023 | cited:646 | doi:10.48550/arxiv.2312.10997 | checked:2026-06-10"
    - "Active Retrieval Augmented Generation | 2023 | cited:323 | doi:10.18653/v1/2023.emnlp-main.495 | checked:2026-06-10"
  possible_innovation_points: query rewriting、多跳检索、结构化引用定位、领域知识图谱+RAG、检索失败检测、长期记忆与项目库结合; domain_scope=NLP语音
  maturity: 主流  # 实践主流但仍工程细节决定质量；科研助手必须强制引用定位

- method_name: 连接时序分类与端到端 ASR (CTC / Conformer)
  task_type: 自动语音识别(ASR)、语音到文本、流式识别、音素/字符序列解码
  input_data: 语音波形或声学特征(log-mel)、转写文本；可带语言模型
  output_result: 字符/子词序列、词时间戳、置信度、n-best hypothesis
  core_assumption: CTC 通过 blank 与条件独立近似对齐变长输入输出；Conformer 用卷积捕捉局部声学模式、Transformer 捕捉全局依赖
  advantages: 端到端训练简化传统 HMM-GMM 管线；Conformer 在准确率与并行性上强；可做流式/离线两种部署
  limitations: CTC 条件独立限制语言建模；低资源/口音/噪声/远场仍难；流式低延迟与准确率权衡
  common_baselines: HMM-GMM、LAS/Attention encoder-decoder、RNN-T、wav2vec2/HuBERT + CTC、Whisper
  evaluation_metrics: WER/CER、RTF(实时率)、延迟、噪声/口音分组 WER、置信度校准
  suitable_datasets: LibriSpeech、Common Voice、VoxPopuli、AISHELL、Speech Commands
  implementation_repo: ESPnet、Kaldi、k2/icefall、NVIDIA NeMo、SpeechBrain、torchaudio
  representative_papers:
    - "Connectionist temporal classification | 2006 | cited:5439 | doi:10.1145/1143844.1143891 | checked:2026-06-10"
    - "Conformer: Convolution-augmented Transformer for Speech Recognition | 2020 | cited:2737 | doi:10.21437/interspeech.2020-3015 | checked:2026-06-10"
  possible_innovation_points: 低资源/方言适配、流式 Conformer、端侧压缩、噪声鲁棒与多麦克风、ASR 置信度与人工复核; domain_scope=NLP语音
  maturity: 主流  # CTC 是端到端 ASR 基础损失，Conformer 是强工业/学术基线

- method_name: 自监督语音表征学习 (wav2vec 2.0 / HuBERT)
  task_type: 低标注语音识别、语音表征预训练、说话人/情感/音频事件迁移
  input_data: 大规模未标注语音波形，少量转写标注；可带离散聚类伪标签
  output_result: 上下文语音表示、微调后的 ASR/分类模型、低资源任务特征
  core_assumption: 遮蔽预测/对比学习能从原始语音中学习音素/声学结构，少量标注即可适配下游任务
  advantages: 显著降低标注需求；低资源语言表现好；可迁移到多类语音任务；预训练模型生态成熟
  limitations: 预训练成本高；域/语言不匹配会掉点；伪标签质量影响 HuBERT；隐私与版权需审查
  common_baselines: MFCC/filterbank + HMM、supervised Conformer、CPC、WavLM、Whisper
  evaluation_metrics: WER/CER、低资源小时数曲线、下游分类 Acc/F1、跨语种迁移性能
  suitable_datasets: LibriSpeech、Common Voice、VoxPopuli、AISHELL、TED-LIUM
  implementation_repo: fairseq wav2vec、Hugging Face Transformers、SpeechBrain、ESPnet
  representative_papers:
    - "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations | 2020 | cited:407 | doi:待核查 | checked:2026-06-10"
    - "HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units | 2021 | cited:269 | doi:10.1109/taslp.2021.3122291 | checked:2026-06-10"
  possible_innovation_points: 专业领域语音预训练、低资源中文方言、隐私保护语音表征、轻量蒸馏、跨模态音视频预训练; domain_scope=NLP语音
  maturity: 主流  # 自监督语音预训练已成为低资源 ASR 标准路线

- method_name: 大规模弱监督语音识别与翻译 (Whisper 类模型)
  task_type: 多语言 ASR、语音翻译、嘈杂真实场景转写、字幕生成
  input_data: 大规模弱标注音频-文本对、多语言音频、任务 token(转写/翻译/语言识别)
  output_result: 多语言转写文本、翻译文本、时间戳、语言识别结果
  core_assumption: 海量弱监督数据可带来跨语言/跨域鲁棒性；统一 seq2seq 解码可同时处理 ASR 与翻译
  advantages: 开箱即用、多语言强、噪声/口音鲁棒；小项目无需自训练即可转写访谈/会议/视频
  limitations: 专有/敏感音频上传合规风险；低资源语言仍可能错；幻听/重复/时间戳漂移需人工校对；模型大
  common_baselines: supervised Conformer/RNN-T、wav2vec2/HuBERT fine-tune、Google/Azure/科大讯飞 ASR、传统 Kaldi
  evaluation_metrics: WER/CER、BLEU/COMET(翻译)、语言识别准确率、时间戳误差、人工校对耗时
  suitable_datasets: LibriSpeech、Common Voice、VoxCeleb、FLEURS、真实会议/访谈数据(需授权)
  implementation_repo: openai/whisper、faster-whisper、whisper.cpp、Hugging Face Whisper
  representative_papers:
    - "Robust Speech Recognition via Large-Scale Weak Supervision | 2022 | cited:1159 | doi:10.48550/arxiv.2212.04356 | checked:2026-06-10"
    - "Common Voice: A Massively-Multilingual Speech Corpus | 2019 | cited:209 | doi:10.48550/arxiv.1912.06670 | checked:2026-06-10"
  possible_innovation_points: 领域术语热词/提示、端侧部署、隐私本地化转写、多说话人分离+ASR、字幕质量评估与人工校对工作流; domain_scope=NLP语音
  maturity: 主流  # 通用转写任务强基线，但科研数据合规和人工核对仍不可省
```
