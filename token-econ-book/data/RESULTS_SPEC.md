# results.json 生成规格（data_gen.py 实现依据；锚点值不得改动）

总原则：`numpy.random.default_rng(20260813)` 固定种子；序列平滑且**精确穿过锚点**；生成后写 `data/results.json` 与 `data/series.csv`（tidy：series,x,value）并打印锚点校验。凡标注【facts】的以 `data/facts.md` 核实值为准（集中在 FACTS_SEED 区块）。

**模型命名纪律**：一律使用**档位名**而非真实产品名（避免把校准复算值挂到具体商业产品上）。六档：`light`（轻量蒸馏级）、`mid`（中型通用级，**基准档，η≡1**）、`open`（开源旗舰级）、`flag`（旗舰闭源级）、`reason`（推理增强级）、`multi`（多模态级）。

---

## 1. `ste`：标准词元效值折算（第5章，全书基石）
`ste: {base: 'mid', dims: {档位: {P, R, S, eta}}, weights: {wP 0.42, wR 0.38, wS 0.20}, ces_rho -0.35, fit: {R2 0.91, N 1240, rmse 0.087}, dispersion: {...}}`

三维效值（相对基准档 mid≡1）与合成效值系数 η（CES 合成，见式 5-5）：

| 档位 | P 算力强度 | R 推理质量 | S 场景效用 | η |
|---|---|---|---|---|
| light | 0.22 | 0.46 | 0.68 | **0.38** |
| mid | 1.00 | 1.00 | 1.00 | **1.00** |
| open | 2.60 | 1.72 | 1.34 | **1.96** |
| flag | 4.80 | 2.35 | 1.66 | **2.94** |
| reason | 8.40 | 3.10 | 1.92 | **4.28** |
| multi | 3.70 | 1.88 | 2.15 | **2.62** |

**离散度对照（第5章核心发现）**：折算前后单位价格的变异系数
`dispersion: {price_cv_raw 0.92, price_cv_ste 0.31, gini_raw 0.47, gini_ste 0.17, spread_raw 12.6, spread_ste 2.4}`
（spread＝最高／最低倍数；折算后价格离散度下降约三分之二，趋近一价定律。）

## 2. `usage`：调用量与场景结构（第4章）【部分 facts】
`usage: {daily_tokens: {2024Q1 …2026Q2 日均万亿枚}, by_scene: {agent_coding 0.812, chat 0.086, content 0.058, other 0.044}, app_share: {agent_coding 0.19}, cn_share_openrouter: {周度序列}}`
日均调用量（万亿枚）锚点：2024Q1 = 0.10；2024Q4 = 3.6；2025Q2 = 18；2025Q4 = 62；2026Q2 = 155；2026Q3 = 180。

## 3. `price`：价格结构与指数（第7章）
`price: {layers: {档位: {floor, eta_premium, scene_rent, market}}, tpi: {2024Q1…2026Q2}, stpi: {同期}, decomp: {pure_price_cut, eta_gain}, elasticity: {coef -1.34, se 0.19, t -7.05, R2 0.83, N 864}, tier: {inclusive, ondemand, custom}}`

**三层价格结构（元／百万物理词元，2026Q2）**：
| 档位 | 成本底价 floor | 效值溢价 | 场景租金 | 市场价 |
|---|---|---|---|---|
| light | 0.18 | 0.09 | 0.13 | 0.40 |
| mid | 0.52 | 0.34 | 0.44 | 1.30 |
| open | 1.05 | 0.98 | 1.27 | 3.30 |
| flag | 1.94 | 2.16 | 2.90 | 7.00 |
| reason | 3.36 | 4.42 | 6.22 | 14.00 |
| multi | 1.48 | 1.36 | 2.16 | 5.00 |

**价格指数（2024Q1＝100，季度）**：
- TPI（物理词元价格指数）：2024Q1 100 → 2024Q4 62 → 2025Q2 41 → 2025Q4 29 → 2026Q2 **21**
- STPI（标准词元价格指数）：2024Q1 100 → 2024Q4 78 → 2025Q2 63 → 2025Q4 54 → 2026Q2 **47**
- 分解（2024Q1—2026Q2 累计降幅 79%）：`decomp: {eta_gain 0.53, pure_price_cut 0.47}`——即表观降价中约 53% 来自效值提升（同价买到更强词元）、约 47% 为真实降价。
- 需求价格弹性 −1.34（稳健区间 −1.52—−1.16）；分行业：制造 −1.62、金融 −0.94、文化传媒 −1.71、政务 −0.68。
- 三级服务（第7.4节）：普惠包 单价 0.9 折、按需套餐 1.0、专属定制 1.6；对应用户占比 0.62/0.31/0.07，收入占比 0.21/0.38/0.41。

## 4. `market`：市场结构与均衡（第8章）
`market: {hhi: {2024 0.34 → 2026 0.21 年度}, supply: {档位: {capacity, mc, ac}}, entry: {sunk_cost, mes}, lemon: {info_gap 0.44, adverse_share 0.27}}`
- 集中度 HHI（模型服务市场）：2024 0.34、2025 0.27、2026 0.21（趋于竞争）。
- 词元工厂：规模最小有效产能 MES 对应日产 1.2 亿标准词元；长期平均成本在 MES 处为 0.61 元/百万 STE。
- 效值信息不对称：企业对所购词元效值的认知偏差均值 0.44（低估高效值档位），导致低效值档位过度采购份额 0.27。

