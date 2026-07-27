# -*- coding: utf-8 -*-
"""论文2：人工智能应用对青年就业的替代效应与创造效应——仿真数据生成与实证估计。

数据结构模仿2013—2024年中国30个省份面板（不含西藏及港澳台）；人工智能
应用水平参照Acemoglu和Restrepo的机器人渗透度构造思路，以国际机器人联合会
分行业机器人安装量按基期行业就业份额加权到省份；数值由蒙特卡洛仿真生成，
全部回归结果由本脚本实际估计得到。
"""
import json
import os
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS
from linearmodels.iv import IV2SLS
import statsmodels.formula.api as smf

RNG = np.random.default_rng(20260705)
YEARS = list(range(2013, 2025))
T = len(YEARS)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")

PROV = [
    "北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏",
    "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "广西",
    "海南", "重庆", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "宁夏", "新疆",
]
EAST = {"北京", "天津", "河北", "辽宁", "上海", "江苏", "浙江", "福建", "山东", "广东", "海南"}
CENTRAL = {"山西", "吉林", "黑龙江", "安徽", "江西", "河南", "湖北", "湖南"}
N_P = len(PROV)

# ============ 1. 省份结构特征 ============
manu_share = np.clip(RNG.normal(0.34, 0.09, N_P), 0.14, 0.56)   # 基期制造业就业份额
# 基期（2010年）装备制造业产值占比：机器人技术采纳的产业基础，独立于制造业总体规模
equip2010 = np.clip(0.42 + 0.30 * (manu_share - manu_share.mean())
                    + RNG.normal(0, 0.11, N_P), 0.12, None)
prov_a = RNG.normal(0, 0.5, N_P) + np.array(
    [0.75 if p in EAST else (0.25 if p in CENTRAL else 0.0) for p in PROV]
)
edu_base = RNG.normal(0, 0.6, N_P) + 0.55 * prov_a               # 教育发展基础

rows = []
for i, p in enumerate(PROV):
    reg = 0 if p in EAST else (1 if p in CENTRAL else 2)
    for ti, yr in enumerate(YEARS):
        rows.append((i, p, yr, ti, reg, manu_share[i], prov_a[i], edu_base[i]))
df = pd.DataFrame(rows, columns=["pid", "prov", "year", "t", "region",
                                 "manu_share", "prov_a", "edu_base"])
n = len(df)
pi = df["pid"].values
tt = df["t"].values

# ============ 2. 人工智能应用水平（机器人渗透度） ============
# 全国机器人存量增长（台/万人，贴近IFR公布的中国装机趋势）
nation_robot = np.array([0.42, 0.63, 0.95, 1.38, 1.92, 2.71, 3.52, 4.18, 5.06, 6.35, 7.62, 8.74])
ai = (nation_robot[tt]
      * (0.32 + 0.82 * df["manu_share"].values / 0.34 + 0.70 * equip2010[pi] / 0.42)
      * np.exp(0.30 * df["prov_a"].values + RNG.normal(0, 0.14, n)))
df["ai"] = ai
df["lnai"] = np.log1p(ai)
ai_std = (df["lnai"] - df["lnai"].mean()) / df["lnai"].std()
df["ai_std"] = ai_std

# ============ 3. 机制变量 ============
# 常规任务岗位占比（替代渠道，AI提高则下降）
routine = 41.0 - 3.15 * ai_std + 2.4 * RNG.normal(0, 1, n) - 0.22 * tt
# 新兴数字职业就业占比（创造渠道）
newjob = 5.2 + 2.35 * ai_std + 0.28 * tt + 1.9 * RNG.normal(0, 1, n)
# 人岗技能匹配度（0—1）
match = 1 / (1 + np.exp(-(0.80 * ai_std + 0.55 * df["edu_base"].values + 0.03 * tt
                          + RNG.normal(0, 0.45, n)))) * 0.86
df["routine"] = np.clip(routine, 18.0, 58.0)
df["newjob"] = np.clip(newjob, 1.2, 26.0)
df["match"] = match

