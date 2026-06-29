# light-frontend-design — 深度分析与同类对标

> 源：[`skills/light-frontend-design/SKILL.md`](../../../skills/light-frontend-design/SKILL.md) ｜ 分析日期 2026-06-13
> 一句话定位：把"好看的前端"从主观审美变成有方法论+机械门禁+反AI-slop黑名单的可判定工程,服务科研项目的答辩/大屏/后台/小程序展示界面。

## 核心运行逻辑
核心思路是"先定方向、再落 token、最后用脚本把好看判成可数的 Pass/Fail"。写码前强制回答四问(Purpose/Tone/Constraints/Differentiation)押注单一设计方向,据此定设计语言并落成 Design Tokens;配色字体不凭空造,而是从 db09 项目 palette.json / db05 design_tokens 这个跨制品视觉 SSOT 取值,保证前端与论文图(m11)、PPT(m16)同源不漂移。交付前必过两个 stdlib linter:audit_checklist.py 检查 6 条可数布局规则(eyebrow 数量/连续 split/布局家族多样性/hero 副文长度/nav 高度/bento 格数),ai_tell_lint.py 黑名单扫 4 类 AI 痕迹(scroll cue/编号 eyebrow/版本页脚/em-dash)。再叠 Awwwards rubric(Design40/Usability30/Creativity20/Content10)自评<6.5重做。整套知识从 Anthropic frontend-design、Vercel、taste-skill、canvas-design 等真实上游技能提炼并标注来源与坑。

## 关键步骤
- 1. 写码前四问定方向:Purpose/Tone(从基调谱系押注一个,涉及具名品牌先10秒web搜索)/Constraints/Differentiation(一个会被记住的记忆点)
- 2. 定设计语言→落 Design Tokens,登记 db05;项目有 db09 palette.json 则必用其取色,前端不另立色板
- 3. 按 brief 信号选唯一一套官方设计系统或 Tailwind+自有token(design-systems-map 决策树),版本 pin 死、一仓一套
- 4. 按场景拨三旋钮 VARIANCE/MOTION/DENSITY(大屏调高密度、落地页调高实验度、后台两者调低)
- 5. 实现:Next.js Server Components 优先 / Tailwind v4 CSS-first / shadcn 源码自持;需动效拷 assets/ 的 GSAP/Motion 骨架
- 6. redesign 场景走 4 步审计协议:detect(preserve vs overhaul)→4轴审计→preservation rules→modernisation levers→决策树
- 7. 交付前机械门禁:audit_checklist.py 6/6 + ai_tell_lint.py CLEAN + Awwwards 自评≥6.5 + 响应式四断点实测
- 8. 产出可运行代码+设计说明+截图,设计系统回写 db05/db09,与 a04 数据接口、a07 一致性衔接

## 自带资产
- scripts/audit_checklist.py — 6 条可数布局规则的 HTML linter(基于 data-* 标注),自带 GOOD/BAD 自测
- scripts/ai_tell_lint.py — 4 类 AI 痕迹黑名单正则扫描,自带 DIRTY/CLEAN 自测
- assets/gsap-sticky-stack.tsx — GSAP ScrollTrigger 粘性堆叠卡片骨架,含 prefers-reduced-motion 回退 + ctx.revert 清理
- assets/gsap-horizontal-pan.tsx — 滚动驱动横向 pan(pin+scrub),reduced-motion 回退原生 overflow
- assets/motion-scroll-reveal.tsx — framer-motion 错峰滚动揭示,useReducedMotion 关动效 + observer 自动清理
- references.md — 14 个上游工具/技能的逐条核查笔记(是什么/可复用法/链接/已知坑)
- references/ecosystem-2026.md — 热门技能雷达 + 前端栈版本快照 + 设计token工程化(Style Dictionary/Terrazzo)
- references/fonts-and-colors.md — 字体取用池 + 配对表 + 禁用字体(Fraunces/Instrument Serif) + 禁用色族(米色/黄铜/酱黑+紫粉渐变)含 hex
- references/design-systems-map.md — brief→8 套官方设计系统映射表 + 决策树 + pin 版本号
- references/redesign-audit.md — 改造已有项目的 5 步审计协议 + 改造vs重做决策树

