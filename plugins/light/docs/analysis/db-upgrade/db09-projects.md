# db09-projects 升级规划

> 分析日期 2026-06-13 ｜ 基于真实 schema + 依赖技能消费方式 ｜ 只读规划,未动库
> 原始库标识：db09-projects — 用户个人项目状态中枢（1 真实项目 dairygoat-detect-track + project_card_template + lessons.md；每项目目录含 project_card.md / decision_log.md / version_history.md / terminology.md / palette.json / literature/{known_dois.txt, saved_search.yaml, watch_report_*.md}）

## 目标形态
升级后 db09 保持"项目状态中枢"本色——14 字段 project_card、decision_log、version_history、terminology、saved_search 全部 C 类，继续本地精养，这是它存在的唯一理由（在线源不知道"你上周决定弃用 re-id"）。真正要动的只是散落在 C 类卡里的少量 B-fact 引用：venue 计量值（h_index=220、2yr 被引 9.19）、数据集许可/DOI、palette 的 hex。这些不立新字段、不离开原卡，而是就地补上"快照值 + last_checked + source_pointer 回指 db01/db04/db05"三件套，约定"投前/用前重核、冲突信在线"，把 db09 内的 B-fact 从"被当事实引用"降级为"带时间戳的线索快照"。palette.json 已经是这个模式的样板（hex+source+last_checked+$aligned_with 回指 db05），把同一纪律推广到另外两处即可。A-通用方法论（lessons.md）天然已分离、继续留本地；A-偏科判断在本库几乎不存在（决策都是项目内 C 类），故隔离改造极轻。净效果：库形态不变，新增的是"B-fact 引用三件套"的硬纪律 + 一个本地可跑的重核脚本，README 卖点诚实改写为"状态中枢 + 在线计量回指"，不再隐含"db09 自带权威计量"。

