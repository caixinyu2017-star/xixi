# light-frontend-design 参考工具研究笔记

逐工具核查笔记，供 SKILL.md 引用。研究日期 2026-06-06。
标注【是什么】【可复用方法】【链接】【已知坑/局限】。未核实的会明确写出。

---

## frontend-design skill (Anthropic)

【是什么】Anthropic 官方/社区版前端设计技能，目标是生成"独特、production-grade"的界面，反对 AI 默认的同质化"安全"审美。核心论点：AI 编码默认收敛到通用审美，解法是全力押注一个明确创作方向并精确执行。

【可复用方法】
- 四问设计思考框架（写码前必答）：Purpose(解决什么问题/谁用)、Tone(选定基调)、Constraints(框架/性能/可访问性)、Differentiation("有什么会被记住的唯一点")。
- 基调谱系可选：brutally minimal / maximalist / retro-futuristic / organic / luxury / playful / editorial / brutalist / art deco / soft-pastel / industrial。
- "意图大于强度"：极繁与极简都成立，关键是刻意执行；代码复杂度要匹配视觉雄心。
- 字体：避开 Arial/Inter/Roboto/系统字体，选有个性的展示字配精炼正文字。
- 配色：用 CSS 变量；"主色 + 锐利强调色" 优于均匀分布的怯懦调色板。
- 动效：HTML 优先纯 CSS，React 用 Motion 库；"一次编排良好的页面载入 + 错峰揭示(animation-delay)" 比散落的微交互更有记忆点。
- 背景：用 gradient mesh、noise 纹理、几何图案、分层透明、戏剧化阴影、自定义光标、grain overlay 制造氛围与纵深，别只填纯色。

【明确禁止(anti-pattern)】Inter/Roboto/Arial/系统字体；紫色渐变配白底；可预测布局与千篇一律组件；缺乏语境个性的"模板感"；不同项目反复收敛到同一选择(点名 Space Grotesk)。

【链接】
- https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
- https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md

【已知坑/局限】偏 landing/展示页审美，对密集信息后台、可访问性细则着墨少；"大胆"导向需要人工把关，避免炫技压过可用性。

---

## web-design-guidelines (Vercel)

【是什么】Vercel 出的 100+ 条可执行 web 设计规则集，分七类：Accessibility、Performance、UX Patterns、Typography、Color & Contrast、Responsive、Interaction。偏"硬规则 checklist"，与 frontend-design 的"审美方向"互补。

【可复用方法/真实规则】
- 可访问性(WCAG 2.1 AA)：所有交互元素键盘可达；图片需有意义 alt(装饰图 alt="")；颜色不能是唯一信息载体；焦点指示清晰可见；ARIA role 正确。
- 性能(Core Web Vitals)：首屏 LCP 图 eager 加载；避免字体替换/动态内容引起的 layout shift；图片用 WebP/AVIF；盯 LCP/CLS/INP。
- UX：错误信息要说明"哪里错了+怎么修"；加载态在用户操作后 100ms 内出现；空状态要引导下一步而非只说"暂无数据"。
- 交互：必须定义 hover 态；交互元素必须有焦点指示；尊重 prefers-reduced-motion。
- 响应式：定义断点；触控目标足够大；移动优先。

【链接】
- https://skills.pawgrammer.com/skills/vercel-web-design-guidelines
- https://www.claudepluginhub.com/plugins/vercel-labs-vercel-web-design-guidelines

【已知坑/局限】是规则清单非生成器，不给具体数值(如确切对比度数字在页面未全列)，需配合实际工具(Lighthouse/对比度检测)落地。

---

## vercel-composition-patterns (Vercel Labs agent-skills)

【是什么】教 React/Next.js 组件组合模式，核心主张：用组合替代布尔属性堆砌(boolean prop proliferation)，让组件 API 在规模化时对人和 AI 都更易维护。按优先级三档分类。

