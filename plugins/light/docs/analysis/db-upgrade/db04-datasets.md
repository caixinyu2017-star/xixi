# db04-datasets 升级规划

> 分析日期 2026-06-13 ｜ 基于真实 schema + 依赖技能消费方式 ｜ 只读规划,未动库
> 原始库标识：db04-datasets（数据集/benchmark/开源项目卡库，真实 schema 16 字段：dataset_name, domain, task, data_type, size, format, license, download_url, paper_url, citation, leaderboard_url, known_issues, bias_risk, privacy_risk, preprocessing_steps, recommended_splits；实体卡分布在 8 个 cards_*.md，dataset_cards.md 仅留模板+canonical 索引，README 宣称 ~100 张）

## 目标形态
升级后 db04 分三层。事实层（dataset_name/domain/task/data_type/size/format/privacy_risk）继续本地精养，是卡的锚点；B-易变层（citation 被引/license/download_url/paper_url/leaderboard_url）退化为"薄缓存"——只存快照值+last_checked+来源指针（OpenAlex W-id / HF repo / GitHub repo / PWC slug），由新脚本 scripts/dataset_signal.py 实时校验，冲突默认信在线；A-通用方法论层（preprocessing_steps/recommended_splits 里的防泄漏/time-forward/按组分域）抽到 m02 数据方法论资产，卡内只留 dataset-specific 片段（如 ImageNet mean-std）+ 一行指针；A-偏科层（bias_risk/known_issues 里"KITTI 单城/ImageNet 西方中心"这类带方向前提的判断）打 domain_scope 标签隔离，非该方向用户可过滤。README 卖点从"~100 张 16 字段全精养卡"诚实改写为"~100 张卡：事实锚点本地 + 易变字段实时校验 + 方法论层复用 + 偏科隔离"。

## 逐字段处置
| 字段/内容块 | 类别 | 动作 |
|---|---|---|
| dataset_name | A-通用 | 留本地。卡主键，canonical 索引去重靠它（dataset_cards.md 已有此约定），不动。 |
| domain | B-事实 | 留本地，但升级为隔离主轴：作为 research_field 过滤键，m03/m05 按它筛卡。值规范化（如统一'计算机视觉'/'NLP'/'奶山羊'）。 |
| task | B-事实 | 留本地。canonical 任务定义稳定，不转。 |
| data_type | B-事实 | 留本地。m03 data-driven idea 的核心输入（SKILL 明确查 data_type 找数据角度），稳定不转。 |
| size | B-事实 | 留本地。canonical 数据集规模基本不变（ImageNet 1.28M），不值得实时；新版本号变化时手动更。 |
| format | B-事实 | 留本地，稳定。 |
| license | B-状态 | 半转实时+薄缓存。能查的（HF cardData.license / GitHub license.spdx_id）转实时校验；官网自定义协议/data.bris/on-request（如 Cityscapes/Cows2021）无 API，保持本地'待核查'文本不强转。冲突信在线，但 license 变更（如 LAION→Re-LAION 下架）必须人工确认再改卡。 |
| download_url | C-状态 | 转实时存活校验（HEAD/GET 200）。link rot 高发（MNIST 原站/LAION 下架已记录），薄缓存存 URL+last_checked，校验失败标 dead 提示换镜像。 |
| paper_url | B-事实 | 保留为来源指针。值已是 openalex.org/W-id，作为 citation 实时查的 key，不删。 |
| citation | B-易变 | 转实时。当前是'Russakovsky 2015, 被引 40,129 (2026-06-06)'混排文本，拆成 结构化书目(留本地) + 被引快照值+last_checked(薄缓存) + W-id(指针)，被引由 OpenAlex cited_by_count 实拉，信在线。 |
| leaderboard_url | B-事实 | 转实时校验存活（PapersWithCode SOTA 页 URL 稳定）；SOTA 数值是否实拉取决于 PWC API 能力（待核实）。薄缓存存 URL+slug+last_checked。 |
| known_issues | A-偏科 | 拆分隔离。通用部分（标签噪声/已饱和/标注主观）留本地通用；带方向前提部分（Cityscapes 仅德国城市/CoNLL 新闻领域窄）打 domain_scope 标签，过滤时随方向显隐。 |
| bias_risk | A-偏科 | 打 domain_scope 标签隔离。ImageNet 西方中心/KITTI 单城/CelebA 人口学偏差都是方向相关判断，非该领域用户应能过滤掉，避免误套用。 |
| privacy_risk | A-通用 | 留本地精养。合规判断（含 PII/肖像权/GDPR）跨学科通用且稳定，是 a10 合规联动的依据，不转不隔离。 |
| preprocessing_steps | A-通用 | 抽方法论层 + 留残片。通用方法论（防泄漏：标准化/插补封进 Pipeline 只在训练折 fit）抽到 m02，卡内只留 dataset-specific（ImageNet mean-std 0.1307/COCO JSON 解析）+ 指针到 m02。 |
| recommended_splits | A-通用 | 抽方法论层 + 留残片。通用原则（time-forward split 防穿越、按牧场/地点/时间分域防泄漏、test 隐藏需提交）抽到 m02 数据方法论；卡内留官方 split 具体数字（train2017 118k 等）。 |

