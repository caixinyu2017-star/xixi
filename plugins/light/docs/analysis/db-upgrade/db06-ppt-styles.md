# db06-ppt-styles 升级规划

> 分析日期 2026-06-13 ｜ 基于真实 schema + 依赖技能消费方式 ｜ 只读规划,未动库
> 原始库标识：db06-ppt-styles（PPT 版式/叙事方法卡）

## 目标形态
升级后 db06 收敛为「方法论库 + 薄事实缓存」两层。核心层是 slide_card 的 12 字段方法卡（resources_real.md 内嵌 7 张场景卡 + slide_pattern_cards.md 的 10 张页型卡）——这些是跨学科的版式/叙事方法论，原地精养，不动 schema。事实层只剩 resources_real.md 的资源表三列（HTTP 状态码、GitHub 星标、许可），降级为"薄缓存"：保留快照值 + last_checked + API 指针，正式引用时由 light-slides 的 resource_signal.py 实时核（复用 venue_signal.py 的 urllib+优雅降级+selftest 范式），冲突信在线。themes.py 仍是本地 A 类资产（已 selftest，调色板/字体是设计常量非易变事实，全留）。偏科只占极少数（医学蓝白/农业绿等学科色板偏好），用卡内 domain_scope 注释行隔离而非进 12 字段 schema。README 卖点从"15 条实测资源 + 星标/许可"诚实改写为"17 张版式方法卡（精养）+ 资源指针实时核"。

## 逐字段处置
| 字段/内容块 | 类别 | 动作 |
|---|---|---|
| scenario (slide_card 主键) | A-通用 | 留本地。check_databases 强校验唯一性，是方法卡的索引键，跨学科通用。 |
| theme_style / page_type / layout_structure / visual_hierarchy / chart_style / icon_style / transition_style | A-通用 | 留本地精养。纯版式叙事方法论（一页一观点/action-title/data-ink/分步揭示），与学科无关，是本库真正资产。 |
| color_palette | A-通用(部分偏科) | 留本地，但把硬编码 hex 的权威指向 themes.py（开题卡/课程教学卡已写死 #1F4E79 等）。学科色偏好（农业绿/医学蓝白）在卡内加 domain_scope 注释隔离。 |
| font_pairing | A-通用 | 留本地。思源系=SIL OFL 可商用是稳定事实，非易变 IF 类，不必实时。 |
| speaker_notes_style | A-通用 | 留本地。控时方法论（8-12min≈10-15页、45min配15-25页）跨学科成立。 |
| reuse_template_notes | A-通用 + 夹带B类 | 方法论部分留；其中夹带的外链（beamer-theme-matrix、CMU 教学页）和隐含工具星标转到资源表统一实时核，卡内只留'见 resources_real 实时核'指针。 |
| resources_real 资源表·HTTP 状态码列（200/403/000） | B-事实 | 转实时。本地只留快照值+last_checked，引用前 curl -sI 重核；403=反爬非失效要标注。 |
| resources_real 资源表·GitHub 星标（reveal.js 71.6k★ 等） | B-事实 | 转实时。GitHub API stargazers_count 查；本地存快照值+last_checked+repo 指针，冲突信在线。 |
| resources_real 资源表·许可列（MIT / CC-BY-SA-4.0 / SIL OFL） | B-事实(合规敏感) | 转实时但保留本地快照（合规红线，metropolis 的 CC-BY-SA-4.0 必须可追溯）。GitHub API license.spdx_id + PyPI info.license 查。 |
| resources_real·许可速查散文（学版式不抄、Pro 素材勿交付） | A-通用 | 留本地。这是 CONVENTIONS §5 合规方法论，非易变事实。 |
| themes.py 10 主题 COLORS/FONTS | A-通用 | 留本地。已 selftest 的设计常量，是 light-slides 取色 SSOT，不动。 |
| 核验日期/curl 实测段（resources_real 头部 2026-06-06 大段） | C-状态 | 留本地但瘦身。改为指向实时脚本的 last_checked 字段，不再在正文堆砌一次性实测快照。 |

