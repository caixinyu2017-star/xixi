# light-self-review 参考工具研究笔记

逐工具核查的硬信息。带【是什么】【可复用方法】【链接】【已知坑/局限】。
研究日期 2026-06。凡未能核实者明确标注。

---

## verification-before-completion (obra/superpowers)

【是什么】Claude 技能，铁律「没有新鲜验证证据就不许宣称完成」(NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE)。核心原则「Evidence before claims」。

【可复用方法】闸门函数五步：
1. IDENTIFY 想清楚「什么命令能证明我要下的结论」。
2. RUN 完整、当场重跑该命令（不能引用旧输出/假设）。
3. READ 读完整输出，查 exit code，数失败条数。
4. VERIFY 确认输出真支撑结论；不支撑就如实报真实状态。
5. ONLY THEN 才下结论。跳任何一步=「在撒谎而非验证」。
对应清单：测试通过=要有 0 失败的测试输出；lint 干净=要有 0 error 输出；构建成功=exit 0（光过 lint 不够）；bug 修复=原始症状被测且通过；回归测试=要有红-绿循环（撤掉修复必须失败，恢复后通过）；子代理完成=要看 VCS diff；需求满足=逐条核对清单。
红旗词：should / probably / seems to / 提前满足 / 轻信子代理报告。

【链接】https://obra-superpowers.mintlify.app/skills/verification-before-completion

【已知坑】要求「当前消息里」就有证据，强调不能复用历史运行结果。

---

## systematic-debugging (obra/superpowers)

【是什么】根因优先调试技能。铁律「没找根因前不许提修复」，治标=失败。

【可复用方法】四阶段，顺序不可跳：
- Phase 1 根因调查：①细读报错(stack/行号/错误码) ②稳定复现(找触发步骤) ③查最近改动(git diff/依赖/配置/环境) ④多组件系统在每个边界加日志记录输入输出，先定位坏在哪层 ⑤逆向追数据流，从坏值追到来源——「在源头修，不在症状处修」。
- Phase 2 模式分析：找同库里能跑通的相似代码，完整读参考实现，逐一列出可跑与坏掉的每个差异。
- Phase 3 假设检验：科学方法——提单一具体假设「我认为 X 是根因，因为 Y」，做最小改动、一次只动一个变量；不成立就换假设，不许在上面堆补丁。
- Phase 4 实现：先写复现失败用例 → 单一修复只针对根因(不夹带重构) → 验证通过且不破坏其他。
失败循环规则：修了≥3 次仍不行→停手，质疑架构（信号：每次修都暴露新耦合/需大重构/按下葫芦浮起瓢），找人讨论。

【链接】https://obra-superpowers.mintlify.app/skills/systematic-debugging

【已知坑/数据】技能自称系统调试 15–30 分钟 vs 乱试 2–3 小时，首次修复率 95% vs 40%（厂商自述，未独立验证）。

---

## test-driven-development (obra/superpowers)

【是什么】红-绿-重构 TDD 技能。铁律「没有先失败的测试，就不许写生产代码」；先写代码后写的测试立即通过=「什么都没证明」。

【可复用方法】循环六步：①RED 写一个最小失败测试(测一个行为、清晰命名、用真实代码、尽量不 mock) ②Verify RED 跑、确认它「失败」(不是 error)且原因正确——强制步骤，绝不跳 ③GREEN 写让它过的最简代码 ④Verify GREEN 跑全套、新测试过且没弄坏别的 ⑤REFACTOR 仅在绿后清理(去重/改名/抽取)、不加新行为 ⑥重复。
具体技巧：修 bug→先写复现 bug 的测试再修；不会测→先写理想 API 和断言再倒推；测试太复杂→简化被测接口；什么都得 mock→代码耦合过重，改用依赖注入。

【链接】https://obra-superpowers.mintlify.app/skills/test-driven-development

【已知坑】测试名里出现 "and" 就该拆。

---

## receiving-code-review (obra/superpowers)

【是什么】处理收到的代码评审意见的技能。反对两种反模式：「表演式同意」(为显得配合而附和)与「盲目实现」(没理解/没验证就改)。

