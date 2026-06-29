# R9 批2 · db01 新卡来源抽查留痕

- 核验日期：2026-06-12
- 数据源：OpenAlex Sources API（`api.openalex.org/sources?filter=issn:<ISSN>`）
- 本批新增：104 张 venue 卡（db01 204 → 308），方向命中农业工程/智慧农业/精准畜牧/奶业/兽医、CV/AI/ML、医学影像与临床肿瘤、生信、机器人/语音、统计、环境/食品/材料/能源/地学、HCI。

## 抽查方法

对本批 104 张新卡（`source=openalex` 且 `risk_note` 含"真实ISSN查询"）按步长均匀采样 **22 张（21%，≥20% 达标）**，
按卡内记录的 ISSN 回查 OpenAlex，比对 `works_count` 与 `h_index`：
- works_count 允许 ±5%/±50 偏差（OpenAlex 收录持续增长，正常浮动）；
- h_index 允许 ±3 偏差。

## 结果：22/22 全部一致

| venue | ISSN | 卡内 works/h | 线上核验 |
|---|---|---|---|
| Journal of the Science of Food and Agriculture | 0022-5142 | 25325/237 | OK |
| Journal of Integrative Agriculture | 2095-3119 | 4759/106 | OK |
| Trends in Food Science & Technology | 0924-2244 | 7977/333 | OK |
| Computer Vision and Image Understanding | 1077-3142 | 4270/173 | OK |
| Pattern Recognition Letters | 0167-8655 | 9745/220 | OK |
| Journal of Clinical Oncology | 0732-183X | 173706/736 | OK |
| Molecular Plant | 1674-2052 | 3113/227 | OK |
| Field Crops Research | 0378-4290 | 8530/247 | OK |
| Environmental Modelling & Software | 1364-8152 | 5905/210 | OK |
| Genomics | 0888-7543 | 11377/218 | OK |
| Robotics and Autonomous Systems | 0921-8890 | 5378/175 | OK |
| IEEE/ACM Trans. Computational Biology & Bioinformatics | 1545-5963 | 3574/112 | OK |
| Journal of Neurology Neurosurgery & Psychiatry | 0022-3050 | 29703/337 | OK |
| Cancer | 0008-543X | 53322/473 | OK |
| British Journal of Anaesthesia | 0007-0912 | 30089/288 | OK |
| Information Processing & Management | 0306-4573 | 6598/186 | OK |
| Carbon | 0008-6223 | 30604/385 | OK |
| IEEE Trans. Network and Service Management | 1932-4537 | 3320/101 | OK |
| ACM Trans. Software Engineering and Methodology | 1049-331X | 1843/118 | OK |
| Journal of Veterinary Internal Medicine | 0891-6640 | 8525/156 | OK |
| Deep Sea Research Part II | 0967-0645 | 5402/194 | OK |
| The Annals of Statistics | 0090-5364 | 6370/321 | OK |

## 采集质量纪律（本批落地）

- **不盲取 search 第一条**：所有数值按精确 ISSN 回查，命中唯一源；多结果时按 issn_l 精确匹配。
- **碎片记录剔除**：works_count<50 的 OpenAlex 碎片/会议年度拆分记录一律剔除（如误命中的 CVPR proceedings works=1 记录已删）。
- **去重双保险**：对照现有 204 卡的 venue_name（小写）与全部 ISSN（含 risk_note 内 ISSN）双重去重，杜绝重名/同刊重复。
- **impact_factor 口径诚实**：列内写 OpenAlex 2yr 均被引并注明"非 JCR IF"；精确 JCR IF/分区标"待核(LetPub/JCR 付费源)"，2yr=0 的标"未公开"，零 N/A 留白。
- **代表作真实**：20 张核心域卡的 representative_papers 取该刊 OpenAlex 被引前 2 works（真实 cited_by_count），如 IJCV→SIFT(被引55201)、Frontiers Plant Sci→植物病害深度学习(被引4534)。

## ai_policy 实查留痕（出版社级，2026-06）

186 张卡有 `ai_policy=` 值（目标 ≥50）。其中 12 张为 R4 期单独实查（CVPR/NeurIPS/ICML/ICLR/TPAMI/Nature/Science/Cell 等），
本批新增 174 张按**出版社官方政策页实查**后批量标注（同社旗下期刊共用该社政策）：

| 出版社 | 卡数 | 官方政策页（实查 2026-06） | 核心口径 |
|---|---|---|---|
| Elsevier | 85 | elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals | AI 声明置参考文献前；AI 不署名；原始数据图禁 AI |
| IEEE | 28 | journals.ieeeauthorcenter.ieee.org（submission-and-peer-review-policies） | 致谢披露+标 AI 系统与章节；含图/码；审稿人禁投喂公共 AI |
| Wiley | 18 | authors.wiley.com/ethics-guidelines | 投稿披露+正文说明；AI 不署名；禁创建篡改数据/可视化 |
| Springer | 17 | springer.com/editorial-policies/artificial-intelligence | 方法学记录；LLM 不署名；生成式 AI 图像原则禁止(三类标注例外) |
| Nature | 10 | nature.com/nature-portfolio/editorial-policies/ai | 方法学记录；LLM 不署名；AI 生成图像原则不允许 |
| ACM | 16 | acm.org/publications/policies + ACM Policy on Authorship | 致谢披露；AI 不署名(遵 COPE) |

> 注：出版社级政策为"同社旗下期刊共用"口径，个别期刊可能有更严附加条款；投稿前仍须看目标刊 Author Guidelines。
> Nature/Springer 政策页对未登录访问有 303 跳转/付费墙，确切措辞经官方页镜像 + 多源核实，立场口径一致。
