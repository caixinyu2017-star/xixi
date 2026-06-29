# 前端设计生态 2026

> **时间锚与口径**：本文件是热门技能雷达 + 前端栈版本快照，研究日期 2026-06-10。**逐工具的真实端点/命令/参数/坑以同技能 `references.md` 为单一真相源**；本文件与 `references.md` 重叠处（栈版本、外部技能信号）以**本文件的时间快照**为准、`references.md` 不复写版本号，二者按"本文件管时效快照、references.md 管工具硬信息"分工。安装量/版本号随时间变，引用前按文末命令复检。

升级技能、选前端设计 workflow、或判断哪些外部技能值得吸收时读本文件。

## 外部技能生态信号

`npx skills find` 检索（2026-06-10）：

| 查询 | 技能 | 安装量 | 信号 |
|---|---:|---:|---|
| `frontend design` | `smithery.ai@frontend-design` | 4.5K | 安装量高，但 2026-06-10 `npx skills use` 克隆失败；依赖前先复验。 |
| `ui ux design` | `nexu-io/open-design@ui-ux-pro-max` | 1.9K | 有发现价值；当前 Open Design 仅目录条目、指向上游。 |
| `frontend design` | `ulpi-io/skills@frontend-design-ui-ux` | 399 | 二级社区信号。 |
| `frontend design` | `rand/cc-polymath@discover-frontend` | 111 | 中低信号；用前先查。 |

本技能已吸收的高价值模式：

- Anthropic `frontend-design`：明确创意方向（目的/调性/约束/差异化），避免泛化 AI 审美。
- Vercel 式 web 设计规则：可访问性、性能、UX 状态、响应式、hover/focus/reduced-motion。
- UI/UX Pro Max 思路：把 brief 映射到行业/风格/token/组件/清单；除非其 assets/scripts 已安装，否则不声称上游库检索在运行。
- Taste/anti-slop 技能：variance/motion/density 旋钮、重设计审计、图转码 workflow、机械化痕迹识别。
- shadcn/Tailwind/Next 最佳实践：源码自持组件、CSS 变量、Server Components、路由/数据/安全边界。

## 设计 token 工程化（衔接 db05 视觉 SSOT）

视觉 token 从单一源生成多端，避免各端各写：

- **Style Dictionary (v4)**：单一 token 源经 `transformGroup`/`transforms` 输出到 `css/variables`、`scss/variables`、`javascript/es6` 等多平台，"一处定义、多端一致"。v4 为 ESM + 异步。
- **Terrazzo**（原 Cobalt）：读 W3C DTCG 格式 token（`tokens.json`）经插件链编译到 CSS/JS/Tailwind/原生平台；适合以 DTCG 为权威源、需要现代插件化构建管线的项目。
- **衔接 db05**：两者的 token 权威源都对齐 db05 的 `design_tokens.template.json`（DTCG 视觉 SSOT，由 a07 consistency 维护）——论文图(db07)/PPT(db06)/前端(db05) 同取一份值，前端构建只是把这份值编译到运行时，不另立一套色板/字阶。

## 当前版本快照

npm 检查（2026-06-10）：

| 包 | 版本 |
|---|---:|
| `next` | 16.2.9 |
| `react` | 19.2.7 |
| `tailwindcss` | 4.3.0 |
| `shadcn` | 4.11.0 |
| `motion` | 12.40.0 |
| `gsap` | 3.15.0 |
| `lucide-react` | 1.17.0 |
| `@radix-ui/react-slot` | 1.2.5 |
| `vite` | 8.0.16 |
| `@vitejs/plugin-react` | 6.0.2 |

安装前复检：

```powershell
npm view next version
npm view react version
npm view tailwindcss version
npm view shadcn version
npm view motion version
npm view gsap version
npm view lucide-react version
npm view @radix-ui/react-slot version
npm view vite version
npm view @vitejs/plugin-react version
```

## 现代栈取向

产品级 web 应用：

1. **Next.js App Router**——需要路由、服务端数据、SEO、auth、表单、部署规范时。
2. **Vite + React**——独立工具、dashboard、游戏、原型或静态产物时。
3. **Tailwind v4** 配 CSS 变量/token——要快速定制样式时。
4. **shadcn/ui**——要项目自持的、基于 Radix 的可访问组件源码时。
5. **Motion 或 GSAP**——仅当动效传达层级或交互时用；尊重 `prefers-reduced-motion`。

小程序 UI：

1. 本 Light 科研技能包**不含独立 `light-miniprogram` 技能**，小程序工作在此只作 UI/视觉指导。
2. 涉及非 UI 决策前，先向用户或项目文档确认 runtime、平台、AppID、发布与 API 约束。
3. 本技能用于 token、信息层级、空/加载/错误态、移动端人因、视觉打磨。
4. 选一套小程序组件体系：原生/WeUI、TDesign、Vant、Ant Design Mini、NutUI Taro 或自建。
