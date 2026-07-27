# -*- coding: utf-8 -*-
"""论文4《人口老龄化对全要素生产率的空间溢出效应与门槛特征》的数据生成与计量估计。

数据为蒙特卡洛仿真面板（30 个省份，2011—2023 年），空间单元、邻接关系与省会
经纬度均为真实地理信息，指标口径参照《中国statistical年鉴》《中国人口和就业
统计年鉴》《中国科技统计年鉴》设定。全部估计结果由本脚本实际计算得到。

估计器清单：
  1. 全局与局部 Moran's I 空间相关性检验
  2. LM-lag / LM-error 及其稳健形式（Anselin, 1996）、Hausman 与 LR 设定检验
  3. 空间杜宾模型（时空双固定效应，拟极大似然估计）
  4. LeSage & Pace（2009）直接效应、间接效应与总效应分解（蒙特卡洛标准误）
  5. 三类空间权重矩阵下的稳健性检验、动态空间杜宾模型
  6. 广义空间两阶段最小二乘（GS2SLS）与外生工具变量
  7. Hansen（1999）面板门槛模型（自助法在原假设下抽样）
  8. 机制检验（两步法）与分区域异质性检验
"""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats, optimize

RNG = np.random.default_rng(20260727)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = {}

# ============================================================
# 一、空间单元与权重矩阵
# ============================================================
PROV = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江",
        "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南",
        "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州",
        "云南", "陕西", "甘肃", "青海", "宁夏", "新疆"]
IDX = {p: i for i, p in enumerate(PROV)}
N = len(PROV)

ADJ = {
    "北京": ["河北", "天津"], "天津": ["北京", "河北"],
    "河北": ["北京", "天津", "辽宁", "内蒙古", "山西", "河南", "山东"],
    "山西": ["河北", "内蒙古", "陕西", "河南"],
    "内蒙古": ["黑龙江", "吉林", "辽宁", "河北", "山西", "陕西", "宁夏",
               "甘肃", "新疆"],
    "辽宁": ["吉林", "内蒙古", "河北"],
    "吉林": ["黑龙江", "内蒙古", "辽宁"],
    "黑龙江": ["吉林", "内蒙古"],
    "上海": ["江苏", "浙江"],
    "江苏": ["山东", "安徽", "浙江", "上海"],
    "浙江": ["江苏", "上海", "安徽", "江西", "福建"],
    "安徽": ["江苏", "浙江", "江西", "湖北", "河南", "山东"],
    "福建": ["浙江", "江西", "广东"],
    "江西": ["安徽", "浙江", "福建", "广东", "湖南", "湖北"],
    "山东": ["河北", "河南", "安徽", "江苏"],
    "河南": ["河北", "山西", "陕西", "湖北", "安徽", "山东"],
    "湖北": ["河南", "安徽", "江西", "湖南", "重庆", "陕西"],
    "湖南": ["湖北", "江西", "广东", "广西", "贵州", "重庆"],
    "广东": ["福建", "江西", "湖南", "广西", "海南"],
    "广西": ["广东", "湖南", "贵州", "云南"],
    "海南": ["广东"],
    "重庆": ["湖北", "湖南", "贵州", "四川", "陕西"],
    "四川": ["青海", "甘肃", "陕西", "重庆", "贵州", "云南"],
    "贵州": ["四川", "重庆", "湖南", "广西", "云南"],
    "云南": ["四川", "贵州", "广西"],
    "陕西": ["内蒙古", "山西", "河南", "湖北", "重庆", "四川", "甘肃", "宁夏"],
    "甘肃": ["内蒙古", "宁夏", "陕西", "四川", "青海", "新疆"],
    "青海": ["甘肃", "四川", "新疆"],
    "宁夏": ["内蒙古", "陕西", "甘肃"],
    "新疆": ["甘肃", "青海", "内蒙古"],
}
LONLAT = {
    "北京": (116.4, 39.9), "天津": (117.2, 39.1), "河北": (114.5, 38.0),
    "山西": (112.5, 37.9), "内蒙古": (111.7, 40.8), "辽宁": (123.4, 41.8),
    "吉林": (125.3, 43.9), "黑龙江": (126.6, 45.8), "上海": (121.5, 31.2),
    "江苏": (118.8, 32.1), "浙江": (120.2, 30.3), "安徽": (117.3, 31.9),
    "福建": (119.3, 26.1), "江西": (115.9, 28.7), "山东": (117.0, 36.7),
    "河南": (113.6, 34.8), "湖北": (114.3, 30.6), "湖南": (113.0, 28.2),
    "广东": (113.3, 23.1), "广西": (108.4, 22.8), "海南": (110.3, 20.0),
    "重庆": (106.5, 29.6), "四川": (104.1, 30.7), "贵州": (106.6, 26.6),
    "云南": (102.7, 25.0), "陕西": (108.9, 34.3), "甘肃": (103.8, 36.1),
    "青海": (101.8, 36.6), "宁夏": (106.3, 38.5), "新疆": (87.6, 43.8),
}
EAST = ["北京", "天津", "河北", "辽宁", "上海", "江苏", "浙江", "福建",
        "山东", "广东", "海南"]
CENTRAL = ["山西", "吉林", "黑龙江", "安徽", "江西", "河南", "湖北", "湖南"]
WEST = [p for p in PROV if p not in EAST + CENTRAL]


def row_std(A):
    A = np.asarray(A, dtype=float).copy()
    np.fill_diagonal(A, 0.0)
    s = A.sum(axis=1, keepdims=True)
    s[s == 0] = 1.0
    return A / s


A01 = np.zeros((N, N))
for p, nbs in ADJ.items():
    for q in nbs:
        A01[IDX[p], IDX[q]] = 1.0
        A01[IDX[q], IDX[p]] = 1.0
W1 = row_std(A01)                                     # 0—1 邻接权重矩阵

R = 6371.0
lon = np.radians(np.array([LONLAT[p][0] for p in PROV]))
lat = np.radians(np.array([LONLAT[p][1] for p in PROV]))
dlon = lon[:, None] - lon[None, :]
dlat = lat[:, None] - lat[None, :]
hav = np.sin(dlat / 2) ** 2 + np.cos(lat[:, None]) * np.cos(lat[None, :]) \
    * np.sin(dlon / 2) ** 2
