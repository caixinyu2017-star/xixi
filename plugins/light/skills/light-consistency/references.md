# light-consistency 参考工具研究笔记

研究日期：2026-06-06。本文档为逐工具核查笔记，供 SKILL.md 引用。
说明：本次研究环境下 WebFetch 被全域拦截，以下信息基于官方文档检索结果（WebSearch 摘要）+ 公开规范。凡无法可靠核实的，明确标注【未能核实】，未编造端点或字段。

---

## distill skill（内容压缩/提炼）
【是什么】写作类技能动词，把长材料压缩为更短版本同时保留核心信息（贡献点、结论、关键数字）。常见于 "marketing-skills" / "one-person marketing team" 这类社区 Claude skill 合集中，与 polish/audit/critique 成组出现。
【可复用方法】一致性场景下的用法：把"创新点 3 条标准措辞"从论文长段落 distill 成 PPT 一句话 / 软著一段话，但要求**信息不丢、提法不变**。提炼时锁定三要素不可改写——方法名、指标名、数值。先抽取要点清单，再按目标载体长度重排，最后回比原文校验"有没有新增/丢失主张"。
【链接】https://opentools.ai/resources/marketingskills ；合集介绍 https://theautomationexchange.beehiiv.com/p/issue-58-this-one-person-marketing-team-repo-just-went-viral
【已知坑/局限】压缩时最易制造不一致：同义改写会把"统一术语"换成近义词、把"F1"写成"准确率"。distill 后必须过术语表回扫。该 skill 的确切 SKILL.md 内部实现【未能核实】（仓库页面无法抓取），以上为基于命名约定与摘要的功能推断。

## polish skill（语言润色）
【是什么】对既有文本做语言层打磨（语法、流畅度、语气统一），不改变事实主张。同属上述写作 skill 合集。
【可复用方法】一致性用途：跨材料统一"语气/人称/时态"。可借鉴的评审动作——逐句检查是否引入新事实、是否替换了受控术语、中英混排是否规范。润色应是"零事实变更"操作，改动范围限定在词法/句法。
【链接】https://opentools.ai/resources/marketingskills
【已知坑/局限】润色会悄悄改专有名词大小写、连字符（如 "fine-tune" vs "finetune"），破坏术语一致。须把受控词表作为"禁改清单"传入。确切实现【未能核实】。

## audit skill（内容审计）
【是什么】对一批内容做盘点+差距分析，输出问题清单。营销语境是内容盘点/覆盖率/语气一致性审计；迁移到科研即"跨材料一致性审计"。
【可复用方法】可直接借鉴的审计维度（来自营销内容审计方法论）：①清单化盘点每份材料的关键主张；②逐项打标签（一致/冲突/缺失）；③量化覆盖率（哪些贡献点在 PPT 缺席）；④输出可执行修正项而非泛泛评价。即"inventory → tag → gap → fix"四步。
【链接】内容审计方法 https://www.imcgrupo.com/how-automated-content-analysis-supports-marketing-consistency/ ；审计清单法 https://themarketingfix.substack.com/p/free-library-95-marketing-audit-questions
【已知坑/局限】审计易停在"列问题"不给修正。一致性报告必须带"统一建议+修正后文本"。skill 内部实现【未能核实】。

## critique skill（评审/批判）
【是什么】对单份产出做结构化批判，给出优缺点与改进方向；偏"质量评审"而非"事实核对"。
【可复用方法】借鉴其"分维度打分+具体证据引用"模式：每条批评须指向具体位置（章节/页/行），给出"现状→问题→建议"三段式。用于一致性时，把维度替换为术语/指标/创新点/视觉/逻辑五维。
【链接】https://opentools.ai/resources/marketingskills
【已知坑/局限】critique 输出主观性强，需绑定客观锚点（术语表、指标表）才能复现。实现细节【未能核实】。

## full-output-enforcement（完整输出强制）
【是什么】一类"约束 skill"，强制模型输出完整内容而非省略/截断（如 "...（其余略）"、占位符、TODO）。在长文档/批量改写时防止偷工。
【可复用方法】一致性报告与批量修正稿最怕"截断"——只改了前 3 处不一致就收尾。可借鉴的强约束写法：明令"逐条列全、不得用省略号代替、不得写'其余同理'"，并在末尾自检"清单条数 = 实际处理条数"。
【链接】合集见 https://www.claudepluginhub.com/plugins/kylemarham-marketing-skills （插件聚合页）
【已知坑/局限】过度强制会让输出冗长；应只对"清单/修正稿"强制完整，对"说明性文字"不强制。确切 prompt 文本【未能核实】。

