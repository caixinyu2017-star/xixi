# 字体池 + 禁用字体 + 禁用色族

具名、可直接落地的取用池。配字遵循「展示字（display）+ 正文字（body）」配对原则。

## Sans display 默认池（展示/标题用，有个性、非系统字）

- **Geist** — Vercel 出品，几何中性偏现代，开发者审美。
- **General Sans**（Indian Type Foundry）— 几何人文混合，标题很挺。
- **Satoshi** — 圆润几何，亲和但不软。
- **Clash Display** — 高对比粗壮，冲击力强的 hero 大字。
- **Cabinet Grotesk** — 当代 grotesk，编辑感。
- **Space Grotesk** — 可用，但**已被过度使用**，作为 AI 默认收敛点，非必要不选（见 frontend-design anti-pattern）。

## 配对池（display ↔ body 推荐组合）

| display | body | 适合基调 |
|---|---|---|
| Clash Display | Geist / Geist Sans | 科技、产品落地页 |
| General Sans | Supreme / Switzer | 现代 SaaS、editorial |
| Cabinet Grotesk | Satoshi | 高级消费品、品牌站 |
| Geist | Geist Mono（代码/数据） | 开发者工具、dashboard |
| Newsreader（serif 正文，允许） | General Sans（标题） | 长文/学术/editorial 反向配 |

正文字优先：Switzer / Supreme / Satoshi / Geist Sans，行高 1.5-1.7，正文 ≥16px。

## Named banned serif（禁用，已成 AI-tell）

- **Fraunces** — 被 AI 生成站点滥用到失去个性。
- **Instrument Serif** — 同上，default landing-page serif 收敛点。

> 需要 serif 时改用 Newsreader / Spectral / GT Sectra 类，并确认与品牌真实匹配，而非默认套用。

## 禁用色族（premium-consumer 套路色，连 hex 一并禁）

这一族「米色 + 黄铜 + 酱黑」被高端消费/AI 模板反复套用，已成视觉俗套，默认禁用：

| 类别 | 禁用 hex（含邻近值） |
|---|---|
| premium 米色/奶油底 | `#F5F0E8` `#EFE9DD` `#E8E0D0` `#F3EDE3` `#FAF6EF` |
| 黄铜/古铜强调 | `#B08D57` `#C9A227` `#A67C00` `#9C7A3C` `#BfA76F` |
| 酱黑/暖黑文字 | `#1A1714` `#211C17` `#2B2620` `#23201B` |

也一并禁掉老 anti-slop：紫/粉渐变配白底（`#A855F7→#EC4899` on `#FFF` 类）、gradient-orb 代表 AI。

## 怎么用

- display+body 各从池里选一支，押注到底，全站统一（登记 design tokens）。
- 禁用清单是**机械可查**的：把字体名与 hex 丢进 grep / 本技能 linter 即可判定。
- 字体托管：Next 用 `next/font`（防 layout shift）；纯 HTML 用 Fontshare/自托管，避免 FOUT。
