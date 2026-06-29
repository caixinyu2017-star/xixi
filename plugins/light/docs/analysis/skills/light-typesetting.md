# light-typesetting — 深度分析与同类对标

> 源：[`skills/light-typesetting/SKILL.md`](../../../skills/light-typesetting/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：按目标 venue 官方模板做 LaTeX/Word 排版、收敛编译、扫 log 排错并导出合规 PDF/Word 的"投稿前最后一公里"排版技能。

## 核心运行逻辑
核心是"用官方模板骨架起手 → 灌内容/图/引用 → latexmk 多轮收敛编译 → precheck_log.py 扫 .log 抓错 → 对照 latex_errors.md 修 → 过检查清单出 PDF"这条 LaTeX 主链路,Word 路线作为中文学位论文/中文期刊的并行链路(docx-js 代码生成或 Pandoc md→docx)。设计哲学很明确:永远从官方 cls/.docx 骨架改而非手搓版式,强调当届模板版本(防 desk-reject)、参考文献两套体系(bibtex+.bst / biblatex+biber)不可混、gbt7714 的 langid 纪律。真实自带资产是"小而经过编译验证":5 份最小可编译 LaTeX 骨架 + 1 份 docx-js 模板 + 1 个纯标准库的 log 解析器 + 错误对照表 + 逐工具笔记。references.md 对核实不到的工具(PACSOMATIC)和本机跑不通的工具(latexdiff 缺 Perl 模块)诚实标注 GAP,可信度高。

## 关键步骤
- 1. 开工前:从 db01 确认 venue 官方模板 URL、reference_style、单双栏、页数限制,取模板优先级 官网 author kit > Overleaf gallery > CTAN,务必用当届版本
- 2. 选骨架:从 templates/ 拷对应官方骨架(IEEE/ACM/Springer/Elsevier/中文)起手,不从空文件写
- 3. 灌内容:填 title/author/abstract/keywords + 正文(m07/m08)、公式(amsmath)、三线表(booktabs)、算法、图(m11)替换 \rule{} 占位框、宽图用 figure* 跨栏
- 4. 挂引用:引用(m10)写进 refs.bib,正文 \cite,启用骨架里注释的 \bibliographystyle + \bibliography,交叉引用用 \label+\cref
- 5. 编译收敛:latexmk -pdf -interaction=nonstopmode(中文 -xelatex),自动跑够轮数+bibtex/biber;缺包 tlmgr/miktex install
- 6. precheck:python scripts/precheck_log.py file.log(--json),退出码非 0=有致命错误,按类别查 references/latex_errors.md 的症状→根因→修法表逐条修
- 7. 复核出 PDF:过导出前检查清单(编译无错/引用解析/图表位置/文献格式/页数页边距/匿名合规),交付 PDF+可编译源工程+合规核对表
- 8. Word 路线(并行):用 assets/docx_template.js 代码生成带样式/TOC/页眉页脚的 docx,或 Pandoc md→docx --reference-doc;过 references.md 的 Word checklist+22 条错误对照表

## 自带资产
- scripts/precheck_log.py:纯标准库扫 LaTeX .log,正则抓 undefined ref/cite、重复 label、overfull/underfull hbox、缺图缺文件、undefined control sequence、致命 error,按严重度汇总,致命项退出码 1,无参跑内置样例自测
- templates/ieee_bare_conf.tex:IEEEtran conference 双栏骨架,含 IEEEauthorblock、IEEEkeywords、IEEEPARstart 首字下沉、figure 占位、thebibliography/bibtex 二选一
- templates/acm_sigconf.tex:acmart sigconf 骨架,含版权/会议信息占位、CCSXML+ccsdesc、\Description 可访问性描述、ACM-Reference-Format
- templates/springer_llncs.tex:llncs runningheads 骨架,含 \inst 机构编号、titlerunning/authorrunning、orcidID、splncs04.bst
- templates/elsevier_elsarticle.tex:elsarticle preprint/review/12pt 投稿骨架,frontmatter+affiliation+cortext 通讯作者、lineno 行号、elsarticle-num
- templates/ctex_chinese.tex:ctexart XeLaTeX 中文骨架,含三线表、公式、gbt7714 注释路线
- references/latex_errors.md:5 大类(致命/警告/bibtex/中文/通用流程)症状日志→根因→修法对照表,与 precheck 配套
- references.md:逐工具(Overleaf/TeX Live/latexmk/TinyTeX/Pandoc/latexdiff/IEEEtran/acmart/llncs/elsarticle/gbt7714/MarkItDown 等)真实端点选项+已知坑,含 Word 学术排版大节(10 步 checklist+22 条错误表+中文学位论文模板纪律)
- assets/docx_template.js:docx-js 模板,含 DXA 换算表、Heading 样式+outlineLevel、TableOfContents、页眉页脚页码、A4/Letter 切换、booktabs 风格三线表
- assets/package.json+package-lock.json:固定 docx ^9.7.1 依赖

## 优点
- 五份 LaTeX 骨架全部声称经 Tectonic 编译验证退出 0(2026-06-12 留痕),不是纸上模板;骨架用 \rule{} 占位框+thebibliography 内联,保证离线零依赖即可编译出 PDF,降低首次跑通门槛
- precheck_log.py 是真有用的工程化资产:纯标准库无依赖、自带 selftest、--json 结构化输出、退出码可入 CI/闸门、正则规则表清晰可扩展,且与 latex_errors.md 形成'抓类别→查修法'闭环
- references.md 学术诚信突出:PACSOMATIC 明确标'未能核实'并建议向用户确认,latexdiff 标本机 GAP 并给依赖修复路径,不臆造功能
- 覆盖了真实 desk-reject 高频雷区:当届模板版本、双栏宽图 figure*、acmart 缺版权红框、llncs 必填 running、gbt7714 的 langid 与 [C]/[J] 标识、cleveref/hyperref 加载顺序
- Word 路线密度对齐 LaTeX,不是敷衍:22 条'现象→原因→修法'错误表覆盖中文论文最痛的样式/多级列表/域刷新/分节符/字体混排,且明确'看起来对≠结构对'这一查重送审系统的真实判定逻辑
- 衔接关系明确写出数据来源(图 m11/引用 m10/内容 m07-m08/目标 m13/版本 db09/自检 a08),在生态里定位清晰

## 缺点 / 可被质疑处
- 最高风险的 desk-reject 触发项零自动化:页数超限、双盲匿名泄漏(尤其 PDF 元数据 /Author /Title 字段、未注释的 \author、致谢/基金信息)全靠人工检查清单,而 precheck_log.py 完全不碰这些——投稿真正被拒的原因恰恰没工具兜底
- precheck 的'通过'与'可交付'语义错位:undefined reference/citation、overfull hbox 都被归为 warning,退出码 0=通过,但未定义引用对一篇投稿论文是必须修的交付阻断项;按当前逻辑一篇满是 undefined cite 的稿子能'precheck 通过',与 a08 交付闸门的期望矛盾
- docx_template.js 自身违反技能宣讲的最佳实践:正文标题用 text:'1. Introduction'/'1.1 Background' 手敲编号 + HeadingLevel,而 references.md checklist 第 3 条明确要求'多级列表绑定标题样式自动连号、手敲序号必乱'——自带模板在教它自己警告的反模式
- docx 模板缺中文支持:无 eastAsia CJK 字体配置(run 里没设东亚字体),而中文学位论文/中文期刊是 Word 路线的主要使用场景,中英文字体混排正是错误表第 6 条的痛点,模板却没示范修法
- precheck 正则未处理 TeX log 的行折行(max_print_line≈79 字符自动换行):长文件路径、长 overfull hbox 上下文会被 TeX 拆成两行,锚定 ^ 的正则(如 overfull_hbox、missing_file)会漏抓或截断详情;真实大工程 log 漏报风险实在
- SKILL 指引与骨架内容不一致:SKILL 力推 algorithm2e/algpseudocode 与 booktabs 三线表+subcaption,但 IEEE 骨架只 \usepackage{algorithmic}(旧包)却无任何算法示例、无 table 示例、无 subcaption;ctex 骨架的文献用 thebibliography 而非真正跑 gbt7714+langid,未实操技能最强调的国标纪律;无任何 biblatex+biber 可跑示例、无自带 refs.bib 样本

## 可优化点（供后续逐技能优化）
- 新增匿名/合规检查脚本:扫 PDF 元数据(/Author /Title /Producer)、检测 anonymous 模式下未注释的 \author/\thanks/致谢/基金/可识别 GitHub 链接、对照 db01 的页数上限解析 PDF 实际页数,输出双盲与页数合规报告,补上当前零自动化的 desk-reject 雷区
- 给 precheck_log.py 加 --strict 模式:把 undefined ref/cite 升级为交付阻断(退出码非 0),让 a08 闸门能据此拦截;同时在解析前先做 log de-wrap(把被 79 字符折行的连续行拼回)再跑正则,消除大工程漏报
- 重写 docx_template.js 用真正的 Word 多级列表(LevelFormat+绑定 Heading 样式自动连号)替代手敲'1./1.1',去掉编号字面量;补 eastAsia CJK 字体配置示范中英文混排;删除 topBottom(width) 里未使用的 width 死参数
- 补齐骨架与 SKILL 指引的一致性:IEEE/ACM 骨架各加一个 algorithm2e 或 algpseudocode 算法示例 + 一个 booktabs 三线表 + 一处 subcaption 子图;ctex 骨架真正接 gbt7714 并自带一份含中英文混排、每条带 langid 的 refs.bib 样本,实操国标文献纪律
- 提供 biblatex+biber 可跑变体(或在骨架里给出经验证的注释块)+ Pandoc 路线的 GB/T 7714 CSL 文件指针/自带,让现代文献体系也有起手式,而不只在 references.md 文字描述
- 把内嵌的验证日期(2026-06-11/12)与 _verification_log 引用收敛成技能内一份可复跑的 verify 脚本(latexmk/tectonic 批量编译 5 份骨架+跑 precheck selftest),让'编译验证'可被重新触发而非一次性时间戳,防止信息腐烂

## 与其他 Light 技能/知识库的衔接
上游:内容来自 m07/m08,图来自 m11(但未约定图格式契约——LaTeX 应优先矢量 PDF,建议补明确),引用来自 m10(未约定交付物是 refs.bib 还是 CSL),目标 venue 要求来自 m13/db01(template_url、reference_style、单双栏、页数限制)。下游/横向:版本入 db09;交付前过 a08(light-self-review)自检闸门——但如缺点所述,precheck 当前的退出码语义与 a08 闸门期望不完全对齐,undefined cite 类问题会漏过闸门。返修场景 latexdiff 标红与 m14(light-review-rebuttal)互引,Word tracked changes 用 OOXML w:ins/w:del 对接。整体在 Light 生态里是"内容/图/引用三流汇合后的排版导出末端节点",定位清晰但与上游的数据格式契约偏口语化、未文档化。

---

## GitHub 同类前沿技能对标

GitHub 上同类项目分三类:(1) 给 LLM/coding agent 用的 LaTeX 技能与 MCP(latex-document-skill、latex-engineer、mcp-latex-server、pdflatex-skill、ARIS 的 paper-compile),(2) 投稿前清理/校验工具(arxiv-latex-cleaner、ALC-NG、latex2arxiv),(3) Overleaf 集成 MCP 与模板环境(overleaf-mcp、PaperShell、mcp-pandoc)。Light 的 light-typesetting 最接近第一类 agent skill 形态,但独有差异化在于:把"按目标 venue 当届官方模板起手 + 收敛编译 + 扫 log 对照错误表排错 + LaTeX/Word 双链路 + gbt7714/中文学位论文"做成一条完整且对 GAP 诚实标注的中文投稿链路。社区里星标最高的要么是纯模板/纯清理工具(不管编译排错与 venue 模板版本),要么是大而全的通用 LaTeX 技能(latex-document-skill 27 模板,但偏通用文档而非投稿合规),少有项目像 light-typesetting 这样同时强调"当届模板防 desk-reject、两套参考文献体系不可混、中文 langid 纪律"这些投稿实务细节。Light 的弱点是自带资产小(5 骨架),通用文档覆盖面与 star 影响力不及头部项目。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [ndpvt-web/latex-document-skill](https://github.com/ndpvt-web/latex-document-skill) | 面向 Claude Code 的通用 LaTeX 文档技能,含 27 套模板、27 个脚本、26 份参考指南,覆盖论文/报告/简历/演示等多种文档类型 | 476 | 2026-06-11 (pushed_at) | 强:资产规模大得多(27 模板 vs Light 5 骨架),同为 SKILL.md 形态、直接对标。弱:定位是通用文档生成,不聚焦投稿合规——没有按目标 venue 当届官方模板、没有专门的 log 扫错对照表、没有 bibtex/biblatex 两体系纪律,也无中文期刊/学位论文与 gbt7714 链路 |
| [shihabshahrier/latex-engineer](https://github.com/shihabshahrier/latex-engineer) | 给 coding agent 用的 AI LaTeX 编译器与项目技能,主打编译与项目管理 | 1 | 2026-06-12 (pushed_at) | 强:同为 agent skill 且专注编译。弱:刚起步 star 极低,文档单薄,无 venue 模板库、无错误对照表沉淀、无 Word/中文链路;Light 的收敛编译+log 解析器+latex_errors.md 对照体系更成形 |
| [b1rd33/pdflatex-skill](https://github.com/b1rd33/pdflatex-skill) | 精简的 Claude Code LaTeX 技能,6 模板 9 参考,约 2K token 上下文成本,零 Python 依赖,覆盖发票/报告/简历/演示/学术论文 | 1 | 2026-03-23 (pushed_at) | 强:设计哲学与 Light 高度相似(轻量、低 token、纯标准库无重依赖)。弱:偏通用文档而非投稿,没有 venue 当届模板版本意识、没有 log 扫错排错链路、无中文/Word 路线,模板数与 Light 接近但缺投稿合规深度 |
| [wanshuiyin/Auto-claude-code-research-in-sleep (ARIS, paper-compile 技能)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 纯 Markdown 的自主 ML 科研技能集(跨模型 review、选题、实验自动化),内含 paper-compile 技能负责论文编译 | 11992 | 2026-06-11 (pushed_at) | 强:star 量级巨大、影响力高,paper-compile 嵌在完整科研自动化流水线里。弱:编译只是其大流水线的一环,排版深度远不及 Light(无 venue 模板库、无错误对照表、无 Word/中文学位论文链路);两者更多是互补关系 |
| [marswangyang/mcp-latex-server](https://github.com/marswangyang/mcp-latex-server) | 面向 LLM/AI 助手的 MCP 服务器,提供 LaTeX 文件创建、编辑、管理的工具集 | 0 | 2026-01-24 (pushed_at) | 强:MCP 形态可被任意 MCP 客户端调用,工具化粒度更细。弱:几乎无人使用、近半年未更新,无 venue 模板与投稿合规逻辑、无错误对照知识沉淀;Light 以知识+骨架取胜而非工具接口 |
| [rangehow/overleaf-mcp](https://github.com/rangehow/overleaf-mcp) | 功能最全的 Overleaf MCP 服务器,18 个工具覆盖全 CRUD、LaTeX 结构、git 历史/diff、PDF 编译与下载 | 0 | 2026-06-08 (pushed_at) | 强:深度集成 Overleaf,带 git diff/版本对比,正好补 Light 标注为 GAP 的 latexdiff 能力。弱:依赖 Overleaf 账号、无本地离线链路、无 venue 模板版本意识与投稿前 log 排错对照表;定位是云端编排而非本地排版收敛 |
| [takashiishida/arxiv-latex-mcp](https://github.com/takashiishida/arxiv-latex-mcp) | MCP 服务器,用 arxiv-to-prompt 抓取并处理 arXiv 论文的 LaTeX 源码,便于精确解析数学公式 | 135 | 2026-06-10 (pushed_at) | 强:有一定 star、专注 LaTeX 源解析,在数学公式解读上更专。弱:方向是读 arXiv 论文而非排版投稿出 PDF,与 Light 几乎正交;无模板、无编译排错、无 Word/中文链路 |
| [google-research/arxiv-latex-cleaner](https://github.com/google-research/arxiv-latex-cleaner) | Google 出品的 arXiv 投稿前 LaTeX 清理工具:删注释、去未用文件、压缩,产出可投稿的干净源码包 | 6898 | 2026-03-27 (pushed_at) | 强:star 极高、是投稿清理事实标准、稳定可靠。弱:只做投稿前清理这一窄环节,不做模板起手、不做编译、不扫 log 排错、不碰 Word/中文;是 Light 投稿链路末端可直接调用的互补工具而非竞品 |
| [COMSYS/ALC-NG](https://github.com/COMSYS/ALC-NG) | 新一代 LaTeX 投稿净化工具,剥离未用文件/注释/条件分支/元数据并保证输出 PDF 不变 | 19 | 2026-06-10 (pushed_at) | 强:比 arxiv-latex-cleaner 更现代、能验证输出 PDF 字节级不变,投稿净化更严谨。弱:同样只做净化单环节,无模板/编译/排错/Word/中文链路;可作为 Light 出包前的可选步骤 |
| [YuZh98/latex2arxiv](https://github.com/YuZh98/latex2arxiv) | 一条命令清理 LaTeX 工程、捕捉会导致 arXiv 拒收的错误并引导上传,自带 MCP 接口 | 4 | 2026-06-03 (pushed_at) | 强:理念与 Light 投稿前最后一公里最贴近——主动抓 desk-reject 级错误并引导提交,且提供 MCP。弱:只覆盖 arXiv 一个目标、不做 venue 官方模板起手、无 Word/中文学位论文链路,错误知识库规模小于 Light 的 latex_errors.md |
| [vivekVells/mcp-pandoc](https://github.com/vivekVells/mcp-pandoc) | 基于 Pandoc 的文档格式转换 MCP 服务器,支持 md/docx/pdf/latex 等互转 | 555 | 2025-09-16 (pushed_at) | 强:star 高、转换格式覆盖广,正对 Light 的 Word 并行链路(md→docx)。弱:纯格式转换、无排版收敛与 venue 合规、无中文学位论文模板与 gbt7714 纪律;可作为 Light Word 路线的底层引擎 |
| [sylvainhalle/PaperShell](https://github.com/sylvainhalle/PaperShell) | 灵活的 LaTeX 论文模板环境,提供项目骨架、构建脚本与多 venue 切换的工程化框架 | 158 | 2026-06-12 (pushed_at) | 强:成熟的工程化模板环境、构建脚本完善、可多 venue 切换。弱:是给人用的脚手架而非 agent skill,无 LLM 集成、无 log 扫错对照知识、无 Word/中文链路;Light 把同类骨架做进了可被 agent 调用的技能里 |

### Light 该技能可借鉴的点
- 资产规模:头部 latex-document-skill 有 27 套模板/脚本/参考,Light 只 5 骨架——可在保持编译验证过前提下扩充更多 venue 当届官方模板(尤其 IEEE/ACM/Springer/Elsevier 系列与中文核心期刊)
- 把 latexdiff GAP 补上:overleaf-mcp 用 git history/diff 实现版本对比,可借鉴用 git 或纯 Python diff 方案替代缺 Perl 模块的 latexdiff,把本机跑不通的 GAP 转成可用能力
- 投稿净化末端:arxiv-latex-cleaner / ALC-NG 是清理事实标准,Light 可在出包前显式调用或内置同类删注释/去未用文件/保证 PDF 不变步骤,补全投稿链路最后一步
- 主动抓 desk-reject 错误:latex2arxiv 一条命令抓拒收级错误的思路可融入 precheck_log.py,把扫 log 从被动报错升级为按 venue 规则主动预检(页数/字体嵌入/颜色模式/匿名化)
- MCP/工具接口:多个同类项目以 MCP 暴露能力,Light 可考虑把 precheck_log.py、编译收敛等核心脚本额外包一层 MCP,让非 Claude 的 agent 也能复用
- Word 链路底层:mcp-pandoc 证明 Pandoc md→docx/pdf 转换可工具化,Light 的 Word 并行链路可显式以 Pandoc 为可插拔后端并补中文模板的 reference.docx 样式管理
- 上下文成本意识:pdflatex-skill 把约 2K token、零 Python 依赖当卖点,与 Light 纯标准库 log 解析器理念一致,可在 SKILL.md 里把低 token/零重依赖显式标注为设计优势