【可复用方法】流程：①收到意见先暂停别立刻改 ②核验该意见技术上是否真成立 ③判断意见是否清晰 ④对可疑/不清的意见提出质疑或要澄清 ⑤只在理解+验证后才动手。维度：技术正确性(这建议真是改进吗)、意图清晰度、避免防御性(是分析性怀疑而非情绪对抗)。规则：别为关闭评审而附和；别改没验证过是改进的东西；反驳时给技术理由/代码/测试证据，不空驳。

【链接】https://github.com/obra/superpowers/blob/main/skills/receiving-code-review/SKILL.md ｜ https://cursor.com/cn/marketplace/skills/receiving-code-review

【已知坑】配套的 requesting-code-review 用子代理评审，关键设计「评审者只拿到精心构造的上下文，绝不给它你这次会话的历史」以聚焦产物本身。问题分三级：Critical(立即修)/Important(进下一任务前修)/Minor(记录待办)。

---

## audit skill

【是什么】目标清单里的「audit skill」在 anthropics/skills 和 obra/superpowers 中**均无同名技能**（已核 README 与技能总览）。它是一类「结构化安全/合规审计」模式的统称。最接近的真实实现是社区的 claude-skill-security-auditor（结构化安全审计+可执行的修复计划）。

【可复用方法(审计模式)】把审计当成带证据的逐条核查：定义审计范围→对每条规则给出 通过/不通过/不适用 三态判定→不通过项附严重级与具体修复建议→输出可追溯的发现清单(来源/位置/证据)。这与 Deepchecks 的 condition pass/fail/warning 三态、Cisco scanner 的 HIGH/MEDIUM/LOW/SAFE 分级同构。

【链接】https://github.com/wrsmith108/claude-skill-security-auditor ｜ https://github.com/anthropics/skills

【已知坑/诚实声明】**无 Anthropic 官方同名 audit 技能**；此处用社区实现+通用审计模式替代，不应把它当成某个权威钦定的技能。

---

## critique skill

【是什么】目标清单里的「critique skill」同样**无 Anthropic/superpowers 官方同名技能**。其职能由 requesting-code-review + receiving-code-review + verification-before-completion 共同承担，学术侧对应下面的 Peer Review / Scientific Critical Thinking / PRISM 维度。

【可复用方法(批判模式)】对自身产出做对抗式自评：分维度打分(可操作性/具体性/论证/解法/语气，见 PRISM)、严重度排序(致命问题排前)、给出明确改进路径而非只指出问题。

【链接】见 receiving-code-review 与下方 PRISM 条目。

【已知坑/诚实声明】无官方同名技能，按通用批判性评审模式落地。

---

## Peer Review (学术同行评审)

【是什么】学术稿件评审制度。评审者给四档建议：无条件接受/修改后接受/拒但鼓励重投/直接拒。

【可复用方法(评审维度清单)】原创性/新颖性(是否有新洞见)、方法学是否扎实、**结论是否被结果支撑**(经典失败点)、文献根基、贡献(对实务/领域是否有用)、与刊物范围契合、格式合规。盲法类型：单盲/双盲/开放/透明/预印本(预)/发表后(PubPeer)/结果盲/注册报告(先审设计再采数据)。

【链接】https://en.wikipedia.org/wiki/Scholarly_peer_review ｜ https://www.springernature.com/jp/researchers/the-source/blog/blogposts-for-peer-reviewers/10-steps-to-evaluating-manuscripts-as-a-peer-reviewer/16679144

【已知坑/偏倚】1998 年实验：多数评审者注意不到「结论不被结果支撑」。系统性偏倚：声望偏倚、保守倾向(压创新)、确认偏倚(挑与己见相左的结论)、地域偏倚；且同行评审无法可靠识别造假/抄袭，评审者间一致性低。

---

## Scientific Critical Thinking (科学批判性思维)

【是什么】Danchin「批判生成法」框架，用于评估科学主张。

【可复用方法(10 条快查清单)】①术语我真懂吗 ②独立 verify 源头主张(「verify, verify, verify」) ③有哪些未明说的公设/假设(公设越多越不可靠) ④作者是否把模型当现实(「模型的真不等于现象的真」「数据不会自己说话」) ⑤把相关当因果了吗(混淆是最大反科学行为) ⑥实验测的真是模型的预测，还是对预测的松散解读 ⑦此主张可证伪吗、举证责任在谁(在提模型者) ⑧只有确认性证据，还是真做过证伪尝试 ⑨失败的预测是被解决了还是被反复重解释搪塞("例外证明规律") ⑩这是解释「为什么」，还是只模拟「是什么」。

