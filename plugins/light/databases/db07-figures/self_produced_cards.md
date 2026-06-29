# db07 反哺卡 — 自家九图（resampling-calibration-study 真实产出）

> schema: `figure_type, paper_source, research_field, purpose, data_required, layout, color_scheme, annotation_style, caption_style, possible_code_tool, replication_notes, where_to_place_in_paper`
> 核验日期：2026-06-12。**来源最硬——本仓库自家产出**：下列 9 张卡逐一对应 `projects/resampling-calibration-study/figures/g1_radar.png … g9_lollipop.png`，全部由 `src/make_gallery.py` 从 `experiments/results.csv`（700 行真实实验记录：5 数据集 × 2 模型 × 7 条件 × 多种子的 ECE/Brier/AUC/PR-AUC/F1）生成，代码与数据均在仓库内可复跑，无版权与外链失效风险。
> 配色铁律（全 db07 统一）：色盲友好、全文统一调色板、黑白可辨（线型+标记）、矢量优先。本组图为 README 展示用的现代鲜艳色板（见 make_gallery.py `C` 常量），投正文时应切回 SciencePlots/ColorBrewer 出版色并补线型冗余。

```yaml
- figure_type: 雷达图(多指标权衡)
  paper_source: "自家产出 projects/resampling-calibration-study/figures/g1_radar.png（src/make_gallery.py g1_radar，数据 experiments/results.csv）"
  research_field: 机器学习 / 类不平衡 / 模型评估
  purpose: 支撑"多指标里只有校准这一根轴在塌陷, 其余指标都还不错"的权衡 claim
  data_required: 同一组方法在 5 个可比指标(AUC/F1/PR-AUC/ECE/Brier)上的均值; 越大越好的轴需把 ECE/Brier 取反归一
  layout: 极坐标多边形, 每轴一指标, 多方法多条闭合曲线叠加半透明填充
  color_scheme: 每方法一色(蓝/橙/红/青), 填充 alpha≈0.08; 类别色板, 黑白下需配标记/线型
  annotation_style: 轴标注明指标方向(如"Calibration(1-ECE)""Brier(inverted)"避免读反); 图例置底部横排
  caption_style: 说明各轴归一方式与方向, 强调"高=好"已统一; 注明数据来源与聚合方式
  possible_code_tool: matplotlib polar subplot (subplot_kw=dict(polar=True))
  replication_notes: 遵 R3(雷达统一方向标注/指标数≤6); 图型特异——轴顺序/缩放会改变形状观感, 不可只挑对自己有利的轴
  where_to_place_in_paper: 结果-总体权衡概览(或答辩首图)

- figure_type: 小提琴图+散点(分布对比)
  paper_source: "自家产出 projects/resampling-calibration-study/figures/g2_violin.png（src/make_gallery.py g2_violin）"
  research_field: 机器学习 / 实验统计
  purpose: 支撑"某条件下指标分布又宽又偏(欠采样), 重校准后收窄"的分布形态 claim
  data_required: 每个条件下跨(数据集×模型×种子)的 ECE 全样本(非只均值)
  layout: 每条件一把小提琴(KDE 轮廓) + 抖动散点叠加 + 菱形标均值 + 基线均值水平虚线
  color_scheme: 每条件一色, 小提琴体 alpha≈0.3, 散点 alpha≈0.55; 类别色板
  annotation_style: 散点抖动避免重叠, 均值用大菱形, 基线用 muted 虚线参照
  caption_style: 说明每个分布的样本量与聚合维度; 强调看的是"分布宽窄/偏移"而非单点
  possible_code_tool: matplotlib violinplot + scatter 抖动 (seaborn violinplot 亦可)
  replication_notes: 遵 R5(小样本叠原始散点); 图型特异——小提琴在小样本下 KDE 会失真, 不要只画小提琴隐藏点数
  where_to_place_in_paper: 结果-稳定性/方差分析

- figure_type: 斜率图(前后配对变化)
  paper_source: "自家产出 projects/resampling-calibration-study/figures/g3_slope.png（src/make_gallery.py g3_slope）"
  research_field: 通用 / 干预前后对比
  purpose: 支撑"同一处理(加一步校准)让每个数据集的指标都朝同方向改善"的配对 claim
  data_required: 每个个体(数据集)在两个状态(校准前/后)的同指标配对值
  layout: 左右两列各一个状态, 每个数据集一条连线, 端点标数值与名称
  color_scheme: 每数据集一色连线, 端点描白边; 类别色板, 斜率方向即信息
  annotation_style: 端点直接标数值与数据集名, 隐藏多余坐标轴(去 top/right/bottom spine)
  caption_style: 说明两状态含义与配对单位; 强调"几乎全部下行"这一一致性
  possible_code_tool: matplotlib 两点连线 + text 标注
  replication_notes: 遵 R1(y 轴不截断以免夸大斜率); 图型特异——只适合配对/前后对比, 线条交叉多时改用其他图
  where_to_place_in_paper: 结果-校准修复效果

- figure_type: 气泡散点图(三变量, 含 log 轴)
  paper_source: "自家产出 projects/resampling-calibration-study/figures/g4_bubble.png（src/make_gallery.py g4_bubble）"
  research_field: 通用 / 关系与规模联合呈现
  purpose: 支撑"欠采样造成的校准恶化随不平衡比上升, 且与数据规模相关"的三变量 claim
  data_required: x=不平衡比(常需对数轴), y=指标恶化量, 气泡面积=第三变量(样本量)
  layout: 散点, x 对数轴; 气泡面积编码 n; 拥挤标签用引导线(leader line)拉到空白区
  color_scheme: 每数据集一色, 气泡 alpha≈0.62 描白边; 类别色板
  annotation_style: 引导线把标签拉到空白处避免压点; 标注 n 值; 面积非半径编码数值
  caption_style: 说明三个变量映射(x/y/面积)与对数轴; 注明面积编码的量
  possible_code_tool: matplotlib scatter (s=面积) + annotate 引导线 + set_xscale('log')
  replication_notes: 遵 R2(气泡面积∝数值非半径,否则视觉夸大平方倍); 图型特异——重叠点用引导线而非堆叠标签
  where_to_place_in_paper: 结果-规模/不平衡影响分析

- figure_type: 发散条形图(带符号增减)
  paper_source: "自家产出 projects/resampling-calibration-study/figures/g5_diverge.png（src/make_gallery.py g5_diverge）"
  research_field: 通用 / 相对基线的增减对比
  purpose: 支撑"各处理相对基线有的更好有的更差, 且两种模型趋势一致"的带符号对比 claim
  data_required: 每个处理相对基线的差值(可正可负), 可分两组(两模型)对照
  layout: 水平条以 0 为中轴左右发散; 两组用成对错位条(y±h/2); 0 处画粗轴线
  color_scheme: 两组各一色; 正负方向靠位置(左/右)区分, 轴标注明"←更好 更差→"
  annotation_style: 0 轴线加粗, x 轴标签显式写方向语义; 图例区分两组
  caption_style: 说明差值相对谁、正负含义、分组维度
  possible_code_tool: matplotlib barh (height 分两组) + axvline(0)
  replication_notes: 遵 R8(别用颜色单独编码正负,色盲不可辨); 图型特异——必须显式标注正负方向语义(读者不会默认哪边好)
  where_to_place_in_paper: 结果-跨模型稳健性
```

