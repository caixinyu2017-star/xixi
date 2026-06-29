# db02 — 论文写作套路与句式库

> db02 的方法论补充。db02 主库（`writing_cards.md`）存「结构化样本卡」训练判断力；本库存**可直接复用的写作骨架、句式模板、审稿人偏好表达与措辞红线**，供 m07(写作)/m08(润色)/m14(审稿模拟) 直接调用。
> 句式均为领域无关骨架，套用时替换占位符 `<...>`，**不照抄任何原文**。
> 与本库互补：[samples_real.md](samples_real.md) 文末「跨样本归纳 A/B/C/D 表」是从 16 篇真实论文**实证归纳**的速查表（带范本名锚点）；本库是**抽象句式模板**。两者视角不同、不重复维护——要范本对照查 samples_real，要可填空骨架查本库。**D 背书清单有偏科前提**（竞赛/SOTA/开源仅 cs.AI/CV 有效），非 CS 方向只用通用项，详见 samples_real D 表。

## 总纲：四条公认底层逻辑

1. **先讲故事，再填细节**（Simon Peyton Jones）：论文是为了传达一个 idea，不是流水账。一篇文章只讲清一个核心贡献。
2. **OCAR / 倒金字塔**（Whitesides；PLOS Ten Simple Rules）：每一层（全文→章节→段落）都遵循「语境 Context → 内容 Content → 结论 Conclusion」，读者随时知道"现在讲什么、为什么"。
3. **段落首句负责导航**：每段第一句（topic sentence）应能被单独抽出，串起来即全文提纲。
4. **少即是多 + 主动语态 + 强动词**：删掉不承载信息的词；用 "We show" 而非 "It is shown that"。