# ============ 4. 控制变量 ============
df["lnpgdp"] = 10.6 + 0.38 * df["prov_a"] + 0.055 * tt + RNG.normal(0, 0.16, n)
df["indus"] = 1.02 + 0.22 * df["prov_a"] + 0.028 * tt + RNG.normal(0, 0.14, n)   # 三二产业比
df["open"] = np.abs(24.0 + 16.0 * df["prov_a"] + RNG.normal(0, 8.0, n))          # 进出口/GDP(%)
df["urban"] = np.clip(52.0 + 8.5 * df["prov_a"] + 0.92 * tt + RNG.normal(0, 3.0, n), 30, 92)
df["fis"] = np.clip(24.0 - 2.2 * df["prov_a"] + 0.28 * tt + RNG.normal(0, 3.4, n), 10, 62)
df["wage"] = 10.6 + 0.30 * df["prov_a"] + 0.072 * tt + RNG.normal(0, 0.10, n)    # ln平均工资
df["edu_level"] = np.clip(34.0 + 7.5 * df["edu_base"] + 1.35 * tt + RNG.normal(0, 2.4, n), 18, 78)
df["train"] = np.clip(11.5 + 3.2 * df["edu_base"] + 0.42 * tt + RNG.normal(0, 1.8, n), 3, 34)

CTRL = ["lnpgdp", "indus", "open", "urban", "fis", "wage"]

# ============ 5. 青年就业结果变量（替代与创造并存的U型净效应） ============
# 净效应：低渗透阶段替代占优，高渗透阶段创造占优 → 对ai_std呈U型
edu_c = (df["edu_level"].values - df["edu_level"].mean()) / df["edu_level"].std()
train_c = (df["train"].values - df["train"].mean()) / df["train"].std()
u_shape = -0.108 * ai_std + 0.045 * ai_std ** 2
lat_emp = (
    u_shape
    + 0.032 * ai_std * edu_c                                     # 教育水平的调节
    + 0.025 * ai_std * train_c                                   # 技能培训的调节
    + 0.0085 * (df["routine"].values - df["routine"].mean())     # 替代渠道：常规岗位是青年就业载体
    + 0.0135 * (df["newjob"].values - df["newjob"].mean())       # 创造渠道
    + 0.215 * (df["match"].values - df["match"].mean())          # 匹配渠道
    + 0.085 * (df["lnpgdp"].values - df["lnpgdp"].mean())
    + 0.0016 * (df["urban"].values - df["urban"].mean())
    + 0.0009 * (df["open"].values - df["open"].mean())
    - 0.0012 * (df["fis"].values - df["fis"].mean())
    + 0.30 * df["prov_a"].values
    + 0.020 * tt
    + RNG.normal(0, 0.055, n)
)
df["lnyemp"] = 6.35 + lat_emp                                     # ln(青年就业人数,万人)
# 替代测度：青年就业占城镇总就业比重（%），用于稳健性检验
df["yshare"] = np.clip(23.5 + 7.8 * lat_emp + RNG.normal(0, 0.9, n), 8.0, 46.0)

# 青年就业结构：高技能与低技能占比（就业极化）
df["hskill"] = np.clip(28.5 + 2.85 * ai_std + 0.16 * df["edu_level"] + 1.5 * RNG.normal(0, 1, n), 12, 62)
df["lskill"] = np.clip(34.0 - 2.42 * ai_std - 0.10 * df["edu_level"] + 1.6 * RNG.normal(0, 1, n), 9, 58)
# 青年失业率（%）
df["yunemp"] = np.clip(13.8 + 1.52 * ai_std - 0.62 * ai_std ** 2 - 0.055 * df["edu_level"]
                       + 1.15 * RNG.normal(0, 1, n), 3.5, 26.0)

panel = df.set_index(["pid", "year"])
RESULTS = {}


def fe_reg(data, y, xs, entity=True, time=True):
    d = data.dropna(subset=[y] + xs)
    res = PanelOLS(d[y], d[xs], entity_effects=entity, time_effects=time,
                   check_rank=False).fit(cov_type="clustered", cluster_entity=True)
    return res


def fmt(res, var, dec=4):
    b, t, p = res.params[var], res.tstats[var], res.pvalues[var]
    star = "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.1 else ""))
    return f"{b:.{dec}f}{star}", f"({t:.4f})", float(b), float(t), float(p)


