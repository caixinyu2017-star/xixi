# IMG-REF — 图片/图表反提与公式 OCR 参考（外部工具，纯 REF）

本文件只列外部工具与依赖，**不配套脚本**（图表反提依赖人工框选/校正，强行脚本化易得错数）。
适用：从图片/截图里把数据、公式、表格、拍摄信息"逆向"提取回结构化形式。
铁律对齐项目底线：**论文图/数据图必须程序化重绘，绝不 AI 生成**——这里只做"反提原始信息"，
反提后若要重画走 m11(light-figure-drawing)。

## 决策表（按"图里要拿什么"选工具）

| 图里有 | 要拿出 | 首选工具 | 性质 |
|--------|--------|----------|------|
| 折线图/散点图/柱状图 | 数据点坐标 | WebPlotDigitizer / PlotDigitizer | 半自动，需人工标轴 |
| 数学公式截图 | LaTeX 源码 | pix2tex(LaTeX-OCR) / Mathpix | OCR，需校对 |
| 表格截图/拍照 | CSV/DataFrame | img2table / Mathpix / PaddleOCR | OCR，需校对 |
| 一般文字截图 | 纯文本 | tesseract / PaddleOCR / EasyOCR | OCR |
| 照片/扫描件 | 拍摄/设备信息 | exiftool / Pillow ExifTags | 元数据，无需 OCR |

## 1 · 图表反提数据（chart digitization）

把发表图里的曲线/散点还原成数据点。**半自动**：人工标定坐标轴两个参考点，工具再沿曲线取点。

### WebPlotDigitizer（首选，图形界面/可本地部署）
- 在线版 https://automeris.io/WebPlotDigitizer/ ；开源仓库 https://github.com/automeris-io/WebPlotDigitizer
- 流程：导入图 → 标 X/Y 轴各两个已知刻度点 → 自动/手动沿曲线取点 → 导出 CSV。
- 支持线性/对数轴、极坐标、误差棒、地图。
- 适合：从别人论文 PDF 截出的图反提数据做对比基线（注意版权与"重绘非复制"边界）。

### PlotDigitizer
- https://plotdigitizer.com/ （在线）与桌面版；定位同 WebPlotDigitizer。
- 适合简单 2D 折线/散点的快速反提。

> 反提数据的诚实纪律：反提值是**近似重建**，标注来源图与误差量级，别当成原始精确数据；
> 能拿到原始数据就别反提（先问作者/查附录/补充材料）。

## 2 · 公式 OCR（公式截图 → LaTeX）

### pix2tex / LaTeX-OCR（开源，可离线）
- 仓库 https://github.com/lukas-blecher/LaTeX-OCR
- 依赖：`pip install pix2tex`（拉 PyTorch 模型，首次会下载权重——离线环境需预置）。
- 用法（CLI）：`pix2tex path/to/formula.png` 输出 LaTeX；也有 GUI `latexocr`。
- 适合：单个公式截图；复杂多行公式需人工校对。

### Mathpix（商业 API，精度高）
- https://mathpix.com/ ；`mpx` CLI 或 REST API（需 API key，**付费**，按调用计费）。
- 支持公式+表格+手写；输出 LaTeX / MathML / Markdown。
- 适合：批量、高精度、含手写；**费用门槛**——用前确认配额与单价。

## 3 · 表格截图 → CSV

| 工具 | 性质 | 备注 |
|------|------|------|
| img2table | 开源 Python | `pip install img2table`，配 tesseract/PaddleOCR 后端，输出 DataFrame/xlsx |
| Mathpix | 商业 API | 表格识别强，付费 |
| PaddleOCR PP-Structure | 开源 | 版面分析+表格还原，依赖 paddlepaddle |
| camelot / tabula | 开源 | 仅适用于**矢量 PDF 里的表**，不吃纯图（图走上面三者） |

- img2table 最小依赖路线：`pip install img2table[paddle]` 或 `[tesseract]`；
  tesseract 需另装系统二进制（Windows 下装 UB-Mannheim 版并配 PATH）。
- 表格 OCR 几乎都需人工校对合并单元格/数字 0-O 混淆。

## 4 · EXIF / 图片元数据（无需 OCR）

读拍摄设备、时间、GPS、分辨率——判断图来源、是否被编辑、拍摄条件。

### exiftool（外部二进制，最全）
- https://exiftool.org/ ；命令：`exiftool photo.jpg`（列全部标签），`exiftool -gps:all photo.jpg`。
- Windows 装 standalone exe 配 PATH；最权威，支持几乎所有相机/格式。

### Pillow（纯 Python，轻量够用）
- `pip install Pillow`；读基本 EXIF：

```python
from PIL import Image
from PIL.ExifTags import TAGS
img = Image.open("photo.jpg")
exif = img.getexif()
for tag_id, value in exif.items():
    print(TAGS.get(tag_id, tag_id), "=", value)
```

> 隐私提醒：EXIF 常含 GPS/设备序列号等敏感信息。分享图前考虑用 `exiftool -all= img.jpg` 清除；
> 处理他人图片时按 key 名引用敏感字段、不回显具体值（CONVENTIONS §5 / a10）。

## 外部依赖一览（装前确认）

| 工具 | 安装 | 联网/费用 | 离线可用 |
|------|------|-----------|----------|
| WebPlotDigitizer | 在线 / 本地部署 | 在线版需网；可自托管 | 自托管后可 |
| PlotDigitizer | 在线 / 桌面 | 在线需网 | 桌面版可 |
| pix2tex | `pip install pix2tex` | 首次下模型权重 | 预置权重后可 |
| Mathpix | API key | **付费**、需网 | 否 |
| img2table | `pip install img2table` + OCR 后端 | OCR 后端本地 | 可 |
| PaddleOCR | `pip install paddleocr paddlepaddle` | 首次下模型 | 预置后可 |
| tesseract | 系统二进制 | 本地 | 可 |
| exiftool | 系统二进制 | 本地 | 可 |
| Pillow | `pip install Pillow` | 本地 | 可 |

## 衔接

- 反提得到的数据/公式/表格 → 填入 `templates/understanding-note.md` 的「可复用内容」。
- 要把反提数据重新画成图 → 走 m11(light-figure-drawing)，**程序化重绘，绝不 AI 生成**。
- 反提的引用/文献信息 → m10(citation) 核验。
