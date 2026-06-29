# PDF-REF — PDF 深度读取参考（copy-paste ready）

配套脚本：`scripts/pdf_ops.py`（已自检通过：meta/text/tables/merge/split/rotate）。
库职责分工见决策表。所有代码块可直接粘贴运行（Windows 记得脚本顶部加
`import sys; sys.stdout.reconfigure(encoding="utf-8")`）。

## 决策表（按任务选库）

| 任务 | 首选 | 说明 |
|------|------|------|
| 抽文本（保版面/多栏） | pdfplumber | `extract_text(layout=True)` |
| 抽表格 → DataFrame | pdfplumber | `extract_tables`，策略 lines/text |
| 内嵌文本快取 | pypdf | `page.extract_text()`，比 pdfplumber 快但不保版面 |
| 合并/拆分/旋转/加密/水印 | pypdf | 结构操作，不碰内容流语义 |
| 读元数据/书签 | pypdf | `reader.metadata` |
| 生成新 PDF | reportlab | Platypus `SimpleDocTemplate` + story |
| 扫描件 OCR | pytesseract + pdf2image | pdfplumber/pypdf 都不做 OCR |
| 命令行批处理 | qpdf / pdftotext / pdfimages | poppler-utils |

## 抽文本（pdfplumber，保版面）

```python
import pdfplumber
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text(layout=True) or ""
        print(f"--- page {i} ---\n{text}")
```

## 抽表格 → DataFrame

```python
import pdfplumber, pandas as pd
dfs = []
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        for tbl in page.extract_tables():
            if tbl and len(tbl) > 1:
                dfs.append(pd.DataFrame(tbl[1:], columns=tbl[0]))
combined = pd.concat(dfs, ignore_index=True) if dfs else None
```

无网格线的表格用 text 策略：
```python
tables = page.extract_tables({"vertical_strategy": "text",
                              "horizontal_strategy": "text",
                              "snap_tolerance": 4})
```

## 定位页面区域（论文图表/栏）

```python
import pdfplumber
with pdfplumber.open("paper.pdf") as pdf:
    page = pdf.pages[0]
    # bbox = (x0, top, x1, bottom)，单位 pt（72/inch）
    region = page.crop((0, 0, page.width / 2, page.height))  # 左半栏
    print(region.extract_text(layout=True))
```

## 可视化调试表格设置

```python
import pdfplumber
with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]
    im = page.to_image(resolution=150)
    im.debug_tablefinder()          # 叠加找到的表格线
    im.save("debug.png")            # 看完即删，勿留库内
```

## 合并 / 拆分 / 旋转（pypdf）

```python
from pypdf import PdfReader, PdfWriter

# 合并
w = PdfWriter()
for p in ["a.pdf", "b.pdf"]:
    for page in PdfReader(p).pages:
        w.add_page(page)
with open("merged.pdf", "wb") as f:
    w.write(f)

# 拆分（每页一文件）
for i, page in enumerate(PdfReader("in.pdf").pages, 1):
    w = PdfWriter(); w.add_page(page)
    with open(f"page_{i}.pdf", "wb") as f:
        w.write(f)

# 旋转第 1 页 90°
r = PdfReader("in.pdf"); w = PdfWriter()
for i, page in enumerate(r.pages):
    if i == 0:
        page.rotate(90)
    w.add_page(page)
with open("rot.pdf", "wb") as f:
    w.write(f)
```

## 加密 / 水印（pypdf）

```python
from pypdf import PdfReader, PdfWriter
r = PdfReader("in.pdf"); w = PdfWriter()
for page in r.pages:
    w.add_page(page)
w.encrypt("userpw", "ownerpw")     # 用户密码 + 所有者密码
with open("enc.pdf", "wb") as f:
    w.write(f)

# 水印：把水印页 merge 到每页
wm = PdfReader("watermark.pdf").pages[0]
r = PdfReader("in.pdf"); w = PdfWriter()
for page in r.pages:
    page.merge_page(wm); w.add_page(page)
with open("wm.pdf", "wb") as f:
    w.write(f)
```

## 扫描件 OCR（pytesseract + pdf2image，需另装）

```python
# pip install pytesseract pdf2image ; 系统装 tesseract + poppler
import pytesseract
from pdf2image import convert_from_path
text = ""
for i, img in enumerate(convert_from_path("scanned.pdf"), 1):
    text += f"--- page {i} ---\n"
    text += pytesseract.image_to_string(img, lang="chi_sim+eng")
print(text)
```

## 命令行（poppler-utils / qpdf）

```bash
pdftotext -layout input.pdf out.txt          # 保版面抽文本
qpdf --empty --pages a.pdf b.pdf -- merged.pdf
qpdf in.pdf --pages . 1-5 -- p1-5.pdf         # 拆页
qpdf in.pdf out.pdf --rotate=+90:1            # 旋转第 1 页
pdfimages -j input.pdf prefix                 # 抽图为 jpg
```

## 已知坑

- pdfplumber/pypdf **都不做 OCR**，纯图扫描件抽不出文本。
- pypdf 解析大内容流吃内存（300MB 未压缩流见过要 10GB RAM）；先 `len(page.get_contents().get_data())` 预判。
- reportlab **绝不要用 Unicode 上下标**（₀₁₂ ⁰¹²）会渲染成黑块；用 Paragraph 内 `<sub>`/`<super>`。
- pdfplumber 基于 pdfminer.six，比 pymupdf 慢；表格策略默认 `lines`，无网格线要切 `text`。

## 链接（均 2026-06 curl 200 核验）

- Anthropic PDF skill: https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md
- pdfplumber: https://github.com/jsvine/pdfplumber
- pypdf: https://pypdf.readthedocs.io/en/stable/user/extract-text.html
