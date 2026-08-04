# 图型提示词配方

每种图型给出：适用场景、推荐画幅、提示词骨架、可直接改用的完整示例。
所有提示词整体用英文；标签用引号原样写出。

---

## 通用骨架

任何一张图的提示词都由这五段拼成，顺序不要变：

```
[1 STYLE]   A flat vector infographic diagram, journal-figure style, clean white background,
            thin uniform stroke weight, restrained academic color palette of
            <2-3 个 HEX 或色名>, generous white space, crisp geometric shapes.

[2 LAYOUT]  Layout: <left-to-right flow | top-down layered | radial hub-and-spoke |
            closed feedback loop | horizontal timeline>, <N> main <stages|modules|layers>,
            evenly spaced, aligned on a strict grid.

[3 ELEMENTS] <逐个要素：形状 + 图标 + 引号里的英文标签>

[4 RELATIONS] <逐条连接：从哪到哪、箭头样式、是否带标注>

[5 CONSTRAINTS] All text in English, spelled exactly as quoted, sans-serif, legible at small size.
            No photorealism, no 3D bevel, no drop shadows, no gradients on text, no lens flare,
            no stock-photo people, no watermark, no signature, no extra decorative elements,
            no invented labels beyond those listed.
```

**配色建议**（学术场景，低饱和、打印友好、色盲可辨）：

| 用途 | 建议 |
|---|---|
| 通用学术 | deep navy `#1F3B63` + slate gray `#6B7A8F` + warm accent `#C9622E` |
| 生物/医学机制图 | teal `#2A7F7F` + sand `#D9C08C` + brick `#A8423F` |
| 工程/技术路线 | graphite `#333B44` + steel blue `#3D6E9E` + amber `#E0A33E` |
| 政策/社科框架 | ink `#2C3E50` + sage `#7A9E7E` + clay `#B5651D` |

同一篇论文里的多张图，**必须复用同一组 HEX**，在每条提示词里原样写死。

---

## 1. 示意图 / Schematic

**用途**：说明一个装置、一个场景、一个设定长什么样、各部分怎么摆。
**画幅**：`1536x1024`（横）；单栏小图用 `1024x1024`。
**要点**：空间关系比逻辑关系重要，交代清楚上下左右、包含关系、比例。

```
A flat vector schematic illustration, journal-figure style, clean white background,
thin uniform stroke weight, palette of deep navy #1F3B63, slate gray #6B7A8F and warm
accent #C9622E, generous white space.

Layout: a single cross-sectional view, viewed from the side, centered on the canvas.

Elements: an outer rounded rectangle labeled "Reaction Chamber" containing three stacked
horizontal layers; the top layer labeled "Inlet Manifold" with three small downward nozzles;
the middle layer labeled "Catalyst Bed" filled with a light dotted texture; the bottom layer
labeled "Collection Tray". A small thermometer icon on the right edge labeled "T sensor".

Relations: three thin straight arrows pointing down from the nozzles into the catalyst bed;
one thicker arrow leaving the collection tray to the right, labeled "Product Stream";
a dashed line from the thermometer icon to the catalyst bed.

All text in English, spelled exactly as quoted, sans-serif, legible at small size.
No photorealism, no 3D bevel, no drop shadows, no lens flare, no stock-photo people,
no watermark, no signature, no extra decorative elements, no invented labels.
```

---

## 2. 机制图 / 机理图 / Mechanism diagram

**用途**：说明"A 通过什么中间环节导致 B"，含调节、中介、反馈。
**画幅**：`1024x1024` 或 `1536x1024`。
**要点**：中介路径画在主轴上，调节变量从侧面用虚线指向路径**箭头本身**（不是指向变量），
反馈回路用弯曲回流箭头。这三条画法约定必须在提示词里写死，否则模型会画成普通流程图。

