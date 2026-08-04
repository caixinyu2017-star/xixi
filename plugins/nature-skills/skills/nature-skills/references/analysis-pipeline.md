# 8 步分析流水线 — 操作清单

每一步给出：产出物、检查项、三种技术栈的代码骨架。骨架是起点不是模板，
变量名、聚类层级、控制变量必须按实际数据改。

---

## 第 0 步 — 对齐

**产出物**：一段写给用户确认的分析方案，包含研究问题、数据说明、技术栈、交付物四项。

**检查项**

- [ ] 被解释变量、核心解释变量、控制变量分别是哪些列，列名写出来
- [ ] 观测单位（个体-年？企业-季度？地区-月？）
- [ ] 用户是否已有既定的识别策略，还是要一起设计
- [ ] 技术栈已确认（Python / Stata / R），没确认就停下来问

---

## 第 1 步 — 数据审计

**产出物**：一份数据体检报告 + 清洗后的分析样本。

**检查项**

- [ ] 行列数、观测单位、面板平衡性
- [ ] 每个待用变量的缺失率、min/max、分位数、类型
- [ ] ID 唯一性、重复观测
- [ ] 时间覆盖与断档
- [ ] 量纲与单位（万元还是元？百分数还是小数？）
- [ ] 极端值：是真实极端还是录入错误，分开处理

```python
# Python
import pandas as pd
df = pd.read_csv("data/raw.csv")
print(df.shape, df.dtypes, sep="\n")
print(df.isna().mean().sort_values(ascending=False).head(20))
print(df.describe(percentiles=[.01, .05, .5, .95, .99]).T)
print("重复 ID-年:", df.duplicated(subset=["id", "year"]).sum())
print("面板平衡:", df.groupby("id")["year"].nunique().value_counts())
```

```stata
* Stata
use "data/raw.dta", clear
describe
misstable summarize
summarize, detail
duplicates report id year
xtset id year
xtdescribe
```

```r
# R
library(dplyr); library(skimr)
df <- readr::read_csv("data/raw.csv")
skim(df)
df |> count(id, year) |> filter(n > 1)
df |> group_by(id) |> summarise(T = n_distinct(year)) |> count(T)
```

**发现问题就停下报告**，不要静默处理。

---

## 第 2 步 — 描述统计 Table 1

**产出物**：分组描述统计表，含组间差异检验。

- 连续变量：N、均值、标准差、最小值、中位数、最大值
- 分类变量：频数与占比
- 处理组 vs 对照组要给组间差异及其检验

```python
import pandas as pd
vars_ = ["y", "treat", "x1", "x2"]
tab = df.groupby("treat")[vars_].agg(["count", "mean", "std", "min", "median", "max"])
```

```stata
estpost summarize y x1 x2, detail
esttab using "tables/table1.rtf", cells("count mean sd min p50 max") replace
estpost ttest y x1 x2, by(treat)
```

```r
library(modelsummary)
datasummary_balance(~ treat, data = df, output = "tables/table1.docx")
```

---

## 第 3 步 — 识别策略

**产出物**：写明估计方程、固定效应、控制变量、标准误聚类、样本筛选，以及**每条的理由**。

模板：

> 基准回归设定为 `Y_it = β·D_it + γ'X_it + μ_i + λ_t + ε_it`。
> `μ_i` 吸收不随时间变化的个体异质性，`λ_t` 吸收全国性冲击。
> 控制变量 `X` 包含 <…>，选择理由是 <…>。
> 标准误在 <层级> 聚类，因为处理在该层级分配 / 误差在该层级相关，共 <N> 个聚类单元。
> 样本剔除 <…>，剔除比例 <…>。

各方法必须交代的假设与检验：

