# light-competition — 深度分析与同类对标

> 源：[`skills/light-competition/SKILL.md`](../../../skills/light-competition/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：面向中国双创/学术竞赛与项目申报的"材料辅助"技能：先定位赛事规则，再用借自 NIH/Market-Research/Beamer 等成熟范式的结构化方法产出申报书/商业计划/路演/答辩材料，并做反模式排雷与评审模拟。

## 核心运行逻辑
设计思路是"先对齐当届官方规则 → 选材料模块 → 按可机检的结构化骨架写 → 反模式排雷 + 评委视角自审 → 与其他 Light 技能联动落盘"。核心方法论不是原创，而是把外部成熟范式迁移到中文竞赛场景：NIH Specific Aims 一页纸→中文"立项核心页"(aims_zh_guide.md)、Market Research 的 TAM/SAM/SOM+假设登记+交叉校验、Lean Canvas 九格、beamer/PPTX 的 assertion-evidence 与视觉 QA 闭环、writing-plans 的可验证里程碑。两段可执行资产是 roadmap_gen.py(里程碑→甘特/路线图) 与 market_charts.py(市场四图)，都本地离线、合成自测、色盲安全。事实层诚实地承认中国赛事官网受网络限制无法实时核实,反复要求用户下载当届规则压缩包对齐。db08 数据库(预算模板/案例骨架/材料卡)作为后端知识存储被 SKILL.md 大量引用。

## 关键步骤
- 1. 定位赛事/项目/组别类型，下当届官方评审规则压缩包对齐评分项(数模/统计建模/创新大赛/挑战杯大挑小挑/大创各不同)
- 2. 按需选材料模块(申报书/商业计划书/路演PPT/答辩稿/摘要/技术路线/创新点/可行性/市场分析/预算/团队分工)
- 3. 先写核心页(借 NIH Specific Aims 八段骨架，第一页/开篇300-500字决定评委读不读)，参 aims_zh_guide.md
- 4. 创业类先填 Lean Canvas 九格自检逻辑闭环，市场做 TAM→SAM→SOM 自下而上+假设登记表+竞品四透镜+交叉校验
- 5. 用 roadmap_gen.py 出甘特/技术路线图、market_charts.py 出市场四图(JSON 与预算/财务预测共用同一套数)
- 6. 路演 deck 交 m16 程序化出 pptx + 视觉 QA 闭环；学术答辩用 assertion-evidence + 内容密度上下界
- 7. 用 references/anti_patterns.md 五类反模式逐条排雷 + 一页速查表
- 8. 评委视角评审模拟(NIH五项/NSF两项/数模回看摘要灵敏度/创业回看UVP壁垒市场测算)+答辩QA预演
- 9. 联动落盘：技术内容←m05/a03，论文←m07，软著专利←m15，图表←m11，一致性由 a07 把关，全程入 db09，真实性风险报 a10，交付前过 a08 自检

## 自带资产
- SKILL.md — 主路由：六大赛事规则定位 + 材料模块 + 通用申报书骨架 + 市场分析纪律 + 路演/答辩 + 评审模拟
- assets/aims_zh_guide.md — 把 NIH Specific Aims 八段骨架迁到中文竞赛核心页，逐段中文范例(学术向+创业向)+10条自检清单+与正文衔接
- references/anti_patterns.md — 跨赛事反模式手册，五类(概念/写作/技术/格式/策略)每条症状→为何被扣→怎么改，附一页交稿前速查表
- references.md — 16 个外部工具/赛事的逐条研究笔记，标真实链接+可复用方法+已知坑+核实程度(含调研诚实声明)
- scripts/roadmap_gen.py — 里程碑 JSON→甘特图(交付物+go/no-go菱形)/技术路线图(蛇形阶段块+箭头)，CJK字体自适配，含 --selftest/--emit-sample，自测通过
- scripts/market_charts.py — 市场 JSON→四图(TAM/SAM/SOM同心圆/竞品2×2/波特五力分级条/风险概率×影响热图)，Okabe-Ito 色盲安全色，强制 TAM≥SAM≥SOM 校验，自测通过
- (后端依赖,非本目录)db08/budget_template.md — 科研支出预算表+已填示例+创业财务预测+假设登记表+自审清单
- (后端依赖)db08/case_skeletons.md — 各赛事高分结构骨架+评审维度+高分特征/常见出局点+互联网+路演时长分配表
- (后端依赖)db08/material_cards.md — 材料卡模板+canonical 索引(实际卡片已迁至 material_extended_cards.md)

## 优点
- 方法论有真实出处且分层诚实：references.md 对每条来源明确区分'已核实/部分核实/未能核实'，MCM/ICM 硬规则(25页含附录代码、99小时、AI说明必填)核到官方 contest instructions，中国赛事则坦承网络受限、要求下当届规则——不臆造分值，这种诚实在申报类技能里少见
- 两段脚本工程质量高：纯本地离线无网络、合成自测可一键验证(实测均 PASS)、CJK 字体优雅降级不崩、Okabe-Ito 色盲安全色、市场图强制 TAM≥SAM≥SOM 层级校验防自上而下虚高、demo 默认写临时目录不污染仓库
- 反模式手册可直接当交稿前 checklist：五类×具体症状→评委扣分逻辑→可执行改法，且一页速查表把整套压成五行自查，命中数模'摘要写成重述/漏灵敏度'、创业'先发当壁垒/市场自上而下虚高'等真实高频出局点
- 核心页指南把抽象的'立项依据怎么写'落到八段式+学术向/创业向两套中文范例+可机检四件套(理由/假设/方法/产出)，并强调'前期证据前移降低评委风险感知'这一 NIH 实操精髓
- 跨材料数据一致性意识强：市场分析 TAM/SAM/SOM 与预算/财务预测显式共用同一套 ARPU/转化率/用户数，由 a07 把关，直接防范评委最爱追问的'BP 说 100 万用户、财务预测却按 10 万算'这类自相矛盾
- 数据纪律具体可执行：市场数据须≤2年标出处、客户画像基于真实评论语言、第一性原理测算后用竞品营收交叉校验，而非空喊'数据要真实'

## 缺点 / 可被质疑处
- 产出工件未进 CONVENTIONS.md §6.1 工件契约表(全仓库交接的单一真相源)：SKILL.md'产出'声明了材料文档/答辩QA预演/材料清单/经费预算表，但既无 canonical 落盘文件名(如 application_draft.md)，也没在那张表里登记;表中明确要求'双向声明'，m17 是唯一缺席的主线产出技能，编排器(light-orchestrator)无法按名调度其产物
- 缺核心交付物的可填模板:同仓 light-paper-drafting 有 templates/01_imrad.md 等6套、light-ip-application 有 claims/specification 模板，而本技能除 db08 预算表外，申报书/商业计划书/答辩稿/项目摘要都只有'结构骨架描述'，用户拿到的是该写什么的说明而非能套着填的文档框架，对'材料辅助'定位是明显缺口
- 无 examples/ 端到端样例:多数兄弟技能(literature-search/result-analysis/consistency)都带 worked_example，本技能横跨6+赛事却没有一个从核心页→骨架→预算→反模式自查的完整走查示例，新手难感知如何串起整套流程
- SKILL.md 信息密度过载:全篇长句套多层括号(如第10行 CUMCM AI 规定一句话塞进时间/正文标注/PDF详情/取消资格四件事)，竞赛时间压力下难快速 action;一个文件试图覆盖数模+统计建模+创新大赛+挑战杯双杯+大创+基金范式+商业计划，路由与细节混在一起
- 事实层时效性是结构性维护负担:中国赛事组别/重点领域/评分细则逐年改且本环境无法核实，CUMCM AI 政策标 last_checked 2026-06、创新大赛组别2024 更名——这些断言会随时间静默过期，技能本身无内建的'当年规则已下载确认'强制闸门(仅靠文字反复提醒)
- 存在指针/交叉引用漂移:SKILL.md'产出'仍把 db08/material_cards.md 称作'材料类型卡'，但该文件现已是 canonical 索引壳、真卡迁到 material_extended_cards.md;anti_patterns.md C2 让'复用 code_assets/stats_tests'，但该路径不属于本技能资产，未确认其存在
- 脚本细粒度局限:roadmap_gen 甘特图仅支持按月(_month_index 以 YYYY-MM 为粒度)，而数模/短周期竞赛进度常以周/天计;market_charts 的 TAM/SAM/SOM note 标注用硬编码偏移(idx*0.5)且五力 rationale 无长度控制，层数多或文案长时可能重叠/溢出，缺多风险同格之外的自动避让

## 可优化点（供后续逐技能优化）
- 在 CONVENTIONS.md §6.1 工件契约表新增 m17 行，定义 canonical 落盘名(如 application_draft.md / business_plan.md / pitch_deck_outline.md / defense_qa.md / budget_table.md / material_checklist.md)，并在 SKILL.md'产出'节逐字双向声明，让 orchestrator 可调度、a07 可跨材料核查
- 补 templates/ 可填模板:申报书八段骨架.md(对齐 case_skeletons §4 十二段)、商业计划书.md(对齐 §1 十一段)、答辩QA预演.md(问题分类+备份附录指引)、项目摘要.md(数模摘要'模型名+关键结论数字'占位)，与 aims_zh_guide.md 的核心页打通
- 加 examples/ 一个端到端 worked example:以 README 里的'基层眼底筛查'为线，串核心页→申报书骨架→roadmap_gen 里程碑 JSON→market_charts 市场 JSON→预算表→反模式自查，展示数据如何在材料间保持一致
- 把 SKILL.md 重构为'瘦路由+厚 references':SKILL.md 只留'先定位→选模块→走流程→自审'主干，每个赛事的硬规则细节下沉到 references/ 分文件(competition_rules_cn.md 等)，降低单文件认知负载、便于按赛事独立更新时效内容
- 给脚本加细粒度与鲁棒性:roadmap_gen 增 --granularity week|month、甘特支持周/天;market_charts 改 note 为基于实际半径/层数动态布局并对 rationale 截断或换行，加层数>4 与长文案的回归用例
- 内建'当届规则确认'闸门:在 SKILL.md 流程首步要求产出一个 rules_checklist(本届组别/重点领域/页数/预算封顶/提交物/AI规定 已核对)，并在 references.md 顶部统一维护 last_checked 字段，把时效风险从'文字提醒'升级为'可勾选工件'
- 修指针漂移:SKILL.md'产出'改指 material_extended_cards.md(或同时列索引);核实并修正 anti_patterns.md C2 的 code_assets/stats_tests 引用(指向真实存在的统计检验资产或改为 light-data-engineering/result-analysis 的对应能力)

## 与其他 Light 技能/知识库的衔接
上游消费:技术内容←m05(research-plan)/a03(backend-coding)、论文成果←m07(paper-drafting)、判断创新点复用 m03/m04(idea-generation/critique)。横向产出:路演 deck 交 m16(light-slides)程序化出 pptx 并按 db06 主题统一视觉、数据图走 m11(figure-drawing 真数据出图，Okabe-Ito 色板即取自其 color_palettes.py)、软著专利←m15(ip-application)。质量闸门:跨材料术语/指标/数据一致性由 a07(light-consistency)把关、交付前过 a08(light-self-review)自检、商业/数据真实性风险上报 a10(合规)。知识沉淀:全过程入 db09(知识库)。后端存储:深度依赖 db08-ip-materials 数据库(预算模板/案例骨架/材料卡/resources_real)。当前主要断点:产出工件未登记进 CONVENTIONS §6.1 契约表，与 light-orchestrator 的自动调度链未真正打通,联动多停留在 SKILL.md 文字层面而非可落盘的命名工件层面。

---

## GitHub 同类前沿技能对标

light-competition 专为中国双创/竞赛/申报定制,GitHub 无直接对手。同类是欧美英文 grant 工具(强在 RAG 后端)或硅谷创业者 Claude skill 包(强在 star 多)。差异化:把 NIH Aims、TAM/SAM/SOM、Lean Canvas、assertion-evidence 迁到中文竞赛+离线 Python 资产+反模式排雷+评委自审。短板:无 RAG、无独立 star。light 偏方法论严谨可复现,对手偏数据驱动生态规模。可借鉴:1)引入 RAG 检索后端(lewisExternal/UABPeriopAI),让用户上传当届规则压缩包做本地向量检索对齐,缓解无法核实官网的短板;2)把评审范式编码为可机检评分卡(参考 tjboudreaux 固化 Sequoia/a16z/YC 原理);3)用真实案例数据背书反模式排雷(参考 yayashuxue 的 101 份访谈),沉淀历年落选案例库入 db08;4)补一键产出与轻量浏览器演示入口(参考 emotixco/yayashuxue),降低答辩路演上手成本;5)借鉴成熟 deck 的 problem/solution/market/business-model 叙事结构,补充中文路演骨架页面顺序。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [eseckel/ai-for-grant-writing](https://github.com/eseckel/ai-for-grant-writing) | LLM 写科研基金资源清单标杆。 | 4139 | 2026-06-12 | 强:验证多。弱:仅清单纯英文。 |
| [shawnpang/startup-founder-skills](https://github.com/shawnpang/startup-founder-skills) | 创业者 agent skill 包。 | 146 | 2026-06-10 | 强:star 最高。弱:非竞赛申报。 |
| [emotixco/claude-skills-founder](https://github.com/emotixco/claude-skills-founder) | 创业者技能含 pitch deck。 | 52 | 2026-06-12 | 强:含 deck。弱:B2B 非竞赛。 |
| [mfwarren/entrepreneur-claude-skills](https://github.com/mfwarren/entrepreneur-claude-skills) | 24 个创业技能。 | 35 | 2026-06-11 | 强:技能多。弱:无申报书骨架。 |
| [tjboudreaux/cc-skills-vc-fundraising](https://github.com/tjboudreaux/cc-skills-vc-fundraising) | VC 原理 pitch 与融资插件。 | 13 | 2026-06-10 | 强:评审框架。弱:纯融资英文。 |
| [yayashuxue/solo-founder-playbook](https://github.com/yayashuxue/solo-founder-playbook) | 101 访谈的 idea 评估与吐槽。 | 20 | 2026-06-09 | 强:数据背书。弱:无中文模板。 |
| [lewisExternal/AI-Grant-Writer-Tool](https://github.com/lewisExternal/AI-Grant-Writer-Tool) | AutoGen+RAG grant 工具。 | 28 | 2026-06-12 | 强:真 RAG 后端。弱:英文基金。 |
| [UABPeriopAI/Grant_Guide](https://github.com/UABPeriopAI/Grant_Guide) | NIH 风格基金写作工具。 | 28 | 2026-06-07 | 强:对标 NIH。弱:纯英文。 |
| [zhsongallen/CharityPen](https://github.com/zhsongallen/CharityPen) | 非营利 AI 资助申请助手。 | 48 | 2026-03-01 | 强:聚焦公益。弱:偏文案募款。 |
| [moefc32/pitch-deck-generator](https://github.com/moefc32/pitch-deck-generator) | Gemini pitch deck 生成器。 | 8 | 2026-05-05 | 强:一键生成。弱:无方法论。 |