# ============ 6. 基准回归 ============
base = []
specs = [
    ("lnyemp", ["ai_std"], "线性设定"),
    ("lnyemp", ["ai_std"] + CTRL, "线性设定+控制变量"),
    ("lnyemp", ["ai_std", "ai_sq"], "二次设定"),
    ("lnyemp", ["ai_std", "ai_sq"] + CTRL, "二次设定+控制变量"),
]
df["ai_sq"] = df["ai_std"] ** 2
panel = df.set_index(["pid", "year"])
for k, (y, xs, label) in enumerate(specs, 1):
    r = fe_reg(panel, y, xs)
    row = {"col": k, "label": label, "n": int(r.nobs), "r2": float(r.rsquared)}
    for v in xs:
        c, t, b, tv, p = fmt(r, v)
        row[v] = {"coef": c, "t": t, "b": b, "tv": tv, "p": p}
    base.append(row)
    if k == 4:
        MAIN = r
RESULTS["baseline"] = base
# U型拐点与Utest（Lind-Mehlum三条件）
b1 = MAIN.params["ai_std"]; b2 = MAIN.params["ai_sq"]
turn = -b1 / (2 * b2)
lo_x, hi_x = df["ai_std"].min(), df["ai_std"].max()
slope_lo = b1 + 2 * b2 * lo_x
slope_hi = b1 + 2 * b2 * hi_x
RESULTS["ushape"] = {
    "turn_std": float(turn),
    "turn_share_below": float((df["ai_std"] < turn).mean()),
    "slope_low": float(slope_lo), "slope_high": float(slope_hi),
    "range": [float(lo_x), float(hi_x)],
    "turn_ai_raw": float(np.exp(turn * df["lnai"].std() + df["lnai"].mean()) - 1),
}

# ============ 7. 就业结构效应（替代与创造的直接证据） ============
struct = {}
for y, nm in [("hskill", "青年高技能就业占比"), ("lskill", "青年低技能就业占比"),
              ("routine", "常规任务岗位占比"), ("newjob", "新兴数字职业占比")]:
    r = fe_reg(panel, y, ["ai_std"] + CTRL)
    c, t, b, tv, p = fmt(r, "ai_std")
    struct[nm] = {"coef": c, "t": t, "b": b, "p": p, "n": int(r.nobs),
                  "r2": float(r.rsquared)}
# 青年失业率：与就业总量的U型相对应，检验倒U型
r = fe_reg(panel, "yunemp", ["ai_std", "ai_sq"] + CTRL)
struct["青年失业率"] = {
    "coef": fmt(r, "ai_std")[0], "t": fmt(r, "ai_std")[1],
    "coef2": fmt(r, "ai_sq")[0], "t2": fmt(r, "ai_sq")[1],
    "b": fmt(r, "ai_std")[2], "b2": fmt(r, "ai_sq")[2],
    "p": fmt(r, "ai_std")[4], "n": int(r.nobs), "r2": float(r.rsquared),
    "turn": float(-fmt(r, "ai_std")[2] / (2 * fmt(r, "ai_sq")[2])),
}
RESULTS["structure"] = struct

# ============ 8. 稳健性检验 ============
rob = {}
r = fe_reg(panel, "lnyemp", ["lnai", "lnai_sq"] + CTRL) if False else None
df["lnai_sq"] = df["lnai"] ** 2
p2 = df.set_index(["pid", "year"])
r = fe_reg(p2, "lnyemp", ["lnai", "lnai_sq"] + CTRL)
rob["替换核心解释变量"] = {"x": fmt(r, "lnai")[:2], "x2": fmt(r, "lnai_sq")[:2],
                           "n": int(r.nobs), "r2": float(r.rsquared)}
sub = df[~df["prov"].isin(["北京", "上海", "天津", "重庆"])]
r = fe_reg(sub.set_index(["pid", "year"]), "lnyemp", ["ai_std", "ai_sq"] + CTRL)
rob["剔除直辖市"] = {"x": fmt(r, "ai_std")[:2], "x2": fmt(r, "ai_sq")[:2],
                     "n": int(r.nobs), "r2": float(r.rsquared)}
