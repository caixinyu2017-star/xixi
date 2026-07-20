# 专著章节撰写规范（供撰写代理严格遵守）

**书名**：《全国统一大市场建设与要素配置效率：理论建构、测度体系与改革路径》 作者：蔡鑫宇
你的任务：撰写指定章节的 `content_chNN.py`，返回一个 `blocks()` 函数（见模板 `content_ch01.py`）。

## 必读文件（用 Read 工具先读）
- `content_ch01.py`：格式与文风模板（务必模仿其密度、学术性、段落长度）。
- `content_helpers.py`：可用的辅助（c, cc, R, cell, coef, t_of, se_of, sig, pct, star 及常量）。
- `DESIGN.md`：核心概念、符号约定、章节结构（务必与之一致）。
- `data/refkeys.txt`：**唯一允许使用的参考文献 key 列表**（key = 文中引用串）。
- `data/facts.md`：真实宏观数据与政策时间线（引用真实数字）。
- `data/results.json`：全部实证结果（回归系数、指数序列等），通过 `content_helpers.R` 访问。

## 硬性要求
1. **字数**：本章正文中文字数（含标点）**不少于 15000 字**。宁多勿少。段落要充实、有分析、有数据、有文献对话，避免空话套话。
2. **文风**：中文经济学顶刊（《经济研究》《管理世界》《中国工业经济》）专著风格；论证严密、逻辑清晰、术语准确；多用数据与文献支撑判断。
3. **引用**：文中引用一律用 `c('key')`→（作者，年）或 `cc('k1','k2')`→（作者1，年；作者2，年）。**只能使用 refkeys.txt 中存在的 key**；严禁杜撰 key 或文献。本章至少自然引用 12 篇以上文献。
4. **数字**：所有实证数字必须来自 `content_helpers.R`（即 results.json），用 `cell()/coef()/t_of()` 等格式化，**不得手写编造回归系数**。宏观事实数字取自 facts.md 并标注来源。
5. **公式**：需要时用块 `{'eq': r'LaTeX', 'num': 'N-〔序〕'}`（如 `'num': '4-1'`），行内公式用 `$...$`。LaTeX 必须 pandoc 可解析（标准 amsmath）。变量符号遵循 DESIGN.md。
6. **图**：用块 `{'fig': 'figs/figX_Y.png', 'caption': '图X.Y  中文图名', 'width_cm': 13.0}`。仅可引用你被分配的图（见各章提示）。图名格式"图章.序  名称"。
7. **表**：用块 `{'table': {'caption': '表X.Y  中文表名', 'header': [...], 'rows': [[...]], 'note': '注：...', 'col_align': [...]}}`。表名格式"表章.序  名称"。回归表数值用 `cell(R[...])`。
8. **标题层级**：`{'h1': '第N章  标题'}`（每章唯一，开头）、`{'h2': 'N.1  ...'}`、`{'h3': 'N.1.1  ...'}`、`{'h4': '...'}`。
9. **正文段落**：`{'p': '...'}`；无缩进说明段（如 where/其中）用 `{'lead': '其中，...'}`。要点列举可用 `{'items': ['...','...']}`。
10. 只输出**一个** `content_chNN.py` 文件，文件顶部 `from content_helpers import c, cc, R, cell, coef, t_of, se_of, sig, pct`，定义 `def blocks():` 返回 block 列表。不要写 `if __name__` 之外的执行代码。

## 交付
写好 `content_chNN.py` 后，运行 `python3 -c "import content_chNN as m, references as R; from docxbuilder import count_chars; R.reset(); b=m.blocks(); print('chars',count_chars(b),'blocks',len(b))"` 自检可导入且字数达标（≥15000），修正所有报错后再结束。最终简要汇报字数与引用数。
