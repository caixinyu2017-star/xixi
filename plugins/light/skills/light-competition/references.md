# light-competition 参考工具研究笔记

逐工具核查笔记。每条尽量给真实链接、可复用方法。查不到可靠信息的明确标注"未能核实"。

> **last_checked: 2026-06**（时效字段单一维护点；与 [`references/competition_rules_cn.md`](references/competition_rules_cn.md) 顶部同步）。各赛事组别/重点领域/评分细则逐年改且本环境网络受限无法实时核实——动笔前以当届官方《评审规则》压缩包为准，按 competition_rules_cn.md 的 rules_checklist 勾选确认。
> 调研日期：2026-06-06。

---

## 中国国际大学生创新大赛（原"互联网+"）

**【是什么】** 教育部主办的最高规格双创赛事，2024 年起由"互联网+大学生创新创业大赛"更名为"中国国际大学生创新大赛"。

**【可复用方法/真实赛制】**
- 高教主赛道按学历分**本科生组**和**研究生组**，每组下设**创意组**（有创意未注册公司或注册≤3年未盈利）和**创业组**（已注册公司）。2024+ 已淘汰旧的"初创组/成长组/师生共创组"名称。
- 重点领域导向：新工科、新医科、新农科、新文科、人工智能+、低空经济、生物技术、量子科技、新能源、新材料。
- 提交物=**商业计划书 + 路演 PPT + 答辩**。评审看：创新性、团队、商业/社会价值、带动就业、可行性、引领性。
- 官方"评审规则"和"学生操作手册"以压缩包形式在官网"资料下载"发布，每年更新，写材料前务必下最新版对齐评分项。

**【链接】** https://cy.ncss.cn/ （评审规则下载入口在站内"资料下载"）

**【已知坑】** 组别名称和重点领域逐年改；不要套旧届模板。市场规模数据须可核查。

---

## 挑战杯

**【是什么】** 共青团中央等主办的"中国大学生系列科技学术竞赛"，含**两个并列主体竞赛**，交替举办、各两年一届。

**【可复用方法】**
- "大挑"=**全国大学生课外学术科技作品竞赛**，作品分三类：①自然科学类学术论文；②哲学社会科学类社会调查报告和学术论文；③科技发明制作（A类侧重技术含量、B类侧重实用创新）。评学术创新、研究深度、成果价值。
- "小挑"=**"挑战杯"中国大学生创业计划竞赛**（建设银行冠名），围绕"科技创新和未来产业""社会治理和公共服务"等赛道，提交创业计划书+答辩。
- 二者评审重点不同：大挑偏学术，小挑偏商业可行性。写材料先确认是哪一杯。

**【链接】** https://www.tiaozhanbei.net/

**【已知坑】** "大挑/小挑"常被混淆；哲社类社会调查须有一手调研数据和规范方法。

---

## 大学生创新创业训练计划（大创）

**【是什么】** 教育部"国家级大学生创新创业训练计划"，国家级/省级/校级三级。

**【可复用方法】**
- 三类项目：**创新训练项目**（学生团队做研究）、**创业训练项目**（模拟创业全过程、写商业计划书）、**创业实践项目**（真实创办企业）。
- 全流程：申报立项 → 中期检查 → 结题验收。申报书核心模块：立项依据/研究意义、国内外现状、研究内容与目标、技术路线/方案、可行性分析、创新点、进度安排、预期成果、经费预算、团队分工与基础。
- 重培养价值（学生主体、过程性成长），不只看结果。

**【链接】** 国家级平台 https://gjcxcy.bjtu.edu.cn/ （部分校外访问证书异常，以本校教务通知为准）

**【已知坑】** 经费预算须分类合理（材料费/测试费/差旅/版面费等），与研究内容匹配，不可堆砌。

---

## 数学建模国赛 CUMCM

**【是什么】** 全国大学生数学建模竞赛（高教社杯），中国工业与应用数学学会主办，三天封闭、三人一队完成一篇论文。

