# LaTeX 常见编译错误对照表（症状日志 → 根因 → 修法）

配合 `scripts/precheck_log.py` 使用：先跑 precheck 抓出问题类别，再来此表查根因与修法。
错误日志里 `! ` 开头是致命错误（编译中断），`LaTeX Warning:` 是警告（PDF 仍生成但可能不正确）。

## 致命错误（`!` 开头，编译停止）

| 症状（日志行） | 根因 | 修法 |
|---|---|---|
| `! Undefined control sequence.` 后跟 `l.NN \somecmd` | 命令拼错，或所属宏包未 `\usepackage` | 检查拼写；补 `\usepackage{对应包}`。如 `\includegraphics` 需 `graphicx`，`\toprule` 需 `booktabs` |
| `! LaTeX Error: File 'xxx.sty' not found.` | 宏包未安装 | TeX Live: `tlmgr install xxx`；MiKTeX 默认弹窗自动装；TinyTeX: `tinytex::tlmgr_install("xxx")` |
| `! LaTeX Error: File 'fig.png' not found.` | 图片路径错/文件不存在/扩展名不符 | 确认文件存在；`\graphicspath{{figs/}}`；pdfLaTeX 支持 pdf/png/jpg，不支持 eps（需 epstopdf 或改 xelatex） |
| `! Missing $ inserted.` | 数学符号（`_` `^` `\alpha`）出现在文本模式 | 包进 `$...$` 或 `\(...\)`；下划线文本用 `\_` |
| `! Missing } inserted.` / `! Too many }` | 花括号不配对 | 检查最近改动处括号；编辑器括号匹配高亮 |
| `! Runaway argument?` | 命令参数缺右括号，或段落中断了不该断的命令 | 找未闭合的 `{`；脆弱命令前加 `\protect` |
| `! Paragraph ended before \xxx was complete.` | 在不接受空行的命令参数里出现了空行 | 删除参数内空行，或命令定义加 `\long` |
| `! LaTeX Error: \begin{xxx} on input line N ended by \end{yyy}.` | 环境 begin/end 不匹配 | 对齐 `\begin`/`\end` 名称与嵌套 |
| `! LaTeX Error: Something's wrong--perhaps a missing \item.` | list/thebibliography 里缺 `\item`/`\bibitem` | 补 `\item`；检查 `description` 等环境 |
| `! Emergency stop.` / `! ==> Fatal error occurred` | 前面有未恢复的错误累积 | 看第一个 `!` 错误，从最早的修起 |
| `! Package inputenc Error: Unicode character ... not set up` | pdfLaTeX 遇到非 ASCII/中文字符 | 改用 XeLaTeX/LuaLaTeX；中文用 `ctex` + `-xelatex` |
| `! Dimension too large.` / `! TeX capacity exceeded` | 图过大/递归/表太宽 | 缩放图片；检查无限递归宏；大表用 `longtable`/`adjustbox` |
| `! Double superscript.` | 出现 `x^2^3` 这类连续上标 | 加括号 `x^{2^3}` |

## 警告（`LaTeX Warning:`，PDF 生成但需修）

| 症状 | 根因 | 修法 |
|---|---|---|
| `Reference 'xxx' on page N undefined` | `\ref` 找不到 `\label`，或编译轮数不够 | 确认 `\label` 存在且拼写一致；多编一轮（latexmk 自动收敛） |
| `Citation 'xxx' on page N undefined` | `\cite` 的 key 不在 .bib，或没跑 bibtex/biber | 用 `latexmk`（自动跑 bibtex）；检查 .bib 里 key；biblatex 用 biber 不是 bibtex |
| `There were undefined references.` | 上述两类汇总 | 同上，跑够轮数 + bibtex/biber |
| `Label(s) may have changed. Rerun to get cross-references right.` | 引用/页码/目录未收敛 | 再编一轮；用 latexmk 免手动 |
| `Label 'xxx' multiply defined.` | 两个 `\label` 同名 | 改成唯一 label（如 `fig:a`/`fig:b`） |
| `Overfull \hbox (N pt too wide)` | 行内容超出文本宽度（长单词/URL/宽公式/宽表） | URL 用 `\url{}`(url/hyperref)；长词加连字符；表用 `\resizebox`/`tabularx`；公式拆行 `split`/`multline` |
| `Underfull \hbox (badness N)` | 行被拉得过稀（常因强制换行/窄栏） | 多为美观问题；可忽略小 badness；避免无谓 `\\` |
| `Underfull \vbox` / `Overfull \vbox` | 竖向空间过松/过满 | 调整图表浮动位置 `[t]/[h]`；`\enlargethispage` |
| `Font shape 'xxx' undefined` | 请求的字形（如粗体小型大写）该字体没有 | 换字体或字形；忽略（会替代为最近字形） |
| `Package hyperref Warning: Token not allowed in a PDF string` | 章节标题/书签里有数学或命令 | 用 `\texorpdfstring{数学}{纯文本}` 提供书签替代文本 |

## bibtex / biber 相关

| 症状 | 根因 | 修法 |
|---|---|---|
| `I couldn't open database file refs.bib` | .bib 路径错/文件名错 | `\bibliography{refs}` 不带 .bib 扩展名；确认文件同目录 |
| `I found no \citation commands` | 正文没 `\cite` 或 .aux 未更新 | 先 pdflatex 生成 .aux 再 bibtex；用 latexmk 顺序自动对 |
| biblatex `Package biblatex Warning: File 'xxx.bbl' is wrong format` | 用 bibtex 跑了 biber 工程（或反之） | biblatex+`backend=biber` 必须跑 biber；删旧 .bbl 重来 |
| 参考文献空白/不出现 | 漏 `\bibliographystyle` 或没跑 bibtex | 补 `\bibliographystyle{...}` + `\bibliography{...}`；跑 bibtex |

## 中文 / CJK 相关

| 症状 | 根因 | 修法 |
|---|---|---|
| pdfLaTeX 下中文报 `Unicode character not set up` | pdfLaTeX 不支持 CJK | 改 `latexmk -xelatex`；文档类用 `ctexart` 或 `\usepackage{ctex}` |
| XeLaTeX 中文变方块/缺字 | 系统缺中文字体 | 装 fandol/思源/Noto CJK；`\setCJKmainfont{SimSun}` 指定已装字体 |
| gbt7714 文献「等」/「et al.」错乱或缺 `[J]/[C]` | 条目缺 `langid`/`language` 字段 | 每条 .bib 加 `langid={chinese}` 或 `{english}`；用正确 entry type |

## 排错通用流程

1. 跑 `python scripts/precheck_log.py file.log` 抓类别与行号。
2. 永远从**第一个** `!` 错误修起（后续错误常是连锁反应）。
3. 缺包/未定义引用类：用 `latexmk` 重编（自动跑够轮数 + bibtex/biber）。
4. 缺宏包：`tlmgr install`（TeX Live）/ MiKTeX 自动装 / `tinytex::tlmgr_install`。
5. 中文/特殊字体：换 `-xelatex` 或 `-lualatex`。
6. 顽固中间文件污染：`latexmk -C` 全清后重编。
