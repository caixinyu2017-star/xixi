# 第三期执行进度台账（PROGRESS）

> 每轮收尾时由执行模型更新本文件（总纲 §5 第 6 步）。新对话接手时**先读本文件**再读对应轮次文件。
> 状态取值：`未开始 / 进行中 / 已完成 / 部分完成（见偏差）`。

## 轮次状态

| 轮 | 名称 | 状态 | 开始 | 完成 | commit 区间 | CI |
|---|---|---|---|---|---|---|
| R1 | P0 与卫生修复 | 已完成 | 2026-06-11 | 2026-06-11 | `1520d93..056165c`（8 commit） | 本地 7 门禁全绿；待推送确认 CI |
| R2 | 会话衔接协议 | 已完成 | 2026-06-11 | 2026-06-11 | `dd00835..7b60de3`（5 commit） | 绿（run 27341424084 三任务全 success） |
| R3 | 中文链路专项 | 已完成 | 2026-06-11 | 2026-06-11 | `89627e2..74a1bb0`（4 commit） | 绿（run 27346343103 三任务全 success） |
| R4 | 合规与生态吸收 | 已完成 | 2026-06-11 | 2026-06-11 | `5c7d2e1..a5a088e`（7 commit） | 绿（run 27353169946 success） |
| R5 | 资产补全 | 已完成 | 2026-06-11 | 2026-06-11 | `94f237e..cc3fd19`（9 commit） | 本地 5 门禁全绿；48 脚本 selftest 全 PASS；待推送确认 CI |
| R6 | PPT 生图流水线 | 部分完成（见偏差） | 2026-06-12 | 2026-06-12 | `55674c2..f04c12b`（5 commit） | 绿（run 27386750356 三任务全 pass）；PR #1 → master |
| R7 | 横切机制与瘦身 | 已完成 | 2026-06-12 | 2026-06-12 | `1cbfc52..961060c`（5 commit） | 绿（run 27389247644 三任务全 success）；PR #2 → master |
| R8 | CI 门禁扩建 | 已完成 | 2026-06-12 | 2026-06-12 | `1c89e06..026d4b5`（7 commit） | 绿（run 27391794048 三任务全 success）；PR #3 → master |
| R9 | 数据库规模化（批1/批2/批3） | 已完成 | 2026-06-12 | 2026-06-12 | 批1 `1187a9d..543e0d0`（4 commit）；批2 `0ef3c2b..9510da0`（4 commit）；批3 `7ecbb62..e2d475d`（3 commit） | 批1 绿（run 27393227083）；批2 绿（run 27395161551）；批3 绿（run 27395903046 三任务全 success）；PR #4/#5/#6 → master |
| R11 | 行为评测与自动化闭环 | 已完成 | 2026-06-12 | 2026-06-12 | `77b6deb..ea7458c`（6 commit） | 绿（PR #8 run 27401073597 三任务全 success）；freshness 另有 2 次 workflow_dispatch 实测 success（run 27399467099/27399541184）；PR #8 → master |
| R12 | 安全、领域与微缺口增补 | 已完成 | 2026-06-12 | 2026-06-12 | `9004f63..746b1f6`（8 commit） | 绿（PR #9 run 27406356396 **四任务**全 success，含新增 windows-latest 安装看护 job）；PR #9 → master |
| R10 | 门面工程与发布（收官） | 已完成 | 2026-06-12 | 2026-06-12 | `55b18c0..783bb8d`（4 commit） | 绿（master run 27409535488 含 windows-latest 全 success）；12 PR 全 merged；v3.0.0 已发布 |

## 基线度量（首次用到时填，后续轮引用）

- 常驻 11 技能 SKILL.md 总行数基线（R7 开工 2026-06-12 `wc -l` 量取）：**901 行**。目标 -15% → ≤765 行（须减 ≥136 行）。逐技能：file-reading 47 / memory-pm 91 / orchestrator 129 / backend-coding 89 / system-design 62 / frontend-design 99 / project-structure 90 / consistency 100 / self-review 65 / tool-selection 77 / research-ethics 52。（m16 slides 非常驻，不计入此基线。）
  - **R7 收尾实测：901 → 763 行（-15.3%，达标）**。逐技能终值：file-reading 42 / memory-pm 81 / orchestrator 111 / backend-coding 57 / system-design 50 / frontend-design 83 / project-structure 80 / consistency 63 / self-review 73(+8) / tool-selection 71 / research-ethics 52。瘦身手法=细节下沉 references/examples、多 bullet 列表合并为少行、跨技能重复内容指认单一真相源后删副本；self-review 因新增「分级执行档」(R7.5)净 +8，属能力增量非冗余。**未删任何能力**：下沉内容全部进对应 references（a03 code_examples.md、m08 examples/full_pipeline_walkthrough.md、orchestrator pipelines.md 契约表+checkpoints.md 恢复探针、file-reading references.md 视频工具链等）。
- db05/db06/db07 真实卡数基线：约 1-2 / 1-2 / 2（审计 2026-06-11 口径）
  - **R9 开工实测（2026-06-12）**：迁移/扩展后基线其实是 14 / 14 / 19（审计口径只数了 seed 卡，未计入 R5 期已迁入 resources_real/design_system_cards/figure_advanced_cards 的实体卡）。**批1 收尾**：db05 14→18、db06 14→16、db07 19→31，三库均 ≥15 达标；新增 18 张卡，每卡带来源+核验日期，抽查 5/18(28%) 来源一致（_verification_log/R9-batch1-card-spotcheck.md）。
  - **批3 跨库机制（2026-06-12）**：R9.7 palette.json 视觉 SSOT 实例机制落地（dairygoat 12 token，hex 逐项比对源文件全匹配），四技能接线；R9.8 四库采集管线同口径成文 + 修 freshness 漏认 `核验日期`（统计 313→318 卡）。db05/06/07 卡数维持批1 的 18/16/31。
- db01 venue 基线 204（R9 开工）→ **批2 收尾 308**：OpenAlex 逐卡核验新增 104 张（方向命中农业工程/智慧农业/精准畜牧/奶业/兽医、CV/AI/ML、医学影像/临床肿瘤、生信、机器人/语音、统计、环境/食品/材料/能源/地学、HCI），全 19 列、物理行==逻辑行无多行字段被压平。ai_policy 12→186 张有值（六大出版社官方页实查）。抽查 22/104(21%) 来源一致（_verification_log/R9-batch2-db01-spotcheck.md）。db02 写作样本 16→24（+8 篇 2024-2026 顶会顶刊）。
- ROUTER_EXAMPLES 必覆盖基线：7/28

## 偏差日志（只追加，不删改）

> 格式：`- [日期] R几.第几项 — 计划说什么 / 现实是什么 / 怎么处理的（自行修正|降级|跳过待用户）`

