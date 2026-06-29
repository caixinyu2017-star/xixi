# patterns.md — python-pptx 版式速查（可直接跑的代码片段）

每段都是从 `examples/build_deck.py` 抽象出的最小可运行片段。共用约定：

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def C(h):                       # hex(6位无#) -> RGBColor
    h = h.lstrip("#")
    return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

prs = Presentation()
prs.slide_width  = Inches(13.333)   # 16:9 宽屏（4:3 用 10×7.5）
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]        # 空白版式，全部自由摆放
```

色板取 `assets/themes.py`：`from themes import get_theme; t = get_theme("academic")`，
下面用 `P=t["COLORS"]["primary"]` 这类简写。设计尺度见 SKILL.md（标题 36-44pt /
正文 14-16pt、页边距≥0.5"、正文左对齐仅标题居中、每页一个重点、禁纯文字页）。

通用工具函数（被多个版式复用）：

```python
from pptx.oxml.ns import qn   # 写 <a:ea> 东亚字体

def _set_run_fonts(run, latin="Calibri", cjk="Microsoft YaHei"):
    """同时设拉丁与**东亚(CJK)字体**。run.font.name 只写 <a:latin>，中文会回退 Office
    默认字体(中文优先技能常见 bug)——补写 <a:ea>/<a:cs>，中英混排各用各的字体。"""
    run.font.name = latin
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {}); rPr.append(el)
        el.set("typeface", cjk)