## 逐字段处置
| 字段/内容块 | 类别 | 动作 |
|---|---|---|
| project_card 14 字段(project_name/goal/current_stage/confirmed_idea/data_status/method_status/experiment_status/paper_status/ppt_status/code_status/risk_list/next_actions/decision_log/version_history) | C-状态 | 全部留本地。这是项目专属、在线不可得的状态，不动 schema、不转实时。 |
| decision_log.md 第7条内嵌的 venue 计量『该刊本方向 h_index=220、2yr 均被引 9.19』 | B-事实 | 转实时(薄缓存)。决策正文(选 CEA 投稿)留本地，把两个数值就地改写为带三件套的快照：『h_index≈220 / 2yr_cited≈9.19 [snapshot 2026-06-12, src=db01:venues.csv#L140, 投前用 venue_signal.py 重核]』。 |
| project_card.data_status / decision_log 第5条 内嵌『CherryChèvre CC许可 DOI:10.57745/4C03OG』『GoatABRD 许可待核』『DiaryGoatMVT 无论文』 | B-事实 | 打来源指针隔离。结论(必须自建标注)是 C 类留本地；许可/DOI 这类 db04 权威字段就地加 src 指针『(license/DOI 见 db04:cards_animal_livestock.md，用前重核)』,db09 只留快照不当权威源。 |
| terminology.md 数据集行『CherryChèvre…CC许可,DOI:10.57745/4C03OG』 | B-事实 | 同上,DOI/许可加 src 指针回指 db04;术语标准叫法/中英对照(A-通用表达资产)留本地。 |
| palette.json 的 hex 值(#4E7D2C 等 12 token) | B-事实 | 留本地薄缓存(已合规)。每 token 已带 source(回指 db06 themes.py/db05 DTCG)+last_checked,且 $aligned_with 声明『色值最终以 db05 DTCG 为准』——这就是目标三件套样板,无需改造,仅作为其他 B-fact 的模仿范式。 |
| saved_search.yaml(query/filters/last_run_date/cadence) | C-状态 | 留本地。这是本项目的检索状态(上次跑到哪、下次从哪天增量),在线不可得。 |
| known_dois.txt(24 条已读 DOI) | C-状态(指针集) | 留本地。是『本项目已读哪些』的去重状态,非文献元数据本身;DOI 背后的题录/被引交给 m01 实时查,db09 只存指针清单。 |
| watch_report_*.md(增量 diff 报告) | C-状态 | 留本地。是某次追踪的留痕快照,本就带日期,不需重核。 |
| lessons.md(跨项目过程教训,2 条) | A-通用 | 已分离,留本地精养。这是跨学科方法论资产(如『三模块纯串联当创新点会被拒』),正是要保留的 A-通用层,见方法论层说明。 |
| decision_log 中的方法判断(弃 re-id/选 ByteTrack/序数回归等) | A-偏科 | 留本地。带强方向前提(奶山羊白羊外观同质化),是项目内 C 类决策的理由,不抽出、不当跨项目通用;仅在归档时择优回写 lessons(去偏科化表述)。 |

## B 类转实时设计
B 类只有三处、且都已有现成 API 通道,优先复用、不新造:
1) venue 计量(h_index/2yr 被引/分区/APC)→ 复用 light-venue-matching/scripts/venue_signal.py(已实测可用):它封装 OpenAlex Sources `GET https://api.openalex.org/sources/issn:{ISSN}`,取 summary_stats.h_index、2yr_mean_citedness、apc_usd、counts_by_year,并以 db01 venues.csv 兜底分区/审稿周期。CEA 投稿前用 `python venue_signal.py --issn <CEA的ISSN> --venues-csv <db01>/venues.csv` 重核。
2) 数据集许可/DOI/被引 → 权威源是 db04 数据集卡(license/citation/download_url 字段);DOI 题录可经 m01 的 OpenAlex `GET /works/doi:{DOI}` 或 Crossref `GET https://api.crossref.org/works/{DOI}` 核实(literature-search references 已实测 200)。
3) 薄缓存存什么(三件套):①快照值(h_index≈220 这种数值,允许本地留,带 ≈ 表示非精确);②last_checked(YYYY-MM-DD,如 palette 的 last_checked);③source_pointer(指回 db01:venues.csv#行 / db04:卡 / db05 DTCG)。不存全量计量历史、不存被引时间序列(那是 db01/OpenAlex 的事)。
4) 冲突信谁:默认信在线(CONVENTIONS §1『投前重核』+ palette『色值以 db05 为准』已是此纪律);本地快照仅当无网时的降级线索,重核后若不一致就地更新快照值+last_checked。
5) 无网降级:venue_signal.py 已实现优雅降级(任一信号取数失败→status=unavailable+reason,不崩、不编数);db09 侧降级策略=直接用本地快照值但必须显示其 last_checked,提示用户『此为 N 天前快照,联网后重核』,不假装是当前值。
6) 待核实:CEA 的精确 ISSN 未在 db09 中出现(只记 venues.csv 第140行),迁移时需从 db01 取 ISSN 才能跑 venue_signal——标『待取 ISSN』,不编造。

## 偏科隔离设计
本库 A-偏科隔离需求极轻,几乎可判『无需重型隔离』。原因:db09 是项目实例库,每个项目目录天然是一个方向的沙盒(dairygoat 全部内容都是『奶山羊CV』方向),目录本身就是隔离边界,不存在 db01/db03 那种『一张通用卡里混入偏科判断需打 domain_scope 过滤』的问题。具体处置:①不给 project_card / decision_log 引入 domain_scope/research_field 字段(项目目录名+goal 已表达方向,加字段是冗余)。②唯一需要轻隔离的是 lessons.md——它是跨项目库,若未来积累多方向项目,某条教训可能带方向前提。处理办法:沿用其现有格式末段『适用条件』列做软隔离(如『适用条件:外观高度同质化的家畜个体跟踪』),a02 检索 lessons 时按阶段/场景关键词匹配,用户读到即知是否适用本方向,无需新增标签字段。③若用户日后明确要按学科过滤 lessons,再在单行格式追加可选 `#domain:` tag,届时增量加,不预先过度设计。结论:隔离设计=『目录即沙盒 + lessons 用适用条件列软过滤』,不进统一 schema。

