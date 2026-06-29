# R9 批1 抽查记录 — db05/db06/db07 新卡来源一致性

- 抽查日期：2026-06-12
- 抽查范围：本批新增 18 张真实卡（db05 +4、db06 +2、db07 +12）
- 抽查比例：5/18 ≈ 28%（≥ 验收要求 20%）
- 抽查方法：来源链接 `curl` HTTP 状态 + 卡内数据与来源逐字比对（自家产出卡比对生成代码与数据）

## 抽查明细

| # | 卡 | 来源 | 核验动作 | 结果 |
|---|---|---|---|---|
| 1 | db05 新拟物控制面板 | https://neumorphism.io/ | curl HTTP 状态 | **200**，可达 ✓ |
| 2 | db06 开题报告答辩 | 自家 themes.py `academic` 主题 | 卡内 hex（primary #1F4E79 / secondary #2E75B6 / accent #C00000 / text #333333）逐字比对 themes.py | **完全一致** ✓ |
| 3 | db07 雷达图(g1) | projects/.../src/make_gallery.py `g1_radar` | 卡内"5 指标 AUC/F1/PR-AUC/ECE/Brier、polar、ECE/Brier 取反归一、填充 alpha=0.08"比对代码 | 代码第 44/47-50/53/57 行**逐项吻合** ✓ |
| 4 | db07 气泡散点图(g4) | projects/.../src/make_gallery.py `g4_bubble` | 卡内"x 对数轴、气泡面积编码 n、引导线 leader line、alpha=0.62"比对代码 | 代码第 136-143 行 `set_xscale('log')`/`N**0.5`/`annotate` 引导线/`alpha=0.62` **吻合** ✓ |
| 5 | db05 编辑器极简(Linear/Vercel) | https://linear.app/method、https://vercel.com/geist/introduction | curl HTTP 状态（双源） | 均 **200**，可达 ✓ |

## 结论

- 5 张抽查卡的来源链接全部可访问（HTTP 200），自家产出卡的卡内描述与生成代码逐项一致。
- 自家九图反哺卡（db07 g1-g9）来源最硬：代码 `src/make_gallery.py` + 数据 `experiments/results.csv`（700 行真实实验记录）均在仓库内，可 `python src/make_gallery.py` 复跑重现，无外链失效与版权风险。
- db06 两卡的色板/字体取自已 selftest 验证的 `themes.py`，非凭记忆；版式逻辑来源（Beamer 主题矩阵、CMU 教学设计）HTTP 200 可达。
- **诚信声明留痕**：R6.5 声明的"imggen deck 实跑沉风格卡"因有 key 端到端实跑仍是 GAP（PROGRESS R6.6#4），本批 db06 卡明确不以 imggen 实跑为来源，待 R6 实跑补做后再沉对应卡。

## 全批来源链接核验汇总（curl，2026-06-12）

db05：MDN backdrop-filter 200 / neumorphism.io 200 / linear.app/method 200 / vercel.com/geist 200 / pudding.cool 200 / typewolf.com 200
db06：mpetroff Beamer 矩阵 200 / CMU 教学设计 200（themes.py selftest 绿）
db07：matplotlib boxplot 200 / seaborn boxplot 200 / matplotlib GridSpec 200 / matplotlib subplots 200；九图来源为仓库内代码+数据