DIST = 2 * R * np.arcsin(np.sqrt(np.clip(hav, 0, 1)))
with np.errstate(divide="ignore"):
    INV = np.where(DIST > 0, 1.0 / DIST ** 2, 0.0)
W2 = row_std(INV)                                     # 地理距离（平方倒数）权重矩阵

# ============================================================
# 二、数据生成
# ============================================================
YEARS = np.arange(2011, 2024)
T = len(YEARS)
region = np.array([0 if p in EAST else 1 if p in CENTRAL else 2 for p in PROV])

# 历史人口结构潜变量：空间相关，决定初始老龄化水平及其后续演进速度
SPF = np.linalg.inv(np.eye(N) - 0.74 * W1)             # 空间滤波算子
hist = SPF @ RNG.normal(0, 1, N)
hist = (hist - hist.mean()) / hist.std()

# 全要素生产率方程的随机扰动项（先行生成，用于刻画老龄化的内生性）
eps = RNG.normal(0, 0.0205, (N, T))

# 人口老龄化：65 岁及以上人口占比（%）
# 负向生产率冲击会引致青壮年劳动力外流，从而抬高本地老龄化水平（反向因果）
aging0 = np.where(region == 0, 9.8, np.where(region == 1, 9.6, 8.4)).astype(float) \
    + 1.05 * hist + RNG.normal(0, 0.70, N)
aging_tr = 0.44 + 0.135 * hist + RNG.normal(0, 0.115, N)
aging = aging0[:, None] + aging_tr[:, None] * np.arange(T)[None, :] \
    + SPF @ RNG.normal(0, 0.115, (N, T)) - 4.0 * eps

# 研发强度（R&D 经费投入强度，%）——门槛变量
rd0 = np.where(region == 0, 1.92, np.where(region == 1, 1.18, 0.92)).astype(float) \
    + RNG.normal(0, 0.42, N)
rd = np.clip(rd0[:, None] + (0.052 + RNG.normal(0, 0.020, N))[:, None]
             * np.arange(T)[None, :] + RNG.normal(0, 0.055, (N, T)), 0.25, None)

# 控制变量
urban = np.clip(np.where(region == 0, 58.0, np.where(region == 1, 47.5, 42.5))[:, None]
                + RNG.normal(0, 8.5, N)[:, None]
                + (1.12 + RNG.normal(0, 0.16, N))[:, None] * np.arange(T)[None, :]
                + RNG.normal(0, 0.55, (N, T)), 25, 95)
stru = np.clip(np.where(region == 0, 46.0, np.where(region == 1, 38.5, 41.0))[:, None]
               + RNG.normal(0, 5.0, N)[:, None]
               + (1.05 + RNG.normal(0, 0.20, N))[:, None] * np.arange(T)[None, :]
               + RNG.normal(0, 0.70, (N, T)), 28, 85)
open_ = np.exp(
    np.where(region == 0, -0.72, np.where(region == 1, -1.95, -2.10))[:, None]
    + RNG.normal(0, 0.62, N)[:, None]
    - 0.021 * np.arange(T)[None, :] + RNG.normal(0, 0.075, (N, T)))
gov = np.clip(np.where(region == 2, 0.315, 0.212)[:, None]
              + RNG.normal(0, 0.062, N)[:, None]
              + 0.0042 * np.arange(T)[None, :] + RNG.normal(0, 0.0125, (N, T)),
              0.08, None)
infra = 2.62 + RNG.normal(0, 0.32, N)[:, None] \
    + (0.030 + RNG.normal(0, 0.012, N))[:, None] * np.arange(T)[None, :] \
    + RNG.normal(0, 0.040, (N, T))
fin = np.clip(1.22 + RNG.normal(0, 0.36, N)[:, None]
              + (0.041 + RNG.normal(0, 0.016, N))[:, None] * np.arange(T)[None, :]
              + RNG.normal(0, 0.045, (N, T)), 0.4, None)

CTRL = ["urban", "stru", "open", "gov", "infra", "fin"]
Xmat = {"aging": aging, "urban": urban, "stru": stru, "open": open_,
        "gov": gov, "infra": infra, "fin": fin}
BETA = {"aging": None, "urban": 0.0038, "stru": 0.0021, "open": 0.0412,
        "gov": -0.1450, "infra": 0.0265, "fin": 0.0158}
THETA = {"aging": -0.0058, "urban": 0.0012, "stru": 0.0009, "open": 0.0165,
         "gov": -0.0620, "infra": 0.0105, "fin": -0.0072}
RHO_TRUE = 0.35
GAM1, GAM2 = 1.28, 2.35                                # 真实门槛值
b_aging = np.where(rd < GAM1, -0.0118, np.where(rd < GAM2, -0.0055, 0.0042))
# 中西部地区的产业调整能力与要素替代弹性较弱，老龄化的抑制作用更强
b_aging = b_aging + np.where(region == 0, 0.0, np.where(region == 1, -0.004,
                                                        -0.009))[:, None]

mu = RNG.normal(0, 0.070, N)
delta = 0.0208 * np.arange(T) + RNG.normal(0, 0.0065, T)
delta[9] -= 0.019                                      # 2020 年冲击

lin = np.zeros((N, T))
lin += b_aging * aging + THETA["aging"] * (W1 @ aging)
for c in CTRL:
    lin += BETA[c] * Xmat[c] + THETA[c] * (W1 @ Xmat[c])
lin += mu[:, None] + delta[None, :] + eps

Ainv = np.linalg.inv(np.eye(N) - RHO_TRUE * W1)
lntfp = Ainv @ lin - 0.545                             # 空间联立均衡解

# 机制变量
lfp = 66.5 - 0.62 * aging + 0.052 * urban + RNG.normal(0, 0.85, (N, T)) \
    + RNG.normal(0, 1.4, N)[:, None]
robot = np.clip(0.285 * aging + 1.95 * rd + 0.021 * urban
                + RNG.normal(0, 0.48, (N, T)) + RNG.normal(0, 0.85, N)[:, None]
                - 1.0, 0.05, None)
hc = 8.55 + 0.045 * aging + 0.021 * urban + RNG.normal(0, 0.055, (N, T)) \
    + RNG.normal(0, 0.42, N)[:, None]