```
A flat vector mechanism diagram, academic journal figure style, clean white background,
thin uniform stroke weight, palette of teal #2A7F7F, sand #D9C08C and brick #A8423F.

Layout: left-to-right causal chain on a single horizontal axis, three main nodes evenly
spaced, plus one moderator above the axis and one feedback loop below.

Elements: leftmost rounded rectangle labeled "Digital Infrastructure"; center rounded
rectangle labeled "Firm Search Cost"; rightmost rounded rectangle labeled "Labor
Reallocation"; a small ellipse above the axis labeled "Market Thickness"; a small ellipse
below the axis labeled "Wage Feedback".

Relations: a solid arrow from "Digital Infrastructure" to "Firm Search Cost" labeled
"reduces"; a solid arrow from "Firm Search Cost" to "Labor Reallocation" labeled
"accelerates"; a dashed arrow from "Market Thickness" pointing down onto the middle of the
first solid arrow, indicating moderation of that path, not of a node; a curved dashed arrow
from "Labor Reallocation" looping back leftward to "Digital Infrastructure", labeled
"feedback".

All text in English, spelled exactly as quoted, sans-serif, legible at small size.
No photorealism, no 3D bevel, no drop shadows, no lens flare, no stock-photo people,
no watermark, no signature, no extra decorative elements, no invented labels.
```

---

## 3. 路径图 / 通路图 / Pathway diagram

**用途**：多条并行/分支通路，常见于信号通路、政策传导、资金流向。
**画幅**：`1536x1024`。
**要点**：并行通路必须**明确编号或命名**（Pathway I / II / III），否则模型会把它们糊成一团；
分叉点用小实心圆节点；抑制关系用平头线（⊣）而不是箭头，这点要专门写出来。

```
A flat vector pathway diagram, molecular-biology figure style, clean white background,
thin uniform stroke weight, palette of teal #2A7F7F, slate gray #6B7A8F and brick #A8423F.

Layout: left-to-right, one shared upstream trigger on the left that splits at a solid circular
junction node into three clearly separated parallel horizontal tracks, recombining into one
outcome box on the right.

Elements: leftmost hexagon labeled "Stimulus"; a small solid circular junction node; three
parallel tracks, each a row of two rounded rectangles — top track "Receptor A" then
"Kinase A", labeled "Pathway I" at its left end; middle track "Receptor B" then "Kinase B",
labeled "Pathway II"; bottom track "Receptor C" then "Kinase C", labeled "Pathway III";
rightmost rounded rectangle labeled "Transcriptional Output".

Relations: one arrow from "Stimulus" to the junction node; three arrows from the junction to
the first box of each track; one arrow along each track; three arrows converging into
"Transcriptional Output"; one flat-headed inhibition connector (a line ending in a short
perpendicular bar, not an arrowhead) from "Kinase C" to the arrow leaving "Kinase A",
labeled "inhibits".

All text in English, spelled exactly as quoted, sans-serif, legible at small size.
No photorealism, no 3D bevel, no drop shadows, no lens flare, no stock-photo people,
no watermark, no signature, no extra decorative elements, no invented labels.
```

---

## 4. 技术路线图 / Technical roadmap

**用途**：课题申报书、开题、标书里的"研究技术路线"，阶段 × 产出 × 方法。
**画幅**：`1536x1024`（默认）；阶段多于 5 个时改竖版 `1024x1536` 分层排。
**要点**：这是中文语境里最常被要求的一种图。每个阶段必须带**三行信息**（阶段名 / 方法 / 产出），
否则出来的图只是一排空盒子；阶段之间用粗箭头，阶段内部的子项用小圆点列表。

