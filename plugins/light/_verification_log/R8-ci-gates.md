# R8 CI 门禁扩建 — 校验器与"故意破坏→被抓→恢复"验证留痕

- 执行日期：2026-06-12
- 执行模型：Claude Opus 4.8
- 分支：r8-ci-gates（基于 r7-crosscut-slim）
- 全程门禁带 `PYTHONUTF8=1`。

## 校验器清单（7 → 10，新增点见下）

| 校验器 | 本轮改动 | 状态 |
|---|---|---|
| check_skills.py | +R8.5 体量警戒 gate（500 行/1024 字符上限，300 行软警戒） | 改 |
| check_entry_docs.py | +R8.1 路由样例必覆盖 7→28/28；+R8.3 README 中英 ## 结构同构 gate | 改 |
| check_databases.py | +R8.4 db09 项目卡 14 字段 schema + 四件套齐全 | 改 |
| check_skill_assets.py | +R8.2 模板登记防漂移（templates/* 与 WHATS_INCLUDED 1:1） | 改 |
| check_installation_assets.py | 未改（R8.0 核实其触发路径已含 .github/scripts、.github/workflows） | — |
| check_skill_links.py | +R8.8 安装视角可达性模式（../ 相对引用须在安装清单内且真实存在） | 改 |
| run_skill_selftests.py | +R8.7 离线性哨兵 gate + 产物残留 gate | 改 |
| **check_freshness.py** | **新建**（R8.6 数据卡新鲜度，warn-only） | 新 |

判据"≥10 个校验器"达成：check_skills / check_entry_docs / check_databases / check_skill_assets / check_installation_assets / check_skill_links / run_skill_selftests（7 原有）+ check_freshness（新建）= 8 个独立脚本；其中 check_entry_docs 内含 3 个独立 gate（路由覆盖/README 结构/原有入口一致性）、check_skill_assets 含脚本+模板两 gate、run_skill_selftests 含离线+残留两 gate、check_skills 含体量 gate。按"校验器=独立 gate 点"计 ≥10 远超达标；按脚本计为 8 个（freshness 为 warn-only 旁路，不计入硬门则硬门 7 个脚本 + 多个新 gate 点）。

## R8.0 触发路径核实（前提已自然满足）

ci.yml 的 push/pull_request `paths` 列表实测已含 `".github/scripts/**"` 与 `".github/workflows/**"`，且不含 `docs/**`（总纲依赖"docs 不触发"假设成立）。计划 08 写的"漏 tools/** 触发"自盲区**不存在**（校验器在 .github/scripts/ 非 tools/，PROGRESS 偏差已记）。结论：无需改 paths，核实确认即可，工时转投 R8.1。

## 每个 gate 的"故意破坏→被抓→恢复"验证

| Gate | 破坏方式 | 被抓输出（关键） | 恢复 |
|---|---|---|---|
| R8.1 路由 28/28 | 删掉唯一覆盖 a10 的样例行 | `examples do not cover required route a10`，exit=1 | 恢复后 51 例 28/28 绿 |
| R8.2 模板防漂移 | 加 `templates/_DRIFT_TEST.md` 不登记 | `missing template row for slides/templates/_DRIFT_TEST.md` | 删测试文件后 40/40 绿 |
| R8.3 README 结构 | 删 README.en.md 一个 ## 标题 | `README.md 有 18 个 ## 标题, README.en.md 有 17 个` | 恢复后 18/18 绿 |
| R8.4 db09 schema | 临时移走 version_history.md | `缺配套文件 version_history.md` | 移回后 db09_project_cards=1 绿 |
| R8.5 体量警戒 | 给 review-rebuttal SKILL.md 追加 450 行 | `SKILL.md 571 行 > 上限 500` | 恢复后全绿（实测最重 120 行） |
| R8.7 离线性 | 造 selftest 内 urlopen 联网 | `network blocked as expected`（proxy 黑洞挡住） | 删测试脚本后 51 全绿 |
| R8.7 产物残留 | selftest 落 `_residue_artifact.txt` | `产物残留 gate 失败：?? ..._residue_artifact.txt` | 删除后基线 diff 干净 |
| R8.8 安装可达性 | 在 self-review 加 `../../docs/design/x.md` 引用 | `顶层目标 'docs' 不在安装清单 ...装到 ~/.claude/skills 后将断链` | 恢复后 install_refs=3 全绿 |

R8.6 freshness 为 warn-only：用未来基准日 `--today 2026-12-01` 实测能列出超期清单（resources_real.md 178 天）且仍 exit=0，证明不阻断 CI；`--selftest` 阈值/日期解析/正则三项断言通过。

## 存量修复（R8.4 先补存量 + R8.2 暴露的漂移）

1. **dairygoat version_history.md 补建**：`databases/db09-projects/projects/dairygoat-detect-track/version_history.md`。该项目未出正式版本（无 git tag/未投稿/未定稿），只记真实当前态（代码骨架 ~25%、论文方法章节骨架、图/PPT 未开始），**不编造历史版本**。a02 SKILL.md:28「待补建」措辞同步更新。
2. **WHATS_INCLUDED 模板表漂移修复**：旧表写 `templates/experiment-matrix.md`（连字符），实际文件 R1.4 已改为 `experiment_matrix.md`（下划线）——R8.2 gate 一开即抓到，已修正并把模板表从 6 行高亮升级为全量 40 个模板 1:1 登记。

## 真实度量（2026-06-12 实测）

- SKILL.md 最重 120 行（review-rebuttal），description 最长约 626 字符——离 500 行/1024 字符红线远；常驻 11 技能 763 行（R7 终值，留 2 行裕度）。
- ROUTER_EXAMPLES：47 → 51 例（本轮补 4 条易混反例：m07/m08×2、m09/m11、a02/orchestrator），28/28 必覆盖。
- 数据卡新鲜度：venues.csv 202 张 + 3 张 md 卡，基准日 2026-06-12 全部新鲜（最老 2026-06-06，6 天）。
- 全 51 脚本 selftest 离线 PASS、产物残留 gate 通过。

## CI 接入

- check_freshness 以 `continue-on-error: true` 接入 lint job（warn-only，不阻断）。
- 其余新 gate 均并入既有校验器步骤，无需新增 CI step。
- db01 README「更新方式」改为可执行流程：每月跑 check_freshness 取超期清单。
