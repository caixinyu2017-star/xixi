<!--
图表规划卡模板（单张图/表一张卡）。
用途：把"这张图讲什么故事、放哪节、绑哪条 claim"（叙事层）与"图型/尺寸/栏宽键/配色/无障碍"（规格层）一次定死，交 m11(light-figure-drawing) 照卡执行。
双层设计对齐 m09 SKILL「每个图表的规划卡」：
  - db07 基础字段可沉淀为 figure_card；
  - 项目执行辅助字段只进规划交付 / manifest，不作为 db07 必填 schema。
栏宽键取值与 light-figure-drawing scripts/figure_export.py 的 JOURNAL_SPECS 唯一真相源对齐。
-->

# 图表规划卡 · {{figure_id}}

> 一张卡 = 一张图或表。上层叙事先定，下层规格再定；规格层缺 target_journal/column 时 m11 会打回本技能补，不自行猜栏宽。

## 上层 · 叙事（这张图为什么存在）

| 字段 | 内容 |
|------|------|
| **figure_id** | `F#` 命名图、`T#` 命名表（与 m07 论文模板 `[图位 F1]`/`[表位 T1]` 占位对齐） |
| **绑定 claim** | 这张图支撑论文的哪一条 claim（一条，写清）；删掉它论文会缺哪一块 |
| **讲什么故事** | 一句话：读者看完这张图应得到什么结论 |
| **放哪节** | 正文哪一节 / 附录 / graphical abstract；`where_to_place_in_paper` |
| **优先级** | 必做（支撑核心贡献）/ 可做（增强）/ 可删（冗余或弱） |
| **组图归属** | 若属某组图，写明 panel 角色（overview / deviation / relationship），并说明本 panel 回答的**唯一科学问题**（遮住它会丢什么独有信息——防冗余检验） |

## 下层 · 规格（怎么把它画对）

### db07 基础字段（可沉淀为 figure_card）

| 字段 | 内容 |
|------|------|
| **figure_type** | 图型（全库唯一键，如 `跨数据集主结果对比(分组柱+误差棒)`） |
| **purpose** | 图的作用 |
| **data_required** | 需要哪些数据（不足回 m06/m02 取） |
| **layout** | 布局（单图 / GridSpec 几行几列 / 跨格） |
| **color_scheme** | 配色约束：离散用 Okabe-Ito（≤8 类）/ 连续用 viridis·cividis；同论文统一调色板（登记 db07） |
| **annotation_style** | 标注：panel 标号 a/b/c、误差棒类型(SD/SEM/CI)+样本量 n、显著性标记、单位入括号 |
| **caption_style** | caption 能否脱离正文独立读懂 |
| **possible_code_tool** | 建议工具（matplotlib/seaborn/ggplot2/TikZ/Graphviz/Inkscape…） |
| **replication_notes** | 复现要点 |

### 项目执行辅助字段（只进规划交付 / manifest）

| 字段 | 内容 |
|------|------|
| **target_journal** | 目标期刊键，取 figure_export.py `JOURNAL_SPECS` 之一：`nature`/`science`/`cell`/`plos`/`ieee`/`elsevier`/`mdpi`；表外刊（如中文刊）填 `custom` 并补 `custom_width_mm`（数据须有来源：db01 卡或实测，禁止臆测） |
| **column** | 栏宽档位，须为该刊在 `JOURNAL_SPECS` 实有的键：`single`/`double`/`full`(仅 science/mdpi)/`onehalf`(仅 plos/elsevier)；`custom` 时省略，以 `custom_width_mm` 为准 |
| **尺寸/格式** | 由 `target_journal`+`column` 锁定物理栏宽 mm、最小字号、首选格式；m11 直接 `save_for_journal(fig, base, journal=target_journal, column=column)` |
| **caption_draft** | caption 初稿 |
| **output_formats** | 矢量(PDF/EPS/SVG) + 位图(TIFF/PNG)，按刊首选格式 |
| **source_card（必填）** | 命中的 db07 canonical 来源，如 `databases/db07-figures/resources_real.md::<figure_type>`；全新模式标 `new_canonical_candidate -> databases/db07-figures/resources_real.md` 并后续回写 db07 |

## 无障碍 / 投稿前自检（交卡前过一遍）

- [ ] 配色色盲安全：Okabe-Ito 或 viridis 系；颜色之外加冗余编码（线型/marker）。
- [ ] 灰度可辨：黑白打印仍能区分各系列。
- [ ] 字号：最终印刷尺寸下达目标刊下限（缩放后仍 ≥ 下限，用 `check_scaled_fonts` 复核）。
- [ ] 坐标轴标签含单位；误差棒注明类型与 n；显著性标记齐全。
- [ ] 物理尺寸 = 目标栏宽（`check_figure_size` 复核，勿被 bbox tight 静默裁剪）。
- [ ] 去 chart junk；不误导（y 轴不偷偷截断、慎用双 y 轴）。
- [ ] 组图：每个 panel 回答唯一科学问题，无冗余。

---

**交接**：本卡交 m11(light-figure-drawing) 执行——m11 读 `source_card` 照卡画、读 `target_journal/column` 锁栏宽、导出后跑 `check_figure_size`/`check_scaled_fonts`。项目级风格/图号/caption/导出路径登记到 `databases/db09-projects/projects/<project_name>/figures/manifest.md`。
