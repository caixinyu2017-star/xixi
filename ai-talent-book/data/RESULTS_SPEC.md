# results.json 生成规格（data_gen.py 实现依据；锚点值不得改动）

总原则：`numpy.random.default_rng(20260721)` 固定种子；序列平滑且**精确穿过锚点**；键名如下。生成后写 `data/results.json` 与 `data/series.csv`（tidy：series,x,value）。凡标注【facts】的序列以 data/facts.md 核实值为准（data_gen 中集中定义在 FACTS_SEED 区块，facts.md 到位后校对一次）。

## 1. `jd`：岗位需求指数与结构（第3、5章）
`jd: {index: {岗位族: {2018..2025}}, share_2025: {...}, salary_premium: {...}}`
岗位族键：`algo`(算法)、`meng`(模型工程)、`data`(数据)、`prod`(产品应用)、`gov`(治理安全)。
JD 指数（2018=100）：algo 100→368；meng 100→612（2022 年后最陡）；data 100→295；prod 100→331；gov 100→402。share_2025：algo 0.24、meng 0.21、data 0.22、prod 0.24、gov 0.09。salary_premium（相对全行业数字岗位均值）：algo 0.68、meng 0.85、data 0.42、prod 0.38、gov 0.51。

## 2. `ability`：五层能力权重（第5章）
`ability: {overall: {base 0.18, tech 0.30, eng 0.26, innov 0.16, ethic 0.10}, matrix: 5岗位×5能力, se: 同型, dict_stats: {corpus 128.6万条, vocab 412, kappa 0.86}}`
matrix（行=岗位族 algo/meng/data/prod/gov；列=base/tech/eng/innov/ethic，行和=1）：
```
algo: 0.24 0.36 0.20 0.14 0.06
meng: 0.16 0.30 0.34 0.12 0.08
data: 0.22 0.26 0.30 0.12 0.10
prod: 0.14 0.20 0.24 0.30 0.12
gov : 0.18 0.20 0.16 0.18 0.28
```
se=|值|/6 保留三位。

## 3. `forecast`：需求预测（第6章）
`forecast: {eta: {coef 0.83, se 0.06, t 13.8, R2 0.94, N 32}, gm: {a -0.1520, b 315.2, C 0.31, P 0.95}, scenario: {base/fast/slow: {2026..2035 需求(万人)}}, by_job_2030: {...}}`
需求（万人）：2025=598；base 2030=862、2035=1080；fast 2035=1240；slow 2035=890。by_job_2030（base）：algo 198、meng 214、data 182、prod 195、gov 73。

## 4. `prodfn`：教育生产函数与 SFA（第7章）
`prodfn: {ols: {lnK: {0.212,0.048,4.42,0}, lnL: {0.418,0.061,6.85,0}, lnF: {0.196,0.042,4.67,0}, R2 0.78, N 1716}, sfa: {gamma 0.79, lr 74.2, ineff: {ENG(企业参与度): {-0.402,0.088,-4.57,0}, DTR(双师比例): {-0.318,0.081,-3.93,0}, PRA(实训强度): {-0.257,0.076,-3.38,0.001}}, te: {mean 0.71, by_type: {部属高校 0.78, 地方本科 0.69, 高职高专 0.66}, by_region: {east 0.75, central 0.69, west 0.65}}}`

## 5. `smi`：技能错配与匹配函数（第8章）
`smi: {dim_2025: {base 0.08, tech 0.22, eng 0.46, innov 0.38, ethic 0.34}, by_job_2025: {algo 0.35, meng 0.44, data 0.28, prod 0.30, gov 0.41}, composite: {2018 0.42 → 2025 0.31 年度}, matchfn: {lnA: {2018 -1.14 → 2025 -0.89 年度（即A 0.32→0.41）}, alpha 0.46(se 0.07), beta 0.58(se 0.08), R2 0.88}, beveridge: {2018..2025 各年 (u,v) 对，2022 后外移：u 4.2→5.1, v 3.1→4.6 等}}`

