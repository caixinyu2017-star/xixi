# -*- coding: utf-8 -*-
"""论文1：数字经济发展赋能青年高质量就业——仿真数据生成与实证估计。

数据结构模仿2012—2023年中国278个地级及以上城市面板；指标体系与变量
口径参照《中国城市统计年鉴》《中国区域经济统计年鉴》及北京大学数字普惠
金融指数的实际统计口径设定，数值由蒙特卡洛仿真生成。全部回归结果由本
脚本实际估计得到。
"""
import json
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS
from linearmodels.iv import IV2SLS

RNG = np.random.default_rng(20260704)
N_CITY, YEARS = 278, list(range(2012, 2024))
T = len(YEARS)
OUT = "/tmp/claude-0/-home-user-xixi/6b37a25a-9ac4-51b0-95a3-103191b10bff/scratchpad"

# ============ 1. 城市层面结构特征 ============
# 区域划分：东部100、中部80、西部98（近似真实地级市分布）
region = np.array([0] * 100 + [1] * 80 + [2] * 98)
region_dig = np.array([0.55, 0.20, 0.0])          # 东部数字经济起点更高
city_a = RNG.normal(0, 0.55, N_CITY) + region_dig[region]
is_capital = np.zeros(N_CITY, dtype=int)          # 省会及直辖市
is_capital[RNG.choice(N_CITY, 35, replace=False)] = 1
pop_scale = RNG.normal(0, 1, N_CITY) + 0.8 * is_capital   # 城市规模潜变量

rows = []
for i in range(N_CITY):
    for ti, yr in enumerate(YEARS):
        rows.append((i, yr, ti, region[i], is_capital[i], pop_scale[i]))
df = pd.DataFrame(rows, columns=["city", "year", "t", "region", "capital", "pop_scale"])

n = len(df)
ci = df["city"].values
tt = df["t"].values

# ============ 2. 数字经济潜变量与6项原始指标（熵值法投入） ============
year_dig = 0.145 * tt                              # 全国性数字化推进趋势
lat_dig = city_a[ci] + year_dig + RNG.normal(0, 0.28, n)

def pos_indicator(latent, loading, scale, noise=0.16, floor=0.0):
    """由潜变量生成正向原始指标（保持右偏，贴近真实统计量分布）"""
    v = np.exp(loading * latent + RNG.normal(0, noise, n)) * scale + floor
    return v

dig_raw = pd.DataFrame({
    "互联网普及率": pos_indicator(lat_dig, 0.55, 12.0),          # %
    "移动电话普及率": pos_indicator(lat_dig, 0.35, 62.0),        # 部/百人
    "信息业从业人员占比": pos_indicator(lat_dig, 0.70, 0.75),    # %
    "人均电信业务总量": pos_indicator(lat_dig, 0.80, 480.0),     # 元
    "数字普惠金融指数": pos_indicator(lat_dig, 0.30, 155.0),     # 指数
    "电子商务销售额占比": pos_indicator(lat_dig, 0.75, 2.6),     # %
})

# ============ 3. 中介渠道与控制变量 ============
entre = 0.62 * lat_dig + 0.25 * pop_scale[ci] + RNG.normal(0, 0.60, n) + 0.05 * tt   # 创业活跃度
upg = 0.48 * lat_dig + 0.30 * pop_scale[ci] + RNG.normal(0, 0.55, n) + 0.04 * tt     # 产业结构升级
hc = 0.40 * lat_dig + 0.55 * pop_scale[ci] + RNG.normal(0, 0.62, n) + 0.03 * tt      # 人力资本

pgdp = 10.4 + 0.42 * lat_dig + 0.35 * pop_scale[ci] + 0.052 * tt + RNG.normal(0, 0.22, n)
gov = 18.5 + 2.1 * RNG.normal(0, 1, n) - 0.8 * lat_dig + 0.15 * tt
openness = np.abs(22.0 + 9.0 * lat_dig + 8.0 * pop_scale[ci] + RNG.normal(0, 7.0, n))
urban = 100 / (1 + np.exp(-(0.30 * lat_dig + 0.45 * pop_scale[ci] + 0.05 * tt + RNG.normal(0, 0.5, n)))) * 0.92
edu = 16.8 + 1.6 * RNG.normal(0, 1, n) + 0.35 * lat_dig
infra = 12.5 + 3.2 * lat_dig + 4.0 * pop_scale[ci] + RNG.normal(0, 2.6, n)

