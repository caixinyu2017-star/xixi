# db01 方法论层 (references.md)

> 本文件是 db01 的 **A-通用方法论层**（库重构定稿，2026-06-13）。venues.csv 的事实行是"薄缓存"（快照值 + last_checked + 锚点指针，冲突默认信在线）；本文件沉淀**跨学科通用、几乎不过时**的判断与查询口径，是这个库真正的资产。
>
> 架构见 [`docs/analysis/db-upgrade/db01-venues-templates.md`](../../docs/analysis/db-upgrade/db01-venues-templates.md)。

---

## 一、risk_note 标准子串（机读锚点与口径标记）

venues.csv 的 `risk_note` 是 catch-all 列，承载以下**机读子串**（分号分隔，`key=value`，供 venue_signal.py 等消费方精确解析，不破 19 列 CI schema）：

| 子串 | 含义 | 取值 | 谁消费 |
|---|---|---|---|
| `oa_id=` | OpenAlex 源 id（实时复查主键） | `S` + 数字 | venue_signal batch/实时查 |
| `issn=` | 规整后的 ISSN（实时复查主键） | `XXXX-XXXX` | venue_signal `_load_card_from_csv` 精确匹配 |
| `domain_scope=` | 偏科隔离标签（G2） | `中国CS` / `中国语境` / `通用` | venue-matching 按方向过滤 |
| `if_kind=` | impact_factor 列的口径（G3/G5） | `jcr` / `proxy` / `na` | venue_signal 信号5 区分真值/代理值 |
| `ai_policy=` | 生成式 AI 投稿政策 | 要点(来源;日期) | a10 / m07 |
| `CCF等级=` | CCF 档位来源 | A/B/C(来源) | venue-matching |

> 新增子串遵循同模式：`key=value`，分号分隔，不加 CSV 列。migrate_db01_v2.py 幂等回填 oa_id/issn/domain_scope/if_kind。

### if_kind 口径（诚实红线，最重要）
- **`if_kind=jcr`**：impact_factor 是**真 JCR 值**（带 LetPub `journalid=`），权威快照。G3 原则：JCR/中科院分区是 Clarivate/中科院**付费数据，OpenAlex 查不到**，故这类本地快照**不被在线代理值覆盖**，投前仍核最新年度。当前仅 5 行（TPAMI/TKDE/TIP/TNNLS/TC）。
- **`if_kind=proxy`**：impact_factor 是 **OpenAlex 2yr 均被引代理值**或"付费墙不可得"。**绝不可当 JCR 真值引用**。venue_signal 会附在线 2yr 值供交叉验证。当前 245 行。
- **`if_kind=na`**：会议或无 JCR 收录，无 IF。当前 58 行。

> **为什么这样设计**：旧版 impact_factor 列把真 JCR(5 行) 和 OpenAlex 代理(245 行) 混在一起，只靠人读那句中文区分。if_kind 让机器能区分，杜绝"用代理值冒充 JCR"这个编造风险。

### domain_scope 口径（偏科隔离）
- **`中国CS`**：有 CCF 等级——CCF 是中国计算机专属评价体系，非 CS 用户应过滤。98 行。
- **`中国语境`**：有中科院分区但无 CCF——主要对投中国体系用户有意义。115 行。
- **`通用`**：纯国际 SCI / 国际会议，跨学科通用。95 行。

> **诚实提醒**：本库 46 个会议 **100% 是 CS 方向**（CVPR/NeurIPS/ICML/ACL/KDD...），其他学科会议待扩。期刊侧覆盖较广但非 CS 学科的行多为薄快照、关键字段（真分区/APC/代表作）大面积"待核查"。

---

## 二、reference_style → LaTeX cls/bst 映射表（跨学科稳定资产）

publisher/venue 的 `reference_style` 字段 → 对应 LaTeX 文档类与参考文献样式。这是 **m10(引用)/m12(排版) 直接复用**的核心资产，与具体 venue 无关、多年稳定。两个技能应同源读此表，不各读各的。

| reference_style | LaTeX 文档类 | bst/CSL | 备注 |
|---|---|---|---|
| IEEE | `IEEEtran` | `IEEEtran.bst` | 数字方括号 [1] |
| ACM | `acmart` | `ACM-Reference-Format.bst` | acmart 自带 |
| Elsevier | `elsarticle` | `elsarticle-num.bst` / `elsarticle-harv.bst` | 多数 Elsevier 刊 num |
| Springer | `svjour3` / `sn-jnl` | `spbasic.bst` / `sn-mathphys.bst` | 看具体系列 |
| Springer LNCS | `llncs` | `splncs04.bst` | 会议论文集常见 |
| Wiley | `wiley` / 期刊模板 | `wileyNJD-*.bst` | 各刊有专属 |
| Nature | `nature` | CSL `nature.csl` | 上标数字 |
| Science | 投稿用 Word/特定模板 | CSL `science.csl` | Science 系列 |
| Cell Press | Cell 模板 | CSL `cell.csl` | numbered |
| ACS | `achemso` | `achemso.bst` | 化学 |
| RSC | RSC 模板 | CSL `rsc.csl` | 化学 |
| GB/T 7714 | `ctexart` + `gbt7714` | `gbt7714-numerical.bst` | 中文国标，数字/著者-出版年两式 |
| Vancouver(各 numbered) | 医学期刊模板 | CSL `vancouver.csl` | 医学通用，各刊微调 |
| ACL | `acl` | `acl_natbib.bst` | NLP 会议 |
| AAAI / IJCAI / NeurIPS / ICML / JMLR(自定义.sty) | 各会议官方 `.sty` | 各自 .bst | 从会议官网取当年模板 |
| MDPI / Frontiers / PLOS / PeerJ(自定义) | 各社官方模板 | 各社 CSL | OA 社，官网下载 |