## 5. `eff`：算力—词元转化效率（第9章）
`eff: {theta: {档位: STE per PFLOPS·h}, nominal_util 0.62, losses: {idle 0.18, batch 0.09, match 0.12, value 0.07}, effective_util 0.38, sched: {matched_util 0.54, gain 0.16, upper_bound 0.61}, queue: {lambda, nu, wait_ms}}`
- 名义算力利用率 0.62；四项损失：空转 0.18、批次 0.09、匹配 0.12、效值 0.07；**有效效值利用率 0.38**。
- 统一调度（任务—模型最优匹配）后 0.54，改进 +0.16 个百分点单位（相对提升 42%）；理论上界 0.61。
- 排队：到达率 λ＝420 请求/秒、服务率 ν＝480、平均等待 96 ms、P95 时延 310 ms。
- 转化效率 θ（万 STE per PFLOPS·h）：light 42.0、mid 18.5、open 9.2、flag 5.4、reason 3.1、multi 6.8。

## 6. `game`：平台—企业—政府三方演化博弈（第10章）
`game: {params: {cP 0.9, cF 1.0, RP 1.3, RF_base 1.5, RF_hi 2.5, s 0.6, cG 0.8, L 0.9, k0 0.55, tau_save 0.35}, threshold: {RF_crit 1.78, RF_selfsustain 2.1, x_crit 0.30}, conv: {scenA, scenB, scenC}, traj: 0—60期 RK4 dt=0.1}`
- 策略：$x$ 平台深度运营（建统一计量结算与调度）、$y$ 企业深度采纳（把词元嵌入主业务流）、$z$ 政府强激励（技改补贴＋政策抵扣）。
- 机理链条：**政府强激励→平台先行建设统一入口（交易费用节约 τ=0.35）→企业采纳收益越过阈值后跟进→采纳规模化后政府退出强激励**。
- 情景 A（基准 RF=1.5）：收敛于「平台热、企业冷」，x→1、y→0.005、z→0.82，T≈10。
- 情景 B（RF=2.5，效值透明＋场景深化）：x→1、y→0.97、z→0，T≈52。
- 情景 C（RF=2.5 且 cF 降至 0.7，统一接入降低企业采纳成本）：同均衡，T≈24。

## 7. `ahp`：制度要件权重（第10章）
`ahp: {criteria: {efficiency 0.412, fairness 0.318, sustain 0.270, CR 0.031, lambda_max 3.036}, items: {metering(统一计量) 0.271, settlement(统一结算) 0.223, entry(统一入口) 0.196, audit(统一安全审计) 0.166, subsidy(统一政策抵扣) 0.144, CR 0.038}, experts: {n 26, rounds 2, kendall_w 0.69}}`

## 8. `green`：绿色词元（第11章）
`green: {energy: {档位: kWh per 百万 STE}, carbon: {grid_factor 0.53, green_factor 0.04, iota_avg 218, iota_green 41}, mix: {2024 0.28 → 2026 0.44 绿电占比}, premium: {coef 0.083, se 0.021, t 3.95, N 612}, scenario: {base/green/deep 2026—2035 碳强度}}`
- 每百万标准词元耗电（kWh）：light 0.9、mid 2.6、open 5.4、flag 9.8、reason 17.2、multi 7.1。
- 电网排放因子 0.53 kgCO₂/kWh，绿电 0.04；平均碳强度 218 gCO₂e/千 STE，绿色词元 41。
- 绿色词元溢价：出海导向企业支付意愿溢价系数 0.083（8.3%），显著。
- 碳强度情景（gCO₂e/kSTE）：2026 = 218；2035 基准 126、绿色 62、深度 34。

## 9. `growth`：增长贡献核算（第12章）
`growth: {prodfn: {lnK 0.318, lnL 0.276, lnD 0.094, lnT 0.108, R2 0.86, N 1240}, decomp: {年份: {gY, cK, cL, cD, cT, tfp}}, tfp_bias: {without_token 2.41, with_token 2.12, overstate 0.29}, region: {east/central/west 贡献率}}`
- 生产函数弹性：资本 0.318、劳动 0.276、数据 0.094、**标准词元流量 0.108**（均 1% 水平显著）。
- 2026 年词元流量对产出增长的直接贡献 0.34 个百分点，占实际增长率的 **6.8%**；2024 年仅 0.06 个百分点、占 1.2%。
- 不引入词元变量时 TFP 残差为 2.41%，引入后降至 2.12%，**残差高估 0.29 个百分点**（与 Jorgenson 资本服务测度的启示同构）。
- 区域贡献率：东部 8.4%、中部 5.1%、西部 3.6%。

## 10. `cases`：案例与扎根（第13章）
`cases: {cities: {jx/sz/wz/gz/sh: {主体类型, 启动时间, 模式特征, 五项能力评分}}, interviews: {platform 12, enterprise 18, govt 9, vendor 8}, coding: {open 412, axial 23, core 4}, categories: {metering(计量不透明) 143, cost(成本不确定) 118, capability(能力缺口) 97, trust(合规与安全顾虑) 76}}`
- 五城五项能力评分（0—1）：接入便利、计量透明、成本可控、合规可信、生态丰度——嘉兴以统一计量与结算见长、苏州以出海服务见长、温州以绿色凭证见长、广州以交易组织见长、上海以政策工具见长。

## 11. `biblio`：发文趋势（第2章，示意口径）
WOS（AI economics/token economy）2015=180→2026=5600；CNKI（数字经济＋算力＋词元）2015=420→2026=8900（2023 后陡增）。

## 12. FACTS_SEED（以 facts.md 为准复核）【facts】
- `daily_call`：日均词元调用量分时点值；`price_api`：主流模型 API 价格对比；`util_idc`：IDC 利用率分布；`silicon`：Token 支出指数；`cities`：五城运营中心要素；`jiaxing`：嘉兴算力与产业底数；`openrouter`：模型周用量与中国模型份额。