## content-strategy（内容策略）
【是什么】营销 skill，先定义受众/核心信息/信息支柱(message pillars)/品牌语气，再产出内容，确保所有材料"同源同调"。
【可复用方法】这正是一致性的上游：先建"单一事实源(single source of truth)"再分发。可借鉴——把"创新点 3 条 / 方法名 / 指标定义 / 品牌语气"固化为一份 brand/定义文件，所有下游材料从它派生（对应 Light 的 db09 术语表）。"先定义后生产"避免事后纠偏。
【链接】品牌信息支柱与语气 https://www.blockchain-council.org/claude-ai/ai-driven-branding-with-claude-ai-brand-voice-messaging-pillars-style-guides/ ；"不再每次重讲品牌"系统 https://medium.com/@valentin.marin83/our-marketing-team-stopped-re-explaining-the-brand-to-ai-every-session-f7670a9d3d39
【已知坑/局限】定义文件一旦过期，下游全错；须设"定义变更即广播回扫"机制。skill 实现【未能核实】。

## Markdown & Mermaid Writing（含 mermaid-syntax-skill）
【是什么】用 Markdown + Mermaid 在文档里画"代码即图"的流程图/时序图等，保证图随文本版本化、可 diff、风格统一。mermaid-syntax-skill 是专门生成"无语法错误 Mermaid"的 Claude skill。
【可复用方法/真实语法】图类型与起始关键字：`flowchart TD`/`graph LR`（流程图，方向 TD/TB/LR/RL/BT）、`sequenceDiagram`（时序）、`classDiagram`、`stateDiagram-v2`、`erDiagram`、`gantt`、`gitGraph`、`pie`。节点形状：`[]`矩形、`()`圆角、`{}`菱形判定、`[()]`圆柱(库)。连线：`-->`实箭头、`-.->`虚线、`==>`粗线、`--文字-->`带标签。子图用 `subgraph ... end`。一致性价值：所有材料用同一套 Mermaid 主题/方向/命名，图风格自动统一。
【链接】官方语法 https://mermaid.js.org/syntax/flowchart.html 、https://mermaid.js.org/syntax/sequenceDiagram.html ；无错生成 skill https://github.com/awesome-skills/mermaid-syntax-skill
【已知坑/局限】节点文字含特殊字符（`()`、`:`、`#`、引号）会渲染失败，须用 `["..."]` 双引号包裹或 `#35;` 实体转义；中文标点（全角括号）常致解析错误；subgraph 内 id 不能与外部重名。生成后务必走一次渲染校验。
【对标记录(2026-06-06 本机 curl 实测)】仓库 `github.com/awesome-skills/mermaid-syntax-skill` 结构已抓取：`SKILL.md` + `scripts/validate-mermaid.sh`(bash 正则校验，11 项检查) + `examples/{flowchart,sequence}-examples.md` + `references/*.md`。其 validate 脚本仅对**单份** Mermaid 文本做正则语法检查(保留字/特殊字符/注释/frontmatter 等)。HTTP 实测：`raw.githubusercontent.com/.../main/SKILL.md` -> 200。本技能 `consistency_audit.py` 定位更高：跨**多份**材料做语义级一致性比对(受控术语替换/指标换名/指标数值冲突/覆盖缺口)，位置感知配对数值，给修正建议并自检条数，能力维度超出单文件语法校验。

## extract-design-system（提取设计系统）
【是什么】从既有网站/截图/代码反推出设计系统（调色板、字体、字号梯度、间距、圆角、阴影），产出结构化"设计语言"文档（如 DESIGN.md / 设计 token），供后续产物复用以保持视觉一致。属 frontend-design 类工作流的前置步骤。
【可复用方法】流程：①采集样本(现有论文图/PPT/前端)；②抽取原子属性——主色/辅助色/语义色、字族与字重、模块化字号比例(modular scale)、间距阶梯(4/8pt)、圆角/阴影；③归一成命名 token；④写入设计规范文件，所有新图表/前端/海报从中取值。这把"视觉一致"从主观变成可对照的清单。
【链接】DESIGN.md 规范法 https://medium.com/@yaro-code/generating-free-google-spec-design-md-specifications-for-your-ai-coding-agents-2231d79949b0 ；样例 https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/claude/DESIGN.md ；Claude frontend-design 指南 https://skywork.ai/blog/claude-frontend-design-skills-ultimate-guide/
【已知坑/局限】从截图取色受压缩/抗锯齿影响有偏差；提取出的"隐含规则"可能并非原设计意图，需人工确认主色与语义映射。Anthropic 官方该 skill 的确切 SKILL.md【未能核实】，方法基于 DESIGN.md/frontend-design 公开实践。

