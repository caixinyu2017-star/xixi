# 工程化升级台账（借鉴 GitHub 同类亮点：软约束→可量化可复现）

> 起始 2026-06-13 ｜ 范围（已拍板）：先做 3 个高价值工程化升级，再逐技能看 MCP 利用。
> 来源：总览第四节 P2 末"借鉴同类工程化亮点" + 各详档 improvement_ideas，均为任务2 实测到的真实 GitHub 项目。
> 方向：和 P1 结构化多样性、P2 契约校验同脉——把"靠模型自觉/人工判断"的环节升级成**可量化、可复现、可机检**的机制。
> 诚实底线：新脚本都给 selftest（离线过）；推荐/打分是**启发式规则不是真值**，输出标"启发式、需人工复核"；不虚构权威依据；规则有依据的引文献（Cleveland-McGill/Mackinlay 等），无依据的标经验值。

---

## 三个工程化升级

| 编号 | 借鉴源（实测 star） | 落到哪个技能 | 做什么 |
|---|---|---|---|
| **E1** | cmudig/draco2(112★)、vega/voyager(1491★) | figure-planning | 图型推荐：数据字段+分析任务→候选图型→按任务排序，可解释可复现；接在 validate_plan_card 上游，串"推荐→规划卡→契约校验"链 |
| **E2** | icip-cas/PPTAgent 的 PPTEval(4640★) | slides | 量化 QA：把"幽灵测试"(人工查重叠/溢出)升级为可打分维度(内容/设计/连贯性)，可回归 |
| **E3** | january-blue/OpenNovelty(134★) | idea-critique | 检索证否 pipeline：把"至少两库交叉"的口头约束工程化为固定四阶段(抽论断→检索相关工作→深度对比→novelty 报告)，可复现 |

---

## 执行进度（⬜待办 / 🔧进行中 / ✅完成）

### E1 figure-planning 图型推荐（Draco 思路）
- ✅ E1a 新建 scripts/recommend_chart.py：数据字段类型+任务→候选图型排序+理由（Cleveland-McGill 感知精度+任务族经验先验，系列数拥挤惩罚，11 图型知识库带 db07 铁律引用），selftest 8 用例全过；诚实标"启发式非真值、人工定夺、不 AI 生图"
- ✅ E1b 登记 WHATS_INCLUDED(scripts→53)；SKILL 规划流程步2 加 recommend_chart 调用，串"推荐→填规划卡→validate_plan_card 校验→m11 出图"链

### E2 slides 量化 QA（PPTEval 思路）
- ✅ E2a 新建 scripts/pptx_eval.py：内容密度/设计一致/连贯性三维扣分制(对照 SKILL 硬尺度：≤7要点/字号区间/配色数/禁纯文字页/禁同版式)，纯 python 读 pptx 几何+run字号+填充色，selftest 造 good/bad/empty 三 deck 验证(good 10.0 vs bad 4.7)；诚实标"只算结构指标，美感/叙事/真数据须人工+thumbnail 复核"
- ✅ E2b 登记 WHATS_INCLUDED(scripts→54)；SKILL 脚本节加 pptx_eval(与 thumbnail 互补：给人看 vs 给分)

### E3 idea-critique 检索证否 pipeline（OpenNovelty 思路）
- ✅ E3a 新建 scripts/novelty_audit.py：四阶段结构化留痕(抽论断→检索证据→撞车对比→判定)+一致性勾稽(抓 NOVELTY-OVERCLAIM/COLLISION-SAME-BLOCK/EVIDENCE-MISSING/SINGLE-SOURCE/DELTA-MISSING 5 类矛盾)，输出 verdict hooks 喂 Step6 否决项；不做检索本身只保证结论与证据自洽，selftest 含矛盾检测全过
- ✅ E3b 登记 WHATS_INCLUDED(scripts→55)；SKILL Step2 加四阶段结构化+novelty_audit 调用，资产地图同步

### 收尾
- ✅ 四 CI 全绿（assets/links/entry/databases，scripts 52→55）+ 三新脚本 selftest 离线过
- ✅ WHATS_INCLUDED 同步（recommend_chart/pptx_eval/novelty_audit 登记）
- ✅ 记忆更新

---

## 本轮工程化升级结论
三个借鉴 GitHub 同类亮点的升级，全部把"靠模型自觉/人工判断"的软环节升级为**可量化/可复现/可机检**的硬机制（与 P1 结构化多样性、P2 契约校验同脉）：
- **E1 recommend_chart.py**（figure-planning，借 Draco）：数据字段+任务→候选图型排序+理由（Cleveland-McGill 感知精度先验），串"推荐→规划卡→validate_plan_card 校验→m11 出图"链。
- **E2 pptx_eval.py**（slides，借 PPTEval）：内容/设计/连贯性三维扣分制，把视觉 QA 从肉眼查升级为可回归打分，与 thumbnail 互补（给人看 vs 给分）。
- **E3 novelty_audit.py**（idea-critique，借 OpenNovelty）：检索证否四阶段留痕+一致性勾稽，抓"声称新却证据打脸"等矛盾，喂回否决项。
**诚实底线贯穿**：三脚本都标"启发式/结构性指标非真值"、"美感/叙事/真假须人工"、"不做检索/不替判断"；不 AI 生图底线不受影响。借鉴源 star 均任务2 实测（Draco 112★/PPTAgent 4640★/OpenNovelty 134★）。

---

## 之后：逐技能 MCP 利用（待 3 升级后做）
做一张"技能×MCP 适配表"：该接的接、不该接的明说不接（不硬塞）。已知落点：figure-planning↔Draw.io/Blender、frontend-design↔Figma、slides↔Canva/Blender、tool-selection↔MATLAB/通用 MCP 发现。其余多数技能无自然 MCP 落点。

## 暂缓：memory-pm 分会话/上下文管理
用户判断"搞不好更垃圾"+ 项目记忆无该设计定稿 → **搁置**。跨会话状态依赖 harness 行为，技能层难做扎实，要做须先有清晰设计（状态存哪/恢复协议/可验证）再动。