## B 类转实时设计
新建 light-slides/scripts/resource_signal.py（与 db06 同消费方，复用 venue_signal.py 范式：urllib.request + UA、每信号独立 try/except 降级、--selftest 走 MockFetcher 不打网）。查三类信号：(1) 星标=GET https://api.github.com/repos/{owner}/{repo} 取 stargazers_count；(2) 许可=同响应的 license.spdx_id，PyPI 包走 GET https://pypi.org/pypi/{pkg}/json 取 info.license + classifiers（这两个端点 db03 cards_frontier.md 与本库头部已实测用过，可信）；(3) 链接存活=curl -sI 取 HTTP 状态（403 标注'反爬非失效'）。薄缓存：每条资源在 resources_real 存 {快照值, last_checked_date(YYYY-MM-DD), source_pointer=API URL}。冲突默认信在线，并把新值回写快照+更新 last_checked。无网降级：脚本任一查失败→该条 status=unavailable+reason，回退展示本地快照值并打 staleness 警告（"缓存于 X，未能在线核"），绝不崩、不编数——与 venue_signal 完全一致。GitHub API 未认证 60次/小时，本库仅 ~8 个开源仓，单轮够用；要更高频再标"待核实 API 限流"。

## 偏科隔离设计
db06 偏科极少（主要是 README 风格速查里的「农业主题/医学主题」学科色偏好，以及开题/课程卡的具体 hex）。隔离手段：在相关 slide_card 的 reuse_template_notes 末尾加一行轻量注释 `# domain_scope: 农业|医学|通用`（注释行不进 12 字段 schema，不触发 check_databases 强校验）。light-slides 在第 3 步'按主题从 db06 选风格'时，按项目 domain 过滤——通用卡默认全可用，带 domain_scope 的卡仅在匹配方向时优先推。不新增 schema 字段（见 schema_changes 的决策约束）。绝大多数版式方法卡是学科无关的，无需打标。

## A-通用判断 → 方法论层
A-通用判断本就是本库主体，无需外迁，做法是"原地标准化 + 去事实化"：把 17 张卡里的纯方法论（action-title、幽灵 deck 测试、data-ink、分步揭示降认知负荷、控时公式、exhibit 纪律）保持在 slide_card/slide_pattern_cards，并与 light-slides SKILL.md「学术报告专项」节去重——SKILL 已重复写了 action-title/ghost-deck/三色克制，应让 SKILL 引用 db06 卡为 SSOT，避免两处方法论漂移（light-consistency 关注点）。themes.py 作为'配色方法论的可执行实例'继续承载设计常量。

## schema 改动
不动 12 字段统一 schema（scenario…reuse_template_notes 被 check_databases.py SCHEMAS['db06-ppt-styles'] 与 CONVENTIONS §3 双重硬锁，新增字段需改校验器，风险大于收益）。新增内容全部走'非 schema'载体：(1) domain_scope 作 reuse_template_notes 内注释行；(2) 薄缓存的 last_checked/source_pointer/快照值写在 resources_real 资源表的列内文本（表不是 YAML 卡，不受 SCHEMAS 校验）。若未来确需结构化 domain_scope，应作为 db06 README 提案统一改 db05/db06/db07 三库（同受 is_schema_card_file 管辖），不单独动 db06。

## 影响的技能及改法
- **light-slides**：主消费方。当前在'先定三件事·视觉风格'引 db06 选风格、引 themes.py 取色，工具选型引 resources_real——目前是'信本地卡'。改为：版式/风格仍信本地方法卡；工具星标/许可/链接改为调新建 scripts/resource_signal.py 实时核，README/SKILL 不再承诺本地星标数值准确。SKILL 与 references.md 里重复的 API 端点（GitHub/PyPI/curl）收敛到脚本，文档只留指针。
- **light-slides/references.md**：已逐工具记了 Canva/Gamma 等端点；把'星标/许可实测值'从散文挪进 resource_signal.py 的缓存数据，references 只留'方法+端点'不留会过期的数值快照。
- **light-memory-pm / light-orchestrator**：二者在'版本与风格登记 db06/db09'引用本库。卡数缩水（README 卖点从15资源→17方法卡+实时指针）后，更新台账描述，避免按旧卖点数汇报。
- **light-consistency**：新增一条'db06 方法论为 SSOT，light-slides SKILL 的 action-title/三色等表述须引用而非各写一份'的一致性检查点。

