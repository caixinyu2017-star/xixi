# R4.1 撤稿核查接线 — 联网实查留痕

- 研究日期：2026-06-11
- 执行：Claude Opus 4.8（Claude Code）
- 任务：light-citation/verify_refs.py 复用 light-research-ethics/check_retractions.py 的
  撤稿判定逻辑，对每条 DOI 检查 Crossref `message.update-to[]` 含 retraction 类型者报 high severity。

## 1. Crossref `update-to` 字段真实行为（实查）

端点：`https://api.crossref.org/works/{doi}?mailto=...`（HTTP 200）

### 1.1 经典撤稿论文「本身」的记录——update-to 多为空
| DOI | 标题 | update-to |
|---|---|---|
| 10.1016/S0140-6736(97)11096-0 | RETRACTED: Ileal-lymphoid-nodular hyperplasia…（Wakefield 1998 Lancet） | NONE |
| 10.1038/nature12968 | RETRACTED ARTICLE: Stimulus-triggered fate conversion…（STAP 细胞） | NONE |
| 10.1126/science.1078616 | （已撤 Science 论文） | NONE |

→ 印证 check_retractions.py 注释的诚实局限：**被撤论文本身不一定暴露 `update-to[]`**
（publisher-dependent）。这类记录的撤稿信号体现在**标题 `RETRACTED` 前缀**上，而非 update-to。

### 1.2 真正在 update-to 暴露 retraction 的记录（Elsevier 样例）
用 `filter=update-type:retraction` 拉取（命中 72416 条，取前 3，均 self-referential）：

| DOI | 标题 | update-to[].type |
|---|---|---|
| **10.1016/j.micpro.2020.103768** | RETRACTED: Cross-Cultural communication of language learning… | retraction |
| 10.1016/j.micpro.2021.103927 | RETRACTED: Research on the spread effect of data record… | retraction |
| 10.1016/j.micpro.2020.103708 | RETRACTED: Development of financial option pricing system… | retraction |

→ 选 **10.1016/j.micpro.2020.103768** 作为本技能的正向测试样例（update-to 含 retraction）。

## 2. 现有 check_retractions.py 实跑验证（同源真相）

```
PYTHONUTF8=1 python skills/light-research-ethics/scripts/check_retractions.py \
    10.1016/j.micpro.2020.103768 10.1038/s41597-023-02555-8
```
输出：
- `10.1016/j.micpro.2020.103768` → 🛑 RETRACTED
- `10.1038/s41597-023-02555-8`（CherryChèvre 正常数据集论文）→ ✅ CLEAN

## 3. 接线设计决策

- **不跨技能 import**：装到 `~/.claude/skills/` 后 light-citation 与 light-research-ethics
  是平级目录，Python 无法 import 对方模块。故在 verify_refs.py 内**内联同源判定逻辑**
  （相同的 `FLAG_TYPES` 常量 + `update-to[].type` 归一化判定），注释指认
  check_retractions.py 为同源真相，两脚本判定口径一致。
- **不新增 HTTP**：verify_refs.py 已取 Crossref `/works/{doi}` 完整 message，
  `update-to` 就在同一响应里，直接解析，零额外请求。
- **诚实局限同步**：沿用 check_retractions.py 的诚实声明——CLEAN 仅表示
  "无 update-to 撤稿信号"，非"保证未撤稿"；高风险引用须交叉查 Retraction Watch。
  额外：标题 `RETRACTED` 前缀也作为补充信号纳入（覆盖 update-to 为空的经典案例）。

## 4. selftest 离线覆盖
verify_refs.py `_selftest()` 增 mock：一条 update-to 含 retraction 的 DOI →
断言 is_retracted=True 且 errors 含 high severity；CLEAN DOI 不误报。离线、不打网。