【链接】https://pmc.ncbi.nlm.nih.gov/articles/PMC10527184/

【已知坑】面向科学哲学层面，工程产出需结合可执行验证(见 verification-before-completion)。

---

## Scholar Evaluation (科研评价)

【是什么】对研究者/成果的评价方法学，从单一 h-index 走向多维「负责任的计量」。

【可复用方法】h-index 定义：有 h 篇论文各被引≥h 次。其局限：跨学科不可比、偏向资深、永不下降、不分自引/合著贡献/引用情感、漏掉「一篇高引+多篇零引」。负责任框架：DORA(别用期刊影响因子评单篇，按成果本身评)、Leiden 宣言(量化指标支撑而非取代专家判断)、Metric Tide(量化+专家+定性互补)、SCOPE。多维评价维度：研究质量(同行评审、领域归一化引用、可复现性)、知识传播(开放获取/预印本/数据集)、政策影响、临床/经济影响、教学指导、协作广度、社会参与、叙述性贡献(自述"so what")。

【链接】https://guides.lib.umich.edu/researchimpact/holisticframeworks ｜ https://guides.lib.umich.edu/researchimpact/hindex

【已知坑】任何单一指标都不能负责任地代表贡献；引用计量只应作为多维评估的一个输入。

---

## Deepchecks (数据/模型验证库, 开源 Python)

【是什么】对 ML 数据与模型做持续验证的库；从研究到生产都能测。

【可复用方法/真实 API】
- 数据对象按模态：`Dataset`(表格)、`TextData`(NLP)、`VisionData`(视觉)，封装数据+元数据。
- 三大内置套件(suites)：`data_integrity`(数据完整性，如冲突标签)、`train_test_validation`(训练/测试分布漂移、泄漏)、`model_evaluation`(模型表现、弱分段)。
- 用法：
  ```python
  from deepchecks.tabular.suites import model_evaluation
  suite = model_evaluation()
  res = suite.run(train_dataset=train, test_dataset=test, model=model)
  res.save_as_html()   # 或 res.show()；res.results[0].value 取程序化结果
  ```
- 核心机制：每个 check 可挂可定制的 **condition**，自动产出 通过✓/失败✖/警告! 三态判定，汇总成报告。
- 安装：`pip install deepchecks -U`；NLP 用 `deepchecks[nlp]`，视觉用 `deepchecks[vision]`。

【链接】https://github.com/deepchecks/deepchecks ｜ https://docs.deepchecks.com/ ｜ 论文 http://arxiv.org/abs/2203.08491

【已知坑】把验证拆成「check + condition」，关键在为 condition 设对阈值，否则只是展示不报警。

---

## Evidently AI (数据漂移/ML/LLM 评估库, 开源 Python)

【是什么】生成数据质量、漂移、ML 表现与 LLM 文本评估的 Report 与 Test。

【可复用方法/真实 API】
```python
from evidently import Report
from evidently.presets import DataDriftPreset, DataSummaryPreset
report = Report([DataDriftPreset(), DataSummaryPreset()])
my_eval = report.run(current_data=cur, reference_data=ref)  # 第1参=当前，第2参=基线
my_eval.json     # 导出 JSON；my_eval.dict() 取字典；直接渲染出 HTML
```
- Preset 即开即用配置：`DataDriftPreset`(需两份数据，测分布漂移)、`DataSummaryPreset`(单份统计)。可传 `column=[...]` 限列。
- 单指标可混用：`ColumnCount()`、`ValueStats(column=...)`、`ValueDrift(column="target", method="psi")`、`PrecisionTopK(k=10)`。
- `GroupBy(metric, "Department")` 分组评估；`compare(eval1, eval2, ...)` 多快照横比。
- Tests 系统：给 Metric 加 condition 得到 pass/fail 阈值判定。
- LLM：给 Dataset 的文本列挂 Descriptors，评文本质量/相关性，沿用同一 Report 模式。

【链接】https://docs.evidentlyai.com/docs/library/report ｜ https://docs.evidentlyai.com/docs/library/overview