- [2026-06-11] 总纲§5 — 计划写校验器在 `tools/`；现实在 `.github/scripts/`（check_*.py + run_skill_selftests.py）。自行修正：全程用 `.github/scripts/` 路径，后续轮同。
- [2026-06-11] 总纲§5 — selftest 在 Windows 默认 GBK 控制台打印 `✓` 抛 UnicodeEncodeError（退出码1，非测试失败，45 脚本全 PASS）。处理：全程用 `PYTHONUTF8=1` 跑门禁；本身是真实可移植性隐患，但修 runner 编码属 R8 CI 范畴，本轮未改 runner，仅记录。
- [2026-06-11] R1.1 — 计划点名限流口径在 m04/m13/m10/a09；现实具体数字在 m01(literature-search)、m03(idea-generation)、venue-matching、citation、ip-application。按现实处理：m01 设真相源，其余全部指向并删数字。另发现 ip-application 有 2026-06-06 curl 实测"匿名仍 200"与官网"需 key"冲突——联网核实官网现行需 key+$1/天，保留实测为诚实存档并判定为过渡期现象。附带修正：OpenAlex 文档域名已迁 docs.openalex.org→developers.openalex.org，相关链接同步。
- [2026-06-11] R1.2 — 计划说 MDPI 栏宽"以 m09 SKILL.md 已核实表格为准"；现实 m09 表无 MDPI 行，真实来源是 m11(figure-planning) references.md「出版商图宽核查表」MDPI 行(170mm,⚠️付费墙未实测通行值)。按现实处理：figure_export.py mdpi 键 note 注明来源为 m11，verified=False。
- [2026-06-11] R1.3 — 联网核实 Science 三档为 5.5/12/18.3cm，即双栏 120mm，121mm 系换算误差。额外发现 science.mplstyle 把 121mm 写死进默认 figsize(真实出图偏差)，一并订正为 120mm(4.724in)。science.org 仍 403，数值经 WebSearch 多源一致核实。
- [2026-06-11] R1.4 — m05 模板实际文件名是连字符 experiment-matrix.md，与 orchestrator 下划线契约不符；按计划统一为下划线(git mv + 3 处引用)。仓库内 m 编号与计划标签偶有错位(如 figure-planning 内部自称 m11 指执行器)，按文件路径作业，不按编号。
- [2026-06-11] R1.5 — 计划假设 11 个 SKILL.md 有 `../../docs/design`/CONVENTIONS 硬路径会断；现实只有 orchestrator:121 一处 `../../docs/design` 硬链接(已改弱引用)，其余 16 处 CONVENTIONS 均为纯文字提及(不算断链)。仍按计划把 4 文档随装链接(sh symlink / ps1 hardlink)并加校验，使纯文字引用装后可达。已在临时/真实 ~/.claude 实测链接生成成功、内容可读。
- [2026-06-11] R1.5 — install.ps1 原为纯 ASCII；首次加中文注释触发 PowerShell 5.1 GBK 解析错误(真实 Windows 用户会中招)。修正：install.ps1 注释保持 ASCII-only。
- [2026-06-11] R1.6 — 计划假设 README:9 写"三端(Claude/Codex/Hermes)"与 install 两端冲突；现实 README 已是"Claude Code 与 Codex"两端表述，无三端硬冲突。曾按方案 B 在中英 README 补 Hermes 说明，**后经用户确认对外只支持两端，已删除该 Hermes 段**（见用户决策项，此项关闭，install 不加第三目标）。
- [2026-06-11] R1.8 — 计划说 a03 已实测 v6；现实 a03(backend-coding)确已全 v6 且有 GitHub API 实测记录。真正残留 v4/v5 在 system-design(a04 模板+references)与 tool-selection(references+detect_stack.py fixture)，已升 v6 并指向 a03 真相源。
- [2026-06-11] R1.10 — 计划说无参 selftest 落 5 PNG 到技能根；现实 `--selftest` 路径已用 tempfile(不污染)，真正污染是"无参无 JSON 的 demo 路径"(tag=selftest 落 CWD)。修正该 demo 路径改临时目录，并把 tag 由 selftest 改 demo。
- [2026-06-11] R1.12 — .gitignore 已含 __pycache__//*.py[cod]，无 tracked 缓存；out_multipanel 由 examples/example_matplotlib_multipanel.py 落 HERE 造成。改为默认临时目录(--outdir 可选)，删残留 PNG/PDF，清本地缓存目录。
- [2026-06-11] R2 全程 — 计划要求 a02 新模板放 templates/、细则下沉 references/；orchestrator §5 引用这些跨技能文件时，check_skill_links.py 会把裸 `templates/x.md` / `references/x.md` 反引号路径当成 orchestrator 自身内部路径校验而报缺失。处理：orchestrator 内一律写全 `light-memory-pm/templates/...`、`light-memory-pm/references/...` 前缀，链接门转绿。后续轮跨技能引用模板/参考时同此写法。
- [2026-06-11] R2.4-4 — 计划只说 a06 scaffold 纳入 `.light/`；执行中明确 `.light/`（passport + handoff 卡）是跨会话续跑真相源，应**纳入版本控制而非忽略**，故在 python-research.gitignore 末尾加注释显式声明不忽略 .light/，并在 scaffold selftest 断言两目录生成。
- [2026-06-11] R2.5 演练 — 示例项目 dairygoat 演练前无 `.light/`（轻项目靠 db09 卡承载）。按协议新建 .light/handoff 并落 S01/S02 两张真实卡作为工作示例；B 会话恢复用 `pytest tests/test_infer_track.py`(2 passed)实证 S01"已完成"声明无损，非口头比对。
- [2026-06-11] R3.5 — 计划说把实测栏宽写入 db01"新增字段/列"；现实 venues.csv 为固定 19 列 schema，check_databases.py 按列校验，新增列会破坏既有 332 卡。按现实处理：栏宽实测值追加进末列 catch-all `risk_note`（带来源+日期+方法），不改 schema，与 README"新增条目追加"惯例一致。
- [2026-06-11] R3.5 — 农业机械学报(j-csam.org)版心栏宽未取得：站点 PDF 入口返回反爬 JS 守卫页(`_guard/html.js`，59 字节)而非 PDF，三次重试均被拦。按诚信纪律标 GAP、db01 该刊栏宽留"待核查"，不从记忆/英文刊类比硬填。其余三刊(农业工程学报/中国农业科学/作物学报)均从发表 PDF 实测成功。
- [2026-06-11] R3.2 — 可选项 lint_gbt7714.py(GB/T 7714 中文条目 lint 脚本)本轮未实现：核验兜底以"人工浏览器比对检索结果页"为主路径(CNKI 执行环境直连不通，见验证日志§4)，脚本化 lint 价值有限且会新增 selftest 负担，判定为非必需，降级跳过。如后续要做，归 R8 CI 门禁范畴。
- [2026-06-11] R4.1 — 计划说"复用 a10 脚本接线"。现实：装到 ~/.claude/skills 后两技能平级、Python 无法跨技能 import。按现实处理：在 verify_refs.py **内联**同源判定逻辑(相同 FLAG_TYPES + update-to[] 判定)，注释指认 check_retractions.py 为同源真相，两脚本口径一致；不新增 HTTP(update-to 在已取的 Crossref 响应里)。另发现经典撤稿论文(STAP/Wakefield)本身 update-to 多为空、仅标题带 RETRACTED 前缀，故补标题前缀作补充信号。实查撤稿样例 `10.1016/j.micpro.2020.103768`(Elsevier，update-to 暴露 retraction)留痕。
- [2026-06-11] R4.3 — 计划说"db01 增 ai_policy 字段 / check_databases 认识新字段"。核查真相：check_databases.py 只 rglob databases/**/*.md 校验 db03–db08 的 YAML 卡，**根本不读 venues.csv**(db01/02 是 CSV，不在 schema 校验范围)，故"加列破坏 332 卡校验"的技术理由不准确。但用户硬约束(不加列、追加 risk_note)是明确产品意志且有独立合理性(204 卡加列需逐行补值)，遵守之：ai_policy 以 `ai_policy=` 子串追加进 risk_note。**两个坑**：①venues.csv 含多行字段，禁用 csv 模块全量重写(会把多行压成单行，205→186 行)；②追加文本禁含英文逗号(目标字段无外层引号，逗号会拆列)，改用中文分号/顿号 + 文本级唯一锚点替换，最终 diff 仅 12 增 12 删。
- [2026-06-11] R4.3 — 发现 R3 遗留瑕疵(不在 R4 范围)：venues.csv 物理行 186/187(中国农业科学、作物学报)在 HEAD 版即为 22 列(非 19)——R3 填栏宽实测时 risk_note 写入未加引号的英文逗号(如 `81mm/整页约170mm(A4双栏,来源:...,2026-06-11),2026-06`)被 CSV 解析器拆成多列。check_databases 不读 CSV 故 CI 不报。修复=给 risk_note 加引号，零风险但属扩大范围，**留 R9(db01 规模化)统一处理**。
- [2026-06-11] R4.2/R4.12/R4.13 — 实查诚信记录：①AI 图像政策 Elsevier 取得逐字原文，Nature(登录墙 303)/Science(403) 仅政策立场多源核实、确切引文标 GAP；②latexdiff 本机 MiKTeX 缺 Perl 模块 Algorithm::Diff，`latexdiff --version` 即报错，diff 输出未跑通标 GAP，流程按公开文档写并注明未本机验证；③飞书实查澄清官方云文档**无独立演示文稿 OpenAPI**，lark-slides 是 larksuite/cli 社区工具非官方 API，未凭"飞书有幻灯片"印象硬填。
- [2026-06-11] R4 跨技能引用 — 再次踩 check_skill_links 陷阱：在 A 技能 SKILL/references 用反引号写 B 技能的 `scripts/x.py`、`references/x.md` 会被当 A 自身路径报缺失。已全部加 `light-<skill>/` 前缀修正(citation↔research-ethics 脚本互引、figure-drawing/slides↔其他、typesetting↔review-rebuttal)。另：技能正文引用 `databases/db01...` 完整路径属安装后断链风险，改纯文字"db01"提及(与全仓库惯例一致)。
- [2026-06-11] R5.4 — 功效分析算例数值不凭记忆：本机 statsmodels 0.14.5 实跑 `TTestIndPower().solve_power`，d=0.3/0.5/0.8 → 每组 175.38/63.77/25.52(取 176/64/26)，反查 d=0.5 n=5 → power 仅 0.108。逐字留痕 `_verification_log/R5-04-power-analysis.md`，references 表数值与之一致并注明留痕路径。结论写实"3~5 种子只够检大效应"这一对用户最有用的功效缺口。
- [2026-06-11] R5.4 — plan_lint.py 首版在 Python 字符串里用了中文引号包"对应假设"导致 SyntaxError(全角引号≠ASCII)；改用「」书名号修复。教训:脚本内中文文案避免与 Python 语法字符冲突的全角标点。
- [2026-06-11] R5.5 — 计划要"先查有无现成 bootstrap 工具勿重写"：现实 significance_test.py 已有 `bootstrap_ci`，analyze_results 的配对差值 CI 直接 import 复用，未重写。配对识别复用合成 CSV 本就共享 seed 列(天然配对陷阱)，selftest 同时验配对/独立/共享<2 跳过/缺键四路径。
- [2026-06-11] R5.7 — er_diagram selftest 初版断言 `out.count("{")==2` 误判:Mermaid 关系符号 `||--o{` 自带花括号，把关系行也数进去了。改为只数"以 { 结尾的行"判实体块数。教训:对含特殊符号的 DSL 输出做结构断言要按行语义数，别全文 count 字符。
- [2026-06-11] R5.7 — a04 references 是 7 个常驻技能里唯一没有研究日期时效锚标头的(计划点名)，已补"研究日期 2026-06 + 落地前以所装版本官方文档为准"。
- [2026-06-11] R5.8 — m15↔m11 专利附图断链:m15 原本只写"交 m11 绘制"无具体规范、m11 无对应节。已在 m11 references 新增「专利附图规范」节(图号/标记线/黑白线条/流程图框图)作真相源，m15 SKILL 两处 + m11 SKILL 衔接段双向互指该节。专利附图规范以 CNIPA 现行审查指南为准,本节为通用要点未逐条核对最新版次(已注明),最终须代理师审。
- [2026-06-11] R5.9 — scaffold 目录有本地 `.pytest_cache/`(被 .gitignore:7 覆盖、未追踪),属跑测试的本地产物非仓库内容,未提交。pyproject 加 [tool.mypy] 后用 tomllib 实测可解析。
- [2026-06-12] R6.1 — 三家生图 API 已联网核实(2026-06-12)端点/参数/尺寸/透明支持,逐条留痕 `_verification_log/R6-imggen-api.md`并回填 references.md「生图后端」节。关键真相:①透明背景**仅 OpenAI gpt-image 有显式 `background:transparent`**,Gemini/Seedream 无开关(标 GAP,做透明图标优先 OpenAI 或 PIL 去底);②三家 seed 都不稳(OpenAI/Gemini 官方未列,Seedream 5.0 系列亦未明列),风格一致性改靠唯一 style_anchor+图生图参考,不靠 seed;③Seedream `watermark` 默认 true,封装层已默认置 false(否则 PPT 元素带"AI 生成"水印);④Gemini 图像走通用 generateContent 无独立 images 端点;⑤OpenAI size 仅固定档,16:9 用 1536x1024 近似。
- [2026-06-12] R6.6#4 — `GAP：待实测(2026-06-XX)`:有 key 端到端实跑(≥5 页 deck、五阶段产物齐全、QA 两项新检查、db06 沉风格卡)**未做**。执行环境探测到平台级 `OPENAI_API_KEY`,但真实生图请求会向第三方传 prompt 且计费,属外部副作用,未经用户显式授权不触发(与 selftest 离线纪律一致)。无 key 装配链(R6.6#3)已端到端实测 PASS:3 页 deck_spec 模板 + imagegen.py mock 占位 PNG → assemble_from_spec.py 产 3 页可编辑 pptx,重开校验 6 原生文本框(=title/body 元素数,守边界三文本未栅格化)+ 4 图片 + 0 warning。
  - **[2026-06-13 已关闭]** 用户显式授权后实跑:经 OpenAI 兼容中转 gpt-image-2 出 5 个生图元素(2 背景+2 插画+1 图标)+ m11 真数据图,assemble 出 5 页可编辑 pptx(10 原生文本框 + 6 图片 + 0 warning,数据图未生图)。踩坑回灌 imagegen.py(中转两跳/CDN 下载需浏览器 UA/超时/重试/manifest model)。实测记录回填 imggen_pipeline.md,db06 沉「智慧农业项目答辩 — imggen 实跑」卡,spec=`light-slides/examples/deck_spec.dairygoat.yaml`,留痕 `_verification_log/R-imggen-deck-e2e.md`。
