# Reporting-Guideline 映射表

按研究类型选对应的报告规范。落笔 Methods/Results 前先认领清单，把必报条目映射进对应小节，避免审稿时被"未按 X 报告"打回。
下列规范名与归口组织为公开常识；具体条目数与当年版本以官方站点为准（投稿前核对当年清单）。

---

## 1. 研究类型 → 规范速查

| 研究类型 | 规范 | 配套图/件 | 归口/站点 |
|---|---|---|---|
| 随机对照试验(RCT) | **CONSORT** | 流程图 + 25 条清单 | consort-statement.org |
| 观察性研究(队列/病例对照/横断面) | **STROBE** | 22 条清单 | strobe-statement.org |
| 系统综述 / Meta 分析 | **PRISMA** (2020) | 流程图 + 27 条清单 | prisma-statement.org |
| 诊断准确性研究 | **STARD** | 流程图 + 30 条清单 | equator-network.org（STARD） |
| 预测模型(开发/验证) | **TRIPOD** (含 TRIPOD+AI) | 清单 | tripod-statement.org |
| 动物实验(临床前) | **ARRIVE** 2.0 | Essential 10 + Recommended | arriveguidelines.org |
| 个案报告 | **CARE** | 清单 + 时间线 | care-statement.org |
| 定性研究 | **SRQR / COREQ** | 清单 | equator-network.org |
| 研究方案(protocol) | **SPIRIT**(试验) / **PRISMA-P**(综述) | 清单 | 同上 |

> 一站式索引：EQUATOR Network（equator-network.org）汇总各领域报告规范，找不到时先查它。

---

## 1b. CS/ML 报告件（本技能范例与主要受众，别只借医学规范）

CS/ML 投稿很少触发 CONSORT/STROBE 等医学规范，但顶会/顶刊有自己的报告件，落笔前认领：

| 研究类型/场景 | 报告件 | 要点 | 归口/出处 |
|---|---|---|---|
| ML 论文通用（NeurIPS/ICLR/ICML 等） | **Reproducibility Checklist / Paper Checklist** | 模型/数据/算力/超参/随机性/限制/社会影响逐条勾选，多数顶会投稿强制 | NeurIPS/ICLR 官方（当年版） |
| 发布数据集 | **Datasheets for Datasets** | 动机/构成/采集/预处理/用途/分发/维护/伦理（对齐 m02 data_card + croissant_export） | Gebru et al. 2021 |
| 发布模型 | **Model Cards** | 预期用途/训练数据/评估/局限/偏差/伦理考量 | Mitchell et al. 2019 |
| 预测模型（含 ML） | **TRIPOD+AI** | 开发/验证、校准、外部验证 | tripod-statement.org |
| 涉人体数据/众包标注 | venue 的 **Ethics / Broader Impact** 声明 + IRB | 知情同意、隐私、潜在滥用（联动 a10） | venue 当年要求 |

> 落地：①投 NeurIPS/ICLR 先填该会**当年** reproducibility/paper checklist，逐条映射到正文+附录；②发数据集随论文附 Datasheet（可由 m02 data_card + croissant 机读卡生成）；③发模型附 Model Card；④这些进 mandatory_inclusions 的声明位。**别因 guideline_map 偏医学就给 CS/ML 论文硬套 CONSORT**。

---

## 2. 任务速判（题述触发词 → 认领哪份）

- "我们随机分组对比 A/B 干预" → **CONSORT**（+ 注册号、CONSORT 流程图）。
- "我们回顾性/前瞻性观察队列，无干预分配" → **STROBE**。
- "我们系统检索并综合已有研究" → **PRISMA**（+ PRISMA 流程图、检索式、纳排标准；见 02_review_survey.md 的 F1 图位）。
- "我们评估某检测/诊断方法相对金标准的准确性" → **STARD**。
- "我们建/验一个风险或结局预测模型" → **TRIPOD**（ML 模型用 TRIPOD+AI）。
- "我们用动物做实验" → **ARRIVE 2.0**（Essential 10 必报：样本量、分组、盲法、纳排、统计等）。
- "我们详述一个患者/单一案例" → **CARE**（+ 知情同意、时间线，见 04_case_study.md）。
- "我们做访谈/扎根理论等定性研究" → **SRQR**（或访谈类用 **COREQ**）。

---

## 3. 落地动作

- [ ] 认领规范后，把清单逐条映射到模板小节（如 STROBE 12 项→Methods 各段）。
- [ ] 流程类规范（CONSORT/PRISMA/STARD）务必出**流程图**，交 m09 绘制，正文留[图位]。
- [ ] 临床/动物研究的伦理与注册号属强制项，进 mandatory_inclusions.md 的声明位。
- [ ] 纯 CS/ML 非人体实验通常不触发上述医学规范，但若涉**预测模型**仍可借 TRIPOD+AI；遵 venue 的 Repro/Ethics/Broader-Impact 要求。
- [ ] 投稿前到 EQUATOR / 官方站点核对**当年版本**清单（版本逐年微调）。