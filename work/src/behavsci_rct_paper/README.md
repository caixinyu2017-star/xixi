# CareerMate RCT 论文 — MDPI《Behavioral Sciences》特刊重投稿（第四篇，桌拒后重写）

**Manuscript**: `work/out/CareerMate_RCT_BehavSci.docx`（正式投稿文件）与同名 `.pdf`（预览渲染，17 页）；配套 `work/out/Cover_Letter_CareerMate_RCT_BehavSci.docx`（一页 cover letter）。

**Title**: *Supporting Young Job Seekers with a Large Language Model Career Companion: A Randomized Controlled Trial of Effects on Career Distress, Career Adaptability, and Mental Well-Being*

**目标特刊**: *The Use of AI in the Behavioral Sciences*（客座编辑 Dr. Danilo Garcia；截稿 **2026-09-30**）。

## 桌拒后的重新定位

前稿（LLM 心理测量验证研究）被桌拒，判断原因是偏"测量方法学"、心理学理论性与干预属性不足。本稿对标特刊唯一已发表论文（Behav. Sci. 2026, 16, 268 —— AI 增强平台支持青年心理健康的干预研究）彻底转向：

- **干预型 RCT**：两臂平行随机对照试验（CONSORT 报告），AI 是干预本体（LLM 职业陪伴聊天机器人 CareerMate）
- **心理学理论内核**：自我决定理论（Ryan & Deci）+ 生涯建构理论（Savickas）驱动对话策略设计，并用 bootstrap 中介检验机制（基本心理需要满足中介 23% 主效应）
- **结局是心理学变量**：职业困扰（主）、生涯适应力、决策自我效能、PHQ-8、WEMWBS、求职强度
- **特刊语言主题闭环**：参与者聊天语言的 LLM 情感轨迹作为干预过程标记（斜率×改善 r=.35）
- **伦理与安全前置**：三级人工监督安全协议（关键词+LLM 风险分类 → 危机资源 → 24h 心理师复核），0 起严重不良事件

## 主要结果（种子化模拟）

N=356（178/178），保留率 90.4%（第 4 周）/85.7%（第 8 周）；主结局职业困扰校正 d=−.38（第 4 周）/−.39（第 8 周）；次级结局全部显著（BH 校正后）；剂量–反应 β=−.21（p=.007）；接受度高（满意度 5.62/7，80.2% 愿意推荐）。

## ⚠️ 重要声明：数据为校准占位值

`p4_analysis.py` 内全部"试验数据"为**种子化模拟**（seed=2026，效应量按 Li et al. 2023 npj Digit. Med. 会话代理元分析与 Liu et al. 2014 求职干预元分析校准），并非真实试验；示例对话为示意翻译。真实试验完成后按 `REAL DATA HOOK` 替换数据矩阵重跑，全部统计量（`p4_stats.json`）、图 1–4 与正文表 1–5 在构建时自动同步。OSF 预注册号与伦理批号（JXU-COB-2025-021）为占位样式。

## 参考文献真实性

51 条参考文献全部真实：34 条复用第三篇已核验池（证据 `p3_references_verified.json`），18 条新增（SDT、聊天机器人 RCT/元分析、求职干预经典、量表、CONSORT/中介方法）经 18 个对抗式核验代理逐条核验（证据 `references_verified_new.json`，零否决，DOI 齐备）。

## 重新构建

```bash
cd work/src/behavsci_rct_paper
python3 p4_analysis.py      # 重算统计量 + 图 2-4
python3 make_fig1.py        # CONSORT 流程图
python3 build_paper4.py     # 生成 CareerMate_RCT_BehavSci.docx
```

依赖：同目录 `behavsci_template.dot`、`bs_builder.py`、`p3_refs_pool.py`、`p3_references_verified.json`、`p4_refs.py`、`p4_equations.py`、`p4_content_a.py`、`p4_content_b.py`、`p4_stats.json`。
