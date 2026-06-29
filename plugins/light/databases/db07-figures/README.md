# db07 — 科研图表与可视化案例库

学习顶刊顶会图表的审美、布局、配色与组图逻辑，重点学"图表如何支撑论点"，服务 m09(图表规划) 与 m11(绘图)。

## 这个库是什么(诚实卖点)

**不是**"N 张实测卡 + 工具被引数字库",而是**制图方法论(craft)精养 + 偏科按 research_field 过滤**:

- **方法论层(本地精养,护城河)**:31 张 figure_card 的 purpose(图↔claim 映射)/layout/color_scheme/replication_notes 等是跨学科制图 craft,几乎不过时,是 m09/m11 的真正消费对象。通用诚实性铁律去重上提为下方 R1-R9 单一真相源。
- **偏科隔离层(用现有 research_field 字段,非新增 domain_scope)**:领域专属图型(volcano/Manhattan/KM/CONSORT/Bland-Altman/PRISMA/forest/calibration)随该卡 research_field 隔离;`research_field=通用` 即通用层对所有可见,其余为偏科层,planning 按项目方向过滤。受控取值表见下。
- **薄缓存**:资源表的工具论文被引数是快照(last_checked=2026-06-06、会增长、作背书非权威),DOI 已在表内可随时 OpenAlex 手查;栏宽尺寸由 figure_export.py::JOURNAL_SPECS 独占真相源,db07 不碰。

## figure_card schema
`figure_type, paper_source, research_field, purpose, data_required, layout, color_scheme, annotation_style, caption_style, possible_code_tool, replication_notes, where_to_place_in_paper`

## 制图方法论铁律 R1–R9（诚实性单一真相源，各卡 replication_notes 以"遵 R#"引用）

- **R1** y 轴不截断(尤其柱状图从 0 起),要截断须显式断轴标记。
- **R2** 气泡/面积图：面积 ∝ 数值,非半径 ∝ 数值(否则视觉夸大)。
- **R3** 雷达图：统一方向、轴数 ≤6、各轴量纲归一并标注。
- **R4** 相关 ≠ 一致性：方法学比较用 Bland-Altman,不能只给 R²/散点。
- **R5** 小样本(n≲20)叠原始散点,不只画均值±误差棒。
- **R6** 跨子图热力图固定同一 vmin/vmax,色标可比。
- **R7** 误差棒必须注明是 SD/SEM/CI 哪种 + 样本量 n。
- **R8** 色盲友好(viridis/ColorBrewer/Okabe-Ito) + 黑白打印靠线型/标记冗余区分,不靠颜色单一编码。
- **R9** 多 panel 反冗余：每个 panel 回答唯一科学问题,不重复同一信息。

> 执行端 lint 规则对齐 [light-figure-drawing/references/figure_integrity.md](../../skills/light-figure-drawing/references/figure_integrity.md)(本节是案例库侧的方法论真相源,不复写执行细节)。

## research_field 受控取值表（偏科隔离过滤键）

`通用`=通用层(对所有方向可见);以下为偏科层(planning 仅在 claim 命中领域专属图型时取):

| research_field | 典型图型 | 偏科 |
|---|---|---|
| 通用 | 柱/箱/折线/散点/雷达/热力/ECDF/小提琴/气泡/multi-panel | 否(对所有方向可见) |
| 系统综述 / 文献调研 | PRISMA 流程图 | 是 |
| 临床试验 / 干预研究 | CONSORT 流程图 | 是 |
| 生物医学 / 生存分析 | Kaplan-Meier 曲线 | 是 |
| 医学统计 / meta-analysis | forest plot | 是 |
| 医学测量 / 方法学比较 | Bland-Altman | 是 |
| 机器学习 / 临床预测 | 校准曲线 calibration | 是 |
| 组学 / 差异表达 | volcano plot | 是 |
| 遗传学 / GWAS | Manhattan / QQ | 是 |
| 单细胞 / 表征学习 | UMAP / t-SNE | 跨域偏通用 |

> 缺项降级：项目方向(db09 项目卡 domain)缺失时不过滤、全集候选,不漏卡。

## 数据来源
CVPR/ICCV/ECCV/NeurIPS/ICLR/ICML/AAAI/ACL/KDD/CHI 顶会，Nature/Science/Cell，Papers With Code，matplotlib/seaborn/plotly/ggplot2 gallery，Observable，Datawrapper examples，IEEE VIS。