**【可复用方法/论文结构】**
- 论文标准结构：摘要（关键，单独一页，含问题/方法/结论/特色，决定初筛去留）→ 问题重述 → 模型假设 → 符号说明 → 模型建立与求解 → 结果分析与检验 → **灵敏度分析** → 模型优缺点 → 改进方向 → 参考文献 → 附录（代码）。
- **两级评审**：先赛区评阅，优秀者送全国评阅。评委首先看摘要和结果，再看模型与求解。
- 复用要点：摘要要把模型名称、关键结论数字写清楚；每问要有"模型→求解→检验"闭环；附录放完整可复现代码。

**【链接】** http://www.mcm.edu.cn/ ；范例与经验 https://github.com/MATHmodels/CUMCM

**【已知坑】** 评委时间有限，摘要写不好直接出局；灵敏度分析和误差检验最容易被忽略却是拉分项。

---

## 数学建模美赛 MCM/ICM

**【是什么】** COMAP 主办的美国大学生数学建模竞赛，MCM（A连续/B离散/C数据）+ ICM（D运筹网络/E环境/F政策），三人队、99 小时赛程（见下「赛程 99 小时」条赛历）、英文论文。

**【可复用方法/已核实硬规则（2026 届 contest instructions）】**
- **页数硬上限 25 页**：包含 Summary Sheet + 正文 + 参考文献 + 目录 + 注释 + 附录 + 代码，全部计入。唯一例外是 **"Report on Use of AI"**（AI 使用说明）章节，不计页数也不计入 25 页——但必须如实写。超页直接出问题。
- **Summary Sheet 必须是报告第一页**，评委给极高权重，"获奖论文常靠摘要质量与他人拉开差距"。官方明确告诫：摘要不要写成问题重述、也不要从引言里复制粘贴；建议最后写，须讲清方法与最重要结论。
- **赛程 99 小时**：2026 届为 1/29 17:00 EST 至 2/2 20:00 EST，之后再给 1 小时上传 PDF。三人一队。
- **奖项层级（由低到高，官方无"及格线/分数线"，按完成度评级）**：Successful Participant（有努力但要求回应不全/建模有缺陷）→ Honorable Mention（高于平均、过程有据）→ Meritorious（多方面优秀、清晰有据有组织）→ Finalist（进入最终轮、属全体最佳之一）→ Outstanding Winner（最终轮"best of the best"）。官方未公布各档百分比。
- 题型：MCM A 连续/B 离散/C 数据洞察；ICM D 运筹网络/E 可持续/F 政策。
- 复用：英文摘要重于一切；图表/可视化质量影响评分；C/E/F 题需扎实数据处理与现实解释。

**【链接】** https://www.comap.com/contests/mcm-icm ；规则原文 https://www.contest.comap.com/undergraduate/contests/mcm/instructions.php

**【已知坑】** 把附录代码当"页外内容"是常见误区——除 AI 说明外一切计入 25 页。英文写作和摘要是中国队最大短板；AI 使用说明现为必填项，瞒报有风险。

---

## 全国大学生统计建模大赛

**【是什么】** 中国统计教育学会主办（曾"东证期货杯"冠名），偏真实数据的统计分析与实证建模。

**【可复用方法】**
- 完整提交=数据预处理 + 多模型对比 + 论文。常见做法：对同一问题用多种方法（逻辑回归、岭回归、SGD、决策树、神经网络等）对比并解释优劣。
- 比数学建模更强调**数据来源真实、变量解释、统计推断的严谨性和现实意义**，而非纯算法炫技。

**【链接】** 参赛范例仓库 https://github.com/HandsomeBrotherShuaiLi/National-University-Student-Statistical-Modeling-Competition

**【已知坑】** 官方论文格式/字数/选题细则未在公开范例中给出（**官方细则未能核实**，以当届通知为准）；重数据合规与可解释性。

---

## 商业计划书 / 精益画布 Lean Canvas

**【是什么】** Ash Maurya 在 Osterwalder 商业模式画布基础上改造的创业单页工具，更适合早期高不确定项目。

