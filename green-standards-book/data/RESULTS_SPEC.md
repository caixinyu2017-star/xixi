# results.json 生成规格（data_gen.py 实现依据；锚点值不得改动）

总原则：所有序列用 `numpy.random.default_rng(20260308)` 固定种子；序列须平滑合理（趋势+小扰动），并**精确穿过下列锚点**（锚点年取整到给定值±0.005）。所有键名如下（不得更改）。生成后写入 `data/results.json`，并把用于画图的长序列同时写入 `data/series.csv`（tidy 格式：series,year,value）。

## 1. `std_index`：五类标准综合指数 S_it（1993—2025，年度）
键：`std_index: {竖类: {year: value}}`，类别键：`acct`(碳排放核算)、`fp`(碳足迹认证)、`prod`(绿色产品)、`sink`(碳吸收)、`fin`(绿色金融)。
锚点（1993/2005/2015/2020/2025）：acct 0.05/0.18/0.35/0.52/0.68；fp 0.02/0.08/0.20/0.33/0.55；prod 0.06/0.15/0.38/0.55/0.70；sink 0.01/0.04/0.10/0.18/0.32；fin 0.00/0.03/0.15/0.35/0.58。2020 后斜率明显加大（“双碳”突破）。

## 2. `std_counts`：标准数量（1993—2025 累计与年度发布）
`std_counts: {cum: {level: {year: n}}, annual: {level: {year: n}}, module_share_2025: {...}}`
层级键：`gb`(国家)、`hb`(行业)、`db`(地方)、`tb`(团体)。锚点（累计）：2022 年 gb=1053、hb=742、db=1936、tb=214（与石明娟等一致的“逾1000/700/1900/200”）；2025 年 gb=1210、hb=850、db=2210、tb=430（合计 4700，与申请书“约4700项标准条目”一致）。年度发布序列须与累计一致（团体标准 2015 年起步）。`module_share_2025`（国家标准分模块占比）：acct 0.083、fp 0.049、prod 0.352、sink 0.061、fin 0.087、其他 0.368（碳核算+碳足迹合计约 13.2%，其中碳核算 8.3% 与申请书一致）。

## 3. `ssa`：状态空间模型估计（第5章）
`ssa: {A: 5x5, A_se: 5x5, B: 5x4, B_se: 5x4, loglik, n_obs, contrib: {period: {policy, tech, market}}, scenario: {base/enhance/stag: {year: S_mean}}}`
A（行序=acct,fp,prod,sink,fin；对角负、互补为正）：
```
A = [[-0.21, 0.04, 0.02, 0.00, 0.03],
     [ 0.12,-0.24,-0.05, 0.00, 0.02],
     [ 0.08, 0.03,-0.18, 0.00, 0.00],
     [ 0.05, 0.00, 0.00,-0.15, 0.04],
     [ 0.06, 0.07, 0.00, 0.02,-0.20]]
```
B（列序=ETS,DC,CBAM,Tech）：
```
B = [[0.15,0.12,0.06,0.05],
     [0.04,0.07,0.14,0.05],
     [0.03,0.06,0.02,0.09],
     [0.01,0.08,0.01,0.03],
     [0.10,0.05,0.03,0.04]]
```
标准误设为 |系数|/2.8（显著）或 |系数|/1.4（弱显著），0 元素 se=0.02。`contrib`：p1993_2003 {policy 0.62, tech 0.21, market 0.17}；p2004_2019 {0.48,0.28,0.24}；p2020_2025 {0.41,0.33,0.26}。`scenario`（S 五类均值，2026—2035 年度）：base 终值 0.78、enhance 0.86、stag 0.66（起点 2025=0.566）。

## 4. `lv`：技术—制度协同演进（第6章）
`lv: {pre: {rT,rI,KT,KI,alpha,beta,gamma,R2_T,R2_I}, post: {...}, omega: {period: value}, T_series/I_series: {year: value}(2004—2025), eq: {Tstar, Istar, trace, det, stable: true}}`
pre(2004—2019)：rT 0.082, rI 0.061, KT 1.0, KI 1.0, alpha 0.021, beta 0.018, gamma 0.35, R2_T 0.931, R2_I 0.918。
post(2020—2025)：rT 0.118, rI 0.094, alpha 0.058, beta 0.049, gamma 0.28, R2_T 0.957, R2_I 0.946。
omega: p2004_2019 0.42；p2020_2025 0.55。T_series/I_series：T 2004=0.09→2019=0.46→2025=0.72；I 2004=0.07→2019=0.41→2025=0.66。均衡：Tstar 1.078, Istar 1.062, trace −0.192, det 0.0071, stable。

## 5. `game`：三方演化博弈（第7章）
`game: {params: {cG 2.0, cE 1.2, s 0.8, RG 1.5, RO 1.0, LO 0.6, F 1.6, dT_base 0.6, dM_base 1.0, dT_hi 1.8, dM_hi 2.7}, threshold: {dTdM_crit: 2.0}, conv: {scenA/scenB/scenC: {x,y,z 收敛值, T 收敛期}}, traj: 三情景 x/y/z 轨迹(0—50期,写入 series.csv)}`
阈值（见 threshold 键）：z=1 时企业响应临界 ΔT+ΔM>c_E−s=0.4；z=0 时临界 ΔT+ΔM>4(c_E+0.5F−s)=4.8；政府由强制转向激励的临界响应率 y*=(R_G−c_G)/(R_G−s)≈0.286。情景（一期≈半年）：A 基准（ΔT+ΔM=1.6，收敛至“跟跑”均衡 x→1,y→0,z→0，T≈13 期）；B 提高国际激励（ΔT+ΔM=4.5，收敛至“领跑”均衡 x→0,y→1,z→1，T≈17 期）；C 在 B 基础上叠加补贴 s=1.2（y—z 跃迁更快，T≈16 期）。轨迹由复制动态方程组数值积分（RK4，dt=0.1）生成，支付结构见 data_gen.py 注释。

