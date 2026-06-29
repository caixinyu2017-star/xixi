# Brief → 官方设计系统映射表

研究/核实日期 2026-06-06。**一个项目只用一套设计系统**（混用会产生 token 冲突、双倍 bundle、视觉漂移）。
下面每个包名都已 `curl https://registry.npmjs.org/<pkg>` 实测 HTTP 200 并取到 latest 版本号。

> **职责边界（canonical）**：本文件是**方法论**——给 brief 信号→怎么选哪套设计系统、装哪个包。具体的**风格实例卡**（玻璃拟态/新拟物/编辑器极简/杂志编辑/官方设计系统落地模式/科研场景版式…）是 db05 的职责，真相源在 `databases/db05-frontend-styles/`（`style_genre_cards.md` 按视觉风格、`design_system_cards.md` 按官方系统、`resources_real.md` 按科研场景）。选型看本表，找可套用的风格卡去 db05；两边不重复彼此内容。

## 决策表

| brief 信号 | 选哪套 | 理由 | install（pin 到实测版本） |
|---|---|---|---|
| 企业内网 / Office 风 / Windows 生态 / Teams 类 | **Fluent UI v9** | 微软官方，深 Office 视觉，主题 token 体系成熟 | `npm i @fluentui/react-components@9.74.1` |
| 数据密集后台 / 监控 / IBM 风 / 工业 SaaS | **Carbon** | IBM 设计语言，强表格/数据网格，可访问性扎实 | `npm i @carbon/react@1.109.0` |
| 电商 / 商家后台 / Shopify 生态 | **Polaris** | Shopify 官方，电商语义组件（Card/ResourceList）齐全 | `npm i @shopify/polaris@13.9.5` |
| 项目管理 / 协作工具 / Jira-Confluence 风 | **Atlaskit** | Atlassian 官方，分包按需装 | `npm i @atlaskit/primitives@latest @atlaskit/button@latest` |
| 开发者工具 / 代码平台 / GitHub 风 | **Primer** | GitHub 官方，深色友好，开发者审美 | `npm i @primer/react@38.27.0` |
| 英国政府 / 公共服务 / 极致可访问性合规 | **govuk-frontend** | GOV.UK，WCAG/渐进增强标杆，非 React（Nunjucks+原生 JS） | `npm i govuk-frontend@6.2.0` |
| 美国联邦政府 / 公共部门 / Section 508 | **USWDS** | 美国政府标准，508 合规，框架无关 | `npm i @uswds/uswds@3.13.0` |
| 需要无样式可完全定制的底座 / 自建设计系统 | **Radix Primitives** | 只给行为+可访问性，样式全自定义，配 Tailwind | `npm i @radix-ui/react-dialog@latest`（按需逐组件装） |

## 选择决策树（逐条判定，命中即停）

1. 强合规公共部门？ 英国→govuk-frontend；美国→USWDS。
2. 绑定某商业生态？ Office/Teams→Fluent；Shopify→Polaris；Atlassian→Atlaskit；GitHub/devtool→Primer。
3. 数据密集型企业后台、要现成数据表格？ → Carbon。
4. 要自己掌控全部视觉、只借无障碍行为？ → Radix Primitives + Tailwind（这是 shadcn/ui 的底座）。
5. 都不命中（品牌定制落地页/展示页）？ → 不装组件库，用 Tailwind v4 + 自有 token + 本技能 assets/ 的 GSAP/Motion 骨架。

## 硬约束

- 一仓一套：选定后在 `package.json` 只保留这一套 UI 库；新增组件先看库内有没有，没有再自建，不要再引第二套。
- 版本固定：上表写死了实测 latest 版本；用 `npm i pkg@x.y.z` 而非 `^`/`~`，避免无意升级破坏 token。
- Radix 是底座不是成品：装 `@radix-ui/react-*` 是按组件逐个装（dialog/dropdown-menu/tooltip…），样式自己写。
- govuk-frontend / USWDS 非 React 组件库：它们是 CSS + 原生 JS 模块（USWDS 框架无关，govuk 用 Nunjucks 模板）；在 React 项目里用要包一层或只取其 CSS/设计 token。

## 核实证据（npm registry，2026-06-06）

```
200  @fluentui/react-components   9.74.1
200  @carbon/react                1.109.0
200  @shopify/polaris             13.9.5
200  @atlaskit/primitives         (exists)
200  @atlaskit/button             (exists)
200  @primer/react                38.27.0
200  govuk-frontend               6.2.0
200  @uswds/uswds                 3.13.0
200  @radix-ui/react-dialog       (exists)
```