**【可复用方法/九宫格】**
1 Problem（前3大痛点）｜2 Solution｜3 Key Metrics｜4 Unique Value Proposition｜5 Unfair Advantage（难复制壁垒）｜6 Channels｜7 Customer Segments｜8 Cost Structure｜9 Revenue Streams。
- 相对商业模式画布，Lean Canvas 用 Problem/Solution/Metrics/Unfair Advantage **替换**了 Key Partners/Key Activities/Key Resources/Customer Relationships 四格，聚焦风险与验证。
- 复用：路演前先填一页 Lean Canvas 自检逻辑闭环，再展开成完整商业计划书。

**【链接】** https://guides.lib.unc.edu/lean-canvas ；理论出处《Running Lean》(Ash Maurya)

**【已知坑】** Unfair Advantage 最难填且最关键，"先发/团队/资源"常被误当壁垒；市场规模须真实测算。

---

## Market Research Reports skill（k-dense-ai/scientific-agent-skills）

**【是什么】** k-dense-ai《Claude Scientific Skills》"Research Methodology & Planning"类下的真实 skill（**已核实**，与 Light 同源）。产出咨询级(50+页)市场研究报告，LaTeX 编译成 PDF，对标 McKinsey/BCG/Gartner 交付物。

**【可复用方法/五阶段 pipeline 与框架】**
- **五阶段**：①研究取数(定边界/地域/时段，结构化查询取市场规模·竞品·趋势·监管，按章归入 `sources/`)→②框架分析(TAM/SAM/SOM + 波特五力 + PESTLE + SWOT + BCG 矩阵；**每个力/维度按 High/Medium/Low 评级并写 rationale**)→③**先批量出 6 张核心图再动笔**(增长曲线、TAM/SAM/SOM、五力图、竞争定位矩阵、风险热图、高管信息图)→④写作(11 章+前后页，统一 `.sty` 样式)→⑤编译(xelatex+bibtex 三遍)+清单校验。
- **TAM→SAM→SOM 分层同心圆**：TAM=100%份额时总营收机会；SAM=受产品/地域约束的可服务部分；SOM=竞争态势下近期现实可获份额。**每层假设进一个"假设登记表"让评审能直接质疑输入**；配敏感性/情景分析。
- **竞品四透镜**：波特五力(行业结构吸引力，逐力评级)、市场份额(Top10营收与份额%)、竞争定位 2×2 矩阵、战略群组聚类；进入壁垒/供方买方议价/替代威胁显式打分。
- **评审/质量清单(可做自审)**：结构完整(11章+附录+自动TOC/LOF/LOT)、视觉完整(6核心图+章节图)、**数据质量(有出处、假设登记、数据≤2年)**、写作(客观/精确/无占位符)、技术(干净编译、交叉引用有效、文献齐全、50+页)。
- 可复用招式：批量预生成图框定叙事；参数化查询模板(同一 prompt 套不同市场取规模/竞品/趋势/监管)；框架评级表(H/M/L 或 1–5 + 强制 rationale)；语义命名色块环境(insight/data/risk/recommendation)给内容分层。

**【补充：社区 7 步法(openclaw market-research-2，已核实)】** 定 3–5 研究问题→TAM/SAM/SOM(无现成报告用第一性原理：人口基数×转化过滤×现实 ARPU，再用竞品营收交叉校验；SOM 年潜收<$500K 视赛道偏小)→免费数据源(行业报告/Statista/SEC/统计局；定价页/G2·Capterra评论≥20条/SimilarWeb/Crunchbase 看竞品；Google Trends/Reddit/PH/YC 看趋势)→竞品图谱5–7家提炼 table stakes/普遍空白/未服务细分→趋势3–5条(证据/成熟度/顺逆风/行动)→客户画像2–3个(基于真实评论语言)→汇总单文档+编号下一步。