## B 类转实时设计
复用 light-venue-matching/scripts/venue_signal.py 的 http_fetch + _add_mailto 模式，新建 db04-datasets/scripts/dataset_signal.py（带 --selftest 离线 mock，与仓库脚本约定一致）。
【被引 citation — 已实测可用】GET https://api.openalex.org/works/{W-id}?select=id,cited_by_count,publication_year（W-id 来自 paper_url，venue_signal 已验证 /sources 同源端点存活）。接入口径（是否需 key/$1 天额度/退避）一律引 m01 references『OpenAlex 接入真相源』，脚本只带 ?mailto= 进礼貌池，不复写数字。
【license/download 存活 — 部分可用】HF 数据集：GET https://huggingface.co/api/datasets/{repo} 取 cardData.license（端点待核实精确字段名，标'待核实 API 能力'）；GitHub 仓库（AP-10K/APT-36K/GoatABRD 等）：GET https://api.github.com/repos/{owner}/{repo} 取 license.spdx_id（animal_livestock 卡已用 GitHub API 核实过，复用）；download_url 存活做 HEAD 200 校验。
【leaderboard — 待核实】PapersWithCode 有 /api/v1/，但 SOTA 数值抓取能力未实测，先只做 URL HEAD 存活校验，SOTA 数值留手动，标'待核实 PWC API 能力'，不编造端点。
【薄缓存存什么】每个 B 字段存三元组：snapshot_value（被引数值/license SPDX/URL）+ last_checked（ISO 日期）+ source_pointer（W-id / hf:repo / gh:owner/repo / pwc:slug）。
【冲突信谁】默认信在线（用户已定）：实时值与本地快照不一致时，用在线值，并回写快照+刷新 last_checked；唯 license 例外，变更需人工确认（合规高危）。
【无网降级】沿用 venue_signal 的 status=unavailable+reason 模式：取数失败/无 key/离线 → 返回本地快照 + stale 警告（标 last_checked 距今多久），不崩、不阻断下游，由 m05 决定是否带病使用。

## 偏科隔离设计
给每张卡新增 domain_scope 字段（或在 bias_risk/known_issues 行内用 [scope:xxx] 前缀，取决于 schema 决策）。domain_scope 标注该卡 bias/issues 判断成立的方向边界，如 ImageNet=通用CV、KITTI/Cityscapes=自动驾驶+特定地域、奶山羊卡=精准畜牧。现有 domain 字段作为粗粒度 research_field 过滤键，domain_scope 作为细粒度偏科边界。过滤方式：m03/m05 消费时先按用户研究方向匹配 domain/domain_scope，方向外的 bias_risk/known_issues 判断默认折叠或加'(仅适用于X方向)'提示，避免把'西方中心''单城偏差'误套用到不相关领域。奶山羊现状评估说明卡（domain=元说明）天然是偏科隔离的极端样例，已自带方向前提，归入此机制。

