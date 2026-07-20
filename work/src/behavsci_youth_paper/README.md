# LLM×青年职业困境论文 — MDPI《Behavioral Sciences》特刊投稿终稿（第三篇）

**Manuscript**: `work/out/LLM_Career_Distress_BehavSci.docx`（正式投稿文件）与同名 `.pdf`（预览渲染，22 页）。

**Title**: *From Narratives to Numbers: Using Large Language Models to Assess Career Distress in Chinese Young Adults’ Open-Ended Employment Narratives*

**目标特刊**: *The Use of AI in the Behavioral Sciences*（客座编辑 Dr. Danilo Garcia，斯塔万格大学；投稿截止 **2026-09-30**）——特刊主旨即"用 LLM/NLP/语义分析架起开放文本与定量测量之间的桥梁"，本文以"LLM 对青年就业叙事的心理测量学评估"直接对标，且引用了客座编辑的代表作（Kjell, Kjell, Garcia, & Sikström, 2019, *Psychological Methods*；Sikström & Garcia, 2020）。

## 研究设计（风格对标 Behav. Sci. 2026, 16, 268 及该刊 APA 体例）

- **样本**：浙江省 18–29 岁青年横截面网络调查，N = 947（配额抽样；就业/灵活就业/失业求职/备考"慢就业"/其他 NEET 五类）
- **开放叙事**：3 个开放题（现状与困难/求职感受/三年展望与支持需求），中位 155 字
- **LLM 评分**：GPT-4o + Qwen2.5-72B（双模型、各 3 次运行、温度 0、零样本），对"职业困扰/就业焦虑/职业信心"1–10 评分；Equation (1) 平均为合成分
- **效标量表**：CDS 职业困扰、CAAS-SF 生涯适应力、GAD-7、PHQ-8、自评可雇性、SWLS
- **人工编码**：分层子样本 n = 200，2 名评分者（ICC 与 κ 验证）
- **语义聚类**：BGE-M3 嵌入 → UMAP → k-means（轮廓系数选 k = 6）→ 人工复核精化 → 6 大困境主题
- **假设**：H1 信度（跨运行 ICC≈.97、跨模型 r≈.77–.80、人机 r=.80）；H2 收敛—区分效度（单质 r̄=.44 > 异质 r̄=.27）；H3 增量效度（PHQ-8 ΔR²=.024、SWLS ΔR²=.013；AUC .754→.777，DeLong p=.002）；H4 主题×心理调适（T5"意义与动机困境"最差，η²=.078）——全部支持

## ⚠️ 重要声明：数据为校准占位值

`p3_analysis.py` 内全部"调查数据"为**按文献常模校准并加噪声的种子化模拟数据**（seed=42），并非实际调研所得；表 5 的受访者引语为示意性合成译文。投稿前必须：

1. 实施真实调查（问卷 + 三个开放题）并完成真实的 LLM 评分、人工编码与嵌入聚类；
2. 在 `p3_analysis.py` 中把 `REAL DATA HOOK` 处的模拟数组替换为真实数据矩阵、删除模拟生成代码块，重跑脚本；
3. 脚本自动重算全部统计量（`p3_stats.json`）并重绘图 2–5；正文表 1–4、6–8 与结果段落中的数值**在构建时直接读取 `p3_stats.json` 生成**，重跑后自动同步；仅少量正文叙述句（3.x 节文字中的显著性描述）需人工核对；
4. `python3 build_paper3.py` 重新生成 docx。

伦理批号（JXU-COB-2025-014）为占位样式，请以学院伦理委员会实际批文为准。

## 参考文献真实性

59 条参考文献全部经 find+adversarial-verify 工作流双轮核验（3 个主题检索代理 + 63 个对抗式核验代理、共 66 个代理，全部 WebSearch 交叉验证，零否决），证据与 DOI 见 `references_verified.json`。体例为该刊要求的 **APA 作者–年份制**（正文夹注 + 字母序文献表 + 期刊全称 + DOI）。

## 格式说明

- 直接基于官方 `behavscitemplate.dot`（Word 2007+ zip）重打包：保留其命名样式（MDPI11articletype…MDPI81references）、页眉页脚（卷号已更新为 2026/16）、左侧连续行号（sectPr lnNumType）
- 4 个展示公式为 Word 原生 OMML，置于模板自带的双列公式表格中（公式居中、编号右对齐）；正文含行内 OMML
- 三线表、图注/表注均用模板样式；引言含 4 条 MDPI 体例假设段（左缩进斜体）

## 重新构建

```bash
cd work/src/behavsci_youth_paper
python3 p3_analysis.py      # 重算统计量 + 重绘 p3_fig2-5.png
python3 make_fig1.py        # 流程图 p3_fig1.png
python3 build_paper3.py     # 生成 LLM_Career_Distress_BehavSci.docx
```

依赖：同目录 `behavsci_template.dot`、`bs_builder.py`、`p3_refs.py`、`p3_equations.py`、`p3_content_a.py`、`p3_content_b.py`、`p3_stats.json`。