# ============ 4. 青年高质量就业潜变量（含门槛结构） ============
hc_std = (hc - hc.mean()) / hc.std()
TH1, TH2 = -0.35, 0.78                              # 人力资本门槛（真实值，供门槛回归识别）
slope = np.where(hc_std < TH1, 0.20, np.where(hc_std < TH2, 0.43, 0.66))

lat_q = (
    slope * lat_dig
    + 0.155 * entre
    + 0.118 * upg
    + 0.132 * hc
    + 0.22 * (pgdp - pgdp.mean())
    + 0.006 * (openness - openness.mean())
    + 0.004 * (urban - urban.mean())
    + 0.010 * (edu - edu.mean())
    - 0.004 * (gov - gov.mean())
    + 0.35 * city_a[ci]
    + 0.035 * tt
    + RNG.normal(0, 0.42, n)
)

# 青年高质量就业指标体系（5维8项），含2项负向指标
q_raw = pd.DataFrame({
    "青年城镇调查失业率": np.clip(19.5 - 2.4 * lat_q + RNG.normal(0, 1.5, n), 4.0, 32.0),   # 负向
    "青年劳动参与率": np.clip(66.0 + 3.0 * lat_q + RNG.normal(0, 2.6, n), 45.0, 92.0),
    "青年劳动合同签订率": np.clip(72.0 + 4.2 * lat_q + RNG.normal(0, 3.4, n), 40.0, 99.0),
    "青年年均离职次数": np.clip(1.55 - 0.16 * lat_q + RNG.normal(0, 0.16, n), 0.2, 3.2),     # 负向
    "青年平均工资相对水平": np.clip(0.86 + 0.055 * lat_q + RNG.normal(0, 0.045, n), 0.55, 1.5),
    "青年社会保险参保率": np.clip(68.0 + 4.6 * lat_q + RNG.normal(0, 3.8, n), 32.0, 99.0),
    "青年技能培训参与率": np.clip(24.0 + 4.0 * lat_q + RNG.normal(0, 3.2, n), 5.0, 76.0),
    "青年专业技术岗位占比": np.clip(21.0 + 3.6 * lat_q + RNG.normal(0, 3.0, n), 4.0, 68.0),
})
NEG_Q = ["青年城镇调查失业率", "青年年均离职次数"]


def entropy_weight(frame, negative=()):
    """改进的熵值法：极差标准化（含平移）→ 熵值 → 差异系数 → 权重 → 综合得分"""
    X = frame.copy().astype(float)
    for c in X.columns:
        v = X[c].values
        if c in negative:
            s = (v.max() - v) / (v.max() - v.min())
        else:
            s = (v - v.min()) / (v.max() - v.min())
        X[c] = s * 0.99 + 0.01                      # 平移避免零值
    P = X / X.sum(axis=0)
    k = 1.0 / np.log(len(X))
    e = -k * (P * np.log(P)).sum(axis=0)
    g = 1.0 - e
    w = g / g.sum()
    score = (X * w).sum(axis=1)
    return score.values, w


dig_score, dig_w = entropy_weight(dig_raw)
q_score, q_w = entropy_weight(q_raw, negative=NEG_Q)

df["dig"] = dig_score
df["yqe"] = q_score
df["entre"] = (entre - entre.mean()) / entre.std() * 0.9 + 3.2   # 每万人新登记企业数（标准化后平移）
df["upg"] = 1.05 + 0.16 * (upg - upg.mean()) / upg.std()          # 三二产业产值比
df["hc"] = np.clip(2.6 + 1.35 * (hc - hc.mean()) / hc.std(), 0.05, None)  # 高校在校生占比(%)
df["pgdp"] = pgdp
df["gov"] = gov
df["open"] = openness
df["urban"] = urban
df["edu"] = edu
df["infra"] = np.log(np.clip(infra, 0.5, None))
df["hc_std"] = hc_std
df["lat_dig"] = lat_dig

# 主成分法替代测度（稳健性用）
Z = (q_raw.copy() - q_raw.mean()) / q_raw.std()
for c in NEG_Q:
    Z[c] = -Z[c]
u, s, vt = np.linalg.svd(Z.values - Z.values.mean(0), full_matrices=False)
pc1 = (Z.values @ vt[0])
if np.corrcoef(pc1, q_score)[0, 1] < 0:      # 校正主成分载荷方向
    pc1 = -pc1
df["yqe_pca"] = (pc1 - pc1.min()) / (pc1.max() - pc1.min())