【已知坑】run() 参数顺序是「当前在前、基线在后」，搞反会让漂移方向反掉。

---

## Snyk (开发者安全平台 / CLI)

【是什么】查并修开源依赖与源码中的已知漏洞，含 SCA 与 SAST。

【可复用方法(CLI 命令)】
- `snyk test`：扫开源依赖(SCA)，比对漏洞库。
- `snyk code test`：对一方源码做静态分析(SAST)，不执行代码找安全缺陷。
- `snyk monitor`：上传依赖快照，持续监控并在新漏洞出现时告警。
- `snyk container test`：扫容器镜像(OS 层+应用依赖)。
- `snyk iac test`：扫 IaC(Terraform/CloudFormation/K8s)配置错误。
- 关键 flag：`--severity-threshold=<low|medium|high|critical>` 只报达阈值的(CI 降噪)；`--all-projects` 扫目录树所有清单(monorepo)；`--json` 机器可读输出。

【链接】https://docs.snyk.io/snyk-cli/commands ｜ 入门 https://support.snyk.io/hc/en-us/articles/360003812458

【已知坑/诚实声明】Snyk 官方 docs 站点对自动抓取多次返回 403/404；上述命令与 flag 取自检索摘要与通行用法，**未能逐条从官方页面原文核验**，使用前请以 `snyk --help` 实测为准。

---

## Socket.dev (软件供应链安全)

【是什么】在装包之前检测供应链攻击；走「行为/能力分析」而非只比 CVE——分析包**做了什么**。AI 扫描 + 人工复核。

【可复用方法】
- `sfw` CLI(Socket Firewall Free)：前缀在包管理命令前，装包前先检测。例：`sfw uv pip install flask`、`sfw npm install ...`。支持 npm/yarn/pnpm/pip/uv/cargo(JS/TS、Python、Rust)。
- 机制：起一个临时 HTTP 代理拦截子进程流量，向 Socket API 查询，覆盖直接+传递依赖。
- 关注信号(能力分析层面)：install/postinstall 脚本、网络/shell/文件系统访问、混淆代码、遥测、typosquatting(仿冒名)。免费版对 AI 标记的告警、仅对人工确认为恶意的拦截(避免误杀)。

【链接】https://socket.dev ｜ https://www.theregister.com/2025/09/30/socket_will_block_it_with/

【已知坑】不查本地已缓存的产物——用 `sfw` 前应先清缓存；遥测会收集机器 ID、被拦包信息、GitHub org 名(付费可配)。socket.dev 主站对抓取返回 403，细节取自 The Register 报道。

---

## Cisco AI Defense — MCP Scanner (开源)

【是什么】扫 MCP(Model Context Protocol)服务器及其 tools/prompts/resources/instructions 的安全威胁，保护 AI 代理供应链。Apache 2.0，Python 3.11+，PyPI 包 `cisco-ai-mcp-scanner`。

【可复用方法】
- 三大分析引擎可单用或合用：①YARA 分析器(规则匹配可疑代码，无需 API key，适合离线/CI) ②LLM-as-Judge(GPT-4o/Claude 做语义分析，抓 prompt injection、tool poisoning) ③Cisco AI Defense API(云端 inspect)。
- 附加分析器：VirusTotal(SHA256 查恶意文件)、行为代码扫描(检"docstring 声称 vs 实际实现"的行为不符，多语言)、pip-audit 查依赖 CVE、就绪性扫描(20 条启发式查超时/重试/错误处理)、Prompt Defense(正则查 12 类攻击的缺失防护)。
- 威胁分类(AITech/AISubtech)：prompt injection、tool poisoning、命令注入、数据泄漏、角色逃逸/间接注入、输出武器化、多语言绕过/Unicode 同形字、上下文溢出、社工、恶意包注入。分级 HIGH/MEDIUM/LOW/SAFE。
- CLI：
  ```bash
  mcp-scanner --scan-known-configs --analyzers yara --format summary
  mcp-scanner --server-url https://mcp.example.com/mcp --analyzers yara
  mcp-scanner stdio --stdio-command uvx --stdio-arg mcp-server-fetch --analyzers yara
  mcp-scanner-api --host 0.0.0.0 --port 8080   # REST 服务
  ```
  输出格式 summary/detailed/table/by_severity/raw JSON。

