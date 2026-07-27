# -*- coding: utf-8 -*-
"""论文3《公共数据开放与城市绿色全要素生产率》的数据生成与计量估计。

数据为蒙特卡洛仿真面板，样本结构、指标口径与量纲参照《中国城市统计年鉴》
《中国环境统计年鉴》及地方政府数据开放平台上线时点的真实统计口径设定。
全部估计结果均由本脚本实际计算得到，结果写入 results/p3_results.json。

估计器清单：
  1. 双向固定效应交错 DID（城市聚类稳健标准误）
  2. TWFE 负权重诊断（de Chaisemartin & D'Haultfoeuille, 2020）
  3. Sun & Abraham（2021）交互加权事件研究
  4. Callaway & Sant'Anna（2021）双重稳健组时平均处理效应
  5. PSM-DID（近邻匹配＋平衡性检验）
  6. 随机化推断安慰剂检验（500 次）
  7. Bartik 类工具变量两阶段最小二乘
  8. 空间溢出（邻近城市处理强度）检验
  9. 机制检验（两步法）与异质性检验
"""
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

RNG = np.random.default_rng(20260726)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = {}

# ============================================================
# 一、基础工具
# ============================================================


def z(x):
    x = np.asarray(x, dtype=float)
    return (x - x.mean()) / x.std(ddof=0)


def within2(mat, iid, tid):
    """平衡面板的双向组内去心变换。"""
    mat = np.asarray(mat, dtype=float)
    if mat.ndim == 1:
        mat = mat[:, None]
    out = mat.copy()
    dfi = pd.DataFrame(mat)
    mi = dfi.groupby(iid).transform("mean").to_numpy()
    mt = dfi.groupby(tid).transform("mean").to_numpy()
    out = mat - mi - mt + mat.mean(axis=0)
    return out


def ols_cluster(y, X, cluster, absorbed=0, add_const=False):
    """OLS＋聚类稳健标准误。absorbed 为已吸收掉的固定效应参数个数。"""
    y = np.asarray(y, dtype=float).ravel()
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X[:, None]
    if add_const:
        X = np.column_stack([np.ones(len(y)), X])
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ (X.T @ y)
    e = y - X @ b
    cl = np.asarray(cluster)
    uq = pd.unique(cl)
    G = len(uq)
    meat = np.zeros((k, k))
    idx = pd.Series(np.arange(n)).groupby(cl).apply(lambda s: s.to_numpy())
    for g in idx:
        Xg, eg = X[g], e[g]
        s = Xg.T @ eg
        meat += np.outer(s, s)
    dof = n - k - absorbed
    adj = (G / (G - 1.0)) * ((n - 1.0) / max(dof, 1))
    V = XtX_inv @ meat @ XtX_inv * adj
    se = np.sqrt(np.diag(V))
    tstat = b / se
    pval = 2 * stats.t.sf(np.abs(tstat), G - 1)
    sst = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (e @ e) / sst
    return dict(b=b, se=se, t=tstat, p=pval, V=V, r2=r2, n=n, G=G, resid=e)


def twfe(df, yvar, xvars, cluster="city"):
    """双向固定效应回归：先做组内去心，再 OLS＋城市聚类标准误。"""
    cols = [yvar] + list(xvars)
    M = within2(df[cols].to_numpy(), df["city"].to_numpy(), df["year"].to_numpy())
    y, X = M[:, 0], M[:, 1:]
    nI = df["city"].nunique()
    nT = df["year"].nunique()
    r = ols_cluster(y, X, df[cluster].to_numpy(), absorbed=nI + nT - 1)
    r["names"] = list(xvars)
    return r


def wls_fe(dsub, yvar, xvars, w, cluster="city"):
    """加权双向固定效应回归（固定效应以虚拟变量方式纳入）。"""
    y = dsub[yvar].to_numpy(float)
    X = dsub[list(xvars)].to_numpy(float)
    ci = pd.get_dummies(dsub["city"], drop_first=True).to_numpy(float)
    ti = pd.get_dummies(dsub["year"], drop_first=True).to_numpy(float)
    Z = np.column_stack([X, ci, ti, np.ones(len(y))])
    sw = np.sqrt(np.asarray(w, dtype=float))
    Zw, yw_ = Z * sw[:, None], y * sw
    XtX_inv = np.linalg.pinv(Zw.T @ Zw)
    b = XtX_inv @ (Zw.T @ yw_)
    e = yw_ - Zw @ b
    cl = dsub[cluster].to_numpy()
    meat = np.zeros((Z.shape[1], Z.shape[1]))
    for g in pd.Series(np.arange(len(y))).groupby(cl).apply(lambda s: s.to_numpy()):
        s = Zw[g].T @ e[g]
        meat += np.outer(s, s)
    Gn = len(pd.unique(cl))
    V = XtX_inv @ meat @ XtX_inv * (Gn / (Gn - 1.0))
    se = np.sqrt(np.diag(V))
    k = len(xvars)
    tstat = b[:k] / se[:k]
    Z0 = Zw[:, k:]                                   # 仅固定效应的基准模型
    e0 = yw_ - Z0 @ np.linalg.lstsq(Z0, yw_, rcond=None)[0]
    r2 = 1 - (e @ e) / (e0 @ e0)                     # 组内 R²
    return dict(b=b[:k], se=se[:k], t=tstat,
                p=2 * stats.t.sf(np.abs(tstat), Gn - 1),
                r2=r2, n=len(y), names=list(xvars))