sub = df[~df["year"].isin([2020, 2021])]
r = fe_reg(sub.set_index(["pid", "year"]), "lnyemp", ["ai_std", "ai_sq"] + CTRL)
rob["调整样本区间"] = {"x": fmt(r, "ai_std")[:2], "x2": fmt(r, "ai_sq")[:2],
                       "n": int(r.nobs), "r2": float(r.rsquared)}
dw = df.copy()
for c in ["lnyemp", "ai_std"] + CTRL:
    lo, hi = dw[c].quantile([0.01, 0.99]); dw[c] = dw[c].clip(lo, hi)
dw["ai_sq"] = dw["ai_std"] ** 2
r = fe_reg(dw.set_index(["pid", "year"]), "lnyemp", ["ai_std", "ai_sq"] + CTRL)
rob["缩尾处理"] = {"x": fmt(r, "ai_std")[:2], "x2": fmt(r, "ai_sq")[:2],
                   "n": int(r.nobs), "r2": float(r.rsquared)}
r = fe_reg(panel, "yshare", ["ai_std", "ai_sq"] + CTRL)
rob["替换被解释变量"] = {"x": fmt(r, "ai_std")[:2], "x2": fmt(r, "ai_sq")[:2],
                         "n": int(r.nobs), "r2": float(r.rsquared)}
RESULTS["robust"] = rob

# ============ 9. 内生性：Bartik类工具变量 ============
# 美国同期分行业机器人渗透度（外生技术冲击）× 本省基期制造业就业份额
us_robot = np.array([1.72, 2.05, 2.44, 2.88, 3.35, 3.92, 4.46, 4.95, 5.38, 6.02, 6.71, 7.35])
df["iv_bartik"] = us_robot[tt] * df["manu_share"] * 10
# 第二工具变量：基期装备制造业产值占比 × 全国机器人装机量
# 仅通过技术采纳的产业基础影响当期机器人渗透度，不含直接作用于青年就业的省份禀赋
df["iv_hist"] = equip2010[pi] * nation_robot[tt]
d = df.dropna(subset=["lnyemp", "ai_std", "iv_bartik", "iv_hist"] + CTRL).reset_index(drop=True)
d["iv_b2"] = d["iv_bartik"] ** 2
d["iv_h2"] = d["iv_hist"] ** 2
pd_ = pd.get_dummies(d["pid"], prefix="p", drop_first=True, dtype=float)
yd = pd.get_dummies(d["year"], prefix="y", drop_first=True, dtype=float)
Xex = pd.concat([d[CTRL], pd_, yd], axis=1)
Xex.insert(0, "const", 1.0)
ivr = IV2SLS(d["lnyemp"], Xex, d[["ai_std"]],
             d[["iv_bartik", "iv_hist"]]).fit(cov_type="clustered", clusters=d["pid"])


def _st(pv):
    return "***" if pv < 0.01 else ("**" if pv < 0.05 else ("*" if pv < 0.1 else ""))


b1i, t1i, p1i = float(ivr.params["ai_std"]), float(ivr.tstats["ai_std"]), float(ivr.pvalues["ai_std"])
fs = ivr.first_stage.diagnostics
fs_ai = ivr.first_stage.individual["ai_std"]
RESULTS["iv"] = {
    "coef": f"{b1i:.4f}{_st(p1i)}", "t": f"({t1i:.4f})", "b": b1i, "p": p1i,
    "first_f": float(fs["f.stat"].iloc[0]), "first_p": float(fs["f.pval"].iloc[0]),
    "sargan_stat": float(ivr.sargan.stat), "sargan_p": float(ivr.sargan.pval),
    "n": int(ivr.nobs),
    "first_stage": {v: {"b": float(fs_ai.params[v]), "t": float(fs_ai.tstats[v]),
                        "p": float(fs_ai.pvalues[v])} for v in ["iv_bartik", "iv_hist"]},
}