【可复用方法/具体规则】
- 组件架构(HIGH)：`architecture-avoid-boolean-props`(别加布尔属性定制行为，用组合)、`architecture-compound-components`(用共享 context 组织复杂组件)。
- 状态管理(MEDIUM)：`state-decouple-implementation`(只有 Provider 知道状态怎么管)、`state-context-interface`(用 {state, actions, meta} 泛型接口做依赖注入)、`state-lift-state`(状态上提到 provider 供兄弟组件共享)。
- 实现模式(MEDIUM)：`patterns-explicit-variants`(造 PrimaryButton/GhostButton 显式变体而非 primary/secondary 布尔模式)、`patterns-children-over-render-props`(用 children 组合优于 renderX props)。
- React 19(仅 19+)：`react19-no-forwardref`(别用 forwardRef；用 use() 替代 useContext())。
- 典型重构：Toggle 一堆布尔标志 → ToggleProvider + Toggle.On/Toggle.Off；Modal 库用 Modal/ModalHeader/ModalBody + 共享 open/close context。

【链接】
- https://playbooks.com/skills/vercel-labs/agent-skills/composition-patterns
- https://skills.browseract.com/skills/vercel-labs-agent-skills-vercel-composition-patterns

【已知坑/局限】聚焦客户端 React 组件 API 设计，不涉及 server/client 边界或 slot 模式；compound components 滥用会增加心智负担，简单组件不必上。

---

## ui-ux-pro-max (nextlevelbuilder)

【是什么】"设计智能"技能，靠推理引擎 + 知识库(161 行业规则 / 67 UI 风格 / 57 字体配对 / 161 调色板 / 24 落地页模式 / 25 图表类型 / 99 UX 准则 / 15 技术栈)，把自然语言项目需求映射成完整设计系统。

【可复用方法/工作流】
- 四阶段 pipeline：用户请求 → 多域并行检索(产品类型/风格/调色板/落地页模式/字体) → 推理引擎(BM25 排序风格优先级 + 按行业过滤反模式) → 输出设计系统。
- 每条行业规则含六维：Recommended Pattern / Style Priority / Color Mood / Typography Mood / Key Effects / Anti-Patterns。
- 设计系统输出结构：Pattern(落地页结构如 Hero-Centric+Social Proof) + Style + Colors(主/辅/CTA/背景/文字 各带理由) + Typography(配对+情绪+Google Fonts 链接) + Key Effects + Anti-Patterns + 交付前 checklist。
- 交付前 checklist(直接可抄)：不用 emoji 当图标(用 SVG: Heroicons/Lucide)；所有可点元素 cursor-pointer；hover 态平滑过渡 150-300ms；浅色文字对比 ≥4.5:1；键盘焦点态可见；尊重 prefers-reduced-motion；响应式断点 375/768/1024/1440px。
- 持久化：design-system/MASTER.md 作全局真相源，design-system/pages/<page>.md 做页级覆盖(页级覆盖 Master，无页文件则用 Master)。
- 行业反模式举例：银行类避开 "AI 紫/粉渐变"；CTA 放首屏并在 testimonials 后重复。

【链接】https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/README.md

【已知坑/局限】知识库规模与"BM25"为其自述，实际匹配质量依赖规则库覆盖；产出是设计系统建议非成品代码。

---

## sleek-design-mobile-apps (sleekdotdesign/agent-skills)

【是什么】把 Claude 接到 Sleek 的 AI 移动端设计平台 REST API，用自然语言描述屏幕 → 异步生成 → 拿到真实 HTML/CSS 组件代码。定位是"要真实 mockup 而非描述/线框"的快速原型。

【可复用方法/工作流】REST 流程：创建项目 → 自然语言描述屏幕 → 平台异步生成 UI → 轮询完成 → 拉取最终 HTML/CSS。安装：`npx skills add https://github.com/sleekdotdesign/agent-skills --skill sleek-design-mobile-apps`。

【链接】https://claudemarketplaces.com/skills/sleekdotdesign/agent-skills/sleek-design-mobile-apps

【已知坑/局限】需 Pro plan API key(带相应 scope)，依赖第三方平台与额度；公开页未暴露 SKILL.md 内部设计规则细节(间距/手势/导航数值未核实)。移动端具体设计规范建议改用下方 mobile-app-design / Apple HIG / Material Design 3。

---

## canvas-design / Claude Design (jiji262/claude-design-skill)

【是什么】把 Claude 变成 HTML 制品设计专家：landing page、slide deck、交互原型、动画视频、海报、线框。改编自 Claude.ai 内部 Design 系统提示，环境无关。

