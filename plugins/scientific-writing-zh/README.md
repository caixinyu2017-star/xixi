<div align="center">

# scientific-writing-zh

**一个 Claude Code skill —— 一份可用的科研写作教练(中文)。**

🇬🇧 English version: [**scientific-writing**](https://github.com/<you>/scientific-writing)

</div>

---

## 这是什么?

一个 [Claude Code](https://claude.com/claude-code) **skill**,
可直接使用的科研写作指导,覆盖写作、修改、评审与报告——**用中文讲解**。

安装后,只要你在写论文、摘要、标题、图、审稿回复或报告,Claude 会**自动**调用它——哪怕你
只是随口说"帮我把这段改紧凑些""这个摘要行不行?"。

> **关于例句:** 本 skill 用中文讲解原则,而 `DRAFT → IMPROVED` 例句**保留英文**——因为
> 中文研究者投的多是英文国际期刊(书中那章"非母语作者指南"正是写给你们的)。结构、连贯、
> 简洁、评审、报告等与语言无关的原则完整适用于中文写作;被动语态、冠词、破折号等英文专有
> 部分,用中文解释清楚"为什么"。

## 覆盖什么

涵盖**完整的科研沟通生命周期**:

- 是否/在哪发表、选目标期刊、校样、论文推广
- 动机、头脑风暴、列提纲、写初稿
- 论文结构——标题、摘要、引言、方法、结果、讨论、结论
- 文字打磨——段落、句子、词语(修改引擎)
- 修改——写作/编辑漏斗、CPR、凝练(précis)
- 图、表、公式与引用
- 署名、作者顺序、抄袭与学术伦理
- 非英语母语作者指南
- 同行评审——写评审意见与回复审稿
- 会议摘要、幻灯片、报告、海报
- 职场、公众/媒体与职业沟通

贯穿全书的核心理念是**写作/编辑漏斗**——从大尺度到小尺度(文档 → 段落 → 句子 →
词语 → 标点)——以及 **CPR** 一遍修改:**简洁(Concision)、精确(Precision)、修订
(Revision)**。

## 怎么构建的

用**渐进披露**:一个精简的 `SKILL.md` 路由,加上按主题分的参考文件,只在匹配任务时才加载。
结构与英文版 [`scientific-writing`](https://github.com/<you>/scientific-writing) 完全一致,
文件名相同,内容为中文。

```
scientific-writing-zh/
├── SKILL.md                         # 路由 + 核心方法
└── references/
    ├── pre-writing.md               # 动机、头脑风暴、提纲、初稿
    ├── publishing-process.md        # 是否发表、选期刊、校样、推广
    ├── paper-structure.md           # 标题、摘要、引言/方法/结果/讨论/结论
    ├── prose-craft.md               # 段落、句子、词语
    ├── revision.md                  # 编辑漏斗、CPR、précis
    ├── figures-citations.md         # 图、表、公式、引用
    ├── authorship-ethics.md         # 署名顺序、抄袭、学术不端
    ├── esl-guidance.md              # 作为非母语者写科研英文
    ├── peer-review.md               # 写评审 + 回复审稿
    ├── presentations.md             # 摘要、幻灯片、报告、海报
    ├── career-communication.md      # 备忘录、CV、邮件、媒体、成长
    └── word-usage.md                # 词表、标点、常被误用的术语
```

## 安装

Claude Code 在 `~/.claude/skills/` 下发现 skill。把本仓库直接克隆进去:

```bash
git clone https://github.com/<你>/scientific-writing-zh.git ~/.claude/skills/scientific-writing-zh
```

然后启动(或重启)Claude Code,运行 `/skills` 确认已列出。仓库根目录的 `README.md`、
`LICENSE`、`.gitignore` 会被 Claude 忽略——只有 `SKILL.md` 和 `references/` 起作用。

## 使用

不用按名字调用。只管写,Claude 会把相关指导拉进来。例如:

- *"帮我把这段改紧凑些,去掉被动语态。"*
- *"这个摘要够具体吗?是不是没超 250 词?"*
- *"帮我回复审稿人 2——他们觉得我们的方法没讲清楚。"*
- *"给这篇稿子写一份同行评审意见。"*
- *"我的引言不连贯——先把结构理顺。"*

本 skill 在中文提问(写论文 / 投稿 / 审稿 / 改这段……)时触发。

## 许可

仓库中的 skill 文件(为本仓库撰写的 Markdown 文字)以 **MIT License** 发布,见
[`LICENSE`](LICENSE)。

## 贡献

欢迎 Issue 和 PR——尤其是更清楚的改写、`SKILL.md` 更好的路由,或修正参考文件偏离原书本意之
处。例句保持简短,署名保持完整。
