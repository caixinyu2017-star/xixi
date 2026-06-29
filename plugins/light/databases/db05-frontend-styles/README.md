# db05 — 前端设计风格库

搜集主流热门前端风格，训练 a05(前端设计) 的审美、布局、配色、组件能力。**学版式逻辑，不抄袭**。

> **职责边界（canonical）**：db05 是**风格实例卡片库**（一张卡=一套可迁移的视觉范式：风格名/色板/字体/token/代表实现/适用场景/禁忌）。"brief 信号→怎么选哪套设计系统"的**方法论**在 a05 的 `light-frontend-design/references/design-systems-map.md`。选型看 a05，找可套用的风格卡来 db05；两边不重复彼此内容。

## 这个库是什么(诚实卖点)

**不是**"18 设计卡 + 26 工具 license 认证库",而是**视觉范式本地精养 + 工具 license/版本实时核 + 偏科可过滤**的分层资产:

- **方法论/范式层(本地精养,护城河)**:18 张设计卡的 style_tag/layout_type/color_palette 逻辑/font_style/component_pattern 等 9 个学科中立范式字段 + design_tokens.template.json(DTCG 视觉 SSOT 模板) + 各卡范式专属 a11y 判断(玻璃拟态可读性/新拟物硬伤)。几乎不过时,是 a05 的真正消费对象。纯 WCAG 阈值/触控/栅格判据上抽到 a05 [visual-a11y-rules.md](../../skills/light-frontend-design/references/visual-a11y-rules.md) 一处维护。
- **薄缓存层(工具事实实时核)**:resources_real.md Part1 的 26 条工具,其 license/版本/链接是会变的事实——许可列为**快照、非认证事实**,npm 系工具用 [scripts/style_signal.py](scripts/style_signal.py) 实时查 registry.npmjs.org、冲突信在线;画廊/SaaS/Pro 定价层无 API,只存指针指向官方页、标 *待核查*、投产前人工核。无网降级标 stale。
- **偏科隔离层(可过滤)**:绝大多数 genre/设计系统卡是 general(对所有方向可见);带研究方向前提的卡以 `domain_scope=` 子串标注(如智慧农业平台卡 `domain_scope=agri-tech`),非该方向用户可过滤。无标注的卡默认 general。

## design_card schema
`project_type, style_tag, layout_type, color_palette, font_style, component_pattern, interaction_pattern, animation_type, screenshot_reference, implementation_notes, suitable_project_scene`

共 11 字段。偏科标 `domain_scope=` 以 catch-all 子串塞 suitable_project_scene,不占正式列、零 CI 改动。

## 数据来源
Mobbin、Awwwards、Dribbble、Behance、Lapa Ninja、Land-book、Godly、Siteinspire、CSS Design Awards、Pinterest、Figma Community、shadcn/ui、Tailwind UI、Vercel templates、GitHub frontend-design 类技能。

## 使用方式（重要）
不存图片本身，存**为什么好看 + 适合什么场景 + 可迁移到什么项目 + 实现需要哪些组件**。

## 风格速查

| style_tag | 特征 | 适用场景 | 实现要点 |
|---|---|---|---|
| 极简(minimalist) | 大留白、克制配色、强排版 | 学术主页、作品集 | 栅格 + 字体层次 |
| 科技感(tech) | 深色、霓虹强调色、网格/光效 | 产品落地页、答辩 | 深色主题 + 渐变 + 微动效 |
| 玻璃拟态(glassmorphism) | 半透明模糊、层叠 | 仪表盘、卡片 | backdrop-blur + 边框高光 |
| 卡片式(card) | 模块化卡片、清晰分区 | 管理系统、内容站 | 卡片组件 + 阴影层次 |
| 大屏可视化(data-screen) | 深色、高信息密度、实时图表 | 数据中台、监控大屏 | ECharts/D3 + 16:9 栅格 |
| 农业智慧化(agri-tech) | 绿色系、自然质感、数据+地图 | 智慧农业项目 | 绿色调色板 + 地图组件 |
| 医疗科技(medical) | 蓝白、干净、信任感 | 医疗平台 | 蓝色系 + 高可读性 |
| 移动端(mobile) | 拇指可达、底部导航 | App 演示 | 移动栅格 + 手势 |

## 设计 token 化
每个项目沉淀一套 tokens(色/字/间距/圆角)，由 a07 跨材料统一(链 Style Dictionary/Design Tokens)。

## 视觉 SSOT 锚点
[design_tokens.template.json](design_tokens.template.json) — DTCG(W3C)格式视觉单一事实源种子模板(color brand/semantic、typography 复合类型、4/8pt dimension、radius/shadow，含 `{color.brand.primary}` 别名示例)。由 a05(light-frontend-design) + extract-design-system 维护;论文图(db07)/PPT(db06)/前端(db05)/海报从同一份取值。真实项目副本落 db09 项目目录。

模板与 canonical 索引见 [design_cards.md](design_cards.md)（0 张实体卡，避免重复 `project_type`）。

## 采集→核验→入库管线（照此复现可扩库，与 db01/db06/db07 同口径）
1. **采集**：从上述数据来源记风格的版式逻辑/色板/token，**不存图片本身、不抄受版权素材**（CONVENTIONS §5）。
2. **核验（铁律）**：代表实现链接 `curl` 取 HTTP 状态留痕；色值/token 以官方设计系统文档或自家已 selftest 资产为准，不凭记忆填；抽查 ≥20% 新卡来源可访问且卡内数据与来源一致（记录落 `_verification_log/`）。
3. **入库**：按 `design_card` schema 填卡，YAML 值含英文冒号须紧跟非空格或加引号（PyYAML 陷阱）；新卡文件放本目录，在「真实资源文件」节加链接。
4. **校验**：`PYTHONUTF8=1 python .github/scripts/check_databases.py` 全绿（按 SCHEMA 强校验 `resources_real.md` 与 `*_cards.md` 必填字段）。
5. **落日期**：每张卡/每个卡文件标 `核验日期 YYYY-MM-DD`，供 [check_freshness.py](../../.github/scripts/check_freshness.py) 月度统计（warn-only，不阻断 CI；每月跑一次取超期清单复查）。

## 真实资源文件
- [resources_real.md](resources_real.md) — 真实可用前端资源清单（shadcn/ui、Tailwind、ECharts、Awwwards、Mobbin 等）+ 科研场景 design_card。Part1 许可列为**薄缓存快照、非认证事实**,附 npm 薄缓存映射表供 style_signal.py 实时核;agri-tech 卡带 domain_scope。
- [design_system_cards.md](design_system_cards.md) — 官方设计系统与科研项目落地模式（Carbon、Fluent、Polaris、Atlassian、Primer、USWDS、GOV.UK、Material Design 等 8 卡，站点 HTTP 200 核验）。
- [style_genre_cards.md](style_genre_cards.md) — 风格谱系卡（玻璃拟态、新拟物、编辑器极简 Linear/Vercel、杂志编辑 4 卡，来源 HTTP 200 核验 2026-06-12）。
- [scripts/style_signal.py](scripts/style_signal.py) — 工具 license/版本实时核(npm registry)+ 链接存活探测,冲突信在线、无网降级 stale、定价层标待核查。自检 `python scripts/style_signal.py --selftest`。
