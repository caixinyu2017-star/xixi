# Light 技能包全面审计报告与第三期优化计划

- 审计日期:2026-06-11
- 审计方式:六路并行深读审计(科研上游 6 技能 / 论文流水线 8 技能 / 成果工程 7 技能 / 横切常驻 7 技能+入口文档+CI+安装链路 / 9 数据库 / 2026 技能生态联网调研),全部 28 个 SKILL.md 与 references 逐文件深读,关键脚本实跑 selftest,所有 P0 结论经主审二次交叉验证(file:line 复核)。
- 对照基线:`D:/skill/Light-skills第一轮提示词.txt`(17 手动技能 + 10 常驻技能 + 9 数据库要求)。

---

## 一、总体结论:是否远超第一轮提示词

**结论:已远超,且优势集中在第一轮提示词没想到的维度;但有三个系统性弱点未达成。**

### 远超的证据
1. **点名工具吸收率接近 100%**:四组审计对提示词点名的 200+ 个参考技能/工具逐项 grep 核实,几乎全部有逐条研究笔记(含端点/参数/坑/实测日期);无法核实的(PACSOMATIC、统计建模官方细则)均诚实标注"不可考"而非编造。
2. **大量超纲硬货**(提示词未要求、自行长出的能力):
   - light-orchestrator 全链编排 + 断点恢复六探针 + passport 协议(补了原提示词"常驻技能各自为政"的结构缺口)
   - 诚实性设计体系:禁编录用率(m13)、引用三态审计(m10)、concession 让步评分抗谄媚(m04/m14)、证据闸门+借口拦截(a08)、GAP 标记文化
   - 质量门基建:7 个 CI 校验器 + 45 脚本 selftest 全覆盖 + 安装资产/入口文档/链接防漂移
   - 双向链路设计:m01 gap→m03→m04→m05→m02 回边→m06→m05/m03 回边,模板字段互相点名,是真打通的闭环
3. **生态对照**(2026-06-11 联网调研 skills.sh / anthropics/skills / DeepMind science-skills):Light 28 技能的覆盖面超过当前生态所有单一竞品套件(最接近的 lingzhi227 套件仅 6-8 技能);**投稿匹配、一致性维护、编排器、记忆管理、科研伦理在 skills.sh 上几乎无对应竞品**,属差异化优势。

### 未达成的三个系统性弱点(诚实清单)
1. **"极其庞大的数据库"未达成**:db05/db06/db07 真实卡片各只有 1-2 张;db03(109 卡)/db04(66 卡)领域集中在检测/跟踪/畜牧(用户当前项目域),其他领域是 1 卡占位 seed。
2. **中文科研链路系统性偏弱**:英文链路全闭环,但中文文献核验(m07/m10)、Word/学位论文排版(m12)、国内会议与 EI 核查(m13)、中文刊图栏宽(m09/m11)四处断点。
3. **时效性机制零自动化**:提示词要求"每月元数据/每季度分区版面费"更新,目前只有 db01 README 两行文字,无任何 freshness 检查脚本或提醒机制。

---

## 二、P0 问题清单(已逐项交叉验证,立即修)