来源：[How to Write a Great Research Paper — S. Peyton Jones (Microsoft Research)](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/)；[Whitesides' Group: Writing a Paper, Adv. Mater. 2004, DOI:10.1002/adma.200400767](https://doi.org/10.1002/adma.200400767)（OpenAlex 实测被引 124）；[Ten Simple Rules for Structuring Papers, PLOS Comput Biol 2017, DOI:10.1371/journal.pcbi.1005619](https://doi.org/10.1371/journal.pcbi.1005619)（OpenAlex 实测被引 79）。

---

## 1. 标题 (Title)

**套路**
- `方法名: 一句话能力/任务描述` —— `<MethodName>: <Doing X> for <Task Y>`
- 动词开头陈述能力 —— `Learning to <X> via <Y>` / `Rethinking <X> for <Y>`
- 问句式（慎用，适合立场/综述）—— `Do <models> really <X>?`
- **红线**：避免空泛开头 "A Study on / Towards / Some Notes on"；标题里别堆 novel/efficient 等形容词，让结果说话。

**可复用句式**
- `<MethodName>: <Adjective-free verb phrase> for <task>`
- `<Task>-aware <Architecture> for <Goal>`

## 2. 摘要 (Abstract) —— 5 句倒金字塔

| 句位 | 功能 | 句式骨架 |
|---|---|---|
| ① 背景 | 一句点题 | `<Field/task> is central to <goal>; recent <approaches> have <progress>.` |
| ② 问题/gap | 痛点 | `However, existing methods <fail to / overlook / require> <X>, which <consequence>.` |
| ③ 本文 | 一句话方法 | `We present <Method>, which <key idea in one clause>.` |
| ④ 结果 | 带数字 | `On <benchmarks>, <Method> improves <metric> by <N> (from A to B) over <baseline>.` |
| ⑤ 意义 | 影响/开源 | `Our results suggest <implication>; code and data are available at <url>.` |

- 摘要不引用文献、不放公式、不留缩写未展开。编辑视角：前两句决定是否继续读。
- 来源：[Nature Index — How to write an abstract that stands out](https://www.nature.com/nature-index/news/how-to-write-good-abstract-scientific-research-paper)；[MIT CommLab — Journal Article: Abstract](https://mitcommlab.mit.edu/broad/commkit/journal-article-abstract/)；[How to write a good abstract, PMC3136027](https://pmc.ncbi.nlm.nih.gov/articles/PMC3136027/)。

## 3. 引言 (Introduction) —— problem→gap→contribution

**五段式骨架**（每段首句即 topic sentence）：
1. **重要性**：`<Problem> matters because <high-level impact>.`
2. **现状**：`To address this, prior work has <line A> [refs] and <line B> [refs].`
3. **gap（转折，最关键）**：`Despite this progress, <specific limitation> remains unsolved, because <root cause>.`
4. **本文做法 + 关键洞见**：`In this paper, we <do X>. Our key insight is that <insight>.`
5. **贡献清单 + 结果预告**：bullet 3 条 + 一句主要数字。

**贡献 bullet 句式**
- `We identify/formalize <problem>, showing that <observation>.`
- `We propose <Method>, which <mechanism>.`
- `We demonstrate on <N benchmarks> that <Method> achieves <result>, with extensive ablations isolating <component>.`

来源：[Peyton Jones — Great Research Paper](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/)（"State your contributions" 与 "the money is in the introduction"）；[USC Libraries — Research Writing Guide](https://libguides.usc.edu/writingguide)。

## 4. 相关工作 (Related Work)

**套路**：按方法族/任务分 2–4 类（taxonomy），**不要编年体流水账**。每类先 1–2 句综述，再用一句明确"与本文的差异"。
- 类目导航句：`Work on <topic> falls into two lines: <A> and <B>.`
- 综述句：`<Line A> methods [refs] <do X>, achieving <strength>.`
- **差异句（最重要，决定定位）**：`Unlike these, our method <key difference>; we are the first to <claim> in the setting of <scope>.`（first/the only 必须站得住，限定 scope）
- 礼貌句（避免树敌）：`While effective, these approaches <limitation>, which our work directly addresses.`
- 红线：不要贬低被引工作（审稿人可能就是作者）；用"未覆盖/正交/互补"而非"错误/失败"。

## 5. 方法 (Method)

**叙事顺序**：直觉/动机 → 问题形式化(符号定义) → 整体框架(配图) → 各模块逐一 → 复杂度/理论性质。
- 概览句：`Figure <n> gives an overview. Given <input>, our method <produces output> in <K> stages.`
- 形式化引入：`We denote <X> as <symbol>. The goal is to learn <f> such that <objective>.`
- 设计选择须给理由：`We choose <design> rather than <alt> because <reason>.`（审稿人最反感"无动机的堆砌"）
- 可复现性：关键超参、损失权重、训练细节要么在此要么在附录明确指向。

来源：[Peyton Jones](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/)（"Explain it as if to a friend"，先讲直觉）。

## 6. 实验 (Experiments)

**标准小节顺序**：① Setup（数据集/baselines/指标/实现细节/算力） → ② Main Results（主表+一段解读） → ③ Ablation（逐组件） → ④ Analysis（敏感性/收敛/复杂度/规模） → ⑤ Qualitative（可视化/case） → ⑥（可选）Failure cases。

**句式**
- 提出研究问题驱动实验：`Our experiments answer: (Q1) Does <Method> outperform <baselines>? (Q2) Which component matters? (Q3) Does it scale?`
- 解读主表（先结论后数字）：`<Method> consistently outperforms all baselines, improving <metric> by <N> on <dataset> (Table <k>).`
- 消融定位贡献来源：`Removing <component> drops <metric> by <N>, confirming its contribution.`
- 公平性声明（堵审稿人嘴）：`For fair comparison, all methods use the same <backbone/data/budget> and are tuned with equal effort.`
- 统计显著：`Results are averaged over <K> seeds; improvements are significant (p < 0.05, paired t-test).`（用了 significant 就必须有检验，见红线）

来源：[USC Libraries](https://libguides.usc.edu/writingguide)；[PLOS — Best practices in research reporting](https://journals.plos.org/ploscompbiol/s/best-practices-in-research-reporting)。

## 7. 讨论 (Discussion)

**功能**：把结果上升为洞见，回应引言提出的问题，而非复述实验数字。
- 回扣引言：`Returning to the question raised in Section 1, our results show that <answer>.`
- 解释为何有效（机制）：`We attribute this gain to <mechanism>, supported by <evidence in 6.x>.`
- 解释反常结果（诚实加分）：`Contrary to expectation, <observation>; we hypothesize this is due to <reason>.`
- 与已有结论对话：`This aligns with / contradicts <prior finding> [ref], suggesting <implication>.`
- 红线：区分"相关"与"因果"；解释性陈述用 hedging（suggest/may indicate），别下死结论。

## 8. 结论 (Conclusion)

**套路**：一句复述贡献 + 一句核心发现意义 + 一句未来工作。不引入新结果、不堆形容词。
- `We presented <Method>, which <one-line contribution>. Experiments on <benchmarks> show <key result>. <Method> opens <direction> for future work on <X>.`

## 9. 局限 (Limitations)

**主动承认 2–3 条真实局限 + 对应未来工作**，降低审稿人攻击面（部分会场如 *ACL 已强制要求*，且不计入页数）。
- 范围：`Our evaluation is limited to <scope>; generalization to <other setting> remains untested.`
- 假设：`Our method assumes <assumption>, which may not hold when <condition>.`
- 成本：`<Method> incurs <overhead>; reducing this is left to future work.`
- 红线：写"无明显局限"= 自杀；但也别写到伤及核心贡献（如"我们的主结论可能不成立"）。

来源：[ACL Rolling Review 官方站点](https://aclrollingreview.org)（ARR/ACL 自 2023 起强制 Limitations 小节、不计入页数；具体条款页 URL 待核查）；[PLOS Reviewer Guidelines](https://journals.plos.org/ploscompbiol/s/reviewer-guidelines)。

---

## 10. 审稿人偏好的表达 (Reviewer-friendly phrasing)

审稿人喜欢「可验证、有节制、替读者着想」的表达。逐项可操作：

| 场景 | 别这么写 | 改成 |
|---|---|---|
| 声明贡献 | "We propose a novel framework." | "We propose <Method>; to our knowledge it is the first to <X> under <scope>." |
| 报告提升 | "significantly improves performance" | "improves <metric> by 3.2 points (p<0.05, 5 seeds)" |
| 比较 | "much better than baselines" | "outperforms the strongest baseline <B> on 4/5 datasets" |
| 解释 | "obviously / clearly" | "as shown in Table 3 / Figure 4" |
| 推测 | "This proves that..." | "This suggests / is consistent with..." |
| 未来 | "In future we will solve everything." | "A natural next step is <specific extension>." |

- 替读者降负担：每张图表自含 caption（看 caption 即懂）；首次出现的缩写展开；符号集中定义。
- 主动语态 + 短句：删 "It should be noted that / In order to / due to the fact that"。
- 来源：[Paperpal — Hedging in Academic Writing](https://paperpal.com/blog/academic-writing-guides/what-is-hedging-in-academic-writing)；[NPS Graduate Writing Center — Clarity](https://nps.edu/web/gwc/clarity)；[CERN — Words to avoid](https://test-writing-guidelines.web.cern.ch/test-writing-guidelines/entries/words-avoid-web-texts.html)。

## 11. 常见 reviewer 追问清单（预演用，喂 m14）

**定位 / 新意**
- 你的创新点和最接近的工作 X 到底差在哪？只是组合已有模块吗？
- "first/novel" 的声明有何依据？是否遗漏了相关工作 Y？

**实验严谨**
- 对比是否公平（同数据/同算力/同 backbone/同调参预算）？
- 提升是否统计显著（多种子 + 检验）？误差棒在哪？
- 消融能否证明提升来自所声称的组件，而非超参/数据？
- baseline 是否用了其原文最佳配置，还是被你弱化了？

**泛化 / 代价**
- 在更大规模 / 真实分布 / 跨域上能否泛化？
- 计算与内存开销如何？相对收益是否值得？
- 对超参/随机性的敏感度？最坏情况表现？

**清晰 / 可复现**
- 关键细节是否足以复现？是否开源？
- 图表是否支持文中结论？有无 cherry-picking？

**写作策略**：rebuttal 时按"先承认→给证据→给新实验/数字"回应，逐条编号对应。

来源：[NeurIPS 公开审稿样例（OpenReview/proceedings）](https://proceedings.neurips.cc/)；[Peyton Jones — 关于 reviewer 视角](https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/)。

## 12. 措辞红线汇总（写作/润色共用）

**慎用词 → 使用条件**
- `novel / new`：只在确有明确差异且 related work 已论证时，且最好限定 scope。
- `significantly`：仅当做了显著性检验；否则用 "substantially/markedly" 或直接给数字。
- `state-of-the-art / SOTA`：需在公平设置下、注明截至日期与对比范围。
- `first / the only`：限定 setting，禁止裸用全称量化。
- `obviously / clearly / trivially`：删除或换成指向证据。
- `prove / demonstrate (强因果)`：实证结论用 "show/suggest/indicate"，"prove" 留给数学证明。
- `outperform/beat` 配空话："much/far better" → 给具体差值。
- 填充词：`very, really, quite, in order to, due to the fact that, it is worth noting` → 删。

**结构红线**
- 一篇只讲一个核心 idea；摘要不放引用/公式；结论不引入新结果；related work 不贬低被引方。

来源：[CERN — Words to avoid](https://test-writing-guidelines.web.cern.ch/test-writing-guidelines/entries/words-avoid-web-texts.html)；[Paperpal — Hedging](https://paperpal.com/blog/academic-writing-guides/what-is-hedging-in-academic-writing)；[USC Libraries — Academic Writing Style](https://libguides.usc.edu/writingguide)。

---

## 附：权威写作指南索引（均经检索/curl 佐证）

| 指南 | 链接 | 核查状态 |
|---|---|---|
| S. Peyton Jones, *How to Write a Great Research Paper* | https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/ | WebSearch 命中（MSR 官方专题页） |
| Whitesides, *Writing a Paper*, Adv. Mater. 2004 | https://doi.org/10.1002/adma.200400767 | OpenAlex 实测：被引 124，year 2004 ✔ |
| Mensh & Kording, *Ten Simple Rules for Structuring Papers*, PLOS Comp Biol 2017 | https://doi.org/10.1371/journal.pcbi.1005619 | OpenAlex 实测：被引 79，year 2017 ✔ |
| Nature Index — How to write an abstract that stands out | https://www.nature.com/nature-index/news/how-to-write-good-abstract-scientific-research-paper | WebSearch 命中 |
| MIT CommLab — Journal Article: Abstract | https://mitcommlab.mit.edu/broad/commkit/journal-article-abstract/ | WebSearch 命中 |
| How to write a good abstract (PMC3136027) | https://pmc.ncbi.nlm.nih.gov/articles/PMC3136027/ | WebSearch 命中 |
| ACL Rolling Review（强制 Limitations） | https://aclrollingreview.org | WebSearch 命中；具体条款页 URL 待核查 |
| PLOS Reviewer Guidelines / Best practices | https://journals.plos.org/ploscompbiol/s/reviewer-guidelines | WebSearch 命中 |
| CERN — Words to avoid | https://test-writing-guidelines.web.cern.ch/test-writing-guidelines/entries/words-avoid-web-texts.html | WebSearch 命中 |
| Paperpal — Hedging in Academic Writing | https://paperpal.com/blog/academic-writing-guides/what-is-hedging-in-academic-writing | WebSearch 命中 |
| USC Libraries — Organizing Your Research Writing | https://libguides.usc.edu/writingguide | WebSearch 命中 |

> **诚实声明**：本文件为方法论模板，不含可核查数值型断言（ISSN/被引/DOI 除外）。两条核心参考文献的 DOI、被引数、年份经 OpenAlex curl 实测确认（见上表 ✔）。其余指南链接经 WebSearch 命中标题+URL 佐证；ACL Limitations 政策的具体条款页 URL 标注「待核查」，未臆造。