| 方法 | 假设 | 检验做法 |
|---|---|---|
| DID | 平行趋势 | 事件研究：以处理前一期为基准，画出各期动态系数与置信区间 |
| DID | 无预期效应 | 事件研究图里处理前各期系数应不显著 |
| DID（交错处理） | 异质处理效应 | Goodman-Bacon 分解；改用 CS / SA / did_imputation 估计量 |
| IV | 相关性 | 第一阶段系数与 F 统计量（经验阈值 10，弱工具变量更严格用 Montiel-Pflueger） |
| IV | 外生性 | 理论论证为主；过度识别时做 Hansen J |
| RDD | 无操纵 | McCrary / rddensity 密度检验 |
| RDD | 带宽稳健 | 最优带宽 ± 50% 的敏感性；协变量在断点处连续 |
| PSM | 共同支撑 | 倾向得分分布重叠图 |
| PSM | 平衡性 | 匹配后各协变量标准化偏差 < 10% |
| 合成控制 | 拟合优度 | 拟合期 RMSPE；in-space / in-time 安慰剂 |

---

## 第 4 步 — 基准估计

**产出物**：逐列递进的回归表 + 原始输出日志。

```python
import pyfixest as pf
m1 = pf.feols("y ~ treat",                      data=df, vcov={"CRV1": "id"})
m2 = pf.feols("y ~ treat + x1 + x2",            data=df, vcov={"CRV1": "id"})
m3 = pf.feols("y ~ treat + x1 + x2 | id + year", data=df, vcov={"CRV1": "id"})
pf.etable([m1, m2, m3])
```

```stata
reghdfe y treat, absorb(id year) cluster(id)
eststo m3
esttab m1 m2 m3 using "tables/baseline.rtf", b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) replace
```

```r
library(fixest); library(modelsummary)
m3 <- feols(y ~ treat + x1 + x2 | id + year, data = df, cluster = ~id)
modelsummary(list(m1, m2, m3), stars = c('*'=.1, '**'=.05, '***'=.01))
```

**报出来的每个数字都必须能在输出日志里找到。**

---

## 第 5 步 — 稳健性

至少四类，每类说明它排除了什么替代解释：

1. **换度量**：被解释变量取对数/取水平、核心解释变量换定义
2. **换样本**：剔除 1%/99% 极端值、剔除特殊年份（政策叠加期、疫情期）、剔除头部个体
3. **换设定**：加/减固定效应层级、换聚类层级、加时间趋势项
4. **安慰剂**：随机分配处理若干次（500–1000 次），看真实估计值是否落在分布尾部

```stata
* 随机化推断安慰剂
permute treat _b[treat], reps(1000) seed(20260804): reghdfe y treat, absorb(id year)
```

---

## 第 6 步 — 机制与异质性

**机制**：说清楚理论渠道 → 找到渠道变量 M → 做分渠道回归或中介检验。
中介检验（Baron-Kenny 三步）在因果推断里争议大，用之前说明局限，或改用
"处理 → M" 与 "处理 → Y（控制 M 前后）" 的并列呈现。

**异质性**：分组维度必须有**事前**理由。分样本回归后要检验组间系数差异是否显著
（似无相关模型 / 交互项 / bootstrap 组间差）。

不要做完一堆分组只报显著的那几个。做了几组就说几组。

---

## 第 7 步 — 表图产出

表按 `reporting-standards.md`。图**交给 `nature-figure`**，把以下信息传过去：

- 图要传达的结论是什么（一句话）
- 数据来自哪个结果文件
- 图型（事件研究图 / 系数图 / 森林图 / 分组柱状 / 密度重叠图）
- 目标期刊与栏宽、导出格式（PDF/TIFF/SVG）

---

## 第 8 步 — 收尾

**产出物清单**（交付时逐项列出）：

- [ ] 可复现脚本，标明运行顺序与依赖版本
- [ ] 分析样本文件（或从原始数据到分析样本的完整清洗脚本）
- [ ] 表文件（.rtf / .tex / .docx）与图文件（.pdf / .tiff）
- [ ] 每张表/图对应哪段代码的映射说明
- [ ] 结果段落草稿（→ `nature-writing`）
- [ ] 数据可得性声明（→ `nature-data`）