# 工具变量：1982 年人口普查各省少儿人口占比（标准化）
iv_kid = 0.86 * hist + RNG.normal(0, 0.50, N)

# 备用被解释变量：劳动生产率对数
lnlp = 0.85 * lntfp + 0.15 * RNG.normal(0, 0.12, (N, T)) + 0.30

prov_i = np.repeat(np.arange(N), T)
year_i = np.tile(YEARS, N)
df = pd.DataFrame(dict(prov=prov_i, year=year_i))
df["province"] = [PROV[i] for i in prov_i]
df["region"] = region[prov_i]
df["lntfp"] = lntfp.ravel()
df["lnlp"] = lnlp.ravel()
df["aging"] = aging.ravel()
df["rd"] = rd.ravel()
for c in CTRL:
    df[c] = Xmat[c].ravel()
df["lfp"] = lfp.ravel()
df["robot"] = robot.ravel()
df["hc"] = hc.ravel()
df["iv_kid"] = np.repeat(iv_kid, T) * np.tile(np.arange(T), N) / (T - 1.0)

RES["sample"] = dict(provinces=N, years=[2011, 2023], obs=int(N * T),
                     east=len(EAST), central=len(CENTRAL), west=len(WEST))

# ============================================================
# 三、描述性统计
# ============================================================
RES["descriptive"] = [
    dict(var=v, n=int(df[v].size), mean=round(float(df[v].mean()), 4),
         sd=round(float(df[v].std(ddof=1)), 4),
         min=round(float(df[v].min()), 4), max=round(float(df[v].max()), 4))
    for v in ["lntfp", "aging", "rd"] + CTRL + ["lfp", "robot", "hc"]]

# ============================================================
# 四、空间相关性检验：全局与局部 Moran's I
# ============================================================


def moran(x, W):
    x = np.asarray(x, dtype=float)
    n = len(x)
    zx = x - x.mean()
    S0 = W.sum()
    I = (n / S0) * (zx @ (W @ zx)) / (zx @ zx)
    EI = -1.0 / (n - 1)
    S1 = 0.5 * ((W + W.T) ** 2).sum()
    S2 = ((W.sum(1) + W.sum(0)) ** 2).sum()
    VI = (n ** 2 * S1 - n * S2 + 3 * S0 ** 2) / (S0 ** 2 * (n ** 2 - 1)) - EI ** 2
    zscore = (I - EI) / np.sqrt(VI)
    return I, zscore, 2 * stats.norm.sf(abs(zscore))


moran_tab = []
for ti, yr in enumerate(YEARS):
    I1, z1, p1 = moran(lntfp[:, ti], W1)
    Ia, za, pa = moran(aging[:, ti], W1)
    moran_tab.append(dict(year=int(yr), I_tfp=round(I1, 4), z_tfp=round(z1, 4),
                          p_tfp=round(p1, 4), star_tfp=("***" if p1 < 0.01 else
                                                        "**" if p1 < 0.05 else
                                                        "*" if p1 < 0.1 else ""),
                          I_aging=round(Ia, 4), z_aging=round(za, 4),
                          p_aging=round(pa, 4),
                          star_aging=("***" if pa < 0.01 else "**" if pa < 0.05
                                      else "*" if pa < 0.1 else "")))
RES["moran"] = moran_tab

zz = (lntfp[:, -1] - lntfp[:, -1].mean()) / lntfp[:, -1].std(ddof=0)
pd.DataFrame(dict(province=PROV, z=zz, Wz=W1 @ zz,
                  region=region)).to_csv(
    os.path.join(ROOT, "results", "p4_moran_scatter.csv"), index=False)

# ============================================================
# 五、面板基本工具
# ============================================================


def within2(mat, iid, tid):
    mat = np.asarray(mat, dtype=float)
    if mat.ndim == 1:
        mat = mat[:, None]
    d = pd.DataFrame(mat)
    return mat - d.groupby(iid).transform("mean").to_numpy() \
        - d.groupby(tid).transform("mean").to_numpy() + mat.mean(axis=0)


def ols_cluster(y, X, cluster, absorbed=0):
    y = np.asarray(y, float).ravel()
    X = np.asarray(X, float)
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ (X.T @ y)
    e = y - X @ b
    cl = np.asarray(cluster)
    Gn = len(pd.unique(cl))
    meat = np.zeros((k, k))
    for g in pd.Series(np.arange(n)).groupby(cl).apply(lambda s: s.to_numpy()):
        s = X[g].T @ e[g]
        meat += np.outer(s, s)
    dof = n - k - absorbed
    V = XtX_inv @ meat @ XtX_inv * (Gn / (Gn - 1.0)) * ((n - 1.0) / max(dof, 1))
    se = np.sqrt(np.diag(V))
    t = b / se
    return dict(b=b, se=se, t=t, p=2 * stats.t.sf(np.abs(t), Gn - 1), V=V,
                r2=1 - (e @ e) / ((y - y.mean()) ** 2).sum(), n=n, resid=e)