## A-通用判断 → 方法论层
preprocessing_steps/recommended_splits 中反复出现的通用判断（防泄漏：标准化/插补/编码封进 sklearn Pipeline+ColumnTransformer 只在训练折 fit；time-forward split 防未来穿越；按 group/牧场/地点/时间分域防泄漏；test 集隐藏需提交）其实已是 m02 light-data-engineering SKILL『处理流程·划分』和『防泄漏铁律』的内容。沉淀方式：不在 db04 重复，而是在 m02 SKILL 该节固化为命名方法论条目（如 LEAK-01 训练折内 fit、SPLIT-01 按组分域、SPLIT-02 time-forward），db04 卡的这两个字段只保留 dataset-specific 实参（ImageNet mean-std、COCO test-dev 需提交、Cows2021 按已知/未知个体划分），并加一行指针'通用防泄漏/分域见 m02 §划分'。这样 A-通用判断对任意学科成立、单点维护，偏科数据集只贡献它独有的参数。

## schema 改动
CONVENTIONS §3 数据集卡当前 16 字段固定。升级需新增：domain_scope（偏科边界）、被引/license/url 的薄缓存结构（snapshot_value+last_checked+source_pointer）。两种实现待决：(A) 扩 §3 schema 显式加字段（yaml 卡无 CSV 列 CI 约束，比 db01 灵活，可加）；(B) 仿 db01 venues.csv 的 risk_note catch-all 做法，把 domain_scope/last_checked 塞进现有字段文本前缀不加字段。建议 A（db04 是 yaml 非定列 CSV，加字段成本低且机器可解析），但需用户拍板是否动 §3 真相源。citation 字段必须从'文本混排被引数+日期'拆成结构化(书目本地 / 被引快照+last_checked / W-id 指针)。

## 影响的技能及改法
- **light-data-engineering (m02)**：①assets/data_card_template.md 加 domain_scope + 薄缓存三字段(snapshot/last_checked/source_pointer)，与 db04 新 schema 对齐；②SKILL『处理流程·划分』固化命名方法论条目(LEAK-01/SPLIT-01/02)，作为 db04 preprocessing/splits 字段的指针目标；③自建数据集产出 dataset_card 时按新分层填（事实本地、易变留指针、偏科打 domain_scope）。
- **light-research-plan (m05)**：SKILL 实验设计节现在写'数据集(来自 db04：规模/划分/许可/已知问题)'是信本地卡——改为：规模/划分信本地事实层；citation/leaderboard/license 改为开工时跑 scripts/dataset_signal.py 实时校验(信在线)，本地快照仅作无网降级；bias_risk/known_issues 按本项目 domain_scope 过滤，方向外的不当坑预判。
- **light-idea-generation (m03)**：SKILL data-driven 节'查 db04 的 data_type/已知偏倚/许可'——data_type 仍信本地；'已知偏倚'(bias_risk)必须按 domain_scope 过滤后再用，防止把某方向的偏差判断误当成通用机会/障碍；license 用实时值判可行性。
- **light-venue-matching**：无需改，其 scripts/venue_signal.py 是 dataset_signal.py 的复用母本(http_fetch/_add_mailto/优雅降级/selftest 模式直接照搬)，反向证明 OpenAlex 实时模式在本仓库已跑通。
- **light-literature-search (m01)**：无需改结论。dataset_signal.py 的 OpenAlex 接入口径(key/限流/退避)一律指针引用 m01 references『OpenAlex 接入真相源』，不在 db04 复写数字(遵 CONVENTIONS §1 单一真相源)。