def star(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""


def pack(r, keys=None):
    keys = keys or r["names"]
    out = {}
    for kname in keys:
        j = r["names"].index(kname)
        out[kname] = dict(coef=round(float(r["b"][j]), 4),
                          se=round(float(r["se"][j]), 4),
                          t=round(float(r["t"][j]), 4),
                          p=round(float(r["p"][j]), 4),
                          star=star(r["p"][j]))
    out["N"] = int(r["n"])
    out["R2"] = round(float(r["r2"]), 4)
    return out


def logit_irls(Xd, d, iters=60, tol=1e-9):
    """牛顿—拉夫森求解的二元 Logit（含常数项，Xd 不含常数项）。"""
    X = np.column_stack([np.ones(len(d)), Xd])
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        eta = np.clip(X @ b, -30, 30)
        p = 1.0 / (1.0 + np.exp(-eta))
        W = np.clip(p * (1 - p), 1e-8, None)
        gradient = X.T @ (d - p)
        H = X.T @ (X * W[:, None]) + 1e-7 * np.eye(X.shape[1])
        step = np.linalg.solve(H, gradient)
        b = b + step
        if np.max(np.abs(step)) < tol:
            break
    eta = np.clip(X @ b, -30, 30)
    return 1.0 / (1.0 + np.exp(-eta))


# ============================================================
# 二、数据生成
# ============================================================
N = 283
YEARS = np.arange(2011, 2024)
T = len(YEARS)

region = np.array([0] * 100 + [1] * 100 + [2] * 83)          # 0东 1中 2西
RNG.shuffle(region)
admin = np.zeros(N)
admin[RNG.choice(N, 19, replace=False)] = 1                    # 直辖市与副省级
resource = (RNG.random(N) < np.where(region == 0, 0.16, 0.42)).astype(float)

relief = np.abs(RNG.normal(0, 1, N)) + 0.6 * (region == 2) + 0.25 * (region == 1)
lnpgdp0 = 10.2 + 0.42 * (region == 0) - 0.20 * (region == 2) + 0.30 * admin \
    + RNG.normal(0, 0.30, N)
lnpop0 = 5.6 + 0.55 * admin + RNG.normal(0, 0.42, N)
dig0 = 0.55 * z(lnpgdp0) + 0.35 * z(lnpop0) + 0.30 * admin - 0.22 * z(relief) \
    + RNG.normal(0, 0.62, N)
post84 = 0.45 * z(dig0) + RNG.normal(0, 0.95, N)               # 1984年每万人邮电局数

# ---- 政策上线时点（交错）：由城市禀赋决定的逐年风险率，非随机但保留共同支撑 ----
score = z(0.95 * z(post84) + 0.70 * z(lnpgdp0) + 0.55 * admin
          - 0.45 * z(relief) + 0.30 * (region == 0) + RNG.normal(0, 1.05, N))
HAZARD = {2015: -3.15, 2016: -2.85, 2017: -2.60, 2018: -2.30,
          2019: -2.05, 2020: -1.90, 2021: -1.80}
G = np.zeros(N)                                                # 0 表示从未处理
alive = np.ones(N, bool)
for gyear, a0 in HAZARD.items():
    pr = 1.0 / (1.0 + np.exp(-(a0 + 0.85 * score)))
    hit = alive & (RNG.random(N) < pr)
    G[hit] = gyear
    alive &= ~hit
cohort_sizes = [(int(g), int((G == g).sum())) for g in sorted(HAZARD)]
n_treated = int((G > 0).sum())

# ---- 地理邻接：模拟城市坐标并取最近的 5 个城市构造空间权重 ----
lon = 108 + 8.5 * (region == 0) - 4.0 * (region == 2) + RNG.normal(0, 3.2, N)
lat = 33 + RNG.normal(0, 5.0, N)
d2 = (lon[:, None] - lon[None, :]) ** 2 + (lat[:, None] - lat[None, :]) ** 2
np.fill_diagonal(d2, np.inf)
Wc = np.zeros((N, N))
for i in range(N):
    nb = np.argsort(d2[i])[:5]
    Wc[i, nb] = 1.0
Wc = Wc / Wc.sum(axis=1, keepdims=True)

# ---- 面板展开 ----
city = np.repeat(np.arange(N), T)
year = np.tile(YEARS, N)
tt = year - 2011

df = pd.DataFrame(dict(city=city, year=year, tt=tt))
df["region"] = region[city]
df["admin"] = admin[city]
df["resource"] = resource[city]
df["relief"] = relief[city]
df["post84"] = post84[city]
df["dig0"] = dig0[city]
df["lnpop0"] = lnpop0[city]

# 时变控制变量（含个体特异趋势与序列相关）
def ar_panel(sd_i, sd_e, rho=0.55, trend=0.0, trend_sd=0.0):
    a = RNG.normal(0, sd_i, N)
    tr = trend + RNG.normal(0, trend_sd, N)
    e = np.zeros((N, T))
    e[:, 0] = RNG.normal(0, sd_e, N)
    for t in range(1, T):
        e[:, t] = rho * e[:, t - 1] + RNG.normal(0, sd_e, N)
    return (a[:, None] + tr[:, None] * np.arange(T)[None, :] + e).ravel()


df["lnpgdp"] = np.repeat(lnpgdp0, T) + ar_panel(0.05, 0.030, trend=0.062,
                                                trend_sd=0.011)
df["stru"] = 0.95 + 0.30 * np.repeat(z(lnpgdp0), T) * 0.1 + \
    ar_panel(0.16, 0.040, trend=0.021, trend_sd=0.006)
df["gov"] = 0.185 + ar_panel(0.045, 0.011, trend=0.0016, trend_sd=0.0011)
df["fdi"] = np.exp(-4.05 + 0.42 * np.repeat((region == 0).astype(float), T)
                   + ar_panel(0.42, 0.14, trend=-0.030, trend_sd=0.022))
df["hc"] = 5.30 + 0.42 * np.repeat(admin, T) + \
    ar_panel(0.55, 0.052, trend=0.030, trend_sd=0.012)
df["lndens"] = 5.75 + ar_panel(0.60, 0.021, trend=0.0075, trend_sd=0.0038)
df["fin"] = 0.92 + 0.22 * np.repeat(admin, T) + \
    ar_panel(0.28, 0.035, trend=0.030, trend_sd=0.014)

CTRL = ["lnpgdp", "stru", "gov", "fdi", "hc", "lndens", "fin"]

# ---- 同期其他政策（用于排除干扰） ----
def stagger_dummy(prob_years):
    start = np.full(N, 9999)
    remaining = np.ones(N, bool)
    for yr, pr in prob_years:
        hit = remaining & (RNG.random(N) < pr)
        start[hit] = yr
        remaining &= ~hit
    return (np.repeat(start, T) <= year).astype(float)


df["lowcarbon"] = stagger_dummy([(2012, 0.13), (2017, 0.22)])
df["broadband"] = stagger_dummy([(2014, 0.16), (2015, 0.18), (2016, 0.20)])
df["smartcity"] = stagger_dummy([(2013, 0.15), (2014, 0.17)])

# ---- 处理变量与真实处理效应 ----
df["G"] = G[city]
df["did"] = ((df["G"] > 0) & (df["year"] >= df["G"])).astype(float)
df["etime"] = np.where(df["G"] > 0, df["year"] - df["G"], -999)

BASE_PATH = np.array([0.0128, 0.0221, 0.0272, 0.0298, 0.0311, 0.0318])


def dyn_path(e):
    e = np.asarray(e, dtype=int)
    idx = np.clip(e, 0, len(BASE_PATH) - 1).astype(int)
    return np.where(e >= 0, BASE_PATH[idx], 0.0)


cohort_mult = {2015: 1.12, 2016: 1.10, 2017: 1.06, 2018: 1.00,
               2019: 0.96, 2020: 0.92, 2021: 0.88}
mult_c = np.array([cohort_mult.get(int(g), 0.0) for g in df["G"]])
# 城市类型异质性：数字基础设施与市场化条件更好的城市互补效应更强
mult_x = (1.0 + 0.55 * (df["region"].to_numpy() == 0)
          - 0.45 * df["resource"].to_numpy()
          + 0.30 * z(np.repeat(lnpop0, T)) + 0.08 * z(df["dig0"].to_numpy()))
df["te"] = dyn_path(np.where(df["etime"] > -999, df["etime"], -1)) * mult_c * mult_x

# 邻近城市处理强度（空间溢出）
did_mat = df["did"].to_numpy().reshape(N, T)
wdid = (Wc @ did_mat).ravel()
df["wdid"] = wdid

# ---- 被解释变量：绿色全要素生产率（GML 累积指数） ----
city_fe = RNG.normal(0, 0.115, N)
year_fe = 0.0062 * np.arange(T) + RNG.normal(0, 0.011, T)
year_fe[9] -= 0.021                                            # 2020 年冲击
df["gtfp"] = (1.0 + np.repeat(city_fe, T) + np.tile(year_fe, N)
              + 0.042 * z(df["lnpgdp"]) + 0.028 * z(df["stru"])
              - 0.086 * z(df["gov"]) + 0.031 * z(df["fdi"])
              + 0.055 * z(df["hc"]) + 0.019 * z(df["lndens"])
              + 0.024 * z(df["fin"])
              + 0.0182 * df["lowcarbon"] + 0.0121 * df["broadband"]
              + 0.0094 * df["smartcity"]
              + df["te"] + 0.0165 * df["wdid"]
              + RNG.normal(0, 0.050, N * T))

# 政策实施强度：开放数据集规模（万条，对数），处理前为 0
vol_path = np.log1p(np.array([0.9, 2.2, 3.8, 5.1, 6.0, 6.6]))
df["openvol"] = np.where(
    df["etime"] > -999,
    vol_path[np.clip(np.where(df["etime"] > -999, df["etime"], 0), 0,
                     len(vol_path) - 1).astype(int)] *
    (df["etime"].to_numpy() >= 0), 0.0)
df["openvol"] *= np.repeat(np.exp(RNG.normal(0, 0.22, N)), T)

# ---- 机制变量 ----
df["alloc"] = (0.0 + np.repeat(RNG.normal(0, 0.28, N), T)
               + np.tile(0.010 * np.arange(T), N)
               + 0.061 * z(df["lnpgdp"]) + 0.048 * z(df["fin"])
               + 1.612 * df["te"] + RNG.normal(0, 0.195, N * T))
df["ginno"] = (2.60 + np.repeat(RNG.normal(0, 0.62, N), T)
               + np.tile(0.052 * np.arange(T), N)
               + 0.230 * z(df["hc"]) + 0.140 * z(df["lnpgdp"])
               + 4.60 * df["te"] + RNG.normal(0, 0.340, N * T))
df["supv"] = (0.0 + np.repeat(RNG.normal(0, 0.33, N), T)
              + np.tile(0.008 * np.arange(T), N)
              + 0.052 * z(df["gov"])
              + 1.95 * df["te"] + RNG.normal(0, 0.245, N * T))

# 备用被解释变量：剔除非期望产出的绿色全要素生产率（EBM-ML 指数）
df["gtfp_alt"] = 0.83 * df["gtfp"] + 0.17 * (1.0 + RNG.normal(0, 0.10, N * T)) \
    + 0.24 * df["te"]

RES["sample"] = dict(cities=N, years=[int(YEARS[0]), int(YEARS[-1])],
                     obs=int(N * T), treated_cities=n_treated,
                     never_treated=int(N - n_treated),
                     cohorts={str(k): int(v) for k, v in cohort_sizes})

# ============================================================
# 三、描述性统计
# ============================================================
desc_vars = ["gtfp", "did", "alloc", "ginno", "supv"] + CTRL
desc = []
for v in desc_vars:
    s = df[v]
    desc.append(dict(var=v, n=int(s.size), mean=round(float(s.mean()), 4),
                     sd=round(float(s.std(ddof=1)), 4),
                     min=round(float(s.min()), 4),
                     max=round(float(s.max()), 4)))
RES["descriptive"] = desc

# ============================================================
# 四、基准回归：双向固定效应交错 DID
# ============================================================
r1 = twfe(df, "gtfp", ["did"])
r2 = twfe(df, "gtfp", ["did"] + CTRL)
RES["baseline"] = dict(col1=pack(r1), col2=pack(r2))
BASE_DID = float(r2["b"][0])

# ============================================================
# 五、TWFE 负权重诊断
# ============================================================
Md = within2(df[["did"] + CTRL].to_numpy(), df["city"].to_numpy(),
             df["year"].to_numpy())
dres = Md[:, 0] - Md[:, 1:] @ np.linalg.lstsq(Md[:, 1:], Md[:, 0], rcond=None)[0]
treated_mask = df["did"].to_numpy() > 0.5
eps_t = dres[treated_mask]
w_it = eps_t / eps_t.sum()
neg = w_it < 0
RES["neg_weight"] = dict(
    treated_cells=int(treated_mask.sum()),
    negative_cells=int(neg.sum()),
    negative_share=round(float(neg.mean()), 4),
    negative_weight_sum=round(float(w_it[neg].sum()), 4),
    positive_weight_sum=round(float(w_it[~neg].sum()), 4))

# ============================================================
# 六、Sun–Abraham 交互加权事件研究
# ============================================================
EMIN, EMAX = -5, 6
cohorts = sorted(int(g) for g in np.unique(G) if g > 0)
inter_cols, inter_key = [], []
for g in cohorts:
    for e in range(EMIN, EMAX + 1):
        if e == -1:
            continue
        yr = g + e
        if yr < 2011 or yr > 2023:
            continue
        col = ((df["G"] == g) & (df["year"] == yr)).astype(float).to_numpy()
        if e == EMIN:
            col = ((df["G"] == g) & (df["year"] <= yr)).astype(float).to_numpy()
        if e == EMAX:
            col = ((df["G"] == g) & (df["year"] >= yr)).astype(float).to_numpy()
        if col.sum() == 0:
            continue
        inter_cols.append(col)
        inter_key.append((g, e))
Xsa = np.column_stack(inter_cols + [df[c].to_numpy() for c in CTRL])
Msa = within2(np.column_stack([df["gtfp"].to_numpy(), Xsa]),
              df["city"].to_numpy(), df["year"].to_numpy())
rsa = ols_cluster(Msa[:, 0], Msa[:, 1:], df["city"].to_numpy(),
                  absorbed=N + T - 1)
bsa, Vsa = rsa["b"], rsa["V"]
gsize = {g: int((G == g).sum()) for g in cohorts}

event = []
for e in range(EMIN, EMAX + 1):
    if e == -1:
        event.append(dict(e=e, coef=0.0, se=0.0, t=0.0, p=1.0, lo=0.0, hi=0.0))
        continue
    sel = [(i, g) for i, (g, ee) in enumerate(inter_key) if ee == e]
    if not sel:
        continue
    tot = sum(gsize[g] for _, g in sel)
    wvec = np.zeros(len(bsa))
    for i, g in sel:
        wvec[i] = gsize[g] / tot
    coef = float(wvec @ bsa)
    se = float(np.sqrt(wvec @ Vsa @ wvec))
    tv = coef / se
    event.append(dict(e=e, coef=round(coef, 4), se=round(se, 4),
                      t=round(tv, 4),
                      p=round(float(2 * stats.t.sf(abs(tv), N - 1)), 4),
                      lo=round(coef - 1.96 * se, 4),
                      hi=round(coef + 1.96 * se, 4)))
RES["event_study_sa"] = event
pre = [d for d in event if d["e"] < -1]

# ---- 平行趋势的联合检验 ----
# （a）聚合后的各前期动态效应联合为零；（b）全部队列×前期交互项联合为零
Ragg = []
for d in pre:
    sel = [(i, g) for i, (g, ee) in enumerate(inter_key) if ee == d["e"]]
    tot = sum(gsize[g] for _, g in sel)
    wv = np.zeros(len(bsa))
    for i, g in sel:
        wv[i] = gsize[g] / tot
    Ragg.append(wv)
Ragg = np.array(Ragg)
th_pre = Ragg @ bsa
W_agg = float(th_pre @ np.linalg.pinv(Ragg @ Vsa @ Ragg.T) @ th_pre)
q_agg = Ragg.shape[0]

idx_pre = [i for i, (g, ee) in enumerate(inter_key) if ee < -1]
b_pre = bsa[idx_pre]
W_all = float(b_pre @ np.linalg.pinv(Vsa[np.ix_(idx_pre, idx_pre)]) @ b_pre)
q_all = len(idx_pre)

# ---- 一致置信带（sup-t band, Montiel Olea & Plagborg-Møller, 2019）----
# 用独立的随机数发生器，以免影响主流程中其余结果的可复现性
RNG_BAND = np.random.default_rng(90210)
plot_es = [d["e"] for d in event if d["e"] != -1]
Rall = []
for e in plot_es:
    sel = [(i, g) for i, (g, ee) in enumerate(inter_key) if ee == e]
    tot = sum(gsize[g] for _, g in sel)
    wv = np.zeros(len(bsa))
    for i, g in sel:
        wv[i] = gsize[g] / tot
    Rall.append(wv)
Rall = np.array(Rall)
Vth = Rall @ Vsa @ Rall.T
se_th = np.sqrt(np.diag(Vth))
Dinv = np.diag(1.0 / se_th)
Corr = Dinv @ Vth @ Dinv
wc, Qc = np.linalg.eigh((Corr + Corr.T) / 2)
Corr = Qc @ np.diag(np.clip(wc, 1e-10, None)) @ Qc.T
zdraw = RNG_BAND.multivariate_normal(np.zeros(len(plot_es)), Corr,
                                     size=20000, method="eigh")
CSUPT_SA = float(np.quantile(np.abs(zdraw).max(axis=1), 0.95))
for d in event:
    if d["e"] == -1:
        d["supt_lo"], d["supt_hi"] = 0.0, 0.0
        continue
    j = plot_es.index(d["e"])
    d["supt_lo"] = round(d["coef"] - CSUPT_SA * float(se_th[j]), 4)
    d["supt_hi"] = round(d["coef"] + CSUPT_SA * float(se_th[j]), 4)
RES["supt_sa"] = round(CSUPT_SA, 4)

# 基期（e = −1）上处理组被解释变量的均值，用于把系数换算为相对幅度
Ygrid = df["gtfp"].to_numpy().reshape(N, T)
base_vals = [Ygrid[i, int(g - 1 - 2011)] for i, g in enumerate(G) if g > 0]
RES["base_period_mean"] = round(float(np.mean(base_vals)), 4)

RES["pretrend_joint"] = dict(
    n_pre=len(pre),
    max_abs_t=round(max(abs(d["t"]) for d in pre), 4),
    all_insignificant=bool(all(d["p"] > 0.1 for d in pre)),
    wald_aggregated=dict(stat=round(W_agg, 4), df=q_agg,
                         p=round(float(stats.chi2.sf(W_agg, q_agg)), 4),
                         F=round(W_agg / q_agg, 4),
                         p_F=round(float(stats.f.sf(W_agg / q_agg, q_agg,
                                                    N - 1)), 4)),
    wald_all_cohorts=dict(stat=round(W_all, 4), df=q_all,
                          p=round(float(stats.chi2.sf(W_all, q_all)), 4),
                          F=round(W_all / q_all, 4),
                          p_F=round(float(stats.f.sf(W_all / q_all, q_all,
                                                     N - 1)), 4)))

# ============================================================
# 七、Callaway–Sant'Anna 双重稳健组时 ATT
# ============================================================
Ymat = df["gtfp"].to_numpy().reshape(N, T)
Cmat = {c: df[c].to_numpy().reshape(N, T) for c in CTRL}
tinv = np.column_stack([z(relief), z(post84), admin, resource,
                        (region == 0).astype(float)])


def cs_estimate(idx_units, Yin, Cin, Gin, tinv_in):
    """以从未处理城市为对照组的双重稳健 ATT(g,t)。"""
    out = {}
    never = Gin[idx_units] == 0
    for g in cohorts:
        gi = Gin[idx_units] == g
        if gi.sum() < 5 or never.sum() < 5:
            continue
        sub = gi | never
        d = gi[sub].astype(float)
        b = int(g - 1 - 2011)
        Xb = np.column_stack([Cin[c][idx_units][sub, b] for c in CTRL]
                             + [tinv_in[idx_units][sub]])
        Xb = (Xb - Xb.mean(0)) / np.where(Xb.std(0) == 0, 1, Xb.std(0))
        ps = np.clip(logit_irls(Xb, d), 0.01, 0.99)
        w1 = d / d.mean()
        w0raw = (1 - d) * ps / (1 - ps)
        w0 = w0raw / w0raw.mean()
        Xc = np.column_stack([np.ones(sub.sum()), Xb])
        for ti in range(T):
            if ti == b:
                continue
            dY = Yin[idx_units][sub, ti] - Yin[idx_units][sub, b]
            ctrl = d < 0.5
            beta = np.linalg.lstsq(Xc[ctrl], dY[ctrl], rcond=None)[0]
            m = Xc @ beta
            out[(g, int(YEARS[ti]))] = float(np.mean((w1 - w0) * (dY - m)))
    return out


def cs_aggregate(attgt):
    overall_num = overall_den = 0.0
    dyn = {}
    bygroup = {}
    for (g, yr), v in attgt.items():
        e = yr - g
        ng = gsize[g]
        if e >= 0:
            overall_num += ng * v
            overall_den += ng
            bygroup.setdefault(g, [0.0, 0.0])
            bygroup[g][0] += v
            bygroup[g][1] += 1
        if EMIN <= e <= EMAX:
            dyn.setdefault(e, [0.0, 0.0])
            dyn[e][0] += ng * v
            dyn[e][1] += ng
    return (overall_num / overall_den,
            {e: s / w for e, (s, w) in dyn.items()},
            {g: s / c for g, (s, c) in bygroup.items()})


allu = np.arange(N)
attgt = cs_estimate(allu, Ymat, Cmat, G, tinv)
cs_overall, cs_dyn, cs_group = cs_aggregate(attgt)

NBOOT = 400
boot_overall = np.empty(NBOOT)
boot_dyn = {e: np.empty(NBOOT) for e in cs_dyn}
boot_group = {g: np.empty(NBOOT) for g in cs_group}
for bidx in range(NBOOT):
    idx = RNG.integers(0, N, N)
    try:
        a = cs_estimate(idx, Ymat, Cmat, G, tinv)
        o, dn, gp = cs_aggregate(a)
    except Exception:
        o, dn, gp = np.nan, {}, {}
    boot_overall[bidx] = o
    for e in boot_dyn:
        boot_dyn[e][bidx] = dn.get(e, np.nan)
    for g in boot_group:
        boot_group[g][bidx] = gp.get(g, np.nan)


def bse(arr):
    arr = arr[np.isfinite(arr)]
    return float(np.std(arr, ddof=1))


se_o = bse(boot_overall)
RES["cs_overall"] = dict(coef=round(cs_overall, 4), se=round(se_o, 4),
                         t=round(cs_overall / se_o, 4),
                         p=round(float(2 * stats.norm.sf(abs(cs_overall / se_o))), 4),
                         star=star(2 * stats.norm.sf(abs(cs_overall / se_o))),
                         nboot=NBOOT)
# 一致置信带：以自助分布上各期标准化偏离的最大值的 95% 分位数为临界值
es_sorted = sorted(cs_dyn)
Zmat = np.column_stack([(boot_dyn[e] - cs_dyn[e]) / bse(boot_dyn[e])
                        for e in es_sorted])
Zmat = Zmat[np.isfinite(Zmat).all(axis=1)]
CSUPT_CS = float(np.quantile(np.abs(Zmat).max(axis=1), 0.95))
RES["supt_cs"] = round(CSUPT_CS, 4)
RES["cs_dynamic"] = [
    dict(e=e, coef=round(cs_dyn[e], 4), se=round(bse(boot_dyn[e]), 4),
         t=round(cs_dyn[e] / bse(boot_dyn[e]), 4),
         lo=round(cs_dyn[e] - 1.96 * bse(boot_dyn[e]), 4),
         hi=round(cs_dyn[e] + 1.96 * bse(boot_dyn[e]), 4),
         supt_lo=round(cs_dyn[e] - CSUPT_CS * bse(boot_dyn[e]), 4),
         supt_hi=round(cs_dyn[e] + CSUPT_CS * bse(boot_dyn[e]), 4))
    for e in es_sorted]
RES["cs_bygroup"] = [
    dict(g=int(g), n=gsize[g], coef=round(cs_group[g], 4),
         se=round(bse(boot_group[g]), 4),
         t=round(cs_group[g] / bse(boot_group[g]), 4),
         star=star(2 * stats.norm.sf(abs(cs_group[g] / bse(boot_group[g])))))
    for g in sorted(cs_group)]

# ============================================================
# 八、PSM-DID
# ============================================================
base_idx = 0
Xps = np.column_stack([Cmat[c][:, base_idx] for c in CTRL] + [tinv])
Xps = (Xps - Xps.mean(0)) / Xps.std(0)
ever = (G > 0).astype(float)
ps_all = logit_irls(Xps, ever)


def std_bias(Xm, dvec):
    t_, c_ = Xm[dvec > 0.5], Xm[dvec < 0.5]
    return 100 * (t_.mean(0) - c_.mean(0)) / np.sqrt(
        (t_.var(0, ddof=1) + c_.var(0, ddof=1)) / 2)


bias_before = std_bias(Xps, ever)
tr_i = np.where(ever > 0.5)[0]
ct_i = np.where(ever < 0.5)[0]
lps = np.log(ps_all / (1 - ps_all))
lo_sup = max(lps[tr_i].min(), lps[ct_i].min())
hi_sup = min(lps[tr_i].max(), lps[ct_i].max())
h = 0.06 * lps.std()                                            # 核匹配带宽
uw = np.zeros(N)
matched_t = []
for i in tr_i:
    if not (lo_sup <= lps[i] <= hi_sup):
        continue
    u = (lps[ct_i] - lps[i]) / h
    kern = np.where(np.abs(u) < 1, 0.75 * (1 - u ** 2), 0.0)     # Epanechnikov 核
    if kern.sum() <= 0:
        continue
    matched_t.append(i)
    uw[ct_i] += kern / kern.sum()
matched_t = np.array(matched_t)
uw[matched_t] = 1.0
used_c = np.where((uw > 0) & (ever < 0.5))[0]
mt, mc = Xps[matched_t], Xps[used_c]
wc = uw[used_c]
bias_after = 100 * (mt.mean(0) - np.average(mc, axis=0, weights=wc)) / np.sqrt(
    (mt.var(0, ddof=1) + mc.var(0, ddof=1)) / 2)
keep_units = np.unique(np.concatenate([matched_t, used_c]))
dfm = df[df["city"].isin(keep_units)].copy()
dfm["psw"] = uw[dfm["city"].to_numpy()]
rpsm = wls_fe(dfm, "gtfp", ["did"] + CTRL, dfm["psw"].to_numpy())
RES["psm_did"] = dict(result=pack(rpsm, ["did"]),
                      matched_cities=int(len(keep_units)),
                      matched_treated=int(len(matched_t)),
                      matched_control=int(len(used_c)),
                      mean_abs_bias_before=round(float(np.mean(np.abs(bias_before))), 2),
                      mean_abs_bias_after=round(float(np.mean(np.abs(bias_after))), 2),
                      max_abs_bias_after=round(float(np.max(np.abs(bias_after))), 2))

# ============================================================
# 九、随机化推断安慰剂检验
# ============================================================
NPLACEBO = 500
placebo = np.empty(NPLACEBO)
Wctrl = within2(df[CTRL].to_numpy(), df["city"].to_numpy(), df["year"].to_numpy())
ygw = within2(df["gtfp"].to_numpy(), df["city"].to_numpy(), df["year"].to_numpy()).ravel()
for bidx in range(NPLACEBO):
    Gp = RNG.permutation(G)
    dp = ((Gp[city] > 0) & (year >= Gp[city])).astype(float)
    Xp = within2(np.column_stack([dp, df[CTRL].to_numpy()]),
                 df["city"].to_numpy(), df["year"].to_numpy())
    bb = np.linalg.lstsq(Xp, ygw, rcond=None)[0]
    placebo[bidx] = bb[0]
RES["placebo"] = dict(
    n=NPLACEBO, mean=round(float(placebo.mean()), 4),
    sd=round(float(placebo.std(ddof=1)), 4),
    p_two_sided=round(float(np.mean(np.abs(placebo) >= abs(BASE_DID))), 4),
    p_one_sided=round(float(np.mean(placebo >= BASE_DID)), 4),
    actual=round(BASE_DID, 4))
pd.DataFrame(dict(b=placebo)).to_csv(
    os.path.join(ROOT, "results", "p3_placebo.csv"), index=False)

# ============================================================
# 十、内生性：Bartik 类工具变量
# ============================================================
natl = np.array([1, 2, 4, 8, 15, 26, 42, 68, 102, 146, 175, 198, 214],
                dtype=float)
natl = natl / natl.max()
df["iv1"] = df["post84"] * np.tile(natl, N)
df["iv2"] = -df["relief"] * np.tile(natl, N)
Miv = within2(df[["gtfp", "did", "iv1", "iv2"] + CTRL].to_numpy(),
              df["city"].to_numpy(), df["year"].to_numpy())
yw, dw, ivw, ctlw = Miv[:, 0], Miv[:, 1], Miv[:, 2:4], Miv[:, 4:]
Z = np.column_stack([ivw, ctlw])
Xen = np.column_stack([dw, ctlw])
# 第一阶段
fs = ols_cluster(dw, Z, df["city"].to_numpy(), absorbed=N + T - 1)
fs_r = ols_cluster(dw, ctlw, df["city"].to_numpy(), absorbed=N + T - 1)
ssr_u = float(fs["resid"] @ fs["resid"])
ssr_r = float(fs_r["resid"] @ fs_r["resid"])
dof_u = len(yw) - Z.shape[1] - (N + T - 1)
Fstat = ((ssr_r - ssr_u) / 2) / (ssr_u / dof_u)
# 两阶段最小二乘
PZ = Z @ np.linalg.pinv(Z.T @ Z) @ Z.T
Xhat = np.column_stack([PZ @ dw, ctlw])
b2 = np.linalg.pinv(Xhat.T @ Xen) @ (Xhat.T @ yw)
e2 = yw - Xen @ b2
A = np.linalg.pinv(Xhat.T @ Xen)
meat = np.zeros((Xen.shape[1], Xen.shape[1]))
for gidx in pd.Series(np.arange(len(yw))).groupby(df["city"].to_numpy()).apply(
        lambda s: s.to_numpy()):
    s = Xhat[gidx].T @ e2[gidx]
    meat += np.outer(s, s)
Nc = df["city"].nunique()
V2 = A @ meat @ A.T * (Nc / (Nc - 1.0))
se2 = np.sqrt(np.diag(V2))
t2 = b2 / se2
# Hansen 过度识别检验
gbar = Z.T @ e2 / len(yw)
S = np.zeros((Z.shape[1], Z.shape[1]))
for gidx in pd.Series(np.arange(len(yw))).groupby(df["city"].to_numpy()).apply(
        lambda s: s.to_numpy()):
    s = Z[gidx].T @ e2[gidx]
    S += np.outer(s, s)
J = float(len(yw) ** 2 * gbar @ np.linalg.pinv(S) @ gbar)
RES["iv"] = dict(
    first_stage=dict(iv1=dict(coef=round(float(fs["b"][0]), 4),
                              t=round(float(fs["t"][0]), 4),
                              star=star(fs["p"][0])),
                     iv2=dict(coef=round(float(fs["b"][1]), 4),
                              t=round(float(fs["t"][1]), 4),
                              star=star(fs["p"][1])),
                     F=round(float(Fstat), 3)),
    second_stage=dict(coef=round(float(b2[0]), 4), se=round(float(se2[0]), 4),
                      t=round(float(t2[0]), 4),
                      p=round(float(2 * stats.norm.sf(abs(t2[0]))), 4),
                      star=star(2 * stats.norm.sf(abs(t2[0])))),
    hansen_J=round(J, 4),
    hansen_p=round(float(stats.chi2.sf(J, 1)), 4),
    N=int(len(yw)))

# ============================================================
# 十一、稳健性检验
# ============================================================
rob = {}
rob["ctrl_policy"] = pack(
    twfe(df, "gtfp", ["did"] + CTRL + ["lowcarbon", "broadband", "smartcity"]),
    ["did", "lowcarbon", "broadband", "smartcity"])
rob["alt_y"] = pack(twfe(df, "gtfp_alt", ["did"] + CTRL), ["did"])
dfw = df.copy()
for v in ["gtfp"] + CTRL:
    lo, hi = dfw[v].quantile([0.01, 0.99])
    dfw[v] = dfw[v].clip(lo, hi)
rob["winsor"] = pack(twfe(dfw, "gtfp", ["did"] + CTRL), ["did"])
rob["drop_admin"] = pack(
    twfe(df[df["admin"] < 0.5], "gtfp", ["did"] + CTRL), ["did"])
rob["drop_2020"] = pack(
    twfe(df[df["year"] != 2020], "gtfp", ["did"] + CTRL), ["did"])
rob["intensity"] = pack(twfe(df, "gtfp", ["openvol"] + CTRL), ["openvol"])
rob["drop_late"] = pack(
    twfe(df[(df["G"] == 0) | (df["G"] <= 2020)], "gtfp", ["did"] + CTRL), ["did"])
RES["robustness"] = rob

# ============================================================
# 十二、空间溢出（SUTVA）检验
# ============================================================
r_sp = twfe(df, "gtfp", ["did", "wdid"] + CTRL)
RES["spillover"] = pack(r_sp, ["did", "wdid"])
wbar = df.groupby("city")["wdid"].mean().to_numpy()
nt_mask = G == 0
cut = np.median(wbar[nt_mask])
drop_units = np.where(nt_mask & (wbar > cut))[0]
dfnb = df[~df["city"].isin(drop_units)]
RES["spillover_clean"] = pack(twfe(dfnb, "gtfp", ["did"] + CTRL), ["did"])
RES["spillover_clean"]["cities"] = int(dfnb["city"].nunique())
RES["spillover_clean"]["dropped"] = int(len(drop_units))

# ============================================================
# 十三、机制检验（两步法）
# ============================================================
mech = {}
for m in ["alloc", "ginno", "supv"]:
    mech[m] = pack(twfe(df, m, ["did"] + CTRL), ["did"])
RES["mechanism"] = mech

# ============================================================
# 十四、异质性检验
# ============================================================
het = {}
splits = [
    ("east", df["region"] == 0, "midwest", df["region"] > 0),
    ("large", df["lnpop0"] >= np.median(lnpop0), "small",
     df["lnpop0"] < np.median(lnpop0)),
    ("nonresource", df["resource"] < 0.5, "resource", df["resource"] > 0.5),
]
for n1, m1, n2, m2 in splits:
    het[n1] = pack(twfe(df[m1], "gtfp", ["did"] + CTRL), ["did"])
    het[n2] = pack(twfe(df[m2], "gtfp", ["did"] + CTRL), ["did"])
    b1, s1 = het[n1]["did"]["coef"], het[n1]["did"]["se"]
    b2_, s2_ = het[n2]["did"]["coef"], het[n2]["did"]["se"]
    zz = (b1 - b2_) / np.sqrt(s1 ** 2 + s2_ ** 2)
    het[f"{n1}_vs_{n2}_z"] = round(float(zz), 4)
    het[f"{n1}_vs_{n2}_p"] = round(float(2 * stats.norm.sf(abs(zz))), 4)
RES["heterogeneity"] = het

# ============================================================
# 十五、输出
# ============================================================
os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
with open(os.path.join(ROOT, "results", "p3_results.json"), "w",
          encoding="utf-8") as f:
    json.dump(RES, f, ensure_ascii=False, indent=1)
pd.DataFrame(RES["event_study_sa"]).to_csv(
    os.path.join(ROOT, "results", "p3_event.csv"), index=False)
pd.DataFrame(RES["cs_dynamic"]).to_csv(
    os.path.join(ROOT, "results", "p3_cs_dynamic.csv"), index=False)
df.to_csv(os.path.join(ROOT, "results", "p3_panel.csv"), index=False)

print("基准 DID：", RES["baseline"]["col2"]["did"])
print("负权重：", RES["neg_weight"])
print("CS 总体 ATT：", RES["cs_overall"])
print("事件研究（前期）：", [(d["e"], d["coef"], d["t"]) for d in event if d["e"] < 0])
print("事件研究（后期）：", [(d["e"], d["coef"], d["t"]) for d in event if d["e"] >= 0])
print("PSM-DID：", RES["psm_did"])
print("安慰剂：", RES["placebo"])
print("IV：", RES["iv"])
print("溢出：", RES["spillover"])
print("机制：", RES["mechanism"])
print("异质性：", {k: v for k, v in het.items() if isinstance(v, float)})
print("稳健性：", {k: v.get("did", v.get("openvol")) for k, v in rob.items()})
print("异质性系数：", {k: v["did"] for k, v in het.items() if isinstance(v, dict)})
print("真实处理效应均值（处理组）：",
      round(float(df.loc[df["did"] > 0.5, "te"].mean()), 4))
print("队列规模：", cohort_sizes, " 从未处理：", N - n_treated)