**【链接】** https://playbooks.com/skills/k-dense-ai/scientific-agent-skills/market-research-reports ；7步法 https://playbooks.com/skills/openclaw/skills/market-research-2

**【已知坑】** TAM 易自上而下虚高，必须用竞品营收/SEC 交叉验证；数据须≤2年且标出处；评论挖掘要够样本量；竞赛路演不必凑50页，但"假设登记+交叉校验+逐力评级"的严谨度直接抄。

---

## to-prd（产品需求文档技能，mattpocock/skills）

**【是什么】** 把已有上下文综合成 PRD 的工程 skill（不访谈用户，从对话+代码库综合）。

**【可复用方法/PRD模板】** Problem Statement（用户视角）→ Solution（用户视角）→ User Stories（详尽编号"As a… I want… so that…"）→ Implementation Decisions（模块/接口/架构/schema/API，不写文件路径或代码）→ Testing Decisions → Out of Scope → Further Notes。流程：先探仓库 → 找测试切入点并与用户确认 → 写 PRD 入 issue tracker 打 `ready-for-agent` 标签。

**【链接】** https://github.com/mattpocock/skills/blob/main/skills/engineering/to-prd/SKILL.md

**【已知坑】** 适合工程项目立项书的"问题-方案-范围"骨架；"Out of Scope"显式排除是防范围蔓延的关键。

---

## writing-plans（obra/superpowers）

**【是什么】** 把 spec/需求转成逐步可执行实施计划的 skill，处于 brainstorm → write-plan → execute 流水线中段。

**【可复用方法】** 计划=Header（一句话目标 + 2–3句架构 + 技术栈 + 指向执行）+ Tasks。每个 task 列出确切文件，按严格 TDD 拆成 2–5 分钟一步（写失败测试→跑确认失败→最小实现→跑确认通过→提交）。原则 DRY/YAGNI/TDD/频繁提交；自底向上；假设读者零上下文，写确切命令与预期输出，**不写时间估算**，只写相对粒度。

**【链接】** https://obra-superpowers.mintlify.app/skills/writing-plans ；https://github.com/obra/superpowers

**【已知坑】** 用于大创/项目"进度安排+技术路线"：把里程碑拆成可验证小步，每步有交付物，比笼统"第一阶段调研"更经得起评审。

---

## content-strategy（内容策略 skill）

**【是什么】** 规划"做什么内容"的 skill：内容支柱 + 主题优先级。

**【可复用方法/已核实】** ①收集上下文(业务/客户研究/现状/竞争)；②定 3–5 个**内容支柱**(四透镜：产品导向/受众导向/搜索导向/竞品导向)；③六源选题(关键词数据/通话记录/问卷/论坛/竞品/销售支持)；④按**加权打分**排序：客户影响 40% + 内容市场契合 30% + 搜索潜力 20% + 资源需求 10%(各项1–10分×权重求和，如 8/9/7/6→总分8.0)；⑤映射买家阶段(认知"what is/how to"→考虑"best/vs/alternatives"→决策"pricing/reviews/demo"→落地"templates/tutorial/setup")；⑥输出支柱→优先主题→主题集群图。内容分 searchable(接需求，默认优先)与 shareable(造需求：新数据/反直觉/故事)，"搜索流量是地基"。

**【链接】** https://playbooks.com/skills/insight68/skills/content-strategy

**【已知坑】** 用于路演/项目传播叙事时，可借"加权打分"法对卖点排序，避免平铺直叙。

---

## PPTX skill（Anthropic 官方）

**【是什么】** Anthropic 官方文档 skill，生成/编辑 .pptx。

**【可复用方法/三模式】**
- 读：`python -m markitdown x.pptx` 抽文本；`scripts/thumbnail.py` 出缩略图总览。
- 改模板：unpack（pptx 即 zip）→ 直接改 XML → repack，保模板版式。
- 从零建：用 **PptxGenJS（Node）** 而非 python-pptx。
- **视觉 QA 闭环（最值得借鉴）**：soffice 转 PDF → `pdftoppm -jpeg -r 150` 逐页转图 → 用"新眼睛"subagent 检查重叠/对比度/溢出/残留占位 → 修 → 只重验受影响页 → 直到无新问题。还用 `markitdown | grep -iE "xxxx|lorem|ipsum"` 查残留占位符。