# 控制函数法：非线性设定下的内生性处理（Wooldridge, 2015）
# 第一阶段：内生变量对工具变量与外生变量回归，取广义残差
d_cf = df.copy()
r_fs = fe_reg(d_cf.set_index(["pid", "year"]), "ai_std", ["iv_bartik", "iv_hist"] + CTRL)
d_cf["cf_v"] = np.asarray(r_fs.resids).ravel()
r_cf = fe_reg(d_cf.set_index(["pid", "year"]), "lnyemp", ["ai_std", "ai_sq", "cf_v"] + CTRL)
b1c, b2c = float(r_cf.params["ai_std"]), float(r_cf.params["ai_sq"])


def cf_bootstrap(n_boot=400):
    """按省份整群自助，校正两阶段估计的标准误"""
    ids = df["pid"].unique()
    out = []
    for _ in range(n_boot):
        pick = RNG.choice(ids, size=len(ids), replace=True)
        parts = []
        for j, p_ in enumerate(pick):
            s = df[df["pid"] == p_].copy()
            s["pid"] = j                       # 重新编号以允许重复抽取
            parts.append(s)
        db = pd.concat(parts, ignore_index=True)
        try:
            rf = fe_reg(db.set_index(["pid", "year"]), "ai_std", ["iv_bartik", "iv_hist"] + CTRL)
            db["cf_v"] = np.asarray(rf.resids).ravel()
            rc = fe_reg(db.set_index(["pid", "year"]), "lnyemp", ["ai_std", "ai_sq", "cf_v"] + CTRL)
            out.append([float(rc.params["ai_std"]), float(rc.params["ai_sq"]),
                        float(rc.params["cf_v"])])
        except Exception:
            continue
    return np.array(out)


BS = cf_bootstrap(400)
se_cf = BS.std(axis=0, ddof=1)
tv_cf = np.array([b1c, b2c, float(r_cf.params["cf_v"])]) / se_cf
from scipy import stats as _sps
pv_cf = 2 * (1 - _sps.norm.cdf(np.abs(tv_cf)))
RESULTS["control_function"] = {
    "ai_std": {"coef": f"{b1c:.4f}{_st(pv_cf[0])}", "se": float(se_cf[0]),
               "t": f"({tv_cf[0]:.4f})", "b": b1c, "p": float(pv_cf[0])},
    "ai_sq": {"coef": f"{b2c:.4f}{_st(pv_cf[1])}", "se": float(se_cf[1]),
              "t": f"({tv_cf[1]:.4f})", "b": b2c, "p": float(pv_cf[1])},
    "cf_v": {"coef": f"{float(r_cf.params['cf_v']):.4f}{_st(pv_cf[2])}", "se": float(se_cf[2]),
             "t": f"({tv_cf[2]:.4f})", "p": float(pv_cf[2])},
    "turn": float(-b1c / (2 * b2c)),
    "n": int(r_cf.nobs), "r2": float(r_cf.rsquared), "n_boot": int(len(BS)),
    "first_stage": {v: {"b": float(r_fs.params[v]), "t": float(r_fs.tstats[v]),
                        "p": float(r_fs.pvalues[v])} for v in ["iv_bartik", "iv_hist"]},
    "first_r2": float(r_fs.rsquared),
}

# ============ 10. 作用机制检验（逐步回归） ============
mech = {}
for m, nm in [("routine", "常规任务替代"), ("newjob", "新兴岗位创造"), ("match", "人岗技能匹配")]:
    r1 = fe_reg(panel, m, ["ai_std"] + CTRL)
    r2 = fe_reg(panel, "lnyemp", ["ai_std", m] + CTRL)
    mech[nm] = {
        "var": m,
        "s1": {"coef": fmt(r1, "ai_std")[0], "t": fmt(r1, "ai_std")[1],
               "n": int(r1.nobs), "r2": float(r1.rsquared)},
        "s2_x": {"coef": fmt(r2, "ai_std")[0], "t": fmt(r2, "ai_std")[1]},
        "s2_m": {"coef": fmt(r2, m)[0], "t": fmt(r2, m)[1]},
        "n2": int(r2.nobs), "r2_2": float(r2.rsquared),
        "b1": fmt(r1, "ai_std")[2], "bm": fmt(r2, m)[2],
        "indirect": float(fmt(r1, "ai_std")[2] * fmt(r2, m)[2]),
    }