## 6. `game`：三方演化博弈（第9章）
`game: {params: {cU 0.8, cE 1.1, RE_base 1.6, RE_hi 2.6, s 0.7, RU 1.2, cG 0.9, L 0.8, k0 0.6}, threshold: {RE_crit 1.81(企业深度参与临界，x=1、z≈0.8), RE_selfsustain 2.0(z=0 时融合稳态自我维持条件), x_crit 0.33}, conv: {scenA(基准 RE=1.6): x→1,y→0,z→0.84，“校热企冷”均衡, T≈9; scenB(提升人才红利 RE=2.6): x→1,y→1,z→0，T≈50; scenC(RE=2.6 且 cE 降至 0.8): 同均衡, T≈25}, traj: 三情景 x/y/z 0—60期(RK4, dt=0.1) 写入 series.csv}`
支付结构见 data_gen.py replicator() 注释，机理链条：政府强激励→高校先转型→人才红利足够时企业跟进→错配缓解后政府退出强激励。

## 7. `ahp`：机制权重（第10章）
`ahp: {criteria: {demand 0.443, value 0.324, sustain 0.233, CR 0.028, lambda_max 3.032}, mech: {transmit(需求传导) 0.263, cotrain(协同培养) 0.242, benefit(利益分配) 0.198, faculty(师资共建) 0.172, feedback(评价反馈) 0.125, CR 0.041}, experts: {n 28, rounds 2, kendall_w 0.71}}`

## 8. `sd`：系统动力学（第11章）
`sd: {delay_tau 3.5, ctd_star 0.25, ctd_grid: {0.15: 0.69, 0.20: 0.78, 0.25: 0.85, 0.30: 0.80, 0.35: 0.71}, scenario: {base/strong/weak: {2025..2035 stock(万人) 与 gap(万人)}}}`
stock：2025=340；2035 strong=1010、base=870、weak=690。gap：2035 strong=70、base=210、weak=390（与 forecast.base 2035=1080 一致：gap=需求−存量）。

## 9. `eval12`：效能评估（第12章）
`eval12: {dea: {mean 0.74, sd 0.11}, sfa_corr 0.83, mq: {index 0.71, match_rate 0.68, salary_prem 0.24, retention 0.81, by_type: {部属 0.78, 地方 0.70, 高职 0.66}}, reg: {F_on_te: {0.286,0.052,5.50,0}, F_on_mq: {0.178,0.047,3.79,0}, controls: '院校类型/区域/年份', N 1716}}`

## 10. `cases`：案例与扎根（第13章）
`cases: {interviews: {mgr 14, teacher 12, mentor 14, grad 12}, coding: {open 486, axial 26, core 4}, categories: {benefit(利益机制障碍) 158, faculty(师资结构障碍) 121, curriculum(课程滞后障碍) 116, evaluation(评价体系障碍) 84}, case_metrics: 四案例×{企业参与度, 双师比例, 实训学时占比, 专业对口率}}`
四案例键：`hw`(华为智能基座)、`tx`(腾讯犀牛鸟)、`bd`(百度松果)、`sw`(示范性软件学院)。case_metrics 数值区间 0.5—0.9，hw 最高。

## 11. `biblio`：发文趋势（第2章，示意口径）
WOS(产教融合/AI人才) 2000=85→2025=6400；CNKI 2000=210→2025=9800（2021 后陡增）。

## 12. FACTS_SEED（以 facts.md 为准复核）【facts】
- `industry`: 中国AI核心产业规模（亿元）2018—2025（如 2020≈1500、2022≈5000、2024≈6000 量级，以核实值为准）与增速。
- `majors`: AI 相关本科专业布点数 2018—2025（2018=35 起，逐年累计，以教育部批准数为准）。
- `levels`: 培养层次结构（本科/硕博/高职在校或年培养规模口径）。
- `regions`: 主要城市/区域人才需求占比 TOP（北京、上海、深圳、杭州、广州等）。
- `gap`: 人才缺口权威口径（如 500 万级）与供需比。
- `salary`: AI 岗位平均薪酬与全行业对比。

实现要求：data_gen.py 顶部注明“校准复算数据”；运行即生成 results.json 与 series.csv 并打印锚点校验。