**长尾原则**（表中未列的 `自定义(X.sty)` / 小众样式）：一律从该 venue 官网 author kit / Overleaf 官方模板取当期 `.cls`+`.bst`，不猜测、不复用旧版。`template_url` 字段是易腐链接，取用前校验 200，失链回 venue 官网。

---

## 三、subject_area 受控词归一表（261 碎值 → ~30 大方向）

**问题**：venues.csv 的 subject_area 实测 308 行有 261 个不同值、233 个只出现一次（如"遥感/地球观测(交叉)""理论计算机科学/算法"），venue-matching 按方向筛根本筛不动。

**方案**：归一到 ~30 个受控大方向供筛选，原 subject_area 值保留作二级标签（细分信息不丢）。

| 受控大方向 | 归并的碎值示例 |
|---|---|
| 计算机视觉 | 计算机视觉, 图像处理, 模式识别 |
| 机器学习/AI | 机器学习, 人工智能, 深度学习, 强化学习 |
| 自然语言处理 | 自然语言处理, 计算语言学, 语音 |
| 数据挖掘/IR | 数据挖掘, 信息检索, 推荐系统 |
| 计算机系统 | 操作系统/系统, 体系结构, 分布式, 网络, 数据库 |
| 软件工程/理论 | 软件工程, 程序设计语言, 理论计算机科学/算法, 形式化方法 |
| 机器人/控制 | 机器人, 自动化控制, 智能系统 |
| 生物信息/计算生物 | 生物信息学, 计算生物学, 基因组学 |
| 生物医学/临床 | 医学, 临床, 放射, 病理, 公共卫生 |
| 神经科学 | 神经科学, 脑科学, 认知 |
| 农业/畜牧/兽医 | 农业, 畜牧, 兽医, 食品科学, 动物科学 |
| 材料科学 | 材料, 纳米, 复合材料 |
| 化学 | 化学, 有机化学, 分析化学, 物理化学 |
| 物理 | 物理, 凝聚态, 光学, 高能 |
| 地球/环境/遥感 | 遥感/地球观测, 大气, 海洋, 地质, 环境科学 |
| 能源 | 能源, 电力, 新能源, 储能 |
| 统计/数学 | 统计学, 应用数学, 概率, 运筹 |
| 经济/金融 | 经济学, 金融, 计量经济 |
| 管理/信息系统 | 管理科学, 信息系统, 运营管理 |
| 社会科学 | 社会学, 心理学, 教育, 政治, 传播 |
| 综合/跨学科 | 综合自然科学, 计算机综合, 交叉学科 |

> 完整归一映射在扩库时维护。venue-matching 按大方向筛候选 → 命中后用二级标签精排。

---

## 四、实时复查管线（薄缓存的"活水"）

venues.csv 的 B 类事实（IF/被引/APC/h_index/发文趋势）是快照，靠 venue_signal.py 保持新鲜：

1. **单候选**：`venue_signal.py --issn <ISSN> --venues-csv <path>` —— 五信号实时查 OpenAlex + 读本地卡，冲突信在线（JCR 真值除外，见 §1 if_kind）。
2. **全库复查**：`venue_signal.py --batch <venues.csv>` —— 逐行按 issn 锚点查 OpenAlex，产"在线值 vs 本地快照"diff 清单，喂给月度保鲜。
3. **保鲜触发**：`check_freshness.py` 读 last_checked_date 产超期清单 → 超期行喂步骤2复查。
4. **礼貌池**：`--mailto you@inst.edu` 或环境变量 `OPENALEX_MAILTO`；不传匿名查（不伪造邮箱）。OpenAlex key/限流口径见 m01 references「OpenAlex 接入真相源」节。

### 采集→双源核验→入库铁律（建库/扩库照此复现）
1. **采集**：OpenAlex Sources API 按方向 `search=`/`filter=` 拉候选，记 ISSN/display_name/works_count/summary_stats/host/type。
2. **双源核验**：按精确 ISSN 回查 OpenAlex（不盲取 search 第一条），比对年份/被引/works_count 合理性；剔除 works_count<50 碎片与重名/同 ISSN 重复。
3. **入库**：按 19 列 schema 生成行；impact_factor 必标 if_kind 口径（真 JCR vs OpenAlex 代理）；含逗号字段加引号（交程序按 CSV 规范转义）。
4. **校验**：`PYTHONUTF8=1 python .github/scripts/check_databases.py`；自检列数=19、物理行数==逻辑行数（无多行字段被压平）。
5. **落锚点**：新增行写 `oa_id=`/`issn=`/`domain_scope=`/`if_kind=` 子串 + `last_checked_date`。

> 改 venues.csv 三条血泪铁律（R4/R8）：①含多行字段时禁用 csv 模块全量重写（会压平）——本库当前无多行字段，重写前务必先验"物理行数==逻辑行数"；②无引号字段禁含英文逗号（会拆列）；③`last_checked_date` 必须日期格式。migrate_db01_v2.py 已遵守。
