# 浙江青年就业论文 — MDPI《Systems》特刊投稿初稿

**Manuscript**: `work/out/Zhejiang_Youth_Employment_Systems.docx`（正式投稿文件）与同名 `.pdf`（预览渲染）。

**Title**: *Industrial Intelligent Transformation and Youth Employment and Career Development: A Regional Socio-Economic Systems Analysis of Zhejiang, China*

对应课题：《浙江青年就业和职业发展困境、成因及解决对策研究》。

---

## 目标特刊（截至 2026-07-11 检索确认）

**首选**：*Socio-Economic System Analysis: Urban, Regional and Industrial Perspectives*
- 截稿：**2026 年 11 月 30 日**（单一检索来源，投稿前请在特刊页面复核）
- 佐证：该特刊 2026 年 7 月仍在发文（如 Systems 14(7):740），确认开放中
- 契合点：区域（浙江）× 产业（智能化转型）× 社会经济系统结果（青年就业）

**备选**：*Economic System Management, Sustainability, and Innovation in Digital Environments*
- 截稿：**2026 年 8 月 31 日**（两个独立检索来源确认）
- 客座编辑：Raquel Ibar-Alonso, Maria-Carmen García-Centeno, Raquel Quiroga-Garcia
- 关键词：数字化转型、创新、大数据、人工智能、可持续、竞争力

其他仍开放的候选（供参考）：*Exploring the Interrelation of HRM and Corporate Performance Using Systems Thinking*（2026-09-30）、*Digital Business Systems for Entrepreneurial Innovation and Strategic Development*（2027-01-31）、*Systems Thinking for Business Strategic Management*（2027-01-20）。

> 注：本环境无法直接访问 mdpi.com（网络策略封锁），特刊信息全部来自搜索引擎摘要的多源交叉验证。投稿前请务必在官网复核截稿日期与征稿范围。

---

## ⚠️ 重要声明：实证数据为占位数值

**正文中所有回归系数、描述性统计、样本量（668 家企业 / 6,124 观测）均为按文献合理量级构造的占位数值，并非真实估计结果。** 投稿前必须：

1. 以 CSMAR + IFR + 城市统计年鉴构建真实的浙江上市公司面板；
2. 重新估计式 (5)–(8) 并替换表 1–9、A1、A2 的全部数值；
3. 用真实结果重绘图 2（PSM 平衡性检验图）；
4. 核对文中引用的经济显著性计算（现按占位值推算，已保证内部自洽：中介效应满足加总约束、VIF 均值与表内数值一致、各子样本观测数加总等于全样本）。

## 参考文献真实性

52 条参考文献**全部经过两轮独立核验**（10 个主题检索代理 + 10 个对抗式核验代理，共 476 次检索，零拒绝）：作者、期刊、年份、卷期、页码/文章号均与公开记录一致。DOI 与核验证据见 `references_verified.json`。其中 2023–2026 年文献约占三分之二，来源含 JPE、Econometrica、AER、JEEA、J. Labor Econ.、China Econ. Rev.、World Dev.、TFSC、Systems 等。

唯一遗留事项：Zhu & Nie (2026, J. Asia Pac. Econ.) 的页码 31–61 未能从搜索摘要独立确认（DOI 10.1080/13547860.2024.2403399 已确认），请以期刊目录页复核。

## 格式说明（与团队范文/MDPI 模板一致）

- 基于团队 AI-青年就业范文的 MDPI Systems 模板骨架（`template_scaffold.docx`）：左侧连续行号（`lnNumType`）、首页侧栏（学术编辑/日期/引用/版权框）、Palatino Linotype 字体、三线表；
- **公式全部为 Word 原生公式编辑器格式（OMML）**：8 个展示式公式居中排版、编号 (1)–(8) 右对齐（制表位 center@4600 / right@9200），另有 87 处行内 OMML 变量；
- 参考文献按 MDPI 样式（期刊缩写斜体、年份加粗、卷号斜体）、悬挂缩进、按首次引用顺序编号；
- 图 1（概念框架）与图 2（PSM 平衡）为 matplotlib 生成的嵌入 PNG。

已知渲染小瑕疵：LibreOffice 预览中 `Size`、`Mod` 等变量显示为 "S ize"、"M od"（为规避 LO 公式引擎关键字替换而做的双 run 拆分）；在 Microsoft Word 中显示正常无空隙。

## 重新构建

```bash
cd work/src/zhejiang_youth_paper
python3 make_figures.py       # 重绘图 1 / 图 2
python3 build_paper.py        # 输出 Zhejiang_Youth_Employment_Systems.docx（需同目录有 template_scaffold.docx，脚本内路径指向 sample_ai_youth.docx，请按需调整）
```

正文内容在 `paper_content_part1/2/3.py`（引文用 `{{key}}` 占位，构建时自动按首现顺序编号）；公式在 `paper_equations.py`；参考文献元数据在 `paper_refs.py`。
