# P1 优化台账（硬编码阈值 / 领域 profile / 结构化多样性）

> 起始 2026-06-13 ｜ 范围（已与用户拍板）：**idea-critique 深做（三块全修）+ 顺手清 citation/literature-search/paper-polishing 的相似度/比例魔数**。
> 依据口径（已拍板）：硬编码阈值/权重 → **显式声明为可调超参 + 写默认值理由（承认是经验设定，不虚构权威出处）+ 让函数可注入阈值**；calibration.py 改三分类，作为"用户有标注集时可反推"的工具（现在 Light 无真实标注集，**不假装有依据**——这是诚实底线）。
> 硬纪律：改脚本前读真实文件、改后跑 `--selftest`（离线过）+ 四 CI；提交只署用户本人、中文 commit。

---

## P1 三类问题（总览第三节 3/5/6 + idea-critique 详档可优化点）

| 类 | 问题 | 主要落点 |
|---|---|---|
| **阈值** | 关键阈值/权重硬编码无依据 | idea-critique（通过线 80、八维权重、否决线 45/60）；citation+lit-search（sim<0.6）；paper-polishing（被动 0.4） |
| **领域 profile** | rubric anchor 偏 ML，宣称通用 | idea-critique rubric 数据/实验维 anchor（backbone/消融/baseline）对理论/数学/systems/HCI-定性不适配 |
| **结构化多样性** | 单模型扮多视角=伪多样性 | idea-critique 五视角靠 prompt 自律，无可机检的张力/去重判据 |

---

## 执行进度（⬜待办 / 🔧进行中 / ✅完成）

### idea-critique（深做，本轮主战场）
- ✅ I1 score_aggregate.py — 阈值提为 DEFAULT_THRESHOLDS 具名配置（每行写默认值理由）+ 顶部"依据声明"（承认权重是经验设定非 NeurIPS 官方/非数据反推）+ decide(thresholds=) 可注入 + 新增 weight_sensitivity() 敏感性分析；修 selftest 51.2→51.0 bug；selftest 加 [G]阈值注入/[H]敏感性 用例，全过
- ✅ I2 calibration.py — 改三分类(accept/revise/reject)：CalibItem.actual_outcome 取代 actual_accept；strict_FNR(误杀最终会发表的)/FPR(放行真被拒)/revise_match(需修订识别)取代旧二分类；修"有条件通过当拒稿高估 FNR"的根本缺陷；含三类混淆矩阵+逐类 P/R+回归断言+非法值 guard，selftest 过
- ✅ I3 rubric.md — 第5行锚定声明改为"维度构成不自创但权重/阈值是经验设定"+ 顶部依据警示框；权重表/decision mapping 表标注"可调超参"+ 具名键(pass_line 等)与脚本 DEFAULT_THRESHOLDS 对齐；末尾加调阈值/反推路径(不假装有数据背书)
- ✅ I4 rubric.md 领域 profile — 新增 §0.5 领域 profile 表(ml-empirical默认/theory-math/systems/biomed-clinical/hci-qualitative/design-artifact)，每档给"数据/实验"两维替换 anchor(理论用证明草图、定性用编码信度等)；只换证据形态不换权重；CONSORT/GRADE 收进 biomed 档不再混入默认
- ✅ I5 protocol.md 结构化多样性 — 四视角加可机检三标签(anchor_dim 互不同/cited_prior 引不同前作可核/blind_spot 去重≥3) + 可逐条打勾清单(不过则重抽) + 汇总规则先过清单 + anti-pattern#1 改写指向清单；保留"条件允许上真多 agent"出口
- ✅ I6 SKILL.md — Step1 加选 profile、Step4 加结构化多样性三标签机检、Step6 加阈值可调声明、Step7 pass_line 可调、calibration mode 改三分类说明、资产地图同步 weight_sensitivity/三分类

### 顺手清魔数
- ✅ M1 citation/verify_refs.py — `sim < 0.6` 提为 `TITLE_SIM_WARN=0.6` 具名常量 + 依据注释(字符 Jaccard 保守线，可调非数据反推)，告警文案带阈值
- ✅ M2 literature-search/verify_citations.py — `sim < 0.6` 提为 `TITLE_SIM_WARN=0.6`(difflib 口径) + 依据注释
- ✅ M3 paper-polishing/mechanical_check.py — 被动 `threshold=0.4` 提为 `PASSIVE_RATIO_WARN` 常量 + 依据注释 + 暴露 CLI `--passive-threshold`(threaded through run())

### 收尾
- ✅ 四 CI 全绿（51 脚本/51 登记/51 selftest）+ 改动脚本 selftest 离线过
- ✅ 记忆更新

---

## 本轮 P1 结论

**主战场 idea-critique（6 块全修）**：阈值/权重从硬编码魔数 → 具名 `DEFAULT_THRESHOLDS`/`WEIGHTS` + 顶部诚实依据声明（承认是经验设定、非 NeurIPS 官方、非数据反推）+ `decide(thresholds=)` 可注入 + `weight_sensitivity()` 敏感性分析；calibration 二分类→三分类（修"有条件通过当拒稿高估 FNR"根本缺陷）；rubric 加 §0.5 领域 profile（6 档替换数据/实验 anchor，破 ML 偏科）；protocol 五视角加可机检三标签（anchor_dim/cited_prior/blind_spot）破伪多样性；SKILL 全程同步。

**顺手清魔数（3 处）**：citation/lit-search 的 `sim<0.6`、polishing 的被动 `0.4` 全提为具名可调常量 + 依据。

**诚实底线贯穿**：所有阈值标"经验默认值、可调、非数据反推"，**不虚构权威出处**；calibration 反推路径标注"需用户自己的标注集，Light 无公开标注集不假装有依据"。

**未做（如实标注）**：真·多模型/多 agent 并行（结构化多样性只是单模型下的可机检兜底，SKILL 已标"条件允许优先真多 agent"）；其余技能的 P2（批量排序、真实检索后端）；result-analysis 的 GAP_OVERFIT 等已是具名常量本轮未动。