## 优点
- 把抽象审美做成可数判定是真正的差异点:两个 linter 各带自测(GOOD/BAD、DIRTY/CLEAN),脚本本身自证可跑,不靠'看着不错'的手挥
- 反 AI-slop 立场具体且机械可查:禁用字体名、禁用色族连邻近 hex 一并列出,可直接 grep/lint,而非空喊'别做模板感'
- 溯源纪律强:references.md 对每个上游技能标【是什么/可复用法/链接/已知坑】,且每条都写了局限,不夸大上游能力(明确写'除非 assets 已装否则不声称上游检索在跑')
- 文件间职责边界写得清楚:db05 管风格卡、references.md 管工具硬信息、ecosystem 管版本时效快照,显式声明不互相复写,降低维护漂移
- 方法论可执行且来源可信:四问框架 + VARIANCE/MOTION/DENSITY 三旋钮 + redesign 4 轴审计,都是从可验证上游(frontend-design/taste-skill)提炼的成型套路
- asset 骨架默认内建可访问性与正确性:prefers-reduced-motion 回退 + gsap.context/ctx.revert 清理 + SSR-safe,把常见内存泄漏/SSR 坑预先堵上
- 跨制品视觉 SSOT 架构正确:前端配色与论文图/PPT 同取一份 palette.json/design_tokens,从架构上消除多制品风格漂移,这对科研项目一致交付很关键
- 设计系统选型有硬约束:一仓一套 + 版本 pin 死 + 决策树命中即停,直击真实的 token 冲突/双倍 bundle 问题

## 缺点 / 可被质疑处
- 机械门禁名不副实:audit_checklist 全靠 agent 自己给输出加 data-* 标注再校验自己的标注,是循环验证;nav 高度/bento 格数都是自声明属性而非从真实渲染测量,agent 漏标或错标即可让检查空过。号称'脚本即真相'但实际只验声明的元数据,不验真实 DOM
- 重度强调 WCAG 2.1 AA(4.5:1 等对比度反复出现)却不带任何对比度检测脚本:references 提到 mobile-app-design 有 check-contrast.py,本技能并未自带;'浅色文字对比≥4.5:1'只能靠人工,工具与宣称的严谨度脱节
- ai_tell_lint 误报面大且对中文不友好:T4 一刀切禁所有 em-dash 字符,会命中 CSS/JS 注释、字符串、以及中文正文里合法的破折号(本技能面向中文用户),无白名单;T3 版本正则会误杀 changelog/版本展示组件里的合法 semver
- assets 覆盖严重偏科:3 个骨架全是 landing 炫技向的滚动/动效效果,而 description 重点承诺的大屏/数据可视化/管理系统/小程序一个起手骨架都没有(无 ECharts/D3、无 shadcn 组件、无响应式布局、无表格/仪表盘),最该给科研后台/大屏的脚手架反而缺位
- 自带 tsx 骨架未经构建验证:文件自己注明'node --check 不解析 TSX,结构正确性即契约',即承认没编译过,与技能本身'交付前必跑 build+Lighthouse'的要求自相矛盾
- 版本快照是会腐烂的负债且部分数值可疑:next16.2.9/react19.2.7/tailwind4.3.0/lucide-react1.17.0/vite8.0.16 等为前瞻数字(lucide-react 1.17 与现实差距大),'curl 实测 HTTP 200'无法再核验,过期会误导 pin 版本
- 科研特化偏薄:作为'科研 AI 技能',内容绝大部分是通用产品/落地页设计;真正科研专属能力(论文图转交互、实验数据表、公式/LaTeX 渲染、引用/参考文献 UI、可复现实验可视化)几乎没有,科研味只体现在'学术感'tone + 答辩场景一句话
- 对 Light 生态强耦合、独立可用性差:db05/db09/a04/a07/m11/m16 等代号在 SKILL.md 大量出现却无内联解释,palette/token SSOT 工作流离开这些库无法运行,脱离整包几乎跑不起来,新读者认知负荷极高
- 无端到端示例:examples/ 目录为空,没有一个完整的标注页面或 before/after 走查样例,使用者只能从脚本自测里反推 data-* 该怎么标