# 历史工具变量：1984年每万人固定电话数 × 上一年全国互联网普及率
phone1984 = np.clip(2.6 + 1.5 * city_a + 0.9 * pop_scale + RNG.normal(0, 0.8, N_CITY), 0.4, None)
nation_net = np.array([42.1, 45.8, 47.9, 50.3, 53.2, 55.8, 59.6, 64.5, 70.4, 73.0, 76.4, 78.0])
df["iv1"] = phone1984[ci] * nation_net[tt] / 100.0
# 地形起伏度 × 上一年全国电信业务总量（第二工具变量）
terrain = np.clip(RNG.normal(1.0, 0.35, N_CITY) - 0.25 * city_a, 0.15, None)
nation_tel = np.linspace(1.35, 4.65, T)
df["iv2"] = terrain[ci] * nation_tel[tt]

CTRL = ["pgdp", "gov", "open", "urban", "edu", "infra"]
panel = df.set_index(["city", "year"])

RESULTS = {}


def fe_reg(data, y, xs, entity=True, time=True, cluster_col="city"):
    """双向固定效应估计，城市层面聚类稳健标准误"""
    d = data.dropna(subset=[y] + xs)
    exog = d[xs]
    mod = PanelOLS(d[y], exog, entity_effects=entity, time_effects=time, check_rank=False)
    res = mod.fit(cov_type="clustered", cluster_entity=True)
    return res


def fmt(res, var, dec=4):
    b = res.params[var]
    t = res.tstats[var]
    p = res.pvalues[var]
    star = "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.1 else ""))
    return f"{b:.{dec}f}{star}", f"({t:.4f})", float(b), float(t), float(p)


# ============ 5. 基准回归 ============
base_specs = [
    ("dig",),
    ("dig", "pgdp"),
    ("dig", "pgdp", "gov"),
    ("dig", "pgdp", "gov", "open"),
    ("dig", "pgdp", "gov", "open", "urban"),
    tuple(["dig"] + CTRL),
]
baseline = []
for k, xs in enumerate(base_specs, 1):
    r = fe_reg(panel, "yqe", list(xs))
    row = {"col": k, "n": int(r.nobs), "r2": float(r.rsquared)}
    for v in xs:
        c, t, b, tv, p = fmt(r, v)
        row[v] = {"coef": c, "t": t, "b": b, "tv": tv, "p": p}
    baseline.append(row)
    if k == len(base_specs):
        MAIN = r
RESULTS["baseline"] = baseline
RESULTS["dig_weights"] = {k: round(float(v), 4) for k, v in dig_w.items()}
RESULTS["q_weights"] = {k: round(float(v), 4) for k, v in q_w.items()}

# ============ 6. 稳健性检验 ============
rob = {}
# (1) 双向1%缩尾
dw = df.copy()
for c in ["yqe", "dig"] + CTRL:
    lo, hi = dw[c].quantile([0.01, 0.99])
    dw[c] = dw[c].clip(lo, hi)
r = fe_reg(dw.set_index(["city", "year"]), "yqe", ["dig"] + CTRL)
rob["winsor"] = fmt(r, "dig") + (int(r.nobs), float(r.rsquared))
# (2) 剔除直辖市与省会城市
sub = df[df["capital"] == 0]
r = fe_reg(sub.set_index(["city", "year"]), "yqe", ["dig"] + CTRL)
rob["drop_capital"] = fmt(r, "dig") + (int(r.nobs), float(r.rsquared))
# (3) 调整样本区间（剔除2020—2021年疫情冲击）
sub = df[~df["year"].isin([2020, 2021])]
r = fe_reg(sub.set_index(["city", "year"]), "yqe", ["dig"] + CTRL)
rob["drop_covid"] = fmt(r, "dig") + (int(r.nobs), float(r.rsquared))
# (4) 替换被解释变量（主成分法测度）
r = fe_reg(panel, "yqe_pca", ["dig"] + CTRL)
rob["alt_y"] = fmt(r, "dig") + (int(r.nobs), float(r.rsquared))
# (5) 被解释变量前置一期（缓解反向因果并考察滞后影响）
df_l = df.sort_values(["city", "year"]).copy()
df_l["yqe_f1"] = df_l.groupby("city")["yqe"].shift(-1)
r = fe_reg(df_l.set_index(["city", "year"]), "yqe_f1", ["dig"] + CTRL)
rob["lead1"] = fmt(r, "dig") + (int(r.nobs), float(r.rsquared))
# (6) 替换核心解释变量测度方式（主成分法测度数字经济发展水平）
Zd = (dig_raw - dig_raw.mean()) / dig_raw.std()
ud, sd, vtd = np.linalg.svd(Zd.values - Zd.values.mean(0), full_matrices=False)
pcd = Zd.values @ vtd[0]
if np.corrcoef(pcd, df["dig"].values)[0, 1] < 0:
    pcd = -pcd
