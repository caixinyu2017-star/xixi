# DOCX-REF — Word 深度读取参考（copy-paste ready）

配套脚本：`scripts/docx_read.py`（已自检：paragraphs/headings/runs/tables/layout）。
读用 python-docx 或 pandoc；**改原文/修订/批注**走裸 XML 三步流（python-docx 不读修订、不渲染）。

## 决策表

| 任务 | 首选 | 说明 |
|------|------|------|
| 读章节骨架/样式 | python-docx | 遍历 paragraphs→runs |
| 读表格 | python-docx | `doc.tables` |
| 读页边距/纸张（模板规范） | python-docx | `doc.sections` |
| 读修订/批注 | pandoc | `--track-changes=all`，python-docx 读不到 |
| 归一为 md 喂 LLM | pandoc / markitdown | `pandoc in.docx -o out.md` |
| 精确改原文 + redline | 解包→改 XML→重打包 | 见底部三步流 |
| .doc→.docx / 转图 | LibreOffice soffice | |

## 读章节骨架（python-docx）

```python
from docx import Document
doc = Document("paper.docx")
for p in doc.paragraphs:
    if p.text.strip():
        print(f"[{p.style.name}] {p.text}")
```

## 读 run 级样式（提取格式要求）

```python
from docx import Document
doc = Document("paper.docx")
for i, p in enumerate(doc.paragraphs):
    for r in p.runs:
        if not r.text:
            continue
        sz = r.font.size
        print(i, repr(r.text), "bold" if r.bold else "",
              "italic" if r.italic else "",
              sz.pt if sz else "", r.font.name)
```

## 读表格

```python
from docx import Document
doc = Document("data.docx")
for t in doc.tables:
    for row in t.rows:
        print([c.text for c in row.cells])
```

## 读页边距 / 纸张（模板规范）

```python
from docx import Document
doc = Document("template.docx")
for s in doc.sections:
    print("page", s.page_width.inches, "x", s.page_height.inches, "in")
    print("margins T/B/L/R:",
          s.top_margin.inches, s.bottom_margin.inches,
          s.left_margin.inches, s.right_margin.inches)
```

## 读修订 / 批注（pandoc，python-docx 做不到）

```bash
# 把增删/批注包成 insertion/deletion/comment span，保留作者+时间
pandoc --track-changes=all document.docx -o out.md
pandoc --track-changes=accept document.docx -o accepted.md   # 接受全部
pandoc --track-changes=reject document.docx -o rejected.md   # 拒绝全部
pandoc --extract-media=./media document.docx -o out.md       # 同时导出内嵌图
```

## 精确改原文 + 修订标记（解包→改 XML→重打包三步流）

python-docx 无法写修订；用 Anthropic DOCX skill 的裸 XML 路线：

1. 解包：`python scripts/office/unpack.py document.docx unpacked/`
2. 用 Edit 直接改 `unpacked/word/document.xml`（不要写 Python 脚本改 XML）
3. 重打包：`python scripts/office/pack.py unpacked/ out.docx --original document.docx`

插入（替换整个 `<w:r>` 块为 ins/del 兄弟节点，勿塞进 run 内）：
```xml
<w:ins w:id="1" w:author="Claude" w:date="2026-06-06T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

删除（`<w:del>` 内用 `<w:delText>`，不是 `<w:t>`）：
```xml
<w:del w:id="2" w:author="Claude" w:date="2026-06-06T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

删整段：把段落标记也标删，否则接受后留空段：
```xml
<w:pPr><w:rPr>
  <w:del w:id="1" w:author="Claude" w:date="2026-06-06T00:00:00Z"/>
</w:rPr></w:pPr>
```

批注的 `<w:commentRangeStart/End>` 必须是 `<w:r>` 的兄弟节点。

## 已知坑

- python-docx **不读修订、不读批注、不渲染 PDF/图**，复杂格式无完整往返保真。
- pandoc 转换天然有损（AST 比源弱），页边距等精确格式不保；`--track-changes` 仅 docx reader 有效。
- 最小化修订：只标真正变动的词，别整段重写。

## 链接（2026-06 curl 200 核验）

- Anthropic DOCX skill: https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md
- python-docx: https://python-docx.readthedocs.io/en/latest/
- Pandoc: https://pandoc.org/MANUAL.html