| # | 问题 | 位置(已验证) | 修法 | 验收 |
|---|---|---|---|---|
| P0-1 | **OpenAlex 限流口径分裂**:m01 仍写"10万次/天、10/s 共享池、免 key",m03 已实测 2026 新政"需免费 API key、$1/天、看 cost_usd"。m01 是检索主技能,照做会 401/超额 | m01 references.md:80、SKILL.md:20 vs m03 references.md:212 | 把 m03 核实结论回灌 m01,m01 references 设为全包 OpenAlex 真相源单节;m04/m13 等所有调用方指向它 | `grep "100,000 次/天"` 零命中;全包口径一致 |
| P0-2 | **MDPI/中文刊栏宽死锁**:m09 限定 target_journal 只能取 JOURNAL_SPECS 六键(nature/science/cell/plos/ieee/elsevier),无 mdpi 键;db01 实有 6 个 MDPI 刊;m11 又禁止臆测栏宽并要求回 m09——互踢皮球 | m09 SKILL.md:62;m11 scripts/figure_export.py(无 mdpi);db01 venues.csv(6 个 MDPI) | figure_export.py JOURNAL_SPECS 增 `mdpi`(170mm,m09 表已有数据)+ `custom_mm` 逃生通道(中文刊用);m09/m11 文档同步 | 投 MDPI/农业工程学报场景 m09→m11 走通;selftest 过 |
| P0-3 | **Science 双栏宽两套数字**:120mm vs 121mm,散落 5 处 | m09 SKILL.md:39(120) vs m11 SKILL.md:51、figure_export.py:39(121) | JOURNAL_SPECS 定为单一真相源,文档只引用键名不重复数字;核实 Science 官方规格后统一 | 全包栏宽数字仅出现在 figure_export.py 一处 |
| P0-4 | **orchestrator 契约单向断裂**:契约表钦定 `idea_candidates.md`/`critique_verdict.md`/`PROJECT_PLAN.md`/`experiment_matrix.md`/`claim_evidence_table.md` 等工件名,但零个 m 技能 SKILL.md 提到这些名字;单技能直调时落盘名靠缘分 | orchestrator SKILL.md:64-79;grep 证实 m03 等技能内零命中 | 各 m 技能"产出"节写明标准工件名;文件名连字符/下划线统一(m05 模板 `experiment-matrix.md` vs 契约 `experiment_matrix.md`);契约表抽为 CONVENTIONS 附录双向引用 | 每个链路技能 SKILL.md 都声明自己的标准产出文件名,与契约表一致 |
| P0-5 | **安装后断链 + Claude 端路由不可达**:install 只链 skills/databases/code_assets;CONVENTIONS/ROUTER/MODE_REGISTRY 不进安装目录,11 个 SKILL.md 内 "CONVENTIONS §4/§5" 引用安装后空指;orchestrator 引用 `../../docs/design/` 同断;Codex 有 AGENTS.snippet,Claude Code 端无等效物 | install.sh:69-70;orchestrator SKILL.md:121;file-reading SKILL.md:41 等 | install 增链 CONVENTIONS.md/ROUTER.md/MODE_REGISTRY.md 三文件(或并入新 CLAUDE.snippet.md);orchestrator 的 docs/design 引用改为包内可达或移除;check_installation_assets.py 同步校验 | 模拟安装视角:技能内全部相对引用可解析 |
| P0-6 | **Hermes 无安装目标**:三端定位(Claude/Codex/Hermes)vs install.sh 只有 `both\|claude\|codex` | install.sh:24;README.md:9 | 二选一:加第三安装目标,或 README 明确声明"Hermes 复用 ~/.claude 目录"并验证 | 三端安装路径均有文档+实测记录 |
| P0-7 | **MCM 赛时自相矛盾**:同文件先写"约 96 小时"后写"99 小时" | m17 references.md:71(96) vs :76、SKILL.md:11(99) | 统一为 99 小时(2026 届实测:1/29 17:00 EST–2/2 20:00 EST) | grep "96 小时" 零命中 |
| P0-8 | **CI 模板版本漂移**:a04 模板用 checkout@v4/setup-python@v5,本仓库自身与 a03 已实测升级 v6(Node20 将于 2026-06-16 被强制切换) | a04 templates/ci.yml:18-19、references.md:278,285 | 升 v6;并把"GitHub Actions 版本真相源"定在 a03 references,a04/a06 引用 | 同包 action 版本说法唯一 |
| P0-9 | **m04 示例自相矛盾**:文件头声明"检索条目为示意",第 28 行又写"2026-06-06 实测 200"——诚实标注示范打了自己脸 | m04 examples/worked_example_dermoscopy.md:4 vs :28 | 统一:实测条目标日期留痕,示意条目明确标示意,不混写 | 同文件内声明与内容一致 |
| P0-10 | **m17 脚本污染技能目录**:roadmap_gen.py/market_charts.py 无参 selftest 把 5 张 PNG 直接落技能根目录,违反 a03 自家规矩"自测用 TemporaryDirectory 并清理" | m17 scripts/(实跑验证) | 改 TemporaryDirectory;清理已生成残留;把"selftest 不留产物"并入 CI selftest 执行器检查(见 P1-H7) | 跑全部 selftest 后 `git status` 干净 |
| P0-11 | **README 卸载指引数据风险**:Windows 下 `Remove-Item -Recurse` 删 junction 会穿透删除源仓库内容;.codex/INSTALL.md 已正确判 ReparsePoint,README 这句没警告 | README.md:93 | 加"Windows 用 `rmdir` 勿用 `Remove-Item -Recurse`"警告,与 .codex/INSTALL.md 口径对齐 | 中英 README 同步更新 |