## 可优化点（供后续逐技能优化）
- 给 audit_checklist 加真实渲染校验层:用 Playwright/Puppeteer headless 加载产物,从计算样式真测 nav 高度、对比度、触控目标尺寸、CLS,替代自声明 data-*;退一步至少加'未标注即 FAIL'的强制标注覆盖率检查,堵住空过
- 补一个 contrast_lint.py:解析 token/CSS 变量两两组合算 WCAG 对比度,正文4.5:1、大字3:1、UI3:1 直接判定,兑现 SKILL 反复承诺的对比度门禁
- 修 ai_tell_lint 的 em-dash 规则:排除代码注释/字符串与中文语境,或改为只在 data-role 正文节点内检测;T3 版本正则加 footer/页脚上下文限定,避免误杀合法 semver
- 补齐科研后台向 assets:加 ECharts/D3 大屏起手骨架、shadcn 数据表格、KPI 卡片栅格、空/加载/错误三态组件、响应式 dashboard 布局,匹配 description 承诺的大屏/管理系统/数据可视化
- 给 3 个 tsx 骨架接最小构建验证:配一个 tsc --noEmit 或 vite build 的 smoke 脚本(可放 scripts/),让'结构即契约'升级为'编译通过',与技能自身 build 要求一致
- 把易腐版本号从正文抽到单独的 versions.lock 并标注'仅快照、用前必跑 npm view 复检',或直接只留复检命令不写死可疑数字,降低误导
- 增厚科研特化:加论文配图转 web 交互、实验结果表格/误差棒可视化、公式渲染(KaTeX/MathJax)、引用与参考文献组件、数据集浏览器等科研专属模式卡与骨架
- 加一个 examples/ 端到端样例:一个完整标注好 data-* 的科研答辩页 + redesign before/after 走查,既当文档又当 linter 的真实回归用例
- SKILL.md 顶部加一段代号词表(db05/db09/a04/a07/m11/m16 各是什么),或在首次出现处内联一句注解,降低脱离整包时的认知门槛

## 与其他 Light 技能/知识库的衔接
["视觉 SSOT 取色:必用 db09-projects 下 <project>/palette.json,色值真相源锚定 db05 design_tokens.template.json(DTCG),前端不另立色板/字阶","风格实例卡:具体玻璃拟态/科研场景版式/官方系统落地模式等卡片在 db05(style_genre_cards/design_system_cards/resources_real),本技能只管选型方法论不复写卡片","一致性维护:同项目 palette 由 a07 统一,前端配色与 PPT(m16)、论文图(m11)同源协调,a07 维护 design_tokens","数据对接:前端数据接口对接 a04","技术实现细节:栈命令/参数/坑分流到同目录 references.md;版本时效快照分流到 references/ecosystem-2026.md","设计 token 多端编译:Style Dictionary/Terrazzo 从 db05 单一源编译到 CSS/JS/Tailwind,衔接论文图(db07)、PPT(db06)、前端(db05)","安全衔接:无鉴权接口风险提示对接 security_awareness;说明本包不含独立 light-miniprogram,小程序仅做 UI/视觉指导"]

---

## GitHub 同类前沿技能对标

同类分三层:一是把好看做成可执行脚本门禁的工程化技能(Light 最独特);二是反 AI-slop 提示词/规则集(taste-skill、hallmark),靠 prompt 黑名单,几乎无人提供能跑 Pass/Fail 的 linter;三是 DESIGN.md/设计系统投喂库(awesome-claude-design、bergside、open-design、huashu-design),靠塞美学风格提升出图,胜在数量与生态,弱在无可判定验收闭环。Light 差异化:四问押注方向、跨制品 token SSOT(与 m11 论文图/m16 PPT 同源)、两个 stdlib linter 机械判定加 Awwwards rubric 自评<6.5重做,且服务科研答辩/大屏/后台/小程序。弱点是 star/社区/风格库规模不及头部,且绑定 db09/db05 私有制品,通用性不如开箱即用 DESIGN.md 库。