## 图表类型库
折线、柱状、箱线、热力、雷达、散点、误差棒、混淆矩阵、ROC、PR、消融图、参数敏感性图、模型框架图、流程图、技术路线图、数据集示意图、可解释性可视化、真实效果图。

## 配色规范（统一）
- 色盲友好：viridis / ColorBrewer / Set2。
- 同一论文统一调色板（由 a07 跨图维护，链 db05/db06）。
- 黑白打印可辨：线型 + 标记 双重区分。
- 矢量优先(PDF/SVG)，位图 ≥300 dpi。

## 图表类型 → 工具 → 用途速查

| figure_type | 推荐工具 | 主要用途 |
|---|---|---|
| 主结果对比 | matplotlib/seaborn 柱状+误差棒 | 证明优于 baseline |
| 消融 | 分组柱状/折线 | 证明各组件贡献 |
| 参数敏感性 | 折线(多曲线) | 鲁棒性/调参分析 |
| ROC/PR/混淆矩阵 | sklearn + matplotlib | 分类性能 |
| 模型框架图 | TikZ/draw.io/Illustrator | 方法概览 |
| 流程/技术路线 | Graphviz/Mermaid/TikZ | 整体流程 |
| 可解释性 | SHAP/注意力热力图 | 机理证据 |
| 真实效果图 | 拼图(GridSpec/PPT) | 定性结果 |

## 使用方式
重点学"图支撑哪个 claim"，而非只学样式。每张参考图沉淀 figure_card，标注"放论文哪里"。

模板与 canonical 索引见 [figure_cards.md](figure_cards.md)（0 张实体卡，避免重复 `figure_type`）。

## 采集→核验→入库管线（照此复现可扩库，与 db01/db05/db06 同口径）
1. **采集**：从上述顶刊顶会与 gallery 记图型的轴/标注规范、配色、组图逻辑与"支撑哪个 claim"，顶刊实例只存元数据级引用（DOI+图号，**不存原图**——版权纪律）；自家产出（如 g1-g9 九图）来源最硬，直接反哺卡。
2. **核验（铁律）**：实例 DOI 经 OpenAlex 回查（不盲取 search 第一条，比对年份/被引/DOI 合理性），gallery 链接 `curl` 取 HTTP 状态；栏宽/配色衔接 `light-figure-drawing/scripts/figure_export.py` 的 `JOURNAL_SPECS` 实测值，不凭记忆填；抽查 ≥20% 新卡（记录落 `_verification_log/`）。
3. **入库**：按 `figure_card` schema 填卡，YAML 值含英文冒号须紧跟非空格或加引号；新卡文件放本目录，在「真实资源文件」节加链接。
4. **校验**：`PYTHONUTF8=1 python .github/scripts/check_databases.py` 全绿（按 SCHEMA 强校验 `resources_real.md` 与 `*_cards.md`）。
5. **落日期**：每张卡/每个卡文件标 `核验日期 YYYY-MM-DD`，供 [check_freshness.py](../../.github/scripts/check_freshness.py) 月度统计（warn-only，不阻断 CI）。

## 真实资源文件
- [resources_real.md](resources_real.md) — 真实绘图资源清单（Matplotlib/Seaborn/ggplot2 gallery、SciencePlots、ColorBrewer、viridis、Graphviz、BioRender 等）+ 通用 figure_card（按"支撑哪个 claim + 工具 + 放论文哪里"组织）。工具论文被引数为 OpenAlex 快照(last_checked=2026-06-06、会增长、作背书),DOI 在表内可随时手查。
- [figure_advanced_cards.md](figure_advanced_cards.md) — 高级科研图表模式（PRISMA、CONSORT、KM、forest plot、Bland-Altman、校准曲线、volcano、Manhattan/QQ、UMAP 等 9 卡，官网/OpenAlex 核验）。
- [self_produced_cards.md](self_produced_cards.md) — **自家产出反哺卡**（resampling-calibration-study 的 g1-g9 九图：雷达/小提琴/斜率/气泡/发散条/矩阵热力/山脊/ECDF/棒棒糖，来源最硬——代码+700 行真实数据在仓库内可复跑，2026-06-12）。
- [spectrum_fill_cards.md](spectrum_fill_cards.md) — 谱系补缺卡（箱线、数据集示意、组图 multi-panel 3 卡，matplotlib/seaborn gallery HTTP 200 核验 2026-06-12）。
