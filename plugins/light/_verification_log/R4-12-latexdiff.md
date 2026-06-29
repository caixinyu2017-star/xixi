# R4.12 latexdiff 返修标红 — 本机实测留痕（部分 GAP）

- 研究日期：2026-06-11
- 执行：Claude Opus 4.8（Claude Code）
- 任务：light-typesetting references 增 latexdiff 流程；与 light-review-rebuttal tracked changes 互引。

## 本机实测结果

- **latexdiff/latexdiff-vc/pdflatex 均已安装**（MiKTeX，路径
  `C:/Users/Light/AppData/Local/Programs/MiKTeX/miktex/bin/x64/`）。
- **但 latexdiff 无法运行**：`latexdiff --version` 及实际 diff 调用均报
  `Can't locate Algorithm/Diff.pm in @INC (you may need to install the Algorithm::Diff module)`
  ——MiKTeX 自带的 latexdiff 是 Perl 脚本，依赖 Perl 模块 `Algorithm::Diff`，本机 Perl 环境
  缺该模块，且本机无 `perl`/`cpan`/`cpanm`（系统级），无法即时补装。
- **GAP**：latexdiff 实际 diff 输出（DIFadd/DIFdel 标记）本机未跑通，标 GAP：
  待安装 Perl + `cpan Algorithm::Diff`（或用 TeX Live 自带完整 Perl 的环境）后复测。

## 已造测试样例（命令本身正确，仅因缺 Perl 模块未出结果）
- old.tex / new.tex 两版小文档（goat behavior recognition，改了措辞+数值）。
- 命令 `latexdiff old.tex new.tex > diff.tex` 语法正确，因 BEGIN 阶段加载 Algorithm::Diff 失败而中止。
- 临时文件已清理，未留产物。

## 写入 references 的口径
- latexdiff 命令/流程是确凿公开知识，照写**方法流程**，但明确标注"本机因缺 Perl 模块
  Algorithm::Diff 未跑通输出，命令未经本机验证产出，使用前确认 Perl 环境"。不冒充实测通过。
- 关键流程要点（公开文档）：
  - 基本：`latexdiff old.tex new.tex > diff.tex`，编译 diff.tex 得标红（新增下划线、删除删除线）。
  - 多文件项目：`--flatten` 展开 `\input`/`\include` 后再 diff。
  - 与 git 配合：`latexdiff-vc --git -r <旧tag> main.tex`（或 `latexdiff-vc -r REV1 -r REV2`）。
  - 中文/复杂公式炸点：中文宏包（ctex/xeCJK）或复杂公式环境易使标记破坏编译，降级
    `--math-markup=0`（公式整体当一块，不逐符号标）、`--encoding=utf8`；必要时 `--type=CFONT`。
- 依赖提醒：latexdiff 是 Perl 脚本，需 Perl + Algorithm::Diff（MiKTeX 环境可能缺，TeX Live 通常自带）。

## 双向互引
- light-typesetting 该节 ← → light-review-rebuttal：返修要"tracked changes/标红改前改后"，
  latexdiff 是 LaTeX 项目生成 tracked changes 的标准工具。两处互相指认（堵单向挂载）。
