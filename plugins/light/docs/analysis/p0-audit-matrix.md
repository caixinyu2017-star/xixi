# P0 全扫审计矩阵（28 技能 × 3 类诚实性问题）

> 起始 2026-06-13 ｜ 本轮范围：**全 28 技能扫一遍 P0**，承诺差距**能补脚本就补、补不动才降措辞**。
> 优先级依据：`docs/analysis/README.md` 第三节 8 条共性缺点中的 P0 三类，第四节 P0 批次。
> 执行口径（已与用户拍板）：
> - **邮箱**：环境变量（`OPENALEX_MAILTO`/`CROSSREF_MAILTO`）+ `--mailto`，不传则匿名查询（**不伪造**）。范式模板 = `light-venue-matching/scripts/venue_signal.py`。
> - **api-key**：联网脚本统一加 `--api-key` 参数 + 读环境变量（`OPENALEX_API_KEY`），传了带上；口径单一真相源仍指向 `light-literature-search` references「OpenAlex 接入真相源」节。
> - **离线降级**：联网闸门须有明确状态机（能否放行 / 要不要二次检索），不只是「标 unavailable」。
> - 硬纪律：不编造；改脚本前读真实文件、改后跑对应 CI + `--selftest`（须离线过）；提交只署用户本人、中文 commit。

---

## 三类 P0 问题定义

| 类 | 问题 | 判定标准 |
|---|---|---|
| **A 承诺>能力** | 文档宣称的源/功能在代码里不存在 | SKILL/README 宣称 vs scripts 实际覆盖 |
| **B api-key/mailto** | 伪造/私人邮箱硬编码；联网脚本无 key 透传 | grep 邮箱常量 + argparse 无 `--api-key` |
| **C 离线降级** | 联网闸门无离线状态机 | 网络失败时是否有 `[OFFLINE]` 回退 + 放行规则 |

---

## 客观落点（已 grep + Explore 核查确认）

### A 承诺>能力 —— 收敛到 3 个技能（Explore 实读 SKILL+scripts 确认）

| 技能 | 宣称 | 实际 | 处置 |
|---|---|---|---|
| **literature-search** | ~13 类源 / 7-8 API；L28「四源并查(OpenAlex+Europe PMC+PubMed+bioRxiv)」；生医「PubMed+MeSH 必做」 | 脚本仅 OpenAlex+Crossref（+S2 仅滚雪球） | **补脚本**：Europe PMC + PubMed E-utilities + arXiv（均免 key urllib）；补不动的源降措辞 |
| **citation** | 描述「生成 BibTeX/EndNote/GB-T7714/APA/IEEE」 | `doi_to_any --format` 仅 bibtex/csljson/gbt7714 | **补脚本**：加 `--format apa\|ieee\|ris`，复用已有 `negotiate()` 内容协商 |
| **ip-application** | 7 源专利检索表（CNIPA/Google Patents/WIPO/EPO/Lens/USPTO/OpenAlex） | 能程序化取数专利源=0（OpenAlex 仅论文型 NPL）；docstring 已较诚实 | **降措辞**：L50 明确为「OpenAlex NPL + 专利库请求体构造器(需自带凭证)」；专利库实查标已知缺口 |

> 其余 25 技能无明显承诺差距（result-analysis/data-engineering 等的「工具」节列了 ydata-profiling/deepchecks 等库，但写在「推荐用法」语境，「随技能脚本」小节与真实脚本一一对应，不计差距；可选保守加一句「以下为推荐库非随技能脚本」）。

### B api-key/mailto —— 伪造/私人邮箱硬编码（4 技能 7 脚本）

| 技能 | 脚本 | 现状 | 处置 |
|---|---|---|---|
| **research-ethics** | check_retractions.py | `MAILTO="1833058953@qq.com"`（**真实私人 QQ 邮箱，泄露隐私，最严重**） | 改 `CROSSREF_MAILTO` 环境变量+`--mailto`，不传匿名 |
| **literature-search** | search_normalize / snowball / verify_citations / cn_journal_probe | `MAILTO="light-skill@example.com"`（伪造） | 同上，OPENALEX/CROSSREF 双口径 + `--api-key` |
| **citation** | doi_to_any / verify_refs / verify_citation_edge | `light.research@gmail.com`（伪造） | 同上 |
| **ip-application** | patent_search.py | 已 `--mailto` 参数化；自承「尚未透传 api_key，已知缺口」 | 补 `--api-key` 透传 |

> **已合规标杆**（db01 重构时已修，作模板）：`venue-matching/venue_signal.py`（环境变量+`--mailto`+不伪造）。

### C 离线降级 —— 多数已闭环，逐脚本复核

| 技能 | 状态 |
|---|---|
| **literature-search** | search_normalize / snowball / cn_journal_probe **已有 `[OFFLINE]` 回退**；verify_citations 待复核 |
| **citation** | 三脚本 selftest 离线；联网失败时放行规则待复核 |
| **research-ethics** | check_retractions 网络失败返回 UNRESOLVED（不崩，待确认是否够「状态机」） |
| **venue-matching** | 已有完整离线 selftest + 各信号独立降级（标杆） |

---

## 执行进度（逐项勾掉）

> 状态：⬜ 待办 / 🔧 进行中 / ✅ 完成（CI+selftest 过）