```
A flat vector technical roadmap diagram, research-proposal figure style, clean white
background, thin uniform stroke weight, palette of graphite #333B44, steel blue #3D6E9E and
amber #E0A33E.

Layout: horizontal left-to-right pipeline, four equal-width stage cards in a single row,
each card a tall rounded rectangle divided into three stacked sections, connected by thick
arrows between cards. A thin horizontal band across the bottom spanning all four cards.

Elements:
Card 1 — header "Phase 1: Data Construction"; middle section with three bulleted lines
"Panel assembly", "Variable coding", "Quality audit"; footer "Output: Clean panel".
Card 2 — header "Phase 2: Identification"; bullets "DID design", "Parallel-trend test",
"Placebo"; footer "Output: Baseline estimates".
Card 3 — header "Phase 3: Mechanism"; bullets "Mediation", "Heterogeneity",
"Sub-sample split"; footer "Output: Channel evidence".
Card 4 — header "Phase 4: Synthesis"; bullets "Robustness", "Policy simulation",
"Manuscript"; footer "Output: Submitted paper".
Bottom band labeled "Continuous: reproducibility archive and version control".

Relations: three thick horizontal arrows connecting Card 1 to 2, 2 to 3, 3 to 4;
one thin dashed feedback arrow arcing from Card 3 back to Card 2 labeled "re-specify".

All text in English, spelled exactly as quoted, sans-serif, legible at small size.
No photorealism, no 3D bevel, no drop shadows, no lens flare, no stock-photo people,
no watermark, no signature, no extra decorative elements, no invented labels.
```

---

## 5. 研究框架图 / Conceptual framework

**用途**：社科论文的理论框架，通常"理论层—变量层—实证层"三层。
**画幅**：`1024x1536`（竖）或 `1536x1024`。
**要点**：分层要用**带浅色底的横向泳道**，层名写在左侧，否则层次感会丢失。

```
A flat vector conceptual framework diagram, social-science journal figure style, clean white
background, thin uniform stroke weight, palette of ink #2C3E50, sage #7A9E7E and clay #B5651D.

Layout: top-down, three horizontal swim lanes with very light tinted backgrounds, lane labels
written vertically on the left edge; boxes centered within each lane.

Elements: top lane labeled "Theory" containing one wide rectangle "Institutional Complementarity";
middle lane labeled "Constructs" containing three equal rectangles side by side
"Policy Intensity", "Firm Capability", "Market Access"; bottom lane labeled "Empirics"
containing two rectangles "Baseline DID" and "Heterogeneity by Region".

Relations: one arrow from the theory box down to each of the three construct boxes; arrows from
all three construct boxes converging down into "Baseline DID"; one arrow from "Baseline DID"
to "Heterogeneity by Region"; one dashed upward arrow from the bottom lane back to the top
lane on the far right, labeled "feeds back".

All text in English, spelled exactly as quoted, sans-serif, legible at small size.
No photorealism, no 3D bevel, no drop shadows, no lens flare, no stock-photo people,
no watermark, no signature, no extra decorative elements, no invented labels.
```

---

## 常见失败模式与对症改法

| 症状 | 原因 | 改法 |
|---|---|---|
| 标签是乱码或伪单词 | 标签太长、字数太多、或用了中文 | 每个标签压到 1–3 个英文词；把标签数量降到 10 个以内；分两张图 |
| 中文标签糊成方块 | 模型中文字形能力弱 | 换英文；或生成时留空白框，事后在 PPT/Illustrator 里补中文 |
| 元素比要求的少 | 要素过多，模型自行删减 | 拆图，或在提示词里加 `exactly N boxes, no more, no fewer` |
| 箭头方向反了 | 只写了 "connect A and B" | 改写成 `an arrow starting at "A" and ending at "B", arrowhead on "B"` |
| 画成了 3D 立体渲染风 | 排除项没写全 | 补 `strictly 2D flat vector, orthographic, no perspective, no shading` |
| 出现虚构的图例/坐标轴 | 模型脑补 | 补 `no legend, no axes, no tick marks, no numbers` |
| 多张图风格不一致 | 每次提示词的风格段不同 | 把 `[1 STYLE]` 段整段固定复用，HEX 一字不改 |
| 密集图排版拥挤 | 画幅不够 | 换 `1536x1024`，或减少要素，或拆成上下两张 |

## 什么时候该放弃生成、改走矢量方案

出现下面任一情况，直接建议用户改用 `auto-visio-helper` / `visio-image-rebuilder`（可编辑 Visio）
或 `nature-figure`（Python/R 绘制），不要继续消耗轮次：

- 图内必须出现 15 个以上带文字的元素
- 标签必须是中文且必须精确无误（如报奖材料、正式标书）
- 交付后用户还要自己反复微调元素位置
- 图里有必须与真实数据对齐的坐标或数值
