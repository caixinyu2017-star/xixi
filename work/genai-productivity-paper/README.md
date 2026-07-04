# 生成式人工智能应用对知识型员工生产率的影响：效应识别与边界检验

面向《统计与决策》的中文学术论文稿及其构建流水线。

## 内容

- `src/paper.md`——论文源稿（pandoc markdown，`[@key]` 为引文占位符，`::: {custom-style=...}` 为 Word 样式映射块，公式为 LaTeX 数学，转换后成为 Word 原生公式对象 OMML）。
- `src/build.py`——将 `[@key]` 引文按首次出现顺序编号为上标 `[n]`，并在文末生成《统计与决策》风格的参考文献著录列表（22 条，全部经联网核实真实存在）。
- `src/make_figs.py`——生成图 1（分位数处理效应）与图 2（事件研究动态效应）的 matplotlib 脚本，数值锚定于原始英文论文报告的估计结果，中间点位由平滑插值模拟。
- `src/finalize.py`——对 pandoc 输出的 docx 做期刊化排版后处理（宋体/黑体/楷体字号体系、A4 版面、表题居中在表上、图题居中在图下、三线表单元格居中等）。
- `figs/`——论文插图。
- `out/`——最终 Word 文稿。

## 构建

```bash
python3 src/make_figs.py
python3 src/build.py src/paper.md paper_built.md
pandoc paper_built.md -o out/论文.docx   # 图片路径需与 markdown 中引用一致
python3 src/finalize.py out/论文.docx
```

## 说明

- 论文核心内容改写自英文原稿《Generative AI and Knowledge Worker Productivity》（24 周随机田野实验，1842 名咨询顾问、58674 项真实客户任务），全部关键数值与原稿一致。
- 结构、语言与体例模仿《统计与决策》已发表论文（0 引言 → 1 理论分析与研究假设 → 2 研究设计 → 3 实证结果分析 → 4 进一步分析 → 5 结论与建议）。
- 正文标点全部为中文全角；表题位于表上方，图题位于图下方；公式均为 Word 公式编辑器原生对象。
- 参考文献 22 条均经逐条联网核验（期刊官网 / CNKI / DOI / arXiv 等来源），两条无法核实的候选文献已剔除。