---

## 三、P1 主题分组(第三期主体工作)

### A. 中文科研链路专项(系统性补强,最高优先 P1)
英文链路全闭环、中文链路四处断点,与提示词"中文论文"要求存在一致性缺口:
1. **m07 诚信门中文路径**:引用核查全走 DOI/Crossref/arXiv,知网/万方文献(常无 DOI)无核验路径——补"无 DOI 中文文献核对协议"(题录三字段比对:题名/作者/刊名+年卷期,留人工核对记录)。
2. **m10 中文核验兜底**:doi_to_any/verify_refs 均以 DOI 为入口;补 CNKI 题录手工 .bib 核对清单与 GB/T 7714 中文条目核对要点。
3. **m12 Word 路线深度**:目前仅 5 行(LaTeX 侧有 63 行错误对照表,Word 侧为零)——补 Word 题注/交叉引用/域更新/样式管理 checklist + 常见错误对照表;补中文学位论文模板指针(thuthesis 等;生态调研:latex-thesis-zh 技能 2.4K 安装量,证明真实需求)。
4. **m13 EI 与国内会议**:description 承诺 EI 但无 Compendex 核查路径(Engineering Village 源列表);国内会议无任何数据源。
5. **m09/m11 中文刊规格**:`custom_mm` 通道落地后,把农业工程学报等用户高频中文刊实测栏宽补进 db01/JOURNAL_SPECS。

### B. 阈值与立场统一(跨技能矛盾,半天)
1. 检索库数:m03 撞车检查"≥2 库交叉" vs m04 复核"≥1 库"——复核者标准弱于自报者,统一 ≥2。
2. 种子数:m05 "≥3~5" vs m06 必查"≥5"——按 m05 下限跑会在 m06 验收不合格;统一为"≥5,算力受限时 ≥3 且在 m06 报告显式标注"。
3. uv vs Poetry:a03 推 uv(快 10-100x)、a06 scaffold 只有 `--poetry`——a06 加 `--uv` 并设为默认,Poetry 降备选。
4. vaex 过时推荐(2023 后停止维护):a09 decision_matrix.md:13 换 DuckDB/polars streaming(表内 DuckDB 行已存在,自相矛盾)。

### C. 撤稿检测与 AI 合规(2026 投稿硬需求;生态调研证实已成头部工具标配)
1. **m10 撤稿核查**:verify_refs.py 不查 retraction;2023 起 Retraction Watch 并入 Crossref(`update-to` 字段免费)——加 high severity 检查;a10 已有 check_retractions.py,优先复用接线而非重写。
2. **m11 AI 生成图像政策**:Nature/Science/Elsevier 2023 起明令禁止生成式 AI 图像,figure_integrity.md 与投稿自查清单均未提——补一节,对接 m07 AI 声明。
3. **db01 增 `ai_policy` 字段**:2025-2026 各 venue AI 披露政策已分化(ICML/NeurIPS/Nature/arXiv 各有成文规定),a10 通用模板不够——venue 卡记录各刊政策,a10/m07 引用。
4. Turnitin AI 检测误报率数字标注"厂商自报"性质(a10 SKILL.md:30)。