RESULTS["mechanism"] = mech

# ============ 11. 调节效应 ============
modr = {}
for z, nm in [("edu_level", "教育发展水平"), ("train", "职业技能培训")]:
    d2 = df.copy()
    d2[z + "_c"] = (d2[z] - d2[z].mean()) / d2[z].std()
    d2["inter"] = d2["ai_std"] * d2[z + "_c"]
    r = fe_reg(d2.set_index(["pid", "year"]), "lnyemp",
               ["ai_std", "ai_sq", z + "_c", "inter"] + CTRL)
    modr[nm] = {
        "x": {"coef": fmt(r, "ai_std")[0], "t": fmt(r, "ai_std")[1]},
        "x2": {"coef": fmt(r, "ai_sq")[0], "t": fmt(r, "ai_sq")[1]},
        "z": {"coef": fmt(r, z + "_c")[0], "t": fmt(r, z + "_c")[1]},
        "inter": {"coef": fmt(r, "inter")[0], "t": fmt(r, "inter")[1]},
        "n": int(r.nobs), "r2": float(r.rsquared),
    }
RESULTS["moderation"] = modr

# ============ 12. 异质性分析 ============
het = {}
for k, nm in [(0, "东部地区"), (1, "中部地区"), (2, "西部地区")]:
    sub = df[df["region"] == k]
    r = fe_reg(sub.set_index(["pid", "year"]), "lnyemp", ["ai_std", "ai_sq"] + CTRL)
    het[nm] = {"x": {"coef": fmt(r, "ai_std")[0], "t": fmt(r, "ai_std")[1]},
               "x2": {"coef": fmt(r, "ai_sq")[0], "t": fmt(r, "ai_sq")[1]},
               "n": int(r.nobs), "r2": float(r.rsquared)}
med_edu = df.groupby("pid")["edu_level"].mean().median()
prov_edu = df.groupby("pid")["edu_level"].mean()
for flag, nm in [(True, "高教育水平地区"), (False, "低教育水平地区")]:
    ids = prov_edu[(prov_edu >= med_edu) == flag].index
    sub = df[df["pid"].isin(ids)]
    r = fe_reg(sub.set_index(["pid", "year"]), "lnyemp", ["ai_std", "ai_sq"] + CTRL)
    het[nm] = {"x": {"coef": fmt(r, "ai_std")[0], "t": fmt(r, "ai_std")[1]},
               "x2": {"coef": fmt(r, "ai_sq")[0], "t": fmt(r, "ai_sq")[1]},
               "n": int(r.nobs), "r2": float(r.rsquared)}
med_mn = df.groupby("pid")["manu_share"].first().median()
prov_mn = df.groupby("pid")["manu_share"].first()
for flag, nm in [(True, "制造业密集地区"), (False, "非制造业密集地区")]:
    ids = prov_mn[(prov_mn >= med_mn) == flag].index
    sub = df[df["pid"].isin(ids)]
    r = fe_reg(sub.set_index(["pid", "year"]), "lnyemp", ["ai_std", "ai_sq"] + CTRL)
    het[nm] = {"x": {"coef": fmt(r, "ai_std")[0], "t": fmt(r, "ai_std")[1]},
               "x2": {"coef": fmt(r, "ai_sq")[0], "t": fmt(r, "ai_sq")[1]},
               "n": int(r.nobs), "r2": float(r.rsquared)}
RESULTS["hetero"] = het

# ============ 13. 分位数回归 ============
dq = df.copy()
for c in ["pid", "year"]:
    dq[c] = dq[c].astype("category")