## A-通用判断 → 方法论层
A-通用方法论的承载体是 db09 顶层 lessons.md,已和 projects/ 平级分离,且边界定义清晰(收『做法层面有效/失败经验』,不收方法选型事实→db03、不收个人偏好→feedback 记忆)。升级动作不是搬家,而是强化其『去偏科化沉淀』纪律:①归档协议(README 已有)规定项目完结时回写 1-3 条可跨项目复用教训——把这步明确为『回写时须剥离方向前提、抽到对任意学科成立的层面』(如当前『三模块纯串联当创新点会被拒——近同工作已占坑须有方法层 delta』就是好样板,对任何 CV/ML 方向都成立;反例『白羊外观同质化弃 re-id』属偏科,留 decision_log 不上 lessons)。②a02 SKILL 已有『新项目立项/选方法/投稿策略前先 Grep lessons 同类阶段关键词』的检索纪律,这条是方法论复用的入口,保留并在 README 卖点里如实标注为 db09 的 A-通用资产。无需新建目录或新文件。

## schema 改动
不改 CONVENTIONS §3 的 4 个统一字段定义(project_card 14 字段保持原样,这是 CI/check_databases 校验依据,动它会波及全仓库)。不新增 domain_scope/research_field 字段(理由见隔离设计:目录即沙盒)。唯一新增的是『约定层』而非『schema 层』:在 db09 README 定义 B-fact 引用三件套书写规范(快照值+last_checked+source_pointer 内联子串),复用 palette.json 已有的 source/last_checked/$aligned_with 模式作为既成 schema 样板,不为它在 14 字段里加列。consistency_audit.py 可选增加 last_checked 超期 WARN 规则(逻辑改动非 schema)。net:零 schema 字段变更,纯约定与纪律强化。

## 影响的技能及改法
- **light-venue-matching**：已用 venue_signal.py 实时查 OpenAlex Sources,是 B-fact 转实时的现成通道。改动:在 SKILL/references 增一句『db09 decision_log/project_card 内嵌的 venue 计量值为快照,投前用 venue_signal.py --issn 重核,冲突信在线』,把 db09 列为该脚本的下游消费方之一。无代码改动。
- **light-memory-pm(a02)**：它是 db09 的写入执行者,改动最大。①写 decision_log/data_status 引用 venue 计量、数据集许可/DOI 时,强制带三件套(快照值+last_checked+src 指针),禁止裸写数值。②会话开始读 project_card 恢复状态时,对带 last_checked 的 B-fact 快照若超期(如>90天)给『需重核』提示,不直接当当前值汇报。③归档回写 lessons 时执行『去偏科化』纪律(见方法论层)。需改 SKILL『写入步骤示例』与『更新纪律』两节。
- **light-consistency(a07)**：它已把 palette.json 当视觉 SSOT 逐项核(三件套样板)。改动:把同样的『对照 source_pointer 核快照是否过期』检查从 palette 推广到 db09 内其他 B-fact 引用(venue 计量/数据集许可);consistency_audit.py 的 METRIC_VALUE 检测可顺带标记『db09 快照 last_checked 超期』为 WARN。需在 SKILL『视觉规范/变更广播』节补一句覆盖非视觉 B-fact 快照。
- **light-orchestrator(m13/m14 阶段)**：投稿定位阶段(m13)的确认点应要求 venue 计量为新鲜证据(venue_signal 当轮输出),而非 db09 旧快照。改动:在 §3 确认点纪律里点名『db09 内 venue 快照不算新鲜证据,投稿决策点须重核』。无代码改动。
- **light-literature-search(m01)**：它维护 saved_search/known_dois/watch_report(均 C 类,留本地)。改动仅澄清:known_dois.txt 是指针集不是元数据库,DOI 背后的题录/被引一律实时查 OpenAlex/Crossref(references 已有端点),db09 不缓存被引数。基本是确认现状,无实质改动。

