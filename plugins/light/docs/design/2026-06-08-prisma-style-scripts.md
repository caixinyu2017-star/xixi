# PRISMA 与文风校准：做成可执行脚本而非纯文档

**日期**：2026-06-08
**影响范围**：light-literature-search、light-paper-polishing、light-memory-pm 协作

## 背景

调研 ARS 后补齐最后两项差距：#8 系统综述（PRISMA）、#9 文风校准（对应 ARS 的 Style Calibration）。这两项 Light 此前都有"理念层"的影子——literature-search 提过"PRISMA 思想留痕"，polishing 有 mechanical_check 抓 AI 腔——但都停在文字描述，没有可操作、可复现的落地。

## 决策

两项都**做成带自测的可执行脚本**，而非又写一篇 references 文档：

- **#8 `prisma_flow.py`**：输入综述各阶段计数，机械核对勾稽关系（前阶段−排除=后阶段），抓出"凭空消失/多出"的算术错误，产出 PRISMA 2020 流程图结构化数据。
- **#9 `style_fingerprint.py`**：从用户过往文稿量出个人文风指纹（句长/被动/第一人称/连接词/标点/高频词），润色时校准到作者声音而非通用模板。

两脚本都**只做机械可验证的部分，不替人做判断**：prisma_flow 核对计数自洽但不评判筛选决定；style_fingerprint 画像但不自动改写。

## 理由

PRISMA 计数勾稽、文风指纹统计，本质都是**可量化、可自测、易错且审稿人会查**的机械工作——正是脚本的强项，也符合 Light "脚本管机械验证、人管判断"的一贯分工。做成文档只能提醒"要注意"，做成脚本能当场算出对不对、能进 pipeline 当闸门。

边界同上一篇 [orchestrator-tiered](2026-06-08-orchestrator-tiered.md) 的复核原则：把诚实底线工程化（计数必须勾稽、文风别被抹平），但不越界替研究者做学术判断。ARS 的 Style Calibration 我们只取"量化个人文风、校准而非抹平"这一核心思路，用 Light 自己的特征集和实现重写。

## 复核问题

下次再补一项"借鉴来的能力"时，先问：

> **这件事的可验证部分能不能做成带自测的脚本？**

能（计数、统计、格式、勾稽）→ 优先脚本，比文档更硬、能进 pipeline。
不能（需要领域判断、价值取舍）→ 做成 references 流程文档，明确标注"脚本不替人判断"的边界。
