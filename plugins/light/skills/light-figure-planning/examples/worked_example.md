<!--
figure-planning worked example：一个小型项目的 claim→图表清单全景 + 3 张填满的规划卡。
展示"必做/可做/可删"的实际判定粒度，以及图卡 vs 表卡的字段差异。
场景：奶山羊发情行为识别（与 db04/dairygoat 项目一致），方法演示用，数值为合理示例非真实采集。
-->

# Worked Example — claim→图表清单 + 3 张规划卡（奶山羊发情识别）

## Step A：claim→图表清单全景（先盘点，再决定做哪些）

论文 4 条核心 claim，逐条配图并标优先级（display item 预算：目标刊正文限 ~6 件）：

| claim | 候选 display item | 优先级 | 理由 |
|---|---|---|---|
| C1 我方法整体优于 baseline | F1 跨数据集主结果对比图（分组柱+误差棒） | **必做** | 支撑核心贡献，删了论文没有主结果 |
| C2 各模块都有贡献 | T1 消融表 | **必做** | 消融是 soundness 命门，审稿人必看 |
| C3 发情早期识别提前量更长 | F2 提前量随时间曲线 | **必做** | 这是创新点的独有卖点 |
| C4 方法整体流程 | F3 框架图 | **可做** | 帮理解但不含新数据；正文紧可降附录 |
| C4' 数据采集装置 | F4 传感器装置照片 | **可删** | 装饰性，删了不缺论证；附录或略 |
| C2' 各超参敏感性 | F5 超参热力图 | **可删/附录** | 增强但非核心，进附录省正文预算 |

> **display item 预算核查**：正文必做 = F1+T1+F2 = 3 件，可做 F3 = 4 件，≤ 目标刊 ~6 件上限 ✅。F4 删、F5 进附录。**超预算时先砍"可删"、再降"可做"到附录，绝不砍"必做"**。

---

## 卡 1（必做·图）：F1 跨数据集主结果对比

### 上层 · 叙事
| 字段 | 内容 |
|------|------|
| **figure_id** | `F1` |
| **绑定 claim** | C1：我方法在 3 个数据集上整体优于 4 个 baseline。删了论文就没有主结果证据。 |
| **讲什么故事** | 读者一眼看到：我方法（最右深色柱）在每个数据集都最高且误差棒不重叠。 |
| **放哪节** | 正文 §4.2 主结果，首个图。 |
| **优先级** | 必做 |
| **组图归属** | 单图，非组图。 |

### 下层 · 规格（db07 基础字段）
| 字段 | 内容 |
|------|------|
| **figure_type** | `跨数据集主结果对比(分组柱+误差棒)`（db07 命中 resources_real.md::bar_grouped_ci） |
| **purpose** | 多方法×多数据集的主指标比较 |
| **data_required** | 各方法各数据集 5 种子的 mean±std（来自 m06 claim_evidence_table.md） |
| **layout** | 单图，x=数据集分组，组内并列各方法 |
| **color_scheme** | Okabe-Ito 离散 5 色（4 baseline + 我方法），我方法用最深/强调色 |
| **annotation_style** | 误差棒=±std 标注 n=5；y 轴含单位；显著性 * 标在我方法 vs 次优 |
| **possible_code_tool** | matplotlib（`scripts/make_figs.py` 的 grouped_bar_ci） |

### 下层 · 规格（项目执行辅助）
| 字段 | 内容 |
|------|------|
| **target_journal** | `ieee` |
| **column** | `double`（5 数据集需宽幅） |
| **source_card（必填）** | `m06 claim_evidence_table.md / Table 2` |
| **output_formats** | PDF 矢量 + TIFF 300dpi |

---

## 卡 2（必做·表）：T1 消融表（用 table_plan_card 而非图卡）