## 迁移步骤
- 1. 决策定稿：先确认 decisions_needed 的 6 点（尤其 schema 加字段 vs catch-all、license 半转边界、无网是否阻断），再动手。
- 2. 改 CONVENTIONS.md §3 数据集卡 schema：加 domain_scope，并把 citation 拆为 citation_bib(本地) + cited_count_snapshot + last_checked + source_id；同步该文件为唯一真相源。
- 3. 在 m02 SKILL.md『处理流程·划分』固化命名方法论条目 LEAK-01/SPLIT-01/SPLIT-02，作为指针目标。
- 4. 新建 db04-datasets/scripts/dataset_signal.py（照搬 venue_signal.py 的 http_fetch/_add_mailto/降级/--selftest），实现：OpenAlex /works/{W-id} 取 cited_by_count；GitHub /repos 取 license.spdx_id；HF /api/datasets 取 license（标待核实）；download/leaderboard URL HEAD 存活校验。带离线 mock selftest。
- 5. 逐 cards_*.md 迁移字段（8 个文件）：preprocessing_steps/recommended_splits 抽通用句到 m02、留 dataset-specific 残片+指针；bias_risk/known_issues 拆通用 vs 偏科、偏科加 domain_scope；citation 拆结构化；为每张卡填 source_pointer。先迁最大的 cards_frontier/animal_livestock/cv_nlp 验证模式，再批量其余 5 个。
- 6. 更新 m02 assets/data_card_template.md：加 domain_scope + 薄缓存三字段。
- 7. 改 m05/m03 SKILL.md 对 db04 的引用措辞（按 affected_skills 所述：实时查 vs 信本地、按 domain_scope 过滤）。
- 8. 改 db04 README.md：诚实同步卖点（卡数不缩水但'全精养'改为分层；声明易变字段已转实时校验、附 dataset_signal.py 用法）；更新 dataset_cards.md 模板字段。
- 9. 跑 dataset_signal.py --selftest 验证离线通过；抽 3-5 张卡做一次真实联网校验（如带 key 查 ImageNet W2117539524 被引），确认端点与降级路径。
- 10. 把本次为边界级决策（B 转实时/偏科隔离哲学）记一篇 docs/design/ 决策记录（遵 CONVENTIONS §8）。

## ⚠ 需要你拍板的决策点
- 薄缓存粒度：citation 被引存数值快照(40,129)+last_checked 利于无网降级但易显旧，还是只存 W-id 指针每次必实拉(无网即无值)？建议存快照+date，但请拍板。
- schema 落地方式：domain_scope/last_checked 进 CONVENTIONS §3 显式加字段(yaml 卡可行)，还是仿 db01 用现有字段文本 catch-all 不加字段？影响是否动跨库真相源。
- license 转实时边界：HF/GitHub 能查的转、官网自定义协议/data.bris/on-request 留本地'待核查'——接受这种'半转'，还是 license 一律留本地不转(只人工核)？
- leaderboard：PapersWithCode API 抓 SOTA 数值能力未实测——先只做 URL 存活校验、SOTA 留手动，可接受吗？还是要我先去核实 PWC /api/v1 能力再定？
- 无网/无 key 时 m05 取数：允许带本地 stale 快照继续(降级警告)，还是阻断要求联网核实后才进实验设计？
- README 卖点措辞：卡数不缩水但'~100 张 16 字段全精养'要改为'事实锚点+实时校验+方法论层+偏科隔离'的分层表述——确认这个诚实改写口径。

## 工作量与风险
- 工作量：中-重。8 个 cards 文件逐卡迁移字段是主要工作量（~80-100 张卡 × 5 字段拆分）；dataset_signal.py 有 venue_signal.py 现成母本可照搬，约 1 个脚本工作量（轻）；CONVENTIONS/3 个 SKILL/README/模板的引用改动是轻量但要一致。风险点在卡级迁移的体量与一致性。
- 风险：①联网依赖加重：m05/m03 取数从纯本地变为依赖 OpenAlex(需 key+$1/天额度)/GitHub/HF/PWC，无网或限流时降级到 stale 快照，需保证降级不阻断主线。②迁移破坏现有引用：m05 SKILL 明文'数据集(来自 db04：规模/划分/许可/已知问题)'、m03'查 data_type/已知偏倚/许可'若不同步改，会出现技能仍信本地卡而卡已转指针的割裂。③偏科隔离过度：domain_scope 打标太细会让 bias_risk 通用警示(如 PII 风险)被误折叠，需区分'通用警示不隔离'与'方向判断才隔离'。④license 信在线的合规风险：license 是 a10 合规命脉，盲目信在线可能漏掉'API 未反映的下架/协议变更'(LAION 教训)，故 license 变更强制人工确认。⑤PWC/HF 端点能力未实测，若编造端点违反 CONVENTIONS §4 诚实底线——已标'待核实'规避。