**【链接】** https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md

**【已知坑】** 一次修改常引入新问题，必须重新渲染验证；占位符文字残留是低级失分点。

---

## Scientific Slides（学术演示：assertion-evidence + Beamer 全生命周期）

**【是什么】** 任务点名的"Scientific Slides"在 k-dense-ai《Claude Scientific Skills》"Scientific Communication"类下确有同名 skill（**已核实存在**，与 LaTeX Posters/PPTX Posters 同组；其 SKILL.md 细节未逐字抓取）。下面的可复用方法补以**已核实的 Noi1r/beamer-skill**（功能更具体）与 Michael Alley 的 assertion-evidence 方法学。

**【可复用方法/已核实】**
- **Assertion-Evidence（Michael Alley, Penn State）**：每页标题写一句**完整断言**(结论句)而非短语主题；正文用图表/示意图等**视觉证据**支撑，去掉 bullet 堆砌。模板见 hplgit/MAlley-slide-templates。
- **Beamer 全生命周期(beamer-skill 五阶段)**：`create→compile→review→polish→verify`。create 含 材料分析→需求访谈→结构计划(带时长)→起草→质量环(迭代到评分阈值)。compile=**3 遍 XeLaTeX+bibtex**+编译后诊断。
- **评审动作矩阵(可直接当答辩幻灯自审清单)**：`review`(只读校对：语法/错字/溢出/一致性/学术质量)、`audit`(版面：溢出/字体/框/间距)、`pedagogy`(13条教学验证：先 Why 后 What、密度上下界"每页≤7 bullet/2 公式/5 符号"且"每页都要值得存在"、按时长分配页数、自动备份附录应对 Q&A)、`tikz`(图用 `\pgfmathsetmacro` 不硬编码近似)、`excellence`(多维质量)、`devils-advocate`(对抗式质疑设计)、`visual-check`(基于 PDF 视觉核验)。
- **扣分制评分**：从 100 起，按违规逐项扣，阈值 Excellent/Good/Needs Work/Poor，每轮起草后自动跑。
- **视觉/结构硬约束**：不用 overlay(`\pause/\onslide/\only`)，改用多页+颜色强调；色盲安全语义色 `\pos{}/\con{}/\HL{}` 且 WCAG AA 对比≥4.5:1；Beamer 在 block 内会吞溢出警告，须靠视觉 audit 抓；XeLaTeX、16:9、10pt。
- **关键复用模式**：①审改分离(只读出"位置/现状/建议/严重度"结构化报告，改在另一步)；②硬约束可机检(页数区间/禁用命令/必备章节程序化断言)；③内容密度设上下限防过载与灌水；④devil's-advocate 专设对抗轮。

**【链接】** Scientific Slides 同源仓库 https://github.com/K-Dense-AI/scientific-agent-skills ；beamer-skill https://github.com/Noi1r/beamer-skill ；assertion-evidence https://www.assertion-evidence.com/ ；模板 https://github.com/hplgit/MAlley-slide-templates ；Beamer 教程 https://www.overleaf.com/learn/latex/Beamer

**【已知坑】** 默认"主题短语+一堆 bullet"是最常见反模式；公式/图占位需预留避免溢出；overlay 在打印/讲义模式易乱，beamer-skill 索性弃用改多页+颜色。

---

## python-pptx（库，补充）

**【是什么】** 读写 .pptx 的 Python 库（与官方 PPTX skill 的 PptxGenJS 路线不同的另一选择）。

**【可复用方法】** 层级 `Presentation → slide_layouts → add_slide → placeholders/shapes → text_frame → paragraph/run → font`。单位 `Inches()/Pt()`、颜色 `RGBColor`；`add_table`、`add_chart(XL_CHART_TYPE..., CategoryChartData)`。最小流程见官方文档。