```yaml
- figure_type: 条件×数据集矩阵热力图(带注数)
  paper_source: "自家产出 projects/resampling-calibration-study/figures/g6_heatmap.png（src/make_gallery.py g6_heatmap）"
  research_field: 通用 / 二维因子全景
  purpose: 支撑"每个处理在每个数据集上的表现一眼可比"的全景 claim(区别于混淆矩阵——这里是 条件×数据集 因子矩阵, 非真实vs预测)
  data_required: 行=数据集, 列=处理条件, 格值=指标(ECE)均值
  layout: 矩形热力网格, 每格写数值, 右侧色标
  color_scheme: 发散/顺序色图(RdYlGn_r, 低=好), 固定 vmin/vmax 便于跨图比; 格内文字按底色深浅自动黑/白
  annotation_style: 每格标数值, 文字颜色随背景明暗切换保证可读; 行列标签清晰
  caption_style: 说明指标、颜色方向(越红越差)、聚合方式与 vmin/vmax
  possible_code_tool: matplotlib imshow + 双层循环 text 标注 + colorbar
  replication_notes: 遵 R6(跨多张热力图固定同一 vmin/vmax); 图型特异——注数防重叠需控字号; 与"混淆矩阵热力图"是两类不同用途, 勿混名
  where_to_place_in_paper: 结果-全条件总览(附录或主结果旁)

- figure_type: 山脊图/joyplot(多组密度堆叠)
  paper_source: "自家产出 projects/resampling-calibration-study/figures/g7_ridge.png（src/make_gallery.py g7_ridge）"
  research_field: 通用 / 多组分布对比
  purpose: 支撑"随处理越激进, 指标分布整体右移"的多组分布趋势 claim
  data_required: 多个组各自的指标样本(用于核密度估计)
  layout: 纵向堆叠的密度曲线, 各组轻微重叠, 左侧标组名
  color_scheme: 每组一色填充 alpha≈0.7 + 白描边分层; 顺序排列体现趋势
  annotation_style: 组名直接标在各脊左端并用该组色; 隐藏 y 轴刻度(密度无绝对意义)
  caption_style: 说明分布变量、各组样本量、KDE 带宽设置
  possible_code_tool: scipy gaussian_kde + matplotlib fill_between(逐组偏移)
  replication_notes: KDE 带宽(bw_method)会显著影响形状, 须报告; 重叠过多会互相遮挡, 组数适中; 小样本慎用
  where_to_place_in_paper: 结果-分布演变趋势

- figure_type: 经验累积分布图(ECDF 阶梯)
  paper_source: "自家产出 projects/resampling-calibration-study/figures/g8_ecdf.png（src/make_gallery.py g8_ecdf）"
  research_field: 通用 / 无分箱的分布对比
  purpose: 支撑"某方法的指标整条曲线都偏右(更差)"的随机占优式 claim, 不依赖分箱
  data_required: 各方法的指标样本(每个 run 一个值)
  layout: 阶梯线 x=指标值 y=累计占比[0,1]; 多方法多条; 可在中位数处标点
  color_scheme: 每方法一色粗线; 类别色板 + 线型冗余备黑白
  annotation_style: 中位数标点; 曲线水平分离即效应大小的直观体现
  caption_style: 说明样本量与"曲线靠右=更差"的读法
  possible_code_tool: numpy 排序 + matplotlib step(where='post')
  replication_notes: ECDF 比直方图更稳(无分箱偏差), 适合小样本; 标注读法避免读者误解方向
  where_to_place_in_paper: 结果-分布对比(替代/补充直方图)

- figure_type: 棒棒糖图(排序数值)
  paper_source: "自家产出 projects/resampling-calibration-study/figures/g9_lollipop.png（src/make_gallery.py g9_lollipop）"
  research_field: 通用 / 排序与排名
  purpose: 支撑"哪些数据集受损最重"的排序 claim, 比满条形更轻量
  data_required: 每个类别一个数值, 按值排序
  layout: 水平茎(0→值)+末端圆点, 按数值升/降序排列, 点内或旁标数值
  color_scheme: 顺序色(YlOrRd 按排名渐变)突出极值; 单调即可黑白辨
  annotation_style: 圆点内标数值; y 轴类别名; 去除多余 spine 与刻度
  caption_style: 说明数值含义与排序方向
  possible_code_tool: matplotlib hlines/plot(茎) + scatter(点) + text
  replication_notes: 棒棒糖=条形的轻量替代, 适合类别多/强调排名; 排序方向与基线须明确; 别在需要精确读值的场合替代带刻度条形
  where_to_place_in_paper: 结果-按受损程度排名
```

---

### 与 m11 绘图执行 / JOURNAL_SPECS 的衔接

- 这 9 张是 README 展示色板（make_gallery.py 的鲜艳 `C` 常量，DejaVu Sans）。**投稿正文出图时**：切到绘图执行技能 light-figure-drawing 的 `assets/science.mplstyle` / SciencePlots，配 ColorBrewer/Okabe-Ito 出版色，并补线型+标记冗余满足黑白可辨。
- **栏宽**：`light-figure-drawing/scripts/figure_export.py` 的 `JOURNAL_SPECS` 是栏宽/figsize 的**真相源**，按目标刊取实有键（实测值：IEEE 单栏 88.9mm≈3.5in、Nature 单栏 89mm/双栏 183mm、Science 单栏 55mm/双栏 120mm/整页 183mm），并用 `check_figure_size` 校验。本项目 `make_figures.py` 已示范 IEEE 单栏 `COLW=3.5`。db07 卡不另写死尺寸。
- 全文统一调色板与跨材料（论文图/PPT/前端）一致由 a07(consistency) 维护，色值锚点对齐 db05 `design_tokens.template.json`。