def add_text(slide, x, y, w, h, text, size, color, *, bold=False,
             font="Calibri", cjk_font="Microsoft YaHei", align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for m in ("margin_left","margin_right","margin_top","margin_bottom"):
        setattr(tf, m, 0)            # margin=0 才能与形状精确对齐
    for i, item in enumerate(text if isinstance(text, list) else [(text,0)]):
        line, lvl = item if isinstance(item, tuple) else (item, 0)
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment = align; p.level = lvl
        r = p.add_run(); r.text = ("• " if lvl else "") + line
        r.font.size = Pt(size if lvl==0 else max(14,size-2))
        r.font.bold = bold and lvl==0
        _set_run_fonts(r, latin=font, cjk=cjk_font)   # 拉丁+CJK 都设，中文不回退默认
        r.font.color.rgb = C(color)
    return tb

def rect(slide, x, y, w, h, color):  # 实心无边无影矩形（色块/色带/背景）
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x),Inches(y),Inches(w),Inches(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = C(color)
    sp.line.fill.background(); sp.shadow.inherit = False
    return sp
```

---

## 0. 页背景填充（python-pptx 无原生页背景）

python-pptx 不能直接设页背景色，用全幅矩形沉到底层代替：

```python
def fill_bg(slide, color):
    sp = rect(slide, 0, 0, prs.slide_width.inches, prs.slide_height.inches, color)
    slide.shapes._spTree.remove(sp._element)      # 取出
    slide.shapes._spTree.insert(2, sp._element)   # 插到最底层（index 2 = 第一个 shape 前）
    return sp
```

---

## 1. 封面（cover）

深色主视觉块 + 大标题 + 强调色块（替代 AI 味下划线）+ 副标题 + 作者行。

```python
s = prs.slides.add_slide(BLANK)
fill_bg(s, P_bg)
rect(s, 0, 0, prs.slide_width.inches, 4.6, P_primary)        # 上 62% 深色块
add_text(s, 0.9, 1.4, 11.5, 1.4, "标题：写成有信息量的短句", 40,
         "FFFFFF", bold=True, font=F_title)
rect(s, 0.92, 2.95, 1.4, 0.09, P_accent)                     # 强调色块=重复视觉母题
add_text(s, 0.9, 3.15, 11.5, 0.8, "副标题/一句话定位", 20, "FFFFFF", font=F_body)
add_text(s, 0.9, 5.1, 11.5, 1.2,
         [("作者 · 单位 · 学院", 0), ("2026-06 · 场合", 0)], 16, P_text, font=F_body)
s.notes_slide.notes_text_frame.text = "开场 30s：点题+抛钩子，不照念标题。"
```

---

## 2. 目录（toc）

左侧大号节标题区号，右侧条目；用强调色块标“当前节”。

```python
s = prs.slides.add_slide(BLANK); fill_bg(s, P_bg)
add_text(s, 0.7, 0.5, 6, 1, "目录", 32, P_primary, bold=True, font=F_title)
items = ["研究背景与问题", "方法设计", "实验与结果", "对比分析", "结论与展望"]
for i, it in enumerate(items):
    y = 1.7 + i*1.0
    rect(s, 0.9, y+0.05, 0.5, 0.5, P_primary if i==0 else P_surface)  # 序号块
    add_text(s, 0.9, y+0.05, 0.5, 0.5, f"{i+1:02d}",
             16, "FFFFFF" if i==0 else P_muted, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font=F_en)
    add_text(s, 1.7, y, 10, 0.6, it, 20,
             P_primary if i==0 else P_text, bold=(i==0),
             anchor=MSO_ANCHOR.MIDDLE, font=F_body)
```

---

## 3. 过渡页（section transition）

整页深色 + 居中大号节标题 + 进度（第 N / 总）。过渡页是少数允许居中的页。

```python
s = prs.slides.add_slide(BLANK); fill_bg(s, P_primary)
rect(s, 5.67, 4.0, 2.0, 0.08, P_accent)                      # 居中强调短线
add_text(s, 0, 2.6, 13.333, 1.4, "02  方法设计", 40, "FFFFFF",
         bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font=F_title)
add_text(s, 0, 4.3, 13.333, 0.6, "Part 2 / 5", 16, P_secondary,
         align=PP_ALIGN.CENTER, font=F_en)
```

---

## 4. 内容页（content，行动式标题 + bullet）

顶部色带标题条 + 强调色块 + 左对齐要点。标题写成陈述结论的完整句。

```python
s = prs.slides.add_slide(BLANK); fill_bg(s, P_bg)
rect(s, 0, 0, prs.slide_width.inches, 1.25, P_surface)       # 标题条
add_text(s, 0.7, 0.32, 12, 0.8, "行动式标题：直接陈述本页结论", 26,
         P_primary, bold=True, font=F_title)
rect(s, 0.72, 1.05, 0.55, 0.07, P_accent)                    # 标题下强调块（非下划线）
add_text(s, 0.9, 1.9, 11.5, 4.5,
         [("要点一：一句话讲清", 1), ("要点二：≤40 词/页", 1),
          ("要点三：留白，别塞满", 1)], 18, P_text, font=F_body)
```

---

## 5. 结果页（results，左图右解读）

左放原生柱状图，右放 “so what” bullet（左→右阅读）。结果优先用图不用表。

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
s = prs.slides.add_slide(BLANK); fill_bg(s, P_bg)
rect(s, 0, 0, prs.slide_width.inches, 1.25, P_surface)
add_text(s, 0.7, 0.32, 12, 0.8, "本方法速度提升 2.3 倍且精度持平", 26,
         P_primary, bold=True, font=F_title)
rect(s, 0.72, 1.05, 0.55, 0.07, P_accent)
cd = CategoryChartData()
cd.categories = ["Base", "Lite", "Ours"]
cd.add_series("FPS",     (14, 22, 32))
cd.add_series("mAP×100", (87, 79, 86))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                        Inches(0.7), Inches(1.7), Inches(6.6), Inches(4.6), cd)
gf.chart.has_title = False; gf.chart.has_legend = True
add_text(s, 7.6, 1.9, 5.2, 4.3,
         [("Ours 达 32 FPS，越过实时线", 1), ("mAP 仅降 1 点", 1),
          ("参数 4.6M，可上 Jetson", 1)], 18, P_text, font=F_body)
```

要给单序列柱子单独上色（高亮 Ours 那根）：

```python
from pptx.oxml.ns import qn
plot = gf.chart.plots[0]; plot.vary_by_categories = True   # 按类别变色（单序列时）
# 或逐点：series.points[i].format.fill.solid(); ...fore_color.rgb = C(P_accent)
```

**原生图表必须套主题色**（不套则沿用 Office 默认蓝橙灰，破坏全 deck 审美统一）：

```python
def style_chart(chart, series_colors, *, font="Calibri", font_pt=12, text_color="404040"):
    """给原生 chart 各 series 上主题色 + 统一字体/字号。series_colors 取自 theme palette
    或 db09 项目 palette（与 m11 出图同色板），让 PPT 原生图表与论文图/主题色一致。"""
    for i, ser in enumerate(chart.series):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = C(series_colors[i % len(series_colors)])
    # 统一坐标轴/图例字号字体
    for axis in (chart.category_axis, chart.value_axis):
        try:
            axis.tick_labels.font.size = Pt(font_pt); axis.tick_labels.font.name = font
            axis.tick_labels.font.color.rgb = C(text_color)
        except Exception:
            pass
    if chart.has_legend:
        chart.legend.font.size = Pt(font_pt); chart.legend.font.name = font

# 用法：紧跟 add_chart 后调用，series_colors 用主题强调色族（Okabe-Ito 色盲安全）
style_chart(gf.chart, [P_primary, P_accent, "888888"], font=F_body)
```

**导入 m11 程序化出图成品（结果页常复用论文图，而非在 PPT 里重画）**：

```python
def add_figure_with_caption(slide, img_path, x, y, w, *, caption="", cap_size=14,
                            color="404040", font="Calibri", cjk_font="Microsoft YaHei"):
    """插入 m11 出的 PNG/矢量图 + 下方 caption。图按宽 w 等比缩放，caption 居中。
    论文数据图走 m11 真数据程序化绘制后在此导入，**不在 PPT 里用生成式重画数据图**。"""
    pic = slide.shapes.add_picture(img_path, Inches(x), Inches(y), width=Inches(w))
    h_in = pic.height / 914400.0      # EMU→inch，拿真实缩放后高度
    if caption:
        add_text(slide, x, y + h_in + 0.08, w, 0.5, caption, cap_size, color,
                 font=font, cjk_font=cjk_font, align=PP_ALIGN.CENTER)
    return pic
```

> 数据图来源唯一真相是 m11（真数据程序化出图）；PPT 里只**导入**成品 + 配 caption，绝不在 slides 里用 AI/生成式重画数据图（守 m11 诚实底线）。

---

## 6. 对比页（compare，高亮本方法列的表格）

表头深色、本方法列用强调色整列高亮，其余中性。

```python
s = prs.slides.add_slide(BLANK); fill_bg(s, P_bg)
rect(s, 0, 0, prs.slide_width.inches, 1.25, P_surface)
add_text(s, 0.7, 0.32, 12, 0.8, "三项指标本方法全面占优", 24, P_primary, bold=True, font=F_title)
rect(s, 0.72, 1.05, 0.55, 0.07, P_accent)
rows, cols = 4, 4
tb = s.shapes.add_table(rows, cols, Inches(0.9), Inches(1.8),
                        Inches(11.5), Inches(3.6)).table
head = ["维度", "Base", "Lite", "Ours"]
body = [["参数(M)","37.2","6.8","4.6"], ["FPS","14","22","32"], ["mAP","0.87","0.79","0.86"]]
for j, h in enumerate(head):
    c0 = tb.cell(0, j); c0.text = h
    c0.fill.solid(); c0.fill.fore_color.rgb = C(P_primary)
    pr = c0.text_frame.paragraphs[0]
    pr.font.size = Pt(15); pr.font.bold = True; pr.font.color.rgb = C("FFFFFF"); pr.font.name = F_body
for i, row in enumerate(body, 1):
    for j, v in enumerate(row):
        cell = tb.cell(i, j); cell.text = v
        hot = (j == 3)                                       # Ours 列高亮
        cell.fill.solid(); cell.fill.fore_color.rgb = C(P_accent) if hot else C(P_surface)
        pr = cell.text_frame.paragraphs[0]
        pr.font.size = Pt(14); pr.font.name = F_body
        pr.font.color.rgb = C("FFFFFF") if hot else C(P_text); pr.font.bold = hot
```

---

## 7. 时间线页（timeline / 里程碑）

一条横轴 + 等距节点 + 上下交替标注（避免文字打架）。

```python
s = prs.slides.add_slide(BLANK); fill_bg(s, P_bg)
add_text(s, 0.7, 0.5, 12, 0.8, "项目分四阶段推进", 26, P_primary, bold=True, font=F_title)
rect(s, 1.0, 3.7, 11.3, 0.06, P_secondary)                  # 主轴
nodes = [("Q1","数据采集"), ("Q2","模型设计"), ("Q3","边缘部署"), ("Q4","场测调优")]
for i,(t0,t1) in enumerate(nodes):
    x = 1.6 + i*3.5
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x-0.18),Inches(3.55),Inches(0.36),Inches(0.36))
    dot.fill.solid(); dot.fill.fore_color.rgb = C(P_accent); dot.line.fill.background()
    up = (i % 2 == 0)
    add_text(s, x-1.2, 2.5 if up else 4.2, 2.4, 1.0,
             [(t0,0),(t1,1)], 16, P_text, align=PP_ALIGN.CENTER, font=F_body)
```

---

## 8. 结论页（conclusions，学术 deck 收尾，不写 Thank You）

三条带强调色块的结论 + 一句价值升华。以 Conclusions 收尾而非空白致谢页。

```python
s = prs.slides.add_slide(BLANK); fill_bg(s, P_primary)      # 深色收尾
add_text(s, 0.9, 0.7, 12, 1, "Conclusions", 32, "FFFFFF", bold=True, font=F_en)
pts = ["在 <5M 参数下达 30+ FPS，越过边缘实时线",
       "精度几乎无损（mAP 0.86 vs 0.87）",
       "已在 Jetson Nano 完成场测部署"]
for i, p in enumerate(pts):
    y = 2.2 + i*1.1
    rect(s, 0.95, y+0.06, 0.14, 0.5, P_accent)              # 左侧强调竖块
    add_text(s, 1.3, y, 11, 0.8, p, 20, "FFFFFF", anchor=MSO_ANCHOR.MIDDLE, font=F_body)
add_text(s, 0.9, 6.2, 12, 0.6, "下一步：多目标跟踪 + 行为识别联合优化",
         16, P_secondary, font=F_body)
```

---

## 9. References 页

编号文献列表，注释色弱化，用衬线/英文字体。占位文献交付前须核实 DOI（CONVENTIONS §4）。

```python
s = prs.slides.add_slide(BLANK); fill_bg(s, P_bg)
rect(s, 0, 0, prs.slide_width.inches, 1.25, P_surface)
add_text(s, 0.7, 0.32, 12, 0.8, "References", 26, P_primary, bold=True, font=F_en)
rect(s, 0.72, 1.05, 0.55, 0.07, P_accent)
refs = ["[1] Redmon J, Farhadi A. YOLOv3. arXiv:1804.02767, 2018.",
        "[2] Howard A, et al. MobileNetV3. ICCV, 2019.",
        "[3] Ding X, et al. RepVGG. CVPR, 2021."]
add_text(s, 0.9, 1.9, 11.8, 4.4, [(r,0) for r in refs], 14, P_muted, font=F_en)
```

---

## speaker notes（每页都配）

```python
slide.notes_slide.notes_text_frame.text = "讲稿 1-2 句 + 时长 + 必讲/可略标记"
```

## 讲稿导出（speaker notes → 逐字稿初稿）

答辩/路演要逐字稿时，把每页 notes 读出来拼成初稿，再据时长扩写——无需新脚本，python-pptx 直接读：

```python
from pptx import Presentation
prs = Presentation("deck.pptx")
lines = []
for i, slide in enumerate(prs.slides, 1):
    # has_notes_slide 先判，避免访问 .notes_slide 时凭空建出空 notes
    note = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
    lines.append(f"## 第 {i} 页\n{note.strip() or '（无备注，待补）'}\n")
open("script_draft.md", "w", encoding="utf-8").write("\n".join(lines))
```

- 产出是**初稿骨架**（每页一段 notes），不是终稿——逐字稿要据每页时长（notes 里标的"30s/1min"）扩写成口语化整段，开场/转场/收尾另补。
- 与写入方向对称：上节往 notes 写"1-2 句 + 时长 + 必讲/可略"，导出时这些标记正好成为扩写依据。诚实边界：notes 为空的页如实标"待补"，不替用户编讲稿内容。

## 保存与 QA

```python
prs.save("deck.pptx")
# 内容 QA： python -m markitdown deck.pptx | grep -iE "xxxx|lorem|ipsum"
# 视觉 QA： python scripts/thumbnail.py deck.pptx     （无 soffice 也能出版式示意）
#          python scripts/to_pdf.py deck.pptx        （有 LibreOffice 时转 PDF）
```

> 端到端整合见 `examples/build_deck.py`（封面/内容/结果/对比/References 五版式 +
> 每页 notes + 幽灵 deck 测试），可直接 `python build_deck.py --theme tech` 运行。