**【链接】** https://python-pptx.readthedocs.io/

**【已知坑】** 对复杂版式/精细排版控制不如直接改 XML；图表类型有限。

---

## Research Grants skill（科研基金申请，k-dense-ai/scientific-agent-skills）

**【是什么】** k-dense-ai《Claude Scientific Skills》"Research Methodology & Planning"类下的真实 skill（**已核实**，与 Light 技能同源生态）。生成贴合机构格式、评审标准、合规要求的竞争性基金申请书。

**【可复用方法/真实结构与评审维度】**
- 覆盖机构：**NIH**(R01/R21/R03/R15/R35/F30·F31·F32/K99·R00 等)、**NSF**(Standard/CAREER/RAPID/EAGER)、**DOE**、**DARPA**、**NSTC**(台湾，CM03 表、双语摘要)。
- 提交时间线（可借来排大创/基金进度）：立项准备(提前2–6月，找机会+攒前期数据+列 aims)→起草(提前2–3月，先写 aims 再写正文/图/预算)→内审 mock review(提前1–2月)→定稿(提前2–4周)→提交(提前48小时上传校验)。
- 申请书结构：摘要(NIH 30行/NSF 1页)→**Specific Aims**(1页：知识缺口开场→长期目标与近期目标→中心假设→2–4个 aims，每个含 rationale/工作假设/方法概要/预期产出→收尾"payoff"段；原则"aims 彼此独立但互补、且在时间预算内可完成")→Significance→**Innovation**(五维：概念/方法/整合/转化/规模)→Approach(每个 aim 的设计·样本量·统计功效·分析计划·质控·备选方案；NIH R01 正文12页含 Sig+Innov+Approach)→Preliminary Data(降低评审感知风险)→Broader Impacts(NSF 五领域，须具体活动非空话)→Timeline(里程碑+go/no-go)→Team→Budget & Justification(逐项对齐研究计划)。
- **评审打分维度（直接可做自审清单）**：NIH 1–9 分(1最优)评 Significance/Investigator/Innovation/Approach/Environment；NSF 两项等权 Intellectual Merit + Broader Impacts；DARPA 技术merit+使命契合+成本现实性；NSTC 创新性/可行性/主持人能力/价值。
- 复用提示结构：**Hook→Problem→Solution→Evidence→Impact→Team**；主动用 contingency 段回应风险；保证 预算↔活动↔时间线↔人员 内部一致。Resubmission：1页 intro 列被批评点+逐条改动+强化前期数据。
- 反模式：超页、目标含糊、预算与计划不符、前期数据不足、Broader Impacts 空泛。

**【链接】** https://playbooks.com/skills/k-dense-ai/scientific-agent-skills/research-grants ；仓库 https://github.com/K-Dense-AI/scientific-agent-skills

**【已知坑】** 与大创/挑战杯申报书的"立项依据-研究内容-可行性-预期成果"高度同构可互借，但具体机构(国自然/NSF/NIH)评审项差异大，按目标机构指南对齐。Specific Aims 是 NIH 体系命门，写不好整本被毙。

---

## NSFC / 纵向项目立项依据写法

> 上面 Research Grants skill 给的是 NIH/NSF 体系结构；本节专补**国自然（NSFC）立项依据**的中文写法要点——它最易写垮的不是格式而是"立项依据"那几段。对标社区 nsfc-justification-writer 技能（仅学结构，不抄文本）。立项依据=研究现状评述 → 问题凝练 → 科学问题属性，三段递进，环环相扣。

### 1. 研究现状评述：要"评"不是"堆"
- **失败相**：把文献按时间/作者罗列成流水账（"A 做了…，B 做了…，C 做了…"），不下判断。这是国自然函评最常见的扣分点。
- **正确相**：按**问题脉络**而非作者组织——这个方向的核心矛盾是什么、已有路线分几派、各派的关键进展与**未解决的硬骨头**。每段落脚到"还缺什么"，为下文的问题凝练铺垫。评述里要有你的**判断**（哪条路线更有前景、为什么某个瓶颈至今未破）。
- 落地：用 m01(light-literature-search) 的检索+深读卡产出脉络，但写立项依据时**重组为"问题演进"叙事**，不是综述的"方法分类"叙事。