df["dig_pca"] = (pcd - pcd.min()) / (pcd.max() - pcd.min())
r = fe_reg(df.set_index(["city", "year"]), "yqe", ["dig_pca"] + CTRL)
rob["alt_x"] = fmt(r, "dig_pca") + (int(r.nobs), float(r.rsquared))
RESULTS["robust"] = {k: {"coef": v[0], "t": v[1], "b": v[2], "tv": v[3], "p": v[4],
                         "n": v[5], "r2": v[6]} for k, v in rob.items()}

# ============ 7. 内生性检验（2SLS） ============
d = df.dropna(subset=["yqe", "dig", "iv1", "iv2"] + CTRL).copy()
city_d = pd.get_dummies(d["city"], prefix="c", drop_first=True, dtype=float)
year_d = pd.get_dummies(d["year"], prefix="y", drop_first=True, dtype=float)
X_exog = pd.concat([d[CTRL].reset_index(drop=True),
                    city_d.reset_index(drop=True),
                    year_d.reset_index(drop=True)], axis=1)
X_exog.insert(0, "const", 1.0)
iv_res = IV2SLS(d["yqe"].reset_index(drop=True), X_exog,
                d[["dig"]].reset_index(drop=True),
                d[["iv1", "iv2"]].reset_index(drop=True)).fit(cov_type="clustered",
                                                              clusters=d["city"].reset_index(drop=True))
first = iv_res.first_stage.diagnostics
b_iv = float(iv_res.params["dig"]); t_iv = float(iv_res.tstats["dig"]); p_iv = float(iv_res.pvalues["dig"])
star = "***" if p_iv < 0.01 else ("**" if p_iv < 0.05 else ("*" if p_iv < 0.1 else ""))
sarg = iv_res.sargan
RESULTS["iv"] = {
    "coef": f"{b_iv:.4f}{star}", "t": f"({t_iv:.4f})", "b": b_iv, "tv": t_iv, "p": p_iv,
    "first_f": float(first["f.stat"].iloc[0]),
    "first_pval": float(first["f.pval"].iloc[0]),
    "sargan_stat": float(sarg.stat), "sargan_p": float(sarg.pval),
    "n": int(iv_res.nobs),
}
# 第一阶段系数
fs_key = list(iv_res.first_stage.individual.keys())[0]
fs = iv_res.first_stage.individual[fs_key]
RESULTS["iv_first"] = {
    v: {"b": float(fs.params[v]), "t": float(fs.tstats[v]), "p": float(fs.pvalues[v])}
    for v in ["iv1", "iv2"]
}

# ============ 8. 中介效应检验（逐步回归法） ============
med = {}
for m in ["entre", "upg", "hc"]:
    r1 = fe_reg(panel, m, ["dig"] + CTRL)                 # X → M
    r2 = fe_reg(panel, "yqe", ["dig", m] + CTRL)          # X + M → Y
    med[m] = {
        "stage1": {"coef": fmt(r1, "dig")[0], "t": fmt(r1, "dig")[1], "n": int(r1.nobs),
                   "r2": float(r1.rsquared)},
        "stage2_dig": {"coef": fmt(r2, "dig")[0], "t": fmt(r2, "dig")[1]},
        "stage2_m": {"coef": fmt(r2, m)[0], "t": fmt(r2, m)[1]},
        "n2": int(r2.nobs), "r2_2": float(r2.rsquared),
        "b1": fmt(r1, "dig")[2], "b2m": fmt(r2, m)[2], "b2x": fmt(r2, "dig")[2],
    }
    med[m]["indirect_share"] = round(med[m]["b1"] * med[m]["b2m"] /
                                     RESULTS["baseline"][-1]["dig"]["b"] * 100, 2)
RESULTS["mediation"] = med

# ============ 9. 门槛效应检验（Hansen门槛模型） ============
def threshold_ssr(data, y, xs, thvar, gamma):
    d = data.copy()
    d["_lo"] = d["dig"] * (d[thvar] <= gamma)
    d["_hi"] = d["dig"] * (d[thvar] > gamma)
    r = fe_reg(d.set_index(["city", "year"]), y, ["_lo", "_hi"] + xs)
    return float(np.sum(r.resids ** 2)), r