### D. 资产补全(零脚本/零模板技能拉平)
1. **m03**:补 `templates/idea_card.md`(立项卡 schema,m04 复核的握手件,现在全凭散文);SKILL.md 检索步骤指向 m01 已验证脚本(search_normalize/snowball)而非教模型手拼 URL。
2. **m09**:补 `templates/figure_plan_card.md`(规划卡双层字段是关键交付物却无模板文件);PLOS 补进栏宽列表。
3. **m13**:全组唯一零脚本——补 `venue_signal.py`(输入作者名+ISSN,封装 OpenAlex Authors/Sources 查询,输出五信号对照 JSON,带 selftest)。
4. **m05**:补统计功效/样本量规划节(statsmodels `TTestIndPower.solve_power` 推算最小种子数/样本量);补算力/成本预算字段(承接 m04 rubric 维度7,放行后第一个落地环节反而不算账);可选 `plan_lint.py`(实验矩阵 EXP-Bench 四要素齐全性检查)。
5. **m06**:补配对检验(同种子同测试集比较两方法是天然配对设计,配对 t/Wilcoxon 功效更高;analyze_results.py 选择树增加配对结构识别);补切片分析协议(按子群/难度切,复用 Deepchecks `model_evaluation` 弱分段检查);AUC 类指标补 bootstrap 配对差值 CI 用法。
6. **m02**:数据增强从一行扩为 references 节(按模态:albumentations/nlpaug/时序增强,含坑);标注规范模板 + LLM 辅助标注/审核指引(2026 自建数据集主流做法);补 cleanlab(置信学习找标签错误——质量评估有"标注质量"指标却无检测手段)。
7. **a04**:references 补"研究日期/实测"标头(7 技能中唯一无时效锚点);补 `er_diagram.py`(表结构→Mermaid erDiagram,衔接 a06 版本控制);补 pgvector+HNSW 选型节与 OpenTelemetry 可观测一节(科研 AI 系统常用)。
8. **m15→m11 专利附图断链**:m15 把附图交 m11,但 m11 无专利制图规范(图号/标记线/不得着色)——m11 加"专利附图"小节,m15 指向。
9. **a03**:质量门补静态类型检查(mypy/pyright,2026 Python 工程标配缺口),scaffold pyproject 同步。

### E. 横切机制升级
1. **a08 self-review 分级执行档**:现在"任何产出交付前过全清单"对轻任务(改一句摘要)意味着 11 项全跑,实际执行中要么慢要么整体跳过失守——定义"轻任务最小三项"(证据/事实/夸大)+ 重产出全量档。
2. **a07 变更广播挂接 passport**:"定义修改立即回扫所有已产出材料"无机制支撑(已产出材料清单在哪?)——挂接 orchestrator passport 的 artifacts 列表。
3. **a01 file-reading**:补宿主原生多模态优先决策链(Claude Code 的 Read 可直读 PDF/图片,现在教 agent 一律先上 pdfplumber 绕远);补视频一节(ffmpeg 抽帧+转写工具链,提示词明确要求,目前真空);700 字工具杂烩段下沉 references。
4. **a02 memory-pm**:Hermes 会话链恢复节(单一客户端内容)从正文第一节降为 references 一行指针,减常驻死重。
5. **orchestrator**:`.light/passport.yaml` 纳入 a06 scaffold.py 与 .gitignore 模板;pipeline 声明可并行步骤(图表 m11 与引用 m10 实际可并行)。
6. **m14**:三套评审 rubric(NeurIPS 官方/ScholarEval 8 维/GRADE)补选用指引(按论文类型择一,不叠加);补 rebuttal 字数预算检查(会议 1 页限制,纯 stdlib)。
7. **m08→m14 findings JSON 接口**:findings_schema 声称喂 m14/db09,但消费侧无约定——m14 补消费说明或 m08 删承诺。

