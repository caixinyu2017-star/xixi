# db08 扩展卡 — 软著 / 专利 / 竞赛材料细分模板

> schema: `material_type, required_sections, official_requirement, writing_style, common_mistakes, checklist, sample_structure, legal_risk, reuse_scope, final_review_needed`
> 核验日期：2026-06-10。CNIPA、CPCC、挑战杯、中国国际大学生创新大赛官网均脚本 HTTP 200 可达。本文只总结结构与检查清单，不缓存受版权模板原文；专利最终文本必须由代理师/法律人员审核。

```yaml
- material_type: 技术交底书(发明/实用新型前置材料)
  required_sections: [技术名称, 技术领域, 背景技术与现有缺陷, 要解决的技术问题, 技术方案, 有益效果, 实施例, 附图清单, 关键词与检索式]
  official_requirement: 不是官方提交文件，但通常是代理师撰写专利申请的核心输入；内容须真实、充分、可实施
  writing_style: 工程化、客观、可复现；先讲问题，再讲方案，再讲效果；避免营销词
  common_mistakes: [只写功能不写技术手段, 有益效果无数据/机理支撑, 关键步骤缺参数, 与论文创新点混淆, 未列对比现有技术]
  checklist: ["现有技术至少检索 Google Patents/CNIPA/Espacenet", "技术问题一句话明确", "每个创新点对应技术特征", "至少一个可实施例", "附图编号与正文一致"]
  sample_structure: "1 技术领域→2 背景与缺陷→3 技术问题→4 方案步骤/模块→5 有益效果→6 实施例→7 附图说明→8 检索证据"
  legal_risk: 公开不充分或虚构效果会影响授权与稳定性；早公开论文/答辩可能影响新颖性，提交前需评估公开时间
  reuse_scope: 可复用 m05 方案、a03 实现、m07 方法章节、m11 流程图
  final_review_needed: true

- material_type: 权利要求书草案(方法+系统+介质组合)
  required_sections: [独立方法权利要求, 从属方法权利要求, 装置/系统权利要求, 计算机可读存储介质权利要求]
  official_requirement: 权利要求应清楚、简要，并以说明书为依据；软件类需体现技术问题、技术手段、技术效果
  writing_style: 独立项覆盖必要技术特征，从属项逐层收窄；术语前后一致；避免“优选地”写进独立项
  common_mistakes: [独立项过窄导致保护范围小, 过宽无说明书支持, 功能性限定无结构/步骤支撑, 多个发明点缺单一性, 从属项引用错误]
  checklist: ["独立项包含解决问题的必要特征", "每个特征能在说明书找到支持", "从属项形成回退层级", "方法/系统/介质三类主题互相对应", "术语表统一"]
  sample_structure: "权1 方法独立项；权2-6 方法从属；权7 系统/装置；权8 电子设备；权9 存储介质"
  legal_risk: 权利要求决定保护范围，非专业撰写风险极高；不得直接提交未经审核草案
  reuse_scope: 技术步骤来自技术交底书与系统设计；术语同步 a07/论文/软著材料
  final_review_needed: true

- material_type: 专利附图与图号说明
  required_sections: [附图清单, 每幅图的图名, 图中标号说明, 与说明书段落对应关系, 绘图规范说明]
  official_requirement: 附图应清楚显示技术方案；发明/实用新型通常使用黑白线图，标号一致，避免照片式装饰
  writing_style: 简洁、结构化；每个标号只代表一个部件/步骤；图号按出现顺序排列
  common_mistakes: [图中标号与说明书不一致, 箭头/流程方向不清, 截图含无关个人信息, 颜色依赖导致黑白不可读, 图太像产品宣传图]
  checklist: ["图1总体架构", "图2方法流程", "图3模块结构", "图4关键算法/数据流", "所有标号在正文解释", "黑白打印可辨"]
  sample_structure: "图1 系统总体结构示意图；图2 方法流程图；图3 模块交互图；图4 实施例数据处理流程图"
  legal_risk: 图文不一致会导致不清楚/不支持；公开过多商业秘密也有风险
  reuse_scope: 可由 m11/db07 的 pipeline/architecture 图转成专利黑白线图
  final_review_needed: true

- material_type: 在先技术检索报告
  required_sections: [检索目的, 检索日期, 数据库与入口, 检索式, 命中文献表, 相关段落/权利要求摘录, 对比矩阵, 初步风险判断]
  official_requirement: 非官方必交文件，但代理师/学校知识产权办常要求作为可专利性判断依据
  writing_style: 证据导向；每个结论附公开号/DOI/URL/日期；不下最终法律结论
  common_mistakes: [只搜中文不搜英文, 只搜论文不搜专利, 不记录检索式, 命中文献无相关段落, 把未授权检索当 FTO 结论]
  checklist: ["Google Patents/CNIPA/Espacenet 至少三源", "中文+英文关键词", "IPC/CPC 分类检索", "同族与引用追踪", "命中文献按相关度排序", "风险只写初步"]
  sample_structure: "A 检索策略→B 命中文献表→C 与本方案区别矩阵→D 新颖性/创造性初步风险→E 待代理师复核问题"
  legal_risk: 检索不充分会误判授权前景；FTO/侵权自由实施必须另做专业法律意见
  reuse_scope: 与 m01 文献检索、m15 patent_search.py、m04 idea-critique 的新颖性审查联动
  final_review_needed: true

- material_type: 软著操作说明书
  required_sections: [软件概述, 运行环境, 安装部署, 登录/权限, 功能模块操作步骤, 输入输出说明, 异常提示, 截图清单, 版本信息]
  official_requirement: 中国版权保护中心软件著作权登记文档鉴别材料；通常提交前后各 30 页，不足 60 页全交，以当期指南为准
  writing_style: 用户手册式，客观描述真实功能；每个功能“入口→操作→结果”闭环
  common_mistakes: [截图与功能不一致, 版本号与申请表/源码页眉不一致, 操作步骤空泛, 使用不存在功能, 截图含个人隐私或密钥]
  checklist: ["软件名+版本全篇一致", "每个核心模块有截图", "截图脱敏", "运行环境明确", "前后30页连续", "功能与源码/系统一致"]
  sample_structure: "1 概述→2 环境→3 安装→4 登录→5 模块A操作→6 模块B操作→7 数据导出→8 常见问题→9 版本说明"
  legal_risk: 材料不实可能影响登记效力；截图泄露隐私/密钥有安全风险
  reuse_scope: 可复用 a04 系统设计、a05 前端页面、README 使用说明
  final_review_needed: false

- material_type: 软著源代码鉴别材料
  required_sections: [源代码页眉, 页码, 前30页, 后30页, 脱敏记录, 第三方依赖说明]
  official_requirement: 通行规则为源程序前后各连续 30 页、每页不少于 50 行，不足 60 页全交；最新口径以 CPCC 当期指南为准(规则单一真相源见 resources_real.md §2 带 last_checked,本卡不另维护页数口径)
  writing_style: 代码原样连续，必要注释保留；不得插入无关代码/空行充页
  common_mistakes: [代码不连续, 行数不足, 页眉缺软件名版本, 含 token/password, 大量第三方库代码, 与申请软件无关]
  checklist: ["运行 secret 扫描", "移除密钥/个人路径", "页眉=软件全称+版本", "页码连续", "不足60页全交", "第三方开源许可记录"]
  sample_structure: "submit_source.txt / PDF：页眉、页码、代码正文；另附脱敏说明与依赖清单"
  legal_risk: 提交第三方或虚假代码会产生权属/真实性风险；泄露密钥会造成安全事故
  reuse_scope: 由 m15 scripts/copyright_source_prep.py 从真实仓库生成
  final_review_needed: false

- material_type: 挑战杯课外学术科技作品申报书
  required_sections: [作品简介, 研究背景, 国内外现状, 科学问题, 研究方法, 主要成果, 创新点, 应用价值, 研究基础, 参考文献, 附件]
  official_requirement: 以当届挑战杯和学校通知模板为准；需团队/指导教师/学校审核
  writing_style: 学术作品风，强调问题价值、研究过程、证据链和真实成果；避免创业路演式空话
  common_mistakes: [把产品功能当科研创新, 文献综述薄弱, 数据/实验不可复现, 成果夸大, 附件证据不足]
  checklist: ["创新点有文献对比", "方法与结果可复现", "图表支撑核心结论", "参考文献真实", "附件含代码/数据/论文/证明", "伦理与数据合规说明"]
  sample_structure: "摘要→背景与问题→相关工作→研究方法→实验/调研结果→创新点→社会/应用价值→不足与展望→附件"
  legal_risk: 伪造成果、冒用他人成果、数据造假会触发学术诚信风险
  reuse_scope: 可复用 m01 调研、m05 方案、m06 结果、m07 论文、m16 PPT
  final_review_needed: false

- material_type: 中国国际大学生创新大赛商业计划书
  required_sections: [项目概述, 痛点与需求, 产品/服务, 技术壁垒, 市场分析, 商业模式, 竞争分析, 运营计划, 财务预测, 团队分工, 风险与对策, 社会价值]
  official_requirement: 以当届赛事平台 cy.ncss.cn 与学校通知为准；不同赛道/组别材料要求不同
  writing_style: 证据型路演文风；市场和财务用可核查来源，技术壁垒要落到真实成果
  common_mistakes: [市场规模臆造, 财务预测无假设, 技术壁垒空泛, 竞品分析只贬低别人, 团队经历与项目不匹配, 社会价值口号化]
  checklist: ["TAM/SAM/SOM 来源可查", "收入/成本假设登记", "竞品维度公平", "原型/用户验证证据", "知识产权/软著/专利状态真实", "风险不回避"]
  sample_structure: "一句话项目→问题→解决方案→技术/产品→市场→商业模式→验证数据→团队→财务→风险→融资/资源需求"
  legal_risk: 商业数据、用户数、收入、专利状态不得虚构；涉及医疗/教育/金融需合规声明
  reuse_scope: 与 db06 路演 PPT、db08 budget_template、m17 competition、m15 IP 材料联动
  final_review_needed: false
```