grid = np.quantile(df["hc_std"], np.linspace(0.15, 0.85, 60))
ssr_list = [(g, threshold_ssr(df, "yqe", CTRL, "hc_std", g)[0]) for g in grid]
g1 = min(ssr_list, key=lambda x: x[1])[0]
ssr1, r_single = threshold_ssr(df, "yqe", CTRL, "hc_std", g1)

# 线性模型（无门槛）SSR，用于门槛存在性检验
r_lin = fe_reg(panel, "yqe", ["dig"] + CTRL)
ssr0 = float(np.sum(r_lin.resids ** 2))
sigma2 = ssr1 / len(df)
F1 = (ssr0 - ssr1) / sigma2

# 自助法求单一门槛P值：自助样本在“无门槛”零假设下生成
BOOT_GRID = np.quantile(df["hc_std"], np.linspace(0.2, 0.8, 24))


def bootstrap_p(n_boot=300):
    resid_h0 = np.asarray(r_lin.resids).ravel()          # 线性（零假设）模型残差
    fitted_h0 = df["yqe"].values - resid_h0
    cnt = 0
    for _ in range(n_boot):
        yb = fitted_h0 + RNG.choice(resid_h0, size=len(resid_h0), replace=True)
        db = df.copy(); db["yqe"] = yb
        rl = fe_reg(db.set_index(["city", "year"]), "yqe", ["dig"] + CTRL)
        s0 = float(np.sum(rl.resids ** 2))
        best = min(threshold_ssr(db, "yqe", CTRL, "hc_std", g)[0] for g in BOOT_GRID)
        Fb = (s0 - best) / (best / len(db))
        if Fb > F1:
            cnt += 1
    return cnt / n_boot


p_th1 = bootstrap_p(300)

# 双重门槛：固定第一门槛，搜索第二门槛
def double_ssr_on(data, gamma1, gamma2):
    d = data.copy()
    lo, hi = min(gamma1, gamma2), max(gamma1, gamma2)
    d["_r1"] = d["dig"] * (d["hc_std"] <= lo)
    d["_r2"] = d["dig"] * ((d["hc_std"] > lo) & (d["hc_std"] <= hi))
    d["_r3"] = d["dig"] * (d["hc_std"] > hi)
    r = fe_reg(d.set_index(["city", "year"]), "yqe", ["_r1", "_r2", "_r3"] + CTRL)
    return float(np.sum(r.resids ** 2)), r


cand = [g for g in grid if abs(g - g1) > 0.12]
ssr2_list = [(g, double_ssr_on(df, g1, g)[0]) for g in cand]
g2 = min(ssr2_list, key=lambda x: x[1])[0]
ssr2, r_double = double_ssr_on(df, g1, g2)
F2 = (ssr1 - ssr2) / (ssr2 / len(df))


def bootstrap_p2(n_boot=200):
    """双重门槛检验：自助样本在“单一门槛”零假设下生成"""
    resid_h0 = np.asarray(r_single.resids).ravel()
    fitted_h0 = df["yqe"].values - resid_h0
    gg = np.quantile(df["hc_std"], np.linspace(0.2, 0.8, 16))
    cnt = 0
    for _ in range(n_boot):
        yb = fitted_h0 + RNG.choice(resid_h0, size=len(resid_h0), replace=True)
        db = df.copy(); db["yqe"] = yb
        cand1 = [(g, threshold_ssr(db, "yqe", CTRL, "hc_std", g)[0]) for g in gg]
        gb1, s1 = min(cand1, key=lambda x: x[1])
        s2 = min(double_ssr_on(db, gb1, g)[0] for g in gg if abs(g - gb1) > 0.12)
        Fb = (s1 - s2) / (s2 / len(db))
        if Fb > F2:
            cnt += 1
    return cnt / n_boot


p_th2 = bootstrap_p2(200)

lo, hi = sorted([g1, g2])
RESULTS["threshold"] = {
    "gamma1": float(lo), "gamma2": float(hi),
    "F1": float(F1), "p1": p_th1, "F2": float(F2), "p2": p_th2,
    "single": {v: {"coef": fmt(r_single, v)[0], "t": fmt(r_single, v)[1]} for v in ["_lo", "_hi"]},
    "double": {v: {"coef": fmt(r_double, v)[0], "t": fmt(r_double, v)[1]} for v in ["_r1", "_r2", "_r3"]},
    "n": int(r_double.nobs), "r2": float(r_double.rsquared),
    "share_r1": float((df["hc_std"] <= lo).mean()),
    "share_r2": float(((df["hc_std"] > lo) & (df["hc_std"] <= hi)).mean()),
    "share_r3": float((df["hc_std"] > hi).mean()),
}