### B 类（邮箱+api-key）—— 先修，最伤诚实，改动确定
- ✅ B1 research-ethics/check_retractions.py — 私人邮箱（最高优先）→ 改 CROSSREF_MAILTO 环境变量+`--mailto`，删旧 pyc，selftest 过，私人邮箱全仓清除
- ✅ B2 citation/doi_to_any.py — UA 去伪造化+`--mailto`/CROSSREF_MAILTO（doi.org 协商无需 key）；与 A2 合并改
- ✅ B3 citation/verify_refs.py — `_MAILTO`/`_API_KEY` 运行时可配，Crossref+OpenAlex 双源 helper，加 `--mailto`/`--api-key`，selftest 过
- ✅ B4 citation/verify_citation_edge.py — UA 去伪造化+`--mailto`；S2 加 `--s2-api-key`/S2_API_KEY（x-api-key header），selftest 过
- ✅ B5 literature-search/search_normalize.py — `_MAILTO`/`_API_KEY` 运行时，`_oa_params`/`_cr_params` helper，加 `--mailto`/`--api-key`，selftest 离线过
- ✅ B6 literature-search/snowball.py — 补 `import os`，`_oa_suffix`/`_oa_dict` 处理字符串+dict 两型，S2 加 `--s2-api-key`，加 `--mailto`/`--api-key`，selftest 过
- ✅ B7 literature-search/verify_citations.py — 补 `import os`，doi.org+Crossref 双源 `_user_agent`+mailto 后缀，加 `--mailto`（无 OpenAlex 故无 key），selftest 过
- ✅ B8 literature-search/cn_journal_probe.py — OpenAlex sources 查询 `_user_agent`+按需注入，加 `--mailto`/`--api-key`，selftest 过
- ✅ B9 ip-application/patent_search.py — 补 `import os`+全局 `_API_KEY`，`_http_get_json` 对 OpenAlex 域名统一注入 key（不污染专利库请求），加 `--api-key`，更新自承缺口声明，selftest 过

### A 类（承诺>能力）—— 能补脚本就补
- ✅ A1 literature-search — 新增 biomedical_search.py（Europe PMC+PubMed+MeSH 透传）+ arxiv_search.py（arXiv Atom+bioRxiv 本地过滤）；登记 WHATS_INCLUDED（scripts 49→51）；SKILL 脚本节+生医纪律措辞校准；MeSH 自动映射如实标 P2 未做；CI 全绿
- ✅ A2 citation — doi_to_any 补 `--format apa|ieee|ris`（复用 negotiate() 内容协商，apa/ieee 标"非本地排版"），selftest 加注册断言
- ✅ A3 ip-application — SKILL 表格后加"脚本能力边界"诚实声明（区分 OpenAlex 可程序化 / Lens-EPO-USPTO 仅请求体 / CNIPA-Google-WIPO 纯人工）；L50 措辞校准 + 示例加 `--api-key`

### C 类（离线降级复核）
- ✅ C1 citation 三脚本联网失败放行规则复核 — verify_citation_edge 已三态(unknown 不裸 false)；doi_to_any 取不到打 [ERROR HTTP]；**verify_refs 实质改进**：裁决区分 code=0 网络失败(unverified_offline，warning 不报 high) vs 404 真查不到(疑似臆造 high)，新增 summary.unverified_offline_count + offline_note，selftest 加离线降级断言
- ✅ C2 research-ethics check_retractions 状态机复核 — UNRESOLVED 已是诚实未核验态(不崩不假装 CLEAN)；SKILL 第4条补离线降级协议(UNRESOLVED=未核验非无撤稿，不放行)
- ✅ C3 SKILL 层离线降级协议 — citation workflow 第3步补"离线降级协议"(三态+不得把没连网当已核验通过+不放行闸门)；research-ethics 同步

### 收尾
- ✅ 四 CI 校验器全绿（check_skill_assets 51脚本/51登记/51selftest · check_skill_links · check_entry_docs · check_databases）
- ✅ 所有改动脚本 `--selftest` 离线过（含新增 2 脚本；CI 逐个跑过全部 51 个）
- ✅ WHATS_INCLUDED.md 同步（scripts 49→51，新增 arxiv_search / biomedical_search 登记行）
- ✅ 全仓伪造/私人邮箱终检：私人 QQ 邮箱 0 处、伪造邮箱字面量 0 处（注释里的说明性提及也已去具体地址）

---

## 本轮 P0 全扫结论

**涉及技能**：literature-search（A1+B5-B8）、citation（A2+B2-B4+C1+C3）、ip-application（A3+B9）、research-ethics（B1+C2）。其余 24 技能经 Explore 核查无 P0 承诺差距、无联网脚本，本轮不涉及。

**三类问题处置**：
- **A 承诺>能力**：literature-search 补 2 个真脚本兑现生医/预印本承诺（能补则补）；citation 补 3 格式；ip-application 降措辞标边界（补不动则降）。
- **B api-key/mailto**：9 脚本全部去伪造化，统一环境变量+`--mailto`/`--api-key`/`--s2-api-key`，不传则匿名（不伪造）。私人邮箱泄露已根除。
- **C 离线降级**：verify_refs 实质改进（网络失败≠疑似臆造≠已核验，三态裁决）；citation/research-ethics SKILL 补离线降级协议（闸门无网不放行、不假装已核验）。

**未做（如实标注）**：
- MeSH 自由词→主题词自动映射（需接 NCBI MeSH 库）→ 归 P2，SKILL/脚本已标。
- arxiv/biomedical 新脚本尚未串入 search_normalize 的统一去重管线（各自独立输出）→ 可 P2 整合。
- P1（硬编码阈值/领域 profile/结构化多样性）、P2（批量排序/真实检索后端）未动，属后续批次。
