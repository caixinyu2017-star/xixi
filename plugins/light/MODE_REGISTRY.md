# Light 模式注册表（MODE_REGISTRY）

Light 绝大多数技能是"一个技能 = 一条固定流程"的流程型技能，**不需要也没有**模式切换。只有少数技能定义了可选的操作模式（mode）——选对档位能避免每次都走完整流程。这张表是这些 mode 的单一真相源；修改某技能的 mode 时，先更新这里。

> 说明：这张表故意只收录**真正存在显式 mode 机制**的技能。Light 共 28 个技能，但有显式 mode 的仅 3 个、合计 8 个 mode。其余技能走固定流程，不在此列——这是 Light 与"少技能多模式"型技能包（如 ARS）的结构差异，不是遗漏。

## m07 paper-drafting（5 种）

定义于 `skills/light-paper-drafting/references/operational_modes.md`。先选档位，别每次都走全流程。

| mode | 产出 | 触发场景 |
|------|------|----------|
| `full` | 完整初稿（分模块草稿 + 贡献清单 + GAP 台账 + 声明） | "写整篇 / 一篇完整草稿" |
| `outline-only` | 大纲 + 论证图（带每节 brief 与字数预算，不写正文） | "先给我个结构 / 提纲 / 论证骨架" |
| `abstract-only` | 一段 150–250 词摘要（可选双语） | "帮我写 / 改摘要" |
| `section-redraft` | 某一节的新稿 + 改动说明 | "把方法 / 实验 / 引言这节重写" |
| `self-review` | 逐维问题清单 + 命中失败模式 + 必改项 + 声明缺失项 | "草稿自检 / 挑毛病 / 失败模式检查" |

## m14 review-rebuttal（2 种）

定义于 `skills/light-review-rebuttal/SKILL.md` 的两个大节。

| mode | 产出 | 触发场景 |
|------|------|----------|
| 模式一 投稿前模拟审稿 | 3–4 位独立审稿人按目标 venue 标准出具的评审报告 | 投稿前预审、压力测试论文 |
| 模式二 真实意见返修 | 解析意见 → 定策略 → R→A→C response letter → 改论文 → 提交前自审 | 收到真实审稿意见后做返修 |

## m04 idea-critique（1 种可选子模式）

主流程是固定的 Step 0–7 严审管线；下面是可选附加模式。

| mode | 产出 | 触发场景 |
|------|------|----------|
| `calibration` | 喂一批已知结局的 idea 跑 `scripts/calibration.py`，算 FNR/FPR，据此调严格度 | 怀疑自己审得过严 / 过松时 |

## m16 light-slides

light-slides 已统一为 **python-pptx 程序化单一路线**（无显式 mode）：themes.py 主题色板 + patterns.md 版式 + build_deck.py 端到端，出可编辑 pptx。需要更强设计感时借 PptxGenJS/Marp/reveal.js/Beamer（见 SKILL.md「实现工具」），但不再有 mode 切换。

---

其余 Light 科研技能（m01–m03、m05、m06、m08–m13、m15、m16、m17、a01–a10 与 light-orchestrator）均无显式 mode，走各自固定流程。如需为某技能新增 mode，在该技能内定义后，把它登记到本表。