【链接】https://github.com/cisco-ai-defense/mcp-scanner ｜ https://blogs.cisco.com/ai/securing-the-ai-agent-supply-chain-with-ciscos-open-source-mcp-scanner ｜ https://cisco-ai-defense.github.io/

【已知坑】YARA 与就绪性扫描无需 key；LLM/API/VirusTotal 引擎需对应凭据。

---

## Cisco AI Defense — Skill Scanner (开源, 扫 agent skill)

【是什么】专扫「Agent Skill」(SKILL.md + 脚本)的安全扫描器，查 prompt injection、数据外泄、恶意代码。PyPI 包 `cisco-ai-skill-scanner`，CLI 名 `skill-scanner`。明确声明只做 best-effort：**「无发现≠无威胁，覆盖天然不完整，高风险部署仍须人工复核」**——这正是自检要内化的诚实姿态。

【可复用方法/真实命令】
- 8 个分析引擎，可单用/合用：Static(YAML+YARA 模式，无需 key)、Bytecode(.pyc 完整性)、Pipeline(shell 管道命令污点分析)、Behavioral(Python AST 数据流)、LLM(语义分析 SKILL.md+脚本，需 key)、Meta(假阳过滤，需 key)、VirusTotal(二进制哈希查毒)、AI Defense(云端)；另有 Trigger 分析器查「描述过于含糊」。
- CLI 子命令：`scan <dir>`(单技能)、`scan-all ./skills --recursive --check-overlap`(批量+查跨技能描述重叠/冲突)、`generate-policy`/`configure-policy`(策略模板/TUI)、`list-analyzers`、`validate-rules`。
- 典型用法：
  ```bash
  skill-scanner scan /path/to/skill --use-behavioral --use-llm --use-aidefense
  skill-scanner scan /path --use-llm --llm-consensus-runs 3   # LLM 多轮共识降假阳
  skill-scanner scan-all ./skills --fail-on-severity high --format sarif --output r.sarif  # CI
  skill-scanner scan .claude/commands/deploy --lenient        # 扫非标准格式(Claude 命令)
  ```
- 严重级：`--fail-on-severity` 取 critical/high/medium/low/info；`--fail-on-findings` 等价于 HIGH 或 CRITICAL 即失败。
- 输出格式：summary/json/markdown/table/sarif/html(自含交互报告，带可折叠关联组、可展开代码片段、管道污点流图)。
- 集成：GitHub Actions(PR 内联注解+Code Scanning)、pre-commit 钩子(只扫暂存的技能目录)、Python SDK(`SkillScanner` 类)、策略预设 strict/balanced/permissive。
- 原生支持 OpenAI Codex / Cursor Agent Skills(遵循 agentskills.io 规范，默认认 SKILL.md，可 `--skill-file` 覆盖)；`--lenient` 才扫 Claude Code 命令等非标准格式。

【链接】https://github.com/cisco-ai-defense/skill-scanner ｜ https://pypi.org/project/cisco-ai-skill-scanner/ ｜ https://blogs.cisco.com/ai/introducing-the-ai-agent-security-scanner-for-ides-verify-your-agents

【已知坑】自承「coverage inherently incomplete」、对零日/新手法尤其弱，假阳假阴都会有；默认只认带 SKILL.md 的标准格式，扫 Claude `.claude/commands/*.md` 必须加 `--lenient`，否则漏扫。批评者(Snyk/Trail of Bits)指出「skill 扫描器本身可能给人虚假安全感」，应作多层防御之一而非唯一防线。

---

## 横向可复用模式总结

1. **三态判定**：通过/失败/警告(Deepchecks condition) ≈ 安全分级 HIGH/MED/LOW/SAFE(Cisco) ≈ Critical/Important/Minor(code-review)。自检清单每项都该落到明确判定，而非含糊感受。
2. **证据闸门**：下结论前必须有当场跑出的证据(verification-before-completion)。
3. **根因优先 + 失败循环熔断**：修≥3 次停手质疑架构(systematic-debugging)。
4. **对抗式评审维度打分**：可操作性/具体性/论证/解法/语气(PRISM MCS)，致命问题排前(nCPS)。
5. **结论须被证据支撑**：同行评审最经典失败点，对应自检的「夸大」与「事实」项。
