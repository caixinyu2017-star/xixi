# R7.22 — m12 五份 .tex 骨架编译验证记录

- 验证日期：2026-06-12
- 验证环境：本机 Windows 11；引擎 **Tectonic**（自带包管理，按需联网拉宏包/字体）；本机另有 MiKTeX pdflatex/xelatex 与 latexmk 可用。
- 命令：`tectonic --outdir <tmp> skills/light-typesetting/templates/<f>.tex`
- 结论：五份骨架**全部编译通过（exit 0）并产出 PDF**。

| 骨架 | 引擎路径 | 结果 | 产物 PDF |
|---|---|---|---|
| `ieee_bare_conf.tex` | pdflatex（默认） | exit 0 | 25.7 KiB |
| `acm_sigconf.tex` | pdflatex（默认） | exit 0 | 57.7 KiB |
| `springer_llncs.tex` | pdflatex（默认） | exit 0 | 26.9 KiB |
| `elsevier_elsarticle.tex` | pdflatex（默认） | exit 0 | 33.6 KiB |
| `ctex_chinese.tex` | XeLaTeX（ctex 触发） | exit 0 | 42.4 KiB |

## 备注
- Tectonic 首次编译会联网下载缺失宏包/字体（如 acm 的 txfonts、ctex 的中文字体、Springer 的 lm 系列），属正常；离线 CI 需预置 TeX Live/MiKTeX 对应包。
- ACM/IEEE/Springer/Elsevier 编译期有 venue 模板的常规 warning（缺 `\acmConference` 实参等占位提示），不影响出 PDF；正式投稿须按各 venue 注意事项填全著录项。
- ctex 走 XeLaTeX 是 ctex 文档类的强制要求（pdflatex 不支持中文字体），与骨架文件头注释一致。
- 本验证为"骨架可编译"的事实核验；灌入真实内容/引用后仍须按 m12 检查清单复核页数、匿名、引用收敛。