### 上层 · 叙事
| 字段 | 内容 |
|------|------|
| **table_id** | `T1` |
| **绑定 claim** | C2：每个模块都有正贡献。必须是表——5 个变体×3 指标的精确数值对照，图读不出精确值。 |
| **讲什么** | 逐行移除一个模块，指标都下降，证明各模块必要。 |
| **放哪节** | 正文 §4.3 消融。 |
| **优先级** | 必做 |

### 下层 · 规格（表结构）
| 字段 | 内容 |
|------|------|
| **行含义** | 每行一个变体：完整模型 + 4 个"去掉 X"行；共 5 行 |
| **列含义** | 每列一个指标：Acc / F1 / 提前量(h)；共 3 列 |
| **表头分组** | 单层表头即可，无需多级 |
| **数值对齐** | 数字按小数点对齐（siunitx S 列） |
| **有效位数** | Acc/F1 1 位小数（76.3），提前量 1 位小数（6.2） |
| **最优标注** | 完整模型每列加粗（应为各列最优，证明去任一模块都变差）；按列比 |
| **显著性/不确定性** | 带 ±std（n=5）；与 m06 口径一致 |
| **单位** | 提前量列表头 "Lead time (h)" |

### 下层 · 规格（排版/格式）
| 字段 | 内容 |
|------|------|
| **booktabs 规则** | toprule/midrule/bottomrule，无竖线 |
| **跨页/横排** | 5 行 3 列小表，不跨页不横排 |
| **宽度适配** | ieee single 栏即可 |
| **caption 位置** | 表上方；表注解释"w/o X = 去掉 X 模块" |
| **source_card（必填）** | `m06 claim_evidence_table.md / 消融部分` |
| **target_journal / column** | `ieee` / `single` |

> 注意：这张是**表卡**，没有图卡的 color_scheme/layout/GridSpec——表的规格是行列结构/对齐/有效位数/booktabs，用 `table_plan_card.md` 模板。

---

## 卡 3（可做·图）：F3 方法框架图

### 上层 · 叙事
| 字段 | 内容 |
|------|------|
| **figure_id** | `F3` |
| **绑定 claim** | C4：方法整体流程。帮理解但不含新数据——故**可做**，正文紧张可降附录。 |
| **讲什么故事** | 数据流：输入→编码器→对比学习→分类头→输出，标出创新模块。 |
| **放哪节** | 正文 §3 方法开头（紧张则附录）。 |
| **优先级** | 可做 |

### 下层 · 规格
| 字段 | 内容 |
|------|------|
| **figure_type** | `方法框架图(diagram-as-code)` |
| **purpose** | 展示组件与数据流，非定量 |
| **possible_code_tool** | **Draw.io MCP**（diagram-as-code，可版本控制）或 TikZ；非 AI 生图（见 SKILL Blender/Draw.io 节） |
| **color_scheme** | 灰阶为主 + 创新模块 1 个强调色；色盲安全 |
| **target_journal / column** | `ieee` / `single`；矢量 PDF（框架图必矢量，缩放不糊） |
| **source_card（必填）** | `new_canonical_candidate -> databases/db07-figures/resources_real.md`（新框架，后续回写 db07） |

---

## 小结：本例演示的判定粒度

- **必做/可做/可删**按"删了论证缺不缺"判：F1/T1/F2 删了没主结果/消融/创新卖点 → 必做；F3 帮理解不含新数据 → 可做；F4 装饰 → 可删。
- **图 vs 表**：精确多指标对照(T1 消融)用表，趋势/比较(F1/F2)用图。
- **display item 预算**先盘全景再砍到 venue 上限内，砍序：可删 → 可做降附录 → 必做不动。
- **图卡 vs 表卡**字段不同：表卡无 color_scheme/layout，有行列结构/对齐/booktabs。
- 每张卡 `source_card` 必填、数值追溯到 m06，`target_journal/column` 取 JOURNAL_SPECS，交 m11 前可跑 `validate_plan_card.py` 校验、`recommend_chart.py` 辅助选型。