| 项目 | 做什么 | Star | 最近更新 | 相比 Light |
|---|---|---|---|---|
| [anthropics/skills (frontend-design)](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | 官方 Agent Skills 仓库的前端设计技能,Light 核心上游,给审美原则与设计语言指导 | 149996(整仓) | 2026-06-09 | 权威生态最大、是 Light 根基;但只给通用原则,无可数布局脚本/AI-tell linter/跨制品 token。Light 加了机械门禁与科研锚点 |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 给 AI 注入品味、阻止通用 slop 的反 slop 框架,Light 上游 | 42465 | 2026-06-12 | 星数适配远超 Light;但偏提示词品味引导,缺 Pass/Fail linter 与可数布局门禁 |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 面向 Claude/Cursor/Codex 的反 AI-slop 设计技能 | 3062 | 2026-06-04 | 与 Light 反 AI-tell 高度重合;但偏规则提示词,无脚本数值验收与跨制品 token |
| [nexu-io/open-design](https://github.com/nexu-io/open-design) | 本地优先开源 Claude Design 替代品,桌面 App,259+ 技能、142+ 设计系统 | 64026 | 2026-06-13 | 数量碾压、生态活跃;但是广度平台,不做单页可数验收门禁,无论文图/PPT 视觉 SSOT |
| [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design) | HTML-native 的 Claude Code 设计技能,直接用 HTML 产出界面 | 18499 | 2026-06-06 | 中文热度高出图直观;偏生成 HTML,无脚本门禁/AI-tell 黑名单/跨制品 token |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | 配合 Stitch MCP server 的 Agent Skills 库,用于 UI 设计生成 | 5999 | 2026-06-04 | 背靠 Google Labs、MCP 集成强;但聚焦生成非可判定验收,无反 slop linter 与 rubric |
| [VoltAgent/awesome-claude-design](https://github.com/VoltAgent/awesome-claude-design) | 68 套即用 DESIGN.md 设计系统灵感,一份即可搭整套 UI | 2658 | 2026-04-18 | 风格库丰富即用、可作灵感源;但只是静态清单,无门禁/AI-tell 检测/跨制品同源 |
| [bergside/awesome-design-skills](https://github.com/bergside/awesome-design-md) | 67 个 DESIGN.md/SKILL.md 设计技能清单,覆盖 Claude/Stitch/Codex/Cursor | 1233 | 2026-05-25 | 聚合面广是好入口;是清单非可执行验收工具,无脚本门禁 |
| [hamen/material-3-skill](https://github.com/hamen/material-3-skill) | Material Design 3 的 Claude Code 技能,含 30+ 组件、design tokens、主题化 | 990 | 2026-05-21 | token/主题化与 Light 相通且组件成体系;但锁定 MD3、无反 slop 门禁、token 不跨论文图/PPT |
| [phazurlabs/ux-ui-mastery](https://github.com/phazurlabs/ux-ui-mastery) | 面向 Claude Code 的 UX/UI 设计大全插件,19 skills、55 references、31 万字 | 18 | 2026-02-14 | 体量大覆盖全流程可作参考;但 star 低偏文档堆叠,缺可执行数值门禁与反 AI-tell 脚本 |

### Light 该技能可借鉴的点
- 借鉴 awesome-claude-design/bergside 的按美学家族分类风格库,把方向押注扩成可选风格清单
- 参考 taste-skill/hallmark 的跨工具适配与品牌化,抽出不依赖 db09/db05 的通用版
- 学习 open-design 的本地沙箱预览加多格式导出,把 linter 验收与预览串成闭环
- 参考 material-3-skill 的组件加 token 加主题化打包,把 Design Tokens 扩成组件级
- 借鉴 stitch-skills 的 MCP 集成,把 audit_checklist.py/ai_tell_lint.py 暴露为可调用工具或 MCP
- 对标 tasteskill.dev 把 Awwwards rubric 阈值与样例公开增强可信度