# ============ 10. 异质性分析 ============
het = {}
names = {0: "东部地区", 1: "中部地区", 2: "西部地区"}
for k, nm in names.items():
    sub = df[df["region"] == k]
    r = fe_reg(sub.set_index(["city", "year"]), "yqe", ["dig"] + CTRL)
    het[nm] = {"coef": fmt(r, "dig")[0], "t": fmt(r, "dig")[1], "n": int(r.nobs),
               "r2": float(r.rsquared), "b": fmt(r, "dig")[2]}
med_pop = df.groupby("city")["pop_scale"].first().median()
for flag, nm in [(True, "大规模城市"), (False, "中小规模城市")]:
    sub = df[(df["pop_scale"] >= med_pop) == flag]
    r = fe_reg(sub.set_index(["city", "year"]), "yqe", ["dig"] + CTRL)
    het[nm] = {"coef": fmt(r, "dig")[0], "t": fmt(r, "dig")[1], "n": int(r.nobs),
               "r2": float(r.rsquared), "b": fmt(r, "dig")[2]}
for flag, nm in [(1, "中心城市"), (0, "非中心城市")]:
    sub = df[df["capital"] == flag]
    r = fe_reg(sub.set_index(["city", "year"]), "yqe", ["dig"] + CTRL)
    het[nm] = {"coef": fmt(r, "dig")[0], "t": fmt(r, "dig")[1], "n": int(r.nobs),
               "r2": float(r.rsquared), "b": fmt(r, "dig")[2]}
RESULTS["hetero"] = het

# ============ 11. 描述性统计 ============
desc_vars = ["yqe", "dig", "entre", "upg", "hc", "pgdp", "gov", "open", "urban", "edu", "infra"]
desc = df[desc_vars].agg(["count", "mean", "std", "min", "max"]).T
RESULTS["desc"] = {v: {k: round(float(desc.loc[v, k]), 4) for k in desc.columns} for v in desc_vars}

# ============ 12. 数字经济与青年就业质量的时序演进（作图用） ============
trend = df.groupby("year").agg(dig=("dig", "mean"), yqe=("yqe", "mean")).reset_index()
trend_reg = df.groupby(["year", "region"]).agg(dig=("dig", "mean"), yqe=("yqe", "mean")).reset_index()
trend.to_csv(f"{OUT}/p1_trend.csv", index=False)
trend_reg.to_csv(f"{OUT}/p1_trend_region.csv", index=False)
# 门槛效应作图数据
pd.DataFrame(ssr_list, columns=["gamma", "ssr"]).to_csv(f"{OUT}/p1_threshold_ssr.csv", index=False)
df.to_csv(f"{OUT}/p1_panel.csv", index=False)

with open(f"{OUT}/p1_results.json", "w", encoding="utf-8") as f:
    json.dump(RESULTS, f, ensure_ascii=False, indent=2)

print("=== 基准回归（列6） ===")
print(RESULTS["baseline"][-1]["dig"], "N=", RESULTS["baseline"][-1]["n"], "R2=", round(RESULTS["baseline"][-1]["r2"], 4))
print("=== 稳健性 ===")
for k, v in RESULTS["robust"].items():
    print(f"  {k}: {v['coef']} {v['t']} N={v['n']}")
print("=== 内生性 ===")
print("  2SLS:", RESULTS["iv"]["coef"], RESULTS["iv"]["t"],
      "F1st=", round(RESULTS["iv"]["first_f"], 3), "Sargan p=", round(RESULTS["iv"]["sargan_p"], 4))
print("=== 中介 ===")
for m, v in med.items():
    print(f"  {m}: 一阶段{v['stage1']['coef']}  二阶段M{v['stage2_m']['coef']}  X{v['stage2_dig']['coef']}  中介占比{v['indirect_share']}%")
print("=== 门槛 ===")
print(f"  γ1={lo:.4f} (F={F1:.3f}, p={p_th1:.3f})  γ2={hi:.4f} (F={F2:.3f}, p={p_th2:.3f})")
print("  分段:", RESULTS["threshold"]["double"])
print("=== 异质性 ===")
for k, v in het.items():
    print(f"  {k}: {v['coef']} {v['t']} N={v['n']}")
print("\n权重:", RESULTS["dig_weights"])