### F. 渐进披露瘦身(token 纪律;11 个常驻 description 合计约 5.1KB 是每会话固定负担)
1. m15 SKILL.md:35-41 API 参数整段与 references 大面积重复——只留一行表+指针。
2. m16 SKILL.md:35 论文转稿 300+ 字段缩两行指针(references 已有同内容)。
3. m08 SKILL.md 示例占全文 60%——下沉 examples/ 留一例。
4. a03 "资产清单防漂移/脚本自测治理"两段维护元规则移 references(与"给科研项目写后端"主旨不同层)。
5. m07 description 近 300 字信息过载稀释关键词权重——砍到能力+触发场景。
6. a09 任务→工具映射瘦身 1/3 指向 matrix;skills.sh 安装量阈值补 last_checked 标注。
7. a05 ecosystem-2026.md 中文化(全包中文文风);与 references.md 双时间锚声明以哪份为准;补 Style Dictionary/Terrazzo token 编译一行(衔接 db05 tokens)。
8. m17 SKILL.md 三段 200-400 字长难段拆 bullet;补 CUMCM 2024 起 AI 使用规定(现在只写了 MCM 的)。
9. a07 SKILL.md 移除"比 mermaid-syntax-skill 能力维度更高"自证段(对执行 agent 是噪声)。
10. m12 五个 .tex 骨架补编译验证记录(本机无 TeX 则在 CI/有 TeX 环境验一次留痕)。

### G. CI 盲区修复(防漂移基建,按价值排序)
1. ROUTER_EXAMPLES 必覆盖码从 7 个扩到全部 28 个技能码(check_entry_docs.py:183)。
2. WHATS_INCLUDED "模板与数据文件"表纳入防漂移(现在只有 scripts 表有校验)。
3. README 中英结构同步 gate(比对两文件 `##` 标题数+顺序;现在 324 行纯靠人工)。
4. db09 项目卡 14 字段 schema 纳入 check_databases.py(memory-pm 定义为"硬性"却无 gate;现存 dairygoat 项目缺 version_history.md,先补)。
5. SKILL.md 行数与 description 长度警戒 gate(当前最重 133 行/最长 626 字符,设 500 行/1024 字符红线防膨胀)。
6. 数据卡 `last_checked` 新鲜度检查:新增 `check_freshness.py`(>90 天 WARN 列清单,本地/CI warn-only,支撑提示词"每月/每季度"要求)。
7. selftest 离线性 gate(防未来脚本在 selftest 里打真网络)+ selftest 产物残留检查(跑完 `git status` 必须干净,堵 P0-10 类问题)。
8. 安装视角链接校验:check_skill_links.py 增"安装后可达性"模式(技能引用 CONVENTIONS/docs 类仓库级文件的,验证安装清单包含它)。

### H. 生态吸收清单(2026-06-11 调研,按价值排序)
1. **PRISMA 五阶段综述工作流**→m01:2026 头部工具(Paperguide/CiteDash)统一收敛为 plan→search→screen→extract→generate;m01 已有 prisma_flow.py 勾稽脚本,补"筛选(screen)/逐篇抽取(extract)"阶段协议(对标 systematic-literature-review 技能,814 装)。
2. **NSFC 立项依据写法**→m17 references 增节:研究现状评述→问题凝练→科学问题属性(对标 nsfc-justification-writer,261 装;与用户画像高度匹配)。
3. **单篇深读协议**→m01:检索后精读环节(逐节结构化读、提取假设/方法/证据链;对标 karpathy read-arxiv-paper,2K 装)。
4. **EuropePMC/bioRxiv 预印本源**→m01:DeepMind science-skills 官方套件用 OpenAlex+EuropePMC+bioRxiv+PubMed 四源并查;m01 生医纪律已有 PubMed/EuropePMC,补 bioRxiv 预印本源。
5. **灰色文献网页抓取方法**→m01:标准/政策/行业报告/竞赛方案四类源只罗列无方法(全国标准信息平台、Kaggle solutions/天池、咨询报告源的检索路径)——这同时是提示词第 1 条的明确缺口。
6. **Writefull Sentence Palette 思路**→m07 分模块要点(按语义功能给期刊真实句式)。
7. **SciencePlots 库对照**→m11(社区标准 mplstyle 集,与自有三套 mplstyle 互参)。
8. **latexdiff 返修标红流程**→m12(m14 需要 tracked changes,LaTeX 侧实现命令缺位)。
9. **Lark Slides 条目**→m16(国内协作场景真实需求)。
10. **grill-me 对抗质询句式**→m04/a08 已有等价物(反谄媚/借口拦截),仅借鉴"强制三个致命弱点、不许客套"话术,低成本。
11. **Connected Papers/ResearchRabbit 图谱视角**→m01 snowball.py 只出表,可补图谱式可视化输出(低优先)。
12. **S2 SPECTER2 embedding 语义去重**→m01(字段已记录未用)/m03(候选 idea 防伪多样)。