## Style Dictionary（设计 token 构建工具，v4）
【是什么】Amazon 开源的设计 token 构建系统：单一 token 源(JSON/JS) → 经 transform/format → 输出到多平台(CSS 变量、SCSS、JS、iOS、Android)。是"一处定义、多端一致"的工程化落点。
【可复用方法/真实配置】核心概念四件套：`source`(token 文件 glob)、`platforms`(各目标平台)、每平台含 `transformGroup`(预设转换组，如 `css`/`scss`/`js`/`android`/`ios`)或 `transforms`(自定义转换链)、`files`(输出文件+`format`)。内置 format 用斜杠命名：`css/variables`、`scss/variables`、`javascript/es6`、`android/resources`、`json/flat`。自定义转换用 `registerTransform({name, type, transform})`，自定义格式 `registerFormat`。v4 变化：ESM 优先、API 异步，配置常用 `export default`，构建 `await sd.buildAllPlatforms()`，`registerTransform` 的 name 写在对象内。
【链接】配置参考 https://styledictionary.com/reference/config/ ；预置转换 https://github.com/amzn/style-dictionary/blob/f2395f3d/docs/src/content/docs/reference/Hooks/Transforms/predefined.mdx ；npm https://www.npmjs.com/package/style-dictionary
【已知坑/局限】v3→v4 为破坏性升级（同步→异步、CJS→ESM），旧配置直接跑会报错；transformGroup 与 transforms 二选一，同时写后者覆盖前者；token 引用/别名解析顺序可能踩坑。

## Prettier（代码格式化器）
【是什么】"有主见(opinionated)"的代码格式化器，重排代码为统一风格，消灭团队风格争论。支持 JS/TS/CSS/HTML/JSON/Markdown/YAML 等。
【可复用方法/真实选项】核心选项与默认值：`printWidth`(80)、`tabWidth`(2)、`useTabs`(false)、`semi`(true)、`singleQuote`(false)、`quoteProps`("as-needed")、`trailingComma`(v3 默认 "all")、`bracketSpacing`(true)、`arrowParens`("always")、`endOfLine`("lf")、`proseWrap`("preserve")。配置文件 `.prettierrc`(JSON/YAML)/`.prettierrc.js`/package.json 的 `prettier` 字段；忽略文件用 `.prettierignore`。一致性用途：代码命名/格式统一，配合术语表保证"代码符号 = 论文符号"。
【链接】选项文档 https://prettier.io/docs/en/next/options.html
【已知坑/局限】Prettier 只管格式不管代码质量(需配 ESLint，且要 eslint-config-prettier 关掉冲突规则)；`printWidth` 是"目标"非硬上限；proseWrap 默认不重排 Markdown 散文，跨文档换行风格需显式设。

## EditorConfig（跨编辑器基础风格统一）
【是什么】用一个 `.editorconfig` 文件统一不同编辑器/IDE 的基础排版（缩进、换行、编码），多数编辑器原生或插件支持。比 Prettier 更底层、更语言无关。
【可复用方法/真实属性】根文件首行 `root = true`(停止向上查找)；按 glob 分节如 `[*]`、`[*.{js,py}]`、`[Makefile]`。常用键：`indent_style`(space/tab)、`indent_size`(数字)、`tab_width`、`end_of_line`(lf/crlf/cr)、`charset`(utf-8 等)、`trim_trailing_whitespace`(true/false)、`insert_final_newline`(true/false)。一致性用途：保证论文配套代码/脚本/配置在所有人机器上缩进与换行一致，避免 diff 噪声。
【链接】规范与属性 https://editorconfig.org （样例 https://github.com/pallets/jinja/blob/main/.editorconfig ）
【已知坑/局限】只覆盖基础排版，不做代码重排(与 Prettier 互补，二者 indent 设定须一致否则打架)；部分编辑器需装插件才生效；属性值大小写不敏感但建议小写。

## Design Tokens W3C（DTCG 设计 token 标准格式）
【是什么】W3C Design Tokens Community Group(DTCG)制定的跨工具 token 交换格式(JSON)，让 Figma、Style Dictionary、Tokens Studio 等以统一结构互通。
【可复用方法/真实结构】token 是带 `$value` 与 `$type` 的对象，可选 `$description`；嵌套对象即 token 分组(group)，`$type` 可在组上声明被子级继承。别名/引用用花括号路径：`"$value": "{color.brand.primary}"`。基础类型：`color`、`dimension`、`fontFamily`、`fontWeight`、`duration`、`cubicBezier`、`number`。复合(composite)类型：`typography`、`shadow`、`border`、`transition`、`gradient`、`strokeStyle`——其 `$value` 是子属性对象(如 typography 含 fontFamily/fontSize/fontWeight/lineHeight)。一致性用途：把"视觉规范"写成 DTCG token，论文图/PPT/前端/海报全部从同一 token 源取值。
【链接】DTCG 格式草案 https://www.designtokens.org/tr/drafts/format/ ；社区组 https://www.w3.org/community/design-tokens/
【已知坑/局限】格式仍是 draft，工具实现进度不一(`$type` 继承、composite 支持各家有差异)；`$` 前缀为保留字，自定义元数据须避开；与各厂商私有扩展混用易破坏可移植性。