### 2. 问题凝练：从"领域很重要"收到"一个具体科学问题"
- 漏斗：领域意义（1-2 句，别长篇大论）→ 现状评述揭示的关键缺口 → **凝练出 1 个核心科学问题**（可被研究内容直接回应的、具体到能设计实验的问题）。
- 检验：你的"研究内容/目标"是否逐条对应这个核心问题？对不上=问题大而空或内容跑偏。问题与内容**脱节**是第二大失败模式。

### 3. 科学问题属性（国自然特有，须选准）
2020 起 NSFC 申请要求选 1 类科学问题属性，并在立项依据里**论证为何属于该类**（选错或论证不到位直接影响分流评审）：
- **鼓励探索、突出原创**：从 0 到 1 的原创设想，无现成路径。
- **聚焦前沿、独辟蹊径**：紧跟国际前沿但走出差异化路线。
- **需求牵引、突破瓶颈**：由国家/产业实际需求倒逼的关键技术瓶颈。
- **共性导向、交叉融通**：多学科共性问题、交叉融合。
- 选属性 = 给评审定调你的项目"该用哪把尺子量"。属性要与现状评述、问题凝练**自洽**（如选"需求牵引"，现状评述就该突出需求与瓶颈，而非纯理论空白）。

### 常见失败模式（自审清单）
1. 现状综述无批判性——只堆不评，看不出缺口（最高频）。
2. 问题大而空——"研究 XX 的机理"宽到无法证伪/无法在周期内完成。
3. 问题与研究内容脱节——内容回答的不是凝练出的那个问题。
4. 科学问题属性选错或不自洽——属性与依据/内容调性不符。
5. 创新点与现状评述断裂——说自己创新，但前文没铺出"别人没做到"的对照。

> 诚实边界：NSFC 指南**逐年修订**，科学问题属性的四类表述与申报要求以**当年度项目指南**为准；本节为结构方法论，写材料前务必下当届官方指南核对。对标的 nsfc-justification-writer 仅借其"依据三段式"结构，不抄其任何模板文本。


---

## 调研诚实声明

- **充分核实并提炼可复用方法**：MCM/ICM(25页硬限/99小时/摘要权重/奖项分级/AI说明，核到官方 contest instructions)、Research Grants skill(k-dense-ai，真实存在，结构+5机构评审维度齐)、Market Research Reports skill(k-dense-ai，真实存在，五阶段+框架评级+假设登记)、Scientific Slides(k-dense-ai 真实存在) + beamer-skill(Noi1r，五阶段/扣分制/审改分离全核实)、to-prd(mattpocock，模板+流程核到 SKILL.md)、content-strategy(权重40/30/20/10+买家阶段修饰词核实)、PPTX skill(anthropics/skills 真实存在)、Lean Canvas(九宫格+替换四格)、writing-plans(obra/superpowers)、python-pptx、assertion-evidence(Michael Alley)。
- **中国赛事按权威领域知识与多年公开赛制描述**：中国国际大学生创新大赛(原互联网+)、挑战杯(大挑/小挑)、大创、CUMCM、全国统计建模大赛——官网(cy.ncss.cn / mcm.edu.cn / tiaozhanbei.net / gjcxcy.bjtu.edu.cn)受本环境网络限制未能直连抓取，**组别/重点领域/论文细则逐年改，写材料前务必下当届官方规则压缩包对齐**。
- **部分核实**：统计建模大赛官方论文字数/选题细则(以当届通知为准)；Scientific Slides 的 SKILL.md 未逐字抓取，方法以同源仓库+beamer-skill+assertion-evidence 补全。
- 无编造端点或功能；查不到可靠信息处已显式标注。