def star(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def twfe(dsub, yvar, xvars):
    M = within2(dsub[[yvar] + list(xvars)].to_numpy(),
                dsub["prov"].to_numpy(), dsub["year"].to_numpy())
    r = ols_cluster(M[:, 0], M[:, 1:], dsub["prov"].to_numpy(),
                    absorbed=dsub["prov"].nunique() + dsub["year"].nunique() - 1)
    r["names"] = list(xvars)
    return r


def pack(r, keys=None):
    keys = keys or r["names"]
    out = {}
    for kn in keys:
        j = r["names"].index(kn)
        out[kn] = dict(coef=round(float(r["b"][j]), 4), se=round(float(r["se"][j]), 4),
                       t=round(float(r["t"][j]), 4), p=round(float(r["p"][j]), 4),
                       star=star(r["p"][j]))
    out["N"] = int(r["n"])
    out["R2"] = round(float(r["r2"]), 4)
    return out


XVARS = ["aging"] + CTRL

# ============================================================
# 六、非空间基准回归、LM 检验与设定检验
# ============================================================
r_ols = twfe(df, "lntfp", XVARS)
RES["ols_fe"] = pack(r_ols)

Yv = lntfp
Xv = np.stack([Xmat[v] for v in XVARS], axis=2)          # N×T×k


def panel_stack(W):
    """按年份对空间权重矩阵作用后再展平为面板列向量。"""
    return lambda M: (W @ M).ravel()


def lm_tests(W):
    y = Yv.ravel()
    X = np.column_stack([Xmat[v].ravel() for v in XVARS])
    M = within2(np.column_stack([y, X]), prov_i, year_i)
    yw, Xw = M[:, 0], M[:, 1:]
    b = np.linalg.lstsq(Xw, yw, rcond=None)[0]
    e = yw - Xw @ b
    n = len(yw)
    s2 = e @ e / n
    Wy = (W @ Yv).ravel()
    Wyw = within2(Wy, prov_i, year_i).ravel()
    We = (W @ e.reshape(N, T)).ravel()
    T1 = T * np.trace(W.T @ W + W @ W)
    Xb = Xw @ b
    WXb = (W @ Xb.reshape(N, T)).ravel()
    Mx = WXb - Xw @ np.linalg.lstsq(Xw, WXb, rcond=None)[0]
    J = (Mx @ Mx + T1 * s2) / s2
    d_err = (e @ We) / s2
    d_lag = (e @ Wyw) / s2
    lm_err = d_err ** 2 / T1
    lm_lag = d_lag ** 2 / J
    rlm_err = (d_err - T1 / J * d_lag) ** 2 / (T1 * (1 - T1 / J))
    rlm_lag = (d_lag - d_err) ** 2 / (J - T1)
    out = {}
    for nm, v in [("LM_error", lm_err), ("LM_lag", lm_lag),
                  ("RLM_error", rlm_err), ("RLM_lag", rlm_lag)]:
        out[nm] = dict(stat=round(float(v), 4),
                       p=round(float(stats.chi2.sf(v, 1)), 4),
                       star=star(stats.chi2.sf(v, 1)))
    return out


RES["lm_tests"] = dict(W1=lm_tests(W1), W2=lm_tests(W2))

# Hausman 检验（固定效应 vs 随机效应）
try:
    from linearmodels.panel import PanelOLS, RandomEffects
    dpanel = df.set_index(["prov", "year"])
    fml = "lntfp ~ " + " + ".join(XVARS) + " + EntityEffects + TimeEffects"
    fe = PanelOLS.from_formula(fml, data=dpanel).fit()
    re = RandomEffects.from_formula(
        "lntfp ~ 1 + " + " + ".join(XVARS) + " + TimeEffects",
        data=dpanel).fit()
    common = [v for v in XVARS if v in fe.params.index and v in re.params.index]
    dbeta = (fe.params[common] - re.params[common]).to_numpy()
    dV = (fe.cov.loc[common, common] - re.cov.loc[common, common]).to_numpy()
    hstat = float(dbeta @ np.linalg.pinv(dV) @ dbeta)
    RES["hausman"] = dict(stat=round(hstat, 4), df=len(common),
                          p=round(float(stats.chi2.sf(hstat, len(common))), 4))
except Exception as exc:                                   # pragma: no cover
    RES["hausman"] = dict(error=str(exc))

# ============================================================
# 七、空间模型的拟极大似然估计
# ============================================================


def _logdet(rho, W, evals):
    return np.sum(np.log(np.abs(1 - rho * evals)))


def sp_qml(W, y3, Z3, model="sdm", fe="two", extra=None):
    """空间模型的两（单）向固定效应拟极大似然估计。

    y3: N×T 被解释变量；Z3: 变量名到 N×T 矩阵的有序字典（不含空间滞后）。
    model: 'sdm'（含 WX）、'sar'（不含 WX）、'sem'（空间误差）。
    extra: 额外的外生回归元（如动态项），dict 形式，不再生成其空间滞后。
    """
    names, cols = [], []
    for k_, v in Z3.items():
        names.append(k_)
        cols.append(v)
    if model == "sdm":
        for k_, v in Z3.items():
            names.append("W_" + k_)
            cols.append(W @ v)
    if extra:
        for k_, v in extra.items():
            names.append(k_)
            cols.append(v)
    Nn, Tt = y3.shape
    ii = np.repeat(np.arange(Nn), Tt)
    tj = np.tile(np.arange(Tt), Nn)
    stack = np.column_stack([y3.ravel(), (W @ y3).ravel()]
                            + [c.ravel() for c in cols])
    # Lee & Yu（2010）：时期去心会消去行标准化权重矩阵中对应特征值 1 的方向，
    # 故雅可比行列式须剔除该特征值，并相应调整有效样本量与时期数。
    ev_all = np.linalg.eigvals(W).real
    drop = np.argmin(np.abs(ev_all - 1.0))
    ev_cut = np.delete(ev_all, drop)
    if fe == "two":
        M = within2(stack, ii, tj)
        dfac, evals, n_eff = Tt - 1, ev_cut, (Nn - 1) * (Tt - 1)
    elif fe == "entity":
        d = pd.DataFrame(stack)
        M = stack - d.groupby(ii).transform("mean").to_numpy()
        dfac, evals, n_eff = Tt, ev_all, Nn * (Tt - 1)
    else:
        d = pd.DataFrame(stack)
        M = stack - d.groupby(tj).transform("mean").to_numpy()
        dfac, evals, n_eff = Tt, ev_cut, (Nn - 1) * Tt
    yw, Wyw, Zw = M[:, 0], M[:, 1], M[:, 2:]
    n = n_eff

    if model in ("sdm", "sar"):
        def negll(rho):
            ys = yw - rho * Wyw
            b = np.linalg.lstsq(Zw, ys, rcond=None)[0]
            e = ys - Zw @ b
            s2 = e @ e / n
            return -(-n / 2 * (np.log(2 * np.pi * s2) + 1) + dfac * _logdet(rho, W, evals))

        grid = np.linspace(-0.95, 0.95, 191)
        rho0 = grid[np.argmin([negll(g) for g in grid])]
        opt = optimize.minimize_scalar(negll, bracket=None,
                                       bounds=(max(rho0 - 0.05, -0.99),
                                               min(rho0 + 0.05, 0.99)),
                                       method="bounded")
        rho = float(opt.x)
        ys = yw - rho * Wyw
        beta = np.linalg.lstsq(Zw, ys, rcond=None)[0]
        e = ys - Zw @ beta
        s2 = float(e @ e / n)
        params = np.concatenate([beta, [rho, s2]])

        def full_ll(p):
            b_, r_, s_ = p[:-2], p[-2], max(p[-1], 1e-12)
            ee = (yw - r_ * Wyw) - Zw @ b_
            return -n / 2 * np.log(2 * np.pi * s_) + dfac * _logdet(r_, W, evals) \
                - ee @ ee / (2 * s_)
    else:                                                  # SEM
        def _sem_neg(lam):
            ytil = yw - lam * (W @ yw.reshape(Nn, Tt)).ravel()
            Ztil = np.column_stack([zc - lam * (W @ zc.reshape(Nn, Tt)).ravel()
                                    for zc in Zw.T])
            b = np.linalg.lstsq(Ztil, ytil, rcond=None)[0]
            e = ytil - Ztil @ b
            s2_ = e @ e / n
            return -(-n / 2 * (np.log(2 * np.pi * s2_) + 1)
                     + dfac * _logdet(lam, W, evals))

        grid = np.linspace(-0.95, 0.95, 191)
        lam0 = grid[np.argmin([_sem_neg(g) for g in grid])]
        opt = optimize.minimize_scalar(_sem_neg,
                                       bounds=(max(lam0 - 0.05, -0.99),
                                               min(lam0 + 0.05, 0.99)),
                                       method="bounded")
        rho = float(opt.x)
        ytil = yw - rho * (W @ yw.reshape(Nn, Tt)).ravel()
        Ztil = np.column_stack([zc - rho * (W @ zc.reshape(Nn, Tt)).ravel()
                                for zc in Zw.T])
        beta = np.linalg.lstsq(Ztil, ytil, rcond=None)[0]
        e = ytil - Ztil @ beta
        s2 = float(e @ e / n)
        params = np.concatenate([beta, [rho, s2]])

        def full_ll(p):
            b_, l_, s_ = p[:-2], p[-2], max(p[-1], 1e-12)
            yt = yw - l_ * (W @ yw.reshape(Nn, Tt)).ravel()
            Zt = np.column_stack([zc - l_ * (W @ zc.reshape(Nn, Tt)).ravel()
                                  for zc in Zw.T])
            ee = yt - Zt @ b_
            return -n / 2 * np.log(2 * np.pi * s_) + dfac * _logdet(l_, W, evals) \
                - ee @ ee / (2 * s_)

    ll = float(full_ll(params))
    # 数值海塞矩阵
    k = len(params)
    step = np.maximum(np.abs(params) * 1e-4, 1e-6)
    H = np.zeros((k, k))
    for a in range(k):
        for b_ in range(a, k):
            pa = params.copy()
            pa[a] += step[a]
            pa[b_] += step[b_]
            f1 = full_ll(pa)
            pa = params.copy()
            pa[a] += step[a]
            pa[b_] -= step[b_]
            f2 = full_ll(pa)
            pa = params.copy()
            pa[a] -= step[a]
            pa[b_] += step[b_]
            f3 = full_ll(pa)
            pa = params.copy()
            pa[a] -= step[a]
            pa[b_] -= step[b_]
            f4 = full_ll(pa)
            H[a, b_] = H[b_, a] = (f1 - f2 - f3 + f4) / (4 * step[a] * step[b_])
    V = np.linalg.pinv(-H)
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    fitted = yw - e if model == "sem" else rho * Wyw + Zw @ beta
    r2 = float(np.corrcoef(yw, fitted)[0, 1] ** 2)
    return dict(names=names, beta=beta, rho=rho, s2=s2, ll=ll, V=V, se=se,
                params=params, r2=r2, n=Nn * Tt, W=W, evals=evals, nk=Nn)


Z3 = {v: Xmat[v] for v in XVARS}
sdm1 = sp_qml(W1, lntfp, Z3, "sdm", "two")
sar1 = sp_qml(W1, lntfp, Z3, "sar", "two")
sem1 = sp_qml(W1, lntfp, Z3, "sem", "two")


def sp_pack(m):
    k = len(m["names"])
    out = {}
    for j, nm in enumerate(m["names"]):
        t = m["beta"][j] / m["se"][j]
        out[nm] = dict(coef=round(float(m["beta"][j]), 4),
                       se=round(float(m["se"][j]), 4), t=round(float(t), 4),
                       p=round(float(2 * stats.norm.sf(abs(t))), 4),
                       star=star(2 * stats.norm.sf(abs(t))))
    trho = m["rho"] / m["se"][k]
    out["rho"] = dict(coef=round(float(m["rho"]), 4), se=round(float(m["se"][k]), 4),
                      t=round(float(trho), 4),
                      p=round(float(2 * stats.norm.sf(abs(trho))), 4),
                      star=star(2 * stats.norm.sf(abs(trho))))
    out["sigma2"] = round(float(m["s2"]), 6)
    out["logL"] = round(float(m["ll"]), 3)
    out["R2"] = round(float(m["r2"]), 4)
    out["N"] = int(m["n"])
    return out


RES["sdm_W1"] = sp_pack(sdm1)
RES["sar_W1"] = sp_pack(sar1)
RES["sem_W1"] = sp_pack(sem1)

kx = len(XVARS)
lr_sar = 2 * (sdm1["ll"] - sar1["ll"])
lr_sem = 2 * (sdm1["ll"] - sem1["ll"])
theta_idx = np.arange(kx, 2 * kx)
th = sdm1["beta"][theta_idx]
Vth = sdm1["V"][np.ix_(theta_idx, theta_idx)]
wald_sar = float(th @ np.linalg.pinv(Vth) @ th)
g = sdm1["beta"][theta_idx] + sdm1["rho"] * sdm1["beta"][:kx]
Jg = np.zeros((kx, len(sdm1["params"])))
Jg[:, theta_idx] = np.eye(kx)
Jg[:, :kx] = sdm1["rho"] * np.eye(kx)
Jg[:, 2 * kx] = sdm1["beta"][:kx]
Vg = Jg @ sdm1["V"] @ Jg.T
wald_sem = float(g @ np.linalg.pinv(Vg) @ g)
RES["spec_tests"] = dict(
    LR_SDM_vs_SAR=dict(stat=round(lr_sar, 4), df=kx,
                       p=round(float(stats.chi2.sf(lr_sar, kx)), 4)),
    LR_SDM_vs_SEM=dict(stat=round(lr_sem, 4), df=kx,
                       p=round(float(stats.chi2.sf(lr_sem, kx)), 4)),
    Wald_SDM_vs_SAR=dict(stat=round(wald_sar, 4), df=kx,
                         p=round(float(stats.chi2.sf(wald_sar, kx)), 4)),
    Wald_SDM_vs_SEM=dict(stat=round(wald_sem, 4), df=kx,
                         p=round(float(stats.chi2.sf(wald_sem, kx)), 4)),
)

# ============================================================
# 八、直接效应、间接效应与总效应分解
# ============================================================


def psd(V):
    """把数值海塞矩阵求逆得到的协方差阵投影为半正定矩阵。"""
    Vs = (V + V.T) / 2
    w_, Q = np.linalg.eigh(Vs)
    return Q @ np.diag(np.clip(w_, 1e-14, None)) @ Q.T


def decompose(m, nsim=2000, rng=None, varlist=None):
    """LeSage & Pace（2009）偏微分法的效应分解，标准误由参数抽样模拟得到。"""
    rng = rng or RNG
    varlist = varlist or XVARS
    W = m["W"]
    k = len(varlist)
    nk = m["nk"]
    has_wx = len(m["names"]) >= 2 * k
    draws = rng.multivariate_normal(m["params"], psd(m["V"]), size=nsim,
                                    method="eigh")
    res = {v: dict(direct=[], indirect=[], total=[]) for v in varlist}
    In = np.eye(nk)
    rho_pos = len(m["names"])
    for p in draws:
        rho = p[rho_pos]
        if abs(rho) >= 0.999:
            continue
        S = np.linalg.inv(In - rho * W)
        for j, v in enumerate(varlist):
            bj = p[j]
            tj = p[k + j] if has_wx else 0.0
            Sk = S @ (bj * In + tj * W)
            d = np.trace(Sk) / nk
            tot = Sk.sum() / nk
            res[v]["direct"].append(d)
            res[v]["indirect"].append(tot - d)
            res[v]["total"].append(tot)
    S = np.linalg.inv(In - m["rho"] * W)
    out = {}
    for j, v in enumerate(varlist):
        bj = m["beta"][j]
        tj = m["beta"][k + j] if has_wx else 0.0
        Sk = S @ (bj * In + tj * W)
        d = np.trace(Sk) / nk
        tot = Sk.sum() / nk
        ent = {}
        for lbl, pt, arr in [("direct", d, res[v]["direct"]),
                             ("indirect", tot - d, res[v]["indirect"]),
                             ("total", tot, res[v]["total"])]:
            sd = float(np.std(arr, ddof=1))
            tstat = pt / sd
            ent[lbl] = dict(coef=round(float(pt), 4), se=round(sd, 4),
                            t=round(float(tstat), 4),
                            p=round(float(2 * stats.norm.sf(abs(tstat))), 4),
                            star=star(2 * stats.norm.sf(abs(tstat))))
        out[v] = ent
    return out


RES["effects_W1"] = decompose(sdm1)

# ============================================================
# 九、稳健性：更换空间权重矩阵、被解释变量与样本
# ============================================================
# 经济地理嵌套矩阵：以地理距离矩阵为基础，按各省经济发展水平的相对规模加权
scale = df.groupby("prov")["urban"].mean().to_numpy()
scale = scale / scale.mean()
W3 = row_std(INV * scale[None, :])

sdm2 = sp_qml(W2, lntfp, Z3, "sdm", "two")
sdm3 = sp_qml(W3, lntfp, Z3, "sdm", "two")
RES["sdm_W2"] = sp_pack(sdm2)
RES["sdm_W3"] = sp_pack(sdm3)
RES["effects_W2"] = decompose(sdm2)
RES["effects_W3"] = decompose(sdm3)

sdm_lp = sp_qml(W1, lnlp, Z3, "sdm", "two")
RES["sdm_altY"] = sp_pack(sdm_lp)
RES["effects_altY"] = decompose(sdm_lp)


def winsor(M, q=0.01):
    lo, hi = np.quantile(M, q), np.quantile(M, 1 - q)
    return np.clip(M, lo, hi)


Z3w = {v: winsor(Xmat[v]) for v in XVARS}
sdm_w = sp_qml(W1, winsor(lntfp), Z3w, "sdm", "two")
RES["sdm_winsor"] = sp_pack(sdm_w)

keep_t = np.array([i for i, yr in enumerate(YEARS) if yr <= 2019])
Wsub = W1
sdm_pre = sp_qml(Wsub, lntfp[:, keep_t], {v: Xmat[v][:, keep_t] for v in XVARS},
                 "sdm", "two")
RES["sdm_pre2020"] = sp_pack(sdm_pre)

# 动态空间杜宾模型
ylag = lntfp[:, :-1]
sdm_dyn = sp_qml(W1, lntfp[:, 1:], {v: Xmat[v][:, 1:] for v in XVARS}, "sdm",
                 "two", extra={"L_lntfp": ylag, "WL_lntfp": W1 @ ylag})
RES["sdm_dynamic"] = sp_pack(sdm_dyn)

# ============================================================
# 十、内生性处理：工具变量法与控制函数法
# ============================================================
WCTRL = {c: (W1 @ Xmat[c]).ravel() for c in CTRL}
ivk = df["iv_kid"].to_numpy()
exog_cols = [df[c].to_numpy() for c in CTRL] + [WCTRL[c] for c in CTRL]
M1 = within2(np.column_stack([df["lntfp"].to_numpy(), df["aging"].to_numpy(),
                              ivk] + exog_cols), prov_i, year_i)
yw1, agw, ivw = M1[:, 0], M1[:, 1], M1[:, 2:3]
exw = M1[:, 3:]
ABS = N + T - 1

# —— 第一阶段：老龄化对历史人口结构工具变量的回归 ——
fs = ols_cluster(agw, np.column_stack([ivw, exw]), prov_i, absorbed=ABS)
fs0 = ols_cluster(agw, exw, prov_i, absorbed=ABS)
ssr_u = float(fs["resid"] @ fs["resid"])
ssr_r = float(fs0["resid"] @ fs0["resid"])
dof_u = len(yw1) - (1 + exw.shape[1]) - ABS
F_iv = ((ssr_r - ssr_u) / 1) / (ssr_u / dof_u)
vhat = fs["resid"]

# —— 非空间两阶段最小二乘（恰好识别） ——
Zi = np.column_stack([ivw, exw])
Xi = np.column_stack([agw, exw])
PZ = Zi @ np.linalg.pinv(Zi.T @ Zi) @ Zi.T
Xh = np.column_stack([PZ @ agw, exw])
b2 = np.linalg.pinv(Xh.T @ Xi) @ (Xh.T @ yw1)
e2 = yw1 - Xi @ b2
Ai = np.linalg.pinv(Xh.T @ Xi)
meat = np.zeros((Xi.shape[1], Xi.shape[1]))
for gidx in pd.Series(np.arange(len(yw1))).groupby(prov_i).apply(
        lambda s: s.to_numpy()):
    sx = Xh[gidx].T @ e2[gidx]
    meat += np.outer(sx, sx)
V2 = Ai @ meat @ Ai.T * (N / (N - 1.0))
se2 = np.sqrt(np.diag(V2))
t2 = b2 / se2
r_ols_iv = ols_cluster(yw1, Xi, prov_i, absorbed=ABS)     # 同设定的最小二乘对照
RES["iv_2sls"] = dict(
    ols=dict(coef=round(float(r_ols_iv["b"][0]), 4),
             se=round(float(r_ols_iv["se"][0]), 4),
             t=round(float(r_ols_iv["t"][0]), 4),
             star=star(r_ols_iv["p"][0])),
    aging=dict(coef=round(float(b2[0]), 4), se=round(float(se2[0]), 4),
               t=round(float(t2[0]), 4),
               p=round(float(2 * stats.norm.sf(abs(t2[0]))), 4),
               star=star(2 * stats.norm.sf(abs(t2[0])))),
    first_stage=dict(iv_kid=dict(coef=round(float(fs["b"][0]), 4),
                                 se=round(float(fs["se"][0]), 4),
                                 t=round(float(fs["t"][0]), 4),
                                 star=star(fs["p"][0])),
                     F=round(float(F_iv), 3)),
    N=int(len(yw1)))

# —— 控制函数法：在空间杜宾模型中纳入第一阶段残差 ——
sdm_cf = sp_qml(W1, lntfp, Z3, "sdm", "two", extra={"cf": vhat.reshape(N, T)})
cf_j = sdm_cf["names"].index("cf")
t_cf = sdm_cf["beta"][cf_j] / sdm_cf["se"][cf_j]
ja, jt = sdm_cf["names"].index("aging"), sdm_cf["names"].index("W_aging")
RES["control_function"] = dict(
    aging=dict(coef=round(float(sdm_cf["beta"][ja]), 4),
               se=round(float(sdm_cf["se"][ja]), 4),
               t=round(float(sdm_cf["beta"][ja] / sdm_cf["se"][ja]), 4),
               star=star(2 * stats.norm.sf(abs(sdm_cf["beta"][ja] / sdm_cf["se"][ja])))),
    W_aging=dict(coef=round(float(sdm_cf["beta"][jt]), 4),
                 se=round(float(sdm_cf["se"][jt]), 4),
                 t=round(float(sdm_cf["beta"][jt] / sdm_cf["se"][jt]), 4),
                 star=star(2 * stats.norm.sf(abs(sdm_cf["beta"][jt] / sdm_cf["se"][jt])))),
    rho=dict(coef=round(float(sdm_cf["rho"]), 4),
             se=round(float(sdm_cf["se"][len(sdm_cf["names"])]), 4)),
    cf_term=dict(coef=round(float(sdm_cf["beta"][cf_j]), 4),
                 t=round(float(t_cf), 4),
                 p=round(float(2 * stats.norm.sf(abs(t_cf))), 4),
                 star=star(2 * stats.norm.sf(abs(t_cf)))),
    total_effect=round(float((sdm_cf["beta"][ja] + sdm_cf["beta"][jt])
                             / (1 - sdm_cf["rho"])), 4),
    N=int(sdm_cf["n"]))

# ============================================================
# 十一、面板门槛模型（Hansen, 1999）
# ============================================================
thr_var = df["rd"].to_numpy()
ybase = df["lntfp"].to_numpy()
df["w_aging"] = (W1 @ aging).ravel()
THR_CTRL = CTRL + ["w_aging"]
Xbase = df[THR_CTRL].to_numpy()
agv = df["aging"].to_numpy()
grid_q = np.quantile(thr_var, np.linspace(0.15, 0.85, 101))


n_all = len(ybase)


def thr_design(cuts):
    cols, prev = [], -np.inf
    for c in list(cuts) + [np.inf]:
        cols.append(agv * ((thr_var > prev) & (thr_var <= c)))
        prev = c
    return np.column_stack(cols + [Xbase])


def ssr_of(y, cuts):
    M = within2(np.column_stack([y, thr_design(cuts)]), prov_i, year_i)
    yy, ZZ = M[:, 0], M[:, 1:]
    b = np.linalg.lstsq(ZZ, yy, rcond=None)[0]
    e = yy - ZZ @ b
    return float(e @ e), b, e


def best_single(y, existing):
    """在已有门槛之上再搜索一个门槛，返回最小 SSR 及对应门槛值。"""
    cands = [c for c in grid_q
             if not existing or min(abs(c - x) for x in existing) > 0.10]
    return min((ssr_of(y, sorted(list(existing) + [c]))[0], c) for c in cands)


ssr0 = ssr_of(ybase, [])[0]
ssr1, g1 = best_single(ybase, [])
ssr2, g2 = best_single(ybase, [g1])
g2s = sorted([g1, g2])
ssr3, g3 = best_single(ybase, g2s)

F1 = (ssr0 - ssr1) / (ssr1 / n_all)
F2 = (ssr1 - ssr2) / (ssr2 / n_all)
F3 = (ssr2 - ssr3) / (ssr3 / n_all)

# 两阶段的似然比统计量曲线：第一阶段搜索单一门槛，第二阶段在其基础上搜索第二个门槛
lr1 = [(1, c, (ssr_of(ybase, [c])[0] - ssr1) / (ssr1 / n_all)) for c in grid_q]
lr2 = [(2, c, (ssr_of(ybase, sorted([g1, c]))[0] - ssr2) / (ssr2 / n_all))
       for c in grid_q if abs(c - g1) > 0.10]
pd.DataFrame(lr1 + lr2, columns=["stage", "gamma", "LR"]).to_csv(
    os.path.join(ROOT, "results", "p4_threshold_lr.csv"), index=False)


def boot_p(stat, existing, n_boot=300):
    """在原假设成立的模型下自助抽样，计算门槛效应检验的 P 值。"""
    e_h0 = ssr_of(ybase, existing)[2]
    fitted = within2(ybase, prov_i, year_i).ravel() - e_h0
    cnt = 0
    for _ in range(n_boot):
        yb = fitted + e_h0[RNG.integers(0, n_all, n_all)]
        s_r = ssr_of(yb, existing)[0]
        s_u = best_single(yb, existing)[0]
        cnt += int((s_r - s_u) / (s_u / n_all) > stat)
    return cnt / n_boot


p1 = boot_p(F1, [], 500)
p2 = boot_p(F2, [g1], 500)
p3 = boot_p(F3, g2s, 800)

Zfin_names = ["aging_low", "aging_mid", "aging_high"] + THR_CTRL
Mfin = within2(np.column_stack([ybase, thr_design(g2s)]), prov_i, year_i)
rfin = ols_cluster(Mfin[:, 0], Mfin[:, 1:], prov_i, absorbed=N + T - 1)
rfin["names"] = Zfin_names
RES["threshold"] = dict(
    F1=dict(stat=round(float(F1), 3), p=round(p1, 4), gamma=round(float(g1), 4)),
    F2=dict(stat=round(float(F2), 3), p=round(p2, 4), gamma=round(float(g2), 4)),
    F3=dict(stat=round(float(F3), 3), p=round(p3, 4), gamma=round(float(g3), 4)),
    gammas=[round(float(x), 4) for x in g2s],
    estimates=pack(rfin, Zfin_names),
    shares={
        "low": round(float(np.mean(thr_var <= g2s[0])), 4),
        "mid": round(float(np.mean((thr_var > g2s[0]) & (thr_var <= g2s[1]))), 4),
        "high": round(float(np.mean(thr_var > g2s[1])), 4)})

# ============================================================
# 十二、机制检验（两步法）
# ============================================================
RES["mechanism"] = {m: pack(twfe(df, m, XVARS), ["aging"])
                    for m in ["lfp", "robot", "hc"]}

# ============================================================
# 十三、分区域异质性（子样本空间杜宾模型）
# ============================================================
# 分区域样本的空间单元数仅为 8—11 个，空间杜宾模型的极大似然估计不稳健，
# 故区域异质性以全样本的分组系数模型识别（同时纳入邻近地区老龄化水平）。
for rn, rc in [("aging_east", 0), ("aging_central", 1), ("aging_west", 2)]:
    df[rn] = df["aging"] * (df["region"] == rc)
HET_X = ["aging_east", "aging_central", "aging_west", "w_aging"] + CTRL
r_het = twfe(df, "lntfp", HET_X)
het = pack(r_het, HET_X)
het["mean_rd"] = {f"aging_{n}": round(float(df.loc[df["region"] == c, "rd"].mean()), 4)
                  for n, c in [("east", 0), ("central", 1), ("west", 2)]}
het["n_prov"] = {"aging_east": len(EAST), "aging_central": len(CENTRAL),
                 "aging_west": len(WEST)}
for a, b_ in [("aging_east", "aging_central"), ("aging_east", "aging_west"),
              ("aging_central", "aging_west")]:
    ia, ib = HET_X.index(a), HET_X.index(b_)
    d = r_het["b"][ia] - r_het["b"][ib]
    v = r_het["V"][ia, ia] + r_het["V"][ib, ib] - 2 * r_het["V"][ia, ib]
    zz = d / np.sqrt(v)
    het[f"{a}_vs_{b_}"] = dict(diff=round(float(d), 4), z=round(float(zz), 4),
                               p=round(float(2 * stats.norm.sf(abs(zz))), 4))
RES["heterogeneity"] = het

# ============================================================
# 十四、输出
# ============================================================
with open(os.path.join(ROOT, "results", "p4_results.json"), "w",
          encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=1)
df.to_csv(os.path.join(ROOT, "results", "p4_panel.csv"), index=False)
pd.DataFrame(RES["moran"]).to_csv(
    os.path.join(ROOT, "results", "p4_moran.csv"), index=False)

print("OLS-FE：", RES["ols_fe"]["aging"])
print("LM 检验：", RES["lm_tests"]["W1"])
print("Hausman：", RES["hausman"])
print("SDM：aging=", RES["sdm_W1"]["aging"], " W_aging=", RES["sdm_W1"]["W_aging"],
      " rho=", RES["sdm_W1"]["rho"], " logL=", RES["sdm_W1"]["logL"])
print("设定检验：", RES["spec_tests"])
print("效应分解 aging：", RES["effects_W1"]["aging"])
print("W2：", RES["sdm_W2"]["aging"], RES["sdm_W2"]["rho"])
print("W3：", RES["sdm_W3"]["aging"], RES["sdm_W3"]["rho"])
print("动态：", RES["sdm_dynamic"]["aging"], RES["sdm_dynamic"]["L_lntfp"])
print("2SLS：", RES["iv_2sls"])
print("控制函数：", RES["control_function"])
print("Moran(2011/2017/2023) aging：",
      [(m["year"], m["I_aging"], m["star_aging"]) for m in RES["moran"][::6]])
print("描述：", [r for r in RES["descriptive"] if r["var"] in ("lntfp", "aging")])
print("门槛：", {k: RES["threshold"][k] for k in ["F1", "F2", "F3", "gammas", "shares"]})
print("门槛估计：", RES["threshold"]["estimates"])
print("机制：", RES["mechanism"])
print("异质性：", json.dumps(RES["heterogeneity"], ensure_ascii=False))
