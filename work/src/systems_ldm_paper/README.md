# 数字化转型中的领导与决策论文 — MDPI《Systems》特刊平行稿（第六篇）

**Manuscript**: `work/out/Digital_Leadership_Decision_Agility_Systems.docx`（正式投稿文件，24 页）与同名 `.pdf`。
**Cover Letter**: `work/out/Cover_Letter_Digital_Leadership_Decision_Agility_Systems.docx`。

**Title**: *Leadership and Decision Making in Digitally Transforming Enterprises: Multivariate Modeling and Cluster Typologies of Decision Agility and Young Managerial Advancement*

**目标特刊**: *Navigating Digital Transformation: Leadership and Decision Making in Today's Systems*（客座编辑 Prof. Dr. Maja Meško）。与第五篇（`systems_dtl_paper`）为**同一特刊的平行备选稿**，选题、样本、变量、行文完全不同。

## 选题定位（与第五篇的区别）

第五篇研究"数字实践 → 青年雇佣结果"（青年员工占比、青年离职率）；本篇把特刊标题的三要素**直接作为研究对象**：

- **预测变量（领导-决策实践 4 项）**：数字化转型领导力 DLV（6 条目）、AI 辅助管理决策广度 ADM（10 个管理决策域计数）、决策过程数字化 DPD（5 条目）、青年员工决策参与 EDI（4 条目,含反向导师制、跨层级委员会）
- **因变量（决策系统的两个属性）**：组织决策敏捷性 ODA（5 条目）+ **青年管理者占比 YMP**（≤35 岁管理岗占比——青年职业发展/晋升维度）
- **样本**：长三角（沪苏浙皖）285 家企业,CEO/总经理/战略高管报告人,2026-03–05 调研
- **理论**：上层梯队 + 组织信息加工理论 + 社会技术系统 + 动态能力/决策速度经典（Eisenhardt 1989; Baum & Wally 2003）+ AI 增强决策（Shrestha et al. 2019; Csaszar et al. 2024）

## 主要结果（H1–H3）

- **H1 部分支持——"技术提速、参与换代"的互补不对称**：DLV 与 DPD 同时关联敏捷性与管理层年轻化；ADM 只与敏捷性显著（与 YMP 边缘 p=0.077）；EDI 只与年轻化显著（效应量全文最大 η²=0.163;与 ODA 边缘 p=0.051）
- **H2 支持**：单一潜因子 FACT_LDC（领导-决策构型,抽取后方差 42.8%）,对 ODA β=0.482、对 YMP β=0.256,均 p<0.001;构型的"引擎"是领导与流程,AI 广度与青年参与公因子方差最低
- **H3 支持**：两类社会技术决策体制——敏捷数字引领型（133 家,YMP 34.4%）vs 常规科层型（152 家,YMP 28.1%）;轮廓系数 0.283,Ward 层次聚类与 k-means 一致率 76.8%;**两类体制的行业构成几乎相同**（数字核心 27.1% vs 24.3%）——决策体制是组织选择而非行业宿命

## ⚠️ 数据为模拟仿真

问卷数据由 `p6_analysis.py`（种子 20260721）模拟生成,统计量全部自洽（信度 α 0.795–0.864、Harman 33.4%<40%、无应答检验最小 p=0.337、MANOVA/MANCOVA/EFA/回归/聚类交叉一致）。`p6_stats.json` 为唯一数据源,正文与表格数值全部由脚本生成。

## 参考文献

74 条:10 条新增（决策速度/敏捷性经典、AI 增强决策、CEO 年龄与数字化转型、反向导师制、员工发声元分析、青年晋升纵向研究,均双源核验含 DOI,证据见 `p6_references_verified.json`）+ 64 条复用一/二/五篇已核验文献池。39/74（53%）为 2023–2026 年文献。

## 重新构建

```bash
cd work/src/systems_ldm_paper
python3 p6_analysis.py        # 统计量 + p6_fig1-5.png
python3 build_paper6.py       # 生成 Digital_Leadership_Decision_Agility_Systems.docx
python3 make_cover_letter6.py # 生成 Cover Letter
```

依赖同目录 `mdpi_builder.py`、`front_matter.xml`、`template_scaffold.docx`、`paper_refs.py`、`p2_refs.py`、`p5_refs.py`、`cover_letter_template.docx`。