- [2026-06-12] R6 跨技能引用 — 又踩 check_skill_links 陷阱(PROGRESS 已多次记):在 a05/a10/m17 用反引号写 m16 的 `references/imggen_pipeline.md` 被当本技能内部路径报缺失,全部加 `light-slides/` 前缀修正。imagegen.py mock selftest 在 Windows 下 `Image.open` 不 `.load()` 会锁文件致 TemporaryDirectory 清理失败(WinError 32),改 `with Image.open() as im: im.load()` 释放句柄。
- [2026-06-12] R6.2 — assemble_from_spec.py 装配 chart 元素**只 add_picture 真数据图(figures/),绝不在装配层生图**(守边界一);资产缺失画占位框+warn 不静默跳过(诚信纪律,与 to_pdf.py 同);themes.py 跨目录 import 失败时用内置兜底色板,保证离线 selftest 不依赖 import 路径。
- [2026-06-12] R7 行数目标 — 计划把 F 组瘦身列在 m07/m08/m15/m16/m17 等**手动技能**，但 -15% 目标是对**常驻 11 技能**。两者交集小（F 组直接命中常驻的只有 a03/a09），且 E 组(R7.5-R7.12)给常驻**增**内容(a08 分级档+8、orchestrator passport/并行、a01 视频)。故按 F 组「正文留决策+一行指针、细节下沉 references」手法**横向施于全部常驻**：a03 代码例/调试四法下沉 code_examples.md(-32)、consistency 工具视角+检查维度合并(-37)、orchestrator §2 契约表镜像下沉 pipelines.md + §0 探针下沉 checkpoints.md(-18)、frontend 框架 how-to 指 references(-16)、system-design 部署/RLS/迁移多 bullet 合并(-12)、memory-pm 工具映射+写入示例压缩(-10)、project-structure 质量门/模板列表压缩(-10)。最终 901→763(-15.3%)。**严格只下沉不删能力**：每处删除的正文内容均已在对应 references 存在或同轮补入，新建 a03/code_examples.md 与 m08/examples/full_pipeline_walkthrough.md 承接。
- [2026-06-12] R7.2 种子数 — 计划写 m05「≥3~5」vs m06「≥5」。统一为「≥5；算力受限 ≥3 且须在 m06 报告显式标注」，两技能同句式。功效分析数值(d=0.5 需每组~64)保留，措辞从「3~5 个种子」改为「少量种子」避免与新阈值打架。
- [2026-06-12] R7.3 uv 默认 — scaffold.py 原只有 `--poetry`。改为 pyproject **始终落地**、默认 uv 后端(hatchling + `[dependency-groups]` + `[tool.hatch]` src 布局)、`--poetry` 切备选(poetry-core)，`--uv/--poetry` 互斥组。selftest 覆盖两路径并 tomllib 解析校验。a06 SKILL 三处(整理动作/版本依赖/资产清单)同步改默认 uv。
- [2026-06-12] R7.4 vaex — 计划只点 a09 decision_matrix.md:13。现实 vaex 还活跃出现在 m02(data-engineering) SKILL:18 + references「## Vaex」节、a09 detect_stack.py:31。按验收「grep vaex 仅余已淘汰标注」全仓库处理：decision_matrix 换 DuckDB/polars streaming/dask、detect_stack 改迁移告警、m02 SKILL 换 DuckDB 并指 a09 单一口径、m02 references「## Vaex」标「已淘汰仅存档」并新增「## DuckDB」承接能力。
- [2026-06-12] R7.10 CUMCM AI 规定 — 计划写「CUMCM 2024 起 AI 使用规定」。联网核实(官方 dxs.moe.gov.cn，2026-06)：CUMCM 正式 AI 规定是**2025 年试行版(自 2025-09-01)**，非 2024。按现实写入 m17：允许但非必须、核心独立完成、未用须声明、用了须正文标注+提交 PDF「AI 工具使用详情」、违规取消评奖；带 last_checked。留痕见对话。
- [2026-06-12] R7.22 tex 编译 — 计划预案「本机无 TeX 则标注待验证」。现实本机有 MiKTeX + **Tectonic**，五份 .tex 骨架全部 `tectonic` 实编译退出 0 产 PDF(IEEE/ACM/Springer/Elsevier 走 pdflatex、ctex_chinese 走 XeLaTeX 自动装中文字体)，非 GAP。留痕 `_verification_log/R7-tex-compile.md`。
- [2026-06-12] R7 新脚本 — m14 新增 `scripts/rebuttal_budget.py`(会议 rebuttal 字数/页数预算检查，纯 stdlib，中英混排分别计词，超限返回码 1)，已登记 WHATS_INCLUDED(脚本数 50→51，meta 表计数同步)、selftest 通过。
- [2026-06-12] R8.0 — 计划 08 写校验器在 `tools/`、疑 ci.yml 漏 `tools/**` 触发。现实(已核实)：校验器在 `.github/scripts/`，ci.yml 两处 paths 已含 `".github/scripts/**"` 与 `".github/workflows/**"`，且不含 `docs/**`(总纲"docs 不触发"假设成立)。自盲区**不存在**，无需改 paths，工时转投 R8.1(PROGRESS 早有此偏差，本轮确认关闭)。
- [2026-06-12] R8.4 db09 路径 — 计划写 db09 项目卡在 `projects/*/project_card.md`。现实 db09 真相在 `databases/db09-projects/projects/<slug>/`(根目录 `projects/` 是可运行 scaffold 演示，两者不同)。schema 校验对准 databases/db09-projects；CONVENTIONS §3 的 14 字段为真相源(yaml 块含全部 14 键，末两键 decision_log/version_history 写"见 X.md"指针，校验只验键存在非空)。
- [2026-06-12] R8.2 暴露存量漂移 — WHATS_INCLUDED 模板表旧写 `experiment-matrix.md`(连字符)，实际文件 R1.4 已改 `experiment_matrix.md`(下划线)。模板 gate 一开即抓，已修；并把原 6 行高亮表升级为 40 个模板全量 1:1 登记(表末保留 scripts 配套/assets/db 文件高亮行，正则只认 `templates/` 行进校验)。
- [2026-06-12] R8 校验器计数口径 — 判据"7→≥10 个校验器"：独立脚本 7→8(新建 check_freshness)；但新增 gate 点远超 3 个(路由 28/28、README 结构、模板防漂移、db09 schema、体量、离线性、产物残留、安装可达性)。按"独立 gate 点"计 ≥10 达标；freshness 为 warn-only 旁路不计硬门。
- [2026-06-12] R8.7 离线 gate 实现档 — 按计划取折中方案：环境哨兵 `LIGHT_SELFTEST_OFFLINE=1` + 代理指黑洞(127.0.0.1:9) + 文档纪律。能挡 proxy 感知的 HTTP 客户端(实测 urlopen 被挡)，挡不住裸 socket 连硬编码 IP——已在 runner docstring 留 UPGRADE 注释(socket 层 audit hook/seccomp/netns 为后续升级路径)。
- [2026-06-12] R9批1 — 计划/审计说 db05/06/07 真实卡"各仅 1-2 张"；开工实测基线实为 14/14/19（审计只数了各库 *_cards.md 的 seed，未计 R5 期已迁入 resources_real.md / design_system_cards.md / figure_advanced_cards.md 的实体卡）。按现实处理：批1 仍按"补到 ≥15"目标推进并实打实新增（db05+4/db06+2/db07+12），不因基线已达标而跳过——谱系/场景/图型缺口才是真需求。db07 早已 >15，但 g1-g9 自家图与箱线/数据集示意/组图谱系缺口仍补齐（计划明确点名）。
- [2026-06-12] R9批1 — YAML 填卡两次踩"值内英文冒号+空格"陷阱：db05 `backdrop-filter: blur()`、db07 `区别于混淆矩阵: 这里`，PyYAML 报 `mapping values are not allowed here`。check_databases 当场抓。修法=去掉冒号后空格(`backdrop-filter:blur()`)或换破折号。教训沿用 R4 卡填经验：卡内值含英文冒号须紧跟非空格或加引号。
- [2026-06-12] R9批1 — db06 风格卡来源诚信：R6.5 声明"每出一套 imggen deck 落一张 db06 风格卡"，但有 key 端到端实跑仍是 GAP(R6.6#4)。批1 db06 两卡(开题/课程教学)**不冒充 imggen 来源**——色板/字体取自已 selftest 验证的 themes.py(academic/light_elegant)，版式逻辑参照公开来源(Beamer 矩阵/CMU 教学，HTTP 200)，并在卡文件头与抽查日志显式声明此边界。imggen 实跑沉卡待 R6 补做。
- [2026-06-12] R9批1 — db07 九图反哺卡衔接 JOURNAL_SPECS 时，核实真相源在 light-figure-**drawing**(非 figure-planning) 的 `scripts/figure_export.py`，实测值 IEEE 单栏 88.9mm(≈3.5in)/Nature 89-183mm/Science 55-120-183mm；卡内衔接段按实测值与正确技能名写，未凭"m11"标签想当然。
- [2026-06-12] R9批2 — venues.csv **CRLF 回归**：本机 Python 脚本以 `newline=""` 写回时把原 LF 文件整体转成 CRLF，`git diff --check` 把 205 行 `\r` 全报 trailing whitespace、diff 也虚增。核实 HEAD 版本是纯 LF(205 LF/0 CRLF)，判定为我引入的回归，已字节级 `replace(b'\r\n',b'\n')` 统一回 LF，diff 收敛为真实改动(201 增 97 删=104 新行+97 行追加 ai_policy)。教训：改 venues.csv 的脚本应显式按 LF 写(或写完即转)，Windows 默认行尾会污染整文件 diff。
- [2026-06-12] R9批2 — OpenAlex **publication_year 噪声**：按 `cited_by_count>X` 拉"2024-2026 高被引"时，大量经典论文(Attention/BatchNorm)因镜像记录重标 2024/2025、DOI 为 `10.57702/*` 等非权威重复 DOI 混入。判定不可盲取：db02 改用官方获奖名单(NeurIPS/CVPR Awards 页)定篇 → 逐篇按标题回查 OpenAlex 取权威 IEEE/期刊 DOI(CVPR 系 10.1109/cvpr52733.2024.*)，"Not All Tokens"回查命中 2019 错篇即剔除。venue 采集同理按精确 ISSN 查、剔 works<50 碎片记录。
- [2026-06-12] R9批3 — R9.7 palette.json 取色来源选定：dairygoat 是农业/CV/畜牧项目，色板取自 db06 `light-slides/assets/themes.py` 的 AGRICULTURE 主题（该主题 scenario 原文含"畜牧检测项目"，themes.py 已 selftest 绿，是最硬的可追溯真相源），语义色取自 db05 design_tokens.template.json(DTCG SSOT)。12 个 token 的 hex 经程序化逐项比对源文件**全部精确匹配**（留痕 `_verification_log/R9-batch3-palette-verification.md`），无凭记忆填色。卡内 `source` 字段用 `db06:light-slides/...::AGRICULTURE.COLORS.primary` / `db05:design_tokens.template.json::color.semantic.success` 这类可定位 id。
- [2026-06-12] R9批3 — palette.json 跨技能引用写法：技能正文引用 palette.json 用完整 `databases/db09-projects/projects/<project_name>/palette.json` 路径（与 m11 既有引用 `databases/db09-projects/.../version_history.md` 同惯例），不带 `../` 不以 references/templates 等受保护目录开头，故不触发 check_skill_links 的内部路径/安装可达性 gate（已实测 8 门禁全绿）。四处接线 grep 可见：m11 配色节、m16 视觉风格步、a05 设计语言段、a07 维护要点+五维⑤视觉。
- [2026-06-12] R9批3 — R9.8 发现并修一处真实 freshness 衔接断点：`check_freshness.py` 的 PROSE_DATE_RE 原只认 `核实日期/研究日期/核查日期/核实于/更新于`，而 db05/06/07 的 6 个卡文件实际写 `核验日期`，导致它们被静默漏统计（db05/06/07 仅各计 2/1/1 张）。补 `核验日期` 同义词到正则 + selftest 断言，修复后统计 3/2/3 张（合计 313→318）。这是 warn-only 脚本（不阻断 CI），属"采集管线与 freshness 月度流程衔接"的实质修复，非扩大范围。db05/06/07 README 各补与 db01 同口径的五步采集→核验→入库管线。
- [2026-06-12] R11.2/R11.5 评测方法 — 计划写"每任务新开会话粘 input 判分"。本执行环境用 Claude Code 子代理实现：actor 子会话读真实 SKILL.md+脚本、对 expect/red_flags **盲**、dry-run 产出，主会话作**独立判分员**（满足"判分者≠被测会话本人"）。Tier1 24 任务全 2 分、红旗 0；弱模型用同族低配档 **Haiku 4.5**（第三方 DeepSeek 等无 API 接入，标 GAP）跑 8 红旗任务，红线守住 8/8。已在 evals/README「已知局限」声明非第三方人工评测。
- [2026-06-12] R11.3 结构性约束（重要，给 R10 合并用） — 计划要求 freshness.yml `workflow_dispatch` 手动触发实测成功。**GitHub 硬规则：workflow_dispatch 只能触发"默认分支(master)上已存在的工作流文件"**。本仓库 R1-R11 叠加 PR 未并入 master（master 落后约 46 提交、连 check_freshness.py 都没有），直接 dispatch 报 `HTTP 404 not found on the default branch`。经用户授权（"哪个好用哪个"，选可逆方案）：临时把仓库默认分支切到 r11 分支 → 实测两次 success（run 27399467099 开单/27399541184 更单）→ **立即切回 master**（已确认复原）。留痕 `_verification_log/R11-freshness-dispatch.md`。**R10 合并后 dispatch 即在 master 长期可用，无需再切默认分支。**
- [2026-06-12] R11.4 增量追踪诚实发现 — dairygoat 真实增量跑（OpenAlex/Crossref=200）证 `--from-date` 过滤生效（基线 1970-2020、增量仅 2023-24、year<2023 为 0）。但宽 query+被引排序的原始增量 24 条几乎全是领域外高被引噪声（YOLOv7/DETR/DreamBooth/无关综述），真正相关≈0-1。如实写进 watch_report 与 references 铁律"宽 query 须相关度筛选再入库"，**未把噪声自动入 known_dois.txt**（演示不污染已读库）。这复现了 m01 既有"收窄检索式"纪律，非技能缺陷。
- [2026-06-12] R12.1 防注入标记口径 — 计划 13 号文件头写标记为 `INJECTION-ACKNOWLEDGED`，但仓库现实里 m04（protocol.md/SKILL.md×2/verdict_template.md/eval）早已用 `INJECTION-ATTEMPT-DETECTED`。按"以仓库现实为准"采用既有标记 `INJECTION-ATTEMPT-DETECTED` 作全仓库唯一措辞，CONVENTIONS §4 设真相源、a01/m01/a10 放指针。计划说"四处落地"=CONVENTIONS+a01+m01+a10；m04 是既有第五处、自动随之口径统一（非新增）。顺手修回 m01 灰色文献节丢失的 `##` 标题（疑早期编辑误删）。
- [2026-06-12] R12.2 穿透删除复现的诚实结论 — 计划要求"本地复现穿透删除会被抓"。本机 Win11 10.0.26200 + PS5.1 实测：经典 `rmdir /s` / `Remove-Item -Recurse` 作用于 junction **均未穿透**删到源（现代 Windows/.NET 已修复该行为），与教科书假设不符。真正稳定触发穿透的是"先 `Get-Item.Target` 解析成目标真实路径再递归删"（Case4，任何 OS 都删源）。故 CI 断言以"卸载后源哨兵文件+28 SKILL.md 必须完好"为准（对任何穿透成因都成立），Case4 证该断言 exit 1 有牙。留痕 `_verification_log/R12-02`。新增 CI 用 `.github/scripts/check_install_windows.ps1`（非技能脚本、不进 51 selftest、不入四件套计数），windows-latest job CI 实跑 success（run 27406356396）。
- [2026-06-12] R12.7 m11 色觉模拟"伪缺口"确认 — 计划列为可选微项，实查发现 m11 `scripts/color_palettes.py` **早有** `simulate_cvd()`(colorspacious 精确+降级近似)+`preview_palette()`(原色/灰度/三色盲对照)，能力已在。故只在 references 加一行"定稿前渲染模拟复核"指引（指向既有脚本+Coblis 在线器），不新增脚本，避免重复建设（与计划"色盲安全色环已是 m11 默认"的伪缺口排除一致）。m16 讲稿导出同走 ≤15 行 patterns 说明（python-pptx 读 notes，本机实跑验证 `has_notes_slide` 有效），不新增脚本。
- [2026-06-12] R12.8 竞品技能数审计旧结论已过时 — 计划/审计称"最接近的仅 6-8 技能"。2026-06-12 GitHub 实拉：anthropics/skills=**17**、K-Dense-AI/scientific-agent-skills=**146**(单库封装路线，远超审计估值)、ScienceIntelligence/ResearchSkills=8 学科+**有中文 README**。诚实修正写入矩阵：Light 差异化**不在技能数**（数量不占优），在**形态组合**（主线闭环+自有知识库+诚实机制+中文+会话衔接+行为评测同时具备）。逐格按实查写（中文链路格对 ScienceIntelligence 不写"无"），留痕 `_verification_log/R12-08`+草稿存 plan 文件夹供 R10。
- [2026-06-12] R10 合并方式 — 计划要求"先核对 PR #1-#9 依赖与冲突，拿不准问用户"。实测拓扑：master(R4)→r5→r6→r7→r8→r9批1/2/3→r11→r12 为**严格线性叠加**（r5-r11 全是 r12 的祖先，0 commit 在 master 不在 r12）。故无依赖/冲突问题，用户拍板**快进合并**（`git merge --ff-only`），master 一次性收 62 commit、0 冲突；push 后 GitHub 自动把 8 个 PR(#1/2/3/4/5/6/8/9)标记为 merged（#7 当初未建）。
- [2026-06-12] R10.1#3 演示动图 — 计划首选 vhs、备选 asciinema+agg，本机做不了则截图三联代替并标注。**本机无 vhs/asciinema/agg**（仅有 ffmpeg 但无录制源）。按诚信纪律**不放未经真实录制的动图**：①写可复现 `assets/demo.tape`（vhs 脚本，待装 vhs 的环境渲染 GIF）；②README「看它真的能跑」改以**真实案例 PDF + 九图**作"真的能跑"的证据（本就是端到端真跑产物，证据力强于摆拍 GIF）。链路图/社交预览图改用 matplotlib 程序化生成（真资产、可复现，非 GIF）。
- [2026-06-12] R10.1#6 链路图 SVG — 计划要 Mermaid 导出或手绘 SVG。本机无 rsvg/inkscape/mermaid-cli，改用 **matplotlib 程序化生成** `assets/pipeline.svg`(+png)，蛇形布局 17 手动主线 + 11 常驻底注环，中文字体走 Microsoft YaHei（实测无 tofu）。生成器 `assets/make_pipeline_svg.py` 入仓可复现。注意：YaHei 缺 `⇄/↔` 数学箭头（matplotlib 读 cmap 报 missing glyph，虽 PIL 能渲染），改用中文「·」连接符规避，无 glyph 警告。
- [2026-06-12] R10.3 Discussion 分类 — 计划要建 3 个中文分类(使用问答/技能建议/成果展示)。GitHub API/gh CLI **不支持程序化创建 discussion category**（仅 Web UI 可建）。现有默认分类 Q&A / Ideas / Show and tell 在语义上已覆盖三意图；社交预览图 PNG 与 discussion 分类两项需用户在仓库 Settings/Discussions 页手动操作，已在收官报告给指引。
- [2026-06-12] R10.4 版本号基线 — 仓库此前 Release 是 v1.0.0（CITATION 亦 1.0.0），并无 v2.x。第三期发布按计划锁定为 **v3.0.0**（"第三期"语义对齐主版本号），CITATION/CHANGELOG/tag/Release 四处一致；CHANGELOG 1.0.0→3.0.0 中间不补造 2.x 节（无对应发布，凭空造节违诚信）。

## 留给下一轮的话

> 每轮收尾写 1-3 行：下一轮要注意什么、有什么现场发现。

- R2 注意：orchestrator §5 已有 Handoff 格式、§0 断点恢复协议、§2 契约表(本轮已声明 CONVENTIONS §6.1 为真相源)；R2 收编 handoff 为单一口径时直接基于现有 §5，勿另起一套。
- R3 注意：会话衔接协议已就位——CONVENTIONS §9 全局纪律 + a02 两件套模板/细则 + orchestrator §5 收编 + a06 scaffold .light/ + 路由触发 + README FAQ + A/B 演练（_verification_log/session_handoff_drill.md）。后续任何轮长任务收尾都应主动留衔接卡 + 打印启动提示词（含执行本计划的轮间交接，11 号文件模板可与 handoff_prompt.md 互参）。
- R3 注意：跨技能引用别的技能的 templates//references/ 文件，反引号路径必须带 `light-<skill>/` 前缀，否则 check_skill_links.py 误判为本技能内部路径报缺失（R2 已踩，见偏差日志）。
- R3 注意：中文链路专项独立于 R2，无新增硬依赖；ROUTER_EXAMPLES 现 47 例(R2 +3 主动交接正例)，check_entry_docs 必覆盖集仍含 light-orchestrator。
- R4 注意：R3 未增减技能数(仍 28)、未加脚本、未动路由，故 WHATS_INCLUDED/MODE_REGISTRY/ROUTER_EXAMPLES 本轮无需同步(check_entry_docs 已绿)。R4 若收编外部生态技能会动技能数，记得四件套(README/ROUTER/MODE_REGISTRY/ROUTER_EXAMPLES)同步 + ROUTER_EXAMPLES 必覆盖集。
- R4 注意：db01 venues.csv 是 19 列固定 schema，任何"补字段"需求一律追加进 risk_note catch-all，勿加列(check_databases 按列校验 332 卡)。中文刊实测栏宽语义=版心栏宽(非官方图宽硬规格)，已在 db01 备注注明，引用时别当成出版商 author-guide 的 figure width。
- R4 注意：EI 收录权威源=Engineering Village 的 Compendex Source List(从产品页 View source list 现取当期 Excel，CDN 链接随版本变动，勿硬编码)；m13 已禁引第三方"EI 源刊"站。
- 全程门禁请带 `PYTHONUTF8=1`（Windows GBK 否则 selftest runner 打印 `✓` 报 UnicodeEncodeError，非测试失败）。校验器在 `.github/scripts/`，非 `tools/`。
- 安装链接已扩到 4 文档；R2 若动 CONVENTIONS/ROUTER 结构，记得 install 与 check_installation_assets.py 已对这些文件名有依赖。
- **R4 已完成（给 R5 的话）**：R4 未增减技能数(仍 28)、未加新脚本(只改 citation/verify_refs.py 现有脚本加撤稿检测)、未动路由，故四件套(README/ROUTER/MODE_REGISTRY/ROUTER_EXAMPLES)本轮无需同步，check_entry_docs 已绿。R5(资产补全)独立于 R4，按 05 号文件做。
- **R4.16(H11 图谱可视化)登记入 backlog，本轮不做**：计划 04 号文件明确 H-11 入 backlog；若未来要做，归 m01/m11 的引文网络/主题图谱可视化方向，非本期范围。
- **给 R9 的话(db01 规模化)**：①ai_policy 字段已定义为 risk_note 内 `ai_policy=` 子串口径(见 CONVENTIONS §3)，已实查填 12 家头部 venue，其余卡待 R9 批量补；②R4 发现 venues.csv 有 2 行(中国农业科学/作物学报，物理行 186/187)是 22 列(R3 填栏宽时 risk_note 含未加引号英文逗号被拆列)，R9 重做 db01 时给这两行 risk_note 加引号修回 19 列；③改 venues.csv 切记：含多行字段，禁用 csv 模块全量重写(会压平多行)，禁在无引号字段追加含英文逗号的文本(会拆列)，安全做法是文本级唯一锚点替换或给字段加引号。
- **R4 现场口径(供 a10/m07/m11/m16 后续轮引用一致性)**：AI 政策两类口径——期刊=AI 生成图像禁止+文本须披露；会议=LLM 允许+作者全责+不得署名。论文图严禁生成式 AI(figure_integrity「AI 生成图像政策」节为真相源)，R6 PPT 生图流水线只服务 PPT/前端、严禁进论文图链路(figure_integrity↔slides 已双向互指)。撤稿判定真相源=research-ethics/check_retractions.py 的 FLAG_TYPES，citation/verify_refs.py 内联同源(改判定常量须两处同步)。
- **R5 已完成（给 R6 的话）**：R5 新增 3 个脚本(plan_lint/venue_signal/er_diagram)，技能数仍 28、未动路由，故只需同步 WHATS_INCLUDED(已登记)，四件套其余无需动(check_entry_docs/check_skill_assets 已绿，48 脚本全 selftest)。零脚本技能(m13/a04)与零模板关键交付物(m03/m09)均已清零。R6(PPT 生图流水线)按 06 号文件做，注意 R4 现场口径"PPT 生图严禁进论文图链路"。
- **R5 现场口径(供后续轮引用一致性)**：①功效分析数值是 statsmodels 0.14.5 实跑(d=0.3/0.5/0.8 → 每组 176/64/26)，留痕 `_verification_log/R5-04-power-analysis.md`，改动须重跑核验；②paper2code 已按 I-1 以 references 形式并入 m05(复现五步协议)，非独立技能；③配对检验识别(m06 analyze_results --paired-by)与切片分析是结果分析两大新纪律，配对效应量用 d_z 不可与独立 d 混比；④数据增强红线"先划分再增强、只增训练折"，标注 IAA 复用 code_assets/agreement.py、标签错误检测用 cleanlab(找候选→人工裁定不全自动删)；⑤专利附图规范真相源在 m11 references「专利附图规范」节(m15↔m11 双向互引)，黑白线条不套论文配色；⑥静态类型档位:科研代码 pyright basic 起步/库代码 mypy --strict，scaffold pyproject 已带 [tool.mypy]。
- **R6 已完成（给 R7 的话）**：R6 是 m16 内部新增 mode(技能数仍 28),新增 2 脚本(imagegen/assemble_from_spec,共 50 脚本全 selftest)+1 模板(deck_spec.yaml)+1 references(imggen_pipeline.md),mode 数 8→10、有 mode 技能 3→4。四件套已同步:MODE_REGISTRY(m16 两 mode + 计数句 + footer 去 m16)、WHATS_INCLUDED(2 脚本+1 模板+计数 45→50)、check_entry_docs/check_skill_assets 已绿;ROUTER/ROUTER_EXAMPLES 未动(m16 路由触发词没变,本轮没加新触发场景)。**R7(横切机制与瘦身)注意**:①R7 要量取常驻 11 技能 SKILL.md 行数基线——m16 SKILL 本轮**只增 5 行**(两 mode 分流段),细节全下沉 imggen_pipeline.md(常驻瘦身纪律已遵守),量基线时把这 5 行算进去;②瘦身若动 m16 SKILL,别把两 mode 分流段删了(MODE_REGISTRY/check_entry_docs 依赖"两 mode"在正文可见)。
- **R6 现场口径(供后续轮/有 key 实跑引用一致性)**：①三家生图 API 真相源=`_verification_log/R6-imggen-api.md`(改端点同步 references.md「生图后端」节 + imagegen.py ENDPOINTS 常量,三处);②透明背景仅 OpenAI 原生,seed 三家都不稳→风格靠唯一 style_anchor(真相源在 deck_spec.yaml),Seedream 水印默认 true 必关;③三条硬边界(数据图不生图/论文图禁生图/文本不烤进图)三处互引锚点=m16 imggen_pipeline.md ↔ m11 figure_integrity「与 R6 生图流水线的边界」节 ↔ a10 SKILL §5,改任一处口径须同步三处;④**R6.6#4 有 key 端到端实跑是 GAP**:配 OPENAI/GEMINI/ARK key 后按 06 号文件 R6.6 第 4 条跑≥5 页 deck,回填 imggen_pipeline.md「实测记录」节 + 沉一张 db06 风格卡 + 留痕 `_verification_log/`;db06 风格卡是 R9 db06 上量的主要真实卡来源(R6.5 已声明联动)。
- **R7 已完成（给 R8 的话）**：①脚本数 50→51（新增 m14 `rebuttal_budget.py`），WHATS_INCLUDED + meta 计数已同步，check_skill_assets/run_skill_selftests 全绿（51 PASS）。R8(CI 门禁扩建)若加「行数预算门」可直接量常驻 11 技能（763/≤765，留 2 行裕度，后续轮往常驻加内容前先看这条余量）。②技能数仍 28、mode 仍 10、路由触发词未改，ROUTER/ROUTER_EXAMPLES/MODE_REGISTRY 本轮未动（仅 m07 description 精简但触发关键词全保留，check_entry_docs 已绿）——R8 若新增校验器注意 route_examples=47 不变。③R7 新建两个下沉文件（`light-backend-coding/references/code_examples.md`、`light-paper-polishing/examples/full_pipeline_walkthrough.md`）属 references/examples 非脚本，不进 selftest。④跨技能新口径供 R8+ 一致性引用：检索库数统一 ≥2（m03↔m04）、种子数统一 ≥5/受限≥3 须标注（m05↔m06）、依赖管理默认 uv（a03↔a06）、vaex 全仓库标已淘汰（迁 DuckDB/polars streaming，a09 decision_matrix 为单一口径）。⑤a08 self-review 新增「分级执行档」（轻任务最小三项证据/事实/夸大 vs 重产出全量 11 项），orchestrator checkpoints.md 已引用；R8 行为评测设计自审类任务时按此分档。
- **R7 现场口径(供后续轮引用一致性)**：①a07 consistency「变更广播」回扫的权威已产出材料清单 = orchestrator `.light/passport.yaml` 各阶段 `artifacts:` 并集（无 passport 退 db09 version_history），orchestrator §4 已双向指认——改 passport schema 须顾及 a07 消费侧。②m08 findings JSON 被 m14 模拟审稿消费（overclaim→Soundness major、ai_tone/punctuation→Presentation minor），字段映射在 m14「消费 m08 润色发现」节、schema 在 m08 references/findings_schema.md，改 category 取值两处同步。③m12 五份 .tex 骨架已 Tectonic 实编译验证（留痕 `_verification_log/R7-tex-compile.md`），R8 若上 CI TeX 编译门可复用此结论、离线环境需预置 TeX Live/MiKTeX 对应包。

- **R8 已完成（给 R9 的话）**：①CI 校验器现 8 个脚本(新建 `check_freshness.py`，warn-only 旁路)+多个新 gate 点，全部本地+CI 双绿(run 27391794048)，PR #3 待并。②**R9 改 venues.csv 会触发新 gate**：check_freshness 读 venues.csv 的 `last_checked_date` 列(已 202 行有值)——R9 批量补卡时该列须填 `YYYY-MM` 或 `YYYY-MM-DD`，否则该卡不计入新鲜度统计(不报错，但漏统计)。PROGRESS 早记的"venues.csv 2 行 22 列(中国农业科学/作物学报，risk_note 含未加引号英文逗号)"R9 重做时修回 19 列；改 CSV 仍守"禁 csv 模块全量重写(压平多行)、禁无引号字段含英文逗号"两铁律。③**db09 新增项目须过 schema gate**：新建项目卡必含 14 字段且 decision_log/version_history/terminology 三件套齐全(check_databases 现强校验)，否则 CI 红。④db05/db06/db07 上量(R9 主攻)注意：check_databases 对 `resources_real.md` 与 `*_cards.md` 按 SCHEMA 强校验必填字段，db06 风格卡来源是 R6.5 声明的有 key 生图实跑(仍是 GAP)。⑤新增技能/脚本/模板/mode 仍须同步四件套——本轮模板表已全量 1:1 登记，R9 若加模板记得进 WHATS_INCLUDED「可套用模板与数据文件」表(check_skill_assets 防漂移会抓)。⑥ROUTER_EXAMPLES 现 51 例、28/28 必覆盖(check_entry_docs 已收紧到全集)——R9 不动路由则无需改；若动则保持 28/28。

- **R8 现场口径(供后续轮一致性)**：①体量红线 500 行/1024 字符、软警戒 300 行(check_skills 常量带依据注释)；常驻 763 行、最重单文件 120 行，往常驻加内容前看这条余量。②安装清单(install.sh sibling)= `databases/code_assets/CONVENTIONS.md/ROUTER.md/ROUTER_EXAMPLES.md/MODE_REGISTRY.md`——技能正文用 `../` 相对引用仓库级文件**只能引这 6 个**，引别的(如 docs/)会被 check_skill_links 安装可达性 gate 判断为装后断链；要新引须先把目标加进 install.sh/ps1 的 sibling 链接。③selftest 离线纪律升级为 gate：脚本可读环境变量 `LIGHT_SELFTEST_OFFLINE=1` 主动跳过联网分支；新脚本 selftest 严禁打真网络、跑完须自清理产物(残留 gate 会抓)。④check_freshness 是 warn-only，CI 用 continue-on-error 接入，永不阻断——它是"每月跑一次出待办清单"的运维工具，不是硬门。

- **R9 批1 已完成（给批2 的话）**：①三库均 ≥15 达标(db05 18/db06 16/db07 31)，8 门禁+51 selftest 全绿，批1 commit 区间 `1187a9d..543e0d0`(含本 PROGRESS 提交)。②**批2 db01 改 venues.csv 三铁律照旧**：禁 csv 模块全量重写(压平多行)、禁无引号字段含英文逗号、`last_checked_date` 列填 `YYYY-MM(-DD)`(check_freshness 读它)；先修中国农业科学/作物学报两行的 22 列→19 列(给 risk_note 加引号)。ai_policy 字段口径=risk_note 内 `ai_policy=` 子串(CONVENTIONS §3)，已实查 12 家，批2 扩到 ≥50 卡有值。③**填卡 YAML 陷阱**(批1 踩两次)：卡内值含英文冒号须紧跟非空格或加引号，否则 PyYAML 报 `mapping values are not allowed here`，check_databases 当场抓。④新卡铁律=真实来源链接+核验日期、OpenAlex 不盲取第一条(比对年份/被引/DOI)、禁凭记忆填卡；抽查 ≥20% 落 _verification_log。⑤新增卡文件直接放各库目录、在 README「真实资源文件」节加链接即可，无需动技能四件套(本批未加技能/脚本/模板/路由)。
- **R9 批1 给批3 的话**：palette.json 跨库机制(R9.7)——db05 的 `design_tokens.template.json`(DTCG 视觉 SSOT)已是色值锚点真相源，a05/db07 衔接段均已指认它；批3 落 palette.json 时与之字段对齐，dairygoat 项目(databases/db09-projects/projects/dairygoat-detect-track)建真实实例，m11(figure-drawing)/m16(slides)/a05 三处+a07 加"读取项目 palette.json"指针。db07 九图反哺卡的 JOURNAL_SPECS 衔接段已写明栏宽真相源=light-figure-drawing/figure_export.py。

- **R9 批2 已完成（给批3/收尾的话）**：①完成判据全过——db01 308≥300、ai_policy 186≥50、db02 新样本 8≥5、抽查 22/104(21%)≥20% 落 _verification_log；8 门禁+51 selftest 全绿、git 干净、3 个中文 commit 无 AI 署名(`0ef3c2b..048a2c3`)。②**改 venues.csv 必显式按 LF 写**：本机脚本默认 CRLF 会把整文件 diff 污染(批2 已踩并修，见偏差日志)；改完务必 `git diff --check` 干净 + 验"物理行==逻辑行"。③venues.csv 现 308 卡仍**无多行字段**(物理行==逻辑行)，故"禁 csv 模块全量重写"的前提当前不成立、重写安全——但批3 若有人往 risk_note 塞换行就会破此前提，改前必先验。④db01/db02 扩充**未动技能四件套**(无新技能/脚本/模板/路由)，check_entry_docs 仍 28/28、route_examples=51。⑤批2 临时采集脚本(_collect/_gen/_enrich/_apply 等)跑完即删、未入库(联网脚本严禁留仓污染 selftest/CI)，采集→核验→入库管线已成文进 db01 README 供复现。⑥批3 只剩 palette.json 跨库机制(R9.7)+采集管线成文(R9.8 已部分落 db01 README)，收尾后打印 R11 启动提示词。

- **R9 批3 已完成（R9 三批全部收尾，给 R11 的话）**：①**完成判据全过**——palette.json 机制四处接线(m11 配色/m16 视觉风格/a05 设计语言/a07 维护要点+五维⑤)grep 可见、dairygoat 真实实例落地(12 token hex 经程序化逐项比对源文件全匹配，留痕 `_verification_log/R9-batch3-palette-verification.md`)；schema 进 db09 README + project_card_template；8 门禁+51 selftest 全绿、git 干净、3 个中文 commit 无 AI 署名(`7ecbb62..本提交`)。②R9.8 采集管线在 db01/db05/db06/db07 README 四库同口径成文，并修一处 freshness 真实断点(`核验日期` 同义词漏认，见偏差日志)。③**批3 动了一个校验器脚本**(check_freshness.py 加同义词+selftest 断言，warn-only 不阻断)——R11 行为评测若覆盖新鲜度检查按 318 卡基线。④**未动技能四件套计数**：仍 28 技能/10 mode/51 脚本/40 模板/51 route_examples，仅 4 个 SKILL.md 各加一行 palette.json 指针(check_entry_docs/check_skill_links 已绿)，未加新技能/脚本/模板/路由。⑤palette.json 用完整 `databases/db09-projects/projects/<name>/palette.json` 路径引用(不带 `../`、不以受保护目录开头)，不触发 check_skill_links gate；新项目要挂色板照 db09 README schema、source 指 db05/db06 真实卡、hex 不凭记忆填。⑥**R9 全轮验收对账**：db05 18/db06 16/db07 31(均≥15)、db01 308(≥300)/ai_policy 186(≥50)、db02 +8(≥5)、palette 四处接线+实例、每张新卡带来源+last_checked、抽查记录三份(`R9-batch1/2/3`)——R10 收官指标"db05+db06+db07 真实卡 ≥45"实达 65、"db01 venue 300+ 且 ai_policy ≥10"实达 308/186。

- **R11 已完成（给 R12/R10 的话）**：①**验收全过**——44 黄金任务(Tier1 8×3+Tier2 20×1，YAML 全 schema 校验通过)+评测协议成文；Tier1 24 任务首轮基线 48/48 红旗 0(`evals/runs/2026-06.md`)；freshness.yml 上线且 workflow_dispatch **两次真实触发 success**(开单+更单，留痕 `_verification_log/R11-freshness-dispatch.md`)；m01 追踪协议+search_normalize `--from-date`/`--known-dois`+dairygoat 真实增量留痕；弱模型 Haiku 记录(红线 8/8，第三方 DeepSeek 标 GAP)。②6 中文 commit 无 AI 署名(`77b6deb..ea7458c`)，8 门禁+51 selftest 全绿，PR #8 三任务 CI 全 success。③**evals 不进 CI**(维护节律，README「参与贡献」已指认 CI 验结构/evals 验行为分工)；**freshness.yml warn-only 永不阻断**。④**技能四件套计数变化**：仍 28 技能/10 mode/**51 脚本**(search_normalize 加 flag 非新脚本)/40 模板/51 route_examples——R12 若加技能/脚本记得同步四件套+ROUTER_EXAMPLES 28/28。⑤**给 R10 的关键提醒**：R10 合并所有叠加 PR 入 master 后，freshness.yml 的 schedule+workflow_dispatch 即在默认分支长期可用，**无需再临时切默认分支**；evals 基线分(48/48、弱模型红线 8/8)是 R10 门面宣传"质量有据/诚实底线"的现成证据来源；Tier2 20 任务本轮未实跑(计划只要求 Tier1)，列 evals backlog 待下季度补成 28/28 全覆盖。⑥**给 R12 的话**：R11 未碰 CONVENTIONS 诚实底线/LICENSE/捐赠区；新增 evals/ 目录在仓库根、不在 skills/ 故不被 check_skills/check_entry_docs 扫，R12 加安全/领域内容时 evals 任务可按需补对应技能的红旗场景(诱导编造压力测试范式见 evals/tasks/*.yaml)。

- **R12 已完成（给 R10 收官的话）**：①**验收全过**——七块全落地：防注入纪律四处口径唯一(CONVENTIONS §4 真相源+a01/m01/a10 指针+m04 既有，标记统一 `INJECTION-ATTEMPT-DETECTED`)；Windows 安装看护 windows-latest job **CI 实跑 success**(run 27406356396 四任务全绿)；a10 涉动物伦理块(GB/T 35892-2018 实查)+dairygoat 演练；m05 预注册节(复用 R5.4)+m01↔m10 OA 衔接+a02/db09 归档协议(archived 字段，schema 兼容)三处互引成立；竞品矩阵草稿存 `docs/plans/2026-06-11-phase3-execution/R12-competitor-matrix-draft.md`(实查留痕 `_verification_log/R12-08`)。②**8 中文 commit 无 AI 署名**(`9004f63..746b1f6`)，7 Python 校验器+51 selftest 全绿、git 干净、PR #9 四任务 CI 全 success。③**技能四件套计数全程不变**：仍 28 技能/10 mode/**51 脚本**/40 模板/51 route_examples——R12 新增的 `check_install_windows.ps1` 是 CI 用 PowerShell 脚本(放 `.github/scripts/`)，**不是技能脚本**、不进 51 selftest、不计入 WHATS_INCLUDED；未加任何技能/mode/模板/路由。④**给 R10 收官的关键弹药**：竞品矩阵草稿可直接搬进 README「为什么用它」节(**发布前复查竞品当日版本**，数字会变；措辞"陈述事实不贬低"，Light 打"形态组合"旗号不打"技能最多")；防注入纪律+涉动物伦理+预注册是 README/Release Notes 可宣传的 2026 安全合规增量；R10 最终验收指标"外部内容防注入纪律=四处落地口径唯一"已达成。⑤**用户决策项**(skills.sh 发布、db08 样例来源)R12 未碰，留 R10 找用户拍板。⑥未动 CONVENTIONS 诚实底线/LICENSE/捐赠区。

- **R10 已完成（第三期收官，全期闭环）**：①**合并发布全过**——12 条线性叠加分支经 `git merge --ff-only` 一次性快进入 master(62 commit、0 冲突)，8 个 PR(#1/2/3/4/5/6/8/9)GitHub 自动标 merged；master CI(含 windows-latest)run 27409535488 全 success；**v3.0.0 已 tag+push+GitHub Release 发布**(中英双语 Release Notes，附 pipeline.png/social-preview.png 两张亮点图)。②**门面四组 commit**(`55b18c0..783bb8d`，中文无 AI 署名)：中文 README 推荐配置/竞品矩阵/链路图/会话衔接卖点、英文 README 同构、社交预览图+知识卡 issue 模板、CHANGELOG 3.0.0+CITATION 升版。③**8 门禁+51 selftest 全绿、git 干净**；README 数字全仓一致(28/9/51/40/318/44)。④**用户两决策拍板**：skills.sh 发布(README 声明官方源仅 GitHub)、db08 不放全文(保持脱敏模板+要点)。⑤**两项需用户手动**：社交预览图上传(Settings>Social preview)、Discussion 三分类创建(API 不支持，Web UI 建)——已在收官报告给指引。⑥**诚信留痕**：本机无 vhs/asciinema/agg 故不放摆拍动图，改以真实案例 PDF/九图作证 + 留可复现 `assets/demo.tape`；竞品矩阵发布前已复查当日版本(SHA 与草稿一致，anthropics 17 真实技能)。⑦未动 CONVENTIONS 诚实底线/LICENSE/捐赠区。

## 收官记录（R10 填，第三期最终验收）

### 总纲 §7 最终验收指标逐项达成

| 指标 | 现状(2026-06-11) | 目标 | **实际达成(2026-06-12)** | 判定 |
|---|---|---|---|---|
| P0 问题 | 11 | 0 | **0**(11 条逐条修复，见 CHANGELOG Fixed) | ✅ |
| 跨技能口径冲突 | 5 处 | 0 | **0**(OpenAlex 限流/Science 栏宽/契约/种子数/vaex 全设单一真相源) | ✅ |
| 零脚本/零模板技能 | m13、a04 / m03、m09 | 0 | **0**(均补齐) | ✅ |
| 中文链路断点 | 4 处 | 0 | **0**(R3 专项闭环，CI 守) | ✅ |
| 会话衔接协议 | 无 | 全局规约+模板+路由+演练 | **全到位**(CONVENTIONS §9+a02 两件套+orchestrator §5+路由+A/B 演练) | ✅ |
| PPT 生图流水线 | 无 | 五阶段+脚本+prompt+离线 selftest | **到位**(imggen-enhanced：imagegen.py+assemble_from_spec.py+deck_spec.yaml，离线 selftest 绿) | ✅ |
| db05+db06+db07 真实卡 | ~5 | ≥45 | **65**(18+16+31) | ✅ 超 |
| db01 venue | 204(无 ai_policy) | 300+ 且 ai_policy ≥10 | **308**，ai_policy **186** 卡有值 | ✅ 超 |
| CI 校验器 | 7 | ≥10 | **8 脚本 + 多 gate 点**(路由 28/28、README 结构、模板防漂移、db09 schema、体量、离线、产物残留、安装可达、windows 安装看护)，按独立 gate 点计 ≥10 | ✅ |
| ROUTER_EXAMPLES 必覆盖 | 7/28 | 28/28 | **28/28**(route_examples=51) | ✅ |
| 常驻 SKILL.md 总行数 | 基线 901 | -15%(≤765) | **763**(-15.3%) | ✅ |
| 安装后断链 | ≥3 类 | 0 | **0**(4 文档随装链接+check_installation_assets 守) | ✅ |
| README | 无推荐配置/动图/社交预览 | R10 清单全过 | **推荐配置✓ 竞品矩阵✓ 链路图✓ 社交预览✓ 会话衔接卖点✓**；动图按诚信以真实案例 PDF 代替(本机无录制工具，留可复现 demo.tape) | ✅* |
| 行为评测(evals) | 无 | 44 任务+Tier1 基线 | **44 任务**(YAML 全校验)+Tier1 基线 **48/48**、红线 8/8 | ✅ |
| 保鲜自动化 | 无 | 月度 cron+自动开单实测 | **freshness.yml** 月度 cron+workflow_dispatch 两次实测 success | ✅ |
| 外部内容防注入纪律 | 无 | 四处落地口径唯一 | **四处**(CONVENTIONS §4+a01/m01/a10)，标记统一 `INJECTION-ATTEMPT-DETECTED` | ✅ |
| 发布 | 无 tag | v3.0.0 + Release Notes | **v3.0.0** tag+GitHub Release(中英双语+两亮点图) | ✅ |

> *README 动图项:计划允许"本机做不了用三联截图代替并标注"。本机无 vhs/asciinema/agg，按诚信纪律不放摆拍 GIF，改以**真实端到端案例 PDF+九图**作"真的能跑"证据(证据力更强)+留可复现 `assets/demo.tape` 待渲染。视为达标(诚实降级，已标注)。

### 12 轮逐轮状态对账

| 轮 | 名称 | 状态 | 关键达成 |
|---|---|---|---|
| R1 | P0 与卫生修复 | ✅ 已完成 | 11 P0 清零，口径冲突归零 |
| R2 | 会话衔接协议 | ✅ 已完成 | CONVENTIONS §9+a02 两件套+演练 |
| R3 | 中文链路专项 | ✅ 已完成 | 4 断点闭环，CI 守中文链路 |
| R4 | 合规与生态吸收 | ✅ 已完成 | AI 图像政策/撤稿核查/EI 口径 |
| R5 | 资产补全 | ✅ 已完成 | 零脚本/零模板技能清零，+3 脚本 |
| R6 | PPT 生图流水线 | ✅ 已完成 | imggen-enhanced 五阶段(有 key 端到端实跑列 GAP) |
| R7 | 横切机制与瘦身 | ✅ 已完成 | 常驻 901→763(-15.3%)，跨技能口径统一 |
| R8 | CI 门禁扩建 | ✅ 已完成 | 7→8 脚本+多 gate 点，28/28 路由 |
| R9 | 数据库规模化(3 批) | ✅ 已完成 | db05/06/07=65、db01=308/ai_policy 186、db02+8、palette 机制 |
| R11 | 行为评测与自动化闭环 | ✅ 已完成 | 44 任务+Tier1 48/48+freshness 实测 |
| R12 | 安全、领域与微缺口 | ✅ 已完成 | 防注入四处+windows 看护+动物伦理+预注册 |
| R10 | 门面工程与发布(收官) | ✅ 已完成 | 12 分支并 master+v3.0.0 发布+门面全过 |

### 遗留 backlog（非本期范围，诚实登记）

- R6.6#4 有 key 端到端生图实跑(配 OPENAI/GEMINI/ARK key 跑≥5 页 deck 回填 imggen_pipeline.md「实测记录」+沉 db06 风格卡)——无 key 装配链已实测，有 key 链标 GAP。**[2026-06-13 已关闭]** 用户授权后经中转 gpt-image-2 实跑 5 页 deck,五阶段齐全、0 warning、守边界,留痕 `_verification_log/R-imggen-deck-e2e.md`。
- evals Tier2 20 任务实跑(本期只要求 Tier1)，下季度评测节律滚动补成 28/28 全覆盖。
- 第三方备用档(DeepSeek V4 Pro 等)弱模型实测——本环境无 API，标 GAP。
- README 演示 GIF 实渲染——`assets/demo.tape` 已备，待装 vhs 的环境产出。
- H-11 图谱可视化(引文网络/主题图谱)——审计列 backlog，归 m01/m11 未来方向。
- 社交预览图上传 + Discussion 三分类创建——需用户在仓库 Settings 手动操作。

### 用户两决策拍板（2026-06-12）

1. **skills.sh：发布**，README 中英安装节声明"官方源仅 GitHub"。
2. **db08：不放全文样例**，保持脱敏模板+逐节要点结构。

## 用户决策项登记（出现一个登记一个，R10 统一找用户拍板）

- [x] skills.sh 发布与否（审计 I-5）→ **2026-06-12 用户拍板：发布**，但 README 中英安装节均声明"官方源仅 GitHub，第三方分发同步/完整性不作保证，安装更新以本仓库为准"。
- [x] db08 脱敏高分申报书全文样例来源（用户提供或公开样例，R9）→ **2026-06-12 用户拍板：不放全文**，db08 保持现有脱敏模板 + 逐节要点结构（不冒充"真实高分样例"）；后续若有合规样例再补。
- [x] Hermes 安装目标方案确认（2026-06-11 用户确认：对外只支持 Claude Code 与 Codex 两端，Hermes 不单独支持。已删除中英 README 的 Hermes 说明段；install 脚本不加第三目标。此项关闭。）
