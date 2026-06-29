# db04 数据集卡 — 统计 / 经济金融 / 社会科学

> schema: `dataset_name, domain, task, data_type, size, format, license, download_url, paper_url, citation, leaderboard_url, known_issues, bias_risk, privacy_risk, preprocessing_steps, recommended_splits`
> 可核查字段来自 OpenAlex 真实查询（2026-06-10）；金融商业数据库若需订阅/授权，必须写明，不把“可访问”误写成“可公开再分发”。

```yaml
- dataset_name: FRED-MD / FRED-QD
  domain: 宏观经济 / 时间序列
  task: 宏观预测、nowcasting、因子模型、VAR/机器学习预测比较
  data_type: 月度/季度宏观经济指标面板(产出、就业、价格、货币、利率等)
  size: FRED-MD 百余月度变量；FRED-QD 数百季度变量（随版本更新）
  format: CSV / Excel / ALFRED/FRED 数据接口
  license: Federal Reserve/FRED 数据多数公开；再分发和商用需遵守 FRED/来源机构条款
  download_url: https://research.stlouisfed.org/econ/mccracken/fred-databases/
  paper_url: https://doi.org/10.1080/07350015.2015.1086655 ; https://doi.org/10.3386/w26872
  citation: |
    FRED-MD: A Monthly Database for Macroeconomic Research | 2015 | cited:888 | doi:10.1080/07350015.2015.1086655
    FRED-QD: A Quarterly Database for Macroeconomic Research | 2020 | cited:100 | doi:10.3386/w26872
    [last_checked=待核; 锚点已内联 doi:/cited:,被引实时查见 dataset_signal.py]
  leaderboard_url: 无统一官方榜
  known_issues: 变量会修订；季节调整/转换代码必须固定；实时预测需使用 vintages 避免未来修订泄漏; domain_scope=经济
  bias_risk: 中 — 以美国宏观经济为主，跨国泛化有限
  privacy_risk: 无
  preprocessing_steps: 按论文 transformation code 平稳化；记录 vintage；缺失填补；时间滚动 split
  recommended_splits: expanding/rolling window；若做实时预测，用 ALFRED vintage split

- dataset_name: Penn World Table (PWT)
  domain: 国际宏观 / 增长经济学
  task: 跨国经济增长、生产率、资本存量、收入水平比较
  data_type: 国家-年份面板，GDP、资本、就业、TFP、价格水平等
  size: 180+ 国家/地区 × 1950 后年度数据（版本不同）
  format: Excel / CSV / R pwt 包
  license: Groningen Growth and Development Centre 数据条款；学术使用需引用，商用/再分发需核实
  download_url: https://www.rug.nl/ggdc/productivity/pwt/
  paper_url: https://doi.org/10.1257/aer.20130954
  citation: "The Next Generation of the Penn World Table | 2015 | cited:4710 | doi:10.1257/aer.20130954; last_checked=待核; doi=10.1257/aer.20130954"
  leaderboard_url: 无
  known_issues: 购买力平价与国民账户修订导致版本差异；缺失国家/年份；跨国可比性受统计体系影响; domain_scope=经济
  bias_risk: 中 — 低收入国家统计质量不均，历史数据不确定性高
  privacy_risk: 无
  preprocessing_steps: 固定 PWT 版本；国家代码对齐；处理缺失/异常；按国家或时间留出验证
  recommended_splits: country-disjoint 或 time-forward split；报告 PWT version

- dataset_name: World Bank World Development Indicators (WDI)
  domain: 发展经济学 / 国际比较
  task: 发展指标建模、政策评估协变量、国家层面描述性统计
  data_type: 国家-年份面板，人口、教育、健康、贸易、贫困、环境等指标
  size: 数千指标 × 200+ 经济体 × 多年
  format: API / CSV / bulk download
  license: World Bank Open Data 多数 CC BY 4.0；具体指标可能有来源限制，使用前核实
  download_url: "https://databank.worldbank.org/source/world-development-indicators ; API: https://api.worldbank.org/"
  paper_url: https://doi.org/10.1596/978-1-4648-0484-7_world_development_indicators
  citation: "World Development Indicators | 2015 | cited:760 | doi:10.1596/978-1-4648-0484-7_world_development_indicators; last_checked=待核; doi=10.1596/978-1-4648-0484-7_world_development_indicators"
  leaderboard_url: 无
  known_issues: 缺失严重、指标定义变更、国家边界/代码变化；不同来源统计口径不一; domain_scope=经济
  bias_risk: 中 — 国家统计能力差异导致测量偏差
  privacy_risk: 无（聚合国家级）
  preprocessing_steps: 指标筛选；缺失率阈值；国家代码标准化；固定下载日期；避免用未来年份协变量
  recommended_splits: time-forward split 或 country-group split；政策研究按设计定义处理/对照

- dataset_name: Fama-French 因子库
  domain: 金融资产定价 / 股票收益
  task: 因子模型、资产定价检验、组合收益解释、风险调整
  data_type: 市场/规模/价值/盈利/投资等因子收益，组合收益
  size: 月度/日度因子与组合，时间跨度随地区/版本
  format: CSV/TXT ZIP
  license: Kenneth French Data Library 免费公开；再分发/商用需核对网站条款并引用
  download_url: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
  paper_url: https://doi.org/10.1016/0304-405x(93)90023-5
  citation: "Common risk factors in the returns on stocks and bonds | 1993 | cited:27629 | doi:10.1016/0304-405x(93)90023-5; last_checked=待核; doi=10.1016/0304-405x(93)90023-5"
  leaderboard_url: 无
  known_issues: 因子构造更新；幸存者/数据清洗细节依赖 CRSP/Compustat；国际市场覆盖不均; domain_scope=金融-特定市场
  bias_risk: 中 — 美股研究最充分，跨市场泛化需谨慎
  privacy_risk: 无（公开市场聚合数据）
  preprocessing_steps: 统一频率；处理百分比单位；对齐无风险利率；避免 look-ahead；记录下载日期
  recommended_splits: time-series rolling/expanding split；危机期单独外推验证

- dataset_name: CRSP / Compustat / WRDS 金融数据库
  domain: 金融市场 / 公司财务
  task: 股票收益预测、事件研究、资产定价、公司财务实证
  data_type: 股票价格/收益/成交量、公司财务报表、标识符映射
  size: 大型商业数据库，按订阅模块与时间范围变化
  format: WRDS SQL/SAS/CSV 导出
  license: 商业/机构订阅，严格禁止未授权再分发；仅授权用户按协议使用
  download_url: https://wrds-www.wharton.upenn.edu/
  paper_url: 待核查（数据库本身无单一论文；使用时引用 CRSP/Compustat/WRDS 与具体研究）
  citation: |
    A First Look at the Accuracy of the CRSP Mutual Fund Database and a Comparison of the CRSP and Morningstar Mutual Fund Databases | 2001 | cited:419 | doi:10.1111/0022-1082.00410
    注：这是 CRSP 相关核查文献示例，非数据库唯一引用。
    [last_checked=待核; 锚点已内联 doi:/cited:,被引实时查见 dataset_signal.py]
  leaderboard_url: 无
  known_issues: PERMNO/GVKEY/link table 对齐复杂；退市收益、幸存者偏差、公告日期与可得日期必须处理; domain_scope=金融-特定市场
  bias_risk: 中 — 覆盖上市公司/美股为主，私营企业与小市场不足
  privacy_risk: 低 — 市场/公司数据为商业授权数据，但非个人隐私为主
  preprocessing_steps: 使用 CCM link table；加入 delisting returns；按可得日期滞后财务变量；保留查询 SQL 与日期
  recommended_splits: time-forward split；按公司/行业聚类稳健标准误；事件研究按事件窗口

- dataset_name: OECD Data / Product Market Regulation / Employment Protection
  domain: 国际政策 / 制度指标
  task: 跨国政策比较、制度强度指标、宏观/劳动市场实证协变量
  data_type: 国家-年份政策指标、监管强度、就业保护、产业/市场指标
  size: 按 OECD 数据集变化，通常几十国家 × 多年 × 多指标
  format: OECD API / CSV / SDMX
  license: OECD 数据条款；多数可用于研究并需引用，商用/再分发需核实
  download_url: https://data-explorer.oecd.org/ ; https://www.oecd.org/economy/reform/indicators-of-product-market-regulation/
  paper_url: https://doi.org/10.2139/ssrn.201668
  citation: "Summary Indicators of Product Market Regulation with an Extension to Employment Protection Legislation | 2000 | cited:474 | doi:10.2139/ssrn.201668; last_checked=待核; doi=10.2139/ssrn.201668"
  leaderboard_url: 无
  known_issues: 指标定义和方法随版本更新；非 OECD 国家覆盖有限；政策指标可能主观/离散; domain_scope=通用
  bias_risk: 中 — 发达经济体覆盖更好，制度指标跨国可比性有限
  privacy_risk: 无（国家/制度级）
  preprocessing_steps: 固定指标版本；国家代码/年份对齐；处理断点；与 WDI/PWT 合并时记录 merge 规则
  recommended_splits: country/time panel split；政策研究按理论定义 treatment 与 timing
```