qres = {}
formula = "lnyemp ~ ai_std + ai_sq + " + " + ".join(CTRL) + " + C(pid) + C(year)"
for q in [0.10, 0.25, 0.50, 0.75, 0.90]:
    m = smf.quantreg(formula, dq).fit(q=q, max_iter=8000)
    b1q, b2q = m.params["ai_std"], m.params["ai_sq"]
    p1q, p2q = m.pvalues["ai_std"], m.pvalues["ai_sq"]
    s1 = "***" if p1q < 0.01 else ("**" if p1q < 0.05 else ("*" if p1q < 0.1 else ""))
    s2 = "***" if p2q < 0.01 else ("**" if p2q < 0.05 else ("*" if p2q < 0.1 else ""))
    qres[f"Q{int(q*100)}"] = {
        "x": f"{b1q:.4f}{s1}", "tx": f"({m.tvalues['ai_std']:.4f})",
        "x2": f"{b2q:.4f}{s2}", "tx2": f"({m.tvalues['ai_sq']:.4f})",
        "turn": float(-b1q / (2 * b2q)) if b2q != 0 else None,
    }
RESULTS["quantile"] = qres

# ============ 14. 描述性统计 ============
dvars = ["lnyemp", "hskill", "lskill", "yunemp", "ai_std", "ai", "routine", "newjob",
         "match", "lnpgdp", "indus", "open", "urban", "fis", "wage", "edu_level", "train"]
desc = df[dvars].agg(["count", "mean", "std", "min", "max"]).T
RESULTS["desc"] = {v: {k: round(float(desc.loc[v, k]), 4) for k in desc.columns} for v in dvars}

# 作图数据
df.groupby("year").agg(ai=("ai", "mean"), lnyemp=("lnyemp", "mean"),
                       hskill=("hskill", "mean"), lskill=("lskill", "mean")).reset_index() \
  .to_csv(f"{OUT}/p2_trend.csv", index=False)
df.to_csv(f"{OUT}/p2_panel.csv", index=False)
with open(f"{OUT}/p2_results.json", "w", encoding="utf-8") as f:
    json.dump(RESULTS, f, ensure_ascii=False, indent=2)

print("=== 基准回归 ===")
for r in base:
    ln = f"  ({r['col']}) {r['label']}: ai={r['ai_std']['coef']}{r['ai_std']['t']}"
    if "ai_sq" in r:
        ln += f"  ai²={r['ai_sq']['coef']}{r['ai_sq']['t']}"
    print(ln + f"  N={r['n']} R2={r['r2']:.4f}")
print(f"=== U型拐点: {RESULTS['ushape']['turn_std']:.4f}（标准化），"
      f"低于拐点样本占比 {RESULTS['ushape']['turn_share_below']:.3f}，"
      f"折合机器人渗透度 {RESULTS['ushape']['turn_ai_raw']:.3f} 台/万人")
print("=== 就业结构 ===")
for k, v in struct.items():
    print(f"  {k}: {v['coef']}{v['t']} N={v['n']}")
print("=== 稳健性 ===")
for k, v in rob.items():
    print(f"  {k}: x={v['x'][0]}{v['x'][1]} x2={v['x2'][0]}{v['x2'][1]} N={v['n']}")
print("=== 内生性 ===")
print(f"  线性2SLS: {RESULTS['iv']['coef']}{RESULTS['iv']['t']} 第一阶段F={RESULTS['iv']['first_f']:.3f} "
      f"Sargan p={RESULTS['iv']['sargan_p']:.4f}")
_cf = RESULTS['control_function']
print(f"  控制函数法: x={_cf['ai_std']['coef']}{_cf['ai_std']['t']} x2={_cf['ai_sq']['coef']}{_cf['ai_sq']['t']} "
      f"广义残差={_cf['cf_v']['coef']}{_cf['cf_v']['t']} 拐点={_cf['turn']:.4f} 一阶段R2={_cf['first_r2']:.4f}")
print("=== 机制 ===")
for k, v in mech.items():
    print(f"  {k}: 一阶段{v['s1']['coef']}{v['s1']['t']} 二阶段M{v['s2_m']['coef']}{v['s2_m']['t']}")
print("=== 调节 ===")
for k, v in modr.items():
    print(f"  {k}: 交互项{v['inter']['coef']}{v['inter']['t']}")
print("=== 异质性 ===")
for k, v in het.items():
    print(f"  {k}: x={v['x']['coef']} x2={v['x2']['coef']} N={v['n']}")
print("=== 分位数 ===")
for k, v in qres.items():
    print(f"  {k}: x={v['x']} x2={v['x2']}")