### I. 新技能/新方向评估(默认不加,需用户决策)
| 方向 | 生态信号 | 建议 | 理由 |
|---|---|---|---|
| 论文复现(paper2code) | 536 装;AI Scientist-v2/MARS 均以复现为核心环节 | **以 references 并入 m05**("复现已有论文"协议:复现也是一种研究方案),不新建技能 | 28 技能边界已稳(README/CI/计数全锁);需求大了再独立 |
| skill-creator 元技能 | 官方 262.9K 装 | **不做** | Light 定位是科研不是技能开发;自身维护已有 light_skill_pack_maintenance.md |
| 9 库 MCP 化 | mcp-builder 官方范式 | **观望,记 backlog** | symlink 方案工作良好;MCP server 维护成本 > 当前收益 |
| 浏览器自动化 | agent-browser 438K 装 | **依赖声明**:a09 工具选择里提"投稿系统操作可装 agent-browser",不自建 | 科研场景低频 |
| 发布 Light 到 skills.sh | 生态索引 90K+ 技能;13.4% 含安全问题(Snyk) | **用户决策项** | 获得分发 vs 维护公开承诺;吸收外部技能时只借鉴写法、不直接安装(安全) |
| 交互式工件(web-artifacts) | 官方技能 | **不做** | a05 前端已覆盖工程路线;"单文件交互式解释物"科研场景可由 a05 现有能力达成 |
| 生医领域库(PDB/UniProt 等) | DeepMind 30+ 库 | **不做,除非用户转向生医** | 用户当前方向是农业/CV |

---

## 四、数据库改进计划(逐库)

### 现状盘点(2026-06-11 精确统计)
| 库 | 真实规模 | 质量抽查结论 | 主要缺口 |
|---|---|---|---|
| db01 venues | **204 个 venue**(158 刊+46 会),18 字段与提示词逐字段对齐,risk_note 100% 非空,last_checked=2026-06 | 卡片真实(OpenAlex source ID/works_count/h_index 实测留痕;CCF 等级标来源年份) | 学科 CS 重;медицина/社科空白;无 ai_policy 字段;IF 多为 N/A(会议合理,期刊部分待补) |
| db02 writing | 模板+通用套路库(196 行)+ **20+ 篇经典论文结构化样本**(363 行) | 样本真实(含 ResNet/AlphaFold 等,有来源) | 样本偏 2012-2016 经典;缺 2024-2026 顶会新样本(LLM 时代写作风格演变);reviewer_potential_questions 字段覆盖不全 |
| db03 methods | **~109 张方法卡**,maturity(经典/主流/新兴/过时)全标注,DOI+被引数实测 | 抽查高质量(可直接支撑 m03/m04 判断) | 领域集中:检测/跟踪/动作/夜间 ≈82 张,其他领域 1-8 张占位;last_checked 覆盖率低(部分文件仅 1 处) |
| db04 datasets | **~66 张数据集卡**,license/bias_risk/privacy_risk 字段齐 | 抽查真实(畜牧 19+CV/NLP 18+frontier 20) | 同 db03 领域集中;更新机制无 |
| db05 frontend | 模板+canonical 索引,**真实卡仅 1-2 张** | 设计系统卡/token 模板质量好 | **规模与提示词"庞大"差距最大**;与 a05 references/design-systems-map.md 职责重叠待声明 canonical |
| db06 ppt | 同上结构,**真实卡 1-2 张** | themes.py 十主题与卡对齐已验证 | 同 db05 规模缺口 |
| db07 figures | 模板+advanced 卡,**真实卡 2 张** | canonical 入口纪律已建立 | 提示词点名 18 种图型,现覆盖 2 种 |
| db08 ip | 34 个 heading 块:材料卡+扩展卡+预算模板+案例骨架 | 骨架可直接套用 | 缺 1 份脱敏高分申报书全文样例 |
| db09 projects | 1 个真实项目(dairygoat)+lessons 2 条+模板 | 结构健康,被 26 个技能挂载(全包枢纽) | 无 CI schema 校验;dairygoat 缺 version_history.md |