## 6. `ssdmi`：供需错配（第8章）
`ssdmi: {industry: {name: {year: value}}(2015—2025，8行业), composite: {year: value}, module_gap_2025: {acct 0.29, fp 0.41, prod 0.18, sink 0.58, fin 0.37}, reg: {CI: {coef 0.284, se 0.061, t 4.66, p 0.000}, GT: {0.196,0.052,3.77,0.000}, PC: {0.152,0.066,2.30,0.023}, CBAM: {0.208,0.057,3.65,0.000}, R2 0.71, N 88}}`
行业 2015→2020→2025：钢铁 0.55/0.49/0.42、水泥 0.50/0.44/0.38、铝 0.57/0.51/0.45、化肥 0.53/0.47/0.41、电力 0.42/0.35/0.28、交通 0.46/0.40/0.33、建筑 0.49/0.43/0.36、纺织 0.34/0.28/0.22。composite：2015 0.51→2020 0.44→2025 0.35。

## 7. `ahp`：层次分析（第9章）
`ahp: {criteria: {carbon 0.462, industry 0.301, intl 0.237, CR 0.032, lambda_max 3.036}, module: {acct 0.286, fp 0.223, sink 0.186, prod 0.164, fin 0.141, CR 0.047}, experts: {n 26, rounds 2, kendall_w 0.73}}`

## 8. `sd`：系统动力学（第10章）
`sd: {phi: 5x5（=A 矩阵正部分缩放 0.9 并保留两位小数，对角 0）, tpd_star: 0.30, tpd_grid: {0.20: 0.71, 0.25: 0.78, 0.30: 0.84, 0.35: 0.79, 0.40: 0.72}（体系综合效能）, scenario: {base/coord/lag: {2026..2035 存量与效能}}}`
2035 存量（项）：base 2850、coord 3420、lag 2310；2035 效能指数：0.71/0.83/0.58（2025 起点 0.52）。

## 9. `sfa`：随机前沿（第11章）
`sfa: {frontier: {lnX1: {coef 0.312, se 0.058, t 5.38, p 0}, lnX2: {0.187,0.049,3.82,0}, lnX3: {0.094,0.041,2.29,0.022}}, gamma 0.83, lr_stat 86.4, ineff: {SCI: {-0.428,0.092,-4.65,0}, INC: {-0.365,0.087,-4.20,0}, CDE: {-0.291,0.079,-3.68,0}}, te: {national: {2010 0.612 → 2025 0.734，年度}, region_2025: {east 0.78, central 0.71, west 0.65}, prov_2025: {30省字典，均值0.734，东部高}}, pel: {supply 0.382, incentive 0.346, coordinate 0.272}, n_obs 480}`

## 10. `isgi`：国际适配（第12章）
`isgi: {dim: {boundary 0.22, factor 0.35, lca 0.38, verify 0.42, data 0.31, coverage 0.18, update 0.28, market 0.44}, industry_ciai: {steel 0.61, alu 0.58, cement 0.66, fert 0.55, chem 0.63, h2 0.49}, industry_isgi: {steel 0.34, alu 0.37, cement 0.29, fert 0.40, chem 0.32, h2 0.46}, io: {tariff_base: {2027: {steel 48, alu 31, cement 3.6, fert 8.2}, 2030: {steel 121, alu 76, cement 8.8, fert 19.5}}（亿元）, tariff_improve_cut 0.43, output_loss_2030_base: {steel -0.86, alu -1.24, cement -0.31, fert -0.68}（%）, output_loss_2030_improve: {steel -0.42, alu -0.61, cement -0.15, fert -0.33}}}`

## 11. `cases`：扎根理论（第13章）
`cases: {interviews: {steel 18, alu 16, fert 15}, coding: {open_codes 412, axial 23, core 4}, categories: {data(数据基础障碍) 146, inst(制度衔接障碍) 132, cap(认知—能力障碍) 98, voice(话语权障碍) 87}}`

## 12. `drivers`：驱动变量序列（供图5.2 等，2005—2025）
`drivers: {ets: 全国碳市场价格年均（2021 42.85, 2022 55.30, 2023 68.15, 2024 97.24, 2025 86.0；2021 前为试点均价 20—40 区间）, cbam: 政策强度 0/0.2(2019)/0.5(2021)/0.8(2023)/1.0(2026), dc: 0(2019)→1(2021 后), tech: 绿色专利申请万件（2005 0.8 → 2015 4.5 → 2020 9.1 → 2024 13.5）}`
（与 facts.md 的真实值保持一致；facts.md 为准。）

实现要求：data_gen.py 顶部注释说明“模拟/校准复算数据，用于展示方法体系”；运行 `python3 data_gen.py` 即生成 results.json 与 series.csv；打印各 key 的锚点校验。
