# PPTX-REF — PowerPoint 深度读取参考（copy-paste ready）

读 PPTX 以**文本抽取 + 渲染成图视觉理解**为主线。无配套脚本（读取靠 markitdown CLI
+ LibreOffice 渲染），但视觉理解流程是核心，编辑/创建请回到 Anthropic PPTX skill。

## 决策表

| 任务 | 首选 | 说明 |
|------|------|------|
| 抽文本 | markitdown | `python -m markitdown deck.pptx` |
| 视觉理解（版式/配色/层级） | soffice 转 PDF + pdftoppm 转图 | 喂视觉模型逐页看 |
| 查残留占位符 | markitdown + grep | lorem/ipsum/xxxx |
| 读裸 XML | 解包 | `scripts/office/unpack.py` |
| 编辑/套模板/从零建 | Anthropic PPTX skill | pptxgenjs / 三步流，不在本读取技能内 |

## 抽文本

```bash
python -m markitdown presentation.pptx          # 输出 markdown 文本
pip install "markitdown[pptx]"                   # 依赖
```

## 渲染成图做视觉理解（核心）

```bash
# 1. 转 PDF（LibreOffice headless）
soffice --headless --convert-to pdf presentation.pptx
# 2. PDF 逐页转 jpg（poppler）
pdftoppm -jpeg -r 150 presentation.pdf slide
# 生成 slide-01.jpg, slide-02.jpg ...，逐页喂视觉模型理解
```

逐页学：版式类型、配色（主/辅/强调比例）、字号层级（标题 36-44pt / 正文 14-16pt /
注释 10-12pt）、留白、深浅"三明治"结构（深色用于标题+结论，浅色用于正文）。

## 查残留占位符（内容 QA）

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
# 有命中就是模板没填干净
```

## 读裸 XML（深结构）

```bash
python scripts/office/unpack.py presentation.pptx unpacked/
# 看 unpacked/ppt/slides/slide1.xml 等
```

## 视觉风格提取要点（供下游 PPT/前端/图表复用）

- 配色：识别一个主导色（60-70% 视觉权重）+ 1-2 辅色 + 1 强调色，别等权。
- 视觉母题：圆角图框 / 彩圈图标 / 单侧粗边——是否贯穿每页。
- AI 痕迹（提取时也要识别）：标题下强调线、每页同版式、纯文字页、默认蓝。

## 已知坑

- markitdown 输出供文本分析、**非高保真人读**；图像内容需接 LLM vision 才描述。
- 首次渲染几乎必有视觉问题（重叠/溢出/低对比）——理解时按"找 bug"心态逐页核。
- 转图依赖 LibreOffice + poppler；渲染图看完即删，勿留库内。

## 链接（2026-06 curl 200 核验）

- Anthropic PPTX skill: https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md
- MarkItDown: https://github.com/microsoft/markitdown
