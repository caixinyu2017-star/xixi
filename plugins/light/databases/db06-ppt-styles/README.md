# db06 — PPT 设计风格库

搜集热门精美 PPT 风格与版式，训练 m16(PPT 制作) 的排版与审美。学版式逻辑与视觉层次，**最终原创化**。

## 这个库是什么(诚实卖点)

**不是**"15 条实测资源 + 星标/许可认证库",而是**版式/叙事方法卡精养 + 资源指针实时核**两层:

- **方法论层(本地精养,护城河)**:16 张 slide_card(resources_real 6 场景卡 + slide_pattern_cards 10 页型卡)的 theme_style/page_type/layout_structure/visual_hierarchy/chart_style 等版式叙事方法(一页一观点/action-title/data-ink/分步揭示/控时公式),跨学科成立、几乎不过时,是 m16 的真正消费对象。调色板/字体取色锚定 `light-slides/assets/themes.py`(已 selftest 的设计常量)。
- **薄缓存层(资源事实实时核)**:resources_real.md 资源表的 GitHub 星标/许可/链接 HTTP 状态是会变的事实——**快照值非长期有效**,开源仓由 [scripts/resource_signal.py](scripts/resource_signal.py) 实时查 GitHub/PyPI API、冲突信在线、无网回退快照标 stale;许可为合规红线以官方 LICENSE 为准。
- 偏科极少:绝大多数版式卡学科无关;README 风格速查里的农业/医学是学科色板偏好,非卡的偏科标。

## slide_card schema
`scenario, theme_style, page_type, layout_structure, color_palette, font_pairing, visual_hierarchy, chart_style, icon_style, transition_style, speaker_notes_style, reuse_template_notes`

## 数据来源
Canva、PowerPoint 模板、Slidesgo、Beautiful.ai、Gamma、Pitch、SlideModel、Envato Elements、Behance/Dribbble Presentation、Pinterest PPT boards、国内优秀答辩/竞赛 PPT、学校优秀毕业答辩 PPT。

## ⚠ 合规
商用模板不直接复制；学版式、配色、结构、视觉层次，最终重绘原创(CONVENTIONS §5)。

## 页面类型库
封面 / 目录 / 过渡 / 背景 / 内容 / 图表 / 流程 / 时间线 / 对比 / 团队 / 结论 / 致谢 / QA。

## 风格速查

| theme_style | 配色 | 适用场景 |
|---|---|---|
| 学术风 | 白底 + 单一主色 + 深灰字 | 答辩、组会、学术报告 |
| 科技风(深色) | 深底 + 霓虹强调 + 光效 | 路演、产品发布、AI 主题 |
| 浅色高级风 | 米白/浅灰 + 莫兰迪色 | 商务汇报、结题 |
| 极简风 | 大留白 + 一两个强调色 | 内容聚焦、演讲 |
| 数据分析风 | 中性底 + 图表主导 | 数据汇报、竞赛 |
| 农业主题 | 绿色系 + 自然质感 | 智慧农业项目 |
| 医学主题 | 蓝白 + 干净专业 | 医学研究 |
| 竞赛路演风 | 强对比 + 大字 + 视觉冲击 | 互联网+/挑战杯路演 |

## 排版原则（贯穿）
一页一观点、对齐、留白、视觉层次(标题>要点>细节)、图大字少、统一图标线型、克制转场。答辩 8–12 min ≈ 10–15 页。

模板与 canonical 索引见 [slide_cards.md](slide_cards.md)（0 张实体卡，避免重复 `scenario`）。

## 采集→核验→入库管线（照此复现可扩库，与 db01/db05/db07 同口径）
1. **采集**：从上述数据来源记版式逻辑/调色板/字体配对/视觉层次，**学结构不复制商用模板素材**（CONVENTIONS §5）；增量来源是每做一套真实 deck 沉一张风格卡，调色板/字体取自 `light-slides/assets/themes.py` 十主题。
2. **核验（铁律）**：资源链接 `curl`/GitHub-PyPI API 取 HTTP 状态与许可留痕；调色板/字体取自 db06 自家已 selftest 的 `light-slides/assets/themes.py` 或公开来源，不凭记忆填；抽查 ≥20% 新卡（记录落 `_verification_log/`）。
3. **入库**：按 `slide_card` schema 填卡，YAML 值含英文冒号须紧跟非空格或加引号；新卡文件放本目录，在「真实资源文件」节加链接。
4. **校验**：`PYTHONUTF8=1 python .github/scripts/check_databases.py` 全绿（按 SCHEMA 强校验 `resources_real.md` 与 `*_cards.md`）。
5. **落日期**：每张卡/每个卡文件标 `核验日期 YYYY-MM-DD`，供 [check_freshness.py](../../.github/scripts/check_freshness.py) 月度统计（warn-only，不阻断 CI）。

## 真实资源文件
- [resources_real.md](resources_real.md) — 真实 PPT 资源清单（Marp/reveal.js/python-pptx 等）+ 答辩/路演/汇报场景 slide_card。星标/许可/HTTP 状态为薄缓存快照(last_checked=2026-06-06),以 resource_signal.py 实时核为准。
- [slide_pattern_cards.md](slide_pattern_cards.md) — 高级 PPT 页型与叙事模式（action-title 结果页、方法 pipeline、文献矩阵、dashboard、路演钩子、商业模式、A0 海报、rebuttal 汇报 + 开题报告答辩、课程教学共 10 卡）。
- [scripts/resource_signal.py](scripts/resource_signal.py) — 资源星标/许可/存活实时核(GitHub stars+spdx / PyPI license / URL 状态,403 反爬标注),冲突信在线、无网降级 stale。自检 `python scripts/resource_signal.py --selftest`。
