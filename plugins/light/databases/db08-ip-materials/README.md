# db08 — 软著、专利与项目材料模板库

不只存模板，还总结**写作逻辑、常见错误、审查重点、高质量结构、材料间如何互相支撑、可复用范围**。服务 m15(软著专利)、m17(竞赛申报)。

## 这个库是什么(诚实卖点)

**db08 是方法论库,不是事实表**——与 db01(venues 数值事实)模型根本不同,卡数不缩水(都是方法论资产):

- **方法论层(本地精养,护城河,占绝大多数)**:material_card 的 10 字段(软著登记/专利撰写/申报书的行政程序+写作方法论)、budget 预算科目体系、case_skeletons 高分结构骨架——跨学科行政程序与写作 craft,不偏科、变动极慢,是库的核心资产。
- **指针模型(B 类事实,大多无 API)**:加急费用/评分权重/页数口径/竞赛逐年链接**绝大多数无可查 API**,故"转实时"在 db08 = **存口径文字或【待核查】+ source_pointer 指向官方源 + last_checked + 提交前强制核查**,而非 db01/venue_signal 式"查 API 缓存数值"——**绝不缓存数值假权威值**(合规最稳)。唯一真有 API 的专利检索已由 light-ip-application 的 [patent_search.py](../../skills/light-ip-application/scripts/patent_search.py) 实时化,端点真相源唯一在其 [references.md](../../skills/light-ip-application/references.md)。
- **偏科极薄(~3%)**:仅 budget §3 材料化学示例,用 `illustrative_only` 行内标记隔离(科目体系 universal 照搬、领域细节仅演示),不引入 domain_scope 字段。竞赛类型差异(数模/互联网+/挑战杯)是 material_type 合法核心轴、非偏科。
- **无网降级**:写软著/专利常在受限网环境,用本地快照口径(如 60 页/约 30 工作日)+ 产出顶部打显著【提交前以官方当期公告核查】警示,不强制联网。

## material_card schema
`material_type, required_sections, official_requirement, writing_style, common_mistakes, checklist, sample_structure, legal_risk, reuse_scope, final_review_needed`

## 数据来源
中国版权保护中心公开材料、CNIPA、WIPO、USPTO、EPO、Google Patents、The Lens、各高校创新创业/大创/挑战杯/互联网+官方通知、优秀申报书样例、学校教务处/创新创业学院模板、专利代理机构公开案例。

## ⚠ 合规（联动 a10）
- 软著/专利材料不得夸大或虚构。
- 专利最终文本应由专业代理人或法律人员审查（`final_review_needed: true`）。
- 仅学习公开模板结构，不违规收集受版权材料。

## 关于"脱敏高分申报书全文样例"（如实声明，2026-06-12）
本库目前**只存结构骨架、写作逻辑、审查重点与材料卡，不含任何申报书全文样例**。
全文样例（如一份脱敏的高分大创/挑战杯/互联网+申报书）属**用户决策项**，来源有两条路且均需用户拍板：
1. 用户提供自己的申报书，脱敏后入库；
2. 公开渠道的获奖公示材料，且须确认其**可再分发授权**（多数获奖公示仅供查阅、未授权再分发，不可径直入库）。
在用户提供合规来源前，本库保持骨架现状——这是**诚实的"暂缺"而非遗漏**：结构骨架（见 [case_skeletons.md](case_skeletons.md)）已足以指导写作，全文样例是锦上添花而非必需。该项已登记第三期 PROGRESS 用户决策区，待 R10 统一拍板。

## 材料类型库

### 软件著作权
required_sections: 软件名称(全称+简称+版本) / 功能说明 / 操作说明书 / 源代码(前后30页) / 申请表 / 权属证明。
common_mistakes: 源代码页不连续、含敏感信息、版本号不一致、功能与代码不符。
checklist: □ 名称规范 □ 60页代码带页眉 □ 文档配截图 □ 完成/发表日期 □ 权属清晰。

### 发明专利
required_sections: 技术领域 / 背景技术 / 发明内容 / 附图说明 / 具体实施方式 / 权利要求书。
writing_style: 权利要求独立项求最大范围、从属项逐层限定；说明书支持权利要求。
common_mistakes: 权利要求过窄/过宽、缺实施例、创新点不清、检索不足。

### 竞赛/项目申报书
required_sections: 项目摘要 / 背景意义 / 研究内容 / 技术路线 / 创新点 / 可行性 / 研究基础 / 预期成果 / 进度 / 经费预算 / 团队分工。
common_mistakes: 创新点空泛、可行性不足、预算不合理、市场数据臆造。

模板与 canonical 索引见 [material_cards.md](material_cards.md)（0 张实体卡，避免重复 `material_type`）。

## 竞赛申报配套资产（服务 m17 / light-competition）
- [budget_template.md](budget_template.md) — **经费预算表模板**：科研经费支出预算表（大创/大挑，含科目+测算依据列）、已填示例、创业财务预测表（互联网+创业组，含假设登记表+三年损益+现金流转正点）、提交前自审清单。
- [case_skeletons.md](case_skeletons.md) — **优秀案例结构骨架**：互联网+创业组/创意组、挑战杯大挑三类作品、大创申报书、数模 CUMCM/MCM-ICM 的高分结构 + 评审维度 + 高分特征/常见出局点 + 评委视角自审。

## 真实资源文件
- [resources_real.md](resources_real.md) — 真实专利检索入口（Google Patents/CNIPA/Espacenet/PATENTSCOPE/PatentsView/The Lens，平台指针 + 可达性 last_checked;**API 端点/认证/限流真相源唯一在 light-ip-application/references.md,程序化检索走 patent_search.py**)、软著申请要点（CPCC 流程、源代码 60 页规则**单一真相源**）、专利文书结构与常见驳回理由、竞赛申报官方入口(逐年链接标 volatility:high 待核查)。
- [material_extended_cards.md](material_extended_cards.md) — 软著/专利/竞赛材料细分卡（技术交底、权利要求、专利附图、在先技术检索报告、软著说明书/源码材料、挑战杯申报书、创新大赛商业计划书等 8 卡，官方入口 HTTP 200 核验）。