## 迁移步骤
- 1. 新建 light-slides/scripts/resource_signal.py：复用 venue_signal.py 骨架，实现 github_repo(owner,repo)→stars+spdx、pypi_pkg(name)→license、link_status(url)→http_code 三函数 + assemble + --selftest（MockFetcher 覆盖三路径+降级），不打真实网过 selftest。
- 2. 改 resources_real.md 资源表：每个开源行（Marp/reveal.js/PptxGenJS/python-pptx/mtheme/moloch）许可与星标列改为 `值(last_checked=2026-06-06, src=API URL)` 薄缓存格式；闭源站（Canva/Slidesgo…）HTTP 状态同样格式。头部大段'本轮 curl 实测'压缩为一句'实时核见 resource_signal.py'。
- 3. resources_real.md 内嵌 7 张 slide_card 与 slide_pattern_cards.md 10 张：保持 12 字段不动（check_databases 会强校验）；对 color_palette 硬编码 hex 的卡，reuse_template_notes 注明'取色以 themes.py 为准'；对学科色卡加 `# domain_scope:` 注释行。
- 4. 改 README.md：卖点诚实改写（17 张版式方法卡精养 + 资源星标/许可/链接实时核，不再宣称本地实测值长期有效）；'真实资源文件'节加 resource_signal.py 链接与用法。
- 5. 改 light-slides SKILL.md + references.md：工具选型处加'星标/许可/链接见 scripts/resource_signal.py 实时核'；删除与 db06 重复的方法论散文，改为引用 db06 卡。
- 6. 跑 PYTHONUTF8=1 python .github/scripts/check_databases.py 确认 db06 schema 全绿（12 字段+scenario 唯一性未被破坏），跑 resource_signal.py --selftest 绿，跑 check_freshness.py 确认 last_checked 被识别。
- 7. 更新 light-memory-pm/light-orchestrator 台账对 db06 卖点的描述。

## ⚠ 需要你拍板的决策点
- domain_scope 用注释行还是进 schema？db06 的 12 字段被 check_databases.py + CONVENTIONS §3 硬锁，加字段会改全库校验逻辑且破坏 scenario 唯一性外的契约。建议用 reuse_template_notes 内的 `# domain_scope:` 注释行隔离（零 schema 风险）——需你确认接受'注释级隔离'而非'字段级隔离'。
- resource_signal.py 放哪？放 light-slides/scripts/（贴近唯一消费方，复用其 Python 环境）还是 db06 自带 scripts/（db06 当前无 scripts 目录，与 db01 的 venue_signal 在 skill 侧不一致）。建议前者。
- 薄缓存存不存数值？合规敏感的'许可列'（metropolis=CC-BY-SA-4.0 是红线）建议存快照值+last_checked 以便离线可追溯；而'星标'这种纯参考值可只存指针、不存易过期数字。需你拍板是否对两类区别对待。
- 转实时是否强制联网？light-slides 多在无网/沙箱跑 python-pptx。建议默认用本地快照，仅在用户要'正式核对许可/选工具'时才联网核——不强制。
- README 卖点缩水的口径：直接写'资源实测值已转实时核、本地不保证长期有效'是否可接受（诚实但弱化卖点），还是保留'核验于 2026-06-06'的历史快照作背书。

## 工作量与风险
- 工作量：中。新建一个 ~250 行脚本（venue_signal.py 已有完整可抄范式，含 selftest）+ 改 4 个 md 的表格/散文 + 改 light-slides 两文件去重。无 schema 变更、无 CI 校验器改动是省力点；薄缓存格式要逐条资源手改是主要工作量。
- 风险：(1) README 卖点卡数/实测数值缩水，对外观感变弱——需 light-memory-pm 同步、避免别处仍按旧数宣传。(2) 联网依赖加重：GitHub API 未认证限 60/h、PyPI/curl 在沙箱可能被拦（本库头部已记 Canva/Gamma curl 403/000），脚本须像 venue_signal 一样优雅降级回快照，否则离线出稿被阻断。(3) 方法论去重时若 light-slides SKILL 的 action-title 等表述与 db06 卡产生分叉，反而制造不一致——必须确立 db06 为 SSOT 并让 SKILL 引用。(4) domain_scope 用注释行=弱隔离，过滤逻辑在 light-slides 侧靠约定实现，无校验兜底，可能被后续维护忽略。