【可复用方法】
- Priority #0 事实核查：设计涉及具名产品先 web 搜索("10 秒搜索胜过 1-2 小时返工")。
- Context-First：好设计长在已有语境(品牌/代码库/UI kit)上而非凭空造；Core Asset Protocol 把 logo/产品图/UI 截图当一等公民，结果写入 brand-spec.md。
- Advisor Mode：简报太空(如"做个好看的")时，从"5 学派 10 设计哲学"提 3 个差异化方向让用户选。
- 先声明视觉系统(字体/色彩/间距规则)再落像素；变体策略从 conservative → novel，可在原型里加实时调色/字体/变体控件。
- 风格库结构：每条含 pitch / flagship / keywords / signature moves / when-to-use(如 Swiss Editorial: 超大页码、发丝级分隔线、单一强调色；Kenya Hara 极简；Brutalist web；Editorial magazine)。
- 输出骨架：slide deck 带缩放/导航/localStorage 持久化/打印 PDF/键盘导航/1-indexed 页标；交互原型用 React+Babel(锁版本+SRI)；动画用 Stage/Sprite/useTime/interpolate/Easing。
- 验证纪律：标记完成前确认制品在真实浏览器干净加载(verification.md)。

【明确禁止(anti-slop)】激进渐变、emoji 项目符号、rounded-cards-with-left-border、CSS 剪影冒充产品图、gradient-orb 代表 AI 等"机器生成的破绽"。React+Babel 内联 JSX 坑：style 对象作用域冲突、Babel 作用域隔离、integrity hash、必须锁库版本。

【链接】https://github.com/jiji262/claude-design-skill

【已知坑/局限】偏单文件 HTML 制品(artifact)，非大型工程化前端；React 内联原型有上述脆弱点。

---

## design-taste-frontend / minimalist-ui / high-end-visual-design (leonxlnx/taste-skill)

【是什么】"Anti-Slop Frontend Framework for AI Agents"——给 AI 注入设计品味，阻止生成无聊通用的 slop。规则针对设计意图非单一框架 API，兼容 React/Vue/Svelte 与 Codex/Cursor/Claude Code。design-taste-frontend、minimalist-ui、high-end-visual-design(soft-skill 系列)均属该 repo 的风格变体。

【可复用方法】
- 三个旋钮(1-10，文件顶部)：DESIGN_VARIANCE(布局实验度，低=居中/干净 高=非对称/现代)、MOTION_INTENSITY(动效深度，低=hover 高=scroll/magnetic)、VISUAL_DENSITY(每屏信息量，低=空旷 高=密集仪表盘)。
- v2 机制：读简报→推断设计语言→调三旋钮；硬性 em-dash 禁令；canonical GSAP 代码骨架；redesign-audit 协议 + 严格 pre-flight 检查。
- 风格变体(各为独立可装 skill)：soft-skill = `high-end-visual-design`(打磨、平静、昂贵感，低对比+留白+高级字体+spring motion)、minimalist-skill = `minimalist-ui`(Notion/Linear 编辑风，克制配色+清晰结构)、brutalist-skill = `industrial-brutalist-ui`(Swiss 字体+硬对比+实验布局)。另有 `gpt-taste`(更激进 anti-slop)。
- 审查维度(redesign-skill = `redesign-existing-projects` 的 redesign-audit 协议，先读现有代码再按轴修)：Layout(结构构图)、Spacing(节奏/呼吸)、Hierarchy(视觉权重/阅读顺序)、Styling(色/字/表面处理)。
- 图像管线(image-to-code-skill = `image-to-code`)：Generate(出参考板，可用 ChatGPT Images)→ Analyze(分析版式/字体/间距/动效线索)→ Implement(照参考帧出码)。配套 `imagegen-frontend-web`/`imagegen-frontend-mobile`/`brandkit` 生成参考板。

【链接】
- https://github.com/leonxlnx/taste-skill
- https://claudemarketplaces.com/skills/leonxlnx/taste-skill/design-taste-frontend
- https://claudemarketplaces.com/skills/leonxlnx/taste-skill/minimalist-ui

【已知坑/局限】high-end-visual-design / minimalist-ui 经核实即该 repo 的具名变体(分别对应 soft-skill / minimalist-skill)；强 anti-slop/高 variance 可能与企业级规范冲突，需按场景调旋钮。

