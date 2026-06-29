# db07 补充卡 — 谱系补缺（箱线 / 数据集示意 / 组图）

> schema: `figure_type, paper_source, research_field, purpose, data_required, layout, color_scheme, annotation_style, caption_style, possible_code_tool, replication_notes, where_to_place_in_paper`
> 核验日期：2026-06-12。补齐 R9.3 图型清单中尚缺的箱线图、数据集示意图、组图(multi-panel)。来源为 matplotlib/seaborn 官方 gallery 文档（HTTP 200 核验，见文末），图型规范为通用统计制图通识。配色铁律同 db07 README（色盲友好/全文统一/黑白可辨/矢量优先）。

```yaml
- figure_type: 箱线图(分组分布与离群)
  paper_source: "matplotlib boxplot gallery https://matplotlib.org/stable/gallery/statistics/boxplot_demo.html ; seaborn https://seaborn.pydata.org/generated/seaborn.boxplot.html"
  research_field: 通用 / 分组分布对比
  purpose: 支撑"不同组的中位数/四分位距/离群存在差异"的稳健分布 claim(对离群不敏感, 比均值±SD 更稳)
  data_required: 每组的样本集合(原始值); 不需正态假设
  layout: 每组一个箱(中位线+IQR 盒+须), 离群点单独标; 可叠加抖动散点显示真实点数
  color_scheme: 每组一色或统一中性色+强调一组; 类别色板, 黑白下靠位置区分
  annotation_style: 须线规则需说明(默认 1.5×IQR); 小样本叠散点; 必要时标中位数值
  caption_style: 说明箱体含义(中位/IQR/须/离群)、样本量、须线定义
  possible_code_tool: matplotlib boxplot / seaborn boxplot(+stripplot 叠点)
  replication_notes: 箱线图隐藏分布形状(双峰看不出)——小样本或疑似多峰时叠散点或改小提琴; 须线倍数须注明; n 很小时(<10)慎用箱线
  where_to_place_in_paper: 结果-分组分布/稳健性对比

- figure_type: 数据集示意图(样本与统计概览)
  paper_source: "通用数据集 figure 范式; 组图布局参照 matplotlib GridSpec https://matplotlib.org/stable/api/_as_gen/matplotlib.gridspec.GridSpec.html"
  research_field: CV/NLP/时序/表格 通用
  purpose: 支撑"数据集构成、类别分布、样本长相、采集设置"的可理解性, 让审稿人快速建立数据直觉
  data_required: 代表性样本缩略图/片段 + 类别数量分布 + 划分(train/val/test)统计 + 采集元信息
  layout: 上排样本网格(每类 1-2 例), 下排类别分布柱/饼 + 划分表; GridSpec 控制混合面板
  color_scheme: 样本保真; 统计图用统一调色板, 类别色与正文一致
  annotation_style: 样本标类别名; 分布图标数量; 标注划分比例与是否分层
  caption_style: 说明来源/许可、样本量、类别、划分方式、采集设置; 有隐私/伦理需说明脱敏
  possible_code_tool: matplotlib GridSpec(图文混排) / PIL 拼样本 / seaborn 画分布
  replication_notes: 样本须随机抽非挑樱桃; 标注真实许可与来源(db04 数据集卡联动); 涉人/隐私数据需脱敏并说明伦理
  where_to_place_in_paper: 方法-数据集 或 实验设置开头

- figure_type: 组图 / 多面板(multi-panel, 带 a/b/c 标号)
  paper_source: "组图布局: matplotlib subplots https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html ; GridSpec https://matplotlib.org/stable/api/_as_gen/matplotlib.gridspec.GridSpec.html"
  research_field: 通用 / 一图讲多个相关证据
  purpose: 把一组逻辑相关的子图(如不同数据集/不同视角)合成单图整体, 支撑"同一结论在多条件下成立"的综合 claim, 满足顶刊一图多面板规范
  data_required: 多个子分析的结果, 彼此逻辑关联可并置
  layout: 规则/不规则网格(GridSpec), 每面板左上角 a/b/c 粗体标号; 共享坐标轴/图例时统一放置
  color_scheme: 全panel统一调色板与字号; 共用图例避免重复; 跨面板同一含义同一色
  annotation_style: 面板标号 a/b/c(常 8pt 粗体, 对齐 Nature 规范); 共享轴只在边缘标; 统一刻度范围便于比较
  caption_style: 总说明 + 分述 (a)…(b)…; 每面板自洽; 注明共享的设置
  possible_code_tool: matplotlib subplots/GridSpec / subfigure; 复杂排版可 Inkscape 拼矢量
  replication_notes: 面板间字号/线宽/配色必须一致(最常见的不一致来源); 标号风格跟目标刊(a vs A vs (a)); 缩放到栏宽后最小字号仍须达标(见 JOURNAL_SPECS min_font_pt)
  where_to_place_in_paper: 主结果大图 或 综合分析(跨章节证据合并)
```

---

### 核验表（2026-06-12，curl HTTP 状态）

| 来源 | 状态 |
|---|---|
| https://matplotlib.org/stable/gallery/statistics/boxplot_demo.html | 200 |
| https://seaborn.pydata.org/generated/seaborn.boxplot.html | 200 |
| https://matplotlib.org/stable/api/_as_gen/matplotlib.gridspec.GridSpec.html | 200 |
| https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html | 200 |

> 说明：链接经 Bash `curl` 取 HTTP 状态码核实于 2026-06-12 真实可达；卡内图型规范为统计制图通识与各 gallery 公开示例的提炼，落地以 m11(light-figure-drawing) 的样式与 JOURNAL_SPECS 为准。
