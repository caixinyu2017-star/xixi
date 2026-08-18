# 专著章节撰写规范（供撰写代理严格遵守）

**书名**：《标准词元与智能经济——Token的价值计量、定价机制与配置效率研究》 作者：蔡鑫宇
你的任务：撰写指定章节的 `content_chNN.py`，定义 `def blocks():` 返回 block 字典列表。

## 必读文件（用 Read 工具先读，全部在 token-econ-book/ 目录）
- `DESIGN.md`：核心概念、符号约定、你所在章的内容要点与图表清单（**必须与之一致**）。
- `../ai-talent-book/content_ch07.py`：格式与文风样板（模仿其密度、学术性、推导衔接；主题不同勿抄内容）。
- `content_helpers.py`：可用辅助（c, cc, R, F, cell, coef, pct 等）。
- `data/refkeys.txt`：**唯一允许使用的参考文献 key 列表**。
- `data/facts.md`：已核实的真实宏观数据与政策时间线（宏观数字只能取自这里）。
- `data/results.json`：全部模型估计/模拟结果（经 `content_helpers.R` 访问；模型数字只能取自这里，键结构见 data/RESULTS_SPEC.md）。
- `data/figures_manifest.md`：你章节分配到的图（文件名、图名、note 要点）。

## 硬性要求
1. **字数**：本章正文中文字数（含标点）不少于分配目标。宁多勿少；充实有据，严禁注水。
2. **文风**：中文经济学/教育经济学专著风格（《经济研究》《教育研究》《中国工业经济》水准）；观点—证据—文献三位一体；全部中文全角标点；数字与英文字母半角。
3. **引用**：`c('key')`→（作者，年）；多篇 `cc('k1','k2')`（自动按年份升序）；句法嵌入 `c('key', paren=False)`。**只能用 refkeys.txt 中的 key**；本章 ≥14 个不同 key（第2、3、4、10 章 ≥18 个）。
4. **数字纪律**：宏观事实取 `data/facts.md`；模型数字经 `R[...]` 取自 results.json 并用 f-string 格式化，**不得手写编造**。
5. **公式**：显示公式 `{'eq': r'<LaTeX>', 'num': 'N-序'}`（章内从 1 连续）；行内 `$...$`。LaTeX 用 pandoc 可解析的 amsmath 子集（**禁用 \begin{aligned} 与 \text{中文}**）。推导完整：设定→求解/估计→性质→经济含义，公式间文字衔接。
6. **图**：`{'fig': 'figs/figN_M.png', 'caption': '图N.M  中文图名', 'width_cm': 13.5, 'note': ...（可选）}`。注（若有）排在图题下方、小五宋体、无缩进、两端对齐，与表注同格式；注文严禁写进图片内部。只能用 manifest 分配给本章的图；正文必须先提及“如图N.M所示”，图块紧随该段之后，且图后有解读。
7. **表**：`{'table': {'caption': '表N.M  中文表名', 'header': [...], 'rows': [[...]], 'note': ...（可选）, 'col_align': ['left','center',...]}}`。表名在上；估计表数值从 R 取（cell/coef 格式化）；每表正文先提及后出现、并有解读。
7b. **图表注的取舍原则（按学术惯例，宁缺勿滥）**：注只承载**正文无法承载、读者读图读表时必需**的元信息，**凡正文已交代的内容一律不再设注**。
   - **应当设注**：①数据来源／资料来源（凡承载数据的分析图与数据表必标）；②统计口径、样本范围、时间窗、单位、基期、匿名化处理等测量性说明；③显著性标记与标准误含义、样本量N、控制变量；④图中缩写或简称与正文名称的对应；⑤读图必需的符号约定与图例（如因果回路图的＋／－／R／B／∥、存量—流量图的图形语义）；⑥参数取值出处与复现信息（如“其余参数取表N.M基准值”“步长0.1、窗口60期”）。
   - **不应设注**：①复述图中要素、层次与箭头关系（正文已逐一解释）；②复述正文刚给出的结论、数值或机理；③作者自绘的纯概念框架图／流程图／结构图，若正文已完整解释其构造且无需符号说明，则**整条注删除**，不必补写“资料来源：作者绘制”；④仅为凑格式而写的空泛说明。
   - 注文务求简洁，一般不超过两三句；多条信息以分号连缀，末句为来源。
8. **排版铁律**：先文后图/表；图表编号严格按出现顺序（图N.1、图N.2…）；标题层级 `{'h1': '第N章  标题'}`（唯一，块列表第一个）、`{'h2': 'N.1  …'}`、`{'h3': 'N.1.1  …'}`；每章末设“N.x 本章小结”（≥600 字）。
9. **段落**：`{'p': '…'}`；无缩进说明段 `{'lead': '其中，…'}`；少用 `{'items': [...]}`。
10. 文件顶部 `# -*- coding: utf-8 -*-` 与 `from content_helpers import c, cc, R, F, cell, coef, pct`，除 import 与 `def blocks():` 外无执行代码。

## 自检（必须通过后才能结束）
```bash
cd /home/user/xixi/token-econ-book && python3 -c "
import content_chNN as m, references, docxbuilder
references.reset(); b=m.blocks()
print('chars', docxbuilder.count_chars(b), 'blocks', len(b), 'refs', references.n_used())
figs=[x for x in b if 'fig' in x]; tabs=[x for x in b if 'table' in x]
notes=[x.get('note') for x in figs]+[x['table'].get('note') for x in tabs]
assert all(n.startswith('注：') for n in notes if n), '注文须以“注：”开头'
print('有注', sum(1 for n in notes if n), '/', len(notes))
from docxbuilder import collect_math, latex_batch_to_omml
latex_batch_to_omml(list(dict.fromkeys(collect_math(b))), 'build/eqchk_NN')
print('math ok; figs', len(figs), 'tables', len(tabs))"
```
要求：无报错、字数达标、引用数达标、公式全部可转换、图表注齐全。最终仅简要汇报：字数、块数、引用数、公式数、图表数。
