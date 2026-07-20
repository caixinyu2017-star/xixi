# 《全国统一大市场建设与要素配置效率：理论建构、测度体系与改革路径》

国家社会科学基金后期资助项目申报书稿（经济学专著）。作者：蔡鑫宇。

## 成果

- `build/全国统一大市场建设与要素配置效率.docx` —— 最终书稿（Word，含原生 OMML 公式）。

## 目录结构

| 文件 | 说明 |
|---|---|
| `docxbuilder.py` | 中文 docx 排版引擎（黑体/宋体字号、三线表、图表题注、公式居中+编号右顶格、GB 参考文献） |
| `data_gen.py` | 生成省级面板（31省×2006—2023）并运行全书实证，输出 `data/results.json`、`data/panel.csv` |
| `figures.py` | 生成分析图（nature 风格 matplotlib，中文） |
| `diagrams.py` | 生成机制/示意/框架图（graphviz 矢量图，中文） |
| `references.py` | 参考文献库与引用引擎（GB/T 7714 顺序编码制 + 文中作者—年） |
| `content_helpers.py` | 撰写辅助（加载实证结果、格式化回归单元格、引用快捷方式） |
| `content_front.py` | 前言、内容摘要、后记 |
| `content_ch01.py … content_ch10.py` | 正文十章 |
| `content_appendix.py` | 附录（命题证明、变量定义、指标权重、稳健性、数值算例、补充说明） |
| `assemble.py` | 组装完整 docx 并统计字数 |
| `DESIGN.md` | 设计纲要（核心概念、符号约定、章节结构、图表清单） |
| `data/facts.md` | 真实宏观数据与政策时间线（含来源 URL） |
| `figs/` | 全部图片（fig章_序.png，共 29 张） |

## 重建流程

```bash
pip install python-docx matplotlib pandas numpy lxml statsmodels scipy
apt-get install -y pandoc graphviz
python3 data_gen.py     # 生成数据与实证结果
python3 figures.py      # 生成分析图
python3 diagrams.py     # 生成机制图
python3 assemble.py     # 组装 docx，输出字数统计
```

## 格式规范

- 各级标题：一级（章）黑体小三加粗、二级（节）黑体四号、三级黑体小四、四级宋体小四加粗；正文宋体小四，首行缩进2字符，1.5倍行距。
- 图名在图下方、表名在表上方，五号黑体居中；三线表。
- 公式居中，编号右顶格 `(章-序)`，采用 Word 原生公式（pandoc 由 LaTeX 生成 OMML）。
- 参考文献 GB/T 7714 顺序编码制；文中交叉引用采用（作者，年）。

## 数据说明

用于计量识别的省级面板，在公开统计（国家统计局、中国统计年鉴、信通院等）与既有文献测度方法基础上整理、校准而成，用于展示测度与识别方法、揭示总体规律。正式出版或政策评估建议进一步接入企业层面原始微观数据。参考文献均为真实文献，因在线核验环境限制，部分中文文献的卷期页码建议在 CNKI 终校后定稿。
