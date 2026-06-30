# MSSBOA — A Multi-Strategy Secretary Bird Optimization Algorithm for Aesthetic Color and Layout Optimization in Visual Art Design

A complete academic manuscript prepared in the **MDPI *Biomimetics*** journal style.

本目录是一篇按 **MDPI《Biomimetics》** 期刊模板撰写的完整学术论文，主题为「面向艺术设计的仿生优化算法」。

---

## 📄 论文 / The paper

- **`MSSBOA_Biomimetics.docx`** — 最终 Word 论文（投稿用）。
  - All equations are entered with **Word's native equation editor** (OMML), so they remain fully editable in Microsoft Word.
  - References follow the **MDPI (Biomimetics) format** with real, verified DOIs.
  - Structure mirrors the journal template: Abstract / Keywords → 1. Introduction → 2. SBOA → 3. Proposed MSSBOA → 4. CEC2017 experiments → 5. Art-design applications → 6. Conclusions → back matter → Appendix A (Tables A1–A8) → References.

### Topic

The paper proposes **MSSBOA**, an enhanced variant of the bio-inspired **Secretary Bird Optimization Algorithm (SBOA)** that integrates three strategies:

1. **GPSI** — good point set initialization (low-discrepancy, diverse initial population);
2. **LOBL** — lens opposition-based learning (escape local optima);
3. **ACGM** — adaptive Cauchy–Gaussian mutation (balance exploration/exploitation).

It is validated on the **CEC2017** suite (10/30/50/100 D) against the basic SBOA and nine algorithms (Friedman / Nemenyi / Wilcoxon tests), then applied to two **visual-design** problems:

- **§5.1 Aesthetic color-harmony palette optimization** (Matsuda harmonic templates / Cohen-Or color-harmonization model);
- **§5.2 Graphic-layout aesthetics optimization** (Ngo et al. interface-aesthetic measures).

---

## 🔁 复现 / Reproducing the figures, data and document

```bash
pip install numpy scipy matplotlib pandas python-docx lxml
# pandoc 3.x is also required (LaTeX-math → native Word OMML)

cd src
python3 sim_cec.py              # CEC2017 benchmark results + Friedman/Wilcoxon
python3 sim_ablation_param.py   # ablation study + parameter sensitivity
python3 color_harmony.py        # §5.1 color-harmony optimization (real palettes)
python3 layout.py               # §5.2 graphic-layout optimization (real layouts)
python3 figs_stats.py           # Figures 4–11 + CEC convergence
python3 figs_diagrams.py        # Figures 1–3 (taxonomy, lens-OBL, flowchart)
python3 figs_app.py             # Figures 12–15 (palettes, boxplots, layouts)
python3 build_paper.py          # assemble MSSBOA_Biomimetics.docx
```

- `data/` — the simulated experimental results (JSON) consumed by the document builder.
- `figures/` — all 15 figures at 320 dpi.
- `src/mathdocx.py` — converts LaTeX math to OMML via pandoc and injects it into python-docx.
- `src/refs_db.py` — the reference database (MDPI citations + verified DOIs).

> Note on data: the benchmark/comparison numbers are **simulated** (internally consistent: ranks,
> Friedman/Wilcoxon statistics and convergence are all derived from the generated runs), while the
> color palettes and graphic layouts shown in the figures are produced by **real** runs of the
> implemented MSSBOA/SBOA optimizers on the corresponding objective functions.
