# R4.9 灰色文献四类源 — 实查留痕

- 研究日期：2026-06-11
- 执行：Claude Opus 4.8（Claude Code）
- 任务：light-literature-search references 增"灰色文献检索路径"节，四类源各一实查示例。

## 1. 标准（全国标准信息公共服务平台）✓ WebSearch 实查
- 目录查询（标准号+状态）：https://std.samr.gov.cn/gb/gbQuery
- 高级检索（多字段组合）：https://std.samr.gov.cn/gb/search/gbAdvancedSearch?type=std
- 国标全文公开（在线读强制性+部分推荐性国标）：https://openstd.samr.gov.cn/bzgk/gb/indexgf
- 结果列表标注状态字段：现行/即将实施/已废止/被代替。引用标准必须核对**现行/废止状态**与代替关系。
- 行标/地标/团标在 sacinfo（https://std.sacinfo.org.cn/home/query）。

## 2. 政策（国务院/部委文件库）✓ WebSearch 实查
- 国务院政策文件库：https://sousuo.www.gov.cn/zcwjk/ ；检索接口 `policyDocumentLibrary?q=<关键词>&t=zhengcelibrary`（支持 q 关键词 + t 类型参数）。
- 中国政府网政府文件检索：https://www.gov.cn/zfwj/search.htm ；国务院公报高级检索：https://www.gov.cn/search/gbsousuo.htm
- 部委自建文件库（例：发改委 https://www.ndrc.gov.cn/xxgk/wjk/ 按年份）。
- 注意：权威域名是 `sousuo.www.gov.cn`（政府网搜索子站）；部委文件两条路径——国务院库统一检索 或 各部委自建栏目。引用须核发文字号、成文日期、是否现行有效。

## 3. 行业报告（咨询机构）✓ WebSearch 实查
- 一手机构（可信度最高，方法论透明）：IDC（完整报告付费，但**新闻稿/Press Release 含核心数据摘要免费**，如 my.idc.com getdoc）、Gartner（gartner.com/cn/publications 公开摘要+部分免费）、信通院（公开白皮书）。
- 本土咨询（中国细分市场丰富，免费多）：艾瑞 report.iresearch.cn、36氪研究院 pitchhub.36kr.com/research。
- 第三方聚合（水滴研报/发现报告）属典型灰色文献，**须回溯原始发布方核实**，不直接引二手版。
- 可信度警示：行业报告非同行评审，数据口径/样本说明常不透明；引用优先标原始机构+报告发布日期，机构报告 > 本土咨询 > 聚合平台。

## 4. 竞赛方案（Kaggle/天池）✓ WebSearch 实查
- Kaggle：竞赛 Discussion 区获奖者 writeup + Code/Notebooks 区开源方案；聚合索引站 farid.one/kaggle-solutions/（按竞赛检索历届方案）；GitHub 合集 apachecn/awesome-data-comp-solution。
- 天池：技术圈论坛 tianchi.aliyun.com/forum 赛后方案分享帖。
- 检索法：按"竞赛名 + solution/writeup/方案/top"检索 Discussion 区与技术博客；金牌方案常附 GitHub 复现仓库。
- 可信度警示：竞赛方案是工程 trick 富矿但**非学术同行评审**，过拟合 leaderboard、缺理论论证常见；借鉴方法不等于可直接写进论文当 SOTA，须复现验证 + 回学术文献找理论支撑。

## 共性
四类源都是灰色文献（非正式出版/非同行评审），价值在补学术库盲区（标准/政策/产业动态/工程实践），但引用须：① 标原始来源+日期；② 核现行有效性（标准/政策尤甚）；③ 不当同行评审证据，关键结论回学术源交叉验证。
