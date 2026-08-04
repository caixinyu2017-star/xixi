# 嘉兴市烟草专卖局五篇论文评审与改稿

## 交付物（deliver/）

| 文件 | 说明 |
|---|---|
| `评审意见与改进建议.docx` | 五篇论文的重点问题、解决办法与可提升之处 |
| `论文1_…_修改稿.docx` | 11 图 8 表 |
| `论文2_…_修改稿.docx` | 10 图 6 表 |
| `论文3_…_修改稿.docx` | 9 图 7 表 |
| `论文4_…_修改稿.docx` | 9 图 6 表 |
| `论文5_…_修改稿.docx` | 9 图 10 表 |

排版规范：一级标题黑体小三加粗；二级标题黑体四号；三级标题黑体小四；
正文宋体小四、段前段后 0、首行缩进 2 字符、1.5 倍行距；
图名置于图下方（五号黑体），表名置于表上方（五号黑体），表格为三线表；
全部图表均在正文中先引用后出现，编号连续。

公式排版：数学公式为 Word 原生 OMML 对象（可用公式编辑器直接打开编辑），
居中排布，编号以圆括号置于公式行末。转换器见 `omml.py`（LaTeX → OMML）。

写作风格：主题段落式——每段首句为主题句概括核心观点，其余句子解释与展开。

## 目录结构

```
analysis/    分析与绘图代码（可复现）
  style.py         论文级绘图统一样式
  diagram.py       概念图绘制工具箱
  pN_analysis.py   第 N 篇的数据/实证分析（输出 pN_results.json）
  pN_figs.py       第 N 篇的概念图
figures/     46 张图（cN=概念图，dN=数据图）+ prompts.json
origimg/     论文一案例截图（已脱敏）
raw/         原始稿件
deliver/     交付的 Word 文档
build_pN.py  由分析结果 + 图生成 Word
docbuild.py  Word 排版工具（字体字号规范集中在此）
verify_fmt.py / qa_order.py   排版与图表顺序自动核验
```

## 复现方式

```bash
cd analysis && for n in 1 2 3 4 5; do python3 p${n}_analysis.py; python3 p${n}_figs.py; done
cd .. && for n in 1 2 3 4 5; do python3 build_p${n}.py; done && python3 build_review.py
python3 verify_fmt.py deliver/*.docx && python3 qa_order.py deliver/*.docx
```

## 两点说明

**1. 概念图的生成方式。** 25 张概念图（示意图、机制图、路径图、技术路线图）由
gpt-image-2 生成，提示词为中文——该模型的简体中文渲染准确，无需退回英文标签，
清单见 `figures/prompts_cn.json` 与分批清单 `figures/cn_p1..5.json`。重新生成：

```bash
cd figures && for p in 1 2 3 4 5; do
  python3 ~/.claude/skills/gpt-image-2/scripts/gpt_image2.py --manifest cn_p$p.json -o .
done
```

带真实数据的统计图（文件名含 `_d`）仍由 Python 绘制（`analysis/pN_analysis.py`），
不使用生成式图像模型——这是数据图的基本要求。
`analysis/pN_figs.py` 为早期的 matplotlib 概念图脚本，已被 gpt-image-2 版本取代，保留备查。

**2. 数据的三类证据效力（修改稿中已逐处标注）。**

- **原文报告的实测值**：论文一的三方案性能与测试集构成、论文五的样本量与聚类分布。
  在其基础上的推算（置信区间、混淆矩阵反推、可行域、卡方检验）对原文直接有效。
- **情景仿真**：论文二、三、四原本无一手数据，改稿构建了参数化模型并做真实数值求解，
  揭示的是机制方向与量级关系，参数依据已在正文说明并配敏感性分析，
  **不是对本单位实测指标的观测值**，应以真实数据替换参数后重跑。
- **方法学演示**：论文五第 6 章的合成数据集实验，用于演示原文缺失的关键检验会得出什么结果，
  **必须在原始 DII 数据上重跑后方可写入结论**。

**脱敏说明**：论文一案例截图已按最小必要原则处理——移除含可识别人脸的视频画面截图，
遮蔽行政相对人姓名与许可证号。`origimg/` 中仅保留脱敏后的版本。