## 迁移步骤
- 1. 不动 schema 不动目录结构。先在 db09 README 增『B-fact 引用三件套纪律』一节:凡 db09 卡内引用 venue 计量/数据集许可/DOI/外部数值,必须写成『快照值 + [snapshot YYYY-MM-DD, src=dbNN:文件#定位, 用前重核, 冲突信在线]』,并指 palette.json 为样板。
- 2. 改 decision_log.md 第7条:把『h_index=220、2yr 均被引 9.19』改为带三件套的快照串,src 指 db01:venues.csv 第140行,注『投前用 venue_signal.py 重核』。决策结论文字不动。
- 3. 改 project_card.md data_status 与 decision_log 第5条 + terminology.md 数据集行:CherryChèvre 的 DOI/CC许可、GoatABRD『许可待核』就地加 src 指针『(见 db04:cards_animal_livestock.md,用前重核)』,结论(自建标注)留本地。
- 4. palette.json 不改(已是合规样板),仅在 README 三件套节引用它作范式。
- 5. 改 light-memory-pm/SKILL.md『写入步骤示例』『更新纪律』两节:加『引用外部 B-fact 必带三件套』『读卡时超期快照给重核提示』『归档回写 lessons 去偏科化』三条纪律。
- 6. 改 light-consistency/SKILL.md『变更广播/五维』节:把『对照 source_pointer 核快照过期』从 palette 推广到所有 db09 B-fact;consistency_audit.py 增 last_checked 超期 WARN(可选,需另跑脚本验证)。
- 7. 改 light-orchestrator/SKILL.md §3:m13 投稿决策点要求 venue 计量为当轮新鲜证据,db09 快照不算数。
- 8. 改 light-venue-matching SKILL/references + literature-search references:声明 db09 为 venue_signal/OpenAlex 重核的下游消费方,口径互指不复写。
- 9. 诚实改写 db09 README 卖点:从隐含『自带计量』改为『项目状态中枢 + B-fact 回指在线源』,并说明卡数/字段不缩水(本库 B-fact 极少,只是引用方式变严),区别于其他库的卖点缩水。
- 10. 跑 consistency_audit.py 与 venue_signal.py --selftest 验证未破坏现有引用,确认 a02/a07 仍能正常读 db09。

## ⚠ 需要你拍板的决策点
- 决策1(纪律落点):B-fact 三件套写成『卡内内联子串』(如 decision_log 行尾加 [snapshot...]) 还是另起一个 sources.yaml 旁文件集中管?内联改动小、不破坏现有 14 字段;旁文件更整洁但 a02/a07 要多读一个文件。建议内联(本库 B-fact 仅 3 处,不值得为它建文件)。
- 决策2(快照存不存数值):venue h_index/2yr 被引这类数值,本地薄缓存到底存不存具体值,还是只存 src 指针+last_checked、数值每次现查?存值:无网时有线索、但有过期风险;只存指针:绝不误用旧值、但无网时空白。建议存值但带 ≈ 与 last_checked(对齐 palette 现状)。
- 决策3(超期阈值):a02 读卡时『快照超期给重核提示』的阈值定多少天?venue 计量年级别变化、许可几乎不变,可能需分类(计量90天/许可365天)。需你定或授权我按字段类型分档。
- 决策4(domain_scope 是否进 schema):本库我判断『目录即沙盒』已够隔离、不建议给 project_card 加 domain_scope 字段。若你计划未来跨库统一 schema 都带 domain_scope,需你明确——否则我维持不加。
- 决策5(lessons 去偏科化由谁判):归档回写 lessons 时『剥离方向前提』是 a02 自动判还是每次让你确认?涉及方法论资产质量,建议 a02 起草、你在归档确认点拍板。

## 工作量与风险
- 工作量：轻。3 处内联文本快照改写(decision_log/project_card/terminology) + README 增一节 + 4 个技能各改一两段纪律文字,无数据迁移、无 schema 变更、无破坏性操作;唯一稍重的是 consistency_audit.py 可选加超期 WARN(中,需写测试)。半天内可完成主体,风险与回滚成本都低。
- 风险：本升级是 Light 各库里风险最低的一个:db09 ~82% 是 C 类项目状态,本就该且已经本地存,核心结构(14 字段/目录/模板)完全不动,迁移只触及 3 处内联 B-fact 引用 + 4 个技能的纪律文字。主要风险:①README 卖点改写若措辞不当会被误读为『db09 缩水』,实则本库卡数/字段不减,需在改写中显式说明『本库 B-fact 极少,只是引用方式变严,与其他库的卖点缩水性质不同』。②投稿计量转实时后加重对 OpenAlex 联网与 API key 的依赖(2026 起需 key),无网时只能用快照降级——venue_signal.py 已有优雅降级,但用户若误信过期快照仍有风险,靠 last_checked 强制显示缓解。③CEA 精确 ISSN 不在 db09 内,跑 venue_signal 前须从 db01 取 ISSN,迁移时标『待取』不可编造。④改 a02/a07/orchestrator 的纪律文字属低风险文档改动,但需回归跑 consistency_audit/venue_signal selftest 确保现有 dairygoat 卡的引用不被破坏。整体:轻量,无破坏性数据迁移,可回滚(改的都是文本)。
