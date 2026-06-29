# Resampling Silently Degrades Probability Calibration in Tree Ensembles

[![Read PDF](https://img.shields.io/badge/Read%20PDF-6--page%20IEEE%20paper-b91c1c)](paper/main.pdf)
[![Pages](https://img.shields.io/badge/pages-6-0f766e)](paper/main.pdf)
[![Figures](https://img.shields.io/badge/figures-6-2563eb)](figures/)
[![Datasets](https://img.shields.io/badge/datasets-5%20OpenML-7c3aed)](data/processed/)
[![Reproducible](https://img.shields.io/badge/reproducible-end--to--end-brightgreen)](#-复现)

> 一篇**完全用 [Light](../../README.md) 技能包从零做到底**的端到端实证研究：找文献 → 提 idea → 对抗严审 → 跑实验 → 出图 → 写成 6 页 IEEE 论文。**所有数字都来自真实运行，不造一个数据。**

## 📄 论文展示

**[📖 阅读完整 IEEE PDF 论文](paper/main.pdf)** · [Raw PDF](https://raw.githubusercontent.com/Light0305/Light-skills/master/projects/resampling-calibration-study/paper/main.pdf) · [LaTeX 源码](paper/main.tex)

<p align="center">
  <a href="paper/main.pdf">
    <img src="paper/main-preview.png" alt="论文首页预览" width="720">
  </a>
</p>

<p align="center"><sub>点击论文首页预览即可打开完整 PDF</sub></p>

## TL;DR

重采样(SMOTE、随机过/欠采样)是处理类别不平衡的标准做法，几乎总是用 F1 或 AUC 来评判。本研究揭示它们有个隐形代价：会**系统性破坏树集成的概率校准**，而实践者常看的判别指标几乎不动甚至变好——所以这个代价在标准评估下完全看不见。

- **5** 个 OpenML 数据集(不平衡比 1.9–70)· **2** 个树集成 · **7** 种处理 · **10** 个随机种子 · 配对统计检验
- 所有重采样族都显著抬高 ECE(Wilcoxon *p* < 10⁻³，Holm 校正)
- 欠采样最糟，且随不平衡比急剧恶化：IR=70 时 ECE 从 0.008 飙到 0.395
- 一步事后校准可把 ECE 降约 66%，AUC 仅损 0.003

## 📊 图表展示

九种各不相同的图,全部来自真实实验数据——一图一个角度,拼成完整故事。

<table>
  <tr>
    <td align="center" width="33%">
      <b>🕸 五指标权衡雷达</b><br>
      <img src="figures/g1_radar.png" alt="radar" width="280"><br>
      <sub>判别指标几乎不变,唯独校准轴塌陷</sub>
    </td>
    <td align="center" width="33%">
      <b>🎻 ECE 分布小提琴</b><br>
      <img src="figures/g2_violin.png" alt="violin" width="280"><br>
      <sub>欠采样散得极宽,校准后收紧贴地</sub>
    </td>
    <td align="center" width="33%">
      <b>📉 校准修复斜率图</b><br>
      <img src="figures/g3_slope.png" alt="slope" width="280"><br>
      <sub>SMOTE→+Iso,五数据集无一例外下降</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <b>🫧 损害随不平衡比放大气泡图</b><br>
      <img src="figures/g4_bubble.png" alt="bubble" width="280"><br>
      <sub>对数不平衡比,气泡面积=样本量</sub>
    </td>
    <td align="center" width="33%">
      <b>↔️ 双模型发散条形</b><br>
      <img src="figures/g5_diverge.png" alt="diverge" width="280"><br>
      <sub>提升树 vs 随机森林,两者都受害都能救</sub>
    </td>
    <td align="center" width="33%">
      <b>🔥 条件×数据集热力图</b><br>
      <img src="figures/g6_heatmap.png" alt="heatmap" width="280"><br>
      <sub>七处理×五数据集的 ECE 一览</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <b>🏔 ECE 密度山脊图</b><br>
      <img src="figures/g7_ridge.png" alt="ridgeline" width="280"><br>
      <sub>重采样越激进,分布整体右移</sub>
    </td>
    <td align="center" width="33%">
      <b>📈 累积分布 ECDF</b><br>
      <img src="figures/g8_ecdf.png" alt="ecdf" width="280"><br>
      <sub>欠采样曲线远远甩到右侧</sub>
    </td>
    <td align="center" width="33%">
      <b>🍭 数据集损害排行棒棒糖</b><br>
      <img src="figures/g9_lollipop.png" alt="lollipop" width="280"><br>
      <sub>按校准损害排序,谁最受伤一目了然</sub>
    </td>
  </tr>
</table>

<details>
<summary>📎 论文里用到的原始出版级图(点开)</summary>

<table>
  <tr>
    <td align="center" width="50%"><img src="figures/fig1_ece_by_condition.png" width="380"><br><sub>ECE by condition</sub></td>
    <td align="center" width="50%"><img src="figures/fig3_ece_vs_ir.png" width="380"><br><sub>ECE vs imbalance ratio</sub></td>
  </tr>
  <tr>
    <td align="center" width="50%"><img src="figures/fig4_rho_sweep.png" width="380"><br><sub>ECE vs oversampling ratio</sub></td>
    <td align="center" width="50%"><img src="figures/fig6_shap_shift.png" width="380"><br><sub>SHAP attribution shift (ρ=0.96)</sub></td>
  </tr>
</table>

</details>

## 📂 项目内容

| 路径 | 内容 |
|------|------|
| [`paper/main.pdf`](paper/main.pdf) | 6 页 IEEE 论文(编译零错误：6 图 5 表 8 条已核验引用) |
| [`paper/main.tex`](paper/main.tex) · [`paper/refs.bib`](paper/refs.bib) | LaTeX 源码与文献库 |
| [`src/`](src/) | 数据获取、主实验、ρ 扫描、SHAP、先验校正、绘图脚本 |
| [`experiments/`](experiments/) | 原始结果：700 行主网格、250 行 ρ 扫描、SHAP 偏移、E5 先验校正 |
| [`data/processed/`](data/processed/) | 5 个预处理好的 OpenML 数据集(parquet) |
| [`docs/`](docs/) | 各阶段记录：文献综述、idea、严审判决、计划、数据集卡、结果分析 |

## 🔁 复现

```bash
pip install numpy pandas scikit-learn matplotlib scipy shap
python src/fetch_data.py          # 拉取并预处理 5 个 OpenML 数据集
python src/run_experiments.py     # 主网格 700 行
python src/run_rho_sweep.py       # E4：过采样比扫描
python src/run_prior_correct.py   # E5：解析先验校正(负结果)
python src/run_shap.py            # SHAP 特征归因偏移
python src/make_figures.py && python src/make_figures_extra.py && python src/make_gallery.py
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## 🪞 诚实复盘：Light 在这个项目里暴露并修复了自己的短板

这篇论文最有价值的产出，其实不是论文本身。它的**核心结论与前人工作高度重叠**(Dal Pozzolo 2015 已专门研究欠采样破坏校准)，而这一点直到接近完稿才被检索出来——立项时新颖性被高估为约 70，实际只有 35–45。

我们没有掩盖这件事，而是把它转化成对技能包的改进。为根除此类"做完才发现撞车"：

- **`idea-generation`**：提 idea 时强制回答四问——有没有人做过同一核心、是不是真缺口、是真创新还是增量、审稿人会用什么理由拒；
- **`idea-critique`**：严审时独立复核核心撞车、对新颖性谎报记红旗、预演拒稿理由；
- **`self-review`**：论文定稿前的核心撞车终检兜底；
- **`paper-drafting`**：补上"论文确实只是增量时，如何诚实地讲好故事"——重定位而非夸大、把负结果变成卖点、把 claim 收缩到证据撑得住的尺度。

论文本身也贯彻了同样的诚实：明确承认前作、如实写出一个**负结果**(解析先验校正对 SMOTE 不奏效，因为 SMOTE 扭曲的是类条件密度而非单纯先验)，而不是假装首创。**技能包通过真刀真枪做项目、并诚实面对不足，变得更可靠。**

> 本项目是 [Light](../../README.md) 科研技能包的端到端案例展示。
