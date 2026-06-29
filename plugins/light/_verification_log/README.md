# 核实日志 (_verification_log)

Phase 3 用 curl 直读 GitHub raw / PyPI / 官方 API，对 Phase 1 因 WebFetch 被拦而标"未能核实"的项做二次核实的记录。结论可回查、带真实 HTTP 码与来源。

## 文件
- [skill_sources.md](skill_sources.md) — 第三方 skill 内部实现重核（直读 SKILL.md 源码）。**重要更正**：`K-Dense-AI/claude-scientific-skills` 已改名 `scientific-agent-skills`（旧链接 301 重定向，已实测，相关技能 references.md 已批量更新）。含 obra/superpowers 的 verification-before-completion、requesting-code-review 等真实步骤。回填 light-self-review / light-idea-critique / light-literature-search 等。
- [api_fields.md](api_fields.md) — API 端点活性实测（HTTP 码确凿）：Zotero 公共库匿名 200；Mendeley/Scopus/Lens 端点存活但需 token(401)；PatentsView 旧 API 已迁移(301→USPTO)；LanguageTool /v2/check 匿名 200(限流 20 req/IP/min)；DeepL 需 key(403)。回填 light-citation / light-ip-application / light-paper-polishing 等。
- [lib_specifics.md](lib_specifics.md) — 开源库真实 license/版本(PyPI+GitHub API)：Deepchecks=AGPL-3.0、Evidently=Apache-2.0(0.6+ 新导入路径 `from evidently import Report`)、python-pptx/Marp/reveal.js=MIT、BioRender 免费版不可用于论文投稿。回填对应技能。
- [R8-ci-gates.md](R8-ci-gates.md) — R8 CI 门禁扩建：校验器 7→8 脚本(新建 check_freshness)+多个新 gate 点，每个 gate 的"故意破坏→被抓→恢复"留痕，R8.0 触发路径核实，dairygoat version_history 补建与模板表漂移修复。

## 仍无公开免费源（如实标注，非遗漏）
EndNote 无公开 REST API；Clarivate JCR 精确影响因子、Scimago SJR 为付费墙；WIPO PATENTSCOPE 为 JSF 应用非 REST。这些用 OpenAlex 2yr 均被引 / h-index 作可核查替代指标。