---

## mobile-app-design (awesome-skills) — sleek-design-mobile-apps 的规范补充

【是什么】移动端 UI/UX 设计技能，覆盖 iOS HIG、Material Design 3、WCAG 2.1 AA，用原子设计法组织，带可执行校验脚本。

【可复用方法/真实数值】
- 触控目标：iOS ≥44×44pt；Android ≥48×48dp(strict 模式校验 48×48)。
- 字号：正文 ≥16sp/pt；标签 ≥11pt。
- 对比度(WCAG AA)：正文 4.5:1；大字 3:1；UI 组件 3:1。
- 导航：iOS=返回左上/操作右上/tab 底部，底 tab 3-5 项；Android=返回左上/菜单右上/FAB 右下。
- iOS 用 SF 字体、large title、haptic、swipe、VoiceOver；Android 用 Roboto、bottom nav/drawer、FAB、ripple、TalkBack。
- 无障碍：每个交互元素要 accessibilityLabel/Role/Hint + 合理焦点顺序。
- RN 性能：FlatList 用 getItemLayout/removeClippedSubviews/windowSize/maxToRenderPerBatch；React.memo + useCallback + useMemo。
- 校验工具：check-contrast.py、validate-touch-targets.sh、accessibility-audit.sh。

【链接】https://github.com/awesome-skills/mobile-app-design

【已知坑/局限】偏 React Native；纯 web 移动端需按 web 触控/视口习惯微调。

---

## shadcn/ui

【是什么】不是 npm 组件库，而是把组件源码直接拷进项目的"copy-paste + registry"方案，配 CLI 拉取放置文件，基于 Radix(或 base) + Tailwind。完全可改源码。

【可复用方法/真实命令】
- `npx/pnpm dlx shadcn@latest init` 初始化：装依赖、cn 工具、CSS 变量。选项 `-t <next|vite|start|react-router|laravel|astro>`、`-b <radix|base>`、`-d/--defaults`(template=next, preset=nova)、`--css-variables/--no-css-variables`(默认开)、`--monorepo`、`--rtl`、`--pointer`(按钮 cursor)、`--reinstall`、`-f` 强制覆盖。`create` 是 `init` 的别名。生成 components.json(记录框架/基库/CSS 变量/RTL/UI 目录/monorepo)。
- `shadcn@latest add [component]`：可按名/URL/本地路径加；`-a` 全加、`-o` 覆盖、`-p <path>` 自定义路径、`--dry-run` 预览、`--diff [path]` 看 diff、`--view [path]` 看源码、`-y` 跳过确认。
- 主题默认走 CSS 变量；global CSS 引入 tailwindcss + tw-animate-css + shadcn/tailwind.css(提供 data-open:/data-closed: 等变体与动画)。
- 自建分发：registry.json 定义自己的 registry，`build` 生成到 public/r；`view`/`search` 支持命名空间 registry(@shadcn/@v0/@acme)。
- `migrate radix|icons|rtl` 做迁移(如 ml-4→ms-4)；`eject` 把 shadcn/tailwind.css 内联并移除依赖(不可逆)。

【链接】
- https://ui.shadcn.com/docs/cli
- https://ui.shadcn.com/docs/installation

【已知坑/局限】组件进了你的代码库就由你维护(升级需手动 diff)；与 Tailwind v4 配套(tw-animate-css)；`eject` 不可逆。

---

## next-best-practices (Next.js 官方 production checklist)

【是什么】Next.js App Router 生产优化最佳实践(官方 production checklist，v16 文档)。