### 改进动作
1. **规模化策略(核心原则:按需生长+每用必沉,拒绝盲目铺量)**:
   - db05/db06/db07 设本期目标**各 ≥15 张真实卡**:db05 按风格谱系(科技感/学术感/玻璃拟态/大屏/管理系统/移动端等 10 风格 × 1-2 卡);db06 按场景(答辩/路演/汇报/商业计划等 8 场景);db07 按图型(提示词点名的折线/柱状/箱线/热力/雷达/散点/误差棒/混淆矩阵/ROC/PR/消融/敏感性/框架图/流程图/数据集示意/可解释性/真实效果图)。
   - 来源协议:每次 m11/m16/a05 实际产出后强制沉卡(orchestrator 链路终点加钩子;a07 验收时检查);批量补卡时走"采集→人工核验→入库"管线,核验标准沿用 OpenAlex 卡片核验注意(不盲取第一条,比对年份/被引/DOI 合理性)。
   - db03/db04 不盲目铺全领域:每立项一个新方向时批量补 15-25 张该域卡(与 m01 调研产出联动)。
2. **字段补全**:db01 增 `ai_policy`(C-3);db03 补 last_checked 全覆盖;db02 样本卡补 reviewer_potential_questions。
3. **新鲜度机制**:新增 `check_freshness.py`(G-6),月度人工跑一次,>90 天的卡列清单;README 的"每月/每季度"承诺改为指向该脚本的可执行流程。
4. **内容更新**:db02 补 5-10 篇 2024-2026 顶会结构样本;db01 按用户实际投稿方向补医学/交叉学科 venue(目标 204→300+,不追求绝对数量追求方向命中)。
5. **跨库统一**:新增共享色板 token 方案——db09 项目卡旁挂 `palette.json`,m11(论文图)/m16(PPT)/a05(前端)三方共读,解决"slides 与 figure 风格统一靠 a07 人工把关"的问题;db05 tokens 模板与之对齐。
6. **db09 治理**:14 字段 schema 进 CI(G-4);补 dairygoat version_history.md;lessons.md 持续沉淀(现 2 条,质量好)。

---

## 五、分轮执行计划

> 每轮收尾必须全量过门禁:6 校验器 + 45 selftest + 静态扫描 + `git diff --check`,重大改动加独立审查;提交按用途分组、中文 message、不带 AI 署名;推送后看 CI 绿。

### R1|P0 修复轮(预计半天)
二章 11 项逐个修。顺序:P0-1 口径(影响面最大)→ P0-2/3 栏宽(连带)→ P0-4 契约(动 6 个技能的产出节)→ P0-5/6 安装(动 install+校验器)→ P0-7/8/9/10/11 杂项。
**验收**:每项的验收列全过;CI 绿。

### R2|中文链路专项轮(预计 1 天)
三章 A 组 5 项。m07 中文核对协议、m10 兜底清单、m12 Word checklist+错误对照表+学位论文指针、m13 EI+国内会议、中文刊栏宽数据落 db01。
**验收**:用一篇虚构中文论文场景走 m07→m10→m12→m13 全链,无"仅英文可用"断点。

### R3|撤稿+AI 合规+生态高价值吸收轮(预计 1 天)
三章 C 组 4 项 + H 组 1-5 项(PRISMA 阶段化/NSFC/单篇深读/bioRxiv/灰色文献方法)。
**验收**:m10 verify_refs 对已知撤稿 DOI 报 high;db01 ai_policy 字段有 ≥10 个头部 venue 实查记录;m01 五阶段协议有 worked example。

