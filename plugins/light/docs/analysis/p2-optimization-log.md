# P2 优化台账（批量/排序工作流 + 接真实检索后端）

> 起始 2026-06-13 ｜ 范围（已拍板）：**批量排序 + 接检索后端**。
> idea-critique 批量排序口径（已拍板）：**逐卡完整严审 + 汇总排序**（保留每卡八维严审，只加批量汇总+Weighted 排序+top-k 输出层，不做"预筛省算力"）。
> 硬纪律：能补脚本就补、补不动降措辞；改脚本前读真实文件、改后跑 selftest（离线过）+ 四 CI；接外部后端必须有离线降级（沿用 P0 闭环）；提交只署用户本人、中文 commit；不编造（DOAJ 查不到标 unavailable）。

---

## P2 落点（总览第四节 + 详档可优化点）

| 项 | 技能 | 内容 |
|---|---|---|
| **批量排序** | idea-critique | 摄入 idea_candidates 多卡，逐卡八维严审 → 汇总按 Weighted 排序 → 输出 top-k 放行 + 余下附判决理由 |
| **批量排序** | venue-matching | 转投顺序做成可执行字典序 fallback 规则（方向匹配↓→接收信号↓→周期↑→APC↑） |
| **接检索后端** | venue-matching | 接 DOAJ 收录核查（白名单正面信号，免 key REST），离线降级 |
| **接检索后端** | figure-planning | 规划卡可喂执行层（结构化 spec 输出，对接 m11 出图/MCP） |

---

## 执行进度（⬜待办 / 🔧进行中 / ✅完成）

### 批量排序
- ✅ Q1 idea-critique — score_aggregate.py 加 rank_batch()(逐卡 decide+档位/Weighted 降序+top-k，gate 不放宽，确定性排序)；selftest 加 [I]/[I'] 批量用例；SKILL 加"批量评审排序"节(强调逐卡完整严审非预筛省算力)
- ✅ Q2 venue-matching — SKILL 加"转投顺序：可执行排序规则"节(字典序：方向匹配↓→录用信号↓→周期↑→APC↑，预警直接剔除；按拒稿原因调权)，从原则变可落地 fallback 链

### 接检索后端
- ✅ Q3 venue-matching — venue_signal.py 加 doaj_by_issn()(直查 doaj.org 免 key，三态 in_doaj True/False/None，seal 标记，查询失败标 unavailable 绝不当未收录)，assemble 加 whitelist 块(DOAJ + OpenAlex is_in_doaj 交叉)；selftest 加 DOAJ 命中+失败降级用例；SKILL 脚本输出说明加 DOAJ 白名单行
- ✅ Q4 figure-planning — 新增 validate_plan_card.py：校验 target_journal/column 命中 figure_export JOURNAL_SPECS(动态读单一真相源杜绝漂移)、figure_id 唯一且 F#/T# 格式、custom 带 width、source_card 必填；登记 WHATS_INCLUDED(scripts 51→52)；SKILL 加"交 m11 前契约校验"节；selftest 7 用例全过

### 收尾
- ✅ 四 CI 全绿（52 脚本/52 登记/52 selftest）+ 改动/新增脚本 selftest 离线过
- ✅ WHATS_INCLUDED 同步（validate_plan_card 登记，scripts 51→52）
- ✅ 记忆更新

---

## 本轮 P2 结论
**批量排序**：idea-critique 加 rank_batch()(逐卡完整严审+档位/Weighted 降序+top-k，gate 不放宽)；venue-matching 转投顺序做成可执行字典序 fallback。
**接检索后端**：venue-matching 接 DOAJ 官方库(免 key 三态，查询失败标 unavailable 绝不当未收录)；figure-planning validate_plan_card 把规划卡与 m11 figure_export 契约对齐(动态读 JOURNAL_SPECS)，打回前移。
**诚实底线**：DOAJ 查不到标 unavailable；validate 只校验可机检契约；批量排序不因 top-k 放宽 gate。
**未做(如实标)**：figure-planning 其余可优化点(display item 预算/table_plan_card 变体/examples 实卡)属体验增强；PPTEval/OpenNovelty pipeline 等工程化借鉴未做。