【可复用方法/具体规则】
- 默认即优化：Server Components 默认(无客户端 JS 体积)、按路由段代码分割、视口内 `<Link>` 预取、build 期预渲染并缓存、多层缓存。
- 渲染：用 layout 共享 UI 做局部渲染；自定义 error/404；检查 `"use client"` 边界位置避免膨胀客户端 bundle；cookies/searchParams 等 request-time API 会把整路由(在 root layout 用会是整应用)打入动态渲染，需有意使用并用 `<Suspense>` 包裹。
- 数据/缓存：Server Components 取数；Client Components 用 Route Handlers 访问后端，但别在 Server Component 里调 Route Handler(多一次请求)；用 loading.tsx + Suspense 做流式;并行取数避免瀑布;非 fetch 取数用 unstable_cache。
- UI/可访问性：Server Actions 处理表单+服务端校验；app/global-error.tsx 与 app/global-not-found.tsx；next/font 模块自托管字体防 layout shift；`<Image>` 自动优化+防 CLS+WebP；`<Script>` 延迟第三方脚本；eslint-plugin-jsx-a11y。
- 安全：taint 防敏感数据泄到客户端；每个 Server Action 内做鉴权(别只靠 layout/page 检查)，DB 访问放 server-only 数据访问层 + 限流;.env 入 .gitignore，仅 NEXT_PUBLIC_ 前缀的公开;加 CSP。
- SEO：Metadata API + OG image + sitemap/robots。
- 上线前：`next build` 抓错 + `next start` 测；Lighthouse(隐身)；useReportWebVitals 上报 Core Web Vitals；@next/bundle-analyzer 分析包体。

【链接】https://nextjs.org/docs/app/building-your-application/deploying/production-checklist

【已知坑/局限】request-time API 误用会把整应用打成动态渲染，损失静态优化；Partial Prerendering 仍实验性。

---

## Awwwards

【是什么】网页设计奖项/灵感库(Site of the Day 等)，给前端审美提供高水准参照与可量化评审维度。

【可复用方法/评审权重(可直接当自评 rubric)】Design 40% / Usability 30% / Creativity 20% / Content 10%。评分阈值：陪审 6.5+ 得 Honorable Mention，最高分得 SOTD，开发奖需 >7。机制：每站 ≥18 名评委、自动剔除偏离均值最远的 3 个分、投票 5 天。

【链接】https://www.awwwards.com/about-evaluation/

【已知坑/局限】奖项偏视觉创意(Design+Creativity 占 60%)，落地系统/后台不能照搬其炫技导向；学版式与交互思路，不抄具体设计。

---

## Mobbin

【是什么】"全球最大 UI/UX 设计参照库"，收录 iOS/Android/web 真实生产 App 的截图、用户流程(video flows)与设计模式。区别于 Dribbble 的精修 mockup——这是真实在用的界面。

【可复用方法】按 section/category/style 过滤；研究头部产品如何处理具体 flow(登录/onboarding/支付等)做 benchmarking；含 Figma 集成与按时序展示的流程视频。用法：先在 Mobbin 找 2-3 个同类真实流程对照，再定本项目的信息架构与交互顺序。

【链接】https://www.producthunt.com/products/mobbin

【已知坑/局限】需订阅；搜索精度一般，有时难精确命中；是研究/benchmark 工具非生成器，参考而非复制。

---

## Tailwind CSS (v4)

【是什么】utility-first CSS 框架；v4 改为 CSS-first 配置，按需扫描源码生成 CSS。

【可复用方法/真实用法】
- 配置在 CSS 里：`@import "tailwindcss";`，参数如 `@import "tailwindcss" prefix(tw);` / `important`。主题用 @theme 暴露成 CSS 变量，自定义 CSS 直接 `var(--color-violet-500)` / `--spacing(5)` / `var(--font-weight-semibold)`。
- 变体可叠：`hover:` `disabled:` `dark:`(默认走 prefers-color-scheme) `sm:`(默认 40rem，移动优先) `group-hover:` `data-current:`，可堆 `dark:lg:data-current:hover:bg-indigo-600`。
- 任意值：`bg-[#316ff6]`、`grid-cols-[24rem_2.5rem_minmax(0,1fr)]`、`max-h-[calc(100dvh-(--spacing(6)))]`、任意变量 `[--gutter:1rem]`、内联变量 `bg-(--bg-color)`。
- 强制：`bg-red-500!`(!important)。
- 冲突规则：同属性"样式表中靠后者"胜(不是 class 属性里靠后)。
- 复用别滥抽 class：用循环/组件/模板片段管理重复，@layer components 只留按钮等简单元素。

【链接】https://tailwindcss.com/docs/styling-with-utility-classes

【已知坑/局限】v4 与 v3(tailwind.config.js)配置范式差异大，迁移需注意；class 顺序不决定优先级(易踩坑)；与 shadcn 配套需 tw-animate-css。