### R4|资产补全轮(预计 1-1.5 天)
三章 D 组 9 项(m03 立项卡模板/m09 规划卡模板/m13 脚本/m05 功效+预算/m06 配对+切片/m02 增强+标注+cleanlab/a04 脚本+标头/m15→m11 附图/a03 类型门)。
**验收**:新增脚本全部带 selftest 并登记 WHATS_INCLUDED;零脚本技能清零(m13/a04);新模板被对应 SKILL.md 引用且 check_skill_links 过。

### R5|横切机制+瘦身轮(预计 1 天)
三章 E 组 7 项 + F 组 10 项。注意瘦身动 description 时同步跑 check_skills.py/check_entry_docs.py。
**验收**:11 个常驻 SKILL.md 总行数下降 ≥15%;a08 有轻/重两档且 orchestrator checkpoints 引用;`.light/` 进 scaffold。

### R6|CI 盲区轮(预计 1 天)
三章 G 组 8 项。新校验器逐个上线(每个先本地全绿再进 CI),check_freshness 为 warn-only。
**验收**:ROUTER_EXAMPLES 必覆盖 28/28;README 中英结构 gate 上线;db09 schema 进校验;selftest 产物残留检查上线(用 P0-10 的修复回归验证)。

### R7|数据库规模化轮(持续,分 2-3 批)
四章动作 1-5。第一批:db05/06/07 各补到 ≥15 卡(走采集→核验→入库管线,每张卡须有真实来源链接+核验日期);第二批:db02 新样本 + db01 ai_policy 与方向扩充;第三批:palette.json 跨库方案。
**验收**:check_databases.py 扩展后全绿;抽查 20% 新卡来源可访问、数据与来源一致。

### R8|决策与发布轮(等用户拍板)
三章 I 组决策项:paper2code 并入 m05 与否、skills.sh 发布与否、Hermes 安装目标方案。完成后更新 CHANGELOG、README 数字、WHATS_INCLUDED,打 tag。

### 轮次依赖与并行性
- R1 必须最先(P0 里有口径/契约这类影响后续所有轮的基础)。
- R2/R3/R4 互相独立可乱序;R5 的瘦身建议在 R4 资产补全之后(避免同文件反复改);R6 随时可插,但 G-7(selftest 产物检查)依赖 P0-10 先修;R7 独立可与任何轮并行。

---

## 六、效果指标(本期结束时验收全包)

| 指标 | 现状 | 目标 |
|---|---|---|
| P0 问题 | 11 | 0 |
| 跨技能口径冲突(OpenAlex/栏宽/种子/检索库数/uv) | 5 处 | 0 |
| 零脚本技能 | m13、a04(m03/m09 零模板) | 0 |
| 中文链路断点 | 4 处 | 0 |
| db05+db06+db07 真实卡 | ~5 张 | ≥45 张 |
| CI 校验器 | 7 个 | 10+(freshness/db09/同步 gate) |
| ROUTER_EXAMPLES 必覆盖 | 7/28 | 28/28 |
| 常驻 SKILL.md 总 token | 基线待量 | -15% |
| 安装后断链 | ≥3 类 | 0(含安装视角校验) |

---

## 附:本次审计的方法论沉淀(供 light_skill_pack_maintenance.md 吸收)
1. 多路并行分组深读 + 主审对 P0 二次交叉验证(防审计代理误报),是 28 技能规模下唯一可行的全量审计方式。
2. 审计发现的最大风险类别不是"内容错",而是:**跨技能口径分裂**(同一事实两套说法)、**单向挂载**(A 声明 B 消费,B 不知道)、**安装视角断链**(仓库内有效、装完失效)。后续新增内容时,这三类要在写入时就检查。
3. 生态调研结论:科研垂直技能安装量普遍 30-3K,Light 的差异化(编排/一致性/诚实性)无竞品;吸收外部技能只借鉴写法、不直接安装(13.4% 含安全问题)。
